"""JP_Tabi_Waraji: split-toe cloth socks (tabi) + straw sandals (waraji) as one Feet-slot item.

Method (the "offset a smoothed vanilla part" recipe, reusable for socks / tight sleeves / leggings):
  1. weld the vanilla bare foot (feet3_<sex>) per foot; it has one open loop at the ankle
  2. Laplacian-smooth the toe region so the toes merge (a mitten), keeping the sole flat
  3. cut the split-toe groove between the big toe and the second toe
  4. extrude the ankle loop up the shin, projecting each new ring onto the vanilla leg + ease
  5. offset everything outward along the normals by EASE (cloth thickness)
  6. weights = closest-point transfer from the vanilla foot / leg, then smoothed
The sandal sole is the foot's plan-view outline + margin; the cords are tubes routed over the sock surface.
"""
import numpy as np

from garment import Garment, tube
from geom import weld, tris, vertex_normals, Surface, unit, smoothstep, convex_hull_2d
from wlib import load_ref

EASE = 0.0035
SHAFT = {"m": 0.185, "f": 0.175}        # tabi top height (vanilla feet end at ~0.12 / 0.107)
SOLE_TOP, SOLE_BOT = 0.0025, -0.012     # waraji sole (vanilla shoes also sink ~1.3 cm)
TABI_FLOOR = 0.004

# texture atlas regions (u0, v0, u1, v1), 1024 x 1024
R_TOP = (0.00, 0.00, 0.50, 0.50)       # tabi top / instep (planar XZ)
R_SIDE = (0.00, 0.50, 1.00, 0.75)      # tabi sides (cylindrical)
R_SOLE = (0.50, 0.00, 0.75, 0.50)      # tabi sole cloth (grey, planar)
R_STRAW = (0.75, 0.00, 1.00, 0.50)     # waraji sole top / bottom (planar)
R_STRAWSIDE = (0.00, 0.75, 0.50, 0.85)
R_CORD = (0.50, 0.75, 1.00, 0.85)
R_KOHAZE = (0.00, 0.85, 0.50, 1.00)    # (unused region reserved for clasps drawn into R_SIDE)


def reg_uv(reg, s, t):
    u0, v0, u1, v1 = reg
    return (u0 + (u1 - u0) * float(np.clip(s, 0, 1)), v0 + (v1 - v0) * float(np.clip(t, 0, 1)))


def foot_parts(sex):
    m = load_ref("feet3_" + sex)
    U, inv = weld(m.P, 1e-4)
    T = tris([[inv[i] for i in f] for f in m.F])
    # weights for welded points (first occurrence)
    W = [None] * len(U)
    for i, j in enumerate(inv):
        if W[j] is None:
            W[j] = {b: w for b, w in m.W[i]}
    feet = {}
    for side, sgn in (("left", 1), ("right", -1)):
        keep = np.where(U[:, 0] * sgn > 0)[0]
        remap = -np.ones(len(U), dtype=int)
        remap[keep] = np.arange(len(keep))
        TT = np.array([[remap[v] for v in t] for t in T if all(remap[v] >= 0 for v in t)])
        feet[side] = (U[keep].copy(), TT, [W[k] for k in keep])
    return feet


def boundary_loop(T, n):
    from collections import Counter
    ec = Counter()
    for t in T:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            ec[(a, b)] += 1
    # directed boundary edges: an edge (a, b) whose reverse (b, a) is absent
    bd = {}
    for (a, b), c in ec.items():
        if (b, a) not in ec:
            bd[a] = b
    start = next(iter(bd))
    loop = [start]
    while True:
        nx = bd.get(loop[-1])
        if nx is None or nx == start:
            break
        loop.append(nx)
    return loop


def neighbours(T, n):
    nb = [set() for _ in range(n)]
    for t in T:
        for a in t:
            for b in t:
                if a != b:
                    nb[a].add(b)
    return nb


