"""Life layer H (research/interior/LIFE_LAYER.md items 63-74): streets, roads and shores, outdoor, autumn, 'as left':
the dead-world story (people fled, things dropped where they were).

Folder src/JP/site/street_life. Mounts: road (dropped travel gear, the palanquin), street (shop fronts, fire watch,
the stool, footwear), shore (nets, boats), surface (dressing for B3b's bench seats). Era verdicts:
research/interior/LIFE_LAYER_ERA.md (L2 section). Text: skit.text_ok (faces out, reads right in game).
"""
import math
import random

import l2kit as K
from l2kit import (core, box, prism, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, beam,
                   rope_path, sag, grid_sheet, text_ok, leaves, litter, add_all, ground, hull3, disc, rest, M, rng,
                   bipyramid, cord, WOOD, DARK, INT, BAMBOO, WEAVE, IRON, PALE, DARKC, LACQ, RIVER, FIELD, CUT,
                   MUSHIRO, TAWARA, ROPE, STACK, PAPER, CHOCHIN, KINARI, PLAIN, INDIGO, LEAF, EARTH, ASH, SUMI, LIFE,
                   SOOTW, NET)
import props_life_wall as LW      # L1 (read-only): kasa(), waraji(), daikon(), sandal_bunch()
import props_wood as PW           # B3b (read-only): basket(), vessel(), teoke()

CAT = "street_life"
PROPS = []


def pillow(w, d, h, mat, wear=None, vis=(1,), nx=3, nz=2, pinch=0.3):
    return K.lkit.pillow(w, d, h, mat, nx=nx, nz=nz, pinch=pinch, wear=wear, vis=vis)


# ================================================================================================ 63 travel gear
def stick(L=1.30, wear=None):
    """Walking stick (tsue), lying along +x, with a knob."""
    out = [pole((-L / 2, 0.016, 0.0), (L / 2, 0.016, 0.0), 0.015, WOOD, n=5, vis=(1, 2)),
           lathe([(0.0, 0.0), (0.025, 0.02), (0.02, 0.05), (0.0, 0.06)], 5, WOOD, vis=(1,))]
    out[-1] = xf(out[-1], rz=-90.0, t=(L / 2, 0.02, 0.0))
    return K.wear_all(out, wear)


def bundle(wear=None, burst=False):
    """A wrapping-cloth bundle (furoshiki), knotted on top; burst = cloth open and flat, contents strewn."""
    if not burst:
        out = [pillow(0.36, 0.30, 0.18, INDIGO, wear=wear, vis=(1, 2))]
        for sx in (-1, 1):
            out.append(bipyramid((sx * 0.03, 0.19, 0.0), 0.04, 0.03, 0.03, INDIGO, n=4, wear=wear))
        return out
    out = [grid_sheet(lambda u, v: (-0.4 + 0.8 * u, 0.006 + 0.02 * math.sin(3 * u + 2 * v) ** 2, -0.35 + 0.7 * v), 3, 3,
                      INDIGO, vis=(1,), two_sided=False, wear="_w2")]
    out.append(pillow(0.30, 0.22, 0.06, PLAIN, wear="_w2", vis=(1,)))        # a folded under-kimono, flattened
    out[-1] = xf(out[-1], ry=20.0, t=(-0.1, 0.006, 0.05))
    out.append(W(-0.4, 0.4, 0.0, 0.03, -0.35, 0.35, INDIGO, vis=(2,)))
    out[-1].wear = "_w2"
    return out


def travel_gear(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("travel_gear", budget="small", mass=2.0, flat=True, wear="_w2" if ab else "_w1")
    hat = LW.kasa(0.0, 0.0, 0.0, R=0.22, H=0.12, rx=180.0, wear=wear or "_w1", n=10)
    hat = rest(xfs(hat, rz=8.0), 0.0)
    if kind == "set":
        add_all(P, xfs(hat, t=(-0.55, 0.0, 0.25)))
        add_all(P, xfs(stick(), ry=-15.0, t=(0.0, 0.0, -0.25)))
        add_all(P, xfs(bundle(), ry=25.0, t=(0.45, 0.0, 0.3)))
        add_all(P, xfs(LW.waraji(), ry=60.0, t=(0.05, 0.0, 0.55)))
        P.dim("pieces", 4, 4, tol=0)
    elif kind == "hat_stick":
        add_all(P, xfs(hat, t=(0.35, 0.0, 0.2)))
        add_all(P, xfs(stick(), ry=35.0, t=(-0.2, 0.0, -0.1)))
        P.dim("pieces", 2, 2, tol=0)
    else:   # ab_burst: the bundle burst open, the hat split and crushed, a sandal
        crushed = LW.kasa(0.0, 0.0, 0.0, R=0.22, H=0.12, rx=160.0, wear="_w2", n=10)
        add_all(P, rest(xfs(crushed, t=(-0.6, 0.0, 0.1)), 0.0))
        add_all(P, xfs(bundle(burst=True), ry=-10.0, t=(0.2, 0.0, 0.1)))
        add_all(P, xfs(LW.waraji(wear="_w2"), ry=-40.0, t=(0.75, 0.0, -0.35)))
        add_all(P, xfs(stick(wear="_w2"), ry=80.0, t=(-0.15, 0.0, -0.55)))
        P.add(litter(631, 0.0, 0.0, 0.8, sx=1.5))
        P.dim("pieces", 4, 4, tol=0)
    P.notes.append("dropped travel gear: sedge hat (sugegasa), walking stick, wrapping-cloth bundle, straw sandal "
                   "(the people-fled signature); visual only")
    return P


PROPS.append({"id": "jp_s_travel_gear", "cat": CAT, "ll": "#63", "mount": "road", "tiers": [1, 2, 3],
              "models": [
                  M("jp_s_travel_gear_set", "set", "intact", "Dropped travel gear: hat, stick, bundle, sandal",
                    lambda: travel_gear("set")),
                  M("jp_s_travel_gear_hat_stick", "hat_stick", "intact", "A sedge hat and a walking stick in the road",
                    lambda: travel_gear("hat_stick")),
                  M("jp_s_travel_gear_ab_burst", "set", "abandoned", "Travel bundle burst open, hat crushed",
                    lambda: travel_gear("ab_burst")),
              ]})


# ================================================================================================ 64 palanquin (kago)
def kago_body(wear=None, roof=True, pole_on=True):
    """The open hired kago (yotsude-kago): a square base with a woven seat, four bamboo corner posts up to the
    carrying pole (along z, 3.6 m, at 1.10), a straw mat roof over the pole, a woven back rest, a rope sling."""
    out, lo2 = [], []
    out.append(W(-0.38, 0.38, 0.0, 0.08, -0.38, 0.38, DARK, vis=(1, 2)))
    out.append(W(-0.34, 0.34, 0.08, 0.10, -0.34, 0.34, WEAVE, vis=(1,)))
    out.append(W(-0.34, 0.34, 0.10, 0.55, -0.36, -0.33, WEAVE, vis=(1,)))
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(pole((sx * 0.34, 0.06, sz * 0.34), (sx * 0.06, 1.06, sz * 0.30), 0.025, BAMBOO, n=5, vis=(1, 2)))
    if pole_on:
        out.append(pole((0.0, 1.10, -1.80), (0.0, 1.10, 1.80), 0.05, DARK, n=6, vis=(1, 2), r1=0.042))
    if roof:
        out.append(grid_sheet(lambda u, v: ((u - 0.5) * 0.95, 1.16 - 0.30 * abs(u - 0.5) * 2, -0.45 + 0.9 * v), 2, 1,
                              MUSHIRO, vis=(1, 2), two_sided=True, wear=wear or "_w1"))
    for sx in (-1, 1):
        out += rope_path([(sx * 0.30, 0.55, 0.30), (sx * 0.12, 0.95, 0.25), (0.0, 1.10, 0.25)], 0.008, ROPE, n=3)
    return K.wear_all(out, wear)


def kago(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("kago", budget="medium", res3=True, mass=30.0, wear="_w2" if ab else "_w1")
    lo3 = [W(-0.38, 0.38, 0.0, 1.1, -0.38, 0.38, DARK, vis=(3,)), W(-0.04, 0.04, 1.06, 1.14, -1.8, 1.8, DARK, vis=(3,))]
    cols = [col(-0.38, 0.38, 0.0, 1.05, -0.38, 0.38, DARK), col(-0.05, 0.05, 1.05, 1.15, 0.39, 1.80, DARK),
            col(-0.05, 0.05, 1.05, 1.15, -1.80, -0.39, DARK)]
    if kind == "down":
        add_all(P, kago_body() + lo3 + cols)
        P.dim("pole_l", 3.60, 3.60, tol=0.01)
        P.dim("pole_h", 1.10, 1.10, tol=0.01)
    elif kind == "ab_tipped":
        vs, cs = K.lkit.place_group(kago_body(wear="_w2") + lo3, cols, [dict(rz=82.0)])
        add_all(P, vs + cs)
        P.add(litter(641, 0.3, 0.0, 1.0, sx=0.8, sz=1.6))
        P.dim("pole_l", 3.60, 3.60, tol=0.01)
    else:   # ab_broken: the pole thrown down beside it, two posts snapped, the roof mat in the road
        body = kago_body(wear="_w2", roof=False, pole_on=False)
        body = [s for s in body if not (s.mats == BAMBOO and s.bbox()[0] > 0.0)]
        add_all(P, body)
        for sz in (-1, 1):
            P.add(pole((0.34, 0.06, sz * 0.34), (0.22, 0.45, sz * 0.32), 0.025, BAMBOO, n=5, vis=(1, 2), wear="_w2"))
        P.add(pole((0.9, 0.05, -1.7), (1.2, 0.05, 1.9), 0.05, DARK, n=6, vis=(1, 2), wear="_w2"))
        P.add(col_solid(beam((0.9, 0.05, -1.7), (1.2, 0.05, 1.9), 0.1, 0.1, DARK)))
        mat = grid_sheet(lambda u, v: (-1.2 + 0.95 * u, 0.01 + 0.05 * math.sin(math.pi * u) * v, 0.3 + 0.9 * v), 2, 2,
                         MUSHIRO, vis=(1,), two_sided=True, wear="_w2")
        P.add(mat)
        P.add(pillow(0.40, 0.40, 0.06, INDIGO, wear="_w2", vis=(1,)))
        P.solids[-1] = xf(P.solids[-1], ry=30.0, t=(-0.1, 0.10, 0.0))
        P.add(W(-0.38, 0.38, 0.0, 0.55, -0.38, 0.38, DARK, vis=(3,)))
        P.add(col(-0.38, 0.38, 0.0, 0.55, -0.38, 0.38, DARK))
        P.add(litter(642, -0.3, 0.3, 1.0, sx=1.4))
        P.dim("pole_l", 3.60, math.hypot(0.3, 3.6), tol=0.02)
    P.notes.append("the open hired palanquin (yotsude-kago) of streets and highways, set down where its bearers "
                   "dropped it (era: LIFE_LAYER_ERA.md #64); not the lacquered norimono")
    return P


PROPS.append({"id": "jp_s_kago", "cat": CAT, "ll": "#64", "mount": "road", "tiers": [1, 2, 3],
              "models": [
                  M("jp_s_kago_down", "yotsude", "intact", "Palanquin (kago) set down in the road",
                    lambda: kago("down")),
                  M("jp_s_kago_ab_tipped", "yotsude", "abandoned", "Palanquin tipped on its side", lambda: kago("ab_tipped")),
                  M("jp_s_kago_ab_broken", "yotsude", "abandoned", "Palanquin broken, pole thrown down, roof mat in the "
                    "road", lambda: kago("ab_broken")),
              ]})


# ================================================================================================ 65 tenbin spill (extends B3b's tenbin)
def peddler_box(w=0.40, d=0.30, h=0.25, lid=True, wear=None, name=None):
    """A peddler's wooden box (the B3b tenbin 'boxes' load, dark wood), optional lid and a shop name on its front."""
    out = [W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, DARK, vis=(1, 2))]
    if lid:
        out.append(W(-w / 2 - 0.01, w / 2 + 0.01, h, h + 0.03, -d / 2 - 0.01, d / 2 + 0.01, DARK, vis=(1,)))
    if name:
        out.append(text_ok((0.0, h * 0.5, d / 2), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), h * 0.8, LIFE, name, wear="_w1",
                           off=0.003))
    return K.wear_all(out, wear)


