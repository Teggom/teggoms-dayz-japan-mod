"""Life layer C (research/interior/LIFE_LAYER.md items 18-26): meals and kitchen life, the "they left mid-meal" layer.

Small table things (trays, flasks, grinding bowl, fire-striker) are visual only (flat=True) and mount on a surface or
the floor. Casks, baskets that stand, charcoal bales and the steamer on its pot carry collision; casks and standing
bales carry a loot point on their tops (BUILD_LIST jp_f_taru: cask top, 1 point, range 0.15).
"""
import math
import random

import lkit
from lkit import (core, box, prism, lathe, xf, xfs, flat_poly, W, board, pole, beam, rope_path, grid_sheet, col, disc,
                  stain, mound, text, uvcell, LPart, M, rng, bipyramid, lod_box, wear_all, rest, cyl_col, hull_col,
                  soft_slab, WOOD, WEATH, SOOTW, IRON, PALE, DARK, LACQ, BAMBOO, WEAVE, MUSHIRO, TAWARA, ROPE, PAPER,
                  INDIGO, RED, LEAF, LITTER, ASH, RICE, KAKI, KINARI, STONE, LIFE)

CAT = "meal"


def flatpart(name, mass=0.5):
    return LPart(name, budget="small", mass=mass, anchor="floor", flat=True)


def bowl(cx, cz, y=0.0, r=0.06, h=0.055, mat=LACQ, n=6, wear=None, lid=False, fill=None, fill_wear="_w1"):
    """A rice / soup bowl on a foot ring; lid: its own lid on top; fill: a mound of rice (RICE) or a dark soup."""
    out = [lathe([(0.0, 0.0), (r * 0.45, 0.0), (r * 0.5, 0.01), (r, h), (r * 0.9, h), (0.0, 0.015)], n, mat, vis=(1,),
                 wear=wear)]
    if fill == "rice":
        out.append(xf(mound(int(cx * 997 + cz * 131) % 1000, 0.0, 0.0, r * 0.8, 0.02, RICE, wear=fill_wear, vis=(1,)),
                      t=(0.0, h - 0.018, 0.0)))
    elif fill == "soup":
        out.append(flat_poly([(r * 0.8 * math.cos(-k * 2 * math.pi / 6), r * 0.8 * math.sin(-k * 2 * math.pi / 6))
                              for k in range(6)], h - 0.02, ASH, vis=(1,), wear="_w2"))
    if lid:
        out.append(lathe([(0.0, h + 0.03), (r * 0.3, h + 0.03), (r * 0.35, h + 0.02), (r * 0.95, h), (0.0, h)], n, mat,
                         vis=(1,), wear=wear))
    return xfs(out, t=(cx, y, cz))


def chopsticks(cx, y, cz, yaw=0.0, mat=LACQ):
    return xfs([box(-0.11, 0.11, 0.0, 0.006, d - 0.003, d + 0.003, mat, vis=(1,)) for d in (-0.006, 0.006)],
               ry=yaw, t=(cx, y, cz))


def sakazuki(cx, cz, y=0.0, r=0.045, tipped=False):
    """A shallow lacquered sake cup (the period cup: LIFE_LAYER_ERA 20, not the later porcelain choko)."""
    s = lathe([(0.0, 0.0), (r * 0.35, 0.0), (r * 0.35, 0.008), (r, 0.022), (r * 0.92, 0.022), (0.0, 0.012)], 7, LACQ,
              vis=(1,))
    if tipped:
        s = xf(s, rx=80.0, t=(0.0, r * 0.95, 0.0))
    return xf(s, t=(cx, y, cz))


# ================================================================================================ 18 tableware (★)
def hakozen(cx, cz, y=0.0, mat=LACQ, lid_up=True, wear=None):
    """Box tray 0.30 x 0.30 x 0.20: a lidded box holding one person's bowls; the lid turns over as the tray."""
    out = [W(cx - 0.15, cx + 0.15, y, y + 0.17, cz - 0.15, cz + 0.15, mat, vis=(1,))]
    if lid_up:
        out.append(W(cx - 0.155, cx + 0.155, y + 0.17, y + 0.20, cz - 0.155, cz + 0.155, mat, vis=(1,)))
    return wear_all(out, wear)


def zen(cx, cz, y=0.0, mat=LACQ, wear=None, rim=True):
    """Legged tray 0.36 x 0.36 x 0.15: a rimmed top on four legs."""
    out = [W(cx - 0.18, cx + 0.18, y + 0.12, y + 0.135, cz - 0.18, cz + 0.18, mat, vis=(1, 2))]
    if rim:
        out += [W(cx - 0.18, cx + 0.18, y + 0.135, y + 0.15, cz + 0.17, cz + 0.18, mat, vis=(1,)),
                W(cx - 0.18, cx + 0.18, y + 0.135, y + 0.15, cz - 0.18, cz - 0.17, mat, vis=(1,)),
                W(cx - 0.18, cx - 0.17, y + 0.135, y + 0.15, cz - 0.17, cz + 0.17, mat, vis=(1,)),
                W(cx + 0.17, cx + 0.18, y + 0.135, y + 0.15, cz - 0.17, cz + 0.17, mat, vis=(1,))]
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(cx + sx * 0.15 - 0.015, cx + sx * 0.15 + 0.015, y, y + 0.12, cz + sz * 0.15 - 0.015,
                         cz + sz * 0.15 + 0.015, mat, vis=(1,)))
    out.append(W(cx - 0.18, cx + 0.18, y, y + 0.15, cz - 0.18, cz + 0.18, mat, vis=(2,)))
    return wear_all(out, wear)


