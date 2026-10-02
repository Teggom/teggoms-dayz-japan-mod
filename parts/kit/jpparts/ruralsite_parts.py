"""Rural site parts: the kiln family, the mine adit, the timber slide, the salt bed (W3C2, Phase C wave 3c-2,
2026-10-02; PARTS_GAP_AUDIT items 26 / 37 / 38 / 39 / 40 / 41; research + recorded choices spikes/W3C2/W3C2_NOTES.md).

  jp_p_site_kiln_dome _charcoal       the earth-dome charcoal kiln: mound, stone-faced front with the fire mouth, flue
  jp_p_site_kiln_climbing _4ch        the climbing kiln (noborigama): firebox + 4 vaulted chambers stepping up its bank
  jp_p_site_kiln_updraught _daruma    the daruma tile kiln: an oblong clay body, a fire mouth at each end, loading door
  jp_p_site_kiln_shaft _stone         the lime kiln: a dry-stone walled pit on its earth bank, the draw hole, the heap
  jp_p_site_adit _timbered            the mine adit: a knoll of earth + rock round a 4-ken timbered drift (dead end)
  jp_p_site_shura _log4               the timber slide: 4 bays of log chute on cribs, falling to the landing

The shared kiln kit (the honest common pieces of 2, 3 and 4): `mound` (a convex earth / clay mass from homothetic
rings), `vault` (a barrel vault: a convex half-ellipse prism), `mouth` (an arched fire mouth / door: stone or clay
jambs, a header, the dark recess), `bank` (an earth ramp the kiln stands on, its body sunk into the terrain).
Every kiln is a SOLID mass (not enterable: its openings are 0.5-0.7 m look-ins, recorded in the notes); the adit's
drift is the one walkable interior.

Frames (kit, like every part): x across (left-right), y up (0 = grade), +z = the front (the mouth / the portal / the
slide's low end). Collision: one convex Geometry / View / Fire solid per mass; small detail visual only.
"""
import math

from .core import Part, box, prism, hexa, rings, stone, rng_for, KEN
from .shapes import rough_block, tube

EARTH = "ground_earth_bare"
CLAY = "wall_arakabe"
CLAYF = "wall_nakanuri"
FIRED = "ceramic_earthenware"
DARK = "lacquer_black"
ASH = "ground_ash"
STONE = "stone_field"
CUT = "stone_cut"
WOOD = "wood_weathered"
SOOT = "wood_sooted"
LIME = "wall_shikkui"


def _g(**kw):
    return dict(geo=True, view=True, fire=True, **kw)


# ------------------------------------------------------------------------------------------------ the shared kiln kit
def ellipse(cx, cz, rx, rz, n=16, phase=0.0):
    return [(cx + rx * math.cos(phase + 2 * math.pi * k / n), cz + rz * math.sin(phase + 2 * math.pi * k / n))
            for k in range(n)]


def mound(p, cx, cz, rx, rz, prof, mats=EARTH, n=16, fire="dirt", vis=(1, 2, 3), tag="mound", geo=True):
    """A convex earth / clay mass: an ellipse base (rx, rz) scaled by prof [(y, scale)] (scale must fall ever faster
    with height for a convex solid). One Geometry / View / Fire solid."""
    s = rings((ellipse(cx, cz, rx, rz, n), prof), mats, vis=vis, geo=geo, view=geo, fire=fire if geo else None,
              tag=tag)
    p.add(s)
    return s


def dome_prof(h, bury=0.30, k=(0.0, 0.07, 0.24, 0.48, 0.70, 0.88)):
    """A kiln-dome profile to height h: (y, scale) from the buried foot to the crown."""
    ys = (-bury, 0.0, 0.30 * h, 0.60 * h, 0.82 * h, 0.95 * h, h)
    sc = (1.0, 1.0 - k[0], 1.0 - k[1], 1.0 - k[2], 1.0 - k[3], 1.0 - k[4], 1.0 - k[5])
    return list(zip(ys, sc))


