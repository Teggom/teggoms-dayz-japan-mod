"""W3B specialty props for the wave-3b workshops + services (spikes/W3B/W3B_NOTES.md "Props"), built into
jp_furniture.pbo by spikes/W3B/build_w3b.py (after B3a + L1 + S1 + W2F). Frames as fkit / lkit: 'floor' base centre on
the floor, +z = front; 'wall' origin on the floor below, wall face z = 0, the prop at +z (heights built in).

Dead world, autumn: the boiler and the furnace are cold, the tub drained, the stalls empty, the work left where it lay.
Every model has its 'as left' state; the _ab / second states are the ransacked or fallen-apart ones.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "W2F"))
import props_w2f_sacred as SC  # noqa: E402,F401
from props_w2f_sacred import (core, box, prism, lathe, xf, xfs, W, col, cyl_col, LPart, pole, cord, lod_box,  # noqa
                              wear_all, peg, rng, M, WOOD, WEATH, IRON, DARK, PALE, BAMBOO, ASH, LITTER, ROPE, KINARI,
                              INDIGO, LACQ, PAPER, BRONZE, KURO, NEW, CUTSTONE, SHU, PAINT)
import fkit  # noqa: E402
from bits import stain, mound, disc  # noqa: E402

CAT = "tradefit"
SOOTW = "wood_sooted"
ENDG = "wood_endgrain"
CLAY = "wall_nakanuri_int"
SAND = "ground_earth_bare"
MUSHIRO = "straw_mushiro"
STRAW = "straw_stack"
WEAVE = "bamboo_weave"
SBAMB = "bamboo_sooted"
RIVER = "stone_river"
FIELD = "stone_field"
TATAMI = "floor_tatami"


def logp(p0, p1, r, n=8, vis=(1, 2), wear=None):
    """A log / round timber with end grain on its caps (visual)."""
    return pole(p0, p1, r, WEATH, n=n, vis=vis, caps=ENDG, wear=wear)


def logc(p0, p1, r, n=6):
    """A log's collision (Geometry + View + Fire), convex n-gon prism."""
    return pole(p0, p1, r, WEATH, n=n, vis=(), geo=True, view=True, fire=True)


def tub_shell(R, h, t, mat=WEATH, n=12, vis=(1,), y0=0.0):
    """An open wooden tub / bucket: closed annular wall + bottom (lathe, cup profile)."""
    return lathe([(0.0, y0), (R, y0), (R, y0 + h), (R - t, y0 + h), (R - t, y0 + t), (0.0, y0 + t)], n, mat, vis=vis)


def adds1(P, out):
    """Add the detailed visual solids as Resolution 1 only (every prop has its own Res 2 stand-in) and lift any piece
    a tilt pushed below the floor back onto it (C6a: base within 0-2 cm)."""
    for i, s in enumerate(out):
        lo = min(v[1] for v in s.verts)
        if lo < 0.0:
            out[i] = s = xf(s, t=(0.0, -lo, 0.0))
        s.vis = {1}
    P.adds(out)
    return out


def hoops(R, ys, n=12, mat=BAMBOO):
    return [lathe([(R - 0.002, y - 0.012), (R + 0.008, y - 0.012), (R + 0.008, y + 0.012), (R - 0.002, y + 0.012)], n,
                  mat, vis=(1,), closed_ends=False) for y in ys]


# ================================================================================================ sento
def yubune(staved=False):
    """The bath tub (yubune) of a zakuro-guchi bath: a big board box tub raised on sleepers, its rim at 0.75, a step
    board (fumidai) along the bather's side, drained: a dark sludge line and leaves at the bottom. +z = the bather's
    side (the step), -z = the end wall (the boiler's flue box at the back)."""
    P = LPart("yubune", budget="furniture", mass=300.0, anchor="floor")
    w, d, h, t = 1.25, 2.10, 0.78, 0.05
    x0, x1, z0, z1 = -w / 2, w / 2, -d / 2, d / 2
    out = [W(x0, x1, 0.0, 0.10, z0 + 0.10, z0 + 0.22, SOOTW, vis=(1,)), W(x0, x1, 0.0, 0.10, z1 - 0.22, z1 - 0.10,
                                                                         SOOTW, vis=(1,)),
           W(x0, x1, 0.10, 0.14, z0, z1, WEATH, vis=(1,))]                                        # sleepers + bottom
    walls_ = [(x0, x0 + t, z0, z1), (x1 - t, x1, z0, z1), (x0 + t, x1 - t, z0, z0 + t), (x0 + t, x1 - t, z1 - t, z1)]
    for k, (a, b, c, e) in enumerate(walls_):
        if staved and k == 3:
            # a split board: the front wall's left half broken down to 0.40, the board lying in the tub
            out.append(W(a, (a + b) / 2 - 0.10, 0.14, h, c, e, WEATH, vis=(1,)))
            out.append(W((a + b) / 2 - 0.10, b, 0.14, 0.40, c, e, WEATH, vis=(1,)))
            out.append(xf(W(-0.30, 0.30, 0.0, 0.03, -0.12, 0.12, WEATH, vis=(1,)), rz=18.0, ry=20.0,
                          t=(0.15, 0.20, z1 - 0.30)))
        else:
            out.append(W(a, b, 0.14, h, c, e, WEATH, vis=(1,)))
    for (zz) in (z0 + 0.04, z1 - 0.04):                                                           # iron corner straps
        for xx in (x0 + 0.01, x1 - 0.01):
            out.append(W(xx - 0.012, xx + 0.012, 0.20, h - 0.06, zz - 0.012, zz + 0.012, IRON, vis=(1,)))
    out.append(W(x0 - 0.02, x1 + 0.02, h, h + 0.04, z0 - 0.02, z0 + 0.06, SOOTW, vis=(1,)))       # rim caps
    out.append(W(x0 - 0.02, x1 + 0.02, h, h + 0.04, z1 - 0.06, z1 + 0.02, WEATH, vis=(1,)))
    # the boiler flue box at the back (the iron pot under the tub is fired from the wall behind)
    out.append(W(-0.28, 0.28, 0.14, 0.60, z0 + t, z0 + 0.45, IRON, vis=(1,)))
    out.append(W(x0 + t, x1 - t, 0.14, 0.16, z0 + t, z1 - t, "ground_ash", vis=(1,)))             # sludge
    out.append(stain("yub", 0.10, 0.30, 0.45, y=0.163))
    # the step board on the bather's side
    out.append(W(x0 + 0.05, x1 - 0.05, 0.0, 0.32, z1 + 0.02, z1 + 0.34, WEATH, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(x0, x1, 0.0, h + 0.04, z0, z1 + 0.34, WEATH, vis=(2,)))
    cols = [col(x0, x0 + t, 0.0, h, z0, z1, WEATH), col(x1 - t, x1, 0.0, h, z0, z1, WEATH),
            col(x0 + t, x1 - t, 0.0, h, z0, z0 + t, WEATH), col(x0 + t, x1 - t, 0.0, 0.40 if staved else h, z1 - t, z1,
                                                                 WEATH),
            col(x0 + t, x1 - t, 0.0, 0.16, z0 + t, z1 - t, WEATH), col(x0 + 0.05, x1 - 0.05, 0.0, 0.32, z1 + 0.02,
                                                                       z1 + 0.34, WEATH)]
    P.adds(cols)
    P.loot_rect("step", 0.32, x0 + 0.20, x1 - 0.20, z1 + 0.10, z1 + 0.26, rng=0.12)
    P.loot_rect("tub", 0.16, x0 + 0.25, x1 - 0.25, z0 + 0.60, z1 - 0.25, rng=0.2, kind="floor", per=1.2)
    P.dim("w", w, w, tol=0.005)
    P.dim("h", h + 0.04, h + 0.04, tol=0.005)
    P.notes.append("the bath tub (yubune), drained (sludge, leaves); flue box at -z (the end wall), step board at +z%s"
                   % ("; a front board split" if staved else ""))
    return P


def bath_boiler(ab=False):
    """The boiler's fire mouth on the bath house end wall, outside in the kama-ba lean-to (mount wall: wall face z 0):
    a clay-and-stone firebox against the wall, an iron mouth frame, the iron door (hung / fallen), ash raked out,
    a poker."""
    P = LPart("bath_boiler", budget="furniture", mass=500.0, anchor="wall")
    w, d, h = 0.90, 0.55, 0.70
    out = [W(-w / 2, w / 2, 0.0, h, 0.0, d, CLAY, vis=(1,))]
    r = rng("boiler")
    for k in range(9):                                                                   # facing stones
        x = -w / 2 + 0.05 + (w - 0.10) * (k % 3) / 2.0
        y = 0.05 + (h - 0.20) * (k // 3) / 2.0
        if abs(x) < 0.20 and y < 0.45:
            continue
        out.append(W(x - 0.09, x + 0.09, y, y + r.uniform(0.12, 0.16), d, d + 0.02, FIELD, vis=(1,)))
    out.append(W(-0.20, 0.20, 0.10, 0.46, d, d + 0.03, IRON, vis=(1,)))                    # mouth frame
    out.append(W(-0.15, 0.15, 0.14, 0.42, d + 0.03, d + 0.031, "ground_ash", vis=(1,)))      # the dark mouth
    if ab:
        out.append(xf(W(-0.16, 0.16, 0.0, 0.02, -0.15, 0.15, IRON, vis=(1,)), ry=25.0, t=(0.30, 0.0, d + 0.45)))
        out.append(mound("bbash", -0.05, d + 0.40, 0.35, 0.06, "ground_ash"))
    else:
        out.append(W(-0.16, 0.10, 0.12, 0.44, d + 0.032, d + 0.045, IRON, vis=(1,)))           # the door, ajar
        out.append(mound("bbash", 0.0, d + 0.18, 0.20, 0.03, "ground_ash"))
    out.append(pole((0.38, 0.02, d + 0.10), (0.20, 0.95, d + 0.05), 0.012, IRON, n=4, vis=(1,)))   # poker
    out.append(W(-w / 2 - 0.02, w / 2 + 0.02, h, h + 0.05, 0.0, d + 0.03, CUTSTONE, vis=(1,)))      # top slab
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.05, 0.0, d + 0.03, CLAY, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h + 0.05, 0.0, d + 0.03, CLAY))
    P.loot_rect("top", h + 0.05, -w / 2 + 0.10, w / 2 - 0.10, 0.10, d - 0.05, rng=0.15)
    P.dim("w", w, w, tol=0.005)
    P.notes.append("the bath boiler's fire mouth on the end wall outside (mount wall), cold%s"
                   % ("; the door torn off, ash raked out" if ab else ""))
    return P


def bath_stools(tipped=False):
    """Two low bath stools (koshikake) and two small wooden buckets (oke) on the washing floor."""
    P = LPart("bath_stools", budget="small", mass=6.0, anchor="floor")
    out = []
    seats = [(-0.30, 0.0, 0.0), (0.25, 0.15, 25.0)]
    for i, (cx, cz, a) in enumerate(seats):
        st = [W(-0.17, 0.17, 0.17, 0.21, -0.11, 0.11, WEATH), W(-0.15, -0.12, 0.0, 0.17, -0.10, 0.10, WEATH),
              W(0.12, 0.15, 0.0, 0.17, -0.10, 0.10, WEATH)]
        if tipped and i == 1:
            st = [xf(s, rz=90.0, t=(0.0, 0.17, 0.0)) for s in st]
        out += [xf(s, ry=a, t=(cx, 0.0, cz)) for s in st]
    for (cx, cz) in ((0.05, -0.32), (-0.15, 0.35)):
        b = [tub_shell(0.13, 0.15, 0.012, WEATH, n=10)] + hoops(0.13, (0.04, 0.11), n=10)
        if tipped and cx > 0:
            b = [xf(s, rx=90.0, t=(0.0, 0.13, 0.0)) for s in b]
        out += [xf(s, t=(cx, 0.0, cz)) for s in b]
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.50, 0.50, 0.0, 0.21, -0.45, 0.48, WEATH, vis=(2,)))
    P.add(col(-0.47, -0.13, 0.0, 0.21, -0.11, 0.11, WEATH))
    P.dim("h", 0.21, 0.21, tol=0.01)
    P.notes.append("two bath stools and two wooden buckets on the washing floor%s" % ("; knocked over" if tipped else ""))
    return P


