"""FX1 rope torii head room: for every torii MODEL with a rope (jp_s_torii_*rope*) and every PLACED walk-through torii
(test/placements/*.csv, FB1 toriiclear's skip list), the clear height under
  - the tie-beam (nuki) / any Geometry over the walking strip, and
  - the lowest VISUAL point over the walking strip (rope sag, tassels, shide tips): Resolution 1 vertices above 1.0 m,
    across the passage between the posts minus 0.25 m at each post (where a player walks).
Model numbers are over the torii base (y 0); placed numbers over the walking surface under it (terrain or a step's
Roadway, as FB1/toriiclear.py). NEED_ROPE = 2.30 m to the lowest shide / tassel tip (FX1 brief).

  python spikes/FX1/ropeclear.py [--models] [--placed] [csv ...]
"""
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "FB1"))
import toriiclear as TC  # noqa: E402  (FB1: walk_y, lod, rows_of, SKIP)
from jpparts import mlod, checks as C, decor as DC  # noqa: E402

NEED_ROPE = 2.30


def strip_of(name):
    """(x half-width of the walking strip, lowest visual y over it, lowest Geometry y over it) in the model frame."""
    geo = TC.lod(name, "Geometry")
    comps = C.components(geo)
    posts = [c["bbox"] for c in comps if c["bbox"][2] < 0.5 and c["bbox"][3] > 1.5]
    xin = min((min(abs(b[0]), abs(b[1])) for b in posts), default=0.6)
    half = max(0.3, xin - 0.25)
    g = [c["bbox"][2] for c in comps if c["bbox"][0] < half and c["bbox"][1] > -half and c["bbox"][2] > 1.0]
    r1 = TC.lod(name, "Resolution 1")
    used = set(v[0] for f in r1.faces for v in f[0])
    vis = [r1.points[i][1] for i in used if abs(r1.points[i][0]) <= half and r1.points[i][1] > 1.0]
    return half, (min(vis) if vis else None), (min(g) if g else None)


def models():
    cat = DC.catalog()
    print("model                                       strip +-   nuki/geo clear   lowest rope/shide")
    for k in sorted(cat):
        if not k.startswith("jp_s_torii") or "rope" not in k or any(s in k for s in TC.SKIP):
            continue
        half, v, g = strip_of(k)
        print("%-44s %5.2f      %5.2f            %5.2f  %s" % (k, half, g or -1, v or -1,
                                                              "OK" if v and v >= NEED_ROPE else "LOW"))


def placed(argv):
    paths = [a for a in argv if a.endswith(".csv")] or sorted(glob.glob(os.path.join(DEV, "test", "placements",
                                                                                       "*.csv")))
    rows = TC.rows_of(paths)
    steps = [r for r in rows if "steps" in r[1]]
    bad = 0
    for (src, nm, x, z, yaw, yo) in rows:
        if "torii" not in nm or any(s in nm for s in TC.SKIP):
            continue
        half, v, g = strip_of(nm)
        base = TC.T.ground(x, z) + yo
        worst_v = worst_g = 99.0
        for fx in (-half, -half / 2, 0.0, half / 2, half):
            for fz in (-0.3, 0.0, 0.3):
                a = math.radians(yaw)
                wx = x + fx * math.cos(a) + fz * math.sin(a)
                wz = z - fx * math.sin(a) + fz * math.cos(a)
                w = TC.walk_y(wx, wz, steps)
                if v is not None:
                    worst_v = min(worst_v, base + v - w)
                if g is not None:
                    worst_g = min(worst_g, base + g - w)
        rope = "rope" in nm
        ok = (not rope) or worst_v >= NEED_ROPE
        bad += not ok
        print("%-4s %-6s %-44s (%.1f, %.1f) under nuki %.2f  under rope/shide %s" % (
            "OK" if ok else "LOW", src, nm, x, z, worst_g, ("%.2f" % worst_v) if rope else "-"))
    print("ropeclear: %d placed rope torii with less than %.2f m under the lowest rope / shide tip" % (bad, NEED_ROPE))
    return bad


if __name__ == "__main__":
    if "--placed" not in sys.argv:
        models()
    if "--models" not in sys.argv:
        sys.exit(1 if placed(sys.argv[1:]) else 0)
