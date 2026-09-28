"""Ray and intersection checks added after Stephen's first in-game house walk (G3, 2026-09-27; PLAYBOOK §15).

  door_reach    C10  every door / window leaf is hit FIRST by the camera ray from BOTH sides, open and closed, as the
                     engine needs (View Geometry ray, 5 m; hit within 2 m; the leaf's memory point within 2 m)
  envelope_leak C11  from inside each room nothing sees outside except through declared openings (doors, windows,
                     lattices): rays against the Resolution 1 faces
  roof_pokes    C12  no solid of another sub-part (walls, gables, udatsu, pents, posts...) enters a roof's body
                     (the collision slab between rafter underside and tile top) in any LOD
  convex_overlap     sampled convex-vs-convex overlap, used by the rotation sweep and C12

Components are dicts as checks.components() makes them: planes = [(inward unit normal n, d)], inside <=> n.p >= d.
"""
import math

from . import mlod
from .core import add, sub, mul, dot, cross, norm, anim_point_fn

CAM_H = 1.60            # standing camera height above the feet (DayZ third/first person, approx.)
RAY_MAX = 5.0           # ActionTargets c_RayDistance
REACH = 2.0             # UAMaxDistances.DEFAULT (CCTCursor and IsInReach)
MIN_EYES = 4            # a leaf must be the first hit from >= 4 of the 15 standing positions per side (0.7-1.4 m out,
#                         +-0.6 m along): a grazing sliver past a post (the pre-G3 doors) is seen from 0-2 of them


# ------------------------------------------------------------------------------------------------ components
def solid_comp(s, name="solid"):
    """A closed kit Solid -> component dict (inward planes from its resolved outward normals)."""
    s.finalize()
    planes = []
    for fi in range(len(s.faces)):
        n = mul(s.fn[fi], -1.0)
        planes.append((n, dot(n, s.verts[s.faces[fi][0]])))
    xs, ys, zs = [v[0] for v in s.verts], [v[1] for v in s.verts], [v[2] for v in s.verts]
    return dict(name=name, planes=planes, bbox=(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)), door=s.door,
                pts=list(s.verts))


def moved(comp, f):
    """Component moved by an affine point map f (translation / rotation of a door animation)."""
    c = dict(comp)
    planes = []
    for n, d in comp["planes"]:
        p0 = mul(n, d)
        q0 = f(p0)
        n2 = sub(f(add(p0, n)), q0)
        planes.append((n2, dot(n2, q0)))
    c["planes"] = planes
    pts = [f(p) for p in comp["pts"]]
    c["pts"] = pts
    if pts:
        xs, ys, zs = [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts]
        c["bbox"] = (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))
    return c


def open_state(comps, doors, frac=1.0):
    """Components with every leaf of `doors` moved to phase frac."""
    fn = {}
    for d in doors:
        for a in d.anims:
            fn[a["bone"]] = anim_point_fn(a, frac)
    return [moved(c, fn[c["door"]]) if c.get("door") in fn else c for c in comps]


def ray_comp(o, dv, comp, tmax):
    """Entry distance of the ray o + t dv (dv unit) into a convex component, or None."""
    b = comp["bbox"]
    t0, t1 = 0.0, tmax
    for n, d in comp["planes"]:
        nd = dot(n, dv)
        val = dot(n, o) - d
        if abs(nd) < 1e-12:
            if val < -1e-9:
                return None
            continue
        t = -val / nd
        if nd > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return t0 if b else None


def first_hit(o, dv, comps, tmax):
    best, bc = tmax, None
    for c in comps:
        b = c["bbox"]
        # cheap slab reject on the bbox
        lo, hi = 0.0, best
        ok = True
        for k in range(3):
            if abs(dv[k]) < 1e-12:
                if o[k] < b[2 * k] - 1e-6 or o[k] > b[2 * k + 1] + 1e-6:
                    ok = False
                    break
                continue
            ta, tb = (b[2 * k] - o[k]) / dv[k], (b[2 * k + 1] - o[k]) / dv[k]
            if ta > tb:
                ta, tb = tb, ta
            lo, hi = max(lo, ta), min(hi, tb)
            if lo > hi:
                ok = False
                break
        if not ok:
            continue
        t = ray_comp(o, dv, c, best)
        if t is not None and t < best:
            best, bc = t, c
    return (best, bc) if bc is not None else (None, None)