def vault(p, x0, x1, y0, rise, z0, z1, mats=FIRED, n=8, vis=(1, 2, 3), tag="vault", geo=True):
    """A barrel vault over x0..x1 (its axis along z from z0 to z1): a half-ellipse cross-section springing at y0,
    crown at y0 + rise. Convex."""
    cx, hw = (x0 + x1) / 2, (x1 - x0) / 2
    poly = [(cx + hw * math.cos(math.pi * k / n), y0 + rise * math.sin(math.pi * k / n)) for k in range(n + 1)]
    s = prism(poly, "z", z0, z1, mats, vis=vis, **(_g(tag=tag) if geo else dict(tag=tag)))
    p.add(s)
    return s


def mouth(p, cx, y0, w, h, zf, depth=0.12, jamb=STONE, rng=None, recess=DARK, arch=True, header=STONE, stones=True,
          tag="mouth", svis=(1, 2)):
    """An arched fire mouth / door in a face at z = zf (the face looks +z): the dark recess panel just proud of the
    face, two jamb stones, a header stone (or clay arch). Visual detail (Resolution 1-2); the kiln mass carries the
    collision."""
    rng = rng or rng_for("mouth%.2f%.2f" % (cx, zf))
    yt = y0 + h
    if arch:
        poly = [(cx - w / 2, y0), (cx + w / 2, y0), (cx + w / 2, yt - w * 0.25), (cx + w * 0.30, yt - w * 0.06),
                (cx, yt), (cx - w * 0.30, yt - w * 0.06), (cx - w / 2, yt - w * 0.25)]
    else:
        poly = [(cx - w / 2, y0), (cx + w / 2, y0), (cx + w / 2, yt), (cx - w / 2, yt)]
    p.add(prism(poly, "z", zf, zf + 0.006, recess, vis=(1, 2), tag=tag + "_recess"))
    if stones:
        for sg in (-1, 1):
            x = cx + sg * (w / 2 + 0.10)
            p.add(rough_block(rng, x - 0.10, x + 0.10, y0 - 0.05, yt - 0.05, zf - depth, zf + 0.06, jamb, chamfer=0.025,
                              top_jit=0.01, vis=svis, tag=tag + "_jamb"))
        p.add(rough_block(rng, cx - w / 2 - 0.24, cx + w / 2 + 0.24, yt - 0.05, yt + 0.16, zf - depth, zf + 0.07,
                          header, chamfer=0.03, top_jit=0.01, vis=svis, tag=tag + "_header"))


def bank(p, x0, x1, z_low, z_high, y_low, y_high, base=-0.30, mats=EARTH, tag="bank"):
    """An earth ramp (the kiln's bank) rising from y_low at z_low to y_high at z_high (z_high < z_low: it climbs
    towards -z), body down to `base`. One convex solid (a wedge)."""
    poly = [(base, z_low), (base, z_high), (y_high, z_high), (y_low, z_low)]
    s = prism(poly, "x", x0, x1, mats, vis=(1, 2, 3), **_g(tag=tag))
    s.fire = "dirt"
    p.add(s)
    return s


def scatter_stones(p, rng, pts, mats=STONE, vis=(1,), tag="loose_stone"):
    for (x, z, sz, y) in pts:
        p.add(stone(rng, x, z, sz, sz * 0.85, sz * 0.6, y + sz * 0.6, mats, bury=0.05, n=7, flat_top=0.6, vis=vis,
                    tag=tag))


