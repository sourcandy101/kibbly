# Kibbly prototype specification

Version 1 (2 November 2026). Demo due **~7 December 2026**.

Items marked **[proposed]** are suggestions added during planning; confirm or change them as a team. Everything else was decided by the team.

---

## 1. What the prototype must show

A working feeder that **feeds, chimes and recognizes the dog**, plus generative AI features in the app.

**Animals:** dogs only for now. Cats come in a later version (recognition, portions and food differ).

**Food:** dry kibble only. Prototype tank: **1 kg**. Commercial versions: several models from 1 kg to 4 kg.

## 2. Phases

### Phase 1: Setup (once per home)

1. Owner plugs in Kibbly (12 V wall adapter).
2. Owner presses the button **twice** → Kibbly enters Wi-Fi pairing; the LED shows the state (see §6). The owner connects it from the web app.
3. Owner creates a profile for each dog in the web app: name, breed, age, weight, activity level.
4. Owner adds **a few photos and a short video** of each dog. The server extracts face images from the video and builds the dog's recognition profile.
5. **Feeding plan generator** (generative AI) suggests portions and meal times from the profile; the owner confirms or edits them.
   - Up to **4 meals per day, per dog**, each with its own time and grams.
   - The owner sets the **calling order** (e.g. the shy dog first).
6. Owner records each dog's call ("Biscuit!") in the app. The clip is stored in **Firebase** (master copy) and synced to the feeder's **SD card** so it plays offline.

### Phase 2: A meal (repeats for every scheduled meal)

1. **Call.** At the meal time, Kibbly calls the first dog in the owner's order (recorded call or chime).
2. **Presence.** The **ultrasonic sensor** detects an animal in front of the bowl and wakes the camera.
3. **Recognition.** The ESP32-CAM takes a photo and sends it to the recognition server, which answers e.g. "Biscuit, 94%".
   - **[proposed]** Dispense only if confidence ≥ 80%; below that, treat as unknown.
4. **Serve in small bursts.** If it is the called dog, the STM32 dispenses in small bursts while that dog stays in front of the camera.
   - **[proposed]** About 5 g per burst; re-check the dog every few seconds; stop when the dog leaves or the portion is complete.
5. **Weigh.** The bowl scale measures grams dispensed and grams eaten, so the app knows exactly who ate what.
6. **Next dog.** When the first dog is done, Kibbly calls the next dog in the order and repeats steps 2–5.
7. **Log.** Each meal is saved in Firebase (dog, time, grams served, grams eaten).

**Special cases**

| Situation | What Kibbly does |
|---|---|
| Called dog doesn't come | Calls again, then notifies the owner. **[proposed]** Calls at T, T+5 min and T+10 min, then sends "Biscuit skipped dinner" at T+15 min. |
| Wrong dog at the bowl during another dog's meal | Stops dispensing (no bursts for the wrong dog); the scale records any food taken. |
| Unknown dog | Dispenses a small portion and notifies the owner, with a photo. **[proposed]** At most 20 g, at most twice a day. |
| A person or no animal | Nothing is dispensed. |

### Phase 3: Reports and insights (in the app)

- Meal diary per dog.
- **Smart meal reports** (generative AI): daily/weekly summaries in plain language.
- **Explained alerts** (generative AI): alerts with a likely explanation and a next step.
- **Ask Kibbly** (generative AI): chat with questions answered from the dog's real data.

## 3. Failure handling

| Failure | Behavior |
|---|---|
| **Jam** | Motor turns but the scale gains no weight → retry, then alert "Kibbly is jammed". |
| **Low / empty tank** | Tank level below threshold → refill alert. Empty → no meal + urgent alert. |
| **Wi-Fi or server down** | Keeps the schedule. Without recognition, serves meals in the owner's order and logs that recognition was unavailable; syncs logs when back online. |
| **Power cut** | Remembers the schedule (stored in flash/SD) and missed meals; tells the owner when power returns. |

## 4. Architecture

```
            ┌──────────────── Web app (PWA) ────────────────┐
            │ profiles · schedule · meal diary · AI chat     │
            └───────────────▲───────────────────────────────┘
                            │
                     ┌──────┴──────┐          ┌──────────────────────┐
                     │  Firebase   │◄────────►│ AI server (Python)   │
                     │ DB · files  │          │ recognition + Gen AI │
                     │ push notif. │          └──────────▲───────────┘
                     └──────▲──────┘                     │ photo → "Biscuit 94%"
                            │ Wi-Fi                      │
                   ┌────────┴─────────┐                  │
                   │    ESP32-CAM     │──────────────────┘
                   │ camera + Wi-Fi   │
                   └────────▲─────────┘
                            │ UART [proposed]
                   ┌────────┴─────────┐
                   │ NUCLEO-F439ZI    │  real-time control
                   │ (STM32F439ZI)    │
                   └──┬───┬───┬───┬───┘
                motor │   │   │   │ speaker, SD card, button, LED
         load cell ───┘   │   └── ultrasonic sensor
                    tank level sensor
```

