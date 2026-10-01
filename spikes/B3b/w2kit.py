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
    """A straw rope (shimenawa) hung between (x0, y, z) and (x1, y, z), sagging `drop`: two twisted strands, straw
    tassels (shibe) between, paper shide (4-step zigzag, props_straw.shide) if with_shide. Visual only."""
    rr = random.Random(seed)
    a, b = (x0, y, z), (x1, y, z)
    pts = sag(a, b, drop, 8)
    out = rope_path(pts, r, ROPE, n=6, wear=wear)
    out += rope_path([core.add(p, (0.0, 0.012, 0.010)) for p in pts], r * 0.55, ROPE, n=4, wear=wear)
    L = abs(x1 - x0)
    nt = n_tassel or max(2, int(L / 0.45))
    for i in range(nt):
        t = (i + 0.5) / nt
        xx = x0 + (x1 - x0) * t
        yy = y - drop * 4 * t * (1 - t) - r
        if with_shide and i % 2 == 1:
            out.append(shide((xx, yy, z + 0.01), s=0.24 + rr.uniform(-0.04, 0.03), wear=wear))
        else:
            ln = 0.18 + rr.uniform(-0.04, 0.05)
            out.append(pole((xx, yy, z), (xx + rr.uniform(-0.02, 0.02), yy - ln, z + 0.01), 0.022, ROPE, n=4, vis=(1,),
                            r1=0.010, wear=wear))
    lo = core.sheet([[(x0, y + r, z), (x1, y + r, z), (x1, y - drop - r, z), (x0, y - drop - r, z)]], ROPE,
                    (0.0, 0.0, 1.0), vis=(2,))
    lo2 = core.sheet([[(x1, y + r, z), (x0, y + r, z), (x0, y - drop - r, z), (x1, y - drop - r, z)]], ROPE,
                     (0.0, 0.0, -1.0), vis=(2,))
    for s in (lo, lo2):
        s.finalize()
        s.wear = wear
    out += [lo, lo2]
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
