"""The wave-3b trade / service shell template (W3B, Phase C wave 3b, 2026-10-02): the public bathhouse (sento, TR08),
the stable row of a stable yard (TR09), the stall-kit booths that are buildings (barber's booth, show booth, TR02),
the earth-floor and raised-floor workshops (TR13 / TR14), the timber-yard sheds (TR15), the foundry (TR12) and the
yard compounds (K3's wall kit, via templates/dwelling.compound). Bare shells: every shell lists its fixed-prop spots in
info['fittings'] for the furnisher. Research per building: spikes/W3B/W3B_NOTES.md.

    M, floors, rooms, info = trade.model(kind="sento", roof="sangawara")

Kinds and parameters (kit frame as rural.py: x 0..W along the front, z 0 = front wall line, +z = out, z -D = back)
  sento      W 6 x D 3 ken: entrance doma (1.5 ken: the bandai at the step-up) | the changing room + washing floor
             (raised boards 0.40, 3 ken) | the zakuro-guchi partition (a decorative low gabled opening, D9, + a normal
             board door) | the dim bath room (1.5 ken, the tub = a prop on the end wall) | the kama-ba = an open lean-to
             on the right gable (the boiler's fire mouth). A koshiyane steam vent over the bath.  roof sangawara|itabuki
  stablerow  W 5.5 x D 2.5 ken: four stalls in a row on the back wall (the kit's stall frame, bars down), their aisle
             open to the yard; a closed tack room (1.5 ken) at the right end.  roof itabuki|thatch
  booth      form 'barber'   W 2 x D 2 ken: the de-doko booth: open front, earth floor where the barber works, a
                             raised board bench (0.40) at the back for the waiting customers
             form 'misemono' W 3 x D 2.5 ken: the show booth: straw-mat walls on posts, a board roof, a curtained (rolled
                             mushiro) entrance, an earth pit for the audience, a low board stage (0.60) at the back
  workshop   form 'doma'  W 3 x D 2.5 ken: an earth work floor 2 ken wide open to the street (two bays), a raised board
                          room 1 ken at the right end (kamachi), back door.  roof itabuki|sangawara
             form 'bench' W 3.5 x D 3 ken: an entrance doma 1.5 ken (full depth, front + back doors), the raised work
                          room (2 x 1.5 ken, a wide lattice window on the street) and behind it the closed back room
                          (the dust-free coating room: one high window, a door from the work room).  roof as above
  timbershed form 'saw' W 4 x D 2 ken open shed (back wall only): the sawing trestle stands under it
             form 'store' W 4 x D 1.5 ken, open front: timber stood upright against the back wall
             form 'shingle' W 2 x D 1.5 ken, open front: the shingle splitter's shed
  foundry    W 4 x D 3 ken, eave 3.80: two open front bays, earth walls over a board skirt, sooted roof frame, a 1.5-ken
             koshiyane over the furnace; the furnace (koshiki-ro) + treadle bellows at the back, the casting floor (sand)
             in front of it.  roof itabuki|sangawara
  compound   plot 'stableyard' | 'timberyard' | 'foundryyard': board-fence yards with a wide gate (K3's kit through
             dwelling.compound; the plots are registered into dwelling.COMPOUNDS here)
"""
import math

from ..core import Part, box, prism, KEN, HALF, POST, KETA_H, DOOR_H
from .. import walls, openings, roofs as R, floors as FL, stall as SL
from .rural import Shell, big_leaf, _gable_leanto, _kamado, _r, DOMA, A_, BOARDS_ROUGH
from .civic import fit, trim_lods, koshiyane, open_front, _ext
from . import dwelling as DW

KINDS = ("sento", "stablerow", "booth", "workshop", "timbershed", "foundry", "compound")
FLR = 0.40                    # raised floors (changing room, bench, workshop rooms): PLAYBOOK §4 hut / shop agari
STAGE = 0.60                  # the show booth's stage
SAND = {"top": "ground_earth_bare", "body": "stone_cut"}     # the foundry's casting floor (moulding sand)


def _bw(mat="wood_weathered"):
    return dict(kind="board_vertical", mat=mat, grime=False)


def _open_end(S, side, L, y):
    """An open gable end (a shed): posts every ken + a plate beam under the gable boards at y (the gable panel sits on
    it) + a tie (nuki) at door height."""
    k = 0
    while k * KEN <= L + 1e-6:
        S.side_post(side, round(k * KEN, 4), y)
        k += 1
    s = S.B.P("open_%s_plate" % side)
    s.add(box(-0.06, L + 0.06, y - 0.15, y, -0.06, 0.06, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="plate"))
    s.add(box(-0.06, L + 0.06, 2.25, 2.37, -0.05, 0.05, "wood_weathered", vis=(1, 2), geo=True, view=True,
              fire=True, tag="nuki"))
    S.B.put(s, S.F[side])


