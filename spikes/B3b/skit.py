"""skit - the B3b site-object kit (outdoor props, wave 1): B3a's furniture kit (spikes/B3a/fkit.py, bits.py, imported
read-only, nothing there is modified) plus the outdoor helpers: oriented members (poles, beams, ropes between any two
points), two-sided cloth grids, atlas text decals, moss and leaf-litter patches, spoked wheels.

Site-object frame (BUILD_LIST 'Engine notes', PLAYBOOK §10.4): origin = base centre on the terrain, +y up, +z = the
object's front (the side that faces the road or the viewer), autocenter=0. Anchors (sidecar 'anchor'):
  'floor'  free-standing on the terrain (most items); may be seated up to `bury` m into the ground (C6: 0-2 cm,
           stones and posts deeper where noted)
  'wall'   wall-backed or building proxy: the wall plane is z = 0 and the object stands `wall_gap` m in front of it
           (+z); y = 0 is the ground / floor at the wall foot (firewood stacks, eave buckets, shop-front dressing)
"""
import copy
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
import fkit  # noqa: E402
import bits  # noqa: E402
from fkit import (core, mlod, box, prism, ngon, sheet, hexa, Solid, lathe, xf, xfs, flat_poly, W, col, col_solid,  # noqa
                  cyl_col, lcyl, rest, auto_smooth, rotated_box, ring_band, FPart)
from bits import disc, jag_rim, stain, rope_ring, blob, mound, pillow  # noqa: E402,F401

# ------------------------------------------------------------------------------------------------ materials (outdoor)
WOOD = "wood_weathered"
DARK = "wood_street_dark"
KURO = "wood_kuro"
BAMBOO = "bamboo_weathered"
IRON = "metal_iron"
CUT = "stone_cut"
FIELD = "stone_field"
RIVER = "stone_river"
CARVED = "stone_carved"
ROOFB = "roof_kureita"
MUSHIRO = "straw_mushiro"
ROPE = "straw_rope"
STACK = "straw_stack"
TAWARA = "straw_tawara"
PAPER = "paper_shoji"
CHOCHIN = "paper_chochin"
NOREN = "textile_noren"
KINARI = "textile_kinari"
REED = "reed_yoshizu"
ENDG = "wood_endgrain"
LEAF = "ground_leaf_litter"
MOSS = "decal_moss"
LITTER = "decal_litter"
SUMI = "decal_sumi_text"
CTEXT = "decal_carved_text"
BENGARA = "wood_bengara"
BIB = "textile_bib_red"          # added by B3b through B1's pipeline (research/materials/make_b3b_materials.py)

# PLAYBOOK §12 + G1 A3 decision 9 (1,500 is a ceiling): LOD0 / LOD1 / LOD2 caps per class
BUDGET = {"small": (300, 300, 300), "box": (600, 300, 120), "medium": (1500, 600, 200)}


class SPart(FPart):
    """A site object. need: which collision LODs it must have ('geo', 'view', 'fire'): straw stacks are soft cover
    (View only), cloth and rope have none (then flat=True: visual only)."""

    def __init__(self, name, budget="small", res3=False, mass=10.0, anchor="floor", wear="_w1", need=("geo", "view", "fire"),
                 bury=0.02, wall_gap=0.0, flat=False):
        super().__init__(name, budget=budget, res3=res3, mass=mass, anchor=anchor, flat=flat, wear=wear)
        self.need = () if flat else tuple(need)
        self.bury = bury
        self.wall_gap = wall_gap


# ------------------------------------------------------------------------------------------------ transforms
def _v(p):
    return tuple(float(c) for c in p)


