import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

FIGURE = "fig12_radome_3d_explodida.png"

fig = plt.figure(figsize=(14, 9), dpi=180)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor("white")

# Triangulated spherical shell representing the radome envelope.
radius = 3.0
latitudes = np.linspace(-1.05, 1.05, 7)
longitudes = np.linspace(0, 2 * np.pi, 13)
vertices = []
for lat in latitudes:
    for lon in longitudes[:-1]:
        vertices.append((radius * np.cos(lat) * np.cos(lon),
                         radius * np.cos(lat) * np.sin(lon),
                         radius * np.sin(lat)))
vertices = np.asarray(vertices)
faces = []
cols = []
cols_palette = ["#dbe9f2", "#c9dfec", "#e5edf3", "#d4e6dc"]
row_size = len(longitudes) - 1
for i in range(len(latitudes) - 1):
    for j in range(row_size):
        a = i * row_size + j
        b = i * row_size + (j + 1) % row_size
        c = (i + 1) * row_size + (j + 1) % row_size
        d = (i + 1) * row_size + j
        faces.extend([(vertices[a], vertices[b], vertices[c]),
                      (vertices[a], vertices[c], vertices[d])])
        cols.extend([cols_palette[(i + j) % len(cols_palette)]] * 2)
ax.add_collection3d(Poly3DCollection(faces, facecolors=cols, edgecolors="#8aa5b5", linewidths=0.55, alpha=0.42))

# Highlight a representative triangular face on the front-right of the shell.
face_center = np.array([2.0, 1.0, 0.55])
face_center = radius * face_center / np.linalg.norm(face_center)
normal = face_center / np.linalg.norm(face_center)
axis = np.cross(normal, np.array([0.0, 0.0, 1.0]))
axis = axis / np.linalg.norm(axis)
axis2 = np.cross(normal, axis)
tri = [face_center + 0.85 * (np.cos(k * 2 * np.pi / 3) * axis + np.sin(k * 2 * np.pi / 3) * axis2) for k in range(3)]
ax.add_collection3d(Poly3DCollection([tri], facecolors="#e39a55", edgecolors="#9a4c2b", linewidths=2.2, alpha=0.9))

# Exploded triangular pyramid module, offset from the radome.
offset = np.array([6.2, 2.0, 0.6])
# The triangular face lies in the Y-Z tangent plane. Its RF normal is X,
# so the external Yagi is mounted parallel to the face and projects outward.
base = offset + np.array([[0.0, -1.0, -1.0], [0.0, 1.0, -1.0], [0.0, 0.0, 0.95]])
apex = offset + np.array([1.45, 0.0, 0.0])
pyramid_faces = [(base[0], base[1], apex), (base[1], base[2], apex), (base[2], base[0], apex)]
ax.add_collection3d(Poly3DCollection(pyramid_faces, facecolors="#b9d8e8", edgecolors="#21445d", linewidths=2, alpha=0.6))
ax.add_collection3d(Poly3DCollection([base], facecolors="#e5eef4", edgecolors="#21445d", linewidths=2, alpha=0.75))

# Exploded internal layers as smaller triangular plates.
for index, (x, color, label) in enumerate([(0.18, "#fae6c9", "pele + núcleo dielétrico"), (0.42, "#c8e0ed", "abertura / PCB RF"), (0.72, "#d6e8dc", "módulos blindados ADC + ASIC")]):
    layer = offset + np.column_stack((np.full(3, x), base[:, 1] * 0.72, base[:, 2] * 0.72))
    ax.add_collection3d(Poly3DCollection([layer], facecolors=color, edgecolors="#536b78", linewidths=1.3, alpha=0.92))

# Central face module and optical/power exits.
central = offset + np.array([0.95, 0.0, 0.0])
ax.scatter(*central, s=220, c="#7c68a8", edgecolors="#352e57", depthshade=False)
for end, color, label in [(offset + np.array([1.0, 0.0, -1.25]), "#3c8c83", "fibra"), (offset + np.array([1.0, 1.25, -0.8]), "#c7792d", "energia")]:
    ax.plot([central[0], end[0]], [central[1], end[1]], [central[2], end[2]], color=color, linewidth=2)
    ax.text(*end, label, fontsize=9, color=color)

