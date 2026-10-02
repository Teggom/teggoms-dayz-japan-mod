"""Strip roofs on the ken grid (agent K3, 2026-10-01; parts/K3_NOTES.md): ONE engine for the wall caps of the wall kit
(sitewall.py) and the roofs of the covered-corridor / kairo kit (roka.py).

A strip roof covers a band of width D between two bearing lines (a corridor's post lines, a wall's two faces) with an
eave overhang `ov` past each, ridge on the centreline. Modules butt on the grid:

    straight(part, S, L, ends=("seam", "gable"), branches=((1, "+z"),))   # along x 0..L, centreline z = 0
    junction(part, S, arms=("-x", "+z"))                                   # corner / T / cross cell centred on (0, 0)

ends: "seam" (the next module continues: nothing drawn at the cut), "gable" (verge `gov` past the end: hafu boards,
verge tiles, ridge-end tile / small oni), "hip" (a hipped end, eave `ov` past the end). branches: (end 0 | 1, "+z" |
"-z"): a junction cell sits past that end with an arm leaving to that side; the module's front / back overhang next to
it is cut on the VALLEY line (the branch module and the junction build the rest), so modules never overlap.

How the surface is defined: every eave line e (point o, inward normal n) gives f_e(p) = (p - o) . n, the plan distance
in from that eave. A corridor's profile is the MIN over its eaves (its two sides + any end where it stops); the roof is
the MAX over the corridors present (two at a junction): d(p) = max_c min_e f_e(p). The min makes ridges and hips, the max
makes valleys, and every module evaluates the same function, so ridges, hips and valleys meet across module joints.
Height: y(p) = yb + E(d), E(d) = t d (straight) or W2P2's sori profile E(d) = t0 d + (t1 - t0) R/(p+1) (d/R)^(p+1)
(curved, R = D/2 + ov), bearing line at y_bear. Curved roofs are built in d-bands with planar faces per band; band
breaks depend on d only, so neighbouring facets stay continuous.

Layers per facet (y measured up from the rafter-underside plane y_r(p), as roofs.py): rafters 0 .. 0.06 (open roofs: the
whole span, R1; caps: the overhang only), sheathing 0.06 .. 0.072 (tag 'sheathing'), tile bed (tag 'tile_bed', T1)
0.072 .. stack-0.004, tile field from `stack` (kawara.field, clipped in plan to the facet: hips and valleys cut it),
eave tiles + fascia (C13), far-material slab R2/R3 (C16); board roofs: a board sheet with stepped eave courses, the
thick eave edge in every LOD. Collision: one convex slab per facet (per band) rafter plane .. covering top (tag
'roof_geo_<name>'), Roadway on top when walkable. Caps (body='solid'): inside the bearing lines the collision and a
clay bed go down to y_solid (the wall top).
"""
import math

from .core import Solid, box, hexa, KEN, HALF, rng_for, add, sub, mul, norm, cross, dot, mat_info, LIBRARY
from .shapes import slab, clip_poly, clean_poly, oriented_box, frame_of, tube
from . import kawara as K

EPS = 1e-6
GROW = 0.12            # the covering's clip region runs this far past an eave (eave tiles hang 0.06 over)

FAMILIES = {
    # kind, default pitch, stack (covering base over the rafter plane), covering top over the base, fire, Roadway
    "sangawara": dict(kind="tile", t=0.45, stack=0.152, top=0.05, fire="pottery", surf="tile_roof"),
    "hongawara": dict(kind="tile", t=0.45, stack=0.152, top=0.06, fire="pottery", surf="tile_roof", hong=True),
    "itabuki": dict(kind="board", t=0.40, stack=0.084, top=0.012, fire="wood", surf="board_roof", mat="roof_kokera"),
    "kokera": dict(kind="board", t=0.42, stack=0.084, top=0.016, fire="wood", surf="board_roof", mat="roof_kokera"),
    "hiwada": dict(kind="board", t=0.42, stack=0.084, top=0.016, fire="wood", surf="board_roof",
                   mat="roof_hiwada" if "roof_hiwada" in LIBRARY else "roof_kureita"),
    "kureita": dict(kind="board", t=0.36, stack=0.084, top=0.014, fire="wood", surf="board_roof", mat="roof_kureita"),
}


class Spec:
    """Strip-roof parameters.
    D        width between the bearing lines (corridor post centres, or the wall top width)
    ov       eave overhang past a bearing line (plan); gov: verge overhang past a gable end
    y_bear   rafter-underside plane height at the bearing line
    family   sangawara | hongawara | itabuki | kokera | hiwada | kureita
    profile  'straight' (pitch t) | 'sori' (t0, t1, p: W2P2's curve)
    body     'open' (corridor: underside seen, rafters across the span) | 'solid' (cap: bed + collision down to y_solid)
    """

    def __init__(self, D, ov, y_bear, family="sangawara", profile="straight", t=None, sori=(0.30, 0.70, 1.6),
                 gov=0.30, body="open", y_solid=None, walkable=True, rafter_sp=0.303, rafter_sec=(0.045, 0.06),
                 courses=3, wood="wood_weathered", bed_mat=None, oni=True, ridge_w=None, fire=True):
        self.D, self.ov, self.y_bear, self.gov = D, ov, y_bear, gov
        self.fam = FAMILIES[family]
        self.family = family
        self.kind = self.fam["kind"]
        self.profile = profile
        self.t = self.fam["t"] if t is None else t
        self.t0, self.t1, self.p = sori
        self.R = D / 2 + ov
        self.body = body
        self.y_solid = y_solid
        self.walkable = walkable
        self.sp, self.sec = rafter_sp, rafter_sec
        self.courses = courses
        self.wood = wood
        self.bed_mat = bed_mat or "wall_arakabe"
        self.oni = oni
        self.ridge_w = ridge_w or (0.22 if D < 1.2 else 0.26)
        self.stack = self.fam["stack"]
        self.top = self.fam["top"]
        self.fire = self.fam["fire"] if fire else None
        self.yb = y_bear - self.E(ov)

    def E(self, d):
        if self.profile == "straight":
            return self.t * d
        if d <= 0:
            return self.t0 * d
        R = self.R
        return self.t0 * d + (self.t1 - self.t0) * R / (self.p + 1) * (d / R) ** (self.p + 1)

    def y(self, d, h=0.0):
        return self.yb + self.E(d) + h

    def breaks(self):
        """d band breaks (planar bands). Straight: one band."""
        top = self.R + 0.02
        if self.profile == "straight":
            return [-1.0, top + 1.0]
        out = [-1.0, 0.0]
        d = 0.0
        step = max(0.30, min(0.55, self.R / 4))
        while d + step < top - 0.15:
            d += step
            out.append(d)
        out.append(top + 1.0)
        return out

    def ridge_y(self):
        return self.y(self.R)


