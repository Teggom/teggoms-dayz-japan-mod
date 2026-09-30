"""Party parts of snap-together townhouse units (B2 parts 2-4 + the seam cap; PARTS_GAP_AUDIT §3 parts 7, 14, 25,
§5 parts 2-4, §6 risk 1), and the townhouse template hooks that use them (templates/townhouse.py HOOKS).

The rules they follow (audit §6 risk 1; PLAYBOOK §15 T5, T7b, T8):
  - EACH UNIT SEALS ON ITS OWN, because a neighbour may be missing: the party wall is a complete end wall on the unit's
    own wall line, half a wall inside the lot (the lot line is LOT_PAD outside the wall line), cut to the roof section
    and sealed to the rafter underside.
  - NOTHING COPLANAR ACROSS A SEAM: every roof, pent, lean-to, keta and flashing of a unit stops LOT_GAP (2 mm) inside
    its lot line, so two neighbours' faces are 4 mm apart and never overlap in one plane.
  - PARTY ROOF ENDS ARE FLUSH: no verge tiles, bargeboards, onigawara or purlin ends (roofs.roof(plain_ends=...)); a
    closure band (plaster on tile, a board on boards) closes the covering's section at the end, so a step to a lower
    neighbour, or a missing one, shows a clean end; the ridge stack gets an end plate.
  - ONE SEAM CAP PER SEAM: the unit whose finished low-x side is the seam owns it (the udatsu rule): a small tile
    ridge (kawara) or a board and batten (boards) over the joint of the main roofs and lean-tos, and of the street
    pents in Edo (in Kamigata the udatsu covers the pent seam).
  - CORNER UNITS WRAP THE PENT: the square between the street pent and the side pent gets a hipped pent corner (two
    convex slopes meeting on a hip, hip ridge, purlin return, a diagonal corner bracket), nothing through a roof.

Frames: the townhouse template's canonical kit frame (x along the street, z 0 = street wall line, +z = street, y 0 =
grade). Part samples use the same numbers (the Kamigata unit section: eave 4.63, pent 3.30).
"""
import math

from .core import Part, box, prism, hexa, KEN, HALF, POST, KETA_H, add, sub, mul, norm, cross
from .shapes import oriented_box, frame_of, clean_poly
from . import walls, frame, roofs as R, kawara as K, roofparts, leanto
from .assemble import Builder

LOT_GAP = 0.002             # roof / pent / lean-to / keta ends stop this far inside the lot line
BAND_T = 0.03               # closure band thickness
KAWARA = ("sangawara", "hongawara")


def cover_h(fam):
    """Height of the covering top above the rafter underside plane (kawara field rolls / board courses)."""
    if fam in KAWARA:
        return R.STACK[fam] + 0.055 + 0.022
    if fam == "thatch":
        return R.STACK[fam] + 0.60
    return R.STACK[fam] + 0.014


def body_h(fam):
    """Top of the roof collision body (roofs.collision h_top) above the rafter underside plane."""
    return R.STACK[fam] + (0.05 if fam in KAWARA else 0.012)


# ------------------------------------------------------------------------------------------------ recipes
def gable_party(part, D, t, eave_y, finish="wall_nakanuri", thick=0.075, tie=True):
    """The party wall's gable (local wall frame: x 0..D across the span, +z out): tie beam, posts on the ken grid and
    the ridge post, plain earth panels. Every panel AND post top is cut to the roof line (the rafter underside), so the
    wall is sealed to the roof: no slit over a post, nothing into the roof body (C12). Exterior face earth, the loft
    face the interior clay (PLAYBOOK §15 T6)."""
    yr = walls.roof_line(D, t, eave_y)
    fm = "wood_weathered"
    mats = walls.interior_mats(finish, "back")
    if tie:
        part.add(box(-0.06, D + 0.06, eave_y - 0.21, eave_y, -0.06, 0.06, fm, vis=(1, 2, 3), geo=True, view=True,
                     fire=True, tag="tie_beam"))
    cols = sorted({round(k * KEN, 4) for k in range(1, int(D / KEN) + 1) if k * KEN < D - 0.05} | {round(D / 2, 4)})

    def top_poly(a, b):
        pts = [(a, eave_y), (b, eave_y), (b, yr(b))]
        if a < D / 2 - 1e-6 < b:
            pts.append((D / 2, yr(D / 2)))
        pts.append((a, yr(a)))
        return clean_poly(pts)
    for x in cols:
        part.add(prism(top_poly(x - 0.06, x + 0.06), "z", -0.06, 0.06, fm, vis=(1, 2, 3), geo=True, view=True,
                       fire=True, tag="gable_post", grain="long"))
    edges = [0.0] + cols + [D]
    for i in range(len(edges) - 1):
        a = edges[i] + (0.06 if i > 0 else 0.0)
        b = edges[i + 1] - (0.06 if i < len(edges) - 2 else 0.0)
        pc = top_poly(a, b)
        if len(pc) >= 3:
            part.add(prism(pc, "z", -thick / 2, thick / 2, mats, vis=(1, 2, 3), geo=True, view=True, fire=True,
                           tag="gable_infill"))
    return yr(D / 2)


