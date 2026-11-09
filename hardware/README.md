# Kibbly hardware

Owners: Youssef Bousnina (Embedded and Hardware Lead) and Hedi Ennaifer (Hardware and Electrical Lead).

This folder holds everything technical about the feeder: parts, architecture, wiring and test results. The code for the STM32 and the ESP32 lives in [`firmware/`](../firmware/). The main [README](../README.md) explains the project in general.

## What the feeder does

1. At meal time the feeder plays the call of the first dog ("Biscuit!") from the SD card.
2. An ultrasonic sensor notices when an animal comes in front of the bowl.
3. The ESP32-CAM takes a photo and asks the AI server which dog it is.
4. If it is the right dog, the STM32 turns the dispenser in small bursts of about 5 g while the dog stays there.
5. A scale under the bowl measures how much was served and how much was eaten.
6. The feeder writes the meal into the database, and the app shows it to the owner.

The feeder keeps working without internet: it follows the schedule saved on the SD card and uploads its logs when WiFi comes back.

## Two boards, two jobs

| Board | Job |
|---|---|
| **NUCLEO-F439ZI (STM32)** | Real time control: clock and schedule, motor, scale, sensors, speaker, SD card, button and LED |
| **ESP32 camera board** (XIAO ESP32S3 Sense, see step 1) | Camera and WiFi: photos to the AI server, reading and writing the database, passing orders to the STM32 |

The two boards talk to each other over a serial cable (UART).

## The database is our link to the software

The hardware never talks to the app directly. Everything goes through the Firebase database, which Moetaz owns.

| Direction | Data | Firebase collection |
|---|---|---|
| Database to feeder | Meal times and grams per dog | `schedules` |
| Database to feeder | Dog names, calling order, voice clips | `dogs` |
| Feeder to database | Each meal: dog, time, grams served, grams eaten, recognized, confidence | `meals` |
| Feeder to database | Alerts: skipped meal, unknown dog, wrong dog, jam, low tank, offline, power cut | `alerts` |
| Feeder to database | WiFi status and last time seen | `homes` |

The exact field names are agreed with Moetaz and are listed in `docs/SPEC.md` section 6.

## Workflow

We build the hardware in 7 steps, in order. Each step has its own file or folder. When a step is done, we update its file, tick it below and push.

| Step | What | Where | Status |
|---|---|---|---|
| 1 | List of hardware | [01_hardware_list.md](01_hardware_list.md) | In progress |
| 2 | System architecture | `02_system_architecture.md` | Not started |
| 3 | Wiring and testing each component alone | [03_component_tests/](03_component_tests/) | Not started |
| 4 | Wiring list for every component | `04_wiring_list.md` | Not started |
| 5 | Code for the ESP32 and the STM32 | [`firmware/`](../firmware/) | Not started |
| 6 | Wiring and testing 2 or more components together | `06_integration/` | Not started |
| 7 | Final system | `07_final_system.md` | Not started |

Repository rules: English only, no dashes of any kind in docs, comments or commit messages (use numbered lists or tables), snake_case file names.
