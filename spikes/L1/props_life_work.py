"""Life layer E (research/interior/LIFE_LAYER.md items 37-44): work at home.

Spinning wheel, ground loom, mortar and hand mill carry collision (the loom and the wheel are 'standard' pieces with
Res 1-3); straw work, winnowing basket, writing box, the account clutter and the measures are visual only. Loot: the
mortar rim, the hand-mill top and the coin box lid (BUILD_LIST jp_f_usu: usu top 1 point, range 0.2).
"""
import math
import random

import lkit
from lkit import (core, box, prism, lathe, xf, xfs, flat_poly, W, board, pole, beam, rope_path, grid_sheet, col, disc,
                  stain, mound, soft_slab, text, LPart, M, rng, bipyramid, lod_box, wear_all, rest, cyl_col,
                  place_group, WOOD, WEATH, IRON, PALE, DARK, LACQ, BAMBOO, WEAVE, MUSHIRO, TAWARA, STACK, ROPE, PAPER,
                  INDIGO, KINARI, RED, LITTER, STONE, CUT, RICE, LIFE)

CAT = "work"


def flatpart(name, mass=0.5, anchor="floor"):
    return LPart(name, budget="small", mass=mass, anchor=anchor, flat=True)


# ================================================================================================ 37 spinning wheel
def itoguruma(wear=None, wheel=True, thread=False):
    """Cotton spinning wheel (itoguruma): a floor plank 0.85 long, two posts carrying a bamboo-spoked wheel d 0.60
    (axle 0.42 up), a crank, the spindle post at the far end."""
    out = [board(-0.42, 0.42, 0.0, 0.04, -0.11, 0.11, k=2, vis=(1, 2))]
    ax, ay = -0.15, 0.42
    for dz in (-0.07, 0.07):
        out.append(W(ax - 0.025, ax + 0.025, 0.04, ay + 0.04, dz - 0.015, dz + 0.015, WEATH, vis=(1, 2)))
    if wheel:
        out += wheel_parts(ax, ay)
        out.append(box(ax - 0.01, ax + 0.01, ay - 0.10, ay, 0.10, 0.12, WEATH, vis=(1,)))   # crank arm
        out.append(pole((ax, ay - 0.10, 0.12), (ax, ay - 0.10, 0.20), 0.01, WEATH, n=4, vis=(1,)))
    out.append(W(0.30, 0.34, 0.04, 0.30, -0.02, 0.02, WEATH, vis=(1, 2)))                   # spindle post
    out.append(pole((0.26, 0.26, 0.0), (0.42, 0.27, 0.0), 0.004, IRON, n=3, vis=(1,)))      # the spindle (tsumu)
    if thread:
        out.append(lathe([(0.0, 0.0), (0.012, 0.01), (0.014, 0.05), (0.0, 0.06)], 5, KINARI, vis=(1,)))
        out[-1] = xf(out[-1], rz=-90.0, t=(0.32, 0.27, 0.0))
        out.append(rope_path([(0.36, 0.27, 0.0), (0.10, ay + 0.28, 0.0), (ax, ay + 0.29, 0.0)], 0.0015, KINARI, n=3,
                             vis=(1,))[0])
    out.append(W(-0.45, 0.45, 0.0, ay + 0.32, -0.12, 0.12, WEATH, vis=(3,)))
    return wear_all(out, wear)


def wheel_parts(ax, ay, R=0.30, vis=(1,), broken=False):
    """The wheel: two rims of cord laced round bamboo spokes (8 each side), the hub; axis along z."""
    out = []
    for dz, ph in ((-0.05, 0.0), (0.05, math.pi / 8)):
        rim = lkit.coil(0.0, 0.0, R, 0.006, ROPE, n=12, m=3, z0=-0.006, vis=vis)
        out.append(xf(rim, t=(ax, ay, dz)))
        for k in range(8):
            if broken and k in (1, 2, 5):
                continue
            a = ph + 2 * math.pi * k / 8
            out.append(beam((ax, ay, 0.0), (ax + R * math.cos(a), ay + R * math.sin(a), dz), 0.008, 0.004, BAMBOO,
                            up=(0.0, 0.0, 1.0), vis=vis))
    out.append(pole((ax, ay, -0.09), (ax, ay, 0.09), 0.02, WEATH, n=5, vis=vis))
    out.append(xf(lathe([(0.0, -0.05), (R, -0.05), (R, 0.05), (0.0, 0.05)], 8, BAMBOO, vis=(2,), smooth=False),
                  rx=90.0, t=(ax, ay, 0.0)))
    return out


def spinning(kind):
    P = LPart("itoguruma", budget="furniture", res3=True, mass=6.0, anchor="floor")
    if kind in ("std", "thread"):
        P.adds(itoguruma(thread=kind == "thread"))
        if kind == "thread":                            # a basket of cotton slivers beside it
            P.add(lathe([(0.0, 0.0), (0.12, 0.0), (0.14, 0.10), (0.13, 0.10), (0.0, 0.01)], 8, WEAVE, vis=(1,)))
            P.solids[-1] = xf(P.solids[-1], t=(0.30, 0.0, 0.32))
            for k in range(5):
                P.add(xf(lkit.lcyl("x", 0.0, 0.0, 0.015, -0.08, 0.08, KINARI, n=5, vis=(1,)), ry=k * 35.0,
                         t=(0.30, 0.09 + 0.012 * (k % 2), 0.32)))
        P.add(col(-0.42, 0.42, 0.0, 0.04, -0.11, 0.11))
        P.add(col(-0.46, 0.16, 0.04, 0.74, -0.10, 0.10))
    else:                                               # as left: the wheel knocked off its posts, spokes broken
        P.adds(itoguruma(wear="_w2", wheel=False))
        wp = wheel_parts(0.0, 0.0, broken=True)
        ws, wc = place_group(wp, [lkit.fkit.col_solid(xf(lkit.cyl_col(0.30, -0.06, 0.06, n=8), rx=90.0))],
                             [dict(rx=85.0, ry=30.0, t=(0.10, 0.0, 0.45))])
        P.adds(ws)
        P.adds(wc)
        P.add(col(-0.42, 0.42, 0.0, 0.04, -0.11, 0.11))
        P.add(stain(371, 0.1, 0.4, 0.3, sx=1.5))
    P.dim("wheel_d", 0.60, 0.60, tol=0.01)
    P.notes.append("cotton spinning wheel (itoguruma), farm and village women's work (BUILDING_LIST 300, 304, 1436)")
    return P


