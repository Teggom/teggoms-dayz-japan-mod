"""bits - small shared pieces for the B3a props: vessels, lids, shards, spills, cloth, pillows."""
import math
import random

import fkit
from fkit import core, box, prism, ngon, sheet, lathe, xf, flat_poly, W, WOOD, IRON, DARK, PALE, LITTER, PAPER


def rng_for(name):
    return random.Random(core.hash_str(name))


def jag_rim(s, ytop, amp, seed, drop=None):
    """Make a lathe's top ring (verts at y == ytop) jagged: y += random(-amp, 0) per angle; drop=(a0, a1, depth)
    lowers an arc (radians) further (a broken-out piece)."""
    r = random.Random(seed)
    cache = {}
    nv = []
    for v in s.verts:
        if abs(v[1] - ytop) < 1e-6:
            a = math.atan2(v[2], v[0]) % (2 * math.pi)
            k = round(a, 4)
            if k not in cache:
                d = -r.uniform(0.0, amp)
                if drop and drop[0] <= a <= drop[1]:
                    d -= drop[2] * math.sin(math.pi * (a - drop[0]) / (drop[1] - drop[0])) ** 0.6
                cache[k] = d
            v = (v[0], v[1] + cache[k], v[2])
        nv.append(v)
    s.verts = nv
    return s


def shards(seed, cx, cz, spread, n, mat=PALE, size=(0.03, 0.08), wear="_w1", vis=(1,)):
    """Broken pottery on the floor: small flat triangular/quad chips (visual only)."""
    r = random.Random(seed)
    out = []
    for i in range(n):
        s = r.uniform(*size)
        k = r.choice((3, 4))
        pts = [(s / 2 * math.cos(2 * math.pi * j / k + r.uniform(-0.3, 0.3)) * r.uniform(0.6, 1.0),
                s / 2 * math.sin(2 * math.pi * j / k + r.uniform(-0.3, 0.3)) * r.uniform(0.6, 1.0)) for j in range(k)]
        pts = core.hull2d(pts)
        if len(pts) < 3:
            continue
        p = prism(pts, "y", 0.0, 0.006, mat, vis=vis)
        a = r.uniform(0, 360)
        p = xf(p, rx=r.uniform(-8, 8), ry=a, t=(cx + r.uniform(-spread, spread), 0.004, cz + r.uniform(-spread, spread)))
        p.wear = wear
        out.append(p)
    return out


def blob(seed, r0, n=9, jitter=0.25, sx=1.0, sz=1.0):
    """Irregular convex outline [(x, z)] counter-clockwise, radius ~r0."""
    r = random.Random(seed)
    pts = [(r0 * sx * (1 + r.uniform(-jitter, jitter)) * math.cos(2 * math.pi * k / n + r.uniform(-0.2, 0.2)),
            r0 * sz * (1 + r.uniform(-jitter, jitter)) * math.sin(2 * math.pi * k / n + r.uniform(-0.2, 0.2)))
           for k in range(n)]
    return core.hull2d(pts)


def stain(seed, cx, cz, r0, y=0.003, mat=LITTER, wear="_w2", vis=(1,), sx=1.0, sz=1.0):
    pts = [(cx + x, cz + z) for x, z in blob(seed, r0, sx=sx, sz=sz)]
    return flat_poly(pts, y, mat, vis=vis, wear=wear, uvoff=(random.Random(seed).random(), 0.37))


