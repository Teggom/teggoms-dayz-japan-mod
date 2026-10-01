"""S1 group 1 (research/interior/SHOP_SETS.md 2a, trades 1-5): general goods, draper, old clothes, ironmonger,
ceramics and lacquerware.

Goods clusters (jp_f_sg_*, category shopgoods) are visual-only dressing sized for a stand step (<= 0.55 x 0.22);
fittings (shopfit) carry collision and loot; signs (shopsign) are front proxies.
"""
import math
import random

from s1kit import (core, box, lathe, xf, xfs, W, col, col_solid, board, pole, cord, stext, rest, lod_box, wear_all,
                   bowl, bowl_stack, dish_stack, tray, garment_folded, kimono_t, kanban_prop, finish_goods, furn_lods,
                   SP, M, SHOP, SUMI, WOOD, WEATH, IRON, PALE, DARK, LACQ, BAMBOO, WEAVE, MUSHIRO, STACK, ROPE, PAPER,
                   INDIGO, KINARI, RED, LITTER, SHU, PORC, LEATHER)
import fkit
from bits import shards

G = "shopgoods"
F = "shopfit"


def ring_tub(cx, cz, r, h, y0=0.0, wear=None, n=8):
    """A small open tub (oke): staves outside, rim, inside, bottom; a bamboo hoop."""
    prof = [(0.0, y0), (r * 0.92, y0), (r, y0 + h), (r - 0.008, y0 + h), (r * 0.9 - 0.008, y0 + 0.012), (0.0, y0 + 0.012)]
    out = [xf(lathe(prof, n, WEATH, vis=(1,), wear=wear), t=(cx, 0.0, cz)),
           xf(lathe([(r * 0.97 + 0.004, y0 + h * 0.6), (r * 0.98 + 0.004, y0 + h * 0.75), (r * 0.98, y0 + h * 0.75),
                     (r * 0.97, y0 + h * 0.6), (r * 0.97 + 0.004, y0 + h * 0.6)], n, BAMBOO, vis=(1,), wear=wear),
              t=(cx, 0.0, cz))]
    return out


def broom(x0, x1, z, y0=0.0, wear=None):
    """A sorghum-straw broom (zashiki-boki) lying along x: bamboo handle, a flat fan head sewn with three cord rows,
    the end cut square (FP1 remake 2026-10-01, spikes/B3b/fp1kit.zashiki_boki; was a box on a stick)."""
    import fp1kit
    return fp1kit.zashiki_boki(x0, x1, z, y0=y0, wear=wear, seed=int(abs(z) * 1000) + 3)


# ================================================================================================ goods
def sg_aramono(state="intact"):
    P = SP("sg_aramono", flat=True, mass=2.0)
    if state == "intact":
        for k, dz in enumerate((-0.085, -0.045)):
            P.adds(broom(-0.27, 0.27, dz, y0=0.026 * (k % 2)))
        P.adds(ring_tub(0.17, 0.05, 0.07, 0.08))
        P.adds(ring_tub(0.17, 0.05, 0.055, 0.07, y0=0.012))
        P.add(dish_stack(-0.10, 0.05, 0.08, 3, WEAVE, t=0.014))
        P.add(xf(lathe([(0.0, 0.0), (0.06, 0.0), (0.065, 0.035), (0.058, 0.035), (0.0, 0.006)], 8, WEAVE, vis=(1,)),
                 t=(0.02, 0.0, 0.07)))
    else:                                             # brooms knocked down, tubs rolled
        P.adds(xfs(broom(-0.27, 0.27, 0.0), ry=25.0, t=(0.05, 0.0, 0.10)))
        P.adds(xfs(broom(-0.27, 0.27, 0.0, wear="_w2"), ry=-50.0, t=(-0.10, 0.0, -0.02)))
        P.adds(rest(xfs(ring_tub(0.0, 0.0, 0.07, 0.08, wear="_w2"), rx=90.0, ry=30.0, t=(0.25, 0.0, 0.05))))
        P.add(xf(dish_stack(0.0, 0.0, 0.08, 1, WEAVE, t=0.014), t=(-0.22, 0.0, 0.12)))
    return finish_goods(P, STACK)


