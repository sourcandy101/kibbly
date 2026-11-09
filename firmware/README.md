# Firmware

All code that runs on the feeder: the STM32 and the ESP32 camera board.

Owners: Youssef Bousnina and Hedi Ennaifer. Hardware details (parts, wiring, tests) are in [`hardware/`](../hardware/).

## Layout

| Folder | Content | Tool |
|---|---|---|
| `stm32/` | Main feeder program for the NUCLEO-F439ZI: schedule, motor, scale, sensors, sound, SD card, button, failure handling | STM32CubeIDE (HAL drivers) |
| `esp32/` | Camera board program: WiFi, photos to the AI server, Firebase read and write, UART link to the STM32 | PlatformIO in VS Code (Arduino framework) |
| `tests/` | One small test program per component, used in hardware step 3 (for example `tests/hx711_load_cell/`) | Same tools as above |

## Rules

1. Each component gets its own driver file pair (for example `hx711.c` and `hx711.h`) so tests and the main program share the same code.
2. Build output (Debug, Release, .elf, .bin, .hex) is ignored by git.
3. English only, no dashes of any kind in comments or commit messages, snake_case file names.
