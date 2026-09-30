"""Life layer D (research/interior/LIFE_LAYER.md items 27-36): living rooms and bedrooms.

Cushions, dropped clothes, toys and the sewing things are visual only (flat); standing screens, the clothes rack, the
go / shogi board and the tall candle stand carry collision; the straw bed is a thin Geometry slab + Roadway with
loot on it (as B3a's laid futon, like vanilla beds). Zabuton are T3 only (G1 A2-9).
"""
import math
import random

import lkit
from lkit import (core, box, prism, lathe, xf, xfs, flat_poly, W, board, pole, beam, rope_path, grid_sheet, col, disc,
                  stain, mound, soft_slab, LPart, M, rng, bipyramid, lod_box, wear_all, rest, cyl_col, place_group,
                  WOOD, WEATH, IRON, PALE, DARK, LACQ, BAMBOO, MUSHIRO, TAWARA, STACK, ROPE, PAPER, FUSUMA, INDIGO,
                  KINARI, RED, LITTER, LEAF)

CAT = "living"


def flatpart(name, mass=0.5, anchor="floor"):
    return LPart(name, budget="small", mass=mass, anchor=anchor, flat=True)


def dome_sheet(w, d, h, mat, nu=4, nv=4, seed=1, bump=0.0, wear=None, cx=0.0, cz=0.0, yaw=0.0, fn=None):
    """A soft up-facing surface (cloth lying on the floor): f(u, v) -> height, closed by nothing (seen from above)."""
    r = random.Random(seed)
    bumps = [(r.uniform(0, 1), r.uniform(0, 1), r.uniform(0.3, 1.0)) for _ in range(4)]

    def f(u, v):
        x, z = -w / 2 + w * u, -d / 2 + d * v
        edge = min(u, 1 - u, v, 1 - v)
        y = h * min(1.0, edge * 6.0)
        for bu, bv, a in bumps:
            y += bump * a * math.exp(-((u - bu) ** 2 + (v - bv) ** 2) * 20)
        if fn:
            x, y, z = fn(u, v, x, y, z)
        return (x, y + 0.002, z)
    s = grid_sheet(f, nu, nv, mat, vis=(1,), two_sided=False, wear=wear)
    return xf(s, ry=yaw, t=(cx, 0.0, cz))


# ================================================================================================ 27 enza / zabuton (★)
def enza_disc(wear=None, vis=(1,)):
    """Round coiled-straw cushion d 0.40, 3 cm, a slightly domed top."""
    s = lathe([(0.0, 0.0), (0.19, 0.0), (0.20, 0.012), (0.19, 0.028), (0.10, 0.034), (0.0, 0.035)], 12, MUSHIRO,
              vis=vis, wear=wear)
    rings = [lkit.rope_ring(r_, 0.03 - 0.02 * (r_ / 0.2) ** 2 + 0.002, 0.012, TAWARA, 12, vis=(1,), proud=0.002)
             for r_ in (0.07, 0.13)] if vis == (1,) else []
    return [s] + rings


def enza(kind):
    anchor = "wall" if kind == "enza_kicked" else "floor"
    P = flatpart("enza", 0.8, anchor)
    if kind == "enza":
        P.adds(enza_disc())
        P.dim("d", 0.40, 0.40, tol=0.005)
    elif kind == "enza_stack3":
        for k in range(3):
            ss = enza_disc(wear="_w1" if k else "_w0")
            P.adds(xfs(ss if k == 2 else ss[:1], ry=k * 21.0, t=(0.01 * k, 0.034 * k, -0.008 * k)))
        P.dim("d", 0.40, 0.40, tol=0.005)
    elif kind == "enza_kicked":                         # as left: kicked against the wall, standing on its edge
        ss = xfs(enza_disc(wear="_w2"), rx=75.0)        # the top faces the room
        lo = min(v[1] for q in ss for v in q.verts)
        zmin = min(v[2] for q in ss for v in q.verts)
        P.adds(xfs(ss, t=(0.0, -lo, 0.003 - zmin)))
        P.add(stain(271, 0.25, 0.25, 0.20, sx=1.4))
        P.dim("d", 0.40, 0.40, tol=0.005)
    elif kind in ("zabuton", "zabuton_stack3"):
        n = 1 if kind == "zabuton" else 3
        for k in range(n):
            s = soft_slab(0.55, 0.60, 0.06, INDIGO, n=2, vis=(1,))
            P.add(xf(s, ry=90.0 + k * 5.0, t=(0.0, 0.055 * k, 0.0)))
            for sx in (-1, 1):                          # the corner tufts
                for sz in (-1, 1):
                    P.add(box(sx * 0.2 - 0.01, sx * 0.2 + 0.01, 0.055 * k + 0.05, 0.055 * k + 0.065, sz * 0.22 - 0.01,
                              sz * 0.22 + 0.01, KINARI, vis=(1,)))
        P.dim("w", 0.55, 0.55, tol=0.005)
    else:                                               # zabuton folded over and shoved askew
        s = soft_slab(0.55, 0.30, 0.11, INDIGO, n=3, vis=(1,), wear="_w2")
        P.add(xf(s, ry=70.0))
        P.add(stain(272, 0.1, 0.1, 0.25, sx=1.3))
        P.dim("w", 0.55, 0.55, tol=0.005)
    P.add(lod_box([s for s in P.solids if 1 in s.vis], MUSHIRO if kind.startswith("enza") else INDIGO, vis=(2,)))
    P.notes.append("round straw enza everywhere; cotton zabuton T3 only (G1 A2-9); no Geometry (walk over)")
    return P


