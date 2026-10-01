"""The civic / roadside shell template (W2C, Phase C wave 2, 2026-10-01): roadside tea houses (TR01), the smithy and the
swordsmith (TR11), the guard hut (GV1) and the ward gate (kido) with its gatekeeper hut (GV7). Bare shells: no
furniture (a later agent furnishes); every shell lists its fixed-prop spots in info['fittings'] (kamado, forge,
bellows, anvil, quench tub, fire ladder ...) for the furnisher. Built on templates/rural.py's Shell (posts on soseki,
wall lines, koyagumi under the roof, floors, kamachi) and the new jpparts/gates.py (the kido).

    M, floors, rooms, info = civic.model(kind="teahouse", size="shop", roof="itabuki")

Kinds and parameters (kit frame as rural.py: x 0..W along the front, z 0 = front wall line, +z = out, z -D = back)
  teahouse  TR01 roadside tea house (kake-jaya / chamise / tateba-jaya); the pass tea house (toge-jaya) is a size
              size   'bench'  W 2 x D 1.5 ken: open-fronted bench shed, earth floor, board walls on three sides
                     'shop'   W 3 x D 2 ken: open-fronted shop: doma 2 ken + a raised board agari (1 ken) with the
                              kamachi; the battari bench folded down in the front bay
                     'pass'   W 3 x D 2 ken, the mountain-pass tea house: stone-weighted boards, the front lean-to
                              and a woodshed lean-to on the doma gable, one front bay walled against the wind
                     'tateba' W 5 x D 3 ken, the rest stop with rooms: doma 2 ken full depth (open front, battari),
                              agari (boards, open to the doma) + zashiki (tatami, closed, hikiwake from the agari)
              roof   'thatch' (no front lean-to: a pent cannot sit under a thatch eave, C2) | 'itabuki' | 'ishioki'
                     (board roofs get a 1-ken front lean-to on posts over the benches)
  smithy    TR11 smithy (kaji-ya): doma only, open front, koyagumi framing (sooted), a koshiyane smoke vent over the
            forge bay; the forge / bellows / anvil / quench tub are specialty props (spots in info['fittings'])
              form   'open'  W 3 x D 2 ken, two front bays open, the third walled with a push-up shutter
                     'sword' W 4 x D 3 ken, the swordsmith: closed; a front work doma + the darkened forge room
                              behind a partition (one small high shutter), shimenawa spot over the forge
              roof   'itabuki' | 'sangawara'
  guardhut  GV1 guard hut (kido-ban / jishin-ban / tsuji-ban / bridge, ferry, border, water guard: props decide)
              size   's' W 1.5 x D 1 ken (6 x 9 shaku, eave ~10 shaku [T11]): katabiki door on the long side, a
                     push-up counter shutter on the end, doma + a raised board bench at the back
                     'm' W 2 x D 1.5 ken (the self-watch post / jishin-ban): door + a front window, doma + boards,
                     a fire-ladder spot on the roof
              roof   'itabuki' | 'sangawara'    walls 'board' | 'earth'
  kido      GV7 ward gate: main posts 1.5 ken apart with the hinged leaf pair (gates.gate_leaves), a 1.5-ken wicket bay
            (the kuguri as a katabiki door under a board panel), tie beam + kasagi or a small board roof
              leaves 'lattice' | 'board'   roofed  False | True   hut  None | 'right' (the kidoban hut, GV1 size s,
              inside the ward beside the wicket bay, its door facing the street)

Levels (m): doma 0.05, raised floors 0.40 (huts / agari) or 0.45 (tateba rooms); eave (keta top) 3.10 thatch / 3.30
board roofs with a front lean-to (its eave stays >= 2.40); guard hut 3.03 (10 shaku).
"""
import math

from ..core import Part, box, KEN, HALF, POST, KETA_H, LIBRARY
from .. import walls, openings, roofs as R, floors as FL, leanto, frame, gates as G, pits as PI
from ..assemble import to_world
from .rural import Shell, big_leaf, _gable_leanto, _kamado, ishioki_lod, _r, DOMA, A_, BOARDS_ROUGH

KINDS = ("teahouse", "smithy", "guardhut", "kido")
AGARI = 0.40
ROOM_FLOOR = 0.45


# ------------------------------------------------------------------------------------------------ helpers
def open_front(S, x0, x1, YT, side="front", name="open_front_beam"):
    """Posts at every ken node of an open run (the shed's open front) + a head beam (nuki) at door height."""
    fr = S.F[side]
    k = 0
    while x0 + k * KEN <= x1 + 1e-6:
        S.side_post(side, x0 + k * KEN, YT)
        k += 1
    s = S.B.P(name)
    s.add(box(x0 - 0.06, x1 + 0.06, YT - 0.40, YT - 0.25, -0.06, 0.06, "wood_weathered", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="nuki"))
    S.B.put(s, fr)


def front_leanto(S, fam, E, t_main, depth=KEN, t_lt=0.30, x0=0.0, x1=None, gov=0.25):
    """A lean-to on posts along the FRONT (the long eave side), under the main eave: the tea house's bench roof
    (kake: 'hung' roof). Its covering top at the wall line stays 0.25 under the main keta top, so it clears the main
    rafters over the whole main overhang (t_main > t_lt); its posts stand on soseki on the outer line every ken. Returns
    its eave (keta top) height."""
    x1 = S.W if x1 is None else x1
    top = E - 0.25
    stack = R.STACK[fam]
    eave = top - stack - t_lt * depth
    zw = -(POST / 2 + 0.02)
    s, sl = leanto.roof("leanto_front", 0.0, x1 - x0, zw, -depth, eave, fam, t=t_lt, gov=gov,
                        flash_top=top + 0.10, keta_ext=0.06)
    if fam == "ishioki":
        ishioki_lod(s, [sl])
    # the lean-to frame: local x 0..L -> world x x1..x0 (yaw 180), local -z (the eave) -> world +z (out of the front)
    S.B.put(s, (180.0, (x1, 0.0, 0.0)), what="leanto.roof %s along the front (bench roof)" % fam)
    k = 0
    while x0 + k * KEN <= x1 + 1e-6:
        S.post(round(x0 + k * KEN, 4), round(depth, 4), eave - KETA_H)
        k += 1
    S.log.append("front lean-to: eave %.2f, top at the wall %.2f (main eave %.2f)" % (eave, top, E))
    return eave


