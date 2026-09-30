"""Roofs (build list jp_p_roof_*): a generator from the footprint (PLAYBOOK §10.2) plus the fixed roof parts.

roof(part, W, D, form, family, ...) covers a W x D footprint (x 0..W along the ridge, z 0 = front wall .. -D back
wall, y 0 = floor) with form kirizuma | yosemune | irimoya | kabuto and family sangawara | hongawara | ishioki |
itabuki | kakigara | thatch. The eave line is the keta top (eave_y, 2.88 by default). Every slope is a convex plan
polygon with a plane; coverings are clipped to it, collision is one convex slab per slope.
"""
import math

from .core import Part, Solid, box, prism, hexa, KEN, HALF, QK, POST, EAVE_Y, WALL_H, rng_for, add, mul, norm, cross, dot
from .shapes import slab, tube, half_tube, oriented_box, clip_poly, clean_poly, posed, frame_of
from . import kawara as K

PITCH = {"sangawara": 0.45, "hongawara": 0.45, "ishioki": 0.35, "itabuki": 0.45, "kakigara": 0.45, "thatch": 1.0}
EAVE_OV = {"sangawara": 0.90, "hongawara": 0.90, "ishioki": 1.05, "itabuki": 0.75, "kakigara": 0.75, "thatch": 1.00}
GABLE_OV = {"sangawara": 0.40, "hongawara": 0.40, "ishioki": 0.40, "itabuki": 0.35, "kakigara": 0.35, "thatch": 0.45}
STACK = {"sangawara": 0.152, "hongawara": 0.152, "ishioki": 0.10, "itabuki": 0.09, "kakigara": 0.09, "thatch": 0.06}
BOARD_MAT = {"ishioki": ("roof_kureita", (1.2, 1.2), 0.15), "itabuki": ("roof_kokera", None, 0.0909),
             "kakigara": ("roof_kakigara", None, 0.0909)}


# ------------------------------------------------------------------------------------------------ slopes
class Slope:
    def __init__(self, name, poly, in_dir, wall_pt, u_dir, u_origin, eave_y, t, ov, full_ridge=False, verges=(),
                 pieces=None):
        self.name = name
        self.poly = _ccw(poly)
        self.pieces = [_ccw(pc) for pc in pieces] if pieces else [self.poly]      # convex parts of the slope
        self.inw = in_dir
        self.wall = wall_pt
        self.udir = u_dir
        self.uo = u_origin            # plan point where u = 0 (a ken line on the eave edge)
        self.eave_y = eave_y
        self.t = t
        self.ov = ov
        self.full_ridge = full_ridge
        self.verges = verges          # u positions of verge edges (kirizuma ends)
        self.plain = (False, False)   # B2: a verge end left plain (party end): (u-low end, u-high end)
        self.cos = math.cos(math.atan(t))

    def s(self, x, z):
        return (x - self.wall[0]) * self.inw[0] + (z - self.wall[1]) * self.inw[1]

    def y(self, x, z, h0):
        return self.eave_y + h0 + self.t * self.s(x, z)

    def u_of(self, x, z):
        return (x - self.uo[0]) * self.udir[0] + (z - self.uo[1]) * self.udir[1]

    def eave_point(self, u):
        return (self.uo[0] + self.udir[0] * u, self.uo[1] + self.udir[1] * u)

    def u_range(self):
        us = [self.u_of(x, z) for x, z in self.poly]
        return min(us), max(us)

    def depth_at(self, u):
        """Plan distance from the eave edge at u, inward, to the boundary of the union of the convex pieces."""
        ex, ez = self.eave_point(u)
        d = 0.0
        for _ in range(len(self.pieces) + 1):
            px, pz = ex + self.inw[0] * (d + 1e-4), ez + self.inw[1] * (d + 1e-4)
            best = None
            for pc in self.pieces:
                if _inside(pc, px, pz):
                    e = _exit(pc, px, pz, self.inw)
                    best = e if best is None else max(best, e)
            if best is None:
                break
            d = d + 1e-4 + best
        return d

    def frame(self, h0):
        """kawara SlopeFrame with h = 0 on the tile bed; origin at u = 0 on the eave edge."""
        ex, ez = self.eave_point(0.0)
        return K.SlopeFrame((ex, self.y(ex, ez, h0), ez), (self.udir[0], 0.0, self.udir[1]),
                            (self.inw[0], 0.0, self.inw[1]), self.t)


def _inside(pc, x, z, eps=1e-6):
    n = len(pc)
    for i in range(n):
        ax, az = pc[i]
        bx, bz = pc[(i + 1) % n]
        if (bx - ax) * (z - az) - (bz - az) * (x - ax) < -eps:
            return False
    return True


def _exit(pc, x, z, d):
    best = 1e9
    n = len(pc)
    for i in range(n):
        ax, az = pc[i]
        bx, bz = pc[(i + 1) % n]
        nx, nz = (bz - az), -(bx - ax)                         # outward normal of a CCW edge
        den = nx * d[0] + nz * d[1]
        if den > 1e-9:
            best = min(best, (nx * (ax - x) + nz * (az - z)) / den)
    return max(0.0, best)


def _ccw(poly):
    a = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    # plan coordinates (x, z): the p3d frame is left-handed seen from above; keep a consistent orientation
    return list(poly) if a > 0 else list(poly)[::-1]


