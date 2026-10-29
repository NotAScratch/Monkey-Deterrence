# Research 03: Code review of SentaFito53's monkey deterrent

_29 Oct 2026. Repo: [SentaFito53/real-time-monkey-intrusion-detection-and-defensive-response-yolov8-coral-edgeTPU](https://github.com/SentaFito53/real-time-monkey-intrusion-detection-and-defensive-response-yolov8-coral-edgeTPU). MIT licence, © 2025 Senta Fito Situmorang. One commit (4 Aug 2025). The comments are in Indonesian. There is a [demo video](https://youtu.be/YGD9WaCn3TU)._

## What's in it

| File | What it is |
|---|---|
| `yolov8_coral/.../test.py` | **The real program**, about 150 lines. Two cameras, YOLOv8 on a Coral TPU, plays a gunshot MP3 on detection. |
| `test-backup.py`, `example.py` | Earlier versions with one camera. `example.py` is copied from a licence-plate tutorial: it still draws the label "license_plate". |
| `*.tflite` (6 files) | Models compiled for the Edge TPU: YOLOv8n at input sizes 192 and 240, plus an SSD-MobileNet v1. All int8. |
| `coco1.txt` | A single class: `monkey`. |
| `gunshot.mp3` | The deterrent sound. |
| `install-steps`, `detect_yolov8.sh`, `autostart/` | Setup steps: pyenv with Python 3.9, the `edge-tpu-silva` package, and autostart on the desktop. |

There is **no training data, no training script beyond two `yolo` commands in the README, no evaluation numbers and no logs.**

## How `test.py` works

1. **Capture:** one thread per camera (`CAMERA_INDICES = [0, 2]`), each at 640×480. Each thread writes into a queue of size 1, so only the newest frame is kept.
2. **Inference:** the main loop switches between the cameras in turn and **runs the model on only every 3rd frame** from each. It calls `model.predict(frame, imgsz=240)`, so frames are shrunk to **240 px**.
3. **Decision:** if any box has the label `monkey`, it starts `play_target_sound()` in a new thread.
4. **Deterrent:** pygame plays `gunshot.mp3`. A **1-second cooldown** is the only rate limit.
5. **Display:** `cv2.imshow` shows a window for each camera, so it needs a desktop session.

## Problems and gaps

These bear on our design.

1. **No confidence threshold.** `test.py` never sets `conf`, so Ultralytics' default of **0.25** applies. Any box with 25% confidence fires a gunshot. `example.py` used 0.6, but the version they deploy doesn't. That means a lot of false positives.
2. **The same sound every time, up to once a second.** There is no randomisation, no escalation and no limit per event. This is the worst case for habituation, and it would also be very loud for nearby people and livestock.
3. **One detection triggers it.** There is no requirement for the monkey to appear over several frames or stay in view for a while, so a single bad frame sets it off.
4. **No logging.** There is no record of when it fired, how confident it was, or whether the monkey left. You can't measure whether it works or tune it.
5. **Hard-coded paths and a GUI dependency.** The sound path is `/home/raspi/Desktop/gunshot.mp3`, and the code needs `imshow` plus a desktop autostart. It won't run headless as a service.
6. **A new thread for every detection.** The lock and cooldown hide the cost, but it's wasteful. A single worker thread with a queue would be cleaner.
7. **The input size (240 px) is small.** At that size a monkey 20 to 30 m away is only a few pixels. It trades range for speed and isn't documented.
8. **Model files are unexplained.** There are six `.tflite` files, including `_old` and `_192_monkey`, and only one is used. We don't know what data they were trained on or how well they score.

## What to reuse

- **The Pi 5 with a Coral USB TPU works**, with an int8 YOLOv8n exported via `yolo export format=edgetpu`. This agrees with Thapa's Pi 5 results (see [02](./02-nepal-prior-work.md)). The Coral should use less power per inference than the Pi's CPU, which matters on solar. **We still need to measure it.**
- **One capture thread per camera, each with a queue of size 1**, is a clean pattern for always working on the newest frame.
- **Two cameras** give wider coverage of a field. It's worth keeping as an option.
- The models are MIT-licensed. We could use them as a quick first test on our own footage, but we know nothing about their training data, so not as a baseline.

## What we do differently (design requirements)

| Gap | Bandar Sentinel requirement |
|---|---|
| conf 0.25, one frame | Confidence threshold of 0.5 or higher to start, tuned on our data. **Confirm over N of M frames** (for example 3 of 5) before acting. |
| One gunshot every second | **Event-based**: one deterrent sequence per incursion, then a lockout. Each sequence is **randomised** from a sound library (predator calls, dog barks, alarm calls) and **escalates** (sound, then louder sound, then water) only if the monkey stays. |
| No logs | Log every event to local storage: time, camera, confidence, behaviour class, deterrent chosen, **time until the monkey left**, and a short clip. Sync to the cloud when a connection is available. |
| Needs a GUI | Run headless as a systemd service, with an optional debug stream. |
| Hard-coded paths | One config file for each site. |
| Monkeys only | Classes for monkey, **person**, dog or livestock and Assamese macaque if possible, so the system **never fires at people** and leaves protected species alone. |
| No quiet hours or volume limit | Volume cap, quiet hours, and a manual override for the farmer. |

## Open questions

- [ ] Watch the demo video at 1:56 to see how the monkeys actually react to the gunshot, and where the system was deployed.
- [ ] Benchmark the Pi 5 on its CPU against the Pi 5 with Coral at input sizes 240, 320 and 640: FPS, watts, and detection range.
