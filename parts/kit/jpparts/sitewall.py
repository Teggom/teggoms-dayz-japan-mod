"""The reusable WALL KIT (agent K3, 2026-10-01; research + choices in parts/K3_NOTES.md §1-2, API in §6).

Frame of every wall part: the run along +x from 0 to L on the wall centreline z = 0, +z = the OUTSIDE (street / road)
face, y 0 = grade at the module. Module ends sit on the half-ken grid (rule 9; connectors type 'post', hidden).
Footings run 0.40 below grade, so a module sits on +-0.3 m of uneven ground without daylight (PARTS_GAP issue 9).

    wall(kind, L, ends=("seam", "seam"), **opt) -> Part        one run module
    corner pieces: ends "corner+z" / "corner-z" (the other run leaves to that local side; bodies mitre on the
        diagonal; the module whose END (x = L) is the corner builds the cap's corner cell: hip outside, valley inside)
    ends: "seam" (the next module continues), "end" (a finished free end: cap gable, closed body end),
          "post" (the end node holds a gate / door post: body stops at the post face, cap verge flush with it)
    step(kind, L, rise, **opt)                                  terrain step: the second half stands `rise` higher
    run_wall(nodes, kind, gates=..., **opt) -> Part             a whole wall along a grid polyline (corners, gates)
    gate_kabuki(span, roofed), gate_munemon(span, covering), wicket(kind)   gate pieces that sit in a run

kinds: tsuiji (finishes plaster / earth / nakanuri / suji5 / neri; caps tile / hongawara / board), dobei (shikkui /
namako / kuro; hikae posts), itabei (plain / kuro; caps none / board / tile), yotsume, kenninji, shiba, takeho,
ikegaki (low / tall), ishigaki (nozura / uchikomi; free-standing or retaining), bank (earth bank with a stone toe).
states: None, "collapsed", "tiles" (fallen cap tiles), "overgrown", "leaning", "broken".
"""
import math

from .core import Part, Solid, box, prism, hexa, cyl, stone, rings, rand_convex, KEN, HALF, QK, rng_for, Door, \
    add, sub, mul, norm, cross, dot, newell as _newell
from .shapes import board_run, rough_block, tube, half_tube, oriented_box
from . import striproof as SR
from . import walls as WL

GROUP = "site_walls"
_PW = [0.21 / 2]                 # half the post width a 'post' end stops at (set per wall() call)
FOOT = -0.40                     # footing depth below grade

# ------------------------------------------------------------------------------------------------ wall sections
TYPES = {
    #           base w, top w, body top, footing stones (h, mat), cap (family, ov, pitch), materials
    "tsuiji": dict(wb=0.90, wt=0.56, H=2.30, foot=(0.25, "stone_field"), cap=("sangawara", 0.24, 0.45)),
    "dobei": dict(wb=0.30, wt=0.30, H=2.10, foot=(0.30, "stone_cut"), cap=("sangawara", 0.26, 0.45)),
    "itabei": dict(wb=0.12, wt=0.12, H=1.80, foot=None, cap=None),
}
FINISH = {"plaster": "wall_shikkui", "earth": "wall_arakabe", "nakanuri": "wall_nakanuri", "suji5": "wall_nakanuri",
          "neri": "wall_shikkui_aged", "shikkui": "wall_shikkui", "namako": "wall_shikkui", "kuro": "wall_shikkui"}
CAP_FAM = {"tile": "sangawara", "hongawara": "hongawara", "board": "itabuki", "none": None}


