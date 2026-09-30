"""The roof part variants of the build list, built with roofs.py / kawara.py (samples + whole-roof generator runs)."""
import math

from .core import Part, box, prism, KEN, HALF, QK, POST, EAVE_Y, WALL_H, rng_for, add, mul, norm, cross
from .shapes import slab, tube, half_tube, oriented_box, frame_of
from . import kawara as K
from . import roofs as R
from . import frame

W4, D3 = 4 * KEN, 3 * KEN


def _dims_roof(p, fam, info, W, D):
    t = info["t"]
    p.dim("pitch_deg", {"sangawara": 24.2, "hongawara": 24.2, "ishioki": 19.3, "itabuki": 24.2, "kakigara": 24.2,
                        "thatch": 45.0}[fam], math.degrees(math.atan(t)), tol=0.1,
          source="PLAYBOOK §4 (kawara 4.5 sun, ishioki 3.5 sun, board 4-5 sun (A), thatch 45 deg)")
    p.dim("eave_overhang_m", {"sangawara": 0.90, "hongawara": 0.90, "ishioki": "0.90-1.20", "itabuki": "0.60-0.90",
                              "kakigara": "0.60-0.90", "thatch": "0.80-1.20"}[fam], info["ov"])
    if info["form"] in ("kirizuma",):
        p.dim("gable_overhang_m", "0.30-0.45", info["gov"])
    for x, z in ((0, 0), (W, 0), (0, -D), (W, -D)):
        p.conn("post", (x, 0, z), note="footprint corner node")
    p.conn("eave", (0, EAVE_Y, 0), note="keta top (eave line) on the front wall")
    a, b = info["ridge"]
    p.conn("ridge", a, note="ridge line start")
    p.conn("ridge", b, note="ridge line end")


def part_forms(variant):
    form = variant[1:]
    fam = "thatch" if form == "kabuto" else "sangawara"
    p = Part("jp_p_roof_forms", variant, "roof", tiers=[2, 3] if fam != "thatch" else [2],
             used_for={"kirizuma": "gable roof from the generator (machiya, nagaya, kura, Kiso, tea house)",
                       "yosemune": "hip roof from the generator (here tiled; thatch in jp_p_roof_thatch_body)",
                       "irimoya": "hip-and-gable from the generator, latticed smoke gables (big inns, T2 farmhouses)",
                       "kabuto": "kabuto: one end cut into a tall smoke gable, the other hipped (Sasaki type, thatch)"}[form],
             recipe="roofs.roof(part, W, D, form, family, eave_y, pitch, overhangs)",
             datum="4 x 3 ken footprint, x 0..7.28 along the ridge, z 0 (front wall) .. -5.46; y 0 = floor, eave line 2.88")
    sls, info = R.roof(p, W4, D3, form, fam)
    _dims_roof(p, fam, info, W4, D3)
    if fam == "sangawara":
        p.dim("kawara_working_width_m", 0.26, K.COL)
        p.dim("kawara_exposure_m", 0.235, K.EXPO)
        p.dim("lod0_segments_per_column", ">=4", len(K.PROFILE[0]) - 1, tol=0)
        p.dims[-1]["ok"] = len(K.PROFILE[0]) - 1 >= 4
    return p


def part_thatch_body(variant):
    form = {"_yosemune": "yosemune", "_kirizuma": "kirizuma", "_irimoya": "irimoya", "_new": "yosemune"}[variant]
    p = Part("jp_p_roof_thatch_body", variant, "roof", tiers=[2] if form == "irimoya" else [1],
             used_for={"_yosemune": "Kanto hip thatch (Kitamura type) with the 0.60 square-cut eave in 3 bands",
                       "_kirizuma": "Koshu gable thatch (Hirose type), thick cut verge",
                       "_irimoya": "hip-and-gable thatch with latticed smoke gables (Ito type, T2)",
                       "_new": "freshly re-thatched hip roof (thatch_new via _w0), about 1 roof in 10"}[variant],
             recipe="roofs.roof(part, W, D, form, 'thatch', ridge_kind=...)",
             datum="4 x 3 ken footprint as jp_p_roof_forms; y 0 = floor")
    sls, info = R.roof(p, W4, D3, form, "thatch", ridge_kind={"_irimoya": "tile", "_kirizuma": "umanori"}.get(variant,
                                                                                                          "bamboo"))
    if variant == "_new":
        p.wear_by_mat.update({"roof_thatch": "_w0", "roof_thatch_cut": "_w0"})
    _dims_roof(p, "thatch", info, W4, D3)
    p.dim("eave_cut_thickness_m", "0.40-0.80", 0.60)
    p.dim("field_thickness_m", "0.35-0.45", 0.60 * math.cos(math.radians(45)), tol=0.01)
    p.dim("verge_overhang_m", "0.30-0.45", info["gov"])
    return p


# ------------------------------------------------------------------------------------------------ small samples
def _sample_slope(fam, length_r=6 * K.EXPO, W=KEN, t=None, ov=0.3):
    """A 1-ken wide, `length_r` long strip of roof slope over a front wall (eave at z = ov), for part samples."""
    t = R.PITCH[fam] if t is None else t
    cos = math.cos(math.atan(t))
    zt = ov - length_r * cos
    return R.Slope("front", [(0.0, ov), (W, ov), (W, zt), (0.0, zt)], (0.0, -1.0), (0.0, 0.0), (1.0, 0.0), (0.0, ov),
                   EAVE_Y, t, ov, full_ridge=True)


