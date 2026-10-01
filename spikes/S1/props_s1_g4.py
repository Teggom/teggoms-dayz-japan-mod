"""S1 group 4 (research/interior/SHOP_SETS.md 2b-2c, trades 16-20): sake shop, cooked-food and sake house,
apothecary and doctor, pawnbroker and moneychanger, publisher and bookshop."""
import math
import random

from s1kit import (box, lathe, xf, xfs, W, col, board, pole, cord, stext, rest, lod_box, wear_all, stain, jug,
                   packet, tray, kanban_prop, kanban_parts, finish_goods, garment_folded, SP, M, SHOP, SUMI, WOOD,
                   WEATH, IRON, PALE, DARK, LACQ, BAMBOO, ROPE, PAPER, INDIGO, KINARI, RED, LITTER, FOLIAGE, ARM_Y,
                   ARM_L, KB_T)
import fkit
import skit
from props_s1_g1 import two, ERA_BTI

G = "shopgoods"
F = "shopfit"
S = "shopsign"


# ================================================================================================ sake
def sugidama(state="green"):
    """The sugidama (sakabayashi): a ball of cedar sprigs (d 0.45) hung by a cord from a short bracket under the eave
    at the sake shop's door. green = fresh (new sake), brown = a season old, fallen = lying at the foot of the facade.
    Frame: facade plane z = 0, y = 0 at the wall foot (front proxy)."""
    P = SP("sugidama", flat=True, anchor="wall", mass=3.0)
    w = {"green": "_w0", "brown": "_w2", "fallen": "_w2"}[state]
    r = 0.225
    zc = 0.42
    P.add(W(-0.03, 0.03, ARM_Y - 0.20, ARM_Y + 0.06, 0.0, 0.03, WEATH, vis=(1, 2)))
    P.add(W(-0.02, 0.02, ARM_Y, ARM_Y + 0.04, 0.03, zc + 0.04, WEATH, vis=(1, 2)))
    yc = ARM_Y - 0.35 - r if state != "fallen" else r * 0.92
    prof = [(0.0, -r)] + [(r * math.sin(math.pi * k / 6), -r * math.cos(math.pi * k / 6)) for k in range(1, 6)] + \
        [(0.0, r)]
    outer = xf(lathe(prof, 10, FOLIAGE, vis=(1,), wear=w), t=(0.0, yc, zc))
    inner = xf(lathe([(x * 0.82, y * 0.82) for x, y in prof], 8, FOLIAGE, vis=(1,), wear=w), ry=17.0, t=(0.0, yc, zc))
    P.adds([outer, inner])
    if state != "fallen":
        P.add(cord((0.0, ARM_Y, zc), (0.0, yc + r, zc), 0.006))
    else:
        P.add(cord((0.0, ARM_Y, zc), (0.0, ARM_Y - 0.25, zc + 0.03), 0.006))       # the snapped cord
    P.add(lod_box([outer], WEATH, vis=(2,)))
    P.dim("d", 2 * r, 2 * r)
    P.notes.append("the sake shop's sign (BTI 575-578); foliage _w0 green when the new sake is in, _w2 brown")
    P.extra["hang_y"] = ARM_Y + 0.05
    return P


# ================================================================================================ medicine
YK_W, YK_D, YK_H = 0.91, 0.40, 1.20


