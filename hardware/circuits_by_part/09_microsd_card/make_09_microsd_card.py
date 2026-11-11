"""Draw hardware/circuits_by_part/09_microsd_card/09_microsd_card.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import (BLACK, CN7, CN8, CN10, DARKPURPLE, LIGHTPURPLE, ORANGE, PINK, PURPLE, ROW,  # noqa: E402
                    Drawing, X)

d = Drawing(1880, 960)
a, t = d.add, d.text
d.title("PART 9: MICROSD CARD MODULE (SPI)",
        "Test setup for step 3. The top + rail (5 V) comes from the Nucleo 5V pin (R1) on USB alone, or from the XL4015 (circuit 7).")
d.nucleo([(CN8(9), "5V (CN8 pin 9)", ORANGE, "right", (128, 408)), (CN7(10), "D13 · PA5 SCK (pin 10)", PURPLE, "left"),
          (CN7(12), "D12 · PA6 MISO (pin 12)", LIGHTPURPLE, "left"), (CN7(13), "D22 · PB5 MOSI (pin 13)", DARKPURPLE, "left"),
          (CN10(5), "GND (pin 5)", BLACK, "left", (186, 534)), (CN10(6), "D5 · PE11 CS (pin 6)", PINK, "left")])
d.breadboard(used=(True, True, True, False))

# microSD module: 6 pins in row j, columns 42 to 47, board over the top edge (it covers the top rails of columns 40 to 49)
x1, x2 = X(42) - 44, X(47) + 44
cx = (x1 + x2) / 2
a(f'<rect x="{x1}" y="112" width="{x2 - x1}" height="252" rx="6" fill="#0d47a1" stroke="#082f6b" stroke-width="2"/>')
a(f'<rect x="{cx - 52}" y="122" width="104" height="92" rx="4" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
a(f'<rect x="{cx - 40}" y="128" width="80" height="62" rx="3" fill="#263238"/>')
t(cx, 162, "microSD", 11, "#eceff1", "middle", "bold")
t(cx, 176, "card in here", 9, "#b0bec5", "middle")
a(f'<rect x="{cx - 46}" y="232" width="34" height="22" rx="2" fill="#111"/>')
t(cx - 29, 247, "3.3 V", 7, "#ccc", "middle")
a(f'<rect x="{cx + 6}" y="228" width="40" height="30" rx="2" fill="#111"/>')
t(cx + 26, 247, "buffer", 7, "#ccc", "middle")
for k, lab in enumerate(["CS", "SCK", "MOSI", "MISO", "VCC", "GND"]):
    x = X(42 + k)
    a(f'<rect x="{x - 4}" y="{ROW["j"] - 4}" width="8" height="8" fill="#d4af37"/>')
    t(x, 342, lab, 6.3 if len(lab) > 3 else 7.5, "#fff", "middle", "bold")
t(x1 - 12, 168, "microSD card module (SPI)", 14, "#c62828", "end", "bold")
t(x1 - 12, 186, "pins in row j, columns 42 to 47,", 11, "#555", "end")
t(x1 - 12, 202, "card slot over the top edge", 11, "#555", "end")
t(x1 - 12, 224, "Check the pin names printed on your board", 11, "#c62828", "end", "bold")

# power: VCC (column 46) to the top + rail, column 52; GND (column 47) to the top − rail, column 51
d.wire(f"M{X(47)},{ROW['i']} L{X(51) - 12},{ROW['i']} C{X(51) - 4},{ROW['i']} {X(51)},{ROW['i'] - 6} {X(51)},{ROW['i'] - 16} "
       f"L{X(51)},{ROW['top-']}", BLACK, [(X(47), ROW['i']), (X(51), ROW['top-'])])
d.wire(f"M{X(46)},{ROW['h']} L{X(52) - 12},{ROW['h']} C{X(52) - 4},{ROW['h']} {X(52)},{ROW['h'] - 6} {X(52)},{ROW['h'] - 16} "
       f"L{X(52)},{ROW['top+']}", ORANGE, [(X(46), ROW['h']), (X(52), ROW['top+'])])

# SPI wires: each one a row lower than the column on its right, so none passes over another wire end
for pin, col, row, colour, (c1, c2) in ((CN7(12), 45, "i", LIGHTPURPLE, (400, 430)), (CN7(13), 44, "h", DARKPURPLE, (400, 430)),
                                        (CN7(10), 43, "g", PURPLE, (400, 430)), (CN10(6), 42, "f", PINK, (420, 440))):
    x, y = pin
    d.wire(f"M{x},{y} C{c1},{y} {c2},{ROW[row]} 480,{ROW[row]} L{X(col)},{ROW[row]}", colour, [(x, y), (X(col), ROW[row])])
d.five_volt_feed(2)
d.ground_link(1)
d.ground_feed(3)
d.nucleo_labels()
d.zones(9)

# notes
d.notes_box(640, 712, 1220, 230)
t(660, 740, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(660, 764, [(ORANGE, "5 V: top + rail; module VCC"), (BLACK, "GND"),
                         (PURPLE, "SCK: Nucleo D13 · PA5"), (DARKPURPLE, "MOSI: Nucleo D22 · PB5"),
                         (LIGHTPURPLE, "MISO: Nucleo D12 · PA6"), (PINK, "CS: Nucleo D5 · PE11")])
t(1060, 740, "CARD AND SETTINGS", 14, "#c62828", weight="bold")
d.lines(1060, 764, ["Card: 8 to 32 GB, known brand, FAT32",
                    "Format it on the computer before first use",
                    "SPI1, mode 0; start at about 350 kHz,",
                    "then about 11 MHz (lower it if errors appear)",
                    "Module VCC on 5 V: it makes the 3.3 V itself",
                    "PA7 is not used: Ethernet needs it"])
t(1460, 740, "TIPS", 14, "#c62828", weight="bold")
d.lines(1460, 764, ["1. Wire everything with the USB unplugged.",
                    "2. Insert or remove the card only with power off.",
                    "3. Keep the SPI wires short and together.",
                    "4. The card holds clips, schedule and logs.",
                    "5. Read errors: check GND first, then lower speed.",
                    "6. Check every Nucleo pin label before plugging."])
d.footer("Kibbly hardware · circuit 9 of the circuits by part · wires S1 to S6 in hardware/04_wiring_list.md section 10, rails R1, R3 and R4 in section 4B")
d.save(sys.argv[1])
