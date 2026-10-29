# Bandar Sentinel

**An AI-based monkey detection and deterrence system for rural and urban Nepal.**

Bandar Sentinel watches farmland and rooftops for rhesus macaques, classifies what they're doing, and triggers a non-lethal deterrent (sound and water) before crops are raided — without needing a farmer to stand guard.

Built at [Baliyo Technologies](https://baliyotech.com).

---

## The problem

Rhesus macaques are among Nepal's top crop-raiding species. Farmers in the mid-hills report losing large shares of their maize harvest to raids every year, often with no compensation available from local government. The usual response — a person standing in the field at dawn, beating drums or waving fire — doesn't scale and doesn't last.

Existing deterrents (fixed ultrasonic emitters, scarecrows, noise) tend to work for a while and then stop, because monkeys habituate to anything that never carries a real consequence.

## What Bandar Sentinel does

A camera watches a field or rooftop continuously. When it sees a monkey, it classifies the behavior — aggressive, foraging, curious, or fleeing — and a decision engine picks a response based on that classification and how serious the threat is. The response is a randomized, escalating combination of ultrasonic sound, audible sound, and a water jet, designed specifically to resist the habituation that defeats fixed-pattern deterrents. Events are logged to a cloud dashboard so false positives can be reviewed and the system can improve over time.

```
edge capture → detection → behavior classification → decision engine → deterrence trigger → cloud monitoring
```

## Status

This project is currently in its **feasibility sprint** (Sprint 1, started 28 Sep 2026). The goal of this sprint is not a working prototype — it's to close every open question about the approach before hardware and models get locked in. That includes:

- A survey of existing detection/deterrence systems worldwide and in Nepal
- The detection and behavior-classification approach (model type, label taxonomy, dataset gaps)
- System architecture
- Hardware spec (camera, speaker, water-jet, solar power, enclosure)
- Site requirements for rural vs. urban deployment
- A regulatory and animal-welfare review (Nepal's DNPWC / Division Forest Office rules on deterring macaques)

Sprint 1 runs through **9 Oct 2026**, with a mid-sprint check-in on 2 Oct and a retro on 12 Oct. See [`docs/`](./docs) for sprint artifacts as they're produced.

Currently being developed solo, across AI/ML, hardware, backend, frontend, DevOps, and project management.

## Why this is hard

- **Habituation.** Monkeys are known to learn and ignore fixed deterrent patterns within weeks. The deterrent design has to randomize and escalate from day one.
- **Rural connectivity and power.** Weak 4G and unreliable grid power at farmland sites rule out a cloud-dependent design — this has to be offline-first with periodic sync, solar-powered.
- **Wildlife protection rules.** Macaque species in Nepal may fall under protections that limit how a deterrent can affect them. Regulatory review comes before hardware is finalized, not after.
- **False positives.** Misclassifying other animals or people as targets risks wasted deterrence or complaints — needs confidence thresholding and a human-review queue by design.
- **No local dataset.** There's no existing Nepal-context monkey behavior dataset to train against; scoping a data-collection pass is on the roadmap.

## Roadmap

- [ ] Survey existing systems — first pass in [`docs/research/01-landscape.md`](./docs/research/01-landscape.md)
- [ ] Detection + behavior classification approach
- [ ] System architecture
- [ ] Hardware spec
- [ ] Site requirements (rural vs. urban)
- [ ] Regulatory & welfare review
- [ ] Sprint 2: local dataset collection, prototype build

## Contributing / contact

This is an early-stage, solo-led project at Baliyo Technologies. If you're working on human-wildlife conflict, wildlife detection AI, or embedded deterrent hardware in Nepal or elsewhere and want to compare notes, open an issue or reach out.

## License

TBD.
