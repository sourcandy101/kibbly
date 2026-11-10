"""Draw hardware/circuits_by_part/03_ultrasonic_hc_sr04/03_ultrasonic_hc_sr04.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import BLACK, BLUEGREY, BROWN, CN7, CN8, CN10, GREY, ORANGE, ROW, Drawing, X  # noqa: E402

d = Drawing(1880, 960)
a, t = d.add, d.text
d.title("PART 3: ULTRASONIC SENSOR HC-SR04",
        "Test setup for step 3. Only the laptop USB is needed: the Nucleo 5V pin feeds the top + rail (5 V).")
d.nucleo([(CN8(9), "5V (CN8 pin 9)", ORANGE, "right"), (CN7(16), "D10 · PD14 (pin 16)", GREY, "left"),
          (CN7(18), "D9 · PD15 (pin 18)", BROWN, "left"), (CN10(5), "GND (pin 5)", BLACK, "left")])
d.breadboard(used=(True, True, True, False))


def resistor(x, y1, y2, bands, label):
    """Vertical resistor between two holes in column x, label on the left."""
    a(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#9e9e9e" stroke-width="2.5"/>')
    top, h = y1 + 8, (y2 - y1) - 16
    a(f'<rect x="{x - 7}" y="{top}" width="14" height="{h}" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
    for k, c in enumerate(bands):
        a(f'<rect x="{x - 7}" y="{top + 4 + k * 5}" width="14" height="3" fill="{c}"/>')
    for y in (y1, y2):
        a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
    t(x - 12, (y1 + y2) / 2 + 4, label, 11, "#6d5a2a", "end", "bold")


# HC-SR04 outside the board, above columns 24 to 27 (VCC, Trig, Echo, Gnd)
px = [X(24), X(25), X(26), X(27)]
cx = (px[0] + px[3]) / 2
a(f'<rect x="{cx - 120}" y="96" width="240" height="140" rx="6" fill="#1565c0" stroke="#0d47a1" stroke-width="2"/>')
for ox in (-62, 62):
    a(f'<circle cx="{cx + ox}" cy="160" r="48" fill="#cfd8dc" stroke="#90a4ae" stroke-width="3"/>')
    a(f'<circle cx="{cx + ox}" cy="160" r="36" fill="#455a64"/>')
    for r in (10, 20, 30):
        a(f'<circle cx="{cx + ox}" cy="160" r="{r}" fill="none" stroke="#607d8b" stroke-width="1.5"/>')
a(f'<rect x="{cx - 14}" y="106" width="28" height="12" rx="5" fill="#eceff1" stroke="#90a4ae"/>')
for x, lab in zip(px, ["VCC", "Trig", "Echo", "Gnd"]):
    a(f'<rect x="{x - 3}" y="236" width="6" height="12" fill="#d4af37"/>')
    t(x, 230, lab, 8, "#fff", "middle", "bold")
t(cx - 132, 140, "HC-SR04 ultrasonic sensor", 14, "#c62828", "end", "bold")
t(cx - 132, 158, "outside the board, facing the dog,", 11, "#555", "end")
t(cx - 132, 174, "joined with 4 female to male wires", 11, "#555", "end")

# sensor wires straight down into the board
d.wire(f"M{px[0]},248 L{px[0]},{ROW['top+']}", ORANGE, [(px[0], ROW['top+'])])
d.wire(f"M{px[1]},248 L{px[1]},{ROW['j']}", GREY, [(px[1], ROW['j'])])
d.wire(f"M{px[2]},248 L{px[2]},{ROW['j']}", BLUEGREY, [(px[2], ROW['j'])])
d.wire(f"M{px[3]},248 L{px[3]},{ROW['top-']}", BLACK, [(px[3], ROW['top-'])])

# voltage divider in column 26: 1 kohm across the middle gap, 2 kohm to the bottom − rail
resistor(X(26), ROW["f"], ROW["e"], ["#8d4e2b", "#111", "#e53935"], "1 kΩ")
resistor(X(26), ROW["a"], ROW["bot-"], ["#e53935", "#111", "#e53935"], "2 kΩ")
a(f'<line x1="{X(26) + 8}" y1="{ROW["c"] - 10}" x2="{X(30)}" y2="{ROW["c"] - 10}" stroke="#4e342e" stroke-width="1.2" stroke-dasharray="4 3"/>')
a(f'<rect x="{X(30) + 2}" y="{ROW["c"] - 26}" width="132" height="32" rx="4" fill="#ffffff" stroke="#bcaaa4"/>')
t(X(30) + 6, ROW["c"] - 14, "middle of the divider:", 10, "#4e342e", weight="bold")
t(X(30) + 6, ROW["c"] + 1, "PD15 sees 3.3 V here", 10, "#4e342e", weight="bold")

# wires to the Nucleo and the rails
d.five_volt_feed(2)
d.ground_link(1)
d.ground_feed(3)
x, y = CN7(16)
d.wire(f"M{x},{y} C560,{y} 760,{ROW['h']} {X(25)},{ROW['h']}", GREY, [(x, y), (X(25), ROW['h'])])
x, y = CN7(18)
d.wire(f"M{x},{y} C600,{y} 780,{ROW['c']} {X(26)},{ROW['c']}", BROWN, [(x, y), (X(26), ROW['c'])])
d.nucleo_labels()
d.zones(3)

# notes
d.notes_box(640, 712, 1220, 230)
t(660, 740, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 764, [(ORANGE, "5 V: Nucleo 5V to the top + rail; sensor VCC"), (BLACK, "GND"),
                         (GREY, "TRIG: Nucleo D10 · PD14"), (BLUEGREY, "ECHO from the sensor (5 V signal)"),
                         (BROWN, "ECHO to Nucleo D9 · PD15 (3.3 V, after the divider)")])
t(1060, 740, "WHY TWO RESISTORS", 14, "#c62828", weight="bold")
d.lines(1060, 764, ["Echo gives 5 V; an STM32 pin wants 3.3 V.",
                    "1 kΩ from Echo to PD15, 2 kΩ from PD15 to GND:",
                    "PD15 sees 5 × 2 ÷ 3 = 3.3 V.",
                    "Bands: 1 kΩ brown black red, 2 kΩ red black red.",
                    "Trig needs no resistor: 3.3 V starts the sensor."])
t(1460, 740, "TIPS", 14, "#c62828", weight="bold")
d.lines(1460, 764, ["1. Wire everything with the USB unplugged.",
                    "2. VCC on 5 V: the HC-SR04 does not work on 3.3 V.",
                    "3. Never connect Echo straight to the Nucleo.",
                    "4. Keep the front clear (range 2 cm to 4 m).",
                    "5. Feeder: an animal under 40 cm starts a photo.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 3 of the circuits by part · wires U1 to U8 in hardware/04_wiring_list.md section 8, rails R1, R3 and R4 in section 4B")
d.save(sys.argv[1])
