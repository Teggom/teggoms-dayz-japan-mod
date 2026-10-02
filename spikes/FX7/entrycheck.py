"""FX7 entry check (Stephen's 3d walk, 2026-10-02: "the spiky-fence building sits higher on the ground than the other
buildings; I can't walk in, I need to jump").

For every placed building / compound on the island (test/placements/*.csv rows whose MLOD is in buildings/*/out):
a 2.5D walk map on a 0.10 m world grid around it, built from the real terrain (terrain_sh1.ground) and the Geometry
of the object AND every placed neighbour (their proxies' masters included; door leaves left out = open):
  - a cell's standing height h = the highest top of a walkable component (both plan sides >= 0.20 m) that is at most
    1.40 m over the terrain there, else the terrain (upper floors / roofs are overhead);
  - a cell is blocked when any component occupies the body band (h + STEP_MAX .. h + 1.75) there; blocked cells are
    grown by the capsule radius (0.25 m);
  - moves are 4-neighbour; a move up of more than STEP_MAX is a jump. The cost of a route = its largest single rise.
Checks (minimax route, Dijkstra):
  ROOMS  (objects with a rooms file): from the terrain at the window's edge (3 m round the object) to each room at its
         floor level (rooms over 1.5 m = upper floors: skipped). FAIL when the best route needs a rise > STEP_MAX.
  GATES  (objects without a rooms file, with door leaves = compound gates): through each gate, from 1.2 m outside its
         leaves to 1.2 m inside (towards the object's origin), inside a 5 m window. FAIL as above.
STEP_MAX = 0.30 m (the brief's DayZ step-up; the kit's verandas use two 0.25 rises, walked in game since D3).

  python spikes/FX7/entrycheck.py [--only W3D,W3C2] [--id <stem substring>] [-v]
"""
import csv
import glob
import heapq
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "buildings"), os.path.join(DEV, "spikes", "SH1")):
    if p not in sys.path:
        sys.path.insert(0, p)
from jpparts import mlod, proxies as PX, decor as DC, checks as C  # noqa: E402
import terrain_sh1 as T  # noqa: E402

STEP_MAX = 0.30
CELL = 0.10
RAD = 0.25
BODY = 1.75
SURF_MAX = 1.40
MIN_SIDE = 0.0
MARGIN = 3.0
_CACHE = {}


def lodn(lods, name):
    return next((l for l in lods if mlod.lod_name(l.resolution) == name), None)


def comps_of(path, with_proxies=True):
    """[(planes nx,ny,nz,d array, bbox, walkable, door)] in the model frame (proxies' masters folded in)."""
    key = (path, with_proxies)
    if key in _CACHE:
        return _CACHE[key]
    out = []
    lods = mlod.read_mlod(path)
    g = lodn(lods, "Geometry")
    if g is None:
        _CACHE[key] = out
        return out
    for c in C.components(PX.strip(g)):
        out.append(_pack(c["planes"], c["bbox"], c["door"]))
    if with_proxies:
        cat = DC.catalog()
        for name, o, up, fw in PX.listed(g):
            stem = re.split(r"[\\/]", name.split(":", 1)[1].rsplit(".", 1)[0])[-1].lower()
            inf = cat.get(stem)
            if not inf or not inf.get("master") or not os.path.exists(inf["master"]):
                continue
            yaw = math.degrees(math.atan2(fw[0], fw[2]))
            for pl, bb, wk, dr in comps_of(inf["master"], False):
                out.append(_move(pl, bb, wk, yaw, o))
    _CACHE[key] = out
    return out


def _pack(planes, bb, door):
    pl = np.array([[n[0], n[1], n[2], d] for n, d in planes], float)
    walk = (bb[1] - bb[0]) >= MIN_SIDE and (bb[5] - bb[4]) >= MIN_SIDE
    return pl, bb, walk, door


def _move(pl, bb, walk, yaw, o):
    """Planes / bbox of a component turned by yaw (clockwise from +z) and moved to o (model frame of the parent)."""
    a = math.radians(yaw)
    c, s = math.cos(a), math.sin(a)
    n = pl[:, :3]
    # p_parent = (x c + z s, y, -x s + z c) + o
    nn = np.stack([n[:, 0] * c + n[:, 2] * s, n[:, 1], -n[:, 0] * s + n[:, 2] * c], 1)
    d = pl[:, 3] + nn @ np.array(o, float)
    xs, zs = [], []
    for x in (bb[0], bb[1]):
        for z in (bb[4], bb[5]):
            xs.append(x * c + z * s + o[0])
            zs.append(-x * s + z * c + o[2])
    nb = (min(xs), max(xs), bb[2] + o[1], bb[3] + o[1], min(zs), max(zs))
    return np.concatenate([nn, d[:, None]], 1), nb, walk, None