def _xprism(section, e0, e1, mats, **kw):
    """A prism along x over a convex (y, z) section, each end on its own plane x = a + b y + c z (mitres, butts)."""
    n = len(section)
    v0 = [(e0[0] + e0[1] * y + e0[2] * z, y, z) for y, z in section]
    v1 = [(e1[0] + e1[1] * y + e1[2] * z, y, z) for y, z in section]
    faces = [list(range(n)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    return Solid(v0 + v1, faces, mats, **kw)


def _end_plane(end, x, idx):
    """End plane (a, b, c): x = a + b y + c z, for end kind `end` at node x (idx 0 = start, 1 = end)."""
    if end == "corner+z":
        return (x, 0.0, -1.0) if idx == 1 else (x, 0.0, 1.0)
    if end == "corner-z":
        return (x, 0.0, 1.0) if idx == 1 else (x, 0.0, -1.0)
    return (x, 0.0, 0.0)


def _xat(e, y, z):
    return e[0] + e[1] * y + e[2] * z


def _width(T, y):
    """Body width at height y (battered tsuiji; vertical walls constant)."""
    return T["wb"] - (T["wb"] - T["wt"]) * y / T["H"]


def _ends_x(T, ends, L, post=None):
    """Body end planes for both ends (posts: the body stops at the post face)."""
    post = 2 * _PW[0] if post is None else post
    e0 = _end_plane(ends[0], 0.0, 0)
    e1 = _end_plane(ends[1], L, 1)
    if ends[0] == "post":
        e0 = (post / 2, 0.0, 0.0)
    if ends[1] == "post":
        e1 = (L - post / 2, 0.0, 0.0)
    return e0, e1


def _cap(part, T, L, ends, family, y_top, finish_mat, ov=None, t=None, D=None, name="cap", wood="wood_weathered"):
    """The wall cap: a strip roof (striproof) along the run; corner cells at a corner END; gable ends at free ends and
    posts (flush verge at a post face)."""
    fam = family
    D = D if D is not None else T["wt"]
    ov = ov if ov is not None else T["cap"][1]
    t = t if t is not None else T["cap"][2]
    flush = "step" in ends
    S = SR.Spec(D, ov, y_top + 0.05, fam, t=t, gov=0.0 if flush else 0.18, body="solid", y_solid=y_top,
                walkable=False, rafter_sp=0.20, rafter_sec=(0.04, 0.05), courses=3 if fam != "hongawara" else 5,
                bed_mat=finish_mat, ridge_w=0.20 if D < 0.4 else 0.22, wood=wood, oni=not flush)
    x0, x1 = 0.0, L
    ce = []
    br = []
    for idx, end in enumerate(ends):
        if end.startswith("corner"):
            side = end[-2:]
            br.append((idx, side))
            ce.append("seam")
            if idx == 0:
                x0 = D / 2
            else:
                x1 = L - D / 2
        elif end in ("end", "step"):
            ce.append("gable")
        elif end == "post":
            ce.append("gable")
            if idx == 0:
                x0 = _PW[0] + S.gov
            else:
                x1 = L - _PW[0] - S.gov
        else:
            ce.append("seam")
    sub_ = Part(part.name + "_" + name, "", "")
    if x1 - x0 > 0.05:
        SR.straight(sub_, S, x1 - x0, tuple(ce), branches=[(i, s) for i, s in br])
        sub_ = sub_.transformed(0.0, (x0, 0.0, 0.0))
    if ends[1].startswith("corner"):
        cj = Part(part.name + "_capj", "", "")
        SR.junction(cj, S, ("-x", ends[1][-2:]))
        sub_.merge(cj.transformed(0.0, (L, 0.0, 0.0)))
    part.merge(sub_)
    return S


def _foot_stones(part, T, L, e0, e1, rng, h, mat, cut=False):
    """Individual footing stones along both faces (rule 3), each row ending at its face's end points (mitres)."""
    for s in (1.0, -1.0):
        zf = s * (_width(T, 0.0) / 2 + 0.015)
        xa, xb = _xat(e0, 0.0, s * T["wb"] / 2), _xat(e1, 0.0, s * T["wb"] / 2)
        x = xa
        while x < xb - 0.08:
            w = rng.uniform(0.32, 0.50) if not cut else rng.uniform(0.45, 0.80)
            w = min(w, xb - x)
            if xb - (x + w) < 0.15:
                w = xb - x
            if cut:
                za, zb = sorted((zf - s * 0.11, zf + s * 0.04))
                part.add(rough_block(rng, x + 0.006, x + w - 0.006, -0.10, h, za, zb, mat, chamfer=0.015, vis=(1,),
                                     tag="foot_stone"))
            else:
                part.add(face_stone(rng, x + 0.01, x + w - 0.01, -0.06, h + rng.uniform(-0.03, 0.03), zf + s * 0.03, s,
                                    0.24, mat, tag="foot_stone"))
            x += w
        # far LODs: one strip per face
        za, zb = sorted((zf - 0.10 * s, zf + 0.05 * s))
        part.add(box(xa, xb, -0.10, h * 0.9, za, zb, mat, vis=(2, 3), tag="foot_far"))


def _face_lines(part, T, e0, e1, ys, mat, proud=0.010, hgt=0.035, sides=(1.0, -1.0), tag="line", vis=(1,)):
    """Thin horizontal strips on the (battered) faces at the heights ys: a front face + a top and bottom bevel."""
    for s in sides:
        for y in ys:
            ya, yb = y - hgt / 2, y + hgt / 2
            za, zb = s * _width(T, ya) / 2, s * _width(T, yb) / 2
            pa, pb = za + s * proud, zb + s * proud
            # the section: on the face at ya and yb, proud between
            sec = [(ya, za - s * 0.002), (ya + 0.006, pa), (yb - 0.006, pb), (yb, zb - s * 0.002)]
            if s < 0:
                sec = sec[::-1]
            xa0, xb0 = _xat(e0, y, s * _width(T, y) / 2), _xat(e1, y, s * _width(T, y) / 2)
            part.add(_xprism(sec, (xa0, 0.0, 0.0), (xb0, 0.0, 0.0), mat, vis=vis, tag=tag))


def face_stone(rng, x0, x1, y0, y1, zf, s, depth, mat, jag=0.22, vis=(1,), tag="wall_stone", lean=0.0):
    """A wall stone seen on its face: an irregular convex face polygon filling the cell x0..x1 x y0..y1 at z = zf
    (s = +1: the face looks to +z), swelling slightly behind the face, then tapering to the back (convex: the scale
    profile is concave). lean: the batter (z shift per metre of height, toward -s going up)."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hh = (x1 - x0) / 2, (y1 - y0) / 2
    poly = [(cx + a * hw, cy + b * hh) for a, b in rand_convex(rng, 7, 1.0, 1.0, jag)]
    prof = [(0.0, 0.86), (0.05, 1.0), (depth, 0.78)]
    verts = []
    for dz, sc in prof:
        for px, py in poly:
            x, y = cx + (px - cx) * sc, cy + (py - cy) * sc
            verts.append((x, y, zf - s * dz - s * lean * (y - cy)))
    n = len(poly)
    faces = [list(range(n)), list(range(2 * n, 3 * n))]
    for r in range(2):
        for i in range(n):
            j = (i + 1) % n
            faces.append([r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i])
    return Solid(verts, faces, mat, vis=vis, tag=tag)


# ------------------------------------------------------------------------------------------------ earth / plaster walls
def _earth_wall(kind, L, ends, finish, cap, state, hikae, rng, P):
    T = TYPES[kind]
    fmat = FINISH[finish]
    e0, e1 = _ends_x(T, ends, L)
    H = T["H"]
    if state == "collapsed":
        return _collapsed(P, T, L, e0, e1, fmat, cap, rng, ends)
    # body: battered (tsuiji) or vertical (dobei) prism, from the footing to the wall top
    sec = [(FOOT, -_width(T, FOOT) / 2), (FOOT, _width(T, FOOT) / 2), (H, T["wt"] / 2), (H, -T["wt"] / 2)]
    if kind == "dobei":
        y0 = T["foot"][0]
        # dobei: the plastered wall stands on a cut-stone course (the course is the footing)
        P.add(_xprism([(FOOT, -0.17), (FOOT, 0.17), (y0, 0.17), (y0, -0.17)], e0, e1, T["foot"][1], vis=(), geo=True,
                      view=True, fire=True, tag="foot_core"))
        sec = [(y0, -0.15), (y0, 0.15), (H, 0.15), (H, -0.15)]
    outer = fmat
    P.add(_xprism(sec, e0, e1, {"front": outer, "back": fmat, "default": fmat}, vis=(1, 2, 3), geo=True, view=True,
                  fire="building" if kind == "tsuiji" else True, tag="wall_body"))
    fh, fm = T["foot"]
    if kind == "tsuiji":
        _foot_stones(P, T, L, e0, e1, rng, fh, fm)
    else:
        _foot_stones(P, dict(T, wb=0.34, wt=0.34, H=H), L, e0, e1, rng, fh, fm, cut=True)
    # finish details
    if finish == "earth":
        # rammed-earth lifts (hanchiku) every ~0.12 m: a slight ridge on both faces (c29)
        ys = [0.40 + 0.125 * k for k in range(int((H - 0.55) / 0.125))]
        _face_lines(P, T, e0, e1, ys, fmat, proud=0.008, hgt=0.03, tag="hanchiku")
    elif finish == "suji5":
        ys = [H - 0.32 - 0.13 * k for k in range(5)]
        _face_lines(P, T, e0, e1, ys, "wall_shikkui", proud=0.008, hgt=0.045, tag="sujibei", vis=(1, 2))
    elif finish == "neri":
        ys = [0.35 + 0.13 * k for k in range(int((H - 0.50) / 0.13))]
        _face_lines(P, T, e0, e1, ys, "roof_kawara", proud=0.016, hgt=0.024, tag="neri_course")
    elif finish == "namako":
        xa, xb = _xat(e0, 0.5, 0.15), _xat(e1, 0.5, 0.15)
        WL.namako(P, xa + 0.02, xb - 0.02, T["foot"][0] + 0.05, 1.20, 0.15, diagonal=True)
        P.add(box(xa, xb, 1.20, 1.25, 0.15, 0.172, "wall_shikkui", vis=(1, 2), tag="namako_cap"))
    elif finish == "kuro":
        xa, xb = _xat(e0, 0.5, 0.15), _xat(e1, 0.5, 0.15)
        P.extend(board_run(xa + 0.01, xb - 0.01, T["foot"][0] + 0.02, 1.15, 0.152, 0.17, rng, 0.20, 0.28, "wood_kuro",
                           vis=(1,), tag="koshi_board"))
        P.add(box(xa + 0.01, xb - 0.01, T["foot"][0] + 0.02, 1.15, 0.152, 0.17, "wood_kuro", vis=(2, 3),
                  tag="koshi_lod"))
        P.add(box(xa, xb, 1.15, 1.19, 0.15, 0.19, "wood_kuro", vis=(1, 2), tag="koshi_cap"))
    if hikae and kind == "dobei" and L >= KEN - 1e-6:
        _hikae(P, L / 2, rng)
    if state == "overgrown":
        _overgrow(P, L, T, rng)
    # cap
    fam = CAP_FAM[cap]
    if fam:
        S = _cap(P, T, L, ends, fam, H, fmat)
        if state == "tiles":
            _drop_tiles(P, L, T, rng, S)
    return P


def _hikae(P, x, rng):
    """Hikae-bashira: a buttress post 0.9 m inside the wall with two tie beams into it (GK)."""
    z = -0.15 - 0.90
    from .found import soseki
    sub_ = Part("hikae", "", "")
    soseki(sub_, x, z, int(rng.random() * 8))
    sub_.add(box(x - 0.06, x + 0.06, 0.0, 1.75, z - 0.06, z + 0.06, "wood_weathered", vis=(1, 2, 3), geo=True,
                 view=True, fire=True, tag="hikae_post"))
    for y in (0.85, 1.50):
        sub_.add(box(x - 0.03, x + 0.03, y, y + 0.10, z - 0.06, -0.152, "wood_weathered", vis=(1, 2), tag="hikae_nuki"))
    sub_.add(box(x - 0.08, x + 0.08, 1.75, 1.79, z - 0.08, z + 0.08, "wood_weathered", vis=(1,), tag="hikae_cap"))
    P.merge(sub_)


def _overgrow(P, L, T, rng):
    """Dead-world overgrowth: moss patches on both faces near the foot, weed clumps along the foot."""
    for s in (1.0, -1.0):
        for k in range(max(1, int(L / 0.9))):
            x = rng.uniform(0.2, L - 0.6)
            w, h = rng.uniform(0.4, 0.8), rng.uniform(0.3, 0.7)
            y0 = rng.uniform(0.25, 0.6)
            z = s * (_width(T, y0) / 2 + 0.006)
            quad = [(x, y0, z), (x + w, y0, z), (x + w, y0 + h, z), (x, y0 + h, z)]
            P.add(Solid(quad, [[0, 1, 2, 3]], "decal_moss", vis=(1,), normals=[(0.0, 0.0, s)], uv="fit",
                        tag="moss"))
        for k in range(max(2, int(L / 0.6))):
            x = rng.uniform(0.1, L - 0.1)
            z = s * (_width(T, 0.0) / 2 + rng.uniform(0.05, 0.20))
            r = rng.uniform(0.15, 0.30)
            P.add(_posed_ring(rng, x, z, r, "plant_foliage"))


def _posed_ring(rng, x, z, r, mat, h=None):
    h = h if h is not None else r * 1.3
    base = [(x + a, z + b) for a, b in rand_convex(rng, 6, r, r * 0.8)]
    return rings((base, [(-0.05, 0.8), (h * 0.45, 1.0), (h, 0.35)]), mat, vis=(1, 2), tag="weeds")


def _drop_tiles(P, L, T, rng, S):
    """Fallen cap tiles: holes in the R1 tile field (the clay bed shows) and broken tiles at the foot."""
    holes = []
    for k in range(max(1, int(L / 0.9))):
        x = rng.uniform(0.15, L - 0.5)
        holes.append((x, x + rng.uniform(0.25, 0.45), rng.choice((-1.0, 1.0))))
    for s_ in list(P.solids):
        if s_.tag not in ("kawara_field", "eave_tile", "hongawara", "cover"):
            continue
        keep = []
        for fi, f in enumerate(s_.faces):
            pts = [s_.verts[i] for i in f]
            cx = sum(p[0] for p in pts) / len(pts)
            cz = sum(p[2] for p in pts) / len(pts)
            if any(a <= cx <= b and cz * sd > 0.05 for a, b, sd in holes):
                continue
            keep.append(fi)
        if len(keep) == len(s_.faces):
            continue
        s_.faces = [s_.faces[i] for i in keep]
        s_.fm = [s_.fm[i] for i in keep]
        s_.fuv = [s_.fuv[i] for i in keep]
        s_.fn = [s_.fn[i] for i in keep]
        if isinstance(s_.uv, list):
            s_.uv = s_.fuv
        if s_.normals is not None:
            s_.normals = s_.fn
    P.solids = [s_ for s_ in P.solids if s_.faces]
    for a, b, sd in holes:
        for k in range(3):
            x = rng.uniform(a - 0.2, b + 0.2)
            z = sd * (T["wb"] / 2 + rng.uniform(0.15, 0.6))
            yaw = rng.uniform(0, math.pi)
            w, d = rng.uniform(0.10, 0.20), rng.uniform(0.08, 0.16)
            P.add(oriented_box((x, 0.015, z), (math.cos(yaw), 0.0, math.sin(yaw)), (0.0, 1.0, 0.0),
                               (-math.sin(yaw), 0.0, math.cos(yaw)), w / 2, 0.012, d / 2, "roof_kawara", vis=(1,),
                               tag="tile_shard"))


def _collapsed(P, T, L, e0, e1, fmat, cap, rng, ends):
    """A section fallen: two broken stubs left and right, the middle a mound of earth and rubble, cap pieces only
    over the stubs, tiles strewn at the foot."""
    H = T["H"]
    a = L * rng.uniform(0.22, 0.32)
    b = L * rng.uniform(0.68, 0.78)
    for (xa, xb, ea, eb) in ((None, a, e0, None), (b, None, None, e1)):
        x0e = ea if ea is not None else (xa, 0.0, 0.0)
        x1e = eb if eb is not None else (xb, 0.0, 0.0)
        # broken ends: the stub top drops toward the break (two prisms: full + a sloped shoulder)
        lo = 0.35 if xa is None else 0.0
        if xa is None:
            mid = xb - 0.35
            P.add(_xprism([(FOOT, -_width(T, FOOT) / 2), (FOOT, _width(T, FOOT) / 2), (H, T["wt"] / 2),
                           (H, -T["wt"] / 2)], x0e, (mid, 0.0, 0.0), fmat, vis=(1, 2, 3), geo=True, view=True,
                          fire="building", tag="wall_body"))
            pts = [(mid, FOOT), (xb, FOOT), (xb, 1.1), (mid, H)]
        else:
            mid = xa + 0.35
            P.add(_xprism([(FOOT, -_width(T, FOOT) / 2), (FOOT, _width(T, FOOT) / 2), (H, T["wt"] / 2),
                           (H, -T["wt"] / 2)], (mid, 0.0, 0.0), x1e, fmat, vis=(1, 2, 3), geo=True, view=True,
                          fire="building", tag="wall_body"))
            pts = [(xa, FOOT), (mid, FOOT), (mid, H), (xa, 1.25)]
        w = T["wt"] / 2 + 0.02 if T["wb"] == T["wt"] else _width(T, 1.0) / 2
        P.add(_shoulder(pts, w, fmat))
    # the mound
    for k in range(5):
        x = rng.uniform(a + 0.1, b - 0.1)
        r = rng.uniform(0.35, 0.55)
        P.add(rings(([(x + p, q) for p, q in rand_convex(rng, 7, r * 1.3, T["wb"] * 1.1)],
                     [(FOOT * 0.3, 1.0), (rng.uniform(0.25, 0.40), 0.80), (rng.uniform(0.45, 0.70), 0.35)]),
                    "wall_arakabe", vis=(1, 2, 3), geo=True, view=True, fire="building", tag="rubble"))
    for k in range(6):
        x = rng.uniform(a - 0.2, b + 0.2)
        z = rng.choice((-1, 1)) * (T["wb"] / 2 + rng.uniform(0.1, 0.8))
        P.add(stone(rng, x, z, rng.uniform(0.12, 0.25), rng.uniform(0.10, 0.2), 0.08, 0.06, "roof_kawara", bury=0.02,
                    n=5, vis=(1,), tag="tile_shard"))
    fam = CAP_FAM[cap]
    if fam:
        S = SR.Spec(T["wt"], T["cap"][1], H + 0.05, fam, t=T["cap"][2], gov=0.18, body="solid", y_solid=H,
                    walkable=False, rafter_sp=0.20, rafter_sec=(0.04, 0.05), bed_mat=fmat, ridge_w=0.22, oni=False)
        for xs, xe, ce in ((0.0, a - 0.35, (("gable" if ends[0] == "end" else "seam"), "seam")),
                           (b + 0.35, L, ("seam", ("gable" if ends[1] == "end" else "seam")))):
            if xe - xs < 0.2:
                continue
            c = Part(P.name + "_capc", "", "")
            SR.straight(c, S, xe - xs, ce)
            P.merge(c.transformed(0.0, (xs, 0.0, 0.0)))
    return P


def _shoulder(pts, w, fmat):
    return prism(pts, "z", -w, w, fmat, vis=(1, 2, 3), geo=True, view=True, fire="building", tag="wall_broken")


# ------------------------------------------------------------------------------------------------ board fence
def _itabei(L, ends, kuro, cap, state, rng, P):
    m = "wood_kuro" if kuro else "wood_weathered"
    H = 1.80
    from .found import soseki
    posts = _post_nodes(L, ends)
    lean = 0.0
    for x in posts:
        P.add(box(x - 0.06, x + 0.06, FOOT, H + 0.04, -0.06, 0.06, m, vis=(1, 2, 3), geo=True, view=True, fire=True,
                  tag="fence_post", grain="long"))
    xa = 0.06 if ends[0] in ("seam", "end") else (_PW[0] if ends[0] == "post" else 0.06)
    xa = 0.0 if ends[0] == "seam" else xa
    xb = L if ends[1] == "seam" else L - (_PW[0] if ends[1] == "post" else 0.06)
    if ends[0].startswith("corner"):
        xa = 0.06
    if ends[1].startswith("corner"):
        xb = L + 0.06
    # rails (nuki) through the posts, behind the boards
    for y in (0.30, 1.00, 1.62):
        P.add(box(xa if ends[0] != "seam" else 0.0, xb if ends[1] != "seam" else L, y, y + 0.09, -0.045, 0.06, m,
                  vis=(1, 2), tag="fence_nuki"))
    # boards on the outside face, battens (oshibuchi) over the joints every ~0.45
    z0, z1 = 0.06, 0.08
    bx0, bx1 = (xa if ends[0] != "seam" else 0.0), (xb if ends[1] != "seam" else L)
    boards = board_run(bx0, bx1, 0.04, H, z0, z1, rng, 0.22, 0.30, m, vis=(1,), tag="fence_board")
    if state == "broken":
        boards = [b for b in boards if rng.random() > 0.3]
    P.extend(boards)
    P.add(box(bx0, bx1, 0.04, H, z0, z1, m, vis=(2, 3), tag="fence_board_lod"))
    k = 0
    x = bx0 + 0.22
    while x < bx1 - 0.15:
        P.add(box(x - 0.025, x + 0.025, 0.06, H - 0.02, z1, z1 + 0.018, m, vis=(1,), tag="oshibuchi"))
        x += 0.45
    if state != "broken":
        P.add(box(bx0, bx1, -0.30, H, -0.045, z1, m, vis=(), geo=True, view=True, fire=True, tag="fence_geo"))
    else:
        P.add(box(bx0, bx1, -0.30, H, -0.045, z1, m, vis=(), geo=True, view=False, fire=None, tag="fence_geo"))
    if cap in (None, "none"):
        # kasagi: the cap board over boards and posts
        P.add(box(bx0 - (0.02 if ends[0] == "end" else 0.0), bx1 + (0.02 if ends[1] == "end" else 0.0), H + 0.04,
                  H + 0.09, -0.08, 0.10, m, vis=(1, 2, 3), tag="kasagi"))
    else:
        T = dict(TYPES["itabei"], H=H + 0.04)
        _cap(P, T, L, ends, CAP_FAM[cap], H + 0.04, m, ov=0.20, t=0.42, D=0.16, wood=m)
    if state == "leaning":
        _lean(P, rng.uniform(5.0, 9.0))
    return P


def _post_nodes(L, ends):
    xs = []
    if ends[0] not in ("corner+z", "corner-z", "post"):
        xs.append(0.0)
    if ends[1] in ("end", "corner+z", "corner-z"):
        xs.append(L)
    return xs


def _lean(P, deg):
    """The whole panel out of plumb toward the outside (+z), turning about the foot line (y 0)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    for sd in P.solids:
        sd.verts = [(v[0], v[1] * c - v[2] * s if v[1] > 0 else v[1], v[2] * c + v[1] * s if v[1] > 0 else v[2])
                    for v in sd.verts]
        sd.center = tuple(sum(v[k] for v in sd.verts) / len(sd.verts) for k in range(3))
        sd.fm = None
        sd.finalize()


# ------------------------------------------------------------------------------------------------ palisade (W3D)
SAKU_H = 2.40                    # W3D: the palisade's log tops (before the points)
SAKU_PITCH = 0.22                # log centres
SAKU_R = 0.08                    # log radius (~0.16 across: 6 cm gaps between logs)


def _saku(L, ends, state, rng, P):
    """W3D (2026-10-02, spikes/W3D/W3D_NOTES.md site 1): the wooden palisade (saku) of checkpoints and military posts
    (KEEP_CIVIC walls: 'sharpened timber fence'; Hakone's palisade round the whole checkpoint): round logs set close in
    the ground (footing -0.40), tops cut to a point, two rails (nuki) on the inside face (-z)."""
    H = SAKU_H
    m = "wood_weathered"
    xa = 0.0 if ends[0] == "seam" else (_PW[0] if ends[0] == "post" else SAKU_R + 0.01)
    xb = L if ends[1] == "seam" else L - (_PW[0] if ends[1] == "post" else SAKU_R + 0.01)
    if ends[0].startswith("corner"):
        xa = SAKU_R + 0.01
    if ends[1].startswith("corner"):
        xb = L + SAKU_R + 0.01          # the corner log belongs to the module that ends there
    n = max(1, int(round((xb - xa) / SAKU_PITCH)))
    for k in range(n):
        x = xa + (k + 0.5) * (xb - xa) / n
        if state == "broken" and rng.random() < 0.25:
            continue
        r = SAKU_R * rng.uniform(0.88, 1.06)
        top = H + rng.uniform(-0.03, 0.03)
        base = [(x + r * math.cos(2 * math.pi * (i + 0.25) / 6), r * math.sin(2 * math.pi * (i + 0.25) / 6))
                for i in range(6)]
        P.add(rings((base, [(FOOT, 1.0), (top, 1.0), (top + 0.20, 0.04)]), m, vis=(1,), tag="saku_log",
                    grain="long"))
    # far LODs: the run as one slab with a ridge where the points are (Resolution 2) / the slab alone (Resolution 3)
    P.add(box(xa, xb, 0.0, H, -SAKU_R, SAKU_R, m, vis=(2, 3), tag="saku_lod", uv="fit"))
    P.add(prism([(H, -SAKU_R), (H, SAKU_R), (H + 0.20, 0.0)], "x", xa, xb, m, vis=(2, 3), tag="saku_lod_top"))
    for y in (0.55, 1.85):
        P.add(box(xa if ends[0] != "seam" else 0.0, xb if ends[1] != "seam" else L, y, y + 0.10,
                  -SAKU_R - 0.07, -SAKU_R + 0.005, m, vis=(1, 2), tag="saku_nuki"))
    blocked = state != "broken"
    P.add(box(xa, xb, -0.30, H, -SAKU_R, SAKU_R, m, vis=(), geo=True, view=blocked, fire=True if blocked else None,
              tag="fence_geo"))
    if state == "leaning":
        _lean(P, rng.uniform(4.0, 8.0))
    return P


# ------------------------------------------------------------------------------------------------ bamboo fences
def _yotsume(L, ends, state, rng, P):
    H = 1.05
    m = "bamboo_weathered"
    for x in _post_nodes(L, ends):
        P.add(cyl("y", x, 0.0, 0.045, FOOT, H + 0.08, "wood_weathered", n=8, vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag="fence_post"))
        P.add(cyl("y", x, 0.0, 0.05, H + 0.06, H + 0.10, "wood_weathered", n=8, vis=(1,), tag="post_cap"))
    xa = 0.0 if ends[0] == "seam" else (_PW[0] if ends[0] == "post" else 0.045)
    xb = L if ends[1] == "seam" else L - (_PW[0] if ends[1] == "post" else 0.045)
    if ends[1].startswith("corner"):
        xb = L - 0.045
    # horizontal rails (dobuchi) on the outer face
    for y in (0.28, 0.62, 0.96):
        P.add(cyl("x", y, 0.06, 0.018, xa, xb, m, n=6, vis=(1, 2), tag="dobuchi"))
    # vertical culms (tateko) every 0.30, alternating front / back of the rails
    n = max(1, int(round((xb - xa) / 0.30)))
    for k in range(n):
        x = xa + (k + 0.5) * (xb - xa) / n
        if state == "broken" and rng.random() < 0.35:
            continue
        z = 0.025 if k % 2 else 0.095
        top = H + rng.uniform(-0.02, 0.02)
        P.add(cyl("y", x, z, 0.016, 0.0, top, m, n=6, vis=(1, 2) if k % 2 == 0 else (1,), tag="tateko"))
    # palm-rope ties where the rails cross the posts (straw rope stands in for black shuro rope)
    for x in _post_nodes(L, ends):
        for y in (0.28, 0.62, 0.96):
            P.add(box(x - 0.05, x + 0.05, y - 0.025, y + 0.025, 0.035, 0.085, "straw_rope", vis=(1,), tag="tie"))
    # collision: one Geometry slab (blocks walking); see-through: no View, Fire only the posts
    P.add(box(xa, xb, -0.30, H, 0.0, 0.11, m, vis=(), geo=True, view=False, fire=None, tag="fence_geo"))
    if state == "leaning":
        _lean(P, rng.uniform(6.0, 12.0))
    return P


def _kenninji(L, ends, state, rng, P):
    H = 1.80
    m = "bamboo_weathered"
    for x in _post_nodes(L, ends):
        P.add(cyl("y", x, 0.0, 0.055, FOOT, H + 0.05, "wood_weathered", n=8, vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag="fence_post"))
    xa = 0.0 if ends[0] == "seam" else (_PW[0] if ends[0] == "post" else 0.055)
    xb = L if ends[1] == "seam" else L - (_PW[0] if ends[1] == "post" else 0.055)
    if ends[1].startswith("corner"):
        xb = L - 0.055
    # the backing (split-bamboo screen as one panel) + close-set split culms in front (R1)
    P.add(box(xa, xb, -0.25, H, -0.015, 0.015, m, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="kenninji_panel",
              uvscale=(0.5, 2.0)))
    gaps = set()
    if state == "broken":
        gaps = {k for k in range(200) if rng.random() < 0.18}
    k = 0
    x = xa + 0.01
    while x < xb - 0.05:
        if k not in gaps:
            for s in (1.0, -1.0):
                P.add(box(x + 0.004, x + 0.052, 0.03, H - 0.012, min(s * 0.015, s * 0.026), max(s * 0.015, s * 0.026), m,
                          vis=(1,), tag="waridake", uvoff=(rng.random(), rng.random())))
        k += 1
        x += 0.056
    # battens (oshibuchi): split-bamboo pairs both faces at 4 heights, rope ties; the top cap (tamabuchi)
    for y in (0.35, 0.80, 1.25, 1.62):
        for s in (1.0, -1.0):
            P.add(box(xa, xb, y - 0.022, y + 0.022, min(s * 0.026, s * 0.046), max(s * 0.026, s * 0.046), m,
                           vis=(1, 2), tag="oshibuchi"))
        for x in [xa + 0.15 + j * 0.6 for j in range(int((xb - xa) / 0.6) + 1) if xa + 0.15 + j * 0.6 < xb - 0.05]:
            P.add(box(x - 0.02, x + 0.02, y - 0.035, y + 0.035, -0.052, 0.052, "straw_rope", vis=(1,), tag="tie"))
    P.add(box(xa - 0.01, xb + 0.01, H, H + 0.05, -0.05, 0.05, m, vis=(1, 2, 3), tag="tamabuchi"))
    if state == "leaning":
        _lean(P, rng.uniform(4.0, 8.0))
    return P


def _brush(L, ends, kind, state, rng, P):
    """shiba-gaki (brushwood) / takeho-gaki (bamboo-branch bundles) between posts and split-bamboo battens."""
    H = 1.50 if kind == "shiba" else 1.80
    m = "wood_firewood" if kind == "shiba" else "bamboo_weathered"
    for x in _post_nodes(L, ends):
        P.add(cyl("y", x, 0.0, 0.05, FOOT, H + 0.05, "wood_weathered", n=8, vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag="fence_post"))
    xa = 0.0 if ends[0] == "seam" else (_PW[0] if ends[0] == "post" else 0.05)
    xb = L if ends[1] == "seam" else L - (_PW[0] if ends[1] == "post" else 0.05)
    if ends[1].startswith("corner"):
        xb = L - 0.05
    x = xa
    while x < xb - 0.04:
        w = min(rng.uniform(0.10, 0.16), xb - x)
        if not (state == "broken" and rng.random() < 0.25):
            top = H + rng.uniform(-0.10, 0.08)
            base = [(x + w / 2 + p, q) for p, q in rand_convex(rng, 5, w / 2, 0.07, 0.2)]
            P.add(rings((base, [(0.0, 0.85), (top * 0.5, 1.0), (top, 0.7)]), m, vis=(1,), tag="brush"))
        x += w
    P.add(box(xa, xb, -0.25, H, -0.06, 0.06, m, vis=(2, 3), tag="brush_lod"))
    for y in (0.35, 0.85, 1.30 if kind == "shiba" else 1.55):
        for s in (1.0, -1.0):
            P.add(box(xa, xb, y - 0.02, y + 0.02, min(s * 0.075, s * 0.095), max(s * 0.075, s * 0.095),
                      "bamboo_weathered", vis=(1, 2), tag="oshibuchi"))
    P.add(box(xa, xb, -0.30, H, -0.07, 0.07, m, vis=(), geo=True, view=True, fire=None, tag="fence_geo"))
    if state == "leaning":
        _lean(P, rng.uniform(5.0, 10.0))
    return P


# ------------------------------------------------------------------------------------------------ hedge
# FX5 (2026-10-02, Stephen's 3a walk: "I can see each segment, the bulges are bad"). The hedge is ONE continuous clipped
# form along the whole run: a battered section with rounded top edges swept along the module, its surface moved in and
# out by smooth noise of the RUN coordinate (s = distance along the whole wall path, passed in by run_wall /
# dwelling._wall_path as run=(s0, seed)), so modules join with no seam, no restart of the bulges and continuous UVs
# (u = s / tile, v = arc length round the section). Smooth per-vertex normals. Opaque leaf material jp_m_plant_hedge on
# the body; a leafy fringe of two-sided alpha cards (jp_m_plant_hedge_fringe, sprig cells) breaks the silhouette along the
# top edges and the upper faces. The noise fades to zero at corners (mitred like the wall bodies), at gate posts and at
# free ends, so neighbouring pieces meet exactly. Geometry / View: a mitred box core (blocks walking and seeing; the
# compound template makes it Fire Geometry too).
HEDGE_TILE = 0.5                     # jp_m_plant_hedge tile (m)


def _h32(i, j, seed):
    n = (i * 374761393 + j * 668265263 + seed * 1442695041) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 32767.5 - 1.0


def _vnoise(s, t, seed):
    i, j = math.floor(s), math.floor(t)
    fs, ft = s - i, t - j
    u, v = fs * fs * (3 - 2 * fs), ft * ft * (3 - 2 * ft)
    a, b = _h32(i, j, seed), _h32(i + 1, j, seed)
    c, d = _h32(i, j + 1, seed), _h32(i + 1, j + 1, seed)
    return (a + (b - a) * u) + ((c + (d - c) * u) - (a + (b - a) * u)) * v


def _hedge_noise(s, t, seed):
    """Smooth surface noise of the run coordinate s and the section arc t (about -1..1): broad, soft swells."""
    return 0.68 * _vnoise(s / 1.45, t / 0.85, seed) + 0.32 * _vnoise(s / 0.70, t / 0.45, seed + 7)


def _hedge_section(H, W, R, step=0.48):
    """The clean clipped section, from the buried foot of the +z face, up, over the rounded top, down the -z face:
    [(y, z, ny, nz)] (outward unit normals) and the arc length t of every point."""
    Wb, Wt = W, W - 0.10                       # a slight batter: clipped hedges are trimmed narrower at the top
    zf = lambda y: Wb / 2 - (Wb - Wt) / 2 * max(0.0, y) / H        # noqa: E731
    bat = math.atan2((Wb - Wt) / 2, H)
    side = []
    n = max(1, int(math.ceil((H - R) / step)))
    ys = [-0.30] + [(H - R) * k / n for k in range(1, n + 1)]
    for y in ys:
        side.append((y, zf(max(y, 0.0)), math.sin(bat), math.cos(bat)))
    yc, zc = H - R, zf(H - R) - R
    for k in (1, 2):
        a = math.radians(45.0 * k)
        side.append((yc + R * math.sin(a), zc + R * math.cos(a), math.sin(a), math.cos(a)))
    top = [(H, zc * 0.5, 1.0, 0.0), (H, 0.0, 1.0, 0.0)]
    pts = side + top
    mirror = [(y, -z, ny, -nz) for (y, z, ny, nz) in reversed(side + top[:1])]
    pts = pts + mirror
    t, arc = [0.0], 0.0
    for a_, b_ in zip(pts, pts[1:]):
        arc += math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        t.append(arc)
    return pts, t


def _end_x(end, x_node, idx, z):
    """x of the hedge body at a module end for a section point at z (corners: the wall kit's mitre plane)."""
    if end.startswith("corner"):
        e = _end_plane(end, x_node, idx)
        return e[0] + e[2] * z
    if end == "seam":
        return x_node
    if end == "post":
        return x_node + (_PW[0] - 0.01 if idx == 0 else -(_PW[0] - 0.01))    # 1 cm into the gate post: no slit
    return x_node + (0.05 if idx == 0 else -0.05)


def _smooth01(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _hedge(L, ends, size, state, rng, P, run=None):
    s0, seed = run if run else (0.0, int(rng.random() * 1e6))
    H, W = (1.40, 0.70) if size == "low" else (2.00, 0.90)
    over = state == "overgrown"
    if over:
        H, W = H + 0.45, W + 0.35
    R = 0.16 if size == "low" else 0.20
    R = R + (0.12 if over else 0.0)
    amp = 0.045 if not over else 0.090          # metres: a well-kept clipped face is nearly flat
    m = "plant_hedge"
    sec, tt = _hedge_section(H, W, R)
    ns = len(sec)
    nx = max(2, int(math.ceil(L / 0.40))) + 1   # stations along the module, every <= 0.40 m
    fade_len = 0.40

    def fade_x(x):
        f = 1.0
        if ends[0] != "seam":
            f = min(f, _smooth01(x / fade_len))
        if ends[1] != "seam":
            f = min(f, _smooth01((L - x) / fade_len))
        return f

    grid = []
    for k in range(nx):
        f = k / (nx - 1)
        row = []
        for (y, z, ny, nz), t in zip(sec, tt):
            xa_ = _end_x(ends[0], 0.0, 0, z)
            xb_ = _end_x(ends[1], L, 1, z)
            x = xa_ + (xb_ - xa_) * f
            xc = min(max(x, 0.0), L)
            fy = _smooth01((y - 0.02) / 0.30)
            d = amp * _hedge_noise(s0 + xc, t, seed) * fade_x(xc) * fy
            if ny > 0.9:                         # the clipped top: a slow rise and fall along the run too
                d += 0.6 * amp * _vnoise((s0 + xc) / 3.2, 0.5, seed + 29) * fade_x(xc)
            row.append(((x, y + ny * d, z + nz * d), (s0 + x) / HEDGE_TILE, t / HEDGE_TILE))
        grid.append(row)
    verts, faces, uvs, fns = [], [], [], []
    idx = {}
    for k in range(nx):
        for i in range(ns):
            idx[(k, i)] = len(verts)
            verts.append(grid[k][i][0])
    for k in range(nx - 1):
        for i in range(ns - 1):
            q = [(k, i), (k + 1, i), (k + 1, i + 1), (k, i + 1)]
            faces.append([idx[a] for a in q])
            uvs.append([(grid[a][b][1], grid[a][b][2]) for a, b in q])
            pts = [grid[a][b][0] for a, b in q]
            n = norm(_newell(pts))
            want = (0.0, sec[i][2] + sec[i + 1][2], sec[i][3] + sec[i + 1][3])
            if dot(n, want) < 0:
                n = mul(n, -1.0)
            fns.append(n)
    acc = {}                                     # smooth normals: the mean of the faces round each grid point
    for f_, n in zip(faces, fns):
        for vi in f_:
            a = acc.get(vi, (0.0, 0.0, 0.0))
            acc[vi] = (a[0] + n[0], a[1] + n[1], a[2] + n[2])
    body = Solid(verts, faces, m, vis=(1,), normals=fns, uv=uvs, tag="hedge_body")
    body.vn = [[norm(acc[vi]) for vi in f_] for f_ in faces]
    P.add(body)
    # end caps at free ends and gate posts (the noise is faded out there: the clean convex section)
    for idx_end, k in ((0, 0), (1, nx - 1)):
        if ends[idx_end] in ("end", "post"):
            pts = [grid[k][i][0] for i in range(ns)]
            capuv = [(p[2] / HEDGE_TILE, -p[1] / HEDGE_TILE) for p in pts]
            P.add(Solid(pts, [list(range(ns))], m, vis=(1,), normals=[(-1.0 if idx_end == 0 else 1.0, 0.0, 0.0)],
                        uv=[capuv], tag="hedge_cap"))
    # far LODs: the clean section (every other point) at the module ends only, capped where res 1 is capped
    coarse = [j for j in range(ns) if j % 2 == 0 or j == ns - 1]
    nc = len(coarse)
    cv = []
    for f in (0.0, 1.0):
        for j in coarse:
            y, z, ny, nz = sec[j]
            xa_ = _end_x(ends[0], 0.0, 0, z)
            xb_ = _end_x(ends[1], L, 1, z)
            cv.append((xa_ + (xb_ - xa_) * f, y, z))
    cf, cn, cu = [], [], []
    for i in range(nc - 1):
        q = [i, nc + i, nc + i + 1, i + 1]
        cf.append(q)
        a_, b_ = sec[coarse[i]], sec[coarse[i + 1]]
        cn.append(norm((0.0, a_[2] + b_[2], a_[3] + b_[3])))
        cu.append([((s0 + cv[v][0]) / HEDGE_TILE, tt[coarse[v % nc]] / HEDGE_TILE) for v in q])
    P.add(Solid(cv, cf, m, vis=(2, 3), normals=cn, uv=cu, tag="hedge_lod"))
    for idx_end in (0, 1):
        if ends[idx_end] in ("end", "post"):
            pts = cv[idx_end * nc:(idx_end + 1) * nc]
            P.add(Solid(pts, [list(range(nc))], m, vis=(2, 3), normals=[(-1.0 if idx_end == 0 else 1.0, 0.0, 0.0)],
                        uv=[[(p[2] / HEDGE_TILE, -p[1] / HEDGE_TILE) for p in pts]], tag="hedge_lod"))
    # the core (Geometry + View; the compound template adds Fire): mitred like the body, inside the clean faces
    cw = W / 2 - 0.06
    csec = [(-0.30, -cw), (-0.30, cw), (H - 0.08, cw - 0.05), (H - 0.08, -cw + 0.05)]

    def plane(end, idx_end, x_node):
        if end.startswith("corner"):
            return _end_plane(end, x_node, idx_end)
        return (_end_x(end, x_node, idx_end, 0.0) + (0.005 if idx_end == 0 else -0.005), 0.0, 0.0)
    P.add(_xprism(csec, plane(ends[0], 0, 0.0), plane(ends[1], 1, L), m, vis=(), geo=True, view=True, fire=None,
                  tag="hedge_core"))
    _hedge_fringe(P, L, ends, H, sec, tt, amp, s0, seed, over, fade_x)
    if over:
        for k in range(max(2, int(L / 0.32))):
            x = rng.uniform(0.1, L - 0.1)
            P.add(tube((x, H - 0.1, rng.uniform(-0.2, 0.2)), (x + rng.uniform(-0.2, 0.2), H + rng.uniform(0.4, 0.8),
                                                              rng.uniform(-0.4, 0.4)), 0.04, "plant_hedge", n=5,
                       vis=(1,), tag="shoot"))
    return P


def _hedge_fringe(P, L, ends, H, sec, tt, amp, s0, seed, over, fade_x):
    """Two-sided leaf-sprig cards (jp_m_plant_hedge_fringe, one 2 x 2 atlas cell each) along the two top edges, a few on the top and
    on the upper faces: bases sunk in the body, tips standing 0.10-0.18 m proud, so the silhouette is leafy instead of
    a ruled line. Placed by the run coordinate (no restart per module)."""
    fm = "plant_hedge_fringe"
    step = 0.16 if not over else 0.13
    k0 = int(math.ceil(s0 / step))
    k1 = int(math.floor((s0 + L) / step))
    anchors = []
    for j, (y, z, ny, nz) in enumerate(sec):
        if 0.40 < ny < 0.95:
            anchors.append((j, 0.92))                     # rounded top edge
        elif ny > 0.95 and abs(z) < 0.01:
            anchors.append((j, 0.35))                     # top middle
        elif over and ny < 0.2 and 0.25 < y < H - 0.05:
            anchors.append((j, 0.35))                     # untrimmed: sprigs all over the faces
    for kk in range(k0, k1 + 1):
        x = kk * step - s0
        for (j, prob) in anchors:
            if _h32(kk, j * 31 + 5, seed + 101) * 0.5 + 0.5 > prob:
                continue
            xs = x + 0.4 * step * _h32(kk, j, seed + 103)
            if xs < 0.06 or xs > L - 0.06 or fade_x(xs) < 0.35:
                continue                                  # corners / posts / free ends stay clean
            y, z, ny, nz = sec[j]
            d = amp * _hedge_noise(s0 + xs, tt[j], seed)
            c = (xs, y + ny * d, z + nz * d)
            up = norm((0.0, (0.55 * ny + 0.45) if ny < 0.9 else 1.0, 0.75 * nz))
            ang = math.radians(40.0 * _h32(kk, j, seed + 107))
            r0 = norm(sub((1.0, 0.0, 0.0), mul(up, up[0])))
            right = norm(add(mul(r0, math.cos(ang)), mul(cross(up, r0), math.sin(ang))))
            w = (0.36 if not over else 0.46) * (0.85 + 0.15 * (_h32(kk, j, seed + 109) + 1.0))
            hh = (0.32 if not over else 0.42) * (0.85 + 0.15 * (_h32(kk, j, seed + 111) + 1.0))
            base = sub(c, mul(up, 0.11))
            p0 = sub(base, mul(right, w / 2))
            p1 = add(base, mul(right, w / 2))
            p2 = add(p1, mul(up, hh))
            p3 = add(p0, mul(up, hh))
            cell = int((_h32(kk, j, seed + 113) * 0.5 + 0.5) * 3.999)        # one sprig cell of the 2 x 2 atlas
            u0, v0 = 0.5 * (cell % 2), 0.5 * (cell // 2)
            if _h32(kk, j, seed + 117) > 0.0:                                 # mirrored half the time
                uv = [(u0 + 0.5, v0 + 0.5), (u0, v0 + 0.5), (u0, v0), (u0 + 0.5, v0)]
            else:
                uv = [(u0, v0 + 0.5), (u0 + 0.5, v0 + 0.5), (u0 + 0.5, v0), (u0, v0)]
            quad = [p0, p1, p2, p3]
            n = norm(_newell(quad))
            for q, nn, uu in ((quad, n, uv), (quad[::-1], mul(n, -1.0), uv[::-1])):
                P.add(Solid(q, [[0, 1, 2, 3]], fm, vis=(1,), normals=[nn], uv=[uu], tag="hedge_fringe"))


# ------------------------------------------------------------------------------------------------ stone walls, banks
def _ishigaki(L, ends, kind, H, retaining, state, rng, P):
    """nozura (rough natural stones) / uchikomi (knocked faces, packed joints): free-standing low wall (both faces
    battered) or a retaining revetment (outer face battered, earth fill behind at the top level)."""
    bat = 0.27                      # batter: horizontal per vertical (~75 deg)
    T_top = 0.45 if not retaining else 0.0
    zb0 = 0.30 + bat * H            # outer foot z (centreline 0 at the top outer edge for retaining)
    mat = "stone_field" if kind == "nozura" else "stone_cut"
    xa = 0.0 if ends[0] == "seam" else 0.05
    xb = L if ends[1] == "seam" else L - 0.05
    # core (collision): free = trapezoid; retaining = the wedge + the fill behind
    sb = 0.10                       # the core stands this far behind the face stones (the joints read dark)
    if retaining:
        sec = [(FOOT, -0.9), (FOOT, bat * (H - FOOT) - sb), (H - 0.02, -sb), (H - 0.02, -0.9)]
    else:
        sec = [(FOOT, -(T_top / 2 + bat * (H - FOOT)) + sb), (FOOT, T_top / 2 + bat * (H - FOOT) - sb),
               (H - 0.02, T_top / 2 - sb), (H - 0.02, -T_top / 2 + sb)]
    P.add(_xprism(sec, (xa, 0.0, 0.0), (xb, 0.0, 0.0), {"default": "stone_field", "top": "ground_earth_bare"},
                  vis=(1, 2, 3), geo=True, view=True, fire="stone", tag="stone_core", uvscale=(0.6, 0.6)))
    faces = [1.0] if retaining else [1.0, -1.0]
    courses = max(2, int(round(H / (0.30 if kind == "nozura" else 0.34))))
    for s in faces:
        for c in range(courses):
            y0 = -0.08 + c * (H + 0.08) / courses
            y1 = -0.08 + (c + 1) * (H + 0.08) / courses
            if state == "collapsed" and c >= courses - 2:
                continue
            ym = (y0 + y1) / 2
            zf = (bat * (H - ym) + (T_top / 2 if not retaining else 0.0)) * s
            x = xa + (rng.uniform(0, 0.2) if c % 2 else 0.0)
            while x < xb - 0.08:
                w = min(rng.uniform(0.28, 0.48) if kind == "nozura" else rng.uniform(0.35, 0.60), xb - x)
                if xb - (x + w) < 0.14:
                    w = xb - x
                h = (y1 - y0) * rng.uniform(0.92, 1.05)
                if kind == "nozura":
                    P.add(face_stone(rng, x + 0.01, x + w - 0.01, y0 + 0.01, y0 + h, zf + s * 0.02, s, 0.34, mat,
                                     jag=0.30, lean=bat))
                else:
                    z_out = zf + s * 0.02
                    blk = rough_block(rng, x + 0.008, x + w - 0.008, y0 + 0.01, y1 - 0.01,
                                      min(z_out, z_out - s * 0.30), max(z_out, z_out - s * 0.30), mat, chamfer=0.03,
                                      vis=(1,), tag="wall_stone")
                    blk.verts = [(v[0], v[1], v[2] - s * bat * (v[1] - ym)) for v in blk.verts]
                    blk.center = tuple(sum(v[k] for v in blk.verts) / len(blk.verts) for k in range(3))
                    P.add(blk)
                    if rng.random() < 0.5:
                        P.add(stone(rng, x + w, zf + s * 0.005, 0.10, 0.08, 0.08, y0 + rng.uniform(0.08, 0.2),
                                    "stone_field", bury=0.0, n=5, vis=(1,), tag="packer"))
                x += w
    if retaining:
        # the fill's top behind the coping stones (the terrain carries on at y = H behind it)
        P.add(box(xa, xb, H - 0.10, H + 0.02, -0.9, -0.25, "ground_earth_bare", vis=(1, 2, 3), tag="fill_top"))
    if state == "collapsed":
        for k in range(int(L * 3)):
            x = rng.uniform(xa, xb)
            z = rng.uniform(0.2, 1.2) + zb0 * 0.5
            P.add(stone(rng, x, z, rng.uniform(0.2, 0.4), rng.uniform(0.2, 0.35), 0.22, 0.12, mat, bury=0.05, n=6,
                        vis=(1, 2), tag="fallen_stone"))
    return P


def _bank(L, ends, state, rng, P):
    """Earth bank (dote) 1.2 m high, 2.6 m base, 0.8 m top, with a nozura stone toe on the outer face."""
    H = 1.20
    xa, xb = 0.0, L
    sec = [(FOOT, -1.40), (FOOT, 1.40), (0.0, 1.30), (0.50, 1.05), (H, 0.40), (H, -0.40), (0.0, -1.30)]
    P.add(_xprism(sec, (xa, 0.0, 0.0), (xb, 0.0, 0.0), {"top": "ground_earth_bare", "default": "ground_earth_bare"},
                  vis=(1, 2, 3), geo=True, view=True, fire="ground", tag="bank_body", uvscale=(2.0, 2.0)))
    P.road([(xa, H, -0.40), (xb, H, -0.40), (xb, H, 0.40), (xa, H, 0.40)], "dirt_ext")
    x = xa
    while x < xb - 0.08:
        w = min(rng.uniform(0.30, 0.45), xb - x)
        if xb - (x + w) < 0.14:
            w = xb - x
        P.add(face_stone(rng, x + 0.005, x + w - 0.005, -0.05, 0.48 + rng.uniform(-0.04, 0.03), 1.33, 1.0, 0.30,
                         "stone_field", jag=0.12, tag="toe_stone", lean=0.25))
        x += w
    P.add(box(xa, xb, 0.0, 0.45, 1.10, 1.36, "stone_field", vis=(2, 3), tag="toe_far"))
    for k in range(max(2, int(L / 0.8))):
        x = rng.uniform(0.1, L - 0.7)
        y = rng.uniform(0.55, 0.85)
        quad = [(x, y, 1.05 - (y - 0.5) * 0.93 + 0.01), (x + 0.6, y, 1.05 - (y - 0.5) * 0.93 + 0.01),
                (x + 0.6, y + 0.3, 1.05 - (y - 0.2) * 0.93 + 0.01 - 0.28), (x, y + 0.3, 1.05 - (y - 0.2) * 0.93 + 0.01 - 0.28)]
        n_ = norm((0.0, 0.65, 0.70))
        P.add(Solid(quad, [[0, 1, 2, 3]], "decal_moss", vis=(1,), normals=[n_], uv="fit", tag="moss"))
    return P


# ------------------------------------------------------------------------------------------------ the module API
def wall(kind, L=KEN, ends=("seam", "seam"), finish=None, cap=None, state=None, hikae=False, size="low", stone="nozura",
         H=None, retaining=False, kuro=False, seed=0, pid=None, variant="", post_w=0.21, run=None):
    """One wall module (see the module docstring). Returns a Part with connectors 'post' (hidden) at both end nodes.
    run=(s0, seed): the module's start along the whole wall path and the path's seed (FX5: the hedge's surface noise,
    fringe and UVs follow the run, so a run is continuous across modules); None for a single module."""
    pid = pid or "jp_p_wall_site_" + kind
    P = Part(pid, variant, GROUP, tiers=[1, 2, 3], used_for="site wall module: " + kind,
             datum="run along +x 0..L on the wall centreline z 0, +z the outside face, y 0 = grade; footing to -0.40",
             recipe="sitewall.wall(%r, L=%.3f, ends=%r, finish=%r, cap=%r, state=%r)" % (kind, L, ends, finish, cap,
                                                                                            state))
    rng = rng_for(pid + variant + kind + str(seed))
    _PW[0] = post_w / 2
    if kind in ("tsuiji", "dobei"):
        finish = finish or ("plaster" if kind == "tsuiji" else "shikkui")
        cap = cap or "tile"
        _earth_wall(kind, L, ends, finish, cap, state, hikae, rng, P)
    elif kind == "itabei":
        _itabei(L, ends, kuro, cap, state, rng, P)
    elif kind == "yotsume":
        _yotsume(L, ends, state, rng, P)
    elif kind == "kenninji":
        _kenninji(L, ends, state, rng, P)
    elif kind in ("shiba", "takeho"):
        _brush(L, ends, kind, state, rng, P)
    elif kind == "ikegaki":
        _hedge(L, ends, size, state, rng, P, run=run)
    elif kind == "saku":
        _saku(L, ends, state, rng, P)
    elif kind == "ishigaki":
        _ishigaki(L, ends, stone, H or 0.90, retaining, state, rng, P)
    elif kind == "bank":
        _bank(L, ends, state, rng, P)
    else:
        raise ValueError(kind)
    P.conn("post", (0.0, 0.0, 0.0), hidden=True, role="wall_node", end=ends[0])
    P.conn("post", (L, 0.0, 0.0), hidden=True, role="wall_node", end=ends[1])
    P.dim("module_length_m", round(L, 3), L, source="K3_NOTES §2 (half-ken grid)")
    return P


def step(kind, L=KEN, rise=0.30, ends=("seam", "seam"), seed=0, pid=None, variant="", **opt):
    """Terrain step: the run's second half (L/2..L) stands `rise` higher; place the next module that much higher.
    Capped walls: both caps end at the step with a flush gable (verge tiles + hafu, no overhang, no oni) and the upper
    body's end face (the riser) closes the step; its footing runs down to the lower grade. Fences: the upper half
    starts with a post."""
    pid = pid or "jp_p_wall_site_step"
    P = Part(pid, variant, GROUP, tiers=[1, 2, 3], used_for="terrain step in a " + kind + " run",
             datum="run along +x 0..L; the second half (L/2..L) is %.2f m higher; y 0 = grade at x 0" % rise,
             recipe="sitewall.step(%r, L=%.3f, rise=%.2f, ends=%r)" % (kind, L, rise, ends))
    h = L / 2
    if kind in ("tsuiji", "dobei") or (kind == "itabei" and opt.get("cap") not in (None, "none")):
        P.merge(wall(kind, h, (ends[0], "step"), seed=seed, pid=pid + "_lo", **opt))
        P.merge(wall(kind, L - h, ("step", ends[1]), seed=seed + 1, pid=pid + "_hi", **opt).transformed(
            0.0, (h, rise, 0.0)))
        if kind != "itabei":
            T = TYPES[kind]
            fm = FINISH[opt.get("finish") or ("plaster" if kind == "tsuiji" else "shikkui")]
            # the upper half's footing continues down to the lower grade (its own stops at rise - 0.40)
            y1 = FOOT + rise
            sec = [(FOOT, -_width(T, FOOT) / 2 - 0.01), (FOOT, _width(T, FOOT) / 2 + 0.01),
                   (y1, _width(T, FOOT) / 2 + 0.01), (y1, -_width(T, FOOT) / 2 - 0.01)]
            P.add(_xprism(sec, (h + 0.003, 0.0, 0.0), (L - 0.003, 0.0, 0.0), T["foot"][1], vis=(1, 2, 3), geo=True,
                          view=True, fire=True, tag="step_footing"))
    else:
        P.merge(wall(kind, h, (ends[0], "seam"), seed=seed, pid=pid + "_lo", **opt))
        P.merge(wall(kind, L - h, ("seam", ends[1]), seed=seed + 1, pid=pid + "_hi", **opt).transformed(
            0.0, (h, rise, 0.0)))
    P.conn("post", (0.0, 0.0, 0.0), hidden=True, role="wall_node", end=ends[0])
    P.conn("post", (L, rise, 0.0), hidden=True, role="wall_node", end=ends[1], rise=rise)
    P.meta["rise"] = rise
    return P


# ------------------------------------------------------------------------------------------------ gates in a run
def _post_stone(P, x, rng, size=0.21):
    """A gate post's foot stone (the post stands on it; the post itself runs down into the footing)."""
    P.add(face_stone(rng, x - size / 2 - 0.08, x + size / 2 + 0.08, -0.08, 0.10, size / 2 + 0.09, 1.0,
                     size + 0.18, "stone_cut", jag=0.10, vis=(1, 2), tag="post_stone"))


def gate_kabuki(span=1.5 * KEN, roofed=False, covering="itabuki", leaves="_board", pid="jp_p_gate_kabuki",
                variant="", leaf_y0=None):
    """Kabuki-mon: two 0.21 posts `span` apart (centres at x 0 and span, on the wall line z 0), the kabuki beam on
    the post tops with cut ends, a head tie, two hinged board leaves swinging into the compound (-z; W2C's
    gates.gate_leaves); `roofed` adds a small gable roof on the beam. The beam sits at 2.91..3.15, above any wall cap
    of the kit (tsuiji ridge ~2.85), so walls butt the posts with ends 'post'."""
    from . import gates as G
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="kabuki-mon gate in a wall run (headman, samurai, honjin)",
             datum="posts centred at x 0 and x span on the wall line z 0 (+z outside), y 0 = grade",
             recipe="sitewall.gate_kabuki(span=%.3f, roofed=%r, covering=%r)" % (span, roofed, covering))
    rng = rng_for(pid + variant)
    post, top = 0.21, 3.15
    for x in (0.0, span):
        P.add(box(x - post / 2, x + post / 2, FOOT, top - 0.24, -post / 2, post / 2, "wood_weathered", vis=(1, 2, 3),
                  geo=True, view=True, fire=True, tag="gate_post", grain="long"))
        _post_stone(P, x, rng)
    # kabuki beam: ends cut on a slant underneath, projecting 0.36 past the post centres
    yb, yt = top - 0.24, top
    P.add(prism([(-0.36, yb + 0.10), (-0.26, yb), (span + 0.26, yb), (span + 0.36, yb + 0.10), (span + 0.36, yt),
                 (-0.36, yt)], "z", -0.11, 0.11, "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True,
                tag="kabuki", grain="long"))
    P.add(box(post / 2, span - post / 2, 2.40, 2.52, -0.04, 0.04, "wood_weathered", vis=(1, 2), tag="kashiranuki"))
    # leaf_y0 (FX5): the leaves' bottom over grade when the passage carries a raised sill (compound gates)
    y0 = G.LEAF_Y0 if leaf_y0 is None else leaf_y0
    P.merge(G.gate_leaves(leaves, span, post=post, y0=y0, height=2.22 - (y0 - G.LEAF_Y0), y_floor=y0 - G.LEAF_Y0))
    if roofed:
        S = SR.Spec(0.22, 0.42, top + 0.05, covering, t=0.42, gov=0.42, body="solid", y_solid=top, walkable=False,
                    rafter_sp=0.20, rafter_sec=(0.04, 0.05), ridge_w=0.20, bed_mat="wall_arakabe")
        r = Part(pid + "_roof", "", "")
        SR.straight(r, S, span, ("gable", "gable"))
        P.merge(r)
    for x in (0.0, span):
        P.conn("post", (x, 0.0, 0.0), size=post, role="gate_post")
    P.dim("clear_open_m", ">=1.00 (D1)", span - post - 2 * 0.05)
    return P


def gate_koraimon(span=1.5 * KEN, covering="itabuki", leaves="_board", pid="jp_p_gate_koraimon", variant="",
                  leaf_y0=None):
    """W3D (2026-10-02, spikes/W3D/W3D_NOTES.md site 1): the kora-mon of the checkpoint (Hakone's Kyoguchi gate is
    one; the form dates from the 1590s castle gates): K3's roofed kabuki-mon (two main posts, the kabuki beam, a small
    gable roof along the gate line, two hinged board leaves swinging 90 deg in) + two rear posts (hikae-bashira) set
    back behind the main posts, tied to them at 2.6 m, each pair under its own small gable roof at right angles: the
    open leaves stand under the rear roofs. The rear posts stand just outboard of the main posts' lines so the open
    leaves (against the main posts' back faces) clear them."""
    from . import gates as G
    P = gate_kabuki(span, roofed=True, covering=covering, leaves=leaves, pid=pid, variant=variant, leaf_y0=leaf_y0)
    P.used_for = "kora-mon (checkpoint / official gate in a palisade or wall run)"
    rng = rng_for(pid + variant + "_hikae")
    leaf_w = (span - 0.21) / 2 + G.OVERLAP
    zr = -(leaf_w + 0.40)                     # the rear posts' centre line (behind the open leaves' far edges)
    top_r = 2.72
    for (x, sx) in ((-0.11, -1), (span + 0.11, 1)):
        P.add(box(x - 0.09, x + 0.09, FOOT, top_r, zr - 0.09, zr + 0.09, "wood_weathered", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="hikae_post", grain="long"))
        P.add(stone(rng, x, zr, 0.34, 0.34, 0.14, 0.06, "stone_cut", bury=0.10, n=7, flat_top=0.85, vis=(1, 2),
                    tag="post_stone"))
        # the tie (nuki) from the rear post into the main post's back face, over the leaves' tops
        xm = 0.0 if sx < 0 else span
        a, b = min(x, xm) - 0.05, max(x, xm) + 0.05
        P.add(box(a, b, 2.52, 2.66, zr + 0.09, -0.105, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag="hikae_nuki", grain="long"))
        # the small gable roof over the pair, ridge along z (the leaf's open line), from behind the main post to past
        # the rear post
        S_ = SR.Spec(0.16, 0.36, top_r + 0.05, covering, t=0.42, gov=0.20, body="solid", y_solid=top_r,
                     walkable=False, rafter_sp=0.20, rafter_sec=(0.04, 0.05), ridge_w=0.16, bed_mat="wall_arakabe")
        r = Part(pid + "_hikae_roof", "", "")
        Lr = -zr + 0.30 - 0.32
        SR.straight(r, S_, Lr, ("gable", "gable"))
        P.merge(r.transformed(-90.0, ((x + xm) / 2, 0.0, -0.32)))     # its verge clear of a palisade / wall line
    P.dim("rear_posts_z", round(zr, 3), zr)
    return P


def _arm(x, top):
    """A cross arm (hijiki) on a post top, square to the gate line, its ends cut on a slant underneath."""
    return prism([(top + 0.06, -0.80), (top, -0.70), (top, 0.70), (top + 0.06, 0.80), (top + 0.16, 0.80),
                  (top + 0.16, -0.80)], "x", x - 0.07, x + 0.07, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
                 fire=True, tag="hijiki", grain="long")


def gate_munemon(span=1.5 * KEN, covering="hongawara", leaves="_board", pid="jp_p_gate_munemon", variant="",
                 leaf_y0=None):
    """Mune-mon: the single-ridge gate: two main posts on the gate line carry, through cross arms (hijiki) on their
    tops, a gable roof whose ridge runs along the gate line (eaves front and back, no rear posts), a head tie and
    two hinged board leaves into the compound."""
    from . import gates as G
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="mune-mon gate (temple, samurai, top headman)",
             datum="posts centred at x 0 and x span on the wall line z 0 (+z outside), y 0 = grade",
             recipe="sitewall.gate_munemon(span=%.3f, covering=%r)" % (span, covering))
    rng = rng_for(pid + variant)
    post, top = 0.24, 2.95
    for x in (0.0, span):
        P.add(box(x - post / 2, x + post / 2, FOOT, top, -post / 2, post / 2, "wood_weathered", vis=(1, 2, 3),
                  geo=True, view=True, fire=True, tag="gate_post", grain="long"))
        _post_stone(P, x, rng, post)
        P.add(_arm(x, top))
    P.add(box(-0.30, span + 0.30, top + 0.16, top + 0.32, -0.10, 0.10, "wood_weathered", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="munagi", grain="long"))
    P.add(box(post / 2, span - post / 2, 2.40, 2.54, -0.05, 0.05, "wood_weathered", vis=(1, 2), tag="kashiranuki"))
    # leaf_y0 (FX5): the leaves' bottom over grade when the passage carries a raised sill (compound gates)
    y0 = G.LEAF_Y0 if leaf_y0 is None else leaf_y0
    P.merge(G.gate_leaves(leaves, span, post=post, y0=y0, height=2.22 - (y0 - G.LEAF_Y0), y_floor=y0 - G.LEAF_Y0))
    S = SR.Spec(0.20, 1.05, top + 0.32, covering, t=0.42, gov=0.55, body="open", walkable=True, rafter_sp=0.26,
                courses=5 if covering == "hongawara" else 3)
    r = Part(pid + "_roof", "", "")
    SR.straight(r, S, span, ("gable", "gable"))
    P.merge(r)
    for x in (0.0, span):
        P.conn("post", (x, 0.0, 0.0), size=post, role="gate_post")
    P.dim("clear_open_m", ">=1.00 (D1)", span - post - 2 * 0.05)
    return P


def _hinged_leaf(P, x0, x1, y0, h, mat, rng, kind="plank", lattice=False):
    """One hinged leaf in an opening x0..x1 (jamb faces), hung behind the jambs on the compound face (-z), hinge at
    x0, swinging 90 deg into the compound (gates.py convention, right-hand rule about +y; engine-untested)."""
    from .gates import _leaf_solids
    bone = P.next_bone()
    zf = -0.05 - 0.004
    zb = zf - 0.045
    a0, a1 = x0 - 0.03, x1 + 0.03
    for s in _leaf_solids(a0, a1, y0, y0 + h, zb, zf, "_lattice" if lattice else "_board", rng, astragal=0, hinge="l"):
        s.door = bone
        if isinstance(s.mats, str) and s.mats == "wood_street_dark":
            s.mats = mat
            s.fm = None
            s.finalize()
        P.add(s)
    axis = [(a0, y0, zb), (a0, y0 + h, zb)]
    P.memory[bone + "_axis"] = axis
    P.memory[bone] = [((a0 + a1) / 2, y0 + 1.0, (zb + zf) / 2)]
    action = ((x0 + x1) / 2, y0 + 1.0, zf)
    P.memory[bone + "_action"] = [action]
    d = Door(kind=kind, anims=[{"bone": bone, "type": "rotation", "axis": axis, "amount": math.radians(90.0),
                                "note": "wicket leaf, swings into the compound"}], action=action,
             centre=((a0 + a1) / 2, y0 + h / 2, (zb + zf) / 2), anim_period=1.2, init_opened=0.0,
             sound="doorWoodSlide", display="door", style="hinged", note="wicket (wakido): one hinged leaf",
             engine_tested=False, passable=True, has_view=True, opening=(x0, x1, y0, y0 + h), z_face=zf, side=-1,
             leaf_z=(zb, zf), sweep=(a0, a1), stub=0.0, hinged=True, swing_deg=90.0)
    P.doors.append(d)
    return d


def wicket(kind="itabei", L=KEN, pid="jp_p_gate_wicket", variant="", kuro=False):
    """A 1-ken run module with a wicket door (wakido / shiori-do): clear 1.04 x 1.98 (D1 / D2; the period stoop-
    through wicket is too small, PLAYBOOK D9), one hinged leaf into the compound. itabei / kenninji: the fence either
    side + a small frame with a cap board above the fence; dobei: a door frame in the plastered wall, the cap runs
    on over it."""
    P = Part(pid, variant, GROUP, tiers=[1, 2, 3], used_for="wicket door module in a " + kind + " run",
             datum="run along +x 0..L on the wall centreline z 0, +z outside; y 0 = grade",
             recipe="sitewall.wicket(%r, L=%.3f)" % (kind, L))
    rng = rng_for(pid + variant + kind)
    xm = L / 2
    xa, xb = xm - 0.57, xm + 0.57
    jamb = 0.10
    leafmat = {"itabei": "wood_kuro" if kuro else "wood_weathered", "dobei": "wood_weathered",
               "kenninji": "bamboo_weathered"}[kind]
    if kind == "dobei":
        T = TYPES["dobei"]
        fmat = FINISH["shikkui"]
        y0 = T["foot"][0]
        for (a, b) in ((0.0, xa - jamb / 2), (xb + jamb / 2, L)):
            P.add(_xprism([(FOOT, -0.17), (FOOT, 0.17), (y0, 0.17), (y0, -0.17)], (a, 0.0, 0.0), (b, 0.0, 0.0),
                          "stone_cut", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="foot_core"))
            P.add(_xprism([(y0, -0.15), (y0, 0.15), (T["H"], 0.15), (T["H"], -0.15)], (a, 0.0, 0.0), (b, 0.0, 0.0),
                          fmat, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="wall_body"))
        # over the door: the plastered wall from the lintel to the wall top
        P.add(box(xa - jamb / 2, xb + jamb / 2, 2.12, T["H"], -0.15, 0.15, fmat, vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag="wall_body"))
        top = 2.12
        _cap(P, T, L, ("seam", "seam"), "sangawara", T["H"], fmat)
    else:
        top = 2.30
        P.merge(wall(kind, xa, ("seam", "post"), kuro=kuro, pid="wl", seed=1, post_w=jamb))
        P.merge(wall(kind, L - xb, ("post", "seam"), kuro=kuro, pid="wr", seed=2, post_w=jamb).transformed(
            0.0, (xb, 0.0, 0.0)))
        P.add(box(xa - jamb / 2 - 0.10, xb + jamb / 2 + 0.10, top, top + 0.05, -0.12, 0.12, leafmat, vis=(1, 2, 3),
                  tag="kasagi"))
    for x in (xa, xb):
        P.add(box(x - jamb / 2, x + jamb / 2, FOOT, top, -0.05, 0.05, "wood_weathered", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="jamb", grain="long"))
    P.add(box(xa - jamb / 2, xb + jamb / 2, 1.98 + 0.02, 2.12, -0.05, 0.05, "wood_weathered", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="kamoi"))
    _hinged_leaf(P, xa + jamb / 2, xb - jamb / 2, 0.02, 1.96, leafmat, rng, lattice=(kind == "kenninji"))
    P.conn("post", (0.0, 0.0, 0.0), hidden=True, role="wall_node")
    P.conn("post", (L, 0.0, 0.0), hidden=True, role="wall_node")
    P.dim("clear_width_m", ">=1.00 (D1)", xb - xa - jamb)
    return P


# ------------------------------------------------------------------------------------------------ small gates (FX6)
# FX6 (2026-10-02, Stephen's 3c-1 walk: "the gate to the paper yard is waaaay too big for that fence ... every
# double-door gate seems to be the same"): a family of small gates sized to the fence they sit in. Research, sizes and
# the picker rule: spikes/FX6/FX6_NOTES.md; API: parts/K3_NOTES.md §6. Frame as every gate: posts on the wall line
# z 0 at x 0 and x span (grid nodes), +z outside, leaves on the -z face swinging 90 deg into the compound; leaf_y0 =
# the leaves' bottom over grade (compound gates lift them over FX5's sill pad). POST_W[kind] is the post width the
# fence modules either side stop at (dwelling._wall_path passes it as wall(post_w=...)).
POST_W = {"kabuki": 0.21, "kabuki_roofed": 0.21, "koraimon": 0.21, "munemon": 0.21, "kido_kata": 0.15, "kido_ryo": 0.18,
          "shiorido": 0.12, "opening": 0.12, "opening_board": 0.15}
KIDO_LATCH = 1.26           # kido_kata / shiorido: the latch post's centre from the hinge post's centre
LIGHT_FENCES = ("yotsume", "kenninji", "shiba", "takeho")


def _leaf_door(P, a0, a1, y0, h, zf, mat, rng, variant="_board", note="gate leaf", lattice_fn=None):
    """One hinged leaf a0..a1 (hinge at a0), its street face at zf, on the -z side, swinging 90 deg into the compound
    (right-hand rule about +y, gates.py convention; engine-untested like every rotation door). lattice_fn(zb, zf) ->
    visual solids replaces the board / lattice visuals (the shiorido's bamboo diamond lattice). Returns the Door."""
    from .gates import _leaf_solids
    bone = P.next_bone()
    t = 0.045 if lattice_fn is None else 0.04
    zb = zf - t
    if lattice_fn is None:
        sols = _leaf_solids(a0, a1, y0, y0 + h, zb, zf, variant, rng, astragal=0, hinge="l")
        for s in sols:
            if isinstance(s.mats, str) and s.mats == "wood_street_dark" and mat != "wood_street_dark":
                s.mats = mat
                s.fm = None
                s.finalize()
    else:
        # the leaf's collision box carries View + Fire too: the door action and its checks need a View leaf
        sols = [box(a0, a1, y0, y0 + h, zb, zf, mat, vis=(), geo=True, view=True, fire=True, tag="gate_leaf_geo")]
        sols += lattice_fn(zb, zf)
    for s in sols:
        s.door = bone
        P.add(s)
    axis = [(a0, y0, zb), (a0, y0 + h, zb)]
    P.memory[bone + "_axis"] = axis
    P.memory[bone] = [((a0 + a1) / 2, y0 + min(1.0, h / 2), (zb + zf) / 2)]
    action = ((a0 + a1) / 2, y0 - 0.03 + 1.0, zf)          # 1.0 over the floor the leaf clears by 3 cm (act_h)
    P.memory[bone + "_action"] = [action]
    kind = "lattice" if (lattice_fn is not None or variant == "_lattice") else "plank"
    d = Door(kind=kind, anims=[{"bone": bone, "type": "rotation", "axis": axis, "amount": math.radians(90.0),
                                "note": note + ", swings into the compound"}], action=action,
             centre=((a0 + a1) / 2, y0 + h / 2, (zb + zf) / 2), anim_period=1.2, init_opened=0.0,
             sound="doorWoodSlide", display="gate", style="hinged", note=note, engine_tested=False, passable=True,
             has_view=True, opening=(a0, a1, y0, y0 + h), z_face=zf, side=-1, leaf_z=(zb, zf),
             sweep=(a0, a1), stub=0.0, hinged=True, swing_deg=90.0)
    P.doors.append(d)
    return d


def _sq_post(P, x, w, top, mat, rng, depth=None, stone=True, tag="gate_post"):
    dz = (depth or w) / 2
    P.add(box(x - w / 2, x + w / 2, FOOT, top, -dz, dz, mat, vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag,
              grain="long"))
    if stone:
        _post_stone(P, x, rng, w)


def _round_post(P, x, r, top, rng, cap=True):
    P.add(cyl("y", x, 0.0, r, FOOT, top, "wood_weathered", n=8, vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="gate_post"))
    if cap:
        P.add(cyl("y", x, 0.0, r + 0.008, top - 0.03, top + 0.01, "wood_weathered", n=8, vis=(1,), tag="post_cap"))


def _side_panel(P, fence, x0, x1, kuro=False):
    """The fixed fence panel between a gate's latch post (x0 face) and its far post (x1 face): the fence's own kind."""
    if x1 - x0 < 0.05:
        return
    if fence in LIGHT_FENCES:
        q = wall(fence, x1 - x0 + 0.02, ("post", "post"), pid="gate_side", seed=3, post_w=0.02)
        P.merge(q.transformed(0.0, (x0 - 0.01, 0.0, 0.0)))
        return
    m = "wood_kuro" if kuro else "wood_weathered"
    rng = rng_for("gate_side" + fence + str(kuro))
    for y in (0.30, 1.00, 1.62):
        P.add(box(x0, x1, y, y + 0.09, -0.045, 0.06, m, vis=(1, 2), tag="fence_nuki"))
    P.extend(board_run(x0, x1, 0.04, 1.80, 0.06, 0.08, rng, 0.20, 0.28, m, vis=(1,), tag="fence_board"))
    P.add(box(x0, x1, 0.04, 1.80, 0.06, 0.08, m, vis=(2, 3), tag="fence_board_lod"))
    P.add(box(x0, x1, -0.30, 1.80, -0.045, 0.08, m, vis=(), geo=True, view=True, fire=True, tag="fence_geo"))


def gate_kido_kata(span=KEN, fence="itabei", kuro=False, leaf_y0=None, pid="jp_p_gate_kido", variant="_kata"):
    """Single-leaf board gate (katabiraki ita-kido) for board fences and hedges: two square posts (0.15) to 2.15 with a
    cap board across their tops, a latch post 1.26 m from the hinge post, one battened board leaf (1.86 high) hinged on
    the left post, a fixed panel of the fence's boards between the latch post and the far post. No kabuki beam."""
    from . import gates as G
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="single-leaf board gate (kido) in a board fence / hedge",
             datum="posts centred at x 0 and x span on the wall line z 0 (+z outside), y 0 = grade",
             recipe="sitewall.gate_kido_kata(span=%.3f, fence=%r)" % (span, fence))
    rng = rng_for(pid + variant + fence)
    m = "wood_kuro" if kuro else "wood_weathered"
    pw, top = POST_W["kido_kata"], 2.15
    for x in (0.0, span):
        _sq_post(P, x, pw, top, m, rng)
    xl = KIDO_LATCH
    _sq_post(P, xl, 0.12, top, m, rng, depth=pw, stone=False, tag="latch_post")
    P.add(prism([(-0.12, top + 0.02), (-0.08, top), (span + 0.08, top), (span + 0.12, top + 0.02),
                 (span + 0.12, top + 0.06), (-0.12, top + 0.06)], "z", -0.09, 0.09, m, vis=(1, 2, 3), geo=True,
                view=True, fire=True, tag="kasagi"))
    _side_panel(P, fence if fence != "ikegaki" else "itabei", xl + 0.06, span - pw / 2, kuro)
    y0 = G.LEAF_Y0 if leaf_y0 is None else leaf_y0
    zf = -pw / 2 - G.GAP
    _leaf_door(P, pw / 2 - G.OVERLAP, xl - 0.06 + 0.03, y0, 1.86, zf, m, rng, note="kido leaf (single)")
    for x in (0.0, span):
        P.conn("post", (x, 0.0, 0.0), size=pw, role="gate_post")
    P.dim("clear_open_m", ">=1.00 (D1)", xl - 0.06 - pw / 2 - 0.05)
    P.dim("head_m", ">=2.00 (D2) over the sill", top - y0 + 0.03)
    return P


def gate_kido_ryo(span=KEN, kuro=False, leaf_y0=None, pid="jp_p_gate_kido", variant="_ryo"):
    """Two-leaf board gate (ryobiraki ita-kido) without the kabuki beam: two square posts (0.18) to 2.35 under a cap
    beam (kasagi) with cut ends; gates.gate_leaves '_board' 1.90 high. 1 ken (clear ~1.6) or 1.5 ken for carts."""
    from . import gates as G
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="two-leaf board gate (kido) in a board fence: yard gates",
             datum="posts centred at x 0 and x span on the wall line z 0 (+z outside), y 0 = grade",
             recipe="sitewall.gate_kido_ryo(span=%.3f)" % span)
    rng = rng_for(pid + variant)
    m = "wood_kuro" if kuro else "wood_weathered"
    pw, top = POST_W["kido_ryo"], 2.35
    for x in (0.0, span):
        _sq_post(P, x, pw, top, m, rng)
    P.add(prism([(-0.22, top + 0.04), (-0.14, top), (span + 0.14, top), (span + 0.22, top + 0.04),
                 (span + 0.22, top + 0.12), (-0.22, top + 0.12)], "z", -0.10, 0.10, m, vis=(1, 2, 3), geo=True,
                view=True, fire=True, tag="kasagi", grain="long"))
    y0 = G.LEAF_Y0 if leaf_y0 is None else leaf_y0
    lv = G.gate_leaves("_board", span, post=pw, y0=y0, height=1.90, y_floor=y0 - G.LEAF_Y0)
    for s in lv.solids:
        if isinstance(s.mats, str) and s.mats == "wood_street_dark":
            s.mats = m                          # the leaves take the fence's own wood (black in a kuro fence)
            s.fm = None
            s.finalize()
    P.merge(lv)
    for x in (0.0, span):
        P.conn("post", (x, 0.0, 0.0), size=pw, role="gate_post")
    P.dim("clear_open_m", ">=1.00 (D1)", span - pw - 2 * G.LEAF_T)
    return P


