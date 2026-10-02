#!/usr/bin/env python3
r"""make_fp1_materials.py - FP1 (Stephen's showcase walk, 2026-10-01): material fixes and additions through B1's pipeline.

  python make_fp1_materials.py [--no-pack] [--only ID[,ID...]]

Route of make_l2_materials.py / make_m1_materials.py: B1's make_one (textures, PAAs, rvmats, sidecar, C1 matcheck on
the PNG and the shipped PAA), then jp_common.pbo is repacked. Results: src/JP/common/materials/checks_fp1.json.

REDRAWN (same id, same paths, so every model that uses them changes without a rebuild):
- jp_m_decal_litter     Stephen: leaf litter showed "orange dots", and under the fallen lantern the decal read as a
                        clear plastic sheet. Cause: B1's atlas drew leaves as round spots (MT.spots) and laid a soft
                        semi-transparent dust haze (alpha 0.35, 20-30 % of the pixels between 16 and 240) under them;
                        the decal rvmat is NoZWrite (blended), so that haze drew as a filmy sheet. Now: real autumn
                        leaf shapes (iroha maple, ginkgo, konara oak, yamazakura cherry, old brown leaves) in varied
                        sizes, rotations and colours, drifting in clumps, plus straw bits, paper scraps and shards;
                        alpha is cut (0 / 1 with a 1 px edge), no haze. Palette id leaf_litter_autumn (it is a leaf
                        decal now; grime_splash was the dust).
- jp_m_decal_moss       the same check on the other ground / stone decal: its soft alpha ramps (10-16 % of the pixels
                        semi-transparent) are hardened to a 1-2 px edge; colours unchanged.
NEW:
- jp_m_wall_shikkui_aged  aged exterior lime plaster for FB1's kura (the white kura looked brand-new and too bright):
                        sampled from c25 (a decades-old tile-and-plaster wall, three sunlit plaster patches) and c03
                        (Tsumago, an old maintained wall), each reference weighing the same -> palette
                        shikkui_aged [162,163,159] (spikes/FP1/sample_aged.py). Rain streaks from the top (v = 0 at the
                        top of a storey-high wall), splash grime at the foot, grey blotches, hairline cracks at _w2.
- jp_m_stone_carved_aged  the stone torii / lantern stone without the repeating lichen dots (Stephen: the stone
                        torii's lichen dots repeat in a pattern): a 2.0 m tile at 1024 px (stone_carved is 1 m at 512),
                        lichen as irregular rosettes of two kinds at several scales (fbm-cut, never round dots), a
                        broad weathering cloud and rain darkening; the models also turn and shift the UVs per piece
                        (spikes/B3b/w2kit.aged_stone).
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

PAL = os.path.join(DEV, "playbook", "palette.json")
f32 = np.float32
ENTRIES = [
    {"id": "shikkui_aged", "name": "Shikkui lime plaster, aged and weathered (greyed, rain-stained)",
     "material": "old exterior lime plaster (shikkui) on kura and walls after decades of rain", "group": "wall",
     "tiers": [2, 3], "use": "jp_m_wall_shikkui_aged: kura and plastered walls in the dead world",
     "note": "Added 2026-10-01 by FP1. Each reference weighs the same: c25 (mean of 3 sunlit plaster patches "
             "between the tile courses: 137,132,119 / 122,118,104 / 137,133,121) and c03 (193,198,203, B1's "
             "shikkui box). spikes/FP1/sample_aged.py.",
     "srgb": [162, 163, 159], "method": "sampled", "tolerance_dE76": 14,
     "samples": [{"ref": "c25_tsuijibei", "box": [0.755, 0.39, 0.80, 0.44], "select": "mid 70 % luminance"},
                 {"ref": "c25_tsuijibei", "box": [0.67, 0.18, 0.71, 0.21], "select": "mid 70 % luminance"},
                 {"ref": "c25_tsuijibei", "box": [0.61, 0.50, 0.66, 0.54], "select": "mid 70 % luminance"},
                 {"ref": "c03_tsumago_street", "box": [0.79, 0.33, 0.86, 0.45], "select": "mid 70 % luminance"}]},
    {"id": "earthenware_unglazed", "name": "Unglazed earthenware (suyaki flower pots), dull red-brown",
     "material": "low-fired unglazed clay pots (ueki-bachi)", "group": "ceramic", "tiers": [1, 2, 3],
     "use": "jp_m_ceramic_earthenware: flower pots and bonsai pots (LIFE_LAYER_ERA #58: unglazed pots only)",
     "note": "Added 2026-10-01 by FP1. Assumed (general knowledge, no local photo of an Edo flower pot): a dull "
             "red-brown low-fired body, darker than roof-tile clay, lighter than stoneware_dark. Judge in game.",
     "srgb": [134, 98, 74], "method": "assumed", "tolerance_dE76": 12},
    {"id": "kiku_flower", "name": "Chrysanthemum flower heads (white, yellow, rust), mean of the atlas",
     "material": "kiku petals", "group": "plant", "tiers": [2, 3],
     "use": "jp_m_plant_kiku: the potted chrysanthemums (Kyoho kiku fashion, LIFE_LAYER_ERA #58)",
     "note": "Added 2026-10-01 by FP1. Assumed: three classic Edo kiku colours (white, yellow, rust-red) side by "
             "side in u; the entry is their mean. Judge in game.",
     "srgb": [196, 160, 104], "method": "assumed", "tolerance_dE76": 14},
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
            f.write(json.dumps(pal, indent=1, ensure_ascii=False).encode("utf-8"))
    return added


# ================================================================================================ leaf shapes
def _rot(pts, a, x, y, s):
    c, sn = math.cos(a), math.sin(a)
    return [(x + s * (px * c - py * sn), y + s * (px * sn + py * c)) for px, py in pts]


def leaf_maple(rg):
    """Iroha-momiji: palmate, 7 pointed lobes spread over ~290 degrees, deep sinuses; petiole at the origin, the
    leaf along +x, size ~1 (the radius of the longest lobe)."""
    lobes = [(-2.4, 0.42), (-1.65, 0.68), (-0.85, 0.88), (0.0, 1.0), (0.85, 0.88), (1.65, 0.68), (2.4, 0.42)]
    pts = []
    n = 70
    cx = 0.30                                   # the lobes radiate from a point a little up the blade
    for k in range(n):
        th = -math.pi + 2 * math.pi * (k + 0.5) / n
        r = 0.28
        for a, L in lobes:
            d = abs((th - a + math.pi) % (2 * math.pi) - math.pi)
            w = 0.44
            if d < w:
                r = max(r, 0.28 + (L * 0.72 - 0.28) * (1 - d / w) ** 0.75)
        r *= 1 + 0.05 * rg.uniform(-1, 1)        # the fine teeth
        pts.append((cx + r * math.cos(th), r * math.sin(th)))
    return pts, [(0.0, 0.0), (cx, 0.0)], [[(cx, 0.0), (cx + 0.68 * math.cos(a), 0.68 * math.sin(a))]
                                          for a in (-1.65, -0.85, 0.0, 0.85, 1.65)]


def leaf_ginkgo(rg):
    """Ginkgo: a fan on a long petiole, the outer edge wavy with a central notch."""
    pts = [(0.30, 0.0)]
    n = 26
    for k in range(n + 1):
        th = -1.05 + 2.1 * k / n
        r = 0.95 * (1 - 0.22 * math.exp(-(th / 0.10) ** 2)) * (1 + 0.035 * math.sin(th * 23 + rg.uniform(0, 6)))
        pts.append((0.30 + r * math.cos(th), r * math.sin(th)))
    return pts, [(-0.15, 0.0), (0.30, 0.0)], []


def _blade(rg, L, W, p, lobes=0, lobe_amp=0.0, teeth=0, tooth_amp=0.0, tip=0.8):
    """An oblong leaf blade along +x from 0 to L: half-width W * sin(pi t)^p (t along), lobes / teeth on the edge."""
    up, dn = [], []
    n = 40
    for k in range(n + 1):
        t = k / n
        w = W * math.sin(math.pi * t ** tip) ** p
        if lobes:
            w *= 1 + lobe_amp * math.sin(math.pi * lobes * t) ** 2 - lobe_amp * 0.5
        if teeth:
            w *= 1 + tooth_amp * ((k % 2) * 2 - 1)
        up.append((L * t, w))
        dn.append((L * t, -w * (1 + 0.04 * rg.uniform(-1, 1))))
    return up + dn[::-1][1:-1]


def leaf_oak(rg):
    pts = _blade(rg, 1.0, 0.30, 0.8, lobes=6, lobe_amp=0.35, tip=0.75)
    return pts, [(-0.12, 0.0), (0.9, 0.0)], []


def leaf_cherry(rg):
    pts = _blade(rg, 1.0, 0.27, 0.9, teeth=1, tooth_amp=0.05, tip=1.25)
    return pts, [(-0.20, 0.0), (0.92, 0.0)], []


def leaf_old(rg):
    """An old brown leaf, curled: a narrow ellipse, one side rolled in (shorter)."""
    pts = _blade(rg, 1.0, 0.24, 0.85, tip=1.0)
    pts = [(x, y * (0.55 if y < 0 else 1.0)) for x, y in pts]
    return pts, [(-0.08, 0.0), (0.9, 0.0)], []


# (shape, weight, size range in px at 512 px/m, colours sRGB): sizes from the leaves' real lengths (maple 5-8 cm
# across, ginkgo 5-7, konara 7-11, cherry 7-10, old leaves 4-8), colours dulled for leaves weeks on a floor
KINDS = [
    (leaf_maple, 0.30, (24, 34), [(150, 48, 30), (172, 76, 36), (128, 42, 32), (160, 96, 42), (112, 58, 36)]),
    (leaf_ginkgo, 0.16, (20, 28), [(196, 158, 58), (182, 140, 52), (170, 128, 60)]),
    (leaf_oak, 0.20, (36, 56), [(122, 88, 52), (104, 74, 46), (138, 100, 58)]),
    (leaf_cherry, 0.18, (34, 50), [(160, 74, 40), (138, 62, 40), (176, 104, 50), (120, 74, 44)]),
    (leaf_old, 0.16, (22, 40), [(92, 68, 46), (80, 62, 46), (104, 82, 58)]),
]


def leaves_layer(S, n, seed, density=None):
    """Draw n leaves (wrapping) into an RGB + coverage pair. density: an S x S array 0-1; leaves are placed by
    rejection against it (drifts)."""
    rg = np.random.default_rng(seed)
    import random
    rr = random.Random(seed)
    col = B.MT.Wrap(S, "RGB", (0, 0, 0))
    cov = B.MT.Wrap(S)
    shade = B.MT.Wrap(S)
    vein = B.MT.Wrap(S)
    wts = np.array([k[1] for k in KINDS])
    wts = wts / wts.sum()
    placed = 0
    tries = 0
    while placed < n and tries < n * 40:
        tries += 1
        x, y = rg.uniform(0, S, 2)
        if density is not None and rg.random() > density[int(y) % S, int(x) % S]:
            continue
        kind = KINDS[rg.choice(len(KINDS), p=wts)]
        pts, stem, veins = kind[0](rr)
        s = rg.uniform(*kind[2])
        a = rg.uniform(0, 2 * math.pi)
        c = np.array(kind[3][rg.integers(len(kind[3]))], f32) * rg.uniform(0.85, 1.12)
        c = tuple(int(v) for v in np.clip(c, 0, 255))
        poly = _rot(pts, a, x, y, s)
        col.polygon(poly, c)
        cov.polygon(poly, 255)
        # one half of the blade a little darker (the leaf is not flat): the half on one side of the midrib
        half = [p for p in pts if p[1] >= 0]
        if len(half) > 2:
            shade.polygon(_rot(half + [(pts[0][0], 0.0)], a, x, y, s), int(rg.uniform(30, 90)))
        dark = tuple(int(v * 0.62) for v in c)
        st = _rot(stem, a, x, y, s)
        col.line(st, dark, 1)
        cov.line(st, 255, 1)
        vein.line(st, 255, 1)
        for v in veins:
            vein.line(_rot(v, a, x, y, s), 160, 1)
        placed += 1
    return col.arr(), cov.arr(), shade.arr(), vein.arr()


def decal_litter(lv, S):
    """FP1 redraw: autumn leaves (shapes, sizes, rotations, colours), straw bits, paper scraps, shards; cut alpha."""
    MT, T = B.MT, B.T
    t = [T("leaf_litter_autumn", 4, 2, 2), T("leaf_litter_autumn"), T("leaf_litter_autumn", -6, -2, -4)][lv]
    drift = np.clip(MT.blur(MT.fbm(S, 2.6, 1, 1, 7101), 1.0) * 0.55 + [0.25, 0.40, 0.60][lv], 0.03, 1.0)
    rgb, cov, shade, vein = leaves_layer(S, [170, 380, 760][lv], 7102 + lv, density=drift)
    cov = cov > 0.5
    co = np.where(cov[..., None], rgb, (np.asarray(t, f32) / 255.0)[None, None, :])
    co = co * (1 - 0.25 * shade)[..., None]
    co = co * (1 - 0.30 * vein)[..., None]
    if lv >= 1:                                                   # older leaves greyed by dust and damp
        co = MT.mix(co, MT.grey(co, 1.0), np.full((S, S), [0, 0.18, 0.32][lv], f32) * cov)
    sa, st = MT.straw_flecks(S, [160, 300, 480][lv], 7103, 12, 44)
    sa = sa > 0.5
    co = MT.mix(co, (170, 146, 98), sa * (0.75 + 0.25 * st))
    pa = B.polys(S, [5, 10, 16][lv], 7104, 10, 26, 4) > 0.5             # paper scraps (detail: masked)
    co = MT.mix(co, (186, 178, 160), pa.astype(f32))
    sh = B.polys(S, [3, 8, 14][lv], 7105, 4, 12, 5) > 0.5              # pottery shards (masked)
    co = MT.mix(co, (90, 72, 58), sh.astype(f32))
    grit = MT.spots(S, [30, 60, 120][lv], 6, 0.6, 1.4, 25, 7106) > 0.5  # a little grit (1-2 px: below a 'dot')
    co = MT.mix(co, (78, 68, 58), grit.astype(f32) * 0.9)
    a = (cov | sa | pa | sh | grit).astype(f32)
    a = np.clip(MT.blur(a, 0.5) * 1.6 - 0.3, 0, 1)                  # cut, with a 1 px edge for the mip
    mask = pa | sh
    h = MT.blur(cov.astype(f32), 1.5) * 2.0 + sa * 1.0 + pa * 0.5 - vein * 0.6
    return B.R(np.clip(co, 0, 1), MT.h2n(h.astype(f32), 1.2), 0.92, mask, t, 0.04, 0.08, alpha=a)


def decal_moss(lv, S):
    """B1's moss decal with its alpha hardened (1-2 px edge): no semi-transparent film."""
    r = B.decal_moss(lv, S)
    a = np.asarray(r["alpha"], f32)
    r["alpha"] = np.clip((a - 0.45) * 5.0 + 0.5, 0, 1)
    return r


