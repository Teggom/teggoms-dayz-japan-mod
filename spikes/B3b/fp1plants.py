"""fp1plants - FP1 (2026-10-01) remake of the potted plants (L2 #58, Stephen: 'redo completely'): unglazed pots, a
potted pine with a real trunk / branch structure and needle pads, a satsuki azalea, chrysanthemums with leaves,
stakes and flower heads.

Era (research/interior/LIFE_LAYER_ERA.md #58, binding): a small pine, an azalea (satsuki), chrysanthemums (the Kyoho
kiku fashion); unglazed earthenware pots or a cut-down tub, no glazed Chinese-style trays, no morning glories.
Forms (general knowledge, no web request): an Edo flower pot (ueki-bachi) is a deep round unglazed pot with a thick
rolled rim and a low foot; a potted pine is kept small like a bonsai: a thick, tapering, S-curved trunk with surface
roots (nebari), branches set alternately up the trunk, the needles in flat cloud pads on the branch ends, a rounded
apex pad; a satsuki is a low dome of small leaves on a few stems (no flowers in autumn); chrysanthemums in autumn
are several upright stems tied to a thin bamboo stake, lobed leaves up the stems, one flower head per stem, one
colour per pot (white, yellow or rust). Materials: jp_m_ceramic_earthenware, jp_m_plant_kiku (both FP1),
jp_m_plant_foliage (L2's needle / leaf cards), wood_sooted bark, wood_weathered stems.
"""
import math
import random

from skit import core, xf, pole, lathe  # noqa: F401
import fkit

ROPE = "straw_rope"
EARTHEN = "ceramic_earthenware"
FOLI = "plant_foliage"
KIKU = "plant_kiku"
BARK = "wood_sooted"
STEM = "wood_weathered"


def earthen_pot(c, r=0.11, h=0.17, wear=None, vis=(1,), soil=True, soil_mat="ground_leaf_litter", soil_wear="_w1",
                shallow=False):
    """An unglazed flower pot standing at c: a low foot, a slightly flared wall, a thick rolled rim, the inside wall
    and the soil 3 cm below the rim. shallow: a low wide pot (pine)."""
    if shallow:
        prof = [(0.0, 0.0), (r * 0.84, 0.0), (r * 0.92, 0.016), (r, h * 0.80), (r + 0.010, h * 0.88),
                (r + 0.010, h), (r - 0.010, h), (r - 0.014, h - 0.026)]
    else:                                     # the inside ends under the soil disc (never seen)
        prof = [(0.0, 0.0), (r * 0.64, 0.0), (r * 0.70, 0.02), (r * 0.94, h * 0.82), (r + 0.013, h * 0.90),
                (r + 0.012, h), (r - 0.012, h), (r - 0.016, h - 0.036)]
    out = [fkit.lathe(prof, 8, EARTHEN, vis=vis, smooth=True)]
    out.append(fkit.lathe([(0.0, 0.0), (r * 0.8, 0.0), (r + 0.01, h), (0.0, h)], 6, EARTHEN, vis=(2,), smooth=False))
    if wear:
        for s in out:
            s.wear = wear
    if soil:
        sy = h - (0.022 if shallow else 0.032)
        sr = (r - 0.012) * (0.97 if shallow else 0.94)
        s = fkit.lathe([(0.0, sy + 0.004), (sr, sy)], 8, soil_mat, vis=vis, smooth=False)
        s.wear = soil_wear
        out.append(s)
    return [fkit.xf(s, t=c) for s in out]


def _card(pts, mat, uvs, vis=(1,), wear=None):
    """A two-sided quad card (front + back) through 4 points."""
    n = core.norm(core.newell(pts))
    a = core.sheet([list(pts)], mat, n, vis=vis, uvs=[list(uvs)])
    b = core.sheet([list(pts)[::-1]], mat, core.mul(n, -1.0), vis=vis, uvs=[list(uvs)[::-1]])
    for s in (a, b):
        s.finalize()
        if wear:
            s.wear = wear
    return [a, b]