def bandai(ab=False):
    """The bandai: the attendant's raised pay counter at the step-up (a board box 0.80 high with a low front rail),
    the cashbox (zeni-bako) and a tobacco tray on it. +z faces the entrance doma."""
    P = LPart("bandai", budget="furniture", mass=40.0, anchor="floor")
    w, d, h = 0.70, 0.90, 0.80
    out = [W(-w / 2, w / 2, 0.0, h - 0.03, -d / 2, d / 2, WEATH), W(-w / 2 - 0.02, w / 2 + 0.02, h - 0.03, h, -d / 2 - 0.02,
                                                                     d / 2 + 0.02, WOOD)]
    for sx in (-1, 1):                                                              # the low front rail posts
        out.append(W(sx * (w / 2 - 0.02) - 0.02, sx * (w / 2 - 0.02) + 0.02, h, h + 0.22, d / 2 - 0.04, d / 2, WOOD))
    out.append(W(-w / 2, w / 2, h + 0.18, h + 0.22, d / 2 - 0.04, d / 2, WOOD))
    # the cashbox: a slotted box (forced: lid off, coins spilled)
    cb = [W(-0.16, 0.16, h, h + 0.16, -0.30, -0.08, KURO)]
    if ab:
        cb.append(xf(W(-0.17, 0.17, 0.0, 0.02, -0.12, 0.12, KURO), rz=-30.0, t=(0.30, h + 0.09, -0.05)))
        for k in range(7):
            a = 2.4 * k
            cb.append(disc(0.012, h, h + 0.003, BRONZE, n=6, vis=(1,), cx=0.05 + 0.03 * math.cos(a) * k / 2,
                           cz=0.10 + 0.03 * math.sin(a) * k / 2))
    else:
        cb.append(W(-0.17, 0.17, h + 0.16, h + 0.18, -0.31, -0.07, KURO))
        cb.append(W(-0.10, 0.10, h + 0.18, h + 0.185, -0.20, -0.18, IRON, vis=(1,)))
    out += cb
    out.append(W(0.10, 0.30, h, h + 0.08, 0.10, 0.28, WOOD))                         # tobacco tray
    out.append(W(0.14, 0.20, h + 0.08, h + 0.12, 0.14, 0.20, DARK, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.22, -d / 2, d / 2, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.loot_rect("counter", h, -0.25, 0.25, 0.30, 0.40, rng=0.1, points=[(-0.15, h, 0.32)])
    P.dim("h", h, h, tol=0.005)
    P.notes.append("the bandai (pay counter) with the cashbox%s and a tobacco tray" % (" forced open, coins spilled"
                                                                                       if ab else ""))
    return P


def nagashi(warped=False):
    """The nagashi: the slatted washing floor over its drain (a board frame, slats across, a gutter along the -x
    edge); walk-on (Roadway on the slats, top 0.06)."""
    P = LPart("nagashi", budget="furniture", mass=50.0, anchor="floor")
    w, d, hh = 1.30, 2.40, 0.06
    out = [W(-w / 2, -w / 2 + 0.06, 0.0, hh - 0.02, -d / 2, d / 2, SOOTW, vis=(1,)),
           W(w / 2 - 0.06, w / 2, 0.0, hh - 0.02, -d / 2, d / 2, SOOTW, vis=(1,))]
    n = 18
    r = rng("nagashi")
    for k in range(n):
        z = -d / 2 + 0.02 + (d - 0.04) * k / n
        if warped and k in (4, 5, 11):
            continue
        tilt = r.uniform(-2.0, 2.0) if warped else 0.0
        out.append(xf(W(-w / 2 + 0.03, w / 2 - 0.03, hh - 0.025, hh, -0.045, 0.045, WEATH, vis=(1,)), rx=tilt,
                      t=(0.0, 0.0, z + 0.06)))
    out.append(W(-w / 2 - 0.16, -w / 2, 0.0, 0.03, -d / 2, d / 2, SOOTW, vis=(1,)))                  # gutter floor
    out.append(W(-w / 2 - 0.18, -w / 2 - 0.16, 0.0, 0.07, -d / 2, d / 2, SOOTW, vis=(1,)))
    out.append(stain("nag", -w / 2 - 0.08, 0.0, 0.10, y=0.031, sz=6.0))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2 - 0.18, w / 2, 0.0, hh, -d / 2, d / 2, WEATH, vis=(2,)))
    cols = [col(-w / 2, w / 2, 0.0, hh, -d / 2, d / 2, WEATH)]
    P.adds(cols)
    fkit.road_tops(P, cols, surf="boards")
    zk = [-d / 2 + 0.02 + (d - 0.04) * k / n + 0.06 for k in (7, 13)]
    P.loot_rect("slats", hh, -w / 2 + 0.15, w / 2 - 0.15, -d / 2 + 0.20, d / 2 - 0.20, rng=0.2, kind="floor",
                points=[(0.0, hh, z) for z in zk])
    P.dim("w", w + 0.18, w + 0.18, tol=0.005)
    P.notes.append("the slatted washing floor (nagashi) over its drain gutter; walk-on%s"
                   % ("; slats warped, three missing" if warped else ""))
    return P


def datsui_dana(ransacked=False):
    """The changing room's clothes cubbies (mount wall): an open board case 1.80 x 1.40, 4 x 3 cubbies, wicker
    baskets in some (ransacked: baskets thrown down, a robe on the floor)."""
    P = LPart("datsui_dana", budget="furniture", mass=40.0, anchor="wall")
    w, h, d, y0 = 1.80, 1.40, 0.38, 0.0
    t = 0.022
    out = [W(-w / 2, w / 2, y0, y0 + t, 0.0, d, WOOD), W(-w / 2, w / 2, y0 + h - t, y0 + h, 0.0, d, WOOD),
           W(-w / 2, w / 2, y0, y0 + h, 0.0, 0.012, WOOD)]
    for i in range(5):
        x = -w / 2 + w * i / 4
        out.append(W(x - t / 2 if 0 < i < 4 else (x if i == 0 else x - t), x + t / 2 if 0 < i < 4 else (x + t if i == 0 else x),
                     y0, y0 + h, 0.012, d, WOOD))
    for j in (1, 2):
        y = y0 + h * j / 3
        out.append(W(-w / 2 + t, w / 2 - t, y - t / 2, y + t / 2, 0.012, d, WOOD))
    r = rng("datsui")
    baskets = []
    for i in range(4):
        for j in range(3):
            if r.random() < 0.45:
                cx = -w / 2 + w * (i + 0.5) / 4
                cy = y0 + h * j / 3 + t / 2
                baskets.append((cx, cy))
    for k, (cx, cy) in enumerate(baskets):
        if ransacked and k % 2 == 0:
            b = W(-0.17, 0.17, 0.0, 0.16, -0.13, 0.13, "wicker_aged", vis=(1,))
            out.append(xf(b, rz=90.0 * (k % 3 == 0), ry=30.0 * k, t=(cx * 0.8, 0.0 if k % 3 else 0.17, d + 0.35 + 0.1 * k)))
            continue
        out.append(W(cx - 0.17, cx + 0.17, cy, cy + 0.16, 0.06, 0.32, "wicker_aged", vis=(1,)))
    if ransacked:
        out.append(xf(W(-0.40, 0.40, 0.0, 0.03, -0.25, 0.25, INDIGO, vis=(1,)), ry=20.0, t=(0.30, 0.0, d + 0.65)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, y0, y0 + h, 0.0, d, WOOD, vis=(2,)))
    P.add(col(-w / 2, w / 2, y0, y0 + h, 0.0, d, WOOD))
    P.loot_rect("cubby_low", y0 + t, -w / 2 + 0.12, w / 2 - 0.12, 0.10, d - 0.06, rng=0.08,
                points=[(-w / 2 + w * (i + 0.5) / 4, y0 + t, 0.20) for i in (0, 3)])
    P.dim("w", w, w, tol=0.005)
    P.notes.append("clothes cubbies with wicker baskets (mount wall)%s" % ("; ransacked" if ransacked else ""))
    return P


# ================================================================================================ stable
def tack_wall(taken=False):
    """Tack on pegs (mount wall): straw horseshoes (uma-waraji) strung in bundles (Japanese horses went unshod), a
    rope halter + bridle, a girth band, a pack-saddle pad (straw)."""
    P = LPart("tack_wall", budget="furniture", mass=8.0, anchor="wall", flat=True)
    y = 1.45
    out = [W(-0.70, 0.70, y, y + 0.10, 0.0, 0.022, WEATH)]
    items = ["shoes", "shoes", "halter", "girth", "pad", "shoes"]
    if taken:
        items = ["shoes", None, "halter", None, "pad", None]
    for k, it in enumerate(items):
        x = -0.58 + k * 0.232
        out.append(peg(x, y + 0.05, L=0.08, z0=0.0))
        if it is None:
            continue
        z = 0.06
        if it == "shoes":
            out.append(cord((x, y + 0.04, z), (x, y - 0.40, z), 0.004))
            for j in range(4):
                yy = y - 0.08 - j * 0.09
                out.append(xf(W(-0.05, 0.05, -0.012, 0.012, -0.035, 0.035, STRAW, vis=(1,)), rx=60.0, rz=15.0 * (j % 2),
                              t=(x + 0.01 * (j % 2), yy, z + 0.01)))
        elif it == "halter":
            for j in range(6):
                a0, a1 = 2 * math.pi * j / 6, 2 * math.pi * (j + 1) / 6
                out.append(cord((x + 0.10 * math.sin(a0), y - 0.20 - 0.18 * math.cos(a0), z),
                                (x + 0.10 * math.sin(a1), y - 0.20 - 0.18 * math.cos(a1), z), 0.007))
            out.append(cord((x, y + 0.04, z), (x, y - 0.02, z), 0.007))
        elif it == "girth":
            out.append(W(x - 0.04, x + 0.04, y - 0.70, y + 0.03, z - 0.004, z + 0.004, KINARI, vis=(1,)))
        else:
            out.append(W(x - 0.20, x + 0.20, y - 0.50, y, z - 0.03, z + 0.03, MUSHIRO, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.70, 0.70, y - 0.70, y + 0.10, 0.0, 0.08, WEATH, vis=(2,)))
    P.dim("w", 1.40, 1.40, tol=0.005)
    P.notes.append("tack on pegs: straw horseshoes, rope halter, girth, a straw saddle pad (mount wall)%s"
                   % ("; half taken" if taken else ""))
    return P


# ================================================================================================ stalls
def ekisha_table(upset=False):
    """The street fortune-teller's table (eki-sha): a small low table with a cloth hung on its front, a paper lantern
    on a stand, the divination sticks (zeichiku) in their cylinder, counting rods (sangi), a book; his stool."""
    P = LPart("ekisha_table", budget="furniture", mass=10.0, anchor="floor")
    w, d, h = 0.75, 0.45, 0.60
    tb = [W(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, WOOD)]
    for sx in (-1, 1):
        for sz in (-1, 1):
            tb.append(W(sx * (w / 2 - 0.04) - 0.02, sx * (w / 2 - 0.04) + 0.02, 0.0, h - 0.03, sz * (d / 2 - 0.04) - 0.02,
                        sz * (d / 2 - 0.04) + 0.02, WOOD))
    tb.append(W(-w / 2, w / 2, 0.18, h - 0.03, d / 2, d / 2 + 0.005, KINARI, vis=(1,)))      # the front cloth
    goods = [lathe([(0.0, h), (0.035, h), (0.035, h + 0.22), (0.0, h + 0.22)], 8, BAMBOO, vis=(1,))]   # stick cylinder
    for k in range(9):
        a = 2 * math.pi * k / 9
        goods.append(pole((0.012 * math.cos(a), h + 0.15, 0.012 * math.sin(a)),
                          (0.025 * math.cos(a), h + 0.36, 0.025 * math.sin(a)), 0.003, NEW, n=3, vis=(1,)))
    goods = [xf(s, t=(-0.22, 0.0, -0.08)) for s in goods]
    for k in range(6):
        goods.append(W(0.02 + 0.03 * k, 0.04 + 0.03 * k, h, h + 0.015, 0.02, 0.14, NEW, vis=(1,)))   # sangi
    goods.append(W(0.05, 0.27, h, h + 0.03, -0.18, 0.0, PAPER, vis=(1,)))                     # the book
    lamp = [pole((0.0, 0.0, 0.0), (0.0, 1.05, 0.0), 0.012, WOOD, n=5, vis=(1,)),
            lathe([(0.0, 1.05), (0.10, 1.05), (0.12, 1.20), (0.10, 1.35), (0.0, 1.35)], 8, PAPER, vis=(1,)),
            W(-0.08, 0.08, 0.0, 0.03, -0.08, 0.08, WOOD)]
    lamp = [xf(s, t=(w / 2 + 0.22, 0.0, -0.05)) for s in lamp]
    stool = [W(-0.15, 0.15, 0.36, 0.40, -0.12, 0.12, WOOD), W(-0.13, -0.10, 0.0, 0.36, -0.10, 0.10, WOOD),
             W(0.10, 0.13, 0.0, 0.36, -0.10, 0.10, WOOD)]
    stool = [xf(s, t=(0.0, 0.0, -d / 2 - 0.35)) for s in stool]
    if upset:
        goods = [xf(s, rz=90.0, t=(0.0, -h + 0.04, 0.45)) if i < 10 else xf(s, ry=40.0, t=(0.25, -h + 0.0, 0.60))
                 for i, s in enumerate(goods)]
        lamp = [xf(s, rz=85.0, t=(0.0, 0.10, 0.0), pivot=(w / 2 + 0.22, 0.0, -0.05)) for s in lamp]
    out = tb + goods + lamp + stool
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2 + 0.35, 0.0, h, -d / 2 - 0.50, d / 2, WOOD, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD))
    P.loot_rect("table", h, 0.10, w / 2 - 0.08, 0.05, d / 2 - 0.08, rng=0.1, points=[(0.22, h, 0.12)])
    P.dim("h", h, h, tol=0.005)
    P.notes.append("the fortune-teller's table: sticks in their cylinder, counting rods, a book, the lantern%s"
                   % ("; knocked over" if upset else ""))
    return P


