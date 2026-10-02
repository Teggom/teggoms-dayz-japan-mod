"""The COVERED-CORRIDOR kit (watari-roka) and the CLOISTER (kairo): agent K3, 2026-10-01 (parts/K3_NOTES.md §3, API
§6). Stephen's idea (PRODUCTION_PLAN 2026-10-01): temple hondo <-> kuri corridors round tsuboniwa courtyards, abbot's
quarters, shrine kairo, samurai / honjin / daimyo wings linked round gardens.

Frames (the striproof frames): a straight module runs along +x from 0 to L (1 / 2 / 3 ken) on the corridor centreline
z = 0, posts on the lines z = +-D/2 (D = width, 1 ken default); a junction module (corner / T / cross) is centred on
the crossing of two centrelines, its four posts at (+-D/2, +-D/2). y 0 = grade at the module; the raised board floor
(top `floor`, 0.45 default = the kit's agari level) is continuous across modules (Roadway joins on the post lines).

    straight(L, sides=("open", "open"), roof="itabuki", ends=("seam", "seam"), branches=(), posts0=True, ...)
    junction(arms, sides={...}, roof=...)            arms: '-x' '+x' '-z' '+z' (2 adjacent = corner, 3 = T, 4 = cross)
    stair(L, rise, ...)                              level change: covered stair, roof at the upper level, stepped
    connector(L=HALF, ...)                           the end that butts a host building's wall / veranda
    run_roka(path, ...)                              a whole corridor from grid nodes (corners, T's, stairs)
    connector_fit(host_soffit_y, floor, roof, ...)   does the corridor ridge fit under a host's eave?

sides: per side ('-z' first, '+z' second for a straight; a dict side -> kind for a junction's outer sides):
  'open' (W2P1's koran rail outside the posts), 'half' (board koshi wall to 0.90 + a cap rail), 'enclosed' (plaster
  wall with a renji vertical-bar window in every bay), 'blank' (plaster wall), 'board' (board wall + renji window),
  'none'. A KAIRO is the same pieces with the outer side 'enclosed' and the inner (court) side 'open'.
roof: itabuki | kokera | hiwada | sangawara | hongawara; profile 'straight' or 'sori' (W2P2's curve maths).
"""
import math

from .core import Part, Solid, box, prism, hexa, cyl, stone, KEN, HALF, QK, rng_for, MIN_HEAD
from .shapes import board_run, tube
from . import striproof as SR
from . import koran as KR
from .found import soseki

GROUP = "roka"
FLOOR = 0.45                 # floor top over grade (agari level, PLAYBOOK §4)
H_TIE = 2.10                 # head tie underside over the floor (D2 / D5: >= 2.05 head room)
H_KETA = 2.24                # keta underside over the floor; keta top (the roof bearing) 2.42
POST = 0.12
DECK_OUT = 0.16              # deck edge past the post line
RAIL_Z = 0.11                # koran rail centre past the post line (clear of the post face 0.06)
WOOD = "wood_weathered"


def _spec(D, floor, roof, profile="straight", ov=0.75, gov=0.45):
    fam = roof
    t = None
    if profile == "straight":
        t = 0.40 if fam in ("itabuki", "kokera", "hiwada", "kureita") else 0.45
    return SR.Spec(D, ov, floor + H_KETA + 0.18, fam, profile=profile, t=t, gov=gov, body="open", walkable=True,
                   rafter_sp=0.30, rafter_sec=(0.05, 0.065), courses=3 if fam != "hongawara" else 5,
                   sori=(0.30, 0.68, 1.6))


def _post(P, x, z, y0, y1, rng, stone_=True):
    if stone_:
        soseki(P, x, z, int(rng.random() * 8), grade=-0.12)
    P.add(box(x - POST / 2, x + POST / 2, y0, y1, z - POST / 2, z + POST / 2, WOOD, vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="roka_post", grain="long"))


def _deck(P, x0, x1, z0, z1, F, rng, along="x", road=True):
    """The raised board floor over x0..x1 x z0..z1 (top at F): boards along the corridor, edge beams, sleepers on
    short posts, a Geometry block under the floor down to grade (nobody crawls under), Roadway on top."""
    P.add(box(x0, x1, F - 0.10, F, z0, z1, WOOD, vis=(), geo=True, view=True, fire=True, tag="deck_geo"))
    P.add(box(x0 + 0.01, x1 - 0.01, -0.30, F - 0.10, z0 + 0.03, z1 - 0.03, WOOD, vis=(), geo=True, view=False,
              fire=None, tag="under_block"))
    if road:
        P.road([(x0, F, z0), (x1, F, z0), (x1, F, z1), (x0, F, z1)], "boards_ext")
    # boards (R1) along x (or z), one far slab (R2 / R3)
    if along == "x":
        z = z0
        while z < z1 - 1e-3:
            e = min(z1, z + rng.uniform(0.18, 0.26))
            if z1 - e < 0.09:
                e = z1
            P.add(box(x0 + 0.001, x1 - 0.001, F - 0.03, F, z + 0.002, e - 0.002, WOOD, vis=(1,), tag="floor_board",
                      uvoff=(rng.random(), rng.random()), grain="long"))
            z = e
    else:
        P.extend(board_run(x0, x1, F - 0.03, F, z0, z1, rng, 0.18, 0.26, WOOD, vertical=True, vis=(1,),
                           tag="floor_board"))
    P.add(box(x0, x1, F - 0.03, F - 0.004, z0, z1, WOOD, vis=(2, 3), tag="floor_lod"))
    # dark underside board (the void reads dark) + the sleepers
    P.add(box(x0, x1, F - 0.20, F - 0.03, z0 + 0.02, z1 - 0.02, "wood_sooted", vis=(1, 2), tag="under_void"))