# ================================================================================================ aged plaster
def wall_shikkui_aged(lv, S):
    """Old exterior lime plaster (v = 0 at the top of a storey-high wall, 2.0 m tile): the clean shikkui photo
    recoloured to the sampled aged value, rain streaks running down from the top, a grime band at the foot, grey
    blotches where the lime has gone; _w1 a few hairline cracks, _w2 cracks and a flaked patch showing the earth."""
    MT, T = B.MT, B.T
    t = [T("shikkui_aged", 6, 0, 0), T("shikkui_aged"), T("shikkui_aged", -6, 0.5, 2.0)][lv]
    r0 = MT.wall_shikkui(0, S)
    co = MT.recolor(r0["co"], t, 1.5, 0.15)
    yy, xx = B.grid(S)
    y01 = yy / S
    streak = np.clip(MT.vstreaks(S, 7201, 1.0, 18), 0, 1.4) * np.clip(1.15 - y01 * 0.6, 0.3, 1.2)
    co = co * (1 - [0.08, 0.13, 0.17][lv] * streak)[..., None]
    foot = np.clip((y01 - 0.78) / 0.22, 0, 1) * (0.7 + 0.3 * MT.fbm(S, 2.0, 1, 1, 7202))
    co = MT.mix(co, (118, 108, 92), foot * [0.18, 0.30, 0.42][lv])
    blot = B.blobs(S, 7203, [1.5, 1.2, 0.95][lv], 2.8, 3)
    co = MT.patch(co, blot, (138, 138, 132), 0.35, 7204)
    mask = blot.copy()
    h = np.zeros((S, S), f32)
    if lv >= 1:
        c = MT.cracks(S, [0, 10, 26][lv], 7205, seg=(4, 9), jitter=0.55)
        co = MT.mix(co, (104, 98, 90), c * 0.6)
        h -= c * 1.5
        mask |= c > 0.3
    if lv == 2:                                                   # lime flaked off: the earth coat below
        fl = B.blobs(S, 7206, 1.55, 2.6, 2)
        co = MT.patch(co, fl, (132, 112, 84), 0.85, 7207)
        h -= fl * 1.2
        mask |= fl
    return B.R(np.clip(co, 0, 1), MT.combine(r0["n"], MT.h2n(h, 1.0)), r0["rough"], mask, t, r0["spec"], r0["gloss"])


