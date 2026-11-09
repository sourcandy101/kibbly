# Step 2: System architecture

How the parts from [step 1](01_hardware_list.md) fit together: which board does what, how they talk, how power flows, which pin each part uses, and how a meal runs from start to end.

## Contents

| # | Section | What it shows |
|---|---|---|
| 1 | [Overview](#1-overview) | The whole system in layers: cloud, boards, parts |
| 2 | [Who decides what](#2-who-decides-what) | The job of the STM32 and the job of the ESP32 |
| 3 | [Connection diagram](#3-connection-diagram) | Every part, its bus and its pins |
| 4 | [Communication links](#4-communication-links) | Bus types, speeds, addresses, UART messages |
| 5 | [Power](#5-power) | Power tree, voltages, currents, safety rules |
| 6 | [Pin plan](#6-pin-plan) | The exact pin for every wire |
| 7 | [One meal in time order](#7-one-meal-in-time-order) | Messages between STM32, ESP32, AI server and Firebase |
| 8 | [STM32 states](#8-stm32-states) | The feeder program as a state machine |
| 9 | [Decision at the bowl](#9-decision-at-the-bowl) | What happens for each AI answer |
| 10 | [Dispensing and jam check](#10-dispensing-and-jam-check) | How each 5 g burst is checked with the scale |
| 11 | [Failure handling](#11-failure-handling) | Jam, tank, WiFi, power cut |
| 12 | [Data with the database](#12-data-with-the-database) | What the feeder reads and writes in Firebase |
| 13 | [Button and LED](#13-button-and-led) | Press patterns and LED states |
| 14 | [Decisions to confirm](#14-decisions-to-confirm) | Open points for the team |

## 1. Overview

```mermaid
flowchart TB
    subgraph CLOUD["Cloud and software"]
        APP["Web app (Moetaz)"]
        FB[("Firebase database (Moetaz)")]
        AI["AI server (Zaineb)"]
        APP <--> FB
        AI <--> FB
    end

    subgraph FEEDER["Feeder (Youssef and Hedi)"]
        ESP["ESP32S3 camera board<br/>eyes and internet link"]
        STM["NUCLEO-F439ZI<br/>brain, real time control"]
        ESP <-->|"UART 115200"| STM
    end

    subgraph PARTS["Parts on the STM32"]
        MOT["Dispenser<br/>TMC2209, NEMA 17, auger"]
        SCALE["Scale<br/>load cell, HX711"]
        PRES["Presence<br/>ultrasonic sensor"]
        TANK["Tank level<br/>VL53L1X"]
        CLK["Clock<br/>DS3231"]
        SD["Storage<br/>microSD"]
        SND["Sound<br/>MAX98357A, speaker"]
        UI["Button and LED"]
    end

    ESP <-->|"WiFi HTTPS"| FB
    ESP <-->|"WiFi HTTP photo"| AI
    STM --- MOT
    STM --- SCALE
    STM --- PRES
    STM --- TANK
    STM --- CLK
    STM --- SD
    STM --- SND
    STM --- UI
```

## 2. Who decides what

The STM32 is the **brain**: it runs the meal, owns the clock and the schedule copy, and keeps working when WiFi is down. The ESP32 is the **eyes and the internet link**: it only does what the STM32 asks and reports back.

| Decision or job | STM32 | ESP32 |
|---|---|---|
| Meal time (clock and schedule) | Yes | No |
| Playing the dog's call | Yes | No |
| Detecting an animal | Yes (ultrasonic) | No |
| Taking a photo and asking the AI server | No | Yes, when the STM32 asks |
| Deciding to dispense | Yes, from the AI answer | No |
| Motor, scale, tank level | Yes | No |
| Reading schedules and voice clips from Firebase | No | Yes, then sends them to the STM32 |
| Writing meals and alerts to Firebase | No | Yes, from messages sent by the STM32 |
| Offline logs | Yes (SD card) | No |
| WiFi pairing and status | No | Yes, reports the status to the STM32 |
| Correct time | Yes (DS3231) | Sends internet time once a day to correct it |

Why this split: if WiFi, the ESP32 or the AI server fails, the STM32 alone still feeds the dogs on time.

## 3. Connection diagram

Every arrow shows the bus and the STM32 pins it uses. Full pin table in [section 6](#6-pin-plan).

```mermaid
flowchart LR
    subgraph NUCLEO["NUCLEO-F439ZI"]
        STM["STM32F439ZI<br/>3.3 V logic"]
    end

    ESP["ESP32S3 camera board"]
    DRV["TMC2209 driver"]
    MOT["NEMA 17 stepper<br/>and auger"]
    HX["HX711"]
    LC["5 kg load cell<br/>under the bowl"]
    US["Ultrasonic sensor<br/>3.3 V version"]
    TOF["VL53L1X<br/>I2C 0x29"]
    RTC["DS3231<br/>I2C 0x68"]
    SDC["microSD breakout"]
    AMP["MAX98357A"]
    SPK["4 ohm 3 W speaker"]
    BTN["Push button"]
    LED["Status LED"]

    STM <-->|"USART6<br/>PC6 TX, PC7 RX"| ESP
    STM -->|"TIM1 PE9 STEP<br/>PF13 DIR, PF15 EN"| DRV
    STM <-->|"USART2 single wire<br/>PD5 PDN_UART"| DRV
    DRV -->|"4 coil wires"| MOT
    LC -->|"4 wires E+ E- A+ A-"| HX
    HX -->|"PF14 DOUT<br/>PE13 SCK"| STM
    STM -->|"PD14 TRIG"| US
    US -->|"TIM4 PD15 ECHO"| STM
    STM <-->|"I2C1 PB8 SCL, PB9 SDA"| TOF
    STM <-->|"I2C1 PB8 SCL, PB9 SDA"| RTC
    STM <-->|"SPI1 PA5 SCK, PA6 MISO<br/>PB5 MOSI, PE11 CS"| SDC
    STM -->|"I2S3 PC10 BCLK<br/>PC12 DIN, PA4 LRC"| AMP
    AMP --> SPK
    BTN -->|"PF12 interrupt"| STM
    STM -->|"PG14"| LED
```

## 4. Communication links

| Link | Between | Type | Speed or setting |
|---|---|---|---|
| Feeder to cloud | ESP32 and Firebase | WiFi, HTTPS | |
| Recognition | ESP32 and AI server | WiFi, HTTP: JPEG photo in, dog id and confidence out | Answer within about 1 s |
| Boards | STM32 and ESP32 | UART, 3.3 V, text lines ending with a newline | 115200 baud, 8N1 |
| Motor driver settings | STM32 and TMC2209 | Single wire UART (current, microsteps, stall detection) | 115200 baud |
| Motor movement | STM32 and TMC2209 | STEP pulses from a timer, DIR and EN levels | 1/16 microsteps, 3200 steps per auger turn |
| Scale | STM32 and HX711 | 2 wire serial (clock and data) | 10 readings per second, gain 128 |
| Presence | STM32 and ultrasonic | TRIG pulse of 10 us, ECHO pulse timed by TIM4 | One reading every 100 ms |
| Sensors and clock | STM32, VL53L1X, DS3231 | I2C1 bus | 400 kHz |
| Storage | STM32 and microSD | SPI1 with FatFs | Up to 12 MHz |
| Sound | STM32 and MAX98357A | I2S3 with DMA | WAV, 16 kHz, 16 bit, mono |
| Debug | STM32 and computer | ST-LINK virtual serial port (USART3, PD8, PD9) | 115200 baud |

### I2C addresses

| Device | Address | Note |
|---|---|---|
| VL53L1X | 0x29 | Fixed at power on |
| DS3231 | 0x68 | Real time clock |
| AT24C32 EEPROM on the DS3231 module | 0x57 | Present on most modules, not used |

### UART messages between the boards

One message per line, readable as text, so we can watch and type them in a serial monitor while testing. Every message gets `OK` or `ERR` back, so a lost message is noticed and sent again. Final format is fixed in step 5.

| Direction | Message | Meaning |
|---|---|---|
| STM32 to ESP32 | `PHOTO` | An animal is in front of the bowl: take a photo and ask the AI server |
| ESP32 to STM32 | `DOG,biscuit,94` | AI answer: dog id and confidence in percent |
| ESP32 to STM32 | `DOG,unknown,0` | An animal that is not one of the home's dogs |
| ESP32 to STM32 | `DOG,none,0` | No animal, or a person |
| ESP32 to STM32 | `DOG,error,0` | AI server or WiFi unavailable |
| STM32 to ESP32 | `MEAL,biscuit,1730900000,280,265,1,94` | Meal log: dog, time, grams served, grams eaten, recognized, confidence |
| STM32 to ESP32 | `ALERT,jam` | Alert to write to Firebase (skipped, unknown_dog, wrong_dog, jam, low_tank, empty_tank, power_cut) |
| STM32 to ESP32 | `TANK,62` | Tank level in percent |
| ESP32 to STM32 | `SCHED,biscuit,1,08:00,280,18:00,280` | Schedule for one dog: id, call order, then time and grams for each meal |
| ESP32 to STM32 | `CLIP,biscuit,8000` | A voice clip of 8000 bytes follows, to save on the SD card |
| ESP32 to STM32 | `TIME,1730900000` | Internet time to correct the clock |
| ESP32 to STM32 | `WIFI,1` | WiFi status: 1 connected, 0 offline, 2 pairing |
| STM32 to ESP32 | `PAIR` | Button pressed twice: start WiFi pairing |
| Both | `OK`, `ERR` | Reply to every message |

## 5. Power

```mermaid
flowchart TB
    AD["12 V 3 A wall adapter"]
    PROT["3 A fuse and<br/>reverse polarity protection"]
    BUS12["12 V bus"]
    BK["XL4015 buck converter<br/>set to 5.0 V"]
    BUS5["5 V bus"]
    LDO["Nucleo 3.3 V regulator<br/>500 mA max"]
    BUS3["3.3 V bus"]

    DRV["TMC2209 VM and motor<br/>0.8 A peak"]
    NU["NUCLEO-F439ZI E5V<br/>0.2 A"]
    ESP["ESP32S3 5V pin<br/>0.5 A peak"]
    AMP["MAX98357A VIN<br/>0.8 A peak"]
    S3["HX711, ultrasonic, VL53L1X,<br/>DS3231, microSD, TMC2209 VIO<br/>about 0.15 A"]

    AD --> PROT --> BUS12
    BUS12 --> DRV
    BUS12 --> BK --> BUS5
    BUS5 --> NU
    BUS5 --> ESP
    BUS5 --> AMP
    NU --> LDO --> BUS3 --> S3
```

| Rail | Source | Loads | Peak current | Margin |
|---|---|---|---|---|
| 12 V | Adapter, 3 A | Motor driver, buck converter | About 1.6 A | Adapter gives 3 A |
| 5 V | XL4015, 5 A | Nucleo, ESP32, amplifier | About 1.5 A | Buck gives 5 A |
| 3.3 V | Nucleo regulator, 500 mA | Sensors, SD card, driver logic, STM32 | About 0.25 A | Half of the limit |

Rules:

1. **All grounds are connected together**: adapter, buck, Nucleo, ESP32, driver, amplifier. Without a common ground, UART and sensors give wrong values.
2. **Set the buck to 5.0 V with the multimeter before connecting anything** to it. A new XL4015 can come set to any voltage.
3. A 1000 uF capacitor and a 100 nF capacitor sit at the TMC2209 12 V input, and another pair at the ESP32 5 V pin.
4. The motor driver needs its 12 V before the motor moves, and the motor wires are **never** plugged or unplugged while the driver is powered (this destroys the TMC2209).
5. During development the Nucleo runs from USB. When it runs from the 5 V bus, set the power jumper to E5V (see the Nucleo user manual UM1974) and do not rely on USB power at the same time.
6. On most DS3231 modules a charging circuit is fitted for a rechargeable LIR2032 cell. With a normal CR2032, remove the charging resistor or diode on the module.

## 6. Pin plan

Pins chosen to avoid the ones already used on the board by Ethernet (PA1, PA2, PA7, PB13, PC1, PC4, PC5, PG11, PG13), USB (PA8 to PA12, PG6, PG7) and the ST-LINK serial port (PD8, PD9). **Check every pin in STM32CubeMX and the user manual UM1974 before wiring**; CubeMX shows conflicts in red.

### NUCLEO-F439ZI

| # | Part | Signal | STM32 pin | Header label | Peripheral | Direction |
|---|---|---|---|---|---|---|
| 1 | TMC2209 | STEP | PE9 | D6 | TIM1 channel 1, pulse output | Out |
| 2 | TMC2209 | DIR | PF13 | D7 | GPIO | Out |
| 3 | TMC2209 | EN (low enables the motor) | PF15 | D2 | GPIO | Out |
| 4 | TMC2209 | PDN_UART | PD5 | CN9 | USART2 TX, single wire mode, through 1 kohm | In and out |
| 5 | HX711 | DOUT | PF14 | D4 | GPIO | In |
| 6 | HX711 | SCK | PE13 | D3 | GPIO | Out |
| 7 | Ultrasonic | TRIG | PD14 | D10 | GPIO | Out |
| 8 | Ultrasonic | ECHO | PD15 | D9 | TIM4 channel 4, input capture | In |
| 9 | VL53L1X and DS3231 | SCL | PB8 | D15 | I2C1 | Out |
| 10 | VL53L1X and DS3231 | SDA | PB9 | D14 | I2C1 | In and out |
| 11 | microSD | SCK | PA5 | D13 | SPI1 | Out |
| 12 | microSD | MISO | PA6 | D12 | SPI1 | In |
| 13 | microSD | MOSI | PB5 | CN7 | SPI1 (PA7 avoided, used by Ethernet) | Out |
| 14 | microSD | CS | PE11 | D5 | GPIO | Out |
| 15 | MAX98357A | BCLK | PC10 | CN8 | I2S3 CK | Out |
| 16 | MAX98357A | DIN | PC12 | CN8 | I2S3 SD | Out |
| 17 | MAX98357A | LRC | PA4 | CN7 | I2S3 WS | Out |
| 18 | ESP32 | STM32 TX to ESP32 RX | PC6 | CN7 | USART6 TX | Out |
| 19 | ESP32 | STM32 RX from ESP32 TX | PC7 | CN7 | USART6 RX | In |
| 20 | Button | Input | PF12 | D8 | GPIO with interrupt, internal pull up | In |
| 21 | Status LED | Output | PG14 | D1 | GPIO, through 330 ohm | Out |

Built in parts kept for debugging: LD1 green (PB0), LD2 blue (PB7), LD3 red (PB14), user button (PC13), ST-LINK serial port (PD8, PD9) for printing logs to the computer.

### ESP32S3 (XIAO Sense)

| Signal | XIAO pin | Connects to |
|---|---|---|
| UART TX | D6 (GPIO43) | STM32 PC7 |
| UART RX | D7 (GPIO44) | STM32 PC6 |
| 5V | 5V | 5 V bus |
| GND | GND | Common ground |

The camera is built into the Sense board. USB C stays free for flashing and logs.

### TMC2209 module

| Driver pin | Connects to |
|---|---|
| VM | 12 V bus, with 1000 uF and 100 nF capacitors |
| GND (motor side and logic side) | Common ground |
| VIO | 3.3 V bus |
| STEP, DIR, EN | STM32 PE9, PF13, PF15 |
| PDN_UART | STM32 PD5 through 1 kohm |
| MS1, MS2 | GND (driver address 0) |
| A1, A2, B1, B2 | Motor coils (check the pairs with the multimeter) |

## 7. One meal in time order

Example: Biscuit eats at 18:00, then Mochi.

```mermaid
sequenceDiagram
    autonumber
    participant RTC as DS3231 clock
    participant STM as STM32
    participant DOG as Dog at the bowl
    participant ESP as ESP32S3
    participant AI as AI server
    participant FB as Firebase

    RTC->>STM: It is 18.00
    STM->>STM: Schedule says Biscuit, 280 g, called first
    STM->>DOG: Plays biscuit.wav from the SD card
    DOG->>STM: Ultrasonic reads under 40 cm
    STM->>ESP: PHOTO
    ESP->>AI: POST /recognize with a JPEG
    AI-->>ESP: dog_id biscuit, confidence 94
    ESP-->>STM: DOG,biscuit,94
    Note over STM: Called dog and 94 is 80 or more, so serve
    loop Until 280 g served or Biscuit leaves
        STM->>STM: One 5 g burst, check the scale gained weight
        STM->>ESP: PHOTO every few seconds
        ESP-->>STM: DOG,biscuit,9x
    end
    Note over STM: Biscuit leaves, wait 2 minutes, weigh what is left
    STM->>STM: Save the meal line on the SD card
    STM->>ESP: MEAL,biscuit,time,280,265,1,94
    ESP->>FB: Write to meals
    ESP-->>STM: OK
    FB-->>FB: App shows Biscuit ate 265 g
    STM->>DOG: Plays mochi.wav, next dog
```

## 8. STM32 states

The main feeder program is one state machine. Each box is a state; each arrow is the event that changes it.

```mermaid
stateDiagram-v2
    [*] --> Boot
    Boot --> Idle : clock read, schedule loaded from SD
    Boot --> Idle : missed meals found, ALERT power_cut sent

    Idle --> CheckTank : meal time reached
    CheckTank --> Calling : food available
    CheckTank --> Idle : tank empty, ALERT empty_tank, no meal

    Calling --> WaitPresence : call played
    WaitPresence --> Recognizing : animal under 40 cm
    WaitPresence --> Calling : no dog after 5 or 10 minutes, call again
    WaitPresence --> Logging : no dog after 15 minutes, ALERT skipped

    Recognizing --> Dispensing : called dog, confidence 80 or more
    Recognizing --> WaitPresence : another known dog, ALERT wrong_dog
    Recognizing --> UnknownPortion : unknown dog
    Recognizing --> WaitPresence : no animal or a person
    Recognizing --> Dispensing : AI or WiFi down, serve in owner order

    UnknownPortion --> Logging : at most 20 g served, ALERT unknown_dog

    Dispensing --> Dispensing : burst done, dog still there
    Dispensing --> Settling : portion complete or dog left
    Dispensing --> JamAlert : 3 bursts without weight gain

    JamAlert --> Idle : motor stopped, ALERT jam

    Settling --> Logging : 2 minutes without eating
    Logging --> Calling : next dog in the order
    Logging --> Idle : all dogs done
```

## 9. Decision at the bowl

```mermaid
flowchart TD
    A["Animal under 40 cm"] --> B["STM32 sends PHOTO"]
    B --> C{"Answer from ESP32"}
    C -->|"DOG,error"| OFF["Offline mode:<br/>serve the called dog<br/>without recognition,<br/>log recognized = 0"]
    C -->|"DOG,none"| N["Nothing dispensed,<br/>keep waiting"]
    C -->|"DOG,unknown"| U{"Unknown portions<br/>today under 2?"}
    U -->|"Yes"| U1["Serve at most 20 g,<br/>ALERT unknown_dog with photo"]
    U -->|"No"| U2["Nothing dispensed,<br/>ALERT unknown_dog"]
    C -->|"DOG,id,confidence"| K{"id is the called dog?"}
    K -->|"No"| W["Nothing dispensed,<br/>ALERT wrong_dog"]
    K -->|"Yes"| T{"Confidence 80 or more?"}
    T -->|"No"| R["Treat as unknown,<br/>ask for one more photo"]
    T -->|"Yes"| S["Serve in 5 g bursts"]
```

## 10. Dispensing and jam check

The scale checks every burst, so a jam or an empty tank is noticed after a few grams.

```mermaid
flowchart TD
    START["Start of serving<br/>target = portion grams"] --> TARE["Read the scale: start weight"]
    TARE --> BURST["Turn the auger for one burst<br/>(about 5 g, calibrated in step 3)"]
    BURST --> WAIT["Wait 1 s for the kibble to settle"]
    WAIT --> READ["Read the scale"]
    READ --> GAIN{"Weight went up<br/>by 2 g or more?"}
    GAIN -->|"No"| CNT{"3 failed bursts<br/>in a row?"}
    CNT -->|"No"| REV["Turn back half a turn<br/>to free the auger"] --> BURST
    CNT -->|"Yes"| JAM["Stop the motor<br/>ALERT jam"]
    GAIN -->|"Yes"| DONE{"Served grams reached<br/>the target?"}
    DONE -->|"Yes"| FIN["Stop, go to Settling"]
    DONE -->|"No"| DOG{"Dog still there?<br/>(ultrasonic and photo)"}
    DOG -->|"Yes"| BURST
    DOG -->|"No"| FIN
```

Second jam check: the TMC2209 stall detection (StallGuard) flags a blocked motor even before the scale reading.

## 11. Failure handling

| Failure | How the feeder notices | What it does | Alert sent |
|---|---|---|---|
| Jam | 3 bursts in a row without weight gain, or TMC2209 stall flag | Turns back to free the auger, then stops the motor | `jam` |
| Low tank | VL53L1X distance above the low threshold | Keeps serving | `low_tank` |
| Empty tank | VL53L1X distance at the bottom, or bursts without weight | No meal | `empty_tank` (urgent) |
| WiFi or AI server down | `DOG,error` or no answer within 5 s | Serves meals in the owner's order without recognition; saves logs on the SD card | `offline`, sent when WiFi is back |
| Power cut | At boot, last meal time on the SD card is older than a scheduled meal | Does not serve missed meals automatically; lists them | `power_cut` with the number of missed meals |
| SD card missing or broken | FatFs mount fails at boot | Uses the last schedule kept in STM32 flash and plays a built in chime instead of voice clips | `offline` style alert with the reason |
| ESP32 not answering | No `OK` to 3 messages | Treats it like WiFi down; resets the ESP32 through its power or reset line in a later version | none until it is back |

## 12. Data with the database

The database is the only link between the feeder and the software. Field names follow `docs/SPEC.md` section 6 and are agreed with Moetaz.

```mermaid
flowchart LR
    subgraph FB["Firebase"]
        HOMES[("homes")]
        DOGS[("dogs")]
        SCHED[("schedules")]
        MEALS[("meals")]
        ALERTS[("alerts")]
        STORE[("Storage:<br/>voice clips")]
    end

    ESP["ESP32S3"]
    STM["STM32 and SD card"]

    DOGS -->|"names, call order"| ESP
    SCHED -->|"meal times, grams"| ESP
    STORE -->|"WAV clips"| ESP
    ESP -->|"SCHED, CLIP"| STM
    STM -->|"MEAL, ALERT, TANK"| ESP
    ESP -->|"new meal"| MEALS
    ESP -->|"new alert"| ALERTS
    ESP -->|"WiFi status, last seen,<br/>tank level"| HOMES
```

| Collection | Feeder reads | Feeder writes | When |
|---|---|---|---|
| `homes/{homeId}` | | WiFi status, last seen, tank level | Every 5 minutes and on change |
| `dogs/{dogId}` | Name, call order, voice clip url | | When the app changes them |
| `schedules/{dogId}` | Up to 4 meals: time, grams | | When the app changes them |
| `meals/{mealId}` | | Dog, time, grams served, grams eaten, recognized, confidence | After each meal (later if offline) |
| `alerts/{alertId}` | | Type, time, message, photo url | When it happens (later if offline) |
| Storage | Voice clip files | Photo of an unknown dog | When a clip changes; on unknown dog |

## 13. Button and LED

```mermaid
flowchart TD
    P["Button pressed"] --> L{"Held more than 3 s?"}
    L -->|"Yes"| OFFS["Shut down:<br/>motor disabled, feeder asleep"]
    L -->|"No"| CNT["Count presses<br/>within 2 s"]
    CNT --> N{"Number of presses"}
    N -->|"2"| PAIR["WiFi pairing:<br/>STM32 sends PAIR to the ESP32"]
    N -->|"5"| RST["Reset the feeder"]
    N -->|"Other"| IGN["Ignored"]
```

| LED | Meaning |
|---|---|
| Solid | Connected to WiFi |
| Blinking | Pairing mode |
| Off | Offline |

## 14. Decisions to confirm

| # | Decision | Proposed | With |
|---|---|---|---|
| 1 | STM32 is the brain, ESP32 only camera and internet | Yes | Hedi |
| 2 | UART text messages at 115200 baud, every message answered with `OK` or `ERR` | Yes | Hedi |
| 3 | Presence distance that starts a photo | Under 40 cm | Hedi |
| 4 | Audio format on the SD card | WAV, 16 kHz, 16 bit, mono (the app converts recordings) | Moetaz |
| 5 | Firebase access from the ESP32 | Firestore REST API | Moetaz |
| 6 | AI endpoint | `POST /recognize` with a JPEG, answer `{"dog_id": "biscuit", "confidence": 94}` | Zaineb |
| 7 | Values from the spec | 80% confidence, 5 g bursts, calls at 0, 5 and 10 minutes, alert at 15, unknown dog 20 g twice a day | Team |
| 8 | Jam rule | 3 bursts in a row with less than 2 g gain | Hedi |
| 9 | Missed meals after a power cut | Not served automatically, the owner decides in the app | Team |
