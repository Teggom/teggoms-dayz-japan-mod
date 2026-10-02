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

from .core import Part, box, prism, hexa, rings, stone, rng_for, KEN, Solid
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
# FX7 (2026-10-02, Stephen's 3c-2 walk: the banks / knoll / quarry read as beige blobs): real rock and soil
BANK = "ground_earth_bank"           # an old soil bank, dry autumn grass + leaves (research/materials/make_fx7_materials)
OUTCROP = "stone_outcrop"            # natural weathered rock, lichen
QFACE = "stone_quarry_face"          # a split quarry face: bedding joints, wedge-hole channels, tool marks


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


def hull_solid(pts, mats, eps=1e-6, **kw):
    """FX7: the convex hull of a few points (<= ~12) as one Solid, coplanar faces merged (n-gons; Solid fans them)."""
    import itertools
    P = [tuple(float(c) for c in p) for p in pts]
    n = len(P)

    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    faces, seen = [], set()
    for i, j, k in itertools.combinations(range(n), 3):
        nn = cross(sub(P[j], P[i]), sub(P[k], P[i]))
        L = dot(nn, nn) ** 0.5
        if L < 1e-9:
            continue
        nn = (nn[0] / L, nn[1] / L, nn[2] / L)
        d = [dot(nn, sub(q, P[i])) for q in P]
        if max(d) > 1e-5 and min(d) < -1e-5:
            continue
        on = frozenset(m for m in range(n) if abs(d[m]) <= 1e-5)
        if on in seen:
            continue
        seen.add(on)
        c = tuple(sum(P[m][a] for m in on) / len(on) for a in range(3))
        u = sub(P[i], c)
        ul = dot(u, u) ** 0.5 or 1.0
        u = (u[0] / ul, u[1] / ul, u[2] / ul)
        v = cross(nn, u)
        import math as _m
        faces.append(sorted(on, key=lambda m: _m.atan2(dot(sub(P[m], c), v), dot(sub(P[m], c), u))))
    return Solid(P, faces, mats, **kw)


