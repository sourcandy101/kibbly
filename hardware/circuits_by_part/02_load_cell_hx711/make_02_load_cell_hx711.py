"""Draw hardware/circuits_by_part/02_load_cell_hx711/02_load_cell_hx711.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, BROWN, CN8, CN10, GREEN, GREY, RED, ROW, WHITE, YELLOW,  # noqa: E402
                    Drawing, X)

d = Drawing(1880, 1160)
a, t = d.add, d.text
d.title("PART 2: LOAD CELL AND HX711",
        "Test setup for step 3. Only the laptop USB is needed: the scale runs on 3.3 V from the Nucleo.")
d.nucleo([(CN10(5), "GND (pin 5)", BLACK, "left"), (CN10(8), "D4 · PF14 (pin 8)", BROWN, "left"),
          (CN10(10), "D3 · PE13 (pin 10)", GREY, "left"), (CN8(7), "3V3 (CN8 pin 7)", YELLOW, "right")])
d.breadboard(used=(False, False, True, True))

# HX711: 4 pin header in row a, columns 15 to 18, board hanging over the bottom edge
x1, x2 = X(15) - 12, X(18) + 12
a(f'<rect x="{x1}" y="546" width="{x2 - x1}" height="144" rx="4" fill="#1b6e3a" stroke="#0f4a26" stroke-width="2"/>')
for k, lab in enumerate(["GND", "DT", "SCK", "VCC"]):
    x = X(15 + k)
    a(f'<rect x="{x - 4}" y="{ROW["a"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 574, lab, 8, "#fff", "middle", "bold")
cx = (x1 + x2) / 2
a(f'<rect x="{cx - 18}" y="598" width="36" height="28" rx="2" fill="#1a1a1a"/>')
t(cx, 616, "HX711", 8, "#ddd", "middle", "bold")
pin6 = [x1 + 10 + 15 * k for k in range(6)]
for x, lab in zip(pin6, ["E+", "E−", "A−", "A+", "B−", "B+"]):
    a(f'<rect x="{x - 3.5}" y="674" width="7" height="8" fill="#d4af37"/>')
    t(x, 668, lab, 7, "#fff", "middle", "bold")
t(x1 - 8, 700, "HX711 board", 13, "#1b6e3a", "end", "bold")

# load cell bar and its 4 thin wires to E+, E−, A−, A+ (no crossing)
a('<rect x="900" y="708" width="260" height="48" rx="3" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
for x in (922, 946, 1114, 1138):
    a(f'<circle cx="{x}" cy="732" r="6" fill="#ffffff" stroke="#90a4ae" stroke-width="1.5"/>')
a('<rect x="1010" y="711" width="40" height="10" rx="2" fill="#f5f5f5" stroke="#b0bec5"/>')
a('<line x1="1030" y1="726" x2="1030" y2="744" stroke="#455a64" stroke-width="2.5"/>')
a('<path d="M1023,740 L1030,750 L1037,740 Z" fill="#455a64"/>')
t(1030, 700, "5 kg load cell (owned)", 14, "#c62828", "middle", "bold")
t(1030, 776, "arrow on the bar points down", 11, "#555", "middle")
for y, xpin, col in ((720, pin6[3], GREEN), (728, pin6[2], WHITE), (736, pin6[1], BLACK), (744, pin6[0], RED)):
    d.wire(f"M900,{y} L{xpin + 12},{y} Q{xpin},{y} {xpin},{y - 12} L{xpin},678", col, [(xpin, 678)], width=3)

# wires on the breadboard and to the Nucleo
d.wire(f"M{X(15)},{ROW['b']} C{X(14) + 2},{ROW['b']} {X(14)},556 {X(14)},{ROW['bot-']}", BLACK,
       [(X(15), ROW['b']), (X(14), ROW['bot-'])])
d.wire(f"M{X(18)},{ROW['b']} C{X(20) - 5},{ROW['b']} {X(20)},560 {X(20)},{ROW['bot+']}", YELLOW,
       [(X(18), ROW['b']), (X(20), ROW['bot+'])])
x, y = CN10(8)
d.wire(f"M{x},{y} C440,{y} 600,{ROW['d']} {X(16)},{ROW['d']}", BROWN, [(x, y), (X(16), ROW['d'])])
x, y = CN10(10)
d.wire(f"M{x},{y} C440,{y} 620,{ROW['c']} {X(17)},{ROW['c']}", GREY, [(x, y), (X(17), ROW['c'])])
d.three_volt_feed(2)
d.ground_feed(3)
d.nucleo_labels()

# mounting inset (side view), shifted under the board
dy = 514
a(f'<rect x="1176" y="656" width="684" height="204" rx="10" fill="#fafafa" stroke="#dddddd"/>')
t(1190, 678, "HOW TO MOUNT THE LOAD CELL (side view)", 12, "#c62828", weight="bold")
a(f'<path d="M1285,{184 + dy} L1390,{184 + dy} L1378,{226 + dy} L1297,{226 + dy} Z" fill="#b0bec5" stroke="#78909c"/>')
a(f'<rect x="1262" y="{226 + dy}" width="133" height="14" fill="#90a4ae"/>')
a(f'<rect x="1357" y="{240 + dy}" width="28" height="26" fill="#78909c"/>')
a(f'<rect x="1255" y="{266 + dy}" width="130" height="28" fill="#cfd8dc" stroke="#90a4ae"/>')
a(f'<rect x="1255" y="{294 + dy}" width="28" height="26" fill="#78909c"/>')
a(f'<rect x="1250" y="{320 + dy}" width="145" height="16" fill="#a1887f"/>')
for x0, y0, y1 in ((1262, 266, 336), (1273, 266, 336), (1364, 226, 294), (1375, 226, 294)):
    a(f'<rect x="{x0}" y="{y0 + dy}" width="3" height="{y1 - y0}" fill="#37474f"/>')
a(f'<line x1="1320" y1="{270 + dy}" x2="1320" y2="{286 + dy}" stroke="#455a64" stroke-width="2"/>')
a(f'<path d="M1315,{283 + dy} L1320,{291 + dy} L1325,{283 + dy} Z" fill="#455a64"/>')
for y, lab in ((210, "bowl"), (237, "plate"), (257, "spacer"), (284, "load cell"), (311, "spacer"), (332, "base")):
    t(1244, y + dy, lab, 10, "#555", "end")
d.lines(1420, 720, ["1. One end screwed to the base, the other end holds the plate.",
                    "2. Spacers let the bar bend.",
                    "3. The arrow on the bar points down.",
                    "4. Nothing else touches the plate (no wire, no wall)."], 22, 12)
d.zones(2, 880)

# notes
d.notes_box(640, 918, 1220, 220)
t(660, 946, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 970, [(YELLOW, "3.3 V"), (BLACK, "GND"), (BROWN, "DT: Nucleo D4 · PF14"),
                         (GREY, "SCK: Nucleo D3 · PE13")])
d.lines(662, 1064, ["Load cell: red E+, black E−, white A−, green A+", "(colours vary by brand)"], 18)
t(1060, 946, "HX711 SETTINGS", 14, "#c62828", weight="bold")
d.lines(1060, 970, ["Powered at 3.3 V: its DT signal is safe for the STM32",
                    "Channel A, gain 128 (chosen by the code)",
                    "B− and B+: not used",
                    "10 readings per second (fixed on most boards)"])
t(1460, 946, "TIPS", 14, "#c62828", weight="bold")
d.lines(1460, 970, ["1. Wire everything with the USB unplugged.",
                    "2. Solder the thin load cell wires (or a terminal).",
                    "3. Never press more than 5 kg on the bar.",
                    "4. Weight reads negative: swap A+ and A−.",
                    "5. Calibrate with a known weight.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 2 of the circuits by part · wires H1 to H10 in hardware/04_wiring_list.md section 7, rails R2 and R3 in section 4B")
d.save(sys.argv[1])
