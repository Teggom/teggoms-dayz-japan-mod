#!/usr/bin/env python3
r"""make_m1_materials.py - the materials agent M1 ADDS to jp_common through B1's pipeline (2026-09-30): the material gaps
W2, W3 and B3a left open (PRODUCTION_PLAN "Confirmed future work").

  python make_m1_materials.py [--no-pack] [--only ID[,ID...]]
  python make_m1_materials.py --draft [--only ...]   textures to spikes/M1/draft/ only (no PAA, no sidecar, no palette)

Adds only; never changes an existing material or palette entry (the route of make_l1 / make_l2 / make_s1_materials.py:
B1's make_one = textures, PAAs, rvmats, sidecar, C1 matcheck on the PNG and the shipped PAA), then repacks jp_common.

- jp_m_ground_earth_bare        Bare outdoor earth: grave mounds, worn paths, yard ground. New palette `earth_bare`,
                                sampled (Kanto loam topsoil k41 + brown forest soil k37 + a worn Hida path k27).
- jp_m_wood_new                 Pale NEW wood: freshly split / planed sugi-hinoki (fresh grave posts, new repairs).
                                New palette `wood_new_cut`, sampled (i04, split kindling, white-balanced on the ash).
- jp_m_wood_silver              True silver-grey weathered wood (old unpainted sugi / hinoki). New palette
                                `wood_silver_grey`, sampled (k31 old handcart in sun, c03 Tsumago gate post + leaf).
- jp_m_floor_tatami_heri_cha    Plain brown (cha) cotton / hemp tatami edge: B1's heri recipe in palette `cha_koge`.
- jp_m_decal_carved_text_grave  Carved posthumous names for gravestones: 13 cells (14 names), Yuji Syuku, vertical.
- jp_m_decal_sumi_text_grave    Ink posthumous names for wooden grave posts (bohyo): 6 cells, crisp to faded.
- jp_m_wicker_aged              Warm woven bamboo / willow wicker for kori trunks (bamboo_weave's twill, not grey).
                                New palette `wicker_aged`, sampled from the CC0 scan bamboo_wall (no kori photo here).
- jp_m_wood_firewood            Split firewood sides (split faces + grey bark). New palette `firewood_split` (i22).
- jp_m_wood_endgrain_firewood   Firewood log ends (B1's endgrain recipe). New palette `firewood_end` (i22).
NOT made: Sanskrit seed syllables (bonji) - no Siddham-capable font on this machine (spikes/M1/font_scan.py).
Samples and boxes: spikes/M1/sample.py -> spikes/M1/samples.json. C1 results: src/JP/common/materials/checks_m1.json.
Never starts or stops the server or any GUI program.
"""
import json
import math
import os
import struct
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

PAL = os.path.join(DEV, "playbook", "palette.json")
DRAFT = os.path.join(DEV, "spikes", "M1", "draft")
f32 = np.float32
T, MT = B.T, B.MT

SAMPLED_BY = "Added 2026-09-30 by M1 (spikes/M1/sample.py, the playbook method: per box the mid-70 % luminance median, " \
             "mean of the box medians)."
