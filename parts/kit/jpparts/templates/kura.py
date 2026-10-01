"""The kura template (C3, Phase C wave 1, 2026-09-30): DW22 plastered storehouse (dozo kura), KEEP_DWELLINGS 22,
PARTS_GAP_AUDIT DW22 row ('buildable today': frame_town, kura_footing, kura_walls, kura_open, kura_eave, sangawara /
hongawara, grime, helper:floors; 'loft by stair or ladder for elevation', G1-5).

    M, floors, rooms, info = kura.model(lower="namako", door="_open")

The shell: 3 x 2 ken (5.46 x 3.64 m, the common town kura behind a machiya lot), hirairi (door on a long side),
  - a one-course cut-granite footing (found.kura_footing, individual blocks) under 0.24 m okabe walls (posts hidden in
    the plaster, walls.wall_run kind 'okabe'); white shikkui outside, B1's jp_m_wall_shikkui_int on every face that
    looks into a room (PLAYBOOK §15 T6, the T6 gap the audit named)
  - the lower wall: 'namako' (diagonal namako tiles, walls.namako) on the front and both gables, the back plain with a
    grime band | 'shitami' (black lapped boards, walls.wall_run kind 'shitami' _kura) on all four | 'plain'
  - the kura doorway (openings.part_kura_door): stepped plaster surround, inner sliding plank door (the game door),
    outer plaster leaves static open ('_open') or as rotation doors ('_hinged': the engine test PARTS_GAP_AUDIT §6
    risk 4 asks for before the gate family); a stone landing and step with a hidden walk ramp (<= 34 deg)
  - kura windows (openings.part_kura_window, static: iron bars, a plaster shutter, a tiny tile pent): one on the ground
    floor (right gable), four upstairs (front, back, both gables)
  - two storeys inside (a kura's upper floor is its period form; G1-5 'kura lofts by stair' for elevation): ground
    floor boards at 0.45 on the footing, the upper floor at 2.85 reached by jp_p_stair _open (the plain stair of kura
    lofts: 1.10 wide, 37.8 deg walk ramp) along the back wall, its stairwell cut into the upper floor with a rim and a
    guard rail (stair.well_fn); >= 2.10 m head room over both floors
  - the roof: kirizuma, sangawara | hongawara (roofs.roof, soffit off) with the kura eave look: plastered soffit
    under the overhang, plaster fascia and bargeboards, two stepped plaster bands at the wall head (roofparts
    part_kura_eave's bands), the eave closed to the roof (C11); plaster gables (walls.gable _kura) with the barred vent;
    a ridge beam and purlins seen from the upper floor

Kit frame (the rural template's): x 0..W along the ridge, z 0 = front wall line (+z out), z -D back wall line, y 0
grade. model() puts the origin on the footprint centre, +z = front (the door side).
Levels (m): footing top 0.30, ground floor 0.45, upper floor 2.85 (underside 2.70: 2.25 clear below), eave 5.00.
"""
import math

from ..core import Part, box, prism, KEN, HALF, POST
from .. import walls, found, openings, roofs as R, floors as FL, stair as ST, trim
from ..shapes import slab, clip_rect, rough_block
from ..core import rng_for
from .rural import Shell, _r

FOOT = 0.30                 # footing top (walls stand on it)
FLOOR = 0.45                # ground floor boards (0.15 sleepers on the footing course)
LOFT = 2.85                 # upper floor top
LOFT_CEIL = 2.70            # upper floor underside
E = 5.00                    # eave line (rafter underside at the wall line)
T_WALL = 0.24
FACE = T_WALL / 2
OKABE_IN = {"back": "wall_shikkui_int", "default": "wall_shikkui"}      # okabe faces: local -z looks into the room
OV, GOV = 0.60, 0.30        # the kura eave is short (part_kura_eave 0.55) and plastered
STAIR_W = 1.10
NAMAKO_H = 1.35             # namako tile field height over the footing (face budget: the joints are modelled)
LOWER = ("namako", "shitami", "plain")


