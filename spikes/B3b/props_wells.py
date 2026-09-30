"""Wells (BUILD_LIST order of work, step 2): the pulley well (tsurube-ido, incl. `_roofed` = dwelling shell 28) and the
lever well (hanetsurube). Built once here and reused by KEEP_CIVIC (G1 A3 answer 2).

Drink + wash: every well model (except the lever sweep over a field ditch) gets a Land_JP_S_Well_* config class and a
one-line script class 'extends Well' (build.py), exactly as vanilla Land_Misc_Well_Pump_Yellow; the actions target the
object the camera ray hits in View Geometry, so the curb is one closed View / Fire / Geometry cylinder (nobody falls in,
and looking at the curb top from a crouch is the drink target).

The shaft: DayZ terrain has no holes, so the water sits just above grade inside the curb: a glossy black disc
(jp_m_lacquer_black, the library's only env-reflective black) 8 cm up reads as dark water deep in the shaft.
"""
import math
import random

from skit import (core, box, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, lcyl, SPart, pole, beam,
                  rope_path, sag, leaves, litter, add_all, ground, disc, moss_top, WOOD, DARK, BAMBOO, IRON, CUT, FIELD,
                  RIVER, ROPE, ROOFB, LEAF)
from props_wood import hoop, vessel, M

WATER = "lacquer_black"
WATER_Y = 0.08
CURB_H = 0.70
R_OUT, R_IN = 0.575, 0.48          # tub curb: outside d 1.15, inside d 0.96 (shaft 0.9-1.0)


# ------------------------------------------------------------------------------------------------ curbs
def water(r, n=12, wear="_w1", leafy=False, seed=1):
    out = [flat_poly([(r * math.cos(2 * math.pi * k / n), -r * math.sin(2 * math.pi * k / n)) for k in range(n)],
                     WATER_Y, WATER, vis=(1, 2), wear=wear)]
    if leafy:
        out.append(litter(seed, 0.05, -0.05, r * 0.7, wear="_w2"))
        out[-1] = xf(out[-1], t=(0.0, WATER_Y, 0.0))
    return out


def curb_tub(wear=None, leafy=False):
    """Round stave curb, bamboo hoops (list: tub curb d 1.05-1.20 x h 0.60-0.75)."""
    out = [lathe([(R_OUT, 0.0), (R_OUT, CURB_H), (R_IN, CURB_H), (R_IN, WATER_Y)], 16, WOOD, vis=(1,), wear=wear)]
    out.append(lathe([(R_OUT, 0.0), (R_OUT, CURB_H), (R_IN, CURB_H), (R_IN, WATER_Y)], 8, WOOD, vis=(2,), wear=wear,
                     smooth=False))
    out.append(lathe([(R_OUT, 0.0), (R_OUT, CURB_H), (0.0, CURB_H - 0.1)], 6, WOOD, vis=(3,), wear=wear, smooth=False))
    for y in (0.10, 0.36, 0.60):
        out.append(hoop(R_OUT, y, 0.035, 16, wear=wear))
    out += water(R_IN, leafy=leafy)
    return out, [cyl_col(R_OUT, 0.0, CURB_H, n=10)], R_OUT, "tub"


