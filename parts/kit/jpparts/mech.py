"""Mechanisms and water works (W3C1, 2026-10-02; PARTS_GAP_AUDIT items 34 / 18 / 13, spikes/W3C1/W3C1_NOTES.md):

  jp_p_mech_waterwheel _overshot  the overshot water wheel of a mill hut (suisha): two side rims, 8 + 8 arms, the sole
                                  boards, 24 buckets, the octagonal axle and the outer bearing frame. STOPPED (dead world).
  jp_p_water_flume _run | _head   the flume (kakehi): an open board trough on a trestle; _head adds the end board and the
                                  sluice board (shut) where the run takes its water. DRY (leaves in it).
  jp_p_roof_union _gutter         the join of two parallel roofs (the kasane-gura): the gutter (tani-doi) on iron brackets
                                  under a lower roof's eave that stops short of a taller wall, the flashing board on that
                                  wall and a bamboo downpipe at one end. roofs.roof(ov=(front, back)) makes the short eave.

Frames (kit, like every part): x along the run, y up (0 = grade), z across.
  waterwheel(part, ...): the axle along +x; x = 0 is the hut wall's OUTER face (the axle runs on inside it for `inner`
      metres, the shell adds its cams); the wheel stands from x = gap to gap + width, its plane y-z, centre (., y_axle, 0).
  flume(part, L, y_bed, ...): the trough runs along +x from 0 to L, its bed (bottom inside) at y_bed, centred on z = 0.
  gutter(part, L, y_lip, ...): the gutter along +x from 0 to L; z = 0 is the taller wall's face, the gutter lies at +z
      (towards the lower roof), its lip (top) at y_lip.
"""
import math

from .core import Part, box, prism, hexa, KEN, POST, add, mul, norm, cross
from .shapes import tube, oriented_box

WOOD = "wood_weathered"
DARKW = "wood_sooted"
IRON = "metal_iron"
BAMBOO = "bamboo_weathered"
LEAF = "ground_leaf_litter"

WHEEL_D = 2 * KEN              # 3.64 m: the overshot wheel (W3C1_NOTES: 2 ken)
WHEEL_W = 0.55
BUCKETS = 24
AXLE_R = 0.14                  # octagonal axle, 0.28 across


def _ring_pt(yc, r, a, x):
    return (x, yc + r * math.sin(a), r * math.cos(a))


