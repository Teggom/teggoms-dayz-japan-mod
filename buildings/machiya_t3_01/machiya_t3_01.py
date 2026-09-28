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
import copy
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import core, walls, frame, found, openings, roofs as R, roofparts, trim  # noqa: E402
from jpparts import kawara as K  # noqa: E402
from jpparts.core import Part, box, prism, KEN, HALF, POST, rng_for, add, mul, norm, cross, sub  # noqa: E402
from jpparts.shapes import oriented_box, frame_of, board_run  # noqa: E402

NAME = "jp_machiya_t3_01"
CLASS = "Land_JP_Machiya_T3_01"

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


# ------------------------------------------------------------------------------------------------ helpers
def P(name):
    return Part(name, "", "")


INTERIOR = [False]          # while True, merged solids are interior-only (dropped from Resolution 3)


def merge(H, part):
    n0 = len(H.solids)
    H.merge(part)
    if INTERIOR[0]:
        for s in H.solids[n0:]:
            s.interior = True


def put(H, sub_, fr, dx=0.0, dy=0.0, mirror=False, what=None):
    yaw, o = fr
    off = core.rot_y((dx, 0.0, 0.0), yaw)
    merge(H, sub_.transformed(yaw, (o[0] + off[0], o[1] + dy, o[2] + off[2]), mirror))
    if what:
        LOG.append(what)


def place_door(H, door_part, fr, dx, dy, mirror=False, label=""):
    """A registry door part placed on a wall frame; its twin selection / action point renamed to DoorsTwin<k>."""
    k = len(H.doors) + 1
    dp = copy.copy(door_part)
    dp.solids = [copy.copy(s) for s in door_part.solids]
    dp.memory = dict(door_part.memory)
    dp.doors = [copy.copy(d) for d in door_part.doors]
    old = dp.doors[0].twin
    new = "doorstwin%d" % k
    for s in dp.solids:
        if s.sel == old:
            s.sel = new
    dp.memory[new + "_action"] = dp.memory.pop(old + "_action")
    dp.doors[0].twin = new
    dp.doors[0].label = label
    put(H, dp, fr, dx, dy, mirror, what="%s: %s%s" % (new, door_part.name, " (mirrored)" if mirror else ""))
    return H.doors[-1]


def to_world(fr, lx, lz=0.0):
    yaw, o = fr
    p = core.rot_y((lx, 0.0, lz), yaw)
    return (o[0] + p[0], o[2] + p[2])


def posts_on(H, fr, xs, y0, y1, size=POST):
    for lx in xs:
        x, z = to_world(fr, lx)
        if any(abs(x - a) < 1e-4 and abs(z - b) < 1e-4 for a, b, _, _ in POSTS):
            continue
        POSTS.append((x, z, y0, y1))
        p_ = frame.post(H, x, z=z, y0=y0, y1=y1, size=size)
        if INTERIOR[0]:
            p_.interior = True


def grime_post(H, x, z, y0):
    g = trim.part_grime("_post")
    H.merge(g.transformed(0.0, (x, y0, z)))


def dodai_stones(H, fr, x0, x1, seed):
    """found.dodai_stones (dressed): the sill stays on the wall line; the stone course is set 0.10 outwards so its
    inner face is flush with the inside of the wall (no kerb inside the doma, no stone under a doorway)."""
    s = P("dodai_%d" % seed)
    found.dodai_stones(s, x0, x1, dressed=True, show=0.15, seed=seed)
    s.solids = [x.transformed(0.0, (0.0, 0.0, 0.10)) if x.tag in ("dodai_stone", "dodai_stone_lod") else x
                for x in s.solids]
    put(H, s, fr, 0.0, SILL, what="found.dodai_stones _dressed (jp_p_found_dodai_stones_dressed recipe)")


def wall(H, fr, name, kind, x0, x1, y0, y1, finish="nakanuri", head=True, openings_=(), grime=None, koshiita=None,
         kokabe="plaster", internal_posts=False, mat=None, board_opts=None, thick=None, head_clip=None, interior=None):
    """interior: 'back' = an exterior wall (its -z face looks into a room), 'both' = a partition (default while
    INTERIOR is on), see PLAYBOOK §15 T6: interior faces never use the exterior-weathered earth."""
    if interior is None:
        interior = "both" if INTERIOR[0] else "back"
    s = P(name)
    walls.wall_run(s, kind, x0, x1, y0=y0, y1=y1, openings=openings_, finish=finish, head=head, kokabe=kokabe,
                   internal_posts=internal_posts, mat=mat, board_opts=board_opts, thick=thick, interior=interior)
    if head_clip:
        # a sliding leaf of the perpendicular door line runs 0.07-0.16 in front of the corner post: the head rail
        # (kamoi) of this wall stops short of it
        lo, hi = head_clip
        for i, x in enumerate(s.solids):
            if x.tag == "head_rail":
                b = x.bbox()
                s.solids[i] = box(max(b[0], lo), min(b[1], hi), b[2], b[3], b[4], b[5], "wood_weathered", vis=(1, 2, 3),
                                  geo=True, view=True, fire=True, tag="head_rail").finalize()
    t = walls.FINISH[finish][1] if kind == "shinkabe" else 0.075
    if koshiita:
        for (a, b, h) in koshiita:
            walls.koshiita(s, a, b, h, t / 2, y0=y0)
    if grime:
        for (a, b, face) in grime:
            trim.grime_band(s, a, b, face if face is not None else t / 2 + (0.015 if koshiita else 0.0), y0=y0)
    put(H, s, fr, what="walls.wall_run %s %s (%s)" % (kind, finish if kind == "shinkabe" else (mat or ""), name))


