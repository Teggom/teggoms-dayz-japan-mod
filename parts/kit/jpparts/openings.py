"""Openings (build list jp_p_open_*): sliding doors in B's proven format, windows, lattices, shop closures.

Every passable door is a 1-ken bay (posts at x = 0 and 1.82, clear 1.70 m between post faces): one leaf covers the
opening and parks along the facade over the NEXT bay (D1: never across a passage). Outside leaves (itado) run on a
track on the exterior face, inside leaves (koshido, shoji) on the interior face. The part carries its tracks over the
park bay; that bay must be a plain wall on the parking face (no wainscot / lattice there) - connector 'park'.
Opening parts fill a hole the wall recipe leaves (walls.wall_run(openings=[...])).
"""
import math

from .core import (Part, Door, box, prism, KEN, HALF, POST, DOOR_H, WALL_H, GAP, OV, sliding_leaf, rng_for, add, mul)
from .shapes import board_run, tube, oriented_box, clip_rect
from . import kawara

A, B = POST / 2, KEN - POST / 2          # 1-ken bay opening between post faces


# ------------------------------------------------------------------------------------------------ shared bits
def tracks(part, x0, x1, z_face, side, thick=0.04, mat="wood_weathered", head_y=DOOR_H):
    """Sill track (flush with the floor) and head track on the face the leaf runs on, over door + park bays."""
    tw = thick + 2 * GAP + 0.02
    z0, z1 = sorted((z_face, z_face + side * tw))
    part.add(box(x0, x1, -0.03, 0.0, z0, z1, mat, vis=(1, 2), tag="track"))
    part.add(box(x0, x1, head_y + 0.035, head_y + 0.14, z0, z1, mat, vis=(1, 2, 3), tag="track"))


def threshold(part, a, b, mat="wood_weathered", depth=POST):
    part.add(box(a, b, -0.10, 0.0, -depth / 2, depth / 2, mat, vis=(1, 2), geo=True, view=False, fire=True,
                 tag="threshold"))
    part.road([(a, 0.0, -depth / 2), (b, 0.0, -depth / 2), (b, 0.0, depth / 2), (a, 0.0, depth / 2)], "boards_ext")


def door_conns(part, bay=KEN, park=KEN, park_side=+1, face="exterior"):
    for x in (0.0, bay):
        part.conn("post", (x, 0, 0))
    part.conn("post", (bay + park if park_side > 0 else -park, 0, 0), note="far end of the park bay")
    part.conn("sill", (0, 0, 0), note="runs in a grooved sill at floor level")
    part.conn("head", (0, DOOR_H, 0))
    part.conn("park", ((bay if park_side > 0 else -park), 0, 0), length=park, face=face,
              note="the next bay must be a plain wall on the %s face: the open leaf parks there" % face)


