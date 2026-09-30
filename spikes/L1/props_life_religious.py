"""Life layer B (research/interior/LIFE_LAYER.md items 15-17): the religious corner.

G1 A2-12: shrines and the butsudan are left UNDISTURBED and carry no loot. Their 'as left' state is dust, dried
flowers and sakaki, a burnt-down candle: never knocked over. Nothing here has a loot surface.
"""
import math
import random

import lkit
from lkit import (core, box, prism, lathe, xf, xfs, flat_poly, W, board, pole, beam, rope_path, grid_sheet, col, disc,
                  stain, mound, LPart, M, rng, bipyramid, lod_box, wear_all, WOOD, IRON, PALE, DARK, LACQ, BAMBOO,
                  PAPER, INDIGO, ROPE, LEAF, LITTER, ASH, RICE)

CAT = "religious"


# ================================================================================================ 15 butsudan (★)
def butsudan(kind="lacquer", dusty=False):
    """Household Buddhist cabinet, 0.50 x 0.40 x 0.80 on its drawer base (BUILD_LIST jp_f_butsudan), doors shut."""
    mat = LACQ if kind == "lacquer" else WOOD
    P = LPart("butsudan", budget="furniture", res3=True, mass=18.0, anchor="floor")
    wr = "_w2" if dusty else None
    w, d, h = 0.50, 0.40, 0.80
    hb = 0.14                                            # drawer base
    x0, x1, z0, z1 = -w / 2, w / 2, -d / 2, d / 2
    out = [W(x0, x1, 0.0, hb, z0, z1, mat, vis=(1, 2)),                     # base with one drawer
           W(x0 + 0.02, x1 - 0.02, hb, h - 0.06, z0 + 0.01, z1 - 0.02, mat, vis=(1, 2)),   # carcass
           W(x0 - 0.015, x1 + 0.015, h - 0.06, h - 0.03, z0 - 0.005, z1 + 0.015, mat, vis=(1, 2)),  # cornice
           W(x0 + 0.01, x1 - 0.01, h - 0.03, h, z0 + 0.005, z1 + 0.005, mat, vis=(1, 2))]
    # two shut doors, a hair gap between them, a frame bead and iron hinges and a pull ring
    for sx in (-1, 1):
        xa, xb = (x0 + 0.03, -0.002) if sx < 0 else (0.002, x1 - 0.03)
        out.append(W(xa, xb, hb + 0.02, h - 0.08, z1 - 0.02, z1 - 0.005, mat, vis=(1,)))
        out.append(W(xa + 0.025, xb - 0.025, hb + 0.05, h - 0.11, z1 - 0.005, z1 - 0.001, mat, vis=(1,)))  # panel
        hx = xa + 0.004 if sx < 0 else xb - 0.004
        for hy in (hb + 0.08, h - 0.14):
            out.append(box(hx - 0.012, hx + 0.012, hy - 0.02, hy + 0.02, z1 - 0.005, z1, IRON, vis=(1,)))
    out.append(box(-0.012, 0.012, 0.40, 0.44, z1 - 0.001, z1 + 0.006, IRON, vis=(1,)))
    out.append(W(-0.08, 0.08, 0.04, 0.10, z1, z1 + 0.004, mat, vis=(1,)))                   # drawer front
    out.append(box(-0.01, 0.01, 0.065, 0.075, z1 + 0.004, z1 + 0.012, IRON, vis=(1,)))
    out.append(W(x0, x1, 0.0, h, z0, z1, mat, vis=(3,)))
    for s in out:
        if wr:
            s.wear = wr
    P.adds(out)
    if dusty:                                            # undisturbed: dust on the top and a web of dust at the foot
        P.add(stain(151, 0.0, 0.0, 0.18, y=h + 0.002, sx=1.2, mat=LITTER, wear="_w1"))
        P.add(stain(152, 0.05, z1 + 0.15, 0.22, sx=1.6, mat=LITTER, wear="_w2"))
    P.add(col(x0, x1, 0.0, h, z0, z1, mat))
    P.dim("w", 0.50, w, tol=0.005)
    P.dim("h", 0.80, h, tol=0.005)
    P.notes.append("left undisturbed, doors shut, no loot (G1 A2-12); dust only in the as-left state")
    return P


