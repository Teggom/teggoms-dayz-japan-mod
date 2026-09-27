"""Parametric machiya (Kyoto-style town house) generator.

generate(params) -> Model with:
  solids   convex Solids tagged with the LODs they belong to (visual 1-3, Geometry, View, Fire) and door bones
  roadway  walkable faces [(points, surface)]
  memory   {selection: [points]} (door axes, action points, leaf centres)
  doors    door records (config + model.cfg data)
  floors   loot floors: rectangles + obstacles

Model space: x right, y up, z forward; +z = street front. Origin = centre of the footprint at ground level
(y = 0 = grade). autocenter = 0 keeps this origin, so a placement at ground height puts the house on the ground.
The toriniwa (earthen passage) is generated on the +x side and the whole model is mirrored for side='west'.
"""
import copy
import math

from .geom import Solid, box, prism, hexa

KEN = 1.82
EXT = 0.14          # exterior wall thickness
INT = 0.10          # interior partition thickness
GAP = 0.012         # air gap between a wall face and a sliding leaf
OV = 0.02           # leaf overlap past each jamb
BASE = -0.30        # foundations / floor blocks go this far below grade (hides small terrain dips)

DEFAULTS = {
    "name": "jp_machiya_01",
    "class": "Land_JP_Machiya_01",
    "width_ken": 4.0,
    "depth_ken": 6.0,
    "storeys": 2,
    "toriniwa_ken": 1.0,
    "toriniwa_side": "east",
    # rooms along the depth, front (street) to back
    "rooms": [
        {"ken": 2.0, "floor": "tatami", "toriniwa_door": True},
        {"ken": 2.0, "floor": "boards", "toriniwa_door": True, "irori": True, "stair": True},
        {"ken": 2.0, "floor": "tatami", "toriniwa_door": False, "window_back": True},
    ],
    "link_doors": [True, True],          # fusuma between room i and i+1
    "roof": "kirizuma",
    "roof_pitch": 0.45,                  # rise / run (about 24 degrees, Kyoto machiya are shallow)
    "eave_overhang": 0.90,
    "gable_overhang": 0.30,
    "hisashi": True,                     # tiled pent roof over the ground-floor street front
    "walls": "white",                    # exterior plaster: white | earth
    "interior_walls": "earth",
    "lower_walls": "boards",             # exterior skirting: boards | plaster
    "front": "koshi",                    # ground-floor street front of the rooms: koshi lattice
    "upper_front": "mushiko",            # slatted upper windows
    "kamado": True,
    "floor_doma": 0.05,
    "floor_room": 0.45,
    "ceiling_1": 2.95,                   # underside of the upper floor
    "floor_upper": 3.10,
    "eave_2": 5.30,                      # wall-plate height, 2 storeys
    "eave_1": 3.05,                      # wall-plate height, 1 storey
    "door_h": 2.00,                      # interior door opening height above its floor
    "door_h_ext": 2.00,
    "door_w": 1.00,                      # interior openings (vanilla doors are ~1.2 x 2.2 m; real shoji ~0.9 x 1.76)
    "stair_width": 0.90,
    "stair_angle": 40.0,                 # of the step line; the walkable ramp over the nosings is a bit flatter
    "mass": 60000.0,
}


def plaster(p, which):
    w = p["walls"] if which == "ext" else p["interior_walls"]
    return "plaster_white" if w == "white" else "plaster_earth"


class Door:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class Model:
    def __init__(self, params):
        self.params = params
        self.solids = []
        self.roadway = []
        self.memory = {}
        self.doors = []
        self.floors = []
        self.notes = []

    def add(self, s):
        self.solids.append(s)
        return s


# ------------------------------------------------------------------------------------------------------
# wall helpers
# ------------------------------------------------------------------------------------------------------
def _split(s0, s1, y0, y1, openings):
    """Rectangle [s0,s1]x[y0,y1] minus opening rects [(a0,a1,b0,b1)] -> list of rects (a0,a1,b0,b1)."""
    out = []
    ops = sorted(openings)
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


def wall_along_x(m, z, thick, x0, x1, y0, y1, openings, face_plus, face_minus, vis=(1, 2), fire="dirt",
                 tag="wall", geo=True):
    """Wall in a constant-z plane running along x. face_plus = material of the +z face."""
    mats = {"front": face_plus, "back": face_minus, "default": "timber"}
    for a0, a1, b0, b1 in _split(x0, x1, y0, y1, openings):
        m.add(box(a0, a1, b0, b1, z - thick / 2, z + thick / 2, mats, vis=vis, geo=geo, view=geo, fire=fire,
                  tag=tag))


def wall_along_z(m, x, thick, z0, z1, y0, y1, openings, face_plus, face_minus, vis=(1, 2), fire="dirt",
                 tag="wall", geo=True):
    """Wall in a constant-x plane running along z. face_plus = material of the +x face."""
    mats = {"right": face_plus, "left": face_minus, "default": "timber"}
    for a0, a1, b0, b1 in _split(z0, z1, y0, y1, openings):
        m.add(box(x - thick / 2, x + thick / 2, b0, b1, a0, a1, mats, vis=vis, geo=geo, view=geo, fire=fire,
                  tag=tag))


def gable_triangle(m, x, thick, zf, zb, y_eave, pitch, mats, vis=(1, 2, 3), tag="gable"):
    """Triangle wall above the eave line, top edges on the roof underside (ridge at z = 0)."""
    half = (zf - zb) / 2.0
    zc = (zf + zb) / 2.0
    poly = [(y_eave, zb), (y_eave, zf), (y_eave + half * pitch, zc)]
    m.add(prism(poly, "x", x - thick / 2, x + thick / 2, mats, vis=vis, geo=True, view=True, fire="dirt", tag=tag))