def packets(seed, cx, cz, n, spread=0.35, wear="_w2"):
    r = random.Random(seed)
    out = []
    for k in range(n):
        a, dd = r.uniform(0, 2 * math.pi), r.uniform(0.05, spread)
        w, d, h = r.uniform(0.08, 0.14), r.uniform(0.06, 0.10), r.uniform(0.03, 0.06)
        b = W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, PLAIN if k % 2 else PAPER, vis=(1,))
        b.wear = wear
        out.append(xf(b, ry=r.uniform(0, 180), t=(cx + dd * math.cos(a), 0.0, cz + dd * math.sin(a))))
    return out


def tenbin_spill(kind):
    P = SPart("tenbin_spill", budget="small", mass=12.0, wear="_w2")
    pole_ = beam((-0.85, 0.03, 0.15), (0.80, 0.03, -0.20), 0.05, 0.03, WOOD, vis=(1, 2), wear="_w2")
    P.add(pole_)
    P.add(col_solid(beam((-0.85, 0.03, 0.15), (0.80, 0.03, -0.20), 0.05, 0.03, WOOD)))
    if kind == "boxes":
        add_all(P, xfs(peddler_box(name="chochin_iseya", wear="_w2"), ry=10.0, t=(-0.75, 0.0, 0.55)))
        P.add(xf(col(-0.20, 0.20, 0.0, 0.28, -0.15, 0.15, DARK), ry=10.0, t=(-0.75, 0.0, 0.55)))
        ov = peddler_box(lid=False, wear="_w2")
        ov = rest(xfs(ov, rx=90.0, ry=-30.0, t=(0.55, 0.0, 0.55)), 0.0)
        add_all(P, ov)
        P.add(hull3([v for s in ov for v in s.verts], DARK))
        lid = W(-0.21, 0.21, 0.0, 0.03, -0.16, 0.16, DARK, vis=(1,))
        lid.wear = "_w2"
        P.add(xf(lid, ry=50.0, t=(0.15, 0.0, 0.95)))
        add_all(P, packets(651, 0.75, 0.95, 7))
        P.dim("boxes", 2, 2, tol=0)
    elif kind == "fish":
        for i, (x, z, flip) in enumerate(((-0.7, 0.5, True), (0.6, 0.5, False))):
            tub = PW.vessel(0.26, 0.30, 0.16, n=12, fill=None, hoops=(0.04, 0.12), wear="_w2", lod2=True)
            cc = [cyl_col(0.30, 0.0, 0.16, n=8)]
            if flip:
                tub, cc = xfs(tub, rz=180.0, t=(0.0, 0.16, 0.0)), xfs(cc, rz=180.0, t=(0.0, 0.16, 0.0))
            else:
                tub, cc = K.lkit.place_group(tub, cc, [dict(rx=75.0)])
            add_all(P, xfs(tub, t=(x, 0.0, z)) + xfs(cc, t=(x, 0.0, z)))
        r = random.Random(652)
        for k in range(6):                       # dried fish, black
            P.add(xf(bipyramid((0.0, 0.015, 0.0), 0.015, 0.09, 0.03, SOOTW, n=4, wear="_w2"), rz=90.0,
                     ry=r.uniform(0, 180), t=(0.1 + r.uniform(-0.3, 0.3), 0.015, 0.95 + r.uniform(-0.2, 0.2))))
        P.add(K.mound(653, 0.1, 0.95, 0.25, 0.03, LEAF, sx=1.4, wear="_w2", vis=(1,)))
        P.dim("tubs", 2, 2, tol=0)
    else:   # vegetables: two baskets, one overturned, shrivelled daikon and rotted greens
        b1 = PW.basket(wear="_w2", fill=leaves(654, 0.0, 0.0, 0.17, 0.17, wear="_w2"))
        add_all(P, xfs(b1, t=(-0.75, 0.0, 0.5)))
        P.add(cyl_col(0.225, 0.0, 0.25, n=6, cx=-0.75, cz=0.5))
        b2 = xfs(PW.basket(wear="_w2"), rz=180.0, t=(0.0, 0.25, 0.0))
        c2 = xfs([cyl_col(0.225, 0.0, 0.25, n=6)], rz=180.0, t=(0.0, 0.25, 0.0))
        b2, c2 = K.lkit.place_group(b2, c2, [dict(rz=15.0, t=(0.65, 0.0, 0.55))])
        add_all(P, b2 + c2)
        r = random.Random(655)
        for k in range(5):
            d = LW.daikon((0.0, 0.0, 0.0), L=0.34, r=0.03, wear="_w2", bend=r.uniform(-10, 10))
            d = rest(xfs(d, rz=90.0, ry=r.uniform(0, 180)), 0.0)
            add_all(P, xfs(d, t=(0.25 + r.uniform(-0.3, 0.4), 0.0, 1.0 + r.uniform(-0.2, 0.25))))
        P.add(K.mound(656, 0.3, 0.95, 0.3, 0.05, LEAF, sx=1.5, wear="_w2", vis=(1,)))
        P.dim("baskets", 2, 2, tol=0)
    P.add(litter(657, 0.0, 0.6, 0.8, sx=1.5))
    ground(P)
    P.notes.append("extends B3b's jp_s_tenbin: the peddler's load overturned where the carrier dropped it")
    return P


PROPS.append({"id": "jp_s_tenbin_spill", "cat": CAT, "ll": "#65", "mount": "street", "tiers": [2, 3],
              "refs": ["k28_kusakabe_peddler"],
              "models": [
                  M("jp_s_tenbin_spill_boxes", "boxes", "abandoned", "Peddler's boxes overturned, goods spilled",
                    lambda: tenbin_spill("boxes")),
                  M("jp_s_tenbin_spill_fish", "fish", "abandoned", "Fish seller's tubs overturned, fish dried black",
                    lambda: tenbin_spill("fish")),
                  M("jp_s_tenbin_spill_veg", "baskets", "abandoned", "Vegetable baskets overturned, daikon rotted",
                    lambda: tenbin_spill("veg"), mount="road"),
              ]})