def mound(seed, cx, cz, r0, h, mat, sx=1.0, sz=1.0, wear=None, vis=(1, 2)):
    """A low spill mound (rice, ash, salt): an irregular cone frustum, closed, visual only."""
    base = [(cx + x, cz + z) for x, z in blob(seed, r0, n=8, sx=sx, sz=sz)]
    top = [(cx + (x - cx) * 0.35, cz + (z - cz) * 0.35) for x, z in base]
    verts = [(x, 0.001, z) for x, z in base] + [(x, h, z) for x, z in top]
    n = len(base)
    faces = [list(range(n))[::-1], list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    s = fkit.Solid(verts, faces, mat, vis=vis)
    if wear:
        s.wear = wear
    return s


def disc(r, y0, y1, mat, n=10, vis=(1, 2), cx=0.0, cz=0.0, wear=None):
    """Flat round board / lid: closed cylinder as a lathe (top face = triangles from the centre)."""
    s = lathe([(0.0, y0), (r, y0), (r, y1), (0.0, y1)], n, mat, vis=vis)
    if cx or cz:
        s = xf(s, t=(cx, 0.0, cz))
    if wear:
        s.wear = wear
    return s


def jar_profile(d, h, mouth=0.60, open_top=True):
    """Stoneware storage jar (tsubo): foot, shoulder, short neck, rolled lip; interior down to 0.72 h."""
    R = d / 2
    out = [(0.0, 0.0), (0.72 * R, 0.0), (0.82 * R, 0.07 * h), (0.97 * R, 0.33 * h), (R, 0.58 * h),
           (0.92 * R, 0.78 * h), (mouth * R + 0.02 * R, 0.92 * h), (mouth * R, 0.965 * h), (mouth * R + 0.05 * R, h)]
    if open_top:
        out += [(mouth * R - 0.06 * R, h), (mouth * R - 0.08 * R, 0.88 * h), (0.60 * R, 0.72 * h), (0.0, 0.70 * h)]
    else:
        out += [(0.0, h)]
    return out


def jar(d, h, mat=DARK, n=10, lid=True, name="jar", wear=None, vis=(1, 2), mouth=0.60):
    """[solids], lid top y. A jar with a wooden board lid resting on the lip."""
    s = lathe(jar_profile(d, h, mouth), n, mat, vis=vis, wear=wear)
    out = [s]
    top = h
    if lid:
        r = mouth * d / 2 + 0.05 * d / 2 + 0.012
        out.append(disc(r, h, h + 0.02, WOOD, n=max(8, n - 2), vis=vis))
        out.append(W(-0.012, 0.012, h + 0.02, h + 0.035, -r * 0.7, r * 0.7, vis=(1,)))
        top = h + 0.02
    return out, top


def jar_lod2(d, h, mat=DARK, n=6, lid=True):
    s = lathe([(0.0, 0.0), (0.36 * d, 0.0), (0.5 * d, 0.5 * h), (0.34 * d, h), (0.0, h + (0.02 if lid else 0.0))],
              n, mat, vis=(2,))
    return [s]


def cloth_patch(cx, cz, w, d, yaw, mat=fkit.INDIGO, h=0.012, wear="_w2", vis=(1,)):
    s = fkit.rotated_box(cx, cz, w, d, 0.0, h, yaw, mat, vis=vis)
    s.wear = wear
    return s


def pillow(w, d, h, mat, nx=4, nz=3, pinch=0.25, wear=None, vis=(1, 2), sag=0.0):
    """A stuffed straw bag / bedding roll: flat bottom, domed top grid (visual only, closed by explicit normals)."""
    def top_y(u, v):         # u, v in [-1, 1]
        return h * (pinch + (1 - pinch) * (1 - abs(u) ** 3) * (1 - abs(v) ** 3)) - sag * (1 - u * u)
    xs = [-w / 2 + w * i / nx for i in range(nx + 1)]
    zs = [-d / 2 + d * j / nz for j in range(nz + 1)]
    quads, normals, uvs = [], [], []
    t = core.mat_info(mat)["tile"]
    for i in range(nx):
        for j in range(nz):
            q = []
            for (a, b) in ((i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)):
                q.append((xs[a], top_y(2 * a / nx - 1, 2 * b / nz - 1), zs[b]))
            n = core.norm(core.newell(q))
            if n[1] < 0:
                n = core.mul(n, -1.0)
                q = q[::-1]
            quads.append(q)
            normals.append(n)
            uvs.append([(p[0] / t, p[2] / t) for p in q])
    ring = [(i, 0) for i in range(nx)] + [(nx, j) for j in range(nz)] + [(i, nz) for i in range(nx, 0, -1)] + \
        [(0, j) for j in range(nz, 0, -1)]
    for k in range(len(ring)):
        a, b = ring[k], ring[(k + 1) % len(ring)]
        pa = (xs[a[0]], top_y(2 * a[0] / nx - 1, 2 * a[1] / nz - 1), zs[a[1]])
        pb = (xs[b[0]], top_y(2 * b[0] / nx - 1, 2 * b[1] / nz - 1), zs[b[1]])
        q = [(pa[0], 0.0, pa[2]), (pb[0], 0.0, pb[2]), pb, pa]
        mid = ((pa[0] + pb[0]) / 2, 0, (pa[2] + pb[2]) / 2)
        n = core.norm((mid[0] / (w / 2) ** 2, 0.0, mid[2] / (d / 2) ** 2))
        quads.append(q)
        normals.append(n)
        L = math.hypot(pb[0] - pa[0], pb[2] - pa[2])
        uvs.append([(0, 0), (L / t, 0), (L / t, pa[1] / t), (0, pa[1] / t)])
    quads.append([(-w / 2, 0.0, -d / 2), (w / 2, 0.0, -d / 2), (w / 2, 0.0, d / 2), (-w / 2, 0.0, d / 2)])
    normals.append((0.0, -1.0, 0.0))
    uvs.append([(0, 0), (w / t, 0), (w / t, d / t), (0, d / t)])
    s = sheet(quads, mat, normals, vis=vis, uvs=uvs)
    if wear:
        s.wear = wear
    return s


def rope_ring(r, y, width, mat, n, vis=(1,), proud=0.008):
    """A rope / hoop band: the outer strip only, a little proud of radius r (cheap: n faces + 2n edges)."""
    return lathe([(r - 0.001, y - width / 2), (r + proud, y - width / 2 + 0.003), (r + proud, y + width / 2 - 0.003),
                  (r - 0.001, y + width / 2)], n, mat, vis=vis)