def slopes_for(W, D, form, eave_y, t, ov, gov):
    """The slope list of a roof form over x 0..W, z 0..-D (ridge along x). gov: the verge overhang, a number or
    (left, right) for a kirizuma roof whose two ends differ (a townhouse unit's party end, B0)."""
    h = D / 2
    S = []
    gl, gr = gov if isinstance(gov, (tuple, list)) else (gov, gov)
    if form == "kirizuma":
        S.append(Slope("front", [(-gl, ov), (W + gr, ov), (W + gr, -h), (-gl, -h)], (0.0, -1.0), (0.0, 0.0),
                       (1.0, 0.0), (0.0, ov), eave_y, t, ov, True, verges=(-gl, W + gr)))
        S.append(Slope("back", [(-gl, -D - ov), (-gl, -h), (W + gr, -h), (W + gr, -D - ov)], (0.0, 1.0), (0.0, -D),
                       (-1.0, 0.0), (W, -D - ov), eave_y, t, ov, True, verges=(-W - gl + W, gr + W - W)))
        S[1].verges = (S[1].u_of(W + gr, -D - ov), S[1].u_of(-gl, -D - ov))
        return S
    if form == "yosemune":
        xg0, xg1 = h, W - h
    elif form == "irimoya":
        xg0, xg1 = D / 4, W - D / 4
    elif form == "kabuto":
        xg0, xg1 = D / 6, W - h
    else:
        raise ValueError(form)
    # front / back: hip lines from the eave corners at 45 deg in plan up to x = xg, then (irimoya) straight up
    def fb(front):
        if front:
            e, sgn, wz = ov, -1.0, 0.0
        else:
            e, sgn, wz = -D - ov, 1.0, -D
        # hip meets x = xg0 at inward distance (xg0 + ov) from the eave
        zl = e + sgn * (xg0 + ov)
        zr = e + sgn * (W - xg1 + ov)
        zr_top = -h
        poly = clean_poly([(-ov, e), (W + ov, e), (xg1, zr), (xg1, zr_top), (xg0, zr_top), (xg0, zl)])
        pieces = [clean_poly([(-ov, e), (W + ov, e), (xg1, zr), (xg0, zl)])]
        up = clean_poly([(xg0, zl), (xg1, zr), (xg1, zr_top), (xg0, zr_top)])
        if len(up) >= 3 and abs(sum(up[i][0] * up[(i + 1) % len(up)][1] - up[(i + 1) % len(up)][0] * up[i][1]
                                    for i in range(len(up)))) > 1e-4:
            pieces.append(up)
        if front:
            return Slope("front", poly, (0.0, -1.0), (0.0, 0.0), (1.0, 0.0), (0.0, ov), eave_y, t, ov, True,
                         pieces=pieces)
        return Slope("back", poly, (0.0, 1.0), (0.0, -D), (-1.0, 0.0), (W, -D - ov), eave_y, t, ov, True, pieces=pieces)
    S.append(fb(True))
    S.append(fb(False))
    # side slopes: the hip triangle / trapezoid up to x = xg (or the small gable foot)
    left = clean_poly([(-ov, ov), (-ov, -D - ov), (xg0, -D + xg0), (xg0, -xg0)])
    S.append(Slope("left", left, (1.0, 0.0), (0.0, 0.0), (0.0, -1.0), (-ov, 0.0), eave_y, t, ov))
    r0 = W - xg1
    right = clean_poly([(W + ov, -D - ov), (W + ov, ov), (xg1, -r0), (xg1, -D + r0)])
    S.append(Slope("right", right, (-1.0, 0.0), (W, 0.0), (0.0, 1.0), (W + ov, -D), eave_y, t, ov))
    return S


# ------------------------------------------------------------------------------------------------ coverings
def collision(part, sl, h_top, fire, surf=None, rafter=0.0):
    """One convex slab per slope: rafter underside plane .. covering top plane (Geometry / View / Fire)."""
    for pc in sl.pieces:
        part.add(slab(pc, lambda x, z: sl.y(x, z, -0.0), lambda x, z: sl.y(x, z, h_top), "wood_weathered", vis=(),
                      geo=True, view=True, fire=fire, tag="roof_geo_" + sl.name))
        if surf:
            part.road([(x, sl.y(x, z, h_top), z) for x, z in pc], surf)


def sheathing(part, sl, h0=0.06, mat="wood_weathered", vis=(1, 2, 3)):
    for pc in sl.pieces:
        part.add(slab(pc, lambda x, z: sl.y(x, z, h0), lambda x, z: sl.y(x, z, h0 + 0.012),
                      {"bottom": mat, "default": mat}, vis=vis, tag="sheathing"))


def rafters(part, sl, spacing=0.303, sec=(0.045, 0.06), round_=False, only_eave=True, mat="wood_weathered", vis=(1,),
            d_start=0.03, tag="rafter"):
    """Rafters on a slope from d_start (plan distance in from the eave edge) to the eave soffit end (only_eave) or the
    top of the slope. B2's koyagumi continues the eave rafters inside with d_start = ov + 0.25."""
    u0, u1 = sl.u_range()
    k = math.ceil(u0 / spacing)
    while k * spacing < u1:
        u = k * spacing
        if u - sec[0] / 2 < u0 - 1e-9 or u + sec[0] / 2 > u1 + 1e-9:
            # C1 (2026-09-30): a rafter on the slope's end line would stick half out past the covering (C15 saw it
            # from above on pent ends at x 0): keep every rafter inside the slope
            k += 1
            continue
        dmax = sl.depth_at(u)
        if dmax > max(0.2, d_start + 0.05):
            ex, ez = sl.eave_point(u)
            d1 = min(dmax, sl.ov + 0.25) if only_eave else dmax
            a = (ex + sl.inw[0] * d_start, ez + sl.inw[1] * d_start)
            b = (ex + sl.inw[0] * d1, ez + sl.inw[1] * d1)
            if round_:
                pa = (a[0], sl.y(a[0], a[1], 0.0) + 0.035, a[1])
                pb = (b[0], sl.y(b[0], b[1], 0.0) + 0.035, b[1])
                part.add(tube(pa, pb, 0.035, mat, n=6, vis=vis, tag=tag))
            else:
                # open-topped (hidden under the sheathing): bottom, two sides, foot = 4 faces
                w = sec[0] / 2
                ux, uz = sl.udir
                P = lambda px, pz, sg, h: (px + ux * w * sg, sl.y(px + ux * w * sg, pz + uz * w * sg, h),  # noqa: E731
                                            pz + uz * w * sg)
                qs = [[P(a[0], a[1], -1, 0.0), P(a[0], a[1], 1, 0.0), P(b[0], b[1], 1, 0.0), P(b[0], b[1], -1, 0.0)],
                      [P(a[0], a[1], -1, 0.0), P(b[0], b[1], -1, 0.0), P(b[0], b[1], -1, sec[1]), P(a[0], a[1], -1, sec[1])],
                      [P(a[0], a[1], 1, 0.0), P(b[0], b[1], 1, 0.0), P(b[0], b[1], 1, sec[1]), P(a[0], a[1], 1, sec[1])],
                      [P(a[0], a[1], -1, 0.0), P(a[0], a[1], 1, 0.0), P(a[0], a[1], 1, sec[1]), P(a[0], a[1], -1, sec[1])]]
                hint = [(0.0, -1.0, 0.0), (-ux, 0.0, -uz), (ux, 0.0, uz), (-sl.inw[0], 0.0, -sl.inw[1])]
                part.add(Solid([p for q in qs for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(4)],
                               mat, vis=vis, normals=hint, tag=tag, grain="long"))
        k += 1


