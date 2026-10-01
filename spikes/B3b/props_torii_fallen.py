"""FP1 (2026-10-01, Stephen: 'fully collapsed torii, 1-2 per type'): torii that have come down, for ruined and
abandoned shrines. jp_site, folder shrine, mount 'shrine'; dimensions from props_torii (WOOD_FORMS / STONE_FORMS).

Causes and era (general knowledge; recorded in spikes/FP1/FP1_PROGRESS.md 'Forms'):
- Wooden torii rot at the foot first, where the post meets the damp ground and the footing stone: the post breaks a
  hand above the stone and the frame falls; a typhoon (nowaki) blows a weakened torii over in one piece. Both are
  ordinary sights by 1730 (unpainted torii were renewed every few decades; neglected ones fell).
- Vermilion (shu) torii rot the same way under the paint; one post snapping lets the kasagi fall from it.
- Stone torii fall in earthquakes: the Genroku quake (1703) and the Hoei quake (1707) both toppled stone monuments
  across the Kanto and Tokai; the posts break into drums, the one-piece kasagi breaks in two or three, the dome bases
  (kamebara) stay in place. A collapse decades old: moss, leaf litter, pieces sunk into the soil.
Frame: origin = the centre between the two post feet, +z = the approach. Each lying piece has its own convex
collision (Geometry + View + Fire); splinters, moss and litter are visual only.
"""
import math
import random

import skit
from skit import (core, xf, xfs, W, col, SPart, pole, add_all, CARVED, FIELD, WOOD, KURO, LITTER, litter, moss_top,
                  hull3)
from props_wood import M
import w2kit as K
from w2kit import SHU
import props_torii as T

ROT = "wood_sooted"            # rotten, black wood at a break
LEAF = "ground_leaf_litter"


def Ww(x0, x1, y0, y1, z0, z1, mat, vis=(1, 2), wear=None):
    s = W(x0, x1, y0, y1, z0, z1, mat, vis=vis)
    if wear:
        s.wear = wear
    return s


def place(ss, rx=0.0, ry=0.0, rz=0.0, at=(0.0, 0.0), sink=0.03, cols=()):
    """Turn a member group (built about its own origin) and lay it on the ground at (x, z): the lowest visual point
    `sink` below the terrain (pieces settle in). Collision solids follow the same move."""
    vs = [xf(s, rx=rx, ry=ry, rz=rz) for s in ss]
    cs = [xf(s, rx=rx, ry=ry, rz=rz) for s in cols]
    lo = min(v[1] for s in vs if s.vis for v in s.verts)
    t = (at[0], -sink - lo, at[1])
    return [xf(s, t=t) for s in vs], [xf(s, t=t) for s in cs]


def splinters(p, d, r, seed, mat=WOOD, wear="_w2", n=5, length=(0.06, 0.16)):
    """A snapped / rotted end at p (axis direction d): jagged splinters standing out of the break."""
    rg = random.Random(seed)
    d = core.norm(d)
    ref = (0.0, 1.0, 0.0) if abs(d[1]) < 0.9 else (1.0, 0.0, 0.0)
    a1 = core.norm(core.cross(d, ref))
    a2 = core.norm(core.cross(d, a1))
    out = []
    for k in range(n):
        th = 2 * math.pi * k / n + rg.uniform(-0.4, 0.4)
        o = core.add(core.mul(a1, math.cos(th) * r * rg.uniform(0.3, 0.8)), core.mul(a2, math.sin(th) * r * rg.uniform(0.3, 0.8)))
        p0 = core.add(p, core.add(o, core.mul(d, -0.03)))
        L = rg.uniform(*length)
        p1 = core.add(p0, core.add(core.mul(d, L), core.mul(o, 0.3)))
        out.append(pole(p0, p1, r * rg.uniform(0.18, 0.32), mat, n=3, vis=(1,), r1=0.004, wear=wear))
    return out


