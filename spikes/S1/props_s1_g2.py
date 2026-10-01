"""S1 group 2 (research/interior/SHOP_SETS.md 2a, trades 6-10): paper and brushes, oil and candles, charcoal and
firewood (reuse only), tobacco, travel goods and souvenirs."""
import math
import random

from s1kit import (box, lathe, xf, xfs, W, col, col_solid, board, pole, cord, stext, rest, lod_box, wear_all, stain,
                   jug, packet, tray, kanban_prop, kanban_parts, finish_goods, SP, M, SHOP, SUMI, WOOD, WEATH, IRON,
                   DARK, PALE, LACQ, BAMBOO, WEAVE, MUSHIRO, STACK, ROPE, PAPER, CHOCHIN, INDIGO, KINARI, LITTER,
                   LEATHER, ARM_Y, ARM_L)
import fkit
import props_shop as B3SHOP          # B3a (read-only): straw sandals
from props_s1_g1 import two, ERA_BTI

G = "shopgoods"
F = "shopfit"
S = "shopsign"


# ================================================================================================ goods
def brush(x, y, z, L=0.22, wear=None):
    """A writing brush hanging tip down: a bamboo shaft and a dark hair tip."""
    return wear_all([pole((x, y, z), (x, y - L, z), 0.005, BAMBOO, n=4),
                     xf(lathe([(0.0, y - L - 0.035), (0.007, y - L - 0.01), (0.006, y - L), (0.0, y - L)], 5, LACQ,
                              vis=(1,)), t=(x, 0.0, z))], wear)


def sg_brushes(state="intact"):
    """A small brush rack (two posts, a bar, eight brushes hanging), boxes of ink sticks, a paper ream."""
    P = SP("sg_brushes", flat=True, mass=1.5)
    if state == "intact":
        for x in (-0.25, 0.05):
            P.add(W(x - 0.01, x + 0.01, 0.0, 0.30, -0.01, 0.01, WOOD, vis=(1,)))
        P.add(W(-0.25, 0.05, 0.0, 0.015, -0.05, 0.05, WOOD, vis=(1,)))
        P.add(W(-0.26, 0.06, 0.28, 0.30, -0.012, 0.012, WOOD, vis=(1,)))
        for k in range(8):
            P.adds(brush(-0.225 + 0.036 * k, 0.28, 0.0, L=0.15 + 0.01 * (k % 3)))
        for k in range(2):
            P.add(W(0.10, 0.24, 0.035 * k, 0.035 * k + 0.03, -0.06, 0.06, LACQ, vis=(1,)))
        P.add(W(0.12, 0.26, 0.07, 0.10, -0.08, 0.08, PAPER, vis=(1,)))
    else:
        P.add(rest([xf(W(-0.15, 0.15, 0.0, 0.015, -0.05, 0.05, WOOD, vis=(1,)), rx=90.0)])[0])
        r = random.Random(31)
        for k in range(5):
            P.add(xf(pole((0.0, 0.006, -0.10), (0.0, 0.006, 0.10), 0.005, BAMBOO, n=4), ry=r.uniform(0, 180),
                     t=(r.uniform(-0.25, 0.25), 0.0, r.uniform(0.0, 0.18))))
        P.add(stain(32, 0.15, 0.10, 0.10, mat=LITTER))
    return finish_goods(P, WOOD)


def sg_oil(state="intact"):
    """Oil jugs (stoneware), a wooden funnel and the ladle on a tray; ab: a jug over, an oil stain."""
    P = SP("sg_oil", flat=True, mass=4.0)
    if state == "intact":
        for k, x in enumerate((-0.20, -0.08)):
            P.add(jug(x, 0.0, 0.055, 0.22, DARK))
        P.add(jug(0.03, 0.02, 0.045, 0.17, PALE))
        P.adds(tray(0.17, 0.0, 0.18, 0.16, WOOD))
        P.add(xf(lathe([(0.008, 0.025), (0.06, 0.09), (0.055, 0.09), (0.004, 0.03), (0.008, 0.025)], 7, WOOD,
                       vis=(1,)), t=(0.13, 0.0, -0.02)))
        P.add(xf(lathe([(0.0, 0.006), (0.035, 0.006), (0.035, 0.05), (0.031, 0.05), (0.0, 0.01)], 6, WOOD, vis=(1,)),
                 t=(0.21, 0.0, 0.03)))
        P.add(pole((0.21, 0.04, 0.03), (0.30, 0.03, -0.10), 0.006, WOOD, n=4))
    else:
        P.add(jug(-0.20, 0.0, 0.055, 0.22, DARK, wear="_w2"))
        P.add(rest([xf(jug(0.0, 0.0, 0.055, 0.22, DARK, wear="_w2"), rx=90.0, ry=30.0)])[0])
        P.solids[-1] = xf(P.solids[-1], t=(0.02, 0.0, 0.06))
        P.add(stain(41, 0.18, 0.12, 0.14, sx=1.6, mat=LITTER))
    return finish_goods(P, DARK)