SHEATH_TOP = 0.072     # sheathing (nojiita) top above the rafter underside plane (sheathing(): 0.06 + 0.012)
BED_MAT = "wall_arakabe"   # fuki-tsuchi: straw-tempered clay, the same earth as arakabe walls


def tile_bed(part, sl, h_bed, h0=SHEATH_TOP, vis=(1, 2)):
    """G3 fix (Stephen: "roof tiles are not on the roof; there's a gap when I get close"). The period laid kawara on a
    bed of straw-tempered clay (fuki-tsuchi) spread over the sheathing boards; the tiles sit IN it. One convex slab per
    slope piece from the sheathing top to 4 mm under the tile bed plane, so no daylight shows between boards and tiles
    at the eave, the verge or anywhere a player looks along the roof. PLAYBOOK §15 T1."""
    for pc in sl.pieces:
        part.add(slab(pc, lambda x, z: sl.y(x, z, h0), lambda x, z: sl.y(x, z, h_bed - 0.004), BED_MAT, vis=vis,
                      tag="tile_bed"))


def kawara_fascia(part, sl, h_bed, mat="wood_weathered", vis=(1, 2, 3)):
    """G3 fix: the eave board (kayaoi / hana-kakushi) along each eave edge, square to the rafters, from just under the
    rafter plane up to 12 mm above the tile bed plane, so the eave tiles' lips hang in front of it and nothing is open
    between tiles, bed, sheathing and rafter ends. PLAYBOOK §15 T1."""
    F = sl.frame(0.0)
    us = [sl.u_of(x, z) for x, z in sl.poly if abs(sl.s(x, z) + sl.ov) < 1e-6]
    if len(us) < 2:
        return
    u0, u1 = min(us), max(us)
    r0, r1 = -0.035, 0.0
    hl, hh = -0.02, h_bed + 0.012
    c = [F.P(u0, r0, hl), F.P(u1, r0, hl), F.P(u1, r1, hl), F.P(u0, r1, hl),
         F.P(u0, r0, hh), F.P(u1, r0, hh), F.P(u1, r1, hh), F.P(u0, r1, hh)]
    part.add(hexa(c, mat, vis=vis, tag="kawara_fascia", grain="long"))


def cover_kawara(part, sl, fam="sangawara", eave_style="tomoe", h0=None):
    h0 = STACK[fam] if h0 is None else h0
    tile_bed(part, sl, h0)
    kawara_fascia(part, sl, h0)
    F = sl.frame(h0)
    u0, u1 = sl.u_range()
    vw = 0.13
    pl = getattr(sl, "plain", (False, False))
    fu0 = sl.verges[0] + (0.0 if pl[0] else vw) if sl.verges else u0
    fu1 = sl.verges[1] - (0.0 if pl[1] else vw) if sl.verges else u1
    if sl.verges:
        rl = sl.depth_at((u0 + u1) / 2) / sl.cos
        r1fn = None
    else:
        rl = None
        r1fn = lambda u: sl.depth_at(u) / sl.cos       # noqa: E731
    if fam == "hongawara":
        K.hongawara_field(part, F, fu0, fu1, K.EXPO, rl if rl else max(sl.depth_at(u) for u in (u0, (u0 + u1) / 2, u1)) / sl.cos)
    else:
        K.field(part, F, fu0, fu1, K.EXPO, rl if rl else 0.0, r1_fn=r1fn, rows_eave=2, rows_ridge=1 if rl else 0)
    K.eave_tiles(part, F, fu0 if sl.verges else u0, fu1 if sl.verges else u1, style=eave_style)
    if sl.verges:
        if not pl[0]:
            K.verge(part, F, sl.verges[0], 0.0, rl, -1)
        if not pl[1]:
            K.verge(part, F, sl.verges[1], 0.0, rl, +1)
    return F


