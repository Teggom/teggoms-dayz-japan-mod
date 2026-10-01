"""Life layer A (research/interior/LIFE_LAYER.md items 1-14): on the walls, posts and beams.

Everything here is visual only (flat=True: no Geometry / View / Fire), like vanilla's small wall items (BUILD_LIST Q5
rule 1: Resolution 1 only in the house), and carries no loot: they make a room lived-in without eating floor or loot
space. Wall and post items: anchor 'wall' (origin on the floor below, the wall face z = 0, heights built in); beam
items: anchor 'hang' (origin = the beam underside). The one floor model per item is the 'as left' state that fell.
"""
import math
import random

import lkit
from lkit import (core, box, prism, sheet, lathe, xf, xfs, flat_poly, W, board, pole, beam, rope_path, sag, grid_sheet,
                  text, uvcell, disc, stain, LPart, M, rng, peg, peg_board, cord, hook_iron, bipyramid, coil, flat_coil,
                  lod_box, only_vis, wall_text, rest, WOOD, WEATH, IRON, PALE, BAMBOO, SOOTB, WEAVE, MUSHIRO, TAWARA,
                  ROPE, STACK, PAPER, CHOCHIN, INDIGO, KINARI, NOREN, RED, LEAF, LITTER, SUMI, LIFE, KAKI, KAYA, LACQ)

CAT = "wall"


def wallpart(name, mass=1.0):
    return LPart(name, budget="small", mass=mass, anchor="wall", flat=True)


def hangpart(name, mass=1.0):
    return LPart(name, budget="small", mass=mass, anchor="hang", flat=True)


# ================================================================================================ 1 mino pegs (★)
BOARD_Y = 1.60          # BUILD_LIST jp_f_mino_pegs: 0.91 peg board at 1.60


def mino(px, py, wear=None, skew=0.0, vis_hi=(1,), vis_lo=(2,)):
    """Straw raincoat hung by its collar from a peg at (px, py): three overlapping straw capes, 0.90 long, the hem
    0.75 wide, bulging off the wall."""
    out = []
    top = py - 0.01
    for k, (y0, L, w0, w1) in enumerate(((top, 0.40, 0.30, 0.52), (top - 0.24, 0.36, 0.46, 0.64),
                                          (top - 0.50, 0.40, 0.58, 0.76))):
        def f(u, v, y0=y0, L=L, w0=w0, w1=w1, k=k):
            w = w0 + (w1 - w0) * v
            x = px + (u - 0.5) * w + skew * (top - (y0 - L * v))
            z = 0.025 + (0.05 + 0.03 * k) * math.sin(math.pi * u) * (0.5 + 0.5 * v) + 0.015 * v
            return (x, y0 - L * v, z)
        out.append(grid_sheet(f, 4, 2, MUSHIRO, vis=vis_hi, wear=wear))
    out.append(grid_sheet(lambda u, v: (px + (u - 0.5) * (0.30 + 0.46 * v) + skew * 0.9 * v, top - 0.90 * v,
                                        0.03 + 0.07 * math.sin(math.pi * u)), 2, 1, MUSHIRO, vis=vis_lo, wear=wear))
    out.append(cord((px - 0.05, top - 0.02, 0.03), (px, py + 0.01, 0.07), 0.005, ROPE))
    out.append(cord((px + 0.05, top - 0.02, 0.03), (px, py + 0.01, 0.07), 0.005, ROPE))
    return out


def kasa(cx, cy, cz, R=0.25, H=0.15, rx=90.0, ry=0.0, rz=0.0, wear=None, vis=(1,), n=10):
    """Conical sedge hat: outer cone + flat underside, a chin cord ring; built axis +y, then turned."""
    s = lathe([(0.0, 0.0), (R, 0.0), (R * 0.96, 0.02), (0.0, H)], n, TAWARA, vis=vis, wear=wear, smooth=False)
    s2 = lathe([(0.0, 0.0), (R, 0.0), (0.0, H)], 6, TAWARA, vis=(2,), wear=wear, smooth=False)
    return [xf(q, rx=rx, ry=ry, rz=rz, t=(cx, cy, cz)) for q in (s, s2)]


def hoe(px, py, z=0.06, ang=8.0, vis=(1,), lo=True):
    """Farm hoe (kuwa) hung by its blade over a peg: iron blade 0.20 x 0.13, handle 1.00 hanging down, tilted."""
    out = [box(-0.10, 0.10, -0.13, 0.0, -0.004, 0.004, IRON, vis=vis),
           box(-0.03, 0.03, -0.16, -0.12, -0.02, 0.02, WEATH, vis=vis),
           pole((0.0, -0.14, 0.0), (0.0, -1.10, 0.02), 0.018, WEATH, n=5, vis=vis)]
    if lo:
        out.append(box(-0.10, 0.10, -1.10, 0.0, -0.02, 0.02, WEATH, vis=(2,)))
    return xfs(out, rz=ang, t=(px, py + 0.02, z))


def sickle(px, py, z=0.05, ang=-6.0, vis=(1,)):
    """Sickle (kama) hung by its handle: handle 0.30, a thin curved blade (two segments)."""
    out = [pole((0.0, 0.0, 0.0), (0.0, -0.30, 0.0), 0.014, WEATH, n=5, vis=vis),
           prism([(0.0, -0.30), (0.10, -0.33), (0.19, -0.30), (0.10, -0.315)], "z", -0.002, 0.002, IRON, vis=vis)]
    return xfs(out, rz=ang, t=(px, py - 0.01, z))


def mino_pegs(state="full"):
    P = wallpart("mino_pegs", 3.0)
    x0, x1 = -0.455, 0.455
    P.add(peg_board(x0, x1, BOARD_Y - 0.05, BOARD_Y + 0.05, k=3))
    pegs = [-0.33, 0.02, 0.28, 0.40]
    for px in pegs:
        P.add(peg(px, BOARD_Y, z0=0.02))
    if state == "full":
        P.adds(mino(-0.33, BOARD_Y))
        P.adds(kasa(0.02, BOARD_Y - 0.25, 0.04))
        P.adds(sickle(0.28, BOARD_Y, z=0.06))
        P.adds(hoe(0.40, BOARD_Y, z=0.08))
    elif state == "rain":
        P.adds(mino(-0.33, BOARD_Y))
        P.adds(kasa(0.02, BOARD_Y - 0.25, 0.04))
    else:                                   # as left: the hat fell, the coat slid round on its peg, one peg empty
        P.adds(mino(-0.33, BOARD_Y, wear="_w2", skew=0.10))
        P.adds(rest(kasa(0.10, 0.0, 0.42, rx=180.0 - 12.0, ry=30.0, wear="_w2"), 0.0))   # upside down on the floor
        P.adds(hoe(0.40, BOARD_Y, z=0.08, ang=22.0))
        P.add(stain(101, 0.10, 0.45, 0.28, sx=1.3))
    P.dim("board_y", BOARD_Y, BOARD_Y, tol=0.005)
    P.dim("board_w", 0.91, x1 - x0, tol=0.005)
    P.notes.append("rural doma wall by the door (BUILD_LIST jp_f_mino_pegs, Kitamura-type set); visual only")
    return P