def battari(S, lx, side="front"):
    """The battari-shogi (fold-down bench, down by day) in the 1-ken front bay starting at lx: a walkable seat (its own
    Roadway at 0.42) on the street face; returns its footprint (kit frame) for the floor obstacles."""
    S.B.put(openings.part_battari("_down"), S.F[side], lx, 0.0, what="jp_p_open_battari _down (bay %.2f)" % lx)
    p0 = to_world(S.F[side], lx, 0.0)
    p1 = to_world(S.F[side], lx + KEN, 0.62)
    return _r(min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[1], p1[1]))


def fit(S, kind, room, rect=None, centre=None, yaw=None, size=None, note="", y=None, obstacle=True, pad=0.20):
    """A fixed-prop spot for the furnisher (info['fittings']): rect (x0, x1, z0, z1) or centre + size (w, d) + yaw; it
    is kept clear of loot points (an obstacle of its room) unless obstacle=False."""
    f = {"kind": kind, "room": room, "note": note}
    if rect is not None:
        f["rect"] = tuple(round(v, 3) for v in rect)
        r = rect
    else:
        f["centre"] = (round(centre[0], 3), round(centre[1], 3))
        f["size"] = size
        if yaw is not None:
            f["yaw"] = yaw
        w, d = size
        ca, sa = abs(math.cos(math.radians(yaw or 0.0))), abs(math.sin(math.radians(yaw or 0.0)))
        hx, hz = (w * ca + d * sa) / 2, (w * sa + d * ca) / 2
        r = (centre[0] - hx, centre[0] + hx, centre[1] - hz, centre[1] + hz)
    if y is not None:
        f["y"] = round(y, 3)
    S.fittings.append(f)
    if obstacle and room:
        S.obst.append((room, _r(r[0] - pad, r[1] + pad, r[2] - pad, r[3] + pad)))


def _bw(mat="wood_weathered"):
    return dict(kind="board_vertical", mat=mat, grime=False)


def _ext(W, D):
    return lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6


FRAME_R2_DROP = ("tsuka", "munazuka", "moya", "kutsunugi", "sumi_sasu", "tsuma_sasu")
FRAME_R3_DROP = ("tie_beam", "collar", "ushibari", "tsuka", "munazuka", "moya", "track", "sill", "head", "top_rail",
                 "verge_batten")


def trim_lods(H, stones_keep=1):
    """Civic far-LOD trim (PLAYBOOK §12 budgets on small open-fronted shells): the window bars show as the kit's
    bars_lod slab from Resolution 2 on (as the board walls' board_lod); the small roof-frame members under the roof
    (struts, purlins, the kutsunugi stone) are Resolution 1 only, the tie beams and collars leave Resolution 3 (the
    roof covers them; C15 compares top heights only); stones_keep > 1 keeps every n-th stone the kit's ishioki_lod left
    in Resolution 1 (the lean-to roofs of the pass tea house)."""
    k = 0
    keep = []
    for s in H.solids:
        if s.tag == "bar" and 2 in s.vis:
            s.vis = set(s.vis) - {2}
        if s.tag == "bars_lod" and 3 in s.vis:
            s.vis = set(s.vis) | {2}
        if s.tag in FRAME_R2_DROP and 2 in s.vis:
            s.vis = set(s.vis) - {2}
        if s.tag in FRAME_R3_DROP and 3 in s.vis:
            s.vis = set(s.vis) - {3}
        if s.tag == "roof_stone" and stones_keep > 1 and 1 in s.vis:
            k += 1
            if k % stones_keep:
                continue
        keep.append(s)
    H.solids = keep


def _main_roof(S, W, D, fam, E, form="kirizuma", ridge="bamboo", soot=True):
    ov = {"thatch": 1.05}.get(fam)
    sls, info_r, K = S.roof(W, D, form, fam, E, ov=ov, soot=soot, ridge=ridge)
    S.keta_ring(W, D, E, hip=(form != "kirizuma"))
    return sls, info_r, K


