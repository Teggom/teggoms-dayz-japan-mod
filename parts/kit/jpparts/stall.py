"""Stable stalls (B2 part 5, jp_p_frame_stall; PARTS_GAP_AUDIT §3 part 20): the built-in fittings of an ox or horse
stall in a doma corner (Kinai farmhouse DW07's ox stall in the niwa, Kanto farmhouse DW06's inside stable, the post-
town house DW10's stable): front posts with a head rail, board partitions, the bars (mase-bo) that close the front,
a manger trough (kaiba-oke) on the back wall and a straw bedding layer.

Part frame: origin = the LEFT front post at the doma floor (y 0 = doma top); +x along the stall front, +z out into the
doma, the stall's inside is -z down to the back wall line z = -depth (the building's wall: not in the part). Every
stall is 'as left' (dead world, 0-2 years): bars down (one lying across the floor, one leaning on a post) so the stall
is enterable for loot, unless bars='closed' (dressing).
"""
import math

from .core import Part, box, KEN, POST, rng_for
from .shapes import tube

BAR_Y = (0.62, 1.12)          # mase-bo heights (A: ox / horse chest and knee)
HEAD = 2.12                   # head rail underside: >= 2.05 clear under it (D2 + margin)


def stall(part, width, depth, sides=(True, True), divider_at=(), bars="down", manger=True, soot=False,
          part_h=1.55, mat="wood_weathered"):
    """One stall front of `width` (x 0..width) over `depth` (z 0..-depth): front posts (and one at every divider),
    a head rail, board partitions on the chosen sides (+ dividers at x in divider_at) from the front post to the back
    wall face, mase-bo bars, the manger on the back wall and straw bedding. Returns {posts, bays}."""
    fm = "wood_sooted" if soot else mat
    rng = rng_for(part.name + "stall")
    xs = sorted({0.0, width} | set(divider_at))
    posts = []
    for x in xs:
        part.add(box(x - POST / 2, x + POST / 2, 0.0, HEAD + 0.15, -POST / 2, POST / 2, fm, vis=(1, 2, 3), geo=True,
                     view=True, fire=True, tag="stall_post", grain="long"))
        posts.append((x, 0.0))
    part.add(box(-POST / 2, width + POST / 2, HEAD, HEAD + 0.15, -0.05, 0.05, fm, vis=(1, 2, 3), geo=True, view=True,
                 fire=True, tag="head_rail", grain="long"))
    zb = -depth + 0.04                                      # the back wall's inner face (wall 0.075 thick, 4 cm)
    # board partitions: sill, boards, top rail (one collision slab each)
    lines = [x for x, on in ((0.0, sides[0]), (width, sides[1])) if on] + list(divider_at)
    for x in lines:
        t0, t1 = x - 0.02, x + 0.02
        part.add(box(t0, t1, 0.0, part_h, zb, -POST / 2, fm, vis=(), geo=True, view=True, fire=True, tag="partition_geo"))
        z = zb
        while z < -POST / 2 - 1e-3:
            z1 = min(-POST / 2, z + rng.uniform(0.22, 0.30))
            if -POST / 2 - z1 < 0.10:
                z1 = -POST / 2
            part.add(box(t0 + 0.004, t1 - 0.004, 0.08, part_h - 0.07, z + 0.003, z1 - 0.003, fm, vis=(1,),
                         tag="partition_board", uvoff=(rng.random(), rng.random())))
            z = z1
        part.add(box(t0 - 0.01, t1 + 0.01, 0.0, 0.08, zb, -POST / 2, fm, vis=(1, 2), tag="partition_sill"))
        part.add(box(t0 - 0.015, t1 + 0.015, part_h - 0.07, part_h, zb, -POST / 2, fm, vis=(1, 2), tag="partition_rail"))
        part.add(box(t0, t1, 0.08, part_h - 0.07, zb, -POST / 2, fm, vis=(2, 3), tag="partition_lod"))
        # the partition's back post against the wall
        part.add(box(x - 0.05, x + 0.05, 0.0, part_h + 0.10, zb - 0.02, zb + 0.08, fm, vis=(1, 2), tag="partition_post"))
    # mase-bo: through holes in the front posts
    bays = [(xs[i], xs[i + 1]) for i in range(len(xs) - 1)]
    for (a, b) in bays:
        if bars == "closed":
            for y in BAR_Y:
                part.add(tube((a - 0.04, y, 0.0), (b + 0.04, y, 0.0), 0.035, fm, n=7, vis=(1, 2), geo=True, view=True,
                              fire=True, tag="mase_bo"))
        else:
            # as left: one bar leaning on the right-hand post, one lying across the floor inside the stall
            L = b - a + 0.08
            part.add(tube((b - 0.14, 0.04, 0.35), (b - 0.10, BAR_Y[1] + 0.25, 0.08), 0.035, fm, n=7, vis=(1, 2),
                          tag="mase_bo_leaning"))
            ang = math.radians(rng.uniform(8, 20))
            cz = -depth * 0.45
            half = L / 2 * 0.95
            p0 = ((a + b) / 2 - half * math.cos(ang), 0.035, cz - half * math.sin(ang))
            p1 = ((a + b) / 2 + half * math.cos(ang), 0.035, cz + half * math.sin(ang))
            part.add(tube(p0, p1, 0.035, fm, n=7, vis=(1, 2), tag="mase_bo_floor"))
        # holes the bars run in: two dark blocks on each post face (visual)
        for x in (a, b):
            for y in BAR_Y:
                part.add(box(x - POST / 2 - 0.003, x + POST / 2 + 0.003, y - 0.04, y + 0.04, -0.03, 0.03,
                             "wood_sooted", vis=(1,), tag="bar_hole"))
        # manger on the back wall
        if manger:
            mw = min(1.10, b - a - 0.40)
            mx0 = (a + b) / 2 - mw / 2
            md, y0, y1 = 0.42, 0.55, 0.92
            z0 = zb
            part.add(box(mx0, mx0 + mw, y0, y1, z0, z0 + md, fm, vis=(), geo=True, view=True, fire=True,
                         tag="manger_geo"))
            wt = 0.035
            for (qa, qb, za, zb2) in ((mx0, mx0 + mw, z0, z0 + wt), (mx0, mx0 + mw, z0 + md - wt, z0 + md),
                                      (mx0, mx0 + wt, z0 + wt, z0 + md - wt), (mx0 + mw - wt, mx0 + mw, z0 + wt,
                                                                               z0 + md - wt)):
                part.add(box(qa, qb, y0, y1, za, zb2, fm, vis=(1, 2), tag="manger"))
            part.add(box(mx0 + wt, mx0 + mw - wt, y0, y0 + 0.04, z0 + wt, z0 + md - wt, fm, vis=(1,), tag="manger"))
            part.add(box(mx0 + wt, mx0 + mw - wt, y0 + 0.04, y0 + 0.10, z0 + wt, z0 + md - wt, "straw_stack", vis=(1,),
                         tag="fodder"))
            for lx in (mx0 + 0.05, mx0 + mw - 0.09):
                for lz in (z0 + 0.03, z0 + md - 0.07):
                    part.add(box(lx, lx + 0.04, 0.0, y0, lz, lz + 0.04, fm, vis=(1, 2), tag="manger_leg"))
            part.add(box(mx0 - 0.01, mx0 + mw + 0.01, y0, y1, z0, z0 + md, fm, vis=(3,), tag="manger_lod"))
            # tether ring on the back wall beside the manger
            part.add(tube((mx0 + mw + 0.12, 1.00, zb + 0.01), (mx0 + mw + 0.12, 1.00, zb + 0.05), 0.045, "metal_iron",
                          n=8, vis=(1,), tag="tether_ring"))
        # straw bedding: a thin uneven layer on the doma (visual; the doma's Roadway carries the feet)
        part.add(box(a + 0.08, b - 0.08, 0.0, 0.025, zb + 0.05, -0.10, "straw_stack", vis=(1, 2), tag="bedding",
                     uvscale=(0.8, 0.8)))
        for _ in range(4):
            cx = rng.uniform(a + 0.3, b - 0.3)
            cz = rng.uniform(-depth + 0.4, -0.4)
            r = rng.uniform(0.18, 0.32)
            part.add(box(cx - r, cx + r, 0.025, 0.025 + rng.uniform(0.03, 0.06), cz - r * 0.8, cz + r * 0.8,
                         "straw_stack", vis=(1,), tag="bedding_heap", uvoff=(rng.random(), rng.random())))
    return {"posts": posts, "bays": bays}


