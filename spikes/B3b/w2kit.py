"""w2kit - helpers for the W2 site objects (BUILD_LIST wave 2: torii, stone lanterns, basin, steps, graveyard), agent W2
2026-09-30. Built on skit (B3b) and fkit (B3a), which stay unchanged.

  sweep()       a rectangular section swept along a curve in the x-y plane (torii kasagi / shimaki with upswept ends)
  hollow()      a block with a cut hollow (basins, incense stands, grave water hollows): outer rings + rim + inner wall
                + floor, visual only (collision is a separate box)
  moss_strip()  moss decal following the top of a member (kasagi, tie-beam, lantern roof edge)
  moss_foot()   moss quads round the foot of a round post on its shady (-z, north) side
  shear()       rack a group of solids (x += k * (y - y0)): leaning torii with both feet on the ground
  carved()      a carved-text decal (B1's jp_m_decal_carved_text atlas only), text_on + crop
  torii_rope()  a straw rope (shimenawa) between two points with straw tassels and, optionally, paper shide
Frame (skit): origin = base centre on the terrain, +y up, +z = front (the approach / the path), autocenter 0.
"""
import math
import random

import skit
from skit import (core, box, prism, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, beam,
                  rope_path, sag, text_on, moss_top, moss_face, leaves, litter, add_all, ground, hull3, CARVED, CUT,
                  FIELD, RIVER, WOOD, KURO, ROPE, PAPER, CTEXT, SUMI, MOSS, LEAF, BAMBOO)
from props_straw import shide

X, Y, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)
SHU = "paint_shu"
ASH = "ground_ash"
SOOT = "wood_sooted"