# ================================================================================================ aged carved stone
def _lichen(S, seed, cover, scale_beta):
    """Irregular lichen rosettes: an fbm field thresholded, with a ragged (second fbm) edge; never round."""
    MT = B.MT
    f = MT.fbm(S, scale_beta, 1, 1, seed) + 0.35 * MT.fbm(S, 1.2, 1, 1, seed + 1)
    return (f > cover)


def stone_carved_aged(lv, S):
    MT, T = B.MT, B.T
    t = [T("stone_lantern", 5), T("stone_lantern", 0), T("stone_lantern", -3)][lv]
    a = MT.photo("rock_surface", "diff", S, tiles=2)
    co = MT.recolor(a, t, 1.0, 0.3)
    pn = MT.pnormal("rock_surface", S, tiles=2, k=0.6)
    rough = MT.prough("rock_surface", S, 2)
    cloud = MT.fbm(S, 2.8, 1, 1, 7301)                        # the broad weathering cloud (breaks the photo repeat)
    co = co * (1 + 0.10 * cloud)[..., None]
    yy, _ = B.grid(S)
    rain = np.clip(MT.vstreaks(S, 7302, 1.0, 10), 0, 1.4)
    co = co * (1 - [0.04, 0.08, 0.12][lv] * rain)[..., None]
    mask = B.Z(S)
    if lv >= 0:
        big = _lichen(S, 7303, [1.55, 1.15, 0.95][lv], 2.4)            # pale grey-green foliose patches
        small = _lichen(S, 7305, [1.75, 1.45, 1.25][lv], 1.6)          # yellow-ochre crustose, smaller and finer
        co = MT.patch(co, big, (168, 170, 146), 0.55, 7304)
        co = MT.patch(co, small & ~big, (184, 158, 98), 0.45, 7306)
        dark = _lichen(S, 7307, [1.9, 1.6, 1.3][lv], 1.9)              # black lichen
        co = MT.patch(co, dark & ~big, (40, 40, 36), 0.45, 7308)
        mask = big | small | dark
    if lv == 2:
        mo = MT.blur((MT.fbm(S, 2.4, 1, 1, 7309) > 1.0).astype(f32), 2) > 0.5
        co = MT.patch(co, mo, (70, 84, 40), 0.85, 7310)
        mask |= mo
    return B.R(np.clip(co, 0, 1), pn, rough, mask, t, 0.2, 0.3)