def curb_igeta(wear=None, leafy=False):
    """Square timber igeta curb 1.20 x 1.20 x 0.65: four courses of beams crossing at the corners (井), ends proud."""
    S, H, T = 1.20, 0.65, 0.15
    out, cols = [], []
    ny = 4
    th = H / ny
    for k in range(ny):
        y0, y1 = k * th, (k + 1) * th
        if k % 2 == 0:
            for sz in (-1, 1):
                out.append(W(-S / 2 - 0.10, S / 2 + 0.10, y0, y1, sz * S / 2 - T / 2, sz * S / 2 + T / 2, WOOD, vis=(1,)))
        else:
            for sx in (-1, 1):
                out.append(W(sx * S / 2 - T / 2, sx * S / 2 + T / 2, y0, y1, -S / 2 - 0.10, S / 2 + 0.10, WOOD, vis=(1,)))
    # inner lining boards down to the water, and the Res 2 / 3 block
    ri = S / 2 - T / 2
    for sx in (-1, 1):
        out.append(W(sx * ri - 0.01, sx * ri + 0.01, WATER_Y, H, -ri, ri, WOOD, vis=(1,)))
        out.append(W(-ri, ri, WATER_Y, H, sx * ri - 0.01, sx * ri + 0.01, WOOD, vis=(1,)))
    for sz in (-1, 1):
        out.append(W(-S / 2 - 0.1, S / 2 + 0.1, 0.0, H, sz * S / 2 - T / 2, sz * S / 2 + T / 2, WOOD, vis=(2, 3)))
        out.append(W(sz * S / 2 - T / 2, sz * S / 2 + T / 2, 0.0, H, -S / 2 + T / 2, S / 2 - T / 2, WOOD, vis=(2, 3)))
    out.append(flat_poly([(-ri, -ri), (ri, -ri), (ri, ri), (-ri, ri)][::-1], WATER_Y, WATER, vis=(1, 2)))
    if leafy:
        out.append(xf(litter(3, 0.0, 0.0, 0.3), t=(0.0, WATER_Y, 0.0)))
    if wear:
        for s in out:
            s.wear = wear
    cols.append(col(-S / 2 - 0.1, S / 2 + 0.1, 0.0, H, -S / 2 - 0.1, S / 2 + 0.1))
    return out, cols, S / 2 + 0.1, "igeta"


def curb_stone(wear=None, leafy=False):
    """Cut granite curb (T3, temples): an octagonal ring of dressed stone, d 1.20 x h 0.65, a coping course."""
    H = 0.65
    out = [lathe([(0.60, -0.03), (0.60, H - 0.10), (0.63, H - 0.10), (0.63, H), (0.47, H), (0.47, WATER_Y)], 8, CUT,
                 vis=(1,), wear=wear, smooth=False, phase=math.pi / 8)]
    out.append(lathe([(0.62, -0.03), (0.62, H), (0.47, H), (0.47, WATER_Y)], 8, CUT, vis=(2,), wear=wear, smooth=False,
                     phase=math.pi / 8))
    out.append(lathe([(0.62, 0.0), (0.62, H), (0.0, H - 0.1)], 6, CUT, vis=(3,), wear=wear, smooth=False))
    out += water(0.47, n=8, leafy=leafy)
    out.append(moss_top(7, 0.35, -0.35, 0.12, H, wear="_w1"))
    return out, [cyl_col(0.62, 0.0, H, n=8, mat=CUT)], 0.63, "stone"


# ------------------------------------------------------------------------------------------------ buckets, frame
def well_bucket(wear=None, vis=(1,), fill=None):
    """Tsurube-oke d 0.26 x h 0.28 with an iron band and an iron bail (O23: iron fittings on well buckets)."""
    rb, rt, h = 0.12, 0.13, 0.28
    out = vessel(rb, rt, h, n=10, fill=fill if fill is not None else 0.04, hoops=(0.14,), vis=vis, wear=wear,
                 lod2=False, fill_mat=WATER if fill is None else LEAF)
    band = lathe([(rt + 0.004, h - 0.035), (rt + 0.004, h - 0.005)], 10, IRON, vis=vis, smooth=True)
    out.append(band)
    out += rope_path([(-rt, h - 0.02, 0.0), (-0.06, h + 0.14, 0.0), (0.06, h + 0.14, 0.0), (rt, h - 0.02, 0.0)], 0.006,
                     IRON)
    if wear:
        for s in out:
            s.wear = wear
    return out


