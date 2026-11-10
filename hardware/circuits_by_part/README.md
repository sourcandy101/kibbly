# Circuits by part

Wiring pictures of the feeder, one part at a time, then the full circuit. Each part has its own picture and its own page, named after the part. Every picture matches a wire table in [04_wiring_list.md](../04_wiring_list.md).

## Parts

| # | Part | Page | Picture | Wire table | Status |
|---|---|---|---|---|---|
| 1 | Stepper motor and DRV8825 driver | [01_stepper_motor_drv8825.md](01_stepper_motor_drv8825.md) | [svg](01_stepper_motor_drv8825.svg) | [Section 6B](../04_wiring_list.md#6b-drv8825-driver-and-stepper-motor-local-option) | Done |
| 2 | Load cell and HX711 | | | Section 7 | Next |
| 3 | Ultrasonic sensor (HC-SR04) | | | Section 8 | |
| 4 | I2C bus: DS3231 clock and VL53L0X | | | Section 9 | |
| 5 | microSD card | | | Section 10 | |
| 6 | MAX98357A amplifier and speaker | | | Section 11 | |
| 7 | Button and status LED | | | Section 12 | |
| 8 | ESP32-CAM link to the STM32 | | | Section 5 | |
| 9 | Flashing the ESP32-CAM with the ESP32 DevKit V1 | | | Parts list, programming note | |
| 10 | Power: 12 V, XL4015 to 5 V, 3.3 V | | | Section 4 | |
| 11 | Full circuit | | | All sections | |

## How to read the pictures

1. **A dot with a white ring** is a wire end plugged into that hole. A wire drawn over other holes is not connected to them.
2. **Colours** follow the colour code of the wiring list: red 12 V, orange 5 V, yellow 3.3 V, black GND, grey and brown for signals. Cables that come with a part (like the motor cable) keep their own colours, which do not follow this code.
3. **Breadboard:** columns 1 to 30, rows a to j. The 5 holes of one column on the same side of the middle gap are connected together. Each rail row is connected along its length; on some breadboards the rail is cut in the middle (a break in the red and blue lines): bridge it with a short wire if so.
4. **Nucleo pins** are named three ways: board label (D6), STM32 pin (PE9) and header pin number (CN10 pin 4). Pin numbers come from the Nucleo user manual UM1974: check them on the board before plugging.

## Editing a picture

Each picture is drawn by a Python script in [scripts/](scripts/). To change a picture, edit its script and run it from this folder:

```
python3 scripts/make_01_stepper_motor_drv8825.py 01_stepper_motor_drv8825.svg
```