# ------------------------------------------------------------------------------------------------ TR08 sento
def zakuro_guchi(S, fr, a, b, floor_y, oh=0.95):
    """The zakuro-guchi (D9: decorative): a low opening a..b (partition-local x) oh high over the floor, framed in black
    lacquer, under a painted (vermilion) panel and a small gable with black bargeboards, on the partition's +z face (the
    washing side). Visual only (no collision: nobody passes, the normal door beside it is the way in)."""
    p = S.B.P("zakuro_guchi")
    zf = POST / 2 + 0.036                       # just proud of the board wall's battens (0.093)
    fm, pm, rm = "lacquer_black", "paint_shu", "wood_weathered"
    x0, x1 = a + A_ + 0.005, b - A_ - 0.005      # the opening (the wall's cut is a + A_ .. b - A_)
    yh = floor_y + oh
    # jambs + lintel inside the opening (the visible frame)
    for (u0, u1) in ((x0, x0 + 0.05), (x1 - 0.05, x1)):
        p.add(box(u0, u1, floor_y, yh, -POST / 2 + 0.005, zf + 0.025, fm, vis=(1, 2), tag="zg_jamb"))
    p.add(box(x0, x1, yh - 0.06, yh, -POST / 2 + 0.005, zf + 0.025, fm, vis=(1, 2), tag="zg_lintel"))
    # the painted panel over the opening, framed
    px0, px1 = a - 0.30, b + 0.30
    py0, py1 = yh + 0.03, floor_y + 1.95
    p.add(box(px0, px1, py0, py1, zf, zf + 0.018, pm, vis=(1, 2), tag="zg_panel"))
    for (u0, u1, v0, v1) in ((px0 - 0.04, px1 + 0.04, py0 - 0.04, py0), (px0 - 0.04, px1 + 0.04, py1, py1 + 0.04),
                             (px0 - 0.04, px0, py0, py1), (px1, px1 + 0.04, py0, py1)):
        p.add(box(u0, u1, v0, v1, zf, zf + 0.030, fm, vis=(1,), tag="zg_frame"))
    # the small gable: two board slopes from the eaves (px0 - 0.15 / px1 + 0.15 at py1 + 0.04) to the ridge, 0.40 out
    cx = (a + b) / 2
    ye, yr = py1 + 0.04, py1 + 0.40
    xe0, xe1 = px0 - 0.18, px1 + 0.18
    zo = zf + 0.42
    for (ua, ub) in ((xe0, cx), (cx, xe1)):
        ya, yb = (ye, yr) if ua == xe0 else (yr, ye)
        p.add(prism([(ua, ya), (ub, yb), (ub, yb + 0.035), (ua, ya + 0.035)], "z", zf, zo, rm, vis=(1, 2),
                    tag="zg_roof"))
        # the black bargeboard (hafu) on the front edge
        p.add(prism([(ua, ya - 0.07), (ub, yb - 0.07), (ub, yb + 0.045), (ua, ya + 0.045)], "z", zo, zo + 0.03, fm,
                    vis=(1, 2), tag="zg_hafu"))
    # the gable's tympanum (the triangle under the slopes), painted
    p.add(prism([(xe0 + 0.10, ye + 0.01), (xe1 - 0.10, ye + 0.01), (cx, yr - 0.02)], "z", zf, zf + 0.02, pm, vis=(1,),
                tag="zg_tympanum"))
    S.B.interior = True
    S.B.put(p, fr, what="zakuro-guchi (D9 decorative low gabled opening)")
    S.B.interior = False


