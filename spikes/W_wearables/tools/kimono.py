"""JP_Kimono_Short / JP_Kimono_Long: a kosode-style kimono (V collar crossed left-over-right, wide sleeves,
obi) for the Body slot, generated against the vanilla male / female body.

The method (reusable for any loose top, coat or robe):
  PROFILE  slice the vanilla trunk (torso3 without the arm-weighted faces) + legs3 every centimetre, take the
           convex hull of each slice, read its radius in 72 directions around a smoothed centre line, add ease,
           then apply the garment's drape rules (bloused chest, cinched obi, straight or A-line skirt)
  TRUNK    a (row, column) grid over that profile from the hem to the neckline; rows above the V bottom lose
           the V at the front; the top row follows the neckline (higher at the back of the neck)
  PARTS    collar bands on the V edges (left over right), obi band + knot, sleeves as tubes along the arm
           (pouch below the arm, partly closed cuff), skin patches ('personality') where the body shows
  WEIGHTS  trunk above the crotch: closest-point transfer from the vanilla torso/legs, smoothed; skirt below the
           crotch: the vanilla coat rule (sides follow their thigh, centre split between both, pelvis share
           falling with depth - read from raincoat_m / labcoat_m / nursedress_f); sleeves: along the arm chain
           by the projection on the arm axis; skin: transferred from the vanilla arm / torso
Everything is in the bind pose; faces use the MLOD winding (outward = -cross, see geom.py).
"""
import numpy as np

from garment import Garment
from geom import (Surface, convex_hull_2d, polar_profile, slice_points, smoothstep, tris, unit, face_normals)
from wlib import body, load_ref
import anm_pose

ARM_BONES = ("arm", "armroll", "forearm", "forearmroll", "hand", "armextra", "elbowextra", "forearmextra",
             "wristextra")

# texture atlas (2048 x 2048), (u0, v0, u1, v1)
A_TRUNK = (0.00, 0.00, 1.00, 0.56)
A_SLEEVE = {"left": (0.00, 0.56, 0.50, 0.80), "right": (0.50, 0.56, 1.00, 0.80)}
A_COLLAR = (0.00, 0.80, 1.00, 0.86)
A_OBI = (0.00, 0.86, 0.80, 0.92)
A_KNOT = (0.80, 0.86, 1.00, 0.92)
A_LINING = (0.00, 0.92, 0.70, 1.00)
A_CUFF = (0.70, 0.92, 1.00, 1.00)

LANDMARKS = {
    # neck_top: the vanilla torso's top; v: bottom of the V; obi band; crotch; neckline heights
    "m": {"v": 1.305, "obi": (1.000, 1.105), "crotch": 0.875, "n_side": 1.525, "n_back": 1.530, "theta_n": 38.0},
    "f": {"v": 1.290, "obi": (1.075, 1.185), "crotch": 0.870, "n_side": 1.500, "n_back": 1.500, "theta_n": 38.0},
}
HEM = {"short": 0.720, "long": 0.085}
POUCH_DOWN = 0.45
EASE_CHEST = 0.026
EASE_SKIRT = 0.030
EASE_NECK = 0.010


def reg(r, s, t):
    u0, v0, u1, v1 = r
    return (u0 + (u1 - u0) * float(s), v0 + (v1 - v0) * float(t))


def is_arm(ws):
    return sum(w for b, w in ws if any(b == side + a for side in ("left", "right") for a in ARM_BONES)) >= 0.5


