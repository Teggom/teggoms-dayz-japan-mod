"""V1 prototype: any-hit ray casting with per-origin angular (cone) culling + distance stages. Same per-(ray, triangle)
hit predicate as raycheck._cast_brute (two-sided Moller-Trumbore, u/v >= -1e-9, u+v <= 1+1e-9, 1e-4 < t < tmax)."""
import numpy as np

NEAR = 0.05          # triangles closer than this (box distance) to the origin are always candidates
PAD = 1e-4           # angular pad (rad) on every cone: covers the 1e-9 barycentric tolerance many times over
STAGES = (0.75, 1.5, 3.0, 6.0, 12.0)  # distance stages (box distance of the triangle), then the rest


def _dot(a, b):
    return np.einsum("pk,pk->p", a, b)


def hit_pairs(T, O, D, ri, ti, tmax):
    """The _cast_brute hit predicate for the pairs (ray ri[k], triangle ti[k]). tmax: scalar or per-ray array."""
    v0 = T[ti, 0]
    e1 = T[ti, 1] - v0
    e2 = T[ti, 2] - v0
    o = O[ri]
    dv = D[ri]
    p = np.cross(dv, e2)
    det = _dot(p, e1)
    ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
    tv = o - v0
    uu = _dot(tv, p) * inv
    q = np.cross(tv, e1)
    vv = _dot(dv, q) * inv
    tt = _dot(q, e2) * inv
    tm = tmax[ri] if isinstance(tmax, np.ndarray) else tmax
    return ok & (uu >= -1e-9) & (vv >= -1e-9) & (uu + vv <= 1 + 1e-9) & (tt > 1e-4) & (tt < tm)


def box_dist(Tmin, Tmax, o):
    """Distance from o to every triangle's axis-aligned box (a lower bound of the distance to the triangle)."""
    gap = np.maximum(np.maximum(Tmin - o, o - Tmax), 0.0)
    return np.sqrt((gap * gap).sum(1))


def _cones(T, o, bdist):
    """Per triangle of T: (axis (N,3), cos threshold (N,)) of the cone of directions from o that holds it. A threshold
    of -2 = always a candidate (near, or a cone of >= 90 deg)."""
    V = T - o                                   # (N,3,3)
    ln = np.sqrt((V * V).sum(2))                # (N,3)
    U = V / np.maximum(ln, 1e-12)[:, :, None]
    S = U.sum(1)
    sl = np.sqrt((S * S).sum(1))
    A = S / np.maximum(sl, 1e-12)[:, None]
    c = np.einsum("nk,nmk->nm", A, U).min(1)
    c = np.clip(c, -1.0, 1.0)
    th = np.arccos(c) + PAD
    thr = np.cos(th)
    bad = (bdist < NEAR) | (th >= np.pi / 2 - 1e-3) | (sl < 1e-9) | (ln.min(1) < 1e-9)
    thr = np.where(bad, -2.0, thr)
    return A, thr


def escapes(T, O, D, tmax=60.0):
    """True per ray when it hits no triangle at 1e-4 < t < tmax (tmax scalar or per ray). D must be unit vectors."""
    O = np.asarray(O, float)
    D = np.asarray(D, float)
    n = len(O)
    hit = np.zeros(n, bool)
    if n == 0 or len(T) == 0:
        return ~hit
    tm_arr = np.broadcast_to(np.asarray(tmax, float), (n,)).copy() if np.ndim(tmax) else None
    Tmin, Tmax = T.min(1), T.max(1)
    uo, inv = np.unique(O, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    order = np.argsort(inv, kind="stable")
    bounds = np.searchsorted(inv[order], np.arange(len(uo) + 1))
    for g in range(len(uo)):
        rays = order[bounds[g]:bounds[g + 1]]
        o = uo[g]
        bd = box_dist(Tmin, Tmax, o)
        tmg = float(tm_arr[rays].max()) if tm_arr is not None else float(tmax)
        keep = bd <= tmg + 1e-6
        edges = [0.0] + [s for s in STAGES if s < tmg] + [np.inf]
        todo = rays
        for s0, s1 in zip(edges[:-1], edges[1:]):
            if not len(todo):
                break
            tsel = np.where(keep & (bd >= s0) & (bd < s1))[0]
            if not len(tsel):
                continue
            A, thr = _cones(T[tsel], o, bd[tsel])
            M = (D[todo] @ A.T) >= thr[None, :]
            rr, tt_ = np.nonzero(M)
            if not len(rr):
                continue
            ri = todo[rr]
            h = hit_pairs(T, O, D, ri, tsel[tt_], tm_arr if tm_arr is not None else tmax)
            if h.any():
                hit[ri[h]] = True
                todo = todo[~hit[todo]]
    return ~hit
