# Step 1: List of hardware

One chosen part per job, picked for reliability and for good support on the STM32 and ESP32. Fill the **Have it** column with Hedi (yes, ordered or no).

## 1. Boards

| # | Part | Qty | Job | Why this one | Have it |
|---|---|---|---|---|---|
| 1 | **NUCLEO-F439ZI** | 1 | Main controller: schedule, motor, scale, sensors, sound, SD card, button | Team choice. Enough timers, I2C, SPI, I2S and UART for every part below; built in ST-LINK for flashing and debugging | Yes |
| 2 | **Seeed XIAO ESP32S3 Sense** (camera board) | 1 | Camera and WiFi; link to the AI server and Firebase | More reliable than the AI Thinker ESP32-CAM: USB C for flashing (no extra programmer), 8 MB PSRAM for photos, external antenna for stable WiFi, fewer brownout resets. Fallback: AI Thinker ESP32-CAM with an ESP32-CAM-MB programmer if already bought | |

## 2. Dispenser

| # | Part | Qty | Job | Why this one | Have it |
|---|---|---|---|---|---|
| 3 | **NEMA 17 stepper motor**, 42 x 40 mm, about 0.4 Nm, 1.5 A | 1 | Turns the auger | Precise, repeatable rotation, so each burst gives the same amount of kibble | See with Hedi's ISS Group |
| 4 | **TMC2209 driver module** (BigTreeTech or FYSETC) | 1 | Drives the stepper from the STM32 | Silent, current set in software over UART, built in stall detection (StallGuard) as a second jam check next to the scale | See with Hedi's ISS Group|
| 5 | **Auger**, 3D printed in PETG, with a 5 mm shaft coupler | 1 | Pushes about 5 g of kibble per burst | An auger meters dry kibble evenly and rarely jams; PETG is stronger and safer for food than PLA | |

## 3. Sensors

| # | Part | Qty | Job | Why this one | Have it |
|---|---|---|---|---|---|
| 6 | **Load cell, bar type, 5 kg** | 1 | Scale under the bowl | 5 kg survives a dog pushing on the bowl; resolution with the HX711 is still well under 1 g | |
| 7 | **HX711 board** (SparkFun or a shielded clone) | 1 | Reads the load cell | Standard 24 bit amplifier, simple 2 wire interface, many tested drivers | |
| 8 | **RCWL-1601 or HC-SR04P ultrasonic sensor** (3.3 V versions) | 1 | Detects an animal in front of the bowl | Same as the HC-SR04 the team chose, but runs at 3.3 V, so its signal is safe for the STM32 without a voltage divider | |
| 9 | **VL53L1X time of flight sensor** | 1 | Food level in the tank, from the lid | Narrow beam that sees the kibble surface; ST provides an official STM32 driver (ULD). Better range and stability than the VL53L0X | |
| 10 | **DS3231 RTC module** with a CR2032 coin cell | 1 | Keeps the real time during a power cut | Accurate to about 1 minute per year; without it the feeder loses the time after a power cut when WiFi is down | |

## 4. Sound and storage

| # | Part | Qty | Job | Why this one | Have it |
|---|---|---|---|---|---|
| 11 | **MAX98357A I2S amplifier** | 1 | Plays the voice clips | Digital audio from the STM32 I2S port: no hiss or motor noise, unlike the DAC with an analog amplifier | |
| 12 | **Speaker, 4 ohm, 3 W** | 1 | The dog's call or a chime | Matches the MAX98357A output; loud enough for a room | |
| 13 | **MicroSD breakout, 3.3 V, SPI** (Adafruit or similar) and an 8 to 32 GB card from a known brand | 1 | Voice clips, schedule copy, offline meal logs | SPI with FatFs is the simplest reliable setup on STM32; branded cards avoid corrupted files | |

## 5. Button and LED

| # | Part | Qty | Job | Why this one | Have it |
|---|---|---|---|---|---|
| 14 | **Push button**, 12 mm, panel mount | 1 | Long press: shut down. 2 presses: WiFi pairing. 5 presses: reset | Panel mount survives daily use better than a breadboard button | |
| 15 | **LED and 330 ohm resistor** | 1 | WiFi status | | |

## 6. Power

| # | Part | Qty | Job | Why this one | Have it |
|---|---|---|---|---|---|
| 16 | **12 V 3 A wall adapter** | 1 | Powers the whole feeder | Covers the motor and the 5 V rail with margin (see the budget below) | |
| 17 | **DC barrel jack with screw terminals** | 1 | Adapter input | Screw terminals do not shake loose | |
| 18 | **Inline fuse, 3 A**, and a **reverse polarity diode or MOSFET** | 1 | Protection | A wrong adapter or a short does not burn the boards | |
| 19 | **XL4015 buck converter** set to 5.0 V (5 A) | 1 | 5 V for the Nucleo, the ESP32, the amplifier and the sensors | Large current margin, so WiFi and audio peaks do not drop the voltage | |
| 20 | **Capacitors: 1000 uF electrolytic and 100 nF ceramic** | 2 of each | Next to the ESP32 and the motor driver | Absorb current peaks and protect against resets | |

The TMC2209 takes 12 V directly. The Nucleo takes 5 V on its E5V pin (power jumper set to E5V) and makes its own 3.3 V for the sensors.

### Power budget

| Load | Rail | Peak current |
|---|---|---|
| Stepper through the TMC2209 | 12 V | 0.8 A |
| ESP32S3 with camera and WiFi | 5 V | 0.5 A |
| NUCLEO-F439ZI | 5 V | 0.2 A |
| MAX98357A at full volume | 5 V | 0.8 A |
| Sensors, SD card, RTC | 3.3 V from the Nucleo | 0.1 A |
| **Total from the adapter** | 12 V | **about 1.6 A** (adapter gives 3 A) |

## 7. Mechanical

| # | Part | Qty | Job | Have it |
|---|---|---|---|---|
| 21 | Food tank for 1 kg of kibble (about 2.5 L) | 1 | Holds the food | |
| 22 | Stainless steel bowl | 1 | Sits on the load cell | |
| 23 | Body and mounts (3D printed or laser cut) | 1 | Holds everything | |

## 8. Prototyping tools

| # | Part | Qty | Job | Have it |
|---|---|---|---|---|
| 24 | Breadboards, jumper wires (male and female), Dupont and JST connectors | several | Tests in steps 3 and 6 | |
| 25 | Multimeter | 1 | Check every voltage before connecting a board | |
| 26 | Known weights or a kitchen scale | 1 | Calibrate the load cell | |

## Changes from the original spec

| Item | Spec | Chosen here | Reason |
|---|---|---|---|
| Camera board | AI Thinker ESP32-CAM | XIAO ESP32S3 Sense | Reliability and easier flashing. Same role, so nothing changes for Zaineb or Moetaz |
| Dispenser | Open | Auger, NEMA 17, TMC2209 | Precise bursts and jam detection |
| Tank level | Open | VL53L1X | Official ST driver, stable reading of the kibble surface |
| Audio | STM32 DAC and analog amplifier | MAX98357A over I2S | Clean sound next to a motor |
| Clock | STM32 internal RTC | DS3231 module | Keeps the time through power cuts |
| Ultrasonic | HC-SR04 | 3.3 V version | Safe signal levels for the STM32 |
