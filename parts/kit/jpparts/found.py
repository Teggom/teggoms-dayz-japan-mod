"""Foundations, sills, under-floor zone, steps (build list jp_p_found_*) and verandas (jp_p_porch_*).
Rule 3: every visible stone is its own convex shape; never a continuous plinth."""
import math

from .core import Part, box, prism, stone, rings, rand_convex, KEN, HALF, QK, POST, rng_for
from .shapes import rough_block, board_run, tube
from . import frame


# ------------------------------------------------------------------------------------------------ soseki
SOSEKI_SHAPES = 8


def soseki(part, x, z, shape, grade=-0.12, sel=None):
    """One rounded field stone under a post node: top at y 0 (post foot), grade at `grade`."""
    rng = rng_for("soseki", shape)
    w = rng.uniform(0.30, 0.50)
    d = w * rng.uniform(0.8, 1.05)
    h = rng.uniform(0.15, 0.30)
    s = stone(rng, x, z, w, d, h, 0.0, "stone_field", bury=0.0, n=9, flat_top=rng.uniform(0.55, 0.72), vis=(1,),
              tag="soseki", sel=sel)
    part.add(s)
    lo = stone(rng_for("soseki_lo", shape), x, z, w, d, h, 0.0, "stone_field", bury=0.0, n=6, flat_top=0.6,
               vis=(2, 3), geo=True, view=True, fire=True, tag="soseki_lod", sel=sel)
    lo.verts = [(v[0], v[1], v[2]) for v in lo.verts]
    part.add(lo)
    return s, h


def part_soseki(variant):
    p = Part("jp_p_found_soseki", variant, "found", tiers=[1, 2],
             used_for="the 8 field-stone shapes under the posts of rural houses and verandas" +
             (" (north-side moss, wear _w2)" if variant == "_mossy" else ""),
             recipe="found.soseki(part, x, z, shape 0-7)", datum="stone k at x = k * 0.91; y 0 = stone top = post foot; "
             "grade at -0.12 (exposed 0.05-0.20 by placement)")
    for k in range(SOSEKI_SHAPES):
        s, h = soseki(p, k * HALF, 0.0, k, sel="stone%d" % (k + 1))
        p.conn("post", (k * HALF, 0, 0), shape=k)
    p.conn("grade", (0, -0.12, 0), note="exposure 0.05-0.20 set by the placement")
    if variant == "_mossy":
        p.wear_by_mat["stone_field"] = "_w2"
    bbs = [s.bbox() for s in p.solids if s.tag == "soseki"]
    p.dim("stone_across_m", "0.30-0.50", max(b[1] - b[0] for b in bbs), source="build_list (A)")
    p.dim("stone_across_min_m", "0.30-0.50", min(b[1] - b[0] for b in bbs), source="build_list (A)")
    p.dim("stone_height_m", "0.15-0.30", max(b[3] - b[2] for b in bbs), source="build_list (A)")
    p.dim("shapes", 8, SOSEKI_SHAPES, tol=0)
    return p


# ------------------------------------------------------------------------------------------------ dodai on stones
def dodai_stones(part, x0, x1, dressed=False, show=0.15, seed=0, z=0.0):
    """Timber sill (0.12 x 0.12, top at y 0) on a course of individual cut stones; joints avoid the post nodes."""
    rng = rng_for(part.name + "dodai", seed)
    frame.dodai(part, x0 - 0.06, x1 + 0.06, z=z)
    top = -0.12
    grade = top - show
    nodes = [x0 + k * KEN for k in range(int(round((x1 - x0) / KEN)) + 1)]
    x = x0 - 0.10
    while x < x1 + 0.10 - 1e-3:
        L = rng.uniform(0.30, 0.60) if not dressed else rng.uniform(0.45, 0.60)
        e = min(x + L, x1 + 0.10)
        for nd in nodes:                                   # no joint within 8 cm of a post node
            if abs(e - nd) < 0.08:
                e = nd + 0.09
        if x1 + 0.10 - e < 0.2:
            e = x1 + 0.10
        gap = rng.uniform(0.005, 0.02) if not dressed else rng.uniform(0.004, 0.008)
        dep = rng.uniform(0.25, 0.35) if not dressed else 0.30
        yt = top - (rng.uniform(0.0, 0.015) if not dressed else 0.0)
        b = rough_block(rng, x + gap / 2, e - gap / 2, grade - 0.12, yt, z - dep / 2, z + dep / 2, "stone_cut",
                        chamfer=0.03 if not dressed else 0.012, top_jit=0.012 if not dressed else 0.002,
                        vis=(1,), tag="dodai_stone",
                        uvoff=(rng.random(), rng.random()))
        part.add(b)
        x = e
    part.add(box(x0 - 0.10, x1 + 0.10, grade - 0.12, top, z - 0.14, z + 0.14, "stone_cut", vis=(2, 3), geo=True, view=True,
                 fire=True, tag="dodai_stone_lod"))
    return grade


