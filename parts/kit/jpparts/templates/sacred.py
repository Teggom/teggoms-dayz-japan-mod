"""The shrine + temple shell template (W2S, Phase C wave 2, 2026-10-01): village AND town grades, bare (a later agent
furnishes; every shell lists its fixed-prop spots in info['fittings']). Built on templates/rural.py's Shell (rooms,
obstacles, portals, fittings bookkeeping) and the W2P1 / W2P2 kit: koran (en + kumi-koran + kizahashi), tobira,
nagare / kohai / hogyo, ornament, stilts / kidan, shitomi (W2P1); sori (curved roofs), kumimono (bracket sets), storey
(hakama) (W2P2); gates (W2C). Research, proportions and choices: spikes/W2S/W2S_NOTES.md.

    M, floors, rooms, info = sacred.model(kind="haiden", grade="village")

Kit frame (as rural.py): x 0..W along the front, z 0 = the front wall (column) line, +z = out (the stair side), z -D =
back, y 0 = grade. Raised halls are built in their FLOOR frame (y 0 = the hall floor, grade at -drop, as the W2P1
parts expect) and lifted by `drop` at the end (_lift).

Kinds (params; see BUILDERS):
  haiden    worship hall          grade village (3 x 2 ken, kirizuma kokera) | town (3 x 2 bays 2.275, curved irimoya)
                                  cover (town) 'hiwada' | 'copper'
  honden    main sanctuary        style 'nagare' | 'shinmei' | 'kasuga'; grade village | town (nagare 3-bay, curved);
                                  chigi True: okichigi + katsuogi on a nagare roof. SEALED (static closed tobira)
  temizuya  purification pavilion grade village | town
  shamusho  priests' office       roof 'itabuki' | 'sangawara'
  kagura    kagura stage          grade village | town
  do        small sacred hall     size 2 | 3; roof 'board' | 'thatch' | 'tile' (village) | grade town (curved copper)
  hondo     main hall             grade village (4 x 4 ken) | town (3 x 3 bays, degumi / mitesaki)
  kuri      priests' quarters     grade village (thatch) | town (sangawara); the genkan porch on the rooms' gable
  shoro     bell tower            grade village (open four-post) | town (hakama skirt + outside stair)
  gate      small gate            grade village (yakui-mon) | town (shikyaku-mon, curved)
"""
import math

from ..core import Part, box, cyl, KEN, HALF, QK, POST, KETA_H, EAVE_Y, WALL_H, DOOR_H, LIBRARY
from .. import walls, frame, roofs as R, floors as FL, openings, found
from .. import koran as KR, tobira as TB, nagare as NG, ornament as ORN, stilts as STL, shitomi as SH
from .. import sori as SO, kumimono as KM, storey as ST, gates as G, trim, pits as PI
from ..assemble import to_world
from .rural import Shell, _r, DOMA, A_, BOARDS_ROUGH, big_leaf, _irori, _kamado
from .civic import fit, trim_lods

KINDS = ("haiden", "honden", "temizuya", "shamusho", "kagura", "do", "hondo", "kuri", "shoro", "gate")
TOWN_BAY = 2.275            # 7.5 shaku: the town-grade hall bay (W2P2's assemblies); on the 0.455 grid
WOOD = "wood_weathered"


# ------------------------------------------------------------------------------------------------ helpers
def frames(W, D):
    return {"front": (0.0, (0.0, 0.0, 0.0)), "back": (180.0, (W, 0.0, -D)), "left": (90.0, (0.0, 0.0, -D)),
            "right": (-90.0, (W, 0.0, 0.0))}


def _lift(S, drop):
    """Everything built so far in the floor frame (y 0 = floor) -> the kit frame (y 0 = grade)."""
    H = S.H.transformed(0.0, (0.0, drop, 0.0))
    H.wear = getattr(S.H, "wear", None)
    S.H = H
    S.B.H = H
    S.posts[:] = [(x, z, y0 + drop, y1 + drop) for (x, z, y0, y1) in S.posts]


def stones_as_soseki(H):
    """The platform / en / stair stones are separate stones under posts (PLAYBOOK §6.4 rule 3): shellcheck's C8 era
    lint counts them by the 'soseki' tag (the kit names them tsuka_stone / en_stone / foot_stone)."""
    n = 0
    for s in H.solids:
        if s.tag in ("tsuka_stone", "en_stone", "foot_stone", "soseki_dressed"):
            s.tag = "soseki"
            n += 1
    return n


def hall_box(S, W, D, xs_front, front=(), kind="board_vertical", finish="nakanuri", gables=True, hip=False,
             wall_h=WALL_H, xs_side=None, open_sides=()):
    """Posts on every node, walls on four sides (front bays listed in `front` are left open for their door / lattice
    parts: {bay index: (a, b)}), keta, gable walls. Floor frame (y 0 = floor). xs_front / xs_side: post nodes."""
    F = frames(W, D)
    B = S.B
    xs_side = xs_side or [k * KEN for k in range(int(round(D / KEN)) + 1)]
    for side, xs in (("front", xs_front), ("back", xs_front), ("left", xs_side), ("right", xs_side)):
        B.posts_on(F[side], xs, 0.0, wall_h)
    kw = {"finish": finish} if kind == "shinkabe" else {"mat": WOOD}
    holes = [(a + POST / 2, b - POST / 2, 0.0, 2.0) for (a, b) in front]
    if "front" not in open_sides:
        B.wall(F["front"], "front", kind, 0.0, W, 0.0, wall_h, openings_=holes, **kw)
    for side, L in (("back", W), ("left", D), ("right", D)):
        if side not in open_sides:
            B.wall(F[side], side, kind, 0.0, L, 0.0, wall_h, **kw)
    for side, L in (("front", W), ("back", W)) + ((("left", D), ("right", D)) if hip else ()):
        k = Part("keta", "", "")
        ext = 0.06 if hip else 0.30
        frame.keta(k, -ext, L + ext, y_top=wall_h + KETA_H)
        B.put(k, F[side])
    line_board_walls(S.H)
    if gables:
        t = R.PITCH.get(gables if isinstance(gables, str) else "itabuki", 0.45)
        for side in ("left", "right"):
            g = Part("gable", "", "")
            walls.gable(g, D, t, wall_h + KETA_H, "_board")
            for s in g.solids:
                if s.tag == "gable_geo":
                    s.vis = {1}
            B.put(g, F[side])


def line_board_walls(H):
    """Board walls (walls.wall_run board_vertical) hang their boards on the posts' outer face with 4 mm gaps and nothing
    visible behind them (the collision slab is invisible): from inside, daylight shows through the gaps (C11). The slab
    becomes the walls' inner lining in Resolution 1 (as rural.Shell.gable does for the gable boards)."""
    for s in H.solids:
        if s.tag == "board_geo" and not s.vis:
            s.vis = {1}


def hide_underfloor(H, W, D, corner=0.25):
    """A boarded-skirt platform ('hall') hides what stands behind the skirt: the underfloor posts, their stones, the
    sleepers and the nuki leave the visual LODs except at the four corners, and the skirt's random boards become its
    one-slab LOD face in Resolution 1 too (under an en deck the skirt is in shadow). Budget (PLAYBOOK §12): ~1,600
    faces on a town hall. The Geometry-only underfloor block stays."""
    keep = []
    for s in H.solids:
        if s.tag in ("tsuka_stone", "yukazuka", "obiki", "nuki") and 1 in s.vis and not (s.geo or s.view or s.fire):
            b = s.bbox()
            cx, cz = (b[0] + b[1]) / 2, (b[4] + b[5]) / 2
            if s.tag in ("tsuka_stone", "yukazuka") and (abs(cx) < corner or abs(cx - W) < corner) and                     (abs(cz) < corner or abs(cz + D) < corner):
                keep.append(s)
            continue
        if s.tag == "skirt_board":
            continue
        if s.tag == "skirt_lod":
            s.vis = set(s.vis) | {1}
        keep.append(s)
    H.solids = keep


def far_trim(H, keep=("hashira",)):
    """Resolution 3 of a bracketed hall: the bracket sets under the eaves leave it (the roof covers them from above:
    C15 compares top heights only); the columns stay."""
    for s in H.solids:
        if getattr(s, "src", None) == "kumimono" and s.tag not in keep and 3 in s.vis:
            s.vis = set(s.vis) - {3}
        if s.tag in ("tsuka_stone", "en_stone", "foot_stone", "soseki", "yukazuka") and 3 in s.vis:
            s.vis = set(s.vis) - {3}            # stones and stubs at grade under the skirt / en: not a far silhouette


def far_lift(part, dy=0.04, tags=("far_body", "kawara_far"), lods=(2, 3)):
    """A SMALL curved hongawara roof (temizuya, gate): its round covers stand 0.11-0.13 m over the far field of
    Resolution 2 / 3 (C15 allows 0.10); the far field rises dy (it is far-LOD only: no collision, no Roadway)."""
    for s in part.solids:
        if s.tag in tags and s.vis and 1 not in s.vis and set(s.vis) <= set(lods) and not (s.geo or s.view or s.fire):
            s.verts = [(v[0], v[1] + dy, v[2]) for v in s.verts]
            s.center = (s.center[0], s.center[1] + dy, s.center[2])


def far_r2_in_r3(part, tags=("far_body", "kawara_far", "eave_strip", "board_field_lod", "koba_far")):
    """A SMALL curved roof: Resolution 3 uses Resolution 2's finer far field (the 2-ken x 3-band R3 field of a 1.5-ken
    roof misses the sori curve by > 0.10 m, C15); the R3-only field goes. A few dozen faces."""
    keep = []
    for s in part.solids:
        if s.tag in tags and s.vis == {3}:
            continue
        if s.tag in tags and s.vis == {2}:
            s.vis = {2, 3}
        keep.append(s)
    part.solids = keep


def remat(part, old, new):
    """Swap a library material on every solid of a part (str or per-face dict mats)."""
    for s in part.solids:
        if isinstance(s.mats, dict):
            s.mats = {k: (new if v == old else v) for k, v in s.mats.items()}
        elif s.mats == old:
            s.mats = new
        else:
            continue
        if s.fm is not None:            # already resolved per face: swap there too, world UVs at the new tile size
            from ..core import face_uvs
            s.fm = [new if m == old else m for m in s.fm]
            if not isinstance(s.uv, list):
                s.fuv = [face_uvs(s, fi, s.fn[fi], m) for fi, m in enumerate(s.fm)]


def town_frame(S, W, D, nx, nz, col_h, form, cover, c=None, nakazonae="kentozuka", y0=0.0):
    """kumimono.frame (columns, head tie, bracket sets, gangyo) in its own sub-part; the columns become the shell's
    posts (C3 grid: the 2.275 bay nodes are on the 0.455 grid)."""
    km = Part("kumimono", "", "")
    K = KM.frame(km, W, D, nx, nz, col_h, form, c=c, y0=y0, covering=cover, nakazonae=nakazonae)
    S.H.merge(km)
    for (x, z) in K["nodes"]:
        S.posts.append((round(x, 4), round(z, 4), y0, y0 + col_h))
    return K


