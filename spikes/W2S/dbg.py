"""W2C debug (from spikes/C2/dbg.py): python spikes/C2/dbg.py <key> leak | c15 | c17 <door#> | c12
(rural shells, model frame)."""
import os
import sys

import numpy as np

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import registry  # noqa: E402
import sacredkit as ruralkit  # noqa: E402
from jpparts import mlod, checks as C, raycheck as RC  # noqa: E402

b = registry.get(sys.argv[1])
M, floors, rooms = ruralkit.model(name=b.get("recipe_name", b["name"]), **b["params"])
L = {mlod.lod_name(l.resolution): l for l in M.lods()}
what = sys.argv[2]


def solids_at(x, z, lod=1, y_min=-9):
    out = []
    for s in M.solids:
        if lod not in s.vis:
            continue
        bb = s.bbox()
        if bb[0] - 0.02 <= x <= bb[1] + 0.02 and bb[4] - 0.02 <= z <= bb[5] + 0.02 and bb[3] > y_min:
            out.append((round(bb[3], 2), s.tag))
    return sorted(out, reverse=True)[:6]


if what == "leak":
    T = RC.lod_triangles(L["Resolution 1"])
    rr = [{"name": f["name"], "rect": f["rect"], "y": f["y"], "obstacles": f.get("obstacles", [])} for f in floors
          if f.get("enclosed", True)]
    res = RC.envelope_leak(L["Resolution 1"], rr, [(n, b_) for n, b_ in ruralkit.PORTALS])
    for name, (n, via, leaks) in res.items():
        print(name, n, via, len(leaks))
        for o, dv in leaks[:12]:
            o, dv = np.array(o), np.array(dv)
            pts = [tuple(round(float(v), 2) for v in (o + dv * t)) for t in (0.5, 1.0, 1.5, 2.0, 3.0)]
            print("  o", tuple(o), "d", tuple(round(float(v), 3) for v in dv), pts)
elif what == "c15":
    x0, x1, _, _, z0, z1 = M.bbox()
    xs = np.arange(x0 + 0.05, x1, 0.12)
    zs = np.arange(z0 + 0.05, z1, 0.12)
    O = np.array([(x, 30.0, z) for x in xs for z in zs])
    Dn = np.tile(np.array([[0.0, -1.0, 0.0]]), (len(O), 1))
    tops = {ln: 30.0 - RC.cast(RC.lod_triangles(L[ln]), O, Dn, 40.0, chunk=64) for ln in
            ("Resolution 1", "Resolution 2", "Resolution 3")}
    for ln in ("Resolution 2", "Resolution 3"):
        a, bb = tops["Resolution 1"], tops[ln]
        dd = np.where(np.isfinite(bb), np.abs(a - bb), 9.9)
        m = np.isfinite(a) & (a > 2.5) & (dd > 0.10)
        idx = np.where(m)[0]
        print(ln, len(idx))
        seen = set()
        for i in idx[:400]:
            x, z = O[i][0], O[i][2]
            tags = tuple(t for _, t in solids_at(x, z, 1, a[i] - 0.05)[:2])
            if tags in seen:
                continue
            seen.add(tags)
            print("  (%.2f, %.2f) R1 %.2f %s %.2f  R1 top tags %s" % (x, z, a[i], ln, bb[i] if np.isfinite(bb[i]) else -1,
                                                                    tags))
elif what == "c17":
    k = int(sys.argv[3])
    d = M.doors[k - 1]
    vcomps = C.components(L["View Geometry"])
    T1 = RC.lod_triangles(L["Resolution 1"])
    n_, sl = RC.jamb_slits(d, vcomps, T1)
    print(getattr(d, "label", ""), n_, len(sl))
    for e, q in sl[:10]:
        print("  eye", tuple(round(float(v), 3) for v in e), "->", tuple(round(float(v), 3) for v in q))
elif what == "c12":
    for x in RC.roof_pokes(M.solids)[:10]:
        print(x)