def yakudansu(state="intact"):
    """The apothecary's drawer cabinet (hyakumi-dansu, 0.91 x 0.40 x 1.20): 6 x 6 small drawers with paper labels
    (drug names, the shop atlas), a plinth, a top board. ab: eight drawers pulled out, three on the floor, packets
    spilled."""
    P = SP("yakudansu", budget="furniture", res3=True, mass=55.0)
    ab = state != "intact"
    w, d, h = YK_W, YK_D, YK_H
    P.add(board(-w / 2, w / 2, 0.0, 0.08, -d / 2, d / 2, k=1, vis=(1, 2)))                       # plinth
    P.add(board(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, k=2, vis=(1, 2)))                     # top
    P.add(W(-w / 2, w / 2, 0.08, h - 0.03, -d / 2, d / 2 - 0.02, WOOD, vis=(1, 2)))              # the carcass
    cw, rh = (w - 0.04) / 6, (h - 0.11 - 0.02) / 6
    rr = random.Random(141)
    out_set = {3, 8, 14, 15, 21, 26, 30, 33} if ab else set()
    gone = {9, 20, 27} if ab else set()
    labels = skit.cell(SHOP, "drawer_labels")
    for row in range(6):
        for c in range(6):
            k = row * 6 + c
            x0 = -w / 2 + 0.02 + c * cw
            y0 = 0.09 + row * rh
            if k in gone:
                P.add(W(x0 + 0.004, x0 + cw - 0.004, y0 + 0.004, y0 + rh - 0.004, d / 2 - 0.03, d / 2 - 0.021,
                        LACQ, vis=(1,)))                                                           # the dark hole
                continue
            pull = rr.uniform(0.08, 0.20) if k in out_set else 0.0
            P.add(W(x0 + 0.004, x0 + cw - 0.004, y0 + 0.004, y0 + rh - 0.004, d / 2 - 0.02 + pull, d / 2 + pull,
                    WOOD, vis=(1,)))
            if pull:
                P.add(W(x0 + 0.006, x0 + cw - 0.006, y0 + 0.006, y0 + 0.012, d / 2 - 0.02, d / 2 - 0.02 + pull,
                        WOOD, vis=(1,)))
            ci = k % 16
            crop = ((ci % 4) / 4.0, (ci // 4) / 4.0, (ci % 4 + 1) / 4.0, (ci // 4 + 1) / 4.0)
            P.add(stext((x0 + cw / 2, y0 + rh * 0.62, d / 2 + pull), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), rh * 0.45,
                        "drawer_labels", wear="_w2" if ab else None, off=0.0012, crop=crop))
            P.add(box(x0 + cw / 2 - 0.012, x0 + cw / 2 + 0.012, y0 + rh * 0.22, y0 + rh * 0.30, d / 2 + pull,
                      d / 2 + pull + 0.008, IRON, vis=(1,)))
    if ab:
        for k in range(3):
            P.add(xf(W(-cw / 2 + 0.004, cw / 2 - 0.004, 0.0, rh - 0.008, -0.16, 0.0, WOOD, vis=(1,)),
                     ry=rr.uniform(-40, 40), rx=rr.choice((0.0, 90.0)) * 0, t=(rr.uniform(-0.4, 0.4), 0.0,
                                                                                d / 2 + rr.uniform(0.25, 0.55))))
        for k in range(5):
            P.add(packet(rr.uniform(-0.4, 0.4), d / 2 + rr.uniform(0.1, 0.6), 0.06, 0.09, 0.012, PAPER,
                         ry=rr.uniform(0, 180), wear="_w2"))
    c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
    P.add(c)
    fkit.road_tops(P, [c], "boards")
    P.loot_rect("top", h, -w / 2 + 0.05, w / 2 - 0.05, -d / 2 + 0.05, d / 2 - 0.05, rng=0.20)
    P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD, vis=(3,)))
    P.dim("w", w, w)
    P.dim("h", h, h)
    P.notes.append("hyakumi-dansu (BTI 808, 815); against the party wall (back z = -0.20); loot on the top")
    return P


def yagen(state="intact"):
    """The drug chopper (yagen): a boat-shaped iron trough (0.45 x 0.10 x 0.12) on a wooden block, the iron wheel with
    its axle handle in the trough. ab: the wheel off, lying beside it."""
    P = SP("yagen", budget="small", mass=9.0)
    L, wd, h = 0.45, 0.10, 0.12
    P.add(W(-L / 2 - 0.03, L / 2 + 0.03, 0.0, 0.04, -wd / 2 - 0.02, wd / 2 + 0.02, WOOD, vis=(1, 2)))
    P.add(fkit.prism([(-L / 2, h), (L / 2, h), (L / 2 - 0.06, 0.04), (-L / 2 + 0.06, 0.04)], "z", -wd / 2, wd / 2,
                     IRON, vis=(1, 2)))
    wheel = [fkit.lcyl("z", 0.0, 0.0, 0.08, -0.008, 0.008, IRON, n=10, vis=(1,)),
             pole((0.0, 0.0, -0.16), (0.0, 0.0, 0.16), 0.008, WOOD, n=5)]
    if state == "intact":
        P.adds([xf(s, t=(0.05, h + 0.02, 0.0)) for s in wheel])
    else:
        P.adds(rest([xf(s, rx=90.0, t=(0.0, 0.0, 0.28)) for s in wheel]))
    P.add(col(-L / 2 - 0.03, L / 2 + 0.03, 0.0, h, -wd / 2 - 0.02, wd / 2 + 0.02))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], IRON, vis=(2,)))
    P.dim("L", L, L)
    P.notes.append("drug chopper (BTI 807, 815)")
    return P


