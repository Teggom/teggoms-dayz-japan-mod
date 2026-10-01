"""zfight.py - coplanar overlapping faces (z-fighting) in a building's visual LODs (FB2, 2026-10-01).

Stephen's re-check: "a couple of places where items are perfectly aligned and flicker" (a stair stringer flush with a
plaster wall, interior door sills flush with the floor, a wall / floor pair in the mochi building). Two faces of
DIFFERENT solids that lie in the same plane (within TOL, 1 mm) and overlap in area fight for the depth buffer.

  same      the two faces point the same way: both are drawn from the same side -> visible flicker. Check C20 fails.
  opposite  they point at each other (two solids touching face to face): with backface culling only one of the two is
            ever drawn from any eye point, so they cannot flicker; counted and reported, not failed.

coplanar(M, lods=(1, 2, 3)) works on the Part (finalized solids: s.faces, s.fn, s.vis); the faces are exactly the
faces Part._visual(k) writes. Returns {'same': [...], 'opposite': [...]} with one record per overlapping face pair:
(lod, area_m2, tag_a, tag_b, src_a, src_b, point).
"""
import math
import os

TOL = 0.001             # plane distance (m)
COS = 0.99996           # normals parallel within ~0.5 deg
MIN_AREA = 1.0e-4       # overlap area worth reporting (1 cm2)
NQ = 100.0              # normal quantisation (hash)
DQ = 200.0              # plane offset quantisation (hash, 5 mm)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _canon(n, d):
    """Sign-canonical plane: the largest-magnitude normal component positive."""
    k = max(range(3), key=lambda i: abs(n[i]))
    if n[k] < 0:
        return (-n[0], -n[1], -n[2]), -d, -1
    return n, d, 1


def _basis(n):
    a = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
    u = (n[1] * a[2] - n[2] * a[1], n[2] * a[0] - n[0] * a[2], n[0] * a[1] - n[1] * a[0])
    lu = math.sqrt(_dot(u, u))
    u = (u[0] / lu, u[1] / lu, u[2] / lu)
    v = (n[1] * u[2] - n[2] * u[1], n[2] * u[0] - n[0] * u[2], n[0] * u[1] - n[1] * u[0])
    return u, v


def _area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return a / 2.0


def _ccw(poly):
    return poly if _area(poly) >= 0 else poly[::-1]


