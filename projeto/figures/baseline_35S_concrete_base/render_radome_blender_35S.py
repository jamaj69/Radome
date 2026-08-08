import bpy
import math
from mathutils import Vector

OUTPUT = "/home/jamaj/src/Radome/projeto/figures/fig13_radome_blender.png"
INTERNAL_OUTPUT = "/home/jamaj/src/Radome/projeto/figures/fig14_radome_interior_blender.png"

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
internal_module_mat = material("Internal band module highlight", (0.72, 0.28, 0.08), metallic=0.35, roughness=0.3)
board_mat = material("RF PCB", (0.08, 0.33, 0.20), roughness=0.4)
ffasic_mat = material("FFASIC central module", (0.38, 0.25, 0.62), metallic=0.3, roughness=0.28)
yagi_mat = material("Yagi aluminium", (0.67, 0.70, 0.72), metallic=0.82, roughness=0.2)
yagi_gold = material("Yagi bracket", (0.82, 0.50, 0.06), metallic=0.65, roughness=0.25)
mast_mat = material("Mast", (0.20, 0.22, 0.24), metallic=0.7, roughness=0.25)
white_mat = material("White", (0.92, 0.94, 0.95), roughness=0.45)
base_mat = material("Concrete base", (0.42, 0.45, 0.47), roughness=0.88)
opening_mat = material("Access opening", (0.015, 0.02, 0.025), roughness=0.5)
warning_mat = material("Access frame", (0.82, 0.42, 0.06), metallic=0.3, roughness=0.35)

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

# Radome shell: equator as the mid-plane and lower cut at latitude 35 S.
shell_center = Vector((-3.7, 0.0, 0.0))
radius = 2.75
segments = 24
rings = 7
lower_cut_latitude = math.radians(-35.0)
cut_polar_angle = math.pi / 2.0 - lower_cut_latitude
shell_vertices = [shell_center + Vector((0, 0, radius))]
shell_faces = []
for ring in range(1, rings + 1):
    theta = cut_polar_angle * ring / rings
    for segment in range(segments):
        phi = 2.0 * math.pi * segment / segments
        shell_vertices.append(shell_center + Vector((radius * math.sin(theta) * math.cos(phi), radius * math.sin(theta) * math.sin(phi), radius * math.cos(theta))))
for segment in range(segments):
    shell_faces.append((0, 1 + segment, 1 + (segment + 1) % segments))
for ring in range(rings - 1):
    start = 1 + ring * segments
    next_start = start + segments
    for segment in range(segments):
        a = start + segment
        b = start + (segment + 1) % segments
        c = next_start + (segment + 1) % segments
        d = next_start + segment
        shell_faces.extend([(a, b, c), (a, c, d)])
shell_mesh = bpy.data.meshes.new("Upper radome cut at latitude 35 S")
shell_mesh.from_pydata(shell_vertices, [], shell_faces)
shell_mesh.update()
shell = bpy.data.objects.new("Transparent upper geodesic radome shell", shell_mesh)
bpy.context.collection.objects.link(shell)
shell.data.materials.append(shell_mat)
wire = shell.modifiers.new("Geodesic frame", "WIREFRAME")
wire.thickness = 0.012
wire.material_offset = 0
shell.data.materials.append(frame_mat)

# Supporting reinforced-concrete cuboid and visible maintenance/access opening.
cut_height = radius * math.sin(lower_cut_latitude)
base_width = 4.0
base_depth = 4.0
base_height = 3.0
bpy.ops.mesh.primitive_cube_add(size=1, location=shell_center + Vector((0, 0, cut_height - base_height / 2)))
base = bpy.context.object
base.name = "Reinforced concrete radome base 4x4x2 m"
base.dimensions = (base_width, base_depth, base_height)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
base.data.materials.append(base_mat)
base_bevel = base.modifiers.new("Concrete edge bevel", "BEVEL")
base_bevel.width = 0.10
base_bevel.segments = 3
bpy.ops.mesh.primitive_cube_add(size=1, location=shell_center + Vector((0, -base_depth / 2 - 0.02, cut_height - base_height + 0.85)))
opening = bpy.context.object
opening.name = "Concrete base interior access opening"
opening.dimensions = (1.70, 0.08, 2.20)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
opening.data.materials.append(opening_mat)
for x in (-0.92, 0.92):
    cylinder_between("Access opening vertical frame", shell_center + Vector((x, -base_depth / 2 - 0.08, cut_height - base_height + 0.05)), shell_center + Vector((x, -base_depth / 2 - 0.08, cut_height - base_height + 2.25)), 0.035, warning_mat)