def sloped_wall(H, fr, name, nodes, y0, ytop, mat="wall_nakanuri", t=0.075, head_y=None, door_bays=(),
                koshiita_h=None, grime=False, window=None, interior="back"):
    """Wall under a lean-to verge: infill between post faces from y0 up to the roof line ytop(x) (local x), a head rail
    at head_y, and a sloped wall plate under the roof bed. The shinkabe recipe (walls.wall_run) cut to the roof line.
    interior: 'back' (exterior wall) or 'both' (partition) - the room faces get the interior clay (§15 T6)."""
    mat = walls.interior_mats(mat, interior)
    s = P(name)
    fm = "wood_weathered"
    rng = rng_for(name)
    for i in range(len(nodes) - 1):
        a, b = nodes[i] + POST / 2, nodes[i + 1] - POST / 2
        is_door = any(abs(nodes[i] - d) < 1e-6 for d in door_bays)
        ylo = y0
        if head_y is not None:
            if not is_door:
                holes = [window] if window and abs(window[0] - a) < 1e-6 else []
                for (r0, r1, s0, s1) in walls._split(a, b, y0, head_y, holes):
                    s.add(box(r0, r1, s0, s1, -t / 2, t / 2, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                              tag="infill", uvoff=(rng.random(), rng.random())))
            s.add(box(a, b, head_y, head_y + walls.HEAD_T, -POST / 2, POST / 2, fm, vis=(1, 2, 3), geo=True, view=True,
                      fire=True, tag="head_rail"))
            ylo = head_y + walls.HEAD_T
        poly = [(a, ylo), (b, ylo), (b, ytop(b) - 0.12), (a, ytop(a) - 0.12)]
        s.add(prism(poly, "z", -t / 2, t / 2, mat, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="infill_sloped",
                    uvoff=(rng.random(), rng.random())))
        if koshiita_h and not is_door:
            walls.koshiita(s, a, b, koshiita_h, t / 2, y0=y0)
        if grime and not is_door:
            trim.grime_band(s, a, b, t / 2 + (0.015 if koshiita_h else 0.0), y0=y0)
    x0, x1 = nodes[0] - POST / 2, nodes[-1] + POST / 2
    s.add(prism([(x0, ytop(x0) - 0.12), (x1, ytop(x1) - 0.12), (x1, ytop(x1)), (x0, ytop(x0))], "z", -POST / 2,
                POST / 2, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="wall_plate"))
    put(H, s, fr, what="sloped shinkabe under the geya verge (%s)" % name)


def floor_rect(x0, x1, z0, z1):
    return (min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1))


def open_box(x0, x1, y0, y1, z0, z1, mat, keep, tag, vis=(1,), **kw):
    """Visual-only box without its hidden faces (bottom, butt ends): keep = subset of top/xlo/xhi/zlo/zhi."""
    Q = {"top": ([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0.0, 1.0, 0.0)),
         "xlo": ([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], (-1.0, 0.0, 0.0)),
         "xhi": ([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], (1.0, 0.0, 0.0)),
         "zlo": ([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0.0, 0.0, -1.0)),
         "zhi": ([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0.0, 0.0, 1.0))}
    return core.sheet([Q[k][0] for k in keep], mat, [Q[k][1] for k in keep], vis=vis, tag=tag, **kw)


# ------------------------------------------------------------------------------------------------ tatami
def shugi_layout(nx, nz):
    """Tile an nx x nz grid of half-ken cells with 2x1 mats so that no four mats meet at one point (shugi layout,
    PLAYBOOK §3). Returns [(i0, i1, j0, j1)] cell rectangles."""
    grid = [[-1] * nz for _ in range(nx)]
    mats = []

    def ok_corners():
        for i in range(1, nx):
            for j in range(1, nz):
                c = {grid[i - 1][j - 1], grid[i][j - 1], grid[i - 1][j], grid[i][j]}
                if -1 not in c and len(c) == 4:
                    return False
        return True

    def solve():
        for i in range(nx):
            for j in range(nz):
                if grid[i][j] == -1:
                    for (di, dj) in ((2, 1), (1, 2)):
                        if i + di <= nx and j + dj <= nz and all(grid[a][b] == -1 for a in range(i, i + di)
                                                                 for b in range(j, j + dj)):
                            k = len(mats)
                            for a in range(i, i + di):
                                for b in range(j, j + dj):
                                    grid[a][b] = k
                            mats.append((i, i + di, j, j + dj))
                            if ok_corners() and solve():
                                return True
                            mats.pop()
                            for a in range(i, i + di):
                                for b in range(j, j + dj):
                                    grid[a][b] = -1
                    return False
        return True
    if not solve():
        raise RuntimeError("no shugi layout for %d x %d" % (nx, nz))
    return mats


