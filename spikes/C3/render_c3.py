#!/usr/bin/env python3
r"""C3 render sheets (Blender in the background; parts/kit/render_parts.py helpers + the B4 prop-mesh reader).

  python spikes/C3/render_c3.py [kura|rooms|plans|street|hamlet ...] [--jobs N] [--compose]
  python spikes/C3/render_c3.py preview --keys k1,k2 [--jobs N]

Every building comes from its registry recipe (buildings/pipeline.py load_module), its furniture from the decorator
items (the prop MLOD masters at their proxy poses), its yard / street objects from its site() items, and the free
island dressing from test/placements/C3.csv. Sheets: research/production/contact_sheets/c3_*.jpg.
"""
import csv
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
BLD = os.path.join(DEV, "buildings")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(HERE, "renders")
SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
for p in (BLD, KIT, os.path.join(DEV, "spikes", "B_building", "kit"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

STREET_O = (1024.0, 1080.0)
HAMLET_O = (950.0, 1024.0)
SCENES = {"street": (STREET_O, (975.0, 1075.0, 1055.0, 1110.0)),
          "hamlet": (HAMLET_O, (920.0, 985.0, 985.0, 1065.0))}


def jobs_for(name):
    import c3_jobs
    return c3_jobs.JOBS.get(name, [])


# ================================================================================================ data (both sides)
def bundle(key):
    """(M, items, site, pts) of a registry building in its model frame."""
    import registry
    import pipeline
    b = registry.get(key)
    mod = pipeline.load_module(b)
    if "params" in b:
        M, floors, rooms = mod.model(name=b["name"], **b["params"])
    else:
        M, floors, rooms = mod.model()
    D = getattr(mod, "D", None)
    items = list(D.items) if D else []
    site = list(D.site) if D else []
    if hasattr(mod, "loot_points"):
        pts = mod.loot_points(floors)
    else:
        from jpkit import loot as bloot
        pts = [dict(p, container="lootFloor") for f in floors for p in bloot.floor_points(f)]
    return M, items, site, pts


def c3_csv_items():
    """The free island dressing (test/placements/C3.csv) as decorator-like items in WORLD coordinates."""
    from jpparts import decor as DC
    p = os.path.join(DEV, "test", "placements", "C3.csv")
    out = []
    if not os.path.isfile(p):
        return out
    cat = DC.catalog()
    for r in csv.DictReader(open(p)):
        name = os.path.basename(r["p3d"])[:-4]
        if name not in cat:
            continue
        out.append({"name": name, "info": cat[name], "x": float(r["x"]), "y": float(r["y_offset"]),
                    "z": float(r["z"]), "yaw": float(r["yaw_deg"])})
    return out


# ================================================================================================ Blender side
def blender_main(spec):
    import bpy
    import copy
    import math
    from mathutils import Vector, Euler
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    exec(compile(src, "render_parts.py", "exec"), g)
    import registry
    from jpparts import mlod, decor as DC
    from jpkit import loot as bloot
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"]((1280, 800))
    gm = g["plain"]("ground", (0.36, 0.37, 0.33))
    mats = {}

    def mat_for(tex):
        if tex in mats:
            return mats[tex]
        m = bpy.data.materials.new(os.path.basename(tex))
        m.use_nodes = True
        nt = m.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        bsdf.inputs["Roughness"].default_value = 0.85
        png = os.path.join(TEXPNG, os.path.basename(tex).replace(".paa", ".png"))
        if os.path.isfile(png):
            t = nt.nodes.new("ShaderNodeTexImage")
            t.image = bpy.data.images.load(png, check_existing=True)
            nt.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
            if tex.endswith("_ca.paa"):
                out = nt.nodes.get("Material Output")
                tr = nt.nodes.new("ShaderNodeBsdfTransparent")
                mix = nt.nodes.new("ShaderNodeMixShader")
                gt = nt.nodes.new("ShaderNodeMath")
                gt.operation = "GREATER_THAN"
                gt.inputs[1].default_value = 0.5
                nt.links.new(t.outputs["Alpha"], gt.inputs[0])
                nt.links.new(gt.outputs[0], mix.inputs[0])
                nt.links.new(tr.outputs[0], mix.inputs[1])
                nt.links.new(bsdf.outputs[0], mix.inputs[2])
                nt.links.new(mix.outputs[0], out.inputs["Surface"])
                try:
                    m.surface_render_method = "DITHERED"
                except Exception:
                    m.blend_method = "CLIP"
        else:
            bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
        mats[tex] = m
        return m

    lodcache = {}

    def prop_mesh(it, xf, cut_y=None):
        """it: a decorator item; xf: model-frame point -> scene point."""
        mp = it["info"]["master"]
        if mp not in lodcache:
            try:
                lodcache[mp] = next(l for l in mlod.read_mlod(mp) if abs(l.resolution - 1.0) < 1e-3)
            except Exception:
                lodcache[mp] = None
        lod = lodcache[mp]
        if lod is None:
            return
        verts, polys, uvs, mids, ml = [], [], [], [], []
        for fv, fl, tex, mat in lod.faces:
            loc = [lod.points[v[0]] for v in fv]
            pts_ = [xf(DC.to_model(it, q)) for q in loc]
            if cut_y is not None and min(p[1] for p in pts_) > cut_y:
                continue
            bp = [g["to_b"](p) for p in pts_]
            inward = lod.normals[fv[0][1]]
            a = xf(DC.to_model(it, loc[0]))
            b_ = xf(DC.to_model(it, (loc[0][0] - inward[0], loc[0][1] - inward[1], loc[0][2] - inward[2])))
            want = g["to_b"]((b_[0] - a[0], b_[1] - a[1], b_[2] - a[2]))
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
            uvs += [(fv[i][2], 1.0 - fv[i][3]) for i in order]
            if tex not in ml:
                ml.append(tex)
            mids.append(ml.index(tex))
        if not polys:
            return
        me = bpy.data.meshes.new(it["name"])
        me.from_pydata(verts, [], polys)
        uv = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uv.data[i].uv = uvs[loop.vertex_index]
        for k in ml:
            me.materials.append(mat_for(k))
        for i, mi in enumerate(mids):
            me.polygons[i].material_index = mi
        me.update()
        ob = bpy.data.objects.new(it["name"], me)
        bpy.context.scene.collection.objects.link(ob)

    def marker(p, rgb, r=0.08):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=g["to_b"](p), segments=10, ring_count=6)
        ob = bpy.context.active_object
        key = "mk%s" % str(rgb)
        m = bpy.data.materials.get(key)
        if m is None:
            m = bpy.data.materials.new(key)
            m.use_nodes = True
            b = m.node_tree.nodes.get("Principled BSDF")
            b.inputs["Base Color"].default_value = rgb + (1.0,)
            b.inputs["Emission Color"].default_value = rgb + (1.0,)
            b.inputs["Emission Strength"].default_value = 2.0
        ob.data.materials.append(m)

    cache = {}

    def get_bundle(key):
        if key not in cache:
            cache[key] = bundle(key)
        return cache[key]

    def cut_part(P, cut_y, drop_above=None):
        if cut_y is None and drop_above is None:
            return P
        Q = copy.copy(P)
        Q.solids = [s for s in P.solids if (cut_y is None or s.bbox()[2] < cut_y)]
        return Q

    os.makedirs(OUT, exist_ok=True)
    for out, cap, v in spec:
        g["clear_objects"]()
        res = v.get("res", [1280, 800])
        sc = bpy.context.scene
        sc.render.resolution_x, sc.render.resolution_y = res
        cut = v.get("cut_y")
        markers = []
        if v.get("scene"):
            (ox, oz), (bx0, bx1, bz0, bz1) = SCENES[v["scene"]]
            for b in registry.BUILDINGS:
                for pl in b.get("placements", []):
                    x, y, z = pl["pos"]
                    if not (bx0 <= x <= bx1 and bz0 <= z <= bz1):
                        continue
                    M, items, site, pts = get_bundle(b["key"])
                    yaw = pl["yaw"]
                    P = cut_part(M, cut).transformed(-yaw, (x - ox, 0.0, z - oz))
                    g["part_mesh"](P, b["key"], lod=1, open_doors=v.get("open", 0.0))

                    def xf(p, pos=(x, 0.0, z), yaw=yaw):
                        w = bloot.model_to_world(p, pos, yaw)
                        return (w[0] - ox, w[1], w[2] - oz)
                    for it in items + site:
                        prop_mesh(it, xf, cut)
            for it in c3_csv_items():
                if bx0 - 5 <= it["x"] <= bx1 + 5 and bz0 - 5 <= it["z"] <= bz1 + 5:
                    prop_mesh(it, lambda p: (p[0] - ox, p[1], p[2] - oz))
            for hx, hz in v.get("humans", []):
                g["human"](hx, hz, 0.0)
        else:
            M, items, site, pts = get_bundle(v["key"])
            g["part_mesh"](cut_part(M, cut), "bld", lod=1, open_doors=v.get("open", 0.0))
            for it in items + (site if v.get("site", True) else []):
                prop_mesh(it, lambda p: p, cut)
            if v.get("loot"):
                lo = v.get("loot_floor")
                for p in pts:
                    if lo is not None and p.get("floor") != lo:
                        continue
                    rgb = (0.1, 0.85, 0.15) if p.get("container", "lootFloor") == "lootFloor" else (1.0, 0.45, 0.0)
                    x, y, z = p["model"]
                    markers.append(((x, y + 0.03, z), rgb))
            for p, rgb in markers:
                marker(p, rgb)
            if v.get("human"):
                g["human"](v["human"][0], v["human"][1], v["human"][2] if len(v["human"]) > 2 else 0.0)
        bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.003))
        bpy.context.active_object.data.materials.append(gm)
        if v.get("plan"):
            c = v.get("center", [0.0, 0.0])
            cam.location = Vector(g["to_b"]((c[0], 60.0, c[1])))
            cam.rotation_mode = "XYZ"
            cam.rotation_euler = Euler((0.0, 0.0, math.radians(v.get("rot", 0.0))))
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = v["scale"]
            cam.data.clip_start = 0.1
            cam.data.clip_end = 200
        elif v.get("cam"):
            c = Vector(g["to_b"](v["cam"]))
            t = Vector(g["to_b"](v["look"]))
            cam.location = c
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
            cam.data.type = "PERSP"
            cam.data.lens = v["lens"]
            cam.data.clip_start = 0.05
            cam.data.clip_end = 600
            if v.get("fill", True):
                lamp = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "POINT"))
                lamp.data.energy = v.get("fill_w", 700)
                lamp.location = c + Vector((0, 0, 0.3))
                sc.collection.objects.link(lamp)
        else:
            M = get_bundle(v["key"])[0]
            b = M.bbox()
            size = max(b[1] - b[0], b[5] - b[4], (b[3] - b[2]) * 1.3)
            g["human"](b[0] + 0.2 + (b[1] - b[0]) * 0.1, b[5] + 1.2, 0.0)
            tgt = ((b[0] + b[1]) / 2, min(b[3], 7.0) / 2.2, (b[4] + b[5]) / 2)
            g["look"](cam, g["to_b"](tgt), v.get("view", "3q"), size * 1.35 * v.get("fit", 1.0))
        sc.render.filepath = os.path.join(OUT, out + ".png")
        bpy.ops.render.render(write_still=True)
        for ob in list(bpy.data.objects):
            if ob.type == "LIGHT" and ob.name.startswith("fill"):
                bpy.data.objects.remove(ob, do_unlink=True)
        print("rendered", out)