def sento(name=None, roof="sangawara", wear="_w2"):
    fam = roof
    W, D = 6 * KEN, 3 * KEN
    XD, XZ = 1.5 * KEN, 4.5 * KEN
    E = 3.40
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_sento", W, D, [2, 3], "public bathhouse (sento, TR08)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    # front (lx = x): the entrance door (parks over the doma's second half-ken), two changing-room windows, a high
    # push-up vent window in the bath room
    S.wall_line("front", [(0.0, XD, DOMA), (XD, W, FLR)], YT,
                [(0.0, KEN, DOMA, DOMA + 2.0, "door"),
                 (2.0 * KEN, 2.5 * KEN, FLR + 0.90, FLR + 1.65, "window"),
                 (3.5 * KEN, 4.0 * KEN, FLR + 0.90, FLR + 1.65, "window"),
                 (5.0 * KEN, 5.5 * KEN, FLR + 1.30, FLR + 2.00, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(2.0 * KEN, 2.5 * KEN, 3.5 * KEN, 4.0 * KEN, 5.0 * KEN,
                                                        5.5 * KEN))
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Entrance (bathhouse)", "front")
    S.window(openings.part_window_slide("_board"), "front", 2.0 * KEN, FLR, "Window (changing room, front L)")
    S.window(openings.part_window_slide("_board"), "front", 3.5 * KEN, FLR, "Window (changing room, front R)")
    S.window(openings.part_tsukiage("_board"), "front", 5.0 * KEN, FLR + 0.40, "Steam window (bath room, high)")
    # back (lx = W - x): bath lx 0..1.5k, changing room lx 1.5k..4.5k, doma lx 4.5k..6k with the back door
    S.wall_line("back", [(0.0, 4.5 * KEN, FLR), (4.5 * KEN, W, DOMA)], YT,
                [(2.5 * KEN, 3.0 * KEN, FLR + 0.90, FLR + 1.65, "window"),
                 (4.5 * KEN, 5.5 * KEN, DOMA, DOMA + 2.0, "door")],
                finish=fin, koshiita=kosh, nodes_extra=(2.5 * KEN, 3.0 * KEN, 5.5 * KEN))
    S.door(openings.part_itado("_single"), "back", 4.5 * KEN, DOMA, "Back door (doma)", "back")
    S.window(openings.part_window_slide("_board"), "back", 2.5 * KEN, FLR, "Window (changing room, back)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(1.0 * KEN, 1.5 * KEN, DOMA + 0.90, DOMA + 1.65, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(1.0 * KEN, 1.5 * KEN))
    S.window(openings.part_window_slide("_board"), "left", 1.0 * KEN, DOMA, "Window (doma end)")
    S.wall_line("right", [(0.0, D, FLR)], YG, (), finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN,))
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    # the zakuro-guchi partition x = XZ (lx = z + D; +z face = the changing / washing side): the low gabled opening
    # (decorative, D9) in bay lx 0.5k..1k, the normal board door lx 1.5k..2.5k (parks over 2.5k..3k); full height with
    # a board gable above, so the bath room is closed (steam)
    FX = (90.0, (XZ, 0.0, -D))
    B.interior = True
    S.wall_line((FX, D, "part_zakuro"), [(0.0, D, FLR)], YG,
                [(0.5 * KEN, 1.0 * KEN, FLR, FLR + 0.95, "window"), (1.5 * KEN, 2.5 * KEN, FLR, FLR + 2.0, "door")],
                interior="both", nodes_extra=(0.5 * KEN, 1.0 * KEN, 1.5 * KEN, 2.5 * KEN), **_bw())
    S.door(openings.part_itado("_single"), FX, 1.5 * KEN, FLR, "Washing floor -> bath room (the way in, D9)", "bath")
    B.interior = False
    DW.interior_gable(S, XZ, D, t, E, "gable_zakuro", "_board")
    zakuro_guchi(S, FX, 0.5 * KEN, 1.0 * KEN, FLR)
    S.portals.append(("zakuro-guchi (interior low opening)", (XZ - 0.25, XZ + 0.25, FLR - 0.02, FLR + 1.0,
                                                               -D + 0.5 * KEN, -D + 1.0 * KEN)))
    koshiyane(S, XZ + 0.25 * KEN, KEN, info_r, E, D, fam)
    # floors
    B.interior = True
    B.merge(FL.doma("doma", 0.0, XD, -D, 0.0, road=(A_, XD - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.boards("datsuiba", XD + 0.06, XZ - A_, -D + A_, -A_, FLR, mats=FL.MATS_BOARDS_B1))
    B.merge(FL.boards("bath", XZ + A_, W - A_, -D + A_, -A_, FLR, mats=BOARDS_ROUGH))
    B.interior = False
    S.kamachi((90.0, (XD, 0.0, -D)), D, FLR, [1.0 * KEN], "doma", soot=False)
    # the kama-ba: an open lean-to on the right gable (the boiler is fired from outside, through the end wall)
    _gable_leanto(S, "right", fam, E, t)
    fit(S, "tub", "bath", rect=(W - A_ - 1.30, W - A_ - 0.02, -D + A_ + 0.20, -D + A_ + 0.20 + 2.10), y=FLR,
        note="the yubune (tub) against the end wall (prop); the boiler under it is fired from the lean-to outside")
    fit(S, "boiler", "leanto", centre=(W + 0.38, -D + A_ + 1.50), size=(0.55, 0.90), yaw=90.0,
        note="the boiler's fire mouth on the end wall outside (prop) + firewood stacks")
    fit(S, "bandai", "doma", centre=(XD - 0.42, -0.78), size=(0.70, 0.95), yaw=90.0,
        note="the bandai: the attendant's pay counter at the step-up, the cashbox on it (prop)")
    fit(S, "geta_shelf", "doma", rect=(A_ + 0.02, A_ + 0.40, -D + 0.40, -1.25 * KEN), obstacle=False,
        note="the footwear shelf on the doma end wall")
    fit(S, "clothes_shelves", "datsuiba", rect=(XD + 0.30, XZ - 1.60, -D + A_ + 0.02, -D + A_ + 0.40), obstacle=False,
        note="clothes shelves / baskets on the changing room's back wall")
    fit(S, "nagashi", "datsuiba", rect=(XZ - 1.45, XZ - A_ - 0.05, -D + A_ + 0.10, -1.5 * KEN - 0.20), obstacle=False,
        note="the nagashi: the slatted washing floor over its drain on the bath side (walk-on prop)")
    S.place_windows()
    S.room("doma", "doma", "earth", DOMA, (A_, XD - 0.07, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "entrance doma: the noren, the bandai at the step-up, the footwear shelf, the back door")
    S.room("datsuiba", "bath", "boards", FLR, (XD + 0.07, XZ - A_, -D + A_, -A_), [S.dn["bath"]],
           "changing room + washing floor (nagashi) on one board floor, open to the doma over the kamachi")
    S.room("bath", "bath", "boards", FLR, (XZ + A_, W - A_, -D + A_, -A_), [S.dn["bath"]],
           "the dim bath room behind the zakuro-guchi: the tub on the end wall, one high steam window")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "sento", "roof": roof},
                        "levels": {"doma": DOMA, "floor": FLR, "eave": E}, "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ TR09 stable row
def stablerow(name=None, roof="itabuki", wear="_w2"):
    fam = roof
    W, D = 5.5 * KEN, 2.5 * KEN
    XS = 4 * KEN
    DS = 1.5 * KEN                               # stall depth from the back wall
    E = 3.10 if fam == "thatch" else 3.20
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_stablerow", W, D, [1, 2], "stable row (TR09), %s" % fam, wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=0.90 if fam == "thatch" else None, soot=False,
                            ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    bw = _bw()
    open_front(S, 0.0, XS, YT)
    S.wall_line("front", [(XS, W, DOMA)], YT, [(XS, XS + KEN, DOMA, DOMA + 2.0, "door")], **bw)
    S.door(openings.part_itado("_single"), "front", XS, DOMA, "Tack room door", "tack")
    S.wall_line("back", [(0.0, W, DOMA)], YT, [(0.5 * KEN, 1.0 * KEN, DOMA + 0.90, DOMA + 1.65, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN, W - XS), **bw)
    S.window(openings.part_window_slide("_board"), "back", 0.5 * KEN, DOMA, "Window (tack room, back)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, (), nodes_extra=(D - DS,), **bw)
    S.wall_line("right", [(0.0, D, DOMA)], YG, [(1.0 * KEN, 1.5 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(1.0 * KEN, 1.5 * KEN), **bw)
    S.window(openings.part_tsukiage("_board"), "right", 1.0 * KEN, DOMA, "Window (tack room end, push-up)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board", thatch=(fam == "thatch"))
    # the tack-room partition x = XS, full height + a board gable (the stall side is open to the yard)
    FX = (90.0, (XS, 0.0, -D))
    B.interior = True
    S.wall_line((FX, D, "part_tack"), [(0.0, D, DOMA)], YG, (), finish="nakanuri", grime=False, interior="both",
                nodes_extra=(D - DS,))
    B.interior = False
    DW.interior_gable(S, XS, D, t, E, "gable_tack")
    # the stalls: one frame of four (dividers every ken), its end posts stand in the end wall / the partition
    p = Part("stall_row4", "", "")
    SL.stall(p, XS, DS, sides=(False, False), divider_at=(KEN, 2 * KEN, 3 * KEN), bars="down")
    keep = []
    for s in p.solids:
        b = s.bbox()
        cxs = (b[0] + b[1]) / 2
        if s.tag == "stall_post" and (abs(cxs) < 1e-3 or abs(cxs - XS) < 1e-3):
            continue
        if s.tag == "head_rail":
            continue
        keep.append(s)
    p.solids = keep
    p.add(box(A_ + 0.005, XS - A_ - 0.005, SL.HEAD, SL.HEAD + 0.15, -0.05, 0.05, "wood_weathered", vis=(1, 2, 3),
              geo=True, view=True, fire=True, tag="head_rail", grain="long"))
    B.interior = True
    B.merge(p.transformed(0.0, (0.0, DOMA, -D + DS)))
    B.merge(FL.doma("stalls", -0.06, XS, -D, 0.30, road=(A_, XS - A_, -D + A_, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.doma("tack", XS, W, -D, 0.0, road=(XS + A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.obst.append(("stalls", _r(0.0, XS, -D, -D + DS + 0.14)))
    S.fittings.append({"kind": "stall", "room": "stalls", "rect": (0.0, XS, -D + A_, -D + DS),
                       "note": "four stalls (jp_p_frame_stall frame, bars down = as left), mangers on the back wall"})
    fit(S, "tack_wall", "tack", rect=(XS + A_ + 0.05, W - A_ - 0.05, -D + A_ + 0.02, -D + A_ + 0.30), obstacle=False,
        note="tack on the back wall: pack saddles, bridles, straw horseshoes (props)")
    fit(S, "aisle", "stalls", rect=(0.40, XS - 0.40, -D + DS + 0.30, -0.35), obstacle=False,
        note="the aisle in front of the stalls (open to the yard): the fodder cutter, buckets, a dropped saddle")
    S.place_windows()
    S.room("stalls", "storage", "earth", DOMA, (A_, XS - A_, -D + A_, -0.15), [],
           "the stable: four stalls on the back wall, the aisle open to the yard", enclosed=False)
    S.room("tack", "storage", "earth", DOMA, (XS + A_, W - A_, -D + A_, -A_), [S.dn["tack"]],
           "the tack room: saddles, harness, straw horseshoes, the groom's things")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "stablerow", "roof": roof}, "levels": {"doma": DOMA, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ TR02 booths
def booth(name=None, form="barber", wear="_w2"):
    if form == "barber":
        return _barber(name, wear)
    return _misemono(name, wear)


def _barber(name, wear):
    W, D = 2 * KEN, 2 * KEN
    ZB = -1.0 * KEN                              # the bench's front edge
    fam = "itabuki"
    E = 2.95
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_booth_barber", W, D, [2, 3], "barber's booth (de-doko, TR02)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    bw = _bw()
    open_front(S, 0.0, W, YT)
    S.wall_line("back", [(0.0, W, FLR)], YT, (), **bw)
    S.wall_line("left", [(0.0, D + ZB, FLR), (D + ZB, D, DOMA)], YG, (), **bw)
    S.wall_line("right", [(0.0, -ZB, DOMA), (-ZB, D, FLR)], YG, [(0.0, 0.5 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(0.5 * KEN,), **bw)
    S.window(openings.part_tsukiage("_board"), "right", 0.0, DOMA, "Window (end, push-up shutter)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    B.interior = True
    B.merge(FL.doma("doma", -0.06, W + 0.06, ZB, 0.30, road=(A_, W - A_, ZB + 0.10, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.boards("bench", A_, W - A_, -D + A_, ZB - 0.06, FLR, mats=BOARDS_ROUGH))
    B.interior = False
    S.kamachi((0.0, (0.0, 0.0, ZB)), W, FLR, [0.5 * KEN], "doma", soot=False)
    fit(S, "barber_kit", "doma", centre=(W - 0.45, ZB + 0.45), size=(0.45, 0.60), yaw=0.0,
        note="the barber's kit box (bin-darai: basin on top, drawers of razors, combs, pomade, paper cord)")
    fit(S, "stool", "doma", centre=(1.0 * KEN, ZB + 0.85), size=(0.40, 0.40), yaw=0.0,
        note="the customer's low stool, facing the street")
    fit(S, "bench_goods", "bench", rect=(A_ + 0.10, W - A_ - 0.10, -D + A_ + 0.05, ZB - 0.15), obstacle=False,
        note="the waiting bench: a go / shogi board, the tobacco tray, a cushion")
    S.place_windows()
    S.room("doma", "workshop", "earth", DOMA, (A_, W - A_, ZB + 0.07, -0.15), [],
           "the barber's floor: the customer's stool, the kit box; open to the street", enclosed=False)
    S.room("bench", "living", "boards", FLR, (A_, W - A_, -D + A_, ZB - 0.07), [],
           "the raised bench where customers wait (board games, tobacco)", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "booth", "form": "barber"},
                        "levels": {"doma": DOMA, "floor": FLR, "eave": E}, "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


def _misemono(name, wear):
    W, D = 3 * KEN, 2.5 * KEN
    ZS = -1.5 * KEN                              # the stage's front edge
    fam = "itabuki"
    E = 3.10
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_booth_misemono", W, D, [2, 3], "show booth (misemono-goya, TR02)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="log")
    S.keta_ring(W, D, E, hip=False)
    mw = _bw("straw_mushiro")
    # front: mats on posts, the rolled-mat entrance in the middle bay
    S.wall_line("front", [(0.0, W, DOMA)], YT, [(KEN, 2 * KEN, DOMA, DOMA + 2.0, "open")], **mw)
    B.put(openings.part_mushiro("_rolled"), S.F["front"], KEN, DOMA, what="jp_p_open_mushiro _rolled (the entrance)")
    S.portals.append(("mushiro entrance", (KEN + A_ - 0.05, 2 * KEN - A_ + 0.05, DOMA - 0.1, DOMA + 2.1, -0.25, 0.25)))
    S.passages.append((1.5 * KEN, 0.0, DOMA))
    S.wall_line("back", [(0.0, W, STAGE)], YT, (), **mw)
    S.wall_line("left", [(0.0, D + ZS, STAGE), (D + ZS, D, DOMA)], YG, (), **mw)
    S.wall_line("right", [(0.0, -ZS, DOMA), (-ZS, D, STAGE)], YG, (), **mw)
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    B.interior = True
    B.merge(FL.doma("pit", 0.0, W, ZS, 0.0, road=(A_, W - A_, ZS + 0.10, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.boards("stage", A_, W - A_, -D + A_, ZS - 0.06, STAGE, mats=BOARDS_ROUGH))
    B.interior = False
    S.kamachi((0.0, (0.0, 0.0, ZS)), W, STAGE, [0.5 * KEN], "pit", soot=False)
    fit(S, "benches", "pit", rect=(0.35, W - 0.35, ZS + 0.85, -0.90), obstacle=False,
        note="plank benches for the audience (props)")
    fit(S, "signboard", "pit", centre=(1.5 * KEN, 0.45), size=(2.40, 0.20), yaw=0.0, y=2.25, obstacle=False,
        note="the show's signboard over the entrance, outside (a front prop); banners either side")
    fit(S, "show", "stage", rect=(A_ + 0.20, W - A_ - 0.20, -D + A_ + 0.10, ZS - 0.30), obstacle=False,
        note="the show's things left on the stage (a cage, a curtain rail, a drum)")
    S.place_windows()
    S.room("pit", "storage", "earth", DOMA, (A_, W - A_, ZS + 0.07, -A_), [],
           "the audience pit: plank benches on the earth, the rolled-mat entrance")
    S.room("stage", "storage", "boards", STAGE, (A_, W - A_, -D + A_, ZS - 0.07), [], "the low board stage")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "booth", "form": "misemono"},
                        "levels": {"doma": DOMA, "floor": STAGE, "eave": E}, "koyagumi": K["counts"]},
                       exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ TR13 / TR14 workshops
def workshop(name=None, form="doma", roof="itabuki", wear="_w2"):
    if form == "doma":
        return _ws_doma(name, roof, wear)
    return _ws_bench(name, roof, wear)


def _ws_doma(name, roof, wear):
    fam = roof
    W, D = 3 * KEN, 2.5 * KEN
    XR = 2 * KEN
    E = 3.30
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_workshop_doma", W, D, [2, 3], "earth-floor workshop (TR13)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    open_front(S, 0.0, XR, YT)
    S.wall_line("front", [(XR, W, FLR)], YT, [(2.0 * KEN, 2.5 * KEN, FLR + 0.90, FLR + 1.65, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(2.5 * KEN,))
    S.window(openings.part_window_slide("_board"), "front", 2.0 * KEN, FLR, "Window (room, front)")
    # back (lx = W - x): the room lx 0..1k, the doma lx 1k..3k: back door lx 1k..2k (parks 2k..2.5k), push-up window
    S.wall_line("back", [(0.0, KEN, FLR), (KEN, W, DOMA)], YT,
                [(KEN, 2 * KEN, DOMA, DOMA + 2.0, "door"), (2.5 * KEN, 3.0 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN, 2.5 * KEN))
    S.door(openings.part_itado("_single"), "back", KEN, DOMA, "Back door (work floor)", "back")
    S.window(openings.part_tsukiage("_board"), "back", 2.5 * KEN, DOMA, "Window (work floor, back, push-up)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(1.0 * KEN, 1.5 * KEN, DOMA + 0.90, DOMA + 1.65, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(1.0 * KEN, 1.5 * KEN))
    S.window(openings.part_window_slide("_board"), "left", 1.0 * KEN, DOMA, "Window (work floor, end)")
    S.wall_line("right", [(0.0, D, FLR)], YG, [(1.0 * KEN, 1.5 * KEN, FLR + 0.90, FLR + 1.60, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(1.0 * KEN, 1.5 * KEN))
    S.window(openings.part_tsukiage("_board"), "right", 1.0 * KEN, FLR, "Window (room end, push-up)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    B.interior = True
    B.merge(FL.doma("doma", 0.0, XR, -D, 0.30, road=(A_, XR - 0.07, -D + A_, -0.15), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.boards("room", XR + 0.06, W - A_, -D + A_, -A_, FLR, mats=FL.MATS_BOARDS_B1))
    B.interior = False
    S.kamachi((90.0, (XR, 0.0, -D)), D, FLR, [1.5 * KEN], "doma", soot=False)
    fit(S, "work_centre", "doma", rect=(0.60, XR - 0.80, -D + 1.40, -1.10), obstacle=False,
        note="the main work spot: the planing beam / lathe / basket work (the furnisher's specialty props)")
    fit(S, "tool_wall", "doma", rect=(0.25, XR - 0.30, -D + A_ + 0.02, -D + A_ + 0.12), obstacle=False,
        note="tools on the back wall (saws, planes, knives)")
    fit(S, "stock", "doma", rect=(A_ + 0.02, A_ + 0.60, -D + 0.40, -0.40), obstacle=False,
        note="raw stock along the end wall (timber, bamboo poles)")
    S.place_windows()
    S.room("doma", "workshop", "earth", DOMA, (A_, XR - 0.07, -D + A_, -0.15), [S.dn["back"]],
           "the earth work floor, open to the street by day", enclosed=False)
    S.room("room", "living", "boards", FLR, (XR + 0.07, W - A_, -D + A_, -A_), [],
           "the raised room: finished goods, the master's desk; open to the work floor", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "workshop", "form": "doma", "roof": roof},
                        "levels": {"doma": DOMA, "floor": FLR, "eave": E}, "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


def _ws_bench(name, roof, wear):
    fam = roof
    W, D = 3.5 * KEN, 3 * KEN
    XD = 1.5 * KEN                              # entrance doma | the raised rooms
    ZP = -1.5 * KEN                             # work room | back room
    E = 3.30
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_workshop_bench", W, D, [2, 3], "raised-floor bench workshop (TR14)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    # front: the entrance (parks over the doma's second half-ken), the work room's wide lattice windows (shoji inside)
    S.wall_line("front", [(0.0, XD, DOMA), (XD, W, FLR)], YT,
                [(0.0, KEN, DOMA, DOMA + 2.0, "door"),
                 (1.5 * KEN, 2.0 * KEN, FLR + 0.45, FLR + DOOR_H, "window"),
                 (2.5 * KEN, 3.0 * KEN, FLR + 0.45, FLR + DOOR_H, "window")],
                finish=fin, koshiita=None, nodes_extra=(2.0 * KEN, 2.5 * KEN, 3.0 * KEN))
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Entrance", "front")
    S.window(openings.part_window_slide("_shoji"), "front", 1.5 * KEN, FLR, "Lattice window (work room, front L)")
    S.window(openings.part_window_slide("_shoji"), "front", 2.5 * KEN, FLR, "Lattice window (work room, front R)")
    # back (lx = W - x): the back room lx 0..2k (one high push-up window), the doma lx 2k..3.5k (back door)
    S.wall_line("back", [(0.0, 2 * KEN, FLR), (2 * KEN, W, DOMA)], YT,
                [(0.5 * KEN, 1.0 * KEN, FLR + 1.30, FLR + 2.00, "window"),
                 (2.0 * KEN, 3.0 * KEN, DOMA, DOMA + 2.0, "door")],
                finish=fin, koshiita=kosh, nodes_extra=(0.5 * KEN, 1.0 * KEN, 3.0 * KEN))
    S.window(openings.part_tsukiage("_board"), "back", 0.5 * KEN, FLR + 0.40, "High window (back room)")
    S.door(openings.part_itado("_single"), "back", 2.0 * KEN, DOMA, "Back door (doma)", "back")
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(0.5 * KEN, 1.0 * KEN, DOMA + 0.90, DOMA + 1.65, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(0.5 * KEN, 1.0 * KEN))
    S.window(openings.part_window_slide("_board"), "left", 0.5 * KEN, DOMA, "Window (doma end)")
    # right end (lx = -z): the work room lx 0..1.5k (push-up window), the back room lx 1.5k..3k
    S.wall_line("right", [(0.0, D, FLR)], YG, [(0.5 * KEN, 1.0 * KEN, FLR + 0.90, FLR + 1.60, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(0.5 * KEN, 1.0 * KEN, 1.5 * KEN))
    S.window(openings.part_tsukiage("_board"), "right", 0.5 * KEN, FLR, "Window (work room end, push-up)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    # partitions: the back room's doma side (x = XD, z -D..ZP) and its front (z = ZP, x XD..W) with the door from the
    # work room (lx 0.5k..1.5k, parks over 1.5k..2k); both end at a head beam (FB2 C21)
    PT = FLR + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F_X = (90.0, (XD, 0.0, -D))
    S.wall_line((F_X, D + ZP, "part_x"), [(0.0, D + ZP, FLR)], PT, (), finish="nakanuri", grime=False, interior="both")
    F_Z = (0.0, (XD, 0.0, ZP))
    S.wall_line((F_Z, W - XD, "part_z"), [(0.0, W - XD, FLR)], PT, [(0.5 * KEN, 1.5 * KEN, FLR, FLR + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(0.5 * KEN, 1.5 * KEN))
    S.door(openings.part_itado("_single"), F_Z, 0.5 * KEN, FLR, "Work room -> back room (the dust-free room)", "inner")
    B.interior = False
    S.head_beam(F_X, D + ZP, PT, "part_x_head")
    S.head_beam(F_Z, W - XD, PT, "part_z_head")
    B.interior = True
    B.merge(FL.doma("doma", 0.0, XD, -D, 0.0, road=(A_, XD - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.boards("work", XD + 0.06, W - A_, ZP + 0.06, -A_, FLR, mats=FL.MATS_BOARDS_B1))
    B.merge(FL.boards("back", XD + A_, W - A_, -D + A_, ZP - 0.06, FLR, mats=FL.MATS_BOARDS_B1))
    B.interior = False
    S.kamachi((90.0, (XD, 0.0, ZP)), -ZP, FLR, [0.75 * KEN], "doma", soot=False)
    _kamado(S, "doma", 0.42, -D + 0.50, 0.0, size=(0.60, 0.60))
    fit(S, "bench_spot", "work", rect=(XD + 0.55, W - 0.70, ZP + 0.45, -0.55), obstacle=False,
        note="the craftsman's place by the lattice window (polishing stand / lacquer tray / fittings bench)")
    fit(S, "cabinet", "back", rect=(W - A_ - 0.75, W - A_ - 0.02, -D + A_ + 0.02, -D + A_ + 0.60), obstacle=True,
        note="the drying cupboard (urushi-buro) / the store chest in the back room")
    fit(S, "water", "doma", rect=(0.25, XD - 0.30, ZP + 0.30, -0.70), obstacle=False,
        note="water jar + tubs in the doma (polishing water, rinsing)")
    S.place_windows()
    S.room("doma", "doma", "earth", DOMA, (A_, XD - 0.07, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "the entrance doma: the kamado (hot water), the water jar, front + back doors")
    S.room("work", "workshop", "boards", FLR, (XD + 0.07, W - A_, ZP + 0.07, -A_), [S.dn["inner"]],
           "the bench work room: sitting work by the lattice window; open to the doma over the kamachi")
    S.room("back", "workshop", "boards", FLR, (XD + A_, W - A_, -D + A_, ZP - 0.07), [S.dn["inner"]],
           "the closed back room (the dust-free coating room / store): the drying cupboard, one high window")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "workshop", "form": "bench", "roof": roof},
                        "levels": {"doma": DOMA, "floor": FLR, "eave": E}, "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ TR15 timber sheds
TIMBER = {
    # form: (W, D, eave, walled sides, what)
    "saw": (4 * KEN, 2 * KEN, 3.60, ("back",), "the sawing shed: the sawing trestle with its log stands under it"),
    "store": (4 * KEN, 1.5 * KEN, 3.80, ("back", "left", "right"), "the timber store: timber stood upright on the "
              "back wall (tate-kake), planks stacked"),
    "shingle": (2 * KEN, 1.5 * KEN, 3.00, ("back", "left", "right"), "the shingle splitter's shed: the splitting "
                "block, bundles of shingles"),
}


def timbershed(name=None, form="saw", wear="_w2"):
    W, D, E, walled, what = TIMBER[form]
    fam = "itabuki"
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_timber_%s" % form, W, D, [1, 2], "timber yard shed (TR15), %s" % form, wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    bw = _bw()
    open_front(S, 0.0, W, YT)
    if "back" in walled:
        S.wall_line("back", [(0.0, W, DOMA)], YT, (), **bw)
    else:
        open_front(S, 0.0, W, YT, side="back", name="open_back_beam")
    for side in ("left", "right"):
        if side in walled:
            S.wall_line(side, [(0.0, D, DOMA)], YG, (), **bw)
        else:
            _open_end(S, side, D, YG)
        S.gable(side, D, t, E, "_board")
    ol = 0.06 if "left" not in walled else 0.0
    orr = 0.06 if "right" not in walled else 0.0
    B.interior = True
    B.merge(FL.doma("floor", -0.06 - ol, W + 0.06 + orr, -D - (0.0 if "back" in walled else 0.30), 0.30,
                    road=(A_, W - A_, -D + A_, -0.15), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    if form == "saw":
        fit(S, "trestle", "floor", rect=(0.45, W - 0.45, -D + 0.80, -0.90), obstacle=False,
            note="the sawing trestle + the log raised at an angle (prop, ~4.5 m long)")
    elif form == "store":
        fit(S, "upright", "floor", rect=(A_ + 0.05, W - A_ - 0.05, -D + A_ + 0.02, -D + A_ + 0.60), obstacle=False,
            note="timber stood upright against the back wall (tate-kake rack prop)")
        fit(S, "planks", "floor", rect=(0.40, W - 0.40, -D + 1.00, -0.40), obstacle=False,
            note="plank stacks on bearers (props)")
    else:
        fit(S, "split_block", "floor", centre=(1.0 * KEN, -D / 2), size=(0.6, 0.6), yaw=0.0,
            note="the splitting block with the froe (prop)")
        fit(S, "bundles", "floor", rect=(A_ + 0.05, W - A_ - 0.05, -D + A_ + 0.02, -D + A_ + 0.45), obstacle=False,
            note="bundles of shingles along the back wall")
    S.place_windows()
    S.room("floor", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -0.15), [], what, enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "timbershed", "form": form}, "levels": {"doma": DOMA, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ TR12 foundry
def foundry(name=None, roof="itabuki", wear="_w2"):
    fam = roof
    W, D = 4 * KEN, 3 * KEN
    E = 3.80
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_foundry", W, D, [2, 3], "foundry (imoji, TR12)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=True, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    # front: bays 0-1 open (the casting floor in view of the yard), bays 2-3 walled with a window
    open_front(S, 0.0, 2 * KEN, YT)
    S.wall_line("front", [(2 * KEN, W, DOMA)], YT, [(3.0 * KEN, 3.5 * KEN, DOMA + 1.10, DOMA + 1.85, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(3.0 * KEN, 3.5 * KEN))
    S.window(openings.part_window_slide("_board"), "front", 3.0 * KEN, DOMA + 0.20, "Window (front)")
    # back (lx = W - x): back door lx 0..1k (x 4k..3k), parks 1k..1.5k; the furnace wall solid
    S.wall_line("back", [(0.0, W, DOMA)], YT, [(0.0, KEN, DOMA, DOMA + 2.0, "door")], finish=fin, koshiita=kosh,
                nodes_extra=(1.5 * KEN,))
    S.door(openings.part_itado("_single"), "back", 0.0, DOMA, "Back door (charcoal + scrap yard)", "back")
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(2.0 * KEN, 2.5 * KEN, DOMA + 1.10, DOMA + 1.80, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(2.0 * KEN, 2.5 * KEN))
    S.window(openings.part_tsukiage("_board"), "left", 2.0 * KEN, DOMA + 0.20, "Window (end, push-up)")
    S.wall_line("right", [(0.0, D, DOMA)], YG, (), finish=fin, koshiita=kosh)
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    koshiyane(S, 0.5 * KEN, 1.5 * KEN, info_r, E, D, fam)
    B.interior = True
    B.merge(FL.doma("doma", 0.0, W, -D, 0.30, road=(A_, W - A_, -D + A_, -0.15), y=DOMA, mats=SAND))
    B.interior = False
    fx, fz = 1.25 * KEN, -D + 0.85
    fit(S, "furnace", "doma", centre=(fx, fz), size=(1.20, 1.20), yaw=0.0,
        note="the koshiki-ro (stacked clay-ring cupola) on its base, under the smoke vent (specialty prop)")
    fit(S, "bellows", "doma", centre=(fx + 1.55, fz + 0.05), size=(1.10, 1.70), yaw=90.0,
        note="the treadle bellows (fumi-fuigo) beside the furnace, its pipe to the tuyere (specialty prop)")
    fit(S, "casting_floor", "doma", rect=(0.40, 2.6 * KEN, -D + 2.00, -0.55), obstacle=False,
        note="the sand casting floor: moulds bedded in sand, a ladle (props)")
    fit(S, "goods", "doma", rect=(3.0 * KEN, W - A_ - 0.05, -D + A_ + 0.05, -1.0 * KEN), obstacle=False,
        note="new pots and kettles cooling, scrap iron, charcoal (props)")
    S.place_windows()
    S.room("doma", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -0.15), [S.dn["back"]],
           "the foundry floor: the furnace + bellows at the back, the sand casting floor, the goods corner",
           enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "foundry", "roof": roof}, "levels": {"doma": DOMA, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ yard compounds
YARDS = {
    # the stable yard: a board fence round the plot, the wide kabuki gate on the street (south) side; the stable row
    # stands inside at the north with its open stall front to the yard
    "stableyard": dict(W=8 * KEN, D=7 * KEN, closed=True,
                       runs=[([(0.0, 0.0), (0.0, 7 * KEN), (8 * KEN, 7 * KEN), (8 * KEN, 0.0)], "itabei",
                              dict(kuro=False, cap="none"), ("end", "end"))],
                       gates=[(0, 3, 3 * KEN, "kabuki", 1.5 * KEN)]),
    # the timber yard: a long board fence, a wide gate for the log carts (south) and a back wicket-size gate (north)
    "timberyard": dict(W=15 * KEN, D=11 * KEN, closed=True,
                       runs=[([(0.0, 0.0), (0.0, 11 * KEN), (15 * KEN, 11 * KEN), (15 * KEN, 0.0)], "itabei",
                              dict(kuro=False, cap="none"), ("end", "end"))],
                       gates=[(0, 3, 6 * KEN, "kabuki", 1.5 * KEN)]),
    # the foundry yard: a board fence, the gate on the south (the bell mould site sits in the yard)
    "foundryyard": dict(W=10 * KEN, D=8 * KEN, closed=True,
                        runs=[([(0.0, 0.0), (0.0, 8 * KEN), (10 * KEN, 8 * KEN), (10 * KEN, 0.0)], "itabei",
                               dict(kuro=False, cap="none"), ("end", "end"))],
                        gates=[(0, 3, 4 * KEN, "kabuki", 1.5 * KEN)]),
}
DW.COMPOUNDS.update(YARDS)


def compound(name=None, plot="stableyard", wear="_w1"):
    return DW.compound(name=name, plot=plot, wear=wear)


BUILDERS = {"sento": sento, "stablerow": stablerow, "booth": booth, "workshop": workshop, "timbershed": timbershed,
            "foundry": foundry, "compound": compound}


def build(kind, **params):
    if kind not in BUILDERS:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(KINDS)))
    return BUILDERS[kind](**params)


def budget_class(kind, **params):
    """PLAYBOOK §12: the barber's booth and the small sheds are 'small'; the sento and the foundry yard ring 'large'; the
    rest 'standard'."""
    if kind == "booth" and params.get("form", "barber") == "barber":
        return "small"
    if kind == "timbershed" and params.get("form") in ("shingle",):
        return "small"
    if kind in ("sento",):
        return "large"
    if kind == "compound":
        return "large"
    return "standard"


def over_budget_ok(kind, **params):
    """CA1: a deliberate overage (<= +50 %, PLAYBOOK §12) and its reason, or None."""
    if kind == "workshop" and params.get("form") == "bench" and params.get("roof") == "sangawara":
        return "a tiled 3.5 x 3 ken workshop: kawara geometry + two lattice windows + the closed back room"
    if kind == "foundry" and params.get("roof") == "sangawara":
        return "a tiled 4 x 3 ken foundry with the 1.5-ken louvred smoke vent (kawara geometry)"
    return None


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front), as rural.model."""
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
