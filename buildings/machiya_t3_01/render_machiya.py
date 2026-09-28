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
    ("street", "Street front (south face when placed): twin plank entrance leaves in the toriniwa bay, plain park bay, "
     "half-ken koshi window, two degoshi bays (shop front), tiled street pent between plastered udatsu, low plastered "
     "upper storey with three oval mushiko, 5-course ridge with onigawara.",
     {"view": "front", "scale": 11.5, "target": [0.0, 3.2, 4.6]}),
    ("q_front_right", "3/4 from the street, west corner (rooms side): zashiki koshi window, board wainscot over the "
     "grime band, shinkabe upper wall, tile gable with bosses and bargeboard, dodai on separate dressed stones.",
     {"view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26}),
    ("q_front_left", "3/4 from the street, east corner (toriniwa side): the gable pent at the upper-floor line (Ioka), "
     "dark vertical boards below, entrance bay with its twin plank leaves, rear lean-to behind.",
     {"view": "3q_left", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26}),
    ("back", "Back (yard side): geya lean-to with verge tiles and bargeboards, twin kitchen back door, renji kitchen "
     "window, storage wall; the main roof's back eave over the lean-to. Eave edge 2.53 m (the climb route to the roof).",
     {"view": "back", "persp": 30, "target": [0.0, 2.4, 0.0], "dist": 26}),
    ("plan", "Plan cut at 1.3 m, doors CLOSED. Left: toriniwa (doma) with two stepping stones; mise (shop, 9 mats) at "
     "the front, zashiki (9 mats) behind; geya: kitchen (doma, kamado) and storage (boards). North is down.",
     {"view": "top", "scale": 12.5, "cut_y": 1.3, "no_human": True}),
    ("plan_open", "Plan cut, every door OPEN (both leaves of each twin door stacked over the next half-ken): 1.70 m "
     "clear openings.", {"view": "top", "scale": 12.5, "cut_y": 1.3, "no_human": True, "open": 1.0}),
    ("section", "Long section through the rooms (cut at 1.4 m in from the east wall, looking west): raised tatami "
     "rooms (2.50 m ceilings), sealed low loft (no stair, no hatch), kirizuma main roof, geya lean-to over the doma.",
     {"view": "side", "scale": 12.5, "cut_x": 0.5, "target": [0.0, 3.0, 0.0]}),
    ("doors_closed", "Entrance closed: two ~0.88 m leaves in the 1-ken bay.",
     {"view": "3q", "persp": 35, "target": [-2.6, 1.3, 4.6], "dist": 9}),
    ("doors_open", "Entrance open (one action): both leaves stacked over the plain half-ken; 1.70 m clear.",
     {"view": "3q", "persp": 35, "target": [-2.6, 1.3, 4.6], "dist": 9, "open": 1.0}),
    ("interior_toriniwa", "Inside the toriniwa looking back to the kitchen: stepping stones and shoji into the rooms "
     "(open), joisted ceiling, kamado beyond.",
     {"interior": {"cam": [-2.75, 1.55, 3.9], "look": [-2.3, 1.2, -3.5], "lens": 20}, "open": 1.0}),
    ("interior_mise", "Inside the mise (shop): 9 tatami in a shugi layout, degoshi lattice with paper behind, the "
     "plastered partition with its twin shoji to the zashiki open.",
     {"interior": {"cam": [3.2, 1.9, 2.1], "look": [-1.5, 0.8, 4.3], "lens": 18}, "open": 1.0}),
    ("interior_kitchen", "Kitchen (geya): built-in kamado against the sooted boards, twin plank door to the storage, "
     "the omoya back wall rising into the lean-to.",
     {"interior": {"cam": [-0.4, 1.6, -4.1], "look": [-3.3, 0.8, -2.0], "lens": 18}, "open": 0.0}),
    ("lod2", "Resolution 2 (LOD1).", {"view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26, "lod": 2}),
    ("lod3", "Resolution 3 (LOD2).", {"view": "3q", "persp": 30, "target": [0.0, 2.6, 0.0], "dist": 26, "lod": 3}),
    ("roof_walk", "Rooftop: walkable tile slopes (Roadway), ridge walk strip; the lean-to leads up to the main roof.",
     {"view": "back", "persp": 35, "target": [0.0, 4.5, -3.0], "dist": 14, "human_at": [1.0, -2.45],
      "human_y": 3.73}),
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
    d.text((14, 80), "4 x 3 ken omoya (sealed low loft) + 4 x 2 ken rear lean-to; 6 twin sliding doors; model front = "
           "+z (placed at yaw 180 facing south, centre (1024, 1045)).", font=F["s"], fill=(60, 60, 60))
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