def leaf_plank(style, mat, rng):
    def build(l0, l1, bot, top, z0, z1, bone):
        out = [box(l0, l1, bot, top, z0, z1, mat, vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
        W = l1 - l0
        zin, zout = (z0, z1)
        if style == "plain":
            for s in board_run(l0, l1, bot, top, z0 + 0.012, z1, rng, 0.20, 0.30, mat, vis=(1,), tag="leaf_board"):
                out.append(s)
            for yy in (bot + 0.25, (bot + top) / 2, top - 0.30):
                out.append(box(l0 + 0.05, l1 - 0.05, yy, yy + 0.09, z0, z0 + 0.012, mat, vis=(1,), tag="leaf_batten"))
        else:
            sw = 0.075
            out.append(box(l0, l0 + sw, bot, top, z0, z1, mat, vis=(1,), tag="stile"))
            out.append(box(l1 - sw, l1, bot, top, z0, z1, mat, vis=(1,), tag="stile"))
            out.append(box(l0 + sw, l1 - sw, bot, bot + 0.10, z0, z1, mat, vis=(1,), tag="rail"))
            out.append(box(l0 + sw, l1 - sw, top - 0.08, top, z0, z1, mat, vis=(1,), tag="rail"))
            for s in board_run(l0 + sw, l1 - sw, bot + 0.10, top - 0.08, z0 + 0.012, z1 - 0.01, rng, 0.22, 0.30, mat,
                               vis=(1,), tag="leaf_board"):
                out.append(s)
            nb = 4
            for k in range(nb):
                yy = bot + 0.25 + k * (top - bot - 0.55) / (nb - 1)
                out.append(box(l0 + sw, l1 - sw, yy, yy + 0.07, z1 - 0.01, z1 + 0.008, mat, vis=(1,), tag="leaf_batten"))
            if style == "oodo":
                # decorative kuguri wicket (D9): its own frame, battens and iron fittings; not a working door
                kx0 = l0 + 0.30
                kx1 = kx0 + 0.60
                ky0, ky1 = bot + 0.12, bot + 0.12 + 1.20
                for (a, b, c, d) in ((kx0, kx0 + 0.05, ky0, ky1), (kx1 - 0.05, kx1, ky0, ky1), (kx0, kx1, ky1 - 0.05, ky1),
                                     (kx0, kx1, ky0, ky0 + 0.05)):
                    out.append(box(a, b, c, d, z1 - 0.01, z1 + 0.018, mat, vis=(1,), tag="kuguri"))
                for yy in (ky0 + 0.30, ky1 - 0.35):
                    out.append(box(kx0 + 0.05, kx1 - 0.05, yy, yy + 0.06, z1 - 0.01, z1 + 0.015, mat, vis=(1,),
                                   tag="kuguri"))
                for (xx, yy) in ((kx0 + 0.02, ky0 + 0.25), (kx0 + 0.02, ky1 - 0.25), (kx1 - 0.08, ky0 + 0.6)):
                    out.append(box(xx, xx + 0.06, yy, yy + 0.10, z1 + 0.015, z1 + 0.025, "metal_iron", vis=(1,),
                                   tag="iron"))
            out.append(box(l1 - 0.20, l1 - 0.12, bot + 0.95, bot + 1.05, z1 + 0.008, z1 + 0.02, "metal_iron", vis=(1,),
                           tag="iron"))
        return out
    return build


def leaf_lattice(papered, mat):
    def build(l0, l1, bot, top, z0, z1, bone):
        out = [box(l0, l1, bot, top, z0, z1, mat, vis=(2, 3), geo=True, view=papered, fire=True, tag="leaf")]
        sw = 0.05
        out += [box(l0, l0 + sw, bot, top, z0, z1, mat, vis=(1,)), box(l1 - sw, l1, bot, top, z0, z1, mat, vis=(1,)),
                box(l0 + sw, l1 - sw, top - 0.05, top, z0, z1, mat, vis=(1,)),
                box(l0 + sw, l1 - sw, bot, bot + 0.30, z0 + 0.008, z1 - 0.008, mat, vis=(1,), tag="lower_board"),
                box(l0 + sw, l1 - sw, bot + 0.30, bot + 0.35, z0, z1, mat, vis=(1,))]
        n = int((l1 - l0 - 2 * sw) / 0.06)
        for k in range(n):
            x = l0 + sw + (k + 0.5) * (l1 - l0 - 2 * sw) / n
            out.append(box(x - 0.015, x + 0.015, bot + 0.35, top - 0.05, z0 + 0.004, z1 - 0.004, mat, vis=(1,), tag="bar"))
        for yy in (bot + 1.0, bot + 1.55):
            out.append(box(l0 + sw, l1 - sw, yy, yy + 0.025, z0 + 0.002, z0 + 0.012, mat, vis=(1,), tag="nuki"))
        if papered:
            out.append(box(l0 + sw, l1 - sw, bot + 0.35, top - 0.05, z0 - 0.001, z0 + 0.002, "paper_shoji", vis=(1, 2),
                           tag="paper"))
        return out
    return build


def leaf_shoji(low, mat="wood_weathered"):
    def build(l0, l1, bot, top, z0, z1, bone):
        out = [box(l0, l1, bot, top, z0, z1, {"front": "paper_shoji", "back": "paper_shoji", "default": mat},
                   vis=(2, 3), geo=True, view=True, fire="fabric_thin", uv="fit", tag="leaf")]
        sw = 0.035
        mid = (l0 + l1) / 2
        out += [box(l0, l0 + sw, bot, top, z0, z1, mat, vis=(1,)), box(l1 - sw, l1, bot, top, z0, z1, mat, vis=(1,)),
                box(mid - sw / 2, mid + sw / 2, bot, top, z0, z1, mat, vis=(1,), tag="centre_stile"),
                box(l0, l1, top - 0.04, top, z0, z1, mat, vis=(1,)),
                box(l0, l1, bot, bot + low, z0 + 0.004, z1 - 0.004, mat, vis=(1,), tag="lower_board"),
                box(l0, l1, bot + low, bot + low + 0.035, z0, z1, mat, vis=(1,))]
        zc = (z0 + z1) / 2
        out.append(box(l0 + sw, l1 - sw, bot + low + 0.035, top - 0.04, zc - 0.0015, zc + 0.0015, "paper_shoji", vis=(1,),
                       uv="world", tag="paper"))
        for (a, b) in ((l0 + sw, mid - sw / 2), (mid + sw / 2, l1 - sw)):
            for k in (1, 2, 3):
                x = a + (b - a) * k / 4
                out.append(box(x - 0.008, x + 0.008, bot + low + 0.035, top - 0.04, z0 + 0.003, z1 - 0.003, mat, vis=(1,),
                               tag="kumiko"))
        y = bot + low + 0.035 + 0.25
        while y < top - 0.1:
            out.append(box(l0 + sw, l1 - sw, y - 0.008, y + 0.008, z0 + 0.003, z1 - 0.003, mat, vis=(1,), tag="kumiko"))
            y += 0.25
        return out
    return build


def sliding_door_part(pid, variant, tiers, used, leaf_build, kind, side, thick, mat_track="wood_weathered",
                      bay=KEN, park=KEN, note=""):
    p = Part(pid, variant, "open", tiers=tiers, used_for=used,
             datum="1-ken door bay between post nodes x=0 and x=1.82 + its park bay to x=3.64; y 0 = sill/floor")
    zf = side * POST / 2
    sliding_leaf(p, A, bay - POST / 2, 0.0, DOOR_H, zf, side, +1, None, thick=thick, kind=kind, build=leaf_build,
                 park_span=(A - OV, bay + park - POST / 2), note=note)
    tracks(p, A, bay + park - POST / 2, zf, side, thick, mat_track)
    threshold(p, A, bay - POST / 2)
    door_conns(p, bay, park, +1, "exterior" if side > 0 else "interior")
    d = p.doors[0]
    p.dim("clear_opening_m", ">=1.00", (bay - POST / 2) - A, source="D1")
    p.dims[-1]["ok"] = (bay - POST) >= 1.0
    p.dim("head_m", DOOR_H, d.opening[3] - d.opening[2], source="D2")
    p.dim("leaf_slide_m (= leaf width)", round(d.width, 4), d.slide)
    return p


# ------------------------------------------------------------------------------------------------ itado
def part_itado(variant):
    rng = rng_for("itado" + variant)
    mat = "wood_weathered"
    if variant == "_pair":
        return _itado_pair(rng)
    style = {"_plain": "plain", "_battened": "battened", "_oodo": "oodo"}[variant]
    used = {"_plain": "plank sliding door of poor houses (T1), boards only; one 1.74 m leaf parks outside",
            "_battened": "framed and battened plank door, the everyday exterior door (T2)",
            "_oodo": "big entrance door with a decorative kuguri wicket (D9: the wicket does not open)"}[variant]
    p = sliding_door_part("jp_p_open_itado", variant, [1] if variant == "_plain" else [2, 3], used,
                          leaf_plank(style, mat, rng), "plank", +1, 0.04, note="exterior leaf, parks over the next bay")
    p.dims.append({"name": "leaf_thickness_m", "expected": 0.04, "measured": 0.04, "tol": 0.01, "source": "build_list"})
    return p


def _itado_pair(rng):
    """Two leaves, bi-parting, each parking over its own neighbour bay. Built on a 1.5-ken bay, not the build list's
    1-ken: a 1-ken pair gives 0.85 m per leaf, below D1 (logged as a deviation)."""
    bay = 1.5 * KEN
    p = Part("jp_p_open_itado", "_pair", "open", tiers=[2, 3],
             used_for="pair of plank leaves in a 1.5-ken bay, each opening >= 1.00 m (D1; build list said 1 ken)",
             deviation="bay 1.5 ken instead of the build list's 1 ken: a 1-ken pair opens 0.85 m per leaf (< D1)",
             datum="1.5-ken bay x 0..2.73; left leaf parks over x -1.82..0, right leaf over 2.73..4.55")
    mid = bay / 2
    zf = POST / 2
    mat = "wood_weathered"
    sliding_leaf(p, A, mid, 0.0, DOOR_H, zf, +1, -1, None, thick=0.04, kind="plank",
                 build=leaf_plank("battened", mat, rng), park_span=(-KEN + A, mid + OV), note="left leaf")
    sliding_leaf(p, mid, bay - POST / 2, 0.0, DOOR_H, zf + 0.05, +1, +1, None, thick=0.04, kind="plank",
                 build=leaf_plank("battened", mat, rng), park_span=(mid - OV, bay + KEN - POST / 2), note="right leaf")
    tracks(p, -KEN + A, bay + KEN - POST / 2, zf, +1, 0.09)
    threshold(p, A, bay - POST / 2)
    for x in (0.0, bay):
        p.conn("post", (x, 0, 0))
    p.conn("post", (-KEN, 0, 0), note="far end of the left park bay")
    p.conn("post", (bay + KEN, 0, 0), note="far end of the right park bay")
    p.conn("park", (-KEN, 0, 0), length=KEN, face="exterior")
    p.conn("park", (bay, 0, 0), length=KEN, face="exterior")
    p.conn("sill", (0, 0, 0))
    p.conn("head", (0, DOOR_H, 0))
    for d in p.doors:
        o = d.opening
        p.dim("clear_per_leaf_m (%s)" % d.note, ">=1.00", o[1] - o[0], source="D1")
        p.dims[-1]["ok"] = o[1] - o[0] >= 1.0
    return p


def part_koshido(variant):
    pap = variant == "_papered"
    p = sliding_door_part("jp_p_open_koshido", variant, [2, 3],
                          "lattice day door behind the itado, paper behind the bars" if pap
                          else "open-bar lattice day door behind the itado (T2-3 entrances)",
                          leaf_lattice(pap, "wood_street_dark"), "lattice", -1, 0.035,
                          note="interior leaf, parks inside over the next bay")
    p.doors[0].sound = "doorWoodSlide"
    return p


def part_shoji_ext(variant):
    low = 0.60 if variant == "_koshidaka" else 0.15
    p = sliding_door_part("jp_p_open_shoji_ext", variant, [1] if variant == "_koshidaka" else [2, 3],
                          "board-bottomed paper door of nagaya and doma entrances (T1)" if variant == "_koshidaka"
                          else "plain shoji line behind the amado of a veranda (T2)",
                          leaf_shoji(low), "shoji", -1, 0.03, note="paper door, interior track")
    p.doors[0].kind = "shoji"
    p.doors[0].anim_period = 0.8
    p.doors[0].init_opened = 0.5
    p.dim("lower_board_m", low, low)
    return p


# ------------------------------------------------------------------------------------------------ amado + tobukuro
def amado_leaves(part, x0, x1, y0=0.0, z=0.0, mat="wood_weathered", geo=True):
    n = max(1, round((x1 - x0) / HALF))
    w = (x1 - x0) / n
    rng = rng_for(part.name + "amado")
    for k in range(n):
        a, b = x0 + k * w, x0 + (k + 1) * w
        part.add(box(a, b + 0.01, y0 + 0.005, y0 + DOOR_H + 0.03, z - 0.015, z + 0.015, mat, vis=(2, 3), geo=geo,
                     view=geo, fire=True if geo else None, tag="amado"))
        part.extend(board_run(a + 0.03, b - 0.03, y0 + 0.04, y0 + DOOR_H - 0.01, z - 0.009, z + 0.0, rng, 0.14, 0.22, mat,
                              vis=(1,), tag="amado_board"))
        for (c, d, e, f) in ((a, a + 0.03, y0, y0 + DOOR_H + 0.03), (b - 0.03, b, y0, y0 + DOOR_H + 0.03),
                             (a, b, y0, y0 + 0.04), (a, b, y0 + DOOR_H - 0.01, y0 + DOOR_H + 0.03)):
            part.add(box(c, d, e, f, z - 0.015, z + 0.015, mat, vis=(1,), tag="amado_frame"))
        for yy in (0.55, 1.05, 1.55):
            part.add(box(a + 0.03, b - 0.03, y0 + yy, y0 + yy + 0.025, z + 0.0, z + 0.012, mat, vis=(1,), tag="amado_bar"))


def part_amado(variant):
    closed = variant == "_closed"
    p = Part("jp_p_open_amado", variant, "open", tiers=[2, 3],
             used_for="storm shutters closed in a line (abandoned houses; blocks the opening)" if closed
             else "amado track and transom with the leaves stowed in the tobukuro (default, open)",
             datum="2-ken run along the veranda's outer groove line (z 0); y 0 = veranda floor",
             note="static, not doors: a run of 6-10 leaves would be 6-10 door bones (build list)")
    L = 2 * KEN
    if closed:
        amado_leaves(p, A, L - A)
    p.add(box(A - 0.06, L - A + 0.06, DOOR_H + 0.03, DOOR_H + 0.13, -0.05, 0.05, "wood_weathered", vis=(1, 2, 3),
              tag="head_rail"))
    p.add(box(A - 0.06, L - A + 0.06, DOOR_H + 0.13, DOOR_H + 0.40, -0.012, 0.0, "wood_weathered", vis=(1, 2),
              tag="transom_board"))
    p.add(box(A - 0.06, L - A + 0.06, DOOR_H + 0.40, DOOR_H + 0.45, -0.04, 0.03, "wood_weathered", vis=(1, 2),
              tag="transom_rail"))
    for x in (0.0, KEN, L):
        p.conn("post", (x, 0, 0), note="veranda outer posts")
    p.conn("sill", (0, 0, 0), note="outer groove of jp_p_porch_engawa")
    p.conn("head", (0, DOOR_H, 0))
    p.dim("leaf_m", "0.91 x 2.00", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % ((L - 2 * A) / 4, DOOR_H), ok=True)
    return p


def part_tobukuro(variant):
    p = Part("jp_p_open_tobukuro", variant, "open", tiers=[2, 3],
             used_for="board box holding the stowed amado at the end of a run" if variant == "_box"
             else "Morse's swinging shutter closet, shown swung clear of the veranda (P3)",
             datum="beside the end post of the amado run: x from the post face, z 0 = groove line, y 0 = veranda floor")
    iw, n = 0.91 + 0.05, 8
    dp = n * 0.03 + 0.05
    h = DOOR_H + 0.10 + 0.03
    x0, x1 = A, A + iw + 0.04
    z0, z1 = -dp / 2, dp / 2
    rng = rng_for("tobukuro" + variant)
    sol = []
    sol.append(box(x0, x1, 0.0, h, z0, z1, "wood_weathered", vis=(2, 3), geo=True, view=True, fire=True, tag="box"))
    sol += board_run(x0, x1, 0.0, h, z1 - 0.015, z1, rng, 0.18, 0.28, "wood_weathered", vis=(1,), tag="box_board")
    sol.append(box(x0, x1, 0.0, h, z0, z0 + 0.015, "wood_weathered", vis=(1,)))
    sol.append(box(x1 - 0.02, x1, 0.0, h, z0, z1, "wood_weathered", vis=(1,)))
    sol.append(box(x0 - 0.02, x1 + 0.03, h, h + 0.05, z0 - 0.03, z1 + 0.04, "wood_weathered", vis=(1, 2), tag="lid"))
    for yy in (0.4, 1.1, 1.8):
        sol.append(box(x0, x1, yy, yy + 0.06, z1, z1 + 0.018, "wood_weathered", vis=(1,), tag="batten"))
    if variant == "_swing":
        sol = [s.transformed(-90.0, (0, 0, 0)) for s in [s.finalize() for s in sol]]
        sol = [s.transformed(0.0, (A + dp / 2, 0.0, 0.05)) for s in sol]
        for s in sol:
            p.solids.append(s)
        p.add(box(A - 0.01, A + 0.02, 0.3, 0.45, 0.0, 0.05, "metal_iron", vis=(1,), tag="pivot"))
        p.add(box(A - 0.01, A + 0.02, 1.8, 1.95, 0.0, 0.05, "metal_iron", vis=(1,), tag="pivot"))
    else:
        p.extend(sol)
    p.conn("post", (0, 0, 0), note="outside the end post of the amado run")
    p.dim("inner_width_m", 0.96, iw)
    p.dim("depth_m (8 leaves)", round(dp, 3), dp)
    p.dim("height_m", 2.13, h, source="leaf + 0.10")
    return p


# ------------------------------------------------------------------------------------------------ kura door
def kura_surround(part, cx, clear_w, clear_h, face_z, steps=4, step=0.035, proj=0.16, border=0.30, mat="wall_shikkui"):
    """Stepped plaster door/window surround projecting from an okabe face; hole = clear at the wall, widening outward."""
    ow = clear_w + 2 * border
    oh_top = clear_h + border
    for k in range(steps):
        za, zb = face_z + k * proj / steps, face_z + (k + 1) * proj / steps
        hw = clear_w / 2 + k * step
        ht = clear_h + k * step
        for (a, b, c, d) in ((cx - ow / 2, cx - hw, 0.0, oh_top), (cx + hw, cx + ow / 2, 0.0, oh_top),
                             (cx - hw, cx + hw, ht, oh_top)):
            part.add(box(a, b, c, d, za, zb, mat, vis=(1, 2, 3) if k == 0 else (1, 2), geo=True, view=True, fire=True,
                         tag="surround"))
    return ow, oh_top, face_z + proj


def mini_pent(part, x0, x1, y_wall, z_wall, depth=0.60, t=0.40, brackets=True):
    """Small tiled pent (kura door / window): sheathing slab + a kawara course set + eave tiles."""
    y_edge = y_wall - depth * t
    part.add(prism([(y_wall, z_wall), (y_edge, z_wall + depth), (y_edge + 0.06, z_wall + depth), (y_wall + 0.06, z_wall)],
                   "x", x0, x1, {"default": "wood_weathered"}, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="pent"))
    F = kawara.SlopeFrame((x0, y_edge + 0.06 + 0.012, z_wall + depth), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), t)
    rl = depth / F.cos
    kawara.eave_tiles(part, F, 0.0, x1 - x0, style="plain")
    kawara.field(part, F, 0.0, x1 - x0, kawara.EXPO, rl, rows_eave=1, rows_ridge=0)
    if brackets:
        for x in (x0 + 0.12, x1 - 0.12):
            part.add(box(x - 0.04, x + 0.04, y_edge - 0.16, y_edge + 0.02, z_wall, z_wall + depth - 0.08, "wood_weathered",
                         vis=(1, 2), tag="bracket"))


def part_kura_door(variant):
    hinged = variant == "_hinged"
    p = Part("jp_p_open_kura_door", variant, "open", tiers=[2, 3],
             used_for=("kura doorway with the thick plastered leaves as rotation doors (engine test, P2)" if hinged
                       else "kura doorway: stepped plaster surround, outer leaves static open, inner sliding door"),
             datum="1-ken bay of a 0.24 okabe wall (faces z +-0.12), centred at x 0.91; y 0 = approach level")
    th = 0.15                                  # raised stone threshold (hidden ramps both sides)
    cx, cw, ch = HALF, 1.10, DOOR_H + th       # 2.00 clear above the threshold
    fz = 0.12
    ow, oh, zf_out = kura_surround(p, cx, cw, ch, fz)
    p.add(box(cx - cw / 2 - 0.06, cx + cw / 2 + 0.06, -0.10, th, -0.12, zf_out, "stone_cut", vis=(1, 2, 3), geo=True,
              view=False, fire=True, tag="threshold"))
    p.road([(cx - cw / 2, th, -0.12), (cx + cw / 2, th, -0.12), (cx + cw / 2, th, zf_out), (cx - cw / 2, th, zf_out)],
           "stone_ext")
    for (za, zb) in ((zf_out, zf_out + 0.26), (-0.12, -0.38)):
        poly = [(za, th), (zb, 0.0), (za, 0.0)]
        if (zb - za) * 1 < 0:
            poly = [(za, th), (za, 0.0), (zb, 0.0)]
        s = prism([(y, z) for z, y in poly], "x", cx - cw / 2, cx + cw / 2, "stone_cut", vis=(), geo=True, tag="ramp")
        p.add(s)
        p.road([(cx - cw / 2, th, za), (cx + cw / 2, th, za), (cx + cw / 2, 0.0, zb), (cx - cw / 2, 0.0, zb)], "stone_ext")
    # inner sliding door (the game door), on the interior face, parks over the next bay inside
    rng = rng_for("kura_inner")

    def inner(l0, l1, bot, top, z0, z1, bone):
        out = [box(l0, l1, bot, top, z0, z1, "wood_weathered", vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
        out += board_run(l0, l1, bot, bot + 1.0, z0, z1, rng, 0.2, 0.28, "wood_weathered", vis=(1,), tag="leaf_board")
        out.append(box(l0, l1, bot + 1.0, top, z0, z0 + 0.012, "wood_weathered", vis=(1,), tag="leaf_back"))
        for k in range(12):
            x = l0 + 0.05 + k * (l1 - l0 - 0.1) / 11
            out.append(box(x - 0.018, x + 0.018, bot + 1.0, top, z0 + 0.012, z1, "wood_weathered", vis=(1,), tag="bar"))
        for (a, b) in ((l0, l0 + 0.05), (l1 - 0.05, l1)):
            out.append(box(a, b, bot, top, z0, z1 + 0.004, "wood_weathered", vis=(1,), tag="stile"))
        out.append(box(l0, l1, top - 0.05, top, z0, z1 + 0.004, "wood_weathered", vis=(1,)))
        out.append(box(l1 - 0.25, l1 - 0.15, bot + 0.95, bot + 1.10, z0 - 0.012, z0, "metal_iron", vis=(1,), tag="iron"))
        return out
    sliding_leaf(p, cx - cw / 2, cx + cw / 2, th, DOOR_H, -0.12, -1, +1, None, thick=0.04, kind="plank",
                 build=inner, park_span=(cx - cw / 2 - OV, KEN + KEN), note="inner sliding door (game door)")
    tracks(p, cx - cw / 2, cx + cw / 2 + cw + 0.2, -0.12, -1, 0.04, head_y=th + DOOR_H)
    # outer leaves: 0.16 thick plastered, stepped edge
    lw = ow / 2 - 0.30 + 0.07 + 4 * 0.035
    lh = ch + 0.14 + 0.04 - th
    hinges = [(cx - cw / 2 - 4 * 0.035 - 0.03, -1), (cx + cw / 2 + 4 * 0.035 + 0.03, +1)]
    for hx, sg in hinges:
        def leaf_solids(closed):
            out = []
            if closed:
                x0, x1 = (hx, hx - sg * lw) if sg < 0 else (hx - lw, hx)
                x0, x1 = min(hx, hx - sg * lw), max(hx, hx - sg * lw)
                out.append(box(x0, x1, 0.0 + th, th + lh, zf_out, zf_out + 0.16, "wall_shikkui", vis=(1, 2, 3),
                               geo=True, view=True, fire=True, tag="kura_leaf"))
                out.append(box(x0 + 0.04, x1 - 0.04, th + 0.04, th + lh - 0.04, zf_out + 0.16, zf_out + 0.19,
                               "wall_shikkui", vis=(1,), tag="kura_leaf_step"))
            else:
                # static open ~100 degrees: the leaf stands out from the surround edge
                z0 = zf_out
                xa = hx + sg * 0.0
                out.append(box(min(xa, xa + sg * 0.16), max(xa, xa + sg * 0.16), th, th + lh, z0, z0 + lw, "wall_shikkui",
                               vis=(1, 2, 3), geo=True, view=True, fire=True, tag="kura_leaf"))
                out.append(box(min(xa + sg * 0.16, xa + sg * 0.19), max(xa + sg * 0.16, xa + sg * 0.19), th + 0.04,
                               th + lh - 0.04, z0 + 0.04, z0 + lw - 0.04, "wall_shikkui", vis=(1,), tag="kura_leaf_step"))
            return out
        if hinged:
            bone = p.next_bone()
            for s in leaf_solids(True):
                s.door = bone
                p.add(s)
            axis = [(hx, th, zf_out), (hx, th + lh, zf_out)] if sg < 0 else [(hx, th + lh, zf_out), (hx, th, zf_out)]
            ang = math.radians(100)
            centre = (hx - sg * lw / 2, th + lh / 2, zf_out + 0.08)
            p.memory[bone + "_axis"] = axis
            p.memory[bone + "_action"] = [(cx, 1.0 + th, zf_out)]
            p.memory[bone] = [centre]
            p.doors.append(Door(kind="kura", anims=[{"bone": bone, "type": "rotation", "axis": axis, "amount": ang}],
                                action=(cx, 1.0 + th, zf_out), centre=centre, anim_period=2.0, init_opened=1.0,
                                sound="doorWoodSlide", display="kura door", note="outer plaster leaf (rotation)",
                                engine_tested=False, passable=False, has_view=True))
        else:
            p.extend(leaf_solids(False))
        for yy in (th + 0.35, th + lh - 0.45):
            p.add(box(hx - 0.05, hx + 0.05, yy, yy + 0.12, zf_out - 0.01, zf_out + 0.02, "metal_iron", vis=(1,),
                      tag="hinge"))
    mini_pent(p, cx - ow / 2 - 0.05, cx + ow / 2 + 0.05, oh + 0.45, zf_out)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), hidden=True, note="okabe: posts hidden in the wall")
    p.conn("sill", (0, 0, 0), note="raised stone threshold 0.15 with hidden ramps")
    p.conn("park", (KEN, 0, 0), length=KEN, face="interior")
    p.dim("clear_m", ">=1.00 x 2.00", 0.0, source="build_list / D1")
    p.dims[-1].update(measured="%.2f x %.2f" % (cw, ch - th), ok=cw >= 1.0 and ch - th >= 2.0 - 1e-6)
    p.dim("leaf_thickness_m", "0.15-0.20", 0.16)
    p.dim("jamb_steps", "3-5", 4, tol=0)
    p.dim("door_pent_m", 0.60, 0.60)
    p.notes.append("Opening 1.10 x 2.15 from the approach level = 2.00 clear above the 0.15 threshold; the okabe wall "
                   "recipe must leave that hole (walls.wall_run(kind='okabe', openings=[(0.36, 1.46, 0, 2.15)])).")
    return p


def part_kura_window(variant):
    p = Part("jp_p_open_kura_window", variant, "open", tiers=[2, 3],
             used_for="kura window with iron bars, sliding plaster shutter and a tiny tile pent" if variant == "_slide"
             else "kura window with a pair of hinged plaster shutters (static open)",
             datum="half-ken bay of a 0.24 okabe wall, opening centred at x 0.455, sill at 1.20; y 0 = kura floor")
    cx, w, h, sill = QK_, 0.60, 0.75, 1.20
    fz = 0.12
    # surround (2 steps) sits around the 0.60 x 0.75 hole
    for k in range(2):
        za, zb = fz + k * 0.05, fz + (k + 1) * 0.05
        hw, hh = w / 2 + k * 0.03, h / 2 + k * 0.03
        cy = sill + h / 2
        for (a, b, c, d) in ((cx - w / 2 - 0.20, cx - hw, sill - 0.20, sill + h + 0.20),
                             (cx + hw, cx + w / 2 + 0.20, sill - 0.20, sill + h + 0.20),
                             (cx - hw, cx + hw, cy + hh, sill + h + 0.20), (cx - hw, cx + hw, sill - 0.20, cy - hh)):
            p.add(box(a, b, c, d, za, zb, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="surround"))
    for k in range(6):
        x = cx - w / 2 + (k + 0.5) * w / 6
        p.add(box(x - 0.015, x + 0.015, sill, sill + h, -0.015, 0.015, "metal_iron", vis=(1, 2), tag="bar"))
    p.add(box(cx - w / 2, cx + w / 2, sill, sill + h, -0.015, 0.015, "metal_iron", vis=(), geo=True, tag="bars_geo"))
    zo = fz + 0.10
    if variant == "_slide":
        p.add(box(cx - w / 2 + 0.30, cx + w / 2 + 0.36, sill - 0.04, sill + h + 0.04, zo, zo + 0.12, "wall_shikkui",
                  vis=(1, 2, 3), geo=True, view=True, fire=True, tag="shutter"))
        p.add(box(cx - w / 2 - 0.05, cx + w + 0.45, sill + h + 0.04, sill + h + 0.10, zo, zo + 0.13, "wall_shikkui",
                  vis=(1, 2), tag="shutter_track"))
        p.add(box(cx - w / 2 - 0.05, cx + w + 0.45, sill - 0.10, sill - 0.04, zo, zo + 0.13, "wall_shikkui",
                  vis=(1, 2), tag="shutter_track"))
    else:
        for sg in (-1, 1):
            hx = cx + sg * (w / 2 + 0.06)
            p.add(box(min(hx, hx + sg * 0.12), max(hx, hx + sg * 0.12), sill - 0.03, sill + h + 0.03, zo, zo + w / 2 + 0.06,
                      "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="shutter"))
    mini_pent(p, cx - w / 2 - 0.30, cx + w / 2 + 0.30, sill + h + 0.42, fz + 0.10, depth=0.35, brackets=False)
    p.conn("post", (0, 0, 0), hidden=True)
    p.conn("post", (HALF, 0, 0), hidden=True)
    p.dim("opening_m", "0.60 x 0.75", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (w, h), ok=True)
    p.dim("bars_m", "0.03 at 0.09", 0.0)
    p.dims[-1].update(measured="0.03 at %.3f" % (w / 6), ok=abs(w / 6 - 0.09) < 0.02)
    p.dim("shutter_thickness_m", 0.12, 0.12)
    return p


QK_ = HALF / 2


# ------------------------------------------------------------------------------------------------ mushiko
def stadium_panel(part, x0, x1, y0, y1, t, holes, mat="wall_shikkui", slat=0.045, gap=0.045):
    """Plaster panel with stadium (round-ended) holes [(cx, cy, w, h)], slatted with plastered vertical slats.
    Each plaster piece is a convex prism; one geometry box for the whole panel."""
    z0, z1 = -t / 2, t / 2
    part.add(box(x0, x1, y0, y1, z0, z1, mat, vis=(), geo=True, view=False, fire=True, tag="panel_geo"))
    xs = [x0]
    for (cx, cy, w, h) in sorted(holes):
        xs += [cx - w / 2, cx + w / 2]
    xs.append(x1)
    # vertical strips between holes (full height)
    for i in range(0, len(xs), 2):
        if xs[i + 1] - xs[i] > 1e-4:
            part.add(box(xs[i], xs[i + 1], y0, y1, z0, z1, mat, vis=(1, 2, 3), view=True, tag="panel"))
    for (cx, cy, w, h) in holes:
        r = h / 2
        a, b = cx - w / 2, cx + w / 2
        part.add(box(a, b, y0, cy - r, z0, z1, mat, vis=(1, 2, 3), view=True, tag="panel"))
        part.add(box(a, b, cy + r, y1, z0, z1, mat, vis=(1, 2, 3), view=True, tag="panel"))
        n = 6
        for side in (-1, 1):
            xe = a if side < 0 else b
            xc = a + r if side < 0 else b - r
            for q in (-1, 1):                      # lower / upper quarter
                for k in range(n):
                    th0 = math.pi / 2 * k / n
                    th1 = math.pi / 2 * (k + 1) / n
                    p0 = (xc + side * r * math.cos(th0), cy + q * r * math.sin(th0))
                    p1 = (xc + side * r * math.cos(th1), cy + q * r * math.sin(th1))
                    poly = [(xe, p0[1]), p0, p1, (xe, p1[1])]
                    area = sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))
                    if abs(area) < 1e-7:
                        continue
                    if area < 0:
                        poly = poly[::-1]
                    from .shapes import clean_poly
                    poly = clean_poly(poly)
                    if len(poly) >= 3:
                        part.add(prism(poly, "z", z0, z1, mat, vis=(1, 2), tag="panel_arc"))
        # slats (plastered) across the hole
        x = a + gap / 2
        while x + slat < b - 0.01:
            xm = x + slat / 2
            dx = max(0.0, max(a + r - xm, xm - (b - r)))
            hh = math.sqrt(max(0.0, r * r - dx * dx)) if dx > 0 else r
            if hh > 0.03:
                part.add(box(x, x + slat, cy - hh, cy + hh, -0.03, 0.03, mat, vis=(1, 2), tag="slat"))
            x += slat + gap
        part.add(box(a + r * 0.3, b - r * 0.3, cy - r * 0.9, cy + r * 0.9, -0.03, 0.03, "wood_sooted", vis=(3,),
                     tag="hole_lod"))


def part_mushiko(variant):
    pair = variant == "_oval_pair"
    p = Part("jp_p_open_mushiko", variant, "open", tiers=[3],
             used_for=("two small oval mushiko in one 1-ken bay of the low upper street wall (1730 form)" if pair
                       else "single small oval mushiko on the low upper street wall of Kamigata machiya (1730 form)"),
             deviation="oval pair: each oval 0.70 x 0.40 so two fit one 1-ken bay (build list single oval 0.90 x 0.45)"
             if pair else None,
             datum="1-ken bay of the upper plastered front (0.15 thick, hidden posts); y 0 = upper floor, wall to 1.30")
    H = 1.30
    if pair:
        holes = [(HALF / 2 + 0.02, 0.40 + 0.20, 0.70, 0.40), (HALF + HALF / 2 - 0.02, 0.40 + 0.20, 0.70, 0.40)]
    else:
        holes = [(HALF, 0.40 + 0.225, 0.90, 0.45)]
    stadium_panel(p, 0.0, KEN, 0.0, H, 0.15, holes)
    p.conn("post", (0, 0, 0), hidden=True)
    p.conn("post", (KEN, 0, 0), hidden=True)
    p.conn("floor", (0, 0, 0), note="upper floor level; street wall above it <= 1.30 (D3)")
    w, h = holes[0][2], holes[0][3]
    p.dim("opening_m", "0.90 x 0.45" if not pair else "0.70 x 0.40 (pair)", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (w, h), ok=True)
    p.dim("slat_face_m", 0.045, 0.045)
    p.dim("depth_m", 0.15, 0.15)
    p.dim("sill_above_upper_floor_m", 0.40, holes[0][1] - h / 2)
    return p


# ------------------------------------------------------------------------------------------------ koshi lattice
def koshi(part, x0, x1, variant, y0=0.45, y1=DOOR_H, z=0.0):
    mat = "wood_bengara" if variant == "_bengara" else "wood_street_dark"
    zb = z + 0.05                      # bars stand proud of the frame line on the street side
    part.add(box(x0, x1, y0 - 0.06, y0, z - 0.03, zb + 0.03, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                 tag="koshi_sill"))
    part.add(box(x0, x1, y1 - 0.06, y1, z - 0.03, zb + 0.02, mat, vis=(1, 2, 3), tag="koshi_head"))
    part.add(box(x0, x1, y0, y1 - 0.06, z - 0.03, zb, mat, vis=(), geo=True, view=True, fire=True, tag="koshi_geo"))
    # paper of the static shoji behind
    part.add(box(x0, x1, y0, y1 - 0.06, z - 0.03, z - 0.027, "paper_shoji", vis=(1, 2, 3), tag="koshi_paper"))
    part.add(box(x0, x1, y0, y1 - 0.06, z - 0.027, zb, mat, vis=(3,), tag="koshi_lod", uv="fit"))
    if variant == "_komeya":
        face, cc = 0.06, 0.12
    else:
        face, cc = 0.03, 0.06
    n = max(2, int(round((x1 - x0) / cc)))
    ytop = y1 - 0.06
    for k in range(n):
        x = x0 + (k + 0.5) * (x1 - x0) / n
        top = ytop
        if variant == "_oyako" and k % 4:
            top = ytop - 0.30
        vis = (1, 2) if k % 2 == 0 else (1,)
        part.add(box(x - face / 2, x + face / 2, y0, top, z, zb, mat, vis=vis, tag="koshi_bar"))
    rails = [y0 + (ytop - y0) * f for f in ((0.35, 0.7) if variant != "_komeya" else (0.5,))]
    if variant == "_oyako":
        rails = [ytop - 0.30]
    for yy in rails:
        part.add(box(x0, x1, yy - 0.012, yy + 0.012, z - 0.012, z, mat, vis=(1,), tag="koshi_rail"))


def part_koshi(variant):
    used = {"_kyo": "fine-bar Kyoto lattice front / window", "_oyako": "parent bars + cut-top children (cloth, thread)",
            "_komeya": "thick bars for rice and charcoal shops (T2)", "_degoshi": "projecting lattice on its own sill (T3)",
            "_bengara": "bengara-red fine lattice (Kamigata, sparingly; restricted colour)"}[variant]
    p = Part("jp_p_open_koshi", variant, "open", tiers=[2] if variant == "_komeya" else [3], used_for=used,
             recipe="openings.koshi(part, x0, x1, variant) for 0.5 / 1 / 1.5 / 2-ken modules",
             datum="1-ken module between post faces; y 0 = sill level of the wall (lattice sill 0.45, head 2.00)")
    if variant == "_degoshi":
        pz = 0.30
        koshi(p, A + 0.02, B - 0.02, "_kyo", z=pz)
        for x in (A, B):
            p.add(box(x - 0.02 if x == A else x - 0.04, x + 0.04 if x == A else x + 0.02, 0.45 - 0.06, DOOR_H - 0.06,
                      0.0, pz + 0.08, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="degoshi_side"))
            n = 5
            for k in range(n):
                zz = 0.03 + k * (pz - 0.02) / n
                p.add(box(x - 0.01, x + 0.01, 0.45, DOOR_H - 0.12, zz, zz + 0.03, "wood_street_dark", vis=(1,),
                          tag="side_bar"))
        p.add(box(A - 0.04, B + 0.04, DOOR_H - 0.06, DOOR_H - 0.02, -0.02, pz + 0.12, "wood_street_dark", vis=(1, 2, 3),
                  tag="degoshi_top"))
        p.add(box(A - 0.04, B + 0.04, 0.33, 0.39, 0.0, pz + 0.12, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag="degoshi_sill"))
        p.dim("degoshi_projection_m", 0.30, pz)
    else:
        koshi(p, A, B, variant)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0.45, 0), note="own sill rail on the koshi-ita / plinth")
    p.conn("head", (0, DOOR_H, 0))
    p.dim("bar_face_m", 0.06 if variant == "_komeya" else 0.03, 0.06 if variant == "_komeya" else 0.03)
    p.dim("module_width_ken", "0.5 / 1 / 1.5 / 2", 1.0)
    return p


