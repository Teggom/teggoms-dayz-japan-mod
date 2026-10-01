"""W2 graveyard (BUILD_LIST items 26-27; agent W2, 2026-09-30): the 1730 gravestone mix at about 3x the list's
variety (Stephen: forms that existed in 1730 graveyards only; W2_ERA.md G1-G15) and the graveyard wood set.

Stones: board-shaped (itabi), boat-halo figure stones (funagata), round-headed slabs (kushigata), square pillars
(kakuchu, rare: flat and the new Kyoho pointed top), gorinto (small, large, re-stacked, fallen, a fragment heap),
hokyointo, a child's Jizo, field stones (single, a mound, a pair). Sizes, weathering (_w1 / _w2 + moss), tilt and
sink, broken tops, with and without carved posthumous names (B1's carved-text atlas only: grave_doshin_shinji, Kyoho 9;
grave_shakuni_myoshin, Hoei 2; crops give name-only / date-only faces). No family-name inscriptions (Meiji), no
polished black stone, no square-pillar rows, no muen-to pyramids.
Wood: sotoba slats (3 behind a stone, a rack), flower tubes, incense stand, bucket rack, fallen slats, a wooden grave
post on an earth mound (the poor grave).
Frame: origin = base centre on the terrain, +z = the inscribed face (towards the path). Plot grid 0.9 m (sidecar).
"""
import math
import random

import skit
from skit import (core, box, prism, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, beam, add_all,
                  leaves, litter, moss_top, moss_face, CARVED, CUT, FIELD, RIVER, BAMBOO, WOOD, MOSS, LEAF, CTEXT, SUMI,
                  GTEXT, GSUMI, EARTH, NEWWOOD, SILVER)
from props_wood import M, teoke
import props_stone as PS
import w2kit as K
from w2kit import X, Y, Z, ASH, SOOT

SQ = math.pi / 4
NAME = (0.28, 0.0, 0.72, 1.0)         # crop: the posthumous-name column of a grave_* cell
DATE_R = (0.74, 0.0, 1.0, 1.0)        # crop: the right-hand (year) column
DATE_L = (0.0, 0.0, 0.26, 1.0)        # crop: the left-hand (month-day / cyclical year) column
MEN = "grave_doshin_shinji"           # Kyoho 9 (1724), a man
WOMAN = "grave_shakuni_myoshin"       # Hoei 2 (1705), a woman (Shin sect)
# M1 (2026-09-30): the grave-names atlas jp_m_decal_carved_text_grave (13 cells, 14 kaimyo, 1670-1729; forms and dates
# in spikes/M1/M1_PROGRESS.md "Text"). Its three-column cells keep the columns at fixed fractions:
GNAME = (0.26, 0.0, 0.74, 1.0)        # the kaimyo column
GDATE_R = (0.70, 0.0, 1.0, 1.0)       # the era-year column
# kind -> (atlas material, cell, crop): every inscribed stone its own person; older forms on older stone types
KAIMYO = {
    "board": (GTEXT, "kaimyo_joshin_shinji_genroku8", None),
    "board_s": (GTEXT, "kaimyo_myotei_shinnyo_hoei4", GNAME),
    "board_tall_moss": (GTEXT, "kaimyo_myoju_zenjoni_kanbun10", None),
    "ab_leaning": (GTEXT, "kaimyo_soen_zenjomon_enpo6", None),
    "ab_board_broken": (CTEXT, WOMAN, (0.0, 0.42, 1.0, 1.0)),
    "boat_halo": (GTEXT, "kaimyo_kigen_dokaku_shinji_genroku11", GNAME),
    "boat_halo_child": (GTEXT, "kaimyo_shunko_doji_kyoho5", GNAME),
    "ab_boat_halo_sunk": (GTEXT, "kaimyo_enjaku_myosho_shinnyo_kyoho12", GNAME),
    "round": (GTEXT, "kaimyo_ryozen_shinji_kyoho14", None),
    "ab_round_lean": (GTEXT, "kaimyo_shaku_ryonen_kyoho8", None),
    "pillar": (GTEXT, "kaimyo_hozan_zenjomon_shotoku1", None),
    "pillar_pointed": (GTEXT, "kaimyo_chisei_shinnyo_kyoho10", None),
}


# ================================================================================================ parts
def base_stack(specs, wear=None, mat=CARVED):
    """Stacked base stones [(w, d, h), ...] bottom up; the lowest sits 5 cm into the ground. Returns (vis, cols, top)."""
    vis, cols, y = [], [], 0.0
    for i, (w, d, h) in enumerate(specs):
        y0 = y - (0.05 if i == 0 else 0.0)
        s = W(-w / 2, w / 2, y0, y + h, -d / 2, d / 2, mat, vis=(1, 2))
        if wear:
            s.wear = wear
        vis.append(s)
        cols.append(col(-w / 2, w / 2, y, y + h, -d / 2, d / 2, mat))
        y += h
    return vis, cols, y


def board_profile(w, h, peak=0.42):
    """Itabi: a flat board with a gabled (pointed) top."""
    return [(-w / 2, 0.0), (w / 2, 0.0), (w / 2, h - w * peak), (0.0, h), (-w / 2, h - w * peak)]


def arch_profile(w, h, k=6):
    pts = [(-w / 2, 0.0), (w / 2, 0.0), (w / 2, h - w / 2)]
    for i in range(1, k):
        a = math.pi * i / k
        pts.append((w / 2 * math.cos(a), h - w / 2 + w / 2 * math.sin(a)))
    pts.append((-w / 2, h - w / 2))
    return pts


def boat_profile(w, h):
    return [(-w * 0.44, 0.0), (w * 0.44, 0.0), (w / 2, h * 0.47), (w * 0.40, h * 0.76), (w * 0.17, h * 0.95),
            (0.0, h), (-w * 0.17, h * 0.95), (-w * 0.40, h * 0.76), (-w / 2, h * 0.47)]


def slab(pts, t, y0, wear=None, vis=(1, 2)):
    s = prism([(x, y + y0) for x, y in pts], "z", -t / 2, t / 2, CARVED, vis=vis)
    if wear:
        s.wear = wear
    return s


def nijo(w, y, z, wear=None):
    """The two incised lines under an itabi's gable, as two shallow raised bands (the cut shadow reads as lines)."""
    out = []
    for dy in (0.0, 0.03):
        s = W(-w / 2 + 0.004, w / 2 - 0.004, y + dy, y + dy + 0.012, z - 0.004, z + 0.004, CARVED, vis=(1,))
        if wear:
            s.wear = wear
        out.append(s)
    return out


