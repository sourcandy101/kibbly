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
- **Camera + Wi-Fi:** ESP32-CAM.
- **AI server (Python):** dog recognition + generative AI.
- **Data:** Firebase. **App:** web app (PWA).
- **Sensors:** bowl load cell, food tank level, ultrasonic presence sensor.

## Generative AI

- **Must have:** feeding plan generator, smart meal reports.
- **Stretch goals:** Ask Kibbly (chat), synthetic training photos.
- **Version 2:** explained alerts, dog's daily diary.

## Repository layout

```
firmware/   STM32 project (STM32CubeIDE): drivers, scheduler, feeding logic
ai/         dataset tools, recognition model, generative AI experiments
app/        owner app and backend
hardware/   enclosure CAD, mechanism, PCB (KiCad), bill of materials
docs/       planning, meeting notes, course deliverables
```

## Plan

| Week | Milestone |
|---|---|
| 1 | Scope frozen, STM32 part chosen, parts ordered, generative AI direction chosen |
| 2–3 | Each subsystem works alone (dispense, weigh, recognize, notify) |
| 4 | First integration: recognize → dispense |
| 5 | Chime + app notifications, bug fixing |
| 6 | Demo rehearsal + backup video |