def build_party_wall(B, fr, D, lv, pitch, which="omoya", ytop=None, name="party"):
    """The party wall on the wall-line frame fr (+z = out, towards the lot line): a stone footing course with a dodai,
    posts, the earth wall from the sill up (interior clay on the room face), and for the omoya the floor beam, the
    upper wall and the party gable cut to the roof section. which='geya': the lean-to's sloped wall under ytop(lx).
    The far LOD (Resolution 3) gets ONE slab with the wall's outline instead of its posts, panels and gable pieces
    (townhouse rows put dozens of units in view)."""
    n0 = len(B.H.solids)
    _party_wall_detail(B, fr, D, lv, pitch, which, ytop, name)
    for x in B.H.solids[n0:]:
        if 3 in x.vis:
            x.vis = set(x.vis) - {3}
    y0 = lv["doma"] - 0.20
    if which == "geya":
        poly = [(0.0, y0), (D, y0), (D, ytop(D)), (0.0, ytop(0.0))]
    else:
        yr = walls.roof_line(D, pitch, lv["eave"])
        poly = [(-0.06, y0), (D + 0.06, y0), (D + 0.06, lv["eave"]), (D / 2, yr(D / 2)), (-0.06, lv["eave"])]
    f = B.P(name + "_far")
    f.add(prism(poly, "z", -0.04, 0.04, "wall_nakanuri", vis=(3,), tag="party_far"))
    B.put(f, fr)


def _party_wall_detail(B, fr, D, lv, pitch, which, ytop, name):
    s = B.P(name + "_footing")
    s.add(box(0.0, D, lv["doma"] - 0.20, lv["sill"] - 0.12, -POST / 2, POST / 2, "stone_cut", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="party_footing"))
    s.add(box(-0.06, D + 0.06, lv["sill"] - 0.12, lv["sill"], -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3),
              geo=True, view=True, fire=True, tag="dodai"))
    B.put(s, fr, what="jp_p_wall_party footing + dodai (%s)" % name)
    if which == "geya":
        nodes = [k * KEN for k in range(int(round(D / KEN)) + 1)]
        B.sloped_wall(fr, name, nodes, lv["sill"], ytop, head_y=lv["sill"] + 2.0,
                      what="jp_p_wall_party _geya: sloped earth wall under the lean-to (%s)" % name)
        return
    B.posts_on(fr, [KEN, KEN + HALF, 2 * KEN], lv["sill"], lv["gable_tie"])
    B.wall(fr, name, "shinkabe", 0.0, D, lv["sill"], lv["ceil"], head=False)
    s = B.P(name + "_beam")
    s.add(box(-0.06, D + 0.06, lv["ceil"], lv["loft"], -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="floor_beam"))
    B.put(s, fr)
    B.wall(fr, name + "_upper", "shinkabe", 0.0, D, lv["loft"], lv["gable_tie"], finish="nakanuri", head=False)
    g = B.P(name + "_gable")
    gable_party(g, D, pitch, lv["eave"])
    B.put(g, fr, what="jp_p_wall_party _omoya: plain earth wall cut to the roof section (%s)" % name)