def _diamond(a0, a1, y0, y1, zb, zf, step=0.16, w=0.022, mat="bamboo_weathered"):
    """Split-bamboo strips in a diamond lattice over the rectangle a0..a1 x y0..y1 (two layers, +45 / -45 deg)."""
    from .shapes import oriented_box
    out = []
    zm = (zb + zf) / 2
    for sgn, zc in ((1.0, zm - 0.006), (-1.0, zm + 0.006)):
        # lines x = a0 + c + sgn * (y - y0), c on a 'step' spacing; clip t = y - y0 in [0, H] so x stays in [a0, a1]
        H_ = y1 - y0
        c = -H_ - step
        while c < (a1 - a0) + H_ + step:
            lo, hi = 0.0, H_
            # a0 <= a0 + c + sgn * t <= a1
            if sgn > 0:
                lo, hi = max(lo, -c), min(hi, (a1 - a0) - c)
            else:
                lo, hi = max(lo, c - (a1 - a0)), min(hi, c)
            if hi - lo > 0.05:
                pa = (a0 + c + sgn * lo, y0 + lo)
                pb = (a0 + c + sgn * hi, y0 + hi)
                L = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
                u = ((pb[0] - pa[0]) / L, (pb[1] - pa[1]) / L, 0.0)
                out.append(oriented_box(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2, zc), u, (-u[1], u[0], 0.0),
                                        (0.0, 0.0, 1.0), L / 2, w / 2, 0.003, mat, vis=(1,), tag="shiori_strip"))
            c += step
    return out