VARIANTS = {
    # variant: (width ken, depth ken, sides, dividers (ken), bars, soot, used for, tiers)
    "_ox": (1.0, 1.5, (True, True), (), "down", False,
            "Kinai farmhouse ox stall in the niwa (DW07, required): 1 x 1.5 ken, board partitions, bars down (as left), "
            "manger and tether ring on the back wall, straw bedding", [1, 2]),
    "_ox_closed": (1.0, 1.5, (True, True), (), "closed", False,
                   "the same ox stall with its two mase-bo in place (dressing; not enterable)", [1, 2]),
    "_umaya": (1.5, 1.5, (True, False), (), "down", True,
               "Kanto farmhouse inside stable (umaya) in a doma corner (DW06 variant): 1.5 x 1.5 ken, one partition "
               "(the building's walls close the rest), sooted from the kitchen smoke", [1, 2]),
    "_row2": (2.0, 1.5, (True, True), (1.0,), "down", False,
              "two stalls side by side for the post-town house / inn stable (DW10 variant, TR09): 2 x 1.5 ken with a "
              "divider", [2]),
}


def part_stall(variant):
    wk, dk, sides, divs, bars, soot, used, tiers = VARIANTS[variant]
    W, D = wk * KEN, dk * KEN
    p = Part("jp_p_frame_stall", variant, "frame", tiers=tiers, used_for=used,
             recipe="stall.stall(part, width, depth, sides, divider_at, bars, manger, soot)",
             datum="origin = the left front post at the doma top (y 0); +x along the stall front (%.2f), the stall "
                   "goes -z to the building's back wall line at z -%.2f (the wall is the building's)" % (W, D))
    S = stall(p, W, D, sides=sides, divider_at=tuple(d * KEN for d in divs), bars=bars, soot=soot)
    for (x, z) in S["posts"]:
        p.conn("post", (x, 0, z), hidden=True, note="stall front post (in the part)")
    p.conn("post", (0, 0, -D), note="the building's wall line behind the stall")
    p.dim("stall_width_m", "1.82-2.73", W / (len(divs) + 1), source="(A) umaya 1 x 1.5 ken per animal")
    p.dim("stall_depth_m", 2.73, D, source="(A) 1.5 ken")
    p.dim("head_clear_m", ">=2.05", HEAD, source="PLAYBOOK D2 / D4")
    p.dims[-1]["ok"] = HEAD >= 2.05
    p.dim("bar_heights_m", "0.6 / 1.1 (A)", 0.0, source="(A) mase-bo")
    p.dims[-1].update(measured="%.2f / %.2f" % BAR_Y, ok=True)
    clear = W / (len(divs) + 1) - POST - 0.04
    p.dim("stall_entry_clear_m", ">=1.00", round(clear, 3), source="PLAYBOOK D1 (bars down)")
    p.dims[-1]["ok"] = clear >= 1.0 or bars == "closed"
    return p


def register(reg):
    reg("jp_p_frame_stall", list(VARIANTS), part_stall)