def bolt(L=0.34, d=0.09, mat=INDIGO, wear=None):
    s = fkit.lcyl("x", d / 2 + 0.002, 0.0, d / 2, -L / 2, L / 2, mat, n=6, vis=(1,), phase=0.0)
    fkit.auto_smooth(s, 70.0)
    b = fkit.lcyl("x", d / 2 + 0.002, 0.0, d / 2 + 0.002, -0.025, 0.025, PAPER, n=6, vis=(1,), phase=0.0)
    return wear_all([s, b], wear)


def sg_bolts(state="intact"):
    """Bolts of cloth (one tan rolled, 0.34 x d 0.09) in a 3-2-1 pyramid along x, the ends to the street."""
    P = SP("sg_bolts", flat=True, mass=3.0)
    mats = (INDIGO, KINARI, INDIGO, RED, KINARI, INDIGO)
    if state == "intact":
        k = 0
        for row, n in enumerate((3, 2, 1)):
            for i in range(n):
                x = (i - (n - 1) / 2) * 0.095
                P.adds(xfs(bolt(mat=mats[k]), ry=90.0, t=(x, row * 0.078, 0.0)))
                k += 1
    else:
        r = random.Random(11)
        for i in range(3):
            P.adds(xfs(bolt(mat=mats[i], wear="_w2"), ry=r.uniform(0, 180), t=(r.uniform(-0.2, 0.2), 0.0,
                                                                               r.uniform(-0.05, 0.10))))
        cl = W(-0.25, 0.25, 0.0, 0.004, -0.09, 0.09, INDIGO, vis=(1,))
        cl.wear = "_w2"
        P.add(xf(cl, ry=8.0, t=(0.05, 0.0, 0.20)))
    P.dim("bolt_d", 0.09, 0.09, tol=0.005)
    return finish_goods(P, INDIGO)


def sg_folded(state="intact"):
    """Folded second-hand garments in three piles (indigo, undyed, a faded red under-robe)."""
    P = SP("sg_folded", flat=True, mass=3.0)
    piles = [(-0.18, (INDIGO, KINARI, INDIGO)), (0.0, (KINARI, RED)), (0.18, (INDIGO, INDIGO, KINARI))]
    if state == "intact":
        for x, ms in piles:
            for k, m in enumerate(ms):
                P.adds(garment_folded(x, 0.0, w=0.17, d=0.18, h=0.035, mat=m, ry=(-3.0, 4.0, -2.0)[k], y0=0.04 * k))
    else:
        r = random.Random(12)
        for i, (x, ms) in enumerate(piles):
            for k, m in enumerate(ms[:2]):
                P.adds(garment_folded(x + r.uniform(-0.05, 0.05), r.uniform(0.0, 0.15), w=0.17, d=0.18, h=0.03, mat=m,
                                      ry=r.uniform(-40, 40), y0=0.032 * k, wear="_w2"))
    return finish_goods(P, INDIGO)


def nabe_small(cx, cz, r=0.09, h=0.07, y0=0.0, wear=None):
    """A small iron pot with two lugs."""
    out = [xf(lathe([(0.0, y0), (r * 0.8, y0), (r, y0 + h * 0.6), (r, y0 + h), (r - 0.005, y0 + h),
                     (r * 0.8 - 0.005, y0 + 0.006), (0.0, y0 + 0.006)], 8, IRON, vis=(1,), wear=wear), t=(cx, 0.0, cz))]
    for s in (-1, 1):
        out.append(box(cx + s * r - 0.008, cx + s * r + 0.008, y0 + h - 0.02, y0 + h, cz - 0.015, cz + 0.015, IRON,
                       vis=(1,)))
    return out


