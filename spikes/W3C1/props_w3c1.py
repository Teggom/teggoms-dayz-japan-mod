"""W3C1 specialty props for the wave-3c-1 trade sites (spikes/W3C1/W3C1_NOTES.md): the sake brewery (big tubs, starter
tubs, stirring poles, the steaming hearth, the lever press, the koji bed and tray shelves, the foot-treadle mortar,
the sugidama, a Hatcho miso vat, a leaning ladder), the dyer (sukumo bales, lye drip tubs, the drying frame, the
shop-front cloths, the pole rack) and the paper mill (the vat with its mould and spring pole, the beating board, the
couching press, the drying-board rack, the bark steamer). Built into jp_furniture.pbo by spikes/W3C1/build_w3c1.py
(after B3a + L1 + S1 + W2F + W3B). Frames as fkit / lkit: 'floor' base centre on the floor, +z = front; 'wall' origin
on the floor below, wall face z = 0, the prop at +z; 'hang' origin = the beam underside, hangs down (-y).

Dead world, autumn: the brewery is between seasons (brewing is winter work): tubs dry and empty, the steamer cold, the
press slack, the sugidama brown. Every model has its 'as left' state; the second state is the ransacked or fallen one.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "W3B"))
sys.path.insert(0, os.path.join(DEV, "spikes", "W2F"))
import props_w3b as P3  # noqa: E402  (W3B helpers, read-only)
from props_w2f_sacred import (core, box, prism, lathe, xf, xfs, W, col, cyl_col, LPart, pole, cord,  # noqa
                              wear_all, rng, M, WOOD, WEATH, IRON, DARK, PALE, BAMBOO, ASH, ROPE, KINARI, INDIGO,
                              PAPER, KURO, CUTSTONE)
from bits import stain, mound, disc  # noqa: E402
from skit import beam  # noqa: E402
from jpparts.shapes import oriented_box  # noqa: E402

CAT = "brewfit"
SOOTW = "wood_sooted"
ENDG = "wood_endgrain"
CLAY = "wall_nakanuri_int"
STRAW = "straw_tawara"
RIVER = "stone_river"
FIELD = "stone_field"
CEDAR = "ground_leaf_litter"       # the brown, dried cedar sprigs of an autumn sugidama (the leaf-litter browns)
tub_shell, hoops, adds1 = P3.tub_shell, P3.hoops, P3.adds1


def ocol(p0, p1, w, h, mat=WEATH, up=(0.0, 1.0, 0.0)):
    """An oriented collision member (Geometry / View / Fire)."""
    return beam(p0, p1, w, h, mat, up=up, vis=(), geo=True, view=True, fire=True)


def stone_lump(r_, cx, cy, cz, s, mat=RIVER, n=7):
    """A small rounded river stone (convex ring solid) of size s with its top at cy + s / 2."""
    return core.stone(r_, cx, cz, s, s * 0.85, s * 0.75, cy + s * 0.5, mat, bury=0.0, n=n, flat_top=0.6, vis=(1,))


# ================================================================================================ brewery
def shikomi_oke(state="dry"):
    """The big fermentation tub (shikomi-oke, ~20 koku): cedar staves (lathe), five bamboo hoops, a plank lid half on,
    dry with a dark crust at the bottom. state 'ladder': a ladder leaning on it; 'staved': hoops slipped, five staves
    fallen out on the front (+z), the gap open."""
    P = LPart("shikomi_oke", budget="detail", mass=600.0, anchor="floor")
    R, H, t = 0.91, 1.70, 0.05
    n = 20
    skip = (3, 4, 5, 6, 7) if state == "staved" else ()
    out = [lathe([(R, 0.0), (R, H), (R - t, H), (R - t, 0.06), (0.0, 0.06)], n, WEATH, vis=(1,), skip=skip)]
    out.append(lathe([(0.0, 0.0), (R - 0.01, 0.0), (R - 0.01, 0.06), (0.0, 0.06)], n, WEATH, vis=(1,)))
    out.append(disc(R - t - 0.01, 0.06, 0.075, "ground_ash", n=12, vis=(1,)))          # the dry crust
    ys = (0.12, 0.32) if state == "staved" else (0.18, 0.55, 0.92, 1.29, 1.60)
    out += hoops(R, ys, n=n)
    if state == "staved":
        r_ = rng("oke_staves")
        for k in range(5):
            a = (3.5 + k) * 2 * math.pi / n
            L = H * r_.uniform(0.85, 1.0)
            st = W(-0.14, 0.14, 0.0, 0.035, 0.0, L, WEATH, vis=(1,))
            out.append(xf(st, ry=math.degrees(-a) + r_.uniform(-25, 25),
                          t=(R * math.sin(a) * 1.05, 0.0, R * math.cos(a) * 1.05)))
    else:
        # the lid: four planks over the back half, a cross batten
        for k in range(4):
            z0 = -R + 0.10 + k * 0.23
            hw = math.sqrt(max(0.05, R * R - (z0 + 0.11) ** 2)) - 0.04
            out.append(W(-hw, hw, H, H + 0.035, z0, z0 + 0.22, WEATH, vis=(1,)))
        out.append(W(-0.05, 0.05, H + 0.035, H + 0.075, -R + 0.12, -0.02, WEATH, vis=(1,)))
    if state == "ladder":
        rl = [(-0.24, 0.0, R + 0.78), (-0.24, H + 0.15, R - 0.02)]
        for sx in (-0.24, 0.24):
            out.append(pole((sx, 0.0, R + 0.78), (sx, H + 0.15, R - 0.02), 0.03, WEATH, n=5, vis=(1,)))
        for k in range(1, 7):
            f = k / 7.0
            y, z = f * (H + 0.15), R + 0.78 - f * 0.80
            out.append(pole((-0.24, y, z), (0.24, y, z), 0.018, WEATH, n=4, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(lathe([(R, 0.0), (R, H), (R - t, H), (R - t, 0.10), (0.0, 0.10)], 10, WEATH, vis=(2,),
                skip=(1, 2) if state == "staved" else ()))
    if state == "ladder":
        P.add(W(-0.27, 0.27, 0.0, H, R + 0.02, R + 0.70, WEATH, vis=(2,)))
    P.add(cyl_col(R, 0.0, H, n=10, mat=WEATH))
    if state == "ladder":
        P.add(ocol((0.0, 0.035, R + 0.76), (0.0, H + 0.10, R + 0.03), 0.52, 0.05))
    P.dim("d", 2 * R, 2 * R, tol=0.005)
    P.dim("h", H + (0.075 if state != "staved" else 0.0), H + (0.075 if state != "staved" else 0.0), tol=0.20)
    P.notes.append("big fermentation tub (shikomi-oke, 1.82 x 1.70), dry; %s" % {
        "dry": "plank lid half on", "ladder": "lid half on, a ladder leaning on it",
        "staved": "hoops slipped, five staves fallen out"}[state])
    return P


def hangiri(scattered=False):
    """Shallow starter tubs (hangiri, 1.10 across x 0.28): three stacked + one set out (scattered: knocked about)."""
    P = LPart("hangiri", budget="furniture", mass=40.0, anchor="floor")
    R, h = 0.55, 0.28
    out = []
    if scattered:
        poses = [((-0.20, 0.0, -0.10), 0.0, 0.0), ((0.75, 0.0, 0.55), 0.0, 0.0), ((-0.70, 0.30, 0.70), 70.0, 30.0)]
    else:
        poses = [((-0.30, 0.0, 0.0), 0.0, 0.0), ((-0.30, h - 0.03, 0.0), 0.0, 0.0), ((-0.30, 2 * h - 0.06, 0.0), 0.0, 0.0),
                 ((0.85, 0.0, 0.10), 0.0, 0.0)]
    for (c, rx, ry) in poses:
        tub = [tub_shell(R, h, 0.03, WEATH, n=14)] + hoops(R, (0.07, 0.20), n=14)
        out += [xf(s, rx=rx, ry=ry, t=c) for s in tub]
    wear_all(out, "_w2")
    adds1(P, out)
    if scattered:
        P.add(W(-0.75, 1.30, 0.0, 0.30, -0.65, 1.15, WEATH, vis=(2,)))
        P.add(cyl_col(R, 0.0, h, cx=-0.20, cz=-0.10, mat=WEATH))
        P.add(cyl_col(R * 0.8, 0.0, h, cx=0.95, cz=0.75, mat=WEATH))
        P.loot_rect("tub", 0.03, -0.45, 0.05, -0.35, 0.15, rng=0.15, kind="floor", per=1.0)
    else:
        P.add(W(-0.30 - R, -0.30 + R, 0.0, 3 * h - 0.06, -R, R, WEATH, vis=(2,)))
        P.add(W(0.85 - R, 0.85 + R, 0.0, h, 0.10 - R, 0.10 + R, WEATH, vis=(2,)))
        P.add(cyl_col(R, 0.0, 3 * h - 0.06, cx=-0.30, mat=WEATH))
        P.add(cyl_col(R * 0.96, 0.0, h, cx=0.85 + 0.03, cz=0.10, mat=WEATH))
        P.loot_rect("top", 2 * h - 0.03, -0.55, -0.05, -0.20, 0.20, rng=0.15, per=1.0)
    P.dim("d", 2 * R, 2 * R, tol=0.005)
    P.notes.append("shallow starter tubs (hangiri)%s" % (", knocked about" if scattered else ", stacked + one set out"))
    return P


def kai_poles():
    """Stirring poles (kai: a long pole with a flat paddle head) and a bamboo broom leaning on the wall (mount wall)."""
    P = LPart("kai_poles", budget="small", mass=8.0, anchor="wall")
    out = []
    for k, x in enumerate((-0.45, -0.20, 0.10, 0.38)):
        top = (x + 0.05 * k, 2.35 - 0.05 * k, 0.022)
        foot = (x - 0.10, 0.0, 0.42)
        out.append(pole(foot, top, 0.018, WEATH, n=5, vis=(1,)))
        if k < 3:
            d = core.norm(core.sub(top, foot))
            c = core.add(foot, core.mul(d, 0.12))
            out.append(oriented_box(c, (1.0, 0.0, 0.0), d, core.norm(core.cross((1.0, 0.0, 0.0), d)), 0.09, 0.12,
                                    0.012, WEATH, vis=(1,)))
    out.append(pole((0.62, 0.0, 0.38), (0.70, 1.85, 0.018), 0.014, BAMBOO, n=5, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.60, 0.75, 0.0, 2.35, 0.02, 0.45, WEATH, vis=(2,)))
    P.add(col(-0.60, 0.75, 0.0, 2.30, 0.02, 0.40, WEATH))
    P.dim("h", 2.35, 2.35, tol=0.05)
    P.notes.append("stirring poles (kai) and a bamboo broom leaning on the wall")
    return P


def kamaba(state="cold"):
    """The kamaba hearth: a clay-and-stone kamado (2.20 x 1.90 x 0.85) with its fire mouth to the front (+z), the iron
    cauldron sunk in it, the cedar steamer (koshiki, 1.45 across x 1.15) on it with its lid, a stone step block at the
    left. state 'toppled': the koshiki knocked off and lying in front, the lid on the floor, the cauldron open."""
    P = LPart("kamaba", budget="detail", mass=3000.0, anchor="floor")
    w, d, h = 2.20, 1.90, 0.85
    r_ = rng("kamaba")
    out = [W(-w / 2, w / 2, 0.0, h - 0.04, -d / 2, d / 2, CLAY, vis=(1,))]
    out.append(W(-w / 2 - 0.02, w / 2 + 0.02, h - 0.04, h, -d / 2 - 0.02, d / 2 + 0.02, CUTSTONE, vis=(1,)))
    for k in range(7):                                           # facing stones along the front
        x = -w / 2 + 0.16 + k * (w - 0.32) / 6
        if abs(x) < 0.40:
            continue
        out.append(W(x - 0.15, x + 0.15, 0.04, 0.04 + r_.uniform(0.30, 0.42), d / 2, d / 2 + 0.03, FIELD, vis=(1,)))
    # the fire mouth: an arched dark opening with an iron frame, ash raked out on the floor
    out.append(W(-0.36, 0.36, 0.02, 0.62, d / 2, d / 2 + 0.04, IRON, vis=(1,)))
    out.append(W(-0.30, 0.30, 0.06, 0.56, d / 2 + 0.04, d / 2 + 0.041, "ground_ash", vis=(1,)))
    out.append(mound("kmash", 0.0, d / 2 + 0.35, 0.40, 0.05, "ground_ash"))
    # the cauldron rim (iron) in the top
    kc = (0.0, -0.05)
    out.append(lathe([(0.78, h - 0.01), (0.80, h + 0.06), (0.70, h + 0.06), (0.68, h - 0.01)], 16, IRON, vis=(1,),
                     closed_ends=False))
    out = [xf(s, t=(0.0, 0.0, 0.0)) for s in out]
    if state == "cold":
        ko = [lathe([(0.0, h + 0.06), (0.75, h + 0.06), (0.72, h + 1.15), (0.66, h + 1.15), (0.68, h + 0.12),
                     (0.0, h + 0.12)], 16, WEATH, vis=(1,))]
        ko += hoops(0.745, (h + 0.25, h + 0.70), n=16)
        ko += hoops(0.725, (h + 1.05,), n=16)
        ko.append(disc(0.70, h + 1.15, h + 1.19, WEATH, n=16, vis=(1,)))             # the lid
        ko.append(W(-0.04, 0.04, h + 1.19, h + 1.24, -0.55, 0.55, WEATH, vis=(1,)))
        out += [xf(s, t=(kc[0], 0.0, kc[1])) for s in ko]
    else:
        out.append(disc(0.68, h - 0.02, h, "ground_ash", n=16, vis=(1,)))           # the open cauldron, ash in it
        ko = [lathe([(0.0, 0.0), (0.75, 0.0), (0.72, 1.09), (0.66, 1.09), (0.68, 0.06), (0.0, 0.06)], 14, WEATH,
                    vis=(1,))]
        ko += hoops(0.745, (0.19, 0.64), n=14)
        out += [xf(s, rx=90.0, ry=80.0, t=(0.25, 0.73, d / 2 + 0.85)) for s in ko]
        out.append(xf(disc(0.70, 0.0, 0.04, WEATH, n=14, vis=(1,)), rz=12.0, t=(-0.75, 0.10, d / 2 + 0.55)))
    # the step block (cut stone) on the left
    out.append(W(-w / 2 - 0.55, -w / 2 - 0.05, 0.0, 0.40, -0.20, 0.30, CUTSTONE, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, CLAY, vis=(2,)))
    P.add(W(-w / 2 - 0.55, -w / 2 - 0.05, 0.0, 0.40, -0.20, 0.30, CUTSTONE, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, CLAY))
    P.add(col(-w / 2 - 0.55, -w / 2 - 0.06, 0.0, 0.40, -0.20, 0.30, CUTSTONE))
    if state == "cold":
        P.add(lathe([(0.0, h), (0.75, h), (0.72, h + 1.19), (0.0, h + 1.19)], 10, WEATH, vis=(2,)))
        P.add(cyl_col(0.74, h + 0.005, h + 1.19, n=10, cx=kc[0], cz=kc[1], mat=WEATH))
        P.loot_rect("hearth", h, w / 2 - 0.30, w / 2 - 0.06, -d / 2 + 0.10, d / 2 - 0.10, rng=0.12, per=0.8)
    else:
        P.add(W(-0.35, 0.85, 0.0, 1.50, d / 2 + 0.25, d / 2 + 1.45, WEATH, vis=(2,)))
        P.add(ocol((-0.35, 0.73, d / 2 + 0.80), (0.85, 0.73, d / 2 + 0.95), 1.40, 1.40))
        P.loot_rect("hearth", h, -w / 2 + 0.10, w / 2 - 0.10, d / 2 - 0.30, d / 2 - 0.10, rng=0.12, per=0.8)
    P.dim("w", w, w, tol=0.05)
    P.over_budget_ok = "the steaming hearth is the brewery's hero machine (kamado, cauldron, the hooped koshiki)"
    P.notes.append("the kamaba hearth: kamado + iron cauldron + cedar koshiki, cold%s" % (
        "" if state == "cold" else "; the koshiki knocked off and lying in front"))
    return P


def fune_press(state="slack"):
    """The lever press (fune + tenbin): the press box (2.40 x 0.95 x 0.95) with its lid and pressing blocks, the spout
    over a receiving jar; at the box's head two heavy posts (otoko-bashira) with a cross-beam under which the 6.4 m
    beam pivots; the beam lies over the blocks; at its free end six weight stones hang in rope slings. Along +x: the
    posts at +3.0, the free end at -3.3. state 'down': the slings cut, the beam's free end on the floor, the stones
    rolled about, the lid off."""
    P = LPart("fune_press", budget="detail", mass=4000.0, anchor="floor")
    r_ = rng("fune")
    out = []
    bx0, bx1, bw, bh = 0.30, 2.70, 0.95, 0.95
    # the box: thick boards, a spout at the low (-x) end, iron bands
    out.append(W(bx0, bx1, 0.0, 0.10, -bw / 2, bw / 2, SOOTW, vis=(1,)))
    for (a, b, z0_, z1_) in ((bx0, bx1, -bw / 2, -bw / 2 + 0.07), (bx0, bx1, bw / 2 - 0.07, bw / 2),
                             (bx0, bx0 + 0.07, -bw / 2 + 0.07, bw / 2 - 0.07),
                             (bx1 - 0.07, bx1, -bw / 2 + 0.07, bw / 2 - 0.07)):
        out.append(W(a, b, 0.10, bh, z0_, z1_, WEATH, vis=(1,)))
    for x in (bx0 + 0.25, bx1 - 0.25):
        out.append(W(x - 0.03, x + 0.03, 0.15, bh - 0.05, -bw / 2 - 0.012, bw / 2 + 0.012, IRON, vis=(1,)))
    out.append(W(bx0 - 0.22, bx0, 0.08, 0.14, -0.05, 0.05, WEATH, vis=(1,)))                 # spout
    # the receiving jar under the spout
    out.append(lathe([(0.0, 0.0), (0.20, 0.0), (0.26, 0.25), (0.20, 0.42), (0.16, 0.42), (0.16, 0.38),
                      (0.0, 0.38)], 12, DARK, vis=(1,)))
    out[-1] = xf(out[-1], t=(bx0 - 0.30, 0.0, 0.0))
    # inside: a few cloth bags left in the box (lees), the lid and pressing blocks
    for k in range(3):
        out.append(W(bx0 + 0.20 + k * 0.75, bx0 + 0.85 + k * 0.75, 0.10, 0.22, -0.35, 0.35, KINARI, vis=(1,)))
    if state == "slack":
        out.append(W(bx0 + 0.08, bx1 - 0.08, bh - 0.12, bh - 0.06, -bw / 2 + 0.08, bw / 2 - 0.08, WEATH, vis=(1,)))
        out.append(W(1.20, 1.80, bh - 0.06, bh + 0.30, -0.20, 0.20, WEATH, vis=(1,)))        # pressing blocks
        out.append(W(1.25, 1.75, bh + 0.30, bh + 0.52, -0.18, 0.18, WEATH, vis=(1,)))
    else:
        out.append(xf(W(-1.10, 1.10, 0.0, 0.06, -0.40, 0.40, WEATH, vis=(1,)), rz=70.0, t=(bx1 + 0.40, 0.90, 0.70)))
        out.append(W(0.30, 0.90, 0.0, 0.36, 0.80, 1.20, WEATH, vis=(1,)))
    # the head: two posts, the cross-beam, a footing sill
    px = 3.00
    for sz in (-0.55, 0.55):
        out.append(W(px - 0.14, px + 0.14, 0.0, 2.60, sz - 0.14, sz + 0.14, SOOTW, vis=(1,)))
    out.append(W(px - 0.16, px + 0.16, 2.05, 2.35, -0.75, 0.75, SOOTW, vis=(1,)))
    out.append(W(px - 0.25, px + 0.25, 0.0, 0.10, -0.80, 0.80, WEATH, vis=(1,)))
    # the beam
    if state == "slack":
        p0, p1 = (px + 0.10, 2.05 - 0.17, 0.0), (-3.30, 1.62, 0.0)
    else:
        p0, p1 = (px + 0.10, 2.05 - 0.17, 0.0), (-3.10, 0.17, 0.10)
    out.append(beam(p0, p1, 0.30, 0.32, SOOTW, vis=(1,)))
    # the weight stones in rope slings at the free end (slack) / on the floor (down)
    if state == "slack":
        for k in range(6):
            x = -3.05 + (k % 3) * 0.22 - 0.22
            zz = -0.22 if k < 3 else 0.22
            yb = 0.30 + 0.05 * (k % 3)
            out.append(stone_lump(r_, x, yb, zz, 0.36, RIVER, n=8))
            out.append(cord((x, yb + 0.30, zz), (x * 0.0 - 3.05, 1.47, zz * 0.3), r=0.012))
        out.append(W(-3.30, -2.80, 1.40, 1.48, -0.26, 0.26, WEATH, vis=(1,)))               # sling bar
    else:
        for k in range(6):
            a = 0.9 * k
            out.append(stone_lump(r_, -2.9 + 0.75 * math.cos(a), 0.0, 0.10 + 0.70 * math.sin(a), 0.34, RIVER, n=8))
    wear_all(out, "_w2")
    adds1(P, out)
    # Resolution 2
    P.add(W(bx0, bx1, 0.0, bh, -bw / 2, bw / 2, WEATH, vis=(2,)))
    P.add(W(px - 0.14, px + 0.14, 0.0, 2.60, -0.69, -0.41, SOOTW, vis=(2,)))
    P.add(W(px - 0.14, px + 0.14, 0.0, 2.60, 0.41, 0.69, SOOTW, vis=(2,)))
    P.add(W(px - 0.16, px + 0.16, 2.05, 2.35, -0.75, 0.75, SOOTW, vis=(2,)))
    P.add(beam(p0, p1, 0.30, 0.32, SOOTW, vis=(2,)))
    # collision (no two components overlapping)
    P.add(col(bx0, bx1, 0.0, bh if state != "slack" else bh - 0.06, -bw / 2, bw / 2, WEATH))
    for sz in (-0.55, 0.55):
        P.add(col(px - 0.14, px + 0.14, 0.10, 2.04, sz - 0.14, sz + 0.14, SOOTW))
    P.add(col(px - 0.16, px + 0.16, 2.05, 2.35, -0.75, 0.75, SOOTW))
    if state == "slack":
        P.add(col(1.20, 1.80, bh - 0.05, bh + 0.52, -0.20, 0.20, WEATH))
        P.add(ocol((px - 0.25, 1.88 - 0.01, 0.0), (-3.30, 1.62, 0.0), 0.30, 0.30))
        P.add(col(-3.42, -2.60, 0.12, 0.66, -0.42, 0.42, RIVER))
    else:
        P.add(ocol((px - 0.25, 1.83, 0.0), (-3.10, 0.17, 0.10), 0.30, 0.30))
    if state == "slack":
        P.loot_rect("lid", bh - 0.06, bx1 - 0.65, bx1 - 0.15, -0.30, 0.30, rng=0.12, per=1.0)
    else:
        P.loot_rect("bags", 0.22, bx0 + 0.40, bx0 + 1.40, -0.25, 0.25, rng=0.12, per=1.0,
                    points=[(bx0 + 0.52, 0.22, 0.0), (bx0 + 1.27, 0.22, 0.0)])
    P.dim("len", 6.4, round(math.dist(p0, p1), 2), tol=0.4)
    P.over_budget_ok = "the lever press is the brewery's hero machine (box, posts, 6.4 m beam, six weight stones)"
    P.notes.append("the lever press (fune + tenbin beam + weight stones)%s" % (
        ", slack" if state == "slack" else ": slings cut, the beam down, the stones rolled about"))
    return P


def koji_toko(ab=False):
    """The koji bed (toko) of the koji room: a broad board table (1.80 x 1.20 x 0.72) with a raised rim, the cloth
    (as left: folded back over a heap of dried koji rice; ab: dragged half off onto the floor), two koji trays."""
    P = LPart("koji_toko", budget="furniture", mass=60.0, anchor="floor")
    w, d, h = 1.80, 1.20, 0.72
    out = [W(-w / 2, w / 2, h - 0.05, h, -d / 2, d / 2, WEATH, vis=(1,))]
    for (a, b, c, e) in ((-w / 2, w / 2, -d / 2, -d / 2 + 0.04), (-w / 2, w / 2, d / 2 - 0.04, d / 2),
                         (-w / 2, -w / 2 + 0.04, -d / 2 + 0.04, d / 2 - 0.04), (w / 2 - 0.04, w / 2, -d / 2 + 0.04,
                                                                               d / 2 - 0.04)):
        out.append(W(a, b, h, h + 0.08, c, e, WEATH, vis=(1,)))
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * (w / 2 - 0.10) - 0.05, sx * (w / 2 - 0.10) + 0.05, 0.0, h - 0.05, sz * (d / 2 - 0.10)
                         - 0.05, sz * (d / 2 - 0.10) + 0.05, WEATH, vis=(1,)))
    out.append(mound("koji", -0.25, 0.0, 0.40, 0.10, "food_rice"))
    out[-1] = xf(out[-1], t=(0.0, h, 0.0))
    if ab:
        out.append(xf(W(-0.70, 0.70, 0.0, 0.01, -0.50, 0.50, KINARI, vis=(1,)), rx=-35.0, t=(0.30, h - 0.30, d / 2 + 0.20)))
        out.append(W(-0.60, 0.40, 0.0, 0.012, d / 2 + 0.35, d / 2 + 0.95, KINARI, vis=(1,)))
        out.append(xf(W(-0.22, 0.22, 0.0, 0.05, -0.15, 0.15, WEATH, vis=(1,)), ry=30.0, rz=8.0, t=(-0.50, 0.0, d / 2 + 0.55)))
    else:
        out.append(W(0.10, 0.85, h + 0.01, h + 0.045, -0.50, 0.50, KINARI, vis=(1,)))
        out.append(W(-0.80, -0.36, h + 0.01, h + 0.06, 0.20, 0.50, WEATH, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.08, -d / 2, d / 2, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.loot_rect("bed", h, -w / 2 + 0.15, w / 2 - 0.15, -d / 2 + 0.15, d / 2 - 0.15, rng=0.15, per=0.9)
    P.dim("w", w, w, tol=0.01)
    P.notes.append("the koji bed (toko) with its cloth%s" % (" dragged half off" if ab else ""))
    return P


def kojibuta_tana(ab=False):
    """Shelves of koji trays (koji-buta, 0.45 x 0.30 x 0.05) along the koji room's wall (mount wall): a 1.80 wide,
    0.48 deep, 1.55 high rack of four shelves, the trays in stacks; ab: half the stacks pulled down, trays on the
    floor in front."""
    P = LPart("kojibuta_tana", budget="furniture", mass=60.0, anchor="wall")
    w, d, h = 1.80, 0.48, 1.55
    ys = (0.15, 0.50, 0.85, 1.20)
    out = []
    for x in (-w / 2, -w / 2 + 0.88, w / 2 - 0.05):
        for z in (0.005, d - 0.05):
            out.append(W(x, x + 0.05, 0.0, h, z, z + 0.04, WEATH, vis=(1,)))
    for y in ys:
        out.append(W(-w / 2, w / 2, y - 0.025, y, 0.005, d - 0.01, WEATH, vis=(1,)))
    r_ = rng("kojibuta" + str(ab))
    for y in ys:
        for x in (-0.62, -0.14, 0.38):
            if ab and r_.random() < 0.5:
                continue
            k = r_.randint(3, 5)
            for j in range(k):
                out.append(W(x - 0.22, x + 0.22, y + 0.05 * j, y + 0.05 * j + 0.045, 0.08, 0.38, WEATH, vis=(1,)))
    if ab:
        for j in range(6):
            out.append(xf(W(-0.22, 0.22, 0.0, 0.045, -0.15, 0.15, WEATH, vis=(1,)), ry=r_.uniform(-40, 40),
                          rz=r_.uniform(-6, 6) if j % 2 else 0.0, t=(r_.uniform(-0.7, 0.7), 0.0, d + r_.uniform(0.25, 0.75))))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h, 0.005, d, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, 0.005, d, WEATH))
    P.loot_rect("shelf", ys[1], 0.64, 0.82, 0.10, d - 0.06, rng=0.08, per=0.9,
                points=[(0.73, ys[1], 0.26), (0.73, ys[2], 0.26)])
    P.dim("w", w, w, tol=0.01)
    P.notes.append("shelves of koji trays%s" % (", half pulled down" if ab else ""))
    return P


def karausu(broken=False):
    """The foot-treadle mortar (kara-usu, fumi-usu): the mortar (a stone-lined wooden usu, rim 0.30 over the floor) at
    the front (+z), the 2.3 m lever on its pivot between two posts, the pestle head under the lever's front end, the
    treader's end at the back, a hand rail on two posts behind. broken: the lever off its pivot on the floor."""
    P = LPart("karausu", budget="furniture", mass=150.0, anchor="floor")
    out = []
    zm = 1.05                                               # mortar centre
    out.append(lathe([(0.0, 0.0), (0.30, 0.0), (0.30, 0.30), (0.20, 0.30), (0.17, 0.10), (0.0, 0.10)], 12,
                     CUTSTONE, vis=(1,)))
    out[-1] = xf(out[-1], t=(0.0, 0.0, zm))
    out.append(disc(0.16, 0.10, 0.14, "food_rice", n=10, vis=(1,), cz=zm))
    zp = -0.10                                              # pivot
    for sx in (-0.17, 0.17):
        out.append(W(sx - 0.05, sx + 0.05, 0.0, 0.62, zp - 0.06, zp + 0.06, WEATH, vis=(1,)))
    out.append(W(-0.24, 0.24, 0.0, 0.08, zp - 0.20, zp + 0.20, WEATH, vis=(1,)))
    if broken:
        lev = [W(-0.07, 0.07, 0.0, 0.13, -1.05, 1.15, WEATH, vis=(1,))]
        lev.append(W(-0.09, 0.09, 0.0, 0.18, 1.15, 1.33, WEATH, vis=(1,)))
        out += [xf(s, ry=14.0, t=(0.30, 0.0, -0.10)) for s in lev]
    else:
        ang = math.radians(4.0)
        p0, p1 = (0.0, 0.52 + 1.20 * math.sin(ang), zm + 0.05), (0.0, 0.52 - 1.15 * math.sin(ang), -1.10)
        out.append(beam(p0, p1, 0.13, 0.14, WEATH, vis=(1,)))
        out.append(W(-0.09, 0.09, 0.36, 0.60, zm - 0.09, zm + 0.09, WEATH, vis=(1,)))       # pestle head
        out.append(W(-0.06, 0.06, 0.31, 0.36, zm - 0.06, zm + 0.06, IRON, vis=(1,)))
        out.append(pole((-0.17, 0.58, zp), (0.17, 0.58, zp), 0.025, IRON, n=5, vis=(1,)))   # pivot pin
    # the hand rail at the back
    for sx in (-0.32, 0.32):
        out.append(W(sx - 0.04, sx + 0.04, 0.0, 1.10, -1.38, -1.30, WEATH, vis=(1,)))
    out.append(pole((-0.36, 1.08, -1.34), (0.36, 1.08, -1.34), 0.025, BAMBOO, n=5, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.30, 0.30, 0.0, 0.30, zm - 0.30, zm + 0.30, CUTSTONE, vis=(2,)))
    P.add(W(-0.36, 0.36, 0.0, 1.10, -1.38, -1.30, WEATH, vis=(2,)))
    P.add(W(-0.24, 0.24, 0.0, 0.62, zp - 0.20, zp + 0.20, WEATH, vis=(2,)))
    P.add(cyl_col(0.30, 0.0, 0.30, n=8, cz=zm, mat=CUTSTONE))
    P.add(col(-0.24, 0.24, 0.0, 0.62, zp - 0.20, zp + 0.20, WEATH))
    P.add(col(-0.36, 0.36, 0.0, 1.10, -1.38, -1.30, WEATH))
    if not broken:
        P.add(W(-0.07, 0.07, 0.40, 0.66, -1.10, zm + 0.10, WEATH, vis=(2,)))
    P.dim("len", 2.4, 2.25 if not broken else 2.38, tol=0.25)
    P.notes.append("foot-treadle rice-polishing mortar (kara-usu)%s" % (", the lever off its pivot" if broken else ""))
    return P