# ------------------------------------------------------------------------------------------------ plan maths
def _f(e, x, z):
    return (x - e[0]) * e[2] + (z - e[1]) * e[3]


def _same(e1, e2):
    return (abs(e1[2] - e2[2]) < 1e-6 and abs(e1[3] - e2[3]) < 1e-6 and
            abs((e1[0] * e1[2] + e1[1] * e1[3]) - (e2[0] * e2[2] + e2[1] * e2[3])) < 1e-6)


def _le(poly, e1, e2):
    """Keep f_e1 <= f_e2."""
    a, b = e1[2] - e2[2], e1[3] - e2[3]
    c = (e1[0] * e1[2] + e1[1] * e1[3]) - (e2[0] * e2[2] + e2[1] * e2[3])
    if abs(a) < 1e-12 and abs(b) < 1e-12:
        return list(poly) if -c <= 1e-9 else []
    return clip_poly(poly, a, b, c)


def _area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly))) / 2


def _intersect(A, B):
    s = 1.0 if _area(B) > 0 else -1.0
    out = list(A)
    for i in range(len(B)):
        p, q = B[i], B[(i + 1) % len(B)]
        a = (q[1] - p[1]) * s
        b = -(q[0] - p[0]) * s
        c = ((q[1] - p[1]) * p[0] - (q[0] - p[0]) * p[1]) * s
        out = clip_poly(out, a, b, c)
        if len(out) < 3:
            return []
    return out


def _ok(poly):
    return poly and len(poly) >= 3 and abs(_area(poly)) > 2e-5


def rect(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def pieces(region, corridors):
    """Convex pieces [(poly, eave, corridor index)] where d(p) = max_c min_e f_e(p) equals f_eave(p)."""
    def cells(ci):
        c = corridors[ci]
        out = []
        for i, e in enumerate(c):
            poly = list(region)
            for j, e2 in enumerate(c):
                if j != i and not _same(e, e2):
                    poly = _le(poly, e, e2)
                    if len(poly) < 3:
                        break
            # two identical eaves (a shared line): the first one owns it
            if any(_same(e, c[j]) for j in range(i)):
                continue
            if _ok(poly):
                out.append((poly, e, ci))
        return out
    cur = cells(0)
    for ci in range(1, len(corridors)):
        nxt = []
        for (pA, eA, cA) in cur:
            for (pB, eB, cB) in cells(ci):
                inter = _intersect(pA, pB)
                if not _ok(inter):
                    continue
                if _same(eA, eB):
                    nxt.append((inter, eA, cA))
                    continue
                a = _le(inter, eB, eA)               # eA active (eB <= eA)
                if _ok(a):
                    nxt.append((a, eA, cA))
                b = _le(inter, eA, eB)               # eB active
                if _ok(b):
                    nxt.append((b, eB, cB))
        cur = nxt
    return cur


def eave(o, n):
    return (float(o[0]), float(o[1]), float(n[0]), float(n[1]))


def udir(e):
    """Unit vector along the eave (u): the inward normal turned 90 deg (front eave n (0, -1) -> u = +x)."""
    return (-e[3], e[2])


# ------------------------------------------------------------------------------------------------ sheet clipping
def _clip_attr(pts, a, b, c):
    """Sutherland-Hodgman in plan on points (x, y, z, u, v): keep a x + b z <= c."""
    out = []
    n = len(pts)
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        fp = a * p[0] + b * p[2] - c
        fq = a * q[0] + b * q[2] - c
        if fp <= 1e-9:
            out.append(p)
        if (fp < -1e-9 and fq > 1e-9) or (fp > 1e-9 and fq < -1e-9):
            t = fp / (fp - fq)
            out.append(tuple(p[k] + t * (q[k] - p[k]) for k in range(5)))
    res = []
    for p in out:
        if not res or max(abs(p[k] - res[-1][k]) for k in (0, 1, 2)) > 1e-6:
            res.append(p)
    if len(res) > 1 and max(abs(res[0][k] - res[-1][k]) for k in (0, 1, 2)) < 1e-6:
        res.pop()
    return res


def _poly_planes(poly):
    s = 1.0 if _area(poly) > 0 else -1.0
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        out.append(((q[1] - p[1]) * s, -(q[0] - p[0]) * s, ((q[1] - p[1]) * p[0] - (q[0] - p[0]) * p[1]) * s))
    return out


def clip_sheets(solids, poly, part, tag=None):
    """Clip open visual sheets (explicit uv lists + normal hints) to a convex plan polygon and add them to `part`."""
    planes = _poly_planes(poly)
    for s in solids:
        if not s.vis and not s.geo:
            continue
        if s.closed:
            # closed solids: keep when the centre is inside (small pieces: eave strip blocks are re-made per piece)
            cx, cz = s.center[0], s.center[2]
            if all(a * cx + b * cz <= c + 1e-6 for a, b, c in planes):
                part.add(s)
            continue
        s.finalize()
        verts, faces, uvs, nrm = [], [], [], []
        for fi, f in enumerate(s.faces):
            pts = [s.verts[i] + tuple(s.fuv[fi][k]) for k, i in enumerate(f)]
            for a, b, c in planes:
                pts = _clip_attr(pts, a, b, c)
                if len(pts) < 3:
                    break
            if len(pts) < 3:
                continue
            # drop slivers
            ar = 0.0
            for i in range(1, len(pts) - 1):
                ar += length_(cross(sub(pts[i][:3], pts[0][:3]), sub(pts[i + 1][:3], pts[0][:3])))
            if ar < 2e-6:
                continue
            faces.append(list(range(len(verts), len(verts) + len(pts))))
            verts += [p[:3] for p in pts]
            uvs.append([(p[3], p[4]) for p in pts])
            nrm.append(s.fn[fi])
        if faces:
            ns = Solid(verts, faces, s.mats if isinstance(s.mats, str) else s.fm[0], vis=s.vis, uv=uvs, normals=nrm,
                       tag=tag or s.tag)
            part.add(ns)


def length_(v):
    return math.sqrt(dot(v, v))


# ------------------------------------------------------------------------------------------------ the builder
class _Tmp:
    """A throwaway part for kawara.field / eave_tiles output (they only need .add and .name)."""

    def __init__(self, name):
        self.name = name
        self.solids = []

    def add(self, s):
        s.finalize()
        self.solids.append(s)
        return s

    def extend(self, ss):
        for s in ss:
            self.add(s)


def _frame(S, e, da, db):
    """kawara SlopeFrame for the planar band da..db of eave e (u = absolute along the eave)."""
    ux, uz = -e[3], e[2]
    # the point on the eave line with u = 0
    o = (e[0], e[1])
    u0 = o[0] * ux + o[1] * uz
    q0 = (o[0] - ux * u0, o[1] - uz * u0)
    t = (S.E(db) - S.E(da)) / (db - da) if db > da else S.t
    org = (q0[0] + e[2] * da, S.y(da, S.stack), q0[1] + e[3] * da)
    return K.SlopeFrame(org, (ux, 0.0, uz), (e[2], 0.0, e[3]), t), t


def _band_fn(S, e, da, db, h):
    """Planar height over the band: linear in d between the band's ends (exact for straight roofs)."""
    ya, yb_ = S.y(da, h), S.y(db, h)
    k = (yb_ - ya) / (db - da) if db > da else S.t

    def fn(x, z):
        return ya + k * (_f(e, x, z) - da)
    return fn


def _u_range(poly, e):
    ux, uz = -e[3], e[2]
    us = [x * ux + z * uz for x, z in poly]
    return min(us), max(us)


def _d_range(poly, e):
    ds = [_f(e, x, z) for x, z in poly]
    return min(ds), max(ds)


def _d_interval_at_u(poly, e, u):
    """d-interval of the line {u = const} inside a convex plan polygon (None if it misses)."""
    ux, uz = -e[3], e[2]
    lo, hi = 1e9, -1e9
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        up, uq = p[0] * ux + p[1] * uz, q[0] * ux + q[1] * uz
        if (up - u) * (uq - u) > 0 and abs(up - u) > 1e-9 and abs(uq - u) > 1e-9:
            continue
        if abs(uq - up) < 1e-9:
            for r in (p, q):
                if abs(r[0] * ux + r[1] * uz - u) < 1e-6:
                    d = _f(e, r[0], r[1])
                    lo, hi = min(lo, d), max(hi, d)
            continue
        t = (u - up) / (uq - up)
        if -1e-9 <= t <= 1 + 1e-9:
            x, z = p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])
            d = _f(e, x, z)
            lo, hi = min(lo, d), max(hi, d)
    return (lo, hi) if hi > lo + 1e-4 else None


