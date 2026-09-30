"""Floors (B0 step 0a, promoted from buildings/machiya_t3_01): tatami rooms, board floors, doma (earth) floors and the
sealed loft floor, each as a sub-Part in the building's kit frame (x, z plan rectangle, y up; no transform). The caller
merges it (a Builder merges floors while its interior flag is on, so they drop out of Resolution 3).

Every floor takes `holes`: plan rectangles cut out of the floor for a stairwell or a floor pit (irori, kabata tank),
as tuples (x0, x1, z0, z1[, kind]) or dicts {rect: (x0, x1, z0, z1), kind: 'stair' | 'pit' | ...}. A hole removes the
visual floor, the support block (Geometry / View / Fire) and the Roadway over its rectangle; nothing else. Its rim and
lining (kamachi frame, pit walls, the stair itself) belong to the part that fills it: pass hole_fn(part, hole, y) and
it is called once per hole after the floor is built (B2: jp_p_floor_pit, jp_p_stair). part.meta["holes"] lists them.
Tatami holes must sit on the half-ken mat grid (they replace whole cells).

With no holes every function builds exactly what the machiya built before (same solids in the same order).
"""
from .core import Part, box, sheet, HALF, rng_for

DOMA_Y = 0.05          # PLAYBOOK §4: doma = grade + 0.05
TATAMI_T = 0.055       # mat thickness (the kit's inakama mat, G1 A2)


# ------------------------------------------------------------------------------------------------ helpers
def open_box(x0, x1, y0, y1, z0, z1, mat, keep, tag, vis=(1,), **kw):
    """Visual-only box without its hidden faces (bottom, butt ends): keep = subset of top/xlo/xhi/zlo/zhi."""
    Q = {"top": ([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0.0, 1.0, 0.0)),
         "xlo": ([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], (-1.0, 0.0, 0.0)),
         "xhi": ([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], (1.0, 0.0, 0.0)),
         "zlo": ([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0.0, 0.0, -1.0)),
         "zhi": ([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0.0, 0.0, 1.0))}
    return sheet([Q[k][0] for k in keep], mat, [Q[k][1] for k in keep], vis=vis, tag=tag, **kw)


def floor_rect(x0, x1, z0, z1):
    return (min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1))


def norm_holes(holes):
    out = []
    for h in holes or ():
        if isinstance(h, dict):
            r = h["rect"]
            out.append(dict(h, rect=floor_rect(*r[:4]), kind=h.get("kind", "hole")))
        else:
            out.append({"rect": floor_rect(*h[:4]), "kind": h[4] if len(h) > 4 else "hole"})
    return out


def rect_minus(rect, holes, eps=1e-6):
    """The plan rectangle minus hole rectangles, as a list of rectangles. No hole overlapping -> [rect]."""
    rects = [tuple(rect)]
    for h in holes:
        hx0, hx1, hz0, hz1 = h["rect"] if isinstance(h, dict) else h[:4]
        new = []
        for (x0, x1, z0, z1) in rects:
            if hx1 <= x0 + eps or hx0 >= x1 - eps or hz1 <= z0 + eps or hz0 >= z1 - eps:
                new.append((x0, x1, z0, z1))
                continue
            if hx0 > x0 + eps:
                new.append((x0, hx0, z0, z1))
            if hx1 < x1 - eps:
                new.append((hx1, x1, z0, z1))
            a, b = max(x0, hx0), min(x1, hx1)
            if hz0 > z0 + eps:
                new.append((a, b, z0, hz0))
            if hz1 < z1 - eps:
                new.append((a, b, hz1, z1))
        rects = new
    return rects


def _finish_holes(s, hs, y, hole_fn):
    s.meta["holes"] = [dict(h, y=y) for h in hs]
    if hole_fn:
        for h in hs:
            hole_fn(s, h, y)


# ------------------------------------------------------------------------------------------------ tatami
def shugi_layout(nx, nz, blocked=()):
    """Tile an nx x nz grid of half-ken cells with 2x1 mats so that no four mats meet at one point (shugi layout,
    PLAYBOOK §3). blocked: cells (i, j) left empty (a hole). Returns [(i0, i1, j0, j1)] cell rectangles."""
    grid = [[-1] * nz for _ in range(nx)]
    for (i, j) in blocked:
        grid[i][j] = -2
    mats = []

    def ok_corners():
        for i in range(1, nx):
            for j in range(1, nz):
                c = {grid[i - 1][j - 1], grid[i][j - 1], grid[i - 1][j], grid[i][j]}
                if -1 not in c and -2 not in c and len(c) == 4:
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
        raise RuntimeError("no shugi layout for %d x %d (blocked %s)" % (nx, nz, sorted(blocked)))
    return mats


