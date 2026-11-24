"""Draw hardware/circuits_by_part/10_button_led/10_button_led.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import BLACK, BROWN, CN7, CN10, GREY, ROW, Drawing, X  # noqa: E402

d = Drawing(1880, 1160)
a, t = d.add, d.text
d.title("PART 10: PUSH BUTTON AND STATUS LED",
        "Test setup for step 3. Only the laptop USB is needed: the button uses the STM32 internal pull up, the LED is driven by a pin.")
d.nucleo([(CN7(20), "D8 · PF12 (pin 20)", GREY, "left", (150, 410)), (CN10(5), "GND (pin 5)", BLACK, "left"),
          (CN10(14), "D1 · PG14 (pin 14)", BROWN, "left")])
d.breadboard(used=(False, False, True, False))

# 330 ohm resistor lying flat in row c, from column 44 (PG14) to column 47 (LED long leg)
x1, x2, y = X(44), X(47), ROW["c"]
a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<rect x="{x1 + 11}" y="{y - 7}" width="{x2 - x1 - 22}" height="14" rx="6" fill="#e8d5a3" stroke="#b39b62"/>')
for k, col in enumerate(["#ef6c00", "#ef6c00", "#8d4e2b"]):
    a(f'<rect x="{x1 + 16 + k * 6}" y="{y - 7}" width="3" height="14" fill="{col}"/>')
a(f'<rect x="{x2 - 17}" y="{y - 7}" width="3" height="14" fill="#c9a227"/>')
for x in (x1, x2):
    a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
a(f'<rect x="{(x1 + x2) / 2 - 18}" y="{y - 22}" width="36" height="13" rx="3" fill="#ffffff" stroke="#d7ccc8"/>')
t((x1 + x2) / 2, y - 12, "330 Ω", 10, "#6d5a2a", "middle", "bold")

# LED standing in column 47: long leg (+) in row a, short leg in the bottom − rail
lx = X(47)
a(f'<line x1="{lx}" y1="{ROW["a"]}" x2="{lx}" y2="{ROW["bot-"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
a(f'<circle cx="{lx}" cy="578" r="10" fill="#e53935" stroke="#b71c1c" stroke-width="2"/>')
a(f'<circle cx="{lx - 3}" cy="575" r="3" fill="#ffcdd2"/>')
a(f'<line x1="{lx - 10}" y1="586" x2="{lx + 10}" y2="586" stroke="#b71c1c" stroke-width="2"/>')
for yy in (ROW["a"], ROW["bot-"]):
    a(f'<circle cx="{lx}" cy="{yy}" r="3.5" fill="#757575"/>')
a(f'<rect x="{X(39) - 4}" y="664" width="164" height="34" rx="4" fill="#ffffff" stroke="#e57373"/>')
t(X(39) + 2, 678, "LED: long leg (+) in row a,", 10, "#c62828", weight="bold")
t(X(39) + 2, 692, "short leg (flat side) in the rail", 10, "#c62828")
a(f'<line x1="{X(46) + 2}" y1="664" x2="{lx - 6}" y2="590" stroke="#e57373" stroke-width="1.2"/>')

# push button (12 mm, panel mount) outside the board: one wire into column 49, one to the bottom − rail
bx, by = X(51), 760
a(f'<rect x="{bx - 34}" y="{by - 18}" width="68" height="36" rx="6" fill="#455a64" stroke="#263238" stroke-width="2"/>')
a(f'<circle cx="{bx}" cy="{by}" r="14" fill="#e53935" stroke="#b71c1c" stroke-width="2"/>')
a(f'<circle cx="{bx - 4}" cy="{by - 4}" r="4" fill="#ef9a9a"/>')
for ox in (-10, 10):
    a(f'<rect x="{bx + ox - 3}" y="{by - 30}" width="6" height="12" fill="#bdbdbd" stroke="#757575"/>')
t(bx + 46, by - 6, "Push button, 12 mm, panel mount", 13, "#c62828", weight="bold")
t(bx + 46, by + 10, "on the feeder body, 2 wires soldered to it", 11, "#555")
t(bx + 46, by + 26, "Not soldered yet: touch the two wire ends together to test", 11, "#555")
d.wire(f"M{bx - 10},{by - 30} L{bx - 10},640 C{bx - 10},630 {bx - 10},620 {bx - 10},{ROW['c'] + 10} "
       f"C{bx - 10},{ROW['c'] + 4} {bx - 14},{ROW['c']} {bx - 20},{ROW['c']} L{X(49)},{ROW['c']}", GREY, [(X(49), ROW['c'])], width=3.5)
d.wire(f"M{bx + 10},{by - 30} L{bx + 10},{ROW['bot-'] + 30} C{bx + 10},{ROW['bot-'] + 12} {X(52)},{ROW['bot-'] + 12} "
       f"{X(52)},{ROW['bot-']}", BLACK, [(X(52), ROW['bot-'])], width=3.5)

# wires to the Nucleo: PF12 to column 49 (row e), PG14 to column 44 (row d), GND to the bottom − rail
d.ground_feed(3)
x, y = CN7(20)
d.wire(f"M{x},{y} C400,{y} 430,{ROW['e']} 480,{ROW['e']} L{X(49)},{ROW['e']}", GREY, [(x, y), (X(49), ROW['e'])])
x, y = CN10(14)
d.wire(f"M{x},{y} C410,{y} 440,{ROW['d']} 480,{ROW['d']} L{X(44)},{ROW['d']}", BROWN, [(x, y), (X(44), ROW['d'])])
d.nucleo_labels()
d.zones(10, 880)

# notes
d.notes_box(640, 918, 1220, 220)
t(660, 946, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 970, [(GREY, "Button: Nucleo D8 · PF12 to column 49"), (BROWN, "LED: Nucleo D1 · PG14 to column 44"),
                         (BLACK, "GND")])
d.lines(662, 1042, ["Button wires: one into column 49,", "the other to the bottom − rail (column 52)",
                    "No 3.3 V wire needed in this circuit"], 18)
t(1060, 946, "SETTINGS", 14, "#c62828", weight="bold")
d.lines(1060, 970, ["PF12: input, internal pull up, interrupt",
                    "on the falling edge: free 3.3 V, pressed 0 V",
                    "Bounce filtered in the code (50 ms), no capacitor",
                    "PG14: output, high = LED on",
                    "LED current: (3.3 − 2.0) V ÷ 330 Ω ≈ 4 mA",
                    "Resistor bands: orange, orange, brown"])
t(1460, 946, "WHAT THEY DO", 14, "#c62828", weight="bold")
d.lines(1460, 970, ["Button held 3 s: shut down",
                    "Button pressed 2 times: WiFi pairing",
                    "Button pressed 5 times: reset",
                    "LED on: WiFi connected",
                    "LED blinking: pairing",
                    "LED off: offline"])
d.footer("Kibbly hardware · circuit 10 of the circuits by part · wires B1 to B4 and L1 to L3 in hardware/04_wiring_list.md section 12, rail R3 in section 4B")
d.save(sys.argv[1])