def post(L, r, mat, top_break=False, foot_rot=True, seed=1, n=8, wear="_w2", rot_mat=ROT):
    """A round post along +y from 0 to L, tapering, its foot rotten black (a band) and its top snapped (splinters)."""
    out = [pole((0.0, 0.0, 0.0), (0.0, L, 0.0), r, mat, n=n, vis=(1,), r1=r * 0.95, wear=wear),
           pole((0.0, 0.0, 0.0), (0.0, L, 0.0), r, mat, n=5, vis=(2, 3), wear=wear)]
    if foot_rot:
        out.append(pole((0.0, -0.002, 0.0), (0.0, 0.22, 0.0), r * 1.02, rot_mat, n=n, vis=(1,), wear="_w2"))
    if top_break:
        out += splinters((0.0, L, 0.0), (0.0, 1.0, 0.0), r, seed, mat=rot_mat if foot_rot else mat)
    c = core.cyl("y", 0.0, 0.0, r * 0.95, 0.0, L, mat, n=8, vis=(), geo=True, view=True, fire=True)
    return out, [c]


def stump(x, h, r, mat, seed, wear="_w2"):
    """A rotted post stump standing on its footing: h tall, black and splintered at the top."""
    out = [pole((x, -0.06, 0.0), (x, h, 0.0), r, mat, n=8, vis=(1, 2, 3), wear=wear),
           pole((x, h - 0.12, 0.0), (x, h + 0.002, 0.0), r * 1.01, ROT, n=8, vis=(1,), wear="_w2")]
    out += splinters((x, h, 0.0), (0.0, 1.0, 0.0), r, seed, mat=ROT, n=6, length=(0.08, 0.22))
    return out, [core.cyl("y", x, 0.0, r * 0.95, 0.0, h, mat, n=8, vis=(), geo=True, view=True, fire=True)]


def beam_piece(x0, x1, h, d, mat, broken_end=None, seed=1, wear="_w2", y=0.0):
    """A straight rectangular beam piece along x (tie-beam / a straight kasagi part), centred on y; broken_end:
    'x0' / 'x1' gets splinters."""
    out = [Ww(x0, x1, y - h / 2, y + h / 2, -d / 2, d / 2, mat, vis=(1, 2, 3), wear=wear)]
    if broken_end:
        xe = x0 if broken_end == "x0" else x1
        out += splinters((xe, y, 0.0), (-1.0 if broken_end == "x0" else 1.0, 0.0, 0.0), min(h, d) * 0.6, seed,
                         mat=mat, n=4, length=(0.05, 0.12))
    return out, [col(x0, x1, y - h / 2, y + h / 2, -d / 2, d / 2, mat)]


def curved_piece(cl, kh, kd, sh_h, sh_d, mat, top_mat, wear="_w2", shimaki=True, top_w=None):
    """A kasagi piece (and the shimaki under it) along the centre-line slice cl [(x, y)] (myojin forms)."""
    out = [K.sweep(cl, kh, kd, top_mat, vis=(1,), top_w=top_w or kd * 1.15), K.sweep(cl[::2] if len(cl) > 2 else cl,
                                                                                     kh, kd, top_mat, vis=(2, 3))]
    if shimaki:
        scl = [(x, y - kh / 2 - sh_h / 2) for x, y in cl]
        out += [K.sweep(scl, sh_h, sh_d, mat, vis=(1,)), K.sweep(scl[::2] if len(scl) > 2 else scl, sh_h, sh_d, mat,
                                                                   vis=(2,))]
    for s in out:
        s.wear = wear
    vs = [v for s in out for v in s.verts]
    xs, ys, zs = [v[0] for v in vs], [v[1] for v in vs], [v[2] for v in vs]
    return out, [col(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs), mat)]   # local box -> oriented once placed