# ================================================================================================ 70 bench dressing
def cup(c, r=0.036, h=0.06, mat=DARKC, tipped=False):
    s = lathe([(r * 0.7, 0.0), (r, h), (r - 0.004, h), (r * 0.7 - 0.004, 0.006), (0.0, 0.006)], 7, mat, vis=(1,))
    if tipped:
        s = rest([xf(s, rx=90.0)], 0.0)[0]
    return xf(s, t=c)


def tabako_bon(wear=None):
    """Tobacco tray: a small open wooden box with a handle arch, a clay fire pot with ash, a bamboo ash tube, and a
    long pipe (kiseru) lying across it."""
    out = [W(-0.12, 0.12, 0.0, 0.012, -0.08, 0.08, WOOD, vis=(1, 2))]
    for sx in (-1, 1):
        out.append(W(sx * 0.12 - 0.01 * (sx > 0), sx * 0.12 + 0.01 * (sx < 0), 0.0, 0.10, -0.08, 0.08, WOOD, vis=(1,)))
        out.append(W(-0.11, 0.11, 0.0, 0.10, sx * 0.08 - 0.008 * (sx > 0), sx * 0.08 + 0.008 * (sx < 0), WOOD, vis=(1,)))
        out.append(W(sx * 0.005 - 0.005, sx * 0.005 + 0.005, 0.10, 0.22, -0.01, 0.01, WOOD, vis=(1,)))
    out.append(W(-0.03, 0.03, 0.21, 0.23, -0.01, 0.01, WOOD, vis=(1,)))
    out.append(lathe([(0.035, 0.012), (0.045, 0.08), (0.04, 0.08), (0.0, 0.07)], 6, DARKC, vis=(1,)))
    out[-1] = xf(out[-1], t=(-0.06, 0.0, 0.0))
    out.append(disc(0.036, 0.07, 0.072, ASH, n=6, vis=(1,), cx=-0.06))
    out.append(lathe([(0.025, 0.012), (0.025, 0.09), (0.0, 0.09)], 5, BAMBOO, vis=(1,)))
    out[-1] = xf(out[-1], t=(0.06, 0.0, 0.0))
    out.append(pole((-0.14, 0.108, -0.05), (0.14, 0.108, 0.07), 0.004, BAMBOO, n=3, vis=(1,)))
    out.append(W(-0.12, 0.12, 0.0, 0.10, -0.08, 0.08, WOOD, vis=(2,)))
    return K.wear_all(out, wear)


def bench_dress(kind):
    ab = kind.startswith("ab")
    P = SPart("bench_dress", budget="small", mass=0.5, flat=True, wear="_w2" if ab else "_w1")
    tray = W(-0.15, 0.15, 0.0, 0.015, -0.10, 0.10, WOOD, vis=(1, 2))
    if kind == "tea":
        P.add(tray)
        P.add(cup((-0.06, 0.015, 0.0)))
        P.add(cup((0.07, 0.015, 0.02), mat=PALE))
        P.dim("cups", 2, 2, tol=0)
    elif kind == "tobacco":
        add_all(P, tabako_bon())
        P.add(cup((0.25, 0.0, 0.05)))
        P.dim("tray_w", 0.24, 0.24, tol=0.01)
    elif kind == "cloth":
        P.add(W(-0.16, 0.16, 0.0, 0.02, -0.05, 0.05, PLAIN, vis=(1, 2)))
        P.solids[-1] = xf(P.solids[-1], ry=12.0, t=(-0.05, 0.0, 0.0))
        P.add(cup((0.18, 0.0, 0.06), tipped=True))
        P.dim("cloth_l", 0.32, 0.32, tol=0.01)
    else:   # ab_spilled: tray askew, cups knocked over, the tobacco tray tipped and its ash spilled
        P.add(xf(tray, ry=25.0, t=(-0.25, 0.0, 0.0)))
        P.solids[-1].wear = "_w2"
        P.add(cup((-0.22, 0.015, 0.02), tipped=True))
        tb = rest(xfs(tabako_bon("_w2"), rz=90.0, t=(0.2, 0.0, 0.0)), 0.0)
        add_all(P, tb)
        P.add(K.mound(701, 0.30, 0.02, 0.08, 0.012, ASH, sx=1.6, wear="_w2", vis=(1,)))
        P.dim("pieces", 3, 3, tol=0)
    P.notes.append("dressing for B3b's bench seats (jp_s_bench_*): decor.on_surface(name, bench); base = the seat "
                   "top. Stoneware cups, no porcelain choko (L1 #20 ruling); tobacco tray and kiseru (BUILDING_LIST 5)")
    return P


PROPS.append({"id": "jp_s_bench_dress", "cat": CAT, "ll": "#70", "mount": "surface", "tiers": [2, 3],
              "refs": ["i38_morse_tabakobon"],
              "models": [
                  M("jp_s_bench_dress_tea", "tea", "intact", "Tea tray with two cups (bench dressing)",
                    lambda: bench_dress("tea")),
                  M("jp_s_bench_dress_tobacco", "tobacco", "intact", "Tobacco tray, pipe and a cup (bench dressing)",
                    lambda: bench_dress("tobacco")),
                  M("jp_s_bench_dress_cloth", "cloth", "intact", "Folded cloth and a tipped cup (bench dressing)",
                    lambda: bench_dress("cloth")),
                  M("jp_s_bench_dress_ab_spilled", "tobacco", "abandoned", "Cups knocked over, tobacco tray tipped, ash "
                    "spilled (bench dressing)", lambda: bench_dress("ab_spilled")),
              ]})


# ================================================================================================ 73 stool
def stool_parts(wear=None):
    out = [W(-0.225, 0.225, 0.37, 0.40, -0.125, 0.125, WOOD, vis=(1, 2))]
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(beam((sx * 0.17, 0.0, sz * 0.09), (sx * 0.15, 0.37, sz * 0.08), 0.035, 0.035, WOOD, vis=(1, 2)))
        out.append(W(sx * 0.16 - 0.015, sx * 0.16 + 0.015, 0.12, 0.15, -0.09, 0.09, WOOD, vis=(1,)))
    lo3 = [W(-0.225, 0.225, 0.0, 0.40, -0.125, 0.125, WOOD, vis=(3,))]
    cols = [col(-0.225, 0.225, 0.37, 0.40, -0.125, 0.125), col(-0.19, 0.19, 0.0, 0.365, -0.11, 0.11)]
    return K.wear_all(out, wear), lo3, cols


def stool(kind):
    ab = kind.startswith("ab")
    P = SPart("stool", budget="small", res3=True, mass=5.0, wear="_w2" if ab else "_w1")
    ss, lo3, cs = stool_parts(wear="_w2" if ab else None)
    if kind == "std":
        add_all(P, ss + lo3 + cs)
        import fkit                                     # F1: a player may stand on the stool seat (vanilla benches)
        fkit.road_tops(P, cs[:1], "boards_ext")
    elif kind == "ab_tipped":
        vs, cs = K.lkit.place_group(ss + lo3, cs, [dict(rz=90.0)])
        add_all(P, vs + cs)
        P.add(litter(731, 0.0, 0.1, 0.4))
    else:   # ab_broken: one leg gone, the stool slumped on its corner, the leg in the leaves
        ss = [s for s in ss if not (s.bbox()[0] > 0.1 and s.bbox()[4] > 0.0 and s.bbox()[3] < 0.38)]
        vs, cs = K.lkit.place_group(ss + lo3, cs[:1], [dict(rz=-14.0, rx=10.0)])
        add_all(P, vs + cs)
        leg = beam((0.0, 0.0, 0.0), (0.0, 0.37, 0.0), 0.035, 0.035, WOOD, vis=(1,), wear="_w2")
        P.add(rest([xf(leg, rz=88.0, ry=30.0, t=(0.45, 0.0, 0.25))], 0.0)[0])
        P.add(litter(732, 0.1, 0.1, 0.4))
    P.dim("seat_h", 0.40, 0.40, tol=0.01)
    P.dim("seat_w", 0.45, 0.45, tol=0.01)
    return P


PROPS.append({"id": "jp_s_stool", "cat": CAT, "ll": "#73", "mount": "street", "tiers": [1, 2, 3],
              "models": [
                  M("jp_s_stool_std", "std", "intact", "Wooden stool", lambda: stool("std")),
                  M("jp_s_stool_ab_tipped", "std", "abandoned", "Wooden stool knocked over", lambda: stool("ab_tipped")),
                  M("jp_s_stool_ab_broken", "std", "abandoned", "Wooden stool, a leg broken off",
                    lambda: stool("ab_broken"), mount="yard"),
              ]})


# ================================================================================================ 74 footwear
def geta(wear=None, broken=False):
    """Two-tooth paulownia clog 0.22 x 0.09, teeth 0.05, cloth thong (lying the right way up, toe +z)."""
    out = [W(-0.045, 0.045, 0.05, 0.075, -0.11, 0.11, WOOD, vis=(1,)),
           W(-0.045, 0.045, 0.0, 0.05, 0.05, 0.065, WOOD, vis=(1,)),
           W(-0.045, 0.045, 0.0, 0.05, -0.07, -0.055, WOOD, vis=(1,))]
    if broken:
        out += rope_path([(-0.035, 0.078, -0.01), (0.0, 0.10, 0.05)], 0.006, INDIGO, n=3)
    else:
        out += rope_path([(-0.035, 0.078, -0.01), (0.0, 0.10, 0.06), (0.035, 0.078, -0.01)], 0.006, INDIGO, n=3)
    return K.wear_all(out, wear)