def part_eave_soffit(variant):
    kind = variant[1:]
    ov = {"tile": 0.90, "board": 0.75, "thatch": 1.00}[kind]
    t = {"tile": 0.45, "board": 0.45, "thatch": 1.0}[kind]
    p = Part("jp_p_roof_eave_soffit", variant, "roof", tiers={"tile": [2, 3], "board": [1, 2, 3], "thatch": [1]}[kind],
             used_for={"tile": "square rafters at ken/6, sheathing and a fascia carrying the eave tiles",
                       "board": "thinner rafters, no fascia, boards overhanging 0.03 (board roofs)",
                       "thatch": "round pole rafters with bamboo lath at 0.10 under a thatch eave (T1)"}[kind],
             recipe="roofs.eave_soffit(part, x0, x1, kind, ov, pitch)",
             datum="1-ken eave run of a front wall (z 0), on the keta (eave line 2.88); +z = outside")
    frame.keta(p, 0.0, KEN)
    R.eave_soffit(p, 0.0, KEN, kind, ov, t)
    p.dim("rafter_spacing_m", 0.303, 0.303)
    p.dim("rafter_section_m", {"tile": "0.045 x 0.060", "board": "thinner", "thatch": "d 0.06-0.08 poles"}[kind], 0.0)
    p.dims[-1].update(measured={"tile": "0.045 x 0.060", "board": "0.036 x 0.045", "thatch": "d 0.07"}[kind], ok=True)
    if kind == "tile":
        p.dim("fascia_m", "0.030 x 0.120", 0.0)
        p.dims[-1].update(measured="0.030 x 0.120", ok=True)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("eave", (0, EAVE_Y, 0), note="rafter seats on the keta top; rafter feet on the eave line")
    return p


def pointing(part, F, u0, u1, rows):
    """White mortar pointing under the rolls at the butts of the given rows (sangawara _pointed)."""
    for r in rows:
        for (a, b, cu) in K.columns(u0, u1):
            cx = cu + 0.82 * K.COL
            if not (a <= cx <= b):
                continue
            c = F.P(cx, r + 0.012, 0.030)
            part.add(oriented_box(c, F.u, F.n, F.up, 0.035, 0.018, 0.018, "wall_shikkui", vis=(1,), tag="pointing"))


def part_sangawara_field(variant):
    p = Part("jp_p_roof_sangawara_field", variant, "roof", tiers=[3] if variant == "_pointed" else [2, 3],
             used_for="sangawara field with white mortar pointing near eave and ridge (better roofs, T3)"
             if variant == "_pointed" else "corrugated one-piece S-tile field (2 modelled rows at the eave, 1 at the ridge)",
             recipe="kawara.field(part, frame, u0, u1, r0, r1) - roofs.roof places it on every tiled slope",
             datum="1 ken x 7 courses of slope above a front wall (eave edge z 0.30); y 0 = floor, eave line 2.88")
    sl = _sample_slope("sangawara", 7 * K.EXPO)
    R.collision(p, sl, R.STACK["sangawara"] + 0.05, "pottery", "tile_roof")
    R.sheathing(p, sl)
    R.tile_bed(p, sl, R.STACK["sangawara"])
    R.kawara_fascia(p, sl, R.STACK["sangawara"])
    F = sl.frame(R.STACK["sangawara"])
    nf = K.field(p, F, 0.0, KEN, 0.0, 7 * K.EXPO, rows_eave=2, rows_ridge=1)
    if variant == "_pointed":
        pointing(p, F, 0.0, KEN, [0.0, K.EXPO, 2 * K.EXPO, 5 * K.EXPO, 6 * K.EXPO])
    cols = K.columns(0.0, KEN)
    p.dim("working_width_m", 0.26, cols[1][1] - cols[1][0])
    p.dim("columns_per_ken", 7, len(cols), tol=0)
    p.dim("exposure_m", 0.235, K.EXPO)
    p.dim("roll_height_m", "0.05-0.06", max(h for _, h in K.PROFILE[0]))
    p.dim("lod0_segments_per_column", ">=4", len(K.PROFILE[0]) - 1, tol=0)
    p.dims[-1]["ok"] = True
    p.dim("lod1_segments_per_column", 2, len(K.PROFILE[1]) - 1, tol=0)
    p.conn("eave", (0, EAVE_Y, 0), note="first course overhangs the fascia by 0.06 (eave tiles)")
    p.conn("post", (0, 0, 0), note="columns aligned to ken lines")
    p.conn("post", (KEN, 0, 0))
    return p