def moss_on(ss, seed, wear="_w2", k=2):
    """Moss patches on the top of a lying group (decals 3 mm above its highest faces)."""
    rg = random.Random(seed)
    vs = [v for s in ss if s.vis for v in s.verts]
    xs, zs = [v[0] for v in vs], [v[2] for v in vs]
    ytop = max(v[1] for v in vs)
    out = []
    for i in range(k):
        x = rg.uniform(min(xs) * 0.7 + max(xs) * 0.3, min(xs) * 0.3 + max(xs) * 0.7)
        z = rg.uniform(min(zs) * 0.6 + max(zs) * 0.4, min(zs) * 0.4 + max(zs) * 0.6)
        # the patch lies on the piece's top near (x, z): the highest vertex within 0.25 m
        near = [v[1] for v in vs if abs(v[0] - x) < 0.25 and abs(v[2] - z) < 0.25]
        out.append(moss_top(seed + i, x, z, 0.10, (max(near) if near else ytop) - 0.005, wear=wear, sx=1.4, sz=0.6))
    return out


def leaf_drifts(P, seed, spots):
    for k, (x, z, r) in enumerate(spots):
        P.add(litter(seed + k, x, z, r, sx=1.4))
        from bits import stain
        P.add(stain(seed + 20 + k, x + 0.25, z - 0.15, r * 0.6, y=0.007, mat=LITTER, wear="_w2", sx=1.2))  # denser drift