def end_band(part, x_edge, sg, z0, z1, yfn, h_lo, h_hi, mat, thick=BAND_T, vis=(1, 2, 3), tag="party_closure"):
    """Closure band at a flush roof end: a vertical slab in the plane x = x_edge (inside it: sg = +1 when the end faces
    +x), following one slope from z0 to z1 (yfn(z) = the rafter underside), from h_lo to h_hi above it."""
    xa, xb = sorted((x_edge, x_edge - sg * thick))
    poly = [(yfn(z0) + h_lo, z0), (yfn(z1) + h_lo, z1), (yfn(z1) + h_hi, z1), (yfn(z0) + h_hi, z0)]
    return part.add(prism(poly, "x", xa, xb, mat, vis=vis, tag=tag))


def roof_end(part, x_edge, sg, W, D, eave_y, t, ov, fam, ridge=None, courses=3):
    """jp_p_roof_party_end on a kirizuma main roof built with roofs.roof(..., plain_ends): the closure band over both
    slopes and the ridge-end plate. Add it to the ROOF part (the band lies in the roof body, C12 is per sub-part)."""
    h = D / 2
    kaw = fam in KAWARA
    mat = "wall_shikkui" if kaw else "wood_weathered"
    hi = cover_h(fam) + 0.02
    end_band(part, x_edge, sg, ov, -h, lambda z: eave_y - t * z, -0.03, hi, mat)
    end_band(part, x_edge, sg, -D - ov, -h, lambda z: eave_y + t * (z + D), -0.03, hi, mat)
    if kaw and ridge:
        yr = ridge[0][1]
        base = yr - 0.02
        top = base + 0.04 + courses * 0.025 + 0.08
        xa, xb = sorted((x_edge - sg * 0.002, x_edge - sg * 0.04))
        part.add(box(xa, xb, base - 0.06, top + 0.01, -h - 0.14, -h + 0.14, "wall_shikkui", vis=(1, 2, 3),
                     tag="ridge_end_plate"))


def pent_end(part, x_edge, sg, y_wall, proj, t, kind):
    """Closure at a pent's party end (street pent of a townhouse unit): the pent section boxed in at the lot line."""
    fam = {"tile": "sangawara", "gable": "sangawara", "board": "itabuki", "ishioki": "ishioki", "skirt": "ishioki"}[kind]
    y0 = y_wall - 0.10
    end_band(part, x_edge, sg, 0.06, proj, lambda z: y0 - t * z, -0.05, cover_h(fam) + 0.02,
             "wall_shikkui" if fam in KAWARA else "wood_weathered", vis=(1, 2), tag="pent_closure")


def leanto_end(part, x_edge, sg, z_wall, z_eave, eave_y, t, ov, fam):
    """Closure at a lean-to's party end (the rear kitchen roof of a unit)."""
    end_band(part, x_edge, sg, z_eave - ov, z_wall, lambda z: eave_y + t * (z - z_eave), -0.03, cover_h(fam) + 0.02,
             "wall_shikkui" if fam in KAWARA else "wood_weathered", vis=(1, 2), tag="leanto_closure")


def cap_line(part, x, za, zb, yfn, fam, width=0.20, vis=(1, 2), end_tile=True, tag="seam_cap"):
    """A seam cap along a slope at x from za (low end) to zb (high end); yfn(z) = the rafter underside. Kawara: one
    noshi course on mortar under a round cap, like a small hip ridge; boards: a cap board and a batten."""
    base = body_h(fam) - 0.002
    p0 = (x, yfn(za) + base, za)
    p1 = (x, yfn(zb) + base, zb)
    if fam in KAWARA:
        # no mortar bed: it runs 3 cm wider than the course and exists in Resolution 1-2 only, so over the
        # neighbour's side (no roof of this unit under it) the far LOD would lose it (C15)
        K.ridge(part, p0, p1, courses=2, width=width, cap_d=0.12, mortar=False, end_tiles=(end_tile, False), vis=vis,
                tag=tag)
        return
    d, e1, e2 = frame_of(sub(p1, p0))
    if e2[1] < 0:
        e2 = mul(e2, -1.0)
    c = add(mul(add(p0, p1), 0.5), mul(e2, 0.0125))
    L = math.dist(p0, p1) / 2
    part.add(oriented_box(c, d, e2, norm(cross(d, e2)), L, 0.0125, width / 2, "wood_weathered",
                          vis=tuple(sorted(set(vis) | {3})), tag=tag, grain="long"))
    part.add(oriented_box(add(c, mul(e2, 0.03)), d, e2, norm(cross(d, e2)), L, 0.0175, 0.022, "wood_weathered",
                          vis=(1,), tag=tag + "_batten", grain="long"))


