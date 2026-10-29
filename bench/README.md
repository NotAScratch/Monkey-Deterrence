# Jetson detector benchmark

Measures how fast, and at what power, YOLO detectors run on the ROSMASTER R2's Jetson Orin NX. The point is to choose the smallest model and input size that is good enough, because power decides the field hardware (see [research 04](../docs/research/04-dev-hardware.md)).

For each model × input size × precision it builds a TensorRT engine (cached in `bench/engines/`), runs 30 warm-up frames and 300 timed frames, and samples `tegrastats` throughout. It appends one row per run to `bench/results.csv`:

| Column | Meaning |
|---|---|
| `fps`, `latency_mean_ms`, `latency_p95_ms` | End-to-end per frame: preprocessing, inference and postprocessing |
| `inference_ms` | Model only, as reported by Ultralytics |
| `power_w` | Average total module power (`VDD_IN`) while running |
| `idle_w`, `inference_power_w` | Power before the run, and the extra power the model costs |
| `gpu_util_pct` | Average GPU load |

## Setup on the robot

Needs JetPack 6 with Ultralytics installed for Jetson. Follow the [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/); plain `pip install ultralytics` installs a PyTorch without GPU support on Jetson.

```bash
python3 -c "import torch; print(torch.cuda.is_available())"
```

That should print `True`.

## Running

Run once per power mode. Changing mode may need a reboot, and the current mode is recorded in each row. List the modes with `sudo nvpmodel -p --verbose`, set one with:

```bash
sudo nvpmodel -m 0
```

Then:

```bash
cd ~/Monkey-Deterrence
python3 bench/jetson_bench.py --models yolo11n yolo11s yolo11m --imgsz 320 640 --pytorch
```

The first run takes a while: each TensorRT export takes a few minutes.

Optional:
- `--precision fp16 int8`: also try INT8. Calibration here uses the small `coco8` set, so treat INT8 accuracy as unknown until we calibrate on our own footage.
- `--source path/to/folder_or_video.mp4`, or `--source 0` for a camera: use real frames. The number of detections slightly affects postprocessing time.
- Keep the robot on a charger and close other programs (ROS nodes, the desktop) for stable numbers.

Commit `bench/results.csv` when done. The engines are ignored by git.
