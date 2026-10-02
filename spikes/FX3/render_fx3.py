#!/usr/bin/env python3
r"""FX3: ONE before / after sheet of the sample set (spikes/FX3/out/{before,after}/*.p3d) -> spikes/FX3/fx3_samples.jpg.

  python spikes/FX3/render_fx3.py

Blender --background (no GUI), the FP2 renderer (game-like: back faces culled, alpha-tested _ca). 'after' takes
the draft textures (spikes/FX3/drafts/textures) before the library PNGs and emulates the Super shader's macro
stage: colour = lerp(CO, MC.rgb, MC.alpha) with MC sampled at uv * (aside, up) of the draft rvmat.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
DRAFT = os.path.join(HERE, "drafts", "textures")
INSITU = "--insitu" in sys.argv or os.environ.get("FX3_INSITU") == "1"
if INSITU:                       # phase 2: the shipped masters with the library (atlas + macro) PNGs
    DRAFT = TEXPNG
SHIPPED = {"torii": "spikes/B3b/out/shrine/jp_s_torii_wood_shinmei.p3d", "bench": "spikes/B3b/out/street/jp_s_bench_1ken.p3d",
           "woodpile": "spikes/B3b/out/yard/jp_s_firewood_stack_wall_1ken_h120.p3d",
           "chest": "spikes/B3a/out/storage/jp_f_nagamochi.p3d", "tansu": "spikes/B3a/out/storage/jp_f_tansu.p3d",
           "teahouse": "buildings/teahouse/out/jp_teahouse_shop_thatch.p3d"}
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
REN = os.path.join(HERE, "renders")
JOBS = os.path.join(HERE, "_build", "render_jobs.json")
WOOD = ["wood_weathered", "wood_street_dark", "wood_kuro", "wood_sooted", "wood_bengara", "wood_new", "wood_silver",
        "wood_interior", "ceil_boards", "floor_boards_int", "floor_boards_rough"]
INTERIOR = {"wood_interior", "ceil_boards", "floor_boards_int", "floor_boards_rough"}
DARK = {"wood_kuro", "wood_sooted", "wood_street_dark", "wood_bengara"}
MACRO = {"wood": (0.2721, 0.1156), "thatch": (0.2151, 0.2597)}
# (shot, [(sample, (dx, dy))], view (blender: x, y = model z, z up), tight, frac box or None, label)
SHOTS = [
    ("torii", [("torii", (0, 0))], (0.35, 1.0, 0.12), 1.0, None, "wooden torii (shinmei): the two poles"),
    ("wall", [("teahouse", (0, 0))], (0.25, 1.0, 0.08), 1.0, (0.0, 0.0, 0.0, 1.0, 1.0, 0.55),
     "K2 tea house: posts, beams, board walls"),
    ("roof", [("teahouse", (0, 0))], (0.7, 0.9, 1.1), 1.0, None, "K2 tea house thatch (_w2): moss"),
    ("bench", [("bench", (0, 0))], (0.5, 1.0, 0.55), 1.0, None, "street bench: boards"),
    ("chest", [("chest", (0, 0)), ("tansu", (1.9, 0))], (0.35, 1.0, 0.45), 1.0, None,
     "nagamochi + tansu (wood_interior, plank bands kept)"),
    ("woodpile", [("woodpile", (0, 0))], (0.4, 1.0, 0.3), 1.0, None, "firewood stack (posts / cover boards)"),
]


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
    cam = g["setup"]((900, 675))
    ground = g["plain"]("ground", (0.30, 0.29, 0.26))
    mats = {}

    def macro_for(base):
        # base like jp_m_wood_weathered_w1_co.png
        stem = base[len("jp_m_"):-len("_co.png")] if base.endswith("_co.png") else None
        if not stem:
            return None
        mid, wear = stem[:-3], stem[-2:]
        if mid in WOOD:
            name = "jp_m_macro_wood%s_%s_mc.png" % ("_dark" if mid in DARK else ("_int" if mid in INTERIOR else ""), wear)
            return os.path.join(DRAFT, name), MACRO["wood"]
        if mid == "roof_thatch" and wear in ("w1", "w2"):
            return os.path.join(DRAFT, "jp_m_macro_thatch_%s_mc.png" % wear), MACRO["thatch"]
        return None

    def mat_for(tex, after):
        key = (tex, after)
        if key in mats:
            return mats[key]
        m = bpy.data.materials.new(os.path.basename(tex))
        m.use_nodes = True
        m.use_backface_culling = True
        nt = m.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        iron = "metal" in tex
        glossy = "ceramic" in tex or "lacquer" in tex
        bsdf.inputs["Roughness"].default_value = 0.5 if iron else (0.35 if glossy else 0.88)
        bsdf.inputs["Metallic"].default_value = 0.45 if iron else 0.0
        base = os.path.basename(tex).replace(".paa", ".png")
        png = os.path.join(DRAFT, base) if after and os.path.isfile(os.path.join(DRAFT, base)) else os.path.join(TEXPNG, base)
        if os.path.isfile(png):
            t = nt.nodes.new("ShaderNodeTexImage")
            t.image = bpy.data.images.load(png, check_existing=True)
            col = t.outputs["Color"]
            mc = macro_for(base) if after else None
            if mc and os.path.isfile(mc[0]):
                uvn = nt.nodes.new("ShaderNodeUVMap")
                mp = nt.nodes.new("ShaderNodeMapping")
                mp.inputs["Scale"].default_value = (mc[1][0], mc[1][1], 1.0)
                nt.links.new(uvn.outputs["UV"], mp.inputs["Vector"])
                mt = nt.nodes.new("ShaderNodeTexImage")
                mt.image = bpy.data.images.load(mc[0], check_existing=True)
                nt.links.new(mp.outputs["Vector"], mt.inputs["Vector"])
                mix = nt.nodes.new("ShaderNodeMix")
                mix.data_type = "RGBA"
                ins = {s.identifier: s for s in mix.inputs}
                outs = {s.identifier: s for s in mix.outputs}
                nt.links.new(mt.outputs["Alpha"], ins["Factor_Float"])
                nt.links.new(col, ins["A_Color"])
                nt.links.new(mt.outputs["Color"], ins["B_Color"])
                col = outs["Result_Color"]
            nt.links.new(col, bsdf.inputs["Base Color"])
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
        mats[key] = m
        return m

    def lod_mesh(lod, name, off, after):
        verts, polys, uvs, mids, ml, lnor = [], [], [], [], [], []
        for fi, (fv, fl, tex, mat) in enumerate(lod.faces):
            pts = [lod.points[v[0]] for v in fv]
            bp = [(p[0] + off[0], p[2] + off[1], p[1]) for p in pts]
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
                nn = lod.normals[fv[i][1]]
                lnor.append((-nn[0], -nn[2], -nn[1]))
            if tex not in ml:
                ml.append(tex)
            mids.append(ml.index(tex))
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], polys)
        uv = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uv.data[i].uv = uvs[loop.vertex_index]
        for k in ml:
            me.materials.append(mat_for(k, after))
        for i, mi in enumerate(mids):
            me.polygons[i].material_index = mi
        me.update()
        try:
            me.shade_smooth()
            me.normals_split_custom_set([lnor[l.vertex_index] for l in me.loops])
        except Exception as e:
            print("custom normals failed", e)
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    os.makedirs(REN, exist_ok=True)

    def shoot(out, lo, hi, view, lens, tight):
        c = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
        v = Vector((view[0], view[1], view[2])).normalized()
        q = (-v).to_track_quat("-Z", "Y")
        rx = q @ Vector((1, 0, 0))
        uy = q @ Vector((0, 1, 0))
        th = 18.0 / lens * 0.92
        tv = th * 3 / 4
        corners = [Vector((a, b, e)) for a in (lo[0], hi[0]) for b in (lo[1], hi[1]) for e in (lo[2], hi[2])]
        d = 0.3
        for _ in range(80):
            ok = True
            for k in corners:
                w = k - (c + v * d)
                depth = w.dot(-v)
                if depth <= 0.05 or abs(w.dot(rx)) / depth > th or abs(w.dot(uy)) / depth > tv:
                    ok = False
                    break
            if ok:
                break
            d *= 1.1
        cam.location = c + v * d * tight
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = q
        cam.data.type = "PERSP"
        cam.data.lens = lens
        cam.data.clip_start = 0.02
        cam.data.clip_end = 300
        bpy.context.scene.render.filepath = os.path.join(REN, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)

    for job in jobs:
        g["clear_objects"]()
        lo, hi = [1e9] * 3, [-1e9] * 3
        for item in job["items"]:
            lods = mlod.read_mlod(item["p3d"])
            lod = next(l for l in lods if abs(l.resolution - 1.0) < 1e-3)
            ox, oz = item["off"]
            lod_mesh(lod, "m", (ox, oz), job["after"])
            for p in lod.points:
                q = (p[0] + ox, p[2] + oz, p[1])
                lo = [min(a, b) for a, b in zip(lo, q)]
                hi = [max(a, b) for a, b in zip(hi, q)]
        bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, min(lo[2], 0.0) - 0.002))
        bpy.context.active_object.data.materials.append(ground)
        if job.get("frac"):
            f = job["frac"]
            lo2 = [lo[i] + (hi[i] - lo[i]) * f[i] for i in range(3)]
            hi2 = [lo[i] + (hi[i] - lo[i]) * f[3 + i] for i in range(3)]
            lo, hi = lo2, hi2
        hi[2] = max(hi[2], lo[2] + 0.2)
        shoot(job["out"], lo, hi, tuple(job["view"]), 50, job["tight"])


def sheet(after="after", out="fx3_samples.jpg", title=None):
    from PIL import Image, ImageDraw, ImageFont
    W, H = 900, 675
    pad, lab = 8, 26
    im = Image.new("RGB", (2 * W + 3 * pad, len(SHOTS) * (H + lab + pad) + 40), (32, 32, 32))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    d.text((pad, 8), title or "FX3 wood texture variety: BEFORE (left) / AFTER (right: atlas + uvwood + macro, draft)",
           fill=(240, 240, 240), font=font)
    y = 40
    for shot, items, view, tight, frac, label in SHOTS:
        d.text((pad, y + 2), label, fill=(230, 230, 200), font=font)
        for k, mode in enumerate(("before", after)):
            p = os.path.join(REN, "%s_%s.png" % (mode, shot))
            if os.path.isfile(p):
                im.paste(Image.open(p).convert("RGB"), (pad + k * (W + pad), y + lab))
        y += H + lab + pad
    im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    im.save(os.path.join(HERE, out), quality=86)
    print("sheet", im.size)


def main():
    jobs = []
    for mode in (("insitu",) if INSITU else ("before", "after")):
        for shot, items, view, tight, frac, label in SHOTS:
            jobs.append({"out": "%s_%s" % (mode, shot), "view": view, "tight": tight, "frac": frac,
                         "after": mode != "before",
                         "items": [{"p3d": os.path.join(DEV, SHIPPED[s]) if INSITU else
                                    os.path.join(HERE, "out", mode, s + ".p3d"), "off": list(o)} for s, o in items]})
    os.makedirs(os.path.dirname(JOBS), exist_ok=True)
    with open(JOBS, "wb") as fh:
        fh.write(json.dumps(jobs, indent=1).encode("utf-8"))
    env = dict(os.environ, FX3_INSITU="1" if INSITU else "0")
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__)],
                       capture_output=True, text=True, errors="replace", env=env)
    with open(os.path.join(HERE, "_build", "render.log"), "wb") as fh:
        fh.write((r.stdout + "\n" + r.stderr).replace("\r\n", "\n").encode("utf-8"))
    done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
    print("blender exit", r.returncode, "; rendered:", len(done), "of", len(jobs))
    if r.returncode or len(done) < len(jobs):
        print(r.stderr[-1500:])
    if INSITU:
        sheet("insitu", "fx3_insitu.jpg", "FX3 in situ: BEFORE (phase-1 render, old textures) / AFTER (the rebuilt shipped "
              "masters, library atlases + macro)")
    else:
        sheet()


if __name__ == "__main__":
    if "bpy" in sys.modules:
        blender_main()
    else:
        main()