def _edge_beam(P, x0, x1, z, F, sg):
    za, zb = sorted((z - sg * 0.13, z - sg * 0.012))
    P.add(box(x0, x1, F - 0.19, F - 0.032, za, zb, WOOD, vis=(1, 2, 3), tag="en_katsura", grain="long"))


def _frame_side(P, x0, x1, z, F, y_tie):
    """Head tie (kashira-nuki) and keta along one post line from x0 to x1."""
    P.add(box(x0, x1, F + y_tie, F + y_tie + 0.10, z - 0.035, z + 0.035, WOOD, vis=(1, 2), tag="kashiranuki",
              grain="long"))
    P.add(box(x0, x1, F + H_KETA, F + H_KETA + 0.18, z - 0.06, z + 0.06, WOOD, vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="keta", grain="long"))


def _tie_across(P, x, D, F, S):
    """A tie beam across the corridor at a post pair (koryo, on the keta) + a strut to the ridge beam."""
    P.add(box(x - 0.06, x + 0.06, F + H_KETA - 0.02, F + H_KETA + 0.16, -D / 2 - 0.07, D / 2 + 0.07, WOOD,
              vis=(1, 2), tag="koryo", grain="long"))
    yr = S.y(S.R, -0.10)
    P.add(box(x - 0.045, x + 0.045, F + H_KETA + 0.16, yr - 0.10, -0.045, 0.045, WOOD, vis=(1,), tag="tsuka"))


def _ridge_beam(P, x0, x1, S, along="x"):
    yr = S.y(S.R, 0.0)
    if along == "x":
        P.add(box(x0, x1, yr - 0.12, yr - 0.002, -0.06, 0.06, WOOD, vis=(1, 2), tag="munagi", grain="long"))
    else:
        P.add(box(-0.06, 0.06, yr - 0.12, yr - 0.002, x0, x1, WOOD, vis=(1, 2), tag="munagi", grain="long"))


# ------------------------------------------------------------------------------------------------ sides
def _side(P, kind, x0, x1, z, sg, F, rng, ends=("open", "open"), lift=0.0, posts_at=()):
    """One side of a run between x0 and x1 on the post line z (sg: +1 = the +z side). posts_at: the post x's inside
    the run (walls stop at their faces)."""
    if kind == "none":
        return
    if kind == "open":
        r = Part("rail", "", "")
        zc = z + sg * RAIL_Z
        KR.rail(r, (x0, zc), (x1, zc), style="plain", ends=ends, lift=lift)
        P.merge(r.transformed(0.0, (0.0, F, 0.0)))
        return
    # walls between the posts
    stops = sorted(set([x0] + [p for p in posts_at if x0 < p < x1] + [x1]))
    for a, b in zip(stops[:-1], stops[1:]):
        a2 = a + (POST / 2 if any(abs(a - p) < 1e-6 for p in posts_at) else 0.0)
        b2 = b - (POST / 2 if any(abs(b - p) < 1e-6 for p in posts_at) else 0.0)
        if b2 - a2 < 0.05:
            continue
        if kind == "half":
            za, zb = z - 0.02, z + 0.02
            P.extend(board_run(a2, b2, F, F + 0.90, za, zb, rng, 0.20, 0.28, WOOD, vis=(1,), tag="koshi_board"))
            P.add(box(a2, b2, F, F + 0.90, za, zb, WOOD, vis=(2, 3), geo=True, view=True, fire=True, tag="koshi_lod"))
            P.add(box(a2 - (0.0 if a2 > a else 0.0), b2, F + 0.90, F + 0.95, z - 0.06, z + 0.06, WOOD, vis=(1, 2, 3),
                      tag="koshi_cap"))
            continue
        mat = "wall_shikkui" if kind in ("enclosed", "blank") else WOOD
        t = 0.04
        za, zb = z - t, z + t
        top = F + H_TIE
        win = kind in ("enclosed", "board") and b2 - a2 > 0.9
        if win:
            wa, wb_ = (a2 + b2) / 2 - 0.40, (a2 + b2) / 2 + 0.40
            yw0, yw1 = F + 0.85, F + 1.60
            parts = [(a2, wa, F, top), (wb_, b2, F, top), (wa, wb_, F, yw0), (wa, wb_, yw1, top)]
        else:
            parts = [(a2, b2, F, top)]
        for (p0, p1, y0, y1) in parts:
            if kind == "board":
                P.extend(board_run(p0, p1, y0, y1, za + 0.02, zb - 0.02, rng, 0.22, 0.30, WOOD, vis=(1,),
                                   tag="wall_board"))
                P.add(box(p0, p1, y0, y1, za + 0.02, zb - 0.02, WOOD, vis=(2, 3), geo=True, view=True, fire=True,
                          tag="wall_board_lod"))
            else:
                P.add(box(p0, p1, y0, y1, za, zb, mat, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="roka_wall"))
        if kind == "enclosed":
            # a board wainscot under the plaster (weather) on the outside face
            P.extend(board_run(a2, b2, F, F + 0.60, (zb if sg > 0 else za - 0.015), (zb + 0.015 if sg > 0 else za),
                               rng, 0.20, 0.28, WOOD, vis=(1,), tag="koshiita"))
        if win:
            # renji-mado: a frame + vertical square bars (see-through: the bars only, no View in the gap)
            for (p0, p1, y0, y1) in ((wa - 0.04, wa, yw0, yw1), (wb_, wb_ + 0.04, yw0, yw1),
                                     (wa - 0.04, wb_ + 0.04, yw0 - 0.04, yw0), (wa - 0.04, wb_ + 0.04, yw1, yw1 + 0.04)):
                P.add(box(p0, p1, y0, y1, za - 0.012, zb + 0.012, WOOD, vis=(1, 2), tag="renji_frame"))
            n = 9
            for k in range(1, n):
                xx = wa + (wb_ - wa) * k / n
                P.add(box(xx - 0.017, xx + 0.017, yw0, yw1, -0.017 + z, 0.017 + z, WOOD, vis=(1,) if k % 2 else (1, 2),
                          geo=True, view=False, fire=None, tag="renji_bar"))