def tableware(kind):
    P = flatpart("tableware", 2.0)
    if kind == "hakozen_stack":
        for k in range(3):
            P.adds(xfs(hakozen(0.0, 0.0, 0.20 * k), ry=(k - 1) * 4.0))
        P.dim("stack_h", 0.60, 0.60, tol=0.005)
    elif kind == "hakozen_plain":
        for k in range(2):
            P.adds(xfs(hakozen(0.0, 0.0, 0.20 * k, mat=WOOD), ry=k * 6.0))
        P.adds(bowl(0.25, 0.05, 0.0, mat=WOOD, n=6))
        P.dim("stack_h", 0.40, 0.40, tol=0.005)
    elif kind == "zen":
        P.adds(zen(0.0, 0.0))
        P.adds(bowl(-0.08, 0.07, 0.135, lid=True))
        P.adds(bowl(0.08, 0.07, 0.135, r=0.055, lid=True))
        P.adds(bowl(-0.07, -0.08, 0.135, r=0.045, h=0.03, mat=PALE))
        P.adds(chopsticks(0.02, 0.137, -0.14))
        P.dim("zen_w", 0.36, 0.36, tol=0.005)
    elif kind == "bowls":                               # a stack of bowls and dishes for a shelf board
        for k in range(4):
            P.adds(bowl(-0.07, 0.0, 0.012 * k, r=0.062, mat=PALE if k % 2 else DARK, n=7))
        for k in range(3):
            P.add(lathe([(0.0, 0.006 * k), (0.07, 0.006 * k), (0.075, 0.006 * k + 0.012), (0.0, 0.006 * k + 0.008)],
                        7, PALE, vis=(1,)))
            P.solids[-1] = xf(P.solids[-1], t=(0.10, 0.0, 0.02))
        P.adds(bowl(0.0, 0.10, 0.0, r=0.06, lid=True))
        P.dim("bowl_d", 0.12, 0.124, tol=0.01)
    else:                                               # as left: a tray on its side, bowls overturned, lids away
        P.adds(rest(xfs(hakozen(0.0, 0.0, 0.0, lid_up=False), rz=90.0, t=(-0.20, 0.0, 0.0)), 0.0))
        P.adds(xfs(hakozen(0.0, 0.0, 0.0), rx=0.0, t=(0.30, 0.0, -0.05)))
        P.adds(rest(xfs(bowl(0.0, 0.0), rx=180.0, t=(0.10, 0.0, 0.25)), 0.0))
        P.adds(rest(xfs(bowl(0.0, 0.0, mat=PALE, r=0.05), rx=165.0, t=(-0.05, 0.0, 0.32)), 0.0))
        P.adds(chopsticks(0.05, 0.0, 0.40, yaw=35.0))
        P.add(stain(181, 0.05, 0.30, 0.18, sx=1.5))
        P.dim("tray_w", 0.30, 0.30, tol=0.005)
    lo = [s for s in P.solids if 1 in s.vis]
    P.add(lod_box(lo, LACQ if kind != "hakozen_plain" else WOOD, vis=(2,)))
    P.notes.append("tableware clutter (mount surface or floor): box trays, legged trays, bowls; no loot (clutter)")
    return P


# ================================================================================================ 19 meal left
def meal_left(kind):
    P = flatpart("meal_left", 2.0)
    if kind in ("zen", "two"):
        P.adds(zen(0.0, 0.0))
        P.adds(bowl(-0.08, 0.07, 0.135, fill="rice", fill_wear="_w2"))
        P.adds(bowl(0.08, 0.07, 0.135, r=0.055, fill="soup"))
        lid = lathe([(0.0, 0.03), (0.018, 0.03), (0.02, 0.02), (0.052, 0.0), (0.0, 0.0)], 6, LACQ, vis=(1,))
        if kind == "zen":
            P.add(xf(lid, rx=180.0, t=(0.20, 0.03, 0.14)))          # the soup lid put down upside down
        dish = lathe([(0.0, 0.0), (0.045, 0.0), (0.05, 0.012), (0.0, 0.008)], 6, PALE, vis=(1,))
        P.add(xf(dish, t=(-0.07, 0.135, -0.08)))
        for k in range(3 if kind == "zen" else 0):                  # pickled plums on the dish
            P.add(bipyramid((-0.08 + 0.018 * k, 0.15, -0.08 + 0.01 * (k % 2)), 0.011, 0.008, 0.011, RED, n=4,
                            wear="_w2"))
        P.adds(chopsticks(0.05, 0.137, -0.10, yaw=8.0))
        P.add(sakazuki(0.28, -0.12, tipped=True))
        if kind == "zen":
            P.add(stain(191, 0.30, -0.02, 0.14, sx=1.4))
        if kind == "two":                                           # the other tray pushed back askew, its flask down
            ss = zen(0.0, 0.0, rim=False) + bowl(-0.08, 0.07, 0.135, n=5, fill="rice", fill_wear="_w2")
            P.adds(xfs(ss, ry=160.0, t=(0.10, 0.0, -0.75)))
            P.adds(rest(xfs(tokkuri(0.0, 0.0, 0.08, 0.16, DARK, n=5), rx=90.0, ry=40.0, t=(-0.35, 0.0, -0.40)),
                        0.0))
            P.add(stain(192, -0.30, -0.35, 0.18, sx=1.3))
        P.dim("zen_w", 0.36, 0.36, tol=0.005)
    else:                                                           # T1: the box tray's lid as the tray, mixed grain
        P.adds(hakozen(0.0, 0.0, 0.0, mat=WOOD, lid_up=False))
        lid = W(-0.155, 0.155, 0.0, 0.03, -0.155, 0.155, WOOD, vis=(1, 2))
        P.add(xf(lid, t=(0.36, 0.0, 0.05)))
        P.adds(bowl(0.30, 0.02, 0.03, mat=WOOD, n=6, fill="rice", fill_wear="_w2"))
        P.adds(bowl(0.42, 0.10, 0.03, r=0.05, mat=WOOD, n=6, fill="soup"))
        P.adds(chopsticks(0.36, 0.032, -0.08, yaw=-10.0, mat=BAMBOO))
        P.adds(rest(xfs(bowl(0.0, 0.0, 0.0, mat=WOOD, n=6), rx=175.0, t=(0.55, 0.0, -0.18)), 0.0))
        P.add(stain(193, 0.45, -0.10, 0.16, sx=1.4))
        P.dim("tray_w", 0.31, 0.31, tol=0.005)
    lo = [s for s in P.solids if 1 in s.vis]
    P.add(lod_box(lo, LACQ if kind != "hakozen" else WOOD, vis=(2,)))
    P.notes.append("a meal left out mid-way: dried rice, soup dregs, pickled plums, a knocked-over sake cup "
                   "(dead-world signature; mount floor or surface; no loot)")
    return P


