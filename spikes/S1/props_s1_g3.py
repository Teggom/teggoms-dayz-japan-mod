"""S1 group 3 (research/interior/SHOP_SETS.md 2a-2b, trades 11-15): rice dealer, fishmonger and greengrocer, tofu,
soba and rice eatery, sweets and rice cakes."""
import math
import random

from s1kit import (box, lathe, xf, xfs, W, col, board, pole, cord, rest, lod_box, wear_all, stain, mound, bipyramid,
                   ball, bowl, tray, skewer, kanban_prop, finish_goods, cyl_col, SP, M, SHOP, SUMI, WOOD, WEATH, IRON,
                   DARK, PALE, LACQ, BAMBOO, WEAVE, STACK, ROPE, PAPER, KINARI, RED, LITTER, LEAF, ASH, RICE, KAKI,
                   SHU, TOFU, FOLIAGE, FISH)
import fkit
from props_s1_g1 import two, ERA_BTI

G = "shopgoods"
F = "shopfit"
WATER = "lacquer_black"          # still water: B3b's wells use the black lacquer as the dark water surface


def tub(r, h, wear=None, n=10, inner=0.012):
    """An open stave tub (outside, rim, inside, bottom) with two bamboo hoops."""
    prof = [(0.0, 0.0), (r * 0.94, 0.0), (r, h), (r - inner, h), (r * 0.94 - inner, 0.015), (0.0, 0.015)]
    out = [lathe(prof, n, WEATH, vis=(1, 2), wear=wear)]
    for y in (h * 0.25, h * 0.75):
        rr = r * 0.94 + (r - r * 0.94) * y / h
        out.append(lathe([(rr + 0.004, y - 0.012), (rr + 0.006, y + 0.012), (rr, y + 0.012), (rr - 0.002, y - 0.012),
                          (rr + 0.004, y - 0.012)], n, BAMBOO, vis=(1,), wear=wear))
    return out


# ================================================================================================ rice
def rice_bin(state="intact"):
    """Rice bin (kome-bitsu) 0.75 x 0.50 x 0.60: a lidded wooden bin, the lid in two halves (the near half lifted off
    and leaning, the rice showing), the scoop and the strike stick on the closed half. ab: both halves off, the rice
    spilled in front, the bin half empty."""
    P = SP("rice_bin", budget="small", mass=30.0)
    w, d, h = 0.75, 0.50, 0.60
    t = 0.022
    P.adds([board(-w / 2, w / 2, 0.0, h, -d / 2, -d / 2 + t, k=1, vis=(1, 2)),
            board(-w / 2, w / 2, 0.0, h, d / 2 - t, d / 2, k=2, vis=(1, 2)),
            board(-w / 2, -w / 2 + t, 0.0, h, -d / 2 + t, d / 2 - t, k=3, vis=(1, 2)),
            board(w / 2 - t, w / 2, 0.0, h, -d / 2 + t, d / 2 - t, k=4, vis=(1, 2)),
            W(-w / 2 - 0.01, w / 2 + 0.01, 0.0, 0.03, -d / 2 - 0.01, d / 2 + 0.01, WEATH, vis=(1,))])
    if state == "intact":
        P.add(W(-w / 2 + t, w / 2 - t, h - 0.10, h - 0.09, -d / 2 + t, d / 2 - t, RICE, vis=(1,)))
        lid = board(-w / 2, 0.0, h, h + 0.02, -d / 2, d / 2, k=5, vis=(1, 2))
        P.add(lid)
        P.add(xf(board(w / 2 + 0.01, w / 2 + 0.03, 0.0, w / 2, -d / 2, d / 2, k=6, vis=(1, 2)), rz=12.0,
                 pivot=(w / 2 + 0.03, 0.0, 0.0), t=(0.04, 0.005, 0.0)))                              # the other half
        P.add(pole((-0.33, h + 0.03, 0.15), (-0.05, h + 0.03, 0.18), 0.012, WEATH, n=5))         # strike stick
        P.add(xf(lathe([(0.0, 0.0), (0.05, 0.0), (0.05, 0.06), (0.046, 0.06), (0.0, 0.004)], 6, WEATH, vis=(1,)),
                 t=(-0.20, h + 0.02, -0.10)))                                                    # scoop
        c = col(-w / 2, w / 2, 0.0, h + 0.02, -d / 2, d / 2)
        P.add(c)
        P.loot_rect("lid", h + 0.02, -0.35, -0.02, -0.22, 0.10, rng=0.15, points=[(-0.10, h + 0.02, 0.0)])
    else:
        P.add(W(-w / 2 + t, w / 2 - t, 0.20, 0.21, -d / 2 + t, d / 2 - t, RICE, vis=(1,)))
        P.add(xf(board(-w / 2, 0.0, 0.0, 0.02, -d / 2, d / 2, k=5, vis=(1, 2)), ry=20.0, t=(-0.10, 0.0, d / 2 + 0.35)))
        P.add(mound(91, 0.15, d / 2 + 0.20, 0.25, 0.04, RICE, sx=1.6, wear="_w2", vis=(1,)))
        c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
        P.add(c)
        P.loot_rect("rice", 0.21, -0.30, 0.30, -0.18, 0.18, rng=0.15, points=[(0.0, 0.21, 0.0)])
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("w", w, w)
    P.notes.append("the rice dealer's bin (BTI 713-714); loot on the closed lid half / in the bin when abandoned")
    return P


