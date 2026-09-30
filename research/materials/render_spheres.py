"""Blender (background) script: render one lit sphere per texture set for the contact sheets.

  blender --background --factory-startup --python render_spheres.py -- jobs.json

jobs.json: [{"co": png, "nohq_gl": png (OpenGL green), "smdi": png, "tile_m": float, "out": png}, ...]
Principled BSDF: base colour = _co, normal = _nohq, specular = smdi.G, roughness from smdi.B (gloss).
Standard view transform so the sphere shows the texture colours as authored (no AgX/Filmic shift).
"""
import json
import math
import sys

import bpy

jobs = json.load(open(sys.argv[sys.argv.index("--") + 1], encoding="utf-8"))

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 24
sc.cycles.use_denoising = True
sc.render.resolution_x = sc.render.resolution_y = 300
sc.render.film_transparent = False
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"

world = bpy.data.worlds.new("w")
sc.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.42, 0.44, 0.47, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.55

bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=0.5)
sph = bpy.context.active_object
bpy.ops.object.shade_smooth()
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.2
sun.data.angle = math.radians(3)
sun.rotation_euler = (math.radians(50), math.radians(-35), math.radians(-30))
sc.collection.objects.link(sun)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.type = "ORTHO"
cam.data.ortho_scale = 1.08
cam.location = (0, -5, 0)
cam.rotation_euler = (math.radians(90), 0, 0)
sc.collection.objects.link(cam)
sc.camera = cam

mat = bpy.data.materials.new("m")
mat.use_nodes = True
nt = mat.node_tree
N, L = nt.nodes, nt.links
bsdf = N["Principled BSDF"]
tc = N.new("ShaderNodeTexCoord")
mp = N.new("ShaderNodeMapping")
L.new(tc.outputs["UV"], mp.inputs["Vector"])
ico, inor, ism = N.new("ShaderNodeTexImage"), N.new("ShaderNodeTexImage"), N.new("ShaderNodeTexImage")
for i in (ico, inor, ism):
    L.new(mp.outputs["Vector"], i.inputs["Vector"])
nm = N.new("ShaderNodeNormalMap")
L.new(ico.outputs["Color"], bsdf.inputs["Base Color"])
L.new(inor.outputs["Color"], nm.inputs["Color"])
L.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
sep = N.new("ShaderNodeSeparateColor")
L.new(ism.outputs["Color"], sep.inputs["Color"])
spec = N.new("ShaderNodeMath")
spec.operation = "MULTIPLY_ADD"
spec.inputs[1].default_value = 1.2
spec.inputs[2].default_value = 0.15
L.new(sep.outputs[1], spec.inputs[0])
L.new(spec.outputs[0], bsdf.inputs["Specular IOR Level"])
rough = N.new("ShaderNodeMath")
rough.operation = "MULTIPLY_ADD"
rough.inputs[1].default_value = -1.3
rough.inputs[2].default_value = 0.95
rough.use_clamp = True
L.new(sep.outputs[2], rough.inputs[0])
L.new(rough.outputs[0], bsdf.inputs["Roughness"])
sph.data.materials.append(mat)

for j in jobs:
    for node, key, cs in ((ico, "co", "sRGB"), (inor, "nohq_gl", "Non-Color"), (ism, "smdi", "Non-Color")):
        img = bpy.data.images.load(j[key], check_existing=False)
        img.colorspace_settings.name = cs
        old = node.image
        node.image = img
        if old is not None:
            bpy.data.images.remove(old)
    # UV sphere: u runs around (2 pi r = 3.14 m), v pole to pole (pi r = 1.57 m) -> real-world texel scale
    # tile_v_m (optional, B1 2026-09-29): non-square tiles such as one tatami mat per texture (1.82 x 0.91 m)
    mp.inputs["Scale"].default_value = (math.pi / j["tile_m"], math.pi * 0.5 / j.get("tile_v_m", j["tile_m"]), 1)
    sc.render.filepath = j["out"]
    bpy.ops.render.render(write_still=True)
    print("rendered", j["out"])
