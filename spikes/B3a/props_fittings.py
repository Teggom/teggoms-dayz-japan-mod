"""Built-in fittings as proxied props, added by B4 (the machiya pilot, 2026-09-30) through B3a's extension point
(MODULES in build.py): research/interior/BUILD_LIST.md fittings 6 (nagashi) and 7 (kamidana).

Why props and not merged kit parts: the build list calls them fittings "merged like any kit part", but the machiya
has 32 Resolution-1 faces of its 12,000 budget left (PLAYBOOK §15 T9); a proxy does not count against the house
budget (BUILD_LIST Q5 rule 4). Same frame and conventions as every B3a prop (fkit.py).

  jp_f_kamidana_plain   god shelf with a plain shrine box (miya), two small offering vases, a water cup and a paper
                        charm; wall-hung (anchor 'wall'); hanging prop = Resolution 1 only in the house, no Geometry
                        (Q5 rule 1). Shelf underside 2.05 above the floor (list: 1.95-2.05; head room >= 2.00). Left
                        undisturbed and carries no loot (G1 A2 decision 12).
  jp_f_nagashi_wood     standing wooden sink trough on four legs, top 0.75, 1.00 x 0.45, 0.08 deep, a bamboo spout
                        into the wall at the back, a slatted shelf between the legs; anchor 'wall'. Loot on the trough
                        bottom (0.69) and the under-shelf (0.16).
"""
import math

import fkit
import bits
from fkit import core, box, prism, lathe, xf, W, col, board, FPart, WOOD, PALE, PAPER, HOOP, LITTER
from bits import disc, stain

CAT = "fittings"


def add_all(P, ss):
    for s in ss:
        P.add(s)


# ================================================================================================ kamidana
KAMI_Y = 2.05          # shelf underside above the floor
KAMI_W, KAMI_D, KAMI_T = 0.90, 0.30, 0.03


def kamidana():
    P = FPart("kamidana", budget="small", res3=False, mass=4.0, anchor="wall", flat=True)
    y0, y1 = KAMI_Y, KAMI_Y + KAMI_T
    x0, x1 = -KAMI_W / 2, KAMI_W / 2
    P.add(board(x0, x1, y0, y1, 0.0, KAMI_D, k=2, vis=(1, 2)))
    for bx in (x0 + 0.08, x1 - 0.08):
        P.add(W(bx - 0.02, bx + 0.02, y0 - 0.22, y0, 0.0, 0.03, vis=(1,)))            # wall cleat
        P.add(W(bx - 0.018, bx + 0.018, y0 - 0.05, y0, 0.03, KAMI_D - 0.04, vis=(1,)))   # arm
        br = W(-0.015, 0.015, -0.02, 0.02, -0.11, 0.11, vis=(1,))
        P.add(xf(br, rx=-45.0, t=(bx, y0 - 0.12, 0.10)))                               # brace (<= 0.2 off the wall)
    # the miya: base, body with a door face, gabled roof (plain wood), ridge billet
    by = y1
    P.add(W(-0.22, 0.22, by, by + 0.03, 0.03, 0.27, vis=(1, 2)))
    P.add(W(-0.15, 0.15, by + 0.03, by + 0.27, 0.06, 0.22, vis=(1, 2)))
    P.add(W(-0.07, 0.07, by + 0.05, by + 0.24, 0.219, 0.225, vis=(1,)))                 # closed door leaf
    ry = by + 0.27
    roof = prism([(-0.20, 0.0), (0.20, 0.0), (0.0, 0.13)], "z", 0.02, 0.28, WOOD, vis=(1, 2))
    P.add(xf(roof, t=(0.0, ry, 0.0)))
    P.add(W(-0.21, 0.21, ry + 0.12, ry + 0.15, 0.02, 0.28, vis=(1,)))
    # offering vases (heishi) and a water cup, pale stoneware; a paper charm (ofuda) leaning on the box
    for vx in (-0.34, 0.34):
        js, _ = bits.jar(0.07, 0.13, PALE, n=8, lid=False, vis=(1,))
        add_all(P, fkit.xfs(js[:2], t=(vx, y1, 0.15)))
    P.add(disc(0.035, y1, y1 + 0.04, PALE, n=8, vis=(1,), cx=0.25, cz=0.08))
    charm = box(-0.04, 0.04, 0.0, 0.20, -0.004, 0.004, PAPER, vis=(1,))
    P.add(xf(charm, rx=-12.0, t=(-0.24, y1 + 0.005, 0.12)))
    P.dim("shelf_width", KAMI_W, KAMI_W, tol=0.005)
    P.dim("shelf_underside", KAMI_Y, y0, tol=0.005)
    P.notes.append("hanging prop: Resolution 1 only in the house, no Geometry (BUILD_LIST Q5 rule 1); undisturbed, no "
                   "loot (G1 A2-12); shelf underside 2.05 so head room under it stays >= 2.00")
    return P