def _bands(S, poly, e):
    out = []
    br = S.breaks()
    for da, db in zip(br[:-1], br[1:]):
        b = clip_poly(poly, e[2], e[3], db + e[0] * e[2] + e[1] * e[3])          # f <= db
        if len(b) >= 3:
            b = clip_poly(b, -e[2], -e[3], -(da + e[0] * e[2] + e[1] * e[3]))     # f >= da
        if _ok(b):
            dlo, dhi = _d_range(b, e)
            out.append((b, max(da, dlo), min(db, dhi)))
    return out


def _edges_shared(P, Q, eps=2e-5):
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        ab = (b[0] - a[0], b[1] - a[1])
        L2 = ab[0] ** 2 + ab[1] ** 2
        if L2 < 1e-10:
            continue
        L = math.sqrt(L2)
        for j in range(len(Q)):
            c, d = Q[j], Q[(j + 1) % len(Q)]
            dist_c = abs(ab[0] * (c[1] - a[1]) - ab[1] * (c[0] - a[0])) / L
            dist_d = abs(ab[0] * (d[1] - a[1]) - ab[1] * (d[0] - a[0])) / L
            if dist_c > eps or dist_d > eps:
                continue
            tc = ((c[0] - a[0]) * ab[0] + (c[1] - a[1]) * ab[1]) / L2
            td = ((d[0] - a[0]) * ab[0] + (d[1] - a[1]) * ab[1]) / L2
            t0, t1 = max(0.0, min(tc, td)), min(1.0, max(tc, td))
            if (t1 - t0) * L > 1e-3:
                out.append(((a[0] + ab[0] * t0, a[1] + ab[1] * t0), (a[0] + ab[0] * t1, a[1] + ab[1] * t1)))
    return out


def _centroid(poly):
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


def _merge_lines(segs):
    """Merge collinear touching / overlapping plan segments (each a tuple of two points)."""
    out = []
    used = [False] * len(segs)
    for i, (a, b) in enumerate(segs):
        if used[i]:
            continue
        used[i] = True
        a, b = list(a), list(b)
        changed = True
        while changed:
            changed = False
            for j, (c, d) in enumerate(segs):
                if used[j]:
                    continue
                ab = (b[0] - a[0], b[1] - a[1])
                L = math.hypot(*ab)
                if L < 1e-9:
                    break
                if any(abs(ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])) / L > 2e-5 for p in (c, d)):
                    continue
                ts = sorted([0.0, 1.0])
                tc = ((c[0] - a[0]) * ab[0] + (c[1] - a[1]) * ab[1]) / (L * L)
                td = ((d[0] - a[0]) * ab[0] + (d[1] - a[1]) * ab[1]) / (L * L)
                if max(tc, td) < -1e-4 or min(tc, td) > 1 + 1e-4:
                    continue
                lo, hi = min(0.0, tc, td), max(1.0, tc, td)
                na = (a[0] + ab[0] * lo, a[1] + ab[1] * lo)
                nb = (a[0] + ab[0] * hi, a[1] + ab[1] * hi)
                a, b = list(na), list(nb)
                used[j] = True
                changed = True
        out.append((tuple(a), tuple(b)))
    return out