# ================================================================================================ 28 byobu (★)
def screen_panel(w, h, torn=False, frame=WOOD, wear=None, feet=0.0, vis_lo=(2,)):
    """One screen panel standing on y = feet: a 3 cm frame, paper both faces (the fusuma paper), in the x-y plane."""
    t = 0.022
    out = [W(-w / 2, w / 2, feet, feet + 0.03, -t / 2, t / 2, frame, vis=(1,)),
           W(-w / 2, w / 2, feet + h - 0.03, feet + h, -t / 2, t / 2, frame, vis=(1,)),
           W(-w / 2, -w / 2 + 0.03, feet + 0.03, feet + h - 0.03, -t / 2, t / 2, frame, vis=(1,)),
           W(w / 2 - 0.03, w / 2, feet + 0.03, feet + h - 0.03, -t / 2, t / 2, frame, vis=(1,))]
    pw = "_w2" if (torn or wear) else "_w1"
    for zz, n in ((0.005, 1.0), (-0.005, -1.0)):
        def f(u, v, zz=zz):
            return (-w / 2 + 0.03 + (w - 0.06) * u, feet + h - 0.03 - (h - 0.06) * v, zz)
        g = grid_sheet(f, 2, 3, FUSUMA, vis=(1,), two_sided=False, wear=pw)
        if n < 0:
            g = xf(g, ry=180.0)
            g = xf(g, t=(0.0, 0.0, 0.0))
        if torn:                                        # a torn-out hole: drop two cells
            keep = [i for i in range(len(g.faces)) if i not in (2, 3)]
            g.faces = [g.faces[i] for i in keep]
            g.fn = [g.fn[i] for i in keep]
            g.fm = [g.fm[i] for i in keep]
            g.fuv = [g.fuv[i] for i in keep]
            g.normals = g.fn
        out.append(g)
    out.append(W(-w / 2, w / 2, feet, feet + h, -t / 2, t / 2, FUSUMA, vis=vis_lo))
    return wear_all(out, wear)


def byobu(kind):
    fallen = kind.endswith("fallen")
    P = LPart("byobu", budget="furniture", res3=True, mass=6.0, anchor="floor", flat=fallen)
    if kind.startswith("makura"):
        w, h = 0.60, 0.90
        ang = 55.0                                      # each leaf 55 deg off the line: a zigzag standing on its own
        pa = xfs(screen_panel(w, h, torn=fallen), t=(-w / 2, 0.0, 0.0))
        pb = xfs(screen_panel(w, h, torn=False), t=(w / 2, 0.0, 0.0))
        left = xfs(pa, ry=-ang * 0.5, pivot=(0.0, 0.0, 0.0))
        right = xfs(pb, ry=ang * 0.5, pivot=(0.0, 0.0, 0.0))
        for q in pa[-1:] + pb[-1:]:
            pass
        ss = left + right
        cols = [lkit.fkit.col_solid(xf(box(-w, 0.0, 0.0, h, -0.011, 0.011, WOOD), ry=-ang * 0.5)),
                lkit.fkit.col_solid(xf(box(0.0, w, 0.0, h, -0.011, 0.011, WOOD), ry=ang * 0.5))]
        ss.append(W(-0.5, 0.5, 0.0, h, -0.1, 0.1, FUSUMA, vis=(3,)))
        if not fallen:
            P.adds(ss)
            P.adds(cols)
        else:                                           # knocked flat, paper torn
            P.adds(rest(xfs([q for q in ss if 3 not in q.vis], rx=-90.0, t=(0.0, 0.0, 0.0)), 0.0))
            P.add(W(-0.5, 0.5, 0.0, 0.02, -0.4, 0.4, FUSUMA, vis=(3,)))
            P.add(stain(281, 0.1, 0.5, 0.3, sx=1.5))
        P.dim("panel_h", 0.90, h, tol=0.005)
    else:                                               # tsuitate: one standing panel 1.20 x 1.40 on two feet
        w, h, feet = 1.20, 1.30, 0.10
        ss = screen_panel(w, h, torn=fallen, feet=feet)
        for sx in (-1, 1):
            ss.append(W(sx * 0.45 - 0.04, sx * 0.45 + 0.04, 0.0, feet + 0.08, -0.22, 0.22, WOOD, vis=(1, 2)))
        ss.append(W(-0.6, 0.6, 0.0, h + feet, -0.2, 0.2, FUSUMA, vis=(3,)))
        if not fallen:
            P.adds(ss)
            P.add(col(-w / 2, w / 2, feet, feet + h, -0.011, 0.011, WOOD))
            for sx in (-1, 1):
                P.add(col(sx * 0.45 - 0.04, sx * 0.45 + 0.04, 0.0, feet, -0.22, 0.22, WOOD))
        else:
            P.adds(rest(xfs([q for q in ss if 3 not in q.vis], rx=-88.0, ry=10.0), 0.0))
            P.add(W(-0.6, 0.6, 0.0, 0.02, -0.5, 0.5, FUSUMA, vis=(3,)))
            P.add(stain(282, 0.2, 0.8, 0.35, sx=1.6))
        P.dim("h", 1.40, h + feet, tol=0.005)
    P.notes.append("low bedding screen (makura-byobu, 2 leaves) and entrance screen (tsuitate); standing ones against "
                   "a wall or across a corner only (BUILD_LIST jp_f_byobu); fallen = no Geometry")
    return P


