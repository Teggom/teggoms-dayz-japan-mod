#!/usr/bin/env python3
r"""make_b1_materials.py - Phase B1 (2026-09-29): the interior and outdoor-kit materials of jp_common.

  python make_b1_materials.py [--only ID[,ID...]] [--set interior|outdoor] [--no-pack] [--no-render] [--sheets-only]
  python make_b1_materials.py --rvmats-only [--no-pack]
  python make_b1_materials.py --status          (rewrite B1_STATUS.md only)

What it makes (from research/interior/materials_needed.json (A2) and research/outdoor_kit/materials_needed.json (A3),
both accepted at gate G1): 21 interior materials and 11 of the 13 outdoor-kit materials, 3 wear levels each (_w0 clean,
_w1 normal, _w2 heavy / abandoned). Same layout as the library (build_materials.py) and the fix materials:
  data/materials/textures/<id>_w<n>_{co,nohq,smdi}.png (+ _ca.png for alpha materials, + _mask.png painted detail)
  src/JP/common/materials/<family>/<id>_w<n>_{co|ca,nohq,smdi}.paa, <id>_w<n>.rvmat, <id>.json (sidecar)
  src/JP/common/materials/checks_b1.json (C1 palette, tools/matcheck), then repacks @Japan\addons\jp_common.pbo
  research/materials/contact_sheets/b1_*.jpg, research/materials/B1_STATUS.md
Finish (PLAYBOOK §15.3 T12, build_materials.finish_for): matte everywhere; plaster walls the wall fresnel; glazed
stoneware and lacquer 'glazed' = fresnel(1.42,0) + env_land (the vanilla glazed-tile analogue).
Alpha: 'decal' = _ca + renderFlags NoZWrite (jp_m_wall_grime / vanilla decal_patch_floor pattern: moss, litter);
'cut' = _ca + renderFlags AlphaTest32 (vanilla ghillie / fur pattern: torn cloth, holed paper, reed gaps).
For every alpha material the RGB is a continuous material colour everywhere (alpha only sets coverage), so the palette
mean over the whole RGB is the mean of what shows (the grime rule).
Never starts or stops the server or any GUI program.
"""
import concurrent.futures as cf
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [HERE, os.path.join(DEV, "tools", "matcheck"), os.path.join(DEV, "tools", "common")]
import make_textures as MT  # noqa: E402
import build_materials as BM  # noqa: E402
import matcheck  # noqa: E402

TEX = MT.OUT
LIB = BM.MATDIR
SHEETS = BM.SHEETS
f32 = np.float32
NEED_INT = json.load(open(os.path.join(DEV, "research", "interior", "materials_needed.json"), encoding="utf-8"))
NEED_OUT = json.load(open(os.path.join(DEV, "research", "outdoor_kit", "materials_needed.json"), encoding="utf-8"))
NEED = {m["id"]: m for m in NEED_INT["materials"] + NEED_OUT["materials"]}
T = MT.tgt


# ================================================================================================ helpers
def _arr(im):
    return np.asarray(im).astype(f32) / 255.0


def _img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def ph_raw(asset, kind):
    return _arr(Image.open(os.path.join(MT.PH, asset, "%s_%s_1k.jpg" % (asset, kind))).convert("RGB"))


def fit(a, W, H=None):
    H = H or W
    if a.shape[1] == W and a.shape[0] == H:
        return a
    return _arr(_img(a).resize((W, H), Image.LANCZOS))


def src(asset, S, rot=False, roll=0, crop=None, tiles=1, kn=1.0):
    """Diffuse, DirectX normal and roughness of a Poly Haven asset at S x S. rot: turn 90 deg CCW (the normal vectors
    turn with it); roll: x shift (px of the turned 1k map) before crop = (x0, x1, y0, y1)."""
    out = []
    for kind in ("diff", "nor_dx", "rough"):
        a = ph_raw(asset, kind)
        if rot:
            a = np.rot90(a, 1).copy()
        if roll:
            a = np.roll(a, roll, axis=1)
        if crop:
            a = a[crop[2]:crop[3], crop[0]:crop[1]]
        a = fit(a, S // tiles)
        out.append(np.tile(a, (tiles, tiles, 1)))
    d, n, r = out
    n = n * 2.0 - 1.0
    if rot:                                                       # CCW: right -> up, down -> right (DX: +y = down)
        n = np.stack([n[..., 1], -n[..., 0], n[..., 2]], -1)
    return d, MT.flatten(n, kn), r[..., 0]


def joints(a, min_gap=20):
    """x positions of board joints (dark columns) in an image whose boards run along v."""
    c = MT.lum(a).mean(0)
    k = 7
    cs = np.convolve(np.r_[c[-k:], c, c[:k]], np.ones(k) / k, "same")[k:-k]
    thr = cs.mean() - 1.0 * cs.std()
    out = []
    for i in np.argsort(cs):
        if cs[i] > thr:
            break
        if all(min(abs(i - j), len(cs) - abs(i - j)) >= min_gap for j in out):
            out.append(int(i))
    return sorted(out)


def hinoki(S, scale=1.0):
    """Hinoki Planks (Poly Haven, 1.89 m) turned so the grain runs along v. scale > 1 widens the boards: the crop
    runs joint to joint (so the tile seam is a joint) over 1/scale of the width, then is stretched across."""
    if scale <= 1.0:
        return src("hinoki_planks", S, rot=True)
    a = np.rot90(ph_raw("hinoki_planks", "diff"), 1)
    W = a.shape[1]
    J = joints(a)
    want = W / scale
    best = None
    for j0 in J:
        for j1 in J + [x + W for x in J]:
            w = j1 - j0
            if w > 0 and (best is None or abs(w - want) < abs(best[1] - want)):
                best = (j0, w)
    j0, w = best
    return src("hinoki_planks", S, rot=True, roll=-j0, crop=(0, w, 0, a.shape[0]))


def grid(S):
    yy, xx = np.mgrid[0:S, 0:S]
    return yy.astype(f32), xx.astype(f32)


def base(t, val):
    return (np.asarray(t, f32) / 255.0)[None, None, :] * np.asarray(val, f32)[..., None]


def blobs(S, seed, thr, beta=3.0, soft=2.0, fx=1.0, fy=1.0):
    return MT.blur((MT.fbm(S, beta, fx, fy, seed) > thr).astype(f32), soft) > 0.5


def scratches(S, n, seed, lmin=20, lmax=90, ang=None, sd=0.15, width=1):
    w = MT.Wrap(S)
    rg = np.random.default_rng(seed)
    for _ in range(n):
        x, y = rg.uniform(0, S, 2)
        a = rg.uniform(0, math.pi) if ang is None else ang + rg.normal(0, sd)
        L = rg.uniform(lmin, lmax)
        w.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], 255, width)
    return w.arr()


def fibres(S, n, seed, ang, sd, lmin, lmax):
    """Directed fibre strokes: coverage and a random tone per stroke (straw, rush, rope fibres)."""
    w, tone = MT.Wrap(S), MT.Wrap(S)
    rg = np.random.default_rng(seed)
    for _ in range(n):
        x, y = rg.uniform(0, S, 2)
        a = ang + rg.normal(0, sd)
        L = rg.uniform(lmin, lmax)
        pts = [(x, y), (x + L * math.cos(a), y + L * math.sin(a))]
        w.line(pts, 255, 1)
        tone.line(pts, int(rg.uniform(120, 255)), 1)
    return w.arr(), tone.arr()


def ring_marks(S, n, seed, rmin, rmax, width=2):
    w = MT.Wrap(S)
    rg = np.random.default_rng(seed)
    for _ in range(n):
        x, y = rg.uniform(0, S, 2)
        r = rg.uniform(rmin, rmax)
        w.ellipse(x, y, r, r * rg.uniform(0.85, 1.0), None, 255, width)
    return MT.blur(w.arr(), 0.8)


def polys(S, n, seed, rmin, rmax, k=5):
    w = MT.Wrap(S)
    rg = np.random.default_rng(seed)
    for _ in range(n):
        cx, cy = rg.uniform(0, S, 2)
        a0 = rg.uniform(0, 2 * math.pi)
        pts = [(cx + rg.uniform(rmin, rmax) * math.cos(a0 + q), cy + rg.uniform(rmin, rmax) * math.sin(a0 + q))
               for q in np.linspace(0, 2 * math.pi, k + 1)[:-1]]
        w.polygon(pts, 255)
    return w.arr()


def weave_var(S, seed, amp=0.05):
    """Thread-scale variation of plain cloth (slubs along both thread directions) and a soft cloud."""
    return (amp * 0.7 * (MT.fbm(S, 1.2, 40, 1, seed) + MT.fbm(S, 1.2, 1, 40, seed + 1))
            + 0.03 * MT.fbm(S, 2.2, 1, 1, seed + 2))


def tide(S, seed, thr=1.4, beta=3.0, soft=3.0):
    """Irregular water-stain blotches and their tide-mark rims: (inside bool, rim 0-1)."""
    b = MT.blur((MT.fbm(S, beta, 1, 1, seed) > thr).astype(f32), soft)
    return b > 0.5, np.clip(1 - np.abs(b - 0.5) * 5, 0, 1)


def R(co, n, rough, mask, t, spec, gloss, alpha=None):
    S = co.shape[0]
    return {"co": co, "n": n, "rough": rough, "mask": np.zeros((S, S), bool) if mask is None else mask,
            "target": t, "spec": spec, "gloss": gloss, "alpha": alpha}


def Z(S):
    return np.zeros((S, S), bool)


# ================================================================================================ interior recipes
def floor_tatami(lv, S):
    a = ph_raw("tatami_mat", "diff")
    g = (a[..., 1] - a[..., 0]).mean(1)                           # the green heri rows of the scan
    band = g > g.mean() + 1.5 * g.std()
    best, i = (0, 0), 0
    while i < len(band):
        if band[i]:
            i += 1
            continue
        j = i
        while j < len(band) and not band[j]:
            j += 1
        if j - i > best[1] - best[0]:
            best = (i, j)
        i = j
    d, nn, r = src("tatami_mat", S, crop=(0, a.shape[1], best[0] + 6, best[1] - 6))   # one mat, heri cut off
    t = [T("tatami_aged", 8, -5, 6), T("tatami_aged"), T("tatami_aged", -3, 0, -2)][lv]
    co = MT.recolor(d, t, 1.0, 0.25)
    yy, xx = grid(S)
    h = np.zeros((S, S), f32)
    mask = Z(S)
    if lv >= 1:                                                   # worn lanes along the mat length (u)
        co = co * (1 - [0, 0.07, 0.05][lv] * np.clip(MT.fbm(S, 3.0, 8, 1, 1101), 0, 1.5))[..., None]
    if lv == 2:
        mil = MT.blur(MT.spots(S, 16, 12, 3, 12, 30, 1103), 2) > 0.35     # mildew blooms
        co = MT.patch(co, mil, (150, 152, 128), 0.55, 1104)
        st = blobs(S, 1105, 1.4, 3.0, 3)                                  # stains
        co = MT.patch(co, st, (80, 62, 44), 0.5, 1106)
        fw, ft = fibres(S, 700, 1107, 0.0, 0.25, 8, 26)                   # frayed rush along the long edges
        fr = fw * ((yy < 0.05 * S) | (yy > 0.95 * S))
        co = MT.mix(co, (172, 152, 112), fr * 0.8)
        corner = (xx + yy + 40 * MT.fbm(S, 2.0, 1, 1, 1108)) > 1.78 * S    # one torn corner
        co[corner] = co[corner] * 0.35 + 0.65 * np.array([70, 58, 44], f32) / 255
        h = h - 1.5 * corner
        mask = mil | st | (fr > 0.3) | corner
    return R(co, MT.combine(nn, MT.h2n(h, 1.0)), r, mask, t, 0.1, 0.25)


def floor_tatami_heri(lv, S):
    t = [T("tatami_heri"), T("tatami_heri", 6, 1, 4), T("tatami_heri", 8, 1, 5)][lv]
    co, nn, r = cotton_common(S, t, kn=0.8, tiles=4, contrast=1.6, seed=1200)
    yy, xx = grid(S)
    mask = Z(S)
    h = np.zeros((S, S), f32)
    if lv >= 1:                                                   # frayed threads along both edges of the band
        fw, _ = fibres(S, [0, 300, 500][lv], 1201, 0.0, 0.6, 4, 14)
        fr = fw * ((yy < 0.06 * S) | (yy > 0.94 * S))
        co = MT.mix(co, (120, 110, 100), fr * 0.7)
        mask |= fr > 0.3
    if lv == 2:                                                   # torn: the rush of the mat shows through
        tear = blobs(S, 1202, 1.5, 3.0, 2)
        rush = 1 + 0.15 * np.sin(yy * 2 * math.pi / 3.0)
        co[tear] = (base((127, 108, 90), rush))[tear]
        h = h - 1.0 * tear
        mask |= tear
    return R(co, MT.combine(nn, MT.h2n(h, 1.0)), r, mask, t, 0.08, 0.2)


def floor_boards_int(lv, S):
    d, nn, r = hinoki(S, 1.6)                                     # boards ~0.26 m wide
    t = [T("timber_interior", 4, 1, 3), T("timber_interior"), T("timber_interior", 5, -2, -3)][lv]
    co = MT.recolor(d, t, 1.1, 0.35)
    mask = Z(S)
    h = np.zeros((S, S), f32)
    if lv == 1:                                                   # darker traffic lanes along the boards, scratches
        co = co * (1 - 0.10 * np.clip(MT.fbm(S, 3.2, 1, 10, 1301), 0, 1.5))[..., None]
        sc = scratches(S, 140, 1302, 15, 70)
        co = MT.mix(co, (128, 104, 84), sc * 0.6)
        mask = sc > 0.3
    if lv == 2:                                                   # dusty grey film, water rings, raised grain
        co = MT.mix(co, (122, 114, 106), np.clip(0.35 + 0.25 * MT.fbm(S, 2.6, 1, 1, 1303), 0, 0.6))
        wr = ring_marks(S, 12, 1304, 20, 60, 3)
        co = MT.mix(co, (40, 32, 28), wr * 0.6)
        h = h + (MT.lum(co) - MT.blur(MT.lum(co), 3)) * 25 - wr
        mask = wr > 0.3
    rough = r * [0.8, 0.9, 1.0][lv]
    return R(co, MT.combine(nn, MT.h2n(h, 1.0)), rough, mask, t, [0.12, 0.1, 0.06][lv], [0.35, 0.3, 0.2][lv])


