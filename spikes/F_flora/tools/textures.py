r"""textures.py - every 2D texture of the F (flora) spike, procedural or from CC0 sources.

    python spikes/F_flora/tools/textures.py            (writes PNGs to data/F/work/tex, PAAs to src/JP/plants)

Outputs (PAA next to the models under src/JP/plants/<area>/data):
  tree/data    jp_sakura_bark_co / _nohq         Poly Haven "Sakura Bark" (CC0), darkened towards Somei-yoshino
               jp_sakura_blossom_ca              2048 atlas, 4 procedural blossom sprites (2 sprays, a dense clump, a radial spray)
               jp_sakura_blossom_windmask_co     256, red = how much each texel flutters (0 at the twig base, 1 at the tips)
  bamboo/data  jp_bamboo_culm_co / _nohq         1024, 4 culm colour columns, one internode per tile, node ring at v=0
               jp_bamboo_leaves_ca               2048 atlas, 4 procedural leaf sprays
               jp_bamboo_leaves_windmask_co      256
  items/data   jp_bamboo_pole_co / _nohq         512x2048, the whole 2.5 m pole unwrapped + an end-cap square
The LOD4 impostor textures (*_lod4_ca) are rendered by render_blender.py, not here.
"""
import math
import os
import random
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (WORK_TEX, DATA, P_TREE, P_BAMBOO, P_ITEMS, src_dir, to_paa)  # noqa: E402

SS = 2  # supersampling factor for the vector-drawn atlases