def samples(comp, k=4):
    """Points on / inside a convex component: vertices, pair midpoints and quarter points."""
    pts = list(comp["pts"])
    out = list(pts)
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            for f in ((0.5,) if k <= 2 else (0.25, 0.5, 0.75)):
                out.append(tuple(pts[i][q] + (pts[j][q] - pts[i][q]) * f for q in range(3)))
    return out


def broad_planes(comp):
    """The two opposite planes of a thin leaf component that are closest together (its broad faces)."""
    pl = comp["planes"]
    best = None
    for i, (n1, d1) in enumerate(pl):
        for j, (n2, d2) in enumerate(pl):
            if j <= i or dot(n1, n2) > -0.999:
                continue
            th = -(d1 + d2)
            if best is None or th < best[0]:
                best = (th, i, j)
    return [] if best is None else [pl[best[1]], pl[best[2]]]


def broad_face_points(comp, n=5, inset=0.03):
    """Grid points on the two BROAD faces of a thin leaf component (the pair of opposite planes closest together),
    inset from the face edges: what a player can put the crosshair on. Edges and end faces are left out on purpose -
    a 4 cm leaf edge seen past a post at a grazing angle is not aimable in game (the pre-G3 doors)."""
    pl = comp["planes"]
    best = None
    for i, (n1, d1) in enumerate(pl):
        for j, (n2, d2) in enumerate(pl):
            if j <= i or dot(n1, n2) > -0.999:
                continue
            th = -(d1 + d2)
            if best is None or th < best[0]:
                best = (th, i, j)
    if best is None:
        return list(comp["pts"])
    out = []
    for k in (best[1], best[2]):
        nn, dd = pl[k]
        face = [p for p in comp["pts"] if abs(dot(nn, p) - dd) < 1e-4]
        if len(face) < 3:
            continue
        o = face[0]
        # two in-plane directions from the face's own extent
        far = max(face, key=lambda q: math.dist(q, o))
        e1 = norm(sub(far, o))
        e2 = norm(cross(nn, e1))
        us = [dot(sub(q, o), e1) for q in face]
        vs = [dot(sub(q, o), e2) for q in face]
        u0, u1, v0, v1 = min(us) + inset, max(us) - inset, min(vs) + inset, max(vs) - inset
        if u1 <= u0 or v1 <= v0:
            continue
        for a in range(n):
            for b in range(n):
                uu = u0 + (u1 - u0) * a / (n - 1)
                vv = v0 + (v1 - v0) * b / (n - 1)
                q = add(o, add(mul(e1, uu), mul(e2, vv)))
                if inside_depth(comp, q) > -1e-4:       # the rectangle may overhang a non-rectangular face
                    out.append(q)
    return out


def inside_depth(comp, p):
    """How deep p is inside the convex component (min over planes of n.p - d); negative = outside."""
    return min(dot(n, p) - d for n, d in comp["planes"])


def convex_overlap(a, b, pad=0.01):
    """Depth (> pad) of the deepest sampled point of one component inside the other, else 0."""
    ba, bb = a["bbox"], b["bbox"]
    if not (ba[0] < bb[1] - pad and ba[1] > bb[0] + pad and ba[2] < bb[3] - pad and ba[3] > bb[2] + pad
            and ba[4] < bb[5] - pad and ba[5] > bb[4] + pad):
        return 0.0
    best = 0.0
    for p, c in [(p, b) for p in samples(a)] + [(p, a) for p in samples(b)]:
        dd = inside_depth(c, p)
        if dd > pad and dd > best:
            best = dd
    return best