# ================================================================================================ 20 tokkuri
def tokkuri(cx, cz, r=0.06, h=0.16, mat=DARK, wear=None, n=7):
    """Sake flask: a bulbous body, narrow neck, a flared lip (1700-1750 stoneware, refs i50 i51)."""
    s = lathe([(0.0, 0.0), (r * 0.6, 0.0), (r, h * 0.3), (r * 0.95, h * 0.55), (r * 0.3, h * 0.82), (r * 0.25, h * 0.95),
               (r * 0.35, h), (0.0, h * 0.98)], n, mat, vis=(1,), wear=wear)
    return [xf(s, t=(cx, 0.0, cz))]


def tokkuri_set(kind):
    P = flatpart("tokkuri", 1.0)
    if kind == "pair":
        tray = W(-0.16, 0.16, 0.0, 0.02, -0.11, 0.11, LACQ, vis=(1, 2))
        P.add(tray)
        P.adds(xfs(tokkuri(0.0, 0.0), t=(-0.07, 0.02, 0.0)))
        P.adds(xfs(tokkuri(0.0, 0.0, mat=PALE, r=0.055, h=0.15), t=(0.03, 0.02, -0.03)))
        P.add(sakazuki(0.10, 0.05, 0.02))
        P.add(sakazuki(0.10, -0.06, 0.02))
        P.dim("flask_h", 0.16, 0.16, tol=0.005)
    elif kind == "large":
        P.adds(tokkuri(0.0, 0.0, r=0.09, h=0.26))
        P.add(sakazuki(0.14, 0.04))
        P.dim("flask_h", 0.26, 0.26, tol=0.005)
    else:                                               # as left: a flask on its side, a cup rolled off, the stain
        P.adds(rest(xfs(tokkuri(0.0, 0.0), rz=88.0, ry=30.0), 0.0))
        P.adds(xfs(tokkuri(0.0, 0.0, mat=PALE, r=0.055, h=0.15), t=(-0.15, 0.0, -0.08)))
        P.add(sakazuki(0.20, 0.12, tipped=True))
        P.add(sakazuki(-0.05, 0.18))
        P.add(stain(201, 0.10, 0.05, 0.16, sx=1.6))
        P.dim("flask_h", 0.16, 0.16, tol=0.005)
    P.add(lod_box([s for s in P.solids if 1 in s.vis], DARK, vis=(2,)))
    P.notes.append("sake flasks and shallow lacquered cups (no porcelain choko: LIFE_LAYER_ERA 20); mount surface")
    return P


# ================================================================================================ 21 suribachi / board
def suribachi(cx, cz, tipped=False):
    s = lathe([(0.0, 0.0), (0.07, 0.0), (0.15, 0.11), (0.155, 0.12), (0.14, 0.12), (0.06, 0.02), (0.0, 0.02)], 9, DARK,
              vis=(1,))
    stick = pole((0.0, 0.03, 0.0), (0.10, 0.34, 0.08), 0.017, WEATH, n=5, vis=(1,))
    out = [s] if tipped else [s, stick]
    out = xfs(out, t=(cx, 0.0, cz))
    if tipped:
        out = rest(xfs(out, rz=75.0, t=(cx, 0.0, cz)), 0.0)
    return out


def manaita_knife(cx, cz, yaw=0.0, knife_on=True, daikon=True):
    out = [box(-0.21, 0.21, 0.0, 0.04, -0.11, 0.11, WEATH, vis=(1, 2))]
    if knife_on:
        out += [box(0.02, 0.14, 0.04, 0.052, 0.03, 0.05, BAMBOO, vis=(1,)),
                prism([(-0.16, 0.02), (0.02, 0.02), (0.02, 0.065), (-0.14, 0.065)], "y", 0.04, 0.043, IRON, vis=(1,))]
    if daikon:
        out.append(xf(lathe([(0.0, 0.0), (0.035, 0.0), (0.035, 0.11), (0.0, 0.12)], 6, KINARI, vis=(1,)), rz=90.0,
                      t=(0.10, 0.075, -0.04)))
    return xfs(out, ry=yaw, t=(cx, 0.0, cz))


def suribachi_set(kind):
    P = flatpart("suribachi", 3.0)
    if kind == "bowl":
        P.adds(suribachi(0.0, 0.0))
        P.dim("d", 0.31, 0.31, tol=0.005)
    elif kind == "board":
        P.adds(manaita_knife(0.0, 0.0))
        P.dim("board_w", 0.42, 0.42, tol=0.005)
    else:                                               # as left: the bowl on its side, the pestle rolled, board askew
        P.adds(suribachi(-0.25, 0.10, tipped=True))
        P.add(pole((0.10, 0.017, 0.35), (0.40, 0.017, 0.20), 0.017, WEATH, n=5, vis=(1,)))
        P.adds(manaita_knife(0.25, -0.20, yaw=25.0, knife_on=False, daikon=False))
        P.adds(xfs([box(-0.06, 0.06, 0.0, 0.012, -0.01, 0.01, BAMBOO, vis=(1,)),
                    prism([(0.06, -0.02), (0.24, -0.02), (0.22, 0.025), (0.06, 0.025)], "y", 0.0, 0.003, IRON,
                          vis=(1,))], ry=-60.0, t=(0.05, 0.0, 0.10)))
        P.add(mound(211, -0.40, 0.25, 0.10, 0.012, ASH, sx=1.4, wear="_w2", vis=(1,)))
        P.add(stain(212, -0.30, 0.20, 0.20, sx=1.5))
        P.dim("d", 0.31, 0.31, tol=0.005)
    P.add(lod_box([s for s in P.solids if 1 in s.vis], DARK, vis=(2,)))
    P.notes.append("grinding bowl with its pestle; cutting board with a knife (mount surface or floor)")
    return P


# ================================================================================================ 22 seiro on the pot
SEAT_Y = 0.168          # as jp_f_kama: the flange underside seats in the kamado rim (rim top - 0.168)


def hagama():
    """A light rice pot for the steamer stack (the same seat and flange as jp_f_kama, fewer faces)."""
    return [lathe([(0.0, 0.0), (0.16, 0.02), (0.21, 0.10), (0.212, 0.165), (0.252, 0.168), (0.252, 0.182),
                   (0.20, 0.19), (0.19, 0.27), (0.0, 0.26)], 10, IRON, vis=(1,)),
            lathe([(0.0, 0.0), (0.25, 0.175), (0.19, 0.27), (0.0, 0.26)], 6, IRON, vis=(2,))]