# ================================================================================================ fish and greens
def fish_tub(state="intact"):
    """A shallow fish tub (d 0.70 x 0.22): salt fish laid in a ring on a bamboo-leaf bed. ab: empty, the bottom stained
    dark, a few bones."""
    P = SP("fish_tub", budget="small", mass=8.0)
    r, h = 0.35, 0.22
    P.adds(tub(r, h, wear="_w2" if state != "intact" else None))
    if state == "intact":
        P.add(W(-0.26, 0.26, 0.10, 0.105, -0.26, 0.26, LEAF, vis=(1,)))
        for k in range(9):
            a = 2 * math.pi * k / 9
            P.add(xf(bipyramid((0.0, 0.0, 0.0), 0.11, 0.025, 0.035, FISH, n=4, top=0.025), ry=math.degrees(a) + 90.0,
                     t=(0.18 * math.cos(a), 0.13, 0.18 * math.sin(a))))
        P.loot_rect("rim", h, -0.04, 0.04, 0.338, 0.35, rng=0.10, points=[(0.0, h, 0.344)])
    else:
        P.add(stain(101, 0.0, 0.0, 0.22, y=0.016, mat=LITTER))
        for k in range(3):
            P.add(xf(box(-0.06, 0.06, 0.016, 0.022, -0.004, 0.004, PALE, vis=(1,)), ry=40.0 * k, t=(0.05 * k, 0.0, 0.03)))
    P.add(cyl_col(r, 0.0, h, n=8))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WEATH, vis=(2,)))
    P.dim("d", 2 * r, 2 * r)
    return P


def fish_board(state="intact"):
    """Fishmonger's cutting board on legs (manaita, 0.90 x 0.35 x 0.30), a deba knife and a fish on it. ab: tipped on
    its side, the knife on the floor."""
    P = SP("fish_board", budget="small", mass=10.0)
    w, d, h = 0.90, 0.35, 0.30
    parts = [board(-w / 2, w / 2, h - 0.06, h, -d / 2, d / 2, k=3, vis=(1, 2))]
    for x in (-w / 2 + 0.06, w / 2 - 0.06):
        parts.append(board(x - 0.03, x + 0.03, 0.0, h - 0.06, -d / 2 + 0.02, d / 2 - 0.02, k=6, vis=(1, 2)))
    if state == "intact":
        P.adds(parts)
        P.add(W(0.10, 0.28, h, h + 0.004, -0.03, 0.03, IRON, vis=(1,)))
        P.add(W(0.28, 0.40, h, h + 0.02, -0.015, 0.015, WOOD, vis=(1,)))
        P.add(xf(bipyramid((0.0, 0.0, 0.0), 0.16, 0.03, 0.045, FISH, n=4, top=0.03), ry=8.0, t=(-0.18, h + 0.03, 0.0)))
        c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
        P.add(c)
        fkit.road_tops(P, [c], "boards")
        P.loot_rect("board", h, -0.02, 0.40, -0.14, 0.14, rng=0.15, points=[(0.20, h, 0.08)])
    else:
        from lkit import place_group
        vs, cs = place_group(parts, [box(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD)], [dict(rx=-90.0), dict(ry=10.0)])
        P.adds(vs)
        P.adds([fkit.col_solid(c) for c in cs])
        P.add(xf(W(-0.09, 0.09, 0.0, 0.004, -0.03, 0.03, IRON, vis=(1,)), ry=60.0, t=(0.30, 0.0, 0.45)))
        P.add(stain(102, -0.1, 0.5, 0.2, mat=LITTER))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("w", w, w)
    return P