# ------------------------------------------------------------------------------------------------ sweep
def sweep(cl, h, d, mat, vis=(1, 2), wear=None, caps=True, top_w=None):
    """Rectangular section swept along the centre line cl = [(x, y), ...] (z = 0 plane): height h across the curve
    (in-plane normal), depth d along z (top_w: a wider top edge, kasagi overhang look). Visual only."""
    tw = d if top_w is None else top_w
    secs = []
    for i, (x, y) in enumerate(cl):
        a = cl[max(0, i - 1)]
        b = cl[min(len(cl) - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / L, tx / L                       # in-plane normal (up for a left-to-right curve)
        if ny < 0:
            nx, ny = -nx, -ny
        lo = (x - nx * h / 2, y - ny * h / 2)
        hi = (x + nx * h / 2, y + ny * h / 2)
        secs.append([(lo[0], lo[1], -d / 2), (lo[0], lo[1], d / 2), (hi[0], hi[1], tw / 2), (hi[0], hi[1], -tw / 2)])
    quads, normals = [], []
    for i in range(len(secs) - 1):
        s0, s1 = secs[i], secs[i + 1]
        for k in range(4):
            q = [s0[k], s0[(k + 1) % 4], s1[(k + 1) % 4], s1[k]]
            c = [sum(p[j] for p in q) / 4 for j in range(3)]
            cc = [(s0[0][j] + s0[2][j] + s1[0][j] + s1[2][j]) / 4 for j in range(3)]
            n = core.norm(core.newell(q))
            if core.dot(n, core.sub(c, cc)) < 0:
                n = core.mul(n, -1.0)
                q = q[::-1]
            quads.append(q)
            normals.append(n)
    if caps:
        for s, sgn in ((secs[0], -1.0), (secs[-1], 1.0)):
            q = list(s)
            n = core.norm(core.newell(q))
            a = cl[0] if sgn < 0 else cl[-1]
            b = cl[1] if sgn < 0 else cl[-2]
            out = core.norm((a[0] - b[0], a[1] - b[1], 0.0))
            if core.dot(n, out) < 0:
                q = q[::-1]
                n = core.mul(n, -1.0)
            quads.append(q)
            normals.append(n)
    s = core.sheet(quads, mat, normals, vis=vis)
    s.grain = "long"
    s.finalize()
    if wear:
        s.wear = wear
    return s


def curve(x0, x1, y_mid, rise, n=8, power=2.0):
    """Centre line from x0 to x1: y = y_mid + rise * |2t-1|^power (upswept ends: sori)."""
    out = []
    for i in range(n + 1):
        t = i / n
        out.append((x0 + (x1 - x0) * t, y_mid + rise * abs(2 * t - 1) ** power))
    return out


# ------------------------------------------------------------------------------------------------ hollow block
def hollow(outer_rings, inner, top_y, floor_y, mat, vis=(1, 2), wear=None, fill=None, fill_mat=LEAF,
           fill_wear="_w2", bottom=False):
    """A stone block with a cut hollow. outer_rings = [(y, [(x, z) * n]), ...] from the bottom up (the last is the rim
    level top_y); inner = [(x, z) * n] the hollow's outline at the rim (same vertex count, counter-clockwise from
    above, like the outer). The hollow has straight walls down to floor_y. fill: a leaf / ash disc at that height.
    Returns [visual solid(s)]."""
    n = len(inner)
    quads, normals = [], []

    def add(q, hint):
        nn = core.norm(core.newell(q))
        if core.dot(nn, hint) < 0:
            q = q[::-1]
            nn = core.mul(nn, -1.0)
        quads.append(q)
        normals.append(nn)
    cx = sum(p[0] for p in inner) / n
    cz = sum(p[1] for p in inner) / n
    for r in range(len(outer_rings) - 1):
        (ya, A), (yb, B) = outer_rings[r], outer_rings[r + 1]
        for i in range(n):
            j = (i + 1) % n
            q = [(A[i][0], ya, A[i][1]), (A[j][0], ya, A[j][1]), (B[j][0], yb, B[j][1]), (B[i][0], yb, B[i][1])]
            mx = (A[i][0] + A[j][0]) / 2 - cx
            mz = (A[i][1] + A[j][1]) / 2 - cz
            add(q, (mx, 0.0, mz))
    T = outer_rings[-1][1]
    for i in range(n):
        j = (i + 1) % n
        add([(T[i][0], top_y, T[i][1]), (T[j][0], top_y, T[j][1]), (inner[j][0], top_y, inner[j][1]),
             (inner[i][0], top_y, inner[i][1])], (0.0, 1.0, 0.0))
        mx = (inner[i][0] + inner[j][0]) / 2 - cx
        mz = (inner[i][1] + inner[j][1]) / 2 - cz
        add([(inner[i][0], top_y, inner[i][1]), (inner[j][0], top_y, inner[j][1]),
             (inner[j][0], floor_y, inner[j][1]), (inner[i][0], floor_y, inner[i][1])], (-mx, 0.0, -mz))
    add([(p[0], floor_y, p[1]) for p in inner], (0.0, 1.0, 0.0))
    if bottom:
        B0 = outer_rings[0]
        add([(p[0], B0[0], p[1]) for p in B0[1]], (0.0, -1.0, 0.0))
    s = core.sheet(quads, mat, normals, vis=vis)
    s.finalize()
    if wear:
        s.wear = wear
    out = [s]
    if fill is not None:
        out.append(flat_poly([(cx + (p[0] - cx) * 1.004, cz + (p[1] - cz) * 1.004) for p in inner], fill, fill_mat,
                             vis=vis, wear=fill_wear))
    return out


def rect(x0, x1, z0, z1):
    """Counter-clockwise (from above) rectangle [(x, z)]: the hollow() vertex order."""
    return [(x0, z1), (x1, z1), (x1, z0), (x0, z0)]


def ring_poly(rx, rz, n, phase=0.0, rr=None, jitter=0.0):
    out = []
    for k in range(n):
        a = phase + 2 * math.pi * k / n
        f = 1.0 + (rr.uniform(-jitter, jitter) if rr else 0.0)
        out.append((rx * f * math.cos(a), -rz * f * math.sin(a)))
    return out


# ------------------------------------------------------------------------------------------------ moss
def moss_strip(pts, w, seed=0, wear="_w1", off=0.004, vis=(1,), frac=(0.0, 1.0)):
    """Moss decal along a polyline of 3D points on a top surface (it lies `off` above them), w wide across (z)."""
    rr = random.Random(seed)
    k0 = int(frac[0] * (len(pts) - 1))
    k1 = max(k0 + 1, int(round(frac[1] * (len(pts) - 1))))
    pts = pts[k0:k1 + 1]
    t = core.mat_info(MOSS)["tile"]
    quads, normals, uvs = [], [], []
    u = rr.random()
    v0 = rr.random()
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        wa = w * (0.6 + 0.4 * rr.random())
        wb = w * (0.6 + 0.4 * rr.random())
        q = [(a[0], a[1] + off, a[2] - wa / 2), (b[0], b[1] + off, b[2] - wb / 2), (b[0], b[1] + off, b[2] + wb / 2),
             (a[0], a[1] + off, a[2] + wa / 2)]
        L = core.length(core.sub(b, a))
        quads.append(q)
        n = core.norm(core.newell(q))
        if n[1] < 0:
            n = core.mul(n, -1.0)
        normals.append(n)
        uvs.append([(u, v0), (u + L / t, v0), (u + L / t, v0 + wb / t), (u, v0 + wa / t)])
        u += L / t
    s = core.sheet(quads, MOSS, normals, vis=vis, uvs=uvs)
    s.finalize()
    s.wear = wear
    return s


def moss_foot(x, z, r, h, n=8, sides=3, seed=0, wear="_w1", y0=0.0, phase=None, off=0.004, facing=-1.0):
    """Moss quads on `sides` faces of an n-sided round post (centre x, z, radius r) on its shady side (facing -z by
    default; +1 for +z), from y0 to y0 + h (ragged top)."""
    rr = random.Random(seed)
    ph = math.pi / n if phase is None else phase
    out = []
    # faces of the post: between angles a_k and a_k+1; the face centre direction (cos, sin) maps to (x, z)
    cands = []
    for k in range(n):
        a0, a1 = ph + 2 * math.pi * k / n, ph + 2 * math.pi * (k + 1) / n
        am = (a0 + a1) / 2
        cands.append((math.sin(am) * facing, k, a0, a1))
    cands.sort(reverse=True)
    t = core.mat_info(MOSS)["tile"]
    rp = r * math.cos(math.pi / n) + off
    for _, k, a0, a1 in cands[:sides]:
        hh = h * (0.6 + 0.4 * rr.random())
        R = r + off / math.cos(math.pi / n)
        p0 = (x + R * math.cos(a0), y0, z + R * math.sin(a0))
        p1 = (x + R * math.cos(a1), y0, z + R * math.sin(a1))
        q = [p0, p1, (p1[0], y0 + hh, p1[2]), (p0[0], y0 + hh, p0[2])]
        am = (a0 + a1) / 2
        nn = (math.cos(am), 0.0, math.sin(am))
        w = core.length(core.sub(p1, p0))
        u, v = rr.random(), rr.random()
        s = core.sheet([q], MOSS, nn, vis=(1,), uvs=[[(u, v + hh / t), (u + w / t, v + hh / t), (u + w / t, v), (u, v)]])
        s.finalize()
        s.wear = wear
        out.append(s)
    del rp
    return out


# ------------------------------------------------------------------------------------------------ transforms
def shear(ss, k, y0=0.0, axis="x"):
    """Rack solids: x (or z) += k * (y - y0). Recomputes normals / uvs (smooth vertex normals dropped)."""
    out = []
    for s in ss:
        s.finalize()
        n = xf(s)
        if axis == "x":
            n.verts = [(v[0] + k * (v[1] - y0), v[1], v[2]) for v in n.verts]
        else:
            n.verts = [(v[0], v[1], v[2] + k * (v[1] - y0)) for v in n.verts]
        n.center = tuple(sum(v[j] for v in n.verts) / len(n.verts) for j in range(3))
        if n.normals is not None:
            hint = []
            for fi, f in enumerate(n.faces):
                q = [n.verts[i] for i in f]
                nn = core.norm(core.newell(q))
                if core.dot(nn, s.fn[fi]) < 0:
                    nn = core.mul(nn, -1.0)
                hint.append(nn)
            n.normals = hint
        explicit_uv = isinstance(n.uv, list)
        keep_uv = [list(u) for u in s.fuv]
        if explicit_uv:
            n.uv = keep_uv                       # per (already split) face
        n.fm = None
        n.fn = None
        if hasattr(n, "vn"):
            n.vn = None
        n.finalize()
        if explicit_uv or getattr(s, "cell", None) or n.mats in (MOSS, CTEXT, SUMI):
            n.fuv = keep_uv
        for a in ("cell", "_text_faced"):
            if hasattr(s, a):
                setattr(n, a, getattr(s, a))
        out.append(n)
    return out


def tilt(ss, rx=0.0, rz=0.0, ry=0.0, pivot=(0.0, 0.0, 0.0), sink=0.0):
    """Lean a group about its base pivot, then sink it into the ground by `sink`. Keeps decal attributes."""
    out = []
    for s in ss:
        n = xf(s, rx=rx, ry=ry, rz=rz, pivot=pivot, t=(0.0, -sink, 0.0))
        for a in ("cell", "_text_faced"):
            if hasattr(s, a):
                setattr(n, a, getattr(s, a))
        out.append(n)
    return out


# ------------------------------------------------------------------------------------------------ text
def carved(center, right, up, h, cellname, wear="_w1", crop=None, width=None, off=0.003, vis=(1,), mat=CTEXT):
    """Carved text from B1's atlas (jp_m_decal_carved_text; M1: mat=GTEXT for the grave names atlas); faced and
    un-mirrored by build.py (skit.face_text)."""
    return text_on(center, right, up, h, mat, cellname, wear=wear, off=off, vis=vis, width=width, crop=crop)


def inked(center, right, up, h, cellname, wear="_w2", crop=None, width=None, off=0.003, vis=(1,), mat=SUMI):
    """Brush text from B1's sumi atlas (plaques, sotoba; M1: mat=GSUMI for the grave-post names atlas)."""
    return text_on(center, right, up, h, mat, cellname, wear=wear, off=off, vis=vis, width=width, crop=crop)


# ------------------------------------------------------------------------------------------------ rope
def torii_rope(x0, x1, y, z, r=0.04, drop=0.10, with_shide=True, wear="_w2", seed=1, n_tassel=None):
    """A straw rope (shimenawa) hung between (x0, y, z) and (x1, y, z), sagging `drop`: FP1 (2026-10-01) twisted
    straw strands (twisted_rope), straw tassels (shibe, tassel()) between, paper shide (4-step zigzag,
    props_straw.shide) if with_shide. Visual only."""
    rr = random.Random(seed)
    a, b = (x0, y, z), (x1, y, z)
    pts = sag(a, b, drop, 8)
    out = twisted_rope(pts, r, seed=seed, wear=wear)
    L = abs(x1 - x0)
    nt = n_tassel or max(2, int(L / 0.45))
    for i in range(nt):
        t = (i + 0.5) / nt
        xx = x0 + (x1 - x0) * t
        yy = y - drop * 4 * t * (1 - t) - r * 0.8
        if with_shide and i % 2 == 1:
            out.append(shide((xx, yy, z + 0.01), s=0.24 + rr.uniform(-0.04, 0.03), wear=wear))
        else:
            ln = 0.18 + rr.uniform(-0.04, 0.05)
            if r < 0.02:                                         # a mini torii's cord: one thin tuft
                out.append(pole((xx, yy, z), (xx + rr.uniform(-0.02, 0.02), yy - ln, z + 0.01), 0.012, ROPE, n=4,
                                vis=(1,), r1=0.005, wear=wear))
            else:
                out += tassel((xx, yy, z), ln, seed * 31 + i, wear=wear)
    return out


def ring_band(r, y0, y1, mat, n=8, vis=(1,), wear=None):
    s = lathe([(r, y0), (r, y1)], n, mat, vis=vis, smooth=True)
    if wear:
        s.wear = wear
    return s


def pebbles(seed, cx, cz, r0, n=5, mat=RIVER, vis=(1,), size=0.05):
    rr = random.Random(seed)
    out = []
    for k in range(n):
        a = rr.uniform(0, 2 * math.pi)
        d = rr.uniform(0, r0)
        s = size * rr.uniform(0.6, 1.3)
        out.append(core.stone(rr, cx + d * math.cos(a), cz + d * math.sin(a), s * 1.3, s, s * 0.7, s * 0.55, mat,
                              bury=0.01, n=5, vis=vis))
    return out


# ------------------------------------------------------------------------------------------------ FP1: aged stone
AGED = "stone_carved_aged"


def aged_stone(solids, seed, frm=(CARVED,), to=AGED, scale=0.5):
    """FP1 (2026-10-01, Stephen: the stone torii's lichen dots repeat in a pattern). Every visual face in `frm`
    (stone_carved, a 1 m tile of round lichen dots) moves to jp_m_stone_carved_aged (a 2 m tile of irregular lichen
    rosettes): its world-scale uv is scaled by `scale` (1 m -> 2 m tile, same texel density), then each piece (solid)
    gets its own random turn and shift, so neighbouring pieces never show the same patch. Text decals are untouched.
    Lists are replaced, not edited in place (xf() copies share them)."""
    rg = random.Random(seed)
    for s in solids:
        if not s.vis:
            continue
        s.finalize()
        if not any(m in frm for m in s.fm):
            continue
        a = rg.uniform(0.0, 2 * math.pi)
        c, sn = math.cos(a), math.sin(a)
        ou, ov = rg.uniform(0.0, 1.0), rg.uniform(0.0, 1.0)
        fm, fuv = list(s.fm), [list(f) for f in s.fuv]
        for fi, m in enumerate(fm):
            if m in frm:
                fm[fi] = to
                fuv[fi] = [((u * c - v * sn) * scale + ou, (u * sn + v * c) * scale + ov) for u, v in fuv[fi]]
        s.fm, s.fuv = fm, fuv
    return solids


# ------------------------------------------------------------------------------------------------ FP1: twisted rope
def _catmull(pts, step):
    """Resample a polyline as a Catmull-Rom curve with points about `step` apart (keeps the end points)."""
    P = [core.add(pts[0], core.sub(pts[0], pts[1]))] + list(pts) + [core.add(pts[-1], core.sub(pts[-1], pts[-2]))]
    out = [tuple(pts[0])]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        n = max(1, int(math.ceil(core.length(core.sub(p2, p1)) / step)))
        for k in range(1, n + 1):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                    + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in range(3)))
    return out