def pad(c, rx, rz, h, kind="needle", wear=None, vis=(1,), yaw=0.0, seed=1):
    """A foliage pad (a flat cloud of needles / leaves): a horizontal top card, a smaller under card and two crossed
    upright cards, all two-sided, on plant_foliage's needle (u 0-0.5) or leaf (u 0.5-1) half."""
    rg = random.Random(seed)
    u0 = 0.0 if kind == "needle" else 0.5
    x, y, z = c
    ca, sa = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))

    def P(px, py, pz):
        return (x + px * ca - pz * sa, y + py, z + px * sa + pz * ca)
    out = []
    # top and under layers: two quads turned 45 deg to each other, so the outline reads as a rounded cloud, not a square
    for yy, k, turn in ((h * 0.6, 1.0, 0.0), (h * 0.62, 0.86, 45.0), (h * 0.05, 0.78, 22.0)):
        t = math.radians(turn)
        ct, st = math.cos(t), math.sin(t)

        def R(px, pz):
            return P(px * ct - pz * st, 0.0, px * st + pz * ct)
        q = [R(-rx * k, -rz * k), R(rx * k, -rz * k), R(rx * k, rz * k), R(-rx * k, rz * k)]
        q = [(a[0], a[1] + yy + (rg.uniform(-0.008, 0.008) if i % 2 else 0.0), a[2]) for i, a in enumerate(q)]
        out += _card(q, FOLI, [(u0, 0.0), (u0 + 0.45, 0.0), (u0 + 0.45, 0.6), (u0, 0.6)], vis, wear)
    for ang in (0.0, 90.0):
        a = math.radians(ang)
        dx, dz = math.cos(a), math.sin(a)
        rr = rx if ang == 0.0 else rz
        q = [P(-dx * rr, 0.0, -dz * rr), P(dx * rr, 0.0, dz * rr), P(dx * rr * 0.8, h, dz * rr * 0.8),
             P(-dx * rr * 0.8, h, -dz * rr * 0.8)]
        out += _card(q, FOLI, [(u0, 0.9), (u0 + 0.45, 0.9), (u0 + 0.45, 0.4), (u0, 0.4)], vis, wear)
    return out


def limb(pts, r0, r1, mat, sides=5, vis=(1,), wear=None, step=0.035):
    """A tapering round limb (trunk, branch, root) along a smooth curve through pts."""
    import w2kit
    path = w2kit._catmull(pts, step)
    T, _, _ = w2kit._frames(path)
    return w2kit._tube(path, T, r0, sides, mat, vis, wear, tile=0.5, cap0=True, cap1=True,
                       taper=lambda t: (r0 + (r1 - r0) * t) / r0)


def pine_bonsai(c, size=1.0, seed=1, wear=None, foliage_wear="_w1", vis=(1,)):
    """A potted pine kept small: S-curved tapering trunk (dark bark), three surface roots, four branches set
    alternately (low left long, right, back, front-high short), needle pads on the branch ends and a rounded apex."""
    rg = random.Random(seed)
    x, y, z = c
    S = size
    tr = [(0.0, 0.0, 0.0), (0.04, 0.09, 0.01), (-0.015, 0.19, -0.01), (0.03, 0.28, 0.005), (0.0, 0.36, 0.0)]
    tr = [(x + px * S, y + py * S, z + pz * S) for px, py, pz in tr]
    out = [limb(tr, 0.032 * S, 0.009 * S, BARK, sides=6, vis=vis, wear=wear)]
    for k in range(3):                                         # nebari: surface roots
        a = 2 * math.pi * k / 3 + rg.uniform(-0.3, 0.3)
        out.append(limb([(x, y + 0.012, z), (x + 0.045 * S * math.cos(a), y + 0.004, z + 0.045 * S * math.sin(a))],
                        0.016 * S, 0.004 * S, BARK, sides=4, vis=vis, wear=wear))

    def at(t):
        f = t * (len(tr) - 1)
        i = min(len(tr) - 2, int(f))
        u = f - i
        return core.add(tr[i], core.mul(core.sub(tr[i + 1], tr[i]), u))
    for t, ang, L, droop in ((0.32, 200.0, 0.17, -0.02), (0.50, 20.0, 0.14, 0.0), (0.66, 120.0, 0.11, 0.01),
                             (0.80, -60.0, 0.09, 0.02)):
        p0 = at(t)
        a = math.radians(ang + rg.uniform(-12, 12))
        d = (math.cos(a), 0.0, math.sin(a))
        p1 = core.add(p0, (d[0] * L * 0.55 * S, droop * S, d[2] * L * 0.55 * S))
        p2 = core.add(p0, (d[0] * L * S, (droop + 0.025) * S, d[2] * L * S))
        out.append(limb([p0, p1, p2], 0.011 * S, 0.004 * S, BARK, sides=4, vis=vis, wear=wear))
        out += pad(core.add(p2, (0.0, -0.005 * S, 0.0)), (0.065 + L * 0.25) * S, (0.050 + L * 0.15) * S, 0.05 * S,
                   "needle", wear=foliage_wear, vis=vis, yaw=-math.degrees(a), seed=seed + int(ang))
    out += pad(core.add(tr[-1], (0.0, -0.015 * S, 0.0)), 0.075 * S, 0.065 * S, 0.065 * S, "needle", wear=foliage_wear,
               vis=vis, yaw=rg.uniform(0, 90), seed=seed + 7)
    return out


