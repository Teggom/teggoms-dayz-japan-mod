"""Kawara as geometry (PLAYBOOK rule 1, §6.1): corrugated sangawara field with modelled rows near eave and ridge,
eave tiles with round ends and lips, verge tiles, noshi ridges with a round cap, onigawara, hongawara pans + covers.

A slope is described by a SlopeFrame: world point (u, r, h) = origin + u*u_dir + r*(up-the-slope unit) + h*(slope
normal); u runs along the eave (0 = a ken line, so the 0.26 columns land on every ken line), r is the distance up the
slope surface from the eave line, h the height above the tile bed plane.
"""
import math

from .core import Solid, add, mul, norm, cross, box, rng_for
from .shapes import tube, half_tube, oriented_box, frame_of

COL = 0.26            # working width (ken / 7)
EXPO = 0.235          # exposure along the slope
FIELD = "roof_kawara_field"
TILE = "roof_kawara"
UVU, UVV = 1.04, 0.94  # field texture tile (4 columns x 4 courses)

# corrugation profiles (fraction across the column, height above the bed): pan dip at 0.30, roll at 0.82
PROFILE = {0: [(0.0, 0.035), (0.30, 0.0), (0.62, 0.012), (0.82, 0.055), (1.0, 0.035)],          # 4 segments
           1: [(0.0, 0.045), (0.45, 0.0), (1.0, 0.045)],                                           # 2 segments
           2: [(0.0, 0.03), (1.0, 0.03)]}
HONG_COL = 0.303


class SlopeFrame:
    def __init__(self, origin, u_dir, in_dir, t):
        self.o = origin
        self.u = norm(u_dir)
        ang = math.atan(t)
        self.t = t
        self.cos = math.cos(ang)
        self.up = (in_dir[0] * math.cos(ang), math.sin(ang), in_dir[2] * math.cos(ang))
        self.n = (-in_dir[0] * math.sin(ang), math.cos(ang), -in_dir[2] * math.sin(ang))
        self.inw = norm(in_dir)

    def P(self, u, r, h=0.0):
        return add(self.o, add(mul(self.u, u), add(mul(self.up, r), mul(self.n, h))))


def columns(u0, u1, w=COL):
    k0 = math.floor(u0 / w + 1e-6)
    out = []
    k = k0
    while k * w < u1 - 1e-6:
        a, b = max(u0, k * w), min(u1, (k + 1) * w)
        if b - a > 1e-4:
            out.append((a, b, k * w))
        k += 1
    return out


def _prof_pts(a, b, cu, lod):
    """Profile points inside [a, b] of the column starting at cu (clipped columns keep the profile)."""
    pts = []
    for f, h in PROFILE[lod]:
        u = cu + f * COL
        if a - 1e-6 <= u <= b + 1e-6:
            pts.append((u, h))
    # add clipped ends
    def h_at(u):
        pr = PROFILE[lod]
        f = (u - cu) / COL
        for i in range(len(pr) - 1):
            if pr[i][0] <= f <= pr[i + 1][0]:
                t = (f - pr[i][0]) / (pr[i + 1][0] - pr[i][0])
                return pr[i][1] + t * (pr[i + 1][1] - pr[i][1])
        return pr[-1][1]
    if not pts or pts[0][0] > a + 1e-6:
        pts.insert(0, (a, h_at(a)))
    if pts[-1][0] < b - 1e-6:
        pts.append((b, h_at(b)))
    return pts