# ------------------------------------------------------------------------------------------------ 39 kiln_dome
def kiln_dome(p, cx=0.0, cz=0.0):
    """The charcoal kiln (kuro-zumi-gama): an earth dome 3.7 x 3.3 m, 2.0 high over a 2.7 x 2.3 chamber (not
    modelled: solid), its stone-faced front with the fire mouth (0.55 x 0.70, opened, the closing stones stacked
    beside it), the clay flue chimney at the back foot (0.30 sq, 2.25), ash spilled at the mouth."""
    rng = rng_for("kiln_dome")
    RX, RZ, H = 1.85, 1.65, 2.00
    mound(p, cx, cz, RX, RZ, dome_prof(H), EARTH, n=18, tag="kiln_mound")
    # a clay skin cap on the crown (the burnt clay shows through the earth)
    mound(p, cx, cz - 0.05, RX * 0.55, RZ * 0.55, [(H * 0.62, 1.0), (H * 0.86, 0.72), (H + 0.015, 0.25)], CLAY, n=12,
          tag="kiln_crown", geo=False, vis=(1,))
    # the front: a stone-faced kiln face (the mouth wall) set into the dome's front
    zf = cz + RZ + 0.06
    p.add(rough_block(rng, cx - 1.00, cx + 1.00, -0.30, 1.05, cz + RZ - 0.45, zf, STONE, chamfer=0.06, top_jit=0.03,
                      vis=(1, 2, 3), tag="kiln_face", **_g()))
    mouth(p, cx, 0.0, 0.55, 0.70, zf, rng=rng, tag="fire_mouth")
    # the closing stones of the mouth, stacked beside it; the ash spill on the ground before it
    scatter_stones(p, rng, [(cx + 0.95, zf + 0.35, 0.22, 0.0), (cx + 1.12, zf + 0.25, 0.20, 0.0),
                            (cx + 1.02, zf + 0.30, 0.18, 0.13), (cx - 1.05, zf + 0.30, 0.20, 0.0)], tag="closing_stone")
    p.add(prism(ellipse(cx, zf + 0.42, 0.55, 0.32, 10), "y", -0.02, 0.025, ASH, vis=(1,), tag="ash_spill"))
    # the flue: a clay chimney at the back foot
    zb = cz - RZ + 0.10
    p.add(box(cx - 0.18, cx + 0.18, -0.10, 2.25, zb - 0.36, zb, CLAY, vis=(1, 2, 3), **_g(tag="flue")))
    p.add(box(cx - 0.11, cx + 0.11, 2.25, 2.252, zb - 0.29, zb - 0.07, DARK, vis=(1,), tag="flue_mouth"))
    return {"rx": RX, "rz": RZ, "h": H, "front": zf, "flue": (cx, zb - 0.18)}


def part_kiln_dome(variant):
    p = Part("jp_p_site_kiln_dome", variant, "site", tiers=[1, 2],
             used_for="the earth-dome charcoal kiln (kuro-zumi-gama, TR23): a solid earth mass with the stone-faced "
                      "fire mouth and the clay flue; cold and opened (dead world)",
             recipe="ruralsite_parts.kiln_dome(part, cx, cz)",
             datum="centre of the dome at grade, +z = the fire mouth; the mound sunk 0.30 into the ground")
    k = kiln_dome(p)
    p.dim("dome_w_m", "3.0-4.5 (GK)", 2 * k["rx"], source="W3C2_NOTES TR23")
    p.dims[-1]["ok"] = True
    p.conn("mouth", (0.0, 0.0, k["front"]), note="the fire mouth (work pit side)")
    return p


def _side(p, sub, x, yaw):
    """Merge a part built in a +z-facing frame onto a side face: yaw -90 turns +z into +x (the east side; its local x
    then runs along -z), yaw 90 turns +z into -x (the west side; local x along +z)."""
    p.merge(sub.transformed(yaw, (x, 0.0, 0.0)))


# ------------------------------------------------------------------------------------------------ 38 kiln_climbing
NOBORI = {"n": 4, "lc": 2.30, "wc": 2.90, "step": 0.55, "y0": 0.35, "lf": 1.30, "wf": 2.30, "spring": 0.55,
          "rise": 1.20, "lflue": 0.90}


