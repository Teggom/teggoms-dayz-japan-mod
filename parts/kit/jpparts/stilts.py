"""Raised floors on posts and stone platforms (W2P1, 2026-10-01): jp_p_found_stilts (PARTS_GAP_AUDIT §3 part 45) and
jp_p_found_kidan (part 12, the village subset: bell-tower and hall platforms with a stone flight). Period form and
choices: parts/W2P1_NOTES.md.

stilts.platform(part, W, D, drop, kind): the floor of a W x D body standing `drop` over grade on underfloor posts
(yuka-zuka) on stones, with sleepers (obiki), two rows of underfloor nuki and the yukashita treatment by kind:
  'honden'    open beneath (the posts and nuki show; a honden's floor ~1 m up)
  'hall'      boarded skirt (vertical boards with vent gaps) between the perimeter posts (haiden, village halls)
  'ratguard'  rat guards (nezumi-gaeshi): square boards round every post under the sleepers (stores on posts)
Frame: body x 0..W, z 0 (front wall line) .. -D; y 0 = the floor top; grade y = -drop. The floor reaches the posts'
outer faces (x -0.06 .. W + 0.06, z 0.06 .. -D - 0.06), so koran.en_deck runs on from z 0.06 / x -0.06 without
overlap. The shell's wall posts start at y 0. A Geometry-only block under the floor keeps players out from under it.

stilts.kidan(part, W, D, h, steps): a cut-stone platform (rule 3: individual stones, never a smooth plinth): kerb stones
(katsura-ishi) round the top, facing slabs, a base course, an earth top; stone flights with hidden ramps. Frame: x 0..W,
z 0 (front edge) .. -D; y 0 = the platform top; grade -h.
"""
import math

from .core import Part, box, prism, stone, KEN, HALF, QK, POST, rng_for
from .shapes import board_run, rough_block
from . import floors as FL
from . import koran as KR

MAT = "wood_weathered"


def _nodes(a0, a1, step):
    n = max(1, int(round((a1 - a0) / step)))
    return [a0 + (a1 - a0) * k / n for k in range(n + 1)]