def frame(s, origin, ux, uy, uz):
    """Copy of a solid expressed in a new orthonormal frame: p' = origin + x*ux + y*uy + z*uz."""
    s.finalize()
    n = copy.copy(s)
    f = lambda p: (origin[0] + p[0] * ux[0] + p[1] * uy[0] + p[2] * uz[0],   # noqa: E731
                   origin[1] + p[0] * ux[1] + p[1] * uy[1] + p[2] * uz[1],
                   origin[2] + p[0] * ux[2] + p[1] * uy[2] + p[2] * uz[2])
    r = lambda q: (q[0] * ux[0] + q[1] * uy[0] + q[2] * uz[0], q[0] * ux[1] + q[1] * uy[1] + q[2] * uz[1],  # noqa
                   q[0] * ux[2] + q[1] * uy[2] + q[2] * uz[2])
    n.verts = [f(v) for v in s.verts]
    n.center = f(s.center)
    n.fn = [r(q) for q in s.fn]
    if getattr(s, "vn", None) is not None:
        n.vn = [[r(q) for q in ff] for ff in s.vn]
    if s.normals is not None:
        n.normals = n.fn
    n.faces = [list(ff) for ff in s.faces]
    for k in ("wear", "no_dust", "tag"):
        if hasattr(s, k):
            setattr(n, k, getattr(s, k))
    return n


def basis(d, up=(0.0, 1.0, 0.0)):
    """Orthonormal (ux, uy=d, uz) with ux horizontal where possible."""
    d = core.norm(d)
    a = core.cross(d, up)
    if core.length(a) < 1e-6:
        a = core.cross(d, (1.0, 0.0, 0.0))
    ux = core.norm(a)
    uz = core.norm(core.cross(ux, d))
    return ux, d, uz


