"""Railed veranda (en) with koran railings and kizahashi front stairs (W2P1, 2026-10-01; jp_p_porch_koran;
PARTS_GAP_AUDIT §3 part 4). Period form and choices: parts/W2P1_NOTES.md.

Kumi-koran (the shrine / temple hall railing): a bottom sill on the en edge (jifuku), short lower struts, a middle
rail (hirageta), short upper struts with a bearing block (totsuka + to), a round top rail (hokogi). Corners: the rails
cross and run out past the corner ('cross'), or end in a corner post ('post'), capped with an onion finial (giboshi)
in the giboshi style. The en boards are kirime-en: laid crosswise, end grain at the edge.

Part frame (PLAYBOOK §10.2): a run along +x on a wall whose centreline is z 0; the en deck runs from the wall face
(z POST/2) out to its edge z = depth (default 1.365, on the 0.455 grid: D5 >= 1.00 m clear to the rail); y 0 = the en
floor top (the hall floor level); grade at y = -drop.

Generators (used by the assemblies and by W2S's shells):
  en_deck(part, x0, x1, z0, z1, drop, along)      deck boards + edge beam + en posts on stones + Geometry + Roadway
  rail(part, p0, p1, style, ends, ...)             one axis-aligned koran run between plan points, end treatments
  kizahashi(part, xa, xb, z_edge, drop, style)     the stair down from the en edge (+z), its side rails and foot posts
  en_wrap(part, W, D, ...)                         the whole en round a W x D hall: front + sides, corners, the stair
                                                   gap, wakishoji screens at the rear ends
Gameplay: Roadway is continuous from the en onto the stair ramp (<= 38 deg, D4) and the foot; the rails are one thin
Geometry slab per run (players don't fall off; bullets and the camera pass the open rails).
"""
import math

from .core import Part, box, prism, hexa, cyl, rings, ngon, stone, KEN, HALF, QK, POST, rng_for
from .shapes import tube, board_run

DEPTH = 1.365          # en edge from the wall centreline (grid): 1.365 - 0.06 - 0.08 = 1.225 m clear to the rail (D5)
RAIL_H = 0.75          # top of the hokogi above the en floor (period 0.6-0.8 on small halls)
STAIR_W = 1.10         # clear between the stair rails (D4 >= 1.10)
STAIR_ANGLE = 37.8     # max walk ramp (D4); the run rounds UP to the 0.455 grid
JIF = (0.07, 0.08)     # jifuku height, depth
EDGE_IN = 0.015        # jifuku outer face inside the deck edge (no coplanar faces, C20)
MAT = "wood_weathered"
METAL = "metal_iron"   # stand-in for bronze (no bronze / copper-patina material; parts/W2P1_NOTES.md)


# ------------------------------------------------------------------------------------------------ helpers
def _ax(p0, p1):
    """Axis-aligned run between plan points (x, z): (axis 'x' | 'z', a0, a1, c) with a0 < a1 along the axis, c the
    fixed coordinate."""
    if abs(p0[1] - p1[1]) < 1e-6:
        return "x", min(p0[0], p1[0]), max(p0[0], p1[0]), p0[1]
    if abs(p0[0] - p1[0]) < 1e-6:
        return "z", min(p0[1], p1[1]), max(p0[1], p1[1]), p0[0]
    raise ValueError("koran runs are axis-aligned: %s -> %s" % (p0, p1))


def _bx(axis, a0, a1, y0, y1, c0, c1, mats, **kw):
    """Box along the run axis: a = along, c = across."""
    if axis == "x":
        return box(a0, a1, y0, y1, c0, c1, mats, **kw)
    return box(c0, c1, y0, y1, a0, a1, mats, **kw)