def gorinto(s=1.0, wear=None, drop=(), res3=False):
    """Five-ring stupa of total ~0.6 * s: chirin (cube), suirin (sphere), karin (roof), furin (crescent / bowl),
    kurin (jewel). Returns ({ring: [solids]}, {ring: col}, heights)."""
    v, c, y = {}, {}, 0.0
    a = 0.20 * s
    v["chirin"] = [W(-a / 2, a / 2, -0.04 * s, 0.15 * s, -a / 2, a / 2, CARVED, vis=(1, 2) if not res3 else (1, 2, 3))]
    c["chirin"] = col(-a / 2, a / 2, 0.0, 0.15 * s, -a / 2, a / 2, CARVED)
    y = 0.15 * s
    r = 0.095 * s
    sp = [(0.0, y), (r * 0.55, y), (r, y + r * 0.6), (r * 0.95, y + r * 1.3), (r * 0.5, y + r * 1.85), (0.0, y + 1.9 * r)]
    v["suirin"] = [lathe(sp, 8, CARVED, vis=(1,)), lathe([sp[0], (r, y + r * 0.9), sp[-1]], 6, CARVED, vis=(2,),
                                                         smooth=False)]
    c["suirin"] = cyl_col(r * 0.92, y, y + 1.9 * r, n=6, mat=CARVED)
    y += 1.9 * r
    R = 0.115 * s
    kp = [(0.0, y), (R * 0.95, y), (R * 1.04, y + 0.022 * s), (R * 0.95, y + 0.035 * s), (R * 0.35, y + 0.10 * s),
          (0.0, y + 0.10 * s)]
    v["karin"] = [lathe(kp, 4, CARVED, vis=(1,), phase=SQ, smooth=False),
                  lathe([kp[0], kp[2], kp[-2], kp[-1]], 4, CARVED, vis=(2,), phase=SQ, smooth=False)]
    c["karin"] = cyl_col(R * 0.98, y, y + 0.10 * s, n=4, mat=CARVED)
    y += 0.10 * s
    fr = 0.055 * s
    fp = [(0.0, y), (fr * 0.6, y), (fr, y + 0.035 * s), (fr * 0.85, y + 0.05 * s), (0.0, y + 0.05 * s)]
    v["furin"] = [lathe(fp, 8, CARVED, vis=(1,)), lathe([fp[0], fp[2], fp[-1]], 4, CARVED, vis=(2,), smooth=False)]
    c["furin"] = cyl_col(fr * 0.9, y, y + 0.05 * s, n=6, mat=CARVED)
    y += 0.05 * s
    jr = 0.05 * s
    jp = [(0.0, y), (jr * 0.6, y), (jr, y + 0.03 * s), (jr * 0.75, y + 0.065 * s), (0.0, y + 0.10 * s)]
    v["kurin"] = [lathe(jp, 8, CARVED, vis=(1,)), lathe([jp[0], jp[2], jp[-1]], 4, CARVED, vis=(2,), smooth=False)]
    c["kurin"] = cyl_col(jr * 0.9, y, y + 0.095 * s, n=6, mat=CARVED)
    y += 0.10 * s
    if res3:
        v["suirin"].append(lathe([sp[0], (r, y - 0.35 * s), sp[-1]], 4, CARVED, vis=(3,), smooth=False))
        v["karin"].append(lathe([kp[0], kp[1], kp[-1]], 4, CARVED, vis=(3,), phase=SQ, smooth=False))
        v["kurin"].append(lathe([(0.0, 0.40 * s), (fr, 0.40 * s), (0.0, y)], 4, CARVED, vis=(3,), smooth=False))
    if wear:
        for ss in v.values():
            for q in ss:
                q.wear = wear
    return v, c, y


def lay(ss, rx=0.0, ry=0.0, rz=0.0, at=(0.0, 0.0), lift=0.0):
    """Lay a group on the ground: rotate, then drop it so its lowest visual point is `lift` above y = 0, at (x, z)."""
    g = xfs(ss, rx=rx, ry=ry, rz=rz)
    vv = [v for s in g if s.vis for v in s.verts] or [v for s in g for v in s.verts]
    lo = min(v[1] for v in vv)
    cx = sum(v[0] for v in vv) / len(vv)
    cz = sum(v[2] for v in vv) / len(vv)
    return xfs(g, t=(at[0] - cx, lift - lo, at[1] - cz))