# ================================================================================================ 38 ground loom
def loom(kind):
    """Ground loom (izari-bata): side rails sloping from the weaver's seat up to two back posts; breast beam at the
    lap (0.35), warp beam at the back (0.85); the heddle and reed; cloth rolled on the breast beam."""
    ab = kind == "cut"
    P = LPart("izaribata", budget="furniture", res3=True, mass=20.0, anchor="floor")
    wr = "_w2" if ab else None
    L, Wd = 1.50, 0.60
    out = []
    for sz in (-1, 1):
        z = sz * Wd / 2
        out.append(beam((-L / 2, 0.02, z), (L / 2 - 0.05, 0.02, z), 0.05, 0.04, WEATH, up=(0, 1, 0)))       # floor rail
        out.append(W(L / 2 - 0.10, L / 2 - 0.04, 0.0, 0.95, z - 0.03, z + 0.03, WEATH, vis=(1, 2)))       # back post
        out.append(beam((-0.30, 0.02, z), (L / 2 - 0.08, 0.80, z), 0.04, 0.04, WEATH))                     # brace
    out.append(pole((L / 2 - 0.07, 0.85, -Wd / 2 - 0.04), (L / 2 - 0.07, 0.85, Wd / 2 + 0.04), 0.035, WEATH, n=6))
    # FP1 (2026-10-01, Stephen: "the loom floats"): the breast beam, heddle rod, reed and the back of the seat board
    # hung in the air with nothing under them. Now: the breast beam lies in two notched front uprights on the floor
    # rails (where it is set down when nobody weaves); two lever arms (mane-gi) run forward from the back posts and
    # carry the heddle rod and the reed on cords; the seat board has a back leg too.
    for sz in (-1, 1):
        z = sz * Wd / 2
        out.append(W(-0.47, -0.43, 0.04, 0.32, z - 0.02, z + 0.02, WEATH, vis=(1, 2)))                # beam upright
        out.append(beam((L / 2 - 0.07, 0.93, sz * 0.27), (0.12, 0.97, sz * 0.27), 0.035, 0.035, WEATH))  # lever arm
    out.append(pole((-0.45, 0.35, -Wd / 2 - 0.03), (-0.45, 0.35, Wd / 2 + 0.03), 0.03, WEATH, n=6))  # breast beam
    out.append(W(-L / 2, -L / 2 + 0.30, 0.10, 0.13, -0.25, 0.25, WEATH, vis=(1, 2)))               # the seat board
    out.append(W(-L / 2 + 0.02, -L / 2 + 0.06, 0.0, 0.10, -0.22, 0.22, WEATH, vis=(1,)))
    out.append(W(-L / 2 + 0.24, -L / 2 + 0.28, 0.0, 0.10, -0.22, 0.22, WEATH, vis=(1,)))           # FP1: back leg
    wf, wb = (-0.43, 0.36), (L / 2 - 0.07, 0.86)                                                   # warp ends (x, y)
    if kind in ("cloth", "bare"):
        def warp(u, v):
            return (wf[0] + (wb[0] - wf[0]) * u, wf[1] + (wb[1] - wf[1]) * u, -0.24 + 0.48 * v)
        out.append(grid_sheet(warp, 3, 1, KINARI, vis=(1,), wear="_w1"))
        out.append(W(0.05, 0.08, 0.40, 0.75, -0.27, 0.27, BAMBOO, vis=(1,)))        # reed frame
        out.append(pole((0.25, 0.70, -0.27), (0.25, 0.70, 0.27), 0.012, BAMBOO, n=4))   # heddle rod
        for sz in (-1, 1):                                                         # FP1: hung from the lever arms
            z = sz * 0.27
            out.append(pole((0.25, 0.70, z), (0.25, 0.955, z), 0.003, KINARI, n=3, vis=(1,)))
            out.append(pole((0.065, 0.75, z), (0.065, 0.945, z), 0.003, KINARI, n=3, vis=(1,)))
        if kind == "cloth":
            out.append(xf(lkit.lcyl("z", 0.0, 0.0, 0.05, -0.24, 0.24, INDIGO, n=8, vis=(1,)), t=(-0.45, 0.35, 0.0)))
            def cloth(u, v):
                x0, y0 = -0.45, 0.40
                return (x0 + 0.35 * u, y0 + 0.09 * u, -0.24 + 0.48 * v)
            out.append(grid_sheet(cloth, 2, 1, INDIGO, vis=(1,)))
    else:                                               # as left: the warp cut, threads hanging to the floor, the cloth
        def hang(u, v):                                 # unrolled across the floor in front
            return (wb[0] - 0.02 - 0.05 * v, wb[1] - 0.84 * v, -0.24 + 0.48 * u)
        out.append(grid_sheet(hang, 1, 3, KINARI, vis=(1,), wear="_w2"))
        out.append(grid_sheet(lambda u, v: (-0.45 - 0.9 * u, 0.004 + 0.02 * math.sin(math.pi * u * 3) ** 2,
                                            -0.22 + 0.44 * v + 0.1 * u), 4, 1, INDIGO, vis=(1,), wear="_w2"))
        out.append(W(0.05, 0.08, 0.0, 0.35, -0.27, 0.27, BAMBOO, vis=(1,)))        # the reed dropped, leaning
        out[-1] = rest([xf(out[-1], rz=35.0, pivot=(0.06, 0.0, 0.0))], 0.0)[0]
        out.append(stain(381, -0.8, 0.0, 0.35, sx=1.6))
    out.append(W(-L / 2, L / 2, 0.0, 0.95, -Wd / 2 - 0.04, Wd / 2 + 0.04, WEATH, vis=(2,)))
    out.append(W(-L / 2, L / 2, 0.0, 0.95, -Wd / 2, Wd / 2, WEATH, vis=(3,)))
    P.adds(wear_all(out, wr))
    P.add(col(-0.60, L / 2 - 0.02, 0.0, 0.95, -Wd / 2 - 0.05, Wd / 2 + 0.05, WEATH))
    P.dim("L", 1.50, L, tol=0.005)
    P.notes.append("hand loom (izari-bata) with cloth on the breast beam (BUILDING_LIST 1456-1457); the seat board end "
                   "has no collision (sit-in space); T1-2")
    return P


