"""Geometry helpers for W's garment generators (numpy only; no scipy).

Frames: everything is DayZ model space in the player's BIND pose: X = the character's left, Y up, the bind pose
faces -Z (see REPORT.md). Faces are wound so that, read through the render's (x, z, y) mirror, they are
counter-clockwise from outside - which is the p3d's clockwise-from-outside (same rule the Pokemon tools use).
"""
import numpy as np


def unit(v, axis=-1):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v, axis=axis, keepdims=True)
    n[n == 0] = 1.0
    return v / n


def smoothstep(e0, e1, x):
    t = np.clip((np.asarray(x, dtype=float) - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def weld(P, tol=1e-5):
    """-> (unique points, map old index -> welded index)"""
    key = np.round(np.asarray(P) / tol).astype(np.int64)
    _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    return np.asarray(P)[first], inv.reshape(-1)


def tris(F):
    out = []
    for f in F:
        if len(f) == 3:
            out.append(list(f))
        else:
            out.append([f[0], f[1], f[2]])
            out.append([f[0], f[2], f[3]])
    return np.array(out, dtype=np.int64)


def face_normals(P, T):
    a, b, c = P[T[:, 0]], P[T[:, 1]], P[T[:, 2]]
    # the mirror (x, y, z) -> (x, z, y) flips handedness; the outward normal in DayZ axes of a face that is
    # CCW in the mirrored (Blender) frame is -cross(b - a, c - a) evaluated in DayZ axes
    return unit(-np.cross(b - a, c - a))


def vertex_normals(P, T):
    fn = face_normals(P, T)
    a, b, c = P[T[:, 0]], P[T[:, 1]], P[T[:, 2]]
    area = np.linalg.norm(np.cross(b - a, c - a), axis=1, keepdims=True)
    vn = np.zeros_like(P)
    for k in range(3):
        np.add.at(vn, T[:, k], fn * area)
    return unit(vn)


def closest_point_on_triangles(p, A, B, C):
    """closest points from one point p to many triangles (vectorised, Ericson's method).
    -> (points (n,3), barycentric (n,3))"""
    ab, ac, ap = B - A, C - A, p - A
    d1 = np.einsum("ij,ij->i", ab, ap)
    d2 = np.einsum("ij,ij->i", ac, ap)
    bp = p - B
    d3 = np.einsum("ij,ij->i", ab, bp)
    d4 = np.einsum("ij,ij->i", ac, bp)
    cp = p - C
    d5 = np.einsum("ij,ij->i", ab, cp)
    d6 = np.einsum("ij,ij->i", ac, cp)
    n = len(A)
    bary = np.zeros((n, 3))
    # default: inside
    va = d3 * d6 - d5 * d4
    vb = d5 * d2 - d1 * d6
    vc = d1 * d4 - d3 * d2
    denom = va + vb + vc
    denom[denom == 0] = 1e-30
    v = vb / denom
    w = vc / denom
    bary[:, 0], bary[:, 1], bary[:, 2] = 1 - v - w, v, w
    # region tests (order matters: later assignments override)
    m = (vc <= 0) & (d1 >= 0) & (d3 <= 0)
    t = d1 / np.where(d1 - d3 == 0, 1e-30, d1 - d3)
    bary[m] = np.stack([1 - t[m], t[m], np.zeros(m.sum())], 1)
    m2 = (vb <= 0) & (d2 >= 0) & (d6 <= 0)
    t = d2 / np.where(d2 - d6 == 0, 1e-30, d2 - d6)
    bary[m2] = np.stack([1 - t[m2], np.zeros(m2.sum()), t[m2]], 1)
    m3 = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0)
    t = (d4 - d3) / np.where((d4 - d3) + (d5 - d6) == 0, 1e-30, (d4 - d3) + (d5 - d6))
    bary[m3] = np.stack([np.zeros(m3.sum()), 1 - t[m3], t[m3]], 1)
    ma = (d1 <= 0) & (d2 <= 0)
    bary[ma] = [1, 0, 0]
    mb = (d3 >= 0) & (d4 <= d3)
    bary[mb] = [0, 1, 0]
    mc = (d6 >= 0) & (d5 <= d6)
    bary[mc] = [0, 0, 1]
    pts = bary[:, :1] * A + bary[:, 1:2] * B + bary[:, 2:] * C
    return pts, bary


class Surface:
    """A reference triangle surface with per-vertex attributes (weights as dicts, UVs) and closest-point
    queries. Candidate triangles come from the k nearest vertices, which is plenty for garment-to-body."""

    def __init__(self, P, T, weights=None, uvs=None):
        self.P = np.asarray(P, dtype=float)
        self.T = np.asarray(T, dtype=np.int64)
        self.W = weights
        self.UV = None if uvs is None else np.asarray(uvs, dtype=float)
        self.vert_tris = [[] for _ in range(len(self.P))]
        for ti, t in enumerate(self.T):
            for v in t:
                self.vert_tris[v].append(ti)
        self.N = vertex_normals(self.P, self.T)

    def closest(self, Q, k=6):
        """-> (tri index, bary, point, distance) per query point"""
        Q = np.asarray(Q, dtype=float)
        tri_i = np.zeros(len(Q), dtype=np.int64)
        bary = np.zeros((len(Q), 3))
        pts = np.zeros((len(Q), 3))
        dist = np.zeros(len(Q))
        for s in range(0, len(Q), 512):
            q = Q[s:s + 512]
            d2 = ((q[:, None, :] - self.P[None, :, :]) ** 2).sum(-1)
            near = np.argpartition(d2, min(k, len(self.P) - 1), axis=1)[:, :k]
            for j in range(len(q)):
                cand = sorted({t for v in near[j] for t in self.vert_tris[v]})
                if not cand:
                    continue
                c = np.array(cand)
                A, B, C = self.P[self.T[c, 0]], self.P[self.T[c, 1]], self.P[self.T[c, 2]]
                cp, bc = closest_point_on_triangles(q[j], A, B, C)
                dd = ((cp - q[j]) ** 2).sum(1)
                b = int(np.argmin(dd))
                tri_i[s + j] = c[b]
                bary[s + j] = bc[b]
                pts[s + j] = cp[b]
                dist[s + j] = np.sqrt(dd[b])
        return tri_i, bary, pts, dist

    def interp_weights(self, tri_i, bary):
        out = []
        for t, bc in zip(tri_i, bary):
            acc = {}
            for v, b in zip(self.T[t], bc):
                if b <= 0:
                    continue
                wv = self.W[v]
                for bone, w in (wv.items() if isinstance(wv, dict) else wv):
                    acc[bone] = acc.get(bone, 0.0) + b * w
            out.append(acc)
        return out

    def interp_uv(self, tri_i, bary):
        return np.einsum("ij,ijk->ik", bary, self.UV[self.T[tri_i]])

    def interp_normal(self, tri_i, bary):
        return unit(np.einsum("ij,ijk->ik", bary, self.N[self.T[tri_i]]))


def slice_points(P, T, y):
    """intersection points of a triangle mesh with the plane Y = y"""
    out = []
    ys = P[T][:, :, 1]
    for k0, k1 in ((0, 1), (1, 2), (2, 0)):
        a = P[T[:, k0]]
        b = P[T[:, k1]]
        ya, yb = a[:, 1], b[:, 1]
        m = (ya - y) * (yb - y) < 0
        t = (y - ya[m]) / (yb[m] - ya[m])
        out.append(a[m] + (b[m] - a[m]) * t[:, None])
    return np.concatenate(out) if out else np.zeros((0, 3))


def convex_hull_2d(pts):
    """Andrew's monotone chain; pts (n,2) -> hull (m,2) counter-clockwise"""
    pts = np.unique(np.round(np.asarray(pts, dtype=float), 6), axis=0)
    if len(pts) < 3:
        return pts
    pts = pts[np.lexsort((pts[:, 1], pts[:, 0]))]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(tuple(p))
    for p in pts[::-1]:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(tuple(p))
    return np.array(lower[:-1] + upper[:-1])


def polar_profile(hull_xz, center, thetas):
    """radius of a convex (x, z) polygon around `center` along directions d(theta) = (sin t, -cos t)"""
    H = np.asarray(hull_xz) - np.asarray(center)[None, :]
    out = np.zeros(len(thetas))
    n = len(H)
    for i, th in enumerate(thetas):
        d = np.array([np.sin(th), -np.cos(th)])
        best = 0.0
        for j in range(n):
            a, b = H[j], H[(j + 1) % n]
            # ray s*d hits segment a + u (b - a)
            e = b - a
            den = d[0] * (-e[1]) - d[1] * (-e[0])
            if abs(den) < 1e-12:
                continue
            s = (a[0] * (-e[1]) - a[1] * (-e[0])) / den
            u = (d[0] * a[1] - d[1] * a[0]) / den
            if 0 <= u <= 1 and s > best:
                best = s
        out[i] = best
    return out


def grid_faces(rows, cols, closed_cols=False, flip=False, offset=0):
    """quads for a rows x cols vertex grid (row-major). Winding: rows go up (+Y), cols go around
    the body so that the outward side is CCW in the mirrored frame when cols run counter-clockwise seen
    from above in DayZ axes (+X -> -Z ...). `flip` reverses."""
    F = []
    cmax = cols if closed_cols else cols - 1
    for r in range(rows - 1):
        for c in range(cmax):
            c1 = (c + 1) % cols
            a = offset + r * cols + c
            b = offset + r * cols + c1
            cc = offset + (r + 1) * cols + c1
            d = offset + (r + 1) * cols + c
            F.append([a, d, cc, b] if not flip else [a, b, cc, d])
    return F


def orient_outward(P, F, center_fn):
    """flip faces whose normal points toward center_fn(face centroid) - a safety net for generated shells"""
    out = []
    T = np.array([f[:3] for f in F])
    fn = face_normals(P, T)
    for f, n in zip(F, fn):
        c = P[f].mean(0)
        if np.dot(n, c - center_fn(c)) < 0:
            out.append(f[::-1])
        else:
            out.append(f)
    return out