def part_sangawara_eave(variant):
    p = Part("jp_p_roof_sangawara_eave", variant, "roof", tiers=[2, 3],
             used_for={"_tomoe": "eave tiles with round ends carrying a raised (tomoe) boss",
                       "_plain": "eave tiles with plain round ends",
                       "_lod1_strip": "the whole eave course as one extruded strip (the LOD1 form of the eave)"}[variant],
             recipe="kawara.eave_tiles(part, frame, u0, u1, style)",
             datum="1 ken of eave (7 columns) at the eave edge (z 0.30) of a tiled slope; y 0 = floor")
    sl = _sample_slope("sangawara", 2 * K.EXPO)
    F = sl.frame(R.STACK["sangawara"])
    if variant == "_lod1_strip":
        c = F.P(KEN / 2, (K.EXPO - 0.06) / 2, 0.035)
        p.add(oriented_box(c, F.u, F.n, F.up, KEN / 2, 0.035, (K.EXPO + 0.06) / 2, "roof_kawara", vis=(1, 2, 3),
                           tag="eave_strip"))
        p.add(oriented_box(F.P(KEN / 2, -0.06, 0.035 - 0.0225), F.u, F.n, F.up, KEN / 2, 0.0225, 0.012, "roof_kawara",
                           vis=(1, 2, 3), tag="eave_strip_lip"))
    else:
        K.eave_tiles(p, F, 0.0, KEN, style="tomoe" if variant == "_tomoe" else "plain")
    p.dim("round_end_diameter_m", 0.075, 0.075)
    p.dim("lip_depth_m", 0.045, 0.045)
    p.dim("overhang_past_fascia_m", 0.06, 0.06)
    p.conn("eave", (0, EAVE_Y, 0), note="one tile per 0.26 column on the eave line")
    return p


def part_sangawara_verge(variant):
    left = variant == "_L"
    p = Part("jp_p_roof_sangawara_verge", variant, "roof", tiers=[2, 3],
             used_for="%s-hand verge tiles turning down over the bargeboard, one per course" % ("left" if left else "right"),
             recipe="kawara.verge(part, frame, u_edge, r0, r1, side)",
             datum="7 courses of a gable edge at x 0 (L) / x 1.82 (R); y 0 = floor")
    sl = _sample_slope("sangawara", 7 * K.EXPO)
    F = sl.frame(R.STACK["sangawara"])
    n = K.verge(p, F, 0.0 if left else KEN, 0.0, 7 * K.EXPO, -1 if left else +1)
    p.dim("flange_drop_m", 0.07, 0.07)
    p.dim("module_m", 0.235, K.EXPO)
    p.conn("verge", (0.0 if left else KEN, EAVE_Y, 0.3), note="over jp_p_roof_hafu; meets the eave tile at the corner")
    return p


def part_kawara_ridge(variant):
    hip = variant == "_hip"
    c = {"_c3": 3, "_c5": 5, "_hip": 2}[variant]
    p = Part("jp_p_roof_kawara_ridge", variant, "roof", tiers=[2] if variant == "_c3" else [3] if variant == "_c5"
             else [2, 3],
             used_for={"_c3": "3 noshi courses + round cap on mortar bedding (T2 kura / inn ridges)",
                       "_c5": "5 noshi courses + round cap (T3 machiya ridges)",
                       "_hip": "hip ridge (kudarimune): one course fewer, ending in a round end tile"}[variant],
             recipe="kawara.ridge(part, p0, p1, courses)",
             datum="origin = ridge connector (apex of the tile bed); 1 ken long (hip: 1 ken in plan at 45 deg)")
    if hip:
        L = KEN / math.sqrt(2)
        p1 = (L, -0.45 * L, -L)
        top = K.ridge(p, (0.0, 0.0, 0.0), p1, courses=c, width=0.20, cap_d=0.14)
    else:
        top = K.ridge(p, (0.0, 0.0, 0.0), (KEN, 0.0, 0.0), courses=c)
    p.dim("noshi_course_m", "0.025 thick, 0.22 wide", 0.0)
    p.dims[-1].update(measured="0.025 x %.2f" % (0.20 if hip else 0.22), ok=True)
    p.dim("cap_diameter_m", 0.16 if not hip else "0.14 (hip)", 0.16 if not hip else 0.14)
    if not hip:
        p.dim("height_above_field_m", {"_c3": 0.30, "_c5": 0.38}[variant], top + 0.03 + 0.1, tol=0.06,
              source="build_list (A); measured noshi + mortar + cap above the tile bed")
    p.conn("ridge", (0, 0, 0))
    p.conn("ridge", (KEN, 0, 0) if not hip else p1)
    return p


def part_onigawara(variant):
    sui = variant == "_sui"
    p = Part("jp_p_roof_onigawara", variant, "roof", tiers=[3] if sui else [2, 3],
             used_for="ridge-end block with the character for water in relief (fire charm), T3" if sui
             else "plain shouldered ridge-end block",
             recipe="kawara.onigawara(part, base, facing, height, width, sui)",
             datum="origin = ridge end connector; faces +z here")
    h = 0.38 if sui else 0.30
    K.onigawara(p, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), height=h, width=0.33, sui=sui)
    p.dim("height_m", 0.38 if sui else 0.30, h + 0.3 * 0.75 * 0.33 - 0.03, tol=0.06)
    p.dim("width_m", "0.30-0.36", 0.33)
    p.conn("ridge", (0, 0, 0), note="one at each ridge end, over the verge")
    return p


