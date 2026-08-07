import bpy
import math
from mathutils import Vector

OUTPUT = "/home/jamaj/src/Radome/projeto/figures/fig13_radome_blender.png"

# Reset scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

# Materials.
def material(name, color, metallic=0.0, roughness=0.45, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, alpha)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        bsdf.inputs["Transmission"].default_value = 0.08
        mat.blend_method = "BLEND"
        mat.use_screen_refraction = True
        mat.show_transparent_back = True
        mat.node_tree.nodes.get("Principled BSDF").inputs["IOR"].default_value = 1.45
    return mat

shell_mat = material("Radome dielectric shell", (0.22, 0.52, 0.68), metallic=0.0, roughness=0.35, alpha=0.18)
frame_mat = material("Geodesic frame", (0.10, 0.28, 0.40), metallic=0.35, roughness=0.3)
face_mat = material("Highlighted RF face", (0.92, 0.42, 0.12), metallic=0.05, roughness=0.35, alpha=0.74)
dielectric_mat = material("Dielectric layer", (0.72, 0.83, 0.88), roughness=0.38, alpha=0.82)
core_mat = material("Honeycomb core", (0.95, 0.73, 0.36), roughness=0.55)
shield_mat = material("Shielded RF module", (0.18, 0.34, 0.42), metallic=0.65, roughness=0.28)
board_mat = material("RF PCB", (0.08, 0.33, 0.20), roughness=0.4)
ffasic_mat = material("FFASIC central module", (0.38, 0.25, 0.62), metallic=0.3, roughness=0.28)
yagi_mat = material("Yagi aluminium", (0.67, 0.70, 0.72), metallic=0.82, roughness=0.2)
yagi_gold = material("Yagi bracket", (0.82, 0.50, 0.06), metallic=0.65, roughness=0.25)
mast_mat = material("Mast", (0.20, 0.22, 0.24), metallic=0.7, roughness=0.25)
white_mat = material("White", (0.92, 0.94, 0.95), roughness=0.45)

# Geometry helpers.
def cylinder_between(name, a, b, radius, mat, vertices=20):
    a, b = Vector(a), Vector(b)
    direction = b - a
    midpoint = (a + b) / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=direction.length, location=midpoint)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat("Z", "Y")
    return obj