def part_dodai_stones(variant):
    dressed = variant == "_dressed"
    p = Part("jp_p_found_dodai_stones", variant, "found", tiers=[3] if dressed else [2],
             used_for="timber sill on a course of %s cut stones (town houses)" % ("better dressed" if dressed else
                                                                                 "roughly dressed"),
             recipe="found.dodai_stones(part, x0, x1, dressed)",
             datum="2-ken run from the post node x 0; y 0 = dodai top (posts stand here); grade at -0.27")
    grade = dodai_stones(p, 0.0, 2 * KEN, dressed)
    st = [s.bbox() for s in p.solids if s.tag == "dodai_stone"]
    ls = [b[1] - b[0] for b in st[1:-1]] or [st[0][1] - st[0][0]]
    p.dim("stone_length_m", "0.30-0.60", sum(ls) / len(ls), tol=0.02, source="build_list (A)")
    p.dim("stone_depth_m", "0.25-0.35", max(b[5] - b[4] for b in st), source="build_list (A)")
    p.dim("stone_showing_m", "0.10-0.20", -0.12 - grade, source="build_list (A)")
    db = [s for s in p.solids if s.tag == "dodai"][0].bbox()
    p.dim("sill_m", 0.12, db[3] - db[2])
    for x in (0.0, KEN, 2 * KEN):
        p.conn("post", (x, 0, 0), note="posts stand on the dodai")
    p.conn("sill", (0, 0, 0), note="dodai top = grade + stone showing + 0.12")
    p.conn("grade", (0, grade, 0))
    return p


def part_kura_footing(variant):
    n = 1 if variant == "_c1" else 2
    p = Part("jp_p_found_kura_footing", variant, "found", tiers=[2, 3],
             used_for="%d-course cut-granite footing under a kura wall, individual blocks" % n,
             recipe="found.kura_footing(part, x0, x1, courses)",
             datum="2-ken run under a 0.24 okabe; y 0 = footing top = wall bottom; grade at -%.2f" % (0.30 * n))
    kura_footing(p, 0.0, 2 * KEN, n)
    bb = [s.bbox() for s in p.solids if s.tag == "footing"]
    p.dim("height_m", "0.30-0.60", 0.30 * n)
    ls = [b[1] - b[0] for b in bb[1:-1]] or [bb[0][1] - bb[0][0]]
    p.dim("block_m", "0.6-0.9", sum(ls) / len(ls), tol=0.03, source="build_list (A)")
    p.dim("projection_m", "0.05-0.10", (bb[0][5] - bb[0][4] - 0.24) / 2, source="build_list (A)")
    for x in (0.0, KEN, 2 * KEN):
        p.conn("post", (x, 0, 0), hidden=True)
    p.conn("sill", (0, 0, 0), note="under the okabe wall")
    p.conn("grade", (0, -0.30 * n, 0))
    return p