def sg_medicine(state="intact"):
    """Ready remedies: packets of Hangontan and Mankintan (labelled), small medicine jars, a brand box."""
    P = SP("sg_medicine", flat=True, mass=1.0)
    if state == "intact":
        for k in range(3):
            for j, cell in enumerate(("pkt_hangontan", "pkt_mankintan")):
                x = -0.20 + 0.10 * j
                P.add(packet(x, 0.0, 0.07, 0.13, 0.014, PAPER, y0=0.014 * k))
                if k == 2:
                    P.add(stext((x, 0.042 + 0.0012, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), 0.10, cell, off=0.0012))
        for k, x in enumerate((0.06, 0.13, 0.20)):
            P.add(jug(x, 0.0, 0.03, 0.08 + 0.01 * k, PALE))
        P.add(W(0.15, 0.27, 0.0, 0.05, 0.04, 0.10, LACQ, vis=(1,)))
    else:
        r = random.Random(142)
        for k in range(6):
            P.add(packet(r.uniform(-0.25, 0.2), r.uniform(-0.05, 0.18), 0.07, 0.13, 0.012, PAPER,
                         ry=r.uniform(0, 180), wear="_w2"))
        P.add(rest([xf(jug(0.0, 0.0, 0.03, 0.09, PALE), rx=90.0, ry=40.0)])[0])
        P.solids[-1] = xf(P.solids[-1], t=(0.18, 0.0, 0.08))
    return finish_goods(P, PAPER)


# ================================================================================================ pawn and money
def pawn_board(state="intact"):
    """The pawnbroker's tag board (0.90 wide, 0.95-1.60 up, wall plane z = 0): three rows of nails with numbered pawn
    tickets hung on them. ab: half the tickets torn off, the rest faded and curled."""
    P = SP("pawn_board", flat=True, anchor="wall", mass=3.0)
    ab = state != "intact"
    P.add(board(-0.45, 0.45, 0.95, 1.60, 0.0, 0.02, k=4, vis=(1, 2)))
    cells = ("tag_ichi", "tag_ni", "tag_san")
    rr = random.Random(151)
    for row, y in enumerate((1.52, 1.31, 1.10)):
        for k in range(6):
            x = -0.36 + 0.144 * k
            P.add(box(x - 0.004, x + 0.004, y - 0.004, y + 0.004, 0.02, 0.035, IRON, vis=(1,)))
            if ab and rr.random() < 0.5:
                continue
            tw, th = 0.05, 0.19
            tag = [W(x - tw / 2, x + tw / 2, y - th, y, 0.022, 0.024, PAPER, vis=(1,)),
                   stext((x, y - th / 2 - 0.01, 0.024), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), th * 0.86,
                         cells[(row + k) % 3], wear="_w2" if ab else None, off=0.0012, width=tw * 0.9)]
            if ab:
                tag = [xf(s, rz=rr.uniform(-12, 12), pivot=(x, y, 0.0)) for s in tag]
            P.adds(tag)
    P.add(lod_box([s for s in P.solids if 1 in s.vis and not getattr(s, "_text_faced", False)], WOOD, vis=(2,)))
    P.dim("w", 0.90, 0.90)
    P.notes.append("pawn tickets on a tag board (BTI 831-833)")
    return P


def bundle(x, z, w=0.22, d=0.16, h=0.10, mat=INDIGO, ry=0.0, y0=0.0, wear=None, tag=True):
    """A cloth-wrapped pawned bundle with its knot and a paper tag."""
    out = [W(-w / 2, w / 2, y0, y0 + h, -d / 2, d / 2, mat, vis=(1,)),
           fkit.rotated_box(0.0, 0.0, 0.07, 0.05, y0 + h, y0 + h + 0.03, 20.0, mat, vis=(1,))]
    if tag:
        out.append(W(w / 2 - 0.02, w / 2, y0 + h * 0.3, y0 + h * 0.8, d / 2, d / 2 + 0.002, PAPER, vis=(1,)))
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in wear_all(out, wear)]