def tatami_room(H, name, x0, x1, z0, z1):
    """Raised room floor: support block (Geometry), base under the mats, one slab per mat (0.055, straw_mushiro as the
    rush facing - the library has no tatami material yet, see REPORT), heri edges along the long sides (LOD 1), one
    slab in LOD 2/3. Roadway textile_carpet_int at FLOOR."""
    s = P(name)
    s.add(box(x0, x1, DOMA, FLOOR, z0, z1, {"top": "straw_mushiro", "default": "wood_weathered"}, vis=(2, 3), geo=True,
              view=True, fire="wood", tag="floor_lod"))
    s.add(box(x0, x1, DOMA, FLOOR - 0.055, z0, z1, {"top": "wood_sooted", "default": "wood_weathered"}, vis=(1,),
              tag="floor_base"))
    nx, nz = int(round((x1 - x0) / HALF)), int(round((z1 - z0) / HALF))
    cx, cz = (x1 - x0) / nx, (z1 - z0) / nz
    for (i0, i1, j0, j1) in shugi_layout(nx, nz):
        a, b, c, d = x0 + i0 * cx + 0.002, x0 + i1 * cx - 0.002, z0 + j0 * cz + 0.002, z0 + j1 * cz - 0.002
        along_x = (i1 - i0) > (j1 - j0)
        s.add(open_box(a, b, FLOOR - 0.055, FLOOR, c, d, "straw_mushiro", ("top", "xlo", "xhi", "zlo", "zhi"), "tatami",
                       uvrot=0.0 if along_x else 90.0, uvscale=(0.9, 0.9)))
        hw = 0.03
        if along_x:
            for zz in (c, d - hw):
                s.add(open_box(a, b, FLOOR - 0.004, FLOOR + 0.001, zz, zz + hw, "wood_sooted", ("top", "zlo", "zhi"),
                               "heri"))
        else:
            for xx in (a, b - hw):
                s.add(open_box(xx, xx + hw, FLOOR - 0.004, FLOOR + 0.001, c, d, "wood_sooted", ("top", "xlo", "xhi"),
                               "heri"))
    s.road([(x0, FLOOR, z0), (x1, FLOOR, z0), (x1, FLOOR, z1), (x0, FLOOR, z1)], "tatami")
    merge(H, s)


def board_floor(H, name, x0, x1, z0, z1, y, along_x=False):
    s = P(name)
    s.add(box(x0, x1, y - 0.15, y, z0, z1, "wood_weathered", vis=(2, 3), geo=True, view=True, fire="wood",
              tag="floor_lod"))
    rng = rng_for(name)
    a, b = (z0, z1) if along_x else (x0, x1)
    p = a
    while p < b - 1e-4:
        q = min(b, p + rng.uniform(0.20, 0.30))
        if b - q < 0.1:
            q = b
        if along_x:
            s.add(open_box(x0, x1, y - 0.03, y, p + 0.002, q - 0.002, "wood_weathered", ("top", "zlo", "zhi"),
                           "floor_board", uvoff=(rng.random(), rng.random()), uvrot=90.0))
        else:
            s.add(open_box(p + 0.002, q - 0.002, y - 0.03, y, z0, z1, "wood_weathered", ("top", "xlo", "xhi"),
                           "floor_board", uvoff=(rng.random(), rng.random()), uvrot=90.0))
        p = q
    s.add(box(x0, x1, y - 0.15, y - 0.03, z0, z1, "wood_sooted", vis=(1,), tag="floor_base"))
    s.road([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], "boards")
    merge(H, s)


def doma_floor(H, name, x0, x1, z0, z1, rx0, rx1, rz0, rz1):
    s = P(name)
    s.add(box(x0, x1, DOMA - 0.20, DOMA, z0, z1, {"top": "wall_arakabe", "default": "stone_cut"}, vis=(1, 2, 3),
              geo=True, view=True, fire="dirt", tag="doma"))
    s.road([(rx0, DOMA, rz0), (rx1, DOMA, rz0), (rx1, DOMA, rz1), (rx0, DOMA, rz1)], "doma")
    merge(H, s)


# ------------------------------------------------------------------------------------------------ kamado
def kamado(H, x0, x1, z0, z1):
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
    merge(H, s)
    LOG.append("kamado: built-in clay stove from library materials (wall_nakanuri, stone_cut, wood_sooted, metal_iron)")


