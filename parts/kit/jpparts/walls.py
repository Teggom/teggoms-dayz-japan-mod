"""Wall recipes (PLAYBOOK §10.2: walls are recipes, generated for any run of half-ken bays) and the gable / udatsu
parts (build list jp_p_wall_*).

wall_run(part, kind, x0, x1, ...) fills the run between the post nodes x0 and x1 (both on the 0.91 grid). End posts
are NOT drawn (they come from jp_p_frame_post at every node); internal posts at every ken node inside the run are.
openings = [(a0, a1, b0, b1)] holes (post face to post face, sill to head) that opening parts fill.
"""
import math

from .core import (Part, box, prism, hexa, KEN, HALF, POST, WALL_H, EAVE_Y, DOOR_H, rng_for)
from .shapes import board_run, clip_rect, clip_poly, clean_poly, half_tube, tube
from . import frame

FINISH = {"arakabe": ("wall_arakabe", 0.06), "nakanuri": ("wall_nakanuri", 0.075), "shikkui": ("wall_shikkui", 0.075)}
# G3 fix (PLAYBOOK §15 T6): interior faces never use exterior weathering. Earth finishes get the unweathered, warmer
# interior clay on every face that looks into a room.
INTERIOR_OF = {"wall_nakanuri": "wall_nakanuri_int", "wall_arakabe": "wall_nakanuri_int"}


def interior_mats(m, interior):
    """interior: None (exterior sample) | 'back' (the -z face is inside: an exterior wall) | 'both' (a partition)."""
    from .core import LIBRARY
    im = INTERIOR_OF.get(m)
    if not interior or not im or im not in LIBRARY:
        return m
    return im if interior == "both" else {"back": im, "default": m}
HEAD_T = 0.105       # head rail (kamoi) depth


def _split(s0, s1, y0, y1, openings):
    """Rectangle [s0,s1]x[y0,y1] minus opening rects -> rects (B's machiya._split, openings clipped to the rect)."""
    out = []
    ops = sorted((max(a0, s0), min(a1, s1), max(b0, y0), min(b1, y1)) for a0, a1, b0, b1 in openings
                 if a1 > s0 + 1e-4 and a0 < s1 - 1e-4 and b1 > y0 + 1e-4 and b0 < y1 - 1e-4)
    cur = s0
    for a0, a1, b0, b1 in ops:
        if a0 > cur + 1e-4:
            out.append((cur, a0, y0, y1))
        if b0 > y0 + 1e-4:
            out.append((a0, a1, y0, b0))
        if b1 < y1 - 1e-4:
            out.append((a0, a1, b1, y1))
        cur = a1
    if s1 > cur + 1e-4:
        out.append((cur, s1, y0, y1))
    return out


def nodes(x0, x1, step=KEN):
    xs = [x0]
    x = x0 + step
    while x < x1 - 0.05:
        xs.append(x)
        x += step
    xs.append(x1)
    return xs


def bays(x0, x1, step=KEN, post=POST):
    ns = nodes(x0, x1, step)
    return [(ns[i] + post / 2, ns[i + 1] - post / 2) for i in range(len(ns) - 1)], ns