def nail_box(cx, cz, w=0.11, d=0.08, h=0.05, wear=None, spilled=False):
    out = [W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD, vis=(1,))]
    if not spilled:
        out.append(W(-w / 2 + 0.006, w / 2 - 0.006, h, h + 0.004, -d / 2 + 0.006, d / 2 - 0.006, IRON, vis=(1,)))
    return [xf(s, t=(cx, 0.0, cz)) for s in wear_all(out, wear)]


def padlock(cx, cz, y0=0.0, ry=0.0):
    return [xf(box(-0.03, 0.03, y0, y0 + 0.025, -0.012, 0.012, IRON, vis=(1,)), ry=ry, t=(cx, 0.0, cz)),
            xf(box(-0.022, 0.022, y0 + 0.025, y0 + 0.045, -0.004, 0.004, IRON, vis=(1,)), ry=ry, t=(cx, 0.0, cz))]


def sg_ironware(state="intact"):
    """Ironmonger's step: two small pots nested, nail boxes by size, padlocks, a kitchen knife on a cloth."""
    P = SP("sg_ironware", flat=True, mass=6.0)
    if state == "intact":
        P.adds(nabe_small(-0.17, 0.0))
        P.adds(nabe_small(-0.17, 0.0, r=0.075, h=0.06, y0=0.012))
        for k, x in enumerate((0.0, 0.12)):
            P.adds(nail_box(x, -0.03, w=0.10 - 0.02 * k))
        P.adds(padlock(0.06, 0.07))
        P.adds(padlock(0.16, 0.07, ry=20.0))
        P.add(W(0.18, 0.27, 0.0, 0.004, -0.05, 0.05, KINARI, vis=(1,)))
        P.add(box(0.19, 0.265, 0.004, 0.008, -0.012, 0.012, IRON, vis=(1,)))
    else:
        P.adds(rest(xfs(nabe_small(0.0, 0.0, wear="_w2"), rx=80.0, ry=40.0, t=(-0.15, 0.0, 0.05))))
        P.adds(nail_box(0.05, -0.02, spilled=True, wear="_w2"))
        r = random.Random(13)
        for i in range(14):                               # nails strewn
            x, z = r.uniform(-0.05, 0.30), r.uniform(0.0, 0.20)
            P.add(xf(box(-0.03, 0.03, 0.0, 0.004, -0.002, 0.002, IRON, vis=(1,)), ry=r.uniform(0, 180), t=(x, 0.0, z)))
    return finish_goods(P, IRON)


def sg_porcelain(state="intact"):
    """Blue-and-white bowls in stacks, a dish stack, a big bowl; ab: a stack knocked down, shards."""
    P = SP("sg_porcelain", flat=True, mass=4.0)
    if state == "intact":
        P.add(bowl_stack(-0.19, -0.02, 0.065, 0.06, 4, PORC))
        P.add(bowl_stack(-0.05, 0.03, 0.065, 0.06, 3, PORC))
        P.add(dish_stack(0.09, -0.02, 0.085, 6, PORC))
        P.add(bowl(0.22, 0.04, 0.075, 0.07, PORC))
    else:
        P.add(bowl_stack(-0.19, -0.02, 0.065, 0.06, 2, PORC, wear="_w2"))
        P.add(rest([xf(bowl(0.0, 0.0, 0.065, 0.06, PORC, wear="_w2"), rx=100.0, ry=30.0)])[0])
        P.solids[-1] = xf(P.solids[-1], t=(0.02, 0.0, 0.06))
        P.adds(shards(1301, 0.15, 0.06, 0.12, 7, PORC))
        P.add(dish_stack(0.20, -0.04, 0.085, 2, PORC, wear="_w2"))
    return finish_goods(P, PORC)