# ------------------------------------------------------------------------------------------------------
# doors
# ------------------------------------------------------------------------------------------------------
def sliding_door(m, kind, wall_axis, wall_pos, wall_thick, s0, s1, y0, height, side, direction, span, note):
    """Add one sliding leaf.

    wall_axis 'x': the wall runs along x at z = wall_pos; 'z': runs along z at x = wall_pos.
    [s0, s1]: the opening along the wall. side = +1/-1: which face of the wall the leaf runs on.
    direction = +1/-1: slide direction along the wall. span = (lo, hi) clear run for the leaf along the wall.
    """
    idx = len(m.doors) + 1
    bone = "doors%d" % idx
    lt = 0.04 if kind == "plank" else 0.03
    off = side * (wall_thick / 2 + GAP + lt / 2)
    l0, l1 = s0 - OV, s1 + OV
    width = l1 - l0
    top = y0 + height + 0.03
    bot = y0 + 0.004
    o0, o1 = l0 + direction * width, l1 + direction * width
    if o0 < span[0] - 1e-3 or o1 > span[1] + 1e-3:
        raise ValueError("door %s: open leaf [%.2f, %.2f] leaves the clear span [%.2f, %.2f] (%s)"
                         % (bone, o0, o1, span[0], span[1], note))
    tex = {"plank": "plank_door", "shoji": "shoji", "fusuma": "fusuma"}[kind]
    fire = "wood" if kind == "plank" else "fabric_thin"
    if wall_axis == "x":
        z = wall_pos + off
        leaf = box(l0, l1, bot, top, z - lt / 2, z + lt / 2, {"front": tex, "back": tex, "default": "timber"},
                   vis=(1, 2, 3), geo=True, view=True, fire=fire, door=bone, uv="fit", tag="door")
        centre = ((l0 + l1) / 2, (bot + top) / 2, z)
        dvec = (direction * 1.0, 0.0, 0.0)
        action = ((s0 + s1) / 2, y0 + 1.0, wall_pos)
    else:
        x = wall_pos + off
        leaf = box(x - lt / 2, x + lt / 2, bot, top, l0, l1, {"right": tex, "left": tex, "default": "timber"},
                   vis=(1, 2, 3), geo=True, view=True, fire=fire, door=bone, uv="fit", tag="door")
        centre = (x, (bot + top) / 2, (l0 + l1) / 2)
        dvec = (0.0, 0.0, direction * 1.0)
        action = (wall_pos, y0 + 1.0, (s0 + s1) / 2)
    m.add(leaf)
    # rails: sill and lintel tracks under / over both leaf positions (visual only)
    r0, r1 = min(l0, o0), max(l1, o1)
    tw = lt + 2 * GAP + 0.01
    if wall_axis == "x":
        zc = wall_pos + side * (wall_thick / 2 + tw / 2)
        m.add(box(r0, r1, top - 0.005, top + 0.045, zc - tw / 2, zc + tw / 2, "timber", vis=(1,), tag="rail"))
    else:
        xc = wall_pos + side * (wall_thick / 2 + tw / 2)
        m.add(box(xc - tw / 2, xc + tw / 2, top - 0.005, top + 0.045, r0, r1, "timber", vis=(1,), tag="rail"))
    axis0 = centre
    axis1 = (centre[0] + dvec[0], centre[1] + dvec[1], centre[2] + dvec[2])
    m.memory[bone + "_axis"] = [axis0, axis1]
    m.memory[bone + "_action"] = [action]
    m.memory[bone] = [centre]
    sounds = "doorWoodSlide"
    d = Door(index=idx, bone=bone, cfg="Doors%d" % idx, kind=kind, width=width, slide=width,
             axis_len=1.0, leaf=leaf, centre=centre, direction=dvec, action=action,
             sound_open=sounds + "Open", sound_close=sounds + "Close", sound_locked=sounds + "Rattle",
             sound_openabit=sounds + "OpenABit", anim_period=1.0 if kind == "plank" else 0.8,
             init_opened=0.3 if kind == "plank" else 0.5, note=note, display="%s door" % kind)
    m.doors.append(d)
    return d