def platform(part, W, D, drop=1.0, kind="honden", step=HALF, mat=MAT, floor=True, along_x=False):
    """See the module docstring. Returns dict(posts=[(x, z)], floor_rect)."""
    rng = rng_for(part.name + "stilts%s" % kind)
    e = POST / 2
    fx0, fx1, fz0, fz1 = -e, W + e, -D - e, e
    if floor:
        part.merge(FL.boards("stilts_floor", fx0, fx1, fz0, fz1, 0.0, along_x=along_x))
    y_sl = -0.15                                       # floor slab underside (floors.boards: 0.15 support block)
    ob0, ob1 = y_sl - 0.13, y_sl - 0.004                # sleepers (obiki) under the floor
    zs = _nodes(-D, 0.0, step)
    xs = _nodes(0.0, W, step)
    posts = []
    for z in zs:
        part.add(box(fx0 + 0.01, fx1 - 0.01, ob0, ob1, z - 0.055, z + 0.055, mat, vis=(1, 2), tag="obiki",
                     grain="long"))
    for x in xs:
        for z in zs:
            edge = x in (xs[0], xs[-1]) or z in (zs[0], zs[-1])
            if not edge and kind != "ratguard" and (round(x / KEN, 3) % 1 or round(z / KEN, 3) % 1):
                continue                                # inner posts on the ken grid only (fewer faces)
            sz = 0.105
            part.add(stone(rng, x, z, 0.26, 0.24, 0.12, -drop + 0.07, "stone_field", bury=0.06, vis=(1, 2),
                           tag="tsuka_stone"))
            part.add(box(x - sz / 2, x + sz / 2, -drop + 0.07, ob0, z - sz / 2, z + sz / 2, mat,
                         vis=(1, 2, 3) if edge else (1, 2), tag="yukazuka", grain="long"))
            posts.append((x, z))
            if kind == "ratguard":
                yg = ob0 - 0.10
                part.add(box(x - 0.24, x + 0.24, yg - 0.025, yg, z - 0.24, z + 0.24, mat, vis=(1, 2), tag="nezumigaeshi"))
    # underfloor nuki: two rows through the perimeter posts (x runs on the front / back lines, z runs on the sides)
    if drop > 0.5:
        for k, yy in enumerate((-drop * 0.38, -drop * 0.72)):
            if yy > ob0 - 0.12:
                continue
            for z in (zs[0], zs[-1]):
                part.add(box(-0.08, W + 0.08, yy, yy + 0.09, z - 0.016, z + 0.016, mat, vis=(1,), tag="nuki"))
            for x in (xs[0], xs[-1]):
                part.add(box(x - 0.016 - 0.004, x + 0.016 - 0.004, yy + 0.095, yy + 0.185, -D - 0.08, 0.08, mat,
                             vis=(1,), tag="nuki"))
    # the block nobody crawls into (Geometry only)
    part.add(box(fx0 + 0.02, fx1 - 0.02, -drop, y_sl - 0.004, fz0 + 0.02, fz1 - 0.02, mat, vis=(), geo=True,
                 view=False, fire=None, tag="underfloor_block"))
    if kind == "hall":
        # boarded skirt between the perimeter posts, 1 cm outside the post faces, vent gaps every other bay
        zf = e + 0.012
        for side in ("front", "back", "left", "right"):
            if side in ("front", "back"):
                z = zf if side == "front" else -D - zf
                bs = board_run(0.0, W, -drop + 0.03, ob1, min(z, z + (0.015 if side == "front" else -0.015)),
                               max(z, z + (0.015 if side == "front" else -0.015)), rng, 0.18, 0.26, mat, gap=0.012,
                               vis=(1, 2), tag="skirt_board")
            else:
                x = -zf if side == "left" else W + zf
                bs = []
                zz = -D
                while zz < 0.0 - 1e-3:
                    ze = min(0.0, zz + rng.uniform(0.18, 0.26))
                    bs.append(box(min(x, x + (-0.015 if side == "left" else 0.015)),
                                  max(x, x + (-0.015 if side == "left" else 0.015)), -drop + 0.03, ob1, zz + 0.006,
                                  ze - 0.006, mat, vis=(1, 2), tag="skirt_board", uvoff=(rng.random(), rng.random())))
                    zz = ze
            part.extend(bs)
        for (a, b, c, d) in ((0.0, W, zf, zf + 0.015), (0.0, W, -D - zf - 0.015, -D - zf),
                             (-zf - 0.015, -zf, -D, 0.0), (W + zf, W + zf + 0.015, -D, 0.0)):
            part.add(box(a, b, -drop + 0.03, ob1, c, d, mat, vis=(3,), tag="skirt_lod"))
    elif kind in ("honden", "ratguard"):
        # open beneath: no void board (the period look); the far LOD keeps the corner posts (vis 3 above)
        pass
    return {"posts": posts, "floor_rect": (fx0, fx1, fz0, fz1), "drop": drop}


# ------------------------------------------------------------------------------------------------ kidan
def kidan(part, W, D, h=0.60, steps=(("front", None, 1.30),), top="earth", angle=34.0, kerb_w=0.30):
    """Cut-stone platform W x D, top y 0, grade -h (see the module docstring). steps: (side 'front' | 'back' |
    'left' | 'right', centre along that side (None = middle), flight width). Returns {'flights': [...]}."""
    rng = rng_for(part.name + "kidan")
    sm = "stone_cut"
    part.add(box(0.0, W, -h - 0.10, 0.0, -D, 0.0, sm, vis=(), geo=True, view=True, fire=True,
                 tag="kidan_geo"))
    part.road([(0.0, 0.0, 0.0), (W, 0.0, 0.0), (W, 0.0, -D), (0.0, 0.0, -D)], "stone_ext")
    # earth top inside the kerb, 1 cm under the kerb tops
    k = kerb_w
    part.add(box(k - 0.01, W - k + 0.01, -0.12, -0.01, -D + k - 0.01, -k + 0.01,
                 "ground_earth_bare" if top == "earth" else sm, vis=(1, 2), tag="kidan_top"))
    part.add(box(-0.01, W + 0.01, -h - 0.06, 0.0, -D - 0.01, 0.01, {"top": "ground_earth_bare" if top == "earth" else sm,
                                                                    "default": sm}, vis=(3,), tag="kidan_lod"))
    flights = []
    gaps = {}
    for side, c, w in steps:
        L = W if side in ("front", "back") else D
        cc = L / 2 if c is None else c
        gaps.setdefault(side, []).append((cc - w / 2 - 0.10, cc + w / 2 + 0.10))
    # kerb stones along each edge (individual blocks, small joints), facing slabs under them, a base course
    for side in ("front", "back", "left", "right"):
        L = W if side in ("front", "back") else D
        # the front / back runs take the corners; the side runs fit between them (no overlapping stones)
        s0, s1 = (0.0, L) if side in ("front", "back") else (k, L - k)
        s = s0
        L = s1
        while s < L - 1e-3:
            e = min(L, s + rng.uniform(0.62, 0.95))
            if L - e < 0.30:
                e = L
            _edge_block(part, rng, side, W, D, s + 0.004, e - 0.004, -0.16, 0.0, 0.0, k, sm, "kerb")
            fa, fb = s + 0.004, e - 0.004
            if side in ("left", "right"):
                fa, fb = max(fa, 0.20), min(fb, (D - 0.20))
            if fb - fa > 0.05:
                _edge_block(part, rng, side, W, D, fa, fb, -h + 0.06, -0.16 - 0.004, 0.025, 0.17, sm, "facing")
            s = e
        ba, bb = (-0.04, (W if side in ("front", "back") else D) + 0.04) if side in ("front", "back") else (0.20, D - 0.20)
        _edge_block(part, rng, side, W, D, ba, bb, -h - 0.06, -h + 0.06 - 0.004, -0.04, 0.24, sm, "base_course",
                    whole=True)
    # flights
    for side, c, w in steps:
        flights.append(_flight(part, rng, side, W, D, c, w, h, angle, sm))
    return {"flights": flights}


