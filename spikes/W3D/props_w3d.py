"""W3D specialty props for the wave-3d government sites (spikes/W3D/W3D_NOTES.md): the free-standing rack of the three
capture tools at the checkpoint (sodegarami, sasumata, tsukubo + two six-shaku staffs), the big beam scale of the
post-station yard (the cargo weight check), the 1720s fire-brigade standard (matoi-nobori). Built into
jp_furniture.pbo by spikes/W3D/build_w3d.py (after W3C2). Frames as fkit / lkit: 'floor' base centre on the floor,
+z = front. Dead world, autumn: the posts abandoned, a tool fallen, the standard knocked down.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "W2F"))
from props_w2f_sacred import (core, box, prism, lathe, xf, xfs, W, col, cyl_col, LPart, pole, cord,  # noqa: E402
                              wear_all, rng, M, WOOD, WEATH, IRON, KINARI, INDIGO, KURO, CUTSTONE, ROPE)

CAT = "govfit"
TAWARA = "straw_tawara"


def _tool(kind, x, L, z, y0=0.0):
    """One capture tool standing upright, butt at y0, head at y0 + L (the W2F rack's forms)."""
    out = []
    top = y0 + L
    out.append(pole((x, y0, z), (x, top - 0.18, z), 0.016, WEATH, n=5, vis=(1,)))
    if kind == "sasumata":                                               # the U fork
        out.append(W(x - 0.13, x + 0.13, top - 0.20, top - 0.17, z - 0.015, z + 0.015, IRON, vis=(1,)))
        for s in (-1, 1):
            out.append(W(x + s * 0.13 - 0.012, x + s * 0.13 + 0.012, top - 0.20, top, z - 0.015, z + 0.015, IRON,
                         vis=(1,)))
        out.append(W(x - 0.02, x + 0.02, top - 0.24, top - 0.17, z - 0.02, z + 0.02, IRON, vis=(1,)))
    elif kind == "tsukubo":                                              # the T rake with its teeth
        out.append(W(x - 0.17, x + 0.17, top - 0.20, top - 0.14, z - 0.02, z + 0.02, WEATH, vis=(1,)))
        for k in range(5):
            xx = x - 0.14 + 0.07 * k
            out.append(W(xx - 0.006, xx + 0.006, top - 0.145, top - 0.08, z - 0.006, z + 0.006, IRON, vis=(1,)))
        out.append(W(x - 0.02, x + 0.02, top - 0.21, top - 0.17, z - 0.022, z + 0.022, IRON, vis=(1,)))
    elif kind == "sodegarami":                                           # the barbed head
        out.append(W(x - 0.02, x + 0.02, top - 0.45, top - 0.15, z - 0.02, z + 0.02, IRON, vis=(1,)))
        for k in range(4):
            yy = top - 0.42 + 0.08 * k
            for s in (-1, 1):
                out.append(xf(W(0.0, 0.09, -0.005, 0.005, -0.004, 0.004, IRON, vis=(1,)),
                              rz=35.0 if s > 0 else 145.0, t=(x + s * 0.015, yy, z)))
    else:                                                                # the six-shaku staff (rokushaku-bo)
        out[0] = pole((x, y0, z), (x, top, z), 0.017, WEATH, n=6, vis=(1,))
    return out


# ================================================================================================ 1 the checkpoint rack
def mitsudogu_tate(ab=False):
    """The free-standing rack of the three capture tools before the checkpoint's inspection room [HAK-V]: a sill beam
    on two foot blocks, two posts (2.62), two rails, a small board roof on the post tops; the sasumata, tsukubo and
    sodegarami stand on the sill with two six-shaku staffs, leaning on the rails (front, +z). ab: the sodegarami
    fallen and lying before the rack."""
    P = LPart("mitsudogu_tate", budget="detail", mass=60.0, anchor="floor")
    out = []
    for x in (-0.62, 0.62):
        out.append(W(x - 0.10, x + 0.10, 0.0, 0.08, -0.22, 0.22, WEATH, vis=(1,)))          # foot blocks
        out.append(W(x - 0.05, x + 0.05, 0.08, 2.62, -0.05, 0.05, WEATH, vis=(1,)))         # posts
    out.append(W(-0.72, 0.72, 0.08, 0.18, -0.06, 0.15, WEATH, vis=(1,)))                     # sill (tools stand on it)
    for y in (1.15, 1.95):
        out.append(W(-0.67, 0.67, y, y + 0.06, 0.05, 0.10, WEATH, vis=(1,)))                 # rails (front face)
    out.append(W(-0.80, 0.80, 2.62, 2.66, -0.30, 0.30, KURO, vis=(1,)))                     # the board roof
    out.append(W(-0.80, 0.80, 2.66, 2.72, -0.04, 0.04, KURO, vis=(1,)))                     # its ridge batten
    tools = [("sasumata", -0.40, 2.15), ("tsukubo", -0.13, 2.25), ("sodegarami", 0.14, 2.30), ("bo", 0.36, 1.82),
             ("bo", 0.48, 1.82)]
    z = 0.10 + 0.017
    for kind, x, L in tools:
        if ab and kind == "sodegarami":
            continue
        out += _tool(kind, x, L, z, y0=0.18 if abs(x) < 0.55 else 0.18)
    if ab:                                                              # the sodegarami lying before the rack
        t = _tool("sodegarami", 0.0, 2.30, 0.0)
        out += [xf(s, rx=90.0, t=(-1.10, 0.022, 0.45)) for s in t]
    wear_all(out, "_w2" if ab else "_w1")
    P.adds(out)
    P.add(W(-0.72, 0.72, 0.0, 2.62, -0.06, 0.12, WEATH, vis=(2,)))
    P.add(W(-0.80, 0.80, 2.62, 2.72, -0.30, 0.30, KURO, vis=(2,)))
    for x in (-0.62, 0.62):
        P.add(col(x - 0.10, x + 0.10, 0.0, 2.62, -0.22, 0.22, WEATH))
    P.add(col(-0.52, 0.52, 0.0, 2.62, -0.06, 0.14, WEATH))
    P.dim("h", 2.72, max(v[1] for s in out for v in s.verts), tol=0.05)
    P.notes.append("the three capture tools (sasumata, tsukubo, sodegarami) + two six-shaku staffs on a free-standing "
                   "roofed rack (Hakone sekisho display)%s" % ("; the sodegarami fallen" if ab else ""))
    return P


# ================================================================================================ 2 the beam scale
def kanme_hakari(ab=False):
    """The big steelyard (chigi-bakari) of the post-station yard (C_CIVIC 4.3 18-19: large steelyard scales for cargo;
    the cargo weight check): a gallows frame (two posts on sills, a cross beam at 2.45); the steelyard beam (1.90 m)
    hangs from its fulcrum cord, a rice bale on the load hook resting on the ground (the ropes slack-tight), the iron
    counterweight on the long arm. ab: the steelyard down on the ground under the frame, the bale rolled off."""
    P = LPart("kanme_hakari", budget="detail", mass=80.0, anchor="floor")
    out = []
    for x in (-0.95, 0.95):
        out.append(W(x - 0.08, x + 0.08, 0.0, 0.10, -0.45, 0.45, WEATH, vis=(1,)))          # sills
        out.append(W(x - 0.06, x + 0.06, 0.10, 2.45, -0.06, 0.06, WEATH, vis=(1,)))         # posts
        for sz in (-1, 1):                                                                    # knee braces
            out.append(xf(W(-0.025, 0.025, 0.0, 0.62, -0.025, 0.025, WEATH, vis=(1,)), rx=sz * 38.0,
                          t=(x, 0.10, sz * 0.38)))
    out.append(W(-1.10, 1.10, 2.45, 2.60, -0.07, 0.07, WEATH, vis=(1,)))                     # cross beam
    bale = core.cyl("x", 0.27, 0.0, 0.27, -0.40, 0.40, TAWARA, n=10, vis=(1,))
    if not ab:
        yb = 1.55                                                         # the steelyard beam's height
        xf_ = -0.10                                                       # the fulcrum
        out.append(cord((xf_, 2.45, 0.0), (xf_, yb + 0.03, 0.0), 0.008))
        out.append(W(-0.55, 0.80, yb - 0.025, yb + 0.025, -0.025, 0.025, WEATH, vis=(1,)))   # the beam (clear of the post)
        for k in range(7):                                                                    # brass graduations
            xx = 0.05 + 0.11 * k
            out.append(W(xx - 0.004, xx + 0.004, yb + 0.025, yb + 0.029, -0.012, 0.012, IRON, vis=(1,)))
        xl = -0.48                                                        # the load hook + its ropes to the bale
        out.append(cord((xl, yb - 0.025, 0.0), (xl, 0.62, 0.0), 0.006))
        out.append(xf(bale, t=(xl, 0.0, 0.0)))
        for sz in (-1, 1):
            out.append(cord((xl, 0.62, 0.0), (xl, 0.40, sz * 0.24), 0.008))
        xw = 0.70                                                         # the counterweight
        out.append(cord((xw, yb - 0.025, 0.0), (xw, 1.12, 0.0), 0.004))
        out.append(lathe([(0.0, 0.0), (0.06, 0.02), (0.07, 0.10), (0.04, 0.16), (0.0, 0.17)], 8, IRON, vis=(1,)))
        out[-1] = xf(out[-1], t=(xw, 0.95, 0.0))
    else:
        out.append(xf(W(-0.95, 0.95, 0.0, 0.05, -0.025, 0.025, WEATH, vis=(1,)), ry=12.0, t=(0.0, 0.0, 0.25)))
        out.append(lathe([(0.0, 0.0), (0.06, 0.02), (0.07, 0.10), (0.04, 0.16), (0.0, 0.17)], 8, IRON, vis=(1,)))
        out[-1] = xf(out[-1], t=(0.55, 0.0, 0.45))
        out.append(xf(bale, ry=30.0, t=(-0.30, 0.0, 0.95)))
        out.append(cord((0.10, 2.45, 0.0), (0.10, 1.70, 0.0), 0.008))    # the fulcrum cord left hanging
    wear_all(out, "_w2" if ab else "_w1")
    P.adds(out)
    P.add(W(-1.10, 1.10, 0.0, 2.60, -0.10, 0.10, WEATH, vis=(2,)))
    P.add(xf(core.cyl("x", 0.27, 0.0, 0.27, -0.40, 0.40, TAWARA, n=6, vis=(2,)),
             t=((-0.48, 0.0, 0.0) if not ab else (-0.30, 0.0, 0.95))))
    for x in (-0.95, 0.95):
        P.add(col(x - 0.08, x + 0.08, 0.0, 2.45, -0.10, 0.10, WEATH))
    P.add(col(-1.10, 1.10, 2.45, 2.60, -0.07, 0.07, WEATH))
    P.add(xf(col(-0.40, 0.40, 0.0, 0.54, -0.27, 0.27, TAWARA), t=((-0.48, 0.0, 0.0) if not ab else (-0.30, 0.0, 0.95))))
    P.dim("beam_y", 2.60, 2.60, tol=0.01)
    P.notes.append("big steelyard on its gallows frame, a rice bale on the hook (cargo weight check)%s"
                   % ("; the steelyard down, the bale rolled off" if ab else ""))
    return P


# ================================================================================================ 3 the matoi-nobori
def matoi_nobori(fallen=False):
    """The fire-brigade standard as it was in the 1720s [WP-MATOI: the matoi given to the machi-bikeshi in 1720 was a
    banner type, matoi-nobori; the baren streamers came later]: a pole (2.80) with a carved wooden head (a block and a
    disc, the group's mark) and a long narrow banner hung from a cross bar under it; in a timber ground stand.
    fallen: the standard knocked down, lying, the stand on its side."""
    P = LPart("matoi_nobori", budget="detail", mass=18.0, anchor="floor")
    parts = []
    H = 2.80
    parts.append(pole((0.0, 0.0, 0.0), (0.0, H, 0.0), 0.022, WEATH, n=6, vis=(1,)))
    parts.append(W(-0.13, 0.13, H, H + 0.22, -0.13, 0.13, KURO, vis=(1,)))                   # the carved block
    parts.append(lathe([(0.0, H + 0.22), (0.20, H + 0.24), (0.20, H + 0.28), (0.0, H + 0.30)], 10, KINARI, vis=(1,)))
    parts.append(lathe([(0.0, H + 0.30), (0.05, H + 0.30), (0.0, H + 0.42)], 6, KURO, vis=(1,)))
    parts.append(W(-0.03, 0.32, H - 0.14, H - 0.10, -0.015, 0.015, WEATH, vis=(1,)))         # banner cross bar
    parts.append(W(0.02, 0.30, H - 1.55, H - 0.10, -0.004, 0.004, INDIGO, vis=(1,)))           # the banner
    parts.append(W(0.02, 0.30, H - 1.55, H - 1.50, -0.008, 0.008, KINARI, vis=(1,)))           # its hem
    stand = [W(-0.24, 0.24, 0.0, 0.08, -0.24, 0.24, WEATH, vis=(1,)), W(-0.07, 0.07, 0.08, 0.45, -0.07, 0.07, WEATH,
                                                                       vis=(1,))]
    if not fallen:
        out = stand + [xf(s, t=(0.0, 0.08, 0.0)) for s in parts]
    else:
        # the standard pulled out of its stand and lying beside it: the pole on the ground, the carved head at its end,
        # the disc knocked off flat, the banner and its cross bar flat on the ground
        z = 0.55
        out = list(stand)
        out.append(pole((-1.40, 0.022, z), (1.40, 0.022, z), 0.022, WEATH, n=6, vis=(1,)))
        out.append(W(1.38, 1.60, 0.0, 0.26, z - 0.13, z + 0.13, KURO, vis=(1,)))
        out.append(lathe([(0.0, 0.0), (0.20, 0.0), (0.20, 0.04), (0.0, 0.05)], 10, KINARI, vis=(1,)))
        out[-1] = xf(out[-1], t=(1.95, 0.0, z + 0.30))
        out.append(W(0.90, 1.25, 0.0, 0.03, z + 0.05, z + 0.08, WEATH, vis=(1,)))
        out.append(W(-0.55, 0.90, 0.0, 0.008, z + 0.08, z + 0.36, INDIGO, vis=(1,)))
    wear_all(out, "_w2")
    P.adds(out)
    if not fallen:
        P.add(W(-0.24, 0.32, 0.0, H + 0.50, -0.20, 0.20, KURO, vis=(2,)))
        P.add(col(-0.24, 0.24, 0.0, 0.45, -0.24, 0.24, WEATH))
        P.add(col(-0.03, 0.03, 0.45, H + 0.30, -0.03, 0.03, WEATH))
    else:
        P.add(W(-0.24, 0.24, 0.0, 0.45, -0.24, 0.24, WEATH, vis=(2,)))
        P.add(W(-1.40, 1.60, 0.0, 0.26, 0.42, 0.68, WEATH, vis=(2,)))
        P.add(col(-0.24, 0.24, 0.0, 0.45, -0.24, 0.24, WEATH))
        P.add(col(-1.40, 1.60, 0.0, 0.26, 0.42, 0.68, WEATH))
    P.notes.append("fire-brigade standard, 1720s banner form (matoi-nobori)%s" % (", knocked down" if fallen else ""))
    return P


PROPS = [
    {"id": "jp_f_mitsudogu_tate", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_mitsudogu_tate", "std", "intact", "The three capture tools on a free-standing roofed rack",
          lambda: mitsudogu_tate()),
        M("jp_f_mitsudogu_tate_ab", "std", "fallen", "Capture-tool rack, the sodegarami fallen",
          lambda: mitsudogu_tate(True))]},
    {"id": "jp_f_kanme_hakari", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kanme_hakari", "std", "intact", "Big steelyard on its frame, a bale on the hook", lambda: kanme_hakari()),
        M("jp_f_kanme_hakari_ab", "std", "broken", "Big steelyard down, the bale rolled off",
          lambda: kanme_hakari(True))]},
    {"id": "jp_f_matoi_nobori", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_matoi_nobori", "std", "intact", "Fire-brigade standard (matoi-nobori) in its stand",
          lambda: matoi_nobori()),
        M("jp_f_matoi_nobori_fallen", "std", "fallen", "Fire-brigade standard knocked down",
          lambda: matoi_nobori(True))]},
]