# ------------------------------------------------------------------------------------------------------
# the generator
# ------------------------------------------------------------------------------------------------------
def generate(user_params=None):
    p = copy.deepcopy(DEFAULTS)
    p.update(user_params or {})
    if p["roof"] != "kirizuma":
        raise ValueError("only roof='kirizuma' (gable, ridge parallel to the street) is implemented")
    total = sum(r["ken"] for r in p["rooms"])
    if abs(total - p["depth_ken"]) > 1e-6:
        raise ValueError("room depths (%.2f ken) must add up to depth_ken (%.2f)" % (total, p["depth_ken"]))
    m = Model(p)
    W = p["width_ken"] * KEN
    D = p["depth_ken"] * KEN
    X0, X1 = -W / 2, W / 2
    Z0, Z1 = -D / 2, D / 2
    XT = X1 - p["toriniwa_ken"] * KEN
    two = p["storeys"] == 2
    FD, FR = p["floor_doma"], p["floor_room"]
    C1 = p["ceiling_1"] if two else None
    FU = p["floor_upper"] if two else None
    EV = p["eave_2"] if two else p["eave_1"]
    TOPG = C1 if two else EV          # top of the ground-floor interior partitions
    pitch = p["roof_pitch"]
    ext_pl = plaster(p, "ext")
    int_pl = plaster(p, "int")
    ex_in_x = (X0 + EXT / 2, X1 - EXT / 2)     # inner faces of the party walls
    ex_in_z = (Z0 + EXT / 2, Z1 - EXT / 2)     # inner faces of front / back walls
    m.dims = dict(W=W, D=D, X0=X0, X1=X1, Z0=Z0, Z1=Z1, XT=XT, FD=FD, FR=FR, C1=C1, FU=FU, EV=EV)

    # ---------------- rooms along z (front -> back) ----------------
    rooms = []
    zf = Z1
    for i, r in enumerate(p["rooms"]):
        zb = zf - r["ken"] * KEN
        rooms.append(dict(r, i=i, zf=zf, zb=zb,
                          in_zf=zf - (EXT / 2 if i == 0 else INT / 2),
                          in_zb=zb + (EXT / 2 if i == len(p["rooms"]) - 1 else INT / 2)))
        zf = zb
    stair_room = None
    for r in rooms:
        if r.get("stair"):
            stair_room = r
    if stair_room is not None and not two:
        raise ValueError("a stair needs storeys = 2")
    if two and stair_room is None:
        raise ValueError("storeys = 2 needs one room with stair = True")

    rx0, rx1 = X0 + EXT / 2, XT - INT / 2          # room column inner x range
    tx0, tx1 = XT + INT / 2, X1 - EXT / 2          # toriniwa inner x range

    # ---------------- stair geometry (computed early: doors and slab depend on it) ----------------
    st = None
    if stair_room is not None:
        rise = FU - FR
        run = rise / math.tan(math.radians(p["stair_angle"]))
        nsteps = max(8, int(round(rise / 0.22)))
        g = run / nsteps
        r_step = rise / nsteps
        x_b = rx1 - 0.75                             # front edge of the first step (bottom, next to the toriniwa)
        x_t = x_b - run                              # the stair meets the upper floor here
        sz0 = stair_room["in_zb"]
        sz1 = sz0 + p["stair_width"]
        ramp_foot = x_b + g                          # walkable ramp runs over the step nosings
        slope = rise / (ramp_foot - x_t)
        # stairwell must start where head room under the slab drops below 2.05 m
        x_head = ramp_foot - ((C1 - 2.05) - FR) / slope
        hole_x1 = min(x_head + 0.10, rx1 - 0.3)
        st = dict(rise=rise, run=run, n=nsteps, g=g, r=r_step, x_b=x_b, x_t=x_t, z0=sz0, z1=sz1,
                  foot=ramp_foot, slope=slope, angle=math.degrees(math.atan(slope)), hole=(x_t, hole_x1, sz0, sz1))
        if x_t < rx0 + 0.9:
            raise ValueError("stair does not fit: top at x=%.2f" % x_t)
        m.stair = st

    # ---------------- floors: doma, rooms, aprons ----------------
    # doma block (earthen floor) - geometry + visual share it
    m.add(box(XT, X1, BASE, FD, Z0, Z1, {"top": "doma", "default": "stone"}, vis=(1, 2), geo=True, view=False,
              fire="dirt", tag="floor"))
    m.roadway.append(([(tx0, FD, Z0 - EXT / 2), (tx1, FD, Z0 - EXT / 2), (tx1, FD, Z1 + EXT / 2),
                       (tx0, FD, Z1 + EXT / 2)], "doma"))
    # stone aprons outside the entrance (front, under the eaves) and the back door
    for zz0, zz1 in ((Z1 + EXT / 2, Z1 + 0.85), (Z0 - 0.65, Z0 - EXT / 2)):
        m.add(box(XT, X1, BASE, FD, zz0, zz1, "stone", vis=(1, 2, 3), geo=True, view=False, fire="granite",
                  tag="apron"))
        m.roadway.append(([(tx0 - 0.02, FD, zz0), (tx1 + 0.02, FD, zz0), (tx1 + 0.02, FD, zz1),
                           (tx0 - 0.02, FD, zz1)], "stone_ext"))
    # stone plinth under the whole house (visual, the part above grade shows under the walls)
    for (a0, a1, b0, b1) in ((X0 - EXT / 2 - 0.03, X1 + EXT / 2 + 0.03, Z1 - EXT / 2 - 0.03, Z1 + EXT / 2 + 0.03),
                             (X0 - EXT / 2 - 0.03, X1 + EXT / 2 + 0.03, Z0 - EXT / 2 - 0.03, Z0 + EXT / 2 + 0.03),
                             (X0 - EXT / 2 - 0.03, X0 + EXT / 2 + 0.03, Z0 + EXT / 2 + 0.03, Z1 - EXT / 2 - 0.03),
                             (X1 - EXT / 2 - 0.03, X1 + EXT / 2 + 0.03, Z0 + EXT / 2 + 0.03, Z1 - EXT / 2 - 0.03)):
        m.add(box(a0, a1, BASE, 0.10, b0, b1, "stone", vis=(1, 2, 3), tag="plinth"))

    for r in rooms:
        fl = r["floor"]
        # geometry block: solid up to the walking height
        m.add(box(X0, XT, BASE, FR, r["zb"], r["zf"], "timber", vis=(), geo=True, view=True, fire="wood",
                  tag="floor"))
        # visual block: 6 cm lower, covered by mats / boards
        m.add(box(X0, XT, BASE, FR - 0.06, r["zb"], r["zf"], {"top": "boards_floor", "default": "timber"},
                  vis=(1, 2), tag="floor"))
        m.roadway.append(([(rx0, FR, r["in_zb"]), (XT + INT / 2, FR, r["in_zb"]), (XT + INT / 2, FR, r["in_zf"]),
                           (rx0, FR, r["in_zf"])], "tatami" if fl == "tatami" else "boards"))
        holes = []
        if r.get("irori"):
            cx = (rx0 + rx1) / 2 + 0.2
            zlo = st["z1"] if (st and r is stair_room) else r["in_zb"]
            cz = (zlo + r["in_zf"]) / 2
            hs = 0.45
            holes.append((cx - hs, cx + hs, cz - hs, cz + hs))
            r["irori_rect"] = holes[-1]
            # hearth: frame, ash, a kettle hook is left out
            m.add(box(cx - hs, cx + hs, FR - 0.06, FR - 0.035, cz - hs, cz + hs, "ash", vis=(1, 2), tag="irori"))
            fw = 0.09
            for (a0, a1, b0, b1) in ((cx - hs, cx + hs, cz - hs, cz - hs + fw), (cx - hs, cx + hs, cz + hs - fw, cz + hs),
                                     (cx - hs, cx - hs + fw, cz - hs + fw, cz + hs - fw),
                                     (cx + hs - fw, cx + hs, cz - hs + fw, cz + hs - fw)):
                m.add(box(a0, a1, FR - 0.06, FR + 0.005, b0, b1, "timber", vis=(1, 2), tag="irori"))
            # embers / pot stand
            m.add(box(cx - 0.12, cx + 0.12, FR - 0.035, FR - 0.01, cz - 0.12, cz + 0.12, "timber", vis=(1,),
                      tag="irori"))
        _floor_cover(m, r, rx0, rx1, FR, holes)
        # loot floor
        obst = []
        if r.get("irori_rect"):
            obst.append(r["irori_rect"])
        if st and r is stair_room:
            obst.append((st["x_t"] - 0.05, st["foot"] + 0.35, st["z0"], st["z1"] + 0.05))
        m.floors.append(dict(name="room%d" % (r["i"] + 1), rect=(rx0, rx1, r["in_zb"], r["in_zf"]), y=FR,
                             obstacles=obst))

    # ---------------- exterior walls ----------------
    lower = "boards_ext" if p["lower_walls"] == "boards" else ext_pl
    ex_top = EV
    # front wall (street) - door at the toriniwa, the rest solid (lattice is a visual overlay)
    span_t = (tx0 + GAP, tx1 - GAP)
    leaf_w = (span_t[1] - span_t[0]) / 2.0
    # entrance_at 'party': opening at the party-wall end of the toriniwa, the leaf slides towards the rooms;
    # 'rooms': opening next to the rooms, the leaf slides towards the party wall
    if p.get("entrance_at", "party") == "party":
        fdoor = (span_t[1] - leaf_w + OV, span_t[1] - OV)
        edir = -1
    else:
        fdoor = (span_t[0] + OV, span_t[0] + leaf_w - OV)
        edir = +1
    front_open = [(fdoor[0], fdoor[1], FD, FD + p["door_h_ext"])]
    wall_along_x(m, Z1, EXT, X0 - EXT / 2, X1 + EXT / 2, BASE, ex_top, front_open, ext_pl, int_pl, vis=(1, 2, 3),
                 tag="ext_front")
    back_open = [(fdoor[0], fdoor[1], FD, FD + p["door_h_ext"])]
    wall_along_x(m, Z0, EXT, X0 - EXT / 2, X1 + EXT / 2, BASE, ex_top, back_open, int_pl, ext_pl, vis=(1, 2, 3),
                 tag="ext_back")
    # party walls (gable ends)
    wall_along_z(m, X0, EXT, Z0 + EXT / 2, Z1 - EXT / 2, BASE, ex_top, [], int_pl, ext_pl, vis=(1, 2, 3),
                 tag="ext_west")
    wall_along_z(m, X1, EXT, Z0 + EXT / 2, Z1 - EXT / 2, BASE, ex_top, [], ext_pl, int_pl, vis=(1, 2, 3),
                 tag="ext_east")
    gable_triangle(m, X0, EXT, Z1 + EXT / 2, Z0 - EXT / 2, ex_top, pitch, {"left": ext_pl, "right": int_pl,
                                                                          "default": "timber"}, tag="ext_west")
    gable_triangle(m, X1, EXT, Z1 + EXT / 2, Z0 - EXT / 2, ex_top, pitch, {"right": ext_pl, "left": int_pl,
                                                                          "default": "timber"}, tag="ext_east")

    # front + back doors (plank itado), leaves inside, sliding towards the rooms side
    sliding_door(m, "plank", "x", Z1, EXT, fdoor[0], fdoor[1], FD, p["door_h_ext"], -1, edir, span_t, "front entrance")
    sliding_door(m, "plank", "x", Z0, EXT, fdoor[0], fdoor[1], FD, p["door_h_ext"], +1, edir, span_t, "back door")
    m.floors.append(dict(name="toriniwa", rect=(tx0, tx1, ex_in_z[0], ex_in_z[1]), y=FD, obstacles=[]))
    toriniwa_floor = m.floors[-1]

    # ---------------- toriniwa partition (x = XT) with shoji into rooms ----------------
    xt_openings = []
    for r in rooms:
        if not r.get("toriniwa_door"):
            continue
        zlo = st["z1"] + 0.05 if (st and r is stair_room) else r["in_zb"]
        at = r.get("toriniwa_door_at", 0.5)            # door position: fraction of the free wall, back -> front
        half = p["door_w"] / 2 + 0.1
        cz = min(max(zlo + at * (r["in_zf"] - zlo), zlo + half), r["in_zf"] - half)
        o0, o1 = cz - p["door_w"] / 2, cz + p["door_w"] / 2
        r["tdoor"] = (o0, o1)
        xt_openings.append((o0, o1, FR, FR + p["door_h"]))
    wall_top_xt = EV if two else TOPG
    wall_along_z(m, XT, INT, ex_in_z[0], ex_in_z[1], BASE, wall_top_xt, xt_openings, int_pl, int_pl, vis=(1, 2),
                 tag="int_xt")
    if two:
        gable_triangle(m, XT, INT, ex_in_z[1], ex_in_z[0], EV, pitch, int_pl, vis=(1, 2), tag="int_xt")
    for r in rooms:
        if "tdoor" not in r:
            continue
        o0, o1 = r["tdoor"]
        # leaf on the room side (-x), slides towards the longer free run of the wall
        # the leaf runs 6 cm off the wall, clear of the stair (whose ramp ends 0.5 m from this wall)
        lo, hi = r["in_zb"] + GAP, r["in_zf"] - GAP
        room_side_span = (lo, hi)
        leaf_w = (o1 - o0) + 2 * OV
        direction = +1 if (hi - (o1 + OV)) >= leaf_w else -1
        sliding_door(m, "shoji", "z", XT, INT, o0, o1, FR, p["door_h"], -1, direction, room_side_span,
                     "toriniwa -> room%d" % (r["i"] + 1))
        # hidden walkable ramp + visible stepping stone (kutsunugi-ishi) in the toriniwa
        rz0, rz1 = o0 - 0.05, o1 + 0.05
        ramp = prism([(tx0, FR), (tx0, FD), (tx0 + 0.6, FD)], "z", rz0, rz1, "stone", vis=(), geo=True, view=False,
                     fire=None, tag="ramp")
        m.add(ramp)
        m.roadway.append(([(tx0, FR, rz0), (tx0 + 0.6, FD, rz0), (tx0 + 0.6, FD, rz1), (tx0, FR, rz1)], "stone_ext"))
        m.add(box(tx0 + 0.06, tx0 + 0.52, FD, 0.25, o0 + 0.05, o1 - 0.05, "stone", vis=(1, 2), tag="step_stone"))
        toriniwa_floor["obstacles"].append((tx0, tx0 + 0.65, rz0, rz1))

    # ---------------- partitions between rooms (z = const) with fusuma ----------------
    for i in range(len(rooms) - 1):
        ra, rb = rooms[i], rooms[i + 1]          # ra in front, rb behind
        z = ra["zb"]
        openings = []
        ld = p["link_doors"][i]
        if ld is not False and ld is not None:
            if st and ra is stair_room:
                # this is the wall the stair runs along: use the free end beyond the stair top
                o0 = rx0 + 0.12
            else:
                # True = centred; a number = fraction across the rooms column (0 = party wall, 1 = toriniwa)
                at = 0.5 if ld is True else float(ld)
                cxm = rx0 + at * (rx1 - rx0)
                cxm = min(max(cxm, rx0 + p["door_w"] / 2 + 0.1), rx1 - p["door_w"] / 2 - 0.1)
                o0 = cxm - p["door_w"] / 2
            o1 = o0 + p["door_w"]
            openings.append((o0, o1, FR, FR + p["door_h"]))
        wall_along_x(m, z, INT, rx0 - 0.0, rx1 + 0.0, FR - 0.06, TOPG, openings, int_pl, int_pl, vis=(1, 2),
                     tag="int_part")
        if openings:
            o0, o1 = openings[0][0], openings[0][1]
            # leaf on the side of the room without the stair
            side = -1 if rb is not stair_room else +1
            if ra is stair_room:
                side = -1
            leaf_w = (o1 - o0) + 2 * OV
            direction = +1 if (rx1 - GAP - (o1 + OV)) >= leaf_w else -1
            sliding_door(m, "fusuma", "x", z, INT, o0, o1, FR, p["door_h"], side, direction,
                         (rx0 + GAP, rx1 - GAP), "room%d <-> room%d" % (ra["i"] + 1, rb["i"] + 1))

    # ---------------- kamado (clay stove) against the partition, where no shoji is ----------------
    if p["kamado"]:
        free = [r for r in rooms if not r.get("toriniwa_door")]
        if free:
            r = free[-1]
            kz0, kz1 = r["in_zb"] + 0.9, min(r["in_zb"] + 2.3, r["in_zf"] - 0.2)
            if kz1 - kz0 > 0.8:
                kx0, kx1 = tx0, tx0 + 0.62
                m.add(box(kx0, kx1, FD, 0.72, kz0, kz1, {"top": "plaster_earth", "default": "plaster_earth"},
                          vis=(1, 2), geo=True, view=True, fire="dirt", tag="kamado"))
                for k in range(2):
                    zc = kz0 + (kz1 - kz0) * (0.27 + 0.46 * k)
                    m.add(box(kx0 + 0.13, kx1 - 0.13, 0.72, 0.745, zc - 0.18, zc + 0.18, "ash", vis=(1,),
                              tag="kamado"))
                    m.add(box(kx1 - 0.001, kx1 + 0.004, 0.12, 0.40, zc - 0.14, zc + 0.14, "ash", vis=(1,),
                              tag="kamado"))
                toriniwa_floor["obstacles"].append((kx0, kx1 + 0.1, kz0, kz1))

    # ---------------- upper floor ----------------
    if two:
        hx0, hx1, hz0, hz1 = st["hole"]
        slab_mats = {"top": "boards_floor", "bottom": "boards_ext", "default": "timber"}
        pieces = [(X0, XT, hz1, Z1), (X0, XT, Z0, hz0), (X0, hx0, hz0, hz1), (hx1, XT, hz0, hz1)]
        for (a0, a1, b0, b1) in pieces:
            m.add(box(a0, a1, C1, FU, b0, b1, slab_mats, vis=(1, 2), geo=True, view=True, fire="wood", tag="slab"))
        # roadway on the upper floor (inner area, per piece)
        for (a0, a1, b0, b1) in pieces:
            a0c, a1c = max(a0, rx0), min(a1, rx1)
            b0c, b1c = max(b0, ex_in_z[0]), min(b1, ex_in_z[1])
            m.roadway.append(([(a0c, FU, b0c), (a1c, FU, b0c), (a1c, FU, b1c), (a0c, FU, b1c)], "boards"))
        # stairwell railing (posts + rail), a geometry blocker along the open edges
        rail_h = 0.95
        for (a0, a1, b0, b1) in ((hx0 + 0.3, hx1 + 0.03, hz1, hz1 + 0.05), (hx1, hx1 + 0.05, hz0, hz1 + 0.05)):
            m.add(box(a0, a1, FU, FU + rail_h, b0, b1, "timber", vis=(), geo=True, view=False, fire="wood",
                      tag="railing"))
            m.add(box(a0, a1, FU + rail_h - 0.06, FU + rail_h, b0, b1, "timber", vis=(1, 2), tag="railing"))
            m.add(box(a0, a1, FU + 0.35, FU + 0.39, b0, b1, "timber", vis=(1,), tag="railing"))
        for (x, z) in ((hx0 + 0.32, hz1 + 0.025), (hx1 + 0.025, hz1 + 0.025), (hx1 + 0.025, hz0 + 0.03),
                       ((hx0 + hx1) / 2, hz1 + 0.025)):
            m.add(box(x - 0.03, x + 0.03, FU, FU + rail_h, z - 0.03, z + 0.03, "timber", vis=(1,), tag="railing"))
        # upper partition above the stair room's back wall, fusuma on the back side
        zp = stair_room["zb"]
        yb = EV + (D / 2 - abs(zp)) * pitch
        o0 = rx0 + 0.12
        o1 = o0 + p["door_w"]
        wall_along_x(m, zp, INT, rx0, rx1, FU, yb, [(o0, o1, FU, FU + p["door_h"])], int_pl, int_pl, vis=(1, 2),
                     tag="upper_part")
        leaf_w = (o1 - o0) + 2 * OV
        sliding_door(m, "fusuma", "x", zp, INT, o0, o1, FU, p["door_h"], -1, +1, (rx0 + GAP, rx1 - GAP),
                     "upper front <-> upper back")
        m.floors.append(dict(name="upper_front", rect=(rx0, rx1, zp + INT / 2, ex_in_z[1]), y=FU,
                             obstacles=[(hx0 - 0.1, hx1 + 0.1, hz0 - 0.1, hz1 + 0.1)]))
        m.floors.append(dict(name="upper_back", rect=(rx0, rx1, ex_in_z[0], zp - INT / 2), y=FU, obstacles=[]))
        # the stair
        _stair(m, st, FR, FU)

    # ---------------- roof ----------------
    _roof(m, p, X0, X1, Z0, Z1, EV, pitch)
    if p["hisashi"] and two:
        _hisashi(m, p, X0, X1, Z1, C1)

    # ---------------- visual detail: posts, beams, cladding, windows, lattice ----------------
    _details(m, p, rooms, X0, X1, Z0, Z1, XT, FD, FR, C1, FU, EV, two, lower, ext_pl, fdoor)

    if p["toriniwa_side"] == "west":
        _mirror_x(m)
    return m