def _okabe(S, name, fr, x0, x1, y0, y1, openings_=(), ext=0.0):
    """A 0.24 okabe run on the wall frame fr (local -z = inside): shikkui outside, shikkui_int inside."""
    p = S.B.P(name)
    walls.wall_run(p, "okabe", x0, x1, y0=y0, y1=y1, openings=openings_, thick=T_WALL, face_mats=OKABE_IN,
                   ext0=ext, ext1=ext)
    S.B.put(p, fr, what="walls.wall_run okabe _kura (%s)" % name)
    return p


def _to_int(part, tags):
    """Faces of the tagged solids that look into the room (local -z) take the interior plaster (T6)."""
    for s in part.solids:
        if s.tag in tags and s.fm:
            s.fm = ["wall_shikkui_int" if n[2] < -0.7 else m for n, m in zip(s.fn, s.fm)]


def _recolour(part, tags, mat):
    for s in part.solids:
        if s.tag in tags and s.fm:
            s.fm = [mat] * len(s.fm)


def kura_door(variant="_open"):
    """jp_p_open_kura_door in the DoorsTwinN convention (rural.big_leaf's adapter): the part keeps the older one-leaf
    format (core.sliding_leaf, no twin selection). Every door of the part gets its own twin: the inner sliding door
    doorstwin1 (renamed by Builder.place_door), the '_hinged' outer plaster leaves doorstwin2 / 3 (so the kura door must
    be placed as the building's first door)."""
    p = openings.part_kura_door(variant)
    # T11 / C17 (the part predates G3 fix 2): the inner leaf runs 1.2 cm off the okabe's inner face (z -0.12, leaf
    # z -0.132..-0.172, opening x 0.29..1.53, sliding +x). A lip on the slide-past jamb and a stop on the closing jamb.
    th, zl = 0.15, -0.12 - openings.GAP
    openings.jamb_lip(p, 1.53, 1.53 + 0.10, th, th + 2.03, -0.12, zl)
    openings.jamb_stop(p, 0.29 - openings.OV, +1, th, th + 2.03, -0.12, zl - 0.04 - 0.02)
    for s in p.solids:
        if s.tag == "kura_leaf_step" and not s.door:
            s.vis = set(s.vis) | {2, 3}           # the static open leaves' stepped edge is outline (C15)
    for i, d in enumerate(p.doors):
        tw = "doorstwin%d" % (i + 1)
        bones = set(d.bones())
        for s in p.solids:
            if s.door in bones:
                s.sel = tw
        b0 = d.anims[0]["bone"]
        if b0 + "_action" in p.memory:
            p.memory[tw + "_action"] = p.memory.pop(b0 + "_action")
        d.twin = tw
        if i == 0:
            d.park_end = d.sweep[1] if getattr(d, "sweep", None) else None
            d.passable = True
            d.act_h = d.action[1]
        d.engine_tested = False
    return p