def barber_kit(spilled=False):
    """The barber's kit box (bin-darai): a wooden box with drawers, a copper basin set in its top, a razor, combs,
    a small mirror on a stand."""
    P = LPart("barber_kit", budget="furniture", mass=12.0, anchor="floor")
    w, d, h = 0.45, 0.32, 0.52
    out = [W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD)]
    for j in range(3):
        y = 0.06 + j * 0.13
        out.append(W(-w / 2 + 0.03, w / 2 - 0.03, y, y + 0.11, d / 2, d / 2 + 0.01, WOOD, vis=(1,)))
        out.append(W(-0.03, 0.03, y + 0.05, y + 0.06, d / 2 + 0.01, d / 2 + 0.02, IRON, vis=(1,)))
    out.append(lathe([(0.0, h), (0.16, h), (0.18, h + 0.08), (0.165, h + 0.08), (0.145, h + 0.015), (0.0, h + 0.015)],
                     12, BRONZE, vis=(1,)))
    out.append(W(-w / 2 + 0.02, -w / 2 + 0.12, h, h + 0.006, d / 2 - 0.08, d / 2 - 0.05, IRON, vis=(1,)))   # razor
    out.append(W(0.05, 0.13, h, h + 0.01, -d / 2 + 0.01, -d / 2 + 0.04, WOOD, vis=(1,)))                  # comb
    mir = [W(-0.04, 0.04, 0.0, 0.02, -0.04, 0.04, KURO), pole((0.0, 0.02, 0.0), (0.0, 0.22, 0.0), 0.006, KURO, n=4, vis=(1,)),
           lathe([(0.0, 0.0), (0.06, 0.0), (0.06, 0.008), (0.0, 0.008)], 10, BRONZE, vis=(1,))]
    mir[2] = xf(mir[2], rx=80.0, t=(0.0, 0.26, 0.0))
    if spilled:
        out[-1] = xf(out[-1], t=(0.15, -h, 0.35))
        out.append(xf(W(-w / 2 + 0.03, w / 2 - 0.03, 0.0, 0.11, -0.12, 0.12, WOOD, vis=(1,)), ry=25.0,
                      t=(0.10, 0.0, d / 2 + 0.30)))                                     # a drawer pulled out
        mir = [xf(s, rz=90.0, t=(0.25, 0.0, 0.45)) for s in mir]
    else:
        mir = [xf(s, t=(0.30, 0.0, 0.0)) for s in mir]
    out += mir
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.08, -d / 2, d / 2, WOOD, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD))
    P.loot_rect("top", h + 0.015, -0.10, 0.10, -0.08, 0.08, rng=0.08, points=[(0.0, h + 0.015, 0.0)])
    P.dim("h", h, h, tol=0.005)
    P.notes.append("the barber's kit box with its copper basin, razor, comb, mirror%s" % ("; spilled" if spilled else ""))
    return P


def misemono_sign(torn=False):
    """The show booth's signboard over its entrance (mount wall: the facade face z 0; heights built in): a board
    frame 2.40 x 0.85 at 2.15, the painted cloth panel (indigo ground, red and white figures as plain panels: no
    picture atlas), two side streamers."""
    P = LPart("misemono_sign", budget="furniture", mass=15.0, anchor="wall", flat=True)
    w, y0, y1 = 2.40, 2.15, 3.00
    out = [W(-w / 2 - 0.05, w / 2 + 0.05, y1, y1 + 0.06, 0.0, 0.06, KURO), W(-w / 2 - 0.05, w / 2 + 0.05, y0 - 0.06, y0,
                                                                            0.0, 0.06, KURO)]
    for sx in (-1, 1):
        out.append(W(sx * w / 2 - 0.05, sx * w / 2 + 0.05, y0 - 0.06, y1 + 0.06, 0.0, 0.06, KURO))
    out.append(W(-w / 2, w / 2, y0, y1, 0.02, 0.03, INDIGO, vis=(1,)))
    figs = [(-0.85, 0.35, 2.30, 2.85, PAINT), (-0.35, 0.55, 2.25, 2.75, KINARI), (0.35, 0.25, 2.40, 2.90, PAINT),
            (0.80, 0.30, 2.28, 2.70, KINARI)]
    for (cx, ww, a, b, m) in figs:
        if torn and cx > 0.3:
            continue
        out.append(W(cx - ww / 2, cx + ww / 2, a, b, 0.03, 0.034, m, vis=(1,)))
    if torn:
        out.append(xf(W(0.0, 0.90, -0.004, 0.004, 0.0, 0.55, INDIGO, vis=(1,)), rx=-80.0, t=(0.25, y0 + 0.05, 0.05)))
    for sx in (-1, 1):
        L = 1.4 if not (torn and sx > 0) else 0.6
        out.append(W(sx * (w / 2 + 0.12) - 0.10, sx * (w / 2 + 0.12) + 0.10, y1 - L, y1, 0.04, 0.045, SHU, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2 - 0.25, w / 2 + 0.25, y0 - 0.06, y1 + 0.06, 0.0, 0.06, KURO, vis=(2,)))
    P.dim("w", w + 0.10, w + 0.10, tol=0.005)
    P.notes.append("the show booth's painted-cloth signboard + streamers over the entrance (mount wall)%s"
                   % ("; torn" if torn else ""))
    return P


def show_cage(open_=False):
    """A bamboo animal cage on the show stage (an empty cage: the animal is gone)."""
    P = LPart("show_cage", budget="furniture", mass=20.0, anchor="floor")
    w, d, h = 1.10, 0.75, 0.95
    out = [W(-w / 2, w / 2, 0.0, 0.06, -d / 2, d / 2, WEATH), W(-w / 2, w / 2, h - 0.05, h, -d / 2, d / 2, WEATH)]
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * w / 2 - 0.04 * (sx > 0), sx * w / 2 + 0.04 * (sx < 0), 0.06, h - 0.05,
                         sz * d / 2 - 0.04 * (sz > 0), sz * d / 2 + 0.04 * (sz < 0), WEATH))
    n = 9
    for k in range(1, n):
        x = -w / 2 + w * k / n
        if open_ and 3 <= k <= 5:
            continue
        out.append(pole((x, 0.06, d / 2 - 0.02), (x, h - 0.05, d / 2 - 0.02), 0.012, BAMBOO, n=5, vis=(1,)))
        out.append(pole((x, 0.06, -d / 2 + 0.02), (x, h - 0.05, -d / 2 + 0.02), 0.012, BAMBOO, n=5, vis=(1,)))
    for k in range(1, 5):
        z = -d / 2 + d * k / 5
        for sx in (-1, 1):
            out.append(pole((sx * (w / 2 - 0.02), 0.06, z), (sx * (w / 2 - 0.02), h - 0.05, z), 0.012, BAMBOO, n=5,
                            vis=(1,)))
    out.append(W(-w / 2 + 0.05, w / 2 - 0.05, 0.06, 0.08, -d / 2 + 0.05, d / 2 - 0.05, STRAW, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, BAMBOO, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.loot_rect("top", h, -w / 2 + 0.12, w / 2 - 0.12, -d / 2 + 0.12, d / 2 - 0.12, rng=0.15)
    P.dim("h", h, h, tol=0.005)
    P.notes.append("an empty bamboo animal cage from the show%s" % ("; bars broken out" if open_ else ""))
    return P


# ================================================================================================ earth-floor workshop
def kezuridai(knocked=False):
    """The joiner's planing beam (kezuri-dai): a 2.6 m beam on a low trestle at one end, inclined; a pull plane on
    it, a board half planed, shavings on the floor."""
    P = LPart("kezuridai", budget="furniture", mass=60.0, anchor="floor")
    L = 2.60
    lo, hi = 0.25, 0.62
    ang = math.degrees(math.atan2(hi - lo, L))
    beam = [xf(W(-L / 2, L / 2, -0.06, 0.06, -0.12, 0.12, WEATH), rz=ang, t=(0.0, (lo + hi) / 2, 0.0))]
    tr = [W(L / 2 - 0.25, L / 2 - 0.20, 0.0, hi - 0.06, -0.20, 0.20, WEATH),
          W(L / 2 - 0.30, L / 2 - 0.15, 0.0, 0.05, -0.30, 0.30, WEATH),
          W(-L / 2 + 0.05, -L / 2 + 0.30, 0.0, lo - 0.06, -0.14, 0.14, WEATH)]
    plane = [W(-0.14, 0.14, 0.0, 0.05, -0.04, 0.04, WOOD), W(-0.01, 0.01, 0.04, 0.07, -0.03, 0.03, IRON, vis=(1,))]
    board = [W(-0.70, 0.70, 0.0, 0.02, -0.09, 0.09, NEW)]
    top = lambda x: (lo + hi) / 2 + 0.06 + (x) * math.tan(math.radians(ang))  # noqa: E731
    if knocked:
        plane = [xf(s, rz=90.0, t=(0.40, 0.0, 0.45)) for s in plane]
        board = [xf(s, ry=25.0, t=(-0.30, 0.0, 0.50)) for s in board]
    else:
        plane = [xf(s, rz=ang, t=(0.30, top(0.30), 0.0)) for s in plane]
        board = [xf(s, rz=ang, t=(-0.30, top(-0.30) + 0.0, 0.0)) for s in board]
    out = beam + tr + plane + board
    out.append(mound("shav", -0.60, 0.30, 0.40, 0.05, NEW, sx=1.4))
    out.append(mound("shav2", 0.70, -0.25, 0.25, 0.04, NEW))
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-L / 2, L / 2, 0.0, hi + 0.06, -0.30, 0.30, WEATH, vis=(2,)))
    P.add(xf(col(-L / 2, L / 2, -0.06, 0.06, -0.12, 0.12, WEATH), rz=ang, t=(0.0, (lo + hi) / 2, 0.0)))
    P.add(col(L / 2 - 0.30, L / 2 - 0.15, 0.0, hi - 0.10, -0.20, 0.20, WEATH))
    P.dim("L", L, L, tol=0.01)
    P.notes.append("the planing beam (kezuri-dai), a pull plane%s, shavings" % (" knocked off" if knocked else " on it"))
    return P


def sawhorses(knocked=False):
    """A pair of joiner's sawhorses (uma) with a board across them (the board's top a loot surface)."""
    P = LPart("sawhorses", budget="furniture", mass=25.0, anchor="floor")
    h = 0.55
    out = []
    horses = [(-0.65, 0.0), (0.65, 0.0)]
    for i, (cx, cz) in enumerate(horses):
        hs = [W(-0.05, 0.05, h - 0.08, h, -0.40, 0.40, WEATH)]
        for sz in (-1, 1):
            for sx in (-1, 1):
                hs.append(pole((sx * 0.02, h - 0.06, sz * 0.32), (sx * 0.22, 0.0, sz * 0.38), 0.025, WEATH, n=5))
        if knocked and i == 1:
            hs = [xf(s, rz=90.0, t=(0.0, 0.40, 0.0)) for s in hs]
        out += [xf(s, ry=90.0, t=(cx, 0.0, cz)) for s in hs]
    bd = W(-1.10, 1.10, h, h + 0.03, -0.15, 0.15, NEW)
    if knocked:
        bd = xf(bd, rz=-14.0, t=(0.0, -0.27, 0.10))
    out.append(bd)
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-1.10, 1.10, 0.0, h + 0.03, -0.40, 0.40, WEATH, vis=(2,)))
    P.add(col(-0.75, -0.55, 0.0, h, -0.40, 0.40, WEATH))
    if not knocked:
        P.add(col(-1.10, 1.10, h, h + 0.03, -0.15, 0.15, NEW))
        P.add(col(0.55, 0.75, 0.0, h, -0.40, 0.40, WEATH))
        P.loot_rect("board", h + 0.03, -0.95, 0.95, -0.08, 0.08, rng=0.12)

    P.dim("h", h + 0.03, h + 0.03, tol=0.01)
    P.notes.append("two sawhorses with a board%s" % (" (one knocked over, the board slid down)" if knocked else ""))
    return P