def field(part, F, u0, u1, r0, r1, lod_sets=((0, (1,)), (1, (2,)), (2, (3,))), rows_eave=2, rows_ridge=1, bh=0.022,
          r1_fn=None, mat=FIELD, tag="kawara_field", seed=0):
    """Corrugated field between u0..u1 and r0..r1 (r1_fn(u) overrides r1 for hip-clipped slopes; no ridge rows then).
    LOD0: 4 segments per column, rows_eave + rows_ridge modelled courses (top + butt), the middle one strip carrying
    the course texture. LOD1: 2 segments, one strip. LOD2: flat."""
    rng = rng_for(part.name + tag, seed)
    n_faces = 0
    for lod, vis in lod_sets:
        quads, uvs, nrm = [], [], []
        for (a, b, cu) in columns(u0, u1):
            prof = _prof_pts(a, b, cu, lod)
            ra = r1_fn(a) if r1_fn else r1
            rb = r1_fn(b) if r1_fn else r1
            # row bands along r: (rs, re, stepped)
            bands = []
            if lod == 0:
                rr = r0
                for k in range(rows_eave):
                    if rr + EXPO < min(ra, rb) - 1e-3:
                        bands.append((rr, rr + EXPO, True))
                        rr += EXPO
                top_rows = [] if r1_fn else [(r1 - (k + 1) * EXPO, r1 - k * EXPO, True) for k in range(rows_ridge)]
                mid_end = top_rows[-1][0] if top_rows else None
                bands.append((rr, mid_end, False))
                bands += top_rows[::-1]
            else:
                bands = [(r0, None, False)]
            for (rs, re, stepped) in bands:
                for i in range(len(prof) - 1):
                    (ua, ha), (ub, hb) = prof[i], prof[i + 1]
                    rea = re if re is not None else (r1_fn(ua) if r1_fn else r1)
                    reb = re if re is not None else (r1_fn(ub) if r1_fn else r1)
                    if rea <= rs + 1e-4 and reb <= rs + 1e-4:
                        continue
                    rea, reb = max(rea, rs), max(reb, rs)
                    lo = bh if stepped else bh * 0.5
                    hi = 0.0 if stepped else bh * 0.5
                    if lod > 0:
                        lo = hi = bh * 0.5
                    q = [F.P(ua, rs, ha + lo), F.P(ub, rs, hb + lo), F.P(ub, reb, hb + hi), F.P(ua, rea, ha + hi)]
                    quads.append(q)
                    uvs.append([(ua / UVU, -rs / UVV), (ub / UVU, -rs / UVV), (ub / UVU, -reb / UVV), (ua / UVU, -rea / UVV)])
                    if stepped and lod == 0:
                        # butt face: drop from this row's lower edge to the row below
                        bq = [F.P(ua, rs, ha), F.P(ub, rs, hb), F.P(ub, rs, hb + lo), F.P(ua, rs, ha + lo)]
                        quads.append(bq)
                        uvs.append([(ua / UVU, -rs / UVV + 0.01), (ub / UVU, -rs / UVV + 0.01), (ub / UVU, -rs / UVV),
                                    (ua / UVU, -rs / UVV)])
        if quads:
            s = Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                      mat, vis=vis, uv=uvs, normals=[F.n] * len(quads), tag=tag)
            # butt faces face down-slope: fix their hint normal
            fix = []
            for q in quads:
                nn = norm(cross(tuple(q[1][k] - q[0][k] for k in range(3)), tuple(q[3][k] - q[0][k] for k in range(3))))
                fix.append(F.n if abs(nn[0] * F.n[0] + nn[1] * F.n[1] + nn[2] * F.n[2]) > 0.5 else mul(F.up, -1.0))
            s.normals = fix
            part.add(s)
            if lod == 0:
                n_faces = len(quads)
    return n_faces


