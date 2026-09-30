"""Floor pits and slatted floors (B2 optional wave-1 variety: jp_p_floor_pit, jp_p_floor_sunoko; PARTS_GAP_AUDIT §3
parts 6 and 51). Both work through the promoted floor module (jpparts/floors.py, B0): a pit is a hole of kind 'pit'
cut out of a floor, lined by pit_fn(kind) (floors.<kind>(holes=[(x0, x1, z0, z1, 'pit')], hole_fn=pits.pit_fn(...)));
the fitting inside (irori frame hook, kettle, kamado) is PA2's.

Pit kinds:
  irori       sunken hearth in a raised board floor: a thick sooted wooden frame (robuchi) flush with the floor, clay
              walls, an ash bed 0.20 under the floor (Roadway 'doma': a player can step in)
  irori_doma  hearth in an earth floor (poor huts, DW01 / DW30): a ring of field stones round a shallow ash pit
  slot        the drop slot of a walk-in toilet (DW26): rim boards and a closed, lined pit under it

sunoko(name, x0, x1, z0, z1, y, kind): a slatted floor in the style of floors.boards: 'take' = split-bamboo slats
(take-yuka, the Kinai tenant house floor), 'slat' = board slats with real gaps (sunoko: sinks, bath and wash floors);
support block in Resolution 2 / 3 + Geometry, Roadway 'boards' at y, holes as floors.boards.
"""
import math

from .core import Part, box, KEN, HALF, rng_for, stone
from .floors import norm_holes, rect_minus, _finish_holes, open_box


def pit_fn(kind="irori", soot=True):
    fm = "wood_sooted" if soot else "wood_weathered"

    def fn(part, hole, y):
        if hole.get("kind") not in ("pit", "hearth", "slot"):
            return
        x0, x1, z0, z1 = hole["rect"]
        rng = rng_for(part.name + kind + "%.2f%.2f" % (x0, z0))
        if kind == "irori":
            f = 0.10
            for (a0, a1, b0, b1) in ((x0 - f, x0, z0 - f, z1 + f), (x1, x1 + f, z0 - f, z1 + f), (x0, x1, z0 - f, z0),
                                     (x0, x1, z1, z1 + f)):
                part.add(box(a0, a1, y - 0.12, y + 0.015, b0, b1, fm, vis=(1, 2, 3), geo=True, view=True, fire=True,
                             tag="robuchi", grain="long"))
            ya = y - 0.20
            w = 0.04
            for (a0, a1, b0, b1) in ((x0, x0 + w, z0, z1), (x1 - w, x1, z0, z1), (x0 + w, x1 - w, z0, z0 + w),
                                     (x0 + w, x1 - w, z1 - w, z1)):
                part.add(box(a0, a1, ya - 0.25, y - 0.12, b0, b1, "wall_nakanuri_int", vis=(1, 2), geo=True, view=True,
                             fire=True, tag="pit_wall"))
            part.add(box(x0 + w, x1 - w, ya - 0.25, ya, z0 + w, z1 - w, {"top": "ground_ash", "default": "wall_arakabe"},
                         vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag="ash_bed"))
            part.road([(x0 + w, ya, z0 + w), (x1 - w, ya, z0 + w), (x1 - w, ya, z1 - w), (x0 + w, ya, z1 - w)], "doma")
            # a few charred ends of firewood left in the ash (as left)
            for _ in range(3):
                cx, cz = rng.uniform(x0 + 0.2, x1 - 0.2), rng.uniform(z0 + 0.2, z1 - 0.2)
                a = rng.uniform(0, math.pi)
                L = rng.uniform(0.18, 0.30)
                from .shapes import tube
                part.add(tube((cx - L / 2 * math.cos(a), ya + 0.03, cz - L / 2 * math.sin(a)),
                              (cx + L / 2 * math.cos(a), ya + 0.03, cz + L / 2 * math.sin(a)), 0.028, "wood_sooted",
                              n=5, vis=(1,), tag="firewood"))
        elif kind == "irori_doma":
            ya = y - 0.12
            part.add(box(x0, x1, ya - 0.20, ya, z0, z1, {"top": "ground_ash", "default": "wall_arakabe"},
                         vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag="ash_bed"))
            part.road([(x0, ya, z0), (x1, ya, z0), (x1, ya, z1), (x0, ya, z1)], "doma")
            # the hole's wall: packed earth to the ash
            for (a0, a1, b0, b1) in ((x0 - 0.03, x0, z0 - 0.03, z1 + 0.03), (x1, x1 + 0.03, z0 - 0.03, z1 + 0.03),
                                     (x0, x1, z0 - 0.03, z0), (x0, x1, z1, z1 + 0.03)):
                part.add(box(a0, a1, ya - 0.20, y, b0, b1, "wall_arakabe", vis=(1, 2), geo=True, view=True,
                             fire="dirt", tag="pit_wall"))
            # ring of field stones on the rim
            cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
            rx, rz = (x1 - x0) / 2 + 0.10, (z1 - z0) / 2 + 0.10
            n = 10
            for k in range(n):
                a = 2 * math.pi * (k + rng.uniform(-0.15, 0.15)) / n
                sx, sz = cx + rx * math.cos(a), cz + rz * math.sin(a)
                sx = max(x0 - 0.16, min(x1 + 0.16, sx))
                sz = max(z0 - 0.16, min(z1 + 0.16, sz))
                part.add(stone(rng, sx, sz, rng.uniform(0.18, 0.26), rng.uniform(0.15, 0.22), rng.uniform(0.07, 0.11),
                               y + rng.uniform(0.05, 0.09), "stone_field", bury=0.06, n=8, vis=(1, 2), tag="hearth_stone"))
            for _ in range(3):
                from .shapes import tube
                px, pz = rng.uniform(x0 + 0.15, x1 - 0.15), rng.uniform(z0 + 0.15, z1 - 0.15)
                a = rng.uniform(0, math.pi)
                L = rng.uniform(0.2, 0.32)
                part.add(tube((px - L / 2 * math.cos(a), ya + 0.03, pz - L / 2 * math.sin(a)),
                              (px + L / 2 * math.cos(a), ya + 0.03, pz + L / 2 * math.sin(a)), 0.028, "wood_sooted",
                              n=5, vis=(1,), tag="firewood"))
        else:                                                   # slot: the toilet's drop slot
            for (a0, a1, b0, b1) in ((x0 - 0.04, x1 + 0.04, z0 - 0.04, z0), (x0 - 0.04, x1 + 0.04, z1, z1 + 0.04)):
                part.add(box(a0, a1, y - 0.03, y + 0.004, b0, b1, fm, vis=(1, 2), tag="slot_rim"))
            yb = y - 0.70
            for (a0, a1, b0, b1) in ((x0 - 0.03, x0, z0 - 0.03, z1 + 0.03), (x1, x1 + 0.03, z0 - 0.03, z1 + 0.03),
                                     (x0, x1, z0 - 0.03, z0), (x0, x1, z1, z1 + 0.03)):
                part.add(box(a0, a1, yb, y - 0.03, b0, b1, fm, vis=(1, 2), geo=True, view=True, fire=True,
                             tag="pit_lining"))
            part.add(box(x0, x1, yb, yb + 0.03, z0, z1, fm, vis=(1, 2), geo=True, view=True, fire=True, tag="pit_lining"))
    return fn