# ------------------------------------------------------------------------------------------------ modules
def straight(L=KEN, sides=("open", "open"), roof="itabuki", profile="straight", ends=("seam", "seam"), branches=(),
             D=KEN, floor=FLOOR, posts0=True, posts1=None, pid="jp_p_roka_straight", variant="", state=None, seed=0,
             roof_trim=(0.0, 0.0)):
    """A straight corridor module along +x 0..L. ends: roof ends 'seam' | 'gable' | 'hip'; an end with 'gable' or
    'hip' also gets its posts (posts1). branches: as striproof.straight (a junction past that end)."""
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="covered corridor (watari-roka) / kairo module",
             datum="run along +x 0..L on the corridor centreline z 0, posts on z = +-D/2; y 0 = grade, floor %.2f" % floor,
             recipe="roka.straight(L=%.3f, sides=%r, roof=%r, profile=%r, ends=%r)" % (L, sides, roof, profile, ends))
    rng = rng_for(pid + variant + str(seed))
    F = floor
    S = _spec(D, F, roof, profile)
    posts1 = (ends[1] != "seam") if posts1 is None else posts1
    pxs = ([0.0] if posts0 else []) + ([L] if posts1 else [])
    top = F + H_KETA
    for x in pxs:
        for sg in (-1.0, 1.0):
            _post(P, x, sg * D / 2, 0.0, top, rng)
    # floor and frame
    z0, z1 = -D / 2 - DECK_OUT, D / 2 + DECK_OUT
    _deck(P, 0.0, L, z0, z1, F, rng)
    for sg in (-1.0, 1.0):
        _edge_beam(P, 0.0, L, sg * (D / 2 + DECK_OUT), F, sg)
        _frame_side(P, 0.0, L, sg * D / 2, F, H_TIE)
        # sleepers' short posts on stones under the deck edge every half ken
        x = 0.0 + HALF / 2
        while x < L:
            P.add(box(x - 0.045, x + 0.045, 0.0, F - 0.19, sg * (D / 2 + DECK_OUT - 0.07) - 0.045,
                      sg * (D / 2 + DECK_OUT - 0.07) + 0.045, WOOD, vis=(1,), tag="tsuka_floor"))
            x += HALF
    for x in pxs:
        _tie_across(P, x, D, F, S)
    _ridge_beam(P, 0.0, L, S)
    # sides
    inner_posts = [x for x in pxs]
    for sg, kind in zip((-1.0, 1.0), sides):
        _side(P, kind, 0.0, L, sg * D / 2, sg, F, rng, posts_at=inner_posts)
    # gable infill at a gable end with an enclosed side? (open corridors keep the gable open: rafters show)
    r = Part(pid + "_roof", "", "")
    info = SR.straight(r, S, L - roof_trim[0] - roof_trim[1], ends, branches=branches)
    P.merge(r.transformed(0.0, (roof_trim[0], 0.0, 0.0)))
    if state == "decay":
        _decay(P, rng)
    for x in (0.0, L):
        P.conn("post", (x, 0.0, -D / 2), hidden=not (x in pxs), role="roka_node")
        P.conn("post", (x, 0.0, D / 2), hidden=not (x in pxs), role="roka_node")
    P.conn("floor", (0.0, F, 0.0), role="floor_start")
    P.conn("floor", (L, F, 0.0), role="floor_end")
    P.dim("clear_between_posts_m", ">=1.00 (D5)", D - POST)
    P.dim("head_under_tie_m", ">=2.05", H_TIE)
    P.floors.append({"name": "roka", "rect": (0.0, L, z0, z1), "y": F, "obstacles": [], "enclosed": False})
    P.meta["roof_info"] = {k: v for k, v in info.items() if k in ("ridge_y", "L", "ends")}
    P.meta["spec"] = {"D": D, "floor": F, "y_bear": S.y_bear, "ridge_y": S.ridge_y(), "roof": roof, "profile": profile}
    return P


