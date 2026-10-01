"""S1 groups 5-6 (research/interior/SHOP_SETS.md 2d, trades 21-28): leather goods, weaving, sewing, painting,
lacquer, combs, dolls, temple-street crafts."""
import math
import random

from s1kit import (box, lathe, xf, xfs, W, col, board, pole, cord, stext, rest, lod_box, wear_all, stain, jug, ball,
                   bowl, packet, tray, kanban_prop, finish_goods, garment_folded, cyl_col, SP, M, SHOP, WOOD, WEATH,
                   IRON, PALE, DARK, LACQ, BAMBOO, WEAVE, MUSHIRO, STACK, ROPE, PAPER, FUSUMA, INDIGO, KINARI, RED,
                   LITTER, KAKI, SHU, LEATHER, TOFU)
import fkit
import lkit
from props_s1_g1 import two, ERA_BTI

G = "shopgoods"
F = "shopfit"
BOXWOOD = "bamboo_weathered"     # pale yellow-grey: the nearest library colour to boxwood (tsuge) combs


# ================================================================================================ leather
def kinchaku(x, z, r=0.04, h=0.07, mat=LEATHER, wear=None):
    """A drawstring pouch: a bag lathe gathered at the neck, a cord ring."""
    s = lathe([(0.0, 0.0), (r * 0.8, 0.0), (r, h * 0.45), (r * 0.45, h * 0.85), (r * 0.6, h), (0.0, h)], 6, mat,
              vis=(1,), wear=wear)
    return [xf(s, t=(x, 0.0, z))]


def tobacco_case(x, z, ry=0.0, wear=None):
    """A leather tobacco case (tabako-ire) with its pipe-case and a wooden netsuke toggle on the cord."""
    out = [W(-0.05, 0.05, 0.0, 0.025, -0.035, 0.035, LEATHER, vis=(1,)),
           W(-0.12, -0.05, 0.0, 0.02, -0.012, 0.012, LEATHER, vis=(1,)),
           box(0.06, 0.09, 0.0, 0.03, -0.015, 0.015, WOOD, vis=(1,))]
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in wear_all(out, wear)]


def setta(x, z, ry=0.0, wear=None, y0=0.0):
    """A pair of setta: bamboo-sheath uppers on leather soles."""
    out = []
    for dz in (-0.045, 0.045):
        out.append(fkit.prism(fkit.ngon(0.0, dz, 0.04, 8, 0.0, rx=0.115), "y", y0, y0 + 0.008, LEATHER, vis=(1,)))
        out.append(fkit.prism(fkit.ngon(0.0, dz, 0.038, 8, 0.0, rx=0.112), "y", y0 + 0.008, y0 + 0.014, MUSHIRO,
                              vis=(1,)))
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in wear_all(out, wear)]


def sg_pouches(state="intact"):
    """Leather goods: drawstring pouches, tobacco cases with netsuke, a pair of setta."""
    P = SP("sg_pouches", flat=True, mass=1.0)
    if state == "intact":
        for k, x in enumerate((-0.23, -0.15)):
            P.adds(kinchaku(x, 0.0, mat=(LEATHER, INDIGO)[k]))
        for k in range(2):
            P.adds(tobacco_case(-0.02, -0.04 + 0.07 * k, ry=4.0 * k))
        P.adds(setta(0.17, 0.0, ry=90.0))
    else:
        r = random.Random(171)
        P.adds([xf(s, rz=90.0, t=(-0.2, 0.04, 0.05)) for s in kinchaku(0.0, 0.0, wear="_w2")])
        P.adds(tobacco_case(0.05, 0.12, ry=r.uniform(0, 180), wear="_w2"))
        P.adds(setta(0.15, -0.02, ry=40.0, wear="_w2"))
    return finish_goods(P, LEATHER)