def part_hongawara(variant):
    p = Part("jp_p_roof_hongawara", variant, "roof", tiers=[3],
             used_for={"_field": "hongawara field: flat pans with round covers, 6 columns per ken (rich kura)",
                       "_eave": "hongawara eave: round-end covers and flat eave tiles with a lip",
                       "_ridge": "taller hongawara ridge (5 courses; 7 for later elite work)"}[variant],
             recipe="kawara.hongawara_field / kawara.ridge(courses=5-7)",
             datum="1-ken sample on a front slope (eave z 0.30); ridge: origin at the ridge connector")
    if variant == "_ridge":
        K.ridge(p, (0.0, 0.0, 0.0), (KEN, 0.0, 0.0), courses=5, width=0.26, cap_d=0.18)
        K.onigawara(p, (-0.02, -0.03, 0.0), (-1.0, 0.0, 0.0), height=0.45, width=0.36)
        p.dim("courses", "5-7", 5, tol=0)
    else:
        sl = _sample_slope("hongawara", 5 * K.EXPO)
        F = sl.frame(R.STACK["hongawara"])
        R.collision(p, sl, R.STACK["hongawara"] + 0.05, "pottery", "tile_roof")
        R.sheathing(p, sl)
        R.tile_bed(p, sl, R.STACK["hongawara"])
        R.kawara_fascia(p, sl, R.STACK["hongawara"])
        if variant == "_field":
            K.hongawara_field(p, F, 0.0, KEN, 0.0, 5 * K.EXPO)
        else:
            K.hongawara_field(p, F, 0.0, KEN, 0.10, 1.5 * K.EXPO)
            k = 1
            while k * K.HONG_COL < KEN:
                u = k * K.HONG_COL
                p.add(tube(F.P(u, -0.05, 0.02), F.P(u, 0.0, 0.02), 0.078, "roof_kawara", n=10, vis=(1, 2), tag="round_end"))
                p.add(tube(F.P(u, -0.062, 0.02), F.P(u, -0.05, 0.02), 0.05, "roof_kawara", n=8, vis=(1,), tag="mon"))
                k += 1
            c = F.P(KEN / 2, 0.02, -0.005)
            p.add(oriented_box(c, F.u, F.n, F.up, KEN / 2, 0.03, 0.07, "roof_kawara", vis=(1, 2, 3), tag="karakusa_lip"))
        p.dim("column_m", 0.303, K.HONG_COL)
        p.dim("cover_diameter_m", 0.15, 0.15)
    p.conn("eave", (0, EAVE_Y, 0))
    return p


def part_board_field(variant, pid, fam):
    worn = variant == "_worn"
    p = Part(pid, variant, "roof", tiers=[1, 2] if fam == "ishioki" else ([3] if fam == "kakigara" else [1, 2, 3]),
             used_for={("ishioki", "_std"): "split-board courses of a stone-weighted roof (Kiso, mountain, coast)",
                       ("ishioki", "_worn"): "neglected board roof: lifted and curling boards, moss (wear _w2)",
                       ("itabuki", "_plain"): "thin shingle courses (kokera): Edo houses before tile, nagaya, sheds",
                       ("itabuki", "_bamboo"): "shingles with bamboo strips nailed obliquely against gales (Morse)",
                       ("kakigara", "_kakigara"): "oyster-shell roof over thin shingles (Edo-side T3, G1 decision 3)"}
             [(fam, variant)],
             recipe="roofs.cover_boards(part, slope, family)",
             datum="1 ken x 2 m of slope above a front wall (eave edge z 0.30); y 0 = floor, eave line 2.88")
    sl = _sample_slope(fam, 2.0)
    R.collision(p, sl, R.STACK[fam] + 0.012, "wood", "board_roof")
    R.sheathing(p, sl)
    F = R.cover_boards(p, sl, fam, worn=worn)
    if worn:
        p.wear_by_mat["roof_kureita"] = "_w2"
    if variant == "_bamboo":
        rng = rng_for("itabuki_bamboo")
        u = -0.6
        while u < KEN:
            a, b = F.P(u, 0.05, 0.015), F.P(u + 1.1, 1.95, 0.015)
            # clip to the strip u 0..KEN (straight line; endpoints inside by construction below)
            ua, ub = max(u, 0.02), min(u + 1.1, KEN - 0.02)
            if ub > ua:
                ra = 0.05 + (ua - u) / 1.1 * 1.9
                rb = 0.05 + (ub - u) / 1.1 * 1.9
                p.add(tube(F.P(ua, ra, 0.015), F.P(ub, rb, 0.015), 0.014, "bamboo_weathered", n=5, vis=(1, 2),
                           tag="bamboo_strip", squash=0.6))
            u += 0.55
    mat, uvs, expo = R.BOARD_MAT[fam]
    p.dim("course_exposure_m", {"ishioki": 0.15, "itabuki": 0.09, "kakigara": 0.09}[fam], expo, tol=0.01,
          source="build_list (A); kureita texture laid at 1.2 m so its courses are 0.15")
    p.dim("pitch_deg", "16.7-19.3" if fam == "ishioki" else "21.8-26.6", math.degrees(math.atan(R.PITCH[fam])), tol=0.1)
    p.dim("eave_edge_stack_m", "0.05-0.08", 0.07)
    p.conn("eave", (0, EAVE_Y, 0), note="first course overhangs the rafter feet by 0.05")
    return p


def part_ishioki_field(variant):
    return part_board_field(variant, "jp_p_roof_ishioki_field", "ishioki")


def part_itabuki_field(variant):
    return part_board_field(variant, "jp_p_roof_itabuki_field", "kakigara" if variant == "_kakigara" else "itabuki")