def dogubako(ransacked=False):
    """The joiner's tool chest (dogu-bako), lid open: saws, chisels and planes in it; ransacked = tools strewn."""
    P = LPart("dogubako", budget="furniture", mass=20.0, anchor="floor")
    w, d, h, t = 0.90, 0.38, 0.32, 0.02
    out = [W(-w / 2, w / 2, 0.0, t, -d / 2, d / 2, WEATH), W(-w / 2, w / 2, t, h, -d / 2, -d / 2 + t, WEATH),
           W(-w / 2, w / 2, t, h, d / 2 - t, d / 2, WEATH), W(-w / 2, -w / 2 + t, t, h, -d / 2 + t, d / 2 - t, WEATH),
           W(w / 2 - t, w / 2, t, h, -d / 2 + t, d / 2 - t, WEATH)]
    out.append(xf(W(-w / 2, w / 2, 0.0, t, 0.0, d, WEATH), rx=-100.0, t=(0.0, h, -d / 2)))      # the lid, open back
    tools = []
    for k in range(3):                                                                # saws (blade + handle)
        tools.append(W(-0.38 + 0.02 * k, 0.10, h - 0.10 + 0.02 * k, h - 0.098 + 0.02 * k, -0.12 + 0.08 * k,
                       -0.03 + 0.08 * k, IRON, vis=(1,)))
        tools.append(pole((0.10, h - 0.09 + 0.02 * k, -0.075 + 0.08 * k), (0.36, h - 0.09 + 0.02 * k, -0.075 + 0.08 * k),
                          0.012, BAMBOO, n=5, vis=(1,)))
    for k in range(4):                                                                # chisels
        tools.append(pole((-0.35 + 0.05 * k, h - 0.02, 0.12), (-0.35 + 0.05 * k, h + 0.10, 0.12), 0.01, WOOD, n=4,
                          vis=(1,)))
    if ransacked:
        tools = [xf(s, ry=40.0 * i, t=(0.2 * math.cos(i), -h + 0.02, 0.45 + 0.05 * i)) for i, s in enumerate(tools)]
    out += tools
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.12, -d / 2 - 0.05, d / 2, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.loot_rect("box", t, -w / 2 + 0.12, w / 2 - 0.12, -0.05, 0.05, rng=0.1, points=[(-0.20, t + 0.0, 0.0)])
    P.dim("w", w, w, tol=0.005)
    P.notes.append("the joiner's tool chest, open%s" % ("; tools strewn" if ransacked else ""))
    return P


def frames_lean():
    """Sliding-door and shoji frames (tategu) leaning against the wall (mount wall), a kumiko lattice half made."""
    P = LPart("frames_lean", budget="furniture", mass=15.0, anchor="wall", flat=True)
    out = []
    for k, (x, hh, ww) in enumerate(((-0.55, 1.75, 0.88), (-0.10, 1.75, 0.88), (0.45, 1.60, 0.80))):
        lean = 8.0 + 2 * k
        fr = [W(-ww / 2, -ww / 2 + 0.03, 0.0, hh, -0.015, 0.015, NEW), W(ww / 2 - 0.03, ww / 2, 0.0, hh, -0.015, 0.015, NEW),
              W(-ww / 2, ww / 2, 0.0, 0.05, -0.015, 0.015, NEW), W(-ww / 2, ww / 2, hh - 0.04, hh, -0.015, 0.015, NEW)]
        nb = 3 if k < 2 else 5
        for i in range(1, nb):
            xx = -ww / 2 + ww * i / nb
            fr.append(W(xx - 0.006, xx + 0.006, 0.05, hh - 0.04, -0.008, 0.008, NEW, vis=(1,)))
        for j in range(1, 6 if k < 2 else 3):
            yy = hh * j / 6
            fr.append(W(-ww / 2 + 0.03, ww / 2 - 0.03, yy - 0.006, yy + 0.006, -0.008, 0.008, NEW, vis=(1,)))
        a = math.radians(lean)
        out += [xf(s, rx=-lean, t=(x, 0.0, hh * math.sin(a) + 0.02 + 0.03 * k)) for s in fr]
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-1.00, 0.85, 0.0, 1.75, 0.0, 0.40, NEW, vis=(2,)))
    P.dim("h", 1.75, 1.75, tol=0.05)
    P.notes.append("shoji / door frames leaning on the wall (mount wall); visual only")
    return P


def rokuro(broken=False):
    """The woodturner's strap lathe (te-biki rokuro, GK): two posts on a base beam, a horizontal spindle with a
    bowl blank on its chuck, the pull strap wound on the spindle (a helper pulled it back and forth), the turner's
    tool rest and seat board; turned bowls in a basket."""
    P = LPart("rokuro", budget="furniture", mass=50.0, anchor="floor")
    L, yA = 1.10, 0.42
    out = [W(-L / 2, L / 2, 0.0, 0.10, -0.12, 0.12, WEATH)]
    for sx in (-1, 1):
        out.append(W(sx * 0.38 - 0.05, sx * 0.38 + 0.05, 0.10, yA + 0.12, -0.08, 0.08, WEATH))
    sp = pole((-0.45, yA, 0.0), (0.30, yA, 0.0), 0.025, WOOD, n=6)
    out.append(sp)
    out.append(xf(lathe([(0.0, 0.0), (0.09, 0.0), (0.09, 0.07), (0.0, 0.07)], 10, WOOD, vis=(1,)), rz=-90.0,
                  t=(0.30, yA, 0.0)))                                                            # chuck
    blank = xf(lathe([(0.0, 0.0), (0.06, 0.0), (0.13, 0.05), (0.14, 0.10), (0.0, 0.10)], 12, NEW, vis=(1,)), rz=-90.0,
               t=(0.37, yA, 0.0))
    for k in range(6):                                                                             # the strap turns
        x = -0.30 + 0.035 * k
        out.append(pole((x, yA - 0.031, -0.006), (x, yA - 0.031, 0.006), 0.031, "leather_tan", n=6, vis=(1,)))
    strap = [pole((-0.22, yA - 0.03, 0.0), (-0.22, 0.02, 0.45), 0.006, "leather_tan", n=3, vis=(1,)),
             pole((-0.27, yA - 0.03, 0.0), (-0.40, 0.02, 0.50), 0.006, "leather_tan", n=3, vis=(1,))]
    rest_ = [W(0.40, 0.48, 0.10, yA - 0.02, 0.10, 0.16, WEATH), W(0.30, 0.60, yA - 0.02, yA, 0.08, 0.18, WEATH)]
    seat = [W(0.55, 0.95, 0.0, 0.18, -0.25, 0.25, WEATH)]
    if broken:
        blank = xf(blank, rz=90.0, t=(0.25, -yA + 0.06, 0.45))
        strap = [pole((-0.25, 0.01, 0.10), (-0.10, 0.01, 0.80), 0.006, "leather_tan", n=3, vis=(1,))]
    out += [blank] + strap + rest_ + seat
    basket = [lathe([(0.0, 0.0), (0.20, 0.0), (0.22, 0.16), (0.20, 0.16), (0.18, 0.02), (0.0, 0.02)], 10, WEAVE, vis=(1,))]
    for k in range(4):
        basket.append(lathe([(0.0, 0.02), (0.06, 0.02), (0.08, 0.06), (0.0, 0.06)], 8, NEW, vis=(1,)))
        basket[-1] = xf(basket[-1], rz=20.0 * k, t=(0.05 * math.cos(k * 1.6), 0.03 * k, 0.05 * math.sin(k * 1.6)))
    out += [xf(s, t=(-0.30, 0.0, 0.45)) for s in basket]
    out.append(mound("turn", 0.40, 0.30, 0.30, 0.03, NEW))
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-L / 2, 0.95, 0.0, yA + 0.12, -0.25, 0.65, WEATH, vis=(2,)))
    P.add(col(-L / 2, L / 2, 0.0, yA + 0.12, -0.12, 0.12, WEATH))
    P.add(col(0.55, 0.95, 0.0, 0.18, -0.25, 0.25, WEATH))
    P.loot_rect("seat", 0.18, 0.62, 0.88, -0.15, 0.15, rng=0.1, points=[(0.75, 0.18, 0.0)])
    P.dim("L", L, L, tol=0.005)
    P.notes.append("the woodturner's strap lathe with a bowl blank, the turner's seat, turned bowls%s"
                   % ("; strap snapped, blank off the chuck" if broken else ""))
    return P


def soroban_tray():
    """The abacus maker's work: a low tray of bead blanks and finished beads, bamboo rods bundled, two unstrung frames,
    a finished abacus."""
    P = LPart("soroban_tray", budget="furniture", mass=6.0, anchor="floor")
    out = [W(-0.40, 0.40, 0.0, 0.04, -0.25, 0.25, WOOD), W(-0.40, 0.40, 0.04, 0.07, -0.25, -0.23, WOOD),
           W(-0.40, 0.40, 0.04, 0.07, 0.23, 0.25, WOOD)]
    r = rng("soroban")
    for k in range(26):
        x, z = r.uniform(-0.36, -0.02), r.uniform(-0.20, 0.20)
        out.append(W(x - 0.008, x + 0.008, 0.04, 0.054, z - 0.008, z + 0.008, KURO if k % 3 else WOOD, vis=(1,)))
    for k in range(7):
        out.append(pole((0.05, 0.05, -0.18 + 0.012 * k), (0.36, 0.05, -0.18 + 0.012 * k), 0.003, BAMBOO, n=3, vis=(1,)))
    # a finished abacus: frame + beam + bead rows
    ab = [W(-0.20, 0.20, 0.0, 0.02, -0.08, -0.06, KURO), W(-0.20, 0.20, 0.0, 0.02, 0.06, 0.08, KURO),
          W(-0.20, -0.18, 0.0, 0.02, -0.06, 0.06, KURO), W(0.18, 0.20, 0.0, 0.02, -0.06, 0.06, KURO),
          W(-0.18, 0.18, 0.0, 0.022, 0.025, 0.035, KURO)]
    for i in range(9):
        x = -0.16 + 0.04 * i
        for zz in (-0.045, -0.03, -0.015, 0.0, 0.05):
            ab.append(W(x - 0.009, x + 0.009, 0.004, 0.02, zz - 0.006, zz + 0.006, WOOD, vis=(1,)))
    out += [xf(s, t=(0.18, 0.04, 0.10)) for s in ab]
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-0.40, 0.40, 0.0, 0.07, -0.25, 0.25, WOOD, vis=(2,)))
    P.add(col(-0.40, 0.40, 0.0, 0.04, -0.25, 0.25, WOOD))
    P.dim("w", 0.80, 0.80, tol=0.005)
    P.notes.append("the abacus maker's tray: bead blanks, bamboo rods, a finished abacus (visual; loot beside it)")
    return P


def bamboo_stock(scattered=False):
    """Madake poles stood against the wall (mount wall), a bundle of split strips; scattered = poles fallen."""
    P = LPart("bamboo_stock", budget="furniture", mass=25.0, anchor="wall", flat=True)
    out = []
    r = rng("bamboo_stock")
    for k in range(9):
        x = -0.55 + 0.13 * k + r.uniform(-0.03, 0.03)
        Lh = r.uniform(2.6, 3.0)
        if scattered and k % 2 == 0:
            a = r.uniform(-25, 25)
            out.append(pole((x, 0.03, 0.10 + 0.07 * k), (x + 2.4 * math.sin(math.radians(a)), 0.03,
                                                       0.10 + 0.07 * k + 2.4 * math.cos(math.radians(a))), 0.03,
                            BAMBOO, n=6, vis=(1,)))
            continue
        out.append(pole((x, 0.0, 0.42), (x + r.uniform(-0.05, 0.05), Lh, 0.04), 0.03, BAMBOO, n=6, vis=(1,)))
    for k in range(14):
        out.append(W(0.70, 1.60, 0.02 + 0.006 * (k % 4), 0.025 + 0.006 * (k % 4), 0.20 + 0.025 * k, 0.215 + 0.025 * k,
                     BAMBOO, vis=(1,)))
    out.append(cord((0.95, 0.04, 0.18), (0.95, 0.04, 0.58), 0.006))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.65, 1.60, 0.0, 2.8, 0.0, 0.60, BAMBOO, vis=(2,)))
    P.dim("h", 2.8, 2.8, tol=0.3)
    P.notes.append("bamboo poles stood on the wall + split strips (mount wall; visual)%s"
                   % ("; poles fallen" if scattered else ""))
    return P


def basket_work(abandoned=False):
    """The basket maker's place: a straw mat, a half-woven basket with its strip ends standing up, the splitting
    knife (nata), a soaking tub, finished trays stacked."""
    P = LPart("basket_work", budget="furniture", mass=10.0, anchor="floor")
    out = [W(-0.55, 0.55, 0.0, 0.012, -0.45, 0.45, MUSHIRO, vis=(1,))]
    bk = [lathe([(0.0, 0.012), (0.20, 0.012), (0.22, 0.14), (0.20, 0.14), (0.18, 0.03), (0.0, 0.03)], 10, WEAVE, vis=(1,))]
    for k in range(12):
        a = 2 * math.pi * k / 12
        bk.append(pole((0.21 * math.cos(a), 0.14, 0.21 * math.sin(a)), (0.27 * math.cos(a), 0.36, 0.27 * math.sin(a)),
                       0.004, BAMBOO, n=3, vis=(1,)))
    if abandoned:
        bk = [xf(s, rx=80.0, t=(0.0, 0.20, 0.0)) for s in bk]
    out += [xf(s, t=(-0.15, 0.0, 0.05)) for s in bk]
    out.append(W(0.20, 0.42, 0.012, 0.022, 0.20, 0.24, IRON, vis=(1,)))                             # nata blade
    out.append(pole((0.42, 0.017, 0.22), (0.55, 0.017, 0.22), 0.014, WOOD, n=5, vis=(1,)))
    tub = [tub_shell(0.24, 0.26, 0.02, WEATH, n=12)] + hoops(0.24, (0.06, 0.20))
    out += [xf(s, t=(0.30, 0.0, -0.30)) for s in tub]
    for k in range(4):                                                                              # zaru stack
        out.append(lathe([(0.0, 0.012 + 0.03 * k), (0.17, 0.012 + 0.03 * k), (0.20, 0.04 + 0.03 * k),
                          (0.0, 0.04 + 0.03 * k)], 10, WEAVE, vis=(1,)))
        out[-1] = xf(out[-1], t=(-0.70, 0.0, -0.20))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.90, 0.60, 0.0, 0.26, -0.55, 0.45, WEAVE, vis=(2,)))
    P.add(cyl_col(0.24, 0.0, 0.26, n=8, cx=0.30, cz=-0.30, mat=WEATH))
    P.loot_rect("mat", 0.012, -0.45, 0.45, 0.30, 0.40, rng=0.12, kind="floor", points=[(0.25, 0.012, 0.35)])
    P.dim("w", 1.10, 1.10, tol=0.005)
    P.notes.append("the basket maker's place: half-woven basket, nata, soaking tub, trays%s"
                   % ("; the basket kicked over" if abandoned else ""))
    return P