def giboshi(part, x, z, y, r=0.062, mat=METAL, vis=(1, 2)):
    """Onion finial on a post top at (x, y, z): neck ring, bulb (concave radius profile = convex solid), pointed tip.
    Returns the top height."""
    n = 8
    base = ngon(x, z, r, n, math.pi / n)
    part.add(rings((base, [(y, 1.0), (y + 0.035, 1.0)]), mat, vis=vis, tag="giboshi_neck"))
    part.add(rings((base, [(y + 0.035, 0.80), (y + 0.075, 1.12), (y + 0.115, 1.02), (y + 0.155, 0.66),
                           (y + 0.185, 0.16)]), mat, vis=vis, tag="giboshi"))
    part.add(tube((x, y + 0.183, z), (x, y + 0.235, z), 0.012, mat, n=6, r1=0.002, vis=(1,), tag="giboshi_tip"))
    part.add(rings((ngon(x, z, r * 1.05, n, math.pi / n), [(y, 1.0), (y + 0.235, 1.0)]), mat, vis=(3,),
                   tag="giboshi_lod"))
    return y + 0.235


def end_post(part, x, z, y0, h, style, mat=MAT, size=0.10, tag="oyabashira"):
    """Oyabashira at a rail end / corner / stair gap: octagonal post; giboshi cap (giboshi style) or a cut top with a
    small cap board (plain)."""
    n = 8
    r = size / 2 / math.cos(math.pi / n)
    part.add(rings((ngon(x, z, r, n, math.pi / n), [(y0, 1.0), (y0 + h, 1.0)]), mat, vis=(1, 2, 3), tag=tag,
                   grain="long"))
    if style == "giboshi":
        return giboshi(part, x, z, y0 + h, r=r * 1.04)
    part.add(box(x - size / 2 - 0.012, x + size / 2 + 0.012, y0 + h, y0 + h + 0.03, z - size / 2 - 0.012,
                 z + size / 2 + 0.012, mat, vis=(1, 2), tag="post_cap"))
    return y0 + h + 0.03


# ------------------------------------------------------------------------------------------------ deck
def en_deck(part, x0, x1, z0, z1, drop=1.0, along="z", edge="z1", posts=True, mat=MAT, road=True, step=HALF,
            post_from=None, void=False):
    """The en deck over x0..x1, z0..z1 (floor top y 0). along: the boards' long direction ('z' = crosswise to a wall
    along x: kirime-en). edge: which side is the open outer edge ('z1', 'z0', 'x0', 'x1'): the edge beam and the en
    posts stand under it. Geometry: the deck slab (Geometry / View / Fire) and a Geometry-only block down to grade
    (nobody crawls under a 1 m en)."""
    rng = rng_for(part.name + "en%.2f%.2f%.2f" % (x0, z0, x1))
    part.add(box(x0, x1, -0.10, 0.0, z0, z1, mat, vis=(), geo=True, view=True, fire=True, tag="en_geo"))
    part.add(box(x0 + 0.01, x1 - 0.01, -drop, -0.10, z0 + 0.01, z1 - 0.01, mat, vis=(), geo=True, view=False,
                 fire=None, tag="en_under_block"))
    if road:
        part.road([(x0, 0.0, z0), (x1, 0.0, z0), (x1, 0.0, z1), (x0, 0.0, z1)], "boards_ext")
    if along == "z":
        part.extend(board_run(x0, x1, -0.032, 0.0, z0, z1, rng, 0.17, 0.25, mat, vis=(1, 2), tag="en_board", gap=0.004))
    else:
        part.extend(_boards_x(x0, x1, z0, z1, rng, mat))
    part.add(box(x0, x1, -0.032, -0.004, z0, z1, mat, vis=(3,), tag="en_lod"))
    # edge beam (en-katsura) under the open edge, 1 cm in from it; posts on stones every half ken
    if edge in ("z0", "z1"):
        ze = z1 if edge == "z1" else z0
        sg = 1.0 if edge == "z1" else -1.0
        za, zb = sorted((ze - sg * 0.13, ze - sg * 0.012))
        part.add(box(x0, x1, -0.19, -0.032, za, zb, mat, vis=(1, 2, 3), tag="en_katsura", grain="long"))
        line = [(x, ze - sg * 0.07) for x in _stations(x0, x1, step, post_from)]
    else:
        xe = x1 if edge == "x1" else x0
        sg = 1.0 if edge == "x1" else -1.0
        xa, xb = sorted((xe - sg * 0.13, xe - sg * 0.012))
        part.add(box(xa, xb, -0.19, -0.032, z0, z1, mat, vis=(1, 2, 3), tag="en_katsura", grain="long"))
        line = [(xe - sg * 0.07, z) for z in _stations(z0, z1, step, post_from)]
    if posts:
        for (px, pz) in line:
            part.add(stone(rng, px, pz, 0.24, 0.22, 0.12, -drop + 0.07, "stone_field", bury=0.06, vis=(1, 2),
                           tag="en_stone"))
            part.add(box(px - 0.048, px + 0.048, -drop + 0.07, -0.19, pz - 0.048, pz + 0.048, mat, vis=(1, 2),
                         tag="en_tsuka", grain="long"))
        if drop > 0.6 and len(line) > 1:
            ym = -drop * 0.55
            (ax0, az0), (ax1, az1) = line[0], line[-1]
            if edge in ("z0", "z1"):
                part.add(box(min(ax0, ax1) - 0.06, max(ax0, ax1) + 0.06, ym, ym + 0.09, az0 - 0.017, az0 + 0.017,
                             mat, vis=(1,), tag="en_nuki"))
            else:
                part.add(box(ax0 - 0.017, ax0 + 0.017, ym, ym + 0.09, min(az0, az1) - 0.06, max(az0, az1) + 0.06,
                             mat, vis=(1,), tag="en_nuki"))
    if void:
        part.add(box(x0, x1, -drop, -0.19, z0 + 0.02, z0 + 0.035, "wood_sooted", vis=(1,), tag="dark_void"))


