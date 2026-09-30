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

CAT = "yard_life"
PROPS = []


def view_hull(ss, mat=STACK):
    """Soft cover: one View-only convex component round the given solids (sight stops, bullets pass)."""
    return hull3([v for s in ss for v in s.verts], mat, geo=False, view=True, fire=False)


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


def sheaf_row(x0, x1, yfun, seed, wear=None, seg=0.23, drop=(0.52, 0.72), skip=()):
    r = random.Random(seed)
    out = []
    n = max(1, int(round((x1 - x0) / seg)))
    for i in range(n):
        if i in skip:
            continue
        a, b = x0 + (x1 - x0) * i / n + 0.006, x0 + (x1 - x0) * (i + 1) / n - 0.006
        out.append(sheaf(a, b, yfun((a + b) / 2), r.uniform(*drop), half=r.uniform(0.15, 0.19), wear=wear))
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
        shv = sheaf_row(-1.9, 1.9, yat, 51, wear=wear, skip=(4, 5, 11) if ab else ())
        if ab:        # the fallen sheaves lie in the stubble below
            r = random.Random(5)
            for k in range(4):
                s = sheaf(-0.12, 0.12, 0.0, 0.6, wear="_w2")
                shv.append(rest([xf(s, rx=90.0 + r.uniform(-12, 12), ry=r.uniform(-40, 40),
                                    t=(r.uniform(-1.4, 1.4), 0.17, r.uniform(0.5, 1.0)))], 0.0)[0])
            add_all(P, [litter(8, 0.0, 0.7, 1.4, sx=2.0)])
        add_all(P, shv)
        hang = [s for s in shv if s.bbox()[2] > 0.3]
        for k in range(0, len(hang), 8):
            P.add(view_hull(hang[k:k + 8]))
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
                shv = sheaf_row(-1.9, 1.9, lambda x, y=y: y, 60 + k, seg=0.26)
                shv = xfs(shv, t=(0.0, 0.0, 0.075))
                add_all(P, shv)
                P.add(view_hull(shv[: len(shv) // 2]))
                P.add(view_hull(shv[len(shv) // 2:]))
                P.add(xf(prism([(y + 0.05, -0.04), (y + 0.05, 0.04), (y - 0.5, 0.15), (y - 0.5, -0.15)], "x", -1.9, 1.9,
                               STACK, vis=(2,)), t=(0.0, 0.0, 0.075)))
                P.add(box(-1.9, 1.9, y - 0.5, y + 0.05, -0.05, 0.2, STACK, vis=(3,)))
            else:
                r = random.Random(70 + k)
                for i in range(3):
                    x = r.uniform(-1.6, 1.6)
                    P.add(xf(sheaf(x - 0.04, x + 0.04, y, 0.25, half=0.05, wear="_w2"), t=(0.0, 0.0, 0.075)))
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
            s = sheaf(-0.12, 0.12, 0.0, r.uniform(0.5, 0.65), wear="_w2")
            P.add(rest([xf(s, rx=90.0 + r.uniform(-15, 15), ry=r.uniform(-60, 60),
                           t=(r.uniform(-1.7, 1.7), 0.17, r.uniform(-0.2, 0.9)))], 0.0)[0])
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
