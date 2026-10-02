#!/usr/bin/env python3
r"""FX5 renders (on parts/kit/render_b2.py's Blender side, like render_k3.py).

  python spikes/FX5/render_fx5.py <set> [--tag before|after]     sets: hedge, gate, joint
  python spikes/FX5/render_fx5.py sheet <name> <png ...>          compose a contact sheet from rendered PNGs

Builds are "fx5:<fn>" (functions of this file returning a kit Part in the compound's kit frame, x east, z north,
y up) or anything render_b2.get_part takes. PNGs -> spikes/FX5/renders/<set>_<tag>_<view>.png.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
sys.path.insert(0, KIT)
import render_b2 as RB  # noqa: E402

OUT = os.path.join(HERE, "renders")
SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
KEN = 1.82


def _compound(plot):
    from jpparts.templates import dwelling as DW, trade  # noqa: F401
    H, info = DW.compound(plot=plot)
    return H


def get_part(spec):
    kind, what = spec.split(":", 1)
    if kind == "fx5":
        if what.startswith("compound_"):
            return _compound(what[len("compound_"):])
    return RB._orig_get_part(spec)


# views per set: (name, caption, view dict); kit frame of the compound (x east, z north, y up)
def views(setname):
    if setname == "hedge":
        b = "fx5:compound_headman_east"
        return [
            ("eye_along", "eye level, 2.5 m off the west hedge, looking along the run",
             {"build": b, "interior": {"cam": [-2.5, 1.65, 3.0], "look": [0.0, 1.0, 14.0], "lens": 24}}),
            ("eye_front", "eye level, 3.5 m in front of the west hedge",
             {"build": b, "interior": {"cam": [-3.5, 1.65, 12.0], "look": [0.0, 1.2, 12.0], "lens": 22}}),
            ("corner", "the north-west corner from outside",
             {"build": b, "interior": {"cam": [-4.0, 1.65, 34.5], "look": [0.5, 1.0, 29.5], "lens": 22}}),
            ("wide", "the west run, 3/4 from 14 m",
             {"build": b, "interior": {"cam": [-12.0, 5.0, -4.0], "look": [0.0, 1.0, 12.0], "lens": 30}}),
        ]
    if setname == "gate":
        out = []
        for plot, gx, gz, nz in (("honjin", 5.25 * KEN, 26 * KEN, 1.0), ("doshin", 10 * KEN - 0.0, 7.25 * KEN, 0.0)):
            pass
        b = "fx5:compound_honjin"
        out.append(("honjin_front", "honjin front gate passage, from the street at eye level",
                    {"build": b, "interior": {"cam": [5.25 * KEN + 1.2, 1.65, 26 * KEN + 3.5],
                                              "look": [5.25 * KEN, 0.0, 26 * KEN], "lens": 22}}))
        out.append(("honjin_low", "honjin front gate sill, low close-up",
                    {"build": b, "interior": {"cam": [5.25 * KEN + 0.6, 0.45, 26 * KEN + 1.8],
                                              "look": [5.25 * KEN, 0.0, 26 * KEN], "lens": 20}}))
        b2 = "fx5:compound_stableyard"
        out.append(("stable_gate", "stable yard gate (W3B), eye level from the street",
                    {"build": b2, "interior": {"cam": [4.25 * KEN + 1.0, 1.65, -3.5],
                                               "look": [4.25 * KEN, 0.0, 0.0], "lens": 22}}))
        return out
    if setname == "joint":
        b = "fx5:compound_honjin"
        return [
            ("honjin_ne", "honjin NE: plaster street wall meets the board fence (from inside)",
             {"build": b, "interior": {"cam": [17 * KEN - 3.0, 1.65, 26 * KEN - 3.0],
                                       "look": [17 * KEN, 1.0, 26 * KEN], "lens": 22}}),
            ("honjin_ne_out", "honjin NE from outside (east)",
             {"build": b, "interior": {"cam": [17 * KEN + 3.0, 1.65, 26 * KEN - 2.0],
                                       "look": [17 * KEN, 1.0, 26 * KEN], "lens": 22}}),
        ]
    raise KeyError(setname)


def run_jobs(jobs):
    os.makedirs(OUT, exist_ok=True)
    jf = os.path.join(OUT, "_jobs_%d.json" % os.getpid())
    with open(jf, "wb") as f:
        f.write(json.dumps({"out_dir": OUT, "res": [1280, 800], "jobs": jobs}, indent=1).encode("utf-8"))
    r = subprocess.run([RB.BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__), "--",
                        "--blender", jf], capture_output=True, text=True, errors="replace")
    done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
    print("%d/%d rendered" % (len(done), len(jobs)))
    if len(done) < len(jobs):
        print((r.stdout + r.stderr)[-4000:])
    os.remove(jf)


def sheet(name, title, items, cols=2):
    """items: [(png path, caption)] -> research/production/contact_sheets/<name>.jpg"""
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGB") for p, _ in items]
    w, h = 640, 400
    pad, cap = 8, 22
    rows = (len(ims) + cols - 1) // cols
    W = cols * (w + pad) + pad
    Hh = 40 + rows * (h + cap + pad) + pad
    out = Image.new("RGB", (W, Hh), (245, 244, 240))
    d = ImageDraw.Draw(out)
    d.text((pad, 12), title, fill=(20, 20, 20))
    for k, (im, (_, c)) in enumerate(zip(ims, items)):
        r_, c_ = divmod(k, cols)
        x, y = pad + c_ * (w + pad), 40 + r_ * (h + cap + pad)
        out.paste(im.resize((w, h)), (x, y))
        d.text((x + 2, y + h + 4), c, fill=(20, 20, 20))
    os.makedirs(SHEETS, exist_ok=True)
    dst = os.path.join(SHEETS, name + ".jpg")
    out.save(dst, quality=88)
    print("sheet ->", dst)
    return dst


def main(argv):
    if argv[0] == "sheet":
        return 0
    setname = argv[0]
    tag = argv[argv.index("--tag") + 1] if "--tag" in argv else "after"
    only = [a for a in argv[1:] if not a.startswith("--") and a != tag]
    jobs = [("%s_%s_%s" % (setname, tag, n), c, v) for n, c, v in views(setname) if not only or n in only]
    run_jobs(jobs)
    return 0


RB._orig_get_part = RB.get_part
RB.get_part = get_part

if __name__ == "__main__":
    if "--blender" in sys.argv:
        sys.path.insert(0, HERE)
        RB.blender_main(json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8")))
    else:
        sys.exit(main(sys.argv[1:]))
