# Kibbly AI v2 scope

Decided by Zaineb Sassi on 9 November 2026 (step 1).

## Decisions

| Topic | Decision |
|---|---|
| Feature set | Reframed around three AI blocks: dog recognition, eating behavior analytics, adaptive portions. Generative features become a thin language layer on top. |
| Packages | Python virtual environment in `ai_v2/.venv` with a pinned `requirements.txt`. |
| Language model | Local (Ollama) and cloud (Claude or Gemini) behind one interface. The evaluation compares them; the demo uses the one that scores best. |
| Order | Shared data model first, then recognition. |

## Architecture layers

| Layer | Content | Kind |
|---|---|---|
| Perception | Presence, dog or person, which dog, unknown dog rejection | vision model |
| Engines | Nutrition, meal statistics, anomaly detection, dispensing rules | code |
| Language | Meal insights, grounded chat | LLM |
| Evaluation | One shared harness with test cases for every feature | code |

## Features

| Feature | Layer | Priority | Notes |
|---|---|---|---|
| Dog recognition | Perception | must have | Open set: identify known dogs, reject unknown dogs and people, enroll a new dog from a short video. Augmentation (crops, lighting, blur) for robustness. |
| Nutrition engine and feeding plan | Engines | must have | Energy based (resting energy times a life stage factor) divided by the kcal density of the owner's kibble. Replaces the flat grams per kg rule of `ai/`. |
| Eating behavior analytics | Engines | must have | From the load cell: grams served, grams eaten, leftovers, eating speed, deviation from the dog's own baseline. |
| Meal insights | Language | must have | One pipeline: statistics and anomalies in code, wording by the model. Output formats: meal report, explained alert, daily diary. |
| Adaptive portions | Engines | should have | Suggests a portion change when a dog keeps leaving food or its weight drifts. The owner confirms. |
| Ask Kibbly chat | Language | stretch goal | Answers only from the dog's own logs. No medical answers. |

## Dropped

| Idea | Reason |
|---|---|
| Synthetic training photos | Generated images cannot reproduce the face of a specific dog, so they do not help tell two dogs apart. Standard augmentation covers robustness. |

## Language model choice (9 November 2026)

Benchmark: one meal report task (facts for Mochi with a 28% drop and needs_vet true), 3 runs per model after warm up, on the team laptop (8 GB RAM, i5 8265U, CPU only). Five checks: exact numbers, vet sentence, no sex guess, no diagnosis words, short.

| Model | Time per answer | Score | Main failure |
|---|---|---|---|
| gemma3:1b | 4 s | 3/5 | Wrong facts ("95 grams remaining"), missed the drop and the vet sentence |
| qwen3.5:2b (thinking off) | 10 s | 2/5 | Invented "has not eaten in two days", guessed the sex |
| **gemma3:4b** | **12 s** | **4/5** | Guessed the sex only |

Decision:

1. **Local model: gemma3:4b.** The only local model that kept every fact right. 12 s is acceptable for reports, which are not real time.
2. **Cloud model: Claude Haiku**, to be compared against gemma3:4b in the meal insights evaluation (step 6). Needs an API key.
3. The sex guess is fixed with data, not prompting: the dog profile gets a `sex` field (step 2).
4. Field names must be unambiguous: `grams_left` was read as food left in the feeder. Use names such as `grams_left_in_bowl` (step 2).

## Recognition strategy (9 November 2026)

Decision: **appearance first, colored collar as a tiebreaker.**

| Situation | What decides |
|---|---|
| Appearance clearly matches one dog | Appearance alone |
| Appearance unsure between two dogs | The collar color |
| No collar visible and appearance unsure | Unknown: nothing served, check again a few seconds later |

Collar rules: wide flat band (2 to 3 cm) in a color never found in dog coats (bright blue, bright green, magenta). No red, orange, brown, black or white.

Why not collar only: Kibbly's promise is recognition by appearance; existing feeders already identify pets with tags or microchips. The ESP32-CAM color balance also shifts with light, and a collar can be hidden or removed.

Order: the collar step comes after the appearance pipeline is measured (step 4.8), because it needs real photos of dogs wearing collars and because the numbers will show whether it is needed beyond look alike pairs.

## Recognition decisions (step 4.1, 9 November 2026)

| Topic | Decision | Note |
|---|---|---|
| Test data | DogFaceNet now, friends' dogs videos, PetFace requested | DogFaceNet: 8,363 aligned face images of 1,393 dogs, CC BY 4.0 (credit the authors). PetFace: research use only, request form. Friends' dogs: see `data_collection_guide.md`. |
| Detector | YOLO (Ultralytics) | AGPL 3.0 license: fine for the course prototype. Before any commercial use, switch to a permissive detector (the detector sits behind an interface) or buy an Ultralytics license. |
| Image model | Compare DINOv2 small and CLIP, keep the best | Same evaluation for both |
| Error targets | At most 2% of unknown or wrong dogs accepted, at least 90% of correct dogs accepted at the first check | The threshold is chosen from data to meet the first number |

Data lives in `D:\kibbly_data`, never in the repo (size and privacy).
