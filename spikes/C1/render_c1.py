#!/usr/bin/env python3
r"""C1 render sheets (Blender in the background, parts/kit/render_parts.py helpers, as render_unit.py does).

  python spikes/C1/render_c1.py [family|street|seams|inns ...] [--jobs N] [--compose]

Sheets (research/production/contact_sheets/c1_*.jpg):
  c1_family.jpg   every C1 shell (69 townhouse units, 8 post-town houses, 4 inns), 3/4 view from the street
  c1_street.jpg   the island test street (both sides, as placed by buildings/registry.py C1_PLACEMENTS)
  c1_seams.jpg    the party seams close up: street front, back (lean-to) and roof, Kamigata / Edo / Tokaido rows
  c1_inns.jpg     the post-town houses and the inns (fronts, backs, the stable, cut views with the grand inn's stair)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(HERE, "renders")
SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, KIT)

STREET_O = (1024.0, 1080.0)          # the island street's centre: renders use world - this


def family_jobs():
    import registry
    jobs = []
    for b in registry.BUILDINGS:
        if "dir" not in b:
            continue
        jobs.append(("fam_" + b["key"], b["class"].replace("Land_JP_", ""), {"key": b["key"], "view": "3q", "fit": 1.0,
                                                                             "res": [480, 360]}))
    return jobs


# street scene cameras: world coordinates minus STREET_O (x east, y up, z north)
STREET = [
    ("st_north_kamigata", "North side, Kamigata row from the street (right to left: 3-ken corner, 3-ken middle, 2-ken "
     "middle, 3-ken end): one udatsu per seam, the corner pent wraps the east corner, the end's free gable with its own "
     "udatsu.", {"scene": "street", "cam": [-28.0, 1.7, -2.6], "look": [-28.0, 3.3, 7.0], "lens": 13}),
    ("st_north_edo", "North side, Edo row (2-ken end, 3-ken middle with a board roof, 2-ken middle, 3-ken corner): "
     "plastered upper fronts, board pents meeting at the lot lines under seam caps.",
     {"scene": "street", "cam": [28.0, 1.7, -2.6], "look": [28.0, 3.3, 7.0], "lens": 13}),
    ("st_south", "South side, facing north: post-town house detached (tile, plastered), the post-town row (middle, "
     "board | end, tile), the ordinary inn (5 ken, tile) and the grand inn (two storeys).",
     {"scene": "street", "cam": [-15.0, 1.7, 2.6], "look": [-15.0, 3.6, -7.0], "lens": 11}),
    ("st_street_w", "Down the street from the west end at eye height.",
     {"scene": "street", "cam": [-44.0, 1.7, 0.2], "look": [-10.0, 2.8, 0.0], "lens": 22}),
    ("st_air", "The test street from above the south-west (north side rows at the back).",
     {"scene": "street", "cam": [-6.0, 62.0, -58.0], "look": [0.0, 0.0, 3.0], "lens": 22}),
    ("st_air_e", "From above the east: the Edo row and the inns.",
     {"scene": "street", "cam": [52.0, 30.0, -26.0], "look": [14.0, 0.0, 2.0], "lens": 22}),
]

SEAMS = [
    ("seam_k_front", "Kamigata seam, street front: the udatsu owned by the left unit stands on the lot line, the two "
     "tile pents stop at it; party roof ends under one seam cap.",
     {"scene": "street", "cam": [-25.0, 3.6, -1.2], "look": [-29.1, 4.1, 4.3], "lens": 24}),
    ("seam_k_back", "Kamigata seam from the back yard: the two tile lean-tos meet flush under the seam cap; each "
     "unit's own party wall seals the kitchen (no coplanar walls).",
     {"scene": "street", "cam": [-24.0, 4.8, 16.0], "look": [-29.1, 3.0, 11.0], "lens": 24}),
    ("seam_k_roof", "Kamigata seams from above: flush party roof ends, seam caps, ridge bridges, the corner pent's hip.",
     {"scene": "street", "cam": [-24.0, 13.0, 1.0], "look": [-26.0, 5.5, 7.5], "lens": 22}),
    ("seam_e_front", "Edo seam, street front (tile end | board-roofed middle): board seam cap over the pents, the "
     "tile roof's plaster closure band over the lower boards.",
     {"scene": "street", "cam": [25.2, 3.8, -1.2], "look": [28.2, 4.3, 4.3], "lens": 24}),
    ("seam_e_back", "Edo seams from the back yard: board lean-tos flush under the seam caps.",
     {"scene": "street", "cam": [31.0, 4.8, 16.0], "look": [28.2, 3.0, 11.0], "lens": 24}),
    ("seam_e_roof", "Edo seams from above: tile / board / tile main roofs with the seam caps between them.",
     {"scene": "street", "cam": [29.0, 13.0, 1.0], "look": [28.2, 5.5, 7.5], "lens": 22}),
    ("seam_pt_front", "Tokaido row seam (board-roofed middle | tile end), from the street: board seam cap on the "
     "pents and roofs (no udatsu on the Tokaido).",
     {"scene": "street", "cam": [-21.5, 3.6, 1.2], "look": [-23.95, 4.1, -4.4], "lens": 22}),
    ("seam_pt_back", "Tokaido row seam from the back, and the middle unit's free party side sealed on its own.",
     {"scene": "street", "cam": [-29.0, 4.8, -16.5], "look": [-23.95, 3.0, -11.0], "lens": 22}),
]

INNS = [
    ("pt_det_tile_nuriya", "Post-town house, detached: tile roof, plastered upper front, komeya lattice, Ioka side pent "
     "on the toriniwa gable.", {"key": "pt_det_tile_nuriya", "view": "3q", "fit": 1.0}),
    ("pt_det_board_board", "Post-town house, detached: board roof, boarded upper front, kyo lattice.",
     {"key": "pt_det_board_board", "view": "3q", "fit": 1.0}),
    ("pt_stable_cut", "Post-town house with stable (tile): section at 2.2 m - the umaya (jp_p_frame_stall _umaya) in "
     "the 2-ken kitchen doma, clear of the passage to the back door.",
     {"key": "pt_det_stable_tile", "view": "3q", "fit": 1.0, "cut_y": 2.2, "open": 1.0}),
    ("pt_stable_back", "Post-town house with stable (board): the back, the 2-ken lean-to kitchen / stable.",
     {"key": "pt_det_stable_board", "view": "back", "fit": 1.0}),
    ("inn_std_tile", "Inn (hatago), 5 ken: tile roof, plastered upper front, kyo lattice.",
     {"key": "inn_std_tile", "view": "3q", "fit": 1.0}),
    ("inn_std_cut", "Inn (hatago) at 2.2 m: toriniwa, the front hall (choba), two guest rooms behind (single door "
     "between them), the 2-ken kitchen.", {"key": "inn_std_board", "view": "top", "fit": 1.0, "cut_y": 2.2,
                                            "open": 1.0}),
    ("inn_std_mushiko", "Inn (hatago), mushiko upper front and tile pent.",
     {"key": "inn_std_mushiko", "view": "3q", "fit": 1.0}),
    ("inn_grand", "Grand inn (two storeys, one per tier-3 town): upper storey with two shoji windows on the street and "
     "an amado window in each gable; board pent.", {"key": "inn_grand", "view": "3q", "fit": 1.0}),
    ("inn_grand_cut", "Grand inn at 4.9 m (upper storey): the stairwell with its rail, two upstairs rooms with the "
     "hikiwake pair between them.", {"key": "inn_grand", "view": "top", "fit": 1.0, "cut_y": 4.9, "open": 1.0}),
    ("inn_grand_stair", "Grand inn, the oku at 2.9 m: the box stair (kaidan-dansu) along the back wall up into the "
     "upper floor.", {"key": "inn_grand", "view": "3q", "fit": 0.8, "cut_y": 2.9, "open": 1.0}),
]

SETS = {"family": family_jobs, "street": lambda: STREET, "seams": lambda: SEAMS, "inns": lambda: INNS}


def street_part():
    import registry
    import shellkit
    from jpparts.core import Part
    R = Part("street", "", "")
    R.wear = "_w1"
    for b in registry.BUILDINGS:
        for pl in b.get("placements", []):
            if "dir" not in b:
                continue
            M, _, _ = shellkit.model(name=b["name"], **b["params"])
            x, y, z = pl["pos"]
            R.merge(M.transformed(pl["yaw"], (x - STREET_O[0], 0.0, z - STREET_O[1])))
    return R


def key_part(key):
    import registry
    import shellkit
    b = registry.get(key)
    M, _, _ = shellkit.model(name=b["name"], **b["params"])
    M.wear = "_w1"
    return M


# ================================================================================================ Blender side
def blender_main(spec):
    import bpy
    from mathutils import Vector
    import copy
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    exec(compile(src, "render_parts.py", "exec"), g)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"]((960, 720))
    gm = g["plain"]("ground", (0.36, 0.37, 0.33))
    sm = g["plain"]("street", (0.42, 0.40, 0.36))
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    for out, cap, v in spec:
        res = v.get("res", [960, 720])
        bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = res
        g["clear_objects"]()
        if v.get("scene") == "street":
            if "street" not in cache:
                cache["street"] = street_part()
            P = cache["street"]
        else:
            P = key_part(v["key"])
        if v.get("cut_y"):
            P = copy.copy(P)
            P.solids = [s for s in P.solids if s.bbox()[2] < v["cut_y"]]
        g["part_mesh"](P, "bld", lod=v.get("lod", 1), open_doors=v.get("open", 0.0))
        bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, -0.003))
        bpy.context.active_object.data.materials.append(gm)
        if v.get("scene") == "street":
            bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.0))
            st = bpy.context.active_object
            st.scale = (90.0, 7.2, 1.0)
            st.data.materials.append(sm)
            for hx in (-30.0, 0.0, 28.0):
                g["human"](hx, 0.0, 0.0)
            c = Vector(g["to_b"](v["cam"]))
            t = Vector(g["to_b"](v["look"]))
            cam.location = c
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
            cam.data.type = "PERSP"
            cam.data.lens = v["lens"]
            cam.data.clip_start = 0.05
            cam.data.clip_end = 400
        else:
            b = P.bbox()
            size = max(b[1] - b[0], b[5] - b[4], (b[3] - b[2]) * 1.3)
            if not v.get("cut_y"):
                g["human"](b[0] + 0.2 + (b[1] - b[0]) * 0.1, b[5] + 1.2, 0.0)
            tgt = ((b[0] + b[1]) / 2, min(b[3], 7.0) / 2.2, (b[4] + b[5]) / 2)
            if v["view"] == "top":
                from mathutils import Euler
                cam.location = Vector(g["to_b"]((tgt[0], 40.0, tgt[2])))
                cam.rotation_mode = "XYZ"
                cam.rotation_euler = Euler((0.0, 0.0, 0.0))
                cam.data.type = "ORTHO"
                cam.data.ortho_scale = size * 1.08 * v.get("fit", 1.0)
                cam.data.clip_start = 0.1
                cam.data.clip_end = 100
            else:
                g["look"](cam, g["to_b"](tgt), v["view"], size * 1.35 * v.get("fit", 1.0))
        bpy.context.scene.render.filepath = os.path.join(OUT, out + ".png")
        bpy.ops.render.render(write_still=True)
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
            d.text((x + 5, yy), ln, font=F["b"] if cap < 30 else F["s"], fill=(40, 40, 40))
            yy += 17
    os.makedirs(SHEETS, exist_ok=True)
    dst = os.path.join(SHEETS, "c1_%s.jpg" % name)
    im.save(dst, quality=86)
    print("sheet", dst, im.size)


def compose_all(sets):
    import glob
    import registry
    fails = 0
    nck = 0
    for p in glob.glob(os.path.join(DEV, "buildings", "*", "checks", "*.json")):
        c = json.load(open(p, encoding="utf-8"))
        nck += 1
        fails += c.get("failures", 0)
    sub = "%d C1 shells, checks %s (buildings/<family>/checks/*.json). Dark figure = 1.8 m." % (
        nck, "all pass" if not fails else "%d FAILURES" % fails)
    if "family" in sets:
        jobs = family_jobs()
        for j in jobs:
            b = registry.get(j[2]["key"])
            j[2]["cap"] = b["budget"]
        compose("family", jobs, "C1 town shells: 69 townhouse units, 8 post-town houses, 4 inns (bare)", sub, 9, 320,
                240, 22, 44)
    if "street" in sets:
        compose("street", STREET, "C1 test street on the island (z 1080, x 985-1063)", sub, 3, 640, 480, 76, 80)
    if "seams" in sets:
        compose("seams", SEAMS, "C1 party seams close up (front, back, roof)", sub, 3, 640, 480, 76, 80)
    if "inns" in sets:
        compose("inns", INNS, "C1 post-town houses (DW10) and inns (TR05)", sub, 3, 640, 480, 76, 80)


def main(argv):
    sets = [a for a in argv if a in SETS] or list(SETS)
    jobs_n = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 6
    if "--compose" not in argv:
        alljobs = [j for s in sets for j in SETS[s]()]
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
                                           stderr=subprocess.STDOUT), lf, len(part)))
        for p, lf, n in procs:
            p.wait()
            lf.close()
        done = 0
        for i in range(jobs_n):
            lp = os.path.join(OUT, "_blender_%d.log" % i)
            if os.path.isfile(lp):
                done += sum(1 for l in open(lp, encoding="utf-8", errors="replace") if l.startswith("rendered"))
        print("%d/%d rendered" % (done, len(alljobs)))
    compose_all(sets)


if __name__ == "__main__":
    if "--blender" in sys.argv:
        blender_main(json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8")))
    else:
        main(sys.argv[1:])
