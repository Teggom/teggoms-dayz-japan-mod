"""Life layer G (research/interior/LIFE_LAYER.md items 51-62): yard, eaves and field, outdoor, autumn, 'as left'.

Folder src/JP/site/yard_life. Mounts: field (hasa racks, scarecrows), eaves (persimmon curtains, the moon-viewing
stand on a veranda, the bird cage), yard (the rest). Era verdicts: research/interior/LIFE_LAYER_ERA.md (L2 section).
"""
import math
import random

import l2kit as K
from l2kit import (core, box, prism, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, beam,
                   rope_path, sag, grid_sheet, text_ok, leaves, litter, add_all, ground, hull3, disc, rest, M, rng,
                   bipyramid, cord, lod_box, card, bush, WOOD, DARK, INT, BAMBOO, WEAVE, IRON, PALE, DARKC, RIVER,
                   FIELD, CUT, MUSHIRO, TAWARA, ROPE, STACK, PAPER, KINARI, PLAIN, INDIGO, LEAF, EARTH, SUMI, LIFE,
                   RICE, KAKI, FOLI, SOOTW)
import props_life_wall as LW      # L1 (read-only): kasa()
import fp1kit as FK               # FP1 (2026-10-01): brooms, rice sheaves (spikes/B3b/fp1kit.py)
import fp1plants as FP            # FP1: pots, potted pine, azalea, chrysanthemums (spikes/B3b/fp1plants.py)

CAT = "yard_life"
PROPS = []


def view_hull(ss, mat=STACK):
    """Soft cover: one View-only convex component round the given solids (sight stops, bullets pass)."""
    return hull3([v for s in ss for v in s.verts], mat, geo=False, view=True, fire=False)


def view_boxes(ss, n=4, mat=STACK):
    """FP1: soft cover for a row of hung sheaves: n View-only boxes along x round the sheaves' extent (a hull of the
    many round bundles is not reliably closed); sight stops, bullets pass."""
    if not ss:
        return []
    xs = sorted(set(round(v[0], 3) for s in ss for v in s.verts))
    x0, x1 = xs[0], xs[-1]
    out = []
    for k in range(n):
        a, b = x0 + (x1 - x0) * k / n, x0 + (x1 - x0) * (k + 1) / n
        vs = [v for s in ss for v in s.verts if a - 0.05 <= v[0] <= b + 0.05]
        if not vs:
            continue
        ys, zs = [v[1] for v in vs], [v[2] for v in vs]
        out.append(box(a + 0.01, b - 0.01, min(ys) + 0.02, max(ys) - 0.02, min(zs) + 0.02, max(zs) - 0.02, mat, vis=(),
                       geo=False, view=True, fire=False))
    return out


# ================================================================================================ 51 hasa-kake
def sheaf(x0, x1, y, d, half=0.17, wear=None, vis=(1,)):
    """Rice sheaves hung astride a rail at height y between x0 and x1, dropping d: one convex wedge."""
    pts = [(y + 0.05, -0.04), (y + 0.05, 0.04), (y - 0.55 * d, half), (y - d, 0.8 * half), (y - d, -0.8 * half),
           (y - 0.55 * d, -half)]
    s = prism(pts, "x", x0, x1, STACK, vis=vis)
    s.uv = "grain"
    if wear:
        s.wear = wear
    return s


def sheaf_row(x0, x1, yfun, seed, wear=None, seg=0.23, drop=(0.52, 0.72), skip=(), z=0.0, r_pole=0.022,
              avoid=()):
    """FP1 remake (2026-10-01, Stephen: the sheaves read as brown slabs clipping the rack): one rice sheaf every
    `seg` m, split and hung astride the rail at (yfun(x), z): tied neck and cut ends riding on top of the rail, two
    bundles hanging down either side, ears down, golden and spread (spikes/B3b/fp1kit.hung_sheaf). `avoid`: x of
    posts / stake crotches to keep clear (0.09 m)."""
    r = random.Random(seed)
    out = []
    n = max(1, int(round((x1 - x0) / seg)))
    for i in range(n):
        if i in skip:
            continue
        x = x0 + (x1 - x0) * (i + 0.5) / n + r.uniform(-0.02, 0.02)
        if any(abs(x - a) < 0.09 for a in avoid):
            continue
        out += FK.hung_sheaf(x, yfun(x), z, r_pole, r.uniform(*drop), r, wear=wear)
    return out


def stake_pair(x, H, lean=0.0, wear=None):
    """Crossed stakes (the rail rests in their crotch at H): legs spread 0.8 m in z, 0.35 m buried; lean tilts the
    pair about its foot (degrees about z)."""
    a = pole((x, -0.35, -0.48), (x, H + 0.30, 0.20), 0.035, WOOD, n=5, vis=(1, 2), wear=wear)
    b = pole((x, -0.35, 0.48), (x, H + 0.30, -0.20), 0.035, WOOD, n=5, vis=(1, 2), wear=wear)
    lo3 = beam((x, -0.35, 0.0), (x, H + 0.3, 0.0), 0.05, 0.6, WOOD, vis=(3,), wear=wear)
    ss = [a, b, lo3]
    c = hull3([v for s in (a, b) for v in s.verts], WOOD)
    if lean:
        ss = xfs(ss, rz=lean, pivot=(x, 0.0, 0.0))
        c = xf(c, rz=lean, pivot=(x, 0.0, 0.0))
    return ss, c