def junction(arms, sides=None, roof="itabuki", profile="straight", D=KEN, floor=FLOOR, pid="jp_p_roka_corner",
             variant="", seed=0):
    """A corner / T / cross cell centred on (0, 0). sides: {side: kind} for the outer (non-arm) sides, default
    'open'."""
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="covered corridor junction (corner / T / cross)",
             datum="centred on the crossing of the centrelines; posts at (+-D/2, +-D/2); y 0 = grade, floor %.2f" % floor,
             recipe="roka.junction(arms=%r, sides=%r, roof=%r, profile=%r)" % (arms, sides, roof, profile))
    rng = rng_for(pid + variant + str(seed))
    F = floor
    S = _spec(D, F, roof, profile)
    sides = dict(sides or {})
    top = F + H_KETA
    h = D / 2
    for sx in (-1.0, 1.0):
        for sz in (-1.0, 1.0):
            _post(P, sx * h, sz * h, 0.0, top, rng)
    x0 = -h - (0.0 if "-x" in arms else DECK_OUT)
    x1 = h + (0.0 if "+x" in arms else DECK_OUT)
    z0 = -h - (0.0 if "-z" in arms else DECK_OUT)
    z1 = h + (0.0 if "+z" in arms else DECK_OUT)
    # the deck: the cell plus the outer edges; arms' deck strips come from their straight modules
    _deck(P, x0, x1, z0, z1, F, rng)
    # frame on all four post lines (keta / head ties on the outer sides; on arm sides the keta continues the arm's)
    for name, (a, b, c, axis) in {"-z": (-h, h, -h, "x"), "+z": (-h, h, h, "x"), "-x": (-h, h, -h, "z"),
                                  "+x": (-h, h, h, "z")}.items():
        if axis == "x":
            P.add(box(a, b, F + H_KETA, F + H_KETA + 0.18, c - 0.06, c + 0.06, WOOD, vis=(1, 2, 3), geo=True,
                      view=True, fire=True, tag="keta", grain="long"))
            if name not in arms:
                P.add(box(a, b, F + H_TIE, F + H_TIE + 0.10, c - 0.035, c + 0.035, WOOD, vis=(1, 2),
                          tag="kashiranuki"))
        else:
            P.add(box(c - 0.06, c + 0.06, F + H_KETA + 0.003, F + H_KETA + 0.177, a + 0.06, b - 0.06, WOOD,
                      vis=(1, 2, 3), geo=True, view=True, fire=True, tag="keta", grain="long"))
            if name not in arms:
                P.add(box(c - 0.035, c + 0.035, F + H_TIE + 0.003, F + H_TIE + 0.097, a + 0.06, b - 0.06, WOOD,
                          vis=(1, 2), tag="kashiranuki"))
    # outer sides: walls / rails; edge beams
    for name, sg in (("-z", -1.0), ("+z", 1.0)):
        if name in arms:
            continue
        kind = sides.get(name, "open")
        _edge_beam(P, x0, x1, sg * (h + DECK_OUT), F, sg)
        if kind == "open":
            e0 = "open" if "-x" in arms else "cross"
            e1 = "open" if "+x" in arms else "cross"
            r = Part("rail", "", "")
            KR.rail(r, (x0 if "-x" in arms else -h - RAIL_Z, sg * (h + RAIL_Z)),
                    (x1 if "+x" in arms else h + RAIL_Z, sg * (h + RAIL_Z)), ends=(e0, e1))
            P.merge(r.transformed(0.0, (0.0, F, 0.0)))
        else:
            _side(P, kind, -h, h, sg * h, sg, F, rng, posts_at=(-h, h))
    for name, sg in (("-x", -1.0), ("+x", 1.0)):
        if name in arms:
            continue
        kind = sides.get(name, "open")
        sub_ = Part("sx", "", "")
        # build along x in a rotated frame: local x = world z
        if kind == "open":
            e0 = "open" if "-z" in arms else "cross"
            e1 = "open" if "+z" in arms else "cross"
            zz0 = z0 if "-z" in arms else -h - RAIL_Z
            zz1 = z1 if "+z" in arms else h + RAIL_Z
            r = Part("rail", "", "")
            KR.rail(r, (sg * (h + RAIL_Z), zz0), (sg * (h + RAIL_Z), zz1), ends=(e0, e1), lift=0.015)
            P.merge(r.transformed(0.0, (0.0, F, 0.0)))
        else:
            _side(sub_, kind, -h, h, -sg * h, -sg, F, rng, posts_at=(-h, h))
            P.merge(sub_.transformed(90.0))
        za, zb = (z0, z1)
        xa, xb = sorted((sg * (h + DECK_OUT - 0.13), sg * (h + DECK_OUT - 0.012)))
        P.add(box(xa, xb, F - 0.19, F - 0.032, za + (0.13 if "-z" not in arms else 0.0),
                  zb - (0.13 if "+z" not in arms else 0.0), WOOD, vis=(1, 2, 3), tag="en_katsura", grain="long"))
    # ridge beams only under the arms' ridges (toward a hip the roof drops: a through beam would poke it, C12)
    xa_ = -h if "-x" in arms else -0.06
    xb_ = h if "+x" in arms else 0.06
    if ("-x" in arms) or ("+x" in arms):
        _ridge_beam(P, xa_, xb_, S)
    if "-z" in arms:
        _ridge_beam(P, -h, -0.061, S, along="z")
    if "+z" in arms:
        _ridge_beam(P, 0.061, h, S, along="z")
    r = Part(pid + "_roof", "", "")
    SR.junction(r, S, tuple(arms))
    P.merge(r)
    for sx in (-1.0, 1.0):
        for sz in (-1.0, 1.0):
            P.conn("post", (sx * h, 0.0, sz * h), role="roka_node")
    P.floors.append({"name": "roka_j", "rect": (x0, x1, z0, z1), "y": F, "obstacles": [], "enclosed": False})
    P.meta["spec"] = {"D": D, "floor": F, "y_bear": S.y_bear, "ridge_y": S.ridge_y(), "roof": roof, "profile": profile,
                      "arms": tuple(arms)}
    return P