def cover_boards(part, sl, fam, worn=False, rows_eave=3, rows_ridge=1):
    mat, uvs, expo = BOARD_MAT[fam]
    h0 = STACK[fam]
    F = sl.frame(h0 - 0.012)                 # board courses sit on the sheathing (0.06-0.072)
    u0, u1 = sl.u_range()
    rng = rng_for(part.name + sl.name + "boards")
    rl_mid = sl.depth_at((u0 + u1) / 2) / sl.cos
    su, sv = uvs if uvs else (2.0, 2.0)
    # top surface in strips (uv down the slope from the eave line, courses of the texture align with the steps)
    quads, uvl, nrm = [], [], []
    step_rows = [(k * expo, (k + 1) * expo) for k in range(rows_eave)]
    for (a, b, cu) in K.columns(u0, u1, 0.5):
        ra, rb = sl.depth_at(a) / sl.cos, sl.depth_at(b) / sl.cos
        bands = [(r0, r1, True) for r0, r1 in step_rows]
        top_rows = [] if not sl.full_ridge else [(min(ra, rb) - expo * (k + 1), min(ra, rb) - expo * k, True)
                                                  for k in range(rows_ridge)]
        bands.append((rows_eave * expo, None, False))
        for (rs, re, stepped) in bands:
            rea = re if re is not None else (top_rows[-1][0] if top_rows else ra)
            reb = re if re is not None else (top_rows[-1][0] if top_rows else rb)
            if rea <= rs and reb <= rs:
                continue
            bh = 0.014 if stepped else 0.007
            lo, hi = (bh, 0.0) if stepped else (bh, bh)
            quads.append([F.P(a, rs, lo), F.P(b, rs, lo), F.P(b, max(rs, reb), hi), F.P(a, max(rs, rea), hi)])
            uvl.append([(a / su, -rs / sv), (b / su, -rs / sv), (b / su, -max(rs, reb) / sv), (a / su, -max(rs, rea) / sv)])
            nrm.append(F.n)
            if stepped:
                quads.append([F.P(a, rs, 0.0), F.P(b, rs, 0.0), F.P(b, rs, lo), F.P(a, rs, lo)])
                uvl.append([(a / su, -rs / sv + 0.005), (b / su, -rs / sv + 0.005), (b / su, -rs / sv), (a / su, -rs / sv)])
                nrm.append(mul(F.up, -1.0))
        for (rs, re, _) in top_rows[::-1]:
            quads.append([F.P(a, rs, 0.014), F.P(b, rs, 0.014), F.P(b, re, 0.0), F.P(a, re, 0.0)])
            uvl.append([(a / su, -rs / sv), (b / su, -rs / sv), (b / su, -re / sv), (a / su, -re / sv)])
            nrm.append(F.n)
            quads.append([F.P(a, rs, 0.0), F.P(b, rs, 0.0), F.P(b, rs, 0.014), F.P(a, rs, 0.014)])
            uvl.append([(a / su, -rs / sv + 0.005), (b / su, -rs / sv + 0.005), (b / su, -rs / sv), (a / su, -rs / sv)])
            nrm.append(mul(F.up, -1.0))
    part.add(Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                   mat, vis=(1,), uv=uvl, normals=nrm, tag="board_field"))
    # LOD 2/3: one plane per slope
    for pc in sl.pieces:
        part.add(slab(pc, lambda x, z: sl.y(x, z, h0 - 0.012), lambda x, z: sl.y(x, z, h0 - 0.002), mat, vis=(2, 3),
                      tag="board_field_lod", uvscale=uvs))
    # eave edge: the visible stack of board ends (0.05-0.08); in every LOD (B2: it stands 4 cm past the far slab's
    # eave, and C15 / T7b wants a stable silhouette)
    ea = F.P(u0, -0.02, -0.02)
    eb = F.P(u1, -0.02, -0.02)
    d, e1, e2 = frame_of(tuple(eb[k] - ea[k] for k in range(3)))
    c = tuple((ea[k] + eb[k]) / 2 for k in range(3))
    part.add(oriented_box(c, d, F.n, F.up, (u1 - u0) / 2, 0.035, 0.04, mat, vis=(1, 2, 3), tag="eave_stack",
                          uvscale=uvs))
    if worn:
        for _ in range(9):
            u = rng.uniform(u0 + 0.1, u1 - 0.4)
            r = rng.uniform(0.3, rl_mid - 0.4)
            w = rng.uniform(0.10, 0.20)
            L = rng.uniform(0.3, 0.45)
            p0 = F.P(u, r, 0.02)
            c = add(p0, add(mul(F.u, w / 2), mul(F.up, L / 2)))
            ax = norm(add(F.up, mul(F.n, rng.uniform(0.08, 0.2))))      # lifted, curling board
            part.add(oriented_box(c, F.u, norm(cross(F.u, ax)), ax, w / 2, 0.005, L / 2, mat, vis=(1,), tag="lifted",
                                  uvoff=(rng.random(), rng.random())))
    return F


def battens_stones(part, sl, h0, spacing=0.60, sparse=False, seed=0, first=0.45):
    """Split-pole battens eave-parallel with river stones on their upslope side (8-shape set, random yaw)."""
    F = sl.frame(h0)
    u0, u1 = sl.u_range()
    rng = rng_for(part.name + "stones" + sl.name, seed)
    rmax = sl.depth_at((u0 + u1) / 2) / sl.cos
    r = first
    shapes = [_stone_shape(k) for k in range(8)]
    n = 0
    while r < rmax - 0.25:
        pa, pb = F.P(u0 + 0.05, r, 0.035), F.P(u1 - 0.05, r, 0.035)
        part.add(tube(pa, pb, 0.035, "wood_weathered", n=6, vis=(1, 2), tag="batten"))
        u = u0 + rng.uniform(0.1, 0.3)
        while u < u1 - 0.2:
            if not sparse or rng.random() < 0.45:
                k = rng.randrange(8)
                size = shapes[k]
                yaw = rng.uniform(0, math.pi)
                part.add(_stone_on(F, u, r + 0.035 + size[1] / 2, size, yaw, rng, vis=(1,)))
                if n % 2 == 0:
                    part.add(_stone_on(F, u, r + 0.035 + size[1] / 2, (size[0] * 0.9, size[1] * 0.9, size[2]), yaw, rng,
                                       vis=(2,), n=5))
                n += 1
            u += rng.uniform(0.30, 0.45)
        r += spacing
    return n


def _stone_shape(k):
    rng = rng_for("roofstone", k)
    return (rng.uniform(0.15, 0.30), rng.uniform(0.13, 0.25), rng.uniform(0.08, 0.14))


def _stone_on(F, u, r, size, yaw, rng, vis=(1,), n=7):
    from .core import rings, rand_convex
    w, d, h = size
    base = rand_convex(rng, n, w / 2, d / 2, 0.15)
    prof = [(0.0, 0.9), (h * 0.45, 1.0), (h * 0.85, 0.75), (h, 0.35)]
    s = rings((base, prof), "stone_river", vis=vis, tag="roof_stone")
    ca, sa = math.cos(yaw), math.sin(yaw)

    def f(p):
        a, hh, b = p[0] * ca - p[2] * sa, p[1], p[0] * sa + p[2] * ca
        return F.P(u + a, r + b, hh + 0.005)
    return posed(s, f)


