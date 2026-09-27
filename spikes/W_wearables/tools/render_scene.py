"""Blender (headless) renderer for W's wearable previews.

usage: blender --background --factory-startup --python render_scene.py -- scene.json

scene.json:
  {"out_dir": "...", "res": [800, 1000], "engine": "CYCLES"|"BLENDER_EEVEE"|"BLENDER_WORKBENCH", "samples": 24,
   "objects": [{"name": str, "points": [[x,y,z]...] (DayZ model space), "faces": [[i,j,k(,l)]...],
                "uvs": [[u,v]... per point, p3d convention: origin top-left] | null,
                "face_uvs": [[[u,v]...] per face corner] | null  (overrides uvs),
                "texture": "png" | null, "color": [r,g,b,a], "smooth": true, "roughness": 0.8,
                "backface_cull": false}],
   "shots": [{"name": str, "target": [x,y,z] (DayZ), "dir": [dx,dy,dz] (DayZ, from target to camera),
              "dist": 3.0, "ortho": 1.9 | null, "lens": 50}]}

Coordinates: DayZ (x, y, z) -> Blender (x, z, y). That swap is a mirror, which also turns the p3d's
clockwise-from-outside faces into Blender's counter-clockwise-from-outside, so normals come out right.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
scene_path = argv[0]
S = json.load(open(scene_path))


def bl(p):
    return (p[0], p[2], p[1])


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_material(name, o):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = o.get("roughness", 0.85)
    col = o.get("color", [0.7, 0.7, 0.7, 1.0])
    if o.get("texture"):
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(os.path.abspath(o["texture"]))
        if o.get("tint"):
            mix = nt.nodes.new("ShaderNodeMix")
            mix.data_type = "RGBA"
            mix.blend_type = "MULTIPLY"
            mix.inputs[0].default_value = 1.0
            nt.links.new(tex.outputs["Color"], mix.inputs[6])
            mix.inputs[7].default_value = o["tint"]
            nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
        else:
            nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
        if o.get("alpha_from_texture"):
            nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
            try:
                mat.blend_method = "HASHED"
            except Exception:
                pass
    else:
        bsdf.inputs["Base Color"].default_value = col
    if o.get("show_backfaces", S.get("show_backfaces", False)):
        # QA: faces seen from behind render magenta - a wrong winding shows up at a glance
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        src = bsdf.inputs["Base Color"].links[0].from_socket if bsdf.inputs["Base Color"].links else None
        if src is not None:
            nt.links.new(src, mix.inputs[6])
        else:
            mix.inputs[6].default_value = bsdf.inputs["Base Color"].default_value
        mix.inputs[7].default_value = (1.0, 0.0, 0.8, 1.0)
        nt.links.new(geo.outputs["Backfacing"], mix.inputs[0])
        nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    elif o.get("cull", S.get("cull", False)):
        # game-like single-sided faces: back faces let the ray through
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mixs = nt.nodes.new("ShaderNodeMixShader")
        out = nt.nodes.get("Material Output")
        nt.links.new(geo.outputs["Backfacing"], mixs.inputs[0])
        nt.links.new(bsdf.outputs[0], mixs.inputs[1])
        nt.links.new(tr.outputs[0], mixs.inputs[2])
        nt.links.new(mixs.outputs[0], out.inputs["Surface"])
    mat.use_backface_culling = bool(o.get("backface_cull", False))
    return mat


def add_object(o):
    me = bpy.data.meshes.new(o["name"])
    verts = [bl(p) for p in o["points"]]
    faces = [list(f) for f in o["faces"]]
    me.from_pydata(verts, [], faces)
    me.update()
    uvs = o.get("uvs")
    fuv = o.get("face_uvs")
    if uvs or fuv:
        layer = me.uv_layers.new(name="UVMap")
        for poly in me.polygons:
            for k, li in enumerate(poly.loop_indices):
                if fuv:
                    u, v = fuv[poly.index][k]
                else:
                    u, v = uvs[me.loops[li].vertex_index]
                layer.data[li].uv = (u, 1.0 - v)
    if o.get("smooth", True):
        for poly in me.polygons:
            poly.use_smooth = True
    ob = bpy.data.objects.new(o["name"], me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(make_material(o["name"] + "_mat", o))
    return ob


def setup_world_and_lights():
    sc = bpy.context.scene
    world = bpy.data.worlds.new("W")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.78, 0.80, 0.83, 1)
    bg.inputs["Strength"].default_value = 0.55
    for name, rot, energy in (("key", (math.radians(50), 0, math.radians(35)), 3.2),
                              ("fill", (math.radians(65), 0, math.radians(-120)), 1.3),
                              ("rim", (math.radians(110), 0, math.radians(180)), 1.0)):
        ld = bpy.data.lights.new(name, "SUN")
        ld.energy = energy
        lo = bpy.data.objects.new(name, ld)
        lo.rotation_euler = rot
        sc.collection.objects.link(lo)
    # ground plane at y = 0 (DayZ)
    me = bpy.data.meshes.new("ground")
    s = 6.0
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [[0, 1, 2, 3]])
    g = bpy.data.objects.new("ground", me)
    sc.collection.objects.link(g)
    mat = bpy.data.materials.new("groundmat")
    mat.use_nodes = True
    mat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.55, 0.53, 0.50, 1)
    g.data.materials.append(mat)


def shoot(shot, out_dir, res):
    sc = bpy.context.scene
    cam_d = bpy.data.cameras.new(shot["name"])
    if shot.get("ortho"):
        cam_d.type = "ORTHO"
        cam_d.ortho_scale = shot["ortho"]
    else:
        cam_d.lens = shot.get("lens", 50)
    cam_d.clip_start = 0.01
    cam = bpy.data.objects.new(shot["name"], cam_d)
    sc.collection.objects.link(cam)
    t = Vector(bl(shot["target"]))
    dvec = Vector(bl(shot["dir"])).normalized()
    cam.location = t + dvec * shot.get("dist", 3.0)
    q = (t - cam.location).to_track_quat("-Z", "Y")
    cam.rotation_euler = q.to_euler()
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = shot.get("res", res)
    sc.render.filepath = os.path.join(out_dir, shot["name"] + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", sc.render.filepath)


def main():
    clear()
    sc = bpy.context.scene
    eng = S.get("engine", "CYCLES")
    sc.render.engine = eng
    if eng == "CYCLES":
        sc.cycles.device = "CPU"
        sc.cycles.samples = S.get("samples", 24)
        sc.cycles.use_denoising = True
        sc.cycles.max_bounces = 4
    sc.view_settings.view_transform = "Standard"
    sc.render.film_transparent = False
    setup_world_and_lights()
    for o in S["objects"]:
        add_object(o)
    os.makedirs(S["out_dir"], exist_ok=True)
    for shot in S["shots"]:
        shoot(shot, S["out_dir"], S.get("res", [800, 1000]))


main()