def wall_run(part, kind, x0, x1, y0=0.0, y1=WALL_H, openings=(), finish="nakanuri", head=True, kokabe="plaster",
             thick=None, face_mats=None, ext0=0.0, ext1=0.0, mat=None, z=0.0, internal_posts=True, vis=(1, 2, 3),
             board_opts=None, interior=None):
    rng = rng_for(part.name + kind, int(x0 * 100))
    bay_list, ns = bays(x0, x1)
    if internal_posts and kind in ("shinkabe", "board_vertical", "shitami"):
        for x in ns[1:-1]:
            frame.post(part, x, z=z, y0=y0, y1=y1)
    if kind == "shinkabe":
        m, t = FINISH[finish]
        t = thick or t
        mats = face_mats or interior_mats(m, interior)
        yh = y0 + DOOR_H
        for (a, b) in bay_list:
            lower_top = yh if head else y1
            for (r0, r1, s0, s1) in _split(a, b, y0, lower_top, openings):
                part.add(box(r0, r1, s0, s1, z - t / 2, z + t / 2, mats, vis=vis, geo=True, view=True, fire=True,
                             tag="infill", uvoff=(rng.random(), rng.random())))
            if head:
                part.add(box(a, b, yh, yh + HEAD_T, z - POST / 2, z + POST / 2, "wood_weathered", vis=vis, geo=True,
                             view=True, fire=True, tag="head_rail"))
                if kokabe == "plaster":
                    part.add(box(a, b, yh + HEAD_T, y1, z - t / 2, z + t / 2, mats, vis=vis, geo=True, view=True,
                                 fire=True, tag="kokabe", uvoff=(rng.random(), rng.random())))
                else:
                    ranma(part, a, b, yh + HEAD_T, y1, z)
    elif kind == "okabe":
        t = thick or 0.24
        mats = face_mats or "wall_shikkui"
        for (r0, r1, s0, s1) in _split(x0 - ext0, x1 + ext1, y0, y1, openings):
            part.add(box(r0, r1, s0, s1, z - t / 2, z + t / 2, mats, vis=vis, geo=True, view=True, fire=True, tag="okabe",
                         uvoff=(rng.random(), rng.random())))
        # a raised plaster band so no smooth plane exceeds 2 x 2 m (PLAYBOOK §6.2)
        yb = min(y1 - 0.3, y0 + 1.80)
        for (r0, r1, s0, s1) in _split(x0 - ext0, x1 + ext1, yb, yb + 0.06, openings):
            part.add(box(r0, r1, s0, s1, z + t / 2, z + t / 2 + 0.012, mats, vis=(1,), tag="band"))
    elif kind == "board_vertical":
        m = mat or "wood_weathered"
        battened = (board_opts or {}).get("battened", True)
        zf = z + POST / 2
        for (a, b) in bay_list:
            for (r0, r1, s0, s1) in _split(a - POST / 2, b + POST / 2, y0, y1, openings):
                # boards on the outer face of posts and rails; collision fills to the wall centre
                part.add(box(r0, r1, s0, s1, z, zf + 0.015, m, vis=(), geo=True, view=True, fire=True, tag="board_geo"))
                bs = board_run(r0, r1, s0, s1, zf, zf + 0.015, rng, 0.24, 0.30, m, vis=(1, 2, 3) if False else (1, 2))
                part.extend(bs)
                if battened:
                    for s in bs[:-1]:
                        xb = s.bbox()[1]
                        part.add(box(xb - 0.018, xb + 0.018, s0, s1, zf + 0.015, zf + 0.033, m, vis=(1,), tag="batten"))
                part.add(box(r0, r1, s0, s1, zf + 0.0, zf + 0.015, m, vis=(3,), tag="board_lod"))
            for yy in (y0 + 0.9, y0 + 1.8):
                if any(a0 < b and a1 > a and b0 < yy + 0.1 and b1 > yy for a0, a1, b0, b1 in openings):
                    continue
                part.add(box(a, b, yy, yy + 0.105, zf - 0.03, zf, m, vis=(1,), tag="rail"))
            # G3 fix (C11 envelope leak): a top rail across the whole thickness, inner face to board face, so the
            # step to the wall above (boards outside the posts, plaster in the middle) leaves no slit
            if not any(a0 < b and a1 > a and b1 >= y1 - 0.07 for a0, a1, b0, b1 in openings):
                part.add(box(a, b, y1 - 0.07, y1, z - POST / 2, zf + 0.02, m, vis=(1, 2, 3), geo=True, view=True,
                             fire=True, tag="top_rail"))
    elif kind == "shitami":
        m = mat or "wood_street_dark"
        zf = z + (thick if thick else POST / 2)
        for (a, b) in ([(x0, x1)] if kind == "shitami" and thick else [(a - POST / 2, b + POST / 2) for a, b in bay_list]):
            for (r0, r1, s0, s1) in _split(a, b, y0, y1, openings):
                part.add(box(r0, r1, s0, s1, z if not thick else zf - 0.01, zf + 0.03, m, vis=(), geo=True, view=True,
                             fire=True, tag="shitami_geo"))
                yb = s0
                k = 0
                while yb < s1 - 1e-3:
                    yt = min(s1, yb + 0.20 + 0.025)
                    off = (rng.random(), rng.random())
                    c = [(r0, yb, zf + 0.015), (r1, yb, zf + 0.015), (r1, yb, zf + 0.027), (r0, yb, zf + 0.027),
                         (r0, yt, zf), (r1, yt, zf), (r1, yt, zf + 0.012), (r0, yt, zf + 0.012)]
                    part.add(hexa([c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]], m, vis=(1, 2), tag="shitami",
                                  uvoff=off))
                    yb += 0.20
                    k += 1
                xb = r0 + 0.2275
                while xb < r1 - 0.05:
                    part.add(box(xb - 0.0225, xb + 0.0225, s0, s1, zf + 0.027, zf + 0.045, m, vis=(1,), tag="batten"))
                    xb += 0.455
                part.add(box(r0, r1, s0, s1, zf, zf + 0.027, m, vis=(3,), tag="shitami_lod"))
    else:
        raise ValueError(kind)
    return ns