def town_walls(S, W, D, nx, nz, c, ytop, front=None, sides=("back", "left", "right"), ceiling=True):
    """Board walls between the round columns (column face to column face), from the floor up to ytop (the head tie's
    underside); front = [spec per bay] ('wall' | a front_bay what) -> the front bays' doors / lattices with jambs at
    the column faces and a board panel over each opening; a board ceiling (tenjo) at ytop closes the room under the
    bracket zone (C11). Floor frame."""
    F = frames(W, D)
    B = S.B
    bx, bz = W / nx, D / nz
    dn = {}
    for side in ("front", "back", "left", "right"):
        n, bay = (nx, bx) if side in ("front", "back") else (nz, bz)
        for k in range(n):
            xa = k * bay + c / 2 - POST / 2
            bw = bay - c + POST
            spec = "wall"
            if side == "front":
                spec = (front or ["wall"] * n)[k]
            elif side not in sides:
                continue
            if spec == "open":
                continue
            # a shitomi bay's lower leaf is fixed: the board wall behind it stays up to the leaf joint (no slot at the
            # floor under the leaves, which hang in front of the columns: C11)
            y_lo = SH.SPLIT if spec == "shitomi" else 0.0
            holes = [] if spec == "wall" else [(xa + POST / 2, xa + bw - POST / 2, y_lo, DOOR_H)]
            # temple / shrine hall itakabe: plain boards, no battens (they are a house / shed detail)
            B.wall(F[side], "%s_%d" % (side, k), "board_vertical", xa, xa + bw, 0.0, ytop, openings_=holes, mat=WOOD,
                   board_opts={"battened": False})
            if side == "front" and spec != "wall":
                d = front_bay(S, k * bay, bay, spec, "%s (bay %d)" % (spec, k), c=c)
                if d is not None:
                    dn[k] = "DoorsTwin%d" % len(S.H.doors)
    line_board_walls(S.H)
    if ceiling:
        cp = Part("ceiling", "", "")
        cp.add(box(c / 2, W - c / 2, ytop, ytop + 0.04, -D + c / 2, -c / 2, "ceil_boards", vis=(1, 2), tag="tenjo"))
        B.interior = True
        B.merge(cp)
        B.interior = False
    return dn


def front_bay(S, x0, bay, what, label, c=POST):
    """One front bay between post / column nodes x0 and x0 + bay (floor frame, wall line z 0): what =
    'tobira_lattice_in' | 'tobira_board_in' | 'tobira_board_out' | 'tobira_sankara_in' (doors) | 'shut_board' |
    'shut_lattice' (static closed tobira: the sealed honden) | 'shitomi' (hinged upper leaf) | 'lattice' (fixed
    lattice front, a C11 portal) | 'shitomi_closed'. c: the node column size; a door bay between big round columns
    gets jambs at the column faces (the part's 0.12 posts sit inside the columns)."""
    F0 = (0.0, (0.0, 0.0, 0.0))
    xa = x0 + c / 2 - POST / 2
    bw = bay - c + POST
    B = S.B
    if what.startswith("tobira_"):
        style, swing = what.split("_")[1], what.split("_")[2]
        p = Part("tobira_%d" % int(x0 * 100), "", "")
        TB.tobira(p, 0.0, bw, style, swing)
        return B.place_door(p, F0, xa, 0.0, label=label)
    if what.startswith("shut_"):
        p = Part("tobira_shut_%d" % int(x0 * 100), "", "")
        TB.tobira(p, 0.0, bw, what.split("_")[1], "out", hinged=False, ajar=0.0)
        B.put(p, F0, xa)
        return None
    if what == "shitomi":
        p = Part("shitomi_%d" % int(x0 * 100), "", "")
        if c > POST + 1e-6:
            # between big round columns the hinged leaf hangs IN FRONT of them (column centre to centre), so it swings
            # up clear of the column faces and closes over them (no slit at the jambs)
            SH.shitomi(p, 0.0, bay + POST, "_hinged")
            return B.place_door(p, (0.0, (0.0, 0.0, c / 2 - POST / 2 + 0.006)), x0 - POST / 2, 0.0, label=label)
        SH.shitomi(p, 0.0, bw, "_hinged")
        return B.place_door(p, F0, xa, 0.0, label=label)
    if what in ("lattice", "shitomi_closed"):
        p = Part("lattice_%d" % int(x0 * 100), "", "")
        SH.shitomi(p, 0.0, bw, "_fixed" if what == "lattice" else "_closed")
        B.put(p, F0, xa)
        if what == "lattice":
            S.portals.append(("lattice %.2f" % x0, (xa + 0.06, xa + bw - 0.06, 0.62, 2.0, -0.10, 0.10)))
        return None
    raise ValueError(what)


def lift_portals(S, drop, n0=0):
    S.portals[n0:] = [(n, (b[0], b[1], b[2] + drop, b[3] + drop, b[4], b[5])) for n, b in S.portals[n0:]]


def en_rooms(S, W, D, drop, sides, depth=KR.DEPTH, z0=0.12, returns=False, side_len=None):
    """The en as an open floor (loot on it; C11 skips it). z0: where the front en's floor starts (a town hall's
    shitomido hang in front of its round columns). returns: the front en ends in koran returns (FX1): keep clear of
    them."""
    rects = []
    if "front" in sides:
        e = 0.20 if returns else 0.10
        x0 = -depth + 0.15 if ("left" in sides) else e
        x1 = W + depth - 0.15 if ("right" in sides) else W - e
        rects.append(("en", (x0, x1, z0, depth - 0.18)))
    for sd, sg in (("left", -1), ("right", 1)):
        if sd in sides:
            xa, xb = (-depth + 0.15, -0.12) if sg < 0 else (W + 0.12, W + depth - 0.15)
            rects.append(("en_" + sd, (xa, xb, -(D if side_len is None else side_len) + 0.25,
                                       0.10 if "front" not in sides else 0.0)))
    for nm, rc in rects:
        S.room(nm, "veranda", "boards", drop, rc, [], "the en (veranda) round the hall: open, railed", enclosed=False)


def stair_obstacle(S, room, K):
    """The koran posts at the kizahashi's head stay clear of loot on the en (the stair head itself may hold loot)."""
    for x in (K["xa"], K["xb"]):
        S.obst.append((room, _r(x - 0.18, x + 0.18, KR.DEPTH - 0.30, KR.DEPTH + 0.2)))


# ------------------------------------------------------------------------------------------------ SH2 haiden
def haiden(name=None, grade="village", cover="hiwada", wear="_w1"):
    if grade == "town":
        return _haiden_town(name, cover, wear)
    W, D, drop = 3 * KEN, 2 * KEN, 0.60
    S = Shell(name or "jp_shrine_haiden", W, D, [1, 2], "worship hall (haiden), village", wear)
    STL.platform(S.H, W, D, drop, "hall")
    xs = [k * KEN for k in range(4)]
    hall_box(S, W, D, xs, front=[(0.0, KEN), (KEN, 2 * KEN), (2 * KEN, 3 * KEN)])
    S.door(TB.part_tobira("_lattice_in"), (0.0, (0.0, 0.0, 0.0)), KEN, 0.0, "Haiden doors (lattice, open in)", "front")
    n0 = len(S.portals)
    for k in (0, 2):
        front_bay(S, k * KEN, KEN, "lattice", "")
    en = KR.en_wrap(S.H, W, D, drop=drop, style="plain", sides=("front",), stair=W / 2, waki=False,
                    returns=True)  # FX1: koran returns at the en ends
    rp = Part("roof", "", "")
    sls, info = R.roof(rp, W, D, "kirizuma", "itabuki", eave_y=EAVE_Y)
    (x0, yr, zr), (x1, _, _) = info["ridge"]
    for x, sg in ((x0, -1), (x1, 1)):
        ORN.oniita(rp, x, yr + 0.04, zr, sg)
    S.H.merge(rp)
    kp = Part("kohai", "", "")
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    NG.kohai(kp, KEN, 2 * KEN, zp, R.PITCH["itabuki"], R.EAVE_OV["itabuki"], EAVE_Y, "itabuki", drop)
    S.H.merge(kp)
    _lift(S, drop)
    lift_portals(S, drop, n0)
    S.room("haiden", "worship", "boards", drop, (POST / 2, W - POST / 2, -D + POST / 2, -POST / 2), [S.dn["front"]],
           "worship floor: offering box + bell rope in front of the middle bay, drum, ema on the walls")
    en_rooms(S, W, D, drop, ("front",), returns=True)
    stair_obstacle(S, "en", en["stair"])
    fit(S, "saisen_bako", "en", centre=(W / 2, 0.45), size=(1.20, 0.50), yaw=0.0, y=drop,
        note="offering box (saisen-bako) on the en in front of the doors")
    fit(S, "suzu", "en", centre=(W / 2, 0.55), size=(0.3, 0.3), yaw=0.0, y=round(drop + 2.30, 2), obstacle=False,
        note="bell (suzu) with its cloth rope, hung from the kohai beam / eave over the offering box")
    fit(S, "drum", "haiden", centre=(0.70, -D + 0.70), size=(0.8, 0.8), yaw=0.0, y=drop,
        note="big drum (taiko) on its stand in a back corner")
    fit(S, "kamidana", "haiden", rect=(W / 2 - 0.6, W / 2 + 0.6, -D + A_ + 0.02, -D + A_ + 0.40), y=drop + 1.60,
        obstacle=False, note="offering shelf / gohei stand on the back wall (towards the honden)")
    hide_underfloor(S.H, W, D)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "haiden", "grade": grade}, "levels": {"floor": drop, "eave": drop + EAVE_Y},
                     "stair": en["stair"]})


def _haiden_town(name, cover, wear):
    """Town haiden: 3 x 2 bays of 2.275 on a boarded raised floor (+0.75), hira-mitsudo bracket sets on round columns,
    board walls + a board ceiling, the en on three sides with giboshi koran, wakishoji, kizahashi, the middle bay's
    lattice tobira and hinged shitomido in the side bays, curved irimoya (hiwada / copper), a kohai over the stair fitted
    under the curved eave (sori.kohai_fit)."""
    nx, nz, bay = 3, 2, TOWN_BAY
    W, D, drop, col_h = nx * bay, nz * bay, 0.75, 3.0
    S = Shell(name or "jp_shrine_haiden_town", W, D, [2, 3], "worship hall (haiden), town, %s" % cover, wear)
    STL.platform(S.H, W, D, drop, "hall")
    K = town_frame(S, W, D, nx, nz, col_h, "mitsudo", cover)
    c = K["c"]
    ytop = col_h - 0.62 * c
    n0 = len(S.portals)
    dn = town_walls(S, W, D, nx, nz, c, ytop, front=["shitomi", "tobira_lattice_in", "shitomi"])
    S.dn["front"] = dn[1]
    en = KR.en_wrap(S.H, W, D, drop=drop, style="giboshi", sides=("front", "left", "right"), stair=W / 2, waki=True)
    rp = Part("roof", "", "")
    sls, info = SO.roof(rp, W, D, "irimoya", cover, bear_y=K["bear_y"], g_out=K["g_out"], ov=K["g_out"] + 1.45)
    S.H.merge(rp)
    kf = SO.kohai_fit(info)
    kp = Part("kohai", "", "")
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    NG.kohai(kp, bay, 2 * bay, zp, kf["main_t"], kf["main_ov"], kf["eave_y"], "itabuki", drop)
    remat(kp, "roof_kokera", "roof_hiwada" if cover == "hiwada" else "roof_copper")
    S.H.merge(kp)
    _lift(S, drop)
    lift_portals(S, drop, n0)
    S.room("haiden", "worship", "boards", drop, (c / 2 + 0.03, W - c / 2 - 0.03, -D + c / 2 + 0.03, -c / 2 - 0.03),
           [S.dn["front"]], "worship floor: offering box + bell rope in front of the middle bay, drum, ema, gaku")
    en_rooms(S, W, D, drop, ("front", "left", "right"), z0=0.32)
    stair_obstacle(S, "en", en["stair"])
    fit(S, "saisen_bako", "en", centre=(W / 2, 0.50), size=(1.50, 0.55), yaw=0.0, y=drop,
        note="big slatted offering box (saisen-bako) on the en before the middle bay")
    fit(S, "suzu", "en", centre=(W / 2, 0.60), size=(0.3, 0.3), yaw=0.0, y=round(drop + 2.40, 2), obstacle=False,
        note="bell (suzu) with its thick cloth rope, hung from the kohai beam over the offering box")
    fit(S, "drum", "haiden", centre=(0.85, -D + 0.85), size=(0.9, 0.9), yaw=0.0, y=drop,
        note="big drum (odaiko) on its stand")
    fit(S, "gaku", None, centre=(W / 2, 0.10), size=(1.2, 0.1), yaw=0.0, y=round(drop + ytop - 0.55, 2),
        obstacle=False, note="name board (gaku) over the middle bay, outside")
    fit(S, "kamidana", "haiden", rect=(W / 2 - 0.8, W / 2 + 0.8, -D + c / 2 + 0.03, -D + c / 2 + 0.45),
        y=round(drop + 1.60, 2), obstacle=False, note="offering shelf / gohei stands on the back wall (towards the honden)")
    hide_underfloor(S.H, W, D)
    far_trim(S.H)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "haiden", "grade": "town", "cover": cover},
                     "levels": {"floor": drop, "eave": round(drop + K["bear_y"], 3)}, "stair": en["stair"],
                     "kumimono": {k: v for k, v in K.items() if k != "nodes"}})


