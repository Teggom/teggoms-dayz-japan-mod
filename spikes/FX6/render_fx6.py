#!/usr/bin/env python3
r"""FX6 renders (Blender in the background; parts/kit/render_parts.py helpers, the spikes/D3/render_d3.py pattern).

  python spikes/FX6/render_fx6.py gates|compounds|kura [--jobs N]
  python spikes/FX6/render_fx6.py sheets            compose fx6_gates.jpg + fx6_fixes.jpg from the PNGs

Builds (view dict): {"gate": kind, "fence": kind, "span": m, "opt": {...}} = the gate in a short fence run (2 ken each
side) with its sill pad, as a compound places it; {"plot": name, "old": bool} = a compound (old = its pre-FX6 gates);
{"key": registry key, "kura_old": bool} = a registry shell (kura_old = the pre-FX6 kura door, read from git HEAD).
"human": [x, z] puts the 1.8 m figure there (kit frame). PNGs -> spikes/FX6/renders/.
"""
import copy
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(HERE, "renders")
SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
for p in (os.path.join(DEV, "buildings"), KIT):
    if p not in sys.path:
        sys.path.insert(0, p)
KEN = 1.82
OLD_GATES = {"samurai_m": [(0, 2, 6 * KEN, "kabuki", KEN)], "headman_east": [(0, 2, 9.5 * KEN, "kabuki", KEN)],
             "honjin": [(0, 0, 4.5 * KEN, "kabuki_roofed", 1.5 * KEN), (1, 1, 8 * KEN, "kabuki", KEN)],
             "merchant": [(0, 3, 3 * KEN, "kabuki", KEN)], "kumi": [(0, 0, 4.5 * KEN, "kabuki", KEN)],
             "doshin": [(0, 1, 6.5 * KEN, "kabuki", 1.5 * KEN)],
             "stableyard": [(0, 3, 3 * KEN, "kabuki", 1.5 * KEN)], "timberyard": [(0, 3, 6 * KEN, "kabuki", 1.5 * KEN)],
             "foundryyard": [(0, 3, 4 * KEN, "kabuki", 1.5 * KEN)],
             "brewery": [(0, 3, 6.0 * KEN, "kabuki", 1.5 * KEN)], "dyersyard": [(0, 3, 5.5 * KEN, "kabuki", 1.5 * KEN)],
             "paperyard": [(0, 3, 1.0 * KEN, "kabuki", 1.5 * KEN)]}
OLD_OPENINGS = os.path.join(KIT, "jpparts", "_fx6_old_openings.py")


def gate_demo(kind, fence, span, opt):
    """A gate in a short straight fence (2 ken each side, x 0..4 ken + span), the gate's posts at x 2 ken."""
    from jpparts.core import Part
    from jpparts.templates import dwelling as DW
    from jpparts import sitewall as W, floors as FL
    L = 4 * KEN + span
    P = Part("gate_demo", "", "")
    pw = W.gate_post_w(kind, fence)
    P.merge(DW._wall_path([(0.0, 0.0), (L, 0.0)], fence, ends=("end", "end"), gaps=[(0, 2 * KEN, span, pw)],
                          name="demo_" + kind, **opt))
    gp = DW._gate_part(kind, span, fence, opt)
    P.merge(gp.transformed(0.0, (2 * KEN, 0.0, 0.0)))
    P.merge(FL.sill_pad("demo", 2 * KEN - 0.3, 2 * KEN + span + 0.3, -1.6, 1.4))
    return P


def key_part(v):
    if "gate" in v:
        return gate_demo(v["gate"], v["fence"], v["span"], v.get("opt", {}))
    if "plot" in v:
        from jpparts.templates import dwelling as DW, trade, tradesite  # noqa: F401
        if v.get("old"):
            spec = DW.COMPOUNDS[v["plot"]]
            saved = spec["gates"]
            spec["gates"] = OLD_GATES[v["plot"]]
            try:
                H, _ = DW.compound(plot=v["plot"])
            finally:
                spec["gates"] = saved
            return H
        H, _ = DW.compound(plot=v["plot"])
        return H
    import registry
    import furnishkit
    if v.get("kura_old"):
        import importlib
        from jpparts import openings
        old = importlib.import_module("jpparts._fx6_old_openings")
        openings.part_kura_door = old.part_kura_door
    b = registry.get(v["key"])
    mod = furnishkit._base_module(b)
    M, _, _ = mod.model(name=b.get("recipe_name", b["name"]), **b["params"])
    return M


def blender_main(spec):
    import bpy
    from mathutils import Vector
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
        g["part_mesh"](P, "bld", lod=1, open_doors=v.get("open", 0.0))
        bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.003))
        bpy.context.active_object.data.materials.append(gm)
        if v.get("human"):
            hb = g["to_b"]((v["human"][0], 0.0, v["human"][1]))
            g["human"](hb[0], hb[1], hb[2])
        c = Vector(g["to_b"](v["cam"]))
        t = Vector(g["to_b"](v["look"]))
        cam.location = c
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = (t - c).to_track_quat("-Z", "Y")
        cam.data.type = "PERSP"
        cam.data.lens = v.get("lens", 24)
        cam.data.clip_start = 0.05
        cam.data.clip_end = 500
        bpy.context.scene.render.filepath = os.path.join(OUT, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)


