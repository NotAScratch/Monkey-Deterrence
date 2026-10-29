# Research 01: Landscape survey

_Started 29 Oct 2026. This is a first pass from public sources. Treat the numbers as leads to verify against the original papers, not as settled facts._

This file restarts the research from scratch. It covers four questions:

1. How big is the problem in Nepal?
2. Who has already built AI detection or deterrence for monkeys, and how well does it work?
3. What does the evidence say about deterrents, especially habituation?
4. What legal constraints apply, and what data and models can we start from?

---

## 1. The problem in Nepal

- **Who raids:** rhesus macaques (*Macaca mulatta*) do the most crop damage of Nepal's three monkey species. The Assamese macaque (*M. assamensis*) also lives in Nepal and is nationally listed as **Endangered** ([Mongabay 2023](https://news.mongabay.com/2023/05/after-sri-lanka-nepal-debates-exporting-its-problematic-monkeys/)).
- **Which crops:** a 2017 study of 60 households in Kaski district found maize was raided most (31%), then potato (30%), wheat (17%), cauliflower (15%) and rice (7%) ([Kathmandu Post / CIJ, 2022](https://kathmandupost.com/investigations/2022/03/26/monkey-maize-and-man)).
- **Cost to farmers:**
  - In Kaski, 32% of surveyed households reported losses of about Rs 20,000, and another 30% reported Rs 10,000 to 20,000 (same source).
  - In Panauti, Kavre district, losses averaged about USD 15 a year, around 5% of cropping income. For households that grew only maize, the figure was about 10% ([Dialogue Earth](https://dialogue.earth/en/nature/in-nepal-debate-rages-on-crop-raiding-monkeys/)).
  - A 2026 study found that cultivated crops made up nearly half the macaque diet in one central-Nepal region ([Mongabay, Jul 2026](https://news.mongabay.com/2026/07/monkey-vs-machine-nepal-tests-ai-to-fight-crop-raiding-macaques/)).
- **Compensation:** there is none. Farmers carry the losses themselves. A 15-member government task force was formed in May 2026 and had not reported by mid-2026 (same source).
- **What farmers do now:** they guard in turns. In Birta Deurali, villagers rotate every two hours (same source). That labour is the cost this project is trying to replace.
- **Data gap:** Nepal has no reliable estimate of its macaque population (Dialogue Earth).

**So what for us:** start with maize in the mid-hills, since it is the most raided crop and the deployment target is clear. Any unit has to cost much less than a year of losses, which can be as little as USD 15 per household. That points towards **one unit shared by a community or a ward**, not one per farmer.

## 2. Existing systems

| System | Where | What it does | Evidence |
|---|---|---|---|
| Progress Jung Thapa, Madan Bhandari University | Nepal | Camera plus a small edge device. Detects monkeys, then classifies behaviour as moving, feeding or vigilant, and sends an alert to the farmer's phone. Trained on about 4,000 annotated images. | About **88% accuracy over 28 field trials**. Rain and dense foliage hurt it. A human still decides what to do; there is no automatic deterrent. ([Mongabay](https://news.mongabay.com/short-article/2026/08/nepal-enlists-ai-to-help-fight-against-crop-raiding-macaques/)) |
| Santosh Giri, Tribhuvan University (Pulchowk) | Nepal | AI detection paired with an ultrasonic deterrent. | Prototype only; not yet tested on working farms (Mongabay). Possibly related: the JACEM paper "[Design and Development of an AI-Driven Solution for Rhesus Macaque…](https://www.nepjol.info/index.php/JACEM/article/view/93908)". **To read.** |
| Syangja municipality device | Nepal | A "machine to curb monkey menace". | A one-month trial was run, but no results were published ([Himalayan Times](https://thehimalayantimes.com/nepal/new-machine-introduced-to-curb-monkey-menace-in-syangja/)). |
| Japanese YOLOv4 system | Japan | Four cameras, solar powered, in a sweet-potato field. Alerts are sent through the LINE app. | Ran from September to November in 2022 and 2023 ([TWGrid 2024](https://indico4.twgrid.org/event/33/contributions/1381/)). |
| Mangalore Institute of Technology | India | YOLOv8 plus Swin Transformer for monkeys and bison, triggering a "humane repellent". | Student project with no field data ([KSCST synopsis](https://kscst.org.in/spp/49_series/49s_spp/Poster_Presentation_Synopsis/19_49S_BE_2786.pdf)). |
| Langur detection with VGG19 and YOLO | India | Webcam detection aimed at crop protection. | Academic only ([Springer](https://link.springer.com/chapter/10.1007/978-981-15-3383-9_34)). |
| Hackathon builds | India | Camera trigger that plays 40 to 50 rotating scare sounds, including langur calls, to slow habituation. | No deployment ([Devfolio](https://devfolio.co/projects/farm-invasion-detection-system-0e55)). |
| Ultrasonic repellers | Malaysia and Indonesia | Raspberry Pi with an ultrasonic emitter. | Small tests. One claims frequencies above 30 kHz drove monkeys away **at up to 4 m only** ([USM](https://erepo.usm.my/entities/publication/33ae78ac-d061-417c-b616-c4061c4fb575/full), [Ar-Raniry](https://jurnal.ar-raniry.ac.id/index.php/circuit/article/view/24896)). |

**What we learn from this:**
- Detection is close to solved. The closest Nepali system already gets about 88% in the field. **Nobody has field-tested a closed loop of detect, deter automatically and measure whether the monkeys come back.** That gap is where Bandar Sentinel can add something new.
- Thapa's behaviour classes (moving, feeding, vigilant) are a sensible starting taxonomy, and they have already been tried in the field. We should consider adopting them instead of our current guess of aggressive, foraging, curious and fleeing. "Aggressive" is rare and hard to label from a single camera.
- Thapa is the obvious person to contact. Possible collaboration: data sharing and comparing results.

## 3. Deterrent evidence

- **Habituation is real.** Several sources say primates habituate quickly to new stimuli, so many deterrents only work for a short time ([Conservation Evidence synthesis](https://books.openbookpublishers.com/10.11647/obp.0131/ch7.xhtml); [USM](https://erepo.usm.my/handle/123456789/21113)). We found no controlled study that measures how fast macaques habituate to sound or water. **Our own field data would be new evidence.**
- **What the field evidence supports:**
  - **Electric fencing** was the only one of six methods that kept both baboons and vervets out of a crop field in a South African trial. The same trial raised a risk to small animals ([Durham repository](https://durham-repository.worktribe.com/OutputFile/1249712)).
  - **Human guarding** is rated most effective by farmers but costs a lot of labour ([Kainji Lake, Nigeria](https://journals.unizik.edu.ng/faic/article/view/1908)).
  - **Combining methods** works better than any single method ([Barbados best practices](https://biodiversity.gov.bb/wp-content/uploads/2020/06/Best-Practices-Monkey-Deterrence-2020-V5-Pages.pdf)).
- **Ultrasonic sound is doubtful.** A rhesus audiogram puts the upper hearing limit at about **42 kHz at 60 dB SPL** ([University of Toledo audiogram](https://www.utoledo.edu/al/psychology/research/psychobio/newaudiograms/rhesusmacaque2.html)). Older animals lose high-frequency hearing ([PMC4509406](https://pmc.ncbi.nlm.nih.gov/articles/PMC4509406)). Ultrasound also fades fast in air, and the only test we found worked at about 4 m. Many cheap repellers emit above 40 kHz, which is effectively silent to a macaque. **Plan for audible sound (predator calls, alarm calls, dog barks) and a water jet as the main deterrents. Treat ultrasonic as an add-on to test, not something to rely on.**
- **Possible cheap extras:** spent coffee grounds deterred captive macaques better than neem or ocimum oil. This has not been tested in the field ([Durham](https://durham-repository.worktribe.com/OutputFile/1210150)).

**Design consequences:**
- Make the deterrent **varied and randomised by design**: change the sound, timing and combination on each event.
- **Log every event and its outcome**, for example how long until the monkeys returned. This turns the system into a habituation experiment.
- Always pair the system with a human response path, such as an alert to a guard. Automation reduces guarding; it does not replace it.

## 4. Legal and welfare constraints

- **The rhesus macaque is a protected animal** under Nepal's National Parks and Wildlife Conservation Act, and is listed in **CITES Appendix II** ([Tribune](https://www.tribuneindia.com/news/world/faced-with-increased-crop-destruction-and-simian-menace-nepal-lawmaker-suggests-selling-monkeys-to-china), [Scroll](https://scroll.in/article/1048823/nepal-takes-a-leaf-out-of-sri-lankas-book-considers-exporting-crop-raiding-monkeys)).
- The Act **does not say how to manage protected animals that damage crops**, so there is a legal grey zone. Wildlife trade offences carry 5 to 15 years in prison or fines of NRs 500,000 to 1,000,000.
- Lethal control, capture and export are out of scope and politically fraught. The 2005 export plan was reversed after a Supreme Court petition.
- **Open question:** we need confirmation from DNPWC or the Division Forest Office that **non-contact, non-harmful deterrence** (sound and a low-pressure water jet) is allowed, and whether it is still allowed near protected areas. Ask before choosing hardware.
- **Welfare limits to write into the spec:**
  - Water-jet pressure must not be able to injure an animal, especially an infant.
  - Sound levels must stay safe for people and livestock nearby.
  - **Assamese macaques (Endangered) must not be targeted.** Either the detector has to tell the two species apart, or the deployment has to stay outside their range.

## 5. Data and models

- **Public data:**
  - **MacaquePose** has more than 13,000 in-the-wild macaque images with keypoints. We can turn the keypoints into bounding boxes, and they may help with behaviour classes later ([Frontiers 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7874091/)).
  - **LILA BC** has more than 50 camera-trap datasets in COCO format. We still have to search them for primates ([arXiv 2603.20509](https://arxiv.org/pdf/2603.20509)).
  - iNaturalist and Open Images (the "Monkey" class) are also unchecked.
- **Bootstrap plan:** run **MegaDetector** over raw footage to get animal boxes, then train a small **YOLO** model on our own classes. This is a known and effective way to build a small edge model ([WildLabs](https://wildlabs.net/comment/7157); [MegaDetector](https://pypi.org/project/megadetector/5.0.6)).
- **Gap:** there is no public Nepal-context or behaviour-labelled macaque dataset. Thapa's roughly 4,000 images are the nearest. Local data collection is unavoidable.
- **Edge hardware:** there is little published work on wildlife detection on Raspberry Pi. A CVPR 2021 workshop paper is relevant: it covers quantisation and small architectures for filtering empty frames on embedded devices ([Cunha et al.](https://openaccess.thecvf.com/content/CVPR2021W/MAI/papers/Cunha_Filtering_Empty_Camera_Trap_Images_in_Embedded_Systems_CVPRW_2021_paper.pdf)). We still need to benchmark Pi 5, Jetson Orin Nano and Coral.

---

## Open questions and next research steps

1. ~~Read the full JACEM paper and Thapa's work~~: abstract-level notes in [02-nepal-prior-work.md](./02-nepal-prior-work.md); full texts still needed. Contact Thapa about data and collaboration.
2. Contact DNPWC or the Division Forest Office to confirm non-harmful deterrence is legal.
3. Look for controlled studies on habituation to deterrents (Google Scholar: "macaque deterrent habituation", "crop raiding primate deterrent evaluation"), and read Hill's group at Durham.
4. Check LILA BC, iNaturalist and Open Images for usable macaque images, and tell rhesus apart from Assamese.
5. Benchmark the edge hardware options and their power use under solar.
6. Decide the behaviour taxonomy. Proposed: adopt moving, feeding and vigilant, plus "none" and "other animal or person".