def triangle_mesh(name, points, mat, bevel=0.0):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(points, [], [(0, 1, 2)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Edge bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    return obj

def text_obj(body, location, size=0.20, color_mat=white_mat, align="CENTER"):
    curve = bpy.data.curves.new(body, "FONT")
    curve.body = body
    curve.align_x = align
    curve.size = size
    curve.extrude = 0.004
    obj = bpy.data.objects.new(body, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(color_mat)
    # Keep labels approximately facing the camera through a track quaternion later.
    return obj

# Radome shell: UV sphere with transparent material and visible triangular frame lines.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=2.75, location=(-3.7, 0.0, 1.9))
shell = bpy.context.object
shell.name = "Transparent geodesic radome shell"
shell.data.materials.append(shell_mat)
wire = shell.modifiers.new("Geodesic frame", "WIREFRAME")
wire.thickness = 0.012
wire.material_offset = 0
shell.data.materials.append(frame_mat)
# A second wire object gives a darker structural outline.

# Highlighted face on right/front of radome.
face_center = Vector((-1.22, -1.05, 2.25))
face_normal = (face_center - Vector((-3.7, 0, 1.9))).normalized()
edge_a = Vector((-1.32, -1.55, 1.45))
edge_b = Vector((-1.25, -0.40, 1.48))
edge_c = Vector((-1.05, -1.00, 2.45))
triangle_mesh("Highlighted radome face", [edge_a, edge_b, edge_c], face_mat, 0.015)

# Exploded triangular pyramid: face plane is Y-Z, normal points +X.
offset = Vector((1.55, 0.0, 0.4))
base = [offset + Vector((0.0, -1.20, -0.85)), offset + Vector((0.0, 1.20, -0.85)), offset + Vector((0.0, 0.0, 1.22))]
apex = offset + Vector((1.35, 0.0, 0.0))
for i in range(3):
    triangle_mesh("Pyramid structural side", [base[i], base[(i + 1) % 3], apex], dielectric_mat, 0.025)
triangle_mesh("Outer triangular RF face", base, face_mat, 0.025)

# Exploded layers just behind the external face, separated along +X.
for index, (x, mat, name) in enumerate([(0.18, dielectric_mat, "Dielectric skin and honeycomb"), (0.42, board_mat, "RF aperture and PCB"), (0.68, shield_mat, "Shielded ADC ASIC band modules")]):
    scale = 0.72
    layer = [offset + Vector((x, p.y * scale, p.z * scale)) for p in [Vector((0, -1.2, -0.85)), Vector((0, 1.2, -0.85)), Vector((0, 0, 1.22))]]
    triangle_mesh(name, layer, mat, 0.015)

# FFASIC central face module: box behind the band layers.
bpy.ops.mesh.primitive_cube_add(size=1, location=offset + Vector((0.93, 0.0, 0.0)))
ffasic = bpy.context.object
ffasic.name = "FFASIC central face module"
ffasic.dimensions = (0.28, 0.62, 0.62)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
ffasic.data.materials.append(ffasic_mat)

# Internal joints: structural triangular frame and node plates.
for a, b in [(base[0], base[1]), (base[1], base[2]), (base[2], base[0])]:
    cylinder_between("Internal sealed structural joint", a + Vector((0.06, 0, 0)), b + Vector((0.06, 0, 0)), 0.035, frame_mat)
for point in base:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.09, location=point + Vector((0.08, 0, 0)))
    bpy.context.object.name = "Internal node plate"
    bpy.context.object.data.materials.append(frame_mat)

# External Yagi: the mast is normal to the face (+X), while the boom points
# along the local tangent direction (+Z). Directors remain in the tangent plane.
yagi_x = offset.x + 1.75
mast_base = offset + Vector((1.35, 0.0, -0.85))
mast_top = Vector((yagi_x, 0.0, 0.65))
cylinder_between("Yagi mast normal to face", mast_base, mast_top, 0.065, mast_mat)
# The boom is tangent to the face plane; it does not point along the face normal.
boom_bottom = Vector((yagi_x, -0.02, -0.15))
boom_top = Vector((yagi_x, -0.02, 2.25))
cylinder_between("Yagi longitudinal boom", boom_bottom, boom_top, 0.045, yagi_mat)
# Reflector at bottom, driven folded loop, and directors.
cylinder_between("Yagi reflector", Vector((yagi_x, -0.02, -0.05)), Vector((yagi_x, -0.02, 0.72)), 0.035, yagi_mat)
for z, half in [(-0.05, 0.47), (0.38, 0.43), (0.80, 0.39), (1.20, 0.35), (1.58, 0.31), (1.93, 0.27)]:
    cylinder_between("Yagi director", Vector((yagi_x, -half, z)), Vector((yagi_x, half, z)), 0.022, yagi_mat)
# Folded driven element as a rectangular rounded loop approximated by four cylinders.
loop_z = 1.02
loop_half_y = 0.58
loop_half_x = 0.12
loop_left = Vector((yagi_x - loop_half_x, -loop_half_y, loop_z))
loop_right = Vector((yagi_x + loop_half_x, loop_half_y, loop_z))
cylinder_between("Yagi folded driven element", Vector((yagi_x - loop_half_x, -loop_half_y, loop_z),), Vector((yagi_x + loop_half_x, -loop_half_y, loop_z)), 0.032, yagi_gold)
cylinder_between("Yagi folded driven element", Vector((yagi_x + loop_half_x, -loop_half_y, loop_z),), Vector((yagi_x + loop_half_x, loop_half_y, loop_z)), 0.032, yagi_gold)
cylinder_between("Yagi folded driven element", Vector((yagi_x + loop_half_x, loop_half_y, loop_z),), Vector((yagi_x - loop_half_x, loop_half_y, loop_z)), 0.032, yagi_gold)
cylinder_between("Yagi folded driven element", Vector((yagi_x - loop_half_x, loop_half_y, loop_z),), Vector((yagi_x - loop_half_x, -loop_half_y, loop_z)), 0.032, yagi_gold)
# Feed stalk and bracket.
cylinder_between("Yagi feed stalk", Vector((yagi_x - 0.03, 0, loop_z)), Vector((offset.x + 1.38, 0, loop_z)), 0.035, yagi_gold)
bpy.ops.mesh.primitive_cube_add(size=1, location=offset + Vector((1.37, 0, -0.85)))
bracket = bpy.context.object
bracket.name = "Yagi base bracket"
bracket.dimensions = (0.18, 0.38, 0.22)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bracket.data.materials.append(yagi_gold)

# Fibres and power leaving FFASIC.
central = offset + Vector((0.93, 0.0, 0.0))
cylinder_between("Optical fibre", central, central + Vector((0.45, -1.3, -0.8)), 0.022, material("Fibre", (0.08, 0.55, 0.48), metallic=0.1, roughness=0.3))
cylinder_between("DC power", central, central + Vector((0.45, 1.3, -0.75)), 0.028, material("DC", (0.8, 0.35, 0.08), metallic=0.1, roughness=0.35))

# Text labels placed in world space.
labels = [
    ("RADOME shell / casca", (-3.7, 0.0, 5.0), 0.22, white_mat),
    ("EXPLODED FACE / FACE EXPLODIDA", (3.0, -2.6, 4.3), 0.22, white_mat),
    ("2 m triangular face", (2.4, -2.35, 3.9), 0.18, yagi_gold),
    ("VHF Yagi: boom tangent / mast normal", (3.2, -2.45, 3.55), 0.16, yagi_gold),
    ("shielded ADC + ASIC layers", (3.4, 2.1, 2.1), 0.14, white_mat),
    ("FFASIC / clock / fibre / DC", (3.7, 2.1, 0.4), 0.14, white_mat),
]
for body, loc, size, mat in labels:
    text_obj(body, loc, size, mat)

# Ground plane and lighting.
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -1.1))
plane = bpy.context.object
plane.name = "Ground"
plane.data.materials.append(material("Ground material", (0.025, 0.04, 0.055), metallic=0.0, roughness=0.55))