# ------------------------------------------------------------------------------------------------ jobs
def gate_jobs():
    S = 1.5 * KEN
    rows = [("kido_kata", "itabei", KEN, {"kuro": False, "cap": "none"}, "kido_kata: single-leaf board gate, board fence"),
            ("kido_ryo", "itabei", KEN, {"kuro": False, "cap": "none"}, "kido_ryo 1 ken: two-leaf board gate"),
            ("kido_ryo", "itabei", S, {"kuro": True, "cap": "none"}, "kido_ryo 1.5 ken (cart yards), black fence"),
            ("kido_kata", "ikegaki", KEN, {"size": "tall"}, "kido_kata in a tall hedge"),
            ("shiorido", "yotsume", KEN, {}, "shiorido: bamboo lattice gate, yotsume fence"),
            ("opening", "yotsume", KEN, {}, "opening: two posts, no leaf (lane entrance)"),
            ("kabuki", "itabei", S, {"kuro": False, "cap": "none"}, "kabuki-mon (kept for status gates), same scale")]
    jobs = []
    for k, (kind, fence, span, opt, cap) in enumerate(rows):
        gx = 2 * KEN + span / 2
        base = {"gate": kind, "fence": fence, "span": span, "opt": opt, "human": [2 * KEN - 0.9, 1.0],
                "res": [960, 720], "lens": 26}
        jobs.append(("gate_%d_out" % k, cap + " (outside, closed)",
                     dict(base, cam=[gx + 2.6, 1.7, 6.0], look=[gx, 1.1, 0.0])))
        jobs.append(("gate_%d_in" % k, cap + " (inside, open)",
                     dict(base, cam=[gx - 2.4, 1.7, -5.2], look=[gx, 1.0, 0.0], open=1.0)))
    return jobs


def compound_jobs():
    # (plot, gate centre kit (x, z), outward normal (nx, nz)) of the re-assigned gates shown before / after
    G = [("paperyard", (7.5 * KEN, 0.0), (0.0, -1.0)),
         ("dyersyard", (8 * KEN - 5.5 * KEN - 0.5 * KEN, 0.0), (0.0, -1.0)),
         ("brewery", (12 * KEN - 6.0 * KEN - 0.75 * KEN, 0.0), (0.0, -1.0)),
         ("stableyard", (8 * KEN - 3 * KEN - 0.75 * KEN, 0.0), (0.0, -1.0)),
         ("samurai_m", (6.5 * KEN, 17.5 * KEN), (0.0, 1.0)),
         ("kumi", (5.0 * KEN, 0.0), (0.0, 1.0)),
         ("honjin", (8.5 * KEN, 0.0), (0.0, -1.0))]
    jobs = []
    for plot, (gx, gz), (nx, nz) in G:
        cam = [gx + nx * 7.0 + nz * 2.5, 2.2, gz + nz * 7.0 - nx * 2.5]
        look = [gx, 1.0, gz]
        hum = [gx + nx * 1.6 - nz * 1.4, gz + nz * 1.6 + nx * 1.4]
        for old in (True, False):
            jobs.append(("cmp_%s_%s" % (plot, "before" if old else "after"),
                         "%s gate %s" % (plot, "before (kabuki-mon)" if old else "after (FX6 rule)"),
                         {"plot": plot, "old": old, "cam": cam, "look": look, "human": hum, "lens": 24,
                          "res": [960, 720]}))
    return jobs


def kura_jobs():
    out = []
    for key, cam, look in (("kura_plain", [2.5, 1.8, 7.5], [0.0, 1.2, 1.82]),
                           ("ts_maegura", [-1.0, 2.0, 10.0], [-4.5, 1.3, 2.7])):
        for old in (True, False):
            out.append(("kura_%s_%s" % (key, "before" if old else "after"),
                        "%s kura doors %s" % (key, "before (plaster leaves standing out)" if old else
                                              "after (folded back flat)"),
                        {"key": key, "kura_old": old, "cam": cam, "look": look, "lens": 24, "res": [960, 720]}))
    return out


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