ENTRIES = [
    {"id": "earth_bare", "name": "Bare outdoor earth (Kanto loam / brown forest soil), dry surface",
     "material": "andosol (kuroboku) topsoil and brown forest soil: grave mounds, worn paths, yard ground",
     "group": "ground", "tiers": [1, 2, 3],
     "use": "grave mounds, worn paths, bare yard ground (jp_m_ground_earth_bare)",
     "note": SAMPLED_BY + " Kept: k41 (Matsudo, Kanto loam topsoil at a roadside Koshin site, sunlit, 197,171,127), k37 "
             "(Shikaumi shrine, brown forest soil under the sacred tree, diffuse forest light: 138,117,108 and "
             "117,101,84), k27 (a worn earth path under a Hida village torii, 140,133,112). Rejected: the deep-shade k41 "
             "box (77,69,57; B1's doma rule), x03 (concrete path), x08 (a museum yard of dressed sand). Browner and "
             "darker than earth_road (208,190,167, packed road), browner than doma_earth (137,132,128). Wet earth is "
             "darker: the _w0 fresh mound is moist.",
     "srgb": [148, 130, 108], "method": "sampled", "tolerance_dE76": 14, "observed_spread_dE76": 20.7,
     "samples": [{"ref": "k41_koshin_sendabori", "box": [0.03, 0.83, 0.33, 0.97], "value": [197, 171, 127]},
                 {"ref": "k37_shimenawa_tree", "box": [0.40, 0.66, 0.62, 0.78], "value": [138, 117, 108]},
                 {"ref": "k37_shimenawa_tree", "box": [0.20, 0.56, 0.38, 0.64], "value": [117, 101, 84]},
                 {"ref": "k27_hida_torii", "box": [0.44, 0.84, 0.63, 0.96], "value": [140, 133, 112]}]},
    {"id": "wood_new_cut", "name": "Freshly cut / split sugi-hinoki, unweathered (pale)",
     "material": "new conifer wood: split or planed sugi / hinoki before the sun greys it",
     "group": "timber", "tiers": [1, 2, 3],
     "use": "fresh grave posts, new repairs, new split boards (jp_m_wood_new); weathers to wood_silver_grey",
     "note": SAMPLED_BY + " Kept: i04 (Tsunashima farmhouse, three freshly split conifer sticks by the irori, lit "
             "faces), white-balanced on the hearth's ash wall in the same light (raw 144,150,152 -> the chromaticity "
             "of ash_grey): raw 179,167,153 / 152,135,123 / 155,142,136 -> 190,165,143 / 161,134,115 / 164,141,127. "
             "Rejected: k36 (red pine end grain in low sun, not sugi side grain), x01 bottom (modern plywood), "
             "the hinoki_planks scan (board_new 156,122,84: an oiled-looking board, darker and oranger than split "
             "wood). Paler than board_new, far from timber_weathered (118,82,73).",
     "srgb": [172, 146, 129], "method": "sampled", "tolerance_dE76": 11, "observed_spread_dE76": 10.9,
     "samples": [{"ref": "i04_tsunashima_irori", "box": [0.683, 0.283, 0.717, 0.367], "value": [190, 165, 143]},
                 {"ref": "i04_tsunashima_irori", "box": [0.764, 0.317, 0.791, 0.400], "value": [161, 134, 115]},
                 {"ref": "i04_tsunashima_irori", "box": [0.480, 0.342, 0.502, 0.392], "value": [164, 141, 127]}],
     "white_balance": {"ref": "i04_tsunashima_irori", "box": [0.20, 0.24, 0.36, 0.40], "to": "ash_grey"},
     "weathering": {"worst": "wood_silver_grey", "max_mix": 0.35}},
    {"id": "wood_silver_grey", "name": "Silver-grey weathered wood (old unpainted sugi / hinoki)",
     "material": "unpainted softwood after years of sun and rain: the lignin washed out, the surface silver-grey",
     "group": "timber", "tiers": [1, 2, 3],
     "use": "old grave posts, old fences, gates, carts, sheds: the classic silver look (jp_m_wood_silver)",
     "note": SAMPLED_BY + " Kept, all in daylight: k31 (an old unpainted handcart at Uzumasa, sunlit side rail, "
             "130,124,112), c03 (Tsumago, a sunlit weathered gate post 146,146,145 and its board leaf 103,104,103). "
             "Rejected: x01 (Ioka storehouse gable boards: the right look but evening shade, 57-64 even after a white "
             "balance on the plaster), c04 (Tsumago gate posts, backlit, 44-53). Close to roof_board_silver "
             "(123,128,134, x04 roof) but a touch warmer; far from timber_weathered (118,82,73, the brown of wet "
             "facades).",
     "srgb": [126, 125, 120], "method": "sampled", "tolerance_dE76": 14, "observed_spread_dE76": 23.1,
     "samples": [{"ref": "k31_daihachi_uzumasa", "box": [0.18, 0.60, 0.42, 0.68], "value": [130, 124, 112]},
                 {"ref": "c03_tsumago_street", "box": [0.900, 0.36, 0.917, 0.53], "value": [146, 146, 145]},
                 {"ref": "c03_tsumago_street", "box": [0.926, 0.43, 0.967, 0.53], "value": [103, 104, 103]}],
     "weathering": {"worst": "stone_lantern", "max_mix": 0.3}},
    {"id": "wicker_aged", "name": "Aged wicker (woven bamboo / willow), indoor",
     "material": "woven split bamboo or peeled willow (kori-yanagi) of travel and clothes trunks, aged indoors",
     "group": "fitting", "tiers": [1, 2, 3],
     "use": "kori trunks (jp_m_wicker_aged); bamboo_weathered stays for outdoor, sun-bleached bamboo",
     "note": SAMPLED_BY + " No photo of a kori or of indoor wicker in usable light exists on this machine: i07's woven "
             "basket (Fukagawa Edo Museum) is under a strong orange spotlight with no grey card, k28 is hand-tinted, "
             "k06 a print. Value = the CC0 Poly Haven scan bamboo_wall (Amal Kumar; aged dried bamboo culms under "
             "controlled light), whole diffuse map. Warm tan, unlike bamboo_weathered (169,157,146, sun-bleached "
             "fences). Upgrade from a museum photo of a Toyooka willow kori when one is saved locally.",
     "srgb": [137, 110, 86], "method": "sampled", "tolerance_dE76": 12, "observed_spread_dE76": 5.4,
     "samples": [{"ref": "polyhaven:bamboo_wall (diff 1k)", "box": [0, 0, 1, 1], "value": [137, 110, 86]}]},
    {"id": "firewood_split", "name": "Split firewood, sides (split faces and bark)",
     "material": "split broadleaf / conifer billets: tan split faces, grey bark",
     "group": "timber", "tiers": [1, 2, 3], "use": "firewood stacks and bundles (jp_m_wood_firewood)",
     "note": SAMPLED_BY + " i22 (a kamado with split firewood stacked beside it, CC0): the split pieces (98,74,42), "
             "the mixed sticks (88,77,54) and the big round log's bark (137,126,84). The kamado body in the same "
             "light is neutral (51,53,55), so no white balance. Less red, more yellow-olive than timber_weathered, "
             "which the firewood props used before (B3a gap: 'firewood redder than ref i22').",
     "srgb": [108, 92, 60], "method": "sampled", "tolerance_dE76": 14, "observed_spread_dE76": 21.3,
     "samples": [{"ref": "i22_kamado_firewood", "box": [0.70, 0.10, 0.92, 0.32], "value": [98, 74, 42]},
                 {"ref": "i22_kamado_firewood", "box": [0.62, 0.35, 0.80, 0.52], "value": [88, 77, 54]},
                 {"ref": "i22_kamado_firewood", "box": [0.60, 0.12, 0.67, 0.33], "value": [137, 126, 84]}]},
    {"id": "firewood_end", "name": "Firewood log ends (fresh-cut end grain)",
     "material": "saw- or axe-cut ends of firewood billets", "group": "timber", "tiers": [1, 2, 3],
     "use": "end caps of firewood (jp_m_wood_endgrain_firewood)",
     "note": SAMPLED_BY + " i22: six small boxes inside six cut log ends (169,136,78 / 163,134,66 / 157,124,60 / "
             "170,140,73 / 131,105,56 / 167,138,71). Pale yellow-tan; wood_endgrain (timber_weathered) is the red-brown "
             "end of old structural timber.",
     "srgb": [160, 130, 67], "method": "sampled", "tolerance_dE76": 8, "observed_spread_dE76": 5.9,
     "samples": [{"ref": "i22_kamado_firewood", "box": b} for b in (
         [0.6813, 0.1393, 0.6937, 0.1581], [0.7984, 0.2488, 0.8109, 0.2676], [0.8792, 0.2817, 0.8917, 0.3005],
         [0.8375, 0.4014, 0.85, 0.4202], [0.9198, 0.2175, 0.9323, 0.2363], [0.676, 0.3388, 0.6885, 0.3576])]},
]


