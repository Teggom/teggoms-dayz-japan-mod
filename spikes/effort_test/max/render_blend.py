"""Blender (background) renders of the tansu MLODs for the contact sheet.

  blender --background --factory-startup --python render_blend.py -- <jobs.json>

Reads each p3d MLOD back from disk with the kit's reader (so the renders show what was written: faces, winding,
UVs, texture paths), maps p3d (x, y, z) -> Blender (x, z, y), and textures every face with the library PNG
(data/materials/textures/<stem>.png) of its .paa, plus its _nohq as a normal map (DirectX green flipped).
jobs.json: {"out_dir", "res": [w, h], "jobs": [{"out", "p3d", "lod": 1|2|3|"geo"|"view", "overlay": [lod, ...],
            "view": {"az", "el", "dist", "lens" | "ortho"}, "target": [x, y, z] (p3d), "human": [x, z] (p3d),
            "markers": [[x, y, z], ...], "zone": [x0, x1, z0, z1]}]}
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402

TEXPNG = os.path.join(DEV, "data", "materials", "textures")
_MATS = {}


def b(p):
    return (p[0], p[2], p[1])


def newell(pts):
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[(i + 1) % len(pts)]
        nx += (y0 - y1) * (z0 + z1)
        ny += (z0 - z1) * (x0 + x1)
        nz += (x0 - x1) * (y0 + y1)
    return (nx, ny, nz)


def tex_material(tex):
    if tex in _MATS:
        return _MATS[tex]
    stem = os.path.splitext(os.path.basename(tex.replace("\\", "/")))[0]
    m = bpy.data.materials.new(stem)
    m.use_nodes = True
    m.use_backface_culling = True          # single-sided like the game: a wrongly wound face would show as a hole
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    iron = "metal_iron" in stem
    bsdf.inputs["Roughness"].default_value = 0.42 if iron else 0.86
    bsdf.inputs["Metallic"].default_value = 0.55 if iron else 0.0
    png = os.path.join(TEXPNG, stem + ".png")
    if os.path.isfile(png):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(png, check_existing=True)
        nt.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
        print("MISSING texture png", png)
    nq = os.path.join(TEXPNG, stem[:-3] + "_nohq.png") if stem.endswith("_co") else ""
    if nq and os.path.isfile(nq):
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = bpy.data.images.load(nq, check_existing=True)
        tn.image.colorspace_settings.name = "Non-Color"
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        comb = nt.nodes.new("ShaderNodeCombineColor")
        inv = nt.nodes.new("ShaderNodeMath")
        inv.operation = "SUBTRACT"
        inv.inputs[0].default_value = 1.0
        nt.links.new(tn.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs[0], comb.inputs[0])
        nt.links.new(sep.outputs[1], inv.inputs[1])
        nt.links.new(inv.outputs[0], comb.inputs[1])
        nt.links.new(sep.outputs[2], comb.inputs[2])
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = 0.6
        nt.links.new(comb.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    _MATS[tex] = m
    return m


def plain(name, rgba, emit=0.0, rough=0.9):
    k = ("plain", name)
    if k in _MATS:
        return _MATS[k]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = rgba
    bs.inputs["Roughness"].default_value = rough
    if emit:
        bs.inputs["Emission Color"].default_value = rgba
        bs.inputs["Emission Strength"].default_value = emit
    _MATS[k] = m
    return m


def lod_mesh(lod, name, mat_override=None):
    verts, polys, uvs, mids, mats, mindex = [], [], [], [], [], {}
    for fverts, flags, tex, rvm in lod.faces:
        pts = [lod.points[v[0]] for v in fverts]
        outward = [-c for c in newell(pts)]                          # MLOD formula normal points INTO the solid
        bp = [b(p) for p in pts]
        buv = [(v[2], 1.0 - v[3]) for v in fverts]
        nb = newell(bp)
        ob = b(outward)
        if nb[0] * ob[0] + nb[1] * ob[1] + nb[2] * ob[2] < 0:
            bp, buv = bp[::-1], buv[::-1]
        base = len(verts)
        verts += bp
        uvs += buv
        polys.append(list(range(base, base + len(bp))))
        key = mat_override or tex or rvm or "none"
        if key not in mindex:
            mindex[key] = len(mats)
            mats.append(mat_override_mat(mat_override) if mat_override else
                        (tex_material(tex) if tex else plain("untextured", (0.5, 0.5, 0.5, 1))))
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


def mat_override_mat(key):
    return {"ghost": plain("ghost", (0.78, 0.76, 0.72, 1.0)),
            "geo": plain("geo", (0.85, 0.12, 0.10, 1.0), emit=1.5),
            "view": plain("view", (0.10, 0.35, 0.95, 1.0), emit=1.5)}[key]


def wire(ob, thick):
    md = ob.modifiers.new("wire", "WIREFRAME")
    md.thickness = thick
    md.use_replace = True
    return ob


def human(x, z):
    """1.8 m silhouette (p3d x, z on the floor)."""
    m = plain("human", (0.05, 0.05, 0.06, 1.0))
    bx, by = x, z
    parts = [("sphere", 0.11, (bx, by, 1.69)), ("cyl", (0.17, 0.62), (bx, by, 1.25)),
             ("cyl", (0.075, 0.94), (bx - 0.09, by, 0.47)), ("cyl", (0.075, 0.94), (bx + 0.09, by, 0.47)),
             ("cyl", (0.05, 0.66), (bx - 0.235, by, 1.18)), ("cyl", (0.05, 0.66), (bx + 0.235, by, 1.18))]
    for kind, sz, loc in parts:
        if kind == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=sz, location=loc, segments=16, ring_count=8)
        else:
            bpy.ops.mesh.primitive_cylinder_add(radius=sz[0], depth=sz[1], location=loc, vertices=12)
        bpy.context.active_object.data.materials.append(m)


def marker(p):
    m = plain("marker", (0.05, 0.85, 0.15, 1.0), emit=2.0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, location=b(p), segments=12, ring_count=6)
    bpy.context.active_object.data.materials.append(m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.004, depth=0.25, location=(p[0], p[2], p[1] + 0.125), vertices=6)
    bpy.context.active_object.data.materials.append(m)


def zone(x0, x1, z0, z1):
    m = plain("zone", (0.95, 0.75, 0.05, 1.0), emit=1.5)
    t = 0.008
    for (ax, bx_, az, bz) in ((x0, x1, z0, z0 + t), (x0, x1, z1 - t, z1), (x0, x0 + t, z0, z1), (x1 - t, x1, z0, z1)):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((ax + bx_) / 2, (az + bz) / 2, 0.002))
        o = bpy.context.active_object
        o.scale = (bx_ - ax, bz - az, 0.004)
        o.data.materials.append(m)


def setup(res):
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    try:
        sc.eevee.taa_render_samples = 48
    except AttributeError:
        pass
    for attr, val in (("use_gtao", True), ("use_shadows", True), ("use_raytracing", True)):
        try:
            setattr(sc.eevee, attr, val)
        except AttributeError:
            pass
    w = bpy.data.worlds.new("sky")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.74, 0.75, 0.78, 1.0)
    bg.inputs[1].default_value = 0.55
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.4
    sun.data.angle = math.radians(6)
    sc.collection.objects.link(sun)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    return cam, sun


def clear():
    for ob in list(bpy.data.objects):
        if ob.type == "MESH":
            bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)


def place_camera(cam, sun, target, v):
    az, el = math.radians(v["az"]), math.radians(v["el"])
    d = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    t = Vector(b(target))
    cam.location = t + d * v.get("dist", 6.0)
    cam.rotation_mode = "QUATERNION"
    cam.rotation_quaternion = (-d).to_track_quat("-Z", "Y")
    if "ortho" in v:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = v["ortho"]
    else:
        cam.data.type = "PERSP"
        cam.data.lens = v.get("lens", 50)
    cam.data.clip_start = 0.02
    cam.data.clip_end = 100
    # sun from the camera's side, 40 deg to its left, 50 deg up (so the faces the camera sees are lit)
    sa = az + math.radians(v.get("sun_off", 40))
    se = math.radians(v.get("sun_el", 50))
    sd = Vector((math.sin(sa) * math.cos(se), math.cos(sa) * math.cos(se), math.sin(se)))
    sun.rotation_mode = "QUATERNION"
    sun.rotation_quaternion = (-sd).to_track_quat("-Z", "Y")


def pick(lods, which):
    if which == "geo":
        return mlod.find_lod(lods, mlod.LOD_GEOMETRY)
    if which == "view":
        return mlod.find_lod(lods, mlod.LOD_VIEW_GEOMETRY)
    return mlod.find_lod(lods, float(which))


def main():
    spec = json.load(open(sys.argv[sys.argv.index("--") + 1], encoding="utf-8"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam, sun = setup(tuple(spec["res"]))
    os.makedirs(spec["out_dir"], exist_ok=True)
    floor = plain("floor", (0.40, 0.38, 0.34, 1.0))
    cache = {}
    for job in spec["jobs"]:
        clear()
        if job["p3d"] not in cache:
            cache[job["p3d"]] = mlod.read_mlod(job["p3d"])
        lods = cache[job["p3d"]]
        lod = pick(lods, job.get("lod", 1))
        lod_mesh(lod, "model", mat_override="ghost" if job.get("ghost") else None)
        for ov in job.get("overlay", []):
            o = lod_mesh(pick(lods, ov), "ov_" + str(ov), mat_override=ov)
            wire(o, 0.006)
        if job.get("human"):
            human(job["human"][0], job["human"][1])
        for mk in job.get("markers", []):
            marker(mk)
        if job.get("zone"):
            zone(*job["zone"])
        bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.0005))
        bpy.context.active_object.data.materials.append(floor)
        place_camera(cam, sun, job["target"], job["view"])
        bpy.context.scene.render.filepath = os.path.join(spec["out_dir"], job["out"] + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", job["out"])
    if spec.get("save_blend"):
        # both states side by side, every LOD of each as its own object (Resolution 2/3 and the collision LODs
        # hidden), for inspection in Blender; textures are linked from data/materials/textures, not packed
        clear()
        for k, (p3d, dx) in enumerate(spec["save_blend"]["models"]):
            lods = cache.get(p3d) or mlod.read_mlod(p3d)
            for which, hide in ((1, False), (2, True), (3, True), ("geo", True), ("view", True)):
                l = pick(lods, which)
                if l is None:
                    continue
                o = lod_mesh(l, "%s_%s" % (os.path.basename(p3d)[:-4], which),
                             mat_override=which if which in ("geo", "view") else None)
                o.location.x += dx
                o.hide_render = hide
                o.hide_set(hide)
        bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.0005))
        bpy.context.active_object.data.materials.append(floor)
        bpy.ops.wm.save_as_mainfile(filepath=spec["save_blend"]["path"])
        print("saved", spec["save_blend"]["path"])


main()