# ------------------------------------------------------------------------------------------------ renji
def part_renji(variant):
    p = Part("jp_p_open_renji", variant, "open", tiers={"_bamboo": [1], "_wood": [2], "_muso": [2]}[variant],
             used_for={"_bamboo": "bamboo-barred window with a sliding board shutter (farmhouses, T1)",
                       "_wood": "square wood-barred window with a sliding board shutter (T2)",
                       "_muso": "double slatted kitchen window, one panel slides (date unverified)"}[variant],
             datum="half-ken bay between post nodes x 0 and 0.91; sill 0.90, opening 0.75 high; y 0 = floor")
    a, b = A, HALF - POST / 2
    s0, s1 = 0.90, 1.65
    fm = "wood_weathered"
    p.add(box(a, b, s0 - 0.05, s0, -0.07, 0.07, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="sill"))
    p.add(box(a, b, s1, s1 + 0.05, -0.06, 0.06, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head"))
    p.add(box(a, b, s0, s1, -0.01, 0.01, fm, vis=(), geo=True, tag="bars_geo"))
    if variant == "_muso":
        for zz, off in ((0.01, 0.0), (-0.02, 0.045)):
            x = a + off
            while x + 0.045 <= b + 1e-6:
                p.add(box(x, x + 0.045, s0, s1, zz, zz + 0.018, fm, vis=(1, 2), tag="slat"))
                x += 0.09
    else:
        n = int((b - a) / 0.08)
        for k in range(n):
            x = a + (k + 0.5) * (b - a) / n
            if variant == "_bamboo":
                p.add(tube((x, s0, 0.0), (x, s1, 0.0), 0.014, "bamboo_weathered", n=6, vis=(1, 2), tag="bar"))
            else:
                p.add(box(x - 0.015, x + 0.015, s0, s1, -0.015, 0.015, fm, vis=(1, 2), tag="bar"))
        # board shutter inside, half open (static), sliding inside the wall line
        p.add(box((a + b) / 2, b + 0.35, s0 - 0.02, s1 + 0.02, -0.075, -0.06, fm, vis=(1, 2), tag="shutter"))
        p.add(box(a - 0.02, b + 0.40, s1 + 0.02, s1 + 0.06, -0.09, -0.055, fm, vis=(1,), tag="shutter_track"))
    for x in (0.0, HALF):
        p.conn("post", (x, 0, 0))
    p.dim("opening_m", "0.91 bay x 0.60-0.90", 0.0)
    p.dims[-1].update(measured="%.2f bay (%.2f clear) x %.2f" % (HALF, b - a, s1 - s0), ok=True)
    p.dim("sill_m", 0.9, s0)
    return p


# ------------------------------------------------------------------------------------------------ suriagedo
def part_suriagedo(variant):
    p = Part("jp_p_open_suriagedo", variant, "open", tiers=[2, 3],
             used_for={"_closed": "shop front closed at night by 3 stacked boards in the post grooves (static)",
                       "_part": "shop front with one board left in the grooves (static)",
                       "_door": "animated: the 3 boards rise into the box behind the beam (one door, 3 bones; "
                                "engine test)"}[variant],
             datum="1-ken bay between post nodes; boards in grooves in the wall plane; box above 2.00 inside")
    bh = DOOR_H / 3
    fm = "wood_street_dark"
    rng = rng_for("suriage" + variant)
    zs = [0.03, 0.0, -0.03] if variant == "_door" else [0.0, 0.0, 0.0]
    boards = []
    for k in range(3):                         # k = 0 bottom .. 2 top
        y0, y1 = k * bh + 0.004, (k + 1) * bh
        boards.append((y0, y1, zs[k]))
    # storage box above the head, hollow (front and back boards + top) so the boards can rise into it
    p.add(box(A, B, DOOR_H, WALL_H, 0.045, 0.06, "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="box"))
    p.add(box(A, B, DOOR_H, WALL_H, -0.06, -0.045, "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="box"))
    p.add(box(A, B, WALL_H - 0.02, WALL_H, -0.045, 0.045, "wood_weathered", vis=(1, 2), geo=True, view=True, fire=True,
              tag="box"))
    for x in (A + 0.3, B - 0.3):
        p.add(box(x - 0.03, x + 0.03, DOOR_H + 0.1, WALL_H - 0.1, 0.06, 0.075, "wood_weathered", vis=(1,), tag="batten"))
    threshold(p, A, B)

    def board_solids(y0, y1, z, bone=None):
        t = 0.024
        # collision stops at the post faces; the visual board runs 12 mm into the post grooves
        out = [box(A + 0.002, B - 0.002, y0, y1, z - t / 2, z + t / 2, fm, vis=(), geo=True, view=True, fire=True,
                   tag="suriage_board_geo"),
               box(A - 0.012, B + 0.012, y0, y1, z - t / 2, z + t / 2, fm, vis=(2, 3), tag="suriage_board")]
        out += board_run(A - 0.012, B + 0.012, y0, y1, z - t / 2 + 0.004, z + t / 2, rng, 0.25, 0.4, fm, vertical=False,
                         vis=(1,), tag="suriage_plank")
        out.append(box(A + 0.1, B - 0.1, y1 - 0.08, y1 - 0.03, z + t / 2, z + t / 2 + 0.012, fm, vis=(1,), tag="cleat"))
        out.append(box((A + B) / 2 - 0.08, (A + B) / 2 + 0.08, y0 + 0.25, y0 + 0.33, z + t / 2, z + t / 2 + 0.02,
                       "metal_iron", vis=(1,), tag="grip"))
        for s in out:
            s.door = bone
        return out
    if variant == "_closed":
        for (y0, y1, z) in boards:
            p.extend(board_solids(y0, y1, z))
    elif variant == "_part":
        p.extend(board_solids(*boards[0]))
    else:
        anims = []
        for k, (y0, y1, z) in enumerate(boards):
            bone = "doors%d" % (k + 1)
            p.extend(board_solids(y0, y1, z, bone))
            amt = DOOR_H - y0 + 0.004
            c = ((A + B) / 2, (y0 + y1) / 2, z)
            axis = [c, (c[0], c[1] + 1.0, c[2])]
            p.memory[bone + "_axis"] = axis
            p.memory[bone] = [c]
            anims.append({"bone": bone, "type": "translation", "axis": axis, "amount": amt})
        act = ((A + B) / 2, 1.0, 0.0)
        p.memory["doors1_action"] = [act]
        d = Door(kind="plank", anims=anims, action=act, centre=((A + B) / 2, 1.0, 0.0), anim_period=1.6, init_opened=1.0,
                 display="shop shutters", note="3 boards on one source; vertical translation (engine test)",
                 engine_tested=False, opening=(A, B, 0.0, DOOR_H), z_face=0.0, passable=True)
        p.doors.append(d)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), note="grooved post (0.03 grooves)")
    p.conn("head", (0, DOOR_H, 0), note="stack top under the 2.00 beam; box above it")
    p.dim("boards", 3, 3, tol=0)
    p.dim("board_height_m", 0.68, bh, tol=0.02, source="build_list ~0.68 (2.04/3); here 2.00/3")
    return p


def part_shitomido(variant):
    up = variant == "_up"
    p = Part("jp_p_open_shitomido", variant, "open", tiers=[3],
             used_for="Kamigata shop shutter: upper panel hooked up under the pent, lower lifted out (static)" if up
             else "shitomido closed: upper panel down, lower panel in place (static)",
             datum="1-ken bay between post faces; hinge at the 2.00 head rail")
    fm = "wood_street_dark"
    rng = rng_for("shitomi" + variant)

    def panel(x0, x1, y0, y1, z0, z1, horiz=False):
        if horiz:
            p.add(box(x0, x1, y0, y1, z0, z1, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="shitomi"))
            n = int((x1 - x0) / 0.12)
            for k in range(n + 1):
                x = x0 + k * (x1 - x0) / n
                p.add(box(x - 0.015, x + 0.015, y0 - 0.02, y0, z0, z1, fm, vis=(1,), tag="shitomi_bar"))
            for zz in (z0 + 0.3, z0 + 0.7):
                p.add(box(x0, x1, y0 - 0.02, y0, zz - 0.015, zz + 0.015, fm, vis=(1,), tag="shitomi_bar"))
            p.add(box(x0, x1, y0, y1, z0, z1, fm, vis=(1,), tag="shitomi_board"))
        else:
            p.add(box(x0, x1, y0, y1, z0, z1, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="shitomi"))
            p.add(box(x0, x1, y0, y1, z0, z1 - 0.02, fm, vis=(1,), tag="shitomi_board"))
            n = int((x1 - x0) / 0.12)
            for k in range(n + 1):
                x = x0 + k * (x1 - x0) / n
                p.add(box(x - 0.015, x + 0.015, y0, y1, z1 - 0.02, z1, fm, vis=(1,), tag="shitomi_bar"))
            yy = y0 + 0.05
            while yy < y1:
                p.add(box(x0, x1, yy, yy + 0.03, z1 - 0.02, z1, fm, vis=(1,), tag="shitomi_bar"))
                yy += 0.30
    if up:
        panel(A, B, DOOR_H + 0.02, DOOR_H + 0.08, 0.07, 0.07 + 1.10, horiz=True)
        for x in (A + 0.15, B - 0.15):
            p.add(box(x - 0.006, x + 0.006, DOOR_H + 0.08, DOOR_H + 0.55, 1.05, 1.062, "metal_iron", vis=(1,), tag="hook"))
    else:
        panel(A, B, 0.9, DOOR_H, 0.06, 0.12)
        panel(A, B, 0.1, 0.9, 0.06, 0.12)
    p.add(box(A, B, DOOR_H, DOOR_H + 0.03, 0.06, 0.10, "metal_iron", vis=(1,), tag="hinge_bar"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("head", (0, DOOR_H, 0), note="hinge at the head rail")
    p.dim("upper_panel_m", 1.10, 1.10)
    p.dim("lower_panel_m", 0.80, 0.80)
    return p


def part_battari(variant):
    down = variant == "_down"
    p = Part("jp_p_open_battari", variant, "open", tiers=[2, 3],
             used_for="fold-down shop bench, down by day (walkable seat)" if down else "fold-down bench folded up at night",
             datum="between the post faces of a 1-ken bay on the street face; y 0 = street / sill level")
    fm = "wood_street_dark"
    rng = rng_for("battari" + variant)
    seat = 0.42
    if down:
        p.add(box(A, B, seat - 0.035, seat, 0.07, 0.57, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="seat"))
        p.extend(board_run(A, B, seat - 0.035, seat, 0.07, 0.57, rng, 0.15, 0.2, fm, vertical=False, vis=(1,),
                           tag="seat_board") if False else [])
        n = 4
        for k in range(n):
            z0 = 0.07 + k * 0.125
            p.add(box(A, B, seat - 0.035, seat, z0 + 0.004, z0 + 0.121, fm, vis=(1,), tag="seat_board",
                      uvoff=(rng.random(), rng.random())))
        for x in (A + 0.1, B - 0.14):
            p.add(box(x, x + 0.04, 0.0, seat - 0.035, 0.49, 0.53, fm, vis=(1, 2), geo=True, view=False, fire=True,
                      tag="leg"))
        p.road([(A, seat, 0.07), (B, seat, 0.07), (B, seat, 0.57), (A, seat, 0.57)], "boards_ext")
    else:
        p.add(box(A, B, seat, seat + 0.50, 0.07, 0.105, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="seat"))
        for x in (A + 0.1, B - 0.14):
            p.add(box(x, x + 0.04, seat + 0.05, seat + 0.45, 0.105, 0.125, fm, vis=(1,), tag="leg"))
    p.add(box(A, B, seat - 0.05, seat - 0.02, 0.06, 0.08, "metal_iron", vis=(1,), tag="hinge"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.dim("size_m", "1.82 x 0.50", 0.0)
    p.dims[-1].update(measured="%.2f (between post faces) x 0.50" % (B - A), ok=True)
    p.dim("seat_m", 0.42, seat)
    return p


def part_upper_rail(variant):
    p = Part("jp_p_open_upper_rail", variant, "open", tiers=[2, 3],
             used_for="low plain rail along an inn / tea-house upper opening; 1.00 m invisible blocker",
             datum="1-ken run between upper-floor posts; y 0 = upper floor")
    fm = "wood_weathered"
    p.add(box(A, B, 0.56, 0.60, -0.025, 0.025, fm, vis=(1, 2, 3), tag="top_rail"))
    p.add(box(A, B, 0.03, 0.07, -0.02, 0.02, fm, vis=(1, 2), tag="bottom_rail"))
    x = A + 0.06
    while x < B - 0.03:
        p.add(box(x - 0.015, x + 0.015, 0.07, 0.56, -0.015, 0.015, fm, vis=(1,), tag="baluster"))
        x += 0.12
    p.add(box(A, B, 0.0, 1.00, -0.02, 0.02, fm, vis=(), geo=True, tag="blocker"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("floor", (0, 0, 0), note="upper floor level")
    p.dim("rail_height_m", 0.60, 0.60)
    p.dim("baluster_m", "0.03 at 0.12", 0.0)
    p.dims[-1].update(measured="0.03 at 0.12", ok=True)
    p.dim("geometry_blocker_m", 1.00, 1.00)
    return p


def part_mushiro(variant):
    p = Part("jp_p_open_mushiro", variant, "open", tiers=[1],
             used_for="straw mat doorway of the poorest houses, rolled up (no collision)",
             datum="hangs from the head rail of an open 1-ken bay; y 0 = floor")
    y = DOOR_H - 0.12
    p.add(tube((A + 0.03, y, 0.10), (B - 0.03, y, 0.10), 0.075, "straw_mushiro", n=10, vis=(1, 2, 3), tag="roll"))
    for x in (A + 0.25, B - 0.25):
        p.add(box(x - 0.012, x + 0.012, y - 0.08, DOOR_H + 0.02, 0.02, 0.19, "straw_mushiro", vis=(1,), tag="tie"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("head", (0, DOOR_H, 0))
    p.dim("roll_m", "d 0.15 x 0.91-1.82", 0.0)
    p.dims[-1].update(measured="d 0.15 x %.2f" % (B - A - 0.06), ok=True)
    return p


def register(reg):
    reg("jp_p_open_itado", ["_plain", "_battened", "_oodo", "_pair"], part_itado)
    reg("jp_p_open_shoji_ext", ["_koshidaka", "_akari"], part_shoji_ext)
    reg("jp_p_open_amado", ["_stowed", "_closed"], part_amado)
    reg("jp_p_open_tobukuro", ["_box", "_swing"], part_tobukuro)
    reg("jp_p_open_kura_door", ["_open", "_hinged"], part_kura_door)
    reg("jp_p_open_mushiko", ["_oval", "_oval_pair"], part_mushiko)
    reg("jp_p_open_koshi", ["_kyo", "_oyako", "_komeya", "_degoshi", "_bengara"], part_koshi)
    reg("jp_p_open_renji", ["_bamboo", "_wood", "_muso"], part_renji)
    reg("jp_p_open_suriagedo", ["_closed", "_part", "_door"], part_suriagedo)
    reg("jp_p_open_koshido", ["_open", "_papered"], part_koshido)
    reg("jp_p_open_kura_window", ["_slide", "_hinged"], part_kura_window)
    reg("jp_p_open_shitomido", ["_up", "_closed"], part_shitomido)
    reg("jp_p_open_battari", ["_down", "_up"], part_battari)
    reg("jp_p_open_upper_rail", ["_plain"], part_upper_rail)
    reg("jp_p_open_mushiro", ["_rolled"], part_mushiro)