class Profile:
    """R(phi, y) around centre (0, zc(y)); phi = 0 at the front (-Z), +90 = the wearer's left (+X)"""

    def __init__(self, sex, hem, length):
        B = body(sex)
        T, L = B["torso3"], B["legs3"]
        self.sex = sex
        lm = LANDMARKS[sex]
        Tt = tris(T.F)
        armv = np.array([is_arm(ws) for ws in T.W])
        Tt = np.array([t for t in Tt if not armv[t].any()])
        Lt = tris(L.F)
        self.top = float(T.P[:, 1].max())
        self.ys = np.round(np.arange(hem - 0.02, self.top + 0.015, 0.01), 4)
        self.phis = np.radians(np.arange(0, 360, 5.0))
        zc, rb = [], []
        last = None
        for y in self.ys:
            pts = np.concatenate([slice_points(T.P, Tt, y), slice_points(L.P, Lt, y)])
            if len(pts) < 6:
                pts = last
            last = pts
            h = convex_hull_2d(pts[:, [0, 2]])
            zc.append((h[:, 1].min() + h[:, 1].max()) / 2)
            rb.append(h)
        zc = np.array(zc)
        # smooth the centre line
        k = np.ones(9) / 9
        zcs = np.convolve(np.pad(zc, 4, mode="edge"), k, mode="valid")
        self.zc = zcs
        Rb = np.array([polar_profile(h, (0.0, z), self.phis) for h, z in zip(rb, zcs)])
        self.Rbody = Rb
        # ---- drape rules
        y = self.ys[:, None]
        obi0, obi1 = lm["obi"]
        chest = lm["v"] + 0.02
        ease = np.where(y > chest, EASE_CHEST, EASE_SKIRT) * np.ones_like(Rb)
        ease = np.where(y > self.top - 0.06, EASE_NECK + (EASE_CHEST - EASE_NECK) * np.clip((self.top - y) / 0.06, 0, 1), ease)
        R = Rb + ease
        i_chest = np.argmin(np.abs(self.ys - chest))
        i_o1 = np.argmin(np.abs(self.ys - obi1))
        i_o0 = np.argmin(np.abs(self.ys - obi0))
        i_cr = np.argmin(np.abs(self.ys - lm["crotch"]))
        # obi band: snug
        R[i_o0:i_o1 + 1] = Rb[i_o0:i_o1 + 1] + 0.012
        # blouse between the obi and the chest: hangs from the chest
        for i in range(i_o1 + 1, i_chest):
            t = (self.ys[i_chest] - self.ys[i]) / (self.ys[i_chest] - self.ys[i_o1])
            hang = R[i_chest] * (1 - t) + (R[i_o1] + 0.012) * t
            R[i] = np.maximum(R[i], hang * (1 - 0.15 * t) + R[i] * 0.15 * t)
        # skirt below the obi: the hip profile (max from the crotch up to the obi) with a gentle A-line
        Rhip = (Rb[i_cr:i_o0] + EASE_SKIRT).max(axis=0)
        flare = 0.10 if length == "long" else 0.04
        for i in range(0, i_o0):
            d = self.ys[i_o0] - self.ys[i]
            # hang from the obi edge to the full hip width over the first 9 cm below the obi
            k = smoothstep(0.0, 0.09, d)
            target = (Rb[i_o0] + 0.012) * (1 - k) + Rhip * (1 + flare * d) * k
            R[i] = np.maximum(R[i] * k + target * (1 - k), target)
            if length == "long" and self.ys[i] < lm["crotch"]:
                # below the crotch the long robe is a column: do not follow the separate legs
                R[i] = np.maximum(Rhip * (1 + flare * d), R[i] * 0.0)
        # vertical smoothing except across the obi edges
        Rs = R.copy()
        for i in range(len(self.ys)):
            if abs(i - i_o0) <= 1 or abs(i - i_o1) <= 1:
                continue
            lo, hi = max(0, i - 2), min(len(self.ys), i + 3)
            if lo <= i_o1 < hi or lo <= i_o0 < hi:
                continue
            Rs[i] = R[lo:hi].mean(axis=0)
        self.R = Rs
        self.i_o0, self.i_o1 = i_o0, i_o1

    def point(self, phi, y, extra=0.0):
        """3D point on the profile surface; phi in radians, any y (clamped)"""
        yi = np.clip((y - self.ys[0]) / 0.01, 0, len(self.ys) - 1.001)
        i0 = int(np.floor(yi))
        ty = yi - i0
        ph = (phi % (2 * np.pi)) / np.radians(5.0)
        j0 = int(np.floor(ph)) % len(self.phis)
        j1 = (j0 + 1) % len(self.phis)
        tp = ph - np.floor(ph)
        r = ((1 - ty) * ((1 - tp) * self.R[i0, j0] + tp * self.R[i0, j1]) +
             ty * ((1 - tp) * self.R[i0 + 1, j0] + tp * self.R[i0 + 1, j1]))
        zc = (1 - ty) * self.zc[i0] + ty * self.zc[i0 + 1]
        r = r + extra
        return np.array([r * np.sin(phi), y, zc - r * np.cos(phi)])