def seam_main(part, x_s, D, eave_y, t, ov, fam, ridge=None, courses=3):
    """Seam cap over the joint of two units' main roofs at the lot line x_s: both slopes, eave to ridge, and (kawara)
    a short ridge bridge over the gap between the two ridge stacks."""
    h = D / 2
    cap_line(part, x_s, ov + 0.05, -h, lambda z: eave_y - t * z, fam)
    cap_line(part, x_s, -D - ov - 0.05, -h, lambda z: eave_y + t * (z + D), fam)
    if fam in KAWARA and ridge:
        yr = ridge[0][1]
        K.ridge(part, (x_s - 0.09, yr - 0.02, -h), (x_s + 0.09, yr - 0.02, -h), courses=courses, end_tiles=False,
                tag="seam_ridge")


def corner_pent(part, proj, t, y_wall, kind, posts=False):
    """jp_p_roof_corner: the hipped corner of two pents that wrap a corner, for the LEFT street corner (the wall corner
    at (0, 0); the street pent runs +x along z = 0 and projects +z, the side pent runs -z along x = 0 and projects -x;
    both attach at y_wall with the projection `proj` and pitch t, as roofparts.pent). Fills the square
    x -proj..0, z 0..proj: two convex slopes on the hip line, their rafters (jack rafters to the hip), covering, eave
    tiles or board edge, hip ridge / hip board, the flashing and purlin returns and a diagonal corner bracket (a corner
    post for the skirt pent on posts). Mirror it for the right corner."""
    fam = {"tile": "sangawara", "board": "itabuki", "skirt": "ishioki"}[kind]
    n0 = len(part.solids)
    y0 = y_wall - 0.10
    ov = proj
    q = 0.06
    st = R.Slope("front", [(0.0, q), (0.0, ov), (-ov, ov), (-q, q)], (0.0, -1.0), (0.0, 0.0), (1.0, 0.0), (0.0, ov),
                 y0, t, ov)
    sd = R.Slope("left", [(-q, 0.0), (-q, q), (-ov, ov), (-ov, 0.0)], (1.0, 0.0), (0.0, 0.0), (0.0, -1.0), (-ov, 0.0),
                 y0, t, ov)
    kaw = fam in KAWARA
    h_top = body_h(fam)
    for sl in (st, sd):
        R.collision(part, sl, h_top, "pottery" if kaw else "wood", "tile_roof" if kaw else "board_roof")
        R.sheathing(part, sl)
        R.rafters(part, sl, spacing=0.303, sec=(0.04, 0.05), only_eave=False)
        if kaw:
            R.tile_bed(part, sl, R.STACK[fam])
            R.kawara_fascia(part, sl, R.STACK[fam])
            F = sl.frame(R.STACK[fam])
            u0, u1 = sl.u_range()
            K.eave_tiles(part, F, u0, u1, style="plain")
            K.field(part, F, u0, u1, K.EXPO, 0.0, r1_fn=lambda u, s_=sl: s_.depth_at(u) / s_.cos, rows_eave=1,
                    rows_ridge=0)
        else:
            R.cover_boards(part, sl, fam, rows_eave=2, rows_ridge=0)
    # hip: from the inner corner (post corner) to the outer eave corner
    pa, pb = (-q, q), (-ov, ov)
    ya, yb = y0 - t * q, y0 - t * ov
    if kaw:
        K.ridge(part, (pa[0], ya + R.STACK[fam] + 0.01, pa[1]), (pb[0], yb + R.STACK[fam] + 0.01, pb[1]), courses=1,
                width=0.18, cap_d=0.12, mortar=True, end_tiles=(False, True), tag="corner_hip")
    else:
        cap = cover_h(fam)
        a3, b3 = (pa[0], ya + cap, pa[1]), (pb[0], yb + cap, pb[1])
        d, e1, e2 = frame_of(sub(b3, a3))
        if e2[1] < 0:
            e2 = mul(e2, -1.0)
        c = add(mul(add(a3, b3), 0.5), mul(e2, 0.015))
        part.add(oriented_box(c, d, e2, norm(cross(d, e2)), math.dist(a3, b3) / 2 + 0.03, 0.015, 0.10, "wood_weathered",
                              vis=(1, 2, 3), tag="corner_hip", grain="long"))
    # hip rafter (sumigi) under the hip line
    a3, b3 = (pa[0], ya, pa[1]), (pb[0] + 0.05, yb + t * 0.05, pb[1] - 0.05)
    d, e1, e2 = frame_of(sub(b3, a3))
    if e2[1] < 0:
        e2 = mul(e2, -1.0)
    part.add(oriented_box(add(mul(add(a3, b3), 0.5), mul(e2, -0.05)), d, e2, norm(cross(d, e2)), math.dist(a3, b3) / 2,
                          0.05, 0.04, "wood_weathered", vis=(1, 2), tag="corner_sumigi", grain="long"))
    # flashing returns (the pents' flashing boards meet over the post corner, no overlap)
    part.add(box(-0.09, 0.0, y_wall - 0.05, y_wall + 0.12, 0.06, 0.09, "wood_weathered", vis=(1, 2), tag="flashing"))
    part.add(box(-0.09, -0.06, y_wall - 0.05, y_wall + 0.12, 0.0, 0.06, "wood_weathered", vis=(1, 2), tag="flashing"))
    # purlin returns at the arm ends + the corner bracket (or the corner post of a skirt pent on posts)
    ye = y0 - t * (ov - 0.12)
    part.add(box(-(ov - 0.10), -0.05, ye - 0.10, ye, ov - 0.18, ov - 0.10, "wood_weathered", vis=(1, 2, 3), geo=True,
                 view=True, fire=True, tag="pent_purlin"))
    part.add(box(-(ov - 0.10), -(ov - 0.18), ye - 0.10, ye, 0.05, ov - 0.18, "wood_weathered", vis=(1, 2, 3), geo=True,
                 view=True, fire=True, tag="pent_purlin"))
    c = ov - 0.14
    if posts:
        part.add(box(-c - 0.06, -c + 0.06, 0.0, ye - 0.10, c - 0.06, c + 0.06, "wood_weathered", vis=(1, 2, 3), geo=True,
                     view=True, fire=True, tag="pent_post"))
    else:
        a3, b3 = (-0.06, ye - 0.145, 0.06), (-c, ye - 0.145, c)
        d = norm(sub(b3, a3))
        part.add(oriented_box(mul(add(a3, b3), 0.5), d, (0.0, 1.0, 0.0), norm(cross(d, (0.0, 1.0, 0.0))),
                              math.dist(a3, b3) / 2, 0.045, 0.03, "wood_weathered", vis=(1, 2), geo=True, view=True,
                              fire=True, tag="udegi"))
    # far LOD: the covering, eave strip and hip carry the silhouette; the boards, fascia and purlins under it leave
    # Resolution 3 (C15 compares top heights only; townhouse rows put many units in view)
    for x in part.solids[n0:]:
        if x.tag in ("sheathing", "kawara_fascia", "pent_purlin") and 3 in x.vis:
            x.vis = set(x.vis) - {3}
    return st, sd


