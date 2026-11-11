# Circuits by part

Wiring pictures of the feeder, one part at a time, then the full circuit. Each part has its own folder, named after the part, with everything about it inside. Every picture matches a wire table in [04_wiring_list.md](../04_wiring_list.md).

## Parts

| # | Part | Folder | Picture | Wire table | Status |
|---|---|---|---|---|---|
| 1 | Stepper motor and DRV8825 driver | [01_stepper_motor_drv8825/](01_stepper_motor_drv8825/README.md) | [svg](01_stepper_motor_drv8825/01_stepper_motor_drv8825.svg) | [Section 6B](../04_wiring_list.md#6b-drv8825-driver-and-stepper-motor-demo-driver) | Done |
| 2 | Load cell and HX711 | [02_load_cell_hx711/](02_load_cell_hx711/README.md) | [svg](02_load_cell_hx711/02_load_cell_hx711.svg) | [Section 7](../04_wiring_list.md#7-load-cell-and-hx711) | Done |
| 3 | Ultrasonic sensor (HC-SR04) | [03_ultrasonic_hc_sr04/](03_ultrasonic_hc_sr04/README.md) | [svg](03_ultrasonic_hc_sr04/03_ultrasonic_hc_sr04.svg) | [Section 8](../04_wiring_list.md#8-ultrasonic-sensor) | Done |
| 4 | Sound: MAX98357A amplifier and speaker | [04_sound_max98357a/](04_sound_max98357a/README.md) | [svg](04_sound_max98357a/04_sound_max98357a.svg) | [Section 11](../04_wiring_list.md#11-max98357a-and-speaker) | Done |
| 5 | ESP32-CAM link to the STM32 | [05_esp32_cam_link/](05_esp32_cam_link/README.md) | [svg](05_esp32_cam_link/05_esp32_cam_link.svg) | [Section 5](../04_wiring_list.md#5-esp32-cam-camera-board) | Done |
| 6 | Flashing the ESP32-CAM with the ESP32 DevKit V1 | [06_esp32_cam_flashing/](06_esp32_cam_flashing/README.md) | [svg](06_esp32_cam_flashing/06_esp32_cam_flashing.svg) | [Section 5B](../04_wiring_list.md#5b-flashing-the-esp32-cam-with-the-devkit) | Done |
| 7 | Power: 12 V, XL4015 to 5 V, 3.3 V | [07_power/](07_power/README.md) | [svg](07_power/07_power.svg) | [Section 4](../04_wiring_list.md#4-power) | Done |
| 8 | I2C bus: DS3231 clock and VL53L0X tank sensor | [08_i2c_clock_tank/](08_i2c_clock_tank/README.md) | [svg](08_i2c_clock_tank/08_i2c_clock_tank.svg) | [Section 9](../04_wiring_list.md#9-i2c-bus-vl53l0x-and-ds3231) | Done |
| 9 | microSD card (after the demo essentials) | | | Section 10 | Next |
| 10 | Button and status LED (after the demo essentials) | | | Section 12 | |
| 11 | Full circuit | | | All sections | |

Order: the parts the demo needs come first (1 to 7), then the parts that can wait (8 to 10), then the full circuit.

## Board and column map

Circuit 6 (flashing) is a bench setup off the breadboard. All the other circuits are drawn on **one 830 point breadboard (63 columns)**, each in its own zone, so they can stay plugged in together. Every part fits in columns 1 to 49, so a 60 column board works too. Each picture shows this map at the bottom, with its own zone highlighted.

Checked on the team's board (10 November 2026): 830 points, 63 columns, and the rails run along the whole length, so no bridge wires are needed.

**Rails**

| Rail | Use |
|---|---|
| Top + | **5 V** (amplifier, HC-SR04, ESP32-CAM, microSD), from the XL4015 (circuit 7); before circuit 7, from the Nucleo 5V pin (wire R1) |
| Top − and bottom − | GND (joined by wire R4 in column 1) |
| Bottom + | **3.3 V** (HX711, clock, tank sensor, driver logic) |
| 12 V | **On no rail**: only column 5, top half (the driver VMOT column). Mark it with red tape |

Each rail hole takes one wire. The rail column of every wire is listed in [04_wiring_list.md, section 13](../04_wiring_list.md#13-totals-per-rail), so two circuits never need the same hole.

**Columns** (each column has a top half, rows f to j, and a bottom half, rows a to e, which are not connected to each other)

| Columns | Top half | Bottom half |
|---|---|---|
| 1 to 3 | Power entries: R1 (before circuit 7) or P6, R2 to R4, DC jack GND | Power entries |
| 5 to 12 | 1: driver power and motor (12 V in column 5); 7: XL4015 5 V entry on the top rails at columns 12 and 13 | 1: driver control |
| 15 to 21 | 4: sound amplifier | 2: HX711 (columns 15 to 18) |
| 24 to 27 | 3: HC-SR04 wires | 3: voltage divider (column 26) |
| 29 to 34 | 5: ESP32-CAM link (its 5 V, GND and capacitor on the top rails, columns 36 to 38) | 8: I2C bus: clock (DS3231) in row a, column 31 = SCL, column 32 = SDA; the tank sensor joins these columns |
| 36 to 42 | 9: microSD | Free (spare) |
| 44 to 49 | | 10: button and LED |

Parts that must face outside (HC-SR04, ESP32-CAM camera, tank sensor, speaker, load cell, motor) sit off the board and reach their zone with jumper wires.

Rail wires shared by every circuit (R1 to R4) are in [04_wiring_list.md, section 4B](../04_wiring_list.md#4b-breadboard-rails-and-power-entries).

## How to read the pictures

1. **A dot with a white ring** is a wire end plugged into that hole. A wire drawn over other holes is not connected to them.
2. **Colours** follow the colour code of the wiring list: red 12 V, orange 5 V, yellow 3.3 V, black GND, grey and brown for signals. Cables that come with a part (like the motor cable) keep their own colours, which do not follow this code.
3. **Breadboard:** columns 1 to 63, rows a to j. The 5 holes of one column on the same side of the middle gap are connected together. Each rail row is connected along its whole length (on some other boards it is cut in the middle, which shows as a break in the red and blue lines).
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