# ================================================================================================ bench workshop
def togidai(upset=False):
    """The sword polisher's place: the sloping stone holder (togi-dai) with its foot board, a stone on it, the low
    stool, a water tub, a blade on a stand, a tray of finger stones."""
    P = LPart("togidai", budget="furniture", mass=20.0, anchor="floor")
    out = [W(-0.30, 0.30, 0.0, 0.03, -0.20, 0.20, WEATH)]                                          # foot board
    st = [xf(W(-0.06, 0.06, 0.0, 0.05, -0.16, 0.16, WEATH), rx=-15.0, t=(0.0, 0.12, 0.0)),
          W(-0.05, 0.05, 0.03, 0.12, -0.12, -0.05, WEATH)]
    stone = xf(W(-0.035, 0.035, 0.0, 0.025, -0.10, 0.10, CUTSTONE, vis=(1,)), rx=-15.0, t=(0.0, 0.17, 0.0))
    stool = [W(-0.16, 0.16, 0.24, 0.27, -0.12, 0.12, WEATH), W(-0.14, -0.11, 0.0, 0.24, -0.10, 0.10, WEATH),
             W(0.11, 0.14, 0.0, 0.24, -0.10, 0.10, WEATH)]
    stool = [xf(s, t=(0.0, 0.0, -0.45)) for s in stool]
    tub = [tub_shell(0.20, 0.20, 0.015, WEATH, n=12)] + hoops(0.20, (0.05, 0.15))
    tub = [xf(s, t=(0.48, 0.0, -0.05)) for s in tub]
    stand = [W(-0.30, 0.30, 0.0, 0.03, -0.06, 0.06, KURO), W(-0.25, -0.22, 0.03, 0.22, -0.02, 0.02, KURO),
             W(0.22, 0.25, 0.03, 0.22, -0.02, 0.02, KURO),
             W(-0.36, 0.36, 0.22, 0.226, -0.004, 0.024, IRON, vis=(1,))]
    stand = [xf(s, t=(-0.55, 0.0, 0.20)) for s in stand]
    tray = [W(-0.12, 0.12, 0.0, 0.03, -0.08, 0.08, WOOD)] + [W(-0.10 + 0.05 * k, -0.07 + 0.05 * k, 0.03, 0.04, -0.02, 0.02,
                                                              CUTSTONE, vis=(1,)) for k in range(4)]
    tray = [xf(s, t=(0.30, 0.0, 0.35)) for s in tray]
    if upset:
        tub = [xf(s, rx=85.0, t=(0.0, 0.20, 0.10)) for s in tub]
        stone = xf(stone, t=(0.25, -0.15, 0.30))
        stand = [xf(s, rz=90.0, t=(0.0, 0.0, 0.0), pivot=(-0.55, 0.0, 0.20)) for s in stand]
    out += st + [stone] + stool + tub + stand + tray
    if upset:
        out.append(stain("togi", 0.45, 0.30, 0.35, y=0.004, mat=LITTER))
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-0.85, 0.70, 0.0, 0.27, -0.60, 0.45, WEATH, vis=(2,)))
    P.add(col(-0.30, 0.30, 0.0, 0.20, -0.20, 0.20, WEATH))
    P.loot_rect("board", 0.03, -0.28, -0.12, -0.18, 0.18, rng=0.08, points=[(-0.20, 0.03, 0.10)])
    P.dim("w", 0.60, 0.60, tol=0.005)
    P.notes.append("the sword polisher's stone holder, stool, water tub, blade stand, finger stones%s"
                   % ("; upset" if upset else ""))
    return P


def urushi_tray(spilled=False):
    """The lacquerer's work board: a low board with lacquer pots (lidded), human-hair brushes on a rest, spatulas, a
    paper-covered pot, a bowl in progress on a turning stand; wares on a small drying shelf beside."""
    P = LPart("urushi_tray", budget="furniture", mass=15.0, anchor="floor")
    w, d, h = 0.80, 0.50, 0.25
    out = [W(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, WOOD)]
    for sx in (-1, 1):
        out.append(W(sx * (w / 2 - 0.05) - 0.025, sx * (w / 2 - 0.05) + 0.025, 0.0, h - 0.03, -d / 2 + 0.03, d / 2 - 0.03,
                     WOOD))
    pots = []
    for k, (x, z, m) in enumerate(((-0.25, -0.12, KURO), (-0.12, -0.14, SHU), (0.0, -0.13, KURO))):
        pots.append(lathe([(0.0, h), (0.045, h), (0.05, h + 0.06), (0.0, h + 0.06)], 8, m, vis=(1,)))
        pots[-1] = xf(pots[-1], t=(x, 0.0, z))
    for k in range(3):                                                                    # brushes on a rest
        pots.append(W(-0.10, 0.06, h + 0.02, h + 0.032, 0.05 + 0.03 * k, 0.062 + 0.03 * k, NEW, vis=(1,)))
        pots.append(W(-0.12, -0.10, h + 0.02, h + 0.032, 0.05 + 0.03 * k, 0.062 + 0.03 * k, KURO, vis=(1,)))
    pots.append(W(-0.14, 0.10, h, h + 0.02, 0.04, 0.05, WOOD, vis=(1,)))
    bowl = [xf(lathe([(0.0, 0.0), (0.04, 0.0), (0.10, 0.06), (0.09, 0.065), (0.035, 0.012), (0.0, 0.012)], 12, SHU,
                     vis=(1,)), t=(0.24, h + 0.06, 0.05)),
            lathe([(0.0, h), (0.05, h), (0.05, h + 0.06), (0.0, h + 0.06)], 8, WOOD, vis=(1,))]
    bowl[1] = xf(bowl[1], t=(0.24, 0.0, 0.05))
    if spilled:
        pots[1] = xf(pots[1], rz=90.0, t=(0.0, -0.18, 0.20))
        out.append(stain("urushi", -0.10, 0.30, 0.20, y=0.003, mat=KURO))
    out += pots + bowl
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.10, -d / 2, d / 2, WOOD, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD))
    P.loot_rect("board", h, 0.12, w / 2 - 0.06, -d / 2 + 0.06, -0.05, rng=0.08, points=[(0.25, h, -0.14)])
    P.dim("h", h, h, tol=0.005)
    P.notes.append("the lacquerer's work board: pots, hair brushes, a red bowl on its stand%s"
                   % ("; a pot knocked off, black lacquer spilt" if spilled else ""))
    return P


def kinko_bench(taken=False):
    """The sword-fittings maker's bench: a low desk with the pitch bowl (yani-dai) holding a guard (tsuba) blank,
    chasing punches (tagane) in a rack, files, a tray of finished guards; a small charcoal brazier with a hand
    bellows beside it (the little forge)."""
    P = LPart("kinko_bench", budget="furniture", mass=20.0, anchor="floor")
    w, d, h = 0.90, 0.45, 0.30
    out = [W(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, WOOD)]
    for sx in (-1, 1):
        out.append(W(sx * (w / 2 - 0.05) - 0.03, sx * (w / 2 - 0.05) + 0.03, 0.0, h - 0.03, -d / 2 + 0.03, d / 2 - 0.03, WOOD))
    pitch = [lathe([(0.0, h), (0.09, h), (0.09, h + 0.05), (0.0, h + 0.05)], 10, DARK, vis=(1,)),
             lathe([(0.0, h + 0.05), (0.04, h + 0.05), (0.04, h + 0.056), (0.0, h + 0.056)], 10, IRON, vis=(1,))]
    pitch = [xf(s, t=(-0.15, 0.0, 0.0)) for s in pitch]
    rack = [W(0.05, 0.35, h, h + 0.04, -0.17, -0.12, WOOD)]
    for k in range(7):
        rack.append(pole((0.08 + 0.04 * k, h + 0.02, -0.145), (0.08 + 0.04 * k, h + 0.12, -0.145), 0.004, IRON, n=4,
                         vis=(1,)))
    tray = [W(0.10, 0.36, h, h + 0.02, 0.02, 0.18, KURO)]
    if not taken:
        for k in range(3):
            tray.append(lathe([(0.0, h + 0.02), (0.035, h + 0.02), (0.035, h + 0.026), (0.0, h + 0.026)], 8, IRON,
                              vis=(1,)))
            tray[-1] = xf(tray[-1], t=(0.15 + 0.08 * k, 0.0, 0.10))
    files = [W(-0.40, -0.25, h, h + 0.006, 0.10, 0.11, IRON, vis=(1,)), W(-0.40, -0.25, h, h + 0.006, 0.13, 0.14, IRON,
                                                                          vis=(1,))]
    brazier = [lathe([(0.0, 0.0), (0.16, 0.0), (0.18, 0.22), (0.16, 0.22), (0.14, 0.05), (0.0, 0.05)], 10, DARK, vis=(1,)),
               lathe([(0.0, 0.05), (0.14, 0.05), (0.14, 0.15), (0.0, 0.15)], 10, "ground_ash", vis=(1,))]
    brazier = [xf(s, t=(w / 2 + 0.30, 0.0, -0.05)) for s in brazier]
    hb = [W(-0.06, 0.06, 0.0, 0.12, -0.18, 0.18, WOOD), pole((0.0, 0.08, 0.18), (0.0, 0.08, 0.30), 0.012, WOOD, n=4,
                                                            vis=(1,))]
    hb = [xf(s, ry=90.0, t=(w / 2 + 0.30, 0.0, 0.30)) for s in hb]
    out += pitch + rack + tray + files + brazier + hb
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-w / 2, w / 2 + 0.50, 0.0, h + 0.12, -d / 2, d / 2 + 0.20, WOOD, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD))
    P.add(cyl_col(0.18, 0.0, 0.22, n=8, cx=w / 2 + 0.30, cz=-0.05, mat=DARK))
    P.loot_rect("desk", h, -0.40, -0.25, -0.17, 0.0, rng=0.06, points=[(-0.33, h, -0.10)])
    P.dim("h", h, h, tol=0.005)
    P.notes.append("the sword-fittings maker's bench: pitch bowl, punches, files, guards, the little brazier forge%s"
                   % ("; the finished guards taken" if taken else ""))
    return P


# ================================================================================================ timber yard
def saw_trestle(fallen=False):
    """The sawyer's trestle (no pit: GK, the kobiki method): a tall A-frame trestle (2.0 m) with a log (d 0.44, 4.6 m)
    propped on it at ~25 deg, its foot on a block; the big one-man rip saw (maebiki-oga) in the kerf, wedges, the
    ink-line pot, sawdust. Fallen = the log rolled off, the saw on the ground."""
    P = LPart("saw_trestle", budget="furniture", mass=600.0, anchor="floor")
    P.over_budget_ok = "a 4.6 m log on a 2 m trestle with the big saw: the round log needs its segments"
    th = 2.00
    out = []
    for sz in (-1, 1):
        out.append(pole((-0.45, 0.05, sz * 0.55), (0.0, th, sz * 0.12), 0.06, WEATH, n=6))
        out.append(pole((0.45, 0.05, sz * 0.55), (0.0, th, sz * 0.12), 0.06, WEATH, n=6))
    out.append(pole((0.0, th - 0.02, -0.30), (0.0, th - 0.02, 0.30), 0.07, WEATH, n=6))                 # the cross bar
    out.append(pole((-0.30, 0.65, -0.45), (-0.30, 0.65, 0.45), 0.035, WEATH, n=5))
    L, r = 4.60, 0.22
    if not fallen:
        a = math.atan2(th + 0.05 + r - 0.25, 2.8)
        p0 = (-2.8 + 0.0, 0.25 + r * 0.0, 0.0)
        p1 = (p0[0] + L * math.cos(a), p0[1] + L * math.sin(a), 0.0)
        out.append(logp(p0, p1, r, n=10))
        out.append(W(-3.05, -2.55, 0.0, 0.25, -0.30, 0.30, WEATH))                                     # foot block
        # the saw in the kerf, half way down the log: blade + handle
        s = 0.55
        c = (p0[0] + (p1[0] - p0[0]) * s, p0[1] + (p1[1] - p0[1]) * s)
        blade = xf(W(-0.30, 0.30, -0.18, 0.18, -0.004, 0.004, IRON, vis=(1,)), rz=math.degrees(a) + 90.0,
                   t=(c[0], c[1] + r + 0.05, 0.0))
        out.append(blade)
        out.append(pole((c[0] - 0.10, c[1] + r + 0.25, 0.0), (c[0] - 0.55, c[1] + r + 0.80, 0.0), 0.02, WOOD, n=5,
                        vis=(1,)))
        cols = [logc(p0, p1, r, n=6)]
    else:
        p0, p1 = (-2.6, r, 0.95), (2.0, r, 1.25)
        out.append(logp(p0, p1, r, n=10))
        out.append(xf(W(-0.35, 0.35, 0.0, 0.008, -0.20, 0.20, IRON, vis=(1,)), ry=15.0, t=(-1.0, 0.0, -0.75)))
        out.append(pole((-0.70, 0.02, -0.80), (-0.10, 0.02, -1.00), 0.02, WOOD, n=5, vis=(1,)))
        cols = [logc(p0, p1, r, n=6)]
    for k in range(3):                                                                                     # wedges
        out.append(xf(prism([(0.0, 0.0), (0.18, 0.0), (0.0, 0.05)], "z", -0.03, 0.03, NEW, vis=(1,)), ry=60.0 * k,
                      t=(0.60 + 0.12 * k, 0.0, 0.70)))
    out.append(xf(W(-0.07, 0.07, 0.0, 0.08, -0.05, 0.05, KURO, vis=(1,)), t=(0.80, 0.0, -0.75)))            # ink pot
    out.append(mound("sawdust", -0.6, 0.1, 0.70, 0.04, NEW, sx=1.6))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-3.05, 2.3, 0.0, 2.1 if not fallen else 0.5, -0.6, 0.6 if not fallen else 1.5, WEATH, vis=(2,)))
    cols.append(col(-0.38, 0.38, 0.0, 1.10, -0.48, 0.48, WEATH))          # the trestle's legs as one block (no overlap)
    P.adds(cols)
    P.dim("L", L, L, tol=0.01)
    P.notes.append("the sawyer's trestle with the log propped at an angle and the big rip saw in the kerf%s"
                   % (" (fallen: the log rolled off)" if fallen else ""))
    return P