# ----------------------------------------------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------------------------------------------
def bleed(rgba):
    """Fill the RGB of transparent texels with the colour of the nearest opaque ones (push-pull pyramid), so
    mipmaps and alpha-test edges never pick up black."""
    a = rgba[..., 3:4].astype(np.float64) / 255.0
    rgb = rgba[..., :3].astype(np.float64)
    mask = (a > 0.02).astype(np.float64)
    pyr = []
    c, w = rgb * mask, mask
    while True:
        pyr.append((c, w))
        h, wd = w.shape[:2]
        if h < 2 or wd < 2 or h % 2 or wd % 2:
            break
        c = c.reshape(h // 2, 2, wd // 2, 2, 3).sum(axis=(1, 3))
        w = w.reshape(h // 2, 2, wd // 2, 2, 1).sum(axis=(1, 3))
    filled = pyr[-1][0] / np.maximum(pyr[-1][1], 1e-9)
    for c, w in reversed(pyr[:-1]):
        up = np.repeat(np.repeat(filled, 2, axis=0), 2, axis=1)[: w.shape[0], : w.shape[1]]
        own = c / np.maximum(w, 1e-9)
        filled = np.where(w > 0, own, up)
    out = rgba.copy()
    keep = mask[..., 0] > 0
    out[..., :3] = np.where(keep[..., None], rgba[..., :3], np.clip(filled, 0, 255).astype(np.uint8))
    return out


def periodic_noise(h, w, sy, sx, seed):
    """Tileable (both axes) smooth noise in [-1, 1]: white noise filtered with a Gaussian in the frequency domain."""
    rng = np.random.default_rng(seed)
    n = rng.standard_normal((h, w))
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.fftfreq(w)[None, :]
    g = np.exp(-2 * (math.pi ** 2) * ((fy * sy) ** 2 + (fx * sx) ** 2))
    out = np.real(np.fft.ifft2(np.fft.fft2(n) * g))
    out /= (np.abs(out).max() + 1e-9)
    return out


def height_to_normal_dx(hmap, strength):
    """Height map (rows = image y going down) -> DirectX-style tangent normal map (green = -dh/dy)."""
    dx = (np.roll(hmap, -1, axis=1) - np.roll(hmap, 1, axis=1)) * 0.5
    dy = (np.roll(hmap, -1, axis=0) - np.roll(hmap, 1, axis=0)) * 0.5
    nx, ny, nz = -dx * strength, -dy * strength, np.ones_like(hmap)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    rgb = np.stack([nx / ln, ny / ln, nz / ln], axis=-1) * 0.5 + 0.5
    return Image.fromarray((rgb * 255).clip(0, 255).astype(np.uint8), "RGB")


def jitter(col, rng, amount):
    k = 1.0 + rng.uniform(-amount, amount)
    return tuple(int(max(0, min(255, c * k))) for c in col[:3]) + tuple(col[3:])


def lerp_col(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


_SPRITES = []


class Sprite:
    """One atlas cell, drawn in cell pixel units (final resolution) onto its own supersampled RGBA image, so
    nothing can spill into a neighbouring cell. flush_sprites() pastes every cell into its atlas."""

    def __init__(self, img, draw, ox, oy, size):
        self.atlas, self.ox, self.oy, self.size = img, ox, oy, size
        self.img = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        _SPRITES.append(self)

    def P(self, x, y):
        return (x * SS, y * SS)

    def line(self, pts, width, col):
        ss = [self.P(x, y) for x, y in pts]
        self.d.line(ss, fill=col, width=max(1, int(round(width * SS))), joint="curve")

    def poly(self, pts, col, outline=None):
        self.d.polygon([self.P(x, y) for x, y in pts], fill=col, outline=outline)

    def ellipse(self, cx, cy, rx, ry, col):
        a, b = self.P(cx - rx, cy - ry), self.P(cx + rx, cy + ry)
        self.d.ellipse([a, b], fill=col)

    def taper_line(self, pts, w0, w1, col, hi=None):
        """Polyline with width going w0 -> w1 (drawn as quads + round joints), optional highlight stripe."""
        n = len(pts)
        for i in range(n - 1):
            t0, t1 = i / (n - 1), (i + 1) / (n - 1)
            wa, wb = w0 + (w1 - w0) * t0, w0 + (w1 - w0) * t1
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            dx, dy = x1 - x0, y1 - y0
            ln = math.hypot(dx, dy) or 1e-6
            px, py = -dy / ln, dx / ln
            quad = [(x0 + px * wa / 2, y0 + py * wa / 2), (x1 + px * wb / 2, y1 + py * wb / 2),
                    (x1 - px * wb / 2, y1 - py * wb / 2), (x0 - px * wa / 2, y0 - py * wa / 2)]
            self.poly(quad, col)
            self.ellipse(x1, y1, wb / 2, wb / 2, col)
            if hi and wa > 2.2:
                self.line([(x0 + px * wa * 0.18, y0 + py * wa * 0.18), (x1 + px * wb * 0.18, y1 + py * wb * 0.18)],
                          max(0.6, wa * 0.22), hi)
        self.ellipse(pts[0][0], pts[0][1], w0 / 2, w0 / 2, col)


def flush_sprites(atlas):
    for sp in [s for s in _SPRITES if s.atlas is atlas]:
        atlas.alpha_composite(sp.img, (sp.ox * SS, sp.oy * SS))
        _SPRITES.remove(sp)


def grow_curve(x, y, ang, length, steps, curl, rng):
    pts = [(x, y)]
    a = ang
    for _ in range(steps):
        a += rng.uniform(-curl, curl)
        x += math.cos(a) * length / steps
        y += math.sin(a) * length / steps
        pts.append((x, y))
    return pts, a


def point_along(pts, t):
    """Point and direction at fraction t of a polyline."""
    segs = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(segs)
    d = t * total
    for i, s in enumerate(segs):
        if d <= s or i == len(segs) - 1:
            f = d / s if s else 0
            x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f
            y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
            return x, y, math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
        d -= s
    return pts[-1][0], pts[-1][1], 0.0


# ----------------------------------------------------------------------------------------------------------------
# sakura blossom atlas
# ----------------------------------------------------------------------------------------------------------------
PETAL_OUT = (251, 230, 238)
PETAL_MID = (247, 204, 220)
PETAL_IN = (238, 164, 190)
FLOWER_EYE = (196, 62, 96)
STAMEN = (250, 242, 222)
ANTHER = (226, 186, 92)
PEDICEL = (132, 78, 72)
BUD = (226, 128, 158)
TWIG = (54, 38, 40)
TWIG_HI = (96, 72, 70)
YOUNG_LEAF = (128, 108, 58)


def petal_outline(r, width, notch):
    """Petal in local coords: base at (0,0), tip along +x at distance r, with a notch at the tip."""
    left = []
    for i in range(1, 11):
        t = i / 10.0
        w = width * r * (math.sin(math.pi * min(1.0, t ** 0.75)) ** 0.55) * (0.35 + 0.65 * t)
        left.append((t * r * 0.97, w * 0.5))
    right = [(x, -y) for x, y in reversed(left)]
    tip = [(r * (1.0 - notch), 0.0)]
    return [(0.0, 0.0)] + left + tip + right


def draw_flower(sp, cx, cy, r, rot, squash, sq_dir, rng, face_up=True):
    shade = rng.uniform(-0.05, 0.03)
    pink = rng.uniform(0.0, 1.0)
    c_out = jitter(lerp_col(PETAL_OUT, PETAL_MID, 0.25 * pink), rng, 0.03)
    c_mid = jitter(lerp_col(PETAL_MID, PETAL_IN, 0.3 * pink), rng, 0.04)
    c_in = jitter(PETAL_IN, rng, 0.05)
    c_line = lerp_col(c_mid, (200, 140, 160), 0.5)
    c_out = tuple(int(min(255, c * (1 + shade))) for c in c_out)
    cs, sn = math.cos(sq_dir), math.sin(sq_dir)

    def xf(px, py, ang, scale):
        # rotate petal-local point, scale about the flower centre, squash along sq_dir (foreshortening)
        ca, sa = math.cos(ang), math.sin(ang)
        x, y = (px * ca - py * sa) * scale, (px * sa + py * ca) * scale
        u, v = x * cs + y * sn, -x * sn + y * cs
        u *= squash
        return cx + u * cs - v * sn, cy + u * sn + v * cs

    base = petal_outline(r, rng.uniform(0.95, 1.1), rng.uniform(0.07, 0.13))
    order = list(range(5))
    rng.shuffle(order)
    for layer, (scale, col) in enumerate(((1.0, c_out), (0.62, c_mid), (0.34, c_in))):
        for k in order:
            ang = rot + k * 2 * math.pi / 5 + rng.uniform(-0.08, 0.08)
            pts = [xf(px, py, ang, scale) for px, py in base]
            sp.poly(pts, col, outline=c_line if layer == 0 else None)
    if face_up:
        er = r * 0.17
        sp.ellipse(cx, cy, er * max(0.5, squash), er, FLOWER_EYE)
        for k in range(11):
            ang = rng.uniform(0, 2 * math.pi)
            ln = r * rng.uniform(0.32, 0.46)
            x1, y1 = xf(ln, 0.0, ang, 1.0)
            sp.line([(cx, cy), (x1, y1)], 0.55, STAMEN)
            sp.ellipse(x1, y1, 0.9, 0.9, ANTHER)


def draw_cluster(sp, x, y, base_ang, fr, rng, n=None):
    """An umbel: 2-5 flowers (and the odd bud) on pedicels radiating from a spur at (x, y)."""
    n = n or rng.randint(3, 6)
    flowers = []
    for i in range(n):
        a = base_ang + rng.uniform(-1.8, 1.8)
        ln = fr * rng.uniform(0.7, 1.45)
        fx, fy = x + math.cos(a) * ln, y + math.sin(a) * ln
        sp.line([(x, y), ((x + fx) / 2 + rng.uniform(-2, 2), (y + fy) / 2 + rng.uniform(-2, 2)), (fx, fy)], 1.3, PEDICEL)
        flowers.append((fx, fy, a))
    rng.shuffle(flowers)
    for fx, fy, a in flowers:
        if rng.random() < 0.08:
            sp.ellipse(fx, fy, fr * 0.28, fr * 0.4, jitter(BUD, rng, 0.08))
            continue
        side = rng.random() < 0.35
        squash = rng.uniform(0.35, 0.7) if side else rng.uniform(0.8, 1.0)
        draw_flower(sp, fx, fy, fr * rng.uniform(0.9, 1.1), rng.uniform(0, 2 * math.pi), squash, a, rng,
                    face_up=(not side or rng.random() < 0.5))


def draw_young_leaf(sp, x, y, ang, ln, rng):
    w = ln * 0.32
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((t * ln, math.sin(math.pi * t) * w * 0.5))
    pts += [(t_x, -t_y) for t_x, t_y in reversed(pts[1:-1])]
    ca, sa = math.cos(ang), math.sin(ang)
    sp.poly([(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts], jitter(YOUNG_LEAF, rng, 0.1))


def fit_twigs(twigs, anchor, lo, hi):
    """Scale a twig set about its anchor so every point stays inside the box [lo, hi] (never scales up)."""
    ax, ay = anchor
    lo = (min(lo[0], ax), min(lo[1], ay))       # an anchor on the cell edge (a spray leaving the culm) is allowed
    hi = (max(hi[0], ax), max(hi[1], ay))
    s = 1.0
    for pts, _, _ in twigs:
        for x, y in pts:
            dx, dy = x - ax, y - ay
            for d, a, l, h in ((dx, ax, lo[0], hi[0]), (dy, ay, lo[1], hi[1])):
                if d > 1e-6 and a + d > h:
                    s = min(s, (h - a) / d)
                if d < -1e-6 and a + d < l:
                    s = min(s, (l - a) / d)
    if s >= 1.0:
        return twigs
    return [([(ax + (x - ax) * s, ay + (y - ay) * s) for x, y in pts], w0, w1) for pts, w0, w1 in twigs]


def sakura_spray(sp, rng, anchor, up_ang, reach, fr, density=1.0, side_twigs=6):
    """A twig spray growing from `anchor` in direction up_ang, laden with blossom clusters.
    The whole spray is scaled to stay inside its atlas cell with a margin for the flowers."""
    ax, ay = anchor
    main, _ = grow_curve(ax, ay, up_ang, reach, 14, 0.12, rng)
    twigs = [(main, 9.0, 2.4)]
    for i in range(side_twigs):
        t = 0.18 + 0.72 * i / max(1, side_twigs - 1) + rng.uniform(-0.04, 0.04)
        sx, sy, sa = point_along(main, t)
        side = 1 if i % 2 == 0 else -1
        ln = reach * rng.uniform(0.28, 0.45) * (1.0 - 0.45 * t)
        pts, _ = grow_curve(sx, sy, sa + side * rng.uniform(0.5, 0.95), ln, 8, 0.15, rng)
        twigs.append((pts, 5.0 * (1 - 0.4 * t), 1.6))
        if rng.random() < 0.55:
            qx, qy, qa = point_along(pts, rng.uniform(0.35, 0.6))
            sub, _ = grow_curve(qx, qy, qa - side * rng.uniform(0.4, 0.8), ln * 0.45, 5, 0.2, rng)
            twigs.append((sub, 2.6, 1.2))
    m = fr * 3.4
    twigs = fit_twigs(twigs, anchor, (m, m), (sp.size - m, sp.size - m))
    for pts, w0, w1 in twigs:
        sp.taper_line(pts, w0, w1, TWIG, TWIG_HI)
    # blossom clusters along every twig (denser towards the tips)
    clusters = []
    for pts, w0, w1 in twigs:
        total = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
        n = max(2, int(total / (fr * 1.45) * density))
        for k in range(n):
            t = (k + rng.uniform(0.3, 0.9)) / n
            x, y, a = point_along(pts, min(0.999, t))
            clusters.append((x, y, a))
        x, y, a = point_along(pts, 1.0)
        clusters.append((x, y, a))
    rng.shuffle(clusters)
    for i, (x, y, a) in enumerate(clusters):
        if rng.random() < 0.05:
            draw_young_leaf(sp, x, y, a + rng.choice((-1, 1)) * rng.uniform(0.6, 1.2), fr * 1.6, rng)
        draw_cluster(sp, x, y, a + rng.choice((-1, 1)) * math.pi / 2 * rng.uniform(0.3, 1.0), fr, rng)


def sakura_clump(sp, rng, cx, cy, rad, fr):
    """Dense ball of blossom with a few twig stubs - fills the crown volume in the lower LODs."""
    for _ in range(7):
        a = rng.uniform(0, 2 * math.pi)
        r0 = rad * rng.uniform(0.0, 0.3)
        pts, _ = grow_curve(cx + math.cos(a) * r0, cy + math.sin(a) * r0, a, rad * rng.uniform(0.5, 0.85), 6, 0.2, rng)
        sp.taper_line(pts, 4.0, 1.5, TWIG, TWIG_HI)
    spots = []
    for _ in range(9000):
        a = rng.uniform(0, 2 * math.pi)
        r = rad * math.sqrt(rng.random())
        edge = r / rad
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r * 0.92
        if edge > 0.72 and rng.random() < (edge - 0.72) * 3.0:
            continue
        if all((x - sx) ** 2 + (y - sy) ** 2 > (fr * 1.2) ** 2 for sx, sy in spots):
            spots.append((x, y))
        if len(spots) > 360:
            break
    for x, y in spots:
        draw_cluster(sp, x, y, rng.uniform(0, 2 * math.pi), fr, rng, n=rng.randint(2, 4))


def make_blossom_atlas(size=2048, seed=7):
    rng = random.Random(seed)
    img = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cell = size // 2
    fr = cell / 1024.0 * 19.0          # flower radius in px (1024 px cell ~ 0.9 m -> ~3.3 cm flowers)
    # cell 0: upright spray, anchor bottom centre
    sakura_spray(Sprite(img, d, 0, 0, cell), rng, (cell * 0.5, cell * 0.985), -math.pi / 2, cell * 0.86, fr, 1.0, 7)
    # cell 1: second upright spray, leaning
    sakura_spray(Sprite(img, d, cell, 0, cell), rng, (cell * 0.5, cell * 0.985), -math.pi / 2 + 0.12, cell * 0.84, fr, 1.1, 6)
    # cell 2: dense clump
    sakura_clump(Sprite(img, d, 0, cell, cell), rng, cell * 0.5, cell * 0.5, cell * 0.42, fr)
    # cell 3: radial spray seen from above (5 twigs from the centre)
    sp = Sprite(img, d, cell, cell, cell)
    for k in range(5):
        a = k * 2 * math.pi / 5 + rng.uniform(-0.25, 0.25)
        sakura_spray(sp, rng, (cell * 0.5, cell * 0.5), a, cell * 0.43, fr, 0.9, 2)
    flush_sprites(img)
    img = img.resize((size, size), Image.LANCZOS)
    arr = np.array(img)
    # keep the alpha crisp for alpha testing but not aliased: gentle contrast on alpha
    a = arr[..., 3].astype(np.float64) / 255.0
    a = np.clip((a - 0.5) * 1.6 + 0.5, 0, 1)
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(bleed(arr), "RGBA")


def windmask(size, cells):
    """cells: list of (kind, anchor_u, anchor_v, reach) per quadrant in atlas UV (v down).
    kind 'dist' -> red = distance from anchor / reach, 'const' -> red = reach."""
    img = np.zeros((size, size, 3), np.float64)
    ys, xs = np.mgrid[0:size, 0:size]
    u, v = (xs + 0.5) / size, (ys + 0.5) / size
    for q, (kind, au, av, reach) in enumerate(cells):
        cu, cv = (q % 2) * 0.5, (q // 2) * 0.5
        m = (u >= cu) & (u < cu + 0.5) & (v >= cv) & (v < cv + 0.5)
        if kind == "const":
            img[..., 0][m] = reach
        else:
            dist = np.sqrt((u - au) ** 2 + (v - av) ** 2) / reach
            img[..., 0][m] = np.clip(dist, 0, 1)[m] ** 1.2
    return Image.fromarray((img * 255).astype(np.uint8), "RGB")


# ----------------------------------------------------------------------------------------------------------------
# bamboo leaf atlas
# ----------------------------------------------------------------------------------------------------------------
LEAF_A = (70, 104, 44)
LEAF_B = (98, 130, 56)
LEAF_OLD = (150, 146, 70)
BRANCHLET = (96, 112, 58)


def bamboo_leaf(sp, x, y, ang, ln, wd, droop, rng):
    """Lanceolate leaf from its base (x, y): short petiole, widest ~25 %, long pointed tip, curving by `droop`."""
    n = 14
    axis = []
    a = ang
    px, py = x, y
    for i in range(n + 1):
        axis.append((px, py, a))
        a += droop / n
        px += math.cos(a) * ln / n
        py += math.sin(a) * ln / n
    left, right = [], []
    for i, (ax_, ay_, aa) in enumerate(axis):
        t = i / n
        if t < 0.06:
            w = wd * 0.12
        elif t < 0.25:
            w = wd * (0.12 + 0.88 * ((t - 0.06) / 0.19) ** 0.6)
        else:
            w = wd * (1.0 - (t - 0.25) / 0.75) ** 1.1
        nx, ny = -math.sin(aa), math.cos(aa)
        left.append((ax_ + nx * w / 2, ay_ + ny * w / 2))
        right.append((ax_ - nx * w / 2, ay_ - ny * w / 2))
    old = rng.random() < 0.12
    base = lerp_col(LEAF_A, LEAF_B, rng.random())
    if old:
        base = lerp_col(base, LEAF_OLD, rng.uniform(0.3, 0.7))
    c1 = jitter(base, rng, 0.06)
    c2 = tuple(int(c * 0.82) for c in c1)
    mid = [(p[0], p[1]) for p in axis]
    sp.poly(left + list(reversed(mid)), c1)
    sp.poly(right + list(reversed(mid)), c2)
    sp.line(mid[:-2], 0.8, lerp_col(c1, (190, 205, 140), 0.35))


def bamboo_twigs(rng, anchor, ang, reach, n_side, gravity):
    """Branchlet skeleton: a main twig from `anchor` that arcs under `gravity`, with short side twigs.
    Returns [(pts, w0, w1, fan)] where fan = number of leaves at the tip."""
    ax, ay = anchor
    pts, a = [(ax, ay)], ang
    x, y = ax, ay
    for i in range(12):
        dx, dy = math.cos(a), math.sin(a) + gravity * 0.035 * i
        a = math.atan2(dy, dx) + rng.uniform(-0.06, 0.06)
        x += math.cos(a) * reach / 12
        y += math.sin(a) * reach / 12
        pts.append((x, y))
    twigs = [(pts, 3.4, 1.4, rng.randint(4, 6))]
    for i in range(n_side):
        t = 0.2 + 0.78 * i / max(1, n_side - 1)
        sx, sy, sa = point_along(pts, t)
        side = 1 if i % 2 == 0 else -1
        sub, _ = grow_curve(sx, sy, sa + side * rng.uniform(0.35, 0.75), reach * rng.uniform(0.1, 0.2), 4, 0.12, rng)
        twigs.append((sub, 1.8, 1.0, rng.randint(2, 5)))
    return twigs


def draw_bamboo_twigs(sp, rng, twigs, leaf_len, droop):
    for pts, w0, w1, _ in twigs:
        sp.taper_line(pts, w0, w1, BRANCHLET)
    leaves = []
    for pts, _, _, fan in twigs:
        tx, ty, ta = point_along(pts, 1.0)
        for j in range(fan):
            a = ta + (j - (fan - 1) / 2) * rng.uniform(0.3, 0.5)
            dx, dy = math.cos(a), math.sin(a) + 0.7 * droop          # gravity pulls leaves down (+y)
            leaves.append((tx, ty, math.atan2(dy, dx), leaf_len * rng.uniform(0.8, 1.15)))
        # a couple of single leaves along the twig too
        for _ in range(rng.randint(0, 2)):
            qx, qy, qa = point_along(pts, rng.uniform(0.4, 0.9))
            a = qa + rng.choice((-1, 1)) * rng.uniform(0.5, 1.0)
            leaves.append((qx, qy, math.atan2(math.sin(a) + 0.7 * droop, math.cos(a)), leaf_len * rng.uniform(0.7, 1.0)))
    rng.shuffle(leaves)
    for tx, ty, a, ln in leaves:
        bamboo_leaf(sp, tx, ty, a, ln, ln * rng.uniform(0.13, 0.17), rng.uniform(0.2, 0.6) * droop, rng)


def bamboo_cell(sp, rng, sprays, leaf_len, droop):
    """sprays: [(anchor, ang, reach, n_side, gravity)] - all fitted together into the cell, then drawn."""
    anchor = sprays[0][0]
    twigs = []
    for anc, ang, reach, n_side, grav in sprays:
        twigs += bamboo_twigs(rng, anc, ang, reach, n_side, grav)
    m = leaf_len * 1.12
    fitted = fit_twigs([(p, w0, w1) for p, w0, w1, _ in twigs], anchor, (m, m), (sp.size - m, sp.size - m))
    twigs = [(fp, w0, w1, fan) for (fp, w0, w1), (_, _, _, fan) in zip(fitted, twigs)]
    draw_bamboo_twigs(sp, rng, twigs, leaf_len, droop)


def make_bamboo_leaf_atlas(size=2048, seed=11):
    rng = random.Random(seed)
    img = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cell = size // 2
    ll = cell / 1024.0 * 175.0     # leaf length px (1024 px cell ~ 1.2 m -> ~20 cm leaves)
    # cell 0 + 1: side sprays - anchor on the left edge (the culm), growing out to the right and arcing down
    for q, seedang in ((0, 0.05), (1, -0.1)):
        sp = Sprite(img, d, q * cell, 0, cell)
        anc = (cell * 0.03, cell * 0.3)
        sprays = [(anc, seedang + rng.uniform(-0.1, 0.1), cell * 0.95, 8, 0.8),
                  (anc, seedang - 0.45, cell * 0.55, 4, 0.6),
                  (anc, seedang + 0.5, cell * 0.6, 4, 0.9)]
        bamboo_cell(sp, rng, sprays, ll, 1.0)
    # cell 2: dense tuft (culm top) - many short sprays radiating from the centre, all drooping
    sp = Sprite(img, d, 0, cell, cell)
    anc = (cell * 0.5, cell * 0.45)
    sprays = [(anc, -math.pi / 2 + (k - 4) * 0.42 + rng.uniform(-0.1, 0.1), cell * rng.uniform(0.35, 0.5), 3, 0.7)
              for k in range(9)]
    bamboo_cell(sp, rng, sprays, ll * 0.95, 0.9)
    # cell 3: upright fan - anchor bottom centre (a culm tip), sprays up then arcing over
    sp = Sprite(img, d, cell, cell, cell)
    anc = (cell * 0.5, cell * 0.9)
    sprays = [(anc, -math.pi / 2 + (k - 2) * 0.3, cell * rng.uniform(0.8, 1.0), 6, 0.45) for k in range(5)]
    bamboo_cell(sp, rng, sprays, ll, 0.8)
    flush_sprites(img)
    img = img.resize((size, size), Image.LANCZOS)
    arr = np.array(img)
    a = arr[..., 3].astype(np.float64) / 255.0
    a = np.clip((a - 0.5) * 1.6 + 0.5, 0, 1)
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(bleed(arr), "RGBA")


# ----------------------------------------------------------------------------------------------------------------
# bamboo culm (tiling) and the pole item
# ----------------------------------------------------------------------------------------------------------------
CULM_COLS = [(64, 112, 48), (78, 110, 46), (118, 124, 58), (56, 92, 44)]   # young, mature, ageing, dark


def culm_column(h, w, base, seed, node_rows, powder=True, mottle=0.0):
    """One culm colour column. node_rows: list of row positions (image y) of nodes. Returns (rgb float, height)."""
    fib = periodic_noise(h, w, 1.0, 40.0, seed) * 0.5 + periodic_noise(h, w, 4.0, 90.0, seed + 1) * 0.5
    blot = periodic_noise(h, w, 25.0, 25.0, seed + 2)
    rgb = np.ones((h, w, 3)) * np.array(base, np.float64)
    rgb *= (1.0 + fib[..., None] * 0.06 + blot[..., None] * 0.05)
    hgt = fib * 0.15
    ys = np.arange(h)[:, None]
    for nr in node_rows:
        dy = (ys - nr + h / 2) % h - h / 2        # signed wrapped distance to the node row (px)
        ring = np.exp(-(dy / 5.0) ** 2)            # the sheath scar
        ridge = np.exp(-((dy + 12.0) / 7.0) ** 2)  # raised supranodal ridge just above it
        rgb = rgb * (1.0 - 0.55 * ring[..., None]) + ring[..., None] * np.array([40, 30, 14])
        rgb += ridge[..., None] * np.array([34, 36, 16])
        hgt += ridge * 1.5 - ring * 0.6
        if powder:
            band = np.where((dy > 4) & (dy < 130), np.exp(-(dy - 4) / 45.0), 0.0)
            rgb = rgb * (1 - 0.45 * band[..., None]) + np.array([205, 212, 190]) * 0.45 * band[..., None]
    if mottle > 0:
        m = np.clip(periodic_noise(h, w, 10.0, 10.0, seed + 3) * 2.0 - 0.9, 0, 1)
        rgb = rgb * (1 - mottle * m[..., None]) + np.array([150, 138, 80]) * mottle * m[..., None]
    return rgb, hgt


def make_culm_textures(size=1024):
    cw = size // 4
    rgb = np.zeros((size, size, 3))
    hgt = np.zeros((size, size))
    for i, base in enumerate(CULM_COLS):
        c, hh = culm_column(size, cw, base, 100 + i, [0], powder=(i in (0, 1, 3)), mottle=(0.5 if i == 2 else 0.12))
        rgb[:, i * cw:(i + 1) * cw] = c
        hgt[:, i * cw:(i + 1) * cw] = hh
    co = Image.fromarray(rgb.clip(0, 255).astype(np.uint8), "RGB")
    no = height_to_normal_dx(hgt, 3.0)
    return co, no


POLE_LEN = 2.5
POLE_NODES = [0.16, 0.54, 0.93, 1.31, 1.70, 2.09, 2.44]   # metres from the top end


def make_pole_textures(w=512, h=2048):
    cw = int(w * 0.75)
    rows = [int(n / POLE_LEN * h) for n in POLE_NODES]
    # green at the top end, sun-cured yellow-green at the butt
    top, butt = np.array([72, 112, 48], np.float64), np.array([150, 146, 72], np.float64)
    t = (np.arange(h) / (h - 1))[:, None, None]
    base = top * (1 - t) + butt * t
    fib = periodic_noise(h, cw, 1.0, 40.0, 5) * 0.5 + periodic_noise(h, cw, 4.0, 90.0, 6) * 0.5
    rgb = base * (1.0 + fib[..., None] * 0.06)
    hgt = fib * 0.15
    ys = np.arange(h)[:, None]
    for nr in rows:
        dy = ys - nr
        ring = np.exp(-(dy / 2.5) ** 2)
        ridge = np.exp(-((dy + 6.0) / 4.0) ** 2)
        rgb *= (1.0 - 0.45 * ring[..., None])
        rgb += ridge[..., None] * np.array([18, 18, 8])
        hgt = hgt + ridge * 1.0 - ring * 0.4
        band = np.where((dy > 2) & (dy < 40), np.exp(-(dy - 2) / 16.0), 0.0)
        rgb = rgb * (1 - 0.25 * band[..., None]) + np.array([200, 205, 180]) * 0.25 * band[..., None]
    full = np.zeros((h, w, 3))
    full[:, :cw] = rgb
    full_h = np.zeros((h, w))
    full_h[:, :cw] = hgt
    # end cap square (u 0.75..1, v 0..128/h): cut culm - pale wall ring, dark hollow, faint growth rings
    cs = w - cw
    yy, xx = np.mgrid[0:cs, 0:cs]
    r = np.sqrt((xx - cs / 2 + 0.5) ** 2 + (yy - cs / 2 + 0.5) ** 2) / (cs / 2)
    cap = np.zeros((cs, cs, 3))
    wall = (r > 0.80) & (r <= 1.0)
    cap[...] = np.array([70, 52, 36])                              # hollow (shadowed inside)
    cap[wall] = np.array([214, 206, 150])                           # cut wall, pale
    cap[(r > 0.96)] = np.array([96, 120, 52])                       # green skin edge
    cap[(r > 0.8) & (r < 0.83)] = np.array([176, 160, 110])         # inner wall edge
    full[0:cs, cw:w] = cap
    full[cs:, cw:w] = rgb[cs:, 0:w - cw]            # unused strip: culm colour, so mip bleed at the u seam stays green
    co = Image.fromarray(full.clip(0, 255).astype(np.uint8), "RGB")
    no = height_to_normal_dx(full_h, 3.0)
    return co, no


# ----------------------------------------------------------------------------------------------------------------
# bark
# ----------------------------------------------------------------------------------------------------------------
def make_bark(size=1024):
    src = os.path.join(DATA, "polyhaven")
    diff = Image.open(os.path.join(src, "sakura_bark_diff_2k.jpg")).convert("RGB").resize((size, size), Image.LANCZOS)
    nor = Image.open(os.path.join(src, "sakura_bark_nor_dx_2k.jpg")).convert("RGB").resize((size, size), Image.LANCZOS)
    a = np.asarray(diff).astype(np.float64)
    # Somei-yoshino bark: darker, cooler, faintly purple-brown; keep the lenticel bands (they are the point)
    lum = a.mean(axis=2, keepdims=True)
    a = a * 0.55 + lum * 0.45 * np.array([1.0, 0.93, 0.95])
    a = a * np.array([0.66, 0.58, 0.60])
    a = ((a / 255.0) ** 1.08) * 255.0
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGB"), nor


# ----------------------------------------------------------------------------------------------------------------
def save(img, name, p_rel):
    png = os.path.join(WORK_TEX, name + ".png")
    img.save(png)
    paa = os.path.join(src_dir(p_rel), "data", name + ".paa")
    os.makedirs(os.path.dirname(paa), exist_ok=True)
    to_paa(png, paa)
    print("  %-34s %s  -> %s (%d bytes)" % (name, img.size, os.path.relpath(paa, src_dir("JP\\plants")), os.path.getsize(paa)))


def main(argv):
    only = set(argv)
    print("textures ->", WORK_TEX)
    if not only or "bark" in only:
        co, no = make_bark()
        save(co, "jp_sakura_bark_co", P_TREE)
        save(no, "jp_sakura_bark_nohq", P_TREE)
    if not only or "blossom" in only:
        save(make_blossom_atlas(), "jp_sakura_blossom_ca", P_TREE)
        save(windmask(256, [("dist", 0.25, 0.49, 0.43), ("dist", 0.75, 0.49, 0.43),
                            ("const", 0, 0, 0.35), ("dist", 0.75, 0.75, 0.23)]), "jp_sakura_blossom_windmask_co", P_TREE)
    if not only or "bamboo" in only:
        co, no = make_culm_textures()
        save(co, "jp_bamboo_culm_co", P_BAMBOO)
        save(no, "jp_bamboo_culm_nohq", P_BAMBOO)
        save(make_bamboo_leaf_atlas(), "jp_bamboo_leaves_ca", P_BAMBOO)
        save(windmask(256, [("dist", 0.015, 0.15, 0.3), ("dist", 0.515, 0.15, 0.3),
                            ("dist", 0.25, 0.725, 0.2), ("dist", 0.75, 0.95, 0.28)]), "jp_bamboo_leaves_windmask_co", P_BAMBOO)
    if not only or "pole" in only:
        co, no = make_pole_textures()
        save(co, "jp_bamboo_pole_co", P_ITEMS)
        save(no, "jp_bamboo_pole_nohq", P_ITEMS)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