def candle(x, z, h, r, y0=0.0, wear=None):
    """A Japanese candle: slightly flared to the top, the wick showing (paper-white wax)."""
    return wear_all([xf(lathe([(0.0, y0), (r * 0.8, y0), (r, y0 + h), (r * 0.4, y0 + h), (0.0, y0 + h)], 6, PAPER,
                              vis=(1,)), t=(x, 0.0, z)),
                     box(x - 0.0015, x + 0.0015, y0 + h, y0 + h + 0.012, z - 0.0015, z + 0.0015, LACQ, vis=(1,))],
                    wear)


def sg_candles(state="intact"):
    """Candles by size standing in a tray, bundles of small ones tied in paper, a lidded box."""
    P = SP("sg_candles", flat=True, mass=2.0)
    if state == "intact":
        P.adds(tray(-0.14, 0.0, 0.26, 0.16, WOOD))
        for k, (h, r) in enumerate(((0.20, 0.016), (0.17, 0.014), (0.14, 0.012), (0.11, 0.010))):
            for j in range(2):
                P.adds(candle(-0.23 + 0.06 * k, -0.035 + 0.07 * j, h, r, y0=0.006))
        for j in range(2):
            P.add(W(0.02, 0.17, 0.03 * j, 0.03 * j + 0.03, -0.06, 0.06, PAPER, vis=(1,)))
            P.add(W(0.09, 0.10, 0.03 * j, 0.03 * j + 0.031, -0.061, 0.061, ROPE, vis=(1,)))
        P.add(W(0.19, 0.29, 0.0, 0.06, -0.06, 0.06, WOOD, vis=(1,)))
    else:
        r = random.Random(42)
        P.adds(tray(-0.14, 0.0, 0.26, 0.16, WOOD, wear="_w2"))
        for k in range(7):
            ss = candle(0.0, 0.0, r.uniform(0.10, 0.20), 0.013, wear="_w2")
            ss = [xf(s, rz=90.0, ry=r.uniform(0, 180), t=(r.uniform(-0.25, 0.25), 0.013, r.uniform(0.02, 0.2)))
                  for s in ss]
            P.adds(ss)
    return finish_goods(P, PAPER)


def kiseru(x, z, L=0.30, y0=0.0, ry=0.0, wear=None):
    """A tobacco pipe lying flat: iron bowl and mouthpiece, a bamboo stem (rao)."""
    out = [pole((-L / 2 + 0.04, y0 + 0.006, 0.0), (L / 2 - 0.03, y0 + 0.006, 0.0), 0.004, BAMBOO, n=4),
           box(-L / 2, -L / 2 + 0.045, y0, y0 + 0.012, -0.005, 0.005, IRON, vis=(1,)),
           box(-L / 2, -L / 2 + 0.012, y0, y0 + 0.022, -0.008, 0.008, IRON, vis=(1,)),
           box(L / 2 - 0.035, L / 2, y0 + 0.002, y0 + 0.01, -0.004, 0.004, IRON, vis=(1,))]
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in wear_all(out, wear)]