def seiro_tier(y, R=0.20, h=0.13, wear=None, vis=(1,)):
    """One round bentwood steamer tier: the band (outside, rim, inside) and its slatted floor."""
    out = [lathe([(R, y), (R, y + h), (R - 0.012, y + h), (R - 0.012, y + 0.02)], 10, WEATH, vis=vis, wear=wear,
                 smooth=True),
           flat_poly([((R - 0.012) * math.cos(-k * 2 * math.pi / 8), (R - 0.012) * math.sin(-k * 2 * math.pi / 8))
                      for k in range(8)], y + 0.02, BAMBOO, vis=vis, wear=wear)]
    out.append(lkit.rope_ring(R, y + h - 0.02, 0.014, BAMBOO, 10, vis=vis, proud=0.004))
    return out


def seiro_lid(y, R=0.205, wear=None):
    return [lathe([(R, y), (R, y + 0.03), (0.0, y + 0.03)], 10, WEATH, vis=(1,), wear=wear, smooth=False),
            W(-0.012, 0.012, y + 0.03, y + 0.05, -0.12, 0.12, WEATH, vis=(1,))]


def seiro(kind):
    if kind == "stack":                                 # tiers stacked off the pot (a shelf or the floor)
        P = LPart("seiro", budget="small", mass=3.0, anchor="floor", flat=True)
        for k in range(3):
            P.adds(xfs(seiro_tier(0.0, wear="_w1"), ry=k * 11.0, t=(0.0, 0.13 * k, 0.0)))
        P.adds(seiro_lid(0.39))
        P.add(lathe([(0.20, 0.0), (0.20, 0.42), (0.0, 0.42)], 6, WEATH, vis=(2,), smooth=False))
        P.dim("d", 0.40, 0.40, tol=0.005)
        P.notes.append("steamer tiers stacked off the pot (mount surface / floor)")
        return P
    P = LPart("seiro", budget="small", mass=9.0, anchor="floor")
    P.adds(hagama())
    n = 3 if kind == "kama3" else 2
    base = 0.27
    top = base
    if kind in ("kama2", "kama3"):
        for k in range(n):
            P.adds(seiro_tier(base + 0.13 * k))
        top = base + 0.13 * n
        P.adds(seiro_lid(top))
        top += 0.05
    else:                                               # as left: lid and the top tier fallen onto the kamado top
        P.adds(seiro_tier(base, wear="_w2"))
        top = base + 0.13
        kt = SEAT_Y - 0.03                              # the kamado top, 3 cm under the rim (jp_f_kama frame)
        P.adds(rest(xfs(seiro_tier(0.0, wear="_w2"), rx=80.0, ry=20.0, t=(0.40, 0.0, 0.05)), kt))
        P.adds(rest(xfs(seiro_lid(0.0, wear="_w2"), ry=40.0, t=(0.02, 0.0, 0.42)), kt))
    P.add(lathe([(0.25, 0.10), (0.20, top), (0.0, top)], 6, WEATH, vis=(2,), smooth=False))
    P.add(cyl_col(0.23, 0.0, top, n=8, mat=IRON))
    P.seat_y = SEAT_Y
    P.extra["seat_y"] = SEAT_Y
    P.dim("tier_d", 0.40, 0.40, tol=0.005)
    P.notes.append("steamer on the rice pot, seated in the kamado rim like jp_f_kama (mount kamado): place the proxy "
                   "at rim top - 0.168; the 'toppled' state drops the lid and a tier onto the kamado top")
    return P


# ================================================================================================ 23 taru (★)
def cask(cx, cz, y=0.0, d=0.45, h=0.50, wear=None, komo=False, n=10, staved=False, text_cell=None):
    """A coopered cask (4-to), bamboo hoops, a lid; komo: wrapped in a straw mat and roped, a mark on the wrap."""
    R = d / 2
    skip = (2, 3) if staved else ()
    body_mat = MUSHIRO if komo else WOOD
    out = [lathe([(R * 0.94, 0.0), (R, h * 0.5), (R * 0.94, h), (R * 0.9, h), (R * 0.9, h - 0.02), (0.0, h - 0.02)], n,
                 body_mat, vis=(1,), wear=wear, skip=skip)]
    if staved:                                          # the broken staves lie inside, the cask dry and empty
        out.append(lathe([(R * 0.9, 0.03), (R * 0.93, h * 0.5), (0.0, 0.03)], n, WOOD, vis=(1,), wear="_w2"))
    if komo:
        for yy in (0.08, h * 0.5, h - 0.08):
            out.append(lkit.rope_ring(R * (1.0 if 0.1 < yy < h - 0.1 else 0.96), yy, 0.025, ROPE, n, vis=(1,)))
        out.append(lathe([(R * 0.96, h), (R * 0.75, h + 0.03), (0.0, h + 0.03)], n, MUSHIRO, vis=(1,), wear=wear))
        if text_cell:
            out.append(text((0.0, h * 0.55, R + 0.004), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), h * 0.45, LIFE, text_cell,
                            wear="_w1" if not wear else "_w2", off=0.006))
    else:
        for yy in (0.06, 0.16, h - 0.16, h - 0.06):
            out.append(lkit.rope_ring(R * (0.95 + 0.05 * math.sin(math.pi * yy / h)), yy, 0.022, BAMBOO, n, vis=(1,)))
    out.append(lathe([(R * 0.94, 0.0), (R, h * 0.5), (R * 0.94, h), (0.0, h)], 6, body_mat, vis=(2,), smooth=False))
    return xfs(out, t=(cx, y, cz))


