# Research 02: Nepal prior work (Thapa and Giri)

_29 Oct 2026. Follows on from [01-landscape](./01-landscape.md)._

**Access caveat:** the full texts were **not read**. nepjol.info, which hosts the JACEM paper, can't be reached from our research environment, and the IEEE paper is paywalled. Everything below comes from the paper abstracts, citation listings and news coverage. **Next step:** get the PDFs, either through IEEE or NepJOL access or by emailing the authors, and check every number below.

---

## A. Thapa, Madan Bhandari University ("EdgeYOLO")

- **Paper:** "Real-Time Monkey Detection Using YOLO with Slack Alerts for Crop Protection", IEEE Xplore ([doc 11485402](https://ieeexplore.ieee.org/abstract/document/11485402/)). It is also cited as "Real-time YOLO-based monkey detection with Slack alerting for crop protection in Nepal". The author list has not been checked against the paper; press coverage credits Progress Jung Thapa ([Earth Journal](https://earthjournal.com/nepal-enlists-ai-to-help-fight-against-crop-raiding-macaques/)).
- **Timeline:** 2024 to 2025, on rural farms ([AE News](https://aenewslive.com/nepal-uses-ai-technology-to-find-new-ways-of-protecting-crops-from-monkey-raids/)).
- **Hardware:** **Raspberry Pi 5 and a USB camera**. No accelerator is mentioned in the abstract.
- **Model:** **YOLOv8n** detector. Mongabay describes a "second layer" that classifies behaviour into movement, vigilance and feeding. It is unclear whether that is a separate classifier or extra detector classes.
- **Data:** more than **4,000 annotated images**. The source, the class balance and whether the dataset is public are all unknown.
- **Results (abstract):**
  - **91.7% mAP@0.5** on the test set
  - **About 88% accuracy in the field** across 28 sessions
  - **15 to 22 FPS** on the Pi 5, depending on optimisation settings
- **Output:** an alert to the farmer through **Slack**. There is **no deterrent**, and a human decides what to do.
- **Limitations they report:** rain and dense foliage reduce accuracy. Farmers who are short of labour may not be able to act on alerts ([Mongabay](https://news.mongabay.com/2026/07/monkey-vs-machine-nepal-tests-ai-to-fight-crop-raiding-macaques/)).
- **A claim to verify:** the abstract says losses reach **45% of yields** in the mid-hills. This is far above the 5 to 10% of income in the Kavre study, and the definitions probably differ (worst-case yield loss versus average income loss). Check what source the paper cites.

**What it means for us:**
- A Pi 5 running YOLOv8n is a **proven baseline**: about 90% mAP and real-time speed. We don't need to research whether detection is possible. We can reproduce this baseline and spend our effort on the deterrent loop.
- Slack is a poor fit for rural farmers. Use SMS or Viber instead, and plan a voice call for people who can't read.
- Their weak spots (rain, foliage) suggest adding night/IR testing and weather augmentation to our evaluation plan.

## B. Giri et al., Pulchowk Campus, Tribhuvan University

- **Paper:** Santosh Giri, Bikal Adhikari, Binaya Basnet, Binit K.C. and Rajesh Subedi, "Design and Development of an AI-Driven Solution for Rhesus Macaque…", *Journal of Advanced College of Engineering and Management* (JACEM), **vol. 12, pp. 73–87**, DOI [10.3126/jacem.v12i01.93908](https://doi.org/10.3126/jacem.v12i01.93908).
- **System:** monkey detection that **switches on an ultrasonic deterrent automatically** ([Mongabay](https://news.mongabay.com/2026/07/monkey-vs-machine-nepal-tests-ai-to-fight-crop-raiding-macaques/)).
- **Status:** it has **not been tested on working farms**.
- **Unknown until we read the full text:** the model, the hardware, the ultrasonic frequency and output level, the effective range, and how it was evaluated.

**What it means for us:** this is the nearest thing to our closed loop, and it rests on ultrasound, the deterrent with the weakest support (see 01, §3). When we read the paper, check one thing first: **whether its frequency is below about 42 kHz**, the upper limit of rhesus hearing.

## C. Related builds found along the way

| Project | Stack | Deterrent | Number |
|---|---|---|---|
| Malaysian university, Pi 4 ([USM](https://erepo.usm.my/items/33ae78ac-d061-417c-b616-c4061c4fb575)) | YOLOv8 and a webcam | Piezo buzzer designed for **45 kHz** | precision 0.845 |
| SMART REPELLER ([ResearchGate](https://www.researchgate.net/publication/377320647_SMART_REPELLER_A_Smart_system_to_prevent_Rhesus_Macaque_Trespassing_in_Human_Settlements_and_Agricultural_Areas)) | YOLOv5 | Ultrasonic plus a calcium-carbide cannon | precision 0.888 |
| [SentaFito53 on GitHub](https://github.com/SentaFito53/real-time-monkey-intrusion-detection-and-defensive-response-yolov8-coral-edgeTPU) | Pi 5, Coral USB TPU, YOLOv8, two cameras | Gunshot audio | Open source, so we can read it |

The Malaysian 45 kHz design sits **above** the roughly 42 kHz limit of rhesus hearing. It is a concrete example of the ultrasonic concern raised in 01.

---

## Updated takeaways

1. **Detection baseline:** reproduce YOLOv8n on a Pi 5, which reaches about 90% mAP in published work. Also test a Coral TPU to save power on solar.
2. **Where we can add something:** an **automatic deterrent that is randomised and escalates, field-tested, with the outcome of each event logged.** No Nepali project has shown this yet.
3. **Behaviour taxonomy:** adopt **moving, vigilant and feeding** to match Thapa's. It is field-tested and maps onto how urgent a response is. Vigilant means warn; feeding means deter now.
4. **Collaboration:** both groups are in Nepal. Ask Thapa about data sharing (4,000 images), and ask Giri for field-trial data on the deterrent.

## To do

- [ ] Get the full PDFs of both papers and fill in the unknowns above
- [ ] Read the SentaFito53 code
- [ ] Email Thapa and Giri
