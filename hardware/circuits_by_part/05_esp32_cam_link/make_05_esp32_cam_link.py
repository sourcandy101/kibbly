"""Draw hardware/circuits_by_part/05_esp32_cam_link/05_esp32_cam_link.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import BLACK, CN7, CN8, CN10, GREEN, LIGHTGREEN, ORANGE, ROW, Drawing, X  # noqa: E402

d = Drawing(1880, 960)
a, t = d.add, d.text
d.title("PART 5: ESP32-CAM LINK TO THE STM32 (UART)",
        "Test setup for step 3. Only the laptop USB is needed: the Nucleo 5V pin feeds the top + rail (5 V).")
d.nucleo([(CN8(9), "5V (CN8 pin 9)", ORANGE, "right"), (CN7(1), "D16 · PC6 TX (pin 1)", LIGHTGREEN, "left"),
          (CN7(11), "D21 · PC7 RX (pin 11)", GREEN, "left"), (CN10(5), "GND (pin 5)", BLACK, "left")])
d.breadboard(used=(True, True, True, False))

# ESP32-CAM outside the board. The pin row used here (5V ... IO4) sits over columns 30 to 37,
# the other row (3V3 ... GND, used only for flashing) along the top edge.
bottom = ["IO4", "IO2", "IO14", "IO15", "IO13", "IO12", "GND", "5V"]
top = ["GND", "U0T", "U0R", "VCC", "GND", "IO0", "IO16", "3V3"]
px = {name: X(30 + k) for k, name in enumerate(bottom)}
bx1, bx2 = X(30) - 176, X(37) + 16
a(f'<rect x="{bx1}" y="96" width="{bx2 - bx1}" height="140" rx="6" fill="#262626" stroke="#000" stroke-width="2"/>')
# ESP32-S module with its antenna, camera, flash LED
a(f'<rect x="{bx1 + 10}" y="108" width="128" height="116" rx="3" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
a(f'<path d="M{bx1 + 16},120 L{bx1 + 16},212 M{bx1 + 22},120 L{bx1 + 22},212 M{bx1 + 16},120 L{bx1 + 22},120 '
  f'M{bx1 + 16},212 L{bx1 + 22},212" stroke="#d4af37" stroke-width="2" fill="none"/>')
t(bx1 + 80, 162, "ESP32-S", 12, "#455a64", "middle", "bold")
t(bx1 + 80, 178, "WiFi module", 9, "#607d8b", "middle")
cx, cy = X(32) + 10, 168
a(f'<rect x="{cx - 30}" y="{cy - 30}" width="60" height="60" rx="4" fill="#3a3a3a" stroke="#111"/>')
a(f'<circle cx="{cx}" cy="{cy}" r="22" fill="#111" stroke="#555" stroke-width="2"/>')
a(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#1a237e"/>')
a(f'<circle cx="{cx - 4}" cy="{cy - 4}" r="4" fill="#90caf9"/>')
t(cx, cy + 44, "camera", 9, "#bbb", "middle")
a(f'<rect x="{X(36) - 6}" y="{cy - 8}" width="16" height="16" rx="2" fill="#fff9c4" stroke="#f9a825"/>')
t(X(36) + 2, cy + 22, "flash", 8, "#bbb", "middle")
for x, lab in zip([X(30 + k) for k in range(8)], top):
    a(f'<rect x="{x - 3}" y="98" width="6" height="8" fill="#d4af37"/>')
    t(x, 117, lab, 6.5, "#9e9e9e", "middle", "bold")
used = {"IO14", "IO15", "GND", "5V"}
for name, x in px.items():
    a(f'<rect x="{x - 3}" y="236" width="6" height="12" fill="#d4af37"/>')
    t(x, 230, name, 7 if len(name) > 3 else 8, "#fff" if name in used else "#8a8a8a", "middle", "bold")
t(bx1 - 12, 136, "ESP32-CAM camera board", 14, "#c62828", "end", "bold")
t(bx1 - 12, 154, "outside the board, camera facing the bowl,", 11, "#555", "end")
t(bx1 - 12, 170, "joined with 4 female to male wires", 11, "#555", "end")
t(bx1 - 12, 192, "The pin order can look reversed on your board:", 11, "#c62828", "end", "bold")
t(bx1 - 12, 208, "match every wire by its printed name", 11, "#c62828", "end")
t(bx2 + 14, 110, "Other row: U0T, U0R and IO0 stay free,", 10, "#555")
t(bx2 + 14, 124, "they load the programs (circuit 6)", 10, "#555")

# ESP32-CAM wires straight down: power to the top rails, TX and RX into columns 33 and 32
d.wire(f"M{px['5V']},248 L{px['5V']},{ROW['top+']}", ORANGE, [(px['5V'], ROW['top+'])])
d.wire(f"M{px['GND']},248 L{px['GND']},{ROW['top-']}", BLACK, [(px['GND'], ROW['top-'])])
d.wire(f"M{px['IO15']},248 L{px['IO15']},{ROW['j']}", GREEN, [(px['IO15'], ROW['j'])])
d.wire(f"M{px['IO14']},248 L{px['IO14']},{ROW['j']}", LIGHTGREEN, [(px['IO14'], ROW['j'])])

# 1000 uF capacitor across the top rails in column 38: long leg (+) in the top + rail, short leg in the top − rail
c = X(38)
a(f'<line x1="{c}" y1="280" x2="{c}" y2="{ROW["top+"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<path d="M{c + 12},280 L{c + 12},302 L{c},{ROW["top-"]}" fill="none" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<rect x="{c - 6}" y="250" width="24" height="32" rx="5" fill="#1f2f74"/>')
a(f'<rect x="{c + 10}" y="250" width="8" height="32" rx="3" fill="#9fb0e8"/>')
for y in (258, 266, 274):
    a(f'<line x1="{c + 12}" y1="{y}" x2="{c + 16}" y2="{y}" stroke="#1f2f74" stroke-width="2"/>')
a(f'<ellipse cx="{c + 6}" cy="251" rx="12" ry="3.5" fill="#3a4c9a"/>')
for y in (ROW["top+"], ROW["top-"]):
    a(f'<circle cx="{c}" cy="{y}" r="3.5" fill="#757575"/>')
a(f'<line x1="{bx2 + 16}" y1="226" x2="{c + 10}" y2="246" stroke="#1f2f74" stroke-width="1.2"/>')
t(bx2 + 14, 176, "1000 µF capacitor", 12, "#1f2f74", weight="bold")
t(bx2 + 14, 192, "long leg (+): top + rail, column 38", 10, "#1f2f74")
t(bx2 + 14, 206, "short leg (stripe): top − rail, column 38", 10, "#1f2f74")
t(bx2 + 14, 220, "stops restarts on WiFi current peaks", 10, "#1f2f74")

# 1 kohm resistor lying flat in row i, from column 29 (STM32 TX side) to column 32 (ESP32-CAM RX side)
x1, x2, y = X(29), X(32), ROW["i"]
a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<rect x="{x1 + 11}" y="{y - 7}" width="{x2 - x1 - 22}" height="14" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
for k, col in enumerate(["#8d4e2b", "#111", "#e53935"]):
    a(f'<rect x="{x1 + 16 + k * 6}" y="{y - 7}" width="3" height="14" fill="{col}"/>')
a(f'<rect x="{x2 - 17}" y="{y - 7}" width="3" height="14" fill="#c9a227"/>')
for x in (x1, x2):
    a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
a(f'<line x1="{(x1 + x2) / 2}" y1="{y + 8}" x2="{(x1 + x2) / 2}" y2="{y + 10}" stroke="#4e342e" stroke-width="1.2"/>')
a(f'<path d="M{(x1 + x2) / 2},{y + 10} L{X(40)},{y + 10}" stroke="#4e342e" stroke-width="1.2" stroke-dasharray="4 3" fill="none"/>')
a(f'<rect x="{X(40) + 2}" y="{y - 6}" width="284" height="32" rx="4" fill="#ffffff" stroke="#bcaaa4"/>')
t(X(40) + 8, y + 6, "1 kΩ in the STM32 TX line (columns 29 to 32):", 10, "#4e342e", weight="bold")
t(X(40) + 8, y + 20, "protects both pins, does not slow the messages", 10, "#4e342e")

# wires to the Nucleo and the rails
d.five_volt_feed(2)
d.ground_link(1)
d.ground_feed(3)
x, y = CN7(1)
d.wire(f"M{x},{y} C380,{y} 420,{ROW['h']} 480,{ROW['h']} L{X(29)},{ROW['h']}", LIGHTGREEN, [(x, y), (X(29), ROW['h'])])
x, y = CN7(11)
d.wire(f"M{x},{y} C380,{y} 420,{ROW['g']} 480,{ROW['g']} L{X(33)},{ROW['g']}", GREEN, [(x, y), (X(33), ROW['g'])])
d.nucleo_labels()
d.zones(5)

# notes
d.notes_box(640, 712, 1220, 230)
t(660, 740, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 764, [(ORANGE, "5 V: Nucleo 5V to the top + rail; ESP32-CAM 5V"), (BLACK, "GND"),
                         (GREEN, "ESP32-CAM IO15 (TX) to Nucleo D21 · PC7 (RX)"),
                         (LIGHTGREEN, "Nucleo D16 · PC6 (TX), 1 kΩ, ESP32-CAM IO14 (RX)")])
d.lines(662, 858, ["Wires at the ESP32-CAM: 5V, GND, IO15, IO14,", "all on the same pin row"], 18)
t(1060, 740, "TX GOES TO RX", 14, "#c62828", weight="bold")
d.lines(1060, 764, ["ESP32-CAM TX (IO15) → STM32 RX (PC7)",
                    "STM32 TX (PC6) → 1 kΩ → ESP32-CAM RX (IO14)",
                    "Text lines, 115200 baud, 8N1",
                    "Both boards use 3.3 V signals: no divider",
                    "1000 µF on the rails: no restarts on WiFi peaks",
                    "Test program: load it first with the DevKit",
                    "(circuit 6)"])
t(1460, 740, "TIPS", 14, "#c62828", weight="bold")
d.lines(1460, 764, ["1. Wire everything with the USB unplugged.",
                    "2. Power into 5V only (not 3V3, not VCC).",
                    "3. Keep the ESP32-CAM microSD slot empty.",
                    "4. Short 5V and GND wires if you have them.",
                    "5. Restarts again and again: power problem.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 5 of the circuits by part · wires E1 to E9 in hardware/04_wiring_list.md section 5, rails R1, R3 and R4 in section 4B")
d.save(sys.argv[1])