def _clip(subject, clip):
    """Sutherland-Hodgman: convex subject clipped by convex CCW clip polygon."""
    out = subject
    for i in range(len(clip)):
        if not out:
            return []
        ax, ay = clip[i]
        bx, by = clip[(i + 1) % len(clip)]
        ex, ey = bx - ax, by - ay
        inp, out = out, []

        def side(p):
            return ex * (p[1] - ay) - ey * (p[0] - ax)
        for j in range(len(inp)):
            p, q = inp[j], inp[(j + 1) % len(inp)]
            sp, sq = side(p), side(q)
            if sp >= 0:
                out.append(p)
            if (sp >= 0) != (sq >= 0):
                t = sp / (sp - sq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out


def faces_of(M, k, skip=None):
    """[(solid_index, face_index, pts, normal)] of every face Part._visual(k) writes."""
    out = []
    for si, s in enumerate(M.solids):
        if k not in s.vis or (skip and skip(s)):
            continue
        if s.fn is None:
            s.finalize()
        for fi, f in enumerate(s.faces):
            pts = [s.verts[i] for i in f]
            out.append((si, fi, pts, s.fn[fi]))
    return out


def _uv_at(s, fi, q):
    """The face's (affine) uv at point q in its plane, from its first three vertices."""
    pts = [s.verts[i] for i in s.faces[fi]]
    uv = s.fuv[fi]
    a, b, c = pts[0], pts[1], pts[2]
    e1 = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    e2 = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    w = (q[0] - a[0], q[1] - a[1], q[2] - a[2])
    d11, d12, d22 = _dot(e1, e1), _dot(e1, e2), _dot(e2, e2)
    dw1, dw2 = _dot(w, e1), _dot(w, e2)
    den = d11 * d22 - d12 * d12
    if abs(den) < 1e-14:
        return None
    s1 = (d22 * dw1 - d12 * dw2) / den
    s2 = (d11 * dw2 - d12 * dw1) / den
    return (uv[0][0] + s1 * (uv[1][0] - uv[0][0]) + s2 * (uv[2][0] - uv[0][0]),
            uv[0][1] + s1 * (uv[1][1] - uv[0][1]) + s2 * (uv[2][1] - uv[0][1]))


def looks_same(A, fa, B, fb, pts3):
    """True when two coplanar faces would draw identical pixels over their overlap (same material, same uv mapping
    at the overlap's corners): their depth fight is invisible."""
    if A.fm[fa] != B.fm[fb]:
        return False
    for q in pts3:
        ua, ub = _uv_at(A, fa, q), _uv_at(B, fb, q)
        if ua is None or ub is None or abs(ua[0] - ub[0]) > 2e-3 or abs(ua[1] - ub[1]) > 2e-3:
            return False
    return True


class _Occ:
    """Point-in-solid tests against the closed solids of one LOD (bbox-bucketed)."""

    def __init__(self, M, k):
        self.sol = []
        self.cell = {}
        for si, s in enumerate(M.solids):
            if k not in s.vis or not s.closed or len(s.faces) < 4:
                continue
            pl = []
            for fi, f in enumerate(s.faces):
                n = s.fn[fi]
                pl.append((n, _dot(n, s.verts[f[0]])))
            bb = s.bbox()
            self.sol.append((si, bb, pl))
            i = len(self.sol) - 1
            for cx in range(int(math.floor(bb[0])), int(math.floor(bb[1])) + 1):
                for cz in range(int(math.floor(bb[4])), int(math.floor(bb[5])) + 1):
                    self.cell.setdefault((cx, cz), []).append(i)

    def inside(self, p, skip=()):
        for i in self.cell.get((int(math.floor(p[0])), int(math.floor(p[2]))), ()):
            si, bb, pl = self.sol[i]
            if si in skip:
                continue
            if not (bb[0] < p[0] < bb[1] and bb[2] < p[1] < bb[3] and bb[4] < p[2] < bb[5]):
                continue
            if all(_dot(n, p) - d < -1e-4 for n, d in pl):
                return True
        return False


def _visible(occ, samples, n, skip):
    """Some sample of the overlap is not covered: in front of it (4 mm out along n) is not inside another solid, and
    it is not a downward face at grade (the terrain covers those)."""
    for q in samples:
        if n[1] < -0.9 and q[1] <= 0.005:
            continue
        p = (q[0] + n[0] * 0.004, q[1] + n[1] * 0.004, q[2] + n[2] * 0.004)
        if not occ.inside(p, skip):
            return True
    return False


_VEC_MIN = 48           # V1: candidate lists longer than this get the numpy pre-filter
FAST = os.environ.get("JP_ZFIGHT_ENGINE", "fast") != "old"     # V1: "old" = the pre-V1 per-face loop (equivalence runs)


def _cand_arrays(cands, F, planes):
    """V1: a candidate list as numpy columns (face index, solid index, canonical normal, box) for _prefilter."""
    import numpy as np
    ci = np.asarray(cands, dtype=np.int64)
    return cands, (ci, np.asarray([F[j][0] for j in cands], dtype=np.int64),
                   np.asarray([planes[j][0] for j in cands], dtype=np.float64),
                   np.asarray([planes[j][3] for j in cands], dtype=np.float64))


def _prefilter(arr, idx, si, cn, bb, tol):
    """V1: the candidates that pass coplanar()'s first four per-pair tests (j > idx, another solid, normals within
    COS, boxes within tol), in list order; the per-pair loop repeats those tests (identical IEEE arithmetic)."""
    import numpy as np
    ci, sol, nrm, box = arr
    m = (ci > idx) & (sol != si)
    m &= ~((nrm[:, 0] * cn[0] + nrm[:, 1] * cn[1] + nrm[:, 2] * cn[2]) < COS)
    m &= ~((bb[1] < box[:, 0] - tol) | (box[:, 1] < bb[0] - tol) | (bb[3] < box[:, 2] - tol) |
           (box[:, 3] < bb[2] - tol) | (bb[5] < box[:, 4] - tol) | (box[:, 5] < bb[4] - tol))
    return ci[m].tolist()


def coplanar(M, lods=(1, 2, 3), tol=TOL, min_area=MIN_AREA, skip=None, occlusion=True):
    """Every overlapping coplanar face pair of different solids. 'same' = same-facing, visibly different (material or
    uv) and not covered by a third solid (occlusion=True); 'hidden' = same-facing but drawn identically or covered;
    'opposite' = touching faces."""
    res = {"same": [], "opposite": [], "hidden": []}
    for k in lods:
        occ = _Occ(M, k) if occlusion else None
        F = faces_of(M, k, skip)
        grid = {}
        planes = []
        for idx, (si, fi, pts, n) in enumerate(F):
            ln = math.sqrt(_dot(n, n)) or 1.0
            n = (n[0] / ln, n[1] / ln, n[2] / ln)
            d = sum(_dot(n, p) for p in pts) / len(pts)
            cn, cd, sg = _canon(n, d)
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            zs = [p[2] for p in pts]
            planes.append((cn, cd, sg, (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))))
            key = (round(cn[0] * NQ), round(cn[1] * NQ), round(cn[2] * NQ), round(cd * DQ))
            grid.setdefault(key, []).append(idx)
        seen = set()
        # V1 (2026-10-01): the 81-cell candidate list depends only on the face's key: built once per key (not per
        # face), and the cheap rejections (j <= idx, same solid, normals not parallel, boxes apart) run as one numpy
        # pass over it for long lists. Same pairs, same order, same float arithmetic as the per-pair tests below.
        ccache = {}
        for idx, (si, fi, pts, n) in enumerate(F):
            cn, cd, sg, bb = planes[idx]
            key = (round(cn[0] * NQ), round(cn[1] * NQ), round(cn[2] * NQ), round(cd * DQ))
            cc = ccache.get(key) if FAST else None
            if cc is None:
                cands = []
                for a in (-1, 0, 1):
                    for b in (-1, 0, 1):
                        for c in (-1, 0, 1):
                            for e in (-1, 0, 1):
                                cands += grid.get((key[0] + a, key[1] + b, key[2] + c, key[3] + e), ())
                cc = ccache[key] = _cand_arrays(cands, F, planes) if FAST and len(cands) > _VEC_MIN else (cands, None)
            cands, arr = cc
            if arr is not None:
                cands = _prefilter(arr, idx, si, cn, bb, tol)
            for j in cands:
                if j <= idx:
                    continue
                sj, fj, ptsj, nj = F[j]
                if sj == si:
                    continue
                cn2, cd2, sg2, bb2 = planes[j]
                if _dot(cn, cn2) < COS:
                    continue
                if (bb[1] < bb2[0] - tol or bb2[1] < bb[0] - tol or bb[3] < bb2[2] - tol or bb2[3] < bb[2] - tol or
                        bb[5] < bb2[4] - tol or bb2[5] < bb[4] - tol):
                    continue
                if any(abs(_dot(cn, p) - cd) > tol for p in ptsj) or any(abs(_dot(cn2, p) - cd2) > tol for p in pts):
                    continue
                u, v = _basis(cn)
                pa = _ccw([(_dot(p, u), _dot(p, v)) for p in pts])
                pb = _ccw([(_dot(p, u), _dot(p, v)) for p in ptsj])
                ov = _clip(pa, pb)
                if len(ov) < 3:
                    continue
                ar = abs(_area(ov))
                if ar < min_area:
                    continue
                if (idx, j) in seen:
                    continue
                seen.add((idx, j))
                A, Bs = M.solids[si], M.solids[sj]
                # the overlap polygon back in 3D (on face A's plane)
                o3 = [tuple(cn[i] * cd + u[i] * p[0] + v[i] * p[1] for i in range(3)) for p in ov]
                cx = sum(p[0] for p in o3) / len(o3)
                cy = sum(p[1] for p in o3) / len(o3)
                cz = sum(p[2] for p in o3) / len(o3)
                r = (k, round(ar, 4), A.tag or "?", Bs.tag or "?", getattr(A, "src", "") or "",
                     getattr(Bs, "src", "") or "", (round(cx, 3), round(cy, 3), round(cz, 3)),
                     tuple(round(c, 3) for c in cn), A.fm[fi], Bs.fm[fj], si, sj, tuple(A.fn[fi]))
                if sg != sg2:
                    res["opposite"].append(r)
                    continue
                if looks_same(A, fi, Bs, fj, o3[:3] + [(cx, cy, cz)]):
                    res["hidden"].append(r)
                    continue
                if occ is not None:
                    smp = [(cx, cy, cz)] + [tuple(c * 0.75 + q * 0.25 for c, q in zip(p, (cx, cy, cz))) for p in o3]
                    if not _visible(occ, smp, A.fn[fi], (si, sj)):
                        res["hidden"].append(r)
                        continue
                res["same"].append(r)
    return res


