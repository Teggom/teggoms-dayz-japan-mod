"""FX4 lathecheck: find every fkit.lathe surface built inside out (the bonsho fault, 2026-10-01).

fkit.lathe wants the profile traversed with the material on the LEFT (up the outside, over the rim, down the inside);
a profile run the other way turns every face inward (you see into the object, its outside is culled).
A profile that is closed (axis to axis, or first point == last point) has a signed area in the (r, y) plane:
counter-clockwise (> 0) = outward = right; clockwise (< 0) = inside out. Open profiles (a hoop band, a cup wall) are
not judged (counted only).

  python spikes/FX4/lathecheck.py            build every prop of jp_furniture (B3a+L1+S1+W2F) and jp_site (B3b+L2)
                                             geometry only (no MLOD, no binarize), list the inside-out call sites
"""
import collections
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in reversed(("B3a", "L1", "S1", "W2F", "B3b", "L2", "FX2")):   # B3a first: its build.py is 'build'
    sys.path.insert(0, os.path.join(DEV, "spikes", p))

import fkit  # noqa: E402

_orig = fkit.lathe
BAD = collections.Counter()
OPEN = [0]
OK = [0]


def area(prof):
    a = 0.0
    for i in range(len(prof)):
        r0, y0 = prof[i]
        r1, y1 = prof[(i + 1) % len(prof)]
        a += r0 * y1 - r1 * y0
    return a / 2.0


def lathe(profile, n, mat, *a, **kw):
    pr = [tuple(map(float, q)) for q in profile]
    closed = (abs(pr[0][0]) < 1e-6 and abs(pr[-1][0]) < 1e-6) or (abs(pr[0][0] - pr[-1][0]) < 1e-6 and
                                                                abs(pr[0][1] - pr[-1][1]) < 1e-6)
    if not closed or len(pr) < 3:
        OPEN[0] += 1
    elif area(pr) < -1e-9:
        st = traceback.extract_stack(limit=6)[:-1]
        site = next((f for f in reversed(st) if not f.filename.endswith("fkit.py")), st[-1])
        BAD["%s:%d" % (os.path.relpath(site.filename, DEV), site.lineno)] += 1
    else:
        OK[0] += 1
    return _orig(profile, n, mat, *a, **kw)


fkit.lathe = lathe


def models(builder, modules_attr="MODULES"):
    import importlib
    out = []
    for m in getattr(builder, modules_attr):
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
        for p in mod.PROPS:
            for md in p["models"]:
                out.append((m, md))
    return out


def main():
    import build_w2f  # noqa: F401  (B3a build MODULES = B3a + L1 + S1 + W2F)
    import importlib
    BA = importlib.import_module("build")            # spikes/B3a/build.py (first on the path)
    todo = []
    fa = os.path.join(DEV, "spikes", "B3a", "build.py")
    if os.path.abspath(BA.__file__) != fa:
        raise SystemExit("unexpected build module %s" % BA.__file__)
    todo += models(BA)
    # jp_site: B3b build + L2 modules (load B3b's build.py under another name)
    import importlib.util
    spec = importlib.util.spec_from_file_location("b3b_build", os.path.join(DEV, "spikes", "B3b", "build.py"))
    BB = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(BB)
    BB.MODULES = BB.MODULES + ["props_l2_yard", "props_l2_street"]
    todo += models(BB)
    fails = 0
    for m, md in todo:
        try:
            md["build"]()
        except Exception as e:          # noqa: BLE001  (a model that needs its builder's state: report, go on)
            fails += 1
            print("  build error %s %s: %s" % (m, md["p3d"], e))
    print("models built: %d (errors %d); closed lathes ok %d, open (not judged) %d" % (len(todo), fails, OK[0], OPEN[0]))
    if BAD:
        print("INSIDE-OUT lathe call sites (calls):")
        for k, v in sorted(BAD.items()):
            print("  %s  x%d" % (k, v))
    else:
        print("no inside-out lathe")
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