# ================================================================================================ 39 straw work
def stool(wear=None):
    return wear_all([W(-0.18, 0.18, 0.12, 0.15, -0.09, 0.09, WEATH, vis=(1, 2)),
                     W(-0.15, -0.12, 0.0, 0.12, -0.08, 0.08, WEATH, vis=(1,)),
                     W(0.12, 0.15, 0.0, 0.12, -0.08, 0.08, WEATH, vis=(1,))], wear)


def straw_bundle(L=0.7, r=0.07, wear=None):
    s = lkit.lcyl("x", r, 0.0, r, -L / 2, L / 2, STACK, n=6, vis=(1,))
    out = [s]
    for x in (-L / 4, L / 4):
        out.append(xf(lkit.rope_ring(r, 0.0, 0.02, ROPE, 6, vis=(1,)), rz=90.0, t=(x, r, 0.0)))
    return wear_all(out, wear)


def half_sandal(wear=None):
    """A sandal half made: the sole woven two-thirds up its four warp cords, the rest of the cords loose."""
    out = [box(-0.045, 0.045, 0.0, 0.012, -0.05, 0.12, MUSHIRO, vis=(1,))]
    for dx in (-0.03, -0.01, 0.01, 0.03):
        out.append(pole((dx, 0.006, -0.05), (dx * 1.4, 0.004, -0.22), 0.003, ROPE, n=3, vis=(1,)))
    return wear_all(out, wear)


def straw_work(kind):
    P = flatpart("straw_work", 3.0)
    if kind == "sandal":
        P.adds(stool())
        P.adds(xfs(half_sandal(), ry=10.0, t=(0.0, 0.15, 0.0)))
        P.adds(xfs(straw_bundle(), ry=15.0, t=(0.10, 0.0, 0.35)))
        P.adds(xfs(lkit.skit.rope_path([(0.3, 0.01, -0.1), (0.5, 0.01, 0.05), (0.45, 0.01, 0.25)], 0.006, ROPE, n=3),
                   t=(0.0, 0.0, 0.0)))
    elif kind == "beating":                             # the straw-beating stone and mallet (wara-uchi)
        st = core.stone(random.Random(391), 0.0, 0.0, 0.40, 0.32, 0.12, 0.12, CUT, bury=0.0, n=8, vis=(1, 2))
        P.add(st)
        P.adds(xfs([lkit.lcyl("x", 0.0, 0.0, 0.05, -0.12, 0.12, WEATH, n=6, vis=(1,)),
                    pole((0.0, 0.0, 0.0), (0.0, 0.0, 0.35), 0.015, WEATH, n=4, vis=(1,))], ry=30.0, t=(0.0, 0.17, 0.0)))
        P.adds(xfs(straw_bundle(0.8, 0.06), ry=-20.0, t=(0.0, 0.0, 0.35)))
    else:                                               # as left: stool tipped, straw spread, the sandal dropped
        P.adds(rest(xfs(stool(wear="_w2"), rz=90.0, ry=20.0), 0.0))
        P.add(lkit.bits.mound(392, 0.25, 0.30, 0.35, 0.03, STACK, sx=1.6, wear="_w2", vis=(1,)))
        P.adds(xfs(half_sandal(wear="_w2"), ry=60.0, t=(-0.30, 0.0, 0.30)))
        P.add(stain(393, 0.0, 0.2, 0.40, sx=1.6))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], STACK, vis=(2,)))
    P.dim("stool_h", 0.15, 0.15, tol=0.005)
    P.notes.append("rural straw work: a half-made sandal on the stool, straw bundles, the beating stone and mallet")
    return P


# ================================================================================================ 40 mi / furui
def mi_basket(wear=None, vis=(1,)):
    """Winnowing basket (mi): 0.60 wide x 0.55 deep, the back and sides raised to 0.16, the front a flat lip."""
    def f(u, v):                                        # u across (x), v from the lip (+z) to the back (-z)
        x = -0.30 + 0.60 * u
        side = (abs(u - 0.5) * 2) ** 3
        y = 0.16 * max(side, v ** 2.5) * (0.6 + 0.4 * v)
        z = 0.275 - 0.55 * v
        return (x * (1 - 0.15 * v * v), y + 0.003, z)
    out = [grid_sheet(f, 5, 4, WEAVE, vis=vis, wear=wear)]
    out.append(beam((-0.30, 0.02, 0.27), (-0.26, 0.19, -0.27), 0.015, 0.015, BAMBOO, vis=vis))
    out.append(beam((0.30, 0.02, 0.27), (0.26, 0.19, -0.27), 0.015, 0.015, BAMBOO, vis=vis))
    return out


def furui(wear=None):
    return [lathe([(0.225, 0.0), (0.225, 0.08), (0.215, 0.08), (0.215, 0.0)], 10, WEATH, vis=(1,), wear=wear),
            flat_poly([(0.215 * math.cos(-k * math.pi / 5), 0.215 * math.sin(-k * math.pi / 5)) for k in range(10)], 0.02,
                      WEAVE, vis=(1,), wear=wear)]