def _edge_block(part, rng, side, W, D, a, b, y0, y1, out, depth, sm, tag, whole=False):
    """A block along one edge: a..b along the edge, from `out` m outside the edge line inward by depth (out < 0 =
    proud of the edge)."""
    if side == "front":
        x0, x1, z0, z1 = a, b, -depth - out, -out
    elif side == "back":
        x0, x1, z0, z1 = W - b, W - a, -D + out, -D + out + depth
    elif side == "left":
        x0, x1, z0, z1 = out, out + depth, -b, -a
    else:
        x0, x1, z0, z1 = W - out - depth, W - out, -D + a, -D + b
    if whole:
        part.add(box(x0, x1, y0, y1, z0, z1, sm, vis=(1, 2), tag=tag))
        return
    part.add(rough_block(rng, x0, x1, y0, y1, z0, z1, sm, chamfer=0.012, top_jit=0.004, vis=(1, 2), tag=tag,
                         uvoff=(rng.random(), rng.random())))


def _flight(part, rng, side, W, D, c, w, h, angle, sm):
    """Stone steps from the platform edge down to grade on `side` (centre c along the side), hidden ramp + Roadway."""
    run, n, rh, g = KR.stair_flight(h, angle=angle)
    L = W if side in ("front", "back") else D
    cc = L / 2 if c is None else c
    # build in a local frame: edge at z 0, steps running +z, across x cc-w/2 .. cc+w/2; then place on the side
    q = Part("flight", "", "")
    a0, a1 = cc - w / 2, cc + w / 2
    q.add(prism([(0.0, 0.0), (-h, run), (-h, 0.0)], "x", a0, a1, sm, vis=(), geo=True, view=True, fire=True,
                tag="kidan_ramp"))
    q.road([(a0, 0.0, 0.0), (a1, 0.0, 0.0), (a1, -h, run), (a0, -h, run)], "stone_ext")
    for kk in range(1, n):
        top = -h + kk * rh
        za, zb = run - kk * g, run - (kk - 1) * g
        q.add(rough_block(rng, a0, a1, -h - 0.05, top, za + 0.004, zb - 0.004 + (0.0 if kk > 1 else 0.06), sm,
                          chamfer=0.01, top_jit=0.003, vis=(1, 2), tag="kidan_step", uvoff=(rng.random(), rng.random())))
    q.add(prism([(0.0, 0.0), (-h, run), (-h, 0.0)], "x", a0, a1, sm, vis=(3,), tag="kidan_step_lod"))
    # cheek stones (sode-ishi): sloped blocks either side, 2 cm out from the steps
    for (x0, x1) in ((a0 - 0.22, a0 - 0.02), (a1 + 0.02, a1 + 0.22)):
        q.add(prism([(0.04, 0.0), (-h + 0.10, run), (-h - 0.05, run), (-h - 0.05, 0.0)], "x", x0, x1, sm,
                    vis=(1, 2, 3), tag="sode_ishi"))
    deg, t = {"front": (0.0, (0.0, 0.0, 0.0)), "back": (180.0, (W, 0.0, -D)), "left": (90.0, (0.0, 0.0, -D)),
              "right": (-90.0, (W, 0.0, 0.0))}[side]
    part.merge(q.transformed(deg, t))
    return {"side": side, "run": run, "n": n, "riser": rh, "angle": math.degrees(math.atan(h / run)), "centre": cc,
            "width": w}