def log_stack(collapsed=False):
    """Logs stacked 3-2-1 on two bearers with chocks (4.0 m, d 0.36-0.44), the dealer's mark on the ends (a dark
    brand); collapsed = the top logs rolled down."""
    P = LPart("log_stack", budget="furniture", mass=2500.0, anchor="floor")
    P.over_budget_ok = "six round logs with end grain: the round silhouette needs the segments"
    L = 4.0
    r = rng("logstack")
    out = [W(-1.6, -1.4, 0.0, 0.12, -1.1, 1.1, WEATH), W(1.4, 1.6, 0.0, 0.12, -1.1, 1.1, WEATH)]
    rows = [(3, 0.12), (2, None), (1, None)]
    logs = []
    rr = 0.20
    zs = [[-0.42, 0.0, 0.42], [-0.21, 0.21], [0.0]]
    y = 0.12 + rr
    for i, row in enumerate(zs):
        for z in row:
            logs.append((z, y, rr + r.uniform(-0.02, 0.02)))
        y += rr * 1.72
    if collapsed:
        logs = logs[:4] + [(1.40, 0.20, 0.20), (1.85, 0.20, 0.19)]
    cols = []
    for (z, yy, rad) in logs:
        out.append(logp((-L / 2, yy, z), (L / 2, yy, z), rad, n=9))
        cols.append(logc((-L / 2, yy, z), (L / 2, yy, z), rad - 0.01, n=6))
        out.append(W(L / 2 + 0.001, L / 2 + 0.004, yy - 0.05, yy + 0.05, z - 0.05, z + 0.05, KURO, vis=(1,)))  # mark
    for z in (-0.68, 0.68):
        out.append(xf(prism([(0.0, 0.0), (0.12, 0.0), (0.0, 0.12)], "x", -0.08, 0.08, WEATH, vis=(1,)),
                      ry=0.0 if z < 0 else 180.0, t=(-1.5, 0.12, z)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-L / 2, L / 2, 0.0, 1.2 if not collapsed else 0.8, -0.65, 0.65 if not collapsed else 1.6, WEATH, vis=(2,)))
    cols += [col(-1.6, -1.4, 0.0, 0.12, -1.1, 1.1, WEATH), col(1.4, 1.6, 0.0, 0.12, -1.1, 1.1, WEATH)]
    P.adds(cols)
    P.dim("L", L, L, tol=0.01)
    P.notes.append("logs stacked on bearers with chocks, the dealer's mark on the ends%s"
                   % ("; the top rolled down" if collapsed else ""))
    return P


def timber_upright(half=False):
    """Squared timber and poles stood upright against a rail (tate-kake; mount wall: the store's back wall), 3.4 m."""
    P = LPart("timber_upright", budget="furniture", mass=400.0, anchor="wall", flat=True)
    out = [W(-1.6, 1.6, 2.20, 2.30, 0.0, 0.08, WEATH)]
    for x in (-1.5, 0.0, 1.5):
        out.append(W(x - 0.05, x + 0.05, 2.15, 2.35, 0.0, 0.10, WEATH))
    r = rng("upright")
    n = 16 if not half else 7
    for k in range(n):
        x = -1.45 + 2.9 * k / 15
        s = r.uniform(0.09, 0.15)
        top = r.uniform(3.1, 3.5)
        foot = 0.45 + r.uniform(-0.05, 0.08)
        if k % 3 == 2:
            out.append(pole((x, 0.0, foot), (x, top, 0.12), s / 2 + 0.02, WEATH, n=7, caps=ENDG, vis=(1, 2)))
        else:
            d = core.sub((x, top, 0.12), (x, 0.0, foot))
            a = math.degrees(math.atan2(foot - 0.12, top))
            out.append(xf(W(-s / 2, s / 2, 0.0, top, -s / 2, s / 2, NEW if k % 2 else WEATH, vis=(1, 2)), rx=-a,
                          t=(x, 0.0, foot)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-1.6, 1.6, 0.0, 3.4, 0.0, 0.55, WEATH, vis=(2,)))
    P.dim("w", 3.2, 3.2, tol=0.01)
    P.notes.append("timber stood upright on the rack rail (tate-kake; mount wall; visual)%s"
                   % ("; half sold / taken" if half else ""))
    return P


def plank_stack(scattered=False):
    """Sawn planks stacked on bearers with stickers between the layers (air drying), 3.6 m."""
    P = LPart("plank_stack", budget="furniture", mass=500.0, anchor="floor")
    L, w = 3.6, 0.90
    out = [W(-1.4, -1.25, 0.0, 0.12, -w / 2 - 0.05, w / 2 + 0.05, WEATH), W(1.25, 1.4, 0.0, 0.12, -w / 2 - 0.05,
                                                                          w / 2 + 0.05, WEATH)]
    y = 0.12
    r = rng("planks")
    layers = 5 if not scattered else 2
    for j in range(layers):
        for k in range(4):
            z = -w / 2 + w * (k + 0.5) / 4
            out.append(W(-L / 2 + r.uniform(0, 0.05), L / 2 - r.uniform(0, 0.05), y, y + 0.03, z - 0.10, z + 0.10,
                         NEW if j % 2 else WEATH, vis=(1, 2)))
        y += 0.03
        if j < layers - 1:
            for x in (-1.3, 0.0, 1.3):
                out.append(W(x - 0.02, x + 0.02, y, y + 0.025, -w / 2, w / 2, WEATH, vis=(1,)))
            y += 0.025
    if scattered:
        for k in range(4):
            out.append(xf(W(-L / 2, L / 2, 0.0, 0.03, -0.10, 0.10, NEW), ry=8.0 * k - 12.0,
                          t=(0.2 * k, 0.0, w / 2 + 0.35 + 0.18 * k)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-L / 2, L / 2, 0.0, y, -w / 2, w / 2 + (1.1 if scattered else 0.0), WEATH, vis=(2,)))
    P.add(col(-L / 2, L / 2, 0.0, y, -w / 2, w / 2, WEATH))
    P.loot_rect("top", y, -1.4, 1.4, -0.25, 0.25, rng=0.12, points=[(x, y, 0.1125) for x in (-0.9, 0.0, 0.9)])
    P.dim("L", L, L, tol=0.01)
    P.notes.append("planks air-drying on bearers with stickers%s" % ("; half the stack pulled down" if scattered else ""))
    return P


def shingle_split(scattered=False):
    """The shingle splitter's place: a round splitting block (log section) with the froe (hegi-nata) in a bolt, the
    mallet, split shingles strewn, bundles of shingles tied with bamboo bands stacked beside."""
    P = LPart("shingle_split", budget="furniture", mass=80.0, anchor="floor")
    out = [logp((0.0, 0.0, 0.0), (0.0, 0.45, 0.0), 0.25, n=10)]
    bolt = W(-0.07, 0.07, 0.45, 0.80, -0.05, 0.05, NEW, vis=(1,))
    out.append(bolt)
    out.append(W(-0.12, 0.10, 0.66, 0.70, -0.004, 0.004, IRON, vis=(1,)))                             # froe blade
    out.append(pole((0.10, 0.68, 0.0), (0.42, 0.62, 0.0), 0.015, WOOD, n=5, vis=(1,)))                 # froe handle
    out.append(pole((0.35, 0.03, 0.35), (0.65, 0.03, 0.30), 0.02, WOOD, n=5, vis=(1,)))                # mallet
    out.append(pole((0.62, 0.05, 0.22), (0.62, 0.05, 0.40), 0.05, WEATH, n=6, vis=(1,)))
    r = rng("shingle")
    for k in range(10 if not scattered else 18):
        out.append(xf(W(-0.15, 0.15, 0.0, 0.006, -0.05, 0.05, NEW, vis=(1,)), ry=r.uniform(0, 180),
                      t=(r.uniform(-0.6, 0.6), 0.0 + 0.006 * (k % 2), r.uniform(0.3, 0.7))))
    # bundles: 3 stacked
    for k in range(3 if not scattered else 1):
        bx, by = -0.85 + (0.32 * (k % 2)), 0.20 * (k // 2)
        out.append(W(bx - 0.15, bx + 0.15, by, by + 0.20, -0.25, 0.05, NEW, vis=(1, 2)))
        for zz in (-0.18, -0.02):
            out.append(W(bx - 0.152, bx + 0.152, by + 0.03, by + 0.05, zz - 0.012, zz + 0.012, BAMBOO, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-1.0, 0.7, 0.0, 0.8, -0.3, 0.75, NEW, vis=(2,)))
    P.add(cyl_col(0.25, 0.0, 0.45, n=8, mat=WEATH))
    P.add(col(-1.0, -0.38, 0.0, 0.20 if scattered else 0.40, -0.25, 0.05, NEW))
    P.loot_rect("block", 0.45, 0.08, 0.20, -0.15, 0.10, rng=0.06, points=[(0.14, 0.45, -0.10)])
    P.dim("block_h", 0.45, 0.45, tol=0.005)
    P.notes.append("the shingle splitting block with the froe in a bolt, mallet, shingles and bundles%s"
                   % ("; bundles taken, shingles strewn" if scattered else ""))
    return P


# ================================================================================================ foundry
def koshikiro(fallen=False):
    """The koshiki-ro (the Japanese cupola, W3B_NOTES TR12): a clay base on stones, three stacked fire-clay rings
    tapering up to ~1.55 m (d 0.70 -> 0.55), iron hoops, the clay tuyere on the -x side (the bellows' pipe), the tap
    spout + clay channel on +z, cold slag; fallen = the top ring knocked off and broken on the floor."""
    P = LPart("koshikiro", budget="furniture", mass=900.0, anchor="floor")
    out = [W(-0.50, 0.50, 0.0, 0.30, -0.50, 0.50, CLAY)]
    for k in range(8):
        a = 2 * math.pi * k / 8
        out.append(W(0.47 * math.cos(a) - 0.08, 0.47 * math.cos(a) + 0.08, 0.0, 0.16, 0.47 * math.sin(a) - 0.06,
                     0.47 * math.sin(a) + 0.06, FIELD, vis=(1,)))
    rings = [(0.30, 0.70, 0.35), (0.70, 1.10, 0.32), (1.10, 1.50, 0.29)]
    if fallen:
        rings = rings[:2]
    for (y0, y1, R) in rings:
        out.append(lathe([(0.0, y0), (R, y0), (R - 0.01, y1), (R - 0.08, y1), (R - 0.07, y0 + 0.05), (0.0, y0 + 0.05)],
                         12, CLAY, vis=(1,)))
        out.append(lathe([(R - 0.004, y0 + 0.06), (R + 0.012, y0 + 0.06), (R + 0.012, y0 + 0.10), (R - 0.004, y0 + 0.10)],
                         12, IRON, vis=(1,), closed_ends=False))
    top = rings[-1][1]
    out.append(lathe([(0.0, top - 0.08), (rings[-1][2] - 0.08, top - 0.08), (rings[-1][2] - 0.08, top - 0.06),
                      (0.0, top - 0.06)], 10, "ground_ash", vis=(1,)))                                # dead charge
    out.append(pole((-0.70, 0.42, 0.0), (-0.30, 0.42, 0.0), 0.06, CLAY, n=8, vis=(1,)))                 # tuyere
    out.append(pole((0.0, 0.34, 0.30), (0.0, 0.30, 0.62), 0.05, CLAY, n=6, vis=(1,)))                    # tap spout
    out.append(W(-0.10, 0.10, 0.0, 0.08, 0.50, 1.10, CLAY, vis=(1,)))                                    # channel
    out.append(mound("slag", 0.30, 0.80, 0.25, 0.08, DARK))
    if fallen:
        r = rng("ring")
        for k in range(4):
            a = 2 * math.pi * k / 4 + 0.3
            out.append(xf(lathe([(0.22, 0.0), (0.29, 0.0), (0.29, 0.35), (0.22, 0.35)], 4, CLAY, vis=(1,),
                                 closed_ends=True), ry=40.0 * k, rz=80.0 + 10 * k,
                          t=(0.85 + 0.25 * math.cos(a), 0.12, -0.30 + 0.25 * math.sin(a))))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.50, 0.50, 0.0, 0.30, -0.50, 0.50, CLAY, vis=(2,)))
    P.add(lathe([(0.0, 0.30), (0.35, 0.30), (0.29, top), (0.0, top)], 8, CLAY, vis=(2,)))
    P.add(W(-0.50, 0.50, 0.0, top, -0.50, 0.50, CLAY, vis=(3,)))
    P.res3 = True
    P.add(col(-0.50, 0.50, 0.0, 0.30, -0.50, 0.50, CLAY))
    P.add(cyl_col(0.35, 0.30, top, n=8, mat=CLAY))
    P.loot_rect("base", 0.30, 0.36, 0.46, -0.40, 0.40, rng=0.05, points=[(0.44, 0.30, 0.44)])
    P.dim("h", top, top, tol=0.01)
    P.notes.append("the koshiki-ro cupola furnace, cold: stacked clay rings, tuyere on -x, tap spout on +z%s"
                   % ("; the top ring knocked off and broken" if fallen else ""))
    return P