# ================================================================================================ 29 iko (★)
def iko_frame(mat=LACQ, wear=None):
    """Clothes rack 1.50 x 0.40 x 1.50: two posts on feet, a top rail with upturned ends, a lower rail."""
    out = []
    for sx in (-1, 1):
        out.append(W(sx * 0.65 - 0.025, sx * 0.65 + 0.025, 0.05, 1.45, -0.02, 0.02, mat, vis=(1, 2)))
        out.append(W(sx * 0.65 - 0.035, sx * 0.65 + 0.035, 0.0, 0.05, -0.20, 0.20, mat, vis=(1, 2)))
    out.append(W(-0.75, 0.75, 1.45, 1.49, -0.022, 0.022, mat, vis=(1, 2)))
    for sx in (-1, 1):
        out.append(prism([(0.0, 0.0), (0.06, 0.0), (0.075, 0.035), (0.02, 0.012)], "z", -0.022, 0.022, mat, vis=(1,)))
        out[-1] = xf(out[-1], ry=0.0 if sx > 0 else 180.0, t=(sx * 0.75, 1.46, 0.0))
    out.append(W(-0.65, 0.65, 1.00, 1.03, -0.018, 0.018, mat, vis=(1,)))
    out.append(W(-0.75, 0.75, 0.0, 1.50, -0.2, 0.2, mat, vis=(3,)))
    return wear_all(out, wear)


def robe_on_rail(mat=INDIGO, wear=None, y=1.49, span=1.30, drop=1.05):
    """A kimono spread over the top rail, back outward, sleeves out (tagasode): a sheet over the rail, hanging on
    both sides (the front side longer)."""
    out = []
    for side, L in ((1, drop), (-1, drop * 0.55)):
        def f(u, v, side=side, L=L):
            x = -span / 2 + span * u
            sleeve = abs(u - 0.5) > 0.27
            Lx = L * (0.62 if sleeve else 1.0)
            return (x, y + 0.012 - Lx * v, side * (0.025 + 0.05 * v + 0.012 * math.sin(6 * math.pi * u) * v))
        out.append(grid_sheet(f, 6, 2, mat, vis=(1,), two_sided=True, wear=wear))
    out.append(W(-span / 2, span / 2, y - drop, y + 0.01, -0.05, 0.05, mat, vis=(2,)))
    return out


def iko(kind):
    fallen = kind == "fallen"
    P = LPart("iko", budget="furniture", res3=True, mass=7.0, anchor="floor", flat=fallen)
    if kind == "robe":
        P.adds(iko_frame())
        P.adds(robe_on_rail())
    elif kind == "plain":
        P.adds(iko_frame(WOOD))
        P.adds(robe_on_rail(KINARI, span=1.20, drop=0.95))
    elif kind == "empty":
        P.adds(iko_frame(WOOD))
        P.add(pole((-0.5, 1.40, 0.02), (-0.2, 1.47, 0.02), 0.012, INDIGO, n=4, vis=(1,)))   # an obi end over the rail
    else:                                               # as left: the rack fallen on its back, the robe on the mat
        fr = [q for q in iko_frame(LACQ, wear="_w2") if 3 not in q.vis]
        P.adds(rest(xfs(fr, rx=-90.0, t=(0.0, 0.0, 0.0)), 0.0))
        P.add(dome_sheet(1.2, 0.9, 0.04, INDIGO, 5, 3, seed=291, bump=0.05, wear="_w2", cx=0.1, cz=0.9, yaw=12.0))
        P.add(W(-0.75, 0.75, 0.0, 0.10, -0.2, 1.3, LACQ, vis=(3,)))
        P.add(stain(291, 0.0, 0.6, 0.4, sx=1.6))
    if not fallen:
        P.add(col(-0.76, 0.76, 0.05, 1.50, -0.07, 0.07, WOOD))
        for sx in (-1, 1):
            P.add(col(sx * 0.65 - 0.035, sx * 0.65 + 0.035, 0.0, 0.05, -0.20, 0.20, WOOD))
    P.dim("w", 1.50, 1.50, tol=0.005)
    P.dim("h", 1.50, 1.49, tol=0.02)
    P.notes.append("clothes rack (iko) with a robe spread over it; 1.5 m wide: along walls only (BUILD_LIST jp_f_iko)")
    return P


# ================================================================================================ 30 dropped clothes
def kimono_flat(mat=INDIGO, wear="_w2", seed=1, cx=0.0, cz=0.0, yaw=0.0, L=1.20, W_=0.62):
    """A kimono dropped on the mat: body and sleeves as low rumpled sheets, a collar band."""
    out = [dome_sheet(W_, L, 0.03, mat, 3, 4, seed=seed, bump=0.05, wear=wear)]
    for sx in (-1, 1):
        out.append(xf(dome_sheet(0.40, 0.45, 0.02, mat, 2, 2, seed=seed + sx, bump=0.04, wear=wear),
                      ry=sx * 15.0, t=(sx * (W_ / 2 + 0.17), 0.0, -L / 2 + 0.30)))
    out.append(xf(W(-0.03, 0.03, 0.0, 0.035, -0.35, 0.10, KINARI if mat != KINARI else INDIGO, vis=(1,)), ry=20.0,
                  t=(0.05, 0.0, -L / 2 + 0.25)))
    return xfs(out, ry=yaw, t=(cx, 0.0, cz))


def obi_ribbon(pts, w=0.10, mat=INDIGO, wear="_w2", h=0.012):
    """A long sash lying in loops: a strip along a polyline (up faces only + low sides)."""
    quads, normals = [], []
    for i in range(len(pts) - 1):
        (x0, z0), (x1, z1) = pts[i], pts[i + 1]
        dx, dz = x1 - x0, z1 - z0
        L = math.hypot(dx, dz) or 1.0
        nx, nz = -dz / L * w / 2, dx / L * w / 2
        quads.append([(x0 - nx, h, z0 - nz), (x0 + nx, h, z0 + nz), (x1 + nx, h, z1 + nz), (x1 - nx, h, z1 - nz)])
        normals.append((0.0, 1.0, 0.0))
    s = core.sheet(quads, mat, normals, vis=(1,))
    s.finalize()
    s.wear = wear
    return s