def cover_thatch(part, sl, cut=0.60):
    """Thick thatch slab per slope with a stepped (3-band) square-cut eave face; top = thatch, sides = cut face."""
    h0 = STACK["thatch"]
    mats = {"top": "roof_thatch", "bottom": "bamboo_weathered", "side": "roof_thatch_cut", "default": "roof_thatch_cut"}
    set_back = 0.08

    def inset(poly, d):
        """The slope polygon with its eave edge moved inward by d (eave-side half-plane)."""
        ex, ez = sl.eave_point(0.0)
        a, b = -sl.inw[0], -sl.inw[1]
        c = a * (ex + sl.inw[0] * d) + b * (ez + sl.inw[1] * d)
        return clean_poly(clip_poly(poly, a, b, c))
    for pc in sl.pieces:
        body = inset(pc, set_back)
        if len(body) >= 3:
            part.add(slab(body, lambda x, z: sl.y(x, z, h0), lambda x, z: sl.y(x, z, h0 + cut), mats, vis=(1, 2, 3),
                          geo=True, view=True, fire="hay", tag="thatch_body"))
    # two bands in front of the body: each lower edge higher, each 0.04 further out (layer bands of the cut face)
    for k, (d0, d1) in enumerate(((set_back / 2, set_back), (0.0, set_back / 2))):
        band = inset(sl.pieces[0], d0)
        band = clean_poly(clip_poly(band, sl.inw[0], sl.inw[1],
                                    sl.inw[0] * (sl.eave_point(0.0)[0] + sl.inw[0] * d1) +
                                    sl.inw[1] * (sl.eave_point(0.0)[1] + sl.inw[1] * d1)))
        if len(band) >= 3:
            lift = cut * (k + 1) / 3.2
            part.add(slab(band, lambda x, z, l=lift: sl.y(x, z, h0 + l), lambda x, z: sl.y(x, z, h0 + cut), mats,
                          vis=(1, 2), tag="thatch_band"))
    return h0 + cut


def hip_lines(sls, W, D, form, ov):
    """Hip ridge segments (plan) for hipped forms: from the eave corners to the top of each hip."""
    out = []
    for sl in sls:
        if sl.name not in ("left", "right"):
            continue
        poly = sl.poly
        # the two corners on the eave (x = -ov or W + ov) and the two top points
        eave = [p for p in poly if abs(sl.s(p[0], p[1]) + ov) < 1e-6]
        top = [p for p in poly if abs(sl.s(p[0], p[1]) + ov) >= 1e-6]
        for e in eave:
            tp = min(top, key=lambda q: math.dist(q, e))
            out.append((e, tp))
    return out


def roof(part, W, D, form="kirizuma", fam="sangawara", eave_y=EAVE_Y, t=None, ov=None, gov=None, walkable=True,
         courses=None, eave_style="tomoe", ridge_kind=None, soffit=True, worn=False, plain_ends=(False, False)):
    """plain_ends (kirizuma only; B2 jp_p_roof_party_end): (left, right) verge ends left PLAIN for a party line: no
    verge tiles (the field runs to the edge), no bargeboard or purlin ends, no onigawara or ridge-end tile; the ridge
    stops 2.5 cm inside the edge so nothing crosses into the neighbour's lot. The closures are party.roof_end's."""
    t = PITCH[fam] if t is None else t
    ov = EAVE_OV[fam] if ov is None else ov
    gov = GABLE_OV[fam] if gov is None else gov
    gl, gr = gov if isinstance(gov, (tuple, list)) else (gov, gov)
    sls = slopes_for(W, D, form, eave_y, t, ov, gov)
    pe = tuple(bool(v) for v in plain_ends) if form == "kirizuma" else (False, False)
    if any(pe):
        sls[0].plain = (pe[0], pe[1])                 # front: u runs +x (u-low = left)
        sls[1].plain = (pe[1], pe[0])                 # back: u runs -x (u-low = right)
    info = {"slopes": [], "t": t, "ov": ov, "gov": gov, "form": form, "fam": fam}
    fire = {"thatch": "hay"}.get(fam, "pottery" if fam in ("sangawara", "hongawara") else "wood")
    h_top = STACK[fam] + (0.05 if fam in ("sangawara", "hongawara") else 0.012)
    surf = "tile_roof" if fam in ("sangawara", "hongawara") else ("board_roof" if fam != "thatch" else None)
    for sl in sls:
        if fam == "thatch":
            top = cover_thatch(part, sl)
            rafters(part, sl, spacing=0.303, round_=True, only_eave=False, vis=(1,))
            for pc in sl.pieces:
                part.add(slab(pc, lambda x, z, s_=sl: s_.y(x, z, 0.055), lambda x, z, s_=sl: s_.y(x, z, 0.06),
                              "bamboo_weathered", vis=(1, 2), tag="lath", uvscale=(0.5, 0.5)))
        else:
            collision(part, sl, h_top, fire, surf if walkable else None)
            sheathing(part, sl)
            if soffit:
                rafters(part, sl, only_eave=True)
            if fam in ("sangawara", "hongawara"):
                cover_kawara(part, sl, fam, eave_style)
            else:
                cover_boards(part, sl, fam, worn=worn)
                if fam == "ishioki":
                    battens_stones(part, sl, STACK[fam] - 0.02)
                if fam == "itabuki":
                    pass
        info["slopes"].append(sl.name)
    # ridge line
    h = D / 2
    xr0, xr1 = {"kirizuma": (-gl, W + gr), "yosemune": (h, W - h), "irimoya": (D / 4, W - D / 4),
                "kabuto": (D / 6, W - h)}[form]
    stack_top = {"thatch": STACK["thatch"] + 0.60}.get(fam, STACK[fam] + 0.03)
    yr = eave_y + t * h + stack_top
    info["ridge"] = ((xr0, yr, -h), (xr1, yr, -h))
    if any(pe):
        info["plain_ends"] = pe
    if fam in ("sangawara", "hongawara"):
        c = courses or (5 if fam == "hongawara" else 3)
        if any(pe):
            K.ridge(part, (xr0 + (0.025 if pe[0] else 0.04), yr - 0.02, -h),
                    (xr1 - (0.025 if pe[1] else 0.04), yr - 0.02, -h), courses=c, end_tiles=(not pe[0], not pe[1]))
        else:
            K.ridge(part, (xr0 + 0.04, yr - 0.02, -h), (xr1 - 0.04, yr - 0.02, -h), courses=c)
        if form == "kirizuma":
            for x, f, plain in ((xr0, (-1.0, 0.0, 0.0), pe[0]), (xr1, (1.0, 0.0, 0.0), pe[1])):
                if plain:
                    continue
                K.onigawara(part, (x + (0.04 if f[0] < 0 else -0.04), yr - 0.03, -h), f,
                            height=0.38 if c >= 5 else 0.30, width=0.33)
        for (e, tp) in hip_lines(sls, W, D, form, ov):
            p0 = (tp[0], _hip_y(sls, tp, stack_top) - 0.02, tp[1])
            p1 = (e[0], _hip_y(sls, e, stack_top) + 0.02, e[1])
            K.ridge(part, p0, p1, courses=max(2, c - 1), width=0.20, cap_d=0.14, mortar=True, end_tiles=True)
        if form in ("irimoya", "kabuto"):
            _small_gables(part, W, D, form, eave_y, t, stack_top, fam)
    elif fam == "thatch":
        for (e, tp) in hip_lines(sls, W, D, form, ov):
            p0 = (tp[0], _hip_y(sls, tp, stack_top) - 0.08, tp[1])
            p1 = (e[0], _hip_y(sls, e, stack_top) - 0.10, e[1])
            part.add(tube(p0, p1, 0.26, "roof_thatch", n=8, vis=(1, 2), tag="hip_roll", uvscale=(2.0, 2.0)))
        if form in ("irimoya", "kabuto"):
            _small_gables(part, W, D, form, eave_y, t, stack_top, fam)
        thatch_ridge(part, (xr0 - (gl if form == "kirizuma" else 0.0) * 0.0, yr, -h), (xr1, yr, -h),
                     ridge_kind or "bamboo")
    else:
        board_ridge(part, (xr0, yr, -h), (xr1, yr, -h), t, stoned=(fam == "ishioki"))
    if form == "kirizuma" or fam != "thatch":
        if form == "kirizuma":
            for x, sg, plain in ((-gl, -1, pe[0]), (W + gr, 1, pe[1])):
                if not plain:
                    hafu(part, x, D, t, eave_y, ov, sg, fam)
    part.meta.setdefault("roof", info)
    return sls, info