def fumifuigo(broken=False):
    """The treadle bellows (fumi-fuigo): a long box 1.60 x 0.90 x 0.45 sunk a little in the floor, the seesaw board
    on its central pivot (workers stood on it and rocked), the wind trunk out of the -z end to the furnace's
    tuyere; broken = the board split and lying askew."""
    P = LPart("fumifuigo", budget="furniture", mass=200.0, anchor="floor")
    w, L, h = 0.90, 1.60, 0.45
    out = [W(-w / 2, w / 2, 0.0, h - 0.04, -L / 2, L / 2, SOOTW)]
    for sz in (-1, 1):
        out.append(W(-w / 2 - 0.005, w / 2 + 0.005, 0.05, h - 0.06, sz * L * 0.3 - 0.025, sz * L * 0.3 + 0.025, IRON,
                     vis=(1,)))
    out.append(W(-0.06, 0.06, h - 0.04, h + 0.06, -0.06, 0.06, WEATH))                                # pivot block
    bd = xf(W(-w / 2 + 0.05, w / 2 - 0.05, -0.025, 0.025, -L / 2 + 0.05, L / 2 - 0.05, WEATH), rx=8.0,
            t=(0.0, h + 0.09, 0.0))
    if broken:
        bd = xf(W(-w / 2 + 0.05, w / 2 - 0.05, 0.0, 0.05, -0.60, 0.20, WEATH), ry=20.0, rz=10.0, t=(0.55, 0.0, 0.70))
    out.append(bd)
    out.append(W(-0.15, 0.15, 0.10, 0.32, -L / 2 - 0.45, -L / 2, SOOTW))                                # wind trunk
    out.append(pole((0.0, 0.21, -L / 2 - 0.45), (0.0, 0.21, -L / 2 - 0.65), 0.07, CLAY, n=8, vis=(1,)))
    for sx in (-1, 1):                                                                          # hand rails / posts
        out.append(pole((sx * (w / 2 + 0.25), 0.0, 0.0), (sx * (w / 2 + 0.25), 1.75, 0.0), 0.04, WEATH, n=6))
    out.append(pole((-(w / 2 + 0.25), 1.55, 0.0), ((w / 2 + 0.25), 1.55, 0.0), 0.035, WEATH, n=6))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2 - 0.3, w / 2 + 0.3, 0.0, 1.75, -L / 2 - 0.65, L / 2, SOOTW, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -L / 2, L / 2, SOOTW))
    P.add(col(-0.15, 0.15, 0.10, 0.32, -L / 2 - 0.45, -L / 2, SOOTW))
    for sx in (-1, 1):
        P.add(pole((sx * (w / 2 + 0.25), 0.0, 0.0), (sx * (w / 2 + 0.25), 1.75, 0.0), 0.04, WEATH, n=6, vis=(),
                   geo=True, view=True, fire=True))
    P.loot_rect("box", h - 0.04, -w / 2 + 0.10, -0.12, -L / 2 + 0.15, -0.20, rng=0.1, points=[(-0.28, h - 0.04, -0.50)])
    P.dim("L", L, L, tol=0.005)
    P.notes.append("the treadle bellows (fumi-fuigo) with its seesaw board and wind trunk to the tuyere (-z)%s"
                   % ("; board split off" if broken else ""))
    return P


def imono_moulds(broken=False):
    """The sand casting bed: a low board-edged bed of moulding sand with three clay moulds bedded in it (pot / rice
    kettle / tea kettle sizes: cope on drag, the pouring cup on top), loose cores; broken = moulds knocked open, a
    cast pot showing."""
    P = LPart("imono_moulds", budget="furniture", mass=300.0, anchor="floor")
    w, d = 1.80, 1.00
    out = [W(-w / 2, w / 2, 0.0, 0.12, -d / 2, -d / 2 + 0.04, WEATH), W(-w / 2, w / 2, 0.0, 0.12, d / 2 - 0.04, d / 2, WEATH),
           W(-w / 2, -w / 2 + 0.04, 0.0, 0.12, -d / 2 + 0.04, d / 2 - 0.04, WEATH),
           W(w / 2 - 0.04, w / 2, 0.0, 0.12, -d / 2 + 0.04, d / 2 - 0.04, WEATH),
           W(-w / 2 + 0.04, w / 2 - 0.04, 0.0, 0.10, -d / 2 + 0.04, d / 2 - 0.04, SAND, vis=(1,))]
    moulds = [(-0.55, 0.0, 0.30, 0.28), (0.05, 0.05, 0.26, 0.24), (0.55, -0.05, 0.20, 0.30)]
    for i, (cx, cz, R, hh) in enumerate(moulds):
        if broken and i == 1:
            out.append(xf(lathe([(0.0, 0.0), (R - 0.04, 0.0), (R - 0.02, 0.10), (R - 0.06, 0.10), (R - 0.07, 0.02),
                                 (0.0, 0.02)], 12, IRON, vis=(1,)), t=(cx, 0.10, cz)))            # the pot inside
            for k in range(3):
                out.append(xf(lathe([(R - 0.06, 0.0), (R, 0.0), (R, hh * 0.6), (R - 0.06, hh * 0.6)], 3, CLAY, vis=(1,)),
                              ry=120.0 * k, rz=70.0, t=(cx + 0.40 * math.cos(2.1 * k), 0.10, cz + 0.35 * math.sin(2.1 * k))))
            continue
        out.append(lathe([(0.0, 0.10), (R, 0.10), (R * 0.9, 0.10 + hh), (0.05, 0.10 + hh), (0.05, 0.10 + hh + 0.06),
                          (0.0, 0.10 + hh + 0.06)], 12, CLAY, vis=(1,)))
        out[-1] = xf(out[-1], t=(cx, 0.0, cz))
        out.append(xf(lathe([(R - 0.01, 0.10 + hh * 0.45), (R + 0.006, 0.10 + hh * 0.45), (R + 0.006, 0.10 + hh * 0.52),
                             (R - 0.01, 0.10 + hh * 0.52)], 12, DARK, vis=(1,), closed_ends=False), t=(cx, 0.0, cz)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, 0.45, -d / 2, d / 2, CLAY, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, 0.12, -d / 2, d / 2, WEATH))
    P.loot_rect("bed", 0.10, -0.80, 0.80, 0.36, 0.42, rng=0.06, points=[(-0.20, 0.10, 0.40)])
    P.dim("w", w, w, tol=0.005)
    P.notes.append("the sand casting bed with clay moulds for a pot, a rice kettle and a tea kettle%s"
                   % ("; one knocked open, the cast pot inside" if broken else ""))
    return P


def toribe_rack():
    """Long-handled clay-lined ladles (tori-be) and skimmers on a wall rack (mount wall)."""
    P = LPart("toribe_rack", budget="furniture", mass=25.0, anchor="wall", flat=True)
    out = [W(-0.75, 0.75, 1.55, 1.65, 0.0, 0.025, SOOTW)]
    for k, x in enumerate((-0.55, -0.20, 0.15, 0.50)):
        out.append(peg(x, 1.60, L=0.10, z0=0.0))
        z = 0.10
        out.append(pole((x, 1.62, z), (x + 0.05, 0.25, z + 0.02), 0.016, WEATH, n=5, vis=(1,)))
        if k < 3:
            out.append(xf(lathe([(0.0, 0.0), (0.12, 0.0), (0.14, 0.12), (0.12, 0.12), (0.10, 0.03), (0.0, 0.03)], 10,
                                IRON if k % 2 else CLAY, vis=(1,)), t=(x + 0.05, 0.12, z + 0.04)))
        else:
            out.append(W(x - 0.08, x + 0.16, 0.18, 0.26, z, z + 0.01, IRON, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.75, 0.75, 0.10, 1.65, 0.0, 0.25, SOOTW, vis=(2,)))
    P.dim("w", 1.50, 1.50, tol=0.005)
    P.notes.append("the casting ladles (tori-be) and a skimmer on the wall (mount wall; visual)")
    return P


def cast_pots(scattered=False):
    """New cast-iron goods cooling on a board rack: pots (nabe), rice kettles (kama) with their flanges, tea kettles
    (chagama); scattered = knocked off the rack. No side-spouted tetsubin (mid-18th c. on)."""
    P = LPart("cast_pots", budget="furniture", mass=120.0, anchor="floor")
    w, d, h = 1.40, 0.55, 0.45
    out = [W(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, WEATH), W(-w / 2, w / 2, 0.10, 0.13, -d / 2, d / 2, WEATH)]
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * (w / 2 - 0.04) - 0.03, sx * (w / 2 - 0.04) + 0.03, 0.0, h - 0.03, sz * (d / 2 - 0.04) - 0.03,
                         sz * (d / 2 - 0.04) + 0.03, WEATH))

    def nabe(R):
        return lathe([(0.0, 0.0), (R * 0.7, 0.0), (R, R * 0.45), (R * 0.96, R * 0.47), (R * 0.66, R * 0.04),
                      (0.0, R * 0.04)], 12, IRON, vis=(1,))

    def kama(R):
        return lathe([(0.0, 0.0), (R * 0.8, 0.0), (R, R * 0.5), (R * 1.35, R * 0.55), (R * 1.35, R * 0.6),
                      (R * 0.9, R * 0.62), (R * 0.85, R * 0.9), (R * 0.75, R * 0.9), (R * 0.70, R * 0.06),
                      (0.0, R * 0.06)], 12, IRON, vis=(1,))

    def chagama(R):
        return lathe([(0.0, 0.0), (R * 0.6, 0.0), (R, R * 0.6), (R * 0.8, R * 1.1), (R * 0.45, R * 1.2),
                      (R * 0.45, R * 1.3), (R * 0.38, R * 1.3), (R * 0.38, R * 1.15), (0.0, R * 1.15)], 12, IRON,
                     vis=(1,))
    goods = [(nabe(0.20), -0.45, h, 0.0), (kama(0.16), -0.05, h, 0.0), (chagama(0.13), 0.38, h, 0.0),
             (nabe(0.17), -0.40, 0.13, 0.05), (kama(0.14), 0.15, 0.13, 0.0), (nabe(0.15), 0.48, 0.13, -0.05)]
    for i, (s, x, y, z) in enumerate(goods):
        if scattered and i in (0, 2):
            out.append(xf(s, rz=95.0, t=(x * 0.6 + 0.3, 0.18, d / 2 + 0.35 + 0.2 * i)))
        else:
            out.append(xf(s, t=(x, y, z)))
    wear_all(out, "_w1")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.20, -d / 2, d / 2, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.loot_rect("rack", h, -0.20, 0.20, -0.20, -0.12, rng=0.06, points=[(0.15, h, -0.18)])
    P.dim("w", w, w, tol=0.005)
    P.notes.append("new cast-iron pots, rice kettles and tea kettles on a cooling rack%s"
                   % ("; two knocked off" if scattered else ""))
    return P