def sg_lacquer(state="intact"):
    """Lacquer wares: black and shu bowl stacks, a stack of trays (zen) and lidded bowls."""
    P = SP("sg_lacquer", flat=True, mass=2.0)
    if state == "intact":
        P.add(bowl_stack(-0.20, 0.0, 0.06, 0.06, 4, LACQ))
        P.add(bowl_stack(-0.07, 0.0, 0.06, 0.06, 4, SHU))
        for k in range(3):
            P.adds(tray(0.14, 0.0, 0.24, 0.17, LACQ if k % 2 == 0 else SHU, y0=0.026 * k, ry=(0.0, 3.0, -2.0)[k]))
    else:
        r = random.Random(14)
        for i in range(4):
            P.add(rest([xf(bowl(0.0, 0.0, 0.06, 0.06, (LACQ, SHU)[i % 2], wear="_w2"), rx=r.choice((0.0, 95.0, 180.0)),
                           ry=r.uniform(0, 180))])[0])
            P.solids[-1] = xf(P.solids[-1], t=(r.uniform(-0.25, 0.1), 0.0, r.uniform(-0.05, 0.18)))
        P.adds(tray(0.15, 0.06, 0.24, 0.17, SHU, ry=25.0, wear="_w2"))
    return finish_goods(P, LACQ)


# ================================================================================================ fittings
BS_W, BS_D, BS_H = 0.91, 0.45, 1.50
BS_LEVELS = (0.03, 0.50, 0.98, 1.47)


def bolt_shelf(state="intact"):
    """Cloth-bolt shelf (tana of cubbies, half ken): 2 x 3 cubbies, bolts end-on to the room in half of them, the other half
    left for loot (shelf points on the free boards). Draper, weaver."""
    P = SP("bolt_shelf", budget="furniture", res3=True, mass=40.0)
    x0, x1, z0, z1 = -BS_W / 2, BS_W / 2, -BS_D / 2, BS_D / 2
    t = 0.022
    vis = [board(x0, x1, 0.0, BS_H, z0, z0 + 0.012, k=1, vis=(1, 2))]            # back
    for x in (x0, x1 - t):
        vis.append(board(x, x + t, 0.0, BS_H, z0 + 0.012, z1, k=3, vis=(1, 2)))     # sides
    for i, y in enumerate(BS_LEVELS):
        vis.append(board(x0 + t, x1 - t, y - t, y, z0 + 0.012, z1, k=4 + i, vis=(1, 2)))  # shelves (+ the top)
    cw = (BS_W - 2 * t) / 2
    for i in range(1, 2):
        x = x0 + t + cw * i
        for a, b in zip(BS_LEVELS[:-1], BS_LEVELS[1:]):
            vis.append(W(x - 0.009, x + 0.009, a, b - t, z0 + 0.012, z1 - 0.01, vis=(1,)))
    P.adds(vis)
    rr = random.Random(21 if state == "intact" else 22)
    mats = (INDIGO, KINARI, INDIGO, RED, KINARI, INDIGO)
    full = {(0, 0), (1, 1), (0, 2)} if state == "intact" else {(1, 2)}
    free = []
    for lev in range(3):
        y = BS_LEVELS[lev]
        for c in range(2):
            cx = x0 + t + cw * (c + 0.5)
            if (c, lev) in full:
                for k, (dx, dy) in enumerate(((-0.10, 0.0), (0.0, 0.0), (0.10, 0.0), (-0.05, 0.085), (0.05, 0.085))):
                    s = xfs(bolt(L=0.36, d=0.085, mat=mats[(c + lev + k) % 6]), ry=90.0,
                            t=(cx + dx, y + dy, z1 - 0.20))
                    P.adds(s)
            else:
                free.append((c, lev, cx, y))
    cols = [col(x0, x1, 0.0, BS_H, z0, z0 + 0.012)]
    for x in (x0, x1 - t):
        cols.append(col(x, x + t, 0.0, BS_H, z0 + 0.012, z1))
    for y in BS_LEVELS:
        cols.append(col(x0 + t, x1 - t, y - t, y, z0 + 0.012, z1))
    P.adds(cols)
    for c, lev, cx, y in free:
        if y <= 1.40:
            P.loot_rect("cubby_%d_%d" % (lev, c), y, cx - cw / 2 + 0.03, cx + cw / 2 - 0.03, z0 + 0.06, z1 - 0.04,
                        rng=0.15, points=[(cx, y, 0.03)])
    if state != "intact":                                         # bolts pulled out onto the floor in front
        for i in range(4):
            P.adds(xfs(bolt(mat=mats[i], wear="_w2"), ry=rr.uniform(0, 180), t=(rr.uniform(-0.35, 0.35), 0.0,
                                                                                z1 + rr.uniform(0.12, 0.40))))
        cl = W(-0.45, 0.45, 0.0, 0.004, -0.16, 0.16, INDIGO, vis=(1,))
        cl.wear = "_w2"
        P.add(xf(cl, ry=-10.0, t=(0.10, 0.0, z1 + 0.50)))
    P.add(W(x0, x1, 0.0, BS_H, z0, z1, WOOD, vis=(3,)))
    P.dim("w", BS_W, P.bbox()[1] - P.bbox()[0] if state == "intact" else BS_W, tol=0.01)
    P.dim("h", BS_H, BS_H)
    P.notes.append("against the party wall (back at z = -0.225); loot on the empty cubbies' boards (<= 1.40)")
    return P