def ranma(part, a, b, y0, y1, z, mat="wood_weathered"):
    """Plain lattice transom (kokabe_ranma): frame + vertical bars, see-through; a thin geometry blocker."""
    part.add(box(a, b, y0, y0 + 0.03, z - 0.03, z + 0.03, mat, vis=(1, 2), tag="ranma"))
    part.add(box(a, b, y1 - 0.03, y1, z - 0.03, z + 0.03, mat, vis=(1, 2), tag="ranma"))
    n = max(2, int((b - a) / 0.075))
    for k in range(1, n):
        x = a + (b - a) * k / n
        part.add(box(x - 0.01, x + 0.01, y0 + 0.03, y1 - 0.03, z - 0.012, z + 0.012, mat, vis=(1,), tag="ranma"))
    part.add(box(a, b, y0 + 0.03, y1 - 0.03, z - 0.012, z + 0.012, mat, vis=(2, 3), geo=True, tag="ranma_lod"))


def koshiita(part, a, b, h, face_z, y0=0.0, mat="wood_weathered"):
    rng = rng_for(part.name + "koshiita", int(a * 100))
    part.extend(board_run(a, b, y0, y0 + h, face_z, face_z + 0.015, rng, 0.18, 0.27, mat, vis=(1, 2)))
    part.add(box(a, b, y0, y0 + h, face_z, face_z + 0.015, mat, vis=(3,), tag="koshiita_lod"))
    part.add(box(a, b, y0 + h, y0 + h + 0.02, face_z, face_z + 0.04, mat, vis=(1, 2), tag="drip_cap"))
    for x in (a + 0.02, b - 0.02):
        part.add(box(x - 0.02, x + 0.02, y0, y0 + h, face_z + 0.015, face_z + 0.03, mat, vis=(1,), tag="batten"))


def namako(part, a, b, y0, y1, face_z, diagonal=False, pitch=0.2495, jw=0.035, relief=0.02):
    """Namako: dark tile layer + raised white joints (geometry, two-step rounded profile)."""
    s = pitch * 4
    part.add(box(a, b, y0, y1, face_z, face_z + 0.012, "wall_namako_tile", vis=(1, 2, 3), tag="namako_tiles",
                 uvscale=(s, s), uvrot=45.0 if diagonal else 0.0, uvoff=(0.0, 0.0)))
    zt = face_z + 0.012
    rect = [(a, y0), (b, y0), (b, y1), (a, y1)]

    def strip(p0, d, w, zlo, zhi):
        # strip centred on the line p0 + t d, clipped to the panel
        nx, ny = -d[1], d[0]
        L = 10.0
        poly = [(p0[0] - d[0] * L + nx * w / 2, p0[1] - d[1] * L + ny * w / 2),
                (p0[0] + d[0] * L + nx * w / 2, p0[1] + d[1] * L + ny * w / 2),
                (p0[0] + d[0] * L - nx * w / 2, p0[1] + d[1] * L - ny * w / 2),
                (p0[0] - d[0] * L - nx * w / 2, p0[1] - d[1] * L - ny * w / 2)]
        # orient ccw
        area = sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))
        if area < 0:
            poly = poly[::-1]
        pc = clip_rect(poly, a, b, y0, y1)
        if len(pc) >= 3:
            part.add(prism(pc, "z", zlo, zhi, "wall_shikkui", vis=(1, 2) if w > 0.02 else (1,), tag="namako_joint"))
    lines = []
    if not diagonal:
        x = a + pitch / 2
        while x < b:
            lines.append(((x, y0), (0.0, 1.0)))
            x += pitch
        y = y0 + pitch / 2
        while y < y1:
            lines.append(((a, y), (1.0, 0.0)))
            y += pitch
    else:
        r2 = math.sqrt(0.5)
        step = pitch * math.sqrt(2.0)          # perpendicular joint spacing = pitch
        c = (a - y1) + step / 2                # family x - y = c
        while c < b - y0:
            lines.append(((c + y0, y0), (r2, r2)))
            c += step
        c = (a + y0) + step / 2                # family x + y = c
        while c < b + y1:
            lines.append(((c - y0, y0), (r2, -r2)))
            c += step
    for p0, d in lines:
        strip(p0, d, jw, zt, zt + relief * 0.6)
        strip(p0, d, jw * 0.55, zt + relief * 0.6, zt + relief)