def pole(p0, p1, r, mat, n=6, vis=(1, 2), caps=None, geo=False, view=False, fire=None, wear=None, r1=None, phase=None):
    """A round member from p0 to p1 (any direction). r1: taper radius at p1. Closed (caps)."""
    p0, p1 = _v(p0), _v(p1)
    L = core.length(core.sub(p1, p0))
    r1 = r if r1 is None else r1
    ph = math.pi / n if phase is None else phase
    b = [(r * math.cos(ph + 2 * math.pi * k / n), r * math.sin(ph + 2 * math.pi * k / n)) for k in range(n)]
    t = [(r1 * math.cos(ph + 2 * math.pi * k / n), r1 * math.sin(ph + 2 * math.pi * k / n)) for k in range(n)]
    verts = [(x, 0.0, z) for x, z in b] + [(x, L, z) for x, z in t]
    faces = [list(range(n))[::-1], list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    mats = mat if caps is None else {"top": caps, "bottom": caps, "default": mat}
    s = Solid(verts, faces, mats, vis=vis, geo=geo, view=view, fire=fire, grain=None)
    s.uv = "grain"
    ux, uy, uz = basis(core.sub(p1, p0))
    s = frame(s, p0, ux, uy, uz)
    if wear:
        s.wear = wear
    return s


def beam(p0, p1, w, h, mat, up=(0.0, 1.0, 0.0), vis=(1, 2), geo=False, view=False, fire=None, wear=None, **kw):
    """A rectangular member from p0 to p1 (centre line), w across (horizontal-ish), h in the `up` direction."""
    p0, p1 = _v(p0), _v(p1)
    L = core.length(core.sub(p1, p0))
    s = box(-w / 2, w / 2, 0.0, L, -h / 2, h / 2, mat, vis=vis, geo=geo, view=view, fire=fire, **kw)
    s.uv = "grain"
    d = core.norm(core.sub(p1, p0))
    uz = core.norm(core.sub(up, core.mul(d, core.dot(up, d))))
    if core.length(core.sub(up, core.mul(d, core.dot(up, d)))) < 1e-6:
        uz = (0.0, 0.0, 1.0)
    ux = core.norm(core.cross(d, uz))
    s = frame(s, p0, ux, d, uz)
    if wear:
        s.wear = wear
    return s


def rope_path(pts, r, mat=None, n=4, vis=(1,), wear=None):
    """A rope along a polyline: one thin closed prism per segment (visual only)."""
    mat = mat or ROPE
    return [pole(pts[i], pts[i + 1], r, mat, n=n, vis=vis, wear=wear) for i in range(len(pts) - 1)]


def sag(p0, p1, drop, k=6):
    """k+1 points from p0 to p1 hanging `drop` m at the middle (parabola)."""
    out = []
    for i in range(k + 1):
        t = i / k
        p = core.add(p0, core.mul(core.sub(p1, p0), t))
        out.append((p[0], p[1] - drop * 4 * t * (1 - t), p[2]))
    return out


# ------------------------------------------------------------------------------------------------ surfaces
def grid_sheet(f, nu, nv, mat, vis=(1,), two_sided=True, uv=None, wear=None, tile=None):
    """A cloth / paper surface from a parametric f(u, v) -> point (u, v in [0, 1]). uv(u, v) -> texture uv (default:
    world-ish metres / tile along the surface). Two-sided: a back copy with reversed normals."""
    t = tile or core.mat_info(mat)["tile"]
    P = [[_v(f(i / nu, j / nv)) for j in range(nv + 1)] for i in range(nu + 1)]
    # arc-length uv
    if uv is None:
        us = [[0.0] * (nv + 1) for _ in range(nu + 1)]
        vs = [[0.0] * (nv + 1) for _ in range(nu + 1)]
        for j in range(nv + 1):
            for i in range(1, nu + 1):
                us[i][j] = us[i - 1][j] + core.length(core.sub(P[i][j], P[i - 1][j]))
        for i in range(nu + 1):
            for j in range(1, nv + 1):
                vs[i][j] = vs[i][j - 1] + core.length(core.sub(P[i][j], P[i][j - 1]))
        UV = lambda i, j: (us[i][j] / t, vs[i][j] / t)   # noqa: E731
    else:
        UV = lambda i, j: uv(i / nu, j / nv)             # noqa: E731
    quads, normals, uvs = [], [], []
    for i in range(nu):
        for j in range(nv):
            q = [P[i][j], P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]]
            n = core.norm(core.newell(q))
            quads.append(q)
            normals.append(n)
            uvs.append([UV(i, j), UV(i + 1, j), UV(i + 1, j + 1), UV(i, j + 1)])
            if two_sided:
                quads.append(q[::-1])
                normals.append(core.mul(n, -1.0))
                uvs.append([UV(i, j + 1), UV(i + 1, j + 1), UV(i + 1, j), UV(i, j)])
    s = sheet(quads, mat, normals, vis=vis, uvs=uvs)
    s.finalize()
    if wear:
        s.wear = wear
    return s


_CELLS = {}


def cell(mat, name):
    """uv rect [u0, v0, u1, v1] (v down) of an atlas cell from the material sidecar."""
    if mat not in _CELLS:
        mi = core.mat_info(mat)
        sc = json.load(open(os.path.join(core.LIB, mi["family"], mi["id"] + ".json"), encoding="utf-8"))
        _CELLS[mat] = sc.get("cells", {})
    return _CELLS[mat][name]["uv"]


def cell_size(mat, name):
    """The cell's real size (m): 1024 px = 1 m on both atlases."""
    u0, v0, u1, v1 = cell(mat, name)
    return (u1 - u0), (v1 - v0)


def decal(tl, tr, br, bl, mat, cellname, wear=None, vis=(1,), crop=None):
    """One alpha decal quad mapped onto an atlas cell (tl -> the cell's top-left). crop = (a0, b0, a1, b1) fractions of
    the cell to use (e.g. only the top half of a banner text)."""
    u0, v0, u1, v1 = cell(mat, cellname)
    if crop:
        a0, b0, a1, b1 = crop
        u0, u1 = u0 + (u1 - u0) * a0, u0 + (u1 - u0) * a1
        v0, v1 = v0 + (v1 - v0) * b0, v0 + (v1 - v0) * b1
    q = [_v(tl), _v(tr), _v(br), _v(bl)]
    n = core.norm(core.newell(q))
    s = sheet([q], mat, n, vis=vis, uvs=[[(u0, v0), (u1, v0), (u1, v1), (u0, v1)]])
    s.finalize()
    s.cell = "%s:%s" % (mat, cellname)
    if wear:
        s.wear = wear
    return s