# ------------------------------------------------------------------------------------------------ wooden
def fallen_wood(form, kind):
    F = T.WOOD_FORMS[form]
    S, H, r = F["S"], F["H"], F["r"]
    shu = kind == "shu_snapped"
    mat = SHU if shu else WOOD
    top_mat = KURO if shu else mat
    P = SPart("torii_fallen", budget="medium", res3=True, mass=900.0, bury=0.15)
    P.wear = "_w2"
    vis, cols = [], []
    L = S + 2 * F["over"]
    nh, nd = F["nuki"]
    for sx in (-1, 1):
        vis.append(T.footing(sx * S / 2, 7 + sx, r, wear="_w2"))
    if form == "shinmei" and kind == "rot":
        # both posts rotted at the foot: the left one still stands as a 0.38 m stump, the right fell forward whole;
        # the round kasagi broke in two, the tie-beam lies across the fallen post
        v, c = stump(-S / 2, 0.38, r, mat, 31)
        vis += v
        cols += c
        pv, pc = post(H - 0.30, r, mat, top_break=False, seed=32)
        v, c = place(pv, rx=90.0, ry=12.0, at=(S / 2 + 0.05, 0.25), cols=pc)
        vis += v
        cols += c
        vis += moss_on(v, 33)
        for i, (x0, x1, at, yaw, flip) in enumerate(((-L / 2, 0.15, (-0.7, 1.6), 18.0, 0.0),
                                                     (0.15, L / 2, (1.85, 1.9), -35.0, 180.0))):
            kv = [pole((x0, 0.0, 0.0), (x1, 0.0, 0.0), 0.10, mat, n=8, vis=(1,), wear="_w2"),
                  pole((x0, 0.0, 0.0), (x1, 0.0, 0.0), 0.10, mat, n=5, vis=(2, 3), wear="_w2")]
            kv += splinters((0.15, 0.0, 0.0), (1.0 if i == 0 else -1.0, 0.0, 0.0), 0.10, 34 + i, mat=ROT)
            kc = [core.cyl("x", 0.0, 0.0, 0.095, x0, x1, mat, n=8, vis=(), geo=True, view=True, fire=True)]
            mid = (x0 + x1) / 2
            kv = xfs(kv, t=(-mid, 0.0, 0.0))
            kc = xfs(kc, t=(-mid, 0.0, 0.0))
            v, c = place(kv, rx=flip, ry=yaw, at=at, cols=kc)
            vis += v + moss_on(v, 36 + i, k=1)
            cols += c
        bv, bc = beam_piece(-S / 2 - 0.05, S / 2 + 0.05, nh, nd, mat, broken_end="x1", seed=38)
        v, c = place(bv, ry=-8.0, at=(-0.55, 3.05), cols=bc, sink=0.01)
        vis += v
        cols += c
        leaf_drifts(P, 400, ((0.0, 0.8, 1.2), (-0.9, 1.9, 0.7), (1.3, 0.2, 0.6)))
        P.notes.append("wooden shinmei torii rotted through at the feet (moss, leaves): one stump, the rest down")
    elif kind == "typhoon":
        # a myojin blown over backwards in one piece: both posts snapped just above their footings and lie side by side
        # behind; the kasagi + shimaki tore off the post tops and broke in two; the tie-beam snapped in the middle
        for sx in (-1, 1):
            v, c = stump(sx * S / 2, 0.20 + 0.06 * sx, r, mat, 41 + sx)
            vis += v
            cols += c
            pv, pc = post(F["nuki_y"] + 0.55, r, mat, top_break=False, seed=43 + sx, foot_rot=True)
            v, c = place(pv, rx=-90.0, ry=4.0 * sx, at=(sx * (S / 2 - 0.04), -0.35), cols=pc)
            vis += v
            cols += c
        kh, kd = 0.16, 0.22
        sh_h, sh_d = 0.12, 0.17
        cl = K.curve(-L / 2, L / 2, 0.0, F["rise"], n=8)
        for half, sl, at, yaw, roll in ((0, slice(0, 5), (-0.9, -4.15), 8.0, 0.0), (1, slice(4, 9), (1.1, -4.05), -14.0, 92.0)):
            kv, kc = curved_piece(cl[sl], kh, kd, sh_h, sh_d, mat, top_mat)
            cx = sum(p[0] for p in cl[sl]) / len(cl[sl])
            kv, kc = xfs(kv, t=(-cx, 0.0, 0.0)), xfs(kc, t=(-cx, 0.0, 0.0))
            xe = cl[sl][-1][0] - cx if half == 0 else cl[sl][0][0] - cx
            kv += splinters((xe, 0.0, 0.0), (1.0 if half == 0 else -1.0, 0.0, 0.0), kh * 0.6, 45 + half, mat=mat)
            v, c = place(kv, rx=roll, ry=yaw, at=at, cols=kc)
            vis += v + moss_on(v, 47 + half, k=1)
            cols += c
        xp = S / 2
        for side, (x0, x1) in enumerate(((-xp - F["proj"], -0.05), (0.08, xp + F["proj"]))):
            bv, bc = beam_piece(x0, x1, nh, nd, mat, broken_end="x1" if side == 0 else "x0", seed=49 + side)
            bv, bc = xfs(bv, t=(-(x0 + x1) / 2, 0.0, 0.0)), xfs(bc, t=(-(x0 + x1) / 2, 0.0, 0.0))
            v, c = place(bv, ry=(6.0 if side == 0 else -80.0), rz=3.0, at=((-0.25, -1.55) if side == 0 else (2.65, -1.3)),
                         cols=bc)
            vis += v
            cols += c
        leaf_drifts(P, 410, ((0.0, -1.8, 1.3), (-1.4, -3.2, 0.8), (1.5, 0.4, 0.6)))
        P.notes.append("wooden myojin torii blown over backwards by a typhoon: posts snapped at the rotted feet")
    else:   # shu_snapped: a vermilion myojin, paint peeled; the left post snapped at 1.2 m, the kasagi fell from it
        kh, kd = 0.16, 0.22
        sh_h, sh_d = 0.12, 0.17
        rise = F["rise"]
        lean = F["lean"]
        # the right post still stands full height (with its black base band); its top carries nothing now
        xr = S / 2
        vis.append(pole((xr, -0.06, 0.0), (xr - lean, H - kh - sh_h, 0.0), r, mat, n=8, vis=(1,), r1=r * 0.94, wear="_w2"))
        vis.append(pole((xr, -0.06, 0.0), (xr - lean, H - kh - sh_h, 0.0), r, mat, n=6, vis=(2, 3), wear="_w2"))
        vis.append(pole((xr, -0.06, 0.0), (xr - lean * 0.12, 0.42, 0.0), r * 1.03, KURO, n=8, vis=(1, 2), wear="_w2"))
        cols.append(core.cyl("y", xr - lean / 2, 0.0, r * 0.95, 0.0, H - kh - sh_h, mat, n=8, vis=(), geo=True, view=True,
                             fire=True))
        # the left post: a 1.2 m lower part standing (rotted through inside), the upper part lies to the left
        v, c = stump(-S / 2, 1.20, r, mat, 51)
        vis += v
        cols += c
        vis.append(pole((-S / 2, -0.06, 0.0), (-S / 2, 0.42, 0.0), r * 1.03, KURO, n=8, vis=(1, 2), wear="_w2"))
        Lu = H - kh - sh_h - 1.25
        pv, pc = post(Lu, r, mat, top_break=True, foot_rot=True, seed=52)
        pv, pc = xfs(pv, t=(0.0, -Lu / 2, 0.0)), xfs(pc, t=(0.0, -Lu / 2, 0.0))
        v, c = place(pv, rz=-88.0, ry=-24.0, at=(-S / 2 - 1.35, 0.75), cols=pc)
        vis += v
        cols += c
        # the kasagi (with its shimaki) fell forward and broke in two; the tie-beam lies beside the standing post
        cl = K.curve(-L / 2, L / 2, 0.0, rise, n=8)
        for half, sl, at, yaw, roll in ((0, slice(0, 5), (-0.9, 1.75), 10.0, 0.0), (1, slice(4, 9), (1.15, 2.45), -22.0, 0.0)):
            kv, kc = curved_piece(cl[sl], kh, kd, sh_h, sh_d, mat, top_mat)
            cx = sum(p[0] for p in cl[sl]) / len(cl[sl])
            kv, kc = xfs(kv, t=(-cx, 0.0, 0.0)), xfs(kc, t=(-cx, 0.0, 0.0))
            xe = cl[sl][-1][0] - cx if half == 0 else cl[sl][0][0] - cx
            kv += splinters((xe, 0.0, 0.0), (1.0 if half == 0 else -1.0, 0.0, 0.0), kh * 0.6, 53 + half, mat=mat)
            v, c = place(kv, rx=roll, ry=yaw, at=at, cols=kc)
            vis += v + moss_on(v, 55 + half, k=1)
            cols += c
        bv, bc = beam_piece(-S / 2 + 0.25, S / 2 + F["proj"], nh, nd, mat, broken_end="x0", seed=54)
        mid = (-S / 2 + 0.25 + S / 2 + F["proj"]) / 2
        bv, bc = xfs(bv, t=(-mid, 0.0, 0.0)), xfs(bc, t=(-mid, 0.0, 0.0))
        v, c = place(bv, ry=-80.0, at=(S / 2 + 0.95, 0.35), cols=bc, sink=0.01)
        vis += v
        cols += c
        # the plaque fell face down at the foot
        vis.append(Ww(-0.15, 0.15, 0.0, 0.035, 0.55, 0.97, WOOD, vis=(1,), wear="_w2"))
        leaf_drifts(P, 420, ((-0.8, 0.9, 1.0), (0.6, 0.5, 0.7), (-2.0, 0.4, 0.6)))
        P.notes.append("vermilion myojin torii, paint peeled; one post snapped at 1.2 m, the kasagi slid down to the "
                       "ground (Inari / Hachiman only, as the standing vermilion torii)")
    add_all(P, vis + cols)
    P.dim("post_span", S, S, tol=0.01)
    P.extra.update({"cause": kind, "form": form, "shu": shu})
    return P