def gate_shiorido(span=KEN, fence="yotsume", leaf_y0=None, pid="jp_p_gate_shiorido", variant=""):
    """Shiorido: the low bamboo garden gate of light fences (yotsume, kenninji, brushwood): two round posts to 1.35, a
    latch post, one leaf of split bamboo woven in a diamond lattice on a thin round-bamboo frame, rope ties; open
    above (no head). See-through (Geometry only, no View), like the fence."""
    from . import gates as G
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="shiorido: low bamboo lattice gate in a light fence",
             datum="posts centred at x 0 and x span on the wall line z 0 (+z outside), y 0 = grade",
             recipe="sitewall.gate_shiorido(span=%.3f, fence=%r)" % (span, fence))
    rng = rng_for(pid + variant + fence)
    r, top = POST_W["shiorido"] / 2, 1.35
    for x in (0.0, span):
        _round_post(P, x, r, top, rng)
    xl = KIDO_LATCH
    _round_post(P, xl, 0.05, top - 0.05, rng)
    _side_panel(P, fence, xl + 0.05, span - r)
    y0 = G.LEAF_Y0 if leaf_y0 is None else leaf_y0
    h = 1.20
    a0, a1 = r - 0.02, xl - 0.05 + 0.03
    zf = -r - 0.004

    def lattice(zb, zf_):
        zc = (zb + zf_) / 2
        out = []
        fr = 0.02
        for x in (a0 + fr, a1 - fr):
            out.append(cyl("y", x, zc, fr, y0, y0 + h, "bamboo_weathered", n=6, vis=(1, 2), tag="shiori_frame"))
        for y in (y0 + fr, y0 + h - fr, y0 + h * 0.55):
            out.append(cyl("x", y, zc, fr * 0.9, a0 + fr, a1 - fr, "bamboo_weathered", n=6, vis=(1, 2),
                           tag="shiori_frame"))
        out += _diamond(a0 + 2 * fr, a1 - 2 * fr, y0 + 2 * fr, y0 + h - 2 * fr, zb, zf_)
        # rope ties at the hinge (two loops round the post) and the latch
        for y in (y0 + 0.25, y0 + h - 0.25):
            out.append(box(a0 - 0.01, a0 + 0.06, y - 0.02, y + 0.02, zb - 0.005, zf_ + 0.005, "straw_rope", vis=(1,),
                           tag="tie"))
        out.append(box(a1 - 0.07, a1 + 0.01, y0 + h * 0.55 - 0.02, y0 + h * 0.55 + 0.02, zb - 0.005, zf_ + 0.005,
                       "straw_rope", vis=(1,), tag="tie"))
        return out
    _leaf_door(P, a0, a1, y0, h, zf, "bamboo_weathered", rng, note="shiorido leaf (bamboo lattice)",
               lattice_fn=lattice)
    for x in (0.0, span):
        P.conn("post", (x, 0.0, 0.0), size=2 * r, role="gate_post")
    P.dim("clear_open_m", ">=1.00 (D1)", xl - 0.05 - r - 0.045)
    return P