def text_on(center, right, up, h, mat, cellname, wear=None, off=0.003, normal=None, vis=(1,), width=None, crop=None):
    """A text decal centred at `center` on a plane (right, up unit vectors), height h (width from the cell aspect unless
    given), pushed `off` along the plane normal (right x up points out of the face)."""
    cw, ch = cell_size(mat, cellname)
    if crop:
        cw, ch = cw * (crop[2] - crop[0]), ch * (crop[3] - crop[1])
    w = width if width is not None else h * cw / ch
    nrm = normal or core.norm(core.cross(right, up))
    c = core.add(center, core.mul(nrm, off))
    hr, hu = core.mul(right, w / 2), core.mul(up, h / 2)
    tl = core.add(core.sub(c, hr), hu)
    tr = core.add(core.add(c, hr), hu)
    br = core.sub(core.add(c, hr), hu)
    bl = core.sub(core.sub(c, hr), hu)
    return decal(tl, tr, br, bl, mat, cellname, wear=wear, vis=vis, crop=crop)


# ------------------------------------------------------------------------------------------------ text facing (L2 fix)
# L2, 2026-09-30 (spikes/L2/textface.py, research/outdoor_kit/contact_sheets/l2_textcheck_*.jpg): DayZ model space is
# LEFT-handed (x east, y up, z north) and the game draws single-sided faces from their outward side only. decal() /
# text_on() above assume right x up = outward in a right-handed sense, so the quads they write (and grid-sheet text
# built the same way) (a) face INTO their host surface (outward = -(right x up)): invisible in game from the front,
# and (b) run the texture u along 'right', which a viewer outside sees as his LEFT: mirrored. face_text() turns such
# solids round and, when asked, mirrors u within the solid's own cell range. text_ok() = text_on() already fixed.
TEXT_MATS = ("decal_sumi_text", "decal_carved_text", "decal_sumi_text_life")


def is_text(s):
    return isinstance(s.mats, str) and s.mats in TEXT_MATS


def face_text(solids, mirror_u=True):
    """Fix text solids in place (see above): flip every face's outward normal; mirror u if mirror_u. Returns how many
    solids it turned. B3b's builders call it with mirror_u=True (their u runs along 'right'), L1's with False (lkit.text
    and lkit.uvcell already mirror u)."""
    k = 0
    for s in solids:
        if not is_text(s) or getattr(s, "_text_faced", False):
            continue
        s.finalize()
        if mirror_u:
            us = [a for f in s.fuv for a, _ in f]
            lo, hi = min(us), max(us)
            s.fuv = [[(lo + hi - a, b) for a, b in f] for f in s.fuv]
        s.fn = [core.mul(n, -1.0) for n in s.fn]
        if s.normals is not None:
            s.normals = s.fn
        if getattr(s, "vn", None) is not None:
            s.vn = [[core.mul(q, -1.0) for q in ff] for ff in s.vn]
        s._text_faced = True
        k += 1
    return k


def text_ok(center, right, up, h, mat, cellname, wear=None, off=0.003, vis=(1,), width=None, crop=None):
    """text_on(), faced out along right x up and reading correctly in game (u runs to the viewer's right). New code
    (L2 on) uses this; right x up is the side the text is read from."""
    s = text_on(center, right, up, h, mat, cellname, wear=wear, off=off, vis=vis, width=width, crop=crop)
    face_text([s], mirror_u=True)
    return s