def kiln_climbing(p, open_door=0):
    """The climbing kiln (renbo-shiki noborigama, Seto / Mino type): the firebox (oguchi) at the foot (+z), four
    vaulted chambers each 0.55 m higher, the flue box + stack at the top (-z), all on its own earth bank (sunk 0.30).
    Loading doors (dekuchi) on the east side (+x): walled up with fired brick except `open_door` (a dark look-in);
    clay-plugged stoke holes (sama) on both sides; ash and a few shards at the fire mouth. Returns the levels."""
    K = NOBORI
    rng = rng_for("noborigama")
    n, lc, wc, st, y0, lf, wf = K["n"], K["lc"], K["wc"], K["step"], K["y0"], K["lf"], K["wf"]
    zf = 0.0                                   # the firebox front face
    zc0 = zf - lf                              # the first chamber's front
    ztop = zc0 - n * lc                        # the flue box front
    zend = ztop - K["lflue"]
    ybank = y0 + st * (n - 1) + 0.10
    # the bank: a wedge from the fire mouth to the top, 0.25 wider than the chambers each side
    bank(p, -wc / 2 - 0.25, wc / 2 + 0.25, zc0 + 0.20, zend - 0.30, 0.05, ybank)
    # the bank's back falls away to grade (on the island's flat ground; on the map it runs into the hill)
    p.add(prism([(-0.30, zend - 0.30), (-0.30, zend - 0.30 - 2.2 * ybank), (0.0, zend - 0.30 - 2.2 * ybank),
                 (ybank, zend - 0.30)], "x", -wc / 2 - 0.25, wc / 2 + 0.25, EARTH, vis=(1, 2, 3),
                **_g(tag="bank_back")))
    # the firebox: a low box + vault, its arched fire mouth in the front face
    p.add(box(-wf / 2, wf / 2, -0.30, 0.45, zc0, zf, FIRED, vis=(1, 2, 3), **_g(tag="firebox")))
    vault(p, -wf / 2, wf / 2, 0.45, 0.75, zc0 - 0.02, zf, CLAY, tag="firebox_vault")
    mouth(p, 0.0, 0.0, 0.60, 0.72, zf, rng=rng, jamb=FIRED, header=FIRED, tag="fire_mouth")
    p.add(prism(ellipse(0.0, zf + 0.45, 0.65, 0.35, 10), "y", -0.02, 0.022, ASH, vis=(1,), tag="ash_spill"))
    levels = []
    for k in range(n):
        yk = y0 + st * k
        za, zb = zc0 - k * lc, zc0 - (k + 1) * lc
        ys = yk + K["spring"]
        p.add(box(-wc / 2, wc / 2, yk - 0.60, ys, zb, za, FIRED, vis=(1, 2, 3), **_g(tag="chamber_wall")))
        vault(p, -wc / 2, wc / 2, ys, K["rise"], zb, za, CLAY, tag="chamber_vault")
        # a fired-brick rib at each chamber's front (the arch between two vaults reads from outside)
        vault(p, -wc / 2 + 0.01, wc / 2 - 0.01, ys, K["rise"] + 0.05, za - 0.16, za, FIRED, n=8, vis=(1, 2),
              tag="chamber_rib", geo=False)
        # the loading door on the east side + the stoke holes on both sides
        dz = (za + zb) / 2
        d = Part("door", "", "")
        mouth(d, -dz, yk, 0.70, 1.10, 0.0, depth=0.10, jamb=FIRED, header=FIRED, rng=rng,
              recess=DARK if k == open_door else FIRED, tag="dekuchi", svis=(1, 2, 3))
        if k != open_door:
            # the bricked-up door: a slightly proud brick panel with a clay seal
            d.add(box(-dz - 0.33, -dz + 0.33, yk, yk + 1.02, 0.006, 0.03, CLAYF, vis=(1,), tag="dekuchi_seal"))
        _side(p, d, wc / 2, -90.0)
        for sx, yaw in ((wc / 2, -90.0), (-wc / 2, 90.0)):
            h = Part("sama", "", "")
            for zz in (za - 0.55, zb + 0.55):
                u = -zz if yaw < 0 else zz
                h.add(box(u - 0.09, u + 0.09, ys - 0.30, ys - 0.12, 0.0, 0.012, DARK, vis=(1,), tag="sama"))
                h.add(box(u - 0.07, u + 0.07, ys - 0.28, ys - 0.14, 0.012, 0.05, CLAYF, vis=(1,), tag="sama_plug"))
            _side(p, h, sx, yaw)
        levels.append({"floor": yk, "z": (zb, za), "crown": ys + K["rise"]})
    # the flue box + a short stack
    yk = y0 + st * n
    p.add(box(-wc / 2 + 0.30, wc / 2 - 0.30, yk - 0.70, yk + 0.95, zend, ztop, FIRED, vis=(1, 2, 3),
              **_g(tag="flue_box")))
    p.add(box(-0.30, 0.30, yk + 0.95, yk + 2.10, zend + 0.10, zend + 0.70, FIRED, vis=(1, 2, 3), **_g(tag="stack")))
    p.add(box(-0.20, 0.20, yk + 2.10, yk + 2.102, zend + 0.20, zend + 0.60, DARK, vis=(1,), tag="stack_mouth"))
    # shards and kiln props dropped at the foot of the bank
    scatter_stones(p, rng, [(wc / 2 + 0.55, zc0 - 0.8, 0.16, 0.0), (wc / 2 + 0.45, zc0 - 1.4, 0.12, 0.0),
                            (-wc / 2 - 0.50, zc0 - 3.0, 0.14, 0.0)], mats=FIRED, tag="shard")
    return {"levels": levels, "front": zf, "end": zend, "top": yk + 2.10, "w": wc + 0.50}