def sleeve_section(top, half, depth, n):
    """closed 2D contour (x = across, y = pouch direction) of a flat kimono sleeve: round over the arm
    (radius `top`, `half` wide at the arm), flat sides tapering to a 2.4 cm thick rounded pouch bottom.
    Resampled to n points by arc length, starting at the top, running +x first."""
    tb = 0.012
    arc = [(half * np.cos(a), -top * np.sin(a)) for a in np.linspace(np.pi, 0, 16)]   # -half -> +half over the top
    side_r = [(half + (tb - half) * t, depth * t) for t in np.linspace(0, 1, 12)[1:]]
    bot = [(tb * np.cos(a), depth + tb * np.sin(a)) for a in np.linspace(0, np.pi, 8)[1:-1]]
    side_l = [(-(half + (tb - half) * t), depth * t) for t in np.linspace(1, 0, 12)[:-1]]
    poly = np.array(arc + side_r + bot + side_l)
    seg = np.linalg.norm(np.diff(np.vstack([poly, poly[:1]]), axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    target = np.linspace(0, cum[-1], n, endpoint=False)
    out = []
    closed = np.vstack([poly, poly[:1]])
    for t in target:
        i = int(np.searchsorted(cum, t, side="right") - 1)
        f = (t - cum[i]) / max(seg[i], 1e-9)
        out.append(closed[i] + (closed[i + 1] - closed[i]) * f)
    return out


def neckline_y(lm, c):
    """collar line height along the column parameter c in [0, 1] (0 = left V corner, 0.5 = back, 1 = right)"""
    return lm["n_side"] + (lm["n_back"] - lm["n_side"]) * np.sin(np.pi * c) ** 2


def build(sex, length="short", lod=0):
    lm = LANDMARKS[sex]
    hem = HEM[length]
    prof = Profile(sex, hem, length)
    g = Garment("kimono_%s_%s" % (length, sex))
    ncol = (48, 32, 20)[lod]
    th_n = np.radians(lm["theta_n"])
    y_v = lm["v"]
    # ---------------------------------------------------------------- trunk rows
    n_low = {"short": (18, 12, 7), "long": (34, 22, 12)}[length][lod]
    n_up = (9, 6, 4)[lod]
    obi0, obi1 = lm["obi"]
    # lower rows: dense around the obi edges and the hem
    lows = np.unique(np.concatenate([np.linspace(hem, y_v, n_low), [obi0 - 0.005, obi0 + 0.005, obi1 - 0.005, obi1 + 0.005]]))
    lows = lows[lows < y_v - 0.004]
    rows_t = np.linspace(0, 1, n_up + 1)          # 0 = V bottom, 1 = neckline
    grid = []
    uvg = []
    y_top_front = lm["n_side"]
    total_h = lm["n_back"] - hem

    def uv_trunk(c, y):
        return reg(A_TRUNK, c, (lm["n_back"] + 0.01 - y) / (total_h + 0.02))
    for y in lows:
        row = [prof.point(2 * np.pi * c, y) for c in np.linspace(0, 1, ncol + 1)]
        grid.append(row)
        uvg.append([uv_trunk(c, y) for c in np.linspace(0, 1, ncol + 1)])
    for t in rows_t:
        yb = y_v + (y_top_front - y_v) * t
        th = th_n * t
        row, uvr = [], []
        for c in np.linspace(0, 1, ncol + 1):
            phi = th + c * (2 * np.pi - 2 * th)
            y = yb + (neckline_y(lm, c) - y_top_front) * t ** 2
            row.append(prof.point(phi, y))
            uvr.append(uv_trunk(phi / (2 * np.pi), y))
        grid.append(row)
        uvg.append(uvr)
    grid = np.array(grid)
    R = len(grid)
    # the lower rows are closed rings: the last column duplicates the first (UV seam at the front centre,
    # hidden under the overlap flap); the V rows are open. Build faces by hand to weld the ring seam.
    base = g.add_points(grid.reshape(-1, 3))
    C = ncol + 1
    idx = lambda r, c: base + r * C + c  # noqa: E731
    n_closed = len(lows)
    for r in range(R - 1):
        for c in range(ncol):
            v = [idx(r, c), idx(r, c + 1), idx(r + 1, c + 1), idx(r + 1, c)]
            uv = [uvg[r][c], uvg[r][c + 1], uvg[r + 1][c + 1], uvg[r + 1][c]]
            g.add_face(v, uv, "trunk")
    # weld the ring seam of the closed rows (column ncol -> column 0) so normals are continuous
    seam = {idx(r, ncol): idx(r, 0) for r in range(n_closed)}
    g.F = [[seam.get(v, v) for v in f] for f in g.F]
    trunk_rows = (base, R, C, n_closed)
    # ---------------------------------------------------------------- collar bands
    collar_w = 0.048
    nb = g.arrays()

    def surf_point(phi, y, extra):
        return prof.point(phi, y, extra)

    def collar_path(side):
        """list of (phi, y) along one collar: back centre -> neck side -> V edge -> V bottom (-> left crosses
        on to the obi on the wearer's right)"""
        pts = []
        sgn = 1 if side == "left" else -1
        for c in np.linspace(0.5, 0.0, 10):          # back centre -> left V corner (mirrored for right)
            phi = th_n + c * (2 * np.pi - 2 * th_n)
            if sgn < 0:
                phi = 2 * np.pi - phi
            pts.append((phi, neckline_y(lm, c)))
        for t in np.linspace(1, 0, 8)[1:]:           # down the V edge
            pts.append((sgn * th_n * t % (2 * np.pi), y_v + (y_top_front - y_v) * t))
        if side == "left":                           # outer panel: across to the wearer's right, under the obi
            end_phi = -np.radians(42)
            for t in np.linspace(0, 1, 7)[1:]:
                pts.append(((end_phi * t) % (2 * np.pi), y_v + (obi1 - 0.02 - y_v) * t))
        return pts

    def band(path, side, lift, mat, uv_fn, width):
        """a band laid on the profile surface along path, extending into the panel (away from the V)"""
        P = np.array([surf_point(ph, y, 0.0) for ph, y in path])
        n = len(P)
        rows = []
        for i in range(n):
            a, b = P[max(i - 1, 0)], P[min(i + 1, n - 1)]
            tg = unit(b - a)
            ph, y = path[i]
            outward = unit(surf_point(ph, y, 0.01) - P[i])
            side_dir = unit(np.cross(outward, tg))
            # the band extends away from the V opening = toward the back / outward of the panel
            if (side == "left" and side_dir[0] < 0 and y > y_v) or (side == "right" and side_dir[0] > 0 and y > y_v):
                side_dir = -side_dir
            if y <= y_v and side == "left":
                # below the V the band lies on the right panel, pointing down/right
                if side_dir[1] > 0:
                    side_dir = -side_dir
            o0 = P[i] + outward * (lift * 0.4)
            o1 = P[i] + outward * lift
            o2 = P[i] + side_dir * width + outward * lift
            o3 = P[i] + side_dir * width + outward * (lift * 0.4)
            rows.append([o0, o1, o2, o3])
        rows = np.array(rows)
        b0 = g.add_points(rows.reshape(-1, 3))
        for i in range(n - 1):
            seg = []
            for k in range(4):          # edge, top, edge, underside: a closed band (never see-through)
                k1 = (k + 1) % 4
                v = [b0 + i * 4 + k, b0 + i * 4 + k1, b0 + (i + 1) * 4 + k1, b0 + (i + 1) * 4 + k]
                uv = [uv_fn(i, k), uv_fn(i, k1), uv_fn(i + 1, k1), uv_fn(i + 1, k)]
                g.add_face(v, uv, mat)
                seg.append(len(g.F) - 1)
            top = g.F[seg[1]]
            Pa = g.arrays()
            fn = face_normals(Pa, np.array([top[:3]]))[0]
            c = Pa[top].mean(0)
            yy = float(np.clip(c[1], prof.ys[0], prof.ys[-1]))
            zc = np.interp(yy, prof.ys, prof.zc)
            radial = unit(np.array([c[0], 0.0, c[2] - zc]))
            if np.dot(fn, radial) < 0:
                for fi in seg:
                    g.F[fi] = g.F[fi][::-1]
                    g.FUV[fi] = g.FUV[fi][::-1]
        # end caps (orientation: facing away from the band's middle)
        mid = rows[n // 2].mean(0)
        for i in (0, n - 1):
            f0 = len(g.F)
            g.add_face([b0 + i * 4 + k for k in range(4)], [uv_fn(i, k) for k in range(4)], mat)
            g.orient([f0], lambda c, mid=mid: c - mid)
        return b0, n

    def collar_uv(offset, total):
        def f(i, k):
            return reg(A_COLLAR, (offset + i) / total, [0.0, 0.15, 0.85, 1.0][k])
        return f
    lp = collar_path("left")
    rp = collar_path("right")
    tot = len(lp) + len(rp)
    band(rp, "right", 0.005, "collar", collar_uv(len(lp), tot), collar_w)
    band(lp, "left", 0.008, "collar", collar_uv(0, tot), collar_w)
    # overlap flap below the obi: the outer panel's front edge down to the hem, on the wearer's right
    flap_phi = -np.radians(42) % (2 * np.pi)
    fp = [(flap_phi, y) for y in np.linspace(obi0 + 0.01, hem, 8 if length == "short" else 16)]
    band(fp, "left", 0.004, "collar", lambda i, k: reg(A_COLLAR, 0.98 - 0.02 * k / 3, 0.5 + 0.0 * i), 0.018)
    # ---------------------------------------------------------------- obi + knot
    ob_rows = []
    obs = np.linspace(obi0, obi1, 4)
    for y in obs:
        extra = 0.010 + (0.004 if y in (obs[1], obs[2]) else 0.0)
        ob_rows.append([prof.point(2 * np.pi * c, y, extra) for c in np.linspace(0, 1, ncol + 1)])
    ob_rows = np.array(ob_rows)
    # tuck the edges into the kimono
    ob_rows[0] = [prof.point(2 * np.pi * c, obi0 - 0.004, 0.002) for c in np.linspace(0, 1, ncol + 1)]
    ob_rows[-1] = [prof.point(2 * np.pi * c, obi1 + 0.004, 0.002) for c in np.linspace(0, 1, ncol + 1)]
    ob_uv = [[reg(A_OBI, c, 1 - r / 3.0) for c in np.linspace(0, 1, ncol + 1)] for r in range(4)]
    g.add_grid(ob_rows, ob_uv, "obi", closed=False)
    # knot: a flat pillow on the back (kai-no-kuchi), 20 x 9 x 4 cm
    kc = prof.point(np.pi, (obi0 + obi1) / 2, 0.024)
    kx, ky, kz = 0.10, 0.045, 0.022
    corners = np.array([[sx * kx, sy * ky, sz * kz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]) + kc
    corners[:, 2] += np.where(corners[:, 2] > kc[2], 0.0, 0.0)
    kb = g.add_points(corners)
    quads = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    k0 = len(g.F)
    for q in quads:
        g.add_face([kb + i for i in q], [reg(A_KNOT, s, t) for s, t in ((0, 0), (1, 0), (1, 1), (0, 1))], "obi")
    g.orient(range(k0, len(g.F)), lambda c: c - kc)
    # ---------------------------------------------------------------- sleeves
    rig = anm_pose.Rig(anm_pose.XOB_M if sex == "m" else anm_pose.XOB_F)
    sleeves = {}
    for side, sgn in (("left", 1), ("right", -1)):
        S = side.capitalize()
        J_arm, J_fore, J_hand = rig.joint(S + "Arm"), rig.joint(S + "ForeArm"), rig.joint(S + "Hand")
        a = unit(J_hand - J_arm)
        down = np.array([0, -1.0, 0]) - np.dot([0, -1.0, 0], a) * a
        back = np.array([0, 0, 1.0]) - np.dot([0, 0, 1.0], a) * a
        # pouch direction: mostly BEHIND the arm, a little down. LBS carries it rigidly with the arm, so this
        # is chosen for the common poses: arms down (idle, run) -> hangs behind the forearm; arms forward
        # (weapon raised) -> the back direction turns into "down" and the sleeve hangs under the arm
        e_down = unit(unit(back) + POUCH_DOWN * unit(down))
        e_side = unit(np.cross(a, e_down)) * sgn
        s0 = J_arm - a * 0.015          # the open root end sits inside the trunk shell
        s1 = J_hand - a * 0.085
        L = np.linalg.norm(s1 - s0)
        nrow = (10, 7, 4)[lod]
        nsec = (20, 16, 12)[lod]
        rows, uvs_ = [], []
        ts = np.linspace(0, 1, nrow)
        for ti, t in enumerate(ts):
            ctr = s0 + (s1 - s0) * t
            depth = 0.10 + 0.13 * smoothstep(0.0, 0.45, t)          # pouch depth below the arm axis
            depth *= 1.0 - 0.10 * smoothstep(0.85, 1.0, t)          # rounded bottom corner at the cuff
            top = 0.064 + 0.012 * (1 - t) + 0.012 * float(np.exp(-((t - 0.55) / 0.2) ** 2))   # elbow room
            half = 0.080 + 0.010 * (1 - t)
            ring = [ctr + e_side * px + e_down * py for px, py in sleeve_section(top, half, depth, nsec)]
            rows.append(ring)
        rows = np.array(rows)
        # orientation: sections run k up -> ... decide by checking one face below
        sb = g.add_points(rows.reshape(-1, 3))
        A = A_SLEEVE[side]
        f_first = len(g.F)
        for r in range(nrow - 1):
            for k in range(nsec):
                k1 = (k + 1) % nsec
                v = [sb + r * nsec + k, sb + (r + 1) * nsec + k, sb + (r + 1) * nsec + k1, sb + r * nsec + k1]
                uv = [reg(A, k / nsec, ts[r]), reg(A, k / nsec, ts[r + 1]), reg(A, (k + 1) / nsec, ts[r + 1]), reg(A, (k + 1) / nsec, ts[r])]
                g.add_face(v, uv, "sleeve_" + side)
        # cuff cap with the hand opening (sode-guchi) around the arm axis
        last = rows[-1]
        ctr = s1
        open_r = (0.068, 0.062)
        hole = np.array([ctr + e_side * open_r[0] * np.cos(2 * np.pi * k / nsec) + e_down * (0.012 + open_r[1] * np.sin(2 * np.pi * k / nsec)) for k in range(nsec)])
        hb = g.add_points(hole)
        lb = sb + (nrow - 1) * nsec
        for k in range(nsec):
            k1 = (k + 1) % nsec
            v = [lb + k, hb + k, hb + k1, lb + k1]
            uv = [reg(A_CUFF, k / nsec, 0), reg(A_CUFF, k / nsec, 1), reg(A_CUFF, (k + 1) / nsec, 1), reg(A_CUFF, (k + 1) / nsec, 0)]
            g.add_face(v, uv, "cuff_" + side)
        f_cuff = len(g.F) - nsec
        # root cap: closes the open end inside the trunk (faces toward the body)
        rc = g.add_points(np.array([s0 + e_down * 0.05]))
        f_root = len(g.F)
        for k in range(nsec):
            k1 = (k + 1) % nsec
            g.add_face([sb + k, rc, sb + k1], [reg(A_CUFF, 0.5, 0.5)] * 3, "cuff_" + side)
        g.orient(range(f_root, len(g.F)), lambda c, a=a: -a)
        axis_c = s0 + (s1 - s0) * 0.5 + e_down * 0.06

        def radial_out(c, s0=s0, a=a, e_down=e_down):
            base_pt = s0 + a * np.dot(c - s0, a) + e_down * 0.06
            return c - base_pt
        g.orient(range(f_first, f_cuff), radial_out)
        g.orient(range(f_cuff, f_root), lambda c, a=a: a)
        sleeves[side] = {"a": a, "s0": s0, "s1": s1, "base": sb, "n": nrow * nsec, "hole": (hb, nsec),
                         "J": (J_arm, J_fore, J_hand), "e_down": e_down, "e_side": e_side}
    g.meta = {"prof": prof, "sleeves": sleeves, "trunk": trunk_rows, "lm": lm, "hem": hem, "length": length,
              "sex": sex, "lod": lod}
    return g


if __name__ == "__main__":
    for sex in "mf":
        for length in ("short", "long"):
            g = build(sex, length)
            print(g.stats())