def mi(kind):
    anchor = "wall" if kind == "mi_wall" else "floor"
    P = flatpart("mi", 1.0, anchor)
    if kind == "mi":
        P.adds(mi_basket())
    elif kind == "mi_wall":                             # hung on a peg by its back rim, the bowl facing the room
        P.add(lkit.peg(0.0, 1.50, z0=0.0))
        ss = xfs(mi_basket(), rx=-80.0, t=(0.0, 1.50 - 0.30, 0.0))
        zmin = min(v[2] for q in ss for v in q.verts)
        P.adds(xfs(ss, t=(0.0, 0.0, 0.004 - zmin)))
    elif kind == "furui":
        P.adds(furui())
    else:                                               # as left: tipped on its side, the grain spilled
        P.adds(rest(xfs(mi_basket(wear="_w2"), rx=-60.0, ry=20.0), 0.0))
        P.add(mound(401, 0.10, 0.35, 0.22, 0.03, RICE, sx=1.5, wear="_w2", vis=(1,)))
        P.adds(xfs(furui(wear="_w2"), t=(-0.45, 0.0, 0.25)))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WEAVE, vis=(2,)))
    P.dim("mi_w", 0.60, 0.60, tol=0.01)
    P.notes.append("winnowing basket (mi) and rice sieve (furui): rural core (BUILDING_LIST 2835)")
    return P


# ================================================================================================ 41 usu (★)
USU_N = 16                     # FP2: a rounder mortar (was 10 sides)
USU_PROF = [(0.0, 0.0), (0.25, 0.0), (0.25, 0.08), (0.22, 0.28), (0.25, 0.47), (0.25, 0.55), (0.20, 0.55),
            (0.12, 0.44), (0.0, 0.40)]


def usu_body(wear=None):
    """Wooden mortar d 0.50 h 0.55: a waisted log, the hollow 0.15 deep, a 5 cm flat rim; flat base on y = 0."""
    return [lathe(USU_PROF, USU_N, WOOD, vis=(1,), wear=wear),
            lathe([(0.0, 0.0), (0.25, 0.0), (0.23, 0.28), (0.25, 0.55), (0.0, 0.50)], 6, WOOD, vis=(2,), smooth=False),
            lathe([(0.0, 0.0), (0.25, 0.0), (0.25, 0.55), (0.0, 0.55)], 4, WOOD, vis=(3,), smooth=False)]


def _bowl_y(r):
    """Height of the mortar's hollow at radius r, on the FACETED lathe (inscribed radius, cos(pi / USU_N))."""
    r = r / math.cos(math.pi / USU_N)
    if r <= 0.12:
        return 0.40 + r / 0.12 * 0.04
    return 0.44 + min(r - 0.12, 0.08) / 0.08 * 0.11


def tategine(L=0.90):
    """The vertical pounder: a pole thick at both ends, waisted in the middle for the hands."""
    s = lathe([(r, y * L / 0.90) for r, y in TATE_PROF], 10, WEATH, vis=(1,))
    return [s]


TATE_PROF = [(0.0, 0.0), (0.05, 0.0), (0.05, 0.25), (0.03, 0.35), (0.03, 0.55), (0.05, 0.65), (0.05, 0.90),
             (0.0, 0.90)]


def _tate_r(sv):
    """The pounder's radius at distance sv along it (TATE_PROF)."""
    for (r0, y0), (r1, y1) in zip(TATE_PROF[1:-2], TATE_PROF[2:-1]):
        if y0 <= sv <= y1:
            return r0 + (r1 - r0) * (sv - y0) / max(1e-6, y1 - y0)
    return 0.05


def tategine_leaning(phi=16.0):
    """FP2 (Stephen: the pounder hung in the air beside the mortar): the tategine stands on the floor beside the
    mortar (+z side) and leans on the rim's outer edge. Solved: the foot disc's low edge on the floor, the shaft
    surface touching the rim corner (y 0.55, r 0.25), using the pounder's real radius at the contact."""
    f = math.radians(phi)
    d = (math.cos(f), -math.sin(f))                     # axis direction in (y, z): up and toward the mortar
    yb = 0.05 * math.sin(f) + 0.001                     # the foot disc's lowest edge on the floor
    E = (0.55, 0.25)

    def gap(zb):
        vy, vz = E[0] - yb, E[1] - zb
        t = vy * d[0] + vz * d[1]
        return math.hypot(vy - t * d[0], vz - t * d[1]) - _tate_r(t), t
    lo, hi = 0.25, 0.80                                 # gap shrinks as the foot moves in
    for _ in range(60):
        mid = (lo + hi) / 2
        g, t = gap(mid)
        if g > 0:
            hi = mid
        else:
            lo = mid
    zb = hi
    g, t = gap(zb)
    return xfs(tategine(), rx=-phi, t=(0.0, yb, zb)), {"foot": (0.0, yb, zb), "contact_s": t, "gap": g}


def yokogine():
    """The mallet pounder (yokogine): a short thick head (d 0.14, 0.28 long, along x), the handle along +z."""
    head = lkit.lcyl("x", 0.0, 0.0, 0.07, -0.14, 0.14, WEATH, n=12, vis=(1,))
    lkit.auto_smooth(head, 40.0)
    return [head, pole((0.0, 0.0, 0.06), (0.0, 0.0, 0.75), 0.02, WEATH, n=7, vis=(1,))]


def yokogine_in_usu():
    """FP2: the mallet's head lies in the hollow (its two end circles on the bowl), the handle rests on the rim's
    inner edge and sticks out over it, rising a few degrees (the head's weight holds it)."""
    zc = -0.03
    yc = 0.0                                            # the head's end circles rest on the bowl (every point clear)
    for k in range(72):
        a = 2 * math.pi * k / 72
        zz, dy = zc + 0.07 * math.cos(a), 0.07 * math.sin(a)
        yc = max(yc, _bowl_y(math.hypot(0.14, zz)) - dy + 0.002)
    E = (0.55, 0.20 * math.cos(math.pi / USU_N))        # the rim's inner edge on the handle side (+z)
    dz, dy = E[1] - zc, E[0] - yc
    th = math.atan2(dy, dz) + math.asin(0.021 / math.hypot(dy, dz))   # the handle (r 0.02) just on the edge
    return xfs(yokogine(), rx=-math.degrees(th), t=(0.0, yc, zc)), math.degrees(th), yc