# ================================================================================================ nagashi
NAG_W, NAG_D, NAG_TOP = 1.00, 0.45, 0.75


def nagashi():
    P = FPart("nagashi", budget="furniture", res3=True, mass=25.0, anchor="wall")
    x0, x1, z0, z1 = -NAG_W / 2, NAG_W / 2, 0.0, NAG_D
    t = 0.03
    top, bot = NAG_TOP, NAG_TOP - 0.08
    # trough: bottom board, four sides (the front one a little lower, where it drains towards the wall)
    P.add(board(x0 + t, x1 - t, bot - 0.03, bot, z0 + t, z1 - t, k=4, vis=(1, 2)))
    P.add(board(x0, x1, bot - 0.03, top, z1 - t, z1, k=5, vis=(1, 2)))
    P.add(board(x0, x1, bot - 0.03, top + 0.04, z0, z0 + t, k=6, vis=(1, 2)))           # back splash, a bit taller
    for xa, xb in ((x0, x0 + t), (x1 - t, x1)):
        P.add(W(xa, xb, bot - 0.03, top, z0 + t, z1 - t, vis=(1, 2)))
    P.add(W(x0, x1, bot - 0.03, top, z0, z1, vis=(3,)))
    # legs and the slatted under-shelf
    for lx in (x0 + 0.04, x1 - 0.04):
        for lz in (z0 + 0.04, z1 - 0.04):
            P.add(W(lx - 0.03, lx + 0.03, 0.0, bot - 0.03, lz - 0.03, lz + 0.03, vis=(1, 2)))
    for k in range(5):
        zz = z0 + 0.06 + k * (NAG_D - 0.12) / 4.0
        P.add(W(x0 + 0.07, x1 - 0.07, 0.14, 0.16, zz - 0.035, zz + 0.035, vis=(1,)))
    P.add(W(x0 + 0.07, x1 - 0.07, 0.14, 0.16, z0 + 0.03, z1 - 0.03, vis=(2,)))
    # bamboo spout from the trough's back corner into the wall (visual)
    sp = core.cyl("z", x1 - 0.12, bot + 0.02, 0.025, 0.0, z0 + t + 0.01, HOOP, n=6, vis=(1,))   # ends at the wall
    P.add(sp)
    # leaf litter blown into the dry trough, a stain under it
    P.add(stain(41, 0.05, 0.23, 0.15, y=bot + 0.002, sx=1.8))
    # collision: the trough block and the under-shelf (players can't walk through the legs)
    P.add(col(x0, x1, 0.0, top, z0, z1))
    P.loot_rect("trough", bot, x0 + 0.08, x1 - 0.08, z0 + 0.08, z1 - 0.08, rng=0.18)
    P.loot_rect("under_shelf", 0.16, x0 + 0.10, x1 - 0.10, z0 + 0.08, z1 - 0.08, rng=0.15)
    P.dim("width", NAG_W, NAG_W, tol=0.005)
    P.dim("top", NAG_TOP, top, tol=0.005)
    P.notes.append("wall-backed standing sink (hashiri) of town kitchens [N10, i08, i32]; dry, leaves in the trough")
    return P


def M(p3d, variant, state, display, fn):
    return {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}


PROPS = [
    {"id": "jp_f_kamidana", "cat": CAT, "wall": True, "notes": ["fitting 7 as a proxied prop (B4): hanging, Resolution 1 "
                                                               "only in the house; undisturbed, no loot"], "models": [
        M("jp_f_kamidana_plain", "plain", "intact", "God shelf (kamidana) with shrine box", kamidana),
    ]},
    {"id": "jp_f_nagashi", "cat": CAT, "wall": True, "notes": ["fitting 6 as a proxied prop (B4): standing wooden "
                                                              "sink, wall-backed"], "models": [
        M("jp_f_nagashi_wood", "wood", "intact", "Kitchen sink (nagashi), wooden trough on legs", nagashi),
    ]},
]