### Responsibilities

| Part | Does |
|---|---|
| **NUCLEO-F439ZI** (STM32F439ZI, Cortex-M4) | Meal schedule and clock, dispensing motor, bowl scale, tank level, ultrasonic presence, speaker playback, SD card, button and LED, failure handling. Works even when offline. |
| **ESP32-CAM** | Wi-Fi for the whole feeder, takes photos, talks to the AI server and Firebase, forwards commands to the STM32. |
| **AI server** (Python) | Dog recognition; generative AI features; synthetic training photos. Runs on a laptop for the demo, cloud later. |
| **Firebase** | Accounts, dog profiles, schedules, meal logs, voice clips, push notifications. |
| **Web app (PWA)** | Everything the owner sees and does. |

### Hardware choices

| Item | Choice |
|---|---|
| Main board | **NUCLEO-F439ZI** |
| Camera + Wi-Fi | **ESP32-CAM** |
| Dispenser | **To choose:** paddle wheel + servo, or auger + stepper motor |
| Bowl scale | Load cell + HX711 amplifier |
| Presence | Ultrasonic sensor (e.g. HC-SR04) |
| Tank level | **To choose** [proposed: ultrasonic or time-of-flight sensor at the top of the tank] |
| Sound | Speaker + small amplifier, clips stored on SD card [proposed: STM32 DAC output] |
| Power | 12 V wall adapter |

### Button and LED

| Action | Result |
|---|---|
| Long press | Shut down |
| 2 presses | Connect to Wi-Fi (pairing mode) |
| 5 presses | Reset |
| LED | Shows whether Kibbly is connected to Wi-Fi [proposed: solid = connected, blinking = pairing, off = not connected] |

## 5. Generative AI

The team wants **all of these**. Prototype priority keeps the demo safe:

| Feature | What it does | Prototype |
|---|---|---|
| **Feeding plan generator** | Suggests portions and meal times from breed, age, weight, activity; owner confirms. | **Must have** |
| **Smart meal reports** | Turns meal logs into daily/weekly summaries in plain language. | **Must have** |
| **Ask Kibbly (chat)** | Answers owner questions from the dog's real data. | Stretch goal |
| **Synthetic training photos** | Generates extra photos of each dog to improve recognition from few examples. | Stretch goal |
| **Explained alerts** | Adds a likely explanation and next step to each alert. | Version 2 |
| **Dog's daily diary** | Fun, shareable post written "by the dog". | Version 2 |

- **Provider:** to decide later. All features go through one interface on the AI server so the provider can be swapped.
- **[proposed] Safety rules for every prompt:** never give a medical diagnosis; recommend a vet for health concerns; never invent data that isn't in the logs.
- **Course link:** prompt design and evaluation for these features is the Prompt Engineering course deliverable.

## 6. Data

**[proposed, 9 November 2026]** The data model is defined as JSON Schema files in [`schemas/`](../schemas/README.md), with examples and a checker. Objects: `homes`, `dogs`, `weights`, `schedules`, `meals` (with the visits of each meal slot), `visits` (outside meal times), `daily_summaries` (computed by the AI server) and `alerts`. The schemas are the source of truth; this section only points to them.

**Dataset:** the team has no dogs yet. Use public dog datasets plus friends' dogs; collect real data in the pilot.

## 7. Team and timeline

| Week | Youssef (design & PCB) | Hedi (hardware) | Zaineb (AI & data) | Moetaz (app & connectivity) |
|---|---|---|---|---|
| 1 (2–8 Nov) | Choose dispenser, sketch body | Parts list, order parts | Collect dataset, set up AI server | Firebase project, app skeleton |
| 2 (9–15 Nov) | Build dispenser mechanism | Motor + scale working | Recognition prototype on laptop | Profiles + schedule screens |
| 3 (16–22 Nov) | 1 kg tank + bowl | Ultrasonic, tank sensor, speaker, SD | Feeding plan generator | Voice recording, meal diary |
| 4 (23–29 Nov) | First full assembly | STM32 ↔ ESP32-CAM link | Recognition server live | Notifications |
| 5 (30 Nov–6 Dec) | Fixes, PCB draft | Failure handling | Meal reports (+ stretch goals) | AI features in the app |
| Demo (~7 Dec) | Rehearsal + backup video | | | |

## 8. Open questions

1. Dispenser: paddle wheel + servo, or auger + stepper?
2. Tank level sensor type.
3. Generative AI provider.
4. Where the AI server runs after the demo (cloud host).
5. Confirm the [proposed] values: confidence threshold, burst size, call retries, unknown-dog portion, LED states.