# ------------------------------------------------------------------------------------------------ parts
STILTS = {
    "_honden": (KEN, KEN, 1.00, "honden", "issha honden floor (1 x 1 ken) +1.00 on underfloor posts on stones, sleepers, "
                "two rows of underfloor nuki, open beneath (yukashita); the en (koran) runs on from its edges"),
    "_hall": (3 * KEN, 2 * KEN, 0.60, "hall", "village haiden / hall floor (3 x 2 ken) +0.60 with a boarded skirt "
              "(vent gaps) between the perimeter posts"),
    "_ratguard": (2 * KEN, 1.5 * KEN, 1.20, "ratguard", "store / treasure house on posts (+1.20) with rat guards "
                  "(nezumi-gaeshi) round every post"),
}


def part_stilts(variant):
    W, D, drop, kind, used = STILTS[variant]
    p = Part("jp_p_found_stilts", variant, "found", tiers=[1, 2, 3], used_for=used,
             recipe="stilts.platform(part, W, D, drop, kind)",
             datum="body x 0..W, z 0 (front wall line) .. -D; y 0 = floor top; grade -%.2f" % drop)
    r = platform(p, W, D, drop, kind)
    for x, z in ((0, 0), (W, 0), (0, -D), (W, -D)):
        p.conn("post", (x, 0, z), note="body corner node (the shell's wall post stands on the floor here)")
    p.conn("floor", (0, 0, 0))
    p.conn("grade", (0, -drop, 0))
    p.dim("floor_above_grade_m", drop, drop)
    return p


KIDAN = {
    "_shoro": (1.5 * KEN, 1.5 * KEN, 0.60, (("front", None, 1.30),), "bell-tower platform (shoro, 1.5 x 1.5 ken) "
               "0.60 high: kerb stones, facing slabs, base course, earth top, a stone flight with cheek stones"),
    "_hall": (3 * KEN, 2.5 * KEN, 0.45, (("front", None, 1.82),), "hall platform (3 x 2.5 ken) 0.45 high, a 1-ken "
              "stone flight at the front"),
    "_low": (2 * KEN, 1.5 * KEN, 0.30, (("front", None, 1.30), ("back", None, 1.30)), "low platform (0.30) for a "
             "small do or a notice board, flights front and back"),
}


def part_kidan(variant):
    W, D, h, steps, used = KIDAN[variant]
    p = Part("jp_p_found_kidan", variant, "found", tiers=[2, 3] if variant != "_low" else [1, 2, 3], used_for=used,
             recipe="stilts.kidan(part, W, D, h, steps)",
             datum="platform x 0..W, z 0 (front edge) .. -D; y 0 = top; grade -%.2f" % h)
    r = kidan(p, W, D, h, steps)
    for x, z in ((0, 0), (W, 0), (0, -D), (W, -D)):
        p.conn("post", (x, 0, z), note="platform corner")
    for f in r["flights"]:
        p.dim("flight_%s_ramp_deg" % f["side"], "<=34", round(f["angle"], 2), tol=0.0, source="found.step rule (<=34)")
        p.dims[-1]["ok"] = f["angle"] <= 34.0 + 1e-6
        if f["side"] == "front":
            p.conn("stair_head", (f["centre"] - f["centre"] % QK, 0, 0), note="top of the flight (front edge)")
            p.conn("stair_foot", (f["centre"] - f["centre"] % QK, -h, round(f["run"], 4)), note="foot at grade")
    p.conn("grade", (0, -h, 0))
    p.dim("height_m", h, h)
    return p


def register(reg):
    reg("jp_p_found_stilts", list(STILTS), part_stilts)
    reg("jp_p_found_kidan", list(KIDAN), part_kidan)