FR_W, FR_H = 1.20, 1.70


def furugi_rack(state="intact"):
    """Old-clothes rack (1.20): a bamboo pole on two T-footed stands, three second-hand kimono hung by the sleeves."""
    P = SP("furugi_rack", budget="furniture", res3=True, mass=12.0)
    xs = (-FR_W / 2 + 0.06, FR_W / 2 - 0.06)
    for x in xs:
        P.add(W(x - 0.03, x + 0.03, 0.0, 0.05, -0.22, 0.22, WEATH, vis=(1, 2)))                 # foot
        P.add(pole((x, 0.05, 0.0), (x, FR_H, 0.0), 0.022, BAMBOO, n=6, vis=(1, 2)))           # upright
    cols = [col(x - 0.03, x + 0.03, 0.0, 0.05, -0.22, 0.22) for x in xs]
    cols += [col(x - 0.022, x + 0.022, 0.05, FR_H, -0.022, 0.022) for x in xs]
    if state == "intact":
        P.add(pole((xs[0] - 0.05, FR_H - 0.04, 0.0), (xs[1] + 0.05, FR_H - 0.04, 0.0), 0.018, BAMBOO, n=6, vis=(1, 2)))
        py = FR_H - 0.04
        for k, (x, m, L) in enumerate(((-0.36, INDIGO, 0.78), (0.0, KINARI, 0.66), (0.36, RED, 0.72))):
            # a robe folded lengthwise and draped over the pole: two panels down the front and back, the fold on top,
            # the hem a little uneven, the collar band showing on the front panel
            w = 0.34
            P.add(W(x - w / 2, x + w / 2, py - L, py + 0.02, 0.020, 0.028, m, vis=(1, 2)))
            P.add(W(x - w / 2 + 0.01, x + w / 2 - 0.01, py - L + 0.06, py + 0.02, -0.028, -0.020, m, vis=(1, 2)))
            P.add(W(x - w / 2, x + w / 2, py + 0.018, py + 0.030, -0.028, 0.028, m, vis=(1,)))
            P.add(W(x - 0.05, x + 0.05, py - L + 0.10, py + 0.0, 0.028, 0.032, KINARI if m != KINARI else INDIGO,
                    vis=(1,)))
        cols.append(col(-FR_W / 2 + 0.10, FR_W / 2 - 0.10, py - 0.78, py + 0.03, -0.03, 0.03))
    else:                                         # the pole down at one end, the robes heaped under it
        P.add(pole((xs[0], FR_H - 0.04, 0.0), (xs[1] - 0.05, 0.06, 0.12), 0.018, BAMBOO, n=6, vis=(1, 2)))
        r = random.Random(23)
        for k, m in enumerate((INDIGO, KINARI, RED)):
            P.adds(garment_folded(r.uniform(-0.3, 0.3), r.uniform(0.0, 0.35), w=0.55, d=0.40, h=0.03, mat=m,
                                  ry=r.uniform(-60, 60), y0=0.025 * (k % 2), wear="_w2"))
    P.adds(cols)
    P.add(W(-FR_W / 2, FR_W / 2, 0.0, FR_H, -0.22, 0.22, BAMBOO, vis=(3,)))
    P.dim("h", FR_H, FR_H)
    P.notes.append("garments hung by the sleeves (BTI 924-925); no loot (the robes are dressing)")
    return P


