#!/usr/bin/env python3
r"""C2 render sheets (Blender in the background; parts/kit/render_parts.py helpers, as spikes/C1/render_c1.py).

  python spikes/C2/render_c2.py [family|hamlet|interior|preview ...] [--keys k1,k2] [--jobs N] [--compose]

Sheets (research/production/contact_sheets/c2_*.jpg):
  c2_family.jpg    every C2 rural shell (farmhouses, huts, sheds), 3/4 view from the front
  c2_hamlet.jpg    the test-island hamlet as placed by buildings/registry.py C2_PLACEMENTS
  c2_interior.jpg  inside views: the sooted koyagumi over the hiroma / daidokoro, the irori pit, the doma, the stalls
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

HAMLET_O = (950.0, 1024.0)            # the hamlet's centre on the island: scene coordinates = world - this
ROOF_TAGS = ("thatch_body", "thatch_band", "lath", "rafter", "hip_roll", "thatch_ridge", "ridge_bamboo", "binding",
             "umanori", "umanori_pole", "turf", "iris", "sheathing", "board_field", "board_field_lod", "eave_stack",
             "kawara_field", "roof_geo_front", "roof_geo_back", "roof_geo_left", "roof_geo_right", "hafu",
             "verge_batten", "board_ridge", "ridge_batten", "ridge_stone", "stone", "batten", "kemuri_bar",
             "kemuri_dark", "small_hafu", "kemuri_sill", "thatch_roll", "noshi", "cap", "noshi_far", "eave_tile",
             "tile_bed", "fascia", "bed", "flashing", "lashing_rope")


def family_jobs():
    import registry
    jobs = []
    for b in registry.BUILDINGS:
        if b.get("dir") not in ("farmhouse", "hut", "shed"):
            continue
        jobs.append(("fam_" + b["key"], b["class"].replace("Land_JP_", ""), {"key": b["key"], "view": "3q", "fit": 1.0,
                                                                             "res": [480, 360]}))
    return jobs


# interior views, model frame of the shell (x right along the front, y up, z = front (+) .. back (-))
INTERIOR = [
    ("in_kanto_hiroma", "Kanto farmhouse (DW06), inside from the doma: the hiroma over the agari-kamachi with its irori "
     "pit, the sooted koyagumi above (log ushibari on the joya posts, sasu, purlins, the lath under the thatch).",
     {"key": "farmhouse_kanto_yosemune_umaya", "cam": [5.6, 1.7, 2.6], "look": [-1.5, 2.6, -1.2], "lens": 14}),
    ("in_kanto_up", "Kanto farmhouse: looking up into the sooted roof from the hiroma (joya plate, geya beams to the "
     "outer walls: the aisles under the one sweeping roof).",
     {"key": "farmhouse_kanto_yosemune_umaya", "cam": [-0.5, 1.9, 2.8], "look": [0.2, 6.5, -2.0], "lens": 12}),
    ("in_kanto_cut", "Kanto farmhouse, thatch and lath removed: the koyagumi from above (sasu pairs lashed at the ridge, "
     "joya core 3 ken + geya aisles 1 ken), the irori pit, the umaya in the doma corner.",
     {"key": "farmhouse_kanto_yosemune_umaya", "view": "3q", "fit": 1.0, "drop": "roof"}),
    ("in_kanto_plan", "Kanto farmhouse at 2.2 m: dei (tatami) / nando | hiroma with the irori | doma with the stall, "
     "kamado spot on the end wall.", {"key": "farmhouse_kanto_yosemune_umaya", "view": "top", "fit": 1.0, "cut_y": 2.2,
                                      "open": 1.0}),
    ("in_kinai_daidokoro", "Kinai farmhouse (DW07), from the niwa: the daidokoro's irori, the tall sooted roof over the "
     "rooms (tie beams at 4.1 m, sasu), the ox stall behind.",
     {"key": "farmhouse_kinai_kirizuma_tile_takahe", "cam": [-4.8, 1.7, 2.8], "look": [2.0, 2.8, -2.0], "lens": 14}),
    ("in_kinai_plan", "Kinai farmhouse at 2.2 m: niwa with the ox stall and the kamado spot | mise / daidokoro | "
     "zashiki (tatami) / nando.", {"key": "farmhouse_kinai_kirizuma_tile_takahe", "view": "top", "fit": 1.0,
                                   "cut_y": 2.2, "open": 1.0}),
    ("in_hut_east", "Poor hut east (DW01), earth floor: the stone-ringed hearth under the sooted sasu and tie beams.",
     {"key": "hut_east_l_earth", "cam": [-2.6, 1.6, 1.9], "look": [1.2, 1.4, -1.0], "lens": 14}),
    ("in_hut_board", "Poor hut east, board floor: the raised floor with the irori pit over the kamachi and step.",
     {"key": "hut_east_l_board", "cam": [-3.0, 1.6, 2.2], "look": [1.2, 1.0, -1.0], "lens": 14}),
    ("in_hut_west", "Poor hut west (DW30), thatch gable: board walls inside, the bamboo-slat / board floor, "
     "the sooted roof.", {"key": "hut_west_thatch_leanl", "cam": [-2.0, 1.6, 1.3], "look": [1.8, 1.8, -1.0],
                         "lens": 14}),
]


def hamlet_jobs():
    return [
        ("ham_air", "The hamlet from above the south-east.",
         {"scene": "hamlet", "cam": [38.0, 34.0, -42.0], "look": [0.0, 0.0, 0.0], "lens": 22}),
        ("ham_air_w", "From above the north-west.",
         {"scene": "hamlet", "cam": [-40.0, 30.0, 40.0], "look": [0.0, 0.0, 0.0], "lens": 22}),
        ("ham_eye_s", "At eye height from the south lane.",
         {"scene": "hamlet", "cam": [4.0, 1.7, -34.0], "look": [0.0, 3.0, 0.0], "lens": 16}),
        ("ham_eye_n", "At eye height from the north.",
         {"scene": "hamlet", "cam": [-4.0, 1.7, 36.0], "look": [0.0, 3.0, 0.0], "lens": 16}),
    ]


SETS = {"family": family_jobs, "hamlet": hamlet_jobs, "interior": lambda: INTERIOR}


def hamlet_part():
    import registry
    import ruralkit
    from jpparts.core import Part
    R = Part("hamlet", "", "")
    R.wear = "_w1"
    for b in registry.BUILDINGS:
        if b.get("dir") not in ("farmhouse", "hut", "shed"):
            continue
        for pl in b.get("placements", []):
            M, _, _ = ruralkit.model(name=b["name"], **b["params"])
            x, y, z = pl["pos"]
            R.merge(M.transformed(pl["yaw"], (x - HAMLET_O[0], 0.0, z - HAMLET_O[1])))
    return R


def key_part(key):
    import registry
    import ruralkit
    b = registry.get(key)
    M, _, _ = ruralkit.model(name=b["name"], **b["params"])
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
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    for out, cap, v in spec:
        res = v.get("res", [960, 720])
        bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = res
        g["clear_objects"]()
        if v.get("scene") == "hamlet":
            if "hamlet" not in cache:
                cache["hamlet"] = hamlet_part()
            P = cache["hamlet"]
        else:
            if v["key"] not in cache:
                cache[v["key"]] = key_part(v["key"])
            P = cache[v["key"]]
        if v.get("cut_y") or v.get("drop"):
            P = copy.copy(P)
            if v.get("cut_y"):
                P.solids = [s for s in P.solids if s.bbox()[2] < v["cut_y"]]
            if v.get("drop") == "roof":
                P.solids = [s for s in P.solids if s.tag not in ROOF_TAGS and not s.tag.startswith("roof_geo")]
        g["part_mesh"](P, "bld", lod=v.get("lod", 1), open_doors=v.get("open", 0.0))
        bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.003))
        bpy.context.active_object.data.materials.append(gm)
        if "cam" in v:
            if v.get("scene") == "hamlet":
                for hx, hz in ((0.0, -20.0), (-12.0, 4.0)):
                    g["human"](hx, hz, 0.0)
            c = Vector(g["to_b"](v["cam"]))
            t = Vector(g["to_b"](v["look"]))
            cam.location = c
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
            cam.data.type = "PERSP"
            cam.data.lens = v["lens"]
            cam.data.clip_start = 0.05
            cam.data.clip_end = 500
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
    dst = os.path.join(SHEETS, "c2_%s.jpg" % name)
    im.save(dst, quality=86)
    print("sheet", dst, im.size)


def compose_all(sets):
    import glob
    fails = nck = 0
    for fam in ("farmhouse", "hut", "shed"):
        for p in glob.glob(os.path.join(DEV, "buildings", fam, "checks", "*.json")):
            c = json.load(open(p, encoding="utf-8"))
            nck += c.get("checks_n", 0)
            fails += c.get("failures", 0)
    sub = "C2 rural shells, %d checks %s (buildings/farmhouse|hut|shed/checks/*.json). Dark figure = 1.8 m." % (
        nck, "all pass" if not fails else "%d FAILURES" % fails)
    if "family" in sets:
        compose("family", family_jobs(), "C2 rural shells: Kanto + Kinai farmhouses, huts east + west, sheds (bare)",
                sub, 5, 480, 360, 22, 52)
    if "hamlet" in sets:
        compose("hamlet", hamlet_jobs(), "C2 hamlet on the test island (west of the yard)", sub, 2, 800, 600, 24, 90)
    if "interior" in sets:
        compose("interior", INTERIOR, "C2 interiors: sooted koyagumi, irori pits, doma, stalls", sub, 3, 640, 480, 76,
                80)


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
                                       stderr=subprocess.STDOUT), lf, len(part)))
    for p, lf, n in procs:
        p.wait()
        lf.close()


def main(argv):
    jobs_n = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 6
    if "preview" in argv:
        keys = argv[argv.index("--keys") + 1].split(",")
        jobs = [("pv_" + k, k, {"key": k, "view": "3q", "fit": 1.0, "res": [800, 600]}) for k in keys]
        run_jobs(jobs, min(jobs_n, len(jobs)))
        return 0
    sets = [a for a in argv if a in SETS] or list(SETS)
    if "--compose" not in argv:
        run_jobs([j for s in sets for j in SETS[s]()], jobs_n)
    compose_all(sets)
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        spec = json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8"))
        blender_main(spec)
    else:
        sys.exit(main(sys.argv[1:]))