# ------------------------------------------------------------------------------------------------ SH3 honden
def honden(name=None, style="nagare", grade="village", chigi=False, wear="_w1"):
    if style == "shinmei":
        return _honden_shinmei(name, wear)
    if grade == "town":
        return _honden_nagare_town(name, wear)
    W = D = KEN
    drop = 1.0
    S = Shell(name or "jp_shrine_honden", W, D, [1, 2, 3], "main sanctuary (honden), nagare, village", wear)
    STL.platform(S.H, W, D, drop, "honden")
    hall_box(S, W, D, [0.0, KEN], front=[(0.0, KEN)])
    front_bay(S, 0.0, KEN, "shut_board", "")
    en = KR.en_wrap(S.H, W, D, drop=drop, style="giboshi", stair=W / 2, waki=True)
    rp = Part("roof", "", "")
    sls, info = NG.nagare(rp, W, D, drop=drop, gov=0.60)
    if chigi:
        top = info.get("ridge_top", info["ridge"][0][1] + 0.08)
        for x in (-0.50, W + 0.50):
            ORN.chigi(rp, x, top - 0.02, -D / 2, cut="soto")
        ORN.katsuogi(rp, -0.6, W + 0.6, top - 0.01, -D / 2, n=3, r=0.07, length=0.70, inset=0.45)
    S.H.merge(rp)
    _lift(S, drop)
    sides = ("front", "left", "right")
    en_rooms(S, W, D, drop, sides)
    stair_obstacle(S, "en", en["stair"])
    fit(S, "sanctum", None, rect=(A_, W - A_, -D + A_, -A_), y=drop, obstacle=False,
        note="the sealed sanctum (shintai in a zushi, mirror, gohei): seen through the doors only; dressing behind "
             "the closed tobira")
    fit(S, "offering_table", "en", centre=(W / 2, 0.55), size=(0.9, 0.45), yaw=0.0, y=drop, obstacle=False,
        note="hassoku-an offering table with sanbo on the en before the doors")
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "honden", "style": style, "grade": "village", "chigi": chigi},
                     "levels": {"floor": drop}, "stair": en["stair"], "sealed": True})


# ------------------------------------------------------------------------------------------------ BU1 small hall (do)
def do(name=None, size=3, roof="tile", grade="village", wear="_w1"):
    if grade == "town":
        return _do_town(name, wear)
    W = D = size * KEN
    drop = 0.60
    S = Shell(name or "jp_temple_do", W, D, [1, 2], "small sacred hall (do), %d x %d ken, %s" % (size, size, roof),
              wear)
    STL.platform(S.H, W, D, drop, "hall")
    xs = [k * KEN for k in range(size + 1)]
    fam = {"tile": "sangawara", "board": "itabuki", "thatch": "thatch"}[roof]
    kind = "shinkabe" if roof == "tile" else "board_vertical"
    bays = [(k * KEN, (k + 1) * KEN) for k in range(size)]
    thatch = roof == "thatch"
    E = EAVE_Y
    hall_box(S, W, D, xs, front=bays, kind=kind, gables=False, hip=True, wall_h=E - KETA_H)
    n0 = len(S.portals)
    F0 = (0.0, (0.0, 0.0, 0.0))
    if size == 3:
        S.door(TB.part_tobira("_sankara_in"), F0, KEN, 0.0, "Hall doors (sankarado, open in)", "front")
        for k in (0, 2):
            front_bay(S, k * KEN, KEN, "shitomi", "Shitomido %d (upper leaf)" % k)
    elif thatch:
        # the thatched rural do: no en (the thatch eave hangs low over it); a lattice door with a cut step, a fixed
        # lattice front beside it
        S.door(TB.part_tobira("_lattice_in"), F0, 0.0, 0.0, "Hall doors (lattice, open in)", "front")
        front_bay(S, KEN, KEN, "lattice", "")
        st = Part("step", "", "")
        found.step(st, KEN / 2, "cut", drop=drop, width=1.10)
        S.B.put(st, F0, 0.0, 0.0, what="found.step (cut) at the door")
    else:
        S.door(TB.part_tobira("_lattice_in"), F0, 0.0, 0.0, "Hall doors left (lattice, open in)", "front")
        S.door(TB.part_tobira("_lattice_in"), F0, KEN, 0.0, "Hall doors right (lattice, open in)", "front2")
    en = None
    if not thatch:
        en = KR.en_wrap(S.H, W, D, drop=drop, style="plain", sides=("front",), stair=W / 2, waki=False,
                        returns=True)  # FX1: koran returns at the en ends
    rp = Part("roof", "", "")
    if thatch:
        sls, info = NG._hogyo_thatch(rp, W)
    else:
        sls, info = NG.hogyo(rp, W, fam, eave_y=E, apex="hoju_kawara" if roof == "tile" else "hoju_bronze")
    S.H.merge(rp)
    if not thatch:
        kp = Part("kohai", "", "")
        zp = KR.DEPTH + KR.stair_flight(drop)[0]
        kx = (KEN, 2 * KEN) if size == 3 else (KEN / 2, 1.5 * KEN)
        NG.kohai(kp, kx[0], kx[1], zp, R.PITCH[fam], R.EAVE_OV[fam], E, fam, drop)
        S.H.merge(kp)
    _lift(S, drop)
    lift_portals(S, drop, n0)
    doors = [S.dn["front"]] + ([S.dn["front2"]] if "front2" in S.dn else [])
    S.room("hall", "worship", "boards", drop, (POST / 2, W - POST / 2, -D + POST / 2, -POST / 2), doors,
           "one-room hall: the statue on an altar shelf at the back; also the village meeting place")
    if en:
        en_rooms(S, W, D, drop, ("front",), returns=True)
        stair_obstacle(S, "en", en["stair"])
    fit(S, "altar", "hall", rect=(W / 2 - 0.9, W / 2 + 0.9, -D + A_ + 0.02, -D + A_ + 0.80), y=drop,
        note="altar shelf / dais (shumidan) with the statue (Jizo / Kannon / Yakushi / Koshin / Enma), incense burner, "
             "candle stands, vases, bowl gong")
    fit(S, "saisen_bako", "en" if en else None, centre=(W / 2, 0.45) if en else (1.5 * KEN, 0.45), size=(1.0, 0.45),
        yaw=0.0, y=drop if en else 0.0, obstacle=bool(en),
        note="donation box on the en before the doors" if en else "donation box on the ground before the lattice front")
    fit(S, "gong", "en" if en else None, centre=(W / 2, 0.55) if en else (KEN / 2, 0.30), size=(0.3, 0.3), yaw=0.0,
        y=round(drop + 2.25, 2), obstacle=False, note="waniguchi gong + rope hung under the eave / kohai before the doors")
    hide_underfloor(S.H, W, D)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "do", "size": size, "roof": roof, "grade": "village"},
                     "levels": {"floor": drop, "eave": drop + E}, "stair": en["stair"] if en else None})


def _honden_shinmei(name, wear):
    """Shinmei honden: 1 x 1 ken hirairi on stilts (+1.00), straight kirizuma board roof, the free-standing ridge posts
    (munamochi-bashira) outside both gables, okichigi (soto) + 5 katsuogi, a front en with giboshi koran and the kizahashi;
    board tobira, sealed."""
    W = D = KEN
    drop = 1.0
    S = Shell(name or "jp_shrine_honden_shinmei", W, D, [1, 2, 3], "main sanctuary (honden), shinmei", wear)
    STL.platform(S.H, W, D, drop, "honden")
    hall_box(S, W, D, [0.0, KEN], front=[(0.0, KEN)])
    front_bay(S, 0.0, KEN, "shut_board", "")
    en = KR.en_wrap(S.H, W, D, drop=drop, style="giboshi", sides=("front",), stair=W / 2, waki=False,
                    returns=True)  # FX1: koran returns at the en ends
    rp = Part("roof", "", "")
    sls, info = R.roof(rp, W, D, "kirizuma", "itabuki", eave_y=EAVE_Y, gov=0.55)
    (x0, yr, zr), (x1, _, _) = info["ridge"]
    top = yr + 0.10
    for x in (x0 - 0.02, x1 + 0.02):
        ORN.chigi(rp, x, top - 0.02, zr, cut="soto")
    ORN.katsuogi(rp, x0, x1, top - 0.01, zr, n=5, r=0.075, length=0.80, inset=0.25)
    for s in rp.solids:
        if s.tag == "katsuogi_end":
            s.vis = set(s.vis) | {2, 3}      # C15: the far logs keep their end caps (the outline)
    S.H.merge(rp)
    # munamochi-bashira: a free-standing post at each gable end, from a stone at grade up under the ridge board
    t = R.PITCH["itabuki"]
    yu = EAVE_Y + t * (D / 2 - 0.10) - 0.12
    mp = Part("munamochi", "", "")
    for x in (-0.30, W + 0.30):
        mp.add(cyl("y", x, -D / 2, 0.11, -drop, yu, WOOD, n=8, vis=(1, 2, 3), geo=True, view=True, fire=True,
                   tag="munamochi"))
        found.soseki(mp, x, -D / 2, 3)
        for s in mp.solids[-2:]:
            s.verts = [(v[0], v[1] - drop, v[2]) for v in s.verts]
            s.center = (s.center[0], s.center[1] - drop, s.center[2])
    S.H.merge(mp)
    _lift(S, drop)
    en_rooms(S, W, D, drop, ("front",), returns=True)
    stair_obstacle(S, "en", en["stair"])
    fit(S, "sanctum", None, rect=(A_, W - A_, -D + A_, -A_), y=drop, obstacle=False,
        note="the sealed sanctum (shintai in a zushi, mirror, gohei): seen through the doors only")
    fit(S, "offering_table", "en", centre=(W / 2, 0.55), size=(0.9, 0.45), yaw=0.0, y=drop, obstacle=False,
        note="hassoku-an offering table with sanbo on the en before the doors")
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "honden", "style": "shinmei"}, "levels": {"floor": drop},
                     "stair": en["stair"], "sealed": True})


def _honden_nagare_town(name, wear):
    """Town nagare honden: sangen-sha 3 x 1.5 ken on stilts (+1.00), CURVED nagare hiwada (nagare.nagare(curve=
    sori.nagare)) with its kohai posts, lattice tobira in all three bays (sealed), en on three sides with giboshi koran,
    wakishoji, kizahashi."""
    W, D = 3 * KEN, 1.5 * KEN
    drop = 1.0
    S = Shell(name or "jp_shrine_honden_town", W, D, [2, 3], "main sanctuary (honden), nagare sangen-sha, town", wear)
    STL.platform(S.H, W, D, drop, "honden")
    xs = [k * KEN for k in range(4)]
    hall_box(S, W, D, xs, front=[(k * KEN, (k + 1) * KEN) for k in range(3)],
             xs_side=[0.0, 0.5 * KEN, 1.5 * KEN], wall_h=WALL_H - 0.06)
    for k in range(3):
        front_bay(S, k * KEN, KEN, "shut_lattice", "")
    en = KR.en_wrap(S.H, W, D, drop=drop, style="giboshi", stair=W / 2, waki=True)
    rp = Part("roof", "", "")
    sls, info = NG.nagare(rp, W, D, fam="itabuki", drop=drop, gov=0.60, kohai_xs=(KEN, 2 * KEN), curve=SO.nagare)
    remat(rp, "roof_kokera", "roof_hiwada")
    S.H.merge(rp)
    _lift(S, drop)
    en_rooms(S, W, D, drop, ("front", "left", "right"))
    stair_obstacle(S, "en", en["stair"])
    fit(S, "sanctum", None, rect=(A_, W - A_, -D + A_, -A_), y=drop, obstacle=False,
        note="three sealed sanctum bays (a zushi each): seen through the lattice doors only")
    fit(S, "offering_table", "en", centre=(W / 2, 0.55), size=(1.2, 0.45), yaw=0.0, y=drop,
        note="hassoku-an offering tables with sanbo on the en before the doors")
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "honden", "style": "nagare", "grade": "town"}, "levels": {"floor": drop},
                     "stair": en["stair"], "sealed": True})