def gate_opening(span=KEN, fence="yotsume", pid="jp_p_gate_opening", variant=""):
    """A plain opening between two posts, no leaf (light fences: the lane entrance of a row yard, a work yard's
    gap): round posts to 1.35 in bamboo fences, square 0.15 posts to 2.10 in board fences."""
    P = Part(pid, variant, GROUP, tiers=[2, 3], used_for="a plain opening between two gate posts (no leaf)",
             datum="posts centred at x 0 and x span on the wall line z 0 (+z outside), y 0 = grade",
             recipe="sitewall.gate_opening(span=%.3f, fence=%r)" % (span, fence))
    rng = rng_for(pid + variant + fence)
    if fence in LIGHT_FENCES:
        for x in (0.0, span):
            _round_post(P, x, POST_W["opening"] / 2, 1.35, rng)
    else:
        for x in (0.0, span):
            _sq_post(P, x, POST_W["opening_board"], 2.10, "wood_weathered", rng)
    for x in (0.0, span):
        P.conn("post", (x, 0.0, 0.0), role="gate_post")
    P.dim("clear_m", ">=1.00 (D1)", span - POST_W["opening"])
    return P


def gate_post_w(kind, fence=None):
    """The post width a fence module stops at beside a gate of this kind."""
    if kind == "opening" and fence not in LIGHT_FENCES:
        return POST_W["opening_board"]
    return POST_W.get(kind, 0.21)