def sugidama(fallen=False):
    """The sugidama (sakabayashi): a ball of cedar sprigs, 0.75 across, hung from the eave by a rope; brown (hung green
    with the new sake in early spring, brown by autumn). Hung: anchor 'hang' (origin = the eave underside). fallen: on
    the ground, its rope coiled (anchor floor)."""
    r_ = rng("sugidama")
    Rb = 0.375
    if fallen:
        P = LPart("sakabayashi", budget="small", mass=6.0, anchor="floor")
        cy, cx = Rb * 0.92, 0.0
    else:
        P = LPart("sakabayashi", budget="small", mass=6.0, anchor="hang", flat=True)
        cy, cx = -0.30 - Rb, 0.0
    out = []
    prof = [(0.0, -Rb)] + [(Rb * math.sin(math.pi * k / 6), -Rb * math.cos(math.pi * k / 6)) for k in range(1, 6)] + \
        [(0.0, Rb)]
    out.append(lathe(prof, 12, CEDAR, vis=(1,)))
    for k in range(28):                                    # shaggy tufts
        a, b = r_.uniform(0, 2 * math.pi), r_.uniform(-1.2, 1.2)
        dvec = (math.cos(b) * math.cos(a), math.sin(b), math.cos(b) * math.sin(a))
        p0 = core.mul(dvec, Rb * 0.85)
        p1 = core.mul(dvec, Rb * 1.10)
        out.append(pole(p0, p1, 0.07, CEDAR, n=4, vis=(1,), r1=0.02))
    out = [xf(s, t=(cx, cy, 0.0)) for s in out]
    if fallen:
        out.append(xf(core_ring_rope(), t=(0.55, 0.0, 0.10)))
    else:
        out.append(cord((0.0, 0.0, 0.0), (0.0, -0.31, 0.0), r=0.012))
        out.append(W(-0.06, 0.06, -0.33, -0.29, -0.06, 0.06, ROPE, vis=(1,)))
    wear_all(out, "_w1")
    adds1(P, out) if fallen else P.adds([dict_vis(s, {1}) for s in out])
    P.add(lathe([(0.0, -Rb), (Rb, 0.0), (0.0, Rb)], 6, CEDAR, vis=(2,)))
    P.solids[-1] = xf(P.solids[-1], t=(cx, cy, 0.0))
    P.solids[-1].vis = {2}
    if fallen:
        P.add(cyl_col(Rb * 0.9, 0.0, 2 * Rb * 0.9, n=8, mat=CEDAR))
    else:
        P.finish_hang()
    P.dim("d", 2 * Rb, 2 * Rb, tol=0.01)
    P.notes.append("the sugidama (cedar ball), brown in autumn%s" % (", fallen to the ground" if fallen else
                                                                    ", hung from the eave"))
    return P


