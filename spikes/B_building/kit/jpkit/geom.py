"""Geometry primitives for the Japanese building kit.

Everything is in p3d model space: x right, y up, z forward, metres. For the machiya, +z is the street front.
A Solid is a closed convex polyhedron (prism of a convex 2D polygon), so the same object can be written as a
flat-shaded visual mesh AND as a convex component in the Geometry / View / Fire LODs.
"""
import math


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def length(a):
    return math.sqrt(dot(a, a))


def norm(a):
    l = length(a) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


def newell(pts):
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[(i + 1) % len(pts)]
        nx += (y0 - y1) * (z0 + z1)
        ny += (z0 - z1) * (x0 + x1)
        nz += (x0 - x1) * (y0 + y1)
    return (nx, ny, nz)


class Solid:
    """Closed convex polyhedron.

    mats:  a material name, or a dict {'top':m, 'bottom':m, 'side':m, 'front':m, 'back':m} picked per face by
           its outward normal ('front' = +z facing, 'back' = -z facing; fall back to 'side').
    vis:   set of resolution LOD indices (1, 2, 3) the solid is drawn in.
    geo / view: also a component in Geometry / View Geometry.
    fire:  penetration material name (dz\\data\\data\\penetration\\<fire>.rvmat) or None = not in Fire Geometry.
    door:  bone/selection name (doorsN) when the solid is part of a door leaf.
    uv:    'world' (tiling, metres per tile from the material), 'fit' (each face 0..1), or ('rect', u0, v0, u1, v1)
           for the +y face (tatami).
    """

    def __init__(self, verts, faces, mats, vis=(1, 2), geo=False, view=False, fire=None, door=None, uv="world",
                 tag=""):
        self.verts = [tuple(float(c) for c in v) for v in verts]
        self.faces = [list(f) for f in faces]
        self.mats = mats
        self.vis = set(vis)
        self.geo = geo
        self.view = view
        self.fire = fire
        self.door = door
        self.uv = uv
        self.tag = tag
        c = [sum(v[k] for v in self.verts) / len(self.verts) for k in range(3)]
        self.center = tuple(c)

    # --------------------------------------------------------------------------------------------------
    def face_points(self, fi):
        return [self.verts[i] for i in self.faces[fi]]

    def outward(self, fi):
        pts = self.face_points(fi)
        n = norm(newell(pts))
        fc = tuple(sum(p[k] for p in pts) / len(pts) for k in range(3))
        if dot(n, sub(fc, self.center)) < 0:
            n = mul(n, -1.0)
        return n

    def face_role(self, n):
        if n[1] > 0.5:
            return "top"
        if n[1] < -0.5:
            return "bottom"
        if n[2] > 0.7:
            return "front"
        if n[2] < -0.7:
            return "back"
        if n[0] > 0.7:
            return "right"
        if n[0] < -0.7:
            return "left"
        return "side"

    def face_mat(self, fi):
        if isinstance(self.mats, str):
            return self.mats
        role = self.face_role(self.outward(fi))
        if role in self.mats:
            return self.mats[role]
        if role in ("front", "back", "left", "right") and "side" in self.mats:
            return self.mats["side"]
        return self.mats.get("default", next(iter(self.mats.values())))

    def bbox(self):
        xs = [v[0] for v in self.verts]
        ys = [v[1] for v in self.verts]
        zs = [v[2] for v in self.verts]
        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    def translated(self, d):
        s = Solid([add(v, d) for v in self.verts], self.faces, self.mats, self.vis, self.geo, self.view,
                  self.fire, self.door, self.uv, self.tag)
        return s