# ================================================================================================ gravestones
def grave(kind):
    ab = kind.startswith("ab")
    rr = random.Random(core.hash_str(kind))
    big = kind in ("gorinto_l", "hokyointo", "ab_hokyointo_broken")
    P = SPart("grave_stones", budget="box" if big else "small", res3=big, mass=200.0, bury=0.12)
    wear = "_w2" if (ab or "moss" in kind or kind in ("gorinto_heap", "field_mound")) else "_w1"
    P.wear = wear
    vis, cols, tx = [], [], []
    lean = None            # (rx, rz, sink)
    top = 0.0
    # ---------------------------------------------------------------- board-shaped (itabi)
    if kind in ("board", "board_s", "board_tall_moss", "ab_leaning", "ab_board_broken"):
        w, h, t, bases = {
            "board": (0.30, 0.62, 0.14, [(0.48, 0.32, 0.13)]),
            "board_s": (0.24, 0.48, 0.12, []),
            "board_tall_moss": (0.32, 0.80, 0.15, [(0.56, 0.36, 0.12), (0.44, 0.28, 0.10)]),
            "ab_leaning": (0.30, 0.64, 0.14, [(0.48, 0.32, 0.13)]),
            "ab_board_broken": (0.30, 0.66, 0.14, [(0.48, 0.32, 0.13)]),
        }[kind]
        tmat, cell, crop = KAIMYO[kind]
        bv, bc, y0 = base_stack(bases, wear=wear)
        vis += bv
        cols += bc
        if not bases:
            y0 = -0.10                       # set straight into the ground
        hh = h if kind != "ab_board_broken" else 0.40
        prof = board_profile(w, h) if kind != "ab_board_broken" else \
            [(-w / 2, 0.0), (w / 2, 0.0), (w / 2, 0.36), (w * 0.2, 0.42), (-w * 0.1, 0.38), (-w / 2, 0.43)]
        vis.append(slab(prof, t, y0, wear=wear))
        if bases and kind != "ab_board_broken":
            cols.append(col_solid(slab(prof, t, y0)))
        else:     # set in the ground, or the jagged broken stump (not convex): a box up to the break
            cols.append(col(-w / 2, w / 2, max(0.0, y0), y0 + (0.36 if kind == "ab_board_broken" else
                                                                 max(p[1] for p in prof) - w * 0.42), -t / 2, t / 2,
                            CARVED))
        if kind != "ab_board_broken":
            vis += nijo(w, y0 + h - w * 0.42 - 0.07, t / 2, wear=wear)
        th = min(0.42, (hh - w * 0.42 - 0.08)) if kind != "ab_board_broken" else 0.26
        tc = y0 + (hh - w * 0.42 - 0.08) / 2 + 0.02 if kind != "ab_board_broken" else y0 + 0.18
        tx.append(K.carved((0.0, tc, t / 2), X, Y, th, cell, wear=wear, crop=crop, mat=tmat))
        top = y0 + hh
        if kind == "ab_board_broken":
            # the snapped-off gable lies face-up in front of the stone
            piece = [slab([(-w / 2, 0.0), (w / 2, 0.0), (w / 2, h - 0.40 - w * 0.42), (0.0, h - 0.40),
                           (-w / 2, h - 0.40 - w * 0.42)], t, 0.0, wear="_w2")]
            piece.append(col_solid(slab([(-w / 2, 0.0), (w / 2, 0.0), (w / 2, h - 0.40 - w * 0.42), (0.0, h - 0.40),
                                         (-w / 2, h - 0.40 - w * 0.42)], t, 0.0)))
            pz = lay(piece, rx=-88.0, ry=24.0, at=(0.18, 0.42), lift=-0.01)
            vis += [s for s in pz if s.vis]
            cols += [s for s in pz if not s.vis]
            vis.append(litter(rr.randint(1, 99), 0.1, 0.4, 0.45))
        if kind == "board_tall_moss":
            vis.append(K.moss_strip([(-w / 2 + 0.02, y0 + h - w * 0.42, 0.0), (0.0, y0 + h - 0.01, 0.0)], t * 0.8,
                                    seed=3, wear="_w2", off=0.006))
            vis.append(moss_face((0.0, y0 + 0.25, t / 2), X, Y, w * 0.9, 0.22, seed=4, wear="_w1", off=0.004))
        if kind == "ab_leaning":
            lean = (-13.0, 5.0, 0.07)
        P.dim("stone_h", h, h, tol=0.002)
        P.dim("stone_w", w, w, tol=0.002)
    # ---------------------------------------------------------------- boat-halo (funagata)
    elif kind in ("boat_halo", "boat_halo_child", "ab_boat_halo_sunk"):
        w, h, t, fig, bases = {
            "boat_halo": (0.40, 0.80, 0.16, 0.50, [(0.52, 0.34, 0.12)]),
            "boat_halo_child": (0.26, 0.48, 0.11, 0.32, []),
            "ab_boat_halo_sunk": (0.38, 0.76, 0.15, 0.48, [(0.50, 0.32, 0.12)]),
        }[kind]
        bv, bc, y0 = base_stack(bases, wear=wear)
        vis += bv
        cols += bc
        if not bases:
            y0 = -0.06
        pr = boat_profile(w, h)
        vis.append(slab(pr, t, y0, wear=wear, vis=(1, 2)))
        cols.append(col_solid(slab(pr, t, max(0.0, y0))))
        # the Jizo / Amida in relief on the face (B3b's figure, the back half cut away)
        fg = PS.jizo_figure(fig, relief=True, vis_3=(), vis_lo=())
        fg = [PS.scale_z(s, 0.55) for s in fg]
        vis += xfs(fg, t=(-0.035 * (kind != "boat_halo_child"), y0 + 0.06, t / 2 - 0.01))
        tmat, cell, crop = KAIMYO[kind]
        if kind != "boat_halo_child":
            tx.append(K.carved((w * 0.30, y0 + h * 0.45, t / 2), X, Y, h * 0.44, cell, wear=wear, crop=crop, mat=tmat))
        else:   # M1: later boat-halo stones are mostly children's graves: the child's name beside the Jizo
            tx.append(K.carved((w * 0.31, y0 + h * 0.42, t / 2), X, Y, h * 0.40, cell, wear=wear, crop=crop, mat=tmat))
        if kind == "ab_boat_halo_sunk":
            lean = (11.0, -4.0, 0.14)
            vis.append(moss_face((0.0, y0 + h * 0.75, t / 2 + 0.03), X, Y, w * 0.7, h * 0.3, seed=7, wear="_w2",
                                 off=0.004))
        top = y0 + h
        P.dim("stone_h", h, h, tol=0.002)
        P.dim("figure_h", fig, fig, tol=0.002)
    # ---------------------------------------------------------------- round-headed (kushigata)
    elif kind in ("round", "round_s_plain", "ab_round_lean"):
        w, h, t, bases = {
            "round": (0.30, 0.70, 0.20, [(0.46, 0.36, 0.14)]),
            "round_s_plain": (0.26, 0.50, 0.16, []),
            "ab_round_lean": (0.30, 0.72, 0.19, [(0.46, 0.36, 0.14)]),
        }[kind]
        tmat, cell, _ = KAIMYO.get(kind, (None, None, None))
        bv, bc, y0 = base_stack(bases, wear=wear, mat=CUT)
        vis += bv
        cols += bc
        if not bases:
            y0 = -0.08
        pr = arch_profile(w, h)
        vis.append(slab(pr, t, y0, wear=wear))
        cols.append(col_solid(slab(pr, t, max(0.0, y0))))
        if cell:
            tx.append(K.carved((0.0, y0 + (h - w / 2) * 0.55, t / 2), X, Y, min(0.42, h - w / 2 - 0.06), cell, wear=wear,
                               mat=tmat))
        if kind == "ab_round_lean":
            lean = (-4.0, -12.0, 0.08)
        top = y0 + h
        P.dim("stone_h", h, h, tol=0.002)
    # ---------------------------------------------------------------- square pillar (kakuchu), rare in 1730
    elif kind in ("pillar", "pillar_pointed"):
        if kind == "pillar":
            a, h, bases, cap = 0.22, 0.62, [(0.62, 0.62, 0.15), (0.46, 0.46, 0.12), (0.34, 0.34, 0.10)], 0.03
        else:
            a, h, bases, cap = 0.20, 0.66, [(0.54, 0.54, 0.14), (0.38, 0.38, 0.11)], 0.11
        bv, bc, y0 = base_stack(bases, wear=wear, mat=CUT)
        vis += bv
        cols += bc
        vis.append(W(-a / 2, a / 2, y0, y0 + h, -a / 2, a / 2, CARVED, vis=(1, 2)))
        pyr = core.Solid([(-a / 2, y0 + h, -a / 2), (a / 2, y0 + h, -a / 2), (a / 2, y0 + h, a / 2), (-a / 2, y0 + h, a / 2),
                          (0.0, y0 + h + cap, 0.0)], [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]], CARVED,
                         vis=(1, 2))
        vis.append(pyr)
        cols.append(col(-a / 2, a / 2, y0, y0 + h, -a / 2, a / 2, CARVED))
        tmat, cell, _ = KAIMYO[kind]
        tx.append(K.carved((0.0, y0 + h * 0.52, a / 2), X, Y, h * 0.80, cell, wear=wear, crop=GNAME, mat=tmat))
        tx.append(K.carved((a / 2, y0 + h * 0.55, 0.0), (0.0, 0.0, -1.0), Y, h * 0.62, cell, wear=wear, crop=GDATE_R,
                           mat=tmat))
        # the water hollow (mizubachi) cut in the front of the upper base, leaves in it
        bw = bases[-1][0]
        yb = y0
        vis += K.hollow([(yb - 0.002, K.rect(-0.08, 0.08, a / 2 + 0.005, bw / 2 - 0.012)),
                         (yb + 0.001, K.rect(-0.08, 0.08, a / 2 + 0.005, bw / 2 - 0.012))],
                        K.rect(-0.06, 0.06, a / 2 + 0.02, bw / 2 - 0.03), yb + 0.001, yb - 0.035, CARVED, vis=(1,),
                        fill=yb - 0.02, fill_wear="_w2")
        vis.append(moss_top(11, 0.0, -bases[0][0] * 0.3, bases[0][0] * 0.25, bases[0][2] - 0.001, wear="_w1",
                            sx=1.4, sz=0.5))
        top = y0 + h + cap
        P.dim("shaft_h", h, h, tol=0.002)
        P.dim("shaft_a", a, a, tol=0.002)
        P.notes.append("rare in 1730 (about 5 % of stones); never in uniform rows (W2_ERA G4)")
    # ---------------------------------------------------------------- gorinto
    elif kind in ("gorinto_s", "gorinto_l", "gorinto_stack", "ab_gorinto_fallen"):
        s = {"gorinto_s": 1.0, "gorinto_l": (2.0 - 0.36) / 0.58, "gorinto_stack": 1.0, "ab_gorinto_fallen": 1.15}[kind]
        y0 = 0.0
        if kind == "gorinto_l":
            # a two-course platform (kidan) under the large stupa
            bv, bc, y0 = base_stack([(1.20, 1.20, 0.20), (0.92, 0.92, 0.16)], wear=wear)
            vis += bv
            cols += bc
        v, c, hgt = gorinto(s, wear=wear, res3=(kind == "gorinto_l"))
        if kind == "gorinto_stack":
            # re-stacked from two stupas: the roof and jewel from a bigger one, the crescent missing, rings askew
            v2, c2, _ = gorinto(1.25, wear="_w2")
            for k in ("karin", "kurin"):
                shift = v["karin"][0].bbox()[2] - v2["karin"][0].bbox()[2]
                v[k] = xfs(v2[k], ry=rr.uniform(-20, 20), t=(0.012, shift if k == "karin" else 0.0, -0.01))
                c[k] = xf(c2[k], t=(0.012, shift if k == "karin" else 0.0, -0.01))
            # drop the crescent: the jewel sits straight on the roof
            jlo = v["kurin"][0].bbox()[2]
            rtop = v["karin"][0].bbox()[3]
            v["kurin"] = xfs(v["kurin"], t=(0.0, rtop - jlo - 0.004, 0.0))
            c["kurin"] = xf(c["kurin"], t=(0.0, rtop - c["kurin"].bbox()[2] + 0.001, 0.0))
            del v["furin"], c["furin"]
            v["suirin"] = xfs(v["suirin"], ry=25.0, t=(-0.01, 0.0, 0.008))
        if kind == "ab_gorinto_fallen":
            # quake: the roof, crescent and jewel lie beside the cube and sphere
            for k, (rx_, rz_, at) in {"karin": (0.0, 160.0, (0.32, 0.18)), "furin": (90.0, 0.0, (-0.28, 0.30)),
                                      "kurin": (0.0, 75.0, (0.10, 0.48))}.items():
                g = lay(v.pop(k) + [c.pop(k)], rx=rx_, rz=rz_, ry=rr.uniform(0, 90), at=at, lift=-0.01)
                vis += [q for q in g if q.vis]
                cols += [q for q in g if not q.vis]
            vis.append(litter(23, 0.1, 0.3, 0.5))
        for k in v:
            vis += xfs(v[k], t=(0.0, y0, 0.0))
            cols.append(xf(c[k], t=(0.0, y0, 0.0)))
        if kind in ("gorinto_s", "gorinto_l"):
            ks = v["karin"][0].bbox()
            vis.append(moss_top(17, 0.0, 0.0, 0.08 * s, ks[2] + y0 + 0.024 * s, wear="_w1"))
        vis.append(moss_top(18, -0.04 * s, -0.05 * s, 0.07 * s, y0 + 0.15 * s + 0.001, wear="_w2"))
        top = y0 + hgt
        P.dim("total_h", round(0.60 * s, 3) if kind != "gorinto_l" else 2.0, y0 + hgt if kind != "gorinto_l" else
              round(y0 + hgt, 2), tol=0.05 if kind != "gorinto_l" else 0.08)
        if kind == "gorinto_stack":
            P.notes.append("re-stacked by later hands from two stupas: roof and jewel too big, crescent missing")
    elif kind == "gorinto_heap":
        # a few medieval fragments gathered at a plot corner: NOT a muen-to pyramid (W2_ERA G9 / G10)
        pieces = []
        for i, (sc, ring, at, rot) in enumerate([(1.0, "chirin", (-0.12, 0.0), (0, 10, 0)), (1.2, "chirin", (0.20, -0.08), (0, -25, 0)),
                                                 (1.0, "suirin", (0.02, 0.12), (30, 0, 15)), (0.9, "suirin", (-0.30, 0.18), (70, 0, 0)),
                                                 (1.1, "karin", (0.05, -0.12), (0, 30, 170)), (1.0, "karin", (0.34, 0.20), (12, 0, 25)),
                                                 (1.0, "kurin", (-0.22, -0.20), (0, 0, 80))]):
            v, c, _ = gorinto(sc, wear="_w2" if i % 2 else "_w1")
            g = lay(v[ring] + [c[ring]], rx=rot[0], ry=rot[1], rz=rot[2], at=at, lift=-0.015)
            pieces.append(g)
        # the sphere on top of the two cubes
        top_piece = pieces[2]
        pieces[2] = xfs(top_piece, t=(0.0, 0.10, 0.0))
        for g in pieces:
            vis += [q for q in g if q.vis]
        allv = [v_ for g in pieces for q in g if q.vis for v_ in q.verts]
        xs = [p[0] for p in allv]
        zs = [p[2] for p in allv]
        cols.append(col(min(xs) + 0.03, max(xs) - 0.03, 0.0, 0.26, min(zs) + 0.03, max(zs) - 0.03, CARVED))
        vis.append(litter(29, 0.0, 0.0, 0.6, sx=1.3))
        vis.append(moss_top(30, -0.1, 0.0, 0.12, 0.155, wear="_w2"))
        top = max(p[1] for p in allv)
        P.dim("heap_h", 0.40, top, tol=0.12)
        P.notes.append("a small heap of old fragments; the big muen-to pyramids are Meiji and later (W2_ERA G10)")
    # ---------------------------------------------------------------- hokyointo
    elif kind in ("hokyointo", "ab_hokyointo_broken"):
        bv, bc, y0 = base_stack([(0.62, 0.62, 0.16), (0.48, 0.48, 0.18)], wear=wear)
        vis += bv
        cols += bc
        # body (toshin) with four recessed panels (seed-syllable niches; the syllables need atlas cells we lack)
        a = 0.32
        vis.append(W(-a / 2, a / 2, y0, y0 + 0.30, -a / 2, a / 2, CARVED, vis=(1, 2, 3)))
        cols.append(col(-a / 2, a / 2, y0, y0 + 0.30, -a / 2, a / 2, CARVED))
        for ang in (0.0, 90.0, 180.0, 270.0):
            vis.append(xf(W(-0.10, 0.10, y0 + 0.06, y0 + 0.24, a / 2 - 0.004, a / 2 + 0.003, CARVED, vis=(1,)),
                          ry=ang))
        y = y0 + 0.30
        # the roof: two steps under, the eave slab, five steps over, corner horns
        steps_ = [(0.36, 0.035), (0.42, 0.035), (0.56, 0.07), (0.44, 0.035), (0.36, 0.035), (0.28, 0.035),
                  (0.20, 0.035), (0.14, 0.035)]
        roof = []
        for w_, h_ in steps_:
            roof.append(W(-w_ / 2, w_ / 2, y, y + h_, -w_ / 2, w_ / 2, CARVED, vis=(1,)))
            y += h_
        ry0 = y0 + 0.30
        roof.append(W(-0.28, 0.28, ry0, y, -0.28, 0.28, CARVED, vis=(2,)))
        roof.append(core.Solid([(-0.28, ry0, -0.28), (0.28, ry0, -0.28), (0.28, ry0, 0.28), (-0.28, ry0, 0.28),
                                (0.0, y, 0.0)], [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]], CARVED, vis=(3,)))
        eave_y = y0 + 0.30 + 0.07 + 0.07
        horns = []
        for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            # the corner horn (sumi-kazari): an upright ear-shaped plate leaning outward
            horns.append(beam((sx * 0.235, eave_y - 0.01, sz * 0.235), (sx * 0.285, eave_y + 0.15, sz * 0.285), 0.09,
                              0.03, CARVED, up=(sx * 0.7, 0.0, sz * 0.7), vis=(1, 2)))
        rc = col(-0.28, 0.28, ry0, y, -0.28, 0.28, CARVED)
        # the finial (sorin): a ringed rod with a jewel
        fy = y
        rod = [(0.0, fy), (0.045, fy)]
        for i in range(9):
            rod += [(0.045, fy + 0.035 * i + 0.01), (0.035, fy + 0.035 * i + 0.025)]
        rod += [(0.03, fy + 0.34), (0.065, fy + 0.38), (0.05, fy + 0.45), (0.0, fy + 0.52)]
        fin = [lathe(rod, 6, CARVED, vis=(1,), smooth=False), pole((0.0, fy, 0.0), (0.0, fy + 0.52, 0.0), 0.04, CARVED,
                                                                    n=4, vis=(2, 3))]
        fc = cyl_col(0.045, fy, fy + 0.50, n=6, mat=CARVED)
        if wear:
            for q in roof + horns + fin:
                q.wear = wear
        vis += roof + horns
        cols.append(rc)
        if kind == "ab_hokyointo_broken":
            g = lay(fin + [fc], rz=88.0, ry=35.0, at=(0.62, 0.52), lift=-0.01)
            vis += [q for q in g if q.vis]
            cols += [q for q in g if not q.vis]
            # one horn snapped off and lying on the base
            vis.remove(horns[1])
            hn = lay([horns[1]], rz=70.0, at=(-0.25, 0.30), lift=0.16 - 0.01)
            vis += hn
            vis.append(litter(31, 0.3, 0.3, 0.6, sx=1.3))
            top = fy
        else:
            vis += fin
            cols.append(fc)
            top = fy + 0.52
        vis.append(moss_top(32, 0.0, 0.0, 0.16, eave_y + 0.001 - 0.07, wear="_w2"))
        P.dim("total_h", 1.5, fy + 0.52, tol=0.05)
    # ---------------------------------------------------------------- a child's Jizo
    elif kind == "jizo_child":
        H = 0.40
        bv, bc, y0 = base_stack([(0.32, 0.26, 0.14)], wear=wear)
        vis += bv
        cols += bc
        vis += xfs(PS.jizo_figure(H, vis_3=()), t=(0.0, y0, 0.0))
        cols.append(cyl_col(0.17 * H, y0, y0 + H, n=6, mat=CARVED))
        vis += xfs(PS.bib_and_cap(H), t=(0.0, y0, 0.0))
        tx.append(K.carved((0.0, y0 * 0.5, 0.13), X, Y, 0.10, "enmei_jizo", wear=wear, crop=(0.0, 0.0, 1.0, 0.4)))
        top = y0 + H
        P.dim("figure_h", H, H, tol=0.002)
        P.notes.append("a child's grave: small standing Jizo, a faded rag bib (G1 A3 answer 4)")
    # ---------------------------------------------------------------- field stones (poor graves)
    elif kind in ("field", "field_mound", "field_pair"):
        if kind == "field":
            st = core.stone(rr, 0.0, 0.0, 0.30, 0.20, 0.50, 0.45, FIELD, bury=0.08, n=7, flat_top=0.45, vis=(1, 2))
            st = xf(st, rz=6.0)
            vis.append(st)
            cols.append(col_solid(st, FIELD))
            vis.append(moss_top(41, -0.02, -0.04, 0.06, max(v[1] for v in st.verts) - 0.04, wear="_w1"))
            top = 0.45
        elif kind == "field_mound":
            # a low earth mound with a field stone at its head (the commonest poor grave)
            m = lathe([(0.0, -0.03), (0.58, -0.03), (0.45, 0.06), (0.22, 0.12), (0.0, 0.13)], 8, EARTH, vis=(1, 2),
                      smooth=True)
            m = xf(m, t=(0.0, 0.0, 0.0))
            m.verts = [(v[0], v[1], v[2] * 1.5) for v in m.verts]
            m.fm = None
            m.fn = None
            m.vn = None
            m.finalize()
            m.wear = "_w1"
            vis.append(m)
            st = core.stone(rr, 0.0, -0.62, 0.26, 0.16, 0.36, 0.32, FIELD, bury=0.06, n=7, flat_top=0.5, vis=(1, 2))
            vis.append(st)
            cols.append(col_solid(st, FIELD))
            vis += K.pebbles(43, 0.0, 0.1, 0.35, n=4)
            top = 0.32
            lt = xf(litter(45, 0.0, 0.05, 0.30, sx=0.9, sz=1.3), t=(0.0, 0.12, 0.0))
            vis.append(lt)
            P.notes.append("the mound is bare earth (M1: jp_m_ground_earth_bare) with a little litter; no collision on "
                           "it (walk over)")
        else:
            for i, (x, hh, rz_) in enumerate(((-0.18, 0.34, -3.0), (0.16, 0.26, 9.0))):
                st = core.stone(rr, x, 0.0, 0.22, 0.15, hh + 0.05, hh, FIELD if i == 0 else RIVER, bury=0.06, n=7,
                                flat_top=0.5, vis=(1, 2))
                st = xf(st, rz=rz_, pivot=(x, 0.0, 0.0))
                vis.append(st)
                cols.append(col_solid(st, FIELD))
            vis.append(litter(44, 0.0, 0.15, 0.4))
            top = 0.34
        P.dim("height", {"field": 0.45, "field_mound": 0.32, "field_pair": 0.34}[kind], top, tol=0.01)
    else:
        raise KeyError(kind)
    # ---- lichen / moss on every stone: the base tops and the north (back) face
    if kind not in ("field_mound", "gorinto_heap"):
        bb = [v for s in vis if s.vis for v in s.verts]
        zmin = min(v[2] for v in bb)
        vis.append(moss_face((0.0, 0.12, zmin - 0.002), (-1.0, 0.0, 0.0), Y, 0.24, 0.18, seed=rr.randint(0, 99),
                             wear="_w1" if wear == "_w1" else "_w2", off=0.0))
    ss = vis + tx + cols
    if lean:
        rx_, rz_, sink = lean
        ss = K.tilt(ss, rx=rx_, rz=rz_, pivot=(0.0, 0.0, 0.0), sink=sink)
        P.bury = max(P.bury, sink + 0.14)
        ss.append(litter(rr.randint(50, 90), 0.05, 0.25, 0.45))
        P.notes.append("abandoned: leaning %.0f / %.0f deg, sunk %.2f m" % (rx_, rz_, sink))
    add_all(P, ss)
    lo = min(v[1] for s in P.solids if s.vis for v in s.verts)
    P.bury = max(P.bury, -lo + 0.001)
    P.extra.update({"plot_grid_m": 0.9, "inscription": sorted({getattr(s, "cell", "") for s in tx}) or None})
    return P