# ------------------------------------------------------------------------------------------------------
def _floor_cover(m, r, rx0, rx1, FR, holes):
    """Tatami mats or floor boards over the 6 cm recess of a room block (visual only)."""
    z0, z1 = r["in_zb"], r["in_zf"]
    if r["floor"] == "tatami":
        # lay mats 0.91 x 1.82 in rows across x; last row / column trimmed to fit
        L, S = KEN, KEN / 2
        z = z0
        row = 0
        while z < z1 - 1e-3:
            zz = min(z + S, z1)
            x = rx0 + (S if row % 2 else 0.0)   # staggered rows
            if row % 2:
                m.add(box(rx0, rx0 + S, FR - 0.06, FR, z, zz, "tatami", vis=(1, 2),
                          uv=("rect", 0.0, 0.0, 0.5, 0.5 * (zz - z) / S), tag="tatami"))
            while x < rx1 - 1e-3:
                xx = min(x + L, rx1)
                frac = (xx - x) / L
                m.add(box(x, xx, FR - 0.06, FR, z, zz, "tatami", vis=(1, 2),
                          uv=("rect", 0.0, 0.0, frac, 0.5 * (zz - z) / S), tag="tatami"))
                x = xx
            z = zz
            row += 1
    else:
        # boards around the holes (one hole max)
        rects = [(rx0, rx1, z0, z1)]
        for (hx0, hx1, hz0, hz1) in holes:
            new = []
            for (a0, a1, b0, b1) in rects:
                if hx1 <= a0 or hx0 >= a1 or hz1 <= b0 or hz0 >= b1:
                    new.append((a0, a1, b0, b1))
                    continue
                if hz0 > b0:
                    new.append((a0, a1, b0, hz0))
                if hz1 < b1:
                    new.append((a0, a1, hz1, b1))
                if hx0 > a0:
                    new.append((a0, hx0, max(b0, hz0), min(b1, hz1)))
                if hx1 < a1:
                    new.append((hx1, a1, max(b0, hz0), min(b1, hz1)))
            rects = new
        for (a0, a1, b0, b1) in rects:
            m.add(box(a0, a1, FR - 0.06, FR, b0, b1, {"top": "boards_floor", "default": "timber"}, vis=(1, 2),
                      tag="boards"))