# ================================================================================================ 2 ofuda
def ofuda_card(x, yc, cellname, w=0.075, h=0.26, wear="_w1", paper_wear="_w1", peel=0.0, z=0.0):
    """A paper charm pasted on a post face (z = 0): thin paper + its printed text. peel > 0: the lower part curls
    away from the post (grid)."""
    out = []
    if peel <= 0:
        pp = box(x - w / 2, x + w / 2, yc - h / 2, yc + h / 2, z + 0.0006, z + 0.0016, PAPER, vis=(1,), uv="fit")
        pp.wear = paper_wear
        out.append(pp)
        out.append(text((x, yc, z + 0.0016), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), h * 0.92, LIFE, cellname, wear=wear,
                        off=0.0008, width=w * 0.86))
    else:
        def f(u, v, dz=0.0):
            t = max(0.0, v - 0.45) / 0.55
            return (x + (u - 0.5) * w, yc + h / 2 - h * v + peel * 0.35 * t * t, z + 0.001 + dz + peel * t * t)
        out.append(grid_sheet(f, 1, 3, PAPER, vis=(1,), wear=paper_wear, uv=lambda u, v: (u * 0.5, v * 0.5)))
        tx = grid_sheet(lambda u, v: f(u * 0.86 + 0.07, v * 0.92 + 0.04, 0.0009), 1, 3, LIFE, vis=(1,),
                        two_sided=False, wear=wear, uv=uvcell(LIFE, cellname))
        out.append(tx)
    return out


def ofuda(state="single"):
    P = wallpart("ofuda", 0.05)
    if state == "single":
        P.adds(ofuda_card(0.0, 1.72, "ofuda_jingu"))
    elif state == "akiba":
        P.adds(ofuda_card(0.0, 1.70, "ofuda_akiba", w=0.07, h=0.24))
    elif state == "row":
        P.adds(ofuda_card(0.0, 1.86, "ofuda_jingu"))
        P.adds(ofuda_card(0.004, 1.58, "ofuda_akiba", w=0.07, h=0.24, wear="_w1", paper_wear="_w1"))
        P.adds(ofuda_card(-0.004, 1.30, "ofuda_somin", w=0.075, h=0.26, wear="_w1", paper_wear="_w2"))
    else:                                   # as left: faded, one peeling off, one torn away to a scrap
        P.adds(ofuda_card(0.0, 1.86, "ofuda_jingu", wear="_w2", paper_wear="_w2"))
        P.adds(ofuda_card(0.0, 1.58, "ofuda_goo", w=0.07, h=0.22, wear="_w2", paper_wear="_w2", peel=0.05))
        scrap = box(-0.03, 0.035, 1.40, 1.44, 0.0006, 0.0016, PAPER, vis=(1,), uv="fit")
        scrap.wear = "_w2"
        P.add(scrap)
    P.add(box(-0.04, 0.04, 1.55, 1.85, 0.0004, 0.0012, PAPER, vis=(2,), uv="fit"))
    P.dim("card_w", 0.075, 0.075, tol=0.01)
    P.notes.append("pasted on a post face (mount 'post'): the post face is z = 0; the card is 7.5 cm wide, so any "
                   "post >= 0.10 takes it")
    return P


# ================================================================================================ 3 koyomi
KOYOMI_W, KOYOMI_Y = 0.42, 1.55


def koyomi(state="std"):
    P = wallpart("koyomi", 0.05)
    cw, ch = lkit.skit.cell_size(LIFE, "koyomi_kyoho15")
    w = KOYOMI_W
    h = w * ch / cw
    y0 = KOYOMI_Y - h / 2
    u0, v0, u1, v1 = lkit.skit.cell(LIFE, "koyomi_kyoho15")
    curl = 0.0 if state == "std" else 1.0
    pw = "_w1" if state == "std" else "_w2"

    def f(u, v, dz=0.0):
        # the bottom-left corner curls off the wall (as left); pinned along the top
        t = max(0.0, (v - 0.55) / 0.45) * max(0.0, (0.55 - u) / 0.55)
        return (-w / 2 + w * u, KOYOMI_Y + h / 2 - h * v + curl * 0.05 * t * t, 0.0012 + dz + curl * 0.07 * t * t)
    P.add(grid_sheet(f, 3, 3, PAPER, vis=(1,), wear=pw, two_sided=True, uv=lambda u, v: (u * w, v * h)))
    P.add(grid_sheet(lambda u, v: f(u, v, 0.0012), 3, 3, LIFE, vis=(1,), two_sided=False, wear="_w1",
                     uv=uvcell(LIFE, "koyomi_kyoho15")))
    for px in (-w / 2 + 0.02, w / 2 - 0.02):                  # two bamboo pins through the top edge
        P.add(pole((px, KOYOMI_Y + h / 2 - 0.015, 0.0), (px, KOYOMI_Y + h / 2 - 0.013, 0.012), 0.003, BAMBOO, n=3))
    P.add(box(-w / 2, w / 2, y0, y0 + h, 0.0008, 0.0016, PAPER, vis=(2,), uv="fit"))
    P.dim("sheet_w", KOYOMI_W, w, tol=0.005)
    P.notes.append("printed calendar for Kyoho 15 (1730): the month heads and the 24 seasonal nodes (LIFE_LAYER_ERA 3)")
    return P


# ================================================================================================ 4 kitchen utensil board
def hishaku(r=0.045, h=0.07, L=0.36, vis=(1,)):
    """Water dipper: a small coopered cup with a bamboo handle along +x (cup at the origin, mouth up)."""
    cup = lathe([(r, 0.0), (r, h), (r - 0.006, h), (r - 0.006, 0.008), (0.0, 0.008)], 7, BAMBOO, vis=vis)
    han = pole((r - 0.004, h * 0.7, 0.0), (r + L, h * 0.85, 0.0), 0.008, BAMBOO, n=4, vis=vis)
    return [cup, han]


def shamoji(L=0.23, vis=(1,)):
    """Rice paddle, blade down (built lying in the x-y plane, handle up +y)."""
    return [prism([(-0.035, -0.10), (0.035, -0.10), (0.04, -0.03), (0.015, 0.0), (-0.015, 0.0), (-0.04, -0.03)], "z",
                  -0.005, 0.005, BAMBOO, vis=vis),
            box(-0.012, 0.012, 0.0, L - 0.10, -0.005, 0.005, BAMBOO, vis=vis)]


def ladle(L=0.32, vis=(1,)):
    """Wooden ladle (otama) hung by its handle: bowl at the bottom."""
    return [lathe([(0.0, -0.035), (0.04, -0.025), (0.045, 0.0), (0.0, -0.008)], 6, BAMBOO, vis=vis),
            box(-0.008, 0.008, 0.0, L, -0.004, 0.004, BAMBOO, vis=vis)]


def manaita(w=0.42, h=0.22, t=0.03, vis=(1, 2)):
    """Cutting board, standing on its long edge against the wall (built in the x-y plane)."""
    return [box(-w / 2, w / 2, 0.0, h, 0.0, t, WEATH, vis=vis)]


def knife(L=0.30, vis=(1,)):
    """Kitchen knife (hocho), blade down along -y: wooden handle 0.12, blade 0.18."""
    return [box(-0.012, 0.012, 0.0, 0.12, -0.008, 0.008, BAMBOO, vis=vis),
            prism([(-0.02, 0.0), (0.02, 0.0), (0.02, -0.16), (-0.02, -0.18)], "z", -0.0015, 0.0015, IRON, vis=vis)]