# ================================================================================================ pots and flowers
def ceramic_earthenware(lv, S):
    """Unglazed low-fired clay (suyaki): matte red-brown body, fine throwing rings round the pot (along u), fire
    clouding (darker smoke patches), grit; _w1 dusty with lime bloom, _w2 green-black damp at the foot and chipped."""
    MT, T = B.MT, B.T
    t = [T("earthenware_unglazed", 2), T("earthenware_unglazed"), T("earthenware_unglazed", -4, -2, -3)][lv]
    yy, xx = B.grid(S)
    ridge = np.sin(2 * math.pi * (yy * 40 / S + 0.15 * MT.fbm(S, 2.0, 1, 1, 7401)))
    co = B.base(t, 1 + 0.07 * MT.fbm(S, 2.4, 1, 1, 7402) + 0.03 * ridge)
    smoke = np.clip(MT.fbm(S, 2.6, 1, 1, 7403) - 0.6, 0, 1)
    co = MT.mix(co, (74, 58, 50), smoke * 0.55)
    grit = MT.spots(S, 160, 3, 0.5, 1.2, 25, 7404)
    co = MT.mix(co, (196, 176, 150), grit * 0.4)
    h = ridge * 0.6 + grit * 0.4
    mask = B.Z(S)
    if lv >= 1:                                                   # lime bloom / dust
        bloom = np.clip(MT.fbm(S, 2.2, 1, 3, 7405) - 0.5, 0, 1)
        co = MT.mix(co, (176, 166, 150), bloom * [0, 0.35, 0.45][lv])
        mask |= bloom > 0.4
    if lv == 2:                                                   # damp algae at the foot (v = 0 at the rim), chips
        foot = np.clip((yy / S - 0.6) / 0.4, 0, 1) * np.clip(0.6 + 0.5 * MT.fbm(S, 2.0, 1, 1, 7406), 0, 1)
        co = MT.mix(co, (52, 62, 44), foot * 0.6)
        chips = B.polys(S, 6, 7407, 3, 8, 6) > 0.5
        co = MT.mix(co, (170, 130, 100), chips.astype(f32))
        mask |= (foot > 0.3) | chips
    return B.R(np.clip(co, 0, 1), MT.h2n(h.astype(f32), 1.0), 0.9, mask, t, 0.05, 0.1)