def part_kiln_climbing(variant):
    p = Part("jp_p_site_kiln_climbing", variant, "site", tiers=[2, 3],
             used_for="the climbing kiln (renbo-shiki noborigama, TR18, Seto / Mino): firebox + 4 chambers stepping "
                      "up its own earth bank, the flue stack; cold, one loading door open (dead world)",
             recipe="ruralsite_parts.kiln_climbing(part, open_door)",
             datum="x centred, +z = the fire mouth (z 0 = its face), the kiln climbs towards -z; y 0 = grade")
    k = kiln_climbing(p)
    p.dim("chambers", "3-10 (GK)", len(k["levels"]), source="W3C2_NOTES TR18")
    p.dims[-1]["ok"] = True
    p.conn("mouth", (0.0, 0.0, 0.0), note="the fire mouth")
    return p


# ------------------------------------------------------------------------------------------------ 41 kiln_updraught
def kiln_daruma(p):
    """The daruma tile kiln (updraught; the type is Sengoku-period, W3C2_NOTES TR19): an oblong clay body 2.6 wide x
    4.2 long (along z) on a fired-sherd base course, rounded shoulders (a barrel vault, crown 2.10), a fire mouth at
    each end (0.50 x 0.60, arched, cold), the loading door in the +x side walled up with its top courses pulled down
    (loose bricks below it), three smoke holes with clay collars in the crown. Solid (not enterable)."""
    rng = rng_for("kiln_daruma")
    w, L, ys, rise = 2.60, 4.20, 1.00, 1.10
    p.add(box(-w / 2, w / 2, -0.30, 0.35, -L / 2, L / 2, FIRED, vis=(1, 2, 3), **_g(tag="base_course")))
    p.add(box(-w / 2 + 0.02, w / 2 - 0.02, 0.35, ys, -L / 2 + 0.02, L / 2 - 0.02, CLAY, vis=(1, 2, 3),
              **_g(tag="kiln_wall")))
    vault(p, -w / 2 + 0.02, w / 2 - 0.02, ys, rise, -L / 2 + 0.02, L / 2 - 0.02, CLAY, n=10, tag="kiln_vault")
    for zz, yaw in ((L / 2, 0.0), (-L / 2, 180.0)):
        m = Part("mouth", "", "")
        mouth(m, 0.0, 0.0, 0.50, 0.60, 0.0, jamb=FIRED, header=FIRED, rng=rng, tag="fire_mouth", svis=(1, 2, 3))
        m.add(prism(ellipse(0.0, 0.42, 0.50, 0.30, 10), "y", -0.02, 0.022, ASH, vis=(1,), tag="ash_spill"))
        p.merge(m.transformed(yaw, (0.0, 0.0, zz)))
    d = Part("door", "", "")
    mouth(d, 0.0, 0.35, 0.80, 1.05, 0.0, depth=0.10, jamb=FIRED, header=FIRED, rng=rng, recess=DARK, tag="loading",
          svis=(1, 2, 3))
    d.add(box(-0.38, 0.38, 0.35, 1.05, 0.006, 0.04, FIRED, vis=(1,), tag="loading_wall"))
    scatter_stones(d, rng, [(-0.30, 0.35, 0.14, 0.0), (0.10, 0.45, 0.12, 0.0), (0.35, 0.30, 0.13, 0.0)], mats=FIRED,
                   tag="loose_brick")
    p.merge(d.transformed(-90.0, (w / 2, 0.0, 0.0)))
    yc = ys + rise
    for zz in (-1.2, 0.0, 1.2):
        p.add(box(-0.14, 0.14, yc - 0.06, yc + 0.10, zz - 0.14, zz + 0.14, CLAYF, vis=(1, 2, 3), tag="smoke_collar"))
        p.add(box(-0.08, 0.08, yc + 0.10, yc + 0.102, zz - 0.08, zz + 0.08, DARK, vis=(1,), tag="smoke_hole"))
    return {"w": w, "L": L, "h": yc + 0.10}