def azalea(c, size=1.0, seed=1, wear=None, foliage_wear="_w1", vis=(1,), half_dead=False):
    """A potted satsuki: a short trunk splitting into three stems, a rounded mound of leaf pads (no flowers in
    autumn); half_dead: one side's pads and the crown brown."""
    rg = random.Random(seed)
    x, y, z = c
    S = size
    out = [limb([(x, y, z), (x + 0.01 * S, y + 0.07 * S, z)], 0.016 * S, 0.012 * S, STEM, sides=5, vis=vis, wear=wear)]
    tops = []
    for k in range(3):
        a = 2 * math.pi * k / 3 + rg.uniform(-0.3, 0.3)
        tp = (x + 0.06 * S * math.cos(a), y + rg.uniform(0.15, 0.19) * S, z + 0.06 * S * math.sin(a))
        out.append(limb([(x + 0.01 * S, y + 0.07 * S, z), tp], 0.010 * S, 0.005 * S, STEM, sides=4, vis=vis,
                        wear=wear))
        tops.append((a, tp))
    for k, (a, tp) in enumerate(tops):
        fw = "_w2" if (half_dead and k == 0) else foliage_wear
        out += pad(tp, 0.085 * S, 0.075 * S, 0.07 * S, "leaf", wear=fw, vis=vis, yaw=-math.degrees(a), seed=seed + k)
    out += pad((x, y + 0.20 * S, z), 0.08 * S, 0.08 * S, 0.06 * S, "leaf", wear=("_w2" if half_dead else foliage_wear),
               vis=vis, seed=seed + 9)
    return out