# ------------------------------------------------------------------------------------------------ template hooks
def _lot_x(ctx, side, inset=LOT_GAP):
    """x of the lot line on a canonical side, moved `inset` into the unit."""
    return (-ctx["lot_pad"] + inset) if side == "left" else (ctx["W"] + ctx["lot_pad"] - inset)


def hook_party_wall(B, ctx):
    """townhouse HOOKS['party_wall']: jp_p_wall_party on the unit's end wall line (omoya or lean-to)."""
    lv = ctx["levels"]
    if ctx["part"] == "geya":
        build_party_wall(B, ctx["frame"], ctx["DG"], lv, None, "geya", ytop=ctx["ytop"],
                         name="party_g_%s" % ctx["side"])
    else:
        build_party_wall(B, ctx["frame"], ctx["DO"], lv, ctx["pitch"], "omoya", name="party_%s" % ctx["side"])


def hook_party_roof_end(B, ctx):
    """townhouse HOOKS['party_roof_end']: the flush party end of the main roof (built with plain_ends, see the
    template), the street pent's end closure (unless this unit's own udatsu stands on the seam) and the lean-to's."""
    side = ctx["side"]
    sg = -1.0 if side == "left" else 1.0
    lv = ctx["levels"]
    x_e = _lot_x(ctx, side)
    roof_end(ctx["roof_part"], x_e, sg, ctx["W"], ctx["DO"], lv["eave"], ctx["pitch"], R.EAVE_OV[ctx["covering"]],
             ctx["covering"], ctx["roof_info"]["ridge"], ctx["courses"])
    kind, proj, pt = ctx["pent"]
    if not ctx.get("udatsu_here"):
        p = Part("pent_front", "", "")                   # same name as the pent: C12 treats it as the pent itself
        pent_end(p, x_e, sg, lv["pent"], proj, pt, kind)
        B.merge(p)
    g = ctx.get("geya")
    if g:
        p = Part("roof_geya", "", "")
        leanto_end(p, x_e, sg, g["z_wall"], g["z_eave"], g["eave_y"], g["t"], g["ov"], g["fam"])
        B.merge(p)