def clothes(kind):
    P = flatpart("clothes", 1.0)
    if kind == "kimono":
        P.adds(kimono_flat(seed=301, yaw=10.0))
    elif kind == "kimono_obi":
        P.adds(kimono_flat(KINARI, seed=302, yaw=-20.0))
        P.add(obi_ribbon([(-0.6, 0.5), (-0.2, 0.62), (0.2, 0.45), (0.35, 0.10), (0.1, -0.1), (0.45, -0.35),
                          (0.8, -0.2)], w=0.14))
    else:                                               # a short jacket (haori) and a sash, dropped by the bedding
        P.adds(kimono_flat(INDIGO, seed=303, yaw=35.0, L=0.80, W_=0.58))
        P.add(obi_ribbon([(0.5, 0.4), (0.7, 0.1), (0.55, -0.2), (0.85, -0.4)], w=0.08, mat=KINARI))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], INDIGO, vis=(2,)))
    P.dim("kimono_L", 1.20 if kind != "haori" else 0.80, 1.20 if kind != "haori" else 0.80, tol=0.01)
    P.notes.append("clothes dropped on the mat (the abandoned layer); no Geometry")
    return P


# ================================================================================================ 31 sewing
def haribako(wear=None, drawer_out=False):
    """Sewing box 0.32 x 0.22 x 0.20: two drawers, a tray lid, the pincushion on a short post."""
    out = [W(-0.16, 0.16, 0.0, 0.20, -0.11, 0.11, vis=(1, 2)),
           W(-0.165, 0.165, 0.20, 0.215, -0.115, 0.115, vis=(1,))]
    for k, y0 in enumerate((0.02, 0.105)):
        dz = 0.12 if (drawer_out and k == 0) else 0.0
        out.append(W(-0.14, 0.14, y0, y0 + 0.075, 0.11 + dz - 0.004, 0.113 + dz, vis=(1,)))
        out.append(box(-0.012, 0.012, y0 + 0.03, y0 + 0.045, 0.113 + dz, 0.12 + dz, IRON, vis=(1,)))
        if dz:
            out.append(W(-0.14, 0.14, y0, y0 + 0.06, 0.0 + dz, 0.11 + dz, vis=(1,)))
    out.append(box(0.08, 0.10, 0.215, 0.33, -0.01, 0.01, WOOD, vis=(1,)))
    out.append(xf(soft_slab(0.08, 0.06, 0.04, RED, n=2, vis=(1,)), t=(0.09, 0.33, 0.0)))
    return wear_all(out, wear)


def spool(cx, cz, lying=True, mat=INDIGO):
    s = lathe([(0.0, 0.0), (0.02, 0.0), (0.02, 0.006), (0.015, 0.008), (0.015, 0.042), (0.02, 0.044), (0.02, 0.05),
               (0.0, 0.05)], 6, WOOD, vis=(1,))
    t = lathe([(0.016, 0.008), (0.016, 0.042)], 6, mat, vis=(1,))
    ss = [s, t]
    if lying:
        ss = rest(xfs(ss, rz=90.0), 0.0)
    return xfs(ss, t=(cx, 0.0, cz))


def sewing(kind):
    P = flatpart("sewing", 2.0)
    if kind == "box":
        P.adds(haribako())
    elif kind == "work":
        P.adds(haribako())
        P.add(dome_sheet(0.55, 0.40, 0.015, KINARI, 3, 2, seed=311, bump=0.02, cx=0.10, cz=0.45, yaw=-8.0))
        P.add(obi_ribbon([(-0.10, 0.40), (0.05, 0.48), (0.30, 0.46)], w=0.01, mat=INDIGO, wear="_w1", h=0.02))
        P.adds(spool(0.35, 0.20))
    else:                                               # as left: a drawer out, spools rolled, the garment trodden
        P.adds(haribako(wear="_w2", drawer_out=True))
        P.add(dome_sheet(0.55, 0.40, 0.015, KINARI, 3, 2, seed=312, bump=0.03, wear="_w2", cx=-0.35, cz=0.45,
                         yaw=30.0))
        P.adds(spool(0.30, 0.35))
        P.adds(spool(0.45, 0.10, mat=RED))
        P.add(stain(313, 0.1, 0.4, 0.3, sx=1.5))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("box_w", 0.32, 0.32, tol=0.005)
    P.notes.append("sewing box (haribako) with a half-sewn garment (mount floor or surface)")
    return P


# ================================================================================================ 32 mirror stand
def kyodai(open_=False, wear=None):
    """Mirror stand: a drawer box 0.28 x 0.22 x 0.14, two posts to 0.52, a round mirror d 0.20 in its hanger,
    covered with a cloth (kagami-kake) unless open."""
    out = [W(-0.14, 0.14, 0.0, 0.14, -0.11, 0.11, LACQ, vis=(1, 2)),
           W(-0.10, 0.10, 0.03, 0.10, 0.11, 0.114, LACQ, vis=(1,))]
    for sx in (-1, 1):
        out.append(W(sx * 0.10 - 0.012, sx * 0.10 + 0.012, 0.14, 0.52, -0.03, -0.006, LACQ, vis=(1, 2)))
    out.append(W(-0.11, 0.11, 0.50, 0.52, -0.03, -0.006, LACQ, vis=(1,)))
    mirror = lathe([(0.0, 0.0), (0.10, 0.0), (0.10, 0.012), (0.0, 0.012)], 10, IRON, vis=(1,))
    out.append(xf(mirror, rx=80.0, t=(0.0, 0.34, -0.01)))
    if not open_:                                       # the cover cloth hanging over the face
        def f(u, v):
            return (-0.12 + 0.24 * u, 0.46 - 0.26 * v, 0.02 + 0.03 * v + 0.01 * math.sin(math.pi * u))
        out.append(grid_sheet(f, 2, 2, RED, vis=(1,), wear="_w1"))
    out.append(W(-0.14, 0.14, 0.0, 0.52, -0.11, 0.11, LACQ, vis=(2,)) if False else
               box(-0.14, 0.14, 0.0, 0.52, -0.11, 0.11, LACQ, vis=(2,)))
    return wear_all(out, wear)