def summary(res, which="same", top=8):
    """'tag_a | tag_b: n pairs, area' lines, the biggest groups first."""
    g = {}
    for r in res[which]:
        key = tuple(sorted((r[2], r[3])))
        n, a, ex = g.get(key, (0, 0.0, r))
        g[key] = (n + 1, a + r[1], ex)
    items = sorted(g.items(), key=lambda kv: -kv[1][1])
    return ["%s | %s: %d pairs, %.3f m2 (e.g. LOD %d at %s)" % (k[0], k[1], n, a, ex[0], ex[6])
            for k, (n, a, ex) in items[:top]]


DELTA_NEAR = 0.005      # push for a solid drawn in Resolution 1 (seen up close)
DELTA_FAR = 0.012       # push for a solid only in Resolution 2 / 3 (seen from further away: coarser depth)


def _vol(s):
    b = s.bbox()
    return max(b[1] - b[0], 1e-3) * max(b[3] - b[2], 1e-3) * max(b[5] - b[4], 1e-3)


def _order(s, i):
    """Who stands proud: the smaller solid (volume, 2 % bands); on a tie (crossing kumiko, equal boards) the one
    taller in y, then wider in x, then the earlier solid: a consistent rule, so a lattice resolves in one pass."""
    b = s.bbox()
    v = _vol(s)
    return (round(math.log(v) / math.log(1.02)), -round(b[3] - b[2], 3), -round(b[1] - b[0], 3), i)