def eave_tiles(part, F, u0, u1, style="plain", lip=0.045, manju_d=0.075, over=0.06, vis0=(1,), vis1=(2,), tag="eave_tile"):
    """First course: the tile body (4-segment profile, one course), a turned-down lip across each column and the
    round end (manju) on the roll. style: 'plain' | 'tomoe' (raised boss). LOD1: one extruded strip."""
    quads, uvs, nrm = [], [], []
    r_lo = -over
    out_dir = mul(F.up, -1.0)
    discs = []
    for (a, b, cu) in columns(u0, u1):
        prof = _prof_pts(a, b, cu, 0)
        for i in range(len(prof) - 1):
            (ua, ha), (ub, hb) = prof[i], prof[i + 1]
            quads.append([F.P(ua, r_lo, ha + 0.022), F.P(ub, r_lo, hb + 0.022), F.P(ub, EXPO, hb), F.P(ua, EXPO, ha)])
            uvs.append([(ua / 1.0, 0.0), (ub / 1.0, 0.0), (ub / 1.0, 0.3), (ua / 1.0, 0.3)])
            nrm.append(F.n)
        # lip: one turned-down band across the column, under the pan
        hm = 0.022 + 0.01
        quads.append([F.P(a, r_lo, hm), F.P(b, r_lo, hm), F.P(b, r_lo, hm - lip), F.P(a, r_lo, hm - lip)])
        uvs.append([(a, 0.0), (b, 0.0), (b, 0.05), (a, 0.05)])
        nrm.append(out_dir)
        # round end (manju) on the roll: a hexagonal disc facing out; tomoe = a raised boss disc
        cx = cu + 0.82 * COL
        if a <= cx <= b:
            for (rr, off) in ((manju_d / 2, 0.004),) + (((manju_d * 0.28, 0.010),) if style == "tomoe" else ()):
                c = F.P(cx, r_lo - off, 0.055 + 0.022 - manju_d / 2 + 0.012)
                ring = [add(c, add(mul(F.u, rr * math.cos(math.pi / 3 * k)), mul(F.n, rr * math.sin(math.pi / 3 * k))))
                        for k in range(6)]
                discs.append(ring)
    if discs:
        part.add(Solid([p for d in discs for p in d], [list(range(6 * i, 6 * i + 6)) for i in range(len(discs))], TILE,
                       vis=vis0, uv="fit", normals=[out_dir] * len(discs), tag="manju"))
    if quads:
        part.add(Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                       TILE, vis=vis0, uv=uvs, normals=nrm, tag=tag))
    # LOD1 strip: one extruded box along the eave
    d, e1, e2 = F.u, F.up, F.n
    c = F.P((u0 + u1) / 2, (r_lo + EXPO) / 2, 0.035)
    part.add(oriented_box(c, d, e2, e1, (u1 - u0) / 2, 0.035, (EXPO - r_lo) / 2, TILE, vis=vis1, tag="eave_strip"))
    return len(quads)


def verge(part, F, u_edge, r0, r1, side, drop=0.07, width=0.13, vis=(1, 2), tag="verge"):
    """Sode-gawara along a gable edge at u_edge (side = -1: left end, +1: right end), one tile per course."""
    quads, uvs, nrm = [], [], []
    ui = u_edge - side * width
    r = r0
    k = 0
    while r < r1 - 1e-4:
        re = min(r1, r + EXPO)
        lo, hi = 0.045, 0.028
        quads.append([F.P(ui, r, lo), F.P(u_edge, r, lo), F.P(u_edge, re, hi), F.P(ui, re, hi)])
        nrm.append(F.n)
        quads.append([F.P(u_edge, r, lo), F.P(u_edge, re, hi), F.P(u_edge, re, hi - drop), F.P(u_edge, r, lo - drop)])
        nrm.append(mul(F.u, side))
        quads.append([F.P(ui, r, lo), F.P(u_edge, r, lo), F.P(u_edge, r, lo - drop), F.P(ui, r, 0.0)])
        nrm.append(mul(F.up, -1.0))
        for _ in range(3):
            uvs.append([(0, 0), (1, 0), (1, 0.25), (0, 0.25)])
        r = re
        k += 1
    part.add(Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                   TILE, vis=vis, uv=uvs, normals=nrm, tag=tag))
    return k


def ridge(part, p0, p1, courses=3, width=0.22, cap_d=0.16, mortar=True, end_tiles=True, vis=(1, 2), up_hint=None,
          tag="ridge"):
    """Noshi courses + a round cap along p0 -> p1 (level ridge or sloped hip). Returns the ridge top height above p0."""
    d, e1, e2 = frame_of(tuple(p1[k] - p0[k] for k in range(3)))
    L = math.dist(p0, p1)
    c = tuple((p0[k] + p1[k]) / 2 for k in range(3))
    h = 0.0
    if mortar:
        cc = add(c, mul(e2, 0.02))
        part.add(oriented_box(cc, d, e2, e1, L / 2, 0.02, width / 2 + 0.03, "wall_shikkui", vis=(1, 2), tag="mortar"))
        h = 0.04
    for k in range(courses):
        w = width - (0.02 if k % 2 else 0.0)
        cc = add(c, mul(e2, h + 0.0125))
        part.add(oriented_box(cc, d, e2, e1, L / 2 + 0.01, 0.0125, w / 2, TILE, vis=vis if k < 2 else (1,), tag="noshi",
                              uvoff=(0.13 * k, 0.37 * k)))
        h += 0.025
    a = add(p0, mul(e2, h))
    b = add(p1, mul(e2, h))
    part.add(half_tube(add(a, mul(d, -0.02)), add(b, mul(d, 0.02)), cap_d / 2, TILE, n=6, vis=(1, 2, 3), tag="ganburi"))
    if end_tiles:
        for q, sg in ((a, -1), (b, 1)):
            part.add(tube(add(q, mul(d, sg * 0.02)), add(q, mul(d, sg * 0.05)), cap_d / 2 + 0.01, TILE, n=8, vis=(1,),
                          tag="ridge_end"))
    return h + cap_d / 2


