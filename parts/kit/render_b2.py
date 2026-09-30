#!/usr/bin/env python3
r"""Render sheets for B2's test assemblies and building views (cutaways, interiors, rows), in the contact-sheet style.

  python render_b2.py <sheet> [--compose]

A job builds a Part (a b2_assembly builder, a registry part, or a python callable 'module:function' returning a Part
or (Part, ...)), optionally hides roof covering solids (cut: keep the koyagumi / given tags, drop the rest of the roof
over a plan half-space or above a height) and renders it with parts/kit/render_parts.py's helpers.
Sheets -> parts/contact_sheets/<sheet>.jpg; PNGs -> parts/_render/<sheet>/.
"""
import importlib
import json
import os
import subprocess
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
RENDER = os.path.join(DEV, "parts", "_render")
SHEETS = os.path.join(DEV, "parts", "contact_sheets")
RES = (960, 720)

COVER = ("thatch_body", "thatch_band", "lath", "rafter", "hip_roll", "thatch_ridge", "ridge_bamboo", "binding",
         "sheathing", "tile_bed", "kawara_field", "kawara_far", "eave_tile", "kawara_fascia", "verge", "noshi", "cap",
         "ridge", "ridge_end", "onigawara", "hafu", "purlin_end", "hongawara", "board_field", "board_field_lod",
         "eave_stack", "board_ridge", "ridge_batten", "roof_geo_front", "roof_geo_back", "roof_geo_left",
         "roof_geo_right", "mortar", "ganburi", "noshi_far", "ridge_far", "eave_far", "field_far", "tile", "kawara")

SHEETS_DEF = {
    "9a_koyagumi_assembly": (
        "B2 koyagumi test assemblies: thatch over koyagumi on posts (joya / geya), sooted, hut, tile wagoya", [
            ("farm_ext", "Kanto-type farmhouse test frame, 7 x 5 ken yosemune thatch on adzed posts and soseki "
             "(koya_farmhouse). The whole roof as built.",
             {"build": "b2:koya_farmhouse", "view": "3q", "persp": 30, "target": [6.4, 3.5, -4.5], "dist": 34}),
            ("farm_cut", "The same with the front half of the thatch cut away: joya posts on the aisle lines, cambered "
             "ushibari, sasu pairs crossed at the ridge, round purlins, hip and end sasu; geya aisle beams from the "
             "low outer walls into the joya posts. ONE sweeping slope over both.",
             {"build": "b2:koya_farmhouse", "cut": {"z_gt": -4.55}, "view": "3q", "persp": 30,
              "target": [6.4, 3.5, -4.5], "dist": 30}),
            ("farm_section", "Section at the middle frame line (front view, roof in front of x 6.4 hidden): outer "
             "wall 2.88, geya 1 ken each side, joya 3 ken, beam 4.52, ridge 7.4.",
             {"build": "b2:koya_farmhouse", "cut": {"x_lt": 6.30, "x_gt": 6.45}, "view": "side_l", "scale": 12.5,
              "target": [6.4, 3.8, -4.55]}),
            ("farm_in", "Inside, from the doma under the front aisle, looking up into the joya: the frame reads as "
             "big log beams and poles under the bamboo lath (_w1).",
             {"build": "b2:koya_farmhouse", "interior": {"cam": [2.6, 1.6, -0.9], "look": [7.5, 5.2, -5.5],
                                                          "lens": 16}}),
            ("farm_in_soot", "The same view, SOOTED wear level (koyagumi soot=True + soot_roof): smoke-black beams, "
             "rafters, lath and thatch underside (W5).",
             {"build": "b2:koya_farm_soot", "interior": {"cam": [2.6, 1.6, -0.9], "look": [7.5, 5.2, -5.5],
                                                          "lens": 16}}),
            ("hut_in", "Poor hut 3 x 2 ken (koya_hut, sooted): sasu on log tie beams, lashed crossing, ridge pole; "
             "thatch gable walls. 'No ceiling, open to soot-black thatch'.",
             {"build": "b2:koya_hut", "interior": {"cam": [0.6, 1.6, -0.4], "look": [4.2, 3.6, -2.4], "lens": 14}}),
            ("hut_cut", "The hut with the front slope cut away.",
             {"build": "b2:koya_hut", "cut": {"z_gt": -1.82}, "view": "3q", "persp": 30, "target": [2.7, 2.6, -1.8],
              "dist": 16}),
            ("shop_cut", "Tile workshop 4 x 3 ken (koya_workshop): WAGOYA, sawn tie beams on the posts, struts, "
             "purlins every half ken, ridge beam, koyanuki, rafters continued to the ridge; tile gables.",
             {"build": "b2:koya_workshop", "cut": {"z_gt": -2.73}, "view": "3q", "persp": 30,
              "target": [3.6, 2.8, -2.7], "dist": 19}),
            ("hip_cut", "Hipped tile roof (koya_hip), covering above 3.05 m cut away: hip rafters (sumigi), end "
             "purlins on struts on the end beams (tsunagi), jack rafters to the hips, the ridge beam on its strut.",
             {"build": "b2:koya_hip", "cut": {"y_gt": 3.05}, "view": "3q", "persp": 30,
              "target": [3.6, 2.8, -2.7], "dist": 19}),
        ]),
    "9d_stair_toilet_stall": (
        "B2 stair, toilet half door and ox stall: offline test assemblies", [
            ("hatago_stair", "Box stair (kaidan-dansu look, drawers in its side) between the raised lower floor (0.50) "
             "and a walkable upper floor (3.30) of a 3 x 2 ken post frame: 37.6 deg walk ramp, 1.20 wide, 2 ken run.",
             {"build": "b2:stair_hatago", "view": "3q", "persp": 30, "target": [2.7, 2.0, -1.8], "dist": 15,
              "human": [4.8, -2.4, 0.5]}),
            ("hatago_well", "The upper floor's stairwell from above: the 'stair' hole cut by floors.boards(holes=...), "
             "rim boards and a guard rail on the two open sides (the wall side and the arrival end stay open).",
             {"build": "b2:stair_hatago", "view": "3q_left", "persp": 30, "target": [2.7, 3.3, -1.5], "dist": 11}),
            ("hatago_up", "Walking up: head room over the flight >= 2.05 (the well starts where the upper floor would "
             "come closer; ST3).",
             {"build": "b2:stair_hatago", "interior": {"cam": [0.15, 2.1, -0.65], "look": [4.4, 3.8, -0.65],
                                                        "lens": 18}}),
            ("kura_stair", "Open stair (stringers, treads, no risers) to a kura-type loft 2.40 up: 37.0 deg, 1.10 wide.",
             {"build": "b2:stair_kura", "view": "3q", "persp": 30, "target": [2.2, 1.6, -1.8], "dist": 13}),
            ("toilet_out", "Walk-in toilet 1 x 1.5 ken (G1 A1-1): board walls, itabuki roof, the half door (rotation, "
             "swings out; shown 60 % open), fixed board panel beside it. Doorway 1.04 x 2.00 (D1).",
             {"build": "b2:toilet", "view": "3q", "persp": 30, "target": [0.9, 1.3, -1.0], "dist": 9, "open": 0.6,
              "human": [2.6, 0.9, 0.0]}),
            ("toilet_in", "Inside the toilet: board floor with the drop slot over a closed pit (a floors 'pit' hole), "
             "the half door closed, the open top of the doorway above it.",
             {"build": "b2:toilet", "interior": {"cam": [0.95, 1.55, -2.4], "look": [0.9, 0.9, 0.2], "lens": 16}}),
            ("stall", "Ox stall (jp_p_frame_stall _ox) in a doma corner (DW07): board partitions, bars down as left "
             "(one on the floor, one leaning), manger with fodder, tether ring, straw bedding.",
             {"build": "b2:stall_doma", "view": "3q", "persp": 30, "target": [1.0, 1.0, -1.4], "dist": 9,
              "human": [3.0, 0.8, 0.05]}),
        ]),
}