def build(part, S, region, corridors, own=(0,), eave_sides=(), verges=(), name="roof", grow_sides=None):
    """Build the strip roof over `region` (convex plan polygon) for the corridors (lists of eaves); only pieces whose
    active corridor is in `own` are built (the rest belong to a neighbour module). verges: [(side_axis 'x', value,
    sign)] gable edges (x = value; sign -1 = the low-x end, +1 = the high-x end). Returns an info dict."""
    info = {"pieces": 0, "ridges": [], "hips": [], "valleys": [], "verges": list(verges)}
    exact = [p for p in pieces(region, corridors) if p[2] in own]
    # the covering's grown region (past the eaves)
    gx0, gx1 = min(p[0] for p in region), max(p[0] for p in region)
    gz0, gz1 = min(p[1] for p in region), max(p[1] for p in region)
    gs = grow_sides if grow_sides is not None else eave_sides
    grown_r = rect(gx0 - (GROW if "x0" in gs else 0.0), gx1 + (GROW if "x1" in gs else 0.0),
                   gz0 - (GROW if "z0" in gs else 0.0), gz1 + (GROW if "z1" in gs else 0.0))
    grown = [p for p in pieces(grown_r, corridors) if p[2] in own]
    allp = pieces(region, corridors)
    info["pieces"] = len(exact)
    geo_tag = "roof_geo_" + name
    surf = S.fam["surf"] if S.walkable else None
    tile = S.kind == "tile"
    # -------------------------------------------------------------- body: collision, sheathing, bed, far LODs
    for poly, e, ci in exact:
        for b, da, db in _bands(S, poly, e):
            # inside the bearing lines vs the overhang (d < ov) for solid caps
            zones = [(b, "all")]
            if S.body == "solid":
                inner = clip_poly(b, -e[2], -e[3], -(S.ov + e[0] * e[2] + e[1] * e[3]))      # f >= ov
                outer = clip_poly(b, e[2], e[3], S.ov + e[0] * e[2] + e[1] * e[3])           # f <= ov
                zones = [(z, k) for z, k in ((inner, "in"), (outer, "out")) if _ok(z)]
            top = _band_fn(S, e, da, db, S.stack + S.top)
            r0 = _band_fn(S, e, da, db, 0.0)
            sh0 = _band_fn(S, e, da, db, 0.06)
            sh1 = _band_fn(S, e, da, db, 0.072)
            bed = _band_fn(S, e, da, db, S.stack - 0.004)
            cov0 = _band_fn(S, e, da, db, S.stack - 0.012) if not tile else bed
            for z, kind in zones:
                ys = S.y_solid
                low = (lambda x, zz, v=ys: v) if kind == "in" else r0
                part.add(slab(z, low, top, S.wood, vis=(), geo=True, view=True, fire=S.fire, tag=geo_tag))
                if surf:
                    part.road([(x, top(x, zz), zz) for x, zz in z], surf)
                if kind == "in":
                    # the clay / plaster bed on the wall top under the covering (T1: no daylight under the tiles)
                    part.add(slab(z, low, bed if tile else cov0, S.bed_mat, vis=(1, 2, 3), tag="tile_bed"))
                    if tile:
                        part.add(slab(z, bed, lambda x, zz, f=bed: f(x, zz) + 0.004 + 0.05, K.far_mat(), vis=(2, 3),
                                      tag="kawara_far_body"))
                    else:
                        part.add(slab(z, cov0, lambda x, zz, f=top: f(x, zz) - 0.002, S.fam["mat"], vis=(2, 3),
                                      tag="board_field_lod"))
                    continue
                part.add(slab(z, sh0, sh1, {"bottom": S.wood, "default": S.wood}, vis=(1, 2, 3), tag="sheathing"))
                if tile:
                    part.add(slab(z, sh1, bed, R_BED, vis=(1,), tag="tile_bed"))
                    part.add(slab(z, sh1, lambda x, zz, f=bed: f(x, zz) + 0.004 + 0.05, K.far_mat(), vis=(2, 3),
                                  tag="kawara_far_body"))
                else:
                    part.add(slab(z, sh1, lambda x, zz, f=top: f(x, zz) - 0.002, S.fam["mat"], vis=(2, 3),
                                  tag="board_field_lod"))
    # -------------------------------------------------------------- covering (R1), clipped to the grown pieces
    vw = 0.13 if tile else 0.0
    for poly, e, ci in grown:
        cpoly = poly
        for (ax, val, sg) in verges:
            if tile:
                # the field stops `vw` inside the verge (the verge tiles take the edge)
                cpoly = clip_poly(cpoly, sg * 1.0, 0.0, sg * (val - sg * vw)) if sg > 0 else \
                    clip_poly(cpoly, -1.0, 0.0, -(val + vw))
        if not _ok(cpoly):
            continue
        u0, u1 = _u_range(poly, e)
        for b, da, db in _bands(S, cpoly, e):
            F, t = _frame(S, e, da, db)
            rl = (db - da) / F.cos
            first = da <= 1e-6
            tmp = _Tmp(part.name + name + "%.2f%.2f" % (da, u0))
            if tile:
                r0 = K.EXPO if first else 0.0
                if S.fam.get("hong"):
                    _hong_field(tmp, F, u0 - 0.4, u1 + 0.4, r0, rl + 0.05)
                else:
                    K.field(tmp, F, u0 - 0.4, u1 + 0.4, r0, rl + 0.05, lod_sets=((0, (1,)),),
                            rows_eave=2 if first else 0, rows_ridge=0)
                clip_sheets(tmp.solids, b, part)
                if first:
                    # eave tiles only along the exact eave segment (past a valley's foot or a hip corner they would
                    # stand out of the far LODs' eave strip, C15)
                    et = _Tmp(tmp.name + "e")
                    K.eave_tiles(et, F, u0 - 0.4, u1 + 0.4, style="tomoe", vis1=())
                    ue = [x for x in _eave_us(exact, e)]
                    if ue:
                        ux_, uz_ = -e[3], e[2]
                        bb = clip_poly(clip_poly(b, ux_, uz_, max(ue)), -ux_, -uz_, -min(ue))
                        if _ok(bb):
                            clip_sheets(et.solids, bb, part)
            else:
                _board_sheet(tmp, S, F, e, b, da, db, first)
                clip_sheets(tmp.solids, b, part)
    # eave edges (exact pieces): fascia / board edge, eave tile strip in the far LODs
    for poly, e, ci in exact:
        segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
        for a, b in segs:
            if abs(_f(e, *a)) < 1e-5 and abs(_f(e, *b)) < 1e-5:
                _eave_edge(part, S, e, a, b, tile)
    # -------------------------------------------------------------- rafters
    for poly, e, ci in exact:
        _rafters(part, S, poly, e)
    # -------------------------------------------------------------- ridges, hips, valleys
    ridges, hips = [], []
    for i, (P, eP, cP) in enumerate(exact):
        for j, (Q, eQ, cQ) in enumerate(allp):
            if _same(eP, eQ):
                continue
            for seg in _edges_shared(P, Q):
                m = ((seg[0][0] + seg[1][0]) / 2, (seg[0][1] + seg[1][1]) / 2)
                c = _centroid(P)
                k = 0.02 / max(1e-9, math.hypot(c[0] - m[0], c[1] - m[1]))
                mp = (m[0] + (c[0] - m[0]) * k, m[1] + (c[1] - m[1]) * k)
                convex = _f(eP, *mp) < _f(eQ, *mp)
                if convex:
                    # drawn once per pair: only from the lower index among the kept pieces (Q kept and earlier) or
                    # from P when Q is not kept here
                    if any(_same(eQ, x[1]) and x[0] == Q for x in exact[:i]):
                        continue
                    dz = abs(_f(eP, *seg[0]) - _f(eP, *seg[1]))
                    (ridges if dz < 1e-4 else hips).append(seg)
                else:
                    info["valleys"].append(seg)
                    _valley_half(part, S, P, eP, seg)
    ridges = _merge_lines(ridges)
    hips = _merge_lines(hips)
    # ridges meeting (T) or crossing (cross): the later ridge is cut around the earlier one (no stacked noshi);
    # an end on a module seam stops 11 mm short (the neighbour's noshi run 10 mm past their own ends)
    bx0, bx1 = min(p[0] for p in region), max(p[0] for p in region)
    bz0, bz1 = min(p[1] for p in region), max(p[1] for p in region)
    placed = []
    # an L meeting (two ridges ending on one point: a corner): the first runs on over the meeting point by half a
    # ridge width, so the second butts against its side
    ridges = [list(map(tuple, r)) for r in ridges]
    for k in range(len(ridges)):
        for k2 in range(k):
            for ia in (0, 1):
                for ib in (0, 1):
                    if _near(ridges[k][ia], ridges[k2][ib]):
                        a_, b_ = ridges[k2][1 - ib], ridges[k2][ib]
                        L_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                        if L_ > 1e-6:
                            ext_ = S.ridge_w / 2
                            ridges[k2][ib] = (b_[0] + (b_[0] - a_[0]) / L_ * ext_, b_[1] + (b_[1] - a_[1]) / L_ * ext_)
    for (a, b) in ridges:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-3:
            continue
        dx, dz = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        cuts = []
        for (c, d) in placed:
            t = _cross_t(a, b, c, d)
            if t is not None:
                cuts.append(t)
        w = S.ridge_w / 2 + 0.01
        spans = [[0.0, L]]
        for t in sorted(cuts):
            nsp = []
            for s0, s1 in spans:
                if s0 < t < s1 or abs(t - s0) < 1e-4 or abs(t - s1) < 1e-4:
                    if t - w > s0 + 1e-3:
                        nsp.append([s0, t - w])
                    if t + w < s1 - 1e-3:
                        nsp.append([t + w, s1])
                else:
                    nsp.append([s0, s1])
            spans = nsp
        for s0, s1 in spans:
            pa = (a[0] + dx * s0, a[1] + dz * s0)
            pb = (a[0] + dx * s1, a[1] + dz * s1)
            ends = []
            for q, sg in ((pa, 1.0), (pb, -1.0)):
                ends.append(any(abs(q[0] - v[1]) < 1e-4 for v in verges))
            seam = [(not ends[k]) and _on_box(q, bx0, bx1, bz0, bz1) for k, q in enumerate((pa, pb))]
            if seam[0]:
                pa = (pa[0] + dx * 0.011, pa[1] + dz * 0.011)
            if seam[1]:
                pb = (pb[0] - dx * 0.011, pb[1] - dz * 0.011)
            _ridge(part, S, exact, pa, pb, tuple(ends))
            info["ridges"].append((pa, pb))
        placed.append((a, b))
    for a, b in hips:
        _hip(part, S, exact, a, b)
        info["hips"].append((a, b))
    # -------------------------------------------------------------- verges (gable ends)
    for v in verges:
        _verge(part, S, grown, exact, v)
    return info


