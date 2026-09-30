#!/usr/bin/env python3
r"""Render sheet for the townhouse template test unit (B0 step 0c) and a snapped row of three units.

  python render_unit.py            (drives Blender in the background, then composes the sheet)
  python render_unit.py --compose  (only recompose from existing PNGs)

Blender side: the parts kit's render helpers (parts/kit/render_parts.py), as buildings/machiya_t3_01/render_machiya.py.
Outputs: renders/*.png, townhouse_unit_test_sheet.jpg
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
RES = (960, 720)
# units in +x order, i.e. listed from the street-view RIGHT to LEFT (the DayZ frame is left-handed); sides street-view
ROW = [dict(frontage=3, region="kamigata", position="end", free="right", tori="right"),
       dict(frontage=2, region="kamigata", position="middle", tori="left"),
       dict(frontage=4, region="kamigata", position="corner", free="left", tori="right")]
ROW_EDO = [dict(frontage=2, region="edo", position="end", free="right", tori="right"),
           dict(frontage=3, region="edo", position="middle", tori="right", covering="itabuki"),
           dict(frontage=2, region="edo", position="end", free="left", tori="left")]

JOBS = [
    ("street", "The test unit (Kamigata, 3 ken, END; free gable and toriniwa on the right): entrance, koshi window, "
     "one degoshi bay, street "
     "pent running to the party lot line on the left, udatsu on the free gable, mushiko upper front.",
     {"view": "front", "scale": 9.5, "target": [0.0, 3.2, 4.0]}),
    ("q_free", "3/4 from the street, free gable: board wall, Ioka gable pent, tile gable, lean-to kitchen behind.",
     {"view": "3q_left", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 22}),
    ("q_party", "3/4 from the street, PARTY side: PLACEHOLDERS (stone footing, plain clay wall, normal verge cut back "
     "to the lot line). B2's party wall / party roof end replace these.",
     {"view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 22}),
    ("back", "Back: single plank back door into the lean-to kitchen (1 ken deep, sangawara lean-to from leanto.roof).",
     {"view": "back", "persp": 30, "target": [0.0, 2.4, 0.0], "dist": 22}),
    ("plan", "Plan cut at 1.3 m: toriniwa (doma) + 2 single shoji doors, mise and oku (tatami, shugi), hikiwake "
     "pair between them, kitchen doma. North is down.",
     {"view": "top", "scale": 10.5, "cut_y": 1.3, "no_human": True}),
    ("row_street", "A snapped ROW (Kamigata), right to left: 3-ken end unit, 2-ken middle unit (toriniwa left), "
     "4-ken corner unit. "
     "Lot line to lot line; one udatsu per seam; the corner square between the street pent and the side pent is "
     "open (roof_corner placeholder).",
     {"row": "kamigata", "view": "front", "scale": 17.0, "target": [0.0, 3.2, 4.0]}),
    ("row_3q", "The Kamigata row from the corner end: wrapped side pent (placeholder corner), party seams.",
     {"row": "kamigata", "view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 30}),
    ("row_edo", "An Edo row: plastered nuriya fronts, board pents, board lean-tos; the middle unit has an itabuki main "
     "roof. No udatsu: the seams show (seam_cap placeholder) and the roof steps are open (party_roof_end).",
     {"row": "edo", "view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26}),
    ("seam_close", "Up close at a Kamigata party seam from the street: two end posts 8 mm apart, pents meeting at the "
     "lot line under the udatsu, verges cut back (placeholder gap between the roofs).",
     {"row": "kamigata", "interior": {"cam": [-1.5, 5.6, 7.0], "look": [-4.6, 4.3, 0.5], "lens": 30}}),
]


def row_part(specs):
    sys.path.insert(0, KIT)
    from jpparts.templates import townhouse
    from jpparts.core import Part
    units = [townhouse.model(name="row%d" % i, **p) for i, p in enumerate(specs)]
    total = sum(u[3]["lot_width"] for u in units)
    x = -total / 2
    R = Part("row", "", "")
    R.wear = "_w1"
    for (M, _, _, info) in units:
        cx = x + info["lot_width"] / 2
        R.merge(M.transformed(0.0, (cx, 0.0, 0.0)))
        x += info["lot_width"]
    return R


# ================================================================================================ Blender side
def blender_main(spec):
    import bpy
    from mathutils import Vector, Euler
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    sys.path.insert(0, KIT)
    exec(compile(src, "render_parts.py", "exec"), g)
    sys.path.insert(0, HERE)
    import townhouse_unit_test as TU
    M, floors, rooms = TU.model()
    rows = {"kamigata": row_part(ROW), "edo": row_part(ROW_EDO)}
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"](RES)
    gm = g["plain"]("ground", (0.36, 0.37, 0.33))
    os.makedirs(OUT, exist_ok=True)
    for out, cap, v in spec:
        g["clear_objects"]()
        P = rows[v["row"]] if v.get("row") else M
        if v.get("cut_y"):
            import copy
            P = copy.copy(P)
            P.solids = [s for s in P.solids if s.bbox()[2] < v["cut_y"]]
        g["part_mesh"](P, "bld", lod=v.get("lod", 1), open_doors=v.get("open", 0.0))
        if not v.get("no_human") and not v.get("interior"):
            g["human"](-1.0, 6.2, 0.0)
        bpy.ops.mesh.primitive_plane_add(size=160, location=(0, 0, -0.003))
        bpy.context.active_object.data.materials.append(gm)
        if v.get("interior"):
            it = v["interior"]
            c = Vector(g["to_b"](it["cam"]))
            t = Vector(g["to_b"](it["look"]))
            cam.location = c
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
            cam.data.type = "PERSP"
            cam.data.lens = it["lens"]
            cam.data.clip_start = 0.05
        elif v["view"] == "top":
            cam.location = Vector(g["to_b"]((0.0, 20.0, 0.0)))
            cam.rotation_mode = "XYZ"
            cam.rotation_euler = Euler((0.0, 0.0, 0.0))
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = v["scale"]
            cam.data.clip_start = 0.1
            cam.data.clip_end = 100
        elif v.get("persp"):
            g["look"](cam, g["to_b"](v["target"]), v["view"], 10, dist=v.get("dist", 25), lens=v["persp"] * 1.4)
        else:
            g["look"](cam, g["to_b"](v["target"]), v["view"], v["scale"])
        bpy.context.scene.render.filepath = os.path.join(OUT, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)


# ================================================================================================ driver
def compose():
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 30),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 17),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 17)}.items()}
    cw, ch, cols, cap = 640, 480, 3, 92
    rows = (len(JOBS) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw + (cols + 1) * 10, 90 + rows * (ch + cap + 10) + 10), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((14, 12), "Townhouse unit template (B0 step 0c) - test unit + snapped rows, PLACEHOLDERS at party / corner",
           font=F["h1"], fill=(20, 20, 20))
    chk = os.path.join(HERE, "checks.json")
    if os.path.isfile(chk):
        c = json.load(open(chk, encoding="utf-8"))
        d.text((14, 56), "Checks: %d/%d pass (checks.json). Faces R1/R2/R3 = %s. Dark figure = 1.8 m." % (
            sum(1 for x in c["checks"] if x["ok"]), len(c["checks"]), c.get("faces", "")), font=F["s"],
            fill=(60, 60, 60))
    for i, (out, caption, v) in enumerate(JOBS):
        x = 10 + (i % cols) * (cw + 10)
        y = 90 + (i // cols) * (ch + cap + 10)
        p = os.path.join(OUT, out + ".png")
        if os.path.isfile(p):
            im.paste(Image.open(p).convert("RGB").resize((cw, ch)), (x, y))
        d.rectangle([x, y + ch, x + cw, y + ch + cap], fill=(250, 249, 246))
        d.text((x + 6, y + ch + 4), out, font=F["b"], fill=(20, 20, 20))
        yy = y + ch + 25
        for ln in textwrap.wrap(caption, 78)[:4]:
            d.text((x + 6, yy), ln, font=F["s"], fill=(50, 50, 50))
            yy += 16
    dst = os.path.join(HERE, "townhouse_unit_test_sheet.jpg")
    im.save(dst, quality=88)
    print("sheet", dst, im.size)


def main(argv):
    if "--compose" not in argv:
        jf = os.path.join(OUT, "_jobs.json")
        os.makedirs(OUT, exist_ok=True)
        only = [a for a in argv if not a.startswith("--")]
        jobs = [j for j in JOBS if not only or j[0] in only]
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