def _boards_x(x0, x1, z0, z1, rng, mat):
    out = []
    z = z0
    while z < z1 - 1e-3:
        e = min(z1, z + rng.uniform(0.17, 0.25))
        if z1 - e < 0.08:
            e = z1
        out.append(box(x0, x1, -0.032, 0.0, z + 0.002, e - 0.002, mat, vis=(1, 2), tag="en_board",
                       uvoff=(rng.random(), rng.random())))
        z = e
    return out


def _stations(a0, a1, step, first=None):
    """Post stations along a0..a1: one 0.07 in from each end (or from `first`, the 'first' end only) and evenly
    between them, no more than `step` apart."""
    s0 = a0 + 0.07 if first is None else first
    s1 = a1 - 0.07
    if s1 - s0 < 0.05:
        return [(s0 + s1) / 2]
    n = max(1, int(math.ceil((s1 - s0) / step - 1e-9)))
    return [s0 + (s1 - s0) * k / n for k in range(n + 1)]


# ------------------------------------------------------------------------------------------------ rail
def rail(part, p0, p1, style="plain", ends=("open", "open"), h=RAIL_H, mat=MAT, lift=0.0, geo=True, struts=HALF,
         post_h=0.92, collide_ends=True):
    """One koran run on the plan line p0 -> p1 (axis-aligned; the line is the rail centre). ends: per end
    'open' (stops square at the point: the next run continues), 'cross' (rails run out 0.10 past the point: a crossed
    corner), 'post' (an oyabashira centred ON the point, the rails end at its faces), 'stop' (ends 1 cm short: against
    a wall or screen). lift: raises the rails (a crossing run sits 1.5 cm higher so no two rails share a plane, C20).
    Returns the list of end-post tops."""
    axis, a0, a1, c = _ax(p0, p1)
    flip = (axis == "x" and p0[0] > p1[0]) or (axis == "z" and p0[1] > p1[1])
    e0, e1 = (ends[1], ends[0]) if flip else (ends[0], ends[1])
    tops = []
    ps = 0.05                                                  # half post size
    # the sill (jifuku) and the rails per end
    def span(ext_cross):
        lo = a0 - (ext_cross if e0 == "cross" else (-ps - 0.002 if e0 == "post" else (-0.01 if e0 == "stop" else 0.0)))
        hi = a1 + (ext_cross if e1 == "cross" else (-ps - 0.002 if e1 == "post" else (-0.01 if e1 == "stop" else 0.0)))
        return lo, hi
    jl, jh = span(0.0)
    if e0 == "cross":           # the first (unlifted) run's sill runs to the corner; a lifted run's stops at its face
        jl = a0 - JIF[1] / 2 + 0.004 if not lift else a0 + JIF[1] / 2 + 0.004
    if e1 == "cross":
        jh = a1 + JIF[1] / 2 - 0.004 if not lift else a1 - JIF[1] / 2 - 0.004
    part.add(_bx(axis, jl, jh, lift * 0.0, JIF[0] + lift, c - JIF[1] / 2, c + JIF[1] / 2, mat, vis=(1, 2, 3),
                 tag="jifuku", grain="long"))
    rl, rh = span(0.10)
    yh0, yh1 = 0.34 + lift, 0.40 + lift                        # hirageta
    part.add(_bx(axis, rl, rh, yh0, yh1, c - 0.028, c + 0.028, mat, vis=(1, 2), tag="hirageta", grain="long"))
    yk = h - 0.035 + lift                                      # hokogi centre
    pa = (rl, yk, c) if axis == "x" else (c, yk, rl)
    pb = (rh, yk, c) if axis == "x" else (c, yk, rh)
    part.add(tube(pa, pb, 0.035, mat, n=8, vis=(1, 2), tag="hokogi", grain="long"))
    part.add(_bx(axis, rl, rh, yk - 0.03, yk + 0.03, c - 0.03, c + 0.03, mat, vis=(3,), tag="hokogi_lod"))
    # struts: lower (jifuku -> hirageta) and upper (hirageta -> to block -> hokogi) at every half ken between the ends
    n = max(1, int(round((a1 - a0) / struts)))
    for k in range(n):
        s = a0 + (k + 0.5) * (a1 - a0) / n
        if (e0 == "post" and s < a0 + 0.12) or (e1 == "post" and s > a1 - 0.12):
            continue
        part.add(_bx(axis, s - 0.022, s + 0.022, JIF[0] + lift, yh0, c - 0.021, c + 0.021, mat, vis=(1,),
                     tag="koran_tsuka"))
        part.add(_bx(axis, s - 0.024, s + 0.024, yh1, yk - 0.075, c - 0.023, c + 0.023, mat, vis=(1,),
                     tag="totsuka"))
        part.add(_bx(axis, s - 0.045, s + 0.045, yk - 0.075, yk - 0.031, c - 0.036, c + 0.036, mat, vis=(1,),
                     tag="to_block"))
    for e, a in ((e0, a0), (e1, a1)):
        if e == "post":
            x, z = (a, c) if axis == "x" else (c, a)
            tops.append(end_post(part, x, z, 0.0, post_h + lift, style))
    if geo:
        gl, gh = span(0.0)
        if not collide_ends:
            gl, gh = a0 + 0.01, a1 - 0.01
        part.add(_bx(axis, gl, gh, 0.0, h + lift, c - 0.04, c + 0.04, mat, vis=(), geo=True, view=False, fire=None,
                     tag="koran_geo"))
    return tops