def plant_kiku(lv, S):
    """Chrysanthemum heads, three colour columns in u (0-1/3 white, 1/3-2/3 yellow, 2/3-1 rust): v = 0 the flower
    centre, v = 1 the petal tips; narrow ray petals along v with dark gaps, a green-yellow disc at v < 0.12. _w1 a
    little faded, _w2 withered brown (dead, as left)."""
    MT, T = B.MT, B.T
    t = [T("kiku_flower", 3), T("kiku_flower"), T("kiku_flower", -8, -3, -8)][lv]
    yy, xx = B.grid(S)
    u, v = xx / S, yy / S
    cols = [np.array(c, f32) / 255 for c in ((226, 220, 200), (214, 172, 60), (150, 62, 40))]
    band = np.clip((u * 3).astype(int), 0, 2)
    base_c = np.stack([cols[0], cols[1], cols[2]])[band]
    petals = 0.5 + 0.5 * np.cos(2 * math.pi * (u * 3 * 14 + 0.25 * MT.fbm(S, 2.0, 1, 1, 7501)))
    co = base_c * (0.70 + 0.30 * petals)[..., None] * (0.85 + 0.15 * v)[..., None]
    disc = np.clip((0.14 - v) / 0.05, 0, 1)
    co = MT.mix(co, (150, 140, 60), disc * 0.9)
    if lv >= 1:
        co = MT.mix(co, MT.grey(co, 1.0), np.full((S, S), [0, 0.12, 0.6][lv], f32))
    if lv == 2:
        co = MT.mix(co, (104, 78, 52), np.full((S, S), 0.55, f32))
    h = petals * 0.8 + disc * 0.5
    return B.R(np.clip(co, 0, 1), MT.h2n(h.astype(f32), 1.0), 0.85, B.Z(S), t, 0.05, 0.1)