def frame(top=2.40, span=1.30, wear=None, roofed=False):
    """Two posts either side of the curb, a cap beam, the pulley block hanging at the middle (Morse fig 289)."""
    out, cols = [], []
    for sx in (-1, 1):
        x = sx * span / 2
        out.append(W(x - 0.06, x + 0.06, -0.10, top, -0.06, 0.06, WOOD, vis=(1, 2, 3)))
        out.append(core.stone(random.Random(3 + sx), x, 0.0, 0.26, 0.26, 0.12, 0.06, FIELD, bury=0.06, n=7, vis=(1,)))
        cols.append(col(x - 0.06, x + 0.06, 0.0, top, -0.06, 0.06))
    if not roofed:
        out.append(W(-span / 2 - 0.22, span / 2 + 0.22, top, top + 0.12, -0.07, 0.07, WOOD, vis=(1, 2, 3)))
        cols.append(col(-span / 2 - 0.22, span / 2 + 0.22, top, top + 0.12, -0.07, 0.07))
        out.append(W(-span / 2 + 0.06, span / 2 - 0.06, 1.62, 1.70, -0.045, 0.045, WOOD, vis=(1, 2)))
        hang = top                      # the sheave hangs from the cap beam
    else:
        hang = top + 0.42               # from the ridge beam (roof(): ridge beam underside at top + rise - 0.08)
    # pulley block (kassha): a wooden sheave (axle 2.30, list 2.2-2.4) in an iron strap
    py = 2.30
    tie = hang
    sh = lathe([(0.0, -0.025), (0.10, -0.025), (0.10, 0.025), (0.0, 0.025)], 10, WOOD, vis=(1,), smooth=False)
    out.append(xf(sh, rx=90.0, t=(0.0, py, 0.0)))
    for sz in (-1, 1):
        out.append(W(-0.02, 0.02, py - 0.02, hang, sz * 0.035 - 0.006, sz * 0.035 + 0.006, IRON, vis=(1,)))
    out.append(W(-0.1, 0.1, py - 0.1, hang, -0.03, 0.03, WOOD, vis=(2,)))
    if wear:
        for s in out:
            if s.mats != IRON:
                s.wear = wear
    return out, cols, py


def roof(span=1.30, top=2.10, plan=(1.80, 1.60), rise=0.50, wear=None):
    """Small board gable roof (dwelling 28, Morse fig 293): ridge along x, eaves at `top`, plan 1.8 (x) x 1.6 (z)."""
    L, D = plan
    out, cols = [], []
    ry = top + rise
    for sz in (-1, 1):
        # board plane from the ridge down to the eave, 3 cm thick, as a sloped slab
        c = [(-L / 2, ry, 0.0), (L / 2, ry, 0.0), (L / 2, top, sz * D / 2), (-L / 2, top, sz * D / 2)]
        c2 = [(p[0], p[1] + 0.035, p[2]) for p in c]
        s = core.hexa(c + c2, ROOFB, vis=(1, 2, 3))
        s.uv = "world"
        out.append(s)
        cols.append(col_solid(core.hexa(c + c2, ROOFB)))
        # battens (visual strips) every 0.3
        for k in range(1, 5):
            t = k / 5
            y = ry + (top - ry) * t + 0.035
            z = sz * D / 2 * t
            out.append(W(-L / 2, L / 2, y, y + 0.02, z - 0.012, z + 0.012, ROOFB, vis=(1,)))
    out.append(W(-L / 2 - 0.02, L / 2 + 0.02, ry + 0.02, ry + 0.09, -0.06, 0.06, ROOFB, vis=(1, 2, 3)))
    # gable: tie beam, king post, barge boards; eave purlins on the posts
    for sx in (-1, 1):
        x = sx * (span / 2)
        out.append(W(x - 0.05, x + 0.05, top - 0.12, top, -D / 2 + 0.05, D / 2 - 0.05, WOOD, vis=(1, 2)))
        out.append(W(x - 0.04, x + 0.04, top, ry, -0.04, 0.04, WOOD, vis=(1,)))
        for sz in (-1, 1):
            out.append(beam((sx * (L / 2 + 0.01), ry + 0.04, 0.0), (sx * (L / 2 + 0.01), top - 0.02, sz * (D / 2 + 0.03)),
                            0.025, 0.12, ROOFB, vis=(1,), up=(0.0, 1.0, 0.0)))
    out.append(W(-L / 2, L / 2, ry - 0.08, ry, -0.05, 0.05, WOOD, vis=(1, 2)))
    if wear:
        for s in out:
            s.wear = wear
    return out, cols


def slab(x, z, wear=None, silted=False):
    """The wash slab (nagashi) beside the curb, seated 5 cm."""
    out = [W(x - 0.5, x + 0.5, -0.05, 0.07, z - 0.3, z + 0.3, FIELD, vis=(1, 2))]
    out.append(W(x - 0.45, x + 0.45, 0.07, 0.075, z - 0.02, z + 0.02, "wood_sooted", vis=(1,)))
    if silted:
        out.append(leaves(9, x, z, 0.35, 0.076, wear="_w2", sx=1.3, sz=0.8))
    else:
        out.append(leaves(9, x + 0.25, z + 0.05, 0.14, 0.076, wear="_w1"))
    if wear:
        out[0].wear = wear
    return out, [col(x - 0.5, x + 0.5, 0.0, 0.07, z - 0.3, z + 0.3, FIELD)]