# ================================================================================================ wood set
def sotoba(h=1.05, w=0.075, t=0.012, notched=True, wear="_w2", text=True, vis=(1,)):
    """A memorial slat standing on y = 0 (its foot 0.15 in the ground): shaft, the five-ring notches, a pointed tip;
    faded ink on the front."""
    out = []
    y = h - 0.22 if notched else h - 0.06
    out.append(W(-w / 2, w / 2, -0.15, y, -t / 2, t / 2, WOOD, vis=vis))
    if notched:
        for ww, hh in ((0.70, 0.03), (1.0, 0.06), (0.70, 0.025), (1.0, 0.045)):
            out.append(W(-w * ww / 2, w * ww / 2, y, y + hh, -t / 2, t / 2, WOOD, vis=vis))
            y += hh
    tip = prism([(-w / 2, y), (w / 2, y), (w / 2, y + 0.02), (0.0, h), (-w / 2, y + 0.02)], "z", -t / 2, t / 2, WOOD,
                vis=vis)
    out.append(tip)
    if text:
        out.append(K.inked((0.0, (h - 0.22) * 0.55, t / 2), X, Y, min(0.40, (h - 0.25) * 0.75), "sotoba_namuamida",
                           wear="_w2"))
    lo = W(-w / 2, w / 2, -0.15, h, -t / 2, t / 2, WOOD, vis=(2,))
    out.append(lo)
    for s in out:
        if s.mats == WOOD:
            s.wear = wear
    return out


