"""Shared drawing pieces for the circuits by part (Fritzing style SVG).

Every circuit uses the same Nucleo, breadboard, wire style and colours, so the
pictures fit together when the full circuit is drawn.
"""

FONT = 'font-family="Arial, Helvetica, sans-serif"'

# wire colours: (fill, outline)
RED = ("#e53935", "#8e1b18")
BLACK = ("#333333", "#000000")
YELLOW = ("#fdd835", "#a68a00")
ORANGE = ("#fb8c00", "#a65c00")
GREY = ("#a8a8a8", "#5f5f5f")
BROWN = ("#8d6e63", "#4e342e")
BLUEGREY = ("#78909c", "#37474f")
GREEN = ("#43a047", "#1b5e20")
LIGHTGREEN = ("#9ccc65", "#558b2f")
BLUE = ("#1e88e5", "#0d47a1")
WHITE = ("#f5f5f5", "#8a8a8a")
PURPLE = ("#8e24aa", "#4a148c")
DARKPURPLE = ("#5e35b1", "#311b92")
LIGHTPURPLE = ("#ce93d8", "#7b1fa2")
PINK = ("#ec407a", "#ad1457")

# breadboard geometry: 830 point board, columns 1 to 63, and named rows
COLS = 63
RIGHT = 500 + (COLS - 1) * 20  # x of column 63

# column map of the whole feeder on one board (every part fits in columns 1 to 49)
ZONES = [(1, 3, "power", (1, 7)), (5, 12, "1 motor driver", (1,)), (15, 21, "4 sound · 2 HX711", (2, 4)),
         (24, 27, "3 HC-SR04", (3,)), (29, 34, "5 ESP32-CAM · 8 I2C bus", (5, 8)),
         (42, 49, "9 microSD · 10 button, LED", (9, 10))]
ROW = {"top+": 292, "top-": 312, "j": 356, "i": 376, "h": 396, "g": 416, "f": 436,
       "e": 476, "d": 496, "c": 516, "b": 536, "a": 556, "bot-": 600, "bot+": 620}


# ESP32-CAM pin rows as seen from the camera side, left to right
ESP_BOTTOM = ["IO4", "IO2", "IO14", "IO15", "IO13", "IO12", "GND", "5V"]
ESP_TOP = ["GND", "U0T", "U0R", "VCC", "GND", "IO0", "IO16", "3V3"]


def X(c):
    return 500 + (c - 1) * 20