def kura(name=None, lower="namako", door="_open", roof="sangawara", window="_slide", wear="_w1"):
    if lower not in LOWER:
        raise ValueError("lower: one of %s" % (LOWER,))
    W, D = 3 * KEN, 2 * KEN
    t = R.PITCH[roof]
    S = Shell(name or "jp_kura", W, D, [2, 3], "plastered storehouse (DW22 dozo kura), 3 x 2 ken, upper floor by stair",
              wear)
    B = S.B
    F = S.F
    portals = S.portals

    # ------------------------------------------------ footing (individual cut blocks), hidden post nodes
    for side, (a, b), seed in (("front", (-FACE, W + FACE), 1), ("back", (-FACE, W + FACE), 2),
                               ("left", (0.28, D - 0.28), 3), ("right", (0.28, D - 0.28), 4)):
        p = B.P("footing_" + side)
        found.kura_footing(p, a, b, 1, wall_t=T_WALL, seed=seed)
        B.put(p, F[side], 0.0, FOOT, what="found.kura_footing _c1 (%s)" % side)
    for k in range(4):
        for z in (0.0, -D):
            S.posts.append((round(k * KEN, 4), z, FOOT, E))
    for z in (-KEN,):
        for x in (0.0, W):
            S.posts.append((x, z, FOOT, E))

    # ------------------------------------------------ openings (local x on each wall frame)
    DX = KEN                                       # the door bay on the front: x 1.82..3.64, parks over 3.64..5.46
    door_hole = (DX + 0.29, DX + 1.53, FLOOR, FLOOR + 2.15)
    win = []                                       # (side, dx, dy): kura window half-ken bays

    def wh(dx, dy):
        return (dx + HALF / 2 - 0.30, dx + HALF / 2 + 0.30, dy + 1.20, dy + 1.95)
    # upper windows only on the gables: on the eave walls a window's surround and tile pent would run up into the
    # short plastered eave (C12)
    win.append(("left", D / 2 - HALF / 2, LOFT))   # upper gables, centred
    win.append(("right", D / 2 - HALF / 2, LOFT))
    win.append(("back", 0.0, FLOOR))               # the ground floor's one small window (back, by the right gable)
    holes = {s: [wh(dx, dy) for (s_, dx, dy) in win if s_ == s] for s in F}
    holes["front"].append(door_hole)

    # ------------------------------------------------ walls: eave walls up under the roof, gable walls to the eave
    YE = E - t * (FACE + 0.02) - 0.02              # eave-wall top: under the rafter plane at the outer face
    for side in ("front", "back"):
        _okabe(S, "okabe_" + side, F[side], 0.0, W, FOOT, YE, holes[side], ext=FACE)
        # the wedge that closes the wall head to the roof underside (inside to outside, 1 cm under the rafter plane)
        p = B.P("wall_head_" + side)
        p.add(prism([(YE, -FACE), (YE, FACE), (E - t * FACE - 0.01, FACE), (E + t * FACE - 0.01, -FACE)], "x",
                    -FACE, W + FACE, OKABE_IN, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="wall_head"))
        # the kura eave's stepped plaster bands (roofparts.part_kura_eave) under the plastered soffit: the outer band
        # (0.14 proud) just under the soffit, the inner one (0.07) below it
        b2 = E - t * (FACE + 0.14) - 0.105
        for (y0_, y1_, pr) in ((b2 - 0.14, b2, 0.14), (b2 - 0.30, b2 - 0.14, 0.07)):
            p.add(box(-FACE - pr, W + FACE + pr, y0_, y1_, FACE, FACE + pr, "wall_shikkui", vis=(1, 2, 3),
                      geo=True, view=True, fire=True, tag="kura_band"))
        B.put(p, F[side], what="kura eave bands + wall head (%s)" % side)
    for side in ("left", "right"):
        _okabe(S, "okabe_" + side, F[side], FACE, D - FACE, FOOT, E, holes[side])
        g = B.P("gable_" + side)
        walls.gable(g, D, t, E, "_kura")
        _to_int(g, ("gable_infill",))
        _recolour(g, ("tie_beam",), "wall_shikkui")
        B.put(g, F[side], what="walls.gable _kura (%s)" % side)
        yaw, o = F[side]
        for s in g.transformed(yaw, o).solids:
            if s.tag == "vent_geo":
                b_ = s.bbox()
                portals.append(("gable vent %s" % side, (b_[0] - 0.25, b_[1] + 0.25, b_[2] - 0.05, b_[3] + 0.05,
                                                         b_[4] - 0.25, b_[5] + 0.25)))

    # ------------------------------------------------ lower wall finish
    if lower == "namako":
        for side, runs in (("front", [(-FACE - 0.012, DX - 0.02), (DX + KEN + 0.02, W + FACE + 0.012)]),
                           ("left", [(-FACE, D + FACE)]), ("right", [(-FACE, D + FACE)])):
            p = B.P("namako_" + side)
            for (a, b) in runs:
                walls.namako(p, a, b, FOOT, FOOT + NAMAKO_H, FACE, diagonal=True)
            for s in p.solids:
                if s.tag == "namako_joint":
                    s.vis = {1}                      # the raised joints are close detail (R2 keeps the tile layer)
            B.put(p, F[side], what="walls.namako diagonal (%s)" % side)
        p = B.P("grime_back")
        trim.grime_band(p, -FACE, W + FACE, FACE, y0=FOOT)
        B.put(p, F["back"], what="trim.grime_band (back)")
    elif lower == "shitami":
        for side, runs in (("front", [(-FACE - 0.03, DX - 0.02), (DX + KEN + 0.02, W + FACE + 0.03)]),
                           ("back", [(-FACE - 0.03, W + FACE + 0.03)]), ("left", [(-FACE, D + FACE)]),
                           ("right", [(-FACE, D + FACE)])):
            p = B.P("shitami_" + side)
            for (a, b) in runs:
                # one lapped board run on the okabe face (thick = FACE puts it on the plaster, walls.part_shitami)
                ops = [(x0 - 0.02, x1 + 0.02, y0 - FOOT, y1 - FOOT) for (x0, x1, y0, y1) in holes[side]
                       if y0 < FOOT + 1.80]
                sub = B.P("sh")
                walls.wall_run(sub, "shitami", a, b, y0=0.0, y1=1.80, openings=ops, mat="wood_kuro", thick=FACE)
                for s in sub.solids:              # face budget: the lapped boards stay close, one slab from R2 on
                    if s.tag == "shitami":
                        s.vis = {1}
                    if s.tag == "shitami_lod":
                        s.vis = {2, 3}
                p.merge(sub.transformed(0.0, (0.0, FOOT, 0.0)))
            B.put(p, F[side], what="walls.wall_run shitami _kura (%s)" % side)
    else:
        for side in F:
            p = B.P("grime_" + side)
            trim.grime_band(p, -FACE if side in ("front", "back") else 0.0,
                            W + FACE if side in ("front", "back") else D, FACE, y0=FOOT)
            B.put(p, F[side], what="trim.grime_band (%s)" % side)

    # ------------------------------------------------ the door (+ the hinged outer leaves as their own doors)
    if S.H.doors:
        raise ValueError("the kura door must be the building's first door (its outer leaves are doorstwin2 / 3)")
    S.door(kura_door(door), "front", DX, FLOOR, "Kura door (inner sliding door)", "front")
    for k, d in enumerate(S.H.doors[1:], 2):
        d.label = "Kura outer leaf %s" % ("left" if k == 2 else "right")
    S.dn["front"] = "DoorsTwin1"
    # C15: the door pent's eave-tile lips stand past its slab and fascia in plan; a far strip (Resolution 2 / 3) under
    # them keeps the top-down outline (the main roof's own eave_strip does the same)
    tiles = [s.bbox() for s in S.H.solids if (getattr(s, "src", "") or "").startswith("jp_p_open_kura_door") and
             s.tag in ("eave_tile", "kawara_field") and 1 in s.vis and 3 not in s.vis]
    if tiles:
        x0, x1 = min(b[0] for b in tiles), max(b[1] for b in tiles)
        y1, z0, z1 = max(b[3] for b in tiles), min(b[4] for b in tiles), max(b[5] for b in tiles)
        tp = 0.40                                   # the mini pent's slope
        S.H.add(prism([(y1 - 0.03, z0), (y1 - 0.03 - tp * (z1 - z0), z1), (y1 - 0.09 - tp * (z1 - z0), z1),
                       (y1 - 0.09, z0)], "x", x0, x1, "roof_kawara_far", vis=(2, 3), tag="pent_far"))
    # stone landing + step down to grade, over a hidden walk ramp (<= 34 deg) from the door's own outer ramp
    cx = DX + HALF
    z0r = 0.54                                     # where the door part's outer ramp meets FLOOR
    run = FLOOR / math.tan(math.radians(34.0))
    st = B.P("kura_step")
    xa, xb = cx - 0.67, cx + 0.67
    st.add(prism([(FLOOR, z0r), (0.0, z0r + run), (0.0, z0r)], "x", xa, xb, "stone_cut", vis=(), geo=True, view=False,
                 fire="granite", tag="ramp"))
    st.road([(xa, FLOOR, z0r), (xb, FLOOR, z0r), (xb, 0.0, z0r + run), (xa, 0.0, z0r + run)], "stone_ext")
    rng = rng_for("kura_step" + (name or ""))
    st.add(rough_block(rng, cx - 0.78, cx + 0.78, -0.05, FLOOR, FACE, 0.62, "stone_cut", chamfer=0.02, top_jit=0.002,
                       vis=(1, 2, 3), tag="step_slab"))
    st.add(rough_block(rng, cx - 0.70, cx + 0.70, -0.05, 0.22, 0.62, 0.95, "stone_cut", chamfer=0.02, top_jit=0.002,
                       vis=(1, 2, 3), tag="step_slab"))
    B.put(st, (0.0, (0.0, 0.0, 0.0)), what="kura landing + step (cut granite) over a hidden ramp")

    # ------------------------------------------------ windows (static kura windows) = C11 portals
    for (side, dx, dy) in win:
        wp = openings.part_kura_window(window)
        for s in wp.solids:                       # face budget (standard class): small window detail stays close
            if s.tag in ("surround", "shutter"):
                s.vis = set(s.vis) - {3}
            if s.tag in ("bar", "shutter_track"):
                s.vis = {1}
        B.put(wp, F[side], dx, dy, what="jp_p_open_kura_window %s (%s)" % (window, side))
        a0, a1, b0, b1 = wh(dx, dy)
        yaw, o = F[side]
        from ..assemble import to_world
        p0 = to_world(F[side], a0, -0.40)
        p1 = to_world(F[side], a1, 0.40)
        portals.append(("kura window %s %.2f" % (side, dy), (min(p0[0], p1[0]), max(p0[0], p1[0]), b0 - 0.02, b1 + 0.02,
                                                             min(p0[1], p1[1]), max(p0[1], p1[1]))))

    # ------------------------------------------------ floors, stair, upper floor
    xi0, xi1, zi0, zi1 = FACE, W - FACE, -D + FACE, -FACE           # inside faces
    B.interior = True
    B.merge(FL.boards("floor_ground", xi0, xi1, zi0, zi1, FLOOR, along_x=True, mats=FL.MATS_BOARDS_B1))
    rise = LOFT - FLOOR
    stp = Part("stair_kura", "", "")
    SS = ST.stair(stp, STAIR_W, rise, "open")
    srun = SS["run"]
    x_foot, oz = 1.15, zi0
    B.merge(stp.transformed(180.0, (x_foot, FLOOR, oz), mirror=True))      # flight +x, width towards +z
    wx0, wx1, wz0, wz1 = ST.well_rect(srun, STAIR_W, rise)
    well = (x_foot + wx0, x_foot + wx1, zi0, oz - wz0)
    B.merge(FL.loft("floor_upper", xi0, xi1, zi0, zi1, LOFT_CEIL, LOFT, walkable=True,
                    holes=[{"rect": well, "kind": "stair", "open": "x1", "wall": "z0"}], hole_fn=ST.well_fn()))
    # the roof timbers seen from the upper floor: ridge beam + a purlin each side, under the rafter plane (visual)
    for s_in in (D / 2, D / 2 - KEN / 2, D / 2 + KEN / 2):
        zc = -s_in
        yt = E + t * min(s_in, D - s_in) - 0.012
        B.H.add(box(-FACE + 0.01, W + FACE - 0.01, yt - 0.15, yt, zc - 0.07, zc + 0.07, "wood_interior", vis=(1,),
                    tag="roof_timber", grain="long"))
    B.interior = False
    S.obst.append(("kura", _r(x_foot - 0.05, x_foot + srun + 0.05, zi0, oz + STAIR_W + 0.06)))
    S.obst.append(("kura", _r(door_hole[0], door_hole[1], -0.42, -FACE)))           # the door's inner ramp
    S.obst.append(("nikai", _r(well[0] - 0.10, well[1] + 0.10, zi0, well[3] + 0.10)))
    stair_info = {"foot": (x_foot, oz), "run": srun, "width": STAIR_W, "y_low": FLOOR, "y_up": LOFT, "well": well}

    # ------------------------------------------------ roof (kirizuma, plastered kura eave)
    rp = B.P("roof_main")
    sls, info_r = R.roof(rp, W, D, "kirizuma", roof, eave_y=E, ov=OV, gov=GOV, soffit=False,
                         courses=5 if roof == "hongawara" else 3, eave_style="tomoe")
    _recolour(rp, ("kawara_fascia", "hafu", "verge_batten", "purlin_end"), "wall_shikkui")
    for sl in sls:
        for pc in sl.pieces:
            # the plastered soffit under every overhang (outside the wall faces), 10 cm under the rafter plane
            for (a, b, c, d) in ((-99, -FACE, -99, 99), (W + FACE, 99, -99, 99), (-FACE, W + FACE, FACE, 99),
                                 (-FACE, W + FACE, -99, -D - FACE)):
                q = clip_rect(pc, a, b, c, d)
                if len(q) >= 3:
                    rp.add(slab(q, lambda x, z, s_=sl: s_.y(x, z, -0.10), lambda x, z, s_=sl: s_.y(x, z, -0.001),
                                "wall_shikkui", vis=(1, 2, 3), tag="kura_soffit"))
    S.H.merge(rp)
    rw = R.ridge_walk(info_r)
    if rw:
        S.H.merge(rw)
    S.log.append("roofs.roof kirizuma %s eave %.2f ov %.2f (plastered soffit, fascia, bargeboards)" % (roof, E, OV))

    # ------------------------------------------------ rooms
    S.place_windows()
    doors = [S.dn["front"]]
    S.room("kura", "storage", "boards", FLOOR, (xi0, xi1, zi0, zi1), doors,
           "ground floor: boards on the footing, the stair up along the back wall")
    S.room("nikai", "storage", "boards", LOFT, (xi0, xi1, zi0, zi1), [],
           "upper floor (the kura's storey, reached by the stair; G1-5 elevation)")
    H, info = S.finish({"params": {"kind": "kura", "lower": lower, "door": door, "roof": roof, "window": window},
                        "levels": {"footing": FOOT, "floor": FLOOR, "upper": LOFT, "eave": E}, "stair": stair_info,
                        "stairwell": well})
    # FB1 (2026-10-01, Stephen: the white kura "doesn't match anything"): every exterior shikkui face (walls, eave
    # bands, soffit, surrounds, leaves, shutters, ridge) takes FP1's aged plaster; the interior plaster stays
    for s_ in H.solids:
        if isinstance(s_.mats, str):
            if s_.mats == "wall_shikkui":
                s_.mats = PLASTER_OUT
        elif isinstance(s_.mats, dict):
            s_.mats = {k: (PLASTER_OUT if v == "wall_shikkui" else v) for k, v in s_.mats.items()}
        if s_.fm:
            s_.fm = [PLASTER_OUT if m == "wall_shikkui" else m for m in s_.fm]
    return H, info