def sg_tobacco(state="intact"):
    """Cut tobacco in labelled paper packets (stacked), pipes on a tray, a tied bundle of leaf."""
    P = SP("sg_tobacco", flat=True, mass=1.5)
    if state == "intact":
        for k in range(3):
            for j in range(2):
                P.add(packet(-0.20 + 0.075 * j, -0.02, 0.065, 0.10, 0.022, PAPER, y0=0.022 * k))
        P.add(stext((-0.20, 0.066, -0.02), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), 0.07, "pkt_kizami", off=0.0012))
        P.adds(tray(0.07, 0.0, 0.18, 0.16, LACQ))
        for k in range(3):
            P.adds(kiseru(0.07, -0.05 + 0.05 * k, L=0.17, y0=0.006, ry=5.0 * k))
        P.add(xf(fkit.lcyl("x", 0.03, 0.0, 0.03, -0.09, 0.09, LEATHER, n=6, vis=(1,)), ry=70.0, t=(0.24, 0.0, 0.02)))
        P.add(xf(W(-0.005, 0.005, 0.0, 0.062, -0.035, 0.035, ROPE, vis=(1,)), ry=70.0, t=(0.24, 0.0, 0.02)))
    else:
        r = random.Random(51)
        for k in range(5):
            P.add(packet(r.uniform(-0.25, 0.15), r.uniform(0.0, 0.18), 0.065, 0.10, 0.02, PAPER, ry=r.uniform(0, 180),
                         wear="_w2"))
        P.adds(kiseru(0.15, 0.10, L=0.17, ry=40.0, wear="_w2"))
        P.add(xf(W(-0.10, 0.10, 0.0, 0.004, -0.06, 0.06, LEATHER, vis=(1,)), ry=20.0, t=(0.05, 0.0, -0.02)))
    return finish_goods(P, PAPER)


def kasa(x, z, r=0.20, h=0.10, y0=0.0, wear=None, tilt=0.0):
    """A sedge travel hat (sugegasa), a shallow cone, lying crown up."""
    s = lathe([(0.0, y0 + h), (r * 0.15, y0 + h * 0.9), (r, y0), (r - 0.01, y0), (0.0, y0 + h - 0.01)], 8, MUSHIRO,
              vis=(1,), wear=wear)
    return xf(s, rz=tilt, t=(x, 0.0, z))


def sg_travel(state="intact"):
    """Travel goods: two bunches of straw sandals (waraji) tied, a stack of sedge hats, a cloth pouch."""
    P = SP("sg_travel", flat=True, mass=1.5)
    if state == "intact":
        for j in range(3):
            P.adds(xfs(B3SHOP.sandals(), ry=90.0 + 4.0 * j, t=(-0.20, 0.018 * j, 0.0)))
            P.adds(xfs(B3SHOP.sandals(), ry=90.0 - 3.0 * j, t=(-0.07, 0.018 * j, 0.0)))
        for j in range(3):
            P.add(kasa(0.13, 0.0, r=0.14, h=0.07, y0=0.012 * j))
    else:
        r = random.Random(61)
        for j in range(3):
            P.adds(xfs(B3SHOP.sandals("_w2"), ry=r.uniform(0, 180), t=(r.uniform(-0.25, 0.1), 0.0, r.uniform(0, 0.2))))
        P.add(xf(kasa(0.0, 0.0, r=0.14, h=0.07, wear="_w2"), rx=150.0, t=(0.15, 0.07, 0.08)))
    return finish_goods(P, MUSHIRO)


def odawara(x, z, h=0.20, r=0.045, y0=0.0, folded=True, wear=None):
    """An Odawara travel lantern: a paper cylinder between lacquered top and bottom caps; folded = flattened to a
    short drum (the caps nest together)."""
    hh = 0.05 if folded else h
    out = [xf(lathe([(0.0, y0), (r + 0.004, y0), (r + 0.004, y0 + 0.012), (0.0, y0 + 0.012)], 6, LACQ, vis=(1,)),
              t=(x, 0.0, z)),
           xf(lathe([(r, y0 + 0.012), (r * 1.06, y0 + 0.012 + (hh - 0.024) / 2), (r, y0 + hh - 0.012),
                     (r - 0.003, y0 + hh - 0.012), (r - 0.003, y0 + 0.012), (r, y0 + 0.012)], 6, CHOCHIN, vis=(1,)),
              t=(x, 0.0, z)),
           xf(lathe([(0.0, y0 + hh - 0.012), (r + 0.004, y0 + hh - 0.012), (r + 0.004, y0 + hh), (0.0, y0 + hh)], 6,
                    LACQ, vis=(1,)), t=(x, 0.0, z))]
    return wear_all(out, wear)