def _pin(xo, xe, y0, p):
    return (xo if p % 2 else xe), y0 + ((p - 1) // 2) * 14


def CN10(p):
    """Position of Zio connector CN10 pin p (pin numbers from UM1974)."""
    return _pin(264, 280, 460, p)


def CN8(p):
    """Position of Zio connector CN8 pin p (pin numbers from UM1974)."""
    return _pin(100, 116, 300, p)


def CN7(p):
    return _pin(264, 280, 300, p)


def CN9(p):
    return _pin(100, 116, 430, p)


def CN11(p):
    """Position of morpho connector CN11 pin p (left edge of the Nucleo, pin numbers from UM1974)."""
    return _pin(58, 72, 292, p)


class Drawing:
    def __init__(self, width=1880, height=1020):
        self.w, self.h = width, height
        self.out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                    f'<rect width="{width}" height="{height}" fill="#ffffff"/>']

    def add(self, s):
        self.out.append(s)

    def text(self, x, y, s, size=12, fill="#222", anchor="start", weight="normal"):
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text x="{x}" y="{y}" {FONT} font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')

    def wire(self, d, col, ends, width=4.5, dash=None):
        """dash: for example "10 6" for a wire that is only fitted in some setups."""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" fill="none" stroke="{col[1]}" stroke-width="{width + 3}" stroke-linecap="round" stroke-linejoin="round"{da}/>')
        self.add(f'<path d="{d}" fill="none" stroke="{col[0]}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{da}/>')
        for x, y in ends:
            self.add(f'<circle cx="{x}" cy="{y}" r="4.6" fill="{col[1]}" stroke="#ffffff" stroke-width="1.2"/>')

    def title(self, title, subtitle):
        self.text(40, 46, title, 28, "#c62828", weight="bold")
        self.text(40, 72, subtitle, 15, "#444")

    def footer(self, s):
        self.text(40, self.h - 16, s, 11, "#9e9e9e")

    def nucleo(self, pins):
        """Draw the NUCLEO-F439ZI. pins: list of (position, label, colour, side) to highlight;
        side is 'left' for labels left of the pin (right headers) or 'right'. An optional fifth
        item (x, y) places the label there, with a thin line to the pin."""
        a, t = self.add, self.text
        a('<rect x="40" y="130" width="300" height="720" rx="10" fill="#f6f6f3" stroke="#9e9e9e" stroke-width="2"/>')
        a('<line x1="40" y1="270" x2="340" y2="270" stroke="#bdbdbd" stroke-width="2" stroke-dasharray="6 5"/>')
        a('<rect x="165" y="116" width="50" height="26" rx="3" fill="#b0b0b0" stroke="#757575"/>')
        a('<rect x="175" y="122" width="30" height="10" rx="2" fill="#757575"/>')
        a('<path d="M190,116 L190,96" stroke="#555" stroke-width="7" stroke-linecap="round"/>')
        t(222, 108, "USB cable to the laptop (power and code)", 12, "#555")
        a('<rect x="100" y="180" width="44" height="44" rx="3" fill="#2b2b2b"/>')
        t(122, 206, "ST-LINK", 9, "#ddd", "middle")
        t(250, 210, "ST-LINK part", 12, "#9e9e9e", "middle")
        for x0 in (50, 304):
            a(f'<rect x="{x0}" y="284" width="30" height="492" rx="2" fill="#262626"/>')
            for r in range(35):
                for dx in (8, 22):
                    a(f'<rect x="{x0 + dx - 2.5}" y="{292 + r * 14 - 2.5}" width="5" height="5" fill="#d4af37"/>')
        t(65, 280, "CN11", 10, "#666", "middle")
        t(319, 280, "CN12", 10, "#666", "middle")
        for xo, xe, y0, rows, name in ((100, 116, 300, 8, "CN8"), (100, 116, 430, 15, "CN9"),
                                       (264, 280, 300, 10, "CN7"), (264, 280, 460, 17, "CN10")):
            a(f'<rect x="{xo - 8}" y="{y0 - 8}" width="32" height="{rows * 14 + 2}" rx="2" fill="#1b1b1b"/>')
            for r in range(rows):
                for x in (xo, xe):
                    a(f'<rect x="{x - 3}" y="{y0 + r * 14 - 3}" width="6" height="6" fill="#000" stroke="#4d4d4d"/>')
            t((xo + xe) / 2, y0 - 12, name, 10, "#666", "middle")
        a('<rect x="150" y="570" width="80" height="80" rx="4" fill="#2b2b2b"/>')
        t(190, 606, "STM32", 12, "#eee", "middle", "bold")
        t(190, 622, "F439ZI", 12, "#eee", "middle", "bold")
        t(190, 444, "NUCLEO-F439ZI", 15, "#1a237e", "middle", "bold")
        for i, c in enumerate(("#43a047", "#1e88e5", "#e53935")):
            a(f'<rect x="{160 + i * 20}" y="700" width="10" height="6" fill="{c}"/>')
        t(190, 724, "LD1  LD2  LD3", 9, "#888", "middle")
        a('<circle cx="110" cy="800" r="13" fill="#1565c0" stroke="#0d3c84" stroke-width="2"/>')
        t(110, 830, "USER", 9, "#666", "middle")
        a('<circle cx="270" cy="800" r="13" fill="#222" stroke="#000" stroke-width="2"/>')
        t(270, 830, "RESET", 9, "#666", "middle")
        self._pins = pins

    def nucleo_labels(self):
        """Pin rings and labels, drawn after the wires so they stay on top."""
        for pin in self._pins:
            (x, y), label, col, side = pin[:4]
            self.add(f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{col[1]}" stroke-width="2"/>')
            if len(pin) > 4:
                lx, ly = pin[4]
                self.add(f'<line x1="{x}" y1="{y + 7}" x2="{lx - 3}" y2="{ly - 4}" stroke="{col[1]}" stroke-width="1.2"/>')
                self.text(lx, ly, label, 10, col[1], weight="bold")
            elif side == "left":
                self.text(252, y + 4, label, 10, col[1], "end", "bold")
            else:
                self.text(128, y + 4, label, 10, col[1], weight="bold")

    def breadboard(self, top=("5 V", "GND"), bottom=("GND", "3.3 V"), used=(True, True, True, True)):
        """830 point breadboard. used: (top +, top −, bottom −, bottom +); unused rail labels are grey."""
        a, t = self.add, self.text
        a(f'<rect x="474" y="262" width="{RIGHT + 26 - 474}" height="388" rx="8" fill="#f1f1f1" stroke="#c8c8c8" stroke-width="2"/>')
        a(f'<rect x="480" y="448" width="{RIGHT + 14 - 480}" height="16" fill="#dadada"/>')
        for y, col in ((281, "#e53935"), (323, "#1e88e5"), (589, "#1e88e5"), (631, "#e53935")):
            a(f'<line x1="490" y1="{y}" x2="{RIGHT + 12}" y2="{y}" stroke="{col}" stroke-width="2"/>')
        for name, y in ROW.items():
            for c in range(1, COLS + 1):
                a(f'<rect x="{X(c) - 3}" y="{y - 3}" width="6" height="6" rx="1" fill="#4a4a4a"/>')
            if len(name) == 1:
                t(484, y + 4, name, 10, "#999", "middle")
        t(486, 297, "+", 13, "#e53935", "middle", "bold")
        t(486, 316, "−", 13, "#1e88e5", "middle", "bold")
        t(486, 604, "−", 13, "#1e88e5", "middle", "bold")
        t(486, 625, "+", 13, "#e53935", "middle", "bold")
        for c in (1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 63):
            t(X(c), 344, str(c), 9, "#9a9a9a", "middle")
            t(X(c), 577, str(c), 9, "#9a9a9a", "middle")
        grey = "#b0b0b0"
        lx = RIGHT + 34
        t(lx, 297, top[0], 13, "#a65c00" if used[0] else grey, weight="bold")
        t(lx, 317, top[1], 13, "#222" if used[1] else grey, weight="bold")
        t(lx, 605, bottom[0], 13, "#222" if used[2] else grey, weight="bold")
        t(lx, 625, bottom[1], 13, "#b8860b" if used[3] else grey, weight="bold")
        for y, u in ((333, used[0] or used[1]), (641, used[2] or used[3])):
            if not u:
                t(lx, y, "(not used)", 10, grey)

    def zones(self, circuit, y=676):
        """Column map strip under the board; the zones of this circuit are highlighted."""
        a, t = self.add, self.text
        t(480, y - 6, "Column map of the whole feeder:", 10, "#777", weight="bold")
        for c1, c2, label, circuits in ZONES:
            on = circuit in circuits
            x1, x2 = X(c1) - 9, X(c2) + 9
            a(f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="22" rx="4" fill="{"#ffe0b2" if on else "#f3f3f3"}" '
              f'stroke="{"#ef6c00" if on else "#d6d6d6"}" stroke-width="{1.5 if on else 1}"/>')
            t((x1 + x2) / 2, y + 15, label, 9, "#a65c00" if on else "#9a9a9a", "middle", "bold" if on else "normal")

    def five_volt_feed(self, col=2):
        """Nucleo 5V (CN8 pin 9) over the top of the board to the top + rail (5 V)."""
        x, y = CN8(9)
        self.wire(f"M{x},{y} C90,{y} 86,346 86,330 L86,250 C86,242 92,238 100,238 L{X(col) - 12},238 "
                  f"C{X(col) - 4},238 {X(col)},244 {X(col)},252 L{X(col)},{ROW['top+']}",
                  ORANGE, [(x, y), (X(col), ROW['top+'])])

    def three_volt_feed(self, col=2):
        """Nucleo 3V3 (CN8 pin 7) around the left and bottom of the board to the bottom + rail (3.3 V)."""
        x, y = CN8(7)
        self.wire(f"M{x},{y} C40,{y} 22,380 22,440 L22,866 C22,886 40,892 64,892 L430,892 C456,892 464,876 464,850 "
                  f"L464,654 C464,644 470,640 480,640 L{X(col) - 10},640 C{X(col) - 4},640 {X(col)},634 {X(col)},{ROW['bot+']}",
                  YELLOW, [(x, y), (X(col), ROW['bot+'])])

    def ground_feed(self, col=3):
        """Nucleo GND (CN10 pin 5) to the bottom − rail."""
        x, y = CN10(5)
        self.wire(f"M{x},{y} C380,{y} 470,{ROW['bot-']} {X(col)},{ROW['bot-']}", BLACK, [(x, y), (X(col), ROW['bot-'])])

    def ground_link(self, col=1):
        """Join the top − rail and the bottom − rail."""
        self.wire(f"M{X(col)},{ROW['top-']} L{X(col)},{ROW['bot-']}", BLACK, [(X(col), ROW['top-']), (X(col), ROW['bot-'])])

    def esp32_cam(self, x0, y0=96, used_bottom=(), used_top=()):
        """ESP32-CAM seen from the camera side, pins every 20 px. x0: x of the left pins; y0: top of the board.
        The bottom row (5V ... IO4) points down, the top row (3V3 ... GND, used to load programs) points up.
        Returns (bottom, top): pin name to (x, y) of the pin tip. In the top row 'GND' is the pin next to
        IO0 and 'GND end' the one next to U0T. Used pins get white labels."""
        a, t = self.add, self.text
        bx1, bx2 = x0 - 176, x0 + 156
        a(f'<rect x="{bx1}" y="{y0}" width="{bx2 - bx1}" height="140" rx="6" fill="#262626" stroke="#000" stroke-width="2"/>')
        a(f'<rect x="{bx1 + 10}" y="{y0 + 12}" width="128" height="116" rx="3" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>')
        a(f'<path d="M{bx1 + 16},{y0 + 24} L{bx1 + 16},{y0 + 116} M{bx1 + 22},{y0 + 24} L{bx1 + 22},{y0 + 116} '
          f'M{bx1 + 16},{y0 + 24} L{bx1 + 22},{y0 + 24} M{bx1 + 16},{y0 + 116} L{bx1 + 22},{y0 + 116}" '
          f'stroke="#d4af37" stroke-width="2" fill="none"/>')
        t(bx1 + 80, y0 + 66, "ESP32-S", 12, "#455a64", "middle", "bold")
        t(bx1 + 80, y0 + 82, "WiFi module", 9, "#607d8b", "middle")
        cx, cy = x0 + 50, y0 + 72
        a(f'<rect x="{cx - 30}" y="{cy - 30}" width="60" height="60" rx="4" fill="#3a3a3a" stroke="#111"/>')
        a(f'<circle cx="{cx}" cy="{cy}" r="22" fill="#111" stroke="#555" stroke-width="2"/>')
        a(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#1a237e"/>')
        a(f'<circle cx="{cx - 4}" cy="{cy - 4}" r="4" fill="#90caf9"/>')
        t(cx, cy + 44, "camera", 9, "#bbb", "middle")
        a(f'<rect x="{x0 + 114}" y="{cy - 8}" width="16" height="16" rx="2" fill="#fff9c4" stroke="#f9a825"/>')
        t(x0 + 122, cy + 22, "flash", 8, "#bbb", "middle")
        bottom, top = {}, {}
        for k, name in enumerate(ESP_BOTTOM):
            x = x0 + 20 * k
            a(f'<rect x="{x - 3}" y="{y0 + 140}" width="6" height="12" fill="#d4af37"/>')
            t(x, y0 + 134, name, 7 if len(name) > 3 else 8, "#fff" if name in used_bottom else "#8a8a8a", "middle", "bold")
            bottom[name] = (x, y0 + 152)
        for k, name in enumerate(ESP_TOP):
            x = x0 + 20 * k
            key = "GND end" if name == "GND" and k == 0 else name
            a(f'<rect x="{x - 3}" y="{y0 - 12}" width="6" height="12" fill="#d4af37"/>')
            t(x, y0 + 21, name, 6.5, "#fff" if key in used_top else "#9e9e9e", "middle", "bold")
            top[key] = (x, y0 - 12)
        return bottom, top

    def dc_jack(self):
        """12 V adapter and DC jack module above columns 1 to 4. Screw terminals: − at x 534, + at x 564,
        wires leave from y 186 (bottom) or y 142 (top)."""
        a, t = self.add, self.text
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

    def driver_capacitor(self, labels=True):
        """1000 uF capacitor of the driver: long leg (+) in column 5 row j (12 V), short leg in the top − rail, column 4."""
        a, t = self.add, self.text
        a(f'<line x1="582" y1="248" x2="{X(5)}" y2="{ROW["j"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
        a(f'<line x1="566" y1="248" x2="{X(4)}" y2="{ROW["top-"]}" stroke="#9e9e9e" stroke-width="2.5"/>')
        a('<rect x="560" y="206" width="28" height="44" rx="6" fill="#1f2f74"/>')
        a('<rect x="560" y="206" width="9" height="44" rx="3" fill="#9fb0e8"/>')
        for y in (216, 228, 240):
            a(f'<line x1="562" y1="{y}" x2="567" y2="{y}" stroke="#1f2f74" stroke-width="2"/>')
        a('<ellipse cx="574" cy="207" rx="14" ry="4" fill="#3a4c9a"/>')
        for x, y in ((X(5), ROW["j"]), (X(4), ROW["top-"])):
            a(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#757575"/>')
        if labels:
            t(466, 222, "1000 µF capacitor", 12, "#1f2f74", "end", "bold")
            t(466, 237, "long leg (+): column 5 →", 10, "#1f2f74", "end")

    def twelve_volt_column(self):
        """Red frame around column 5, top half: the only place with 12 V."""
        self.add(f'<rect x="{X(5) - 11}" y="{ROW["j"] - 12}" width="22" height="{ROW["f"] - ROW["j"] + 22}" rx="4" '
                 f'fill="#ffcdd2" fill-opacity="0.55" stroke="#e53935" stroke-width="1.5" stroke-dasharray="4 3"/>')

    def notes_box(self, x, y, w, h):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fafafa" stroke="#dddddd"/>')

    def colour_list(self, x, y, rows, step=22):
        for i, (col, lab) in enumerate(rows):
            yy = y + i * step
            self.add(f'<line x1="{x + 2}" y1="{yy - 4}" x2="{x + 40}" y2="{yy - 4}" stroke="{col[1]}" stroke-width="7" stroke-linecap="round"/>')
            self.add(f'<line x1="{x + 2}" y1="{yy - 4}" x2="{x + 40}" y2="{yy - 4}" stroke="{col[0]}" stroke-width="4.5" stroke-linecap="round"/>')
            self.text(x + 52, yy, lab, 12.5)

    def lines(self, x, y, items, step=20, size=12.5):
        for i, s in enumerate(items):
            self.text(x, y + i * step, s, size)

    def save(self, path):
        self.out.append("</svg>")
        with open(path, "w", encoding="utf8") as f:
            f.write("\n".join(self.out))