def veg_basket(state="intact"):
    """A big round basket (d 0.55 x 0.40) heaped with autumn vegetables: daikon, turnips, taro, persimmons, leafy tops.
    ab: rotted to a black heap, the basket sagging."""
    P = SP("veg_basket", budget="small", mass=12.0)
    r, h = 0.275, 0.40
    P.add(lathe([(0.0, 0.0), (r * 0.8, 0.0), (r, h), (r - 0.012, h), (r * 0.8 - 0.012, 0.012), (0.0, 0.012)], 9,
                WEAVE, vis=(1, 2), wear="_w2" if state != "intact" else None))
    rr = random.Random(103 if state == "intact" else 104)
    if state == "intact":
        for k in range(4):                                                # daikon lying across the top
            a = rr.uniform(0, 180)
            P.add(xf(lathe([(0.0, -0.20), (0.02, -0.15), (0.032, 0.0), (0.03, 0.17), (0.0, 0.2)], 5, KINARI,
                           vis=(1,)), rz=90.0, ry=a, t=(rr.uniform(-0.08, 0.08), h - 0.02 + 0.03 * (k % 2),
                                                      rr.uniform(-0.08, 0.08))))
        for k in range(5):                                                # turnips, taro, persimmons
            mat = (KINARI, DARK, RED, DARK, RED)[k]
            P.add(ball((rr.uniform(-0.15, 0.15), h + 0.04, rr.uniform(-0.15, 0.15)), 0.045, mat))
        P.add(xf(W(-0.12, 0.12, 0.0, 0.01, -0.05, 0.05, FOLIAGE, vis=(1,)), ry=30.0, t=(0.05, h + 0.06, 0.0)))
    else:
        P.add(mound(105, 0.0, 0.0, 0.20, 0.06, DARK, wear="_w2", vis=(1,)))
        P.solids[-1] = xf(P.solids[-1], t=(0.0, h - 0.10, 0.0))
        P.add(stain(106, 0.15, 0.30, 0.18, mat=LITTER))
    P.add(cyl_col(r, 0.0, h, n=8))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WEAVE, vis=(2,)))
    P.dim("d", 2 * r, 2 * r)
    P.notes.append("greengrocer's autumn stock (BTI 724-725); rots by the abandoned state")
    return P


# ================================================================================================ tofu
def tofu_tank(state="intact"):
    """The tofu tank (1.20 x 0.60 x 0.55): a wooden water tank with tofu blocks under water, a board across one end.
    ab: dry, a green-black stain on the bottom, the board fallen in."""
    P = SP("tofu_tank", budget="small", mass=40.0)
    w, d, h = 1.20, 0.60, 0.55
    t = 0.03
    P.adds([board(-w / 2, w / 2, 0.0, h, -d / 2, -d / 2 + t, k=1, vis=(1, 2)),
            board(-w / 2, w / 2, 0.0, h, d / 2 - t, d / 2, k=2, vis=(1, 2)),
            board(-w / 2, -w / 2 + t, 0.0, h, -d / 2 + t, d / 2 - t, k=3, vis=(1, 2)),
            board(w / 2 - t, w / 2, 0.0, h, -d / 2 + t, d / 2 - t, k=4, vis=(1, 2)),
            W(-w / 2 + t, w / 2 - t, 0.0, 0.04, -d / 2 + t, d / 2 - t, WEATH, vis=(1,))])
    if state == "intact":
        P.add(W(-w / 2 + t, w / 2 - t, h - 0.08, h - 0.075, -d / 2 + t, d / 2 - t, WATER, vis=(1,)))
        for k in range(5):
            P.add(W(-0.40 + 0.17 * k, -0.28 + 0.17 * k, h - 0.14, h - 0.08, -0.08 + 0.05 * (k % 2), 0.05 + 0.05 * (k % 2),
                    TOFU, vis=(1,)))
        P.add(board(w / 2 - 0.28, w / 2, h, h + 0.025, -d / 2, d / 2, k=7, vis=(1, 2)))
        P.loot_rect("board", h + 0.025, w / 2 - 0.25, w / 2 - 0.03, -0.25, 0.25, rng=0.12,
                    points=[(w / 2 - 0.14, h + 0.025, 0.0)])
    else:
        P.add(stain(111, 0.0, 0.0, 0.40, y=0.042, sx=1.8, mat=LITTER))
        P.add(xf(board(-0.14, 0.14, 0.0, 0.025, -d / 2, d / 2, k=7, vis=(1, 2)), rz=30.0, t=(0.30, 0.10, 0.0)))
        P.loot_rect("rim", h, -w / 2 + 0.005, -w / 2 + 0.025, -0.20, 0.20, rng=0.08, points=[(-w / 2 + 0.015, h, 0.0)])
    for s_ in ((-w / 2, -w / 2 + t), (w / 2 - t, w / 2)):
        P.add(col(s_[0], s_[1], 0.0, h, -d / 2, d / 2))
    for s_ in ((-d / 2, -d / 2 + t), (d / 2 - t, d / 2)):
        P.add(col(-w / 2 + t, w / 2 - t, 0.0, h, s_[0], s_[1]))
    P.add(col(-w / 2 + t, w / 2 - t, 0.0, 0.04, -d / 2 + t, d / 2 - t))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WEATH, vis=(2,)))
    P.dim("w", w, w)
    P.notes.append("tofu shop water tank (BTI 608-611)")
    return P