def utensil_board(state="full"):
    P = wallpart("utensil_board", 3.0)
    wide = state != "small"
    x0, x1 = (-0.455, 0.455) if wide else (-0.30, 0.30)
    yb0, yb1 = 1.10, 1.55
    P.add(board(x0, x1, yb0, yb1, 0.0, 0.018, k=6, vis=(1, 2)))
    rail_y = 1.48
    P.add(board(x0 + 0.02, x1 - 0.02, rail_y - 0.02, rail_y + 0.02, 0.018, 0.04, k=2, vis=(1,)))   # the hook rail
    fell = state == "fallen"
    xs = [-0.34, -0.18, 0.00, 0.20, 0.36] if wide else [-0.20, 0.00, 0.20]
    for x in xs:
        P.add(peg(x, rail_y, L=0.06, r=0.008, z0=0.04))
    # dipper hung by its handle end, cup down and out
    d = xfs(hishaku(), rz=-100.0, t=(xs[0] + 0.02, rail_y + 0.01, 0.075))
    P.adds(d)
    P.adds(xfs(shamoji(), t=(xs[1], rail_y - 0.14, 0.06)))
    if not fell:
        P.adds(xfs(ladle(), t=(xs[2], rail_y - 0.33, 0.062)))
    # knife holder: a slotted block with two handles up
    kx = xs[-1] if wide else xs[2]
    P.add(board(kx - 0.08, kx + 0.08, 1.16, 1.30, 0.018, 0.06, k=8, vis=(1,)))
    if not fell:
        for dx in (-0.035, 0.035):
            P.adds(xfs(knife(), t=(kx + dx, 1.30, 0.04)))
    if wide:
        if not fell:
            P.adds(xfs(manaita(), t=(0.20, 1.12, 0.018)))
            P.adds(xfs(ladle(), t=(xs[3], rail_y - 0.33, 0.062)))
        else:                               # as left: the board and a ladle on the floor, a knife gone, a stain
            P.adds(xfs(manaita(vis=(1,)), rx=-90.0, ry=12.0, t=(0.05, 0.0, 0.30)))
            P.adds(rest(xfs(ladle(), rz=90.0, ry=40.0, t=(-0.20, 0.0, 0.45)), 0.0))
            P.adds(xfs(knife(), t=(kx - 0.035, 1.30, 0.04)))
            P.add(stain(102, 0.0, 0.40, 0.25, sx=1.5))
    P.dim("board_top", 1.55, yb1, tol=0.005)
    P.notes.append("kitchen utensil board: dipper, rice paddle, ladles, cutting board, knives in a slotted holder")
    return P


# ================================================================================================ 5 tool wall
def saw(vis=(1,)):
    """Carpenter's saw (nokogiri) hung by its handle end: handle 0.30 up, blade 0.28 down."""
    return [pole((0.0, 0.0, 0.0), (0.0, 0.28, 0.0), 0.013, WEATH, n=5, vis=vis),
            prism([(-0.035, 0.0), (0.035, 0.0), (0.055, -0.28), (-0.02, -0.28)], "z", -0.001, 0.001, IRON, vis=vis)]


def adze(vis=(1,)):
    """Adze (chona): a curved handle 0.60 hanging from its head, the blade across the top."""
    out = [box(-0.06, 0.06, -0.03, 0.02, -0.012, 0.012, IRON, vis=vis)]
    pts = [(0.0, -0.02, 0.0), (0.02, -0.22, 0.01), (0.0, -0.42, 0.03), (-0.04, -0.60, 0.05)]
    out += rope_path(pts, 0.016, WEATH, n=5, vis=vis)
    return out


def axe(L=0.70, vis=(1,)):
    """Axe (ono): the head on the peg, the handle down."""
    return [prism([(-0.03, 0.03), (0.09, 0.05), (0.10, -0.06), (-0.03, -0.03)], "z", -0.012, 0.012, IRON, vis=vis),
            pole((0.0, 0.0, 0.0), (0.0, -L, 0.0), 0.017, WEATH, n=5, vis=vis)]


def nata(vis=(1,)):
    """Hatchet (nata) in a wooden sheath, hung by a cord from the handle."""
    return [box(-0.015, 0.015, 0.0, 0.16, -0.012, 0.012, WEATH, vis=vis),
            box(-0.035, 0.035, -0.26, 0.0, -0.012, 0.012, WOOD, vis=vis)]


def tool_wall(state="full"):
    P = wallpart("tool_wall", 6.0)
    x0, x1, y = -0.60, 0.60, 1.62
    P.add(peg_board(x0, x1, y - 0.05, y + 0.05, k=4))
    xs = [-0.48, -0.20, 0.10, 0.42]
    for x in xs:
        P.add(peg(x, y, z0=0.02))
    taken = state == "taken"
    if state in ("full", "taken"):
        if not taken:
            P.adds(xfs(saw(), t=(xs[0], y - 0.29, 0.07)))
            P.adds(xfs(axe(), t=(xs[2], y + 0.02, 0.07)))
        P.adds(xfs(adze(), t=(xs[1], y + 0.02, 0.065)))
        P.adds(xfs(nata(), t=(xs[3], y - 0.20, 0.06)))
        P.add(cord((xs[3], y + 0.005, 0.07), (xs[3], y - 0.04, 0.06), 0.004))
        if taken:                           # the saw dropped under its peg; the axe is gone (loot, not dressing)
            P.adds(xfs(saw(), rx=-90.0, ry=70.0, t=(xs[0] + 0.05, 0.004, 0.30)))
            P.add(stain(103, -0.10, 0.35, 0.30, sx=1.6))
    else:                                   # 'wood': the woodcutting set, two axes and a hatchet
        P.adds(xfs(axe(0.75), t=(xs[0], y + 0.02, 0.07)))
        P.adds(xfs(axe(0.62), rz=4.0, t=(xs[1], y + 0.02, 0.07)))
        P.adds(xfs(saw(), t=(xs[2], y - 0.29, 0.07)))
        P.adds(xfs(nata(), t=(xs[3], y - 0.20, 0.06)))
    P.add(box(x0, x1, 0.95, y + 0.05, 0.0, 0.08, WEATH, vis=(2,)))
    P.dim("board_y", 1.62, y, tol=0.005)
    P.notes.append("doma / workshop tool corner: saw, adze, axe, hatchet on pegs; the 'taken' state leaves the axe "
                   "gone and the saw on the floor")
    return P


# ================================================================================================ 6 rope pegs
def rope_pegs(state="2"):
    P = wallpart("rope_pegs", 4.0)
    y = 1.65
    n = 3 if state == "3" else 2
    xs = [-0.28, 0.0, 0.28][:n] if n == 3 else [-0.16, 0.16]
    P.add(peg_board(xs[0] - 0.14, xs[-1] + 0.14, y - 0.05, y + 0.05, k=5))
    for i, x in enumerate(xs):
        P.add(peg(x, y, L=0.12, z0=0.02))
        if state == "fallen" and i == 0:
            continue
        R = 0.12 + 0.02 * (i % 2)
        P.add(coil(x, y - 0.02 - R * 1.6, R, 0.028, ROPE, sy=1.6, n=10, m=4, z0=0.02, wear="_w2" if state ==
                   "fallen" else None))
        P.add(coil(x, y - 0.02 - R * 1.6, R - 0.035, 0.024, ROPE, sy=1.6, n=8, m=3, z0=0.03))
    if state == "fallen":                   # one coil dropped, half paid out across the floor
        P.add(flat_coil(xs[0] + 0.05, 0.35, 0.13, 0.026, wear="_w2"))
        P.adds(rope_path([(xs[0] + 0.18, 0.02, 0.33), (xs[0] + 0.35, 0.02, 0.55), (xs[0] + 0.60, 0.02, 0.50),
                          (xs[0] + 0.78, 0.02, 0.62)], 0.02, ROPE, n=4, vis=(1,), wear="_w2"))
    P.add(box(xs[0] - 0.14, xs[-1] + 0.14, 1.10, y + 0.05, 0.0, 0.10, ROPE, vis=(2,)))
    P.dim("peg_y", 1.65, y, tol=0.005)
    P.notes.append("straw rope coils on pegs (41 entries, BUILDING_LIST 5.7)")
    return P


