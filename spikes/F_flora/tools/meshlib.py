r"""meshlib.py - tiny mesh toolkit for the F spike: build in p3d space, write MLOD LODs and preview OBJs.

Coordinates are p3d model space throughout: X east, Y up, Z north (left-handed), metres, origin at the base.

Winding: p3d wants faces clockwise seen from outside. Numerically that means cross(p1-p0, p2-p0) points
AGAINST the outward normal - the rule pokemon_dev/tools/check_winding.py established and verified in game,
and what vanilla's own LOD4 billboard quads do. Every face here is added with its intended outward normal
and reordered to satisfy that rule, so no generator has to think about it.

OBJ export (Blender previews) maps p3d (x, y, z) -> Blender (x, z, y). That swap is a reflection, so the same
vertex order comes out counter-clockwise in Blender's right-handed frame, which is what OBJ expects.
"""
import math
import os

import mlod


def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def v_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def v_cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def v_len(a):
    return math.sqrt(v_dot(a, a))


def v_norm(a):
    ln = v_len(a)
    return (a[0] / ln, a[1] / ln, a[2] / ln) if ln > 1e-12 else (0.0, 1.0, 0.0)


def v_lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)


def basis_from(d, hint=(0.0, 1.0, 0.0)):
    """Two unit vectors perpendicular to d (and to each other)."""
    d = v_norm(d)
    h = hint if abs(v_dot(d, hint)) < 0.95 else (1.0, 0.0, 0.0)
    a = v_norm(v_cross(d, h))
    b = v_norm(v_cross(a, d))
    return a, b


def rotate_about(v, axis, ang):
    """Rodrigues rotation of v about unit axis."""
    axis = v_norm(axis)
    c, s = math.cos(ang), math.sin(ang)
    return v_add(v_add(v_mul(v, c), v_mul(v_cross(axis, v), s)), v_mul(axis, v_dot(axis, v) * (1 - c)))