# ------------------------------------------------------------------------------------------------ stair
def stair_flight(drop, angle=STAIR_ANGLE, riser_max=0.21, grid=QK):
    run = drop / math.tan(math.radians(angle))
    run = math.ceil(run / grid - 1e-9) * grid
    n = max(2, int(math.ceil(drop / riser_max)))
    return run, n, drop / n, run / n


def kizahashi(part, xc, z_edge, drop=1.0, clear=STAIR_W, style="giboshi", mat=MAT, h=RAIL_H):
    """Wooden stair from the en edge (z_edge, y 0) down along +z to grade (y -drop), centred on x = xc, with side
    stringers, treads, a hidden walk ramp (Geometry + Roadway 'stair'), its own koran down to end posts at the foot
    and a foot stone. Returns dict(run, n, riser, going, angle, xa, xb (rail centrelines), foot z)."""
    run, n, rh, g = stair_flight(drop)
    zf = z_edge + run
    rw = 0.05                                                    # stair rail half width (the rail Geometry)
    xa, xb = xc - clear / 2 - rw, xc + clear / 2 + rw            # rail centrelines
    s0, s1 = xa - 0.03, xb + 0.03                                # stringer outer faces
    # hidden ramp (Geometry / View / Fire) + Roadway: from the en edge to the foot
    part.add(prism([(0.0, z_edge), (-drop, zf), (-drop, z_edge)], "x", xa + rw, xb - rw, mat, vis=(), geo=True,
                   view=True, fire="wood", tag="stair_ramp"))
    part.road([(xa + rw, 0.0, z_edge), (xb - rw, 0.0, z_edge), (xb - rw, -drop, zf), (xa + rw, -drop, zf)], "stair")
    rng = rng_for(part.name + "kizahashi")
    # stringers (gawa-geta): sloped boards along the flight, their top 0.12 over the tread line
    tl = math.atan2(drop, run)
    dv = 0.26 / math.cos(tl)
    for (x0, x1) in ((s0, s0 + 0.055), (s1 - 0.055, s1)):
        poly = [(0.0 + 0.12, z_edge), (0.12 - drop, zf), (-drop - dv + 0.12, zf), (-dv + 0.12, z_edge)]
        part.add(prism([(y, z) for y, z in poly], "x", x0, x1, mat, vis=(1, 2, 3), tag="stringer", grain="long"))
    # treads (fumi-ita) between the stringers, risers left open (period kizahashi have open risers on small halls)
    th = 0.04
    for k in range(1, n):
        top = -drop + k * rh
        za, zb = zf - k * g - 0.025, zf - (k - 1) * g
        part.add(box(s0 + 0.055, s1 - 0.055, top - th, top, za, zb, mat, vis=(1, 2), tag="stair_tread", grain="long",
                     uvoff=(rng.random(), rng.random())))
        for xx in (s0 - 0.008, s1):
            part.add(box(xx, xx + 0.008, top - th, top, za + 0.05, zb - 0.05, mat, vis=(1,), tag="tenon"))
    part.add(prism([(0.0, z_edge), (-drop, zf), (-drop, z_edge)], "x", s0 + 0.055, s1 - 0.055, mat, vis=(3,),
                   tag="stair_lod"))
    # stair koran: sloped hirageta + hokogi from the en gap posts (at z_edge) to the foot posts (zf - 0.10)
    zp = zf - 0.10
    yp = -drop + (zf - zp) / run * drop                          # ramp height at the foot posts
    for xr in (xa, xb):
        p_top = (xr, h, z_edge)
        p_bot = (xr, yp + h, zp)
        part.add(tube(p_top, p_bot, 0.035, mat, n=8, vis=(1, 2), tag="hokogi", grain="long"))
        part.add(tube((xr, 0.37, z_edge), (xr, yp + 0.37, zp), 0.03, mat, n=4, vis=(1,), tag="hirageta"))
        part.add(tube(p_top, p_bot, 0.035, mat, n=4, vis=(3,), tag="hokogi_lod"))
        # struts down to the stringer, every ~0.45 along the flight
        m = max(1, int(round(run / 0.45)))
        for k in range(1, m):
            z = z_edge + run * k / m
            yr = -drop * (z - z_edge) / run
            part.add(box(xr - 0.017, xr + 0.017, yr + 0.10, yr + h - 0.03, z - 0.019, z + 0.019, mat, vis=(1,),
                         tag="totsuka"))
        # one Geometry slab under the rail line (players do not step off the side of the flight)
        c = [(xr - rw, 0.0, z_edge), (xr + rw, 0.0, z_edge), (xr + rw, yp - 0.02, zp + 0.02), (xr - rw, yp - 0.02, zp + 0.02),
             (xr - rw, h, z_edge), (xr + rw, h, z_edge), (xr + rw, yp + h, zp + 0.02), (xr - rw, yp + h, zp + 0.02)]
        part.add(hexa(c, mat, vis=(), geo=True, view=False, fire=None, tag="koran_geo"))
        end_post(part, xr, zp, -drop, (yp + h + 0.17) + drop, style)
    # foot stone (visual: the terrain carries the foot)
    part.add(stone(rng, xc, zf + 0.30, clear + 0.25, 0.50, 0.08, -drop + 0.025, "stone_field", bury=0.05, n=10,
                   flat_top=0.85, vis=(1, 2, 3), tag="foot_stone"))
    return {"run": run, "n": n, "riser": rh, "going": g, "angle": math.degrees(math.atan(drop / run)), "xa": xa,
            "xb": xb, "foot": zf}