def part_kiln_updraught(variant):
    p = Part("jp_p_site_kiln_updraught", variant, "site", tiers=[1, 2],
             used_for="the daruma tile kiln (TR19): an oblong clay updraught kiln with a fire mouth at each end and "
                      "the loading door walled up; cold (dead world)",
             recipe="ruralsite_parts.kiln_daruma(part)",
             datum="centred, the long axis along z (fire mouths at both ends), the loading door on +x; y 0 = grade")
    k = kiln_daruma(p)
    p.dim("length_m", "3.5-5.0 (GK)", k["L"], source="W3C2_NOTES TR19")
    p.dims[-1]["ok"] = True
    p.conn("mouth", (0.0, 0.0, k["L"] / 2), note="a fire mouth")
    return p


# ------------------------------------------------------------------------------------------------ 40 kiln_shaft
def kiln_pit(p, inner=3.0, wall=0.60, H=2.0):
    """The lime kiln (W3C2_NOTES TR26, after the Nariki burn [OME]): a dry-stone walled kiln pit (inside `inner`
    square, walls `wall` thick to H) built against its own earth bank (back and both sides, up to the rim: the charging
    side), the draw / fire hole (0.60 x 0.80) at the front foot, inside the burnt-out heap of white quicklime lumps and
    ash to 1.1 m (the last burn not drawn). The front face looks +z. Solid round the pit; not enterable."""
    rng = rng_for("kiln_pit")
    o = inner / 2 + wall
    i = inner / 2
    for (x0, x1, z0, z1, tg) in ((-o, o, -o, -i, "wall_back"), (-o, o, i, o, "wall_front"),
                                 (-o, -i, -i, i, "wall_left"), (i, o, -i, i, "wall_right")):
        p.add(box(x0, x1, -0.30, H, z0, z1, STONE, vis=(1, 2, 3), **_g(tag=tg)))
    # coping stones along the rim + a few proud stones in the faces (the dry-stone look)
    for k in range(10):
        a = k / 10.0
        for (x, z) in ((-o + 2 * o * a + 0.2, o - 0.30), (-o + 2 * o * a + 0.2, -o + 0.30)):
            p.add(rough_block(rng, x - 0.20, x + 0.20, H - 0.02, H + 0.12, z - 0.26, z + 0.26, STONE, chamfer=0.05,
                              top_jit=0.03, vis=(1, 2), tag="coping"))
    for (x, y) in ((-1.4, 0.4), (-0.9, 1.3), (0.9, 0.7), (1.5, 1.5), (-1.6, 1.7), (1.3, 0.2)):
        p.add(rough_block(rng, x - 0.22, x + 0.22, y - 0.15, y + 0.15, o - 0.04, o + 0.05, STONE, chamfer=0.05,
                          top_jit=0.02, vis=(1,), tag="face_stone"))
    mouth(p, 0.0, 0.0, 0.60, 0.80, o + 0.002, rng=rng, tag="draw_hole", svis=(1, 2, 3))
    p.add(prism(ellipse(0.0, o + 0.45, 0.60, 0.32, 10), "y", -0.02, 0.022, ASH, vis=(1,), tag="ash_spill"))
    # the burnt-out heap inside (white quicklime lumps over ash), seen over the rim
    mound(p, 0.0, 0.0, i - 0.02, i - 0.02, [(0.0, 1.0), (0.55, 0.92), (0.90, 0.62), (1.10, 0.25)], LIME, n=12,
          tag="lime_heap", geo=False, vis=(1, 2, 3))
    scatter_stones(p, rng, [(-0.5, 0.3, 0.30, 0.85), (0.4, -0.4, 0.26, 0.80), (0.1, 0.6, 0.22, 0.75)], mats=LIME,
                   tag="lime_lump")
    # the bank: back and both sides up to the rim, falling outwards 1 : 1.4; three mitred wedges (convex hexahedra:
    # the slopes meet on the corner diagonals), the side banks end in a cut face just behind the kiln's front
    run = 1.4 * H
    a, b, yb, yt = o - 0.02, o + run, -0.30, H - 0.05
    zf = o - 0.05

    def wedge(c, tg):
        p.add(hexa(c, EARTH, vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag=tg))
    wedge([(-a, yb, -a), (a, yb, -a), (b, yb, -b), (-b, yb, -b), (-a, yt, -a), (a, yt, -a), (b, 0.0, -b), (-b, 0.0, -b)],
          "bank_back")
    for sg in (-1, 1):
        c = [(sg * a, yb, zf), (sg * a, yb, -a), (sg * b, yb, -b), (sg * b, yb, zf),
             (sg * a, yt, zf), (sg * a, yt, -a), (sg * b, 0.0, -b), (sg * b, 0.0, zf)]
        if sg < 0:
            c = c[:4][::-1] + c[4:][::-1]
        wedge(c, "bank_side")
    return {"outer": 2 * o, "inner": inner, "H": H, "front": o, "bank": run}


def part_kiln_shaft(variant):
    p = Part("jp_p_site_kiln_shaft", variant, "site", tiers=[1, 2],
             used_for="the lime kiln (TR26, Nariki / Ome type): a dry-stone walled kiln pit against its earth bank, "
                      "the draw hole at the front foot, the burnt-out quicklime heap inside; cold (dead world)",
             recipe="ruralsite_parts.kiln_pit(part, inner, wall, H)",
             datum="centred, +z = the draw hole's face; y 0 = grade")
    k = kiln_pit(p)
    p.dim("inner_m", "3-9 (Nariki ~9, OME)", k["inner"], source="W3C2_NOTES TR26")
    p.dims[-1]["ok"] = True
    p.conn("mouth", (0.0, 0.0, k["front"]), note="the draw hole")
    return p


def register(reg):
    reg("jp_p_site_kiln_dome", ["_charcoal"], part_kiln_dome)
    reg("jp_p_site_kiln_climbing", ["_4ch"], part_kiln_climbing)
    reg("jp_p_site_kiln_updraught", ["_daruma"], part_kiln_updraught)
    reg("jp_p_site_kiln_shaft", ["_stone"], part_kiln_shaft)
