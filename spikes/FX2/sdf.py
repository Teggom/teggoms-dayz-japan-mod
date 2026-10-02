"""sdf.py - FX2 (2026-10-01) signed-distance modelling for statues (numpy only).

A shape is a Node: node(P) -> distances for points P (N x 3, metres; +y up, +z = the statue's front).
Every node carries a bounding box (lo, hi) so unions only evaluate a child near its own box (fast curls, fingers).

Primitives: sphere, ellipsoid, capsule (round cone when r0 != r1), rbox (rounded box), torus, cylinder, plane.
Ops: U (smooth union, k), S (smooth subtraction), I (intersection), mirror_x, xform (rotate + move), displace.
"""
import math

import numpy as np

BIG = 1e3


class Node:
    def __init__(self, f, lo, hi):
        self.f = f
        self.lo = np.asarray(lo, float)
        self.hi = np.asarray(hi, float)

    def __call__(self, P):
        return self.f(P)


def _rot(rx=0.0, ry=0.0, rz=0.0):
    """Rotation matrix (degrees): about x, then z, then y (as fkit.xf)."""
    ax, ay, az = (math.radians(a) for a in (rx, ry, rz))
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    mx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    my = np.array([[cy, 0, -sy], [0, 1, 0], [sy, 0, cy]])
    mz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return my @ mz @ mx


def rotm(rx=0.0, ry=0.0, rz=0.0):
    return _rot(rx, ry, rz)


# ------------------------------------------------------------------------------------------------ primitives
def sphere(c, r):
    c = np.asarray(c, float)
    return Node(lambda P: np.linalg.norm(P - c, axis=1) - r, c - r, c + r)


def ellipsoid(c, rad, rx=0.0, ry=0.0, rz=0.0):
    """Ellipsoid (iq's bound), rotated by (rx, ry, rz) degrees about its centre."""
    c = np.asarray(c, float)
    rad = np.asarray(rad, float)
    R = _rot(rx, ry, rz)
    Ri = R.T

    def f(P):
        q = (P - c) @ Ri.T
        k0 = np.linalg.norm(q / rad, axis=1)
        k1 = np.linalg.norm(q / (rad * rad), axis=1)
        return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)
    m = float(rad.max())
    return Node(f, c - m, c + m)


def capsule(a, b, r0, r1=None):
    """Round cone from a (radius r0) to b (radius r1); a capsule when r1 is None."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if r1 is None or abs(r1 - r0) < 1e-9:
        ba = b - a
        L2 = float(ba @ ba) or 1e-12

        def f(P):
            pa = P - a
            h = np.clip(pa @ ba / L2, 0.0, 1.0)
            return np.linalg.norm(pa - h[:, None] * ba, axis=1) - r0
        m = r0
    else:
        # iq's round cone
        ba = b - a
        l2 = float(ba @ ba)
        rr = r0 - r1
        a2 = l2 - rr * rr
        il2 = 1.0 / l2

        def f(P):
            pa = P - a
            y = pa @ ba
            z = y - l2
            xv = pa * l2 - y[:, None] * ba
            x2 = np.einsum("ij,ij->i", xv, xv)
            y2 = y * y * l2
            z2 = z * z * l2
            k = np.sign(rr) * rr * rr * x2
            out = (np.sqrt(x2 * a2 * il2) + y * rr) * il2 - r0
            c1 = np.sign(z) * a2 * z2 > k
            c2 = np.sign(y) * a2 * y2 < k
            out = np.where(c1, np.sqrt(x2 + z2) * il2 - r1, out)
            out = np.where(c2, np.sqrt(x2 + y2) * il2 - r0, out)
            return out
        m = max(r0, r1)
    return Node(f, np.minimum(a, b) - m, np.maximum(a, b) + m)


def rbox(c, half, r=0.0, rx=0.0, ry=0.0, rz=0.0):
    c = np.asarray(c, float)
    half = np.asarray(half, float) - r
    R = _rot(rx, ry, rz)

    def f(P):
        q = np.abs((P - c) @ R) - half
        return np.linalg.norm(np.maximum(q, 0.0), axis=1) + np.minimum(q.max(axis=1), 0.0) - r
    m = float(np.linalg.norm(half + r))
    return Node(f, c - m, c + m)


def torus(c, R_, r, rx=0.0, ry=0.0, rz=0.0):
    """Torus in its local xz plane (axis +y), rotated."""
    c = np.asarray(c, float)
    M = _rot(rx, ry, rz)

    def f(P):
        q = (P - c) @ M
        qx = np.sqrt(q[:, 0] ** 2 + q[:, 2] ** 2) - R_
        return np.sqrt(qx * qx + q[:, 1] ** 2) - r
    m = R_ + r
    return Node(f, c - m, c + m)


def cylinder(a, b, r, rr=0.0):
    """Capped cylinder a -> b, radius r, edge rounding rr."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    ba = b - a
    L = float(np.linalg.norm(ba))
    u = ba / L

    def f(P):
        pa = P - a
        y = pa @ u
        x = np.linalg.norm(pa - y[:, None] * u, axis=1)
        dx = x - (r - rr)
        dy = np.abs(y - L / 2) - (L / 2 - rr)
        return np.minimum(np.maximum(dx, dy), 0.0) + np.sqrt(np.maximum(dx, 0) ** 2 + np.maximum(dy, 0) ** 2) - rr
    m = r
    return Node(f, np.minimum(a, b) - m, np.maximum(a, b) + m)