def sickle(x, y, z=0.0, wear=None):
    """A sickle hung blade down on a peg: wooden handle (vertical), the crescent blade (two flat iron boxes)."""
    return wear_all([W(x - 0.012, x + 0.012, y - 0.30, y, z, z + 0.022, WEATH, vis=(1,)),
                     xf(box(0.0, 0.16, -0.018, 0.0, 0.0, 0.004, IRON, vis=(1,)), rz=-20.0, t=(x + 0.012, y - 0.29, z + 0.009)),
                     xf(box(0.0, 0.07, -0.016, 0.0, 0.0, 0.004, IRON, vis=(1,)), rz=-55.0, t=(x + 0.16, y - 0.345, z + 0.009))],
                    wear)


def knife(x, y, z=0.0, L=0.30, wear=None):
    return wear_all([W(x - 0.012, x + 0.012, y - 0.12, y, z, z + 0.02, WOOD, vis=(1,)),
                     W(x - 0.022, x + 0.022, y - L, y - 0.12, z + 0.008, z + 0.012, IRON, vis=(1,))], wear)


def saw(x, y, z=0.0, wear=None):
    return wear_all([W(x - 0.015, x + 0.015, y - 0.22, y, z, z + 0.024, WEATH, vis=(1,)),
                     W(x - 0.05, x + 0.04, y - 0.62, y - 0.22, z + 0.009, z + 0.013, IRON, vis=(1,))], wear)


def hoe_head(x, y, z=0.0, wear=None):
    return wear_all([W(x - 0.08, x + 0.08, y - 0.18, y - 0.02, z, z + 0.008, IRON, vis=(1,)),
                     W(x - 0.02, x + 0.02, y - 0.04, y, z, z + 0.03, IRON, vis=(1,))], wear)


def kanamono_wall(state="intact"):
    """Ironmonger's wall board (1.20 x 0.90, 0.80-1.70 up) with pegs: sickles, kitchen knives, a saw, hoe heads,
    padlocks. ab: half taken, one hanging crooked."""
    P = SP("kanamono_wall", flat=True, anchor="wall", mass=10.0)
    ab = state != "intact"
    w = "_w2" if ab else None
    P.add(board(-0.60, 0.60, 0.80, 1.70, 0.0, 0.02, k=5, vis=(1, 2)))
    P.add(W(-0.60, 0.60, 1.40, 1.43, 0.02, 0.05, WEATH, vis=(1,)))                       # the peg rail
    items = [("sickle", -0.50), ("sickle", -0.36), ("sickle", -0.22), ("knife", -0.06), ("knife", 0.04),
             ("saw", 0.20), ("hoe", 0.42)]
    for k, (what, x) in enumerate(items):
        if ab and k in (1, 3, 5):
            continue
        y = 1.42
        if what == "sickle":
            ss = sickle(x, y, 0.05, w)
        elif what == "knife":
            ss = knife(x, y, 0.05, wear=w)
        elif what == "saw":
            ss = saw(x, y, 0.05, w)
        else:
            ss = hoe_head(x, y - 0.06, 0.05, w)
        if ab and k == 6:
            ss = [xf(s, rz=25.0, pivot=(x, y, 0.0)) for s in ss]
        P.adds(ss)
    for x in (-0.40, -0.25, -0.10, 0.10, 0.25):                                          # the lower peg row: padlocks
        if ab and x > 0:
            continue
        P.adds(padlock(x, 0.07, y0=1.02))
        P.solids[-2] = xf(P.solids[-2], rx=90.0, pivot=(x, 1.02, 0.07))
        P.solids[-1] = xf(P.solids[-1], rx=90.0, pivot=(x, 1.02, 0.07))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("board_w", 1.20, 1.20)
    P.notes.append("wall item (visual, Res 1): the ironmonger's stock board (BTI 914-915: tools on the wall)")
    return P