# ------------------------------------------------------------------------------------------------ roofs
def geya_roof(H):
    """Rear lean-to (geya) in sangawara: the roof generator's Slope / collision / sheathing / rafters / kawara cover with
    verges, a flashing strip against the omoya wall, bargeboards and the eave keta."""
    s = P("roof_geya")
    t, ov, gov = T_GEYA, GEYA_OV, GEYA_GOV
    zw = ZB - POST / 2
    poly = [(-gov, ZG - ov), (-gov, zw), (W + gov, zw), (W + gov, ZG - ov)]
    sl = R.Slope("geya", poly, (0.0, 1.0), (0.0, ZG), (-1.0, 0.0), (W, ZG - ov), GEYA_EAVE, t, ov, True)
    sl.verges = (sl.u_of(W + gov, ZG - ov), sl.u_of(-gov, ZG - ov))
    h_top = R.STACK["sangawara"] + 0.05
    R.collision(s, sl, h_top, "pottery", "tile_roof")
    R.sheathing(s, sl)
    R.tile_bed(s, sl, R.STACK["sangawara"])          # G3 fix: tiles seated on the clay bed (PLAYBOOK §15 T1)
    R.kawara_fascia(s, sl, R.STACK["sangawara"])     # G3 fix: eave board under the eave tiles
    R.rafters(s, sl, only_eave=True)
    # kawara cover as roofs.cover_kawara, but one modelled eave row (the library pent recipe's setting; the lean-to
    # is a deep pent) instead of two: rule 1 keeps the corrugation, eave-tile ends, verge tiles and the top row
    F = sl.frame(R.STACK["sangawara"])
    u0, u1 = sl.u_range()
    vw = 0.13
    fu0, fu1 = sl.verges[0] + vw, sl.verges[1] - vw
    rl = sl.depth_at((u0 + u1) / 2) / sl.cos
    K.field(s, F, fu0, fu1, K.EXPO, rl, rows_eave=1, rows_ridge=1)
    K.eave_tiles(s, F, fu0, fu1, style="plain")
    K.verge(s, F, sl.verges[0], 0.0, rl, -1)
    K.verge(s, F, sl.verges[1], 0.0, rl, +1)
    yw = sl.y(0.0, zw - 0.10, R.STACK["sangawara"]) + 0.02
    K.ridge(s, (-gov, yw, zw - 0.10), (W + gov, yw, zw - 0.10), courses=1, width=0.16, cap_d=0.0001, mortar=True,
            end_tiles=False)
    s.add(box(-gov, W + gov, yw - 0.02, KETA_O - 0.02, zw - 0.03, zw, "wood_weathered", vis=(1, 2), tag="flashing"))
    frame.keta(s, -0.30, W + 0.30, z=ZG, y_top=GEYA_EAVE)
    for x, sg in ((-gov, -1.0), (W + gov, 1.0)):
        a = (x, sl.y(x, ZG - ov, R.STACK["sangawara"]) - 0.02, ZG - ov)
        b = (x, sl.y(x, zw, R.STACK["sangawara"]) + 0.02, zw)
        d, e1, e2 = frame_of(sub(b, a))
        up = norm(cross((1.0, 0.0, 0.0), d))
        if up[1] < 0:
            up = mul(up, -1.0)
        c = add(tuple((a[k] + b[k]) / 2 for k in range(3)), mul(up, -0.12 + 0.03))
        L = math.dist(a, b)
        s.add(oriented_box(add(c, (sg * 0.015, 0.0, 0.0)), d, up, (1.0, 0.0, 0.0), L / 2 + 0.03, 0.12, 0.015,
                           "wood_weathered", vis=(1, 2, 3), tag="hafu"))
    H.merge(s)
    LOG.append("roofs.Slope + collision/sheathing/rafters/cover_kawara (sangawara lean-to, verges, eave tiles plain), "
               "kawara.ridge flashing strip, hafu boards, frame.keta")
    return sl


def ridge_walk(H, info):
    """A collision + Roadway strip over the main ridge stack so rooftop players walk the ridge instead of clipping it."""
    (xr0, yr, zr), (xr1, _, _) = info["ridge"]
    s = P("ridge_walk")
    top = yr + 0.14
    s.add(box(xr0 + 0.05, xr1 - 0.05, yr - 0.30, top, zr - 0.14, zr + 0.14, "roof_kawara", vis=(), geo=True, view=True,
              fire="pottery", tag="ridge_geo"))
    s.road([(xr0 + 0.05, top, zr - 0.12), (xr1 - 0.05, top, zr - 0.12), (xr1 - 0.05, top, zr + 0.12),
            (xr0 + 0.05, top, zr + 0.12)], "tile_roof")
    H.merge(s)


def udatsu(H, x):
    """Plastered udatsu wing wall on the pent at a party-wall line (walls.part_udatsu _sode recipe, sized to sit on
    the street pent and stop under the main eave)."""
    s = P("udatsu_%d" % int(x * 100))
    y0, y1, zp = PENT_Y - 0.25, KETA_O - 0.33, 0.50
    s.add(box(x - 0.09, x + 0.09, y0, y1, 0.0, zp, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="udatsu"))
    s.add(box(x - 0.10, x + 0.10, y0 - 0.05, y0, -0.02, zp + 0.02, "wall_shikkui", vis=(1, 2), tag="udatsu_foot"))
    walls.kawara_cap(s, (x, y1, -0.05), (x, y1, zp + 0.10), width=0.30)
    H.merge(s)
    LOG.append("walls.udatsu _sode recipe at x=%.2f (y %.2f-%.2f, projects %.2f)" % (x, y0, y1, zp))


