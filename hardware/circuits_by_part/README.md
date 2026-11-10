# Circuits by part

Wiring pictures of the feeder, one part at a time, then the full circuit. Each part has its own folder, named after the part, with everything about it inside. Every picture matches a wire table in [04_wiring_list.md](../04_wiring_list.md).

## Parts

| # | Part | Folder | Picture | Wire table | Status |
|---|---|---|---|---|---|
| 1 | Stepper motor and DRV8825 driver | [01_stepper_motor_drv8825/](01_stepper_motor_drv8825/README.md) | [svg](01_stepper_motor_drv8825/01_stepper_motor_drv8825.svg) | [Section 6B](../04_wiring_list.md#6b-drv8825-driver-and-stepper-motor-local-option) | Done |
| 2 | Load cell and HX711 | [02_load_cell_hx711/](02_load_cell_hx711/README.md) | [svg](02_load_cell_hx711/02_load_cell_hx711.svg) | [Section 7](../04_wiring_list.md#7-load-cell-and-hx711) | Done |
| 3 | Ultrasonic sensor (HC-SR04) | [03_ultrasonic_hc_sr04/](03_ultrasonic_hc_sr04/README.md) | [svg](03_ultrasonic_hc_sr04/03_ultrasonic_hc_sr04.svg) | [Section 8](../04_wiring_list.md#8-ultrasonic-sensor) | Done |
| 4 | I2C bus: DS3231 clock and VL53L0X | | | Section 9 | Next |
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

## Folder layout

```
circuits_by_part/
  README.md                         this index
  shared/common.py                  drawing pieces shared by every circuit (Nucleo, breadboard, wires)
  01_stepper_motor_drv8825/
    README.md                       the page: picture, how it works, wiring order, first test
    01_stepper_motor_drv8825.svg    the picture
    make_01_stepper_motor_drv8825.py   the script that draws the picture
  02_load_cell_hx711/
    (same three files)
```

Every new circuit gets its own folder with the same three files.

## Editing a picture

To change a picture, edit the script in the part folder and run it from that folder:

```
cd 01_stepper_motor_drv8825
python3 make_01_stepper_motor_drv8825.py 01_stepper_motor_drv8825.svg
```