def dict_vis(s, v):
    s.vis = set(v)
    return s


def core_ring_rope():
    from lkit import flat_coil
    return flat_coil(0.0, 0.0, 0.14, 0.012, n=10, m=3)


def hatcho_oke(ab=False):
    """A Hatcho-style miso vat (dressing): a big cedar vat (1.60 across x 1.45) under a plank lid with a cone of river
    stones piled on it (the Okazaki way). ab: the lid knocked askew, half the stones tumbled round the foot."""
    P = LPart("hatcho_oke", budget="detail", mass=3000.0, anchor="floor")
    R, H = 0.80, 1.45
    r_ = rng("hatcho" + str(ab))
    out = [lathe([(0.0, 0.0), (R, 0.0), (R, H), (R - 0.05, H), (R - 0.05, 0.08), (0.0, 0.08)], 18, WEATH, vis=(1,))]
    out += hoops(R, (0.15, 0.50, 0.85, 1.20, 1.38), n=18)
    lid_t = H + 0.04
    if ab:
        out.append(xf(disc(R - 0.06, 0.0, 0.04, WEATH, n=16, vis=(1,)), rz=9.0, t=(0.18, H - 0.06, 0.0)))
        cone = [(0.30, 0.18, 0.00), (-0.15, 0.15, 0.20), (0.10, 0.16, -0.25)]
        for (x, y, z) in cone:
            out.append(stone_lump(r_, x, lid_t + y, z, 0.28))
        for k in range(12):
            a = r_.uniform(0, 2 * math.pi)
            rr = R + r_.uniform(0.15, 0.55)
            out.append(stone_lump(r_, rr * math.cos(a), 0.0, rr * math.sin(a), r_.uniform(0.22, 0.32)))
    else:
        out.append(disc(R - 0.06, H - 0.02, lid_t, WEATH, n=16, vis=(1,)))
        for layer, (rad, k) in enumerate(((0.55, 9), (0.38, 7), (0.20, 4), (0.0, 1))):
            for j in range(k):
                a = 2 * math.pi * j / k + 0.3 * layer
                out.append(stone_lump(r_, rad * math.cos(a), lid_t + 0.22 * layer, rad * math.sin(a), 0.30))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(lathe([(0.0, 0.0), (R, 0.0), (R, H), (0.0, H)], 10, WEATH, vis=(2,)))
    P.add(cyl_col(R, 0.0, H, n=10, mat=WEATH))
    if not ab:
        P.add(lathe([(0.0, H), (0.62, H), (0.0, H + 0.95)], 8, RIVER, vis=(2,)))
        P.add(cyl_col(0.55, H + 0.005, H + 0.45, n=8, mat=RIVER))
        P.add(cyl_col(0.25, H + 0.455, H + 0.90, n=8, mat=RIVER))
    P.dim("d", 2 * R, 2 * R, tol=0.01)
    P.over_budget_ok = "the stone cone (some 21 river stones) is the Hatcho vat's whole character"
    P.notes.append("Hatcho-style miso vat with its stone cone%s" % (", stones tumbled" if ab else ""))
    return P


