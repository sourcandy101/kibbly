"""Draw hardware/circuits_by_part/03_ultrasonic_hc_sr04/03_ultrasonic_hc_sr04.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import BLACK, BROWN, CN7, CN8, CN10, GREY, ORANGE, ROW, Drawing, X  # noqa: E402

d = Drawing(1420, 1020)
a, t = d.add, d.text
d.title("PART 3: ULTRASONIC SENSOR HC-SR04",
        "Test setup for step 3. Only the laptop USB is needed: the sensor takes 5 V from the Nucleo 5V pin.")
d.nucleo([(CN8(9), "5V (CN8 pin 9)", ORANGE, "right"), (CN7(16), "D10 · PD14 (pin 16)", GREY, "left"),
          (CN7(18), "D9 · PD15 (pin 18)", BROWN, "left"), (CN10(5), "GND (pin 5)", BLACK, "left")])
d.breadboard(used=(False, False, True, False))
t(1114, 333, "(not used)", 10, "#b0b0b0")
t(1114, 641, "(not used)", 10, "#b0b0b0")


def resistor(x, y1, y2, bands, label, side="right"):
    """Vertical resistor between two holes in column x."""
    a(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#9e9e9e" stroke-width="2.5"/>')
    top, h = y1 + 8, (y2 - y1) - 16
    a(f'<rect x="{x - 7}" y="{top}" width="14" height="{h}" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
    for k, c in enumerate(bands):
        a(f'<rect x="{x - 7}" y="{top + 4 + k * 5}" width="14" height="3" fill="{c}"/>')
    for y in (y1, y2):
        a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
    if side == "right":
        t(x + 12, (y1 + y2) / 2 + 4, label, 11, "#6d5a2a", "start", "bold")
    else:
        t(x - 12, (y1 + y2) / 2 + 4, label, 11, "#6d5a2a", "end", "bold")


# HC-SR04: 4 pins in row j, columns 22 to 25, board standing up, the two transducers face the dog
a('<rect x="830" y="206" width="240" height="144" rx="6" fill="#1565c0" stroke="#0d47a1" stroke-width="2"/>')
for cx in (888, 1012):
    a(f'<circle cx="{cx}" cy="270" r="50" fill="#cfd8dc" stroke="#90a4ae" stroke-width="3"/>')
    a(f'<circle cx="{cx}" cy="270" r="38" fill="#455a64"/>')
    for r in (10, 20, 30):
        a(f'<circle cx="{cx}" cy="270" r="{r}" fill="none" stroke="#607d8b" stroke-width="1.5"/>')
a('<rect x="936" y="222" width="28" height="12" rx="5" fill="#eceff1" stroke="#90a4ae"/>')
for k, lab in enumerate(["VCC", "Trig", "Echo", "Gnd"]):
    x = X(22 + k)
    a(f'<rect x="{x - 4}" y="{ROW["j"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 342, lab, 8, "#fff", "middle", "bold")
t(950, 168, "HC-SR04 ultrasonic sensor", 14, "#c62828", "middle", "bold")
t(950, 186, "the two round transducers face the dog", 11, "#555", "middle")

# voltage divider: 1 kohm across the middle gap (Echo to PD15), 2 kohm from PD15 to GND
resistor(X(24), ROW["f"], ROW["e"], ["#8d4e2b", "#111", "#e53935"], "1 kΩ", "left")
resistor(X(24), ROW["a"], ROW["bot-"], ["#e53935", "#111", "#e53935"], "2 kΩ", "left")
a(f'<line x1="{X(24) + 8}" y1="{ROW["c"] - 10}" x2="1108" y2="{ROW["c"] - 10}" stroke="#4e342e" stroke-width="1.2" stroke-dasharray="4 3"/>')
t(1114, ROW["c"] - 14, "middle of the divider:", 10, "#4e342e", weight="bold")
t(1114, ROW["c"] + 1, "PD15 sees 3.3 V here", 10, "#4e342e", weight="bold")

# wires
x, y = CN8(9)
d.wire(f"M{x},{y} C40,{y} 30,400 30,460 L30,872 C30,890 48,898 70,898 L400,898 C428,898 440,880 440,850 "
       f"L440,404 C440,384 452,{ROW['i']} 478,{ROW['i']} L{X(22)},{ROW['i']}", ORANGE, [(x, y), (X(22), ROW['i'])])
x, y = CN7(16)
d.wire(f"M{x},{y} C520,{y} 700,{ROW['h']} {X(23)},{ROW['h']}", GREY, [(x, y), (X(23), ROW['h'])])
x, y = CN7(18)
d.wire(f"M{x},{y} C540,{y} 700,{ROW['c']} {X(24)},{ROW['c']}", BROWN, [(x, y), (X(24), ROW['c'])])
x, y = CN10(5)
d.wire(f"M{x},{y} C380,{y} 470,{ROW['bot-']} {X(3)},{ROW['bot-']}", BLACK, [(x, y), (X(3), ROW['bot-'])])
d.wire(f"M{X(25)},{ROW['i']} C{X(26)},{ROW['i']} {X(26)},420 {X(26)},460 L{X(26)},{ROW['bot-']}", BLACK,
       [(X(25), ROW['i']), (X(26), ROW['bot-'])])
d.nucleo_labels()

# notes
d.notes_box(640, 672, 760, 330)
t(660, 700, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 724, [(ORANGE, "5 V: Nucleo 5V pin"), (BLACK, "GND"), (GREY, "TRIG: Nucleo D10 · PD14"),
                         (BROWN, "ECHO: Nucleo D9 · PD15 (after the divider)")])
d.lines(662, 822, ["Sensor: VCC column 22, Trig 23, Echo 24, Gnd 25", "(row j, top half)"], 18)
t(1010, 700, "WHY TWO RESISTORS", 14, "#c62828", weight="bold")
d.lines(1010, 724, ["Echo gives 5 V; an STM32 pin wants 3.3 V.",
                    "1 kΩ from Echo to PD15, 2 kΩ from PD15",
                    "  to GND: PD15 sees 5 × 2 ÷ 3 = 3.3 V.",
                    "Bands: 1 kΩ brown black red,",
                    "  2 kΩ red black red.",
                    "Trig needs no resistor: 3.3 V is enough",
                    "  for the sensor to start."])
t(660, 892, "TIPS", 14, "#c62828", weight="bold")
d.lines(662, 916, ["1. Wire everything with the USB unplugged.",
                   "2. VCC on 5 V: the HC-SR04 does not work on 3.3 V.",
                   "3. Never connect Echo straight to the Nucleo."])
d.lines(1080, 916, ["4. Keep the front clear (range 2 cm to 4 m).",
                    "5. Feeder: an animal under 40 cm starts a photo.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 3 of the circuits by part · wires U1 to U7 in hardware/04_wiring_list.md section 8")
d.save(sys.argv[1])