# ------------------------------------------------------------------------------------------------ stone
def fallen_stone(size, kind):
    F = T.STONE_FORMS[size]
    S, H, r = F["S"], F["H"], F["r"]
    old = kind == "quake_old"
    wear = "_w2"
    P = SPart("torii_fallen", budget="medium", res3=True, mass={"s": 3500.0, "m": 5000.0, "l": 11000.0}[size], bury=0.12)
    P.wear = wear
    vis, cols = [], []
    L = S + 2 * F["over"]
    kh = max(0.20, round(r * 1.30, 3))
    kd = round(r * 1.6, 3)
    sh_h = round(r * 1.0, 3)
    rg = random.Random(61 if not old else 71)
    sink = 0.07 if old else 0.03
    # the dome bases (kamebara) stay where they were set
    for sx in (-1, 1):
        b = skit.lathe([(0.0, -0.08), (r * 1.75, -0.08), (r * 1.75, 0.04), (r * 1.45, 0.16), (r * 1.08, 0.22), (0.0, 0.22)],
                       10, CARVED, vis=(1,), smooth=True)
        vis.append(xf(b, t=(sx * S / 2, 0.0, 0.0)))
        b2 = skit.lathe([(0.0, -0.08), (r * 1.75, -0.08), (r * 1.6, 0.1), (r * 1.08, 0.22), (0.0, 0.22)], 6, CARVED,
                        vis=(2, 3), smooth=False)
        vis.append(xf(b2, t=(sx * S / 2, 0.0, 0.0)))
        cols.append(core.cyl("y", sx * S / 2, 0.0, r * 1.7, 0.0, 0.20, CARVED, n=8, vis=(), geo=True, view=True, fire=True))
    ky = H - kh - sh_h
    # left post: its lowest drum still stands on the base (broken at 0.9 m); the right post fell whole and broke in two
    drums = [(-S / 2, 0.22, 0.95, True)]
    vis.append(pole((-S / 2, 0.20, 0.0), (-S / 2, 0.95, 0.0), r, CARVED, n=8, vis=(1,), r1=r * 0.98))
    vis.append(pole((-S / 2, 0.20, 0.0), (-S / 2, 0.95, 0.0), r, CARVED, n=6, vis=(2, 3)))
    cols.append(core.cyl("y", -S / 2, 0.0, r * 0.95, 0.21, 0.95, CARVED, n=8, vis=(), geo=True, view=True, fire=True))
    for k in range(4):                                             # the rough break: chips round the top
        a = 2 * math.pi * k / 4 + rg.uniform(-0.3, 0.3)
        vis.append(core.stone(rg, -S / 2 + r * 0.45 * math.cos(a), r * 0.45 * math.sin(a), r * 0.7, r * 0.6, 0.06,
                              0.97 + rg.uniform(0.0, 0.03), CARVED, bury=0.0, n=6, vis=(1,)))
    pieces = [((ky - 0.95) * 0.55, (-S / 2 - 0.6, 1.25), 70.0, "left upper drum"),
              ((ky - 0.95) * 0.45, (-S / 2 - 1.4, -0.3), -20.0, "left top drum"),
              (ky * 0.55, (S / 2 + 0.3, 1.5), 15.0, "right lower half"),
              (ky * 0.45, (S / 2 + 1.5, 0.4), -55.0, "right upper half")]
    for i, (Lp, at, yaw, _) in enumerate(pieces):
        pv = [pole((0.0, 0.0, 0.0), (0.0, Lp, 0.0), r, CARVED, n=8, vis=(1,), r1=r * 0.98),
              pole((0.0, 0.0, 0.0), (0.0, Lp, 0.0), r, CARVED, n=6, vis=(2, 3))]
        pc = [core.cyl("y", 0.0, 0.0, r * 0.95, 0.0, Lp, CARVED, n=8, vis=(), geo=True, view=True, fire=True)]
        pv = xfs(pv, t=(0.0, -Lp / 2, 0.0))
        pc = xfs(pc, t=(0.0, -Lp / 2, 0.0))
        v, c = place(pv, rz=90.0, ry=yaw, at=at, cols=pc, sink=sink)
        vis += v
        cols += c
        if old:
            vis += moss_on(v, 63 + i, k=1)
    # the kasagi broke in three; the tie-beam in two; the strut lies by itself
    cl = K.curve(-L / 2, L / 2, 0.0, F["rise"], n=9)
    for i, (sl, at, yaw, roll) in enumerate(((slice(0, 4), (-1.2, 2.35), 12.0, 0.0), (slice(3, 7), (0.3, 2.9), -8.0, 180.0),
                                              (slice(6, 10), (1.9, 2.8), 25.0, 0.0))):
        kv, kc = curved_piece(cl[sl], kh, kd, sh_h, kd * 0.82, CARVED, CARVED, wear=wear, top_w=kd * 1.12)
        cx = sum(p[0] for p in cl[sl]) / len(cl[sl])
        kv, kc = xfs(kv, t=(-cx, 0.0, 0.0)), xfs(kc, t=(-cx, 0.0, 0.0))
        v, c = place(kv, rx=roll, ry=yaw, at=at, cols=kc, sink=sink)
        vis += v + (moss_on(v, 66 + i, k=2) if old else moss_on(v, 66 + i, k=1))
        cols += c
    nh, nd = F["nuki"]
    xe = S / 2 + F["proj"]
    for side, (x0, x1) in enumerate(((-xe, -0.1), (0.05, xe))):
        bv = [W(x0, x1, -nh / 2, nh / 2, -nd / 2, nd / 2, CARVED, vis=(1, 2, 3))]
        bc = [col(x0, x1, -nh / 2, nh / 2, -nd / 2, nd / 2, CARVED)]
        mid = (x0 + x1) / 2
        bv, bc = xfs(bv, t=(-mid, 0.0, 0.0)), xfs(bc, t=(-mid, 0.0, 0.0))
        v, c = place(bv, ry=-10.0 + 30.0 * side, rz=4.0, at=((mid * 0.8, 1.45) if side == 0 else (0.2, 0.78)), cols=bc,
                     sink=sink)
        vis += v
        cols += c
    sw = r * 0.9
    st = [W(-sw / 2, sw / 2, 0.0, kh + 0.02, -nd * 0.4, nd * 0.4, CARVED, vis=(1, 2))]
    v, _ = place(st, rz=90.0, ry=40.0, at=(0.2, 0.75), sink=sink)
    vis += v
    if old:
        leaf_drifts(P, 430, ((0.0, 1.5, 1.6), (-1.6, 0.6, 0.9), (1.6, 1.3, 0.9), (0.4, 2.8, 0.8)))
        for sx in (-1, 1):
            vis += K.moss_foot(sx * S / 2, 0.0, r * 1.6, 0.20, n=10, sides=4, seed=74 + sx, wear="_w2", y0=0.0)
    else:
        leaf_drifts(P, 440, ((0.0, 1.5, 1.2), (1.5, 0.6, 0.6)))
    K.aged_stone(vis, 9500 + (7 if old else 0))
    add_all(P, vis + cols)
    P.dim("post_span", S, S, tol=0.01)
    P.extra.update({"cause": "earthquake (Genroku 1703 / Hoei 1707)", "old": old, "size": size})
    P.notes.append("stone torii thrown down by an earthquake: posts broken into drums, the kasagi in three, the dome "
                   "bases in place" + ("; decades ago: moss, leaf drifts, pieces sunk" if old else ""))
    return P