def bohyo_mound(seed, r=0.50, h=0.11, sz=1.4, sunk=False, wear="_w1", litter_r=0.22):
    """W3: the earth mound under a grave post (M1: bare earth, jp_m_ground_earth_bare; _w0 = fresh moist clods). sunk:
    the coffin has collapsed, so the rim stands higher than the middle. Returns visual solids (mound + a litter patch
    on its top)."""
    if sunk:
        prof = [(0.0, -0.03), (r, -0.03), (r * 0.84, h), (r * 0.5, h * 0.55), (0.0, h * 0.25)]
        ytop = h * 0.25
    else:
        prof = [(0.0, -0.03), (r, -0.03), (r * 0.8, h * 0.45), (r * 0.4, h * 0.91), (0.0, h)]
        ytop = h
    m = lathe(prof, 8, EARTH, vis=(1, 2))
    m.verts = [(v[0], v[1], v[2] * sz) for v in m.verts]
    m.fm = None
    m.fn = None
    m.vn = None
    m.finalize()
    m.wear = wear
    lt = xf(litter(seed, 0.0, 0.0, litter_r, sx=0.9, sz=1.3), t=(0.0, ytop, 0.0))
    return [lt, m]


def bohyo_post(a, h, z0, mat=WOOD, wear="_w1", tip=0.06, text=True, th=None, crop=None, ink="_w2", cap=False,
               cell=None):
    """W3: a square grave post standing at z0 (its foot 0.20 in the ground), pointed top (tip > 0), flat top
    (tip = 0) or a small two-board gabled cap (cap=True: the kasa-toba form, W2_ERA W5); nenbutsu in ink on the front
    (+z), whole or cropped. Returns (visual solids, collision box)."""
    y1 = h - tip
    out = [W(-a / 2, a / 2, -0.20, y1, z0 - a / 2, z0 + a / 2, mat, vis=(1, 2))]
    if tip > 0:
        out.append(core.Solid([(-a / 2, y1, z0 - a / 2), (a / 2, y1, z0 - a / 2), (a / 2, y1, z0 + a / 2),
                               (-a / 2, y1, z0 + a / 2), (0.0, h, z0)], [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4],
                                                                         [3, 0, 4]], mat, vis=(1,)))
    if cap:
        e, t, rise = a / 2 + 0.05, 0.018, 0.075
        L = a + 0.10
        for sz_ in (1, -1):
            # one board: ridge (y1 + rise, z0) down to the eave (y1 - 0.01, z0 + sz_ * e), 1.8 cm thick
            poly = [(y1 + rise, z0), (y1 - 0.01, z0 + sz_ * e), (y1 - 0.01 + t, z0 + sz_ * e), (y1 + rise + t, z0)]
            out.append(prism(poly, "x", -L / 2, L / 2, mat, vis=(1, 2)))
    for s in out:
        s.wear = wear
    if text and cell:
        # M1: a posthumous name in ink (jp_m_decal_sumi_text_grave): the kaimyo column on the front, the era year on
        # the right-hand side face (as on the square-pillar stones), each at the cell's own aspect (no squeezing)
        cw, ch = skit.cell_size(GSUMI, cell)
        nw = cw * (GNAME[2] - GNAME[0])
        th = th or min(0.42, (y1 - 0.12) * 0.70, a * 0.85 * ch / nw)
        yc = y1 - 0.05 - th / 2
        out.append(K.inked((0.0, yc, z0 + a / 2), X, Y, th, cell, wear=ink, crop=GNAME, mat=GSUMI))
        dw = cw * (GDATE_R[2] - GDATE_R[0])
        dh = min(th, a * 0.85 * ch / dw)
        out.append(K.inked((a / 2, y1 - 0.05 - dh / 2, z0), (0.0, 0.0, -1.0), Y, dh, cell, wear=ink, crop=GDATE_R,
                           mat=GSUMI))
    elif text:
        th = th or min(0.40, (y1 - 0.12) * 0.62)
        yc = y1 - 0.06 - th / 2
        out.append(K.inked((0.0, yc, z0 + a / 2), X, Y, th, "sotoba_namuamida", wear=ink, width=a * 0.78, crop=crop))
    top = y1 + (0.075 + 0.018 if cap else 0.0)
    return out, col(-a / 2, a / 2, 0.0, top, z0 - a / 2, z0 + a / 2, mat)