def sg_odawara(state="intact"):
    """Odawara lanterns (folded, three in a row, one opened) - the travellers' lantern sold on the Tokaido."""
    P = SP("sg_odawara", flat=True, mass=1.0)
    if state == "intact":
        for k in range(3):
            P.adds(odawara(-0.20 + 0.10 * k, 0.0, folded=True))
        P.adds(odawara(0.18, 0.0, h=0.22, folded=False))
    else:
        r = random.Random(71)
        for k in range(3):
            ss = odawara(0.0, 0.0, folded=k != 1, h=0.22, wear="_w2")
            P.adds(rest([xf(s, rz=90.0, ry=r.uniform(0, 180), t=(r.uniform(-0.2, 0.2), 0.05, r.uniform(0, 0.15)))
                         for s in ss]))
    return finish_goods(P, CHOCHIN)


# ================================================================================================ fittings
def tobacco_cutter(state="intact"):
    """The tobacco cutter's bench: a low board (0.80 x 0.35 x 0.25), the leaf pressed in a clamp (two blocks and a
    wedge), the big knife (kizami-bocho) pivoted at the far end; leaf shreds on the board. ab: knife gone, shreds and
    leaf scattered on the floor."""
    P = SP("tobacco_cutter", budget="small", mass=14.0)
    w, d, h = 0.80, 0.35, 0.25
    P.add(board(-w / 2, w / 2, h - 0.04, h, -d / 2, d / 2, k=2, vis=(1, 2)))
    for x in (-w / 2 + 0.05, w / 2 - 0.05):
        P.add(board(x - 0.025, x + 0.025, 0.0, h - 0.04, -d / 2 + 0.02, d / 2 - 0.02, k=5, vis=(1, 2)))
    for x in (-0.12, 0.04):                                                      # clamp blocks + the pressed leaf
        P.add(W(x - 0.03, x + 0.03, h, h + 0.10, -0.10, 0.10, WOOD, vis=(1,)))
    P.add(W(-0.09, 0.01, h, h + 0.06, -0.08, 0.08, LEATHER, vis=(1,)))
    P.add(W(-0.11, 0.03, h + 0.10, h + 0.12, -0.03, 0.03, WEATH, vis=(1,)))      # the wedge bar
    if state == "intact":
        P.add(W(0.06, 0.36, h + 0.025, h + 0.03, -0.035, 0.035, IRON, vis=(1,)))   # the blade lying down
        P.add(W(0.30, 0.38, h + 0.02, h + 0.05, -0.015, 0.015, WOOD, vis=(1,)))
        P.add(W(0.33, 0.37, h, h + 0.03, -0.02, 0.02, IRON, vis=(1,)))             # its pivot
        P.add(W(-0.35, -0.16, h, h + 0.006, -0.12, 0.12, LEATHER, vis=(1,)))       # shreds
    else:
        P.add(stain(81, 0.0, 0.40, 0.30, sx=1.8, mat=LITTER))
        r = random.Random(82)
        for k in range(4):
            P.add(xf(W(-0.06, 0.06, 0.0, 0.004, -0.04, 0.04, LEATHER, vis=(1,)), ry=r.uniform(0, 180),
                     t=(r.uniform(-0.4, 0.4), 0.0, r.uniform(0.25, 0.55))))
    c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
    P.add(c)
    P.add(col(-0.15, 0.07, h, h + 0.12, -0.10, 0.10))
    fkit.road_tops(P, [c], "boards")
    P.loot_rect("bench", h, 0.08, 0.36, -0.15, 0.15, rng=0.15, points=[(0.22, h, 0.10)])
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("w", w, w)
    P.notes.append("hand cutting only (machine cutting is later, general); BTI 936-937")
    return P