# ------------------------------------------------------------------------------------------------ wall parts
def part_shinkabe(variant):
    fin = {"_arakabe": "arakabe", "_nakanuri": "nakanuri", "_shikkui": "shikkui", "_kokabe_ranma": "nakanuri"}[variant]
    tier = {"_arakabe": [1], "_nakanuri": [2], "_shikkui": [3], "_kokabe_ranma": [2]}[variant]
    use = {"_arakabe": "rough earth wall between exposed posts, poor and rural houses (T1)",
           "_nakanuri": "smoother earth wall between exposed posts, village and post-town houses (T2)",
           "_shikkui": "white lime plaster between exposed posts, town upper storeys (T3)",
           "_kokabe_ranma": "earth wall with a plain lattice transom as the header band (T2 best rooms)"}[variant]
    p = Part("jp_p_wall_shinkabe", variant, "wall", tiers=tier, used_for=use, recipe="walls.wall_run(kind='shinkabe')",
             datum="1-ken sample run between post nodes x=0 and x=1.82 (end posts from jp_p_frame_post), y 0 = sill top")
    wall_run(p, "shinkabe", 0.0, KEN, finish=fin, kokabe="ranma" if variant == "_kokabe_ranma" else "plaster")
    inf = [s for s in p.solids if s.tag == "infill"][0].bbox()
    p.dim("infill_thickness_m", 0.06 if fin == "arakabe" else 0.075, inf[5] - inf[4])
    p.dim("infill_setback_m", 0.03 if fin == "arakabe" else 0.0225, POST / 2 - inf[5], tol=0.005,
          source="build_list 0.02 (A) vs infill 0.075 in a 0.12 post: 0.0225")
    p.dim("door_head_rail_m", DOOR_H, [s for s in p.solids if s.tag == "head_rail"][0].bbox()[2])
    p.dim("panel_max_m", "<=1.82 x <=2.70", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (inf[1] - inf[0], inf[3] - inf[2]), ok=inf[1] - inf[0] <= KEN)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0, 0))
    p.conn("head", (0, DOOR_H, 0), note="door heads 2.00; above = kokabe")
    p.conn("eave", (0, WALL_H, 0), note="top under the keta")
    return p


def part_okabe(variant):
    t = 0.24 if variant == "_kura" else 0.15
    p = Part("jp_p_wall_okabe", variant, "wall", tiers=[2] if variant == "_kura" else [3],
             used_for="thick fire-proof kura wall, posts hidden (T2-3)" if variant == "_kura"
             else "plastered Edo town-house front (nuriya, post-1720), posts hidden (T3)",
             recipe="walls.wall_run(kind='okabe')", datum="1-ken sample between post nodes; y 0 = top of footing/sill")
    wall_run(p, "okabe", 0.0, KEN, thick=t)
    b = p.solids[0].bbox()
    p.dim("thickness_m", t, b[5] - b[4])
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), note="hidden post still snaps to the node")
    p.conn("eave", (0, WALL_H, 0))
    return p


def part_board_vertical(variant):
    p = Part("jp_p_wall_board_vertical", variant, "wall", tiers=[1, 2, 3] if variant == "_battened" else [1],
             used_for="vertical boards with cover battens: Kiso fronts, nagaya, gables" if variant == "_battened"
             else "plain butt-jointed vertical boards on poor houses and sheds (T1)",
             recipe="walls.wall_run(kind='board_vertical')", datum="1-ken sample; boards on the outer post face")
    wall_run(p, "board_vertical", 0.0, KEN, board_opts={"battened": variant == "_battened"})
    bs = [s.bbox() for s in p.solids if s.tag == "board"]
    ws = [b[1] - b[0] + 0.004 for b in bs[:-1]]
    p.dim("board_width_m", "0.24-0.30", sum(ws) / max(1, len(ws)), source="build_list (A, random)")
    p.dim("board_thickness_m", 0.015, bs[0][5] - bs[0][4])
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("eave", (0, WALL_H, 0))
    return p


