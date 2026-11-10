"""Draw hardware/circuits_by_part/06_esp32_cam_flashing/06_esp32_cam_flashing.svg (Fritzing style)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from common import BLACK, GREEN, GREY, LIGHTGREEN, ORANGE, Drawing  # noqa: E402

d = Drawing(1880, 960)
a, t = d.add, d.text
d.title("PART 6: FLASHING THE ESP32-CAM WITH THE DEVKIT",
        "Flashing = loading a program into the board. Bench setup, no Nucleo needed: the DevKit lends its USB chip.")

# ESP32 DevKit V1 (30 pins), antenna at the top, USB at the bottom
LEFT = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
RIGHT = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]
XL, XR, Y0, P = 298, 482, 214, 26
dk = {}
a('<rect x="280" y="150" width="220" height="480" rx="8" fill="#1c2833" stroke="#0b1015" stroke-width="2"/>')
a('<rect x="336" y="156" width="108" height="144" rx="3" fill="#2b2b2b"/>')
a('<path d="M344,164 L344,178 L356,178 L356,164 L368,164 L368,178 L380,178 L380,164 L392,164 L392,178 '
  'L404,178 L404,164 L416,164 L416,178 L428,178 L428,164 L436,164" stroke="#d4af37" stroke-width="2" fill="none"/>')
a('<rect x="342" y="186" width="96" height="108" rx="3" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
t(390, 236, "ESP32", 12, "#455a64", "middle", "bold")
t(390, 252, "held off", 9, "#607d8b", "middle")
t(390, 264, "by EN", 9, "#607d8b", "middle")
a('<rect x="372" y="470" width="36" height="36" rx="2" fill="#111"/>')
t(390, 522, "USB chip", 8, "#cfd8dc", "middle", "bold")
t(390, 534, "CP2102 or CH340", 7, "#9e9e9e", "middle")
for x, lab in ((330, "EN"), (450, "BOOT")):
    a(f'<rect x="{x - 9}" y="594" width="18" height="16" rx="2" fill="#9e9e9e"/>')
    a(f'<circle cx="{x}" cy="602" r="5" fill="#424242"/>')
    t(x, 622, lab, 7, "#bdbdbd", "middle")
a('<rect x="372" y="620" width="36" height="20" rx="3" fill="#b0b0b0" stroke="#757575"/>')
a('<path d="M390,640 L390,668" stroke="#555" stroke-width="7" stroke-linecap="round"/>')
t(402, 662, "USB cable to the laptop", 12, "#555")
used_l, used_r = {"EN", "GND", "VIN"}, {"TX0", "RX0", "GND"}
for k, (ln, rn) in enumerate(zip(LEFT, RIGHT)):
    y = Y0 + k * P
    for x, name, used, anchor, lx in ((XL, ln, used_l, "start", 312), (XR, rn, used_r, "end", 468)):
        a(f'<rect x="{x - 3.5}" y="{y - 3.5}" width="7" height="7" fill="#d4af37"/>')
        t(lx, y + 4, name, 10 if name in used else 9, "#fff" if name in used else "#78909c", anchor,
          "bold" if name in used else "normal")
    dk[("L", ln)], dk[("R", rn)] = (XL, y), (XR, y)
t(390, 138, "ESP32 DevKit V1", 14, "#c62828", "middle", "bold")

# ESP32-CAM, same drawing as circuit 5
cam_b, cam_t = d.esp32_cam(1060, 330, used_bottom={"GND", "5V"}, used_top={"U0T", "U0R", "IO0", "GND"})
t(872, 370, "ESP32-CAM", 14, "#c62828", "end", "bold")
t(872, 388, "same board as circuit 5,", 11, "#555", "end")
t(872, 404, "seen from the camera side", 11, "#555", "end")
t(872, 426, "Match every wire by its printed name", 11, "#c62828", "end", "bold")
t(1000, 512, "RST button: on the back of the board", 10, "#555", "middle")

# EN to GND on the DevKit
(x1, y1), (x2, y2) = dk[("L", "EN")], dk[("L", "GND")]
d.wire(f"M{x1},{y1} C262,{y1} 250,{y1 + 12} 250,{y1 + 32} L250,{y2 - 32} C250,{y2 - 12} 262,{y2} {x2},{y2}", GREY,
       [(x1, y1), (x2, y2)])
t(238, 370, "EN to GND (grey wire):", 11, "#555", "end", "bold")
t(238, 386, "holds the DevKit chip off,", 11, "#555", "end")
t(238, 402, "so only its USB chip works", 11, "#555", "end")

# TX0 to U0T and RX0 to U0R (they swap lanes once, near the DevKit)
(x1, y1), (x2, y2) = dk[("R", "TX0")], cam_t["U0T"]
d.wire(f"M{x1},{y1} L560,{y1} C590,{y1} 600,304 630,304 L{x2 - 14},304 C{x2 - 6},304 {x2},308 {x2},314 L{x2},{y2}",
       GREEN, [(x1, y1), (x2, y2)])
(x1, y1), (x2, y2) = dk[("R", "RX0")], cam_t["U0R"]
d.wire(f"M{x1},{y1} L560,{y1} C590,{y1} 600,276 630,276 L{x2 - 14},276 C{x2 - 6},276 {x2},282 {x2},290 L{x2},{y2}",
       LIGHTGREEN, [(x1, y1), (x2, y2)])
t(640, 248, "TX0 to U0T and RX0 to U0R is right here: the DevKit", 10, "#2e7d32", weight="bold")
t(640, 261, "pins are named for its own chip, which is held off", 10, "#2e7d32")

# IO0 to the GND next to it, only while loading
(x1, y1), (x2, y2) = cam_t["GND"], cam_t["IO0"]
d.wire(f"M{x1},{y1} C{x1},{y1 - 22} {x2},{y2 - 22} {x2},{y2}", GREY, [(x1, y1), (x2, y2)], width=3.5)
t(1176, 294, "IO0 to GND (grey):", 10, "#555", weight="bold")
t(1176, 307, "only while loading", 10, "#555")

# power from the DevKit USB
(x1, y1), (x2, y2) = dk[("R", "GND")], cam_b["GND"]
d.wire(f"M{x1},{y1} L{x2 - 14},{y1} C{x2 - 6},{y1} {x2},{y1 - 6} {x2},{y1 - 14} L{x2},{y2}", BLACK, [(x1, y1), (x2, y2)])
(x1, y1), (x2, y2) = dk[("L", "VIN")], cam_b["5V"]
d.wire(f"M{x1},{y1} C272,{y1} 264,{y1 + 12} 264,{y1 + 28} L264,690 C264,702 274,710 290,710 L{x2 - 14},710 "
       f"C{x2 - 4},710 {x2},702 {x2},692 L{x2},{y2}", ORANGE, [(x1, y1), (x2, y2)])

# steps and the second way to connect
d.notes_box(1300, 130, 560, 210)
t(1320, 158, "LOADING A PROGRAM", 14, "#c62828", weight="bold")
d.lines(1320, 184, ["1. Wire everything with the USB unplugged.",
                    "2. Join IO0 to GND on the ESP32-CAM (grey wire).",
                    "3. Plug the DevKit USB into the laptop.",
                    "4. Press the ESP32-CAM RST button (on the back).",
                    "5. Upload from PlatformIO.",
                    "6. Remove the IO0 wire and press RST again: the program",
                    "runs, and its messages show in the serial monitor."], 22)
d.notes_box(1300, 360, 560, 190)
t(1320, 388, "ALREADY WIRED TO THE FEEDER (CIRCUIT 5)?", 14, "#c62828", weight="bold")
d.lines(1320, 414, ["Keep the 4 wires of circuit 5 and add the DevKit:",
                    "1. No orange VIN wire: the top + rail powers the ESP32-CAM.",
                    "2. Black GND wire to the top − rail, column 39: the GND",
                    "pin next to 5V is already taken by circuit 5.",
                    "3. TX0, RX0, EN and IO0 wires as in this picture.",
                    "4. Plug in the Nucleo USB first, then the DevKit USB."], 21)

# notes
d.notes_box(40, 740, 1820, 190)
t(60, 768, "WIRE COLOURS", 14, "#c62828", weight="bold")
d.colour_list(60, 792, [(ORANGE, "5 V: DevKit VIN to ESP32-CAM 5V (bench only)"), (BLACK, "GND: DevKit GND to ESP32-CAM GND"),
                        (GREEN, "ESP32-CAM U0T to DevKit TX0"), (LIGHTGREEN, "DevKit RX0 to ESP32-CAM U0R"),
                        (GREY, "EN to GND (DevKit), IO0 to GND (ESP32-CAM)")])
d.lines(62, 908, ["All female to female jumper wires: both boards have pins"], 18)
t(680, 768, "PLATFORMIO SETTINGS", 14, "#c62828", weight="bold")
d.lines(680, 792, ["board = esp32cam",
                   "upload_speed = 115200 (slow but sure)",
                   "monitor_speed = 115200",
                   "Port: the one that appears when the DevKit is plugged in",
                   "No port: install the CP210x or CH340 driver,",
                   "named after the USB chip on the DevKit"])
t(1260, 768, "IF IT FAILS", 14, "#c62828", weight="bold")
d.lines(1260, 792, ["Timed out waiting for packet header: IO0 not on GND,",
                    "or RST not pressed just before the upload",
                    "The program lands in the DevKit itself: EN wire missing",
                    "Nothing in the monitor: IO0 still on GND, press RST",
                    "Brownout detector was triggered: weak 5 V, try",
                    "another USB port or a shorter cable"])
d.footer("Kibbly hardware · circuit 6 of the circuits by part · wires F1 to F7 in hardware/04_wiring_list.md section 5B")
d.save(sys.argv[1])