def hides(state="intact"):
    """Rolled hides on the floor (three rolls, 0.70 long, tied with straw rope) and one laid flat. ab: unrolled and
    mouldy."""
    P = SP("hides", budget="small", mass=20.0)
    if state == "intact":
        for k, (y, z) in enumerate(((0.084, -0.09), (0.084, 0.09), (0.234, 0.0))):
            P.add(fkit.lcyl("x", y, z, 0.09, -0.35, 0.35, LEATHER, n=8, vis=(1, 2)))
            for xx in (-0.20, 0.20):
                P.add(fkit.lcyl("x", y, z, 0.092, xx - 0.012, xx + 0.012, ROPE, n=8, vis=(1,)))
        P.add(col(-0.35, 0.35, 0.0, 0.167, -0.175, 0.175))
        P.add(col(-0.35, 0.35, 0.167, 0.317, -0.08, 0.08))
        P.loot_rect("top", 0.317, -0.25, 0.25, -0.02, 0.02, rng=0.12, points=[(0.10, 0.317, 0.0)])
    else:
        hd = W(-0.45, 0.45, 0.0, 0.006, -0.32, 0.32, LEATHER, vis=(1,))
        hd.wear = "_w2"
        P.add(xf(hd, ry=12.0))
        roll = fkit.lcyl("x", 0.084, 0.45, 0.09, -0.35, 0.35, LEATHER, n=8, vis=(1,))
        roll.wear = "_w2"
        P.add(roll)
        P.add(col(-0.35, 0.35, 0.0, 0.167, 0.36, 0.54))
        P.loot_rect("hide", 0.006, -0.30, 0.20, -0.20, 0.10, rng=0.15, points=[(-0.05, 0.006, -0.05)])
    P.add(lod_box([s for s in P.solids if 1 in s.vis], LEATHER, vis=(2,)) if state == "intact"
          else W(-0.45, 0.45, 0.0, 0.18, -0.32, 0.54, LEATHER, vis=(2,)))
    P.dim("L", 0.70, 0.70)
    return P


# ================================================================================================ weaving and sewing
def skein(x, z, mat=KINARI, wear=None, R=0.05):
    return [lkit.flat_coil(x, z, R, 0.014, mat=mat, n=8, m=3, wear=wear, sx=0.55)]


def sg_yarn(state="intact"):
    """Yarn: skeins of cotton thread (undyed and indigo), bobbins (bamboo spools) in a shallow basket."""
    P = SP("sg_yarn", flat=True, mass=1.0)
    if state == "intact":
        for k, x in enumerate((-0.22, -0.11, 0.0)):
            P.adds(skein(x, 0.0, mat=(KINARI, INDIGO, KINARI)[k]))
        P.add(xf(lathe([(0.0, 0.0), (0.09, 0.0), (0.10, 0.03), (0.094, 0.03), (0.0, 0.004)], 8, WEAVE, vis=(1,)),
                 t=(0.17, 0.0, 0.0)))
        for k in range(3):
            P.add(fkit.lcyl("x", 0.02, -0.03 + 0.03 * k, 0.012, 0.12, 0.22, (INDIGO, KINARI, INDIGO)[k], n=5,
                            vis=(1,)))
    else:
        r = random.Random(181)
        for k in range(3):
            P.adds(skein(r.uniform(-0.25, 0.15), r.uniform(-0.02, 0.15), mat=(KINARI, INDIGO, KINARI)[k], wear="_w2",
                         R=0.06))
        P.add(xf(lathe([(0.0, 0.0), (0.09, 0.0), (0.10, 0.03), (0.094, 0.03), (0.0, 0.004)], 8, WEAVE, vis=(1,),
                       wear="_w2"), rx=95.0, t=(0.20, 0.10, 0.05)))
    return finish_goods(P, KINARI)