def ware_crate(state="intact"):
    """A wooden crate of wares packed in straw (0.60 x 0.45 x 0.40), its lid leaning; bowl rims show in the straw.
    ab: tipped on its side, straw and shards out."""
    P = SP("ware_crate", budget="small", mass=15.0)
    w, d, h = 0.60, 0.45, 0.40
    t = 0.018
    body = [board(-w / 2, w / 2, 0.0, h, -d / 2, -d / 2 + t, k=1, vis=(1, 2)),
            board(-w / 2, w / 2, 0.0, h, d / 2 - t, d / 2, k=2, vis=(1, 2)),
            board(-w / 2, -w / 2 + t, 0.0, h, -d / 2 + t, d / 2 - t, k=3, vis=(1, 2)),
            board(w / 2 - t, w / 2, 0.0, h, -d / 2 + t, d / 2 - t, k=4, vis=(1, 2)),
            W(-w / 2 + t, w / 2 - t, 0.0, 0.02, -d / 2 + t, d / 2 - t, vis=(1,))]
    straw = W(-w / 2 + t, w / 2 - t, 0.02, h - 0.04, -d / 2 + t, d / 2 - t, STACK, vis=(1,))
    if state == "intact":
        P.adds(body + [straw])
        for x in (-0.15, 0.0, 0.15):
            P.add(xf(lathe([(0.065, h - 0.07), (0.07, h - 0.035), (0.064, h - 0.035), (0.059, h - 0.07)], 8, PORC,
                           vis=(1,)), t=(x, 0.0, -0.05)))
        lid = board(-w / 2, w / 2, 0.0, 0.45, 0.0, 0.018, k=5, vis=(1, 2))      # leaning on the crate front
        P.add(xf(lid, rx=-15.0, t=(0.0, 0.0, d / 2 + 0.125)))
        c = col(-w / 2, w / 2, 0.0, h - 0.04, -d / 2, d / 2)
        P.add(c)
        fkit.road_tops(P, [c], "boards")
        P.loot_rect("straw", h - 0.04, -0.20, 0.20, -0.15, 0.10, rng=0.15, points=[(0.08, h - 0.04, 0.08)])
    else:
        grp = body + [W(-w / 2 + t, w / 2 - t, 0.02, 0.15, -d / 2 + t, d / 2 - t, STACK, vis=(1,))]
        vis_ss, col_ss = fkit_place(grp, [box(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD)], rx=-90.0, ry=15.0)
        P.adds(vis_ss)
        P.adds([col_solid(c) for c in col_ss])
        P.adds(shards(1311, 0.10, 0.45, 0.30, 9, PORC))
        P.add(mound_flat(0.0, 0.40, 0.30, 0.20))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("w", w, w)
    return P


def fkit_place(vis_ss, col_ss, rx=0.0, ry=0.0):
    from lkit import place_group
    return place_group(vis_ss, col_ss, [dict(rx=rx), dict(ry=ry)])


def mound_flat(cx, cz, sx, sz):
    s = W(-sx / 2, sx / 2, 0.0, 0.01, -sz / 2, sz / 2, STACK, vis=(1,))
    s.wear = "_w2"
    return xf(s, ry=20.0, t=(cx, 0.0, cz))


# ================================================================================================ registry
def two(pid, cat, trades, era, mount, fn, names, display):
    """A prop with the intact model and one abandoned state."""
    a, b = names
    return {"id": pid, "cat": cat, "mount": mount, "trades": trades, "era": era, "models": [
        M(a, "std", "intact", display[0], lambda: fn("intact")),
        M(b, "std", b.rsplit("_", 1)[1], display[1], lambda: fn("ab"))]}