# ================================================================================================ 7 sandals hung
def waraji(vis=(1,), wear=None, loops=True):
    """One straw sandal: a sole 0.24 x 0.09 x 0.012 with two side loops (built lying, toe +z)."""
    out = [box(-0.045, 0.045, 0.0, 0.012, -0.12, 0.12, MUSHIRO, vis=vis)]
    if loops:
        out += [box(-0.05, -0.04, 0.0, 0.03, -0.02, 0.03, ROPE, vis=vis),
                box(0.04, 0.05, 0.0, 0.03, -0.02, 0.03, ROPE, vis=vis)]
    return wear_all(out, wear)


def wear_all(ss, w):
    return lkit.wear_all(ss, w)


def sandal_bunch(x, y, z, n=5, wear=None, seed=1, fan=14.0):
    """n pairs tied through their loops on one cord, hanging from (x, y, z): soles vertical, fanned."""
    r = random.Random(seed)
    out = [cord((x, y, z), (x, y - 0.10, z + 0.01), 0.005)]
    for k in range(n):
        a = (k - (n - 1) / 2) * fan + r.uniform(-4, 4)
        for side in (-1, 1):
            s = xfs(waraji(wear=wear, loops=(k == n - 1)), rx=-90.0 + side * 6.0, t=(0.0, 0.0, 0.0))
            s = xfs(s, t=(side * 0.012, -0.10 - 0.12, 0.0))
            s = xfs(s, rz=a, pivot=(0.0, -0.10, 0.0), t=(x, y, z + 0.015 + 0.01 * k))
            out += s
    return out


def sandals_hung(state="wall"):
    if state == "beam":
        P = hangpart("sandals_hung", 2.0)
        P.adds(hook_iron(0.0, 0.0))
        P.adds(sandal_bunch(0.0, -0.06, 0.03, n=5, seed=7))
        P.add(box(-0.12, 0.12, -0.42, -0.10, -0.02, 0.06, MUSHIRO, vis=(2,)))
        P.finish_hang()
        P.notes.append("a bunch of new straw sandals on a beam hook (spares, or stock for sale)")
        return P
    P = wallpart("sandals_hung", 2.0)
    y = 1.70
    P.add(peg_board(-0.30, 0.30, y - 0.04, y + 0.04, k=6))
    for x in (-0.16, 0.16):
        P.add(peg(x, y, z0=0.02))
    if state == "wall":
        P.adds(sandal_bunch(-0.16, y, 0.07, n=5, seed=3))
        P.adds(sandal_bunch(0.16, y, 0.07, n=4, seed=4))
    else:                                   # as left: one bunch fell, the cord burst, sandals scattered
        P.adds(sandal_bunch(0.16, y, 0.07, n=4, seed=4, wear="_w2"))
        r = random.Random(5)
        for k in range(6):
            s = xfs(waraji(wear="_w2"), ry=r.uniform(0, 360), t=(-0.25 + r.uniform(-0.2, 0.25), 0.0,
                                                                 0.30 + r.uniform(-0.1, 0.25)))
            P.adds(s)
    P.add(box(-0.30, 0.30, 1.30, y + 0.04, 0.0, 0.10, MUSHIRO, vis=(2,)))
    P.dim("peg_y", 1.70, y, tol=0.005)
    P.notes.append("straw sandals (waraji) tied in bunches (24 entries, BUILDING_LIST 5.7)")
    return P


# ================================================================================================ 8 hoshigaki (autumn)
def persimmon_string(x, top, n, z=0.0, seed=1, gaps=(), wear=None, drop_len=0.0):
    """A straw cord hanging from `top` with n dried persimmons tied along it in alternating pairs (renkaki)."""
    r = random.Random(seed)
    L = 0.10 * n + 0.10 - drop_len
    out = [cord((x, top, z), (x, top - L, z), 0.005, ROPE, n=3)]
    for k in range(n):
        if k in gaps:
            continue
        side = -1 if k % 2 else 1
        y = top - 0.10 - 0.10 * k
        if y < top - L:
            break
        out.append(bipyramid((x + side * 0.038, y, z + r.uniform(-0.01, 0.01)), 0.034, 0.042, 0.030, KAKI, n=5,
                             phase=r.uniform(0, 1), wear=wear, top=0.036))
    return out


def hoshigaki(state="3"):
    P = hangpart("hoshigaki", 3.0)
    n = {"3": 3, "5": 5, "ab": 3}[state if state in ("3", "5") else "ab"]
    span = 0.22 * (n - 1)
    pole_y = -0.08
    P.add(pole((-span / 2 - 0.12, pole_y, 0.0), (span / 2 + 0.12, pole_y, 0.0), 0.016, SOOTB if state == "ab" else
               BAMBOO, n=5, vis=(1, 2)))
    for sx in (-1, 1):
        P.add(cord((sx * (span / 2 + 0.06), 0.0, 0.0), (sx * (span / 2 + 0.06), pole_y + 0.015, 0.0), 0.004))
    per = 8 if n == 3 else 5
    for i in range(n):
        x = -span / 2 + 0.22 * i
        if state == "ab":
            gaps = {1: (2, 5), 0: (6,), 2: (1, 3, 4)}[i]
            P.adds(persimmon_string(x, pole_y - 0.015, per, seed=10 + i, gaps=gaps, wear="_w2",
                                    drop_len=0.35 if i == 2 else 0.0))
        else:
            P.adds(persimmon_string(x, pole_y - 0.015, per, seed=10 + i))
        P.add(box(x - 0.04, x + 0.04, pole_y - 0.10 * per - 0.10, pole_y - 0.05, -0.02, 0.02, KAKI, vis=(2,)))
    P.finish_hang()
    P.dim("strings", n, n, tol=0.0)
    P.notes.append("autumn: persimmon strings (renkaki) under a beam or the loft joists (BUILDING_LIST 746); hangs "
                   "%.2f m, so hang it over a hearth, a corner or a shelf, not across a walking line" % P.hang_len)
    return P


# ================================================================================================ 9 drying strings
def daikon(c, L=0.34, r=0.03, wear=None, bend=10.0):
    """A shrivelled drying radish hanging root down from its leaf tuft at c."""
    body = lathe([(0.0, -L), (r * 0.35, -L * 0.85), (r, -L * 0.45), (r * 0.9, -0.04), (r * 0.5, 0.0), (0.0, 0.0)], 5,
                 KINARI, vis=(1,), wear=wear)
    leaves = prism([(-0.035, 0.0), (0.035, 0.0), (0.02, 0.10), (-0.025, 0.09)], "z", -0.01, 0.01, LEAF, vis=(1,))
    leaves.wear = "_w2"
    return xfs([body, leaves], rz=bend, t=c)


