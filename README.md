# Kibbly

**Knows every dog. Feeds every dog.**

Kibbly is a smart dog feeder that recognizes each dog, serves each one its own portion, blocks "seconds" for the greedy one, calls each dog by name in the owner's voice, and reports every meal in an app.

It is our **BEAR** project (Business · Embedded · AI · Research), built across three courses: Startup Engineering (ISS197), Embedded Systems and Prompt Engineering.

## Team

| Member | Role | Owns |
|---|---|---|
| Youssef Bousnina | Embedded & Hardware Lead | `firmware/` and `hardware/` (STM32, mechanism, enclosure, PCB) |
| Hedi Ennaifer | Hardware & Electrical Lead | `firmware/` drivers, wiring, power |
| Zaineb Sassi | AI & Data Lead | `ai/` (dataset, models, generative features) |
| Moetaz El Ouaer | Web App & Connectivity Lead | `app/` and device-to-cloud link |

## Prototype goal (6 weeks)

A working demo that **feeds, chimes and recognizes your dog**:

- [ ] Recognizes 2 known dogs (and rejects an unknown one)
- [ ] Dispenses the right portion for the recognized dog and refuses seconds
- [ ] Plays a chime or a recorded name at mealtime
- [ ] Sends a "Biscuit ate 60 g" notification to the app

Out of scope for the prototype: water level, live talk, video history, final enclosure.

## Architecture

Full details in **[docs/SPEC.md](docs/SPEC.md)**.

- **Main board:** NUCLEO-F439ZI (STM32F439ZI): schedule, motor, scale, sensors, speaker, SD card, button.
- **Camera + Wi-Fi:** ESP32-CAM camera board, programs loaded through an ESP32 DevKit V1 (see [hardware/01_hardware_list.md](hardware/01_hardware_list.md)).
- **AI server (Python):** dog recognition + generative AI.
- **Data:** Firebase. **App:** web app (PWA).
- **Sensors:** bowl load cell, food tank level, ultrasonic presence sensor.

## Hardware

**How the feeder works.** At meal time the STM32 plays the dog's call from the SD card. When the ultrasonic sensor sees an animal, the ESP32 camera board takes a photo and asks the AI server which dog it is. If it is the called dog, the STM32 turns the auger in bursts of about 5 g while the dog stays, and the scale under the bowl measures what was served and eaten. Without internet the feeder still follows the schedule saved on the SD card and uploads its logs later.

**The database links hardware and software.** The feeder never talks to the app directly. Through the ESP32 it reads the schedules, dog names and voice clips from Firebase, and writes meals, alerts and its WiFi status back. The app reads and writes the same data.

**Must do now (hardware).** Youssef and Hedi gather every physical part the team has and write the exact list of components. The parts list and the system architecture are then updated to match the real parts, and only after that does coding of the boards start. Details in [hardware/README.md](hardware/README.md#must-do-now-real-hardware-inventory).

**Progress.** Youssef and Hedi build the hardware in 7 steps. Technical details are in [hardware/](hardware/) and the code in [firmware/](firmware/).

| Step | What | Status |
|---|---|---|
| 1 | List of hardware | In progress |
| 2 | System architecture | Updated to the real parts (decisions to confirm) |
| 3 | Wiring and testing each component alone | Not started |
| 4 | Wiring list for every component | Written; circuit pictures 1 to 7 of 11 done |
| 5 | Code for the ESP32 and the STM32 | Not started |
| 6 | Wiring and testing 2 or more components together | Not started |
| 7 | Final system | Not started |

## Generative AI

- **Must have:** feeding plan generator, smart meal reports.
- **Stretch goals:** Ask Kibbly (chat), synthetic training photos.
- **Version 2:** explained alerts, dog's daily diary.

## Repository layout

```
firmware/   STM32 (STM32CubeIDE) and ESP32 (PlatformIO) code: drivers, scheduler, feeding logic, component tests
ai/         dataset tools, recognition model, generative AI experiments
app/        owner app and backend
hardware/   enclosure CAD, mechanism, PCB (KiCad), bill of materials
docs/       planning, meeting notes, course deliverables
```

## Plan

| Week | Milestone |
|---|---|
| 1 | Scope frozen, STM32 part chosen, parts ordered, generative AI direction chosen |
| 2 and 3 | Each subsystem works alone (dispense, weigh, recognize, notify) |
| 4 | First integration: recognize → dispense |
| 5 | Chime + app notifications, bug fixing |
| 6 | Demo rehearsal + backup video |