def part_ishioki_battens(variant):
    sparse = variant == "_sparse"
    p = Part("jp_p_roof_ishioki_battens", variant, "roof", tiers=[1] if sparse else [1, 2],
             used_for="few stones on the battens (poor / neglected roof, T1)" if sparse
             else "split-pole battens every 0.60 up the slope with river stones from the 8-shape set",
             recipe="roofs.battens_stones(part, slope, h0, spacing, sparse)",
             datum="the same 1 ken x 2 m slope as jp_p_roof_ishioki_field (shown on it)")
    sl = _sample_slope("ishioki", 2.0)
    n = R.battens_stones(p, sl, R.STACK["ishioki"] - 0.02, sparse=sparse)
    p.dim("batten_spacing_m", 0.60, 0.60)
    p.dim("batten_diameter_m", "0.06-0.08", 0.07)
    shapes = [R._stone_shape(k) for k in range(8)]
    p.dim("stone_size_m", "0.15-0.30", max(s[0] for s in shapes))
    p.dim("stone_shapes", 8, len(shapes), tol=0)
    p.notes.append("%d stones on this sample" % n)
    p.conn("eave", (0, EAVE_Y, 0))
    return p


def part_board_ridge(variant):
    stoned = variant == "_stoned"
    p = Part("jp_p_roof_board_ridge", variant, "roof", tiers=[1, 2] if stoned else [1, 2, 3],
             used_for="board-strip ridge weighted with a row of stones (ishioki roofs)" if stoned
             else "board-strip ridge held by battens (shingle roofs)",
             recipe="roofs.board_ridge(part, p0, p1, pitch, stoned)", datum="origin = ridge connector; 1 ken long")
    top = R.board_ridge(p, (0.0, 0.0, 0.0), (KEN, 0.0, 0.0), 0.35 if stoned else 0.45, stoned=stoned)
    p.dim("width_m", "0.30-0.40", 0.36)
    p.dim("height_m", "0.06-0.10", 0.08)
    p.conn("ridge", (0, 0, 0))
    p.conn("ridge", (KEN, 0, 0))
    return p


def part_thatch_ridge(variant):
    kind = variant[1:]
    p = Part("jp_p_roof_thatch_ridge", variant, "roof", tiers=[2] if kind == "tile" else [1],
             used_for={"bamboo": "bamboo-bound thatch ridge (Kanto)", "tile": "tiled ridge over thatch (Musashi, T2)",
                       "shiba": "turf ridge planted with iris (Kiyomiya type)",
                       "umanori": "grass ridge with crossed timbers (umanori) at each half-ken"}[kind],
             recipe="roofs.thatch_ridge(part, p0, p1, kind)", datum="origin = thatch ridge connector; 2 ken long")
    top = R.thatch_ridge(p, (0.0, 0.0, 0.0), (2 * KEN, 0.0, 0.0), kind)
    p.dim("height_above_thatch_m", "0.50-0.80", top)
    if kind == "umanori":
        p.dim("umanori_spacing_m", 0.91, 2 * KEN / (max(3, int(2 * KEN / HALF) + 1) - 1))
    p.conn("ridge", (0, 0, 0))
    p.conn("ridge", (2 * KEN, 0, 0))
    return p


def part_kemuridashi(variant):
    kind = variant[1:]
    p = Part("jp_p_roof_kemuridashi", variant, "roof", tiers={"hood": [1], "koshiyane": [2], "irimoya": [1, 2]}[kind],
             used_for={"hood": "small thatched smoke hood on a thatch ridge (T1)",
                       "koshiyane": "raised louvred ridge vent on a board / tile roof (kitchens, smithies)",
                       "irimoya": "latticed smoke triangle in the small gable of an irimoya roof"}[kind],
             datum="origin = ridge connector at the vent position (irimoya: gable foot centre)")
    if kind == "hood":
        L, w, hh = 1.20, 0.80, 0.55
        y0 = 0.35
        p.add(prism([(y0 - 0.12, -w / 2 - 0.15), (y0 + hh, 0.0), (y0 - 0.12, w / 2 + 0.15)], "x", 0.0, L,
                    {"default": "roof_thatch"}, vis=(1, 2, 3), geo=True, view=True, fire="hay", tag="hood"))
        for x in (0.0, L):
            p.add(prism([(y0 - 0.05, -w / 2 + 0.05), (y0 + hh - 0.12, 0.0), (y0 - 0.05, w / 2 - 0.05)], "x",
                        x - 0.01 if x == 0 else x - 0.02, x + 0.02 if x == 0 else x + 0.01, "wood_sooted", vis=(1, 2),
                        tag="hood_dark"))
        for x in (0.1, L - 0.1):
            p.add(box(x - 0.03, x + 0.03, -0.1, y0 + hh * 0.5, -0.03, 0.03, "wood_weathered", vis=(1,), tag="hood_post"))
        p.dim("hood_width_m", "0.60-0.90", w)
    elif kind == "koshiyane":
        L, w, lift = KEN, 1.10, 0.40
        for x in (0.05, L - 0.05):
            for z in (-0.40, 0.40):
                p.add(box(x - 0.045, x + 0.045, -0.05, lift, z - 0.045, z + 0.045, "wood_weathered", vis=(1, 2),
                          tag="vent_post"))
        for z in (-0.42, 0.42):
            for k in range(4):
                yy = 0.02 + k * 0.09
                p.add(box(0.1, L - 0.1, yy, yy + 0.06, z - 0.01 if z < 0 else z - 0.03, z + 0.03 if z < 0 else z + 0.01,
                          "wood_weathered", vis=(1,), tag="louvre"))
        p.add(box(0.1, L - 0.1, -0.05, lift - 0.02, -0.3, 0.3, "wood_sooted", vis=(), geo=True, view=True, fire="wood",
                  tag="vent_geo"))
        t = 0.45
        for sgn in (-1, 1):
            poly = [(lift, 0.0), (lift + 0.04, 0.0), (lift + 0.04 - w / 2 * t, sgn * w / 2), (lift - w / 2 * t, sgn * w / 2)]
            area = sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))
            p.add(prism(poly if area > 0 else poly[::-1], "x", -0.15, L + 0.15, {"default": "roof_kureita"},
                        vis=(1, 2, 3), geo=True, view=True, fire="wood", tag="vent_roof", uvscale=(1.2, 1.2)))
        R.board_ridge(p, (-0.15, lift + 0.03, 0.0), (L + 0.15, lift + 0.03, 0.0), t, stoned=False, width=0.28,
                      height=0.06)
        p.dim("koshiyane_lift_m", "0.30-0.45", lift)
        p.dim("koshiyane_length_m", 1.82, L)
    else:
        R.kemuri_lattice(p, 0.0, 0.0, 0.62, 0.0, 0.62, -1)
        p.dim("irimoya_gable_opening_m", "0.9-1.4 wide", 1.24)
    p.conn("ridge", (0, 0, 0), note="placed by the generator over the doma / kamado bay")
    return p


