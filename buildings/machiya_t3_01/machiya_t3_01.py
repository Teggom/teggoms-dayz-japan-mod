#!/usr/bin/env python3
r"""Land_JP_Machiya_T3_01 - the tier-3 town machiya, assembled ONLY from the parts library (parts/kit, jpparts) and
jp_common materials. The recipe: build() returns the whole building as one kit Part (path A: recipes + fixed parts from
their registry builders, placed on wall-line frames).

Kit frame used while assembling: x 0..W along the street (the toriniwa is x 0..1 ken), z 0 = street wall line with +z
towards the street, the back is -z, y 0 = grade. build() then moves the origin to the centre of the wall footprint, so
the model origin = placement point at ground level (autocenter=0); the front faces model +z (placed at yaw 180 it faces
south).

Plan (PLAYBOOK §2-4, §10.3; references in REPORT.txt):
  omoya  4 x 3 ken, kirizuma sangawara (main span 3 ken, §2.2), low sealed upper storey (tsushi-nikai, G0-4)
    toriniwa (doma)   x 0..1 ken, full depth, entrance from the street
    mise   (shop)     x 1..4 ken, z 0..-1.5 ken, tatami, raised +0.45
    zashiki           x 1..4 ken, z -1.5..-3 ken, tatami, raised +0.45
  geya   4 x 2 ken lean-to (sangawara, 4 sun) behind the omoya, doma level
    kitchen (doma, kamado)  x 0..2 ken
    storage (boards)        x 2..4 ken
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import core, walls, frame, found, openings, roofs as R, roofparts, trim  # noqa: E402
from jpparts.core import Part, box, KEN, HALF, POST  # noqa: E402
from jpparts import floors as FL, leanto  # noqa: E402
from jpparts.assemble import Builder, to_world  # noqa: E402

NAME = "jp_machiya_t3_01"
CLASS = "Land_JP_Machiya_T3_01"
FRAME_NOTE = ("model: origin = footprint centre at grade, +z = street front, +x = the rooms side (the toriniwa is -x); "
              "placed at yaw 180 (front south)")          # rooms.json (buildings/pipeline.py)

# ------------------------------------------------------------------------------------------------ dimensions
W = 4 * KEN                 # frontage 4 ken (Ioka: 4 kyo-ken)
DO = 3 * KEN                # omoya depth = main roof span, 3 ken max for commoners (PLAYBOOK §2.2)
DG = 2 * KEN                # geya (rear lean-to) depth
ZB = -DO                    # omoya back wall line
ZG = -(DO + DG)             # geya back wall line
XT = KEN                    # toriniwa / rooms line
XS = 2 * KEN                # kitchen / storage line (geya)
GRADE = 0.0
SILL = 0.27                 # dodai top (stones show 0.15, sill 0.12)
DOMA = 0.05                 # PLAYBOOK §4: doma = grade + 0.05
FLOOR = 0.50                # raised rooms: doma + 0.45
STORE = 0.08                # storage board floor (boards on sleepers, one 3 cm lip)
CEIL = 3.00                 # underside of the loft floor = room ceiling (2.50 clear over the rooms, D6)
LOFT = 3.15                 # loft floor top (doma + 3.10, PLAYBOOK §4 low upper storey)
KETA_O = LOFT + 1.30        # 4.45 keta underside: street wall above the upper floor 1.30 (§4 / D3, mushiko part)
EAVE_O = KETA_O + 0.18      # 4.63 eave line (keta top)
GTIE = EAVE_O - 0.21        # 4.42 underside of the gable tie beam (walls.gable)
T_MAIN = R.PITCH["sangawara"]
PENT_Y = 3.30               # street pent (jp_p_roof_hisashi_tile): eave edge ~2.99, soffit >= 2.20
GPENT_Y = 3.10              # gable pent at the upper-floor line (Ioka)
T_GEYA = 0.40               # 4 sun
GEYA_EAVE = 2.69            # geya keta top (roof bed at the back wall line)
GEYA_OV, GEYA_GOV = 0.90, R.GABLE_OV["sangawara"]
KETA_G = GEYA_EAVE - 0.18   # 2.51
A_, B_ = POST / 2, KEN - POST / 2

# wall-line frames (yaw, origin): the sub-part's +x runs along the wall, its +z faces 'out' (core.rot_y convention)
F_FRONT = (0.0, (0.0, 0.0, 0.0))            # street wall z=0; local x = x
F_BACK_O = (180.0, (W, 0.0, ZB))            # omoya back wall; local x = W - x; out = -z (geya)
F_LEFT_O = (90.0, (0.0, 0.0, ZB))           # gable x=0 (toriniwa side); local x = z - ZB; out = -x
F_RIGHT_O = (-90.0, (W, 0.0, 0.0))          # gable x=W; local x = -z; out = +x
F_TORI = (90.0, (XT, 0.0, ZB))              # room edge x=1 ken; local x = z - ZB; out = -x (toriniwa)
F_MID = (0.0, (0.0, 0.0, -DO / 2))          # mise / zashiki partition; local x = x; out = +z (mise)
F_BACK_G = (180.0, (W, 0.0, ZG))            # geya back wall; local x = W - x; out = -z (yard)
F_LEFT_G = (90.0, (0.0, 0.0, ZG))           # geya gable x=0; local x = z - ZG; out = -x
F_RIGHT_G = (-90.0, (W, 0.0, ZB))           # geya gable x=W; local x = ZB - z; out = +x
F_PART_G = (90.0, (XS, 0.0, ZG))            # kitchen / storage partition; local x = z - ZG; out = -x (kitchen)

ROOMS = []                  # filled by build(): room tags for the decorator (PLAYBOOK §10.3)
WINDOWS = []                # (label, frame, dx, dy, mirror, part): openable windows, placed after the doors
AMADO_SILL = 0.75           # zashiki amado window sill above the tatami (part jp_p_open_amado_window)
TSUKI_Y = 0.36              # storage tsukiage placed so its shutter clears the 0.90 koshiita (sill 1.26, floor 0.08)
FLOORS = []                 # walkable floors for loot + checks: {name, tag, rect (kit frame), y, obstacles}
POSTS = []                  # (x, z) of every post node, for the C3 grid check
LOG = []                    # which library part / recipe went where
MISE = {}                   # the shop floor's strip / tatami / yose rectangles (kit frame), from floors.mise


# ------------------------------------------------------------------------------------------------ helpers
# The assembly helpers, floors, lean-to, udatsu placer and ridge walk that used to live here are in the kit since B0
# (2026-09-29): jpparts.assemble (Builder: put / place_door / posts_on / wall / dodai_stones / sloped_wall),
# jpparts.floors (tatami / boards / doma / loft), jpparts.leanto (roof, sloped_wall), walls.udatsu_placed and
# roofs.ridge_walk. The machiya builds exactly what it built before (proof: B0_PROGRESS.md / checks.json).
P = Builder.P
floor_rect = FL.floor_rect


# ------------------------------------------------------------------------------------------------ kamado
def kamado(B, x0, x1, z0, z1):
    """Built-in clay stove (two fire mouths) against the kitchen gable: plastered clay on a stone course, sooted
    board splashback (W5). Its Geometry is one box; loot keeps clear of it."""
    s = P("kamado")
    top = DOMA + 0.72
    s.add(box(x0, x1, DOMA, DOMA + 0.10, z0, z1, "stone_cut", vis=(1, 2, 3), tag="kamado_base"))
    s.add(box(x0, x1, DOMA, top, z0, z1, "wall_nakanuri_int", vis=(), geo=True, view=True, fire="dirt",
              tag="kamado_geo"))
    s.add(box(x0 + 0.02, x1 - 0.02, DOMA + 0.10, top - 0.04, z0 + 0.02, z1 - 0.02, "wall_nakanuri_int", vis=(1, 2, 3),
              tag="kamado_body"))
    s.add(box(x0, x1, top - 0.04, top, z0, z1, "wall_nakanuri_int", vis=(1, 2, 3),
              tag="kamado_top"))
    n = 2
    L = (z1 - z0) / n
    for k in range(n):
        zc = z0 + (k + 0.5) * L
        s.add(box(x1 - 0.02, x1 + 0.005, DOMA + 0.16, DOMA + 0.42, zc - 0.17, zc + 0.17, "wood_sooted", vis=(1, 2),
                  tag="fire_mouth"))
        xc = (x0 + x1) / 2
        from jpparts.shapes import tube
        s.add(tube((xc, top, zc), (xc, top + 0.03, zc), 0.22, "metal_iron", n=10, vis=(1,), tag="pot_rim"))
    s.add(box(0.04, 0.056, DOMA + 0.72, DOMA + 2.2, z0 - 0.2, z1 + 0.2, "wood_sooted", vis=(1, 2), tag="soot_boards"))
    B.merge(s)
    LOG.append("kamado: built-in clay stove from library materials (wall_nakanuri, stone_cut, wood_sooted, metal_iron)")


# ------------------------------------------------------------------------------------------------ build
def build():
    del ROOMS[:], FLOORS[:], POSTS[:], LOG[:], WINDOWS[:]
    MISE.clear()
    H = Part(NAME, "", "buildings", tiers=[3], used_for="tier-3 Kamigata town machiya (Ioka type)")
    H.wear = "_w1"
    B = Builder(H, posts=POSTS, log=LOG)
    itado_twin = openings.part_itado("_twin")          # hikichigai: the main entrance only (PLAYBOOK §15 T3)
    itado_single = openings.part_itado("_single")      # katabiki: back and kitchen doors
    shoji_single = openings.part_shoji_ext("_single")  # katabiki: the room entrances off the toriniwa
    shoji_hikiwake = openings.part_shoji_ext("_hikiwake")   # hikiwake: the mise / zashiki shoji pair

    # ======================================================================== STREET FRONT (z = 0)
    # base: low sill over the entrance + park bays (door tracks at doma level), dodai on dressed stones elsewhere
    s = P("front_lowsill")
    frame.dodai(s, -0.06, KEN + HALF + 0.06, z=0.0, y_top=DOMA)
    H.merge(s)
    B.dodai_stones(F_FRONT, KEN + HALF + 0.10, W, 11, SILL)
    B.posts_on(F_FRONT, [0.0, KEN, KEN + HALF], DOMA, KETA_O)
    B.posts_on(F_FRONT, [2 * KEN, 3 * KEN, W], SILL, KETA_O)
    # B1 entrance (twin itado, parks stacked over B2a), B2a plain park bay, B2b koshi window, B3-B4 degoshi shop front
    B.wall(F_FRONT, "front_b1", "shinkabe", 0.0, KEN, DOMA, CEIL, openings_=[(A_, B_, DOMA, DOMA + 2.0)])
    B.place_door(itado_twin, F_FRONT, 0.0, DOMA, label="Entrance (street)")
    B.wall(F_FRONT, "front_b2a", "shinkabe", KEN, KEN + HALF, DOMA, CEIL, grime=[(KEN + A_, KEN + HALF - A_, None)])
    B.wall(F_FRONT, "front_b2b", "shinkabe", KEN + HALF, 2 * KEN, SILL, CEIL,
         openings_=[(KEN + HALF + A_, 2 * KEN - A_, SILL + 0.45, SILL + 2.0)],
         koshiita=[(KEN + HALF + A_, 2 * KEN - A_, 0.39)], grime=[(KEN + HALF + A_, 2 * KEN - A_, None)])
    # street window: koshi lattice + a sliding shoji panel inside, parking over the plain half-ken B2a (mirrored)
    WINDOWS.append(("street window", F_FRONT, 2 * KEN, SILL, True, openings.part_window_slide("_shoji")))
    for k in (2, 3):
        x0 = k * KEN
        B.wall(F_FRONT, "front_b%d" % (k + 1), "shinkabe", x0, x0 + KEN, SILL, CEIL,
             openings_=[(x0 + A_, x0 + B_, SILL + 0.39, SILL + 2.0)], koshiita=[(x0 + A_, x0 + B_, 0.33)],
             grime=[(x0 + A_, x0 + B_, None)])
        B.put(openings.part_koshi("_degoshi"), F_FRONT, x0, SILL, what="jp_p_open_koshi_degoshi (shop front)")
    # floor beam, upper street wall with oval mushiko, keta, street pent, udatsu
    H.add(box(-0.06, W + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="floor_beam"))
    B.wall(F_FRONT, "front_up_b1", "okabe", 0.0, KEN, LOFT, KETA_O, finish="shikkui", thick=0.15)
    for k in (1, 2, 3):
        B.put(openings.part_mushiko("_oval"), F_FRONT, k * KEN, LOFT, what="jp_p_open_mushiko_oval")
    s = P("keta_front")
    frame.keta(s, -0.30, W + 0.30, z=0.0, y_top=EAVE_O)
    H.merge(s)
    s = P("pent_front")
    roofparts.pent(s, 0.09, W - 0.09, PENT_Y, 0.91, 0.40, "tile")
    H.merge(s)
    LOG.append("roofparts.pent tile (jp_p_roof_hisashi_tile recipe) over the street front")
    for x in (0.0, W):
        u = walls.udatsu_placed(x, PENT_Y, KETA_O)          # sits on the street pent, stops under the main eave
        H.merge(u)
        LOG.append("walls.udatsu _sode recipe at x=%.2f (y %.2f-%.2f, projects %.2f)" % ((x,) + u.meta["udatsu"]))

    # ======================================================================== RIGHT GABLE x = W (mise, zashiki)
    B.dodai_stones(F_RIGHT_O, 0.0, DO, 21, SILL)
    B.posts_on(F_RIGHT_O, [KEN, KEN + HALF, 2 * KEN, DO], SILL, GTIE)
    s = P("right_lower")
    s.add(box(A_, DO - A_, SILL, FLOOR, -0.0375, 0.0375, "wall_nakanuri", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="infill"))
    rbays = ((0.0, KEN), (KEN, KEN + HALF), (KEN + HALF, 2 * KEN), (2 * KEN, DO))
    for (a, b) in rbays:
        walls.koshiita(s, a + A_, b - A_, 0.90, 0.0375, y0=SILL)
    B.put(s, F_RIGHT_O, what="walls.koshiita h090 (jp_p_wall_koshiita_h090 recipe) on the right gable")
    for (a, b) in rbays:
        win = [(a + A_, b - A_, FLOOR + AMADO_SILL, FLOOR + 2.0)] if a == 2 * KEN else []
        B.wall(F_RIGHT_O, "right_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL, openings_=win)
    s = P("right_grime")
    trim.grime_band(s, A_, DO - A_, 0.0375 + 0.015, y0=SILL)
    B.put(s, F_RIGHT_O)
    # zashiki window: amado storm shutters stowing in a tobukuro over the plain half-ken 1.5-2 ken (mirrored part)
    WINDOWS.append(("zashiki window", F_RIGHT_O, DO, FLOOR, True, openings.part_amado_window("_twin")))

    # ======================================================================== LEFT GABLE x = 0 (toriniwa)
    B.dodai_stones(F_LEFT_O, 0.0, DO, 31, SILL)
    B.posts_on(F_LEFT_O, [KEN, 2 * KEN], SILL, GTIE)
    B.wall(F_LEFT_O, "left_boards", "board_vertical", 0.0, DO, SILL, SILL + 2.0, mat="wood_street_dark",
         grime=[(0.0, DO, POST / 2 + 0.015)])
    B.wall(F_LEFT_O, "left_kokabe", "shinkabe", 0.0, DO, SILL + 2.0, CEIL, head=False)
    s = P("pent_gable")
    roofparts.pent(s, 0.0, DO, GPENT_Y, 0.45, 0.40, "gable")
    B.put(s, F_LEFT_O, what="roofparts.pent gable (jp_p_roof_hisashi_gable recipe, Ioka side pent)")

    # side beams + upper side walls + tile gables (both gables)
    for fr, nm in ((F_LEFT_O, "left"), (F_RIGHT_O, "right")):
        s = P(nm + "_beam")
        s.add(box(-0.06, DO + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="floor_beam"))
        B.put(s, fr)
        B.wall(fr, nm + "_upper", "shinkabe", 0.0, DO, LOFT, GTIE, finish="shikkui", head=False,
             internal_posts=False)
        g = P(nm + "_gable")
        walls.gable(g, DO, T_MAIN, EAVE_O, "_tile")
        B.put(g, fr, what="walls.gable _tile (jp_p_wall_gable_tile recipe)")

    # ======================================================================== OMOYA BACK WALL z = ZB (local x = W - x)
    B.posts_on(F_BACK_O, [0.0, KEN, 2 * KEN, 3 * KEN, W], DOMA, KETA_O)
    B.interior = True
    s = P("back_o_sill")
    s.add(box(-0.06, 3 * KEN + 0.06, DOMA, SILL, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="dodai"))
    s.add(box(A_, 3 * KEN - A_, SILL, FLOOR, -0.0375, 0.0375, "wall_nakanuri_int", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="infill"))
    B.put(s, F_BACK_O)
    B.wall(F_BACK_O, "back_o_rooms", "shinkabe", 0.0, 3 * KEN, FLOOR, CEIL, head_clip=(-1.0, 3 * KEN - POST / 2 - 0.12))
    # toriniwa passage into the kitchen: open, head beam at door height, plaster above
    s = P("back_o_passage")
    s.add(box(3 * KEN + A_, W - A_, DOMA + 2.0, DOMA + 2.0 + walls.HEAD_T, -POST / 2, POST / 2, "wood_weathered",
              vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head_rail"))
    s.add(box(3 * KEN + A_, W - A_, DOMA + 2.0 + walls.HEAD_T, CEIL, -0.0375, 0.0375, "wall_nakanuri_int",
              vis=(1, 2, 3), geo=True, view=True, fire=True, tag="kokabe"))
    B.put(s, F_BACK_O)
    B.interior = False
    s = P("back_o_beam")
    s.add(box(-0.06, W + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="floor_beam"))
    B.put(s, F_BACK_O)
    B.wall(F_BACK_O, "back_o_upper", "shinkabe", 0.0, W, LOFT, KETA_O, finish="shikkui", head=False)
    s = P("keta_back")
    frame.keta(s, -0.30, W + 0.30, z=ZB, y_top=EAVE_O)
    H.merge(s)

    # ======================================================================== ROOM EDGE x = 1 ken (toriniwa side)
    B.interior = True
    # local x = z - ZB: zashiki door [0, 1 ken] parks over [1, 1.5 ken]; mise door [1.5, 2.5 ken] parks over [2.5, 3]
    B.posts_on(F_TORI, [0.0, KEN, KEN + HALF, 2 * KEN + HALF, DO], DOMA, CEIL)
    s = P("tori_edge")
    s.add(box(0.0, DO, DOMA, FLOOR - 0.12, -0.03, 0.03, "wood_sooted", vis=(1, 2, 3), tag="yukashita_boards"))
    s.add(box(0.0, DO, FLOOR - 0.12, FLOOR - 0.10, -0.05, 0.05, "wood_weathered", vis=(1,), tag="kamachi_lip"))
    B.put(s, F_TORI)
    door_bays_tori = [(0.0, "zashiki"), (KEN + HALF, "mise")]
    oc = A_ + (openings.SINGLE_OPEN - openings.STUB) / 2   # centre of the single door's clear opening
    for (a, room) in door_bays_tori:
        B.wall(F_TORI, "tori_door_%s" % room, "shinkabe", a, a + KEN, FLOOR, CEIL,
             openings_=[(a + A_, a + B_, FLOOR, FLOOR + 2.0)])
        B.place_door(shoji_single, F_TORI, a, FLOOR, label="Toriniwa -> %s" % room)
        st = P("step_%s" % room)
        found.step(st, oc, "natural", drop=FLOOR - DOMA, width=1.04)
        B.put(st, F_TORI, a, FLOOR, what="jp_p_found_step_natural (kutsunugi stone, hidden ramp) at the %s" % room)
        # step footprint in the toriniwa (kit frame) for loot / floor checks
        ramp = (FLOOR - DOMA) / math.tan(math.radians(34.0))
        _, z0 = to_world(F_TORI, a + oc - 0.54)
        _, z1 = to_world(F_TORI, a + oc + 0.54)
        FLOORS_OBST.append(("toriniwa", floor_rect(XT - POST / 2 - ramp - 0.05, XT, z0, z1)))
    for (a, b) in ((KEN, KEN + HALF), (2 * KEN + HALF, DO)):
        B.wall(F_TORI, "tori_park_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL)

    # ======================================================================== MISE / ZASHIKI PARTITION z = -1.5 ken
    B.posts_on(F_MID, [2 * KEN, 3 * KEN, 3 * KEN + HALF], FLOOR, CEIL)
    for (a, b) in ((KEN, 2 * KEN), (3 * KEN, 3 * KEN + HALF), (3 * KEN + HALF, W)):
        B.wall(F_MID, "mid_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL,
             head_clip=(KEN + POST / 2 + 0.12, 99.0) if a == KEN else None)
    B.wall(F_MID, "mid_door", "shinkabe", 2 * KEN, 3 * KEN, FLOOR, CEIL, openings_=[(2 * KEN + A_, 3 * KEN - A_, FLOOR,
                                                                                     FLOOR + 2.0)])
    B.place_door(shoji_hikiwake, F_MID, 2 * KEN, FLOOR, label="Mise <-> zashiki")

    # ======================================================================== LOFT FLOOR (sealed, G0-4) + ceiling
    H.merge(FL.loft("loft", 0.0, W, ZB, 0.0, CEIL, LOFT))          # sealed, not walkable (G0-4)
    LOG.append("loft floor: sealed (no stair, no hatch); ceiling boards on joists at 0.91")

    # ======================================================================== FLOORS
    # B4 (2026-09-30): the B1 interior materials replace the stand-ins (tataki doma, tatami + heri, interior boards),
    # and the shop room gets its board display strip (jp_p_fit_mise_floor _455, behind the degoshi lattice)
    B.merge(FL.doma("doma_tori", 0.0, XT, ZB, 0.0, road=(POST / 2, XT - POST / 2, ZB - POST / 2, -POST / 2),
                    y=DOMA, mats=FL.MATS_DOMA_T3))
    B.merge(FL.doma("doma_kitchen", 0.0, XS, ZG, ZB, road=(POST / 2, XS - POST / 2, ZG + POST / 2, ZB - POST / 2),
                    y=DOMA, mats=FL.MATS_DOMA_T3))
    mise = FL.mise("floor_mise", XT + POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2, top=FLOOR, base=DOMA,
                   variant="_455", street="+z", mats_tatami=FL.MATS_TATAMI_B1, mats_boards=FL.MATS_BOARDS_B1)
    B.merge(mise)
    MISE.update(mise.meta["mise"])
    LOG.append("floors.mise _455 (jp_p_fit_mise_floor): board strip %.3f along the street edge, %d mat rows of %.3f, "
               "tatami-yose board %.3f at the back" % (0.455, MISE["rows"], MISE["cell"],
                                                       MISE["yose"][3] - MISE["yose"][2] if MISE["yose"] else 0.0))
    B.merge(FL.tatami("tatami_zashiki", XT + POST / 2, W - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2, top=FLOOR,
                      base=DOMA, mats=FL.MATS_TATAMI_B1))
    B.merge(FL.boards("boards_storage", XS + POST / 2, W - POST / 2, ZG + POST / 2, ZB - POST / 2, STORE,
                      mats=FL.MATS_BOARDS_B1))

    B.interior = False
    # ======================================================================== GEYA (rear lean-to)
    ytop_left = lambda lx: GEYA_EAVE + T_GEYA * lx                     # noqa: E731  local x = z - ZG
    ytop_right = lambda lx: GEYA_EAVE + T_GEYA * (DG - lx)             # noqa: E731  local x = ZB - z
    # back wall z = ZG (local x = W - x): kitchen door [world 0, 1 ken] parks over [1, 1.5 ken] -> mirrored part
    s = P("back_g_lowsill")
    s.add(box(W - KEN - HALF - 0.06, W + 0.06, DOMA - 0.12, DOMA, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3),
              geo=True, view=True, fire=True, tag="dodai"))
    B.put(s, F_BACK_G)
    B.dodai_stones(F_BACK_G, 0.0, W - KEN - HALF - 0.10, 41, SILL)
    B.posts_on(F_BACK_G, [W - KEN - HALF, W - KEN, W], DOMA, KETA_G)
    B.posts_on(F_BACK_G, [0.0, KEN, 2 * KEN], SILL, KETA_G)
    B.wall(F_BACK_G, "back_g_door", "shinkabe", W - KEN, W, DOMA, KETA_G, openings_=[(W - KEN + A_, W - A_, DOMA,
                                                                                        DOMA + 2.0)])
    B.place_door(itado_single, F_BACK_G, W, DOMA, mirror=True, label="Kitchen back door (yard)")
    B.wall(F_BACK_G, "back_g_park", "shinkabe", W - KEN - HALF, W - KEN, DOMA, KETA_G,
         grime=[(W - KEN - HALF + A_, W - KEN - A_, None)])
    B.wall(F_BACK_G, "back_g_win", "shinkabe", 2 * KEN, 2 * KEN + HALF, SILL, KETA_G,
         openings_=[(2 * KEN + A_, 2 * KEN + HALF - A_, DOMA + 0.85, DOMA + 1.70)],
         koshiita=[(2 * KEN + A_, 2 * KEN + HALF - A_, 0.55)], grime=[(2 * KEN + A_, 2 * KEN + HALF - A_, None)])
    # kitchen window: renji bars + a sliding board shutter inside, parking over the back door's park bay (inside face)
    WINDOWS.append(("kitchen window", F_BACK_G, 2 * KEN, DOMA, False, openings.part_window_slide("_board")))
    for (a, b) in ((0.0, KEN), (KEN, 2 * KEN)):
        B.wall(F_BACK_G, "back_g_store_%d" % int(a * 100), "shinkabe", a, b, SILL, KETA_G,
             koshiita=[(a + A_, b - A_, 0.90)], grime=[(a + A_, b - A_, None)])
    # geya gables (sloped tops)
    B.dodai_stones(F_LEFT_G, 0.0, DG, 51, SILL)
    B.dodai_stones(F_RIGHT_G, 0.0, DG, 61, SILL)
    B.posts_on(F_LEFT_G, [KEN], SILL, ytop_left(KEN))
    B.posts_on(F_RIGHT_G, [KEN], SILL, ytop_right(KEN))
    B.sloped_wall(F_LEFT_G, "geya_left", [0.0, KEN, DG], SILL, ytop_left, head_y=SILL + 2.0, koshiita_h=0.90,
                  grime=True)
    B.posts_on(F_RIGHT_G, [KEN + HALF], SILL, SILL + 2.0)
    B.sloped_wall(F_RIGHT_G, "geya_right", [0.0, KEN, DG], SILL, ytop_right, head_y=SILL + 2.0, koshiita_h=0.90,
                  grime=True, window=(KEN + A_, KEN + HALF - A_, TSUKI_Y + 0.90, TSUKI_Y + 1.60))
    # storage window: bars + a top-hinged push-up shutter (tsukiage), high above the koshiita
    WINDOWS.append(("storage window", F_RIGHT_G, KEN, TSUKI_Y, False, openings.part_tsukiage("_board")))
    # kitchen / storage partition x = 2 ken (local x = z - ZG): door [0.5, 1.5 ken] parks over [1.5, 2 ken]
    B.interior = True
    s = P("part_g_sill")
    s.add(box(0.0, DG, DOMA - 0.12, STORE, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="dodai"))
    B.put(s, F_PART_G)
    B.posts_on(F_PART_G, [HALF], STORE, ytop_left(HALF))
    B.posts_on(F_PART_G, [KEN + HALF], STORE, ytop_left(KEN + HALF))
    B.sloped_wall(F_PART_G, "geya_partition", [0.0, HALF, KEN + HALF, DG], STORE, ytop_left, head_y=STORE + 2.0,
                  door_bays=(HALF,), interior="both")
    B.place_door(itado_single, F_PART_G, HALF, STORE, label="Kitchen -> storage")
    kamado(B, POST / 2 + 0.02, POST / 2 + 0.72, ZG + 1.15, ZG + 2.95)
    FLOORS_OBST.append(("kitchen", floor_rect(0.0, POST / 2 + 0.72, ZG + 1.15, ZG + 2.95)))
    B.interior = False
    g, sl_g = leanto.roof("roof_geya", 0.0, W, ZB - POST / 2, ZG, GEYA_EAVE, "sangawara", t=T_GEYA, ov=GEYA_OV,
                          gov=GEYA_GOV, flash_top=KETA_O - 0.02)
    H.merge(g)
    LOG.append("leanto.roof sangawara (roofs.Slope + collision/sheathing/rafters/kawara cover, verges, eave tiles "
               "plain, kawara.ridge flashing strip, hafu boards, frame.keta)")

    # ======================================================================== WINDOWS (animated like doors, after them)
    for (label, fr, dx, dy, mirror, part) in WINDOWS:
        B.place_door(part, fr, dx, dy, mirror=mirror, label=label.capitalize())

    # ======================================================================== MAIN ROOF
    s = P("roof_main")
    sls, info = R.roof(s, W, DO, "kirizuma", "sangawara", eave_y=EAVE_O, courses=5, eave_style="plain")
    H.merge(s)
    LOG.append("roofs.roof kirizuma sangawara 4 x 3 ken, eave line %.2f, 5-course noshi ridge, plain eave tiles, "
               "onigawara, hafu (jp_p_roof_forms_kirizuma + sangawara_* + kawara_ridge_c5 + onigawara + hafu_tile)"
               % EAVE_O)
    H.merge(R.ridge_walk(info))

    # ======================================================================== grime on exterior posts
    for (x, z, y0, y1) in POSTS:
        exterior = (abs(z) < 1e-6 or abs(z - ZG) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
        if exterior:
            B.grime_post(x, z, y0)

    # ======================================================================== LOD policy (building level)
    B.lod_policy()          # Resolution 3 = the exterior shell only; koshiita / board walls one slab from R2

    # ======================================================================== rooms (tags) and floors
    def room(name, tag, floor, level, rect, doors, note=""):
        ROOMS.append({"name": name, "tag": tag, "floor": floor, "level_m": level, "rect_kit": [round(v, 3) for v in rect],
                      "doors": doors, "note": note})
    room("toriniwa", "doma", "earth", DOMA, floor_rect(POST / 2, XT - POST / 2, ZB + POST / 2, -POST / 2), ["DoorsTwin1", "DoorsTwin2",
         "DoorsTwin3"], "entry passage, 1 ken, full omoya depth; two stepping stones hide the 0.45 ramps")
    room("mise", "shop:general", "tatami", FLOOR, floor_rect(XT + POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2),
         ["DoorsTwin3", "DoorsTwin4"], "shop room behind the degoshi / koshi front; board display strip 0.455 along "
         "the street edge (mise-ita), 6 mats, a tatami-yose board at the back")
    room("zashiki", "zashiki", "tatami", FLOOR, floor_rect(XT + POST / 2, W - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2),
         ["DoorsTwin2", "DoorsTwin4"], "best room, koshi window on the side; plain (no tokonoma status features, §2.2); 9 mats")
    room("kitchen", "doma", "earth", DOMA, floor_rect(POST / 2, XS - POST / 2, ZG + POST / 2, ZB - POST / 2),
         ["DoorsTwin5", "DoorsTwin6"], "hashiri-niwa kitchen with the built-in kamado; subtag kitchen")
    room("storage", "storage", "boards", STORE, floor_rect(XS + POST / 2, W - POST / 2, ZG + POST / 2, ZB - POST / 2),
         ["DoorsTwin6"], "monooki, board floor")
    room("loft", "loft", "boards", LOFT, floor_rect(0.0, W, ZB, 0.0), [], "SEALED (G0-4): no access, no loot")
    for r in ROOMS:
        if r["name"] == "loft":
            continue
        obs = [rect for (nm, rect) in FLOORS_OBST if nm == r["name"]]
        FLOORS.append({"name": r["name"], "tag": r["tag"], "rect": tuple(r["rect_kit"]), "y": r["level_m"],
                       "obstacles": obs})
    return H


FLOORS_OBST = []


def centred(H):
    """Kit frame -> model frame: origin at the centre of the wall footprint, grade y 0."""
    return H.transformed(0.0, (-W / 2, 0.0, -ZG / 2))


def to_model_xz(x, z):
    return (x - W / 2, z - ZG / 2)


def model():
    del FLOORS_OBST[:]
    H = build()
    M = centred(H)
    floors = []
    for f in FLOORS:
        x0, x1, z0, z1 = f["rect"]
        a = to_model_xz(x0, z0)
        b = to_model_xz(x1, z1)
        obs = []
        for (o0, o1, p0, p1) in f["obstacles"]:
            c = to_model_xz(o0, p0)
            d = to_model_xz(o1, p1)
            obs.append((min(c[0], d[0]), max(c[0], d[0]), min(c[1], d[1]), max(c[1], d[1])))
        floors.append(dict(f, rect=(min(a[0], b[0]), max(a[0], b[0]), min(a[1], b[1]), max(a[1], b[1])), obstacles=obs))
    rooms = []
    for r in ROOMS:
        x0, x1, z0, z1 = r["rect_kit"]
        a, b = to_model_xz(x0, z0), to_model_xz(x1, z1)
        rooms.append(dict(r, rect_model=[round(min(a[0], b[0]), 3), round(max(a[0], b[0]), 3),
                                          round(min(a[1], b[1]), 3), round(max(a[1], b[1]), 3)]))
    return M, floors, rooms


if __name__ == "__main__":
    M, floors, rooms = model()
    lods = M.lods()
    for l in lods:
        print(core.mlod.lod_name(l.resolution), len(l.faces))
    print(len(M.doors), "doors", [d.twin for d in M.doors])