cylinder_between("Access opening top frame", shell_center + Vector((-0.92, -base_depth / 2 - 0.08, cut_height - base_height + 2.25)), shell_center + Vector((0.92, -base_depth / 2 - 0.08, cut_height - base_height + 2.25)), 0.035, warning_mat)

# Highlighted face on right/front of radome.
face_center = Vector((-1.22, -1.05, 1.25))
face_normal = (face_center - shell_center).normalized()
edge_a = Vector((-1.32, -1.55, 1.45))
edge_b = Vector((-1.25, -0.40, 1.48))
edge_c = Vector((-1.05, -1.00, 2.45))
triangle_mesh("Highlighted radome face", [edge_a, edge_b, edge_c], face_mat, 0.015)

# Exploded triangular pyramid: the triangular face is on the outer surface
# (x=0) and the apex points inward (-X), into the radome volume.
offset = Vector((1.55, 0.0, 0.4))
base = [offset + Vector((0.0, -1.20, -0.85)), offset + Vector((0.0, 1.20, -0.85)), offset + Vector((0.0, 0.0, 1.22))]
apex = offset + Vector((-1.35, 0.0, 0.0))
for i in range(3):
    triangle_mesh("Pyramid structural side", [base[i], base[(i + 1) % 3], apex], dielectric_mat, 0.025)
triangle_mesh("Outer triangular RF face", base, face_mat, 0.025)

# Exploded layers just behind the external face, separated toward the interior (-X).
for index, (x, mat, name) in enumerate([(0.18, dielectric_mat, "Dielectric skin and honeycomb"), (0.42, board_mat, "RF aperture and PCB"), (0.68, shield_mat, "Shielded ADC ASIC band modules")]):
    x = -x
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

# External antenna: the support strut from the inward apex continues as the
# Yagi boom. The boom and support are collinear; the parasitic elements are
# transverse to that common axis.
yagi_x = offset.x + 0.32
mast_base = apex
mast_top = Vector((yagi_x, 0.0, 0.0))
cylinder_between("Antenna support from inward pyramid apex", mast_base, mast_top, 0.065, mast_mat)
boom_end = Vector((offset.x + 2.75, 0.0, 0.0))
cylinder_between("Yagi boom extension of apex support", mast_top, boom_end, 0.045, yagi_mat)
# Reflector at bottom, driven folded loop, and directors.
cylinder_between("Yagi reflector", Vector((yagi_x, 0.0, 0.0)), Vector((yagi_x, 0.0, 0.78)), 0.035, yagi_mat)
for x, half in [(0.62, 0.47), (1.03, 0.43), (1.43, 0.39), (1.83, 0.35), (2.23, 0.31), (2.62, 0.27)]:
    x_position = offset.x + x
    cylinder_between("Yagi transverse element", Vector((x_position, -half, 0.0)), Vector((x_position, half, 0.0)), 0.022, yagi_mat)
# Folded driven element as a rectangular rounded loop approximated by four cylinders.
loop_x = offset.x + 1.35
loop_half_y = 0.58
loop_half_z = 0.12
cylinder_between("Yagi folded driven element", Vector((loop_x, -loop_half_y, -loop_half_z)), Vector((loop_x, loop_half_y, -loop_half_z)), 0.032, yagi_gold)
cylinder_between("Yagi folded driven element", Vector((loop_x, loop_half_y, -loop_half_z)), Vector((loop_x, loop_half_y, loop_half_z)), 0.032, yagi_gold)
cylinder_between("Yagi folded driven element", Vector((loop_x, loop_half_y, loop_half_z)), Vector((loop_x, -loop_half_y, loop_half_z)), 0.032, yagi_gold)
cylinder_between("Yagi folded driven element", Vector((loop_x, -loop_half_y, loop_half_z)), Vector((loop_x, -loop_half_y, -loop_half_z)), 0.032, yagi_gold)
# Feed stalk and bracket.
cylinder_between("Yagi feed stalk", Vector((yagi_x, 0, 0)), Vector((offset.x + 1.38, 0, 0)), 0.035, yagi_gold)
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