def ishiusu(wear=None, top_on=True):
    """Stone hand mill: two discs d 0.40 (0.12 + 0.11), the top with a feed hole and a wooden handle peg."""
    lo = [lathe([(0.0, 0.0), (0.20, 0.0), (0.20, 0.12), (0.0, 0.125)], 10, CUT, vis=(1, 2), wear=wear, smooth=False)]
    top = [lathe([(0.0, 0.12), (0.20, 0.12), (0.20, 0.23), (0.03, 0.23), (0.03, 0.20), (0.0, 0.20)], 10, CUT, vis=(1, 2),
                 wear=wear, smooth=False),
           pole((0.17, 0.18, 0.0), (0.17, 0.33, 0.0), 0.015, WEATH, n=4, vis=(1,))]
    return lo, top


def usu(kind):
    P = LPart("usu", budget="small", res3=True, mass=40.0 if kind.startswith("usu") else 30.0, anchor="floor")
    if kind in ("usu", "usu_mallet", "usu_fallen"):
        ab = kind == "usu_fallen"
        P.adds(usu_body(wear="_w2" if ab else None))
        if kind == "usu":                               # FP2: the pounder on the floor, leaning on the rim
            ss, info = tategine_leaning()
            P.adds(ss)
            P.notes.append("FP2: the tategine stands on the floor %.2f m out (foot centre), leaning 16 deg on the rim's "
                           "outer edge (touching %.0f cm up the pounder)" % (info["foot"][2], info["contact_s"] * 100))
        elif kind == "usu_mallet":                      # FP2: head in the hollow, handle resting on the rim
            ss, th, yc = yokogine_in_usu()
            P.adds(ss)
            P.notes.append("FP2: the yokogine's head lies in the hollow (centre y %.3f), the handle rests on the rim "
                           "edge rising %.1f deg" % (yc, th))
        else:                                           # the pounder fallen across the floor, dust in the bowl
            # FP2: lies on its two thick ends (r 0.05) on the floor, clear of the mortar
            P.adds(xfs(tategine(), rz=90.0, ry=25.0, t=(1.20, 0.05, 0.35)))
            P.add(xf(mound(411, 0.0, 0.0, 0.10, 0.02, RICE, wear="_w2", vis=(1,)), t=(0.0, 0.41, 0.0)))
            P.add(stain(412, 0.5, 0.3, 0.35, sx=1.5))
        P.add(cyl_col(0.25, 0.0, 0.55, n=8, mat=WOOD))
        P.loot_rect("rim", 0.55, -0.25, 0.25, -0.25, 0.25, rng=0.2, points=[(0.225, 0.55, 0.0)])
        P.dim("d", 0.50, 0.50, tol=0.005)
        P.dim("h", 0.55, 0.55, tol=0.005)
    else:
        lo, top = ishiusu(wear="_w2" if kind == "ishiusu_off" else None)
        P.add(lkit.fkit.W(-0.30, 0.30, 0.0, 0.01, -0.30, 0.30, MUSHIRO, vis=(1,)))
        P.solids[-1] = xf(P.solids[-1], t=(0.0, 0.0, 0.0))
        lo = xfs(lo, t=(0.0, 0.01, 0.0))
        P.adds(lo)
        P.add(cyl_col(0.20, 0.0, 0.13, n=8, mat=CUT))
        if kind == "ishiusu":
            P.adds(xfs(top, t=(0.0, 0.01, 0.0)))
            P.add(cyl_col(0.20, 0.13, 0.24, n=8, mat=CUT))
            P.loot_rect("top", 0.24, -0.15, 0.15, -0.15, 0.15, rng=0.15, points=[(-0.10, 0.24, 0.08)])
        else:                                           # the top stone lifted off and leaning against the bottom one
            ts, tc = place_group(top, [cyl_col(0.20, 0.12, 0.23, n=8, mat=CUT)],
                                 [dict(rz=70.0, t=(0.52, 0.0, 0.05))])
            P.adds(ts)
            P.adds(tc)
            P.add(mound(413, 0.0, 0.0, 0.14, 0.012, RICE, wear="_w2", vis=(1,)))
            P.solids[-1] = xf(P.solids[-1], t=(0.0, 0.135, 0.0))
            P.loot_rect("bottom_stone", 0.135, -0.15, 0.15, -0.15, 0.15, rng=0.15, points=[(-0.10, 0.135, -0.08)])
        P.add(lathe([(0.0, 0.0), (0.20, 0.0), (0.20, 0.23), (0.0, 0.23)], 4, CUT, vis=(3,), smooth=False))
        P.dim("d", 0.40, 0.40, tol=0.005)
    P.notes.append("rice mortar and pounder, stone hand mill (BUILD_LIST jp_f_usu); loot on the rim / millstone")
    return P


# ================================================================================================ 42 writing box
def suzuribako(open_=False, wear=None):
    """Writing box (suzuri-bako) 0.24 x 0.22 x 0.05, lacquered; open: the inkstone, ink stick, two brushes, a
    water dropper in the tray."""
    out = [W(-0.12, 0.12, 0.0, 0.045, -0.11, 0.11, LACQ, vis=(1, 2))]
    if not open_:
        out.append(W(-0.122, 0.122, 0.045, 0.055, -0.112, 0.112, LACQ, vis=(1,)))
    else:
        out.append(W(-0.07, 0.03, 0.045, 0.055, -0.09, 0.09, STONE, vis=(1,)))                     # inkstone
        out.append(W(0.05, 0.06, 0.045, 0.058, -0.06, 0.02, LACQ, vis=(1,)))                        # ink stick
        out.append(lathe([(0.0, 0.045), (0.02, 0.045), (0.02, 0.06), (0.0, 0.066)], 6, PALE, vis=(1,)))
        out[-1] = xf(out[-1], t=(0.08, 0.0, 0.07))
        for dz in (-0.08, -0.06):
            out.append(pole((-0.10, 0.052, dz), (0.10, 0.052, dz + 0.01), 0.004, BAMBOO, n=3, vis=(1,)))
    return wear_all(out, wear)