KOYA = ("hari", "ushibari", "geya_bari", "tsuka", "munazuka", "moya", "munagi", "koyanuki", "sumigi", "tsunagi",
        "rafter_in", "sasu", "sumi_sasu", "tsuma_sasu", "lashing", "joya_plate", "joya_post")


def get_part(spec):
    sys.path.insert(0, HERE)
    kind, what = spec.split(":", 1)
    if kind == "b2":
        import b2_assembly
        a, _ = b2_assembly.ASSEMBLIES[what]()
        return a
    if kind == "part":
        from jpparts import registry
        p, v, fn = next(r for r in registry.ALL if r[0] + r[1] == what)
        return fn(v)
    mod, fn = what.split(".")
    r = getattr(importlib.import_module(mod), fn)()
    return r[0] if isinstance(r, tuple) else r


def apply_cut(P, cut):
    import copy
    keep_tags = set(cut.get("keep", ()))
    out = copy.copy(P)

    def hide(s):
        if s.tag in keep_tags:
            return False
        if cut.get("any"):
            pass
        elif cut.get("srcs") is not None:
            if getattr(s, "src", None) not in cut["srcs"]:
                return False
        elif not (getattr(s, "src", None) == "roof" and s.tag not in KOYA):
            return False
        b = s.bbox()
        cx, cy, cz = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2
        if "z_gt" in cut and cz > cut["z_gt"]:
            return True
        if "z_lt" in cut and cz < cut["z_lt"]:
            return True
        if "x_lt" in cut and cx < cut["x_lt"]:
            return True
        if "x_gt" in cut and cx > cut["x_gt"]:
            return True
        if "y_gt" in cut and cy > cut["y_gt"]:
            return True
        return False
    out.solids = [s for s in P.solids if not hide(s)]
    return out


