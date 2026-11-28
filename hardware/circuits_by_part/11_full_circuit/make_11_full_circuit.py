"""Draw hardware/circuits_by_part/11_full_circuit/11_full_circuit.svg (Fritzing style).

Every part at the same holes as in its own picture (circuits 1 to 5 and 7 to 10). The parts outside the
board are moved around it so nothing overlaps, and each wire to the Nucleo is drawn as a short wire with a
tag naming the Nucleo pin; the same tag sits next to that pin on the Nucleo, and the table lists them all.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, BLUE, BLUEGREY, BROWN, CARRIER_MOTOR, CARRIER_PINS, CN7, CN8, CN10, DARKPURPLE,  # noqa: E402
                    GREEN, GREY, LIGHTGREEN,
                    LIGHTPURPLE, ORANGE, PINK, PURPLE, RED, ROW, WHITE, YELLOW, Drawing, X)

DY = 440  # the whole drawing is shifted down to leave room above the board
d = Drawing(2000, 1840)
a, t = d.add, d.text
d.title("PART 11: FULL CIRCUIT",
        "Every part on one 830 point breadboard, at the same holes as in its own picture. Tags like PE9 are wires to that Nucleo pin.")
a(f'<g transform="translate(0,{DY})">')
d.nucleo([])
# the pin tags fill the space of the board name: move the name under the STM32 chip
a('<rect x="127" y="429" width="128" height="21" fill="#f6f6f3"/>')
t(190, 680, "NUCLEO-F439ZI", 13, "#1a237e", "middle", "bold")
d.breadboard()


def tag(col, row, text, colour, side="left"):
    """Short wire from a hole to a tag naming the Nucleo pin it goes to."""
    x, y = X(col), ROW[row]
    w = 8 + 5.4 * len(text)
    if side == "left":
        x1, x2, x0 = x - 12 - w, x - 12, x - 12
    else:
        x1, x2, x0 = x + 12, x + 12 + w, x + 12
    d.wire(f"M{x},{y} L{x0},{y}", colour, [(x, y)], width=3.5)
    a(f'<rect x="{x1}" y="{y - 6.5}" width="{w}" height="13" rx="6" fill="#ffffff" stroke="{colour[1]}" stroke-width="1.6"/>')
    t((x1 + x2) / 2, y + 3.2, text, 8.5, colour[1], "middle", "bold")


def ntag(pin, text, colour, ty, side="left"):
    """Ring on a Nucleo pin and its tag (left of the inner headers, or right of CN8)."""
    x, y = pin
    w = 8 + 5.0 * len(text)
    a(f'<circle cx="{x}" cy="{y}" r="6.5" fill="none" stroke="{colour[1]}" stroke-width="2"/>')
    if side == "left":
        x1, x2 = 254 - w, 254
        a(f'<line x1="{x2}" y1="{ty}" x2="{x - 6}" y2="{y}" stroke="{colour[1]}" stroke-width="1.2"/>')
    else:
        x1, x2 = 128, 128 + w
        a(f'<line x1="{x1}" y1="{ty}" x2="{x + 6}" y2="{y}" stroke="{colour[1]}" stroke-width="1.2"/>')
    a(f'<rect x="{x1}" y="{ty - 6}" width="{w}" height="12" rx="5" fill="#ffffff" stroke="{colour[1]}" stroke-width="1.4"/>')
    t((x1 + x2) / 2, ty + 3, text, 8, colour[1], "middle", "bold")


# ---------------------------------------------------------------- circuit 7: power entry (12 V and the XL4015)
d.dc_jack()
t(490, 134, "DC jack", 9, "#fff", "middle", "bold")
d.wire(f"M534,186 C534,250 {X(3)},262 {X(3)},290 L{X(3)},{ROW['top-']}", BLACK, [(X(3), ROW['top-'])])
vx, vy = CARRIER_PINS["Vin"]  # V1: 12 V straight from the jack to the carrier, never into the breadboard
d.wire(f"M564,186 L564,196 C564,202 568,204 574,204 L{vx - 10},204 C{vx - 4},204 {vx},200 {vx},194 L{vx},{vy}", RED, [])
# XL4015 standing above the adapter: IN at the bottom, OUT at the top
a('<rect x="380" y="-190" width="80" height="160" rx="5" fill="#1e3a8a" stroke="#0f1f4d" stroke-width="2"/>')
a('<circle cx="420" cy="-128" r="22" fill="#b87333" stroke="#8d5524" stroke-width="3"/>')
a('<circle cx="420" cy="-128" r="8" fill="#37474f"/>')
a('<rect x="392" y="-94" width="34" height="18" rx="2" fill="#1e88e5" stroke="#0d47a1"/>')
a('<circle cx="402" cy="-85" r="4" fill="#d4af37" stroke="#8d6e00"/>')
t(416, -82, "5V", 7, "#fff", "middle", "bold")
for x, y, lab in ((400, -36, "IN−"), (430, -36, "IN+"), (400, -184, "OUT+"), (430, -184, "OUT−")):
    a(f'<circle cx="{x}" cy="{y}" r="6" fill="#d4af37" stroke="#8d6e00"/>')
    t(x, y + (-10 if y > -100 else 18), lab, 6.5, "#fff", "middle", "bold")
t(370, -150, "XL4015", 13, "#c62828", "end", "bold")
t(370, -134, "12 V in, 5.0 V out", 11, "#555", "end")
t(370, -118, "set to 5.0 V before", 11, "#c62828", "end", "bold")
t(370, -103, "wiring OUT", 11, "#c62828", "end", "bold")
d.wire("M534,142 L534,88 C534,82 530,80 524,80 L410,80 C404,80 400,76 400,70 L400,-36", BLACK, [(400, -36)])
d.wire("M564,142 L564,74 C564,68 560,66 554,66 L440,66 C434,66 430,62 430,56 L430,-36", RED, [(430, -36)])
d.wire(f"M400,-184 L400,-215 C400,-221 404,-225 410,-225 L730,-225 C736,-225 740,-221 740,-215 L740,{ROW['top+']}",
       ORANGE, [(400, -184), (740, ROW['top+'])])
d.wire(f"M430,-184 L430,-200 C430,-206 434,-210 440,-210 L710,-210 C716,-210 720,-206 720,-200 L720,{ROW['top-']}",
       BLACK, [(430, -184), (720, ROW['top-'])])
d.ground_link(1)
d.three_volt_feed(2)
d.ground_feed(3)

# ---------------------------------------------------------------- circuit 1: DRV8825 on its carrier, and motor
d.carrier()
gx, gy = CARRIER_PINS["GND"]
d.wire(f"M{gx},{gy} L{gx},{ROW['top-']}", BLACK, [(gx, ROW['top-'])])
for name, col, colour in (("5V", 8, YELLOW), ("E", 9, BLUEGREY), ("D", 10, BROWN), ("S", 11, GREY)):
    x, y = CARRIER_PINS[name]
    d.wire(f"M{x},{y} L{X(col)},{ROW['e']}", colour, [(X(col), ROW['e'])])
d.wire(f"M{X(8)},{ROW['a']} L{X(8)},{ROW['bot+']}", YELLOW, [(X(8), ROW['a']), (X(8), ROW['bot+'])])
d.pull_up_10k(9)
# motor above the carrier, its cable straight down into the carrier motor connector
a('<rect x="570" y="-358" width="120" height="96" rx="10" fill="#bdbdbd" stroke="#8a8a8a" stroke-width="2"/>')
for cx, cy in ((584, -344), (676, -344), (584, -276), (676, -276)):
    a(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#757575"/>')
a('<circle cx="630" cy="-310" r="22" fill="#9e9e9e" stroke="#757575" stroke-width="2"/>')
a('<circle cx="630" cy="-310" r="7" fill="#e0e0e0" stroke="#757575"/>')
a('<rect x="588" y="-262" width="84" height="14" rx="2" fill="#f5f5f5" stroke="#9e9e9e"/>')
t(560, -318, "NEMA 17 motor", 13, "#c62828", "end", "bold")
t(560, -302, "DRV8825 on its carrier below", 11, "#555", "end")
for name, colour in (("2B", BLUE), ("2A", RED), ("1A", BLACK), ("1B", GREEN)):
    x, y = CARRIER_MOTOR[name]
    d.wire(f"M{x},-248 L{x},{y}", colour, [], width=3.5)

# ---------------------------------------------------------------- circuit 2: HX711 and load cell
x1, x2 = X(15) - 12, X(18) + 12
a(f'<rect x="{x1}" y="546" width="{x2 - x1}" height="144" rx="4" fill="#1b6e3a" stroke="#0f4a26" stroke-width="2"/>')
for k, lab in enumerate(["VCC", "DAT", "CLK", "GND"]):
    x = X(15 + k)
    a(f'<rect x="{x - 4}" y="{ROW["a"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 574, lab, 8, "#fff", "middle", "bold")
hx = (x1 + x2) / 2
a(f'<rect x="{hx - 18}" y="598" width="36" height="28" rx="2" fill="#1a1a1a"/>')
t(hx, 616, "HX711", 8, "#ddd", "middle", "bold")
pin6 = [x1 + 10 + 15 * k for k in range(6)]
for x, lab in zip(pin6, ["E+", "E−", "A−", "A+", "B−", "B+"]):
    a(f'<rect x="{x - 3.5}" y="674" width="7" height="8" fill="#d4af37"/>')
    t(x, 668, lab, 7, "#fff", "middle", "bold")
t(x1 - 8, 700, "HX711", 12, "#1b6e3a", "end", "bold")
d.wire(f"M{X(15)},{ROW['b']} C{X(14) + 2},{ROW['b']} {X(14)},556 {X(14)},{ROW['bot+']}", YELLOW,
       [(X(15), ROW['b']), (X(14), ROW['bot+'])])
d.wire(f"M{X(18)},{ROW['b']} C{X(20) - 5},{ROW['b']} {X(20)},560 {X(20)},{ROW['bot-']}", BLACK,
       [(X(18), ROW['b']), (X(20), ROW['bot-'])])
a('<rect x="560" y="770" width="200" height="46" rx="3" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
for x in (580, 602, 718, 740):
    a(f'<circle cx="{x}" cy="793" r="6" fill="#ffffff" stroke="#90a4ae" stroke-width="1.5"/>')
t(660, 798, "5 kg load cell", 11, "#455a64", "middle", "bold")
for y, xpin, col in ((778, pin6[0], RED), (786, pin6[1], BLACK), (794, pin6[2], WHITE), (802, pin6[3], GREEN)):
    d.wire(f"M760,{y} L{xpin - 8},{y} Q{xpin},{y} {xpin},{y - 8} L{xpin},682", col, [(xpin, 682)], width=3)

# ---------------------------------------------------------------- circuit 3: HC-SR04 and its divider
px = [X(24), X(25), X(26), X(27)]
cx = (px[0] + px[3]) / 2
a(f'<rect x="{cx - 100}" y="96" width="200" height="140" rx="6" fill="#1565c0" stroke="#0d47a1" stroke-width="2"/>')
for ox in (-52, 52):
    a(f'<circle cx="{cx + ox}" cy="160" r="40" fill="#cfd8dc" stroke="#90a4ae" stroke-width="3"/>')
    a(f'<circle cx="{cx + ox}" cy="160" r="30" fill="#455a64"/>')
    for r in (9, 18, 26):
        a(f'<circle cx="{cx + ox}" cy="160" r="{r}" fill="none" stroke="#607d8b" stroke-width="1.5"/>')
for x, lab in zip(px, ["VCC", "Trig", "Echo", "Gnd"]):
    a(f'<rect x="{x - 3}" y="236" width="6" height="12" fill="#d4af37"/>')
    t(x, 230, lab, 8, "#fff", "middle", "bold")
t(cx, 84, "HC-SR04 ultrasonic sensor", 13, "#c62828", "middle", "bold")
d.wire(f"M{px[0]},248 L{px[0]},{ROW['top+']}", ORANGE, [(px[0], ROW['top+'])])
d.wire(f"M{px[1]},248 L{px[1]},{ROW['j']}", GREY, [(px[1], ROW['j'])])
d.wire(f"M{px[2]},248 L{px[2]},{ROW['j']}", BLUEGREY, [(px[2], ROW['j'])])
d.wire(f"M{px[3]},248 L{px[3]},{ROW['top-']}", BLACK, [(px[3], ROW['top-'])])


def resistor_v(x, y1, y2, bands):
    a(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#9e9e9e" stroke-width="2.5"/>')
    top, h = y1 + 8, (y2 - y1) - 16
    a(f'<rect x="{x - 7}" y="{top}" width="14" height="{h}" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
    for k, c in enumerate(bands):
        a(f'<rect x="{x - 7}" y="{top + 4 + k * 5}" width="14" height="3" fill="{c}"/>')
    for y in (y1, y2):
        a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')


def resistor_h(x1, x2, y, bands):
    a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#9e9e9e" stroke-width="2.5"/>')
    a(f'<rect x="{x1 + 11}" y="{y - 7}" width="{x2 - x1 - 22}" height="14" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
    for k, c in enumerate(bands):
        a(f'<rect x="{x1 + 16 + k * 6}" y="{y - 7}" width="3" height="14" fill="{c}"/>')
    a(f'<rect x="{x2 - 17}" y="{y - 7}" width="3" height="14" fill="#c9a227"/>')
    for x in (x1, x2):
        a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')


resistor_v(X(26), ROW["f"], ROW["e"], ["#8d4e2b", "#111", "#e53935"])
resistor_v(X(26), ROW["a"], ROW["bot-"], ["#e53935", "#111", "#e53935"])

# ---------------------------------------------------------------- circuit 4: MAX98357A and speaker
ax1, ax2 = X(15) - 14, X(21) + 14
acx = (ax1 + ax2) / 2
a(f'<rect x="{ax1}" y="196" width="{ax2 - ax1}" height="168" rx="5" fill="#263238" stroke="#11171a" stroke-width="2"/>')
a(f'<rect x="{acx - 28}" y="202" width="56" height="30" rx="3" fill="#2e7d32"/>')
for x in (acx - 14, acx + 14):
    a(f'<circle cx="{x}" cy="217" r="8" fill="#bdbdbd" stroke="#757575"/>')
    a(f'<line x1="{x - 5}" y1="217" x2="{x + 5}" y2="217" stroke="#616161" stroke-width="2"/>')
t(acx - 14, 250, "+", 13, "#fff", "middle", "bold")
t(acx + 14, 250, "−", 13, "#fff", "middle", "bold")
a(f'<rect x="{acx - 16}" y="268" width="32" height="32" rx="2" fill="#111"/>')
t(acx, 318, "MAX98357A", 10, "#cfd8dc", "middle", "bold")
for k, lab in enumerate(["LRC", "BCLK", "DIN", "GAIN", "SD", "GND", "Vin"]):
    x = X(15 + k)
    a(f'<rect x="{x - 4}" y="{ROW["j"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 342, lab, 6.3 if len(lab) > 3 else 7.5, "#fff", "middle", "bold")
sx, sy = acx, -70
a(f'<circle cx="{sx}" cy="{sy}" r="56" fill="#37474f"/>')
for r, c in ((47, "#90a4ae"), (35, "#78909c"), (23, "#607d8b"), (12, "#455a64")):
    a(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="{c}"/>')
a(f'<rect x="{acx - 18}" y="-16" width="8" height="8" fill="#c62828"/>')
a(f'<rect x="{acx + 10}" y="-16" width="8" height="8" fill="#212121"/>')
d.wire(f"M{acx - 14},209 L{acx - 14},-8", RED, [], width=3)
d.wire(f"M{acx + 14},209 L{acx + 14},-8", BLACK, [], width=3)
t(sx + 64, -100, "Speaker", 13, "#c62828", weight="bold")
t(sx + 64, -84, "4 or 8 Ω, about 3 W,", 11, "#555")
t(sx + 64, -68, "both wires to the amplifier,", 11, "#555")
t(sx + 64, -52, "never to GND", 11, "#c62828", weight="bold")
d.wire(f"M{X(20)},{ROW['i']} L{X(22) - 12},{ROW['i']} C{X(22) - 4},{ROW['i']} {X(22)},{ROW['i'] - 6} {X(22)},{ROW['i'] - 16} "
       f"L{X(22)},{ROW['top-']}", BLACK, [(X(20), ROW['i']), (X(22), ROW['top-'])])
d.wire(f"M{X(21)},{ROW['h']} L{X(23) - 12},{ROW['h']} C{X(23) - 4},{ROW['h']} {X(23)},{ROW['h'] - 6} {X(23)},{ROW['h'] - 16} "
       f"L{X(23)},{ROW['top+']}", ORANGE, [(X(21), ROW['h']), (X(23), ROW['top+'])])

# ---------------------------------------------------------------- circuit 5: ESP32-CAM (higher up, long wires)
pins, _ = d.esp32_cam(X(30), -330, used_bottom={"IO14", "IO15", "GND", "5V"})
ex = {name: x for name, (x, y) in pins.items()}
ey = pins["5V"][1]
t(X(30) - 188, -300, "ESP32-CAM camera board", 14, "#c62828", "end", "bold")
t(X(30) - 188, -282, "camera facing the bowl,", 11, "#555", "end")
t(X(30) - 188, -266, "4 female to male wires", 11, "#555", "end")
d.wire(f"M{ex['5V']},{ey} L{ex['5V']},{ROW['top+']}", ORANGE, [(ex['5V'], ROW['top+'])])
d.wire(f"M{ex['GND']},{ey} L{ex['GND']},{ROW['top-']}", BLACK, [(ex['GND'], ROW['top-'])])
d.wire(f"M{ex['IO15']},{ey} L{ex['IO15']},{ROW['j']}", GREEN, [(ex['IO15'], ROW['j'])])
d.wire(f"M{ex['IO14']},{ey} L{ex['IO14']},{ROW['j']}", LIGHTGREEN, [(ex['IO14'], ROW['j'])])
c = X(38)
a(f'<line x1="{c}" y1="280" x2="{c}" y2="{ROW["top+"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<path d="M{c + 12},280 L{c + 12},302 L{c},{ROW["top-"]}" fill="none" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<rect x="{c - 6}" y="250" width="24" height="32" rx="5" fill="#1f2f74"/>')
a(f'<rect x="{c + 10}" y="250" width="8" height="32" rx="3" fill="#9fb0e8"/>')
a(f'<ellipse cx="{c + 6}" cy="251" rx="12" ry="3.5" fill="#3a4c9a"/>')
for y in (ROW["top+"], ROW["top-"]):
    a(f'<circle cx="{c}" cy="{y}" r="3.5" fill="#757575"/>')
resistor_h(X(29), X(32), ROW["i"], ["#8d4e2b", "#111", "#e53935"])

# ---------------------------------------------------------------- circuit 8: DS3231 and VL53L0X on the I2C bus
x1, x2 = X(29) - 12, X(34) + 12
a(f'<rect x="{x1}" y="546" width="{x2 - x1}" height="154" rx="4" fill="#1565c0" stroke="#0d47a1" stroke-width="2"/>')
for k, lab in enumerate(["32K", "SQW", "SCL", "SDA", "VCC", "GND"]):
    x = X(29 + k)
    a(f'<rect x="{x - 4}" y="{ROW["a"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 574, lab, 7, "#fff" if lab in ("SCL", "SDA", "VCC", "GND") else "#90caf9", "middle", "bold")
dcx = (x1 + x2) / 2
a(f'<rect x="{dcx - 26}" y="590" width="52" height="30" rx="2" fill="#1a1a1a"/>')
t(dcx, 609, "DS3231", 9, "#ddd", "middle", "bold")
a(f'<circle cx="{dcx}" cy="664" r="22" fill="none" stroke="#bbdefb" stroke-width="1.5" stroke-dasharray="4 3"/>')
t(dcx, 667, "CR2032", 7, "#e3f2fd", "middle", "bold")
t(dcx, 716, "DS3231 clock", 12, "#c62828", "middle", "bold")
d.wire(f"M{X(34)},{ROW['b']} L{X(35) - 8},{ROW['b']} C{X(35) - 2},{ROW['b']} {X(35)},{ROW['b'] + 4} {X(35)},{ROW['b'] + 10} "
       f"L{X(35)},{ROW['bot-']}", BLACK, [(X(34), ROW['b']), (X(35), ROW['bot-'])])
d.wire(f"M{X(33)},{ROW['c']} L{X(36) - 8},{ROW['c']} C{X(36) - 2},{ROW['c']} {X(36)},{ROW['c'] + 4} {X(36)},{ROW['c'] + 10} "
       f"L{X(36)},{ROW['bot+']}", YELLOW, [(X(33), ROW['c']), (X(36), ROW['bot+'])])
vp = {"VIN": X(24), "GND": X(25), "SCL": X(26), "SDA": X(27)}
a(f'<rect x="{X(24) - 16}" y="740" width="{X(27) - X(24) + 32}" height="54" rx="4" fill="#6a1b9a" stroke="#4a148c" stroke-width="2"/>')
for name, x in vp.items():
    a(f'<rect x="{x - 3}" y="728" width="6" height="12" fill="#d4af37"/>')
    t(x, 754, name, 5.2 if len(name) > 3 else 7, "#fff" if name in ("VIN", "GND", "SCL", "SDA") else "#ce93d8", "middle", "bold")
vcx = (X(24) + X(27)) / 2
a(f'<rect x="{vcx - 16}" y="762" width="32" height="20" rx="2" fill="#111"/>')
for ox in (-7, 7):
    a(f'<circle cx="{vcx + ox}" cy="772" r="4" fill="#ffb300" fill-opacity="0.8"/>')
t(X(29) + 30, 758, "VL53L0X tank sensor", 12, "#c62828", weight="bold")
t(X(29) + 30, 774, "in the tank lid, facing the food", 11, "#555")
d.wire(f"M{vp['VIN']},728 L{vp['VIN']},{ROW['bot+']}", YELLOW, [(vp['VIN'], ROW['bot+'])])
d.wire(f"M{vp['GND']},728 L{vp['GND']},{ROW['bot-']}", BLACK, [(vp['GND'], ROW['bot-'])])
for name, row, colour, end in (("SCL", "c", WHITE, X(31)), ("SDA", "b", BLUE, X(32))):
    x = vp[name]
    d.wire(f"M{x},728 C{x},718 {x + 10},718 {x + 10},708 L{x + 10},{ROW[row] + 10} C{x + 10},{ROW[row] + 4} {x + 14},{ROW[row]} "
           f"{x + 20},{ROW[row]} L{end},{ROW[row]}", colour, [(end, ROW[row])])
t(X(31), 459, "SCL", 7.5, "#5f5f5f", "middle", "bold")
t(X(32), 459, "SDA", 7.5, "#0d47a1", "middle", "bold")

# ---------------------------------------------------------------- circuit 9: microSD module
mx1, mx2 = X(42) - 44, X(47) + 44
mcx = (mx1 + mx2) / 2
a(f'<rect x="{mx1}" y="112" width="{mx2 - mx1}" height="252" rx="6" fill="#0d47a1" stroke="#082f6b" stroke-width="2"/>')
a(f'<rect x="{mcx - 52}" y="122" width="104" height="92" rx="4" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
a(f'<rect x="{mcx - 40}" y="128" width="80" height="62" rx="3" fill="#263238"/>')
t(mcx, 162, "microSD", 11, "#eceff1", "middle", "bold")
a(f'<rect x="{mcx - 46}" y="232" width="34" height="22" rx="2" fill="#111"/>')
a(f'<rect x="{mcx + 6}" y="228" width="40" height="30" rx="2" fill="#111"/>')
for k, lab in enumerate(["CS", "SCK", "MOSI", "MISO", "VCC", "GND"]):
    x = X(42 + k)
    a(f'<rect x="{x - 4}" y="{ROW["j"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 342, lab, 6.3 if len(lab) > 3 else 7.5, "#fff", "middle", "bold")
t(mcx, 100, "microSD card module", 12, "#c62828", "middle", "bold")
d.wire(f"M{X(47)},{ROW['i']} L{X(51) - 12},{ROW['i']} C{X(51) - 4},{ROW['i']} {X(51)},{ROW['i'] - 6} {X(51)},{ROW['i'] - 16} "
       f"L{X(51)},{ROW['top-']}", BLACK, [(X(47), ROW['i']), (X(51), ROW['top-'])])
d.wire(f"M{X(46)},{ROW['h']} L{X(52) - 12},{ROW['h']} C{X(52) - 4},{ROW['h']} {X(52)},{ROW['h'] - 6} {X(52)},{ROW['h'] - 16} "
       f"L{X(52)},{ROW['top+']}", ORANGE, [(X(46), ROW['h']), (X(52), ROW['top+'])])

# ---------------------------------------------------------------- circuit 10: button and LED
resistor_h(X(44), X(47), ROW["c"], ["#ef6c00", "#ef6c00", "#8d4e2b"])
lx = X(47)
a(f'<line x1="{lx}" y1="{ROW["a"]}" x2="{lx}" y2="{ROW["bot-"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<circle cx="{lx}" cy="578" r="10" fill="#e53935" stroke="#b71c1c" stroke-width="2"/>')
a(f'<circle cx="{lx - 3}" cy="575" r="3" fill="#ffcdd2"/>')
a(f'<line x1="{lx - 10}" y1="586" x2="{lx + 10}" y2="586" stroke="#b71c1c" stroke-width="2"/>')
for yy in (ROW["a"], ROW["bot-"]):
    a(f'<circle cx="{lx}" cy="{yy}" r="3.5" fill="#757575"/>')
bx, by = X(51), 760
a(f'<rect x="{bx - 34}" y="{by - 18}" width="68" height="36" rx="6" fill="#455a64" stroke="#263238" stroke-width="2"/>')
a(f'<circle cx="{bx}" cy="{by}" r="14" fill="#e53935" stroke="#b71c1c" stroke-width="2"/>')
for ox in (-10, 10):
    a(f'<rect x="{bx + ox - 3}" y="{by - 30}" width="6" height="12" fill="#bdbdbd" stroke="#757575"/>')
t(bx + 46, by - 2, "Push button", 12, "#c62828", weight="bold")
t(bx + 46, by + 14, "on the feeder body", 11, "#555")
d.wire(f"M{bx - 10},{by - 30} L{bx - 10},{ROW['c'] + 10} C{bx - 10},{ROW['c'] + 4} {bx - 14},{ROW['c']} {bx - 20},{ROW['c']} "
       f"L{X(49)},{ROW['c']}", GREY, [(X(49), ROW['c'])], width=3.5)
d.wire(f"M{bx + 10},{by - 30} L{bx + 10},{ROW['bot-'] + 30} C{bx + 10},{ROW['bot-'] + 12} {X(52)},{ROW['bot-'] + 12} "
       f"{X(52)},{ROW['bot-']}", BLACK, [(X(52), ROW['bot-'])], width=3.5)

# ---------------------------------------------------------------- wires to the Nucleo, drawn as tags
TAGS = [  # (column, row, side, pin text, colour, Nucleo pin position, Nucleo tag text, table text)
    (9, "b", "left", "PF15", BLUEGREY, CN10(12), "PF15 EN", "PF15 · D2 · CN10 pin 12: driver EN, column 9 b"),
    (11, "c", "left", "PE9", GREY, CN10(4), "PE9 STEP", "PE9 · D6 · CN10 pin 4: driver STEP, column 11 c"),
    (10, "d", "left", "PF13", BROWN, CN10(2), "PF13 DIR", "PF13 · D7 · CN10 pin 2: driver DIR, column 10 d"),
    (16, "d", "left", "PF14", BROWN, CN10(8), "PF14 DAT", "PF14 · D4 · CN10 pin 8: HX711 DAT, column 16 d"),
    (17, "c", "left", "PE13", GREY, CN10(10), "PE13 HX CLK", "PE13 · D3 · CN10 pin 10: HX711 CLK, column 17 c"),
    (15, "g", "left", "PA4", LIGHTPURPLE, CN7(17), "PA4 LRC", "PA4 · D24 · CN7 pin 17: amplifier LRC, column 15 g"),
    (16, "i", "left", "PC10", PURPLE, CN8(6), "PC10 BCLK", "PC10 · D45 · CN8 pin 6: amplifier BCLK, column 16 i"),
    (17, "h", "left", "PC12", DARKPURPLE, CN8(10), "PC12 DIN", "PC12 · D47 · CN8 pin 10: amplifier DIN, column 17 h"),
    (25, "h", "right", "PD14", GREY, CN7(16), "PD14 TRIG", "PD14 · D10 · CN7 pin 16: HC-SR04 Trig, column 25 h"),
    (26, "c", "left", "PD15", BROWN, CN7(18), "PD15 ECHO", "PD15 · D9 · CN7 pin 18: Echo after the divider, column 26 c"),
    (29, "h", "right", "PC6", LIGHTGREEN, CN7(1), "PC6 TX", "PC6 · D16 · CN7 pin 1: to ESP32-CAM RX via 1 kΩ, column 29 h"),
    (33, "g", "right", "PC7", GREEN, CN7(11), "PC7 RX", "PC7 · D21 · CN7 pin 11: from ESP32-CAM TX, column 33 g"),
    (31, "d", "left", "PB8", WHITE, CN7(2), "PB8 SCL", "PB8 · D15 · CN7 pin 2: I2C SCL bus, column 31 d"),
    (32, "e", "left", "PB9", BLUE, CN7(4), "PB9 SDA", "PB9 · D14 · CN7 pin 4: I2C SDA bus, column 32 e"),
    (42, "f", "left", "PE11", PINK, CN10(6), "PE11 SD CS", "PE11 · D5 · CN10 pin 6: microSD CS, column 42 f"),
    (43, "g", "left", "PA5", PURPLE, CN7(10), "PA5 SD SCK", "PA5 · D13 · CN7 pin 10: microSD SCK, column 43 g"),
    (44, "h", "left", "PB5", DARKPURPLE, CN7(13), "PB5 MOSI", "PB5 · D22 · CN7 pin 13: microSD MOSI, column 44 h"),
    (45, "i", "left", "PA6", LIGHTPURPLE, CN7(12), "PA6 MISO", "PA6 · D12 · CN7 pin 12: microSD MISO, column 45 i"),
    (44, "d", "left", "PG14", BROWN, CN10(14), "PG14 LED", "PG14 · D1 · CN10 pin 14: LED through 330 Ω, column 44 d"),
    (49, "e", "left", "PF12", GREY, CN7(20), "PF12 BUTTON", "PF12 · D8 · CN7 pin 20: button, column 49 e"),
]
for col, row, side, text, colour, *_ in TAGS:
    tag(col, row, text, colour, side)

# Nucleo side: tags left of CN7 and CN10 (in pin order), right of CN8
left = [(pin, ntext, colour) for col, row, side, text, colour, pin, ntext, _ in TAGS if pin[0] > 200]
left.append((CN10(5), "GND (R3)", BLACK))
left.sort(key=lambda p: (p[0][1], p[0][0]))
for i, (pin, ntext, colour) in enumerate(left):
    ntag(pin, ntext, colour, 292 + i * 13.8)
right = [(pin, ntext, colour) for col, row, side, text, colour, pin, ntext, _ in TAGS if pin[0] < 200]
right.append((CN8(7), "3V3 (R2)", YELLOW))
right.sort(key=lambda p: p[0][1])
for i, (pin, ntext, colour) in enumerate(right):
    ntag(pin, ntext, colour, 326 + i * 15, "right")

d.zones("all", 880)

# ---------------------------------------------------------------- notes
d.notes_box(40, 918, 1920, 236)
t(60, 946, "NUCLEO PINS: each tag on the board is a wire from that hole to this pin", 14, "#c62828", weight="bold")
rows = [(colour, table) for col, row, side, text, colour, pin, ntext, table in TAGS]
for i, (colour, table) in enumerate(rows):
    cx0, cy0 = 60 + (i // 7) * 640, 972 + (i % 7) * 25
    a(f'<line x1="{cx0 + 2}" y1="{cy0 - 4}" x2="{cx0 + 34}" y2="{cy0 - 4}" stroke="{colour[1]}" stroke-width="7" stroke-linecap="round"/>')
    a(f'<line x1="{cx0 + 2}" y1="{cy0 - 4}" x2="{cx0 + 34}" y2="{cy0 - 4}" stroke="{colour[0]}" stroke-width="4.5" stroke-linecap="round"/>')
    t(cx0 + 44, cy0, table, 11.5)
t(1340, 1122, "Power wires drawn in full: 3V3 (R2), GND (R3), both GND rails joined (R4).", 11.5, "#555")

d.notes_box(40, 1170, 1920, 196)
t(60, 1198, "HOW TO READ IT", 14, "#c62828", weight="bold")
d.lines(60, 1222, ["1. A dot with a white ring is a wire end in that hole.",
                   "2. A tag such as PE9 at a hole: a wire from that hole to that Nucleo pin.",
                   "3. Parts outside the board join it with female to male wires.",
                   "4. Every part has its own picture with all its wires drawn",
                   "in full: circuits 1 to 10 in circuits_by_part.",
                   "5. Rails: top + 5 V, bottom + 3.3 V, both − GND. 12 V only",
                   "from the jack to the carrier Vin and the XL4015 IN+."], 21)
t(560, 1198, "BUILD ORDER", 14, "#c62828", weight="bold")
d.lines(560, 1222, ["1. Rails R2, R3, R4. No R1: the XL4015 feeds the 5 V.",
                    "2. Power (circuit 7): set the XL4015 to 5.0 V first.",
                    "3. Driver and motor (1), scale (2): first milestone.",
                    "4. HC-SR04 (3), sound (4), ESP32-CAM (5).",
                    "5. Clock and tank sensor (8), microSD (9), button and LED (10).",
                    "6. Test each part before adding the next one.",
                    "7. Check every Nucleo pin label before plugging."], 21)
t(1100, 1198, "POWER ORDER", 14, "#c62828", weight="bold")
d.lines(1100, 1222, ["Tests: Nucleo on the laptop USB (JP3 on U5V).",
                     "On: USB, then the adapter. Off: adapter first.",
                     "Feeder alone: add P6 (top + rail to E5V,",
                     "circuit 7) and set JP3 on E5V; adapter only.",
                     "Never R1 and the XL4015 at the same time.",
                     "Never plug or unplug the motor with 12 V on."], 21)
t(1560, 1198, "NOT IN THIS PICTURE", 14, "#c62828", weight="bold")
d.lines(1560, 1222, ["DevKit for loading programs:",
                     "circuit 6 (bench setup).",
                     "Wire P6 for the feeder alone:",
                     "circuit 7.",
                     "Load cell mount: circuit 2.",
                     "Exact holes of every wire:",
                     "hardware/04_wiring_list.md."], 21)
a('</g>')
d.footer("Kibbly hardware · circuit 11 of the circuits by part · every wire in hardware/04_wiring_list.md (sections 4 to 12, rails in 4B and 13)")
d.save(sys.argv[1])
