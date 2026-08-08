import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, FancyBboxPatch, Polygon

OUT = "/home/jamaj/src/Radome/projeto/figures"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})

# Figure 2: updated functional zoning.
fig, ax = plt.subplots(figsize=(12, 8), dpi=180)
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-4.0, 4.0)
ax.set_ylim(-4.15, 4.05)
ax.set_title("Radome as a hybrid multiband platform\nRadome como plataforma híbrida multifaixa", fontsize=18, color="#17324d", pad=18)
outer = Circle((0, 0), 3.0, facecolor="#e7f0f5", edgecolor="#4e7184", linewidth=2.5, alpha=0.8)
ax.add_patch(outer)
for start, end, color, label, sub in [
    (205, 295, "#9ab98f", "HF", "loops + platform modes"),
    (295, 350, "#d89a58", "VHF Yagi", "large elements"),
    (350, 25, "#8caed0", "UHF Yagi", "smaller elements"),
    (25, 105, "#9ec4d6", "L/S/C", "sinuous / Vivaldi / TCDA"),
    (105, 175, "#aaa0d0", "X/Ku/Ka", "dedicated tiles"),
]:
    if end < start:
        end += 360
    ax.add_patch(Wedge((0, 0), 2.92, start, end, facecolor=color, edgecolor="#ffffff", linewidth=2, alpha=0.82))
    angle = np.deg2rad((start + end) / 2)
    x, y = 1.75 * np.cos(angle), 1.75 * np.sin(angle)
    ax.text(x, y + 0.12, label, ha="center", va="center", fontsize=13, weight="bold", color="#17324d")
    ax.text(x, y - 0.16, sub, ha="center", va="center", fontsize=8, color="#263746")