def hashigo():
    """A plain ladder (hashigo) leaning on the wall (mount wall): two rails 2.70 m, eight rungs; static dressing (no
    climb action: the kura loft is reached by its stair)."""
    P = LPart("hashigo", budget="small", mass=12.0, anchor="wall")
    out = []
    top_z, foot_z, top_y = 0.034, 0.75, 2.62
    for sx in (-0.22, 0.22):
        out.append(pole((sx, 0.0, foot_z), (sx, top_y, top_z), 0.03, WEATH, n=5, vis=(1,)))
    for k in range(1, 9):
        f = k / 9.0
        out.append(pole((-0.22, f * top_y, foot_z - f * (foot_z - top_z)), (0.22, f * top_y, foot_z - f * (foot_z - top_z)),
                        0.018, WEATH, n=4, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(beam((0.0, 0.0, foot_z), (0.0, top_y, top_z), 0.50, 0.05, WEATH, vis=(2,)))
    P.add(ocol((0.0, 0.03, foot_z - 0.03), (0.0, top_y, top_z), 0.50, 0.04))
    P.dim("h", top_y, top_y, tol=0.05)
    P.notes.append("a plain leaning ladder (static)")
    return P


# ================================================================================================ dyer
def sukumo_bales(scattered=False):
    """Sukumo (fermented indigo leaf) in straw-wrapped bales (0.60 across x 0.80), three below and two on top; one
    split open showing the dark indigo mass. scattered: tumbled, one burst on the floor."""
    P = LPart("sukumo_bales", budget="furniture", mass=300.0, anchor="floor")
    r_ = rng("sukumo" + str(scattered))
    out = []

    def bale(cx, cy, cz, ry=0.0, rz=0.0, split=False):
        prof = [(0.0, -0.40), (0.22, -0.40), (0.30, -0.30), (0.30, 0.30), (0.22, 0.40), (0.0, 0.40)]
        ss = [xf(lathe(prof, 10, STRAW, vis=(1,)), rz=90.0)]
        for x in (-0.26, 0.0, 0.26):
            ss.append(xf(lathe([(0.305, x - 0.02), (0.305, x + 0.02)], 10, ROPE, vis=(1,), closed_ends=False), rz=90.0))
        if split:
            ss.append(W(-0.30, 0.30, 0.18, 0.31, -0.14, 0.14, INDIGO, vis=(1,)))
        return [xf(s, ry=ry, rz=rz, t=(cx, cy, cz)) for s in ss]
    if scattered:
        out += bale(-0.35, 0.30, -0.10, ry=10.0)
        out += bale(0.40, 0.30, 0.25, ry=70.0)
        out += bale(-0.10, 0.30, 0.75, ry=-35.0, split=True)
        out.append(mound("suk", 0.45, 0.90, 0.40, 0.10, INDIGO))
        P.add(W(-0.85, 0.95, 0.0, 0.60, -0.45, 1.20, STRAW, vis=(2,)))
        P.add(col(-0.75, 0.05, 0.0, 0.60, -0.40, 0.20, STRAW))
        P.add(col(0.12, 0.70, 0.0, 0.60, -0.15, 0.20, STRAW))
        P.loot_rect("top", 0.60, -0.70, 0.0, -0.30, 0.10, rng=0.12, per=1.0)
    else:
        for k, x in enumerate((-0.62, 0.0, 0.62)):
            out += bale(x, 0.30, 0.0, ry=r_.uniform(-3, 3))
        out += bale(-0.31, 0.88, 0.0, ry=2.0, split=True)
        out += bale(0.31, 0.88, 0.0, ry=-3.0)
        P.add(W(-1.02, 1.02, 0.0, 0.60, -0.30, 0.30, STRAW, vis=(2,)))
        P.add(W(-0.71, 0.71, 0.60, 1.18, -0.30, 0.30, STRAW, vis=(2,)))
        P.add(col(-1.02, 1.02, 0.0, 0.58, -0.30, 0.30, STRAW))
        P.add(col(-0.71, 0.71, 0.585, 1.18, -0.30, 0.30, STRAW))
        P.loot_rect("top", 0.88 + 0.30 * math.cos(math.pi / 10) - 0.007, -0.50, 0.50, -0.05, 0.05, rng=0.10, per=1.0)
    wear_all(out, "_w2")
    adds1(P, out)
    P.dim("bale_d", 0.60, 0.60, tol=0.02)
    P.notes.append("sukumo indigo in straw bales%s" % (", tumbled, one burst" if scattered else ""))
    return P


def akumizu(ab=False):
    """The lye drip tubs (akumizu): a tub of wood ash on a four-legged stand (top 0.70) dripping through a bamboo spout
    into a tub on the floor; beside them a tub of lime and a sack of bran. ab: the ash tub knocked off its stand,
    ash spilled."""
    P = LPart("akumizu", budget="furniture", mass=60.0, anchor="floor")
    out = []
    for sx in (-0.30, 0.30):
        for sz in (-0.30, 0.30):
            out.append(W(sx - 0.03, sx + 0.03, 0.0, 0.70, sz - 0.03, sz + 0.03, WEATH, vis=(1,)))
    out.append(W(-0.34, 0.34, 0.66, 0.70, -0.34, -0.26, WEATH, vis=(1,)))
    out.append(W(-0.34, 0.34, 0.66, 0.70, 0.26, 0.34, WEATH, vis=(1,)))
    lower = [tub_shell(0.28, 0.30, 0.02, WEATH, n=12)] + hoops(0.28, (0.08, 0.22), n=12)
    out += lower
    out.append(disc(0.255, 0.18, 0.19, "lacquer_black", n=10, vis=(1,)))
    if ab:
        top = [tub_shell(0.36, 0.40, 0.025, WEATH, n=12)] + hoops(0.36, (0.10, 0.30), n=12)
        out += [xf(s, rx=85.0, t=(0.75, 0.36, 0.10)) for s in top]
        out.append(mound("akab", 0.55, 0.55, 0.40, 0.08, "ground_ash"))
    else:
        top = [tub_shell(0.36, 0.40, 0.025, WEATH, n=12)] + hoops(0.36, (0.10, 0.30), n=12)
        top.append(disc(0.335, 0.30, 0.32, "ground_ash", n=10, vis=(1,)))
        out += [xf(s, t=(0.0, 0.70, 0.0)) for s in top]
        out.append(pole((0.0, 0.72, 0.0), (0.0, 0.42, 0.10), 0.015, BAMBOO, n=4, vis=(1,)))
    lime = [tub_shell(0.22, 0.32, 0.02, WEATH, n=10), disc(0.20, 0.24, 0.25, "wall_shikkui", n=10, vis=(1,))]
    out += [xf(s, t=(-0.75, 0.0, 0.15)) for s in lime]
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.40, 0.40, 0.0, 1.10 if not ab else 0.70, -0.40, 0.40, WEATH, vis=(2,)))
    P.add(W(-0.97, -0.53, 0.0, 0.32, -0.07, 0.37, WEATH, vis=(2,)))
    P.add(col(-0.36, 0.36, 0.0, 0.70, -0.36, 0.36, WEATH))
    if not ab:
        P.add(cyl_col(0.36, 0.705, 1.10, n=8, mat=WEATH))
    P.add(cyl_col(0.22, 0.0, 0.32, n=8, cx=-0.75, cz=0.15, mat=WEATH))
    P.loot_rect("stand", 0.70, -0.30, 0.30, -0.33, -0.27, rng=0.08, per=1.0) if ab else None
    P.dim("h", 0.70, 0.70, tol=0.01)
    P.notes.append("lye drip tubs (akumizu) with the lime tub%s" % (", the ash tub knocked off" if ab else ""))
    return P