def compose(name, title, sub, cells, cols, cw, ch):
    """cells: [(png path, caption)] -> research/production/contact_sheets/<name>.jpg"""
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts/arialbd.ttf", 28),
                                                      "s": (r"C:\Windows\Fonts/arial.ttf", 15)}.items()}
    cap = 44
    rows = (len(cells) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw + (cols + 1) * 8, 96 + rows * (ch + cap + 8) + 8), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((12, 10), title, font=F["h1"], fill=(20, 20, 20))
    for k, line in enumerate(textwrap.wrap(sub, 190)[:2]):
        d.text((12, 50 + 20 * k), line, font=F["s"], fill=(60, 60, 60))
    for i, (p, c) in enumerate(cells):
        x = 8 + (i % cols) * (cw + 8)
        y = 96 + (i // cols) * (ch + cap + 8)
        if p and os.path.isfile(p):
            src = Image.open(p).convert("RGB")
            r = min(cw / src.size[0], ch / src.size[1])
            src = src.resize((max(1, int(src.size[0] * r)), max(1, int(src.size[1] * r))))
            im.paste(src, (x + (cw - src.size[0]) // 2, y + (ch - src.size[1]) // 2))
        for k, line in enumerate(textwrap.wrap(c, int(cw / 7.2))[:2]):
            d.text((x + 2, y + ch + 4 + 18 * k), line, font=F["s"], fill=(20, 20, 20))
    os.makedirs(SHEETS, exist_ok=True)
    dst = os.path.join(SHEETS, name + ".jpg")
    im.save(dst, quality=86)
    print("sheet ->", dst, im.size)


def sheets():
    R, B, A = OUT, os.path.join(OUT, "before"), os.path.join(OUT, "after")
    cells = []
    for n, c, v in gate_jobs():
        cells.append((os.path.join(R, n + ".png"), c))
    for n, c, v in compound_jobs():
        cells.append((os.path.join(R, n + ".png"), c))
    compose("fx6_gates", "FX6: the small-gate family + every re-assigned compound gate",
            "Rows 1-7: each gate in a short run of its fence, outside closed | inside open (dark figure = 1.8 m). Then "
            "compound gates before (kabuki-mon) | after (the FX6 gate-picker rule: fence kind + height + status; table "
            "in parts/K3_NOTES.md section 6). Status gates kept: honjin roofed kabuki-mon, doshin kabuki-mon, nagaya-mon.",
            cells, 2, 640, 480)
    fx = [(os.path.join(B, "pr_jp_f_monohoshi.png"), "Dyer's drying frames BEFORE: fallen cloths a flat strip + a stiff "
           "ramp in the air; hung lengths beside the bar"),
          (os.path.join(A, "jp_f_monohoshi_row.png"), "AFTER: lengths drape over the bar; the fallen ones lie flat on "
           "the ground (5 cm, 4 cm of it under the yard surface)"),
          (os.path.join(R, "kura_kura_plain_before.png"), "Kura door BEFORE: the white plaster leaves stand straight out "
           "(look like doors that should work)"),
          (os.path.join(R, "kura_kura_plain_after.png"), "AFTER: folded back flat on the surround / wall; only the "
           "wooden sliding door works"),
          (os.path.join(R, "kura_ts_maegura_before.png"), "Sake kura (mae-gura) doors BEFORE"),
          (os.path.join(R, "kura_ts_maegura_after.png"), "AFTER (every '_open' kura: plain, namako, the sake pair, the "
           "cask kura)"),
          (os.path.join(B, "rm_f_ts_maegura_muro.png"), "Koji room BEFORE: the koji bed 0.35 m inside the only door"),
          (os.path.join(A, "rm_f_ts_maegura_muro.png"), "AFTER: the bed against the back wall, the tray shelves on the "
           "side wall, a clear floor inside the door"),
          (os.path.join(B, "jp_f_hangiri_row.png"), "Washing / starter tubs BEFORE (right model): one tub on edge at "
           "70 deg on one rim point, leaning on nothing"),
          (os.path.join(A, "jp_f_hangiri_row.png"), "AFTER: that tub lies upside down on the floor")]
    compose("fx6_fixes", "FX6: Stephen's 3c-1 fixes, before | after",
            "Cloths, kura doors, the koji room table, the floating tub. New checks: spikes/FX6/propfloat.py (prop pieces "
            "rest / cloth hangs), propseat.py (props seated in rooms), roomaccess.py (a 0.6 m capsule walks in from "
            "every door).", fx, 2, 640, 400)


def main(argv):
    if argv[0] == "sheets":
        sheets()
        return 0
    jobs_n = min(4, int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 4)
    if argv[0] == "gates":
        run_jobs(gate_jobs(), jobs_n)
    elif argv[0] == "compounds":
        run_jobs(compound_jobs(), jobs_n)
    elif argv[0] == "kura":
        r = subprocess.run(["git", "show", "4e6c296:parts/kit/jpparts/openings.py"], cwd=DEV, capture_output=True)
        with open(OLD_OPENINGS, "wb") as f:
            f.write(r.stdout)
        try:
            run_jobs(kura_jobs(), jobs_n)
        finally:
            os.remove(OLD_OPENINGS)
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        sys.path.insert(0, HERE)
        try:                                    # Blender's Python has no PIL: skip uvwood's atlas-size guard there
            import PIL  # noqa: F401
        except ImportError:
            from jpparts import uvwood as _uvw
            _uvw._png_ok = lambda core, mat: True
        spec = json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8"))
        blender_main(spec)
    else:
        sys.exit(main(sys.argv[1:]))