def spheres(C, r):
    """Many small spheres (curls, beads): min over centres, evaluated in chunks."""
    C = np.asarray(C, float)
    r = np.broadcast_to(np.asarray(r, float), (len(C),))

    def f(P):
        out = np.full(len(P), BIG)
        for i in range(0, len(C), 64):
            c = C[i:i + 64]
            d = np.sqrt(((P[:, None, :] - c[None, :, :]) ** 2).sum(-1)) - r[i:i + 64][None, :]
            out = np.minimum(out, d.min(1))
        return out
    m = float(r.max())
    return Node(f, C.min(0) - m, C.max(0) + m)


def plane(n, d, lo=(-BIG,) * 3, hi=(BIG,) * 3):
    """Half-space n . p <= d (inside). Used to cut (intersection) or flatten."""
    n = np.asarray(n, float)
    L = float(np.linalg.norm(n))
    n = n / L
    d = d / L
    return Node(lambda P: P @ n - d, lo, hi)


# ------------------------------------------------------------------------------------------------ ops
def _smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def _smax(a, b, k):
    return -_smin(-a, -b, k)


def _near(P, node, pad):
    return np.all((P >= node.lo - pad) & (P <= node.hi + pad), axis=1)


def U(*nodes, k=0.0):
    """Smooth union (k = blend width, m). Children are evaluated only near their own boxes."""
    nodes = [n for n in nodes if n is not None]
    lo = np.min([n.lo for n in nodes], axis=0) - k
    hi = np.max([n.hi for n in nodes], axis=0) + k

    def f(P):
        d = np.full(len(P), BIG)
        pad = k + 0.004
        for n in nodes:
            m = _near(P, n, pad)
            if not m.any():
                continue
            dn = np.full(len(P), BIG)
            dn[m] = n(P[m])
            d = _smin(d, dn, k)
        return d
    return Node(f, lo, hi)


def S(a, *cuts, k=0.0):
    """a minus each cut (smooth)."""
    def f(P):
        d = a(P)
        for c in cuts:
            m = _near(P, c, k + 0.004)
            if m.any():
                dc = np.full(len(P), BIG)
                dc[m] = c(P[m])
                d = _smax(d, -dc, k)
        return d
    return Node(f, a.lo, a.hi)


def I(a, b, k=0.0):
    return Node(lambda P: _smax(a(P), b(P), k), np.maximum(a.lo, b.lo), np.minimum(a.hi, b.hi))


def xform(node, rx=0.0, ry=0.0, rz=0.0, t=(0.0, 0.0, 0.0), pivot=(0.0, 0.0, 0.0), s=1.0):
    """The node rotated (x, z, y order, degrees) about pivot, scaled by s, then moved by t."""
    R = _rot(rx, ry, rz)
    t = np.asarray(t, float)
    pv = np.asarray(pivot, float)

    def f(P):
        q = ((P - t - pv) @ R) / s + pv
        return node(q) * s
    corners = np.array([[x, y, z] for x in (node.lo[0], node.hi[0]) for y in (node.lo[1], node.hi[1])
                        for z in (node.lo[2], node.hi[2])])
    w = ((corners - pv) * s) @ R.T + pv + t
    return Node(f, w.min(0), w.max(0))


def mirror_x(node):
    """The node and its mirror image across x = 0 (a pair: ears, hands, legs)."""
    def f(P):
        q = P.copy()
        q[:, 0] = np.abs(q[:, 0])
        return node(q)
    lo = node.lo.copy()
    hi = node.hi.copy()
    m = max(abs(lo[0]), abs(hi[0]))
    lo[0], hi[0] = -m, m
    return Node(f, lo, hi)


def squash(node, sx=1.0, sy=1.0, sz=1.0, about=(0.0, 0.0, 0.0)):
    """Non-uniform scale about a point (a bound, not an exact distance: fine for meshing)."""
    s = np.array([sx, sy, sz], float)
    a = np.asarray(about, float)
    m = float(s.min())
    return Node(lambda P: node((P - a) / s + a) * m, (node.lo - a) * s + a, (node.hi - a) * s + a)


def displace(node, fn, amp):
    """node + fn(P) (fn returns values in [-1, 1] scaled by amp): folds, chisel marks, curls."""
    return Node(lambda P: node(P) + amp * fn(P), node.lo - amp, node.hi + amp)


def shell(node, t):
    return Node(lambda P: np.abs(node(P)) - t / 2, node.lo - t, node.hi + t)


def onion_cut(node, cut):
    return S(node, cut)


# ------------------------------------------------------------------------------------------------ helpers
def arc_capsules(pts, r0, r1=None):
    """A chain of round cones through pts (radius from r0 to r1)."""
    r1 = r0 if r1 is None else r1
    n = len(pts) - 1
    out = []
    for i in range(n):
        ra = r0 + (r1 - r0) * i / n
        rb = r0 + (r1 - r0) * (i + 1) / n
        out.append(capsule(pts[i], pts[i + 1], ra, rb))
    return out


def bezier(p0, p1, p2, n=8):
    p0, p1, p2 = (np.asarray(p, float) for p in (p0, p1, p2))
    return [tuple((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2) for t in np.linspace(0, 1, n + 1)]
