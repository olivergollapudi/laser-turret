"""Draws hardware/wiring.png and wiring.svg. Run from the repo root: python hardware/make_wiring_diagram.py hardware/wiring"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = sys.argv[1]

C = {
    "5v": "#d62728", "3v3": "#ff8c1a", "gnd": "#222222", "sda": "#1f6fd1",
    "scl": "#e0b000", "gpio": "#2ca02c", "sig": "#ff8c1a", "servo_gnd": "#7a4a1e",
}
FONT = "DejaVu Sans"

fig, ax = plt.subplots(figsize=(16, 10.4), dpi=110)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10.4)
ax.axis("off")
fig.patch.set_facecolor("white")


def board(x0, y0, x1, y1, color, title, sub=None, tcolor="white"):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=color, ec="#00000055", lw=1.5, zorder=2))
    ax.text((x0 + x1) / 2, y1 - 0.35, title, ha="center", va="center", color=tcolor,
            fontsize=15, fontweight="bold", family=FONT, zorder=5)
    if sub:
        ax.text((x0 + x1) / 2, y1 - 0.7, sub, ha="center", va="center", color=tcolor,
                fontsize=10, family=FONT, alpha=0.9, zorder=5)


def pin(x, y, label, side, tcolor="white", nc=False):
    ax.add_patch(Rectangle((x - 0.09, y - 0.09), 0.18, 0.18, fc="#d4af37", ec="#5a4a10", lw=1, zorder=6))
    dx = -0.22 if side == "left" else 0.22
    ha = "right" if side == "left" else "left"
    ax.text(x + dx, y, label, ha=ha, va="center", fontsize=11, color=tcolor, family=FONT,
            zorder=6, alpha=0.55 if nc else 1)


def wire(points, color, lw=3.2):
    xs, ys = zip(*points)
    ax.plot(xs, ys, color="white", lw=lw + 2.2, solid_capstyle="round", solid_joinstyle="round", zorder=3)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=4)


ax.text(0.4, 10.0, "laser-turret wiring", fontsize=22, fontweight="bold", family=FONT, va="center")
ax.text(0.4, 9.6, "Raspberry Pi Zero 2W  ·  PCA9685  ·  2× SG90  ·  KY-008 laser  ·  Camera Module 3",
        fontsize=12, family=FONT, va="center", color="#555")

# --- Raspberry Pi Zero 2W ---
board(0.6, 1.9, 4.7, 7.9, "#1f7a3a", "Raspberry Pi Zero 2W", "physical header pin numbers")
pi_pins = {
    "3v3": (7.0, "Pin 1 · 3.3V"),
    "5v": (6.4, "Pin 2 · 5V"),
    "sda": (5.8, "Pin 3 · GPIO2 SDA"),
    "scl": (5.2, "Pin 5 · GPIO3 SCL"),
    "gnd": (4.6, "Pin 6 · GND"),
    "gnd2": (3.6, "Pin 9 · GND"),
    "gpio": (3.0, "Pin 11 · GPIO17"),
}
PX = 4.4
for k, (y, lab) in pi_pins.items():
    pin(PX, y, lab, "left")
# CSI connector + USB power
ax.add_patch(Rectangle((1.2, 7.78), 1.4, 0.22, fc="#111", ec="#111", zorder=6))
ax.add_patch(Rectangle((2.2, 1.78), 0.6, 0.22, fc="#999", ec="#666", zorder=6))
ax.annotate("", xy=(2.5, 1.95), xytext=(2.5, 1.0),
            arrowprops=dict(arrowstyle="-|>", color="#555", lw=2), zorder=5)
ax.text(2.5, 0.75, "micro-USB power\n(Mac USB port or 5V 2.5A adapter)", ha="center", va="top",
        fontsize=10, family=FONT, color="#444")

# --- Camera Module 3 ---
board(0.6, 8.55, 3.6, 9.3, "#2b2b2b", "Camera Module 3", None)
ax.add_patch(Rectangle((1.65, 7.95), 0.5, 0.62, fc="#e8a33d", ec="#b07010", lw=1, zorder=1))
ax.text(2.35, 8.25, "ribbon (22→15 pin) to CSI port", fontsize=9.5, family=FONT, color="#555", va="center")

# --- PCA9685 ---
board(7.6, 3.9, 11.0, 7.9, "#1d3f8f", "PCA9685", "16-ch servo driver · I²C 0x40")
pca_pins = {
    "gnd": (6.9, "GND"), "oe": (6.5, "OE  (not used)"), "scl": (6.1, "SCL"),
    "sda": (5.7, "SDA"), "3v3": (5.3, "VCC"), "5v": (4.9, "V+"),
}
QX = 7.9
for k, (y, lab) in pca_pins.items():
    pin(QX, y, lab, "right", nc=(k == "oe"))
ax.text(9.3, 4.25, "screw terminal not used", fontsize=9.5, color="white", alpha=0.7,
        family=FONT, ha="center", zorder=6)
ch = {"0": 6.6, "1": 5.3}
for c, y in ch.items():
    for i, dy in enumerate((0.25, 0, -0.25)):
        ax.add_patch(Rectangle((10.62, y + dy - 0.08), 0.16, 0.16, fc="#d4af37", ec="#5a4a10", zorder=6))
    ax.text(10.45, y, f"CH {c}", ha="right", va="center", fontsize=11, color="white",
            fontweight="bold", family=FONT, zorder=6)

# Pi -> PCA9685 wires (each takes its own vertical lane)
lanes = {"3v3": 5.3, "5v": 5.65, "sda": 6.0, "scl": 6.35, "gnd": 6.7}
for k, lane in lanes.items():
    y0 = pi_pins[k][0]
    y1 = pca_pins[k][0]
    wire([(PX, y0), (lane, y0), (lane, y1), (QX, y1)], C[k])

# --- Servos ---
servo_y = {"0": (6.6, "Pan servo", "SG90 · left/right"), "1": (5.3, "Tilt servo", "SG90 · up/down")}
for c, (y, name, sub) in servo_y.items():
    ax.add_patch(FancyBboxPatch((12.6, y - 0.5), 2.6, 1.0, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="#2f57c8", ec="#00000055", lw=1.5, zorder=2))
    ax.text(13.9, y + 0.15, name, ha="center", va="center", fontsize=13, color="white",
            fontweight="bold", family=FONT, zorder=5)
    ax.text(13.9, y - 0.2, sub, ha="center", va="center", fontsize=9.5, color="white", family=FONT, zorder=5)
    for dy, col in ((0.25, C["sig"]), (0, C["5v"]), (-0.25, C["servo_gnd"])):
        wire([(10.78, y + dy), (12.6, y + dy)], col, lw=2.6)
ax.text(11.7, 7.15, "signal / + / −", ha="center", fontsize=9.5, color="#555", family=FONT)

# --- KY-008 laser ---
board(7.6, 1.2, 10.4, 3.2, "#8b1a1a", "KY-008 laser", "650 nm · ≤5 mW")
las = {"gpio": (2.3, "S"), "nc": (1.95, "middle  (not used)"), "gnd2": (1.6, "−")}
for k, (y, lab) in las.items():
    pin(QX, y, lab, "right", nc=(k == "nc"))
wire([(PX, pi_pins["gpio"][0]), (5.6, pi_pins["gpio"][0]), (5.6, las["gpio"][0]), (QX, las["gpio"][0])], C["gpio"])
wire([(PX, pi_pins["gnd2"][0]), (6.1, pi_pins["gnd2"][0]), (6.1, las["gnd2"][0]), (QX, las["gnd2"][0])], C["gnd"])

# --- Legend ---
lx, ly = 11.6, 3.05
ax.text(lx, ly + 0.15, "Wire colors", fontsize=12, fontweight="bold", family=FONT)
items = [("5V", C["5v"]), ("3.3V", C["3v3"]), ("GND", C["gnd"]), ("SDA", C["sda"]),
         ("SCL", C["scl"]), ("GPIO17 → laser", C["gpio"])]
for i, (lab, col) in enumerate(items):
    yy = ly - 0.3 - i * 0.32
    ax.plot([lx, lx + 0.5], [yy, yy], color=col, lw=4, solid_capstyle="round")
    ax.text(lx + 0.65, yy, lab, va="center", fontsize=10.5, family=FONT)

# --- Notes ---
notes = ("Servo power comes from the Pi's 5V pin through the PCA9685's V+ header pin. If the Pi resets when the "
         "servos move,\nfeed the PCA9685 screw terminal from a separate 5V supply instead and connect its − to Pi GND.")
ax.text(5.2, 0.45, notes, fontsize=9.5, family=FONT, color="#444", va="center")

fig.savefig(OUT + ".png", dpi=110, bbox_inches="tight", facecolor="white")
fig.savefig(OUT + ".svg", bbox_inches="tight", facecolor="white")
