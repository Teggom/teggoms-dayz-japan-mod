#!/usr/bin/env python3
r"""Contact sheet for the effort-test tansu (both states), rendered FROM THE WRITTEN MLOD FILES (out/*.p3d).

  python render.py            (Blender in the background, then composes tansu_sheet.png)
  python render.py --compose  (recompose only)

Blender side: the parts kit's scene helpers (parts/kit/render_parts.py: sky + sun, Standard view transform, 1.8 m
figure), meshes built from each LOD's faces with the library _co PNGs (data/materials/textures) by texture path.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(HERE, "renders")
RES = (800, 600)
A = os.path.join(HERE, "out", "jp_efftest_high_tansu.p3d")
B = os.path.join(HERE, "out", "jp_efftest_high_tansu_ransacked.p3d")

# (out, caption, spec). cam/look in MODEL metres (x right, y up, z = drawer front)
JOBS = [
    ("a_front", "Intact, front (ortho): 5 drawers, ring pulls on round plates, lock plate, corner fittings",
     {"p3d": A, "cam": [0, 0.5, 6], "look": [0, 0.5, 0], "ortho": 1.5}),
    ("a_34", "Intact, 3/4 with a 1.8 m figure: side carrying handles, dusty top (_w2)",
     {"p3d": A, "cam": [2.6, 1.9, 3.4], "look": [0.35, 0.8, 0], "lens": 40, "human": [1.05, -0.1]}),
    ("a_back", "Intact, back 3/4: plain back board, handles, stacked boxes",
     {"p3d": A, "cam": [-2.0, 1.6, -2.6], "look": [0, 0.5, 0], "lens": 45}),
    ("a_close", "Intact, close-up: corner fitting, side handle, ring pull, lock plate",
     {"p3d": A, "cam": [0.95, 1.12, 0.75], "look": [0.28, 0.78, 0.2], "lens": 38}),
    ("b_front", "Ransacked, front: drawers pulled, lower-top slot empty, that drawer on the floor",
     {"p3d": B, "cam": [0, 0.5, 6], "look": [0, 0.5, 0.3], "ortho": 1.55}),
    ("b_34", "Ransacked, 3/4 with figure: dropped drawer inside the 0.60 m front zone",
     {"p3d": B, "cam": [2.4, 1.9, 3.3], "look": [0.1, 0.5, 0.35], "lens": 40, "human": [1.15, -0.2]}),
    ("b_back", "Ransacked, back 3/4 (pulled drawers stick out past the front)",
     {"p3d": B, "cam": [-2.2, 1.5, -2.4], "look": [0, 0.5, 0.2], "lens": 45}),
    ("b_close", "Ransacked, close-up: empty slot, open drawers (insides, dust on the drawer floors)",
     {"p3d": B, "cam": [0.75, 0.75, 1.45], "look": [0.0, 0.33, 0.15], "lens": 28}),
    ("a_lod2", "Resolution 2, intact (234 faces): pulls and fittings as plates",
     {"p3d": A, "cam": [2.6, 1.9, 3.4], "look": [0.2, 0.55, 0], "lens": 45, "lod": 2.0}),
    ("a_lod3", "Resolution 3, intact (42 faces): two boxes + proud drawer fronts",
     {"p3d": A, "cam": [2.6, 1.9, 3.4], "look": [0.2, 0.55, 0], "lens": 45, "lod": 3.0}),
    ("b_lod2", "Resolution 2, ransacked (330 faces)",
     {"p3d": B, "cam": [2.4, 1.9, 3.3], "look": [0.1, 0.5, 0.35], "lens": 42, "lod": 2.0}),
    ("b_geo", "Ransacked: Geometry / View / Fire boxes (red) over Resolution 1",
     {"p3d": B, "cam": [2.4, 1.9, 3.3], "look": [0.1, 0.5, 0.35], "lens": 42, "geo": True}),
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
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"](RES)
    ground = g["plain"]("ground", (0.36, 0.37, 0.33))
    mats = {}

    def mat_for(tex):
        if tex in mats:
            return mats[tex]
        m = bpy.data.materials.new(os.path.basename(tex))
        m.use_nodes = True
        nt = m.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        iron = "metal" in tex
        bsdf.inputs["Roughness"].default_value = 0.55 if iron else 0.85
        bsdf.inputs["Metallic"].default_value = 0.5 if iron else 0.0
        png = os.path.join(TEXPNG, os.path.basename(tex).replace(".paa", ".png"))
        if os.path.isfile(png):
            t = nt.nodes.new("ShaderNodeTexImage")
            t.image = bpy.data.images.load(png, check_existing=True)
            nt.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
        else:
            bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
        mats[tex] = m
        return m

    def lod_mesh(lod, name, solid_mat=None):
        verts, polys, uvs, mids, ml = [], [], [], [], []
        for fi, (fv, fl, tex, mat) in enumerate(lod.faces):
            pts = [lod.points[v[0]] for v in fv]
            bp = [(p[0], p[2], p[1]) for p in pts]
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
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    red = bpy.data.materials.new("geo")
    red.use_nodes = True
    rb = red.node_tree.nodes.get("Principled BSDF")
    rb.inputs["Base Color"].default_value = (0.9, 0.05, 0.03, 1)
    rb.inputs["Alpha"].default_value = 0.35
    try:
        red.surface_render_method = "BLENDED"
    except Exception:
        red.blend_method = "BLEND"
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    for out, cap, v in JOBS:
        g["clear_objects"]()
        if v["p3d"] not in cache:
            cache[v["p3d"]] = mlod.read_mlod(v["p3d"])
        lods = cache[v["p3d"]]
        lod = next(l for l in lods if abs(l.resolution - v.get("lod", 1.0)) < 1e-3)
        lod_mesh(lod, "vis")
        if v.get("geo"):
            geo = next(l for l in lods if abs(l.resolution - 1e13) < 1e7)
            ob = lod_mesh(geo, "geo", solid_mat=red)
            ob.scale = (1.004, 1.004, 1.004)
        if v.get("human"):
            g["human"](v["human"][0], v["human"][1], 0.0)
        bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.001))
        bpy.context.active_object.data.materials.append(ground)
        c = Vector((v["cam"][0], v["cam"][2], v["cam"][1]))
        t = Vector((v["look"][0], v["look"][2], v["look"][1]))
        cam.location = c
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
        if v.get("ortho"):
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = v["ortho"]
        else:
            cam.data.type = "PERSP"
            cam.data.lens = v["lens"]
        cam.data.clip_start = 0.02
        cam.data.clip_end = 100
        bpy.context.scene.render.filepath = os.path.join(OUT, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)


# ================================================================================================ compose
def compose():
    from PIL import Image, ImageDraw, ImageFont
    tw, th = 640, 480
    cap_h = 44
    cols = 4
    rows = (len(JOBS) + cols - 1) // cols
    title_h = 40
    sheet = Image.new("RGB", (cols * tw, title_h + rows * (th + cap_h)), (24, 24, 26))
    d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("arial.ttf", 15)
        ft = ImageFont.truetype("arialbd.ttf", 20)
    except OSError:
        f = ft = ImageFont.load_default()
    d.text((10, 9), "jp_f_tansu effort test (high): JP_EffTest_high_Tansu / _Ransacked, rendered from the written "
           "MLOD. Wood jp_m_wood_street_dark _w1 (+_w2 dust on up faces), iron jp_m_metal_iron _w1", fill=(235, 235, 235),
           font=ft)
    for k, (out, cap, v) in enumerate(JOBS):
        im = Image.open(os.path.join(OUT, out + ".png")).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = (k % cols) * tw, title_h + (k // cols) * (th + cap_h)
        sheet.paste(im, (x, y))
        words, lines, cur = cap.split(), [], ""
        for w_ in words:
            if d.textlength(cur + " " + w_, font=f) > tw - 12:
                lines.append(cur)
                cur = w_
            else:
                cur = (cur + " " + w_).strip()
        lines.append(cur)
        for i, ln in enumerate(lines[:2]):
            d.text((x + 6, y + th + 4 + i * 19), ln, fill=(220, 220, 220), font=f)
    p = os.path.join(HERE, "tansu_sheet.png")
    sheet.save(p)
    print("sheet", p, sheet.size)


if __name__ == "__main__":
    if "bpy" in sys.modules or any(a.endswith("blender.exe") for a in sys.argv[:1]):
        blender_main()
    elif "--compose" in sys.argv:
        compose()
    else:
        r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__)],
                           capture_output=True, text=True, errors="replace")
        with open(os.path.join(HERE, "render.log"), "wb") as fh:
            fh.write((r.stdout + "\n" + r.stderr).replace("\r\n", "\n").encode("utf-8"))
        print("blender exit", r.returncode, "; rendered:", sum(1 for l in r.stdout.splitlines() if l.startswith("rendered")))
        compose()
