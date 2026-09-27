"""Small procedural mesh kit for the spike-A weapons: lofts, caps, boxes, selections -> mlod.Lod.

Coordinates are p3d numbers (X right, Y up, Z forward). Internally faces are kept counter-clockwise
seen from outside in the ordinary right-handed sense (cross(b-a, c-a) points outward); to_lod() reverses
them, because p3d wants the opposite (see pokemon_dev/tools/check_winding.py).
"""
import math

import numpy as np

import mlod


def v3(p):
    return np.asarray(p, dtype=np.float64)


def unit(a):
    a = v3(a)
    n = np.linalg.norm(a)
    return a / n if n > 1e-12 else a


class Mesh:
    def __init__(self):
        self.pts = []          # xyz
        self.faces = []        # dict(v=[i..], uv=[(u,v)..], n=[xyz..], tex, mat)
        self.sel = {}          # name -> set(point index)

    # ---------------------------------------------------------------- basic
    def add(self, p):
        self.pts.append(tuple(float(c) for c in p))
        return len(self.pts) - 1

    def face(self, idx, uv, normals, tex, mat, sel=None):
        self.faces.append({"v": list(idx), "uv": list(uv), "n": [tuple(unit(n)) for n in normals], "tex": tex, "mat": mat})
        if sel:
            for s in sel:
                self.sel.setdefault(s, set()).update(idx)
        return len(self.faces) - 1

    def select(self, name, idx):
        self.sel.setdefault(name, set()).update(idx)

    def merge(self, other, xf=None, sel=None):
        """append another mesh, optionally transformed by (R 3x3, t) -> p' = R p + t"""
        base = len(self.pts)
        R, t = (np.eye(3), np.zeros(3)) if xf is None else (np.asarray(xf[0]), np.asarray(xf[1]))
        for p in other.pts:
            self.add(R @ v3(p) + t)
        for f in other.faces:
            self.faces.append({"v": [i + base for i in f["v"]], "uv": list(f["uv"]),
                               "n": [tuple(unit(R @ v3(n))) for n in f["n"]], "tex": f["tex"], "mat": f["mat"]})
        for k, s in other.sel.items():
            self.sel.setdefault(k, set()).update(i + base for i in s)
        if sel:
            self.sel.setdefault(sel, set()).update(range(base, len(self.pts)))
        return base

    def bounds(self):
        P = np.array(self.pts)
        return P.min(0), P.max(0)

    # ---------------------------------------------------------------- lofts
    def loft(self, rings, us, vs, tex, mat, closed=True, hard=False, outward_ref=None, sel=None):
        """rings: list of equal-length point lists. us: per ring point u (len = n+1 if closed: seam value last).
        vs: per ring v. hard=True: flat across strips (sharp ridges), smooth along the length.
        outward_ref: per ring a point that lies INSIDE (default: ring centroid); faces are flipped to face away."""
        n = len(rings[0])
        R = len(rings)
        # us: one list for every ring (old behaviour) or a list per ring (katana: features move across the width)
        U = us if isinstance(us[0], (list, tuple)) else [us] * R
        idx = [[self.add(p) for p in ring] for ring in rings]
        P = [[v3(p) for p in ring] for ring in rings]
        nseg = n if closed else n - 1
        # face normals per (ring segment r, strip j)
        fn = np.zeros((R - 1, nseg, 3))
        for r in range(R - 1):
            for j in range(nseg):
                j2 = (j + 1) % n
                a, b, c, d = P[r][j], P[r][j2], P[r + 1][j2], P[r + 1][j]
                nn = np.cross(c - a, d - b)  # quad normal (diagonals)
                fn[r, j] = nn
        # orientation: majority vote against an inside reference
        score = 0.0
        for r in range(R - 1):
            ref = v3(outward_ref[r]) if outward_ref is not None else np.mean(P[r] + P[r + 1], axis=0)
            for j in range(nseg):
                j2 = (j + 1) % n
                cen = (P[r][j] + P[r][j2] + P[r + 1][j2] + P[r + 1][j]) / 4
                score += float(np.dot(fn[r, j], cen - ref))
        flip = score < 0
        if flip:
            fn = -fn
        # vertex normals
        def vn_smooth(r, j):
            acc = np.zeros(3)
            for rr in (r - 1, r):
                if 0 <= rr < R - 1:
                    for jj in ((j - 1) % n if closed else j - 1, j):
                        if 0 <= jj < nseg:
                            acc += unit(fn[rr, jj])
            return acc

        def vn_hard(r, j):
            acc = np.zeros(3)
            for rr in (r - 1, r):
                if 0 <= rr < R - 1:
                    acc += unit(fn[rr, j])
            return acc
        for r in range(R - 1):
            for j in range(nseg):
                j2 = (j + 1) % n
                quad = [(r, j), (r, j2), (r + 1, j2), (r + 1, j)]
                ids = [idx[a][b] for a, b in quad]
                uvs = [(U[r][j], vs[r]), (U[r][j + 1], vs[r]), (U[r + 1][j + 1], vs[r + 1]), (U[r + 1][j], vs[r + 1])]
                if hard:
                    nrm = [vn_hard(a, j) for a, b in quad]
                else:
                    nrm = [vn_smooth(a, b) for a, b in quad]
                # drop degenerate corners (collapsed rings) -> triangle
                pts = [P[a][b] for a, b in quad]
                keep = [0, 1, 2, 3]
                if np.linalg.norm(pts[0] - pts[1]) < 1e-7:
                    keep = [0, 2, 3]
                elif np.linalg.norm(pts[2] - pts[3]) < 1e-7:
                    keep = [0, 1, 2]
                ids = [ids[k] for k in keep]
                uvs = [uvs[k] for k in keep]
                nrm = [nrm[k] for k in keep]
                if flip:
                    ids, uvs, nrm = ids[::-1], uvs[::-1], nrm[::-1]
                self.face(ids, uvs, nrm, tex, mat, sel)
        return idx

    def cap(self, ring, centre, normal, uv_centre, uvs, tex, mat, sel=None):
        """triangle fan closing a ring; normal = outward direction of the cap"""
        c = self.add(centre)
        ids = [self.add(p) for p in ring]
        n = len(ring)
        nrm = unit(normal)
        for j in range(n):
            j2 = (j + 1) % n
            tri = [c, ids[j], ids[j2]]
            uv = [uv_centre, uvs[j], uvs[j2]]
            a, b, cc = v3(self.pts[tri[0]]), v3(self.pts[tri[1]]), v3(self.pts[tri[2]])
            if np.dot(np.cross(b - a, cc - a), nrm) < 0:
                tri, uv = tri[::-1], uv[::-1]
            self.face(tri, uv, [nrm] * 3, tex, mat, sel)

    def quad2(self, a, b, c, d, uv, tex, mat, sel=None):
        """double-sided planar quad (feathers)"""
        ids = [self.add(p) for p in (a, b, c, d)]
        n = unit(np.cross(v3(c) - v3(a), v3(d) - v3(b)))
        self.face(ids, uv, [n] * 4, tex, mat, sel)
        ids2 = [self.add(p) for p in (d, c, b, a)]
        self.face(ids2, uv[::-1], [-n] * 4, tex, mat, sel)