MATS_TATAMI = {"facing": "straw_mushiro", "heri": "wood_sooted", "base": "wood_sooted", "lod": "straw_mushiro"}
MATS_BOARDS = {"board": "wood_weathered", "base": "wood_sooted", "lod": "wood_weathered", "slab": False}
MATS_DOMA = {"top": "wall_arakabe", "body": "stone_cut"}
# the B1 interior materials (B4 pilot, 2026-09-30): pass these as `mats` to use them; the defaults above are the
# stand-ins every building used before B1 (unchanged, so old recipes build exactly what they built)
MATS_TATAMI_B1 = {"facing": "floor_tatami", "heri": "floor_tatami_heri", "base": "wood_sooted", "lod": "floor_tatami",
                  "fit": True}
MATS_BOARDS_B1 = {"board": "floor_boards_int", "base": "wood_sooted", "lod": "floor_boards_int", "slab": True}
MATS_DOMA_T3 = {"top": "ground_doma_tataki", "body": "stone_cut"}
MATS_DOMA_EARTH = {"top": "ground_doma_earth", "body": "stone_cut"}


def _mats(default, mats):
    m = dict(default)
    m.update(mats or {})
    return m


def tatami(name, x0, x1, z0, z1, top=0.50, base=DOMA_Y, holes=(), hole_fn=None, mats=None, cells=None):
    """Raised room floor: support block (Geometry), base under the mats, one slab per mat (TATAMI_T, straw_mushiro as
    the rush facing), heri edges along the long sides (LOD 1), one slab in LOD 2/3. Roadway 'tatami' at `top`.
    `base` = the level the floor stands on (the doma).
    mats: MATS_TATAMI keys (B1: MATS_TATAMI_B1, whose 'fit' maps the one-mat texture once onto every mat, its length
    along the mat). cells: (nx, nz) half-ken cells, default = the rect rounded to the 0.91 grid."""
    mt = _mats(MATS_TATAMI, mats)
    hs = norm_holes(holes)
    s = Part(name, "", "")
    rects = rect_minus((x0, x1, z0, z1), hs)
    for (a, b, c, d) in rects:
        s.add(box(a, b, base, top, c, d, {"top": mt["lod"], "default": "wood_weathered"}, vis=(2, 3), geo=True,
                  view=True, fire="wood", tag="floor_lod"))
    for (a, b, c, d) in rects:
        s.add(box(a, b, base, top - TATAMI_T, c, d, {"top": mt["base"], "default": "wood_weathered"}, vis=(1,),
                  tag="floor_base"))
    nx, nz = cells if cells else (int(round((x1 - x0) / HALF)), int(round((z1 - z0) / HALF)))
    cx, cz = (x1 - x0) / nx, (z1 - z0) / nz
    blocked = []
    for h in hs:
        hx0, hx1, hz0, hz1 = h["rect"]
        i0, i1 = round((hx0 - x0) / cx), round((hx1 - x0) / cx)
        j0, j1 = round((hz0 - z0) / cz), round((hz1 - z0) / cz)
        if max(abs(x0 + i0 * cx - hx0), abs(x0 + i1 * cx - hx1), abs(z0 + j0 * cz - hz0), abs(z0 + j1 * cz - hz1)) > 0.01:
            raise ValueError("%s: tatami hole %s is not on the half-ken mat grid" % (name, h["rect"]))
        blocked += [(i, j) for i in range(max(0, i0), min(nx, i1)) for j in range(max(0, j0), min(nz, j1))]
    for (i0, i1, j0, j1) in shugi_layout(nx, nz, blocked):
        a, b, c, d = x0 + i0 * cx + 0.002, x0 + i1 * cx - 0.002, z0 + j0 * cz + 0.002, z0 + j1 * cz - 0.002
        along_x = (i1 - i0) > (j1 - j0)
        if mt.get("fit"):
            # one texture tile per mat, u along the mat's length (the B1 tatami texture is one 1.82 x 0.91 mat)
            if along_x:
                uvk = dict(uvscale=(b - a, d - c), uvoff=(-a / (b - a), -c / (d - c)), grain="")
            else:
                uvk = dict(uvscale=(b - a, d - c), uvrot=90.0, uvoff=(d / (d - c), -a / (b - a)), grain="")
            s.add(open_box(a, b, top - TATAMI_T, top, c, d, mt["facing"], ("top", "xlo", "xhi", "zlo", "zhi"),
                           "tatami", **uvk))
        else:
            s.add(open_box(a, b, top - TATAMI_T, top, c, d, mt["facing"], ("top", "xlo", "xhi", "zlo", "zhi"),
                           "tatami", uvrot=0.0 if along_x else 90.0, uvscale=(0.9, 0.9)))
        hw = 0.03
        if along_x:
            for zz in (c, d - hw):
                s.add(open_box(a, b, top - 0.004, top + 0.001, zz, zz + hw, mt["heri"], ("top", "zlo", "zhi"),
                               "heri"))
        else:
            for xx in (a, b - hw):
                s.add(open_box(xx, xx + hw, top - 0.004, top + 0.001, c, d, mt["heri"], ("top", "xlo", "xhi"),
                               "heri"))
    for (a, b, c, d) in rects:
        s.road([(a, top, c), (b, top, c), (b, top, d), (a, top, d)], "tatami")
    _finish_holes(s, hs, top, hole_fn)
    return s