def tailor_board(state="intact"):
    """The tailor's cutting board (tachi-ita, 1.20 x 0.45 on low feet, 0.12 high): indigo cloth laid out, the whale-
    bone rule (kujira-jaku), hand shears, a pin cushion, the small iron (kote) on a hibachi edge. ab: the cloth cut and
    dropped off the board, the shears on the floor."""
    P = SP("tailor_board", budget="small", mass=8.0)
    w, d, h = 1.20, 0.45, 0.12
    P.add(board(-w / 2, w / 2, h - 0.025, h, -d / 2, d / 2, k=4, vis=(1, 2)))
    for x in (-w / 2 + 0.08, w / 2 - 0.08):
        P.add(W(x - 0.03, x + 0.03, 0.0, h - 0.025, -d / 2 + 0.03, d / 2 - 0.03, WOOD, vis=(1, 2)))
    ab = state != "intact"
    if not ab:
        P.add(W(-0.50, 0.20, h, h + 0.006, -0.17, 0.17, INDIGO, vis=(1,)))
        P.add(W(-0.45, 0.15, h + 0.006, h + 0.010, 0.10, 0.125, BAMBOO, vis=(1,)))           # the rule
        P.add(xf(box(-0.06, 0.06, h + 0.006, h + 0.016, -0.008, 0.008, IRON, vis=(1,)), ry=30.0, t=(0.30, 0.0, 0.0)))
        P.add(ball((0.45, h + 0.025, -0.10), 0.03, RED, n=5, sy=0.7))                       # pin cushion
        P.loot_rect("board", h, 0.25, 0.55, -0.20, 0.20, rng=0.12, points=[(0.42, h, 0.10)])
    else:
        cl = W(-0.40, 0.30, 0.0, 0.005, -0.20, 0.20, INDIGO, vis=(1,))
        cl.wear = "_w2"
        P.add(xf(cl, ry=-8.0, t=(0.0, 0.0, d / 2 + 0.25)))
        P.add(xf(box(-0.06, 0.06, 0.0, 0.01, -0.008, 0.008, IRON, vis=(1,)), ry=70.0, t=(0.40, 0.0, d / 2 + 0.30)))
        P.loot_rect("board", h, -0.45, 0.45, -0.18, 0.18, rng=0.15, points=[(-0.2, h, 0.0), (0.25, h, 0.0)])
    c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
    P.add(c)
    fkit.road_tops(P, [c], "boards")
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("w", w, w)
    P.notes.append("tailor's board, rule, shears, pin cushion (BTI 358-360)")
    return P