# ------------------------------------------------------------------------------------------------ SH5 temizuya
def column_bases(H, nodes, c, y_top=0.0):
    for (x, z) in nodes:
        H.add(cyl("y", x, z, 0.78 * c, y_top - 0.14, y_top, "stone_cut", n=8, vis=(1, 2), geo=True, view=True,
                  fire=True, tag="soseki"))


def paving(H, x0, x1, z0, z1, y=0.08, name="pad"):
    """A cut-stone pad (individual slabs in Resolution 1 over one Geometry / Roadway slab), top y."""
    p = Part(name, "", "")
    p.add(box(x0, x1, -0.12, y - 0.02, z0, z1, "stone_cut", vis=(2, 3), geo=True, view=True, fire=True, tag="pad"))
    p.road([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], "stone_ext")
    nx = max(1, int(round((x1 - x0) / 0.60)))
    nz = max(1, int(round((z1 - z0) / 0.45)))
    for i in range(nx):
        for j in range(nz):
            a0 = x0 + (x1 - x0) * i / nx + (0.15 if j % 2 and i == 0 else 0.0)
            a1 = x0 + (x1 - x0) * (i + 1) / nx - (0.0 if not (j % 2 and i == nx - 1) else 0.0)
            b0, b1 = z0 + (z1 - z0) * j / nz, z0 + (z1 - z0) * (j + 1) / nz
            p.add(box(a0 + 0.006, a1 - 0.006, -0.12, y, b0 + 0.006, b1 - 0.006, "stone_cut", vis=(1,), tag="paving",
                      uvoff=((i * 0.37) % 1, (j * 0.61) % 1)))
    p.add(box(x0, x1, -0.12, y - 0.02, z0, z1, "stone_cut", vis=(1,), tag="pad_base"))
    H.merge(p)


def temizuya(name=None, grade="village", wear="_w1"):
    """Four posts over the basin spot, 1.5 x 1 ken, a cut-stone pad: village straight kirizuma boards, town curved
    kirizuma hongawara on funa-hijiki round columns. The basin is a site prop (W2's jp_s_basin_*): its spot is left."""
    W, D = 1.5 * KEN, KEN
    S = Shell(name or "jp_shrine_temizuya", W, D, [1, 2, 3], "purification pavilion (temizuya), %s" % grade, wear)
    paving(S.H, -0.55, W + 0.55, -D - 0.55, 0.55)
    yp = 0.08
    if grade == "town":
        km = Part("kumimono", "", "")
        K = KM.frame(km, W, D, 1, 1, 2.75, "funa", c=0.22, y0=yp, covering="hongawara", nakazonae=None, nageshi=False)
        S.H.merge(km)
        column_bases(S.H, K["nodes"], K["c"], yp)
        for (x, z) in K["nodes"]:
            S.posts.append((x, z, yp, yp + 2.75))
        rp = Part("roof", "", "")
        sls, info = SO.roof(rp, W, D, "kirizuma", "hongawara", bear_y=K["bear_y"], g_out=K["g_out"],
                            ov=K["g_out"] + 0.95, gov=0.75, corner_lift=0.08)
        far_lift(rp)
        far_r2_in_r3(rp)
        S.H.merge(rp)
        eave = K["bear_y"]
    else:
        E = 2.75
        for (x, z) in ((0.0, 0.0), (W, 0.0), (0.0, -D), (W, -D)):
            S.post(x, z, E - KETA_H, y0=yp, stone=False)
        for (x, z) in ((0.0, 0.0), (W, 0.0), (0.0, -D), (W, -D)):
            found.soseki(S.H, x, z, int(x * 10 + z * 3) % 8)
            for s in S.H.solids[-2:]:
                s.verts = [(v[0], v[1] + yp, v[2]) for v in s.verts]
                s.center = (s.center[0], s.center[1] + yp, s.center[2])
        S.keta_ring(W, D, E, hip=False)
        tb = Part("tiebeam", "", "")
        for x in (0.0, W):
            tb.add(box(x - 0.05, x + 0.05, E - KETA_H - 0.30, E - KETA_H - 0.15, -D - 0.04, 0.04, WOOD, vis=(1, 2),
                       geo=True, view=True, fire=True, tag="nuki"))
        S.H.merge(tb)
        rp = Part("roof", "", "")
        sls, info = R.roof(rp, W, D, "kirizuma", "itabuki", eave_y=E, gov=0.45)
        (x0, yr, zr), (x1, _, _) = info["ridge"]
        for x, sg in ((x0, -1), (x1, 1)):
            ORN.oniita(rp, x, yr + 0.04, zr, sg)
        S.H.merge(rp)
        eave = E
    S.room("pavilion", "worship", "stone", yp, (-0.45, W + 0.45, -D - 0.45, 0.45), [],
           "open pavilion over the stone basin: wash hands and mouth before the shrine", enclosed=False)
    fit(S, "basin", "pavilion", centre=(W / 2, -D / 2), size=(1.10, 0.70), yaw=0.0, y=yp,
        note="the stone basin (chozubachi, W2 site prop jp_s_basin_*) with its bamboo spout and ladle rack (hishaku)")
    for (x, z) in ((0.0, 0.0), (W, 0.0), (0.0, -D), (W, -D)):
        S.obst.append(("pavilion", _r(x - 0.20, x + 0.20, z - 0.20, z + 0.20)))
    far_trim(S.H)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "temizuya", "grade": grade}, "levels": {"floor": yp, "eave": round(eave, 3)}})


# ------------------------------------------------------------------------------------------------ SH6 shamusho
def shamusho(name=None, roof="sangawara", wear="_w1"):
    """Priests' office with the amulet window: 3 x 2 ken, a doma by the door (1 ken) and the raised board office
    (0.40) behind its push-up counter shutter on the front; board walls (village, itabuki) or nakanuri + koshiita
    (town, sangawara). As civic.guardhut, larger."""
    W, D = 3 * KEN, 2 * KEN
    E = 3.03
    YT = E - KETA_H
    YG = E - 0.21
    AG = 0.40
    t = R.PITCH[roof]
    S = Shell(name or "jp_shrine_shamusho", W, D, [2, 3], "priests' office + amulet window (shamusho), %s" % roof, wear)
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    wk = dict(kind="board_vertical", mat=WOOD, grime=False) if roof == "itabuki" else dict(finish="nakanuri",
                                                                                            koshiita=0.90)
    XB = KEN
    # front: the door at lx 0..1k (its leaf parks over the next bay's plain wall), the counter shutter at 2..2.5 ken
    S.wall_line("front", [(0.0, XB, DOMA), (XB, W, AG)], YT,
                [(0.0, KEN, DOMA, DOMA + 2.0, "door"), (2.0 * KEN, 2.5 * KEN, AG + 0.85, AG + 1.65, "window")],
                nodes_extra=(1.5 * KEN, 2.0 * KEN, 2.5 * KEN), **wk)
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Door (katabiki)", "front")
    S.window(openings.part_tsukiage("_board"), "front", 2.0 * KEN, AG + 0.05, "Amulet window (push-up counter shutter)")
    S.wall_line("back", [(0.0, W - XB, AG), (W - XB, W, DOMA)], YT,
                [(0.5 * KEN, 1.0 * KEN, AG + 0.90, AG + 1.65, "window")], nodes_extra=(W - XB,), **wk)
    S.window(openings.part_window_slide("_board"), "back", 0.5 * KEN, AG, "Office window (back)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, (), **wk)
    S.wall_line("right", [(0.0, D, AG)], YG, [(0.5 * KEN, 1.0 * KEN, AG + 0.90, AG + 1.65, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN), **wk)
    S.window(openings.part_window_slide("_board"), "right", 0.5 * KEN, AG, "Office window (end)")
    for g in ("left", "right"):
        S.gable(g, D, t, E, "_board" if roof == "itabuki" else "_tile")
    S.B.interior = True
    S.B.merge(FL.doma("doma", 0.0, XB, -D, 0.0, road=(A_, XB - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    S.B.merge(FL.boards("office", XB + 0.06, W - A_, -D + A_, -A_, AG, mats=FL.MATS_BOARDS_B1))
    S.B.interior = False
    S.kamachi((90.0, (XB, 0.0, -D)), D, AG, [D / 2], "doma", soot=False)
    S.place_windows()
    fit(S, "amulet_counter", "office", rect=(2.0 * KEN - 0.05, 2.5 * KEN + 0.05, -0.60, -A_), y=AG, obstacle=False,
        note="behind the push-up counter shutter: the amulet counter (ofuda / omamori stacks, the shrine seal)")
    fit(S, "desk", "office", centre=(W - 0.80, -D + 0.70), size=(1.0, 0.5), yaw=0.0, y=AG,
        note="talisman-making desk with printing blocks, brushes, registers; ritual robes on a rack by the end wall")
    fit(S, "kamidana", "office", rect=(XB + 0.4, XB + 1.4, -D + A_ + 0.02, -D + A_ + 0.35), y=AG + 1.75,
        obstacle=False, note="kamidana shelf high on the back wall")
    S.room("doma", "doma", "earth", DOMA, (A_, XB - 0.07, -D + A_, -A_), [S.dn["front"]],
           "earth-floored entry: sandals off at the step")
    S.room("office", "office", "boards", AG, (XB + 0.045, W - A_, -D + A_, -A_), [],
           "the priests' office behind the amulet window, open to the doma")
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "shamusho", "roof": roof}, "levels": {"doma": DOMA, "floor": AG, "eave": E},
                     "koyagumi": K["counts"]}, exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or
                    abs(x) < 1e-6 or abs(x - W) < 1e-6)


# ------------------------------------------------------------------------------------------------ SH4 kagura stage
def _stage_rails(S, W, D, xs_front, xs_side, c, stair_side, K):
    """Koran on the stage edges between the posts / columns (open front and sides), the gap for the stair on
    stair_side (local K xa..xb along that side)."""
    rl = Part("koran", "", "")
    e = c / 2 + 0.006

    def run(p0, p1, lift):
        KR.rail(rl, p0, p1, "plain", ends=("open", "open"), lift=lift)
    for i in range(len(xs_front) - 1):
        run((xs_front[i] + e, 0.0), (xs_front[i + 1] - e, 0.0), 0.0)
    for sd, x in (("left", 0.0), ("right", W)):
        zs = [-z for z in xs_side]                     # side nodes, front (0) to back (-D)
        for i in range(len(zs) - 1):
            a, b = zs[i] - e, zs[i + 1] + e            # a > b (front to back)
            if sd == stair_side:
                # local x of the left frame = z + D: the stair occupies z in (xa - D, xb - D)
                ga, gb = K["xb"] - D + 0.06, K["xa"] - D - 0.06
                if a > ga and b < gb:
                    run((x, a), (x, ga), 0.015)
                    run((x, gb), (x, b), 0.015)
                    continue
            run((x, a), (x, b), 0.015)
    S.H.merge(rl)


def kagura(name=None, grade="village", wear="_w1"):
    """Kagura stage: 2 x 2 ken (village, posts) / 2 x 2 bays of 1.82 on round columns (town), stage floor +1.00 on
    the open stilts platform, open on three sides with a koran on the edges, a board back wall (the dressing-room side),
    a kizahashi down the left side (the performers' side); roof: straight kokera kirizuma with board gables (village) /
    curved kokera irimoya on funa-hijiki (town)."""
    W = D = 2 * KEN
    drop = 1.0
    S = Shell(name or "jp_shrine_kagura", W, D, [2, 3], "kagura stage (kagura-den), %s" % grade, wear)
    STL.platform(S.H, W, D, drop, "honden")
    F = frames(W, D)
    xs = [0.0, KEN, 2 * KEN]
    if grade == "town":
        K = town_frame(S, W, D, 2, 2, 2.95, "funa", "kokera", c=0.20, nakazonae=None)
        c = K["c"]
        town_walls(S, W, D, 2, 2, c, 2.95 - 0.62 * c, front=["open", "open"], sides=("back",), ceiling=False)
        rp = Part("roof", "", "")
        sls, info = SO.roof(rp, W, D, "irimoya", "kokera", bear_y=K["bear_y"], g_out=K["g_out"], ov=K["g_out"] + 1.05)
        S.H.merge(rp)
    else:
        c = POST
        for (x, z) in [(x, 0.0) for x in (0.0, W)] + [(x, -D) for x in xs] + [(0.0, -KEN), (W, -KEN)]:
            S.B.posts_on((0.0, (0.0, 0.0, 0.0)), [x], 0.0, WALL_H) if z == 0.0 else \
                S.B.posts_on((0.0, (0.0, 0.0, z)), [x], 0.0, WALL_H)
        S.B.wall(F["back"], "back", "board_vertical", 0.0, W, 0.0, WALL_H, mat=WOOD)
        line_board_walls(S.H)
        hd = Part("heads", "", "")
        for side, L in (("front", W), ("back", W), ("left", D), ("right", D)):
            if side in ("front", "back"):
                k = Part("keta", "", "")
                frame.keta(k, -0.30, L + 0.30, y_top=EAVE_Y)
                S.B.put(k, F[side])
            if side != "back":
                n = Part("nuki", "", "")
                n.add(box(0.06, L - 0.06, WALL_H - 0.35, WALL_H - 0.23, -0.04, 0.04, WOOD, vis=(1, 2), geo=True,
                          view=True, fire=True, tag="nuki"))
                S.B.put(n, F[side])
        S.H.merge(hd)
        # a gable (kirizuma) board roof: roofs.roof's straight irimoya in boards leaves its hips uncovered (no hip
        # rolls); the town stage has the curved irimoya
        rp = Part("roof", "", "")
        sls, info = R.roof(rp, W, D, "kirizuma", "itabuki", eave_y=EAVE_Y, gov=0.45)
        (x0, yr, zr), (x1, _, _) = info["ridge"]
        for x, sg in ((x0, -1), (x1, 1)):
            ORN.oniita(rp, x, yr + 0.04, zr, sg)
        S.H.merge(rp)
        for side in ("left", "right"):
            g = Part("gable", "", "")
            walls.gable(g, D, R.PITCH["itabuki"], EAVE_Y, "_board")
            for s in g.solids:
                if s.tag == "gable_geo":
                    s.vis = {1}
            S.B.put(g, F[side])
    # the stair down the left side (local frame of the left wall: x = z + D along the side, +z out = -x)
    sp = Part("stair", "", "")
    Kst = KR.kizahashi(sp, D / 2 - 0.30, 0.06, drop=drop, style="plain")
    S.B.put(sp, F["left"], what="koran.kizahashi down the left side")
    _stage_rails(S, W, D, [0.0, W] if grade != "town" else [0.0, KEN, W], [0.0, KEN, 2 * KEN], c, "left", Kst)
    _lift(S, drop)
    S.room("stage", "worship", "boards", drop, (c / 2 + 0.05, W - c / 2 - 0.05, -D + c / 2 + 0.05, -c / 2 - 0.05), [],
           "the dance stage: open on three sides, the musicians at the back wall", enclosed=False)
    fit(S, "drum", "stage", centre=(W - 0.6, -D + 0.55), size=(0.8, 0.6), yaw=0.0, y=drop,
        note="big drum (odaiko) + small drums, flutes on a rack at the back wall")
    fit(S, "masks", "stage", rect=(0.5, 1.6, -D + c / 2 + 0.02, -D + c / 2 + 0.20), y=drop + 1.50, obstacle=False,
        note="masks on pegs, kagura bells (suzu) on a stand, gohei, fans (back wall)")
    far_trim(S.H)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "kagura", "grade": grade}, "levels": {"floor": drop}, "stair": Kst})