def print_line(kind="otsue", state="intact"):
    """Pictures hung on a cord between two pegs on a wall (wall plane z = 0, the cord 1.55 up): Otsu-e (travel goods),
    printed pages (bookshop), fans and a small landscape (painter). ab: one sheet gone, one hanging by a corner,
    faded."""
    P = SP("print_line", flat=True, anchor="wall", mass=0.5)
    ab = state != "intact"
    yc, L = 1.55, 1.40
    for x in (-L / 2, L / 2):
        P.add(pole((x, yc, 0.002), (x, yc + 0.02, 0.07), 0.01, WOOD, n=5, vis=(1,)))
    P.add(cord((-L / 2, yc + 0.01, 0.05), (L / 2, yc + 0.01, 0.05), 0.003))
    cells = {"otsue": ["pic_otsue", "pic_otsue", "pic_otsue"], "books": ["pic_page", "pic_page", "pic_page"],
             "fans": ["pic_fan", "pic_scroll", "pic_fan"]}[kind]
    xs = (-0.42, 0.0, 0.42)
    for k, (x, cn) in enumerate(zip(xs, cells)):
        if ab and k == 1:
            continue
        import skit
        cw, ch = skit.cell_size(SHOP, cn)
        h = 0.36 if kind != "fans" or cn == "pic_scroll" else 0.22
        w = h * cw / ch
        sheet = [W(x - w / 2 - 0.01, x + w / 2 + 0.01, yc - h - 0.02, yc, 0.046, 0.049, PAPER, vis=(1,)),
                 box(x - 0.012, x + 0.012, yc - 0.01, yc + 0.02, 0.044, 0.056, WOOD, vis=(1,))]
        tx = stext((x, yc - 0.01 - h / 2, 0.049), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), h, cn, wear="_w2" if ab else None,
                   off=0.0015, width=w)
        sheet.append(tx)
        if ab and k == 2:
            sheet = [xf(s, rz=-35.0, pivot=(x - w / 2, yc, 0.0)) for s in sheet]
        P.adds(sheet)
    P.add(lod_box([s for s in P.solids if 1 in s.vis and not getattr(s, "_text_faced", False)], PAPER, vis=(2,)))
    P.dim("cord_L", L, L)
    P.notes.append("wall item (visual): pictures on a cord, ink only (no colour prints before 1744)")
    return P


def shape_pipe(state="intact"):
    """Shape sign: a giant tobacco pipe (1.20 m) hung from a bracket under the eave (facade plane z = 0)."""
    P = SP("shape_pipe", flat=True, anchor="wall", mass=6.0)
    ab = state != "intact"
    out, _, c = kanban_parts("kanban_tabako", SUMI)
    P.adds(out)
    y = ARM_Y - 0.25
    z = 0.03 + ARM_L / 2 + 0.02
    z = 0.03 + ARM_L - 0.06                                  # hung under the arm's end, parallel to the facade
    pipe = [pole((-0.48, y, z), (0.45, y, z), 0.035, BAMBOO, n=6, vis=(1, 2)),
            box(-0.62, -0.48, y - 0.05, y + 0.12, z - 0.05, z + 0.05, IRON, vis=(1, 2)),
            box(-0.61, -0.49, y + 0.06, y + 0.12, z - 0.045, z + 0.045, LACQ, vis=(1,)),
            box(0.45, 0.60, y - 0.03, y + 0.03, z - 0.03, z + 0.03, IRON, vis=(1, 2))]
    for dx in (-0.30, 0.30):
        pipe.append(cord((0.0, ARM_Y, z), (dx, y + 0.035, z), 0.004))
    if ab:
        pipe = [xf(s, rz=25.0, pivot=(0.0, ARM_Y, z)) for s in wear_all(pipe, "_w2")]
    P.adds(pipe)
    P.add(lod_box([s for s in P.solids if 1 in s.vis], BAMBOO, vis=(2,)))
    P.dim("pipe_L", 1.22, 1.22)
    P.notes.append("the giant-pipe shop sign (BTI 487 'three-dimensional signs (a giant pipe...)')")
    P.extra["hang_y"] = ARM_Y + 0.05
    return P