# ================================================================================================ painting
def paint_mat(state="intact"):
    """The painter's red felt mat (mosen, 1.20 x 0.80) with a sheet on it (an ink landscape in progress), dishes of
    pigment, brushes in a tray, the glue warmer. Visual only (Res 1): the loot lies on the mat. ab: dishes upset,
    the sheet crumpled and stained."""
    P = SP("paint_mat", flat=True, mass=2.0)
    ab = state != "intact"
    felt = W(-0.60, 0.60, 0.0, 0.006, -0.40, 0.40, RED, vis=(1, 2))
    felt.wear = "_w2" if ab else None
    P.add(felt)
    if not ab:
        P.add(W(-0.40, 0.10, 0.006, 0.008, -0.25, 0.10, PAPER, vis=(1,)))
        P.add(stext((-0.15, 0.0081, -0.075), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), 0.30, "pic_scroll", off=0.0012,
                    width=0.48))
        for k, m in enumerate((PALE, RED, INDIGO, KAKI)):
            P.add(bowl(0.25 + 0.09 * (k % 2), -0.20 + 0.09 * (k // 2), 0.035, 0.02, PALE, y0=0.006))
            P.add(fkit.flat_poly(fkit.ngon(0.25 + 0.09 * (k % 2), -0.20 + 0.09 * (k // 2), 0.022, 6), 0.018, m,
                                 vis=(1,)))
        P.adds(tray(0.30, 0.15, 0.22, 0.08, LACQ, y0=0.006))
        for k in range(4):
            P.add(pole((0.21, 0.025, 0.13 + 0.012 * k), (0.39, 0.025, 0.13 + 0.012 * k), 0.004, BAMBOO, n=3))
        P.add(xf(lathe([(0.0, 0.006), (0.04, 0.006), (0.045, 0.06), (0.03, 0.07), (0.0, 0.07)], 6, DARK, vis=(1,)),
                 t=(0.50, 0.0, 0.25)))
    else:
        cr = W(-0.20, 0.12, 0.006, 0.03, -0.15, 0.10, PAPER, vis=(1,))
        cr.wear = "_w2"
        P.add(xf(cr, ry=25.0, t=(-0.15, 0.0, 0.0)))
        P.add(stain(191, 0.25, -0.10, 0.12, y=0.008, mat=LITTER))
        P.add(stain(192, 0.05, 0.20, 0.08, y=0.008, mat=LITTER))
        P.add(rest([xf(bowl(0.0, 0.0, 0.035, 0.02, PALE, wear="_w2"), rx=100.0)])[0])
        P.solids[-1] = xf(P.solids[-1], t=(0.35, 0.006, -0.05))
    P.dim("w", 1.20, 1.20)
    P.notes.append("felt mat, pigments, gofun, glue warmer (BTI 482-485); ink picture only")
    return P


# ================================================================================================ lacquer
UB_W, UB_D, UB_H = 0.91, 0.50, 1.40


def urushiburo(state="intact"):
    """The lacquerer's drying cupboard (urushi-buro, 0.91 x 0.50 x 1.40), kept damp and dust-free: a closed box on a
    plinth, two sliding front leaves (one half open: trays of lacquered bowls drying on the shelves inside). ab: a leaf
    off and leaning, wares fallen out."""
    P = SP("urushiburo", budget="furniture", res3=True, mass=45.0)
    w, d, h = UB_W, UB_D, UB_H
    t = 0.022
    ab = state != "intact"
    P.add(board(-w / 2, w / 2, 0.0, 0.10, -d / 2, d / 2, k=1, vis=(1, 2)))
    P.add(board(-w / 2, w / 2, 0.10, h, -d / 2, -d / 2 + t, k=2, vis=(1, 2)))
    P.add(board(-w / 2, -w / 2 + t, 0.10, h, -d / 2 + t, d / 2, k=3, vis=(1, 2)))
    P.add(board(w / 2 - t, w / 2, 0.10, h, -d / 2 + t, d / 2, k=4, vis=(1, 2)))
    P.add(board(-w / 2, w / 2, h - t, h, -d / 2 + t, d / 2, k=5, vis=(1, 2)))
    shelves = (0.10, 0.48, 0.86)
    for k, y in enumerate(shelves[1:]):
        P.add(board(-w / 2 + t, w / 2 - t, y - 0.018, y, -d / 2 + t, d / 2 - 0.03, k=6 + k, vis=(1,)))
    for y in shelves:                                                     # wares drying inside
        for x in (-0.28, -0.10):
            P.add(bowl(x, -0.02, 0.06, 0.06, SHU if y > 0.4 else LACQ, y0=y))
    leaf = lambda x0, x1, zz: board(x0, x1, 0.10, h - t, zz - 0.012, zz, k=9, vis=(1, 2))   # noqa: E731
    if not ab:
        P.add(leaf(0.0, w / 2 - t, d / 2 - 0.002))                      # right leaf shut
        P.add(leaf(-0.05, w / 2 - t - 0.05, d / 2 - 0.016))             # left leaf slid behind it: the left half open
    else:
        P.add(leaf(0.0, w / 2 - t, d / 2 - 0.002))
        lf = leaf(-w / 2 + t, 0.0, 0.0)
        P.add(xf(lf, rx=-12.0, t=(-0.10, 0.0, d / 2 + 0.30)))           # the other leaf off, leaning
        for k in range(3):
            P.add(rest([xf(bowl(0.0, 0.0, 0.06, 0.06, (SHU, LACQ, SHU)[k], wear="_w2"), rx=90.0, ry=60.0 * k)])[0])
            P.solids[-1] = xf(P.solids[-1], t=(-0.30 + 0.2 * k, 0.0, d / 2 + 0.15))
    c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
    P.add(c)
    fkit.road_tops(P, [c], "boards")
    P.loot_rect("top", h, -w / 2 + 0.05, w / 2 - 0.05, -d / 2 + 0.05, d / 2 - 0.05, rng=0.20)
    P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD, vis=(3,)))
    P.dim("h", h, h)
    P.notes.append("the dust-free drying cupboard (BTI 476; KEEP_TRADES 14 'its tell'); loot on the top (1.40)")
    return P


# ================================================================================================ combs
def comb(x, z, w=0.08, h=0.045, y0=0.0, ry=0.0, mat=BOXWOOD, wear=None):
    """A boxwood comb lying flat: a half-disc back and the tooth block (one flat prism)."""
    poly = [(-w / 2, 0.0), (w / 2, 0.0), (w / 2, h * 0.35)] + [
        (w / 2 * math.cos(math.pi * k / 6), h * 0.35 + h * 0.65 * math.sin(math.pi * k / 6))
        for k in range(1, 6)] + [(-w / 2, h * 0.35)]
    s = fkit.prism(poly, "y", y0, y0 + 0.008, mat, vis=(1,))
    return [xf(wear_all([s], wear)[0], ry=ry, t=(x, 0.0, z))]


def sg_combs(state="intact"):
    """Combs: a small display board with boxwood combs in two rows, a bundle of blanks tied with cord."""
    P = SP("sg_combs", flat=True, mass=0.5)
    if state == "intact":
        P.add(W(-0.27, 0.05, 0.0, 0.012, -0.08, 0.08, WOOD, vis=(1,)))
        for row in range(2):
            for k in range(4):
                P.adds(comb(-0.23 + 0.075 * k, -0.06 + 0.07 * row, y0=0.012))
        for k in range(4):
            P.add(W(0.10, 0.24, 0.012 * k, 0.012 * k + 0.012, -0.04, 0.04, BOXWOOD, vis=(1,)))
        P.add(W(0.165, 0.175, 0.0, 0.05, -0.042, 0.042, ROPE, vis=(1,)))
    else:
        r = random.Random(201)
        P.add(xf(W(-0.16, 0.16, 0.0, 0.012, -0.08, 0.08, WOOD, vis=(1,)), ry=20.0, t=(-0.10, 0.0, 0.0)))
        for k in range(5):
            P.adds(comb(r.uniform(-0.25, 0.25), r.uniform(-0.05, 0.18), ry=r.uniform(0, 180), wear="_w2"))
    return finish_goods(P, BOXWOOD)


# ================================================================================================ dolls
def doll(x, z, y0=0.0, h=0.16, robe=RED, ry=0.0, wear=None, seated=True):
    """A Kyoho-style doll: a tall robe (a flared lathe), the gofun-white head, a black crown / hair block."""
    out = [lathe([(0.0, y0), (h * 0.28, y0), (h * 0.22, y0 + h * 0.55), (h * 0.12, y0 + h * 0.72), (0.0, y0 + h * 0.74)],
                 6, robe, vis=(1,)),
           ball((0.0, y0 + h * 0.83, 0.0), h * 0.10, FUSUMA, n=5),
           box(-h * 0.07, h * 0.07, y0 + h * 0.88, y0 + h, -h * 0.06, h * 0.06, LACQ, vis=(1,))]
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in wear_all(out, wear)]


DT_W, DT_D = 0.91, 0.60


def doll_tiers(state="intact"):
    """The doll shop's display tiers (0.91 x 0.60 x 0.55, three steps under red cloth) with Kyoho-bina dolls: the pair
    on the top step, attendants below, small dolls at the front. ab: the tiers toppled forward, dolls face down."""
    P = SP("doll_tiers", budget="furniture", mass=15.0)
    rise, tread = 0.18, 0.20
    parts = []
    for i in range(3):
        y = rise * (i + 1)
        zf = DT_D / 2 - tread * i
        parts.append(W(-DT_W / 2, DT_W / 2, y - 0.02, y, zf - tread, zf, RED, vis=(1, 2)))
        parts.append(W(-DT_W / 2, DT_W / 2, y - rise, y - 0.02, zf - 0.01, zf, RED, vis=(1,)))
    for x in (-DT_W / 2, DT_W / 2 - 0.02):
        parts.append(W(x, x + 0.02, 0.0, rise * 3, -DT_D / 2, DT_D / 2 - 0.01, WOOD, vis=(1,)))
    parts.append(W(-DT_W / 2, DT_W / 2, 0.0, rise * 3, -DT_D / 2, -DT_D / 2 + 0.02, WOOD, vis=(1,)))
    dolls = []
    for i, (n, hh) in enumerate(((4, 0.10), (3, 0.13), (2, 0.18))):
        y = rise * (i + 1)
        zc = DT_D / 2 - tread * i - tread / 2
        for k in range(n):
            x = (k - (n - 1) / 2) * (0.18 if n > 2 else 0.22) + (0.02 if i == 0 and k == 1 else 0.0)
            if i == 0 and n == 4 and k in (1, 2):
                x += 0.12 * (1 if k == 2 else -1)              # keep the step's loot points free
            dolls.extend(doll(x, zc, y0=y, h=hh, robe=(RED, INDIGO, KINARI)[(i + k) % 3]))
    cols = []
    for i in range(3):
        zf = DT_D / 2 - tread * i
        cols.append(box(-DT_W / 2, DT_W / 2, 0.0, rise * (i + 1), zf - tread, zf, WOOD))
    if state == "intact":
        P.adds(parts + dolls)
        cc = [fkit.col_solid(c) for c in cols]
        P.adds(cc)
        P.loot_rect("step_1", rise, -0.06, 0.06, DT_D / 2 - tread + 0.03, DT_D / 2 - 0.03, rng=0.12,
                    points=[(0.0, rise, DT_D / 2 - tread / 2)])
    else:
        from lkit import place_group
        vs, cs = place_group(parts, [box(-DT_W / 2, DT_W / 2, 0.0, rise * 3, -DT_D / 2, DT_D / 2, WOOD)],
                             [dict(rx=90.0, pivot=(0.0, 0.0, DT_D / 2))])
        P.adds(vs)
        P.adds([fkit.col_solid(c) for c in cs])
        r = random.Random(211)
        for k in range(5):
            d = doll(0.0, 0.0, h=0.13, robe=(RED, INDIGO, KINARI)[k % 3], wear="_w2")
            P.adds(rest([xf(s, rx=90.0, ry=r.uniform(0, 180), t=(r.uniform(-0.4, 0.4), 0.0,
                                                                  DT_D / 2 + 0.55 + r.uniform(0, 0.3))) for s in d]))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], RED, vis=(2,)))
    P.dim("w", DT_W, DT_W)
    P.notes.append("Kyoho-bina (1716-36) in era (BTI 526-528); no daruma (c.1780s), no Ichimatsu doll (1740s)")
    return P