ax.add_patch(Circle((0, 0), 0.85, facecolor="#ffffff", edgecolor="#273746", linewidth=2.2))
ax.text(0, 0.12, "FACE CORE", ha="center", weight="bold", fontsize=12, color="#17324d")
ax.text(0, -0.15, "FFASIC / clock / fibre / DC", ha="center", fontsize=8, color="#52606d")
ax.text(-3.25, 3.45, "Two crossed external Yagis share one support axis", fontsize=10, color="#9a4c2b", weight="bold")
ax.text(-3.25, 3.18, "Duas Yagis externas cruzadas compartilham um eixo de suporte", fontsize=9, color="#9a4c2b")
ax.text(-3.25, -3.45, "The angular sectors are functional families, not rigid electromagnetic boundaries.", fontsize=9, color="#52606d")
ax.text(-3.25, -3.68, "Os setores são famílias funcionais, não fronteiras eletromagnéticas rígidas.", fontsize=9, color="#52606d")
fig.savefig(f"{OUT}/fig02_zonamento_radome.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# Figure 4: updated frequency partition.
fig, ax = plt.subplots(figsize=(14, 7), dpi=180)
ax.set_xscale("log")
ax.set_xlim(3e6, 40e9)
ax.set_ylim(-0.95, 7.0)
ax.grid(True, which="both", axis="x", color="#d9e0e5", linewidth=0.7)
ax.set_title("Spectral partition and selected external antennas\nParticionamento espectral e antenas externas selecionadas", fontsize=18, color="#17324d", pad=16)
ax.set_xlabel("Frequency / Frequência (Hz, logarithmic scale)", fontsize=11)
rows = [
    ("HF", 3e6, 30e6, "loops / modes", "#85aa7e"),
    ("VHF", 30e6, 300e6, "external Yagi", "#d08b4d"),
    ("UHF", 470e6, 860e6, "crossed Yagi", "#5f91b7"),
    ("AVIATION", 960e6, 1215e6, "UAT / 1090ES", "#4f7f73"),
    ("L/S/C", 1e9, 8e9, "sinuous / Vivaldi", "#d99a59"),
    ("X/Ku", 8e9, 18e9, "tiles", "#9588bd"),
    ("K/Ka", 18e9, 40e9, "dual-pol tiles", "#bd7777"),
]
for idx, (name, low, high, detail, color) in enumerate(rows):
    y = idx
    ax.barh(y, high - low, left=low, height=0.56, align="center", color=color, alpha=0.9, edgecolor="#52606d", linewidth=0.8)
    center = np.sqrt(low * high)
    if name == "AVIATION":
        ax.text(1.28e9, y, f"{name}\n{detail}", ha="left", va="center", color="#263746", fontsize=7.5, weight="bold")
    else:
        ax.text(center, y, f"{name}\n{detail}", ha="center", va="center", color="white", fontsize=7.5, weight="bold")
ax.set_yticks([])
for value, label in [(3e6, "3 MHz"), (30e6, "30 MHz"), (300e6, "300 MHz"), (470e6, "470 MHz"), (860e6, "860 MHz"), (960e6, "960 MHz"), (1215e6, "1215 MHz"), (8e9, "8 GHz"), (18e9, "18 GHz"), (40e9, "40 GHz")]:
    ax.axvline(value, color="#52606d", linewidth=0.8, alpha=0.65)
    ax.text(value, 6.63, label, rotation=90, ha="center", va="top", fontsize=8, color="#263746")
ax.text(4e6, -0.65, "The 323–470 MHz and 860–960 MHz gaps are deliberate; aviation services use a dedicated chain.", fontsize=8.5, color="#52606d")
ax.text(4e6, -0.82, "As lacunas de 323–470 MHz e 860–960 MHz são deliberadas; serviços aeronáuticos usam cadeia dedicada.", fontsize=8.5, color="#52606d")
fig.savefig(f"{OUT}/fig04_particionamento_espectro.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# Figure 5: cross-band diversity versus valid same-band polarimetry.
fig, ax = plt.subplots(figsize=(13, 7), dpi=180)
ax.axis("off")
ax.set_xlim(0, 13)
ax.set_ylim(-0.55, 7)
ax.set_title("Cross-band diversity is not same-band polarimetry\nDiversidade entre faixas não é polarimetria na mesma faixa", fontsize=16, color="#17324d", pad=14)
def box(x, y, w, h, text, color):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12", facecolor=color, edgecolor="#52606d", linewidth=1.7)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10, color="#263746", wrap=True)
box(0.35, 5.00, 2.2, 1.05, "VHF Yagi\nsingle-pol channel V", "#f4dfc6")
box(0.35, 3.55, 2.2, 1.05, "UHF Yagi\nsingle-pol channel U", "#d5e6f1")
box(4.05, 4.25, 2.55, 1.15, "Independent bands\nindependent RF chains", "#e8edf0")
box(8.10, 4.25, 4.05, 1.15, "Spectral/orientation diversity\nNO cross-band RHCP or Stokes", "#f3d3d3")

box(0.35, 1.85, 2.2, 1.05, "Same-band port X\nE_X(f,t)", "#dcefe9")
box(0.35, 0.40, 2.2, 1.05, "Same-band port Y\nE_Y(f,t)", "#dcefe9")
box(4.05, 1.10, 2.55, 1.15, "Coherent ADCs\namplitude/phase calibration", "#fae6c9")
box(8.10, 1.10, 4.05, 1.15, "Valid same-frequency output\nJones / Stokes / RHCP / LHCP", "#e5dff3")

for x1, y1, x2, y2 in [(2.55, 5.52, 4.05, 5.00), (2.55, 4.07, 4.05, 4.65), (6.60, 4.82, 8.10, 4.82), (2.55, 2.37, 4.05, 1.85), (2.55, 0.92, 4.05, 1.50), (6.60, 1.67, 8.10, 1.67)]:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "->", "color": "#52606d", "lw": 1.8})
ax.text(0.45, -0.18, "Top: current VHF/UHF assembly. Bottom: required architecture wherever polarimetric synthesis is claimed.", fontsize=9, color="#52606d")
ax.text(0.45, -0.43, "Acima: conjunto VHF/UHF atual. Abaixo: arquitetura obrigatória onde houver síntese polarimétrica.", fontsize=9, color="#52606d")
fig.savefig(f"{OUT}/fig05_polarimetria.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# Figure 7: GNSS-referenced temporal calibration.
fig, ax = plt.subplots(figsize=(14, 7), dpi=180)
ax.axis("off")
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.set_title("GNSS-referenced timing and end-to-end calibration\nSincronização referenciada por GNSS e calibração ponta a ponta", fontsize=16, color="#17324d", pad=14)
def timing_box(x, y, w, h, text, color):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12", facecolor=color, edgecolor="#52606d", linewidth=1.7)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5, color="#263746")
timing_box(0.35, 4.65, 2.2, 1.1, "GNSS antenna A/B\nexternal, surveyed phase centre", "#d5e6f1")
timing_box(0.35, 1.25, 2.2, 1.1, "Multi-constellation\nGNSS receiver", "#e8edf0")
timing_box(3.35, 2.9, 2.2, 1.1, "1PPS + 10 MHz\nUTC / ephemerides", "#fae6c9")
timing_box(6.35, 2.9, 2.2, 1.1, "Atomic clock\nslow discipline / holdover", "#e5dff3")
timing_box(9.35, 4.65, 2.2, 1.1, "White Rabbit\ngrandmaster + fibre", "#dcefe9")
timing_box(9.35, 1.25, 2.2, 1.1, "ADC / ASIC faces\nhardware timestamp", "#cfe3ee")
timing_box(12.0, 2.9, 1.6, 1.1, "RF delay\ncalibration", "#f4dfc6")
for x1, y1, x2, y2 in [(2.55, 5.2, 3.35, 3.65), (2.55, 1.8, 3.35, 3.25), (5.55, 3.45, 6.35, 3.45), (8.55, 3.45, 9.35, 5.2), (8.55, 3.25, 9.35, 1.8), (11.55, 5.2, 12.0, 3.75), (11.55, 1.8, 12.0, 3.25)]:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "->", "color": "#52606d", "lw": 1.8})
ax.text(0.45, 0.35, "GNSS supplies absolute epoch and frequency; it does not replace RF delay, temperature and phase calibration.", fontsize=9, color="#52606d")
ax.text(0.45, 0.12, "O GNSS fornece época e frequência absolutas; não substitui a calibração de atrasos, temperatura e fase RF.", fontsize=9, color="#52606d")
fig.savefig(f"{OUT}/fig07_sincronizacao.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