def hook_seam_cap(B, ctx):
    """townhouse HOOKS['seam_cap']: the seam cap, built only by the seam's owner (the unit whose finished low-x side is
    the seam; ctx['owner']): main roof + lean-to (both regions), street pent too in Edo (Kamigata: the udatsu)."""
    if not ctx.get("owner"):
        return
    side = ctx["side"]
    x_s = _lot_x(ctx, side, 0.0)
    lv = ctx["levels"]
    seam_main(ctx["roof_part"], x_s, ctx["DO"], lv["eave"], ctx["pitch"], R.EAVE_OV[ctx["covering"]], ctx["covering"],
              ctx["roof_info"]["ridge"], ctx["courses"])
    if ctx["region"] == "edo":
        kind, proj, pt = ctx["pent"]
        fam = {"tile": "sangawara", "gable": "sangawara", "board": "itabuki"}[kind]
        p = Part("pent_front", "", "")
        y0 = lv["pent"] - 0.10
        cap_line(p, x_s, proj + 0.03, 0.06, lambda z: y0 - pt * z, fam, width=0.16)
        B.merge(p)
    g = ctx.get("geya")
    if g:
        p = Part("roof_geya", "", "")
        cap_line(p, x_s, g["z_eave"] - g["ov"] - 0.03, g["z_wall"] - 0.02,
                 lambda z: g["eave_y"] + g["t"] * (z - g["z_eave"]), g["fam"], width=0.18)
        B.merge(p)


def hook_roof_corner(B, ctx):
    """townhouse HOOKS['roof_corner']: the hipped pent corner where the street pent wraps onto the side street."""
    kind, proj, pt = ctx["pent"]
    p = Part("roof_corner", "", "")
    corner_pent(p, proj, pt, ctx["levels"]["pent"], kind)
    if ctx["side"] == "right":
        p = p.transformed(0.0, (ctx["W"], 0.0, 0.0), mirror=True)
        p.pid = "roof_corner"
    B.merge(p)
    B.log.append("jp_p_roof_corner _%s at the %s street corner" % (kind, ctx["side"]))


HOOKS = {"party_wall": hook_party_wall, "party_roof_end": hook_party_roof_end, "roof_corner": hook_roof_corner,
         "seam_cap": hook_seam_cap}


# ------------------------------------------------------------------------------------------------ part samples
LV = {"doma": 0.05, "sill": 0.27, "floor": 0.50, "ceil": 3.00, "loft": 3.15, "keta": 4.45, "eave": 4.63,
      "gable_tie": 4.42, "pent": 3.30, "geya_eave": 2.69}          # the townhouse template's section (Kamigata)
LOT_PAD = POST / 2 + 0.004