def drying(state="daikon"):
    P = hangpart("drying_" + state, 3.0)
    pole_y = -0.08
    w = 0.70
    P.add(pole((-w / 2, pole_y, 0.0), (w / 2, pole_y, 0.0), 0.016, BAMBOO, n=5, vis=(1, 2)))
    for sx in (-1, 1):
        P.add(cord((sx * (w / 2 - 0.05), 0.0, 0.0), (sx * (w / 2 - 0.05), pole_y + 0.015, 0.0), 0.004))
    if state in ("daikon", "daikon_ab"):
        ab = state == "daikon_ab"
        for i, x in enumerate((-0.24, -0.08, 0.08, 0.24)):
            for side in (-1, 1):
                if ab and (i, side) in ((1, 1), (3, -1)):
                    continue
                P.adds(daikon((x + side * 0.03, pole_y - 0.02, side * 0.03), L=0.34 - 0.05 * ab - 0.02 * (i % 2),
                              r=0.030 - 0.008 * ab, wear="_w2" if ab else None, bend=side * 8.0 + (6.0 if ab else 0.0)))
        P.add(box(-0.28, 0.28, pole_y - 0.36, pole_y, -0.04, 0.04, KINARI, vis=(2,)))
    elif state == "chilli":
        for i, x in enumerate((-0.18, 0.12)):
            top = pole_y - 0.015
            P.add(cord((x, top, 0.0), (x, top - 0.50, 0.0), 0.006))
            r = random.Random(20 + i)
            for k in range(12):
                a = k * 2.4
                y = top - 0.05 - 0.037 * k
                P.add(bipyramid((x + 0.03 * math.cos(a), y, 0.03 * math.sin(a)), 0.011, 0.04, 0.011, RED, n=3,
                                phase=r.uniform(0, 3), top=0.012, wear="_w0"))
            P.add(box(x - 0.04, x + 0.04, top - 0.50, top, -0.04, 0.04, RED, vis=(2,)))
    else:                                   # fish: mezashi, small fish skewered through the eyes on straws
        for i, x in enumerate((-0.22, 0.0, 0.22)):
            top = pole_y - 0.015
            P.add(cord((x, top, 0.0), (x, top - 0.08, 0.0), 0.004))
            P.add(cord((x - 0.12, top - 0.08, 0.0), (x + 0.12, top - 0.08, 0.0), 0.004))
            for k in range(5):
                fx = x - 0.10 + 0.05 * k
                P.add(bipyramid((fx, top - 0.08 - 0.085, 0.0), 0.012, 0.085, 0.006, WEATH, n=4, top=0.012,
                                wear="_w2"))
            P.add(box(x - 0.13, x + 0.13, top - 0.18, top - 0.07, -0.01, 0.01, WEATH, vis=(2,)))
    P.finish_hang()
    P.notes.append("autumn drying under a beam: radishes, chillies, small fish (BUILDING_LIST 746, 2846)")
    return P


# ================================================================================================ 10 chochin
def chochin(R, H, cellname, atlas=LIFE, wear="_w1", text_wear="_w1", vis=(1,), both=True):
    """Hanging paper lantern (B3b's form, props_street.chochin, with the atlas as a parameter): 12-sided oblong
    lathe, dark wooden rings top and bottom, the text wrapped round the front (and the back)."""
    prof = [(R * (0.55 + 0.45 * math.sin(math.pi * k / 6)), H * k / 6) for k in range(7)]
    out = [lathe(prof, 12, CHOCHIN, vis=vis, wear=wear)]
    for y in (0.0, H):
        out.append(lathe([(R * 0.58, y - 0.03), (R * 0.58, y + 0.03)], 12, "wood_street_dark", vis=vis, smooth=True))
    out.append(lathe([(0.0, -0.03), (R * 0.58, -0.03)], 8, "wood_street_dark", vis=vis))
    out.append(lathe([(R, 0.0), (R, H), (0.0, H)], 6, CHOCHIN, vis=(2,), wear=wear, smooth=False))
    cw, ch = lkit.skit.cell_size(atlas, cellname)
    th = H * (0.62 if not cellname.startswith("crest") else 0.40)
    span = th * cw / ch
    y0 = (H - th) / 2
    u0, v0, u1, v1 = lkit.skit.cell(atlas, cellname)

    def rad(y):
        return R * (0.55 + 0.45 * math.sin(math.pi * y / H)) + 0.004

    for back in ((False, True) if both else (False,)):
        def f(u, v, back=back):
            y = y0 + th * (1 - v)
            r = rad(y)
            a = (u - 0.5) * span / max(r, 0.05) + (math.pi if back else 0.0)
            return (r * math.sin(a), y, r * math.cos(a))
        out.append(grid_sheet(f, 3, 3, atlas, vis=vis, two_sided=False, wear=text_wear, uv=uvcell(atlas, cellname)))
    return out


def chochin_model(state="crest"):
    R, H = 0.15, 0.42
    cell = {"crest": "crest_igeta", "shop": "chochin_iseya", "shop2": "chochin_yamatoya", "crest2": "crest_mitsubiki",
            "torn": "chochin_iseya", "fallen": "crest_igeta"}[state]
    if state == "fallen":                   # as left: dropped to the floor, crushed and split
        P = LPart("chochin", budget="small", mass=0.3, anchor="floor", flat=True)
        ss = chochin(R, H * 0.7, cell, wear="_w2", text_wear="_w2")
        ss = xfs(ss, rx=90.0, ry=35.0)
        P.adds(lkit.inner_side(rest(ss, 0.0), (CHOCHIN, "wood_street_dark")))   # FP1: inside of the paper drawn
        P.add(stain(104, 0.05, 0.10, 0.25, sx=1.4))
        P.dim("d", 0.30, 2 * R, tol=0.005)
        P.notes.append("a lantern fallen from its hook, crushed (floor)")
        return P
    P = hangpart("chochin", 0.3)
    drop = 0.12
    P.adds(hook_iron(0.0, 0.0, drop=0.05))
    P.add(cord((0.0, -0.045, 0.02), (0.0, -drop, 0.0), 0.004))
    torn = state == "torn"
    ss = chochin(R, H, cell, wear="_w2" if torn else "_w1", text_wear="_w2" if torn else "_w1")
    ss = xfs(ss, t=(0.0, -drop - 0.03 - H, 0.0))
    if torn:
        ss = xfs(ss, rz=9.0, rx=4.0, pivot=(0.0, -drop, 0.0))
    P.adds(ss)
    P.finish_hang()
    P.dim("d", 0.30, 2 * R, tol=0.005)
    P.dim("h", 0.42, H, tol=0.005)
    P.notes.append("hanging paper lantern, unlit (G1 A2-14), text from the life atlas (B1 pipeline fonts)")
    return P


# ================================================================================================ 11 bangasa
def umbrella_closed(L=0.86, shaft=0.20, r=0.055, wear="_w1", vis=(1,)):
    """A closed oiled-paper umbrella along +y from the handle end (y = 0) to the head (y = L + shaft)."""
    out = [pole((0.0, 0.0, 0.0), (0.0, shaft + 0.05, 0.0), 0.011, BAMBOO, n=5, vis=vis)]
    body = lathe([(0.012, shaft), (r * 0.8, shaft + 0.06), (r, shaft + 0.25), (r * 0.75, shaft + L * 0.8),
                  (0.018, shaft + L), (0.0, shaft + L + 0.02)], 8, CHOCHIN, vis=vis, wear=wear)
    out.append(body)
    out.append(lathe([(0.02, shaft - 0.01), (0.02, shaft + 0.02)], 6, "wood_street_dark", vis=vis))
    out.append(lathe([(0.0, shaft), (r, shaft + 0.25), (0.0, shaft + L)], 4, CHOCHIN, vis=(2,), wear=wear))
    return out