def stair(L=2 * KEN, rise=0.455, sides=("open", "open"), roof="itabuki", profile="straight", D=KEN, floor=FLOOR,
          pid="jp_p_roka_stair", variant="", seed=0, posts0=True):
    """A covered stair module (level change on a slope; nobori-ro form): the floor rises `rise` over the middle of
    the module (landings at both ends, risers <= 0.16, a hidden walk ramp <= 38 deg), the roof at the UPPER level with
    a gable over the lower module's roof and a board infill closing the step between the two roofs."""
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="covered stair corridor (level change)",
             datum="run along +x 0..L, floor %.2f at x 0 and %.2f at x L (y 0 = grade at x 0)" % (floor, floor + rise),
             recipe="roka.stair(L=%.3f, rise=%.3f, sides=%r, roof=%r)" % (L, rise, sides, roof))
    rng = rng_for(pid + variant + str(seed))
    F0, F1 = floor, floor + rise
    S = _spec(D, F1, roof, profile)
    n = max(2, int(math.ceil(rise / 0.16 - 1e-9)))
    rh = rise / n
    going = 0.30
    run = going * n
    if run / L > 0.8 or math.degrees(math.atan(rise / run)) > 37.8:
        run = rise / math.tan(math.radians(37.0))
        going = run / n
    xs0 = (L - run) / 2
    xs1 = xs0 + run
    top0, top1 = F0 + H_KETA, F1 + H_KETA
    for x, tp in ([(0.0, top1)] if posts0 else []) + [(L, top1)]:
        for sg in (-1.0, 1.0):
            _post(P, x, sg * D / 2, 0.0, tp, rng)
    z0, z1 = -D / 2 - DECK_OUT, D / 2 + DECK_OUT
    # lower landing, upper landing, the stair between
    _deck(P, 0.0, xs0, z0, z1, F0, rng)
    _deck(P, xs1, L, z0, z1, F1, rng)
    P.add(box(xs0, xs1, -0.30, F0 - 0.10, z0 + 0.03, z1 - 0.03, WOOD, vis=(), geo=True, view=False, fire=None,
              tag="under_block"))
    # hidden ramp (Geometry / View / Fire) + Roadway 'stair'
    P.add(prism([(xs0, F0 - 0.10), (xs0, F0), (xs1, F1), (xs1, F1 - 0.10)], "z", z0 + 0.02, z1 - 0.02, WOOD, vis=(),
                geo=True, view=True, fire="wood", tag="stair_ramp"))
    P.road([(xs0, F0, z0 + 0.02), (xs1, F1, z0 + 0.02), (xs1, F1, z1 - 0.02), (xs0, F0, z1 - 0.02)], "stair")
    # treads + risers (closed: a corridor stair), stringers
    for k in range(n):
        xa = xs0 + k * going
        ya = F0 + (k + 1) * rh
        P.add(box(xa, xa + going + 0.02 if k < n - 1 else xs1, ya - 0.035, ya, z0 + 0.02, z1 - 0.02, WOOD, vis=(1,),
                  tag="stair_tread", grain="long", uvoff=(rng.random(), rng.random())))
        P.add(box(xa - 0.025, xa, F0 + k * rh - 0.035, ya - 0.035, z0 + 0.03, z1 - 0.03, WOOD, vis=(1,),
                  tag="stair_riser"))
    P.add(prism([(xs0, F0 - 0.03), (xs1, F1 - 0.03), (xs1, F1 - 0.004), (xs0, F0 - 0.004)], "z", z0 + 0.02,
                z1 - 0.02, WOOD, vis=(2, 3), tag="stair_lod"))
    for sg in (-1.0, 1.0):
        zs = sg * (D / 2 + DECK_OUT - 0.03)
        za, zb = sorted((zs, zs - sg * 0.06))
        P.add(prism([(xs0 - 0.05, F0 - 0.25), (xs0 - 0.05, F0 + 0.02), (xs1 + 0.05, F1 + 0.02),
                     (xs1 + 0.05, F1 - 0.25)], "z", za, zb, WOOD, vis=(1, 2, 3), tag="stringer"))
        _edge_beam(P, 0.0, xs0, sg * (D / 2 + DECK_OUT), F0, sg)
        _edge_beam(P, xs1, L, sg * (D / 2 + DECK_OUT), F1, sg)
        _frame_side(P, 0.0, L, sg * D / 2, F1, H_TIE)
        # stair-side rails: a sloped top rail + posts (the koran stops at the landings)
        kind = sides[0 if sg < 0 else 1]
        zc = sg * (D / 2 + RAIL_Z)
        if kind in ("open", "half"):
            pts = [(0.0, F0), (xs0, F0), (xs1, F1), (L, F1)]
            for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
                P.add(tube((xa, ya + 0.75 - 0.035, zc), (xb, yb + 0.75 - 0.035, zc), 0.035, WOOD, n=8, vis=(1, 2),
                           tag="hokogi"))
                P.add(tube((xa, ya + 0.37, zc), (xb, yb + 0.37, zc), 0.028, WOOD, n=6, vis=(1,), tag="hirageta"))
                c = [(xa, ya, zc - 0.04), (xb, yb, zc - 0.04), (xb, yb, zc + 0.04), (xa, ya, zc + 0.04),
                     (xa, ya + 0.75, zc - 0.04), (xb, yb + 0.75, zc - 0.04), (xb, yb + 0.75, zc + 0.04),
                     (xa, ya + 0.75, zc + 0.04)]
                P.add(hexa(c, WOOD, vis=(), geo=True, view=False, fire=None, tag="koran_geo"))
            m = max(2, int(L / HALF))
            for k in range(1, m):
                x = L * k / m
                y = F0 if x <= xs0 else (F1 if x >= xs1 else F0 + (x - xs0) / run * rise)
                P.add(box(x - 0.022, x + 0.022, y, y + 0.72, zc - 0.022, zc + 0.022, WOOD, vis=(1,), tag="totsuka"))
        else:
            _side(P, "blank" if kind == "blank" else kind, 0.0, L, sg * D / 2, sg, F1, rng, posts_at=(0.0, L))
    for x in ([0.0] if posts0 else []) + [L]:
        _tie_across(P, x, D, F1, S)
    _ridge_beam(P, 0.0, L, S)
    r = Part(pid + "_roof", "", "")
    SR.straight(r, S, L, ("gable", "seam"))
    P.merge(r)
    # the step between the roofs: board infill on the x 0 line from the lower roof up to this roof's rafters
    lo = _spec(D, F0, roof, profile)
    # boards 0.12 wide, each a quad following both roof lines (sits on the lower covering, under the upper rafters)
    zs = [(-D / 2 - lo.ov) + k * 0.12 for k in range(int((D + 2 * lo.ov) / 0.12) + 2)]
    zs = sorted(set([round(z, 6) for z in zs if z < D / 2 + lo.ov] + [0.0, round(D / 2 + lo.ov, 6)]))
    xi = -S.gov + 0.06

    def ylo(z):
        return lo.y(lo.R - abs(z), lo.stack + lo.top + (0.21 if lo.kind == "tile" and abs(z) < 0.15 else 0.0)) + 0.004

    def yhi(z):
        return S.y(S.R - abs(z), 0.0) - 0.015
    for za, zb in zip(zs[:-1], zs[1:]):
        za_, zb_ = za + 0.002, zb - 0.002
        if min(yhi(za_) - ylo(za_), yhi(zb_) - ylo(zb_)) < 0.02:
            continue
        P.add(prism([(ylo(za_), za_), (ylo(zb_), zb_), (yhi(zb_), zb_), (yhi(za_), za_)], "x", xi, xi + 0.025, WOOD,
                    vis=(1, 2, 3), tag="step_infill", uvoff=(rng.random(), 0.0)))
    P.conn("floor", (0.0, F0, 0.0), role="floor_start")
    P.conn("floor", (L, F1, 0.0), role="floor_end", rise=rise)
    P.dim("stair_angle_deg", "<=38 (D4)", math.degrees(math.atan(rise / run)), tol=0.0)
    P.dim("riser_m", "<=0.16", rh, tol=0.0)
    P.floors.append({"name": "landing_lo", "rect": (0.0, xs0, z0, z1), "y": F0, "obstacles": [], "enclosed": False})
    P.floors.append({"name": "landing_hi", "rect": (xs1, L, z0, z1), "y": F1, "obstacles": [], "enclosed": False})
    P.meta["stair"] = {"run": run, "risers": n, "riser": rh, "going": going, "x0": xs0, "x1": xs1,
                       "angle": math.degrees(math.atan(rise / run))}
    return P