# ------------------------------------------------------------------------------------------------ whole runs
def _split(length):
    out = []
    r = length
    for m in (2 * KEN, KEN, HALF):
        while r >= m - 1e-6:
            out.append(m)
            r -= m
    if r > 0.01:
        raise ValueError("wall segment %.3f m is not on the half-ken grid" % length)
    return out


def run_wall(nodes, kind, gates=(), closed=False, name="wall_run", **opt):
    """A whole wall along grid nodes [(x, z), ...] (axis-aligned segments, lengths on the half-ken grid). Walk the
    plot CLOCKWISE seen from above with x east, z north: the outside (+z of each module) then faces out.
    gates: [(segment index, offset from the segment start, 'kabuki' | 'kabuki_roofed' | 'munemon' | 'wicket',
    span)]: the gate's posts sit on the grid at offset and offset + span (wicket: span = its module length).
    closed: the last node joins the first. Returns one merged Part (the caller's frame, y 0 = grade)."""
    P = Part(name, "", GROUP)
    n = len(nodes)
    segs = [(nodes[i], nodes[(i + 1) % n]) for i in range(n if closed else n - 1)]

    def turn(i, j):
        (a, b), (c, d) = segs[i], segs[j]
        d1 = ((b[0] - a[0]), (b[1] - a[1]))
        d2 = ((d[0] - c[0]), (d[1] - c[1]))
        cr = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(cr) < 1e-9:
            return "seam"
        return "corner+z" if cr > 0 else "corner-z"

    def put(q, deg, a, x0):
        P.merge(q.transformed(deg, (a[0] + math.cos(math.radians(deg)) * x0, 0.0,
                                    a[1] + math.sin(math.radians(deg)) * x0)))
    rseed = run_seed(name)
    s_seg = 0.0
    for i, (a, b) in enumerate(segs):
        dx, dz = b[0] - a[0], b[1] - a[1]
        Ls = math.hypot(dx, dz)
        deg = math.degrees(math.atan2(dz, dx))
        e0 = turn(i - 1, i) if (closed or i > 0) else "end"
        e1 = turn(i, (i + 1) % len(segs)) if (closed or i < len(segs) - 1) else "end"
        pieces = []
        x = 0.0
        for g in sorted([g for g in gates if g[0] == i], key=lambda g: g[1]):
            pieces.append(("wall", x, g[1]))
            pieces.append(("gate", g[1], g[1] + g[3], g[2]))
            x = g[1] + g[3]
        pieces.append(("wall", x, Ls))
        for k, pc in enumerate(pieces):
            if pc[0] == "gate":
                x0, x1, gk = pc[1], pc[2], pc[3]
                if gk.startswith("kabuki"):
                    q = gate_kabuki(x1 - x0, roofed=gk.endswith("roofed"))
                elif gk == "munemon":
                    q = gate_munemon(x1 - x0)
                else:
                    q = wicket(kind if kind in ("itabei", "dobei", "kenninji") else "itabei", x1 - x0)
                put(q, deg, a, x0)
                continue
            x0, x1 = pc[1], pc[2]
            if x1 - x0 < 0.05:
                continue
            gb = pieces[k - 1][3] if k > 0 and pieces[k - 1][0] == "gate" else None
            ga = pieces[k + 1][3] if k < len(pieces) - 1 and pieces[k + 1][0] == "gate" else None
            mods = _split(x1 - x0)
            xx = x0
            for m_i, m in enumerate(mods):
                if xx < 1e-6:
                    s0 = e0
                elif m_i == 0 and gb:
                    s0 = "seam" if gb == "wicket" else "post"
                else:
                    s0 = "seam"
                if abs(xx + m - Ls) < 1e-6:
                    s1 = e1
                elif m_i == len(mods) - 1 and ga:
                    s1 = "seam" if ga == "wicket" else "post"
                else:
                    s1 = "seam"
                q = wall(kind, m, (s0, s1), seed=int(xx * 100) + i * 1000, pid=name + "_%d_%d" % (i, m_i),
                         run=(s_seg + xx, rseed), **opt)
                put(q, deg, a, xx)
                xx += m
        s_seg += Ls
    return P


