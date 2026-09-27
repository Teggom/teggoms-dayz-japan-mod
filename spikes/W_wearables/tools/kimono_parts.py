"""Kimono second stage: skin patches ('personality'), lining, weights. See kimono.py for the method."""
import numpy as np

from geom import Surface, smoothstep, tris, unit
from wlib import body
import kimono as K

SKIN_UV = (0.78, 0.50, 0.98, 0.76)     # a plain upper-arm area of the vanilla body atlas (u, v box)
SKIN_K = (0.50, 1.00)                  # uv units per metre (u, v): the atlas is 2:1, so v runs twice as fast
DROP = ("forearm", "forearmroll", "hand", "elbowextra", "forearmextra", "wristextra")


def torso_surface(sex):
    T = body(sex)["torso3"]
    return Surface(T.P, tris(T.F), T.W, T.UV), T


def body_surface(sex):
    B = body(sex)
    P = np.concatenate([B["torso3"].P, B["legs3"].P])
    off = len(B["torso3"].P)
    T = np.concatenate([tris(B["torso3"].F), tris(B["legs3"].F) + off])
    W = list(B["torso3"].W) + list(B["legs3"].W)
    return Surface(P, T, W)


def add_neck_skin(g, sex, lod):
    """skin in the V and around the neck, lying on the vanilla torso surface. UVs go to a plain skin area of
    the body atlas, because the vanilla torso's own trunk UVs belong to its undershirt texture"""
    lm = g.meta["lm"]
    prof = g.meta["prof"]
    ts, T = torso_surface(sex)
    top = float(T.P[:, 1].max()) + 0.004
    y0 = lm["v"] - 0.035
    nr = (12, 8, 5)[lod]
    nc = (40, 28, 16)[lod]
    ys = np.linspace(y0, top, nr)
    phis = np.linspace(0, 2 * np.pi, nc + 1)
    th_n = np.radians(lm["theta_n"])
    grid = np.array([[prof.point(ph, y, 0.0) for ph in phis] for y in ys])
    flat = grid.reshape(-1, 3)
    ti, bc, cp, dist = ts.closest(flat)
    nrm = ts.interp_normal(ti, bc)
    cp = cp - nrm * 0.0006
    W = ts.interp_weights(ti, bc)
    grid = cp.reshape(grid.shape)

    def keep(ph, y):
        a = ph if ph <= np.pi else 2 * np.pi - ph           # angle from the front, 0..pi
        if a < th_n:
            edge = lm["v"] + (lm["n_side"] - lm["v"]) * a / th_n
        else:
            c = (a - th_n) / (2 * np.pi - 2 * th_n)
            edge = K.neckline_y(lm, c)
        return y > edge - 0.028
    base = g.add_points(grid.reshape(-1, 3), W)
    C = nc + 1
    f0 = len(g.F)
    for r in range(nr - 1):
        for c in range(nc):
            if not keep((phis[c] + phis[c + 1]) / 2, (ys[r] + ys[r + 1]) / 2):
                continue
            v = [base + r * C + c, base + r * C + c + 1, base + (r + 1) * C + c + 1, base + (r + 1) * C + c]
            uv = []
            for rr, cc in ((r, c), (r, c + 1), (r + 1, c + 1), (r + 1, c)):
                s_ = ((phis[cc] + np.pi) % (2 * np.pi) - np.pi) * 0.075   # ~arc length around the neck
                u = (SKIN_UV[0] + SKIN_UV[2]) / 2 + s_ * SKIN_K[0]
                vv = SKIN_UV[1] + (top - ys[rr]) * SKIN_K[1]
                uv.append((float(np.clip(u, SKIN_UV[0], SKIN_UV[2])), float(np.clip(vv, SKIN_UV[1], SKIN_UV[3]))))
            g.add_face(v, uv, "skin")
    zc_at = lambda y: np.interp(y, prof.ys, prof.zc)  # noqa: E731
    g.orient(range(f0, len(g.F)), lambda c: np.array([c[0], 0, c[2] - zc_at(c[1])]))