# ------------------------------------------------------------------------------------------------ jp_s_well_tsurube
def tsurube(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("well_tsurube", budget="medium", res3=True, mass=800.0, bury=0.13)
    curb_fn = {"curb_igeta": curb_igeta, "curb_stone": curb_stone}.get(kind, curb_tub)
    cs, ccols, rc, ctype = curb_fn(wear=wear, leafy=ab or kind == "lid")
    add_all(P, cs)
    add_all(P, ccols)
    ch = CURB_H if ctype == "tub" else 0.65
    if kind != "lid":
        top = 2.10 if kind == "roofed" else 2.50
        fs, fcols, py = frame(top=top, span=2 * rc + 0.18, wear=wear, roofed=kind == "roofed")
        add_all(P, fs)
        add_all(P, fcols)
        if kind == "roofed":
            rs, rcols = roof(span=2 * rc + 0.18, top=top, wear=wear)
            add_all(P, rs)
            add_all(P, rcols)
        if not ab:
            # the rope over the sheave: one bucket resting on the curb rim, the other hanging in the shaft
            b1 = xfs(well_bucket(), t=(-0.28, ch, 0.0))
            b2 = xfs(well_bucket(), t=(0.20, ch - 0.10, 0.0))
            add_all(P, b1 + b2)
            add_all(P, rope_path([(-0.10, py, 0.0), (-0.24, ch + 0.45, 0.0), (-0.28, ch + 0.42, 0.0)], 0.008, ROPE))
            add_all(P, rope_path([(0.10, py, 0.0), (0.20, ch + 0.32, 0.0)], 0.008, ROPE))
            P.add(W(-0.40, 0.33, ch - 0.1, ch + 0.28, -0.13, 0.13, WOOD, vis=(2,)))
        else:
            # rope rotted away: one bucket on the curb, one at the bottom (unseen), a frayed end on the sheave
            add_all(P, xfs(xfs(well_bucket(wear="_w2", fill=0.05), rz=100.0), t=(-0.95, 0.13, 0.35)))
            add_all(P, rope_path([(0.10, py, 0.0), (0.12, py - 0.35, 0.02)], 0.008, ROPE, wear="_w2"))
            add_all(P, rope_path([(-0.10, py, 0.0), (-0.11, py - 0.18, 0.0)], 0.008, ROPE, wear="_w2"))
            # the half lid askew across the curb
            lid = W(-0.62, 0.62, 0.0, 0.03, -0.30, 0.30, WOOD, vis=(1, 2))
            lid.wear = "_w2"
            P.add(xf(lid, rz=-9.0, ry=20.0, t=(0.15, ch + 0.06, 0.28)))
            P.add(litter(11, -0.5, 0.9, 0.9, sx=1.3))
        P.dim("frame_h", 2.50 if kind != "roofed" else 2.10, top, tol=0.01)
        P.dim("pulley_axle_h", 2.30, py, tol=0.10)
    else:
        # curb with a board lid only, no frame (old well in the woods): two half boards on battens
        for sz in (-1, 1):
            b = W(-0.64, 0.64, ch, ch + 0.035, sz * 0.31 - 0.30, sz * 0.31 + 0.30, WOOD, vis=(1, 2, 3))
            P.add(xf(b, ry=4.0 * sz))
        for sx in (-1, 1):
            P.add(W(sx * 0.35 - 0.03, sx * 0.35 + 0.03, ch + 0.035, ch + 0.07, -0.62, 0.62, WOOD, vis=(1,)))
        P.add(core.stone(random.Random(4), 0.1, 0.05, 0.22, 0.18, 0.13, ch + 0.035 + 0.13, RIVER, bury=0.0, n=7,
                         vis=(1, 2)))
        P.add(litter(12, 0.2, 0.2, 1.0, sx=1.3))
        P.add(moss_top(13, -0.2, -0.2, 0.2, ch + 0.035))
    ss, scols = slab(rc + 0.65, 0.35, wear=wear, silted=ab)
    add_all(P, ss)
    add_all(P, scols)
    if kind == "roofed":
        P.dim("roof_plan_x", 1.80, 1.80, tol=0.01)
        P.dim("eave_h", 2.10, 2.10, tol=0.05)
    P.dim("curb_d" if ctype != "igeta" else "curb_w", {"tub": 1.15, "igeta": 1.20, "stone": 1.20}[ctype],
          {"tub": 2 * R_OUT, "igeta": 1.20, "stone": 1.20}[ctype], tol=0.06)
    P.dim("curb_h", 0.70 if ctype == "tub" else 0.65, ch, tol=0.05)
    P.dim("shaft_d_inside", 0.95, 2 * R_IN if ctype == "tub" else 0.94 if ctype == "stone" else 1.05, tol=0.1)
    P.extra["drink_wash"] = "Land_ class extends Well (drink, wash hands, fill bottles); target = the curb (View Geometry)"
    return P


# ------------------------------------------------------------------------------------------------ jp_s_well_hanetsurube
def hanetsurube(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("well_hanetsurube", budget="medium", res3=True, mass=600.0, bury=0.30)
    PX, PH = -1.80, 2.70                    # the post at x = -1.8, pivot at 2.65
    piv = (PX, PH - 0.05, 0.0)
    # forked post, d 0.15, set 0.3 into the ground
    P.add(pole((PX, -0.30, 0.0), (PX, PH - 0.15, 0.0), 0.075, WOOD, n=7, vis=(1, 2, 3), r1=0.065, wear=wear))
    for sx in (-1, 1):
        P.add(pole((PX, PH - 0.17, 0.0), (PX + sx * 0.02, PH + 0.12, sx * 0.08), 0.04, WOOD, n=5, vis=(1,), wear=wear))
    P.add(pole((PX, PH - 0.05, -0.12), (PX, PH - 0.05, 0.12), 0.015, WOOD, n=4, vis=(1,)))     # through-pin
    P.add(col(PX - 0.07, PX + 0.07, 0.0, PH - 0.25, -0.07, 0.07))
    ang = {"well": 28.0, "field": 28.0, "ab_down": 42.0}[kind]
    a = math.radians(ang)
    d = (math.cos(a), math.sin(a), 0.0)
    wl, bl = 2.0, 4.0                       # pivot at 1/3 of a 6.0 m sweep, from the weight end
    wend = core.sub(piv, core.mul(d, wl))
    tip = core.add(piv, core.mul(d, bl))
    sw = pole(wend, tip, 0.06, WOOD, n=6, vis=(1, 2, 3), r1=0.04, wear=wear)
    P.add(sw)
    P.add(col_solid(beam(wend, tip, 0.09, 0.09, WOOD)))
    # counterweight: a river stone lashed under the weight end
    st = core.stone(random.Random(5), wend[0] + 0.25, 0.0, 0.42, 0.36, 0.34, wend[1] - 0.02, RIVER, bury=0.0, n=8,
                    vis=(1, 2, 3))
    P.add(st)
    P.add(col_solid(st, RIVER))
    add_all(P, rope_path([(wend[0] + 0.25, wend[1] + 0.04, -0.05), (wend[0] + 0.1, wend[1] - 0.25, -0.2),
                          (wend[0] + 0.4, wend[1] - 0.3, 0.2), (wend[0] + 0.25, wend[1] + 0.04, 0.05)], 0.012,
                         wear=wear or "_w1"))
    cx = tip[0]
    ctype = None
    if kind in ("well", "ab_down"):
        cs, ccols, rc, ctype = curb_tub(wear=wear, leafy=ab)
        add_all(P, xfs(cs, t=(cx, 0.0, 0.0)))
        add_all(P, xfs(ccols, t=(cx, 0.0, 0.0)))
        ss, scols = slab(cx + rc + 0.55, 0.4, wear=wear, silted=ab)
        add_all(P, ss)
        add_all(P, scols)
    else:
        # field sweep: over a ditch / pit, no curb: a dark pit ringed by field stones
        pit = [(cx + 0.45 * math.cos(2 * math.pi * k / 9), -0.45 * math.sin(2 * math.pi * k / 9)) for k in range(9)]
        P.add(flat_poly(pit, 0.012, WATER, vis=(1, 2)))
        rr = random.Random(9)
        for k in range(7):
            aa = 2 * math.pi * k / 7
            P.add(core.stone(rr, cx + 0.58 * math.cos(aa), 0.58 * math.sin(aa), 0.25, 0.2, 0.12, 0.10, FIELD, bury=0.05,
                             n=6, vis=(1,)))
        P.add(litter(14, cx, 0.3, 0.9, sx=1.4))
    if kind != "ab_down":
        # the bamboo bucket pole hangs from the tip into the shaft, the bucket just above the curb / pit
        bot_y = (CURB_H - 0.35) if kind == "well" else 0.30
        P.add(pole(tip, (cx, bot_y + 0.30, 0.0), 0.022, BAMBOO, n=5, vis=(1, 2, 3), wear=wear))
        add_all(P, xfs(well_bucket(wear=wear), t=(cx, bot_y, 0.0)))
        if kind != "well":
            P.add(W(cx - 0.13, cx + 0.13, bot_y, bot_y + 0.28, -0.13, 0.13, WOOD, vis=(2,)))
        P.dim("bucket_pole", 3.8, math.dist(tip, (cx, bot_y + 0.30, 0.0)), tol=0.7)
    else:
        # lashing rotted: the bamboo pole and bucket lie across the curb and on the ground
        bp0 = (cx - 1.9, 0.03, 0.9)
        bp1 = (cx + 0.35, CURB_H + 0.03, 0.05)
        P.add(pole(bp0, bp1, 0.022, BAMBOO, n=5, vis=(1, 2, 3), wear="_w2"))
        add_all(P, xfs(xfs(well_bucket(wear="_w2", fill=0.05), rz=95.0), t=(cx - 2.0, 0.13, 1.2)))
        add_all(P, rope_path([tip, core.add(tip, (0.02, -0.5, 0.0))], 0.01, wear="_w2"))
        P.add(litter(15, cx - 1.0, 0.8, 1.0, sx=1.6))
    P.dim("post_h", 2.70, PH, tol=0.3)
    P.dim("sweep_L", 6.0, wl + bl, tol=0.5)
    P.dim("pivot_frac", 1.0 / 3.0, wl / (wl + bl), tol=0.01)
    P.extra["drink_wash"] = ("Land_ class extends Well (drink, wash hands, fill bottles); target = the curb"
                             if kind != "field" else "field sweep over a ditch: not a well")
    return P


PROPS = [
    {"id": "jp_s_well_tsurube", "cat": "water",
     "notes": ["every model is a Land_JP_S_Well_* class extending the vanilla Well script class: drink, wash hands and "
               "fill bottles like the vanilla well pumps", "_roofed = dwelling shell 28 (KEEP_DWELLINGS)",
               "the curb is one closed collision cylinder: nobody falls in; the water is a black disc 8 cm up (the "
               "terrain has no holes)"],
     "models": [
         M("jp_s_well_tsurube_curb_tub", "curb_tub", "intact", "Pulley well, round tub curb", lambda: tsurube("curb_tub"),
           well=True),
         M("jp_s_well_tsurube_curb_igeta", "curb_igeta", "intact", "Pulley well, square igeta curb",
           lambda: tsurube("curb_igeta"), well=True),
         M("jp_s_well_tsurube_curb_stone", "curb_stone", "intact", "Pulley well, stone curb", lambda: tsurube("curb_stone"),
           well=True),
         M("jp_s_well_tsurube_roofed", "roofed", "intact", "Roofed pulley well (dwelling 28)", lambda: tsurube("roofed"),
           well=True),
         M("jp_s_well_tsurube_lid", "lid", "intact", "Well curb with a board lid", lambda: tsurube("lid"), well=True),
         M("jp_s_well_tsurube_ab_open", "curb_tub", "abandoned", "Pulley well, rope rotted, lid askew",
           lambda: tsurube("ab_open"), well=True),
     ]},
    {"id": "jp_s_well_hanetsurube", "cat": "water",
     "notes": ["the sweep and post keep their silhouette in Res 1-3", "_field is a field sweep over a ditch: no Well "
               "class (not a drinking well)"],
     "models": [
         M("jp_s_well_hanetsurube_well", "well", "intact", "Lever well (hanetsurube)", lambda: hanetsurube("well"),
           well=True),
         M("jp_s_well_hanetsurube_field", "field", "intact", "Field sweep over a ditch", lambda: hanetsurube("field")),
         M("jp_s_well_hanetsurube_ab_down", "well", "abandoned", "Lever well, lashing rotted, pole down",
           lambda: hanetsurube("ab_down"), well=True),
     ]},
]
