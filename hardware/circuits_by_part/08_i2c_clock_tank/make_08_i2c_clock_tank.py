"""Draw hardware/circuits_by_part/08_i2c_clock_tank/08_i2c_clock_tank.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import BLACK, BLUE, CN7, CN8, CN10, ROW, WHITE, YELLOW, Drawing, X  # noqa: E402

d = Drawing(1880, 1160)
a, t = d.add, d.text
d.title("PART 8: CLOCK AND TANK SENSOR ON THE I2C BUS",
        "Test setup for step 3. Only the laptop USB is needed: both parts run on 3.3 V from the Nucleo.")
d.nucleo([(CN7(2), "D15 · PB8 SCL (pin 2)", WHITE, "left"), (CN7(4), "D14 · PB9 SDA (pin 4)", BLUE, "left"),
          (CN10(5), "GND (pin 5)", BLACK, "left"), (CN8(7), "3V3 (CN8 pin 7)", YELLOW, "right")])
d.breadboard(used=(False, False, True, True))

# DS3231 module (ZS-042): 6 pins in row a, columns 29 to 34, board hanging over the bottom edge
x1, x2 = X(29) - 12, X(34) + 12
a(f'<rect x="{x1}" y="546" width="{x2 - x1}" height="154" rx="4" fill="#1565c0" stroke="#0d47a1" stroke-width="2"/>')
for k, lab in enumerate(["32K", "SQW", "SCL", "SDA", "VCC", "GND"]):
    x = X(29 + k)
    a(f'<rect x="{x - 4}" y="{ROW["a"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 574, lab, 7, "#fff" if lab in ("SCL", "SDA", "VCC", "GND") else "#90caf9", "middle", "bold")
cx = (x1 + x2) / 2
a(f'<rect x="{cx - 26}" y="590" width="52" height="30" rx="2" fill="#1a1a1a"/>')
t(cx, 609, "DS3231", 9, "#ddd", "middle", "bold")
a(f'<rect x="{cx + 14}" y="636" width="26" height="14" rx="1" fill="#1a1a1a"/>')
t(cx + 27, 646, "24C32", 6, "#bbb", "middle")
a(f'<circle cx="{cx - 18}" cy="664" r="24" fill="none" stroke="#bbdefb" stroke-width="1.5" stroke-dasharray="4 3"/>')
t(cx - 18, 662, "CR2032", 7, "#e3f2fd", "middle", "bold")
t(cx - 18, 672, "on the back", 6, "#e3f2fd", "middle")
t(X(37), 672, "DS3231 clock (ZS-042 board)", 13, "#c62828", weight="bold")
t(X(37), 688, "pins in row a, columns 29 to 34,", 11, "#555")
t(X(37), 703, "board over the bottom edge", 11, "#555")

# DS3231 power: GND (column 34) to the bottom − rail, column 35; VCC (column 33) to the bottom + rail, column 36
d.wire(f"M{X(34)},{ROW['b']} L{X(35) - 8},{ROW['b']} C{X(35) - 2},{ROW['b']} {X(35)},{ROW['b'] + 4} {X(35)},{ROW['b'] + 10} "
       f"L{X(35)},{ROW['bot-']}", BLACK, [(X(34), ROW['b']), (X(35), ROW['bot-'])])
d.wire(f"M{X(33)},{ROW['c']} L{X(36) - 8},{ROW['c']} C{X(36) - 2},{ROW['c']} {X(36)},{ROW['c'] + 4} {X(36)},{ROW['c'] + 10} "
       f"L{X(36)},{ROW['bot+']}", YELLOW, [(X(33), ROW['c']), (X(36), ROW['bot+'])])

# VL53L0X (GY-530) outside the board, below columns 24 to 29
pins = {"VIN": X(24), "GND": X(25), "SCL": X(26), "SDA": X(27), "GPIO1": X(28), "XSHUT": X(29)}
a(f'<rect x="{X(24) - 16}" y="740" width="{X(29) - X(24) + 32}" height="54" rx="4" fill="#6a1b9a" stroke="#4a148c" stroke-width="2"/>')
for name, x in pins.items():
    a(f'<rect x="{x - 3}" y="728" width="6" height="12" fill="#d4af37"/>')
    t(x, 754, name, 5.2 if len(name) > 3 else 7, "#fff" if name in ("VIN", "GND", "SCL", "SDA") else "#ce93d8", "middle", "bold")
sx = (X(24) + X(29)) / 2
a(f'<rect x="{sx - 16}" y="762" width="32" height="20" rx="2" fill="#111"/>')
for ox in (-7, 7):
    a(f'<circle cx="{sx + ox}" cy="772" r="4" fill="#ffb300" fill-opacity="0.8"/>')
t(X(24) - 28, 756, "VL53L0X tank sensor (GY-530)", 13, "#c62828", "end", "bold")
t(X(24) - 28, 772, "in the tank lid, facing the food,", 11, "#555", "end")
t(X(24) - 28, 788, "joined with 4 female to male wires", 11, "#555", "end")
t(sx, 812, "peel off the thin film on the sensor", 10, "#c62828", "middle", "bold")

# VL53L0X wires: power straight up to the bottom rails, SCL and SDA up between the columns into the bus columns
d.wire(f"M{pins['VIN']},728 L{pins['VIN']},{ROW['bot+']}", YELLOW, [(pins['VIN'], ROW['bot+'])])
d.wire(f"M{pins['GND']},728 L{pins['GND']},{ROW['bot-']}", BLACK, [(pins['GND'], ROW['bot-'])])
x = pins["SCL"]
d.wire(f"M{x},728 C{x},718 {x + 10},718 {x + 10},708 L{x + 10},{ROW['c'] + 10} C{x + 10},{ROW['c'] + 4} {x + 14},{ROW['c']} "
       f"{x + 20},{ROW['c']} L{X(31)},{ROW['c']}", WHITE, [(X(31), ROW['c'])])
x = pins["SDA"]
d.wire(f"M{x},728 C{x},718 {x + 10},718 {x + 10},708 L{x + 10},{ROW['b'] + 10} C{x + 10},{ROW['b'] + 4} {x + 14},{ROW['b']} "
       f"{x + 20},{ROW['b']} L{X(32)},{ROW['b']}", BLUE, [(X(32), ROW['b'])])

# Nucleo: SCL to column 31 (row d), SDA to column 32 (row e)
d.three_volt_feed(2)
d.ground_feed(3)
x, y = CN7(2)
d.wire(f"M{x},{y} C400,{y} 420,{ROW['d']} 480,{ROW['d']} L{X(31)},{ROW['d']}", WHITE, [(x, y), (X(31), ROW['d'])])
x, y = CN7(4)
d.wire(f"M{x},{y} C410,{y} 430,{ROW['e']} 480,{ROW['e']} L{X(32)},{ROW['e']}", BLUE, [(x, y), (X(32), ROW['e'])])
d.nucleo_labels()

# bus labels in the middle gap and a note in the free top half
t(X(31), 459, "SCL", 7.5, "#5f5f5f", "middle", "bold")
t(X(32), 459, "SDA", 7.5, "#0d47a1", "middle", "bold")
a(f'<rect x="{X(30) - 8}" y="{ROW["h"] - 14}" width="420" height="38" rx="4" fill="#ffffff" stroke="#90a4ae"/>')
t(X(30), ROW["h"] + 1, "I2C bus, bottom half: column 31 = SCL (white wires),", 11, "#37474f", weight="bold")
t(X(30), ROW["h"] + 17, "column 32 = SDA (blue wires). Every part plugs into these two.", 11, "#37474f")
d.zones(8, 880)

# notes
d.notes_box(640, 918, 1220, 220)
t(660, 946, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 970, [(YELLOW, "3.3 V: Nucleo 3V3 to the bottom + rail; VCC, VIN"), (BLACK, "GND"),
                         (WHITE, "SCL: Nucleo D15 · PB8, column 31"), (BLUE, "SDA: Nucleo D14 · PB9, column 32")])
d.lines(662, 1064, ["Not connected: DS3231 32K and SQW,", "VL53L0X GPIO1 and XSHUT"], 18)
t(1060, 946, "I2C SETTINGS", 14, "#c62828", weight="bold")
d.lines(1060, 970, ["I2C1 at 400 kHz",
                    "Addresses: VL53L0X 0x29, DS3231 0x68,",
                    "EEPROM 0x57 (on the clock board, not used)",
                    "Pull up resistors are on the modules: none added",
                    "Idle check: SDA and SCL both read 3.3 V"])
t(1460, 946, "TIPS", 14, "#c62828", weight="bold")
d.lines(1460, 970, ["1. Wire everything with the USB unplugged.",
                    "2. Both parts on 3.3 V, never on 5 V.",
                    "3. The coin cell keeps the time without power.",
                    "4. At 3.3 V the clock board needs no change.",
                    "5. Tank sensor: nothing in front but the food.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 8 of the circuits by part · wires I1 to I15 in hardware/04_wiring_list.md section 9, rails R2 and R3 in section 4B")
d.save(sys.argv[1])
