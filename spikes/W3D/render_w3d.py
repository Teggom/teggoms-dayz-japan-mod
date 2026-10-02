#!/usr/bin/env python3
r"""W3D render sheets (copied from spikes/W3C2/render_w3c2.py) (Blender in the background; parts/kit/render_parts.py helpers, as spikes/C2/render_c2.py).

  python spikes/W3C1/render_w3c1.py family [--jobs N] [--compose]
  python spikes/W3C1/render_w3c1.py preview --keys k1,k2 [--view 3q|back|top|front|3q_left] [--cut Y] [--drop roof]
  python spikes/W3C1/render_w3c1.py try --kind teahouse --params '{"size": "shop"}' [--view ...] [--name out]

Sheet: research/production/contact_sheets/w3d_family.jpg (every W3D shell + compounds + the tower and props).
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
FAMS = ("gv_hall", "gv_site")
ROOF_TAGS = ("thatch_body", "thatch_band", "lath", "rafter", "hip_roll", "thatch_ridge", "ridge_bamboo", "binding",
             "umanori", "umanori_pole", "turf", "iris", "sheathing", "board_field", "board_field_lod", "eave_stack",
             "kawara_field", "hafu", "verge_batten", "board_ridge", "ridge_batten", "ridge_stone", "stone", "batten",
             "thatch_roll", "noshi", "cap", "noshi_far", "eave_tile", "tile_bed", "fascia", "bed", "flashing",
             "lashing_rope", "stone_layer_lod", "ridge_stone_lod", "roof_stone", "vent_roof", "louvre")


# the kasane-gura as placed: the mae-gura (front, south) and the o-kura behind it, both facing the yard (+z)
_DZ = 3 * 1.82 / 2 + 0.12 + 0.20 + 0.12 + 4 * 1.82 / 2
PAIR = [["okura", {}, 0.0, -_DZ, 0.0], ["maegura", {}, 0.0, 0.0, 0.0]]


def family_jobs():
    import registry
    jobs = []
    for b in registry.BUILDINGS:
        if b.get("dir") not in FAMS:
            continue
        cap = b["class"].replace("Land_JP_", "")
        jobs.append(("fam_" + b["key"], cap, {"key": b["key"], "view": "3q", "fit": 1.0, "res": [480, 360]}))
    jobs.append(("fam_gv_nagayamon_jinya", "NagayaMon_Jinya", {"key": "gv_nagayamon_jinya", "view": "3q", "fit": 1.0,
                                                             "res": [480, 360]}))
    jobs.append(("fam_gv_roya_back", "Roya (back: barred windows)", {"key": "gv_roya", "view": "back", "fit": 1.0,
                                                                     "res": [480, 360]}))
    for (pid, cap) in (("hinomi_yagura", "S_Hinomi_Yagura (tower)"), ("mitsudogu_tate", "f_mitsudogu_tate"),
                       ("mitsudogu_tate_ab", "f_mitsudogu_tate_ab"), ("kanme_hakari", "f_kanme_hakari"),
                       ("kanme_hakari_ab", "f_kanme_hakari_ab"), ("matoi_nobori", "f_matoi_nobori"),
                       ("matoi_nobori_fallen", "f_matoi_nobori_fallen")):
        jobs.append(("fam_p_" + pid, cap, {"prop": pid, "view": "3q", "fit": 1.0, "res": [480, 360]}))
    return jobs


def key_part(v):
    if "multi" in v:
        # several shells / keys merged at offsets (the kasane-gura pair): [[key_or_kind, params, x, z, yaw], ...]
        out = None
        for (k, pr, x, z, yaw) in v["multi"]:
            sub = key_part({"key": k} if pr is None else {"kind": k, "params": pr})
            sub = sub.transformed(yaw, (x, 0.0, z))
            if out is None:
                out = sub
            else:
                out.solids += sub.solids
        return out
    if "prop" in v:                      # W3D: a prop / site object (the tower and the govfit props)
        for p in (os.path.join(DEV, "spikes", "W3D"), os.path.join(DEV, "spikes", "L2"), os.path.join(DEV, "spikes", "L1"),
                  os.path.join(DEV, "spikes", "B3b"), os.path.join(DEV, "spikes", "B3a")):
            if p not in sys.path:
                sys.path.insert(0, p)
        pid = v["prop"]
        if pid == "hinomi_yagura":
            import props_w3d_site as PS
            P = PS.hinomi_yagura()
        else:
            import props_w3d as PW
            fn = {"mitsudogu_tate": lambda: PW.mitsudogu_tate(), "mitsudogu_tate_ab": lambda: PW.mitsudogu_tate(True),
                  "kanme_hakari": lambda: PW.kanme_hakari(), "kanme_hakari_ab": lambda: PW.kanme_hakari(True),
                  "matoi_nobori": lambda: PW.matoi_nobori(), "matoi_nobori_fallen": lambda: PW.matoi_nobori(True)}[pid]
            P = fn()
        from jpparts.core import Part
        out = Part("prop_" + pid, "", "")
        out.solids = [s_ for s_ in P.solids if 1 in s_.vis]
        return out
    if "key" in v:
        import registry
        import furnishkit
        b = registry.get(v["key"])
        mod = furnishkit._base_module(b)
        M, _, _ = mod.model(name=b.get("recipe_name", b["name"]), **b["params"])
    else:
        import govsitekit as dwellingkit
        M, _, _ = dwellingkit.model(kind=v["kind"], **v["params"])
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
    for out, cap, v in spec:
        res = v.get("res", [960, 720])
        bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = res
        g["clear_objects"]()
        P = key_part(v)
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
    dst = os.path.join(SHEETS, "w3d_%s.jpg" % name)
    im.save(dst, quality=86)
    print("sheet", dst, im.size)


def compose_family():
    import glob
    fails = nck = 0
    for fam in FAMS:
        for p in glob.glob(os.path.join(DEV, "buildings", fam, "checks", "*.json")):
            c = json.load(open(p, encoding="utf-8"))
            nck += c.get("checks_n", 0)
            fails += c.get("failures", 0)
    sub = ("W3D government shells (bare) + compounds + the tower and props, %d checks %s (buildings/gv_*/checks/*.json). "
           "Dark figure = 1.8 m; a 3/4 front view each." % (nck, "all pass" if not fails else
                                                                              "%d FAILURES" % fails))
    compose("family", family_jobs(), "W3D: wave 3d government (checkpoint, post-station office, jinya, jail, fire brigade)",
            sub, 6, 480, 360, 22, 52)


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


def _opt(argv, k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d


def main(argv):
    jobs_n = min(4, int(_opt(argv, "--jobs", 4)))
    extra = {}
    if "--cut" in argv:
        extra["cut_y"] = float(_opt(argv, "--cut"))
    if "--drop" in argv:
        extra["drop"] = _opt(argv, "--drop")
    if "--open" in argv:
        extra["open"] = 1.0
    view = _opt(argv, "--view", "3q")
    if "preview" in argv:
        keys = _opt(argv, "--keys").split(",")
        jobs = [("pv_%s_%s" % (k, view), k, dict({"key": k, "view": view, "fit": 1.0, "res": [800, 600]}, **extra))
                for k in keys]
        run_jobs(jobs, min(jobs_n, len(jobs)))
        return 0
    if "pair" in argv:
        jobs = [("pair_%s" % vw, "pair", dict({"multi": PAIR, "view": vw, "fit": 1.0, "res": [960, 720]}, **extra))
                for vw in view.split(",")]
        run_jobs(jobs, min(jobs_n, len(jobs)))
        return 0
    if "try" in argv:
        views = view.split(",")
        nm = _opt(argv, "--name", "try")
        kinds = _opt(argv, "--kind").split(";")
        pars = _opt(argv, "--params", "{}").split(";")
        jobs = []
        for i, kd in enumerate(kinds):
            pr = json.loads(pars[i] if i < len(pars) else "{}")
            nmi = nm if len(kinds) == 1 else "%s%d" % (nm, i)
            jobs += [("tr_%s_%s" % (nmi, vw), nmi, dict({"kind": kd, "params": pr, "view": vw, "fit": 1.0,
                                                        "res": [800, 600]}, **extra)) for vw in views]
        run_jobs(jobs, min(jobs_n, len(jobs)))
        return 0
    if "--compose" not in argv:
        run_jobs(family_jobs(), jobs_n)
    compose_family()
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        spec = json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8"))
        blender_main(spec)
    else:
        sys.exit(main(sys.argv[1:]))