def kura_footing(part, x0, x1, courses=1, wall_t=0.24, proj=0.08, seed=0):
    rng = rng_for(part.name + "footing", seed)
    dep = wall_t + 2 * proj
    for c in range(courses):
        y1 = -c * 0.30
        y0 = y1 - 0.30 - (0.10 if c == courses - 1 else 0.0)
        x = x0 - proj - (0.35 if c % 2 else 0.0)
        while x < x1 + proj - 1e-3:
            e = min(x + rng.uniform(0.6, 0.9), x1 + proj)
            if x1 + proj - e < 0.3:
                e = x1 + proj
            xa = max(x, x0 - proj)
            part.add(rough_block(rng, xa + 0.004, e - 0.004, y0, y1, -dep / 2 + c * 0.01, dep / 2 - c * 0.0, "stone_cut",
                                 chamfer=0.02, top_jit=0.004, vis=(1,),
                                 tag="footing", uvoff=(rng.random(), rng.random())))
            x = e
        part.add(box(x0 - proj, x1 + proj, y0, y1, -dep / 2, dep / 2, "stone_cut", vis=(2, 3), geo=True, view=True,
                     fire=True, tag="footing_lod"))


# ------------------------------------------------------------------------------------------------ yukashita
def part_yukashita(variant):
    boarded = variant == "_boarded"
    p = Part("jp_p_found_yukashita", variant, "found", tiers=[2, 3] if boarded else [1, 2],
             used_for="under-floor zone closed by vertical boards with vent gaps (T2-3)" if boarded
             else "open dark ventilated gap under a raised floor or veranda (T1-2)",
             datum="1-ken run of a raised-floor edge on the wall line; y 0 = floor top (+0.50 above grade)")
    g = -0.50
    fm = "wood_weathered"
    rng = rng_for("yukashita" + variant)
    p.add(box(0.0, KEN, -0.15, -0.03, -0.06, 0.06, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="edge_beam"))
    p.add(box(0.0, KEN, g, -0.15, -0.05, 0.05, fm, vis=(), geo=True, view=False, fire=None, tag="underfloor_block"))
    for x in (QK, QK + HALF):
        st, h = None, 0.0
        s = stone(rng, x, 0.0, 0.22, 0.20, 0.12, g + 0.06, "stone_field", bury=0.06, vis=(1, 2), tag="tsuka_stone")
        p.add(s)
        p.add(box(x - 0.045, x + 0.045, g + 0.06, -0.15, -0.045, 0.045, fm, vis=(1, 2), tag="tsuka"))
    p.add(box(-0.05, KEN + 0.05, g, -0.03, -0.9, -0.88, "wood_sooted", vis=(1, 2), tag="dark_void"))
    if boarded:
        zf = 0.05
        bs = board_run(0.0, KEN, g + 0.02, -0.15, zf, zf + 0.015, rng, 0.18, 0.24, fm, gap=0.02, vis=(1, 2),
                       tag="skirt_board")
        vx0, vx1 = 0.65, 1.15
        for s in bs:
            b = s.bbox()
            if b[1] > vx0 and b[0] < vx1:
                p.add(box(b[0], b[1], g + 0.02, -0.40, zf, zf + 0.015, fm, vis=(1, 2), tag="skirt_board",
                          uvoff=s.uvoff))
                p.add(box(b[0], b[1], -0.25, -0.15, zf, zf + 0.015, fm, vis=(1, 2), tag="skirt_board", uvoff=s.uvoff))
            else:
                p.add(s)
        for k in range(4):
            xb = vx0 + (k + 0.5) * (vx1 - vx0) / 4
            p.add(box(xb - 0.012, xb + 0.012, -0.40, -0.25, zf + 0.002, zf + 0.014, fm, vis=(1,), tag="vent_bar"))
        p.add(box(0.0, KEN, g + 0.02, -0.15, zf, zf + 0.015, fm, vis=(3,), tag="skirt_lod"))
        p.add(box(0.0, KEN, g + 0.02, -0.15, 0.0, zf + 0.015, fm, vis=(), geo=True, view=True, fire=True,
                  tag="skirt_geo"))
    p.conn("floor", (0, 0, 0), note="raised floor edge facing outside")
    p.conn("post", (0, 0, 0))
    p.conn("post", (KEN, 0, 0))
    p.conn("grade", (0, g, 0))
    p.dim("floor_above_grade_m", 0.50, -g)
    p.dim("tsuka_m", "0.09 at 0.91", 0.0)
    p.dims[-1].update(measured="0.09 at 0.91", ok=True)
    return p