def ridge_walk(info, name="ridge_walk", top=0.14, half=0.14, road_half=0.12, inset=0.05):
    """The ridge walk (B0 step 0a, from buildings/machiya_t3_01): a collision + Roadway strip over the main ridge stack
    of roof()'s info, so rooftop players walk the ridge instead of clipping it (PLAYBOOK §15 T9: tile and board roofs
    are walkable). Thatch roofs are not walkable: returns None. Keep the name 'ridge_walk': the C12 roof-poke check
    (raycheck.roof_pokes) allows it inside the roof bodies."""
    fam = info.get("fam", "sangawara")
    if fam == "thatch":
        return None
    kawara = fam in ("sangawara", "hongawara")
    (xr0, yr, zr), (xr1, _, _) = info["ridge"]
    s = Part(name, "", "")
    ytop = yr + top
    s.add(box(xr0 + inset, xr1 - inset, yr - 0.30, ytop, zr - half, zr + half, "roof_kawara" if kawara else "roof_kureita",
              vis=(), geo=True, view=True, fire="pottery" if kawara else "wood", tag="ridge_geo"))
    s.road([(xr0 + inset, ytop, zr - road_half), (xr1 - inset, ytop, zr - road_half),
            (xr1 - inset, ytop, zr + road_half), (xr0 + inset, ytop, zr + road_half)],
           "tile_roof" if kawara else "board_roof")
    return s


def _hip_y(sls, p, stack_top):
    sl = next(s for s in sls if s.name in ("left", "right") and any(math.dist(p, q) < 1e-6 for q in s.poly))
    return sl.y(p[0], p[1], stack_top)


def _small_gables(part, W, D, form, eave_y, t, stack_top, fam):
    """Vertical small gables of irimoya / kabuto: lattice smoke opening (kemuridashi _irimoya) + hafu boards."""
    h = D / 2
    ends = [(D / 4 if form == "irimoya" else D / 6, -1)]
    if form == "irimoya":
        ends.append((W - D / 4, +1))
    for xg, sg in ends:
        yb = eave_y + t * (xg if sg < 0 else W - xg) + stack_top * 0.5
        ya = eave_y + t * h + stack_top * 0.5
        half = h - (xg if sg < 0 else W - xg)
        kemuri_lattice(part, xg, yb, ya, -h, half, sg)


def kemuri_lattice(part, x, yb, ya, zc, half, sg, mat="wood_weathered"):
    """Latticed triangle in a small gable (smoke opening): board rim + 0.03 bars."""
    tri = [(yb, zc - half), (yb, zc + half), (ya, zc)]
    part.add(prism([(y, z) for y, z in tri], "x", x - 0.02, x + 0.02, "wood_sooted", vis=(), geo=True, view=False,
                   fire=None, tag="gable_geo"))
    n = max(2, int(2 * half / 0.08))
    for k in range(1, n):
        z = zc - half + 2 * half * k / n
        top = yb + (ya - yb) * (1 - abs(z - zc) / half)
        if top - yb > 0.05:
            part.add(box(x - 0.015, x + 0.015, yb, top, z - 0.015, z + 0.015, mat, vis=(1,), tag="kemuri_bar"))
    part.add(box(x - 0.025, x + 0.025, yb - 0.06, yb, zc - half, zc + half, mat, vis=(1, 2), tag="kemuri_sill"))
    part.add(prism([(y, z) for y, z in tri], "x", x - sg * 0.30 - 0.01, x - sg * 0.30 + 0.01, "wood_sooted", vis=(1, 2),
                   tag="kemuri_dark"))
    for side in (-1, 1):
        a = (x + sg * 0.02, yb - 0.02, zc + side * (half + 0.10))
        b = (x + sg * 0.02, ya + 0.08, zc)
        d, e1, e2 = frame_of(tuple(b[k] - a[k] for k in range(3)))
        c = tuple((a[k] + b[k]) / 2 for k in range(3))
        part.add(oriented_box(c, d, (1.0, 0.0, 0.0), norm(cross(d, (1.0, 0.0, 0.0))), math.dist(a, b) / 2, 0.015, 0.12,
                              mat, vis=(1, 2), tag="small_hafu"))