# ------------------------------------------------------------------------------------------------ build
def build():
    del ROOMS[:], FLOORS[:], POSTS[:], LOG[:], WINDOWS[:]
    INTERIOR[0] = False
    H = Part(NAME, "", "buildings", tiers=[3], used_for="tier-3 Kamigata town machiya (Ioka type)")
    H.wear = "_w1"
    itado_twin = openings.part_itado("_twin")          # hikichigai: the main entrance only (PLAYBOOK §15 T3)
    itado_single = openings.part_itado("_single")      # katabiki: back and kitchen doors
    shoji_single = openings.part_shoji_ext("_single")  # katabiki: the room entrances off the toriniwa
    shoji_hikiwake = openings.part_shoji_ext("_hikiwake")   # hikiwake: the mise / zashiki shoji pair

    # ======================================================================== STREET FRONT (z = 0)
    # base: low sill over the entrance + park bays (door tracks at doma level), dodai on dressed stones elsewhere
    s = P("front_lowsill")
    frame.dodai(s, -0.06, KEN + HALF + 0.06, z=0.0, y_top=DOMA)
    H.merge(s)
    dodai_stones(H, F_FRONT, KEN + HALF + 0.10, W, 11)
    posts_on(H, F_FRONT, [0.0, KEN, KEN + HALF], DOMA, KETA_O)
    posts_on(H, F_FRONT, [2 * KEN, 3 * KEN, W], SILL, KETA_O)
    # B1 entrance (twin itado, parks stacked over B2a), B2a plain park bay, B2b koshi window, B3-B4 degoshi shop front
    wall(H, F_FRONT, "front_b1", "shinkabe", 0.0, KEN, DOMA, CEIL, openings_=[(A_, B_, DOMA, DOMA + 2.0)])
    place_door(H, itado_twin, F_FRONT, 0.0, DOMA, label="Entrance (street)")
    wall(H, F_FRONT, "front_b2a", "shinkabe", KEN, KEN + HALF, DOMA, CEIL, grime=[(KEN + A_, KEN + HALF - A_, None)])
    wall(H, F_FRONT, "front_b2b", "shinkabe", KEN + HALF, 2 * KEN, SILL, CEIL,
         openings_=[(KEN + HALF + A_, 2 * KEN - A_, SILL + 0.45, SILL + 2.0)],
         koshiita=[(KEN + HALF + A_, 2 * KEN - A_, 0.39)], grime=[(KEN + HALF + A_, 2 * KEN - A_, None)])
    # street window: koshi lattice + a sliding shoji panel inside, parking over the plain half-ken B2a (mirrored)
    WINDOWS.append(("street window", F_FRONT, 2 * KEN, SILL, True, openings.part_window_slide("_shoji")))
    for k in (2, 3):
        x0 = k * KEN
        wall(H, F_FRONT, "front_b%d" % (k + 1), "shinkabe", x0, x0 + KEN, SILL, CEIL,
             openings_=[(x0 + A_, x0 + B_, SILL + 0.39, SILL + 2.0)], koshiita=[(x0 + A_, x0 + B_, 0.33)],
             grime=[(x0 + A_, x0 + B_, None)])
        put(H, openings.part_koshi("_degoshi"), F_FRONT, x0, SILL, what="jp_p_open_koshi_degoshi (shop front)")
    # floor beam, upper street wall with oval mushiko, keta, street pent, udatsu
    H.add(box(-0.06, W + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="floor_beam"))
    wall(H, F_FRONT, "front_up_b1", "okabe", 0.0, KEN, LOFT, KETA_O, finish="shikkui", thick=0.15)
    for k in (1, 2, 3):
        put(H, openings.part_mushiko("_oval"), F_FRONT, k * KEN, LOFT, what="jp_p_open_mushiko_oval")
    s = P("keta_front")
    frame.keta(s, -0.30, W + 0.30, z=0.0, y_top=EAVE_O)
    H.merge(s)
    s = P("pent_front")
    roofparts.pent(s, 0.09, W - 0.09, PENT_Y, 0.91, 0.40, "tile")
    H.merge(s)
    LOG.append("roofparts.pent tile (jp_p_roof_hisashi_tile recipe) over the street front")
    udatsu(H, 0.0)
    udatsu(H, W)

    # ======================================================================== RIGHT GABLE x = W (mise, zashiki)
    dodai_stones(H, F_RIGHT_O, 0.0, DO, 21)
    posts_on(H, F_RIGHT_O, [KEN, KEN + HALF, 2 * KEN, DO], SILL, GTIE)
    s = P("right_lower")
    s.add(box(A_, DO - A_, SILL, FLOOR, -0.0375, 0.0375, "wall_nakanuri", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="infill"))
    rbays = ((0.0, KEN), (KEN, KEN + HALF), (KEN + HALF, 2 * KEN), (2 * KEN, DO))
    for (a, b) in rbays:
        walls.koshiita(s, a + A_, b - A_, 0.90, 0.0375, y0=SILL)
    put(H, s, F_RIGHT_O, what="walls.koshiita h090 (jp_p_wall_koshiita_h090 recipe) on the right gable")
    for (a, b) in rbays:
        win = [(a + A_, b - A_, FLOOR + AMADO_SILL, FLOOR + 2.0)] if a == 2 * KEN else []
        wall(H, F_RIGHT_O, "right_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL, openings_=win)
    s = P("right_grime")
    trim.grime_band(s, A_, DO - A_, 0.0375 + 0.015, y0=SILL)
    put(H, s, F_RIGHT_O)
    # zashiki window: amado storm shutters stowing in a tobukuro over the plain half-ken 1.5-2 ken (mirrored part)
    WINDOWS.append(("zashiki window", F_RIGHT_O, DO, FLOOR, True, openings.part_amado_window("_twin")))

    # ======================================================================== LEFT GABLE x = 0 (toriniwa)
    dodai_stones(H, F_LEFT_O, 0.0, DO, 31)
    posts_on(H, F_LEFT_O, [KEN, 2 * KEN], SILL, GTIE)
    wall(H, F_LEFT_O, "left_boards", "board_vertical", 0.0, DO, SILL, SILL + 2.0, mat="wood_street_dark",
         grime=[(0.0, DO, POST / 2 + 0.015)])
    wall(H, F_LEFT_O, "left_kokabe", "shinkabe", 0.0, DO, SILL + 2.0, CEIL, head=False)
    s = P("pent_gable")
    roofparts.pent(s, 0.0, DO, GPENT_Y, 0.45, 0.40, "gable")
    put(H, s, F_LEFT_O, what="roofparts.pent gable (jp_p_roof_hisashi_gable recipe, Ioka side pent)")

    # side beams + upper side walls + tile gables (both gables)
    for fr, nm in ((F_LEFT_O, "left"), (F_RIGHT_O, "right")):
        s = P(nm + "_beam")
        s.add(box(-0.06, DO + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="floor_beam"))
        put(H, s, fr)
        wall(H, fr, nm + "_upper", "shinkabe", 0.0, DO, LOFT, GTIE, finish="shikkui", head=False,
             internal_posts=False)
        g = P(nm + "_gable")
        walls.gable(g, DO, T_MAIN, EAVE_O, "_tile")
        put(H, g, fr, what="walls.gable _tile (jp_p_wall_gable_tile recipe)")

    # ======================================================================== OMOYA BACK WALL z = ZB (local x = W - x)
    posts_on(H, F_BACK_O, [0.0, KEN, 2 * KEN, 3 * KEN, W], DOMA, KETA_O)
    INTERIOR[0] = True
    s = P("back_o_sill")
    s.add(box(-0.06, 3 * KEN + 0.06, DOMA, SILL, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="dodai"))
    s.add(box(A_, 3 * KEN - A_, SILL, FLOOR, -0.0375, 0.0375, "wall_nakanuri_int", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="infill"))
    put(H, s, F_BACK_O)
    wall(H, F_BACK_O, "back_o_rooms", "shinkabe", 0.0, 3 * KEN, FLOOR, CEIL, head_clip=(-1.0, 3 * KEN - POST / 2 - 0.12))
    # toriniwa passage into the kitchen: open, head beam at door height, plaster above
    s = P("back_o_passage")
    s.add(box(3 * KEN + A_, W - A_, DOMA + 2.0, DOMA + 2.0 + walls.HEAD_T, -POST / 2, POST / 2, "wood_weathered",
              vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head_rail"))
    s.add(box(3 * KEN + A_, W - A_, DOMA + 2.0 + walls.HEAD_T, CEIL, -0.0375, 0.0375, "wall_nakanuri_int",
              vis=(1, 2, 3), geo=True, view=True, fire=True, tag="kokabe"))
    put(H, s, F_BACK_O)
    INTERIOR[0] = False
    s = P("back_o_beam")
    s.add(box(-0.06, W + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="floor_beam"))
    put(H, s, F_BACK_O)
    wall(H, F_BACK_O, "back_o_upper", "shinkabe", 0.0, W, LOFT, KETA_O, finish="shikkui", head=False)
    s = P("keta_back")
    frame.keta(s, -0.30, W + 0.30, z=ZB, y_top=EAVE_O)
    H.merge(s)

    # ======================================================================== ROOM EDGE x = 1 ken (toriniwa side)
    INTERIOR[0] = True
    # local x = z - ZB: zashiki door [0, 1 ken] parks over [1, 1.5 ken]; mise door [1.5, 2.5 ken] parks over [2.5, 3]
    posts_on(H, F_TORI, [0.0, KEN, KEN + HALF, 2 * KEN + HALF, DO], DOMA, CEIL)
    s = P("tori_edge")
    s.add(box(0.0, DO, DOMA, FLOOR - 0.12, -0.03, 0.03, "wood_sooted", vis=(1, 2, 3), tag="yukashita_boards"))
    s.add(box(0.0, DO, FLOOR - 0.12, FLOOR - 0.10, -0.05, 0.05, "wood_weathered", vis=(1,), tag="kamachi_lip"))
    put(H, s, F_TORI)
    door_bays_tori = [(0.0, "zashiki"), (KEN + HALF, "mise")]
    oc = A_ + (openings.SINGLE_OPEN - openings.STUB) / 2   # centre of the single door's clear opening
    for (a, room) in door_bays_tori:
        wall(H, F_TORI, "tori_door_%s" % room, "shinkabe", a, a + KEN, FLOOR, CEIL,
             openings_=[(a + A_, a + B_, FLOOR, FLOOR + 2.0)])
        place_door(H, shoji_single, F_TORI, a, FLOOR, label="Toriniwa -> %s" % room)
        st = P("step_%s" % room)
        found.step(st, oc, "natural", drop=FLOOR - DOMA, width=1.04)
        put(H, st, F_TORI, a, FLOOR, what="jp_p_found_step_natural (kutsunugi stone, hidden ramp) at the %s" % room)
        # step footprint in the toriniwa (kit frame) for loot / floor checks
        ramp = (FLOOR - DOMA) / math.tan(math.radians(34.0))
        _, z0 = to_world(F_TORI, a + oc - 0.54)
        _, z1 = to_world(F_TORI, a + oc + 0.54)
        FLOORS_OBST.append(("toriniwa", floor_rect(XT - POST / 2 - ramp - 0.05, XT, z0, z1)))
    for (a, b) in ((KEN, KEN + HALF), (2 * KEN + HALF, DO)):
        wall(H, F_TORI, "tori_park_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL)

    # ======================================================================== MISE / ZASHIKI PARTITION z = -1.5 ken
    posts_on(H, F_MID, [2 * KEN, 3 * KEN, 3 * KEN + HALF], FLOOR, CEIL)
    for (a, b) in ((KEN, 2 * KEN), (3 * KEN, 3 * KEN + HALF), (3 * KEN + HALF, W)):
        wall(H, F_MID, "mid_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL,
             head_clip=(KEN + POST / 2 + 0.12, 99.0) if a == KEN else None)
    wall(H, F_MID, "mid_door", "shinkabe", 2 * KEN, 3 * KEN, FLOOR, CEIL, openings_=[(2 * KEN + A_, 3 * KEN - A_, FLOOR,
                                                                                     FLOOR + 2.0)])
    place_door(H, shoji_hikiwake, F_MID, 2 * KEN, FLOOR, label="Mise <-> zashiki")

    # ======================================================================== LOFT FLOOR (sealed, G0-4) + ceiling
    s = P("loft")
    s.add(box(0.0, W, CEIL, LOFT, ZB, 0.0, "wood_weathered", vis=(2, 3), geo=True, view=True, fire="wood",
              tag="loft_lod"))
    s.add(box(0.0, W, CEIL + 0.08, LOFT, ZB, 0.0, {"bottom": "wood_weathered", "default": "wood_weathered"}, vis=(1,),
              tag="loft_boards"))
    x = HALF
    while x < W - 0.1:
        s.add(box(x - 0.03, x + 0.03, CEIL, CEIL + 0.08, ZB, 0.0, "wood_weathered", vis=(1,), tag="sao_joist",
                  grain="long"))
        x += HALF
    H.merge(s)
    LOG.append("loft floor: sealed (no stair, no hatch); ceiling boards on joists at 0.91")

    # ======================================================================== FLOORS
    doma_floor(H, "doma_tori", 0.0, XT, ZB, 0.0, POST / 2, XT - POST / 2, ZB - POST / 2, -POST / 2)
    doma_floor(H, "doma_kitchen", 0.0, XS, ZG, ZB, POST / 2, XS - POST / 2, ZG + POST / 2, ZB - POST / 2)
    tatami_room(H, "tatami_mise", XT + POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2)
    tatami_room(H, "tatami_zashiki", XT + POST / 2, W - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2)
    board_floor(H, "boards_storage", XS + POST / 2, W - POST / 2, ZG + POST / 2, ZB - POST / 2, STORE)

    INTERIOR[0] = False
    # ======================================================================== GEYA (rear lean-to)
    ytop_left = lambda lx: GEYA_EAVE + T_GEYA * lx                     # noqa: E731  local x = z - ZG
    ytop_right = lambda lx: GEYA_EAVE + T_GEYA * (DG - lx)             # noqa: E731  local x = ZB - z
    # back wall z = ZG (local x = W - x): kitchen door [world 0, 1 ken] parks over [1, 1.5 ken] -> mirrored part
    s = P("back_g_lowsill")
    s.add(box(W - KEN - HALF - 0.06, W + 0.06, DOMA - 0.12, DOMA, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3),
              geo=True, view=True, fire=True, tag="dodai"))
    put(H, s, F_BACK_G)
    dodai_stones(H, F_BACK_G, 0.0, W - KEN - HALF - 0.10, 41)
    posts_on(H, F_BACK_G, [W - KEN - HALF, W - KEN, W], DOMA, KETA_G)
    posts_on(H, F_BACK_G, [0.0, KEN, 2 * KEN], SILL, KETA_G)
    wall(H, F_BACK_G, "back_g_door", "shinkabe", W - KEN, W, DOMA, KETA_G, openings_=[(W - KEN + A_, W - A_, DOMA,
                                                                                        DOMA + 2.0)])
    place_door(H, itado_single, F_BACK_G, W, DOMA, mirror=True, label="Kitchen back door (yard)")
    wall(H, F_BACK_G, "back_g_park", "shinkabe", W - KEN - HALF, W - KEN, DOMA, KETA_G,
         grime=[(W - KEN - HALF + A_, W - KEN - A_, None)])
    wall(H, F_BACK_G, "back_g_win", "shinkabe", 2 * KEN, 2 * KEN + HALF, SILL, KETA_G,
         openings_=[(2 * KEN + A_, 2 * KEN + HALF - A_, DOMA + 0.85, DOMA + 1.70)],
         koshiita=[(2 * KEN + A_, 2 * KEN + HALF - A_, 0.55)], grime=[(2 * KEN + A_, 2 * KEN + HALF - A_, None)])
    # kitchen window: renji bars + a sliding board shutter inside, parking over the back door's park bay (inside face)
    WINDOWS.append(("kitchen window", F_BACK_G, 2 * KEN, DOMA, False, openings.part_window_slide("_board")))
    for (a, b) in ((0.0, KEN), (KEN, 2 * KEN)):
        wall(H, F_BACK_G, "back_g_store_%d" % int(a * 100), "shinkabe", a, b, SILL, KETA_G,
             koshiita=[(a + A_, b - A_, 0.90)], grime=[(a + A_, b - A_, None)])
    # geya gables (sloped tops)
    dodai_stones(H, F_LEFT_G, 0.0, DG, 51)
    dodai_stones(H, F_RIGHT_G, 0.0, DG, 61)
    posts_on(H, F_LEFT_G, [KEN], SILL, ytop_left(KEN))
    posts_on(H, F_RIGHT_G, [KEN], SILL, ytop_right(KEN))
    sloped_wall(H, F_LEFT_G, "geya_left", [0.0, KEN, DG], SILL, ytop_left, head_y=SILL + 2.0, koshiita_h=0.90,
                grime=True)
    posts_on(H, F_RIGHT_G, [KEN + HALF], SILL, SILL + 2.0)
    sloped_wall(H, F_RIGHT_G, "geya_right", [0.0, KEN, DG], SILL, ytop_right, head_y=SILL + 2.0, koshiita_h=0.90,
                grime=True, window=(KEN + A_, KEN + HALF - A_, TSUKI_Y + 0.90, TSUKI_Y + 1.60))
    # storage window: bars + a top-hinged push-up shutter (tsukiage), high above the koshiita
    WINDOWS.append(("storage window", F_RIGHT_G, KEN, TSUKI_Y, False, openings.part_tsukiage("_board")))
    # kitchen / storage partition x = 2 ken (local x = z - ZG): door [0.5, 1.5 ken] parks over [1.5, 2 ken]
    INTERIOR[0] = True
    s = P("part_g_sill")
    s.add(box(0.0, DG, DOMA - 0.12, STORE, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="dodai"))
    put(H, s, F_PART_G)
    posts_on(H, F_PART_G, [HALF], STORE, ytop_left(HALF))
    posts_on(H, F_PART_G, [KEN + HALF], STORE, ytop_left(KEN + HALF))
    sloped_wall(H, F_PART_G, "geya_partition", [0.0, HALF, KEN + HALF, DG], STORE, ytop_left, head_y=STORE + 2.0,
                door_bays=(HALF,), interior="both")
    place_door(H, itado_single, F_PART_G, HALF, STORE, label="Kitchen -> storage")
    kamado(H, POST / 2 + 0.02, POST / 2 + 0.72, ZG + 1.15, ZG + 2.95)
    FLOORS_OBST.append(("kitchen", floor_rect(0.0, POST / 2 + 0.72, ZG + 1.15, ZG + 2.95)))
    INTERIOR[0] = False
    sl_g = geya_roof(H)

    # ======================================================================== WINDOWS (animated like doors, after them)
    for (label, fr, dx, dy, mirror, part) in WINDOWS:
        place_door(H, part, fr, dx, dy, mirror=mirror, label=label.capitalize())

    # ======================================================================== MAIN ROOF
    s = P("roof_main")
    sls, info = R.roof(s, W, DO, "kirizuma", "sangawara", eave_y=EAVE_O, courses=5, eave_style="plain")
    H.merge(s)
    LOG.append("roofs.roof kirizuma sangawara 4 x 3 ken, eave line %.2f, 5-course noshi ridge, plain eave tiles, "
               "onigawara, hafu (jp_p_roof_forms_kirizuma + sangawara_* + kawara_ridge_c5 + onigawara + hafu_tile)"
               % EAVE_O)
    ridge_walk(H, info)

    # ======================================================================== grime on exterior posts
    for (x, z, y0, y1) in POSTS:
        exterior = (abs(z) < 1e-6 or abs(z - ZG) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
        if exterior:
            grime_post(H, x, z, y0)

    # ======================================================================== LOD policy (building level)
    # Resolution 3 = the exterior shell only; koshiita / board walls show as one slab from Resolution 2 on
    for s_ in H.solids:
        if getattr(s_, "interior", False) and 3 in s_.vis:
            s_.vis = set(s_.vis) - {3}
        if s_.tag == "board" and set(s_.vis) == {1, 2}:
            s_.vis = {1}
        if s_.tag in ("koshiita_lod", "board_lod") and set(s_.vis) == {3}:
            s_.vis = {2, 3}

    # ======================================================================== rooms (tags) and floors
    def room(name, tag, floor, level, rect, doors, note=""):
        ROOMS.append({"name": name, "tag": tag, "floor": floor, "level_m": level, "rect_kit": [round(v, 3) for v in rect],
                      "doors": doors, "note": note})
    room("toriniwa", "doma", "earth", DOMA, floor_rect(POST / 2, XT - POST / 2, ZB + POST / 2, -POST / 2), ["DoorsTwin1", "DoorsTwin2",
         "DoorsTwin3"], "entry passage, 1 ken, full omoya depth; two stepping stones hide the 0.45 ramps")
    room("mise", "shop:general", "tatami", FLOOR, floor_rect(XT + POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2),
         ["DoorsTwin3", "DoorsTwin4"], "shop room behind the degoshi / koshi front; 9 mats")
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