def _stair(m, st, FR, FU):
    z0, z1 = st["z0"], st["z1"]
    # visual: the box stair (hako-kaidan) - a stack of cabinets, each from the floor to its tread
    for i in range(st["n"]):
        xa = st["x_b"] - (i + 1) * st["g"]
        xb = st["x_b"] - i * st["g"]
        top = FR + (i + 1) * st["r"]
        m.add(box(xa, xb, FR - 0.06, top, z0, z1, {"top": "boards_floor", "default": "tansu"}, vis=(1,),
                  uv="world", tag="stair"))
    # simplified stair for resolution 2: two blocks
    mid = st["n"] // 2
    for (i0, i1) in ((0, mid), (mid, st["n"])):
        xa = st["x_b"] - i1 * st["g"]
        xb = st["x_b"] - i0 * st["g"]
        m.add(box(xa, xb, FR - 0.06, FR + i1 * st["r"], z0, z1, {"top": "boards_floor", "default": "tansu"},
                  vis=(2,), tag="stair"))
    # collision / walk ramp over the nosings
    poly = [(st["foot"], FR), (st["x_t"], FR), (st["x_t"], FU)]
    m.add(prism(poly, "z", z0, z1, "timber", vis=(), geo=True, view=True, fire="wood", tag="stair_ramp"))
    m.roadway.append(([(st["foot"], FR, z0), (st["x_t"], FU, z0), (st["x_t"], FU, z1), (st["foot"], FR, z1)],
                      "stair"))