# ================================================================================================ driver
def compose(name, jobs, title, sub, cols, cw, ch, cap, wrap):
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 30),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 16),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 15)}.items()}
    rows = (len(jobs) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw + (cols + 1) * 8, 88 + rows * (ch + cap + 8) + 8), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((12, 10), title, font=F["h1"], fill=(20, 20, 20))
    d.text((12, 52), sub, font=F["s"], fill=(60, 60, 60))
    for i, (out, caption, v) in enumerate(jobs):
        x = 8 + (i % cols) * (cw + 8)
        y = 88 + (i // cols) * (ch + cap + 8)
        p = os.path.join(OUT, out + ".png")
        if os.path.isfile(p):
            im.paste(Image.open(p).convert("RGB").resize((cw, ch)), (x, y))
        d.rectangle([x, y + ch, x + cw, y + ch + cap], fill=(250, 249, 246))
        yy = y + ch + 3
        for ln in textwrap.wrap(caption, wrap)[:max(1, cap // 17)]:
            d.text((x + 5, yy), ln, font=F["s"], fill=(40, 40, 40))
            yy += 17
    os.makedirs(SHEETS, exist_ok=True)
    dst = os.path.join(SHEETS, "c3_%s.jpg" % name)
    im.save(dst, quality=86)
    print("sheet", dst, im.size)


def run_jobs(alljobs, jobs_n):
    os.makedirs(OUT, exist_ok=True)
    procs = []
    for i in range(jobs_n):
        part = alljobs[i::jobs_n]
        if not part:
            continue
        jf = os.path.join(OUT, "_jobs_%d.json" % i)
        with open(jf, "wb") as f:
            f.write(json.dumps(part).encode("utf-8"))
        lf = open(os.path.join(OUT, "_blender_%d.log" % i), "wb")
        procs.append((subprocess.Popen([BLENDER, "--background", "--factory-startup", "--python",
                                        os.path.abspath(__file__), "--", "--blender", jf], stdout=lf,
                                       stderr=subprocess.STDOUT, cwd=DEV), lf, len(part)))
    for p, lf, n in procs:
        p.wait()
        lf.close()


def main(argv):
    jobs_n = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 6
    if "preview" in argv:
        keys = argv[argv.index("--keys") + 1].split(",")
        jobs = [("pv_" + k, k, {"key": k, "view": "3q", "fit": 1.0, "res": [960, 720]}) for k in keys]
        run_jobs(jobs, min(jobs_n, len(jobs)))
        return 0
    import c3_jobs
    sets = [a for a in argv if a in c3_jobs.JOBS] or list(c3_jobs.JOBS)
    if "--compose" not in argv:
        run_jobs([j for s in sets for j in c3_jobs.JOBS[s]], jobs_n)
    for s in sets:
        t, sub, cols, cw, ch, cap, wrap = c3_jobs.SHEETS[s]
        compose(s, c3_jobs.JOBS[s], t, sub, cols, cw, ch, cap, wrap)
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        spec = json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8"))
        blender_main(spec)
    else:
        sys.exit(main(sys.argv[1:]))