# ------------------------------------------------------------------------------------------------ screen
def wakishoji(part, x, z0, z1, top=2.05, mat=MAT, style="plain"):
    """Wakishoji: the board screen closing the rear end of a side en: a post at the en edge and a framed board panel
    across the en (plane x = const) from the wall face z0 to the edge post at z1; the side rail ends against it."""
    rng = rng_for(part.name + "waki%.2f" % x)
    zp = z1 - 0.07
    part.add(box(x - 0.055, x + 0.055, 0.0, top + 0.10, zp - 0.055, zp + 0.055, mat, vis=(1, 2, 3), geo=True,
                 view=True, fire=True, tag="waki_post", grain="long"))
    za, zb = z0 + 0.004, zp - 0.055
    part.add(box(x - 0.02, x + 0.02, 0.0, top, za, zb, mat, vis=(), geo=True, view=True, fire=True, tag="waki_geo"))
    part.extend(_vboards_z(x, za + 0.035, zb, 0.10, top - 0.08, rng, mat))
    for (y0, y1) in ((0.0, 0.10), (top - 0.08, top)):
        part.add(box(x - 0.03, x + 0.03, y0, y1, za, zb, mat, vis=(1, 2), tag="waki_rail", grain="long"))
    part.add(box(x - 0.03, x + 0.03, 0.10, top - 0.08, za, za + 0.06, mat, vis=(1, 2), tag="waki_stile"))
    part.add(box(x - 0.014, x + 0.014, 0.10, top - 0.08, za, zb, mat, vis=(3,), tag="waki_lod"))
    part.add(box(x - 0.06, x + 0.06, top + 0.10, top + 0.14, zp - 0.075, zp + 0.075, mat, vis=(1, 2), tag="post_cap"))


