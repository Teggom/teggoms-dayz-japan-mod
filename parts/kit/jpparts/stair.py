"""Stairs (B2 part 6, jp_p_stair; PARTS_GAP_AUDIT §3 part 11, §6 risk 6): a flight with a hidden walk ramp, the
stairwell cut into the upper floor (floors.<kind>(holes=[(..., 'stair')], hole_fn=stair.well_fn(...))) and its rim
and guard rail. For the one grand hatago per tier-3 town (size 2) and the kura loft (G1-5 elevation).

Rules (PLAYBOOK D4, §15 T9, walked in game at G3): walk ramp <= 38 deg (37.8 walks fine), >= 1.10 m wide, >= 2.05 m
head room over the whole flight (the well starts where the ceiling would come closer), the ramp carries the feet
(Geometry + Roadway 'stair'); the treads are visual.

Part frame: the flight runs along +x from its foot (x 0, first riser, y 0 = the lower floor top) to its head (x = run,
y = rise, the upper floor top); its width runs from z 0 (the wall it stands against, or its left edge) to z = -width.
Connectors stair_foot / stair_head (PLAYBOOK §10.2).

Kinds:
  box   hako-kaidan / kaidan-dansu look: every step a closed box down to the floor, drawers and cupboards in the
        exposed side (shops, inns)
  open  two stringers and treads, no risers: the plain steep-looking stair of kura lofts and work buildings
"""
import math

from .core import Part, box, prism, KEN, HALF, POST, rng_for

ANGLE = 37.8                 # deg, walked in game (G3)
MIN_W, MIN_HEAD = 1.10, 2.05


def flight(rise, angle=ANGLE, riser_max=0.215, grid=0.455):
    """(run, n steps, riser, going) for a straight flight. The run is rounded UP to the 0.455 grid (the head lands on
    a grid line; the walk angle only gets gentler)."""
    run = rise / math.tan(math.radians(angle))
    if grid:
        run = math.ceil(run / grid - 1e-9) * grid
    n = max(2, int(math.ceil(rise / riser_max)))
    return run, n, rise / n, run / n


def well_start(rise, ceil_under, angle=ANGLE, head=MIN_HEAD):
    """x (from the foot) where the stairwell must begin so the head room over the flight stays >= head:
    the ceiling (upper floor underside, y = ceil_under above the lower floor) may not come closer to the ramp."""
    return max(0.0, (ceil_under - head) / math.tan(math.radians(angle)))


def stair(part, width=1.20, rise=2.85, kind="box", angle=ANGLE, mat=None, drawers=True, side_open=-1):
    """Build the flight in the part frame (see the module docstring). side_open: -1 = the exposed side is z = -width
    (drawers there), +1 = z 0. Returns dict(run, n, riser, going, angle)."""
    run, n, rh, g = flight(rise, angle)
    fm = mat or ("wood_interior" if kind == "box" else "wood_weathered")
    z0, z1 = -width, 0.0
    # hidden ramp: the wedge under the tread line (Geometry / View / Fire) + Roadway 'stair' on it
    part.add(prism([(0.0, 0.0), (run, rise), (run, 0.0)], "z", z0, z1, fm, vis=(), geo=True, view=True, fire="wood",
                   tag="stair_ramp"))
    part.road([(0.0, 0.0, z1), (run, rise, z1), (run, rise, z0), (0.0, 0.0, z0)], "stair")
    rng = rng_for(part.name + "stair")
    if kind == "box":
        for k in range(1, n + 1):
            xa, xb = (k - 1) * g, k * g if k < n else run
            top = k * rh
            # the step box (closed, visual); the top tread board with a small nosing
            part.add(box(xa, xb, 0.0, top - 0.03, z0, z1, fm, vis=(1, 2), tag="stair_step",
                         uvoff=(rng.random(), rng.random())))
            part.add(box(xa - 0.02, xb, top - 0.03, top, z0, z1, fm, vis=(1, 2), tag="stair_tread", grain="long"))
            if drawers and k < n and top > 0.35:
                zf = z0 - 0.004 if side_open < 0 else z1 + 0.004
                # drawers / doors in the exposed side of every step column (kaidan-dansu)
                hh = min(0.30, top - 0.10)
                part.add(box(xa + 0.03, xb - 0.03, top - 0.03 - hh, top - 0.06, min(zf, zf + side_open * 0.012),
                             max(zf, zf + side_open * 0.012), fm, vis=(1,), tag="drawer_front"))
                px = (xa + xb) / 2
                py = top - 0.045 - hh / 2
                part.add(box(px - 0.04, px + 0.04, py - 0.012, py + 0.012, min(zf + side_open * 0.012,
                                                                                  zf + side_open * 0.022),
                             max(zf + side_open * 0.012, zf + side_open * 0.022), "metal_iron", vis=(1,), tag="pull_iron"))
        part.add(prism([(0.0, 0.0), (run, rise), (run, 0.0)], "z", z0, z1, fm, vis=(3,), tag="stair_lod"))
    else:
        th = 0.035
        ta = rise / run
        dv = 0.24 / math.cos(math.atan(ta))
        for zz in (z0, z1 - 0.045):
            # stringer: a sloped board 0.24 deep along the flight, its top 0.10 over the tread line
            part.add(prism([(0.0, 0.0), (dv / ta, 0.0), (run, rise - dv), (run, rise + 0.10), (0.0, 0.10)], "z", zz,
                           zz + 0.045, fm, vis=(1, 2, 3), tag="stringer", grain="long"))
        for k in range(1, n + 1):
            xa, xb = (k - 1) * g - 0.03, min(run, k * g + 0.03)
            top = k * rh
            part.add(box(xa, xb, top - th, top, z0 + 0.045, z1 - 0.045, fm, vis=(1, 2), tag="stair_tread",
                         grain="long", uvoff=(rng.random(), rng.random())))
            # the tread tenons through the stringers (small blocks on the outer faces)
            for zz in (z0 - 0.01, z1):
                part.add(box(xa + 0.04, xb - 0.04, top - th, top, zz, zz + 0.01, fm, vis=(1,), tag="tenon"))
    return {"run": run, "n": n, "riser": rh, "going": g, "angle": math.degrees(math.atan(rise / run))}