def onigawara(part, base, facing, height=0.38, width=0.33, sui=False, vis=(1, 2)):
    """Shouldered ridge-end block standing on `base`, its face towards `facing` (unit, horizontal)."""
    f = norm(facing)
    side = norm(cross((0.0, 1.0, 0.0), f))
    up = (0.0, 1.0, 0.0)
    t = 0.07

    def ob(cx, cy, cz, hx, hy, hz, m=TILE, v=vis):
        c = add(base, add(mul(side, cx), add(mul(up, cy), mul(f, cz))))
        part.add(oriented_box(c, side, up, f, hx, hy, hz, m, vis=v, tag="onigawara"))
    h1 = height * 0.58
    ob(0, h1 / 2, 0, width / 2, h1 / 2, t / 2)                                   # lower plate
    ob(0, h1 + height * 0.14, 0, width * 0.38, height * 0.14, t / 2)             # shoulders stepped in
    # rounded top: arc cap (convex polygon prism)
    r = width * 0.30
    cy = h1 + height * 0.28
    pts = [(r * math.cos(math.pi * k / 6), r * 0.75 * math.sin(math.pi * k / 6)) for k in range(7)]
    verts = []
    for dz in (-t / 2, t / 2):
        for (x, y) in pts:
            verts.append(add(base, add(mul(side, x), add(mul(up, cy + y), mul(f, dz)))))
    n = len(pts)
    faces = [list(range(n)), list(range(n, 2 * n))] + [[i, i + 1, n + i + 1, n + i] for i in range(n - 1)] + [[n - 1, 0, n, 2 * n - 1]]
    part.add(Solid(verts, faces, TILE, vis=vis, tag="onigawara"))
    ob(0, height * 0.40, -t / 2 - 0.08, width * 0.30, height * 0.40, 0.08, v=(1,))  # back block
    if sui:
        z = t / 2 + 0.006
        ob(0, h1 * 0.55, z, 0.012, h1 * 0.35, 0.006, v=(1,))
        for sx, sy in ((-0.06, 0.62), (0.06, 0.62), (-0.07, 0.35), (0.07, 0.35)):
            ob(sx, h1 * sy, z, 0.035, 0.010, 0.006, v=(1,))
    else:
        ob(0, h1 * 0.5, t / 2 + 0.005, width * 0.36, h1 * 0.34, 0.005, v=(1,))     # raised panel border


def hongawara_field(part, F, u0, u1, r0, r1, vis0=(1,), tag="hongawara"):
    """Flat pans (slightly dished) in 0.303 columns with round covers (d 0.15) on every seam."""
    quads, uvs = [], []
    k = math.floor(u0 / HONG_COL)
    while k * HONG_COL < u1 - 1e-4:
        a, b = max(u0, k * HONG_COL), min(u1, (k + 1) * HONG_COL)
        m = (a + b) / 2
        for (ua, ub, ha, hb) in ((a, m, 0.02, 0.0), (m, b, 0.0, 0.02)):
            quads.append([F.P(ua, r0, ha + 0.01), F.P(ub, r0, hb + 0.01), F.P(ub, r1, hb + 0.01), F.P(ua, r1, ha + 0.01)])
            uvs.append([(ua / UVU, -r0 / UVV), (ub / UVU, -r0 / UVV), (ub / UVU, -r1 / UVV), (ua / UVU, -r1 / UVV)])
        if k * HONG_COL > u0 + 0.01:
            u = k * HONG_COL
            part.add(half_tube(F.P(u, r0 - 0.03, 0.02), F.P(u, r1, 0.02), 0.075, TILE, n=6, vis=(1, 2), tag="cover"))
        k += 1
    part.add(Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                   FIELD, vis=vis0 + (2,), uv=uvs, normals=[F.n] * len(quads), tag=tag, uvscale=None))
    return len(quads)
