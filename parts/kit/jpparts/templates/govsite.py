"""The wave-3d government template (W3D, Phase C wave 3d, 2026-10-02): the checkpoint guardhouse with its inspection
room (bansho, size 'sekisho') and the jinya's court room (size 'ginmi'), the post-station office (toiyaba), the jail's
cell block (roya), and the yards / compounds through templates/dwelling.compound (the palisade and the kora-mon are
new wall-kit pieces in jpparts/sitewall.py). Research, sizes and every recorded choice: spikes/W3D/W3D_NOTES.md. The
shells a site reuses (the bunk hall, the samurai mansion, the plain kura, the guard hut, the open board shed) are
earlier shells, furnished in buildings/w3d_sets.py.

    M, floors, rooms, info = govsite.model(kind="bansho", size="sekisho")

Kinds (kit frame as rural.py: x 0..W along the front, z 0 = front line, +z = out, z -D = back, y 0 = grade)
  bansho    size 'sekisho' W 5 x D 3.5 ken, black boards, board roof: the inspection room open to the front over
              3.5 ken (veranda 0.45 + the officials' tatami 0.60 = the stepped levels over the gravel court), the back
              office behind sliding doors, the kitchen doma (1.5 ken, front + back doors)
            size 'ginmi'   W 4 x D 3.5 ken, plastered, tiled: the jinya's court room (the same stepped front, no doma)
  toiyaba   W 5 x D 3 ken, tiled: the raised office (choba, 3.5 ken, 0.45) open to the yard, the clerks' doma
  roya      W 4 x D 3 ken, black boards: the outer lattice + its door, the earth corridor, the inner lattice with two
            cells (2 x 2 ken, raised boards, sliding lattice doors), small barred windows high in the back wall
  compound  the plots in GOV (sekisho, toiyayard, jinya, roya, hikeshi)
"""
import math

from ..core import Part, box, KEN, HALF, POST, KETA_H, DOOR_H
from .. import walls, openings, roofs as R, floors as FL
from ..assemble import to_world
from .rural import Shell, _kamado, _r, DOMA, A_, BOARDS_ROUGH
from .civic import fit, trim_lods, open_front, _ext
from . import dwelling as DW

KINDS = ("bansho", "toiyaba", "roya", "compound")
ENGAWA = 0.45            # the veranda of the inspection / court room
HALL = 0.60              # the officials' tatami
AGARI = 0.45             # the toiya-ba's raised office
CELL = 0.30              # the cells' raised board floors
KURO = "wood_kuro"


def _bw(mat="wood_weathered"):
    return dict(kind="board_vertical", mat=mat, grime=False)


def _front_kamachi(S, L, floor_y, steps, x0=0.0):
    """The raised floor's open front edge on the front line (its beam 7 cm proud of the post line so no face is shared
    with the posts), the kutsunugi step(s) out onto the ground / gravel in front."""
    S.kamachi((0.0, (x0, 0.0, 0.07)), L, floor_y, steps, "front_ground", soot=False)