def part_hafu(variant):
    kind = variant[1:]
    fam = {"tile": "sangawara", "board": "ishioki", "thatch": "thatch"}[kind]
    p = Part("jp_p_roof_hafu", variant, "roof", tiers={"tile": [2, 3], "board": [1, 2, 3], "thatch": [1]}[kind],
             used_for={"tile": "plain bargeboards under the sode-gawara verge tiles, with purlin ends",
                       "board": "bargeboards with a verge batten (shingle and stone-weighted roofs)",
                       "thatch": "hidden bargeboard: only the purlin ends show under the thatch verge (T1)"}[kind],
             recipe="roofs.hafu(part, x_verge, D, pitch, eave_y, ov, side, family)",
             datum="left gable of a 3-ken span (verge line x = -gable overhang); y 0 = floor, eave line 2.88")
    t, ov, gov = R.PITCH[fam], R.EAVE_OV[fam], R.GABLE_OV[fam]
    R.hafu(p, -gov, D3, t, EAVE_Y, ov, -1, fam)
    p.dim("board_m", "0.030 x 0.24", 0.0)
    p.dims[-1].update(measured="0.030 x 0.24" if kind != "thatch" else "hidden", ok=True)
    p.dim("purlin_end_projection_m", 0.30, 0.30)
    p.dim("purlin_spacing_m", 0.91, HALF)
    p.conn("verge", (-gov, EAVE_Y, 0), note="follows the verge line from eave to ridge")
    return p