def part_wall_party(variant):
    geya = variant == "_geya"
    p = Part("jp_p_wall_party", variant, "wall", tiers=[2, 3],
             used_for=("party wall of a townhouse unit's rear lean-to kitchen: earth wall on a stone course under the "
                       "lean-to's roof line" if geya else
                       "party wall of a snap-together townhouse unit (DW11 / DW12, DW10 rows): its own end wall, half a "
                       "wall inside the lot, stone course + dodai, earth wall, floor beam, upper wall and a plain earth "
                       "gable cut to the roof section and sealed to the rafter underside"),
             recipe="party.build_party_wall(B, frame, D, levels, pitch, 'omoya' | 'geya') (townhouse hook party_wall)",
             datum="the unit's end wall line as a wall part: x 0..%s along it (back -> front), +z = out towards the "
                   "lot line (LOT_PAD %.3f out); y 0 = grade; townhouse levels (sill 0.27, ceiling 3.00, loft 3.15, "
                   "eave 4.63)" % ("1 ken" if geya else "3 ken", LOT_PAD))
    B = Builder(p)
    D = KEN if geya else 3 * KEN
    fr = (0.0, (0.0, 0.0, 0.0))
    if geya:
        t = leanto.PITCH["sangawara"]
        yt = lambda lx: LV["geya_eave"] + t * lx          # noqa: E731
        B.posts_on(fr, [0.0], LV["doma"], yt(0.0))
        B.posts_on(fr, [D], LV["doma"], yt(D))
        build_party_wall(B, fr, D, LV, None, "geya", ytop=yt, name="party_g")
    else:
        B.posts_on(fr, [0.0, D], LV["doma"], LV["keta"])
        build_party_wall(B, fr, D, LV, R.PITCH["sangawara"], "omoya", name="party")
        p.dim("gable_top_m (rafter underside at the ridge)", LV["eave"] + R.PITCH["sangawara"] * D / 2,
              max(s.bbox()[3] for s in p.solids if s.tag in ("gable_infill", "gable_post")), tol=0.005,
              source="sealed to the roof underside (PARTS_GAP_AUDIT §3 part 14)")
    p.dim("wall_thickness_m", 0.075, 0.075, source="shinkabe nakanuri (kit)")
    p.dim("lot_line_offset_m", "0.064", LOT_PAD, source="audit §6 risk 1: half a wall + 4 mm inside the lot line")
    p.dims[-1]["ok"] = abs(LOT_PAD - 0.064) < 1e-6
    for x in (0.0, D) + (() if geya else (KEN, KEN + HALF, 2 * KEN)):
        p.conn("post", (x, 0, 0), hidden=True, note="post in the part")
    p.conn("sill", (0, LV["sill"], 0))
    return p


def _strip_roof(fam, plain_left=True, W=KEN, D=3 * KEN, eave_y=None):
    eave_y = LV["eave"] if eave_y is None else eave_y
    p = Part("strip", "", "")
    gl = LOT_PAD - LOT_GAP if plain_left else R.GABLE_OV[fam]
    sls, info = R.roof(p, W, D, "kirizuma", fam, eave_y=eave_y, courses=5 if fam in KAWARA else None,
                       eave_style="plain", gov=(gl, R.GABLE_OV[fam]), plain_ends=(plain_left, False))
    return p, info, gl


def part_roof_party_end(variant):
    fam = {"_kawara": "sangawara", "_board": "itabuki"}[variant]
    p = Part("jp_p_roof_party_end", variant, "roof", tiers=[2, 3],
             used_for="flush roof end at a townhouse party line (DW11 / DW12): no verge tiles, bargeboard or "
                      "onigawara; %s closure band over the covering's section and a ridge end plate; the roof stops "
                      "2 mm inside the lot line" % ("plaster" if fam in KAWARA else "board"),
             recipe="roofs.roof(..., plain_ends=(left, right)) + party.roof_end(roof, x_edge, side, ...)",
             datum="a 1-ken strip of a 3-ken kirizuma main roof (townhouse eave 4.63), party end on the left: lot line "
                   "x = -%.3f, roof edge x = -%.3f; the right end keeps a normal verge for comparison" % (
                       LOT_PAD, LOT_PAD - LOT_GAP))
    s, info, gl = _strip_roof(fam)
    roof_end(s, -gl, -1.0, KEN, 3 * KEN, LV["eave"], info["t"], info["ov"], fam, info["ridge"], 5)
    p.merge(s)
    p.dim("edge_inside_lot_line_m", LOT_GAP, LOT_PAD - gl, tol=1e-4, source="4 mm between neighbours, no coplanar faces")
    p.dim("closure_band_m", BAND_T, BAND_T)
    p.conn("post", (0, 0, 0), note="the unit's party wall line")
    p.conn("post", (0, 0, -3 * KEN))
    p.conn("verge", (-gl, LV["eave"], 0), note="flush party end (lot line - 2 mm)")
    return p


