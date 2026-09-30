"""fkit - the B3a furniture kit: helpers shared by every jp_f_ prop builder (interior props, wave 1).

Built on the parts kit (parts/kit/jpparts/core.py: Solid, Part, the LOD writer); nothing in parts/ is modified.

Prop frame (PLAYBOOK §10.4, BUILD_LIST 'Engine notes'): origin = base centre on the supporting floor, +y up,
+z = the prop's front, autocenter=0. Two exceptions, recorded per model in the sidecar ('anchor'):
  'wall'  wall-hung (tana): origin on the floor below the shelf, the wall plane is z = 0, the shelf runs to +z
  'hang'  hanging (jizai-kagi): origin at the hook-beam underside, the prop hangs down (-y)

A model is an FPart: a core.Part plus
  .loot      loot surfaces for the sidecar [{name, kind shelf|floor, y, rect [x0,z0,x1,z1], range, points}]
  .anchor    'floor' | 'wall' | 'hang'
  .budget    'furniture' (<=1000 faces Res 1) | 'small' (<=300), PLAYBOOK §12
  .res3      True for standard-level props (Res 1-3, as vanilla furniture); filler props get Res 1-2
  .mass      kg (Geometry)
  .flat      True: visual only (mats, litter): no Geometry / View / Fire (BUILD_LIST Q5 rule 1)
Per-solid wear: solid.wear = '_w0'|'_w1'|'_w2' overrides the part wear. Dust: up-facing faces of the DUSTY
materials use _w2 (the effort-test tansu rule), unless solid.no_dust.
"""
import copy
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import core, mlod  # noqa: E402
from jpparts.core import box, prism, ngon, sheet, hexa, Solid, rot_y  # noqa: E402,F401

# ------------------------------------------------------------------------------------------------ materials
WOOD = "wood_interior"          # timber_interior: every furniture body (BUILD_LIST material table)
IRON = "metal_iron"
DARK = "ceramic_stoneware_dark"
PALE = "ceramic_stoneware_pale"
HOOP = "bamboo_weathered"
SOOT_BAMBOO = "bamboo_sooted"
SOOT_WOOD = "wood_sooted"
RIVER = "stone_river"
LOGWOOD = "wood_weathered"
ENDGRAIN = "wood_endgrain"
TAWARA = "straw_tawara"
MUSHIRO = "straw_mushiro"
PAPER = "paper_shoji"
FUSUMA = "paper_fusuma"
ASH = "ground_ash"
INDIGO = "textile_cotton_indigo"
KINARI = "textile_cotton_plain"
LACQUER = "lacquer_black"
WEAVE = "bamboo_weave"
LITTER = "decal_litter"

DUSTY = {WOOD, LACQUER, DARK, PALE}   # up faces of these take the dusty wear

BUDGET = {"furniture": 1000, "small": 300}


def add_smooth_face(lod, pts, outward, uvs, vns, texture, material):
    """As mlod.Lod.add_flat_face, but with per-vertex (smooth) normals. MLOD stores normals pointing inward."""
    pts = [tuple(float(c) for c in p) for p in pts]
    n = mlod._face_formula_normal(pts)
    uvs, vns = list(uvs), list(vns)
    if core.dot(n, outward) > 0:
        pts, uvs, vns = pts[::-1], uvs[::-1], vns[::-1]
    verts = []
    for p, uv, vv in zip(pts, uvs, vns):
        pi = lod.add_point(p)
        ni = lod.add_normal(core.mul(core.norm(vv), -1.0))
        verts.append((pi, ni, uv[0], uv[1]))
    return lod.add_face(verts, texture, material)


