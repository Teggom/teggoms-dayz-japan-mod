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
BRONZE = "metal_bronze"      # the steelyard's inlaid graduation pins (W2S material)
TRI_APEX = 3.00
TRI_R = 1.25
TRI_AZ = (270.0, 30.0, 150.0)     # the legs' feet (deg from +x towards +z): one behind, two at the front corners


def _tripod(out, P):
    """The timber tripod (sankyaku): three poles lashed at the apex (their tips crossing 0.18 past it), a rope lashing."""
    apex = (0.0, TRI_APEX, 0.0)
    for az in TRI_AZ:
        a = math.radians(az)
        foot = (TRI_R * math.cos(a), 0.025, TRI_R * math.sin(a))       # the slanted foot cap stays over the floor
        d = [apex[i] - foot[i] for i in range(3)]
        L = math.sqrt(sum(c * c for c in d))
        tip = tuple(apex[i] + d[i] / L * 0.18 for i in range(3))
        out.append(pole(foot, tip, 0.055, WEATH, n=7, vis=(1,), r1=0.045))
        P.add(pole(foot, apex, 0.06, WEATH, n=6, vis=(2,)))
        top = tuple(foot[i] + 0.85 * (apex[i] - foot[i]) for i in range(3))     # Geometry legs stop short of
        P.add(pole(foot, top, 0.06, WEATH, n=6, vis=(), geo=True, view=True, fire=True))   # the apex (C6b)
    out.append(core.cyl("y", 0.0, 0.0, 0.085, TRI_APEX - 0.10, TRI_APEX + 0.04, ROPE, n=8, vis=(1,)))   # lashing
    return apex