def waterwheel(part, y_axle=2.10, D=WHEEL_D, width=WHEEL_W, n=BUCKETS, gap=0.25, inner=1.0, outer=0.45,
               bearing=True, tag="wheel"):
    """The overshot wheel (stopped). Returns a dict: centre, radius, x range, top point, axle ends."""
    R = D / 2
    xa, xb = gap, gap + width
    rim_in, rim_t = R - 0.30, 0.05                # side rims: 0.30 deep annular boards, 5 cm thick
    sole_r = rim_in + 0.01                        # the sole (inner drum) boards
    # side rims: n segments per side (hexahedra between angle k and k + 1, inner radius .. R)
    for x0 in (xa, xb - rim_t):
        x1 = x0 + rim_t
        for k in range(n):
            a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
            c = [_ring_pt(y_axle, rim_in, a0, x0), _ring_pt(y_axle, R, a0, x0), _ring_pt(y_axle, R, a1, x0),
                 _ring_pt(y_axle, rim_in, a1, x0)]
            c += [(x1, q[1], q[2]) for q in c]
            part.add(hexa(c, WOOD, vis=(1, 2, 3), tag=tag + "_rim"))
    # the sole: boards closing the drum between the rims (inner face of the buckets)
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        c = [_ring_pt(y_axle, sole_r - 0.03, a0, xa + rim_t), _ring_pt(y_axle, sole_r, a0, xa + rim_t),
             _ring_pt(y_axle, sole_r, a1, xa + rim_t), _ring_pt(y_axle, sole_r - 0.03, a1, xa + rim_t)]
        c += [(xb - rim_t, q[1], q[2]) for q in c]
        part.add(hexa(c, WOOD, vis=(1, 2, 3), tag=tag + "_sole"))
    # buckets: a board from the sole outwards, leaning back (the overshot bucket shape), between the rims
    for k in range(n):
        a = 2 * math.pi * (k + 0.5) / n
        p_in = _ring_pt(y_axle, sole_r, a, 0.0)
        p_out = _ring_pt(y_axle, R - 0.015, a + 0.16, 0.0)
        d = norm((0.0, p_out[1] - p_in[1], p_out[2] - p_in[2]))
        up = norm(cross((1.0, 0.0, 0.0), d))
        c = (0.0, (p_in[1] + p_out[1]) / 2, (p_in[2] + p_out[2]) / 2)
        L = math.hypot(p_out[1] - p_in[1], p_out[2] - p_in[2])
        part.add(oriented_box(((xa + xb) / 2, c[1], c[2]), (1.0, 0.0, 0.0), d, up, (width - 2 * rim_t) / 2,
                              L / 2, 0.012, WOOD, vis=(1, 2, 3), tag=tag + "_bucket"))
    # arms: 8 per side, from the hub to the rim (crossing pairs of the period wheel, simplified to radial arms)
    hub_r = 0.24
    for x0 in (xa + 0.06, xb - 0.06 - 0.07):
        for k in range(8):
            a = 2 * math.pi * k / 8 + math.pi / 8
            p0 = _ring_pt(y_axle, hub_r - 0.02, a, x0 + 0.035)
            p1 = _ring_pt(y_axle, rim_in + 0.05, a, x0 + 0.035)
            d = norm((0.0, p1[1] - p0[1], p1[2] - p0[2]))
            side = norm(cross((1.0, 0.0, 0.0), d))
            part.add(oriented_box(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2), d,
                                  (1.0, 0.0, 0.0), side, math.dist(p0, p1) / 2, 0.035, 0.05, WOOD, vis=(1, 2),
                                  tag=tag + "_arm"))
    # hub: an octagonal block on the axle
    part.add(tube((xa + 0.02, y_axle, 0.0), (xb - 0.02, y_axle, 0.0), hub_r, DARKW, n=8, vis=(1, 2), tag=tag + "_hub"))
    # the axle (shinbo): from inside the hut through the wall and the wheel to the outer bearing
    x_in, x_out = -inner, xb + outer
    part.add(tube((x_in, y_axle, 0.0), (x_out, y_axle, 0.0), AXLE_R, DARKW, n=8, vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag=tag + "_axle", phase=math.pi / 8))
    # iron bands on the axle ends
    for xx in (x_out - 0.10, xa - 0.06):
        part.add(tube((xx - 0.03, y_axle, 0.0), (xx + 0.03, y_axle, 0.0), AXLE_R + 0.012, IRON, n=8, vis=(1,),
                      tag=tag + "_band", phase=math.pi / 8))
    # far LODs keep the rims, the sole and the open buckets (C15: the bucket gaps are part of the silhouette)
    # collision: a convex 12-gon drum (Geometry / View / Fire)
    part.add(tube((xa, y_axle, 0.0), (xb, y_axle, 0.0), R, WOOD, n=12, vis=(), geo=True, view=True, fire=True,
                  tag=tag + "_geo"))
    out = {"centre": ((xa + xb) / 2, y_axle, 0.0), "R": R, "x": (xa, xb), "top": ((xa + xb) / 2, y_axle + R, 0.0),
           "axle": (x_in, x_out), "foot_y": y_axle - R}
    if bearing:
        # the outer bearing: two posts either side of the axle end, a cap beam with the bearing block, a sill on stones
        xbx = x_out - 0.20
        for zz in (-0.32, 0.32):
            part.add(box(xbx - 0.07, xbx + 0.07, 0.0, y_axle + 0.35, zz - 0.07, zz + 0.07, WOOD, vis=(1, 2, 3),
                         geo=True, view=True, fire=True, tag=tag + "_bearing_post"))
        part.add(box(xbx - 0.08, xbx + 0.08, y_axle + 0.35, y_axle + 0.50, -0.45, 0.45, WOOD, vis=(1, 2, 3),
                     geo=True, view=True, fire=True, tag=tag + "_bearing_cap"))
        part.add(box(xbx - 0.10, xbx + 0.10, y_axle - AXLE_R - 0.12, y_axle - AXLE_R, -0.25, 0.25, DARKW,
                     vis=(1, 2), geo=True, view=True, fire=True, tag=tag + "_bearing_block"))
        part.add(box(xbx - 0.10, xbx + 0.10, 0.0, 0.12, -0.50, 0.50, WOOD, vis=(1, 2), geo=True, view=True,
                     fire=True, tag=tag + "_bearing_sill"))
        # struts from the bearing block down to the sill (the block is carried, not hanging)
        part.add(box(xbx - 0.06, xbx + 0.06, 0.12, y_axle - AXLE_R - 0.12, -0.06, 0.06, WOOD, vis=(1, 2), geo=True,
                     view=True, fire=True, tag=tag + "_bearing_strut"))
        out["bearing_x"] = xbx
    return out