PROPS = [
    {"id": "jp_s_torii_fallen", "cat": "shrine", "mount": "shrine", "per_row": 5,
     "notes": ["FP1 (2026-10-01): fully collapsed torii for ruined shrines, one or two per type; vermilion only at "
               "Inari / Hachiman like the standing ones", "each lying piece has its own convex collision"],
     "models": [
         M("jp_s_torii_fallen_shinmei_rot", "shinmei", "abandoned", "Wooden shinmei torii rotted at the feet and fallen",
           lambda: fallen_wood("shinmei", "rot"), mount="shrine"),
         M("jp_s_torii_fallen_myojin_typhoon", "myojin", "abandoned", "Wooden myojin torii blown over by a typhoon",
           lambda: fallen_wood("myojin", "typhoon"), mount="shrine"),
         M("jp_s_torii_fallen_shu_snapped", "myojin", "abandoned",
           "Vermilion torii, one post snapped, the kasagi fallen and broken (Inari / Hachiman only)",
           lambda: fallen_wood("myojin", "shu_snapped"), mount="shrine"),
         M("jp_s_torii_fallen_stone_quake", "m", "abandoned", "Stone torii thrown down by an earthquake",
           lambda: fallen_stone("m", "quake"), mount="shrine"),
         M("jp_s_torii_fallen_stone_quake_old", "s", "abandoned",
           "Stone torii fallen in an old earthquake, mossy and leaf-covered", lambda: fallen_stone("s", "quake_old"),
           mount="shrine"),
     ]},
]