def _vboards_z(x, z0, z1, y0, y1, rng, mat):
    out = []
    z = z0
    while z < z1 - 1e-3:
        e = min(z1, z + rng.uniform(0.22, 0.30))
        if z1 - e < 0.10:
            e = z1
        out.append(box(x - 0.014, x + 0.014, y0, y1, z, e, mat, vis=(1, 2), tag="waki_board",
                       uvoff=(rng.random(), rng.random())))
        z = e
    return out


# ------------------------------------------------------------------------------------------------ whole en
def en_wrap(part, W, D, depth=DEPTH, drop=1.0, style="plain", sides=("front", "left", "right"), stair=None,
            waki=True, mat=MAT, waki_top=2.05):
    """The en round a W x D hall (front wall line z 0, x 0..W; back wall line z -D): front en over x -depth..W+depth
    (with both corner squares), side en from the front corner back to the rear wall line, kumi-koran on every open
    edge with crossed corners ('plain') or corner posts ('giboshi'), the stair gap and kizahashi at the front (stair =
    x centre), wakishoji at the rear ends of the side en. Returns dict(stair=..., rails=[...])."""
    zr = depth - EDGE_IN - JIF[1] / 2                          # rail centreline (front)
    out = {"rails": []}
    have_l, have_r = "left" in sides, "right" in sides
    fx0 = -depth if have_l else 0.0
    fx1 = W + depth if have_r else W
    if "front" in sides:
        en_deck(part, fx0, fx1, POST / 2, depth, drop, along="z", edge="z1", mat=mat,
                post_from=(fx0 + 0.07) if have_l else None)
    for side in ("left", "right"):
        if side not in sides:
            continue
        sg = -1.0 if side == "left" else 1.0
        xa, xb = sorted((sg * POST / 2 + (W if sg > 0 else 0.0), sg * depth + (W if sg > 0 else 0.0)))
        en_deck(part, xa, xb, -D, POST / 2 if "front" in sides else 0.0, drop, along="x",
                edge="x0" if sg < 0 else "x1", mat=mat)
    corner = "cross" if style == "plain" else "post"
    xl, xr_ = -zr, W + zr                                      # side rail centrelines
    end_back = "stop" if waki else "open"
    if "front" in sides:
        ends_l = corner if have_l else "stop"
        ends_r = corner if have_r else "stop"
        if stair is not None:
            K = kizahashi(part, stair, depth, drop, style=style, mat=mat)
            out["stair"] = K
            gl, gr = K["xa"], K["xb"]
            out["rails"].append(rail(part, (xl if have_l else fx0, zr), (gl, zr), style, (ends_l, "post")))
            out["rails"].append(rail(part, (gr, zr), (xr_ if have_r else fx1, zr), style, ("post", ends_r)))
        else:
            out["rails"].append(rail(part, (xl if have_l else fx0, zr), (xr_ if have_r else fx1, zr), style,
                                     (ends_l, ends_r)))
    zb = -D + 0.08 if waki else -D                              # the side rail stops at the screen
    for side, xc in (("left", xl), ("right", xr_)):
        if side not in sides:
            continue
        if "front" not in sides:
            out["rails"].append(rail(part, (xc, POST / 2), (xc, zb), style, ("stop", end_back)))
        elif style == "plain":
            out["rails"].append(rail(part, (xc, zr), (xc, zb), style, ("cross", end_back), lift=0.015))
        else:
            # the corner post belongs to the front run: the side run starts at its face
            out["rails"].append(rail(part, (xc, zr - 0.052), (xc, zb), style, ("open", end_back)))
        if waki:
            _waki_x(part, 0.0 if side == "left" else W, -1.0 if side == "left" else 1.0, depth, -D + 0.05,
                    waki_top, mat)
    return out