def paper_stack(n=1, wear=None, h=0.03):
    return wear_all([W(-0.12, 0.12, 0.0, h, -0.17, 0.17, PAPER, vis=(1,))], wear)


def writing(kind):
    P = flatpart("writing_box", 1.0)
    if kind == "closed":
        P.adds(suzuribako())
        P.adds(xfs(paper_stack(), ry=6.0, t=(0.30, 0.0, 0.0)))
    elif kind == "open":
        P.adds(suzuribako(open_=True))
        P.add(xf(W(-0.122, 0.122, 0.0, 0.01, -0.112, 0.112, LACQ, vis=(1,)), ry=-15.0, t=(-0.30, 0.0, 0.05)))
        P.adds(xfs(paper_stack(), ry=6.0, t=(0.30, 0.0, 0.0)))
        P.add(pole((0.22, 0.034, 0.05), (0.38, 0.034, -0.02), 0.004, BAMBOO, n=3, vis=(1,)))
    else:                                               # as left: box knocked, lid off, papers slid, an ink stain
        P.adds(rest(xfs(suzuribako(open_=True, wear="_w2"), rz=8.0, ry=25.0), 0.0))
        r = random.Random(421)
        for k in range(4):
            P.adds(xfs(paper_stack(h=0.004, wear="_w2"), ry=r.uniform(0, 90), t=(0.25 + 0.12 * k, 0.001 * k,
                                                                                  0.10 * (k % 2))))
        P.add(pole((-0.18, 0.004, 0.25), (-0.02, 0.004, 0.30), 0.004, BAMBOO, n=3, vis=(1,)))
        P.add(stain(422, 0.05, 0.20, 0.10, sx=1.5, mat=LITTER, wear="_w2"))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], LACQ, vis=(2,)))
    P.dim("box_w", 0.24, 0.24, tol=0.005)
    P.notes.append("writing box with inkstone and brushes, a paper stack (mount surface: a desk or shelf)")
    return P


# ================================================================================================ 43 choba set (★)
def daifukucho(wear="_w1", text_wear="_w1", lying=True):
    """Account book: a thick paper block, a plain paper cover with 'daifukucho' and the year in ink (life atlas),
    the binding cord."""
    out = [W(-0.085, 0.085, 0.0, 0.035, -0.12, 0.12, PAPER, vis=(1,)),
           W(-0.087, 0.087, 0.035, 0.038, -0.122, 0.122, KINARI, vis=(1,))]
    out[1].wear = wear
    out.append(text((0.0, 0.0385, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), 0.20, LIFE, "daifukucho", wear=text_wear,
                    off=0.0008))
    out.append(W(-0.087, 0.087, 0.0, 0.038, -0.105, -0.095, ROPE, vis=(1,)))
    return out


def soroban(wear=None):
    """Abacus 0.30 x 0.08: a frame, the beam, rows of beads as bars."""
    out = [W(-0.15, 0.15, 0.0, 0.02, -0.045, 0.045, WOOD, vis=(1,)),
           W(-0.145, 0.145, 0.02, 0.024, -0.02, -0.014, WOOD, vis=(1,))]
    for k in range(11):
        x = -0.125 + 0.025 * k
        out.append(box(x - 0.009, x + 0.009, 0.02, 0.032, -0.04, -0.024, LACQ, vis=(1,)))
        out.append(box(x - 0.009, x + 0.009, 0.02, 0.032, 0.0, 0.03, LACQ, vis=(1,)))
    return wear_all(out, wear)


def zenibako(open_=False, wear=None):
    """Coin box (zenibako) 0.40 x 0.30 x 0.25: iron-banded, a slot in the lid, a padlock."""
    out = [W(-0.20, 0.20, 0.0, 0.22, -0.15, 0.15, WOOD, vis=(1, 2))]
    if not open_:
        out.append(W(-0.205, 0.205, 0.22, 0.25, -0.155, 0.155, WOOD, vis=(1, 2)))
        out.append(W(-0.10, 0.10, 0.2505, 0.252, -0.012, 0.012, LACQ, vis=(1,)))          # the coin slot
        out.append(box(-0.025, 0.025, 0.14, 0.20, 0.15, 0.17, IRON, vis=(1,)))            # padlock
    else:
        lid = W(-0.205, 0.205, 0.0, 0.03, -0.155, 0.155, WOOD, vis=(1, 2))
        out.append(xf(lid, rx=-100.0, pivot=(0.0, 0.0, -0.155), t=(0.0, 0.22, 0.0)))
        out.append(flat_poly([(-0.18, -0.13), (0.18, -0.13), (0.18, 0.13), (-0.18, 0.13)][::-1], 0.03, LITTER, vis=(1,),
                             wear="_w2"))
    for x in (-0.19, 0.19):
        out.append(W(x - 0.012, x + 0.012, 0.0, 0.22, -0.152, 0.152, IRON, vis=(1,)))
    return wear_all(out, wear)


def tenbin_scale(wear=None):
    """Money-changer's balance: a post on a drawer box, a beam, two pans on cords."""
    out = [W(-0.15, 0.15, 0.0, 0.10, -0.10, 0.10, WOOD, vis=(1, 2)),
           W(-0.01, 0.01, 0.10, 0.42, -0.01, 0.01, WOOD, vis=(1, 2)),
           W(-0.18, 0.18, 0.40, 0.41, -0.006, 0.006, IRON, vis=(1,))]
    for sx in (-1, 1):
        out.append(lkit.cord((sx * 0.17, 0.40, 0.0), (sx * 0.17, 0.18, 0.0), 0.002, ROPE))
        out.append(lathe([(0.0, 0.17), (0.06, 0.18), (0.065, 0.19), (0.0, 0.175)], 7, IRON, vis=(1,)))
        out[-1] = xf(out[-1], t=(sx * 0.17, 0.0, 0.0))
    return wear_all(out, wear)