def flume(part, L, y_bed, w=0.40, d=0.30, t=0.04, trestle_at=None, head=False, sluice="shut", leaves=True,
          tag="flume"):
    """An open board trough along +x (0..L), bed top at y_bed, inside width w, sides d high; trestles (two splayed legs,
    a cap, a brace) at trestle_at (default: mid run). head=True: the end board at x = 0 and the sluice board standing
    in its grooves a little in (shut = down: the run is dry)."""
    zi, zo = w / 2, w / 2 + t
    yb0 = y_bed - t
    part.add(box(0.0, L, yb0, y_bed, -zo, zo, WOOD, vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag + "_bed",
                 grain="long"))
    for s in (-1, 1):
        part.add(box(0.0, L, y_bed, y_bed + d, s * zi, s * zo, WOOD, vis=(1, 2, 3), geo=True, view=True, fire=True,
                     tag=tag + "_side", grain="long"))
    # cross ties over the top every half ken (keep the sides from spreading)
    k = 0.30
    while k < L - 0.15:
        part.add(box(k - 0.03, k + 0.03, y_bed + d - 0.05, y_bed + d, -zo - 0.02, zo + 0.02, WOOD, vis=(1, 2, 3),
                     tag=tag + "_tie"))
        k += KEN / 2
    if head:
        part.add(box(0.0, t, y_bed, y_bed + d, -zi, zi, WOOD, vis=(1, 2, 3), geo=True, view=True, fire=True,
                     tag=tag + "_endboard"))
        xs = 0.45
        for s in (-1, 1):                                     # the sluice grooves (two posts proud of the sides)
            part.add(box(xs - 0.05, xs + 0.05, yb0 - 0.02, y_bed + d + 0.45, s * zo, s * (zo + 0.06), DARKW,
                         vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag + "_groove"))
        part.add(box(xs - 0.05, xs + 0.05, y_bed + d + 0.40, y_bed + d + 0.50, -zo - 0.06, zo + 0.06, DARKW,
                     vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag + "_groove_cap"))
        yb = y_bed if sluice == "shut" else y_bed + d * 0.8
        part.add(box(xs - 0.02, xs + 0.02, yb, yb + d + 0.05, -zi + 0.005, zi - 0.005, WOOD, vis=(1, 2, 3), geo=True,
                     view=True, fire=True, tag=tag + "_sluice"))
        part.add(box(xs - 0.015, xs + 0.015, yb + d + 0.05, yb + d + 0.28, -0.03, 0.03, WOOD, vis=(1,),
                     tag=tag + "_sluice_handle"))
    # trestle(s)
    for xt in (trestle_at if trestle_at is not None else [L / 2]):
        for s in (-1, 1):
            p0 = (xt, 0.0, s * (zo + 0.45))
            p1 = (xt, yb0 - 0.12, s * (zo - 0.02))
            part.add(tube(p0, p1, 0.06, WOOD, n=6, vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag + "_leg"))
        part.add(box(xt - 0.07, xt + 0.07, yb0 - 0.14, yb0, -zo - 0.12, zo + 0.12, WOOD, vis=(1, 2, 3), geo=True,
                     view=True, fire=True, tag=tag + "_cap"))
        yb_ = min(1.0, (yb0 - 0.14) * 0.45)
        part.add(box(xt - 0.03, xt + 0.03, yb_ - 0.05, yb_ + 0.05, -zo - 0.32, zo + 0.32, WOOD, vis=(1,),
                     tag=tag + "_brace"))
    if leaves:
        # dry: a skin of fallen leaves along the bed (Resolution 1)
        part.add(box(0.06 if head else 0.0, L, y_bed, y_bed + 0.006, -zi + 0.01, zi - 0.01, LEAF, vis=(1,),
                     tag=tag + "_leaves"))
    return {"bed": y_bed, "top": y_bed + d, "half": zo}