def connector(L=HALF, sides=("open", "open"), roof="itabuki", profile="straight", D=KEN, floor=FLOOR,
              pid="jp_p_roka_connector", variant="", seed=0):
    """The end that butts a host building at x = L (its wall / veranda edge on that plane): posts at x 0 only, the
    floor to 1 cm short of the host, the roof ends plain at the host wall with a flashing board against it. Check
    with connector_fit() that the ridge clears the host's eave soffit."""
    P = straight(L, sides, roof, profile, ("seam", "seam"), D=D, floor=floor, posts1=False, pid=pid, variant=variant,
                 seed=seed)
    S = _spec(D, floor, roof, profile)
    # flashing (mizukiri) board against the host wall following the roof top
    for sg in (-1.0, 1.0):
        za, zb = (0.0, sg * (D / 2 + S.ov)) if sg > 0 else (sg * (D / 2 + S.ov), 0.0)
        y_ridge = S.y(S.R, S.stack + S.top + 0.03)
        y_eave = S.y(0.0, S.stack + S.top + 0.03)
        c = [(L - 0.025, y_eave, sg * (D / 2 + S.ov)), (L - 0.025, y_ridge, 0.0), (L - 0.025, y_ridge + 0.12, 0.0),
             (L - 0.025, y_eave + 0.12, sg * (D / 2 + S.ov)), (L - 0.005, y_eave, sg * (D / 2 + S.ov)),
             (L - 0.005, y_ridge, 0.0), (L - 0.005, y_ridge + 0.12, 0.0), (L - 0.005, y_eave + 0.12, sg * (D / 2 + S.ov))]
        P.add(hexa(c, WOOD, vis=(1, 2, 3), tag="flashing"))
    P.meta["host_plane_x"] = L
    P.meta["ridge_top_y"] = S.y(S.R, S.stack + S.top) + 0.20
    return P


def connector_fit(host_soffit_y, floor=FLOOR, roof="itabuki", D=KEN, profile="straight"):
    """(fits, ridge_top_y, margin): the corridor's ridge top at the host wall plane vs the host's eave soffit there
    (both over the same grade). A host with a lower soffit needs a lower corridor floor or a narrower corridor."""
    S = _spec(D, floor, roof, profile)
    ridge_top = S.y(S.R, S.stack + S.top) + (0.20 if S.kind == "tile" else 0.08)
    return host_soffit_y - ridge_top >= 0.03, round(ridge_top, 3), round(host_soffit_y - ridge_top, 3)


def _decay(P, rng):
    """Dead-world corridor: a few floor boards gone (dark void shows), some rail pieces missing."""
    keep = []
    for s in P.solids:
        if s.tag in ("floor_board",) and rng.random() < 0.18:
            continue
        if s.tag in ("totsuka", "to_block", "koran_tsuka") and rng.random() < 0.35:
            continue
        keep.append(s)
    P.solids = keep
    P.wear = "_w2"