def apron(p, x0, x1, z0, z1, h, sides, k=1.6, toe_h=0.35, toe_k=3.4, base=-0.20, inset=0.30, mats=BANK,
          tag="apron"):
    """FX7: an earth apron round the rectangle (x0..x1, z0..z1) of a mass sitting on flat ground: on each side in
    `sides` ('back' -z, 'front' +z, 'left' -x, 'right' +x) a hipped slope from `h` (its top edge `inset` inside the
    rectangle, hidden in the mass) down to `base` under grade at a run of k per metre of rise, and a gentler toe
    (toe_h, toe_k) beyond it, so the mass's foot feathers into the terrain instead of meeting it with a hard edge.
    Each piece one convex solid (Geometry / View / Fire 'dirt'); slopes <= ~32 deg (walkable)."""
    out = []
    for (hh, kk, nm) in ((h, k, ""), (toe_h, toe_k, "_toe")):
        if hh <= base + 0.05:
            continue
        r = kk * (hh - base)
        for sd in sides:
            if sd in ("back", "front"):
                zi = z0 + inset if sd == "back" else z1 - inset
                ze = z0 if sd == "back" else z1
                zo = ze - r if sd == "back" else ze + r
                pts = [(x0, hh, zi), (x1, hh, zi), (x0, base, zi), (x1, base, zi),
                       (x0 - r, base, zo), (x1 + r, base, zo)]
            else:
                xi = x0 + inset if sd == "left" else x1 - inset
                xe = x0 if sd == "left" else x1
                xo = xe - r if sd == "left" else xe + r
                pts = [(xi, hh, z0), (xi, hh, z1), (xi, base, z0), (xi, base, z1),
                       (xo, base, z0 - r), (xo, base, z1 + r)]
            sol = hull_solid(pts, mats, vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag=tag + "_" + sd + nm)
            p.add(sol)
            out.append(sol)
    return out


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
    p.add(prism(ellipse(cx, zf + 0.42, 0.55, 0.32, 10), "y", 0.035, 0.062, ASH, vis=(1,), tag="ash_spill"))
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
    bank(p, -wc / 2 - 0.25, wc / 2 + 0.25, zc0 + 0.20, zend - 0.30, 0.05, ybank, mats={"top": BANK, "default": BANK})
    # FX7: the bank's sides slope away in soil (were sheer earth walls): a hull per side whose top edge follows the
    # bank's top (0.05 at the fire mouth -> ybank at the top), its foot 1.5 x the height out, plus a feathered toe
    for sg in (-1, 1):
        xe = sg * (wc / 2 + 0.25)
        xi = xe - sg * 0.30
        za, zb_ = zc0 + 0.20, zend - 0.30
        # (a battered face, 0.45 run per metre, no toe: the tile and pottery yards stand within 2 m on the island;
        # on the map the bank is the hillside itself)
        for (yt0, yt1, kk, ex, tg) in ((0.05, ybank, 0.45, 0.0, "bank_slope"),):
            r0, r1 = kk * (yt0 + 0.20), kk * (yt1 + 0.20)
            pts = [(xi, yt0, za), (xi, yt1, zb_), (xi, -0.20, za), (xi, -0.20, zb_),
                   (xe + sg * r0, -0.20, za + 0.6 * r0), (xe + sg * r1, -0.20, zb_)]
            p.add(hull_solid(pts, BANK, vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag=tg))
    # the bank's back falls away to grade (on the island's flat ground; on the map it runs into the hill)
    p.add(prism([(-0.30, zend - 0.30), (-0.30, zend - 0.30 - 2.2 * ybank), (0.0, zend - 0.30 - 2.2 * ybank),
                 (ybank, zend - 0.30)], "x", -wc / 2 - 0.25, wc / 2 + 0.25, BANK, vis=(1, 2, 3),
                **_g(tag="bank_back")))
    # the firebox: a low box + vault, its arched fire mouth in the front face
    p.add(box(-wf / 2, wf / 2, -0.30, 0.45, zc0, zf, FIRED, vis=(1, 2, 3), **_g(tag="firebox")))
    vault(p, -wf / 2, wf / 2, 0.45, 0.75, zc0 - 0.02, zf, CLAY, tag="firebox_vault")
    mouth(p, 0.0, 0.0, 0.60, 0.72, zf, rng=rng, jamb=FIRED, header=FIRED, tag="fire_mouth")
    p.add(prism(ellipse(0.0, zf + 0.45, 0.65, 0.35, 10), "y", 0.035, 0.062, ASH, vis=(1,), tag="ash_spill"))
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
        m.add(prism(ellipse(0.0, 0.42, 0.50, 0.30, 10), "y", 0.035, 0.062, ASH, vis=(1,), tag="ash_spill"))
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
        p.add(box(x0, x1, -0.30, H, z0, z1, OUTCROP, vis=(1, 2, 3), **_g(tag=tg)))       # FX7: grey field stone
    # coping stones along the rim + a few proud stones in the faces (the dry-stone look)
    for k in range(10):
        a = k / 10.0
        for (x, z) in ((-o + 2 * o * a + 0.2, o - 0.30), (-o + 2 * o * a + 0.2, -o + 0.30)):
            p.add(rough_block(rng, x - 0.20, x + 0.20, H - 0.02, H + 0.12, z - 0.26, z + 0.26, OUTCROP, chamfer=0.05,
                              top_jit=0.03, vis=(1, 2), tag="coping"))
    for (x, y) in ((-1.4, 0.4), (-0.9, 1.3), (0.9, 0.7), (1.5, 1.5), (-1.6, 1.7), (1.3, 0.2)):
        p.add(rough_block(rng, x - 0.22, x + 0.22, y - 0.15, y + 0.15, o - 0.04, o + 0.05, OUTCROP, chamfer=0.05,
                          top_jit=0.02, vis=(1,), tag="face_stone"))
    mouth(p, 0.0, 0.0, 0.60, 0.80, o + 0.002, rng=rng, tag="draw_hole", svis=(1, 2, 3))
    p.add(prism(ellipse(0.0, o + 0.45, 0.60, 0.32, 10), "y", 0.035, 0.062, ASH, vis=(1,), tag="ash_spill"))
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
        p.add(hexa(c, {"top": BANK, "front": OUTCROP, "default": BANK}, vis=(1, 2, 3), geo=True, view=True,
                   fire="dirt", tag=tg))
    # FX7: the feathered toe round the bank's foot (0.40 high at 0.25 inside the bank's foot line, out 2.0 m to
    # 0.20 under grade): the 35 deg bank no longer meets the flat ground in a hard line
    apron(p, -b + 0.65, b - 0.65, -b + 0.65, zf, -0.20, ("back", "left", "right"), toe_h=0.40, toe_k=3.4, inset=0.0,
          tag="bank_toe")
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