def moss_top(seed, cx, cz, r0, y, sx=1.0, sz=1.0, wear="_w1", vis=(1,)):
    """A moss / lichen patch 3 mm above a top face (decal)."""
    pts = [(cx + x, cz + z) for x, z in blob(seed, r0, sx=sx, sz=sz)]
    return flat_poly(pts, y + 0.003, MOSS, vis=vis, wear=wear, uvoff=(random.Random(seed).random(), 0.21))


def moss_face(p, right, up, w, h, seed=0, wear="_w1", vis=(1,), off=0.003):
    """A moss decal quad on a vertical face (centre p, plane right/up)."""
    nrm = core.norm(core.cross(right, up))
    c = core.add(p, core.mul(nrm, off))
    hr, hu = core.mul(right, w / 2), core.mul(up, h / 2)
    q = [core.add(core.sub(c, hr), hu), core.add(core.add(c, hr), hu), core.sub(core.add(c, hr), hu),
         core.sub(core.sub(c, hr), hu)]
    r = random.Random(seed)
    u0, v0 = r.random(), r.random()
    t = core.mat_info(MOSS)["tile"]
    s = sheet([q], MOSS, nrm, vis=vis, uvs=[[(u0, v0), (u0 + w / t, v0), (u0 + w / t, v0 + h / t), (u0, v0 + h / t)]])
    s.finalize()
    s.wear = wear
    return s


def leaves(seed, cx, cz, r0, y, wear="_w1", vis=(1,), sx=1.0, sz=1.0, mat=None):
    """Leaf litter / silt fill (an opaque irregular patch at height y: inside tubs, gutters, basins)."""
    pts = [(cx + x, cz + z) for x, z in blob(seed, r0, n=9, jitter=0.12, sx=sx, sz=sz)]
    return flat_poly(pts, y, mat or LEAF, vis=vis, wear=wear, uvoff=(random.Random(seed).random(), 0.5))


def litter(seed, cx, cz, r0, sx=1.0, sz=1.0, wear="_w2", vis=(1,)):
    """Dead-world ground litter decal (leaves, straw bits) 3 mm above the ground (B3a's decal_litter)."""
    return stain(seed, cx, cz, r0, y=0.003, mat=LITTER, wear=wear, vis=vis, sx=sx, sz=sz)


def add_all(P, ss):
    for s in ss:
        P.add(s)


def ground(P, keep=0.0):
    """Shift every solid so the lowest visual vertex sits at y = keep."""
    lo = min(v[1] for s in P.solids if s.vis for v in s.verts)
    if abs(lo - keep) > 1e-6:
        P.solids = [xf(s, t=(0.0, keep - lo, 0.0)) for s in P.solids]
        P.roadway = [([(q[0], q[1] + keep - lo, q[2]) for q in pts], surf) for pts, surf in P.roadway]
        for L in P.loot:
            L["y"] = round(L["y"] + keep - lo, 4)
            L["points"] = [[p[0], round(p[1] + keep - lo, 4), p[2]] for p in L["points"]]
    return P


def tilt(ss, rx=0.0, rz=0.0, ry=0.0, pivot=(0.0, 0.0, 0.0), t=(0.0, 0.0, 0.0)):
    return [xf(s, rx=rx, ry=ry, rz=rz, pivot=pivot, t=t) for s in ss]


def rng(name):
    return random.Random(core.hash_str(name))


def hull_col(ss, mat=None):
    """One convex collision component round the given solids' vertices (Geometry + View + Fire)."""
    pts = [v for s in ss for v in s.verts]
    return hull3(pts, mat or ss[0].main_mat())