def scrap_heap():
    """Scrap iron for the melt: broken pots, plough shares, bars, in a low heap."""
    P = LPart("scrap_heap", budget="furniture", mass=200.0, anchor="floor")
    out = [mound("scrap", 0.0, 0.0, 0.50, 0.09, "ground_ash", sx=1.3)]
    r = rng("scrapheap")
    for k in range(12):
        x, z = r.uniform(-0.55, 0.55), r.uniform(-0.40, 0.40)
        if k % 3 == 0:
            out.append(xf(lathe([(0.10, 0.0), (0.16, 0.0), (0.16, 0.08), (0.10, 0.08)], 3, IRON, vis=(1,)),
                          rz=r.uniform(20, 80), ry=r.uniform(0, 360), t=(x, 0.15, z)))
        else:
            out.append(xf(W(-0.20, 0.20, -0.012, 0.012, -0.03, 0.03, IRON, vis=(1,)), ry=r.uniform(0, 180),
                          rz=r.uniform(-25, 25), t=(x, 0.12 + r.uniform(0, 0.08), z)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.75, 0.75, 0.0, 0.30, -0.55, 0.55, IRON, vis=(2,)))
    P.add(col(-0.55, 0.55, 0.0, 0.18, -0.38, 0.38, IRON))
    P.dim("h", 0.30, 0.30, tol=0.1)
    P.notes.append("scrap iron for the melt (visual heap; loot around it)")
    return P


def bell_mould():
    """The on-site bell casting kit (BT 'Bell caster, on site'): a dug pit ringed by an earth bank, the clay outer
    mould (cope) of a temple bell standing in it (d 0.95, h 1.55) bound with iron bands and props, a pouring cup on
    top, a small furnace ring of clay and a heap of charcoal bales beside (separate props)."""
    P = LPart("bell_mould", budget="furniture", mass=3000.0, anchor="floor")
    out = []
    for k in range(12):                                                                           # the earth bank
        a = 2 * math.pi * k / 12
        out.append(xf(W(-0.40, 0.40, 0.0, 0.30, -0.25, 0.25, SAND, vis=(1, 2)), ry=-math.degrees(a),
                      t=(1.25 * math.cos(a), 0.0, 1.25 * math.sin(a))))
    out.append(lathe([(0.0, 0.0), (1.05, 0.0), (1.05, 0.02), (0.0, 0.02)], 12, "ground_doma_earth", vis=(1,)))
    R, H = 0.48, 1.55
    out.append(lathe([(0.0, 0.0), (R + 0.06, 0.0), (R + 0.04, 0.20), (R - 0.02, H - 0.25), (R - 0.10, H - 0.05),
                      (0.12, H), (0.12, H + 0.12), (0.0, H + 0.12)], 14, CLAY, vis=(1, 2)))
    for y in (0.25, 0.70, 1.15):
        rr = R + 0.05 - 0.06 * (y / H)
        out.append(lathe([(rr - 0.01, y), (rr + 0.012, y), (rr + 0.012, y + 0.05), (rr - 0.01, y + 0.05)], 14, IRON,
                         vis=(1,), closed_ends=False))
    out.append(lathe([(0.0, H + 0.12), (0.16, H + 0.12), (0.20, H + 0.26), (0.16, H + 0.26), (0.10, H + 0.16),
                      (0.0, H + 0.16)], 10, CLAY, vis=(1,)))                                       # pouring cup
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.5
        out.append(pole((0.95 * math.cos(a), 0.30, 0.95 * math.sin(a)), (0.50 * math.cos(a), 1.10, 0.50 * math.sin(a)),
                        0.04, WEATH, n=5))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(lathe([(0.0, 0.0), (R + 0.06, 0.0), (0.12, H + 0.26), (0.0, H + 0.26)], 8, CLAY, vis=(2,)))
    P.add(lathe([(0.0, 0.0), (1.45, 0.0), (1.45, 0.30), (0.0, 0.30)], 8, SAND, vis=(2,)))
    P.add(lathe([(0.0, 0.0), (1.45, 0.0), (1.45, 0.30), (0.0, 0.30)], 8, SAND, vis=(3,)))
    P.res3 = True
    P.add(cyl_col(R + 0.06, 0.0, H + 0.12, n=8, mat=CLAY))
    P.loot_rect("pit", 0.02, 0.70, 0.90, -0.10, 0.10, rng=0.08, kind="floor", points=[(0.80, 0.02, 0.0)])
    P.dim("h", H + 0.26, H + 0.26, tol=0.01)
    P.notes.append("the on-site bell casting: the clay cope of a temple bell in its pit, banded and propped, the "
                   "pouring cup on top (cold; never poured)")
    return P


PROPS = [
    {"id": "jp_f_yubune", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_yubune", "std", "drained", "Bath tub (yubune), drained", lambda: yubune()),
        M("jp_f_yubune_staved", "std", "broken", "Bath tub, drained, a board split", lambda: yubune(True))]},
    {"id": "jp_f_bath_boiler", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_bath_boiler", "std", "cold", "Bath boiler fire mouth, cold", lambda: bath_boiler()),
        M("jp_f_bath_boiler_ab", "std", "ransacked", "Bath boiler fire mouth, door off, ash raked out",
          lambda: bath_boiler(True))]},
    {"id": "jp_f_bath_stools", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_bath_stools", "std", "intact", "Bath stools and buckets", lambda: bath_stools()),
        M("jp_f_bath_stools_tipped", "std", "tipped", "Bath stools and buckets, knocked over", lambda: bath_stools(True))]},
    {"id": "jp_f_bandai", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_bandai", "std", "intact", "Bathhouse pay counter (bandai) with the cashbox", lambda: bandai()),
        M("jp_f_bandai_ab", "std", "ransacked", "Bathhouse pay counter, cashbox forced", lambda: bandai(True))]},
    {"id": "jp_f_nagashi", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_nagashi", "std", "intact", "Slatted washing floor (nagashi) over its drain", lambda: nagashi()),
        M("jp_f_nagashi_warped", "std", "warped", "Washing floor, slats warped and missing", lambda: nagashi(True))]},
    {"id": "jp_f_datsui_dana", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_datsui_dana", "std", "intact", "Clothes cubbies with baskets", lambda: datsui_dana()),
        M("jp_f_datsui_dana_ransacked", "std", "ransacked", "Clothes cubbies, ransacked", lambda: datsui_dana(True))]},
    {"id": "jp_f_tack_wall", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_tack_wall", "std", "intact", "Tack on pegs: straw horseshoes, halter, girth", lambda: tack_wall()),
        M("jp_f_tack_wall_taken", "std", "taken", "Tack on pegs, half taken", lambda: tack_wall(True))]},
    {"id": "jp_f_ekisha_table", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_ekisha_table", "std", "intact", "Fortune-teller's table", lambda: ekisha_table()),
        M("jp_f_ekisha_table_upset", "std", "upset", "Fortune-teller's table, knocked over", lambda: ekisha_table(True))]},
    {"id": "jp_f_barber_kit", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_barber_kit", "std", "intact", "Barber's kit box with basin", lambda: barber_kit()),
        M("jp_f_barber_kit_spilled", "std", "spilled", "Barber's kit box, spilled", lambda: barber_kit(True))]},
    {"id": "jp_f_misemono_sign", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_misemono_sign", "std", "intact", "Show booth signboard", lambda: misemono_sign()),
        M("jp_f_misemono_sign_torn", "std", "torn", "Show booth signboard, torn", lambda: misemono_sign(True))]},
    {"id": "jp_f_show_cage", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_show_cage", "std", "empty", "Bamboo animal cage, empty", lambda: show_cage()),
        M("jp_f_show_cage_open", "std", "broken", "Bamboo animal cage, bars broken out", lambda: show_cage(True))]},
    {"id": "jp_f_kezuridai", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kezuridai", "std", "intact", "Planing beam with a plane", lambda: kezuridai()),
        M("jp_f_kezuridai_knocked", "std", "knocked", "Planing beam, plane knocked off", lambda: kezuridai(True))]},
    {"id": "jp_f_sawhorses", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_sawhorses", "std", "intact", "Sawhorses with a board", lambda: sawhorses()),
        M("jp_f_sawhorses_knocked", "std", "knocked", "Sawhorses, one knocked over", lambda: sawhorses(True))]},
    {"id": "jp_f_dogubako", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_dogubako", "std", "open", "Joiner's tool chest, open", lambda: dogubako()),
        M("jp_f_dogubako_ransacked", "std", "ransacked", "Joiner's tool chest, tools strewn", lambda: dogubako(True))]},
    {"id": "jp_f_frames_lean", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_frames_lean", "std", "intact", "Shoji and door frames leaning on the wall", frames_lean)]},
    {"id": "jp_f_rokuro", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_rokuro", "std", "intact", "Woodturner's strap lathe", lambda: rokuro()),
        M("jp_f_rokuro_broken", "std", "broken", "Woodturner's strap lathe, strap snapped", lambda: rokuro(True))]},
    {"id": "jp_f_soroban_tray", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_soroban_tray", "std", "intact", "Abacus maker's tray", soroban_tray)]},
    {"id": "jp_f_bamboo_stock", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_bamboo_stock", "std", "intact", "Bamboo poles stood on the wall", lambda: bamboo_stock()),
        M("jp_f_bamboo_stock_scattered", "std", "fallen", "Bamboo poles, fallen", lambda: bamboo_stock(True))]},
    {"id": "jp_f_basket_work", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_basket_work", "std", "intact", "Basket maker's place", lambda: basket_work()),
        M("jp_f_basket_work_abandoned", "std", "abandoned", "Basket maker's place, kicked over",
          lambda: basket_work(True))]},
    {"id": "jp_f_togidai", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_togidai", "std", "intact", "Sword polisher's stand", lambda: togidai()),
        M("jp_f_togidai_upset", "std", "upset", "Sword polisher's stand, upset", lambda: togidai(True))]},
    {"id": "jp_f_urushi_tray", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_urushi_tray", "std", "intact", "Lacquerer's work board", lambda: urushi_tray()),
        M("jp_f_urushi_tray_spilled", "std", "spilled", "Lacquerer's work board, lacquer spilt",
          lambda: urushi_tray(True))]},
    {"id": "jp_f_kinko_bench", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kinko_bench", "std", "intact", "Sword-fittings maker's bench", lambda: kinko_bench()),
        M("jp_f_kinko_bench_taken", "std", "taken", "Sword-fittings maker's bench, guards taken",
          lambda: kinko_bench(True))]},
    {"id": "jp_f_saw_trestle", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_saw_trestle", "std", "intact", "Sawyer's trestle with the log and the big saw", lambda: saw_trestle()),
        M("jp_f_saw_trestle_fallen", "std", "fallen", "Sawyer's trestle, the log rolled off",
          lambda: saw_trestle(True))]},
    {"id": "jp_f_log_stack", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_log_stack", "std", "intact", "Log stack on bearers", lambda: log_stack()),
        M("jp_f_log_stack_collapsed", "std", "collapsed", "Log stack, top rolled down", lambda: log_stack(True))]},
    {"id": "jp_f_timber_upright", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_timber_upright", "std", "intact", "Timber stood upright on its rack", lambda: timber_upright()),
        M("jp_f_timber_upright_half", "std", "taken", "Timber rack, half taken", lambda: timber_upright(True))]},
    {"id": "jp_f_plank_stack", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_plank_stack", "std", "intact", "Planks air-drying on bearers", lambda: plank_stack()),
        M("jp_f_plank_stack_scattered", "std", "scattered", "Plank stack, pulled down", lambda: plank_stack(True))]},
    {"id": "jp_f_shingle_split", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_shingle_split", "std", "intact", "Shingle splitting block, froe, bundles", lambda: shingle_split()),
        M("jp_f_shingle_split_scattered", "std", "scattered", "Shingle splitting block, shingles strewn",
          lambda: shingle_split(True))]},
    {"id": "jp_f_koshikiro", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_koshikiro", "std", "cold", "Cupola furnace (koshiki-ro), cold", lambda: koshikiro()),
        M("jp_f_koshikiro_fallen", "std", "broken", "Cupola furnace, top ring broken", lambda: koshikiro(True))]},
    {"id": "jp_f_fumifuigo", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_fumifuigo", "std", "intact", "Treadle bellows (fumi-fuigo)", lambda: fumifuigo()),
        M("jp_f_fumifuigo_broken", "std", "broken", "Treadle bellows, board split off", lambda: fumifuigo(True))]},
    {"id": "jp_f_imono_moulds", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_imono_moulds", "std", "intact", "Sand casting bed with clay moulds", lambda: imono_moulds()),
        M("jp_f_imono_moulds_broken", "std", "broken", "Casting bed, a mould knocked open", lambda: imono_moulds(True))]},
    {"id": "jp_f_toribe_rack", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_toribe_rack", "std", "intact", "Casting ladles on a wall rack", toribe_rack)]},
    {"id": "jp_f_cast_pots", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_cast_pots", "std", "intact", "New cast-iron pots and kettles on a rack", lambda: cast_pots()),
        M("jp_f_cast_pots_scattered", "std", "scattered", "Cast-iron pots, knocked off the rack",
          lambda: cast_pots(True))]},
    {"id": "jp_f_scrap_heap", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_scrap_heap", "std", "intact", "Scrap iron heap", scrap_heap)]},
    {"id": "jp_f_bell_mould", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_bell_mould", "std", "intact", "Bell casting mould in its pit", bell_mould)]},
]
