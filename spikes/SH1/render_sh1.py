#!/usr/bin/env python3
r"""SH1 renders: overview sheets and the labelled overhead maps (Blender in the background, EEVEE; parts/kit/render_parts
helpers, the C3 building / prop-mesh pattern) on the real terrain.

  python spikes/SH1/render_sh1.py [shrine|graveyard|shops|gallery|maps ...] [--jobs N] [--compose]

Data (system Python): the registry buildings (buildings/registry.py placements) and their furniture / site items,
test/placements/C3.csv and SH1.csv props at ground + y_offset, T's trees (stand-ins: trunk + crown), the heightmap
(a 1 m mesh). Outputs: spikes/SH1/renders/*.png, research/production/contact_sheets/sh1_*.jpg; the maps
(sh1_map_<area>.jpg) get their ID labels drawn with PIL from spikes/SH1/showcase_items.json (map_labels.py).
"""
import csv
import json
import math
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
for p in (BLD, KIT, os.path.join(DEV, "spikes", "B_building", "kit"), os.path.join(DEV, "spikes", "C3"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)
OY = 25.0     # scene height origin (the yard)


# ================================================================================================ data (system Python)
def scene_data(region, pad=6.0):
    """Everything inside region (x0, x1, z0, z1) + pad, in world coordinates (y = height ASL)."""
    import registry
    import terrain_sh1 as T
    x0, x1, z0, z1 = region
    X0, X1, Z0, Z1 = x0 - pad, x1 + pad, z0 - pad, z1 + pad
    blds = []
    for b in registry.BUILDINGS:
        for pl in b.get("placements", []):
            x, y, z = pl["pos"]
            if X0 - 8 <= x <= X1 + 8 and Z0 - 8 <= z <= Z1 + 8:
                blds.append((b["key"], x, y, z, pl["yaw"]))
    props = []
    for fn in ("C3.csv", "SH1.csv"):
        p = os.path.join(DEV, "test", "placements", fn)
        for r in csv.DictReader(open(p)):
            x, z = float(r["x"]), float(r["z"])
            if not (X0 <= x <= X1 and Z0 <= z <= Z1):
                continue
            name = os.path.basename(r["p3d"])[:-4]
            y = T.ground(x, z) + float(r["y_offset"] or 0.0)
            props.append((name, x, y, z, float(r["yaw_deg"])))
    trees = [(float(tx), float(ty), float(tz), float(ts)) for tx, tz, ty, ts in T.trees()
             if X0 <= tx <= X1 and Z0 <= tz <= Z1]
    for name, x, y, z, yaw in props:
        if name.startswith("t_"):
            trees.append((x, y, z, 1.25 if "fagus" in name else 1.1))
    step = 1.0
    nx, nz = int((X1 - X0) / step) + 1, int((Z1 - Z0) / step) + 1
    hs = [[round(T.ground(X0 + i * step, Z0 + j * step), 3) for i in range(nx)] for j in range(nz)]
    return {"buildings": blds, "props": [p for p in props if not p[0].startswith("t_")], "trees": trees,
            "terrain": {"x0": X0, "z0": Z0, "step": step, "nx": nx, "nz": nz, "h": hs}}


def eye(x, z, h=1.7):
    import terrain_sh1 as T
    return [x, T.ground(x, z) + h, z]


def at(x, z, h=1.2):
    import terrain_sh1 as T
    return [x, T.ground(x, z) + h, z]


# ================================================================================================ Blender side
def blender_main(spec):
    import bpy
    import copy
    from mathutils import Vector, Euler
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    exec(compile(src, "render_parts.py", "exec"), g)
    from jpparts import mlod, decor as DC
    from jpkit import loot as bloot
    import render_c3 as RC
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"]((1280, 800))
    gm = g["plain"]("ground", (0.40, 0.38, 0.30))
    trunk_m = g["plain"]("trunk", (0.25, 0.18, 0.12))
    crown_m = g["plain"]("crown", (0.42, 0.36, 0.16))      # autumn
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

    cache = {}

    def get_bundle(key):
        if key not in cache:
            cache[key] = RC.bundle(key)
        return cache[key]

    def terrain_mesh(t, ox, oz):
        verts = []
        for j in range(t["nz"]):
            for i in range(t["nx"]):
                verts.append(g["to_b"]((t["x0"] + i * t["step"] - ox, t["h"][j][i] - OY - 0.01, t["z0"] + j * t["step"] - oz)))
        faces = []
        for j in range(t["nz"] - 1):
            for i in range(t["nx"] - 1):
                a = j * t["nx"] + i
                faces.append([a, a + 1, a + 1 + t["nx"], a + t["nx"]])
        me = bpy.data.meshes.new("terrain")
        me.from_pydata(verts, [], faces)
        me.update()
        ob = bpy.data.objects.new("terrain", me)
        ob.data.materials.append(gm)
        bpy.context.scene.collection.objects.link(ob)

    def tree(x, y, z, s, ox, oz):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.32 * s, depth=7.0 * s,
                                            location=g["to_b"]((x - ox, y - OY + 3.5 * s, z - oz)), vertices=10)
        bpy.context.active_object.data.materials.append(trunk_m)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=4.2 * s, subdivisions=2,
                                              location=g["to_b"]((x - ox, y - OY + 10.5 * s, z - oz)))
        bpy.context.active_object.data.materials.append(crown_m)

    cat = DC.catalog()
    os.makedirs(OUT, exist_ok=True)
    for out, cap, v in spec:
        g["clear_objects"]()
        sc = bpy.context.scene
        sc.render.resolution_x, sc.render.resolution_y = v.get("res", [1280, 800])
        D = v["data"]
        ox, oz = v["origin"]
        bcut = v.get("bcut")
        terrain_mesh(D["terrain"], ox, oz)
        for key, x, y, z, yaw in D["buildings"]:
            M, items, site, pts = get_bundle(key)
            P = M
            if bcut is not None:
                P = copy.copy(M)
                P.solids = [s for s in M.solids if s.bbox()[2] < bcut]
            P = P.transformed(-yaw, (x - ox, y - OY, z - oz))
            g["part_mesh"](P, key, lod=1, open_doors=v.get("open", 0.0))

            def xf(p, pos=(x, y - OY, z), yaw=yaw):
                w = bloot.model_to_world(p, pos, yaw)
                return (w[0] - ox, w[1], w[2] - oz)
            for it in items + site:
                prop_mesh(it, xf, bcut)
        for name, x, y, z, yaw in D["props"]:
            if name not in cat:
                continue
            it = {"name": name, "info": cat[name], "x": x - ox, "y": y - OY, "z": z - oz, "yaw": yaw}
            prop_mesh(it, lambda p: p)
        if v.get("trees", True):
            for x, y, z, s in D["trees"]:
                tree(x, y, z, s, ox, oz)
        for hx, hz, hy in v.get("humans", []):
            g["human"](hx - ox, hz - oz, hy - OY)
        if v.get("plan"):
            c = v["center"]
            cam.location = Vector(g["to_b"]((c[0] - ox, 150.0, c[1] - oz)))
            cam.rotation_mode = "XYZ"
            cam.rotation_euler = Euler((0.0, 0.0, 0.0))
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = v["scale"]
            cam.data.clip_start = 0.1
            cam.data.clip_end = 400
        else:
            c = Vector(g["to_b"]((v["cam"][0] - ox, v["cam"][1] - OY, v["cam"][2] - oz)))
            t = Vector(g["to_b"]((v["look"][0] - ox, v["look"][1] - OY, v["look"][2] - oz)))
            cam.location = c
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
            cam.data.type = "PERSP"
            cam.data.lens = v.get("lens", 24)
            cam.data.clip_start = 0.05
            cam.data.clip_end = 900
        sc.render.filepath = os.path.join(OUT, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)