def kiku_head(c, r, band, wear=None, vis=(1,), n=7):
    """A chrysanthemum head at c: a domed disc of ray petals (plant_kiku colour column `band`: 0 white, 1 yellow,
    2 rust), the tips curving down, closed underneath; explicit uv: v from the centre (0) to the tips (1)."""
    x, y, z = c
    u0, du = band / 3.0 + 0.01, 1.0 / 3.0 - 0.02
    prof = [(0.0, 0.020), (r * 0.55, 0.017), (r, 0.0), (r * 0.6, -0.012)]
    vv = [0.0, 0.5, 1.0, 0.85]
    quads, normals, uvs = [], [], []
    for i in range(len(prof) - 1):
        (r0, y0), (r1, y1) = prof[i], prof[i + 1]
        dr, dy = r1 - r0, y1 - y0
        L = math.hypot(dr, dy) or 1.0
        for k in range(n):
            a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
            am = (a0 + a1) / 2
            p = [(x + r0 * math.cos(a0), y + y0, z + r0 * math.sin(a0)), (x + r0 * math.cos(a1), y + y0, z + r0 * math.sin(a1)),
                 (x + r1 * math.cos(a1), y + y1, z + r1 * math.sin(a1)), (x + r1 * math.cos(a0), y + y1, z + r1 * math.sin(a0))]
            uv = [(u0 + du * k / n, vv[i]), (u0 + du * (k + 1) / n, vv[i]), (u0 + du * (k + 1) / n, vv[i + 1]),
                  (u0 + du * k / n, vv[i + 1])]
            if r0 < 1e-6:
                p, uv = [p[0], p[2], p[3]], [uv[0], uv[2], uv[3]]
            quads.append(p)
            uvs.append(uv)
            normals.append((-dy / L * math.cos(am), dr / L, -dy / L * math.sin(am)))
    for k in range(n):                                        # the underside
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        quads.append([(x, y - 0.014, z), (x + r * 0.6 * math.cos(a1), y - 0.012, z + r * 0.6 * math.sin(a1)),
                      (x + r * 0.6 * math.cos(a0), y - 0.012, z + r * 0.6 * math.sin(a0))])
        normals.append((0.0, -1.0, 0.0))
        uvs.append([(u0, 0.92), (u0 + du * 0.5, 0.92), (u0 + du * 0.5, 0.96)])
    s = core.sheet(quads, KIKU, normals, vis=vis, uvs=uvs)
    s.finalize()
    fkit.auto_smooth(s, 70.0)
    if wear:
        s.wear = wear
    return s


def kiku(c, size=1.0, seed=1, wear=None, flowers=True, band=None, vis=(1,)):
    """Potted chrysanthemums: four stems from the soil tied to a thin bamboo stake, three lobed leaf cards up each
    stem, a flower head on each (one colour per pot); withered and bent over when wear is _w2."""
    rg = random.Random(seed)
    x, y, z = c
    S = size
    band = rg.randint(0, 2) if band is None else band
    dead = wear == "_w2"
    out = [pole((x + 0.012, y - 0.01, z), (x + 0.010, y + 0.40 * S, z), 0.003, "bamboo_weathered", n=3, vis=vis)]
    out.append(core.box(x - 0.025, x + 0.03, y + 0.24 * S, y + 0.252 * S, z - 0.025, z + 0.025, ROPE, vis=vis))
    for k in range(4):
        a = 2 * math.pi * k / 4 + rg.uniform(-0.4, 0.4)
        lean = rg.uniform(0.035, 0.06) * S
        top = (x + lean * math.cos(a), y + rg.uniform(0.33, 0.40) * S, z + lean * math.sin(a))
        if dead:
            top = (top[0] + 0.05 * S * math.cos(a), top[1] - 0.08 * S, top[2] + 0.05 * S * math.sin(a))
        out.append(pole((x, y, z), top, 0.004, STEM, n=3, vis=vis, r1=0.003, wear=wear))
        for j in range(3):
            t = 0.30 + 0.22 * j
            p = core.add((x, y, z), core.mul(core.sub(top, (x, y, z)), t))
            la = a + (1 if j % 2 else -1) * rg.uniform(0.6, 1.2)
            L = rg.uniform(0.055, 0.07) * S
            w = L * 0.6
            dx, dz = math.cos(la), math.sin(la)
            px, pz = -dz, dx
            lift = (0.01 if not dead else -0.03) * S
            q = [(p[0] + px * w / 2, p[1], p[2] + pz * w / 2), (p[0] - px * w / 2, p[1], p[2] - pz * w / 2),
                 (p[0] + dx * L - px * w / 2, p[1] + lift, p[2] + dz * L - pz * w / 2),
                 (p[0] + dx * L + px * w / 2, p[1] + lift, p[2] + dz * L + pz * w / 2)]
            out += _card(q, FOLI, [(0.55, 0.1), (0.78, 0.1), (0.78, 0.38), (0.55, 0.38)], vis,
                         "_w2" if dead else (wear or "_w1"))
        if flowers or dead:
            out.append(kiku_head(top, rg.uniform(0.028, 0.036) * S, band, wear="_w2" if dead else wear, vis=vis))
    return out