def _roof(m, p, X0, X1, Z0, Z1, EV, pitch):
    D = Z1 - Z0
    ov, gov = p["eave_overhang"], p["gable_overhang"]
    t = 0.22
    xl, xr = X0 - EXT / 2 - gov, X1 + EXT / 2 + gov

    def yb(z):
        return EV + (D / 2 - abs(z)) * pitch

    mats = {"top": "kawara", "bottom": "boards_ext", "default": "timber"}
    for sgn in (+1, -1):
        ze = sgn * (D / 2 + ov)
        c = [(xl, yb(0), 0.0), (xr, yb(0), 0.0), (xr, yb(ze), ze), (xl, yb(ze), ze)]
        corners = c + [(x, y + t, z) for (x, y, z) in c]
        m.add(hexa(corners, mats, vis=(1, 2, 3), geo=True, view=True, fire="pottery", tag="roof"))
        # eave tile row (noki-gawara) and verge boards (hafu), visual
        ye = yb(ze)
        m.add(box(xl, xr, ye - 0.05, ye + t + 0.06, ze - 0.10 if sgn > 0 else ze, ze if sgn > 0 else ze + 0.10,
                  "kawara_ridge", vis=(1, 2), tag="roof_detail"))
        for xv in (xl, xr):
            dx = 0.06 if xv == xr else -0.06
            vc = [(xv, yb(0) - 0.12, 0.0), (xv + dx, yb(0) - 0.12, 0.0), (xv + dx, yb(ze) - 0.12, ze),
                  (xv, yb(ze) - 0.12, ze)]
            m.add(hexa(vc + [(x, y + t + 0.14, z) for (x, y, z) in vc], "timber", vis=(1, 2), tag="roof_detail"))
    # ridge (munagawara) + ogre tiles (onigawara)
    ytop = yb(0) + t
    m.add(box(xl + 0.05, xr - 0.05, ytop - 0.12, ytop + 0.28, -0.20, 0.20,
              {"top": "kawara_ridge", "default": "kawara_ridge"}, vis=(1, 2, 3), geo=True, view=True, fire="pottery",
              tag="roof"))
    m.add(box(xl + 0.05, xr - 0.05, ytop + 0.28, ytop + 0.36, -0.12, 0.12, "kawara_ridge", vis=(1, 2),
              tag="roof_detail"))
    for xo in (xl - 0.02, xr - 0.12):
        m.add(box(xo, xo + 0.14, ytop - 0.15, ytop + 0.55, -0.26, 0.26, "kawara_ridge", vis=(1,), tag="roof_detail"))
    # wall plates (keta) on the front and back walls close the gap under the roof
    for z in (Z1, Z0):
        m.add(box(X0 - EXT / 2, X1 + EXT / 2, EV - 0.22, EV + 0.06, z - 0.12, z + 0.12, "timber", vis=(1, 2, 3),
                  tag="beam"))
    # exposed rafters under the eaves (visual)
    n = int((xr - xl) / 0.45)
    for k in range(n + 1):
        x = xl + 0.1 + k * (xr - xl - 0.2) / n
        for sgn in (+1, -1):
            z_in, z_out = sgn * (D / 2 - 0.05), sgn * (D / 2 + ov - 0.05)
            rc = [(x - 0.035, yb(z_in) - 0.09, z_in), (x + 0.035, yb(z_in) - 0.09, z_in),
                  (x + 0.035, yb(z_out) - 0.09, z_out), (x - 0.035, yb(z_out) - 0.09, z_out)]
            m.add(hexa(rc + [(a, b + 0.09, c) for (a, b, c) in rc], "timber", vis=(1,), tag="rafter"))