PLASTER_OUT = "wall_shikkui_aged"         # FB1: jp_m_wall_shikkui_aged (FP1, research/materials/make_fp1_materials.py)


def budget_class(**params):
    """PLAYBOOK §12: two storeys inside, 19.9 m2: 'standard'."""
    return "standard"


def model(name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front, the door side)."""
    H, info = kura(name=name, **params)
    cx, cz = info["W"] / 2, -info["D"] / 2
    M = H.transformed(0.0, (-cx, 0.0, -cz))
    M.meta = dict(H.meta)

    def mr(r):
        return (r[0] - cx, r[1] - cx, r[2] - cz, r[3] - cz)
    floors = [dict(f, rect=mr(f["rect"]), obstacles=[mr(o) for o in f["obstacles"]]) for f in info["floors"]]
    rooms = [dict(r, rect_model=[round(v, 3) for v in mr(r["rect_kit"])]) for r in info["rooms"]]
    st = info["stair"]
    stair_model = dict(st, foot=(st["foot"][0] - cx, st["foot"][1] - cz), dir=1.0, well=mr(st["well"]))
    info = dict(info, centre=(cx, cz), fittings_model=[], stair_model=stair_model,
                portals_model=[(n, (b[0] - cx, b[1] - cx, b[2], b[3], b[4] - cz, b[5] - cz)) for n, b in info["portals"]],
                passages_model=[])
    return M, floors, rooms, info