def monohoshi(torn=False):
    """The tall drying frame of a dyer's yard (monohoshi): two posts 5.6 m high, 4.0 m apart, two cross bars, long
    lengths of indigo cloth hung doubled over the top bar (nearly to the ground). torn: two lengths fallen, two torn
    short, one still hanging."""
    P = LPart("monohoshi", budget="detail", mass=200.0, anchor="floor")
    r_ = rng("monohoshi" + str(torn))
    Hh, L = 5.60, 4.00
    out = []
    for sx in (-L / 2, L / 2):
        out.append(pole((sx, 0.0, 0.0), (sx, Hh, 0.0), 0.07, WEATH, n=6, vis=(1,)))
        for sz in (-1, 1):                                 # raking struts
            out.append(pole((sx, 0.0, sz * 1.20), (sx, 2.40, sz * 0.05), 0.04, WEATH, n=5, vis=(1,)))
    out.append(pole((-L / 2 - 0.20, Hh - 0.15, 0.0), (L / 2 + 0.20, Hh - 0.15, 0.0), 0.045, BAMBOO, n=6, vis=(1,)))
    out.append(pole((-L / 2, Hh - 1.10, 0.0), (L / 2, Hh - 1.10, 0.0), 0.04, BAMBOO, n=6, vis=(1,)))
    yb = Hh - 0.15
    cloths = (-1.45, -0.75, 0.0, 0.70, 1.40)
    for k, x in enumerate(cloths):
        mat = INDIGO if k % 2 == 0 else KINARI
        drop = 4.80
        state = "hang"
        if torn and k in (1, 3):
            state = "fallen"
        elif torn and k in (0, 4):
            drop = r_.uniform(1.4, 2.2)
        if state == "fallen":
            out.append(W(x - 0.18, x + 0.18, 0.0, 0.012, -0.30, 3.20, mat, vis=(1,)))
            out.append(xf(W(x - 0.18, x + 0.18, 0.0, 0.012, 0.0, 1.0, mat, vis=(1,)), rx=-55.0, t=(0.0, 0.0, -0.30)))
            continue
        for sz in (-1, 1):
            sw = r_.uniform(-0.04, 0.04)
            out.append(W(x - 0.18, x + 0.18, yb - drop, yb, sz * 0.050 + sw - 0.002, sz * 0.050 + sw + 0.002, mat,
                         vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    for sx in (-L / 2, L / 2):
        P.add(W(sx - 0.07, sx + 0.07, 0.0, Hh, -0.07, 0.07, WEATH, vis=(2,)))
    P.add(W(-L / 2 - 0.20, L / 2 + 0.20, Hh - 0.20, Hh - 0.10, -0.05, 0.05, BAMBOO, vis=(2,)))
    P.add(W(-1.65, 1.60, 0.80 if not torn else 3.0, Hh - 0.20, -0.06, 0.06, INDIGO, vis=(2,)))
    for sx in (-L / 2, L / 2):
        P.add(col(sx - 0.07, sx + 0.07, 0.0, Hh, -0.07, 0.07, WEATH))
    P.dim("h", Hh, Hh, tol=0.05)
    P.notes.append("tall cloth-drying frame with long indigo lengths%s" % (", two fallen, two torn" if torn else ""))
    return P


def shibori_front(torn=False):
    """Shop-front cloths (the Arimatsu tie-dye shop flavour): a bamboo pole hung under the front beam (anchor 'hang',
    origin = the beam underside) on two cords, five lengths of dyed cloth hanging 1.0 m (indigo and undyed; plain:
    there is no shibori pattern texture). torn: two lengths gone, one torn and half down."""
    P = LPart("shibori_front", budget="small", mass=3.0, anchor="hang", flat=True)
    out = []
    Lp = 2.40
    out.append(cord((-1.05, 0.0, 0.0), (-1.05, -0.18, 0.0), r=0.008))
    out.append(cord((1.05, 0.0, 0.0), (1.05, -0.18, 0.0), r=0.008))
    out.append(pole((-Lp / 2, -0.20, 0.0), (Lp / 2, -0.20, 0.0), 0.02, BAMBOO, n=5, vis=(1,)))
    for k, x in enumerate((-0.94, -0.47, 0.0, 0.47, 0.94)):
        if torn and k in (1, 4):
            continue
        drop = 0.55 if (torn and k == 2) else 1.00
        out.append(W(x - 0.18, x + 0.18, -0.20 - drop, -0.18, -0.025, -0.021, INDIGO if k % 2 == 0 else KINARI,
                     vis=(1,)))
        out.append(W(x - 0.18, x + 0.18, -0.20 - drop * 0.96, -0.18, 0.021, 0.025, INDIGO if k % 2 == 0 else KINARI,
                     vis=(1,)))
    wear_all(out, "_w1")
    P.adds([dict_vis(s, {1}) for s in out])
    P.add(W(-Lp / 2, Lp / 2, -1.20, -0.18, -0.03, 0.03, INDIGO, vis=(2,)))
    P.finish_hang()
    P.dim("w", Lp, Lp, tol=0.05)
    P.notes.append("shop-front cloths on a bamboo pole%s" % (", torn and half gone" if torn else ""))
    return P


def dye_rack():
    """A rack by the vat-room wall (mount wall): stirring poles and a cloth-wringing bar with a dripping length of
    indigo over it."""
    P = LPart("dye_rack", budget="small", mass=15.0, anchor="wall")
    out = []
    for sx in (-0.55, 0.55):
        out.append(W(sx - 0.03, sx + 0.03, 0.0, 1.60, 0.0, 0.06, WEATH, vis=(1,)))
    out.append(pole((-0.62, 1.45, 0.20), (0.62, 1.45, 0.20), 0.025, WEATH, n=5, vis=(1,)))
    out.append(W(-0.50, 0.10, 0.55, 1.47, 0.18, 0.185, INDIGO, vis=(1,)))
    out.append(W(-0.50, 0.10, 0.70, 1.47, 0.215, 0.22, INDIGO, vis=(1,)))
    for k, x in enumerate((0.25, 0.38, 0.50)):
        out.append(pole((x, 0.0, 0.38), (x - 0.02, 1.90, 0.08), 0.016, BAMBOO, n=4, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.62, 0.62, 0.0, 1.90, 0.0, 0.40, WEATH, vis=(2,)))
    P.add(col(-0.62, 0.62, 0.0, 1.60, 0.0, 0.38, WEATH))
    P.dim("h", 1.60, 1.60, tol=0.01)
    P.notes.append("stirring poles and a dripping length of indigo on the wringing bar")
    return P


# ================================================================================================ paper mill
def sukibune(ab=False):
    """The paper vat (suki-bune): a board trough 1.80 x 0.90 x 0.62 on sleepers with a dried white skin of pulp, the
    mould (sugeta 0.75 x 0.55, its bamboo screen) resting across it on two bars, hung by cords from a bamboo spring
    pole arching over from a post at the back end; a stirring rod. ab: the mould fallen into the vat on edge, the pole
    snapped and hanging."""
    P = LPart("sukibune", budget="furniture", mass=120.0, anchor="floor")
    w, d, h = 1.80, 0.90, 0.62
    out = [W(-w / 2 + 0.10, -w / 2 + 0.25, 0.0, 0.06, -d / 2, d / 2, WEATH, vis=(1,)),
           W(w / 2 - 0.25, w / 2 - 0.10, 0.0, 0.06, -d / 2, d / 2, WEATH, vis=(1,)),
           W(-w / 2, w / 2, 0.06, 0.11, -d / 2, d / 2, WEATH, vis=(1,))]
    for (a, b, c, e) in ((-w / 2, w / 2, -d / 2, -d / 2 + 0.05), (-w / 2, w / 2, d / 2 - 0.05, d / 2),
                         (-w / 2, -w / 2 + 0.05, -d / 2 + 0.05, d / 2 - 0.05), (w / 2 - 0.05, w / 2, -d / 2 + 0.05,
                                                                               d / 2 - 0.05)):
        out.append(W(a, b, 0.11, h, c, e, WEATH, vis=(1,)))
    out.append(W(-w / 2 + 0.05, w / 2 - 0.05, 0.11, 0.16, -d / 2 + 0.05, d / 2 - 0.05, PAPER, vis=(1,)))
    # the spring pole: a post at the -x end, the bamboo arching over the vat
    out.append(W(-w / 2 - 0.16, -w / 2 - 0.04, 0.0, 1.80, -0.06, 0.06, WEATH, vis=(1,)))
    if ab:
        out.append(pole((-w / 2 - 0.10, 1.75, 0.0), (-0.10, 2.05, 0.0), 0.025, BAMBOO, n=5, vis=(1,)))
        out.append(pole((-0.10, 2.05, 0.0), (0.20, 1.15, 0.05), 0.022, BAMBOO, n=5, vis=(1,)))
        fr = [W(-0.375, 0.375, 0.0, 0.03, -0.275, 0.275, WEATH, vis=(1,)),
              W(-0.34, 0.34, 0.03, 0.035, -0.24, 0.24, "bamboo_weave", vis=(1,))]
        out += [xf(s, rx=70.0, t=(0.20, 0.17, 0.05)) for s in fr]
    else:
        out.append(pole((-w / 2 - 0.10, 1.75, 0.0), (0.0, 2.15, 0.0), 0.025, BAMBOO, n=5, vis=(1,)))
        out.append(pole((0.0, 2.15, 0.0), (0.55, 2.05, 0.0), 0.02, BAMBOO, n=5, vis=(1,)))
        for x in (-0.40, 0.40):
            out.append(W(x - 0.03, x + 0.03, h, h + 0.04, -d / 2, d / 2, WEATH, vis=(1,)))
        out.append(W(-0.375, 0.375, h + 0.04, h + 0.07, -0.275, 0.275, WEATH, vis=(1,)))
        out.append(W(-0.34, 0.34, h + 0.07, h + 0.075, -0.24, 0.24, "bamboo_weave", vis=(1,)))
        for x in (-0.30, 0.30):
            out.append(cord((x, h + 0.08, 0.0), (x * 0.4 + 0.10, 2.10, 0.0), r=0.006))
    out.append(pole((0.55, h, -0.30), (1.10, 0.0, -0.35), 0.015, WEATH, n=4, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH, vis=(2,)))
    P.add(W(-w / 2 - 0.16, -w / 2 - 0.04, 0.0, 1.80, -0.06, 0.06, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.add(col(-w / 2 - 0.16, -w / 2 - 0.04, 0.0, 1.80, -0.06, 0.06, WEATH))
    P.dim("w", w, w, tol=0.01)
    P.notes.append("the paper vat with the mould and its spring pole%s" % (
        "; the mould fallen in, the pole snapped" if ab else ""))
    return P


def kozo_beat(scattered=False):
    """The beating place: a heavy board (1.20 x 0.60 x 0.22) on the floor with a heap of soaked kozo fibre, two wooden
    mallets, bundles of stripped bark. scattered: mallets and bundles strewn, fibre spilled."""
    P = LPart("kozo_beat", budget="furniture", mass=80.0, anchor="floor")
    r_ = rng("kozo" + str(scattered))
    out = [W(-0.60, 0.60, 0.0, 0.22, -0.30, 0.30, SOOTW, vis=(1,))]
    out.append(mound("kozo", 0.05, 0.0, 0.30, 0.08, PAPER))
    out[-1] = xf(out[-1], t=(0.0, 0.22, 0.0))
    for k in range(2):
        a = (25.0 if k else -40.0) + (r_.uniform(-60, 60) if scattered else 0.0)
        m = [pole((0.0, 0.03, 0.0), (0.55, 0.03, 0.0), 0.018, WEATH, n=5, vis=(1,)),
             W(0.50, 0.68, 0.0, 0.07, -0.05, 0.05, WEATH, vis=(1,))]
        base = (0.10 + 0.5 * k, 0.22, -0.10) if not scattered else (0.70 * (k * 2 - 1), 0.0, 0.50)
        out += [xf(s, ry=a, t=base) for s in m]
    for k in range(3):
        cx, cz = (-0.90 + 0.18 * k, 0.15 * k - 0.10) if not scattered else (r_.uniform(-1.0, 1.0), r_.uniform(0.4, 0.8))
        for j in range(5):
            out.append(pole((cx - 0.40, 0.04 + 0.02 * (j % 2), cz + 0.025 * j), (cx + 0.40, 0.04 + 0.02 * (j % 2),
                                                                                cz + 0.025 * j), 0.012, WEATH, n=4,
                            vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.60, 0.60, 0.0, 0.25, -0.30, 0.30, SOOTW, vis=(2,)))
    P.add(col(-0.60, 0.60, 0.0, 0.22, -0.30, 0.30, SOOTW))
    P.loot_rect("board", 0.22, 0.30, 0.55, -0.25, 0.25, rng=0.12, per=1.0)
    P.dim("w", 1.20, 1.20, tol=0.01)
    P.notes.append("the bark-beating board with mallets and bark bundles%s" % (", strewn" if scattered else ""))
    return P


def shime_press(ab=False):
    """The couching press: the stack of wet sheets (shitoku, 0.75 x 0.55) on a board base, a lid board and a block, a
    2.2 m lever from a slot in a post at the back over the stack, three stones on the lever's free end. ab: the lever
    down on the floor, the stones rolled off, the stack crumbled."""
    P = LPart("shime_press", budget="furniture", mass=200.0, anchor="floor")
    r_ = rng("shime" + str(ab))
    out = [W(-0.42, 0.42, 0.0, 0.18, -0.32, 0.32, WEATH, vis=(1,))]
    out.append(W(-0.375, 0.375, 0.18, 0.42 if not ab else 0.30, -0.275, 0.275, PAPER, vis=(1,)))
    out.append(W(-0.70, -0.58, 0.0, 1.30, -0.08, 0.08, WEATH, vis=(1,)))
    if ab:
        out.append(beam((-0.60, 0.07, 0.0), (1.50, 0.07, 0.20), 0.10, 0.12, WEATH, vis=(1,)))
        for k in range(3):
            out.append(stone_lump(r_, 1.10 + 0.35 * k, 0.0, 0.55 + 0.1 * k, 0.26))
    else:
        out.append(W(-0.35, 0.35, 0.42, 0.46, -0.25, 0.25, WEATH, vis=(1,)))
        out.append(W(-0.12, 0.12, 0.46, 0.62, -0.12, 0.12, WEATH, vis=(1,)))
        out.append(beam((-0.64, 0.72, 0.0), (1.50, 0.66, 0.0), 0.10, 0.12, WEATH, vis=(1,)))
        for k in range(3):
            out.append(stone_lump(r_, 1.10 + 0.17 * k, 0.72, 0.0, 0.24))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.42, 0.42, 0.0, 0.46, -0.32, 0.32, WEATH, vis=(2,)))
    P.add(W(-0.70, -0.58, 0.0, 1.30, -0.08, 0.08, WEATH, vis=(2,)))
    P.add(col(-0.42, 0.42, 0.0, 0.42 if not ab else 0.30, -0.32, 0.32, WEATH))
    P.add(col(-0.70, -0.58, 0.0, 1.30, -0.08, 0.08, WEATH))
    P.dim("w", 0.84, 0.84, tol=0.01)
    P.notes.append("the couching stack under its lever press%s" % (", the lever down" if ab else ""))
    return P


def hoshiita_rack(fallen=False):
    """Drying boards (hoshi-ita, 1.80 x 0.45 planks) leaned against a bar on two posts (1.50 high), their faces to the
    sun (+z), three with paper sheets brushed on. fallen: the bar down, the boards lying flat and askew."""
    P = LPart("hoshiita_rack", budget="furniture", mass=60.0, anchor="floor")
    r_ = rng("hoshi" + str(fallen))
    out = []
    xs = (-1.25, -0.75, -0.25, 0.25, 0.75, 1.25)
    if fallen:
        for sx in (-1.55, 1.55):
            out.append(W(sx - 0.04, sx + 0.04, 0.0, 1.50, -0.44, -0.36, WEATH, vis=(1,)))
        out.append(xf(pole((-1.55, 0.04, 0.0), (1.55, 0.04, 0.0), 0.03, BAMBOO, n=5, vis=(1,)), ry=8.0))
        for k, x in enumerate(xs):
            b = [W(-0.225, 0.225, 0.0, 0.03, -0.90, 0.90, WEATH, vis=(1,))]
            if k % 2 == 0:
                b.append(W(-0.20, 0.20, 0.03, 0.033, -0.60, 0.20, PAPER, vis=(1,)))
            out += [xf(s, ry=r_.uniform(-20, 20) + 90.0 * (k % 2), t=(x * 1.1, 0.0 + 0.03 * (k % 3), 0.55 + 0.25 * (k % 2)))
                    for s in b]
    else:
        for sx in (-1.55, 1.55):
            out.append(W(sx - 0.04, sx + 0.04, 0.0, 1.50, -0.44, -0.36, WEATH, vis=(1,)))
        out.append(pole((-1.60, 1.47, -0.40), (1.60, 1.47, -0.40), 0.03, BAMBOO, n=5, vis=(1,)))
        for k, x in enumerate(xs):
            b = [W(-0.225, 0.225, 0.0, 1.80, -0.015, 0.015, WEATH, vis=(1,))]
            if k % 2 == 0:
                b.append(W(-0.20, 0.20, 0.55, 1.45, 0.015, 0.018, PAPER, vis=(1,)))
            out += [xf(s, rx=-15.0, t=(x, 0.0, 0.05)) for s in b]
    wear_all(out, "_w2")
    adds1(P, out)
    if fallen:
        P.add(W(-1.55, 1.55, 0.0, 0.10, -0.40, 1.35, WEATH, vis=(2,)))
    else:
        P.add(xf(W(-1.50, 1.50, 0.0, 1.80, -0.015, 0.015, WEATH, vis=(2,)), rx=-15.0, t=(0.0, 0.0, 0.05)))
    for sx in (-1.55, 1.55):
        P.add(W(sx - 0.04, sx + 0.04, 0.0, 1.50, -0.44, -0.36, WEATH, vis=(2,)))
        P.add(col(sx - 0.04, sx + 0.04, 0.0, 1.50, -0.44, -0.36, WEATH))
    if not fallen:
        from jpparts.shapes import oriented_box as _ob
        a = math.radians(15.0)
        P.add(_ob((0.0, 0.90 * math.cos(a), 0.05 - 0.90 * math.sin(a)), (1.0, 0.0, 0.0),
                  (0.0, math.cos(a), -math.sin(a)), (0.0, math.sin(a), math.cos(a)), 1.48, 0.88, 0.02, WEATH, vis=(),
                  geo=True, view=True, fire=True))
    P.dim("board_l", 1.80, 1.80, tol=0.01)
    P.notes.append("drying boards leaned to the sun%s" % (", fallen flat" if fallen else ", sheets brushed on three"))
    return P


def kozo_kama(ab=False):
    """The bark steamer: a small clay hearth (0.95 x 0.95 x 0.55) with an iron cauldron and a wooden steaming tub
    (koshiki, 0.80 across x 0.90) on it, fire mouth to the front. ab: the tub knocked off beside it."""
    P = LPart("kozo_kama", budget="furniture", mass=300.0, anchor="floor")
    w, h = 0.95, 0.55
    out = [W(-w / 2, w / 2, 0.0, h, -w / 2, w / 2, CLAY, vis=(1,))]
    out.append(W(-0.18, 0.18, 0.04, 0.34, w / 2, w / 2 + 0.02, IRON, vis=(1,)))
    out.append(W(-0.14, 0.14, 0.07, 0.31, w / 2 + 0.02, w / 2 + 0.021, "ground_ash", vis=(1,)))
    out.append(lathe([(0.42, h - 0.01), (0.44, h + 0.05), (0.36, h + 0.05), (0.34, h - 0.01)], 12, IRON, vis=(1,),
                     closed_ends=False))
    tub = [lathe([(0.0, 0.0), (0.40, 0.0), (0.38, 0.90), (0.34, 0.90), (0.36, 0.05), (0.0, 0.05)], 12, WEATH,
                 vis=(1,))] + hoops(0.39, (0.15, 0.70), n=12)
    if ab:
        out += [xf(s, rx=90.0, ry=30.0, t=(0.70, 0.40, 0.55)) for s in tub]
        out.append(disc(0.34, h - 0.02, h, "ground_ash", n=10, vis=(1,)))
    else:
        out += [xf(s, t=(0.0, h + 0.05, 0.0)) for s in tub]
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-w / 2, w / 2, 0.0, h, -w / 2, w / 2, CLAY, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -w / 2, w / 2, CLAY))
    if not ab:
        P.add(lathe([(0.0, h), (0.40, h), (0.38, h + 0.95), (0.0, h + 0.95)], 8, WEATH, vis=(2,)))
        P.add(cyl_col(0.40, h + 0.005, h + 0.95, n=8, mat=WEATH))
    else:
        P.add(W(0.25, 1.20, 0.0, 0.80, 0.10, 1.05, WEATH, vis=(2,)))
        P.add(col(0.48, 1.15, 0.0, 0.78, 0.20, 1.00, WEATH))
    P.dim("w", w, w, tol=0.01)
    P.notes.append("the bark steamer (koshiki on a cauldron over a small hearth), cold%s" % (
        "; the tub knocked off" if ab else ""))
    return P


