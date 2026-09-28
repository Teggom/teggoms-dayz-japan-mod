#!/usr/bin/env python3
r"""Render sheet for Land_JP_Machiya_T3_01.

  python render_machiya.py            (drives Blender in the background, then composes the sheet)
  python render_machiya.py --compose  (only recompose from existing PNGs)

Blender side: the parts kit's render helpers (parts/kit/render_parts.py: library textures at the building's wear,
1.8 m figure, Standard view transform) on the building from machiya_t3_01.model(). Outputs:
  renders/*.png, machiya_t3_01_sheet.jpg
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

# (out, caption, view spec)
JOBS = [
    ("street", "Street front (south face when placed): hikichigai plank entrance (both leaves stack right, main entrance "
     "only), sliding-shoji street window behind its koshi, two degoshi bays with their head boards closed to the wall, "
     "tiled street pent between udatsu, low plastered upper storey with oval mushiko.",
     {"view": "front", "scale": 11.5, "target": [0.0, 3.2, 4.6]}),
    ("q_front_right", "3/4 from the street, rooms side: the zashiki amado window (two storm shutters, tobukuro box "
     "beside it), board wainscot, tile gable whose board band now stops under the roof line (G3 C12 fix).",
     {"view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26}),
    ("q_front_left", "3/4 from the street, toriniwa side: gable pent at the upper-floor line, dark vertical boards with "
     "their new top rail (closes the slit Stephen saw through), entrance bay, rear lean-to.",
     {"view": "3q_left", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26}),
    ("back", "Back (yard side): single plank back door beside its fixed panel, renji kitchen window with a sliding board "
     "shutter inside, storage wall; lean-to eave with clay bed, fascia and eave tiles (G3 tile seating).",
     {"view": "back", "persp": 30, "target": [0.0, 2.4, 0.0], "dist": 26}),
    ("plan", "Plan cut at 1.3 m, doors CLOSED. Toriniwa with two stepping stones (re-centred on the narrow single "
     "shoji doors), mise and zashiki (9 mats each), kitchen with kamado, storage. North is down.",
     {"view": "top", "scale": 12.5, "cut_y": 1.3, "no_human": True}),
    ("plan_open", "Plan cut, everything OPEN. Door styles by use (PLAYBOOK §15): entrance hikichigai (1.48 m clear), "
     "mise/zashiki hikiwake (1.26), four narrow single doors (1.08). Every open leaf keeps 0.22 m in its opening, "
     "like vanilla, so it can be closed from both sides.",
     {"view": "top", "scale": 12.5, "cut_y": 1.3, "no_human": True, "open": 1.0}),
    ("section", "Long section (cut 1.4 m in from the east wall, looking west): raised tatami rooms, sealed low loft, "
     "kirizuma main roof and lean-to, both on a clay bed with fascia boards at the eaves.",
     {"view": "side", "scale": 12.5, "cut_x": 0.5, "target": [0.0, 3.0, 0.0]}),
    ("doors_closed", "Entrance closed: two ~0.88 m leaves in the 1-ken bay.",
     {"view": "3q", "persp": 35, "target": [-2.6, 1.3, 4.6], "dist": 9}),
    ("doors_open", "Entrance open (one action): both leaves stacked to the right, their edges still 0.22 m inside the "
     "opening - the part you aim at to close it from inside (G3 fix; 1.48 m clear).",
     {"view": "3q", "persp": 35, "target": [-2.6, 1.3, 4.6], "dist": 9, "open": 1.0}),
    ("interior_toriniwa", "Inside the toriniwa (interior clay walls, warmer and unweathered): the two narrow single "
     "shoji doors open, their leaf edges in the openings; kamado beyond.",
     {"interior": {"cam": [-2.75, 1.55, 3.9], "look": [-2.3, 1.2, -3.5], "lens": 20}, "open": 1.0}),
    ("interior_mise", "Inside the mise: the degoshi head boards now meet the wall's head rail (no daylight above the "
     "lattice, C11), the street window's shoji panel open, the hikiwake pair to the zashiki open.",
     {"interior": {"cam": [3.2, 1.9, 2.1], "look": [-1.5, 1.4, 4.3], "lens": 18}, "open": 1.0}),
    ("interior_zashiki", "Inside the zashiki: the amado window open (shutter edges left in the opening so it closes "
     "from inside), interior clay walls, the hikiwake pair to the mise.",
     {"interior": {"cam": [-1.3, 2.05, 1.5], "look": [3.6, 1.45, -0.2], "lens": 18}, "open": 1.0}),
    ("interior_kitchen", "Kitchen: kamado in interior clay, single plank door to the storage (open, leaf edge in the "
     "opening), the renji window's board shutter.",
     {"interior": {"cam": [-0.4, 1.6, -4.1], "look": [-3.3, 0.8, -2.0], "lens": 18}, "open": 1.0}),
    ("eave_closeup", "Eave corner up close (Stephen's 'tiles not on the roof'): eave tiles now sit on a clay bed "
     "(fuki-tsuchi) over the sheathing, their lips hang in front of a fascia board; verge tiles over the bargeboard.",
     {"interior": {"cam": [6.6, 3.7, 7.6], "look": [4.0, 4.45, 5.45], "lens": 34}}),
    ("gable_side", "Gable end from the side: the board band and its rail are clipped under the roof line (they poked "
     "through the roof at both eave corners and popped with distance - C12).",
     {"interior": {"cam": [9.5, 4.6, 5.5], "look": [3.64, 4.9, 1.0], "lens": 28}}),
    ("windows_open", "Back right, everything open: the storage tsukiage shutter pushed up and out (rotation, engine-"
     "untested), the zashiki amado stowed in its tobukuro, back door open.",
     {"interior": {"cam": [7.6, 2.2, -5.6], "look": [3.4, 1.7, -1.3], "lens": 20}, "open": 1.0}),
    ("lod2", "Resolution 2 (LOD1): matte far kawara material, full ridge stack, onigawara.",
     {"view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26, "lod": 2}),
    ("lod3", "Resolution 3 (LOD2): one far-material plane per slope, ridge stack, onigawara and verge strips kept "
     "(stable silhouette, C15).", {"view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26, "lod": 3}),
]


# ================================================================================================ Blender side
def blender_main(spec):
    import math
    import bpy
    from mathutils import Vector, Euler
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    sys.path.insert(0, KIT)
    exec(compile(src, "render_parts.py", "exec"), g)
    sys.path.insert(0, HERE)
    import machiya_t3_01 as MT
    M, floors, rooms = MT.model()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"](RES)
    gm = g["plain"]("ground", (0.36, 0.37, 0.33))
    os.makedirs(OUT, exist_ok=True)
    for out, cap, v in spec:
        g["clear_objects"]()
        P = M
        if v.get("cut_y") or v.get("cut_x") is not None:
            import copy
            P = copy.copy(M)
            if v.get("cut_y"):
                P.solids = [s for s in M.solids if s.bbox()[2] < v["cut_y"]]
            else:
                P.solids = [s for s in M.solids if (s.bbox()[0] + s.bbox()[1]) / 2 < v["cut_x"]]
        g["part_mesh"](P, "bld", lod=v.get("lod", 1), open_doors=v.get("open", 0.0))
        if not v.get("no_human") and not v.get("interior"):
            ha = v.get("human_at", [-1.0, 6.2])
            g["human"](ha[0], ha[1], v.get("human_y", 0.0))
        bpy.ops.mesh.primitive_plane_add(size=120, location=(0, 0, -0.003))
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
            sc = bpy.context.scene
            lamp = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "POINT"))
            lamp.data.energy = 900
            lamp.location = c + Vector((0, 0, 0.3))
            sc.collection.objects.link(lamp)
        elif v["view"] == "top":
            tb = Vector(g["to_b"]((0.0, 20.0, 0.0)))
            cam.location = tb
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
        for ob in list(bpy.data.objects):
            if ob.type == "LIGHT" and ob.name.startswith("fill"):
                bpy.data.objects.remove(ob, do_unlink=True)
        print("rendered", out)


# ================================================================================================ driver
def compose():
    from PIL import Image, ImageDraw, ImageFont
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 34),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 17),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 17)}.items()}
    import textwrap
    cw, ch = 640, 480
    cols = 3
    cap = 92
    rows = (len(JOBS) + cols - 1) // cols
    Wd = cols * cw + (cols + 1) * 10
    Hd = 110 + rows * (ch + cap + 10) + 10
    im = Image.new("RGB", (Wd, Hd), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((14, 12), "Land_JP_Machiya_T3_01 - tier-3 town machiya (Ioka type), from the parts library", font=F["h1"],
           fill=(20, 20, 20))
    chk = os.path.join(HERE, "checks.json")
    line = ""
    if os.path.isfile(chk):
        c = json.load(open(chk, encoding="utf-8"))
        n = len(c["checks"])
        ok = sum(1 for x in c["checks"] if x["ok"])
        line = "Checks: %d/%d pass (checks.json). Faces R1/R2/R3 = %s. " % (ok, n, c.get("faces", ""))
    d.text((14, 58), line + "Resolution-1 LOD with the jp_common textures (_w1) unless noted; dark figure = 1.8 m.",
           font=F["s"], fill=(60, 60, 60))
    d.text((14, 80), "G3 fix pass 2026-09-27: 4 x 3 ken omoya + 4 x 2 ken lean-to; 6 doors (hikichigai, hikiwake, 4 "
           "single) + 4 openable windows; model front = +z (placed at yaw 180 facing south, centre (1024, 1045)).",
           font=F["s"], fill=(60, 60, 60))
    for i, (out, caption, v) in enumerate(JOBS):
        x = 10 + (i % cols) * (cw + 10)
        y = 110 + (i // cols) * (ch + cap + 10)
        p = os.path.join(OUT, out + ".png")
        if os.path.isfile(p):
            im.paste(Image.open(p).convert("RGB").resize((cw, ch)), (x, y))
        d.rectangle([x, y + ch, x + cw, y + ch + cap], fill=(250, 249, 246))
        d.text((x + 6, y + ch + 4), out, font=F["b"], fill=(20, 20, 20))
        yy = y + ch + 25
        for ln in textwrap.wrap(caption, 78)[:4]:
            d.text((x + 6, yy), ln, font=F["s"], fill=(50, 50, 50))
            yy += 16
    dst = os.path.join(HERE, "machiya_t3_01_sheet.jpg")
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