R_BED = "wall_arakabe"


def _cross_t(a, b, c, d):
    """Distance along a -> b where segment c -> d crosses or touches it (None if they do not meet)."""
    r = (b[0] - a[0], b[1] - a[1])
    q = (d[0] - c[0], d[1] - c[1])
    den = r[0] * q[1] - r[1] * q[0]
    if abs(den) < 1e-12:
        return None
    t = ((c[0] - a[0]) * q[1] - (c[1] - a[1]) * q[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    if -1e-4 <= t <= 1 + 1e-4 and -1e-4 <= u <= 1 + 1e-4:
        return t * math.hypot(*r)
    return None


def _on_box(q, x0, x1, z0, z1, eps=1e-4):
    return abs(q[0] - x0) < eps or abs(q[0] - x1) < eps or abs(q[1] - z0) < eps or abs(q[1] - z1) < eps


def _on_seg(p, a, b, eps=1e-4):
    ab = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*ab)
    if L < 1e-9:
        return False
    if abs(ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])) / L > eps:
        return False
    t = ((p[0] - a[0]) * ab[0] + (p[1] - a[1]) * ab[1]) / (L * L)
    return -eps <= t <= 1 + eps


def _near(p, q, eps=1e-4):
    return abs(p[0] - q[0]) < eps and abs(p[1] - q[1]) < eps


def _height_at(S, exact, x, z, h):
    best = None
    for poly, e, ci in exact:
        d = _f(e, x, z)
        if R_inside(poly, x, z, 1e-4):
            y = S.y(d, h) if S.profile == "straight" else _band_y(S, d, h)
            best = y if best is None else max(best, y)
    if best is None:
        ds = [_f(e, x, z) for poly, e, ci in exact]
        best = S.y(min(ds), h)
    return best


def _band_y(S, d, h):
    br = S.breaks()
    for da, db in zip(br[:-1], br[1:]):
        if da - 1e-9 <= d <= db + 1e-9:
            a, b = max(da, -1.0), db
            ya, yb_ = S.y(a, h), S.y(b, h)
            return ya + (yb_ - ya) * (d - a) / (b - a)
    return S.y(d, h)


def R_inside(poly, x, z, eps=1e-6):
    s = 1.0 if _area(poly) > 0 else -1.0
    n = len(poly)
    for i in range(n):
        ax, az = poly[i]
        bx, bz = poly[(i + 1) % n]
        if s * ((bx - ax) * (z - az) - (bz - az) * (x - ax)) < -eps:
            return False
    return True


# ------------------------------------------------------------------------------------------------ pieces of the roof
def _hong_field(tmp, F, u0, u1, r0, r1):
    """Hongawara for a strip roof: flat pans per 0.303 column + round covers on every seam (as kawara.hongawara_field,
    R1 only; the far slab carries R2 / R3)."""
    HC = K.HONG_COL
    quads, uvs = [], []
    k = math.floor(u0 / HC)
    covers = []
    while k * HC < u1 - 1e-4:
        a, b = max(u0, k * HC), min(u1, (k + 1) * HC)
        m = (a + b) / 2
        for (ua, ub, ha, hb) in ((a, m, 0.02, 0.0), (m, b, 0.0, 0.02)):
            quads.append([F.P(ua, r0, ha + 0.01), F.P(ub, r0, hb + 0.01), F.P(ub, r1, hb + 0.01), F.P(ua, r1, ha + 0.01)])
            uvs.append([(ua / K.UVU, -r0 / K.UVV), (ub / K.UVU, -r0 / K.UVV), (ub / K.UVU, -r1 / K.UVV),
                        (ua / K.UVU, -r1 / K.UVV)])
        covers.append(k * HC)
        k += 1
    tmp.add(Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                  K.FIELD, vis=(1,), uv=uvs, normals=[F.n] * len(quads), tag="hongawara"))
    # covers as open half-hexagon sheets (clippable): 3 faces along the column seam
    cq, cn, cu = [], [], []
    r = 0.075
    for u in covers:
        ring0, ring1 = [], []
        for j in range(4):
            ang = math.pi * j / 3
            off = add(mul(F.u, r * math.cos(ang)), mul(F.n, r * math.sin(ang) + 0.02))
            ring0.append(add(F.P(u, r0 - 0.03, 0.0), off))
            ring1.append(add(F.P(u, r1, 0.0), off))
        for j in range(3):
            cq.append([ring0[j], ring1[j], ring1[j + 1], ring0[j + 1]])
            ph = math.pi * (j + 0.5) / 3
            cn.append(norm(add(mul(F.u, math.cos(ph)), mul(F.n, math.sin(ph)))))
            cu.append([(0.0, 0.0), (0.0, (r1 - r0) / 0.6), (0.3, (r1 - r0) / 0.6), (0.3, 0.0)])
    if cq:
        tmp.add(Solid([p for q in cq for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(cq))],
                      K.TILE, vis=(1,), uv=cu, normals=cn, tag="cover"))