def zori(wear=None):
    out = [W(-0.045, 0.045, 0.0, 0.015, -0.115, 0.115, MUSHIRO, vis=(1,))]
    out += rope_path([(-0.035, 0.018, -0.01), (0.0, 0.035, 0.07), (0.035, 0.018, -0.01)], 0.005, PLAIN, n=3)
    return K.wear_all(out, wear)


def footwear(kind):
    ab = kind.startswith("ab")
    P = SPart("footwear", budget="box", mass=1.0, flat=True, wear="_w2" if ab else "_w1")   # FP2: thongs at 2.5x
    if kind == "pairs":
        for x in (-0.30, 0.10):
            for sx in (-1, 1):
                add_all(P, xfs(geta(), t=(x + sx * 0.06, 0.0, 0.0)))
        for sx in (-1, 1):
            add_all(P, xfs(zori(), t=(0.45 + sx * 0.06, 0.0, 0.05)))
        P.dim("pairs", 3, 3, tol=0)
    elif kind == "ab_scattered":
        r = random.Random(741)
        for k in range(4):
            g = geta(wear="_w2")
            if k == 1:
                g = rest(xfs(g, rz=90.0), 0.0)
            elif k == 2:
                g = xfs(g, rz=180.0, t=(0.0, 0.10, 0.0))
            add_all(P, xfs(g, ry=r.uniform(0, 360), t=(r.uniform(-0.6, 0.6), 0.0, r.uniform(-0.3, 0.4))))
        add_all(P, xfs(LW.waraji(wear="_w2"), ry=40.0, t=(0.5, 0.0, 0.5)))
        P.add(litter(742, 0.0, 0.1, 0.7, sx=1.4))
        P.dim("pieces", 5, 5, tol=0)
    else:   # ab_single: one clog, thong broken
        add_all(P, xfs(geta(wear="_w2", broken=True), ry=30.0))
        P.dim("pieces", 1, 1, tol=0)
    P.add(W(-0.5, 0.5, 0.0, 0.02, -0.15, 0.15, WOOD, vis=(2,)) if kind == "pairs" else
          W(-0.1, 0.1, 0.0, 0.02, -0.1, 0.1, WOOD, vis=(2,)))
    P.notes.append("clogs (geta) and sandals left at an entrance (BUILDING_LIST 1386); visual only")
    return P


PROPS.append({"id": "jp_s_footwear", "cat": CAT, "ll": "#74", "mount": "street", "tiers": [2, 3],
              "models": [
                  M("jp_s_footwear_pairs", "pairs", "intact", "Clogs and sandals at an entrance",
                    lambda: footwear("pairs")),
                  M("jp_s_footwear_ab_scattered", "pairs", "abandoned", "Clogs scattered, one upside down",
                    lambda: footwear("ab_scattered")),
                  M("jp_s_footwear_ab_single", "single", "abandoned", "A single clog, thong broken",
                    lambda: footwear("ab_single"), mount="road"),
              ]})


# ================================================================================================ 66 fishing nets
def net_span(xa, xb, top, drop_f, drop_b, wear=None, seed=1, vis=(1,), nu=4, nv=4, sway=0.0):
    """A net hung over a rail at `top` between xa and xb: the front part drops drop_f, the back drop_b (two-sided,
    alpha-cut jp_m_textile_net)."""
    r = random.Random(seed)
    jig = [r.uniform(-0.06, 0.06) for _ in range(nu + 1)]

    def f(u, v):
        t = 2 * v - 1                        # -1 = front hem, 0 = over the rail, 1 = back hem
        d = drop_f if t < 0 else drop_b
        y = top + 0.01 - d * abs(t) ** 1.1 + (jig[int(round(u * nu))] if abs(t) > 0.9 else 0.0)
        z = 0.06 * t + 0.08 * math.sin(math.pi * u) * abs(t) * (1 if t < 0 else -1) + sway * abs(t)
        return (xa + (xb - xa) * u, y, z)
    return grid_sheet(f, nu, nv, NET, vis=vis, two_sided=True, wear=wear)


def floats_row(x0, x1, y, z, n, wear=None, seed=1):
    """Wooden net floats (ukiki): small turned cylinders along the hem (wood, never glass)."""
    r = random.Random(seed)
    out = []
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        s = lathe([(0.0, -0.05), (0.026, -0.04), (0.03, 0.0), (0.026, 0.04), (0.0, 0.05)], 5, WOOD, vis=(1,), wear=wear)
        out.append(xf(s, rz=90.0 + r.uniform(-20, 20), t=(x, y + r.uniform(-0.03, 0.03), z)))
    return out


def sinkers_row(x0, x1, y, z, n, wear=None):
    out = []
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        b = W(-0.02, 0.02, -0.035, 0.0, -0.02, 0.02, DARKC, vis=(1,))
        if wear:
            b.wear = wear
        out.append(xf(b, t=(x, y, z)))
    return out