def _waki_x(part, xw, sg, depth, z, top, mat):
    """wakishoji across a side en (along x from the wall face to the en edge) in the plane z."""
    p = Part("waki", "", "")
    wakishoji(p, 0.0, POST / 2, depth, top=top, mat=mat)
    # wakishoji() draws in the plane x = 0 across z; turn it so it runs along x on the side of the hall
    deg = 90.0 if sg < 0 else -90.0                   # rot_y: +90 sends local +z to -x (the left side)
    q = p.transformed(deg, (xw, 0.0, z))
    part.merge(q)


# ------------------------------------------------------------------------------------------------ parts
VARIANTS = {
    "_plain": ("1-ken run of en (kirime-en, 1.365 deep, floor +1.00) with plain kumi-koran (jifuku, hirageta, struts "
               "with bearing blocks, round hokogi); chains with its neighbours (open ends)", [1, 2, 3]),
    "_giboshi": ("1-ken run of en with a giboshi koran: an octagonal end post with an onion finial (bronze in period; "
                 "iron stand-in) at its left end; chains with its neighbours", [2, 3]),
    "_corner_plain": ("outer corner of the en: corner deck square, the koran runs cross and run out 0.10 past the "
                      "corner (straight; the hane up-turn is a W2P2 curve)", [1, 2, 3]),
    "_corner_giboshi": ("outer corner of the en with a giboshi corner post; both runs end at its faces", [2, 3]),
    "_kizahashi": ("1-ken front run with the kizahashi: the koran gap ends in giboshi posts, the stair (hidden walk "
                   "ramp <= 38 deg, 1.10 clear between its rails) runs down to giboshi foot posts and a foot stone",
                   [2, 3]),
    "_kizahashi_plain": ("the same stair with plain cut-top posts (village shrines / halls without bronze)", [1, 2, 3]),
    "_wakishoji": ("1-ken run of a side en ending in the wakishoji board screen (the rear end of a honden's side en)",
                   [1, 2, 3]),
}