def _board_sheet(tmp, S, F, e, poly, da, db, first):
    """Board covering: the top surface of the band (+ two stepped courses at the eave), explicit uvs (courses run
    along the eave)."""
    mat = S.fam["mat"]
    mi = mat_info(mat)
    su, sv = mi["tile"], mi["tile_v"]
    u0, u1 = _u_range(poly, e)
    rl = (db - da) / F.cos
    quads, uvl, nrm = [], [], []
    expo = 0.10
    rows = [(k * expo, (k + 1) * expo) for k in range(3)] if first else []
    start = rows[-1][1] if rows else 0.0
    h = S.top
    for (rs, re) in rows:
        lo = 0.012
        quads.append([F.P(u0 - 0.3, rs, h + lo - 0.012), F.P(u1 + 0.3, rs, h + lo - 0.012), F.P(u1 + 0.3, re, h - 0.012),
                     F.P(u0 - 0.3, re, h - 0.012)])
        uvl.append([((u0 - 0.3) / su, -rs / sv), ((u1 + 0.3) / su, -rs / sv), ((u1 + 0.3) / su, -re / sv),
                    ((u0 - 0.3) / su, -re / sv)])
        nrm.append(F.n)
        quads.append([F.P(u0 - 0.3, rs, h - 0.024), F.P(u1 + 0.3, rs, h - 0.024), F.P(u1 + 0.3, rs, h + lo - 0.012),
                      F.P(u0 - 0.3, rs, h + lo - 0.012)])
        uvl.append([((u0 - 0.3) / su, -rs / sv + 0.01), ((u1 + 0.3) / su, -rs / sv + 0.01), ((u1 + 0.3) / su, -rs / sv),
                    ((u0 - 0.3) / su, -rs / sv)])
        nrm.append(mul(F.up, -1.0))
    quads.append([F.P(u0 - 0.3, start, h), F.P(u1 + 0.3, start, h), F.P(u1 + 0.3, rl + 0.05, h),
                  F.P(u0 - 0.3, rl + 0.05, h)])
    uvl.append([((u0 - 0.3) / su, -start / sv), ((u1 + 0.3) / su, -start / sv), ((u1 + 0.3) / su, -(rl + 0.05) / sv),
                ((u0 - 0.3) / su, -(rl + 0.05) / sv)])
    nrm.append(F.n)
    tmp.add(Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                  mat, vis=(1,), uv=uvl, normals=nrm, tag="board_field"))


def _eave_us(exact, e):
    """u values of the exact eave segment(s) of eave e (d = 0 edges of the exact pieces with that eave)."""
    ux, uz = -e[3], e[2]
    out = []
    for poly, e2, ci in exact:
        if not _same(e, e2):
            continue
        for i in range(len(poly)):
            a, b = poly[i], poly[(i + 1) % len(poly)]
            if abs(_f(e, *a)) < 1e-5 and abs(_f(e, *b)) < 1e-5:
                out += [a[0] * ux + a[1] * uz, b[0] * ux + b[1] * uz]
    return out


def _eave_edge(part, S, e, a, b, tile):
    """Along one eave segment a -> b (plan, d = 0): the fascia (tile: kawara_fascia, C13) or the thick board edge;
    a far eave strip (tile, R2 / R3)."""
    F, t = _frame(S, e, 0.0, max(0.3, S.ov))
    ux, uz = -e[3], e[2]
    ua, ub = a[0] * ux + a[1] * uz, b[0] * ux + b[1] * uz
    u0, u1 = min(ua, ub), max(ua, ub)
    # F is at the covering base (stack) on the eave line; h offsets along the slope normal
    if tile:
        hl, hh = -S.stack - 0.02, 0.012
        r0, r1 = -0.035, 0.0
        c = [F.P(u0, r0, hl), F.P(u1, r0, hl), F.P(u1, r1, hl), F.P(u0, r1, hl),
             F.P(u0, r0, hh), F.P(u1, r0, hh), F.P(u1, r1, hh), F.P(u0, r1, hh)]
        part.add(hexa(c, S.wood, vis=(1, 2, 3), tag="kawara_fascia", grain="long"))
        # far eave strip: the eave-tile course as one block, a little past the tile lips (C15 at the eave edge)
        cc = F.P((u0 + u1) / 2, (-0.10 + K.EXPO) / 2, 0.04)
        part.add(oriented_box(cc, F.u, F.n, F.up, (u1 - u0) / 2, 0.045, (K.EXPO + 0.10) / 2, K.TILE, vis=(2, 3),
                              tag="eave_strip"))
    else:
        r0, r1 = -0.04, 0.03
        hl, hh = -S.stack + 0.03, S.top + 0.012
        c = [F.P(u0, r0, hl), F.P(u1, r0, hl), F.P(u1, r1, hl), F.P(u0, r1, hl),
             F.P(u0, r0, hh), F.P(u1, r0, hh), F.P(u1, r1, hh), F.P(u0, r1, hh)]
        part.add(hexa(c, S.fam["mat"], vis=(1, 2, 3), tag="eave_stack"))


def _rafters(part, S, poly, e):
    """Open-topped rafters (bottom, two sides, foot: 4 faces) square to the eave every S.sp along u, from the eave
    to the piece's top (open roofs) or to the bearing line (caps)."""
    ux, uz = -e[3], e[2]
    u0, u1 = _u_range(poly, e)
    w, hgt = S.sec
    k = math.ceil((u0 + w) / S.sp)
    while k * S.sp < u1 - w:
        u = k * S.sp
        k += 1
        iv0 = _d_interval_at_u(poly, e, u - w / 2)
        iv1 = _d_interval_at_u(poly, e, u + w / 2)
        if not iv0 or not iv1:
            continue
        d0 = max(iv0[0], iv1[0], 0.0) + 0.02
        d1 = min(iv0[1], iv1[1]) - 0.03
        if S.body == "solid":
            d1 = min(d1, S.ov + 0.05)
        if d1 < d0 + 0.08:
            continue
        br = [d0] + [x for x in S.breaks() if d0 < x < d1] + [d1]
        qs, hint = [], []
        for da, db in zip(br[:-1], br[1:]):
            def P(d, sg, h, u=u):
                o = (e[0] - ux * (e[0] * ux + e[1] * uz), e[1] - uz * (e[0] * ux + e[1] * uz))
                px, pz = o[0] + ux * (u + sg * w / 2) + e[2] * d, o[1] + uz * (u + sg * w / 2) + e[3] * d
                return (px, _band_y(S, d, h) if S.profile != "straight" else S.y(d, h), pz)
            qs += [[P(da, -1, 0.0), P(da, 1, 0.0), P(db, 1, 0.0), P(db, -1, 0.0)],
                   [P(da, -1, 0.0), P(db, -1, 0.0), P(db, -1, hgt), P(da, -1, hgt)],
                   [P(da, 1, 0.0), P(db, 1, 0.0), P(db, 1, hgt), P(da, 1, hgt)]]
            hint += [(0.0, -1.0, 0.0), (-ux, 0.0, -uz), (ux, 0.0, uz)]
        qs.append([P(d0, -1, 0.0), P(d0, 1, 0.0), P(d0, 1, hgt), P(d0, -1, hgt)])
        hint.append((-e[2], 0.0, -e[3]))
        part.add(Solid([p for q in qs for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(qs))],
                       S.wood, vis=(1,), normals=hint, tag="rafter", grain="long"))