# ------------------------------------------------------------------------------------------------ ridges, hafu, eaves
def board_ridge(part, p0, p1, t, stoned=False, width=0.36, height=0.08, mat="roof_kureita"):
    """Board strips nailed over the ridge in a mass, held by battens; stones on ishioki ridges."""
    rng = rng_for(part.name + "board_ridge")
    L = math.dist(p0, p1)
    ang = math.atan(t)
    hw = width / 2
    y0 = p0[1] - hw * math.sin(ang)
    poly = [(p0[1] - 0.02 - hw * t, p0[2] - hw), (p0[1] + height * 0.6, p0[2] - hw * 0.8), (p0[1] + height, p0[2]),
            (p0[1] + height * 0.6, p0[2] + hw * 0.8), (p0[1] - 0.02 - hw * t, p0[2] + hw)]
    poly = [(y, z) for y, z in poly]
    part.add(prism(poly, "x", p0[0], p1[0], {"default": mat}, vis=(1, 2, 3), geo=True, view=True, fire="wood",
                   tag="board_ridge", uvscale=(1.2, 1.2)))
    for sgn in (-1, 1):
        a = (p0[0], p0[1] + height * 0.55, p0[2] + sgn * hw * 0.55)
        b = (p1[0], p1[1] + height * 0.55, p1[2] + sgn * hw * 0.55)
        part.add(tube(a, b, 0.03, "wood_weathered", n=6, vis=(1, 2), tag="ridge_batten"))
    if stoned:
        x = p0[0] + 0.2
        while x < p1[0] - 0.15:
            k = rng.randrange(8)
            w, d, h = _stone_shape(k)
            from .core import rings, rand_convex
            base = rand_convex(rng, 7, w / 2, d / 2, 0.15)
            base = [(bx + x, bz + p0[2]) for bx, bz in base]
            prof = [(p0[1] + height - 0.01, 0.9), (p0[1] + height + h * 0.45, 1.0), (p0[1] + height + h * 0.85, 0.75),
                    (p0[1] + height + h, 0.35)]
            part.add(rings((base, prof), "stone_river", vis=(1,), tag="ridge_stone"))
            x += rng.uniform(0.32, 0.45)
    return p0[1] + height


def thatch_ridge(part, p0, p1, kind="bamboo", seed=0):
    """Thatch ridge caps: bamboo-bound (Kanto), tiled (Musashi), turf with iris (shiba), grass with crossed umanori."""
    rng = rng_for(part.name + "tridge" + kind, seed)
    x0, x1 = p0[0], p1[0]
    y, z = p0[1], p0[2]
    H = {"bamboo": 0.55, "tile": 0.50, "shiba": 0.65, "umanori": 0.60}[kind]
    w = 0.95
    poly = [(y - 0.35, z - w / 2 - 0.25), (y + H * 0.55, z - w / 2), (y + H, z - 0.18), (y + H, z + 0.18),
            (y + H * 0.55, z + w / 2), (y - 0.35, z + w / 2 + 0.25)]
    part.add(prism(poly, "x", x0 - 0.2, x1 + 0.2, {"default": "roof_thatch"}, vis=(1, 2, 3), geo=True, view=True,
                   fire="hay", tag="thatch_ridge", uvscale=(1.5, 1.5)))
    if kind == "bamboo":
        for dz in (-0.33, -0.15, 0.15, 0.33):
            yy = y + H * (0.55 + 0.45 * (1 - (abs(dz) - 0.15) / 0.3)) if abs(dz) > 0.16 else y + H
            part.add(tube((x0 - 0.2, yy + 0.02, z + dz), (x1 + 0.2, yy + 0.02, z + dz), 0.03, "bamboo_weathered", n=6,
                          vis=(1, 2), tag="ridge_bamboo"))
        x = x0
        while x < x1:
            for sgn in (-1, 1):
                a = (x, y + H * 0.55 - 0.02, z + sgn * (w / 2 + 0.02))
                b = (x, y + H + 0.02, z + sgn * 0.12)
                part.add(tube(a, b, 0.018, "bamboo_weathered", n=5, vis=(1,), tag="binding"))
            x += 0.45
    elif kind == "tile":
        K.ridge(part, (x0 - 0.1, y + H - 0.02, z), (x1 + 0.1, y + H - 0.02, z), courses=2, width=0.40, cap_d=0.18,
                mortar=True, end_tiles=True)
        for sgn in (-1, 1):
            part.add(box(x0 - 0.2, x1 + 0.2, y + H * 0.45, y + H * 0.62, z + sgn * 0.42 - 0.06, z + sgn * 0.42 + 0.06,
                         "roof_kawara", vis=(1, 2), tag="ridge_tile_skirt"))
    elif kind == "shiba":
        part.add(prism([(y + H - 0.01, z - 0.30), (y + H + 0.10, z - 0.20), (y + H + 0.12, z + 0.20), (y + H - 0.01, z + 0.30)],
                       "x", x0 - 0.15, x1 + 0.15, "wall_arakabe", vis=(1, 2), tag="turf"))
        x = x0
        while x < x1:
            for k in range(3):
                xx = x + rng.uniform(-0.1, 0.1)
                zz = z + rng.uniform(-0.15, 0.15)
                hh = rng.uniform(0.25, 0.45)
                part.add(tube((xx, y + H + 0.08, zz), (xx + rng.uniform(-0.05, 0.05), y + H + 0.08 + hh, zz), 0.012,
                              "moss_leaf" if False else "bamboo_weathered", n=4, vis=(1,), tag="iris"))
            x += 0.30
    else:
        n = max(3, int((x1 - x0) / HALF) + 1)
        for k in range(n):
            x = x0 + (x1 - x0) * k / (n - 1)
            for sgn in (-1, 1):
                a = (x, y + H * 0.35, z + sgn * 0.55)
                b = (x, y + H + 0.35, z - sgn * 0.20)
                part.add(tube(a, b, 0.045, "wood_weathered", n=6, vis=(1, 2), tag="umanori"))
        part.add(tube((x0 - 0.1, y + H + 0.12, z), (x1 + 0.1, y + H + 0.12, z), 0.06, "wood_weathered", n=6, vis=(1, 2),
                      tag="umanori_pole"))
    return y + H


