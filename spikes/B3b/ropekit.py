"""ropekit - FP2 (2026-10-01): the shared rope geometry. Stephen (re-check): rope needs "2.5x more segments"; the coils
on the pegs read octagonal (4_rope_coils_polygonal.webp).

ROPE_K = 2.5 multiplies, at every rope helper, BOTH the sides round the rope's cross-section and the segments along its
path / round its coil (kit helpers: skit.rope_path / skit.cord_tube, lkit.cord / coil / flat_coil, w2kit.twisted_rope /
torii_rope, bits.rope_ring (cross-section only: a tie lies on its host's facets), fp1sword._cord, props_wood's load and
laundry ties). Ropes are smooth-shaded tubes (per-vertex normals), continuous along a Catmull-Rom curve through the
given points (rope_path used to be one capped prism per segment, so every bend showed a kink and a seam). Lower LODs
keep their old, cheap shapes (only the Res 1 copy is refined).
"""
import math

import fkit
from fkit import core

ROPE_K = 2.5


def rk(n, k=ROPE_K):
    """n sides / segments -> about 2.5x (at least one more); k <= 1 leaves n."""
    if k <= 1.0:
        return n
    return max(n + 1, int(round(n * k)))


def is_rope(mat):
    """Rope and cord materials (straw rope, cotton / hemp cords and threads). Other things drawn with the rope
    helpers (a bent wooden handle, grass stems, a pine trunk) get the smooth tube but keep their counts."""
    m = str(mat)
    return m.startswith("straw_rope") or m.startswith("textile_")


def catmull(pts, step):
    """Resample a polyline as a Catmull-Rom curve with points about `step` apart (keeps the end points)."""
    pts = [tuple(float(c) for c in p) for p in pts]
    if len(pts) < 2:
        return pts
    P = [core.add(pts[0], core.sub(pts[0], pts[1]))] + list(pts) + [core.add(pts[-1], core.sub(pts[-1], pts[-2]))]
    out = [pts[0]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        n = max(1, int(math.ceil(core.length(core.sub(p2, p1)) / step)))
        for k in range(1, n + 1):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                    + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in range(3)))
    return out


def resample(pts, k=ROPE_K):
    """2.5x the segments along a rope's path: a straight 2-point rope stays one segment (more would add nothing);
    a bent path becomes a smooth curve with k times as many segments as it had."""
    if len(pts) < 3:
        return [tuple(float(c) for c in p) for p in pts]
    L = sum(core.length(core.sub(pts[i + 1], pts[i])) for i in range(len(pts) - 1))
    nseg = int(round((len(pts) - 1) * k))
    return catmull(pts, L / max(1, nseg) * 0.999)


def frames(path):
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


def tube(path, r, sides, mat, vis=(1,), wear=None, caps=True, tile=None, phase=0.0, taper=None, cull=None):
    """A smooth round tube through `path`: quads with per-vertex normals; caps as a quad fan (few faces).
    cull(normal, ring index, quad centre) -> True drops a side quad that can never be seen (inside the other strand
    of a laid rope, against a trunk). Returns a solid (or None if empty)."""
    T, N, B = frames(path)
    tile = tile or core.mat_info(mat)["tile"]
    rings, dirs, vacc = [], [], [0.0]
    for i, c in enumerate(path):
        if i:
            vacc.append(vacc[-1] + core.length(core.sub(c, path[i - 1])))
        rr = r * (taper(i / max(1, len(path) - 1)) if taper else 1.0)
        ring, dr = [], []
        for k in range(sides):
            a = phase + 2 * math.pi * k / sides
            d = core.add(core.mul(N[i], math.cos(a)), core.mul(B[i], math.sin(a)))
            ring.append(core.add(c, core.mul(d, rr)))
            dr.append(d)
        rings.append(ring)
        dirs.append(dr)
    quads, normals, uvs, vn = [], [], [], []
    circ = 2 * math.pi * r / tile
    for i in range(len(rings) - 1):
        for k in range(sides):
            k2 = (k + 1) % sides
            nrm = core.norm(core.add(core.add(dirs[i][k], dirs[i][k2]), core.add(dirs[i + 1][k], dirs[i + 1][k2])))
            if cull:
                qc = tuple((rings[i][k][c] + rings[i][k2][c] + rings[i + 1][k][c] + rings[i + 1][k2][c]) / 4
                           for c in range(3))
                if cull(nrm, i, qc):
                    continue
            quads.append([rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]])
            normals.append(nrm)
            uvs.append([(circ * k / sides, vacc[i] / tile), (circ * (k + 1) / sides, vacc[i] / tile),
                        (circ * (k + 1) / sides, vacc[i + 1] / tile), (circ * k / sides, vacc[i + 1] / tile)])
            vn.append([dirs[i][k], dirs[i][k2], dirs[i + 1][k2], dirs[i + 1][k]])
    if caps:
        for end in (0, len(rings) - 1):
            tn = core.mul(T[end], -1.0 if end == 0 else 1.0)
            ring = rings[end] if end else rings[end][::-1]
            k = 1
            while k < sides - 1:                       # quad fan
                idx = [0, k, k + 1, k + 2] if k + 2 < sides else [0, k, k + 1]
                q = [ring[j] for j in idx]
                quads.append(q)
                normals.append(tn)
                uvs.append([(0.5 + 0.02 * j, 0.5) for j in range(len(q))])
                vn.append([tn] * len(q))
                k += len(idx) - 2
    if not quads:
        return None
    s = core.sheet(quads, mat, normals, vis=vis, uvs=uvs)
    s.finalize()
    s.vn = vn
    if wear:
        s.wear = wear
    return s


def rope_tube(pts, r, n, mat, vis=(1,), wear=None, caps=True, k=ROPE_K, cull=None):
    """A rope through pts with 2.5x the sides (n -> rk(n)) and 2.5x the segments along a bent path."""
    return tube(resample(pts, k), r, rk(n, k), mat, vis=vis, wear=wear, caps=caps, cull=cull)
