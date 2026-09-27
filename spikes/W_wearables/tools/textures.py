"""Procedural textures for W's garments (numpy + Pillow; no downloads). Each writes <stem>_co.png,
<stem>_nohq.png and <stem>_smdi.png, then converts them to .paa with DayZ Tools' ImageToPAA.

Conventions (from the vanilla rvmats / textures, see REPORT.md):
  _co    colour (+ alpha 255)
  _nohq  tangent-space normal map, R = +x, G = +y (image up), B = z
  _smdi  R = 255 (unused), G = specular level, B = glossiness
"""
import os
import subprocess

import numpy as np
from PIL import Image

from wlib import IMAGE_TO_PAA

RNG = np.random.default_rng(1187)


def fbm(h, w, octaves=5, base=8, seed=0):
    """cheap tileable-ish value noise (bilinear upsampled random grids), 0..1"""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w))
    amp = 1.0
    tot = 0.0
    for o in range(octaves):
        n = base * (2 ** o)
        g = rng.random((n + 1, n + 1))
        g[-1, :] = g[0, :]
        g[:, -1] = g[:, 0]
        img = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)
        out += amp * np.asarray(img, dtype=float) / 255.0
        tot += amp
        amp *= 0.5
    return out / tot


def normal_from_height(hmap, strength=2.0):
    gy, gx = np.gradient(hmap)
    nx = -gx * strength
    ny = gy * strength     # image rows grow downward; +y (up) = -d/drow
    nz = np.ones_like(hmap)
    n = np.stack([nx, ny, nz], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return ((n * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8)


def save_set(out_dir, stem, co, height, spec, gloss, nstrength=2.0):
    os.makedirs(out_dir, exist_ok=True)
    co = np.clip(co, 0, 1)
    a = np.full(co.shape[:2] + (1,), 1.0)
    Image.fromarray((np.concatenate([co, a], -1) * 255).astype(np.uint8), "RGBA").save(os.path.join(out_dir, stem + "_co.png"))
    Image.fromarray(normal_from_height(height, nstrength), "RGB").save(os.path.join(out_dir, stem + "_nohq.png"))
    sm = np.stack([np.ones_like(spec), np.clip(spec, 0, 1), np.clip(gloss, 0, 1)], -1)
    Image.fromarray((sm * 255).astype(np.uint8), "RGB").save(os.path.join(out_dir, stem + "_smdi.png"))
    return [os.path.join(out_dir, stem + s + ".png") for s in ("_co", "_nohq", "_smdi")]


def to_paa(pngs):
    out = []
    for p in pngs:
        paa = p[:-4] + ".paa"
        r = subprocess.run([IMAGE_TO_PAA, p, paa], capture_output=True, text=True)
        if not os.path.isfile(paa):
            raise SystemExit("ImageToPAA failed on %s: %s %s" % (p, r.stdout, r.stderr))
        out.append(paa)
    return out


def paint_rect(img, reg, color, noise=None, amount=0.1):
    h, w = img.shape[:2]
    u0, v0, u1, v1 = reg
    x0, x1, y0, y1 = int(u0 * w), int(u1 * w), int(v0 * h), int(v1 * h)
    img[y0:y1, x0:x1] = color
    if noise is not None:
        img[y0:y1, x0:x1] *= (1 - amount + amount * 2 * noise[y0:y1, x0:x1, None])


# ------------------------------------------------------------------ kasa
def kasa(out_dir, size=1024):
    import kasa as K
    h = w = size
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx + 0.5) / w
    v = (yy + 0.5) / h
    dx, dz = u - 0.5, v - 0.5
    r = np.hypot(dx, dz) / 0.49          # 0 at apex, 1 at rim
    phi = np.arctan2(dx, -dz)
    n_strips = 220
    s = (phi / (2 * np.pi) + 0.5) * n_strips
    strip_id = np.floor(s).astype(int) % n_strips
    frac = s - np.floor(s)
    rng = np.random.default_rng(7)
    strip_tone = rng.normal(0, 0.06, n_strips)[strip_id]
    ridge = np.sin(np.pi * frac) ** 0.6                      # rounded sedge strips
    fib = fbm(h, w, 5, 16, seed=3)
    fibre = (np.sin(r * 900 + fib * 6) * 0.5 + 0.5) * 0.08    # fibres run along the strips
    base = np.array([0.74, 0.62, 0.38])
    co = base[None, None, :] * (0.82 + 0.18 * ridge[..., None]) * (1 + strip_tone[..., None]) * (1 - fibre[..., None])
    height = ridge * 0.6 + fibre
    # concentric stitch rings (bamboo/thread) holding the sedge
    for rr, wd in ((0.12, 0.012), (0.36, 0.010), (0.62, 0.010), (0.86, 0.012), (0.975, 0.02)):
        band = np.exp(-((r - rr) / wd) ** 2)
        stitch = (np.sin(phi * 160) > 0.2) * band
        co = co * (1 - 0.45 * stitch[..., None]) + np.array([0.35, 0.26, 0.14]) * 0.45 * stitch[..., None]
        height = height + 0.8 * stitch
    # weathering: darker near the apex and rim edge, subtle blotches
    blot = fbm(h, w, 4, 4, seed=11)
    co *= (0.9 + 0.2 * blot[..., None])
    co *= (1 - 0.12 * np.exp(-(r / 0.08) ** 2))[..., None]
    # corner swatches
    paint_rect(co, K.BIND, np.array([0.30, 0.22, 0.12]), fbm(h, w, 3, 16, 5), 0.15)
    paint_rect(co, K.RINGTX, np.array([0.40, 0.30, 0.18]), fbm(h, w, 3, 16, 6), 0.15)
    paint_rect(co, K.KNOB, np.array([0.28, 0.20, 0.11]), fbm(h, w, 3, 16, 8), 0.15)
    spec = 0.10 + 0.10 * ridge
    gloss = 0.25 + 0.05 * ridge
    return to_paa(save_set(out_dir, "jp_kasa", co, height, spec, gloss, 3.0))


# ------------------------------------------------------------------ tabi + waraji
def weave(h, w, pitch=3.0, seed=0):
    yy, xx = np.mgrid[0:h, 0:w]
    a = np.sin(xx * np.pi / pitch) * np.sin(yy * np.pi / pitch)
    return 0.5 + 0.5 * a


def region_px(reg, h, w):
    u0, v0, u1, v1 = reg
    return int(v0 * h), int(v1 * h), int(u0 * w), int(u1 * w)


def tabi(out_dir, size=1024):
    import tabi as TB
    h = w = size
    co = np.zeros((h, w, 3))
    height = np.zeros((h, w))
    spec = np.full((h, w), 0.08)
    gloss = np.full((h, w), 0.2)
    wv = weave(h, w, 2.2)
    grime = fbm(h, w, 5, 8, seed=21)
    white = np.array([0.93, 0.92, 0.87])
    # cloth regions
    for reg in (TB.R_TOP, TB.R_SIDE):
        y0, y1, x0, x1 = region_px(reg, h, w)
        co[y0:y1, x0:x1] = white * (0.93 + 0.07 * wv[y0:y1, x0:x1, None]) * (0.95 + 0.08 * grime[y0:y1, x0:x1, None])
        height[y0:y1, x0:x1] = wv[y0:y1, x0:x1] * 0.3
    # side region: dirt toward the ground (v -> 1 is y -> 0), the kohaze clasps and the slit on the inner back
    y0, y1, x0, x1 = region_px(TB.R_SIDE, h, w)
    vv = np.linspace(0, 1, y1 - y0)[:, None]
    dirt = np.clip((vv - 0.75) / 0.25, 0, 1) * (0.6 + 0.4 * grime[y0:y1, x0:x1])
    co[y0:y1, x0:x1] *= (1 - 0.35 * dirt[..., None])
    rw = x1 - x0
    rh = y1 - y0
    xs = x0 + int(0.635 * rw)
    co[y0 + int(0.08 * rh):y0 + int(0.62 * rh), xs - 1:xs + 1] *= 0.55                 # the slit
    for k in range(4):
        cy = y0 + int((0.14 + 0.12 * k) * rh)
        co[cy - 4:cy + 4, xs + 3:xs + 14] = np.array([0.70, 0.58, 0.30])             # brass kohaze
        height[cy - 4:cy + 4, xs + 3:xs + 14] = 1.0
        spec[cy - 4:cy + 4, xs + 3:xs + 14] = 0.6
        gloss[cy - 4:cy + 4, xs + 3:xs + 14] = 0.7
    # top region: centre seam toward the split toe (medial third), stitched
    y0, y1, x0, x1 = region_px(TB.R_TOP, h, w)
    sx = x0 + int(0.30 * (x1 - x0))
    co[y0:y0 + int(0.4 * (y1 - y0)), sx - 1:sx + 2] *= 0.8
    height[y0:y0 + int(0.4 * (y1 - y0)), sx - 1:sx + 2] = -0.5
    # tabi sole: heavier grey-blue cloth with sashiko lines
    y0, y1, x0, x1 = region_px(TB.R_SOLE, h, w)
    co[y0:y1, x0:x1] = np.array([0.46, 0.47, 0.50]) * (0.9 + 0.1 * wv[y0:y1, x0:x1, None]) * (0.9 + 0.15 * grime[y0:y1, x0:x1, None])
    for k in range(6):
        xx = x0 + int((0.15 + 0.14 * k) * (x1 - x0))
        dash = (np.arange(y1 - y0) // 6) % 2 == 0
        co[y0:y1, xx][dash] = np.array([0.75, 0.75, 0.72])
    # straw: braided sole (rows across the sole), edge, cord
    straw = np.array([0.72, 0.62, 0.40])
    y0, y1, x0, x1 = region_px(TB.R_STRAW, h, w)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    rows_ = np.sin((yy - y0) * np.pi / 7.0 + np.sin((xx - x0) * 0.25) * 0.8)
    co[y0:y1, x0:x1] = straw * (0.78 + 0.22 * (rows_[..., None] * 0.5 + 0.5)) * (0.9 + 0.15 * grime[y0:y1, x0:x1, None])
    height[y0:y1, x0:x1] = rows_ * 0.8
    for reg, pitch in ((TB.R_STRAWSIDE, 5.0), (TB.R_CORD, 4.0)):
        y0, y1, x0, x1 = region_px(reg, h, w)
        yy, xx = np.mgrid[y0:y1, x0:x1]
        tw = np.sin(((xx - x0) + (yy - y0)) * np.pi / pitch)
        co[y0:y1, x0:x1] = straw * 1.05 * (0.78 + 0.22 * (tw[..., None] * 0.5 + 0.5))
        height[y0:y1, x0:x1] = tw * 0.8
    return to_paa(save_set(out_dir, "jp_tabi_waraji", co, height, spec, gloss, 2.5))


# ------------------------------------------------------------------ kimono (short / long)
def kimono(out_dir, length="short", size=2048):
    import kimono as KM
    h = w = size
    trunk_h = {"short": 0.83, "long": 1.465}[length]
    co = np.zeros((h, w, 3))
    height = np.zeros((h, w))
    spec = np.full((h, w), 0.05)
    gloss = np.full((h, w), 0.15)
    wv = weave(h, w, 1.6)
    warp = fbm(h, w, 4, 6, seed=31)
    streak = np.asarray(Image.fromarray((fbm(8, w, 3, 64, seed=32) * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR), float) / 255.0
    indigo = np.array([0.105, 0.150, 0.315])
    cloth = indigo * (0.86 + 0.10 * wv[..., None]) * (0.92 + 0.14 * warp[..., None]) * (0.95 + 0.10 * streak[..., None])
    co[:] = cloth
    height[:] = wv * 0.4

    def box(r):
        return region_px(r, h, w)
    # trunk: side seams, back seam, hem fold, back crest
    y0, y1, x0, x1 = box(KM.A_TRUNK)
    rw, rh = x1 - x0, y1 - y0
    for u in (0.25, 0.5, 0.75):
        xx = x0 + int(u * rw)
        co[y0:y1, xx - 1:xx + 2] *= 0.72
        height[y0:y1, xx - 1:xx + 2] = -0.6
    hem_px = int(0.022 / trunk_h * rh)
    co[y1 - hem_px:y1, x0:x1] *= 0.85
    co[y1 - hem_px - 2:y1 - hem_px, x0:x1] *= 0.7
    # kamon at the back centre, 1.40 m high, 8 cm across (circle + two bars: maru ni futatsu hikiryo)
    cu = x0 + 0.5 * rw
    cv = y0 + (1.54 - 1.40) / trunk_h * rh
    ru = 0.04 / 1.20 * rw
    rv = 0.04 / trunk_h * rh
    yy, xx = np.mgrid[y0:y1, x0:x1]
    dn = np.hypot((xx - cu) / ru, (yy - cv) / rv)
    ring = (dn > 0.80) & (dn < 1.0)
    bars = (dn < 0.80) & ((np.abs((yy - cv) / rv - 0.28) < 0.12) | (np.abs((yy - cv) / rv + 0.28) < 0.12))
    crest = ring | bars
    sub = co[y0:y1, x0:x1]
    sub[crest] = np.array([0.86, 0.85, 0.80])
    # sleeves: pouch seam at the section bottom (k ~ 0.5), cuff edge at the end
    for side in ("left", "right"):
        y0, y1, x0, x1 = box(KM.A_SLEEVE[side])
        rw, rh = x1 - x0, y1 - y0
        xx = x0 + int(0.5 * rw)
        co[y0:y1, xx - 1:xx + 2] *= 0.75
        co[y1 - 10:y1, x0:x1] *= 0.8
    # collar: near-black silk band with the white under-collar (juban) along the V edge (v 0 .. 0.27)
    y0, y1, x0, x1 = box(KM.A_COLLAR)
    rh = y1 - y0
    co[y0:y1, x0:x1] = np.array([0.035, 0.038, 0.055]) * (0.9 + 0.2 * wv[y0:y1, x0:x1, None])
    co[y0:y0 + int(0.27 * rh), x0:x1] = np.array([0.90, 0.89, 0.85]) * (0.95 + 0.05 * wv[y0:y0 + int(0.27 * rh), x0:x1, None])
    spec[y0:y1, x0:x1] = 0.12
    gloss[y0:y1, x0:x1] = 0.35
    # the flap (outer panel edge below the obi) samples u 0.95 - 1.0: indigo edge
    co[y0:y1, x0 + int(0.95 * (x1 - x0)):x1] = indigo * 0.8
    # obi + knot: rust hakata weave, cream edge lines, a repeating motif
    for r_ in (KM.A_OBI, KM.A_KNOT):
        y0, y1, x0, x1 = box(r_)
        rh, rw = y1 - y0, x1 - x0
        yy, xx = np.mgrid[y0:y1, x0:x1]
        base = np.array([0.46, 0.25, 0.11]) * (0.88 + 0.12 * weave(rh, rw, 1.2))[..., None]
        v = (yy - y0) / rh
        lines = (np.abs(v - 0.14) < 0.035) | (np.abs(v - 0.86) < 0.035)
        base[lines] = np.array([0.80, 0.70, 0.48])
        motif = (np.abs(v - 0.5) < 0.22) & (((xx - x0) // 18) % 3 == 0)
        base[motif] = np.array([0.30, 0.15, 0.07])
        co[y0:y1, x0:x1] = base
        height[y0:y1, x0:x1] = weave(rh, rw, 1.2) * 0.6 + lines * 0.3
        spec[y0:y1, x0:x1] = 0.10
        gloss[y0:y1, x0:x1] = 0.3
    # cuff caps: indigo, darker rim
    y0, y1, x0, x1 = box(KM.A_CUFF)
    co[y0:y0 + 8, x0:x1] *= 0.7
    return to_paa(save_set(out_dir, "jp_kimono_%s" % length, co, height, spec, gloss, 2.0))


if __name__ == "__main__":
    import sys
    from wlib import SRC
    which = sys.argv[1:] or ["kasa"]
    if "kasa" in which:
        print(kasa(os.path.join(SRC, "kasa", "data")))
    if "tabi" in which:
        print(tabi(os.path.join(SRC, "tabi", "data")))
    if "kimono" in which:
        for length in ("short", "long"):
            print(kimono(os.path.join(SRC, "kimono", "data"), length))