def zushi(cx, y, cz, wear=None, vis=(1,)):
    """A small open shrine box on the Buddhist shelf with one memorial tablet inside."""
    out = [W(cx - 0.13, cx + 0.13, y, y + 0.02, cz - 0.10, cz + 0.10, LACQ, vis=(1, 2)),
           W(cx - 0.13, cx - 0.11, y + 0.02, y + 0.32, cz - 0.10, cz + 0.08, LACQ, vis=vis),
           W(cx + 0.11, cx + 0.13, y + 0.02, y + 0.32, cz - 0.10, cz + 0.08, LACQ, vis=vis),
           W(cx - 0.13, cx + 0.13, y + 0.02, y + 0.32, cz - 0.10, cz - 0.08, LACQ, vis=vis),
           W(cx - 0.15, cx + 0.15, y + 0.32, y + 0.36, cz - 0.11, cz + 0.11, LACQ, vis=(1, 2))]
    out += ihai(cx, y + 0.02, cz - 0.02, 0.18)
    return wear_all(out, wear)


def ihai(cx, y, cz, h=0.20, vis=(1,)):
    """Memorial tablet: a lacquered board on a stepped plinth."""
    return [W(cx - 0.035, cx + 0.035, y, y + 0.03, cz - 0.025, cz + 0.025, LACQ, vis=vis),
            W(cx - 0.025, cx + 0.025, y + 0.03, y + h, cz - 0.006, cz + 0.006, LACQ, vis=vis),
            W(cx - 0.03, cx + 0.03, y + h, y + h + 0.015, cz - 0.01, cz + 0.01, LACQ, vis=vis)]


def butsudan_shelf(dusty=False):
    """The poorer house's Buddhist shelf (butsudana): a wall board at 1.50 on brackets with a small open zushi."""
    P = LPart("butsudan", budget="small", mass=4.0, anchor="wall", flat=True)
    y = 1.50
    wr = "_w2" if dusty else None
    out = [board(-0.32, 0.32, y - 0.025, y, 0.0, 0.30, k=6, vis=(1, 2))]
    for sx in (-1, 1):
        out.append(W(sx * 0.24 - 0.018, sx * 0.24 + 0.018, y - 0.20, y - 0.025, 0.0, 0.025, vis=(1,)))
        out.append(xf(W(-0.013, 0.013, -0.02, 0.02, -0.11, 0.11, vis=(1,)), rx=-45.0, t=(sx * 0.24, y - 0.10, 0.10)))
    out += zushi(-0.10, y, 0.13, vis=(1,))
    wear_all(out, wr)
    P.adds(out)
    if dusty:
        P.add(stain(153, 0.15, 0.15, 0.10, y=y + 0.002, sx=1.3, mat=LITTER, wear="_w1"))
    P.dim("shelf_y", 1.50, y, tol=0.005)
    P.notes.append("Buddhist shelf of a poorer house (mount wall); the butsu_set 'simple' fits beside the zushi")
    return P


# ================================================================================================ 16 butsudan set
def koro(cx, cz, r=0.05, wear=None, ash=True):
    """Incense burner: a squat bowl on three feet, ash inside, two incense stubs."""
    out = [lathe([(0.0, 0.015), (r * 0.8, 0.015), (r, 0.04), (r * 0.95, 0.07), (r * 0.85, 0.07), (r * 0.85, 0.06),
                  (0.0, 0.06)], 6, DARK, vis=(1,), wear=wear)]
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.3
        out.append(box(r * 0.6 * math.cos(a) - 0.006, r * 0.6 * math.cos(a) + 0.006, 0.0, 0.017,
                       r * 0.6 * math.sin(a) - 0.006, r * 0.6 * math.sin(a) + 0.006, DARK, vis=(1,)))
    if ash:
        out.append(flat_poly([(r * 0.84 * math.cos(-k * math.pi / 3), r * 0.84 * math.sin(-k * math.pi / 3))
                              for k in range(6)], 0.061, ASH, vis=(1,)))
        for dx in (-0.012, 0.015):
            out.append(box(dx - 0.0015, dx + 0.0015, 0.062, 0.095, -0.0015, 0.0015, BAMBOO, vis=(1,)))
    out.append(lathe([(0.0, 0.0), (r, 0.04), (0.0, 0.07)], 5, DARK, vis=(2,), smooth=False))
    return xfs(out, t=(cx, 0.0, cz))


