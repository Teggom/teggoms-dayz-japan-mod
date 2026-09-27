"""Headless Blender preview renders of the spike-A weapons (OBJ exports from tools/build.py).

  blender --background --python tools/render_blender.py -- <out_dir> <name> [<name> ...]

OBJ axes: build.py mirrors p3d X, so after the importer's (forward -Z, up Y) conversion
Blender X = -p3d X, Blender Y = -p3d Z, Blender Z = p3d Y (the model's long axis is up for melee).
"""
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
NAMES = argv[1:]
HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(os.path.dirname(HERE), "work", "obj")

# material look per rvmat stem (the OBJ material name is "<rvmat>__<texture>")
LOOK = {
    "jp_steel": (0.95, 0.18), "jp_iron": (0.7, 0.55), "jp_brass": (0.9, 0.3), "jp_silk": (0.0, 0.75),
    "jp_lacquer": (0.0, 0.25), "jp_bow": (0.0, 0.35), "jp_hemp": (0.0, 0.9), "jp_bamboo": (0.0, 0.45),
    "jp_feather": (0.0, 0.9),
}

# per model: list of (view name, camera direction from target (Blender axes), ortho padding)
VIEWS = {
    "jp_katana": [("side", (1, 0, 0)), ("edge", (0, -1, 0)), ("three_quarter", (0.8, -0.5, 0.35)), ("hilt", (1, -0.6, 0.2))],
    "jp_yari": [("side", (0, -1, 0)), ("three_quarter", (0.8, -0.6, 0.3)), ("head", (0.7, -0.7, 0.2))],
    "jp_yumi": [("side", (0, -1, 0)), ("three_quarter", (0.6, -0.8, 0.25)), ("grip", (0.4, -0.9, 0.2))],
    "jp_yumi_xb": [("side", (0, -1, 0)), ("three_quarter", (0.6, -0.8, 0.25))],
    "jp_ya": [("side", (1, 0.0, 0.0)), ("three_quarter", (0.7, 0.5, 0.5)), ("fletch", (0.7, 0.4, 0.6))],
}
# close-up framing: fraction of the bounding box to frame, and its centre (in fractions of the box)
CLOSE = {"hilt": (0.36, 0.17), "head": (0.2, 0.9), "grip": (0.18, 0.33), "fletch": (0.25, 0.15)}
# close-ups that must centre on a given p3d point (converted to Blender axes: X=-x, Y=-z, Z=y)
FOCUS = {("jp_yumi", "grip"): (-0.037, 0.03, -0.049)}


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    try:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        try:
            sc.render.engine = "BLENDER_EEVEE"
        except TypeError:
            sc.render.engine = "CYCLES"
    sc.render.resolution_x = 1400
    sc.render.resolution_y = 1000
    sc.render.film_transparent = False
    world = bpy.data.worlds.new("w")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.78, 0.80, 0.83, 1)
    bg.inputs[1].default_value = 0.9
    return sc


def import_obj(name):
    path = os.path.join(OBJ, name + ".obj")
    bpy.ops.wm.obj_import(filepath=path, forward_axis="NEGATIVE_Z", up_axis="Y")
    objs = [o for o in bpy.context.selected_objects if o.type == "MESH"]
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or not m.use_nodes:
                continue
            stem = m.name.split("__")[0].split(".")[0]
            met, rough = LOOK.get(stem, (0.0, 0.6))
            bsdf = m.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Metallic"].default_value = met
                bsdf.inputs["Roughness"].default_value = rough
        o.data.shade_smooth() if hasattr(o.data, "shade_smooth") else None
    return objs


def bounds(objs):
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))
    return lo, hi


def lights(centre, size):
    for i, (d, e) in enumerate((((1, -1, 1.2), 3.5), ((-1.2, 0.6, 0.8), 1.6), ((0.2, 1, -0.4), 0.8))):
        ld = bpy.data.lights.new("sun%d" % i, "SUN")
        ld.energy = e
        ob = bpy.data.objects.new("sun%d" % i, ld)
        bpy.context.scene.collection.objects.link(ob)
        dv = Vector(d).normalized()
        ob.rotation_euler = dv.to_track_quat("Z", "Y").to_euler()


def camera(centre, direction, span, sc):
    cd = bpy.data.cameras.new("cam")
    cd.type = "ORTHO"
    cd.ortho_scale = span
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    d = Vector(direction).normalized()
    cam.location = centre + d * 10.0
    up = "Y"
    cam.rotation_euler = (-d).to_track_quat("-Z", up).to_euler()
    cd.clip_end = 50
    sc.camera = cam
    return cam


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in NAMES:
        for view, direction in VIEWS[name]:
            sc = reset()
            objs = import_obj(name)
            lo, hi = bounds(objs)
            centre = (lo + hi) / 2
            size = max(hi - lo)
            span = size * 1.08
            if view in CLOSE:
                frac, pos = CLOSE[view]
                span = size * frac
                # centre along the longest axis at `pos`
                ax = max(range(3), key=lambda k: hi[k] - lo[k])
                centre = centre.copy()
                centre[ax] = lo[ax] + (hi[ax] - lo[ax]) * pos
            ax_long = max(range(3), key=lambda k: hi[k] - lo[k])
            if ax_long == 2 and view not in CLOSE:
                sc.render.resolution_x, sc.render.resolution_y = 900, 1400
            if (name, view) in FOCUS:
                fx, fy, fz = FOCUS[(name, view)]
                centre = Vector((-fx, -fz, fy))
            lights(centre, size)
            camera(centre, direction, span, sc)
            sc.render.filepath = os.path.join(OUT, "%s_%s.png" % (name, view))
            bpy.ops.render.render(write_still=True)
            print("RENDERED", sc.render.filepath)


main()