def mirror_stand(kind):
    P = flatpart("mirror_stand", 3.0)
    if kind == "covered":
        P.adds(kyodai())
    elif kind == "open":
        P.adds(kyodai(open_=True))
    else:                                               # as left: knocked over, the mirror out on the mat, a comb
        ss = [q for q in kyodai(open_=True, wear="_w2") if 2 not in q.vis or 1 in q.vis]
        P.adds(rest(xfs(ss, rx=-85.0, ry=20.0), 0.0))
        P.add(xf(lathe([(0.0, 0.0), (0.10, 0.0), (0.10, 0.012), (0.0, 0.012)], 10, IRON, vis=(1,)),
                 t=(0.30, 0.0, 0.35)))
        P.add(xf(box(-0.05, 0.05, 0.0, 0.006, -0.02, 0.02, LACQ, vis=(1,)), ry=30.0, t=(-0.2, 0.0, 0.4)))
        P.add(stain(321, 0.1, 0.3, 0.25, sx=1.4))
    P.dim("h", 0.52, 0.52, tol=0.01)
    P.notes.append("mirror stand (kyodai), bronze mirror under its cloth (LIFE_LAYER_ERA 32)")
    return P


# ================================================================================================ 33 go / shogi
def board_game(game="go", wear=None):
    """Go board 0.45 x 0.42, 0.12 thick on 0.10 legs (top 0.22); shogi board 0.36 x 0.33 on legs (top 0.20)."""
    if game == "go":
        w, d, t, leg, nl = 0.45, 0.42, 0.12, 0.10, 19
    else:
        w, d, t, leg, nl = 0.36, 0.33, 0.10, 0.10, 10
    top = leg + t
    out = [W(-w / 2, w / 2, leg, top, -d / 2, d / 2, WOOD, vis=(1, 2))]
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * (w / 2 - 0.06) - 0.035, sx * (w / 2 - 0.06) + 0.035, 0.0, leg, sz * (d / 2 - 0.06) - 0.035,
                         sz * (d / 2 - 0.06) + 0.035, WOOD, vis=(1,)))
    m = 0.03
    for k in range(nl):                                 # the grid: up-facing hair quads
        x = -w / 2 + m + (w - 2 * m) * k / (nl - 1)
        z = -d / 2 + m + (d - 2 * m) * k / (nl - 1)
        out.append(flat_poly([(x - 0.0012, -d / 2 + m), (x + 0.0012, -d / 2 + m), (x + 0.0012, d / 2 - m),
                              (x - 0.0012, d / 2 - m)][::-1], top + 0.0008, LACQ, vis=(1,)))
        out.append(flat_poly([(-w / 2 + m, z - 0.0012), (w / 2 - m, z - 0.0012), (w / 2 - m, z + 0.0012),
                              (-w / 2 + m, z + 0.0012)][::-1], top + 0.0008, LACQ, vis=(1,)))
    return wear_all(out, wear), top, w, d


def stones(n, seed, cx, cz, spread, y=0.0):
    r = random.Random(seed)
    out = []
    for k in range(n):
        out.append(bipyramid((cx + r.uniform(-spread, spread), y + 0.004, cz + r.uniform(-spread, spread)), 0.011,
                             0.004, 0.011, LACQ if k % 2 else PALE, n=4, phase=r.uniform(0, 1)))
    return out


def goke(cx, cz, mat=WOOD):
    return [lathe([(0.0, 0.0), (0.05, 0.0), (0.065, 0.04), (0.055, 0.08), (0.0, 0.085)], 6, mat, vis=(1,))] if False \
        else [xf(lathe([(0.0, 0.0), (0.05, 0.0), (0.065, 0.04), (0.055, 0.08), (0.0, 0.085)], 6, mat, vis=(1,)),
                 t=(cx, 0.0, cz))]


def shogi_pieces(n, seed, cx, cz, spread, y):
    r = random.Random(seed)
    out = []
    for k in range(n):
        p = prism([(-0.012, 0.0), (0.012, 0.0), (0.009, 0.022), (0.0, 0.028), (-0.009, 0.022)], "y", 0.0, 0.006, WEATH,
                  vis=(1,))
        out.append(xf(p, ry=r.uniform(0, 360), t=(cx + r.uniform(-spread, spread), y, cz + r.uniform(-spread, spread))))
    return out


def goban(kind):
    game = "go" if kind.startswith("go") else "shogi"
    scattered = kind.endswith("scattered")
    P = LPart("goban", budget="small", mass=12.0, anchor="floor")
    ss, top, w, d = board_game(game, wear="_w2" if scattered else None)
    P.adds(ss)
    if game == "go":
        if not scattered:
            P.adds(goke(0.32, 0.10, LACQ))
            P.adds(goke(-0.32, -0.08, WOOD))
            P.adds(stones(14, 331, -0.05, 0.02, 0.15, top))
        else:                                           # a bowl tipped, stones strewn over the mat
            P.adds(goke(-0.32, -0.08, WOOD))
            P.adds(rest(xfs(goke(0.0, 0.0, LACQ), rz=100.0, ry=30.0, t=(0.40, 0.0, 0.20)), 0.0))
            P.adds(stones(12, 332, 0.45, 0.40, 0.22))
            P.adds(stones(6, 333, 0.0, 0.0, 0.15, top))
    else:
        if not scattered:
            P.adds(shogi_pieces(12, 334, 0.0, 0.0, 0.13, top))
        else:
            P.adds(shogi_pieces(8, 335, 0.0, 0.0, 0.13, top))
            P.adds(shogi_pieces(10, 336, 0.35, 0.30, 0.20, 0.0))
    P.add(col(-w / 2, w / 2, 0.0, top, -d / 2, d / 2, WOOD))
    if not scattered:
        P.loot_rect("board", top, -w / 2 + 0.05, w / 2 - 0.05, -d / 2 + 0.05, d / 2 - 0.05, rng=0.15,
                    points=[(w / 2 - 0.07, top, d / 2 - 0.07)])
    P.dim("top", 0.22 if game == "go" else 0.20, top, tol=0.005)
    P.notes.append("go / shogi board on legs; loot on the board corner when intact")
    return P