def candle_stand(cx, cz, h=0.14, candle=0.06, wear=None):
    """Small iron candle stand with a pricket and a candle (stub when burnt down)."""
    out = [disc(0.035, 0.0, 0.008, IRON, n=6, vis=(1,)),
           box(-0.004, 0.004, 0.008, h, -0.004, 0.004, IRON, vis=(1,)),
           disc(0.028, h, h + 0.006, IRON, n=6, vis=(1,))]
    if candle > 0:
        out.append(lkit.lcyl("y", 0.0, 0.0, 0.009, h + 0.006, h + 0.006 + candle, PAPER, n=5, vis=(1,)))
    return wear_all(xfs(out, t=(cx, 0.0, cz)), wear)


def vase_flowers(cx, cz, dry=False, wear=None, flower_mat=LEAF):
    """A small vase with flowers or evergreen sprigs; dry: stems drooped, leaves browned and some fallen."""
    out = [lathe([(0.0, 0.0), (0.03, 0.0), (0.04, 0.05), (0.022, 0.11), (0.026, 0.13), (0.0, 0.125)], 6, PALE, vis=(1,),
                 wear=wear)]
    r = random.Random(int(cx * 1000) + 7)
    for k in range(3):
        a = k * 2.1 + r.uniform(-0.3, 0.3)
        lean = (0.35 if dry else 0.12) + r.uniform(0, 0.1)
        tip = (0.14 * math.sin(lean) * math.cos(a), 0.13 + 0.14 * math.cos(lean) - (0.04 if dry else 0.0),
               0.14 * math.sin(lean) * math.sin(a))
        out.append(pole((0.0, 0.12, 0.0), tip, 0.003, BAMBOO, n=3, vis=(1,)))
        leaf = prism([(-0.02, 0.0), (0.0, -0.012), (0.02, 0.0), (0.0, 0.012)], "y", tip[1] - 0.002, tip[1] + 0.002,
                     flower_mat, vis=(1,))
        leaf.wear = "_w2" if dry else "_w1"
        out.append(xf(leaf, ry=a * 57.3, t=(tip[0], 0.0, tip[2])))
    out.append(lathe([(0.0, 0.0), (0.04, 0.05), (0.0, 0.13)], 4, PALE, vis=(2,), smooth=False))
    out = xfs(out, t=(cx, 0.0, cz))
    if dry:                                              # fallen leaves round the vase
        for k in range(3):
            l2 = prism([(-0.015, 0.0), (0.0, -0.01), (0.015, 0.0), (0.0, 0.01)], "y", 0.001, 0.003, flower_mat,
                       vis=(1,))
            l2.wear = "_w2"
            out.append(xf(l2, ry=k * 70.0, t=(cx + 0.05 * math.cos(k * 2.1), 0.0, cz + 0.04 * math.sin(k * 2.1))))
    return out


def rin(cx, cz, wear=None):
    """Prayer bell bowl on its small cushion, the striker beside it."""
    out = [lkit.soft_slab(0.08, 0.08, 0.02, INDIGO, n=2, vis=(1,)),
           lathe([(0.0, 0.02), (0.03, 0.022), (0.04, 0.05), (0.036, 0.05), (0.0, 0.03)], 6, IRON, vis=(1,)),
           box(0.05, 0.13, 0.0, 0.01, -0.005, 0.005, WOOD, vis=(1,))]
    return wear_all(xfs(out, t=(cx, 0.0, cz)), wear)


