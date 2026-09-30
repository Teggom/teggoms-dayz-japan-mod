#!/usr/bin/env python3
r"""Contact sheet for jp_f_tansu (effort test, level xhigh).

  python render.py            (Blender in the background renders renders/*.png, then the sheet is composed)
  python render.py --compose  (only recompose)

Renders the MLOD files that build.py wrote (out/*.p3d, read back with tools/common/mlod.py), so what is seen is what
was written: face winding (backface culling ON, so a flipped face shows as a hole), UVs, per-face materials. Library
textures = data/materials/textures/<name>.png (the PNG masters of the .paa files). Standard view transform.
"""
import json
import math
import os
import subprocess
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
RDIR = os.path.join(HERE, "renders")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
REFS = os.path.join(DEV, "data", "research_int", "refs")
SHEET = os.path.join(HERE, "tansu_contact_sheet.png")
RES = (960, 720)
P3D = {"A": os.path.join(HERE, "out", "jp_f_tansu.p3d"), "B": os.path.join(HERE, "out", "jp_f_tansu_ransacked.p3d")}

# (out, caption, spec). Model coordinates: x = the chest's own right, y up, z = front.
JOBS = [
    ("A_front", "A intact, front (ortho): two stacked parts (upper 4 mm smaller), 5 drawers shut 4 mm behind the "
     "frame, 8 iron ring pulls, 3 round lock plates, corner plates at every front corner.",
     {"state": "A", "cam": "ortho", "az": 0, "el": 4, "scale": 1.48, "target": [0, 0.5, 0], "wall": True}),
    ("A_3q", "A intact, 3/4 with a 1.8 m figure: side carrying handles on both parts, the step between the parts, "
     "dusty dark wood (street_dark _w2 stand-in for wood_interior).",
     {"state": "A", "cam": "persp", "az": 38, "el": 16, "dist": 4.6, "lens": 50, "target": [0.55, 0.85, 0.0],
      "wall": True, "human": [1.35, 0.25]}),
    ("A_back", "A intact, back and side (the back sits 2 cm off a wall in a room): plain back boards, handles.",
     {"state": "A", "cam": "persp", "az": 215, "el": 20, "dist": 3.0, "lens": 50, "target": [0, 0.5, 0]}),
    ("A_close", "A close-up: octagonal pull plate with its staple and hanging ring, round lock plate and keyhole, "
     "corner plates wrapping front, side and top, the U handle hanging flat on the side.",
     {"state": "A", "cam": "look", "pos": [0.80, 1.10, 0.66], "at": [0.30, 0.80, 0.18], "lens": 40, "wall": True}),
    ("B_front", "B ransacked, front (ortho): the wide lock drawer is gone (dark cavity) and lies in front; the small "
     "drawer on the right (as seen) and both lower drawers pulled out; the small left one still shut.",
     {"state": "B", "cam": "ortho", "az": 0, "el": 12, "scale": 1.52, "target": [0, 0.52, 0.3], "wall": True}),
    ("B_3q", "B ransacked, 3/4: the dropped drawer lies upright on the floor inside the front zone, yawed 8 deg; the "
     "pulled drawers show their paler unfinished boxes.",
     {"state": "B", "cam": "persp", "az": -32, "el": 24, "dist": 3.3, "lens": 45, "target": [0, 0.45, 0.35],
      "wall": True}),
    ("B_back", "B ransacked, from behind: the pulled drawers and the dropped drawer beyond; the back is unchanged.",
     {"state": "B", "cam": "persp", "az": 205, "el": 24, "dist": 3.3, "lens": 45, "target": [0, 0.45, 0.2]}),
    ("B_close", "B close-up: into the empty slot (dark inside faces stand in for occlusion) and down into the dropped "
     "drawer, where the one ransacked loot point lies (on its bottom board).",
     {"state": "B", "cam": "look", "pos": [-0.55, 1.28, 1.45], "at": [0.05, 0.42, 0.42], "lens": 32, "wall": True}),
    ("lods_A", "A, LODs left to right: Resolution 1 / 2 / 3 (from the MLOD). Res 2 keeps the frame strips, "
     "plates and handles as blocks; Res 3 is two boxes and the plates.",
     {"state": "A", "lods": [1, 2, 3], "cam": "persp", "az": 28, "el": 14, "dist": 5.2, "lens": 50,
      "target": [-1.25, 0.5, 0.0]}),
    ("lods_B", "B, LODs left to right: Resolution 1 / 2 / 3. The empty slot and the gaps above pulled drawers are "
     "dark quads in Res 2 / 3.",
     {"state": "B", "lods": [1, 2, 3], "cam": "persp", "az": -28, "el": 18, "dist": 5.4, "lens": 50,
      "target": [-1.25, 0.45, 0.3]}),
    ("geo_B", "B Geometry (= View and Fire Geometry): the body box, 3 pulled-drawer boxes, the dropped drawer as a "
     "bottom slab + 4 walls; green = loot points and ranges; yellow = front zone (0.90 m).",
     {"state": "B", "geo": True, "cam": "persp", "az": -35, "el": 38, "dist": 3.6, "lens": 40,
      "target": [0, 0.4, 0.45]}),
]