# ================================================================================================ bansho / ginmi-sho
def bansho(name=None, size="sekisho", wear="_w2"):
    """The checkpoint guardhouse with its inspection room (size 'sekisho') or the jinya court room (size 'ginmi'):
    the front open to the gravel court over the inspection bays: a board veranda (0.45) half a ken deep, the
    officials' tatami (0.60) 2 ken deep = the stepped levels (commoners on the gravel, the veranda, the officials
    above: C_CIVIC 4.1), the back office (boards 0.60) behind sliding doors at z -2.5 ken."""
    sek = size == "sekisho"
    W, D = (5 * KEN if sek else 4 * KEN), 3.5 * KEN
    XI = 3.5 * KEN if sek else W                # the inspection front | the kitchen doma
    ZE, ZP = -0.5 * KEN, -2.5 * KEN             # veranda | tatami | office
    fam = "itabuki"                            # boards: Hakone's shingles, Takayama's board roofs [HAK-V, TAK-WP]
    E = 3.30 if sek else 3.40
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or ("jp_bansho_sekisho" if sek else "jp_ginmisho"), W, D, [2, 3],
              "checkpoint guardhouse with the inspection room (obansho)" if sek else "court room (ginmi-sho) of the "
              "intendant's office", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    wk = _bw(KURO) if sek else dict(finish="nakanuri", koshiita=0.90)
    # the open inspection front (posts every ken + a head nuki), the kitchen bay's front wall with its door
    open_front(S, 0.0, XI, YT)
    if sek:
        FD = (0.0, (XI, 0.0, 0.0))
        S.wall_line((FD, W - XI, "front_d"), [(0.0, W - XI, DOMA)], YT, [(0.0, KEN, DOMA, DOMA + 2.0, "door")],
                    nodes_extra=(W - XI,), **wk)
        S.door(openings.part_itado("_single"), FD, 0.0, DOMA, "Kitchen door (front)", "front")
    # back (lx = W - x): the doma lx 0..1.5k (back door), the office the rest (windows)
    if sek:
        S.wall_line("back", [(0.0, W - XI, DOMA), (W - XI, W, HALL)], YT,
                    [(0.0, KEN, DOMA, DOMA + 2.0, "door"), (2.0 * KEN, 2.5 * KEN, HALL + 0.90, HALL + 1.65, "window"),
                     (3.5 * KEN, 4.0 * KEN, HALL + 0.90, HALL + 1.65, "window")],
                    nodes_extra=(1.5 * KEN, 2.0 * KEN, 2.5 * KEN, 3.5 * KEN, 4.0 * KEN), **wk)
        S.door(openings.part_itado("_single"), "back", 0.0, DOMA, "Kitchen door (back)", "back")
        S.window(openings.part_window_slide("_board"), "back", 2.0 * KEN, HALL, "Window (office, back)")
        S.window(openings.part_window_slide("_board"), "back", 3.5 * KEN, HALL, "Window (office, back L)")
    else:
        S.wall_line("back", [(0.0, W, HALL)], YT,
                    [(0.5 * KEN, 1.0 * KEN, HALL + 0.90, HALL + 1.65, "window"),
                     (2.5 * KEN, 3.0 * KEN, HALL + 0.90, HALL + 1.65, "window")],
                    nodes_extra=(0.5 * KEN, 1.0 * KEN, 2.5 * KEN, 3.0 * KEN), **wk)
        S.window(openings.part_window_slide("_board"), "back", 0.5 * KEN, HALL, "Window (office, back R)")
        S.window(openings.part_window_slide("_board"), "back", 2.5 * KEN, HALL, "Window (office, back L)")
    # left end (lx = z + D): office lx 0..1k (window), tatami 1k..3k, veranda 3k..3.5k
    S.wall_line("left", [(0.0, D + ZE, HALL), (D + ZE, D, ENGAWA)], YG,
                [(0.0, 0.5 * KEN, HALL + 0.90, HALL + 1.65, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN, D + ZE), **wk)
    S.window(openings.part_window_slide("_board"), "left", 0.0, HALL, "Window (office, end)")
    if sek:
        S.wall_line("right", [(0.0, D, DOMA)], YG, [(1.5 * KEN, 2.0 * KEN, DOMA + 1.00, DOMA + 1.75, "window")],
                    nodes_extra=(1.5 * KEN, 2.0 * KEN), **wk)
        S.window(openings.part_window_slide("_board"), "right", 1.5 * KEN, DOMA + 0.10, "Window (kitchen, end)")
    else:
        S.wall_line("right", [(0.0, -ZE, ENGAWA), (-ZE, D, HALL)], YG,
                    [(2.5 * KEN, 3.0 * KEN, HALL + 0.90, HALL + 1.65, "window")],
                    nodes_extra=(-ZE, 2.5 * KEN, 3.0 * KEN), **wk)
        S.window(openings.part_window_slide("_board"), "right", 2.5 * KEN, HALL, "Window (office, end R)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board" if sek else "_tile")
    # interior partitions: tatami | office along z = ZP (hikiwake sliding doors x 1k..2k); doma | rooms along x = XI
    PT = HALL + walls.HEAD_T + 2.0 + (0.30 if sek else 0.45)     # sek: its head beam stays under the eave
    B.interior = True
    F_Z = (0.0, (0.0, 0.0, ZP))
    S.wall_line((F_Z, XI, "part_z"), [(0.0, XI, HALL)], PT, [(1.0 * KEN, 2.0 * KEN, HALL, HALL + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(0.5 * KEN, 2.5 * KEN))
    S.door(openings.part_shoji_ext("_hikiwake"), F_Z, 1.0 * KEN, HALL, "Hall -> office (hikiwake)", "office")
    if sek:
        F_X = (90.0, (XI, 0.0, -D))
        S.wall_line((F_X, D, "part_x"), [(0.0, D, HALL)], PT, (), finish="nakanuri", grime=False, interior="both")
    B.interior = False
    S.head_beam(F_Z, XI, PT, "part_z_head")
    if sek:
        S.head_beam(F_X, D, PT, "part_x_head")
    # floors: the veranda (boards), the officials' tatami, the office (boards), the kitchen doma
    xr = XI - (0.06 if sek else A_)
    B.interior = True
    B.merge(FL.boards("engawa", A_, xr, ZE, 0.0, ENGAWA, mats=BOARDS_ROUGH))
    B.merge(FL.tatami("hall", A_, xr, ZP + 0.06, ZE, top=HALL, base=DOMA))
    B.merge(FL.boards("office", A_, xr, -D + A_, ZP - 0.06, HALL, mats=BOARDS_ROUGH))
    if sek:
        B.merge(FL.doma("doma", XI, W, -D, 0.0, road=(XI + 0.07, W - A_, -D + A_, -A_), y=DOMA,
                        mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    _front_kamachi(S, XI, ENGAWA, [XI / 2 - 0.5 * KEN] if sek else [XI / 2])
    if sek:
        _kamado(S, "doma", XI + 0.40, -D / 2 - 0.20, 90.0, size=(1.10, 0.65))     # clear of the door-to-door band
        fit(S, "rack_spot", None, rect=(0.5 * KEN, 1.2 * KEN, 1.20, 1.60), obstacle=False,
            note="the free-standing rack of the three capture tools on the gravel before the inspection room")
    fit(S, "desks", "hall", rect=(1.0 * KEN, XI - 1.0 * KEN, ZP + 0.40, ZP + 1.10), y=HALL, obstacle=False,
        note="the officials' low desks at the back of the tatami, facing the gravel court")
    fit(S, "ledgers", "office", rect=(A_ + 0.05, XI - 0.30, -D + A_ + 0.02, -D + A_ + 0.45), y=HALL, obstacle=False,
        note="the pass ledgers / registers along the back wall")
    S.place_windows()
    S.room("engawa", "office", "boards", ENGAWA, (A_, xr, ZE + 0.02, -0.02), [],
           "the veranda of the inspection room over the gravel court (samurai stood / sat here)", enclosed=False)
    S.room("hall", "office", "tatami", HALL, (A_, xr, ZP + 0.07, ZE - 0.02), [S.dn["office"]],
           "the officials' tatami (the stepped seat over the court), open to the front", enclosed=False)
    S.room("office", "office", "boards", HALL, (A_, xr, -D + A_, ZP - 0.07), [S.dn["office"]],
           "the back office: pass ledgers, the seal box, writing desks")
    if sek:
        S.room("doma", "kitchen", "earth", DOMA, (XI + 0.07, W - A_, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
               "the guardhouse kitchen doma (kamado, water jar)")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "bansho", "size": size}, "levels": {"doma": DOMA, "engawa": ENGAWA,
                                                                             "hall": HALL, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ toiya-ba
def toiyaba(name=None, wear="_w2"):
    """The post-station office (toiya-ba): W 5 x D 3 ken, tiled, board walls; open on its posts the full front to the
    yard: the raised office (choba, 0.45) over 3.5 ken with its kamachi and a step out to the yard, the clerks' earth
    doma (1.5 ken) open to the yard with a back door to the stable side."""
    W, D, E = 5 * KEN, 3 * KEN, 3.30
    XC = 3.5 * KEN
    fam = "sangawara"
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_toiyaba", W, D, [2, 3], "post-station office (toiya-ba) open to its yard", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    wk = _bw()
    open_front(S, 0.0, W, YT)
    # back (lx = W - x): doma lx 0..1.5k with the back door, the office the rest with two windows
    S.wall_line("back", [(0.0, W - XC, DOMA), (W - XC, W, AGARI)], YT,
                [(0.0, KEN, DOMA, DOMA + 2.0, "door"), (2.5 * KEN, 3.0 * KEN, AGARI + 0.90, AGARI + 1.65, "window"),
                 (4.0 * KEN, 4.5 * KEN, AGARI + 0.90, AGARI + 1.65, "window")],
                nodes_extra=(1.5 * KEN, 2.5 * KEN, 3.0 * KEN, 4.0 * KEN, 4.5 * KEN), **wk)
    S.door(openings.part_itado("_single"), "back", 0.0, DOMA, "Back door (doma, to the stables)", "back")
    S.window(openings.part_window_slide("_board"), "back", 2.5 * KEN, AGARI, "Window (office, back)")
    S.window(openings.part_window_slide("_board"), "back", 4.0 * KEN, AGARI, "Window (office, back L)")
    S.wall_line("left", [(0.0, D, AGARI)], YG, [(1.0 * KEN, 1.5 * KEN, AGARI + 0.90, AGARI + 1.65, "window")],
                nodes_extra=(1.0 * KEN, 1.5 * KEN), **wk)
    S.window(openings.part_window_slide("_board"), "left", 1.0 * KEN, AGARI, "Window (office, end)")
    S.wall_line("right", [(0.0, D, DOMA)], YG, (), **wk)
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    B.interior = True
    B.merge(FL.boards("choba", A_, XC - 0.06, -D + A_, 0.0, AGARI, mats=BOARDS_ROUGH))
    B.merge(FL.doma("doma", XC, W, -D, 0.30, road=(XC + 0.07, W - A_, -D + A_, 0.15), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    _front_kamachi(S, XC, AGARI, [1.75 * KEN])
    S.kamachi((-90.0, (XC, 0.0, 0.0)), D, AGARI, [1.5 * KEN], "doma", soot=False)
    fit(S, "ledgers", "choba", rect=(A_ + 0.05, XC - 0.40, -D + A_ + 0.02, -D + A_ + 0.50), y=AGARI, obstacle=False,
        note="the relay ledgers (tsugitate-cho) and registers along the back wall")
    fit(S, "desks", "choba", rect=(0.6 * KEN, XC - 0.6 * KEN, -1.6 * KEN, -0.9 * KEN), y=AGARI, obstacle=False,
        note="the clerks' desks (choba-zukue) facing the yard")
    S.place_windows()
    S.room("choba", "office", "boards", AGARI, (A_, XC - 0.07, -D + A_, -0.05), [],
           "the raised office (choba) open to the yard: clerks' desks, ledgers, the fare board", enclosed=False)
    S.room("doma", "doma", "earth", DOMA, (XC + 0.07, W - A_, -D + A_, 0.15), [S.dn["back"]],
           "the clerks' earth doma open to the yard, the back door to the stables", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "toiyaba"}, "levels": {"doma": DOMA, "floor": AGARI, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ roya (cell block)
BAR, BAR_PITCH = 0.075, 0.15      # the heavy squared lattice bars (C_CIVIC 4.5: double timber lattice cells)


def lattice(S, fr, a, b, y0, y1, name, mat=KURO):
    """A heavy timber lattice from post node a to post node b on frame fr (local x along, z 0 the line): squared
    bars floor to head, a sill, a head rail, a mid rail through the bars; posts on the nodes (C3). Collision: one
    slab (blocks walking and shots, see-through: no View)."""
    for lx in (a, b):
        x, z = to_world(fr, lx)
        S.post(round(x, 4), round(z, 4), y1 + 0.12)
    p = S.B.P(name)
    xa, xb = a + A_, b - A_
    p.add(box(xa, xb, y0 - 0.10, y0, -0.06, 0.06, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="lattice_sill"))
    p.add(box(xa, xb, y1, y1 + 0.12, -0.06, 0.06, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="lattice_head"))
    n = max(1, int(round((xb - xa) / BAR_PITCH)))
    for k in range(n):
        x = xa + (k + 0.5) * (xb - xa) / n
        p.add(box(x - BAR / 2, x + BAR / 2, y0, y1, -BAR / 2, BAR / 2, mat, vis=(1, 2) if k % 2 == 0 else (1,),
                  tag="lattice_bar", grain="long"))
    for yy in (y0 + 0.95, y0 + 1.60):
        p.add(box(xa, xb, yy, yy + 0.07, -BAR / 2 - 0.012, BAR / 2 + 0.012, mat, vis=(1, 2), tag="lattice_rail"))
    p.add(box(xa, xb, y0, y1, -0.03, 0.03, mat, vis=(3,), tag="lattice_lod", uv="fit"))
    p.add(box(xa, xb, y0, y1, -BAR / 2, BAR / 2, mat, vis=(), geo=True, view=False, fire=True, tag="lattice_geo"))
    S.B.put(p, fr)
    # C11: a lattice is a declared see-through opening (a portal), like a barred window
    (x0, z0), (x1, z1) = to_world(fr, a), to_world(fr, b)
    S.portals.append((name, (min(x0, x1) - 0.30, max(x0, x1) + 0.30, y0 - 0.05, y1 + 0.05, min(z0, z1) - 0.30,
                             max(z0, z1) + 0.30)))


def _leaf_cell(mat=KURO):
    """The cell door's leaf: a stout frame with squared bars and two rails (the same lattice as the cell front)."""
    def build(l0, l1, bot, top, z0, z1, bone, dirn=+1):
        out = [box(l0, l1, bot, top, z0, z1, mat, vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
        sw = 0.07
        out += [box(l0, l0 + sw, bot, top, z0, z1, mat, vis=(1,)), box(l1 - sw, l1, bot, top, z0, z1, mat, vis=(1,)),
                box(l0 + sw, l1 - sw, top - 0.08, top, z0, z1, mat, vis=(1,)),
                box(l0 + sw, l1 - sw, bot, bot + 0.10, z0, z1, mat, vis=(1,))]
        n = max(2, int((l1 - l0 - 2 * sw) / BAR_PITCH))
        for k in range(n):
            x = l0 + sw + (k + 0.5) * (l1 - l0 - 2 * sw) / n
            out.append(box(x - 0.03, x + 0.03, bot + 0.10, top - 0.08, z0 + 0.004, z1 - 0.004, mat, vis=(1,),
                           tag="bar"))
        for yy in (bot + 0.95, bot + 1.55):
            out.append(box(l0 + sw, l1 - sw, yy, yy + 0.06, z0 - 0.006, z1 + 0.006, mat, vis=(1,), tag="rail"))
        # the iron lock plate on the closing stile (a readable door: frame, sill, hardware)
        out.append(box(l0 + 0.01, l0 + sw - 0.01, bot + 0.95, bot + 1.15, z1, z1 + 0.012, "metal_iron", vis=(1,),
                       tag="lock"))
        return out
    return build


def part_cell_door():
    p = openings.single_door_part("jp_p_open_roya_door", "_lattice", [2, 3],
                                  "jail cell door: a sliding lattice leaf in the inner lattice (game concession: the "
                                  "period cell door was a low crawl door; D1 / D2 win, W3D_NOTES site 4)",
                                  _leaf_cell(), "lattice", +1, 0.06, note="corridor-side leaf, parks over the lattice")
    return p


def roya(name=None, wear="_w2"):
    """The jail's cell block (a provincial lock-up, C_CIVIC 4.5 33; Kodenmacho's double lattice): W 4 x D 3 ken,
    black boards, board roof. Front: a 1.5-ken board bay with the block's door + the OUTER lattice; behind it the earth
    corridor (1 ken); the INNER lattice with two cells (2 x 2 ken, raised boards 0.30) and their sliding lattice
    doors; a board wall between the cells; a small barred window high in the back wall of each cell. Empty, the
    doors left open (neutral: no bodies)."""
    W, D, E = 4 * KEN, 3 * KEN, 3.10
    ZL = -1.0 * KEN
    fam = "itabuki"
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_roya", W, D, [2, 3], "jail cell block (roya): double lattice, two cells", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    wk = _bw(KURO)
    # front: the board bay with the door (lx 0..1k, parks over 1k..1.5k), then the outer lattice x 1.5k..W under a
    # board panel to the eave
    S.wall_line("front", [(0.0, 1.5 * KEN, DOMA)], YT, [(0.0, KEN, DOMA, DOMA + 2.0, "door")],
                nodes_extra=(1.5 * KEN,), **wk)
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Door (cell block)", "front")
    LY1 = DOMA + 2.10
    lattice(S, S.F["front"], 1.5 * KEN, W, DOMA + 0.10, LY1, "outer_lattice")
    for lx in (2.0 * KEN, 3.0 * KEN):
        S.side_post("front", lx, YT)
    B.wall(S.F["front"], "front_over", "board_vertical", 1.5 * KEN, W, LY1 + 0.12, YT, finish="nakanuri", head=False,
           mat=KURO)
    # back (lx = W - x): cells at CELL, a small high barred window in each
    WY = CELL + 1.45
    S.wall_line("back", [(0.0, W, CELL)], YT,
                [(0.5 * KEN, 1.0 * KEN, WY, WY + 0.75, "window"), (2.5 * KEN, 3.0 * KEN, WY, WY + 0.75, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 2.5 * KEN, 3.0 * KEN), **wk)
    for lx in (0.5 * KEN, 2.5 * KEN):            # the barred windows are static (bars + a half-open board shutter)
        B.put(openings.part_renji("_wood"), S.F["back"], lx, WY - 0.90, what="jp_p_open_renji _wood (cell, high)")
        S.portals.append(("barred window %d" % int(lx * 100), (W - lx - 0.5 * KEN - 0.25, W - lx + 0.25, WY - 0.05,
                                                                WY + 0.80, -D - 0.30, -D + 0.30)))
    # ends: left (lx = z + D): cell lx 0..2k, corridor 2k..3k; right (lx = -z): corridor 0..1k, cell 1k..3k
    S.wall_line("left", [(0.0, D + ZL, CELL), (D + ZL, D, DOMA)], YG, (), nodes_extra=(D + ZL,), **wk)
    S.wall_line("right", [(0.0, -ZL, DOMA), (-ZL, D, CELL)], YG, (), nodes_extra=(-ZL,), **wk)
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    # the inner lattice along z = ZL: cell A x 0..2k (door bay 0..1k), cell B x 2k..4k (door bay 2k..3k); the leaves
    # park on the corridor face over the next half-ken of lattice
    F_L = (0.0, (0.0, 0.0, ZL))
    B.interior = True
    sill = B.P("cell_sill")
    sill.add(box(0.0, W, 0.0, CELL, -0.06, 0.06, KURO, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="cell_sill"))
    B.put(sill, F_L)
    B.interior = False
    for (a, b) in ((1.0 * KEN, 2.0 * KEN), (3.0 * KEN, 4.0 * KEN)):
        lattice(S, F_L, a, b, CELL, CELL + 2.10, "inner_lattice_%d" % int(a * 100))
    for (lx, key, lab) in ((0.0, "cell_a", "Cell door A"), (2.0 * KEN, "cell_b", "Cell door B")):
        x, z = to_world(F_L, lx)
        S.post(round(x, 4), round(z, 4), CELL + 2.22)
        S.door(part_cell_door(), F_L, lx, CELL, lab, key)
    hd = B.P("inner_head")
    hd.add(box(0.0, W, CELL + 2.10, CELL + 2.22, -0.06, 0.06, KURO, vis=(1, 2, 3), geo=True, view=True, fire=True,
               tag="lattice_head"))
    B.put(hd, F_L)
    B.wall(F_L, "inner_over", "board_vertical", 0.0, W, CELL + 2.22, YT, finish="nakanuri", head=False, mat=KURO)
    # the board wall between the cells (x = 2k, z -D..ZL; lx = z + D)
    F_X = (90.0, (2.0 * KEN, 0.0, -D))
    B.interior = True
    S.wall_line((F_X, D + ZL, "part_x"), [(0.0, D + ZL, CELL)], YT, (), finish="nakanuri", grime=False,
                interior="both")
    B.interior = False
    # floors
    B.interior = True
    B.merge(FL.doma("corridor", 0.0, W, ZL + 0.06, 0.0, road=(A_, W - A_, ZL + 0.08, -A_), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.boards("cell_a", A_, 2.0 * KEN - 0.06, -D + A_, ZL - 0.06, CELL, mats=BOARDS_ROUGH))
    B.merge(FL.boards("cell_b", 2.0 * KEN + 0.06, W - A_, -D + A_, ZL - 0.06, CELL, mats=BOARDS_ROUGH))
    B.interior = False
    fit(S, "keys", "corridor", rect=(A_ + 0.02, A_ + 0.10, ZL + 0.30, -0.40), obstacle=False,
        note="the guards' lantern / clappers on the corridor end wall")
    S.place_windows()
    S.room("corridor", "jail", "earth", DOMA, (A_, W - A_, ZL + 0.08, -A_), [S.dn["front"], S.dn["cell_a"],
                                                                         S.dn["cell_b"]],
           "the earth corridor between the outer and the inner lattice (the guards' walk)")
    S.room("cell_a", "jail", "boards", CELL, (A_, 2.0 * KEN - 0.07, -D + A_, ZL - 0.07), [S.dn["cell_a"]],
           "cell A: raised boards, straw mats, the toilet tub in the corner; empty, the door open")
    S.room("cell_b", "jail", "boards", CELL, (2.0 * KEN + 0.07, W - A_, -D + A_, ZL - 0.07), [S.dn["cell_b"]],
           "cell B: raised boards, straw mats; empty, the door open")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "roya"}, "levels": {"doma": DOMA, "cell": CELL, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ compounds
GOV = {
    # the checkpoint: a palisade 13 x 12 ken, the road through it (z 4.5..6 ken), a kora-mon in the west line (Kyoto
    # side) and the east line (Edo side) by the picker. The gravel court is its own object (oshirasu_s: on a slope a pad
    # inside a big compound would be buried on the high side)
    "sekisho": dict(W=13 * KEN, D=12 * KEN, closed=True,
                    runs=[([(0.0, 0.0), (0.0, 12 * KEN), (13 * KEN, 12 * KEN), (13 * KEN, 0.0)], "saku", {},
                           ("end", "end"))],
                    gates=[(0, 0, 4.5 * KEN) + DW.pick_gate("saku", status="high", role="front"),
                           (0, 2, 6.0 * KEN) + DW.pick_gate("saku", status="high", role="front")]),
    # the gravel courts (oshirasu): pads only (white gravel before the inspection room / the court room)
    "oshirasu_s": dict(W=10.0, D=2.6, closed=False, runs=[], gates=[],
                       pad_posts=[(-0.455, -0.455), (10.465, -0.455), (-0.455, 1.365), (10.465, 1.365)],
                       pads=[("oshirasu", 0.0, 10.0, 0.0, 2.6, "the gravel court before the inspection room (travellers "
                              "knelt on straw mats here)")]),
    "oshirasu_j": dict(W=10.0, D=7.2, closed=False, runs=[], gates=[],
                       pad_posts=[(-0.455, -0.455), (10.465, -0.455), (-0.455, 7.735), (10.465, 7.735)],
                       pads=[("oshirasu", 0.0, 10.0, 0.0, 7.2, "the white-gravel court (oshirasu) before the court "
                              "room")]),
    # the post-station yard: a board fence round the office (at the back) and the yard; the street gate by the picker
    "toiyayard": dict(W=9 * KEN, D=8 * KEN, closed=True,
                      runs=[([(0.0, 0.0), (0.0, 8 * KEN), (9 * KEN, 8 * KEN), (9 * KEN, 0.0)], "itabei",
                             dict(kuro=False, cap="none", skirt=0.60), ("end", "end"))],
                      gates=[(0, 3, 3.5 * KEN) + DW.pick_gate("itabei", status="work", carts=True)]),
    # the intendant's office: the black nagaya-mon (a separate object) in the gap of the south line, a black board fence
    # round the rest, the back gate by the picker; the white-gravel court before the court room
    "jinya": dict(W=22 * KEN, D=13 * KEN, gate_obj=(7.5 * KEN, 14.5 * KEN),
                  runs=[([(7.5 * KEN, 0.0), (0.0, 0.0), (0.0, 13 * KEN), (22 * KEN, 13 * KEN), (22 * KEN, 0.0),
                          (14.5 * KEN, 0.0)], "itabei", dict(kuro=True, cap="none", skirt=0.60), ("end", "end"))],
                  gates=[(0, 1, 2.0 * KEN) + DW.pick_gate("itabei", dict(kuro=True), status="high", role="back")]),
    # the jail: a black board fence round the plot (a plastered dobei was 19k faces, a board cap +81 % R3: W3D_NOTES), ONE
    # gate (the picker: high status, front, board fence = a kabuki-mon 1.5 ken)
    "roya": dict(W=10 * KEN, D=9 * KEN, closed=True,
                 runs=[([(0.0, 0.0), (0.0, 9 * KEN), (10 * KEN, 9 * KEN), (10 * KEN, 0.0)], "itabei",
                        dict(kuro=True, cap="none", skirt=0.60), ("end", "end"))],
                 gates=[(0, 3, 6.0 * KEN) + DW.pick_gate("itabei", dict(kuro=True), status="high", role="front")]),
    # the fire brigade station: a board fence round the tower and the tool shed; a wide gate for ladders and hooks
    "hikeshi": dict(W=8 * KEN, D=7 * KEN, closed=True,
                    runs=[([(0.0, 0.0), (0.0, 7 * KEN), (8 * KEN, 7 * KEN), (8 * KEN, 0.0)], "itabei",
                           dict(kuro=False, cap="none", skirt=0.60), ("end", "end"))],
                    gates=[(0, 3, 3.0 * KEN) + DW.pick_gate("itabei", status="work", carts=True)]),
}
DW.COMPOUNDS.update(GOV)


def compound(name=None, plot="sekisho", wear="_w1"):
    return DW.compound(name=name, plot=plot, wear=wear)


# ================================================================================================ dispatch
def _builders():
    return {k: globals().get(k) for k in KINDS}


def build(kind, **params):
    fn = _builders().get(kind)
    if fn is None:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(KINDS)))
    return fn(**params)


def budget_class(kind, **params):
    """PLAYBOOK §12: the compounds 'large'; the halls 'standard'."""
    return "large" if kind == "compound" else "standard"


def over_budget_ok(kind, **params):
    """CA1: a deliberate overage (<= +50 %, PLAYBOOK §12) and its reason, or None."""
    if kind == "toiyaba":
        return "a 5 x 3 ken tiled hall open on its posts the full front (sangawara courses over 5 ken)"
    if kind == "roya":
        return "the double timber lattice (every squared bar of the outer and inner lattice and the two cell doors " \
               "is geometry: the cell block IS its lattice)"
    return None


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front), as ruralsite.model."""
    H, info = build(kind, name=name, **params)
    cx, cz = info.get("centre_kit", (info["W"] / 2, -info["D"] / 2))
    M = H.transformed(0.0, (-cx, 0.0, -cz))
    M.meta = dict(H.meta)

    def mr(r):
        return (r[0] - cx, r[1] - cx, r[2] - cz, r[3] - cz)
    floors = [dict(f, rect=mr(f["rect"]), obstacles=[mr(o) for o in f["obstacles"]]) for f in info["floors"]]
    rooms = [dict(r, rect_model=[round(v, 3) for v in mr(r["rect_kit"])]) for r in info["rooms"]]
    fits = []
    for f in info["fittings"]:
        g = dict(f)
        if "rect" in g:
            g["rect"] = [round(v, 3) for v in mr(g["rect"])]
        if "centre" in g:
            g["centre"] = [round(g["centre"][0] - cx, 3), round(g["centre"][1] - cz, 3)]
        if "hook" in g:
            g["hook"] = [round(g["hook"][0] - cx, 3), g["hook"][1], round(g["hook"][2] - cz, 3)]
        fits.append(g)
    info = dict(info, centre=(cx, cz), fittings_model=fits,
                portals_model=[(n, (b[0] - cx, b[1] - cx, b[2], b[3], b[4] - cz, b[5] - cz)) for n, b in info["portals"]],
                passages_model=[(x - cx, z - cz, y) for (x, z, y) in info["passages"]])
    return M, floors, rooms, info
