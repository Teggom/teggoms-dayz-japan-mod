"""C1 debug: python spikes/C1/dbg.py <key> sweep <door#> | leak | c15"""
import os
import sys

import numpy as np

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import registry  # noqa: E402
import shellkit  # noqa: E402
from jpparts import mlod, checks as C, raycheck as RC  # noqa: E402

b = registry.get(sys.argv[1])
M, floors, rooms = shellkit.model(name=b["name"], **b["params"])
L = {mlod.lod_name(l.resolution): l for l in M.lods()}
what = sys.argv[2]
if what == "sweep":
    k = int(sys.argv[3])
    d = M.doors[k - 1]
    g = C.components(L["Geometry"])
    hits = C.sweep_hits(d, g)
    print(getattr(d, "label", ""), "hits", hits)
    for c in g:
        if c["name"] in hits:
            print(c["name"], [round(v, 3) for v in c["bbox"]])
    for a in d.anims:
        lb = [c["bbox"] for c in g if c["door"] == a["bone"]]
        print("leaf", a["bone"], [[round(v, 3) for v in bb] for bb in lb], "axis", a["axis"], a["amount"])
    # which solids are near the hit boxes
    for c in g:
        if c["name"] in hits:
            bb = c["bbox"]
            for s in M.solids:
                if not getattr(s, "geo", False):
                    continue
                s.finalize()
                sb = s.bbox()
                if all(abs(sb[i] - bb[i]) < 1e-3 for i in range(6)):
                    print("  solid", s.tag, getattr(s, "src", ""))
elif what == "leak":
    T = RC.lod_triangles(L["Resolution 1"])
    rr = [{"name": f["name"], "rect": f["rect"], "y": f["y"], "obstacles": f.get("obstacles", [])} for f in floors]
    res = RC.envelope_leak(L["Resolution 1"], rr, [])
    bb = M.bbox()
    for name, (n, via, leaks) in res.items():
        for o, dv in leaks[:6]:
            o, dv = np.array(o), np.array(dv)
            # where the ray crosses the building's outer bbox planes, and the first 3 m sampled
            pts = [tuple(round(float(v), 2) for v in (o + dv * t)) for t in (0.5, 1.0, 2.0, 3.0, 4.0)]
            print(name, "o", tuple(o), "d", tuple(round(float(v), 3) for v in dv), pts)
elif what == "c15":
    x0, x1, _, _, z0, z1 = M.bbox()
    xs = np.arange(x0 + 0.05, x1, 0.12)
    zs = np.arange(z0 + 0.05, z1, 0.12)
    O = np.array([(x, 30.0, z) for x in xs for z in zs])
    Dn = np.tile(np.array([[0.0, -1.0, 0.0]]), (len(O), 1))
    tops = {ln: 30.0 - RC.cast(RC.lod_triangles(L[ln]), O, Dn, 40.0, chunk=64) for ln in
            ("Resolution 1", "Resolution 2", "Resolution 3")}
    for ln in ("Resolution 2", "Resolution 3"):
        a, c = tops["Resolution 1"], tops[ln]
        m = np.isfinite(a) & (a > 2.5) & (np.where(np.isfinite(c), np.abs(a - c), 9.9) > 0.10)
        for i in np.where(m)[0][:10]:
            print(ln, "at", tuple(round(float(v), 2) for v in O[i][[0, 2]]), "R1 %.3f %s %.3f" % (a[i], ln, c[i]))
if what == "dw":
    import importlib.util
    sp = importlib.util.spec_from_file_location("mv", os.path.join(DEV, "buildings", "machiya_t3_01", "verify.py"))
    sys.path.insert(0, os.path.join(DEV, "buildings", "machiya_t3_01"))
    MV = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(MV)
    k = int(sys.argv[3])
    d = M.doors[k - 1]
    g = C.components(L["Geometry"])
    ok, msg, clear = MV.door_world(d, g)
    print(ok, msg)
    import re as _re
    for nm in _re.findall(r"Component\d+", msg):
        c = [c for c in g if c["name"] == nm][0]
        print(nm, [round(v, 3) for v in c["bbox"]])
if what == "at":
    x, z = float(sys.argv[3]), float(sys.argv[4])
    for s in M.solids:
        s.finalize()
        bb = s.bbox()
        if bb[0] <= x <= bb[1] and bb[4] <= z <= bb[5] and bb[3] > float(sys.argv[5] if len(sys.argv) > 5 else 3.5):
            print(sorted(s.vis), s.tag, [round(v, 3) for v in bb])
if what == "stair":
    print(shellkit.STAIRS)
    from jpparts import buildcheck as BC
    st = shellkit.STAIRS[0]
    w0, w1, z0, z1 = st["well"]
    for x in np.linspace(w0 + 0.05, w1 - 0.05, 6):
        for z in (st["foot"][1] + 0.15, st["foot"][1] + 0.6, st["foot"][1] + 1.05):
            print(round(x, 2), round(z, 2), [(round(h, 2), t[-20:]) for h, t in BC.road_heights(L["Roadway"], x, z)])
