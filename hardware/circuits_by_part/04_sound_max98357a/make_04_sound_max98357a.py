"""Draw hardware/circuits_by_part/04_sound_max98357a/04_sound_max98357a.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, CN7, CN8, CN10, DARKPURPLE, LIGHTPURPLE, ORANGE, PURPLE, RED, ROW,  # noqa: E402
                    Drawing, X)

d = Drawing(1880, 960)
a, t = d.add, d.text
d.title("PART 4: SOUND, MAX98357A AMPLIFIER AND SPEAKER",
        "Test setup for step 3. Only the laptop USB is needed: the Nucleo 5V pin feeds the top + rail (5 V).")
d.nucleo([(CN8(6), "PC10 (pin 6)", PURPLE, "right", (174, 320)), (CN8(10), "PC12 (pin 10)", DARKPURPLE, "right", (174, 348)),
          (CN8(9), "5V (pin 9)", ORANGE, "right", (174, 376)),
          (CN7(17), "PA4 · D24 (pin 17)", LIGHTPURPLE, "left"), (CN10(5), "GND (pin 5)", BLACK, "left")])
d.breadboard(used=(True, True, True, False))

# MAX98357A breakout: 7 pins in row j, columns 15 to 21, board standing over the top edge
x1, x2 = X(15) - 14, X(21) + 14
cx = (x1 + x2) / 2
a(f'<rect x="{x1}" y="196" width="{x2 - x1}" height="168" rx="5" fill="#263238" stroke="#11171a" stroke-width="2"/>')
a(f'<rect x="{cx - 28}" y="202" width="56" height="30" rx="3" fill="#2e7d32"/>')
for x in (cx - 14, cx + 14):
    a(f'<circle cx="{x}" cy="217" r="8" fill="#bdbdbd" stroke="#757575"/>')
    a(f'<line x1="{x - 5}" y1="217" x2="{x + 5}" y2="217" stroke="#616161" stroke-width="2"/>')
t(cx - 14, 250, "+", 13, "#fff", "middle", "bold")
t(cx + 14, 250, "−", 13, "#fff", "middle", "bold")
a(f'<rect x="{cx - 16}" y="268" width="32" height="32" rx="2" fill="#111"/>')
t(cx, 318, "MAX98357A", 10, "#cfd8dc", "middle", "bold")
for k, lab in enumerate(["LRC", "BCLK", "DIN", "GAIN", "SD", "GND", "Vin"]):
    x = X(15 + k)
    a(f'<rect x="{x - 4}" y="{ROW["j"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 342, lab, 6.3 if len(lab) > 3 else 7.5, "#fff", "middle", "bold")
t(x1 - 12, 186, "MAX98357A amplifier", 14, "#c62828", "end", "bold")
t(x1 - 12, 202, "pins in row j, columns 15 to 21", 11, "#555", "end")

# speaker
sx, sy = x2 + 110, 172
a(f'<circle cx="{sx}" cy="{sy}" r="64" fill="#37474f"/>')
for r, c in ((54, "#90a4ae"), (40, "#78909c"), (26, "#607d8b"), (14, "#455a64")):
    a(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="{c}"/>')
a(f'<rect x="{sx - 72}" y="{sy - 18}" width="10" height="10" fill="#c62828"/>')
a(f'<rect x="{sx - 72}" y="{sy + 10}" width="10" height="10" fill="#212121"/>')
t(sx + 80, 140, "Speaker", 14, "#c62828", weight="bold")
t(sx + 80, 158, "4 or 8 Ω, about 3 W", 11, "#555")
t(sx + 80, 174, "both wires go to the amplifier,", 11, "#555")
t(sx + 80, 190, "never to GND", 11, "#c62828", weight="bold")
d.wire(f"M{cx - 14},209 C{cx - 14},150 {sx - 120},{sy - 13} {sx - 70},{sy - 13}", RED, [], width=3)
d.wire(f"M{cx + 14},209 C{cx + 14},182 {sx - 120},{sy + 15} {sx - 70},{sy + 15}", BLACK, [], width=3)

# 5 V and GND straight from the top rails (columns 23 and 24, just right of the board)
d.wire(f"M{X(20)},{ROW['i']} L{X(23) - 12},{ROW['i']} C{X(23) - 4},{ROW['i']} {X(23)},{ROW['i'] - 6} {X(23)},{ROW['i'] - 16} "
       f"L{X(23)},{ROW['top-']}", BLACK, [(X(20), ROW['i']), (X(23), ROW['top-'])])
d.wire(f"M{X(21)},{ROW['h']} L{X(24) - 12},{ROW['h']} C{X(24) - 4},{ROW['h']} {X(24)},{ROW['h'] - 6} {X(24)},{ROW['h'] - 16} "
       f"L{X(24)},{ROW['top+']}", ORANGE, [(X(21), ROW['h']), (X(24), ROW['top+'])])

# I2S wires: BCLK and DIN over the top of the Nucleo, LRC from the right header
x, y = CN8(6)
d.wire(f"M{x},{y} C134,{y} 150,320 150,300 L150,262 C150,250 158,246 170,246 L436,246 C450,246 456,254 456,268 "
       f"L456,364 C456,372 462,{ROW['i']} 470,{ROW['i']} L{X(16)},{ROW['i']}", PURPLE, [(x, y), (X(16), ROW['i'])])
x, y = CN8(10)
d.wire(f"M{x},{y} C140,{y} 162,350 162,330 L162,270 C162,262 166,258 174,258 L432,258 C440,258 444,264 444,272 "
       f"L444,384 C444,392 450,{ROW['h']} 458,{ROW['h']} L{X(17)},{ROW['h']}", DARKPURPLE, [(x, y), (X(17), ROW['h'])])
x, y = CN7(17)
d.wire(f"M{x},{y} C360,{y} 420,{ROW['g']} 480,{ROW['g']} L{X(15)},{ROW['g']}", LIGHTPURPLE, [(x, y), (X(15), ROW['g'])])
d.five_volt_feed(2)
d.ground_link(1)
d.ground_feed(3)
d.nucleo_labels()
d.zones(4)

# notes
d.notes_box(640, 712, 1220, 230)
t(660, 740, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 764, [(ORANGE, "5 V: Nucleo 5V to the top + rail; Vin"), (BLACK, "GND"),
                         (PURPLE, "BCLK: Nucleo PC10"), (DARKPURPLE, "DIN: Nucleo PC12"),
                         (LIGHTPURPLE, "LRC: Nucleo PA4")])
d.lines(662, 880, ["Speaker cable: red +, black −. GAIN and SD: no wire"], 18)
t(1060, 740, "SETTINGS", 14, "#c62828", weight="bold")
d.lines(1060, 764, ["GAIN open: 9 dB (to GND: 12 dB, louder)",
                    "SD open: plays a mono mix",
                    "Sound files: WAV, 16 kHz, 16 bit, mono",
                    "Demo: 2 or 3 short clips in the STM32 memory,",
                    "no SD card needed",
                    "On USB power keep the volume low; full volume",
                    "needs the 5 V supply (circuit 7)"])
t(1460, 740, "TIPS", 14, "#c62828", weight="bold")
d.lines(1460, 764, ["1. Wire everything with the USB unplugged.",
                    "2. Never connect a speaker wire to GND.",
                    "3. Vin on 5 V: louder and cleaner than 3.3 V.",
                    "4. The STM32 sends the sound as numbers (I2S).",
                    "5. Sound crackles: check the GND wires first.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 4 of the circuits by part · wires A1 to A9 in hardware/04_wiring_list.md section 11, rails R1, R3 and R4 in section 4B")
d.save(sys.argv[1])
