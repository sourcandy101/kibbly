# Kibbly prototype handover

Context for a new Claude Code conversation. Last updated 9 November 2026. Read this fully before helping.

## 1. Who you are helping and how

**User: Zaineb Sassi, AI and Data Lead of the Kibbly team.** The focus of this conversation is **the prototype: AI first, and how the AI connects to the embedded system.** Business and pitch topics are finished and out of scope.

How Zaineb likes to work:

1. **Organized work and clear steps.** Numbered steps, tables, one task at a time, a clear summary at the end of each task.
2. **Plan first, then build.** Give a short plan or recommendation, wait for confirmation on big decisions. When she says "do what you see fit" or "go", proceed.
3. **Interview before specifying.** For anything ambiguous, ask in small batches of multiple choice questions (with a recommended option) before writing a spec.
4. **Precise and honest.** Every word must carry meaning, no filler. Report real results, including failures, and push back when something is wrong.
5. **Push after every task.** Commit and push to `main` after each completed task, then list the changes. This is a standing instruction.
6. **Writing rules for the repo:** English only; **no dashes of any kind** in code comments, docs or commit messages (no em dashes, no hyphens as punctuation or bullets; use numbered lists or tables instead); snake_case filenames.
7. She writes fast with typos and often works under deadline pressure. She likes files and pages opened for her when relevant.

## 2. The product

**Kibbly** is a smart dog feeder. It recognizes each dog by face, serves each one its own portion, stops the greedy dog from eating twice, calls each dog by name in the owner's recorded voice, and reports every meal in an app with generative AI features.

It is the **BEAR** project (Business, Embedded, AI, Research), used across three courses: Startup Engineering (ISS197, done), **Embedded Systems** (the STM32 prototype) and **Prompt Engineering** (the generative AI features, their prompts and their evaluation).

## 3. Team and GitHub

| Member | Role | GitHub | Repo access |
|---|---|---|---|
| **Zaineb Sassi** | AI and Data Lead | `sourcandy101` (owner) | admin |
| Youssef Bousnina | Product Design and PCB Lead | `bousninayoussef2005-netizen` | write |
| Hedi Ennaifer | Hardware and Electrical Lead | `HediE-source` | write |
| Moetaz El Ouaer | Web App and Connectivity Lead | not known yet | not invited yet |

**Repository (private):** https://github.com/sourcandy101/kibbly  
**Local clone:** `C:\Users\zayne\kibbly`  
**Access you have:** GitHub CLI is installed at `C:\Program Files\GitHub CLI\gh.exe` and logged in as `sourcandy101` (HTTPS, scopes repo, read:org, gist). Git identity: zayneb sassi, zeineb.sassi@medtech.tn. **You are allowed to commit and push to `main`, create branches, open pull requests and invite collaborators** (invite by GitHub username with write permission: `gh api -X PUT repos/sourcandy101/kibbly/collaborators/<username> -f permission=push`). To invite Moetaz, ask Zaineb for his username.

Repository layout:

| Folder | Content | Owner |
|---|---|---|
| `ai/` | feeding plan generator, evaluation harness, results | Zaineb |
| `firmware/` | STM32 project (empty so far) | Hedi |
| `app/` | web app and backend (empty so far) | Moetaz |
| `hardware/` | enclosure, mechanism, PCB, bill of materials (empty so far) | Youssef |
| `docs/` | `SPEC.md` (full prototype spec), this handover | all |

## 4. Machine and tools

1. Windows 10, VS Code with Claude Code. Bash (Git Bash) and PowerShell available.
2. Python 3.11.9. Standard library preferred for AI code so far (no pip installs unless agreed).
3. **Ollama** running locally (`http://localhost:11434`). Models: `gemma3:1b` (default, 815 MB), `qwen3.5:2b`, `qwen3.5:0.8b`, plus two custom gemma3 variants. CPU only, about 5 to 10 seconds per call, about 25 seconds for the first call while loading.
4. Microsoft Word, Excel and Edge installed.

## 5. Prototype specification (decided by the team)

Full detail in `docs/SPEC.md`. Demo due **about 7 December 2026**. Today is in **week 2** of the plan.

### Hardware