# ================================================================================================ jobs
def jobs():
    S, G, H, L, M = {}, {}, {}, {}, {}
    r_sh = (1008.0, 1066.0, 1092.0, 1268.0)
    r_gr = (984.0, 1022.0, 1102.0, 1134.0)
    r_st = (972.0, 1068.0, 1066.0, 1102.0)
    r_ga = (1062.0, 1098.0, 1014.0, 1042.0)
    data = {"shrine": scene_data(r_sh), "graveyard": scene_data(r_gr, 10.0), "street": scene_data(r_st),
            "gallery": scene_data(r_ga), "wide": scene_data((972.0, 1072.0, 1062.0, 1268.0))}

    def J(area, out, cap, **v):
        d = {"shrine": S, "graveyard": G, "street": H, "gallery": L}[area]
        key = {"shrine": "shrine", "graveyard": "graveyard", "street": "street", "gallery": "gallery"}[area]
        v.setdefault("origin", [1024.0, 1100.0])
        v["data"] = data[v.pop("dkey", key)]
        d[out] = (out, cap, v)
    # --- shrine
    J("shrine", "sh1_s1", "From the town street: the first stone torii (S01), the banners, the approach", cam=eye(1024, 1092.5), look=at(1024, 1125, 2.5), lens=22)
    J("shrine", "sh1_s2", "Inside the second torii: water basin (S15), lantern pairs, the wooden myojin (S22)", cam=eye(1022.0, 1137), look=at(1024, 1175, 1.8), lens=24)
    J("shrine", "sh1_s3", "The sub-shrine row (S40-S51): every small torii form, huts / stones as stand-ins", cam=eye(1029.0, 1147), look=at(1037, 1172, 1.0), lens=24)
    J("shrine", "sh1_s4", "Hall site (empty) between the joyato, the sacred beech with its rope (S33/S34)", cam=eye(1024, 1171), look=at(1030, 1196, 2.0), lens=22)
    J("shrine", "sh1_s5", "Foot of the hill stair: stone torii S63, the wide flights with cheek walls", cam=eye(1041.0, 1219.5), look=at(1042, 1240, 1.0), lens=22)
    J("shrine", "sh1_s6", "Halfway up: myojin torii spanning the stair (S64-S68)", cam=eye(1042.0, 1236.0), look=at(1042, 1252, 1.2), lens=24)
    J("shrine", "sh1_s7", "From the oku-miya down the stair over the town", cam=eye(1043.2, 1261.8), look=at(1038, 1215, -6.0), lens=22)
    J("shrine", "sh1_s8", "The Inari corner: vermilion torii over the narrow stair (S80-S85)", cam=eye(1055.5, 1221.0), look=at(1058, 1238, 1.0), lens=24)
    J("shrine", "sh1_s9", "Aerial from the south-east: town street, approach, precinct, the hill stairs", cam=[1092.0, 105.0, 1060.0], look=[1025.0, 28.0, 1170.0], lens=24, dkey="wide")
    # --- graveyard
    J("graveyard", "sh1_g1", "From the gate (east): six Jizo (GJ), water point (GW), the rows", cam=eye(1016.5, 1116.5), look=at(997, 1119, 0.2), lens=24, origin=[1000.0, 1118.0])
    J("graveyard", "sh1_g2", "From the front (south) up the middle aisle", cam=eye(1000.2, 1104.0), look=at(1000, 1124, 0.2), lens=24, origin=[1000.0, 1118.0])
    J("graveyard", "sh1_g3", "The old section: gorinto 2.0 m on its platform (G7-10), hokyointo, mossy stones", cam=eye(1000.3, 1121.4, 1.6), look=at(1002, 1126.0, 0.7), lens=26, origin=[1000.0, 1118.0])
    J("graveyard", "sh1_g4", "The poor graves at the front: wooden posts on mounds, field stones", cam=eye(994.0, 1105.0, 1.5), look=at(994, 1110.5, 0.2), lens=26, origin=[1000.0, 1118.0])
    J("graveyard", "sh1_g5", "Aerial", cam=[1022.0, 48.0, 1096.0], look=[999.0, 25.0, 1118.0], lens=24, origin=[1000.0, 1118.0])
    # --- street (demo shops)
    J("street", "sh1_h1", "Kamigata row: D6 dolls, D2 tobacco (inserted), paper + rice (C3), D3 sweets (east end)", cam=eye(976.5, 1079.6), look=at(995, 1087, 1.5), lens=20, origin=[1016.0, 1084.0])
    J("street", "sh1_h2", "Edo row: D4 apothecary (west end), D1 ironmonger, D5 tailor, cloth + sake (C3)", cam=eye(1033.5, 1079.6), look=at(1052, 1087, 1.5), lens=20, origin=[1016.0, 1084.0])
    for k, (sid, x, lab) in enumerate([("D1", 1046.146, "ironmonger"), ("D2", 989.236, "tobacco"), ("D3", 1003.238, "sweets"),
                                       ("D4", 1040.590, "apothecary"), ("D5", 1050.824, "tailor"), ("D6", 984.558, "dolls")]):
        J("street", "sh1_h%d" % (3 + k), "%s %s: the front and its signs" % (sid, lab), cam=eye(x + 0.6, 1078.6, 1.6),
          look=at(x, 1085.0, 1.9), lens=22, origin=[1016.0, 1084.0])
    J("street", "sh1_h9", "Aerial of the street", cam=[1016.0, 70.0, 1046.0], look=[1016.0, 25.0, 1086.0], lens=24, origin=[1016.0, 1084.0])
    # --- gallery
    J("gallery", "sh1_l1", "The gallery from the south: sheds LS1-LS3, the ground strip", cam=eye(1080, 1012.5), look=at(1080, 1032, 0.8), lens=22, origin=[1080.0, 1030.0])
    J("gallery", "sh1_l2", "Shed 1: walls, post and beam items (L1-L14, L47)", cam=eye(1072.0, 1031.2, 1.6), look=at(1072, 1037.8, 1.3), lens=20, origin=[1080.0, 1030.0])
    J("gallery", "sh1_l3", "Shed 2: shelves with the surface items, living-room floor items", cam=eye(1080.0, 1031.2, 1.6), look=at(1080, 1037.8, 1.1), lens=20, origin=[1080.0, 1030.0])
    J("gallery", "sh1_l4", "Shed 3: work + tier floor items, eaves pieces", cam=eye(1088.0, 1031.0, 1.6), look=at(1088, 1037.8, 0.9), lens=20, origin=[1080.0, 1030.0])
    J("gallery", "sh1_l5", "Ground strip (L51-L74 outdoor) from the west", cam=eye(1064.5, 1022.0, 2.2), look=at(1082, 1026, 0.2), lens=22, origin=[1080.0, 1030.0])
    J("gallery", "sh1_l6", "Aerial", cam=[1101.0, 45.0, 1006.0], look=[1080.0, 25.0, 1029.0], lens=24, origin=[1080.0, 1030.0])
    # --- maps (top-down ortho; labels drawn afterwards by map_labels.py)
    MAPS = {"shrine": ((1037.0, 1180.0), 182.0, [900, 1800], "shrine", None),
            "graveyard": ((1001.0, 1118.0), 32.0, [1800, 1500], "graveyard", None),
            "gallery": ((1080.0, 1028.0), 34.0, [2000, 1500], "gallery", 2.45),
            "street": ((1018.0, 1085.0), 92.0, [2200, 900], "street", None)}
    for k, (c, scale, res, dk, bcut) in MAPS.items():
        v = {"plan": True, "center": list(c), "scale": scale, "res": res, "origin": list(c), "data": data[dk],
             "trees": k != "gallery", "bcut": bcut}
        M["sh1_map_%s_raw" % k] = ("sh1_map_%s_raw" % k, k, v)
    return {"shrine": S, "graveyard": G, "shops": H, "gallery": L, "maps": M}, MAPS


