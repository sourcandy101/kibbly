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