def bangasa(state="hung"):
    if state == "open_torn":                # as left: dropped open on the floor, upside down, paper split
        P = LPart("bangasa", budget="small", mass=0.8, anchor="floor", flat=True)
        R, H = 0.52, 0.22
        can = lathe([(0.02, H), (R * 0.55, H * 0.72), (R, 0.0)], 16, CHOCHIN, vis=(1,), wear="_w2", smooth=False)
        can_in = lathe([(R - 0.005, 0.004), (R * 0.55, H * 0.72 - 0.006), (0.02, H - 0.008)], 16, CHOCHIN, vis=(1,),
                       wear="_w2", smooth=False)
        out = [can, can_in]
        for k in range(16):
            a = 2 * math.pi * (k + 0.5) / 16
            out.append(beam((0.02 * math.cos(a), H - 0.01, 0.02 * math.sin(a)), (R * math.cos(a), 0.005,
                                                                                 R * math.sin(a)), 0.006, 0.006,
                            BAMBOO, vis=(1,)))
        out.append(pole((0.0, H, 0.0), (0.0, H - 0.75, 0.0), 0.011, BAMBOO, n=5, vis=(1,)))
        out.append(lathe([(0.0, H), (R, 0.0)], 6, CHOCHIN, vis=(2,), wear="_w2", smooth=False))
        out = xfs(out, rx=180.0 - 25.0, ry=20.0)
        P.adds(rest(out, 0.0))
        P.dim("open_d", 1.04, 2 * R, tol=0.01)
        P.notes.append("an umbrella dropped open, upside down, the oiled paper split between the ribs")
        return P
    P = wallpart("bangasa", 0.8)
    if state == "hung":
        py = 1.86
        P.add(peg(0.0, py, z0=0.0))
        top = 0.20 + 0.86 + 0.02                        # hung by the ring at its head, handle down
        P.adds(xfs(umbrella_closed(), t=(0.0, py - 0.04 - top, 0.075)))
        P.add(cord((0.0, py + 0.01, 0.07), (0.0, py - 0.05, 0.07), 0.004))
        P.dim("peg_y", 1.86, py, tol=0.005)
    else:                                   # leaning against the wall, handle on the floor
        ss = umbrella_closed()
        ss = rest(xfs(ss, rx=-14.0), 0.0)
        zmin = min(v[2] for s in ss for v in s.verts)
        P.adds(xfs(ss, t=(0.0, 0.0, 0.002 - zmin)))
        P.dim("length", 1.08, 0.20 + 0.86 + 0.02, tol=0.01)
    P.notes.append("oiled-paper umbrella (bangasa), BUILDING_LIST 1615-1617")
    return P


# ================================================================================================ 12 inner noren
def noren_inner(state="2"):
    P = hangpart("noren_inner", 0.8)
    n = 3 if state == "3" else 2
    pw = 0.44
    W_ = n * pw
    L = 1.10
    top = -0.02
    P.add(pole((-W_ / 2 - 0.08, top, 0.0), (W_ / 2 + 0.08, top, 0.0), 0.014, BAMBOO, n=5, vis=(1, 2)))
    for sx in (-1, 1):
        P.adds(hook_iron(sx * (W_ / 2 + 0.03), 0.0, drop=0.03))
    torn = state == "torn"
    for i in range(n):
        if torn and i == 0:
            continue
        xa = -W_ / 2 + i * pw + 0.004
        Lp = L * (0.6 if torn and i == 1 else 1.0)
        tilt = 0.06 if torn and i == 1 else 0.0

        def f(u, v, xa=xa, Lp=Lp, tilt=tilt, i=i):
            x = xa + (pw - 0.008) * u + tilt * v
            y = top - 0.015 - Lp * v
            z = 0.012 * math.sin(math.pi * u) * v + 0.01 * (i - n / 2) * v
            return (x, y, z)
        P.add(grid_sheet(f, 1, 3, INDIGO, vis=(1,), wear="_w2" if torn else "_w1"))
        for lx in (0.08, pw - 0.08):        # the cloth loops over the rod
            P.add(box(xa + lx - 0.02, xa + lx + 0.02, top - 0.02, top + 0.016, -0.016, 0.016, INDIGO, vis=(1,)))
    P.add(grid_sheet(lambda u, v: (-W_ / 2 + W_ * u, top - L * v, 0.0), 1, 1, INDIGO, vis=(2,)))
    P.finish_hang()
    P.dim("width", 0.88 if n == 2 else 1.32, W_, tol=0.005)
    P.dim("length", 1.10, L, tol=0.005)
    P.notes.append("inner noren between the shop and the back rooms: hangs from the door head (mount 'doorway', "
                   "origin at the head underside, centred in the opening); no collision, players walk through; "
                   "bottom %.2f above a 2.00 head" % (2.00 - L - 0.02))
    return P


# ================================================================================================ 13 kaya (mosquito net)
def kaya(state="draped"):
    P = hangpart("kaya", 3.0)
    pole_y = -0.10
    w = 0.80
    if state in ("draped", "loose"):
        P.add(pole((-w / 2 - 0.08, pole_y, 0.0), (w / 2 + 0.08, pole_y, 0.0), 0.016, BAMBOO, n=5, vis=(1, 2)))
        for sx in (-1, 1):
            P.add(cord((sx * (w / 2 - 0.02), 0.0, 0.0), (sx * (w / 2 - 0.02), pole_y + 0.016, 0.0), 0.004))
        drop_f, drop_b = (0.45, 0.40) if state == "draped" else (1.25, 0.35)

        def side(sign, drop, loose):
            def f(u, v):
                x = -w / 2 + w * u
                if loose:
                    x = x + 0.25 * v * v * (u - 0.2)
                zz = sign * (0.02 + 0.05 * v + 0.012 * math.sin(4 * math.pi * u) * v)
                return (x, pole_y + 0.02 - (0.02 + drop) * v, zz)
            return f
        P.add(grid_sheet(side(1, drop_f, state == "loose"), 4, 3, KAYA, vis=(1,),
                         wear="_w2" if state == "loose" else "_w1"))
        P.add(grid_sheet(side(-1, drop_b, False), 3, 2, KAYA, vis=(1,)))
        # the red hem band (Omi nets: green with a red edge)
        f = side(1, drop_f, state == "loose")
        P.add(grid_sheet(lambda u, v: core.add(f(u, 1.0), (0.0, 0.05 * (1 - v), 0.004)), 4, 1, RED, vis=(1,),
                         wear="_w1"))
        P.add(grid_sheet(lambda u, v: (-w / 2 + w * u, pole_y + 0.02 - 0.47 * v, 0.03 * v), 1, 1, KAYA, vis=(2,)))
        if state == "loose":                # a corner cord with its iron ring still on the beam hook
            P.adds(hook_iron(w / 2 + 0.20, 0.0, drop=0.05))
            P.add(cord((w / 2 + 0.20, -0.05, 0.02), (w / 2 + 0.15, -0.45, 0.04), 0.004))
            P.add(box(w / 2 + 0.13, w / 2 + 0.17, -0.49, -0.45, 0.02, 0.06, IRON, vis=(1,)))
    else:                                   # 'bundle': folded and tied, hung from a hook in its cords
        P.adds(hook_iron(0.0, 0.0, drop=0.05))
        bw, bd, bh = 0.55, 0.30, 0.14
        body = lkit.soft_slab(bw, bd, bh, KAYA, n=3, vis=(1,))
        body = xf(body, rx=90.0, t=(0.0, -0.10 - bd / 2 - 0.05, 0.0))     # folded bundle standing on its long edge
        P.add(body)
        bot = min(v[1] for v in body.verts)
        for sx in (-0.15, 0.15):
            P.add(cord((0.0, -0.05, 0.0), (sx, bot + bd + 0.02, 0.0), 0.004))
            P.add(box(sx - 0.006, sx + 0.006, bot - 0.004, bot + bd + 0.03, -bh / 2 - 0.006, bh / 2 + 0.006, ROPE,
                      vis=(1,)))
        P.add(box(-bw / 2, bw / 2, bot, bot + bd, -bh / 2, bh / 2, KAYA, vis=(2,)))
        P.add(box(-bw / 2 + 0.02, bw / 2 - 0.02, bot - 0.003, bot + 0.03, -bh / 2 - 0.003, bh / 2 + 0.003, RED,
                  vis=(1,)))
    P.finish_hang()
    P.dim("pole_w", 0.80, w, tol=0.005)
    P.notes.append("mosquito net (kaya) folded away for autumn (LIFE_LAYER_ERA 13: kept, T2-3): Omi green hemp with "
                   "a red edge (material jp_m_textile_kaya added by L1)")
    return P