def sg_pawn(state="intact"):
    """Pawned goods: wrapped bundles with tags, a long sword bag, a folded robe with its tag. ab: bundles undone."""
    P = SP("sg_pawn", flat=True, mass=4.0)
    if state == "intact":
        P.adds(bundle(-0.17, 0.0, mat=INDIGO))
        P.adds(bundle(-0.17, 0.0, w=0.18, d=0.13, h=0.08, mat=KINARI, y0=0.10, ry=8.0))
        P.add(xf(fkit.lcyl("x", 0.03, 0.0, 0.03, -0.26, 0.26, INDIGO, n=6, vis=(1,)), ry=4.0, t=(0.05, 0.0, 0.05)))
        P.add(W(-0.21, -0.19, 0.0, 0.065, 0.075, 0.078, PAPER, vis=(1,)))
        P.adds(garment_folded(0.15, -0.04, w=0.20, d=0.14, h=0.04, mat=RED))
    else:
        r = random.Random(152)
        for k, m in enumerate((INDIGO, KINARI)):
            cl = W(-0.14, 0.14, 0.0, 0.004, -0.14, 0.14, m, vis=(1,))
            cl.wear = "_w2"
            P.add(xf(cl, ry=r.uniform(0, 90), t=(-0.15 + 0.25 * k, 0.0, 0.05)))
        P.add(xf(fkit.lcyl("x", 0.03, 0.0, 0.03, -0.26, 0.26, INDIGO, n=6, vis=(1,)), ry=40.0, t=(0.05, 0.0, 0.10)))
    return finish_goods(P, INDIGO)


def coin_string(x, z, L=0.18, y0=0.0, ry=0.0, wear=None):
    """A string of copper coins (zeni-sashi): coins as a segmented roll on a straw cord, knotted at the ends."""
    out = [fkit.lcyl("x", y0 + 0.012, 0.0, 0.012, -L / 2, L / 2, IRON, n=6, vis=(1,))]
    for k in range(5):
        xx = -L / 2 + L * (k + 0.5) / 5
        out.append(fkit.lcyl("x", y0 + 0.012, 0.0, 0.0135, xx - 0.004, xx + 0.004, ROPE, n=6, vis=(1,)))
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in wear_all(out, wear)]


def sg_coins(state="intact"):
    """The moneychanger's tray: strings of copper coins, silver lumps, a small lidded box of gold (shut)."""
    P = SP("sg_coins", flat=True, mass=4.0)
    if state == "intact":
        P.adds(tray(-0.08, 0.0, 0.30, 0.18, LACQ))
        for k in range(3):
            P.adds(coin_string(-0.08, -0.05 + 0.05 * k, y0=0.006, ry=3.0 * k))
        for k in range(4):
            P.add(xf(fkit.lcyl("x", 0.008, 0.0, 0.008, -0.02, 0.02, PALE, n=5, vis=(1,)), ry=30.0 * k,
                     t=(0.13 + 0.03 * (k % 2), 0.0, -0.04 + 0.03 * k)))
        P.add(W(0.17, 0.27, 0.0, 0.05, -0.04, 0.05, LACQ, vis=(1,)))
    else:
        P.adds(tray(-0.08, 0.0, 0.30, 0.18, LACQ, ry=20.0, wear="_w2"))
        P.adds(coin_string(0.15, 0.12, L=0.08, ry=70.0, wear="_w2"))
        P.add(xf(W(-0.05, 0.05, 0.0, 0.01, -0.045, 0.045, LACQ, vis=(1,)), ry=50.0, t=(0.20, 0.0, -0.02)))
    return finish_goods(P, IRON)