# ------------------------------------------------------------------------------------------------ C10 door reach
def door_reach(d, comps, memory, floor_at=None, frac=1.0, others=()):
    """C10 for one door / window at phase frac (1 open, 0 closed). comps: View Geometry components of the whole object
    (the door's own leaves included, in their closed state; comp['door'] = bone). memory: name -> [points] (the
    leaf point <bone> is the IsInReach position). floor_at(x, z, y_hint) -> floor height under an eye point, or None
    (default: the door's floor = action height - d.act_h). Sides: 'leaf' = the side the leaves run on, 'far' = the
    other side; d.reach_sides limits them (a sliding window behind a lattice is worked from its leaf side only).
    Engine rule (vanilla ActionTargets / ActionOpenDoors / CCTCursor / IsInReach): the camera ray (5 m, View Geometry)
    must hit a leaf component FIRST, the hit must be within 2 m of the head or feet, and the leaf point too."""
    bones = [a["bone"] for a in d.anims]
    st = open_state(open_state(comps, [o for o in others if o is not d], 1.0), [d], frac)   # other doors open
    leaves = [c for c in st if c.get("door") in bones]
    closed = [c for c in comps if c.get("door") in bones]
    if not leaves:
        return {"leaf": (False, "no View Geometry leaf component")}
    a0 = d.anims[0]
    ax = norm(sub(a0["axis"][1], a0["axis"][0]))
    bp = broad_planes(closed[0])
    if bp:                                   # the wall normal = the closed leaf's broad-face normal (horizontal part)
        nb = norm((bp[0][0][0], 0.0, bp[0][0][2]))
        u = (-nb[2], 0.0, nb[0])
    else:
        u = norm((ax[0], 0.0, ax[2]))
    c = d.action
    lb = [cc["bbox"] for cc in closed]
    lc = ((min(b[0] for b in lb) + max(b[1] for b in lb)) / 2, 0.0, (min(b[4] for b in lb) + max(b[5] for b in lb)) / 2)
    v = (lc[0] - c[0], 0.0, lc[2] - c[2])
    n = (-u[2], 0.0, u[0])
    if dot(n, v) < 0:
        n = mul(n, -1.0)
    fy0 = c[1] - getattr(d, "act_h", 1.0)
    mem = []
    for a in d.anims:
        pts = memory.get(a["bone"]) or []
        if pts:
            mem.append(anim_point_fn(a, frac)(pts[0]))
    tpts = []
    for cc in leaves:
        tpts += broad_face_points(cc, 6)
    # sliding leaves: the aimable part must be IN the doorway (between the jambs), not a sliver behind a post
    slide = a0["type"] == "translation"
    if slide:
        cu = [dot(q, ax) for cc in closed for q in cc["pts"]]
        olo, ohi = min(cu) + 0.02 + 0.03, max(cu) - 0.02 - 0.03
    near = [cc for cc in st if max(cc["bbox"][0] - c[0], c[0] - cc["bbox"][1], cc["bbox"][4] - c[2],
                                   c[2] - cc["bbox"][5]) < RAY_MAX + 1.0]
    out = {}
    for side in getattr(d, "reach_sides", ("leaf", "far")):
        sg = 1.0 if side == "leaf" else -1.0
        good, tried, first = 0, 0, None
        for dist in (0.7, 1.0, 1.4):
            for k in (0.0, -0.3, 0.3, -0.6, 0.6):
                ex, ez = c[0] + n[0] * sg * dist + u[0] * k, c[2] + n[2] * sg * dist + u[2] * k
                fy = fy0
                if floor_at:
                    f2 = floor_at(ex, ez, fy0)
                    if f2 is not None:
                        fy = f2
                eye, root = (ex, fy + CAM_H, ez), (ex, fy, ez)
                for tp in tpts:
                    dv = sub(tp, eye)
                    L = math.sqrt(dot(dv, dv))
                    if L < 1e-6 or L > RAY_MAX:
                        continue
                    dv = mul(dv, 1.0 / L)
                    tried += 1
                    t, hc = first_hit(eye, dv, near, RAY_MAX)
                    if hc is None or hc.get("door") not in bones:
                        continue
                    hp = add(eye, mul(dv, t))
                    if min(math.dist(hp, eye), math.dist(hp, root)) > REACH:
                        continue
                    # the hit must land on a BROAD face of the leaf, not on its 3-4 cm end face past a post
                    if not any(abs(dot(nn, hp) - dd) < 2e-3 for nn, dd in broad_planes(hc)):
                        continue
                    if slide and side == "far" and not (olo <= dot(hp, ax) <= ohi):
                        continue
                    if mem and min(min(math.dist(m, eye), math.dist(m, root)) for m in mem) > REACH:
                        continue
                    good += 1
                    first = first or (dist, k, t)
                    break
        ok = good >= MIN_EYES
        out[side] = (ok, "leaf hit first from %d/15 standing positions (need %d)%s" % (
            good, MIN_EYES, (", e.g. %.1f m out, %+.1f m along, ray %.2f m" % first) if first else
            " (%d rays tried)" % tried))
    return out