def kanme_hakari(ab=False):
    """The big steelyard (chigi-bakari, the cargo weight check of the post-station yard; C_CIVIC 4.3 18-19: large
    steelyard scales for cargo). FX7 (Stephen's 3d walk: the W3D gallows-like frame with the bale lying under it read
    as a gallows next to the jail): a heavy steelyard was hung from a timber TRIPOD or from a carrying pole on two men
    / trestles; chosen: the tripod (free-standing, reads at once as a hoist, never as a gallows). A long graduated
    beam (2.00 m) hangs by its iron strap and a cord from the lashing; the rice bale HANGS clear of the ground (0.43)
    in a four-rope sling on the load hook of the short arm; the iron counterweight hangs on its loop ON the long arm,
    which carries bronze graduation pins every 0.10 m (long marks every 0.50). ab: abandoned, still a scale, not a
    gallows: the tripod standing, the beam down on the ground, the weight beside it, the bale lying by a leg, the
    fulcrum cord hanging."""
    P = LPart("kanme_hakari", budget="detail", mass=80.0, anchor="floor")
    out = []
    _tripod(out, P)
    yb = 1.60                                                          # the steelyard beam's axis height
    XB0, XB1 = -0.55, 1.45
    w_prof = [(0.0, 0.0), (0.06, 0.015), (0.085, 0.09), (0.06, 0.17), (0.025, 0.20), (0.0, 0.21)]
    if not ab:
        out.append(cord((0.0, TRI_APEX - 0.06, 0.0), (0.0, yb, 0.0), 0.010))                 # the fulcrum cord
        out.append(W(-0.03, 0.03, yb - 0.045, yb + 0.045, -0.04, 0.04, IRON, vis=(1,)))       # its iron strap
        # the beam: a square timber tapering to the long end (two boxes), the load end shod with iron
        out.append(W(XB0, 0.10, yb - 0.035, yb + 0.035, -0.035, 0.035, WEATH, vis=(1,)))
        out.append(W(0.10, XB1, yb - 0.027, yb + 0.027, -0.027, 0.027, WEATH, vis=(1,)))
        out.append(W(XB0 - 0.01, XB0 + 0.08, yb - 0.04, yb + 0.04, -0.04, 0.04, IRON, vis=(1,)))
        for k in range(13):                                            # graduation pins on the top + the front face
            xx = 0.20 + 0.10 * k
            big = k % 5 == 0
            hw = 0.008 if big else 0.005
            dz = 0.024 if big else 0.012
            dy = 0.022 if big else 0.010
            out.append(W(xx - hw, xx + hw, yb + 0.026, yb + 0.031, -dz, dz, BRONZE, vis=(1,)))
            out.append(W(xx - hw, xx + hw, yb - dy, yb + dy, 0.026, 0.031, BRONZE, vis=(1,)))
        xl = -0.32                                                     # the load hook (strap, shank, J) + the sling
        out.append(W(xl - 0.025, xl + 0.025, yb - 0.045, yb + 0.045, -0.045, 0.045, IRON, vis=(1,)))
        out.append(W(xl - 0.010, xl + 0.010, 1.24, yb - 0.03, -0.010, 0.010, IRON, vis=(1,)))
        out.append(W(xl - 0.010, xl + 0.075, 1.22, 1.25, -0.010, 0.010, IRON, vis=(1,)))
        out.append(W(xl + 0.055, xl + 0.075, 1.22, 1.30, -0.010, 0.010, IRON, vis=(1,)))
        cy = 0.70                                                      # the bale's axis: its belly 0.43 off the ground
        out.append(core.cyl("x", cy, 0.0, 0.27, xl - 0.40, xl + 0.40, TAWARA, n=10, vis=(1,)))
        hk = (xl + 0.03, 1.235, 0.0)
        for dx in (-0.25, 0.25):
            for dz in (-0.10, 0.10):
                out.append(cord(hk, (xl + dx, cy + 0.235, dz), 0.008))
        xw = 1.15                                                      # the counterweight on its loop on the long arm
        out.append(W(xw - 0.012, xw + 0.012, yb - 0.035, yb + 0.035, -0.033, 0.033, ROPE, vis=(1,)))
        out.append(cord((xw, yb - 0.02, 0.0), (xw, 1.30, 0.0), 0.006))
        out.append(xf(lathe(w_prof, 8, IRON, vis=(1,)), t=(xw, 1.30 - 0.19, 0.0)))
        P.add(W(XB0, XB1, yb - 0.04, yb + 0.04, -0.04, 0.04, WEATH, vis=(2,)))
        P.add(core.cyl("x", cy, 0.0, 0.27, xl - 0.40, xl + 0.40, TAWARA, n=6, vis=(2,)))
        P.add(col(xl - 0.40, xl + 0.40, cy - 0.27, cy + 0.27, -0.27, 0.27, TAWARA))
        P.add(col(XB0, XB1, yb - 0.04, yb + 0.04, -0.04, 0.04, WEATH))
    else:
        out.append(cord((0.0, TRI_APEX - 0.06, 0.0), (0.0, 1.95, 0.0), 0.010))              # the fulcrum cord left
        beam = [W(XB0, 0.10, 0.0, 0.07, -0.035, 0.035, WEATH, vis=(1,)),
                W(0.10, XB1, 0.008, 0.062, -0.027, 0.027, WEATH, vis=(1,))]
        for k in range(13):
            xx = 0.20 + 0.10 * k
            beam.append(W(xx - 0.005, xx + 0.005, 0.061, 0.066, -0.012, 0.012, BRONZE, vis=(1,)))
        out += [xf(s_, ry=-18.0, t=(0.05, 0.0, 0.30)) for s_ in beam]
        out.append(xf(lathe(w_prof, 8, IRON, vis=(1,)), rz=80.0, t=(1.30, 0.085, 0.80)))   # the weight on its side
        out.append(xf(core.cyl("x", 0.27, 0.0, 0.27, -0.40, 0.40, TAWARA, n=10, vis=(1,)), ry=25.0,
                      t=(-0.85, 0.0, 0.15)))                                                 # the bale by the leg
        P.add(xf(W(XB0, XB1, 0.0, 0.07, -0.04, 0.04, WEATH, vis=(2,)), ry=-18.0, t=(0.05, 0.0, 0.30)))
        P.add(xf(core.cyl("x", 0.27, 0.0, 0.27, -0.40, 0.40, TAWARA, n=6, vis=(2,)), ry=25.0, t=(-0.85, 0.0, 0.15)))
        P.add(xf(col(-0.40, 0.40, 0.0, 0.54, -0.27, 0.27, TAWARA), ry=25.0, t=(-0.85, 0.0, 0.15)))
    wear_all(out, "_w2" if ab else "_w1")
    P.adds(out)
    P.dim("h", TRI_APEX + 0.10, max(v[1] for s_ in out for v in s_.verts), tol=0.10)
    P.notes.append("big steelyard hung from a timber tripod, a rice bale hanging in its sling on the hook, the "
                   "counterweight on the graduated long arm (cargo weight check)%s"
                   % ("; abandoned: the beam down, the weight and the bale on the ground, the tripod standing" if ab
                      else ""))
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
        M("jp_f_kanme_hakari", "std", "intact", "Big steelyard on its tripod, a bale hanging on the hook", lambda: kanme_hakari()),
        M("jp_f_kanme_hakari_ab", "std", "broken", "Big steelyard down by its tripod, the bale on the ground",
          lambda: kanme_hakari(True))]},
    {"id": "jp_f_matoi_nobori", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_matoi_nobori", "std", "intact", "Fire-brigade standard (matoi-nobori) in its stand",
          lambda: matoi_nobori()),
        M("jp_f_matoi_nobori_fallen", "std", "fallen", "Fire-brigade standard knocked down",
          lambda: matoi_nobori(True))]},
]