def well_fn(open_side="x1", rail_h=0.85, mat="wood_weathered", rails=True):
    """hole_fn for floors.<kind>(holes=[(x0, x1, z0, z1, 'stair')], hole_fn=...): a rim board (kamachi) round the
    stairwell and a guard rail on every side but the arrival side `open_side` ('x0' | 'x1' | 'z0' | 'z1') and a side
    that stands against a wall (hole['wall'] in the same codes). Posts at the rail corners; one collision slab per
    rail run (players do not fall in from the side)."""
    def fn(part, hole, y):
        if hole.get("kind") not in ("stair", "stairwell"):
            return
        x0, x1, z0, z1 = hole["rect"]
        op = hole.get("open", open_side)
        wall = hole.get("wall")
        rim = 0.05
        for code, (a0, a1, b0, b1) in (("x0", (x0 - rim, x0, z0 - rim, z1 + rim)), ("x1", (x1, x1 + rim, z0 - rim, z1 + rim)),
                                       ("z0", (x0, x1, z0 - rim, z0)), ("z1", (x0, x1, z1, z1 + rim))):
            part.add(box(a0, a1, y - 0.15, y + 0.005, b0, b1, mat, vis=(1, 2), tag="well_rim"))
        if not rails:
            return
        runs = []
        if op != "z0" and wall != "z0":
            runs.append(((x0, z0 - 0.03), (x1, z0 - 0.03)))
        if op != "z1" and wall != "z1":
            runs.append(((x0, z1 + 0.03), (x1, z1 + 0.03)))
        if op != "x0" and wall != "x0":
            runs.append(((x0 - 0.03, z0), (x0 - 0.03, z1)))
        if op != "x1" and wall != "x1":
            runs.append(((x1 + 0.03, z0), (x1 + 0.03, z1)))
        for (pa, pb) in runs:
            xa, xb = sorted((pa[0], pb[0]))
            za, zb = sorted((pa[1], pb[1]))
            xa, xb = xa - 0.025, xb + 0.025
            za, zb = za - 0.025, zb + 0.025
            part.add(box(xa, xb, y + rail_h - 0.06, y + rail_h, za, zb, mat, vis=(1, 2), tag="well_rail", grain="long"))
            part.add(box(xa, xb, y + 0.40, y + 0.45, za + 0.01, zb - 0.01, mat, vis=(1,), tag="well_rail_mid",
                         grain="long"))
            part.add(box(xa, xb, y, y + rail_h, za, zb, mat, vis=(), geo=True, view=True, fire=True, tag="well_rail_geo"))
            for (px, pz) in (pa, pb):
                part.add(box(px - 0.04, px + 0.04, y, y + rail_h + 0.04, pz - 0.04, pz + 0.04, mat, vis=(1, 2),
                             tag="well_post"))
    return fn