# ------------------------------------------------------------------------------------------------ C11 envelope leak
def lod_triangles(lod):
    import numpy as np
    tris = []
    for verts, _, _, _ in lod.faces:
        pts = [lod.points[v[0]] for v in verts]
        for i in range(1, len(pts) - 1):
            tris.append((pts[0], pts[i], pts[i + 1]))
    T = np.asarray(tris, dtype=np.float64)
    return T


def fib_dirs(n):
    import numpy as np
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.cos(phi), np.sin(th) * np.sin(phi)], -1)


def cast(T, O, D, tmax=60.0, chunk=24):
    """Nearest hit distance per ray (inf = escapes) against triangles T (N,3,3), two-sided (Moller-Trumbore)."""
    import numpy as np
    v0 = T[:, 0]
    e1 = T[:, 1] - v0
    e2 = T[:, 2] - v0
    out = np.full(len(O), np.inf)
    for s in range(0, len(O), chunk):
        o = O[s:s + chunk][:, None, :]
        dv = D[s:s + chunk][:, None, :]
        p = np.cross(dv, e2[None])
        det = np.einsum("rnk,nk->rn", p, e1)
        ok = np.abs(det) > 1e-12
        inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
        tv = o - v0[None]
        uu = np.einsum("rnk,rnk->rn", tv, p) * inv
        q = np.cross(tv, e1[None])
        vv = np.einsum("rnk,rnk->rn", np.broadcast_to(dv, q.shape), q) * inv
        tt = np.einsum("rnk,nk->rn", q, e2) * inv
        hit = ok & (uu >= -1e-9) & (vv >= -1e-9) & (uu + vv <= 1 + 1e-9) & (tt > 1e-4) & (tt < tmax)
        tt = np.where(hit, tt, np.inf)
        out[s:s + chunk] = tt.min(1)
    return out


def seg_box(o, dv, t1, bx):
    """Does the segment o + t dv, t in [0, t1], pass through the axis-aligned box bx (x0,x1,y0,y1,z0,z1)?"""
    lo, hi = 0.0, t1
    for k in range(3):
        a, b = bx[2 * k], bx[2 * k + 1]
        if abs(dv[k]) < 1e-12:
            if o[k] < a or o[k] > b:
                return False
            continue
        ta, tb = (a - o[k]) / dv[k], (b - o[k]) / dv[k]
        if ta > tb:
            ta, tb = tb, ta
        lo, hi = max(lo, ta), min(hi, tb)
        if lo > hi:
            return False
    return True