def grave_wood(kind):
    rr = random.Random(core.hash_str("gw" + kind))
    ab = kind.startswith("ab")
    flat = kind in ("sotoba_x3", "ab_fallen", "ab_bohyo_rotted")
    P = SPart("grave_wood", budget="small", mass=40.0, bury=0.16, flat=flat)
    P.wear = "_w2"
    vis, cols = [], []
    if kind == "sotoba_x3":
        for i, x in enumerate((-0.10, 0.0, 0.10)):
            hh = (1.05, 1.20, 0.90)[i]
            s = sotoba(hh, wear="_w2" if i != 1 else "_w1")
            vis += xfs(s, rx=rr.uniform(-6, 2), rz=rr.uniform(-5, 5), t=(x, 0.0, -0.02 * i))
        P.dim("sotoba_h", 1.05, 1.05, tol=0.001)
        P.notes.append("stands 0.15-0.25 behind a gravestone; no collision (thin slats)")
    elif kind == "rack":
        L, H = 1.82, 1.00
        for sx in (-1, 1):
            vis.append(W(sx * L / 2 - 0.035, sx * L / 2 + 0.035, -0.20, H, -0.035, 0.035, WOOD, vis=(1, 2)))
            cols.append(col(sx * L / 2 - 0.035, sx * L / 2 + 0.035, 0.0, H, -0.035, 0.035, WOOD))
        vis.append(W(-L / 2 - 0.06, L / 2 + 0.06, H - 0.07, H - 0.02, -0.03, 0.03, WOOD, vis=(1, 2)))
        vis.append(W(-L / 2 + 0.035, L / 2 - 0.035, 0.38, 0.43, -0.025, 0.025, WOOD, vis=(1,)))
        cols.append(col(-L / 2 + 0.036, L / 2 - 0.036, H - 0.07, H - 0.02, -0.03, 0.03, WOOD))
        n = 9
        for i in range(n):
            x = -L / 2 + 0.15 + (L - 0.30) * i / (n - 1) + rr.uniform(-0.03, 0.03)
            hh = rr.choice((1.05, 1.20, 1.35))
            s = sotoba(hh, notched=False, wear="_w2" if i % 3 else "_w1", text=(i % 2 == 0))
            # leaning on the top rail from the front: foot 0.25 out
            ang = math.degrees(math.atan2(0.25, H - 0.05))
            vis += xfs(s, rx=-ang + rr.uniform(-2, 2), t=(x, 0.0, 0.25 + 0.03))
        P.dim("rack_len", 1.82, L, tol=0.001)
        P.dim("rack_h", 1.0, H, tol=0.001)
    elif kind == "tubes":
        st = W(-0.15, 0.15, -0.05, 0.10, -0.06, 0.06, CUT, vis=(1, 2))
        vis.append(st)
        cols.append(col(-0.15, 0.15, 0.0, 0.10, -0.06, 0.06, CUT))
        for sx in (-1, 1):
            tb = lathe([(0.03, 0.10), (0.03, 0.40), (0.024, 0.40), (0.024, 0.14), (0.0, 0.14)], 6, BAMBOO, vis=(1,),
                       smooth=True)
            tb.wear = "_w2"
            vis.append(xf(tb, t=(sx * 0.10, 0.0, 0.0)))
            vis.append(xf(lathe([(0.03, 0.10), (0.03, 0.40), (0.0, 0.40)], 4, BAMBOO, vis=(2,), smooth=False),
                          t=(sx * 0.10, 0.0, 0.0)))
        # dead black shikimi stems in one tube
        for k in range(4):
            vis.append(pole((-0.10, 0.36, 0.0), (-0.10 + rr.uniform(-0.12, 0.10), 0.62 + rr.uniform(-0.06, 0.06),
                                                 rr.uniform(-0.08, 0.08)), 0.005, SOOT, n=3, vis=(1,), wear="_w2"))
        vis.append(leaves(5, 0.10, 0.0, 0.022, 0.30, wear="_w2"))
        P.dim("tube_h", 0.30, 0.30, tol=0.001)
    elif kind == "incense":
        outer = [(-0.04, K.rect(-0.14, 0.14, -0.10, 0.10)), (0.20, K.rect(-0.14, 0.14, -0.10, 0.10))]
        vis += K.hollow(outer, K.rect(-0.10, 0.10, -0.06, 0.06), 0.20, 0.14, CARVED, vis=(1,), fill=0.16,
                        fill_mat=ASH, fill_wear="_w2", wear="_w1")
        vis.append(W(-0.14, 0.14, -0.04, 0.20, -0.10, 0.10, CARVED, vis=(2,)))
        cols.append(col(-0.14, 0.14, 0.0, 0.20, -0.10, 0.10, CARVED))
        for k in range(5):
            x, z = rr.uniform(-0.07, 0.07), rr.uniform(-0.04, 0.04)
            vis.append(pole((x, 0.16, z), (x + rr.uniform(-0.01, 0.01), 0.16 + rr.uniform(0.02, 0.06), z), 0.0025, SOOT,
                            n=3, vis=(1,), wear="_w2"))
        vis.append(moss_top(6, 0.06, -0.06, 0.04, 0.201, wear="_w1"))
        P.dim("stand_h", 0.20, 0.20, tol=0.001)
        P.notes.append("a simple stone with an ash hollow; burnt stick stubs")
    elif kind == "bucket_rack":
        L, D, H = 0.91, 0.30, 1.00
        for sx in (-1, 1):
            for sz in (-1, 1):
                vis.append(W(sx * L / 2 - 0.03, sx * L / 2 + 0.03, -0.15, H, sz * D / 2 - 0.03, sz * D / 2 + 0.03, WOOD,
                             vis=(1, 2)))
                cols.append(col(sx * L / 2 - 0.03, sx * L / 2 + 0.03, 0.0, 0.70, sz * D / 2 - 0.03, sz * D / 2 + 0.03,
                                WOOD))
        vis.append(W(-L / 2 - 0.03, L / 2 + 0.03, 0.70, 0.73, -D / 2 - 0.03, D / 2 + 0.03, WOOD, vis=(1, 2)))
        cols.append(col(-L / 2 - 0.03, L / 2 + 0.03, 0.70, 0.73, -D / 2 - 0.03, D / 2 + 0.03, WOOD))
        vis.append(W(-L / 2 - 0.03, L / 2 + 0.03, H - 0.04, H, -0.02, 0.02, WOOD, vis=(1,)))
        for i, x in enumerate((-0.22, 0.20)):
            tk = teoke(wear="_w2", vis=(1,), lod2=False, fill=0.04 if i % 2 == 0 else None, under=(i % 2 == 1))
            if i % 2 == 1:
                tk = xfs(tk, rx=180.0, t=(0.0, 0.45, 0.0))      # upside down to drain
            vis += xfs(tk, t=(x, 0.73, 0.0))
        for x in (0.05,):
            from props_shrine import ladle
            lad = ladle(wear="_w2")
            vis += xfs(lad, rz=-80.0, t=(x, H - 0.06, D / 2 + 0.05))
        P.dim("rack_h", 1.0, H, tol=0.001)
        P.notes.append("by the graveyard well or water point; one per graveyard")
    elif kind == "ab_fallen":
        # slats grey and split, half fallen; the flower tubes knocked over and empty
        s0 = sotoba(1.05, wear="_w2", text=False)
        vis += xfs(s0, rx=-22.0, rz=8.0, t=(-0.15, 0.0, 0.0))
        for i, (at, ry_) in enumerate((((0.10, 0.35), 20.0), ((-0.05, 0.55), -35.0))):
            s1 = sotoba(1.20 - 0.15 * i, wear="_w2", text=(i == 0))
            vis += lay(s1, rx=-90.0, ry=ry_, at=at, lift=0.0)
        # a slat broken in two
        bro = sotoba(0.90, notched=True, wear="_w2", text=False)
        vis += lay(bro, rx=-90.0, rz=0.0, ry=75.0, at=(0.40, 0.10), lift=0.0)
        tb = lathe([(0.03, 0.0), (0.03, 0.30), (0.024, 0.30), (0.024, 0.04), (0.0, 0.04)], 6, BAMBOO, vis=(1,))
        tb.wear = "_w2"
        vis += lay([tb], rz=90.0, ry=40.0, at=(-0.30, 0.40), lift=0.0)
        vis.append(litter(9, 0.0, 0.3, 0.6, sx=1.4))
        P.dim("sotoba_h", 1.05, 1.05, tol=0.001)
    elif kind == "bohyo":
        m = lathe([(0.0, -0.03), (0.50, -0.03), (0.40, 0.05), (0.20, 0.10), (0.0, 0.11)], 8, EARTH, vis=(1, 2))
        m.verts = [(v[0], v[1], v[2] * 1.4) for v in m.verts]
        m.fm = None
        m.fn = None
        m.vn = None
        m.finalize()
        m.wear = "_w1"
        vis.append(litter(13, 0.0, 0.0, 0.45, sx=0.9, sz=1.3))
        vis[-1] = xf(vis[-1], t=(0.0, 0.11, 0.0))
        vis.append(m)
        a = 0.09
        z0 = -0.62
        # M1: a silver-grey post (a few years old) with a faded posthumous name and its year
        post, pc = bohyo_post(a, 0.86, z0, SILVER, "_w1", 0.06, ink="_w2", cell="bohyo_chiko_shinnyo_kyoho12")
        g = K.tilt(post + [pc], rx=-5.0, rz=4.0, pivot=(0.0, 0.0, z0))
        vis += [q for q in g if q.vis]
        cols += [q for q in g if not q.vis]
        vis += K.pebbles(12, 0.05, 0.05, 0.3, n=3)
        P.dim("post_h", 0.86, 0.86, tol=0.001)
        P.notes.append("the poor grave: an earth mound with a wooden post (any fresh grave before its stone)")
    # ---- W3 (2026-09-30): bohyo variety (W2_ERA W4 / W5): sizes, wood ages, lean, split, rotted away
    elif kind in ("bohyo_new", "bohyo_s", "bohyo_roof", "ab_bohyo_lean", "ab_bohyo_split", "ab_bohyo_rotted"):
        # M1: the new post in pale NEW wood with crisp ink, older ones silver-grey (jp_m_wood_silver) with fading ink;
        # each carries a posthumous name (jp_m_decal_sumi_text_grave): name on the front, year on the side
        spec = {  # a, h, z0, wood, wear, tip, text crop (None = whole), tilt rx / rz, sink, mound (r, h, sz, sunk)
            "bohyo_new": (0.105, 1.15, -0.70, NEWWOOD, "_w0", 0.07, None, -1.0, 0.5, 0.0, (0.55, 0.17, 1.4, False)),
            "bohyo_s": (0.06, 0.52, -0.40, SILVER, "_w1", 0.04, None, -3.0, -5.0, 0.0,
                        (0.32, 0.08, 1.35, False)),
            "bohyo_roof": (0.10, 1.00, -0.62, SILVER, "_w0", 0.0, None, -2.0, 2.0, 0.0, (0.50, 0.11, 1.4, False)),
            "ab_bohyo_lean": (0.09, 0.85, -0.60, SILVER, "_w2", 0.06, None, 9.0, -17.0, 0.05,
                              (0.48, 0.07, 1.4, False)),
        }
        names = {"bohyo_new": ("bohyo_jonen_shinji_kyoho15", "_w0"), "bohyo_s": ("bohyo_shungaku_doji_kyoho14", "_w2"),
                 "bohyo_roof": ("bohyo_soshin_shinji_kyoho13", "_w1"),
                 "ab_bohyo_lean": ("bohyo_dosen_zenjomon_kyoho9", "_w2")}
        if kind in spec:
            a, h, z0, mat, wr, tip, crop, rx, rz, sink, (mr, mh, msz, sunk) = spec[kind]
            vis += bohyo_mound(13 + len(kind), mr, mh, msz, sunk, wear="_w0" if wr == "_w0" else "_w1")
            th = None
            if crop:
                th = min(0.40, (h - tip - 0.12) * 0.62) * (crop[3] - crop[1]) * (1.6 if kind == "bohyo_s" else 1.0)
            post, pc = bohyo_post(a, h, z0, mat, wr, tip, th=th, crop=crop, cap=(kind == "bohyo_roof"),
                                  ink=names[kind][1], cell=names[kind][0])
            g = K.tilt(post + [pc], rx=rx, rz=rz, pivot=(0.0, 0.0, z0), sink=sink)
            vis += [q for q in g if q.vis]
            cols += [q for q in g if not q.vis]
            if kind != "bohyo_new":
                vis += K.pebbles(len(kind), 0.05, z0 * 0.1, 0.25, n=3)
            P.dim("post_h", h, h, tol=0.001)
            P.notes.append({"bohyo_new": "a fresh grave: new wood, fresh ink, a high new mound",
                            "bohyo_s": "a small post (a child's grave), silver-grey, the child's name faded",
                            "bohyo_roof": "the kasa-toba form: a small two-board gabled cap keeps rain off the ink "
                                          "(uncommon, about 1 post in 8; W2_ERA W5)",
                            "ab_bohyo_lean": "grey post leaning hard back and aside, the mound slumped, the name "
                                             "a ghost"}[kind])
        elif kind == "ab_bohyo_split":
            # black and rotting; the top 40 cm split in two halves that splay apart; the pointed tip is gone
            a, z0 = 0.10, -0.60
            vis += bohyo_mound(31, 0.48, 0.08, 1.4, False, wear="_w2")
            post = [W(-a / 2, a / 2, -0.20, 0.40, z0 - a / 2, z0 + a / 2, SOOT, vis=(1, 2))]
            for sx, ang, top in ((-1, 4.0, 0.80), (1, -6.5, 0.71)):
                half = W(min(0, sx) * a / 2 + (0.004 if sx > 0 else 0), max(0, sx) * a / 2 - (0.004 if sx < 0 else 0),
                         0.40, top, z0 - a / 2, z0 + a / 2, SOOT, vis=(1, 2))
                post.append(xf(half, rz=ang, pivot=(sx * 0.004, 0.40, z0)))
            for s in post:
                s.wear = "_w2"
            pc = col(-a / 2, a / 2, 0.0, 0.78, z0 - a / 2, z0 + a / 2, SOOT)
            g = K.tilt(post + [pc], rx=-4.0, rz=3.0, pivot=(0.0, 0.0, z0))
            vis += [q for q in g if q.vis]
            cols += [q for q in g if not q.vis]
            vis += K.pebbles(41, 0.05, 0.0, 0.25, n=3)
            P.dim("post_h", 0.80, 0.80, tol=0.001)
            P.notes.append("black, rotting post split down its top half; ink long gone")
        else:  # ab_bohyo_rotted
            # a sunken mound; the post rotted off at the ground: a black stump, its broken top lying on the mound
            a, z0 = 0.09, -0.60
            vis += bohyo_mound(57, 0.50, 0.09, 1.4, True, wear="_w2", litter_r=0.28)
            st = [W(-a / 2, a / 2, -0.20, 0.10, z0 - a / 2, z0 + a / 2, SOOT, vis=(1, 2))]
            for (x0, x1, z_0, z_1, hh) in ((-a / 2, -0.01, z0 - a / 2, z0 + 0.01, 0.17), (0.0, a / 2, z0 - a / 2, z0,
                                                                                         0.14),
                                           (-0.02, a / 2, z0 + 0.005, z0 + a / 2, 0.12)):
                st.append(W(x0, x1, 0.10, hh, z_0, z_1, SOOT, vis=(1,)))
            frag = [W(-a / 2, a / 2, 0.0, 0.42, -a / 2, a / 2, SOOT, vis=(1, 2)),
                    core.Solid([(-a / 2, 0.42, -a / 2), (a / 2, 0.42, -a / 2), (a / 2, 0.42, a / 2), (-a / 2, 0.42, a / 2),
                                (0.0, 0.48, 0.0)], [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]], SOOT,
                               vis=(1,))]
            for s in st + frag:
                s.wear = "_w2"
            vis += K.tilt(st, rx=-3.0, rz=5.0, pivot=(0.0, 0.0, z0))
            vis += lay(frag, rx=-90.0, ry=-28.0, at=(0.10, -0.15), lift=0.012)
            vis.append(leaves(61, 0.0, 0.05, 0.20, 0.03, wear="_w2"))
            P.dim("stump_h", 0.17, 0.17, tol=0.001)
            P.notes.append("the post rotted away: a stump and its fallen top on a sunken mound (walk-over, no "
                           "collision)")
    else:
        raise KeyError(kind)
    add_all(P, vis + cols)
    lo = min(v[1] for s in P.solids if s.vis for v in s.verts)
    P.bury = max(P.bury, -lo + 0.001)
    return P


