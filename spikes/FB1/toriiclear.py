#!/usr/bin/env python3
r"""FB1 (G): head clearance under every walk-through torii on the island (test/placements/*.csv).

For each torii row (p3d name contains 'torii', not mini / leaning / fallen / rotted / collapsed), the lowest Geometry
of the torii over the walking strip (x within +-0.6 m of its centre line, the full depth of its beams) is compared with
the walking surface under it: the terrain (T's heightmap, as SH1 seats objects) or the Roadway of any step / landing
module within 4 m (their MLOD Roadway, placed like the world build: y = ground at the origin + y_offset).

  python spikes/FB1/toriiclear.py [csv ...]       default: every test/placements/*.csv
Prints clearance per torii; NEED = 2.20 m (a standing player both ways, FB1 brief G).
"""
import csv
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "SH1")):
    if p not in sys.path:
        sys.path.insert(0, p)
from jpparts import mlod, checks as C, decor as DC  # noqa: E402
import terrain_sh1 as T  # noqa: E402

NEED = 2.20
SKIP = ("mini", "lean", "fallen", "rotted", "collapsed", "_ab_")


def rows_of(paths):
    out = []
    for p in paths:
        with open(p, "rb") as f:
            for r in csv.reader(f.read().decode("utf-8").splitlines()):
                if not r or r[0].startswith("#") or r[0] == "p3d":
                    continue
                out.append((os.path.basename(p), os.path.basename(r[0].replace("\\", "/"))[:-4], float(r[1]),
                            float(r[2]), float(r[3]), float(r[4])))
    return out


_L = {}


def lod(name, which):
    k = (name, which)
    if k not in _L:
        inf = DC.catalog()[name]
        _L[k] = next((l for l in mlod.read_mlod(inf["master"]) if mlod.lod_name(l.resolution) == which), None)
    return _L[k]


def to_local(x, z, ox, oz, yaw):
    y = math.radians(yaw)
    dx, dz = x - ox, z - oz
    return dx * math.cos(y) - dz * math.sin(y), dx * math.sin(y) + dz * math.cos(y)


def inside(px, pz, poly):
    c = False
    for i in range(len(poly)):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % len(poly)]
        if (z1 > pz) != (z2 > pz) and px < x1 + (pz - z1) * (x2 - x1) / (z2 - z1):
            c = not c
    return c


def road_y(name, lx, lz):
    l = lod(name, "Roadway")
    best = None
    if l is None:
        return None
    for verts, _, _, _ in l.faces:
        pts = [l.points[v[0]] for v in verts]
        if not inside(lx, lz, [(p[0], p[2]) for p in pts]):
            continue
        n = mlod._face_formula_normal(pts)
        if abs(n[1]) < 1e-9:
            continue
        y = (mlod._dot(n, pts[0]) - n[0] * lx - n[2] * lz) / n[1]
        best = y if best is None else max(best, y)
    return best


def walk_y(x, z, steps):
    y = T.ground(x, z)
    for (_, nm, sx, sz, syaw, syo) in steps:
        if abs(sx - x) > 4 or abs(sz - z) > 4:
            continue
        lx, lz = to_local(x, z, sx, sz, syaw)
        ry = road_y(nm, lx, lz)
        if ry is not None:
            y = max(y, T.ground(sx, sz) + syo + ry)
    return y


def main(argv):
    paths = argv or sorted(glob.glob(os.path.join(DEV, "test", "placements", "*.csv")))
    rows = rows_of(paths)
    steps = [r for r in rows if "steps" in r[1]]
    bad = 0
    for (src, nm, x, z, yaw, yo) in rows:
        if "torii" not in nm or any(s in nm for s in SKIP):
            continue
        geo = lod(nm, "Geometry")
        comps = C.components(geo)
        base = T.ground(x, z) + yo
        lowest = None
        for c in comps:
            b = c["bbox"]
            if b[0] < 0.6 and b[1] > -0.6 and b[2] > 1.0:          # spans the walking strip, above head-ish
                if lowest is None or b[2] < lowest[0]:
                    lowest = (b[2], b[4], b[5])
        if lowest is None:
            continue
        worst = 99.0
        for fx in (-0.6, -0.3, 0.0, 0.3, 0.6):
            for fz in (lowest[1], (lowest[1] + lowest[2]) / 2, lowest[2]):
                y = math.radians(yaw)
                wx = x + fx * math.cos(y) + fz * math.sin(y)
                wz = z - fx * math.sin(y) + fz * math.cos(y)
                worst = min(worst, base + lowest[0] - walk_y(wx, wz, steps))
        ok = worst >= NEED
        bad += not ok
        print("%-4s %-8s %-44s (%.2f, %.2f) beam bottom %.2f over its base; clear %.2f m" % (
            "OK" if ok else "LOW", src, nm, x, z, lowest[0], worst))
    print("toriiclear: %d walk-through torii below %.2f m" % (bad, NEED))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
