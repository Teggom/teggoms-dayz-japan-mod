"""JP_Katana v2 textures, from katana_spec.json via katana_geom (numpy + Pillow, own work, no downloads).

  jp_katana_blade_co     512 x 2048  u: mune (0) -> edge (1) as d / width; v: point (0) -> machi (1) along the mune.
                         Zones (shinogi-ji, ji, hamon/boshi, kissaki narume, yokote) come from KatanaGeom.zone_v, so the
                         texture lines up with the mesh's shinogi, yokote and kissaki exactly. Colours: spec.colours_rgb
                         (measured on the Met 27600 / 27601 photos).
  jp_katana_tsuka_co     512 x 1024  u: round the tsuka (0 = +X ura face, 0.25 = edge, 0.5 = -X omote face, 0.75 = mune);
                         v: fuchi (0) -> kashira (1). Leather hineri-maki over black lacquered same, menuki, mekugi.
  jp_katana_fittings_co  512 x 512   atlas (katana_geom.ATLAS): hammered iron, shakudo nanako, horn (side + cap with the
                         wrap passing over), gold foil, copper.
Only katana files are written; the yari / yumi / ya textures are untouched.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import katana_geom as kg  # noqa: E402
from textures import DATA, to_paa, noise  # noqa: E402

V = kg.V


def rng(seed):
    return np.random.default_rng(seed)


def save(name, arr):
    os.makedirs(DATA, exist_ok=True)
    png = os.path.join(DATA, name + ".png")
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").save(png)
    return png


def sm(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ blade
def blade(g, W=512, H=2048):
    C = g.spec["colours_rgb"]
    v = (np.arange(H) + 0.5) / H
    u = (np.arange(W) + 0.5) / W
    s = (1.0 - v)[:, None] * g.L_arc * np.ones((1, W))
    w = g.width_v(s[:, 0])[:, None] * np.ones((1, W))
    d = u[None, :] * w
    zone = g.zone_v(s.ravel(), d.ravel()).reshape(H, W)
    Z = g.ZONES
    # itame grain: stretched along the blade, some mokume swirl; chikei = darker lines in the ji
    grain = 0.55 * noise(H, W, 40, 10, 101) + 0.30 * noise(H, W, 12, 4, 102) + 0.15 * noise(H, W, 3, 2, 103)
    fine = noise(H, W, 1, 1, 104)
    ji = np.array(V(C["ji"]), np.float32)
    ham = np.array(V(C["hamon"]), np.float32)
    shj = np.array(V(C["shinogi_ji"]), np.float32)
    col = np.zeros((H, W, 3), np.float32)
    col[:] = ji + (grain * 9 + fine * 3)[..., None]
    # hamon: frosted white band; nioiguchi = soft bright line on the boundary; nie sparkle; small ashi
    hard = (zone == Z["hamon"]).astype(np.float32)
    soft = np.asarray(Image.fromarray((hard * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)), np.float32) / 255
    edge_band = np.clip(1 - np.abs(soft - 0.5) * 2, 0, 1)                        # 1 on the boundary
    frost = ham + (noise(H, W, 2, 2, 105) * 6)[..., None]
    col = col * (1 - soft[..., None]) + frost * soft[..., None]
    col += (edge_band * 18)[..., None]                                             # subdued nioiguchi
    r = rng(106)
    nie = (r.random((H, W)) > 0.93) & (edge_band > 0.25)
    col[nie] += 34
    # ashi: short soft lines from the boundary into the hamon, about every 2 cm in the body
    ss = s[:, 0]
    body = ss <= g.s_yokote
    depth = g.hamon_depth_v(ss)
    lg = V(g.spec["hamon"]["gunome_wavelength_cm"]) * 0.01
    for k in range(int(g.s_yokote / lg)):
        if k % 2:
            continue
        s0 = (k + 0.5) * lg
        rows = np.where(np.abs(ss - s0) < 0.0006)[0]
        for i in rows:
            dd = d[i] - (w[i] - depth[i])
            m = (dd > 0) & (dd < 0.35 * depth[i])
            col[i, m] = col[i, m] * 0.85 + ham * 0.15 + 10
    # sunagashi / kinsuji: faint bright streaks along the blade just inside the hamon
    streak = sm(0.55, 0.9, noise(H, W, 60, 2, 107)) * (edge_band > 0.05)
    col += (streak * 12)[..., None]
    # kissaki (narume): brighter, smoother, less grain
    kz = (zone == Z["kissaki"])
    nar = 0.55 * ji + 0.45 * ham
    col[kz] = nar + (fine[kz] * 3)[:, None]
    # shinogi-ji and mune: burnished, dark, fine lengthwise polish lines
    polish = noise(H, W, 30, 1, 108)
    for zz, f in ((Z["shinogi_ji"], 1.0), (Z["mune"], 1.08)):
        m = zone == zz
        col[m] = shj * f + (polish[m] * 4)[:, None]
    # yokote: a crisp line from the edge to the shinogi
    vy = 1.0 - g.s_yokote / g.L_arc
    iy = int(round(vy * H))
    dsy = g.shinogi_d(g.s_yokote) / g.width(g.s_yokote)
    for i in range(iy - 1, iy + 2):
        m = u >= dsy
        col[i, m] = col[i, m] * 0.55
    # polished cutting edge (ha): a thin bright line
    col = col * (1 - sm(0.975, 0.995, u))[None, :, None] + np.array([226, 230, 236]) * sm(0.975, 0.995, u)[None, :, None]
    return save("jp_katana_blade_co", col)


# ------------------------------------------------------------------ tsuka
def tsuka(g, W=512, H=1024):
    C = g.spec["colours_rgb"]
    wl = g.y_wrap[1] - g.y_wrap[0]
    P = g.pitch_eff
    u = (np.arange(W) + 0.5) / W
    v = (np.arange(H) + 0.5) / H
    a = v[:, None] * wl * np.ones((1, W))                      # metres from the fuchi end of the wrap
    phi = np.ones((H, 1)) * u[None, :]
    # nearest face centre (0 = ura +X, 0.5 = omote -X) and the signed angular offset from it
    dphi = ((phi + 0.25) % 0.5) - 0.25
    face = np.where(((phi + 0.25) % 1.0) < 0.5, 0, 1)          # 0: ura, 1: omote
    L = g.win_half_len * P
    ph = math.asin(min(1.0, 2 * g.win_half_h)) / (2 * math.pi)
    kk = L / ph
    q = a / P
    wi = np.floor(q)                                           # window index
    da = (q - wi - 0.5) * P
    window = (np.abs(da) / L + np.abs(dphi) / ph) < 1.0
    # tapes: family A along a + k dphi, family B along a - k dphi; which is on top swaps across the face centre
    qa = (a + kk * dphi) / P
    qb = (a - kk * dphi) / P
    half = 0.5 - L / P
    ca = (((qa + 0.5) % 1.0) - 0.5) / max(half, 1e-3)
    cb = (((qb + 0.5) % 1.0) - 0.5) / max(half, 1e-3)
    # the tape on top swaps across the face centre line (the twist); where the top tape does not reach, the
    # other tape shows, a little shaded because it lies underneath
    ctop = np.where(dphi > 0, ca, cb)
    cbot = np.where(dphi > 0, cb, ca)
    under = np.abs(ctop) > 1.0
    cvis = np.where(under, cbot, ctop)
    leather = np.array(V(C["wrap_leather"]), np.float32)
    lgrain = noise(H, W, 3, 3, 201) * 7 + noise(H, W, 1, 1, 202) * 4
    # flat leather tape: only a slight roll-off at its edges (the photo shows an even buff surface)
    shade = (1.0 - 0.10 * np.clip(cvis, -1, 1) ** 2) * np.where(under, 0.90, 1.0)
    edge_line = sm(0.90, 1.0, np.abs(np.clip(cvis, -1, 1)))
    col = (leather[None, None] + lgrain[..., None]) * shade[..., None]
    col *= (1 - 0.18 * edge_line)[..., None]
    # the twist where the two tapes cross on the face centre line, between windows: a short raised knot
    knot = np.exp(-(dphi / 0.018) ** 2) * np.exp(-((((q + 0.5) % 1.0) - 0.5) / 0.10) ** 2)
    col *= (1 + 0.10 * knot)[..., None]
    col *= (1 - 0.22 * np.exp(-(dphi / 0.004) ** 2) * (np.abs(((q + 0.5) % 1.0) - 0.5) < 0.2))[..., None]
    side = np.minimum(np.abs(phi - 0.25), np.abs(phi - 0.75))
    ridge = np.exp(-(side / 0.02) ** 2)
    col += (ridge * 14 * (0.5 + 0.5 * np.cos(2 * np.pi * q)))[..., None]
    # windows: black lacquered same with nodules
    same = np.array(V(C["same_lacquered"]), np.float32)
    r = rng(203)
    nod = (r.random((H // 3, W // 3)) > 0.62).astype(np.uint8) * 255
    nod = np.asarray(Image.fromarray(nod).resize((W, H), Image.NEAREST).filter(ImageFilter.GaussianBlur(1.0)), np.float32) / 255
    same_col = same[None, None] + (nod * 26 - 6)[..., None] + (noise(H, W, 2, 2, 204) * 4)[..., None]
    # sharp window edge with a thin shadow where the tape edge sits on the same
    metric = np.abs(da) / L + np.abs(dphi) / ph
    shadow = sm(1.0, 1.12, metric) * (metric < 1.12) + (metric >= 1.12)
    col = col * (0.55 + 0.45 * np.clip(shadow, 0, 1))[..., None]
    col = np.where(window[..., None], same_col, col)
    # menuki: gold (uttori) over shakudo, seen in the windows, raising the tape above it
    shak = np.array(V(C["shakudo"]), np.float32)
    gold = np.array(V(C["gold_foil"]), np.float32)
    for y_m, fc in ((g.y_menuki_omote, 1), (g.y_menuki_ura, 0)):
        am = g.y_wrap[1] - y_m
        ell = ((a - am) / (0.5 * g.menuki_len)) ** 2 + (dphi * (2 * math.pi) * 0.5 * g.tsuka_depth / (0.5 * g.menuki_w)) ** 2
        inside = (ell < 1.0) & (face == fc)
        scales = 0.5 + 0.5 * np.sin(2 * np.pi * (a - am) / 0.004) * np.sin(2 * np.pi * dphi / 0.02)
        dragon = gold[None, None] * (0.75 + 0.25 * scales[..., None])
        dragon = np.where((scales < 0.25)[..., None], shak[None, None] + 20, dragon)
        col = np.where((inside & window)[..., None], dragon, col)
        col = np.where((inside & ~window)[..., None], col * 1.08, col)
    # mekugi: bamboo peg head on both faces
    am = g.y_wrap[1] - g.y_mekugi
    for fc in (0, 1):
        rr = np.hypot(a - am, dphi * (2 * math.pi) * 0.5 * g.tsuka_depth)
        m = (rr < 0.5 * g.mekugi_d) & (face == fc)
        col[m] = np.array(V(C["mekugi_bamboo"]), np.float32) * (0.85 + 0.15 * (1 - rr[m] / (0.5 * g.mekugi_d)))[:, None]
    return save("jp_katana_tsuka_co", col)


# ------------------------------------------------------------------ fittings atlas
def fittings(g, S=512):
    C = g.spec["colours_rgb"]
    col = np.zeros((S, S, 3), np.float32)

    def rect(name):
        u0, u1, v0, v1 = kg.ATLAS[name]
        return int(v0 * S), int(np.ceil(v1 * S)), int(u0 * S), int(np.ceil(u1 * S))

    def fill(name, fn):
        r0, r1, c0, c1 = rect(name)
        h, w = r1 - r0, c1 - c0
        col[r0:r1, c0:c1] = fn(h, w)
    # hammered iron (tsuchime): dimples from a coarse cell pattern, rust-brown patina, darker hollows
    iron = np.array(V(C["tsuba_iron"]), np.float32)

    def f_iron(h, w):
        r = rng(301)
        pts = r.random((90, 2)) * [h, w]
        yy, xx = np.mgrid[0:h, 0:w]
        dist = np.full((h, w), 1e9)
        for py, px in pts:
            dist = np.minimum(dist, (yy - py) ** 2 + (xx - px) ** 2)
        dist = np.sqrt(dist) / 14.0
        dimple = np.clip(dist, 0, 1)
        n = noise(h, w, 6, 6, 302)
        return iron[None, None] * (0.72 + 0.28 * dimple)[..., None] + (n * 10)[..., None]
    fill("iron", f_iron)
    shak = np.array(V(C["shakudo"]), np.float32)
    gold = np.array(V(C["gold_foil"]), np.float32)

    def f_shak(h, w):
        yy, xx = np.mgrid[0:h, 0:w]
        nanako = 0.5 + 0.5 * np.cos(2 * np.pi * yy / 5.0) * np.cos(2 * np.pi * xx / 5.0)
        c = shak[None, None] * (0.85 + 0.3 * nanako)[..., None]
        r = rng(303)
        sp = r.random((h, w)) > 0.992
        c[sp] = gold
        return c
    fill("shakudo", f_shak)
    horn = np.array(V(C["horn_lacquer"]), np.float32)
    leather = np.array(V(C["wrap_leather"]), np.float32)

    def f_horn_side(h, w):
        c = horn[None, None] + (noise(h, w, 8, 8, 304) * 5)[..., None]
        # the wrap runs up the edge and mune sides (u = 0.25, 0.75) and over the top
        uu = np.linspace(0, 1, w)[None, :]
        band = (np.minimum(np.abs(uu - 0.25), np.abs(uu - 0.75)) < 0.07) * np.ones((h, 1))
        return np.where(band[..., None] > 0, leather[None, None] * 0.92, c)
    fill("horn_side", f_horn_side)

    def f_horn_cap(h, w):
        c = horn[None, None] + (noise(h, w, 8, 8, 305) * 5)[..., None]
        yy, xx = np.mgrid[0:h, 0:w]
        x = (xx / (w - 1)) * 2 - 1           # planar X (side-side)
        z = (yy / (h - 1)) * 2 - 1           # planar Z (edge-mune)
        b1 = np.abs(z - 0.45 * x) < 0.22     # two tapes cross over the top (kashira-kake)
        b2 = np.abs(z + 0.45 * x) < 0.22
        c = np.where((b1 | b2)[..., None], leather[None, None] * 0.9, c)
        return c
    fill("horn_cap", f_horn_cap)
    cu = np.array(V(C["copper"]), np.float32)

    def f_gold(h, w):
        return gold[None, None] + (noise(h, w, 1, 12, 306) * 8)[..., None]
    fill("gold", f_gold)

    def f_cu(h, w):
        return cu[None, None] + (noise(h, w, 4, 4, 307) * 8)[..., None]
    fill("copper", f_cu)
    return save("jp_katana_fittings_co", col)


def main(paa=True):
    g = kg.KatanaGeom()
    pngs = [blade(g), tsuka(g), fittings(g)]
    for p in pngs:
        if paa:
            to_paa(p)
        print("texture", os.path.basename(p), Image.open(p).size, "-> paa" if paa else "")
    return pngs


if __name__ == "__main__":
    main("--no-paa" not in sys.argv)
