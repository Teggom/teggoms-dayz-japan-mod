"""Blender (background) renders of JP parts for the contact sheets.

  blender --background --factory-startup --python render_parts.py -- <jobs.json>

jobs.json: {"out_dir": ..., "jobs": [{"name": part name, "scale": ortho scale m, "view": "3q"|"front"|"top"|"back",
            "context": [[builder name, variant, yaw, [x, y, z]], ...], "extra": {...}}]}
Resolution-1 LOD with the library textures (data/materials/textures/*_co.png at the part's wear), a 1.8 m human
silhouette beside the part, Standard view transform (authored colours), ortho camera at a fixed scale per sheet.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, registry  # noqa: E402

REG = {p + v: (p, v, fn) for p, v, fn in registry.ALL}
_MATS = {}


def to_b(p):
    return (p[0], p[2], p[1])


def material(key, wear, tint=None):
    k = (key, wear, tint)
    if k in _MATS:
        return _MATS[k]
    m = bpy.data.materials.new("%s%s" % (key, wear))
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = 0.85
    png = core.png_path(key, wear)
    if os.path.isfile(png):
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(png, check_existing=True)
        if tint:
            mixn = nt.nodes.new("ShaderNodeMixRGB")
            mixn.blend_type = "MULTIPLY"
            mixn.inputs[0].default_value = 1.0
            mixn.inputs[2].default_value = tint + (1.0,)
            nt.links.new(tex.outputs["Color"], mixn.inputs[1])
            nt.links.new(mixn.outputs[0], bsdf.inputs["Base Color"])
        else:
            nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
        if core.mat_info(key)["alpha"]:
            nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
            try:
                m.surface_render_method = "BLENDED"
            except Exception:
                m.blend_method = "BLEND"
    else:
        bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
    _MATS[k] = m
    return m


def plain(name, rgb):
    k = ("plain", name)
    if k in _MATS:
        return _MATS[k]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = rgb + (1.0,)
    b.inputs["Roughness"].default_value = 0.9
    _MATS[k] = m
    return m


def part_mesh(part, name, lod=1, tint=None, open_doors=0.0):
    verts, polys, uvs, mids = [], [], [], []
    mats, mindex = [], {}
    shift = {}
    if open_doors:
        for d in part.doors:
            for a in d.anims:
                ax = a["axis"]
                dv = [(ax[1][k] - ax[0][k]) for k in range(3)]
                if a["type"] == "translation":
                    shift[a["bone"]] = tuple(dv[k] * a["amount"] * open_doors for k in range(3))
    for s in part.solids:
        if lod not in s.vis:
            continue
        off = shift.get(s.door, (0.0, 0.0, 0.0))
        for fi in range(len(s.faces)):
            pts = [to_b(core.add(p, off)) for p in s.face_points(fi)]
            n = to_b(s.fn[fi])
            nn = core.newell(pts)
            order = list(range(len(pts)))
            if core.dot(nn, n) < 0:
                order = order[::-1]
            base = len(verts)
            verts += [pts[i] for i in order]
            polys.append(list(range(base, base + len(pts))))
            uvs += [(s.fuv[fi][i][0], 1.0 - s.fuv[fi][i][1]) for i in order]
            key = (s.fm[fi], part.wear_of(s.fm[fi]))
            if key not in mindex:
                mindex[key] = len(mats)
                mats.append(material(key[0], key[1], tint))
            mids.append(mindex[key])
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], polys)
    uv = me.uv_layers.new(name="UVMap")
    for i, loop in enumerate(me.loops):
        uv.data[i].uv = uvs[loop.vertex_index]
    for m in mats:
        me.materials.append(m)
    for i, mi in enumerate(mids):
        me.polygons[i].material_index = mi
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def human(x, z, y0=0.0):
    """1.8 m silhouette: head, torso, legs, arms (dark, flat)."""
    m = plain("human", (0.05, 0.05, 0.06))
    obs = []

    def add(op, **kw):
        op(**kw)
        ob = bpy.context.active_object
        ob.data.materials.append(m)
        obs.append(ob)
    add(bpy.ops.mesh.primitive_uv_sphere_add, radius=0.11, location=(x, z, y0 + 1.69), segments=16, ring_count=8)
    add(bpy.ops.mesh.primitive_cylinder_add, radius=0.17, depth=0.62, location=(x, z, y0 + 1.25), vertices=12)
    for dx in (-0.09, 0.09):
        add(bpy.ops.mesh.primitive_cylinder_add, radius=0.075, depth=0.94, location=(x + dx, z, y0 + 0.47), vertices=10)
    for dx in (-0.235, 0.235):
        add(bpy.ops.mesh.primitive_cylinder_add, radius=0.05, depth=0.66, location=(x + dx, z, y0 + 1.18), vertices=8)
    return obs


def setup(res):
    sc = bpy.context.scene
    try:
        sc.render.engine = "BLENDER_EEVEE"
    except TypeError:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    try:
        sc.eevee.taa_render_samples = 24
    except AttributeError:
        pass
    w = bpy.data.worlds.new("sky")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.80, 0.82, 0.85, 1.0)
    bg.inputs[1].default_value = 0.75
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.2
    sun.data.angle = math.radians(4)
    sun.rotation_euler = (math.radians(48), math.radians(8), math.radians(35))
    sc.collection.objects.link(sun)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    return cam


def clear_objects():
    for ob in list(bpy.data.objects):
        if ob.type == "MESH":
            bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)


def look(cam, target, view, scale, dist=40.0, lens=None):
    az, el = {"3q": (35, 22), "front": (0, 8), "top": (0, 88), "back": (200, 22), "3q_low": (35, 10),
              "3q_left": (-35, 22), "under": (20, -25), "side": (90, 10)}[view]
    a, e = math.radians(az), math.radians(el)
    d = Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
    cam.location = Vector(target) + d * dist
    cam.rotation_mode = "QUATERNION"
    cam.rotation_quaternion = (-d).to_track_quat("-Z", "Y")
    if lens:
        cam.data.type = "PERSP"
        cam.data.lens = lens
    else:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = scale
    cam.data.clip_start = 0.1
    cam.data.clip_end = 300


def build(name):
    p, v, fn = REG[name]
    return fn(v)


def main():
    jf = sys.argv[sys.argv.index("--") + 1]
    spec = json.load(open(jf, encoding="utf-8"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = setup(tuple(spec.get("res", (640, 520))))
    os.makedirs(spec["out_dir"], exist_ok=True)
    gm = plain("ground", (0.36, 0.37, 0.33))
    for job in spec["jobs"]:
        clear_objects()
        if job.get("assembly"):
            import assembly  # noqa: E402
            part = assembly.build()
            if job.get("no_roof"):
                part.solids = [s_ for s_ in part.solids if max(v[1] for v in s_.verts) < 2.72 or s_.door]
        else:
            part = build(job["name"])
        if job.get("wear"):
            part.wear = job["wear"]
        dy = 0.0
        if job.get("drop"):                      # lower an elevated sample (roof parts) onto the ground for the sheet
            dy = -part.bbox()[2] + 0.02
            part = part.transformed(0.0, (0.0, dy, 0.0))
        part_mesh(part, "part", lod=job.get("lod", 1), open_doors=job.get("open", 0.0))
        for cname, yaw, t in job.get("context", []):
            cp = build(cname).transformed(yaw, (t[0], t[1] + dy, t[2]))
            part_mesh(cp, "ctx_" + cname, tint=None if job.get("ctx_plain") else (0.8, 0.8, 0.8))
        b = part.bbox()
        hx = b[1] + 0.55 if not job.get("human_at") else job["human_at"][0]
        hz = (b[4] + b[5]) / 2 if not job.get("human_at") else job["human_at"][1]
        hy = job.get("human_y", 0.0)
        if not job.get("no_human"):
            human(hx, hz, hy)
        if not job.get("no_ground"):
            bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, min(0.0, b[2]) - 0.002 if job.get("ground_at_min")
                                                                 else job.get("ground_y", -0.002)))
            bpy.context.active_object.data.materials.append(gm)
        tgt = job.get("target") or ((min(b[0], hx - 0.3) + max(b[1], hx + 0.3)) / 2, (b[4] + b[5]) / 2,
                                    (min(b[2], hy) + max(b[3], hy + 1.8)) / 2)
        look(cam, to_b(tgt) if job.get("target") else (tgt[0], tgt[1], tgt[2]), job.get("view", "3q"), job["scale"],
             lens=job.get("lens"))
        bpy.context.scene.render.filepath = os.path.join(spec["out_dir"], job.get("out", job["name"]) + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", job.get("out", job["name"]))


main()