def taru(kind):
    P = LPart("taru", budget="small" if kind in ("cask", "komo", "staved") else "furniture", mass=30.0,
              anchor="floor")
    h = 0.50
    if kind in ("cask", "komo", "staved"):
        komo = kind == "komo"
        P.adds(cask(0.0, 0.0, komo=komo, text_cell="taru_morohaku" if komo else None, staved=kind == "staved",
                    wear="_w2" if kind == "staved" else None))
        top = h + (0.03 if komo else -0.02)
        cc = P.add(cyl_col(0.225, 0.0, top, n=8))
        if kind != "staved":                            # F1: stand on a whole cask (not the staved-in one)
            import fkit
            fkit.road_tops(P, [cc], "boards" if not komo else "tatami")
        if kind != "staved":
            P.loot_rect("top", top, -0.12, 0.12, -0.12, 0.12, rng=0.15, points=[(0.0, top, 0.0)])
        else:
            P.add(stain(231, 0.10, 0.30, 0.30, sx=1.4))
        P.dim("d", 0.45, 0.45, tol=0.005)
        P.dim("h", 0.50, h, tol=0.005)
    else:                                               # three casks on the low rack (taru-dana), 1.82 x 0.60 x 0.30
        rh = 0.30
        P.add(board(-0.91, 0.91, rh - 0.04, rh, -0.30, 0.30, k=3, vis=(1, 2)))
        for x in (-0.85, 0.0, 0.85):
            P.add(W(x - 0.05, x + 0.05, 0.0, rh - 0.04, -0.28, 0.28, vis=(1, 2)))
        P.add(W(-0.91, 0.91, 0.0, rh, -0.30, 0.30, vis=(3,)))
        xs = [-0.55, 0.0, 0.55]
        ab = kind == "rack3_ab"
        for i, x in enumerate(xs):
            if ab and i == 2:
                continue
            komo = i == 1
            P.adds(cask(x, 0.0, rh, komo=komo, text_cell="taru_morohaku" if komo else None, n=10,
                        wear="_w2" if ab else None))
            top = rh + h + (0.03 if komo else -0.02)
            import fkit                                 # F1: the cask tops on the rack are walkable
            fkit.road_tops(P, [P.add(cyl_col(0.225, rh, top, n=8, cx=x))], "boards" if not komo else "tatami")
            if not (ab and i == 0):
                P.loot_rect("top%d" % i, top, x - 0.12, x + 0.12, -0.12, 0.12, rng=0.15, points=[(x, top, 0.0)])
        P.add(col(-0.91, 0.91, 0.0, rh, -0.30, 0.30))
        if ab:                                          # the third cask rolled off onto the floor in front
            c, cc = lkit.place_group(cask(0.0, 0.0, 0.0, wear="_w2"), [cyl_col(0.225, 0.0, 0.50, n=8)],
                                     [dict(rz=90.0, ry=15.0), dict(t=(0.72, 0.0, 0.66))])
            P.adds(c)
            P.adds(cc)
            P.add(stain(232, 0.60, 0.45, 0.35, sx=1.5))
        P.res3 = True
        P.dim("rack_w", 1.82, 1.82, tol=0.005)
        P.dim("rack_h", 0.30, rh, tol=0.005)
    P.notes.append("casks: coopered or straw-wrapped (komo) with the mark 'morohaku' (fine sake); loot on the tops")
    return P


# ================================================================================================ 24 baskets (★)
def zaru(R=0.20, h=0.08, wear=None, vis=(1,)):
    return [lathe([(0.0, 0.0), (R * 0.7, 0.0), (R, h), (R - 0.01, h), (R * 0.7 - 0.01, 0.008), (0.0, 0.008)], 10, WEAVE,
                  vis=vis, wear=wear),
            lkit.rope_ring(R, h - 0.005, 0.012, BAMBOO, 10, vis=vis)]


def kago(R=0.175, h=0.30, wear=None, vis=(1,), skip=()):
    return [lathe([(0.0, 0.0), (R * 0.8, 0.0), (R, h * 0.7), (R * 0.95, h), (R * 0.9, h), (R * 0.9, 0.02), (0.0, 0.02)],
                  8, WEAVE, vis=vis, wear=wear, skip=skip),
            lkit.rope_ring(R * 0.96, h - 0.01, 0.02, BAMBOO, 8, vis=vis)]


def back_basket(wear=None, vis=(1,)):
    """Back basket (seoi-kago) 0.45 x 0.35 x 0.60: tapered, square-bottomed, two straw shoulder straps."""
    bw, bd, tw, td, h = 0.30, 0.24, 0.45, 0.35, 0.60
    corners = [(-bw / 2, 0.0, -bd / 2), (bw / 2, 0.0, -bd / 2), (bw / 2, 0.0, bd / 2), (-bw / 2, 0.0, bd / 2),
               (-tw / 2, h, -td / 2), (tw / 2, h, -td / 2), (tw / 2, h, td / 2), (-tw / 2, h, td / 2)]
    body = core.hexa(corners, WEAVE, vis=vis)
    body.faces = [f for i, f in enumerate(body.faces) if i != 1]          # open top
    body.normals = None
    s = core.Solid(body.verts, body.faces, WEAVE, vis=vis)
    # an open box drawn as a sheet: outward normals by face centre
    quads = [[corners[i] for i in f] for f in ([0, 3, 2, 1], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7])]
    inner = [q[::-1] for q in quads[1:]]
    ns = []
    for q in quads + inner:
        c = [sum(p[k] for p in q) / 4 for k in range(3)]
        n = core.norm(core.newell(q))
        ns.append(n)
    sh = core.sheet(quads + inner, WEAVE, ns, vis=vis)
    sh.finalize()
    out = [sh, box(-tw / 2 - 0.01, tw / 2 + 0.01, h - 0.03, h, -td / 2 - 0.01, td / 2 + 0.01, BAMBOO, vis=vis)]
    for sx in (-0.10, 0.10):                           # straps on the back (-z)
        out += rope_path([(sx, 0.52, -0.17), (sx * 1.2, 0.45, -0.28), (sx * 1.2, 0.20, -0.26), (sx, 0.10, -0.13)], 0.012,
                         TAWARA, n=4, vis=vis)
    out.append(box(-0.20, 0.20, 0.0, h, -0.16, 0.16, WEAVE, vis=(2,)))
    return wear_all(out, wear)


