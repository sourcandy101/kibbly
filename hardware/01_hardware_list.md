# Step 1: List of hardware

Every part the prototype needs, sorted in groups:

| Group | Meaning | Parts |
|---|---|---|
| [A. Owned](#a-owned) | The team already has it | 8 |
| [B. Buy in Tunisia](#b-buy-in-tunisia) | Not owned yet; sold online by a Tunisian shop (link given) | 15 |
| [C. No link in Tunisia](#c-no-link-in-tunisia) | Not owned yet; no Tunisian online seller found (ask a shop, make it, or import) | 9 |
| [D. Extra parts](#d-extra-parts-not-used-in-the-prototype) | Owned, but not used in the prototype | 2 |

**How to use this list**

1. Compare each picture with the parts on the table. The model name printed on the board must match.
2. Write what we have in **Have it** (yes, ordered or no). A part marked yes moves to group A.
3. For a missing part, open the **Buy in Tunisia** link. Prices and stock change: call the shop before going.
4. When a part differs from this list, write its exact model in **Have it**; we update the architecture and wiring to match.
5. "See with Hedi's ISS Group" means the part may be borrowed: check that before buying.

Links checked on 9 November 2026. Pictures come from the shop pages (they belong to the shops) or from Wikimedia Commons (free licence, credited at the end).

## A. Owned

| # | Picture | Part | Category | Qty | Price (TND) | Job | Buy in Tunisia | Have it |
|---|---|---|---|---|---|---|---|---|
| 1 | <img src="https://little-son.tn/2066-large_default/carte-de-developpement-nucleo-144-stm32f439zit6.jpg" width="90"> | **NUCLEO-F439ZI** (Nucleo 144 board, STM32F439ZIT6) | Board | 1 | 165 | Main controller: schedule, motor, scale, sensors, sound, SD card, button | [Little Son](https://little-son.tn/accueil/1348-carte-de-developpement-nucleo-144-stm32f439zit6.html) | Yes |
| 2 | <img src="https://little-son.tn/1166-large_default/esp32-cam-carte-de-developpement-esp32-cp2102-camera-ov2640-avec-port-usb-.jpg" width="90"> | **ESP32-CAM** with OV2640 camera and a microSD slot (the slot is not used) | Board | 1 | 45 (or 35 plus 9 for the USB board) | Camera and WiFi; link to the AI server and Firebase | [Little Son (with USB board)](https://little-son.tn/accueil/603-esp32-cam-carte-de-developpement-esp32-cp2102-camera-ov2640-avec-port-usb-.html), [SELI (USB C version)](https://seli.tn/product/esp32-cam-ov2640-type-c/), or [ESP32-CAM alone](https://little-son.tn/accueil/242-esp32-cam-carte-de-dev-wifi-bluetooth-avec-module-camera-ov2640.html) plus [USB board](https://little-son.tn/accueil/1410-module-shield-de-programmation-televersement-pour-esp32-cam.html) | Yes, without the USB board: flashed with the ESP32 DevKit V1 |
| 6 | <img src="https://www.celectronix.com/17008-product_main_2x/capteur-de-force-poids-5kg-czl635-5-avec-module-hx711-convertisseur-a-d-24-bit.jpg" width="90"> | **Load cell, bar type, 5 kg** | Sensor | 1 | 29.9 (with an HX711) | Scale under the bowl | [Celectronix (5 kg cell with HX711)](https://www.celectronix.com/capteurs/3302-capteur-de-force-poids-5kg-czl635-5-avec-module-hx711-convertisseur-a-d-24-bit.html) | Yes |
| 15 | <img src="https://little-son.tn/1241-large_default/kit-100-diode-led-5mm-light-assorti-diy.jpg" width="90"> | **LED and 330 ohm resistor** | Button and LED | 1 | 7.5 for the kit (about 0.5 for one LED) | WiFi status | [Little Son (LED kit)](https://little-son.tn/accueil/762-kit-100-diode-led-5mm-light-assorti-diy.html) | Yes |
| 25 | <img src="https://little-son.tn/42-large_default/plaque-d-essai-830pts.jpg" width="90"> | **Breadboard 830 points** | Tool | 2 | 5.3 each | Tests in steps 3 and 6 | [Little Son](https://little-son.tn/accueil/37-plaque-d-essai-830pts.html) | Yes |
| 26 | <img src="https://little-son.tn/2470-large_default/40-fils-de-connexion-jumper-ff-40cm.jpg" width="90"> | **Jumper wires** (female to female, male to male, male to female) | Tool | 40 of each | 12 per pack of 40 | Connections | [Little Son (F/F)](https://little-son.tn/accueil/1691-40-fils-de-connexion-jumper-ff-40cm.html), [Little Son (M/M)](https://little-son.tn/accueil/1530-40-fils-de-connexion-jumper-mm-40cm.html) | Yes |
| 29 | <img src="https://little-son.tn/1205-large_default/carte-esp32-wroom-32d-wifi-bluetooth-.jpg" width="90"> | **ESP32 DevKit V1** (ESP32 WROOM 32, USB) | Board | 1 | 32 | Flashes the ESP32-CAM; test board for the WiFi, server and UART code | [Little Son](https://little-son.tn/accueil/729-carte-esp32-wroom-32d-wifi-bluetooth-.html) | Yes |
| 30 | <img src="https://little-son.tn/1214-large_default/cordon-usb-micro-usb-pour-raspberry-pi-microbit-esp-longueur-15m.jpg" width="90"> | **USB cables** (micro USB) | Tool | 3 | 7.5 each | Power and program the Nucleo and the DevKit from the computer | [Little Son](https://little-son.tn/accueil/737-cordon-usb-micro-usb-pour-raspberry-pi-microbit-esp-longueur-15m.html) | Yes |

## B. Buy in Tunisia

| # | Picture | Part | Category | Qty | Price (TND) | Job | Buy in Tunisia | Have it |
|---|---|---|---|---|---|---|---|---|
| 3 | <img src="https://little-son.tn/2229-large_default/moteur-nema-17-pas-a-pas-17hs4401s.jpg" width="90"> | **NEMA 17 stepper motor** (17HS4401 or similar, 42 x 40 mm, about 0.4 Nm, 1.5 A) | Dispenser | 1 | 35 (29.9 at Celectronix) | Turns the auger | [Little Son](https://little-son.tn/accueil/1481-moteur-nema-17-pas-a-pas-17hs4401s.html), [Didactico](https://didactico.tn/produit/moteur-pas-a-pas-nema-17/), [Celectronix](https://www.celectronix.com/moteur-pas-pas/3986-moteur-pas-a-pas-nema-17-17hs4401.html) | See with Hedi's ISS Group |
| 4B | <img src="https://little-son.tn/852-large_default/module-driver-moteur-pas-a-pas-drv8825-.jpg" width="90"> | **DRV8825 driver** (local fallback): same size and pins for STEP, DIR, EN; louder, no stall detection | Dispenser | 1 | 8.5 | Same job, if no TMC2209 | [Little Son](https://little-son.tn/accueil/559-module-driver-moteur-pas-a-pas-drv8825-.html) |  |
| 7 | <img src="https://2btrading.tn/1882-large_default/hx711-module-load-cell-amplifier.jpg" width="90"> | **HX711 board** | Sensor | 1 | 7 | Reads the load cell | [2B Trading](https://2btrading.tn/accueil/1884-hx711-module-load-cell-amplifier.html), [Little Son](https://little-son.tn/accueil/521-capteur-de-pesage-hx711.html) | No |
| 8 | <img src="https://little-son.tn/413-large_default/module-capteur-ultrason-hc-sr04.jpg" width="90"> | **HC-SR04 ultrasonic sensor** with a 1 kohm and a 2 kohm resistor | Sensor | 1 | 4.8 | Detects an animal in front of the bowl | [Little Son](https://little-son.tn/accueil/294-module-capteur-ultrason-hc-sr04.html) | No |
| 9 | <img src="https://little-son.tn/1739-large_default/gy-530-vl53l0x-v2-module-telemetre-laser-temps-de-vol-i2c.jpg" width="90"> | **VL53L0X time of flight sensor** (GY-530 board) | Sensor | 1 | 20 (19.5 at 2B Trading) | Food level in the tank, from the lid | [Little Son](https://little-son.tn/accueil/1121-gy-530-vl53l0x-v2-module-telemetre-laser-temps-de-vol-i2c.html), [2B Trading](https://2btrading.tn/arduino/2218-module-capteur-de-distance-de-portee-laser-vl53l0x-v2.html) | No |
| 10 | <img src="https://little-son.tn/687-large_default/module-rtc-ds3231-i2c-at24c32-pour-arduino.jpg" width="90"> | **DS3231 RTC module** with a CR2032 coin cell | Sensor | 1 | 8, plus about 3 for the coin cell | Keeps the real time during a power cut | [Little Son](https://little-son.tn/accueil/454-module-rtc-ds3231-i2c-at24c32-pour-arduino.html), [Souilah](https://souilah-electronique.tn/modules-et-capteurs/78-module-rtc-ds3231-.html) | No |
| 11 | <img src="https://little-son.tn/2637-large_default/module-max98357a-i2s-amplificateur-audio.jpg" width="90"> | **MAX98357A I2S amplifier** | Sound and storage | 1 | 14 (9.9 at 2B Trading) | Plays the voice clips, clean digital sound | [Little Son](https://little-son.tn/accueil/1651-module-max98357a-i2s-amplificateur-audio.html), [2B Trading](https://2btrading.tn/accueil/9068-module-max98357a-i2s-audio-amplifier.html) | No |
| 13 | <img src="https://souilah-electronique.tn/656-large_default/module-sd.jpg" width="90"> | **MicroSD card module (SPI)** and an 8 to 32 GB card from a known brand | Sound and storage | 1 | 7, plus about 20 for the card | Voice clips, schedule copy, offline meal logs | [Souilah](https://souilah-electronique.tn/modules-et-capteurs/396-module-sd.html), [Celectronix](https://www.celectronix.com/modules-kits/7382-waveshare-micro-sd-storage-board-copie-.html) | No |
| 16 | <img src="https://little-son.tn/2577-large_default/alimentation-12v-2a.jpg" width="90"> | **12 V wall adapter**, at least 2 A (3 A better) | Power | 1 | 12 | Powers the whole feeder | [Little Son (12 V 2 A)](https://little-son.tn/accueil/1319-alimentation-12v-2a.html) | See with Hedi's ISS Group |
| 17 | <img src="https://little-son.tn/2200-large_default/module-adaptateur-courant-dc-fiche-jack-pour-arduino.jpg" width="90"> | **DC barrel jack with screw terminals** | Power | 1 | 4 | Adapter input | [Little Son](https://little-son.tn/accueil/1456-module-adaptateur-courant-dc-fiche-jack-pour-arduino.html) | See with Hedi's ISS Group |
| 18 | <img src="https://little-son.tn/721-large_default/porte-fusible-5x20mm-avec-couvercle-noir.jpg" width="90"> | **Fuse holder 5 x 20 mm with a 3 A fuse** | Power | 1 | 0.55, plus about 1 for the fuse | Protection against shorts | [Little Son (fuse holder)](https://little-son.tn/accueil/480-porte-fusible-5x20mm-avec-couvercle-noir.html); ask for a 3 A 5 x 20 mm fuse in the same order | No |
| 19 | <img src="https://little-son.tn/512-large_default/module-xl4015-abaisseur-de-tension-dc-dc-5a-75w.jpg" width="90"> | **XL4015 buck converter**, set to 5.0 V (5 A) | Power | 1 | 12 | 5 V for the Nucleo, the ESP32, the amplifier and the SD card | [Little Son](https://little-son.tn/accueil/345-module-xl4015-abaisseur-de-tension-dc-dc-5a-75w.html), [TET Electronics](https://tet-electronics.com/product/module-xl4015-convertisseur-abaisseur-de-tension-dc-dc-5a-75w-e3ee5b2e) | No |
| 20 | <img src="https://little-son.tn/1218-large_default/kit-condensateurs-electrolytiques-en-aluminium-120-pieces-12-valeurs-022uf-470uf.jpg" width="90"> | **Capacitors**: 1000 uF 25 V electrolytic (or two 470 uF in parallel) and 100 nF ceramic | Power | 2 of each | about 1 each when bought singly (kits 25 each) | Next to the ESP32 and the motor driver | [Little Son (electrolytic kit, up to 470 uF)](https://little-son.tn/accueil/739-kit-condensateurs-electrolytiques-en-aluminium-120-pieces-12-valeurs-022uf-470uf.html), [Little Son (ceramic kit, includes 100 nF)](https://little-son.tn/accueil/741-kit-condensateurs-ceramiques-300-pieces-10-valeurs-2pf-01uf.html) | See with Hedi |
| 21 | <img src="https://little-son.tn/2593-large_default/resistance-1kohm-14w.jpg" width="90"> | **Resistors**: 330 ohm, 1 kohm, 2 kohm, 10 kohm | Power | 2 of each | 0.05 each | LED, ultrasonic divider, driver UART, motor enable | [Little Son 1 kohm](https://little-son.tn/accueil/1796-resistance-1kohm-14w.html), [Little Son 2 kohm](https://little-son.tn/accueil/1797-resistance-2kohm-14w.html); the others in the same shop |  |
| 27 | <img src="https://little-son.tn/1644-large_default/multimetre-numerique-dt9205a-.jpg" width="90"> | **Multimeter** | Tool | 1 | 26.1 | Check every voltage before connecting a board | [Little Son](https://little-son.tn/accueil/1050-multimetre-numerique-dt9205a-.html) |  |

## C. No link in Tunisia

| # | Picture | Part | Category | Qty | Price (TND) | Job | Buy in Tunisia | Have it |
|---|---|---|---|---|---|---|---|---|
| 4 | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Trinamic_TMC2209_stepper_motor_controller_board.jpg/250px-Trinamic_TMC2209_stepper_motor_controller_board.jpg" width="90"> | **TMC2209 driver** (first choice): silent, stall detection, current set in software | Dispenser | 1 | about 20 to 40 imported (estimate) | Drives the stepper from the STM32 | **Not found in Tunisian shops.** Borrow from the ISS group, or order abroad | See with Hedi's ISS Group |
| 5 |  | **Auger**, 3D printed in PETG, with a 5 mm shaft coupler | Dispenser | 1 | about 15 (estimate) | Pushes about 5 g of kibble per burst | 3D print (school fab lab or a print shop) |  |
| 12 |  | **Speaker, 4 or 8 ohm, 2 to 3 W**, about 40 to 50 mm | Sound and storage | 1 | about 8 (estimate) | The dog's call or a chime | No online listing found: ask any electronics shop for "haut parleur 4 ohm 3 W", or reuse one from old computer speakers | No |
| 14 |  | **Push button**, momentary, 12 mm, panel mount | Button and LED | 1 | about 2 (estimate) | Long press: shut down. 2 presses: WiFi pairing. 5 presses: reset | Ask any electronics shop for "bouton poussoir 12 mm" | No |
| 18B |  | **3 A Schottky diode** (1N5822 or SS54) | Power | 1 | about 1 (estimate) | Protection against a reversed adapter | No online listing found: ask any electronics shop. The 1N4007 sold online is only 1 A, too weak | No |
| 22 |  | Food tank for 1 kg of kibble (about 2.5 L) | Mechanical | 1 | about 15 (estimate) | Holds the food | Household shop, or 3D print |  |
| 23 |  | Stainless steel bowl | Mechanical | 1 | about 10 (estimate) | Sits on the load cell | Pet shop or household shop |  |
| 24 |  | Body and mounts (3D printed or laser cut) | Mechanical | 1 | about 40 (estimate) | Holds everything | School fab lab |  |
| 28 |  | Known weights or a kitchen scale | Tool | 1 | 0 | Calibrate the load cell | Home |  |

## D. Extra parts, not used in the prototype

Parts the team owns that do not fit the prototype. Kept here so nobody buys or wires them by mistake.

| Picture | Part | Qty | Why it is not used | Possible later use |
|---|---|---|---|---|
| | **Raspberry Pi Camera v1.3** (OV5647, ribbon cable) | 1 | Its ribbon cable uses the MIPI CSI interface, which only Raspberry Pi boards have. The ESP32 and the STM32F439 cannot read it | Collecting dog photos for the AI dataset, if someone has a Raspberry Pi |
| <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Force_Sensing_Resistor_cropped.jpg/250px-Force_Sensing_Resistor_cropped.jpg" width="90"> | **FSR force sensors** | 2 | Not accurate enough to weigh food (readings vary by about 25% and drift); the load cell does this job | Stretch goal: a pressure pad on the floor in front of the bowl, to confirm a dog is standing there before taking a photo |

## Notes on parts

Camera board note: the XIAO ESP32S3 Sense recommended before is more reliable but is **not sold in Tunisia** (only from [Seeed Studio](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html), with weeks of shipping). The ESP32-CAM is sold locally and does the same job; it needs the 1000 uF capacitor on its 5 V pin to avoid resets.

Programming note: the ESP32-CAM has no USB port and we have no USB board for it. The ESP32 DevKit V1 flashes it instead:

1. Connect DevKit `EN` to DevKit `GND`. This keeps the DevKit chip off, so its USB chip talks to the ESP32-CAM.
2. Connect DevKit `TX0` to ESP32-CAM `U0T`, and DevKit `RX0` to ESP32-CAM `U0R` (TX to TX and RX to RX: this is correct in this setup).
3. Connect DevKit `VIN` (5 V) to ESP32-CAM `5V`, and `GND` to `GND`.
4. Connect ESP32-CAM `IO0` to `GND` (flash mode), then press the ESP32-CAM reset button.
5. Upload from the computer through the DevKit USB port.
6. Remove the `IO0` wire and press reset again to run the program.

If this is unreliable, the ESP32-CAM-MB USB board costs about 9 TND at [Little Son](https://little-son.tn/accueil/1410-module-shield-de-programmation-televersement-pour-esp32-cam.html).

Driver note: with the DRV8825 the scale is the only jam check, which is enough for the demo. The wiring changes slightly (no UART wire, three microstep pins); we update it after the inventory.

Sensor notes:

1. The 3.3 V ultrasonic versions (RCWL-1601, HC-SR04P) are not sold locally. The standard HC-SR04 works at 5 V; its Echo wire goes through the two resistors so the STM32 receives 3.3 V.
2. The VL53L1X is not sold locally. The VL53L0X reaches 2 m, more than enough for a 1 kg tank, and ST also provides its STM32 driver.

Power note: avoid the "alimentation à découpage" metal box supplies; they need 230 V wiring by hand. A closed wall adapter is safer.

## Power budget

| Load | Rail | Peak current |
|---|---|---|
| Stepper through the driver | 12 V | 0.8 A |
| ESP32-CAM with WiFi | 5 V | 0.5 A |
| NUCLEO-F439ZI | 5 V | 0.2 A |
| MAX98357A at full volume | 5 V | 0.8 A |
| Sensors, SD card, RTC | 3.3 V and 5 V | 0.15 A |
| **Total from the adapter** | 12 V | **about 1.6 A** (a 2 A adapter is enough, 3 A leaves more margin) |

## Cost

Prices in Tunisian dinars (TND) from the shop pages on 9 November 2026, mostly Little Son so one order covers almost everything. Values marked "about" are estimates where no online price was found. Delivery is not included (Souilah delivers free from 150 DT).

### Everything from scratch

| Group | Parts | Price (TND) |
|---|---|---|
| Boards | NUCLEO-F439ZI 165, ESP32-CAM with USB board 45 | 210 |
| Dispenser | NEMA 17 35, DRV8825 8.5, printed auger about 15 | about 58.5 |
| Sensors | 5 kg load cell with HX711 29.9, HC-SR04 4.8, VL53L0X 20, DS3231 8, coin cell about 3 | about 65.7 |
| Sound and storage | MAX98357A 14, speaker about 8, microSD module 7, card about 20 | about 49 |
| Button, LED, resistors | Button about 2, LED about 0.5, resistors about 1 | about 3.5 |
| Power | Adapter 12, DC jack 4, fuse holder 0.55, fuse and diode about 2, XL4015 12, capacitors bought singly about 3 | about 33.6 |
| **Electronics total** | | **about 420** |
| Mechanical | Tank and bowl about 25, printed body and mounts about 40 | about 65 |
| Tools | 2 breadboards 10.6, 3 packs of jumper wires 36, multimeter 26.1 | 72.7 |
| **Total from scratch** | | **about 560** |

### Still to buy

Based on the **Have it** column (10 November 2026): the team already has the NUCLEO-F439ZI, the ESP32-CAM, the ESP32 DevKit V1, the load cell, the LED, breadboards, jumper wires and USB cables.

| Part | Price (TND) |
|---|---|
| HX711 | 7 |
| HC-SR04 and resistors | about 6 |
| VL53L0X | 20 |
| DS3231 and coin cell | about 11 |
| MAX98357A | 14 |
| Speaker | about 8 |
| microSD module and card | about 27 |
| Push button | about 2 |
| Fuse, fuse holder, diode | about 2.5 |
| XL4015 | 12 |
| **Total** | **about 110** |

| Case | Extra | New total (TND) |
|---|---|---|
| The ISS group cannot lend the motor, driver, adapter, jack and capacitors | NEMA 17 35, DRV8825 8.5, adapter 12, DC jack 4, capacitors about 3 | **about 173** |
| Mechanical parts | Tank, bowl, printed body and auger | about 80 more |
| Multimeter, if nobody on the team has one | DT9205A | 26.1 more |

### Ways to save

1. Buy capacitors singly (about 1 TND each) instead of the two kits (25 TND each).
2. Buy the MAX98357A at 2B Trading (9.9) instead of Little Son (14).
3. Buy the NEMA 17 at Celectronix (29.9) instead of Little Son (35).
4. Borrow a multimeter at school.
5. Flash the ESP32-CAM with the ESP32 DevKit V1 instead of buying the USB board (9 TND).
6. Keep the DRV8825 (8.5) for the demo instead of importing a TMC2209 (about 20 to 40 with shipping, and weeks of waiting).

## Shops

| Shop | Website | Note |
|---|---|---|
| Little Son | [little-son.tn](https://little-son.tn) | Has almost every part on this list, including the NUCLEO-F439ZI |
| 2B Trading | [2btrading.tn](https://2btrading.tn) | HX711, VL53L0X, MAX98357A, XL4015 |
| Souilah Electronique | [souilah-electronique.tn](https://souilah-electronique.tn) | microSD module, DS3231, XL4015; free delivery from 150 DT |
| Celectronix | [celectronix.com](https://www.celectronix.com) | 5 kg load cell with HX711, NEMA 17, microSD |
| Didactico | [didactico.tn](https://didactico.tn) | NEMA 17; shop in Sfax, delivery in 24 to 48 h |
| SELI | [seli.tn](https://seli.tn) | ESP32-CAM with USB C |
| TET Electronics | [tet-electronics.com](https://tet-electronics.com) | XL4015; delivery in 1 to 3 days |

Tip: ordering most parts from one shop (Little Son) saves delivery costs and time.

## Changes from the original spec

| Item | Spec | Chosen here | Reason |
|---|---|---|---|
| Camera board | AI Thinker ESP32-CAM | ESP32-CAM with USB board (XIAO ESP32S3 Sense only if imported) | XIAO not sold in Tunisia |
| Dispenser | Open | Auger, NEMA 17, TMC2209 (DRV8825 as local fallback) | Precise bursts and jam detection |
| Tank level | Open | VL53L0X | Sold locally; enough range for the tank |
| Audio | STM32 DAC and analog amplifier | MAX98357A over I2S | Clean sound next to a motor |
| Clock | STM32 internal RTC | DS3231 module | Keeps the time through power cuts |
| Ultrasonic | HC-SR04 | HC-SR04 with a resistor divider on Echo | 3.3 V versions not sold locally |

## Picture credits

1. TMC2209 board: "Trinamic TMC2209 stepper motor controller board", Wikimedia Commons, CC BY-SA 4.0.
2. FSR sensor: "Force Sensing Resistor", Wikimedia Commons, CC BY-SA 2.0.
3. All other pictures: product photos from the linked shop pages.