def to_model(WX, WZ, pos, yaw):
    a = math.radians(yaw)
    c, s = math.cos(a), math.sin(a)
    dx, dz = WX - pos[0], WZ - pos[2]
    return dx * c - dz * s, dx * s + dz * c


def to_world(mx, mz, pos, yaw):
    a = math.radians(yaw)
    c, s = math.cos(a), math.sin(a)
    return pos[0] + mx * c + mz * s, pos[2] - mx * s + mz * c


def interval(pl, X, Z):
    lo = np.full(X.shape, -1e9)
    hi = np.full(X.shape, 1e9)
    ok = np.ones(X.shape, bool)
    for nx, ny, nz, d in pl:
        rhs = d - nx * X - nz * Z
        if ny > 1e-6:
            lo = np.maximum(lo, rhs / ny)
        elif ny < -1e-6:
            hi = np.minimum(hi, rhs / ny)
        else:
            ok &= rhs <= 1e-6
    ok &= hi > lo + 1e-4
    return ok, lo, hi


# ------------------------------------------------------------------------------------------------ the placed island
def index_records():
    idx = {}
    for r in glob.glob(os.path.join(DEV, "buildings", "*", "records", "*.json")):
        try:
            rec = json.load(open(r, encoding="utf-8"))
        except Exception:
            continue
        d = os.path.dirname(os.path.dirname(r))
        nm = rec.get("name")
        if not nm:
            continue
        mp = os.path.join(d, "out", nm + ".p3d")
        rp = os.path.join(d, "rooms", os.path.basename(r))
        if os.path.exists(mp):
            idx[(os.path.basename(d).lower(), nm.lower())] = (mp, rp if os.path.exists(rp) else None)
    return idx


def placements(only=None):
    idx = index_records()
    rows = []
    for f in sorted(glob.glob(os.path.join(DEV, "test", "placements", "*.csv"))):
        wave = os.path.splitext(os.path.basename(f))[0]
        for r in csv.DictReader(open(f, encoding="utf-8")):
            parts = re.split(r"[\\/]", r["p3d"])
            if len(parts) < 4 or parts[1].lower() != "buildings":
                continue
            k = (parts[2].lower(), os.path.splitext(parts[3])[0].lower())
            if k not in idx:
                continue
            x, z, yaw, yo = float(r["x"]), float(r["z"]), float(r["yaw_deg"]), float(r["y_offset"])
            seat = T.ground(x, z) + yo
            rows.append(dict(wave=wave, stem=k[1], mlod=idx[k][0], rooms=idx[k][1], pos=(x, seat, z), yaw=yaw))
    for r in rows:
        cs = comps_of(r["mlod"])
        xs, zs = [], []
        for _, bb, _, _ in cs:
            for x in (bb[0], bb[1]):
                for z in (bb[4], bb[5]):
                    w = to_world(x, z, r["pos"], r["yaw"])
                    xs.append(w[0])
                    zs.append(w[1])
        r["wbb"] = (min(xs), max(xs), min(zs), max(zs)) if xs else None
    rows = [r for r in rows if r["wbb"]]
    return rows, [r for r in rows if not only or r["wave"] in only]


