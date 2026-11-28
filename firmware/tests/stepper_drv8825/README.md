# Stepper motor test (circuit 1)

STM32 test program for the motor: the DRV8825 on its carrier board turns the NEMA 17 one turn forward, one turn back, rests, and repeats. Wiring and the checks before the first power on: [circuit 1](../../../hardware/circuits_by_part/01_stepper_motor_drv8825/README.md).

Written on 28 November 2026; not yet run on the board.

## Steps

1. **Wire circuit 1** and do its checks before wiring. Set Vref to 0.50 V (circuit 1, wiring order step 12).
2. **STM32CubeIDE:** File, New, STM32 Project, tab **Board Selector**, choose **NUCLEO-F439ZI**, name it `stepper_test`.
3. "Initialize all peripherals with their default Mode?": answer **No**.
4. Open `Core/Src/main.c` and **replace everything** in it with [main.c](main.c). No pin needs to be set in the .ioc: the file sets its own clock and pins.
5. Plug in the USB, then the adapter.
6. Click **Run** (the green play button). If it offers to update the ST-LINK firmware, accept.

Do not regenerate code from the .ioc in this project afterwards: that would overwrite `main.c`.

## What you should see

| What you see | Meaning |
|---|---|
| Blue LED (LD2) on, one turn forward in about 4 s, a pause, one turn back; then the green LED (LD1) blinks for 2 s, and again | **Pass** |
| Green LED blinks, but the motor does not move | The program runs: check the wiring, the switches and Vref (circuit 1, first test table) |
| No LED at all | The program does not run: check the Run result in CubeIDE and the USB cable |

| Setting in main.c | Value | Meaning |
|---|---|---|
| `STEPS_PER_TURN` | 3200 | 200 full steps times 16 microsteps (carrier switches 1 OFF, 2 OFF, 3 ON) |
| `HALF_PERIOD_US` | 625 | 800 steps per second, one turn in 4 s. A bigger value turns slower |
| STEP, DIR, EN | PE9 (D6), PF13 (D7), PF15 (D2) | EN low turns the motor on |
| Clock | 16 MHz, internal HSI | Enough for this test; the feeder program will run faster |
