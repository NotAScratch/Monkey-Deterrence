# Research 04: Development hardware (Jetson Orin NX on ROSMASTER R2)

_29 Oct 2026._

**Decision:** we develop on the hardware we already own, a **Yahboom ROSMASTER R2 with an NVIDIA Jetson Orin NX Super 8 GB**. It is the same robot used in [Autonomous-Mapping-and-Navigation](https://github.com/NotAScratch/Autonomous-Mapping-and-Navigation). This replaces the Raspberry Pi 5 + Coral baseline suggested in [02](./02-nepal-prior-work.md) and [03](./03-code-review-sentafito53.md).

## What it gives us

| | Pi 5 + Coral (prior work) | Jetson Orin NX Super 8 GB |
|---|---|---|
| AI compute | Coral: about 4 TOPS int8; Pi CPU: very little | GPU + DLA, up to about 117 TOPS (sparse INT8, Super mode) |
| Runtime | TFLite int8, input 192 to 240 px | **TensorRT** (FP16 or INT8). Ultralytics exports with `format=engine` |
| Realistic model | YOLOv8n at 240 px | YOLOv8/11 **s or m at 640 px** in real time, plus a second-stage behaviour classifier |
| Power | about 5 to 15 W | about **10 to 40 W** depending on the power mode (`nvpmodel`) |
| Cameras on the R2 | — | Orbbec RGB-D depth camera (gives **distance to the monkey**), USB webcam, 2D LiDAR |

## What changes in the design

1. **Detection quality stops being limited by compute.** We can use a larger model and a higher input size, which matters for small, distant monkeys and for the rain and foliage problems Thapa reported. A two-stage design (detector, then a behaviour classifier on the crop) fits easily.
2. **The depth camera is new information.** Depth can tell us how far away a monkey is. That supports escalation by distance (for example, water only within range) and lets us measure **retreat distance** after a deterrent, a better outcome metric than "left the frame".
3. **Power is the price.** 10 to 40 W around the clock is too much for a cheap solar field unit. Plan: develop and collect data on the Orin. Then measure which model size actually needed, and decide whether field units use the Orin itself, a smaller Jetson (Orin Nano), or a Pi 5 + Coral running a distilled model.
4. **A mobile platform opens another option:** a robot that patrols or drives towards monkeys, compared with a fixed station. Unlike a fixed device, its approach is a real consequence, which may slow habituation. Open question below.

## Open questions

- [ ] Is the R2 only the development rig, or is a **mobile patrol robot** a deployment option? (Ackermann steering and a small chassis make rough farm terrain hard.)
- [ ] Check the JetPack version on the R2, and that Ultralytics + TensorRT export works on it.
- [ ] Benchmark YOLO n/s/m at 320 and 640 px: FPS and watts under each `nvpmodel` mode.
