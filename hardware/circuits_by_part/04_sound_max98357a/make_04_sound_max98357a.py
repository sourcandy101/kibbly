"""Draw hardware/circuits_by_part/04_sound_max98357a/04_sound_max98357a.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, CN7, CN8, CN10, DARKPURPLE, LIGHTPURPLE, ORANGE, PURPLE, RED, ROW,  # noqa: E402
                    Drawing, X)

d = Drawing(1420, 1020)
a, t = d.add, d.text
d.title("PART 4: SOUND, MAX98357A AMPLIFIER AND SPEAKER",
        "Test setup for step 3. Only the laptop USB is needed: the amplifier takes 5 V from the Nucleo 5V pin.")
d.nucleo([(CN8(6), "PC10 (pin 6)", PURPLE, "right", (174, 320)), (CN8(10), "PC12 (pin 10)", DARKPURPLE, "right", (174, 348)),
          (CN8(9), "5V (pin 9)", ORANGE, "right", (174, 376)),
          (CN7(17), "PA4 · D24 (pin 17)", LIGHTPURPLE, "left"), (CN10(5), "GND (pin 5)", BLACK, "left")])
d.breadboard(used=(False, False, True, False))
t(1114, 333, "(not used)", 10, "#b0b0b0")
t(1114, 641, "(not used)", 10, "#b0b0b0")

# MAX98357A breakout: 7 pins in row j, columns 5 to 11, board standing over the top edge
a('<rect x="566" y="196" width="148" height="168" rx="5" fill="#263238" stroke="#11171a" stroke-width="2"/>')
a('<rect x="612" y="202" width="56" height="30" rx="3" fill="#2e7d32"/>')
for x in (626, 654):
    a(f'<circle cx="{x}" cy="217" r="8" fill="#bdbdbd" stroke="#757575"/>')
    a(f'<line x1="{x - 5}" y1="217" x2="{x + 5}" y2="217" stroke="#616161" stroke-width="2"/>')
t(626, 250, "+", 13, "#fff", "middle", "bold")
t(654, 250, "−", 13, "#fff", "middle", "bold")
a('<rect x="624" y="268" width="32" height="32" rx="2" fill="#111"/>')
t(640, 318, "MAX98357A", 10, "#cfd8dc", "middle", "bold")
pins = ["LRC", "BCLK", "DIN", "GAIN", "SD", "GND", "Vin"]
for k, lab in enumerate(pins):
    x = X(5 + k)
    a(f'<rect x="{x - 4}" y="{ROW["j"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 342, lab, 6.3 if len(lab) > 3 else 7.5, "#fff", "middle", "bold")
t(500, 186, "MAX98357A amplifier", 14, "#c62828", "end", "bold")
t(500, 202, "pins in row j, columns 5 to 11", 11, "#555", "end")

# speaker
a('<circle cx="900" cy="186" r="64" fill="#37474f"/>')
for r, c in ((54, "#90a4ae"), (40, "#78909c"), (26, "#607d8b"), (14, "#455a64")):
    a(f'<circle cx="{900}" cy="186" r="{r}" fill="{c}"/>')
a('<rect x="828" y="168" width="10" height="10" fill="#c62828"/>')
a('<rect x="828" y="196" width="10" height="10" fill="#212121"/>')
t(980, 150, "Speaker", 14, "#c62828", weight="bold")
t(980, 168, "4 or 8 Ω, about 3 W", 11, "#555")
t(980, 184, "both wires go to the amplifier,", 11, "#555")
t(980, 200, "never to GND", 11, "#c62828", weight="bold")
d.wire("M626,209 C626,150 760,173 830,173", RED, [], width=3)
d.wire("M654,209 C654,182 760,201 830,201", BLACK, [], width=3)

# wires from the Nucleo: BCLK and DIN over the top of the board, LRC from the right header
x, y = CN8(6)
d.wire(f"M{x},{y} C134,{y} 150,320 150,300 L150,262 C150,250 158,246 170,246 L436,246 C450,246 456,254 456,268 "
       f"L456,364 C456,372 462,{ROW['i']} 470,{ROW['i']} L{X(6)},{ROW['i']}", PURPLE, [(x, y), (X(6), ROW['i'])])
x, y = CN8(10)
d.wire(f"M{x},{y} C140,{y} 162,350 162,330 L162,270 C162,262 166,258 174,258 L432,258 C440,258 444,264 444,272 "
       f"L444,384 C444,392 450,{ROW['h']} 458,{ROW['h']} L{X(7)},{ROW['h']}", DARKPURPLE, [(x, y), (X(7), ROW['h'])])
x, y = CN7(17)
d.wire(f"M{x},{y} C360,{y} 420,{ROW['g']} 480,{ROW['g']} L{X(5)},{ROW['g']}", LIGHTPURPLE, [(x, y), (X(5), ROW['g'])])
# 5 V around the board to column 11 bottom half, then a jumper across the middle gap to Vin
x, y = CN8(9)
d.wire(f"M{x},{y} C40,{y} 30,400 30,460 L30,872 C30,890 48,898 70,898 L400,898 C428,898 436,880 436,850 "
       f"L436,540 C436,524 444,{ROW['c']} 460,{ROW['c']} L{X(11)},{ROW['c']}", ORANGE, [(x, y), (X(11), ROW['c'])])
d.wire(f"M{X(11)},{ROW['f']} L{X(11)},{ROW['e']}", ORANGE, [(X(11), ROW['f']), (X(11), ROW['e'])])
# GND: jumper across the gap in column 10, then to the bottom rail
d.wire(f"M{X(10)},{ROW['f']} L{X(10)},{ROW['e']}", BLACK, [(X(10), ROW['f']), (X(10), ROW['e'])])
d.wire(f"M{X(10)},{ROW['a']} L{X(10)},{ROW['bot-']}", BLACK, [(X(10), ROW['a']), (X(10), ROW['bot-'])])
x, y = CN10(5)
d.wire(f"M{x},{y} C380,{y} 470,{ROW['bot-']} {X(3)},{ROW['bot-']}", BLACK, [(x, y), (X(3), ROW['bot-'])])
d.nucleo_labels()
t(X(12) + 6, ROW["f"] + 24, "2 jumpers across the gap: 5 V and GND", 11, "#555")

# notes
d.notes_box(640, 672, 760, 330)
t(660, 700, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 724, [(ORANGE, "5 V: Nucleo 5V pin"), (BLACK, "GND"), (PURPLE, "BCLK: Nucleo PC10"),
                         (DARKPURPLE, "DIN: Nucleo PC12"), (LIGHTPURPLE, "LRC: Nucleo PA4")])
d.lines(662, 840, ["Speaker cable: red +, black −", "GAIN and SD: no wire"], 18)
t(1010, 700, "SETTINGS", 14, "#c62828", weight="bold")
d.lines(1010, 724, ["GAIN open: 9 dB (to GND: 12 dB, louder)",
                    "SD open: plays a mono mix",
                    "Sound files: WAV, 16 kHz, 16 bit, mono",
                    "Demo: 2 or 3 short clips stored in the",
                    "  STM32 memory, no SD card needed",
                    "On USB power keep the volume low; full",
                    "  volume needs the 5 V supply (circuit 7)"])
t(660, 892, "TIPS", 14, "#c62828", weight="bold")
d.lines(662, 916, ["1. Wire everything with the USB unplugged.",
                   "2. Never connect a speaker wire to GND.",
                   "3. Vin on 5 V: louder and cleaner than 3.3 V."])
d.lines(1080, 916, ["4. The STM32 sends the sound as numbers (I2S).",
                    "5. Sound crackles: check the GND wires first.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 4 of the circuits by part · wires A1 to A12 in hardware/04_wiring_list.md section 11")
d.save(sys.argv[1])
