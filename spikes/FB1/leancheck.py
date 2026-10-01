#!/usr/bin/env python3
r"""FB1 (F): do wall-leaning props actually touch their wall?

A prop with sidecar anchor 'wall' (tools leaned on a wall, a ladder, a shutter, bales against a wall) has its wall
plane at prop z = 0 and stands in front of it (+z). Every such object on the island - the buildings' own site()
objects (records -> C.csv rows) and the free rows of test/placements/C3.csv + SH1.csv - is tested against the
Geometry LOD of every registry building placed within 15 m: rays from the prop's wall plane at heights 0.3 / 0.8 /
1.3 m and across its width, starting at the prop's back-most point (bbox z0), go BACK (-z of the prop) and the gap to
the first building geometry is measured.

  python spikes/FB1/leancheck.py [--all]      prints one line per wall-anchored object: gap (m) to the nearest wall
  OK = gap <= 0.03 m (touching), FAR = nothing within 1.5 m behind it (free-standing: listed, not judged).
"""
import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)
from jpparts import mlod, checks as C, decor as DC  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

TOUCH = 0.03


def ray_convex(o, d, comp):
    t0, t1 = 0.0, 1e9
    for n, dd in comp["planes"]:                        # inside: n . q >= dd (n inward)
        a = mlod._dot(n, d)
        b = mlod._dot(n, o) - dd
        if abs(a) < 1e-12:
            if b < 0:
                return None
            continue
        t = -b / a
        if a > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return t0


def world_to_model(w, pos, yaw):
    y = math.radians(yaw)
    dx, dz = w[0] - pos[0], w[2] - pos[2]
    # inverse of loot.model_to_world: m = Ry(-yaw) * (w - pos)
    return (dx * math.cos(y) - dz * math.sin(y), w[1] - pos[1], dx * math.sin(y) + dz * math.cos(y))


def buildings():
    import registry
    import pipeline
    out = []
    for b in registry.BUILDINGS:
        if not b["ship"] or not b["placements"]:
            continue
        rp = pipeline.record_path(b)
        if not os.path.isfile(rp):
            continue
        rec = json.load(open(rp, "rb"))
        mp = os.path.join(pipeline.bdir(b), "out", rec["name"] + ".p3d")
        if not os.path.isfile(mp):
            continue
        out.append((b, rec, mp))
    return out


_COMPS = {}


def comps(mp):
    if mp not in _COMPS:
        geo = next(l for l in mlod.read_mlod(mp) if mlod.lod_name(l.resolution) == "Geometry")
        _COMPS[mp] = [c for c in C.components(geo) if not c["door"]]
    return _COMPS[mp]


def objects(blds):
    """Every wall-anchored object: (label, name, world x, z, yaw, y_off)."""
    cat = DC.catalog()
    out = []
    for b, rec, mp in blds:
        for s in rec.get("site", []):
            nm = os.path.basename(s["p3d"])[:-4]
            if cat.get(nm, {}).get("anchor") != "wall":
                continue
            for pl in b["placements"]:
                wx, _, wz = bloot.model_to_world((s["x"], 0.0, s["z"]), pl["pos"], pl["yaw"])
                out.append(("%s site" % b["key"], nm, wx, wz, (pl["yaw"] + s["yaw"]) % 360.0, s.get("y", 0.0),
                            (b["key"], s)))
    for f in ("C3.csv", "SH1.csv"):
        p = os.path.join(DEV, "test", "placements", f)
        with open(p, "rb") as fh:
            rows = list(csv.reader(fh.read().decode("utf-8").splitlines()))
        for r in rows[1:]:
            if not r or r[0].startswith("#"):
                continue
            nm = os.path.basename(r[0].replace("\\", "/"))[:-4]
            if cat.get(nm, {}).get("anchor") != "wall":
                continue
            out.append((f, nm, float(r[1]), float(r[2]), float(r[3]), float(r[4]), None))
    return out


def gap(o, blds, ground=25.0):
    label, nm, wx, wz, yaw, yo, _ = o
    inf = DC.catalog()[nm]
    bb = inf["bbox"]                                    # x0, x1, y0, y1, z0, z1 in the prop frame
    best = None
    y = math.radians(yaw)
    back = (-math.sin(y), 0.0, -math.cos(y))           # prop -z in world
    side = (math.cos(y), 0.0, -math.sin(y))            # prop +x in world
    for b, rec, mp in blds:
        for pl in b["placements"]:
            if math.hypot(pl["pos"][0] - wx, pl["pos"][2] - wz) > 15.0:
                continue
            cs = comps(mp)
            for h in (0.3, 0.8, 1.3):
                if h > bb[3]:
                    continue
                for fx in (0.2, 0.5, 0.8):
                    ox = bb[0] + (bb[1] - bb[0]) * fx
                    zb = bb[4]                      # the prop's back-most point (its bbox z0), not just z = 0
                    w = (wx + side[0] * ox - back[0] * zb, ground + yo + h, wz + side[2] * ox - back[2] * zb)
                    om = world_to_model(w, pl["pos"], pl["yaw"])
                    dm = world_to_model((w[0] + back[0], w[1], w[2] + back[2]), pl["pos"], pl["yaw"])
                    dm = (dm[0] - om[0], dm[1] - om[1], dm[2] - om[2])
                    for c in cs:
                        t = ray_convex(om, dm, c)
                        if t is not None and t < 1.5 and (best is None or t < best[0]):
                            best = (t, b["key"], h)
                        if t is not None and t < 1.5:
                            PER_H[h] = min(PER_H.get(h, 9.0), t)
    return best


PER_H = {}


def main(argv):
    blds = buildings()
    objs = objects(blds)
    bad = 0
    for o in objs:
        PER_H.clear()
        g = gap(o, blds)
        if "--heights" in argv and g is not None:
            print("      gap by height: %s" % ", ".join("%.1f m: %.3f" % kv for kv in sorted(PER_H.items())))
        if g is None:
            print("FAR   %-34s %-30s (%.2f, %.2f) nothing behind it within 1.5 m" % (o[0], o[1], o[2], o[3]))
            continue
        ok = g[0] <= TOUCH
        bad += not ok
        print("%-5s %-34s %-30s (%.2f, %.2f) gap %.3f m to %s" % ("OK" if ok else "GAP", o[0], o[1], o[2], o[3], g[0],
                                                                 g[1]))
    print("leancheck: %d wall-anchored objects, %d with a gap > %.2f m" % (len(objs), bad, TOUCH))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