def _visual_only(M, s):
    """Split a Geometry / View / Fire solid before it is moved: an untouched copy keeps the collision components
    (vis empty), the moved one stays visual only. Collision, door sweeps and every Geometry check stay as built."""
    if not (s.geo or s.view or s.fire):
        return
    import copy
    keep = copy.copy(s)
    keep.vis = set()
    keep.verts = list(s.verts)
    keep.faces = [list(f) for f in s.faces]
    keep.fn = list(s.fn)
    M.solids.append(keep)
    s.geo = s.view = False
    s.fire = None


def _stretch(s, n, delta):
    """Move the face(s) of s at its max extent along n by delta (affine stretch along n anchored on the opposite
    extreme: planar faces stay planar, a convex solid stays convex). A flat sheet is translated."""
    ds = [_dot(v, n) for v in s.verts]
    lo, hi = min(ds), max(ds)
    if hi - lo < 1e-4:
        s.verts = [(v[0] + n[0] * delta, v[1] + n[1] * delta, v[2] + n[2] * delta) for v in s.verts]
    else:
        if delta < 0 and hi - lo < 3 * abs(delta):
            return False
        s.verts = [(v[0] + n[0] * delta * (d - lo) / (hi - lo), v[1] + n[1] * delta * (d - lo) / (hi - lo),
                    v[2] + n[2] * delta * (d - lo) / (hi - lo)) for v, d in zip(s.verts, ds)]
    s.center = tuple(sum(v[k] for v in s.verts) / len(s.verts) for k in range(3))
    # keep the face materials and uvs (a few mm of stretch); only the outward normals are re-derived
    s.fn = [s._outward(fi) for fi in range(len(s.faces))]
    if s.normals is not None:
        s.normals = s.fn
    return True