def well_rect(run, width, rise, floor_t=0.15, angle=ANGLE, margin=0.04, x_foot=0.0, z_wall=0.0):
    """The stairwell rectangle (x0, x1, z0, z1) in the stair's frame for an upper floor of thickness floor_t whose top
    is at `rise`: from well_start to the head, over the flight's width plus a margin."""
    xs = well_start(rise, rise - floor_t, angle)
    return (x_foot + xs, x_foot + run, z_wall - width - margin, z_wall)


VARIANTS = {
    # variant: (kind, width, rise, used for, tiers)
    "_box": ("box", 1.20, 2.80, "box stair with the kaidan-dansu look (drawers in its side) for the grand hatago's "
                               "upper floor (TR05 size 2, G1-5) and shops: 1.20 wide, 37.8 deg walk ramp", [2, 3]),
    "_open": ("open", 1.10, 2.40, "plain open stair (stringers + treads) for the kura loft and work buildings (DW22 "
                                 "loft, G1-5 elevation): 1.10 wide, 37.8 deg walk ramp", [1, 2, 3]),
    "_well": ("box", 1.20, 2.80, "the upper floor's stairwell for the _box stair: the floor (floors.boards) cut by a "
                                "'stair' hole, rim boards and a guard rail on the three open sides; shown with its "
                                "stair", [2, 3]),
}


def part_stair(variant):
    from . import floors as FL
    kind, W, rise, used, tiers = VARIANTS[variant]
    p = Part("jp_p_stair", variant, "found", tiers=tiers, used_for=used,
             recipe="stair.stair(part, width, rise, kind) + floors.<kind>(holes=[stair.well_rect(...) + 'stair'], "
                    "hole_fn=stair.well_fn(open_side='x1'))",
             datum="flight along +x from the foot (x 0, y 0 = lower floor top) to the head (x = run, y = rise = upper "
                   "floor top); width from z 0 (wall side) to z -%.2f" % W)
    S = stair(p, W, rise, kind)
    if variant == "_well":
        x0, x1, z0, z1 = well_rect(S["run"], W, rise)
        fl = FL.boards("upper", -0.5, S["run"] + 1.2, -W - 1.0, 0.0, rise, holes=[{"rect": (x0, x1, z0, z1),
                                                                                    "kind": "stair", "open": "x1",
                                                                                    "wall": "z1"}],
                       hole_fn=well_fn())
        p.merge(fl)
        p.dim("well_length_m", round(x1 - x0, 3), x1 - x0, source="head room >= 2.05 over the flight (D4)")
        p.meta["well_rect"] = [round(v, 3) for v in (x0, x1, z0, z1)]
        # head room along the flight under the upper floor (underside rise - 0.15)
        hmin = min((rise - 0.15) - (S["riser"] * math.ceil(x / S["going"] - 1e-9))
                   for x in [i * 0.05 for i in range(int(x0 / 0.05) + 1)])
        p.dim("head_room_m", ">=2.05", round(hmin, 3), source="PLAYBOOK D4 (tread tops under the upper floor)")
        p.dims[-1]["ok"] = hmin >= MIN_HEAD - 1e-6
    p.dim("ramp_deg", "<=38", round(S["angle"], 2), tol=0.0, source="PLAYBOOK D4 / §15 T9 (37.8 walks fine)")
    p.dims[-1]["ok"] = S["angle"] <= 38.0 + 1e-6
    p.dim("width_m", ">=1.10", W, source="PLAYBOOK D4")
    p.dims[-1]["ok"] = W >= MIN_W - 1e-6
    p.dim("riser_m", "0.18-0.22 (A)", round(S["riser"], 3))
    p.dim("steps", S["n"], S["n"], tol=0)
    p.conn("stair_foot", (0.0, 0.0, 0.0), note="first riser at the lower floor top, wall-side edge of the flight")
    p.conn("stair_head", (S["run"], rise, 0.0), note="top of the ramp = upper floor top (run %.3f, on the grid)" % S["run"])
    p.meta["flight"] = {k: round(v, 4) if isinstance(v, float) else v for k, v in S.items()}
    return p



def register(reg):
    reg("jp_p_stair", list(VARIANTS), part_stair)