def basket(kind):
    if kind == "zaru_wall":
        P = LPart("basket", budget="small", mass=0.6, anchor="wall", flat=True)
        P.add(lkit.peg(0.0, 1.55, z0=0.0))
        zs = xfs(zaru(), rx=78.0, t=(0.0, 1.55 - 0.21, 0.0))
        zmin = min(v[2] for q in zs for v in q.verts)
        P.adds(xfs(zs, t=(0.0, 0.0, 0.003 - zmin)))
        P.add(lod_box([s for s in P.solids if 1 in s.vis], WEAVE, vis=(2,)))
        P.dim("d", 0.40, 0.40, tol=0.005)
        P.notes.append("a flat sieve basket hung on a wall peg")
        return P
    flat = kind in ("zaru", "zaru_stack")
    P = LPart("basket", budget="small", mass=1.5, anchor="floor", flat=flat)
    if kind == "zaru":
        P.adds(zaru())
        P.add(lod_box([s for s in P.solids if 1 in s.vis], WEAVE, vis=(2,)))
        P.dim("d", 0.40, 0.40, tol=0.005)
    elif kind == "zaru_stack":
        for k in range(3):
            P.adds(xfs(zaru(R=0.20 - 0.015 * k), ry=k * 17.0, t=(0.0, 0.015 * k, 0.0)))
        P.add(lod_box([s for s in P.solids if 1 in s.vis], WEAVE, vis=(2,)))
        P.dim("d", 0.40, 0.40, tol=0.005)
    elif kind == "kago":
        P.adds(kago())
        P.add(lathe([(0.175, 0.0), (0.175, 0.30), (0.0, 0.30)], 5, WEAVE, vis=(2,), smooth=False))
        P.add(cyl_col(0.175, 0.0, 0.30, n=6, mat=WEAVE))
        P.dim("h", 0.30, 0.30, tol=0.005)
    elif kind == "kago_tipped":
        ss, cc = lkit.place_group(kago(wear="_w2"), [cyl_col(0.175, 0.0, 0.30, n=6, mat=WEAVE)],
                                  [dict(rx=-90.0, ry=30.0)])
        P.adds(ss)
        for k in range(4):                              # a few withered leaves spilled out
            lf = prism([(-0.04, 0.0), (0.0, -0.025), (0.04, 0.0), (0.0, 0.025)], "y", 0.001, 0.004, LEAF, vis=(1,))
            lf.wear = "_w2"
            P.add(xf(lf, ry=k * 55.0, t=(0.15 + 0.07 * k, 0.0, 0.20 + 0.04 * (k % 2))))
        P.add(lod_box([s for s in P.solids if 1 in s.vis], WEAVE, vis=(2,)))
        P.adds(cc)
        P.dim("h", 0.30, 0.30, tol=0.005)
    elif kind == "back":
        P.adds(back_basket())
        P.add(hull3_col(back_basket()[0]))
        P.dim("h", 0.60, 0.60, tol=0.005)
    else:                                               # as left: the back basket on its side, crushed
        cb = lkit.col(-0.20, 0.20, 0.0, 0.60, -0.16, 0.16, WEAVE)
        ss, cc = lkit.place_group(back_basket(wear="_w2"), [cb], [dict(rz=-90.0), dict(ry=25.0)])
        P.adds(ss)
        P.adds(cc)
        P.dim("h", 0.60, 0.60, tol=0.005)
    P.notes.append("bamboo baskets: sieve (zaru), tall basket (kago), back basket (seoi-kago); no loot")
    return P


def hull3_col(s):
    return lkit.hull3([v for v in s.verts], WEAVE)


# ================================================================================================ 25 charcoal
def charcoal_bits(cx, cz, y, r, n, seed, mat=SOOTW, wear="_w2"):
    rg = random.Random(seed)
    out = []
    for k in range(n):
        a = rg.uniform(0, 2 * math.pi)
        d = rg.uniform(0.06, max(r, 0.07))
        L = rg.uniform(0.04, 0.09)
        b = box(-L / 2, L / 2, 0.0, 0.025, -0.013, 0.013, mat, vis=(1,))
        b = xf(b, ry=rg.uniform(0, 180), rz=rg.uniform(-10, 10), t=(cx + d * math.cos(a), y + 0.008,
                                                                     cz + d * math.sin(a)))
        b.wear = wear
        out.append(b)
    return out


def sumi_bale(cx, cz, y=0.0, R=0.17, h=0.62, open_top=True, wear=None):
    """Charcoal bale (sumi-dawara): an upright straw cylinder, roped, the top open on the charcoal."""
    out = [lathe([(R * 0.9, 0.0), (R, 0.08), (R, h - 0.06), (R * 0.85, h), (R * 0.8, h), (R * 0.8, h - 0.03),
                  (0.0, h - 0.03)], 8, TAWARA, vis=(1,), wear=wear)]
    for yy in (0.12, h * 0.5, h - 0.12):
        out.append(lkit.rope_ring(R, yy, 0.02, ROPE, 8, vis=(1,)))
    if open_top:
        out += charcoal_bits(0.0, 0.0, h - 0.035, R * 0.6, 6, int(cx * 100 + 7))
    out.append(lathe([(R, 0.0), (R, h), (0.0, h)], 5, TAWARA, vis=(2,), smooth=False))
    return xfs(out, t=(cx, y, cz))