def resolve(M, passes=8, log=None):
    """FB2: no two visibly different faces share a plane. The visible same-facing coplanar overlaps (coplanar(),
    'same') of one plane form a graph; its solids are coloured greedily from the biggest down (door leaves first:
    they keep their sweeps), and a solid of colour c stands c x DELTA proud of the plane (its face moves out along
    the shared normal; Resolution 2/3-only solids use the larger far DELTA; an upward face steps down instead; a
    collision solid is split first so Geometry / View / Fire stay exactly as built). So the detail (sill, track, rim beam,
    stringer, kumiko, trim) reads just in front of the larger surface and two crossing bars never end up level again.
    Repeats until nothing visible is left (or `passes`). Returns the number of solids moved per pass."""
    moved = []
    for _ in range(passes):
        r = coplanar(M)
        if not r["same"]:
            break
        groups = {}
        for x in r["same"]:
            si, sj, nrm = x[10], x[11], x[12]
            ln = math.sqrt(_dot(nrm, nrm))
            nrm = (nrm[0] / ln, nrm[1] / ln, nrm[2] / ln)
            d = _dot(nrm, x[6])
            gk = (round(nrm[0], 2), round(nrm[1], 2), round(nrm[2], 2), round(d / 0.002))
            g = groups.setdefault(gk, {"n": nrm, "adj": {}})
            g["adj"].setdefault(si, set()).add(sj)
            g["adj"].setdefault(sj, set()).add(si)
        n_ = 0
        for gk, g in sorted(groups.items()):
            nodes = sorted(g["adj"], key=lambda i: (0 if M.solids[i].door else 1, _order(M.solids[i], i)),
                           reverse=False)
            # biggest first: _order is ascending by size, so walk door leaves first, then the static solids from the
            # largest down
            stat = [i for i in nodes if not M.solids[i].door]
            door = [i for i in nodes if M.solids[i].door]
            order = door + sorted(stat, key=lambda i: _order(M.solids[i], i), reverse=True)
            col = {}
            for i in order:
                used = {col[j] for j in g["adj"][i] if j in col}
                c = 0
                while c in used:
                    c += 1
                col[i] = c
            for i, c in col.items():
                if c == 0:
                    continue
                s_ = M.solids[i]
                delta = (DELTA_NEAR if 1 in s_.vis else DELTA_FAR) * c
                # an upward face steps DOWN instead (a sill / track sinks into the floor, a tie beam's top under the
                # keta): pushing tops up would lift them into roof bodies (C12) and above floor levels
                sign = -1.0 if g["n"][1] > 0.5 else 1.0
                ds = [_dot(v, g["n"]) for v in s_.verts]
                if sign < 0 and max(ds) - min(ds) < 3 * delta:
                    sign = 1.0
                _visual_only(M, s_)
                if _stretch(s_, g["n"], sign * delta):
                    n_ += 1
        moved.append(n_)
        if log is not None:
            log.append("zfight.resolve pass: %d visible pairs, %d solids moved" % (len(r["same"]), n_))
        if not n_:
            break
    return moved