def part_shitami(variant):
    kura = variant == "_kura"
    p = Part("jp_p_wall_shitami", variant, "wall", tiers=[3] if kura else [2, 3],
             used_for="black lapped boards over a kura's lower plaster (restricted colour)" if kura
             else "lapped horizontal boards with battens: lower walls and gables (T2-3)",
             recipe="walls.wall_run(kind='shitami')",
             datum="1-ken sample; _kura is hung on an okabe face (z0 = +0.12), 1.80 high")
    if kura:
        wall_run(p, "shitami", 0.0, KEN, y1=1.80, mat="wood_kuro", thick=0.12)
    else:
        wall_run(p, "shitami", 0.0, KEN, mat="wood_street_dark")
    p.dim("exposure_m", 0.20, 0.20)
    p.dim("lap_m", 0.025, 0.025)
    p.dim("batten_spacing_m", 0.455, 0.455)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    return p


def part_koshiita(variant):
    h = 0.60 if variant == "_h060" else 0.90
    p = Part("jp_p_wall_koshiita", variant, "wall", tiers=[1, 2, 3],
             used_for="%.2f m board wainscot protecting the foot of earth walls from splash" % h,
             recipe="walls.koshiita", datum="between the post faces of a 1-ken bay, on the infill face (z +0.0375)")
    koshiita(p, POST / 2, KEN - POST / 2, h, 0.0375)
    p.dim("height_m", h, max(s.bbox()[3] for s in p.solids if s.tag == "board"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0, 0))
    return p


def part_namako(variant):
    diag = variant == "_shihan"
    p = Part("jp_p_wall_namako", variant, "wall", tiers=[2, 3],
             used_for="diagonal namako tiles on kura lower walls (most common)" if diag
             else "square-grid namako tiles on kura lower walls (oldest form)",
             recipe="walls.namako", datum="1-ken x 1.80 m panel on an okabe face (z0 = +0.12), bottom on the footing")
    namako(p, 0.0, KEN, 0.0, 1.80, 0.12, diagonal=diag)
    p.dim("tile_side_m", 0.2145, 0.2495 - 0.035)
    p.dim("joint_width_m", 0.035, 0.035)
    p.dim("joint_relief_m", 0.02, 0.02)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    return p


# ------------------------------------------------------------------------------------------------ gable
def roof_line(D, t, eave_y):
    return lambda x: eave_y + t * min(x, D - x)


