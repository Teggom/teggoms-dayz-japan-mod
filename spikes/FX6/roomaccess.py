"""FX6 room-access check (Stephen's 3c-1 walk, 2026-10-02: "the room next to it has a large table in the middle; I
cannot enter the room").

For every room of a furnished building (buildings/<dir>/rooms/<key>.json + the built MLOD in buildings/<dir>/out):
a player capsule (0.60 m wide = radius 0.30, 1.90 m tall) must walk from EACH door of the room into the room, past
the building's own Geometry and every prop's Geometry (the proxies' masters, placed). Obstacles are the Geometry
components clipped to the body band (floor + 0.35 .. floor + 1.90; lower things are stepped over or are the floor),
projected to plan, rasterised (4 cm) and grown by the capsule radius. Door leaves are left out (open; the door sweep
checks D6 / C7 judge the leaves). From each door the capsule starts 0.45 m inside the doorway's centre (the nearest
free cell within 0.35 m of it) and floods the room.
A room PASSES when, from every door, the reachable floor inside the room is >= 50 % of the room's free floor (cells a
capsule can stand on) and >= min(1.0 m2, that free floor), and every door of the room reaches every other.
Rooms with no doors (open sides, verandas) are skipped (listed).

  python spikes/FX6/roomaccess.py [record.json ...]     default: the 3c-1 furnished set (buildings/ts_furnished)
  python spikes/FX6/roomaccess.py --all                 every furnished variant with a rooms file
"""
import glob
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "buildings")):
    if p not in sys.path:
        sys.path.insert(0, p)
from jpparts import mlod, proxies as PX, decor as DC, checks as C  # noqa: E402

R_CAP = 0.30
STEP_OVER = 0.35
HEAD = 1.90
CELL = 0.04
INSET = 0.45
_PM = {}


def lodn(lods, name):
    return next((l for l in lods if mlod.lod_name(l.resolution) == name), None)


def prop_geo(stem, path):
    if stem not in _PM:
        g = lodn(mlod.read_mlod(path), "Geometry")
        _PM[stem] = [np.array(c["pts"], float) for c in C.components(g)] if g else []
    return _PM[stem]


def footprint(P, y0, y1):
    """Plan polygon (convex hull) of the convex hull of points P clipped to y0 <= y <= y1; None if empty."""
    ins = [p for p in P if y0 <= p[1] <= y1]
    pts = [(p[0], p[2]) for p in ins]
    for yc in (y0, y1):
        lo = P[P[:, 1] < yc]
        hi = P[P[:, 1] > yc]
        for a in lo:
            for b in hi:
                t = (yc - a[1]) / (b[1] - a[1])
                pts.append((a[0] + t * (b[0] - a[0]), a[2] + t * (b[2] - a[2])))
    if len(pts) < 3:
        return None
    pts = sorted(set((round(x, 4), round(z, 4)) for x, z in pts))
    if len(pts) < 3:
        return None

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo_, up = [], []
    for p in pts:
        while len(lo_) >= 2 and cr(lo_[-2], lo_[-1], p) <= 0:
            lo_.pop()
        lo_.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    H = lo_[:-1] + up[:-1]
    return H if len(H) >= 3 else None


def raster(poly, X, Z):
    """Mask of grid points (X, Z) inside the convex polygon (CCW)."""
    m = np.ones(X.shape, bool)
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        m &= ((b[0] - a[0]) * (Z - a[1]) - (b[1] - a[1]) * (X - a[0])) >= -1e-9
    return m


def dilate(B, r_cells):
    out = B.copy()
    R = int(math.ceil(r_cells))
    for dx in range(-R, R + 1):
        for dz in range(-R, R + 1):
            if dx * dx + dz * dz > r_cells * r_cells:
                continue
            sh = np.zeros_like(B)
            xs = slice(max(dx, 0), B.shape[0] + min(dx, 0))
            xd = slice(max(-dx, 0), B.shape[0] + min(-dx, 0))
            zs = slice(max(dz, 0), B.shape[1] + min(dz, 0))
            zd = slice(max(-dz, 0), B.shape[1] + min(-dz, 0))
            sh[xd, zd] = B[xs, zs]
            out |= sh
    return out


def flood(free, start):
    seen = np.zeros_like(free)
    if not free[start]:
        return seen
    st = [start]
    seen[start] = True
    nx, nz = free.shape
    while st:
        i, j = st.pop()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < nx and 0 <= b < nz and free[a, b] and not seen[a, b]:
                seen[a, b] = True
                st.append((a, b))
    return seen


