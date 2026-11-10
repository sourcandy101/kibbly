"""Draw hardware/circuits_by_part/02_load_cell_hx711/02_load_cell_hx711.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, BROWN, CN8, CN10, GREEN, GREY, RED, ROW, WHITE, YELLOW,  # noqa: E402
                    Drawing, X)

d = Drawing(1420, 1110)
a, t = d.add, d.text
d.title("PART 2: LOAD CELL AND HX711",
        "Test setup for step 3. Only the laptop USB is needed: the scale runs on 3.3 V from the Nucleo.")
d.nucleo([(CN10(5), "GND (pin 5)", BLACK, "left"), (CN10(8), "D4 · PF14 (pin 8)", BROWN, "left"),
          (CN10(10), "D3 · PE13 (pin 10)", GREY, "left"), (CN8(7), "3V3 (CN8 pin 7)", YELLOW, "right")])
d.breadboard(top_used=False)
t(1114, 333, "(not used)", 10, "#b0b0b0")

# HX711 module: 4 pin header in row a, columns 22 to 25, board hanging over the bottom edge
a('<rect x="906" y="546" width="88" height="144" rx="4" fill="#1b6e3a" stroke="#0f4a26" stroke-width="2"/>')
for k, lab in enumerate(["GND", "DT", "SCK", "VCC"]):
    x = X(22 + k)
    a(f'<rect x="{x - 4}" y="{ROW["a"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 574, lab, 8, "#fff", "middle", "bold")
a('<rect x="932" y="598" width="36" height="28" rx="2" fill="#1a1a1a"/>')
t(950, 616, "HX711", 8, "#ddd", "middle", "bold")
for x, y in ((916, 600), (916, 614), (980, 600), (980, 614), (922, 640), (972, 640)):
    a(f'<rect x="{x - 4}" y="{y - 2.5}" width="8" height="5" fill="#c9b37e"/>')
pins6 = ["E+", "E−", "A−", "A+", "B−", "B+"]
for k, lab in enumerate(pins6):
    x = 916 + 13 * k
    a(f'<rect x="{x - 3.5}" y="674" width="7" height="8" fill="#d4af37"/>')
    t(x, 668, lab, 7, "#fff", "middle", "bold")
t(1000, 700, "HX711 board", 13, "#1b6e3a", weight="bold")

# load cell bar
a('<rect x="1080" y="708" width="260" height="48" rx="3" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
for x in (1102, 1126, 1294, 1318):
    a(f'<circle cx="{x}" cy="732" r="6" fill="#ffffff" stroke="#90a4ae" stroke-width="1.5"/>')
a('<rect x="1190" y="711" width="40" height="10" rx="2" fill="#f5f5f5" stroke="#b0bec5"/>')
a('<line x1="1210" y1="726" x2="1210" y2="744" stroke="#455a64" stroke-width="2.5"/>')
a('<path d="M1203,740 L1210,750 L1217,740 Z" fill="#455a64"/>')
t(1210, 700, "5 kg load cell (owned)", 14, "#c62828", "middle", "bold")
t(1210, 776, "arrow on the bar points down", 11, "#555", "middle")

# load cell cable to E+, E−, A−, A+ (thin wires, no crossing)
for y, xpin, col in ((720, 955, GREEN), (728, 942, WHITE), (736, 929, BLACK), (744, 916, RED)):
    d.wire(f"M1080,{y} L{xpin + 12},{y} Q{xpin},{y} {xpin},{y - 12} L{xpin},678", col, [(xpin, 678)], width=3)

# wires on the breadboard and to the Nucleo
d.wire(f"M{X(22)},{ROW['b']} C898,{ROW['b']} {X(20)},566 {X(20)},{ROW['bot-']}", BLACK,
       [(X(22), ROW['b']), (X(20), ROW['bot-'])])
d.wire(f"M{X(25)},{ROW['b']} C1004,{ROW['b']} {X(27)},576 {X(27)},{ROW['bot+']}", YELLOW,
       [(X(25), ROW['b']), (X(27), ROW['bot+'])])
x, y = CN10(8)
d.wire(f"M{x},{y} C460,{y} 700,{ROW['d']} {X(23)},{ROW['d']}", BROWN, [(x, y), (X(23), ROW['d'])])
x, y = CN10(10)
d.wire(f"M{x},{y} C460,{y} 720,{ROW['c']} {X(24)},{ROW['c']}", GREY, [(x, y), (X(24), ROW['c'])])
x, y = CN8(7)
d.wire(f"M{x},{y} C40,{y} 22,380 22,440 L22,866 C22,886 40,892 64,892 L430,892 C492,892 {X(2)},820 {X(2)},{ROW['bot+']}",
       YELLOW, [(x, y), (X(2), ROW['bot+'])])
x, y = CN10(5)
d.wire(f"M{x},{y} C380,{y} 470,{ROW['bot-']} {X(3)},{ROW['bot-']}", BLACK, [(x, y), (X(3), ROW['bot-'])])
d.nucleo_labels()

# mounting inset (side view)
a('<rect x="1170" y="110" width="232" height="350" rx="10" fill="#fafafa" stroke="#dddddd"/>')
t(1182, 136, "HOW TO MOUNT THE LOAD CELL", 12, "#c62828", weight="bold")
t(1182, 152, "side view", 10, "#888")
a('<path d="M1285,184 L1390,184 L1378,226 L1297,226 Z" fill="#b0bec5" stroke="#78909c"/>')
a('<rect x="1262" y="226" width="133" height="14" fill="#90a4ae"/>')
a('<rect x="1357" y="240" width="28" height="26" fill="#78909c"/>')
a('<rect x="1255" y="266" width="130" height="28" fill="#cfd8dc" stroke="#90a4ae"/>')
a('<rect x="1255" y="294" width="28" height="26" fill="#78909c"/>')
a('<rect x="1250" y="320" width="145" height="16" fill="#a1887f"/>')
for x0, y0, y1 in ((1262, 266, 336), (1273, 266, 336), (1364, 226, 294), (1375, 226, 294)):
    a(f'<rect x="{x0}" y="{y0}" width="3" height="{y1 - y0}" fill="#37474f"/>')
a('<line x1="1320" y1="270" x2="1320" y2="286" stroke="#455a64" stroke-width="2"/>')
a('<path d="M1315,283 L1320,291 L1325,283 Z" fill="#455a64"/>')
for y, lab in ((210, "bowl"), (237, "plate"), (257, "spacer"), (284, "load cell"), (311, "spacer"), (332, "base")):
    t(1244, y, lab, 10, "#555", "end")
d.lines(1182, 362, ["1. One end screwed to the base,", "   the other end holds the plate.",
                    "2. Spacers let the bar bend.", "3. Arrow on the bar points down.",
                    "4. Nothing else touches the plate."], 18, 11)

# notes
d.notes_box(640, 796, 760, 290)
t(660, 824, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 848, [(YELLOW, "3.3 V"), (BLACK, "GND"), (BROWN, "DT: Nucleo D4 · PF14"),
                         (GREY, "SCK: Nucleo D3 · PE13")])
d.lines(662, 942, ["Load cell cable: red E+, black E−,", "white A−, green A+ (colours vary by brand)"], 18)
t(1010, 824, "HX711 SETTINGS", 14, "#c62828", weight="bold")
d.lines(1010, 848, ["Powered at 3.3 V, so its DT signal is safe", "  for the STM32",
                    "Channel A, gain 128 (chosen by the code)", "B− and B+: not used",
                    "10 readings per second (fixed on most boards)"])
t(660, 1000, "TIPS", 14, "#c62828", weight="bold")
d.lines(662, 1024, ["1. Wire everything with the USB unplugged.",
                    "2. Solder the thin load cell wires (or use a terminal).",
                    "3. Never press more than 5 kg on the bar."])
d.lines(1080, 1024, ["4. Weight reads negative: swap A+ and A−.",
                     "5. Calibrate with a known weight.",
                     "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 2 of the circuits by part · wires H1 to H12 in hardware/04_wiring_list.md section 7")
d.save(sys.argv[1])