def build_tabi(sex, side):
    sgn = 1 if side == "left" else -1
    P, T, W = foot_parts(sex)[side]
    P = P.copy()
    n = len(P)
    nb = neighbours(T, n)
    loop = boundary_loop(T, n)
    # landmarks
    toe_front = P[:, 2].min()
    ball_z = toe_front + 0.075               # toe region = the front 7.5 cm
    toe = (P[:, 2] < ball_z)
    # the groove between big toe and second toe: the big toe is the medial (inner) toe
    front = P[P[:, 2] < toe_front + 0.02]
    med = front[np.argmin(front[:, 0] * sgn)]    # most medial front point ~ big toe
    x_gap = med[0] + sgn * 0.024
    # 2. smooth the toe region (merge toes) - positions only, sole kept flat
    for it in range(14):
        Q = P.copy()
        for i in np.where(toe)[0]:
            if not nb[i]:
                continue
            avg = P[list(nb[i])].mean(0)
            Q[i] = P[i] * 0.4 + avg * 0.6
        Q[:, 1] = np.maximum(Q[:, 1], 0.0)
        P = Q
    # 3. offset outward (cloth), sole clamped to the floor
    from geom import face_normals
    fn = face_normals(P, T)
    vn = np.zeros_like(P)
    for k in range(3):
        np.add.at(vn, T[:, k], fn)
    vn = unit(vn)
    P = P + vn * EASE
    P[:, 1] = np.maximum(P[:, 1], TABI_FLOOR)
    # groove: pull points near the gap line inward/back, strongest at the tip
    tipw = smoothstep(toe_front + 0.045, toe_front, P[:, 2])
    lat = np.exp(-((P[:, 0] - x_gap) / 0.007) ** 2)
    up = smoothstep(0.004, 0.02, P[:, 1])
    d = 0.011 * tipw * lat
    P[:, 2] += d * 1.1                     # back
    P[:, 1] -= d * 0.6 * up                # and down a little on top
    # 4. extrude the ankle loop up the shin, projected on the vanilla leg + ease
    legs = load_ref("legs3_" + sex)
    LU, linv = weld(legs.P, 1e-4)
    LT = tris([[linv[i] for i in f] for f in legs.F])
    LW = [None] * len(LU)
    for i, j in enumerate(linv):
        if LW[j] is None:
            LW[j] = legs.W[i]
    keep = np.where(LU[:, 0] * sgn > 0)[0]
    remap = -np.ones(len(LU), dtype=int)
    remap[keep] = np.arange(len(keep))
    LTT = np.array([[remap[v] for v in t] for t in LT if all(remap[v] >= 0 for v in t)])
    leg_surf = Surface(LU[keep], LTT, [LW[k] for k in keep])
    lp = P[loop]
    y0 = lp[:, 1].mean()
    ytop = SHAFT[sex]
    ring_ys = np.linspace(y0, ytop, 5)[1:]
    centre = lp.mean(0)
    rings = []
    for y in ring_ys:
        q = lp.copy()
        q[:, 1] = y
        # radial probe from the leg axis at this height
        ti, bc, cp, dist = leg_surf.closest(q)
        nrm = leg_surf.interp_normal(ti, bc)
        rings.append(cp + nrm * (EASE + 0.0015))
    # assemble garment points: foot points, then rings
    g = Garment("tabi_%s_%s" % (sex, side))
    base = g.add_points(P)
    ring_base = [g.add_points(r) for r in rings]
    # weights: foot from the vanilla foot, rings from the vanilla leg
    Wt = [dict(w) for w in W]
    for r in rings:
        ti, bc, cp, dist = leg_surf.closest(r)
        Wt += leg_surf.interp_weights(ti, bc)
    g.set_weights(Wt)
    # --- faces + UVs
    P_all = g.arrays()
    axis_c = np.array([centre[0], 0, centre[2]])

    def cyl_uv(p):
        a = np.arctan2((p[0] - axis_c[0]) * sgn, -(p[2] - axis_c[2]))   # 0 = front, + = lateral
        return reg_uv(R_SIDE, (a / (2 * np.pi)) % 1.0, 1.0 - (p[1] / 0.2))

    xmin, xmax = P[:, 0].min() - 0.01, P[:, 0].max() + 0.01
    zmin, zmax = P[:, 2].min() - 0.01, P[:, 2].max() + 0.01

    def top_uv(p, reg):
        s = (p[0] - xmin) / (xmax - xmin)
        if sgn < 0:
            s = 1 - s
        return reg_uv(reg, s, (p[2] - zmin) / (zmax - zmin))

    fn = face_normals(P, T)
    for t, nrm in zip(T, fn):
        pts = [P_all[base + v] for v in t]
        if nrm[1] < -0.5:
            uvs = [top_uv(p, R_SOLE) for p in pts]
            mat = "tabi"
        elif nrm[1] > 0.55 and np.mean([p[2] for p in pts]) < centre[2] - 0.02:
            uvs = [top_uv(p, R_TOP) for p in pts]
            mat = "tabi"
        else:
            uvs = [cyl_uv(p) for p in pts]
            # keep one chart per face (avoid the u wrap)
            us = [u for u, _ in uvs]
            if max(us) - min(us) > 0.5 * (R_SIDE[2] - R_SIDE[0]):
                uvs = [(u + (R_SIDE[2] - R_SIDE[0]) if u < 0.5 else u, v) for u, v in uvs]
                uvs = [(min(u, R_SIDE[2]), v) for u, v in uvs]
            mat = "tabi"
        g.add_face([base + v for v in t], uvs, mat)
    # loop -> rings (the loop direction decides the winding; check below)
    rows = [[base + v for v in loop]] + [[rb + k for k in range(len(loop))] for rb in ring_base]
    for r in range(len(rows) - 1):
        for k in range(len(loop)):
            k1 = (k + 1) % len(loop)
            v = [rows[r][k], rows[r + 1][k], rows[r + 1][k1], rows[r][k1]]
            g.add_face(v, [cyl_uv(P_all[i]) for i in v], "tabi")
    # top hem: a turned-in lip 1.2 cm deep, so the opening has a visible thickness
    top = rows[-1]
    tp = P_all[top]
    cen = tp.mean(0)
    dirs = unit((tp - cen) * np.array([1, 0, 1]))
    lip_top = g.add_points(tp + np.array([0, 0.002, 0]) - dirs * 0.001)
    lip_in = g.add_points(tp - dirs * 0.003 - np.array([0, 0.012, 0]))
    for k in range(len(top)):
        g.W[lip_top + k] = dict(g.W[top[k]])
        g.W[lip_in + k] = dict(g.W[top[k]])
    for k in range(len(top)):
        k1 = (k + 1) % len(top)
        v = [top[k], lip_top + k, lip_top + k1, top[k1]]
        g.add_face(v, [cyl_uv(g.P[i]) for i in v], "tabi")
        v = [lip_top + k, lip_in + k, lip_in + k1, lip_top + k1]
        g.add_face(v, [cyl_uv(g.P[i]) for i in v], "tabi")
    g.meta = {"loop": loop, "x_gap": x_gap, "toe_front": toe_front, "sgn": sgn, "centre": centre,
              "foot_pts": P, "foot_tris": T}
    return g