# ================================================================================================ registry
def G(sfx, display, state="intact"):
    return M("jp_s_grave_stones_" + sfx, sfx.replace("ab_", ""), state, display, lambda: grave(sfx), mount="graveyard")


def GW(sfx, display, state="intact"):
    return M("jp_s_grave_wood_" + sfx, sfx.replace("ab_", ""), state, display, lambda: grave_wood(sfx),
             mount="graveyard")


AB = "abandoned"
PROPS = [
    {"id": "jp_s_grave_stones", "cat": "grave", "mount": "graveyard", "per_row": 8,
     "notes": ["1730 mix for the placement agent (W2_ERA): board 30 %, boat-halo 25 %, round 12 %, field stones / "
               "mounds 15 %, child Jizo 5 %, square pillar 5 %, gorinto / hokyointo 8 %",
               "irregular rows: 0.9 m plot grid jittered +-0.15 m and +-12 deg, mixed heights, gaps",
               "inscriptions (M1): a posthumous name and date per stone from jp_m_decal_carved_text_grave (1670-1729: "
               "-shinji / -shinnyo, -zenjomon / -zenjoni, -doji, shaku-, kigen / enjaku prefixes) + B1's two; no "
               "family-name stones (Meiji); gorinto / hokyointo stay blank (no Siddham font for the seed syllables)", "abandoned share: about 1 stone in 4 leaning / sunk / broken"],
     "models": [
         G("board", "Board-shaped gravestone (itabi) on a base, name and date"),
         G("board_s", "Small board-shaped gravestone set in the ground, name only"),
         G("board_tall_moss", "Tall board-shaped gravestone on two bases, mossy"),
         G("boat_halo", "Boat-halo gravestone with a Jizo in relief"),
         G("boat_halo_child", "Small boat-halo stone (a child's grave), the child's name"),
         G("round", "Round-headed gravestone (kushigata) on a base"),
         G("round_s_plain", "Small round-headed stone, plain"),
         G("pillar", "Square-pillar gravestone on three bases (rare in 1730)"),
         G("pillar_pointed", "Square pillar with a pointed top (new Kyoho fashion, rare)"),
         G("gorinto_s", "Five-ring stupa (gorinto), 0.6"),
         G("gorinto_l", "Large five-ring stupa on a platform, 2.0 (samurai / priest)"),
         G("gorinto_stack", "Gorinto re-stacked from two stupas, crescent missing"),
         G("gorinto_heap", "A small heap of old gorinto fragments at a plot corner"),
         G("hokyointo", "Hokyointo (treasure-seal stupa), 1.5"),
         G("jizo_child", "Small Jizo on a base (a child's grave), faded bib"),
         G("field", "Field stone as a grave marker (poor grave)"),
         G("field_mound", "Earth grave mound with a field stone at its head"),
         G("field_pair", "Two small field stones (a couple's poor grave)"),
         G("ab_leaning", "Board-shaped gravestone leaning and sunk", AB),
         G("ab_board_broken", "Board-shaped gravestone, gable snapped off and lying in front", AB),
         G("ab_boat_halo_sunk", "Boat-halo gravestone leaning forward, half sunk, mossy", AB),
         G("ab_round_lean", "Round-headed gravestone leaning sideways", AB),
         G("ab_gorinto_fallen", "Gorinto with roof, crescent and jewel fallen (quake)", AB),
         G("ab_hokyointo_broken", "Hokyointo, finial and one horn fallen", AB),
     ]},
    {"id": "jp_s_grave_wood", "cat": "grave", "mount": "graveyard", "per_row": 7,
     "notes": ["slats behind about 1 grave in 3; one rack and one bucket rack per graveyard by its water point",
               "_bohyo (wooden post on an earth mound) = the poor grave / a fresh grave (W2_ERA W3)",
               "bohyo mix (W3, W2_ERA W4/W5): grey _bohyo / _bohyo_s commonest, _bohyo_new for fresh graves, "
               "_bohyo_roof about 1 in 8, abandoned lean / split / rotted about 1 in 3"],
     "models": [
         GW("sotoba_x3", "Three sotoba slats behind a stone"),
         GW("rack", "Sotoba rack with leaning slats"),
         GW("tubes", "Bamboo flower tubes in a stone, dead stems"),
         GW("incense", "Stone incense stand with ash"),
         GW("bucket_rack", "Bucket and ladle rack (teoke-kake)"),
         GW("bohyo", "Wooden grave post on an earth mound"),
         GW("bohyo_new", "Fresh wooden grave post, tall, on a new high mound"),
         GW("bohyo_s", "Small silver-grey grave post (child or very poor grave)"),
         GW("bohyo_roof", "Wooden grave post with a small gabled cap (kasa-toba)"),
         GW("ab_fallen", "Sotoba slats fallen and split, flower tube knocked over", AB),
         GW("ab_bohyo_lean", "Grey grave post leaning hard, mound slumped", AB),
         GW("ab_bohyo_split", "Black rotting grave post, top split apart", AB),
         GW("ab_bohyo_rotted", "Sunken grave mound, post rotted to a stump", AB),
     ]},
]