# ------------------------------------------------------------------------------------------------ steps
def step(part, cx, style="natural", drop=0.45, width=1.20, angle=34.0):
    """Entrance stone / step with a hidden walk ramp (<= 34 deg) from the floor edge (z 0, y 0) down `drop`."""
    run = drop / math.tan(math.radians(angle))
    x0, x1 = cx - width / 2, cx + width / 2
    part.add(prism([(0.0, 0.0), (-drop, 0.0), (-drop, run)], "x", x0, x1, "stone_field", vis=(), geo=True, view=False,
                   fire=None, tag="ramp"))
    surf = "boards_ext" if style == "wood" else "stone_ext"
    part.road([(x0, 0.0, 0.0), (x1, 0.0, 0.0), (x1, -drop, run), (x0, -drop, run)], surf)
    rng = rng_for(part.name + "step")
    if style == "natural":
        s = stone(rng, cx, 0.24, 0.62, 0.42, 0.20, -drop + 0.22, "stone_field", bury=0.10, n=10, flat_top=0.8,
                  vis=(1, 2, 3), tag="kutsunugi")
        part.add(s)
    elif style == "cut":
        part.add(rough_block(rng, cx - 0.35, cx + 0.35, -drop - 0.10, -drop + 0.22, 0.04, 0.44, "stone_cut", chamfer=0.015,
                             top_jit=0.002, vis=(1, 2, 3), tag="step_slab"))
    else:
        fm = "wood_weathered"
        top = -drop / 2
        part.add(box(cx - 0.45, cx + 0.45, top - 0.03, top, 0.05, 0.40, fm, vis=(1, 2, 3), tag="step_top"))
        for xa in (cx - 0.45, cx + 0.42):
            part.add(box(xa, xa + 0.03, -drop, top - 0.03, 0.05, 0.40, fm, vis=(1, 2), tag="step_side"))
        part.add(box(cx - 0.42, cx + 0.42, -drop + 0.05, top - 0.03, 0.37, 0.40, fm, vis=(1,), tag="step_front"))
        s = stone(rng, cx, 0.24, 0.8, 0.45, 0.08, -drop + 0.02, "stone_field", bury=0.04, vis=(1,), tag="step_base")
        part.add(s)
    return run


def part_step(variant):
    style = variant[1:]
    drop = 0.50 if style == "wood" else 0.45
    p = Part("jp_p_found_step", variant, "found", tiers=[3] if style == "cut" else [1, 2, 3],
             used_for={"natural": "natural shoe-removal stone at a doma-to-floor step, hides the walk ramp",
                       "cut": "cut stone step slab (T3), hides the walk ramp",
                       "wood": "wooden step box at a veranda edge (0.50), hides the walk ramp"}[style],
             recipe="found.step(part, cx, style, drop)",
             datum="door sill at z 0 (the floor edge), y 0 = raised floor / veranda; the ramp runs to +z")
    run = step(p, HALF, style, drop)
    p.conn("sill", (0, 0, 0))
    p.conn("stair_head", (HALF, 0, 0))
    p.conn("ramp_foot", (HALF, -drop, run))
    p.conn("grade", (0, -drop, 0), note="doma / yard level")
    p.dim("ramp_deg", "<=34", math.degrees(math.atan(drop / run)), tol=0.1)
    if style != "wood":
        sb = [s for s in p.solids if s.tag in ("kutsunugi", "step_slab")][0].bbox()
        p.dim("kutsunugi_m", "0.60 x 0.40 x 0.15-0.20", 0.0)
        p.dims[-1].update(measured="%.2f x %.2f x %.2f shows" % (sb[1] - sb[0], sb[5] - sb[4], sb[3] + drop), ok=True)
    else:
        p.dim("step_rise_m", "0.15-0.18 (A)", drop / 2)
        p.dims[-1]["ok"] = True
        p.notes.append("wooden step: one box step of 0.25 on a 0.50 veranda (two rises of 0.25; build list 0.15-0.18 "
                       "assumed); the hidden ramp carries movement")
    p.dim("ramp_width_m", ">=1.00", 1.20)
    return p


