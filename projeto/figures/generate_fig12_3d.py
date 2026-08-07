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
ax.text(*(face_center * 1.12), "RF face", color="#7c3f1d", fontsize=10, weight="bold")

# Exploded triangular pyramid module, offset from the radome.
offset = np.array([5.2, 1.8, 0.6])
base = np.array([[-1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.95, 0.0]]) + offset
apex = np.array([0.0, 0.0, 1.45]) + offset
pyramid_faces = [(base[0], base[1], apex), (base[1], base[2], apex), (base[2], base[0], apex)]
ax.add_collection3d(Poly3DCollection(pyramid_faces, facecolors="#b9d8e8", edgecolors="#21445d", linewidths=2, alpha=0.6))
ax.add_collection3d(Poly3DCollection([base], facecolors="#e5eef4", edgecolors="#21445d", linewidths=2, alpha=0.75))
ax.text(*(offset + np.array([0.0, -1.35, 2.0])), "EXPLODED FACE / FACE EXPLODIDA", ha="center", color="#17324d", fontsize=11, weight="bold")

# Exploded internal layers as smaller triangular plates.
for z, color, label in [(0.22, "#fae6c9", "pele + núcleo dielétrico"), (0.48, "#c8e0ed", "abertura / PCB RF"), (0.76, "#d6e8dc", "módulos blindados ADC + ASIC")]:
    layer = base * 0.72 + np.array([0.0, 0.0, z])
    ax.add_collection3d(Poly3DCollection([layer], facecolors=color, edgecolors="#536b78", linewidths=1.3, alpha=0.92))
    ax.text(*(layer.mean(axis=0) + np.array([1.55, 0.0, 0.04])), label, fontsize=8, color="#263746")

# Central face module and optical/power exits.
central = offset + np.array([0.0, 0.0, 0.93])
ax.scatter(*central, s=220, c="#7c68a8", edgecolors="#352e57", depthshade=False)
ax.text(*(central + np.array([1.45, 0.0, 0.18])), "FFASIC / clock / fibre / DC", ha="left", fontsize=8, color="#352e57")
for end, color, label in [(offset + np.array([0.0, 0.0, -1.0]), "#3c8c83", "fibra"), (offset + np.array([1.35, 0.0, -0.7]), "#c7792d", "energia")]:
    ax.plot([central[0], end[0]], [central[1], end[1]], [central[2], end[2]], color=color, linewidth=2)
    ax.text(*end, label, fontsize=9, color=color)

# External VHF Yagi: mast, longitudinal boom, reflector, folded driven element and directors.
mast_base = offset + np.array([0.0, -0.15, 0.0])
mast_top = offset + np.array([0.0, -0.35, 2.35])
ax.plot([mast_base[0], mast_top[0]], [mast_base[1], mast_top[1]], [mast_base[2], mast_top[2]], color="#754b2b", linewidth=4)
boom_start = offset + np.array([-1.45, -0.35, 2.35])
boom_end = offset + np.array([1.55, -0.35, 2.35])
ax.plot([boom_start[0], boom_end[0]], [boom_start[1], boom_end[1]], [boom_start[2], boom_end[2]], color="#6d7074", linewidth=5)
# Reflector, driven folded loop and tapered directors.
reflector = offset + np.array([-1.25, -0.35, 2.35])
ax.plot([reflector[0], reflector[0]], [reflector[1] - 0.63, reflector[1] + 0.63], [reflector[2], reflector[2]], color="#9a6b2f", linewidth=4)
driven_x = offset[0] - 0.35
loop_y = offset[1] - 0.35
loop_z = offset[2] + 2.35
loop_y_values = [loop_y - 0.5, loop_y - 0.62, loop_y - 0.62, loop_y - 0.5, loop_y + 0.5, loop_y + 0.62, loop_y + 0.62, loop_y + 0.5]
loop_z_values = [loop_z, loop_z + 0.18, loop_z + 0.18, loop_z, loop_z, loop_z + 0.18, loop_z + 0.18, loop_z]
ax.plot([driven_x] * len(loop_y_values), loop_y_values, loop_z_values, color="#b9792e", linewidth=3)
for index, x in enumerate(np.linspace(-0.05, 1.35, 5)):
    top = offset + np.array([x, -0.35, 2.35])
    half_span = 0.52 - index * 0.055
    ax.plot([top[0], top[0]], [top[1] - half_span, top[1] + half_span], [top[2], top[2]], color="#6d7074", linewidth=2.5)
# Clamp and short feed stalk, matching a practical external mounting arrangement.
ax.plot([offset[0] - 0.1, offset[0] - 0.1], [offset[1] - 0.35, offset[1] - 0.35], [offset[2] + 1.9, offset[2] + 2.35], color="#c08a32", linewidth=5)
ax.text(*(offset + np.array([0.05, -1.05, 2.85])), "VHF YAGI / ANTENA VHF", ha="center", fontsize=10, color="#754b2b", weight="bold")

# Dimension annotation for the 2 m triangular side.
p0, p1 = base[0], base[1]
ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2] - 0.12, p1[2] - 0.12], color="#9a4c2b", linewidth=2)
ax.text(*((p0 + p1) / 2 + np.array([0.0, -0.25, -0.12])), "2.00 m", color="#9a4c2b", fontsize=12, weight="bold")

# Exploded relation lines.
for p in tri:
    ep = offset + (p - face_center) * 0.45
    ax.plot([p[0], ep[0]], [p[1], ep[1]], [p[2], ep[2]], linestyle="--", color="#b74747", linewidth=1.2)
ax.text(3.7, 3.7, 3.7, "2 m triangular face", color="#b74747", fontsize=10, weight="bold")

ax.set_title("RADOME V1 — 3D exploded face architecture", fontsize=18, color="#17324d", pad=18, weight="bold")
ax.set_axis_off()
ax.set_xlim(-3.8, 8.0)
ax.set_ylim(-3.8, 5.4)
ax.set_zlim(-3.8, 5.0)
ax.view_init(elev=19, azim=-58)
ax.set_box_aspect((1.35, 1.0, 1.0))
plt.tight_layout()
plt.savefig(FIGURE, bbox_inches="tight", facecolor="white")