def hull3(pts, mat, geo=True, view=True, fire=True):
    """Convex hull of 3D points as a closed Solid (gift-wrapping by brute force over triples; fine for <= 60 pts)."""
    P = [tuple(round(c, 5) for c in p) for p in pts]
    P = sorted(set(P))
    if len(P) > 60:
        # reduce: keep extreme points along 26 directions + bbox corners
        dirs = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if (a, b, c) != (0, 0, 0)]
        dirs += [(math.cos(k * math.pi / 8), 0.3 * s, math.sin(k * math.pi / 8)) for k in range(16) for s in (-1, 1)]
        keep = set()
        for d in dirs:
            keep.add(max(P, key=lambda p: p[0] * d[0] + p[1] * d[1] + p[2] * d[2]))
        P = sorted(keep)
    faces = []
    n = len(P)
    cen = tuple(sum(p[k] for p in P) / n for k in range(3))
    seen = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                nr = core.cross(core.sub(P[j], P[i]), core.sub(P[k], P[i]))
                if core.length(nr) < 1e-9:
                    continue
                nr = core.norm(nr)
                d = [core.dot(core.sub(p, P[i]), nr) for p in P]
                if max(d) <= 1e-6:
                    pass
                elif min(d) >= -1e-6:
                    nr = core.mul(nr, -1.0)
                else:
                    continue
                key = tuple(round(c, 4) for c in nr) + (round(core.dot(nr, P[i]), 4),)
                if key in seen:
                    continue
                seen.add(key)
                on = [m for m in range(n) if abs(core.dot(core.sub(P[m], P[i]), nr)) < 1e-6]
                # order the coplanar points round their centroid
                c = tuple(sum(P[m][q] for m in on) / len(on) for q in range(3))
                a = core.norm(core.sub(P[on[0]], c))
                b = core.cross(nr, a)
                on.sort(key=lambda m: math.atan2(core.dot(core.sub(P[m], c), b), core.dot(core.sub(P[m], c), a)))
                # drop collinear points
                ring = []
                for idx, m in enumerate(on):
                    pa, pb = P[on[idx - 1]], P[on[(idx + 1) % len(on)]]
                    if core.length(core.cross(core.sub(P[m], pa), core.sub(pb, P[m]))) > 1e-9:
                        ring.append(m)
                if len(ring) >= 3:
                    faces.append(ring)
    s = Solid(P, faces, mat, vis=(), geo=geo, view=view, fire=fire)
    s.center = cen
    s.finalize()
    return s


def spoked_wheel(r, width, hub_r, spokes, mat=WOOD, tyre=IRON, vis=(1,), n=16, wear=None):
    """A wooden spoked wheel in the x = 0 plane (axle along x), centre at the origin: felloe ring + iron tyre as a
    lathe band, hub, flat spokes."""
    out = []
    felloe = lathe([(r - 0.06, -width / 2), (r - 0.012, -width / 2), (r - 0.012, width / 2), (r - 0.06, width / 2),
                    (r - 0.06, -width / 2)], n, mat, vis=vis, smooth=False)
    tyre_s = lathe([(r - 0.012, -width / 2 - 0.004), (r, -width / 2 - 0.004), (r, width / 2 + 0.004),
                    (r - 0.012, width / 2 + 0.004)], n, tyre, vis=vis, smooth=True)
    hub = lathe([(0.0, -0.12), (hub_r, -0.12), (hub_r * 1.1, 0.0), (hub_r, 0.12), (0.0, 0.12)], 8, mat, vis=vis)
    for s in (felloe, tyre_s, hub):
        out.append(xf(s, rz=90.0))       # lathe axis y -> x
    for k in range(spokes):
        a = 2 * math.pi * k / spokes
        p0 = (0.0, hub_r * 0.9 * math.cos(a), hub_r * 0.9 * math.sin(a))
        p1 = (0.0, (r - 0.05) * math.cos(a), (r - 0.05) * math.sin(a))
        out.append(beam(p0, p1, 0.022, 0.045, mat, up=(1.0, 0.0, 0.0), vis=vis))
    if wear:
        for s in out:
            s.wear = wear
    return out


def wheel_lod(r, width, mat=WOOD, vis=(2,), n=8):
    """A wheel as one flat disc (lower LODs)."""
    s = lathe([(0.0, -width / 2), (r, -width / 2), (r, width / 2), (0.0, width / 2)], n, mat, vis=vis, smooth=False)
    return xf(s, rz=90.0)