PROPS = [
    {"id": "jp_f_shikomi_oke", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_shikomi_oke", "std", "dry", "Big fermentation tub (shikomi-oke), dry, lid half on",
          lambda: shikomi_oke()),
        M("jp_f_shikomi_oke_ladder", "std", "ladder", "Big fermentation tub with a ladder leaning on it",
          lambda: shikomi_oke("ladder")),
        M("jp_f_shikomi_oke_staved", "std", "broken", "Big fermentation tub, staves fallen out",
          lambda: shikomi_oke("staved"))]},
    {"id": "jp_f_hangiri", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_hangiri", "std", "stacked", "Shallow starter tubs (hangiri), stacked", lambda: hangiri()),
        M("jp_f_hangiri_scattered", "std", "scattered", "Shallow starter tubs, knocked about",
          lambda: hangiri(True))]},
    {"id": "jp_f_kai_poles", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_kai_poles", "std", "intact", "Stirring poles (kai) leaning on the wall", kai_poles)]},
    {"id": "jp_f_kamaba", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kamaba", "std", "cold", "Brewery steaming hearth (kamado, cauldron, koshiki), cold",
          lambda: kamaba()),
        M("jp_f_kamaba_toppled", "std", "ransacked", "Brewery steaming hearth, the koshiki knocked off",
          lambda: kamaba("toppled"))]},
    {"id": "jp_f_fune_press", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_fune_press", "std", "slack", "Sake lever press (fune + beam + stones), slack", lambda: fune_press()),
        M("jp_f_fune_press_down", "std", "broken", "Sake lever press, the beam down, stones rolled",
          lambda: fune_press("down"))]},
    {"id": "jp_f_koji_toko", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_koji_toko", "std", "intact", "Koji bed (toko) with its cloth", lambda: koji_toko()),
        M("jp_f_koji_toko_ab", "std", "ransacked", "Koji bed, the cloth dragged off", lambda: koji_toko(True))]},
    {"id": "jp_f_kojibuta_tana", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_kojibuta_tana", "std", "intact", "Shelves of koji trays", lambda: kojibuta_tana()),
        M("jp_f_kojibuta_tana_ab", "std", "ransacked", "Shelves of koji trays, half pulled down",
          lambda: kojibuta_tana(True))]},
    {"id": "jp_f_karausu", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_karausu", "std", "intact", "Foot-treadle rice mortar (kara-usu)", lambda: karausu()),
        M("jp_f_karausu_broken", "std", "broken", "Foot-treadle rice mortar, lever off its pivot",
          lambda: karausu(True))]},
    {"id": "jp_f_sakabayashi", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_sakabayashi", "std", "brown", "Brewery sugidama (big cedar ball, 0.75), brown, hung from the eave",
          lambda: sugidama())]},
    {"id": "jp_f_sakabayashi_fallen", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_sakabayashi_fallen", "std", "fallen", "Brewery sugidama, fallen to the ground",
          lambda: sugidama(True))]},
    {"id": "jp_f_hatcho_oke", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_hatcho_oke", "std", "intact", "Hatcho-style miso vat with its stone cone", lambda: hatcho_oke()),
        M("jp_f_hatcho_oke_ab", "std", "ransacked", "Miso vat, the stones tumbled", lambda: hatcho_oke(True))]},
    {"id": "jp_f_hashigo", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_hashigo", "std", "intact", "Plain ladder leaning on the wall", hashigo)]},
    {"id": "jp_f_sukumo_bales", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_sukumo_bales", "std", "intact", "Sukumo indigo in straw bales", lambda: sukumo_bales()),
        M("jp_f_sukumo_bales_scattered", "std", "scattered", "Sukumo bales, one burst", lambda: sukumo_bales(True))]},
    {"id": "jp_f_akumizu", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_akumizu", "std", "intact", "Lye drip tubs (akumizu) and the lime tub", lambda: akumizu()),
        M("jp_f_akumizu_ab", "std", "ransacked", "Lye drip tubs, the ash tub knocked off", lambda: akumizu(True))]},
    {"id": "jp_f_monohoshi", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_monohoshi", "std", "intact", "Tall cloth-drying frame with indigo lengths", lambda: monohoshi()),
        M("jp_f_monohoshi_torn", "std", "torn", "Cloth-drying frame, cloths fallen and torn", lambda: monohoshi(True))]},
    {"id": "jp_f_shibori_front", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_shibori_front", "std", "intact", "Shop-front dyed cloths on a pole", lambda: shibori_front()),
        M("jp_f_shibori_front_torn", "std", "torn", "Shop-front cloths, torn and half gone",
          lambda: shibori_front(True))]},
    {"id": "jp_f_dye_rack", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_dye_rack", "std", "intact", "Dyer's pole rack with a dripping length", dye_rack)]},
    {"id": "jp_f_sukibune", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_sukibune", "std", "intact", "Paper vat with the mould and spring pole", lambda: sukibune()),
        M("jp_f_sukibune_ab", "std", "broken", "Paper vat, the mould fallen in, the pole snapped",
          lambda: sukibune(True))]},
    {"id": "jp_f_kozo_beat", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kozo_beat", "std", "intact", "Bark-beating board with mallets", lambda: kozo_beat()),
        M("jp_f_kozo_beat_scattered", "std", "scattered", "Bark-beating board, mallets strewn",
          lambda: kozo_beat(True))]},
    {"id": "jp_f_shime_press", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_shime_press", "std", "intact", "Couching stack under its lever press", lambda: shime_press()),
        M("jp_f_shime_press_ab", "std", "broken", "Couching press, the lever down", lambda: shime_press(True))]},
    {"id": "jp_f_hoshiita_rack", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_hoshiita_rack", "std", "intact", "Paper drying boards leaned to the sun", lambda: hoshiita_rack()),
        M("jp_f_hoshiita_rack_fallen", "std", "fallen", "Paper drying boards, fallen flat",
          lambda: hoshiita_rack(True))]},
    {"id": "jp_f_kozo_kama", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kozo_kama", "std", "cold", "Bark steamer on its small hearth, cold", lambda: kozo_kama()),
        M("jp_f_kozo_kama_ab", "std", "ransacked", "Bark steamer, the tub knocked off", lambda: kozo_kama(True))]},
]