class FPart(core.Part):
    def __init__(self, name, budget="small", res3=False, mass=5.0, anchor="floor", flat=False, wear="_w1"):
        super().__init__(name)
        self.floors = []
        self.wear = wear
        self.loot = []
        self.budget = budget
        self.res3 = res3
        self.mass = mass
        self.anchor = anchor
        self.flat = flat
        self.notes = []
        self.extra = {}

    # -------------------------------------------------------------- wear
    def face_wear(self, s, fi):
        w = getattr(s, "wear", None)
        if w:
            return w
        m = s.fm[fi]
        if m in DUSTY and s.fn[fi][1] > 0.5 and not getattr(s, "no_dust", False):
            return "_w2"
        return self.wear_of(m)

    def _visual(self, k):
        lod = mlod.Lod(float(k))
        for s in self.solids:
            if k not in s.vis:
                continue
            vn = getattr(s, "vn", None)
            for fi in range(len(s.faces)):
                m = s.fm[fi]
                w = self.face_wear(s, fi)
                if vn is None:
                    lod.add_flat_face(s.face_points(fi), s.fn[fi], s.fuv[fi], core.tex_path(m, w),
                                      core.rvmat_path(m, w))
                else:
                    add_smooth_face(lod, s.face_points(fi), s.fn[fi], s.fuv[fi], vn[fi], core.tex_path(m, w),
                                    core.rvmat_path(m, w))
        return lod

    def lods(self, geo_props=None, mass=None):
        out = super().lods({"autocenter": "0"}, self.mass)
        return [l for l in out if not mlod.same_res(l.resolution, mlod.LOD_MEMORY)]

    # -------------------------------------------------------------- loot
    def loot_rect(self, name, y, x0, x1, z0, z1, rng=0.2, kind="shelf", per=0.9, points=None):
        """A loot surface. Points: 1 per `per` m along the longer side (BUILD_LIST: '1 point per 0.9 m')."""
        if points is None:
            lx, lz = x1 - x0, z1 - z0
            n = max(1, int(round(max(lx, lz) / per)))
            if lx >= lz:
                points = [(x0 + lx * (i + 0.5) / n, y, (z0 + z1) / 2) for i in range(n)]
            else:
                points = [((x0 + x1) / 2, y, z0 + lz * (i + 0.5) / n) for i in range(n)]
        self.loot.append({"name": name, "kind": kind, "y": round(y, 4),
                          "rect": [round(v, 4) for v in (x0, z0, x1, z1)], "range": rng,
                          "points": [[round(c, 4) for c in p] for p in points]})


# ------------------------------------------------------------------------------------------------ solids
def W(x0, x1, y0, y1, z0, z1, mat=WOOD, vis=(1, 2), **kw):
    return box(x0, x1, y0, y1, z0, z1, mat, vis=vis, **kw)


def col(x0, x1, y0, y1, z0, z1, mat=WOOD, fire=True):
    """Collision box: Geometry + View + Fire component, no visual faces."""
    return box(x0, x1, y0, y1, z0, z1, mat, vis=(), geo=True, view=True, fire=fire)


def col_solid(s, mat=None):
    """Turn a closed convex solid into a collision-only component (copy)."""
    c = copy.copy(s)
    c.vis = set()
    c.geo = c.view = True
    c.fire = True
    if mat:
        c.mats = mat
        c.fm = None
        c.finalize()
    return c


