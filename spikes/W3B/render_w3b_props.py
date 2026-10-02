#!/usr/bin/env python3
r"""render_w3b_props.py - W3B specialty prop renders (copy of spikes/W2F/render_w2f_props.py) (copy of spikes/S1/render_s1.py, retargeted to spikes/W2F/out);
S1 original header:: a copy of spikes/L1/render_l1.py (L1's file is not changed)
pointed at spikes/S1/out, with a backdrop wall for wall / post props and a beam over hanging props,
FROM THE WRITTEN MLOD MASTERS (out/<cat>/*.p3d).

  python render.py [prop ...]          renders every model of each prop in one row (3/4 view) + a LOD strip,
                                       -> renders/<prop>_row.png, renders/<prop>_lod.png
  python render.py --sheets            composes the contact sheets (renders beside the build-list references)
                                       -> research/interior/contact_sheets/l1_<group>.jpg

Blender side: the parts kit's scene helpers (parts/kit/render_parts.py: sky + sun, Standard view transform), meshes
from each LOD's faces with the library _co / _ca PNGs (data/materials/textures) by texture path.
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
REN = os.path.join(HERE, "renders")
JOBS = os.path.join(HERE, "_build", "render_jobs.json")
SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
REFDIRS = [os.path.join(DEV, "data", "research_int", "refs"), os.path.join(DEV, "data", "research_ext", "refs"),
           os.path.join(DEV, "data", "playbook", "refs")]
GROUPS = [   # (key, title, category)
    ("trade", "W3B trade props", "tradefit"),
]


# ================================================================================================ Blender side
def blender_main():
    import bpy
    from mathutils import Vector
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    sys.path.insert(0, KIT)
    exec(compile(src, "render_parts.py", "exec"), g)
    from jpparts import mlod
    jobs = json.load(open(JOBS, encoding="utf-8"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"]((1600, 900))
    ground = g["plain"]("ground", (0.30, 0.29, 0.26))
    mats = {}

    def mat_for(tex):
        if tex in mats:
            return mats[tex]
        m = bpy.data.materials.new(os.path.basename(tex))
        m.use_nodes = True
        nt = m.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        iron = "metal" in tex
        glossy = "ceramic" in tex or "lacquer" in tex
        bsdf.inputs["Roughness"].default_value = 0.5 if iron else (0.35 if glossy else 0.88)
        bsdf.inputs["Metallic"].default_value = 0.45 if iron else 0.0
        png = os.path.join(TEXPNG, os.path.basename(tex).replace(".paa", ".png"))
        if os.path.isfile(png):
            t = nt.nodes.new("ShaderNodeTexImage")
            t.image = bpy.data.images.load(png, check_existing=True)
            nt.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
            if tex.endswith("_ca.paa"):
                # alpha-tested decal: mix a transparent shader by a hard threshold of the texture alpha
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
                bsdf.inputs["Specular IOR Level"].default_value = 0.1
                try:
                    m.surface_render_method = "DITHERED"
                except Exception:
                    m.blend_method = "CLIP"
        else:
            bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
        mats[tex] = m
        return m

    def lod_mesh(lod, name, off=(0.0, 0.0), solid_mat=None, lift=0.0):
        verts, polys, uvs, mids, ml, lnor = [], [], [], [], [], []
        for fi, (fv, fl, tex, mat) in enumerate(lod.faces):
            pts = [lod.points[v[0]] for v in fv]
            bp = [(p[0] + off[0], p[2] + off[1], p[1] + lift) for p in pts]
            inward = lod.normals[fv[0][1]]
            want = (-inward[0], -inward[2], -inward[1])
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
            for i in order:
                nn = lod.normals[fv[i][1]] if lod.normals else (0.0, 1.0, 0.0)
                lnor.append((-nn[0], -nn[2], -nn[1]))
            key = solid_mat or tex
            if key not in ml:
                ml.append(key)
            mids.append(ml.index(key))
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], polys)
        uv = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uv.data[i].uv = uvs[loop.vertex_index]
        for k in ml:
            me.materials.append(k if not isinstance(k, str) else mat_for(k))
        for i, mi in enumerate(mids):
            me.polygons[i].material_index = mi
        me.update()
        if lnor and solid_mat is None:
            try:
                me.shade_smooth()
            except Exception:
                for poly in me.polygons:
                    poly.use_smooth = True
            try:
                me.normals_split_custom_set([lnor[l.vertex_index] for l in me.loops])
            except Exception as e:
                print("custom normals failed", e)
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    red = bpy.data.materials.new("geo")
    red.use_nodes = True
    rb = red.node_tree.nodes.get("Principled BSDF")
    rb.inputs["Base Color"].default_value = (0.9, 0.05, 0.03, 1)
    rb.inputs["Alpha"].default_value = 0.30
    try:
        red.surface_render_method = "BLENDED"
    except Exception:
        red.blend_method = "BLEND"
    os.makedirs(REN, exist_ok=True)

    def shoot(out, lo, hi, view=(0.45, 1.0, 0.6), lens=50, tight=1.0):
        """view = (x, front, up) in MODEL terms; the camera distance is solved so every bbox corner fits."""
        c = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
        v = Vector((view[0], view[1], view[2])).normalized()
        q = (-v).to_track_quat("-Z", "Y")
        rx = q @ Vector((1, 0, 0))
        uy = q @ Vector((0, 1, 0))
        th = 18.0 / lens * 0.92                      # tan(half fov): 36 mm sensor, 8 % margin
        tv = th * 9 / 16
        corners = [Vector((a, b, e)) for a in (lo[0], hi[0]) for b in (lo[1], hi[1]) for e in (lo[2], hi[2])]
        d = 0.5
        for _ in range(60):
            ok = True
            for k in corners:
                w = k - (c + v * d)
                depth = w.dot(-v)
                if depth <= 0.05 or abs(w.dot(rx)) / depth > th or abs(w.dot(uy)) / depth > tv:
                    ok = False
                    break
            if ok:
                break
            d *= 1.12
        cam.location = c + v * d * tight
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = q
        cam.data.type = "PERSP"
        cam.data.lens = lens
        cam.data.clip_start = 0.02
        cam.data.clip_end = 200
        bpy.context.scene.render.filepath = os.path.join(REN, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)

    for job in jobs:
        g["clear_objects"]()
        lo, hi = [1e9] * 3, [-1e9] * 3
        for item in job["items"]:
            lods = mlod.read_mlod(item["p3d"])
            want = item.get("lod", 1.0)
            lod = next(l for l in lods if abs(l.resolution - want) < 1e-3)
            ox, oz = item["off"]
            lift = item.get("lift", 0.0)
            lod_mesh(lod, "m", (ox, oz), lift=lift)
            if item.get("geo"):
                ge = [l for l in lods if abs(l.resolution - 1e13) < 1e7]
                if ge:
                    ob = lod_mesh(ge[0], "geo", (ox, oz), solid_mat=red, lift=lift)
            if item.get("beam"):
                xs = [p[0] for p in lod.points]
                bo = bpy.data.objects.new("beam", bpy.data.meshes.new("beam"))
                bpy.context.scene.collection.objects.link(bo)
                x0b, x1b = min(xs) + ox - 0.10, max(xs) + ox + 0.10
                vb = [(x, y, z) for x in (x0b, x1b) for y in (oz - 0.07, oz + 0.07) for z in (lift, lift + 0.14)]
                bo.data.from_pydata(vb, [], [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4],
                                             [1, 5, 7, 3]])
                bo.data.materials.append(g["plain"]("beamc", (0.20, 0.15, 0.11)))
            if item.get("wall"):
                xs = [p[0] for p in lod.points]
                wm = bpy.data.meshes.new("wall")
                wm.from_pydata([(min(xs) + ox - 0.05, oz - 0.002, 0.0), (max(xs) + ox + 0.05, oz - 0.002, 0.0),
                                (max(xs) + ox + 0.05, oz - 0.002, 2.1), (min(xs) + ox - 0.05, oz - 0.002, 2.1)],
                               [], [[0, 1, 2, 3]])
                wo = bpy.data.objects.new("wall", wm)
                wm.materials.append(g["plain"]("wallc", (0.42, 0.38, 0.32)))
                bpy.context.scene.collection.objects.link(wo)
            for p in lod.points:
                q = (p[0] + ox, p[2] + oz, p[1] + lift)
                lo = [min(a, b) for a, b in zip(lo, q)]
                hi = [max(a, b) for a, b in zip(hi, q)]
        bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, min(lo[2], 0.0) - 0.001))
        bpy.context.active_object.data.materials.append(ground)
        hi[2] = max(hi[2], lo[2] + 0.3)
        shoot(job["out"], lo, hi, tuple(job.get("view", (0.45, 1.0, 0.6))), job.get("lens", 50), job.get("tight", 1.0))


# ================================================================================================ jobs
def load_props(ids=None):
    sys.path.insert(0, HERE)
    import build_w3b as build_s1
    reg = build_s1.mine(build_s1.B.registry())
    if ids:
        want = {i if i.startswith("jp_f_") else "jp_f_" + i for i in ids}
        reg = [p for p in reg if p["id"] in want]
    return reg


def row_items(prop, gap=0.25, lod=1.0, geo=False, only=None, per_row=6, wall=False, anchors=None):
    """Lay the prop's models out left to right as seen from the front (+x is on the viewer's left, so towards -x),
    wrapping into rows of `per_row` that step back (-z)."""
    sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
    from jpparts import mlod
    models = prop["models"] if only is None else [m for m in prop["models"] if m["p3d"] in only]
    boxes = []
    for m in models:
        p = os.path.join(HERE, "out", prop["cat"], m["p3d"] + ".p3d")
        r1 = next(l for l in mlod.read_mlod(p) if abs(l.resolution - 1.0) < 1e-3)
        xs = [q[0] for q in r1.points]
        zs = [q[2] for q in r1.points]
        boxes.append((p, min(xs), max(xs), min(zs), max(zs)))
    items = []
    zc = 0.0
    for r0 in range(0, len(boxes), per_row):
        chunk = boxes[r0:r0 + per_row]
        x = 0.0
        row = []
        for p, x0, x1, z0, z1 in chunk:
            an = (anchors or {}).get(p, "floor")
            row.append({"p3d": p, "off": [x - x1, zc - (z1 + z0) / 2 if an != "wall" else zc], "lod": lod, "geo": geo,
                        "wall": an == "wall", "beam": an == "hang", "lift": 2.2 if an == "hang" else 0.0})
            x -= (x1 - x0) + gap
        sh = (x + gap) / 2
        for it in row:
            it["off"][0] -= sh
        items += row
        zc -= max(z1 - z0 for _, _, _, z0, z1 in chunk) + 0.6
    return items


_ANCH = {}


def anchors_of(prop):
    """{master path: anchor} of every model of the prop (from the sidecar written by build_l1)."""
    if prop["id"] not in _ANCH:
        sc = json.load(open(os.path.join(DEV, "src", "JP", "furniture", prop["cat"], prop["id"] + ".prop.json"),
                            encoding="utf-8"))
        _ANCH[prop["id"]] = {os.path.join(HERE, "out", prop["cat"], os.path.basename(m["p3d"])): m["anchor"]
                             for m in sc["models"]}
    return _ANCH[prop["id"]]


def make_jobs(props):
    jobs = []
    for prop in props:
        items = row_items(prop, per_row=prop.get("per_row", 6), anchors=anchors_of(prop))
        multi = len(prop["models"]) > prop.get("per_row", 6)
        jobs.append({"out": prop["id"] + "_row", "items": items,
                     "view": prop.get("view", (0.35, 1.0, 1.0) if multi else (0.45, 1.0, 0.6)),
                     "lens": 50})
        first = prop["models"][0]
        ab = [m for m in prop["models"] if m["state"] != "intact"]
        lodrow = []
        sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
        from jpparts import mlod
        p = os.path.join(HERE, "out", prop["cat"], first["p3d"] + ".p3d")
        lods = mlod.read_mlod(p)
        res = [l.resolution for l in lods if l.resolution < 10]
        r1 = next(l for l in lods if abs(l.resolution - 1.0) < 1e-3)
        w = max(q[0] for q in r1.points) - min(q[0] for q in r1.points)
        x = 0.0
        mx = max(q[0] for q in r1.points)
        for rr in res:
            an = anchors_of(prop).get(p, "floor")
            lodrow.append({"p3d": p, "off": [x - mx, 0.0], "lod": rr, "geo": False, "wall": an == "wall",
                           "beam": an == "hang", "lift": 2.2 if an == "hang" else 0.0})
            x -= w + 0.25
        if ab:
            pa = os.path.join(HERE, "out", prop["cat"], ab[0]["p3d"] + ".p3d")
            la = mlod.read_mlod(pa)
            if any(abs(l.resolution - 1e13) < 1e7 for l in la):
                ra = next(l for l in la if abs(l.resolution - 1.0) < 1e-3)
                lodrow.append({"p3d": pa, "off": [x - max(q[0] for q in ra.points), 0.0], "lod": 1.0, "geo": True,
                               "wall": anchors_of(prop).get(pa) == "wall"})
                x -= max(q[0] for q in ra.points) - min(q[0] for q in ra.points) + 0.25
        sh = (x + 0.25) / 2
        for it in lodrow:
            it["off"][0] -= sh
        jobs.append({"out": prop["id"] + "_lod", "items": lodrow, "view": prop.get("view", (0.45, 1.0, 0.6)), "lens": 50})
    return jobs


# ================================================================================================ sheets
def ref_path(rid):
    for d in REFDIRS:
        for ext in (".jpg", ".png", ".jpeg"):
            p = os.path.join(d, rid + ext)
            if os.path.isfile(p):
                return p
    return None


def compose(props_all):
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, HERE)
    sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
    import build
    chk = json.load(open(os.path.join(HERE, "checks.json"), encoding="utf-8"))["models"]
    groups = []
    for key, title, cat in GROUPS:
        ids = [p["id"] for p in props_all if p["cat"] == cat]
        for k in range(0, len(ids), 7):
            groups.append((key + ("" if k == 0 else "_%d" % (k // 7 + 1)), title, ids[k:k + 7]))
    os.makedirs(SHEETS, exist_ok=True)
    try:
        f = ImageFont.truetype("arial.ttf", 17)
        fb = ImageFont.truetype("arialbd.ttf", 22)
        ft = ImageFont.truetype("arialbd.ttf", 28)
    except OSError:
        f = fb = ft = ImageFont.load_default()
    byid = {p["id"]: p for p in props_all}
    outs = []
    RW, RH = 960, 540          # row render
    LW, LH = 640, 360          # lod render
    FW = 300                   # ref column width
    for key, title, ids in groups:
        ids = [i for i in ids if i in byid]
        if not ids:
            continue
        rowh = RH + 70
        W = 2 * FW + RW + LW + 40
        sheet = Image.new("RGB", (W, 60 + rowh * len(ids)), (24, 24, 26))
        d = ImageDraw.Draw(sheet)
        d.text((14, 14), "S1 shop sets: %s. Left: local references. Middle: every model (intact first, "
               "as left after), Resolution 1 from the written MLOD, on a wall or under a beam where it mounts. Right: "
               "LOD 1-2(-3) + collision (red)." % title, fill=(235, 235, 235), font=fb)
        for r, pid in enumerate(ids):
            prop = byid[pid]
            y = 60 + r * rowh
            refs = [{"id": r} for r in prop.get("refs", [])] + (build.BL.get(pid, {}).get("refs") or [])
            imgs = []
            for x in refs:
                rp = ref_path(x["id"])
                if not rp:
                    continue
                try:
                    Image.open(rp).verify()      # some saved refs are HTML error pages (i31, i35)
                except Exception:
                    continue
                imgs.append((x["id"], rp))
            imgs = imgs[:2]
            for k in range(2):
                x0 = 10 + k * FW
                if k < len(imgs):
                    im = Image.open(imgs[k][1]).convert("RGB")
                    im.thumbnail((FW - 12, RH))
                    sheet.paste(im, (x0, y))
                    d.text((x0, y + im.size[1] + 4), imgs[k][0][:34], fill=(170, 170, 170), font=f)
                else:
                    d.text((x0, y + 10), "(no picture ref:\n text source only)" if k == 0 else "", fill=(120, 120, 120),
                           font=f)
            p = os.path.join(REN, pid + "_row.png")
            if os.path.isfile(p):
                sheet.paste(Image.open(p).convert("RGB").resize((RW, RH), Image.LANCZOS), (2 * FW + 10, y))
            p = os.path.join(REN, pid + "_lod.png")
            if os.path.isfile(p):
                sheet.paste(Image.open(p).convert("RGB").resize((LW, LH), Image.LANCZOS), (2 * FW + RW + 20, y))
            ms = prop["models"]
            ok = sum(1 for m in ms if chk.get(m["p3d"], {}).get("pass"))
            r1 = [chk.get(m["p3d"], {}).get("faces", {}).get("Resolution 1", 0) for m in ms]
            name = ("#%s " % prop.get("ll", "") + (prop["models"][0]["display"] or ""))[:70]
            d.text((2 * FW + RW + 20, y + LH + 8), "%s  (%s)" % (pid, prop["cat"]), fill=(240, 240, 240), font=fb)
            d.text((2 * FW + RW + 20, y + LH + 38), name, fill=(200, 200, 200), font=f)
            d.text((2 * FW + RW + 20, y + LH + 62), "%d models, checks %d/%d pass; Res 1 faces %d-%d" % (
                len(ms), ok, len(ms), min(r1), max(r1)), fill=(160, 220, 160) if ok == len(ms) else (240, 120, 100),
                font=f)
            lab = " | ".join(m["p3d"].replace(pid, "").lstrip("_") or "base" for m in ms)
            d.text((2 * FW + RW + 20, y + LH + 86), lab[:78], fill=(170, 170, 170), font=f)
            if len(lab) > 78:
                d.text((2 * FW + RW + 20, y + LH + 108), lab[78:156], fill=(170, 170, 170), font=f)
        out = os.path.join(SHEETS, "w3b_props_%s.jpg" % key)
        sheet.save(out, quality=88)
        outs.append(out)
        print("sheet", out, sheet.size)
    return outs


if __name__ == "__main__":
    if "bpy" in sys.modules or any(a.lower().endswith("blender.exe") for a in sys.argv[:1]):
        blender_main()
    elif "--sheets" in sys.argv:
        compose(load_props())
    else:
        props = load_props([a for a in sys.argv[1:] if not a.startswith("--")])
        os.makedirs(os.path.dirname(JOBS), exist_ok=True)
        with open(JOBS, "wb") as fh:
            fh.write(json.dumps(make_jobs(props), indent=1).encode("utf-8"))
        r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__)],
                           capture_output=True, text=True, errors="replace")
        with open(os.path.join(HERE, "render.log"), "wb") as fh:
            fh.write((r.stdout + "\n" + r.stderr).replace("\r\n", "\n").encode("utf-8"))
        print("blender exit", r.returncode, "; rendered:", sum(1 for l in r.stdout.splitlines() if l.startswith("rendered")))