# ------------------------------------------------------------------------------------------------ BU1 town do
def _do_town(name, wear):
    """Town small hall: 3 x 3 bays of 2.275 on a boarded raised floor (+0.75), oto-hijiki (daito + arm) on round
    columns, board walls + ceiling, curved hogyo (yosemune on a square plan) in COPPER with a bronze hoju, sankarado in
    the middle bay, hinged shitomido beside, front en with giboshi koran + kizahashi, a copper kohai."""
    n, bay = 3, TOWN_BAY
    W = D = n * bay
    drop, col_h = 0.75, 3.0
    S = Shell(name or "jp_temple_do_town", W, D, [2, 3], "small sacred hall (do), town, curved copper hogyo", wear)
    STL.platform(S.H, W, D, drop, "hall")
    K = town_frame(S, W, D, n, n, col_h, "oto", "copper")
    c = K["c"]
    ytop = col_h - 0.62 * c
    n0 = len(S.portals)
    dn = town_walls(S, W, D, n, n, c, ytop, front=["shitomi", "tobira_sankara_in", "shitomi"])
    S.dn["front"] = dn[1]
    en = KR.en_wrap(S.H, W, D, drop=drop, style="giboshi", sides=("front",), stair=W / 2, waki=False,
                    returns=True, ret_z=c / 2 + 0.01)  # FX1: koran returns to the corner columns
    rp = Part("roof", "", "")
    # corner lift 0.12 (default 0.30): the far LODs of a 6.8 m hogyo cannot follow a stronger sweep (C15)
    sls, info = SO.roof(rp, W, D, "yosemune", "copper", bear_y=K["bear_y"], g_out=K["g_out"], ov=K["g_out"] + 1.40,
                        corner_lift=0.12)
    ax, ay, az = info["apex"]
    ORN.hoju(rp, (ax, ay - 0.05, az), "hoju_bronze", s=1.2)
    S.H.merge(rp)
    kf = SO.kohai_fit(info)
    kp = Part("kohai", "", "")
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    NG.kohai(kp, bay, 2 * bay, zp, kf["main_t"], kf["main_ov"], kf["eave_y"], "itabuki", drop)
    remat(kp, "roof_kokera", "roof_copper")
    S.H.merge(kp)
    _lift(S, drop)
    lift_portals(S, drop, n0)
    S.room("hall", "worship", "boards", drop, (c / 2 + 0.03, W - c / 2 - 0.03, -D + c / 2 + 0.03, -c / 2 - 0.03),
           [S.dn["front"]], "one-room hall: the statue on its dais at the back; also the ward's meeting hall")
    en_rooms(S, W, D, drop, ("front",), z0=0.32, returns=True)
    stair_obstacle(S, "en", en["stair"])
    fit(S, "altar", "hall", rect=(W / 2 - 1.2, W / 2 + 1.2, -D + c / 2 + 0.03, -D + c / 2 + 1.10), y=drop,
        note="Sumeru dais (shumidan) with the statue in its zushi, the three altar pieces, bowl gong, sutra desk")
    fit(S, "saisen_bako", "en", centre=(W / 2, 0.50), size=(1.2, 0.5), yaw=0.0, y=drop,
        note="donation box on the en before the doors")
    fit(S, "gong", "en", centre=(W / 2, 0.60), size=(0.3, 0.3), yaw=0.0, y=round(drop + 2.40, 2), obstacle=False,
        note="waniguchi gong with its rope under the kohai")
    hide_underfloor(S.H, W, D)
    far_trim(S.H)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "do", "grade": "town"}, "levels": {"floor": drop}, "stair": en["stair"],
                     "kumimono": {k: v for k, v in K.items() if k != "nodes"}})


# ------------------------------------------------------------------------------------------------ BU2 hondo
def hondo(name=None, grade="village", form="degumi", wear="_w1"):
    """Village hondo: 4 x 4 ken on a boarded raised floor (+0.60), shinkabe walls, a board ceiling, straight irimoya
    sangawara, front en with plain koran + kizahashi, a tiled kohai over the middle two bays; sankarado in the two
    middle bays, hinged shitomido outside them; a board side door (the priests' way from the kuri)."""
    if grade == "town":
        return _hondo_town(name, form, wear)
    n = 4
    W = D = n * KEN
    drop = 0.60
    S = Shell(name or "jp_temple_hondo", W, D, [1, 2], "main hall (hondo), village, 4 x 4 ken", wear)
    STL.platform(S.H, W, D, drop, "hall")
    xs = [k * KEN for k in range(n + 1)]
    F = frames(W, D)
    B = S.B
    for side, xx in (("front", xs), ("back", xs), ("left", xs), ("right", xs)):
        B.posts_on(F[side], xx, 0.0, WALL_H)
    holes = [(k * KEN + POST / 2, (k + 1) * KEN - POST / 2, 0.0, 2.0) for k in range(n)]
    B.wall(F["front"], "front", "shinkabe", 0.0, W, 0.0, WALL_H, openings_=holes, finish="nakanuri")
    B.wall(F["back"], "back", "shinkabe", 0.0, W, 0.0, WALL_H, finish="nakanuri")
    B.wall(F["left"], "left", "shinkabe", 0.0, D, 0.0, WALL_H, finish="nakanuri")
    B.wall(F["right"], "right", "shinkabe", 0.0, D, 0.0, WALL_H, finish="nakanuri",
           openings_=[(3 * KEN + POST / 2, 4 * KEN - POST / 2, 0.0, 2.0)])
    for side, L in (("front", W), ("back", W), ("left", D), ("right", D)):
        k = Part("keta", "", "")
        frame.keta(k, -0.06, L + 0.06)
        B.put(k, F[side])
    n0 = len(S.portals)
    S.door(TB.part_tobira("_sankara_in"), F["front"], KEN, 0.0, "Hall doors left (sankarado, open in)", "front")
    S.door(TB.part_tobira("_sankara_in"), F["front"], 2 * KEN, 0.0, "Hall doors right (sankarado, open in)", "front2")
    for k in (0, 3):
        front_bay(S, k * KEN, KEN, "shitomi", "Shitomido %d (upper leaf)" % k)
    # the right wall's back bay (local x = -z: 3..4 ken = the back corner): the priests' side door from the kuri
    S.door(TB.part_tobira("_board_in"), F["right"], 3 * KEN, 0.0, "Side door (board, open in)", "side")
    cp = Part("ceiling", "", "")
    cp.add(box(POST / 2, W - POST / 2, WALL_H, WALL_H + 0.04, -D + POST / 2, -POST / 2, "ceil_boards", vis=(1, 2),
               tag="tenjo"))
    B.interior = True
    B.merge(cp)
    B.interior = False
    en = KR.en_wrap(S.H, W, D, drop=drop, style="plain", sides=("front",), stair=W / 2, waki=False,
                    returns=True)  # FX1: koran returns at the en ends
    rp = Part("roof", "", "")
    sls, info = R.roof(rp, W, D, "irimoya", "sangawara", eave_y=EAVE_Y)
    far_r2_in_r3(rp, ("kawara_field_far",))      # C15: the 4-ken irimoya's R3 field misses the gable foot by 0.30
    S.H.merge(rp)
    kp = Part("kohai", "", "")
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    NG.kohai(kp, KEN, 3 * KEN, zp, R.PITCH["sangawara"], R.EAVE_OV["sangawara"], EAVE_Y, "sangawara", drop)
    S.H.merge(kp)
    # the side door's step: a stone with a hidden ramp from the floor down to grade outside the right wall
    st = Part("side_step", "", "")
    found.step(st, 3.5 * KEN, "cut", drop=drop, width=1.10)
    S.B.put(st, F["right"], what="found.step (cut) under the side door")
    _lift(S, drop)
    lift_portals(S, drop, n0)
    S.room("hall", "worship", "boards", drop, (POST / 2, W - POST / 2, -D + POST / 2, -POST / 2),
           [S.dn["front"], S.dn["front2"], S.dn["side"]],
           "gejin (worship floor) in front, naijin (inner sanctum) at the back: the dais spot")
    en_rooms(S, W, D, drop, ("front",), returns=True)
    stair_obstacle(S, "en", en["stair"])
    fit(S, "altar", "hall", rect=(KEN, 3 * KEN, -D + A_ + 0.03, -D + A_ + 1.30), y=drop,
        note="naijin: the Sumeru dais (shumidan) with the honzon in its zushi, canopy over it, the three altar pieces, "
             "the front table, the priest's platform (raiban); memorial tablets (ihai) on a shelf beside")
    fit(S, "sutra_desk", "hall", centre=(W / 2, -D + 2.30), size=(0.9, 0.5), yaw=0.0, y=drop,
        note="sutra desk + bowl gong (keisu) + mokugyo in front of the dais")
    fit(S, "saisen_bako", "en", centre=(W / 2, 0.50), size=(1.4, 0.5), yaw=0.0, y=drop,
        note="donation box on the en before the doors")
    fit(S, "gong", "en", centre=(W / 2, 0.60), size=(0.3, 0.3), yaw=0.0, y=round(drop + 2.35, 2), obstacle=False,
        note="waniguchi gong + rope under the kohai")
    hide_underfloor(S.H, W, D)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "hondo", "grade": "village"}, "levels": {"floor": drop}, "stair": en["stair"]})


