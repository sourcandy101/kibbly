"""Draw hardware/circuits_by_part/01_stepper_motor_drv8825/01_stepper_motor_drv8825.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, BLUE, BLUEGREY, BROWN, CN8, CN10, GREEN, GREY, RED, ROW,  # noqa: E402
                    YELLOW, Drawing, X)

d = Drawing(1880, 960)
a, t = d.add, d.text
d.title("PART 1: STEPPER MOTOR AND DRV8825 DRIVER",
        "Test setup for step 3. The Nucleo runs from the laptop USB; the motor runs from the 12 V adapter.")
d.nucleo([(CN10(2), "D7 · PF13 (pin 2)", BROWN, "left"), (CN10(4), "D6 · PE9 (pin 4)", GREY, "left"),
          (CN10(5), "GND (pin 5)", BLACK, "left"), (CN10(12), "D2 · PF15 (pin 12)", BLUEGREY, "left"),
          (CN8(7), "3V3 (CN8 pin 7)", YELLOW, "right")])
d.breadboard(used=(False, True, True, True))

# 12 V column: column 5, top half (framed in red)
a(f'<rect x="{X(5) - 11}" y="{ROW["j"] - 12}" width="22" height="{ROW["f"] - ROW["j"] + 22}" rx="4" '
  f'fill="#ffcdd2" fill-opacity="0.55" stroke="#e53935" stroke-width="1.5" stroke-dasharray="4 3"/>')

# DRV8825 turned so that VMOT is top left and EN bottom left (columns 5 to 12)
a(f'<rect x="{X(5) - 12}" y="424" width="{X(12) - X(5) + 24}" height="64" rx="3" fill="#4a1f7a" stroke="#2e1250" stroke-width="2"/>')
top = ["VMOT", "GND", "B2", "B1", "A1", "A2", "FLT", "GND"]
bot = ["EN", "M0", "M1", "M2", "RST", "SLP", "STEP", "DIR"]
for k in range(8):
    x = X(5 + k)
    a(f'<circle cx="{x}" cy="436" r="3.5" fill="#d4af37"/>')
    a(f'<circle cx="{x}" cy="476" r="3.5" fill="#d4af37"/>')
    fs = lambda s: 6.3 if len(s) > 3 else 7.5
    t(x, 451, top[k], fs(top[k]), "#fff", "middle", "bold")
    t(x, 469, bot[k], fs(bot[k]), "#fff", "middle", "bold")
t(X(12) + 22, 456, "DRV8825 driver", 14, "#4a1f7a", weight="bold")
t(X(12) + 22, 472, "chip side up, VMOT and EN in column 5", 11, "#6a4a8a")

# 10 kohm resistor from EN (column 5, row a) to the 3.3 V rail
a(f'<line x1="{X(5)}" y1="{ROW["a"]}" x2="{X(5)}" y2="{ROW["bot+"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<rect x="{X(5) - 7}" y="566" width="14" height="38" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
for y, c in ((573, "#8d4e2b"), (580, "#111"), (587, "#ef6c00"), (597, "#c9a227")):
    a(f'<rect x="{X(5) - 7}" y="{y}" width="14" height="3.5" fill="{c}"/>')
for y in (ROW["a"], ROW["bot+"]):
    a(f'<circle cx="{X(5)}" cy="{y}" r="3.5" fill="#757575"/>')
t(X(5) + 11, 588, "10 kΩ", 10, "#6d5a2a", "start", "bold")

# 1000 uF capacitor: long leg (+) in column 5 row j (12 V), short leg in the top − rail, column 4
a(f'<line x1="582" y1="248" x2="{X(5)}" y2="{ROW["j"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<line x1="566" y1="248" x2="{X(4)}" y2="{ROW["top-"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a('<rect x="560" y="206" width="28" height="44" rx="6" fill="#1f2f74"/>')
a('<rect x="560" y="206" width="9" height="44" rx="3" fill="#9fb0e8"/>')
for y in (216, 228, 240):
    a(f'<line x1="562" y1="{y}" x2="567" y2="{y}" stroke="#1f2f74" stroke-width="2"/>')
a('<ellipse cx="574" cy="207" rx="14" ry="4" fill="#3a4c9a"/>')
for x, y in ((X(5), ROW["j"]), (X(4), ROW["top-"])):
    a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
t(466, 222, "1000 µF capacitor", 12, "#1f2f74", "end", "bold")
t(466, 237, "long leg (+): column 5 →", 10, "#1f2f74", "end")

# DC jack module and adapter
a('<rect x="352" y="128" width="100" height="50" rx="8" fill="#263238"/>')
t(402, 151, "12 V 2 A", 13, "#fff", "middle", "bold")
t(402, 167, "adapter", 11, "#cfd8dc", "middle")
t(402, 195, "plug in last", 11, "#c62828", "middle", "bold")
a('<path d="M452,153 C462,153 462,155 470,155" fill="none" stroke="#111" stroke-width="6"/>')
a('<rect x="470" y="124" width="114" height="62" rx="4" fill="#1565c0"/>')
a('<rect x="470" y="138" width="40" height="34" rx="4" fill="#212121"/>')
a('<circle cx="490" cy="155" r="7" fill="#555"/>')
a('<rect x="520" y="142" width="58" height="40" rx="3" fill="#2e7d32"/>')
for x in (534, 564):
    a(f'<circle cx="{x}" cy="161" r="8" fill="#bdbdbd" stroke="#757575"/>')
    a(f'<line x1="{x - 5}" y1="161" x2="{x + 5}" y2="161" stroke="#616161" stroke-width="2"/>')
t(534, 138, "−", 12, "#fff", "middle", "bold")
t(564, 138, "+", 12, "#fff", "middle", "bold")
t(527, 116, "DC jack", 12, "#1565c0", "middle", "bold")

# NEMA 17 motor above its columns, connector pins over columns 7 to 10
a('<rect x="606" y="92" width="130" height="120" rx="10" fill="#bdbdbd" stroke="#8a8a8a" stroke-width="2"/>')
for cx, cy in ((622, 108), (720, 108), (622, 196), (720, 196)):
    a(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#757575"/>')
a('<circle cx="671" cy="152" r="26" fill="#9e9e9e" stroke="#757575" stroke-width="2"/>')
a('<circle cx="671" cy="152" r="7" fill="#e0e0e0" stroke="#757575"/>')
a('<rect x="610" y="212" width="80" height="18" rx="2" fill="#f5f5f5" stroke="#9e9e9e"/>')
t(750, 118, "NEMA 17 stepper motor", 14, "#c62828", weight="bold")
t(750, 136, "17HS4401, 12 V", 12, "#555")
t(750, 152, "cable colours vary by brand:", 11, "#555")
t(750, 166, "find the two coil pairs first", 11, "#555")

# wires, power side (12 V only in column 5)
d.ground_link(1)
d.wire(f"M534,186 C534,250 {X(3)},262 {X(3)},290 L{X(3)},{ROW['top-']}", BLACK, [(X(3), ROW['top-'])])
d.wire(f"M564,186 C564,198 548,198 548,212 L548,404 C548,412 552,{ROW['g']} {X(4)},{ROW['g']} L{X(5)},{ROW['g']}",
       RED, [(X(5), ROW['g'])])
d.wire(f"M{X(6)},{ROW['j']} L{X(6)},{ROW['top-']}", BLACK, [(X(6), ROW['j']), (X(6), ROW['top-'])])
# motor cable: coil B blue (B2) and red (B1), coil A black (A1) and green (A2)
for c, r, col in ((7, "g", BLUE), (8, "h", RED), (9, "i", BLACK), (10, "j", GREEN)):
    d.wire(f"M{X(c)},230 L{X(c)},{ROW[r]}", col, [(X(c), ROW[r])], width=3.5)
    a(f'<rect x="{X(c) - 4}" y="222" width="8" height="8" fill="{col[1]}"/>')
# wires, control side (bottom rail = 3.3 V)
for c in (8, 9, 10):
    d.wire(f"M{X(c)},{ROW['a']} L{X(c)},{ROW['bot+']}", YELLOW, [(X(c), ROW['a']), (X(c), ROW['bot+'])])
d.three_volt_feed(2)
d.ground_feed(3)
x, y = CN10(12)
d.wire(f"M{x},{y} C400,{y} 470,{ROW['b']} {X(5)},{ROW['b']}", BLUEGREY, [(x, y), (X(5), ROW['b'])])
x, y = CN10(4)
d.wire(f"M{x},{y} C430,{y} 560,{ROW['c']} {X(11)},{ROW['c']}", GREY, [(x, y), (X(11), ROW['c'])])
x, y = CN10(2)
d.wire(f"M{x},{y} C430,{y} 540,{ROW['d']} {X(12)},{ROW['d']}", BROWN, [(x, y), (X(12), ROW['d'])])
d.nucleo_labels()
d.zones(1)

# notes
d.notes_box(640, 712, 1220, 230)
t(660, 740, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 764, [(RED, "12 V: DC jack + to column 5 only"), (BLACK, "GND"), (YELLOW, "3.3 V"),
                         (GREY, "STEP: Nucleo D6 · PE9"), (BROWN, "DIR: Nucleo D7 · PF13"),
                         (BLUEGREY, "EN: Nucleo D2 · PF15")])
t(1060, 740, "DRIVER SETTINGS", 14, "#c62828", weight="bold")
d.lines(1060, 764, ["M2 to 3.3 V, M0 and M1 open: 1/16 step (3200 per turn)",
                    "SLP and RST to 3.3 V: driver awake",
                    "10 kΩ on EN: motor off until PF15 goes low",
                    "Current: about 0.5 V on the potentiometer = 1 A",
                    "FLT and the GND above DIR: no wire needed",
                    "Motor: black + green = coil A, red + blue = coil B"])
t(1460, 740, "SAFETY", 14, "#c62828", weight="bold")
d.lines(1460, 764, ["1. Wire with the adapter and USB unplugged.",
                    "2. 12 V only in column 5 (red frame), never",
                    "   on a rail: top + rail is 5 V.",
                    "3. Never plug or unplug the motor with 12 V on.",
                    "4. Power on: USB, then adapter. Off: adapter first.",
                    "5. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 1 of the circuits by part · wires V1 to V19 in hardware/04_wiring_list.md section 6B, rails R2 to R4 in section 4B")
d.save(sys.argv[1])