# ================================================================================================ 34 toys
def koma(cx, cz, lying=True):
    s = lathe([(0.0, 0.0), (0.02, 0.012), (0.035, 0.03), (0.034, 0.04), (0.006, 0.045), (0.006, 0.07), (0.0, 0.07)], 7,
              RED, vis=(1,), wear="_w1")
    ss = [s]
    if lying:
        ss = rest(xfs(ss, rz=70.0), 0.0)
    return xfs(ss, t=(cx, 0.0, cz))


def hagoita(cx, cz, yaw=0.0):
    p = prism([(-0.05, 0.0), (0.05, 0.0), (0.06, 0.20), (0.04, 0.26), (-0.04, 0.26), (-0.06, 0.20)], "y", 0.0, 0.008,
              WEATH, vis=(1,))
    h = box(-0.012, 0.012, 0.0, 0.008, -0.12, 0.0, WEATH, vis=(1,))
    shuttle = [lkit.bipyramid((0.0, 0.01, 0.0), 0.01, 0.01, 0.01, DARK, n=4)]
    feathers = prism([(-0.02, 0.0), (0.02, 0.0), (0.0, 0.05)], "z", -0.001, 0.001, PAPER, vis=(1,))
    shuttle.append(xf(feathers, rx=-60.0, t=(0.0, 0.01, 0.0)))
    return xfs([xf(p, rx=0.0, t=(0.0, 0.0, 0.0)), h], ry=yaw, t=(cx, 0.0, cz)) + xfs(shuttle, t=(cx + 0.15, 0.0, cz))


def doll(cx, cz, yaw=0.0, wear="_w2"):
    """A small cloth doll lying on its back: kimono body, head, a sash."""
    body = lathe([(0.0, 0.0), (0.05, 0.0), (0.04, 0.12), (0.02, 0.16), (0.0, 0.16)], 6, RED, vis=(1,), wear=wear)
    head = lathe([(0.0, 0.16), (0.025, 0.17), (0.028, 0.19), (0.02, 0.21), (0.0, 0.215)], 6, KINARI, vis=(1,))
    hair = lathe([(0.02, 0.19), (0.03, 0.205), (0.0, 0.225)], 6, LACQ, vis=(1,))
    sash = lathe([(0.046, 0.06), (0.046, 0.085)], 6, INDIGO, vis=(1,))
    ss = rest(xfs([body, head, hair, sash], rx=-88.0, ry=yaw), 0.0)
    return xfs(ss, t=(cx, 0.0, cz))


def denden(cx, cz, yaw=0.0):
    drum = lathe([(0.0, 0.0), (0.04, 0.0), (0.04, 0.025), (0.0, 0.025)], 8, KINARI, vis=(1,))
    stick = box(-0.005, 0.005, -0.12, 0.0, -0.005, 0.005, BAMBOO, vis=(1,))
    ss = [xf(drum, rx=90.0, t=(0.0, 0.0, -0.012)), stick]
    ss = rest(xfs(ss, rz=90.0, ry=yaw), 0.0)
    return xfs(ss, t=(cx, 0.0, cz))


def toys(kind):
    P = flatpart("toys", 0.3)
    if kind == "koma":
        P.adds(koma(0.0, 0.0))
        P.adds(rope_path([(0.05, 0.004, 0.02), (0.15, 0.004, 0.08), (0.22, 0.004, 0.02), (0.28, 0.004, 0.10)], 0.003,
                         ROPE, n=3, vis=(1,)))
    elif kind == "hagoita":
        P.adds(hagoita(0.0, 0.0, 20.0))
    elif kind == "doll":
        P.adds(doll(0.0, 0.0, 30.0))
    else:                                               # scattered together by the bedding: the quiet sad touch
        P.adds(koma(0.25, 0.10))
        P.adds(hagoita(-0.20, 0.05, -35.0))
        P.adds(doll(0.05, 0.35, 60.0))
        P.adds(denden(0.35, 0.40, 15.0))
        P.add(stain(341, 0.05, 0.2, 0.3, sx=1.5))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WEATH, vis=(2,)))
    P.dim("koma_d", 0.07, 0.07, tol=0.01)
    P.notes.append("children's toys that pass 1730 (LIFE_LAYER_ERA 34): top, battledore + shuttlecock, a rag doll, "
                   "a rattle drum; no kendama, no daruma")
    return P


# ================================================================================================ 35 shokudai
def shokudai_parts(tall=True, wear=None, candle=True):
    h = 0.75 if tall else 0.35
    mat = LACQ if tall else IRON
    out = [lathe([(0.0, 0.0), (0.12, 0.0), (0.10, 0.03), (0.03, 0.06), (0.0, 0.06)], 8, mat, vis=(1,)),
           lkit.lcyl("y", 0.0, 0.0, 0.012, 0.06, h, mat, n=6, vis=(1,)),
           lathe([(0.0, h), (0.07, h), (0.075, h + 0.015), (0.0, h + 0.01)], 8, mat, vis=(1,)),
           box(-0.002, 0.002, h + 0.01, h + 0.05, -0.002, 0.002, IRON, vis=(1,))]
    if candle:
        out.append(lkit.lcyl("y", 0.0, 0.0, 0.016, h + 0.012, h + 0.012 + (0.12 if tall else 0.08), PAPER, n=6,
                             vis=(1,)))
    out.append(lathe([(0.0, 0.0), (0.12, 0.0), (0.02, 0.06), (0.02, h), (0.0, h + 0.1)], 4, mat, vis=(2,),
                     smooth=False))
    return wear_all(out, wear), h