# ------------------------------------------------------------------------------------------------------
# primitive builders
# ------------------------------------------------------------------------------------------------------
def prism(poly, axis, t0, t1, mats, **kw):
    """Extrude a convex 2D polygon along an axis. poly = [(a, b)], axis 'x': (a,b)=(y,z); 'y': (x,z); 'z': (x,y)."""
    def p3(a, b, t):
        if axis == "x":
            return (t, a, b)
        if axis == "y":
            return (a, t, b)
        return (a, b, t)
    n = len(poly)
    verts = [p3(a, b, t0) for a, b in poly] + [p3(a, b, t1) for a, b in poly]
    faces = [list(range(n)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    return Solid(verts, faces, mats, **kw)


def box(x0, x1, y0, y1, z0, z1, mats, **kw):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    z0, z1 = min(z0, z1), max(z0, z1)
    return prism([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "z", z0, z1, mats, **kw)


def hexa(corners, mats, **kw):
    """Convex hexahedron from 8 corners: bottom quad c0..c3 then top quad c4..c7 (same order)."""
    faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return Solid(corners, faces, mats, **kw)


# ------------------------------------------------------------------------------------------------------
# UV mapping
# ------------------------------------------------------------------------------------------------------
def face_uvs(solid, fi, mat_def):
    """UVs for one face of a solid (MLOD convention: u right, v down, origin top-left)."""
    pts = solid.face_points(fi)
    n = solid.outward(fi)
    mode = solid.uv
    if isinstance(mode, tuple) and mode[0] == "rect":
        # the top face of a thin horizontal box: map its longer extent to u, shorter to v
        if n[1] > 0.5:
            x0, x1, _, _, z0, z1 = solid.bbox()
            _, u0, v0, u1, v1 = mode
            out = []
            for p in pts:
                if (x1 - x0) >= (z1 - z0):
                    fu = (p[0] - x0) / (x1 - x0)
                    fv = (p[2] - z0) / (z1 - z0)
                else:
                    fu = (p[2] - z0) / (z1 - z0)
                    fv = (p[0] - x0) / (x1 - x0)
                out.append((u0 + (u1 - u0) * fu, v0 + (v1 - v0) * fv))
            return out
        mode = "world"
    # in-plane axes
    if abs(n[1]) > 0.7:
        ua = (1.0, 0.0, 0.0)
        ua = norm(sub(ua, mul(n, dot(ua, n))))
        va = norm(cross(n, ua))
        # v must run "downhill" on sloped faces and towards -z... keep it pointing down the slope / to +z
        if va[1] > 1e-6 or (abs(va[1]) <= 1e-6 and va[2] < 0):
            va = mul(va, -1.0)
    else:
        up = (0.0, 1.0, 0.0)
        va = norm(sub(mul(up, -1.0), mul(n, dot((0.0, -1.0, 0.0), n))))
        ua = norm(cross(va, n))
        if dot(cross(ua, va), n) < 0:
            ua = mul(ua, -1.0)
    grain = mat_def.get("grain")
    if grain == "long":
        # align v with the solid's longest edge direction when that direction lies in this face
        x0, x1, y0, y1, z0, z1 = solid.bbox()
        ext = [(x1 - x0, (1.0, 0.0, 0.0)), (y1 - y0, (0.0, 1.0, 0.0)), (z1 - z0, (0.0, 0.0, 1.0))]
        ext.sort(key=lambda e: -e[0])
        L = ext[0][1]
        if abs(dot(L, n)) < 0.3:
            Lp = norm(sub(L, mul(n, dot(L, n))))
            va = Lp
            ua = norm(cross(va, n))
    if mode == "fit":
        us = [dot(p, ua) for p in pts]
        vs = [dot(p, va) for p in pts]
        umin, umax = min(us), max(us)
        vmin, vmax = min(vs), max(vs)
        du = (umax - umin) or 1.0
        dv = (vmax - vmin) or 1.0
        return [((u - umin) / du, (v - vmin) / dv) for u, v in zip(us, vs)]
    su = mat_def.get("scale", 2.0)
    sv = mat_def.get("scale_v", su)
    return [(dot(p, ua) / su, dot(p, va) / sv) for p in pts]