def butsu_set(kind="full", dusty=False):
    P = LPart("butsu_set", budget="small", mass=1.5, anchor="floor", flat=True)
    wr = "_w2" if dusty else None
    if kind == "full":
        P.adds(wear_all(ihai(-0.05, 0.0, -0.06, 0.20) + ihai(0.05, 0.0, -0.06, 0.17), wr))
        P.adds(koro(0.0, 0.03, wear=wr))
        P.adds(candle_stand(-0.13, 0.03, candle=0.012 if dusty else 0.06, wear=wr))
        P.adds(vase_flowers(0.14, 0.02, dry=dusty, wear=wr))
        P.adds(rin(0.10, 0.09, wear=wr))
        w = 0.36
    else:
        P.adds(wear_all(ihai(0.0, 0.0, -0.04, 0.18), wr))
        P.adds(koro(-0.07, 0.04, r=0.04, wear=wr))
        P.adds(vase_flowers(0.08, 0.03, dry=dusty, wear=wr))
        w = 0.22
    if dusty:                                            # undisturbed: incense ash dust, a burnt candle drip
        P.add(stain(154, 0.0, 0.02, w / 2, y=0.002, sx=1.4, mat=LITTER, wear="_w1"))
    P.add(box(-w / 2, w / 2, 0.0, 0.18, -0.08, 0.06, LACQ, vis=(2,)))
    P.dim("w", w, w, tol=0.005)
    P.notes.append("set for the butsudan or the Buddhist shelf (mount surface): tablets, incense burner, candle, vase"
                   ", bell; undisturbed, no loot (G1 A2-12); the 'dusty' state: dried flowers, candle burnt down")
    return P


# ================================================================================================ 17 kamidana set
def heishi(cx, cz, wear=None):
    """A white sake flask for the god shelf (pale), with a paper cap."""
    out = [lathe([(0.0, 0.0), (0.022, 0.0), (0.03, 0.04), (0.02, 0.10), (0.012, 0.12), (0.0, 0.125)], 5,
                 PALE, vis=(1,), wear=wear),
           lathe([(0.0, 0.118), (0.016, 0.118), (0.0, 0.145)], 4, PAPER, vis=(1,))]
    return xfs(out, t=(cx, 0.0, cz))


def sanbo(cx, cz, wear=None, full=True):
    """Offering stand (sanbo): a tray on a pierced box stand, three unglazed dishes of rice, salt and water."""
    out = [W(-0.06, 0.06, 0.0, 0.07, -0.06, 0.06, WOOD, vis=(1, 2)),
           W(-0.085, 0.085, 0.07, 0.08, -0.085, 0.085, WOOD, vis=(1, 2))]
    for k, (dx, dz) in enumerate(((-0.04, 0.03), (0.04, 0.03), (0.0, -0.035))):
        out.append(lathe([(0.0, 0.08), (0.025, 0.08), (0.035, 0.095), (0.0, 0.086)], 6, PALE, vis=(1,), wear="_w1"))
        out[-1] = xf(out[-1], t=(dx, 0.0, dz))
        if full and k < 2:
            out.append(xf(mound(160 + k, 0.0, 0.0, 0.02, 0.012, RICE, wear="_w0" if k == 1 else "_w1", vis=(1,)),
                          t=(dx, 0.084, dz)))
    for s in out:
        if wear:
            s.wear = wear
    return xfs(out, t=(cx, 0.0, cz))


def kamidana_set(kind="offerings", dry=False):
    wr = "_w2" if dry else None
    if kind == "shimenawa":
        import props_straw as PS                         # B3b (read-only): the paper streamer
        P = LPart("kamidana_set", budget="small", mass=0.5, anchor="wall", flat=True)
        y, z = 2.05 - 0.01, 0.305                        # under the front edge of jp_f_kamidana_plain (shelf 2.05)
        pts = [(-0.45 + 0.9 * k / 6, y - 0.05 * math.sin(math.pi * k / 6), z) for k in range(7)]
        P.adds(rope_path(pts, 0.012, ROPE, n=5, vis=(1,), wear=wr or "_w1"))
        for x in (-0.45, 0.45):                          # tied back along the shelf underside to the brackets
            P.add(lkit.cord((x, y + 0.004, z), (x * 0.8, y + 0.004, 0.003), 0.004))
        for k, x in enumerate((-0.27, -0.09, 0.09, 0.27)):
            yy = y - 0.05 * math.sin(math.pi * (x + 0.45) / 0.9) - 0.01
            if dry and k == 2:
                continue                                 # one streamer gone
            P.add(PS.shide((x, yy, z), s=0.18 if not (dry and k == 0) else 0.10, wear=wr or "_w1"))
        P.add(box(-0.45, 0.45, y - 0.08, y, z - 0.01, z + 0.01, ROPE, vis=(2,)))
        P.dim("width", 0.90, 0.90, tol=0.005)
        P.notes.append("the sacred rope with paper streamers for the front edge of the god shelf: place it at the same "
                       "point and yaw as jp_f_kamidana_plain (mount wall; heights built in, shelf 2.05)")
        return P
    P = LPart("kamidana_set", budget="small", mass=0.8, anchor="floor", flat=True)
    P.adds(sanbo(0.0, 0.0, wear=wr, full=not dry))
    for sx in (-1, 1):
        P.adds(heishi(sx * 0.12, -0.02, wear=wr))
        P.adds(vase_flowers(sx * 0.21, 0.0, dry=dry, wear=wr))
    if dry:
        P.add(stain(161, 0.0, 0.02, 0.24, y=0.002, sx=1.3, mat=LITTER, wear="_w1"))
    P.add(box(-0.25, 0.25, 0.0, 0.16, -0.06, 0.06, WOOD, vis=(2,)))
    P.dim("w", 0.50, 0.50, tol=0.01)
    P.notes.append("offerings for a god shelf (mount surface; B4's jp_f_kamidana_plain already has its vases and cup: "
                   "use these on other kamidana, or the shimenawa alone there): sanbo with rice and salt, white flasks, "
                   "sakaki sprigs; undisturbed, no loot; 'dry' = the sakaki browned, the dishes empty, dust")
    return P