def floor_boards_rough(lv, S):
    d, nn, r = src("old_planks_02", S)
    t = [T("timber_interior", 3, 1, 3), T("timber_interior", 1), T("timber_interior", -2, 0, -1)][lv]
    co = MT.recolor(d, t, 1.15, 0.3)
    yy, xx = grid(S)
    k = round(S / (0.07 * 512))                                   # adze scallops every ~7 cm along the grain
    adze = np.sin(2 * math.pi * (yy * k / S + 0.8 * MT.fbm(S, 2.0, 1, 1, 1401)))
    amp = [1.0, 0.35, 0.5][lv]
    co = co * (1 + 0.05 * amp * adze)[..., None]
    h = adze * amp * 1.2
    mask = Z(S)
    if lv == 1:                                                   # worn smooth, a little lighter, in lanes
        lane = np.clip(MT.fbm(S, 3.2, 8, 1, 1402), 0, 1.5)
        co = co * (1 + 0.05 * lane)[..., None]
        r = r * (1 - 0.15 * lane)
    if lv == 2:                                                   # splits and dirt in the joints
        sp = MT.edge_lines(S, 70, 1403, 1, 2, (60, 260))
        co = MT.mix(co, (28, 22, 18), sp * 0.85)
        L = MT.lum(d)
        jm = MT.blur((L < np.percentile(L, 5)).astype(f32), 1.5) > 0.4
        co = MT.patch(co, jm, (62, 52, 40), 0.8, 1404)
        h = h - sp * 2
        mask = (sp > 0.3) | jm
    return R(co, MT.combine(nn, MT.h2n(h, 1.0)), r, mask, t, 0.1, 0.2)


def floor_takeyuka(lv, S):
    """Split-bamboo slat floor (procedural): 3-4 cm slats along v, nodes every 1/3 m, lashing cords every 0.5 m."""
    rg = np.random.default_rng(1501)
    t = [T("bamboo_weathered", 4, 0, 6), T("bamboo_weathered"), T("bamboo_weathered", -6)][lv]
    ppm = S / 1.0
    n = int(round(S / (0.035 * ppm)))
    wd = rg.uniform(0.86, 1.14, n)
    wd = wd * S / wd.sum()
    edges = np.r_[0, np.cumsum(wd)]
    yy, xx = grid(S)
    k = np.clip(np.searchsorted(edges, xx, "right") - 1, 0, n - 1)
    fx = (xx - edges[k]) / wd[k]
    prof = np.sin(np.pi * fx)
    gap = (fx < 0.06) | (fx > 0.94)
    tint = rg.normal(1, 0.06, n)[k]
    per = S / 3.0
    dd = (yy - rg.uniform(0, per, n)[k]) % per
    dn = np.minimum(dd, per - dd)
    node, ridge = np.exp(-(dn / 2.2) ** 2), np.exp(-(dn / 4.0) ** 2)
    fib = MT.fbm(S, 1.5, 1, 30, 1502) * 0.05
    val = tint * (0.82 + 0.18 * prof) * (1 + fib) * (1 - 0.25 * node)
    val = np.where(gap, 0.3, val)
    cord = np.zeros((S, S), bool)
    for c in (0.25 * S, 0.75 * S):
        cord |= np.abs(yy - c) < 3
    tw = 0.75 + 0.25 * np.sin((xx + yy) * 2 * math.pi * 64 / S)
    val = np.where(cord, 0.62 * tw, val)
    co = base(t, val)
    h = prof * 1.5 + ridge * 1.0 - gap * 1.5 + cord * 2.0 * tw
    mask = cord.copy()
    if lv >= 1:
        co = MT.grey(co, [0, 0.2, 0.35][lv])
        co = co * (1 - [0, 0.08, 0.05][lv] * np.clip(MT.fbm(S, 3.2, 8, 1, 1503), 0, 1.5))[..., None]
    if lv == 2:                                                   # splits, two slats gone
        sp = MT.edge_lines(S, 40, 1504, 1, 2, (80, 300))
        co = MT.mix(co, (40, 36, 30), sp * 0.9)
        gone = np.isin(k, rg.choice(n, 2, replace=False)) & ~cord
        co[gone] = np.array([22, 20, 18], f32) / 255
        h = h - sp * 2 - gone * 3
        mask |= (sp > 0.3) | gone
    return R(np.clip(co, 0, 1), MT.h2n(h, 1.0), 0.6, mask, t, 0.15, 0.3)


def doma_common(S, kn, seed):
    d, nn, r = src("clay_floor_001", S, kn=kn)
    return d, nn, r


def ground_doma_earth(lv, S):
    d, nn, r = src("clay_floor_001", S, kn=0.6)
    t = [T("doma_earth", 3, 0, 1), T("doma_earth"), T("doma_earth", -3)][lv]
    co = MT.recolor(d, t, 1.4, 0.15)
    var = 0.06 * MT.fbm(S, 2.2, 1, 1, 1601) + 0.05 * MT.fbm(S, 1.3, 1, 1, 1602)
    co = co * (1 + var)[..., None]
    sa, st = MT.straw_flecks(S, [500, 350, 300][lv], 1603, 6, 18)
    co = MT.mix(co, (150, 136, 108), sa * st * 0.35)
    pb = MT.spots(S, 160, 6, 1.5, 4, 30, 1604)
    co = MT.mix(co, (150, 146, 138), pb * 0.45)
    h = var * 8 + pb * 1.2 + sa * 0.4
    mask = Z(S)
    if lv == 0:                                                   # broom sweep marks
        co = co * (1 + 0.025 * MT.fbm(S, 1.0, 1, 25, 1605))[..., None]
    if lv == 1:                                                   # trodden lanes (darker, smoother), ash by the stove
        lane = np.clip(MT.fbm(S, 3.6, 1, 1, 1606), 0, None)
        co = co * (1 - 0.07 * lane)[..., None]
        h = h * (1 - 0.5 * np.clip(lane, 0, 1))
        ash = MT.blur((MT.fbm(S, 3.2, 1, 1, 1607) > 1.7).astype(f32), 4) > 0.3
        co = MT.patch(co, ash, (150, 146, 140), 0.7, 1608)
        mask = ash
    if lv == 2:                                                   # damp patches, blown-in leaves
        damp = blobs(S, 1609, 1.2, 3.0, 4)
        co = MT.patch(co, damp, (78, 74, 68), 0.55, 1610)
        lf = np.clip(MT.blur(MT.spots(S, 12, 5, 12, 22, 40, 1611), 1.5) * 1.5, 0, 1)
        leaf = MT.recolor(src("dry_decay_leaves", S)[0], T("leaf_litter_autumn", -4), 1.2, 0.6)
        co = MT.mix(co, leaf, lf * 0.95)
        h = h + lf * 0.8
        mask = damp | (lf > 0.3)
    return R(co, MT.combine(nn, MT.h2n(h, 1.0)), np.clip(r + 0.1, 0, 1), mask, t, 0.08, 0.15)


def ground_doma_tataki(lv, S):
    d, nn, r = src("clay_floor_001", S, kn=0.35)
    d = MT.blur(d, 1.5)
    t = [T("doma_earth", 6), T("doma_earth", 3), T("doma_earth", 1)][lv]
    co = MT.recolor(d, t, 1.2, 0.1)
    g = MT.fbm(S, 0.3, 1, 1, 1701)                                # fine gravel in the lime-earth
    co = MT.mix(co, (175, 170, 160), (g > 1.9) * 0.5)
    co = MT.mix(co, (70, 66, 60), (g < -1.9) * 0.5)
    tamp = ring_marks(S, 90, 1702, 20, 45, 2)                     # tamping marks
    co = co * (1 - 0.03 * tamp)[..., None]
    h = -tamp * 0.6 + (np.abs(g) > 1.9) * 0.5
    mask = Z(S)
    if lv >= 1:                                                   # mottled, darker lanes
        co = co * (1 + [0, 0.08, 0.06][lv] * MT.fbm(S, 2.6, 1, 1, 1703))[..., None]
        co = co * (1 - 0.06 * np.clip(MT.fbm(S, 3.6, 1, 1, 1704), 0, None))[..., None]
    if lv == 2:                                                   # cracks, crumbled patches
        c = MT.cracks(S, 30, 1705)
        co = MT.mix(co, (52, 48, 44), c * 0.8)
        crumb = blobs(S, 1706, 1.5, 3.0, 3)
        co = MT.patch(co, crumb, (105, 98, 88), 0.7, 1707)
        h = h - c * 2 - crumb * (1.5 + np.abs(g))
        mask = (c > 0.3) | crumb
    return R(co, MT.combine(nn, MT.h2n(h, 1.0)), np.clip(r + 0.05, 0, 1), mask, t, 0.08, 0.15)


def ground_ash(lv, S):
    t = [T("ash_grey", 3), T("ash_grey"), T("ash_grey", -6, 0, 1)][lv]
    yy, xx = grid(S)
    wob = MT.fbm(S, 2.0, 1, 1, 1801)
    rake = np.sin(2 * math.pi * (yy * 48 / S + 0.35 * wob))       # raked lines ~2 cm apart
    amp = [1.0, 0.4, 0.15][lv]
    fine = 0.04 * MT.fbm(S, 2.6, 1, 1, 1802) + 0.03 * MT.fbm(S, 0.5, 1, 1, 1803)
    co = base(t, 1 + fine + 0.05 * amp * rake)
    h = rake * amp * 1.2 + fine * 10
    mask = Z(S)
    if lv >= 1:                                                   # charcoal bits, ember marks
        ch = MT.spots(S, 40, 8, 1, 3.5, 20, 1804)
        co = MT.mix(co, (32, 30, 28), ch * 0.9)
        em = blobs(S, 1805, 1.8, 3.2, 3)
        co = MT.patch(co, em, (115, 82, 62), 0.6, 1806)
        h = h + ch
        mask = (ch > 0.3) | em
    if lv == 2:                                                   # damp crust, fallen soot
        cr = blobs(S, 1807, 0.9, 3.0, 3)
        co = MT.patch(co, cr, (112, 108, 102), 0.6, 1808)
        so = MT.spots(S, 60, 6, 1, 3, 40, 1809)
        co = MT.mix(co, (40, 38, 36), so * 0.8)
        mask = mask | cr | (so > 0.3)
    return R(np.clip(co, 0, 1), MT.h2n(h, 1.0), 0.95, mask, t, 0.04, 0.1)


def wall_shikkui_int(lv, S):
    """Interior twin of shikkui (PLAYBOOK §15 T6): the CLEAN exterior plaster, no rain streaks, a touch warmer, mean
    kept under 192. _w1 faint smoke toward the top of the tile, _w2 hairline cracks and a damp stain at the foot (the
    2.0 m tile spans a storey: v = 0 at the top)."""
    r0 = MT.wall_shikkui(0, S)
    t = T("shikkui_white", -6, 0.5, 2.5)
    co = MT.recolor(r0["co"], t, 1.4, 0.2)
    yy, xx = grid(S)
    y01 = yy / S
    h = np.zeros((S, S), f32)
    mask = Z(S)
    if lv >= 1:
        soot = np.clip(0.55 - y01, 0, 1) * np.clip(0.8 + 0.4 * MT.fbm(S, 1.8, 1, 1, 1901), 0, 1.4)
        co = co * (1 - [0, 0.08, 0.10][lv] * soot)[..., None]
    if lv == 2:
        c = MT.cracks(S, 22, 1902, seg=(4, 9), jitter=0.55)
        co = MT.mix(co, (110, 104, 96), c * 0.6)
        damp = (y01 + 0.06 * MT.fbm(S, 2.0, 1, 1, 1903)) > 0.82
        damp = damp & blobs(S, 1904, -0.3, 2.6, 3)
        co = MT.patch(co, damp, (150, 138, 112), 0.5, 1905)
        h = h - c * 1.5
        mask = (c > 0.3) | damp
    return R(co, MT.combine(r0["n"], MT.h2n(h, 1.0)), r0["rough"], mask, t, r0["spec"], r0["gloss"])


def ceil_boards(lv, S):
    d, nn, r = hinoki(S, 2.2)                                     # wide sugi-like boards ~0.35 m
    t = [T("timber_interior", 10, 2, 6), T("timber_interior"), T("timber_interior", -2)][lv]
    co = MT.recolor(d, t, 1.05, 0.3)
    lap = np.zeros(S, f32)                                        # each board laps over the next: shadow + step
    x = np.arange(S)
    for j in joints(co, 40):
        dx = (x - j) % S
        lap += np.exp(-dx / 4.0) * (dx < 14)
    co = co * (1 - 0.25 * lap)[None, :, None]
    h = np.broadcast_to(-lap[None, :] * 1.0, (S, S)).astype(f32)
    mask = Z(S)
    if lv == 1:                                                   # smoke along the joints and in streaks
        co = co * (1 - 0.12 * np.clip(MT.vstreaks(S, 1906, 1.0, 10), 0, 1.2))[..., None]
    if lv == 2:                                                   # water stains with tide marks
        bl, rim = tide(S, 1907, 1.3, 3.2, 5)
        co = MT.patch(co, bl, (95, 78, 60), 0.45, 1909)
        co = MT.mix(co, (58, 44, 34), rim * 0.6)
        mask = (rim > 0.3) | bl
    return R(co, MT.combine(nn, MT.h2n(h, 1.0)), r, mask, t, 0.1, 0.25)


def wood_interior(lv, S):
    d, nn, r = hinoki(S, 1.0)
    t = [T("timber_interior", 4, 1, 3), T("timber_interior"), T("timber_interior", 4, -2, -4)][lv]
    co = MT.recolor(d, t, 1.1, 0.35)
    mask = Z(S)
    if lv == 1:                                                   # grime at hand height, polished edges
        co = co * (1 - 0.08 * np.clip(MT.fbm(S, 3.4, 1, 1, 2001), 0, 1.5))[..., None]
        r = r * 0.85
    if lv == 2:                                                   # dust film, scratches, pale edge wear
        co = MT.mix(co, (118, 108, 98), np.clip(0.35 + 0.25 * MT.fbm(S, 2.6, 1, 1, 2002), 0, 0.6))
        sc = scratches(S, 120, 2003, 15, 70)
        co = MT.mix(co, (150, 125, 100), sc * 0.7)
        e = MT.edge_lines(S, 50, 2004, 2, 4)
        co = MT.mix(co, (140, 112, 88), e * 0.7)
        mask = (sc > 0.3) | (e > 0.3)
    return R(co, nn, r, mask, t, 0.1, 0.25)