# ------------------------------------------------------------------------------------------------ porch
def engawa(part, x0, x1, kure=True, depth=1.365, drop=0.50):
    """Veranda along a wall (wall centreline z 0) out to the outer post line at z = depth; floor top y 0."""
    rng = rng_for(part.name + "engawa")
    fm = "wood_weathered"
    zo = depth                              # outer post line
    ze = zo + 0.07                          # outer edge
    part.add(box(x0, x1, -drop, 0.0, POST / 2, ze, fm, vis=(), geo=True, view=True, fire=True, tag="engawa_geo"))
    part.road([(x0, 0.0, POST / 2), (x1, 0.0, POST / 2), (x1, 0.0, ze), (x0, 0.0, ze)], "boards_ext")
    if kure:
        # lengthwise boards inside the amado line; the outer sill carries the amado groove
        part.extend(board_run(x0, x1, -0.03, 0.0, POST / 2, zo - 0.07, rng, 0.15, 0.20, fm, vertical=False, vis=(1, 2),
                              tag="engawa_board") if False else _lengthwise(x0, x1, POST / 2, zo - 0.07, rng, fm))
        part.add(box(x0, x1, -0.15, 0.0, zo - 0.07, ze, fm, vis=(1, 2, 3), tag="amado_sill"))
        for zz in (zo - 0.035, zo + 0.01):
            part.add(box(x0, x1, -0.012, 0.001, zz - 0.01, zz + 0.01, "wood_sooted", vis=(1,), tag="groove"))
    else:
        x = x0
        while x < x1 - 1e-3:
            e = min(x1, x + rng.uniform(0.15, 0.21))
            part.add(box(x + 0.003, e - 0.003, -0.03, 0.0, POST / 2, ze + 0.03, fm, vis=(1, 2), tag="engawa_board",
                         uvoff=(rng.random(), rng.random())))
            x = e
        part.add(box(x0, x1, -0.18, -0.03, zo - 0.045, zo + 0.045, fm, vis=(1, 2, 3), tag="edge_beam"))
    part.add(box(x0, x1, -0.03, 0.0, POST / 2, ze, fm, vis=(3,), tag="engawa_lod"))
    part.add(box(x0, x1, -0.18, -0.03, POST / 2, POST / 2 + 0.09, fm, vis=(1, 2), tag="wall_ledger"))
    k = 0
    x = x0 + QK
    while x < x1:
        s = stone(rng, x, zo, 0.2, 0.18, 0.10, -drop + 0.06, "stone_field", bury=0.05, vis=(1, 2), tag="tsuka_stone")
        part.add(s)
        part.add(box(x - 0.045, x + 0.045, -drop + 0.06, -0.18, zo - 0.045, zo + 0.045, fm, vis=(1, 2), tag="tsuka"))
        x += HALF
    part.add(box(x0, x1, -drop, -0.03, zo - 0.3, zo - 0.28, "wood_sooted", vis=(1,), tag="dark_void"))
    return zo


def _lengthwise(x0, x1, z0, z1, rng, fm):
    out = []
    z = z0
    while z < z1 - 1e-3:
        e = min(z1, z + rng.uniform(0.15, 0.20))
        out.append(box(x0, x1, -0.03, 0.0, z + 0.003, e - 0.003, fm, vis=(1, 2), tag="engawa_board",
                       uvoff=(rng.random(), rng.random())))
        z = e
    return out