def _hondo_town(name, form, wear):
    """Town hondo: 3 x 3 bays of 2.275 on a boarded raised floor (+0.75), degumi (or mitesaki) bracket sets with
    kaerumata, board walls + a board ceiling, curved irimoya hongawara, the en on three sides with giboshi koran,
    wakishoji, kizahashi, a hongawara-style kohai fitted under the curved eave; sankarado in the middle bay, hinged
    shitomido beside, a board side door. FX1: the en is front-only with koran returns (the three-side en the first
    line names is over the face budget)."""
    n, bay = 3, TOWN_BAY
    W = D = n * bay
    drop, col_h = 0.75, 3.2
    S = Shell(name or "jp_temple_hondo_town", W, D, [2, 3], "main hall (hondo), town, %s" % form, wear)
    STL.platform(S.H, W, D, drop, "hall", step=KEN)
    K = town_frame(S, W, D, n, n, col_h, form, "hongawara", c=0.27 if form == "mitesaki" else None,
                   nakazonae="kentozuka")
    c = K["c"]
    ytop = col_h - 0.62 * c
    n0 = len(S.portals)
    dn = town_walls(S, W, D, n, n, c, ytop, front=["shitomi", "tobira_sankara_in", "shitomi"])
    S.dn["front"] = dn[1]
    en = KR.en_wrap(S.H, W, D, drop=drop, style="plain", sides=("front",), stair=W / 2, waki=False,
                    returns=True)  # FX1: koran returns at the en ends (was cut off). A mawari-en (three sides, even
    # one bay deep to a wakishoji: koran.en_wrap side_len) is the fuller form but takes R1 to 12,428 / R3 1,638, over
    # the 'large' budget (12,000 / 1,600); the returns keep it at 11,586 / 1,590
    rp = Part("roof", "", "")
    sls, info = SO.roof(rp, W, D, "irimoya", "hongawara", bear_y=K["bear_y"], g_out=K["g_out"],
                        ov=K["g_out"] + (1.30 if form == "mitesaki" else 1.35), spacing=0.30)
    S.H.merge(rp)
    kf = SO.kohai_fit(info)
    kp = Part("kohai", "", "")
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    NG.kohai(kp, bay, 2 * bay, zp, kf["main_t"], kf["main_ov"], kf["eave_y"], "itabuki", drop)
    remat(kp, "roof_kokera", "roof_copper")     # a copper-clad kohai under the tile roof (C13: a tiled kohai tucked
    # under a curved eave loses its bed). Its sheathing lies UNDER the main roof's eave tiles: C13 (checks.tile_seating)
    # reads every 'sheathing' under a kawara vertex as that kawara's own deck, so the kohai's is named for what it is
    for s in kp.solids:
        if s.tag == "sheathing":
            s.tag = "kohai_sheathing"
    S.H.merge(kp)
    _lift(S, drop)
    lift_portals(S, drop, n0)
    S.room("hall", "worship", "boards", drop, (c / 2 + 0.03, W - c / 2 - 0.03, -D + c / 2 + 0.03, -c / 2 - 0.03),
           [S.dn["front"]], "gejin in front, naijin at the back: the dais spot")
    en_rooms(S, W, D, drop, ("front",), z0=0.32, returns=True)
    stair_obstacle(S, "en", en["stair"])
    fit(S, "altar", "hall", rect=(bay, 2 * bay, -D + c / 2 + 0.03, -D + c / 2 + 1.40), y=drop,
        note="naijin: Sumeru dais (shumidan) with the honzon in its zushi, canopy (tengai), keman, banners, the "
             "three / five altar pieces, front table, the priest's platform (raiban)")
    fit(S, "sutra_desk", "hall", centre=(W / 2, -D + 2.45), size=(0.9, 0.5), yaw=0.0, y=drop,
        note="sutra desk, bowl gong (keisu), mokugyo; big drum by the side")
    fit(S, "saisen_bako", "en", centre=(W / 2, 0.50), size=(1.5, 0.55), yaw=0.0, y=drop,
        note="donation box on the en")
    fit(S, "gong", "en", centre=(W / 2, 0.60), size=(0.3, 0.3), yaw=0.0, y=round(drop + 2.45, 2), obstacle=False,
        note="waniguchi gong + rope under the kohai")
    hide_underfloor(S.H, W, D)
    far_trim(S.H)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "hondo", "grade": "town", "form": form}, "levels": {"floor": drop},
                     "stair": en["stair"], "kumimono": {k: v for k, v in K.items() if k != "nodes"}})