def _hisashi(m, p, X0, X1, Z1, C1):
    """Tiled pent roof over the ground-floor street front, between the floors."""
    ov = 0.85
    y_in = C1 + 0.10
    y_out = y_in - ov * 0.35
    t = 0.12
    c = [(X0 - EXT / 2, y_in, Z1 + EXT / 2), (X1 + EXT / 2, y_in, Z1 + EXT / 2), (X1 + EXT / 2, y_out, Z1 + ov),
         (X0 - EXT / 2, y_out, Z1 + ov)]
    m.add(hexa(c + [(x, y + t, z) for (x, y, z) in c], {"top": "kawara", "bottom": "boards_ext", "default": "timber"},
               vis=(1, 2, 3), geo=True, view=True, fire="pottery", tag="hisashi"))
    m.add(box(X0 - EXT / 2, X1 + EXT / 2, y_out - 0.03, y_out + t + 0.05, Z1 + ov - 0.09, Z1 + ov, "kawara_ridge",
              vis=(1, 2), tag="hisashi"))
    # small brackets
    for x in (X0 + 0.2, (X0 + X1) / 2, X1 - 0.2):
        m.add(box(x - 0.04, x + 0.04, y_in - 0.25, y_in, Z1 + EXT / 2, Z1 + ov - 0.1, "timber", vis=(1,),
                  tag="hisashi"))


def door_sweeps(m):
    """Bounding boxes swept by every leaf between closed and open (x0,x1,y0,y1,z0,z1)."""
    out = []
    for d in m.doors:
        x0, x1, y0, y1, z0, z1 = d.leaf.bbox()
        dx, dz = d.direction[0] * d.slide, d.direction[2] * d.slide
        out.append((min(x0, x0 + dx), max(x1, x1 + dx), y0, y1, min(z0, z0 + dz), max(z1, z1 + dz)))
    return out


def _hits(b, sweeps, pad=0.005):
    for s in sweeps:
        if (b[0] < s[1] + pad and b[1] > s[0] - pad and b[2] < s[3] + pad and b[3] > s[2] - pad
                and b[4] < s[5] + pad and b[5] > s[4] - pad):
            return True
    return False