def _frames(path):
    """Tangents and parallel-transported normals along a path."""
    T = []
    for i in range(len(path)):
        a, b = path[max(0, i - 1)], path[min(len(path) - 1, i + 1)]
        T.append(core.norm(core.sub(b, a)))
    ref = (0.0, 1.0, 0.0) if abs(T[0][1]) < 0.9 else (1.0, 0.0, 0.0)
    N = [core.norm(core.cross(core.cross(T[0], ref), T[0]))]
    for i in range(1, len(path)):
        n = core.sub(N[-1], core.mul(T[i], core.dot(N[-1], T[i])))
        N.append(core.norm(n) if core.length(n) > 1e-6 else N[-1])
    B = [core.norm(core.cross(T[i], N[i])) for i in range(len(path))]
    return T, N, B


def _tube(centres, T, radius, sides, mat, vis, wear, phase=0.0, tile=0.5, cap0=True, cap1=True, taper=None):
    """A tube through `centres` (frames from T): one sheet solid with smooth normals; capped ends."""
    _, N, B = _frames(centres) if len(centres) > 2 else (T, None, None)
    if N is None:
        ref = (0.0, 1.0, 0.0) if abs(T[0][1]) < 0.9 else (1.0, 0.0, 0.0)
        N = [core.norm(core.cross(core.cross(t, ref), t)) for t in T]
        B = [core.norm(core.cross(t, n)) for t, n in zip(T, N)]
    rings, dirs, vacc = [], [], [0.0]
    for i, c in enumerate(centres):
        if i:
            vacc.append(vacc[-1] + core.length(core.sub(c, centres[i - 1])))
        rr = radius * (taper(i / max(1, len(centres) - 1)) if taper else 1.0)
        ring, dr = [], []
        for k in range(sides):
            a = phase + 2 * math.pi * k / sides
            d = core.add(core.mul(N[i], math.cos(a)), core.mul(B[i], math.sin(a)))
            ring.append(core.add(c, core.mul(d, rr)))
            dr.append(d)
        rings.append(ring)
        dirs.append(dr)
    quads, normals, uvs, vn = [], [], [], []
    circ = 2 * math.pi * radius / tile
    for i in range(len(rings) - 1):
        for k in range(sides):
            k2 = (k + 1) % sides
            q = [rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]]
            quads.append(q)
            normals.append(core.norm(core.add(core.add(dirs[i][k], dirs[i][k2]), core.add(dirs[i + 1][k], dirs[i + 1][k2]))))
            uvs.append([(circ * k / sides, vacc[i] / tile), (circ * (k + 1) / sides, vacc[i] / tile),
                        (circ * (k + 1) / sides, vacc[i + 1] / tile), (circ * k / sides, vacc[i + 1] / tile)])
            vn.append([dirs[i][k], dirs[i][k2], dirs[i + 1][k2], dirs[i + 1][k]])
    for end, on in ((0, cap0), (len(rings) - 1, cap1)):
        if not on or len(rings[end]) < 3:
            continue
        tn = core.mul(T[end], -1.0 if end == 0 else 1.0)
        c = centres[end]
        for k in range(sides):
            q = [c, rings[end][k], rings[end][(k + 1) % sides]]
            quads.append(q)
            normals.append(tn)
            uvs.append([(0.5, 0.5), (0.5 + 0.1 * math.cos(2 * math.pi * k / sides), 0.5),
                        (0.5, 0.5 + 0.1 * math.sin(2 * math.pi * k / sides))])
            vn.append([tn, tn, tn])
    s = core.sheet(quads, mat, normals, vis=vis, uvs=uvs)
    s.finalize()
    s.vn = vn
    if wear:
        s.wear = wear
    return s