# ------------------------------------------------------------------------------------------------ the walk map
def walkmap(win, rows):
    x0, x1, z0, z1 = win
    xs = np.arange(x0, x1 + 1e-9, CELL)
    zs = np.arange(z0, z1 + 1e-9, CELL)
    WX, WZ = np.meshgrid(xs, zs, indexing="ij")
    tg = ground_grid(WX, WZ)
    ivs = []          # (mask, lo, hi, walk) in world y
    for r in rows:
        b = r["wbb"]
        if b[1] < x0 or b[0] > x1 or b[3] < z0 or b[2] > z1:
            continue
        MX, MZ = to_model(WX, WZ, r["pos"], r["yaw"])
        for pl, bb, walk, door in comps_of(r["mlod"]):
            if door:
                continue
            sel = (MX >= bb[0] - 0.01) & (MX <= bb[1] + 0.01) & (MZ >= bb[4] - 0.01) & (MZ <= bb[5] + 0.01)
            if not sel.any():
                continue
            ii = np.where(sel)
            ok, lo, hi = interval(pl, MX[ii], MZ[ii])
            if not ok.any():
                continue
            ivs.append(((ii[0][ok], ii[1][ok]), lo[ok] + r["pos"][1], hi[ok] + r["pos"][1], walk))
    h = tg.copy()
    for (ia, ib), lo, hi, walk in ivs:
        if not walk:
            continue
        t = tg[ia, ib]
        good = (hi <= t + SURF_MAX) & (hi > h[ia, ib])
        np.maximum.at(h, (ia[good], ib[good]), hi[good])
    B = np.zeros(h.shape, bool)
    OH = np.full(h.shape, -1e9)        # the blocking things' top / bottom per cell (for the height-aware growth)
    OL = np.full(h.shape, 1e9)
    for (ia, ib), lo, hi, walk in ivs:
        hh = h[ia, ib]
        blk = (lo < hh + BODY) & (hi > hh + STEP_MAX)
        B[ia[blk], ib[blk]] = True
        np.maximum.at(OH, (ia[blk], ib[blk]), hi[blk])
        np.minimum.at(OL, (ia[blk], ib[blk]), lo[blk])
    # grow by the capsule radius, height-aware: a blocking thing next to a cell only blocks it when it stands in
    # THAT cell's body band (a raised floor's edge boards do not close the hidden ramp running up to them)
    r_c = int(round(RAD / CELL))
    D = B.copy()
    for dx in range(-r_c, r_c + 1):
        for dz in range(-r_c, r_c + 1):
            if dx * dx + dz * dz > r_c * r_c or (dx == 0 and dz == 0):
                continue
            rb = np.roll(np.roll(B, dx, 0), dz, 1)
            rh = np.roll(np.roll(OH, dx, 0), dz, 1)
            rl = np.roll(np.roll(OL, dx, 0), dz, 1)
            D |= rb & (rh > h + STEP_MAX) & (rl < h + BODY)
    return WX, WZ, tg, h, D


def ground_grid(X, Z):
    """terrain.bilinear over arrays (the same interpolation as terrain_sh1.ground)."""
    TT = T.terrain
    hm = np.asarray(T.H(), float)
    fx, fz = X / TT.CELL, Z / TT.CELL
    i = np.clip(np.floor(fx).astype(int), 0, TT.N - 2)
    j = np.clip(np.floor(fz).astype(int), 0, TT.N - 2)
    u, v = fx - i, fz - j
    return (hm[j, i] * (1 - u) * (1 - v) + hm[j, i + 1] * u * (1 - v) + hm[j + 1, i] * (1 - u) * v
            + hm[j + 1, i + 1] * u * v)


def minimax(h, blocked, starts, allowed=None):
    INF = 1e9
    cost = np.full(h.shape, INF)
    pq = []
    for s in starts:
        if not blocked[s]:
            cost[s] = 0.0
            pq.append((0.0, s[0], s[1]))
    heapq.heapify(pq)
    nx, nz = h.shape
    while pq:
        c, i, j = heapq.heappop(pq)
        if c > cost[i, j]:
            continue
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if a < 0 or b < 0 or a >= nx or b >= nz or blocked[a, b]:
                continue
            if allowed is not None and not allowed[a, b]:
                continue
            nc = max(c, h[a, b] - h[i, j])
            if nc < cost[a, b] - 1e-9:
                cost[a, b] = nc
                heapq.heappush(pq, (nc, a, b))
    return cost