def sunoko(name, x0, x1, z0, z1, y, kind="take", along_x=False, holes=(), hole_fn=None):
    """Slatted floor (see the module docstring)."""
    hs = norm_holes(holes)
    s = Part(name, "", "")
    rects = rect_minus((x0, x1, z0, z1), hs)
    for (a, b, c, d) in rects:
        s.add(box(a, b, y - 0.15, y, c, d, "wood_weathered", vis=(2, 3), geo=True, view=True, fire="wood",
                  tag="floor_lod"))
        # the dark base under the slats (earth / straw below a raised slat floor)
        s.add(box(a, b, y - 0.15, y - 0.045, c, d, {"top": "ground_doma_earth", "default": "wood_sooted"}, vis=(1,),
                  tag="floor_base"))
    rng = rng_for(name)
    if kind == "take":
        # split bamboo: the take-yuka texture on slat bands, three sleepers under them (cross grain)
        for (a, b, c, d) in rects:
            s.add(open_box(a, b, y - 0.025, y, c, d, "floor_takeyuka", ("top", "xlo", "xhi", "zlo", "zhi"),
                           "takeyuka", uvrot=0.0 if along_x else 90.0))
            n = max(2, int((b - a if not along_x else d - c) / 0.9) + 1)
            for k in range(n):
                if not along_x:
                    xx = a + 0.05 + (b - a - 0.10) * k / (n - 1)
                    s.add(box(xx - 0.035, xx + 0.035, y - 0.095, y - 0.025, c, d, "bamboo_weathered", vis=(1,),
                              tag="sleeper"))
                else:
                    zz = c + 0.05 + (d - c - 0.10) * k / (n - 1)
                    s.add(box(a, b, y - 0.095, y - 0.025, zz - 0.035, zz + 0.035, "bamboo_weathered", vis=(1,),
                              tag="sleeper"))
    else:
        # board slats 0.09 wide with 0.03 gaps over two bearers
        lo, hi = (z0, z1) if along_x else (x0, x1)
        p = lo + 0.015
        while p < hi - 0.05:
            q = min(hi - 0.015, p + 0.09)
            for (a, b, c, d) in rect_minus(((x0, x1, p, q) if along_x else (p, q, z0, z1)), hs):
                s.add(box(a, b, y - 0.03, y, c, d, "wood_weathered", vis=(1,), tag="slat",
                          uvoff=(rng.random(), rng.random())))
            p = q + 0.03
        for (a, b, c, d) in rects:
            for k in (0.2, 0.8):
                if along_x:
                    xx = a + (b - a) * k
                    s.add(box(xx - 0.04, xx + 0.04, y - 0.10, y - 0.03, c, d, "wood_weathered", vis=(1,), tag="bearer"))
                else:
                    zz = c + (d - c) * k
                    s.add(box(a, b, y - 0.10, y - 0.03, zz - 0.04, zz + 0.04, "wood_weathered", vis=(1,), tag="bearer"))
    for (a, b, c, d) in rects:
        s.road([(a, y, c), (b, y, c), (b, y, d), (a, y, d)], "boards")
    _finish_holes(s, hs, y, hole_fn)
    return s