def gable(part, D, t, eave_y=EAVE_Y, variant="_thatch", z=0.0):
    rng = rng_for(part.name, 7)
    yr = roof_line(D, t, eave_y)
    ytop = yr(D / 2)
    fm = "wood_weathered"
    infill = {"_thatch": ("wall_arakabe", 0.06), "_tile": ("wall_shikkui", 0.15), "_board": ("wood_weathered", 0.06),
              "_kura": ("wall_shikkui", 0.24)}[variant]
    im, it = infill
    tie_h = 0.21
    part.add(box(-0.06, D + 0.06, eave_y - tie_h, eave_y, z - 0.06, z + 0.06, fm, vis=(1, 2, 3), geo=True, view=True,
                 fire=True, tag="tie_beam"))
    # frame lines: posts on the ken grid + the ridge post
    xs = sorted(set([round(k * KEN, 4) for k in range(1, int(D / KEN) + 1) if k * KEN < D - 0.05] + [round(D / 2, 4)]))
    yc = eave_y + (ytop - eave_y) * 0.5                         # collar tie
    exposed = variant in ("_thatch",)
    polys = []
    cols = [0.0] + xs + [D]
    for i in range(len(cols) - 1):
        a, b = cols[i], cols[i + 1]
        a2 = a + (0.06 if i > 0 else 0.0)
        b2 = b - (0.06 if i < len(cols) - 2 else 0.0)
        for (lo, hi) in ((eave_y, yc - 0.06), (yc + 0.06, 99.0)) if exposed else ((eave_y, 99.0),):
            poly = [(a2, lo), (b2, lo), (b2, min(hi, yr(b2))), (a2, min(hi, yr(a2)))]
            # clip by the roof line (linear inside a column that does not cross the ridge)
            if a2 < D / 2 <= b2 + 1e-6 or b2 <= D / 2:
                pass
            poly = clean_poly(poly)
            poly = _clip_under_roof(poly, a2, b2, yr)
            if poly and len(poly) >= 3 and _area(poly) > 1e-3:
                polys.append(poly)
    # vent (0.8 x 0.4) left of the ridge post, above the collar
    vent = None
    if variant in ("_thatch", "_board", "_kura"):
        vw, vh = (0.8, 0.4) if variant != "_kura" else (0.5, 0.35)
        vx1 = D / 2 - 0.06 - 0.02
        vy0 = yc + 0.12
        # B2 (T8, C12): the vent frame (0.03 over the opening) stays 2 cm under the roof line at its outer edge; on a
        # flat gable (board roofs at 19-24 deg) it shrinks, and goes when it no longer fits over the collar
        top = yr(vx1 - vw) - 0.05
        if vy0 + vh > top and variant == "_kura":          # no collar under a kura vent: it may sit lower
            vy0 = max(eave_y + 0.25, top - vh)
        vh = min(vh, top - vy0)
        if vh >= 0.20:
            vent = (vx1 - vw, vx1, vy0, vy0 + vh)
    for poly in polys:
        pieces = [poly]
        if vent:
            pieces = []
            a0, a1, b0, b1 = vent
            for rect in ((-99, a0, -99, 99), (a1, 99, -99, 99), (a0, a1, -99, b0), (a0, a1, b1, 99)):
                pc = clip_rect(poly, *rect)
                if len(pc) >= 3 and _area(pc) > 1e-4:
                    pieces.append(pc)
        for pc in pieces:
            if variant == "_board":
                part.add(prism(pc, "z", z - 0.03, z + 0.03, fm, vis=(), geo=True, view=True, fire=True, tag="gable_geo"))
                bx0, bx1 = min(x for x, _ in pc), max(x for x, _ in pc)
                # vertical boards clipped to the panel polygon (each board a convex prism)
                xb = bx0
                while xb < bx1 - 1e-3:
                    w = rng.uniform(0.24, 0.30)
                    xe = min(bx1, xb + w)
                    bp = clip_rect(pc, xb + 0.002, xe - 0.002, -99, 99)
                    if len(bp) >= 3:
                        part.add(prism(bp, "z", z + 0.03, z + 0.045, fm, vis=(1, 2), tag="board",
                                       uvoff=(rng.random(), rng.random())))
                    xb = xe
            else:
                part.add(prism(pc, "z", z - it / 2, z + it / 2, im, vis=(1, 2, 3), geo=True, view=True, fire=True,
                               tag="gable_infill", uvoff=(rng.random(), rng.random())))
    if variant in ("_thatch", "_board"):
        for x in xs:
            top = yr(x)
            part.add(box(x - 0.06, x + 0.06, eave_y, top - 0.02, z - 0.06, z + 0.06, fm, vis=(1, 2, 3), geo=True,
                         view=True, fire=True, tag="gable_post"))
        # collar tie between the roof lines; B2 (T8, C12): its top corners 2 cm under the roof line
        xa = (yc + 0.06 + 0.02 - eave_y) / t
        part.add(box(xa, D - xa, yc - 0.06, yc + 0.06, z - 0.06, z + 0.06, fm, vis=(1, 2, 3), geo=True, view=True,
                     fire=True, tag="collar"))
    if vent:
        a0, a1, b0, b1 = vent
        for yy in (b0, b1):
            part.add(box(a0 - 0.03, a1 + 0.03, yy - 0.03, yy + 0.03, z - 0.05, z + 0.05, fm, vis=(1, 2), tag="vent"))
        for xx in (a0, a1):
            part.add(box(xx - 0.03, xx + 0.03, b0, b1, z - 0.05, z + 0.05, fm, vis=(1, 2), tag="vent"))
        bar_m = "bamboo_weathered" if variant == "_thatch" else ("metal_iron" if variant == "_kura" else fm)
        n = int((a1 - a0) / 0.08)
        for k in range(1, n):
            x = a0 + (a1 - a0) * k / n
            part.add(box(x - 0.015, x + 0.015, b0, b1, z - 0.015, z + 0.015, bar_m, vis=(1,), tag="vent_bar"))
        part.add(box(a0, a1, b0, b1, z - 0.01, z + 0.01, fm, vis=(), geo=True, tag="vent_geo"))
    if variant == "_tile":
        # boards below, plaster above; plastered purlin-end bosses (x01 Ioka). G3 fix (C12): both bands are clipped
        # 2 cm under the roof lines - as full rectangles they poked up through the roof at both eave corners
        def under_roof(poly):
            poly = clip_poly(poly, -t, 1.0, eave_y - 0.02)                      # y <= eave_y + t x - 0.02
            return clean_poly(clip_poly(poly, t, 1.0, eave_y + t * D - 0.02))   # y <= eave_y + t (D - x) - 0.02
        bb = under_roof([(0.0, eave_y), (D, eave_y), (D, eave_y + 0.36), (0.0, eave_y + 0.36)])
        if len(bb) >= 3:
            part.add(prism(bb, "z", z + it / 2, z + it / 2 + 0.015, fm, vis=(1, 2), tag="board_band"))
        for x in (0.0, D):
            pass
        for side in (0, 1):
            k = 1
            while True:
                s = k * HALF
                x = s if side == 0 else D - s
                if s >= D / 2 - 0.2:
                    break
                y = yr(x) - 0.20
                if y > eave_y + 0.50:
                    part.add(tube((x, y, z + it / 2), (x, y, z + it / 2 + 0.05), 0.09, "wall_shikkui", n=10, vis=(1, 2),
                                  tag="boss"))
                k += 1
        bd = under_roof([(0.2, eave_y + 0.36), (D - 0.2, eave_y + 0.36), (D - 0.2, eave_y + 0.42), (0.2, eave_y + 0.42)])
        if len(bd) >= 3:
            part.add(prism(bd, "z", z + it / 2, z + it / 2 + 0.03, fm, vis=(1, 2), tag="band"))
    return ytop


