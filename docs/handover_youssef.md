# Kibbly handover: embedded and hardware (Youssef)

Context for Youssef Bousnina and his Claude Code conversations. Last updated 9 November 2026. Read fully before starting.

## 1. Your role

**Youssef Bousnina, Embedded and Hardware Lead.** You own the feeder itself: the STM32 firmware, the dispensing mechanism, the sensors, the enclosure and the PCB, working with Hedi Ennaifer on the electrical side. Your folders in the repo are `firmware/` and `hardware/`.

## 2. The product in short

**Kibbly** is a smart dog feeder. At each meal time it calls each dog by name, recognizes the dog with a camera, serves that dog its own portion in small bursts, weighs what was eaten, and reports every meal in the app. It is the team's **BEAR** project (Business, Embedded, AI, Research); the hardware is also the team's **Embedded Systems** course project. Prototype demo due **about 7 December 2026**. The prototype must **feed, chime and recognize the dog**.

## 3. Team and repository

| Member | Role | GitHub |
|---|---|---|
| Zaineb Sassi | AI and Data Lead (repo owner) | `sourcandy101` |
| **Youssef Bousnina** | **Embedded and Hardware Lead** | `bousninayoussef2005-netizen` |
| Hedi Ennaifer | Hardware and Electrical Lead | `HediE-source` |
| Moetaz El Ouaer | App and Connectivity Lead | `MoetazEO` |

**Repository (private):** https://github.com/sourcandy101/kibbly (you already have write access).

Getting started:

1. `git clone https://github.com/sourcandy101/kibbly.git`
2. Before each work session: `git pull`
3. Work mainly in `firmware/` and `hardware/`.
4. After each task: `git add .`, `git commit -m "What changed"`, `git push`
5. `.gitignore` already excludes STM32CubeIDE build output (Debug, Release, .elf, .bin, .hex) and KiCad backups.

Team writing rules for the repo: English only; no dashes of any kind in comments, docs or commit messages (use numbered lists or tables); snake_case filenames. Read `docs/SPEC.md` for the full prototype specification.

## 4. Architecture and where you fit

| Part | Does | Owner |
|---|---|---|
| **NUCLEO-F439ZI** (STM32F439ZI, Cortex M4, 180 MHz) | real time control: meal schedule and clock, dispenser motor, bowl scale, tank level, ultrasonic presence, speaker, SD card, button and LED, failure handling. **Must keep working offline.** Too weak for vision. | **Youssef** with Hedi |
| **ESP32-CAM** | camera and WiFi for the whole feeder; sends photos to the AI server; reads and writes Firebase; forwards commands to the STM32 | **Youssef** with Moetaz |
| AI server (Python) | dog recognition (photo in, "Biscuit, 94%" out), feeding plans | Zaineb |
| Firebase and web app | profiles, schedules, logs, notifications | Moetaz |

## 5. Hardware list

| Part | Decision |
|---|---|
| Main board | NUCLEO-F439ZI |
| Camera and WiFi | ESP32-CAM, linked to the STM32 over **UART** (proposed) |
| Dispenser | **Open:** paddle wheel with servo, or auger with stepper motor. Recommendation: auger with a NEMA 17 stepper and a TMC2209 driver (precise 5 g bursts, quiet, jam detection with the scale); paddle wheel as fallback. |
| Bowl scale | Load cell with HX711 amplifier |
| Presence sensor | Ultrasonic (HC-SR04 type): when an animal comes close, it starts the recognition cycle |
| Tank level | **Open.** Recommendation: VL53L0X or VL53L1X time of flight sensor in the lid (I2C), plus a software estimate from grams dispensed since the last refill |
| Sound | Speaker with a small amplifier; clips played from the SD card (owner voice "Biscuit!" or a chime) |
| Storage | SD card: voice clips, schedule copy, offline meal logs |
| Power | 12 V wall adapter (plan regulators for 5 V and 3.3 V; the ESP32-CAM needs a stable 5 V supply with current peaks during WiFi) |
| Tank | 1 kg for the prototype (commercial products later 1 kg to 4 kg) |
| Food | dry kibble only |

Peripheral ideas for the F439ZI (to confirm against the board pinout): timer PWM or step and direction pins for the motor; timer input capture for the ultrasonic echo; GPIO for the HX711; I2C for the time of flight sensor; SDIO or SPI for the SD card; DAC with an amplifier for audio; UART for the ESP32-CAM; RTC with backup for the meal clock; external interrupt for the button.

## 6. Button and LED (decided)

| Action | Result |
|---|---|
| Long press | Shut down |
| 2 presses | WiFi pairing mode |
| 5 presses | Reset |
| LED | WiFi status (proposed: solid when connected, blinking when pairing, off when offline) |

## 7. Firmware behavior: one meal

1. **Meal time** (from the RTC and the stored schedule): play the call of the first dog in the owner's order.
2. **Presence:** the ultrasonic sensor detects an animal; tell the ESP32-CAM to take a photo.
3. **Recognition:** the ESP32-CAM sends the photo to the AI server and returns the dog id and confidence to the STM32.
4. **Decide:**
   1. called dog recognized (proposed: confidence 80% or more): go to step 5
   2. another known dog: do not dispense
   3. unknown dog: small portion (proposed: at most 20 g, twice a day) and an alert with the photo
   4. no animal or a person: nothing
5. **Serve in bursts:** about 5 g per burst, only while the recognized dog stays in front of the camera; stop when the portion is complete or the dog leaves.
6. **Weigh:** the load cell gives grams served and grams eaten.
7. **Next dog:** call the next dog and repeat from step 2.
8. **Log:** send the meal (dog, time, grams served, grams eaten, recognized, confidence) through the ESP32-CAM to Firebase.

If a called dog does not come: call again, then alert the owner (proposed: calls at 0, 5 and 10 minutes, alert at 15 minutes).

## 8. Failure handling (decided)

| Failure | Behavior |
|---|---|
| Jam | Motor turns but the scale gains no weight: retry, then alert "Kibbly is jammed" |
| Low or empty tank | Low: refill alert. Empty: no meal and an urgent alert |
| WiFi or AI server down | Keep the schedule; serve meals in the owner's order without recognition; save logs on the SD card and sync later |
| Power cut | Keep the schedule in flash or on the SD card; detect missed meals after restart and alert the owner |

## 9. Interfaces to agree

1. **With Zaineb (AI):** the message the ESP32-CAM sends to the AI server (a JPEG photo over HTTP) and the answer (dog id, confidence). Also the speed: the decision should arrive in about 1 second.
2. **STM32 and ESP32-CAM UART protocol** (proposed messages to define together): presence detected, take photo, recognized dog and confidence, dispense N bursts, grams measured, meal done, alert type, WiFi status, schedule update.
3. **With Moetaz (app and Firebase):** how the feeder gets its schedule and voice clips, writes meal logs and alerts, and pairs with WiFi.

## 10. Your plan to the demo

| Week | Task |
|---|---|
| 1 (2 to 8 Nov) | Choose the dispenser, sketch the body, order parts with Hedi |
| **2 (9 to 15 Nov)** | **Dispenser mechanism; motor and scale working on the STM32** |
| 3 (16 to 22 Nov) | Tank and bowl; ultrasonic, tank sensor, speaker, SD card |
| 4 (23 to 29 Nov) | First full assembly; STM32 and ESP32-CAM link |
| 5 (30 Nov to 6 Dec) | Failure handling, fixes, PCB draft, demo rehearsal |

First milestone to aim for: **the STM32 dispenses exactly N bursts on command and the scale reads the grams.** Everything else builds on that.