def part_seam_cap(variant):
    fam = {"_kawara": "sangawara", "_board": "itabuki"}[variant]
    p = Part("jp_p_roof_seam_cap", variant, "roof", tiers=[2, 3],
             used_for="cap over the seam between two townhouse units' roofs, built by the seam's owner only (one per "
                      "seam, like the udatsu): %s over the main roof (both slopes) and the lean-to%s" % (
                          "a small noshi ridge on mortar with a round cap, and a ridge bridge" if fam in KAWARA else
                          "a cap board with a batten", "" if fam in KAWARA else ", and the Edo street pent"),
             recipe="party.seam_main / party.cap_line (townhouse hook seam_cap)",
             datum="the seam (lot line) at x = -%.3f of the jp_p_roof_party_end sample: main roof 3 ken, eave 4.63; "
                   "the sheet shows it on two snapped party-end strips" % LOT_PAD)
    s, info, gl = _strip_roof(fam)
    q = Part("cap", "", "")
    seam_main(q, -LOT_PAD, 3 * KEN, LV["eave"], info["t"], info["ov"], fam, info["ridge"], 5)
    p.merge(q)
    p.dim("cap_width_m", "0.16-0.20", 0.20)
    p.conn("post", (0, 0, 0), note="the owner unit's party wall line (the seam is LOT_PAD outside it)")
    return p


def part_roof_corner(variant):
    kind = variant[1:]
    y_wall, proj, t, posts = {"tile": (3.30, 0.91, 0.40, False), "board": (3.00, 0.91, 0.275, False),
                              "skirt": (2.70, 1.20, 0.25, True)}[kind]
    p = Part("jp_p_roof_corner", variant, "roof", tiers={"tile": [3], "board": [1, 2, 3], "skirt": [2]}[kind],
             used_for={"tile": "hipped corner of a tiled street pent wrapping a corner townhouse unit / corner hatago "
                               "(Kamigata, DW11)",
                       "board": "hipped corner of a board pent wrapping a corner (Edo corner unit, DW12)",
                       "skirt": "corner of the farmhouse skirt pent on posts (G1-6), with its corner post (DW06)"}[kind],
             recipe="party.corner_pent(part, projection, pitch, y_wall, kind) (townhouse hook roof_corner)",
             datum="the LEFT corner of two pents (as jp_p_roof_hisashi_%s: attach %.2f, project %.2f): wall corner at "
                   "the origin, the street pent along +x (z 0), the side pent along -z (x 0); fills x -%.2f..0, "
                   "z 0..%.2f; mirror for a right corner" % (kind, y_wall, proj, proj, proj))
    corner_pent(p, proj, t, y_wall, kind, posts=posts)
    p.dim("projection_m", proj, proj)
    p.dim("pitch_sun", {"tile": 4, "board": 2.75, "skirt": 2.5}[kind], t * 10, tol=0.05)
    p.conn("post", (0, 0, 0), note="the corner post of the building")
    p.conn("eave", (-proj, y_wall - 0.10 - t * proj, proj), note="outer corner of the two eaves (hip foot)")
    return p


def register(reg):
    reg("jp_p_wall_party", ["_omoya", "_geya"], part_wall_party)
    reg("jp_p_roof_party_end", ["_kawara", "_board"], part_roof_party_end)
    reg("jp_p_roof_corner", ["_tile", "_board", "_skirt"], part_roof_corner)
    reg("jp_p_roof_seam_cap", ["_kawara", "_board"], part_seam_cap)