# ------------------------------------------------------------------------------------------------ whole runs
def run_roka(path, sides=("open", "open"), roof="itabuki", profile="straight", D=KEN, floor=FLOOR, stairs=(),
             name="roka_run", gable_ends=(True, True), connect=(False, False), host_face=0.08):
    """A corridor along grid nodes [(x, z), ...] (axis-aligned, lengths on the half-ken grid, >= D between corners).
    Corners get junction cells. sides = (right of travel, left of travel) = the straight modules' ('-z', '+z')
    sides (local +z is the left of travel); at a corner the outer sides take the kind of the turn's outside. stairs: [(segment index, offset, length, rise)]: a stair module there; the
    floor after it is that much higher. gable_ends: gable roof ends at the path ends (False: seam, for a connector).
    connect: (start, end): that path end lies on a host building's wall plane: a connector module (half a ken, the
    roof ends plain at the host with a flashing board, its posts away from the host) is put there.
    Returns a merged Part."""
    P = Part(name, "", GROUP)
    path = [tuple(p) for p in path]
    hosts = []
    for k, (flag, i0, i1) in enumerate(((connect[0], 0, 1), (connect[1], -1, -2))):
        if not flag:
            continue
        a_, b_ = path[i0], path[i1]
        Ls = math.dist(a_, b_)
        u = ((b_[0] - a_[0]) / Ls, (b_[1] - a_[1]) / Ls)
        new = (a_[0] + u[0] * HALF, a_[1] + u[1] * HALF)
        # the connector runs from `new` back to the host's wall FACE (host_face past the node a_ toward new)
        deg = math.degrees(math.atan2(a_[1] - new[1], a_[0] - new[0]))
        hosts.append((new, deg, k))
        path[i0] = new
        gable_ends = tuple(False if j == k else g for j, g in enumerate(gable_ends))
    segs = list(zip(path[:-1], path[1:]))
    F = floor
    for i, (a, b) in enumerate(segs):
        dx, dz = b[0] - a[0], b[1] - a[1]
        Ls = math.hypot(dx, dz)
        deg = math.degrees(math.atan2(dz, dx))
        ux, uz = dx / Ls, dz / Ls
        # corner at the start / end of this segment (junction cells take D/2 of the segment at each corner)
        c0 = i > 0
        c1 = i < len(segs) - 1
        s0 = D / 2 if c0 else 0.0
        s1 = Ls - (D / 2 if c1 else 0.0)

        def turn(j):
            (p, q), (r_, s_) = segs[j], segs[j + 1]
            d1 = (q[0] - p[0], q[1] - p[1])
            d2 = (s_[0] - r_[0], s_[1] - r_[1])
            return "+z" if d1[0] * d2[1] - d1[1] * d2[0] > 0 else "-z"
        br = []
        if c0:
            # the previous segment comes in from this segment's local side
            br.append((0, "+z" if turn(i - 1) == "+z" else "-z"))
        if c1:
            br.append((1, turn(i)))
        # straight pieces between s0 and s1, with stairs
        pcs = []
        x = s0
        for st in sorted([s for s in stairs if s[0] == i], key=lambda s: s[1]):
            if st[1] > x + 1e-6:
                pcs.append(("run", x, st[1]))
            pcs.append(("stair", st[1], st[1] + st[2], st[3]))
            x = st[1] + st[2]
        if s1 > x + 1e-6:
            pcs.append(("run", x, s1))
        for k, pc in enumerate(pcs):
            x0, x1 = pc[1], pc[2]
            first, last = k == 0, k == len(pcs) - 1
            if pc[0] == "stair":
                q = stair(x1 - x0, pc[3], sides, roof, profile, D=D, floor=F, pid=name + "_st%d%d" % (i, k),
                          posts0=not (first and c0))
                F += pc[3]
            else:
                e0 = "seam" if (c0 or not first or i > 0) else ("gable" if gable_ends[0] else "seam")
                e1 = "seam" if (c1 or not last) else ("gable" if gable_ends[1] else "seam")
                b_ = [bb for bb in br if (bb[0] == 0 and first) or (bb[0] == 1 and last)]
                # the roof before a stair stops short of the stair's posts and tie beam (they rise to the upper level)
                nxt_stair = k < len(pcs) - 1 and pcs[k + 1][0] == "stair"
                q = straight(x1 - x0, sides, roof, profile, (e0, e1), branches=b_, D=D, floor=F,
                             posts0=not (first and c0), posts1=(e1 == "gable"),
                             pid=name + "_s%d%d" % (i, k), seed=i * 10 + k,
                             roof_trim=(0.0, 0.07 if nxt_stair else 0.0))
            P.merge(q.transformed(deg, (a[0] + ux * x0, 0.0, a[1] + uz * x0)))
        if c1:
            # the corner cell at node b: arms = back along this segment and out along the next
            n_ = segs[i + 1]
            d2 = (n_[1][0] - n_[0][0], n_[1][1] - n_[0][1])
            L2 = math.hypot(*d2)
            arm_in = (-ux, -uz)
            arm_out = (d2[0] / L2, d2[1] / L2)
            arms = []
            for v in (arm_in, arm_out):
                arms.append({(1, 0): "+x", (-1, 0): "-x", (0, 1): "+z", (0, -1): "-z"}[(round(v[0]), round(v[1]))])
            outer = [s_ for s_ in ("-x", "+x", "-z", "+z") if s_ not in arms]
            # the outer sides take the side kind of the outside of the turn
            left_turn = turn(i) == "+z"
            okind = sides[0] if left_turn else sides[1]
            q = junction(tuple(arms), {s_: okind for s_ in outer}, roof, profile, D=D, floor=F,
                         pid=name + "_j%d" % i)
            P.merge(q.transformed(0.0, (b[0], 0.0, b[1])))
    for (pt, deg, k) in hosts:
        # sides seen from the connector's own frame (it runs toward the host): start = reversed travel
        sd = (sides[1], sides[0]) if k == 0 else sides
        q = connector(HALF - host_face, sd, roof, profile, D=D, floor=floor if k == 0 else F, pid=name + "_c%d" % k)
        P.merge(q.transformed(deg, (pt[0], 0.0, pt[1])))
    return P