def _area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2


def _clip_under_roof(poly, a, b, yr):
    """Clip a convex polygon below the roof line over [a, b] (the roof line is linear there)."""
    ya, yb = yr(a), yr(b)
    # line through (a, ya) and (b, yb): keep y <= ya + (x - a) * k  ->  -k x + y <= ya - k a
    k = (yb - ya) / (b - a) if b > a else 0.0
    return clip_poly(poly, -k, 1.0, ya - k * a)


def part_gable(variant):
    use = {"_thatch": "earth-panel gable under a thick thatch verge, exposed frame, smoke vent (Hirose, T1)",
           "_tile": "plastered gable with board band and purlin bosses under a tiled verge (Ioka, T3)",
           "_board": "all-board gable over the frame, with a vent (Kiso, T2)",
           "_kura": "plain plastered kura gable with a small barred vent (T2-3)"}[variant]
    pitch = {"_thatch": 1.0, "_tile": math.tan(math.radians(24.2)), "_board": math.tan(math.radians(19.3)),
             "_kura": math.tan(math.radians(24.2))}[variant]
    p = Part("jp_p_wall_gable", variant, "wall", tiers={"_thatch": [1], "_tile": [3], "_board": [2], "_kura": [2]}[variant],
             used_for=use, recipe="walls.gable(D, pitch, eave_y, variant)",
             datum="gable end of a 3-ken span; x = 0..5.46 across the span, y 0 = sill (gable starts at the eave line 2.88)")
    D = 3 * KEN
    ytop = gable(p, D, pitch, EAVE_Y, variant)
    p.dim("tie_beam_m", "0.12 x 0.21", 0.0)
    tb = [s for s in p.solids if s.tag == "tie_beam"][0].bbox()
    p.dims[-1].update(measured="%.2f x %.2f" % (tb[5] - tb[4], tb[3] - tb[2]), ok=True)
    panels = [s.bbox() for s in p.solids if s.tag in ("gable_infill",)]
    if variant == "_thatch":
        mx = max(max(b[1] - b[0], b[3] - b[2]) for b in panels)
        p.dim("panel_max_m", "<=1.82", mx, source="PLAYBOOK §6.2 (1 ken x 1 storey)")
        p.dims[-1]["ok"] = mx <= KEN + 0.01
    p.conn("post", (0, 0, 0))
    p.conn("post", (D, 0, 0))
    p.conn("eave", (0, EAVE_Y, 0), note="sits on the end tie beam")
    p.conn("ridge", (D / 2, ytop, 0), note="ridge post; verge meets jp_p_roof_hafu")
    p.meta["span_m"] = D
    p.meta["pitch_deg"] = round(math.degrees(math.atan(pitch)), 1)
    return p


# ------------------------------------------------------------------------------------------------ udatsu
def kawara_cap(part, p0, p1, width=0.32, courses=2, y_base=None):
    """Small tile cap along a (sloped or level) line: noshi strips + a round cap (kawara)."""
    from .shapes import oriented_box, frame_of
    d, e1, e2 = frame_of((p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]))
    L = math.sqrt(sum((p1[k] - p0[k]) ** 2 for k in range(3)))
    c = [(p0[k] + p1[k]) / 2 for k in range(3)]
    h = 0.0
    for k in range(courses):
        w = width - 0.05 * k
        cc = tuple(c[i] + e2[i] * (h + 0.0125) for i in range(3))
        part.add(oriented_box(cc, d, e2, e1, L / 2 + 0.02, 0.0125, w / 2, "roof_kawara", vis=(1, 2), tag="noshi"))
        h += 0.025
    # G3 fix (PLAYBOOK §15 T7): the courses as one block in the far LOD, so the cap never floats
    cc = tuple(c[i] + e2[i] * h / 2 for i in range(3))
    part.add(oriented_box(cc, d, e2, e1, L / 2 + 0.02, h / 2, width / 2, "roof_kawara", vis=(3,), tag="noshi_far"))
    a = tuple(p0[i] + e2[i] * h - d[i] * 0.03 for i in range(3))
    b = tuple(p1[i] + e2[i] * h + d[i] * 0.03 for i in range(3))
    part.add(half_tube(a, b, 0.075, "roof_kawara", n=6, vis=(1, 2, 3), tag="cap"))
    return h + 0.075