def choba_set(kind):
    loot = kind == "zenibako"
    P = LPart("choba_set", budget="small", mass=8.0 if kind.startswith("zeni") else 2.0, anchor="floor",
              flat=not kind.startswith("zeni"))
    if kind == "desk":                                  # the things on the desk top
        P.adds(xfs(daifukucho(), ry=8.0, t=(-0.12, 0.0, 0.0)))
        P.adds(xfs(daifukucho(), ry=2.0, t=(-0.12, 0.038, 0.01)))
        P.adds(xfs(soroban(), ry=-5.0, t=(0.14, 0.0, -0.06)))
        P.adds(xfs(suzuribako(), ry=0.0, t=(0.16, 0.0, 0.10)))
        P.dim("ledger_w", 0.17, 0.174, tol=0.01)
    elif kind in ("zenibako", "zenibako_open"):
        P.adds(zenibako(open_=kind == "zenibako_open", wear="_w2" if kind == "zenibako_open" else None))
        top = 0.25 if loot else 0.22
        P.add(col(-0.20, 0.20, 0.0, top, -0.15, 0.15))
        if loot:
            P.loot_rect("lid", 0.25, -0.18, 0.18, -0.13, 0.13, rng=0.15, points=[(0.11, 0.25, 0.06)])
        else:
            P.add(stain(431, 0.0, 0.35, 0.25, sx=1.5))
        P.dim("w", 0.40, 0.40, tol=0.005)
    elif kind == "tenbin":
        P.adds(tenbin_scale())
        P.dim("h", 0.42, 0.42, tol=0.005)
    else:                                               # as left: ledgers splayed on the floor, the abacus upturned
        import props_shop as SH                         # B3a (read-only): the open ledger
        P.adds(xfs(SH.ledger(open_=True, wear="_w2"), ry=20.0, t=(0.0, 0.003, 0.0)))
        P.adds(xfs(daifukucho(wear="_w2", text_wear="_w2"), ry=-50.0, t=(0.35, 0.0, 0.20)))
        P.adds(rest(xfs(soroban(wear="_w2"), rx=180.0, ry=30.0, t=(-0.30, 0.0, 0.25)), 0.0))
        r = random.Random(432)
        for k in range(5):
            P.add(xf(W(-0.08, 0.08, 0.0, 0.002, -0.12, 0.12, PAPER, vis=(1,)), ry=r.uniform(0, 90),
                     t=(r.uniform(-0.4, 0.5), 0.001 * k, r.uniform(0.3, 0.6))))
            P.solids[-1].wear = "_w2"
        P.dim("ledger_w", 0.17, 0.174, tol=0.01)
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.notes.append("account clutter (BUILD_LIST jp_f_choba_set): ledgers (life-atlas cover 'daifukucho, Kyoho 15'), "
                   "abacus, writing box, coin box, balance; the coin box carries a loot point on its lid")
    return P


# ================================================================================================ 44 masu
def masu_box(s, h, wear=None, rice=False, mark=True):
    """A square measure: four boards and a bottom, a rice heap if full."""
    t = 0.01
    out = [W(-s / 2, s / 2, 0.0, 0.012, -s / 2, s / 2, WEATH, vis=(1,)),
           W(-s / 2, s / 2, 0.0, h, s / 2 - t, s / 2, WEATH, vis=(1,)),
           W(-s / 2, s / 2, 0.0, h, -s / 2, -s / 2 + t, WEATH, vis=(1,)),
           W(-s / 2, -s / 2 + t, 0.0, h, -s / 2 + t, s / 2 - t, WEATH, vis=(1,)),
           W(s / 2 - t, s / 2, 0.0, h, -s / 2 + t, s / 2 - t, WEATH, vis=(1,))]
    if rice:
        out.append(flat_poly([(-s / 2 + t, -s / 2 + t), (s / 2 - t, -s / 2 + t), (s / 2 - t, s / 2 - t),
                              (-s / 2 + t, s / 2 - t)][::-1], h - 0.004, RICE, vis=(1,)))
    return wear_all(out, wear)


def masu(kind):
    P = flatpart("masu", 2.0)
    if kind == "set":
        P.adds(masu_box(0.148, 0.082))
        P.adds(xfs(masu_box(0.12, 0.066), t=(0.20, 0.0, 0.02)))
        P.adds(xfs(masu_box(0.095, 0.052), t=(0.34, 0.0, -0.02)))
        P.add(pole((-0.10, 0.012, 0.14), (0.20, 0.012, 0.16), 0.012, WEATH, n=6, vis=(1,)))
        P.dim("sho_w", 0.148, 0.148, tol=0.003)
    elif kind == "to":                                  # the 1-to measure, heaped, the strickle across
        P.adds(masu_box(0.31, 0.18, rice=True))
        P.add(xf(mound(441, 0.0, 0.0, 0.14, 0.04, RICE, vis=(1,)), t=(0.0, 0.176, 0.0)))
        P.add(pole((-0.24, 0.20, 0.03), (0.24, 0.20, 0.05), 0.012, WEATH, n=6, vis=(1,)))
        P.dim("to_w", 0.31, 0.31, tol=0.005)
    else:                                               # as left: tipped over, the rice spilled
        P.adds(rest(xfs(masu_box(0.31, 0.18, wear="_w2"), rx=-95.0, ry=15.0), 0.0))
        P.add(mound(442, 0.05, 0.35, 0.25, 0.035, RICE, sx=1.5, wear="_w2", vis=(1,)))
        P.adds(xfs(masu_box(0.148, 0.082, wear="_w2"), ry=30.0, t=(-0.35, 0.0, 0.25)))
        P.add(pole((0.25, 0.012, 0.30), (0.45, 0.012, 0.05), 0.012, WEATH, n=6, vis=(1,)))
        P.dim("to_w", 0.31, 0.31, tol=0.005)
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WEATH, vis=(2,)))
    P.notes.append("masu measures and strickle (Kyo-masu standard 1669): rice shops and headmen (mount surface or floor)")
    return P