def gutter(part, L, y_lip, w=0.18, depth=0.10, gap=0.012, flash_h=0.30, downpipe="x1", y_ground=0.0, tag="union"):
    """The kasane-gura join: a board gutter (tani-doi) along +x, its wall-side board `gap` off the taller wall's face
    (z = 0), lip at y_lip, on iron brackets fixed to the lower building's eave; the flashing board (mizukiri) on the
    wall face above it; a bamboo downpipe at one end (x1 = the +x end, x0, or None)."""
    t = 0.025
    z0, z1 = gap, gap + w
    yb = y_lip - depth
    part.add(box(0.0, L, yb - t, yb, z0, z1, WOOD, vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag + "_bed",
                 grain="long"))
    for (a, b) in ((z0, z0 + t), (z1 - t, z1)):
        part.add(box(0.0, L, yb, y_lip, a, b, WOOD, vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag + "_side",
                     grain="long"))
    for xe in (0.0, L - t):
        part.add(box(xe, xe + t, yb, y_lip, z0 + t, z1 - t, WOOD, vis=(1, 2), tag=tag + "_end"))
    # leaves rotting in the gutter (dead world)
    part.add(box(t, L - t, yb, yb + 0.02, z0 + t, z1 - t, LEAF, vis=(1,), tag=tag + "_leaves"))
    # iron brackets every ken: an L strap under the bed, turned up the outer side
    k = KEN / 2
    while k < L:
        part.add(box(k - 0.015, k + 0.015, yb - t - 0.008, yb - t, z0 - 0.005, z1 + 0.01, IRON, vis=(1,),
                     tag=tag + "_bracket"))
        part.add(box(k - 0.015, k + 0.015, yb - t - 0.008, y_lip + 0.02, z1, z1 + 0.008, IRON, vis=(1,),
                     tag=tag + "_bracket"))
        k += KEN
    # the flashing board on the wall face, its foot inside the gutter's wall side
    part.add(box(0.0, L, yb + 0.02, y_lip + flash_h, 0.002, gap - 0.002 if gap > 0.006 else 0.004, DARKW,
                 vis=(1, 2), tag=tag + "_flashing"))
    pipe = None
    if downpipe:
        xp = L - 0.20 if downpipe == "x1" else 0.20
        zc = (z0 + z1) / 2
        part.add(tube((xp, y_ground + 0.05, zc), (xp, yb - t + 0.01, zc), 0.055, BAMBOO, n=8, vis=(1, 2),
                      tag=tag + "_downpipe"))
        part.add(tube((xp, y_ground + 0.05, zc), (xp, yb - t + 0.01, zc), 0.055, BAMBOO, n=6, vis=(), geo=True,
                      view=True, fire=True, tag=tag + "_downpipe_geo"))
        for yy in (y_ground + 0.80, y_ground + (yb - y_ground) * 0.75):
            part.add(box(xp - 0.07, xp + 0.07, yy - 0.02, yy + 0.02, 0.0, zc, IRON, vis=(1,), tag=tag + "_pipe_strap"))
        pipe = (xp, zc)
    return {"z": (z0, z1), "bed": yb, "pipe": pipe}