# ------------------------------------------------------------------------------------------------ boards
def boards(name, x0, x1, z0, z1, y, along_x=False, holes=(), hole_fn=None, mats=None):
    """Board floor on sleepers: a 0.15 support block (LOD 2/3 + Geometry), random-width boards 0.20-0.30 (LOD 1),
    a sooted base under them. along_x: boards run along x (else along z). Roadway 'boards' at y.
    mats: MATS_BOARDS keys. 'slab': True lays ONE top slab whose texture carries the boards (B1's jp_m_floor_boards_int
    paints ~0.26 m boards, grain along v), turned so the grain runs along the boards' direction."""
    mt = _mats(MATS_BOARDS, mats)
    hs = norm_holes(holes)
    s = Part(name, "", "")
    rects = rect_minus((x0, x1, z0, z1), hs)
    for (ra, rb, rc, rd) in rects:
        s.add(box(ra, rb, y - 0.15, y, rc, rd, mt["lod"], vis=(2, 3), geo=True, view=True, fire="wood",
                  tag="floor_lod"))
    if mt.get("slab"):
        for (ra, rb, rc, rd) in rects:
            s.add(open_box(ra, rb, y - 0.03, y, rc, rd, mt["board"], ("top", "xlo", "xhi", "zlo", "zhi"), "floor_board",
                           grain="", uvrot=90.0 if along_x else 0.0))
            s.add(box(ra, rb, y - 0.15, y - 0.03, rc, rd, mt["base"], vis=(1,), tag="floor_base"))
            s.road([(ra, y, rc), (rb, y, rc), (rb, y, rd), (ra, y, rd)], "boards")
        _finish_holes(s, hs, y, hole_fn)
        return s
    rng = rng_for(name)
    a, b = (z0, z1) if along_x else (x0, x1)
    p = a
    while p < b - 1e-4:
        q = min(b, p + rng.uniform(0.20, 0.30))
        if b - q < 0.1:
            q = b
        uvoff = (rng.random(), rng.random())
        if along_x:
            pieces = rect_minus((x0, x1, p + 0.002, q - 0.002), hs)
            for (ba, bb, bc, bd) in pieces:
                s.add(open_box(ba, bb, y - 0.03, y, bc, bd, "wood_weathered", ("top", "zlo", "zhi"), "floor_board",
                               uvoff=uvoff, uvrot=90.0))
        else:
            pieces = rect_minus((p + 0.002, q - 0.002, z0, z1), hs)
            for (ba, bb, bc, bd) in pieces:
                s.add(open_box(ba, bb, y - 0.03, y, bc, bd, "wood_weathered", ("top", "xlo", "xhi"), "floor_board",
                               uvoff=uvoff, uvrot=90.0))
        p = q
    for (ra, rb, rc, rd) in rects:
        s.add(box(ra, rb, y - 0.15, y - 0.03, rc, rd, "wood_sooted", vis=(1,), tag="floor_base"))
    for (ra, rb, rc, rd) in rects:
        s.road([(ra, y, rc), (rb, y, rc), (rb, y, rd), (ra, y, rd)], "boards")
    _finish_holes(s, hs, y, hole_fn)
    return s


# ------------------------------------------------------------------------------------------------ doma
def doma(name, x0, x1, z0, z1, road=None, y=DOMA_Y, holes=(), hole_fn=None, mats=None):
    """Earth floor (tataki): a 0.20 slab, arakabe top on a stone_cut body, in every LOD and the Geometry. road: the
    walkable rectangle (x0, x1, z0, z1) for the Roadway 'doma' (usually inset from the walls by half a post);
    default = the slab. mats: MATS_DOMA keys (B1: MATS_DOMA_T3 tataki, MATS_DOMA_EARTH)."""
    mt = _mats(MATS_DOMA, mats)
    hs = norm_holes(holes)
    s = Part(name, "", "")
    for (a, b, c, d) in rect_minus((x0, x1, z0, z1), hs):
        s.add(box(a, b, y - 0.20, y, c, d, {"top": mt["top"], "default": mt["body"]}, vis=(1, 2, 3),
                  geo=True, view=True, fire="dirt", tag="doma"))
    rx0, rx1, rz0, rz1 = road if road else (x0, x1, z0, z1)
    for (a, b, c, d) in rect_minus((rx0, rx1, rz0, rz1), hs):
        s.road([(a, y, c), (b, y, c), (b, y, d), (a, y, d)], "doma")
    _finish_holes(s, hs, y, hole_fn)
    return s