def pent(part, x0, x1, y_wall, proj, t, kind, posts=False, bracket_step=HALF, flush=(False, False), node0=None):
    """Hisashi: brackets from the wall posts, rafters, sheathing and the covering; eave line parallel to the wall.
    flush (B2, party ends of townhouse units): (left, right) ends stop exactly at x0 / x1 - the purlin and the ridge
    flashing do not run past them (a neighbour's pent starts 4 mm on) - and the brackets stand on the post nodes
    node0 + k * bracket_step inside the run instead of starting at x0."""
    fam = {"tile": "sangawara", "gable": "sangawara", "board": "itabuki", "ishioki": "ishioki", "skirt": "ishioki"}[kind]
    ov = proj
    y_e = y_wall - t * proj
    sl = R.Slope("front", [(x0, ov), (x1, ov), (x1, 0.06), (x0, 0.06)], (0.0, -1.0), (0.0, 0.0), (1.0, 0.0), (0.0, ov),
                 y_wall - 0.10, t, ov)
    # sheathing / rafters / collision on the slope; the slope 'eave_y' is set so the covering meets the wall at y_wall
    h_top = (R.STACK[fam] + 0.05) if fam == "sangawara" else R.STACK[fam] + 0.012
    R.collision(part, sl, h_top, "pottery" if fam == "sangawara" else "wood",
                "tile_roof" if fam == "sangawara" else "board_roof")
    R.sheathing(part, sl)
    R.rafters(part, sl, spacing=0.303, sec=(0.04, 0.05), only_eave=False)
    if fam == "sangawara":
        R.tile_bed(part, sl, R.STACK[fam])
        R.kawara_fascia(part, sl, R.STACK[fam])
        F = sl.frame(R.STACK[fam])
        rl = (ov - 0.06) / sl.cos
        K.eave_tiles(part, F, x0, x1, style="plain")
        K.field(part, F, x0, x1, K.EXPO, rl, rows_eave=1, rows_ridge=0)
        K.ridge(part, (x0 + (0.012 if flush[0] else 0.0), sl.y(0, 0.06, R.STACK[fam]) + 0.02, 0.10),
                (x1 - (0.012 if flush[1] else 0.0), sl.y(0, 0.06, R.STACK[fam]) + 0.02, 0.10),
                courses=1, width=0.16, cap_d=0.0001, mortar=True, end_tiles=False)
    else:
        R.cover_boards(part, sl, fam, rows_eave=2, rows_ridge=0)
        if kind in ("ishioki", "skirt"):
            R.battens_stones(part, sl, R.STACK[fam] - 0.02, spacing=0.55, sparse=(kind == "skirt"), first=0.35)
    # flashing board against the wall
    part.add(box(x0, x1, y_wall - 0.05, y_wall + 0.12, 0.06, 0.09, "wood_weathered", vis=(1, 2), tag="flashing"))
    # purlin at the arm ends + brackets (udegi) from every post
    ye = sl.y(0, ov - 0.12, 0.0)
    part.add(box(x0 - (0.0 if flush[0] else 0.05), x1 + (0.0 if flush[1] else 0.05), ye - 0.10, ye, ov - 0.18, ov - 0.10,
                 "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="pent_purlin"))
    x = x0
    if node0 is not None:
        x = node0 + math.ceil((x0 + (0.04 if flush[0] else 0.0) - node0) / bracket_step - 1e-6) * bracket_step
    x_end = x1 - (0.04 if flush[1] else 0.0)
    while x <= x_end + 1e-6:
        if posts:
            part.add(box(x - 0.06, x + 0.06, 0.0, ye - 0.10, ov - 0.20, ov - 0.08, "wood_weathered", vis=(1, 2, 3),
                         geo=True, view=True, fire=True, tag="pent_post"))
        else:
            part.add(box(x - 0.03, x + 0.03, ye - 0.19, ye - 0.10, 0.06, ov - 0.10, "wood_weathered", vis=(1, 2),
                         geo=True, view=True, fire=True, tag="udegi"))
            part.add(prism([(ye - 0.19, 0.06), (ye - 0.45, 0.06), (ye - 0.19, 0.32)], "x", x - 0.025, x + 0.025,
                           "wood_weathered", vis=(1,), tag="bracket_brace"))
        x += bracket_step
    return sl, y_e


def part_hisashi(variant):
    kind = variant[1:]
    cfg = {"tile": (3.30, 0.91, 0.40, False), "board": (3.00, 0.91, 0.275, False), "ishioki": (3.10, 0.91, 0.30, False),
           "skirt": (2.70, 1.20, 0.25, True), "gable": (3.10, 0.45, 0.40, False)}[kind]
    y_wall, proj, t, posts = cfg
    p = Part("jp_p_roof_hisashi", variant, "roof", tiers={"tile": [3], "board": [1, 2, 3], "ishioki": [2], "skirt": [2],
                                                          "gable": [3]}[kind],
             used_for={"tile": "tiled street pent over a machiya shop front (eave 2.94, soffit >= 2.20)",
                       "board": "thin board pent on bracket arms (Morse)",
                       "ishioki": "stone-weighted board pent (Kiso post towns)",
                       "skirt": "board pent eave on posts over a thatch house's entrance side (G1 decision 6, Sasaki "
                                "1731): keeps the entrance above 2.20 without raising the walls",
                       "gable": "small tiled pent along a gable at the upper-floor line (Ioka)"}[kind],
             recipe="roofparts.pent(part, x0, x1, y_wall, projection, pitch, kind)",
             datum="2-ken run of a wall (z 0), y 0 = ground floor; attaches at y %.2f, projects +z %.2f" % (y_wall, proj))
    L = 2 * KEN
    sl, y_e = pent(p, 0.0, L, y_wall, proj, t, kind, posts=posts, bracket_step=KEN if posts else HALF)
    p.dim("projection_m", {"tile": 0.91, "board": 0.91, "ishioki": 0.91, "skirt": "0.91-1.20", "gable": 0.45}[kind], proj)
    p.dim("pitch_sun", {"tile": 4, "board": "2.5-3", "ishioki": 3, "skirt": "2.5-3", "gable": 4}[kind], t * 10, tol=0.05)
    soffit = y_e - 0.10 - 0.1
    p.dim("soffit_min_m", ">=2.20", soffit, source="PLAYBOOK §4 (walked under)")
    p.dims[-1]["ok"] = soffit >= 2.20
    if kind == "tile":
        p.dim("street_eave_edge_m", "2.90-3.20", y_e + 0.05)
    for x in (0.0, KEN, L):
        p.conn("post", (x, 0, 0), note="udegi bracket plugs into each post at the pent height" if not posts
               else "wall post; the pent's own posts stand on the outer line")
    p.conn("eave", (0, y_e, proj), note="pent eave line parallel to the wall")
    p.conn("top", (0, y_wall, 0), note="flashed under the upper wall or main eave")
    return p


def part_kura_eave(variant):
    p = Part("jp_p_roof_kura_eave", variant, "roof", tiers=[2, 3],
             used_for="fire-proof kura eave: plastered rafters and soffit, stepped plaster band, tiles above",
             datum="1-ken run on a 0.24 okabe wall top (z 0 = wall centreline); y 0 = floor; wall top 2.70")
    top = WALL_H
    for k, (h, pr) in enumerate(((0.20, 0.07), (0.18, 0.14))):
        y0 = top + (0.0 if k == 0 else 0.20)
        p.add(box(-0.02, KEN + 0.02, y0, y0 + h, -0.12 - pr, 0.12 + pr, "wall_shikkui", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="band"))
    yb = top + 0.38
    ov, t = 0.55, 0.45
    sl = R.Slope("front", [(0.0, ov), (KEN, ov), (KEN, -0.12), (0.0, -0.12)], (0.0, -1.0), (0.0, 0.0), (1.0, 0.0),
                 (0.0, ov), yb + 0.06, t, ov)
    p.add(slab(sl.poly, lambda x, z: sl.y(x, z, -0.12), lambda x, z: sl.y(x, z, 0.06), "wall_shikkui", vis=(1, 2, 3),
               geo=True, view=True, fire=True, tag="plastered_eave"))
    R.tile_bed(p, sl, 0.10, h0=0.06)
    R.kawara_fascia(p, sl, 0.10, mat="wall_shikkui")
    F = sl.frame(0.10)
    K.eave_tiles(p, F, 0.0, KEN, style="tomoe")
    K.field(p, F, 0.0, KEN, K.EXPO, (ov + 0.12) / sl.cos + 0.2, rows_eave=1, rows_ridge=0)
    p.dim("band_height_m", "0.30-0.45", 0.38)
    p.dim("band_projection_m", "0.05-0.10 per step", 0.07)
    p.dim("eave_overhang_m", "0.45-0.60", ov)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), hidden=True)
    p.conn("eave", (0, top, 0), note="sits on the okabe wall top; tile eave course on top")
    p.notes.append("_okiyane (detached raised roof) NOT built: the build list says its date and region are unverified "
                   "and it must not be built before they are.")
    return p