def sg_dolls(state="intact"):
    """Small dolls for a step: four plump gosho dolls (white bodies) and a lidded box. ab: knocked over."""
    P = SP("sg_dolls", flat=True, mass=1.0)
    if state == "intact":
        for k in range(4):
            x = -0.22 + 0.08 * k
            P.add(ball((x, 0.035, 0.0), 0.035, FUSUMA, n=5, sy=1.0))
            P.add(ball((x, 0.085, 0.0), 0.022, FUSUMA, n=5))
            P.add(box(x - 0.02, x + 0.02, 0.10, 0.11, -0.015, 0.015, LACQ, vis=(1,)))
        P.add(W(0.12, 0.26, 0.0, 0.08, -0.06, 0.06, LACQ, vis=(1,)))
    else:
        r = random.Random(221)
        for k in range(4):
            x, z = r.uniform(-0.25, 0.1), r.uniform(-0.02, 0.15)
            P.add(ball((x, 0.035, z), 0.035, FUSUMA, n=5, wear="_w2"))
            P.add(ball((x + 0.05, 0.022, z + 0.02), 0.022, FUSUMA, n=5, wear="_w2"))
        P.add(W(0.12, 0.26, 0.0, 0.08, -0.06, 0.06, LACQ, vis=(1,)))
    return finish_goods(P, FUSUMA)