# ------------------------------------------------------------------------------------------------ TR01 tea house
def teahouse(name=None, size="shop", roof="thatch", wear="_w2"):
    if size == "pass":
        roof = "ishioki"
    W, D = {"bench": (2 * KEN, 1.5 * KEN), "shop": (3 * KEN, 2 * KEN), "pass": (3 * KEN, 2 * KEN),
            "tateba": (5 * KEN, 3 * KEN)}[size]
    lean = roof != "thatch"
    # tateba thatch 3.40: the hipped thatch's eave slab stays >= 2.00 over the raised rooms' door (D2 head check)
    E = 3.30 if lean else (3.40 if size == "tateba" else 3.10)
    YT = E - KETA_H
    YG = E - 0.21
    t = R.PITCH[roof]
    S = Shell(name or "jp_teahouse", W, D, [1, 2], "roadside tea house (TR01), %s" % size, wear)
    B = S.B
    form = "yosemune" if (size == "tateba" and roof == "thatch") else "kirizuma"
    sls, info_r, K = _main_roof(S, W, D, roof, E, form=form, ridge="bamboo" if size != "tateba" else "shiba",
                                soot=(size != "bench"))
    bw = _bw()
    depth = KEN
    obst_doma = []
    if size == "bench":
        # kake-jaya: the front long side open on its posts; board walls back + both gables
        open_front(S, 0.0, W, YT)
        S.wall_line("back", [(0.0, W, DOMA)], YT, (), **bw)
        S.wall_line("left", [(0.0, D, DOMA)], YG, (), **bw)
        S.wall_line("right", [(0.0, D, DOMA)], YG, [(0.5 * KEN, 1.0 * KEN, DOMA + 1.00, DOMA + 1.70, "window")],
                    nodes_extra=(0.5 * KEN, 1.0 * KEN), **bw)
        S.window(openings.part_tsukiage("_board"), "right", 0.5 * KEN, DOMA + 0.10, "Window (end, push-up shutter)")
        for side in ("left", "right"):
            S.gable(side, D, t, E, "_board", thatch=(roof == "thatch"))
        x_doma = W
    elif size in ("shop", "pass"):
        x_doma = 2 * KEN
        # front: bays 0-1 the open doma front (bay 0 the way in, bay 1 the battari bench); bay 2 the agari, walled
        # with a window. The pass tea house differs by its roof (stone-weighted boards, both lean-tos), not its plan.
        S.wall_line("front", [(2 * KEN, W, AGARI)], YT,
                    [(2.0 * KEN, 2.5 * KEN, AGARI + 0.90, AGARI + 1.65, "window")], nodes_extra=(2.5 * KEN,), **bw)
        open_front(S, 0.0, 2 * KEN, YT)
        S.window(openings.part_window_slide("_board"), "front", 2.0 * KEN, AGARI, "Window (agari, front)")
        obst_doma.append(battari(S, KEN))
        # back: lx = W - x; the agari (lx 0..1k) and the doma (lx 1k..3k) with the back door at lx 1k..2k (x 2k..1k),
        # its leaf parking over lx 2k..2.5k (plain wall), a window lx 2.5k..3k
        S.wall_line("back", [(0.0, KEN, AGARI), (KEN, W, DOMA)], YT, [(KEN, 2 * KEN, DOMA, DOMA + 2.0, "door")],
                    nodes_extra=(1.5 * KEN,), **bw)
        S.door(openings.part_itado("_single"), "back", KEN, DOMA, "Back door (doma)", "back")
        # left end (lx = z + D): a board-shutter window over the kamado corner (the slide parks over the next half-ken)
        S.wall_line("left", [(0.0, D, DOMA)], YG, [(0.5 * KEN, 1.0 * KEN, DOMA + 1.00, DOMA + 1.75, "window")],
                    nodes_extra=(0.5 * KEN, 1.0 * KEN), **bw)
        S.window(openings.part_window_slide("_board"), "left", 0.5 * KEN, DOMA + 0.10, "Window (doma end)")
        S.wall_line("right", [(0.0, D, AGARI)], YG, [(0.5 * KEN, 1.0 * KEN, AGARI + 0.90, AGARI + 1.60, "window")],
                    nodes_extra=(0.5 * KEN, 1.0 * KEN), **bw)
        S.window(openings.part_tsukiage("_board"), "right", 0.5 * KEN, AGARI, "Window (agari end, push-up shutter)")
        for side in ("left", "right"):
            S.gable(side, D, t, E, "_board", thatch=(roof == "thatch"))
    else:   # tateba
        x_doma = 2 * KEN
        ZP = -1.5 * KEN
        fin, kosh = "nakanuri", 0.90
        open_front(S, 0.0, x_doma, YT)
        obst_doma.append(battari(S, KEN))
        S.wall_line("front", [(x_doma, W, ROOM_FLOOR)], YT,
                    [(2.5 * KEN, 3.0 * KEN, ROOM_FLOOR + 0.90, ROOM_FLOOR + 1.65, "window"),
                     (4.0 * KEN, 4.5 * KEN, ROOM_FLOOR + 0.90, ROOM_FLOOR + 1.65, "window")],
                    finish=fin, koshiita=kosh, nodes_extra=(2.5 * KEN, 3.0 * KEN, 4.0 * KEN, 4.5 * KEN))
        S.window(openings.part_window_slide("_board"), "front", 2.5 * KEN, ROOM_FLOOR, "Window (agari, front L)")
        S.window(openings.part_window_slide("_board"), "front", 4.0 * KEN, ROOM_FLOOR, "Window (agari, front R)")
        # back: lx = W - x; zashiki lx 0..3k, doma lx 3k..5k: back door lx 3k..4k (x 2k..1k), parks lx 4k..4.5k
        S.wall_line("back", [(0.0, 3 * KEN, ROOM_FLOOR), (3 * KEN, W, DOMA)], YT,
                    [(1.0 * KEN, 1.5 * KEN, ROOM_FLOOR + 0.90, ROOM_FLOOR + 1.65, "window"),
                     (3 * KEN, 4 * KEN, DOMA, DOMA + 2.0, "door")],
                    finish=fin, koshiita=kosh, nodes_extra=(1.0 * KEN, 1.5 * KEN, 4.5 * KEN))
        S.window(openings.part_window_slide("_board"), "back", 1.0 * KEN, ROOM_FLOOR, "Window (zashiki, back)")
        S.door(openings.part_itado("_single"), "back", 3 * KEN, DOMA, "Back door (doma)", "back")
        S.wall_line("left", [(0.0, D, DOMA)], YT if form != "kirizuma" else YG,
                    [(1.0 * KEN, 1.5 * KEN, DOMA + 1.00, DOMA + 1.75, "window")], finish=fin, koshiita=kosh,
                    nodes_extra=(1.0 * KEN, 1.5 * KEN))
        S.window(openings.part_window_slide("_board"), "left", 1.0 * KEN, DOMA + 0.10, "Window (doma end)")
        # right end: lx = -z: agari lx 0..1.5k, zashiki lx 1.5k..3k (push-up shutter)
        S.wall_line("right", [(0.0, D, ROOM_FLOOR)], YT if form != "kirizuma" else YG,
                    [(2.0 * KEN, 2.5 * KEN, ROOM_FLOOR + 0.90, ROOM_FLOOR + 1.60, "window")], finish=fin,
                    koshiita=kosh, nodes_extra=(1.5 * KEN, 2.0 * KEN, 2.5 * KEN))
        S.window(openings.part_tsukiage("_board"), "right", 2.0 * KEN, ROOM_FLOOR, "Window (zashiki end, push-up)")
        if form == "kirizuma":
            for side in ("left", "right"):
                S.gable(side, D, t, E, "_board")
        # partitions (interior): zashiki | agari along z = ZP (hikiwake shoji at x 3k..4k, plain half-ken both
        # sides), zashiki | doma along x = x_doma (plain wall); both end at a head beam, open above (FB2 C21)
        PT = ROOM_FLOOR + walls.HEAD_T + 2.0 + 0.45
        B.interior = True
        F_Z = (0.0, (x_doma, 0.0, ZP))
        S.wall_line((F_Z, W - x_doma, "part_z"), [(0.0, W - x_doma, ROOM_FLOOR)], PT,
                    [(1.0 * KEN, 2.0 * KEN, ROOM_FLOOR, ROOM_FLOOR + 2.0, "door")], finish="nakanuri", grime=False,
                    interior="both", nodes_extra=(0.5 * KEN, 2.5 * KEN))
        S.door(openings.part_shoji_ext("_hikiwake"), F_Z, 1.0 * KEN, ROOM_FLOOR, "Agari -> zashiki (hikiwake)", "zashiki")
        F_X = (90.0, (x_doma, 0.0, -D))                       # x = x_doma, local lx = z + D, z -D..ZP
        S.wall_line((F_X, D + ZP, "part_x"), [(0.0, D + ZP, ROOM_FLOOR)], PT, (), finish="nakanuri", grime=False,
                    interior="both")
        B.interior = False
        S.head_beam(F_Z, W - x_doma, PT, "part_z_head")
        S.head_beam(F_X, D + ZP, PT, "part_x_head")
    # ------------------------------------------------ floors
    zf = depth - 0.15 if lean else -A_
    B.interior = True
    B.merge(FL.doma("doma", 0.0 if size != "bench" else -0.06, x_doma + (0.06 if size == "bench" else 0.0), -D,
                    (depth + 0.30) if lean else 0.30,
                    road=(A_, x_doma - (A_ if size == "bench" else 0.07), -D + A_, zf), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    if size in ("shop", "pass"):
        B.merge(FL.boards("agari", x_doma + 0.06, W - A_, -D + A_, -A_, AGARI, mats=BOARDS_ROUGH))
    elif size == "tateba":
        B.merge(FL.boards("agari", x_doma + 0.06, W - A_, -1.5 * KEN + A_, -A_, ROOM_FLOOR, mats=BOARDS_ROUGH))
        B.merge(FL.tatami("zashiki", x_doma + A_, W - A_, -D + A_, -1.5 * KEN - A_, top=ROOM_FLOOR, base=0.0))
    B.interior = False
    if size in ("shop", "pass"):
        S.kamachi((90.0, (x_doma, 0.0, -D)), D, AGARI, [D / 2], "doma", soot=True)
    elif size == "tateba":
        # the agari's open edge on the doma: x = x_doma from z ZP to 0 (local lx = z - ZP)
        S.kamachi((90.0, (x_doma, 0.0, -1.5 * KEN)), 1.5 * KEN, ROOM_FLOOR, [0.75 * KEN], "doma", soot=True)
    # the hearth: the kamado (tea kettle / dumplings) on the doma's back wall, away from the back door
    if size == "bench":
        _kamado(S, "doma", 0.45, -D + 0.45, 0.0, size=(0.60, 0.60))
    else:
        _kamado(S, "doma", 0.50, -D + 0.50, 0.0, size=(0.70, 0.70))
    if size == "pass":
        _gable_leanto(S, "left", "ishioki", E, t)
    if lean:
        # the pass tea house's woodshed lean-to on the left gable: the bench roof's verge stops short of it (C12)
        front_leanto(S, roof, E, t, depth=depth, gov=(0.25, 0.0) if size == "pass" else 0.25)
    # bench spots (the free shogi benches are the furnisher's props): along the open front, inside and out
    if size == "bench":
        fit(S, "bench_spot", "doma", rect=(0.25, W - 0.25, -0.75, -0.30), note="shogi bench(es) along the open "
            "front, inside (red felt or mats; the furnisher's prop)", obstacle=False)
    if lean:
        fit(S, "bench_spot", "doma", rect=(0.20, x_doma - 0.20, depth - 0.75, depth - 0.30),
            note="shogi benches under the front lean-to (the furnisher's props)", obstacle=False)
    for r in obst_doma:
        S.obst.append(("doma", r))
    S.place_windows()
    doors = [S.dn[k] for k in ("front", "back") if k in S.dn]
    note = {"bench": "the whole shed: open front, benches, the kettle hearth",
            "shop": "customers' doma with the benches, the kamado on the back wall",
            "pass": "doma with the kamado; the woodshed lean-to on the left gable",
            "tateba": "customers' doma (porters, horses outside), the kamado; open to the agari"}[size]
    S.room("doma", "doma", "earth", DOMA, (A_, x_doma - (A_ if size == "bench" else 0.07), -D + A_, zf), doors,
           note, enclosed=False)
    if size in ("shop", "pass"):
        S.room("agari", "shop:chaya", "boards", AGARI, (x_doma + 0.07, W - A_, -D + A_, -A_), [],
               "raised board seat (agari) open to the doma: customers rest and eat here", enclosed=False)
    elif size == "tateba":
        S.room("agari", "shop:chaya", "boards", ROOM_FLOOR, (x_doma + 0.07, W - A_, -1.5 * KEN + A_, -A_),
               [S.dn["zashiki"]], "agari open to the doma (meals, tea, sake)", enclosed=False)
        S.room("zashiki", "zashiki", "tatami", ROOM_FLOOR, (x_doma + A_, W - A_, -D + A_, -1.5 * KEN - A_),
               [S.dn["zashiki"]], "rest room with tatami (rooms by the hour for travellers; no lodging)")
    trim_lods(S.H, stones_keep=2 if size == "pass" else 1)
    H, info = S.finish({"params": {"kind": "teahouse", "size": size, "roof": roof},
                        "levels": {"doma": DOMA, "floor": AGARI if size != "tateba" else ROOM_FLOOR, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ TR11 smithy
def koshiyane(S, x0, L, info_r, E, D, fam):
    """A raised louvred smoke vent (koshi-yane) straddling the main ridge from x0 to x0 + L: four posts standing on
    the covering either side of the ridge, louvre boards on both sides, a small board gable roof over it with its own
    ridge (PLAYBOOK §6.1 'smithy: roof smoke vent'; the kit's jp_p_roof_kemuridashi _koshiyane at this ridge's
    height). The main roof stays closed under it (the vent reads from outside; C11 / C12 stay clean)."""
    t = R.PITCH[fam]
    (_, yr, zr), _ = info_r["ridge"]
    h_top = R.STACK[fam] + (0.05 if fam in ("sangawara", "hongawara") else 0.012)     # roofs.roof's roof body top
    cover = lambda dz: E + t * (D / 2 - abs(dz)) + h_top              # noqa: E731  roof body top at dz off the ridge
    lift = 0.62 if fam in ("sangawara", "hongawara") else 0.45
    ytop = yr + lift                                                   # louvre top / vent roof seat
    s = S.B.P("koshiyane")
    m = "wood_weathered"
    zp = 0.36
    for x in (x0 + 0.06, x0 + L - 0.06):
        for sg in (-1, 1):
            z = zr + sg * zp
            # seated 2 cm into the roof body at its inner (higher) face (C12 allows 3 cm)
            s.add(box(x - 0.05, x + 0.05, cover(zp - 0.04) - 0.02, ytop, z - 0.04, z + 0.04, m, vis=(1, 2, 3),
                      tag="vent_post"))
    for sg in (-1, 1):
        z = zr + sg * (zp + 0.02)
        yy = cover(zp) + 0.04
        k = 0
        while yy + 0.07 < ytop - 0.02:
            s.add(box(x0 + 0.11, x0 + L - 0.11, yy, yy + 0.07, z - 0.012, z + 0.012, m, vis=(1,) if k % 2 else (1, 2),
                      tag="louvre"))
            yy += 0.10
            k += 1
        # far LODs: the louvre band as one board (C15: the vent's outline)
        s.add(box(x0 + 0.11, x0 + L - 0.11, cover(zp) + 0.04, ytop - 0.02, z - 0.008, z + 0.008, "wood_sooted",
                  vis=(3,), tag="louvre_lod"))
    # the vent's roof: two board slabs at the main pitch, 0.60 out each side, its own board ridge
    tv = t
    w = 0.62
    for sg in (-1, 1):
        a, b = (zr, zr + sg * w)
        poly = [(x0 - 0.14, a), (x0 + L + 0.14, a), (x0 + L + 0.14, b), (x0 - 0.14, b)]
        if sg < 0:
            poly = poly[::-1]
        from ..shapes import slab
        s.add(slab(poly, lambda x, z: ytop + tv * (w - abs(z - zr)) - 0.03 - tv * w + 0.0 + 0.02,
                   lambda x, z: ytop + tv * (w - abs(z - zr)) + 0.02 - tv * w + 0.05,
                   {"default": "roof_kureita"}, vis=(1, 2, 3), geo=True, view=True, fire="wood", tag="vent_roof",
                   uvscale=(1.2, 1.2)))
    R.board_ridge(s, (x0 - 0.14, ytop + 0.07, zr), (x0 + L + 0.14, ytop + 0.07, zr), tv, width=0.26, height=0.06)
    S.B.merge(s)
    S.log.append("koshiyane smoke vent x %.2f..%.2f on the ridge (top %.2f)" % (x0, x0 + L, ytop + 0.13))


def smithy(name=None, form="open", roof="itabuki", wear="_w2"):
    sword = form == "sword"
    W, D = (4 * KEN, 3 * KEN) if sword else (3 * KEN, 2 * KEN)
    E = 3.40
    YT = E - KETA_H
    YG = E - 0.21
    t = R.PITCH[roof]
    S = Shell(name or "jp_smithy", W, D, [1, 2, 3], "smithy (TR11)%s" % (", swordsmith" if sword else ""), wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, soot=True, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90               # earth walls (fire) over a board skirt
    room_f = "forge" if sword else "doma"
    if not sword:
        # front: bays 0-1 open (the forge works in full view of the road), bay 2 walled with a push-up shutter
        open_front(S, 0.0, 2 * KEN, YT)
        S.wall_line("front", [(2 * KEN, W, DOMA)], YT, [(2.25 * KEN, 2.75 * KEN, DOMA + 1.10, DOMA + 1.80, "window")],
                    finish=fin, koshiita=kosh, nodes_extra=(2.25 * KEN, 2.75 * KEN))
        S.window(openings.part_tsukiage("_board"), "front", 2.25 * KEN, DOMA + 0.20, "Window (front, push-up shutter)")
        # back: lx = W - x; back door lx 0..1k (x 3k..2k), parks lx 1k..1.5k; the forge wall lx 1.5k..3k is solid
        S.wall_line("back", [(0.0, W, DOMA)], YT, [(0.0, KEN, DOMA, DOMA + 2.0, "door")], finish=fin, koshiita=kosh,
                    nodes_extra=(1.5 * KEN,))
        S.door(openings.part_itado("_single"), "back", 0.0, DOMA, "Back door", "back")
        S.wall_line("left", [(0.0, D, DOMA)], YG, [(0.5 * KEN, 1.0 * KEN, DOMA + 1.10, DOMA + 1.85, "window")],
                    finish=fin, koshiita=kosh, nodes_extra=(0.5 * KEN, 1.0 * KEN))
        S.window(openings.part_window_slide("_board"), "left", 0.5 * KEN, DOMA + 0.20, "Window (end)")
        S.wall_line("right", [(0.0, D, DOMA)], YG, (), finish=fin, koshiita=kosh)
        # the forge (hodo) in the back-left corner, its bellows (fuigo) on the end wall beside it, the anvil stump
        # in front of the fire, the quench tub and the charcoal bin to hand
        fx, fz = 0.95, -D + 0.75
        fit(S, "forge", "doma", centre=(fx, fz), size=(1.10, 0.90), yaw=0.0,
            note="hodo: the clay forge hearth against the back wall (specialty prop), under the smoke vent")
        fit(S, "bellows", "doma", centre=(0.32, fz + 0.05), size=(0.45, 1.10), yaw=0.0,
            note="fuigo: box bellows (push-pull) against the end wall, nozzle into the forge's side (specialty prop)")
        fit(S, "anvil", "doma", centre=(fx, fz + 1.05), size=(0.50, 0.50), yaw=0.0,
            note="kanatoko set in a stump in front of the fire; the smith sits / kneels on the bellows side")
        fit(S, "quench_tub", "doma", centre=(fx + 0.85, fz + 0.15), size=(0.60, 0.60), yaw=0.0,
            note="mizu-oke quench tub beside the forge")
        fit(S, "charcoal_bin", "doma", centre=(2.0 * KEN + 0.6, -D + 0.45), size=(0.90, 0.55), yaw=0.0,
            note="pine charcoal bin / bales on the back wall (the back door stays clear)", obstacle=False)
        fit(S, "tool_wall", "doma", rect=(2.0 * KEN + 0.15, W - 0.15, -0.20, -0.08), note="finished hoes, sickles "
            "and tongs hung on the front wall's inside (wall-hung props)", obstacle=False)
        vent_x = 0.0
        rooms = [("doma", "workshop:smithy", (A_, W - A_, -D + A_, -A_), "smithy floor: forge corner (left back), open "
                  "front, the walled bay with the shutter", False)]
    else:
        ZP = -1.5 * KEN                         # front work doma | the darkened forge room
        # front (closed): the entrance pair (hikichigai, itado twin) at lx 0.5k..1.5k (+ the half-ken park bay
        # 1.5k..2k), a board-shutter window behind bars at 3k..3.5k
        S.wall_line("front", [(0.0, W, DOMA)], YT, [(0.5 * KEN, 1.5 * KEN, DOMA, DOMA + 2.0, "door"),
                                                   (3.0 * KEN, 3.5 * KEN, DOMA + 1.00, DOMA + 1.75, "window")],
                    finish=fin, koshiita=kosh, nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.0 * KEN, 3.5 * KEN))
        S.door(openings.part_itado("_twin"), "front", 0.5 * KEN, DOMA, "Entrance (itado pair)", "front")
        S.window(openings.part_window_slide("_board"), "front", 3.0 * KEN, DOMA + 0.10, "Window (work room, front)")
        # back (the forge room): solid but one small high shutter (the swordsmith reads the steel's colour in the
        # dark: BUILDING_LIST 'darkened forge room')
        S.wall_line("back", [(0.0, W, DOMA)], YT, [(1.5 * KEN, 2.0 * KEN, DOMA + 1.60, DOMA + 2.35, "window")],
                    finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN, 2.0 * KEN))
        S.window(openings.part_window_slide("_board"), "back", 1.5 * KEN, DOMA + 0.70, "Window (forge room, high)")
        # left end (the work doma side, lx = z + D): a back door out of the work room at lx 1.5k..2.5k? no: the side
        # door into the forge room's yard (water, charcoal) at lx 0.5k..1.5k, parks lx 1.5k..2k
        S.wall_line("left", [(0.0, D, DOMA)], YG, [(0.5 * KEN, 1.5 * KEN, DOMA, DOMA + 2.0, "door")], finish=fin,
                    koshiita=kosh, nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.0 * KEN))
        S.door(openings.part_itado("_single"), "left", 0.5 * KEN, DOMA, "Side door (forge room)", "side")
        S.wall_line("right", [(0.0, D, DOMA)], YG, [(0.5 * KEN, 1.0 * KEN, DOMA + 1.00, DOMA + 1.75, "window")],
                    finish=fin, koshiita=kosh, nodes_extra=(0.5 * KEN, 1.0 * KEN))
        S.window(openings.part_window_slide("_board"), "right", 0.5 * KEN, DOMA + 0.10, "Window (work room, end)")
        # the partition: work doma | forge room, a katabiki door at x 2.5k..3.5k (parks 3.5k..4k? no: the wall ends
        # at 4k, so the door bay is 2k..3k and it parks over 3k..3.5k), closed up to a head beam, open above
        PT = DOMA + walls.HEAD_T + 2.0 + 0.45
        B.interior = True
        F_Z = (0.0, (0.0, 0.0, ZP))
        S.wall_line((F_Z, W, "part_z"), [(0.0, W, DOMA)], PT, [(2.0 * KEN, 3.0 * KEN, DOMA, DOMA + 2.0, "door")],
                    finish="nakanuri", grime=False, interior="both", nodes_extra=(3.5 * KEN,))
        S.door(openings.part_itado("_single"), F_Z, 2.0 * KEN, DOMA, "Work room -> forge room", "forge")
        B.interior = False
        S.head_beam(F_Z, W, PT, "part_z_head")
        for g in ("left", "right"):
            S.gable(g, D, t, E, "_board")
        fx, fz = 2.4 * KEN, -D + 0.80
        fit(S, "forge", "forge", centre=(fx, fz), size=(1.30, 1.00), yaw=0.0,
            note="hodo: the clay forge hearth on the back wall under the vent (specialty prop); the shimenawa hangs "
                 "over it from the tie beam, a kamidana shelf on the wall beside it")
        fit(S, "bellows", "forge", centre=(fx - 1.05, fz + 0.05), size=(0.50, 1.20), yaw=0.0,
            note="fuigo box bellows on the forge's left (specialty prop)")
        fit(S, "anvil", "forge", centre=(fx, fz + 1.20), size=(0.55, 0.55), yaw=0.0,
            note="kanatoko in its stump; the strikers' sledges stand around it")
        fit(S, "quench_trough", "forge", centre=(fx + 1.20, fz + 0.60), size=(0.40, 1.40), yaw=0.0,
            note="long quench trough (mizubune) for blades")
        fit(S, "shimenawa", "forge", centre=(fx, fz), size=(1.6, 0.2), yaw=0.0, y=round(K["levels"].get("beam_top", 3.2)
                                                                                         - 0.25, 2) if K.get("levels") else 3.0,
            note="shimenawa + shide over the forge, hung from the tie beam (the furnisher's site prop)", obstacle=False)
        fit(S, "clay_trough", "work", centre=(0.70, ZP + 0.55), size=(0.90, 0.45), yaw=0.0,
            note="clay-coating trough (tsuchioki) + whetstones: the work doma's back wall")
        fit(S, "blade_rack", "work", rect=(3.0 * KEN + 0.15, W - 0.15, ZP + 0.08, ZP + 0.20),
            note="blade / tool rack on the partition (wall-hung prop)", obstacle=False)
        vent_x = 2.0 * KEN
        rooms = [("work", "workshop:swordsmith", (A_, W - A_, ZP + A_, -A_), "front work doma: polishing, clay coating, "
                  "tools; the entrance pair", True),
                 ("forge", "workshop:swordsmith", (A_, W - A_, -D + A_, ZP - A_), "the darkened forge room: forge, "
                  "bellows, anvil, quench trough under the smoke vent; one high shutter", True)]
    if not sword:
        for g in ("left", "right"):
            S.gable(g, D, t, E, "_board")
    koshiyane(S, vent_x, KEN, info_r, E, D, roof)
    B.interior = True
    if not sword:
        B.merge(FL.doma("doma", 0.0, W, -D, 0.30, road=(A_, W - A_, -D + A_, -0.15), y=DOMA, mats=FL.MATS_DOMA_EARTH))
        rooms[0] = (rooms[0][0], rooms[0][1], (A_, W - A_, -D + A_, -0.15), rooms[0][3], False)
    else:
        B.merge(FL.doma("work", 0.0, W, ZP, 0.0, road=(A_, W - A_, ZP + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
        B.merge(FL.doma("forge", 0.0, W, -D, ZP, road=(A_, W - A_, -D + A_, ZP - A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.place_windows()
    for (nm, tag, rect, note, enc) in rooms:
        drs = [S.dn[k] for k in (("back",) if not sword else (("front", "forge") if nm == "work" else
                                                                ("forge", "side"))) if k in S.dn]
        S.room(nm, tag, "earth", DOMA, rect, drs, note, enclosed=enc)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "smithy", "form": form, "roof": roof},
                        "levels": {"doma": DOMA, "eave": E}, "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ GV1 guard hut
def guardhut(name=None, size="s", roof="itabuki", walls_="board", wear="_w2", **kw):
    walls_ = kw.get("walls", walls_)
    W, D = (1.5 * KEN, 1.0 * KEN) if size == "s" else (2.0 * KEN, 1.5 * KEN)
    E = 3.03                                    # 10 shaku eave [T11]
    YT = E - KETA_H
    YG = E - 0.21
    t = R.PITCH[roof]
    S = Shell(name or "jp_guardhut", W, D, [2, 3], "guard hut (GV1), %s" % size, wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    if walls_ == "board":
        wk = _bw()
    else:
        wk = dict(finish="nakanuri", koshiita=0.90)
    XB = KEN                                    # doma x 0..1k by the door (full depth) | the raised platform x 1k..W
    # front (lx = x): the katabiki door at lx 0..1k, its leaf parking over 1k..1.5k (plain wall); the platform front
    S.wall_line("front", [(0.0, XB, DOMA), (XB, W, AGARI)], YT, [(0.0, KEN, DOMA, DOMA + 2.0, "door")],
                nodes_extra=(1.5 * KEN,) if size == "m" else (), **wk)
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Door (katabiki)", "front")
    # back (lx = W - x): the platform lx 0..W-XB, the doma the rest
    S.wall_line("back", [(0.0, W - XB, AGARI), (W - XB, W, DOMA)], YT, (), nodes_extra=(W - XB,), **wk)
    # left end (lx = z + D), the doma side: M has a board-shutter window (parks over the next half-ken inside)
    lf = [(0.5 * KEN, 1.0 * KEN, DOMA + 1.00, DOMA + 1.75, "window")] if size == "m" else []
    S.wall_line("left", [(0.0, D, DOMA)], YG, lf, nodes_extra=(0.5 * KEN, 1.0 * KEN) if size == "m" else (), **wk)
    if size == "m":
        S.window(openings.part_window_slide("_board"), "left", 0.5 * KEN, DOMA + 0.10, "Window (end)")
    # right end (lx = -z), the platform side: the push-up counter / watch shutter, its sill 1.10 over the platform
    sx0 = 0.5 * KEN
    S.wall_line("right", [(0.0, D, AGARI)], YG, [(sx0, sx0 + 0.5 * KEN, AGARI + 1.10, AGARI + 1.80, "window")],
                nodes_extra=(sx0, sx0 + 0.5 * KEN), **wk)
    S.window(openings.part_tsukiage("_board"), "right", sx0, AGARI + 0.20, "Counter shutter (end, push-up)")
    for g in ("left", "right"):
        S.gable(g, D, t, E, "_board")
    B.interior = True
    B.merge(FL.doma("doma", 0.0, XB, -D, 0.0, road=(A_, XB - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.boards("floor", XB + 0.06, W - A_, -D + A_, -A_, AGARI, mats=BOARDS_ROUGH))
    B.interior = False
    # the platform's open edge on the doma: x = XB, local lx = z + D, local +z -> -x (the doma)
    S.kamachi((90.0, (XB, 0.0, -D)), D, AGARI, [D / 2], "doma", soot=False)
    S.place_windows()
    fit(S, "brazier", "floor", centre=(W - 0.45, -D + 0.45), size=(0.42, 0.42), yaw=0.0,
        note="hibachi / brazier with the kettle on the platform (the night watch)", y=AGARI, pad=0.05)
    fit(S, "counter", "floor", rect=(W - 0.45, W - A_, -sx0 - 0.5 * KEN, -sx0), y=AGARI, obstacle=False,
        note="under the end shutter: the kido-ban's sundries counter (sandals, candles, sweets), a watch hatch for "
             "the others (a toll box for the bridge / ferry / border guard)")
    fit(S, "lantern_post", None, centre=(0.45, 0.70), size=(0.2, 0.2), yaw=0.0,
        note="the ward-name lantern / notice by the door, outside (site prop)", obstacle=False)
    fit(S, "tool_rack", "doma", rect=(A_ + 0.02, A_ + 0.12, -D + 0.30, -0.40), obstacle=False,
        note="the capture tools / staff / fire hook rack on the doma end wall (wall-hung props)")
    if size == "m":
        fit(S, "fire_ladder", None, rect=(W / 2 - 0.25, W / 2 + 0.25, -D / 2 - 0.10, -D / 2 + 0.10),
            y=round(E + t * D / 2 + R.STACK[roof], 2),
            note="the fire ladder on the ridge (jishin-ban with a ladder: Kyoho, PLAYBOOK §1 [T12]) or a fire-bell "
                 "frame: a site prop", obstacle=False)
    S.room("doma", "guard", "earth", DOMA, (A_, XB - 0.07, -D + A_, -A_), [S.dn["front"]],
           "earth floor by the door: the tool rack, a bench")
    S.room("floor", "guard", "boards", AGARI, (XB + 0.045, W - 0.045, -D + A_, -A_), [],
           "raised platform: the watchmen's seat / sleeping place behind the counter shutter, open to the doma")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "guardhut", "size": size, "roof": roof, "walls": walls_},
                        "levels": {"doma": DOMA, "floor": AGARI, "eave": E}, "koyagumi": K["counts"]},
                       exterior=_ext(W, D))
    return H, info


# ------------------------------------------------------------------------------------------------ GV7 kido
def _attach(S, H2, info2, yaw, origin, prefix):
    """Merge a finished shell (H2, info2 in its kit frame) into S at frame (yaw, origin): solids, doors (their twin
    selections renumbered after S's), posts, rooms, floors' obstacles, fittings, portals."""
    fr = (yaw, origin)
    P = H2.transformed(yaw, origin)
    n0 = len(S.H.doors)
    ren = {}
    for k, d in enumerate(P.doors, 1):
        old, new = d.twin, "doorstwin%d" % (n0 + k)
        ren[old] = new
    for s in P.solids:
        if s.sel in ren:
            s.sel = ren[s.sel]
    mem = {}
    for key, v in P.memory.items():
        for old, new in ren.items():
            if key == old + "_action":
                key = new + "_action"
                break
        mem[key] = v
    P.memory = mem
    for d in P.doors:
        d.twin = ren[d.twin]
    S.H.merge(P)

    def tr(rect):
        cs = [to_world(fr, x, z) for x in (rect[0], rect[1]) for z in (rect[2], rect[3])]
        return _r(min(c[0] for c in cs), max(c[0] for c in cs), min(c[1] for c in cs), max(c[1] for c in cs))
    for (x, z, y0, y1) in info2["posts"]:
        wx, wz = to_world(fr, x, z)
        S.posts.append((round(wx, 4), round(wz, 4), y0, y1))
    for r in info2["rooms"]:
        f = [f_ for f_ in info2["floors"] if f_["name"] == r["name"]][0]
        nm = prefix + r["name"]
        S.rooms.append(dict(r, name=nm, rect_kit=tr(r["rect_kit"]),
                            doors=["DoorsTwin%d" % (n0 + int(d_[len("DoorsTwin"):])) for d_ in r["doors"]]))
        for o in f["obstacles"]:
            S.obst.append((nm, tr(o)))
    for f in info2["fittings"]:
        g = dict(f, room=(prefix + f["room"]) if f.get("room") else None)
        if "rect" in g:
            g["rect"] = tr(g["rect"])
        if "centre" in g:
            g["centre"] = to_world(fr, *g["centre"])
        if "yaw" in g:
            g["yaw"] = (g["yaw"] + yaw) % 360.0
        S.fittings.append(g)
    for n_, b in info2["portals"]:
        rr = tr((b[0], b[1], b[4], b[5]))
        S.portals.append((prefix + n_, (rr[0], rr[1], b[2], b[3], rr[2], rr[3])))
    for k, v in info2["doors"].items():
        if isinstance(v, str):
            S.dn[prefix + k] = "DoorsTwin%d" % (n0 + int(v[len("DoorsTwin"):]))
    return n0


def kido(name=None, leaves="lattice", roofed=False, hut=None, wear="_w2"):
    span = 1.5 * KEN                             # main opening, post centres
    W = span + 2.0 * KEN                         # + the wicket bay: a fixed half-ken panel (sode) beside the main
    #                                              post, the 1-ken wicket, its leaf's half-ken park bay
    S = Shell(name or "jp_kido", W, 0.0, [2, 3], "ward gate (kido, GV7)", wear)
    B = S.B
    top = G.POST_TOP
    for x in (0.0, span):
        S.post(x, 0.0, top, size=G.POST_K, mat="wood_street_dark")
    for x in (span + 0.5 * KEN, span + 1.5 * KEN, W):
        S.post(x, 0.0, top, mat="wood_street_dark")
    # the gate posts carry the far silhouette (no wall slab stands beside them): Shell.finish drops 'post' from
    # Resolution 3, a 'gate_post' stays
    for s_ in S.H.solids:
        if s_.tag == "post":
            s_.tag = "gate_post"
    # the wicket bay: board panels from the street up to the tie beam, the kuguri as a katabiki door between 0.12
    # posts (its leaf on the street face, parking over the bay's last half-ken; D1 makes the period's small wicket a
    # 1.08 m door). The fixed half-ken panel keeps the leaf clear of the heavy main post.
    F_W = (0.0, (span, 0.0, 0.0))
    S.wall_line((F_W, W - span, "wicket"), [(0.0, W - span, DOMA)], G.BEAM_Y,
                [(0.5 * KEN, 1.5 * KEN, DOMA, DOMA + 2.0, "door")], nodes_extra=(0.5 * KEN, 1.5 * KEN),
                **_bw("wood_street_dark"))
    S.door(openings.part_itado("_single"), F_W, 0.5 * KEN, DOMA, "Wicket (kuguri)", "wicket")
    # the leaves
    gp = G.gate_leaves("_" + leaves, span, y0=DOMA + 0.03, y_floor=DOMA)
    S.door(gp, (0.0, (0.0, 0.0, 0.0)), 0.0, 0.0, "Gate leaves (kido)", "gate")
    hd = B.P("kido_head")
    if roofed:
        G.kido_head(hd, 0.0, W, kasagi=False)
        ky = G.kido_roof(hd, 0.0, W)
        B.merge(hd)
        rp = B.P("kido_roof")
        sls, info_r = R.roof(rp, W, 2 * HALF, "kirizuma", "itabuki", eave_y=ky, ov=0.40, gov=0.30, walkable=True)
        B.put(rp, (0.0, (0.0, 0.0, HALF)), what="roofs.roof kirizuma itabuki over the gate (1 ken deep)")
    else:
        G.kido_head(hd, 0.0, W)
        B.merge(hd)
    # the passage floor: a 5 cm packed-earth threshold strip through the gate and the wicket (the street is grade)
    z0, z1 = -1.40, 1.20
    B.interior = True
    B.merge(FL.doma("gate", -0.10, W + 0.10, z0 - 0.15, z1 + 0.15, road=(0.10, W - 0.10, z0, z1), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    # the closed leaves' line + the wicket leaf (head room over the floor is measured with them closed) and the open
    # leaves' places stay clear of loot
    S.obst.append(("gate", _r(-0.2, W + 0.2, -0.22, 0.16)))
    S.obst.append(("gate", _r(0.0, 0.30, -1.50, 0.0)))
    S.obst.append(("gate", _r(span - 0.30, span + 0.10, -1.50, 0.0)))
    S.room("gate", "yard", "earth", DOMA, (0.10, W - 0.10, z0, z1), [S.dn["gate"], S.dn["wicket"]],
           "the passage through the kido (street outside +z, the ward inside -z)", enclosed=False)
    fit(S, "lantern", None, centre=(span / 2, 0.0), size=(0.3, 0.3), yaw=0.0, y=G.BEAM_Y - 0.10,
        note="the ward-name lantern hung under the tie beam (site prop)", obstacle=False)
    if hut:
        H2, i2 = guardhut(name="kidoban", size="s", roof="itabuki", walls="board")
        # the hut inside the ward beside the wicket bay: its front (door) faces the passage (-x), its long side runs
        # into the ward along the street edge; yaw 90 maps hut +z -> world -x, hut x -> world +z
        # (on the half-ken grid, clear of the kasagi's end: half a ken out, one ken back into the ward)
        hx, hz = W + HALF, -KEN - 1.5 * KEN
        _attach(S, H2, i2, 90.0, (hx, 0.0, hz), "hut_")
        S.log.append("kido-ban hut attached at x %.2f..%.2f, z %.2f..%.2f" % (hx, hx + KEN, hz, hz + 1.5 * KEN))
    S.place_windows()
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "kido", "leaves": leaves, "roofed": roofed, "hut": hut},
                        "levels": {"doma": DOMA, "beam": G.BEAM_Y}, "centre_kit": (W / 2, 0.0)})
    return H, info


BUILDERS = {"teahouse": teahouse, "smithy": smithy, "guardhut": guardhut, "kido": kido}


def build(kind, **params):
    if kind not in BUILDERS:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(KINDS)))
    return BUILDERS[kind](**params)


def budget_class(kind, **params):
    """PLAYBOOK §12: the guard hut, the kido and the bench shed are small (<= 20 m2); the 5-ken tateba and the 4 x 3
    ken swordsmith with their rooms are 'large' (as C1's 5-ken inns and 4-ken end units); the rest 'standard'."""
    if kind == "kido" and params.get("hut"):
        return "standard"                       # two structures in one object: the gate + the kido-ban hut
    if kind in ("guardhut", "kido") or (kind == "teahouse" and params.get("size") == "bench"):
        return "small"
    if (kind == "teahouse" and params.get("size") == "tateba") or (kind == "smithy" and params.get("form") == "sword"):
        return "large"
    return "standard"


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