def chart_uv(ts, q, tri):
    """UV of point q from ONE reference triangle (affine, barycentrics may be negative)"""
    A, B, C = ts.P[tri[0]], ts.P[tri[1]], ts.P[tri[2]]
    n = np.cross(B - A, C - A)
    nn = np.dot(n, n)
    wb = np.dot(np.cross(q - A, C - A), n) / nn
    wc = np.dot(np.cross(B - A, q - A), n) / nn
    wa = 1 - wb - wc
    uv = wa * ts.UV[tri[0]] + wb * ts.UV[tri[1]] + wc * ts.UV[tri[2]]
    return (float(uv[0]), float(uv[1]))


def add_forearm_skin(g, sex, lod):
    """the forearm inside each wide sleeve: a tube snapped on the vanilla arm, with the vanilla arm's own atlas
    UVs (per face from one reference triangle, so no face straddles a UV seam) and its weights"""
    ts, T = torso_surface(sex)
    for side, info in g.meta["sleeves"].items():
        J_arm, J_fore, J_hand = info["J"]
        a = unit(J_hand - J_fore)
        p1 = J_hand - a * 0.035
        p0 = p1 - a * 0.13              # only the last 13 cm are ever seen (through the cuff); never near the elbow
        nr = (7, 5, 3)[lod]
        ns = (12, 8, 6)[lod]
        up = unit(np.cross(a, [0, 0, 1.0]))
        sd = unit(np.cross(up, a))
        rings = []
        for t in np.linspace(0, 1, nr):
            c = p0 + (p1 - p0) * t
            rings.append([c + (up * np.cos(2 * np.pi * k / ns) + sd * np.sin(2 * np.pi * k / ns)) * 0.06 for k in range(ns)])
        rings = np.array(rings).reshape(-1, 3)
        ti, bc, cp, dist = ts.closest(rings)
        nrm = ts.interp_normal(ti, bc)
        # 3 mm inside the vanilla arm surface: hidden by the sleeve everywhere except through the cuff
        cp = cp - nrm * 0.003
        W = ts.interp_weights(ti, bc)
        base = g.add_points(cp, W)
        f0 = len(g.F)
        for r in range(nr - 1):
            for k in range(ns):
                k1 = (k + 1) % ns
                v = [base + r * ns + k, base + r * ns + k1, base + (r + 1) * ns + k1, base + (r + 1) * ns + k]
                g.add_face(v, [(0.0, 0.0)] * 4, "skin")
        g.orient(range(f0, len(g.F)), lambda c, p0=p0, a=a: c - (p0 + a * np.dot(c - p0, a)))
        Pa = g.arrays()
        for fi in range(f0, len(g.F)):
            f = g.F[fi]
            t_, _, _, _ = ts.closest(Pa[f].mean(0)[None, :])
            tri = ts.T[t_[0]]
            g.FUV[fi] = [chart_uv(ts, Pa[v], tri) for v in f]


def add_lining(g):
    """inward-facing copies of the trunk and sleeve faces (4 mm in): the hem, the sleeves and the collar gap
    never show a see-through back face. Same UVs (a same-cloth lining)"""
    mats = [m for m in set(g.FM) if m == "trunk" or m.startswith("sleeve_") or m.startswith("cuff_")]
    g.inner_shell(offset=0.004, mats=mats, mat_map={m: "lining" for m in mats})


def skirt_weights(x, y, crotch, hem, mode="A"):
    """the vanilla coat rule: sides follow their own thigh, the centre is split between both, the pelvis share
    falls with depth. mode B: below the knee the robe also follows the shins (the long-robe experiment)"""
    s = float(smoothstep(-0.06, 0.06, x))
    knee = 0.50
    if y >= knee:
        d = (crotch - y) / (crotch - knee)
        p = 0.50 - 0.34 * d
    else:
        d = (knee - y) / max(knee - hem, 1e-3)
        p = 0.16 - 0.06 * d
    p = float(np.clip(p, 0.08, 0.55))
    legs = 1 - p
    w = {"pelvis": p}
    if mode == "B" and y < knee:
        q = 0.45 * float(smoothstep(knee, knee - 0.25, y))
        w["leftupleg"] = legs * s * (1 - q)
        w["leftleg"] = legs * s * q
        w["rightupleg"] = legs * (1 - s) * (1 - q)
        w["rightleg"] = legs * (1 - s) * q
    else:
        w["leftupleg"] = legs * s
        w["rightupleg"] = legs * (1 - s)
    return {b: v for b, v in w.items() if v > 1e-4}