def shokudai(kind):
    tipped = kind == "tipped"
    P = LPart("shokudai", budget="small", mass=3.0, anchor="floor", flat=(kind != "tall"))
    if kind in ("tall", "short"):
        ss, h = shokudai_parts(kind == "tall")
        P.adds(ss)
        if kind == "tall":
            P.add(col(-0.10, 0.10, 0.0, h + 0.1, -0.10, 0.10, WOOD))
        P.dim("h", 0.75 if kind == "tall" else 0.35, h, tol=0.005)
    else:                                               # as left: knocked over, the candle broken in two
        ss, h = shokudai_parts(True, wear="_w2", candle=False)
        P.adds(rest(xfs(ss, rz=88.0, ry=25.0), 0.0))
        for k, (x, z, a) in enumerate(((0.40, 0.35, 20.0), (0.52, 0.30, 70.0))):
            c = lkit.lcyl("x", 0.016, 0.0, 0.016, -0.04, 0.04, PAPER, n=6, vis=(1,))
            P.add(xf(c, ry=a, t=(x, 0.0, z)))
        P.add(stain(351, 0.3, 0.2, 0.25, sx=1.5))
        P.dim("h", 0.75, h, tol=0.005)
    P.notes.append("candle stand (rich houses, T3 / upper only: candles were dear); unlit")
    return P


# ================================================================================================ 36 straw bed
def straw_bed(kind):
    P = LPart("straw_bed", budget="small", mass=10.0, anchor="floor")
    L, Wd, h = 1.80, 0.90, 0.20
    scattered = kind == "scattered"

    def pile(u, v, x, y, z):
        return (x, y * (0.4 if scattered else 1.0), z)
    P.add(dome_sheet(L + (0.3 if scattered else 0.0), Wd + (0.3 if scattered else 0.0), h, STACK, 6, 4, seed=361,
                     bump=0.07, wear="_w2" if scattered else "_w1", fn=pile))
    top = h * (0.4 if scattered else 1.0)
    if not scattered:                                   # a straw mat over the heap
        P.add(dome_sheet(1.60, 0.80, 0.02, MUSHIRO, 3, 2, seed=362, bump=0.0, fn=lambda u, v, x, y, z: (x, y + h - 0.01, z)))
        top = h + 0.012
    if kind == "quilt":                                 # the paper quilt (kamibusuma) thrown back
        P.add(dome_sheet(0.80, 0.85, 0.03, PAPER, 2, 2, seed=363, bump=0.03, wear="_w2", cx=0.40,
                         fn=lambda u, v, x, y, z: (x, y + h, z)))
    if scattered:
        P.add(dome_sheet(0.75, 0.70, 0.02, PAPER, 2, 2, seed=364, bump=0.04, wear="_w2", cx=0.9, cz=0.5, yaw=30.0))
    P.add(W(-L / 2, L / 2, 0.0, top, -Wd / 2, Wd / 2, STACK, vis=(2,)))
    slab = max(0.06, top - 0.03)
    P.add(col(-L / 2, L / 2, 0.0, slab, -Wd / 2, Wd / 2, STACK))
    P.road([(-L / 2, slab, -Wd / 2), (L / 2, slab, -Wd / 2), (L / 2, slab, Wd / 2), (-L / 2, slab, Wd / 2)], "tatami")
    import props_bedding as PB                          # B3a (read-only): the highest Res 1 face at a point
    pts = [(-0.45, 0.0, 0.10), (0.35, 0.0, -0.10)]
    fixed = [(x, PB.top_point_y(P, x, z), z) for x, _, z in pts]
    P.loot_rect("bed", fixed[0][1], -L / 2 + 0.1, L / 2 - 0.1, -Wd / 2 + 0.1, Wd / 2 - 0.1, rng=0.4, points=fixed)
    P.dim("L", 1.80, L, tol=0.01)
    P.notes.append("the poor's bed (T1): a straw heap under a straw mat, a paper quilt; a thin Geometry slab + Roadway "
                   "like the laid futon (walk over it, loot on it)")
    return P