def _seg_pts(S, exact, a, b, h):
    """3D points along a plan segment at the roof surface + h, split at the d-band breaks (curved roofs)."""
    pts = [a, b]
    if S.profile != "straight":
        n = 6
        pts = [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n + 1)]
    return [(p[0], _height_at(S, exact, p[0], p[1], h), p[1]) for p in pts]


def _ridge(part, S, exact, a, b, ends):
    """A ridge along the plan segment a -> b: kawara noshi + cap (kawara.ridge) or a board box ridge."""
    p = _seg_pts(S, exact, a, b, S.stack + 0.01)
    p0, p1 = p[0], p[-1]
    if S.kind == "tile":
        top = K.ridge(part, p0, p1, courses=S.courses, width=S.ridge_w, cap_d=0.14 if S.D < 1.2 else 0.16,
                      end_tiles=ends)
        _mortar_far(part, p0, p1, S.ridge_w)
        if S.oni:
            d = norm(sub(p1, p0))
            for q, on, sg in ((p0, ends[0], -1.0), (p1, ends[1], 1.0)):
                if on:
                    f = (d[0] * sg, 0.0, d[2] * sg)
                    K.onigawara(part, add(q, (f[0] * 0.03, -0.01, f[2] * 0.03)), f,
                                height=0.30 if S.D < 1.2 else 0.36, width=0.26 if S.D < 1.2 else 0.30)
        return top
    w = S.ridge_w
    d, e1, e2 = frame_of(sub(p1, p0))
    c = mul(add(p0, p1), 0.5)
    L = math.dist(p0, p1)
    hb = S.top + 0.05
    part.add(oriented_box(add(c, (0.0, hb / 2 - 0.01, 0.0)), d, (0.0, 1.0, 0.0), norm(cross(d, (0.0, 1.0, 0.0))),
                          L / 2 + 0.02, hb / 2, w / 2, S.fam["mat"], vis=(1, 2, 3), tag="board_ridge"))
    part.add(oriented_box(add(c, (0.0, hb + 0.012, 0.0)), d, (0.0, 1.0, 0.0), norm(cross(d, (0.0, 1.0, 0.0))),
                          L / 2 + 0.04, 0.025, w / 2 + 0.03, S.wood, vis=(1, 2, 3), tag="ridge_cap"))
    return hb + 0.04


def _mortar_far(part, p0, p1, width):
    """kawara.ridge keeps its wide mortar bed in Resolution 1 / 2 only: the same footprint in Resolution 3 (C15)."""
    d, e1, e2 = frame_of(sub(p1, p0))
    c = add(mul(add(p0, p1), 0.5), mul(e2, 0.02))
    part.add(oriented_box(c, d, e2, e1, math.dist(p0, p1) / 2, 0.02, width / 2 + 0.03, "wall_shikkui", vis=(3,),
                          tag="mortar_far"))


def _hip(part, S, exact, a, b):
    """A hip (sloped convex edge): kawara noshi stack + cap, or a board hip ridge; in band segments when curved."""
    pts = _seg_pts(S, exact, a, b, S.stack + 0.01)
    if pts[0][1] < pts[-1][1]:
        pts = pts[::-1]                 # from the top down
    for q0, q1 in zip(pts[:-1], pts[1:]):
        last = q1 is pts[-1]
        if S.kind == "tile":
            top = K.ridge(part, q0, q1, courses=max(2, S.courses - 1), width=S.ridge_w - 0.02, cap_d=0.13,
                          end_tiles=(False, last))
            _mortar_far(part, q0, q1, S.ridge_w - 0.02)
            if not last:
                # a curved hip is a chain of straight ridges: one far block over each kink (C15 silhouette)
                d = norm(sub(q1, q0))
                side = norm(cross(d, (0.0, 1.0, 0.0)))
                up = norm(cross(side, d))
                part.add(oriented_box(add(q1, mul(up, top / 2)), d, up, side, 0.10, top / 2, (S.ridge_w - 0.02) / 2,
                                      K.TILE, vis=(2, 3), tag="hip_kink_far"))
        else:
            d = norm(sub(q1, q0))
            side = norm(cross(d, (0.0, 1.0, 0.0)))
            up = norm(cross(side, d))
            c = mul(add(q0, q1), 0.5)
            part.add(oriented_box(add(c, mul(up, S.top / 2 + 0.02)), d, up, side, math.dist(q0, q1) / 2 + 0.01,
                                  S.top / 2 + 0.03, S.ridge_w / 2 - 0.02, S.fam["mat"], vis=(1, 2, 3), tag="hip_board"))
    if S.body == "open":
        # the hip rafter (sumigi) under the hip line
        lo = _seg_pts(S, exact, a, b, -0.10)
        for q0, q1 in zip(lo[:-1], lo[1:]):
            part.add(tube(q0, q1, 0.065, S.wood, n=4, vis=(1, 2), tag="sumigi"))


def _valley_half(part, S, P, e, seg):
    """This piece's half of the valley lining (tani: kawara laid in the valley, or a valley board), lying on the
    piece's own plane within 0.16 of the valley line."""
    a, b = seg
    ab = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*ab)
    if L < 1e-3:
        return
    c = _centroid(P)
    nx, nz = -ab[1] / L, ab[0] / L
    if (c[0] - a[0]) * nx + (c[1] - a[1]) * nz < 0:
        nx, nz = -nx, -nz
    w = 0.16
    strip = clip_poly(P, nx, nz, nx * a[0] + nz * a[1] + w)
    if not _ok(strip):
        return
    tile = S.kind == "tile"
    h0, h1 = (S.stack + 0.025, S.stack + 0.060) if tile else (S.stack + S.top - 0.004, S.stack + S.top + 0.010)
    mat = K.TILE if tile else S.fam["mat"]
    for bnd, da, db in _bands(S, strip, e):
        part.add(slab(bnd, _band_fn(S, e, da, db, h0), _band_fn(S, e, da, db, h1), mat, vis=(1, 2, 3),
                      tag="valley"))
    if S.body == "open":
        # the valley rafter (tanigi) under the valley
        lo = [(p[0], _band_y(S, _f(e, p[0], p[1]), -0.10) if S.profile != "straight" else S.y(_f(e, p[0], p[1]), -0.10),
               p[1]) for p in (a, b)]
        # half section on this side only (the other module / piece draws the other half): a thin box
        d = norm(sub(lo[1], lo[0]))
        side = (nx, 0.0, nz)
        c3 = add(mul(add(lo[0], lo[1]), 0.5), mul(side, 0.035))
        part.add(oriented_box(c3, d, (0.0, 1.0, 0.0), side,
                              math.dist(lo[0], lo[1]) / 2, 0.06, 0.034, S.wood, vis=(1,), tag="tanigi"))