def envelope_leak(lod, rooms, portals, ndirs=320, heights=(0.5, 1.1, 1.65), grid=(4, 3)):
    """C11. rooms: [{name, rect (x0,x1,z0,z1), y}] in model coordinates; portals: [(name, bbox)] volumes of intended
    openings (door leaves + their slots, windows, lattices), in model coordinates. Rays from a grid of eye points in
    every room; a ray that hits no face within 60 m escaped (sees sky / ground outside); it is a LEAK unless it passes
    through a portal. Returns {room: (n_rays, n_escaped_via_portals, [leak samples])}."""
    import numpy as np
    T = lod_triangles(lod)
    D = fib_dirs(ndirs)
    out = {}
    for r in rooms:
        x0, x1, z0, z1 = r["rect"]
        O = []
        for i in range(grid[0]):
            for j in range(grid[1]):
                x = x0 + 0.25 + (x1 - x0 - 0.5) * (i + 0.5) / grid[0]
                z = z0 + 0.25 + (z1 - z0 - 0.5) * (j + 0.5) / grid[1]
                if any(a0 <= x <= a1 and b0 <= z <= b1 for (a0, a1, b0, b1) in r.get("obstacles", ())):
                    continue
                for h in heights:
                    O.append((x, r["y"] + h, z))
        O = np.asarray(O, float)
        OO = np.repeat(O, len(D), 0)
        DD = np.tile(D, (len(O), 1))
        t = cast(T, OO, DD)
        esc = np.where(np.isinf(t))[0]
        leaks, via = [], 0
        for k in esc:
            o, dv = tuple(OO[k]), tuple(DD[k])
            names = [nm for nm, bx in portals if seg_box(o, dv, 60.0, bx)]
            if names:
                via += 1
                continue
            leaks.append((tuple(round(v, 2) for v in o), tuple(round(v, 3) for v in dv)))
        out[r["name"]] = (len(OO), via, leaks)
    return out


def leak_exit(o, dv, walls_bbox):
    """Where a leaking ray leaves the building's wall box (for the report)."""
    lo, hi = 0.0, 1e9
    for k in range(3):
        a, b = walls_bbox[2 * k], walls_bbox[2 * k + 1]
        if abs(dv[k]) < 1e-12:
            continue
        ta, tb = (a - o[k]) / dv[k], (b - o[k]) / dv[k]
        hi = min(hi, max(ta, tb))
    return tuple(round(o[k] + dv[k] * hi, 2) for k in range(3))


# ------------------------------------------------------------------------------------------------ C12 roof pokes
def roof_pokes(solids, pad=0.03, allow_src=("ridge_walk",)):
    """C12. Roof bodies = closed solids tagged roof_geo_* (the collision slab of each slope piece: rafter underside to
    tile top). Every other closed solid, or open sheet, from a DIFFERENT sub-part (solid.src) that reaches more than
    `pad` into a roof body is a poke. Returns [(src, tag, lods, roof_src, roof_tag, depth)]."""
    bodies = [(s, solid_comp(s, s.tag)) for s in solids if s.tag.startswith("roof_geo_") and s.closed]
    out = []
    for s in solids:
        if s.tag.startswith("roof_geo_") or getattr(s, "src", None) in allow_src:
            continue
        if not (s.vis or s.geo):
            continue
        sb = s.bbox()
        for rs, rc in bodies:
            if getattr(s, "src", None) == getattr(rs, "src", None):
                continue
            b = rc["bbox"]
            if not (sb[0] < b[1] - pad and sb[1] > b[0] + pad and sb[2] < b[3] - pad and sb[3] > b[2] + pad
                    and sb[4] < b[5] - pad and sb[5] > b[4] + pad):
                continue
            if s.closed:
                dep = convex_overlap(solid_comp(s, s.tag), rc, pad)
            else:
                dep = max([inside_depth(rc, p) for p in s.verts] + [0.0])
                dep = dep if dep > pad else 0.0
            if dep > 0:
                out.append((getattr(s, "src", None), s.tag, sorted(s.vis) + (["geo"] if s.geo else []),
                            getattr(rs, "src", None), rs.tag, round(dep, 3)))
    return out


def mlod_comps(lod):
    from .checks import components
    return components(lod)
