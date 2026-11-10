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
BLUE = ("#1e88e5", "#0d47a1")
WHITE = ("#f5f5f5", "#8a8a8a")
PURPLE = ("#8e24aa", "#4a148c")
DARKPURPLE = ("#5e35b1", "#311b92")
LIGHTPURPLE = ("#ce93d8", "#7b1fa2")

# breadboard geometry: 830 point board, columns 1 to 63, and named rows
COLS = 63
RIGHT = 500 + (COLS - 1) * 20  # x of column 63

# column map of the whole feeder on one board (every part fits in columns 1 to 49)
ZONES = [(1, 3, "power", (1,)), (5, 12, "1 motor driver", (1,)), (15, 21, "4 sound · 2 HX711", (2, 4)),
         (24, 27, "3 HC-SR04", (3,)), (29, 34, "5 ESP32-CAM · 8 clock", (5, 8)),
         (36, 42, "9 microSD · 8 tank", (8, 9)), (44, 49, "10 button, LED", (10,))]
ROW = {"top+": 292, "top-": 312, "j": 356, "i": 376, "h": 396, "g": 416, "f": 436,
       "e": 476, "d": 496, "c": 516, "b": 536, "a": 556, "bot-": 600, "bot+": 620}


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

    def wire(self, d, col, ends, width=4.5):
        self.add(f'<path d="{d}" fill="none" stroke="{col[1]}" stroke-width="{width + 3}" stroke-linecap="round" stroke-linejoin="round"/>')
        self.add(f'<path d="{d}" fill="none" stroke="{col[0]}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
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