def add_palette():
    pal = json.load(open(PAL, encoding="utf-8"))
    have = {e.get("id") for e in pal["entries"]}
    added = []
    for ent in ENTRIES:
        if ent["id"] in have:
            continue
        e = dict(ent)
        e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
        pal["entries"].append(e)
        added.append(ent["id"])
    if added:
        with open(PAL, "wb") as f:
            f.write(json.dumps(pal, indent=1).encode("utf-8"))
    return added


# ================================================================================================ recipes
def ground_earth_bare(lv, S):
    """Bare earth on a 2 m tile: the clay_floor_001 scan (packed earth) re-coloured, crumb and small stones, a few
    roots / needles; _w0 a fresh mound (moist, darker, loose clods), _w1 settled and dry, _w2 overgrown at the edges:
    moss, litter, rain rills."""
    d, nn, r = B.src("clay_floor_001", S, kn=[0.9, 0.6, 0.6][lv])
    t = [T("earth_bare", -9, 1, 2), T("earth_bare", 0, 0, 0), T("earth_bare", -5, -1, -2)][lv]
    co = MT.recolor(d, t, [1.5, 1.6, 1.5][lv], 0.25)
    yy, xx = B.grid(S)
    h = np.zeros((S, S), f32)
    mask = B.Z(S)
    # soil tone patches (humus-dark and dry-pale), crumbs and pebbles (all wears)
    tone = MT.fbm(S, 2.6, 1, 1, 7110)
    co = co * (1 + 0.12 * np.clip(tone, -1.5, 1.5))[..., None]
    crumb = MT.spots(S, 260, 10, 1, 2, 40, 7111)
    co = co * (1 - 0.35 * crumb)[..., None]
    peb = MT.spots(S, 120, 8, 1, 3, 30, 7101)
    co = MT.mix(co, (150, 140, 124), peb * 0.55)
    h = h + peb * 0.8 - crumb * 0.4
    if lv == 0:                                                   # loose clods of a fresh mound
        cl = MT.blur((MT.fbm(S, 2.2, 1, 1, 7102) > 0.9).astype(f32), 1.5)
        co = co * (1 - 0.18 * cl)[..., None]
        h = h + cl * 1.6
    rw, rt = B.fibres(S, [30, 60, 40][lv], 7103, 0.0, 3.0, 10, 40)   # roots / needles / straws
    co = MT.mix(co, (92, 70, 48), rw * 0.6)
    if lv == 2:
        mo = B.blobs(S, 7104, 1.0, 2.6, 3)                           # moss and weeds creep in
        co = MT.patch(co, mo, (72, 82, 46), 0.75, 7105)
        lf = B.blobs(S, 7106, 1.3, 2.4, 2)                           # wet leaves
        co = MT.patch(co, lf, (96, 66, 42), 0.7, 7107)
        rill = np.clip(1 - np.abs(MT.fbm(S, 2.0, 6, 1, 7108)) * 6, 0, 1) * (MT.fbm(S, 1.5, 1, 1, 7109) > 0.3)
        co = co * (1 - 0.12 * rill)[..., None]
        h = h - rill * 1.0
        mask = mo | lf
    return B.R(np.clip(co, 0, 1), MT.combine(nn, MT.h2n(h, 1.0)), r * [0.8, 1.0, 0.9][lv], mask, t, 0.06,
               [0.2, 0.12, 0.15][lv])


def _planks(asset, S):
    return MT.photo(asset, "diff", S), MT.pnormal(asset, S), MT.prough(asset, S)


def wood_new(lv, S):
    """Pale new wood on wood_weathered's layout (Weathered Planks, 2 m, grain along v) but with the hinoki scan's
    fine grain: low contrast cream-tan; _w1 a season old (warmer, first dirt); _w2 a year or two (beginning to grey
    at the surface, dirt at the foot). Stays well short of wood_silver."""
    d, nn, r = B.hinoki(S, 1.3)
    t = [T("wood_new_cut", 2, 0, -1), T("wood_new_cut", -3, 1, 3),
         T("wood_new_cut", -4, toward="wood_silver_grey", t=0.30)][lv]
    co = MT.recolor(d, t, [0.75, 0.8, 0.85][lv], [0.25, 0.2, 0.1][lv])
    mask = B.Z(S)
    h = np.zeros((S, S), f32)
    if lv == 0:                                                   # fresh tool marks: faint plane / split ridges
        rid = MT.fbm(S, 1.4, 30, 1, 7201)
        co = co * (1 + 0.025 * rid)[..., None]
        h = h + rid * 0.3
    if lv >= 1:
        co = MT.grey(co, [0, 0.1, 0.35][lv]) * (1 + 0.04 * MT.fbm(S, 2.0, 1, 10, 7202))[..., None]
    if lv == 2:                                                   # dirt splash and first checks
        sp = B.scratches(S, 25, 7203, 30, 160, ang=math.pi / 2, sd=0.04, width=1)
        co = MT.mix(co, (60, 52, 44), sp * 0.6)
        h = h - sp * 1.5
        mask = sp > 0.3
    return B.R(np.clip(co, 0, 1), MT.combine(nn, MT.h2n(h, 1.0)), r * [0.85, 0.9, 1.0][lv], mask, t, 0.12, 0.2)