def straw_fray(p, d, r, seed, n=7, length=(0.06, 0.16), wear="_w2", spread=0.55, vis=(1,)):
    """A frayed rope end at p, pointing along d: loose straws splaying out in a cone."""
    rg = random.Random(seed)
    d = core.norm(d)
    ref = (0.0, 1.0, 0.0) if abs(d[1]) < 0.9 else (1.0, 0.0, 0.0)
    a1 = core.norm(core.cross(d, ref))
    a2 = core.norm(core.cross(d, a1))
    out = []
    for _ in range(n):
        th = rg.uniform(0, 2 * math.pi)
        sp = rg.uniform(0.15, spread)
        o = core.add(core.mul(a1, math.cos(th) * r * 0.6), core.mul(a2, math.sin(th) * r * 0.6))
        dirn = core.norm(core.add(d, core.add(core.mul(a1, math.cos(th) * sp), core.mul(a2, math.sin(th) * sp))))
        dirn = core.norm(core.add(dirn, (0.0, -0.25 * rg.random(), 0.0)))        # straws droop
        L = rg.uniform(*length)
        p0 = core.add(p, o)
        p1 = core.add(p0, core.mul(dirn, L))
        p1 = (p1[0], max(p1[1], 0.004), p1[2])                                # never into the ground
        out.append(pole(p0, p1, max(0.004, r * 0.14), ROPE, n=3, vis=vis, r1=0.0015, wear=wear))
    return out


