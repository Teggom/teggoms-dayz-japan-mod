"""Round wood and poles (BUILD_LIST order of work, step 1): oke, fire tub, firewood, bench, laundry pole, tenbin,
handcart. Reuses B3a: props_kitchen.bundle / split_log (firewood), props_storage.tawara_bale (cart loads),
bits (jag_rim, stain, disc), fkit (lathe, xf, col_solid ...)."""
import math
import random

import skit
from skit import (core, box, sheet, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, lcyl, rest, SPart, pole,
                  beam, rope_path, sag, grid_sheet, text_on, leaves, litter, add_all, ground, rng, hull3, disc,
                  jag_rim, spoked_wheel, wheel_lod, WOOD, DARK, BAMBOO, IRON, CUT, FIELD, RIVER, ROPE, TAWARA,
                  MUSHIRO, PAPER, NOREN, KINARI, ENDG, LEAF, SUMI, BENGARA, FIREWOOD, FIREEND)
import props_kitchen as K     # B3a (read-only): bundle(), split_log()
import props_storage as S     # B3a (read-only): tawara_bale()
import woodpile as WP         # FP2 (2026-10-01): the split-billet woodpile (spikes/B3a/woodpile.py)

SOOT = "wood_sooted"
WEAVE = "bamboo_weave"


def M(p3d, variant, state, display, fn, **kw):
    d = {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}
    d.update(kw)
    return d


# ================================================================================================ coopered vessels
def hoop(r, y, w, n, vis=(1,), wear=None, proud=0.007):
    """One split-bamboo hoop: a single band just proud of radius r (n faces)."""
    s = lathe([(r + proud, y - w / 2), (r + proud, y + w / 2)], n, BAMBOO, vis=vis, smooth=True)
    if wear:
        s.wear = wear
    return s


def vessel(rb, rt, h, n=12, fill=None, rim=0.016, under=False, vis=(1,), wear=None, mat=WOOD, hoops=(), lod2=True,
           fill_mat=LEAF, fill_wear="_w1"):
    """A stave vessel standing on y = 0: outside, rim, inside down to `fill` (leaf litter / silt disc) or to the
    bottom board at 0.03. Returns [solids] (Res 1 detail + an optional Res 2 shell)."""
    yb = 0.03 if fill is None else fill
    ri = lambda y: rb - rim + (rt - rb) * y / h          # noqa: E731  inner stave face radius at height y
    rib = ri(yb)
    if fill is None:
        prof = [(rb, 0.0), (rt, h), (rt - rim, h), (rib, yb), (0.0, yb)]
    else:
        # F1 (G4 walk): the fill disc used to be a polygon at phase 0 while the lathe's vertices sit at phase pi/n, so
        # its corners poked into the staves and its edges left a sliver open at every stave corner, through which the
        # back-face-culled outer wall let the street show. Now the inner wall runs 3 cm on below the fill, and the disc
        # has the lathe's own vertex angles and reaches 3 mm into the stave thickness: sealed at any angle.
        yl = max(0.0, yb - 0.03)
        prof = [(rb, 0.0), (rt, h), (rt - rim, h), (ri(yl), yl)]
    if under:
        prof = [(0.0, 0.0)] + prof
    out = [lathe(prof, n, mat, vis=vis, wear=wear, smooth=True)]
    if fill is not None:
        ph = math.pi / n                                   # fkit.lathe's default phase
        rf = rib + 0.003
        out.append(flat_poly([(rf * math.cos(ph + 2 * math.pi * k / n), -rf * math.sin(ph + 2 * math.pi * k / n))
                              for k in range(n)][::-1], yb, fill_mat, vis=vis, wear=fill_wear))
    for y in hoops:
        out.append(hoop(rb + (rt - rb) * y / h, y, 0.024 if h > 0.3 else 0.02, n, vis=vis, wear=wear))
    if lod2:
        out.append(lathe([(rb, 0.0), (rt, h), (0.0, h - 0.03)], 6, mat, vis=(2,), wear=wear, smooth=False))
    return out


def teoke(wear=None, vis=(1,), lod2=True, fill=0.05, under=False):
    """Hand bucket (teoke) d 0.26 x h 0.25, two ear staves to 0.45 with a cross handle (the fire-tub / grave-rack
    bucket)."""
    rb, rt, h = 0.12, 0.13, 0.25
    out = vessel(rb, rt, h, n=10, fill=fill, hoops=(0.05, 0.20), vis=vis, wear=wear, lod2=lod2, under=under)
    for sx in (-1, 1):
        out.append(W(sx * (rt - 0.012) - 0.007, sx * (rt - 0.012) + 0.007, h - 0.03, 0.45, -0.026, 0.026, WOOD,
                     vis=vis))
    out.append(W(-rt - 0.005, rt + 0.005, 0.40, 0.425, -0.012, 0.012, WOOD, vis=vis))
    if wear:
        for s in out:
            s.wear = wear
    return out


def ninai(wear=None, vis=(1,), lod2=True, fill=0.06):
    """Carrying bucket (ninai-oke) d 0.38 x h 0.38, two tall ear staves (0.62) with rope holes."""
    rb, rt, h = 0.18, 0.19, 0.38
    out = vessel(rb, rt, h, n=12, fill=fill, hoops=(0.06, 0.32), vis=vis, wear=wear, lod2=lod2)
    for sx in (-1, 1):
        out.append(W(sx * (rt - 0.012) - 0.008, sx * (rt - 0.012) + 0.008, h - 0.04, 0.62, -0.035, 0.035, WOOD,
                     vis=vis))
        out.append(W(sx * (rt + 0.0) - 0.01, sx * rt + 0.01, 0.54, 0.575, -0.02, 0.02, ROPE, vis=vis))
    if wear:
        for s in out:
            s.wear = wear
    return out


def taru(wear=None, vis=(1,), lod2=True, lid=True, stone=True, n=12):
    """Pickle / soy barrel (taru) d 0.55 x h 0.65 with a drop lid and a river-stone weight."""
    rb, rt, h = 0.265, 0.275, 0.65
    out = vessel(rb, rt, h, n=n, fill=None, hoops=(0.08, 0.33, 0.58), vis=vis, wear=wear, lod2=lod2)
    top = h
    if lid:
        out.append(disc(rt - 0.01, h - 0.06, h - 0.02, WOOD, n=n, vis=vis, wear=wear))
        top = h - 0.02
        if stone:
            st = core.stone(random.Random(11), 0.03, -0.02, 0.26, 0.22, 0.16, top + 0.16, RIVER, bury=0.0, n=8,
                            vis=(1, 2))
            out.append(st)
            top += 0.16
    return out, top