# ================================================================================================ Blender side
def blender_main(jobs):
    import bpy
    from mathutils import Vector
    sys.path.insert(0, os.path.join(DEV, "tools", "common"))
    import mlod as M

    def to_b(p):
        return (p[0], p[2], p[1])

    mats = {}

    def tex_mat(tex, rvmat):
        key = (tex, rvmat)
        if key in mats:
            return mats[key]
        m = bpy.data.materials.new(os.path.basename(tex or rvmat or "none"))
        m.use_nodes = True
        m.use_backface_culling = True
        b = m.node_tree.nodes.get("Principled BSDF")
        iron = "metal" in (tex or "").lower()
        b.inputs["Roughness"].default_value = 0.55 if iron else 0.85
        if iron:
            b.inputs["Metallic"].default_value = 0.35
        png = os.path.join(TEXPNG, os.path.basename(tex).rsplit(".", 1)[0] + ".png") if tex else ""
        if png and os.path.isfile(png):
            t = m.node_tree.nodes.new("ShaderNodeTexImage")
            t.image = bpy.data.images.load(png, check_existing=True)
            m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
        else:
            b.inputs["Base Color"].default_value = (1.0, 0.0, 1.0, 1.0)     # missing texture = magenta
        mats[key] = m
        return m

    def plain(name, rgb, alpha=1.0, cull=False):
        key = ("plain", name)
        if key in mats:
            return mats[key]
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        m.use_backface_culling = cull
        b = m.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = rgb + (1.0,)
        b.inputs["Roughness"].default_value = 0.9
        if alpha < 1.0:
            b.inputs["Alpha"].default_value = alpha
            try:
                m.surface_render_method = "BLENDED"
            except Exception:  # noqa: BLE001
                m.blend_method = "BLEND"
        mats[key] = m
        return m

    lodcache = {}

    def lods_of(state):
        if state not in lodcache:
            lodcache[state] = M.read_mlod(P3D[state])
        return lodcache[state]

    def find(state, res):
        for l in lods_of(state):
            if abs(l.resolution - res) <= abs(res) * 1e-5 + 1e-6:
                return l
        return None

    def lod_mesh(lod, name, dx=0.0, faces=None, material=None):
        verts, polys, uvs, mids, ml, mi = [], [], [], [], [], {}
        for fi, (fv, _, tex, rv) in enumerate(lod.faces):
            if faces is not None and fi not in faces:
                continue
            base = len(verts)
            for (pi, ni, u, v) in fv:
                p = lod.points[pi]
                verts.append(to_b((p[0] + dx, p[1], p[2])))
                uvs.append((u, 1.0 - v))
            polys.append(list(range(base, base + len(fv))))
            key = material or (tex, rv)
            if key not in mi:
                mi[key] = len(ml)
                ml.append(material if material else tex_mat(tex, rv))
            mids.append(mi[key])
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], polys)
        uvl = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uvl.data[i].uv = uvs[loop.vertex_index]
        for m in ml:
            me.materials.append(m)
        for i, k in enumerate(mids):
            me.polygons[i].material_index = k
        me.update()
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    def boxb(name, x0, x1, y0, y1, z0, z1, mat):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=to_b(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)))
        ob = bpy.context.active_object
        ob.name = name
        ob.scale = (x1 - x0, z1 - z0, y1 - y0)
        ob.data.materials.append(mat)
        return ob

    def human(x, z):
        m = plain("human", (0.05, 0.05, 0.06))
        parts = [("uv_sphere", dict(radius=0.11, location=(x, z, 1.69), segments=16, ring_count=8)),
                 ("cylinder", dict(radius=0.17, depth=0.62, location=(x, z, 1.25), vertices=12))]
        for dx in (-0.09, 0.09):
            parts.append(("cylinder", dict(radius=0.075, depth=0.94, location=(x + dx, z, 0.47), vertices=10)))
        for dx in (-0.235, 0.235):
            parts.append(("cylinder", dict(radius=0.05, depth=0.66, location=(x + dx, z, 1.18), vertices=8)))
        for kind, kw in parts:
            getattr(bpy.ops.mesh, "primitive_%s_add" % kind)(**kw)
            bpy.context.active_object.data.materials.append(m)

    sc = bpy.context.scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    try:
        sc.render.engine = "BLENDER_EEVEE"
    except TypeError:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    try:
        sc.eevee.taa_render_samples = 32
    except AttributeError:
        pass
    w = bpy.data.worlds.new("sky")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.80, 0.80, 0.78, 1.0)
    bg.inputs[1].default_value = 0.65
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.0
    sun.data.angle = math.radians(6)
    sun.rotation_mode = "QUATERNION"
    sun.rotation_quaternion = Vector(to_b((-0.45, -0.75, -0.60))).to_track_quat("-Z", "Y")   # from front-right, above
    sc.collection.objects.link(sun)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    os.makedirs(RDIR, exist_ok=True)
    floor = plain("floor", (0.30, 0.25, 0.17))
    wallm = plain("wall", (0.52, 0.46, 0.38))

    for out, cap, v in jobs:
        for ob in list(bpy.data.objects):
            if ob.type == "MESH":
                bpy.data.objects.remove(ob, do_unlink=True)
        st = v["state"]
        if v.get("geo"):
            lod_mesh(find(st, 1.0), "ghost", material=plain("ghost", (0.55, 0.55, 0.55), alpha=0.25))
            g = find(st, M.LOD_GEOMETRY)
            cols = [(0.95, 0.45, 0.10), (0.20, 0.55, 0.95), (0.85, 0.20, 0.55), (0.30, 0.75, 0.35),
                    (0.95, 0.80, 0.15), (0.55, 0.35, 0.90)]
            k = 0
            for name in sorted(g.selections):
                if not name.startswith("Component"):
                    continue
                c = cols[k % len(cols)]
                k += 1
                lod_mesh(g, name, faces=g.selections[name][1], material=plain("geo%d" % k, c, alpha=0.45))
            # loot points as delivered: the sidecar's loot_surfaces (no Memory LOD, BUILD_LIST Q5 item 2)
            side = json.load(open(os.path.join(DEV, "src", "JP", "effort_test", "xhigh", "jp_f_tansu.json"),
                                  encoding="utf-8"))
            var = "" if st == "A" else "_ransacked"
            gm = plain("loot", (0.10, 0.85, 0.20))
            for lp in [p for s_ in side["loot_surfaces"] if var in s_["states"] for p in s_["points"]]:
                p = to_b(lp["model"])
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=p, segments=12, ring_count=6)
                bpy.context.active_object.data.materials.append(gm)
                bpy.ops.mesh.primitive_torus_add(major_radius=lp["range"], minor_radius=0.004,
                                                 location=(p[0], p[1], p[2] + 0.004), major_segments=48,
                                                 minor_segments=6)
                bpy.context.active_object.data.materials.append(gm)
            fz = json.load(open(os.path.join(DEV, "src", "JP", "effort_test", "xhigh", "jp_f_tansu.json"),
                                encoding="utf-8"))["front_zone"]
            ym = plain("zone", (0.95, 0.85, 0.10))
            (x0, x1), (z0, z1) = fz["x"], fz["z"]
            for a, b, c, d in ((x0, x1, z0, z0 + 0.01), (x0, x1, z1 - 0.01, z1), (x0, x0 + 0.01, z0, z1),
                               (x1 - 0.01, x1, z0, z1)):
                boxb("zone", a, b, 0.0, 0.006, c, d, ym)
        else:
            for i, res in enumerate(v.get("lods", [1])):
                dx = -1.25 * i
                lod_mesh(find(st, float(res)), "res%d" % res, dx=dx)
        if v.get("human"):
            human(v["human"][0], v["human"][1])
        bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.0015))
        bpy.context.active_object.data.materials.append(floor)
        if v.get("wall"):
            boxb("wall", -6, 6, 0.0, 2.6, -0.30, -0.245, wallm)
        # camera
        if v["cam"] == "look":
            c = Vector(to_b(v["pos"]))
            t = Vector(to_b(v["at"]))
            cam.location = c
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
            cam.data.type = "PERSP"
            cam.data.lens = v["lens"]
        else:
            a, e = math.radians(v["az"]), math.radians(v["el"])
            d = Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
            tgt = Vector(to_b(v["target"]))
            if v["cam"] == "ortho":
                cam.location = tgt + d * 10.0
                cam.data.type = "ORTHO"
                cam.data.ortho_scale = v["scale"]
            else:
                cam.location = tgt + d * v["dist"]
                cam.data.type = "PERSP"
                cam.data.lens = v["lens"]
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (-d).to_track_quat("-Z", "Y")
        cam.data.clip_start = 0.02
        cam.data.clip_end = 100
        sc.render.filepath = os.path.join(RDIR, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)