def tofu_press(state="intact"):
    """The forming box (slatted, 0.50 x 0.40 x 0.30) on its drain board, the press lid with two weight stones, the
    straining bag hung on the side. ab: the stones off on the floor, the box empty and tipped."""
    P = SP("tofu_press", budget="small", mass=20.0)
    w, d, h = 0.50, 0.40, 0.30
    body = [W(-w / 2 - 0.05, w / 2 + 0.05, 0.0, 0.05, -d / 2 - 0.03, d / 2 + 0.03, WEATH, vis=(1, 2))]
    for k in range(5):
        y0 = 0.05 + 0.05 * k
        body.append(W(-w / 2, w / 2, y0, y0 + 0.04, -d / 2, -d / 2 + 0.018, vis=(1,)))
        body.append(W(-w / 2, w / 2, y0, y0 + 0.04, d / 2 - 0.018, d / 2, vis=(1,)))
        body.append(W(-w / 2, -w / 2 + 0.018, y0, y0 + 0.04, -d / 2, d / 2, vis=(1,)))
        body.append(W(w / 2 - 0.018, w / 2, y0, y0 + 0.04, -d / 2, d / 2, vis=(1,)))
    if state == "intact":
        P.adds(body)
        P.add(W(-w / 2 + 0.02, w / 2 - 0.02, h - 0.03, h, -d / 2 + 0.02, d / 2 - 0.02, WEATH, vis=(1, 2)))
        for x in (-0.11, 0.11):
            P.add(xf(lathe([(0.0, 0.0), (0.09, 0.0), (0.10, 0.06), (0.06, 0.11), (0.0, 0.12)], 7, "stone_river",
                           vis=(1, 2)), t=(x, h, 0.0)))
        P.add(W(-w / 2 - 0.03, -w / 2, 0.10, 0.28, -0.08, 0.08, KINARI, vis=(1,)))
        P.add(col(-w / 2 - 0.05, w / 2 + 0.05, 0.0, h, -d / 2 - 0.03, d / 2 + 0.03))
        P.add(col(-0.21, 0.21, h, h + 0.12, -0.10, 0.10))
        P.loot_rect("drain", 0.05, w / 2 + 0.005, w / 2 + 0.045, -0.12, 0.12, rng=0.08,
                    points=[(w / 2 + 0.025, 0.05, 0.0)])
    else:
        from lkit import place_group
        vs, cs = place_group(body, [box(-w / 2 - 0.05, w / 2 + 0.05, 0.0, h, -d / 2 - 0.03, d / 2 + 0.03, WOOD)],
                             [dict(rz=-90.0), dict(ry=15.0)])
        P.adds(vs)
        P.adds([fkit.col_solid(c) for c in cs])
        for k, x in enumerate((0.45, 0.62)):
            P.adds(rest([xf(lathe([(0.0, 0.0), (0.09, 0.0), (0.10, 0.06), (0.06, 0.11), (0.0, 0.12)], 7, "stone_river",
                                  vis=(1, 2)), rz=20.0 * k, t=(x, 0.0, 0.25 * k))]))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WEATH, vis=(2,)))
    P.dim("w", w, w)
    return P