def _verge(part, S, grown, exact, v):
    """A gable end at x = v[1] (sign v[2]): bargeboards (hafu) under the verge, verge tiles (kawara.verge) on tile
    roofs, per piece and band."""
    _, xv, sg = v
    tile = S.kind == "tile"
    for poly, e, ci in exact:
        on = [p for p in poly if abs(p[0] - xv) < 1e-5]
        if len(on) < 2:
            continue
        za, zb = min(p[1] for p in on), max(p[1] for p in on)
        # hafu: a board in the plane x = xv (outside), from 0.20 under the rafter plane to the covering top,
        # following the slope (band segments when curved)
        n = 1 if S.profile == "straight" else 6
        zs = [za + (zb - za) * k / n for k in range(n + 1)]
        x0, x1 = (xv, xv + 0.035) if sg > 0 else (xv - 0.035, xv)
        for z0, z1 in zip(zs[:-1], zs[1:]):
            d0, d1 = _f(e, xv, z0), _f(e, xv, z1)
            yb0, yb1 = _band_y(S, d0, -0.20), _band_y(S, d1, -0.20)
            yt0, yt1 = _band_y(S, d0, S.stack + S.top + 0.02), _band_y(S, d1, S.stack + S.top + 0.02)
            c = [(x0, yb0, z0), (x0, yb1, z1), (x0, yt1, z1), (x0, yt0, z0),
                 (x1, yb0, z0), (x1, yb1, z1), (x1, yt1, z1), (x1, yt0, z0)]
            part.add(Solid(c, [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]],
                           S.wood, vis=(1, 2, 3), tag="hafu", grain="long"))
    if not tile:
        return
    for poly, e, ci in grown:
        on = [p for p in poly if abs(p[0] - xv) < 1e-5]
        if len(on) < 2:
            continue
        ux, uz = -e[3], e[2]
        u_edge = xv * ux
        side = 1 if (sg > 0) == (ux > 0) else -1
        for b, da, db in _bands(S, poly, e):
            F, t = _frame(S, e, da, db)
            rl = (db - da) / F.cos
            K.verge(part, F, u_edge, -0.06 if da <= 1e-6 else 0.0, rl, side)


# ------------------------------------------------------------------------------------------------ modules
def straight(part, S, L, ends=("seam", "seam"), branches=(), name="roof"):
    """A straight strip roof along x 0..L (centreline z = 0, bearing lines z = +-D/2). ends per end: 'seam' | 'gable'
    | 'hip'. branches: (end 0 | 1, '+z' | '-z'): a junction cell past that end with an arm to that side."""
    h = S.D / 2 + S.ov
    ext = {"seam": 0.0, "gable": S.gov, "hip": S.ov}
    x0, x1 = -ext[ends[0]], L + ext[ends[1]]
    X = [eave((0.0, h), (0.0, -1.0)), eave((0.0, -h), (0.0, 1.0))]
    if ends[0] == "hip":
        X.append(eave((-S.ov, 0.0), (1.0, 0.0)))
    if ends[1] == "hip":
        X.append(eave((L + S.ov, 0.0), (-1.0, 0.0)))
    cors = [X]
    for (end, side) in branches:
        xc = L + S.D / 2 if end == 1 else -S.D / 2
        Z = [eave((xc - h, 0.0), (1.0, 0.0)), eave((xc + h, 0.0), (-1.0, 0.0))]
        Z.append(eave((0.0, -h), (0.0, 1.0)) if side == "+z" else eave((0.0, h), (0.0, -1.0)))
        cors.append(Z)
    es = ["z0", "z1"] + (["x0"] if ends[0] == "hip" else []) + (["x1"] if ends[1] == "hip" else [])
    verges = ([("x", x0, -1)] if ends[0] == "gable" else []) + ([("x", x1, 1)] if ends[1] == "gable" else [])
    info = build(part, S, rect(x0, x1, -h, h), cors, own=(0,), eave_sides=es, verges=verges, name=name)
    info.update(kind="straight", L=L, ends=ends, region=(x0, x1, -h, h), ridge_y=S.ridge_y())
    return info


def junction(part, S, arms, name="roof"):
    """A junction cell centred on (0, 0) (the crossing of the centrelines): arms = the sides another strip leaves
    from ('-x', '+x', '-z', '+z'): 2 adjacent = corner (hip outside, valley inside), 3 = T, 4 = cross."""
    D2 = S.D / 2
    h = D2 + S.ov
    x0 = -D2 - (0.0 if "-x" in arms else S.ov)
    x1 = D2 + (0.0 if "+x" in arms else S.ov)
    z0 = -D2 - (0.0 if "-z" in arms else S.ov)
    z1 = D2 + (0.0 if "+z" in arms else S.ov)
    cors = []
    if "-x" in arms or "+x" in arms:
        X = [eave((0.0, h), (0.0, -1.0)), eave((0.0, -h), (0.0, 1.0))]
        if "+x" not in arms:
            X.append(eave((h, 0.0), (-1.0, 0.0)))
        if "-x" not in arms:
            X.append(eave((-h, 0.0), (1.0, 0.0)))
        cors.append(X)
    if "-z" in arms or "+z" in arms:
        Z = [eave((-h, 0.0), (1.0, 0.0)), eave((h, 0.0), (-1.0, 0.0))]
        if "+z" not in arms:
            Z.append(eave((0.0, h), (0.0, -1.0)))
        if "-z" not in arms:
            Z.append(eave((0.0, -h), (0.0, 1.0)))
        cors.append(Z)
    es = [sd for sd, a in (("x0", "-x"), ("x1", "+x"), ("z0", "-z"), ("z1", "+z")) if a not in arms]
    info = build(part, S, rect(x0, x1, z0, z1), cors, own=tuple(range(len(cors))), eave_sides=es, name=name)
    info.update(kind="junction", arms=tuple(arms), region=(x0, x1, z0, z1), ridge_y=S.ridge_y())
    return info