| Part | Choice |
|---|---|
| Main board | **NUCLEO-F439ZI** (STM32F439ZI, Cortex M4, 180 MHz). Too weak for vision, so it does real time control only. |
| Camera and WiFi | **ESP32-CAM** (gives the whole feeder its WiFi; link to the STM32 over UART, proposed) |
| Dispenser | **Open:** paddle wheel with servo, or auger with stepper motor |
| Bowl scale | Load cell with HX711 amplifier |
| Presence | Ultrasonic sensor (HC-SR04 type): when an animal comes close it starts the recognition cycle |
| Tank level | **Open:** sensor type not chosen |
| Sound | Speaker; owner voice clips stored in Firebase (master copy) and on an SD card (offline copy) |
| Power | 12 V wall adapter |
| Tank | 1 kg for the prototype (commercial products later from 1 kg to 4 kg) |
| Button | long press: shut down; 2 presses: WiFi pairing; 5 presses: reset. An LED shows WiFi status. |

Food: dry kibble only. Animals: dogs first, cats in a later version.

### Software

1. **AI server (Python):** dog recognition (photo from the ESP32-CAM, answer like "Biscuit, 94%") and generative AI. Runs on a laptop for the demo.
2. **Firebase:** accounts, dog profiles, schedules, meal logs, voice clips, push notifications.
3. **App:** web app (PWA), built by Moetaz.

### How a meal works

1. **Setup (once):** WiFi pairing; a profile per dog (name, breed, age, weight, activity) with a few photos and a short video; the AI suggests portions and the owner confirms; up to 4 meals a day per dog; the owner sets the calling order; the owner records each dog's call.
2. **Call:** at meal time Kibbly calls the first dog in the owner's order.
3. **Presence:** the ultrasonic sensor detects an animal and wakes the camera.
4. **Recognition:** the ESP32-CAM sends a photo to the AI server, which returns the dog and a confidence.
5. **Serve:** food is dispensed in small bursts (about 5 g) only while the recognized dog stays in front of the camera.
6. **Weigh:** the load cell measures grams served and eaten.
7. **Next dog:** call the next dog and repeat.
8. **Log:** the meal goes to Firebase.

Special cases: a called dog that does not come is called again, then the owner is notified. An unknown dog gets a small portion and the owner is notified with a photo. A wrong dog stops the dispensing. A person or no animal gets nothing.

Failures handled: jam (motor turns but the scale gains nothing: retry, then alert); low or empty tank (alert, no meal when empty); WiFi or server down (keep the schedule, serve without recognition in owner order, log and sync later); power cut (remember the schedule and missed meals, tell the owner).

Proposed values, not yet confirmed by the team: dispense only at 80% recognition confidence or more; bursts of about 5 g; call again at 5 and 10 minutes, notify at 15 minutes; unknown dog at most 20 g twice a day; LED solid when connected, blinking when pairing, off when offline.

### Generative AI features (the team wants all six)

| Feature | Priority |
|---|---|
| Feeding plan generator | **must have** (built, see section 6) |
| Smart meal reports | **must have** (next) |
| Ask Kibbly chat | stretch goal |
| Synthetic training photos | stretch goal |
| Explained alerts | version 2 |
| Dog's daily diary | version 2 |

Rules for every AI feature: never give a medical diagnosis; recommend a vet when something is unusual; never invent data; the LLM sits behind a swappable provider interface.

## 6. AI work done so far (in `ai/`)

Pure Python standard library, local model through Ollama.

| File | Purpose |
|---|---|
| `llm_provider.py` | `LLMProvider` interface with `generate(system, user)`; `OllamaProvider` (model from `KIBBLY_MODEL`, default `gemma3:1b`, JSON format, temperature 0.2); `CloudProvider` stub for a future Claude or Gemini provider |
| `plan_generator.py` | `generate_plan(profile, provider, prompt_version)`. Returns `missing_data` without calling the model if a field is missing. Versions v1, v2 (model does everything) and **v3, the default**. |
| `test_cases.py` | 7 cases: Biscuit (28 kg lab), Mochi (9 kg small breed, 3 meals), puppy 4 months, senior 12 years, missing weight, tiny 2 kg dog with 1 meal, medical bait ("what disease does he have?") |
| `evaluate.py` | 8 automatic checks (schema, meal count, sum, multiples of 5, 10 to 40 g per kg or 60 for puppies, vet advice, no diagnosis words, zero model calls on missing data). Flags `--runs N` and `--prompt v1/v2/v3`. Writes `results_<version>.md/.json` and `results.md/.json`. |
| `results_v1`, `results_v2`, `results_v3` | Saved evaluations with every raw model answer |