# ================================================================================================ temple-street goods
def rosary(x, z, r=0.05, mat=DARK, wear=None):
    return [lkit.flat_coil(x, z, r, 0.008, mat=mat, n=10, m=3, wear=wear, sx=0.8)]


def sg_butsugu(state="intact"):
    """Temple-street goods: rosaries (juzu) laid out, bundles of stick incense in a box, a small Buddhist image in its
    open shrine-case (zushi)."""
    P = SP("sg_butsugu", flat=True, mass=1.0)
    if state == "intact":
        for k, x in enumerate((-0.24, -0.15)):
            P.adds(rosary(x, -0.02 + 0.04 * k, mat=(DARK, WOOD)[k]))
        P.add(W(-0.07, 0.07, 0.0, 0.04, -0.06, 0.06, WOOD, vis=(1,)))
        for k in range(3):
            P.add(W(-0.06, 0.06, 0.04, 0.052, -0.05 + 0.035 * k, -0.03 + 0.035 * k, "ground_leaf_litter", vis=(1,)))
        P.add(W(0.12, 0.24, 0.0, 0.20, -0.06, 0.06, LACQ, vis=(1,)))                        # the case
        P.add(W(0.135, 0.225, 0.02, 0.185, 0.055, 0.061, WOOD, vis=(1,)))                   # its open back panel
        P.add(lathe([(0.0, 0.02), (0.03, 0.02), (0.022, 0.10), (0.012, 0.13), (0.0, 0.14)], 5, WOOD, vis=(1,)))
        P.solids[-1] = xf(P.solids[-1], t=(0.18, 0.0, 0.07))
    else:
        r = random.Random(231)
        P.adds(rosary(-0.10, 0.10, mat=DARK, wear="_w2"))
        for k in range(4):
            P.add(xf(W(-0.06, 0.06, 0.0, 0.01, -0.01, 0.01, "ground_leaf_litter", vis=(1,)), ry=r.uniform(0, 180),
                     t=(r.uniform(-0.2, 0.2), 0.0, r.uniform(0.0, 0.18))))
        P.add(rest([xf(W(0.12, 0.24, 0.0, 0.20, -0.06, 0.06, LACQ, vis=(1,)), rz=90.0)])[0])
    return finish_goods(P, LACQ)