def hafu(part, x, D, t, eave_y, ov, sg, fam, board=(0.03, 0.24), purlins=True):
    """Bargeboards on a gable end at x (outer face towards sg): two boards meeting at the ridge + purlin ends."""
    h = D / 2
    stack = STACK.get(fam, 0.1)
    kind = "thatch" if fam == "thatch" else ("tile" if fam in ("sangawara", "hongawara") else "board")
    hide = kind == "thatch"
    for side in (-1, 1):
        ze = ov if side > 0 else -D - ov
        zr = -h
        ye = eave_y + stack - t * ov
        yr = eave_y + stack + t * h
        a = (x, ye - 0.02, ze)
        b = (x, yr + 0.02, zr)
        d, e1, e2 = frame_of(tuple(b[k] - a[k] for k in range(3)))
        up = norm(cross((1.0, 0.0, 0.0), d)) if side > 0 else norm(cross(d, (1.0, 0.0, 0.0)))
        if up[1] < 0:
            up = mul(up, -1.0)
        c = add(tuple((a[k] + b[k]) / 2 for k in range(3)), mul(up, -board[1] / 2 + 0.03))
        if not hide:
            part.add(oriented_box(add(c, (sg * board[0] / 2, 0.0, 0.0)), d, up, (1.0, 0.0, 0.0), math.dist(a, b) / 2 + 0.03,
                                  board[1] / 2, board[0] / 2, "wood_weathered", vis=(1, 2, 3), tag="hafu"))
            if kind == "board":
                cc = add(c, add((sg * (board[0] + 0.02), 0.0, 0.0), mul(up, board[1] / 2 - 0.02)))
                part.add(oriented_box(cc, d, up, (1.0, 0.0, 0.0), math.dist(a, b) / 2 + 0.03, 0.025, 0.02,
                                      "wood_weathered", vis=(1, 2, 3), tag="verge_batten"))
        if purlins:
            k = 1
            while True:
                s = k * HALF
                if s >= h - 0.1:
                    break
                zz = (0.0 - s) if side > 0 else (-D + s)
                yy = eave_y + t * s - 0.10
                part.add(box(min(x, x - sg * 0.30), max(x, x - sg * 0.30), yy - 0.06, yy + 0.06, zz - 0.05, zz + 0.05,
                             "wood_weathered", vis=(1, 2), tag="purlin_end"))
                k += 1
    # ridge purlin end
    part.add(box(min(x, x - sg * 0.30), max(x, x - sg * 0.30), eave_y + t * h - 0.12, eave_y + t * h + 0.02, -h - 0.06,
                 -h + 0.06, "wood_weathered", vis=(1, 2), tag="purlin_end"))


def eave_soffit(part, x0, x1, kind="tile", ov=0.90, t=0.45, eave_y=EAVE_Y):
    """Eave underside of a front wall (z 0 wall line) from x0 to x1: rafters, sheathing and fascia / poles + lath."""
    sl = Slope("front", [(x0, ov), (x1, ov), (x1, -0.3), (x0, -0.3)], (0.0, -1.0), (0.0, 0.0), (1.0, 0.0), (0.0, ov),
               eave_y, t, ov)
    if kind == "thatch":
        k = math.ceil(x0 / 0.303)
        while k * 0.303 < x1:
            x = k * 0.303
            part.add(tube((x, sl.y(x, ov, 0.035), ov), (x, sl.y(x, -0.3, 0.035), -0.3), 0.035, "wood_weathered", n=6,
                          vis=(1, 2), tag="pole_rafter"))
            k += 1
        r = 0.0
        while r < ov + 0.3:
            z = ov - r
            part.add(tube((x0, sl.y(x0, z, 0.08), z), (x1, sl.y(x1, z, 0.08), z), 0.012, "bamboo_weathered", n=5,
                          vis=(1,), tag="lath"))
            r += 0.10
        part.add(slab(sl.poly, lambda x, z: sl.y(x, z, 0.07), lambda x, z: sl.y(x, z, 0.075), "bamboo_weathered",
                      vis=(2, 3), tag="lath_lod", uvscale=(0.5, 0.5)))
        return sl
    sec = (0.045, 0.06) if kind == "tile" else (0.036, 0.045)
    rafters(part, sl, spacing=0.303, sec=sec, only_eave=False, vis=(1, 2))
    sheathing(part, sl, h0=sec[1])
    if kind == "tile":
        ze = ov + 0.0
        part.add(box(x0 - 0.02, x1 + 0.02, sl.y(0, ze, 0.0), sl.y(0, ze, 0.0) + 0.12, ze, ze + 0.03, "wood_weathered",
                     vis=(1, 2, 3), tag="fascia"))
    else:
        part.add(box(x0, x1, sl.y(0, ov + 0.03, sec[1]), sl.y(0, ov + 0.03, sec[1] + 0.012), ov, ov + 0.03,
                     "wood_weathered", vis=(1, 2), tag="board_overhang"))
    return sl