def charcoal(kind):
    if kind == "scuttle":
        P = flatpart("charcoal", 3.0)
        w, d, h = 0.32, 0.22, 0.18
        out = [W(-w / 2, w / 2, 0.0, 0.015, -d / 2, d / 2, vis=(1, 2)),
               W(-w / 2, w / 2, 0.0, h, d / 2 - 0.012, d / 2, vis=(1,)),
               W(-w / 2, w / 2, 0.0, h, -d / 2, -d / 2 + 0.012, vis=(1,)),
               W(-w / 2, -w / 2 + 0.012, 0.0, h + 0.05, -d / 2, d / 2, vis=(1,)),
               W(w / 2 - 0.012, w / 2, 0.0, h + 0.05, -d / 2, d / 2, vis=(1,)),
               W(-w / 2, w / 2, h + 0.03, h + 0.05, -0.015, 0.015, vis=(1,)),          # the carrying bar
               W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, vis=(2,))]
        P.adds(out)
        P.adds(charcoal_bits(0.0, 0.0, 0.10, 0.10, 8, 251))
        for dx in (-0.006, 0.006):                      # iron tongs leaning in
            P.add(xf(box(-0.003, 0.003, 0.0, 0.30, -0.003, 0.003, IRON, vis=(1,)), rz=-25.0, t=(0.10 + dx, 0.03, 0.0)))
        P.dim("w", 0.32, w, tol=0.005)
        P.notes.append("charcoal scuttle (sumitori) with tongs (mount floor or surface; beside the hibachi)")
        return P
    P = LPart("charcoal", budget="small" if kind != "bales3" else "furniture", mass=15.0, anchor="floor")
    if kind == "bale":
        P.adds(sumi_bale(0.0, 0.0))
        P.add(cyl_col(0.17, 0.0, 0.62, n=6, mat=TAWARA))
        P.loot_rect("top", 0.59, -0.08, 0.08, -0.08, 0.08, rng=0.15, points=[(0.0, 0.59, 0.0)])
        P.dim("h", 0.62, 0.62, tol=0.005)
    elif kind == "bales3":
        P.adds(sumi_bale(-0.19, 0.0))
        P.adds(sumi_bale(0.19, 0.02, open_top=False))
        P.add(cyl_col(0.17, 0.0, 0.62, n=6, cx=-0.19, mat=TAWARA))
        P.add(cyl_col(0.17, 0.0, 0.62, n=6, cx=0.19, cz=0.02, mat=TAWARA))
        lying, cc = lkit.place_group(sumi_bale(0.0, 0.0, open_top=False), [cyl_col(0.17, 0.0, 0.62, n=6, mat=TAWARA)],
                                     [dict(rx=90.0, ry=10.0, t=(0.0, 0.0, 0.42))])
        P.adds(lying)
        P.adds(cc)
        P.loot_rect("top_l", 0.59, -0.27, -0.11, -0.08, 0.08, rng=0.15, points=[(-0.19, 0.59, 0.0)])
        P.loot_rect("top_r", 0.59, 0.11, 0.27, -0.06, 0.10, rng=0.15, points=[(0.19, 0.59, 0.02)])
        P.dim("h", 0.62, 0.62, tol=0.005)
    else:                                               # as left: a bale on its side, burst, charcoal spilled
        ss, cc = lkit.place_group(sumi_bale(0.0, 0.0, wear="_w2"), [cyl_col(0.17, 0.0, 0.62, n=6, mat=TAWARA)],
                                  [dict(rx=90.0, ry=-20.0)])
        P.adds(ss)
        P.adds(charcoal_bits(0.15, 0.45, 0.0, 0.20, 14, 252))
        P.add(stain(253, 0.12, 0.45, 0.30, sx=1.4, mat=ASH, wear="_w2"))
        P.adds(cc)
        P.dim("h", 0.62, 0.62, tol=0.005)
    P.notes.append("charcoal bales (25 entries, BUILDING_LIST 5.2); standing bales carry a loot point on top")
    return P


# ================================================================================================ 26 hiuchi
def hiuchi(kind):
    P = flatpart("hiuchi", 0.4)
    w, d, h = 0.16, 0.10, 0.07
    box_ = [W(-w / 2, w / 2, 0.0, h - 0.01, -d / 2, d / 2, vis=(1, 2))]
    lid = [W(-w / 2 - 0.003, w / 2 + 0.003, 0.0, 0.012, -d / 2 - 0.003, d / 2 + 0.003, vis=(1,))]
    steel = [box(-0.035, 0.035, 0.0, 0.018, -0.008, 0.008, WOOD, vis=(1,)),
             box(-0.045, 0.045, -0.006, 0.0, -0.006, 0.006, IRON, vis=(1,))]
    flint = [bipyramid((0.0, 0.012, 0.0), 0.02, 0.012, 0.016, STONE, n=4, top=0.012)]
    sticks = [box(-0.06, 0.06, 0.0, 0.003, dz - 0.004, dz + 0.004, BAMBOO, vis=(1,)) for dz in (-0.01, 0.0, 0.01)]
    tinder = [mound(261, 0.0, 0.0, 0.03, 0.012, ASH, vis=(1,), wear="_w2")]
    if kind == "box":
        P.adds(box_ + xfs(lid, t=(0.0, h - 0.01, 0.0)) + xfs(steel, t=(0.0, h + 0.008, 0.0)))
    elif kind == "open":
        P.adds(box_)
        P.adds(xfs(lid, ry=15.0, t=(0.20, 0.0, 0.02)))
        P.adds(xfs(steel, t=(0.02, 0.006, 0.10)))
        P.adds(xfs(flint, t=(-0.12, 0.0, 0.06)))
        P.adds(xfs(sticks, ry=20.0, t=(0.05, 0.0, -0.12)))
        P.adds(xfs(tinder, t=(-0.03, h - 0.02, 0.0)))
    else:                                               # as left: box tipped, tinder and sticks scattered
        P.adds(rest(xfs(box_, rz=90.0, ry=30.0), 0.0))
        P.adds(xfs(lid, ry=70.0, t=(-0.18, 0.0, 0.10)))
        P.adds(xfs(tinder, t=(0.12, 0.0, 0.05)))
        P.adds(xfs(sticks, ry=-40.0, t=(0.10, 0.0, 0.16)))
        P.adds(xfs(steel, ry=80.0, t=(-0.02, 0.006, 0.20)))
        P.add(stain(262, 0.05, 0.10, 0.15, sx=1.4, mat=ASH, wear="_w2"))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("box_w", 0.16, w, tol=0.005)
    P.notes.append("fire-striker kit (hiuchi-bako: flint, steel, tinder, sulphur sticks), every home; on the kamado "
                   "ledge or a shelf (mount surface)")
    return P