def senryobako(state="intact"):
    """The strong money chest (senryo-bako, 0.60 x 0.42 x 0.40): thick boards, iron bands and corner plates, a hasp
    and lock. ab: forced: the lid split and thrown back, the hasp broken, empty."""
    P = SP("senryobako", budget="small", mass=40.0)
    w, d, h = 0.60, 0.42, 0.40
    lid_h = 0.06
    P.add(board(-w / 2, w / 2, 0.0, h - lid_h, -d / 2, d / 2, k=3, vis=(1, 2)))
    for x in (-w / 2 + 0.06, 0.0, w / 2 - 0.06):
        P.add(W(x - 0.02, x + 0.02, 0.0, h - lid_h, -d / 2 - 0.006, d / 2 + 0.006, IRON, vis=(1,)))
    for sx in (-1, 1):
        for sz in (-1, 1):
            xr = (w / 2 - 0.05, w / 2 + 0.006) if sx > 0 else (-w / 2 - 0.006, -w / 2 + 0.05)
            zr = (d / 2 - 0.05, d / 2 + 0.006) if sz > 0 else (-d / 2 - 0.006, -d / 2 + 0.05)
            P.add(W(xr[0], xr[1], 0.0, 0.05, zr[0], zr[1], IRON, vis=(1,)))
    lid = [board(-w / 2, w / 2, 0.0, lid_h, -d / 2, d / 2, k=4, vis=(1, 2)),
           W(-0.05, 0.05, 0.0, lid_h + 0.004, d / 2, d / 2 + 0.008, IRON, vis=(1,))]
    if state == "intact":
        P.adds([xf(s, t=(0.0, h - lid_h, 0.0)) for s in lid])
        P.add(box(-0.03, 0.03, h - lid_h - 0.08, h - lid_h - 0.01, d / 2 + 0.006, d / 2 + 0.03, IRON, vis=(1,)))
        c = col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2)
        P.add(c)
        fkit.road_tops(P, [c], "boards")
        P.loot_rect("lid", h, -0.24, 0.24, -0.16, 0.16, rng=0.15, points=[(-0.12, h, 0.0)])
    else:
        P.adds([xf(s, rx=-105.0, pivot=(0.0, 0.0, -d / 2), t=(0.0, h - lid_h, 0.0)) for s in lid])
        P.add(W(-w / 2 + 0.03, w / 2 - 0.03, h - lid_h - 0.002, h - lid_h, -d / 2 + 0.03, d / 2 - 0.03, LACQ,
                vis=(1,)))                                           # the empty dark inside
        P.add(box(0.06, 0.12, 0.0, 0.02, d / 2 + 0.10, d / 2 + 0.14, IRON, vis=(1,)))   # the broken hasp
        P.add(col(-w / 2, w / 2, 0.0, h - lid_h, -d / 2, d / 2))
        P.add(col(-w / 2, w / 2, h - lid_h, h + 0.35, -d / 2 - 0.08, -d / 2 - 0.0))
        P.loot_rect("inside", h - lid_h, -0.22, 0.22, -0.14, 0.14, rng=0.15, points=[(0.0, h - lid_h, 0.0)])
    P.add(lod_box([s for s in P.solids if 1 in s.vis], WOOD, vis=(2,)))
    P.dim("w", w, w)
    P.notes.append("strong money chest (BTI 828); loot on the lid / in the forced chest")
    return P


def shape_fundo(state="intact"):
    """The moneychanger's sign: a balance-weight (fundo) outline, two discs joined by a notched waist, 0.60 tall,
    lacquered black with '両替' on both faces, hung perpendicular to the facade from the bracket."""
    P = SP("shape_fundo", flat=True, anchor="wall", mass=5.0)
    ab = state != "intact"
    out, _, c = kanban_parts("kanban_ryogae")
    P.adds(out)
    zc = 0.03 + ARM_L / 2 + 0.02
    yc = ARM_Y - 0.10 - 0.33
    body = []
    for dy in (0.17, -0.17):
        body.append(fkit.lcyl("x", yc + dy, zc, 0.16, -KB_T / 2, KB_T / 2, LACQ, n=10, vis=(1, 2)))
    body.append(W(-KB_T / 2, KB_T / 2, yc - 0.10, yc + 0.10, zc - 0.10, zc + 0.10, LACQ, vis=(1, 2)))
    for dz in (-0.09, 0.09):
        body.append(cord((0.0, ARM_Y, zc + dz), (0.0, yc + 0.30, zc + dz), 0.004))
    for sx in (-1, 1):
        right = (0.0, 0.0, -1.0) if sx > 0 else (0.0, 0.0, 1.0)
        body.append(stext((sx * KB_T / 2, yc, zc), right, (0.0, 1.0, 0.0), 0.40, "kanban_ryogae",
                          wear="_w2" if ab else None, off=0.003, width=0.19))
    if ab:
        body = [xf(s, rx=-18.0, rz=10.0, pivot=(0.0, ARM_Y - 0.10, zc + 0.09)) for s in body]
    P.adds(body)
    P.add(lod_box([s for s in P.solids if 1 in s.vis and not getattr(s, "_text_faced", False)], LACQ, vis=(2,)))
    P.dim("h", 0.66, 0.66)
    P.notes.append("BTI 830 says 'a coin-shaped kanban'; the fundo (balance-weight) outline is used (general), "
                   "flagged in SHOP_SETS.md")
    P.extra["hang_y"] = ARM_Y + 0.05
    return P


