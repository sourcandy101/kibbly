"""Draw hardware/circuits_by_part/01_stepper_motor_drv8825.svg (Fritzing style)."""
import sys
W, H = 1420, 1020
out = []
add = out.append
FONT = 'font-family="Arial, Helvetica, sans-serif"'

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, s, size=12, fill="#222", anchor="start", weight="normal", extra=""):
    add(f'<text x="{x}" y="{y}" {FONT} font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{esc(s)}</text>')

RED = ("#e53935", "#8e1b18"); BLACK = ("#333333", "#000000"); YELLOW = ("#fdd835", "#a68a00")
GREY = ("#a8a8a8", "#5f5f5f"); BROWN = ("#8d6e63", "#4e342e"); BLUEGREY = ("#78909c", "#37474f")
GREEN = ("#43a047", "#1b5e20"); BLUE = ("#1e88e5", "#0d47a1")

def wire(d, col, ends):
    add(f'<path d="{d}" fill="none" stroke="{col[1]}" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/>')
    add(f'<path d="{d}" fill="none" stroke="{col[0]}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, y in ends:
        add(f'<circle cx="{x}" cy="{y}" r="4.6" fill="{col[1]}" stroke="#ffffff" stroke-width="1.2"/>')

# breadboard geometry
X = lambda c: 500 + (c - 1) * 20
ROW = {"top+": 292, "top-": 312, "j": 356, "i": 376, "h": 396, "g": 416, "f": 436,
       "e": 476, "d": 496, "c": 516, "b": 536, "a": 556, "bot-": 600, "bot+": 620}

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(40, 46, "PART 1: STEPPER MOTOR AND DRV8825 DRIVER", 28, "#c62828", weight="bold")
text(40, 72, "Test setup for step 3. The Nucleo runs from the laptop USB; the motor runs from the 12 V adapter.", 15, "#444")

# Nucleo
add('<rect x="40" y="130" width="300" height="720" rx="10" fill="#f6f6f3" stroke="#9e9e9e" stroke-width="2"/>')
add('<line x1="40" y1="270" x2="340" y2="270" stroke="#bdbdbd" stroke-width="2" stroke-dasharray="6 5"/>')
add('<rect x="165" y="116" width="50" height="26" rx="3" fill="#b0b0b0" stroke="#757575"/>')
add('<rect x="175" y="122" width="30" height="10" rx="2" fill="#757575"/>')
add('<path d="M190,116 L190,96" stroke="#555" stroke-width="7" stroke-linecap="round"/>')
text(222, 108, "USB cable to the laptop (power and code)", 12, "#555")
add('<rect x="100" y="180" width="44" height="44" rx="3" fill="#2b2b2b"/>')
text(122, 206, "ST-LINK", 9, "#ddd", "middle")
text(250, 210, "ST-LINK part", 12, "#9e9e9e", "middle")
# morpho headers
for x0 in (50, 304):
    add(f'<rect x="{x0}" y="284" width="30" height="492" rx="2" fill="#262626"/>')
    for r in range(35):
        for dx in (8, 22):
            add(f'<rect x="{x0 + dx - 2.5}" y="{292 + r * 14 - 2.5}" width="5" height="5" fill="#d4af37"/>')
text(65, 280, "CN11", 10, "#666", "middle"); text(319, 280, "CN12", 10, "#666", "middle")
# zio headers
def zio(xo, xe, y0, rows, name):
    add(f'<rect x="{min(xo, xe) - 8}" y="{y0 - 8}" width="32" height="{rows * 14 + 2}" rx="2" fill="#1b1b1b"/>')
    for r in range(rows):
        for x in (xo, xe):
            add(f'<rect x="{x - 3}" y="{y0 + r * 14 - 3}" width="6" height="6" fill="#000" stroke="#4d4d4d"/>')
    text((xo + xe) / 2, y0 - 12, name, 10, "#666", "middle")
zio(100, 116, 300, 8, "CN8"); zio(100, 116, 430, 15, "CN9")
zio(264, 280, 300, 10, "CN7"); zio(264, 280, 460, 17, "CN10")
pin = lambda xo, xe, y0, p: ((xo if p % 2 else xe), y0 + ((p - 1) // 2) * 14)
CN10 = lambda p: pin(264, 280, 460, p)
CN8 = lambda p: pin(100, 116, 300, p)
add('<rect x="150" y="570" width="80" height="80" rx="4" fill="#2b2b2b"/>')
text(190, 606, "STM32", 12, "#eee", "middle", "bold"); text(190, 622, "F439ZI", 12, "#eee", "middle", "bold")
text(190, 444, "NUCLEO-F439ZI", 15, "#1a237e", "middle", "bold")
for i, c in enumerate(("#43a047", "#1e88e5", "#e53935")):
    add(f'<rect x="{160 + i * 20}" y="700" width="10" height="6" fill="{c}"/>')
text(190, 724, "LD1  LD2  LD3", 9, "#888", "middle")
add('<circle cx="110" cy="800" r="13" fill="#1565c0" stroke="#0d3c84" stroke-width="2"/>'); text(110, 830, "USER", 9, "#666", "middle")
add('<circle cx="270" cy="800" r="13" fill="#222" stroke="#000" stroke-width="2"/>'); text(270, 830, "RESET", 9, "#666", "middle")

# breadboard
add('<rect x="474" y="262" width="632" height="388" rx="8" fill="#f1f1f1" stroke="#c8c8c8" stroke-width="2"/>')
add('<rect x="480" y="448" width="620" height="16" fill="#dadada"/>')
for y, col in ((281, "#e53935"), (323, "#1e88e5"), (589, "#1e88e5"), (631, "#e53935")):
    add(f'<line x1="490" y1="{y}" x2="1092" y2="{y}" stroke="{col}" stroke-width="2"/>')
for name, y in ROW.items():
    for c in range(1, 31):
        add(f'<rect x="{X(c) - 3}" y="{y - 3}" width="6" height="6" rx="1" fill="#4a4a4a"/>')
    if len(name) == 1:
        text(484, y + 4, name, 10, "#999", "middle")
text(486, 297, "+", 13, "#e53935", "middle", "bold"); text(486, 316, "−", 13, "#1e88e5", "middle", "bold")
text(486, 604, "−", 13, "#1e88e5", "middle", "bold"); text(486, 625, "+", 13, "#e53935", "middle", "bold")
for c in (1, 5, 10, 15, 20, 25, 30):
    text(X(c), 344, str(c), 9, "#9a9a9a", "middle"); text(X(c), 577, str(c), 9, "#9a9a9a", "middle")
text(1114, 297, "12 V", 13, "#c62828", weight="bold"); text(1114, 317, "GND", 13, "#222", weight="bold")
text(1114, 605, "GND", 13, "#222", weight="bold"); text(1114, 625, "3.3 V", 13, "#b8860b", weight="bold")

# DRV8825 (180 degree view: VMOT top left, EN bottom left)
add('<rect x="708" y="424" width="164" height="64" rx="3" fill="#4a1f7a" stroke="#2e1250" stroke-width="2"/>')
top = ["VMOT", "GND", "B2", "B1", "A1", "A2", "FLT", "GND"]
bot = ["EN", "M0", "M1", "M2", "RST", "SLP", "STEP", "DIR"]
for k in range(8):
    x = X(12 + k)
    add(f'<circle cx="{x}" cy="436" r="3.5" fill="#d4af37"/>'); add(f'<circle cx="{x}" cy="476" r="3.5" fill="#d4af37"/>')
    fs = lambda t: 6.3 if len(t) > 3 else 7.5
    text(x, 451, top[k], fs(top[k]), "#fff", "middle", "bold"); text(x, 469, bot[k], fs(bot[k]), "#fff", "middle", "bold")
text(884, 456, "DRV8825 driver", 14, "#4a1f7a", weight="bold")
text(884, 472, "chip side up, VMOT and EN in column 12", 11, "#6a4a8a")

# 10 kOhm resistor EN to 3.3 V (column 12, row a to bottom + rail)
add(f'<line x1="{X(12)}" y1="{ROW["a"]}" x2="{X(12)}" y2="{ROW["bot+"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
add(f'<rect x="{X(12) - 7}" y="566" width="14" height="38" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
for y, c in ((573, "#8d4e2b"), (580, "#111"), (587, "#ef6c00"), (597, "#c9a227")):
    add(f'<rect x="{X(12) - 7}" y="{y}" width="14" height="3.5" fill="{c}"/>')
for y in (ROW["a"], ROW["bot+"]):
    add(f'<circle cx="{X(12)}" cy="{y}" r="3.5" fill="#757575"/>')
text(X(12) + 11, 590, "10 kΩ", 11, "#6d5a2a", "start", "bold")

# 1000 uF capacitor on the 12 V rails: + leg column 10, minus leg column 7
add(f'<line x1="666" y1="254" x2="{X(10)}" y2="{ROW["top+"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
add(f'<line x1="654" y1="254" x2="{X(7)}" y2="{ROW["top-"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
add('<rect x="646" y="212" width="28" height="44" rx="6" fill="#1f2f74"/>')
add('<rect x="646" y="212" width="9" height="44" rx="3" fill="#9fb0e8"/>')
for y in (222, 234, 246):
    add(f'<line x1="648" y1="{y}" x2="653" y2="{y}" stroke="#1f2f74" stroke-width="2"/>')
add('<ellipse cx="660" cy="213" rx="14" ry="4" fill="#3a4c9a"/>')
for x, y in ((X(10), ROW["top+"]), (X(7), ROW["top-"])):
    add(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
text(684, 226, "1000 µF", 12, "#1f2f74", weight="bold"); text(684, 241, "long leg (+) on 12 V", 11, "#1f2f74")

# DC jack module and adapter
add('<rect x="352" y="165" width="100" height="50" rx="8" fill="#263238"/>')
text(402, 188, "12 V 2 A", 13, "#fff", "middle", "bold"); text(402, 204, "adapter", 11, "#cfd8dc", "middle")
text(402, 232, "plug in last", 11, "#c62828", "middle", "bold")
add('<path d="M452,190 C470,190 472,195 490,195" fill="none" stroke="#111" stroke-width="6"/>')
add('<rect x="488" y="164" width="114" height="62" rx="4" fill="#1565c0"/>')
add('<rect x="488" y="178" width="42" height="34" rx="4" fill="#212121"/>')
add('<circle cx="509" cy="195" r="7" fill="#555"/>')
add('<rect x="540" y="182" width="56" height="40" rx="3" fill="#2e7d32"/>')
for x in (554, 582):
    add(f'<circle cx="{x}" cy="200" r="8" fill="#bdbdbd" stroke="#757575"/>')
    add(f'<line x1="{x - 5}" y1="200" x2="{x + 5}" y2="200" stroke="#616161" stroke-width="2"/>')
text(554, 178, "−", 13, "#fff", "middle", "bold"); text(582, 178, "+", 13, "#fff", "middle", "bold")
text(545, 158, "DC jack", 12, "#1565c0", "middle", "bold")

# NEMA 17 motor, connector on its left face, pins aligned with rows j, i, h, g
add('<rect x="1190" y="326" width="140" height="44" fill="#bdbdbd" stroke="#8a8a8a"/>')
add('<rect x="1190" y="370" width="140" height="56" fill="#3a3a3a"/>')
add('<rect x="1190" y="426" width="140" height="44" fill="#bdbdbd" stroke="#8a8a8a"/>')
add('<rect x="1330" y="372" width="10" height="52" fill="#9e9e9e"/>')
add('<rect x="1340" y="391" width="42" height="14" rx="2" fill="#cfcfcf" stroke="#9e9e9e"/>')
add('<rect x="1170" y="342" width="20" height="88" rx="2" fill="#f5f5f5" stroke="#9e9e9e"/>')
text(1260, 312, "NEMA 17 stepper motor", 14, "#c62828", "middle", "bold")
text(1260, 492, "17HS4401, 12 V", 12, "#555", "middle")
text(1260, 508, "cable colours vary by brand:", 11, "#555", "middle")
text(1260, 522, "find the two coil pairs first", 11, "#555", "middle")

# wires
# power side (top rails = 12 V)
wire(f"M{X(1)},{ROW['top-']} L{X(1)},{ROW['bot-']}", BLACK, [(X(1), ROW['top-']), (X(1), ROW['bot-'])])
wire(f"M554,222 C554,262 {X(2)},270 {X(2)},{ROW['top-']}", BLACK, [(X(2), ROW['top-'])])
wire(f"M582,222 C582,262 {X(3)},262 {X(3)},{ROW['top+']}", RED, [(X(3), ROW['top+'])])
wire(f"M{X(12)},{ROW['j']} L{X(12)},{ROW['top+']}", RED, [(X(12), ROW['j']), (X(12), ROW['top+'])])
wire(f"M{X(13)},{ROW['j']} L{X(13)},{ROW['top-']}", BLACK, [(X(13), ROW['j']), (X(13), ROW['top-'])])
# motor cable: coil A black (A1) and green (A2), coil B red (B1) and blue (B2)
for c, r, col in ((17, "j", GREEN), (16, "i", BLACK), (15, "h", RED), (14, "g", BLUE)):
    wire(f"M1170,{ROW[r]} L{X(c)},{ROW[r]}", col, [(X(c), ROW[r])])
    add(f'<rect x="1166" y="{ROW[r] - 4}" width="8" height="8" fill="{col[1]}"/>')
# control side (bottom rails = 3.3 V)
for c in (15, 16, 17):
    wire(f"M{X(c)},{ROW['a']} L{X(c)},{ROW['bot+']}", YELLOW, [(X(c), ROW['a']), (X(c), ROW['bot+'])])
x, y = CN8(7)
wire(f"M{x},{y} C40,{y} 22,380 22,440 L22,866 C22,886 40,892 64,892 L430,892 C492,892 {X(2)},820 {X(2)},{ROW['bot+']}", YELLOW, [(x, y), (X(2), ROW['bot+'])])
x, y = CN10(5)
wire(f"M{x},{y} C380,{y} 470,{ROW['bot-']} {X(3)},{ROW['bot-']}", BLACK, [(x, y), (X(3), ROW['bot-'])])
x, y = CN10(12)
wire(f"M{x},{y} C430,{y} 560,{ROW['b']} {X(12)},{ROW['b']}", BLUEGREY, [(x, y), (X(12), ROW['b'])])
x, y = CN10(4)
wire(f"M{x},{y} C440,{y} 620,{ROW['c']} {X(18)},{ROW['c']}", GREY, [(x, y), (X(18), ROW['c'])])
x, y = CN10(2)
wire(f"M{x},{y} C440,{y} 600,{ROW['d']} {X(19)},{ROW['d']}", BROWN, [(x, y), (X(19), ROW['d'])])

# Nucleo pin labels
for p, lab, col in ((2, "D7 · PF13 (pin 2)", BROWN), (4, "D6 · PE9 (pin 4)", GREY), (5, "GND (pin 5)", BLACK), (12, "D2 · PF15 (pin 12)", BLUEGREY)):
    x, y = CN10(p)
    add(f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{col[1]}" stroke-width="2"/>')
    text(252 if p != 5 else 252, y + 4, lab, 10, col[1], "end", "bold")
x, y = CN8(7)
add(f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{YELLOW[1]}" stroke-width="2"/>')
text(128, y + 4, "3V3 (CN8 pin 7)", 10, YELLOW[1], weight="bold")

# notes
add('<rect x="640" y="672" width="760" height="330" rx="10" fill="#fafafa" stroke="#dddddd"/>')
text(660, 700, "WIRE COLOURS", 14, "#c62828", weight="bold")
rows = [(RED, "12 V"), (BLACK, "GND"), (YELLOW, "3.3 V"), (GREY, "STEP: Nucleo D6 · PE9"),
        (BROWN, "DIR: Nucleo D7 · PF13"), (BLUEGREY, "EN: Nucleo D2 · PF15")]
for i, (col, lab) in enumerate(rows):
    y = 724 + i * 22
    add(f'<line x1="662" y1="{y - 4}" x2="700" y2="{y - 4}" stroke="{col[1]}" stroke-width="7" stroke-linecap="round"/>')
    add(f'<line x1="662" y1="{y - 4}" x2="700" y2="{y - 4}" stroke="{col[0]}" stroke-width="4.5" stroke-linecap="round"/>')
    text(712, y, lab, 12.5)
text(662, 862, "Motor cable: black + green = coil A (A1, A2)", 12.5)
text(662, 880, "red + blue = coil B (B1, B2)", 12.5)

text(1010, 700, "DRIVER SETTINGS", 14, "#c62828", weight="bold")
for i, s in enumerate(["M2 to 3.3 V, M0 and M1 open: 1/16 step,", "  so 3200 steps per motor turn",
                       "SLP and RST to 3.3 V: driver awake",
                       "10 kΩ on EN: motor stays off until the", "  STM32 sets PF15 low",
                       "Current: about 0.5 V on the potentiometer", "  (Vref) gives 1 A",
                       "FLT and the GND above DIR: no wire needed"]):
    text(1010, 724 + i * 20, s, 12.5)

text(660, 912, "SAFETY", 14, "#c62828", weight="bold")
for i, s in enumerate(["1. Wire everything with the adapter and the USB unplugged.",
                       "2. Top + rail is 12 V, bottom + rail is 3.3 V: mark them with tape.",
                       "3. Never plug or unplug the motor while 12 V is on."]):
    text(662, 936 + i * 20, s, 12.5)
for i, s in enumerate(["4. Power on: USB first, then the adapter.",
                       "5. Power off: adapter first, then the USB.",
                       "6. Check every Nucleo pin label before plugging."]):
    text(1080, 936 + i * 20, s, 12.5)
text(40, 1004, "Kibbly hardware · circuit 1 of the circuits by part · wires V1 to V22 in hardware/04_wiring_list.md section 6B", 11, "#9e9e9e")
add("</svg>")
open(sys.argv[1], "w", encoding="utf8").write("\n".join(out))