# ------------------------------------------------------------------------------------------------ registry
def _s(L, sides, roof, profile="straight", **kw):
    return ("straight", dict(L=L, sides=sides, roof=roof, profile=profile, **kw))


def _j(arms, kind, roof, profile="straight"):
    return ("junction", dict(arms=arms, kind=kind, roof=roof, profile=profile))


VARIANTS = {
    "jp_p_roka_straight": {
        "_1ken_open_itabuki": _s(KEN, ("open", "open"), "itabuki"),
        "_2ken_open_itabuki": _s(2 * KEN, ("open", "open"), "itabuki"),
        "_3ken_open_itabuki": _s(3 * KEN, ("open", "open"), "itabuki"),
        "_2ken_half_kokera": _s(2 * KEN, ("half", "half"), "kokera"),
        "_2ken_enclosed_sangawara": _s(2 * KEN, ("open", "enclosed"), "sangawara"),
        "_2ken_board_sangawara": _s(2 * KEN, ("board", "board"), "sangawara"),
        "_2ken_blank_itabuki": _s(2 * KEN, ("blank", "blank"), "itabuki"),
        "_2ken_open_sori_kokera": _s(2 * KEN, ("open", "open"), "kokera", "sori"),
        "_2ken_open_sori_hongawara": _s(2 * KEN, ("open", "open"), "hongawara", "sori"),
        "_2ken_ab_decay": _s(2 * KEN, ("open", "half"), "itabuki", state="decay"),
    },
    "jp_p_roka_corner": {
        "_open_itabuki": _j(("-x", "+z"), "open", "itabuki"),
        "_open_sangawara": _j(("-x", "+z"), "open", "sangawara"),
        "_enclosed_sangawara": _j(("-x", "+z"), "enclosed", "sangawara"),
        "_open_sori_kokera": _j(("-x", "+z"), "open", "kokera", "sori"),
    },
    "jp_p_roka_tee": {
        "_open_itabuki": _j(("-x", "+x", "+z"), "open", "itabuki"),
        "_open_sangawara": _j(("-x", "+x", "+z"), "open", "sangawara"),
    },
    "jp_p_roka_cross": {
        "_open_itabuki": _j(("-x", "+x", "-z", "+z"), "open", "itabuki"),
        "_open_hongawara": _j(("-x", "+x", "-z", "+z"), "open", "hongawara"),
    },
    "jp_p_roka_end": {
        "_gable_itabuki": _s(KEN, ("open", "open"), "itabuki", ends=("seam", "gable")),
        "_gable_sangawara": _s(KEN, ("open", "open"), "sangawara", ends=("seam", "gable")),
        "_hip_sangawara": _s(KEN, ("open", "open"), "sangawara", ends=("seam", "hip")),
        "_gable_sori_kokera": _s(KEN, ("open", "open"), "kokera", "sori", ends=("seam", "gable")),
    },
    "jp_p_roka_stair": {
        "_046_itabuki": ("stair", dict(rise=0.455, sides=("open", "open"), roof="itabuki")),
        "_091_sangawara": ("stair", dict(rise=0.91, sides=("open", "open"), roof="sangawara")),
        "_046_half_kokera": ("stair", dict(rise=0.455, sides=("half", "half"), roof="kokera")),
    },
    "jp_p_roka_connector": {
        "_itabuki": ("connector", dict(roof="itabuki")),
        "_sangawara": ("connector", dict(roof="sangawara")),
    },
    "jp_p_kairo": {
        "_2ken_hongawara": _s(2 * KEN, ("open", "enclosed"), "hongawara"),
        "_2ken_sori_hongawara": _s(2 * KEN, ("open", "enclosed"), "hongawara", "sori"),
        "_2ken_sori_hiwada": _s(2 * KEN, ("open", "enclosed"), "hiwada", "sori"),
        "_corner_hongawara": _j(("-x", "+z"), "enclosed", "hongawara"),
        "_corner_sori_hiwada": _j(("-x", "+z"), "enclosed", "hiwada", "sori"),
    },
}


def part_variant(pid, variant):
    how, kw = VARIANTS[pid][variant]
    kw = dict(kw)
    if how == "straight":
        L = kw.pop("L")
        state = kw.pop("state", None)
        P = straight(L, kw.pop("sides"), kw.pop("roof"), kw.pop("profile"), kw.pop("ends", ("seam", "seam")),
                     pid=pid, variant=variant, state=state)
    elif how == "junction":
        arms = kw["arms"]
        outer = [s_ for s_ in ("-x", "+x", "-z", "+z") if s_ not in arms]
        P = junction(arms, {s_: kw["kind"] for s_ in outer}, kw["roof"], kw["profile"], pid=pid, variant=variant)
    elif how == "stair":
        P = stair(2 * KEN, kw["rise"], kw["sides"], kw["roof"], pid=pid, variant=variant)
    else:
        P = connector(HALF, roof=kw["roof"], pid=pid, variant=variant)
    P.group = GROUP
    P.notes.append("K3 corridor / kairo kit (parts/K3_NOTES.md); samples at _w1 (abandoned at _w2)")
    return P


def register(reg):
    for pid, vs in VARIANTS.items():
        reg(pid, list(vs), lambda v, pid=pid: part_variant(pid, v))
