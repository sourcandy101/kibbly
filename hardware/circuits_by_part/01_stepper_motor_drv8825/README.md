# Circuit 1: Stepper motor and DRV8825 driver

![Circuit 1: stepper motor and DRV8825 driver on its carrier board](01_stepper_motor_drv8825.svg)

**What it is for:** the first milestone of the project, "the STM32 dispenses exactly N bursts on command". The Nucleo runs from the laptop USB; the motor runs from the 12 V adapter.

**The DRV8825 sits on a carrier board** (changed on 28 November 2026). The team's DRV8825 plugs into a red carrier board marked "Keyes 4988 PCB" (also sold as "Wcmcu Stepper motor for arduino control"). The carrier is made for the A4988; the DRV8825 has the same pin positions, so it plugs straight in. The carrier brings the capacitor, the micro step switches and a motor connector, and the 12 V goes straight to it: **no 12 V on the breadboard any more**.

**Where on the board:** the carrier and the motor sit off the board, above columns 6 to 11. On the board: columns 8 to 11, bottom half, for the control wires, and the top − rail at column 7 for the carrier GND (see the [column map](../README.md#board-and-column-map)).

**Parts:** NUCLEO-F439ZI, NEMA 17 motor, DRV8825, its carrier board (Keyes 4988 PCB), 12 V adapter, DC jack, 10 kohm resistor, breadboard, jumper wires (female to male for the carrier pins), USB cable, multimeter.

**Wire table:** wires V1 to V23 in [04_wiring_list.md, section 6B](../../04_wiring_list.md#6b-drv8825-driver-and-stepper-motor-demo-driver), plus rails R2 to R4 in [section 4B](../../04_wiring_list.md#4b-breadboard-rails-and-power-entries).

## How the parts talk

```
Motor ──4 wires──► carrier motor connector (1A, 1B, 2A, 2B)
                         │
                   carrier with the DRV8825 ◄── S, D, E ── breadboard columns 11, 10, 9 ── Nucleo
                         ▲          ▲
             12 V adapter, DC jack   3.3 V rail into the carrier 5V pin (switches only)
```

| Connection | What travels on it |
|---|---|
| Nucleo to carrier (S = STEP, D = DIR, E = EN) | Small 3.3 V orders: one step, this direction, motor on or off |
| 3.3 V rail to the carrier 5V pin | The logic level for the micro step switches and the carrier pull up resistors |
| 12 V adapter to the carrier (Vin, GND) | The power for the motor |
| Carrier to motor (the 4 motor wires) | The strong current that turns the motor |

The Nucleo never powers the motor: it only gives orders, and the driver uses the 12 V to move the motor.

## The carrier board

| Carrier part | Job | Setting |
|---|---|---|
| Socket, 2 rows of 8 | Holds the DRV8825 | Plug it in **by the labels**: the DRV8825 EN pin in the carrier EN corner, VMOT on VMOT. Do not go by where the potentiometer sits. Plugged in backwards, the 12 V destroys the driver |
| Micro step switches 1, 2, 3 | M0, M1, M2 of the DRV8825 | **1 OFF, 2 OFF, 3 ON**: 1/16 step, 3200 steps per turn. All three ON gives 1/32, and the test would turn only half a turn |
| 100 uF 50 V capacitor | Reserve on the motor supply; the DRV8825 needs 47 uF or more | Soldered on: the 470 uF of the first plan is no longer needed here |
| Power header: 5V, GND, 9V (Vin) | 5V: logic level for the switches. Vin: motor supply | 5V pin on **3.3 V** (V20 and V15), Vin on 12 V from the jack (V1), GND to the top − rail (V5) |
| Header S, D, E | STEP, DIR, EN. The "8 9 10" printed next to it are Arduino pin numbers: ignore them | To the Nucleo through columns 11, 10 and 9 |
| Motor connector 2B, 2A, 1A, 1B | 1A and 1B = coil A, 2A and 2B = coil B | Motor cable |

Your board may be a slightly different version (other header sizes or positions): match every pin **by the name printed next to it**, not by its place.

The "PLS USE 9V1A POWER" sticker is the seller's suggestion. 12 V is fine: the DRV8825 takes 8.2 to 45 V and the capacitor is rated 50 V.

Why 3.3 V on the pin marked 5V: the DRV8825 makes its own logic supply, so this pin only feeds the switches and the carrier pull up resistors. 3.3 V is high enough for the DRV8825 inputs and keeps 5 V away from the STM32 pins. The socket pin where an A4988 would take this supply is the FLT pin of the DRV8825, which has a protection resistor on its board, so this is safe.

## 12 V never touches the breadboard

The DC jack + screw goes straight to the carrier Vin pin (V1, red). The motor current comes back through the carrier GND (V5) to the top − rail and the jack − screw (V2). Nothing on the breadboard carries 12 V: the red 12 V column of the first plan is gone.

## The motor wires

The 4 coloured wires come from the motor and go **only to the carrier motor connector**.

| Motor wire | Coil | Carrier pin | DRV8825 pin |
|---|---|---|---|
| Black | A | 1A | A1 |
| Green | A | 1B | A2 |
| Red | B | 2A | B1 |
| Blue | B | 2B | B2 |

1. **These colours are not power colours.** The motor's red and black wires are coil wires: never connect them to a rail.
2. Colours vary by brand; the **pairs** matter. Find them with the multimeter (check 2 below).
3. If the motor only buzzes or shakes, the pairs are mixed: each pair must go on 1A and 1B, or on 2A and 2B. Swapping the two wires inside one coil only reverses the direction: do that, or change DIR in the code, if it turns the wrong way.

## Checks before wiring

No power anywhere for these checks. Take the DRV8825 **out** of the carrier for checks 4 to 6.

1. **Driver:** the board must say **DRV8825** (usually purple). If it says A4988, stop: that chip needs other settings.
2. **Coil pairs:** multimeter on ohm, measure between the motor wires. Two wires with about **1.5 to 2 ohm** between them are one coil; wires of different coils read nothing (OL). The table above expects black and green as coil A, red and blue as coil B. Write down your pairs.
3. **Adapter polarity:** plug the adapter into the jack, with the jack wired to nothing. Multimeter on DC V, red probe on the jack `+` screw, black probe on `−`: it must read about **+12 V**. If it reads −12 V, stop: the screws are marked the other way, and nothing in the circuit protects against a reversed supply.
4. **Carrier EN:** measure between the carrier **E** pin and its **5V** pin, then between **E** and **GND**.

| Reading | Meaning | What to do |
|---|---|---|
| A few kohm to 5V | The carrier pulls EN up: the motor is off at start | Keep V13 (two pull ups side by side are harmless) |
| A few kohm to GND | The carrier pulls EN down: the motor is on at start | Leave V13 out: it would fight the carrier resistor and leave EN half way. The motor then only holds still while the STM32 restarts, which is harmless at 1 A |
| Open both ways | EN floats | Keep V13 |

5. **Sleep and reset:** measure between the socket holes **SL** and **RT** and the **5V** pin. Both must read 0 ohm or a few kohm (held high). If they read open, stop: the DRV8825 would stay asleep, and they need a short wire to the 5V pin soldered on the back (ask Hedi).
6. **Switches:** with switch 3 ON, the **MS3** socket hole reads 0 ohm or a few kohm to the 5V pin; with it OFF, open. With switches 1 and 2 OFF, MS1 and MS2 read open. Then set **1 OFF, 2 OFF, 3 ON** and leave them.

## Wiring order

1. Everything unplugged: no adapter, no USB.
2. Switches 1 OFF, 2 OFF, 3 ON.
3. Plug the DRV8825 into the carrier by its labels: EN in the EN corner, VMOT on VMOT. Stick the small heatsink on its chip if it came with one.
4. Rails: R4 (join the two GND rails, column 1), R3 (Nucleo GND), R2 (Nucleo 3V3).
5. Bottom half of the breadboard: V15 (column 8, row a, to the 3.3 V rail), then V13 (10 kohm from column 9, row a, to the 3.3 V rail; leave it out if check 4 found a pull down).
6. Nucleo signals: V12 (D2 · PF15 to column 9, row b), V19 (D7 · PF13 to column 10, row d), V18 (D6 · PE9 to column 11, row c).
7. Carrier to the breadboard, female to male wires: V20 (5V pin to column 8, row e), V21 (E to column 9, row e), V22 (D to column 10, row e), V23 (S to column 11, row e).
8. Motor: plug the cable into the carrier motor connector, coil A on 1A and 1B, coil B on 2A and 2B (V7 to V10).
9. Power: V5 (carrier GND to the top − rail, column 7), V2 (DC jack − screw to the top − rail, column 3), then V1 (DC jack + screw to the carrier Vin pin).
10. Check before powering:
    1. The red wire goes from the jack + screw to the carrier Vin pin only, never into the breadboard.
    2. The carrier 5V pin goes to column 8 (3.3 V), never to the 5 V rail.
    3. Motor plugged in (never plug or unplug it with 12 V on).
11. Power on: USB first, then the adapter. Power off: adapter first, then the USB.
12. Set the current before loading the program. Black probe on the top − rail, red probe on the metal top of the DRV8825 potentiometer: turn it gently until it reads **0.50 V** (1 A). A plastic screwdriver is safest; with a metal one, do not touch the pins around it. The motor stays off meanwhile (or only holds still, if V13 was left out).

## Test program

The motor turns one full turn forward, pauses, turns one turn back, rests, and repeats. Anyone in the team can copy the three code blocks below (each block has a copy button on GitHub) into a new STM32CubeIDE project.

**Easier:** the complete file is in [firmware/tests/stepper_drv8825/main.c](../../../firmware/tests/stepper_drv8825/main.c). It replaces the whole `main.c` of a new project and sets its own pins, so steps 3 and 4 below are not needed; its [README](../../../firmware/tests/stepper_drv8825/README.md) has the short version of the steps.

### Make the project

1. STM32CubeIDE: **File, New, STM32 Project**, tab **Board Selector**, choose **NUCLEO-F439ZI**, and name the project `stepper_test`.
2. "Initialize all peripherals with their default Mode?": answer **No**, to keep the project small.
3. In the pin view, set **PE9**, **PF13** and **PF15** to **GPIO_Output**. The search box under the chip finds a pin by its name.
4. **System Core, GPIO, PF15**: set **GPIO output level** to **High**, so the motor starts off.
5. Save, and accept when it asks to generate the code.
6. Open `Core/Src/main.c` and paste the three blocks below between the matching `USER CODE` comments. Replace the empty comment pair with the whole block.
7. Plug in the USB, then the adapter, and check that Vref is set (wiring order step 12).
8. Click **Run** (the green play button). If it offers to update the ST-LINK firmware, accept.

### Code

Block 1, between `/* USER CODE BEGIN 0 */` and `/* USER CODE END 0 */`:

```c
/* USER CODE BEGIN 0 */
#define STEPS_PER_TURN 3200U   /* 1/16 step: M2 high, M0 and M1 low */
#define HALF_PERIOD_US 625U    /* 800 steps per second: one turn in 4 s */

static void delay_us(uint32_t us)
{
  uint32_t start = DWT->CYCCNT;
  uint32_t ticks = us * (SystemCoreClock / 1000000U);
  while ((DWT->CYCCNT - start) < ticks) { }
}

static void motor_enable(int on)
{
  /* EN is active low: 0 V turns the motor on */
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_15, on ? GPIO_PIN_RESET : GPIO_PIN_SET);
}

static void motor_steps(uint32_t steps, int forward)
{
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_13, forward ? GPIO_PIN_SET : GPIO_PIN_RESET);
  delay_us(5);  /* let DIR settle before the first step */
  for (uint32_t i = 0; i < steps; i++) {
    HAL_GPIO_WritePin(GPIOE, GPIO_PIN_9, GPIO_PIN_SET);
    delay_us(HALF_PERIOD_US);
    HAL_GPIO_WritePin(GPIOE, GPIO_PIN_9, GPIO_PIN_RESET);
    delay_us(HALF_PERIOD_US);
  }
}
/* USER CODE END 0 */
```

Block 2, between `/* USER CODE BEGIN 2 */` and `/* USER CODE END 2 */`:

```c
  /* USER CODE BEGIN 2 */
  CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;  /* cycle counter for delay_us */
  DWT->CYCCNT = 0;
  DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
  motor_enable(0);
  HAL_Delay(2000);
  /* USER CODE END 2 */
```

Block 3, inside `while (1)`, right after `/* USER CODE BEGIN 3 */`:

```c
    /* USER CODE BEGIN 3 */
    motor_enable(1);
    motor_steps(STEPS_PER_TURN, 1);  /* one turn forward */
    HAL_Delay(1000);
    motor_steps(STEPS_PER_TURN, 0);  /* one turn back */
    motor_enable(0);                 /* rest: motor free and cool */
    HAL_Delay(2000);
```

| Setting | Value | Meaning |
|---|---|---|
| `STEPS_PER_TURN` | 3200 | 200 full steps times 16 microsteps (M2 high, M0 and M1 low) |
| `HALF_PERIOD_US` | 625 | 800 steps per second, one turn in 4 s. A bigger value turns slower |
| STEP, DIR, EN | PE9 (D6), PF13 (D7), PF15 (D2) | Carrier S, D, E through columns 11, 10 and 9 (wires V18, V19, V12) |

## First test

Stick a small tape flag on the motor shaft to see each turn.

| What you see | Meaning or fix |
|---|---|
| Exactly one turn forward in about 4 s, a pause, one turn back, a rest of 2 s, and again | **Pass.** The tape flag stops at the same place every time |
| Nothing moves | Check 12 V between the carrier Vin and GND pins, 3.3 V on the carrier 5V pin, 0 V on column 9 (EN) while it should move, and that Vref is not 0. Then checks 4 and 5 again |
| It makes half a turn, or two turns | The switches are wrong: 1 OFF, 2 OFF, 3 ON gives 3200 steps per turn |
| It buzzes or shakes but does not turn | The coil pairs are mixed: measure the pairs again. Each pair goes on A1 and A2, or on B1 and B2 |
| It turns the wrong way | Swap the two wires of one coil, or flip DIR in the code |
| It skips or grinds | Raise Vref a little (never above 0.75 V) or raise `HALF_PERIOD_US` |
| Motor or driver chip too hot to touch | Lower Vref, and stick the heatsink on the chip |

Write the result in a step 3 test file for this part, copied from the [test template](../../03_component_tests/test_template.md).