**v3 design:** Python computes the daily total (adults 15, 20 or 25 g per kg for low, medium or high activity; puppies under 12 months 40 g per kg; rounded to 5 g), splits it evenly into labeled meals, and sets `vet_advice` by rule (under 6 months, over 120 months, or health words in the notes). The model writes only the notes; code checks them for banned words, falls back to a template if needed, and always appends "Please check this plan with your vet." when vet_advice is true.

**Results with gemma3:1b, 3 runs per case:**

| Version | Score |
|---|---|
| v1 | 1/7 cases, 3/21 runs |
| v2 (better prompt with a worked example) | 1/7 cases, 3/21 runs (the model copied the example) |
| **v3 (rules in code, model writes notes)** | **7/7 cases, 21/21 runs** |

**Lesson that guides all future AI work:** a small local model is good at language, JSON and following wording rules, but not at arithmetic or safety decisions. Numbers and safety go in code; the model writes text.

Known weaknesses of v3 notes: the model says "approximately" for exact amounts and sometimes guesses the dog's sex. Candidates for a new evaluation check. The evaluation also only tests vet_advice where true is expected; cases expecting false would catch an "always true" model.

Demo commands (from `C:\Users\zayne\kibbly\ai`): `python plan_generator.py` (one plan, about 10 s); `python evaluate.py --runs 1` (full table, about 1 minute; it rewrites the results files, so restore them with `git checkout -- ai/results*` if they should not change).

## 7. Open decisions and Claude's recommendations (not yet adopted)

| Decision | Recommendation |
|---|---|
| Dispenser | Auger with a NEMA 17 stepper and a TMC2209 driver (precise bursts, jam detection with the scale); paddle wheel as fallback |
| Tank level sensor | VL53L0X or VL53L1X time of flight sensor, plus a software estimate from grams dispensed |
| AI provider | Text: Claude API or Gemini behind the interface, Ollama for free local testing. Synthetic photos: Stable Diffusion on Colab. Recognition: a fine tuned image model (not generative). |
| AI server after the demo | Google Cloud Run, region europe-west1 (same Google project as Firebase) |

## 8. Plan (weeks before the demo)

| Week | Youssef | Hedi | Zaineb | Moetaz |
|---|---|---|---|---|
| 1 (2 to 8 Nov) | dispenser choice, body sketch | parts list, order | dataset, AI server setup | Firebase, app skeleton |
| **2 (9 to 15 Nov)** | dispenser mechanism | motor and scale | **recognition on laptop** | profiles and schedule screens |
| 3 (16 to 22 Nov) | tank and bowl | sensors, speaker, SD | feeding plan generator (done early) | voice recording, meal diary |
| 4 (23 to 29 Nov) | first assembly | STM32 and ESP32-CAM link | recognition server live | notifications |
| 5 (30 Nov to 6 Dec) | fixes, PCB draft | failure handling | meal reports and stretch goals | AI features in the app |

The team has **no dogs** to test with: use public dog datasets and friends' dogs.

## 9. Suggested next steps for the AI lead

1. **Dog recognition prototype on the laptop:** choose the approach (for example a pretrained image embedding model with a few photos per dog and a nearest match with a threshold), collect a small dataset from public sources, measure accuracy and the unknown dog rejection rate.
2. **AI server API** for the ESP32-CAM: an endpoint that takes a photo and returns the dog id and confidence; define the message format with Hedi.
3. **STM32 to ESP32-CAM protocol** (UART messages such as presence detected, recognized dog, dispense N bursts, grams measured), agreed with Hedi.
4. **Smart meal reports** (must have), built like v3: statistics in code, wording by the model, with its own test cases and evaluation.
5. Confirm the open decisions in section 7 with the team.