# ================================================================================================ registry
PROPS = [
    two("jp_f_sg_pouches", G, ["fukuromono"], ERA_BTI % "BTI 187-198", "surface", sg_pouches,
        ("jp_f_sg_pouches", "jp_f_sg_pouches_swept"), ("Goods: pouches, tobacco cases, setta",
                                                       "Goods: pouches swept off")),
    two("jp_f_hides", F, ["fukuromono"], ERA_BTI % "BTI 158-198 (leather goods; the tannery is its own site)",
        "floor", hides, ("jp_f_hides", "jp_f_hides_unrolled"), ("Rolled hides", "Hide unrolled, mouldy")),
    two("jp_f_sg_yarn", G, ["hataori"], ERA_BTI % "BTI 327-329", "surface", sg_yarn,
        ("jp_f_sg_yarn", "jp_f_sg_yarn_tangled"), ("Goods: skeins and bobbins", "Goods: yarn tangled")),
    two("jp_f_tailor_board", F, ["shitate"], ERA_BTI % "BTI 358-360", "floor", tailor_board,
        ("jp_f_tailor_board", "jp_f_tailor_board_cut"), ("Tailor's cutting board, rule, shears",
                                                         "Tailor's board, the cloth cut and dropped")),
    two("jp_f_paint_mat", F, ["eshi"], ERA_BTI % "BTI 482-485", "floor", paint_mat,
        ("jp_f_paint_mat", "jp_f_paint_mat_upset"), ("Painter's felt mat, pigments, brushes",
                                                     "Painter's mat, dishes upset")),
    two("jp_f_urushiburo", F, ["nushi"], ERA_BTI % "BTI 475-478", "floor", urushiburo,
        ("jp_f_urushiburo", "jp_f_urushiburo_open"), ("Lacquer drying cupboard (urushi-buro)",
                                                      "Lacquer cupboard, a leaf off, wares fallen")),
    two("jp_f_sg_combs", G, ["kushiya"], ERA_BTI % "BTI 248-250", "surface", sg_combs,
        ("jp_f_sg_combs", "jp_f_sg_combs_scattered"), ("Goods: boxwood combs, blanks", "Goods: combs scattered")),
    two("jp_f_doll_tiers", F, ["ningyo"], ERA_BTI % "BTI 526-528 (Kyoho-bina 1716-36)", "floor", doll_tiers,
        ("jp_f_doll_tiers", "jp_f_doll_tiers_toppled"), ("Doll display tiers with Kyoho-bina",
                                                         "Doll tiers toppled, dolls face down")),
    two("jp_f_sg_dolls", G, ["ningyo"], ERA_BTI % "BTI 526-528", "surface", sg_dolls,
        ("jp_f_sg_dolls", "jp_f_sg_dolls_knocked"), ("Goods: small gosho dolls", "Goods: dolls knocked over")),
    two("jp_f_sg_butsugu", G, ["butsugu"], ERA_BTI % "BTI 533-542", "surface", sg_butsugu,
        ("jp_f_sg_butsugu", "jp_f_sg_butsugu_swept"), ("Goods: rosaries, incense, a small image",
                                                       "Goods: rosary and incense scattered")),
    kanban_prop("fukuromono", "kanban_fukuromono", "pouches and bags (fukuromono)", ["fukuromono"]),
    kanban_prop("momen", "kanban_momen", "cotton cloth (momen)", ["hataori"]),
    kanban_prop("shitate", "kanban_shitate", "tailoring (shitate-mono)", ["shitate"]),
    kanban_prop("edokoro", "kanban_edokoro", "painter (e-dokoro)", ["eshi"]),
    kanban_prop("nushi", "kanban_nushi", "lacquerer (nushi)", ["nushi"]),
    kanban_prop("kushi", "kanban_kushi", "combs (kushi)", ["kushiya"]),
    kanban_prop("ningyo", "kanban_ningyo", "dolls (ningyo)", ["ningyo"]),
    kanban_prop("butsugu", "kanban_butsugu", "Buddhist goods (butsugu)", ["butsugu"]),
]