# ================================================================================================ books
def book_stack(x, z, k, y0=0.0, ry=0.0, wear=None, slip=None):
    """k thread-bound books (0.18 x 0.26 x 0.012 each, indigo covers), a title slip on the top cover."""
    out = []
    for i in range(k):
        out.append(W(-0.09, 0.09, y0 + 0.013 * i, y0 + 0.013 * i + 0.011, -0.13, 0.13, PAPER, vis=(1,)))
        out.append(W(-0.091, 0.091, y0 + 0.013 * i + 0.011, y0 + 0.013 * i + 0.013, -0.131, 0.131, INDIGO, vis=(1,)))
    if slip:
        top = y0 + 0.013 * k
        out.append(stext((0.05, top + 0.001, -0.02), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), 0.16, slip, off=0.0012,
                         width=0.035))
    return [xf(s, ry=ry, t=(x, 0.0, z)) for s in wear_all(out, wear)]


def sg_books(state="intact"):
    """Books laid flat for sale (stacks of thread-bound volumes with title slips), a cloth book bag. ab: scattered,
    one open face down."""
    P = SP("sg_books", flat=True, mass=3.0)
    if state == "intact":
        P.adds(book_stack(-0.18, 0.0, 6, slip="title_tsurezure"))
        P.adds(book_stack(0.03, 0.0, 4, ry=3.0, slip="title_hyakunin"))
        P.add(W(0.15, 0.27, 0.0, 0.07, -0.08, 0.08, KINARI, vis=(1,)))
    else:
        r = random.Random(161)
        for k in range(3):
            P.adds(book_stack(r.uniform(-0.2, 0.2), r.uniform(-0.02, 0.15), 1, ry=r.uniform(0, 180), wear="_w2"))
        P.add(xf(W(-0.18, 0.18, 0.0, 0.006, -0.13, 0.13, PAPER, vis=(1,)), ry=25.0, t=(0.10, 0.0, 0.12)))
    return finish_goods(P, PAPER)


def menu_board(state="intact"):
    """The cooked-food house menu: four wooden strips (0.08 x 0.42) hung from a rail on the wall (wall plane z = 0,
    1.45-1.90 up) with the dishes (nishime, simmered beans, dengaku) and 'sake'. ab: one strip down, faded."""
    P = SP("menu_board", flat=True, anchor="wall", mass=1.5)
    ab = state != "intact"
    P.add(W(-0.30, 0.30, 1.90, 1.93, 0.0, 0.03, WEATH, vis=(1,)))
    items = [("menu_nishime", SHOP), ("menu_nimame", SHOP), ("menu_dengaku", SHOP), ("kanban_miki", SUMI)]
    for k, (cell, mat) in enumerate(items):
        x = 0.21 - 0.14 * k
        strip = [board(x - 0.04, x + 0.04, 1.47, 1.89, 0.005, 0.017, k=k, vis=(1,)),
                 stext((x, 1.68, 0.017), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.36, cell, mat=mat,
                       wear="_w2" if ab else None, off=0.0012, width=0.065)]
        if ab and k == 1:
            continue
        if ab and k == 3:
            strip = [xf(s, rz=14.0, pivot=(x - 0.04, 1.89, 0.0)) for s in strip]
        P.adds(strip)
    P.add(lod_box([s for s in P.solids if 1 in s.vis and not getattr(s, "_text_faced", False)], WEATH, vis=(2,)))
    P.dim("w", 0.60, 0.60)
    P.notes.append("the menu strips of the cooked-food house (BTI 659-661); oden in broth is later, so nimono")
    return P