# ================================================================================================ 14 fire gear
def fire_bucket(wear=None, mark="mark_marudai", vis=(1,)):
    """A wooden fire bucket (d 0.26, h 0.25, bail ears), the house mark on its side (B1's atlas)."""
    import props_wood as PW                 # B3b (read-only): the hand bucket
    ss = PW.teoke(wear=wear, vis=vis, lod2=True, fill=0.05)
    h = 0.10 if mark == "mark_marudai" else 0.17
    ss.append(text((0.0, 0.13, 0.126), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), h, SUMI, mark, wear="_w1", off=0.004,
                   vis=vis))
    return ss


def fire_gear(state="full"):
    P = wallpart("fire_gear", 6.0)
    shelf_y = 1.62
    w = 0.95
    if state in ("full", "ab"):
        P.add(board(-w / 2, w / 2, shelf_y - 0.025, shelf_y, 0.0, 0.30, k=4, vis=(1, 2)))
        for sx in (-1, 1):
            P.add(W(sx * (w / 2 - 0.08) - 0.02, sx * (w / 2 - 0.08) + 0.02, shelf_y - 0.24, shelf_y - 0.025, 0.0,
                    0.03, vis=(1,)))
            P.add(xf(W(-0.015, 0.015, -0.02, 0.02, -0.14, 0.14, vis=(1,)), rx=-45.0,
                     t=(sx * (w / 2 - 0.08), shelf_y - 0.12, 0.12)))
        xs = [-0.30, 0.0, 0.30]
        for i, x in enumerate(xs):
            if state == "ab" and i == 2:
                continue
            P.adds(xfs(fire_bucket(wear="_w2" if state == "ab" else None), t=(x, shelf_y, 0.15)))
        # the fire hook (tobiguchi) on two pegs under the shelf
        hy = 1.30
        for x in (-0.35, 0.35):
            P.add(peg(x, hy, z0=0.0, L=0.10))
        a = 0.0 if state == "full" else -24.0
        hook = [pole((-0.75, 0.0, 0.0), (0.75, 0.0, 0.0), 0.017, WEATH, n=5, vis=(1, 2)),
                prism([(0.75, -0.01), (0.84, 0.0), (0.86, -0.07), (0.83, -0.06), (0.80, 0.01)], "z", -0.006, 0.006,
                      IRON, vis=(1,))]
        P.adds(xfs(hook, rz=a, pivot=(-0.35, 0.0, 0.0), t=(0.0, hy + 0.03, 0.07)))
        if state == "ab":                   # as left: a bucket rolled off onto the floor
            P.adds(rest(xfs(fire_bucket(wear="_w2"), rx=90.0, ry=60.0, t=(0.45, 0.0, 0.45)), 0.0))
            P.add(stain(105, 0.40, 0.50, 0.30, sx=1.5))
    else:                                   # 'buckets': two buckets hung by their bails on pegs
        for x in (-0.18, 0.18):
            P.add(peg(x, 1.70, z0=0.0, L=0.10))
            P.adds(xfs(fire_bucket(mark="oke_hinoyojin" if x < 0 else "mark_marudai"), t=(x, 1.70 - 0.44, 0.14)))
    P.dim("shelf_y" if state != "buckets" else "peg_y", shelf_y if state != "buckets" else 1.70,
          shelf_y if state != "buckets" else 1.70, tol=0.005)
    P.notes.append("town fire rules (Kyoho 1718-20): fire buckets with the house mark and a fire hook (BUILDING_LIST "
                   "5.6: 20 entries); visual only (no loot on the bucket shelf: it is above 1.40 over most floors)")
    return P


