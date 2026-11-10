# Circuit 3: Ultrasonic sensor HC-SR04

![Circuit 3: ultrasonic sensor HC-SR04](03_ultrasonic_hc_sr04.svg)

**What it is for:** the sensor that notices an animal in front of the bowl and starts the photo. Only the laptop USB is needed: the Nucleo 5V pin feeds the top + rail (5 V).

**Where on the board:** columns 24 to 27, with the divider in column 26 (see the [column map](../README.md#board-and-column-map)). The sensor itself sits outside the board.

**Parts:** NUCLEO-F439ZI, HC-SR04, one 1 kohm resistor, one 2 kohm resistor, breadboard, 4 female to male jumper wires for the sensor, other jumper wires, USB cable.

**Wire table:** wires U1 to U8 in [04_wiring_list.md, section 8](../../04_wiring_list.md#8-ultrasonic-sensor), plus rails R1, R3 and R4 in [section 4B](../../04_wiring_list.md#4b-breadboard-rails-and-power-entries).

## How it measures

```
Nucleo ── Trig (10 µs pulse) ──► HC-SR04 ──► sends a sound burst (40 kHz, silent for us)
Nucleo ◄── Echo (pulse, through the divider) ── HC-SR04 ◄── the sound bounces back
```

1. The Nucleo sends a 10 µs pulse on **Trig**.
2. The sensor sends a short ultrasonic burst and raises **Echo** until the sound comes back.
3. The Nucleo times the Echo pulse with timer TIM4: **distance in cm = pulse length in µs ÷ 58**.
4. Under 40 cm means an animal is in front of the bowl.

## Why the sensor is outside the board

In the feeder the sensor is mounted on the front, facing the dog, so it is joined to the board with 4 female to male wires: VCC and Gnd straight into the top rails (5 V and GND), Trig and Echo into columns 25 and 26.

## Why two resistors

The HC-SR04 runs on 5 V, so its **Echo** pin goes up to 5 V. An STM32 pin wants 3.3 V. The two resistors form a **voltage divider**:

| Resistor | From | To | Colour bands |
|---|---|---|---|
| 1 kohm | Echo (column 26, top half) | Column 26, bottom half, across the middle gap | brown, black, red |
| 2 kohm | Column 26, bottom half | Bottom − rail (GND) | red, black, red |

The middle point (column 26, bottom half) sees 5 V × 2 ÷ 3 = **3.3 V**: this is where the Nucleo PD15 wire goes. **Never connect Echo straight to the Nucleo.**

**Trig** needs no resistor: the Nucleo sends 3.3 V, which the sensor accepts as "high".

## Where 5 V comes from

The top + rail is the 5 V rail. For the tests it is fed by the Nucleo 5V pin (wire R1); in the full circuit it is fed by the 5 V supply of circuit 7 (power), and R1 is removed.

## Wiring order

1. USB unplugged.
2. Rails: R4 (join the two GND rails, column 1), R3 (Nucleo GND), R1 (Nucleo 5V to the top + rail).
3. U5: 1 kohm across the middle gap in column 26 (row f to row e).
4. U6: 2 kohm from column 26, row a, to the bottom − rail.
5. U7: column 25 (row h) to Nucleo D10 · PD14. U8: column 26 bottom half (row c) to Nucleo D9 · PD15.
6. Sensor: U4 (Gnd to the top − rail), U2 (Trig to column 25), U3 (Echo to column 26), then U1 (VCC to the top + rail).
7. Check: no wire from column 26 **top half** (Echo, 5 V) goes to the Nucleo. Only the bottom half of column 26 does.
8. Plug in the USB.

## First test

1. Point the sensor at a wall 50 cm away: the reading must be about 50 cm.
2. Move a hand closer: below 40 cm the program reports "animal present".
3. The test program and the results table come with the step 3 test file for this part.