# ================================================================================================ registry
PROPS = [
    {"id": "jp_f_sugidama", "cat": S, "mount": "wall", "trades": ["sakaya"],
     "era": ERA_BTI % "BTI 575-578 (the cedar ball under the eaves)", "models": [
         M("jp_f_sugidama", "green", "intact", "Sugidama (cedar ball), green: new sake", lambda: sugidama("green")),
         M("jp_f_sugidama_brown", "green", "brown", "Sugidama, browned a season", lambda: sugidama("brown")),
         M("jp_f_sugidama_fallen", "green", "fallen", "Sugidama fallen at the facade foot",
           lambda: sugidama("fallen"))]},
    two("jp_f_yakudansu", F, ["kusuri"], ERA_BTI % "BTI 806-817", "floor", yakudansu,
        ("jp_f_yakudansu", "jp_f_yakudansu_ransacked"), ("Medicine drawer cabinet (hyakumi-dansu)",
                                                         "Medicine cabinet, drawers pulled out")),
    two("jp_f_yagen", F, ["kusuri"], ERA_BTI % "BTI 807, 815", "floor", yagen,
        ("jp_f_yagen", "jp_f_yagen_apart"), ("Drug chopper (yagen)", "Drug chopper, the wheel off")),
    two("jp_f_sg_medicine", G, ["kusuri"], ERA_BTI % "BTI 814-820 (Toyama Hangontan c.1690)", "surface", sg_medicine,
        ("jp_f_sg_medicine", "jp_f_sg_medicine_spilled"), ("Goods: remedy packets, medicine jars",
                                                           "Goods: packets spilled")),
    two("jp_f_pawn_board", F, ["shichiya"], ERA_BTI % "BTI 831-833", "wall", pawn_board,
        ("jp_f_pawn_board", "jp_f_pawn_board_torn"), ("Pawn-ticket board", "Pawn-ticket board, half torn off")),
    two("jp_f_sg_pawn", G, ["shichiya"], ERA_BTI % "BTI 831-833", "surface", sg_pawn,
        ("jp_f_sg_pawn", "jp_f_sg_pawn_undone"), ("Goods: pawned bundles with tags", "Goods: pawn bundles undone")),
    two("jp_f_sg_coins", G, ["ryogae", "shichiya"], ERA_BTI % "BTI 826-830", "surface", sg_coins,
        ("jp_f_sg_coins", "jp_f_sg_coins_emptied"), ("Goods: coin strings, silver, a box",
                                                     "Goods: coin tray emptied")),
    two("jp_f_senryobako", F, ["ryogae", "shichiya"], ERA_BTI % "BTI 828", "floor", senryobako,
        ("jp_f_senryobako", "jp_f_senryobako_forced"), ("Strong money chest (senryo-bako)",
                                                        "Strong money chest, forced and empty")),
    {"id": "jp_f_kanban_shape_fundo", "cat": S, "mount": "wall", "trades": ["ryogae"],
     "era": ERA_BTI % "BTI 830 ('coin-shaped kanban'); fundo outline (general), flagged", "models": [
         M("jp_f_kanban_shape_fundo", "fundo", "intact", "Shape sign: balance weight (fundo), moneychanger",
           lambda: shape_fundo()),
         M("jp_f_kanban_shape_fundo_askew", "fundo", "askew", "Shape sign: fundo hanging askew",
           lambda: shape_fundo("askew"))]},
    two("jp_f_sg_books", G, ["honya"], ERA_BTI % "BTI 500-512", "surface", sg_books,
        ("jp_f_sg_books", "jp_f_sg_books_scattered"), ("Goods: stacked books with title slips",
                                                       "Goods: books scattered")),
    two("jp_f_menu_board", F, ["nimeuri"], ERA_BTI % "BTI 657-661", "wall", menu_board,
        ("jp_f_menu_board", "jp_f_menu_board_down"), ("Menu strips (nishime, beans, dengaku, sake)",
                                                      "Menu strips, one down, faded")),
    kanban_prop("miki", "kanban_miki", "sake (o-miki)", ["sakaya"], mat=SUMI),
    kanban_prop("niuri", "kanban_niuri", "cooked food (niuri)", ["nimeuri"]),
    kanban_prop("yakushu", "kanban_yakushu", "medicines (yakushu)", ["kusuri"], mat=SUMI),
    kanban_prop("shichi", "kanban_shichi", "pawnbroker (shichi)", ["shichiya"]),
    kanban_prop("ryogae", "kanban_ryogae", "moneychanger (ryogae)", ["ryogae"]),
    kanban_prop("shorin", "kanban_shorin", "bookshop (shorin)", ["honya"]),
]