# ================================================================================================ Blender side
def blender_main(spec):
    import bpy
    from mathutils import Vector, Euler
    src = open(os.path.join(HERE, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(HERE, "render_parts.py")}
    sys.path.insert(0, HERE)
    exec(compile(src, "render_parts.py", "exec"), g)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"](tuple(spec.get("res", RES)))
    gm = g["plain"]("ground", (0.36, 0.37, 0.33))
    os.makedirs(spec["out_dir"], exist_ok=True)
    cache = {}
    for out, cap, v in spec["jobs"]:
        g["clear_objects"]()
        if v["build"] not in cache:
            cache[v["build"]] = get_part(v["build"])
        P = cache[v["build"]]
        if v.get("cut"):
            P = apply_cut(P, v["cut"])
        if v.get("move"):
            P = P.transformed(0.0, tuple(v["move"]))
        g["part_mesh"](P, "bld", lod=v.get("lod", 1), open_doors=v.get("open", 0.0))
        if v.get("human"):
            g["human"](*v["human"])
        bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.003))
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
            cam.data.clip_end = 300
        elif v["view"] == "side_l":
            tg = Vector(g["to_b"](v["target"]))
            cam.location = tg + Vector((-40.0, 0.0, 0.0))
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (tg - cam.location).to_track_quat("-Z", "Y")
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = v["scale"]
            cam.data.clip_start = 0.1
            cam.data.clip_end = 300
        elif v["view"] == "top":
            tg = g["to_b"](v["target"])
            cam.location = Vector((tg[0], tg[1], 30.0))
            cam.rotation_mode = "XYZ"
            cam.rotation_euler = Euler((0.0, 0.0, 0.0))
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = v["scale"]
        elif v.get("persp"):
            g["look"](cam, g["to_b"](v["target"]), v["view"], 10, dist=v.get("dist", 25), lens=v["persp"] * 1.4)
        else:
            g["look"](cam, g["to_b"](v["target"]), v["view"], v["scale"])
        bpy.context.scene.render.filepath = os.path.join(spec["out_dir"], out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)


# ================================================================================================ driver
def compose(sheet, title, jobs, note=""):
    from PIL import Image, ImageDraw, ImageFont
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 30),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 17),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 17)}.items()}
    cw, ch, cols, cap = 640, 480, 3, 92
    rows = (len(jobs) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw + (cols + 1) * 10, 90 + rows * (ch + cap + 10) + 10), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((14, 12), title, font=F["h1"], fill=(20, 20, 20))
    if note:
        d.text((14, 56), note[:230], font=F["s"], fill=(60, 60, 60))
    for i, (out, caption, v) in enumerate(jobs):
        x = 10 + (i % cols) * (cw + 10)
        y = 90 + (i // cols) * (ch + cap + 10)
        p = os.path.join(RENDER, sheet, out + ".png")
        if os.path.isfile(p):
            im.paste(Image.open(p).convert("RGB").resize((cw, ch)), (x, y))
        d.rectangle([x, y + ch, x + cw, y + ch + cap], fill=(250, 249, 246))
        d.text((x + 6, y + ch + 4), out, font=F["b"], fill=(20, 20, 20))
        yy = y + ch + 25
        for ln in textwrap.wrap(caption, 78)[:4]:
            d.text((x + 6, yy), ln, font=F["s"], fill=(50, 50, 50))
            yy += 16
    os.makedirs(SHEETS, exist_ok=True)
    dst = os.path.join(SHEETS, sheet + ".jpg")
    im.save(dst, quality=88)
    print("sheet", dst, im.size)
    return dst


def notes_for(sheet):
    jp = os.path.join(DEV, "parts", "b2_assembly_checks.json")
    if not os.path.isfile(jp):
        return ""
    res = json.load(open(jp, encoding="utf-8"))
    parts = []
    for nm, r in sorted(res.items()):
        cs = r["checks"]
        parts.append("%s %d/%d" % (nm, sum(1 for c in cs if c["ok"]), len(cs)))
    return "Checks (parts/b2_assembly_checks.json): " + ", ".join(parts)


def main(argv):
    sheet = argv[0]
    title, jobs = SHEETS_DEF[sheet]
    only = [a for a in argv[1:] if not a.startswith("--")]
    if "--compose" not in argv:
        todo = [j for j in jobs if not only or j[0] in only]
        jf = os.path.join(RENDER, sheet + "_jobs.json")
        os.makedirs(RENDER, exist_ok=True)
        with open(jf, "wb") as f:
            f.write(json.dumps({"out_dir": os.path.join(RENDER, sheet), "res": list(RES), "jobs": todo},
                               indent=1).encode("utf-8"))
        r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__), "--",
                            "--blender", jf], capture_output=True, text=True, errors="replace")
        done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
        print("%d/%d rendered" % (len(done), len(todo)))
        if len(done) < len(todo):
            print((r.stdout + r.stderr)[-4000:])
    compose(sheet, title, jobs, notes_for(sheet))


if __name__ == "__main__":
    if "--blender" in sys.argv:
        blender_main(json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8")))
    else:
        main(sys.argv[1:])