PROPS = [
    {"id": "jp_f_enza", "cat": CAT, "ll": 27, "mount": "floor", "tiers": [1, 2, 3], "refs": ["i07_edo_nagaya_room"],
     "notes": ["★ BUILD_LIST jp_f_enza; zabuton T3 only"], "models": [
        M("jp_f_enza", "enza", "intact", "Round straw cushion (enza)", lambda: enza("enza")),
        M("jp_f_enza_stack3", "enza", "intact", "Three straw cushions stacked", lambda: enza("enza_stack3")),
        M("jp_f_enza_zabuton", "zabuton", "intact", "Cotton cushion (zabuton), T3", lambda: enza("zabuton"),
          tiers=[3]),
        M("jp_f_enza_zabuton_stack3", "zabuton", "intact", "Three zabuton stacked, T3", lambda: enza("zabuton_stack3"),
          tiers=[3]),
        M("jp_f_enza_kicked", "enza", "kicked", "Straw cushion kicked against the wall", lambda: enza("enza_kicked"),
          mount="wall"),
        M("jp_f_enza_zabuton_folded", "zabuton", "folded", "Zabuton folded over, askew, T3",
          lambda: enza("zabuton_folded"), tiers=[3]),
    ]},
    {"id": "jp_f_byobu", "cat": CAT, "ll": 28, "mount": "floor", "tiers": [1, 2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_byobu"], "models": [
        M("jp_f_byobu_makura", "makura", "intact", "Low bedding screen, two leaves", lambda: byobu("makura")),
        M("jp_f_byobu_tsuitate", "tsuitate", "intact", "Entrance screen on two feet", lambda: byobu("tsuitate")),
        M("jp_f_byobu_makura_fallen", "makura", "fallen", "Bedding screen knocked flat, torn",
          lambda: byobu("makura_fallen")),
        M("jp_f_byobu_tsuitate_fallen", "tsuitate", "fallen", "Entrance screen fallen, torn",
          lambda: byobu("tsuitate_fallen")),
    ]},
    {"id": "jp_f_iko", "cat": CAT, "ll": 29, "mount": "floor", "tiers": [2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_iko"], "models": [
        M("jp_f_iko_robe", "robe", "intact", "Clothes rack, lacquered, a robe spread over it", lambda: iko("robe"),
          tiers=[3]),
        M("jp_f_iko_plain", "plain", "intact", "Clothes rack, plain, an under-robe hung", lambda: iko("plain")),
        M("jp_f_iko_empty", "plain", "intact", "Clothes rack, plain, a sash end over the rail", lambda: iko("empty")),
        M("jp_f_iko_fallen", "robe", "fallen", "Clothes rack fallen, the robe on the mat", lambda: iko("fallen")),
    ]},
    {"id": "jp_f_clothes", "cat": CAT, "ll": 30, "mount": "floor", "tiers": [2, 3], "refs": ["m03_kosode_stencil"],
     "notes": ["the abandoned layer"], "models": [
        M("jp_f_clothes_kimono", "kimono", "dropped", "A kimono dropped on the mat", lambda: clothes("kimono")),
        M("jp_f_clothes_kimono_obi", "kimono_obi", "dropped", "An under-kimono and a sash on the mat",
          lambda: clothes("kimono_obi")),
        M("jp_f_clothes_haori", "haori", "dropped", "A short jacket and a sash on the mat", lambda: clothes("haori")),
    ]},
    {"id": "jp_f_sewing", "cat": CAT, "ll": 31, "mount": "floor", "tiers": [1, 2, 3], "refs": [], "models": [
        M("jp_f_sewing_box", "box", "intact", "Sewing box (haribako) with a pincushion", lambda: sewing("box"),
          mount="surface"),
        M("jp_f_sewing_work", "work", "intact", "Sewing box and a half-sewn garment", lambda: sewing("work")),
        M("jp_f_sewing_spilled", "work", "spilled", "Sewing box, drawer out, spools rolled", lambda: sewing("spilled")),
    ]},
    {"id": "jp_f_mirror_stand", "cat": CAT, "ll": 32, "mount": "floor", "tiers": [2, 3], "refs": [], "models": [
        M("jp_f_mirror_stand", "covered", "intact", "Mirror stand, the mirror under its cloth",
          lambda: mirror_stand("covered")),
        M("jp_f_mirror_stand_open", "open", "intact", "Mirror stand, the bronze mirror uncovered",
          lambda: mirror_stand("open")),
        M("jp_f_mirror_stand_tipped", "open", "tipped", "Mirror stand knocked over, the mirror on the mat",
          lambda: mirror_stand("tipped")),
    ]},
    {"id": "jp_f_goban", "cat": CAT, "ll": 33, "mount": "floor", "tiers": [2, 3], "refs": [], "models": [
        M("jp_f_goban_go", "go", "intact", "Go board with stones and bowls", lambda: goban("go")),
        M("jp_f_goban_shogi", "shogi", "intact", "Shogi board with pieces", lambda: goban("shogi")),
        M("jp_f_goban_go_scattered", "go", "scattered", "Go board, a bowl tipped, stones strewn",
          lambda: goban("go_scattered")),
        M("jp_f_goban_shogi_scattered", "shogi", "scattered", "Shogi board, pieces strewn",
          lambda: goban("shogi_scattered")),
    ]},
    {"id": "jp_f_toys", "cat": CAT, "ll": 34, "mount": "floor", "tiers": [1, 2, 3], "refs": [],
     "notes": ["era check kept with swaps (LIFE_LAYER_ERA 34)"], "models": [
        M("jp_f_toys_koma", "koma", "left", "A spinning top and its string", lambda: toys("koma")),
        M("jp_f_toys_hagoita", "hagoita", "left", "A battledore and shuttlecock", lambda: toys("hagoita")),
        M("jp_f_toys_doll", "doll", "left", "A small cloth doll", lambda: toys("doll")),
        M("jp_f_toys_scattered", "set", "left", "Toys left on the floor together", lambda: toys("scattered")),
    ]},
    {"id": "jp_f_shokudai", "cat": CAT, "ll": 35, "mount": "floor", "tiers": [3], "refs": [],
     "notes": ["T3 and upper only; unlit"], "models": [
        M("jp_f_shokudai_tall", "tall", "intact", "Tall lacquered candle stand, unlit", lambda: shokudai("tall")),
        M("jp_f_shokudai_short", "short", "intact", "Short iron candle stand", lambda: shokudai("short"),
          mount="surface"),
        M("jp_f_shokudai_tipped", "tall", "tipped", "Candle stand knocked over, the candle broken",
          lambda: shokudai("tipped")),
    ]},
    {"id": "jp_f_straw_bed", "cat": CAT, "ll": 36, "mount": "floor", "tiers": [1], "refs": [], "models": [
        M("jp_f_straw_bed_pile", "pile", "intact", "Straw bedding under a straw mat", lambda: straw_bed("pile")),
        M("jp_f_straw_bed_quilt", "quilt", "intact", "Straw bedding, a paper quilt thrown back",
          lambda: straw_bed("quilt")),
        M("jp_f_straw_bed_scattered", "pile", "scattered", "Straw bedding scattered and flattened",
          lambda: straw_bed("scattered")),
    ]},
]