PROPS = [
    {"id": "jp_f_itoguruma", "cat": CAT, "ll": 37, "mount": "floor", "tiers": [1, 2], "refs": [], "models": [
        M("jp_f_itoguruma", "std", "intact", "Spinning wheel (itoguruma)", lambda: spinning("std")),
        M("jp_f_itoguruma_thread", "thread", "intact", "Spinning wheel with thread and a basket of cotton",
          lambda: spinning("thread")),
        M("jp_f_itoguruma_broken", "std", "broken", "Spinning wheel, the wheel knocked off and broken",
          lambda: spinning("broken")),
    ]},
    {"id": "jp_f_izaribata", "cat": CAT, "ll": 38, "mount": "floor", "tiers": [1, 2], "refs": [], "models": [
        M("jp_f_izaribata", "cloth", "intact", "Ground loom (izari-bata) with cloth on it", lambda: loom("cloth")),
        M("jp_f_izaribata_bare", "bare", "intact", "Ground loom, warped, no cloth yet", lambda: loom("bare")),
        M("jp_f_izaribata_cut", "cloth", "cut", "Ground loom, the warp cut, cloth across the floor",
          lambda: loom("cut")),
    ]},
    {"id": "jp_f_straw_work", "cat": CAT, "ll": 39, "mount": "floor", "tiers": [1], "refs": [], "models": [
        M("jp_f_straw_work_sandal", "sandal", "intact", "Straw work: a half-made sandal on a stool, a bundle",
          lambda: straw_work("sandal")),
        M("jp_f_straw_work_beating", "beating", "intact", "Straw-beating stone and mallet, a bundle",
          lambda: straw_work("beating")),
        M("jp_f_straw_work_scattered", "sandal", "scattered", "Straw work scattered, the stool tipped",
          lambda: straw_work("scattered")),
    ]},
    {"id": "jp_f_mi", "cat": CAT, "ll": 40, "mount": "floor", "tiers": [1, 2], "refs": [], "models": [
        M("jp_f_mi", "mi", "intact", "Winnowing basket (mi)", lambda: mi("mi")),
        M("jp_f_mi_wall", "mi_wall", "intact", "Winnowing basket hung on a wall peg", lambda: mi("mi_wall"),
          mount="wall"),
        M("jp_f_mi_furui", "furui", "intact", "Rice sieve (furui)", lambda: mi("furui")),
        M("jp_f_mi_spilled", "mi", "spilled", "Winnowing basket tipped, grain spilled", lambda: mi("spilled")),
    ]},
    {"id": "jp_f_usu", "cat": CAT, "ll": 41, "mount": "floor", "tiers": [1, 2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_usu"], "models": [
        M("jp_f_usu", "usu", "intact", "Rice mortar (usu) with a pounder", lambda: usu("usu")),
        M("jp_f_usu_mallet", "usu", "intact", "Rice mortar with a mallet pounder", lambda: usu("usu_mallet")),
        M("jp_f_usu_ishiusu", "ishiusu", "intact", "Stone hand mill on a straw mat", lambda: usu("ishiusu")),
        M("jp_f_usu_fallen", "usu", "fallen", "Rice mortar, the pounder fallen, dust in the bowl",
          lambda: usu("usu_fallen")),
        M("jp_f_usu_ishiusu_off", "ishiusu", "off", "Stone hand mill, the top stone off", lambda: usu("ishiusu_off")),
    ]},
    {"id": "jp_f_writing_box", "cat": CAT, "ll": 42, "mount": "surface", "tiers": [2, 3], "refs": [], "models": [
        M("jp_f_writing_box", "closed", "intact", "Writing box and a paper stack", lambda: writing("closed")),
        M("jp_f_writing_box_open", "open", "intact", "Writing box open: inkstone, brushes, paper",
          lambda: writing("open")),
        M("jp_f_writing_box_spilled", "open", "spilled", "Writing box knocked, papers slid, ink spilled",
          lambda: writing("spilled")),
    ]},
    {"id": "jp_f_choba_set", "cat": CAT, "ll": 43, "mount": "surface", "tiers": [2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_choba_set"], "models": [
        M("jp_f_choba_set_desk", "desk", "intact", "Ledgers, abacus and writing box for the desk",
          lambda: choba_set("desk")),
        M("jp_f_choba_set_zenibako", "zenibako", "intact", "Coin box (zenibako), locked", lambda: choba_set("zenibako"),
          mount="floor"),
        M("jp_f_choba_set_tenbin", "tenbin", "intact", "Money balance on its box", lambda: choba_set("tenbin")),
        M("jp_f_choba_set_scattered", "desk", "scattered", "Ledgers splayed, abacus upturned, papers",
          lambda: choba_set("scattered"), mount="floor"),
        M("jp_f_choba_set_zenibako_open", "zenibako", "open", "Coin box forced open, empty",
          lambda: choba_set("zenibako_open"), mount="floor"),
    ]},
    {"id": "jp_f_masu", "cat": CAT, "ll": 44, "mount": "surface", "tiers": [2, 3], "refs": [], "models": [
        M("jp_f_masu_set", "set", "intact", "Measures (masu), three sizes, and the strickle", lambda: masu("set")),
        M("jp_f_masu_to", "to", "intact", "A one-to measure heaped with rice, the strickle across",
          lambda: masu("to")),
        M("jp_f_masu_spilled", "to", "spilled", "Measure tipped, the rice spilled", lambda: masu("spilled"),
          mount="floor"),
    ]},
]