def wood_silver(lv, S):
    """Silver-grey weathered wood on wood_weathered's source and layout (Weathered Planks, 2 m, grain along v): raised
    grain, nearly no chroma; _w1 dark streaks and pale lichen; _w2 old and damp: darker, splits, green-black algae."""
    a, pn, pr = _planks("weathered_planks", S)
    t = [T("wood_silver_grey", 2, 0, 0), T("wood_silver_grey", -2, toward="stone_lantern", t=0.1),
         T("wood_silver_grey", -3, toward="stone_lantern", t=0.25)][lv]
    co = MT.recolor(a, t, [1.25, 1.2, 1.15][lv], 0.05)
    co = MT.grey(co, 0.6) * (1 + 0.06 * MT.fbm(S, 2.0, 1, 12, 7301))[..., None]   # fine pale streaks along the grain
    mask = B.Z(S)
    h = np.zeros((S, S), f32)
    if lv >= 1:
        co, lm = MT.lichen_moss(co, S, 1, 7302, [0, 25, 35][lv], None)
        dk = MT.fbm(S, 1.6, 1, 8, 7303) > 1.0                     # dark weather streaks running down
        co = MT.patch(co, dk, (62, 62, 60), 0.5, 7304)
        mask |= lm | dk
    if lv == 2:
        sp = MT.edge_lines(S, 90, 12, 1, 2, (40, 220)) if hasattr(MT, "edge_lines") else \
            B.scratches(S, 60, 7305, 40, 220, ang=math.pi / 2, sd=0.03)
        co = MT.mix(co, (34, 32, 30), sp * 0.85)
        al = B.blobs(S, 7306, 1.2, 2.8, 3)                          # green-black algae in the damp
        co = MT.patch(co, al, (58, 64, 50), 0.6, 7307)
        h = h - sp * 2.0
        mask |= (sp > 0.3) | al
    return B.R(np.clip(co, 0, 1), MT.combine(pn, MT.h2n(h, 1.0)), pr * [0.95, 1.0, 1.0][lv], mask, t, 0.12, 0.2)


def floor_tatami_heri_cha(lv, S):
    """B1's floor_tatami_heri recipe (plain weave, frayed and torn with wear) in the cha (tea-brown) dye."""
    t = [T("cha_koge", 2, 0, 1), T("cha_koge", 0, 0, 0), T("cha_koge", 3, -1, -3)][lv]
    co, nn, r = B.cotton_common(S, t, kn=0.8, tiles=4, contrast=1.6, seed=1210)
    yy, xx = B.grid(S)
    mask = B.Z(S)
    h = np.zeros((S, S), f32)
    if lv >= 1:
        fw, _ = B.fibres(S, [0, 300, 500][lv], 1211, 0.0, 0.6, 4, 14)
        fr = fw * ((yy < 0.06 * S) | (yy > 0.94 * S))
        co = MT.mix(co, (150, 128, 100), fr * 0.7)
        mask |= fr > 0.3
    if lv == 2:
        tear = B.blobs(S, 1212, 1.5, 3.0, 2)
        rush = 1 + 0.15 * np.sin(yy * 2 * math.pi / 3.0)
        co[tear] = (B.base((127, 108, 90), rush))[tear]
        h = h - 1.0 * tear
        mask |= tear
    return B.R(co, MT.combine(nn, MT.h2n(h, 1.0)), r, mask, t, 0.08, 0.2)


