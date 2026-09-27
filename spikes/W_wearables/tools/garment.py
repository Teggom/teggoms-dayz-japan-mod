"""Garment container + helpers shared by the W generators.

A Garment is: points P (n,3) in the player BIND pose (DayZ axes), faces (vertex lists, MLOD winding = the
outward normal is -cross(b - a, c - a)), per-corner UVs (p3d convention, origin top-left), a material key per
face, and skin weights per point ({bone(lower case): w}, <= 4, normalised).
"""
import numpy as np

from geom import tris, vertex_normals, unit


class Garment:
    def __init__(self, name):
        self.name = name
        self.P = []
        self.F = []
        self.FUV = []
        self.FM = []
        self.W = []

    # ------------------------------------------------------------ building
    def add_points(self, pts, weights=None):
        base = len(self.P)
        for i, p in enumerate(np.asarray(pts, dtype=float).reshape(-1, 3)):
            self.P.append(p)
            self.W.append(dict(weights[i]) if weights is not None else {})
        return base

    def add_face(self, verts, uvs, mat):
        assert len(verts) in (3, 4) and len(uvs) == len(verts)
        self.F.append([int(v) for v in verts])
        self.FUV.append([tuple(map(float, uv)) for uv in uvs])
        self.FM.append(mat)

    def add_grid(self, grid, uvgrid, mat, closed=False, flip=False, skip=None):
        """grid: (rows, cols, 3) points; uvgrid (rows, cols, 2). Quads between rows r, r+1 and cols c, c+1.
        closed=True wraps the columns (uvgrid must then have cols+1 columns so the seam gets its own UVs).
        Winding: rows increase upward and (col+1) lies to the viewer's RIGHT when the surface is seen from
        outside (DayZ is left-handed: seen from -Z, +X is on the right) -> outward faces, i.e. the order
        (r,c) (r,c+1) (r+1,c+1) (r+1,c) whose -cross is outward. flip=True otherwise.
        skip(r, c) -> True to leave a cell out."""
        grid = np.asarray(grid, dtype=float)
        R, C = grid.shape[:2]
        base = self.add_points(grid.reshape(-1, 3))
        idx = lambda r, c: base + r * C + (c % C)  # noqa: E731
        cmax = C if closed else C - 1
        for r in range(R - 1):
            for c in range(cmax):
                if skip is not None and skip(r, c):
                    continue
                v = [idx(r, c), idx(r, c + 1), idx(r + 1, c + 1), idx(r + 1, c)]
                uv = [uvgrid[r][c], uvgrid[r][c + 1], uvgrid[r + 1][c + 1], uvgrid[r + 1][c]]
                if flip:
                    v, uv = v[::-1], uv[::-1]
                self.add_face(v, uv, mat)
        return base

    def arrays(self):
        return np.array(self.P, dtype=float)

    def tri_faces(self):
        return tris(self.F)

    def normals(self):
        return vertex_normals(self.arrays(), self.tri_faces())

    # ------------------------------------------------------------ weights
    def set_weights(self, W):
        self.W = [dict(w) for w in W]

    def clean_weights(self, max_bones=4, min_w=0.02):
        out = []
        for w in self.W:
            items = sorted(((b, v) for b, v in w.items() if v > 0), key=lambda kv: -kv[1])[:max_bones]
            items = [(b, v) for b, v in items if v >= min_w] or items[:1]
            s = sum(v for _, v in items) or 1.0
            out.append({b: v / s for b, v in items})
        self.W = out

    def weight_list(self):
        return [[[b, w] for b, w in ws.items()] for ws in self.W]

    def neighbours(self):
        nb = [set() for _ in self.P]
        for f in self.F:
            for i in range(len(f)):
                a, b = f[i], f[(i + 1) % len(f)]
                nb[a].add(b)
                nb[b].add(a)
        return nb

    def smooth_weights(self, iterations=3, alpha=0.5, mask=None, weld_tol=1e-4):
        """Laplacian smoothing of the weight dicts over the mesh (points at the same position are treated as
        one, so UV/material seams don't tear). mask: indices that may change (None = all)."""
        P = self.arrays()
        key = np.round(P / weld_tol).astype(np.int64)
        _, inv = np.unique(key, axis=0, return_inverse=True)
        inv = inv.reshape(-1)
        groups = {}
        for i, g in enumerate(inv):
            groups.setdefault(g, []).append(i)
        nb = self.neighbours()
        gnb = {}
        for i, s in enumerate(nb):
            gnb.setdefault(inv[i], set()).update(inv[j] for j in s)
        for g in gnb:
            gnb[g].discard(g)
        allowed = None if mask is None else set(inv[list(mask)])
        for _ in range(iterations):
            gw = {}
            for g, members in groups.items():
                acc = {}
                for i in members:
                    for b, v in self.W[i].items():
                        acc[b] = acc.get(b, 0.0) + v / len(members)
                gw[g] = acc
            new = {}
            for g, acc in gw.items():
                if allowed is not None and g not in allowed:
                    new[g] = acc
                    continue
                ns = gnb.get(g, ())
                if not ns:
                    new[g] = acc
                    continue
                avg = {}
                for h in ns:
                    for b, v in gw[h].items():
                        avg[b] = avg.get(b, 0.0) + v / len(ns)
                keys = set(acc) | set(avg)
                new[g] = {b: (1 - alpha) * acc.get(b, 0.0) + alpha * avg.get(b, 0.0) for b in keys}
            for g, members in groups.items():
                for i in members:
                    self.W[i] = dict(new[g])

    # ------------------------------------------------------------ transforms
    def copy(self, name=None):
        g = Garment(name or self.name)
        g.P = [p.copy() for p in self.P]
        g.F = [list(f) for f in self.F]
        g.FUV = [list(u) for u in self.FUV]
        g.FM = list(self.FM)
        g.W = [dict(w) for w in self.W]
        return g

    def merge(self, other):
        base = len(self.P)
        self.P += [p.copy() for p in other.P]
        self.W += [dict(w) for w in other.W]
        for f, uv, m in zip(other.F, other.FUV, other.FM):
            self.F.append([base + i for i in f])
            self.FUV.append(list(uv))
            self.FM.append(m)
        return self

    def inner_shell(self, offset=0.002, mats=None, mat_map=None):
        """Duplicate faces (all, or those with material in mats) as an inward-facing lining pushed `offset`
        metres inward along the vertex normals, reversed winding. Weights copied."""
        P = self.arrays()
        N = self.normals()
        sel = [i for i, m in enumerate(self.FM) if mats is None or m in mats]
        used = sorted({v for i in sel for v in self.F[i]})
        remap = {}
        for v in used:
            remap[v] = len(self.P)
            self.P.append(P[v] - N[v] * offset)
            self.W.append(dict(self.W[v]))
        for i in sel:
            f, uv, m = self.F[i], self.FUV[i], self.FM[i]
            self.F.append([remap[v] for v in f][::-1])
            self.FUV.append(list(uv)[::-1])
            self.FM.append(mat_map.get(m, m) if mat_map else m)

    def triangulate(self):
        """quads -> two triangles on the (a, c) diagonal. Done before inner_shell() so the reversed lining uses the
        SAME diagonal as the outer face; with quads, the reversed copy splits on the other diagonal and a twisted
        quad's lining can cross its outer surface (seen in the LOD 2 sleeves)"""
        F, U, M = [], [], []
        for f, uv, m in zip(self.F, self.FUV, self.FM):
            if len(f) == 4:
                F += [[f[0], f[1], f[2]], [f[0], f[2], f[3]]]
                U += [[uv[0], uv[1], uv[2]], [uv[0], uv[2], uv[3]]]
                M += [m, m]
            else:
                F.append(f)
                U.append(uv)
                M.append(m)
        self.F, self.FUV, self.FM = F, U, M

    def orient(self, faces, outward_fn):
        """flip the listed faces whose normal points against outward_fn(centroid) (a unit-ish vector)"""
        from geom import face_normals
        P = self.arrays()
        n = 0
        for i in faces:
            f = self.F[i]
            fn = face_normals(P, np.array([f[:3]]))[0]
            c = P[f].mean(0)
            if np.dot(fn, outward_fn(c)) < 0:
                self.F[i] = f[::-1]
                self.FUV[i] = self.FUV[i][::-1]
                n += 1
        return n

    def stats(self):
        return "%s: %d points, %d faces (%d tris)" % (self.name, len(self.P), len(self.F), len(self.tri_faces()))


def tube(path, radii, up, segs, closed_ring=True):
    """rings of `segs` points around a polyline path. radii: per path point (rx, ry) along (side, up) axes.
    up: per path point vector to use as ring 'up'. -> (rows, segs, 3)"""
    path = np.asarray(path, dtype=float)
    out = []
    for i in range(len(path)):
        t = path[min(i + 1, len(path) - 1)] - path[max(i - 1, 0)]
        t = unit(t)
        u = np.asarray(up[i], dtype=float)
        u = unit(u - np.dot(u, t) * t)
        s = np.cross(u, t)
        rx, ry = radii[i]
        ring = []
        for k in range(segs):
            a = 2 * np.pi * k / segs
            ring.append(path[i] + s * np.cos(a) * rx + u * np.sin(a) * ry)
        out.append(ring)
    return np.array(out)