# ================================================================================================ sheet
def compose():
    from PIL import Image, ImageDraw, ImageFont
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 34),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 17),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 17)}.items()}
    cw, ch, cap, cols = 640, 480, 92, 4
    panels = [(o, c) for o, c, _ in JOBS] + [("refs", None)]
    rows = (len(panels) + cols - 1) // cols
    Wd = cols * cw + (cols + 1) * 10
    Hd = 118 + rows * (ch + cap + 10) + 10
    im = Image.new("RGB", (Wd, Hd), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((14, 12), "jp_f_tansu - clothing chest of drawers (isho-dansu), effort test xhigh: A intact / B ransacked",
           font=F["h1"], fill=(20, 20, 20))
    line = ""
    br = os.path.join(HERE, "out", "build_result.json")
    ck = os.path.join(HERE, "checks.json")
    if os.path.isfile(br):
        inf = json.load(open(br, encoding="utf-8"))["infos"]
        line = "Faces (MLOD) A: %s | B: %s. " % (
            " / ".join("%s %d" % (k.replace("Resolution ", "R").replace(" Geometry", "G").replace("Geometry", "Geo"), n)
                       for k, n in inf["A"]["faces"].items() if n),
            " / ".join("%s %d" % (k.replace("Resolution ", "R").replace(" Geometry", "G").replace("Geometry", "Geo"), n)
                       for k, n in inf["B"]["faces"].items() if n))
    if os.path.isfile(ck):
        c = json.load(open(ck, encoding="utf-8"))
        line += "Checks %d/%d pass." % (sum(1 for x in c["checks"] if x["ok"]), len(c["checks"]))
    d.text((14, 58), line, font=F["s"], fill=(60, 60, 60))
    d.text((14, 82), "Rendered from the written MLOD files (backface culling on). Wood: jp_m_wood_street_dark_w2 "
           "(stand-in for the unbuilt jp_m_wood_interior), drawer boxes wood_weathered_w1, inside wood_sooted_w0; "
           "iron: jp_m_metal_iron_w1. Wall 2 cm behind, floor plain.", font=F["s"], fill=(60, 60, 60))
    for i, (out, caption) in enumerate(panels):
        x = 10 + (i % cols) * (cw + 10)
        y = 118 + (i // cols) * (ch + cap + 10)
        if out == "refs":
            refs = [("i07_edo_nagaya_room.jpg", (520, 330, 890, 850)),
                    ("i01_kasuya_irori.jpg", (1000, 1180, 1850, 2020))]
            wv = cw // 2
            for k, (fn, box) in enumerate(refs):
                p = os.path.join(REFS, fn)
                if os.path.isfile(p):
                    r = Image.open(p).convert("RGB").crop(box)
                    r.thumbnail((wv - 4, ch))
                    im.paste(r, (x + k * wv + (wv - r.size[0]) // 2, y + (ch - r.size[1]) // 2))
            caption = ("References (C9): left i07 Fukagawa Edo Museum tenement (c.1840 reconstruction, DryPot, CC BY "
                       "2.5): two-part tansu, ring pulls, round plates, corner irons. Right i01 Kasuya house (CC0, "
                       "Asanagi): stacked chests, side handle, dark worn wood.")
        else:
            p = os.path.join(RDIR, out + ".png")
            if os.path.isfile(p):
                im.paste(Image.open(p).convert("RGB").resize((cw, ch), Image.LANCZOS), (x, y))
        d.rectangle([x, y + ch, x + cw, y + ch + cap], fill=(250, 249, 246))
        d.text((x + 6, y + ch + 4), out, font=F["b"], fill=(20, 20, 20))
        yy = y + ch + 25
        for ln in textwrap.wrap(caption, 80)[:4]:
            d.text((x + 6, yy), ln, font=F["s"], fill=(50, 50, 50))
            yy += 16
    im.save(SHEET)
    print("sheet", SHEET, im.size)


def main(argv):
    if "--compose" not in argv:
        os.makedirs(RDIR, exist_ok=True)
        only = [a for a in argv if not a.startswith("--")]
        jobs = [j for j in JOBS if not only or j[0] in only]
        jf = os.path.join(RDIR, "_jobs.json")
        with open(jf, "wb") as f:
            f.write(json.dumps(jobs).encode("utf-8"))
        r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__), "--",
                            "--blender", jf], capture_output=True, text=True, errors="replace")
        done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
        print("%d/%d rendered" % (len(done), len(jobs)))
        if len(done) < len(jobs):
            print((r.stdout + r.stderr)[-5000:])
    compose()


if __name__ == "__main__":
    if "--blender" in sys.argv:
        blender_main(json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8")))
    else:
        main(sys.argv[1:])
