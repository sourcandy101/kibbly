# Kibbly handover: app and connectivity (Moetaz)

Context for Moetaz El Ouaer and his Claude Code conversations. Last updated 9 November 2026. Read fully before starting.

## 1. Your role

**Moetaz El Ouaer, App and Connectivity Lead.** You own everything the owner sees and touches: the web app (PWA), Firebase (data, files, login, notifications) and the link between the feeder and the cloud. Your folder in the repo is `app/`.

## 2. The product in short

**Kibbly** is a smart dog feeder. At each meal time it calls each dog by name, recognizes the dog with a camera, serves that dog its own portion in small bursts, weighs what was eaten, and reports every meal in the app. Generative AI suggests portions and writes meal reports. It is the team's **BEAR** project (Business, Embedded, AI, Research). Prototype demo due **about 7 December 2026**.

## 3. Team and repository

| Member | Role | GitHub |
|---|---|---|
| Zaineb Sassi | AI and Data Lead (repo owner) | `sourcandy101` |
| Youssef Bousnina | Embedded and Hardware Lead | `bousninayoussef2005-netizen` |
| Hedi Ennaifer | Hardware and Electrical Lead | `HediE-source` |
| **Moetaz El Ouaer** | **App and Connectivity Lead** | `MoetazEO` |

**Repository (private):** https://github.com/sourcandy101/kibbly. Accept the invitation at https://github.com/sourcandy101/kibbly/invitations first.

Getting started:

1. `git clone https://github.com/sourcandy101/kibbly.git`
2. Before each work session: `git pull`
3. Work mainly in `app/` to avoid conflicts.
4. After each task: `git add .`, `git commit -m "What changed"`, `git push`

Team writing rules for the repo: English only; no dashes of any kind in comments, docs or commit messages (use numbered lists or tables); snake_case filenames. Read `docs/SPEC.md` for the full prototype specification.

## 4. Architecture and where you fit

| Part | Does | Owner |
|---|---|---|
| NUCLEO-F439ZI (STM32) | schedule, motor, scale, sensors, speaker, SD card, button | Youssef with Hedi |
| ESP32-CAM | camera and WiFi for the feeder; talks to the AI server and Firebase | Youssef with Moetaz |
| AI server (Python) | dog recognition, feeding plan, meal reports | Zaineb |
| **Firebase** | accounts, profiles, schedules, meal logs, voice clips, push notifications | **Moetaz** |
| **Web app (PWA)** | everything the owner does | **Moetaz** |

## 5. What the app must do

### Setup (once per home)

1. **Account** and login (Firebase Authentication).
2. **WiFi pairing** of the feeder: the owner presses the feeder button twice, then connects it from the app.
3. **Dog profiles:** name, breed, age in months, weight in kg, activity (low, medium, high), optional notes, **a few photos and a short video** (uploaded to Firebase Storage; the AI server uses them for recognition).
4. **Feeding plan:** the app sends the profile to the AI feeding plan generator and shows the suggestion; the owner confirms or edits it.
5. **Schedule:** up to **4 meals per day per dog**, each with a time and grams (multiples of 5).
6. **Calling order:** the owner sets which dog is called first.
7. **Voice recording:** the owner records each dog's call ("Biscuit!"); the clip goes to Firebase Storage (master copy) and is synced to the feeder's SD card.

### Daily use

1. **Meal diary per dog:** time, grams served, grams eaten, recognized or not.
2. **Notifications** (Firebase Cloud Messaging):

| Event | Example message |
|---|---|
| Meal done | "Dinner done: Biscuit 280 g" |
| Skipped meal | "Biscuit skipped dinner" |
| Unknown dog | "An unknown dog ate 20 g" with the photo |
| Wrong dog tried to eat | "Mochi tried to eat Biscuit's dinner" |
| Jam | "Kibbly is jammed" |
| Low or empty tank | "Food is running low" |
| Offline | "Kibbly is offline" |
| Power cut | "Kibbly restarted after a power cut; 1 meal was missed" |

3. **Feeding level and tank level** shown on the home screen.
4. **Generative AI screens:** smart meal reports (must have); Ask Kibbly chat (stretch goal).

## 6. Data model (proposed by Zaineb on 9 November 2026, please review)

The data model now lives in [`schemas/`](../schemas/README.md): one JSON Schema file per Firestore collection, valid and invalid example documents, and a checker script. Use these field names exactly (snake_case) so data passes between the app, the feeder and the AI server without conversion.

Main changes from the first proposal:

1. Dog profile: `birth_month` instead of an age, plus `sex`, `neutered` and `body_condition` (thin, ideal or overweight, chosen from pictures).
2. Home: the kibble's `kcal_per_kg` from the food bag (may be empty) and the home `timezone`.
3. New `weights` collection: the owner enters each weigh in; the app copies the latest into the dog profile.
4. Meals hold a list of visits (which dog came, confidence, what the feeder did, grams eaten).
5. New `daily_summaries` collection written by the AI server; the reports screen reads it.
6. All timestamps in UTC; schedules in local clock time.

Section "Open questions for the team" in `schemas/README.md` has one question for you (flat collections or subcollections).

## 7. Contract with the AI (already built by Zaineb)

The feeding plan generator lives in `ai/plan_generator.py`.

**Input** (profile): `name`, `breed`, `age_months`, `weight_kg`, `activity` (low, medium or high), `meals_per_day` (1 to 4), optional `notes`.

**Output when a field is missing:** `{"status": "missing_data", "missing": ["weight_kg"]}`. Show the owner which field to fill.

**Output when it works:**

```json
{"status": "ok", "dog_name": "Biscuit", "daily_total_grams": 560,
 "meals": [{"label": "Breakfast", "grams": 280}, {"label": "Dinner", "grams": 280}],
 "notes": "Biscuit gets 560 g of kibble a day in two meals.", "vet_advice": false}
```

When `vet_advice` is true, show the notes prominently (they end with "Please check this plan with your vet."). The owner must confirm before the plan becomes the schedule.

Today it runs as a Python function on a laptop with a local model (Ollama). **To agree with Zaineb:** the HTTP endpoint the app will call (for example `POST /plan`) and where the AI server runs (laptop for the demo, Google Cloud Run later).

## 8. Contract with the feeder (agree with Youssef)

The feeder reaches the internet through the ESP32-CAM over WiFi. Decide together:

1. How the feeder reads its schedule and voice clips from Firebase (sync on change, and a copy kept on the SD card for offline use).
2. How the feeder writes meal logs and alerts to Firebase (and syncs logs saved while offline).
3. How WiFi pairing works (for example the ESP32 opens a temporary access point and the app sends the home WiFi name and password).

## 9. Decisions already made

1. Web app as a **PWA** (works from any phone browser and can be installed).
2. **Firebase** for data, files, login and notifications.
3. Dogs only for now (cats later), dry kibble only.
4. AI features go through Zaineb's AI server; the app never calls an LLM directly.

## 10. Your plan to the demo

| Week | Task |
|---|---|
| 1 (2 to 8 Nov) | Firebase project, app skeleton |
| **2 (9 to 15 Nov)** | **Dog profiles and schedule screens** |
| 3 (16 to 22 Nov) | Voice recording and upload, meal diary |
| 4 (23 to 29 Nov) | Notifications, feeder sync with Youssef |
| 5 (30 Nov to 6 Dec) | AI screens (feeding plan, meal reports), polish for the demo |

Until the feeder works, use fake meal data in Firebase to build and test every screen.