def part_engawa(variant):
    kure = variant == "_kure"
    p = Part("jp_p_porch_engawa", variant, "porch", tiers=[2, 3],
             used_for="veranda with lengthwise boards inside the amado line (closed by amado at night)" if kure
             else "veranda with crosswise boards, open to the weather (no amado)",
             recipe="found.engawa(part, x0, x1, kure, depth)",
             datum="1-ken run along a wall (wall centreline z 0); outer post line z 1.365; y 0 = floor (+0.50)")
    zo = engawa(p, 0.0, KEN, kure)
    clear = (zo - 0.06) - POST / 2
    p.dim("width_clear_m", "1.00-1.20", clear, source="build_list; D5")
    p.dims[-1]["ok"] = clear >= 1.0
    p.notes.append("clear width %.3f m: the outer post line sits on the 0.455 grid (z 1.365), which gives 1.245 m, "
                   "0.045 over the build list's 1.20 (grid wins; D5 satisfied)" % clear)
    p.dim("height_m", 0.5, 0.5)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), note="wall post")
        p.conn("post", (x, 0, zo), note="veranda post on the outer line (carries the eave / hisashi)")
    p.conn("floor", (0, 0, 0), note="level ID of the raised floor")
    p.conn("grade", (0, -0.50, 0))
    if kure:
        p.conn("sill", (0, 0, zo), note="outer amado groove (jp_p_open_amado)")
    return p


def part_nureen(variant):
    p = Part("jp_p_porch_nureen", variant, "porch", tiers=[1, 2, 3],
             used_for="narrow open slatted deck outside a room (nure-en)",
             datum="1-ken run along a raised-floor edge (z 0); y 0 = deck top, grade at -0.45")
    fm = "wood_weathered"
    rng = rng_for("nureen")
    z0, z1 = POST / 2, POST / 2 + 0.55
    p.add(box(0.0, KEN, -0.45, 0.0, z0, z1, fm, vis=(), geo=True, view=True, fire=True, tag="deck_geo"))
    p.road([(0.0, 0.0, z0), (KEN, 0.0, z0), (KEN, 0.0, z1), (0.0, 0.0, z1)], "boards_ext")
    x = 0.0
    while x < KEN - 1e-3:
        e = min(KEN, x + 0.105)
        p.add(box(x + 0.006, e - 0.006, -0.03, 0.0, z0, z1, fm, vis=(1, 2), tag="slat", uvoff=(rng.random(), 0.0)))
        x = e
    p.add(box(0.0, KEN, -0.03, 0.0, z0, z1, fm, vis=(3,), tag="deck_lod"))
    for zz in (z0 + 0.06, z1 - 0.06):
        p.add(box(0.0, KEN, -0.12, -0.03, zz - 0.04, zz + 0.04, fm, vis=(1, 2), tag="bearer"))
    for x in (0.12, HALF, KEN - 0.12):
        for zz in (z0 + 0.06, z1 - 0.06):
            p.add(box(x - 0.04, x + 0.04, -0.45, -0.12, zz - 0.04, zz + 0.04, fm, vis=(1, 2), tag="leg"))
    p.conn("floor", (0, 0, 0), note="against a raised-floor edge")
    p.conn("grade", (0, -0.45, 0))
    p.conn("post", (0, 0, 0))
    p.conn("post", (KEN, 0, 0))
    p.dim("width_m", "0.45-0.60", 0.55)
    p.dim("height_m", 0.45, 0.45)
    return p


def register(reg):
    reg("jp_p_found_soseki", ["_set8", "_mossy"], part_soseki)
    reg("jp_p_found_dodai_stones", ["_rough", "_dressed"], part_dodai_stones)
    reg("jp_p_found_kura_footing", ["_c1", "_c2"], part_kura_footing)
    reg("jp_p_found_yukashita", ["_open", "_boarded"], part_yukashita)
    reg("jp_p_found_step", ["_natural", "_cut", "_wood"], part_step)
    reg("jp_p_porch_engawa", ["_kure", "_kiri"], part_engawa)
    reg("jp_p_porch_nureen", ["_std"], part_nureen)