def box_lod(res, lo, hi, mass=None, props=None, boxes=None):
    """Geometry / fire / view geometry LOD made of one or more boxes (each its own ComponentNN)."""
    lod = mlod.Lod(res)
    boxes = boxes or [(lo, hi)]
    allp = []
    for k, (l, h) in enumerate(boxes):
        (x0, y0, z0), (x1, y1, z1) = l, h
        corners = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        pis = [lod.add_point(c) for c in corners]
        allp += pis
        # CW seen from outside (p3d): same order as pokemon build_item.add_box, which is proven in game
        quads = [((0, 1, 2, 3), (0, 0, -1)), ((7, 6, 5, 4), (0, 0, 1)), ((4, 5, 1, 0), (0, -1, 0)),
                 ((3, 2, 6, 7), (0, 1, 0)), ((0, 3, 7, 4), (-1, 0, 0)), ((5, 6, 2, 1), (1, 0, 0))]
        fis = []
        for q, nrm in quads:
            ni = lod.add_normal(nrm)
            fis.append(lod.add_face([(pis[i], ni, 0.0, 0.0) for i in q]))
        lod.select("Component%02d" % (k + 1), {pi: 1.0 for pi in pis}, fis)
    if mass is not None:
        lod.mass = [float(mass) / len(allp)] * len(allp)
    for k, v in (props or {}).items():
        lod.properties[k] = v
    return lod


def mesh_lod(mesh, res):
    lod = mlod.Lod(res)
    for p in mesh.pts:
        lod.add_point(p)
    for fi, f in enumerate(mesh.faces):
        verts = []
        order = list(range(len(f["v"])))[::-1]   # CCW-outside -> p3d clockwise
        for k in order:
            ni = lod.add_normal(f["n"][k])
            verts.append((f["v"][k], ni, float(f["uv"][k][0]), float(f["uv"][k][1])))
        lod.add_face(verts, texture=f["tex"], material=f["mat"])
    for name, ids in mesh.sel.items():
        lod.select(name, {i: 1.0 for i in ids})
        lod.faces_fully_inside(name)
    return lod


def memory_lod(points, props=None):
    """points: {name: [xyz, ...]}"""
    lod = mlod.Lod(mlod.LOD_MEMORY)
    for name, pts in points.items():
        ids = [lod.add_point(p) for p in pts]
        lod.select(name, {i: 1.0 for i in ids})
    for k, v in (props or {}).items():
        lod.properties[k] = v
    return lod


def ellipse_ring(centre, ax1, ax2, r1, r2, n, phase=0.0):
    """ring of n points: centre + r1 cos(t) ax1 + r2 sin(t) ax2, t from phase"""
    c, a, b = v3(centre), unit(ax1), unit(ax2)
    return [tuple(c + r1 * math.cos(phase + 2 * math.pi * k / n) * a + r2 * math.sin(phase + 2 * math.pi * k / n) * b)
            for k in range(n)]


def rot_cols(x_img, y_img, z_img):
    """rotation matrix whose columns are the images of local X, Y, Z"""
    return np.column_stack([unit(x_img), unit(y_img), unit(z_img)])