def part_gutter(variant):
    p = Part("jp_p_roof_gutter", variant, "roof", tiers=[3],
             used_for="split-bamboo gutter on iron hooks with a bamboo downpipe and a wooden funnel",
             datum="2-ken eave run; hangs 0.05 below a tile eave edge (y 2.63 at z 0.95); y 0 = ground")
    ye, ze = 2.58, 0.95
    L = 2 * KEN
    p.add(half_tube((0.0, ye, ze), (L, ye, ze), 0.05, "bamboo_weathered", n=6, vis=(1, 2, 3), tag="gutter"))
    x = 0.0
    while x <= L + 1e-6:
        p.add(box(x - 0.006, x + 0.006, ye - 0.06, ye + 0.08, ze - 0.06, ze + 0.06, "metal_iron", vis=(1,), tag="hook"))
        x += HALF
    xf = L - 0.10
    p.add(box(xf - 0.08, xf + 0.08, ye - 0.22, ye - 0.04, ze - 0.08, ze + 0.08, "wood_weathered", vis=(1, 2), tag="funnel"))
    p.add(tube((xf, ye - 0.22, ze), (xf, 0.05, ze), 0.04, "bamboo_weathered", n=8, vis=(1, 2, 3), tag="downpipe"))
    for yy in (0.8, 1.7):
        p.add(tube((xf, yy, ze - 0.04), (xf, yy, ze + 0.04), 0.043, "bamboo_weathered", n=8, vis=(1,), tag="node"))
    p.dim("gutter_diameter_m", 0.10, 0.10)
    p.dim("hook_spacing_m", 0.91, HALF)
    p.conn("eave", (0, ye + 0.05, ze), note="hangs 0.05 below the eave edge on hooks at post positions")
    return p


def register(reg):
    reg("jp_p_roof_forms", ["_kirizuma", "_yosemune", "_irimoya", "_kabuto"], part_forms)
    reg("jp_p_roof_eave_soffit", ["_tile", "_board", "_thatch"], part_eave_soffit)
    reg("jp_p_roof_sangawara_field", ["_std", "_pointed"], part_sangawara_field)
    reg("jp_p_roof_sangawara_eave", ["_tomoe", "_plain", "_lod1_strip"], part_sangawara_eave)
    reg("jp_p_roof_sangawara_verge", ["_L", "_R"], part_sangawara_verge)
    reg("jp_p_roof_kawara_ridge", ["_c3", "_c5", "_hip"], part_kawara_ridge)
    reg("jp_p_roof_onigawara", ["_plain", "_sui"], part_onigawara)
    reg("jp_p_roof_ishioki_field", ["_std", "_worn"], part_ishioki_field)
    reg("jp_p_roof_ishioki_battens", ["_stoneset8", "_sparse"], part_ishioki_battens)
    reg("jp_p_roof_itabuki_field", ["_plain", "_bamboo", "_kakigara"], part_itabuki_field)
    reg("jp_p_roof_board_ridge", ["_strips", "_stoned"], part_board_ridge)
    reg("jp_p_roof_thatch_body", ["_yosemune", "_kirizuma", "_irimoya", "_new"], part_thatch_body)
    reg("jp_p_roof_thatch_ridge", ["_bamboo", "_tile", "_shiba", "_umanori"], part_thatch_ridge)
    reg("jp_p_roof_kemuridashi", ["_hood", "_koshiyane", "_irimoya"], part_kemuridashi)
    reg("jp_p_roof_hafu", ["_tile", "_board", "_thatch"], part_hafu)
    reg("jp_p_roof_hisashi", ["_tile", "_board", "_ishioki", "_skirt", "_gable"], part_hisashi)
    reg("jp_p_roof_kura_eave", ["_std"], part_kura_eave)
    reg("jp_p_roof_hongawara", ["_field", "_eave", "_ridge"], part_hongawara)
    reg("jp_p_roof_gutter", ["_std"], part_gutter)
