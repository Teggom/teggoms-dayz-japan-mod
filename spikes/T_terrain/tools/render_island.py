"""Blender (headless) oblique render of the island: heightmap mesh + brightened satellite + simple tree cones.

    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background --python render_island.py -- <out.png>

Reads data/T_terrain/render_input.npz (written by build_world.py: h, sat, trees). Preview only - nothing here
goes into the game.
"""
import math
import os
import sys

import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[0] if argv else os.path.join(DEV, "spikes", "T_terrain", "previews", "render_oblique.png")
view = argv[1] if len(argv) > 1 else "south"
d = np.load(os.path.join(DEV, "data", "T_terrain", "render_input.npz"))
h = d["h"].astype(np.float64)
trees = d["trees"]
n = h.shape[0]
cell = 2048.0 / n
step = 2                                   # 256 x 256 mesh is plenty for a preview
hs = h[::step, ::step]
m = hs.shape[0]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
verts = []
for j in range(m):
    for i in range(m):
        verts.append((i * cell * step, j * cell * step, max(hs[j, i], -40.0)))
faces = []
for j in range(m - 1):
    for i in range(m - 1):
        a = j * m + i
        faces.append((a, a + 1, a + m + 1, a + m))
mesh = bpy.data.meshes.new("terrain")
mesh.from_pydata(verts, [], faces)
mesh.update()
uv = mesh.uv_layers.new(name="uv")
for poly in mesh.polygons:
    for li in poly.loop_indices:
        vi = mesh.loops[li].vertex_index
        x, y, _ = verts[vi]
        uv.data[li].uv = (x / 2048.0, y / 2048.0)
obj = bpy.data.objects.new("terrain", mesh)
scene.collection.objects.link(obj)
for p in mesh.polygons:
    p.use_smooth = True

img = bpy.data.images.load(os.path.join(DEV, "data", "T_terrain", "satellite_bright_full.png"))
mat = bpy.data.materials.new("sat")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes.get("Principled BSDF")
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = img
nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.95
obj.data.materials.append(mat)

# sea plane
bpy.ops.mesh.primitive_plane_add(size=6000, location=(1024, 1024, 0.0))
sea = bpy.context.active_object
sm = bpy.data.materials.new("sea")
sm.use_nodes = True
sb = sm.node_tree.nodes.get("Principled BSDF")
sb.inputs["Base Color"].default_value = (0.05, 0.16, 0.22, 1)
sb.inputs["Roughness"].default_value = 0.15
sea.data.materials.append(sm)

# trees as dark cones (a sample, to keep the render quick)
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=3.5, depth=14, location=(0, 0, -1000))
cone = bpy.context.active_object
tm = bpy.data.materials.new("tree")
tm.use_nodes = True
tm.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.05, 0.12, 0.04, 1)
cone.data.materials.append(tm)
for k, (x, y, z, s) in enumerate(trees[::2]):
    c = bpy.data.objects.new("t%d" % k, cone.data)
    c.location = (x, y, z + 7 * s)
    c.scale = (s, s, s)
    scene.collection.objects.link(c)

sun = bpy.data.lights.new("sun", "SUN")
sun.energy = 4.0
so = bpy.data.objects.new("sun", sun)
so.rotation_euler = (math.radians(50), 0, math.radians(-40))
scene.collection.objects.link(so)
world = bpy.data.worlds.new("w")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.7, 0.9, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.8
scene.world = world

cam = bpy.data.cameras.new("cam")
cam.lens = 28
cam.clip_end = 20000
co = bpy.data.objects.new("cam", cam)
scene.collection.objects.link(co)
if view == "yard":
    co.location = (1024, 760, 140)
    target = (1024, 1080, 30)
else:
    co.location = (1024, -900, 900)
    target = (1024, 1150, 60)
dx, dy, dz = target[0] - co.location[0], target[1] - co.location[1], target[2] - co.location[2]
co.rotation_euler = (math.atan2(math.hypot(dx, dy), -dz), 0, math.atan2(dy, dx) - math.pi / 2)
scene.camera = co
scene.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.filepath = out
bpy.ops.render.render(write_still=True)
print("rendered", out)