# ------------------------------------------------------------------------------------------------ BU3 kuri
def kuri(name=None, grade="village", wear="_w1"):
    """Priests' quarters + kitchen (kuri): W 6 x D 4 ken under one kirizuma roof (thatch, village / sangawara, town)
    with sooted koyagumi over the big doma kitchen (2.5 ken, the kamado row spot, ooto front door + back door), the
    raised rooms beside it: the board daidokoro with the irori (front) and the tatami guest room (back) behind a
    partition, and the formal entrance (genkan) as a porch on the rooms' gable end: a small kirizuma roof on two posts
    (under the main gable, where no eave drops over it), a cut-stone pad, the shikidai step and a door into the guest
    room. PLAYBOOK §2.2: the genkan is a status feature allowed for temple kuri (audit #8)."""
    W, D = 6 * KEN, 4 * KEN
    FLOOR = 0.50
    thatch = grade != "town"
    fam = "thatch" if thatch else "sangawara"
    E = 3.30 if thatch else 3.45
    YT = E - KETA_H
    YG = E - 0.21
    t = R.PITCH[fam]
    XD = 2.5 * KEN                      # doma x 0..XD | rooms XD..W
    ZS = -2.0 * KEN                     # daidokoro (front) / guest room (back)
    S = Shell(name or "jp_temple_kuri", W, D, [1, 2] if thatch else [2, 3],
              "priests' quarters + kitchen (kuri), %s" % grade, wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=0.90 if thatch else None, ridge="bamboo" if thatch else None,
                           stone_fn=lambda x, z: x < XD - 0.1, slim_x=(XD,))
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    front_feats = [(0.5 * KEN, 1.5 * KEN, DOMA, DOMA + 2.0, "door"),
                   (2.0 * KEN, 2.5 * KEN, DOMA + 0.90, DOMA + 1.65, "window"),
                   (3.5 * KEN, 4.0 * KEN, FLOOR + 0.90, FLOOR + 1.65, "window")]
    S.wall_line("front", [(0.0, XD, DOMA), (XD, W, FLOOR)], YT, front_feats, finish=fin, koshiita=kosh,
                nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.5 * KEN, 3.5 * KEN, 4.0 * KEN))
    S.door(big_leaf("_battened"), "front", 0.5 * KEN, DOMA, "Kitchen door (ooto, doma)", "front")
    S.window(openings.part_window_slide("_board"), "front", 2.0 * KEN, DOMA, "Doma window (front)")
    S.window(openings.part_window_slide("_board"), "front", 3.5 * KEN, FLOOR, "Daidokoro window (front)")
    # back (local lx = W - x): the guest room's window, the doma back door
    back_feats = [(1.5 * KEN, 2.0 * KEN, FLOOR + 0.90, FLOOR + 1.65, "window"),
                  (4.5 * KEN, 5.5 * KEN, DOMA, DOMA + 2.0, "door")]
    S.wall_line("back", [(0.0, W - XD, FLOOR), (W - XD, W, DOMA)], YT, back_feats, finish=fin, koshiita=kosh,
                nodes_extra=(1.5 * KEN, 2.0 * KEN, 3.5 * KEN, 4.5 * KEN, 5.5 * KEN))
    S.window(openings.part_window_slide("_board"), "back", 1.5 * KEN, FLOOR, "Guest room window (back)")
    S.door(openings.part_itado("_single"), "back", 4.5 * KEN, DOMA, "Back door (doma)", "back")
    # left gable (doma end, local lx = z + D): a smoke-blackened end wall with a high window
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(1.5 * KEN, 2.0 * KEN, DOMA + 1.20, DOMA + 1.95, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN, 2.0 * KEN))
    S.window(openings.part_window_slide("_board"), "left", 1.5 * KEN, DOMA + 0.30, "Doma window (end)")
    # right gable (rooms end, local lx = -z): the genkan door into the guest room (bay 2.5..3.5 ken)
    S.wall_line("right", [(0.0, D, FLOOR)], YG, [(2.5 * KEN, 3.5 * KEN, FLOOR, FLOOR + 2.0, "door")],
                finish=fin, koshiita=kosh, nodes_extra=(2.5 * KEN, 3.5 * KEN))
    S.door(openings.part_shoji_ext("_single"), "right", 2.5 * KEN, FLOOR, "Genkan door (guest room)", "genkan")
    for g in ("left", "right"):
        S.gable(g, D, t, E, "_board" if thatch else "_tile", thatch=thatch)
    # partition daidokoro | guest room (z = ZS, x XD..W) with a sliding door, to a head beam
    PT = FLOOR + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F_Z = (0.0, (XD, 0.0, ZS))
    S.wall_line((F_Z, W - XD, "part_z"), [(0.0, W - XD, FLOOR)], PT,
                [(1.5 * KEN, 2.5 * KEN, FLOOR, FLOOR + 2.0, "door")], finish="nakanuri", grime=False,
                interior="both", nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.5 * KEN))
    S.door(openings.part_shoji_ext("_single"), F_Z, 1.5 * KEN, FLOOR, "Daidokoro -> guest room", "guest")
    B.interior = False
    S.head_beam(F_Z, W - XD, PT, "part_z_head")
    # floors
    B.interior = True
    B.merge(FL.doma("doma", 0.0, XD, -D, 0.0, road=(A_, XD - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    pit = _irori(S, "daidokoro", XD + 1.5 * KEN, ZS / 2, True, FLOOR, K["levels"])
    B.merge(FL.boards("daidokoro", XD + 0.06, W - A_, ZS + A_, -A_, FLOOR, holes=[pit + ("pit",)],
                      hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    B.merge(FL.tatami("guest", XD + 0.06, W - A_, -D + A_, ZS - A_, top=FLOOR, base=0.0, mats=FL.MATS_TATAMI_B1))
    B.interior = False
    S.kamachi((-90.0, (XD, 0.0, 0.0)), D, FLOOR, [0.5 * KEN], "doma")
    _kamado(S, "doma", 0.50, -2.0 * KEN, 90.0)
    _kamado(S, "doma", 0.50, -3.0 * KEN, 90.0)
    # ---- the genkan porch on the right gable (x W..W + 1 ken, z -2.5..-3.5 ken + a half ken either side)
    zf, zb = -2.0 * KEN, -4.0 * KEN + 0.0           # porch roof front / back eave lines (1 ken + 1 ken wide)
    zf, zb = -2.25 * KEN, -3.75 * KEN
    xp = W + KEN                                    # porch posts line
    ye = 2.95                                       # porch keta top (the door head 2.50 + head room)
    for z in (zf, zb):
        S.post(xp, z, ye - KETA_H)
    pk = Part("genkan_keta", "", "")
    for z in (zf, zb):
        pk.add(box(W + 0.06, xp + 0.30, ye - KETA_H, ye, z - 0.06, z + 0.06, WOOD, vis=(1, 2, 3), geo=True, view=True,
                   fire=True, tag="keta"))
    pk.add(box(xp - 0.06, xp + 0.06, ye - KETA_H - 0.25, ye - KETA_H, zb, zf, WOOD, vis=(1, 2), geo=True, view=True,
               fire=True, tag="genkan_beam"))
    S.H.merge(pk)
    gp = Part("genkan_roof", "", "")
    gfam = "itabuki" if thatch else "sangawara"
    gov = R.GABLE_OV[gfam]
    Lr = xp + 0.30 - (W + 0.08 + gov) - gov         # roof x length between its verge points (outer verge 0.30 out)
    sl_g, info_g = R.roof(gp, Lr, zf - zb, "kirizuma", gfam, eave_y=ye, ov=0.55, gov=gov)
    S.H.merge(gp.transformed(0.0, (W + 0.08 + gov, 0.0, zf)))
    paving(S.H, W + 0.10, xp + 0.45, zb - 0.45, zf + 0.45, y=DOMA, name="genkan_pad")
    st = Part("shikidai", "", "")
    found.step(st, 3.0 * KEN, "wood", drop=FLOOR - DOMA, width=1.20)
    S.B.put(st, S.F["right"], 0.0, FLOOR, what="found.step (wood): the shikidai board step")
    S.place_windows()
    S.room("doma", "doma", "earth", DOMA, (A_, XD - 0.07, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "the big earth-floored kitchen: the kamado row on the end wall, water jars, open to the sooted roof")
    S.room("daidokoro", "daidokoro", "boards", FLOOR, (XD + 0.06, W - A_, ZS + A_, -A_), [S.dn["guest"]],
           "board room with the irori: the office and the priests' living room, open to the doma")
    S.room("guest", "zashiki", "tatami", FLOOR, (XD + 0.06, W - A_, -D + A_, ZS - A_), [S.dn["guest"], S.dn["genkan"]],
           "guest room (tatami) reached from the genkan")
    S.room("genkan", "yard", "stone", DOMA, (W + 0.70, xp + 0.38, zb - 0.38, zf + 0.38), [S.dn["genkan"]],
           "the genkan porch: stone pad, shikidai step up to the guest room", enclosed=False)
    S.obst.append(("genkan", _r(W, W + 0.80, -3.0 * KEN - 0.65, -2.5 * KEN + 0.10)))
    fit(S, "kamado_row", "doma", rect=(A_ + 0.02, 1.00, -3.5 * KEN, -1.5 * KEN), y=DOMA, obstacle=False,
        note="the kamado row with the big iron cauldrons, rice-steaming baskets, water jars (two kamado spots above)")
    fit(S, "zen_trays", "daidokoro", rect=(W - 0.55, W - A_ - 0.02, ZS + 0.30, -0.60), y=FLOOR, obstacle=False,
        note="stacked lacquer meal trays (zen), account books, the temple seal box, writing desk")
    stones_as_soseki(S.H)
    trim_lods(S.H)
    return S.finish({"params": {"kind": "kuri", "grade": grade}, "levels": {"doma": DOMA, "floor": FLOOR, "eave": E},
                     "koyagumi": K["counts"]}, exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or
                    abs(x) < 1e-6 or abs(x - W) < 1e-6)


# ------------------------------------------------------------------------------------------------ BU6 bell tower
def light_platform(H, x0, x1, z0, z1, h, steps=(("front", 1.82),), name="platform"):
    """A cut-stone platform (W2P2's proof platform: W2P1's stilts.kidan costs ~2,000 faces in Resolution 1 AND 2): a
    core slab (every LOD, Geometry, Roadway on an earth top), kerb stones and facing blocks 2 cm proud in Resolution 1,
    cut steps with hidden ramps (found.step). Frame: top y 0, grade -h."""
    p = Part(name, "", "")
    p.add(box(x0, x1, -h - 0.10, 0.0, z0, z1, {"top": "ground_doma_earth", "default": "stone_cut"}, vis=(1, 2, 3),
              geo=True, view=True, fire=True, tag="platform_core"))
    p.road([(x0, 0.0, z0), (x1, 0.0, z0), (x1, 0.0, z1), (x0, 0.0, z1)], "stone_ext")
    k = 0
    for (a0, a1, fixed, axis, sg) in ((x0, x1, z1, "x", 1), (x0, x1, z0, "x", -1), (z0, z1, x0, "z", -1),
                                      (z0, z1, x1, "z", 1)):
        a = a0 + (0.02 if axis == "z" else 0.0)
        while a < a1 - 0.05:
            k += 1
            b = min(a1 - (0.02 if axis == "z" else 0.0), a + 0.9 + 0.4 * ((k * 37) % 10) / 10)
            if a1 - b < 0.4:
                b = a1 - (0.02 if axis == "z" else 0.0)
            for (yy0, yy1, dep, tag) in ((-0.16, 0.02, 0.32, "kerb"), (-h + 0.02, -0.165, 0.10, "footing")):
                o0, o1 = (fixed - dep + 0.02, fixed + 0.02) if sg > 0 else (fixed - 0.02, fixed + dep - 0.02)
                uv = (((k * 0.37) % 1), ((k * 0.61) % 1))
                if axis == "x":
                    p.add(box(a + 0.006, b - 0.006, yy0, yy1, o0, o1, "stone_cut", vis=(1,), tag=tag, uvoff=uv))
                else:
                    p.add(box(o0, o1, yy0, yy1, a + 0.006, b - 0.006, "stone_cut", vis=(1,), tag=tag, uvoff=uv))
            a = b
    for side, w in steps:
        st = Part("step", "", "")
        found.step(st, (x0 + x1) / 2, "cut", drop=h, width=w)
        p.merge(st.transformed(0.0, (0.0, 0.0, z1 + 0.02)) if side == "front" else
                st.transformed(180.0, ((x0 + x1), 0.0, z0 - 0.02)))
    H.merge(p)


def shoro(name=None, grade="village", wear="_w1"):
    """Village bell tower: the open four-post type, one bay of 1.5 ken (2.73) on a low cut-stone platform (0.45), posts
    on dressed stones with head ties, straight irimoya sangawara, the bell beam front to back with the 'bell_hook'
    memory point (bell + striker = W2F props), struck from the platform."""
    if grade == "town":
        return _shoro_town(name, wear)
    B_ = 1.5 * KEN
    h = 0.45
    S = Shell(name or "jp_temple_shoro", B_, B_, [1, 2, 3], "bell tower (shoro), open four-post", wear)
    m = 1.10
    light_platform(S.H, -m, B_ + m, -B_ - m, m, h)
    E = 3.75
    for (x, z) in ((0.0, 0.0), (B_, 0.0), (0.0, -B_), (B_, -B_)):
        S.post(x, z, E - KETA_H, size=0.18, stone=False)
        S.H.add(cyl("y", x, z, 0.16, -0.10, 0.0, "stone_cut", n=8, vis=(1, 2), geo=True, view=True, fire=True,
                    tag="soseki"))
    S.keta_ring(B_, B_, E, hip=True)
    tb = Part("ties", "", "")
    yt = E - KETA_H - 0.55
    for (a, b_, along) in ((0.0, B_, "x"), (0.0, B_, "z")):
        for o in ((0.0, -B_) if along == "x" else (0.0, B_)):
            if along == "x":
                tb.add(box(-0.12, B_ + 0.12, yt, yt + 0.14, o - 0.05, o + 0.05, WOOD, vis=(1, 2), geo=True, view=True,
                           fire=True, tag="nuki"))
            else:
                tb.add(box(o - 0.05, o + 0.05, yt + 0.16, yt + 0.30, -B_ - 0.12, 0.12, WOOD, vis=(1, 2), geo=True,
                           view=True, fire=True, tag="nuki"))
    yb = yt - 0.30
    tb.add(box(B_ / 2 - 0.10, B_ / 2 + 0.10, yb, yb + 0.24, -B_ - 0.08, 0.08, WOOD, vis=(1, 2, 3), geo=True, view=True,
               fire=True, tag="bell_beam"))
    tb.memory["bell_hook"] = [(B_ / 2, yb, -B_ / 2)]
    S.H.merge(tb)
    rp = Part("roof", "", "")
    sls, info = R.roof(rp, B_, B_, "irimoya", "sangawara", eave_y=E, ov=1.05)
    far_r2_in_r3(rp, ("kawara_field_far",))
    for s in rp.solids:
        if s.tag == "tile_bed" and 2 in s.vis:
            s.vis = set(s.vis) | {3}             # C15: the small irimoya's far field has a slot at the gable foot
    S.H.merge(rp)
    S.room("platform", "yard", "stone", 0.0, (-m + 0.35, B_ + m - 0.35, -B_ - m + 0.35, m - 0.35), [],
           "the platform under the bell: the striker log hangs from the roof frame", enclosed=False)
    for (x, z) in ((0.0, 0.0), (B_, 0.0), (0.0, -B_), (B_, -B_)):
        S.obst.append(("platform", _r(x - 0.25, x + 0.25, z - 0.25, z + 0.25)))
    fit(S, "bell", "platform", centre=(B_ / 2, -B_ / 2), size=(1.2, 1.2), yaw=0.0, y=round(yb, 3),
        note="the bronze bell (bonsho, ~0.9 m) hangs from the bell beam at memory point 'bell_hook' (y = beam "
             "underside); the striker log (shumoku) on two ropes from the beams beside it")
    _lift_all(S, h)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    far_trim(S.H)
    return S.finish({"params": {"kind": "shoro", "grade": "village"}, "levels": {"platform": h, "eave": E + h},
                     "bell_hook": (B_ / 2, round(yb + h, 3), -B_ / 2)})


def _lift_all(S, h):
    """Platform-top frame -> grade frame for a shell built on a platform of height h, incl. rooms + fittings."""
    _lift(S, h)
    for r in S.rooms:
        r["level_m"] = round(r["level_m"] + h, 4)
    for f in S.fittings:
        if "y" in f:
            f["y"] = round(f["y"] + h, 3)


def _shoro_town(name, wear):
    """Town bell tower: W2P2's hakama type on a cut-stone platform (0.60): the flared board skirt (storey.hakama),
    the upper deck at +2.80 with a koran, four columns with degumi corner sets, the bell beam (memory 'bell_hook'),
    curved irimoya hongawara; an outside stair (kizahashi, <= 38 deg) from the deck's front edge down to grade, so the
    bell can be reached (period: an inside ladder-stair)."""
    B_ = 2.73
    h = 0.60
    cx, cz = B_ / 2, -B_ / 2
    S = Shell(name or "jp_temple_shoro_town", B_, B_, [2, 3], "bell tower (shoro), hakama, town", wear)
    m = 5.4
    light_platform(S.H, cx - m / 2, cx + m / 2, cz - m / 2, cz + m / 2, h, steps=(("back", 1.30),))
    y_f = 2.80
    hk = Part("hakama", "", "")
    ST.hakama(hk, cx, cz, hb=2.05, ht=1.62, y0=0.0, y1=y_f - 0.30)
    ST.deck(hk, cx, cz, 2.05, y_f)
    S.H.merge(hk)
    # the outside stair from the deck's front edge (z = cz + 2.05) down to grade (y -h): along +z
    sp = Part("stair", "", "")
    Kst = KR.kizahashi(sp, 0.0, 0.0, drop=y_f + h, style="plain")
    # the long flight's rails keep their real slope in every LOD (C15: the far rail of a 3.4 m flight sags 0.18 m)
    sp.solids = [s for s in sp.solids if s.tag not in ("hokogi_lod", "stair_lod") or s.geo or s.view or s.fire]
    for s in sp.solids:
        if s.tag in ("hokogi", "hirageta", "stair_tread", "stringer"):
            s.vis = set(s.vis) | {2, 3}
        if s.tag == "stair_lod":
            s.vis = set()
    S.H.merge(sp.transformed(0.0, (cx, y_f, cz + 2.05)))
    rl = Part("koran", "", "")
    e = 2.05 - 0.10
    xa, xb = cx + Kst["xa"], cx + Kst["xb"]
    KR.rail(rl, (cx - e, cz + e), (xa - 0.08, cz + e), "plain", ends=("cross", "open"))
    KR.rail(rl, (xb + 0.08, cz + e), (cx + e, cz + e), "plain", ends=("open", "cross"))
    KR.rail(rl, (cx - e, cz - e), (cx + e, cz - e), "plain", ends=("cross", "cross"))
    KR.rail(rl, (cx - e, cz + e), (cx - e, cz - e), "plain", ends=("cross", "cross"), lift=0.015)
    KR.rail(rl, (cx + e, cz + e), (cx + e, cz - e), "plain", ends=("cross", "cross"), lift=0.015)
    S.H.merge(rl.transformed(0.0, (0.0, y_f, 0.0)))
    km = Part("kumimono", "", "")
    K = KM.frame(km, B_, B_, 1, 1, 2.75, "degumi", c=0.26, y0=y_f, covering="hongawara", nageshi=False)
    S.H.merge(km)
    c = K["c"]
    for (x, z) in K["nodes"]:
        S.posts.append((x, z, y_f, y_f + 2.75))
    bb = Part("bellbeam", "", "")
    yb = y_f + 2.20
    KM.beam(bb, (cx, yb, 0.0), (cx, yb, -B_), 0.20, 0.24, vis=(1, 2, 3), tag="bell_beam")
    bb.solids[-1].geo = True
    bb.solids[-1].view = True
    bb.solids[-1].fire = True
    bb.memory["bell_hook"] = [(cx, yb, cz)]
    S.H.merge(bb)
    rp = Part("roof", "", "")
    sls, info = SO.roof(rp, B_, B_, "irimoya", "hongawara", bear_y=K["bear_y"], g_out=K["g_out"], ov=K["g_out"] + 1.30,
                        ridge_courses=5)
    S.H.merge(rp)
    obst = [(x - 0.22, x + 0.22, z - 0.22, z + 0.22) for (x, z) in ((0.0, 0.0), (B_, 0.0), (0.0, -B_), (B_, -B_))]
    S.room("upper", "worship", "boards", y_f, (cx - 1.9, cx + 1.9, cz - 1.9, cz + 1.9), [],
           "the bell deck: the bell hangs in the middle, struck with the log", enclosed=False)
    for o in obst:
        S.obst.append(("upper", _r(*o)))
    S.obst.append(("upper", _r(xa - 0.2, xb + 0.2, cz + 1.4, cz + 2.1)))
    S.obst.append(("upper", _r(cx - 0.75, cx + 0.75, cz - 0.75, cz + 0.75)))
    fit(S, "bell", "upper", centre=(cx, cz), size=(1.3, 1.3), yaw=0.0, y=round(yb, 3), obstacle=False,
        note="the bronze bell (bonsho) hangs from the bell beam at memory point 'bell_hook' (y = beam underside); "
             "the striker log (shumoku) on two ropes from the head ties")
    _lift_all(S, h)
    stones_as_soseki(S.H)
    trim_lods(S.H)
    far_trim(S.H)
    return S.finish({"params": {"kind": "shoro", "grade": "town"}, "levels": {"platform": h, "deck": y_f + h},
                     "bell_hook": (cx, round(yb + h, 3), cz), "stair": Kst})


# ------------------------------------------------------------------------------------------------ BU5 small gate
def gate(name=None, grade="village", wear="_w1"):
    """Temple small gate. village = yakui-mon: two main posts (0.24) on the gate line with the hinged board leaf pair
    (W2C gates.gate_leaves), two control posts 1 ken behind, beams over them, straight kirizuma sangawara over the post
    pairs. town = shikyaku-mon: the main round columns on the gate line, four control columns 1 ken in front and
    behind, oto-hijiki on every column, curved kirizuma hongawara. A packed-earth threshold strip through the gate."""
    span = 1.5 * KEN
    S = Shell(name or "jp_temple_gate", span, KEN, [2, 3], "small gate (%s)" % ("shikyaku-mon" if grade == "town" else
                                                                           "yakui-mon"), wear)
    B = S.B
    if grade == "town":
        D = 2 * KEN
        zg = -KEN                                   # the gate line (main columns) between the control columns
        km = Part("kumimono", "", "")
        col_h = 3.30
        K = KM.frame(km, span, D, 1, 2, col_h, "oto", c=0.28, y0=0.0, covering="hongawara", nakazonae=None,
                     nageshi=False)
        S.H.merge(km)
        column_bases(S.H, K["nodes"], K["c"], 0.0)
        for (x, z) in K["nodes"]:
            S.posts.append((x, z, 0.0, col_h))
        c = K["c"]
        tb = Part("ties", "", "")
        tb.add(box(c / 2, span - c / 2, 2.62, 2.80, zg - 0.07, zg + 0.07, WOOD, vis=(1, 2, 3), geo=True, view=True,
                   fire=True, tag="kashira_nuki"))
        S.H.merge(tb)
        gp = G.gate_leaves("_board", span, post=c, y0=DOMA + 0.03, y_floor=DOMA)
        S.door(gp, (0.0, (0.0, 0.0, zg)), 0.0, 0.0, "Gate leaves", "gate")
        rp = Part("roof", "", "")
        sls, info = SO.roof(rp, span, D, "kirizuma", "hongawara", bear_y=K["bear_y"], g_out=K["g_out"],
                            ov=K["g_out"] + 0.95, gov=0.85, ridge_courses=5, corner_lift=0.08)
        far_lift(rp, lods=(2,))
        S.H.merge(rp)
        z0, z1 = -D - 0.6, 0.6
    else:
        D = KEN
        zg = 0.0
        top = 3.10
        for x in (0.0, span):
            S.post(x, 0.0, top, size=0.24, mat="wood_street_dark")
            S.post(x, -KEN, top - 0.20, size=0.15, mat="wood_street_dark")
        hd = Part("heads", "", "")
        hd.add(box(-0.22, span + 0.22, 2.60, 2.78, -0.07, 0.07, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True,
                   fire=True, tag="kashira_nuki"))
        for x in (0.0, span):
            hd.add(box(x - 0.08, x + 0.08, top - 0.20, top, -KEN - 0.25, 0.30, "wood_street_dark", vis=(1, 2, 3),
                       geo=True, view=True, fire=True, tag="hijiki"))
        ky = top + 0.12
        for z in (0.30, -KEN - 0.25):
            hd.add(box(-0.35, span + 0.35, top, ky, z - 0.06, z + 0.06, "wood_street_dark", vis=(1, 2, 3), geo=True,
                       view=True, fire=True, tag="keta"))
        S.H.merge(hd)
        gp = G.gate_leaves("_board", span, post=0.24, y0=DOMA + 0.03, y_floor=DOMA)
        S.door(gp, (0.0, (0.0, 0.0, 0.0)), 0.0, 0.0, "Gate leaves", "gate")
        rp = Part("roof", "", "")
        sls, info = R.roof(rp, span, KEN + 0.55, "kirizuma", "sangawara", eave_y=ky, ov=0.75, gov=0.55)
        S.H.merge(rp.transformed(0.0, (0.0, 0.0, 0.30)))
        z0, z1 = -KEN - 0.6, 0.9
    # the passage floor: a packed-earth threshold strip through the gate (the precinct is grade)
    B.interior = True
    B.merge(FL.doma("gate", -0.10, span + 0.10, z0 - 0.15, z1 + 0.15, road=(0.10, span - 0.10, z0, z1), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.obst.append(("gate", _r(-0.3, span + 0.3, zg - 0.25, zg + 0.18)))
    S.obst.append(("gate", _r(0.0, 0.32, zg - 1.50, zg)))
    S.obst.append(("gate", _r(span - 0.32, span, zg - 1.50, zg)))
    for (x, z, _, _) in S.posts:
        S.obst.append(("gate", _r(x - 0.25, x + 0.25, z - 0.25, z + 0.25)))
    S.room("gate", "yard", "earth", DOMA, (0.10, span - 0.10, z0, z1), [S.dn["gate"]],
           "the passage through the gate (outside +z, the precinct -z)", enclosed=False)
    fit(S, "gaku", None, centre=(span / 2, zg), size=(1.0, 0.1), yaw=0.0, y=2.95, obstacle=False,
        note="the temple's name board (sangaku) over the tie beam")
    stones_as_soseki(S.H)
    trim_lods(S.H)
    far_trim(S.H)
    return S.finish({"params": {"kind": "gate", "grade": grade}, "levels": {"doma": DOMA},
                     "centre_kit": (span / 2, zg)})


# ------------------------------------------------------------------------------------------------ registry glue
BUILDERS = {"haiden": haiden, "honden": honden, "temizuya": temizuya, "shamusho": shamusho, "kagura": kagura,
            "do": do, "hondo": hondo, "kuri": kuri, "shoro": shoro, "gate": gate}


def build(kind, **params):
    if kind not in BUILDERS:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(sorted(BUILDERS))))
    return BUILDERS[kind](**params)


def budget_class(kind, **params):
    """PLAYBOOK §12. Curved / tiled halls are 'large' (W2P1 / W2P2: a tiled hogyo roof alone ~3,600 faces, the curved
    hall 8-11k); the bell towers too (no 'tower' class: the lead asks Stephen); small honden, temizuya, the gate and the
    shamusho 'standard'."""
    grade = params.get("grade", "village")
    if kind == "shoro":
        return "large" if grade == "town" else "standard"     # the town tower: R3 > 800 (no 'tower' class yet)
    if kind in ("hondo", "kuri"):
        return "large"
    if grade == "town" and kind in ("haiden", "do", "kagura", "honden"):
        return "large"
    if kind == "do" and params.get("roof") == "tile":
        return "large"
    return "standard"


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front), as civic.model."""
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
    mem = {}
    for k, v in M.memory.items():
        if k in ("bell_hook",):
            mem[k] = [[round(c, 3) for c in p] for p in v]
    info = dict(info, centre=(cx, cz), fittings_model=fits, memory_points=mem,
                portals_model=[(n, (b[0] - cx, b[1] - cx, b[2], b[3], b[4] - cz, b[5] - cz)) for n, b in info["portals"]],
                passages_model=[(x - cx, z - cz, y) for (x, z, y) in info["passages"]])
    return M, floors, rooms, info
