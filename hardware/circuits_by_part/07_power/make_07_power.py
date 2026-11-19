"""Draw hardware/circuits_by_part/07_power/07_power.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import BLACK, CN8, CN10, CN11, ORANGE, RED, ROW, YELLOW, Drawing, X  # noqa: E402

d = Drawing(1880, 960)
a, t = d.add, d.text
d.title("PART 7: POWER (12 V, 5 V AND 3.3 V)",
        "One adapter feeds everything: 12 V for the motor, 5 V on the top rail from the XL4015, 3.3 V on the bottom rail from the Nucleo.")
d.nucleo([(CN8(9), "5V (CN8 pin 9): R1 out", RED, "right"), (CN8(7), "3V3 (CN8 pin 7)", YELLOW, "right"),
          (CN10(5), "GND (pin 5)", BLACK, "left"), (CN11(6), "E5V (CN11 pin 6)", ORANGE, "right", (96, 244))])
d.breadboard()

# 12 V: adapter, DC jack, the driver column (circuit 1)
d.twelve_volt_column()
d.driver_capacitor(labels=False)
t(594, 232, "470 µF (circuit 1)", 10, "#1f2f74", weight="bold")
d.dc_jack()
t(490, 134, "DC jack", 9, "#fff", "middle", "bold")
a(f'<rect x="{X(6) - 6}" y="{ROW["i"] - 10}" width="262" height="20" rx="4" fill="#ffffff" stroke="#e57373"/>')
t(X(6), ROW["i"] + 4, "← 12 V column: the driver VMOT (circuit 1)", 10, "#c62828", weight="bold")
d.wire(f"M534,186 C534,250 {X(3)},262 {X(3)},290 L{X(3)},{ROW['top-']}", BLACK, [(X(3), ROW['top-'])])
d.wire(f"M564,186 C564,198 548,198 548,212 L548,404 C548,412 552,{ROW['g']} {X(4)},{ROW['g']} L{X(5)},{ROW['g']}",
       RED, [(X(5), ROW['g'])])

# XL4015 buck converter above columns 8 to 19: IN on the left end, OUT on the right end
x1, x2, y1, y2 = 640, 880, 104, 204
a(f'<rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" rx="5" fill="#1e3a8a" stroke="#0f1f4d" stroke-width="2"/>')
a('<rect x="694" y="118" width="70" height="70" rx="10" fill="#37474f"/>')
a('<circle cx="729" cy="153" r="24" fill="#b87333" stroke="#8d5524" stroke-width="3"/>')
a('<circle cx="729" cy="153" r="9" fill="#37474f"/>')
a('<rect x="774" y="116" width="44" height="40" rx="2" fill="#cfd8dc" stroke="#90a4ae"/>')
for k in range(4):
    a(f'<line x1="{781 + k * 10}" y1="118" x2="{781 + k * 10}" y2="154" stroke="#90a4ae" stroke-width="2"/>')
a('<rect x="774" y="164" width="44" height="26" rx="2" fill="#1e88e5" stroke="#0d47a1"/>')
a('<circle cx="786" cy="177" r="5" fill="#d4af37" stroke="#8d6e00"/>')
t(806, 181, "5 V", 8, "#fff", "middle", "bold")
pads = {"IN−": (652, 128), "IN+": (652, 172), "OUT+": (868, 128), "OUT−": (868, 172)}
for name, (x, y) in pads.items():
    a(f'<circle cx="{x}" cy="{y}" r="7" fill="#d4af37" stroke="#8d6e00"/>')
    left = name.startswith("IN")
    t(x + 12 if left else x - 12, y + 4, name, 9, "#fff", "start" if left else "end", "bold")
t(780, 94, "XL4015 buck converter: 12 V in, 5.0 V out", 13, "#c62828", "middle", "bold")
t(916, 132, "Set it to 5.0 V first:", 12, "#c62828", weight="bold")
d.lines(916, 150, ["turn the screw of the blue box", "until OUT reads 5.0 V, with",
                   "nothing on OUT. A new board", "can give up to 12 V."], 15, 11)

# 12 V into the XL4015: second wire in each screw of the DC jack
d.wire(f"M534,142 L534,108 C534,102 538,100 544,100 L612,100 C618,100 620,104 620,110 L620,120 C620,126 624,128 630,128 "
       f"L{pads['IN−'][0]},{pads['IN−'][1]}", BLACK, [pads["IN−"]])
d.wire(f"M564,142 L564,124 C564,118 568,116 574,116 L598,116 C604,116 606,120 606,126 L606,164 C606,170 610,172 616,172 "
       f"L{pads['IN+'][0]},{pads['IN+'][1]}", RED, [pads["IN+"]])

# 5 V out of the XL4015 into the top rails: OUT+ to top + column 13, OUT− to top − column 12
x, y = pads["OUT+"]
d.wire(f"M{x},{y} L894,{y} C898,{y} 900,{y + 4} 900,{y + 8} L900,254 C900,260 896,262 890,262 L{X(13) + 8},262 "
       f"C{X(13) + 2},262 {X(13)},266 {X(13)},272 L{X(13)},{ROW['top+']}", ORANGE, [(x, y), (X(13), ROW['top+'])])
x, y = pads["OUT−"]
d.wire(f"M{x},{y} L880,{y} C884,{y} 886,{y + 4} 886,{y + 8} L886,242 C886,248 882,250 876,250 L{X(12) + 8},250 "
       f"C{X(12) + 2},250 {X(12)},254 {X(12)},260 L{X(12)},{ROW['top-']}", BLACK, [(x, y), (X(12), ROW['top-'])])

# 3.3 V and GND from the Nucleo, as in every circuit
d.ground_link(1)
d.three_volt_feed(2)
d.ground_feed(3)

# E5V: only when the feeder runs alone (R1 out, JP3 on E5V); same rail hole as R1
x, y = CN11(6)
d.wire(f"M{x},{y} C80,{y} 86,{y - 6} 86,{y - 14} L86,262 C86,256 90,252 98,252 L{X(2) - 12},252 "
       f"C{X(2) - 4},252 {X(2)},258 {X(2)},266 L{X(2)},{ROW['top+']}", ORANGE, [(x, y), (X(2), ROW['top+'])], dash="10 6")
t(192, 244, "P6, dashed: only when the feeder runs alone", 10, "#a65c00", weight="bold")
d.nucleo_labels()
d.zones(7)

# notes
d.notes_box(640, 712, 1220, 230)
t(660, 740, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 764, [(RED, "12 V: jack + to column 5 and to XL4015 IN+"), (BLACK, "GND"),
                         (ORANGE, "5 V: XL4015 OUT+ to the top + rail"), (YELLOW, "3.3 V: Nucleo 3V3 to the bottom + rail")])
d.lines(662, 856, ["Dashed orange: top + rail to Nucleo E5V,",
                   "only when the feeder runs alone"], 18)
t(1060, 740, "SET THE XL4015 FIRST", 14, "#c62828", weight="bold")
d.lines(1060, 764, ["1. Adapter, jack and XL4015 only, OUT wires free.",
                    "2. Meter on OUT+ and OUT−. Turn the screw, many",
                    "turns, until it reads 5.0 V (4.95 to 5.10 V).",
                    "3. Unplug the adapter, then wire OUT to the rails.",
                    "No multimeter in the team: borrow one for this step.",
                    "Never connect OUT before it reads 5.0 V."])
t(1460, 740, "POWER ORDER", 14, "#c62828", weight="bold")
d.lines(1460, 764, ["R1 always out: never R1 with the XL4015.",
                    "Tests: Nucleo on USB (JP3 on U5V), no P6.",
                    "On: USB, then adapter. Off: adapter first.",
                    "Feeder alone: P6 in, JP3 on E5V, adapter only.",
                    "Logs then: USB after the adapter, out before it.",
                    "Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 7 of the circuits by part · wires P1 to P6 in hardware/04_wiring_list.md section 4, V1 to V3 in section 6B, rails R2 to R4 in section 4B")
d.save(sys.argv[1])