SHEET_META = {"shrine": ("SH1 shrine (north of the town street)", 3), "graveyard": ("SH1 graveyard (west of the approach)", 3),
              "shops": ("SH1 the six S1 demo shops on the test street", 3), "gallery": ("SH1 life-layer gallery (east yard)", 3)}


def compose(name, items):
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 30),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 16)}.items()}
    title, cols = SHEET_META[name]
    cw, ch, cap = 640, 400, 40
    rows = (len(items) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw + (cols + 1) * 8, 70 + rows * (ch + cap + 8) + 8), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((12, 10), title, font=F["h1"], fill=(20, 20, 20))
    d.text((12, 46), "Blender preview (EEVEE, Res 1 LODs, trees are stand-ins); IDs as in TEST_CHECKLIST.md / spikes/SH1/SHOWCASE_MAP.md",
           font=F["s"], fill=(60, 60, 60))
    for i, (out, caption, v) in enumerate(items):
        x = 8 + (i % cols) * (cw + 8)
        y = 70 + (i // cols) * (ch + cap + 8)
        p = os.path.join(OUT, out + ".png")
        if os.path.isfile(p):
            im.paste(Image.open(p).convert("RGB").resize((cw, ch)), (x, y))
        d.rectangle([x, y + ch, x + cw, y + ch + cap], fill=(250, 249, 246))
        yy = y + ch + 3
        for ln in textwrap.wrap(caption, 78)[:2]:
            d.text((x + 5, yy), ln, font=F["s"], fill=(40, 40, 40))
            yy += 17
    os.makedirs(SHEETS, exist_ok=True)
    dst = os.path.join(SHEETS, "sh1_%s.jpg" % name)
    im.save(dst, quality=86)
    print("sheet", dst, im.size)


def run_jobs(alljobs, jobs_n):
    os.makedirs(OUT, exist_ok=True)
    procs = []
    per = (len(alljobs) + jobs_n - 1) // jobs_n      # contiguous chunks: one process mostly builds one area's houses
    for i in range(jobs_n):
        part = alljobs[i * per:(i + 1) * per]
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
    J, MAPS = jobs()
    sets = [a for a in argv if a in J] or list(J)
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    if "--compose" not in argv:
        todo = [j for s in sets for j in J[s].values() if only is None or j[0] in only]
        run_jobs(todo, min(jobs_n, len(todo)))
    if only:
        return 0
    for s in sets:
        if s != "maps":
            compose(s, list(J[s].values()))
    if "maps" in sets:
        import map_labels
        map_labels.main(MAPS)
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        spec = json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8"))
        blender_main(spec)
    else:
        sys.exit(main(sys.argv[1:]))