def fishnet(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("fishnet", budget="box", mass=20.0, bury=0.32, wear="_w2" if ab else "_w1")
    top = 2.20
    if kind in ("poles", "small"):
        xs = (-1.8, 0.0, 1.8) if kind == "poles" else (-0.9, 0.9)
        for x in xs:
            P.add(pole((x, -0.30, 0.0), (x, 2.45, 0.0), 0.035, BAMBOO, n=6, vis=(1, 2), r1=0.028))
            P.add(col(x - 0.035, x + 0.035, -0.30, 2.45, -0.035, 0.035, BAMBOO))
        P.add(pole((xs[0] - 0.15, top, 0.0), (xs[-1] + 0.15, top, 0.0), 0.02, BAMBOO, n=5, vis=(1, 2)))
        for i, (xa, xb) in enumerate(zip(xs, xs[1:])):
            P.add(net_span(xa + 0.06, xb - 0.06, top + 0.02, 1.55, 1.25, seed=660 + i))
            add_all(P, floats_row(xa + 0.1, xb - 0.1, top + 0.02 - 1.55, -0.07, 6, seed=661 + i))
            add_all(P, sinkers_row(xa + 0.1, xb - 0.1, top + 0.02 - 1.25, 0.07, 6))
            P.add(W(xa, xb, top - 1.4, top, -0.04, 0.04, NET, vis=(2,)))
        P.dim("rail_h", 2.20, top, tol=0.01)
        P.dim("span", 1.8, xs[1] - xs[0], tol=0.01)
    elif kind == "ab_down":
        # the middle pole snapped: its top half lies on the sand, the net slumped to the ground from the left pole
        P.add(pole((-1.8, -0.30, 0.0), (-1.8, 2.45, 0.0), 0.035, BAMBOO, n=6, vis=(1, 2), r1=0.028, wear=wear))
        P.add(col(-1.835, -1.765, -0.30, 2.45, -0.035, 0.035, BAMBOO))
        P.add(pole((0.0, -0.30, 0.0), (0.0, 0.9, 0.0), 0.035, BAMBOO, n=6, vis=(1, 2), wear=wear))
        P.add(col(-0.035, 0.035, -0.30, 0.9, -0.035, 0.035, BAMBOO))
        P.add(pole((0.1, 0.03, 0.2), (1.7, 0.03, 0.9), 0.03, BAMBOO, n=6, vis=(1, 2), wear=wear))
        P.add(col_solid(beam((0.1, 0.03, 0.2), (1.7, 0.03, 0.9), 0.06, 0.06, BAMBOO)))
        sl = grid_sheet(lambda u, v: (-1.75 + 1.9 * u, max(0.02, (2.2 - 2.4 * u) * (1 - v)) + 0.03 * math.sin(7 * u + v),
                                      0.05 + 0.9 * v * (0.3 + u)), 4, 3, NET, vis=(1,), two_sided=True, wear="_w2")
        P.add(sl)
        P.add(pillow(0.9, 0.6, 0.14, NET, wear="_w2", vis=(1,)))
        P.solids[-1] = xf(P.solids[-1], ry=20.0, t=(0.8, 0.0, 0.55))
        add_all(P, floats_row(0.3, 1.4, 0.03, 0.9, 5, wear="_w2", seed=662))
        P.add(W(-1.8, 1.7, 0.0, 1.0, 0.0, 0.9, NET, vis=(2,)))
        P.add(litter(663, 0.0, 0.5, 1.0, sx=1.8))
        P.dim("span", 1.8, 1.8, tol=0.01)
    else:   # heap: a net heaped on the sand to mend, floats and sinkers showing
        P.need = ()
        P.flat = True
        P.bury = 0.02
        P.add(pillow(1.1, 0.8, 0.22, NET, wear="_w1", vis=(1,)))
        P.add(xf(pillow(0.8, 0.6, 0.16, NET, wear="_w2", vis=(1,)), ry=35.0, t=(0.2, 0.0, 0.1)))
        add_all(P, floats_row(-0.6, 0.6, 0.06, 0.5, 6, seed=664))
        add_all(P, sinkers_row(-0.5, 0.5, 0.035, -0.45, 5))
        P.add(W(-0.55, 0.55, 0.0, 0.2, -0.4, 0.4, NET, vis=(2,)))
        P.dim("heap_w", 1.1, 1.1, tol=0.01)
    P.notes.append("nets drying on bamboo poles (BUILDING_LIST 343-346, 1766-1767); wooden floats, clay sinkers, "
                   "never glass; nets are alpha-cut (see-through), only the poles collide")
    return P


PROPS.append({"id": "jp_s_fishnet", "cat": CAT, "ll": "#66", "mount": "shore", "tiers": [1, 2],
              "models": [
                  M("jp_s_fishnet_poles", "poles", "intact", "Fishing nets drying on three bamboo poles",
                    lambda: fishnet("poles")),
                  M("jp_s_fishnet_small", "small", "intact", "A fishing net drying on two poles",
                    lambda: fishnet("small")),
                  M("jp_s_fishnet_heap", "heap", "intact", "A fishing net heaped on the sand", lambda: fishnet("heap")),
                  M("jp_s_fishnet_ab_down", "poles", "abandoned", "Net drying poles snapped, the net slumped",
                    lambda: fishnet("ab_down")),
              ]})


# ================================================================================================ 67 small boat
def boat_stations(n=9):
    """(z, half-width gunwale, half-width bottom, bottom y, gunwale y) from the stern (z -2.6) to the bow (z +2.6)."""
    out = []
    for i in range(n):
        s = i / (n - 1)
        z = -2.6 + 5.2 * s
        if s < 0.55:
            wg = 0.46 + 0.16 * math.sin(math.pi * s / 1.1)
            wb = 0.36 + 0.10 * math.sin(math.pi * s / 1.1)
        else:
            k = (s - 0.55) / 0.45
            wg = 0.62 * (1 - k ** 1.6) + 0.04 * k
            wb = 0.46 * (1 - k ** 1.3) + 0.02 * k
        yb = 0.0 if s < 0.6 else 0.36 * ((s - 0.6) / 0.4) ** 1.6
        yg = 0.45 - 0.04 * math.sin(math.pi * s) + 0.22 * max(0.0, s - 0.7) / 0.3
        out.append((z, wg, wb, yb, yg))
    return out


def hull_shell(st, t=0.03, mat=WOOD, wear=None, vis=(1,), skip_side=()):
    """Open plank hull from stations: outer bottom + sides, inner bottom + sides (offset t), gunwale strips, transom,
    stem. Sheets with explicit normals (the shape is not convex). skip_side: station indices whose left side plank is
    missing (rotten)."""
    Lb = [(-wb, yb, z) for z, wg, wb, yb, yg in st]
    Rb = [(wb, yb, z) for z, wg, wb, yb, yg in st]
    Lg = [(-wg, yg, z) for z, wg, wb, yb, yg in st]
    Rg = [(wg, yg, z) for z, wg, wb, yb, yg in st]
    iLb = [(-wb + t, yb + t, z) for z, wg, wb, yb, yg in st]
    iRb = [(wb - t, yb + t, z) for z, wg, wb, yb, yg in st]
    iLg = [(-wg + t, yg, z) for z, wg, wb, yb, yg in st]
    iRg = [(wg - t, yg, z) for z, wg, wb, yb, yg in st]
    down, up = (lambda p: (0.0, -1.0, 0.0)), (lambda p: (0.0, 1.0, 0.0))
    out = [K.strip(Lb, Rb, mat, down, vis=vis, wear=wear), K.strip(iLb, iRb, mat, up, vis=vis, wear=wear)]
    if skip_side:
        keep = [i for i in range(len(st) - 1) if i not in skip_side]
        for i in keep:
            out.append(K.strip(Lb[i:i + 2], Lg[i:i + 2], mat, lambda p: (-1.0, 0.0, 0.0), vis=vis, wear=wear))
            out.append(K.strip(iLb[i:i + 2], iLg[i:i + 2], mat, lambda p: (1.0, 0.0, 0.0), vis=vis, wear=wear))
    else:
        out.append(K.strip(Lb, Lg, mat, lambda p: (-1.0, 0.0, 0.0), vis=vis, wear=wear))
        out.append(K.strip(iLb, iLg, mat, lambda p: (1.0, 0.0, 0.0), vis=vis, wear=wear))
    out.append(K.strip(Rb, Rg, mat, lambda p: (1.0, 0.0, 0.0), vis=vis, wear=wear))
    out.append(K.strip(iRb, iRg, mat, lambda p: (-1.0, 0.0, 0.0), vis=vis, wear=wear))
    out.append(K.strip(Lg, iLg, mat, up, vis=vis, wear=wear))
    out.append(K.strip(iRg, Rg, mat, up, vis=vis, wear=wear))
    z0, wg0, wb0, yb0, yg0 = st[0]
    tr = [(-wb0, yb0, z0), (wb0, yb0, z0), (wg0, yg0, z0), (-wg0, yg0, z0)]
    out.append(K.quad_sheet(tr, mat, (0.0, 0.0, -1.0), vis=vis, wear=wear))
    out.append(K.quad_sheet([(p[0] * 0.9, p[1] + (t if p[1] == yb0 else 0.0), p[2] + t) for p in tr], mat,
                            (0.0, 0.0, 1.0), vis=vis, wear=wear))
    zb, wgb, wbb, ybb, ygb = st[-1]
    out.append(beam((0.0, ybb - 0.02, zb - 0.02), (0.0, ygb + 0.06, zb + 0.10), 0.07, 0.07, mat, vis=vis, wear=wear))
    return out


def boat_parts(wear=None, rotten=False):
    st = boat_stations()
    ss = hull_shell(st, wear=wear, skip_side=(3, 4) if rotten else ())
    lo = hull_shell(boat_stations(5), vis=(2,), wear=wear)
    lo = [s for s in lo if len(s.faces) > 1 or s.fn[0][1] > -0.5 or True]
    lo3 = [W(-0.55, 0.55, 0.0, 0.45, -2.6, 2.6, WOOD, vis=(3,))]
    for z in (-0.9, 0.6):
        ss.append(W(-0.52, 0.52, 0.34, 0.37, z - 0.12, z + 0.12, WOOD, vis=(1,)))
    ss.append(pole((-0.3, 0.06, -2.2), (0.35, 0.35, 1.3), 0.02, WOOD, n=4, vis=(1,)))       # the sculling oar (ro)
    ss.append(xf(W(-0.07, 0.07, 0.0, 0.015, -0.35, 0.0, WOOD, vis=(1,)), t=(-0.3, 0.05, -2.2)))
    ss.append(K.flat_coil(0.2, -1.6, 0.14, 0.02, ROPE, n=8, m=3))
    ss[-1] = xf(ss[-1], t=(0.0, 0.03, 0.0))
    ss.append(leaves(671, 0.0, -0.3, 0.3, 0.035, wear="_w2", sx=1.0, sz=4.0))
    cols = [col(-0.60, 0.60, 0.0, 0.45, -2.6, 1.2, WOOD),
            hull3([(-0.6, 0.02, 1.2), (0.6, 0.02, 1.2), (-0.6, 0.45, 1.2), (0.6, 0.45, 1.2), (-0.05, 0.36, 2.6),
                   (0.05, 0.36, 2.6), (-0.05, 0.70, 2.6), (0.05, 0.70, 2.6)], WOOD)]
    return K.wear_all(ss, wear), lo + lo3, cols


def boat(kind):
    ab = kind.startswith("ab")
    P = SPart("boat", budget="box", res3=True, mass=150.0, wear="_w2" if ab else "_w1")
    ss, lo, cs = boat_parts(wear="_w2" if ab else None, rotten=kind == "ab_rotten")
    if kind == "up":
        add_all(P, ss + lo + cs)
    elif kind == "tilted":
        ops = [dict(rz=18.0)]
    elif kind == "upturned":
        ss = [s for s in ss if s.mats == WOOD and s.bbox()[3] - s.bbox()[2] > 0.1 or s.mats == WOOD and len(s.faces) > 2]
        ops = [dict(rz=180.0)]
    else:
        ops = [dict(rx=-3.0)]
    if kind != "up":
        allv = xfs(ss + lo, **ops[0])
        allc = xfs(cs, **ops[0])
        lo_y = min(v[1] for s in allv for v in s.verts) - (0.16 if kind == "upturned" else 0.0)
        add_all(P, xfs(allv, t=(0.0, -lo_y, 0.0)) + xfs(allc, t=(0.0, -lo_y, 0.0)))
        if kind == "upturned":
            for z in (-1.3, 1.0):          # two logs under the upturned hull
                P.add(K.lkit.lcyl("x", 0.08, z, 0.08, -0.8, 0.8, WOOD, n=6, vis=(1, 2)))
                P.add(col(-0.8, 0.8, 0.0, 0.155, z - 0.07, z + 0.07, WOOD))
        P.add(litter(672, 0.0, 0.0, 1.2, sx=0.8, sz=2.4))
        if kind == "ab_rotten":
            P.bury = 0.06
            P.solids = [xf(s, t=(0.0, -0.05, 0.0)) for s in P.solids]
    P.dim("length", 5.2, 5.2, tol=0.02)
    P.dim("beam", 1.24, 1.24, tol=0.02)
    P.notes.append("a small plank boat pulled up on a bank, sculling oar (ro) inside (BUILDING_LIST 5: boats 26); "
                   "one Geometry block + a bow wedge: cover, not a vehicle")
    return P


PROPS.append({"id": "jp_s_boat", "cat": CAT, "ll": "#67", "mount": "shore", "tiers": [1, 2],
              "refs": ["x31_masanobu_ryogoku_1748"],
              "models": [
                  M("jp_s_boat_up", "plank", "intact", "Small plank boat pulled up on a bank", lambda: boat("up")),
                  M("jp_s_boat_tilted", "plank", "intact", "Small boat on the bank, rolled on its bilge",
                    lambda: boat("tilted")),
                  M("jp_s_boat_upturned", "plank", "abandoned", "Small boat upturned on two logs",
                    lambda: boat("upturned")),
                  M("jp_s_boat_ab_rotten", "plank", "abandoned", "Small boat rotting on the bank, side planks gone",
                    lambda: boat("ab_rotten")),
              ]})


# ================================================================================================ 68 fire watch gear
import props_street as PS         # noqa: E402  B3b (read-only): chochin(), box_lamp()

EAVE_Y = 2.40


def fire_hook(L=2.2, wear=None):
    """Tobiguchi: a long oak pole with an iron hook head (the fireman's tool), built lying along +x."""
    out = [pole((-L / 2, 0.0, 0.0), (L / 2, 0.0, 0.0), 0.02, WOOD, n=5, vis=(1, 2))]
    out.append(box(L / 2 - 0.02, L / 2 + 0.06, -0.02, 0.02, -0.012, 0.012, IRON, vis=(1,)))
    out.append(xf(prism([(0.0, 0.0), (0.02, 0.0), (0.02, -0.13), (-0.01, -0.10)], "z", -0.006, 0.006, IRON, vis=(1,)),
                  t=(L / 2 + 0.04, 0.0, 0.0)))
    return K.wear_all(out, wear)


def buckets(wear=None, n=3):
    out = []
    for k in range(n):
        b = LW.fire_bucket(wear=wear, mark="oke_hinoyojin" if k % 2 == 0 else "mark_marudai")
        K.face_text(b, mirror_u=False)        # L1-style text (u already mirrored): face it out
        out += xfs(b, t=(-0.32 + 0.32 * k, 0.0, 0.0))
    return out


def fire_watch(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("fire_watch", budget="box", res3=True, mass=60.0, bury=0.40, wear="_w2" if ab else "_w1")
    if kind in ("rack", "ab_fallen"):
        for x in (-0.65, 0.65):
            P.add(W(x - 0.05, x + 0.05, -0.40, 2.40, -0.05, 0.05, WOOD, vis=(1, 2)))
            P.add(col(x - 0.05, x + 0.05, -0.40, 2.40, -0.05, 0.05))
        roof = W(-0.85, 0.85, 2.40, 2.44, -0.30, 0.30, WOOD, vis=(1, 2))
        if ab:
            roof = xf(roof, rz=-14.0, pivot=(-0.7, 2.42, 0.0))
        P.add(roof)
        for y in (0.55, 1.95):
            P.add(W(-0.60, 0.60, y - 0.04, y, -0.05, 0.05, WOOD, vis=(1, 2)))
            P.add(col(-0.595, 0.595, y - 0.04, y, -0.05, 0.05))
        P.add(W(-0.60, 0.60, 0.55, 0.58, 0.05, 0.30, WOOD, vis=(1, 2)))          # bucket shelf
        P.add(col(-0.595, 0.595, 0.55, 0.58, 0.055, 0.30))
        for x in (-0.4, 0.4):                                                   # pegs for the hook
            P.add(beam((x, 1.95, 0.05), (x, 1.99, 0.16), 0.025, 0.025, WOOD, vis=(1,)))
        if kind == "rack":
            add_all(P, xfs(buckets(), t=(0.0, 0.58, 0.17)))
            add_all(P, xfs(fire_hook(), t=(0.0, 2.00, 0.13)))
            ls, lc, _ = ladder_parts_h(2.3)
            add_all(P, xfs(ls, t=(0.0, 0.0, -0.10)))
            P.add(xf(lc[0], t=(0.0, 0.0, -0.10)))
        else:
            add_all(P, xfs(buckets(wear="_w2", n=1), t=(0.32, 0.58, 0.17)))
            r = random.Random(681)
            for k in range(2):
                b = LW.fire_bucket(wear="_w2", mark="oke_hinoyojin")
                K.face_text(b, mirror_u=False)
                b = rest(xfs(b, rx=90.0, ry=r.uniform(0, 360)), 0.0)
                add_all(P, xfs(b, t=(-0.6 + 0.9 * k, 0.0, 0.8 + 0.3 * k)))
            add_all(P, xfs(fire_hook(wear="_w2"), ry=20.0, t=(0.1, 0.02, 1.3)))
            ls, lc, _ = ladder_parts_h(2.3, wear="_w2")
            vs, cs = K.lkit.place_group(ls, lc, [dict(rx=90.0), dict(ry=70.0, t=(1.6, 0.0, 0.4))])
            add_all(P, vs + cs)
            P.add(litter(682, 0.3, 0.8, 1.0, sx=1.5))
        P.add(W(-0.7, 0.7, -0.4, 2.44, -0.3, 0.3, WOOD, vis=(3,)))
        P.dim("rack_w", 1.40, 1.40, tol=0.01)
        P.dim("buckets", 3, 3, tol=0)
        P.notes.append("fire gear at a street corner: buckets marked 'fire, take care' (火之用心), a fire hook "
                       "(tobiguchi), a ladder, under a board roof (Kyoho town firemen; BUILDING_LIST 390, 5.9)")
    else:   # ladder_tower: the fire-watch ladder with its alarm bell (hinomi-hashigo, Kyoho), about 6 m
        # FP1 (2026-10-01, Stephen: 'I can't climb it'): CLIMBABLE the vanilla way (read from
        # P:\DZ\structures\industrial\farms\farm_watertower_small.p3d + scripts ActionEnterLadder): a View Geometry
        # component named 'ladder1'; Memory points ladder1 (the climb line: bottom 0.54 over the ground, top 0.675 over
        # the exit floor), ladder1_con / _bottom_front / _top_front (enter points), ladder1_con_dir / ladder1_dir (the
        # side to stand on: in front at the foot, on the platform at the top); Geometry named properties class=house
        # (so the .wrp object binds to its Land_ class as a Building) and laddertype=wood (the wooden climbing sound);
        # the config class is Land_JP_S_Fire_Watch_Ladder_Tower (Land_ + the p3d name, B3b build.py 'land').
        # The climb face is +z; at the top the player steps off backwards onto a small lookout deck (railed, Roadway),
        # carried by the two raking braces and a third back leg; the bell hangs over the deck (moved out of the climb).
        P.budget = "medium"
        P.bury = 0.52
        P.keep_memory = True
        P.geo_props = {"class": "house", "laddertype": "wood"}
        PY = 4.90                                               # the lookout deck (top of the boards)
        ls, lc, _ = ladder_parts_h(6.3, y0=-0.5)
        # no rungs above the deck (the player steps off over the top: only the two rails rise on as handholds)
        add_all(P, [q for q in ls if not (q.bbox()[2] > PY + 0.01 and q.bbox()[1] - q.bbox()[0] > 0.3)])
        lcol = col(-0.25, 0.25, -0.5, PY - 0.03, -0.03, 0.03)   # the ladder's collision ends at the deck; its View
        lcol.view = False                                       # component is 'ladder1' alone (the camera must hit it)
        P.add(lcol)
        for sx in (-1, 1):
            c = col(sx * 0.21 - 0.03, sx * 0.21 + 0.03, PY - 0.03, 5.80, -0.02, 0.02)
            c.view = False
            P.add(c)
        vt = col(-0.25, 0.25, 0.04, PY + 0.60, -0.04, 0.05)     # View-only component 'ladder1' (the climb target)
        vt.geo, vt.fire, vt.sel = False, None, "ladder1"
        P.add(vt)
        for sx in (-1, 1):                    # two raking braces (now meeting the deck's front bearers)
            P.add(pole((sx * 1.4, -0.5, -1.2), (sx * 0.30, PY - 0.06, -0.06), 0.045, WOOD, n=6, vis=(1, 2)))
        P.add(col_solid(beam((-1.4, -0.5, -1.2), (-0.32, PY - 0.5, -0.10), 0.08, 0.08, WOOD)))
        P.add(col_solid(beam((1.4, -0.5, -1.2), (0.32, PY - 0.5, -0.10), 0.08, 0.08, WOOD)))
        P.add(pole((0.0, -0.5, -2.1), (0.0, PY - 0.06, -0.80), 0.05, WOOD, n=6, vis=(1, 2)))         # the back leg
        P.add(col_solid(beam((0.0, -0.5, -2.1), (0.0, PY - 0.5, -0.86), 0.09, 0.09, WOOD)))
        # the deck: two bearers from the ladder rails back to a cross beam on the back leg, boards on top
        for sx in (-1, 1):
            P.add(W(sx * 0.40 - 0.04, sx * 0.40 + 0.04, PY - 0.12, PY - 0.03, -0.84, 0.0, WOOD, vis=(1, 2)))
        P.add(W(-0.46, 0.46, PY - 0.12, PY - 0.03, -0.86, -0.76, WOOD, vis=(1, 2)))
        for k in range(5):
            z0 = -0.84 + 0.168 * k
            P.add(W(-0.46, 0.46, PY - 0.03, PY, z0 + 0.004, z0 + 0.164, WOOD, vis=(1, 2)))
        P.add(col(-0.46, 0.46, PY - 0.12, PY, -0.86, -0.03))
        P.road([(-0.46, PY, -0.86), (0.46, PY, -0.86), (0.46, PY, -0.03), (-0.46, PY, -0.03)], "boards_ext")
        # railing round the back and the sides (0.9 m), four corner posts carry the roof.
        # FX4 (2026-10-01, Stephen: 'too short at the top: you clip into its roof'): the roof was 1.10 m over the deck
        # and the bell hung over the deck at head height. Now the roof underside (and its tie beams) is RT = deck +
        # 2.20 m (a 1.8 m player + margin; PLAYBOOK D4 asks 2.05-2.10), carried by four corner posts, and the bell
        # hangs from the roof's back overhang OUTSIDE the back rail (struck over the rail), clear of the deck.
        RT = PY + 2.20                                          # roof underside / tie-beam underside
        for sx in (-1, 1):
            for (za, zb) in ((-0.86, -0.80), (-0.07, -0.01)):   # back and front corner posts
                P.add(W(sx * 0.44 - 0.03, sx * 0.44 + 0.03, PY, RT, za, zb, WOOD, vis=(1, 2)))
                P.add(col(sx * 0.44 - 0.03, sx * 0.44 + 0.03, PY, RT, za, zb))
            P.add(W(sx * 0.44 - 0.02, sx * 0.44 + 0.02, PY + 0.86, PY + 0.92, -0.80, -0.07, WOOD, vis=(1, 2)))
            P.add(col(sx * 0.44 - 0.02, sx * 0.44 + 0.02, PY + 0.10, PY + 0.92, -0.80, -0.07))
            P.add(W(sx * 0.44 - 0.025, sx * 0.44 + 0.025, RT - 0.08, RT, -0.80, -0.07, WOOD, vis=(1, 2)))   # side tie
        P.add(W(-0.41, 0.41, PY + 0.86, PY + 0.92, -0.86, -0.80, WOOD, vis=(1, 2)))
        P.add(col(-0.41, 0.41, PY + 0.10, PY + 0.92, -0.86, -0.80))
        for (za, zb) in ((-0.86, -0.80), (-0.07, -0.01)):                                   # back + front ties
            P.add(W(-0.41, 0.41, RT - 0.08, RT, za, zb, WOOD, vis=(1, 2)))
        P.add(W(-0.60, 0.60, RT, RT + 0.04, -1.25, 0.15, WOOD, vis=(1, 2)))                 # the little roof
        bz, by = -1.06, PY + 0.98                                                            # bell outside the back rail
        bell = lathe([(0.0, 0.0), (0.13, 0.0), (0.11, 0.08), (0.09, 0.26), (0.05, 0.30), (0.0, 0.31)], 10, IRON,
                     vis=(1, 2))
        P.add(xf(bell, t=(0.0, by, bz)))
        P.add(cord((0.0, by + 0.31, bz), (0.0, RT, bz), 0.008))
        P.add(pole((0.30, PY + 1.20, -0.88), (0.36, PY + 0.90, -0.88), 0.012, WOOD, n=4, vis=(1,)))   # the striker
        P.add(W(-0.25, 0.25, -0.5, 5.84, -0.05, 0.05, WOOD, vis=(3,)))
        P.add(W(-0.46, 0.46, PY - 0.12, RT, -0.86, -0.01, WOOD, vis=(3,)))
        P.add(W(-0.60, 0.60, RT, RT + 0.04, -1.25, 0.15, WOOD, vis=(3,)))
        P.dim("deck_head_room", 2.20, RT - PY, tol=0.001)          # FX4: >= 2.10 clear over the deck (Stephen)
        # memory points (vanilla names and roles, see above)
        P.memory = {
            "ladder1": [(0.0, PY + 0.675, 0.03), (0.0, 0.54, 0.03)],
            "ladder1_con": [(0.0, PY, 0.0), (0.0, 0.0, 0.10)],
            "ladder1_con_dir": [(0.0, PY, -0.45), (0.0, 0.0, 0.55)],
            "ladder1_dir": [(0.0, 0.0, 0.55)],
            "ladder1_bottom_front": [(0.0, 0.0, 0.10)],
            "ladder1_top_front": [(0.0, PY, 0.0)],
        }
        P.dim("height", 7.64, RT + 0.04 + 0.5, tol=0.1)            # FX4: roof raised (was 6.3)
        P.dim("deck_y", 4.90, PY, tol=0.001)
        P.notes.append("fire-watch ladder with an alarm bell (Kyoho fire rules, PLAYBOOK 1 / T12); CLIMBABLE (FP1): "
                       "climb the +z face, step off onto the railed lookout deck at 4.90 m; Land_ class (class=house); "
                       "FX4: roof 2.20 m over the deck on four posts, the bell outside the back rail")
    return P


def ladder_parts_h(L, wear=None, y0=0.0):
    """A wooden ladder standing on y0 (the B3b-style rails and rungs; one Geometry slab)."""
    out = []
    for sx in (-1, 1):
        out.append(W(sx * 0.21 - 0.03, sx * 0.21 + 0.03, y0, y0 + L, -0.02, 0.02, WOOD, vis=(1, 2)))
    n = int(L / 0.30)
    for k in range(1, n + 1):
        y = y0 + 0.30 * k - 0.05
        out.append(pole((-0.21, y, 0.0), (0.21, y, 0.0), 0.016, WOOD, n=5, vis=(1,)))
    cols = [col(-0.25, 0.25, y0, y0 + L, -0.03, 0.03)]
    return K.wear_all(out, wear), cols, n


PROPS.append({"id": "jp_s_fire_watch", "cat": CAT, "ll": "#68", "mount": "street", "tiers": [2, 3],
              "models": [
                  M("jp_s_fire_watch_rack", "rack", "intact", "Fire gear rack: buckets, fire hook, ladder",
                    lambda: fire_watch("rack")),
                  M("jp_s_fire_watch_ladder_tower", "tower", "intact", "Fire-watch ladder with an alarm bell",
                    lambda: fire_watch("ladder_tower"), land=True),
                  M("jp_s_fire_watch_ab_fallen", "rack", "abandoned", "Fire gear rack, ladder and buckets fallen",
                    lambda: fire_watch("ab_fallen")),
              ]})


# ================================================================================================ 69 sandals for sale
def sandals_sale(kind):
    ab = kind.startswith("ab")
    P = SPart("sandals_sale", budget="box", mass=6.0, wear="_w2" if ab else "_w1")
    if kind == "eave":
        P.anchor, P.wall_gap, P.flat, P.need = "wall", 0.0, True, ()
        P.hung = True
        Z, py = 0.34, EAVE_Y - 0.25
        add_all(P, [beam((x, EAVE_Y, 0.0), (x, EAVE_Y, Z + 0.04), 0.035, 0.035, DARK, vis=(1, 2)) for x in (-0.7, 0.7)])
        P.add(pole((-0.85, py, Z), (0.85, py, Z), 0.016, BAMBOO, n=5, vis=(1, 2)))
        for x in (-0.7, 0.7):
            P.add(cord((x, EAVE_Y, Z), (x, py + 0.016, Z), 0.005))
        for k in range(5):
            x = -0.56 + 0.28 * k
            add_all(P, LW.sandal_bunch(x, py - 0.016, Z, n=3, seed=690 + k))
        P.add(W(-0.7, 0.7, py - 0.55, py, Z - 0.03, Z + 0.03, MUSHIRO, vis=(2,)))
        P.extra["hang_y"] = EAVE_Y
        P.dim("bunches", 5, 5, tol=0)
    elif kind == "stand":
        for x in (-0.75, 0.75):
            P.add(W(x - 0.035, x + 0.035, 0.0, 1.75, -0.035, 0.035, WOOD, vis=(1, 2)))
            P.add(col(x - 0.035, x + 0.035, 0.0, 1.75, -0.035, 0.035))
            P.add(W(x - 0.035, x + 0.035, 0.0, 0.06, -0.25, 0.25, WOOD, vis=(1, 2)))
            P.add(col(x - 0.035, x + 0.035, 0.0, 0.06, -0.25, -0.04))
            P.add(col(x - 0.035, x + 0.035, 0.0, 0.06, 0.04, 0.25))
        P.add(pole((-0.85, 1.70, 0.0), (0.85, 1.70, 0.0), 0.02, BAMBOO, n=5, vis=(1, 2)))
        for k in range(4):
            add_all(P, LW.sandal_bunch(-0.45 + 0.3 * k, 1.68, 0.02, n=3, seed=695 + k))
        P.add(W(-0.6, 0.6, 1.1, 1.68, -0.03, 0.03, MUSHIRO, vis=(2,)))
        P.dim("bunches", 4, 4, tol=0)
    else:   # ab_fallen: the rack blown over, the sandals rotting in the leaves
        P.flat, P.need = True, ()
        P.add(pole((-0.85, 0.02, 0.1), (0.85, 0.02, 0.4), 0.02, BAMBOO, n=5, vis=(1, 2), wear="_w2"))
        r = random.Random(698)
        for k in range(6):
            s = LW.waraji(wear="_w2", loops=k % 2 == 0)
            add_all(P, xfs(s, ry=r.uniform(0, 360), t=(r.uniform(-0.8, 0.8), 0.0, r.uniform(0.3, 1.0))))
        bb = LW.sandal_bunch(0.0, 0.0, 0.0, n=3, seed=699, wear="_w2")
        add_all(P, rest(xfs(bb, rx=-90.0, t=(0.3, 0.0, 0.6)), 0.0))
        P.add(litter(699, 0.0, 0.6, 0.8, sx=1.5))
        P.add(W(-0.8, 0.8, 0.0, 0.03, 0.1, 1.0, MUSHIRO, vis=(2,)))
        P.dim("pieces", 7, 7, tol=0)
    P.notes.append("straw sandals (waraji) hung for sale outside a tea house (BUILDING_LIST 5: 24 entries)")
    return P


PROPS.append({"id": "jp_s_sandals_sale", "cat": CAT, "ll": "#69", "mount": "street", "tiers": [1, 2],
              "models": [
                  M("jp_s_sandals_sale_eave", "eave", "intact", "Straw sandals hung for sale under the eaves",
                    lambda: sandals_sale("eave"), mount="eaves"),
                  M("jp_s_sandals_sale_stand", "stand", "intact", "Straw sandals for sale on a rack",
                    lambda: sandals_sale("stand")),
                  M("jp_s_sandals_sale_ab_fallen", "stand", "abandoned", "Sandal rack blown over, sandals rotting",
                    lambda: sandals_sale("ab_fallen")),
              ]})


# ================================================================================================ 71 shop shutters (amado)
def amado_panel(wear=None, split=False):
    """One rain shutter 0.91 x 1.75 x 0.03: vertical boards in a frame with three cross battens (built standing on
    the origin, face +z)."""
    w, h, t = 0.90, 1.75, 0.03
    out = [W(-w / 2, w / 2, 0.0, h, -t / 2, t / 2, DARK, vis=(1, 2))]
    for y in (0.06, h / 2, h - 0.06):
        out.append(W(-w / 2 + 0.03, w / 2 - 0.03, y - 0.03, y + 0.03, t / 2, t / 2 + 0.012, DARK, vis=(1,)))
    for sx in (-1, 1):
        out.append(W(sx * w / 2 - 0.035 * (sx > 0), sx * w / 2 + 0.035 * (sx < 0), 0.0, h, t / 2, t / 2 + 0.012, DARK,
                     vis=(1,)))
    if split:
        out = [s for s in out]
    return K.wear_all(out, wear)


def amado(kind):
    ab = kind.startswith("ab")
    P = SPart("amado", budget="small", mass=15.0, anchor="wall", wall_gap=0.0, wear="_w2" if ab else "_w1")
    rails = [W(-0.95, 0.95, 0.0, 0.05, 0.0, 0.10, DARK, vis=(1, 2)),
             W(-0.95, 0.95, 1.80, 1.86, 0.0, 0.10, DARK, vis=(1, 2))]
    if kind == "half_open":
        add_all(P, rails)
        P.add(col(-0.95, 0.95, 0.0, 0.05, 0.0, 0.10, DARK))
        for x, z in ((-0.455, 0.03), (-0.30, 0.07)):
            add_all(P, xfs(amado_panel(), t=(x, 0.05, z)))
            P.add(col(x - 0.45, x + 0.45, 0.05, 1.80, z - 0.015, z + 0.015, DARK))
        P.dim("run", 1.82, 1.90, tol=0.1)
        P.notes.append("a 1-ken shutter run half open: two amado slid together to the left; the right half open")
    elif kind == "leaning":
        vs, cs = lean_to_wall_s(amado_panel(), 1.75, 12.0, cols=[col(-0.45, 0.45, 0.0, 1.75, -0.015, 0.027, DARK)])
        add_all(P, vs + cs)
        P.dim("panel_h", 1.75, 1.75, tol=0.01)
    else:
        P.anchor = "floor"
        if kind == "fallen":
            pn = xfs(amado_panel(wear="_w2"), rx=-90.0, t=(0.0, 0.015, 1.9))
            add_all(P, pn)
            P.add(col(-0.45, 0.45, 0.0, 0.042, 0.15, 1.9, DARK))
            P.add(litter(711, 0.0, 1.0, 0.9, sx=1.2, sz=1.4))
        else:   # ab_broken: the fallen shutter snapped across, the two halves askew
            pn = amado_panel(wear="_w2")
            lo = [s for s in pn if s.bbox()[3] <= 0.9]
            hi = [s for s in pn if s.bbox()[2] >= 0.85]
            mid = [s for s in pn if s not in lo and s not in hi]
            lo = xfs([xf(s) for s in lo] + [W(-0.45, 0.45, 0.0, 0.87, -0.015, 0.015, DARK, vis=(1, 2))], rx=-90.0,
                     t=(0.0, 0.015, 0.0))
            hi = xfs([W(-0.45, 0.45, 0.88, 1.75, -0.015, 0.015, DARK, vis=(1, 2))] +
                     [s for s in pn if s.bbox()[2] >= 0.85], rx=-90.0, ry=18.0, t=(0.15, 0.03, 0.1))
            add_all(P, K.wear_all(lo + hi, "_w2"))
            P.add(col(-0.45, 0.45, 0.0, 0.03, 0.0, 0.87, DARK))
            P.add(litter(712, 0.0, 0.9, 0.9, sx=1.2, sz=1.4))
        ground(P)
        P.dim("panel_w", 0.90, 0.90, tol=0.01)
    return P


def lean_to_wall_s(ss, L, theta, top_z=0.028, cols=()):
    a = math.radians(theta)
    d = top_z + L * math.sin(a)
    vs = xfs(ss, rx=-theta, t=(0.0, 0.0, d))
    cs = xfs(list(cols), rx=-theta, t=(0.0, 0.0, d))
    lo = min(v[1] for s in vs for v in s.verts)
    return xfs(vs, t=(0.0, -lo, 0.0)), xfs(cs, t=(0.0, -lo, 0.0))


PROPS.append({"id": "jp_s_amado", "cat": CAT, "ll": "#71", "mount": "street", "tiers": [2, 3],
              "refs": ["x25_morse_amado_box"],
              "notes": ["shop rain shutters (amado, BUILDING_LIST 776); wall pieces: the facade is z = 0"],
              "models": [
                  M("jp_s_amado_half_open", "run", "intact", "Shop shutters half open (two slid together)",
                    lambda: amado("half_open")),
                  M("jp_s_amado_leaning", "panel", "abandoned", "A shop shutter leaned against the front",
                    lambda: amado("leaning")),
                  M("jp_s_amado_fallen", "panel", "abandoned", "A shop shutter fallen flat in the street",
                    lambda: amado("fallen")),
                  M("jp_s_amado_ab_broken", "panel", "abandoned", "A fallen shop shutter snapped in two",
                    lambda: amado("ab_broken")),
              ]})


# ================================================================================================ 72 fallen lantern
def lantern_fallen(kind):
    P = SPart("lantern_fallen", budget="small", mass=1.0, flat=True, wear="_w2")
    if kind == "chochin":
        ch = PS.chochin(0.17, 0.55, "chochin_honcho", wear="_w2", text_wear="_w1")
        K.face_text(ch, mirror_u=True)        # B3b-style text: face it out and read it right
        ch = rest(xfs(ch, rz=88.0, ry=-25.0), 0.0)
        add_all(P, K.lkit.inner_side(ch, (CHOCHIN, DARK)))   # FP1: the open top showed no inside (see-through)
        P.dim("lantern_h", 0.55, 0.55, tol=0.01)
    elif kind == "andon":
        lamp = PS.box_lamp(0.30, 0.15, 0.45, "kanban_oyasumidokoro", wear="_w2", text_wear="_w1")
        K.face_text(lamp, mirror_u=True)
        lamp = rest(xfs(lamp, rx=-88.0), 0.0)            # fallen on its back, the text up
        add_all(P, lamp)
        P.dim("lamp_h", 0.45, 0.45, tol=0.01)
    else:   # crushed: a crest lantern trodden flat against the gutter edge (L1's crest lantern)
        ch = LW.chochin(0.15, 0.48, "crest_igeta", wear="_w2", text_wear="_w2", both=False)
        K.face_text(ch, mirror_u=False)
        ch = rest(xfs(ch, rz=90.0, ry=40.0), 0.0)
        add_all(P, K.lkit.inner_side(ch, (CHOCHIN, DARK)))   # FP1: inside of the paper drawn too
        P.dim("lantern_h", 0.48, 0.48, tol=0.01)
    P.add(litter(720 + len(kind), 0.0, 0.0, 0.5))
    P.notes.append("a paper lantern fallen in the street (G1 A3 answer 1: kept, weathered); never emissive")
    return P


PROPS.append({"id": "jp_s_lantern_fallen", "cat": CAT, "ll": "#72", "mount": "street", "tiers": [2, 3],
              "models": [
                  M("jp_s_lantern_fallen_chochin", "chochin", "abandoned", "A torn paper lantern fallen in the street",
                    lambda: lantern_fallen("chochin")),
                  M("jp_s_lantern_fallen_andon", "andon", "abandoned", "A box lamp fallen on its back",
                    lambda: lantern_fallen("andon")),
                  M("jp_s_lantern_fallen_crushed", "crest", "abandoned", "A crest lantern trodden flat",
                    lambda: lantern_fallen("crushed")),
              ]})