def table():
    lit = dict(B.BYID["jp_m_decal_litter"])
    lit.update({"maker": decal_litter, "pid": "leaf_litter_autumn",
                "grain": "none; autumn leaves (maple, ginkgo, oak, cherry, old brown), straw bits, paper scraps, shards"})
    moss = dict(B.BYID["jp_m_decal_moss"])
    import make_wood_atlas as WA          # FX3 (2026-10-01): irregular drifts, 2 m at 1024 px (Stephen: "too regular")
    moss.update({"maker": WA.moss_b1, "tile": 2.0, "tile_v": 2.0, "px": (1024, 1024), "S": 1024})
    return [
        (lit, {"_w0": "a few leaves blown in", "_w1": "leaves drifting in corners", "_w2": "a thick leaf drift, greyed"},
         None, "FP1 redraw: leaf shapes, cut alpha (was round dots over a soft haze)"),
        (moss, None, None, "FP1: alpha hardened (no semi-transparent film)"),
        (B.M("jp_m_wall_shikkui_aged", "wall", "shikkui_aged", 2.0, 1024, wall_shikkui_aged,
             B.BM.SPEC["jp_m_wall_shikkui"], "dirt", None, "none; trowel",
             uv=B.WORLD + "; v = 0 at the top of a storey-high wall (rain streaks from the top, grime at the foot)",
             srcs=["white_plaster_02"], where="outdoor",
             note="Aged exterior shikkui for kura and plastered walls in the dead world (FP1 2026-10-01, for FB1's "
                  "kura). Same photo as jp_m_wall_shikkui, recoloured to the sampled shikkui_aged."),
         {"_w0": "old, evenly greyed", "_w1": "rain streaks, grime at the foot, hairline cracks",
          "_w2": "heavy streaks, cracks, lime flaked off to the earth coat"},
         ["FB1 kura"], "Kura and plastered walls, aged"),
        (B.M("jp_m_stone_carved_aged", "stone", "stone_lantern", 2.0, 1024, stone_carved_aged, (0.2, 40), "granite",
             "stone_ext", "none; weathered granite with lichen rosettes", uv=B.WORLD + "; turn and shift per piece",
             srcs=["rock_surface"], where="outdoor",
             note="Stone torii and lanterns (FP1 2026-10-01): a 2 m tile so the lichen never repeats on one piece; "
                  "lichen as irregular rosettes, not dots."),
         {"_w0": "pale lichen here and there", "_w1": "lichen rosettes, rain darkening",
          "_w2": "heavy lichen and moss"},
         ["jp_s_torii_stone", "jp_s_stone_lantern"], "Stone torii and lanterns, weathered"),
        (B.M("jp_m_ceramic_earthenware", "ceramic", "earthenware_unglazed", 0.5, 256, ceramic_earthenware, (0.05, 10),
             "pottery", None, "throwing rings round the pot (u), v = 0 at the rim", uv=B.WORLD + "; u round the pot",
             where="outdoor", note="Unglazed suyaki flower and bonsai pots (FP1 2026-10-01; era: no glazed trays)."),
         {"_w0": "clean red-brown", "_w1": "dusty, lime bloom", "_w2": "damp and green at the foot, chipped"},
         ["jp_s_potted"], "Unglazed flower pots"),
        (B.M("jp_m_plant_kiku", "plant", "kiku_flower", 0.5, 256, plant_kiku, (0.05, 10), "cloth", None,
             "ray petals along v (centre v = 0 -> tips v = 1), three colour columns in u",
             uv="ATLAS: u 0-1/3 white, 1/3-2/3 yellow, 2/3-1 rust; map a flower head's faces into one column, "
                "v from the centre (0) out to the petal tips (1)", where="outdoor",
             note="Potted chrysanthemum heads (FP1 2026-10-01)."),
         {"_w0": "fresh", "_w1": "a little faded", "_w2": "withered brown (dead)"},
         ["jp_s_potted"], "Chrysanthemum flower heads"),
    ]


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    added = add_palette()
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        if only and mid not in only:
            continue
        if mid not in B.BYID or B.BYID[mid] is not m:
            if mid not in B.BYID:
                B.MATS.append(m)
            B.BYID[mid] = m
        if wear:
            B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by or B.NEED.get(mid, {}).get("used_by", []),
                           "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"][-1] = {"procedural": "make_fp1_materials.py (on make_b1_materials.make_one)"}
        sc["made_by"] = "research/materials/make_fp1_materials.py (agent FP1, 2026-10-01), through B1's make_one"
        sc["fp1_note"] = note
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-40s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_fp1.json"), json.dumps({"check": "C1 palette (tools/matcheck), FP1 materials",
                                                            "palette_entries_added": added, "results": allres},
                                                           indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("FP1 materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