def check_row(r, rows, verbose=False):
    b = r["wbb"]
    win = (b[0] - MARGIN, b[1] + MARGIN, b[2] - MARGIN, b[3] + MARGIN)
    WX, WZ, tg, h, D = walkmap(win, rows)
    res = []
    if r["rooms"]:
        border = np.zeros(h.shape, bool)
        border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
        st = list(zip(*np.where(border & ~D & (np.abs(h - tg) < 0.02))))
        cost = minimax(h, D, st)
        MX, MZ = to_model(WX, WZ, r["pos"], r["yaw"])
        for rm in json.load(open(r["rooms"], encoding="utf-8"))["rooms"]:
            lvl = rm["level_m"]
            if lvl > 1.5:
                continue
            x0, x1, z0, z1 = rm["rect_model"]
            inr = (MX >= x0) & (MX <= x1) & (MZ >= z0) & (MZ <= z1) & ~D & \
                  (np.abs(h - (r["pos"][1] + lvl)) < 0.08)
            if not inr.any():
                res.append(("room " + rm["name"], None, "no free cell at its floor %.2f" % lvl))
                continue
            c = float(cost[inr].min())
            res.append(("room " + rm["name"], c, "floor %.2f" % lvl))
    else:
        g = lodn(mlod.read_mlod(r["mlod"]), "Geometry")
        groups = {}
        for c in C.components(PX.strip(g)):
            if c["door"]:
                groups.setdefault(re.sub(r"\D", "", c["door"]), []).append(c["bbox"])
        gates = {}
        for k, bbs in groups.items():   # leaves of one gate: within 3 m of each other
            cx = (min(bb[0] for bb in bbs) + max(bb[1] for bb in bbs)) / 2
            cz = (min(bb[4] for bb in bbs) + max(bb[5] for bb in bbs)) / 2
            gates.setdefault((round(cx / 3.0), round(cz / 3.0)), []).extend(bbs)
        for gk, bbs in gates.items():
            bx = (min(bb[0] for bb in bbs), max(bb[1] for bb in bbs), min(bb[4] for bb in bbs), max(bb[5] for bb in bbs))
            cx, cz = (bx[0] + bx[1]) / 2, (bx[2] + bx[3]) / 2
            if (bx[1] - bx[0]) >= (bx[3] - bx[2]):
                nrm = (0.0, -1.0 if cz > 0 else 1.0)
            else:
                nrm = (-1.0 if cx > 0 else 1.0, 0.0)
            pin = to_world(cx + 1.2 * nrm[0], cz + 1.2 * nrm[1], r["pos"], r["yaw"])
            pout = to_world(cx - 1.2 * nrm[0], cz - 1.2 * nrm[1], r["pos"], r["yaw"])
            gc = to_world(cx, cz, r["pos"], r["yaw"])
            allowed = (np.abs(WX - gc[0]) <= 2.5) & (np.abs(WZ - gc[1]) <= 2.5)
            dout = (WX - pout[0]) ** 2 + (WZ - pout[1]) ** 2
            din = (WX - pin[0]) ** 2 + (WZ - pin[1]) ** 2
            st = list(zip(*np.where((dout <= 0.4 ** 2) & ~D)))
            tgt = (din <= 0.4 ** 2) & ~D
            if not st or not tgt.any():
                res.append(("gate (%.1f, %.1f)" % gc, None, "no free cell at a probe"))
                continue
            cost = minimax(h, D, st, allowed)
            c = float(cost[tgt].min())
            res.append(("gate (%.1f, %.1f)" % gc, c, "out %.2f -> in %.2f over the terrain at the probes" % (
                float(h[np.unravel_index(np.argmin(np.where(dout <= 0.16, dout, 9e9)), h.shape)]),
                float(h[np.unravel_index(np.argmin(np.where(din <= 0.16, din, 9e9)), h.shape)]))))
    return res


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    sub = argv[argv.index("--id") + 1].lower() if "--id" in argv else None
    verbose = "-v" in argv
    rows, targets = placements(only)
    nb = nf = 0
    fails = []
    for r in targets:
        if sub and sub not in r["stem"]:
            continue
        res = check_row(r, rows, verbose)
        if not res:
            continue
        nb += 1
        bad = [x for x in res if x[1] is None or x[1] > STEP_MAX + 1e-6]
        tag = "FAIL" if bad else "ok"
        at = "(%.1f, %.1f)" % (r["pos"][0], r["pos"][2])
        print("%-5s %-4s %-44s %s" % (r["wave"], tag, r["stem"], at))
        for nm, c, msg in (res if (verbose or bad) else []):
            print("        %-22s %s  %s" % (nm, "unreached" if c is None or c > 1e8 else "max rise %.2f" % c, msg))
        if bad:
            nf += 1
            fails.append((r["wave"], r["stem"], at, ["%s %s" % (n, "unreached" if c is None or c > 1e8 else
                                                               "%.2f" % c) for n, c, _ in bad]))
    print("ENTRYCHECK: %d objects, %d with an entry over %.2f m" % (nb, nf, STEP_MAX))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