# External VHF Yagi: mast, longitudinal boom, reflector, folded driven element and directors.
mast_base = offset + np.array([-0.18, 0.0, 0.0])
mast_top = offset + np.array([-0.72, 0.0, 0.0])
ax.plot([mast_base[0], mast_top[0]], [mast_base[1], mast_top[1]], [mast_base[2], mast_top[2]], color="#754b2b", linewidth=4)
boom_start = offset + np.array([-0.72, -1.45, 0.0])
boom_end = offset + np.array([-0.72, 1.55, 0.0])
ax.plot([boom_start[0], boom_end[0]], [boom_start[1], boom_end[1]], [boom_start[2], boom_end[2]], color="#6d7074", linewidth=5)
# Reflector, driven folded loop and tapered directors.
reflector = offset + np.array([-0.72, -1.25, 0.0])
ax.plot([reflector[0], reflector[0]], [reflector[1], reflector[1]], [reflector[2] - 0.63, reflector[2] + 0.63], color="#9a6b2f", linewidth=4)
driven_x = offset[0] - 0.72
loop_center_y = offset[1] - 0.35
loop_z_values = [offset[2] - 0.5, offset[2] - 0.62, offset[2] - 0.62, offset[2] - 0.5, offset[2] + 0.5, offset[2] + 0.62, offset[2] + 0.62, offset[2] + 0.5]
loop_y_values = [loop_center_y, loop_center_y - 0.18, loop_center_y + 0.18, loop_center_y, loop_center_y, loop_center_y - 0.18, loop_center_y + 0.18, loop_center_y]
ax.plot([driven_x] * len(loop_y_values), loop_y_values, loop_z_values, color="#b9792e", linewidth=3)
for index, z in enumerate(np.linspace(-0.05, 1.35, 5)):
    top = offset + np.array([-0.72, -0.35, z])
    half_span = 0.52 - index * 0.055
    ax.plot([top[0], top[0]], [top[1], top[1]], [top[2] - half_span, top[2] + half_span], color="#6d7074", linewidth=2.5)
# Clamp and short feed stalk, matching a practical external mounting arrangement.
ax.plot([offset[0] - 0.18, offset[0] - 0.72], [offset[1], offset[1]], [offset[2], offset[2]], color="#c08a32", linewidth=5)

# Dimension annotation for the 2 m triangular side.
p0, p1 = base[0], base[1]
ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2] - 0.12, p1[2] - 0.12], color="#9a4c2b", linewidth=2)
ax.text(*((p0 + p1) / 2 + np.array([0.0, -0.25, -0.12])), "2.00 m", color="#9a4c2b", fontsize=12, weight="bold")

# Exploded relation lines.
for p in tri:
    ep = offset + (p - face_center) * 0.45
    ax.plot([p[0], ep[0]], [p[1], ep[1]], [p[2], ep[2]], linestyle="--", color="#b74747", linewidth=1.2)
fig.text(0.69, 0.78, "EXPLODED FACE / FACE EXPLODIDA", color="#17324d", fontsize=11, weight="bold")
fig.text(0.69, 0.74, "VHF Yagi mounted on outer face", color="#754b2b", fontsize=9, weight="bold")
fig.text(0.69, 0.71, "Yagi VHF montada na face externa", color="#754b2b", fontsize=9)
fig.text(0.69, 0.65, "2 m triangular face / face triangular", color="#9a4c2b", fontsize=9, weight="bold")
fig.text(0.69, 0.60, "shielded ADC + ASIC modules", color="#263746", fontsize=9)
fig.text(0.69, 0.57, "módulos ADC + ASIC blindados", color="#263746", fontsize=9)
fig.text(0.69, 0.52, "FFASIC, clock, fibre and DC", color="#352e57", fontsize=9)
fig.text(0.69, 0.49, "FFASIC, clock, fibra e DC", color="#352e57", fontsize=9)

# Orthographic inset: the support/boom axis continues from the internal apex;
# the Yagi elements are transverse to that axis.
inset = fig.add_axes([0.68, 0.08, 0.28, 0.25])
inset.set_facecolor("#f7fafc")
inset.set_xlim(-1.8, 1.8)
inset.set_ylim(-1.2, 2.3)
inset.axis("off")
inset.set_title("External VHF Yagi / Yagi VHF externa", fontsize=9, color="#17324d", weight="bold", pad=4)
# triangular face edge and normal mast
inset.plot([-1.45, 0.0, 1.45, -1.45], [0.0, 1.8, 0.0, 0.0], color="#21445d", linewidth=2)
inset.plot([0.0, 0.0], [0.0, -0.55], color="#c08a32", linewidth=3)
# Yagi boom vertical, directors horizontal, reflector and folded driven element
inset.plot([0.0, 0.0], [-0.45, 1.95], color="#6d7074", linewidth=4)
inset.plot([0.0, 0.0], [1.72, 1.72], color="#9a6b2f", linewidth=4)
for y in np.linspace(-0.15, 1.4, 5):
    half = 0.62 - (y + 0.15) * 0.08
    inset.plot([-half, half], [y, y], color="#6d7074", linewidth=2)
inset.plot([-0.42, -0.68, 0.68, 0.42], [0.72, 0.88, 0.88, 0.72], color="#b9792e", linewidth=2)
inset.annotate("apex support / boom axis", xy=(0, -0.45), xytext=(0.65, -0.8), fontsize=7, color="#754b2b", arrowprops={"arrowstyle": "->", "color": "#754b2b"})
inset.text(0.05, 2.02, "boom", fontsize=7, color="#263746")
inset.text(0.7, 1.25, "directors", fontsize=7, color="#263746")

ax.set_title("RADOME V1 — 3D exploded face architecture", fontsize=18, color="#17324d", pad=18, weight="bold")
ax.set_axis_off()
ax.set_xlim(-3.8, 9.0)
ax.set_ylim(-3.8, 5.8)
ax.set_zlim(-3.8, 5.0)
ax.view_init(elev=19, azim=-58)
ax.set_box_aspect((1.35, 1.0, 1.0))
plt.tight_layout()
plt.savefig(FIGURE, bbox_inches="tight", facecolor="white")