# ------------------------------------------------------------------------------------------------ jp_s_oke
def oke(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("oke", budget="small", mass={"tarai": 8.0, "teoke": 2.5, "ninai": 5.0, "taru_lid": 40.0,
                                            "stake": 4.0, "ab_tipped": 30.0, "ab_staves": 6.0}[kind])
    P.extra["no_iron"] = True
    if kind == "tarai":
        rb, rt, h = 0.33, 0.35, 0.22
        add_all(P, vessel(rb, rt, h, n=16, fill=0.05, hoops=(0.05, 0.17)))
        P.add(col(-0.30, 0.30, 0.0, 0.05, -0.30, 0.30))
        for sx in (-1, 1):
            P.add(col(sx * 0.305, sx * 0.35, 0.0, h, -0.24, 0.24))
            P.add(col(-0.24, 0.24, 0.0, h, sx * 0.305, sx * 0.35))
        P.add(litter(4, 0.2, 0.25, 0.45, sx=1.3))
        P.dim("d", 0.70, 2 * rt, tol=0.01)
        P.dim("h", 0.22, h, tol=0.01)
    elif kind == "teoke":
        add_all(P, teoke())
        P.add(cyl_col(0.13, 0.0, 0.25, n=8))
        P.dim("d", 0.26, 0.26, tol=0.01)
        P.dim("h", 0.25, 0.25, tol=0.01)
        P.dim("handle", 0.20, 0.45 - 0.25, tol=0.01)
    elif kind == "ninai":
        add_all(P, ninai())
        P.add(cyl_col(0.19, 0.0, 0.38, n=8))
        P.dim("d", 0.38, 0.38, tol=0.01)
        P.dim("h", 0.38, 0.38, tol=0.01)
    elif kind == "taru_lid":
        ss, top = taru()
        add_all(P, ss)
        P.add(cyl_col(0.275, 0.0, 0.63, n=8))
        P.add(col_solid(ss[-2] if False else core.stone(random.Random(11), 0.03, -0.02, 0.24, 0.20, 0.15, top - 0.005,
                                                        RIVER, bury=0.0, n=6)))
        P.dim("d", 0.55, 0.55, tol=0.01)
        P.dim("h", 0.65, 0.65, tol=0.01)
    elif kind == "stake":
        # oke-hoshi: a bucket upside down on a stake, drying
        P.add(pole((0.0, -0.05, 0.0), (0.0, 1.02, 0.0), 0.022, WOOD, n=5, vis=(1, 2)))
        b = teoke(lod2=False, fill=None, under=True)
        b = xfs(b, rz=180.0, t=(0.0, 1.02 + 0.25, 0.0))
        add_all(P, b)
        P.add(lathe([(0.13, 1.02), (0.12, 1.27), (0.0, 1.27)], 6, WOOD, vis=(2,), smooth=False))
        P.add(col(-0.025, 0.025, 0.0, 1.0, -0.025, 0.025))
        P.add(cyl_col(0.13, 1.02, 1.27, n=8))
        P.bury = 0.06
        P.dim("stake_h", 1.02, 1.02, tol=0.01)
        P.dim("bucket_d", 0.26, 0.26, tol=0.01)
    elif kind == "ab_tipped":
        # the pickle barrel on its side, lid rolled off, one hoop sprung, silt spilling out
        ss, top = taru(wear="_w2", lid=False, stone=False, lod2=True)
        ss = [s for s in ss if not (s.mats == skit.BAMBOO and abs(s.bbox()[2] - 0.58 + 0.012) < 0.02)]
        ss = xfs(ss, rx=90.0, t=(0.0, 0.275, -0.325))
        add_all(P, ss)
        hp = hoop(0.29, 0.0, 0.024, 12, wear="_w2")
        add_all(P, rest([xf(hp, rx=8.0, t=(0.25, 0.0, 0.55))], 0.001))
        lid = disc(0.26, 0.0, 0.04, WOOD, n=10, vis=(1, 2), wear="_w2")
        add_all(P, rest([xf(lid, rx=80.0, ry=30.0, t=(-0.45, 0.0, 0.50))], 0.0))
        P.add(core.stone(random.Random(11), -0.55, -0.1, 0.24, 0.20, 0.15, 0.15, RIVER, bury=0.0, n=8, vis=(1, 2)))
        P.add(leaves(5, 0.0, 0.45, 0.35, 0.004, wear="_w2", sx=1.1, sz=0.8))
        P.add(xf(cyl_col(0.275, -0.325, 0.325, n=8), rx=90.0, t=(0.0, 0.275, 0.0)))
        P.add(litter(6, 0.0, 0.2, 0.7, sx=1.2))
        ground(P)
        P.dim("d", 0.55, 0.55, tol=0.01)
    else:   # ab_staves: dried out and fallen apart
        r = random.Random(7)
        n = 14
        for k in range(n):
            a = 2 * math.pi * k / n + r.uniform(-0.15, 0.15)
            d = r.uniform(0.05, 0.35)
            st = W(-0.03, 0.03, 0.0, 0.012, -0.11, 0.11, WOOD, vis=(1,))
            st.wear = "_w2"
            P.add(xf(st, ry=math.degrees(-a) + r.uniform(-30, 30), t=(d * math.cos(a), 0.0, d * math.sin(a))))
        # two staves still standing in the bottom board
        P.add(disc(0.31, 0.0, 0.025, WOOD, n=10, vis=(1, 2), wear="_w2"))
        for a in (0.4, 0.75):
            st = W(-0.03, 0.03, 0.0, 0.2, -0.006, 0.006, WOOD, vis=(1,))
            st.wear = "_w2"
            P.add(xf(st, rz=-12.0, ry=-math.degrees(a * math.pi), t=(0.31 * math.cos(a * math.pi), 0.02,
                                                                      0.31 * math.sin(a * math.pi))))
        hp = hoop(0.34, 0.0, 0.02, 12, wear="_w2")
        P.add(xf(hp, t=(0.12, 0.012, -0.05)))
        P.add(leaves(8, 0.0, 0.0, 0.28, 0.027, wear="_w2"))
        P.add(W(-0.35, 0.35, 0.0, 0.02, -0.35, 0.35, WOOD, vis=(2,)))
        P.add(col(-0.3, 0.3, 0.0, 0.025, -0.3, 0.3))
        P.dim("tub_d", 0.70, 0.62, tol=0.1)
    return P


# ================================================================================================ fire tub
def base_stone(w, d, h, mat=CUT, vis=(1, 2, 3), seed=1):
    return box(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, mat, vis=vis)


def pyramid(y0, wear=None, vis=(1,), mark=True):
    """10 hand buckets in 3 tiers (6 + 3 + 1) on a lid at y0 (merged meshes)."""
    out = []
    spots = [(-0.30, -0.16), (0.0, -0.16), (0.30, -0.16), (-0.30, 0.16), (0.0, 0.16), (0.30, 0.16)]
    tiers = [(y0, spots), (y0 + 0.255, [(-0.15, 0.0), (0.15, 0.0), (0.0, -0.18)]), (y0 + 0.51, [(0.0, -0.05)])]
    k = 0
    for y, sp in tiers:
        for x, z in sp:
            b = vessel(0.12, 0.13, 0.25, n=8, fill=0.14, hoops=(0.19,), vis=vis, wear=wear, lod2=False, fill_mat=WOOD)
            add = xfs(b, t=(x, y, z))
            out += add
            if mark and z > 0.1 and k % 2 == 0:
                out.append(text_on((x, y + 0.13, z + 0.128), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.10, SUMI,
                                   "mark_marudai", wear="_w1", off=0.006))
            k += 1
    return out


def fire_tub(kind):
    ab = kind.startswith("ab")
    P = SPart("fire_tub", budget="box", res3=True, mass={"full": 400.0, "open": 400.0, "eave": 2.5, "rural": 60.0,
                                                           "ab_scattered": 400.0}[kind])
    P.extra["no_iron"] = True
    wear = "_w2" if ab else None
    if kind in ("full", "open", "ab_scattered"):
        R, H, B = 0.625, 1.00, 0.22           # tub d 1.25 x h 1.00 on a 0.22 granite base
        fill = 0.62 if kind == "full" else 0.55
        P.add(base_stone(1.45, 1.45, B, CUT, vis=(1, 2, 3)))
        tub = vessel(R - 0.015, R, H, n=14, fill=None if kind == "full" else fill, hoops=(0.12, 0.50, 0.86),
                     wear=wear, lod2=False, fill_wear="_w2")
        add_all(P, xfs(tub, t=(0.0, B, 0.0)))
        P.add(lathe([(R - 0.015, B), (R, B + H), (0.0, B + H - 0.02)], 8, WOOD, vis=(2,), wear=wear, smooth=False))
        P.add(lathe([(R, B), (R, B + H), (0.0, B + H)], 6, WOOD, vis=(3,), wear=wear, smooth=False))
        P.add(text_on((0.0, B + 0.66, R + 0.004), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.34, SUMI, "oke_yosui",
                      wear="_w1" if not ab else "_w2", off=0.004))
        if kind == "full":
            P.add(disc(R + 0.02, B + H, B + H + 0.035, WOOD, n=12, vis=(1, 2)))
            add_all(P, pyramid(B + H + 0.035))
            P.add(W(-0.43, 0.43, B + H + 0.035, B + H + 0.29, -0.3, 0.3, WOOD, vis=(2,)))
            P.add(W(-0.28, 0.28, B + H + 0.29, B + H + 0.54, -0.2, 0.12, WOOD, vis=(2,)))
            P.add(W(-0.13, 0.13, B + H + 0.54, B + H + 0.79, -0.18, 0.08, WOOD, vis=(2,)))
            P.add(W(-0.3, 0.3, B + H, B + H + 0.5, -0.2, 0.2, WOOD, vis=(3,)))
            P.add(col(-0.45, 0.45, B + H, B + H + 0.54, -0.3, 0.3))
            P.dim("pyramid", 10, 10, tol=0)
        else:
            r = random.Random(3 if kind == "open" else 9)
            nb = 3 if kind == "open" else 4
            for i in range(nb):
                b = teoke(wear="_w2", lod2=False, fill=None, under=True)
                a = r.uniform(0, 360)
                dx, dz = [(0.95, 0.35), (-0.9, 0.55), (0.35, 1.0), (-0.4, -1.0), (1.0, -0.6), (-1.05, -0.2)][i]
                if i % 2 == 0 or kind == "ab_scattered":
                    b = xfs(b, rx=90.0)                      # on its side
                    b = xfs(b, ry=a, t=(dx, 0.13, dz))
                else:
                    b = xfs(b, ry=a, t=(dx, 0.0, dz))
                add_all(P, b)
            if kind == "ab_scattered":
                lid = disc(R + 0.02, 0.0, 0.035, WOOD, n=12, vis=(1, 2), wear="_w2")
                add_all(P, rest([xf(lid, rx=72.0, ry=-20.0, t=(-0.1, 0.0, 0.95))], 0.0))
            P.add(litter(12, 0.0, 0.6, 1.0, sx=1.4))
        P.add(cyl_col(R, B, B + H, n=10))
        P.add(col(-0.72, 0.72, 0.0, B, -0.72, 0.72, CUT))
        P.dim("tub_d", 1.25, 2 * R, tol=0.01)
        P.dim("tub_h", 1.00, H, tol=0.01)
        P.dim("base", 0.22, B, tol=0.08)
    elif kind == "eave":
        # one hand bucket hung from an eave peg at 2.0 m (proxy for building fronts): anchor wall, z = 0 wall plane
        P.anchor, P.wall_gap = "wall", 0.0
        P.res3 = False
        P.budget = "small"
        P.add(beam((0.0, 2.02, 0.0), (0.0, 2.02, 0.20), 0.03, 0.03, WOOD, vis=(1, 2)))
        b = teoke(fill=None)
        add_all(P, xfs(b, t=(0.0, 2.02 - 0.43, 0.16)))
        P.add(text_on((0.0, 2.02 - 0.43 + 0.13, 0.16 + 0.128), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.10, SUMI,
                      "mark_marudai", off=0.006))
        P.add(col(-0.015, 0.015, 1.99, 2.05, 0.0, 0.2))
        P.add(cyl_col(0.13, 2.02 - 0.43, 2.02 - 0.18, n=8, cz=0.16))
        P.hung = True
        P.dim("peg_y", 2.0, 2.02, tol=0.1)
        P.notes.append("hung: y = 0 is the ground at the wall foot; the peg sits at 2.02 m (list 1.9-2.1)")
    else:   # rural rain barrel under an eave, about 1 koku
        R, H = 0.33, 0.72
        P.add(core.stone(random.Random(21), 0.0, 0.0, 0.8, 0.75, 0.14, 0.12, FIELD, bury=0.04, n=8, vis=(1, 2, 3)))
        add_all(P, xfs(vessel(R - 0.01, R, H, n=12, fill=0.48, hoops=(0.1, 0.6), wear=None, lod2=True,
                              fill_wear="_w2"), t=(0.0, 0.12, 0.0)))
        P.add(lathe([(R, 0.12), (R, 0.12 + H), (0.0, 0.12 + H)], 5, WOOD, vis=(3,), smooth=False))
        P.add(cyl_col(R, 0.12, 0.12 + H, n=8))
        P.add(col(-0.3, 0.3, 0.0, 0.12, -0.3, 0.3, FIELD))
        P.add(litter(22, 0.2, 0.3, 0.5))
        P.bury = 0.07
        P.dim("d", 0.66, 2 * R, tol=0.01)
        P.dim("capacity_l", 180.0, math.pi * (R - 0.02) ** 2 * (H - 0.05) * 1000, tol=30.0)
    return P


# ================================================================================================ firewood
def _billet(rr, cx, cy, w, h, z, facing, wear=None, vis=(1,)):
    """One billet end (half, quarter or small round) fitted into a w x h cell, end-grain UVs from its pith."""
    kind = rr.choice(("half", "quarter", "quarter", "round", "half"))
    a0 = rr.uniform(0, 2 * math.pi)
    R = 1.0
    if kind == "quarter":
        pts = [(0.0, 0.0)] + [(R * math.cos(a0 + t), R * math.sin(a0 + t)) for t in (0.1, 0.8, 1.5)]
    elif kind == "half":
        pts = [(R * math.cos(a0 + t), R * math.sin(a0 + t)) for t in (0.0, 1.05, 2.1, 3.14)]
    else:
        pts = [(R * math.cos(a0 + t), R * math.sin(a0 + t)) for t in (0.3, 1.9, 3.5, 5.0)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sc = min(w * 0.94 / (max(xs) - min(xs)), h * 0.94 / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    q = [(cx + (x - mx) * sc, cy + (y - my) * sc, z) for x, y in pts]
    uv = [(0.5 + 0.45 * x * (1 if facing > 0 else -1), 0.5 - 0.45 * y) for x, y in pts]
    if facing < 0:
        q, uv = q[::-1], uv[::-1]
    s = sheet([q], FIREEND, (0.0, 0.0, float(facing)), vis=vis, uvs=[uv])   # M1: firewood ends (i22)
    s.finalize()
    if wear:
        s.wear = wear
    return s


def stack_caps(x0, x1, hfun, zf, facing, cell=0.13, seed=1, wear=None, vis=(1,)):
    rr = random.Random(seed)
    out = []
    y = 0.0
    while True:
        dh = cell * rr.uniform(0.85, 1.15)
        x = x0
        row_any = False
        while x < x1 - 0.03:
            dw = min(cell * rr.uniform(0.8, 1.2), x1 - x)
            if y + dh <= hfun(x + dw / 2) + 0.01:
                out.append(_billet(rr, x + dw / 2, y + dh / 2, dw, dh, zf, facing, wear, vis))
                row_any = True
            x += dw
        y += dh
        if not row_any:
            break
    return out


def stack_core(x0, x1, hfun, z0, z1, steps=8, wear=None, vis=(1,), both=False):
    """Dark gaps behind the caps: stepped core boxes following hfun (front/back sooted, sides/top weathered bark)."""
    out = []
    dx = (x1 - x0) / steps
    for i in range(steps):
        a, b = x0 + i * dx, x0 + (i + 1) * dx
        hh = min(hfun(a + 0.01), hfun(b - 0.01))
        s = box(a, b, 0.0, hh, z0, z1, {"front": SOOT, "back": SOOT if both else FIREWOOD, "default": FIREWOOD},
                vis=vis)
        s.wear = "_w2" if wear is None else wear
        out.append(s)
    return out


def firewood(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    D = 0.33                                        # billet length = stack depth (1.1 shaku)
    if kind == "bundle":
        P = SPart("firewood_stack", budget="small", mass=15.0, anchor="wall", wall_gap=0.05)
        ss = K.bundle(random.Random(5), d=0.40, L=1.05, mats=(FIREWOOD, FIREEND), band=ROPE, core_mat=SOOT)
        c = col_solid(lcyl("z", 0.0, 0.20, 0.19, -0.52, 0.52, WOOD, n=7))
        ss = xfs(ss + [c], rx=-110.0)
        lo_y = min(v[1] for s in ss for v in s.verts)
        lo_z = min(v[2] for s in ss if 1 in s.vis for v in s.verts)
        ss = xfs(ss, t=(0.0, -lo_y, 0.05 - lo_z))
        add_all(P, ss)
        P.add(litter(3, 0.0, 0.55, 0.35))
        P.dim("bundle_d", 0.40, 0.40, tol=0.05)
        P.dim("bundle_L", 1.05, 1.05, tol=0.15)
        P.notes.append("one brushwood bundle (soda) leaning 20 deg on a wall; place 1-6 side by side, yawed a little")
        return P
    if kind == "free_posts":
        L, Hh = 1.82, 1.20
        # FP2 (2026-10-01): a real woodpile of split billets, both ends showing (was a box with flat end decals)
        P = SPart("firewood_stack", budget="medium", mass=500.0)
        hf = lambda x: Hh   # noqa: E731
        z0, z1 = -D / 2, D / 2
        ss, info = WP.woodpile(-L / 2, L / 2, hf, z0, z1, seed=11, max_faces=1250, back=True, loose_top=0,
                               over=0.0)
        add_all(P, ss)
        for sx in (-1, 1):
            P.add(pole((sx * (L / 2 + 0.05), -0.08, 0.0), (sx * (L / 2 + 0.05), Hh + 0.12, 0.0), 0.04, WOOD, n=5,
                       vis=(1, 2)))
            P.add(col(sx * (L / 2 + 0.05) - 0.04, sx * (L / 2 + 0.05) + 0.04, 0.0, Hh + 0.12, -0.04, 0.04))
        top = info["top_y"]
        cap = W(-L / 2 - 0.12, L / 2 + 0.12, top + 0.005, top + 0.035, -0.25, 0.25, WOOD, vis=(1, 2))
        P.add(xf(cap, rz=1.0, pivot=(0.0, top, 0.0)))         # the cap board rests on the highest billets
        P.add(col(-L / 2, L / 2, 0.0, Hh, z0, z1))
        P.bury = 0.08
        P.dim("length", 1.82, L, tol=0.01)
        P.dim("height", 1.20, top, tol=0.05)
        P.dim("depth", 0.33, D, tol=0.03)
        P.loot = []   # the cap slopes: dressing only
        P.notes.append("FP2 woodpile, both ends showing: %d faces, billets ~%.0f cm" % (info["faces"], info["cell"] * 100))
        return P
    # wall stacks: the wall plane z = 0, the stack 5 cm off it (C6 wall-backed rule)
    # FP2 (2026-10-01): a real woodpile of split billets (was a sooted box with flat yellow end decals): medium class
    P = SPart("firewood_stack", budget="medium", mass=600.0, anchor="wall", wall_gap=0.05)
    z0, z1 = 0.05, 0.05 + D
    loose = 2
    if kind == "half":
        L = 0.91
        hf = lambda x: 1.20 if x < -0.15 else (0.95 if x < 0.2 else 0.70)   # noqa: E731
        H = 1.20
        loose = 1
    elif kind == "ab_collapsed":
        L = 1.82
        hf = lambda x: 1.20 if x < 0.1 else max(0.40, 1.20 - (x - 0.1) * 0.95)  # noqa: E731
        H = 1.20
        loose = 1
    else:
        L = 1.82
        H = 1.80 if kind == "wall_1ken_h180" else 1.20
        hf = lambda x: H   # noqa: E731
        loose = 1 if H > 1.5 else 2
    ss, info = WP.woodpile(-L / 2, L / 2, hf, z0, z1, seed=len(kind) * 7, max_faces=1300, wear=wear,
                           loose_top=loose)
    add_all(P, ss)
    sky = info["sky"]                     # (Res 2 = one end-grain quad per billet + a stepped block: woodpile)
    steps = 1 if kind.startswith("wall") else 4
    dx = L / steps
    for i in range(steps):
        a, b = -L / 2 + i * dx, -L / 2 + (i + 1) * dx
        hh = min(hf(a + 0.01), hf(b - 0.01))
        P.add(col(a, b, 0.0, hh - 0.02, z0 + 0.01, z1 - 0.01))
    if kind == "ab_collapsed":
        rr = random.Random(8)
        for i in range(9):
            pc = WP._piece(rr, 0.11, 0.10)
            s, P2, _ = WP._billet(rr, pc, -0.055, -0.05, -0.16, 0.16, True, "_w2", loose=True)
            lo = min(p[1] for p in P2)
            s = xf(s, ry=rr.uniform(-60, 60), t=(0.45 + rr.uniform(-0.25, 0.45), -lo, z1 + 0.25 + rr.uniform(0, 0.45)))
            P.add(s)
        P.add(litter(9, 0.4, z1 + 0.35, 0.6, sx=1.4))
        ground(P)
    else:
        P.add(litter(2, 0.0, z1 + 0.15, 0.5, sx=1.8, sz=0.5, wear="_w1"))
    P.dim("length", L, L, tol=0.01)
    P.dim("height", H, max(sky[:20]), tol=0.06)
    P.dim("depth", 0.33, D, tol=0.03)
    P.notes.append("FP2 woodpile: split billets ~%.0f cm (halves, quarters, thirds, rounds), bark sides, end grain "
                   "from each round's pith, ends staggered +-3 cm, dark core 7 cm back; %d faces" %
                   (info["cell"] * 100, info["faces"]))
    return P


# ================================================================================================ bench
def bench(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    long_ = kind == "long"
    L, Wd, H = (2.73, 0.75, 0.42) if long_ else (1.82, 0.55, 0.43)
    P = SPart("bench", budget="small", res3=True, mass=35.0 if long_ else 20.0, wear=wear or "_w1")
    ss, lo2, lo3 = [], [], []
    nb = 4 if long_ else 3
    bw = Wd / nb
    for i in range(nb):
        b = W(-L / 2, L / 2, H - 0.03, H, -Wd / 2 + i * bw + 0.004, -Wd / 2 + (i + 1) * bw - 0.004, WOOD, vis=(1,))
        ss.append(b)
    frames = (-L / 2 + 0.22, 0.0, L / 2 - 0.22) if long_ else (-L / 2 + 0.2, L / 2 - 0.2)
    for fx in frames:
        for sz in (-1, 1):
            ss.append(W(fx - 0.03, fx + 0.03, 0.0, H - 0.03, sz * (Wd / 2 - 0.06) - 0.03, sz * (Wd / 2 - 0.06) + 0.03,
                        WOOD, vis=(1,)))
        ss.append(W(fx - 0.03, fx + 0.03, H - 0.09, H - 0.03, -Wd / 2 + 0.02, Wd / 2 - 0.02, WOOD, vis=(1, 2)))
        ss.append(W(fx - 0.02, fx + 0.02, 0.10, 0.14, -Wd / 2 + 0.06, Wd / 2 - 0.06, WOOD, vis=(1,)))
    ss.append(W(-L / 2 + 0.2, L / 2 - 0.2, 0.18, 0.22, -0.02, 0.02, WOOD, vis=(1,)))
    lo2 += [W(-L / 2, L / 2, H - 0.03, H, -Wd / 2, Wd / 2, WOOD, vis=(2,))]
    for fx in frames:
        lo2.append(W(fx - 0.03, fx + 0.03, 0.0, H - 0.09, -Wd / 2 + 0.03, Wd / 2 - 0.03, WOOD, vis=(2,)))
    lo3 += [W(-L / 2, L / 2, H - 0.04, H, -Wd / 2, Wd / 2, WOOD, vis=(3,))]
    for fx in frames:
        lo3.append(W(fx - 0.03, fx + 0.03, 0.0, H - 0.04, -Wd / 2 + 0.03, Wd / 2 - 0.03, WOOD, vis=(3,)))
    cols = [col(-L / 2, L / 2, H - 0.04, H, -Wd / 2, Wd / 2)] + \
        [col(fx - 0.03, fx + 0.03, 0.0, H - 0.04, -Wd / 2 + 0.03, Wd / 2 - 0.03) for fx in frames]
    allss = ss + lo2 + lo3
    if kind == "mat":
        # a rotted straw mat thrown over the seat, one end hanging down the front
        def f(u, v):
            x = -0.55 + 1.1 * u
            if v < 0.72:
                z = -Wd / 2 + 0.05 + (Wd + 0.02) * v / 0.72
                return (x, H + 0.006, z)
            t = (v - 0.72) / 0.28
            return (x, H + 0.006 - 0.28 * t, Wd / 2 + 0.03 + 0.03 * t)
        m = grid_sheet(f, 2, 3, MUSHIRO, vis=(1,), two_sided=True, wear="_w2")
        allss.append(xf(m, ry=6.0))
    if kind == "ab_tipped":
        allss = xfs(allss + cols, rx=-90.0, t=(0.0, Wd / 2, 0.0))
        cols = [s for s in allss if s.geo]
        allss = [s for s in allss if not s.geo]
        add_all(P, allss + cols)
        ground(P)
        P.add(litter(3, 0.0, -0.3, 0.6, sx=1.6))
    elif kind == "ab_broken":
        # the right leg frame collapsed: the seat slopes to the ground at +x
        keep = [s for s in allss if not (s.bbox()[1] > L / 2 - 0.3 and s.bbox()[3] < H - 0.02)]
        ang = math.degrees(math.atan2(H - 0.03, L - 0.2))
        piv = (-L / 2 + 0.2, H, 0.0)
        top = [s for s in keep if s.bbox()[3] > H - 0.1]
        rest_ = [s for s in keep if s.bbox()[3] <= H - 0.1]
        top = xfs(top, rz=-ang, pivot=piv)
        add_all(P, top + rest_)
        leg = W(-0.03, 0.03, 0.0, 0.40, -0.03, 0.03, WOOD, vis=(1,))
        leg.wear = "_w2"
        P.add(xf(leg, rz=88.0, ry=20.0, t=(L / 2 - 0.1, 0.03, 0.30)))
        P.add(col_solid(xf(box(-L / 2, L / 2, H - 0.04, H, -Wd / 2, Wd / 2, WOOD), rz=-ang, pivot=piv)))
        P.add(cols[1])
        P.add(litter(5, 0.3, 0.2, 0.6, sx=1.6))
    else:
        add_all(P, allss + cols)
        P.road([(-L / 2, H, -Wd / 2), (L / 2, H, -Wd / 2), (L / 2, H, Wd / 2), (-L / 2, H, Wd / 2)], "boards_ext")
        yt = H + (0.006 if kind == "mat" else 0.0)
        zc = -Wd / 2 + bw * 1.5
        pts = [(-L / 2 + L * (i + 0.5) / 3, yt, zc) for i in range(3)] if long_ else [(-0.45, yt, zc), (0.45, yt, zc)]
        if kind == "mat":
            pts = [(0.0, yt, -0.05)]
        P.loot_rect("seat", yt, -L / 2 + 0.1, L / 2 - 0.1, -Wd / 2 + 0.05, Wd / 2 - 0.05, rng=0.25, points=pts)
    P.dim("length", L, L, tol=0.01)
    P.dim("width", Wd, Wd, tol=0.01)
    P.dim("height", H, H, tol=0.01)
    return P


# ================================================================================================ laundry pole
# F1 (G4 walk): the drying pole runs along x, so a fork or a stake cross that holds it must open ACROSS it (in z) and
# the pole must sit in the V. Before, both forks and crossed stakes opened along x (in the pole's own plane): the pole
# could only pass through the crotch. POLE_R = the drying pole's radius; the seat = where it touches both arms.
POLE_R = 0.023
FORK_DZ, FORK_RISE, FORK_R = 0.11, 0.22, 0.022      # branch tip offset across the pole, rise above the crotch, radius


def fork_seat(h):
    """Centre height of the drying pole resting in a post_forked(h) V: tangent to both branches."""
    s = FORK_DZ / math.hypot(FORK_DZ, FORK_RISE)
    return h - 0.02 + (FORK_R + POLE_R) / s


def post_forked(x, h=2.0, wear=None, vis=(1, 2)):
    """A forked wooden post (monohoshi post): trunk to the fork at h, two short branches opening across the pole (z)."""
    y0 = h - 0.02
    out = [pole((x, -0.08, 0.0), (x, h, 0.0), 0.045, WOOD, n=6, vis=vis, r1=0.035, wear=wear)]
    out.append(pole((x, y0, 0.0), (x + 0.01, y0 + FORK_RISE, -FORK_DZ), 0.026, WOOD, n=5, vis=(1,), r1=0.018,
                    wear=wear))
    out.append(pole((x, y0, 0.0), (x - 0.01, y0 + FORK_RISE - 0.01, FORK_DZ + 0.005), 0.026, WOOD, n=5, vis=(1,),
                    r1=0.018, wear=wear))
    # Res 2: the two branches as one flat V board across the pole
    for sz in (-1, 1):
        out.append(pole((x, y0, 0.0), (x, y0 + FORK_RISE, sz * FORK_DZ), 0.03, WOOD, n=3, vis=(2,), r1=0.02,
                        wear=wear))
    return out


CROSS_Y, CROSS_HALF = 1.8, 0.5                      # stakes cross at 1.8 m, feet 1.0 m apart (across the pole)
STAKE_R = 0.025


def cross_seat():
    """Centre height of the drying pole resting in the V above the crossed stakes."""
    s = CROSS_HALF / math.hypot(CROSS_HALF, CROSS_Y + 0.05)
    return CROSS_Y + (STAKE_R + POLE_R) / s


def stakes_crossed(x, wear=None, vis=(1, 2)):
    """Two 2.2 m bamboo stakes crossed at 1.8 m, feet 1.0 apart ACROSS the pole (z), lashed; the pole lies in the V
    above the lashing."""
    out = []
    top_y = CROSS_Y + (2.2 - math.hypot(CROSS_HALF, CROSS_Y + 0.05)) * 0.95
    for sz in (-1, 1):
        # the two stakes pass each other (one just in front of the other) and touch at the lashing
        a = (x + sz * STAKE_R, -0.05, sz * CROSS_HALF)
        b = (x + sz * STAKE_R, top_y, -sz * (top_y - CROSS_Y) * CROSS_HALF / (CROSS_Y + 0.05))
        out.append(pole(a, b, STAKE_R, BAMBOO, n=5, vis=vis, wear=wear))
    out.append(pole((x - 0.03, CROSS_Y - 0.03, -0.04), (x + 0.03, CROSS_Y + 0.02, 0.04), 0.03, ROPE, n=4, vis=(1,)))
    return out


KIMONO = "textile_cotton_indigo"     # plain indigo cotton (B1 library, 0.5 m tile): no shop marks on a garment
COLLAR = ("textile_cotton_indigo", "_w0")   # the collar (eri) facing: the deep, unfaded indigo (a darker band)


def kimono_hung(cx, pole_y, wear="_w1", mat=KIMONO, yuki=0.64, body_w=0.31, sleeve=0.48, drop=1.30, rc=0.030):
    """F1 (G4 walk): a T-shaped kimono (kosode) hung through its sleeves on a drying pole along x at (y = pole_y, z = 0).
    One continuous two-sided cloth per column: up the back panel, over the pole (a shoulder fold of radius rc), down the
    front. Sleeve columns |x - cx| in [body_w, yuki] hang `sleeve` m, the body |x - cx| < body_w hangs `drop` m; front
    and back converge below the fold (sleeves close at their sewn bottoms, the body hangs 2.4 cm apart). UVs at world
    scale (u = x, v = the arc length down the cloth, / the 0.5 m tile): no stretch anywhere. Returns [solids]."""
    t = core.mat_info(mat)["tile"]

    def zoff(d, col_drop, sl):
        if sl:                                  # sleeve: front and back meet at the sewn bottom
            return rc - (rc - 0.006) * min(1.0, d / col_drop)
        return rc - (rc - 0.012) * min(1.0, d / 0.5)

    def column(x0, x1, col_drop, ds, sl):
        # profile (w, y, z): back hem -> back top -> over the pole -> front top -> front hem; w = arc length
        prof = []
        for d in reversed(ds):
            prof.append((pole_y - d, -zoff(d, col_drop, sl)))
        for a in (135.0, 90.0, 45.0):           # the fold over the pole top (the pole is inside it)
            prof.append((pole_y + rc * math.sin(math.radians(a)), -rc * math.cos(math.radians(180.0 - a))))
        for d in ds:
            prof.append((pole_y - d, zoff(d, col_drop, sl)))
        w = [0.0]
        for i in range(1, len(prof)):
            w.append(w[-1] + math.hypot(prof[i][0] - prof[i - 1][0], prof[i][1] - prof[i - 1][1]))
        quads, normals, uvs = [], [], []
        for i in range(len(prof) - 1):
            (ya, za), (yb, zb) = prof[i], prof[i + 1]
            q = [(x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb)]
            n = core.norm(core.newell(q))
            uv = [(x0 / t, w[i] / t), (x1 / t, w[i] / t), (x1 / t, w[i + 1] / t), (x0 / t, w[i + 1] / t)]
            quads += [q, q[::-1]]
            normals += [n, core.mul(n, -1.0)]
            uvs += [uv, uv[::-1]]
        s = sheet(quads, mat, normals, vis=(1,), uvs=uvs)
        s.finalize()
        s.wear = wear
        return s

    out = []
    for a, b in ((-yuki, -body_w), (body_w, yuki)):
        out.append(column(cx + a, cx + b, sleeve, [0.0, sleeve / 2, sleeve], True))
    for a, b in ((-body_w, 0.0), (0.0, body_w)):
        out.append(column(cx + a, cx + b, drop, [0.0, 0.24, sleeve, 0.90, drop], False))
    # the collar (eri): a pale band from each shoulder down to where the fronts cross, 3 mm proud of the front panel
    for sx in (-1, 1):
        p = [(cx + sx * 0.075, pole_y - 0.005), (cx + sx * 0.005, pole_y - 0.46)]
        lift = 0.003 if sx < 0 else 0.0045            # the right band lies over the left where they cross
        hw = 0.02
        q = [(p[0][0] - hw, p[0][1], rc + lift), (p[0][0] + hw, p[0][1], rc + lift),
             (p[1][0] + hw, p[1][1], zoff(0.46, drop, False) + lift),
             (p[1][0] - hw, p[1][1], zoff(0.46, drop, False) + lift)]
        n = core.norm(core.newell(q))
        if n[2] < 0:
            q, n = q[::-1], core.mul(n, -1.0)
        c = sheet([q], COLLAR[0], n, vis=(1,), uvs=[[(0.0, 0.0), (2 * hw / t, 0.0), (2 * hw / t, 0.46 / t),
                                                     (0.0, 0.46 / t)]])
        c.finalize()
        c.wear = COLLAR[1]
        out.append(c)
    # Res 2: the T as two flat two-sided quads
    t2 = []
    for x0, x1, dd in ((cx - yuki, cx + yuki, sleeve), (cx - body_w, cx + body_w, None)):
        y0, y1 = (pole_y + rc, pole_y - sleeve) if dd else (pole_y - sleeve, pole_y - drop)
        q = [(x0, y0, 0.0), (x1, y0, 0.0), (x1, y1, 0.0), (x0, y1, 0.0)]
        uv = [(x0 / t, 0.0), (x1 / t, 0.0), (x1 / t, (y0 - y1) / t), (x0 / t, (y0 - y1) / t)]
        t2 += [(q, (0.0, 0.0, 1.0), uv), (q[::-1], (0.0, 0.0, -1.0), uv[::-1])]
    s2 = sheet([a for a, _, _ in t2], mat, [b for _, b, _ in t2], vis=(2,), uvs=[c for _, _, c in t2])
    s2.finalize()
    s2.wear = wear
    out.append(s2)
    return out


def laundry(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    # FP2 (2026-10-01): ties and the net's strands at 2.5x: the loaded poles go up a class (net: medium)
    P = SPart("laundry_pole", budget={"load_net": "medium", "load_kaki": "box", "load_daikon": "box"}.get(kind, "small"),
              mass=15.0, bury=0.09)
    L = 3.64
    crossed = kind in ("crossed", "load_kaki", "load_daikon", "load_net")
    X = L / 2 - 0.25
    if crossed:
        y = CROSS_Y
        for sx in (-1, 1):
            add_all(P, stakes_crossed(sx * X, wear))
            P.add(col(sx * X - 0.05, sx * X + 0.05, 0.0, CROSS_Y, -0.55, 0.55, BAMBOO))
        pole_y = cross_seat()
    elif kind == "ab_down":
        y = 2.0
        add_all(P, post_forked(-X, wear="_w2"))
        lean = xfs(post_forked(X, wear="_w2"), rz=24.0, pivot=(X, 0.0, 0.0))
        add_all(P, lean)
        P.add(col(-X - 0.05, -X + 0.05, 0.0, 2.0, -0.05, 0.05))
        pole_y = fork_seat(y)
    else:
        y = 2.0
        for sx in (-1, 1):
            add_all(P, post_forked(sx * X, wear=wear))
            P.add(col(sx * X - 0.05, sx * X + 0.05, 0.0, 2.0, -0.05, 0.05))
        pole_y = fork_seat(y)
    if kind == "ab_down":
        # the pole slipped out of the leaning fork: it still rests in the standing fork's V at -X, its +x end on the
        # ground; it runs on 0.3 m past the seat
        seat = (-X, pole_y, 0.0)
        p1 = (X + 0.7, 0.025, 0.25)
        dv = core.norm(core.sub(p1, seat))
        p0 = core.sub(seat, core.mul(dv, 0.3))
        P.add(pole(p0, p1, POLE_R, BAMBOO, n=6, vis=(1, 2), wear="_w2"))
        m = grid_sheet(lambda u, v: (1.1 + 0.9 * u, 0.012 + 0.03 * math.sin(3 * u), -0.1 + 0.8 * v), 3, 2, KINARI,
                       vis=(1,), wear="_w2")
        P.add(m)
        P.add(litter(4, 0.8, 0.3, 0.8, sx=1.6))
    else:
        P.add(pole((-L / 2, pole_y, 0.0), (L / 2, pole_y, 0.0), 0.023, BAMBOO, n=6, vis=(1, 2), wear=wear))
    if kind == "load_cloth":
        # a kimono hung through its sleeves on the pole (the Edo way: the pole runs in one sleeve, across the shoulders
        # inside the garment and out of the other sleeve) + a plain cloth; one garment fallen on the ground
        add_all(P, kimono_hung(-0.62, pole_y))
        P.add(grid_sheet(lambda u, v: (0.25 + 0.8 * u, pole_y - 0.02 - 0.95 * v, 0.02 * math.sin(4 * v)), 2, 3, KINARI,
                         vis=(1,), wear="_w2"))
        P.add(grid_sheet(lambda u, v: (0.9 + 1.0 * u, 0.01 + 0.04 * math.sin(5 * u * v), 0.35 + 0.7 * v), 3, 2, KINARI,
                         vis=(1,), wear="_w2"))
    elif kind == "load_kaki":
        rr = random.Random(12)
        for i in range(7):
            x = -1.35 + i * 0.44
            top = (x, pole_y - 0.02, 0.0)
            bot = (x + rr.uniform(-0.02, 0.02), pole_y - 0.95, 0.0)
            add_all(P, rope_path([top, bot], 0.006, ROPE, n=3))          # FP2: ropekit (2.5x sides)
            nfr = 4 if i != 3 else 2          # one string snapped
            for k in range(nfr):
                yy = pole_y - 0.18 - k * 0.19
                fr = pole((bot[0], yy + 0.045, 0.0), (bot[0], yy - 0.045, 0.0), 0.035, BENGARA, n=4, vis=(1,),
                          r1=0.028, phase=rr.uniform(0, 1))
                fr.wear = "_w2"
                P.add(fr)
            P.add(W(x - 0.035, x + 0.035, pole_y - 0.95, pole_y - 0.1, -0.03, 0.03, BENGARA, vis=(2,)))
        for k in range(3):
            fr = pole((0.1 + k * 0.12, 0.03, 0.2), (0.16 + k * 0.12, 0.03, 0.26), 0.03, BENGARA, n=4, vis=(1,))
            fr.wear = "_w2"
            P.add(fr)
    elif kind == "load_daikon":
        rr = random.Random(13)
        for i in range(8):
            x = -1.35 + i * 0.38
            for sz in (-1, 1):
                a = (x, pole_y - 0.03, sz * 0.03)
                b = (x + rr.uniform(-0.04, 0.04), pole_y - 0.55 - rr.uniform(0, 0.1), sz * 0.06)
                d = pole(a, b, 0.032, PAPER, n=5, vis=(1,), r1=0.010, wear="_w2")
                P.add(d)
            add_all(P, rope_path([(x, pole_y - 0.03, -0.03), (x, pole_y + 0.025, 0.0)], 0.008, ROPE, n=3))   # FP2
            P.add(W(x - 0.03, x + 0.03, pole_y - 0.55, pole_y - 0.03, -0.05, 0.05, PAPER, vis=(2,)))
    elif kind == "load_net":
        # a small fishing net draped over the pole: strands in both directions, a few floats
        x0, x1 = -1.1, 0.9
        for k in range(8):
            x = x0 + (x1 - x0) * k / 7
            pts = [(x, pole_y - 0.02, 0.0), (x + 0.02, pole_y - 0.6, 0.05), (x + 0.05, pole_y - 1.25, 0.03)]
            add_all(P, rope_path(pts, 0.005, ROPE, n=3))
        for j in range(4):
            yy = pole_y - 0.3 - j * 0.3
            add_all(P, rope_path(sag((x0, yy, 0.03), (x1 + 0.05, yy, 0.03), 0.06, 3), 0.005, ROPE, n=3))
        for k in range(5):
            P.add(box(x0 + 0.3 + k * 0.35, x0 + 0.36 + k * 0.35, pole_y - 1.3, pole_y - 1.24, 0.0, 0.06, WOOD,
                      vis=(1,)))
        P.add(W(x0, x1, pole_y - 1.25, pole_y - 0.02, -0.004, 0.004, ROPE, vis=(2,)))
    ground(P, keep=-0.08)
    P.dim("pole", 3.64, L if kind != "ab_down" else L, tol=0.01)
    P.dim("fork_h", 2.0 if not crossed else 1.8, y, tol=0.1)
    P.extra["loads"] = kind
    return P


# ================================================================================================ tenbin
def basket(wear=None, vis=(1,), d=0.45, h=0.25, n=10, fill=None):
    r = d / 2
    out = [lathe([(r * 0.85, 0.0), (r, h), (r - 0.012, h), (r * 0.85 - 0.012, 0.03), (0.0, 0.03)], n, WEAVE,
                 vis=vis, wear=wear)]
    out.append(hoop(r, h - 0.015, 0.03, n, vis=vis, wear=wear))
    if fill:
        out.append(fill)
    return out


def load_ropes(cx, top_y, rim_y, r, pole_y, vis=(1,)):
    out = []
    for a in (0.3, 2.4, 4.5):
        p = (cx + r * math.cos(a), rim_y, r * math.sin(a))
        out += rope_path([p, (cx, pole_y, 0.0)], 0.006, ROPE, n=3, vis=vis)    # FP2: ropekit (2.5x sides)
    return out


def tenbin(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("tenbin", budget="small", mass=12.0)
    X = 0.75
    Lp = 1.70
    if kind in ("baskets", "buckets", "boxes"):
        tops = []
        for sx in (-1, 1):
            if kind == "baskets":
                ss = basket(fill=leaves(20 + sx, 0.0, 0.0, 0.17, 0.17, wear="_w2", mat=LEAF))
                top, rim_r = 0.25, 0.225
                P.add(lathe([(0.19, 0.0), (0.225, 0.25), (0.0, 0.22)], 5, WEAVE, vis=(2,), smooth=False))
            elif kind == "buckets":
                ss = ninai(lod2=True)
                top, rim_r = 0.62, 0.19
            else:
                ss = [W(-0.2, 0.2, 0.0, 0.25, -0.15, 0.15, DARK, vis=(1, 2)),
                      W(-0.19, 0.19, 0.25, 0.47, -0.14, 0.14, DARK, vis=(1, 2)),
                      W(-0.205, 0.205, 0.11, 0.13, -0.155, 0.155, ROPE, vis=(1,)),
                      W(-0.01, 0.01, 0.0, 0.475, -0.155, 0.155, ROPE, vis=(1,))]
                top, rim_r = 0.47, 0.15
            ss = xfs(ss, t=(sx * X, 0.0, 0.0))
            if kind == "baskets":
                P.solids = [s if 2 not in s.vis or s.bbox()[1] - s.bbox()[0] > 0.5 else s for s in P.solids]
                P.solids[-1] = xf(P.solids[-1], t=(sx * X, 0.0, 0.0))
            add_all(P, ss)
            P.add(cyl_col(rim_r, 0.0, top, n=6, cx=sx * X))
            tops.append(top)
        py = max(tops) + 0.03
        # the pole rests across both loads; the ropes lie slack over the rims
        P.add(beam((-Lp / 2, py, 0.0), (Lp / 2, py, 0.0), 0.05, 0.03, WOOD, vis=(1, 2)))
        for sx in (-1, 1):
            if kind != "boxes":
                add_all(P, load_ropes(sx * X, py, tops[0] - 0.02, rim_r, py))
        P.dim("pole", 1.70, Lp, tol=0.02)
        P.dim("load_d", {"baskets": 0.45, "buckets": 0.38, "boxes": 0.40}[kind], 2 * rim_r if kind != "boxes" else 0.40,
              tol=0.01)
    elif kind == "leaning":
        P.anchor, P.wall_gap = "wall", 0.03
        top_y = 1.62
        P.add(beam((0.10, 0.0, 0.40), (0.0, top_y, 0.045), 0.05, 0.03, WOOD, vis=(1, 2), up=(0.0, 0.0, 1.0)))
        P.add(col_solid(beam((0.10, 0.0, 0.40), (0.0, top_y, 0.045), 0.05, 0.03, WOOD)))
        for sx in (-1, 1):
            ss = basket()
            add_all(P, xfs(ss, t=(sx * 0.5, 0.0, 0.33)))
            P.add(lathe([(0.19, 0.0), (0.225, 0.25), (0.0, 0.22)], 5, WEAVE, vis=(2,), smooth=False))
            P.solids[-1] = xf(P.solids[-1], t=(sx * 0.5, 0.0, 0.33))
            P.add(cyl_col(0.225, 0.0, 0.25, n=6, cx=sx * 0.5, cz=0.33))
            # the ropes gathered and hooked on the pole
            add_all(P, rope_path([(sx * 0.5, 0.24, 0.33 - 0.2), (sx * 0.2, 0.9, 0.2), (0.04, 1.4, 0.10)], 0.006))
        ground(P)
        P.dim("pole", 1.70, math.dist((0.10, 0.0, 0.40), (0.0, top_y, 0.045)) + 0.06, tol=0.06)
    else:   # ab_dropped: pole on the ground, one basket overturned, goods spilled and rotted
        P.add(beam((-0.8, 0.03, 0.1), (0.85, 0.03, -0.12), 0.05, 0.03, WOOD, vis=(1, 2), wear="_w2"))
        P.add(col_solid(beam((-0.8, 0.03, 0.1), (0.85, 0.03, -0.12), 0.05, 0.03, WOOD)))
        ss = basket(wear="_w2", fill=leaves(31, 0.0, 0.0, 0.17, 0.17, wear="_w2"))
        add_all(P, xfs(ss, t=(-0.75, 0.0, 0.35)))
        P.add(cyl_col(0.225, 0.0, 0.25, n=6, cx=-0.75, cz=0.35))
        ov = basket(wear="_w2")
        ov = xfs(ov, rz=180.0, t=(0.0, 0.25, 0.0))
        ov = xfs(ov, rz=12.0, t=(0.9, 0.02, 0.35))
        add_all(P, ov)
        P.add(xf(cyl_col(0.225, 0.0, 0.25, n=6), rz=12.0, t=(0.9, 0.0, 0.35)))
        P.add(bits_mound(41, 1.15, 0.55, 0.30))
        add_all(P, rope_path([(-0.6, 0.03, 0.2), (-0.4, 0.02, 0.5), (-0.55, 0.2, 0.35)], 0.006, wear="_w2"))
        P.add(litter(33, 0.8, 0.5, 0.7, sx=1.5))
        P.add(W(-0.9, 0.9, 0.0, 0.22, -0.1, 0.55, WEAVE, vis=(2,)))
        ground(P)
        P.dim("pole", 1.70, math.dist((-0.8, 0.03, 0.1), (0.85, 0.03, -0.12)) + 0.02, tol=0.05)
    return P


def bits_mound(seed, cx, cz, r0):
    """Rotted goods spilled from a basket: a low dark mound."""
    return skit.mound(seed, cx, cz, r0, 0.05, LEAF, sx=1.3, wear="_w2", vis=(1,))


# ================================================================================================ handcart
def cart_parts(small=False, wear=None, slats_missing=(), no_wheels=False):
    """Daihachi-guruma (or niguruma) in its own frame: bed along z (+z = handles), axle at z = 0, level, axle height
    = wheel radius. Returns (res1, res2, res3, cols, info)."""
    if small:
        BL, BW, WR, HND = 1.50, 0.60, 0.375, 0.70
    else:
        BL, BW, WR, HND = 2.42, 0.76, 0.53, 0.90
    zr = -BL * 0.52                           # bed rear end
    zf = zr + BL                              # bed front end; rails continue HND as handles
    yb = WR + 0.10                            # rail underside (the bed rides on the axle bolsters)
    rh, rw = 0.10, 0.075
    r1, r2, r3, cols = [], [], [], []
    for sx in (-1, 1):
        x = sx * (BW / 2 - rw / 2)
        r1.append(W(x - rw / 2, x + rw / 2, yb, yb + rh, zr, zf + HND - 0.05, WOOD, vis=(1, 2)))
        r1.append(W(x - rw / 2 + 0.01, x + rw / 2 - 0.01, yb + 0.01, yb + rh - 0.01, zf + HND - 0.05, zf + HND,
                    WOOD, vis=(1,)))
        r3.append(W(x - rw / 2, x + rw / 2, yb, yb + rh, zr, zf + HND, WOOD, vis=(3,)))
    # handle cross bar and 5 cross members
    r1.append(pole((-BW / 2 - 0.04, yb + 0.05, zf + HND - 0.05), (BW / 2 + 0.04, yb + 0.05, zf + HND - 0.05), 0.025,
                   WOOD, n=6, vis=(1, 2)))
    for k in range(5):
        z = zr + 0.08 + (BL - 0.16) * k / 4
        r1.append(W(-BW / 2 + rw, BW / 2 - rw, yb + 0.02, yb + rh - 0.02, z - 0.04, z + 0.04, WOOD, vis=(1,)))
    # deck slats along z
    ns = 5
    sw = (BW - 2 * rw) / ns
    for k in range(ns):
        if k in slats_missing:
            continue
        x0 = -BW / 2 + rw + k * sw + 0.006
        r1.append(W(x0, x0 + sw - 0.012, yb + rh - 0.02, yb + rh + 0.005, zr + 0.02, zf - 0.02, WOOD, vis=(1,)))
    r2.append(W(-BW / 2 + rw, BW / 2 - rw, yb + rh - 0.03, yb + rh, zr, zf, WOOD, vis=(2,)))
    r3.append(W(-BW / 2 + rw, BW / 2 - rw, yb + rh - 0.03, yb + rh, zr, zf, WOOD, vis=(3,)))
    # axle bolsters + axle
    for sx in (-1, 1):
        r1.append(W(sx * (BW / 2) - 0.05, sx * (BW / 2) + 0.05, WR - 0.02, yb, -0.09, 0.09, WOOD, vis=(1, 2)))
    r1.append(pole((-BW / 2 - 0.20, WR, 0.0), (BW / 2 + 0.20, WR, 0.0), 0.03, WOOD, n=6, vis=(1,)))
    wx = BW / 2 + 0.11
    cols.append(col(-BW / 2, BW / 2, yb, yb + rh, zr, zf + HND))
    for sx in (-1, 1):
        cols.append(col(sx * (BW / 2) - 0.05, sx * (BW / 2) + 0.05, WR - 0.02, yb, -0.09, 0.09))
    wheels = []
    if not no_wheels:
        for sx in (-1, 1):
            wl = spoked_wheel(WR, 0.07, 0.09 if not small else 0.07, 12 if not small else 10, vis=(1,), n=16,
                              wear=wear)
            wheels.append((sx, xfs(wl, t=(sx * wx, WR, 0.0))))
            r2.append(xf(wheel_lod(WR, 0.07, vis=(2,), n=10), t=(sx * wx, WR, 0.0)))
            r3.append(xf(wheel_lod(WR, 0.07, vis=(3,), n=6), t=(sx * wx, WR, 0.0)))
    info = {"BL": BL, "BW": BW, "WR": WR, "HND": HND, "zr": zr, "zf": zf, "yb": yb, "rh": rh, "wx": wx,
            "deck_y": yb + rh + 0.005}
    return r1, r2, r3, cols, wheels, info


def wheel_col(sx, info):
    c = lcyl("x", info["WR"], 0.0, info["WR"], -0.04, 0.04, WOOD, n=8, vis=(), geo=True, view=True, fire=True)
    c = xf(c, t=(sx * info["wx"], 0.0, 0.0))
    c.wheelcol = True
    return c


def handcart(kind):
    small = kind == "small"
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("handcart", budget="medium", res3=True, mass=90.0 if not small else 45.0, wear=wear or "_w1")
    missing = {"ab_wreck": (1, 3), "ab_broken": (2,)}.get(kind, ())
    r1, r2, r3, cols, wheels, I = cart_parts(small, wear, slats_missing=missing)
    for s in r1 + r2 + r3:
        if wear:
            s.wear = wear
    body = r1 + r2 + r3
    for sx, wl in wheels:
        body += wl
    cols += [wheel_col(sx, I) for sx, _ in wheels]
    load = []
    if kind == "load_bales":
        for i, (x, z, yy) in enumerate(((-0.2, 0.55, 0.0), (0.2, 0.55, 0.0), (-0.2, -0.3, 0.0), (0.2, -0.3, 0.0),
                                        (0.0, 0.12, 0.34))):
            ss = S.tawara_bale(n=6, segs="lo", bands=1, rope=ROPE)
            load += xfs(ss, ry=90.0, t=(x, I["deck_y"] + yy, z))
        load.append(W(-0.4, 0.4, I["deck_y"], I["deck_y"] + 0.40, -0.68, 0.93, TAWARA, vis=(2,)))
        load.append(W(-0.4, 0.4, I["deck_y"], I["deck_y"] + 0.40, -0.68, 0.93, TAWARA, vis=(3,)))
        for z in (0.55, -0.3):
            load += rope_path([(-0.41, I["deck_y"], z), (-0.41, I["deck_y"] + 0.42, z), (0.41, I["deck_y"] + 0.42, z),
                               (0.41, I["deck_y"], z)], 0.008)
        cols.append(col(-0.4, 0.4, I["deck_y"], I["deck_y"] + 0.40, -0.68, 0.93, TAWARA))
    elif kind == "load_barrels":
        for i, z in enumerate((0.55, -0.25)):
            ss, top = taru(lid=True, stone=False, n=10, lod2=True)
            load += xfs(ss, t=(0.0, I["deck_y"], z))
            cols.append(cyl_col(0.275, I["deck_y"], I["deck_y"] + 0.63, n=8, cz=z))
            load += rope_path([(-0.3, I["deck_y"], z), (-0.29, I["deck_y"] + 0.4, z), (0.29, I["deck_y"] + 0.4, z),
                               (0.3, I["deck_y"], z)], 0.008)
        load.append(W(-0.27, 0.27, I["deck_y"], I["deck_y"] + 0.62, -0.5, 0.8, WOOD, vis=(3,)))
    body += load
    allss = body + cols
    # park: 'handles down' - pitch the level cart about the axle until the handle bar touches the ground
    zh = I["zf"] + I["HND"] - 0.05
    tilt = math.degrees(math.atan2(I["yb"] + 0.02, zh))
    if kind in ("empty", "load_bales", "load_barrels", "small"):
        allss = xfs(allss, rx=tilt, pivot=(0.0, I["WR"], 0.0))
    elif kind == "ab_tipped":
        allss = xfs(allss, rx=tilt, pivot=(0.0, I["WR"], 0.0))
        allss = xfs(allss, rz=78.0, pivot=(I["wx"] + 0.04, 0.0, 0.0))
        rr = random.Random(4)
        for i in range(3):
            ss = S.tawara_bale(n=6, segs="lo", bands=1, rope=ROPE, wear="_w2")
            allss += xfs(ss, ry=rr.uniform(0, 180), t=(1.35 + i * 0.1, 0.0, -0.6 + i * 0.55))
            allss.append(col_solid(S.tawara_col(1.35 + i * 0.1, 0.0, -0.6 + i * 0.55, 0.0, n=6)))
        allss.append(skit.mound(5, 1.7, 0.3, 0.35, 0.05, PAPER, sx=1.3, wear="_w2", vis=(1,)))
    elif kind == "ab_broken":
        # the right wheel broke: its rim lies flat, the bed rests on the ground at the right rear
        keep = [s for s in allss if not (s.bbox()[0] > I["wx"] - 0.1 and s.bbox()[0] < I["wx"] + 0.2 and
                                         s.bbox()[1] - s.bbox()[0] < 0.2 and not s.geo and s.bbox()[3] > 0.9)]
        keep = [s for s in allss if not any(s is q for _, wl in wheels if _ == 1 for q in wl)]
        keep = [s for s in keep if not (s.geo and s.bbox()[0] > I["BW"] / 2)]
        keep = [s for s in keep if not (not s.geo and 2 in s.vis and s.bbox()[0] > I["BW"] / 2 + 0.05)]
        keep = [s for s in keep if not (not s.geo and 3 in s.vis and s.bbox()[0] > I["BW"] / 2 + 0.05)]
        keep = xfs(keep, rx=tilt * 0.5, pivot=(0.0, I["WR"], 0.0))
        keep = xfs(keep, rz=-math.degrees(math.atan2(I["yb"] - 0.02, I["wx"] * 2)), pivot=(-I["wx"], 0.0, 0.0))
        allss = keep
        wl = spoked_wheel(I["WR"], 0.07, 0.09, 12, vis=(1,), wear="_w2")
        wl = [s for i, s in enumerate(wl) if i < 3 or i % 3 != 0]          # four spokes gone
        wl = xfs(wl, rz=88.0, t=(I["wx"] + 0.85, 0.04, -0.4))
        allss += wl
        allss.append(xf(wheel_lod(I["WR"], 0.07, vis=(2,), n=10), rz=88.0, t=(I["wx"] + 0.85, 0.04, -0.4)))
        allss.append(xf(xf(wheel_col(0, I), t=(0.0, -I["WR"], 0.0)), rz=88.0, t=(I["wx"] + 0.85, 0.04, -0.4)))
        for i in range(3):
            sp = W(-0.011, 0.011, 0.0, 0.022, -0.2, 0.2, WOOD, vis=(1,))
            sp.wear = "_w2"
            allss.append(xf(sp, ry=40 + i * 50, t=(I["wx"] + 0.3 + i * 0.2, 0.0, 0.3)))
    elif kind == "ab_wreck":
        # the worst: wheels off (one leaning on the bed, one flat), bed on the ground, slats gone, a rail split
        keep = [s for s in allss if not any(s is q for _, wl in wheels for q in wl)]
        keep = [s for s in keep if not getattr(s, "wheelcol", False)]
        keep = [s for s in keep if not (not s.geo and (2 in s.vis or 3 in s.vis) and abs(s.center[0]) > I["BW"] / 2)]
        keep = [s for s in keep if s.bbox()[3] > I["yb"] + 0.001]          # bolsters and axle gone
        keep = xfs(keep, rx=-3.0, t=(0.0, -I["yb"], 0.0))
        allss = keep
        w1 = spoked_wheel(I["WR"], 0.07, 0.09, 12, vis=(1,), wear="_w2")
        allss += xfs(w1, rz=90.0, t=(-1.15, 0.04, 0.2))
        allss.append(xf(wheel_lod(I["WR"], 0.07, vis=(2,), n=10), rz=90.0, t=(-1.15, 0.04, 0.2)))
        allss.append(xf(xf(wheel_col(0, I), t=(0.0, -I["WR"], 0.0)), rz=90.0, t=(-1.15, 0.04, 0.2)))
        w2 = spoked_wheel(I["WR"], 0.07, 0.09, 12, vis=(1,), wear="_w2")
        w2 = [s for i, s in enumerate(w2) if i < 3 or i % 4 != 1]
        allss += xfs(w2, rz=-14.0, t=(I["BW"] / 2 + 0.2, I["WR"] - 0.02, -0.6))
        allss.append(xf(wheel_lod(I["WR"], 0.07, vis=(2,), n=10), rz=-14.0, t=(I["BW"] / 2 + 0.2, I["WR"] - 0.02, -0.6)))
        allss.append(xf(xf(wheel_col(0, I), t=(0.0, -I["WR"], 0.0)), rz=-14.0, t=(I["BW"] / 2 + 0.2, I["WR"] - 0.02, -0.6)))
        allss.append(litter(8, 0.0, 0.0, 1.2, sx=0.8, sz=1.6))
    add_all(P, allss)
    ground(P)
    if kind in ("empty", "small", "load_bales", "load_barrels"):
        P.add(litter(2, 0.0, -0.5, 0.8, sx=0.9, sz=1.4, wear="_w1"))
    P.dim("bed_L", 2.42 if not small else 1.50, I["BL"], tol=0.01)
    P.dim("bed_W", 0.76 if not small else 0.60, I["BW"], tol=0.01)
    P.dim("wheel_d", 1.06 if not small else 0.75, 2 * I["WR"], tol=0.01)
    P.dim("handles", 0.9 if not small else 0.7, I["HND"], tol=0.01)
    P.extra["disrepair"] = {"empty": 1, "small": 1, "load_bales": 1, "load_barrels": 1, "ab_tipped": 2,
                            "ab_broken": 3, "ab_wreck": 4}[kind]
    return P


# ================================================================================================ registry
PROPS = [
    {"id": "jp_s_oke", "cat": "yard", "notes": ["one stave family: yards, inn doors, graves, wells, fire corners; no metal "
                                                "hoops (split bamboo); open vessels hold leaf litter, never water"],
     "models": [
         M("jp_s_oke_tarai", "tarai", "intact", "Wash tub (tarai), leaves inside", lambda: oke("tarai")),
         M("jp_s_oke_teoke", "teoke", "intact", "Hand bucket (teoke)", lambda: oke("teoke")),
         M("jp_s_oke_ninai", "ninai", "intact", "Carrying bucket (ninai-oke)", lambda: oke("ninai")),
         M("jp_s_oke_taru_lid", "taru", "intact", "Pickle barrel with lid and stone", lambda: oke("taru_lid")),
         M("jp_s_oke_stake", "stake", "intact", "Bucket upside down on a stake (oke-hoshi)", lambda: oke("stake")),
         M("jp_s_oke_ab_tipped", "taru", "abandoned", "Barrel tipped over, hoop sprung", lambda: oke("ab_tipped")),
         M("jp_s_oke_ab_staves", "tarai", "abandoned", "Tub collapsed into staves", lambda: oke("ab_staves")),
     ]},
    {"id": "jp_s_fire_tub", "cat": "water", "notes": ["corner tub at crossings only (never one per house, 1789+ trap); "
                                                      "not a water source (leaves and dark rainwater)"],
     "models": [
         M("jp_s_fire_tub_full", "full", "intact", "Corner fire tub with a bucket pyramid", lambda: fire_tub("full")),
         M("jp_s_fire_tub_open", "open", "abandoned", "Fire tub, lid gone, three buckets down", lambda: fire_tub("open")),
         M("jp_s_fire_tub_eave", "eave", "intact", "Fire bucket on an eave peg (building proxy)", lambda: fire_tub("eave")),
         M("jp_s_fire_tub_rural", "rural", "intact", "Rain barrel under an eave (rural)", lambda: fire_tub("rural")),
         M("jp_s_fire_tub_ab_scattered", "full", "abandoned", "Fire tub, pyramid collapsed, buckets scattered",
           lambda: fire_tub("ab_scattered")),
     ]},
    {"id": "jp_s_firewood_stack", "cat": "yard", "notes": ["wall stacks: wall plane z = 0, stack 5 cm off it, 1 billet "
                                                           "(0.33 m) deep; half-ken grid"],
     "models": [
         M("jp_s_firewood_stack_wall_1ken_h120", "wall_1ken_h120", "intact", "Firewood stack on a wall, 1 ken x 1.2 m",
           lambda: firewood("wall_1ken_h120")),
         M("jp_s_firewood_stack_wall_1ken_h180", "wall_1ken_h180", "intact", "Firewood stack on a wall, 1 ken x 1.8 m",
           lambda: firewood("wall_1ken_h180")),
         M("jp_s_firewood_stack_half", "half", "intact", "Firewood stack end piece, half ken, stepped",
           lambda: firewood("half")),
         M("jp_s_firewood_stack_free_posts", "free_posts", "intact", "Firewood stack between two stakes, board cap",
           lambda: firewood("free_posts")),
         M("jp_s_firewood_stack_bundle", "bundle", "intact", "Brushwood bundle (soda) leaning on a wall",
           lambda: firewood("bundle")),
         M("jp_s_firewood_stack_ab_collapsed", "wall_1ken_h120", "abandoned", "Firewood stack, one end slumped, spilled",
           lambda: firewood("ab_collapsed")),
     ]},
    {"id": "jp_s_bench", "cat": "street", "notes": ["seat top = Roadway + loot surface (bench tops are natural loot "
                                                    "surfaces if outdoor loot is wanted later)"],
     "models": [
         M("jp_s_bench_1ken", "1ken", "intact", "Bench (endai), 1 ken", lambda: bench("1ken")),
         M("jp_s_bench_long", "long", "intact", "Tea-stand bench, 1.5 ken", lambda: bench("long")),
         M("jp_s_bench_mat", "1ken", "intact", "Bench with a rotted straw mat", lambda: bench("mat")),
         M("jp_s_bench_ab_tipped", "1ken", "abandoned", "Bench tipped on its side", lambda: bench("ab_tipped")),
         M("jp_s_bench_ab_broken", "1ken", "abandoned", "Bench, one leg frame collapsed", lambda: bench("ab_broken")),
     ]},
    {"id": "jp_s_laundry_pole", "cat": "yard", "notes": ["loads are whole models (pole + posts + load) so one "
                                                         "placement dresses a yard"],
     "models": [
         M("jp_s_laundry_pole_forked", "forked", "intact", "Drying pole on forked posts", lambda: laundry("forked")),
         M("jp_s_laundry_pole_crossed", "crossed", "intact", "Drying pole on crossed stakes", lambda: laundry("crossed")),
         M("jp_s_laundry_pole_load_cloth", "forked", "abandoned", "Drying pole, faded kimono, one cloth fallen",
           lambda: laundry("load_cloth")),
         M("jp_s_laundry_pole_load_kaki", "crossed", "abandoned", "Persimmons dried black on strings (autumn)",
           lambda: laundry("load_kaki")),
         M("jp_s_laundry_pole_load_daikon", "crossed", "abandoned", "Daikon hung in pairs, shrivelled (autumn)",
           lambda: laundry("load_daikon")),
         M("jp_s_laundry_pole_load_net", "crossed", "intact", "A small net draped on the pole (fishing village)",
           lambda: laundry("load_net")),
         M("jp_s_laundry_pole_ab_down", "forked", "abandoned", "Drying pole down, one post leaning",
           lambda: laundry("ab_down")),
     ]},
    {"id": "jp_s_tenbin", "cat": "yard", "models": [
        M("jp_s_tenbin_baskets", "baskets", "intact", "Shoulder pole with two baskets", lambda: tenbin("baskets")),
        M("jp_s_tenbin_buckets", "buckets", "intact", "Shoulder pole with two buckets", lambda: tenbin("buckets")),
        M("jp_s_tenbin_boxes", "boxes", "intact", "Shoulder pole with peddler's boxes", lambda: tenbin("boxes")),
        M("jp_s_tenbin_leaning", "leaning", "intact", "Shoulder pole leaning on a wall", lambda: tenbin("leaning")),
        M("jp_s_tenbin_ab_dropped", "baskets", "abandoned", "Shoulder pole dropped, basket overturned",
          lambda: tenbin("ab_dropped")),
    ]},
    {"id": "jp_s_handcart", "cat": "yard", "notes": ["G1: several variants at increasing disrepair (sidecar "
                                                     "'disrepair' 1-4): parked (1), tipped (2), broken wheel (3), wreck "
                                                     "(4); the DayZ car-wreck role: cover in open streets"],
     "models": [
         M("jp_s_handcart_empty", "daihachi", "intact", "Handcart (daihachi-guruma), handles down",
           lambda: handcart("empty")),
         M("jp_s_handcart_load_bales", "daihachi", "intact", "Handcart with rice bales roped on",
           lambda: handcart("load_bales")),
         M("jp_s_handcart_load_barrels", "daihachi", "intact", "Handcart with barrels", lambda: handcart("load_barrels")),
         M("jp_s_handcart_small", "niguruma", "intact", "Small cart (niguruma)", lambda: handcart("small")),
         M("jp_s_handcart_ab_tipped", "daihachi", "abandoned", "Handcart tipped on its side, load spilled",
           lambda: handcart("ab_tipped")),
         M("jp_s_handcart_ab_broken", "daihachi", "abandoned", "Handcart with a broken wheel, bed down",
           lambda: handcart("ab_broken")),
         M("jp_s_handcart_ab_wreck", "daihachi", "abandoned", "Handcart wreck, wheels off, slats gone",
           lambda: handcart("ab_wreck")),
     ]},
]