def run_seed(name):
    """A stable per-run seed (FX5: the hedge noise of one path)."""
    import zlib
    return zlib.crc32(name.encode("utf-8")) & 0xFFFF


# ------------------------------------------------------------------------------------------------ registry
def _v(kind, **kw):
    return ("wall", kind, kw)


VARIANTS = {
    "jp_p_wall_site_tsuiji": {
        "_plaster_tile": _v("tsuiji", finish="plaster", cap="tile"),
        "_nakanuri_tile": _v("tsuiji", finish="nakanuri", cap="tile"),
        "_earth_hongawara": _v("tsuiji", finish="earth", cap="hongawara"),
        "_suji5_hongawara": _v("tsuiji", finish="suji5", cap="hongawara"),
        "_neri_tile": _v("tsuiji", finish="neri", cap="tile"),
        "_plaster_board": _v("tsuiji", finish="plaster", cap="board"),
        "_2ken": _v("tsuiji", L=2 * KEN, finish="plaster", cap="tile"),
        "_end": _v("tsuiji", finish="plaster", cap="tile", ends=("end", "seam")),
        "_corner": _v("tsuiji", finish="plaster", cap="tile", ends=("seam", "corner+z")),
        "_ab_collapsed": _v("tsuiji", L=2 * KEN, finish="plaster", cap="tile", state="collapsed"),
        "_ab_tiles": _v("tsuiji", finish="plaster", cap="tile", state="tiles"),
        "_ab_overgrown": _v("tsuiji", finish="earth", cap="tile", state="overgrown"),
    },
    "jp_p_wall_site_dobei": {
        "_shikkui": _v("dobei", finish="shikkui"),
        "_namako": _v("dobei", finish="namako"),
        "_kuro": _v("dobei", finish="kuro"),
        "_hikae": _v("dobei", L=2 * KEN, finish="shikkui", hikae=True),
        "_end": _v("dobei", finish="shikkui", ends=("end", "seam")),
        "_corner": _v("dobei", finish="shikkui", ends=("seam", "corner+z")),
        "_ab_collapsed": _v("dobei", L=2 * KEN, finish="shikkui", state="collapsed"),
        "_ab_tiles": _v("dobei", finish="namako", state="tiles"),
    },
    "jp_p_wall_site_itabei": {
        "_plain": _v("itabei"),
        "_kuro": _v("itabei", kuro=True),
        "_cap_board": _v("itabei", cap="board"),
        "_cap_tile": _v("itabei", cap="tile", kuro=True),
        "_end": _v("itabei", ends=("end", "seam")),
        "_corner": _v("itabei", ends=("seam", "corner+z")),
        "_ab_leaning": _v("itabei", state="leaning"),
        "_ab_broken": _v("itabei", state="broken"),
    },
    "jp_p_fence_yotsume": {
        "_std": _v("yotsume"),
        "_end": _v("yotsume", ends=("end", "seam")),
        "_corner": _v("yotsume", ends=("seam", "corner+z")),
        "_ab_leaning": _v("yotsume", state="leaning"),
        "_ab_broken": _v("yotsume", state="broken"),
    },
    "jp_p_fence_kenninji": {
        "_std": _v("kenninji"),
        "_end": _v("kenninji", ends=("end", "seam")),
        "_corner": _v("kenninji", ends=("seam", "corner+z")),
        "_ab_leaning": _v("kenninji", state="leaning"),
        "_ab_broken": _v("kenninji", state="broken"),
    },
    "jp_p_fence_shiba": {
        "_shiba": _v("shiba"),
        "_takeho": _v("takeho"),
        "_end": _v("shiba", ends=("end", "seam")),
        "_ab_broken": _v("shiba", state="broken"),
    },
    "jp_p_hedge_ikegaki": {
        "_low": _v("ikegaki", size="low"),
        "_tall": _v("ikegaki", size="tall"),
        "_end": _v("ikegaki", size="low", ends=("end", "seam")),
        "_corner": _v("ikegaki", size="low", ends=("seam", "corner+z")),
        "_ab_overgrown": _v("ikegaki", size="low", state="overgrown"),
    },
    "jp_p_wall_site_ishigaki": {
        "_nozura": _v("ishigaki", stone="nozura", H=0.90),
        "_nozura_ret12": _v("ishigaki", stone="nozura", H=1.20, retaining=True),
        "_nozura_ret18": _v("ishigaki", stone="nozura", H=1.80, retaining=True),
        "_uchikomi_ret12": _v("ishigaki", stone="uchikomi", H=1.20, retaining=True),
        "_ab_collapsed": _v("ishigaki", stone="nozura", H=1.20, retaining=True, state="collapsed"),
    },
    "jp_p_wall_site_bank": {
        "_stone_toe": _v("bank"),
    },
    "jp_p_wall_site_step": {
        "_tsuiji_030": ("step", "tsuiji", dict(rise=0.30, finish="plaster", cap="tile")),
        "_tsuiji_060": ("step", "tsuiji", dict(rise=0.60, finish="plaster", cap="tile")),
        "_dobei_030": ("step", "dobei", dict(rise=0.30, finish="shikkui")),
        "_itabei_030": ("step", "itabei", dict(rise=0.30)),
        "_yotsume_030": ("step", "yotsume", dict(rise=0.30)),
        "_ikegaki_030": ("step", "ikegaki", dict(rise=0.30)),
    },
    "jp_p_gate_kabuki": {
        "_open": ("kabuki", None, dict(roofed=False)),
        "_roofed": ("kabuki", None, dict(roofed=True)),
    },
    "jp_p_gate_munemon": {
        "_hongawara": ("munemon", None, dict(covering="hongawara")),
        "_itabuki": ("munemon", None, dict(covering="itabuki")),
    },
    "jp_p_gate_wicket": {
        "_itabei": ("wicket", "itabei", {}),
        "_dobei": ("wicket", "dobei", {}),
        "_kenninji": ("wicket", "kenninji", {}),
    },
}


def part_variant(pid, variant):
    how, kind, kw = VARIANTS[pid][variant]
    kw = dict(kw)
    if how == "wall":
        L = kw.pop("L", KEN)
        ends = kw.pop("ends", ("seam", "seam"))
        P = wall(kind, L, ends, pid=pid, variant=variant, **kw)
    elif how == "step":
        rise = kw.pop("rise")
        P = step(kind, KEN, rise, pid=pid, variant=variant, **kw)
    elif how == "kabuki":
        P = gate_kabuki(1.5 * KEN, pid=pid, variant=variant, **kw)
    elif how == "munemon":
        P = gate_munemon(1.5 * KEN, pid=pid, variant=variant, **kw)
    else:
        P = wicket(kind, KEN, pid=pid, variant=variant)
    P.group = GROUP
    if "_ab_" in variant:
        P.wear = "_w2"
    P.notes.append("K3 wall kit (parts/K3_NOTES.md); samples at _w1 (abandoned at _w2); wear per instance")
    return P


def register(reg):
    for pid, vs in VARIANTS.items():
        reg(pid, list(vs), lambda v, pid=pid: part_variant(pid, v))
