"""Draw hardware/circuits_by_part/01_stepper_motor_drv8825/01_stepper_motor_drv8825.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, BLUE, BLUEGREY, BROWN, CN8, CN10, GREEN, GREY, RED, ROW,  # noqa: E402
                    YELLOW, Drawing, X)

d = Drawing(1420, 1020)
a, t = d.add, d.text
d.title("PART 1: STEPPER MOTOR AND DRV8825 DRIVER",
        "Test setup for step 3. The Nucleo runs from the laptop USB; the motor runs from the 12 V adapter.")
d.nucleo([(CN10(2), "D7 · PF13 (pin 2)", BROWN, "left"), (CN10(4), "D6 · PE9 (pin 4)", GREY, "left"),
          (CN10(5), "GND (pin 5)", BLACK, "left"), (CN10(12), "D2 · PF15 (pin 12)", BLUEGREY, "left"),
          (CN8(7), "3V3 (CN8 pin 7)", YELLOW, "right")])
d.breadboard()

# DRV8825 turned so that VMOT is top left and EN bottom left
a('<rect x="708" y="424" width="164" height="64" rx="3" fill="#4a1f7a" stroke="#2e1250" stroke-width="2"/>')
top = ["VMOT", "GND", "B2", "B1", "A1", "A2", "FLT", "GND"]
bot = ["EN", "M0", "M1", "M2", "RST", "SLP", "STEP", "DIR"]
for k in range(8):
    x = X(12 + k)
    a(f'<circle cx="{x}" cy="436" r="3.5" fill="#d4af37"/>')
    a(f'<circle cx="{x}" cy="476" r="3.5" fill="#d4af37"/>')
    fs = lambda s: 6.3 if len(s) > 3 else 7.5
    t(x, 451, top[k], fs(top[k]), "#fff", "middle", "bold")
    t(x, 469, bot[k], fs(bot[k]), "#fff", "middle", "bold")
t(884, 456, "DRV8825 driver", 14, "#4a1f7a", weight="bold")
t(884, 472, "chip side up, VMOT and EN in column 12", 11, "#6a4a8a")

# 10 kohm resistor from EN (column 12, row a) to the 3.3 V rail
a(f'<line x1="{X(12)}" y1="{ROW["a"]}" x2="{X(12)}" y2="{ROW["bot+"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<rect x="{X(12) - 7}" y="566" width="14" height="38" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
for y, c in ((573, "#8d4e2b"), (580, "#111"), (587, "#ef6c00"), (597, "#c9a227")):
    a(f'<rect x="{X(12) - 7}" y="{y}" width="14" height="3.5" fill="{c}"/>')
for y in (ROW["a"], ROW["bot+"]):
    a(f'<circle cx="{X(12)}" cy="{y}" r="3.5" fill="#757575"/>')
t(X(12) + 11, 590, "10 kΩ", 11, "#6d5a2a", "start", "bold")

# 1000 uF capacitor on the 12 V rails: long leg column 10, short leg column 7
a(f'<line x1="666" y1="254" x2="{X(10)}" y2="{ROW["top+"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<line x1="654" y1="254" x2="{X(7)}" y2="{ROW["top-"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a('<rect x="646" y="212" width="28" height="44" rx="6" fill="#1f2f74"/>')
a('<rect x="646" y="212" width="9" height="44" rx="3" fill="#9fb0e8"/>')
for y in (222, 234, 246):
    a(f'<line x1="648" y1="{y}" x2="653" y2="{y}" stroke="#1f2f74" stroke-width="2"/>')
a('<ellipse cx="660" cy="213" rx="14" ry="4" fill="#3a4c9a"/>')
for x, y in ((X(10), ROW["top+"]), (X(7), ROW["top-"])):
    a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
t(684, 226, "1000 µF", 12, "#1f2f74", weight="bold")
t(684, 241, "long leg (+) on 12 V", 11, "#1f2f74")

# DC jack module and adapter
a('<rect x="352" y="165" width="100" height="50" rx="8" fill="#263238"/>')
t(402, 188, "12 V 2 A", 13, "#fff", "middle", "bold")
t(402, 204, "adapter", 11, "#cfd8dc", "middle")
t(402, 232, "plug in last", 11, "#c62828", "middle", "bold")
a('<path d="M452,190 C470,190 472,195 490,195" fill="none" stroke="#111" stroke-width="6"/>')
a('<rect x="488" y="164" width="114" height="62" rx="4" fill="#1565c0"/>')
a('<rect x="488" y="178" width="42" height="34" rx="4" fill="#212121"/>')
a('<circle cx="509" cy="195" r="7" fill="#555"/>')
a('<rect x="540" y="182" width="56" height="40" rx="3" fill="#2e7d32"/>')
for x in (554, 582):
    a(f'<circle cx="{x}" cy="200" r="8" fill="#bdbdbd" stroke="#757575"/>')
    a(f'<line x1="{x - 5}" y1="200" x2="{x + 5}" y2="200" stroke="#616161" stroke-width="2"/>')
t(554, 178, "−", 13, "#fff", "middle", "bold")
t(582, 178, "+", 13, "#fff", "middle", "bold")
t(545, 158, "DC jack", 12, "#1565c0", "middle", "bold")

# NEMA 17 motor, connector on its left face, pins aligned with rows j, i, h, g
a('<rect x="1190" y="326" width="140" height="44" fill="#bdbdbd" stroke="#8a8a8a"/>')
a('<rect x="1190" y="370" width="140" height="56" fill="#3a3a3a"/>')
a('<rect x="1190" y="426" width="140" height="44" fill="#bdbdbd" stroke="#8a8a8a"/>')
a('<rect x="1330" y="372" width="10" height="52" fill="#9e9e9e"/>')
a('<rect x="1340" y="391" width="42" height="14" rx="2" fill="#cfcfcf" stroke="#9e9e9e"/>')
a('<rect x="1170" y="342" width="20" height="88" rx="2" fill="#f5f5f5" stroke="#9e9e9e"/>')
t(1260, 312, "NEMA 17 stepper motor", 14, "#c62828", "middle", "bold")
t(1260, 492, "17HS4401, 12 V", 12, "#555", "middle")
t(1260, 508, "cable colours vary by brand:", 11, "#555", "middle")
t(1260, 522, "find the two coil pairs first", 11, "#555", "middle")

# wires, power side (top rails = 12 V)
d.wire(f"M{X(1)},{ROW['top-']} L{X(1)},{ROW['bot-']}", BLACK, [(X(1), ROW['top-']), (X(1), ROW['bot-'])])
d.wire(f"M554,222 C554,262 {X(2)},270 {X(2)},{ROW['top-']}", BLACK, [(X(2), ROW['top-'])])
d.wire(f"M582,222 C582,262 {X(3)},262 {X(3)},{ROW['top+']}", RED, [(X(3), ROW['top+'])])
d.wire(f"M{X(12)},{ROW['j']} L{X(12)},{ROW['top+']}", RED, [(X(12), ROW['j']), (X(12), ROW['top+'])])
d.wire(f"M{X(13)},{ROW['j']} L{X(13)},{ROW['top-']}", BLACK, [(X(13), ROW['j']), (X(13), ROW['top-'])])
# motor cable: coil A black (A1) and green (A2), coil B red (B1) and blue (B2)
for c, r, col in ((17, "j", GREEN), (16, "i", BLACK), (15, "h", RED), (14, "g", BLUE)):
    d.wire(f"M1170,{ROW[r]} L{X(c)},{ROW[r]}", col, [(X(c), ROW[r])])
    a(f'<rect x="1166" y="{ROW[r] - 4}" width="8" height="8" fill="{col[1]}"/>')
# wires, control side (bottom rails = 3.3 V)
for c in (15, 16, 17):
    d.wire(f"M{X(c)},{ROW['a']} L{X(c)},{ROW['bot+']}", YELLOW, [(X(c), ROW['a']), (X(c), ROW['bot+'])])
x, y = CN8(7)
d.wire(f"M{x},{y} C40,{y} 22,380 22,440 L22,866 C22,886 40,892 64,892 L430,892 C492,892 {X(2)},820 {X(2)},{ROW['bot+']}",
       YELLOW, [(x, y), (X(2), ROW['bot+'])])
x, y = CN10(5)
d.wire(f"M{x},{y} C380,{y} 470,{ROW['bot-']} {X(3)},{ROW['bot-']}", BLACK, [(x, y), (X(3), ROW['bot-'])])
x, y = CN10(12)
d.wire(f"M{x},{y} C430,{y} 560,{ROW['b']} {X(12)},{ROW['b']}", BLUEGREY, [(x, y), (X(12), ROW['b'])])
x, y = CN10(4)
d.wire(f"M{x},{y} C440,{y} 620,{ROW['c']} {X(18)},{ROW['c']}", GREY, [(x, y), (X(18), ROW['c'])])
x, y = CN10(2)
d.wire(f"M{x},{y} C440,{y} 600,{ROW['d']} {X(19)},{ROW['d']}", BROWN, [(x, y), (X(19), ROW['d'])])
d.nucleo_labels()

# notes
d.notes_box(640, 672, 760, 330)
t(660, 700, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 724, [(RED, "12 V"), (BLACK, "GND"), (YELLOW, "3.3 V"), (GREY, "STEP: Nucleo D6 · PE9"),
                         (BROWN, "DIR: Nucleo D7 · PF13"), (BLUEGREY, "EN: Nucleo D2 · PF15")])
d.lines(662, 862, ["Motor cable: black + green = coil A (A1, A2)", "red + blue = coil B (B1, B2)"], 18)
t(1010, 700, "DRIVER SETTINGS", 14, "#c62828", weight="bold")
d.lines(1010, 724, ["M2 to 3.3 V, M0 and M1 open: 1/16 step,", "  so 3200 steps per motor turn",
                    "SLP and RST to 3.3 V: driver awake",
                    "10 kΩ on EN: motor stays off until the", "  STM32 sets PF15 low",
                    "Current: about 0.5 V on the potentiometer", "  (Vref) gives 1 A",
                    "FLT and the GND above DIR: no wire needed"])
t(660, 912, "SAFETY", 14, "#c62828", weight="bold")
d.lines(662, 936, ["1. Wire everything with the adapter and the USB unplugged.",
                   "2. Top + rail is 12 V, bottom + rail is 3.3 V: mark them with tape.",
                   "3. Never plug or unplug the motor while 12 V is on."])
d.lines(1080, 936, ["4. Power on: USB first, then the adapter.",
                    "5. Power off: adapter first, then the USB.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 1 of the circuits by part · wires V1 to V22 in hardware/04_wiring_list.md section 6B")
d.save(sys.argv[1])
