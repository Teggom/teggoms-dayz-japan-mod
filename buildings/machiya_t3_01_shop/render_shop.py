#!/usr/bin/env python3
r"""Render sheets for the B4 pilot (Land_JP_Machiya_T3_01_Shop): every furnished room, the street front and the back
yard, the well, and a top-down plan with the loot points.

  python render_shop.py [job ...]       (Blender in the background, then the sheets)
  python render_shop.py --compose       (sheets only, from the PNGs)

Blender side: the building from its recipe (parts kit render helpers, Resolution 1, library textures at _w1) and
every prop / yard object from its MLOD master (spikes/B3a/out, spikes/B3b/out) at its proxy / placement pose.
Outputs renders/*.png, machiya_t3_01_shop_sheet.jpg (rooms) and machiya_t3_01_shop_site.jpg (street, yard, plan).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(HERE, "renders")
RES = (1280, 800)

# (out, sheet, caption, spec). Cameras in the MODEL frame (x, y up, z = street front).
JOBS = [
    ("room_toriniwa", "rooms", "Toriniwa (doma passage), from the entrance: kept clear - a shelf on the board wall "
     "between the two step stones, a bucket, a tipped bucket at the kitchen passage, leaves and straw on the tataki.",
     {"cam": [-2.55, 1.62, 4.25], "look": [-3.05, 0.75, -0.6], "lens": 16}),
    ("room_mise", "rooms", "Mise (shop: general goods): board display strip behind the degoshi with a stepped stand "
     "and paper bundles, choba corner (desk + lattice), brazier, tobacco tray spilled, stock shelf with a board down.",
     {"cam": [-1.25, 1.70, 2.25], "look": [2.9, 0.7, 3.8], "lens": 16}),
    ("room_mise_back", "rooms", "Mise from the street corner: the board strip (mise-ita) at the lattice, 6 mats, the "
     "tatami-yose board at the back wall; doors to the toriniwa and the zashiki open.",
     {"cam": [3.35, 1.70, 4.30], "look": [-1.2, 0.5, 2.1], "lens": 16, "open": 1.0}),
    ("room_zashiki", "rooms", "Zashiki: bedding laid out, a folded stack in the corner (no oshiire), the tansu "
     "ransacked (drawers out), andon (unlit), round brazier, wicker trunk.",
     {"cam": [-1.30, 1.65, 1.35], "look": [2.6, 0.55, -0.5], "lens": 16}),
    ("room_kitchen", "rooms", "Kitchen doma: two pots on the kamado (one lid off), wooden sink with a shelf over it, "
     "the water jar, the kamidana high on the wall (undisturbed), firewood under the window.",
     {"cam": [-0.45, 1.60, -4.15], "look": [-2.6, 1.05, -1.1], "lens": 16}),
    ("room_storage", "rooms", "Storage (boards): shelving, long chest with its lid thrown back, rice bales (one "
     "burst), boxes, wicker trunks, a big jar, a straw mat.",
     {"cam": [0.35, 1.65, -2.60], "look": [3.2, 0.65, -2.8], "lens": 14}),
    ("street", "site", "Street front: long noren on the entrance, kake-andon, short mizuhiki curtain under the pent, "
     "hanging signboard, tipped bench, covered gutter with a slab at the door, fire tub, banner, cart, Jizo box.",
     {"view": "3q", "persp": 30, "target": [0.0, 1.6, 5.5], "dist": 17}),
    ("street_door", "site", "At the door: noren, kake-andon, carrying pole leaning on the gable, slab over the gutter.",
     {"cam": [-1.2, 1.6, 8.6], "look": [-2.9, 1.3, 4.6], "lens": 26}),
    ("yard", "site", "Back yard (north when placed): pulley well with a rope on its beam, tubs and buckets by the back "
     "door, firewood against the kitchen wall, laundry pole with its cloth fallen.",
     {"cam": [-8.0, 3.4, -13.5], "look": [-0.8, 0.9, -6.5], "lens": 22}),
    ("yard_toilet", "site", "B2's walk-in toilet (Land_JP_Toilet_T1_01) at the back of the yard, its hinged half door "
     "OPEN (swings out towards the house): the half door's first in-game test.",
     {"cam": [5.4, 1.9, -7.9], "look": [2.3, 1.0, -10.3], "lens": 20, "open": 1.0}),
    ("well", "site", "The pulley well (Land_JP_S_Well_Tsurube_Curb_Stone, a vanilla Well): crouch at the curb to "
     "drink, wash hands, fill a bottle.",
     {"cam": [-0.4, 1.4, -10.6], "look": [-2.4, 0.8, -8.3], "lens": 24}),
    ("plan", "site", "Plan cut at 1.75 m (north = model back, down): loot points, GREEN = floor (lootFloor), ORANGE = on "
     "furniture (lootshelves). Street at the top.",
     {"plan": True, "scale": 16.5, "cut_y": 1.75}),
    ("plan_site", "site", "Site plan: the house, the street dressing (top) and the yard (bottom).",
     {"plan": True, "scale": 30.0, "cut_y": 30.0, "center": [0.0, 0.0]}),
]


# ================================================================================================ Blender side
def blender_main(spec):
    import bpy
    from mathutils import Vector, Euler
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    sys.path.insert(0, KIT)
    exec(compile(src, "render_parts.py", "exec"), g)
    sys.path.insert(0, HERE)
    import machiya_t3_01_shop as MS
    from jpparts import mlod, decor as DC
    M, floors, rooms = MS.model()
    D = MS.D
    pts = MS.loot_points(floors)
    # B2's toilet (its own registry building) where the registry places it: (2.3, -11.2) in this model frame
    sys.path.insert(0, os.path.join(DEV, "buildings", "toilet_t1_01"))
    import toilet_t1_01 as TT
    TOILET = TT.model()[0].transformed(0.0, (2.3, 0.0, -11.2))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"](RES)
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

    def prop_mesh(it, cut_y=None):
        mp = it["info"]["master"]
        if mp not in lodcache:
            lodcache[mp] = next(l for l in mlod.read_mlod(mp) if abs(l.resolution - 1.0) < 1e-3)
        lod = lodcache[mp]
        verts, polys, uvs, mids, ml = [], [], [], [], []
        for fv, fl, tex, mat in lod.faces:
            pts_ = [DC.to_model(it, lod.points[v[0]]) for v in fv]
            if cut_y is not None and min(p[1] for p in pts_) > cut_y:
                continue
            bp = [g["to_b"](p) for p in pts_]
            inward = lod.normals[fv[0][1]]
            r, _, f = __import__("jpparts.proxies", fromlist=["frame"]).frame(it["yaw"])
            n = (r[0] * inward[0] + f[0] * inward[2], inward[1], r[2] * inward[0] + f[2] * inward[2])
            want = g["to_b"]((-n[0], -n[1], -n[2]))
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
        return ob

    def marker(p, rgb, r=0.09):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=g["to_b"](p), segments=10, ring_count=6)
        ob = bpy.context.active_object
        m = bpy.data.materials.new("mk%s" % str(rgb))
        m.use_nodes = True
        b = m.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = rgb + (1.0,)
        b.inputs["Emission Color"].default_value = rgb + (1.0,)
        b.inputs["Emission Strength"].default_value = 2.0
        ob.data.materials.append(m)

    os.makedirs(OUT, exist_ok=True)
    for out, sheet, cap, v in spec:
        g["clear_objects"]()
        P = M
        cut = v.get("cut_y")
        if cut:
            import copy
            P = copy.copy(M)
            P.solids = [s for s in M.solids if s.bbox()[2] < cut]
        g["part_mesh"](P, "bld", lod=1, open_doors=v.get("open", 0.0))
        if not cut or cut > 5:
            g["part_mesh"](TOILET, "toilet", lod=1, open_doors=v.get("open", 0.0))
        for it in D.items + D.site:
            prop_mesh(it, cut)
        bpy.ops.mesh.primitive_plane_add(size=160, location=(0, 0, -0.003))
        bpy.context.active_object.data.materials.append(gm)
        sc = bpy.context.scene
        if v.get("plan"):
            c = v.get("center", [0.0, 0.0])
            cam.location = Vector(g["to_b"]((c[0], 40.0, c[1])))
            cam.rotation_mode = "XYZ"
            cam.rotation_euler = Euler((0.0, 0.0, 0.0))
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = v["scale"]
            cam.data.clip_start = 0.1
            cam.data.clip_end = 100
            if out == "plan":
                for p in pts:
                    rgb = (0.1, 0.85, 0.15) if p["container"] == "lootFloor" else (1.0, 0.45, 0.0)
                    x, y, z = p["model"]
                    marker((x, y + 0.03, z), rgb, 0.08)
        elif v.get("cam"):
            c = Vector(g["to_b"](v["cam"]))
            t = Vector(g["to_b"](v["look"]))
            cam.location = c
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
            cam.data.type = "PERSP"
            cam.data.lens = v["lens"]
            cam.data.clip_start = 0.05
            lamp = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "POINT"))
            lamp.data.energy = 700
            lamp.location = c + Vector((0, 0, 0.3))
            sc.collection.objects.link(lamp)
        else:
            g["look"](cam, g["to_b"](v["target"]), v["view"], 10, dist=v.get("dist", 25), lens=v["persp"] * 1.4)
        sc.render.filepath = os.path.join(OUT, out + ".png")
        bpy.ops.render.render(write_still=True)
        for ob in list(bpy.data.objects):
            if ob.type == "LIGHT" and ob.name.startswith("fill"):
                bpy.data.objects.remove(ob, do_unlink=True)
        print("rendered", out)


# ================================================================================================ sheets
def compose():
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 30),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 16),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 17)}.items()}
    chk = os.path.join(HERE, "checks.json")
    line = ""
    if os.path.isfile(chk):
        c = json.load(open(chk, encoding="utf-8"))
        n = len(c["checks"])
        ok = sum(1 for x in c["checks"] if x["ok"])
        line = "Checks %d/%d pass (the machiya's %d + %d decorator checks). " % (ok, n, c.get("machiya_checks", 78),
                                                                               n - c.get("machiya_checks", 78))
    for sheet, title in (("rooms", "Land_JP_Machiya_T3_01_Shop - B4 pilot: the furnished rooms"),
                         ("site", "Land_JP_Machiya_T3_01_Shop - B4 pilot: street front, yard, loot plan")):
        jobs = [j for j in JOBS if j[1] == sheet]
        cols, cw, ch, cap = 2, 960, 600, 78
        rows = (len(jobs) + cols - 1) // cols
        W = cols * cw + (cols + 1) * 10
        H = 96 + rows * (ch + cap + 10) + 10
        im = Image.new("RGB", (W, H), (236, 234, 229))
        d = ImageDraw.Draw(im)
        d.text((14, 12), title, font=F["h1"], fill=(20, 20, 20))
        d.text((14, 56), line + "Props are proxies of the B3a / B3b models (Resolution 1 shown), _w1 textures; "
               "Blender light, not engine light.", font=F["s"], fill=(60, 60, 60))
        for i, (out, _, caption, v) in enumerate(jobs):
            x = 10 + (i % cols) * (cw + 10)
            y = 96 + (i // cols) * (ch + cap + 10)
            p = os.path.join(OUT, out + ".png")
            if os.path.isfile(p):
                im.paste(Image.open(p).convert("RGB").resize((cw, ch)), (x, y))
            d.rectangle([x, y + ch, x + cw, y + ch + cap], fill=(250, 249, 246))
            d.text((x + 6, y + ch + 4), out, font=F["b"], fill=(20, 20, 20))
            yy = y + ch + 24
            for ln in textwrap.wrap(caption, 112)[:3]:
                d.text((x + 6, yy), ln, font=F["s"], fill=(50, 50, 50))
                yy += 17
        dst = os.path.join(HERE, "machiya_t3_01_shop_%s.jpg" % sheet)
        im.save(dst, quality=87)
        print("sheet", dst, im.size)


def main(argv):
    if "--compose" not in argv:
        only = [a for a in argv if not a.startswith("--")]
        jobs = [j for j in JOBS if not only or j[0] in only]
        os.makedirs(OUT, exist_ok=True)
        jf = os.path.join(OUT, "_jobs.json")
        with open(jf, "wb") as f:
            f.write(json.dumps(jobs).encode("utf-8"))
        r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__), "--",
                            "--blender", jf], capture_output=True, text=True, errors="replace")
        done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
        print("%d/%d rendered" % (len(done), len(jobs)))
        if len(done) < len(jobs):
            print((r.stdout + r.stderr)[-4000:])
    compose()


if __name__ == "__main__":
    if "--blender" in sys.argv:
        blender_main(json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8")))
    else:
        main(sys.argv[1:])