class Mesh:
    """Points + faces with per-corner normals and UVs, grouped by (texture, material)."""

    def __init__(self):
        self.points = []
        self.faces = []          # dict(v=[pi], n=[normal], uv=[(u, v)], tex, mat)
        self.selections = {}     # name -> (set(point idx), set(face idx))

    def point(self, p):
        self.points.append((float(p[0]), float(p[1]), float(p[2])))
        return len(self.points) - 1

    def face(self, vids, normals, uvs, tex="", mat="", outward=None):
        """Add a tri/quad. `outward` (defaults to the mean corner normal) fixes the winding."""
        assert len(vids) in (3, 4)
        out = outward or v_norm(tuple(sum(n[i] for n in normals) for i in range(3)))
        p0, p1, p2 = (self.points[i] for i in vids[:3])
        if v_dot(v_cross(v_sub(p1, p0), v_sub(p2, p0)), out) > 0:
            vids, normals, uvs = vids[::-1], normals[::-1], uvs[::-1]
        self.faces.append(dict(v=list(vids), n=[tuple(n) for n in normals], uv=[tuple(u) for u in uvs], tex=tex, mat=mat))
        return len(self.faces) - 1

    def select(self, name, pids=(), fids=()):
        ps, fs = self.selections.setdefault(name, (set(), set()))
        ps.update(pids)
        fs.update(fids)

    def merge(self, other):
        base = len(self.points)
        fbase = len(self.faces)
        self.points += other.points
        for f in other.faces:
            g = dict(f)
            g["v"] = [i + base for i in f["v"]]
            self.faces.append(g)
        for name, (ps, fs) in other.selections.items():
            self.select(name, {i + base for i in ps}, {i + fbase for i in fs})

    def tri_count(self):
        return sum(1 if len(f["v"]) == 3 else 2 for f in self.faces)

    def bbox(self):
        xs, ys, zs = zip(*self.points)
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

    # -- output -------------------------------------------------------------------------------------------
    def to_lod(self, resolution, props=None, mass=None):
        lod = mlod.Lod(resolution)
        for p in self.points:
            lod.add_point(p)
        nidx = {}
        for f in self.faces:
            corners = []
            for pi, n, uv in zip(f["v"], f["n"], f["uv"]):
                key = (round(n[0], 5), round(n[1], 5), round(n[2], 5))
                if key not in nidx:
                    nidx[key] = lod.add_normal(key)
                corners.append((pi, nidx[key], uv[0], uv[1]))
            lod.add_face(corners, texture=f["tex"], material=f["mat"])
        for name, (ps, fs) in self.selections.items():
            lod.select(name, {pi: 1.0 for pi in ps}, fs)
        for k, v in (props or {}).items():
            lod.properties[k] = v
        if mass is not None:
            lod.mass = [mass / max(1, len(self.points))] * len(self.points)
        return lod

    def write_obj(self, path, mtl_map):
        """mtl_map: texture path -> material name in the .mtl written alongside (by the caller)."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        lines = ["# F flora preview mesh (p3d x,y,z -> obj x,z,y)", "mtllib " + os.path.basename(path)[:-4] + ".mtl"]
        for x, y, z in self.points:
            lines.append("v %.5f %.5f %.5f" % (x, z, y))
        vt, vn = {}, {}
        vt_lines, vn_lines, f_lines = [], [], []
        groups = {}
        for f in self.faces:
            groups.setdefault(f["tex"], []).append(f)
        for tex, fs in groups.items():
            f_lines.append("usemtl " + mtl_map.get(tex, "default"))
            for f in fs:
                idx = []
                for pi, n, uv in zip(f["v"], f["n"], f["uv"]):
                    tk = (round(uv[0], 5), round(1.0 - uv[1], 5))
                    if tk not in vt:
                        vt[tk] = len(vt) + 1
                        vt_lines.append("vt %.5f %.5f" % tk)
                    nk = (round(n[0], 4), round(n[2], 4), round(n[1], 4))
                    if nk not in vn:
                        vn[nk] = len(vn) + 1
                        vn_lines.append("vn %.4f %.4f %.4f" % nk)
                    idx.append("%d/%d/%d" % (pi + 1, vt[tk], vn[nk]))
                f_lines.append("f " + " ".join(idx))
        with open(path, "wb") as fh:
            fh.write(("\n".join(lines + vt_lines + vn_lines + f_lines) + "\n").encode("ascii"))
        names = sorted({mtl_map.get(t, "default") for t in groups})
        with open(path[:-4] + ".mtl", "wb") as fh:
            fh.write("".join("newmtl %s\nKd 0.8 0.8 0.8\n" % n for n in names).encode("ascii"))


# ---------------------------------------------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------------------------------------------
def tube(mesh, path, radii, sides, tex, mat, uv_fn, cap_top=False, twist=0.0, hint=(0.0, 0.0, 1.0)):
    """Generalised cylinder along a polyline `path` with per-point radius. Frames are parallel-transported so
    there is no twisting. uv_fn(ring_index, side_fraction, dist_along) -> (u, v). Returns ring point ids."""
    n = len(path)
    dists = [0.0]
    for i in range(1, n):
        dists.append(dists[-1] + v_len(v_sub(path[i], path[i - 1])))
    tangents = []
    for i in range(n):
        a = path[max(0, i - 1)]
        b = path[min(n - 1, i + 1)]
        tangents.append(v_norm(v_sub(b, a)))
    ax, bx = basis_from(tangents[0], hint)
    rings = []
    frames = []
    for i in range(n):
        if i > 0:
            # parallel transport of the frame from tangent i-1 to tangent i
            t0, t1 = tangents[i - 1], tangents[i]
            axis = v_cross(t0, t1)
            if v_len(axis) > 1e-9:
                ang = math.acos(max(-1.0, min(1.0, v_dot(t0, t1))))
                ax = rotate_about(ax, axis, ang)
                bx = rotate_about(bx, axis, ang)
        frames.append((ax, bx))
        ring = []
        for s in range(sides + 1):
            f = s / sides
            th = 2 * math.pi * f + twist
            off = v_add(v_mul(ax, math.cos(th) * radii[i]), v_mul(bx, math.sin(th) * radii[i]))
            ring.append((mesh.point(v_add(path[i], off)) if s < sides else None, v_norm(off), f))
        ring[sides] = (ring[0][0], ring[0][1], 1.0)
        rings.append(ring)
    for i in range(n - 1):
        for s in range(sides):
            a, b = rings[i][s], rings[i][s + 1]
            c, d = rings[i + 1][s + 1], rings[i + 1][s]
            uvs = [uv_fn(i, a[2], dists[i]), uv_fn(i, b[2], dists[i]), uv_fn(i + 1, c[2], dists[i + 1]), uv_fn(i + 1, d[2], dists[i + 1])]
            out = v_norm(v_add(v_add(a[1], b[1]), v_add(c[1], d[1])))
            mesh.face([a[0], b[0], c[0], d[0]], [a[1], b[1], c[1], d[1]], uvs, tex, mat, outward=out)
    if cap_top:
        ring = rings[-1]
        tip = mesh.point(path[-1])
        t = tangents[-1]
        for s in range(sides):
            a, b = ring[s], ring[s + 1]
            mesh.face([a[0], b[0], tip], [t, t, t], [uv_fn(n - 1, a[2], dists[-1]), uv_fn(n - 1, b[2], dists[-1]), uv_fn(n - 1, (a[2] + b[2]) / 2, dists[-1])], tex, mat, outward=t)
    return rings, frames


def card(mesh, corners, uvs, normal_fn, tex, mat, facing=None):
    """A single-sided quad (TreeAdv draws both sides - vanilla's LOD4 billboards are single quads too).
    corners in order around the quad; normal_fn(point) -> the shading normal stored at each corner.
    The winding follows `facing`, or the mean stored normal when facing is None."""
    ids = [mesh.point(c) for c in corners]
    normals = [normal_fn(c) for c in corners]
    if facing is None:
        facing = v_norm(tuple(sum(n[i] for n in normals) for i in range(3)))
    return mesh.face(ids, normals, uvs, tex, mat, outward=facing)


def convex_frustum(mesh, p0, p1, r0, r1, sides, tex="", mat="", sel=None):
    """Closed convex frustum between two parallel n-gons (planar side faces); caps as triangle fans."""
    d = v_norm(v_sub(p1, p0))
    a, b = basis_from(d)
    ring0, ring1 = [], []
    for s in range(sides):
        th = 2 * math.pi * s / sides
        off = v_add(v_mul(a, math.cos(th)), v_mul(b, math.sin(th)))
        ring0.append(mesh.point(v_add(p0, v_mul(off, r0))))
        ring1.append(mesh.point(v_add(p1, v_mul(off, r1))))
    fids = []
    for s in range(sides):
        t = (s + 1) % sides
        th = 2 * math.pi * (s + 0.5) / sides
        out = v_norm(v_add(v_mul(a, math.cos(th)), v_mul(b, math.sin(th))))
        fids.append(mesh.face([ring0[s], ring0[t], ring1[t], ring1[s]], [out] * 4, [(0, 0)] * 4, tex, mat, outward=out))
    c0, c1 = mesh.point(p0), mesh.point(p1)
    nd = v_mul(d, -1)
    for s in range(sides):
        t = (s + 1) % sides
        fids.append(mesh.face([ring0[s], ring0[t], c0], [nd] * 3, [(0, 0)] * 3, tex, mat, outward=nd))
        fids.append(mesh.face([ring1[s], ring1[t], c1], [d] * 3, [(0, 0)] * 3, tex, mat, outward=d))
    pids = ring0 + ring1 + [c0, c1]
    if sel:
        mesh.select(sel, pids, fids)
    return pids, fids


def convex_blob(mesh, center, radii, seg=8, rings=5, tex="", mat="", sel=None):
    """Closed convex low-poly ellipsoid (UV sphere scaled per axis: an affine image of a convex polytope)."""
    cx, cy, cz = center
    rx, ry, rz = radii
    top = mesh.point((cx, cy + ry, cz))
    bot = mesh.point((cx, cy - ry, cz))
    grid = []
    for r in range(1, rings):
        ph = math.pi * r / rings
        row = []
        for s in range(seg):
            th = 2 * math.pi * s / seg
            row.append(mesh.point((cx + rx * math.sin(ph) * math.cos(th), cy + ry * math.cos(ph), cz + rz * math.sin(ph) * math.sin(th))))
        grid.append(row)
    fids = []

    def outn(ids):
        c = tuple(sum(mesh.points[i][k] for i in ids) / len(ids) for k in range(3))
        return v_norm(v_sub(c, center))
    for s in range(seg):
        t = (s + 1) % seg
        ids = [top, grid[0][s], grid[0][t]]
        fids.append(mesh.face(ids, [outn(ids)] * 3, [(0, 0)] * 3, tex, mat, outward=outn(ids)))
        ids = [bot, grid[-1][t], grid[-1][s]]
        fids.append(mesh.face(ids, [outn(ids)] * 3, [(0, 0)] * 3, tex, mat, outward=outn(ids)))
        for r in range(len(grid) - 1):
            ids = [grid[r][s], grid[r][t], grid[r + 1][t], grid[r + 1][s]]
            fids.append(mesh.face(ids, [outn(ids)] * 4, [(0, 0)] * 4, tex, mat, outward=outn(ids)))
    pids = [top, bot] + [p for row in grid for p in row]
    if sel:
        mesh.select(sel, pids, fids)
    return pids, fids


def memory_lod(points, props=None):
    """points: {selection_name: (x, y, z)} -> Memory LOD."""
    lod = mlod.Lod(mlod.LOD_MEMORY)
    for name, p in points.items():
        pi = lod.add_point(p)
        lod.select(name, {pi: 1.0})
    for k, v in (props or {}).items():
        lod.properties[k] = v
    return lod


def check_winding(mesh):
    """Every face must have cross(p1-p0, p2-p0) against its stored mean normal. Returns count of bad faces."""
    bad = 0
    for f in mesh.faces:
        p0, p1, p2 = (mesh.points[i] for i in f["v"][:3])
        n = tuple(sum(c[k] for c in f["n"]) for k in range(3))
        if v_dot(v_cross(v_sub(p1, p0), v_sub(p2, p0)), n) > 0:
            bad += 1
    return bad