# Interior view: central timing/fusion core, structural ribs and representative
# face modules mounted on the inside of the hemispherical radome.
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.24, location=shell_center)
core = bpy.context.object
core.name = "Internal timing and fusion core"
core.data.materials.append(ffasic_mat)
for direction in [Vector((1, 0, 1)), Vector((-1, 0, 1)), Vector((0, 1, 1)), Vector((0, -1, 1))]:
    direction.normalize()
    inner = shell_center + direction * 2.25
    cylinder_between("Internal structural radial tie", shell_center, inner, 0.035, frame_mat)
    cylinder_between("Internal optical and power trunk", shell_center + direction * 0.45, inner, 0.018, yagi_gold)
    # A compact shielded module at the inner shell boundary.
    bpy.ops.mesh.primitive_cube_add(size=1, location=inner)
    module = bpy.context.object
    module.name = "Mounted internal band module"
    module.dimensions = (0.50, 0.70, 0.46)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    module.data.materials.append(internal_module_mat)

# Internal service ring and three visible representative face junctions.
for z in (-0.58, 0.58):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.92, minor_radius=0.025, location=shell_center + Vector((0, 0, z)), rotation=(0, 0, 0))
    bpy.context.object.name = "Internal service ring"
    bpy.context.object.data.materials.append(frame_mat)
for angle in (0.0, 2.1, 4.2):
    p1 = shell_center + Vector((2.15 * math.cos(angle), 2.15 * math.sin(angle), 0.55))
    p2 = shell_center + Vector((2.15 * math.cos(angle + 0.45), 2.15 * math.sin(angle + 0.45), -0.45))
    cylinder_between("Internal triangular face junction", p1, p2, 0.045, frame_mat)

# Text labels placed in world space.
labels = [
    ("RADOME shell / casca", (-3.7, 0.0, 5.0), 0.22, white_mat),
    ("EXPLODED FACE / FACE EXPLODIDA", (3.0, -2.6, 4.3), 0.22, white_mat),
    ("2 m triangular face", (2.4, -2.35, 3.9), 0.18, yagi_gold),
    ("VHF Yagi boom = apex support axis", (3.2, -2.45, 3.55), 0.16, yagi_gold),
    ("shielded ADC + ASIC layers", (3.4, 2.1, 2.1), 0.14, white_mat),
    ("FFASIC / clock / fibre / DC", (3.7, 2.1, 0.4), 0.14, white_mat),
    ("REINFORCED CONCRETE BASE 4 m x 4 m x 3 m", (-0.2, -3.1, cut_height - 1.35), 0.16, warning_mat),
    ("ACCESS / ACESSO", (0.0, -3.2, cut_height - 1.05), 0.14, warning_mat),
]
for body, loc, size, mat in labels:
    text_obj(body, loc, size, mat)

# Ground plane and lighting.
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, cut_height - base_height - 0.22))
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

bpy.ops.object.camera_add(location=(12.5, -16.5, 7.0))
camera = bpy.context.object
camera.name = "Technical camera"
point_camera(camera, (0.3, 0.0, -0.65))
camera.data.lens = 52
bpy.context.scene.camera = camera

scene = bpy.context.scene

# Use NVIDIA CUDA explicitly for Cycles rendering.
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1280
scene.render.resolution_y = 800
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

# Second render: camera physically inside the transparent shell, looking toward
# the internal core and the mounted face modules.
bpy.ops.object.camera_add(location=(-4.85, -0.65, 2.75))
internal_camera = bpy.context.object
internal_camera.name = "Internal inspection camera"
point_camera(internal_camera, (-2.55, 2.15, 2.5))
internal_camera.data.lens = 26
scene.camera = internal_camera
scene.render.resolution_x = 1400
scene.render.resolution_y = 900
scene.render.filepath = INTERNAL_OUTPUT
# Keep the shell context visible without allowing it to occlude the interior.
shell_mat.diffuse_color = (0.22, 0.52, 0.68, 0.045)
shell_mat.node_tree.nodes.get("Principled BSDF").inputs["Alpha"].default_value = 0.045
for obj in bpy.data.objects:
    if obj.name.startswith("Internal service ring"):
        obj.hide_render = True
bpy.ops.render.render(write_still=True)