# ------------------------------------------------------------------------------------------------ 37 site_adit
ADIT = {"half": 0.91, "post": 0.15, "clear_h": 2.15, "pitch": 0.91, "sets": 9, "len": 4 * KEN}


def adit(p, cx=0.0, zp=0.0, H=4.0, W=9.1, D=10.0, floor_y=0.05):
    """The mine adit (mabu; W3C2_NOTES TR27): a knoll of earth + rock round a 4-ken timbered drift that ends at a
    rockfall (a short dead end, recorded). The portal face lies at z = zp (+z = out), the drift runs to -z. Clear
    section 1.215 wide (between the set posts) x 2.15 high (game D1 / D2). Timber sets (two round posts on sill stones
    + a cap) every 0.91, lagging boards over the caps, a heavier portal set with a shimenawa and paper streamers, a board
    drainage trough along the left foot running out of the mouth. Returns the drift's numbers + the set posts."""
    rng = rng_for("adit")
    A = ADIT
    hw, pw = A["half"], A["post"] / 2
    rw = hw + pw + 0.045                               # the rock faces either side
    z_end = zp - A["len"]
    yc0 = floor_y + A["clear_h"]                       # cap underside
    yc1 = yc0 + 0.18
    x0, x1 = cx - W / 2, cx + W / 2
    zb = zp - D
    g = dict(vis=(1, 2, 3), geo=True, view=True, fire="granite")
    MR = {"top": BANK, "default": OUTCROP}             # FX7: grassed soil on the slopes, weathered rock faces
    # the knoll: left + right masses, the roof over the drift, the back (the rockfall face)
    # the side masses fall away from the drift to the knoll's foot (a hill nose cut by the portal face); the back mass
    # falls to the rear; each a convex hexahedron with planar faces
    ye = 0.45
    for sg, tg in ((-1, "knoll_left"), (1, "knoll_right")):
        xi, xo = cx + sg * rw, cx + sg * W / 2
        c = [(xi, -0.30, zp), (xi, -0.30, zb), (xo, -0.30, zb), (xo, -0.30, zp),
             (xi, H - 0.3, zp), (xi, H - 0.3, zb), (xo, ye, zb), (xo, ye, zp)]
        if sg > 0:
            c = c[:4][::-1] + c[4:][::-1]
        p.add(hexa(c, MR, tag=tg, **g))
    p.add(box(cx - rw - 0.02, cx + rw + 0.02, yc1 + 0.025, H - 0.3, z_end - 0.02, zp, MR, tag="knoll_roof", **g))
    p.add(hexa([(cx - rw - 0.02, -0.30, z_end), (cx + rw + 0.02, -0.30, z_end), (cx + rw + 0.02, -0.30, zb),
                (cx - rw - 0.02, -0.30, zb), (cx - rw - 0.02, H - 0.3, z_end), (cx + rw + 0.02, H - 0.3, z_end),
                (cx + rw + 0.02, ye, zb), (cx - rw - 0.02, ye, zb)], MR, tag="knoll_back", **g))
    # the rounded crown and shoulders (natural rock + earth)
    for (x, z, w, d, h, top) in ((cx, zp - 4.0, 3.4, 4.6, 1.0, H + 0.30), (cx - 2.2, zp - 5.5, 2.4, 3.4, 1.4, H - 0.6),
                                 (cx + 2.2, zp - 3.0, 2.2, 3.0, 1.4, H - 0.7), (cx - 3.5, zp - 1.0, 1.4, 1.6, 1.2, 1.5),
                                 (cx + 3.6, zp - 1.2, 1.4, 1.6, 1.3, 1.6)):
        p.add(stone(rng, x, z, w, d, h, top, OUTCROP, bury=0.30, n=9, flat_top=0.5,
                    tag="knoll_crown", **g))
    # FX7: the knoll's sheer 0.75 m foot (ye over grade + 0.30 buried) feathers out in soil on both sides and the back
    apron(p, x0, x1, zb, zp, ye + 0.10, ("back", "left", "right"), k=2.4, toe_h=0.25, toe_k=4.0, tag="knoll_apron")
    # the timber sets: round posts on flat sill stones, a cap, lagging boards over the caps
    posts = []
    for k in range(A["sets"]):
        z = zp - k * A["pitch"]
        heavy = k == 0
        r = 0.11 if heavy else 0.075
        for sx in (-1, 1):
            x = cx + sx * hw
            p.add(tube((x, floor_y - 0.02, z), (x, yc0, z), r, SOOT if not heavy else WOOD, n=8, vis=(1, 2),
                       tag="set_post"))
            p.add(box(x - r, x + r, floor_y - 0.02, yc0, z - r, z + r, WOOD, vis=(3,), geo=True, view=True,
                      fire=True, tag="set_post_lod"))
            p.add(stone(rng, x, z, 0.30, 0.28, 0.10, floor_y + 0.0, STONE, bury=0.10, n=7, flat_top=0.85,
                        vis=(1,), tag="soseki"))
            posts.append((round(x, 4), round(z, 4), floor_y, yc0))
        p.add(box(cx - rw + 0.01, cx + rw - 0.01, yc0, yc1, z - (0.11 if heavy else 0.08), z + (0.11 if heavy else 0.08),
                  WOOD if heavy else SOOT, vis=(1, 2, 3), tag="set_cap", **dict(geo=True, view=True, fire=True)))
    for j in range(int(A["len"] / 0.25)):
        z = zp - 0.12 - j * 0.25
        p.add(box(cx - rw + 0.02, cx + rw - 0.02, yc1, yc1 + 0.025, z - 0.11, z + 0.11, SOOT, vis=(1,),
                  tag="lagging"))
    # the rockfall at the end
    for k in range(8):
        x, z = cx + rng.uniform(-0.55, 0.55), z_end + 0.25 + rng.uniform(0.0, 0.55)
        sz = rng.uniform(0.25, 0.50)
        p.add(stone(rng, x, z, sz, sz * 0.8, sz * 0.7, floor_y + sz * (0.7 if k < 5 else 1.3), STONE, bury=0.05, n=7,
                    flat_top=0.5, vis=(1, 2), tag="rockfall"))
    p.add(box(cx - rw, cx + rw, floor_y - 0.05, floor_y + 0.75, z_end, z_end + 0.70, STONE, vis=(), geo=True,
              view=True, fire="granite", tag="rockfall_geo"))
    # the drainage trough (board, 0.16 wide) along the left foot and out of the mouth
    xt = cx - hw + pw + 0.10
    zt0, zt1 = z_end + 0.75, zp + 1.40
    for (a, b, y0, y1) in ((xt - 0.08, xt - 0.065, floor_y, floor_y + 0.12), (xt + 0.065, xt + 0.08, floor_y,
                                                                            floor_y + 0.12),
                           (xt - 0.08, xt + 0.08, floor_y - 0.02, floor_y)):
        p.add(box(a, b, y0, y1, zt0, zt1, SOOT, vis=(1, 2), tag="trough"))
    p.add(box(xt - 0.08, xt + 0.08, floor_y - 0.02, floor_y + 0.12, zt0, zt1, SOOT, vis=(), geo=True, view=False,
              fire=True, tag="trough_geo"))
    # the shimenawa over the portal cap, its paper streamers (shide)
    zr = zp + 0.02
    p.add(tube((cx - rw, yc0 + 0.05, zr + 0.11), (cx + rw, yc0 + 0.05, zr + 0.11), 0.035, "straw_rope", n=6,
               vis=(1, 2), tag="shimenawa"))
    for k in range(4):
        x = cx - 0.45 + 0.30 * k
        p.add(box(x - 0.035, x + 0.035, yc0 - 0.28, yc0 + 0.02, zr + 0.145, zr + 0.150, "textile_kinari", vis=(1,),
                  tag="shide"))
    return {"posts": posts, "z_end": z_end, "rw": rw, "clear": (2 * (hw - pw), A["clear_h"]), "trough_x": xt,
            "cap": yc0}