# ------------------------------------------------------------------------------------------------ part samples
def part_floor_pit(variant):
    from . import floors as FL
    kind = variant[1:]
    used = {"irori": "sunken hearth (irori) in a raised board floor: sooted robuchi frame flush with the floor, clay "
                     "walls, ash bed 0.20 down with charred firewood (the kettle hook / fitting is PA2's)",
            "irori_doma": "hearth pit in an earth floor ringed with field stones (poor huts DW01 / DW30, work sheds)",
            "slot": "the walk-in toilet's drop slot (DW26): rim boards over a closed, lined pit"}[kind]
    p = Part("jp_p_floor_pit", variant, "found", tiers=[1, 2] if kind != "slot" else [1, 2, 3], used_for=used,
             recipe="floors.<kind>(holes=[(x0, x1, z0, z1, 'pit')], hole_fn=pits.pit_fn('%s'))" % kind,
             datum="a 1 x 1 ken floor sample, x 0..1.82, z 0..-1.82; y 0 = grade; the floor top at %.2f" % (
                 {"irori": 0.45, "irori_doma": 0.05, "slot": 0.12}[kind]))
    if kind == "irori":
        y = 0.45
        h = (HALF / 2 + 0.0, HALF / 2 + HALF, -HALF / 2 - HALF, -HALF / 2)
        p.merge(FL.boards("floor", 0.0, KEN, -KEN, 0.0, y, holes=[h + ("pit",)], hole_fn=pit_fn("irori")))
        p.dim("hearth_m", "0.91 x 0.91 (3 x 3 shaku)", h[1] - h[0])
    elif kind == "irori_doma":
        y = 0.05
        h = (0.55, 1.27, -1.27, -0.55)
        p.merge(FL.doma("floor", 0.0, KEN, -KEN, 0.0, y=y, holes=[h + ("pit",)], hole_fn=pit_fn("irori_doma")))
        p.dim("hearth_m", "0.6-0.9 (A)", h[1] - h[0])
    else:
        y = 0.12
        h = (0.76, 1.06, -1.00, -0.83)
        p.merge(FL.boards("floor", 0.0, KEN, -KEN, 0.0, y, holes=[h + ("slot",)], hole_fn=pit_fn("slot")))
        p.dim("slot_m", "0.30 x 0.17 (A)", h[1] - h[0])
    p.conn("post", (0, 0, 0))
    p.conn("floor", (0, y, 0), note="floor top")
    p.meta["hole"] = [round(v, 3) for v in h]
    return p


def part_floor_sunoko(variant):
    kind = variant[1:]
    p = Part("jp_p_floor_sunoko", variant, "found", tiers=[1, 2] if kind == "take" else [1, 2, 3],
             used_for={"take": "split-bamboo floor (take-yuka / sunoko-yuka) of the Kinai tenant house and poor huts "
                               "(DW01 / DW30 floor axis), on bamboo sleepers",
                       "slat": "board slat floor with gaps (sunoko): kitchen sink and wash floors, bath floors"}[kind],
             recipe="pits.sunoko(name, x0, x1, z0, z1, y, kind) (floors.boards-style; holes + hole_fn)",
             datum="a 1 x 1 ken floor, x 0..1.82, z 0..-1.82; floor top 0.30")
    p.merge(sunoko("floor", 0.0, KEN, -KEN, 0.0, 0.30, kind))
    p.dim("slat_gap_m", "0.02-0.04" if kind == "slat" else "texture", 0.03 if kind == "slat" else 0.0)
    if kind == "take":
        p.dims[-1]["ok"] = True
    p.conn("post", (0, 0, 0))
    p.conn("floor", (0, 0.30, 0), note="floor top")
    return p


def register(reg):
    reg("jp_p_floor_pit", ["_irori", "_irori_doma", "_slot"], part_floor_pit)
    reg("jp_p_floor_sunoko", ["_take", "_slat"], part_floor_sunoko)