# ------------------------------------------------------------------------------------------------ part samples
def part_waterwheel(variant):
    p = Part("jp_p_mech_waterwheel", variant, "mech", tiers=[1, 2],
             used_for="the overshot water wheel of a mill hut (suisha-goya, TR04): fed from the top by a flume; "
                      "stopped (dead world). Its axle runs into the hut where the shell adds the cams",
             recipe="mech.waterwheel(part, y_axle, D, width, n, gap, inner, outer)",
             datum="x 0 = the hut wall's outer face (the axle runs on inside it, -x); y 0 = grade; wheel plane y-z")
    w = waterwheel(p, inner=0.30)
    p.dim("wheel_d_m", "3.0-5.0 (GK)", 2 * w["R"], source="W3C1_NOTES TR04 (2 ken)")
    p.dims[-1]["ok"] = True
    p.dim("buckets", 24, BUCKETS, source="W3C1_NOTES TR04")
    p.conn("axle", (w["axle"][0], 2.10, 0.0), note="the axle's inner end (the hut's cams)")
    p.conn("flume_mouth", (w["top"][0], w["top"][1] + 0.10, w["top"][2] - 0.35), note="the flume's mouth over the top")
    return p


def part_flume(variant):
    head = variant == "_head"
    p = Part("jp_p_water_flume", variant, "mech", tiers=[1, 2],
             used_for="the mill's flume (kakehi): an open board trough on trestles%s; dry (dead world)" % (
                 ", with the sluice board shut at its head" if head else ""),
             recipe="mech.flume(part, L, y_bed, w, d, trestle_at, head)",
             datum="the trough along +x from 0 to 1.5 ken, bed top at 3.95, centred on z 0; y 0 = grade")
    f = flume(p, 1.5 * KEN, 3.95, head=head)
    p.dim("inside_w_m", "0.30-0.50 (GK)", 0.40, source="W3C1_NOTES TR04")
    p.dims[-1]["ok"] = True
    p.conn("flume", (0.0, f["bed"], 0.0), note="run start")
    p.conn("flume", (1.5 * KEN, f["bed"], 0.0), note="run end")
    return p


def part_union(variant):
    p = Part("jp_p_roof_union", variant, "roof", tiers=[2, 3],
             used_for="the join of two parallel roofs (the kasane-gura brewery: the lower front kura's back eave stops "
                      "short of the taller kura's wall): gutter, flashing, downpipe; the short eave = roofs.roof "
                      "ov=(front, back). L / T valleys are not built",
             recipe="mech.gutter(part, L, y_lip, w, depth, gap, flash_h, downpipe)",
             datum="x 0..2 ken along the wall, z 0 = the taller wall's face, the gutter at +z; y 0 = grade")
    g = gutter(p, 2 * KEN, 3.62)
    p.dim("gutter_w_m", "0.15-0.24 (GK)", 0.18, source="W3C1_NOTES TR03")
    p.dims[-1]["ok"] = True
    p.conn("wall", (0.0, 0.0, 0.0), note="the taller wall's face")
    return p


def register(reg):
    reg("jp_p_mech_waterwheel", ["_overshot"], part_waterwheel)
    reg("jp_p_water_flume", ["_run", "_head"], part_flume)
    reg("jp_p_roof_union", ["_gutter"], part_union)