def twisted_rope(pts, r, seed=1, strands=2, sides=None, wear="_w2", vis=(1,), fray0=False, fray1=False, lod2=True,
                 pitch=None):
    """FP1 (2026-10-01, Stephen: the torii's snapped rope 'needs fidelity'): a straw shimenawa as `strands` twisted
    straw strands (left-laid, hidari-nai, as a shimenawa is) along a smooth curve through pts, each strand a round tube
    whose tile runs along the straw; frayed straw ends where the rope ends free (fray0 / fray1). LOD 2: one plain
    4-sided tube. Visual only."""
    pitch = pitch or max(0.15, 8.0 * r)
    if r < 0.02:                                         # a cord (mini torii): one plain strand
        strands, sides = 1, 4
    elif sides is None:
        sides = 4 if r >= 0.05 else 3
    path = _catmull(pts, pitch / 4.0)
    T, N, B = _frames(path)
    sacc = [0.0]
    for i in range(1, len(path)):
        sacc.append(sacc[-1] + core.length(core.sub(path[i], path[i - 1])))
    off = r * {1: 0.0, 2: 0.42, 3: 0.48}[strands]
    rs = r * {1: 1.0, 2: 0.62, 3: 0.52}[strands]
    out = []
    for k in range(strands):
        cs = []
        for i, c in enumerate(path):
            th = 2 * math.pi * k / strands - 2 * math.pi * sacc[i] / pitch      # left-laid
            d = core.add(core.mul(N[i], math.cos(th)), core.mul(B[i], math.sin(th)))
            cs.append(core.add(c, core.mul(d, off)))
        out.append(_tube(cs, T, rs, sides, ROPE, vis, wear, phase=0.3 * k))
    rg = random.Random(seed)
    if fray0:
        out += straw_fray(path[0], core.mul(T[0], -1.0), r, rg.randint(0, 9999), wear=wear, vis=vis)
    if fray1:
        out += straw_fray(path[-1], T[-1], r, rg.randint(0, 9999), wear=wear, vis=vis)
    if lod2:
        coarse = _catmull(pts, max(0.25, pitch))
        T2, _, _ = _frames(coarse)
        out.append(_tube(coarse, T2, r, 4, ROPE, (2,), wear))
    return out


def tassel(p, length, seed, wear="_w2", vis=(1,)):
    """A straw tassel (shibe) hanging from p: three tapered straw bundles fanning slightly, tied at the top."""
    rg = random.Random(seed)
    out = []
    for k in range(3):
        a = 2 * math.pi * k / 3 + rg.uniform(-0.3, 0.3)
        q = (p[0] + 0.035 * math.cos(a) + rg.uniform(-0.01, 0.01), p[1] - length * rg.uniform(0.85, 1.05),
             p[2] + 0.035 * math.sin(a))
        out.append(pole(p, q, 0.016, ROPE, n=4, vis=vis, r1=0.004, wear=wear))
    out.append(pole((p[0], p[1] + 0.012, p[2]), (p[0], p[1] - 0.03, p[2]), 0.019, ROPE, n=5, vis=vis, wear=wear))
    return out