def assign_weights(g, sex, skirt_mode="A"):
    lm = g.meta["lm"]
    hem = g.meta["hem"]
    crotch = lm["crotch"]
    P = g.arrays()
    bs = body_surface(sex)
    base, R, C, n_closed = g.meta["trunk"]
    trunk_idx = list(range(base, base + R * C))
    # 1. trunk: transfer above the crotch, the skirt rule below, blended over 8 cm
    ti, bc, cp, dist = bs.closest(P[trunk_idx])
    tw = bs.interp_weights(ti, bc)
    for n, i in enumerate(trunk_idx):
        w = {b: v for b, v in tw[n].items() if not any(b.endswith(d) for d in DROP)}
        x, y, z = P[i]
        k = float(smoothstep(crotch + 0.04, crotch - 0.08, y))   # the seat keeps the body's own weights longer
        if k > 0:
            sw = skirt_weights(x, y, crotch, hem, skirt_mode)
            w = {b: (1 - k) * w.get(b, 0.0) + k * sw.get(b, 0.0) for b in set(w) | set(sw)}
        g.W[i] = w
    g.smooth_weights(iterations=4, alpha=0.5, mask=trunk_idx)
    # 2. sleeves: along the arm chain (projection on the arm axis), the root blended with the body transfer
    sl = g.meta["sleeves"]
    sleeve_pts = set()
    for side, info in sl.items():
        J_arm, J_fore, J_hand = info["J"]
        a = unit(J_hand - J_arm)
        Lu = np.linalg.norm(J_fore - J_arm)
        Lf = np.linalg.norm(J_hand - J_fore)
        hb, ns = info["hole"]
        idx = list(range(info["base"], info["base"] + info["n"])) + list(range(hb, hb + ns))
        sleeve_pts.update(idx)
        ti, bc, cp, dist = bs.closest(P[idx])
        bw = bs.interp_weights(ti, bc)
        for n, i in enumerate(idx):
            t = float(np.dot(P[i] - J_arm, a))
            fore = float(smoothstep(Lu - 0.07, Lu + 0.07, t))
            up_roll = 0.45 * float(smoothstep(0.05, Lu - 0.03, t))
            fo_roll = 0.55 * float(smoothstep(Lu, Lu + Lf, t))
            w = {side + "arm": (1 - fore) * (1 - up_roll), side + "armroll": (1 - fore) * up_roll,
                 side + "forearm": fore * (1 - fo_roll), side + "forearmroll": fore * fo_roll}
            root = float(smoothstep(0.13, 0.03, t))
            if root > 0:
                b = {k_: v for k_, v in bw[n].items() if not any(k_.endswith(d) for d in DROP)}
                w = {k_: (1 - root) * w.get(k_, 0.0) + root * b.get(k_, 0.0) for k_ in set(w) | set(b)}
            g.W[i] = w
    # 3. parts lying on the trunk (collar, flap, obi, knot): from the trunk itself, so they never separate
    trunk_faces = [f for f, m in zip(g.F, g.FM) if m == "trunk"]
    used = sorted({v for f in trunk_faces for v in f})
    remap = {v: i for i, v in enumerate(used)}
    tsurf = Surface(P[used], tris([[remap[v] for v in f] for f in trunk_faces]), [g.W[v] for v in used])
    rest = [i for i in range(base + R * C, len(P)) if not g.W[i] and i not in sleeve_pts]
    if rest:
        ti, bc, cp, dist = tsurf.closest(P[rest])
        for i, w in zip(rest, tsurf.interp_weights(ti, bc)):
            g.W[i] = w
    g.clean_weights(max_bones=4, min_w=0.02)
    empty = [i for i, w in enumerate(g.W) if not w]
    assert not empty, "unweighted points: %d" % len(empty)


def build_full(sex, length="short", lod=0, skirt_mode="A", lining=True):
    g = K.build(sex, length, lod)
    add_neck_skin(g, sex, lod)
    add_forearm_skin(g, sex, lod)
    assign_weights(g, sex, skirt_mode)
    g.triangulate()
    if lining:
        add_lining(g)
    return g


if __name__ == "__main__":
    import time
    from collections import Counter
    t = time.time()
    g = build_full("m", "short")
    print(g.stats(), "%.1fs" % (time.time() - t))
    print(Counter(g.FM))
    print(Counter(len(w) for w in g.W))