def _details(m, p, rooms, X0, X1, Z0, Z1, XT, FD, FR, C1, FU, EV, two, lower, ext_pl, fdoor):
    ken = KEN
    P = 0.16            # post size
    sweeps = door_sweeps(m)

    def post(b, vis):
        if not _hits(b, sweeps):
            m.add(box(b[0], b[1], b[2], b[3], b[4], b[5], "timber", vis=vis, tag="post"))

    # facade posts at every ken + corners, front and back
    nx = int(round((X1 - X0) / ken))
    for k in range(nx + 1):
        x = X0 + k * ken
        for z, vis in ((Z1, (1, 2, 3)), (Z0, (1,))):
            post((x - P / 2, x + P / 2, 0.10, EV - 0.2, z - P / 2, z + P / 2), vis)
    # side-wall posts (visible inside and outside) and the toriniwa-side posts, every ken
    nz = int(round((Z1 - Z0) / ken))
    for k in range(1, nz):
        z = Z0 + k * ken
        for x in (X0, X1):
            post((x - P / 2, x + P / 2, 0.10, EV - 0.2, z - P / 2, z + P / 2), (1,))
        post((XT - 0.07, XT + 0.07, FD, EV - 0.2, z - 0.07, z + 0.07), (1,))
    # horizontal beams: the storey beam across the facade and back, and inside the toriniwa void
    if two:
        for z, vis in ((Z1, (1, 2, 3)), (Z0, (1, 2))):
            m.add(box(X0 - EXT / 2 - 0.01, X1 + EXT / 2 + 0.01, C1 - 0.22, C1 + 0.02, z - 0.09, z + 0.09, "timber",
                      vis=vis, tag="beam"))
        for k in range(1, nz):
            z = Z0 + k * ken
            m.add(box(XT, X1, C1 + 0.25, C1 + 0.55, z - 0.13, z + 0.13, "timber", vis=(1,), tag="beam"))
    # lower exterior skirting boards (koshi-ita) on the front, back and sides
    sk = 0.012
    y0, y1 = 0.10, 0.85
    rx0 = X0 + EXT / 2
    segs_front = [(X0 - EXT / 2, XT), (XT, fdoor[0]), (fdoor[1], X1 + EXT / 2)]
    for (a0, a1) in segs_front:
        m.add(box(a0, a1, y0, y1, Z1 + EXT / 2, Z1 + EXT / 2 + sk, lower, vis=(1, 2, 3), tag="clad"))
    for (a0, a1) in ((X0 - EXT / 2, fdoor[0]), (fdoor[1], X1 + EXT / 2)):
        m.add(box(a0, a1, y0, y1, Z0 - EXT / 2 - sk, Z0 - EXT / 2, lower, vis=(1, 2), tag="clad"))
    m.add(box(X1 + EXT / 2, X1 + EXT / 2 + sk, y0, y1, Z0 - EXT / 2, Z1 + EXT / 2, lower, vis=(1, 2), tag="clad"))
    m.add(box(X0 - EXT / 2 - sk, X0 - EXT / 2, y0, y1, Z0 - EXT / 2, Z1 + EXT / 2, lower, vis=(1, 2), tag="clad"))
    # --- koshi lattice across the rooms part of the street front, and next to the entrance ---
    lat_y0, lat_y1 = y1 + 0.02, 2.20
    zf = Z1 + EXT / 2
    bays = []
    xk = X0
    while xk < XT - 1e-3:                      # one lattice bay per ken between the facade posts
        bays.append((xk + P / 2 + 0.01, min(xk + ken, XT) - P / 2 - 0.01))
        xk += ken
    if fdoor[0] - XT > 0.5:                    # fixed lattice panel beside the entrance, on whichever side is free
        bays.append((XT + P / 2 + 0.01, fdoor[0] - 0.06))
    else:
        bays.append((fdoor[1] + 0.06, X1 - P / 2 - 0.01))
    for (a0, a1) in bays:
        if a1 - a0 < 0.3:
            continue
        # paper behind the lattice
        m.add(box(a0, a1, lat_y0, lat_y1, zf, zf + 0.008, "shoji", vis=(1,), uv="world", tag="koshi"))
        # frame
        m.add(box(a0 - 0.04, a1 + 0.04, lat_y1, lat_y1 + 0.06, zf, zf + 0.07, "timber", vis=(1,), tag="koshi"))
        m.add(box(a0 - 0.04, a1 + 0.04, lat_y0 - 0.06, lat_y0, zf, zf + 0.07, "timber", vis=(1,), tag="koshi"))
        # slats
        n = int((a1 - a0) / 0.055)
        for k in range(n):
            x = a0 + (k + 0.5) * (a1 - a0) / n
            m.add(box(x - 0.014, x + 0.014, lat_y0, lat_y1, zf + 0.012, zf + 0.055, "timber", vis=(1,), tag="koshi"))
        # resolution 2: one textured panel
        m.add(box(a0, a1, lat_y0, lat_y1, zf, zf + 0.05, {"front": "koshi", "default": "timber"}, vis=(2, 3),
                  tag="koshi"))
    # --- mushiko-mado: slatted plaster windows on the upper street front ---
    if two and p["upper_front"] == "mushiko":
        wy0, wy1 = FU + 0.55, FU + 1.35
        xs = [(X0 + 0.45, (X0 + XT) / 2 - 0.25), ((X0 + XT) / 2 + 0.25, XT - 0.35)]
        for (a0, a1) in xs:
            m.add(box(a0, a1, wy0, wy1, zf, zf + 0.03, {"front": "mushiko", "default": ext_pl}, vis=(1, 2, 3),
                      uv="fit", tag="mushiko"))
    # --- windows: back of the last room, the upper back room, the upper toriniwa wall ---
    last = rooms[-1]
    if last.get("window_back"):
        a0, a1 = X0 + 0.9, XT - 0.9
        for zz, sgn in ((Z0 - EXT / 2, -1), (Z0 + EXT / 2, +1)):
            m.add(box(a0, a1, FR + 0.7, FR + 1.9, zz, zz + sgn * 0.01, {"front": "shoji", "back": "shoji",
                                                                          "default": "timber"},
                      vis=(1, 2), uv="fit", tag="window"))
            m.add(box(a0 - 0.05, a1 + 0.05, FR + 1.9, FR + 1.96, zz, zz + sgn * 0.05, "timber", vis=(1,), tag="window"))
            m.add(box(a0 - 0.05, a1 + 0.05, FR + 0.64, FR + 0.7, zz, zz + sgn * 0.05, "timber", vis=(1,), tag="window"))
    if two:
        a0, a1 = X0 + 1.2, XT - 1.4
        for zz, sgn in ((Z0 - EXT / 2, -1), (Z0 + EXT / 2, +1)):
            m.add(box(a0, a1, FU + 0.8, FU + 1.6, zz, zz + sgn * 0.01, {"front": "shoji", "back": "shoji",
                                                                          "default": "timber"},
                      vis=(1,), uv="fit", tag="window"))
        # small window from the upper front room into the toriniwa void
        for xx, sgn in ((XT - INT / 2, -1), (XT + INT / 2, +1)):
            m.add(box(xx, xx + sgn * 0.01, FU + 0.7, FU + 1.5, 1.2, 2.6, {"left": "shoji", "right": "shoji",
                                                                           "default": "timber"},
                      vis=(1,), uv="fit", tag="window"))


def _mirror_x(m):
    for s in m.solids:
        s.verts = [(-x, y, z) for (x, y, z) in s.verts]
        s.center = (-s.center[0], s.center[1], s.center[2])
        if isinstance(s.mats, dict):
            mm = dict(s.mats)
            if "left" in s.mats or "right" in s.mats:
                mm["left"], mm["right"] = s.mats.get("right"), s.mats.get("left")
                mm = {k: v for k, v in mm.items() if v is not None}
            s.mats = mm
    m.roadway = [([(-x, y, z) for (x, y, z) in pts], surf) for pts, surf in m.roadway]
    m.memory = {k: [(-x, y, z) for (x, y, z) in v] for k, v in m.memory.items()}
    for f in m.floors:
        x0, x1, z0, z1 = f["rect"]
        f["rect"] = (-x1, -x0, z0, z1)
        f["obstacles"] = [(-b, -a, c, d) for (a, b, c, d) in f["obstacles"]]
    for d in m.doors:
        d.centre = (-d.centre[0], d.centre[1], d.centre[2])
        d.direction = (-d.direction[0], d.direction[1], d.direction[2])
        d.action = (-d.action[0], d.action[1], d.action[2])
