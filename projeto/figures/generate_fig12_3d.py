"""Generate a language-neutral exploded 3D face illustration."""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from build_paths import build_output

OUTPUT = build_output("fig12_radome_3d_explodida.png")
fig = plt.figure(figsize=(12, 8), dpi=180)
ax = fig.add_subplot(111, projection="3d")

# Face lies in x=0; +x is the outward normal and the inward apex is at -x.
face = np.array([[0, -1.0, -0.58], [0, 1.0, -0.58], [0, 0.0, 1.15]])
apex = np.array([-0.75, 0.0, 0.0])
ax.add_collection3d(Poly3DCollection([face], facecolors="#dcebf2", edgecolors="#263746", linewidths=2, alpha=0.9))
for i in range(3):
    ax.add_collection3d(Poly3DCollection([[face[i], face[(i+1)%3], apex]], facecolors="#dcefe9", edgecolors="#52606d", linewidths=1.2, alpha=0.45))

# Exploded internal layers remain behind the external aperture.
for x, color, scale in [(-0.18, "#f2d7a9", 0.86), (-0.36, "#cce5d0", 0.72), (-0.56, "#dcd4ee", 0.58)]:
    layer = face.copy() * np.array([1, scale, scale])
    layer[:, 0] = x
    ax.add_collection3d(Poly3DCollection([layer], facecolors=color, edgecolors="#52606d", linewidths=1.0, alpha=0.9))

# Boom is collinear with the external normal; element axes are +45/+135 deg.
ax.plot([-0.75, 2.8], [0, 0], [0, 0], color="#263746", linewidth=5)
directions = [(np.sqrt(0.5), np.sqrt(0.5), "#d08b4d"), (-np.sqrt(0.5), np.sqrt(0.5), "#5f91b7")]
for direction_y, direction_z, color in directions:
    for index, x in enumerate(np.linspace(0.35, 2.55, 6)):
        half = (0.92 - 0.10 * index) * (1.0 if color == "#d08b4d" else 0.65)
        ax.plot([x, x], [-direction_y*half, direction_y*half], [-direction_z*half, direction_z*half], color=color, linewidth=3)

ax.quiver(0, 0, 0, 1.25, 0, 0, color="#4f887c", linewidth=2, arrow_length_ratio=0.12)
ax.set_axis_off()
ax.set_xlim(-1.2, 3.2); ax.set_ylim(-1.8, 1.8); ax.set_zlim(-1.5, 1.7)
ax.set_box_aspect((1.4, 1.0, 1.0))
ax.view_init(elev=22, azim=-55)
plt.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
plt.close(fig)