# ================================================================================================ soba
def soba_board(state="intact"):
    """The soba maker's low table (0.90 x 0.60 x 0.30): the rolling board (noshi-ita) with two pins, the wide noodle
    knife and its guide board, the lacquered kneading bowl (kone-bachi: black outside, shu inside) beside it.
    ab: the bowl upturned on the floor, the pins rolled off."""
    P = SP("soba_board", budget="small", mass=12.0)
    w, d, h = 0.90, 0.60, 0.30
    P.add(board(-w / 2, w / 2, h - 0.04, h, -d / 2, d / 2, k=2, vis=(1, 2)))
    for x in (-w / 2 + 0.05, w / 2 - 0.05):
        P.add(board(x - 0.03, x + 0.03, 0.0, h - 0.04, -d / 2 + 0.03, d / 2 - 0.03, k=6, vis=(1, 2)))
    bowl_vis = [lathe([(0.0, 0.0), (0.12, 0.0), (0.27, 0.13), (0.26, 0.13), (0.11, 0.012), (0.0, 0.012)], 10, LACQ,
                      vis=(1, 2)),
                lathe([(0.0, 0.013), (0.11, 0.013), (0.26, 0.129), (0.25, 0.129), (0.0, 0.03)], 10, SHU, vis=(1,))]
    if state == "intact":
        for k in range(2):
            P.add(pole((-0.35, h + 0.02, -0.12 + 0.07 * k), (0.25, h + 0.02, -0.12 + 0.07 * k), 0.018, WOOD, n=6))
        P.add(W(0.02, 0.30, h, h + 0.008, 0.08, 0.20, PAPER, vis=(1,)))               # a sheet of rolled dough
        P.add(W(0.05, 0.33, h + 0.008, h + 0.012, 0.05, 0.10, IRON, vis=(1,)))        # the noodle knife
        P.add(W(0.05, 0.33, h + 0.012, h + 0.03, 0.10, 0.11, WOOD, vis=(1,)))
        P.adds([xf(s, t=(-0.05, 0.0, d / 2 + 0.32)) for s in bowl_vis])
        P.add(cyl_col(0.27, 0.0, 0.13, n=8, cx=-0.05, cz=d / 2 + 0.32))
    else:
        P.adds([xf(s, rx=180.0, t=(0.20, 0.13, d / 2 + 0.40)) for s in bowl_vis])
        P.add(cyl_col(0.27, 0.0, 0.13, n=8, cx=0.20, cz=d / 2 + 0.40))
        P.add(pole((-0.40, 0.018, d / 2 + 0.20), (0.15, 0.018, d / 2 + 0.80), 0.018, WOOD, n=6))
        P.add(stain(121, -0.2, d / 2 + 0.30, 0.15, mat=LITTER))
    c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
    P.add(c)
    fkit.road_tops(P, [c], "boards")
    P.loot_rect("board", h, 0.30, 0.42, -0.25, 0.25, rng=0.10, points=[(0.37, h, -0.15)])
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("w", w, w)
    P.notes.append("soba steamed in seiro in this period (BTI 650-654); kneading bowl lacquered")
    return P


# ================================================================================================ sweets
def mochi(c, r=0.03, wear=None, mat=TOFU):
    return ball(c, r, mat, n=4, sy=0.55, wear=wear)


def dango_skewer(x, z, y0=0.0, ry=0.0, mat=TOFU, wear=None):
    out = [skewer((-0.07, y0 + 0.012, 0.0), (0.07, y0 + 0.012, 0.0))]
    for k in range(3):
        out.append(ball((-0.03 + 0.03 * k, y0 + 0.012, 0.0), 0.013, mat, n=4, wear=wear))
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in out]


