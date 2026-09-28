"""Shape helpers on top of core: plan-polygon slabs between two linear planes, 3D tubes, convex clipping, board runs,
stones posed on a slope. Every closed shape here is convex by construction."""
import math

from .core import Solid, box, prism, rings, rand_convex, norm, cross, sub, add, mul, dot, length


def clip_poly(poly, a, b, c):
    """Keep the part of a convex 2D polygon where a*x + b*y <= c (Sutherland-Hodgman, one half-plane)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = a * p[0] + b * p[1] - c
        fq = a * q[0] + b * q[1] - c
        if fp <= 1e-9:
            out.append(p)
        if (fp < -1e-9 and fq > 1e-9) or (fp > 1e-9 and fq < -1e-9):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    # drop near-duplicates
    res = []
    for p in out:
        if not res or abs(p[0] - res[-1][0]) > 1e-7 or abs(p[1] - res[-1][1]) > 1e-7:
            res.append(p)
    if len(res) > 1 and abs(res[0][0] - res[-1][0]) < 1e-7 and abs(res[0][1] - res[-1][1]) < 1e-7:
        res.pop()
    return clean_poly(res)


def clean_poly(poly, eps=1e-6):
    """Drop duplicate and collinear points (degenerate faces break the closed-component check)."""
    pts = list(poly)
    changed = True
    while changed and len(pts) >= 3:
        changed = False
        for i in range(len(pts)):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
            cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
            if abs(cr) < eps or (abs(a[0] - b[0]) < 1e-7 and abs(a[1] - b[1]) < 1e-7):
                pts.pop(i)
                changed = True
                break
    return pts if len(pts) >= 3 else []


def clip_rect(poly, x0, x1, y0, y1):
    for a, b, c in ((-1, 0, -x0), (1, 0, x1), (0, -1, -y0), (0, 1, y1)):
        poly = clip_poly(poly, a, b, c)
        if len(poly) < 3:
            return []
    return poly


def slab(plan, ybot, ytop, mats, **kw):
    """Convex 'slanted prism': plan = convex polygon [(x, z)] in world plan; ybot / ytop = functions (x, z) -> y,
    each linear (planes). Side faces are vertical planes through the plan edges."""
    n = len(plan)
    verts = [(x, ybot(x, z), z) for x, z in plan] + [(x, ytop(x, z), z) for x, z in plan]
    faces = [list(range(n)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    return Solid(verts, faces, mats, **kw)


def frame_of(d):
    d = norm(d)
    up = (0.0, 1.0, 0.0) if abs(d[1]) < 0.9 else (1.0, 0.0, 0.0)
    e1 = norm(cross(d, up))
    e2 = norm(cross(e1, d))
    return d, e1, e2


def tube(p0, p1, r, mats, n=8, r1=None, phase=None, squash=1.0, **kw):
    """n-gon prism (or frustum with r1) between two 3D points. squash scales the e2 (roughly vertical) radius."""
    d, e1, e2 = frame_of(sub(p1, p0))
    r1 = r if r1 is None else r1
    ph = math.pi / n if phase is None else phase
    verts = []
    for (c, rr) in ((p0, r), (p1, r1)):
        for k in range(n):
            a = ph + 2 * math.pi * k / n
            verts.append(add(c, add(mul(e1, rr * math.cos(a)), mul(e2, rr * squash * math.sin(a)))))
    faces = [list(range(n)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    return Solid(verts, faces, mats, **kw)


def half_tube(p0, p1, r, mats, n=6, **kw):
    """Half-round (convex D section, flat side down-ish along -e2): covers, gutters, round ridge caps."""
    d, e1, e2 = frame_of(sub(p1, p0))
    verts = []
    for c in (p0, p1):
        for k in range(n + 1):
            a = math.pi * k / n
            verts.append(add(c, add(mul(e1, r * math.cos(a)), mul(e2, r * math.sin(a)))))
    m = n + 1
    faces = [list(range(m)), list(range(m, 2 * m))]
    for i in range(m):
        j = (i + 1) % m
        faces.append([i, j, m + j, m + i])
    return Solid(verts, faces, mats, **kw)


def oriented_box(c, ax, ay, az, hx, hy, hz, mats, **kw):
    """Box centred at c with orthonormal axes ax, ay, az and half sizes."""
    corners = []
    for sy in (-1, 1):
        for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            corners.append(add(c, add(mul(ax, sx * hx), add(mul(ay, sy * hy), mul(az, sz * hz)))))
    faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return Solid(corners, faces, mats, **kw)


def posed(solid, fn):
    """Apply a point function to an un-finalized solid (pose a stone on a slope etc.)."""
    solid.verts = [fn(v) for v in solid.verts]
    solid.center = tuple(sum(v[k] for v in solid.verts) / len(solid.verts) for k in range(3))
    return solid


def slope_pose(origin, u_dir, in_dir, pitch_t):
    """Map local (a along u_dir, h up from the slope surface, s horizontal inward) to world on a plane rising
    `pitch_t` per metre inward, through `origin` (a point on the plane)."""
    ang = math.atan(pitch_t)
    ca, sa = math.cos(ang), math.sin(ang)
    su = (in_dir[0] * ca, sa, in_dir[2] * ca)          # unit vector up the slope
    nrm = (-in_dir[0] * sa, ca, -in_dir[2] * sa)        # slope normal

    def f(p):
        a, h, s_along = p                                # s_along measured along the slope
        return add(origin, add(mul(u_dir, a), add(mul(su, s_along), mul(nrm, h))))
    return f, su, nrm


def board_run(x0, x1, y0, y1, z0, z1, rng, wmin, wmax, mats, vertical=True, gap=0.004, vis=(1, 2), tag="board",
              uvjit=True, **kw):
    """Boards of random width filling [x0, x1] (vertical boards) or [y0, y1] (horizontal). W8: random UV offset."""
    out = []
    a, b = (x0, x1) if vertical else (y0, y1)
    p = a
    while p < b - 1e-4:
        w = rng.uniform(wmin, wmax)
        q = min(b, p + w)
        if b - q < wmin * 0.5:
            q = b
        off = (rng.uniform(0, 1), rng.uniform(0, 1)) if uvjit else (0.0, 0.0)
        if vertical:
            s = box(p + gap / 2, q - gap / 2, y0, y1, z0, z1, mats, vis=vis, tag=tag, uvoff=off, **kw)
        else:
            s = box(x0, x1, p + gap / 2, q - gap / 2, z0, z1, mats, vis=vis, tag=tag, uvoff=off, **kw)
        out.append(s)
        p = q
    return out


def rough_block(rng, x0, x1, y0, y1, z0, z1, mats, chamfer=0.02, top_jit=0.01, **kw):
    """Cut stone block with chamfered vertical edges and a slightly smaller top (convex by homothety)."""
    c = chamfer
    base = [(x0 + c, z0), (x1 - c, z0), (x1, z0 + c), (x1, z1 - c), (x1 - c, z1), (x0 + c, z1), (x0, z1 - c), (x0, z0 + c)]
    h = y1 - y0
    prof = [(y0, 1.0), (y1 - min(0.02, h * 0.2) - rng.uniform(0, top_jit), 1.0), (y1, 1.0 - rng.uniform(0.02, 0.06))]
    return rings((base, prof), mats, **kw)