def part_adit(variant):
    p = Part("jp_p_site_adit", variant, "site", tiers=[1, 2],
             used_for="the mine adit (mabu, TR27): a knoll with a 4-ken timbered drift ending at a rockfall, the "
                      "portal's shimenawa, the drainage trough; walkable (a loot floor)",
             recipe="ruralsite_parts.adit(part, cx, zp, H, W, D, floor_y)",
             datum="x centred on the drift, z 0 = the portal face (+z = out), y 0 = grade")
    a = adit(p)
    p.dim("drift_clear_m", ">= 1.00 x 2.00 (D1 / D2)", a["clear"][0], source="W3C2_NOTES TR27")
    p.dims[-1]["ok"] = a["clear"][0] >= 1.0
    p.conn("portal", (0.0, 0.05, 0.0), note="the portal (the drift's mouth)")
    return p


# ------------------------------------------------------------------------------------------------ 26 site_shura
SHURA = {"bays": 4, "bay": 3.64, "rise": 2.40, "logs": 7, "r": 0.10}


def shura(p, x0=0.0, z0=0.0):
    """The timber slide (shura; W3C2_NOTES TR24): its lowest 4 bays, the trough of 7 logs laid side by side lengthwise
    (the middle one lowest: a 0.75-wide trough 0.30 deep), falling from `rise` at its upper end (-z) to grade at the
    landing (z0, +z = the landing); joined over cross-sleepers at every bay end, a log stopped in it near the foot.
    The trestles under it are the shell's (posts on stones). Returns the bed height function."""
    K = SHURA
    L = K["bays"] * K["bay"]
    zt = z0 - L

    def ybed(z):
        return 0.10 + (z0 - z) / L * (K["rise"] - 0.10)
    offs = [(-0.36, 0.26), (-0.24, 0.13), (-0.12, 0.04), (0.0, 0.0), (0.12, 0.04), (0.24, 0.13), (0.36, 0.26)]
    for b in range(K["bays"]):
        za, zb = z0 - b * K["bay"], z0 - (b + 1) * K["bay"]
        for (dx, dy) in offs:
            p.add(tube((x0 + dx, ybed(za) + dy + K["r"], za + 0.10), (x0 + dx, ybed(zb) + dy + K["r"], zb - 0.10),
                       K["r"], WOOD, n=6, vis=(1, 2, 3), tag="shura_log"))
        # one oriented collision slab per bay (the trough's body)
        from .shapes import oriented_box
        import math as _m
        dz = za - zb
        dy = ybed(zb) - ybed(za)
        n = _m.hypot(dz, dy)
        u = (0.0, dy / n, -dz / n)
        up = (0.0, dz / n, dy / n)
        # the trough's far-LOD body as three slabs (the middle lower: C15 compares top heights): x centre, half width,
        # top over the bed
        for (xc, hx, top) in ((0.0, 0.18, 0.22), (-0.33, 0.15, 0.45), (0.33, 0.15, 0.45)):
            hy = (top + 0.05) / 2
            c = (x0 + xc, (ybed(za) + ybed(zb)) / 2 - 0.05 + hy, (za + zb) / 2)
            p.add(oriented_box(c, (1.0, 0.0, 0.0), up, u, hx, hy, n / 2 + 0.05, WOOD, vis=(), geo=True, view=True,
                               fire=True, tag="shura_geo"))
        # the cross-sleeper at the bay's lower end
        p.add(tube((x0 - 0.55, ybed(za) - 0.05, za), (x0 + 0.55, ybed(za) - 0.05, za), 0.10, SOOT, n=7, vis=(1, 2),
                   tag="sleeper"))
    # a log stopped in the trough near the foot (bark-dark), its butt branded
    zl0, zl1 = z0 - 0.6, z0 - 4.6
    p.add(tube((x0, ybed(zl0) + 0.20, zl0), (x0, ybed(zl1) + 0.20, zl1), 0.20, SOOT, n=9, vis=(1, 2, 3), tag="log"))
    return {"L": L, "top": zt, "ybed": ybed}


def part_shura(variant):
    p = Part("jp_p_site_shura", variant, "site", tiers=[1, 2],
             used_for="the timber slide (shura, TR24; a stone slide later TR20 / TR25): a trough of logs laid "
                      "lengthwise, falling to the landing; a log stopped in it",
             recipe="ruralsite_parts.shura(part, x0, z0)",
             datum="x centred, z 0 = the landing end (+z = the landing), the slide rises towards -z; y 0 = grade")
    k = shura(p)
    p.dim("bay_m", "3-4 (GK)", SHURA["bay"], source="W3C2_NOTES TR24")
    p.dims[-1]["ok"] = True
    p.conn("landing", (0.0, 0.10, 0.0), note="the slide's foot")
    return p


def register(reg):
    reg("jp_p_site_kiln_dome", ["_charcoal"], part_kiln_dome)
    reg("jp_p_site_kiln_climbing", ["_4ch"], part_kiln_climbing)
    reg("jp_p_site_kiln_updraught", ["_daruma"], part_kiln_updraught)
    reg("jp_p_site_kiln_shaft", ["_stone"], part_kiln_shaft)
    reg("jp_p_site_adit", ["_timbered"], part_adit)
    reg("jp_p_site_shura", ["_log4"], part_shura)