def bamboo_sooted(lv, S):
    r0 = MT.bamboo_weathered(0, S)
    t = [T("timber_sooted", 6, 2, 5), T("timber_sooted", 1), T("timber_sooted", 0)][lv]
    co = MT.recolor(r0["co"], t, 1.3, 0.0)
    h = np.zeros((S, S), f32)
    mask = Z(S)
    if lv >= 1:
        co = co * (1 - 0.2 * np.clip(MT.vstreaks(S, 2101, 1.0, 12), 0, 1))[..., None]
    if lv == 2:                                                   # crusted soot
        c = np.clip(MT.fbm(S, 1.3, 1, 1, 2102), 0, None)
        cm = c > 0.7
        co = MT.patch(co, cm, (62, 58, 54), 0.7, 2103)
        h = h + c * 1.2
        mask = cm
    return R(co, MT.combine(r0["n"], MT.h2n(h, 1.0)), [0.6, 0.45, 0.85][lv], mask, t,
             [0.15, 0.25, 0.1][lv], [0.3, 0.55, 0.2][lv])


def paper_fusuma(lv, S):
    r0 = MT.paper_shoji(0, S)
    t = [T("gofun_white", -5, 0, 1), T("gofun_white", -8, 0.5, 7), T("gofun_white", -8, 1, 6)][lv]
    co = MT.recolor(r0["co"], t, 1.6, 0)
    yy, xx = grid(S)
    row = (yy // (S / 2)).astype(int)                             # overlapping paper sheets, 1/3 x 1/2 m, staggered
    seam = (((xx - (row % 2) * S / 6) % (S / 3)) < 4) | ((yy % (S / 2)) < 4)
    co = co * (1 + 0.025 * seam)[..., None]
    h = seam * 0.5
    mask = Z(S)
    if lv >= 1:                                                   # hand marks (smudges)
        sm = MT.blur(MT.spots(S, 6, 6, 10, 25, 30, 2201), 4) > 0.3
        co = MT.patch(co, sm, (150, 140, 120), 0.35, 2202)
        mask |= sm
    if lv == 2:                                                   # torn holes, stains, patches
        tr = polys(S, 6, 2203, 8, 26, 12)
        co = MT.mix(co, (48, 42, 36), tr * 0.95)
        st = blobs(S, 2204, 1.4, 3.0, 3)
        co = MT.patch(co, st, (160, 130, 90), 0.4, 2205)
        pt = polys(S, 5, 2206, 30, 60, 4)
        co = co * (1 + 0.04 * pt)[..., None]
        h = h + pt * 0.3 - tr
        mask |= (tr > 0.3) | st
    return R(np.clip(co, 0, 1), MT.combine(r0["n"], MT.h2n(h, 1.0)), 0.85, mask, t, 0.06, 0.15)


def cotton_common(S, t, kn=0.9, tiles=2, contrast=0.9, seed=2300):
    d, nn, r = src("rough_linen", S, tiles=tiles, kn=kn)
    var = weave_var(S, seed)
    co = MT.recolor(d, t, contrast, 0.0) * (1 + var)[..., None]
    return co, MT.combine(nn, MT.h2n(var * 8, 1.0)), r


def textile_cotton_indigo(lv, S):
    t = [T("aizome_kon", -1), T("aizome_kon", 2), T("aizome_kon", 3.5, 0, 1)][lv]
    co, nn, r = cotton_common(S, t, contrast=1.6)
    yy, xx = grid(S)
    co = co * (1 + 0.035 * np.sin(2 * math.pi * xx * 16 / S))[..., None]   # a faint stripe, ~3 cm
    mask = Z(S)
    if lv >= 1:                                                   # faded folds
        fold = np.clip(MT.fbm(S, 2.8, 1, 6, 2301), 0, None)
        co = co * (1 + [0, 0.12, 0.18][lv] * fold)[..., None]
    if lv == 2:                                                   # mildew, an opened seam
        mil = MT.spots(S, 10, 8, 1, 3, 12, 2302)
        co = MT.mix(co, (140, 146, 140), mil * 0.7)
        w = MT.Wrap(S)
        for x0 in range(0, S, 32):
            if (x0 // 32) % 3:
                w.line([(x0, 0.6 * S), (x0 + 24, 0.6 * S + 1)], 255, 2)
        sm = w.arr()
        co = MT.mix(co, (20, 22, 26), sm * 0.9)
        mask = (mil > 0.3) | (sm > 0.3)
    return R(co, nn, r, mask, t, 0.06, 0.15)


def textile_cotton_plain(lv, S):
    t = [T("kinari_cloth", -2), T("kinari_cloth", -7, 0, 3), T("kinari_cloth", -9, 0.5, 4)][lv]
    co, nn, r = cotton_common(S, t, contrast=0.85)
    mask = Z(S)
    if lv == 2:                                                   # stains, mildew
        st = blobs(S, 2401, 1.4, 3.0, 2)
        co = MT.patch(co, st, (140, 118, 86), 0.5, 2402)
        mil = MT.spots(S, 14, 8, 0.8, 2.5, 10, 2403)
        co = MT.mix(co, (70, 76, 66), mil * 0.7)
        mask = st | (mil > 0.3)
    return R(co, nn, r, mask, t, 0.05, 0.12)


def stoneware(lv, S, pid, seed, light, dark, runs=None):
    t = [T(pid), T(pid, 1), T(pid, 3)][lv]
    yy, xx = grid(S)
    amp = 0.6 + 0.4 * np.clip(MT.fbm(S, 2.0, 1, 1, seed), -1, 1)
    ridge = np.sin(2 * math.pi * (yy * 48 / S + 0.12 * MT.fbm(S, 2.0, 1, 1, seed + 1)))   # throwing ridges ~1 cm
    drip = MT.fbm(S, 2.2, 1, 12, seed + 2)                        # glaze runs down the pot (v)
    co = base(t, 1 + 0.06 * MT.fbm(S, 2.4, 1, 1, seed + 3))
    thin = np.clip(ridge * 0.5 + 0.5, 0, 1) * 0.5 * amp + np.clip(drip, 0, None) * 0.3
    co = MT.mix(co, light, thin * 0.35)
    co = MT.mix(co, dark, np.clip(-drip, 0, None) * 0.3)
    if runs:                                                      # ash glaze: glassy green-grey runs
        co = MT.mix(co, runs, np.clip(drip - 0.4, 0, 1) * 0.5)
    sp = MT.spots(S, 120, 3, 0.6, 1.4, 20, seed + 4)
    co = MT.mix(co, (30, 22, 18), sp * 0.6)
    h = ridge * amp * 1.0 + drip * 0.5
    rough = 0.12 + 0.05 * MT.fbm(S, 2.0, 1, 1, seed + 5)
    mask = Z(S)
    if runs:                                                      # ash glazes craze from new (part of the glaze)
        cz = MT.cracks(S, 90, seed + 6, seg=(3, 7), steps=(4, 12), jitter=0.7)
        co = MT.mix(co, (120, 108, 86), cz * 0.25)
    if lv >= 1:                                                   # dust on the shoulders (top of the tile)
        dust = np.clip(0.45 - yy / S, 0, 1) * 2 * np.clip(0.6 + 0.5 * MT.fbm(S, 2.6, 1, 1, seed + 7), 0, 1)
        co = MT.mix(co, (138, 128, 116), dust * 0.55)
        rough = rough + dust * 0.6
        mask |= dust > 0.35
    if lv == 2:                                                   # crazed, chipped, dry film
        cz = MT.cracks(S, 120, seed + 8, seg=(3, 7), steps=(4, 12), jitter=0.7)
        co = MT.mix(co, (22, 16, 12), cz * 0.7)
        chips = polys(S, 8, seed + 9, 3, 9, 6)
        co = MT.mix(co, (150, 118, 90), chips * 0.95)
        co = MT.mix(co, np.broadcast_to(np.array([118, 108, 98], f32) / 255, co.shape), np.full((S, S), 0.12, f32))
        rough = rough + 0.3
        h = h - chips * 1.5 - cz * 0.5
        mask |= (cz > 0.3) | (chips > 0.3)
    return R(np.clip(co, 0, 1), MT.h2n(h, 1.0), np.clip(rough, 0, 1), mask, t, 0.7, 0.8)


def ceramic_stoneware_dark(lv, S):
    return stoneware(lv, S, "stoneware_dark", 2501, (128, 86, 54), (40, 28, 20))


def ceramic_stoneware_pale(lv, S):
    return stoneware(lv, S, "stoneware_pale", 2511, (186, 170, 136), (120, 100, 76), runs=(150, 152, 112))


def lacquer_black(lv, S):
    t = [T("sumi_black", -4), T("sumi_black", -2), T("sumi_black", 0)][lv]
    brush = MT.fbm(S, 2.0, 10, 1, 2601)                           # brush marks along u
    co = base(t, 1 + 0.04 * brush + 0.03 * MT.fbm(S, 2.6, 1, 1, 2602))
    h = brush * 0.3
    mask = Z(S)
    if lv >= 1:                                                   # rubbed through to the red-brown undercoat
        e = MT.blur(MT.spots(S, [0, 8, 12][lv], 5, 2, 6, 10, 2603), 2.0)
        co = MT.mix(co, (88, 46, 34), np.clip(e * 1.2, 0, 1) * 0.4)
        mask |= e > 0.3
    if lv == 2:                                                   # flaking to the wood, dust
        fl = blobs(S, 2604, 1.4, 3.0, 1.5)
        wood = base((92, 70, 52), 1 + 0.1 * MT.fbm(S, 1.5, 1, 20, 2605))
        co[fl] = wood[fl]
        co = MT.mix(co, (100, 96, 90), np.full((S, S), 0.15, f32))
        h = h - fl * 1.0
        mask |= fl
    return R(np.clip(co, 0, 1), MT.h2n(h, 1.0), [0.08, 0.25, 0.5][lv], mask, t, [0.8, 0.6, 0.35][lv],
             [0.85, 0.6, 0.35][lv])


def straw_tawara(lv, S):
    t = [T("thatch_new", -2), T("thatch_new", -8, -1, -8), T("thatch_new", -10, -1, -6)][lv]
    yy, xx = grid(S)
    stalk = 0.08 * MT.fbm(S, 1.5, 20, 1, 2701) + 0.05 * MT.fbm(S, 2.2, 6, 1, 2702)   # straws along u
    fw, ft = fibres(S, 2500, 2703, 0.0, 0.08, 30, 140)
    val = 1 + stalk + 0.12 * fw * (ft - 0.6)
    band = np.zeros((S, S), bool)                                 # rope bands every 0.25 m
    for c in (0.125, 0.375, 0.625, 0.875):
        dd = np.abs(((yy - c * S) + S / 2) % S - S / 2)
        band |= dd < 8
    tw = 0.5 + 0.5 * np.sin(2 * math.pi * 64 * (xx + yy) / S)
    val = np.where(band, (0.78 + 0.22 * tw) * 0.85, val)
    co = base(t, val)
    h = stalk * 6 + fw * 0.8 + band * 1.5 * tw
    mask = Z(S)
    if lv >= 1:
        co = MT.grey(co, [0, 0.25, 0.35][lv])
    if lv == 2:                                                   # frayed, burst
        fr = scratches(S, 300, 2704, 8, 26)
        co = MT.mix(co, np.clip(co * 1.3, 0, 1), fr)
        bu = blobs(S, 2705, 1.5, 3.0, 3)
        co = MT.patch(co, bu, (58, 48, 38), 0.8, 2706)
        h = h + fr * 0.6 - bu * 1.5
        mask = bu | (fr > 0.3)
    return R(np.clip(co, 0, 1), MT.h2n(h, 1.2), 0.85, mask, t, 0.08, 0.15)


def bamboo_weave(lv, S):
    """2/2 twill of ~1.5 cm bamboo strips (procedural)."""
    t = [T("bamboo_weathered", 4, 0, 6), T("bamboo_weathered", -2), T("bamboo_weathered", -6)][lv]
    w = 8
    yy, xx = np.mgrid[0:S, 0:S]
    i, j = xx // w, yy // w
    over = ((i - j) % 4) < 2                                      # warp (vertical strip) on top
    fx, fy = (xx % w) / w, (yy % w) / w
    across = np.where(over, fx, fy)
    along = np.where(over, fy, fx)
    prof = np.sin(np.pi * across)
    edge = (across < 0.1) | (across > 0.9)
    arch = np.sin(np.pi * along)
    fib = np.where(over, MT.fbm(S, 1.5, 1, 20, 2801), MT.fbm(S, 1.5, 20, 1, 2802))
    rg = np.random.default_rng(2803)
    tint = np.where(over, rg.normal(1, 0.06, S // w)[i], rg.normal(1, 0.06, S // w)[j])
    val = tint * (0.8 + 0.2 * prof) * (0.9 + 0.1 * arch) * (1 + 0.05 * fib)
    val = np.where(edge, val * 0.55, val)
    co = base(t, val)
    h = prof * 1.0 + arch * 0.8 - edge * 1.0
    mask = Z(S)
    if lv >= 1:
        co = MT.grey(co, [0, 0.2, 0.35][lv])
    if lv == 2:                                                   # broken strips
        cells = rg.random((S // w, S // w)) < 0.04
        br = cells[j, i]
        co[br] = np.array([40, 35, 30], f32) / 255
        h = h - br * 2
        mask = br
    return R(np.clip(co, 0, 1), MT.h2n(h.astype(f32), 1.2), 0.6, mask, t, 0.15, 0.3)


def decal_litter(lv, S):
    """Alpha decal (NoZWrite): leaves, straw, paper scraps and shards over dust. RGB = the litter field everywhere."""
    d, nn, r = src("dry_decay_leaves", S)
    t = T("grime_splash", [3, 0, -3][lv])
    co = MT.recolor(d, t, 1.0, 0.45)
    sa, st = MT.straw_flecks(S, 400, 2901, 15, 50)
    co = MT.mix(co, (165, 140, 95), sa * 0.8)
    co = MT.fix_mean(np.clip(co, 0, 1).astype(f32), t, np.ones((S, S), bool))   # before the masked scraps, so the
    pa = polys(S, [6, 12, 20][lv], 2902, 10, 28, 4)
    co = MT.mix(co, (185, 178, 160), pa)
    sh = polys(S, [4, 10, 18][lv], 2903, 5, 14, 5)
    co = MT.mix(co, (88, 70, 56), sh)
    cov = MT.blur(MT.fbm(S, 2.6, 1, 1, 2904), 1.0)
    thr = [1.2, 0.8, 0.4][lv]
    clumps = np.clip((cov - thr) / 0.5, 0, 1)
    dust = 0.35 * np.clip((cov - thr + 0.6) / 0.6, 0, 1)
    leaves = MT.spots(S, [40, 80, 140][lv], 6, 5, 12, 60, 2905)
    alpha = np.maximum.reduce([clumps, dust, leaves, sa * 0.9, pa, sh])
    mask = (pa > 0.3) | (sh > 0.3)
    return R(co, nn, 0.9, mask, t, 0.05, 0.1, alpha=np.clip(alpha, 0, 1))


# ================================================================================================ outdoor recipes
def stone_carved(lv, S):
    t = [T("stone_lantern", 5), T("stone_lantern", 0), T("stone_lantern", -3)][lv]
    co, pn, r = MT.stone("rock_surface", "stone_lantern", lv, S, t, 0.3, nk=0.6)
    yy, xx = grid(S)
    ang = math.radians(35)
    per = 7.0 * (S / 512)
    tool = np.sin((xx * math.cos(ang) + yy * math.sin(ang)) / per * 2 * math.pi + 0.3 * MT.fbm(S, 2.5, 1, 1, 3001))
    tool = MT.blur(tool * [0.8, 0.35, 0.25][lv] * np.clip(MT.fbm(S, 2.0, 1, 1, 3002) * 0.5 + 0.8, 0.2, 1.3),
                   [0.6, 1.5, 1.5][lv])
    co = co * (1 + 0.05 * tool)[..., None]
    if lv >= 1:                                                   # grime in the low parts
        co = co * (1 - 0.12 * np.clip(-MT.fbm(S, 2.2, 1, 1, 3003), 0, None))[..., None]
    co, mask = MT.lichen_moss(co, S, lv, 3004, [0, 35, 25][lv], [None, None, 0.95][lv])
    if lv == 2:                                                   # black lichen streaks
        bs = np.clip(MT.vstreaks(S, 3005, 1.0, 10) - 0.6, 0, 1)
        co = MT.mix(co, (28, 28, 26), bs * 0.6)
        mask = mask | (bs > 0.2)
    return R(co, MT.combine(pn, MT.h2n(tool * 0.8, 1.0)), r, mask, t, 0.2, 0.3)


def decal_moss(lv, S):
    """Alpha decal (NoZWrite): lichen spots (_w0), moss cushions (_w1), thick moss with dead leaves (_w2)."""
    t = [T("moss_on_stone", 4, -4, -6), T("moss_on_stone"), T("moss_on_stone", -4, -2, 2)][lv]
    var = MT.fbm(S, 2.2, 1, 1, 3101)
    co = base(t, 1 + 0.12 * var)
    co = MT.mix(co, (150, 150, 78), np.clip(var, 0, 1) * 0.3)
    co = MT.mix(co, (78, 92, 46), np.clip(-var, 0, 1) * 0.3)
    tips = MT.spots(S, 200, 6, 0.6, 1.5, 10, 3102)
    co = MT.mix(co, (170, 170, 110), tips * 0.4)
    cov = MT.fbm(S, 2.6, 1, 1, 3104)
    mask = Z(S)
    if lv == 0:
        alpha = MT.blur(MT.spots(S, 40, 10, 1.5, 5, 14, 3103), 0.7)
    elif lv == 1:
        alpha = np.clip((cov - 0.6) / 0.5, 0, 1)
    else:
        alpha = np.clip((cov + 0.2) / 0.5, 0, 1)
        lf = MT.spots(S, 10, 4, 3, 6, 20, 3105)
        co = MT.mix(co, (122, 78, 40), lf * 0.95)
        alpha = np.maximum(alpha, lf)
        mask = lf > 0.3
    h = MT.blur(alpha.astype(f32), 3) * 3 + tips + var
    return R(co, MT.h2n(h, 1.5), 0.95, mask, t, 0.05, 0.1, alpha=np.clip(alpha, 0, 1))


def straw_rope(lv, S):
    """Three-strand straw rope: u runs round the rope, v along it; strands at ~60 deg."""
    t = [T("thatch_new", -3), T("straw_aged", 3), T("straw_aged", -4)][lv]
    yy, xx = grid(S)
    fr = (xx / 16.0 + yy / 32.0) % 1.0                            # strand phase (tiles: 256/16, 256/32)
    prof = np.sin(np.pi * fr)
    groove = (fr < 0.08) | (fr > 0.92)
    fw, ft = fibres(S, 900, 3201, math.atan2(-1, 2), 0.1, 10, 30)  # fibres along the strands
    val = (0.72 + 0.28 * prof) * (1 + 0.12 * fw * (ft - 0.6)) * (1 + 0.05 * MT.fbm(S, 2.0, 1, 1, 3202))
    val = np.where(groove, val * 0.6, val)
    co = base(t, val)
    h = prof * 1.5 + fw * 0.4 - groove * 1.0
    mask = Z(S)
    if lv >= 1:
        co = MT.grey(co, [0, 0.25, 0.35][lv])
    if lv == 2:                                                   # frayed fibres, rotten patches
        fy = scratches(S, 120, 3203, 6, 20)
        co = MT.mix(co, np.clip(co * 1.3, 0, 1), fy)
        rot = blobs(S, 3204, 1.6, 3.0, 2)
        co = MT.patch(co, rot, (55, 46, 36), 0.8, 3205)
        mask = (fy > 0.3) | rot
    return R(np.clip(co, 0, 1), MT.h2n(h, 1.2), 0.85, mask, t, 0.08, 0.15)


def straw_stack(lv, S):
    a, pn, pr = MT.reed(S)
    t = [T("thatch_new", 0), T("straw_aged", 4), T("straw_aged", -4, toward="thatch_weathered", t=0.3)][lv]
    co = MT.recolor(a, t, [1.05, 1.15, 1.2][lv], [0.6, 0.25, 0.12][lv])
    yy, xx = grid(S)
    top = np.clip(0.35 - yy / S, 0, 1) / 0.35                     # the weathered top of the stack (top of the tile)
    mask = Z(S)
    h = np.zeros((S, S), f32)
    if lv >= 1:
        co = MT.mix(co, MT.grey(co, 0.8) * 0.9, top * [0, 0.5, 0.6][lv])
    if lv == 2:                                                   # moss, slumped
        mo = blobs(S, 3301, 1.25, 2.4, 2) & (top > 0.2)
        co = MT.patch(co, mo, (72, 84, 44), 0.8, 3302)
        h = h - 3.0 * np.clip(MT.fbm(S, 3.2, 1, 1, 3303) - 0.5, 0, None)
        mask = mo
    return R(co, MT.combine(pn, MT.h2n(h, 2.0)), pr, mask, t, 0.08, 0.15)


def crests(S):
    """Four generic shop marks (maru-ni-ichi, igeta, yamagata-ni-maru, hishi) resist-dyed, one per 0.5 m cell."""
    Zs = 2 * S
    im = Image.new("L", (Zs, Zs), 0)
    d = ImageDraw.Draw(im)
    cell = Zs / 2
    r = 0.30 * cell
    wd = max(2, int(0.18 * r))
    cs = [(cell / 2, cell / 2), (1.5 * cell, cell / 2), (cell / 2, 1.5 * cell), (1.5 * cell, 1.5 * cell)]
    cx, cy = cs[0]                                                # 1 maru ni ichi: ring + bar
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=255, width=wd)
    d.rectangle([cx - 0.6 * r, cy - 0.11 * r, cx + 0.6 * r, cy + 0.11 * r], fill=255)
    cx, cy = cs[1]                                                # 2 igeta: well frame (#)
    for k in (-0.35, 0.35):
        d.rectangle([cx - 0.9 * r, cy + k * r - wd / 2, cx + 0.9 * r, cy + k * r + wd / 2], fill=255)
        d.rectangle([cx + k * r - wd / 2, cy - 0.9 * r, cx + k * r + wd / 2, cy + 0.9 * r], fill=255)
    cx, cy = cs[2]                                                # 3 yamagata ni maru: mountain over a ring
    d.line([(cx - 0.9 * r, cy - 0.1 * r), (cx, cy - 0.8 * r), (cx + 0.9 * r, cy - 0.1 * r)], fill=255, width=wd,
           joint="curve")
    rr = 0.35 * r
    d.ellipse([cx - rr, cy + 0.4 * r - rr, cx + rr, cy + 0.4 * r + rr], outline=255, width=wd)
    cx, cy = cs[3]                                                # 4 hishi: diamond ring + a small diamond
    d.polygon([(cx, cy - r), (cx + 0.8 * r, cy), (cx, cy + r), (cx - 0.8 * r, cy)], outline=255, width=wd)
    s = 0.3 * r
    d.polygon([(cx, cy - s), (cx + 0.8 * s, cy), (cx, cy + s), (cx - 0.8 * s, cy)], fill=255)
    a = _arr(im.resize((S, S), Image.LANCZOS).convert("RGB"))[..., 0]
    return MT.blur(a, 0.6)


def textile_noren(lv, S):
    t = [T("aizome_kon", -2), T("aizome_kon", 3, 0, 1), T("aizome_kon", 4.5, -1, 2)][lv]
    co, nn, r = cotton_common(S, t, tiles=4, contrast=1.6)
    yy, xx = grid(S)
    cr = crests(S)
    co = MT.mix(co, [(205, 205, 196), (180, 184, 182), (160, 168, 170)][lv], cr * [0.95, 0.8, 0.65][lv])
    mask = cr > 0.3
    alpha = np.ones((S, S), f32)
    if lv >= 1:                                                   # faded, sun-bleached folds
        fold = np.clip(MT.fbm(S, 2.6, 1, 8, 3401), 0, None)
        co = co * (1 + [0, 0.15, 0.2][lv] * fold)[..., None]
    if lv == 2:                                                   # torn hems (bottom of each 0.5 m cell), holes, stains
        up = (S / 2) - (yy % (S / 2))                             # px above the next hem line
        depth = 40 * np.clip(MT.fbm(S, 1.6, 1, 1, 3402), 0, None) * (MT.fbm(S, 1.2, 1, 1, 3403) > 0)
        alpha[up < depth] = 0
        alpha[blobs(S, 3404, 2.0, 3.0, 2)] = 0
        st = blobs(S, 3405, 1.3, 3.0, 3)
        co = MT.patch(co, st, (120, 100, 80), 0.5, 3406)
        mask |= st
    return R(co, nn, r, mask, t, 0.05, 0.12, alpha=alpha)


def textile_kinari(lv, S):
    t = [T("kinari_cloth", -3), T("kinari_cloth", -8, 0, 1), T("kinari_cloth", -10, 1, 4)][lv]
    co, nn, r = cotton_common(S, t, tiles=4, contrast=0.85)
    yy, xx = grid(S)
    mask = Z(S)
    alpha = np.ones((S, S), f32)
    if lv >= 1:                                                   # mildew spots
        mil = MT.spots(S, [0, 14, 20][lv], 8, 0.8, 2.5, 14, 3501)
        co = MT.mix(co, (70, 76, 66), mil * 0.7)
        mask |= mil > 0.3
    if lv == 2:                                                   # shredded from the bottom, holes, stains
        rg = np.random.default_rng(3502)
        w = MT.Wrap(S)
        for _ in range(14):
            x = rg.uniform(0, S)
            L = rg.uniform(0.1, 0.4) * S
            w.polygon([(x - rg.uniform(1, 4), S), (x + rg.uniform(1, 4), S), (x + rg.normal(0, 3), S - L)], 255)
        alpha[w.arr() > 0.3] = 0
        alpha[blobs(S, 3503, 1.9, 3.0, 2)] = 0
        st = blobs(S, 3504, 1.3, 3.0, 3)
        co = MT.patch(co, st, (120, 100, 76), 0.5, 3505)
        mask |= st
    return R(co, nn, r, mask, t, 0.05, 0.12, alpha=alpha)


def paper_chochin(lv, S):
    """Oiled lantern paper over ribs (horizontal, 32 per tile = 3.1 cm; u runs round the lantern). No text here:
    the ink text comes from the sumi text decal."""
    r0 = MT.paper_shoji(0, S)
    t = [T("washi_shoji", -3, 1, 8), T("washi_shoji", -5, 1, 9), T("washi_shoji", -7, 1, 8)][lv]
    co = MT.recolor(r0["co"], t, 1.5, 0)
    yy, xx = grid(S)
    rib = np.exp(-(((yy % 16) - 8) / 1.2) ** 2)
    co = co * ((1 - 0.12 * rib) * (1 + 0.04 * MT.fbm(S, 2.0, 1, 1, 3601)))[..., None]
    h = rib * 1.5
    mask = Z(S)
    alpha = np.ones((S, S), f32)
    if lv >= 1:                                                   # water stains with tide marks
        bl, rim = tide(S, 3602, [0, 1.5, 1.3][lv])
        co = MT.patch(co, bl, (170, 140, 95), 0.4, 3604)
        co = MT.mix(co, (120, 96, 66), rim * 0.5)
        mask |= bl | (rim > 0.3)
    if lv == 2:                                                   # split between ribs, holed; ribs stay
        holes = (MT.fbm(S, 2.6, 6, 1, 3605) > 1.5) | blobs(S, 3606, 2.1, 3.0, 1.2)
        holes = holes & (rib < 0.5)
        alpha[holes] = 0
        co = MT.mix(co, (60, 50, 40), (rib > 0.5) * MT.blur(holes.astype(f32), 3) * 0.8)
    return R(np.clip(co, 0, 1), MT.combine(r0["n"], MT.h2n(h, 1.0)), 0.8, mask, t, 0.08, 0.2, alpha=alpha)


def reed_yoshizu(lv, S):
    d, nn, r = src("bamboo_wall", S)                              # the 2 m scan squeezed onto 1 m: reeds ~1 cm
    t = [T("sudare_reed", 4, 0, 4), T("sudare_reed", -2, -1, -4), T("sudare_reed", -6, -1, -5)][lv]
    co = MT.recolor(d, t, 1.0, 0.3)
    yy, xx = grid(S)
    L = MT.lum(d)
    gaps = L < np.percentile(L, [4, 7, 7][lv])
    tie = np.zeros((S, S), bool)                                  # twine ties every 1/3 m
    for c in (S / 6, S / 2, 5 * S / 6):
        tie |= np.abs(yy - c) < 3
    tw = 0.8 + 0.2 * np.sin(2 * math.pi * 128 * (xx + yy) / S)
    co[tie] = (base((70, 60, 48), tw))[tie]
    mask = tie.copy()
    alpha = np.where(gaps & ~tie, 0.0, 1.0).astype(f32)
    h = (L - L.mean()) * 4 + tie * 1.5
    if lv >= 1:
        co = MT.grey(co, [0, 0.25, 0.35][lv])
    if lv == 2:                                                   # broken reeds: gaps along v
        br = (MT.fbm(S, 2.6, 1, 6, 3701) > 1.5) & ~tie
        alpha[br] = 0
        mask |= br
    return R(np.clip(co, 0, 1), MT.combine(nn, MT.h2n(h, 1.0)), r, mask, t, 0.08, 0.2, alpha=alpha)


def paint_shu(lv, S):
    """Vermilion (shu) over weathered planks (RESTRICTED: shrines only, PLAYBOOK §8)."""
    a = MT.photo("weathered_planks", "diff", S)
    t = [T("shu_vermilion"), T("shu_vermilion", 2, -3, -3), T("shu_vermilion", 3, -4, -3)][lv]
    paint = MT.recolor(a, t, 0.5, 0) * (1 + 0.04 * MT.fbm(S, 2.0, 1, 8, 3801))[..., None]
    wood = MT.recolor(a, T("timber_weathered", toward="stone_lantern", t=0.3), 1.1, 0.1)
    if lv >= 1:                                                   # chalky bloom, darkened streaks
        ch = np.clip(0.5 + 0.5 * MT.fbm(S, 2.6, 1, 1, 3802), 0, 1)
        paint = MT.mix(paint, (176, 128, 116), ch * [0, 0.18, 0.25][lv])
        paint = paint * (1 - 0.06 * np.clip(MT.vstreaks(S, 3803, 1.0, 14), 0, 1.3))[..., None]
    m = np.zeros((S, S), f32)
    if lv >= 1:
        m = np.maximum(m, MT.edge_lines(S, [0, 60, 80][lv], 3804, 2, 5))
    if lv == 2:                                                   # peeling patches to grey wood
        m = np.maximum(m, blobs(S, 3805, 1.05, 2.6, 1.5).astype(f32))
    co = MT.mix(paint, wood, m)
    n = MT.combine(MT.pnormal("weathered_planks", S, k=[0.5, 0.6, 0.8][lv]), MT.h2n(-m * 1.0, 1.0))
    return R(co, n, MT.prough("weathered_planks", S) * [0.8, 0.9, 1.0][lv], m > 0.3, t, 0.12, 0.25)


def wood_endgrain(lv, S):
    """One log end per texture (NOT tileable): pith at (0.5, 0.5); map a disc of the log's diameter round it."""
    t = [T("timber_weathered", 8, 3, 8), T("timber_weathered", -2, toward="stone_lantern", t=0.2),
         T("timber_weathered", -6, toward="stone_lantern", t=0.3)][lv]
    yy, xx = grid(S)
    c = S / 2
    rr = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    f = rr / 6.5 + 0.8 * np.sin(rr / 37) + MT.fbm(S, 2.4, 1, 1, 3901) * 0.6   # rings ~1.3 cm (read at a glance)
    fr = f % 1.0
    late = np.clip((fr - 0.62) / 0.1, 0, 1) * np.clip((1 - fr) / 0.08, 0, 1)
    val = (1 - 0.3 * late + 0.05 * MT.fbm(S, 2.6, 1, 1, 3902)) * (1 - 0.45 * np.exp(-(rr / 5) ** 2))
    val = val * (1 - 0.12 * np.clip((rr - 0.42 * S) / (0.08 * S), 0, 1))    # darker sapwood edge
    if lv == 0:                                                   # saw arcs
        val = val * (1 + 0.03 * np.sin(np.sqrt((xx - c) ** 2 + (yy + 3 * S) ** 2) / 5 * 2 * math.pi))
    co = base(t, val)
    h = -late * 0.8
    mask = Z(S)
    if lv >= 1:                                                   # radial checks
        rg = np.random.default_rng(3903 + lv)
        im = Image.new("L", (S, S), 0)
        dr = ImageDraw.Draw(im)
        for _ in range([0, 3, 6][lv]):
            a = rg.uniform(0, 2 * math.pi)
            r1 = rg.uniform(0.3, 0.5) * S
            dr.line([(c + 5 * math.cos(a), c + 5 * math.sin(a)), (c + r1 * math.cos(a), c + r1 * math.sin(a))],
                    fill=255, width=[1, 1, 2][lv])
        ck = MT.blur(_arr(im.convert("RGB"))[..., 0], 0.5)
        co = MT.mix(co, (30, 24, 20), ck * 0.9)
        co = MT.grey(co, [0, 0.2, 0.35][lv])
        h = h - ck * 3
        mask |= ck > 0.3
    if lv == 2:
        co, lm = MT.lichen_moss(co, S, 2, 3905, 8, None)
        mask |= lm
    return R(np.clip(co, 0, 1), MT.h2n(h, 1.0), 0.8, mask, t, 0.1, 0.2)


def ground_leaf_litter(lv, S):
    d, nn, r = src("dry_decay_leaves", S)
    t = [T("leaf_litter_autumn", 3, 4, 4), T("leaf_litter_autumn"), T("leaf_litter_autumn", -10, -2, -7)][lv]
    co = MT.recolor(d, t, 1.0, [0.9, 0.5, 0.25][lv])
    if lv == 0:                                                   # maple red and ginkgo yellow among the brown
        hv = MT.fbm(S, 1.6, 1, 1, 4001)
        co = MT.mix(co, (160, 62, 34), np.clip(hv - 0.4, 0, 1) * 0.45)
        co = MT.mix(co, (196, 150, 52), np.clip(-hv - 0.4, 0, 1) * 0.45)
    if lv == 1:                                                   # brown, in silt
        co = MT.grey(co, 0.3)
        co = MT.patch(co, blobs(S, 4002, 1.0, 2.8, 3), (112, 102, 88), 0.55, 4003)
    if lv == 2:                                                   # rotted black, mud (wetter)
        co = MT.grey(co, 0.45)
        mud = blobs(S, 4004, 0.6, 2.8, 3)
        co = MT.patch(co, mud, (66, 56, 46), 0.7, 4005)
        r = r * (1 - 0.3 * mud)
    return R(co, nn, r, Z(S), t, [0.06, 0.06, 0.12][lv], [0.15, 0.15, 0.3][lv])


# ================================================================================================ text decals
# Lead's go (2026-09-29): the two text atlases, from the OFL fonts in research/fonts/ (G1 decision 5). Kanji in Yuji
# Syuku (kaisho brush); kana in Yuji Hentaigana Akebono, which draws the ordinary hiragana code points as hentaigana
# (checked: no Kana Supplement code points, 86 hiragana) - the old shop-sign look. No Kantei-ryu (1779).
FONT_SYUKU = os.path.join(DEV, "research", "fonts", "yujisyuku", "YujiSyuku-Regular.ttf")
FONT_AKEBONO = os.path.join(DEV, "research", "fonts", "yujihentaiganaakebono", "YujiHentaiganaAkebono-Regular.ttf")
_FC = {}


def _font(path, size):
    from PIL import ImageFont
    k = (path, size)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(path, size)
    return _FC[k]


def _kana(c):
    return 0x3041 <= ord(c) <= 0x309F


def _col(d, xc, y0, text, size, sc, kana_hentai=True):
    """One vertical column, top to bottom, centred on xc. sc = supersampling. ' ' = half a character of space."""
    y = y0
    for c in text:
        if c == " ":
            y += 0.5 * size * sc
            continue
        f = _font(FONT_AKEBONO if (kana_hentai and _kana(c)) else FONT_SYUKU, int(size * sc))
        x0, y0b, x1, y1 = f.getbbox(c)
        d.text((xc - (x0 + x1) / 2, y + (size * sc - (y1 - y0b)) / 2 - y0b), c, font=f, fill=255)
        y += 1.06 * size * sc
    return y


def _wrap(text, n, indent=1):
    """Split an article into columns of n characters; continuation columns start `indent` characters lower."""
    cols, first = [], True
    while text:
        k = n if first else n - indent
        cols.append((text[:k], 0 if first else indent))
        text, first = text[k:], False
    return cols


# name: (x0, y0, x1, y1) px on the 1024 atlas, columns right to left as (text, size px, indent in chars), used by
SUMI_CELLS = [
    ("kosatsu_chuko_1711", (0, 0, 1024, 430), "jp_s_kosatsu boards (the 1711 Shotoku loyalty-and-filial-piety board)"),
    ("kanban_oyado", (0, 450, 120, 760), "jp_s_shopfront / jp_s_lantern_sign _chochin_inn: inn"),
    ("kanban_miki", (120, 450, 240, 760), "sake shop sign"),
    ("kanban_osobakiri", (240, 450, 325, 760), "soba shop (hentaigana so-ba)"),
    ("kanban_okashidokoro", (325, 450, 410, 760), "confectioner"),
    ("kanban_yakushu", (410, 450, 530, 760), "medicine shop (yakushu)"),
    ("kanban_oyasumidokoro", (530, 450, 630, 760), "tea house / rest stop"),
    ("kanban_gofuku", (630, 450, 750, 760), "cloth (gofuku) shop"),
    ("chochin_goshinto", (750, 450, 850, 760), "festival / shrine lantern (go-shinto)"),
    ("chochin_honcho", (850, 450, 970, 760), "ward-gate lantern (Honcho ward)"),
    ("sotoba_namuamida", (0, 780, 50, 1024), "jp_s_grave_wood sotoba"),
    ("gaku_hachimangu", (50, 780, 135, 1024), "jp_s_torii_wood plaque (Hachiman shrine)"),
    ("gaku_inari", (135, 780, 195, 1024), "jp_s_torii_wood plaque (Inari)"),
    ("nobori_hono_inari", (195, 780, 305, 1024), "jp_s_nobori: dedication banner (stretch the cell up the banner)"),
    ("oke_hinoyojin", (305, 780, 375, 1024), "jp_s_fire_tub: fire-watch on buckets"),
    ("oke_yosui", (375, 780, 475, 1024), "jp_s_fire_tub: 'water for use' on the tub"),
    ("mark_marudai", (475, 780, 595, 900), "jp_s_fire_tub house mark on buckets (circle + dai)"),
    ("kanban_manju", (595, 780, 655, 1024), "manju (steamed bun) shop, hentaigana"),
    ("kanban_tabako", (655, 780, 730, 1024), "tobacco shop, hentaigana"),
]
SUMI_TEXT = {
    "kanban_oyado": [("御宿", 100, 0)], "kanban_miki": [("御酒", 100, 0)], "kanban_osobakiri": [("御そば切", 66, 0)],
    "kanban_okashidokoro": [("御菓子所", 66, 0)], "kanban_yakushu": [("薬種", 100, 0)],
    "kanban_oyasumidokoro": [("御休処", 86, 0)], "kanban_gofuku": [("呉服", 100, 0)],
    "chochin_goshinto": [("御神燈", 86, 0)], "chochin_honcho": [("本町", 100, 0)],
    "sotoba_namuamida": [("南無阿弥陀仏", 36, 0)], "gaku_hachimangu": [("八幡宮", 72, 0)],
    "gaku_inari": [("稲荷大明神", 44, 0)], "nobori_hono_inari": [("奉納", 44, 0), ("稲荷大明神", 44, 0)],
    "oke_hinoyojin": [("火之用心", 54, 0)], "oke_yosui": [("用水", 84, 0)], "mark_marudai": [("大", 64, 0)],
    "kanban_manju": [("まんぢう", 50, 0)], "kanban_tabako": [("たばこ", 62, 0)],
}
KOSATSU = (["定"], ["一 忠孝をはげまし夫婦兄弟諸親類にむつましく召仕の者に至るまで憐愍を加ふべし若不忠不孝の者あらば重罪たるべき事",
                   "一 家業を専にし懈る事なく万事其分限に過べからざる事"], "右之条々可相守之者也", "正徳元年五月 日", "奉行")

CARVED_CELLS = [
    ("koshin_kuyoto", (0, 0, 120, 600), "jp_s_stele _koshin / _natural_slab: Koshin memorial"),
    ("shomen_kongo", (120, 0, 240, 480), "jp_s_stele _koshin: the deity's name"),
    ("dosojin", (240, 0, 380, 420), "jp_s_stele _round / _natural_slab: road gods"),
    ("bato_kanzeon", (380, 0, 490, 560), "jp_s_stele _relief_panel: horse-headed Kannon"),
    ("namuamidabutsu", (490, 0, 590, 580), "jp_s_stele nenbutsu stone, jp_s_grave_stones"),
    ("michishirube_edo_oyama", (590, 0, 770, 440), "jp_s_stele _pillar: direction stone, right Edo road / left Oyama road"),
    ("enmei_jizo", (770, 0, 850, 470), "jp_s_stone_jizo plinth / jp_s_stele"),
    ("joyato", (850, 0, 980, 380), "jp_s_stone_lantern shaft: 'ever-lit lamp'"),
    ("hono_genroku10", (0, 620, 160, 1024), "donor + date 1697: jp_s_chozubachi, jp_s_stone_lantern, jp_s_torii_stone"),
    ("kento_kyoho12_ujiko", (160, 620, 340, 1024), "lamp dedication 1727 by the parishioners: jp_s_stone_lantern"),
    ("hono_tenna2_muraju", (340, 620, 520, 1024), "donor + date 1682 by the village: jp_s_chozubachi, jp_s_torii_stone"),
    ("grave_doshin_shinji", (520, 620, 680, 1024), "jp_s_grave_stones: posthumous name + date (Kyoho 9, 1724)"),
    ("grave_shakuni_myoshin", (680, 620, 820, 1024), "jp_s_grave_stones: a woman's posthumous name, Hoei 2 (1705)"),
    ("sakai_kore_yori_higashi", (820, 620, 1024, 1024), "jp_s_stele _pillar: boundary stone 'from here east, Kami village'"),
]
CARVED_TEXT = {
    "koshin_kuyoto": [("庚申供養塔", 96, 0)], "shomen_kongo": [("青面金剛", 96, 0)], "dosojin": [("道祖神", 112, 0)],
    "bato_kanzeon": [("馬頭観世音", 86, 0)], "namuamidabutsu": [("南無阿弥陀仏", 80, 0)],
    "michishirube_edo_oyama": [("右 江戸道", 70, 0), ("左 大山道", 70, 0)], "enmei_jizo": [("延命地蔵尊", 66, 0)],
    "joyato": [("常夜燈", 104, 0)],
    "hono_genroku10": [("奉納", 60, 0), ("元禄十年丁丑九月吉日", 30, 1.5)],
    "kento_kyoho12_ujiko": [("献燈", 56, 0), ("享保十二年丁未三月吉日", 27, 1.8), ("氏子中", 40, 3)],
    "hono_tenna2_muraju": [("奉納", 56, 0), ("天和二年壬戌八月吉日", 29, 1.8), ("願主 村中", 40, 3)],
    "grave_doshin_shinji": [("享保九年", 34, 1), ("道心信士", 62, 0), ("十月十日", 34, 1)],
    "grave_shakuni_myoshin": [("宝永二年", 32, 1), ("釈尼妙信", 56, 0), ("乙酉", 32, 1)],
    "sakai_kore_yori_higashi": [("従是東", 64, 0), ("上村", 64, 1.5)],
}


def _layout(cells, texts, S, sc=2, kosatsu=False):
    """Coverage mask (0-1) of the atlas at S px, and the UV rectangles of the cells."""
    im = Image.new("L", (S * sc, S * sc), 0)
    d = ImageDraw.Draw(im)
    uv = {}
    for name, (x0, y0, x1, y1), use in cells:
        uv[name] = {"uv": [round(x0 / S, 4), round(y0 / S, 4), round(x1 / S, 4), round(y1 / S, 4)], "for": use}
        if name == "kosatsu_chuko_1711":
            cols = [(KOSATSU[0][0], 64, 0)]
            for art in KOSATSU[1]:
                cols += [(t, 30, i) for t, i in _wrap(art, 12)]
            cols += [(KOSATSU[2], 30, 1), (KOSATSU[3], 30, 3), (KOSATSU[4], 30, 9)]
            uv[name]["text"] = " / ".join([KOSATSU[0][0]] + KOSATSU[1] + list(KOSATSU[2:]))
        else:
            cols = texts[name]
            uv[name]["text"] = " / ".join(c[0] for c in cols)
        pitch = [1.3 * s for _, s, _ in cols]
        x = x1 - (x1 - x0 - sum(pitch)) / 2                           # centre the column block in the cell
        for (t, s, ind), p in zip(cols, pitch):
            xc = x - p / 2
            n = sum(0.5 if c == " " else 1.06 for c in t) + ind
            top = y0 + max(10, ((y1 - y0) - n * s) / 2) if not name.startswith("kosatsu") else y0 + 24
            _col(d, xc * sc, (top + ind * s) * sc, t, s, sc)
            x -= p
        if name == "mark_marudai":                                  # a house mark: a ring round the character
            cx, cy, r = (x0 + x1) / 2 * sc, (y0 + y1) / 2 * sc, 48 * sc
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=255, width=9 * sc)
    a = _arr(im.resize((S, S), Image.LANCZOS).convert("RGB"))[..., 0]
    return a, uv


_ATLAS = {}


def atlas(kind, S=1024):
    if kind not in _ATLAS:
        _ATLAS[kind] = (_layout(SUMI_CELLS, SUMI_TEXT, S) if kind == "sumi" else _layout(CARVED_CELLS, CARVED_TEXT, S))
    return _ATLAS[kind]


def decal_sumi_text(lv, S):
    """Ink (sumi) text atlas, alpha decal (NoZWrite). RGB = the ink colour everywhere; alpha = the brushed letters."""
    m, _ = atlas("sumi", S)
    t = [T("sumi_black", -2), T("sumi_black", 7, 2, 5), T("sumi_black", 8, 2, 5)][lv]
    co = base(t, 1 + 0.05 * MT.fbm(S, 2.4, 1, 1, 4101))
    kasure = np.clip(MT.fbm(S, 1.4, 1, 6, 4102) - 0.8, 0, 1)            # dry-brush streaks
    a = m * (1 - 0.35 * kasure)
    if lv == 1:                                                   # faded: thinner, weathered unevenly
        a = a * np.clip(0.72 + 0.12 * MT.fbm(S, 2.4, 1, 1, 4103), 0.45, 0.9)
    if lv == 2:                                                   # a ghost of the text, flaking
        flake = MT.fbm(S, 2.0, 1, 1, 4104) > 0.5
        a = a * 0.42 * np.where(flake, 0.3, 1.0)
    return R(co, MT.flat_n(S), 0.9, Z(S), t, 0.05, 0.1, alpha=np.clip(a, 0, 1))


def decal_carved_text(lv, S):
    """Inscriptions cut into stone, alpha decal (NoZWrite) that carries the carved look in its normal map and shading:
    a V-groove height from the letter mask, darker in the depth. Alpha covers the letters and a thin rim."""
    m, _ = atlas("carved", S)
    t = [T("stone_lantern", 3), T("stone_lantern", 0), T("stone_lantern", -3)][lv]
    co = MT.recolor(MT.photo("rock_surface", "diff", S), t, 1.0, 0.3)
    soft = [0.0, 1.5, 1.5][lv]
    g = 0.55 * MT.blur(m, 1.2 + soft) + 0.45 * MT.blur(m, 3.0 + soft)   # V-groove: deepest on the stroke's spine
    depth = np.clip(g / max(float(g.max()), 1e-4), 0, 1)
    co = co * (1 - [0.22, 0.30, 0.28][lv] * depth)[..., None]            # the cut is in its own shadow
    gx = (np.roll(depth, -1, 1) - np.roll(depth, 1, 1)) * 0.5            # baked light from the upper left: in a
    gy = (np.roll(depth, -1, 0) - np.roll(depth, 1, 0)) * 0.5            # cut, the near (upper-left) wall is in
    lit = np.clip((gx + gy) * 18.0 * [1.0, 0.7, 0.6][lv], -0.45, 0.45)  # shade, the far wall lit (incised, not raised)
    co = co * (1 - lit)[..., None]
    mask = Z(S)
    if lv >= 1:                                                   # grime in the cuts
        gr = depth * [0, 0.45, 0.35][lv]
        co = MT.mix(co, (38, 36, 32), gr)
        mask |= gr > 0.25
    alpha = np.clip(MT.blur(m, 2.0) * 2.4, 0, 1)
    h = -depth * [3.0, 2.2, 1.8][lv]
    if lv == 2:                                                   # lichen over half the text
        li = MT.spots(S, 90, 12, 3, 10, 24, 4105) * (MT.fbm(S, 1.6, 1, 1, 4106) > 0)
        li = MT.blur(li, 1.0)
        near = MT.blur(m, 12) > 0.02
        li = li * near
        co = MT.mix(co, (176, 176, 146), li * 0.7)
        alpha = np.maximum(alpha, li * 0.95)
        h = h * (1 - 0.7 * li) + li * 0.6
        mask |= li > 0.3
    return R(np.clip(co, 0, 1), MT.combine(MT.pnormal("rock_surface", S, k=0.5), MT.h2n(h, 2.0)), 0.85, mask, t,
             0.15, 0.25, alpha=alpha)


# ================================================================================================ the material table
def M(mid, fam, pid, tile, px, maker, spec, pen, road, grain, uv=None, alpha=None, pbw=None, S=None, tile_v=None,
      srcs=(), note=None, used_on=None, where="interior", atlas_kind=None):
    W, H = px if isinstance(px, tuple) else (px, px)
    return {"id": mid, "fam": fam, "pid": pid, "tile": tile, "tile_v": tile_v or tile, "px": (W, H), "S": S or W,
            "maker": maker, "spec": spec, "pen": pen, "road": road, "grain": grain, "uv": uv, "alpha": alpha,
            "pbw": pbw or {}, "srcs": list(srcs), "note": note, "used_on": used_on, "where": where,
            "atlas": atlas_kind}


WORLD = "world-scale: u, v = metres / tile_size_m; v runs down the texture = along the grain"
ATLAS_UV = ("TEXT ATLAS, not world-scale: map a face onto one cell's rectangle (\"cells\": u0, v0, u1, v1 with v "
            "down), keeping the cell's aspect; 1024 px = 1 m, so a cell's size is the text's real size. Lay the decal "
            "face 2-3 mm off the surface; never in Geometry/View/Fire. Text runs top to bottom, columns right to left.")
MATS = [
    # ---- interior (A2, research/interior/materials_needed.json): 21
    M("jp_m_floor_tatami", "floor", "tatami_aged", 1.82, (1024, 512), floor_tatami, (0.1, 20), "wood",
      "textile_carpet_int", "rush stalks across the mat (along v), warp threads along u (the length)", S=1024, tile_v=0.91,
      uv="ONE MAT PER TEXTURE: u = 0..1 along the mat length, v = 0..1 across it (1.76-1.82 x 0.87-0.91), turned "
         "with the mat; the heri are separate geometry (jp_m_floor_tatami_heri)", srcs=["tatami_mat"],
      note="The scan's green heri are cut off; the mat body only. _w2 has one torn corner at u,v ~ (1,1)."),
    M("jp_m_floor_tatami_heri", "floor", "tatami_heri", 1.0, 512, floor_tatami_heri, (0.08, 15), "cloth",
      "textile_carpet_int", "plain hemp/cotton weave", uv=WORLD + "; the 0.03 m band may use any strip of v",
      srcs=["rough_linen"], note="Plain black (commoner). A cha-brown second colour is not made (would need its own "
                                 "palette entry)."),
    M("jp_m_floor_boards_int", "floor", "timber_interior", 2.0, 1024, floor_boards_int, (0.15, 40), "wood",
      "wood_planks_int", "along v; boards ~0.26 m wide", uv=WORLD, srcs=["hinoki_planks"]),
    M("jp_m_floor_boards_rough", "floor", "timber_interior", 2.0, 1024, floor_boards_rough, (0.15, 40), "wood",
      "wood_planks_int", "along v; wide uneven adzed boards", uv=WORLD, srcs=["old_planks_02"]),
    M("jp_m_floor_takeyuka", "floor", "bamboo_weathered", 1.0, 512, floor_takeyuka, (0.15, 40), "wood",
      "wood_planks_int", "split bamboo slats 0.03-0.04 along v, lashing cords every 0.5 m", uv=WORLD),
    M("jp_m_ground_doma_earth", "ground", "doma_earth", 2.0, 1024, ground_doma_earth, (0.08, 15), "dirt", "dirt_int",
      "none; packed earth, straw bits, pebbles", uv=WORLD, srcs=["clay_floor_001"]),
    M("jp_m_ground_doma_tataki", "ground", "doma_earth", 2.0, 1024, ground_doma_tataki, (0.08, 15), "dirt", "dirt_int",
      "none; hard lime-earth, tamp marks, fine gravel", uv=WORLD, srcs=["clay_floor_001"]),
    M("jp_m_ground_ash", "ground", "ash_grey", 1.0, 512, ground_ash, (0.05, 10), "dirt", "dirt_int",
      "raked lines along u, ~2 cm apart", uv=WORLD),
    M("jp_m_wall_shikkui_int", "wall", "shikkui_white", 2.0, 1024, wall_shikkui_int, BM.SPEC["jp_m_wall_shikkui"],
      "dirt", None, "none; trowel", uv=WORLD + "; v = 0 at the top of a storey-high wall (smoke at the top, damp at the "
                                            "foot)", srcs=["white_plaster_02"],
      note="Interior twin of jp_m_wall_shikkui (PLAYBOOK §15 T6): no exterior weathering, mean under 192."),
    M("jp_m_ceil_boards", "wood", "timber_interior", 2.0, 1024, ceil_boards, (0.15, 40), "wood", None,
      "along v; wide boards (~0.35 m) lapped, lap shadow at each joint", uv=WORLD, srcs=["hinoki_planks"]),
    M("jp_m_wood_interior", "wood", "timber_interior", 2.0, 1024, wood_interior, (0.15, 40), "wood", None,
      "along v (member length)", uv=WORLD, srcs=["hinoki_planks"]),
    M("jp_m_bamboo_sooted", "bamboo", "timber_sooted", 1.0, 512, bamboo_sooted, (0.15, 40), "wood", None,
      "culm along v, nodes every 1/3 m", uv=WORLD, note="Built on make_textures.bamboo_weathered, recoloured."),
    M("jp_m_paper_fusuma", "paper", "gofun_white", 1.0, 512, paper_fusuma, (0.08, 20), "fabric_thin", None,
      "plain sheets 1/3 x 1/2 m, faint overlaps", uv=WORLD, note="PLAIN paper only (karakami barred for townsmen)."),
    M("jp_m_textile_cotton_indigo", "textile", "aizome_kon", 0.5, 256, textile_cotton_indigo, (0.06, 15), "cloth",
      None, "cotton weave, a faint 3 cm stripe along v", uv=WORLD, srcs=["rough_linen"]),
    M("jp_m_textile_cotton_plain", "textile", "kinari_cloth", 0.5, 256, textile_cotton_plain, (0.06, 15), "cloth",
      None, "coarse cotton / hemp weave", uv=WORLD, srcs=["rough_linen"]),
    M("jp_m_ceramic_stoneware_dark", "ceramic", "stoneware_dark", 0.5, 256, ceramic_stoneware_dark, (0.45, 70),
      "pottery", None, "throwing ridges along u (round the pot), glaze runs along v", uv=WORLD + "; u round the pot"),
    M("jp_m_ceramic_stoneware_pale", "ceramic", "stoneware_pale", 0.5, 256, ceramic_stoneware_pale, (0.45, 70),
      "pottery", None, "throwing ridges along u, ash-glaze runs along v, fine crackle", uv=WORLD + "; u round the pot"),
    M("jp_m_lacquer_black", "paint", "sumi_black", 0.5, 256, lacquer_black, (0.45, 70), "wood", None,
      "brush marks along u", uv=WORLD, note="No gold (elite only, PLAYBOOK §8)."),
    M("jp_m_straw_tawara", "straw", "thatch_new", 1.0, 512, straw_tawara, (0.08, 15), "hay", None,
      "straws along u, rope bands every 0.25 m across", uv=WORLD + "; u along the bale"),
    M("jp_m_bamboo_weave", "bamboo", "bamboo_weathered", 0.5, 256, bamboo_weave, (0.15, 40), "wood", None,
      "2/2 twill of ~1.5 cm strips", uv=WORLD),
    M("jp_m_decal_litter", "ground", "grime_splash", 2.0, 1024, decal_litter, (0.05, 10), None, None,
      "none; leaves, straw, paper scraps, shards, dust", alpha="decal", srcs=["dry_decay_leaves"],
      uv=WORLD + "; lay 3 mm above the floor on its own faces, never in Geometry/View/Fire"),
    # ---- outdoor kit (A3, research/outdoor_kit/materials_needed.json): 11 of 13
    M("jp_m_stone_carved", "stone", "stone_lantern", 1.0, 512, stone_carved, (0.2, 40), "granite", "stone_ext",
      "none; softened chisel marks", uv=WORLD, srcs=["rock_surface"], where="outdoor"),
    M("jp_m_decal_moss", "stone", "moss_on_stone", 2.0, 1024, decal_moss, (0.05, 10), None, None,   # FX3: 2 m (fp1 maker)
      "none; alpha patches", alpha="decal", uv=WORLD + "; decal faces 3 mm off the stone tops and north faces",
      where="outdoor", note="G1 decision 10: moss as a separate decal material."),
    M("jp_m_straw_rope", "straw", "straw_aged", 0.5, 256, straw_rope, (0.08, 15), "hay", None,
      "three strands, twist at ~60 deg", pbw={"_w0": "thatch_new"},
      uv="u round the rope (0.5 m per tile), v along it", where="outdoor"),
    M("jp_m_straw_stack", "straw", "straw_aged", 1.0, 256, straw_stack, (0.08, 15), "hay", None,
      "stalks down the face (v)", pbw={"_w0": "thatch_new"}, uv=WORLD + "; v = 0 at the top of the stack",
      srcs=["reed_roof_04"], where="outdoor"),
    M("jp_m_textile_noren", "textile", "aizome_kon", 1.0, 512, textile_noren, (0.06, 15), "cloth", None,
      "plain cotton weave", alpha="cut", srcs=["rough_linen"], where="outdoor",
      uv="world-scale, 1 m tile = 2 x 2 cells of 0.5 m, one resist-dyed shop mark per cell (1 maru-ni-ichi, "
         "2 igeta, 3 yamagata-ni-maru, 4 hishi); UV a panel onto a cell; torn hems (_w2) run along v = 0.5 and 1.0",
      note="Two-sided geometry (the rvmat does not make faces two-sided)."),
    M("jp_m_textile_kinari", "textile", "kinari_cloth", 1.0, 512, textile_kinari, (0.06, 15), "cloth", None,
      "plain cotton / hemp weave", alpha="cut", srcs=["rough_linen"], uv=WORLD + "; _w2 shreds hang from v = 1",
      where="outdoor", note="The faded-red Jizo-bib tint is not made (needs a palette entry)."),
    M("jp_m_paper_chochin", "paper", "washi_shoji", 1.0, 512, paper_chochin, (0.08, 20), "fabric_thin", None,
      "fibres; ribs along u every 3.1 cm", alpha="cut", uv="u round the lantern, v up it (ribs horizontal)",
      where="outdoor", note="Never emissive. No text on the paper (the ink text decal is not made yet)."),
    M("jp_m_reed_yoshizu", "straw", "sudare_reed", 1.0, 512, reed_yoshizu, (0.08, 20), "hay", None,
      "vertical reeds ~1 cm, twine ties every 1/3 m", alpha="cut", uv=WORLD, srcs=["bamboo_wall"], where="outdoor"),
    M("jp_m_paint_shu", "paint", "shu_vermilion", 2.0, 1024, paint_shu, (0.12, 30), "wood", None,
      "along v under the paint", uv=WORLD, srcs=["weathered_planks"], where="outdoor",
      note="RESTRICTED: shrines only (PLAYBOOK §8)."),
    M("jp_m_wood_endgrain", "wood", "timber_weathered", 0.5, 256, wood_endgrain, (0.15, 30), "wood", None,
      "growth rings, radial checks", uv="NOT tileable: one 0.5 m log end, pith at (0.5, 0.5); map a disc of the "
                                          "log's diameter centred there", where="outdoor"),
    M("jp_m_decal_carved_text", "stone", "stone_lantern", 1.0, 1024, decal_carved_text, (0.15, 30), None, None,
      "none; V-cut inscriptions (Yuji Syuku)", alpha="decal", uv=ATLAS_UV, srcs=["rock_surface"], where="outdoor",
      atlas_kind="carved", note="Inscriptions for steles, Jizo, lanterns, basins, torii and graves; dates Tenna 2 (1682) "
                               "to Kyoho 12 (1727); no family-name graves (Meiji). The carved look is in the normal "
                               "map and the shading, not ink. Fonts: SIL OFL 1.1, Yuji Project Authors."),
    M("jp_m_decal_sumi_text", "paint", "sumi_black", 1.0, 1024, decal_sumi_text, (0.05, 10), None, None,
      "brush strokes (Yuji Syuku kanji, Yuji Hentaigana Akebono kana)", alpha="decal", uv=ATLAS_UV, where="outdoor",
      atlas_kind="sumi", note="Ink on boards, paper and cloth: the 1711 Shotoku edict board, shop signs (hentaigana "
                             "kana), lanterns, sotoba, torii plaques, a dedication banner, fire-tub marks. Fonts: SIL "
                             "OFL 1.1, Yuji Project Authors. Nothing emissive."),
    M("jp_m_ground_leaf_litter", "ground", "leaf_litter_autumn", 2.0, 512, ground_leaf_litter, (0.06, 15), "dirt",
      "dirt_ext", "none", uv=WORLD, srcs=["dry_decay_leaves"], where="outdoor",
      note="Tile 2.0 m at 256 px/m (A3 asked 1.0 m at 256 px/m): keeps the scan's real leaf size."),
]
BYID = {m["id"]: m for m in MATS}
NOT_MADE = {}   # the two text decals were made after the lead approved the OFL fonts (2026-09-29)


# ================================================================================================ writing
def lp(fam, mid, w, suf):
    return "JP\\common\\materials\\%s\\%s%s%s" % (fam, mid, w, suf)


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def save(path, a):
    _img(a).save(path)


def to_paa(png, paa):
    os.makedirs(os.path.dirname(paa), exist_ok=True)
    r = subprocess.run([BM.IMAGE_TO_PAA, png, paa], capture_output=True, text=True, errors="replace")
    if r.returncode != 0 or not os.path.isfile(paa):
        raise RuntimeError("ImageToPAA failed %s: %s" % (png, r.stdout + r.stderr))


def rvmat_text(m, lv):
    w = "_w%d" % lv
    s, p = m["spec"]
    f = [1.1, 1.0, 0.8][lv]
    t = BM.rvmat_text(lp(m["fam"], m["id"], w, "_nohq.paa"), lp(m["fam"], m["id"], w, "_smdi.paa"), round(s * f, 3),
                      int(p * f), BM.finish_for(m["id"]))
    flag = {"decal": "NoZWrite", "cut": "AlphaTest32"}.get(m["alpha"])
    if flag:
        t = t.replace('VertexShaderID="Super";\n', 'VertexShaderID="Super";\nrenderFlags[]=\n{\n\t"%s"\n};\n' % flag, 1)
    return t


def write_rvmats(m):
    for lv in range(3):
        wb(os.path.join(LIB, m["fam"], m["id"] + "_w%d.rvmat" % lv), rvmat_text(m, lv))


def outfit(a, W, H):
    if a.shape[1] == W and a.shape[0] == H:
        return a
    if a.ndim == 2:
        return np.asarray(Image.fromarray(a.astype(np.float32), mode="F").resize((W, H), Image.BILINEAR))
    return np.stack([outfit(a[..., c], W, H) for c in range(a.shape[2])], -1)


def paa_check(paa, pal, pid, mpath):
    """C1 on the shipped PAA itself (RGB of _co or _ca), with the same detail mask as the PNG check. matcheck's own
    sidecar route cannot find the mask of a _ca file (its stem rule only strips _co)."""
    img = matcheck.read_rgb(paa)
    h, w = img.shape[:2]
    px = img.reshape(-1, 3).astype(np.float64)
    keep = np.ones(len(px), bool)
    if mpath:
        keep = np.asarray(Image.open(mpath).convert("L").resize((w, h), Image.NEAREST)).reshape(-1) < 128
    mean = px[keep].mean(0)
    de = min(float(np.linalg.norm(matcheck.srgb_to_lab(mean) - matcheck.srgb_to_lab(t)))
             for t in matcheck.targets(pal, pid))
    tol = float(pal[pid]["tolerance_dE76"])
    return {"mean_srgb": [round(float(v), 1) for v in mean], "dE": round(de, 2),
            "verdict": "FAIL" if de > tol else "PASS", "warnings": [], "masked": bool(mpath)}


def make_one(m, pal, man):
    W, H = m["px"]
    S = m["S"]
    mid, fam = m["id"], m["fam"]
    res, wears = [], {}
    for lv in range(3):
        w = "_w%d" % lv
        r = m["maker"](lv, S)
        mask = np.asarray(r["mask"], bool)
        alpha = r.get("alpha")
        co = MT.fix_mean(np.clip(r["co"], 0, 1).astype(f32), r["target"], ~mask)
        n = np.asarray(r["n"], f32)
        rough = np.broadcast_to(np.asarray(r["rough"], f32), (S, S)).astype(f32)
        if (W, H) != (S, S):
            co, n, rough = outfit(co, W, H), outfit(n, W, H), outfit(rough, W, H)
            n = n / np.linalg.norm(n, axis=-1, keepdims=True)
            mask = outfit(mask.astype(f32), W, H) > 0.5
            if alpha is not None:
                alpha = outfit(np.asarray(alpha, f32), W, H)
            co = MT.fix_mean(np.clip(co, 0, 1).astype(f32), r["target"], ~mask)
        stem = os.path.join(TEX, mid + w)
        save(stem + "_co.png", co)
        cs = "_co"
        if alpha is not None:
            cs = "_ca"
            save(stem + "_ca.png", np.concatenate([co, np.clip(alpha, 0, 1)[..., None]], -1))
        save(stem + "_nohq.png", n * 0.5 + 0.5)
        save(stem + "_smdi.png", np.stack([np.ones_like(rough), r["spec"] * (1 - rough), r["gloss"] * (1 - rough)], -1))
        mp = stem + "_mask.png"
        if mask.any():
            Image.fromarray((mask * 255).astype(np.uint8)).save(mp)
        elif os.path.isfile(mp):
            os.remove(mp)
        with cf.ThreadPoolExecutor(3) as ex:
            list(ex.map(lambda suf: to_paa(stem + suf + ".png", os.path.join(LIB, fam, mid + w + suf + ".paa")),
                        (cs, "_nohq", "_smdi")))
        pid = m["pbw"].get(w) or m["pid"]
        a = matcheck.check(stem + "_co.png", pal, pid, TEX)
        a["shipped_paa"] = paa_check(os.path.join(LIB, fam, mid + w + cs + ".paa"), pal, pid,
                                     mp if mask.any() else None)
        res.append(a)
        wears[w] = {"name": ["clean", "normal", "heavy"][lv], "look": NEED[mid]["wear"][w],
                    "co": lp(fam, mid, w, cs + ".paa"), "rvmat": lp(fam, mid, w, ".rvmat"),
                    "target_srgb": [round(float(x), 1) for x in r["target"]],
                    "masked_frac": round(float(mask.mean()), 3)}
        if alpha is not None:
            wears[w]["alpha_cover"] = round(float((np.asarray(alpha) > 0.5).mean()), 3)
    write_rvmats(m)
    nd = NEED[mid]
    side = {
        "id": mid, "family": fam, "palette_id": m["pid"], "palette_by_wear": m["pbw"],
        "tile_size_m": m["tile"], "texture_px": [W, H] if W != H else W, "px_per_m": round(W / m["tile"], 1),
        "uv": m["uv"] or WORLD, "grain": m["grain"],
        "penetration_rvmat": ("dz\\data\\data\\penetration\\%s.rvmat" % m["pen"]) if m["pen"] else None,
        "roadway_surface": ("dz\\surfaces\\data\\roadway\\%s.paa" % m["road"]) if m["road"] else None,
        "finish": BM.finish_for(mid), "wear": wears, "used_by": nd.get("used_by", []),
        "used_on": nd.get("note", ""),
        "sources": [{"asset": a_, "name": man[a_]["name"], "page": man[a_]["page"], "licence": "CC0 1.0",
                     "authors": man[a_]["authors"]} for a_ in m["srcs"]] + [{"procedural": "make_b1_materials.py"}],
        "normal_convention": "DirectX (green = down), like the library; make_textures.GREEN_DX flips all",
        "made_by": "research/materials/make_b1_materials.py (agent B1, 2026-09-29)",
        "requested_by": "research/%s/materials_needed.json" % ("interior" if m["where"] == "interior" else "outdoor_kit"),
    }
    if m["tile_v"] != m["tile"]:
        side["tile_size_v_m"] = m["tile_v"]
    if m["alpha"]:
        side["alpha"] = m["alpha"]
        side["render"] = {"decal": "_ca alpha = coverage; renderFlags NoZWrite (jp_m_wall_grime / vanilla decal "
                                   "pattern). RGB is the material colour everywhere, so the palette mean is meaningful.",
                          "cut": "_ca alpha = holes / tears / gaps; renderFlags AlphaTest32 (vanilla ghillie / fur "
                                 "pattern). RGB continues under the holes."}[m["alpha"]]
    if m["note"]:
        side["note"] = m["note"]
    if m["atlas"]:
        side["cells"] = atlas(m["atlas"], W)[1]
        side["fonts"] = ["research/fonts/yujisyuku/YujiSyuku-Regular.ttf (SIL OFL 1.1, Yuji Project Authors)",
                         "research/fonts/yujihentaiganaakebono/YujiHentaiganaAkebono-Regular.ttf (SIL OFL 1.1, "
                         "Yuji Project Authors)"]
    wb(os.path.join(LIB, fam, mid + ".json"), json.dumps(side, indent=1, ensure_ascii=False))
    return res


def run_checks_file(results, only):
    p = os.path.join(LIB, "checks_b1.json")
    old = []
    if only and os.path.isfile(p):
        old = [r for r in json.load(open(p, encoding="utf-8"))["results"]
               if not any(os.path.basename(r["file"]).startswith(o + "_w") for o in only)]
    allr = old + results
    allr.sort(key=lambda r: os.path.basename(r["file"]))
    wb(p, json.dumps({"check": "C1 palette (tools/matcheck), B1 materials", "results": allr}, indent=1))
    return allr


# ================================================================================================ sheets
def renders(ids, do_render):
    rd = os.path.join(BM.BUILD, "render")
    os.makedirs(rd, exist_ok=True)
    jobs = []
    for mid in ids:
        m = BYID[mid]
        for lv in range(3):
            stem = mid + "_w%d" % lv
            out = os.path.join(rd, stem + "_sphere.png")
            co = os.path.join(TEX, stem + "_co.png")
            if os.path.isfile(out) and os.path.getmtime(out) >= os.path.getmtime(co):
                continue
            n = np.asarray(Image.open(os.path.join(TEX, stem + "_nohq.png")).convert("RGB")).copy()
            if MT.GREEN_DX:
                n[..., 1] = 255 - n[..., 1]
            gl = os.path.join(rd, stem + "_nohq_gl.png")
            Image.fromarray(n).save(gl)
            jobs.append({"co": co, "nohq_gl": gl, "smdi": os.path.join(TEX, stem + "_smdi.png"),
                         "tile_m": m["tile"], "tile_v_m": m["tile_v"], "out": out})
    if jobs and do_render:
        jf = os.path.join(rd, "jobs_b1.json")
        wb(jf, json.dumps(jobs, indent=1))
        r = subprocess.run([BM.BLENDER, "--background", "--factory-startup", "--python",
                            os.path.join(HERE, "render_spheres.py"), "--", jf], capture_output=True, text=True,
                           errors="replace")
        done = sum(os.path.isfile(j["out"]) for j in jobs)
        print("blender: %d/%d spheres rendered" % (done, len(jobs)))
        if done < len(jobs):
            print((r.stdout + r.stderr)[-3000:])
    return rd


def atlas_back(mid, w, size):
    """A text atlas composited over what it sits on (stone, or a pale board), for the sheets."""
    a = Image.open(os.path.join(TEX, mid + w + "_ca.png")).convert("RGBA")
    if BYID[mid]["atlas"] == "carved":
        bg = Image.open(os.path.join(TEX, "jp_m_stone_carved_w1_co.png")).convert("RGB").resize(a.size)
    else:
        bg = Image.new("RGB", a.size, (196, 180, 150))
    bg.paste(a, (0, 0), a)
    return bg


def tile_img(mid, w, T_):
    m = BYID[mid]
    W, H = m["px"]
    th = int(round(T_ * H / W))
    if m["atlas"]:
        return atlas_back(mid, w, T_).resize((T_, th), Image.LANCZOS)
    if m["alpha"]:
        a = Image.open(os.path.join(TEX, mid + w + "_ca.png")).convert("RGBA").resize((T_, th), Image.LANCZOS)
        chk = Image.new("RGB", (T_, th), (70, 70, 70))
        d = ImageDraw.Draw(chk)
        for y in range(0, th, 16):
            for x in range(0, T_, 16):
                if (x // 16 + y // 16) % 2:
                    d.rectangle([x, y, x + 15, y + 15], fill=(200, 200, 200))
        chk.paste(a, (0, 0), a)
        return chk
    return Image.open(os.path.join(TEX, mid + w + "_co.png")).convert("RGB").resize((T_, th), Image.LANCZOS)


GROUPS_B1 = [
    ("b1_1_floors_ground", "Interior floors and ground",
     ["jp_m_floor_tatami", "jp_m_floor_tatami_heri", "jp_m_floor_boards_int", "jp_m_floor_boards_rough",
      "jp_m_floor_takeyuka", "jp_m_ground_doma_earth", "jp_m_ground_doma_tataki", "jp_m_ground_ash"]),
    ("b1_2_walls_wood_paper", "Interior walls, wood, bamboo, paper",
     ["jp_m_wall_shikkui_int", "jp_m_ceil_boards", "jp_m_wood_interior", "jp_m_bamboo_sooted", "jp_m_paper_fusuma",
      "jp_m_bamboo_weave"]),
    ("b1_3_textile_ceramic_straw", "Interior textiles, ceramics, lacquer, straw, litter decal",
     ["jp_m_textile_cotton_indigo", "jp_m_textile_cotton_plain", "jp_m_ceramic_stoneware_dark",
      "jp_m_ceramic_stoneware_pale", "jp_m_lacquer_black", "jp_m_straw_tawara", "jp_m_decal_litter"]),
    ("b1_4_outdoor_kit", "Outdoor kit",
     ["jp_m_stone_carved", "jp_m_decal_moss", "jp_m_straw_rope", "jp_m_straw_stack", "jp_m_textile_noren",
      "jp_m_textile_kinari", "jp_m_paper_chochin", "jp_m_reed_yoshizu", "jp_m_paint_shu", "jp_m_wood_endgrain",
      "jp_m_ground_leaf_litter", "jp_m_decal_carved_text", "jp_m_decal_sumi_text"]),
]


def sheets(rd, res):
    os.makedirs(SHEETS, exist_ok=True)
    F = BM.fonts()
    by = {os.path.basename(r["file"])[:-7]: r for r in res}
    T_, LW, CW, RH = 250, 600, 2 * 250 + 30, 250 + 92
    out = []
    for key, title, mids in GROUPS_B1:
        Hh = 90 + len(mids) * (RH + 18)
        Ww = LW + 3 * CW + 20
        im = Image.new("RGB", (Ww, Hh), (236, 234, 229))
        d = ImageDraw.Draw(im)
        d.text((20, 18), "jp_common B1 materials - %s" % title, font=F["h1"], fill=(20, 20, 20))
        d.text((20, 58), "Each wear level: flat tile (one full texture tile; alpha over a checker) and a lit 1 m sphere "
                         "(real texel scale, RGB only). Mean colour checked against palette.json by tools/matcheck.",
               font=F["s"], fill=(60, 60, 60))
        for i, mid in enumerate(mids):
            m = BYID[mid]
            y = 90 + i * (RH + 18)
            d.rectangle([10, y - 6, Ww - 10, y + RH + 6], outline=(190, 186, 178), width=2)
            d.text((20, y), mid, font=F["h2"], fill=(20, 20, 20))
            e = MT.PAL[m["pid"]] if m["pid"] in MT.PAL else matcheck.load_palette()[m["pid"]]
            ptxt = "Palette: %s %s, dE tol %g (%s)%s; finish %s%s" % (
                m["pid"], tuple(e["srgb"]), e["tolerance_dE76"], e.get("method"),
                ("; _w0 uses %s" % m["pbw"]["_w0"]) if m["pbw"] else "", BM.finish_for(mid),
                (", alpha " + m["alpha"]) if m["alpha"] else "")
            d.rectangle([20, y + 36, 44, y + 60], fill=tuple(e["srgb"]), outline=(0, 0, 0))
            yy = BM.wrap(d, (52, y + 38), ptxt, F["s"], 62)
            yy = BM.wrap(d, (20, yy + 6), "Used on: " + NEED[mid].get("note", ""), F["b"], 58)
            BM.wrap(d, (20, yy + 6), "Tile %.2f m, %s px, grain: %s" % (m["tile"], "x".join(map(str, m["px"])),
                                                                         m["grain"]), F["s"], 66, fill=(70, 70, 70))
            for k in range(3):
                w = "_w%d" % k
                x = LW + k * CW
                r = by.get(mid + w, {})
                d.text((x, y), ("%s %s: %s" % (w, ["clean", "normal", "heavy"][k], NEED[mid]["wear"][w]))[:62],
                       font=F["sb"], fill=(20, 20, 20))
                ti = tile_img(mid, w, T_)
                im.paste(ti, (x, y + 24 + (T_ - ti.size[1]) // 2))
                if m["atlas"]:                                    # a text atlas: a 1:1 zoom instead of a sphere
                    im.paste(atlas_back(mid, w, T_).crop((0, 0, 400, 400)).resize((T_, T_), Image.LANCZOS),
                             (x + T_ + 10, y + 24))
                else:
                    im.paste(BM.sphere_img(rd, mid, w, T_), (x + T_ + 10, y + 24))
                if r:
                    col = {"PASS": (20, 110, 40), "WARN": (170, 110, 0), "FAIL": (190, 20, 20)}[r["verdict"]]
                    d.text((x, y + T_ + 30), "mean %s  dE %.1f / %g  %s" % (
                        tuple(int(v) for v in r["mean_srgb"]), r["dE"], r["tol"], r["verdict"]), font=F["sb"], fill=col)
                    if r["warnings"]:
                        d.text((x, y + T_ + 50), "; ".join(r["warnings"])[:70], font=F["s"], fill=(120, 80, 0))
                    elif r["masked_frac"]:
                        d.text((x, y + T_ + 50), "detail mask %.0f %% (excluded from the mean)" % (
                            100 * r["masked_frac"]), font=F["s"], fill=(80, 80, 80))
        p = os.path.join(SHEETS, key + ".jpg")
        im.save(p, quality=88)
        out.append(p)
        print("sheet", p, im.size)
    cols, T2 = 4, 190
    cw, ch = 2 * T2 + 30, T2 + 50
    rows = (len(MATS) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw + 30, rows * ch + 80), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((20, 16), "jp_common B1 - all %d new materials at _w1 (normal wear)" % len(MATS), font=F["h2"],
           fill=(20, 20, 20))
    for i, m in enumerate(MATS):
        x, y = 20 + (i % cols) * cw, 60 + (i // cols) * ch
        ti = tile_img(m["id"], "_w1", T2)
        im.paste(ti, (x, y + (T2 - ti.size[1]) // 2))
        im.paste(BM.sphere_img(rd, m["id"], "_w1", T2), (x + T2 + 6, y))
        r = by.get(m["id"] + "_w1", {})
        d.text((x, y + T2 + 4), m["id"][5:], font=F["sb"], fill=(20, 20, 20))
        if r:
            d.text((x, y + T2 + 24), "%s  dE %.1f/%g %s" % (m["pid"], r["dE"], r["tol"], r["verdict"]), font=F["s"],
                   fill=(60, 60, 60))
    p = os.path.join(SHEETS, "b1_0_overview_w1.jpg")
    im.save(p, quality=88)
    out.append(p)
    print("sheet", p, im.size)
    return out


# ================================================================================================ status table
def status():
    before = set()
    made = set()
    for root, _, files in os.walk(LIB):
        for f in files:
            if f.endswith(".json") and f.startswith("jp_m_"):
                sc = json.load(open(os.path.join(root, f), encoding="utf-8"))
                (made if "make_b1_materials" in sc.get("made_by", "") else before).add(sc["id"])
    refs = {}
    for where, p in (("interior", "research/interior/BUILD_LIST.md"), ("outdoor", "research/outdoor_kit/BUILD_LIST.md")):
        txt = open(os.path.join(DEV, p), "rb").read().decode("utf-8")
        for mid in set(re.findall(r"jp_m_[a-z0-9_]+", txt)):
            refs.setdefault(mid, set()).add(where)
    rows = []
    for mid in sorted(refs):
        if mid in made:
            st, why = "made now (B1)", "%s, palette %s%s" % (BYID[mid]["fam"], BYID[mid]["pid"],
                                                            (", alpha " + BYID[mid]["alpha"]) if BYID[mid]["alpha"] else "")
        elif mid in before:
            st, why = "exists", "in jp_common before B1"
        elif mid in NOT_MADE:
            st, why = "NOT made", NOT_MADE[mid]
        else:
            st, why = "MISSING", "referenced but neither in jp_common nor made (check)"
        rows.append("| `%s` | %s | %s | %s |" % (mid, " + ".join(sorted(refs[mid])), st, why))
    n_made = sum(1 for m in refs if m in made)
    txt = ("# B1 material status: every jp_m_ name the two build lists reference\n\n"
           "Written by `make_b1_materials.py --status` (agent B1, 2026-09-29) from `research/interior/BUILD_LIST.md` "
           "and `research/outdoor_kit/BUILD_LIST.md` against the sidecars in `src/JP/common/materials/`.\n\n"
           "%d names: %d existed, %d made now, %d not made.\n\n"
           "| Material | Build list | Status | Note |\n|---|---|---|---|\n" % (
               len(refs), sum(1 for m in refs if m in before), n_made, sum(1 for m in refs if m in NOT_MADE))
           + "\n".join(rows) + "\n")
    wb(os.path.join(HERE, "B1_STATUS.md"), txt)
    print("B1_STATUS.md: %d names" % len(refs))


# ================================================================================================ main
def main(argv):
    if "--status" in argv:
        status()
        return 0
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    if "--set" in argv:
        s = argv[argv.index("--set") + 1]
        only = [m["id"] for m in MATS if m["where"] == s]
    ids = only or [m["id"] for m in MATS]
    if "--rvmats-only" in argv:
        for mid in ids:
            write_rvmats(BYID[mid])
        print("make_b1_materials: %d rvmats rewritten" % (3 * len(ids)))
        return 0 if ("--no-pack" in argv or BM.pack()) else 1
    pal = matcheck.load_palette()
    MT.PAL.update(pal)
    if "--sheets-only" in argv:
        res = json.load(open(os.path.join(LIB, "checks_b1.json"), encoding="utf-8"))["results"]
    else:
        man = json.load(open(os.path.join(BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
        res = []
        for mid in ids:
            rr = make_one(BYID[mid], pal, man)
            for r in rr:
                print("  %-4s %-34s %-18s mean %-15s dE %4.1f/%-2g paa dE %4.1f %s" % (
                    r["verdict"], os.path.basename(r["file"])[:-7], r["palette_id"], "(%d,%d,%d)" % tuple(r["mean_srgb"]),
                    r["dE"], r["tol"], r["shipped_paa"]["dE"], "; ".join(r["warnings"])))
            res += rr
        res = run_checks_file(res, only)
    bad = [r for r in res if r["verdict"] == "FAIL" or (r.get("shipped_paa") or {}).get("verdict") == "FAIL"]
    print("matcheck: %d sets, %d FAIL, %d WARN" % (len(res), len(bad), sum(r["verdict"] == "WARN" for r in res)))
    ok = not bad
    if "--sheets-only" not in argv:
        status()
        BM.credits()                                              # CREDITS.md from the Poly Haven manifest (+ B1 text)
        if "--no-pack" not in argv:
            ok = BM.pack() and ok
    rd = renders([m["id"] for m in MATS if os.path.isfile(os.path.join(TEX, m["id"] + "_w2_co.png"))],
                 "--no-render" not in argv)
    if all(os.path.isfile(os.path.join(TEX, m["id"] + "_w2_co.png")) for m in MATS):
        sheets(rd, res)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