bpy.ops.object.light_add(type="AREA", location=(1, -6, 10))
key = bpy.context.object
key.name = "Key light"
key.data.energy = 1200
key.data.shape = "DISK"
key.data.size = 6
key.rotation_euler = (math.radians(20), 0, math.radians(10))

bpy.ops.object.light_add(type="AREA", location=(-6, 4, 5))
fill = bpy.context.object
fill.data.energy = 850
fill.data.size = 5
fill.rotation_euler = (math.radians(65), 0, math.radians(-55))

bpy.ops.object.light_add(type="AREA", location=(7, 2, 5))
rim = bpy.context.object
rim.data.energy = 950
rim.data.size = 4
rim.rotation_euler = (math.radians(55), 0, math.radians(125))

# Camera.
def point_camera(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.camera_add(location=(11.5, -15.0, 8.5))
camera = bpy.context.object
camera.name = "Technical camera"
point_camera(camera, (0.3, 0.0, 1.0))
camera.data.lens = 52
bpy.context.scene.camera = camera

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1600
scene.render.resolution_y = 1000
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUTPUT
scene.render.film_transparent = False
scene.world.color = (0.008, 0.015, 0.025)
scene.view_settings.view_transform = "Filmic"
scene.view_settings.look = "Medium High Contrast"
scene.render.resolution_percentage = 100
bpy.ops.wm.save_as_mainfile(filepath="/home/jamaj/src/Radome/projeto/figures/radome_v1_3d.blend")
bpy.ops.render.render(write_still=True)