def check(rec_path, verbose=True):
    rec = json.load(open(rec_path, encoding="utf-8"))
    d = os.path.dirname(os.path.dirname(rec_path))
    rooms_p = os.path.join(d, "rooms", os.path.basename(rec_path))
    mp = os.path.join(d, "out", rec["name"] + ".p3d")
    if not (os.path.exists(rooms_p) and os.path.exists(mp)):
        return None
    rooms = json.load(open(rooms_p, encoding="utf-8"))["rooms"]
    twin_bones = {}
    for m in re.finditer(r'source="(DoorsTwin\d+)";\s*selection="(doors\d+)"', rec.get("cfgmodel", "")):
        twin_bones.setdefault(m.group(1), set()).add(m.group(2))
    lods = mlod.read_mlod(mp)
    g = lodn(lods, "Geometry")
    comps = C.components(PX.strip(g))
    obst = [np.array(c["pts"], float) for c in comps if not c["door"]]
    leaves = {}
    for c in comps:
        if c["door"]:
            leaves.setdefault(c["door"], []).append(c["bbox"])
    cat = DC.catalog()
    for name, o, up, fw in PX.listed(g):
        stem = re.split(r"[\\/]", name.split(":", 1)[1].rsplit(".", 1)[0])[-1].lower()
        inf = cat.get(stem)
        if not inf or not inf.get("master") or not os.path.exists(inf["master"]):
            continue
        yaw = math.degrees(math.atan2(fw[0], fw[2]))
        r, u, f = PX.frame(yaw)
        Rm = np.array([r, u, f])
        for P in prop_geo(stem, inf["master"]):
            obst.append(P @ Rm + np.array(o))
    out = []
    for rm in rooms:
        x0, x1, z0, z1 = rm["rect_model"]
        fy = rm["level_m"]
        doors = [dn for dn in rm.get("doors", []) if dn in twin_bones]
        if not doors:
            out.append((rm["name"], None, "no doors (open sides): skipped"))
            continue
        pad = 0.8
        xs = np.arange(x0 - pad, x1 + pad + 1e-9, CELL)
        zs = np.arange(z0 - pad, z1 + pad + 1e-9, CELL)
        X, Z = np.meshgrid(xs, zs, indexing="ij")
        B = np.zeros(X.shape, bool)
        for P in obst:
            if P[:, 1].max() < fy + STEP_OVER or P[:, 1].min() > fy + HEAD:
                continue
            if P[:, 0].max() < xs[0] - 0.5 or P[:, 0].min() > xs[-1] + 0.5 or P[:, 2].max() < zs[0] - 0.5 or \
                    P[:, 2].min() > zs[-1] + 0.5:
                continue
            poly = footprint(P, fy + STEP_OVER, fy + HEAD)
            if poly:
                B |= raster(poly, X, Z)
        free = ~dilate(B, R_CAP / CELL)
        inroom = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
        room_free = (free & inroom).sum() * CELL * CELL
        res = []
        reached = {}
        for dn in doors:
            bbs = [b for bn in twin_bones[dn] for b in leaves.get(bn, [])]
            if not bbs:
                continue
            bx = (min(b[0] for b in bbs), max(b[1] for b in bbs), min(b[4] for b in bbs), max(b[5] for b in bbs))
            along_x = (bx[1] - bx[0]) >= (bx[3] - bx[2])
            if along_x:
                c = ((bx[0] + bx[1]) / 2, (bx[2] + bx[3]) / 2)
                inward = (0.0, 1.0 if (z0 + z1) / 2 > c[1] else -1.0)
            else:
                c = ((bx[0] + bx[1]) / 2, (bx[2] + bx[3]) / 2)
                inward = (1.0 if (x0 + x1) / 2 > c[0] else -1.0, 0.0)
            s = (c[0] + inward[0] * INSET, c[1] + inward[1] * INSET)
            dd = (X - s[0]) ** 2 + (Z - s[1]) ** 2
            cand = np.where(free & (dd <= 0.35 ** 2))
            if not len(cand[0]):
                res.append((dn, 0.0, "no room for the capsule 0.45 m inside the doorway (%.2f, %.2f)" % s))
                reached[dn] = np.zeros_like(free)
                continue
            k = int(np.argmin(dd[cand]))
            seen = flood(free, (cand[0][k], cand[1][k]))
            reached[dn] = seen
            a = (seen & inroom).sum() * CELL * CELL
            res.append((dn, a, "reaches %.2f of %.2f m2" % (a, room_free)))
        ok = True
        why = []
        for dn, a, msg in res:
            need = min(1.0, room_free)
            if a < max(0.5 * room_free, need) - 1e-9:
                ok = False
                why.append("%s: %s (needs >= %.2f)" % (dn, msg, max(0.5 * room_free, need)))
            else:
                why.append("%s: %s" % (dn, msg))
        for i in range(len(doors)):
            for j in range(i + 1, len(doors)):
                a, b = doors[i], doors[j]
                if a in reached and b in reached and not (reached[a] & reached[b]).any():
                    ok = False
                    why.append("%s and %s do not meet" % (a, b))
        out.append((rm["name"], ok, "; ".join(why)))
    if verbose:
        for nm, ok, msg in out:
            print("  %-4s %-10s %s" % ("skip" if ok is None else ("PASS" if ok else "FAIL"), nm, msg))
    return out


def main(argv):
    if "--all" in argv:
        recs = sorted(glob.glob(os.path.join(DEV, "buildings", "*", "records", "*.json")))
        recs = [r for r in recs if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(r)), "rooms",
                                                               os.path.basename(r)))]
    else:
        recs = [a for a in argv if a.endswith(".json")] or sorted(
            glob.glob(os.path.join(DEV, "buildings", "ts_furnished", "records", "*.json")))
    nb = nf = 0
    for r in recs:
        print(os.path.basename(r))
        res = check(r)
        if res is None:
            print("  (no rooms / MLOD)")
            continue
        nb += 1
        f = sum(1 for x in res if x[1] is False)
        nf += f
    print("ROOMACCESS: %d buildings, %d rooms failing" % (nb, nf))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