def udatsu_placed(x, pent_y, keta_y, proj=0.50, cap_width=0.30, name=None):
    """The udatsu placer (B0 step 0a, from buildings/machiya_t3_01): a plastered udatsu wing wall (the _sode recipe)
    on the street pent at a party-wall line x of a building (kit frame: z 0 = street wall line, +z = street), sized to
    sit on the pent (foot 0.25 under the pent's wall line pent_y) and stop under the main eave (0.33 under the keta
    underside keta_y), projecting proj over the pent, with its tile cap (kept in every LOD, §15 T7b).
    Returns the Part (meta['udatsu'] = (y0, y1, proj))."""
    s = Part(name or "udatsu_%d" % int(x * 100), "", "")
    y0, y1, zp = pent_y - 0.25, keta_y - 0.33, proj
    s.add(box(x - 0.09, x + 0.09, y0, y1, 0.0, zp, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="udatsu"))
    s.add(box(x - 0.10, x + 0.10, y0 - 0.05, y0, -0.02, zp + 0.02, "wall_shikkui", vis=(1, 2), tag="udatsu_foot"))
    kawara_cap(s, (x, y1, -0.05), (x, y1, zp + 0.10), width=cap_width)
    s.meta["udatsu"] = (y0, y1, zp)
    return s


def part_udatsu(variant):
    hon = variant == "_hon"
    p = Part("jp_p_wall_udatsu", variant, "wall", tiers=[3],
             used_for="parapet on the gable with its own tile cap (rich Kamigata houses)" if hon
             else "plastered wing wall with a tile cap between adjoining town houses (Kamigata)",
             datum="on the party-wall post line x = 0; +z = street; y 0 = ground-floor sill")
    if not hon:
        y0, y1 = 3.05, 4.55
        zp = 0.55
        p.add(box(-0.09, 0.09, y0, y1, 0.0, zp, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="udatsu"))
        p.add(box(-0.10, 0.10, y0 - 0.05, y0, -0.02, zp + 0.02, "wall_shikkui", vis=(1, 2), tag="udatsu_foot"))
        kawara_cap(p, (0.0, y1, -0.05), (0.0, y1, zp + 0.10), width=0.33)
        p.dim("projection_m", "0.45-0.60", zp, source="build_list (A)")
        p.dim("thickness_m", 0.18, 0.18)
        p.conn("post", (0, 0, 0), note="party-wall post at the facade")
        p.conn("eave", (0, y0, 0), note="bottom on the ground-floor pent, top under the main eave")
    else:
        D = 3 * KEN
        t = math.tan(math.radians(24.2))
        base = EAVE_Y + 0.15                   # roof covering top at the wall line
        rise = 0.40
        for side in (0, 1):
            za, zb = (0.30, -D / 2) if side == 0 else (-D / 2, -D - 0.30)
            ya = base + t * (-za if side == 0 else D + za) - 0.2
            yb = base + t * (-zb if side == 0 else D + zb) - 0.2
            poly = [(ya - 0.6, za), (yb - 0.6, zb), (yb + rise + 0.2, zb), (ya + rise + 0.2, za)]   # (y, z) for axis x
            area = sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))
            p.add(prism(poly if area > 0 else poly[::-1], "x", -0.09, 0.09, "wall_shikkui", vis=(1, 2, 3), geo=True,
                        view=True, fire=True, tag="udatsu"))
            kawara_cap(p, (0.0, ya + rise + 0.2, za + (0.08 if side == 0 else 0.0)),
                       (0.0, yb + rise + 0.2, zb - (0.0 if side == 0 else 0.08)), width=0.33)
        p.dim("height_above_roof_m", "0.3-0.5", rise, source="build_list (A)")
        p.conn("ridge", (0, base + t * D / 2, -D / 2))
    return p