def hasa(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("hasa", budget="medium", res3=True, mass=60.0, bury=0.37, wear=wear or "_w1")
    if kind in ("low", "ab_sagged"):
        H, xs = 1.20, (-1.82, 0.0, 1.82)
        lean = {0: 0.0, 1: -28.0 if ab else 0.0, 2: 0.0}
        mids = []
        for i, x in enumerate(xs):
            ss, c = stake_pair(x, H, lean[i], wear=wear)
            add_all(P, ss)
            P.add(c)
            a = math.radians(lean[i])
            mids.append((x - (H + 0.02) * math.sin(a), (H + 0.02) * math.cos(a) - 0.02))
        # rail (bamboo) from crotch to crotch; sagged: through the leaning pair's lowered crotch
        for (xa, ya), (xb, yb) in zip(mids, mids[1:]):
            P.add(pole((xa - (0.1 if xa == mids[0][0] else 0.0), ya, 0.0), (xb + (0.1 if xb == mids[-1][0] else 0.0),
                                                                          yb, 0.0), 0.022, BAMBOO, n=5, vis=(1, 2),
                       wear=wear))
            dx = xb - xa
            L = math.hypot(dx, yb - ya)
            ux, uy = dx / L, (yb - ya) / L
            P.add(col_solid(beam((xa + ux * 0.06, ya + uy * 0.06, 0.0), (xb - ux * 0.06, yb - uy * 0.06, 0.0), 0.045,
                                 0.045, BAMBOO)))

        def yat(x):
            for (xa, ya), (xb, yb) in zip(mids, mids[1:]):
                if xa - 0.2 <= x <= xb + 0.2:
                    t = min(1.0, max(0.0, (x - xa) / (xb - xa)))
                    return ya + (yb - ya) * t
            return H
        shv = sheaf_row(-1.9, 1.9, yat, 51, wear=wear, skip=(4, 5, 11) if ab else (), avoid=[m[0] for m in mids],
                        drop=(0.50, 0.66))
        if ab:        # the fallen sheaves lie in the stubble below
            r = random.Random(5)
            for k in range(4):
                s = FK.standing_sheaf((0.0, 0.0, 0.0), (0.0, 0.62, 0.0), r, wear="_w2")
                shv += rest(xfs(s, rx=90.0 + r.uniform(-12, 12), ry=r.uniform(-40, 40),
                                t=(r.uniform(-1.4, 1.4), 0.0, r.uniform(0.5, 1.0))), 0.0)
            add_all(P, [litter(8, 0.0, 0.7, 1.4, sx=2.0)])
        add_all(P, shv)
        hang = [s for s in shv if s.bbox()[2] > 0.3]
        add_all(P, view_boxes(hang, 4))
        P.add(prism([(H + 0.05, -0.04), (H + 0.05, 0.04), (H - 0.62, 0.16), (H - 0.62, -0.16)], "x", -1.9, 1.9,
                    STACK, vis=(2,)))
        P.solids[-1].wear = wear
        P.add(box(-1.9, 1.9, H - 0.62, H + 0.05, -0.12, 0.12, STACK, vis=(3,)))
        P.solids[-1].wear = wear
        P.dim("span", 3.64, xs[-1] - xs[0], tol=0.01)
        P.dim("rail_h", 1.20, H, tol=0.01)
        P.notes.append("one-rail rack on crossed stakes, 2 ken; sheaves hung astride the rail (soft cover: View only)")
    elif kind in ("tiers", "empty"):
        rails = (0.90, 1.45, 2.00)
        for x in (-1.82, 0.0, 1.82):
            P.add(pole((x, -0.35, 0.0), (x, 2.35, 0.0), 0.055, WOOD, n=6, vis=(1, 2), r1=0.045))
            P.add(col(x - 0.05, x + 0.05, -0.35, 2.35, -0.05, 0.05))
        P.add(W(-1.87, 1.87, -0.35, 2.35, -0.04, 0.04, WOOD, vis=(3,)))
        for k, y in enumerate(rails):
            P.add(pole((-1.95, y, 0.075), (1.95, y, 0.075), 0.02, BAMBOO, n=5, vis=(1, 2)))
            for xa, xb in ((-1.95, -1.87), (-1.77, -0.05), (0.05, 1.77), (1.87, 1.95)):
                P.add(col(xa, xb, y - 0.02, y + 0.02, 0.055, 0.095, BAMBOO))
            for x in (-1.82, 0.0, 1.82):         # rope lashings
                P.add(box(x - 0.03, x + 0.03, y - 0.03, y + 0.03, 0.05, 0.10, ROPE, vis=(1,)))
            if kind == "tiers":
                shv = sheaf_row(-1.9, 1.9, lambda x, y=y: y, 60 + k, seg=0.27, z=0.075, r_pole=0.02,
                                avoid=(-1.82, 0.0, 1.82), drop=(0.42, 0.48))
                add_all(P, shv)
                add_all(P, view_boxes(shv, 2))
                P.add(xf(prism([(y + 0.05, -0.04), (y + 0.05, 0.04), (y - 0.5, 0.15), (y - 0.5, -0.15)], "x", -1.9, 1.9,
                               STACK, vis=(2,)), t=(0.0, 0.0, 0.075)))
                P.add(box(-1.9, 1.9, y - 0.5, y + 0.05, -0.05, 0.2, STACK, vis=(3,)))
            else:
                r = random.Random(70 + k)
                for i in range(3):                       # a few thin grey wisps left on the empty rails
                    x = r.uniform(-1.6, 1.6)
                    if min(abs(x - a) for a in (-1.82, 0.0, 1.82)) < 0.1:
                        x += 0.2
                    add_all(P, FK.hung_sheaf(x, y, 0.075, 0.02, 0.25, r, wear="_w2"))
        if kind == "empty":
            P.add(litter(9, 0.3, 0.3, 1.2, sx=2.2))
        P.dim("span", 3.64, 3.64, tol=0.01)
        P.dim("top_rail", 2.00, rails[-1], tol=0.01)
        P.notes.append("tiered rack (hasa-gi): three posts, three bamboo rails lashed on the front; wet-field regions")
    else:   # ab_collapsed: the rack blown down, stakes and rail in the stubble, sheaves in heaps
        P.bury = 0.02
        r = random.Random(81)
        for x, a in ((-1.6, 8.0), (0.1, -12.0), (1.5, 20.0)):
            s = pole((0.0, 0.035, -0.8), (0.0, 0.035, 0.8), 0.035, WOOD, n=5, vis=(1, 2), wear="_w2")
            P.add(xf(s, ry=a, t=(x, 0.0, 0.2)))
            P.add(col_solid(xf(beam((0.0, 0.035, -0.8), (0.0, 0.035, 0.8), 0.06, 0.06, WOOD), ry=a, t=(x, 0.0, 0.2))))
        P.add(pole((-1.9, 0.09, -0.35), (1.9, 0.09, -0.15), 0.022, BAMBOO, n=5, vis=(1, 2), wear="_w2"))
        for k in range(9):
            s = FK.standing_sheaf((0.0, 0.0, 0.0), (0.0, r.uniform(0.55, 0.65), 0.0), r, wear="_w2")
            add_all(P, rest(xfs(s, rx=90.0 + r.uniform(-15, 15), ry=r.uniform(-60, 60),
                                t=(r.uniform(-1.7, 1.7), 0.0, r.uniform(-0.2, 0.9))), 0.0))
        P.add(K.mound(82, 0.4, 0.5, 0.6, 0.25, STACK, sx=1.6, wear="_w2", vis=(1, 2)))
        P.add(K.mound(83, -1.0, 0.1, 0.5, 0.2, STACK, sx=1.3, wear="_w2", vis=(1, 2)))
        P.add(litter(84, 0.0, 0.3, 1.6, sx=1.6))
        P.add(box(-1.9, 1.9, 0.0, 0.2, -0.3, 0.9, STACK, vis=(3,)))
        P.solids[-1].wear = "_w2"
        ground(P)
        P.dim("span", 3.64, 3.8, tol=0.3)
    return P


PROPS.append({"id": "jp_s_hasa", "cat": CAT, "ll": "#51", "mount": "field", "tiers": [1, 2],
              "refs": ["k34_straw_rice"],
              "notes": ["AUTUMN: rice drying racks, sheaves hung astride the rails (soft cover: View Geometry on the "
                        "sheaves, Geometry only on stakes, posts and rails)",
                        "place along field edges and in the threshing yard, rails roughly east-west"],
              "models": [
                  M("jp_s_hasa_low", "low", "intact", "Rice drying rack on crossed stakes, hung with sheaves",
                    lambda: hasa("low")),
                  M("jp_s_hasa_tiers", "tiers", "intact", "Tiered rice drying rack, three rails of sheaves",
                    lambda: hasa("tiers")),
                  M("jp_s_hasa_empty", "tiers", "intact", "Tiered rice drying rack, empty", lambda: hasa("empty")),
                  M("jp_s_hasa_ab_sagged", "low", "abandoned", "Rice drying rack, one stake pair leaning, rail sagged, "
                    "sheaves grey and fallen", lambda: hasa("ab_sagged")),
                  M("jp_s_hasa_ab_collapsed", "low", "abandoned", "Rice drying rack blown down, sheaves in heaps",
                    lambda: hasa("ab_collapsed")),
              ]})


# ================================================================================================ 52 persimmon curtain
EAVE_Y = 2.40         # eave / bracket underside assumed (move y to the real eave: sidecar hang_y)


def kaki_string(x, top, n, z, seed, gaps=(), wear=None, cut=0.0):
    """A straw cord with n dried persimmons tied in alternating pairs (4-sided fruit to keep the curtain light)."""
    r = random.Random(seed)
    L = 0.10 * n + 0.08 - cut
    out = [cord((x, top, z), (x, top - L, z), 0.005, ROPE, n=3)]
    for k in range(n):
        y = top - 0.09 - 0.10 * k
        if k in gaps or y < top - L:
            continue
        side = -1 if k % 2 else 1
        out.append(bipyramid((x + side * 0.036, y, z + r.uniform(-0.012, 0.012)), 0.033, 0.040, 0.030, KAKI, n=4,
                             phase=r.uniform(0, 1), wear=wear, top=0.034))
    return out


def brackets(xs, z=0.38, y=EAVE_Y, vis=(1, 2)):
    return [beam((x, y, 0.0), (x, y, z), 0.035, 0.035, DARK, vis=vis) for x in xs]


def kaki_curtain(kind):
    ab = kind.startswith("ab")
    P = SPart("kaki_curtain", budget="box", mass=4.0, anchor="wall", wall_gap=0.0, flat=True,
              wear="_w2" if ab else "_w1")
    P.hung = True
    ns = {"1ken": 6, "half": 3, "ab_fallen": 6}[kind]
    span = 0.26 * (ns - 1)
    Z, py = 0.34, EAVE_Y - 0.16
    add_all(P, brackets((-span / 2 - 0.10, span / 2 + 0.10)))
    wear = "_w2" if ab else None
    if not ab:
        P.add(pole((-span / 2 - 0.16, py, Z), (span / 2 + 0.16, py, Z), 0.015, BAMBOO, n=5, vis=(1, 2)))
        for sx in (-1, 1):
            P.add(cord((sx * (span / 2 + 0.10), EAVE_Y, Z), (sx * (span / 2 + 0.10), py + 0.015, Z), 0.005))
        for i in range(ns):
            x = -span / 2 + 0.26 * i
            add_all(P, kaki_string(x, py - 0.015, 9, Z, 520 + i, gaps=((3,) if i % 3 == 1 else ())))
            P.add(box(x - 0.045, x + 0.045, py - 1.0, py - 0.05, Z - 0.02, Z + 0.02, KAKI, vis=(2,)))
        P.dim("strings", ns, ns, tol=0)
        P.dim("drop", 1.0, 0.98, tol=0.05)
    else:
        # the right cord rotted: the pole hangs from the left bracket, its right end on the ground; strings snapped
        p0, p1 = (-span / 2 - 0.16, py, Z), (span / 2 + 0.1, 0.03, Z + 0.25)
        P.add(pole(p0, p1, 0.015, BAMBOO, n=5, vis=(1, 2), wear="_w2"))
        P.add(cord((-span / 2 - 0.10, EAVE_Y, Z), (-span / 2 - 0.10, py + 0.015, Z), 0.005))
        for i in range(2):
            t = 0.12 + 0.18 * i
            q = core.add(p0, core.mul(core.sub(p1, p0), t))
            add_all(P, kaki_string(q[0], q[1] - 0.015, 9, q[2], 530 + i, gaps=(2, 5, 6), wear="_w2",
                                   cut=0.0 if i else 0.3))
        r = random.Random(53)
        for k in range(24):                     # fallen fruit, dried black, in the leaf litter
            P.add(bipyramid((r.uniform(-0.8, 0.8), 0.028, r.uniform(0.2, 0.9)), 0.033, 0.028, 0.030, KAKI, n=4,
                            phase=r.uniform(0, 1), wear="_w2", top=0.028))
        for i in range(2):                      # two whole strings lying on the ground
            ly = xfs(kaki_string(0.0, 0.0, 8, 0.0, 540 + i, gaps=(1,), wear="_w2"), rx=-90.0)
            z0 = min(v[2] for q in ly for v in q.verts)
            add_all(P, xfs(ly, ry=25.0 * (i - 0.5), t=(-0.4 + 0.7 * i, 0.03, 0.25 - z0)))
        P.add(litter(55, 0.0, 0.62, 0.55, sx=1.6))
        P.add(box(-0.8, 0.8, 0.0, 0.05, 0.2, 0.9, KAKI, vis=(2,)))
        P.solids[-1].wear = "_w2"
        P.dim("strings", 6, 6, tol=0)
    P.extra["hang_y"] = EAVE_Y
    P.extra["proxy"] = "eaves piece: facade z = 0, y = 0 at the wall foot, brackets at hang_y (move y to the real eave)"
    return P


PROPS.append({"id": "jp_s_kaki_curtain", "cat": CAT, "ll": "#52", "mount": "eaves", "tiers": [1, 2],
              "refs": ["k35_firewood_hoshigaki"],
              "notes": ["AUTUMN: persimmon curtain (kaki-sudare) under the eaves: the outdoor version of L1's #8",
                        "visual only; brackets touch the facade at hang_y"],
              "models": [
                  M("jp_s_kaki_curtain_1ken", "1ken", "intact", "Persimmon curtain under the eaves, six strings",
                    lambda: kaki_curtain("1ken")),
                  M("jp_s_kaki_curtain_half", "half", "intact", "Persimmon curtain, three strings",
                    lambda: kaki_curtain("half")),
                  M("jp_s_kaki_curtain_ab_fallen", "1ken", "abandoned", "Persimmon curtain fallen, fruit black on the "
                    "ground", lambda: kaki_curtain("ab_fallen")),
              ]})


# ================================================================================================ 53 moon-viewing stand
def dango(c, r=0.021, wear="_w1"):
    s = lathe([(0.0, -r), (r * 0.8, -r * 0.6), (r, 0.0), (r * 0.8, r * 0.6), (0.0, r)], 5, RICE, vis=(1,), wear=wear,
              smooth=True)
    return xf(s, t=c)


def sanbo(wear=None):
    """Offering stand: a plain hinoki tray on a pierced base (0.27 square tray, 0.20 high)."""
    out = [W(-0.10, 0.10, 0.0, 0.14, -0.10, 0.10, WOOD, vis=(1, 2)),
           W(-0.135, 0.135, 0.14, 0.155, -0.135, 0.135, WOOD, vis=(1, 2))]
    for sx in (-1, 1):
        out.append(W(sx * 0.135 - 0.008 * (sx > 0), sx * 0.135 + 0.008 * (sx < 0), 0.155, 0.19, -0.135, 0.135, WOOD,
                     vis=(1,)))
        out.append(W(-0.127, 0.127, 0.155, 0.19, sx * 0.135 - 0.008 * (sx > 0), sx * 0.135 + 0.008 * (sx < 0), WOOD,
                     vis=(1,)))
    return K.wear_all(out, wear)


def dango_pile(y, wear="_w1", missing=(), r=0.021):
    out = []
    k = 0
    for tier, n in enumerate((3, 2, 1)):
        off = (n - 1) * r
        for i in range(n):
            for j in range(n):
                if k not in missing:
                    out.append(dango((-off + 2 * r * i, y + r + tier * r * 1.45, -off + 2 * r * j), r, wear))
                k += 1
    return out


def susuki(c, wear="_w1", snapped=(), n=5, seed=1):
    """Pampas grass stems in a stoneware jar at c: jar + arching stems with plumes."""
    r = random.Random(seed)
    out = [lathe([(0.06, 0.0), (0.085, 0.08), (0.075, 0.20), (0.045, 0.26), (0.05, 0.28), (0.04, 0.28),
                  (0.035, 0.25), (0.0, 0.25)], 8, DARKC, vis=(1,))]
    out.append(lathe([(0.06, 0.0), (0.085, 0.10), (0.05, 0.28), (0.0, 0.28)], 5, DARKC, vis=(2,), smooth=False))
    for k in range(n):
        a = 2 * math.pi * k / n + r.uniform(-0.3, 0.3)
        lean = r.uniform(0.10, 0.22)
        L = r.uniform(0.62, 0.85)
        p0 = (0.0, 0.25, 0.0)
        p1 = (lean * math.cos(a) * 0.5, 0.25 + L * 0.6, lean * math.sin(a) * 0.5)
        if k in snapped:
            p2 = (lean * math.cos(a) * 1.6, 0.25 + L * 0.35, lean * math.sin(a) * 1.6)
        else:
            p2 = (lean * math.cos(a), 0.25 + L, lean * math.sin(a))
        out += rope_path([p0, p1, p2], 0.004, STACK, n=3, wear=wear)
        d = core.norm(core.sub(p2, p1))
        tip = core.add(p2, core.mul(d, 0.17))
        mid = core.add(p2, core.mul(d, 0.085))
        pl = bipyramid(mid, 0.022, 0.09, 0.022, PLAIN, n=4, wear=wear)
        ux, uy, uz = K.skit.basis(d)
        pl = K.frame(xf(pl, t=core.mul(mid, -1.0)), mid, ux, uy, uz)
        out.append(pl)
    return [xf(s, t=c) for s in out]


def tsukimi(kind):
    ab = kind.startswith("ab")
    P = SPart("tsukimi", budget="box", mass=2.0, flat=True, wear="_w2" if ab else "_w1")
    if kind == "stand":
        add_all(P, sanbo())
        P.add(K.quad_sheet([(-0.12, 0.158, -0.12), (0.12, 0.158, -0.12), (0.12, 0.158, 0.12), (-0.12, 0.158, 0.12)],
                           PAPER, (0.0, 1.0, 0.0)))
        add_all(P, dango_pile(0.158))
        add_all(P, susuki((0.30, 0.0, -0.05), seed=3))
        for x, z in ((-0.26, 0.10), (-0.20, 0.17)):
            P.add(bipyramid((x, 0.03, z), 0.035, 0.03, 0.035, KAKI, n=5, top=0.028))
    elif kind == "ab_dried":
        add_all(P, sanbo(wear="_w2"))
        P.add(K.quad_sheet([(-0.12, 0.158, -0.12), (0.12, 0.158, -0.12), (0.12, 0.158, 0.12), (-0.12, 0.158, 0.12)],
                           PAPER, (0.0, 1.0, 0.0), wear="_w2"))
        add_all(P, dango_pile(0.158, wear="_w2", missing=(0, 2, 5, 8, 11, 13)))
        add_all(P, susuki((0.30, 0.0, -0.05), wear="_w2", snapped=(1, 3), seed=3))
        P.add(litter(56, 0.1, 0.1, 0.35))
    else:   # ab_tipped: the stand knocked over, dango scattered, the jar on its side
        st = xfs(sanbo(wear="_w2"), rx=90.0, t=(0.0, 0.135, -0.1))
        add_all(P, st)
        r = random.Random(57)
        for k in range(8):
            P.add(dango((r.uniform(-0.3, 0.3), 0.021, r.uniform(0.1, 0.45)), wear="_w2"))
        jar = susuki((0.0, 0.0, 0.0), wear="_w2", snapped=(0, 2, 4), seed=4)
        add_all(P, xfs(jar, rz=-88.0, t=(0.35, 0.085, 0.15)))
        P.add(litter(58, 0.0, 0.2, 0.45))
        ground(P)
    lo = [s for s in P.solids if 1 in s.vis]
    if kind != "stand":
        pass
    P.add(W(-0.14, 0.14, 0.0, 0.25, -0.14, 0.14, WOOD, vis=(2,)))
    P.dim("stand_h", 0.19, 0.19, tol=0.02)
    P.dim("dango", 14 if kind == "stand" else 8, sum(1 for s in P.solids if s.mats == RICE), tol=0)
    return P


PROPS.append({"id": "jp_s_tsukimi", "cat": CAT, "ll": "#53", "mount": "eaves", "tiers": [2, 3],
              "notes": ["AUTUMN: the jugoya moon offering on a veranda edge: plain offering stand, 14 white dango, "
                        "pampas grass in a stoneware jar, two persimmons (era: LIFE_LAYER_ERA.md #53)",
                        "visual only; stands on the veranda boards (base centre on the boards)"],
              "models": [
                  M("jp_s_tsukimi_stand", "stand", "intact", "Moon-viewing offering: dango on a stand, pampas grass",
                    lambda: tsukimi("stand")),
                  M("jp_s_tsukimi_ab_dried", "stand", "abandoned", "Moon-viewing offering, dango mouldy and pecked, "
                    "grass snapped", lambda: tsukimi("ab_dried")),
                  M("jp_s_tsukimi_ab_tipped", "stand", "abandoned", "Moon-viewing stand knocked over, dango scattered",
                    lambda: tsukimi("ab_tipped")),
              ]})


# ================================================================================================ 62 scarecrow
def scarecrow_figure(wear=None, hat=True):
    """Kakashi: a pole with a crossbar, a straw-bundle body, a straw cape (mino), a cloth-wrapped head, a sedge hat,
    rag sleeves on the arms. Built standing; the pole's foot at y = -0.35 (buried)."""
    out = [pole((0.0, -0.35, 0.0), (0.0, 1.58, 0.0), 0.03, WOOD, n=5, vis=(1, 2), wear=wear),
           pole((-0.60, 1.25, 0.0), (0.60, 1.25, 0.0), 0.022, BAMBOO, n=5, vis=(1, 2), wear=wear),
           lathe([(0.10, 0.55), (0.15, 0.75), (0.16, 1.05), (0.13, 1.30), (0.05, 1.34), (0.0, 1.34)], 7, STACK,
                 vis=(1,), wear=wear),
           lathe([(0.0, 1.35), (0.09, 1.38), (0.11, 1.48), (0.09, 1.58), (0.0, 1.62)], 7, PLAIN, vis=(1,),
                 wear=wear or "_w1")]

    def skirt(u, v):
        a = 2 * math.pi * u
        rr = 0.13 + 0.26 * v
        return (rr * math.cos(a), 1.31 - 0.62 * v, rr * math.sin(a) * 0.85)
    out.append(grid_sheet(skirt, 8, 2, MUSHIRO, vis=(1,), wear=wear or "_w1"))
    for sx in (-1, 1):                       # rag sleeves hanging from the crossbar
        def slv(u, v, sx=sx):
            return (sx * (0.18 + 0.34 * u), 1.25 - 0.38 * v * (0.6 + 0.4 * u), 0.03 * math.sin(math.pi * u) * v)
        out.append(grid_sheet(slv, 2, 1, INDIGO, vis=(1,), wear="_w2"))
    if hat:
        out += LW.kasa(0.0, 1.58, 0.0, R=0.24, H=0.13, rx=0.0, wear=wear or "_w1", n=10)
    out.append(lathe([(0.12, 0.55), (0.30, 0.70), (0.14, 1.30), (0.0, 1.34)], 5, STACK, vis=(2,), wear=wear,
                     smooth=False))
    out.append(W(-0.6, 0.6, 1.22, 1.28, -0.02, 0.02, BAMBOO, vis=(2,)))
    out.append(W(-0.15, 0.15, -0.35, 1.6, -0.12, 0.12, STACK, vis=(3,)))
    out.append(W(-0.6, 0.6, 1.2, 1.3, -0.03, 0.03, BAMBOO, vis=(3,)))
    cols = [cyl_col(0.16, 0.55, 1.34, n=8), col(-0.035, 0.035, -0.35, 0.55, -0.035, 0.035)]
    return out, cols


def naruko_board(c, wear=None):
    """A bird clapper: a small board with three bamboo tubes hung on cords below it."""
    out = [W(-0.13, 0.13, -0.18, 0.0, -0.01, 0.01, WOOD, vis=(1,))]
    for k in range(3):
        x = -0.08 + 0.08 * k
        out.append(cord((x, -0.18, 0.0), (x, -0.22, 0.0), 0.003))
        out.append(lathe([(0.018, -0.36), (0.018, -0.22), (0.0, -0.22)], 5, BAMBOO, vis=(1,)))
        out[-1] = xf(out[-1], t=(x, 0.0, 0.02))
    return K.wear_all([xf(s, t=c) for s in out], wear)


def scarecrow(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("scarecrow", budget="box", res3=True, mass=12.0, bury=0.35, wear=wear or "_w1")
    if kind == "kasa":
        ss, cs = scarecrow_figure()
        add_all(P, ss + cs)
        P.dim("height", 1.75, 1.58 + 0.13, tol=0.1)
    elif kind == "naruko":
        P.budget = "box"
        for x in (-2.0, 2.0):
            P.add(pole((x, -0.35, 0.0), (x, 1.30, 0.0), 0.03, WOOD, n=5, vis=(1, 2)))
            P.add(col(x - 0.03, x + 0.03, -0.35, 1.30, -0.03, 0.03))
        pts = sag((-2.0, 1.22, 0.0), (2.0, 1.22, 0.0), 0.14, k=8)
        add_all(P, rope_path(pts, 0.005, ROPE, n=3))
        for k, t in enumerate((0.2, 0.4, 0.6, 0.8)):
            i = int(t * 8)
            q = pts[i]
            add_all(P, naruko_board((q[0], q[1] - 0.005, 0.0), wear="_w1"))
        P.add(W(-2.0, 2.0, 1.0, 1.2, -0.01, 0.01, WOOD, vis=(2,)))
        for x in (-2.0, 2.0):
            P.add(W(x - 0.03, x + 0.03, -0.35, 1.3, -0.03, 0.03, WOOD, vis=(3,)))
        P.dim("span", 4.0, 4.0, tol=0.01)
        P.notes.append("naruko bird clappers on a rope between two stakes (crop watch, BUILDING_LIST 306-307)")
    elif kind == "ab_leaning":
        ss, cs = scarecrow_figure(wear="_w2", hat=False)
        add_all(P, xfs(ss, rz=24.0) + xfs(cs, rz=24.0))
        add_all(P, LW.kasa(0.55, 0.0, 0.45, R=0.24, H=0.13, rx=0.0, rz=160.0, wear="_w2", n=10))
        P.solids[-2] = xf(P.solids[-2], t=(0.0, 0.13, 0.0))
        P.solids[-1] = xf(P.solids[-1], t=(0.0, 0.13, 0.0))
        P.add(litter(62, 0.3, 0.3, 0.7))
        P.dim("lean_deg", 24.0, 24.0, tol=0)
    else:   # ab_down: the pole rotted through at the ground, the figure face down in the stubble
        P.bury = 0.02
        ss, cs = scarecrow_figure(wear="_w2", hat=False)
        ss = [s for s in ss if not (s.mats == WOOD and s.bbox()[2] < -0.3)]
        ss.append(pole((0.0, 0.0, 0.0), (0.0, 1.58, 0.0), 0.03, WOOD, n=5, vis=(1, 2), wear="_w2"))
        cs = [cyl_col(0.16, 0.55, 1.34, n=8), col(-0.035, 0.035, 0.0, 0.55, -0.035, 0.035)]
        vs, cs = K.lkit.place_group(ss, cs, [dict(rx=-86.0)])
        add_all(P, vs + cs)
        add_all(P, LW.kasa(0.7, 0.0, -0.6, R=0.24, H=0.13, rx=180.0, wear="_w2", n=10))
        P.solids[-2] = xf(P.solids[-2], t=(0.0, 0.13, 0.0))
        P.solids[-1] = xf(P.solids[-1], t=(0.0, 0.13, 0.0))
        P.add(litter(63, 0.0, -0.8, 0.9, sx=1.5))
        ground(P)
        P.dim("length", 1.93, 1.62, tol=0.35)
    return P


PROPS.append({"id": "jp_s_scarecrow", "cat": CAT, "ll": "#62", "mount": "field", "tiers": [1],
              "notes": ["AUTUMN fields: straw kakashi in a sedge hat and mino, and naruko clappers on a rope; no painted "
                        "face (era: LIFE_LAYER_ERA.md #62)"],
              "models": [
                  M("jp_s_scarecrow_kasa", "kasa", "intact", "Scarecrow in a sedge hat and straw cape",
                    lambda: scarecrow("kasa")),
                  M("jp_s_scarecrow_naruko", "naruko", "intact", "Bird clappers on a rope between stakes",
                    lambda: scarecrow("naruko")),
                  M("jp_s_scarecrow_ab_leaning", "kasa", "abandoned", "Scarecrow leaning, hat blown off",
                    lambda: scarecrow("ab_leaning")),
                  M("jp_s_scarecrow_ab_down", "kasa", "abandoned", "Scarecrow fallen face down in the stubble",
                    lambda: scarecrow("ab_down")),
              ]})


# ================================================================================================ helpers: leaning
def lean_to_wall(ss, L, theta, x=0.0, top_z=0.012, cols=()):
    """Tools built standing on the origin along +y (length L) leaned back against the wall plane z = 0: the top
    touches at top_z, the foot rests on the ground. Returns (visual, collision) solids, both lifted so the lowest
    visual point is y = 0."""
    a = math.radians(theta)
    d = top_z + L * math.sin(a)
    vs = xfs(ss, rx=-theta, t=(x, 0.0, d))
    cs = xfs(list(cols), rx=-theta, t=(x, 0.0, d))
    lo = min(v[1] for s in vs for v in s.verts)
    vs = xfs(vs, t=(0.0, -lo, 0.0))
    cs = xfs(cs, t=(0.0, -lo, 0.0))
    return vs, cs


# ================================================================================================ 54 farm tools
def hoe(wear=None):
    """Hira-guwa: a 1.15 m oak handle, the iron blade set at an angle at its foot, a wooden head block."""
    out = [pole((0.0, 0.0, 0.0), (0.0, 1.15, 0.0), 0.017, WOOD, n=5, vis=(1, 2)),
           box(-0.03, 0.03, 0.0, 0.07, -0.03, 0.03, WOOD, vis=(1,))]
    bl = box(-0.075, 0.075, 0.0, 0.004, 0.0, 0.22, IRON, vis=(1,))
    out.append(xf(bl, rx=-20.0, t=(0.0, 0.02, 0.02)))
    return K.wear_all(out, wear)


def rake(wear=None):
    """Kumade: bamboo rake, a 1.35 m bamboo handle and a fan of split-bamboo tines (one flat fan)."""
    out = [pole((0.0, 0.0, 0.0), (0.0, 1.35, 0.0), 0.016, BAMBOO, n=5, vis=(1, 2))]
    fan = [(0.0, 1.20)] + [(0.28 * math.sin(math.radians(a)), 1.20 + 0.40 * math.cos(math.radians(a)))
                           for a in range(-40, 41, 20)]
    out.append(prism(fan, "z", -0.006, 0.006, BAMBOO, vis=(1,)))
    return K.wear_all(out, wear)


def flail(wear=None):
    """Kururi-bo: a 1.7 m pole with a swinging bar of three bamboo slats on a peg at its top."""
    out = [pole((0.0, 0.0, 0.0), (0.0, 1.70, 0.0), 0.018, BAMBOO, n=5, vis=(1, 2))]
    for k in range(3):
        out.append(box(-0.045 + 0.03 * k, -0.02 + 0.03 * k, 1.05, 1.68, 0.02, 0.032, BAMBOO, vis=(1,)))
    out.append(box(-0.05, 0.05, 1.64, 1.69, 0.015, 0.035, WOOD, vis=(1,)))
    return K.wear_all(out, wear)


def sickle(wear=None):
    """Kama: 0.30 handle, a curved iron blade (flat prism), hung by its handle from a nail."""
    out = [box(-0.014, 0.014, -0.30, 0.0, -0.01, 0.01, WOOD, vis=(1,))]
    bl = [(0.0, -0.30), (0.03, -0.30), (0.19, -0.26), (0.24, -0.20)]
    out.append(prism(bl, "z", -0.002, 0.002, IRON, vis=(1,)))
    return K.wear_all(out, wear)


def farm_tools(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("farm_tools", budget="small", mass=6.0, anchor="wall", wall_gap=0.0, flat=True,
              wear="_w2" if ab else "_w1")
    P.add(K.lkit.peg(0.55, 1.30))                       # the nail the sickle hangs from
    if kind in ("lean", "pair"):
        tools = [(hoe, 1.15, 12.0, -0.45), (rake, 1.60, 14.0, 0.05)]
        if kind == "lean":
            tools.append((flail, 1.70, 10.0, 0.35))
        for fn, L, th, x in tools:
            vs, _ = lean_to_wall(fn(wear), L, th, x=x, top_z=0.035)
            add_all(P, vs)
        if kind == "lean":
            add_all(P, xfs(sickle(), t=(0.55, 1.32, 0.05)))
        P.add(W(-0.6, 0.45, 0.0, 1.5, 0.02, 0.10, WOOD, vis=(2,)))
        P.dim("tools", 4 if kind == "lean" else 2, len(tools) + (1 if kind == "lean" else 0), tol=0)
    else:   # ab_fallen: slid down the wall into the leaves, the sickle on the ground, iron rusted
        r = random.Random(54)
        for fn, L, x, a in ((hoe, 1.15, -0.4, 80.0), (rake, 1.60, 0.1, 70.0), (flail, 1.70, 0.5, 95.0)):
            ss = xfs(fn("_w2"), rx=90.0)
            ss = rest(xfs(ss, ry=a + r.uniform(-8, 8), t=(x, 0.0, 0.55)), 0.0)
            z0 = min(v[2] for q in ss for v in q.verts)
            add_all(P, xfs(ss, t=(0.0, 0.0, max(0.0, 0.08 - z0))))
        add_all(P, rest(xfs(sickle("_w2"), rx=90.0, ry=30.0, t=(0.6, 0.0, 0.3)), 0.0))
        P.add(litter(541, 0.0, 0.85, 0.6, sx=1.6))
        P.add(W(-0.9, 0.9, 0.0, 0.06, 0.1, 1.2, WOOD, vis=(2,)))
        P.dim("tools", 4, 4, tol=0)
    P.notes.append("farm tools against a yard wall: hoe (kuwa), bamboo rake (kumade), flail (kururi-bo), sickle on "
                   "a nail; no threshing comb (a floor machine). Visual only.")
    return P


PROPS.append({"id": "jp_s_farm_tools", "cat": CAT, "ll": "#54", "mount": "yard", "tiers": [1, 2],
              "models": [
                  M("jp_s_farm_tools_lean", "lean", "intact", "Farm tools leaned on a wall: hoe, rake, flail, sickle",
                    lambda: farm_tools("lean")),
                  M("jp_s_farm_tools_pair", "pair", "intact", "Hoe and rake leaned on a wall", lambda: farm_tools("pair")),
                  M("jp_s_farm_tools_ab_fallen", "lean", "abandoned", "Farm tools slid down into the leaves, rusted",
                    lambda: farm_tools("ab_fallen")),
              ]})


# ================================================================================================ 55 broom + leaf pile
def broom(wear=None, seed=1):
    """Take-boki (FP1 remake, 2026-10-01, Stephen: the broom 'looks like shit' - it was a flat plank fan): a 1.45 m
    bamboo handle with nodes, a bundle of bamboo branchlets bound twice round its foot, the twigs (each with a side
    branchlet) fanning flat to ~0.46 m; lying along +z, handle butt at z -0.75 (spikes/B3b/fp1kit.take_boki)."""
    ss = FK.lying_boki(seed=seed, wear=wear)
    zmin = min(v[2] for s in ss for v in s.verts)
    out = xfs(ss, t=(0.0, 0.0, -0.75 - zmin))
    out.append(pole((0.0, 0.03, -0.75), (0.0, 0.03, 0.70), 0.014, BAMBOO, n=4, vis=(2,)))        # LOD 2: handle
    out.append(prism([(-0.05, 0.70), (0.05, 0.70), (0.23, 1.0), (-0.23, 1.0)], "y", 0.0, 0.04, BAMBOO, vis=(2,)))
    return K.wear_all(out, wear)


def leaf_pile(kind):
    ab = kind.startswith("ab")
    # FP1: with the remade broom (~230 faces) the pile + broom models are box class (<= 600)
    P = SPart("leaf_pile", budget="small" if kind == "small" else "box", mass=1.0, flat=True, wear="_w2" if ab else "_w1")
    if kind in ("broom", "small"):
        P.add(K.mound(551, 0.0, 0.0, 0.45, 0.16, LEAF, sx=1.3, wear="_w1", vis=(1, 2)))
        P.add(K.mound(552, 0.28, -0.1, 0.28, 0.10, LEAF, sx=1.1, wear="_w2", vis=(1,)))
        P.add(litter(553, 0.1, 0.0, 0.9, sx=1.4))
        if kind == "broom":
            add_all(P, xfs(broom(), ry=-65.0, t=(-0.2, 0.0, 0.75)))
        P.dim("pile_h", 0.16, 0.16, tol=0.01)
    else:   # ab_scattered: the wind has spread the pile, the broom lies where it fell
        for k, (x, z, rr) in enumerate(((0.0, 0.0, 0.32), (0.55, 0.25, 0.22), (-0.45, 0.35, 0.18))):
            P.add(K.mound(554 + 10 * k, x, z, rr, 0.05 - 0.01 * k, LEAF, sx=1.4, wear="_w2", vis=(1, 2) if k == 0 else (1,)))
        for k, (x, z, rr) in enumerate(((1.1, 0.4, 0.6), (-1.0, -0.3, 0.7), (0.2, 0.9, 0.5))):
            P.add(litter(555 + k, x, z, rr, sx=1.3))
        add_all(P, xfs(broom("_w2"), ry=150.0, t=(0.9, 0.0, -0.8)))
        P.dim("pile_h", 0.05, 0.05, tol=0.01)
    P.notes.append("autumn: a raked leaf pile and the bamboo broom (take-boki); visual only, walk-through")
    return P


PROPS.append({"id": "jp_s_leaf_pile", "cat": CAT, "ll": "#55", "mount": "yard", "tiers": [1, 2, 3],
              "models": [
                  M("jp_s_leaf_pile_broom", "broom", "intact", "Raked leaf pile with a bamboo broom",
                    lambda: leaf_pile("broom")),
                  M("jp_s_leaf_pile_small", "small", "intact", "Raked leaf pile", lambda: leaf_pile("small"),
                    mount="street"),
                  M("jp_s_leaf_pile_ab_scattered", "broom", "abandoned", "Leaf pile spread by the wind, broom fallen",
                    lambda: leaf_pile("ab_scattered")),
              ]})


# ================================================================================================ 56 ladder
def ladder_parts(L, bamboo=False, missing=(), wear=None):
    rail = BAMBOO if bamboo else WOOD
    out = []
    for sx in (-1, 1):
        x = sx * 0.21
        if bamboo:
            out.append(pole((x, 0.0, 0.0), (x, L, 0.0), 0.028, BAMBOO, n=6, vis=(1, 2), r1=0.022))
        else:
            out.append(W(x - 0.03, x + 0.03, 0.0, L, -0.02, 0.02, WOOD, vis=(1, 2)))
    n = int(L / 0.30)
    for k in range(1, n + 1):
        if k in missing:
            continue
        y = 0.30 * k - 0.05
        out.append(pole((-0.21, y, 0.0), (0.21, y, 0.0), 0.016, rail, n=4 if bamboo else 5, vis=(1,)))
        if bamboo:
            for sx in (-1, 1):
                out.append(box(sx * 0.21 - 0.035, sx * 0.21 + 0.035, y - 0.02, y + 0.02, -0.035, 0.035, ROPE, vis=(1,)))
    for k in range(1, n + 1, 3):
        y = 0.30 * k - 0.05
        out.append(W(-0.2, 0.2, y - 0.015, y + 0.015, -0.015, 0.015, rail, vis=(2,)))
    cols = [col(-0.25, 0.25, 0.0, L, -0.03, 0.03, rail)]
    return K.wear_all(out, wear), cols, n


def ladder(kind):
    ab = kind.startswith("ab")
    P = SPart("ladder", budget="small", mass=12.0, anchor="wall" if not ab else "floor", wall_gap=0.0,
              wear="_w2" if ab else "_w1")
    if kind in ("lean", "bamboo"):
        L = 3.0 if kind == "lean" else 3.6
        ss, cs, n = ladder_parts(L, bamboo=kind == "bamboo")
        th = 15.0
        vs, cs = lean_to_wall(ss, L, th, top_z=0.012 + (0.028 if kind == "bamboo" else 0.02), cols=cs)
        add_all(P, vs + cs)
        P.dim("length", L, L, tol=0.01)
        P.dim("top_h", L * math.cos(math.radians(th)), max(v[1] for s in vs for v in s.verts), tol=0.08)
        P.notes.append("leaned against the eaves at 15 degrees (top %.2f m): place with the wall plane on the facade"
                       % (L * math.cos(math.radians(th))))
    else:   # ab_fallen: down on the ground, two rungs gone, one rail split
        ss, cs, n = ladder_parts(3.0, missing=(4, 7), wear="_w2")
        ss = xfs(ss, rx=90.0, ry=12.0, t=(0.0, 0.03, -1.4))
        cs = xfs(cs, rx=90.0, ry=12.0, t=(0.0, 0.03, -1.4))
        add_all(P, ss + cs)
        for k, a in ((4, 40.0), (7, -25.0)):
            b = pole((-0.2, 0.0, 0.0), (0.2, 0.0, 0.0), 0.016, WOOD, n=5, vis=(1,), wear="_w2")
            P.add(xf(b, ry=a, t=(0.45 + 0.1 * k / 4, 0.016, -1.4 + 0.30 * k)))
        P.add(litter(561, 0.1, 0.0, 1.0, sx=0.6, sz=1.6))
        ground(P)
        P.dim("length", 3.0, 3.0, tol=0.01)
    return P


PROPS.append({"id": "jp_s_ladder", "cat": CAT, "ll": "#56", "mount": "yard", "tiers": [1, 2, 3],
              "notes": ["a ladder against the eaves (roof and fire access); Geometry: one slab (not climbable)"],
              "models": [
                  M("jp_s_ladder_lean", "wood", "intact", "Wooden ladder leaned against the eaves",
                    lambda: ladder("lean")),
                  M("jp_s_ladder_bamboo", "bamboo", "intact", "Bamboo ladder leaned against the eaves",
                    lambda: ladder("bamboo"), mount="street"),
                  M("jp_s_ladder_ab_fallen", "wood", "abandoned", "Ladder fallen on the ground, rungs broken",
                    lambda: ladder("ab_fallen")),
              ]})


# ================================================================================================ 57 charcoal bales
import props_life_meal as LM      # noqa: E402  L1 (read-only): sumi_bale(), charcoal_bits()


def charcoal_bales(kind):
    ab = kind.startswith("ab")
    P = SPart("charcoal_bales", budget="box", mass=60.0, anchor="wall", wall_gap=0.05, wear="_w2" if ab else "_w1")
    R, h = 0.17, 0.62
    zc = 0.05 + R + 0.01
    wear = "_w2" if ab else None
    if kind == "stack":
        for x in (-0.36, 0.0, 0.36):
            add_all(P, LM.sumi_bale(x, zc, R=R, h=h, open_top=False, wear=wear))
            P.add(cyl_col(R, 0.0, h, n=8, cx=x, cz=zc))
        top = LM.sumi_bale(0.0, 0.0, R=R, h=h, open_top=False, wear=wear)
        top = xfs(top, t=(0.0, -h / 2, 0.0))
        top = xfs(top, rz=90.0, t=(-0.1, h + R + 0.005, zc))
        add_all(P, top)
        P.add(xf(cyl_col(R, -h / 2, h / 2, n=8), rz=90.0, t=(-0.1, h + R + 0.005, zc)))
        P.dim("bales", 4, 4, tol=0)
    elif kind == "row2":
        for x in (-0.19, 0.19):
            add_all(P, LM.sumi_bale(x, zc, R=R, h=h, open_top=(x > 0), wear=wear))
            P.add(cyl_col(R, 0.0, h, n=8, cx=x, cz=zc))
        P.dim("bales", 2, 2, tol=0)
    else:   # ab_burst: one bale fallen and burst, charcoal spilled
        add_all(P, LM.sumi_bale(-0.25, zc, R=R, h=h, open_top=True, wear="_w2"))
        P.add(cyl_col(R, 0.0, h, n=8, cx=-0.25, cz=zc))
        fb = LM.sumi_bale(0.0, 0.0, R=R, h=h, open_top=False, wear="_w2")
        fb = xfs(fb, t=(0.0, -h / 2, 0.0))
        fb = xfs(fb, rx=90.0, ry=-35.0, t=(0.35, R, 0.55))
        add_all(P, fb)
        P.add(xf(xf(cyl_col(R, -h / 2, h / 2, n=8), rx=90.0), ry=-35.0, t=(0.35, R, 0.55)))
        add_all(P, LM.charcoal_bits(0.55, 0.95, 0.0, 0.28, 16, 571))
        P.add(K.mound(572, 0.5, 0.9, 0.25, 0.04, SOOTW, sx=1.4, wear="_w2", vis=(1,)))
        P.add(litter(573, 0.3, 0.7, 0.6))
        P.dim("bales", 2, 2, tol=0)
    P.notes.append("charcoal bales (sumi-dawara) stacked by a door, 5 cm off the wall (BUILDING_LIST 5.2: 25 entries)")
    return P


PROPS.append({"id": "jp_s_charcoal_bales", "cat": CAT, "ll": "#57", "mount": "yard", "tiers": [1, 2, 3],
              "models": [
                  M("jp_s_charcoal_bales_stack", "stack", "intact", "Charcoal bales stacked by a door",
                    lambda: charcoal_bales("stack")),
                  M("jp_s_charcoal_bales_row2", "row2", "intact", "Two charcoal bales against a wall",
                    lambda: charcoal_bales("row2")),
                  M("jp_s_charcoal_bales_ab_burst", "stack", "abandoned", "Charcoal bale fallen and burst, charcoal "
                    "spilled", lambda: charcoal_bales("ab_burst")),
              ]})


# ================================================================================================ 58 potted plants
def pot(c, r=0.10, h=0.16, mat=DARKC, soil=True, wear=None, dead_soil=False):
    """An unglazed-looking stoneware pot, flared, soil (or leaf-litter crust) 3 cm below the rim."""
    out = [lathe([(r * 0.7, 0.0), (r, h), (r + 0.006, h), (r - 0.008, h), (r * 0.95 - 0.008, h - 0.03), (0.0, h - 0.03)],
                 8, mat, vis=(1,), wear=wear)]
    out.append(lathe([(r * 0.7, 0.0), (r, h), (0.0, h)], 5, mat, vis=(2,), smooth=False, wear=wear))
    if soil:
        out.append(disc(r * 0.93 - 0.008, h - 0.03, h - 0.028, LEAF if dead_soil else EARTH, n=7, vis=(1,),
                        wear="_w2" if dead_soil else "_w1"))
    return [xf(s, t=c) for s in out]


def pine(c, wear=None, seed=1):
    """A small potted pine: an S-bent trunk and three needle pads."""
    r = random.Random(seed)
    x, y, z = c
    pts = [(x, y, z), (x + 0.05, y + 0.12, z), (x - 0.03, y + 0.24, z + 0.02), (x + 0.04, y + 0.34, z)]
    out = rope_path(pts, 0.018, DARK, n=5, vis=(1,))
    for k, (dx, dy) in enumerate(((0.10, 0.14), (-0.10, 0.25), (0.02, 0.36))):
        out += K.bush((x + dx, y + dy, z + r.uniform(-0.03, 0.03)), 0.10 - 0.015 * k, 0.07, kind="needle", wear=wear,
                      n=2, seed=seed + k)
    return out


def kiku(c, wear=None, flowers=True, seed=1):
    """Chrysanthemums: stems, a leafy clump, cream flower heads (kinari cotton discs) when in bloom."""
    r = random.Random(seed)
    x, y, z = c
    out = K.bush((x, y, z), 0.11, 0.24, kind="leaf", wear=wear, n=3, seed=seed)
    for k in range(4):
        a = 2 * math.pi * k / 4 + r.uniform(-0.4, 0.4)
        top = (x + 0.06 * math.cos(a), y + 0.34 + r.uniform(-0.04, 0.04), z + 0.06 * math.sin(a))
        out.append(pole((x, y, z), top, 0.004, "bamboo_weathered", n=3, vis=(1,), wear="_w2" if wear == "_w2" else None))
        if flowers:
            out.append(xf(lathe([(0.0, 0.0), (0.035, 0.008), (0.03, 0.02), (0.0, 0.025)], 6, PLAIN, vis=(1,)),
                          t=top))
    return out


def potted(kind):
    """FP1 remake (2026-10-01, Stephen: 'redo completely'): unglazed earthenware pots with a rolled rim and foot, a
    potted pine with an S-curved tapering trunk, surface roots, alternate branches and needle pads, a satsuki azalea
    (leaf mound on three stems), chrysanthemums (stems tied to a stake, leaves, one colour of flower head per pot);
    builders in spikes/B3b/fp1plants.py. The stand is kept (Stephen). Era: LIFE_LAYER_ERA.md #58."""
    ab = kind.startswith("ab")
    dead = "_w2" if ab else None
    P = SPart("potted", budget="medium", res3=True, mass=25.0, wear="_w2" if ab else "_w1")
    if kind == "pair":
        P.flat = True
        P.need = ()
        P.res3 = False
        P.budget = "box"
        add_all(P, pot((0.0, 0.0, 0.0), r=0.14, h=0.20, mat=WOOD, dead_soil=True))  # the cut-down tub
        add_all(P, FP.pine_bonsai((0.0, 0.17, 0.0), size=1.15, seed=3))
        add_all(P, FP.earthen_pot((0.36, 0.0, 0.08), r=0.10, h=0.16))
        add_all(P, FP.azalea((0.36, 0.128, 0.08), size=1.0, seed=5))
        P.dim("pots", 2, 2, tol=0)
        return P
    # the stand: two sloped side boards and three steps (0.25 / 0.50 / 0.75), 1.2 m wide, each step 0.22 deep
    stand = []
    side = [(0.0, 0.34), (0.27, 0.34), (0.77, -0.34), (0.0, -0.34)]
    for sx in (-1, 1):
        stand.append(prism(side, "x", sx * 0.60 - 0.015, sx * 0.60 + 0.015, WOOD, vis=(1, 2)))
    for k, (y, z0, z1) in enumerate(((0.25, 0.12, 0.34), (0.50, -0.11, 0.11), (0.75, -0.34, -0.12))):
        stand.append(W(-0.585, 0.585, y - 0.025, y, z0, z1, WOOD, vis=(1, 2)))
    lod3 = [W(-0.6, 0.6, 0.0, 0.75, -0.34, 0.34, WOOD, vis=(3,))]
    hull = [col(-0.60, 0.60, 0.0, 0.25, 0.12, 0.34), col(-0.60, 0.60, 0.0, 0.50, -0.11, 0.11),
            col(-0.60, 0.60, 0.0, 0.75, -0.34, -0.12)]
    pots, plants = [], []
    R, H = 0.088, 0.15                                    # flower pots fit the 0.22 m steps (rim d 0.20)
    spots = [(-0.30, 0.25, 0.23, "kiku"), (0.25, 0.25, 0.23, "kiku"), (-0.2, 0.50, 0.0, "azalea"),
             (0.3, 0.50, 0.0, "weeds"), (0.0, 0.75, -0.23, "pine")]
    for i, (x, y, z, what) in enumerate(spots):
        if kind == "ab_dead" and i == 1:
            continue                     # this one fell: see below
        if what == "pine":
            pots += FP.earthen_pot((x, y, z), r=0.095, h=0.085, shallow=True, wear=dead,
                                   soil_mat=LEAF, soil_wear="_w2" if ab else "_w1")
            plants += FP.pine_bonsai((x, y + 0.063, z), size=1.05, seed=40 + i, foliage_wear="_w1")
            continue
        pots += FP.earthen_pot((x, y, z), r=R, h=H, wear=dead, soil_mat=LEAF, soil_wear="_w2" if ab else "_w1")
        ys = y + H - 0.032
        if what == "kiku":
            plants += FP.kiku((x, ys, z), size=0.95, seed=10 + i, wear=dead, flowers=not ab, band=i % 3)
        elif what == "azalea":
            plants += FP.azalea((x, ys, z), size=0.95, seed=20 + i, half_dead=ab)
        else:
            plants += K.bush((x, ys, z), 0.07, 0.14, kind="needle", n=2, seed=30 + i, wear="_w2")
    if kind == "ab_dead":
        # the fallen pot: shards and a soil clod with the dead chrysanthemum, in front of the stand
        add_all(P, K.lkit.shards(581, 0.35, 0.55, 0.18, 7, mat=FP.EARTHEN, wear="_w2"))
        P.add(K.mound(582, 0.30, 0.52, 0.10, 0.06, EARTH, wear="_w2", vis=(1,)))
        add_all(P, rest(xfs(FP.kiku((0.0, 0.0, 0.0), wear="_w2", flowers=False, seed=11, band=1), rz=80.0,
                            t=(0.30, 0.06, 0.52)), 0.0))
    everything = stand + pots + plants
    if kind == "ab_fallen":
        # the stand tipped forward onto its face, pots spilled in front
        tip = dict(rx=78.0, pivot=(0.0, 0.0, 0.34))
        everything = xfs(stand, **tip)
        hull = xfs(hull, **tip)
        lod3 = xfs(lod3, **tip)
        r = random.Random(583)
        for k in range(4):
            px, pz = -0.45 + 0.3 * k, 1.05 + r.uniform(-0.1, 0.25)
            pp = FP.earthen_pot((0.0, 0.0, 0.0), r=R, h=H, wear="_w2", soil_mat=LEAF, soil_wear="_w2")
            everything += rest(xfs(pp, rx=90.0 if k % 2 else 0.0, ry=r.uniform(0, 360), t=(px, 0.0, pz)), 0.0)
            everything.append(K.mound(584 + k, px + 0.1, pz + 0.12, 0.12, 0.05, EARTH, wear="_w2", vis=(1,)))
        everything += rest(xfs(FP.pine_bonsai((0.0, 0.0, 0.0), size=1.05, seed=45), rz=75.0, t=(0.5, 0.0, 1.3)), 0.0)
        P.add(litter(585, 0.0, 1.1, 0.7, sx=1.5))
    add_all(P, everything + lod3 + hull)
    if kind == "ab_fallen":
        ground(P)
    P.dim("stand_w", 1.20, 1.20, tol=0.01)
    P.dim("top_step", 0.75, 0.75, tol=0.01)
    return P


PROPS.append({"id": "jp_s_potted", "cat": CAT, "ll": "#58", "mount": "yard", "tiers": [2, 3],
              "notes": ["potted plants on a stepped stand: pine, azalea, chrysanthemums (in bloom = cream heads), weeds; "
                        "no morning glories (era: LIFE_LAYER_ERA.md #58). Stand = Geometry (one hull); pots visual",
                        "as left: unwatered, the chrysanthemums and azalea dead (jp_m_plant_foliage _w2), the pine green"],
              "models": [
                  M("jp_s_potted_stand", "stand", "intact", "Potted plants on a stepped stand", lambda: potted("stand")),
                  M("jp_s_potted_pair", "pair", "intact", "A potted pine in a tub and an azalea",
                    lambda: potted("pair"), mount="street"),
                  M("jp_s_potted_ab_dead", "stand", "abandoned", "Potted plants dead on their stand, one pot broken",
                    lambda: potted("ab_dead")),
                  M("jp_s_potted_ab_fallen", "stand", "abandoned", "Plant stand tipped over, pots spilled",
                    lambda: potted("ab_fallen")),
              ]})


# ================================================================================================ 59 bird cage
def cage(wear=None, door_open=False, torn=False):
    """A square bamboo songbird cage (uguisu-kago) 0.30 x 0.24 x 0.32: tray, paper-covered top, corner posts, thin
    bars, a small door on the front, a feeder cup inside. Built with its base centre at the origin."""
    w, d, h = 0.30, 0.24, 0.32
    out = [W(-w / 2, w / 2, 0.0, 0.03, -d / 2, d / 2, WOOD, vis=(1, 2)),
           W(-w / 2, w / 2, h - 0.02, h, -d / 2, d / 2, PAPER, vis=(1, 2))]
    out[-1].wear = "_w2" if torn else "_w1"
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * w / 2 - 0.008 * (sx > 0), sx * w / 2 + 0.008 * (sx < 0), 0.03, h - 0.02,
                         sz * d / 2 - 0.008 * (sz > 0), sz * d / 2 + 0.008 * (sz < 0), BAMBOO, vis=(1,)))
    for k in range(1, 6):
        x = -w / 2 + w * k / 6
        for sz in (-1, 1):
            if door_open and sz == 1 and abs(x) < 0.06:
                continue
            out.append(pole((x, 0.03, sz * (d / 2 - 0.004)), (x, h - 0.02, sz * (d / 2 - 0.004)), 0.0025, BAMBOO, n=3,
                            vis=(1,)))
    for k in range(1, 5):
        z = -d / 2 + d * k / 5
        for sx in (-1, 1):
            out.append(pole((sx * (w / 2 - 0.004), 0.03, z), (sx * (w / 2 - 0.004), h - 0.02, z), 0.0025, BAMBOO, n=3,
                            vis=(1,)))
    door = W(-0.05, 0.05, 0.05, 0.16, d / 2 + 0.002, d / 2 + 0.008, BAMBOO, vis=(1,))
    out.append(xf(door, rx=-100.0, pivot=(0.0, 0.05, d / 2)) if door_open else door)
    cup = lathe([(0.02, 0.0), (0.025, 0.03), (0.0, 0.03)], 6, DARKC, vis=(1,))
    out.append(xf(cup, rz=80.0, t=(0.06, 0.055, 0.02)) if door_open else xf(cup, t=(0.07, 0.03, 0.02)))
    out.append(W(-w / 2, w / 2, 0.03, h - 0.02, -d / 2, d / 2, BAMBOO, vis=(2,)))
    return K.wear_all(out, wear)


def bird_cage(kind):
    ab = kind.startswith("ab")
    P = SPart("bird_cage", budget="small", mass=1.0, anchor="wall" if not ab else "floor", wall_gap=0.0, flat=True,
              wear="_w2" if ab else "_w1")
    if not ab:
        P.hung = True
        add_all(P, brackets((0.0,), z=0.36))
        top = EAVE_Y - 0.30
        P.add(cord((0.0, EAVE_Y, 0.33), (0.0, top + 0.32, 0.33), 0.004))
        add_all(P, xfs(cage(door_open=kind == "open"), t=(0.0, top, 0.33)))
        P.extra["hang_y"] = EAVE_Y
        P.dim("cage_h", 0.32, 0.32, tol=0.01)
        P.dim("bottom_y", 2.10, top, tol=0.05)
    else:   # ab_fallen: the cord rotted, the cage fell and lies skewed on its side, paper torn
        c = cage(wear="_w2", door_open=True, torn=True)
        c = xfs(c, rz=90.0, rx=12.0)
        add_all(P, rest(c, 0.0))
        P.add(litter(591, 0.0, 0.1, 0.35))
        P.dim("cage_h", 0.32, 0.32, tol=0.01)
    P.notes.append("empty songbird cage (bush warbler, BUILDING_LIST 824): the bird is gone; visual only")
    return P


PROPS.append({"id": "jp_s_bird_cage", "cat": CAT, "ll": "#59", "mount": "eaves", "tiers": [2, 3],
              "models": [
                  M("jp_s_bird_cage_hung", "hung", "intact", "Empty bird cage hung under the eaves",
                    lambda: bird_cage("hung")),
                  M("jp_s_bird_cage_open", "hung", "abandoned", "Empty bird cage, door open, feeder tipped",
                    lambda: bird_cage("open")),
                  M("jp_s_bird_cage_ab_fallen", "hung", "abandoned", "Bird cage fallen, paper torn",
                    lambda: bird_cage("ab_fallen"), mount="yard"),
              ]})


# ================================================================================================ 60 bamboo pipe (kakei)
def trough_wood(x0, x1, z0, z1, h, t=0.04, wear=None, fill=None, broken=False):
    """A plank trough on the ground: bottom + 4 sides, leaf / silt fill (open vessel: leaves, never water)."""
    out = [W(x0, x1, 0.0, t, z0, z1, WOOD, vis=(1, 2)),
           W(x0, x0 + t, t, h, z0, z1, WOOD, vis=(1, 2)), W(x1 - t, x1, t, h, z0, z1, WOOD, vis=(1, 2)),
           W(x0 + t, x1 - t, t, h, z0, z0 + t, WOOD, vis=(1, 2))]
    front = W(x0 + t, x1 - t, t, h, z1 - t, z1, WOOD, vis=(1, 2))
    if broken:
        front = xf(front, rx=80.0, pivot=(0.0, 0.0, z1))
        front = rest([front], 0.0)[0]
    out.append(front)
    if fill is not None:
        out.append(leaves(601, (x0 + x1) / 2, (z0 + z1) / 2, 0.9 * min(x1 - x0, z1 - z0) / 2, fill, wear="_w2",
                          sx=(x1 - x0) / (z1 - z0)))
    return K.wear_all(out, wear)


def kakei(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("kakei", budget="small", mass=40.0, bury=0.37, wear="_w2" if ab else "_w1")
    for x, H, lean in ((-1.6, 1.0, 0.0), (-0.5, 0.82, -22.0 if ab else 0.0)):
        ss, c = stake_pair(x, H, lean, wear=wear)
        ss = [s for s in ss if 3 not in s.vis]
        add_all(P, ss)
        P.add(c)
    if kind in ("trough", "stone"):
        P.add(pole((-2.6, 1.14, 0.0), (0.45, 0.66, 0.0), 0.04, BAMBOO, n=6, vis=(1, 2)))
        if kind == "trough":
            add_all(P, trough_wood(0.25, 1.35, -0.18, 0.18, 0.34, fill=0.26))
            P.add(col(0.25, 1.35, 0.0, 0.34, -0.18, 0.18))
            P.dim("trough_l", 1.10, 1.10, tol=0.01)
        else:
            basin = lathe([(0.26, 0.0), (0.32, 0.18), (0.30, 0.40), (0.24, 0.42), (0.20, 0.30), (0.0, 0.30)], 9, FIELD,
                          vis=(1,))
            add_all(P, [xf(basin, t=(0.75, 0.0, 0.0)),
                        xf(lathe([(0.26, 0.0), (0.32, 0.2), (0.26, 0.42), (0.0, 0.42)], 6, FIELD, vis=(2,),
                                 smooth=False), t=(0.75, 0.0, 0.0)),
                        leaves(602, 0.75, 0.0, 0.19, 0.305, wear="_w2"),
                        K.moss_top(603, 0.75, 0.0, 0.10, 0.42, sx=2.2)])
            P.add(cyl_col(0.31, 0.0, 0.42, n=8, cx=0.75))
            P.dim("basin_d", 0.64, 0.64, tol=0.02)
        P.dim("pipe_l", 3.08, math.hypot(3.05, 0.48), tol=0.05)
    else:   # ab_broken: the pipe split and fallen in two, the trough dry, its front board off
        P.add(pole((-2.4, 0.04, 0.35), (-1.0, 0.04, 0.55), 0.04, BAMBOO, n=6, vis=(1, 2), wear="_w2"))
        P.add(pole((-0.9, 0.9, 0.0), (0.2, 0.04, 0.45), 0.04, BAMBOO, n=6, vis=(1, 2), wear="_w2"))
        add_all(P, trough_wood(0.25, 1.35, -0.18, 0.18, 0.34, fill=0.08, wear="_w2", broken=True))
        P.add(col(0.25, 1.35, 0.0, 0.34, -0.18, 0.14))
        P.add(litter(604, 0.5, 0.4, 0.8, sx=1.6))
        P.dim("trough_l", 1.10, 1.10, tol=0.01)
    P.notes.append("rural water without a well: a bamboo pipe (kakei) on crossed stakes into a trough or basin "
                   "(BUILDING_LIST 1850, 2420); dead world: leaves and silt, no running water")
    return P


PROPS.append({"id": "jp_s_kakei", "cat": CAT, "ll": "#60", "mount": "yard", "tiers": [1, 2],
              "models": [
                  M("jp_s_kakei_trough", "trough", "intact", "Bamboo water pipe into a wooden trough",
                    lambda: kakei("trough")),
                  M("jp_s_kakei_stone", "stone", "intact", "Bamboo water pipe into a stone basin",
                    lambda: kakei("stone")),
                  M("jp_s_kakei_ab_broken", "trough", "abandoned", "Bamboo pipe fallen, trough dry and broken",
                    lambda: kakei("ab_broken")),
              ]})


# ================================================================================================ 61 stable yard
def pack_saddle(wear=None):
    """Nigura: two straw cushions over a horse's back and two wooden arches joined by side bars (0.9 x 0.6)."""
    out = []
    for sz in (-1, 1):
        cu = K.lkit.pillow(0.75, 0.22, 0.10, TAWARA, nx=3, nz=2, wear=wear, vis=(1,))
        out.append(xf(cu, rx=sz * 62.0, t=(0.0, -0.02, sz * 0.10)))
    for x in (-0.28, 0.28):
        for sz in (-1, 1):
            out.append(beam((x, 0.02, sz * 0.24), (x, 0.20, sz * 0.03), 0.05, 0.035, WOOD, vis=(1,)))
        out.append(W(x - 0.025, x + 0.025, 0.18, 0.24, -0.05, 0.05, WOOD, vis=(1,)))
    for sz in (-1, 1):
        out.append(beam((-0.36, 0.10, sz * 0.15), (0.36, 0.10, sz * 0.15), 0.04, 0.03, WOOD, vis=(1,)))
    out.append(prism([(-0.02, -0.26), (0.24, 0.0), (-0.02, 0.26)], "x", -0.38, 0.38, TAWARA, vis=(2,)))
    return K.wear_all(out, wear)


def sawhorse(L=1.2, H=0.90, wear=None):
    out = [W(-L / 2, L / 2, H - 0.08, H, -0.04, 0.04, WOOD, vis=(1, 2))]
    for x in (-L / 2 + 0.1, L / 2 - 0.1):
        for sz in (-1, 1):
            out.append(beam((x, 0.0, sz * 0.30), (x, H - 0.08, sz * 0.02), 0.05, 0.05, WOOD, vis=(1, 2)))
    return K.wear_all(out, wear)


def stable_yard(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("stable_yard", budget="box", res3=True, mass=80.0, bury=0.40, wear="_w2" if ab else "_w1")
    if kind == "tie_post":
        P.add(W(-0.07, 0.07, -0.40, 1.30, -0.07, 0.07, WOOD, vis=(1, 2)))
        P.add(W(-0.07, 0.07, -0.40, 1.30, -0.07, 0.07, WOOD, vis=(3,)))
        ring = K.lkit.coil(0.0, 0.0, 0.05, 0.008, IRON, n=8, m=3)
        P.add(xf(ring, t=(0.0, 1.05, 0.07)))
        add_all(P, rope_path([(0.0, 1.02, 0.12), (0.03, 0.75, 0.16), (0.12, 0.30, 0.20), (0.25, 0.02, 0.35),
                              (0.55, 0.02, 0.40)], 0.008, ROPE, n=4, wear="_w2"))
        P.add(col(-0.07, 0.07, -0.40, 1.30, -0.07, 0.07))
        # a wooden trough on legs beside it
        tr = trough_wood(0.35, 1.55, -0.20, 0.20, 0.30, fill=0.20)
        tr = xfs(tr, t=(0.0, 0.35, 0.0))
        add_all(P, tr)
        for x in (0.42, 1.48):
            for sz in (-1, 1):
                P.add(W(x - 0.03, x + 0.03, 0.0, 0.35, sz * 0.15 - 0.03, sz * 0.15 + 0.03, WOOD, vis=(1, 2)))
        P.add(W(0.35, 1.55, 0.0, 0.65, -0.2, 0.2, WOOD, vis=(3,)))
        P.add(col(0.35, 1.55, 0.35, 0.65, -0.20, 0.20))
        for x in (0.42, 1.48):
            P.add(col(x - 0.03, x + 0.03, 0.0, 0.345, -0.18, 0.18))
        P.dim("post_h", 1.30, 1.30, tol=0.01)
    elif kind in ("saddle_rack", "ab_saddle_fallen"):
        P.bury = 0.02
        rk = sawhorse(wear=wear)
        add_all(P, rk)
        P.add(W(-0.6, 0.6, 0.0, 0.9, -0.3, 0.3, WOOD, vis=(3,)))
        if kind == "saddle_rack":
            sd = xfs(pack_saddle(), t=(0.0, 0.92, 0.0))
            add_all(P, sd)
            P.add(hull3([v for s in rk + sd for v in s.verts if 1 in s.vis], WOOD))
        else:
            P.add(hull3([v for s in rk for v in s.verts], WOOD))
            sd = xfs(pack_saddle(wear="_w2"), rz=100.0, ry=25.0)
            sd = rest(xfs(sd, t=(0.95, 0.0, 0.45)), 0.0)
            add_all(P, sd)
            add_all(P, rope_path([(0.6, 0.02, 0.1), (0.4, 0.02, 0.6), (0.1, 0.02, 0.7)], 0.008, ROPE, n=4, wear="_w2"))
            P.add(litter(611, 0.5, 0.4, 0.7, sx=1.5))
        P.dim("rack_h", 0.90, 0.90, tol=0.01)
    else:   # trough_stone: a long cut-stone water trough, leaves and silt inside
        P.bury = 0.05
        t = 0.08
        parts = [W(-0.70, 0.70, -0.05, t, -0.22, 0.22, CUT, vis=(1, 2)),
                 W(-0.70, -0.70 + t, t, 0.40, -0.22, 0.22, CUT, vis=(1, 2)),
                 W(0.70 - t, 0.70, t, 0.40, -0.22, 0.22, CUT, vis=(1, 2)),
                 W(-0.70 + t, 0.70 - t, t, 0.40, -0.22, -0.22 + t, CUT, vis=(1, 2)),
                 W(-0.70 + t, 0.70 - t, t, 0.40, 0.22 - t, 0.22, CUT, vis=(1, 2))]
        add_all(P, parts)
        P.add(leaves(612, 0.0, 0.0, 0.14, 0.30, wear="_w2", sx=4.0))
        P.add(K.moss_top(613, -0.55, 0.0, 0.10, 0.40, sx=1.0))
        P.add(W(-0.7, 0.7, -0.05, 0.40, -0.22, 0.22, CUT, vis=(3,)))
        P.add(col(-0.70, 0.70, -0.05, 0.40, -0.22, 0.22, CUT))
        P.dim("trough_l", 1.40, 1.40, tol=0.01)
    P.notes.append("stable yard: tie post with an iron ring, feed trough, pack saddle (nigura) on a rack, stone "
                   "trough (BUILDING_LIST 550, 971, 2466)")
    return P


PROPS.append({"id": "jp_s_stable_yard", "cat": CAT, "ll": "#61", "mount": "yard", "tiers": [1, 2],
              "models": [
                  M("jp_s_stable_yard_tie_post", "tie_post", "intact", "Horse tie post and a feed trough",
                    lambda: stable_yard("tie_post")),
                  M("jp_s_stable_yard_saddle_rack", "saddle_rack", "intact", "Pack saddle on a rack",
                    lambda: stable_yard("saddle_rack")),
                  M("jp_s_stable_yard_trough_stone", "trough_stone", "intact", "Stone water trough, leaves inside",
                    lambda: stable_yard("trough_stone"), mount="street"),
                  M("jp_s_stable_yard_ab_saddle_fallen", "saddle_rack", "abandoned", "Pack saddle fallen off its rack",
                    lambda: stable_yard("ab_saddle_fallen")),
              ]})
