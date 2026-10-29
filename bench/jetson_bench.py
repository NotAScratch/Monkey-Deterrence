#!/usr/bin/env python3
"""Benchmark YOLO detectors on a Jetson: speed and power per model / input size / precision.

Run once per power mode (see bench/README.md). Results are appended to a CSV so
runs from different modes end up in one table.

Example:
    python3 bench/jetson_bench.py --models yolo11n yolo11s yolo11m --imgsz 320 640
"""
import argparse
import csv
import platform
import re
import shutil
import statistics
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

import cv2

# tegrastats prints e.g. "VDD_IN 5640mW/5702mW": current/average for the whole module.
POWER_RE = re.compile(r"VDD_IN (\d+)mW")
GPU_RE = re.compile(r"GR3D_FREQ (\d+)%")


def parse_tegrastats(line):
    """Return (total_power_mW, gpu_util_pct) from one tegrastats line; None where missing."""
    p = POWER_RE.search(line)
    g = GPU_RE.search(line)
    return (int(p.group(1)) if p else None, int(g.group(1)) if g else None)


class PowerSampler:
    """Reads tegrastats in the background while a benchmark runs."""

    def __init__(self, interval_ms=100):
        self.interval_ms = interval_ms
        self.proc = None
        self.samples = []
        self._thread = None

    def __enter__(self):
        if shutil.which("tegrastats") is None:
            print("[warn] tegrastats not found: power will not be recorded")
            return self
        self.proc = subprocess.Popen(
            ["tegrastats", "--interval", str(self.interval_ms)],
            stdout=subprocess.PIPE, text=True)
        self._thread = threading.Thread(target=self._read, daemon=True)
        self._thread.start()
        return self

    def _read(self):
        for line in self.proc.stdout:
            self.samples.append(parse_tegrastats(line))

    def __exit__(self, *exc):
        if self.proc:
            self.proc.terminate()
            self.proc.wait()

    def summary(self):
        power = [p for p, _ in self.samples if p is not None]
        gpu = [g for _, g in self.samples if g is not None]
        return (statistics.mean(power) if power else None,
                statistics.mean(gpu) if gpu else None)


def idle_power(seconds):
    """Average module power with nothing running, to subtract from inference power."""
    with PowerSampler() as s:
        time.sleep(seconds)
    return s.summary()[0]


def power_mode():
    try:
        out = subprocess.run(["nvpmodel", "-q"], capture_output=True, text=True).stdout
        m = re.search(r"NV Power Mode: (\S+)", out)
        return m.group(1) if m else "unknown"
    except FileNotFoundError:
        return "not-jetson"


def load_frames(source, limit):
    """Load frames into memory so disk/camera speed doesn't count as inference time."""
    if source is None:
        from ultralytics.utils import ASSETS
        img = cv2.imread(str(ASSETS / "bus.jpg"))
        return [img]
    path = Path(source)
    if path.is_dir():
        files = sorted(f for f in path.iterdir()
                       if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"})
        return [cv2.imread(str(f)) for f in files[:limit]]
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    frames = []
    while len(frames) < limit:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame)
    cap.release()
    if not frames:
        raise SystemExit(f"no frames read from {source}")
    return frames


def build_engine(model_name, imgsz, precision, engine_dir):
    """Export a TensorRT engine once and cache it; engines are fixed to one input size."""
    from ultralytics import YOLO
    engine = engine_dir / f"{model_name}_{imgsz}_{precision}.engine"
    if engine.exists():
        return engine
    print(f"[export] {engine.name} (several minutes on first run)")
    exported = YOLO(f"{model_name}.pt").export(
        format="engine", imgsz=imgsz,
        half=precision == "fp16", int8=precision == "int8",
        data="coco8.yaml" if precision == "int8" else None)
    engine_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(exported, engine)
    return engine


def bench_one(weights, imgsz, frames, warmup, iters):
    from ultralytics import YOLO
    model = YOLO(str(weights), task="detect")
    for i in range(warmup):
        model.predict(frames[i % len(frames)], imgsz=imgsz, verbose=False)

    latencies, infer = [], []
    with PowerSampler() as sampler:
        for i in range(iters):
            t0 = time.perf_counter()
            r = model.predict(frames[i % len(frames)], imgsz=imgsz, verbose=False)
            latencies.append((time.perf_counter() - t0) * 1000)
            infer.append(r[0].speed["inference"])
    power_mw, gpu_pct = sampler.summary()

    latencies.sort()
    mean_ms = statistics.mean(latencies)
    return {
        "fps": round(1000 / mean_ms, 1),
        "latency_mean_ms": round(mean_ms, 2),
        "latency_p95_ms": round(latencies[int(0.95 * (len(latencies) - 1))], 2),
        "inference_ms": round(statistics.mean(infer), 2),
        "power_w": round(power_mw / 1000, 2) if power_mw else None,
        "gpu_util_pct": round(gpu_pct) if gpu_pct is not None else None,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="+", default=["yolo11n", "yolo11s", "yolo11m"])
    ap.add_argument("--imgsz", nargs="+", type=int, default=[320, 640])
    ap.add_argument("--precision", nargs="+", default=["fp16"],
                    choices=["fp32", "fp16", "int8"])
    ap.add_argument("--pytorch", action="store_true",
                    help="also benchmark the plain .pt model (no TensorRT) for comparison")
    ap.add_argument("--source", help="image folder, video file or camera index; default: sample image")
    ap.add_argument("--frames", type=int, default=200, help="max frames to load from --source")
    ap.add_argument("--warmup", type=int, default=30)
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--idle-seconds", type=float, default=5)
    ap.add_argument("--engines", type=Path, default=Path("bench/engines"))
    ap.add_argument("--out", type=Path, default=Path("bench/results.csv"))
    args = ap.parse_args()

    frames = load_frames(args.source, args.frames)
    mode = power_mode()
    idle = idle_power(args.idle_seconds)
    idle_w = round(idle / 1000, 2) if idle else None
    print(f"power mode {mode}, idle {idle_w} W, {len(frames)} frame(s)")

    runs = [(m, s, p, "tensorrt") for m in args.models for s in args.imgsz for p in args.precision]
    if args.pytorch:
        runs += [(m, s, "fp32", "pytorch") for m in args.models for s in args.imgsz]

    new_file = not args.out.exists()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", newline="") as f:
        writer = None
        for model_name, imgsz, precision, backend in runs:
            weights = (build_engine(model_name, imgsz, precision, args.engines)
                       if backend == "tensorrt" else f"{model_name}.pt")
            res = bench_one(weights, imgsz, frames, args.warmup, args.iters)
            row = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "host": platform.node(), "power_mode": mode,
                "model": model_name, "backend": backend, "precision": precision,
                "imgsz": imgsz, **res, "idle_w": idle_w,
                "inference_power_w": round(res["power_w"] - idle_w, 2)
                if res["power_w"] and idle_w else None,
                "source": args.source or "sample",
            }
            print(f"{model_name:10} {backend:8} {precision:5} {imgsz:4}px  "
                  f"{row['fps']:6} FPS  p95 {row['latency_p95_ms']} ms  {row['power_w']} W")
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=list(row))
                if new_file:
                    writer.writeheader()
            writer.writerow(row)
            f.flush()


if __name__ == "__main__":
    main()