PROPS = [
    {"id": "jp_f_butsudan", "cat": CAT, "ll": 15, "mount": "floor", "tiers": [1, 2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_butsudan; undisturbed, no loot"], "models": [
        M("jp_f_butsudan_lacquer", "lacquer", "intact", "Buddhist cabinet (butsudan), lacquered, doors shut",
          lambda: butsudan("lacquer"), tiers=[3]),
        M("jp_f_butsudan_plain", "plain", "intact", "Buddhist cabinet, plain wood", lambda: butsudan("plain"),
          tiers=[2]),
        M("jp_f_butsudan_shelf", "shelf", "intact", "Buddhist shelf with a small shrine box", lambda: butsudan_shelf(),
          mount="wall", tiers=[1, 2]),
        M("jp_f_butsudan_lacquer_dusty", "lacquer", "dusty", "Buddhist cabinet, undisturbed, dusty",
          lambda: butsudan("lacquer", True), tiers=[3]),
        M("jp_f_butsudan_plain_dusty", "plain", "dusty", "Buddhist cabinet, plain, dusty",
          lambda: butsudan("plain", True), tiers=[2]),
        M("jp_f_butsudan_shelf_dusty", "shelf", "dusty", "Buddhist shelf, undisturbed, dusty",
          lambda: butsudan_shelf(True), mount="wall", tiers=[1, 2]),
    ]},
    {"id": "jp_f_butsu_set", "cat": CAT, "ll": 16, "mount": "surface", "tiers": [1, 2, 3], "refs": [], "models": [
        M("jp_f_butsu_set_full", "full", "intact", "Butsudan set: tablets, incense burner, candle, vase, bell",
          lambda: butsu_set("full")),
        M("jp_f_butsu_set_simple", "simple", "intact", "Butsudan set: a tablet, burner and vase",
          lambda: butsu_set("simple")),
        M("jp_f_butsu_set_full_dusty", "full", "dusty", "Butsudan set, flowers dried, candle burnt down",
          lambda: butsu_set("full", True)),
        M("jp_f_butsu_set_simple_dusty", "simple", "dusty", "Butsudan set, simple, dusty",
          lambda: butsu_set("simple", True)),
    ]},
    {"id": "jp_f_kamidana_set", "cat": CAT, "ll": 17, "mount": "surface", "tiers": [1, 2, 3], "refs": [],
     "models": [
        M("jp_f_kamidana_set_offerings", "offerings", "intact", "God-shelf offerings: sanbo, flasks, sakaki",
          lambda: kamidana_set("offerings")),
        M("jp_f_kamidana_set_shimenawa", "shimenawa", "intact", "Sacred rope with paper streamers for a god shelf",
          lambda: kamidana_set("shimenawa"), mount="wall"),
        M("jp_f_kamidana_set_offerings_dry", "offerings", "dry", "God-shelf offerings, sakaki dried, dishes empty",
          lambda: kamidana_set("offerings", True)),
        M("jp_f_kamidana_set_shimenawa_old", "shimenawa", "old", "Sacred rope, faded, a streamer gone",
          lambda: kamidana_set("shimenawa", True), mount="wall"),
    ]},
]