def orient_check(g, centre_fn):
    from geom import face_normals
    P = g.arrays()
    T = np.array([f[:3] for f in g.F])
    fn = face_normals(P, T)
    c = np.array([P[f].mean(0) for f in g.F])
    d = np.einsum("ij,ij->i", fn, c - np.array([centre_fn(x) for x in c]))
    return d


if __name__ == "__main__":
    for sex in "mf":
        for side in ("left", "right"):
            g = build_tabi(sex, side)
            print(g.stats())


# ---------------------------------------------------------------------------------------------- waraji
def build_waraji(sex, side, tb, segs=40, cord_sides=6):
    """straw sole under the tabi + cords routed over the tabi surface. tb = the tabi Garment of that foot."""
    sgn = tb.meta["sgn"]
    FP = tb.meta["foot_pts"]
    g = Garment("waraji_%s_%s" % (sex, side))
    # plan outline: hull of the sock's low points + margin, resampled by angle around its centroid
    low = FP[FP[:, 1] < 0.02][:, [0, 2]]
    hull = convex_hull_2d(low)
    c = hull.mean(0)
    ang = np.linspace(0, 2 * np.pi, segs, endpoint=False)
    from geom import polar_profile
    rad = polar_profile(hull, c, ang) + 0.007
    outline = np.stack([c[0] + rad * np.sin(ang), c[1] - rad * np.cos(ang)], 1)
    # a straw sandal is a little longer at the front and back than the foot
    fwd = outline[:, 1] < c[1]
    outline[:, 1] += np.where(fwd, -0.004, 0.006) * np.abs(np.cos(ang))
    top = np.stack([outline[:, 0], np.full(segs, SOLE_TOP), outline[:, 1]], 1)
    bot = np.stack([outline[:, 0], np.full(segs, SOLE_BOT), outline[:, 1]], 1)
    zmin, zmax = outline[:, 1].min(), outline[:, 1].max()
    xmin, xmax = outline[:, 0].min(), outline[:, 0].max()

    def plan_uv(p, reg):
        s = (p[0] - xmin) / (xmax - xmin)
        return reg_uv(reg, s if sgn > 0 else 1 - s, (p[2] - zmin) / (zmax - zmin))
    ct = g.add_points([[c[0], SOLE_TOP, c[1]]])
    cb = g.add_points([[c[0], SOLE_BOT, c[1]]])
    t0 = g.add_points(top)
    b0 = g.add_points(bot)
    for k in range(segs):
        k1 = (k + 1) % segs
        g.add_face([ct, t0 + k1, t0 + k], [plan_uv(g.P[i], R_STRAW) for i in (ct, t0 + k1, t0 + k)], "straw")
        g.add_face([cb, b0 + k, b0 + k1], [plan_uv(g.P[i], R_STRAW) for i in (cb, b0 + k, b0 + k1)], "straw")
        v = [b0 + k, t0 + k, t0 + k1, b0 + k1]
        uvs = [reg_uv(R_STRAWSIDE, (k + (1 if i in (2, 3) else 0)) / segs, 0 if i in (1, 2) else 1) for i in range(4)]
        g.add_face(v, uvs, "straw")
    # weights: closest vanilla-foot point below
    foot = foot_parts(sex)[side]
    fs = Surface(foot[0], foot[1], foot[2])
    q = g.arrays().copy()
    q[:, 1] = 0.005
    ti, bc, cp, dist = fs.closest(q)
    g.set_weights(fs.interp_weights(ti, bc))
    # ---- cords (hanao): tubes over the tabi surface
    ts = Surface(tb.arrays(), tb.tri_faces(), [tb.W[i] for i in range(len(tb.P))])
    tf = tb.meta["toe_front"]
    xg = tb.meta["x_gap"]
    ank = tb.meta["centre"]
    heel_z = FP[:, 2].max()
    med = lambda k: ank[0] - sgn * k   # noqa: E731  medial side offset
    lat = lambda k: ank[0] + sgn * k   # noqa: E731
    front = [xg, 0.012, tf + 0.012]
    paths = [
        # front loop (chichi) -> medial side loop -> up to the ankle
        [front, [xg - sgn * 0.004, 0.035, tf + 0.035], [med(0.03), 0.045, ank[2] - 0.045], [med(0.045), 0.02, ank[2] - 0.02],
         [med(0.045), 0.03, ank[2] + 0.005], [med(0.04), 0.07, ank[2] + 0.01]],
        [front, [xg + sgn * 0.006, 0.035, tf + 0.035], [lat(0.02), 0.05, ank[2] - 0.05], [lat(0.045), 0.02, ank[2] - 0.02],
         [lat(0.05), 0.03, ank[2] + 0.005], [lat(0.045), 0.07, ank[2] + 0.01]],
        # ankle wrap: behind the heel, around, tied in front on the lateral side
        [[med(0.04), 0.07, ank[2] + 0.01], [med(0.02), 0.075, heel_z - 0.005], [ank[0], 0.078, heel_z + 0.002],
         [lat(0.02), 0.075, heel_z - 0.005], [lat(0.045), 0.07, ank[2] + 0.01], [lat(0.035), 0.085, ank[2] - 0.035],
         [ank[0], 0.09, ank[2] - 0.05], [med(0.035), 0.085, ank[2] - 0.035], [med(0.04), 0.07, ank[2] + 0.01]],
        # heel return loop (kaeshi) from the sole back edge up to the wrap
        [[med(0.02), 0.012, heel_z - 0.012], [ank[0], 0.03, heel_z + 0.004], [lat(0.02), 0.012, heel_z - 0.012]],
    ]
    cr = 0.0035
    for pi_, path in enumerate(paths):
        path = np.array(path, dtype=float)
        # densify with Catmull-Rom-ish linear resampling
        dens = []
        for a, b in zip(path[:-1], path[1:]):
            for t in np.linspace(0, 1, 5, endpoint=False):
                dens.append(a + (b - a) * t)
        dens.append(path[-1])
        dens = np.array(dens)
        # smooth
        for _ in range(3):
            dens[1:-1] = dens[1:-1] * 0.5 + (dens[:-2] + dens[2:]) * 0.25
        # snap onto the tabi surface + cord radius
        ti, bc, cp, dist = ts.closest(dens)
        nrm = ts.interp_normal(ti, bc)
        onsurf = cp + nrm * (cr + 0.0008)
        onsurf[:, 1] = np.maximum(onsurf[:, 1], SOLE_TOP + cr)
        ups = [nrm[i] for i in range(len(onsurf))]
        rings = tube(onsurf, [(cr, cr)] * len(onsurf), ups, cord_sides)
        cw = ts.interp_weights(ti, bc)
        base = g.add_points(rings.reshape(-1, 3), [cw[i] for i in range(len(onsurf)) for _ in range(cord_sides)])
        L = len(onsurf)
        for i in range(L - 1):
            for k in range(cord_sides):
                k1 = (k + 1) % cord_sides
                v = [base + i * cord_sides + k, base + i * cord_sides + k1, base + (i + 1) * cord_sides + k1, base + (i + 1) * cord_sides + k]
                uvs = [reg_uv(R_CORD, (i + (1 if j in (2, 3) else 0)) / (L - 1), (k + (1 if j in (1, 2) else 0)) / cord_sides) for j in range(4)]
                g.add_face(v, uvs, "straw")
    # everything above was wound the other way round (checked in the backface QA render): flip
    g.F = [f[::-1] for f in g.F]
    g.FUV = [u[::-1] for u in g.FUV]
    return g


def build_item(sex, lod=0):
    """both feet: tabi + waraji, one Garment, material 'tabi' for everything (one atlas)"""
    out = Garment("tabi_waraji_%s" % sex)
    for side in ("left", "right"):
        tb = build_tabi(sex, side)
        wr = build_waraji(sex, side, tb, segs=(40, 24, 14)[lod], cord_sides=(6, 4, 3)[lod])
        out.merge(tb)
        out.merge(wr)
    out.FM = ["tabi" for _ in out.FM]
    out.smooth_weights(iterations=2, alpha=0.4)
    out.clean_weights()
    return out
