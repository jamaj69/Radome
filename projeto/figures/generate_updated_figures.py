"""Generate the shared, language-neutral technical figures 01--10.

Permanent publication rule: figures contain geometry, colour and line style
only. All verbal explanation belongs in the language-specific LaTeX caption.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle, Wedge


OUT = Path(__file__).resolve().parent
INK = "#263746"
BLUE = "#5f91b7"
CYAN = "#7eb6c9"
ORANGE = "#d08b4d"
GREEN = "#78a56f"
PURPLE = "#9588bd"
RED = "#bd7777"
PALE = "#e8edf0"


def canvas(figsize=(12, 7), equal=False):
    fig, ax = plt.subplots(figsize=figsize, dpi=180)
    ax.axis("off")
    if equal:
        ax.set_aspect("equal")
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def box(ax, xy, wh=(1.4, 0.8), color=PALE, radius=0.08):
    patch = FancyBboxPatch(xy, *wh, boxstyle=f"round,pad=0.04,rounding_size={radius}", facecolor=color, edgecolor=INK, linewidth=1.5)
    ax.add_patch(patch)
    return patch


def arrow(ax, a, b, color=INK, width=1.8, style="->"):
    ax.annotate("", xy=b, xytext=a, arrowprops={"arrowstyle": style, "color": color, "lw": width})


# 01 — distributed hierarchy.
fig, ax = canvas(equal=True)
ax.set_xlim(-6, 6); ax.set_ylim(-4, 4)
source = Polygon([(-0.8, 3.1), (0.8, 3.1), (0.45, 3.65), (-0.45, 3.65)], closed=True, facecolor=ORANGE, edgecolor=INK, linewidth=1.6)
ax.add_patch(source)
stations = [(-4.3, 0.8), (0, 0.35), (4.3, 0.8)]
for x, y in stations:
    ax.add_patch(Wedge((x, y), 1.05, 0, 180, facecolor="#dcebf2", edgecolor=BLUE, linewidth=2))
    arrow(ax, (0, 3.05), (x, y + 1.0), ORANGE)
fusion = box(ax, (-1.15, -3.0), (2.3, 0.9), PURPLE)
for x, y in stations:
    arrow(ax, (x, y - 0.05), (0, -2.05), GREEN)
save(fig, "fig01_arquitetura_rede.png")


# 02 — hybrid functional zoning; no sector is a rigid EM boundary.
fig, ax = canvas((10, 8), equal=True)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5)
colors = [GREEN, ORANGE, BLUE, CYAN, PURPLE]
angles = [(205, 295), (295, 350), (350, 385), (25, 105), (105, 175)]
for (start, end), color in zip(angles, colors):
    ax.add_patch(Wedge((0, 0), 2.9, start, end, facecolor=color, edgecolor="white", linewidth=3, alpha=0.88))
ax.add_patch(Circle((0, 0), 0.82, facecolor="white", edgecolor=INK, linewidth=2.2))
for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
    arrow(ax, (0.75*np.cos(angle), 0.75*np.sin(angle)), (2.45*np.cos(angle), 2.45*np.sin(angle)), "#ffffff", 1.0, "-")
save(fig, "fig02_zonamento_radome.png")


# 03 — triangular face and layered electromechanical stack.
fig, ax = canvas((12, 7), equal=True)
ax.set_xlim(-4.5, 6.5); ax.set_ylim(-3.5, 3.5)
tri = np.array([[-3.4, -2.3], [-0.2, -2.3], [-1.8, 2.55]])
ax.add_patch(Polygon(tri, closed=True, facecolor="#dcebf2", edgecolor=INK, linewidth=2.2))
ax.add_patch(Polygon(tri*0.62 + np.array([-0.68, -0.25]), closed=True, facecolor=GREEN, edgecolor=INK, linewidth=1.5))
for point in tri:
    arrow(ax, (-1.8, 0.0), tuple(point), PURPLE, 1.5)
layers = ["#dcebf2", "#f2d7a9", "#d4dde3", "#cce5d0", "#ead2d2", "#dcd4ee"]
for i, color in enumerate(layers):
    ax.add_patch(Rectangle((1.0, 2.3-i*0.82), 4.5, 0.45, facecolor=color, edgecolor=INK, linewidth=1.2))
    if i:
        arrow(ax, (3.25, 2.25-(i-1)*0.82), (3.25, 2.3-i*0.82+0.46), INK, 1.0)
for y, color in [(-2.65, ORANGE), (-2.0, CYAN)]:
    box(ax, (1.2, y), (1.7, 0.52), color)
    box(ax, (3.6, y), (1.7, 0.52), color)
save(fig, "fig03_modulo_face.png")


# 04 — spectral allocation by relative logarithmic span; gaps remain white.
fig, ax = canvas((14, 6))
ax.set_xlim(6.3, 10.7); ax.set_ylim(-0.8, 7.2)
bands = [(6.48, 7.48, GREEN), (7.48, 8.48, ORANGE), (8.67, 8.93, BLUE), (8.98, 9.08, "#4f7f73"), (9.0, 9.90, CYAN), (9.90, 10.26, PURPLE), (10.26, 10.60, RED)]
for y, (low, high, color) in enumerate(bands):
    ax.add_patch(Rectangle((low, y-0.3), high-low, 0.6, facecolor=color, edgecolor=INK, linewidth=1.2))
for x in [6.48, 7.48, 8.48, 8.67, 8.93, 8.98, 9.08, 9.90, 10.26, 10.60]:
    ax.plot([x, x], [-0.5, 6.6], color="#ccd4d9", linewidth=0.8, zorder=0)
save(fig, "fig04_particionamento_espectro.png")


# 05 — invalid cross-band fusion above, valid coherent same-band pair below.
fig, ax = canvas((13, 7))
ax.set_xlim(0, 13); ax.set_ylim(0, 7)
for y, colors_pair in [(4.5, (ORANGE, BLUE)), (1.2, (GREEN, GREEN))]:
    box(ax, (0.5, y+0.75), (2.0, 0.9), colors_pair[0])
    box(ax, (0.5, y-0.55), (2.0, 0.9), colors_pair[1])
    box(ax, (4.2, y+0.1), (2.5, 1.0), PALE if y > 2 else "#f2d7a9")
    box(ax, (8.4, y+0.1), (3.6, 1.0), "#ead2d2" if y > 2 else "#dcd4ee")
    arrow(ax, (2.5, y+1.2), (4.2, y+0.75)); arrow(ax, (2.5, y-0.1), (4.2, y+0.45)); arrow(ax, (6.7, y+0.6), (8.4, y+0.6))
ax.plot([8.8, 11.6], [5.0, 6.0], color=RED, linewidth=4)
ax.plot([8.8, 11.6], [6.0, 5.0], color=RED, linewidth=4)
save(fig, "fig05_polarimetria.png")


# 06 — RF chain and edge processing.
fig, ax = canvas((14, 6))
ax.set_xlim(0, 14); ax.set_ylim(0, 6)
colors = [CYAN, "#f2d7a9", GREEN, PURPLE, RED, BLUE, "#dcd4ee"]
for i, color in enumerate(colors):
    box(ax, (0.35+i*1.9, 3.6), (1.45, 0.9), color)
    if i < len(colors)-1: arrow(ax, (1.8+i*1.9, 4.05), (2.25+i*1.9, 4.05))
for x, color in [(2.25, ORANGE), (6.05, CYAN), (9.85, PURPLE)]:
    box(ax, (x, 1.0), (1.55, 0.8), color)
    arrow(ax, (x+0.78, 1.8), (x+0.78, 3.55), color)
save(fig, "fig06_cadeia_rf.png")


# 07 — GNSS/holdover timing and end-to-end delay calibration.
fig, ax = canvas((13, 7))
ax.set_xlim(0, 13); ax.set_ylim(0, 7)
left = [(0.6, 5.0), (0.6, 1.2)]
for xy in left: box(ax, xy, (2.0, 1.0), "#dcebf2")
box(ax, (4.2, 3.1), (2.0, 1.0), PURPLE)
box(ax, (7.8, 4.8), (2.0, 1.0), GREEN)
box(ax, (7.8, 1.4), (2.0, 1.0), "#dcebf2")
box(ax, (10.8, 3.1), (1.6, 1.0), "#f2d7a9")
for a, b in [((2.6,5.5),(4.2,3.8)), ((2.6,1.7),(4.2,3.4)), ((6.2,3.6),(7.8,5.3)), ((6.2,3.6),(7.8,1.9)), ((9.8,5.3),(10.8,3.8)), ((9.8,1.9),(10.8,3.4))]: arrow(ax, a, b)
save(fig, "fig07_sincronizacao.png")


# 08 — bistatic/multistatic geometry.
fig, ax = canvas((13, 7), equal=True)
ax.set_xlim(-6, 6); ax.set_ylim(-3.2, 3.6)
illuminator = Circle((-4.5, -2.0), 0.28, facecolor=ORANGE, edgecolor=INK); ax.add_patch(illuminator)
target = Polygon([(-0.4,2.4),(0.4,2.4),(0.65,2.7),(0,3.1),(-0.65,2.7)], closed=True, facecolor="#b7c5cc", edgecolor=INK); ax.add_patch(target)
receivers = [(3.8,-2.0),(4.0,0.2),(-0.4,-2.5)]
for p in receivers: ax.add_patch(Circle(p, 0.25, facecolor=BLUE, edgecolor=INK))
arrow(ax, (-4.25,-1.85), (-0.35,2.35), ORANGE)
for p in receivers: arrow(ax, (0.35,2.4), p, RED)
ax.plot([-4.25,3.55],[-2.0,-2.0], color="#8a9aa3", linewidth=1.2)
ax.add_patch(Wedge((-4.5,-2.0), 8.4, 2, 34, fill=False, edgecolor=PURPLE, linewidth=1.4, linestyle="--"))
save(fig, "fig08_geometria_bistatica.png")


# 09 — passive multistatic processing flow.
fig, ax = canvas((14, 6))
ax.set_xlim(0, 14); ax.set_ylim(0, 6)
box(ax, (0.4, 4.1), (1.7, 0.8), "#f2d7a9")
box(ax, (0.4, 1.1), (1.7, 0.8), "#dcebf2")
for i, color in enumerate([PALE, GREEN, PURPLE, RED, ORANGE]):
    box(ax, (3.1+i*2.05, 2.6), (1.55, 0.9), color)
    if i < 4: arrow(ax, (4.65+i*2.05,3.05),(5.15+i*2.05,3.05))
arrow(ax, (2.1,4.5),(3.1,3.25)); arrow(ax, (2.1,1.5),(3.1,2.85))
box(ax, (5.15, 0.55), (2.0, 0.75), "#dcd4ee"); arrow(ax, (6.15,1.3),(6.15,2.55), PURPLE)
box(ax, (9.25, 0.55), (2.0, 0.75), CYAN); arrow(ax, (10.25,2.55),(10.25,1.3), CYAN)
save(fig, "fig09_fluxo_processamento.png")


# 10 — staged development roadmap.
fig, ax = canvas((13, 6))
ax.set_xlim(0, 13); ax.set_ylim(0, 6)
stages = [(0.5,4.7,2.0,PALE),(2.0,3.7,3.0,BLUE),(4.0,2.7,3.6,GREEN),(6.6,1.7,3.5,PURPLE),(9.3,0.7,3.0,ORANGE)]
for x,y,w,color in stages:
    ax.add_patch(Rectangle((x,y),w,0.72,facecolor=color,edgecolor=INK,linewidth=1.3))
for i in range(len(stages)-1):
    x,y,w,_ = stages[i]; nx,ny,_,_ = stages[i+1]
    arrow(ax,(x+w,y+0.36),(nx,ny+0.36),INK,1.2)
save(fig, "fig10_roteiro.png")