ERA_BTI = "KEPT (research/interior/SHOP_SETS.md: %s)"
PROPS = [
    two("jp_f_sg_aramono", G, ["aramono"], ERA_BTI % "BTI 912-913", "surface", sg_aramono,
        ("jp_f_sg_aramono", "jp_f_sg_aramono_swept"), ("Goods: brooms, tubs, sieves", "Goods: brooms knocked down")),
    two("jp_f_sg_bolts", G, ["draper", "hataori"], ERA_BTI % "BTI 919-923", "surface", sg_bolts,
        ("jp_f_sg_bolts", "jp_f_sg_bolts_swept"), ("Goods: cloth bolts, 3-2-1", "Goods: bolts rolled off")),
    two("jp_f_sg_folded", G, ["furugi", "shitate"], ERA_BTI % "BTI 924-925", "surface", sg_folded,
        ("jp_f_sg_folded", "jp_f_sg_folded_tumbled"), ("Goods: folded garments", "Goods: garment piles tumbled")),
    two("jp_f_sg_ironware", G, ["kanamono"], ERA_BTI % "BTI 914-915", "surface", sg_ironware,
        ("jp_f_sg_ironware", "jp_f_sg_ironware_spilled"), ("Goods: pots, nail boxes, padlocks, a knife",
                                                           "Goods: pot over, nails strewn")),
    two("jp_f_sg_porcelain", G, ["setomono"], ERA_BTI % "BTI 916-917; Hizen porcelain (general)", "surface",
        sg_porcelain, ("jp_f_sg_porcelain", "jp_f_sg_porcelain_broken"),
        ("Goods: blue-and-white bowls and dishes", "Goods: bowls knocked down, shards")),
    two("jp_f_sg_lacquer", G, ["setomono", "nushi"], ERA_BTI % "BTI 918, 475-478", "surface", sg_lacquer,
        ("jp_f_sg_lacquer", "jp_f_sg_lacquer_scattered"), ("Goods: black and red lacquer bowls, trays",
                                                           "Goods: lacquer bowls scattered")),
    two("jp_f_bolt_shelf", F, ["draper", "hataori"], ERA_BTI % "BTI 919-923", "floor", bolt_shelf,
        ("jp_f_bolt_shelf", "jp_f_bolt_shelf_pulled"), ("Cloth-bolt shelf (cubbies)", "Cloth-bolt shelf, bolts "
                                                                                    "pulled out")),
    two("jp_f_furugi_rack", F, ["furugi"], ERA_BTI % "BTI 924-925", "floor", furugi_rack,
        ("jp_f_furugi_rack", "jp_f_furugi_rack_down"), ("Old-clothes rack, four robes", "Old-clothes rack, pole "
                                                                                       "down, robes heaped")),
    two("jp_f_kanamono_wall", F, ["kanamono"], ERA_BTI % "BTI 914-915", "wall", kanamono_wall,
        ("jp_f_kanamono_wall", "jp_f_kanamono_wall_taken"), ("Ironmonger's tool board", "Ironmonger's board, half "
                                                                                       "taken")),
    two("jp_f_ware_crate", F, ["setomono"], ERA_BTI % "BTI 916 (a packing corner with straw)", "floor", ware_crate,
        ("jp_f_ware_crate", "jp_f_ware_crate_tipped"), ("Crate of wares in straw", "Crate tipped, straw and shards")),
    kanban_prop("aramono", "kanban_aramono", "general goods (aramono)", ["aramono"]),
    kanban_prop("gofuku", "kanban_gofuku", "silk draper (gofuku)", ["draper"], mat=SUMI),
    kanban_prop("futomono", "kanban_futomono", "cotton cloth (futomono)", ["draper"]),
    kanban_prop("furugi", "kanban_furugi", "old clothes (furugi)", ["furugi"]),
    kanban_prop("kanamono", "kanban_kanamono", "ironmonger (kanamono)", ["kanamono"]),
    kanban_prop("setomono", "kanban_setomono", "ceramics (setomono)", ["setomono"]),
    kanban_prop("nurimono", "kanban_nurimono", "lacquerware (nurimono)", ["setomono"]),
]