# ------------------------------------------------------------------------------------------------ shop floor
MISE_STRIP = {"_455": 0.455, "_910": 0.91}


def mise(name, x0, x1, z0, z1, top=0.50, base=DOMA_Y, variant="_455", street="+z", cell=None, mats_tatami=None,
         mats_boards=None):
    """jp_p_fit_mise_floor (research/interior/BUILD_LIST.md fitting 8): the shop room's raised floor with a board
    display strip (mise-ita) along its street edge, where goods are laid out, and tatami behind it.
      variant  '_455' narrow strip behind a lattice front (degoshi); '_910' wide strip behind an open front
      street   '+z' or '-z': the street edge of the rect
      cell     depth of one tatami cell (default: the rect depth over its half-ken count, so the mats match the other
               rooms of the house). The mats keep their standard size; whatever depth is left after the strip and the
               whole mat rows is closed with a plain board band (tatami-yose) at the back of the room, as carpenters
               filled off-module rooms.
    Returns one Part (strip + tatami + yose). part.meta['mise'] = the three plan rectangles and the row count."""
    strip = MISE_STRIP[variant]
    depth = z1 - z0
    if cell is None:
        cell = depth / max(1, int(round(depth / HALF)))
    rows = max(1, int((depth - strip) / cell + 1e-3))
    tat = rows * cell
    yose = depth - strip - tat
    if street == "+z":
        r_strip = (x0, x1, z1 - strip, z1)
        r_tat = (x0, x1, z1 - strip - tat, z1 - strip)
        r_yose = (x0, x1, z0, z0 + yose)
    else:
        r_strip = (x0, x1, z0, z0 + strip)
        r_tat = (x0, x1, z0 + strip, z0 + strip + tat)
        r_yose = (x0, x1, z1 - yose, z1)
    s = Part(name, "", "")
    nx = int(round((x1 - x0) / HALF))
    s.merge(boards(name + "_strip", *r_strip, top, along_x=True, mats=mats_boards))
    s.merge(tatami(name + "_tatami", *r_tat, top=top, base=base, mats=mats_tatami, cells=(nx, rows)))
    if yose > 0.02:
        s.merge(boards(name + "_yose", *r_yose, top, along_x=True, mats=mats_boards))
        # the board bands stand on the doma like the mats' support block (Geometry and the far LODs)
    for r in (r_strip, r_yose):
        if r[3] - r[2] > 0.02:
            s.add(box(r[0], r[1], base, top - 0.15, r[2], r[3], "wood_sooted", vis=(), geo=True, view=True,
                      fire="wood", tag="floor_support"))
    s.meta["mise"] = {"variant": variant, "strip": r_strip, "tatami": r_tat, "yose": r_yose if yose > 0.02 else None,
                      "rows": rows, "cell": cell}
    return s


# ------------------------------------------------------------------------------------------------ loft
def loft(name, x0, x1, z0, z1, ceil, top, joist_step=HALF, walkable=False, holes=(), hole_fn=None):
    """Upper (loft) floor that is also the ceiling of the rooms under it: a slab ceil..top in LOD 2/3 + Geometry, the
    boards (LOD 1, visible underside) on sao joists every joist_step along x (LOD 1). walkable: Roadway 'boards' at
    top (the machiya's loft is sealed, G0-4: False). A stairwell is a hole (kind 'stair')."""
    hs = norm_holes(holes)
    s = Part(name, "", "")
    rects = rect_minus((x0, x1, z0, z1), hs)
    for (a, b, c, d) in rects:
        s.add(box(a, b, ceil, top, c, d, "wood_weathered", vis=(2, 3), geo=True, view=True, fire="wood",
                  tag="loft_lod"))
    for (a, b, c, d) in rects:
        s.add(box(a, b, ceil + 0.08, top, c, d, {"bottom": "wood_weathered", "default": "wood_weathered"}, vis=(1,),
                  tag="loft_boards"))
    x = x0 + joist_step
    while x < x1 - 0.1:
        for (a, b, c, d) in rect_minus((x - 0.03, x + 0.03, z0, z1), hs):
            s.add(box(a, b, ceil, ceil + 0.08, c, d, "wood_weathered", vis=(1,), tag="sao_joist", grain="long"))
        x += joist_step
    if walkable:
        for (a, b, c, d) in rects:
            s.road([(a, top, c), (b, top, c), (b, top, d), (a, top, d)], "boards")
    _finish_holes(s, hs, top, hole_fn)
    return s