# ================================================================================================ registry
PROPS = [
    two("jp_f_sg_brushes", G, ["kamiya"], ERA_BTI % "BTI 928-929, 519-521", "surface", sg_brushes,
        ("jp_f_sg_brushes", "jp_f_sg_brushes_scattered"), ("Goods: brush rack, ink sticks, paper",
                                                           "Goods: brush rack down, brushes scattered, ink")),
    two("jp_f_sg_oil", G, ["abura"], ERA_BTI % "BTI 930-932", "surface", sg_oil,
        ("jp_f_sg_oil", "jp_f_sg_oil_spilled"), ("Goods: oil jugs, funnel, ladle", "Goods: oil jug over, stain")),
    two("jp_f_sg_candles", G, ["abura", "butsugu"], ERA_BTI % "BTI 540-542, 933", "surface", sg_candles,
        ("jp_f_sg_candles", "jp_f_sg_candles_scattered"), ("Goods: candles by size, bundles, a box",
                                                           "Goods: candles scattered")),
    two("jp_f_sg_tobacco", G, ["tabako"], ERA_BTI % "BTI 936-938", "surface", sg_tobacco,
        ("jp_f_sg_tobacco", "jp_f_sg_tobacco_scattered"), ("Goods: tobacco packets, pipes, leaf",
                                                           "Goods: packets scattered, leaf")),
    two("jp_f_sg_travel", G, ["tabidogu"], ERA_BTI % "BTI 942-943", "surface", sg_travel,
        ("jp_f_sg_travel", "jp_f_sg_travel_scattered"), ("Goods: straw sandals, sedge hats",
                                                         "Goods: sandals and a hat scattered")),
    two("jp_f_sg_odawara", G, ["tabidogu"], ERA_BTI % "BTI 497-499 (founding date uncertain, early 18th c.: kept, "
                                                      "flagged)", "surface", sg_odawara,
        ("jp_f_sg_odawara", "jp_f_sg_odawara_crushed"), ("Goods: Odawara lanterns", "Goods: lanterns crushed")),
    two("jp_f_tobacco_cutter", F, ["tabako"], ERA_BTI % "BTI 936-937 (hand knife only)", "floor", tobacco_cutter,
        ("jp_f_tobacco_cutter", "jp_f_tobacco_cutter_bare"), ("Tobacco-cutting bench with clamp and knife",
                                                              "Tobacco-cutting bench, knife gone, leaf scattered")),
    {"id": "jp_f_print_line", "cat": F, "mount": "wall", "trades": ["tabidogu", "honya", "eshi"],
     "era": ERA_BTI % "BTI 500-512 (ink prints only; benizuri-e 1744 / nishiki-e 1765 later); Otsu-e (general)",
     "models": [
         M("jp_f_print_line_otsue", "otsue", "intact", "Otsu-e pictures on a cord", lambda: print_line("otsue")),
         M("jp_f_print_line_otsue_torn", "otsue", "torn", "Otsu-e on a cord, one gone, one hanging",
           lambda: print_line("otsue", "torn")),
         M("jp_f_print_line_books", "books", "intact", "Printed pages on a cord", lambda: print_line("books")),
         M("jp_f_print_line_books_torn", "books", "torn", "Printed pages on a cord, torn",
           lambda: print_line("books", "torn")),
         M("jp_f_print_line_fans", "fans", "intact", "Fans and a landscape on a cord", lambda: print_line("fans")),
         M("jp_f_print_line_fans_torn", "fans", "torn", "Fans on a cord, one gone", lambda: print_line("fans", "torn")),
     ]},
    {"id": "jp_f_kanban_shape_pipe", "cat": S, "mount": "wall", "trades": ["tabako"],
     "era": ERA_BTI % "BTI 487 (the giant-pipe sign)", "models": [
         M("jp_f_kanban_shape_pipe", "pipe", "intact", "Shape sign: giant tobacco pipe", lambda: shape_pipe()),
         M("jp_f_kanban_shape_pipe_askew", "pipe", "askew", "Shape sign: giant pipe hanging askew",
           lambda: shape_pipe("askew"))]},
    kanban_prop("hitsuboku", "kanban_hitsuboku", "brushes and ink (hitsuboku)", ["kamiya"]),
    kanban_prop("abura", "kanban_abura", "lamp oil (abura)", ["abura"]),
    kanban_prop("rousoku", "kanban_rousoku", "candles (rousoku)", ["abura", "butsugu"]),
    kanban_prop("sumimaki", "kanban_sumimaki", "charcoal and firewood (sumi, maki)", ["sumiya"]),
    kanban_prop("tabako", "kanban_tabako", "tobacco (tabako)", ["tabako"], mat=SUMI),
    kanban_prop("tabidogu", "kanban_tabidogu", "travel goods (tabi-dogu)", ["tabidogu"]),
    kanban_prop("otsue", "kanban_otsue", "Otsu pictures (Otsu-e)", ["tabidogu"]),
]
