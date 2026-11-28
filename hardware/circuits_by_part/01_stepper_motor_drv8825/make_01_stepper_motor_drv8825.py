"""Draw hardware/circuits_by_part/01_stepper_motor_drv8825/01_stepper_motor_drv8825.svg (Fritzing style).

The DRV8825 sits on its carrier board (Keyes 4988 PCB) above the breadboard. The 12 V goes from the DC jack
straight to the carrier; only the control wires and the carrier GND reach the breadboard.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, BLUE, BLUEGREY, BROWN, CARRIER_MOTOR, CARRIER_PINS, CN8, CN10, GREEN, GREY,  # noqa: E402
                    RED, ROW, YELLOW, Drawing, X)

DY = 340  # the drawing is shifted down to leave room for the carrier and the motor above the board
d = Drawing(1880, 960 + DY)
a, t = d.add, d.text
d.title("PART 1: STEPPER MOTOR AND DRV8825 DRIVER ON ITS CARRIER BOARD",
        "Test setup for step 3. The Nucleo runs from the laptop USB; the 12 V adapter goes straight to the carrier board, never into the breadboard.")
a(f'<g transform="translate(0,{DY})">')
d.nucleo([(CN10(2), "D7 · PF13 (pin 2)", BROWN, "left"), (CN10(4), "D6 · PE9 (pin 4)", GREY, "left"),
          (CN10(5), "GND (pin 5)", BLACK, "left"), (CN10(12), "D2 · PF15 (pin 12)", BLUEGREY, "left"),
          (CN8(7), "3V3 (CN8 pin 7)", YELLOW, "right")])
d.breadboard(used=(False, True, True, True))

# adapter, DC jack and the carrier with the DRV8825
d.dc_jack()
t(527, 116, "DC jack", 12, "#1565c0", "middle", "bold")
d.carrier()
t(458, -92, "DRV8825 on its carrier board", 13, "#c62828", "end", "bold")
t(458, -74, "Keyes 4988 PCB, off the breadboard", 11, "#555", "end")
t(458, -58, "plug the DRV8825 in by its labels:", 11, "#555", "end")
t(458, -44, "EN on EN, VMOT on VMOT", 11, "#555", "end")
t(458, -26, "switches: 1 OFF, 2 OFF, 3 ON (1/16 step)", 11, "#555", "end")
t(458, -10, "Vref 0.50 V on the DRV8825 (1 A)", 11, "#555", "end")
t(716, 30, "match every pin by the name printed next to it", 10, "#555")

# NEMA 17 motor right of the carrier; its 4 wires plug into the carrier motor connector
mx, my = 800, -236
a(f'<rect x="{mx}" y="{my}" width="124" height="116" rx="10" fill="#bdbdbd" stroke="#8a8a8a" stroke-width="2"/>')
for cx, cy in ((mx + 14, my + 14), (mx + 110, my + 14), (mx + 14, my + 102), (mx + 110, my + 102)):
    a(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#757575"/>')
a(f'<circle cx="{mx + 62}" cy="{my + 58}" r="26" fill="#9e9e9e" stroke="#757575" stroke-width="2"/>')
a(f'<circle cx="{mx + 62}" cy="{my + 58}" r="7" fill="#e0e0e0" stroke="#757575"/>')
a(f'<rect x="{mx - 16}" y="{my + 20}" width="16" height="76" rx="2" fill="#f5f5f5" stroke="#9e9e9e"/>')
t(940, -200, "NEMA 17 stepper motor", 14, "#c62828", weight="bold")
t(940, -182, "17HS4401, 12 V", 12, "#555")
t(940, -164, "coil A: black and green on 1A and 1B", 11, "#555")
t(940, -148, "coil B: red and blue on 2A and 2B", 11, "#555")
t(940, -132, "find the pairs first: about 1.5 to 2 Ω", 11, "#555")
for name, colour, yl in (("2B", BLUE, -196), ("2A", RED, -180), ("1A", BLACK, -164), ("1B", GREEN, -148)):
    x, y = CARRIER_MOTOR[name]
    d.wire(f"M{x},{y} L{x},{yl + 8} C{x},{yl + 2} {x + 4},{yl} {x + 10},{yl} L{mx - 16},{yl}", colour, [], width=3.5)

# power: V1 jack + straight to the carrier Vin; V2 jack − and V5 carrier GND to the top − rail
d.ground_link(1)
d.wire(f"M534,186 C534,250 {X(3)},262 {X(3)},290 L{X(3)},{ROW['top-']}", BLACK, [(X(3), ROW['top-'])])
vx, vy = CARRIER_PINS["Vin"]
d.wire(f"M564,186 L564,196 C564,202 568,204 574,204 L{vx - 10},204 C{vx - 4},204 {vx},200 {vx},194 L{vx},{vy}", RED, [])
gx, gy = CARRIER_PINS["GND"]
d.wire(f"M{gx},{gy} L{gx},{ROW['top-']}", BLACK, [(gx, ROW['top-'])])

# carrier pins straight down into the bottom half, row e: 5V to column 8, E to 9, D to 10, S to 11
for name, col, colour in (("5V", 8, YELLOW), ("E", 9, BLUEGREY), ("D", 10, BROWN), ("S", 11, GREY)):
    x, y = CARRIER_PINS[name]
    d.wire(f"M{x},{y} L{X(col)},{ROW['e']}", colour, [(X(col), ROW['e'])])
# column 8 to the 3.3 V rail (feeds the carrier 5V pin), 10 kohm from EN (column 9) to the 3.3 V rail
d.wire(f"M{X(8)},{ROW['a']} L{X(8)},{ROW['bot+']}", YELLOW, [(X(8), ROW['a']), (X(8), ROW['bot+'])])
d.pull_up_10k(9)

# Nucleo: rails and the three control wires
d.three_volt_feed(2)
d.ground_feed(3)
x, y = CN10(12)
d.wire(f"M{x},{y} C400,{y} 470,{ROW['b']} {X(9)},{ROW['b']}", BLUEGREY, [(x, y), (X(9), ROW['b'])])
x, y = CN10(4)
d.wire(f"M{x},{y} C430,{y} 560,{ROW['c']} {X(11)},{ROW['c']}", GREY, [(x, y), (X(11), ROW['c'])])
x, y = CN10(2)
d.wire(f"M{x},{y} C430,{y} 540,{ROW['d']} {X(10)},{ROW['d']}", BROWN, [(x, y), (X(10), ROW['d'])])
d.nucleo_labels()
d.zones(1)

# notes
d.notes_box(640, 712, 1220, 230)
t(660, 740, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 764, [(RED, "12 V: DC jack + to the carrier Vin only"), (BLACK, "GND"),
                         (YELLOW, "3.3 V, also into the carrier 5V pin"),
                         (GREY, "STEP: carrier S, Nucleo D6 · PE9"),
                         (BROWN, "DIR: carrier D, Nucleo D7 · PF13"),
                         (BLUEGREY, "EN: carrier E, Nucleo D2 · PF15")])
t(1060, 740, "DRIVER SETTINGS", 14, "#c62828", weight="bold")
d.lines(1060, 764, ["Switches 1 OFF, 2 OFF, 3 ON: 1/16 step, 3200 per turn",
                    "Carrier 5V pin on 3.3 V: it only feeds the switches",
                    "10 kΩ on EN: motor off until PF15 goes low",
                    "Current: 0.50 V on the potentiometer = 1 A",
                    "RST and SLP: held high by the carrier (check 2)",
                    "Motor: black + green = coil A, red + blue = coil B"])
t(1460, 740, "SAFETY", 14, "#c62828", weight="bold")
d.lines(1460, 764, ["1. Wire with the adapter and USB unplugged.",
                    "2. 12 V goes from the jack to the carrier only,",
                    "   never into the breadboard or a rail.",
                    "3. Never plug or unplug the motor with 12 V on.",
                    "4. Power on: USB, then adapter. Off: adapter first.",
                    "5. Check every Nucleo pin label before plugging."])
a('</g>')
d.footer("Kibbly hardware · circuit 1 of the circuits by part · wires V1 to V23 in hardware/04_wiring_list.md section 6B, rails R2 to R4 in section 4B")
d.save(sys.argv[1])
