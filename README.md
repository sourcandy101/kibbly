# Kibbly

**Knows every dog. Feeds every dog.**

Kibbly is a smart dog feeder that recognizes each dog, serves each one its own portion, blocks "seconds" for the greedy one, calls each dog by name in the owner's voice, and reports every meal in an app.

It is our **BEAR** project (Business · Embedded · AI · Research), built across three courses: Startup Engineering (ISS197), Embedded Systems and Prompt Engineering.

## Team

| Member | Role | Owns |
|---|---|---|
| Youssef Bousnina | Product Design & PCB Lead | `hardware/` (enclosure, mechanism, PCB) |
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

- **Main board: STM32** (exact part to choose: e.g. STM32N6 with neural accelerator, or STM32H7 + camera, or STM32 + companion module for vision).
- **Actuation:** motor + auger for portions, load cell (HX711) to weigh grams, speaker for the call.
- **Connectivity:** Wi-Fi/BLE module to reach the app.
- **AI:** dog recognition + **generative AI features** (to brainstorm, see below).

## Generative AI: ideas to brainstorm

Open question: what should Kibbly *generate*? Candidate directions to discuss as a team:

- Natural-language meal reports ("Mochi ate 30% less this week, here's what that may mean")
- Personalized feeding plans generated from each dog's profile and history
- Voice: generated calls/messages in the owner's voice or style
- Chat with Kibbly about your dog ("Did Biscuit eat today?")
- Synthetic dog images to augment the recognition dataset

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