def part_koran(variant):
    used, tiers = VARIANTS[variant]
    p = Part("jp_p_porch_koran", variant, "porch", tiers=tiers, used_for=used,
             recipe="koran.en_wrap(part, W, D, depth, drop, style, stair=x) for a whole hall; koran.en_deck / rail / "
                    "kizahashi / wakishoji for pieces",
             datum="run along +x on a wall whose centreline is z 0; en deck z 0.06 .. 1.365 (edge); y 0 = en floor = "
                   "hall floor (+1.00 above grade)")
    drop = 1.0
    zr = DEPTH - EDGE_IN - JIF[1] / 2
    style = "giboshi" if "giboshi" in variant or variant == "_kizahashi" else "plain"
    if variant in ("_plain", "_giboshi"):
        en_deck(p, 0.0, KEN, POST / 2, DEPTH, drop)
        rail(p, (0.0, zr), (KEN, zr), style, ("post" if variant == "_giboshi" else "open", "open"))
        for x in (0.0, KEN):
            p.conn("post", (x, 0, 0), note="hall wall post")
    elif variant.startswith("_corner"):
        # building corner post at the origin: the front wall runs along x <= 0, the side wall along z <= 0
        en_deck(p, -0.0, DEPTH, POST / 2, DEPTH, drop, edge="z1", post_from=DEPTH - 0.07)
        en_deck(p, POST / 2, DEPTH, -0.0, POST / 2, drop, along="x", edge="x1", posts=False)
        corner = "cross" if style == "plain" else "post"
        rail(p, (0.0, zr), (zr, zr), style, ("open", corner))
        if style == "plain":
            rail(p, (zr, zr), (zr, 0.0), style, ("cross", "open"), lift=0.015)
        else:
            rail(p, (zr, zr - 0.052), (zr, 0.0), style, ("open", "open"))
        p.conn("post", (0, 0, 0), note="hall corner post")
    elif variant.startswith("_kizahashi"):
        en_deck(p, 0.0, KEN, POST / 2, DEPTH, drop)
        K = kizahashi(p, HALF, DEPTH, drop, style=style)
        rail(p, (0.0, zr), (K["xa"], zr), style, ("open", "post"))
        rail(p, (K["xb"], zr), (KEN, zr), style, ("post", "open"))
        p.conn("post", (0, 0, 0))
        p.conn("post", (KEN, 0, 0))
        p.conn("stair_head", (HALF, 0, DEPTH), note="top of the walk ramp at the en edge")
        p.conn("stair_foot", (HALF, -drop, K["foot"]), note="foot of the walk ramp at grade")
        p.dim("ramp_deg", "<=38", round(K["angle"], 2), tol=0.0, source="PLAYBOOK D4")
        p.dims[-1]["ok"] = K["angle"] <= 38.0 + 1e-6
        clear = (K["xb"] - 0.05) - (K["xa"] + 0.05)
        p.dim("stair_clear_m", ">=1.10", round(clear, 3), source="PLAYBOOK D4")
        p.dims[-1]["ok"] = clear >= 1.10 - 1e-6
        p.dim("riser_m", "0.18-0.22 (A)", round(K["riser"], 3))
        p.dims[-1]["ok"] = 0.15 <= K["riser"] <= 0.22
        p.meta["flight"] = {k: round(v, 4) if isinstance(v, float) else v for k, v in K.items()}
    elif variant == "_wakishoji":
        en_deck(p, 0.0, KEN + 0.12, POST / 2, DEPTH, drop)
        rail(p, (0.0, zr), (KEN, zr), style, ("open", "stop"))
        p2 = Part("waki", "", "")
        wakishoji(p2, 0.0, POST / 2, DEPTH)
        p.merge(p2.transformed(0.0, (KEN + 0.06, 0.0, 0.0)))
        p.conn("post", (0, 0, 0))
        p.conn("post", (KEN, 0, 0), note="the hall's rear corner post (the screen stands just past it)")
    p.conn("floor", (0, 0, 0), note="en floor = hall floor level")
    p.conn("grade", (0, -drop, 0))
    clear = zr - JIF[1] / 2 - POST / 2
    p.dim("en_clear_m", ">=1.00", round(clear, 3), source="PLAYBOOK D5 (engawa and corridors)")
    p.dims[-1]["ok"] = clear >= 1.0
    p.dim("rail_top_m", RAIL_H, RAIL_H)
    return p


def register(reg):
    reg("jp_p_porch_koran", list(VARIANTS), part_koran)