def wicker_aged(lv, S):
    """B1's bamboo_weave geometry (2/2 twill of ~1.5 cm strips) in a warm, indoor-aged wicker colour; wear darkens and
    dirties it (indoors it browns, it does not bleach grey)."""
    t = [T("wicker_aged", 4, 0, 2), T("wicker_aged", 0), T("wicker_aged", -6, 0, -2)][lv]
    w = 8
    yy, xx = np.mgrid[0:S, 0:S]
    i, j = xx // w, yy // w
    over = ((i - j) % 4) < 2
    fx, fy = (xx % w) / w, (yy % w) / w
    across = np.where(over, fx, fy)
    along = np.where(over, fy, fx)
    prof = np.sin(np.pi * across)
    edge = (across < 0.1) | (across > 0.9)
    arch = np.sin(np.pi * along)
    fib = np.where(over, MT.fbm(S, 1.5, 1, 20, 7401), MT.fbm(S, 1.5, 20, 1, 7402))
    rg = np.random.default_rng(7403)
    tint = np.where(over, rg.normal(1, 0.08, S // w)[i], rg.normal(1, 0.08, S // w)[j])
    val = tint * (0.8 + 0.2 * prof) * (0.88 + 0.12 * arch) * (1 + 0.06 * fib)
    val = np.where(edge, val * 0.5, val)
    co = B.base(t, val)
    h = prof * 1.0 + arch * 0.8 - edge * 1.0
    mask = B.Z(S)
    if lv >= 1:                                                   # handling grime on the strips' crowns
        g = np.clip(MT.fbm(S, 2.2, 1, 1, 7404), 0, None) * [0, 0.15, 0.3][lv]
        co = co * (1 - g * arch)[..., None]
    if lv == 2:                                                   # broken strips, mildew
        cells = rg.random((S // w, S // w)) < 0.04
        br = cells[j, i]
        co[br] = np.array([40, 33, 26], f32) / 255
        mil = MT.blur(MT.spots(S, 10, 10, 2, 8, 20, 7405), 1.5) > 0.35
        co = MT.patch(co, mil, (150, 150, 128), 0.5, 7406)
        h = h - br * 2
        mask = br | mil
    return B.R(np.clip(co, 0, 1), MT.h2n(h.astype(f32), 1.2), 0.6, mask, t, 0.12, 0.25)


def wood_firewood(lv, S):
    """Split firewood sides on a 2 m tile (the props' world UVs): long split facets of tan wood with fibre tear-out,
    and runs of grey-olive bark (the rounds' outsides) along v; _w0 fresh-split, _w1 seasoned a year (greyer),
    _w2 old, damp, mouldy."""
    a, pn, pr = _planks("weathered_planks", S)
    t = [T("firewood_split", 3, 0, 2), T("firewood_split", 0, 0, 0), T("firewood_split", -4, -1, -3)][lv]
    yy, xx = B.grid(S)
    split = MT.recolor(a, (160, 120, 70), 1.3, 0.2)                # split faces, warm tan with torn fibres
    tear = MT.fbm(S, 1.2, 1, 40, 7501)
    split = split * (1 + 0.08 * tear)[..., None]
    bark_m = (MT.fbm(S, 2.4, 1, 6, 7502) > 0.35).astype(f32)       # bark in long strips along v
    bark_m = MT.blur(bark_m, 1.2)
    bk = MT.fbm(S, 1.3, 25, 3, 7503)                               # bark fissures run along v
    bark = B.base((138, 126, 90), 0.85 + 0.2 * np.clip(bk, -1.5, 1.5) * 0.5)
    co = split * (1 - bark_m[..., None]) + bark * bark_m[..., None]
    co = MT.recolor(co, t, 1.0, 0.45)
    h = bark_m * 1.0 + np.clip(bk, -1, 1) * bark_m * 0.6 + tear * 0.2 * (1 - bark_m)
    mask = B.Z(S)
    if lv >= 1:
        co = MT.grey(co, [0, 0.25, 0.4][lv])
    if lv == 2:
        mo = B.blobs(S, 7504, 1.2, 2.6, 2)
        co = MT.patch(co, mo, (132, 136, 112), 0.55, 7505)          # pale mould
        mask = mo
    return B.R(np.clip(co, 0, 1), MT.combine(pn, MT.h2n(h, 1.0)), pr, mask, t, 0.1, 0.2)


def wood_endgrain_firewood(lv, S):
    """B1's wood_endgrain recipe (one log end per texture, pith at the centre) in the firewood end colour."""
    t = [T("firewood_end", 3, 0, 2), T("firewood_end", -2, 0, -2), T("firewood_end", -4, 0, -3)][lv]
    yy, xx = B.grid(S)
    c = S / 2
    rr = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    f = rr / 4.5 + 0.8 * np.sin(rr / 29) + MT.fbm(S, 2.4, 1, 1, 7601) * 0.6
    fr = f % 1.0
    late = np.clip((fr - 0.62) / 0.1, 0, 1) * np.clip((1 - fr) / 0.08, 0, 1)
    val = (1 - 0.22 * late + 0.05 * MT.fbm(S, 2.6, 1, 1, 7602)) * (1 - 0.35 * np.exp(-(rr / 5) ** 2))
    bark = np.clip((rr - 0.45 * S) / (0.03 * S), 0, 1)              # the bark ring at the rim
    val = val * (1 - 0.45 * bark)
    if lv == 0:
        val = val * (1 + 0.03 * np.sin(np.sqrt((xx - c) ** 2 + (yy + 3 * S) ** 2) / 5 * 2 * math.pi))
    co = B.base(t, val)
    co = MT.mix(co, (110, 100, 80), bark * 0.6)
    h = -late * 0.8
    mask = B.Z(S)                                                 # the bark ring is part of the look: counted in the mean
    if lv >= 1:
        rg = np.random.default_rng(7603 + lv)
        im = Image.new("L", (S, S), 0)
        dr = ImageDraw.Draw(im)
        for _ in range([0, 4, 7][lv]):
            a = rg.uniform(0, 2 * math.pi)
            r1 = rg.uniform(0.3, 0.45) * S
            dr.line([(c + 4 * math.cos(a), c + 4 * math.sin(a)), (c + r1 * math.cos(a), c + r1 * math.sin(a))],
                    fill=255, width=[1, 1, 2][lv])
        ck = MT.blur(B._arr(im.convert("RGB"))[..., 0], 0.5)
        co = MT.mix(co, (36, 28, 20), ck * 0.9)
        co = MT.grey(co, [0, 0.2, 0.35][lv])
        h = h - ck * 3
        mask |= ck > 0.3
    return B.R(np.clip(co, 0, 1), MT.h2n(h, 1.0), 0.8, mask, t, 0.1, 0.2)


# ================================================================================================ the text atlases
# Posthumous names (kaimyo) of commoners, as on Edo stones and grave posts up to 1730 (forms: M1_PROGRESS.md "Text").
# A cell = (name, (x0, y0, x1, y1) px on the 1024 atlas, use, columns); a column = (text, size px, top indent in
# characters, x centre as a fraction of the cell width). Right column = the era year (+ cyclical sign), centre = the
# kaimyo, left = month and day: the usual face of an Edo grave. Fixed x fractions, so the crops NAME (0.26-0.74),
# DATE_R (0.70-1.0) and DATE_L (0.0-0.30) always hold one column.
def _three(year, name, md, nsize=50, dsize=24):
    return [(year, dsize, 1.0, 0.85), (name, nsize, 0.0, 0.5), (md, dsize, 2.2, 0.15)]


CW, CH = 170, 340
CARVED_GRAVE = [
    ("kaimyo_joshin_shinji_genroku8", "a man, Genroku 8 (1695)", _three("元禄八年乙亥", "浄心信士", "三月十日")),
    ("kaimyo_myotei_shinnyo_hoei4", "a woman, Hoei 4 (1707)", _three("宝永四年丁亥", "妙貞信女", "十一月廿三日")),
    ("kaimyo_soen_zenjomon_enpo6", "a man (zenjomon, an older stone), Enpo 6 (1678)",
     _three("延宝六年戊午", "宗円禅定門", "八月十五日", 48)),
    ("kaimyo_myoju_zenjoni_kanbun10", "a woman (zenjoni, an older stone), Kanbun 10 (1670)",
     _three("寛文十年庚戌", "妙寿禅定尼", "二月九日", 48)),
    ("kaimyo_shunko_doji_kyoho5", "a boy (doji), Kyoho 5 (1720)", _three("享保五年庚子", "春光童子", "四月八日")),
    ("kaimyo_shugetsu_donyo_shotoku3", "a girl (donyo), Shotoku 3 (1713)",
     _three("正徳三年癸巳", "秋月童女", "九月十二日")),
    ("kaimyo_ryozen_shinji_kyoho14", "a man, Kyoho 14 (1729)", _three("享保十四年己酉", "了善信士", "正月廿日")),
    ("kaimyo_chisei_shinnyo_kyoho10", "a woman, Kyoho 10 (1725)", _three("享保十年乙巳", "智清信女", "六月五日")),
    ("kaimyo_shaku_ryonen_kyoho8", "a man, Shin sect (shaku- name, no rank title), Kyoho 8 (1723)",
     _three("享保八年癸卯", "釈了念", "十月三日", 54)),
    ("kaimyo_kigen_dokaku_shinji_genroku11", "a man, Zen 'kigen' (returned to the source) prefix, Genroku 11 (1698)",
     _three("元禄十一年戊寅", "帰元道覚信士", "七月二日", 44)),
    ("kaimyo_enjaku_myosho_shinnyo_kyoho12", "a woman, Zen 'enjaku' (perfect rest) prefix, Kyoho 12 (1727)",
     _three("享保十二年丁未", "円寂妙照信女", "七月十日", 44)),
    ("kaimyo_hozan_zenjomon_shotoku1", "a man (zenjomon), Shotoku 1 (1711)",
     _three("正徳元年辛卯", "法山禅定門", "十二月朔日", 48)),
]
CARVED_COUPLE = ("kaimyo_couple_dosei_myosei", "a married couple on one stone: husband Genroku 11 (1698), wife "
                 "Kyoho 7 (1722); use the whole cell on a wide stone",
                 [("元禄十一年戊寅八月", 22, 1.0, 0.89), ("道清信士", 48, 0.0, 0.64), ("妙清信女", 48, 0.0, 0.36),
                  ("享保七年壬寅三月", 22, 1.0, 0.11)])
SUMI_GRAVE = [
    ("bohyo_jonen_shinji_kyoho15", "a man, Kyoho 15 (1730): a fresh post", _three("享保十五年庚戌", "浄念信士", "三月七日")),
    ("bohyo_myoho_shinnyo_kyoho15", "a woman, Kyoho 15 (1730): a fresh post",
     _three("享保十五年庚戌", "妙法信女", "正月十八日")),
    ("bohyo_shungaku_doji_kyoho14", "a boy, Kyoho 14 (1729)", _three("享保十四年己酉", "春岳童子", "八月四日")),
    ("bohyo_soshin_shinji_kyoho13", "a man, Kyoho 13 (1728)", _three("享保十三年戊申", "宗心信士", "五月廿日")),
    ("bohyo_chiko_shinnyo_kyoho12", "a woman, Kyoho 12 (1727)", _three("享保十二年丁未", "智光信女", "九月廿八日")),
    ("bohyo_dosen_zenjomon_kyoho9", "a man (zenjomon), Kyoho 9 (1724): an old post",
     _three("享保九年甲辰", "道仙禅定門", "九月朔日", 48)),
]
GRAVE_CROPS = {"NAME": [0.26, 0.0, 0.74, 1.0], "DATE_R": [0.70, 0.0, 1.0, 1.0], "DATE_L": [0.0, 0.0, 0.30, 1.0]}


def _cells(kind):
    """[(name, (x0, y0, x1, y1), use, cols)]: 6 cells a row, CW x CH px; the couple stone takes two slots."""
    if kind == "carved_grave":
        lst = CARVED_GRAVE + [CARVED_COUPLE]
    else:
        lst = SUMI_GRAVE
    out = []
    k = 0
    for name, use, cols in lst:
        span = 2 if name == CARVED_COUPLE[0] else 1
        if k % 6 + span > 6:
            k += 6 - k % 6
        x0, y0 = (k % 6) * CW, (k // 6) * CH
        out.append((name, (x0, y0, x0 + CW * span, y0 + CH), use, cols))
        k += span
    return out


def grave_layout(kind, S=1024, sc=2):
    """Coverage mask (0-1) and the cells' UV rectangles, drawn with B1's column writer (_col: Yuji Syuku)."""
    im = Image.new("L", (S * sc, S * sc), 0)
    d = ImageDraw.Draw(im)
    uv = {}
    for name, (x0, y0, x1, y1), use, cols in _cells(kind):
        uv[name] = {"uv": [round(x0 / S, 4), round(y0 / S, 4), round(x1 / S, 4), round(y1 / S, 4)], "for": use,
                    "text": " / ".join(c[0] for c in cols)}
        if len(cols) == 3:
            uv[name]["crops"] = GRAVE_CROPS
        for t, s, ind, xf_ in cols:
            if ind == 0:                                          # the name: centred in the cell's height
                top = y0 + max(8, ((y1 - y0) - len(t) * 1.06 * s) / 2)
            else:                                                 # the dates: hung from the top, indented
                top = y0 + 12 + ind * s
            xc = x0 + xf_ * (x1 - x0)
            assert top + len(t) * 1.06 * s <= y1 + 1, (name, t)
            B._col(d, xc * sc, top * sc, t, s, sc, kana_hentai=False)
    a = B._arr(im.resize((S, S), Image.LANCZOS).convert("RGB"))[..., 0]
    return a, uv


def decal_carved_text_grave(lv, S):
    """B1's decal_carved_text recipe (V-groove from the letter mask, baked light from the upper left, grime in the cuts,
    lichen at _w2) on the grave atlas."""
    m, _ = B.atlas("carved_grave", S)
    t = [T("stone_lantern", 3), T("stone_lantern", 0), T("stone_lantern", -3)][lv]
    co = MT.recolor(MT.photo("rock_surface", "diff", S), t, 1.0, 0.3)
    soft = [0.0, 1.5, 1.5][lv]
    g = 0.55 * MT.blur(m, 1.2 + soft) + 0.45 * MT.blur(m, 3.0 + soft)
    depth = np.clip(g / max(float(g.max()), 1e-4), 0, 1)
    co = co * (1 - [0.22, 0.30, 0.28][lv] * depth)[..., None]
    gx = (np.roll(depth, -1, 1) - np.roll(depth, 1, 1)) * 0.5
    gy = (np.roll(depth, -1, 0) - np.roll(depth, 1, 0)) * 0.5
    lit = np.clip((gx + gy) * 18.0 * [1.0, 0.7, 0.6][lv], -0.45, 0.45)
    co = co * (1 - lit)[..., None]
    mask = B.Z(S)
    if lv >= 1:
        gr = depth * [0, 0.45, 0.35][lv]
        co = MT.mix(co, (38, 36, 32), gr)
        mask |= gr > 0.25
    alpha = np.clip(MT.blur(m, 2.0) * 2.4, 0, 1)
    h = -depth * [3.0, 2.2, 1.8][lv]
    if lv == 2:
        li = MT.spots(S, 90, 12, 3, 10, 24, 7705) * (MT.fbm(S, 1.6, 1, 1, 7706) > 0)
        li = MT.blur(li, 1.0) * (MT.blur(m, 12) > 0.02)
        co = MT.mix(co, (176, 176, 146), li * 0.7)
        alpha = np.maximum(alpha, li * 0.95)
        h = h * (1 - 0.7 * li) + li * 0.6
        mask |= li > 0.3
    return B.R(np.clip(co, 0, 1), MT.combine(MT.pnormal("rock_surface", S, k=0.5), MT.h2n(h, 2.0)), 0.85, mask, t,
               0.15, 0.25, alpha=alpha)


def decal_sumi_text_grave(lv, S):
    """B1's decal_sumi_text recipe on the grave-post atlas: _w0 crisp black (a new post), _w1 faded, _w2 a ghost."""
    m, _ = B.atlas("sumi_grave", S)
    t = [T("sumi_black", -2), T("sumi_black", 7, 2, 5), T("sumi_black", 8, 2, 5)][lv]
    co = B.base(t, 1 + 0.05 * MT.fbm(S, 2.4, 1, 1, 7801))
    kasure = np.clip(MT.fbm(S, 1.4, 1, 6, 7802) - 0.8, 0, 1)
    a = m * (1 - [0.2, 0.35, 0.35][lv] * kasure)
    if lv == 1:
        a = a * np.clip(0.72 + 0.12 * MT.fbm(S, 2.4, 1, 1, 7803), 0.45, 0.9)
    if lv == 2:
        flake = MT.fbm(S, 2.0, 1, 1, 7804) > 0.5
        a = a * 0.42 * np.where(flake, 0.3, 1.0)
    return B.R(co, MT.flat_n(S), 0.9, B.Z(S), t, 0.05, 0.1, alpha=np.clip(a, 0, 1))


# ================================================================================================ the table
ATL = ("TEXT ATLAS, not world-scale (as jp_m_decal_carved_text): map a face onto one cell's rectangle (\"cells\": "
       "u0, v0, u1, v1 with v down), keeping the cell's aspect; 1024 px = 1 m. Three-column cells carry \"crops\" "
       "(fractions of the cell): NAME = the kaimyo column only, DATE_R = the era-year column, DATE_L = month and "
       "day. Lay the decal 2-3 mm off the surface; never in Geometry/View/Fire. Text runs top to bottom, columns "
       "right to left.")


def table():
    WP = ("wood", "dz\\surfaces\\data\\roadway\\wood_planks_ext.paa")
    return [
        (B.M("jp_m_ground_earth_bare", "ground", "earth_bare", 2.0, 1024, ground_earth_bare, (0.06, 12), "dirt",
             "dirt_ext", "none; crumb, pebbles, roots", uv=B.WORLD, srcs=["clay_floor_001"], where="outdoor",
             note="Bare outdoor earth (grave mounds, worn paths, yards). Same tile and layout as jp_m_ground_leaf_litter "
                  "(2 m), so a mound can swap one for the other."),
         {"_w0": "fresh-heaped, moist and darker, loose clods (a new grave mound)",
          "_w1": "settled dry earth, crumb and pebbles", "_w2": "overgrown: moss and weeds creeping in, wet leaves, "
                                                                "rain rills"},
         ["jp_s_grave_stones", "jp_s_grave_wood"], "Grave mounds, worn paths, bare yard ground"),
        (B.M("jp_m_wood_new", "wood", "wood_new_cut", 2.0, 1024, wood_new, (0.15, 30), WP[0], "wood_planks_ext",
             "along v (member length), fine straight grain", uv=B.WORLD, srcs=["hinoki_planks"], where="outdoor",
             note="Pale NEW sugi / hinoki. Same tile and grain direction as jp_m_wood_weathered (2 m, grain along v) "
                  "so props swap material without new UVs."),
         {"_w0": "fresh-split / planed, pale cream-tan", "_w1": "a season old: warmer, first dirt",
          "_w2": "a year or two: the surface starting to grey, dirt splash, first checks"},
         ["jp_s_grave_wood"], "New wood: fresh grave posts, new repairs"),
        (B.M("jp_m_wood_silver", "wood", "wood_silver_grey", 2.0, 1024, wood_silver, (0.12, 25), WP[0],
             "wood_planks_ext", "along v (member length), raised weathered grain", uv=B.WORLD,
             srcs=["weathered_planks"], where="outdoor",
             note="True silver-grey weathered wood. Same tile, scan and grain as jp_m_wood_weathered (which is the warm "
                  "brown of wet facades: keep it there)."),
         {"_w0": "silver-grey, raised grain", "_w1": "dark weather streaks, pale lichen",
          "_w2": "old and damp: darker, splits, green-black algae"},
         ["jp_s_grave_wood"], "Old unpainted wood gone silver"),
        (B.M("jp_m_floor_tatami_heri_cha", "floor", "cha_koge", 1.0, 512, floor_tatami_heri_cha, (0.08, 15), "cloth",
             "textile_carpet_int", "plain hemp/cotton weave", uv=B.WORLD + "; the 0.03 m band may use any strip of v",
             srcs=["rough_linen"],
             note="Plain brown (cha) heri: A2's 'plain black or brown heri' second colour. Commoner-plain; patterned "
                  "(monberi) heri stay temple / elite only. Same layout as jp_m_floor_tatami_heri."),
         {"_w0": "even tea-brown", "_w1": "frayed threads along the edges", "_w2": "torn: the rush shows through"},
         ["floors (jpparts.floors)"], "Brown tatami edge for farmhouse / T2 best rooms"),
        (B.M("jp_m_decal_carved_text_grave", "stone", "stone_lantern", 1.0, 1024, decal_carved_text_grave,
             (0.15, 30), None, None, "none; V-cut inscriptions (Yuji Syuku)", alpha="decal", uv=ATL,
             srcs=["rock_surface"], where="outdoor", atlas_kind="carved_grave",
             note="Posthumous names (kaimyo) and death dates for gravestones: 13 cells, 14 names (one couple stone), "
                  "dates Kanbun 10 (1670) to Kyoho 14 (1729). Commoner forms only: -shinji / -shinnyo, -zenjomon / "
                  "-zenjoni, -doji / -donyo, Shin-sect shaku-; no family names (Meiji). Fonts: SIL OFL 1.1, Yuji "
                  "Project Authors."),
         {"_w0": "crisp cut", "_w1": "softened, grime in the cuts", "_w2": "lichen over half the text"},
         ["jp_s_grave_stones"], "Carved posthumous names for gravestones"),
        (B.M("jp_m_decal_sumi_text_grave", "paint", "sumi_black", 1.0, 1024, decal_sumi_text_grave, (0.05, 10), None,
             None, "brush strokes (Yuji Syuku kanji)", alpha="decal", uv=ATL, where="outdoor",
             atlas_kind="sumi_grave",
             note="Posthumous names in ink for wooden grave posts (bohyo): 6 cells, Kyoho 9 (1724) to Kyoho 15 (1730). "
                  "_w0 = a new post's crisp ink; _w1 faded; _w2 a ghost. Fonts: SIL OFL 1.1, Yuji Project Authors."),
         {"_w0": "crisp black ink (a new post)", "_w1": "faded to grey-brown", "_w2": "ghost of text, flaking"},
         ["jp_s_grave_wood"], "Ink posthumous names for grave posts"),
        (B.M("jp_m_wicker_aged", "bamboo", "wicker_aged", 0.5, 256, wicker_aged, (0.15, 40), "wood", None,
             "2/2 twill of ~1.5 cm strips", uv=B.WORLD, srcs=["bamboo_wall"],
             note="Warm wicker for kori trunks (same twill and tile as jp_m_bamboo_weave, which stays for the props "
                  "that want grey, sun-bleached bamboo)."),
         {"_w0": "warm honey-tan wicker", "_w1": "handled, grime on the strip crowns",
          "_w2": "broken strips, mildew"},
         ["jp_f_kori"], "Kori wicker trunks"),
        (B.M("jp_m_wood_firewood", "wood", "firewood_split", 2.0, 1024, wood_firewood, (0.12, 25), WP[0], None,
             "along v (billet length): split facets and bark strips", uv=B.WORLD, srcs=["weathered_planks"],
             note="Split firewood sides (i22). For firewood only; the log ends are jp_m_wood_endgrain_firewood."),
         {"_w0": "fresh-split tan faces, grey bark", "_w1": "seasoned a year, greyer",
          "_w2": "old and damp, pale mould"},
         ["jp_f_firewood", "jp_s_firewood_stack"], "Split firewood"),
        (B.M("jp_m_wood_endgrain_firewood", "wood", "firewood_end", 0.5, 256, wood_endgrain_firewood, (0.15, 30),
             WP[0], None, "growth rings, bark ring, radial checks",
             uv="NOT tileable: one 0.5 m log end, pith at (0.5, 0.5); map a disc of the log's diameter centred there "
                "(as jp_m_wood_endgrain)"),
         {"_w0": "fresh-cut pale end", "_w1": "seasoned: checks open, greyer", "_w2": "old: dark checks, grey"},
         ["jp_f_firewood", "jp_s_firewood_stack"], "Firewood log ends"),
    ]


def setup_atlases():
    B._ATLAS["carved_grave"] = grave_layout("carved_grave")
    B._ATLAS["sumi_grave"] = grave_layout("sumi_grave")


def draft(only):
    """Textures only, to spikes/M1/draft/ (the palette entries are put into MT.PAL in memory, not written)."""
    os.makedirs(DRAFT, exist_ok=True)
    for e in ENTRIES:
        MT.PAL[e["id"]] = dict(e)
    pal = B.matcheck.load_palette()
    for e in ENTRIES:
        pal[e["id"]] = dict(e)
    MT.PAL.update({k: v for k, v in pal.items() if k not in MT.PAL})
    setup_atlases()
    for m, wear, used_by, note in table():
        if only and m["id"] not in only:
            continue
        for lv in range(3):
            r = m["maker"](lv, m["S"])
            mask = np.asarray(r["mask"], bool)
            co = MT.fix_mean(np.clip(r["co"], 0, 1).astype(f32), r["target"], ~mask)
            stem = os.path.join(DRAFT, "%s_w%d" % (m["id"], lv))
            if r.get("alpha") is not None:
                B.save(stem + "_ca.png", np.concatenate([co, np.clip(r["alpha"], 0, 1)[..., None]], -1))
            else:
                B.save(stem + "_co.png", co)
            print("draft", os.path.basename(stem), "mean", (co.reshape(-1, 3).mean(0) * 255).round())


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    if "--draft" in argv:
        draft(only)
        return 0
    added = add_palette()
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    setup_atlases()
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        if only and mid not in only:
            continue
        B.MATS.append(m)
        B.BYID[mid] = m
        B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by, "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"][-1] = {"procedural": "make_m1_materials.py (on make_b1_materials.make_one)"}
        sc["made_by"] = "research/materials/make_m1_materials.py (agent M1, 2026-09-30), through B1's make_one"
        sc["requested_by"] = "PRODUCTION_PLAN.md 'Confirmed future work' (W2 / W3 / B3a material gaps)"
        if m["atlas"]:
            sc["fonts"] = ["research/fonts/yujisyuku/YujiSyuku-Regular.ttf (SIL OFL 1.1, Yuji Project Authors)"]
            sc["text_sources"] = "spikes/M1/M1_PROGRESS.md 'Text': kaimyo forms, ranks and era dates, each checked"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-40s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_m1.json"), json.dumps({"check": "C1 palette (tools/matcheck), M1 materials",
                                                           "palette_entries_added": added, "results": allres},
                                                          indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("M1 materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