PROPS = [
    {"id": "jp_f_tableware", "cat": CAT, "ll": 18, "mount": "surface", "tiers": [1, 2, 3],
     "refs": ["i18_moronobu_1685_p9"], "notes": ["★ BUILD_LIST jp_f_tableware"], "models": [
        M("jp_f_tableware_hakozen_stack", "hakozen_stack", "intact", "Box trays (hakozen), three stacked, lacquer",
          lambda: tableware("hakozen_stack")),
        M("jp_f_tableware_hakozen_plain", "hakozen_plain", "intact", "Box trays, plain wood, two stacked",
          lambda: tableware("hakozen_plain"), tiers=[1, 2]),
        M("jp_f_tableware_zen", "zen", "intact", "Legged tray (zen) with lidded bowls", lambda: tableware("zen")),
        M("jp_f_tableware_bowls", "bowls", "intact", "A stack of bowls and dishes", lambda: tableware("bowls")),
        M("jp_f_tableware_scattered", "scattered", "scattered", "Tableware knocked over, bowls upturned",
          lambda: tableware("scattered"), mount="floor"),
    ]},
    {"id": "jp_f_meal_left", "cat": CAT, "ll": 19, "mount": "floor", "tiers": [1, 2, 3], "refs": [],
     "notes": ["the dead-world signature"], "models": [
        M("jp_f_meal_left_zen", "zen", "left", "A meal left on its tray, a cup knocked over", lambda: meal_left("zen")),
        M("jp_f_meal_left_two", "two", "left", "Two meals left, one tray pushed back, the flask down",
          lambda: meal_left("two")),
        M("jp_f_meal_left_hakozen", "hakozen", "left", "A poor meal on a box-tray lid", lambda: meal_left("hakozen"),
          tiers=[1]),
    ]},
    {"id": "jp_f_tokkuri", "cat": CAT, "ll": 20, "mount": "surface", "tiers": [1, 2, 3],
     "refs": ["i50_met_tokkuri_stoneware", "i51_met_tokkuri_porcelain"], "models": [
        M("jp_f_tokkuri_pair", "pair", "intact", "Two sake flasks and cups on a tray", lambda: tokkuri_set("pair")),
        M("jp_f_tokkuri_large", "large", "intact", "A large sake flask and a cup", lambda: tokkuri_set("large")),
        M("jp_f_tokkuri_tipped", "pair", "tipped", "Sake flask on its side, a cup rolled off",
          lambda: tokkuri_set("tipped")),
    ]},
    {"id": "jp_f_suribachi", "cat": CAT, "ll": 21, "mount": "surface", "tiers": [1, 2, 3], "refs": [], "models": [
        M("jp_f_suribachi_bowl", "bowl", "intact", "Grinding bowl (suribachi) and pestle", lambda: suribachi_set("bowl")),
        M("jp_f_suribachi_board", "board", "intact", "Cutting board with a knife and a radish",
          lambda: suribachi_set("board")),
        M("jp_f_suribachi_spilled", "bowl", "spilled", "Grinding bowl tipped, pestle rolled, board askew",
          lambda: suribachi_set("spilled"), mount="floor"),
    ]},
    {"id": "jp_f_seiro", "cat": CAT, "ll": 22, "mount": "kamado", "tiers": [1, 2, 3], "refs": ["i20_hachioji_kamado"],
     "models": [
        M("jp_f_seiro_kama2", "kama2", "intact", "Steamer, two tiers, on the rice pot", lambda: seiro("kama2")),
        M("jp_f_seiro_kama3", "kama3", "intact", "Steamer, three tiers, on the rice pot", lambda: seiro("kama3")),
        M("jp_f_seiro_stack", "stack", "intact", "Steamer tiers stacked", lambda: seiro("stack"), mount="surface"),
        M("jp_f_seiro_toppled", "kama2", "toppled", "Steamer on the pot, lid and a tier fallen",
          lambda: seiro("toppled")),
    ]},
    {"id": "jp_f_taru", "cat": CAT, "ll": 23, "mount": "floor", "tiers": [2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_taru"], "models": [
        M("jp_f_taru_cask", "cask", "intact", "Coopered cask (taru)", lambda: taru("cask")),
        M("jp_f_taru_komo", "komo", "intact", "Straw-wrapped sake cask, marked", lambda: taru("komo")),
        M("jp_f_taru_rack3", "rack3", "intact", "Three casks on a low rack", lambda: taru("rack3")),
        M("jp_f_taru_staved", "cask", "staved", "Cask staved in, dry", lambda: taru("staved")),
        M("jp_f_taru_rack3_ab", "rack3", "rolled", "Cask rack, one cask gone, one rolled off",
          lambda: taru("rack3_ab")),
    ]},
    {"id": "jp_f_basket", "cat": CAT, "ll": 24, "mount": "floor", "tiers": [1, 2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_basket"], "models": [
        M("jp_f_basket_zaru", "zaru", "intact", "Flat sieve basket (zaru)", lambda: basket("zaru"), mount="surface"),
        M("jp_f_basket_zaru_stack", "zaru", "intact", "Three sieve baskets stacked", lambda: basket("zaru_stack"),
          mount="surface"),
        M("jp_f_basket_zaru_wall", "zaru_wall", "intact", "Sieve basket hung on a wall peg", lambda: basket("zaru_wall"),
          mount="wall"),
        M("jp_f_basket_kago", "kago", "intact", "Tall basket (kago)", lambda: basket("kago")),
        M("jp_f_basket_back", "back", "intact", "Back basket (seoi-kago) with straps", lambda: basket("back")),
        M("jp_f_basket_kago_tipped", "kago", "tipped", "Tall basket on its side, leaves spilled",
          lambda: basket("kago_tipped")),
        M("jp_f_basket_back_crushed", "back", "crushed", "Back basket on its side", lambda: basket("back_crushed")),
    ]},
    {"id": "jp_f_charcoal", "cat": CAT, "ll": 25, "mount": "floor", "tiers": [1, 2, 3], "refs": [], "models": [
        M("jp_f_charcoal_bale", "bale", "intact", "Charcoal bale (sumi-dawara), open", lambda: charcoal("bale")),
        M("jp_f_charcoal_bales3", "bales3", "intact", "Three charcoal bales", lambda: charcoal("bales3")),
        M("jp_f_charcoal_scuttle", "scuttle", "intact", "Charcoal scuttle with tongs", lambda: charcoal("scuttle")),
        M("jp_f_charcoal_burst", "bale", "burst", "Charcoal bale burst, charcoal spilled", lambda: charcoal("burst")),
    ]},
    {"id": "jp_f_hiuchi", "cat": CAT, "ll": 26, "mount": "surface", "tiers": [1, 2, 3], "refs": [], "models": [
        M("jp_f_hiuchi_box", "box", "intact", "Fire-striker box, the steel on the lid", lambda: hiuchi("box")),
        M("jp_f_hiuchi_open", "open", "intact", "Fire-striker kit laid out", lambda: hiuchi("open")),
        M("jp_f_hiuchi_spilled", "box", "spilled", "Fire-striker box tipped, tinder spilled", lambda: hiuchi("spilled")),
    ]},
]