def _rotm(rx=0.0, ry=0.0, rz=0.0):
    """Rotation matrix: about x, then z, then y (degrees)."""
    def mx(a):
        c, s = math.cos(a), math.sin(a)
        return [[1, 0, 0], [0, c, -s], [0, s, c]]

    def my(a):
        c, s = math.cos(a), math.sin(a)
        return [[c, 0, -s], [0, 1, 0], [s, 0, c]]     # same sense as core.rot_y (+x -> +z for +90)

    def mz(a):
        c, s = math.cos(a), math.sin(a)
        return [[c, -s, 0], [s, c, 0], [0, 0, 1]]

    def mm(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(my(math.radians(ry)), mm(mz(math.radians(rz)), mx(math.radians(rx))))


def _apply(m, p):
    return (m[0][0] * p[0] + m[0][1] * p[1] + m[0][2] * p[2],
            m[1][0] * p[0] + m[1][1] * p[1] + m[1][2] * p[2],
            m[2][0] * p[0] + m[2][1] * p[1] + m[2][2] * p[2])


def xf(s, rx=0.0, ry=0.0, rz=0.0, t=(0.0, 0.0, 0.0), pivot=(0.0, 0.0, 0.0)):
    """Copy of a solid rotated (x, then z, then y; degrees) about `pivot`, then moved by t. UVs stay glued."""
    s.finalize()
    m = _rotm(rx, ry, rz)
    n = copy.copy(s)
    f = lambda p: core.add(core.add(_apply(m, core.sub(p, pivot)), pivot), t)   # noqa: E731
    n.verts = [f(v) for v in s.verts]
    n.center = f(s.center)
    n.fn = [_apply(m, q) for q in s.fn]
    if getattr(s, "vn", None) is not None:
        n.vn = [[_apply(m, q) for q in f] for f in s.vn]
    if s.normals is not None:
        n.normals = n.fn
    n.faces = [list(ff) for ff in s.faces]
    for k in ("wear", "no_dust", "tag"):
        if hasattr(s, k):
            setattr(n, k, getattr(s, k))
    return n


def xfs(ss, **kw):
    return [xf(s, **kw) for s in ss]


def lathe(profile, n, mat, vis=(1, 2), phase=None, tile=None, tag="", wear=None, closed_ends=True, skip=(),
          smooth=True):
    """Surface of revolution about +y. profile = [(r, y), ...] traversed so the material is on the left
    (e.g. up the outside, over the rim, down the inside). Visual only (explicit outward normals).
    Cylindrical UVs: u around (metres of mean circumference / tile), v along the profile."""
    ph = math.pi / n if phase is None else phase
    t = tile or core.mat_info(mat)["tile"]
    angs = [ph + 2 * math.pi * k / n for k in range(n + 1)]
    quads, normals, uvs = [], [], []
    vacc = [0.0]
    for i in range(len(profile) - 1):
        (r0, y0), (r1, y1) = profile[i], profile[i + 1]
        vacc.append(vacc[-1] + math.hypot(r1 - r0, y1 - y0))
    for i in range(len(profile) - 1):
        (r0, y0), (r1, y1) = profile[i], profile[i + 1]
        dr, dy = r1 - r0, y1 - y0
        L = math.hypot(dr, dy) or 1.0
        nr, ny = dy / L, -dr / L
        rm = max((r0 + r1) / 2, 0.02)
        for k in range(n):
            if k in skip:
                continue
            a0, a1 = angs[k], angs[k + 1]
            am = (a0 + a1) / 2
            p = [(r0 * math.cos(a0), y0, r0 * math.sin(a0)), (r0 * math.cos(a1), y0, r0 * math.sin(a1)),
                 (r1 * math.cos(a1), y1, r1 * math.sin(a1)), (r1 * math.cos(a0), y1, r1 * math.sin(a0))]
            u0, u1 = rm * a0 / t, rm * a1 / t
            v0, v1 = vacc[i] / t, vacc[i + 1] / t
            uv = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
            if r0 < 1e-6:
                p, uv = [p[0], p[2], p[3]], [uv[0], uv[2], uv[3]]
            elif r1 < 1e-6:
                p, uv = [p[0], p[1], p[2]], [uv[0], uv[1], uv[2]]
            quads.append(p)
            normals.append((nr * math.cos(am), ny, nr * math.sin(am)))
            uvs.append(uv)
    s = sheet(quads, mat, normals, vis=vis, uvs=uvs, tag=tag)
    if smooth:
        # per profile vertex: the normals of its two segments, averaged unless they crease more than 50 deg
        segn = []
        for i in range(len(profile) - 1):
            (r0, y0), (r1, y1) = profile[i], profile[i + 1]
            L = math.hypot(r1 - r0, y1 - y0) or 1.0
            segn.append(((y1 - y0) / L, -(r1 - r0) / L))

        def vnorm(i, seg):
            a = segn[seg]
            other = seg - 1 if i == seg else seg + 1
            if 0 <= other < len(segn):
                b = segn[other]
                if a[0] * b[0] + a[1] * b[1] > math.cos(math.radians(50)):
                    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            return a
        vn = []
        fi = 0
        for i in range(len(profile) - 1):
            (r0, _), (r1, _) = profile[i], profile[i + 1]
            n0, n1 = vnorm(i, i), vnorm(i + 1, i)
            for k in range(n):
                if k in skip:
                    continue
                a0, a1 = angs[k], angs[k + 1]
                q = [(n0[0] * math.cos(a0), n0[1], n0[0] * math.sin(a0)), (n0[0] * math.cos(a1), n0[1], n0[0] * math.sin(a1)),
                     (n1[0] * math.cos(a1), n1[1], n1[0] * math.sin(a1)), (n1[0] * math.cos(a0), n1[1], n1[0] * math.sin(a0))]
                if r0 < 1e-6:
                    q = [q[0], q[2], q[3]]
                elif r1 < 1e-6:
                    q = [q[0], q[1], q[2]]
                vn.append(q)
                fi += 1
        s.finalize()
        s.vn = vn
    if wear:
        s.wear = wear
    return s


def lcyl(axis, c0, c1, r, t0, t1, mat, n=6, vis=(1, 2), caps=None, phase=None, **kw):
    """Closed round member (log, bale, pole). caps = material for the two end faces (e.g. end grain)."""
    s = core.cyl(axis, c0, c1, r, t0, t1, mat, n=n, phase=phase, vis=vis, **kw)
    if caps:
        ax = {"x": ("left", "right"), "y": ("top", "bottom"), "z": ("front", "back")}[axis]
        s.mats = {ax[0]: caps, ax[1]: caps, "default": mat}
        s.fm = None
        s.finalize()
    return s


def flat_poly(pts_xz, y, mat, vis=(1, 2), wear=None, tag="", uvoff=(0.0, 0.0), tile=None):
    """Up-facing flat polygon at height y (decals, mats). Convex pts [(x, z)] counter-clockwise from above."""
    pts = [(x, y, z) for x, z in pts_xz]
    t = tile or core.mat_info(mat)["tile"]
    uv = [(x / t + uvoff[0], z / t + uvoff[1]) for x, z in pts_xz]
    s = sheet([pts], mat, (0.0, 1.0, 0.0), vis=vis, uvs=[uv], tag=tag)
    s.finalize()
    if wear:
        s.wear = wear
    return s


def band_fit(s, lo_px, hi_px, normal=(0.0, 0.0, 1.0), tex_px=1024, voff=0.0):
    """Remap u of the faces facing `normal` into the clean texture band [lo_px, hi_px] (between plank grooves),
    so a small board face shows no plank seam. Stretches across the grain only."""
    s.finalize()
    lo, hi = lo_px / tex_px, hi_px / tex_px
    for fi in range(len(s.faces)):
        if core.dot(s.fn[fi], normal) > 0.9:
            us = [a for a, b in s.fuv[fi]]
            u0, u1 = min(us), max(us)
            span = (u1 - u0) or 1.0
            s.fuv[fi] = [(lo + (a - u0) / span * (hi - lo), b + voff) for a, b in s.fuv[fi]]
    return s


# wood_interior (_w0/_w1/_w2) plank grooves every ~78.7 px (measured in the _co maps): clean bands between them
WOOD_BANDS = [(86, 150), (165, 229), (243, 307), (322, 386), (400, 465), (479, 543), (558, 622), (637, 701),
              (716, 780), (794, 858), (873, 937)]


def board(x0, x1, y0, y1, z0, z1, k=0, mat=WOOD, vis=(1, 2), normals=((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0),
                                                                   (1, 0, 0), (-1, 0, 0)), **kw):
    """A single board: every face mapped into one clean plank band (no seam across a single board)."""
    s = W(x0, x1, y0, y1, z0, z1, mat, vis=vis, **kw)
    b = WOOD_BANDS[k % len(WOOD_BANDS)]
    for nn in normals:
        band_fit(s, b[0], b[1], nn, voff=0.137 * k)
    return s


def road_tops(P, cols, surf="boards", others=None, min_area=0.004):
    """F1 (G4 walk: 'the goods stand can't be walked on, glitches when you clip on top'): a Roadway on the flat
    up-facing faces of the given collision components, as vanilla gives tables, desks, benches, beds, shelves and
    carts one (their Roadway LOD). A top face whose centre is inside another collision component (a bale under the
    next bale, a box under the next box) is skipped. surf = a core.ROADWAY key ('boards' = wood_planks_int, 'boards_ext',
    'tatami' = textile_carpet_int for straw and cloth). Returns how many faces it added."""
    others = list(others if others is not None else cols)
    k = 0
    for c in cols:
        c.finalize()
        for fi, f in enumerate(c.faces):
            if c.fn[fi][1] < 0.999:
                continue
            pts = [c.verts[i] for i in f]
            n = core.newell(pts)
            if 0.5 * core.length(n) < min_area:
                continue
            cen = tuple(sum(p[q] for p in pts) / len(pts) for q in range(3))
            probe = (cen[0], cen[1] + 0.02, cen[2])
            covered = False
            for o in others:
                if o is c:
                    continue
                b = o.bbox()
                if b[0] < probe[0] < b[1] and b[2] < probe[1] < b[3] and b[4] < probe[2] < b[5]:
                    covered = True
                    break
            if covered:
                continue
            # MLOD roadway faces: counter-clockwise seen from above
            if n[1] < 0:
                pts = pts[::-1]
            P.road(pts, surf)
            k += 1
    return k


def pts_ring(r, n, y, phase=0.0, cx=0.0, cz=0.0):
    return [(cx + r * math.cos(phase + 2 * math.pi * k / n), y, cz + r * math.sin(phase + 2 * math.pi * k / n))
            for k in range(n)]


def cyl_col(r, y0, y1, n=8, cx=0.0, cz=0.0, mat=WOOD):
    """Convex n-gon collision prism about +y."""
    return prism(ngon(cx, cz, r, n, math.pi / n), "y", y0, y1, mat, vis=(), geo=True, view=True, fire=True)


def ring_band(r_in, r_out, y0, y1, mat, n, vis=(1, 2), wear=None):
    """A hoop / flange: closed annulus as a lathe (outside, top, inside, bottom)."""
    return lathe([(r_out, y0), (r_out, y1), (r_in, y1), (r_in, y0), (r_out, y0)], n, mat, vis=vis, wear=wear)


def rotated_box(cx, cz, w, d, y0, y1, yaw, mat, vis=(1, 2), **kw):
    """Axis box of w (x) by d (z) centred at (cx, cz), yawed about +y (degrees)."""
    s = W(-w / 2, w / 2, y0, y1, -d / 2, d / 2, mat, vis=vis, **kw)
    return xf(s, ry=yaw, t=(cx, 0.0, cz))


def rest(ss, y=0.0):
    """Move a group of solids up/down so its lowest vertex sits at y (a lid leaning on the floor)."""
    lo = min(v[1] for s in ss for v in s.verts)
    return [xf(s, t=(0.0, y - lo, 0.0)) for s in ss]


def auto_smooth(s, crease=60.0):
    """Per-vertex smooth normals for any solid: average the normals of the faces meeting at a vertex position
    whose normal is within `crease` degrees of this face's (a hard edge stays hard)."""
    s.finalize()
    key = lambda p: (round(p[0], 4), round(p[1], 4), round(p[2], 4))   # noqa: E731
    at = {}
    for fi, f in enumerate(s.faces):
        for vi in f:
            at.setdefault(key(s.verts[vi]), []).append(fi)
    cc = math.cos(math.radians(crease))
    vn = []
    for fi, f in enumerate(s.faces):
        nf = s.fn[fi]
        row = []
        for vi in f:
            acc = (0.0, 0.0, 0.0)
            for fj in at[key(s.verts[vi])]:
                if core.dot(s.fn[fj], nf) >= cc:
                    acc = core.add(acc, s.fn[fj])
            row.append(core.norm(acc))
        vn.append(row)
    s.vn = vn
    return s
