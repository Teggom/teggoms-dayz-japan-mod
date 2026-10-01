#!/usr/bin/env python3
r"""FB1 viewer: render registry buildings from their MLOD (Resolution 1 by default) the way the ENGINE draws them:
face orientation from the p3d winding (formula normal points inward, jpparts/mlod.py) and BACKFACE CULLING on, so a
face wound the wrong way disappears (the C3 / SH1 renders orient faces by the stored normals and draw both sides).

  python spikes/FB1/cullview.py <out.png> --keys k1,k2,... --cam x,y,z --at x,y,z [--lens 24] [--lod 1] [--res 1280x800]
         [--mlod path@x,z,yaw ...]   (extra MLODs at a world spot, e.g. a prop)
World coordinates: x east, y height ASL (the yard is 25.0), z north. Proxies are not drawn.
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
BLD = os.path.join(DEV, "buildings")
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
for p in (BLD, KIT, os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)


def faces_world(mp, pos, yaw, lodres):
    from jpparts import mlod, proxies as PX
    from jpkit import loot as bloot
    lod = next(l for l in mlod.read_mlod(mp) if abs(l.resolution - lodres) < 1e-3)
    lod = PX.strip(lod)
    out = []
    for fv, _, tex, mat in lod.faces:
        pts = [lod.points[v[0]] for v in fv]
        n = mlod._normalize(mlod._face_formula_normal(pts))
        wpts = [bloot.model_to_world(p, pos, yaw) for p in pts]
        # outward = -formula normal, rotated like the points
        a = bloot.model_to_world((0.0, 0.0, 0.0), pos, yaw)
        b = bloot.model_to_world((-n[0], -n[1], -n[2]), pos, yaw)
        out.append({"p": [list(q) for q in wpts], "o": [b[i] - a[i] for i in range(3)],
                    "uv": [[v[2], v[3]] for v in fv], "t": os.path.basename(tex)})
    return out


def collect(keys, extra, lodres):
    import registry
    import pipeline
    allf = []
    for k in keys:
        b = registry.get(k)
        rec = json.load(open(pipeline.record_path(b), "rb"))
        mp = os.path.join(pipeline.bdir(b), "out", rec["name"] + ".p3d")
        for pl in b["placements"]:
            allf += faces_world(mp, pl["pos"], pl["yaw"], lodres)
    for e in extra:
        path, x, z, yaw = e.rsplit("@", 1)[0], *[float(v) for v in e.rsplit("@", 1)[1].split(",")]
        allf += faces_world(path, (x, 25.0, z), yaw, lodres)
    return allf


def blender(spec):
    import bpy
    from mathutils import Vector
    d = json.load(open(spec, "rb"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    try:
        sc.render.engine = "BLENDER_EEVEE"
    except TypeError:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.render.resolution_x, sc.render.resolution_y = d["res"]
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("sky")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes.get("Background").inputs[0].default_value = (0.55, 0.75, 0.95, 1.0)
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
    sc.collection.objects.link(sun)
    mats = {}

    def mat_for(t):
        if t in mats:
            return mats[t]
        m = bpy.data.materials.new(t)
        m.use_nodes = True
        m.use_backface_culling = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Roughness"].default_value = 0.9
        png = os.path.join(d["texpng"], t.replace(".paa", ".png"))
        if os.path.isfile(png):
            tx = m.node_tree.nodes.new("ShaderNodeTexImage")
            tx.image = bpy.data.images.load(png, check_existing=True)
            m.node_tree.links.new(tx.outputs["Color"], bsdf.inputs["Base Color"])
        else:
            bsdf.inputs["Base Color"].default_value = (0.9, 0.2, 0.9, 1)
        mats[t] = m
        return m
    verts, polys, uvs, mids, ml = [], [], [], [], []
    for f in d["faces"]:
        bp = [(p[0], p[2], p[1]) for p in f["p"]]
        want = (f["o"][0], f["o"][2], f["o"][1])
        nx = ny = nz = 0.0
        for i in range(len(bp)):
            x0, y0, z0 = bp[i]
            x1, y1, z1 = bp[(i + 1) % len(bp)]
            nx += (y0 - y1) * (z0 + z1)
            ny += (z0 - z1) * (x0 + x1)
            nz += (x0 - x1) * (y0 + y1)
        order = list(range(len(bp)))
        if nx * want[0] + ny * want[1] + nz * want[2] < 0:
            order = order[::-1]
        base = len(verts)
        verts += [bp[i] for i in order]
        polys.append(list(range(base, base + len(bp))))
        uvs += [(f["uv"][i][0], 1.0 - f["uv"][i][1]) for i in order]
        if f["t"] not in ml:
            ml.append(f["t"])
        mids.append(ml.index(f["t"]))
    me = bpy.data.meshes.new("scene")
    me.from_pydata(verts, [], polys)
    uv = me.uv_layers.new(name="UVMap")
    for i, loop in enumerate(me.loops):
        uv.data[i].uv = uvs[loop.vertex_index]
    for k in ml:
        me.materials.append(mat_for(k))
    for i, mi in enumerate(mids):
        me.polygons[i].material_index = mi
    me.update()
    ob = bpy.data.objects.new("scene", me)
    sc.collection.objects.link(ob)
    # ground
    gm = bpy.data.meshes.new("ground")
    cx, cz = d["at"][0], d["at"][2]
    gm.from_pydata([(cx - 300, cz - 300, 24.99), (cx + 300, cz - 300, 24.99), (cx + 300, cz + 300, 24.99),
                    (cx - 300, cz + 300, 24.99)], [], [[0, 1, 2, 3]])
    go = bpy.data.objects.new("ground", gm)
    gmat = bpy.data.materials.new("g")
    gmat.use_nodes = True
    gmat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.4, 0.38, 0.3, 1)
    gm.materials.append(gmat)
    sc.collection.objects.link(go)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    c = Vector((d["cam"][0], d["cam"][2], d["cam"][1]))
    a = Vector((d["at"][0], d["at"][2], d["at"][1]))
    cam.location = c
    cam.rotation_mode = "QUATERNION"
    cam.rotation_quaternion = (a - c).to_track_quat("-Z", "Y")
    cam.data.lens = d["lens"]
    cam.data.clip_start = 0.05
    cam.data.clip_end = 600
    sc.render.filepath = d["out"]
    bpy.ops.render.render(write_still=True)


def main(argv):
    out = os.path.abspath(argv[0])
    opts = {"--keys": "", "--cam": None, "--at": None, "--lens": "24", "--lod": "1", "--res": "1280x800"}
    extra = []
    i = 1
    while i < len(argv):
        if argv[i] == "--mlod":
            extra.append(argv[i + 1])
        else:
            opts[argv[i]] = argv[i + 1]
        i += 2
    keys = [k for k in opts["--keys"].split(",") if k]
    faces = collect(keys, extra, float(opts["--lod"]))
    spec = {"faces": faces, "cam": [float(v) for v in opts["--cam"].split(",")],
            "at": [float(v) for v in opts["--at"].split(",")], "lens": float(opts["--lens"]),
            "res": [int(v) for v in opts["--res"].split("x")], "out": out, "texpng": TEXPNG}
    sp = out + ".json"
    with open(sp, "wb") as f:
        f.write(json.dumps(spec).encode("utf-8"))
    r = subprocess.run([BLENDER, "--background", "--python", os.path.abspath(__file__), "--", "--blender", sp],
                       capture_output=True, text=True, errors="replace")
    os.remove(sp)
    if not os.path.isfile(out):
        print(r.stdout[-3000:], r.stderr[-3000:])
        return 1
    print("wrote", out, "(%d faces)" % len(faces))
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        blender(sys.argv[sys.argv.index("--blender") + 1])
    else:
        sys.exit(main(sys.argv[1:]))
