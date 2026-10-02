#!/usr/bin/env python3
"""Make the jp_common material library textures: 22 materials x 3 wear levels (_w0 clean, _w1 normal, _w2 heavy).

Writes data/materials/textures/<id>_w<n>_{co,nohq,smdi}.png plus <id>_w<n>_mask.png where painted-on detail exists
(moss, lichen, cracks, rust, edge wear, drips...). The mask is what matcheck excludes from the palette mean
(PLAYBOOK §8); rain streaks, silvering, soot and bloom are part of the material and are NOT masked.

Every texture tiles. Sources: CC0 Poly Haven maps in data/materials/polyhaven (fetch_sources.py), recoloured to the
palette, or procedural (numpy/PIL, periodic FFT noise, wrap-around drawing). The last step of every texture forces
the unmasked mean onto its wear target (a palette entry plus a small, logged Lab offset inside tolerance).
Normal maps are DirectX style (green = down), like agent B's proven machiya maps; GREEN_DX flips them all.
Texel density: 512 px/m everywhere (the machiya wall density Stephen approved); size = tile_size_m x 512.
Usage:  python make_textures.py [material_id ...]
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
PH = os.path.join(DEV, "data", "materials", "polyhaven")
OUT = os.path.join(DEV, "data", "materials", "textures")
PAL = {e["id"]: e for e in json.load(open(os.path.join(DEV, "playbook", "palette.json"), encoding="utf-8"))["entries"]}
NEED = json.load(open(os.path.join(DEV, "research", "exterior", "materials_needed.json"), encoding="utf-8"))
MATS = {m["id"]: m for m in NEED["materials"]}
PPM = 512
GREEN_DX = True


# ----------------------------------------------------------------------------------------------------------------
# colour
# ----------------------------------------------------------------------------------------------------------------
_M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_WP = np.array([0.95047, 1.0, 1.08883])


def srgb_to_lab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    xyz = c @ _M.T / _WP
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def lab_to_srgb(lab):
    L, a, b = lab
    fy = (L + 16) / 116
    f = np.array([fy + a / 500, fy, fy - b / 200])
    xyz = np.where(f ** 3 > 0.008856, f ** 3, (f - 16 / 116) / 7.787) * _WP
    c = np.linalg.solve(_M, xyz)
    c = np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055)
    return np.clip(c * 255, 0, 255)


def tgt(pid, dL=0.0, da=0.0, db=0.0, toward=None, t=0.0):
    """Wear target in sRGB 0-255: palette entry, optionally mixed toward another entry (weathering.worst), plus a Lab
    offset. Offsets stay well inside tolerance; matcheck verifies."""
    c = np.array(PAL[pid]["srgb"], float)
    if toward:
        c = c + (np.array(PAL[toward]["srgb"], float) - c) * t
    return lab_to_srgb(srgb_to_lab(c) + np.array([dL, da, db]))


def lum(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def recolor(a, target, contrast=1.0, chroma=0.0):
    """Keep the source's light/dark pattern (scaled by contrast) around the target colour; add back `chroma` of its
    own colour variation."""
    l = lum(a)
    d = 1.0 + contrast * (l / max(l.mean(), 1e-4) - 1.0)
    out = (np.asarray(target, np.float32) / 255.0)[None, None, :] * d[..., None]
    if chroma:
        out = out + chroma * (a - l[..., None]) * (lum(out).mean() / max(l.mean(), 1e-4))
    return np.clip(out, 0, 1).astype(np.float32)


def fix_mean(a, target, keep):
    t = np.asarray(target, np.float32) / 255.0
    for _ in range(6):
        m = a[keep].mean(0) if keep.any() else a.reshape(-1, 3).mean(0)
        a = np.clip(a * (t / np.maximum(m, 1e-4)), 0, 1)
    return a


def mix(a, col, alpha):
    """alpha: HxW (0-1); col: rgb 0-255 or HxWx3 0-1."""
    c = np.asarray(col, np.float32)
    if c.ndim == 1:
        c = c / 255.0
    al = np.clip(alpha, 0, 1)[..., None]
    return a * (1 - al) + c * al


def patch(co, m, col, alpha, seed):
    """Blend a blob (moss, dirt, grime, mildew) in softly: blurred edge, broken-up alpha, colour that follows the
    texture below, so it does not read as a flat painted shape."""
    S = co.shape[0]
    soft = np.clip(blur(np.asarray(m, np.float32), 2.5) * 1.4, 0, 1)
    brk = np.clip(0.7 + 0.45 * fbm(S, 1.6, 1, 1, seed), 0.25, 1)
    det = lum(co) / max(float(lum(co).mean()), 1e-4)
    c = (np.asarray(col, np.float32) / 255)[None, None, :] * (0.7 + 0.3 * det)[..., None]
    c = c * (1 + 0.15 * fbm(S, 2.0, 1, 1, seed + 1))[..., None]
    return mix(co, np.clip(c, 0, 1), soft * brk * alpha)


def grey(a, k):
    """desaturate by k (0..1)."""
    return mix(a, np.repeat(lum(a)[..., None], 3, -1), np.full(a.shape[:2], k, np.float32))


# ----------------------------------------------------------------------------------------------------------------
# noise, drawing (everything periodic so textures tile)
# ----------------------------------------------------------------------------------------------------------------
def fbm(n, beta=2.0, fx=1.0, fy=1.0, seed=0, lowcut=0.0):
    """Periodic spectral noise, zero mean, unit std. fx/fy > 1 suppress x/y frequencies (fy large = streaks along v)."""
    r = np.random.default_rng(seed)
    F = np.fft.fft2(r.standard_normal((n, n)))
    ky = np.fft.fftfreq(n)[:, None] * n
    kx = np.fft.fftfreq(n)[None, :] * n
    k = np.sqrt((kx * fx) ** 2 + (ky * fy) ** 2)
    k[0, 0] = 1.0
    amp = k ** (-beta / 2.0)
    amp[0, 0] = 0.0
    if lowcut:
        amp[np.sqrt(kx ** 2 + ky ** 2) < lowcut] = 0.0
    x = np.real(np.fft.ifft2(F * amp))
    x -= x.mean()
    return (x / (x.std() + 1e-9)).astype(np.float32)


def blur(a, r):
    if r <= 0:
        return a
    n = a.shape[0]
    # float gaussian via FFT (periodic)
    ky = np.fft.fftfreq(n)[:, None]
    kx = np.fft.fftfreq(n)[None, :]
    g = np.exp(-2 * (math.pi ** 2) * (r ** 2) * (kx ** 2 + ky ** 2))
    if a.ndim == 2:
        return np.real(np.fft.ifft2(np.fft.fft2(a) * g)).astype(np.float32)
    return np.stack([np.real(np.fft.ifft2(np.fft.fft2(a[..., c]) * g)) for c in range(a.shape[2])], -1).astype(np.float32)


def offsets(xs, ys, r, S):
    ox = [0] + ([S] if min(xs) - r < 0 else []) + ([-S] if max(xs) + r >= S else [])
    oy = [0] + ([S] if min(ys) - r < 0 else []) + ([-S] if max(ys) + r >= S else [])
    return [(a, b) for a in ox for b in oy]


class Wrap:
    """PIL drawing on an S x S image; every shape is repeated across the edges so the result tiles."""

    def __init__(self, S, mode="L", fill=0):
        self.S = S
        self.im = Image.new(mode, (S, S), fill)
        self.d = ImageDraw.Draw(self.im)

    def line(self, pts, fill, width=1):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        for ox, oy in offsets(xs, ys, width + 2, self.S):
            self.d.line([(x + ox, y + oy) for x, y in pts], fill=fill, width=width)

    def ellipse(self, cx, cy, rx, ry, fill, outline=None, width=1):
        for ox, oy in offsets([cx], [cy], max(rx, ry) + 2, self.S):
            self.d.ellipse([cx - rx + ox, cy - ry + oy, cx + rx + ox, cy + ry + oy], fill=fill, outline=outline, width=width)

    def polygon(self, pts, fill, outline=None):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        for ox, oy in offsets(xs, ys, 2, self.S):
            self.d.polygon([(x + ox, y + oy) for x, y in pts], fill=fill, outline=outline)

    def rect(self, x0, y0, x1, y1, fill):
        self.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill)

    def arr(self):
        return np.asarray(self.im).astype(np.float32) / 255.0


def cracks(S, count, seed, seg=(5, 11), steps=(8, 30), width=1, jitter=0.45, branch=0.08):
    w = Wrap(S)
    r = np.random.default_rng(seed)
    stack = [(r.uniform(0, S), r.uniform(0, S), r.uniform(0, 2 * math.pi), int(r.integers(*steps))) for _ in range(count)]
    while stack:
        x, y, ang, n = stack.pop()
        pts = [(x, y)]
        for _ in range(n):
            ang += r.normal(0, jitter)
            L = r.uniform(*seg)
            x, y = x + L * math.cos(ang), y + L * math.sin(ang)
            pts.append((x, y))
            if r.random() < branch and n > 4:
                stack.append((x, y, ang + r.choice([-1, 1]) * r.uniform(0.6, 1.2), n // 2))
        w.line(pts, 255, width)
    return w.arr()


def spots(S, clusters, per, rmin, rmax, spread, seed):
    """Clustered round spots (lichen, rust bloom, moss seeds). Returns coverage 0-1."""
    w = Wrap(S)
    r = np.random.default_rng(seed)
    for _ in range(clusters):
        cx, cy = r.uniform(0, S, 2)
        for _ in range(int(r.integers(max(1, per // 2), per + 1))):
            x, y = cx + r.normal(0, spread), cy + r.normal(0, spread)
            rr = r.uniform(rmin, rmax)
            w.ellipse(x, y, rr, rr * r.uniform(0.7, 1.0), 255)
    return w.arr()


def vstreaks(S, seed, strength=1.0, fy=14.0):
    """Rain / soot streaks running down the texture (v), 0-1, tileable."""
    return np.clip(fbm(S, 2.0, 1.0, fy, seed) * 0.6 + 0.2, 0, 1.6) * strength


# ----------------------------------------------------------------------------------------------------------------
# sources and maps
# ----------------------------------------------------------------------------------------------------------------
def photo(asset, kind, S, tiles=1):
    im = Image.open(os.path.join(PH, asset, "%s_%s_1k.jpg" % (asset, kind))).convert("RGB")
    t = S // tiles
    a = np.asarray(im.resize((t, t), Image.LANCZOS)).astype(np.float32) / 255.0
    return np.tile(a, (tiles, tiles, 1))


def pnormal(asset, S, tiles=1, k=1.0):
    n = photo(asset, "nor_dx", S, tiles) * 2.0 - 1.0
    return flatten(n, k)


def prough(asset, S, tiles=1):
    return photo(asset, "rough", S, tiles)[..., 0]


def flatten(n, k):
    n = n.copy()
    n[..., :2] *= k
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def h2n(h, s):
    """height (any units) -> tangent normal (DirectX: +y = down the texture)."""
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * s
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * s
    n = np.stack([-dx, -dy if GREEN_DX else dy, np.ones_like(h)], -1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def combine(n1, n2):
    n = np.stack([n1[..., 0] + n2[..., 0], n1[..., 1] + n2[..., 1], n1[..., 2] * n2[..., 2]], -1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def flat_n(S):
    n = np.zeros((S, S, 3), np.float32)
    n[..., 2] = 1
    return n


def trim_tile_v(a, top_frac, band):
    """Cut a feature strip off the top of a photo and make it tile vertically (half-offset cross-fade near the seam)."""
    S = a.shape[0]
    c0 = int(S * top_frac)
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).crop((0, c0, S, S)).resize((S, S), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    a2 = np.roll(a, S // 2, axis=0)
    y = np.arange(S, dtype=np.float32)
    w = np.clip(np.minimum(y, S - 1 - y) / band, 0, 1)[:, None, None]
    return a * w + a2 * (1 - w)


# ----------------------------------------------------------------------------------------------------------------
# recipes: each returns dict(co, n, rough, mask[, spec, gloss]); lv = 0, 1, 2
# ----------------------------------------------------------------------------------------------------------------
def R(co, n, rough, mask=None, spec=0.2, gloss=0.3, target=None):
    S = co.shape[0]
    return {"co": co, "n": n, "rough": np.clip(rough, 0, 1), "mask": np.zeros((S, S), bool) if mask is None else mask,
            "spec": spec, "gloss": gloss, "target": target}


def edge_lines(S, count, seed, wmin=2, wmax=4, seg=(20, 90)):
    """Broken vertical wear lines (plank edges, lattice corners)."""
    w = Wrap(S)
    r = np.random.default_rng(seed)
    for _ in range(count):
        x = r.uniform(0, S)
        y = r.uniform(0, S)
        L = r.uniform(*seg)
        w.line([(x, y), (x + r.normal(0, 1.5), y + L)], 255, int(r.integers(wmin, wmax + 1)))
    return w.arr()


def wood_weathered(lv, S):
    a, pn, pr = photo("weathered_planks", "diff", S), pnormal("weathered_planks", S), prough("weathered_planks", S)
    t = [tgt("timber_weathered", 2, 1, 3), tgt("timber_weathered", toward="stone_lantern", t=0.15),
         tgt("timber_weathered", -3, toward="stone_lantern", t=0.30)][lv]
    co = recolor(a, t, [1.15, 1.05, 1.0][lv], [0.55, 0.3, 0.12][lv])
    mask = np.zeros((S, S), bool)
    h = np.zeros((S, S), np.float32)
    if lv >= 1:                                                   # W3 silvering: greyer, fine pale streaks
        co = grey(co, [0, 0.3, 0.55][lv]) * (1 + 0.05 * fbm(S, 2.0, 1, 10, 11))[..., None]
    if lv == 2:                                                   # splits along the grain + grime blotches
        sp = edge_lines(S, 90, 12, 1, 2, (40, 220))
        g = blur((fbm(S, 3.0, 1, 1, 13) > 1.35).astype(np.float32), 2) > 0.5
        co = mix(co, (30, 26, 24), sp * 0.85)
        co = patch(co, g, (52, 46, 40), 0.6, 14)
        h -= sp * 2.0
        mask = (sp > 0.3) | g
    n = combine(pn, h2n(h, 1.0))
    return R(co, n, pr * [0.9, 0.95, 1.0][lv], mask, 0.2, 0.3, t)


def cedar_dark(lv, S, t, contrast, chroma):
    a = photo("japanese_cedar_planks", "diff", S)
    return recolor(a, t, contrast, chroma), pnormal("japanese_cedar_planks", S), prough("japanese_cedar_planks", S)


def wood_street_dark(lv, S):
    t = [tgt("timber_street_dark", -1), tgt("timber_street_dark", 1), tgt("timber_street_dark", 4, -2, -2)][lv]
    co, pn, pr = cedar_dark(lv, S, t, 1.0, 0.15)
    mask = np.zeros((S, S), bool)
    h = np.zeros((S, S), np.float32)
    if lv >= 1:                                                   # W7 edge wear
        e = edge_lines(S, [0, 45, 90][lv], 21 + lv)
        co = mix(co, (150, 112, 80) if lv == 1 else (170, 140, 110), e * 0.75)
        mask |= e > 0.3
    if lv == 2:                                                   # dust + raised grain
        d = np.clip(fbm(S, 3.0, 1, 1, 23) * 0.5 + 0.4, 0, 1)
        co = mix(co, (120, 108, 96), d * 0.3)
        h += (lum(co) - blur(lum(co), 3)) * 25
    n = combine(flatten(pn, [1.0, 1.1, 1.5][lv]), h2n(h, 1.0))
    return R(co, n, pr * [0.75, 0.9, 1.0][lv], mask, [0.35, 0.3, 0.2][lv], [0.5, 0.4, 0.3][lv], t)


def wood_bengara(lv, S):
    t = [tgt("bengara_lattice", 0, 9, 1), tgt("bengara_lattice", 1, 8, 1), tgt("bengara_lattice", 3, 5, 1)][lv]
    a = photo("japanese_cedar_planks", "diff", S)
    paint = recolor(a, t, 0.55, 0.0) * (1 + 0.04 * fbm(S, 2.0, 1, 8, 31))[..., None]
    wood = recolor(a, (112, 92, 76), 1.1, 0.04)
    m = np.zeros((S, S), np.float32)
    if lv >= 1:
        m = np.maximum(m, edge_lines(S, [0, 50, 70][lv], 32 + lv, 2, 5))
    if lv == 2:
        m = np.maximum(m, (blur((fbm(S, 2.5, 1, 3, 33) > 1.15).astype(np.float32), 1.5) > 0.5).astype(np.float32))
    co = mix(paint, wood, m)
    n = pnormal("japanese_cedar_planks", S, k=[0.6, 0.7, 0.9][lv])
    return R(co, n, prough("japanese_cedar_planks", S) * [0.7, 0.8, 0.95][lv], m > 0.3, 0.3, 0.4, t)


def wood_kuro(lv, S):
    t = [tgt("kuro_board"), tgt("kuro_board", 3.5), tgt("kuro_board", 4.0)][lv]
    a = photo("black_painted_planks", "diff", S)
    co = recolor(a, t, 1.0, 0.2)
    mask = np.zeros((S, S), bool)
    if lv >= 1:                                                   # grey bloom (weathered sumi / charring)
        co = co + [0, 0.035, 0.05][lv] * np.clip(fbm(S, 3.0, 1, 1, 41) * 0.5 + 0.5, 0, 1.5)[..., None]
    if lv == 2:
        e = edge_lines(S, 70, 42, 2, 4)
        co = mix(co, (105, 80, 62), e * 0.8)
        mask = e > 0.3
    return R(np.clip(co, 0, 1), pnormal("black_painted_planks", S), prough("black_painted_planks", S), mask, 0.25, 0.35, t)


def wood_sooted(lv, S):
    t = [tgt("timber_sooted", 1), tgt("timber_sooted", -1), tgt("timber_sooted", -1.5)][lv]
    co, pn, pr = cedar_dark(lv, S, t, 1.2, 0.05)
    h = np.zeros((S, S), np.float32)
    if lv >= 1:                                                   # soot streaks
        co = co * (1 - 0.35 * np.clip(vstreaks(S, 51, 1.0, 12), 0, 1))[..., None]
    if lv == 2:                                                   # crusted soot
        c = fbm(S, 1.3, 1, 1, 52)
        h += np.clip(c, 0, None) * 1.2
        co = co * (1 - 0.25 * (c > 0.6))[..., None]
    n = combine(flatten(pn, 0.8), h2n(h, 1.0))
    return R(co, n, pr * [1.0, 0.95, 0.85][lv], None, 0.15, 0.25, t)


def straw_flecks(S, count, seed, lmin, lmax, col=(196, 168, 110)):
    w, tone = Wrap(S), Wrap(S)
    r = np.random.default_rng(seed)
    for _ in range(count):
        x, y = r.uniform(0, S, 2)
        ang = r.uniform(0, math.pi)
        L = r.uniform(lmin, lmax)
        pts = [(x, y), (x + L * math.cos(ang), y + L * math.sin(ang))]
        w.line(pts, 255, 1 if r.random() < 0.7 else 2)
        tone.line(pts, int(r.uniform(150, 255)), 1)
    return w.arr(), tone.arr()


def earth_wall(lv, S, fine):
    a = photo("clay_plaster", "diff", S)
    if fine:
        a = blur(a, 1.2)
    pn = pnormal("clay_plaster", S, k=0.5 if fine else 1.0)
    return a, pn, prough("clay_plaster", S)


def wall_arakabe(lv, S):
    t = [tgt("earth_wall_aged", 4, 1, 4), tgt("earth_wall_aged"), tgt("earth_wall_aged", -2, 0, -2)][lv]
    a, pn, pr = earth_wall(lv, S, False)
    hc = fbm(S, 2.2, 1, 1, 61) + 0.4 * fbm(S, 1.4, 1, 1, 62)
    co = recolor(a, t, 1.2, 0.4) * (1 + 0.05 * hc)[..., None]
    h = hc * 1.2
    mask = np.zeros((S, S), bool)
    sa, st = straw_flecks(S, [1400, 700, 1100][lv], 63 + lv, 8, 24)
    co = mix(co, (200, 172, 112) if lv == 0 else (150, 130, 95), sa * st * [0.75, 0.45, 0.55][lv])
    h += sa * 0.8
    if lv >= 1:                                                   # W2 rain streaks
        co = co * (1 - 0.09 * np.clip(vstreaks(S, 64, 1.0, 14), 0, 1.3))[..., None]
    if lv == 2:                                                   # eroded patches, bamboo lath (komai) in the worst
        e = blur(fbm(S, 2.6, 1, 1, 65), 1.5)
        pat = e > 1.05
        h -= np.clip(e - 1.05, 0, None) * 6
        co = co * (1 - 0.12 * pat)[..., None]
        yy, xx = np.mgrid[0:S, 0:S]
        lath = (((xx % 25) < 9) | ((yy % 25) < 9)) & (e > 1.75)
        co[lath] = (co[lath] * 0.3 + np.array([150, 128, 92], np.float32) / 255 * 0.7)
        h[lath] += 1.5
        sa2, _ = straw_flecks(S, 900, 66, 10, 28)
        co = mix(co, (170, 150, 105), sa2 * pat * 0.6)
        mask = lath
    n = combine(pn, h2n(h, 1.5))
    return R(co, n, pr, mask, 0.1, 0.2, t)


def trowel(S, seed, count):
    w = Wrap(S)
    r = np.random.default_rng(seed)
    for _ in range(count):
        cx, cy = r.uniform(0, S, 2)
        rad = r.uniform(60, 160)
        a0 = r.uniform(0, 360)
        pts = [(cx + rad * math.cos(math.radians(a)), cy + rad * math.sin(math.radians(a)))
               for a in np.linspace(a0, a0 + r.uniform(30, 80), 16)]
        w.line(pts, int(r.uniform(90, 200)), 1)
    return blur(w.arr(), 1.0)


def wall_nakanuri(lv, S):
    t = [tgt("earth_wall_aged", 6, 0, 2), tgt("earth_wall_aged", 2), tgt("earth_wall_aged", 0, 0, -1)][lv]
    a, pn, pr = earth_wall(lv, S, True)
    co = recolor(a, t, 1.6, 0.35) * (1 + 0.035 * fbm(S, 2.4, 1, 1, 70))[..., None]
    h = trowel(S, 71, 260) * 1.5
    mask = np.zeros((S, S), bool)
    if lv >= 1:
        co = co * (1 - 0.08 * np.clip(vstreaks(S, 72, 1.0, 14), 0, 1.3))[..., None]
    if lv == 2:
        p = Wrap(S)                                               # patched repairs, a shade off
        r = np.random.default_rng(73)
        for _ in range(7):
            cx, cy = r.uniform(0, S, 2)
            pts = [(cx + r.uniform(40, 110) * math.cos(k), cy + r.uniform(40, 110) * math.sin(k))
                   for k in np.linspace(0, 2 * math.pi, 9)[:-1]]
            p.polygon(pts, int(r.choice([60, 200])))
        pa = blur(p.arr(), 2.0)
        co = co * (1 + 0.07 * (pa - 0.5 * (pa > 0.05)))[..., None]
        c = cracks(S, 34, 74)
        co = mix(co, (48, 40, 32), c * 0.8)
        h -= c * 2.0
        mask = c > 0.3
    n = combine(pn, h2n(h, 1.0))
    return R(co, n, pr, mask, 0.12, 0.25, t)


def wall_shikkui(lv, S):
    t = [tgt("shikkui_white", -3), tgt("shikkui_white", -7), tgt("shikkui_white", -10, toward="earth_wall_ochre", t=0.2)][lv]
    a = photo("white_plaster_02", "diff", S, tiles=2)
    co = recolor(a, t, 0.6, 0.2)
    pn = pnormal("white_plaster_02", S, tiles=2, k=0.7)
    h = np.zeros((S, S), np.float32)
    mask = np.zeros((S, S), bool)
    if lv >= 1:                                                   # grey streaks under eaves and sills
        co = co * (1 - [0, 0.10, 0.12][lv] * np.clip(vstreaks(S, 81, 1.0, 16), 0, 1.4))[..., None]
    if lv == 2:
        c = cracks(S, 26, 82, seg=(4, 9), jitter=0.55)
        g = blur((fbm(S, 3.0, 1, 2, 83) > 1.25).astype(np.float32), 3) > 0.45
        co = mix(co, (120, 112, 100), c * 0.7)
        co = patch(co, g, (140, 128, 108), 0.45, 84)
        h -= c * 1.5
        mask = (c > 0.3) | g
    n = combine(pn, h2n(h, 1.0))
    return R(co, n, prough("white_plaster_02", S, 2), mask, 0.15, 0.25, t)


def wall_namako_tile(lv, S):
    t = [tgt("namako_tile"), tgt("namako_tile", 1), tgt("namako_tile", 2)][lv]
    r = np.random.default_rng(91)
    k = 4
    c = S // k
    yy, xx = np.mgrid[0:S, 0:S]
    tint = 1 + 0.12 * r.standard_normal((k, k))
    tile_tint = tint[yy // c, xx // c].astype(np.float32)
    de = np.minimum(np.minimum(xx % c, c - 1 - xx % c), np.minimum(yy % c, c - 1 - yy % c)).astype(np.float32)
    bevel = np.clip(de / 6.0, 0, 1)
    base = np.asarray(t, np.float32) / 255
    co = base[None, None, :] * (tile_tint * (1 + 0.09 * fbm(S, 2.2, 1, 1, 92)) * (0.8 + 0.2 * bevel))[..., None]
    h = bevel * 2.0 + 0.15 * fbm(S, 1.4, 1, 1, 93)
    mask = np.zeros((S, S), bool)
    if lv >= 1:                                                   # lime-wash drips from the top joint of each tile
        w = Wrap(S)
        for i in range(k):
            for j in range(k):
                for _ in range(int(r.integers(1, 3 if lv == 1 else 4))):
                    x = j * c + r.uniform(8, c - 8)
                    y0 = i * c + 2
                    L = r.uniform(10, 60 if lv == 1 else 90)
                    wd = r.uniform(2, 4)
                    w.line([(x, y0), (x + r.normal(0, 1), y0 + L)], 255, int(wd))
                    w.ellipse(x, y0 + L, wd * 0.7, wd * 0.9, 255)
        dr = w.arr()
        co = mix(co, (190, 190, 184), dr * 0.55)
        mask |= dr > 0.3
    if lv == 2:                                                   # chipped corners, stained joints
        w = Wrap(S)
        for i in range(k):
            for j in range(k):
                if r.random() < 0.45:
                    cx, cy = j * c + r.choice([0, c]), i * c + r.choice([0, c])
                    pts = [(cx + r.uniform(-18, 18), cy + r.uniform(-18, 18)) for _ in range(5)]
                    w.polygon(pts, 255)
        ch = w.arr()
        stain = (de < 10) & (fbm(S, 2.5, 1, 1, 94) > 0.3)
        co = mix(co, (96, 86, 74), ch * 0.9)
        co = mix(co, (70, 60, 44), stain * 0.6)
        h -= ch * 2.0
        mask |= (ch > 0.3) | stain
    n = h2n(h, 1.2)
    return R(co, n, 0.55 - 0.1 * bevel, mask, 0.35, 0.45, t)


def roof_kawara(lv, S):
    t = [tgt("kawara_ibushi", 1), tgt("kawara_ibushi", -8, 0, -1), tgt("kawara_ibushi", -9, toward="kawara_weathered", t=0.7)][lv]  # -9: parts agent 2026-09-27, keeps _w2 near _w1 after the darker calibrated entry
    base = np.asarray(t, np.float32) / 255
    m = 0.045 * fbm(S, 2.8, 1, 1, 101) + 0.035 * fbm(S, 1.2, 1, 1, 102)
    if lv >= 1:                                                   # W8: stronger tile-scale tone changes
        m = m + [0, 0.07, 0.06][lv] * fbm(S, 2.0, 1, 1, 103, lowcut=3)
    smoke = np.clip(fbm(S, 3.2, 1, 1, 104) - 0.8, 0, None)       # ibushi smoke blotches
    co = base[None, None, :] * ((1 + m) * (1 - 0.12 * smoke))[..., None]
    h = 0.3 * fbm(S, 1.2, 1, 1, 105) + 0.6 * fbm(S, 2.4, 1, 1, 106)
    rough = 0.32 + 0.12 * np.clip(m * 4, -1, 1) + [0, 0.08, 0.22][lv]
    mask = np.zeros((S, S), bool)
    if lv == 2:                                                   # W6 lichen crusts
        l1 = spots(S, 40, 14, 2, 9, 22, 107)
        l2 = spots(S, 25, 8, 3, 12, 18, 108)
        co = mix(co, (178, 176, 146), l1 * 0.85)
        co = mix(co, (196, 194, 184), l2 * 0.8)
        h += (l1 + l2) * 0.8
        mask = (l1 + l2) > 0.3
    return R(co, h2n(h, 1.0), rough, mask, 0.6, 0.65, t)


def reed(S):
    a = trim_tile_v(photo("reed_roof_04", "diff", S), 0.09, S // 8)
    n = trim_tile_v(photo("reed_roof_04", "nor_dx", S), 0.09, S // 8) * 2 - 1
    r = trim_tile_v(photo("reed_roof_04", "rough", S), 0.09, S // 8)[..., 0]
    return a, n / np.linalg.norm(n, axis=-1, keepdims=True), r


def courses(S, n, seed, amp=1.0):
    """Faint layering of thatch bundles: a step and a shadow every S/n rows, edges wavy."""
    yy = np.arange(S, dtype=np.float32)[:, None]
    wav = 8 * np.repeat(fbm(S, 2.2, 1, 1, seed)[:1], S, 0)
    ph = ((yy + wav) % (S / n)) / (S / n)                         # 0 at a course top -> 1 at the next
    h = ph * amp
    sh = np.exp(-ph * 14.0)                                       # shadow just below each course edge
    return h, sh


def roof_thatch(lv, S):
    t = [tgt("thatch_new", -2), tgt("thatch_weathered", 3), tgt("thatch_weathered", -3, toward="stone_lantern", t=0.18)][lv]
    a, pn, pr = reed(S)
    co = recolor(a, t, [1.1, 1.2, 1.25][lv], [0.6, 0.2, 0.1][lv])
    h, sh = courses(S, 5, 111, 1.0)
    co = co * (1 - 0.18 * sh)[..., None]
    mask = np.zeros((S, S), bool)
    if lv == 2:                                                   # sagging hollows (FX3 2026-10-01: the W6 moss
        h = h - 3.0 * np.clip(fbm(S, 3.2, 1, 1, 114) - 0.5, 0, None)   # lives in the rvmat macro, make_wood_atlas.py:
        #                                                           a 2 m tile repeated it in rows on K2's roof)
    n = combine(pn, h2n(h, 2.0))
    return R(co, n, pr, mask, 0.08, 0.15, t)


def roof_thatch_cut(lv, S):
    t = [tgt("thatch_new", -4), tgt("thatch_weathered", 5), tgt("thatch_weathered", -2, toward="stone_lantern", t=0.15)][lv]
    r = np.random.default_rng(121 + lv)
    tone, hole, ht = Wrap(S), Wrap(S), Wrap(S)
    n_st = int(S * S * 0.8 / (math.pi * 2.3 ** 2) * 1.6)
    for _ in range(n_st):
        x, y = r.uniform(0, S, 2)
        rr = r.uniform(1.4, 2.8)
        if lv == 2 and r.random() < 0.12:
            continue                                              # ragged: missing stalks
        v = int(r.uniform(150, 255))
        tone.ellipse(x, y, rr, rr * r.uniform(0.75, 1.0), v)
        ht.ellipse(x, y, rr, rr, 255)
        if rr > 1.9:
            hole.ellipse(x, y, 0.6, 0.6, 255)
    tn, ho, hh = tone.arr(), hole.arr(), blur(ht.arr(), 0.6)
    yy = np.arange(S, dtype=np.float32)[:, None]
    wav = 10 * np.repeat(fbm(S, 2.2, 1, 1, 125)[:1], S, 0)
    band = np.sin((yy + wav) / S * 2 * math.pi * 3)               # the 2-3 light/dark layers of a cut eave (Morse)
    bamp = [0.05, 0.16, 0.12][lv]
    val = np.where(tn > 0, 0.68 + 0.3 * tn, 0.45) * (1 - 0.55 * ho) * (1 + bamp * band)
    base = np.asarray(t, np.float32) / 255
    co = base[None, None, :] * val[..., None] * (1 + 0.06 * fbm(S, 2.0, 1, 1, 126))[..., None]
    if lv == 2:
        co = grey(co, 0.25)
    n = h2n(hh * 1.5 - ho * 1.0, 1.5)
    return R(np.clip(co, 0, 1), n, 0.9 - 0.1 * tn, None, 0.08, 0.15, t)


def boards(lv, S, exposure_m, wmin_m, wmax_m, seed, tint_sd, curl=0.0, lift=0.0):
    """Split boards / shingles in courses; grain and v run down-slope. Returns (value 0-~1.2, height, board_id)."""
    g = lum(photo("wood_planks_grey", "diff", S))
    g = g / g.mean()
    r = np.random.default_rng(seed)
    nc = max(1, int(round(S / (exposure_m * PPM))))
    ch = S / nc
    val = np.zeros((S, S), np.float32)
    h = np.zeros((S, S), np.float32)
    yy = np.arange(S)
    split = fbm(S, 1.6, 1, 14, seed + 1)
    butts = []
    for k in range(nc):
        y0, y1 = int(round(k * ch)), int(round((k + 1) * ch))
        rows = yy[y0:y1]
        ph = (rows - y0) / max(1, (y1 - y0))
        x0 = x = r.uniform(0, S)
        edges = [x0]
        while True:
            x += r.uniform(wmin_m, wmax_m) * PPM
            if x >= x0 + S - wmin_m * PPM * 0.5:
                break
            edges.append(x)
        edges.append(x0 + S)
        butts.append(y1)
        for b in range(len(edges) - 1):
            xa, xb = edges[b], edges[b + 1]
            cols = np.arange(int(math.floor(xa)), int(math.ceil(xb))) % S
            sx, sy = int(r.integers(0, S)), int(r.integers(0, S))
            src = g[np.ix_((rows + sy) % S, (cols + sx) % S)]
            tint = 1 + tint_sd * r.standard_normal()
            hb = ph[:, None] * (1.0 + (curl * r.uniform(0.5, 1.5) * ph[:, None] ** 2 if curl else 0))
            if lift and r.random() < lift:
                hb = hb * 2.2
                tint *= 0.85
            val[np.ix_(rows, cols)] = src * tint * (1 + 0.05 * split[np.ix_(rows, cols)])
            h[np.ix_(rows, cols)] = hb + 0.15 * split[np.ix_(rows, cols)]
            # joint gap
            for xe in (xa,):
                c0 = int(math.floor(xe)) % S
                val[np.ix_(rows, [c0, (c0 + 1) % S])] *= 0.35
                h[np.ix_(rows, [c0, (c0 + 1) % S])] -= 0.4
    for y1 in butts:                                              # butt shadow cast on the course below
        yb = np.arange(y1, y1 + int(ch * 0.25) + 3) % S
        fall = np.exp(-np.arange(len(yb)) / max(2.0, ch * 0.07))[:, None]
        val[yb] *= (1 - 0.45 * fall)
    return val, h


def roof_boards_common(lv, S, t, exposure, wmin, wmax, seed, curl=0.0):
    val, h = boards(lv, S, exposure, wmin, wmax, seed, [0.05, 0.07, 0.1][lv], curl=curl,
                    lift=[0, 0, 0.08][lv] if curl == 0 else 0)
    base = np.asarray(t, np.float32) / 255
    co = base[None, None, :] * (1 + 0.9 * (val - 1))[..., None]
    co = np.clip(co * (1 + 0.04 * fbm(S, 2.4, 1, 1, seed + 5))[..., None], 0, 1)
    mask = np.zeros((S, S), bool)
    if lv == 0:                                                   # paler, warmer: fresh wood still showing
        co = mix(co, np.clip(co * np.array([1.08, 1.0, 0.9]), 0, 1), np.full((S, S), 0.8))
    if lv == 2:                                                   # W6 moss along the butts
        mo = spots(S, 30, 10, 3, 9, 20, seed + 6) * (fbm(S, 2.0, 1, 1, seed + 7) > -0.2)
        co = patch(co, mo, (84, 96, 52), 0.85, 157)
        mask = mo > 0.3
    return co, h, mask


def roof_kureita(lv, S):
    t = [tgt("board_new"), tgt("roof_board_silver"), tgt("roof_board_silver", -8)][lv]      # _w0 = board_new (2026-09-27)
    co, h, mask = roof_boards_common(lv, S, t, 0.25, 0.12, 0.30, 131)
    return R(co, h2n(h * 6.0, 1.0), 0.8 + 0.1 * lv, mask, 0.2, 0.3, t)


def roof_kokera(lv, S):
    t = [tgt("board_new", -2), tgt("roof_board_silver", 2), tgt("roof_board_silver", -8)][lv]  # _w0 = board_new
    co, h, mask = roof_boards_common(lv, S, t, 2.0 / 22, 0.06, 0.13, 141, curl=[0, 0, 1.2][lv])
    return R(co, h2n(h * 4.0, 1.0), 0.8 + 0.1 * lv, mask, 0.2, 0.3, t)


def roof_kakigara(lv, S):
    t = [tgt("kakigara_shell", 3), tgt("kakigara_shell", -5), tgt("kakigara_shell", -8)][lv]
    bt = [tgt("roof_board_silver", 4), tgt("roof_board_silver", -2), tgt("roof_board_silver", -8)][lv]
    co, h, mask = roof_boards_common(lv, S, bt, 2.0 / 22, 0.06, 0.13, 151)
    r = np.random.default_rng(152 + lv)
    img = Image.fromarray((co * 255).astype(np.uint8))
    hh = Image.fromarray(np.clip((h / max(h.max(), 1e-3)) * 120, 0, 255).astype(np.uint8))
    wc, wh = Wrap(S, "RGB"), Wrap(S)
    wc.im, wh.im = img, hh
    wc.d, wh.d = ImageDraw.Draw(img), ImageDraw.Draw(hh)
    count = [2900, 2500, 1100][lv]
    shell = [np.array([206, 202, 192]), np.array([178, 176, 170]), np.array([170, 168, 162])][lv]
    for _ in range(count):
        cx, cy = r.uniform(0, S, 2)
        L = r.uniform(26, 46) / 2
        W = L * r.uniform(0.6, 0.8)
        ang = r.uniform(0, math.pi)
        pts = [(cx + L * math.cos(q) * math.cos(ang) - W * math.sin(q) * math.sin(ang),
                cy + L * math.cos(q) * math.sin(ang) + W * math.sin(q) * math.cos(ang))
               for q in np.linspace(0, 2 * math.pi, 14)[:-1]]
        pts = [(x + r.normal(0, 1.2), y + r.normal(0, 1.2)) for x, y in pts]
        f = r.uniform(0.82, 1.05)
        col = tuple(int(v) for v in np.clip(shell * f, 0, 255))
        rim = tuple(int(v) for v in np.clip(shell * f * 0.62, 0, 255))
        wc.polygon(pts, col, rim)
        inner = [(cx + (x - cx) * 0.55, cy + (y - cy) * 0.55) for x, y in pts]
        wc.line(inner + inner[:1], tuple(int(v) for v in np.clip(shell * f * 0.8, 0, 255)), 1)
        wh.polygon(pts, 200, 150)
        wh.polygon(inner, 255)
    co = np.asarray(img).astype(np.float32) / 255
    h2 = blur(np.asarray(hh).astype(np.float32) / 255, 0.8)
    if lv >= 1:                                                   # dirt in the gaps between shells
        co = co * (1 - 0.12 * np.clip(fbm(S, 2.5, 1, 1, 155), 0, 1))[..., None]
    if lv == 2:
        mo = spots(S, 35, 10, 3, 9, 20, 156)
        co = patch(co, mo, (84, 96, 52), 0.85, 157)
        mask = mask | (mo > 0.3)
    return R(co, h2n(h2 * 4.0, 1.0), 0.6 + 0.1 * lv, mask, 0.3, 0.35, t)


def stone(asset, pid, lv, S, t, chroma, nk=1.0, seed=0):
    a = photo(asset, "diff", S)
    co = recolor(a, t, 1.0, chroma)
    return co, pnormal(asset, S, k=nk), prough(asset, S)


def lichen_moss(co, S, lv, seed, lichen, moss):
    mask = np.zeros((S, S), bool)
    if lichen:
        l1 = spots(S, lichen, 10, 2, 7, 16, seed)
        l2 = spots(S, lichen // 2, 6, 2, 6, 12, seed + 1)
        co = mix(co, (176, 176, 146), l1 * 0.55)
        co = mix(co, (196, 166, 96), l2 * 0.5)
        mask |= (l1 + l2) > 0.3
    if moss:
        mo = blur((fbm(S, 2.4, 1, 1, seed + 2) > moss).astype(np.float32), 2) > 0.5
        co = patch(co, mo, (70, 84, 40), 0.85, seed + 3)
        mask |= mo
    return co, mask


def stone_field(lv, S):
    t = [tgt("stone_granite", 1), tgt("stone_granite", -2), tgt("stone_granite", -4)][lv]
    co, n, r = stone("worn_rock_natural_01", "stone_granite", lv, S, t, 0.6)
    co, mask = lichen_moss(co, S, lv, 161, [0, 30, 20][lv], [None, None, 0.9][lv])
    return R(co, n, r, mask, 0.25, 0.35, t)


def stone_cut(lv, S):
    t = [tgt("stone_granite", 2), tgt("stone_granite", -1), tgt("stone_granite", -3)][lv]
    co, pn, r = stone("rock_surface", "stone_granite", lv, S, t, 0.4, nk=0.7)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    ang = math.radians(35)
    per = 9.0 * (S / 512)
    tool = np.sin((xx * math.cos(ang) + yy * math.sin(ang)) / per * 2 * math.pi + 0.3 * fbm(S, 2.5, 1, 1, 171))
    amp = [1.0, 0.45, 0.35][lv] * np.clip(fbm(S, 2.0, 1, 1, 172) * 0.5 + 0.8, 0.2, 1.3)
    tool = blur(tool * amp, [0.0, 1.2, 1.2][lv])
    co = co * (1 + 0.04 * tool)[..., None]
    if lv >= 1:
        co = co * (1 - 0.08 * np.clip(fbm(S, 3.0, 1, 1, 173), 0, 1))[..., None]
    mask = np.zeros((S, S), bool)
    if lv == 2:                                                   # moss in the low parts
        mo =blur((fbm(S, 1.8, 1, 1, 174) + 0.5 * fbm(S, 3.0, 1, 1, 175) > 1.3).astype(np.float32), 1.5) > 0.5
        co = patch(co, mo, (70, 84, 40), 0.85, 176)
        mask = mo
    n = combine(pn, h2n(tool * 0.8, 1.0))
    return R(co, n, r, mask, 0.25, 0.35, t)


def stone_river(lv, S):
    t = [tgt("stone_lantern", 2), tgt("stone_lantern"), tgt("stone_lantern", -2)][lv]
    co, n, r = stone("seaside_rock", "stone_lantern", lv, S, t, 0.5, nk=0.6)
    co = blur(co, 0.6)
    co, mask = lichen_moss(co, S, lv, 181, [0, 35, 25][lv], [None, None, 1.0][lv])
    return R(co, n, r * 0.9, mask, 0.3, 0.4, t)


def paper_shoji(lv, S):
    t = [tgt("washi_shoji", 1), tgt("washi_shoji", -3, 0, 5), tgt("washi_shoji", -5, 0.5, 6)][lv]
    r = np.random.default_rng(191)
    base = np.asarray(t, np.float32) / 255
    fib, ft = Wrap(S), Wrap(S)
    for _ in range(1600):
        x, y = r.uniform(0, S, 2)
        ang = r.uniform(0, 2 * math.pi)
        pts = [(x, y)]
        for _ in range(int(r.integers(4, 12))):
            ang += r.normal(0, 0.35)
            x, y = x + 7 * math.cos(ang), y + 7 * math.sin(ang)
            pts.append((x, y))
        fib.line(pts, 255, 1)
        ft.line(pts, int(r.choice([60, 230])), 1)
    fa, fv = fib.arr(), ft.arr()
    val = 1 + 0.03 * fbm(S, 2.6, 1, 1, 192) + 0.035 * fa * (fv - 0.55) * 2
    co = base[None, None, :] * val[..., None]
    h = fa * 0.4 + 0.2 * fbm(S, 1.6, 1, 1, 193)
    mask = np.zeros((S, S), bool)
    if lv >= 1:                                                   # patched squares of newer paper
        p = Wrap(S)
        for _ in range([0, 9, 6][lv]):
            x, y = r.uniform(0, S, 2)
            w_, h_ = r.uniform(60, 150), r.uniform(50, 130)
            p.rect(x, y, x + w_, y + h_, 255)
        pa = p.arr()
        co = co * (1 + 0.06 * pa)[..., None] * np.where(pa[..., None] > 0, np.array([1.0, 1.0, 1.03]), 1.0)
        h += pa * 0.3
    if lv == 2:                                                   # torn squares + stains
        tw = Wrap(S)
        for _ in range(5):
            cx, cy = r.uniform(0, S, 2)
            pts = [(cx + r.uniform(6, 22) * math.cos(q), cy + r.uniform(6, 22) * math.sin(q))
                   for q in np.linspace(0, 2 * math.pi, 15)[:-1]]
            tw.polygon(pts, 255)
        tr = tw.arr()
        st = blur((fbm(S, 3.0, 1, 1, 194) > 1.35).astype(np.float32), 3)
        co = mix(co, (40, 34, 28), tr * 0.95)
        co = mix(co, (150, 120, 80), (st > 0.4) * 0.35 + st * 0.1)
        mask = (tr > 0.3) | (st > 0.4)
    return R(np.clip(co, 0, 1), h2n(h, 1.0), 0.85, mask, 0.08, 0.2, t)


def bamboo_weathered(lv, S):
    t = [tgt("bamboo_weathered", 4, 0, 6), tgt("bamboo_weathered"), tgt("bamboo_weathered", -9)][lv]
    base = np.asarray(t, np.float32) / 255
    fib = fbm(S, 1.5, 1, 30, 201) * 0.05 + fbm(S, 2.2, 1, 6, 202) * 0.04
    y = np.arange(S, dtype=np.float32)[:, None]
    nodes = np.zeros((S, 1), np.float32)
    ridge = np.zeros((S, 1), np.float32)
    for yc in (0.02 * S, 0.35 * S, 0.68 * S):
        d = (y - yc + S / 2) % S - S / 2
        nodes += np.exp(-(d / 2.2) ** 2)
        ridge += np.exp(-(d / 4.0) ** 2) - 0.6 * np.exp(-((d - 7) / 3.0) ** 2)
    val = (1 + fib) * (1 - 0.25 * nodes) * (1 + 0.05 * np.exp(-((y % (0.333 * S) - 12) / 10) ** 2))
    co = base[None, None, :] * np.broadcast_to(val, (S, S))[..., None]
    h = np.broadcast_to(ridge * 2.0, (S, S)) + fib * 3
    mask = np.zeros((S, S), bool)
    if lv >= 1:
        co = grey(co, [0, 0.2, 0.35][lv])
    if lv == 2:
        sp = edge_lines(S, 40, 203, 1, 2, (80, 300))
        mil = blur((fbm(S, 3.0, 1, 3, 204) > 1.3).astype(np.float32), 2) > 0.5
        co = mix(co, (40, 36, 30), sp * 0.9)
        co = patch(co, mil, (78, 72, 60), 0.6, 205)
        h = h - sp * 2
        mask = (sp > 0.3) | mil
    return R(np.clip(co, 0, 1), h2n(h, 1.0), [0.45, 0.6, 0.8][lv], mask, [0.35, 0.25, 0.15][lv], [0.5, 0.35, 0.25][lv], t)


def metal_iron(lv, S):
    t = [tgt("iron_black", -3), tgt("iron_black", -1), tgt("iron_black", -1)][lv]
    base = np.asarray(t, np.float32) / 255
    d = Wrap(S)
    r = np.random.default_rng(211)
    for _ in range(260):
        x, y = r.uniform(0, S, 2)
        rr = r.uniform(3, 8)
        d.ellipse(x, y, rr, rr * r.uniform(0.7, 1.0), int(r.uniform(90, 255)))
    dim = blur(d.arr(), 1.5)
    h = 0.5 * fbm(S, 2.0, 1, 1, 212) - dim * 1.5
    co = base[None, None, :] * (1 + 0.12 * fbm(S, 2.2, 1, 1, 213) - 0.1 * dim)[..., None]
    mask = np.zeros((S, S), bool)
    rough = 0.45 + 0.1 * fbm(S, 2.0, 1, 1, 214)
    if lv >= 1:                                                   # rust bloom
        rs = np.clip(spots(S, [0, 14, 12][lv], 12, 1.5, 5, 10, 215) + (fbm(S, 2.6, 1, 1, 216) > [9, 1.4, 1.35][lv]), 0, 1)
        rc = photo("rust_coarse_01", "diff", S)
        co = mix(co, np.clip(rc * 1.1, 0, 1), rs * 0.9)
        rough = rough + rs * 0.4
        mask |= rs > 0.3
    if lv == 2:                                                   # runs downward from the rust
        runs = np.zeros((S, S), np.float32)
        rs_ = (mask).astype(np.float32)
        for k in range(1, 40, 3):
            runs = np.maximum(runs, np.roll(rs_, k, axis=0) * (1 - k / 40) * (fbm(S, 2.0, 12, 1, 217) > -0.3))
        co = mix(co, (110, 62, 34), runs * 0.6)
        mask |= runs > 0.3
    return R(np.clip(co, 0, 1), h2n(h, 1.2), rough, mask, 0.5, 0.45, t)


def straw_mushiro(lv, S):
    t = [tgt("thatch_new"), tgt("thatch_new", -6, -1, -6), tgt("thatch_new", -9, 0, -5)][lv]
    base = np.asarray(t, np.float32) / 255
    r = np.random.default_rng(221)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    sh = 3.0 * (S / 512)                                          # straw pitch ~6 mm
    wp = 16.0 * (S / 512)                                         # warp cord pitch ~3 cm
    row = np.floor(yy / sh).astype(int)
    rt = (1 + 0.09 * r.standard_normal(int(S / sh) + 2))[row]
    prof = np.cos(((yy % sh) / sh - 0.5) * math.pi)
    along = fbm(S, 2.0, 25, 1, 222) * 0.06
    wx = (xx % wp) / wp
    warp = (np.abs(wx - 0.5) < 0.1).astype(np.float32)
    twist = 0.5 + 0.5 * np.sin((xx + yy) / 2.0)
    val = rt * (0.75 + 0.25 * prof) * (1 + along) * (1 - 0.1 * np.exp(-((wx - 0.5) / 0.18) ** 2))
    val = np.where(warp > 0, 0.55 + 0.2 * twist, val)
    co = base[None, None, :] * val[..., None]
    h = prof * 0.8 + warp * (1.2 + 0.4 * twist)
    mask = np.zeros((S, S), bool)
    if lv >= 1:
        co = grey(co, [0, 0.3, 0.4][lv])
    if lv == 2:
        w = Wrap(S)
        for _ in range(260):                                      # frayed broken straws
            x, y = r.uniform(0, S, 2)
            ang = r.uniform(-0.6, 0.6) + (math.pi if r.random() < 0.5 else 0)
            L = r.uniform(8, 24)
            w.line([(x, y), (x + L * math.cos(ang), y + L * math.sin(ang))], 255, 1)
        fr = w.arr()
        co = mix(co, np.clip(co * 1.25, 0, 1), fr)
        dirt = blur((fbm(S, 2.8, 1, 1, 224) > 1.2).astype(np.float32), 2) > 0.5
        co = patch(co, dirt, (60, 52, 40), 0.6, 225)
        h = h + fr * 0.6
        mask = dirt
    return R(np.clip(co, 0, 1), h2n(h, 1.2), 0.85, mask, 0.1, 0.2, t)


RECIPES = {
    "jp_m_wood_weathered": wood_weathered, "jp_m_wood_street_dark": wood_street_dark, "jp_m_wood_bengara": wood_bengara,
    "jp_m_wood_kuro": wood_kuro, "jp_m_wood_sooted": wood_sooted, "jp_m_wall_arakabe": wall_arakabe,
    "jp_m_wall_nakanuri": wall_nakanuri, "jp_m_wall_shikkui": wall_shikkui, "jp_m_wall_namako_tile": wall_namako_tile,
    "jp_m_roof_kawara": roof_kawara, "jp_m_roof_thatch": roof_thatch, "jp_m_roof_thatch_cut": roof_thatch_cut,
    "jp_m_roof_kureita": roof_kureita, "jp_m_roof_kokera": roof_kokera, "jp_m_roof_kakigara": roof_kakigara,
    "jp_m_stone_field": stone_field, "jp_m_stone_cut": stone_cut, "jp_m_stone_river": stone_river,
    "jp_m_paper_shoji": paper_shoji, "jp_m_bamboo_weathered": bamboo_weathered, "jp_m_metal_iron": metal_iron,
    "jp_m_straw_mushiro": straw_mushiro,
}
# wear levels whose colour is a different palette entry than the material's own (matcheck reads this from the sidecar)
PALETTE_BY_WEAR = {"jp_m_roof_thatch": {"_w0": "thatch_new"}, "jp_m_roof_thatch_cut": {"_w0": "thatch_new"},
                   "jp_m_roof_kureita": {"_w0": "board_new"}, "jp_m_roof_kokera": {"_w0": "board_new"}}


def size_for(tile_m):
    n = tile_m * PPM
    return int(min(1024, max(256, 2 ** round(math.log2(n)))))


def save_png(path, a):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)


def make(mid):
    m = MATS[mid]
    S = size_for(m["tile_size_m"])
    info = []
    for lv in range(3):
        res = RECIPES[mid](lv, S)
        mask = res["mask"]
        co = fix_mean(res["co"].astype(np.float32), res["target"], ~mask)
        n = res["n"]
        stem = os.path.join(OUT, "%s_w%d" % (mid, lv))
        save_png(stem + "_co.png", co)
        save_png(stem + "_nohq.png", n * 0.5 + 0.5)
        rough = np.broadcast_to(np.asarray(res["rough"], np.float32), (S, S))
        smdi = np.stack([np.ones((S, S)), res["spec"] * (1 - rough), res["gloss"] * (1 - rough)], -1)
        save_png(stem + "_smdi.png", smdi)
        mp = stem + "_mask.png"
        if mask.any():
            Image.fromarray((mask * 255).astype(np.uint8)).save(mp)
        elif os.path.isfile(mp):
            os.remove(mp)
        info.append({"wear": "_w%d" % lv, "size": S, "target_srgb": [round(float(v), 1) for v in res["target"]],
                     "masked_frac": round(float(mask.mean()), 3), "spec": res["spec"], "gloss": res["gloss"]})
    print("  %-24s %4d px  masked %s" % (mid, S, [i["masked_frac"] for i in info]))
    return info


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    ids = argv or list(RECIPES)
    out = {}
    for mid in ids:
        out[mid] = make(mid)
    return out


if __name__ == "__main__":
    main(sys.argv[1:])