# ================================================================================================ registry
PROPS = [
    {"id": "jp_f_mino_pegs", "cat": CAT, "ll": 1, "mount": "wall", "tiers": [1, 2], "refs": ["i06_tsunashima_doma"],
     "notes": ["★ BUILD_LIST jp_f_mino_pegs; visual only, no loot"], "models": [
        M("jp_f_mino_pegs", "full", "intact", "Wall pegs: straw raincoat, hat, hoe, sickle", lambda: mino_pegs("full")),
        M("jp_f_mino_pegs_rain", "rain", "intact", "Wall pegs: straw raincoat and hat", lambda: mino_pegs("rain")),
        M("jp_f_mino_pegs_fallen", "full", "fallen", "Wall pegs, the hat fallen, one peg empty",
          lambda: mino_pegs("fallen")),
    ]},
    {"id": "jp_f_ofuda", "cat": CAT, "ll": 2, "mount": "post", "tiers": [1, 2, 3], "refs": [],
     "notes": ["paper charms on a post: Ise taima, Akiba fire charm, Somin Shorai, Goo hoin (life atlas)"], "models": [
        M("jp_f_ofuda_single", "single", "intact", "Paper charm (Ise taima) on a post", lambda: ofuda("single")),
        M("jp_f_ofuda_akiba", "akiba", "intact", "Fire charm (Akiba) on a kitchen post", lambda: ofuda("akiba")),
        M("jp_f_ofuda_row", "row", "intact", "Three paper charms on a post, old and new", lambda: ofuda("row")),
        M("jp_f_ofuda_torn", "row", "torn", "Paper charms, faded, one peeling, one torn away", lambda: ofuda("torn")),
    ]},
    {"id": "jp_f_koyomi", "cat": CAT, "ll": 3, "mount": "wall", "tiers": [2, 3], "refs": [],
     "notes": ["the printed calendar for Kyoho 15 (1730)"], "models": [
        M("jp_f_koyomi", "sheet", "intact", "Printed calendar (Kyoho 15) on the wall", lambda: koyomi("std")),
        M("jp_f_koyomi_curled", "sheet", "curled", "Calendar, faded, a corner curling off", lambda: koyomi("curled")),
    ]},
    {"id": "jp_f_utensil_board", "cat": CAT, "ll": 4, "mount": "wall", "tiers": [1, 2, 3],
     "refs": ["i32_morse_city_kitchen", "i08_edo_nagaya_kitchen"], "models": [
        M("jp_f_utensil_board", "full", "intact", "Kitchen utensil board: dipper, paddle, ladles, knives, board",
          lambda: utensil_board("full")),
        M("jp_f_utensil_board_small", "small", "intact", "Small utensil board", lambda: utensil_board("small")),
        M("jp_f_utensil_board_fallen", "full", "fallen", "Utensil board, board and ladle on the floor",
          lambda: utensil_board("fallen")),
    ]},
    {"id": "jp_f_tool_wall", "cat": CAT, "ll": 5, "mount": "wall", "tiers": [1, 2], "refs": ["i16_moronobu_1685_p6"],
     "models": [
        M("jp_f_tool_wall", "full", "intact", "Tool wall: saw, adze, axe, hatchet", lambda: tool_wall("full")),
        M("jp_f_tool_wall_wood", "wood", "intact", "Tool wall: axes, saw, hatchet", lambda: tool_wall("wood")),
        M("jp_f_tool_wall_taken", "full", "taken", "Tool wall, axe taken, saw on the floor", lambda: tool_wall("taken")),
    ]},
    {"id": "jp_f_rope_pegs", "cat": CAT, "ll": 6, "mount": "wall", "tiers": [1, 2], "refs": [], "models": [
        M("jp_f_rope_pegs_2", "2", "intact", "Two rope coils on pegs", lambda: rope_pegs("2")),
        M("jp_f_rope_pegs_3", "3", "intact", "Three rope coils on pegs", lambda: rope_pegs("3")),
        M("jp_f_rope_pegs_fallen", "2", "fallen", "Rope coils, one fallen and paid out", lambda: rope_pegs("fallen")),
    ]},
    {"id": "jp_f_sandals_hung", "cat": CAT, "ll": 7, "mount": "wall", "tiers": [1, 2], "refs": [], "models": [
        M("jp_f_sandals_hung_wall", "wall", "intact", "Straw sandals in bunches on wall pegs",
          lambda: sandals_hung("wall")),
        M("jp_f_sandals_hung_beam", "beam", "intact", "A bunch of straw sandals on a beam hook",
          lambda: sandals_hung("beam"), mount="beam"),
        M("jp_f_sandals_hung_fallen", "wall", "fallen", "Straw sandals, one bunch burst on the floor",
          lambda: sandals_hung("fallen")),
    ]},
    {"id": "jp_f_hoshigaki", "cat": CAT, "ll": 8, "mount": "beam", "tiers": [1, 2], "refs": ["k35_firewood_hoshigaki"],
     "notes": ["autumn"], "models": [
        M("jp_f_hoshigaki_3", "3", "intact", "Dried persimmons, three strings", lambda: hoshigaki("3")),
        M("jp_f_hoshigaki_5", "5", "intact", "Dried persimmons, five strings", lambda: hoshigaki("5")),
        M("jp_f_hoshigaki_rotten", "3", "rotten", "Dried persimmons, blackened, gaps, a broken string",
          lambda: hoshigaki("ab")),
    ]},
    {"id": "jp_f_drying", "cat": CAT, "ll": 9, "mount": "beam", "tiers": [1, 2], "refs": [], "notes": ["autumn"],
     "models": [
        M("jp_f_drying_daikon", "daikon", "intact", "Radishes drying on a pole", lambda: drying("daikon")),
        M("jp_f_drying_chilli", "chilli", "intact", "Chilli strings drying", lambda: drying("chilli")),
        M("jp_f_drying_fish", "fish", "intact", "Small fish drying on straws", lambda: drying("fish")),
        M("jp_f_drying_daikon_shrivelled", "daikon", "shrivelled", "Radishes shrivelled, two fallen",
          lambda: drying("daikon_ab")),
    ]},
    {"id": "jp_f_chochin", "cat": CAT, "ll": 10, "mount": "beam", "tiers": [2, 3], "refs": [],
     "notes": ["unlit; crest / shop name from the life atlas"], "models": [
        M("jp_f_chochin_crest", "crest", "intact", "Paper lantern with a family crest", lambda: chochin_model("crest")),
        M("jp_f_chochin_crest2", "crest2", "intact", "Paper lantern, three-bar crest", lambda: chochin_model("crest2")),
        M("jp_f_chochin_shop", "shop", "intact", "Paper lantern, shop name Iseya", lambda: chochin_model("shop")),
        M("jp_f_chochin_shop2", "shop2", "intact", "Paper lantern, shop name Yamatoya", lambda: chochin_model("shop2")),
        M("jp_f_chochin_torn", "shop", "torn", "Paper lantern, torn, hanging askew", lambda: chochin_model("torn")),
        M("jp_f_chochin_fallen", "crest", "fallen", "Paper lantern fallen and crushed", lambda: chochin_model("fallen"),
          mount="floor"),
    ]},
    {"id": "jp_f_bangasa", "cat": CAT, "ll": 11, "mount": "wall", "tiers": [2, 3], "refs": [], "models": [
        M("jp_f_bangasa_hung", "hung", "intact", "Oiled-paper umbrella hung on a peg", lambda: bangasa("hung")),
        M("jp_f_bangasa_leaning", "leaning", "intact", "Oiled-paper umbrella leaning on the wall",
          lambda: bangasa("leaning")),
        M("jp_f_bangasa_open_torn", "open", "torn", "Umbrella dropped open, paper split", lambda: bangasa("open_torn"),
          mount="floor"),
    ]},
    {"id": "jp_f_noren_inner", "cat": CAT, "ll": 12, "mount": "doorway", "tiers": [2, 3], "refs": [], "models": [
        M("jp_f_noren_inner_2", "2", "intact", "Inner noren, two panels (0.88)", lambda: noren_inner("2")),
        M("jp_f_noren_inner_3", "3", "intact", "Inner noren, three panels (1.32)", lambda: noren_inner("3")),
        M("jp_f_noren_inner_torn", "2", "torn", "Inner noren, a panel torn off", lambda: noren_inner("torn")),
    ]},
    {"id": "jp_f_kaya", "cat": CAT, "ll": 13, "mount": "beam", "tiers": [2, 3], "refs": [],
     "notes": ["era check kept (LIFE_LAYER_ERA 13); folded away for autumn"], "models": [
        M("jp_f_kaya_draped", "draped", "intact", "Mosquito net folded over a pole", lambda: kaya("draped")),
        M("jp_f_kaya_bundle", "bundle", "intact", "Mosquito net tied in a bundle on a hook", lambda: kaya("bundle")),
        M("jp_f_kaya_loose", "draped", "loose", "Mosquito net come loose, hanging in a swag", lambda: kaya("loose")),
    ]},
    {"id": "jp_f_fire_gear", "cat": CAT, "ll": 14, "mount": "wall", "tiers": [2, 3], "refs": [], "models": [
        M("jp_f_fire_gear", "full", "intact", "Fire buckets on a shelf, fire hook on pegs", lambda: fire_gear("full")),
        M("jp_f_fire_gear_buckets", "buckets", "intact", "Two fire buckets hung on pegs", lambda: fire_gear("buckets")),
        M("jp_f_fire_gear_fallen", "full", "fallen", "Fire gear, a bucket on the floor, the hook askew",
          lambda: fire_gear("ab")),
    ]},
]