def sg_sweets(state="intact"):
    """Trays of rice cakes (mochi), skewered dango (plain and glazed), steamed buns; a lidded tiered box (jubako).
    ab: trays emptied, a few cakes left mouldy, crumbs."""
    P = SP("sg_sweets", flat=True, mass=2.0)
    if state == "intact":
        P.adds(tray(-0.17, 0.0, 0.20, 0.16, LACQ))
        for k in range(4):
            P.add(mochi((-0.21 + 0.07 * (k % 2), 0.02, -0.035 + 0.07 * (k // 2))))
        P.adds(tray(0.05, 0.0, 0.20, 0.16, SHU))
        for k in range(3):
            P.adds(dango_skewer(0.05, -0.04 + 0.04 * k, y0=0.006, mat=TOFU if k % 2 else WEATH))
        for j in range(2):
            P.add(W(0.18, 0.28, 0.035 * j, 0.035 * j + 0.033, -0.06, 0.06, LACQ, vis=(1,)))
    else:
        P.adds(tray(-0.17, 0.0, 0.20, 0.16, LACQ, wear="_w2"))
        P.add(mochi((-0.20, 0.02, 0.02), wear="_w2"))
        P.adds(tray(0.08, 0.06, 0.20, 0.16, SHU, ry=25.0, wear="_w2"))
        P.add(stain(131, 0.0, 0.12, 0.10, mat=LITTER))
        for j in range(2):
            P.add(W(0.18, 0.28, 0.035 * j, 0.035 * j + 0.033, -0.06, 0.06, LACQ, vis=(1,)))
    return finish_goods(P, TOFU)


def konro(kind="grill", state="intact"):
    """Clay charcoal stoves (shichirin-type boxes are an uncertain date, so these are earthen konro built of clay and
    boards, BTI 415): 'grill' 0.80 x 0.35 x 0.35, an ash bed and iron bars with dango skewers (the sweet shop);
    'nabe3' 1.60 x 0.45 x 0.60, three pot holes with simmering pots (the cooked-food house). ab: cold ash, a pot or
    the skewers off on the floor."""
    big = kind == "nabe3"
    w, d, h = (1.60, 0.45, 0.60) if big else (0.80, 0.35, 0.35)
    P = SP("konro", budget="small", mass=60.0 if big else 25.0)
    ab = state != "intact"
    P.add(W(-w / 2, w / 2, 0.0, h - 0.03, -d / 2, d / 2, DARK, vis=(1, 2)))
    P.add(board(-w / 2 - 0.01, w / 2 + 0.01, h - 0.03, h, -d / 2 - 0.01, d / 2 + 0.01, k=3, vis=(1, 2)))
    P.add(W(-w / 2 + 0.05, w / 2 - 0.05, h + 0.0, h + 0.002, -d / 2 + 0.05, d / 2 - 0.05, ASH, vis=(1,)))
    if not big:
        for k in range(5):
            x = -w / 2 + 0.10 + k * (w - 0.2) / 4
            P.add(W(x - 0.005, x + 0.005, h + 0.002, h + 0.012, -d / 2 + 0.03, d / 2 - 0.03, IRON, vis=(1,)))
        if not ab:
            for k in range(3):
                P.adds(dango_skewer(-0.15 + 0.15 * k, 0.0, y0=h + 0.012, ry=90.0, mat=WEATH))
        else:
            for k in range(3):
                P.adds(dango_skewer(0.25 * k - 0.25, d / 2 + 0.25, y0=0.0, ry=40.0 * k, mat=WEATH, wear="_w2"))
        P.loot_rect("ledge", h, w / 2 - 0.12, w / 2 - 0.02, -0.12, 0.12, rng=0.08, points=[(w / 2 - 0.07, h, 0.0)])
    else:
        from props_s1_g1 import nabe_small
        for k, x in enumerate((-0.50, 0.0, 0.50)):
            if ab and k == 2:
                P.adds(rest([xf(s, rx=95.0, ry=30.0) for s in nabe_small(0.0, 0.0, r=0.17, h=0.14, wear="_w2")]))
                P.solids[-3:] = [xf(s, t=(0.55, 0.0, d / 2 + 0.35)) for s in P.solids[-3:]]
                continue
            P.adds(nabe_small(x, 0.0, r=0.17, h=0.14, y0=h - 0.06, wear="_w2" if ab else None))
        P.loot_rect("ledge", h, w / 2 - 0.20, w / 2 - 0.03, -0.15, 0.15, rng=0.08, points=[(w / 2 - 0.10, h, 0.0)])
        P.loot_rect("ledge2", h, -w / 2 + 0.03, -w / 2 + 0.20, -0.15, 0.15, rng=0.08, points=[(-w / 2 + 0.10, h, 0.0)])
    c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
    P.add(c)
    P.add(lod_box([s for s in P.solids if 1 in s.vis], DARK, vis=(2,)))
    P.dim("w", w, w)
    return P


# ================================================================================================ registry
PROPS = [
    two("jp_f_rice_bin", F, ["komeya"], ERA_BTI % "BTI 713-714", "floor", rice_bin,
        ("jp_f_rice_bin", "jp_f_rice_bin_spilled"), ("Rice bin (kome-bitsu), lid half off",
                                                     "Rice bin, lids off, rice spilled")),
    two("jp_f_fish_tub", F, ["sakana"], ERA_BTI % "BTI 715-717", "floor", fish_tub,
        ("jp_f_fish_tub", "jp_f_fish_tub_empty"), ("Fish tub with salt fish", "Fish tub, empty and stained")),
    two("jp_f_fish_board", F, ["sakana"], ERA_BTI % "BTI 715 (manaita, deba)", "floor", fish_board,
        ("jp_f_fish_board", "jp_f_fish_board_tipped"), ("Fishmonger's cutting board with knife and fish",
                                                        "Cutting board on its side, knife on the floor")),
    two("jp_f_veg_basket", F, ["yaoya"], ERA_BTI % "BTI 724-725", "floor", veg_basket,
        ("jp_f_veg_basket", "jp_f_veg_basket_rotted"), ("Basket of autumn vegetables", "Basket, vegetables rotted")),
    two("jp_f_tofu_tank", F, ["tofu"], ERA_BTI % "BTI 608-611", "floor", tofu_tank,
        ("jp_f_tofu_tank", "jp_f_tofu_tank_dry"), ("Tofu tank with blocks under water", "Tofu tank, dry and stained")),
    two("jp_f_tofu_press", F, ["tofu"], ERA_BTI % "BTI 608-611", "floor", tofu_press,
        ("jp_f_tofu_press", "jp_f_tofu_press_tipped"), ("Tofu forming box with press stones",
                                                        "Tofu box tipped, stones off")),
    two("jp_f_soba_board", F, ["soba"], ERA_BTI % "BTI 650-656", "floor", soba_board,
        ("jp_f_soba_board", "jp_f_soba_board_upset"), ("Soba board, pins, knife, kneading bowl",
                                                       "Soba board, bowl upturned, pins rolled off")),
    two("jp_f_sg_sweets", G, ["mochiya"], ERA_BTI % "BTI 630-639 (sakura-mochi 1717 in era)", "surface", sg_sweets,
        ("jp_f_sg_sweets", "jp_f_sg_sweets_mouldy"), ("Goods: mochi, dango, a tiered box",
                                                      "Goods: trays emptied, mould")),
    {"id": "jp_f_konro", "cat": F, "mount": "floor", "trades": ["mochiya", "nimeuri"],
     "era": ERA_BTI % "BTI 415 (earthen stoves; the small shichirin is an uncertain date), 635-637, 659-661",
     "models": [
         M("jp_f_konro_grill", "grill", "intact", "Clay grill with dango skewers", lambda: konro("grill")),
         M("jp_f_konro_grill_cold", "grill", "cold", "Clay grill, cold, skewers on the floor",
           lambda: konro("grill", "cold")),
         M("jp_f_konro_nabe3", "nabe3", "intact", "Long clay stove with three simmering pots", lambda: konro("nabe3")),
         M("jp_f_konro_nabe3_cold", "nabe3", "cold", "Long clay stove, cold, a pot tipped off",
           lambda: konro("nabe3", "cold"))]},
    kanban_prop("kome", "kanban_kome", "rice (kome)", ["komeya"]),
    kanban_prop("sakana", "kanban_sakana", "fish (sakana)", ["sakana"]),
    kanban_prop("aomono", "kanban_aomono", "greens (aomono)", ["yaoya"]),
    kanban_prop("tofu", "kanban_tofu", "tofu", ["tofu"]),
    kanban_prop("soba", "kanban_osobakiri", "soba (o-soba-kiri)", ["soba"], mat=SUMI),
    kanban_prop("mochi", "kanban_mochi", "famous rice cakes (meibutsu mochi)", ["mochiya"]),
    kanban_prop("okashi", "kanban_okashidokoro", "confectioner (o-kashi-dokoro)", ["mochiya"], mat=SUMI),
]
