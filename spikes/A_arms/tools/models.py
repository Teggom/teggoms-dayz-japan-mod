"""Procedural katana, yari, yumi (two frames) and ya, in the vanilla parents' grip frames.

Grip frames (measured by tools/vanilla_frames.py + the finger-curl circumcentres, see REPORT.md):
  Sword  (medieval_sword.anm): handle along +Y through x=0,z=0; right hand centre y=+0.085, left y=0.00;
         vanilla guard y 0.125-0.167; the wrists sit on -Z, so the cutting edge (ha) faces +Z.
  Spear  (advanced_spear.anm): shaft along +Y through x=0.01,z=0; right hand y=+0.276, left y=-0.077.
  Recurve bow (bow_erc_recurve_IK.anm + bow clips, no hand IK): forward = -X, up = +Y, right = +Z;
         left hand (bow hand) grip centre (-0.037, 0.000, -0.049), right hand (-> string) (0.132, 0.056, -0.048).
  Crossbow (crossbow.anm): forward = -X, up = +Y, right = +Z; left hand (-0.21, 0.035, 0.01), right (0.06, 0.046, 0.0).
  Projectiles (bolt_biggame, arrow_composite): tip at the origin, shaft along +Z.
"""
import math

import numpy as np

import meshkit as mk
from meshkit import Mesh, v3, unit

D = "JP\\weapons\\data\\"
TEX = {
    "blade": D + "jp_blade_co.paa", "tsuka": D + "jp_tsuka_co.paa", "fit": D + "jp_fittings_co.paa",
    "lacquer": D + "jp_lacquer_co.paa", "yumi": D + "jp_yumi_co.paa", "ya": D + "jp_ya_co.paa",
}
MAT = {k: D + "jp_%s.rvmat" % k for k in ("steel", "iron", "brass", "silk", "lacquer", "bow", "hemp", "bamboo", "feather")}
# fittings atlas quadrants (u0, u1, v0, v1)
Q_IRON, Q_BRASS, Q_HEMP, Q_HORN = (0.02, 0.48, 0.02, 0.48), (0.52, 0.98, 0.02, 0.48), (0.02, 0.48, 0.52, 0.98), (0.52, 0.98, 0.52, 0.98)


def qmap(q, u, v):
    return q[0] + (q[1] - q[0]) * u, q[2] + (q[3] - q[2]) * v


def tube(m, axis_pts, radii, n, tex, mat, uq=None, vq=None, ax_x=(1, 0, 0), ax_z=(0, 0, 1), sel=None, scale2=None):
    """loft circles (or ellipses: radii (rx, rz) pairs) around a polyline running along +Y-ish"""
    rings = []
    for k, c in enumerate(axis_pts):
        r = radii[k]
        rx, rz = (r, r) if not isinstance(r, tuple) else r
        rings.append(mk.ellipse_ring(c, ax_x, ax_z, rx, rz, n))
    us = [k / n for k in range(n + 1)]
    L = [0.0]
    for a, b in zip(axis_pts, axis_pts[1:]):
        L.append(L[-1] + float(np.linalg.norm(v3(b) - v3(a))))
    vs = [l / L[-1] if L[-1] else 0.0 for l in L]
    if uq is not None:
        us = [uq[0] + (uq[1] - uq[0]) * u for u in us]
    if vq is not None:
        vs = [vq[0] + (vq[1] - vq[0]) * v for v in vs]
    return m.loft(rings, us, vs, tex, mat, closed=True, outward_ref=axis_pts[:-1], sel=sel)


# =========================================================================== katana
K = dict(y_kashira=-0.118, y_tsuka0=-0.108, y_fuchi=0.110, y_tsuba0=0.117, y_tsuba1=0.124, y_habaki=0.154,
         L=0.745, sori=0.017, W0=0.031, Wk=0.0225, T0=0.0072, Tk=0.0052, k=0.035)


def katana_blade_frame(s):
    """mune point M(s) and unit normal n(s) (towards the edge) in the (y, z) plane"""
    R = K["L"] ** 2 / (8 * K["sori"])
    th = s / R
    y = K["y_tsuba1"] + R * math.sin(th)
    z = -K["W0"] / 2 - R * (1 - math.cos(th))
    return np.array([0.0, y, z]), np.array([0.0, math.sin(th), math.cos(th)])


def build_katana(detail=1.0):
    m = Mesh()
    L, k = K["L"], K["k"]
    nseg = int(60 * detail)
    ss = [L * (i / nseg) for i in range(nseg + 1)]
    # extra samples inside the kissaki
    ks = [L - k + k * (i / int(10 * detail)) for i in range(1, int(10 * detail))]
    ss = sorted(set([round(s, 6) for s in ss + ks if s < L * 0.9995]))
    rings = []
    vs = []
    for s in ss:
        M, n = katana_blade_frame(s)
        xdir = np.array([1.0, 0, 0])
        if s <= L - k:
            f = s / (L - k)
            w = K["W0"] + (K["Wk"] - K["W0"]) * f
            T = K["T0"] + (K["Tk"] - K["T0"]) * f
            dm, de = 0.0, w
        else:
            t = (s - (L - k)) / k
            w0 = K["Wk"]
            dm = 0.25 * w0 * t ** 2
            de = 0.25 * w0 + 0.75 * w0 * math.sqrt(max(0.0, 1 - t ** 2))
            T = K["Tk"] * (1 - 0.85 * t)
        ww = de - dm
        prof = [(dm, 0.0), (dm + 0.06 * ww, 0.42 * T), (dm + 0.30 * ww, 0.5 * T), (de, 0.0),
                (dm + 0.30 * ww, -0.5 * T), (dm + 0.06 * ww, -0.42 * T)]
        rings.append([tuple(M + d * n + x * xdir) for d, x in prof])
        vs.append(1.0 - s / L)
    us = [0.0, 0.06, 0.30, 1.0, 0.30, 0.06, 0.0]
    inside = []
    for s in ss[:-1]:
        M, n = katana_blade_frame(s)
        inside.append(M + 0.3 * K["Wk"] * n)
    m.loft(rings, us, vs, TEX["blade"], MAT["steel"], closed=True, hard=True, outward_ref=inside, sel=["blade"])
    # tip: fan the last ring into the point
    Mt, nt = katana_blade_frame(L)
    tip = tuple(Mt + 0.25 * K["Wk"] * nt)
    last = rings[-1]
    m.cap(last, tip, v3(katana_blade_frame(L)[0]) - v3(katana_blade_frame(L - 0.01)[0]), (0.25, 0.0),
          [(u, 0.0) for u in us[:-1]], TEX["blade"], MAT["steel"])
    # base cap of the blade (hidden inside the habaki)
    M0, n0 = katana_blade_frame(0)
    m.cap(rings[0], tuple(M0 + 0.3 * K["W0"] * n0), (0, -1, 0), (0.3, 1.0), [(u, 1.0) for u in us[:-1]], TEX["blade"], MAT["steel"])
    # habaki: sleeve around the blade base
    hr = []
    for y in (K["y_tsuba1"], K["y_habaki"] - 0.004, K["y_habaki"]):
        s = y - K["y_tsuba1"]
        M, n = katana_blade_frame(s)
        c = M + (K["W0"] / 2) * n
        shrink = 0.0 if y < K["y_habaki"] - 0.001 else 0.0015
        hr.append((c, K["W0"] / 2 + 0.0022 - shrink, K["T0"] / 2 + 0.0024 - shrink))
    rings = [mk.ellipse_ring(c, (1, 0, 0), (0, 0, 1), b, a, int(12 * detail) or 8) for c, a, b in hr]
    n_h = len(rings[0])
    uq = [qmap(Q_BRASS, j / n_h, 0)[0] for j in range(n_h + 1)]
    m.loft(rings, uq, [qmap(Q_BRASS, 0, t)[1] for t in (0, 0.8, 1.0)], TEX["fit"], MAT["brass"], outward_ref=[r[0] for r in hr[:-1]])
    m.cap(rings[-1], tuple(hr[-1][0]), (0, 1, 0), qmap(Q_BRASS, 0.5, 0.5), [qmap(Q_BRASS, 0.5 + 0.4 * math.cos(2 * math.pi * j / n_h), 0.5) for j in range(n_h)], TEX["fit"], MAT["brass"])
    # tsuba: mokko (four lobes) disc in the XZ plane
    nt_ = int(40 * detail) or 16

    def mokko(y, grow=0.0):
        pts = []
        for j in range(nt_):
            a = 2 * math.pi * j / nt_
            r = 0.0365 + 0.0020 * math.cos(4 * a) + grow
            pts.append((0.94 * r * math.cos(a), y, r * math.sin(a) + 0.002))
        return pts
    tr = [mokko(K["y_tsuba0"]), mokko(K["y_tsuba0"] + 0.0012, 0.0006), mokko(K["y_tsuba1"] - 0.0012, 0.0006), mokko(K["y_tsuba1"])]
    uq = [qmap(Q_IRON, j / nt_, 0)[0] for j in range(nt_ + 1)]
    m.loft(tr, uq, [qmap(Q_IRON, 0, t)[1] for t in (0, 0.1, 0.9, 1.0)], TEX["fit"], MAT["iron"],
           outward_ref=[(0, K["y_tsuba0"], 0.002)] * 3)
    for ring, y, nrm in ((tr[0], K["y_tsuba0"], (0, -1, 0)), (tr[-1], K["y_tsuba1"], (0, 1, 0))):
        uvs = [qmap(Q_IRON, 0.5 + 0.5 * p[0] / 0.04, 0.5 + 0.5 * (p[2] - 0.002) / 0.04) for p in ring]
        m.cap(ring, (0, y, 0.002), nrm, qmap(Q_IRON, 0.5, 0.5), uvs, TEX["fit"], MAT["iron"])
    # tsuka (oval, long axis along Z = edge direction), slight hourglass, silk wrap texture
    ntk = int(20 * detail) or 10
    ys = np.linspace(K["y_tsuka0"], K["y_fuchi"], int(14 * detail) or 6)
    mid = (K["y_tsuka0"] + K["y_fuchi"]) / 2
    axis = [(0, y, 0) for y in ys]
    half = (K["y_fuchi"] - K["y_tsuka0"]) / 2
    radii = []
    for y in ys:
        waist = 1 - 0.06 * (1 - abs(y - mid) / half) ** 1.5    # slightly narrower in the middle
        radii.append((0.0122 * waist, 0.0160 * waist))
    rings = [mk.ellipse_ring(c, (1, 0, 0), (0, 0, 1), rx, rz, ntk) for c, (rx, rz) in zip(axis, radii)]
    m.loft(rings, [j / ntk for j in range(ntk + 1)], [(K["y_fuchi"] - y) / (K["y_fuchi"] - K["y_tsuka0"]) for y in ys],
           TEX["tsuka"], MAT["silk"], outward_ref=axis[:-1])
    # fuchi (collar) and kashira (pommel cap), iron
    for y0, y1, grow, dome in ((K["y_fuchi"], K["y_tsuba0"], 0.0012, False), (K["y_kashira"], K["y_tsuka0"], 0.0012, True)):
        rs = [mk.ellipse_ring((0, y, 0), (1, 0, 0), (0, 0, 1), 0.0122 + grow, 0.0160 + grow, ntk) for y in (y0, y1)]
        uq = [qmap(Q_IRON, j / ntk, 0)[0] for j in range(ntk + 1)]
        m.loft(rs, uq, [qmap(Q_IRON, 0, 0.2)[1], qmap(Q_IRON, 0, 0.8)[1]], TEX["fit"], MAT["iron"], outward_ref=[(0, y0, 0)])
        if dome:
            inner = mk.ellipse_ring((0, y0 - 0.0035, 0), (1, 0, 0), (0, 0, 1), (0.0122 + grow) * 0.75, (0.0160 + grow) * 0.75, ntk)
            m.loft([inner, rs[0]], uq, [qmap(Q_IRON, 0, 0.05)[1], qmap(Q_IRON, 0, 0.2)[1]], TEX["fit"], MAT["iron"],
                   outward_ref=[(0, y0 + 0.004, 0)])
            m.cap(inner, (0, y0 - 0.0045, 0), (0, -1, 0), qmap(Q_IRON, 0.5, 0.5),
                  [qmap(Q_IRON, 0.5 + 0.4 * math.cos(2 * math.pi * j / ntk), 0.5 + 0.4 * math.sin(2 * math.pi * j / ntk)) for j in range(ntk)],
                  TEX["fit"], MAT["iron"])
    return m


def katana_memory(m):
    lo, hi = m.bounds()
    tip, _ = katana_blade_frame(K["L"])
    return {
        "boundingbox_min": [tuple(lo)], "boundingbox_max": [tuple(hi)],
        "invview": [(0.82, 0.36, 0.0)],
        "meleerangestart": [(0.0, 0.05, 0.0)], "meleerangeend": [tuple(tip + np.array([0, 0, 0.004]))],
        "ce_center": [(0.0, (lo[1] + hi[1]) / 2, 0.0)], "ce_radius": [tuple(hi)],
        "throwingimpulseposition": [(0.0, 0.142, 0.0)],
    }


# =========================================================================== yari
Y = dict(ax=0.01, y_butt=-0.400, y_ishi=-0.365, y_shaft1=1.115, y_collar=1.150, y_tip=1.400, r=0.0145)


def build_yari(detail=1.0):
    m = Mesh()
    ax = Y["ax"]
    n = int(16 * detail) or 8
    # shaft, black lacquer
    ys = np.linspace(Y["y_ishi"], Y["y_shaft1"], int(12 * detail) or 4)
    axis = [(ax, y, 0) for y in ys]
    tube(m, axis, [Y["r"]] * len(ys), n, TEX["lacquer"], MAT["lacquer"],
         vq=(1.0, 0.0))
    # ishizuki (iron butt cap): rounded end
    ys2 = [Y["y_ishi"] + 0.001, Y["y_butt"] + 0.008, Y["y_butt"] + 0.002]
    rr = [Y["r"] + 0.0012, Y["r"] + 0.0012, Y["r"] * 0.7]
    rings = [mk.ellipse_ring((ax, y, 0), (1, 0, 0), (0, 0, 1), r, r, n) for y, r in zip(ys2, rr)]
    uq = [qmap(Q_IRON, j / n, 0)[0] for j in range(n + 1)]
    m.loft(rings[::-1], uq, [qmap(Q_IRON, 0, t)[1] for t in (0.9, 0.2, 0.0)], TEX["fit"], MAT["iron"],
           outward_ref=[(ax, y, 0) for y in ys2[::-1][:-1]])
    m.cap(rings[-1], (ax, Y["y_butt"], 0), (0, -1, 0), qmap(Q_IRON, 0.5, 0.5),
          [qmap(Q_IRON, 0.5 + 0.4 * math.cos(2 * math.pi * j / n), 0.5 + 0.4 * math.sin(2 * math.pi * j / n)) for j in range(n)],
          TEX["fit"], MAT["iron"])
    # collar (sakawa), brass, tapering into the blade neck
    ys3 = [Y["y_shaft1"] - 0.004, Y["y_shaft1"] + 0.012, Y["y_collar"] - 0.006, Y["y_collar"]]
    rr3 = [Y["r"] + 0.0012, Y["r"] + 0.0016, 0.0105, 0.0085]
    rings = [mk.ellipse_ring((ax, y, 0), (1, 0, 0), (0, 0, 1), r, r, n) for y, r in zip(ys3, rr3)]
    uq = [qmap(Q_BRASS, j / n, 0)[0] for j in range(n + 1)]
    m.loft(rings, uq, [qmap(Q_BRASS, 0, t)[1] for t in (0.0, 0.3, 0.8, 1.0)], TEX["fit"], MAT["brass"],
           outward_ref=[(ax, y, 0) for y in ys3[:-1]])
    m.cap(rings[-1], (ax, Y["y_collar"], 0), (0, 1, 0), qmap(Q_BRASS, 0.5, 0.5),
          [qmap(Q_BRASS, 0.5 + 0.4 * math.cos(2 * math.pi * j / n), 0.5) for j in range(n)], TEX["fit"], MAT["brass"])
    # blade: su-yari, diamond (ryo-shinogi) section, width along X, ridges on +-Z
    L = Y["y_tip"] - Y["y_collar"]
    nb = int(24 * detail) or 8
    rings, vs, inside = [], [], []
    for i in range(nb):
        t = i / nb
        y = Y["y_collar"] + L * t
        if t < 0.15:
            w = 0.015 + (0.032 - 0.015) * math.sin(0.5 * math.pi * t / 0.15)
        else:
            w = 0.032 * ((1 - t) / 0.85) ** 0.8
        T = 0.0100 * (1 - 0.7 * t)
        rings.append([(ax + w / 2, y, 0), (ax, y, T / 2), (ax - w / 2, y, 0), (ax, y, -T / 2)])
        vs.append(1.0 - (0.06 + 0.94 * t))
        inside.append((ax, y, 0))
    us = [1.0, 0.3, 1.0, 0.3, 1.0]
    m.loft(rings, us, vs, TEX["blade"], MAT["steel"], closed=True, hard=True, outward_ref=inside[:-1], sel=["blade"])
    m.cap(rings[-1], (ax, Y["y_tip"], 0), (0, 1, 0), (0.65, 0.0), [(u, 0.0) for u in us[:-1]], TEX["blade"], MAT["steel"])
    return m


def yari_memory(m):
    lo, hi = m.bounds()
    return {
        "boundingbox_min": [tuple(lo)], "boundingbox_max": [tuple(hi)],
        "invview": [(0.55, 0.50, -1.05)],
        "meleerangestart": [(Y["ax"], -0.30, 0.0)], "meleerangeend": [(Y["ax"], Y["y_tip"] - 0.01, 0.0)],
        "ce_center": [(Y["ax"], (lo[1] + hi[1]) / 2, 0.0)], "ce_radius": [tuple(hi)],
    }


# =========================================================================== ya
A = dict(tip=-0.032, head1=0.012, socket=0.020, shaft1=0.930, nock=0.955, r=0.0045, f0=0.735, f1=0.885)


def build_ya(detail=1.0):
    m = Mesh()
    n = int(8 * detail) or 6
    total = A["nock"] - A["tip"]

    def vtex(z):
        return (z - A["tip"]) / total
    # head: diamond (flat along X), iron
    zs = [A["tip"] + 0.0005, -0.018, -0.006, 0.004, A["head1"]]
    ws = [0.0006, 0.0105, 0.0135, 0.008, 0.0042]
    ts = [0.0004, 0.0028, 0.0034, 0.0030, 0.0042]
    rings = [[(w, 0, z), (0, t, z), (-w, 0, z), (0, -t, z)] for z, w, t in zip(zs, ws, ts)]
    m.loft(rings, [qmap(Q_IRON, u, 0)[0] for u in (0, 0.25, 0.5, 0.75, 1.0)], [qmap(Q_IRON, 0, (z - A["tip"]) / 0.05)[1] for z in zs],
           TEX["fit"], MAT["iron"], hard=True, outward_ref=[(0, 0, z) for z in zs[:-1]])
    m.cap(rings[0], (0, 0, A["tip"]), (0, 0, -1), qmap(Q_IRON, 0.5, 0.0), [qmap(Q_IRON, u, 0.0) for u in (0, 0.25, 0.5, 0.75)], TEX["fit"], MAT["iron"])
    # socket + shaft + nock, one tube each
    ax = (1, 0, 0), (0, 1, 0)
    sock = [mk.ellipse_ring((0, 0, z), ax[0], ax[1], r, r, n) for z, r in ((A["head1"] - 0.001, 0.0042), (A["socket"], 0.0050))]
    m.loft(sock, [qmap(Q_IRON, j / n, 0)[0] for j in range(n + 1)], [qmap(Q_IRON, 0, 0.3)[1], qmap(Q_IRON, 0, 0.5)[1]],
           TEX["fit"], MAT["iron"], outward_ref=[(0, 0, A["head1"])])
    zs = list(np.linspace(A["socket"] - 0.001, A["shaft1"], int(10 * detail) or 3))
    rings = [mk.ellipse_ring((0, 0, z), ax[0], ax[1], A["r"], A["r"], n) for z in zs]
    m.loft(rings, [0.5 * j / n for j in range(n + 1)], [vtex(z) for z in zs], TEX["ya"], MAT["bamboo"], outward_ref=[(0, 0, z) for z in zs[:-1]])
    nk = [mk.ellipse_ring((0, 0, z), ax[0], ax[1], r, r, n) for z, r in ((A["shaft1"] - 0.001, 0.0049), (A["nock"] - 0.004, 0.0046), (A["nock"], 0.0036))]
    m.loft(nk, [qmap(Q_HORN, j / n, 0)[0] for j in range(n + 1)], [qmap(Q_HORN, 0, t)[1] for t in (0, 0.7, 1.0)], TEX["fit"], MAT["iron"],
           outward_ref=[(0, 0, A["shaft1"]), (0, 0, A["nock"] - 0.004)])
    m.cap(nk[-1], (0, 0, A["nock"] - 0.0015), (0, 0, 1), qmap(Q_HORN, 0.5, 0.5), [qmap(Q_HORN, 0.5, 0.5)] * n, TEX["fit"], MAT["iron"])
    # three feathers (hane), double-sided vanes
    L = A["f1"] - A["f0"]
    nsteps = int(6 * detail) or 3
    for ang in (90, 210, 330):
        a = math.radians(ang)
        rd = np.array([math.cos(a), math.sin(a), 0.0])
        prev = None
        for i in range(nsteps + 1):
            t = i / nsteps
            z = A["f0"] + L * t
            h = 0.0135 * min(1.0, t / 0.25) ** 0.7 * (1 - 0.35 * max(0.0, (t - 0.6) / 0.4))
            root = v3((0, 0, z)) + rd * (A["r"] * 0.9)
            tipp = root + rd * max(h, 0.0008)
            cur = (root, tipp, t)
            if prev is not None:
                (r0, t0, v0), (r1, t1, v1) = prev, cur
                m.quad2(tuple(r0), tuple(r1), tuple(t1), tuple(t0),
                        [(0.5, v0), (0.5, v1), (0.99, v1), (0.99, v0)], TEX["ya"], MAT["feather"])
            prev = cur
    return m


def ya_memory(m):
    lo, hi = m.bounds()
    return {
        "boundingbox_min": [tuple(lo)], "boundingbox_max": [tuple(hi)],
        "invview": [(-0.45, 0.0, 0.46)],
        "ce_center": [(0.0, 0.0, (lo[2] + hi[2]) / 2)], "ce_radius": [tuple(hi)],
    }


# =========================================================================== yumi
YU = dict(length=2.2, below=0.733, grip_half=0.055, brace=0.150)


def build_yumi(G, draw_to=None, detail=1.0, arrow_side=+1):
    """G = bow-hand grip centre (x, y, z); the bow lies in the plane z = G.z, belly towards +X,
    forward (arrow flight) = -X. draw_to = None: braced string at G.x + 0.016 + brace;
    else the nock point the string is drawn back to (V string)."""
    m = Mesh()
    gx, gy, gz = G
    top, bot = gy + YU["length"] - YU["below"], gy - YU["below"]
    xs = gx + 0.016 + YU["brace"]
    tip_x = xs - 0.009 + (0.025 if draw_to is not None else 0.0)
    ntot = int(110 * detail) or 30
    n = int(8 * detail) or 6

    def cx(y):
        if y >= gy:
            u = (y - gy) / (top - gy)
        else:
            u = (gy - y) / (gy - bot)
        f = min(1.0, (u / 0.95)) ** 2.4
        reflex = 0.016 * max(0.0, (u - 0.95) / 0.05) ** 1.6
        return gx + (tip_x - gx) * f - reflex, u

    ys = list(np.linspace(bot, top, ntot))
    for extra in (gy - YU["grip_half"], gy + YU["grip_half"], gy - YU["grip_half"] - 0.004, gy + YU["grip_half"] + 0.004):
        ys.append(extra)
    ys = sorted(set(round(y, 5) for y in ys))
    rings, vs, inside, cs = [], [], [], []
    for y in ys:
        x, u = cx(y)
        cs.append((x, y, gz))
    for i, (x, y, z) in enumerate(cs):
        a = cs[max(0, i - 1)]
        b = cs[min(len(cs) - 1, i + 1)]
        tng = unit(v3(b) - v3(a))
        ez = np.array([0.0, 0.0, 1.0])
        et = unit(np.cross(tng, ez))           # thickness direction in the XY plane
        _, u = cx(y)
        in_grip = abs(y - gy) <= YU["grip_half"] + 1e-6
        if in_grip:
            tx, tz = 0.0165, 0.0150
        else:
            tx = 0.0105 - 0.0045 * u
            tz = 0.0135 - 0.0055 * u
        # rounded rectangle: 8 points
        ring = []
        for k in range(n):
            ang = 2 * math.pi * (k + 0.5) / n
            ca, sa = math.cos(ang), math.sin(ang)
            px = tx * np.sign(ca) * abs(ca) ** 0.6
            pz = tz * np.sign(sa) * abs(sa) ** 0.6
            ring.append(tuple(v3((x, y, z)) + px * et + pz * ez))
        rings.append(ring)
        vs.append((top - y) / YU["length"])
        inside.append((x, y, z))
    m.loft(rings, [k / n for k in range(n + 1)], vs, TEX["yumi"], MAT["bow"], outward_ref=inside[:-1], sel=["body"])
    # tip caps (horn nocks)
    for ring, (x, y, z), sgn in ((rings[0], cs[0], -1), (rings[-1], cs[-1], +1)):
        m.cap(ring, (x - 0.004, y + sgn * 0.02, z), (0, sgn, 0), qmap(Q_HORN, 0.5, 0.5),
              [qmap(Q_HORN, 0.5 + 0.4 * math.cos(2 * math.pi * k / n), 0.5) for k in range(n)], TEX["fit"], MAT["iron"])
    # string (tsuru), hemp
    def contact(y):
        x, _ = cx(y)
        return np.array([x + 0.008, y, gz])
    pt_top = contact(top - 0.035)
    pt_bot = contact(bot + 0.035)
    ns = 6
    segs = [(pt_top, pt_bot)] if draw_to is None else [(pt_top, v3(draw_to)), (v3(draw_to), pt_bot)]
    for a, b in segs:
        d = unit(b - a)
        e1 = unit(np.cross(d, (0, 0, 1)))
        e2 = np.cross(d, e1)
        ringsS = [mk.ellipse_ring(p, e1, e2, 0.0022, 0.0022, ns) for p in (a, b)]
        m.loft(ringsS, [qmap(Q_HEMP, k / ns, 0)[0] for k in range(ns + 1)], [qmap(Q_HEMP, 0, 0)[1], qmap(Q_HEMP, 0, 1)[1]],
               TEX["fit"], MAT["hemp"], outward_ref=[tuple(a)], sel=["string"])
    string_x = xs if draw_to is None else draw_to[0]
    return m, {"top": top, "bot": bot, "xs": xs, "string_x": string_x, "tip_x": tip_x, "gz": gz}


def nocked_ya(nock, direction=(-1, 0, 0), detail=1.0):
    """a ya mesh placed with its nock end at `nock`, flying along `direction`"""
    ya = build_ya(detail)
    z_img = -unit(direction)                    # ya +Z (tip -> nock) points backwards
    y_img = np.array([0.0, 1.0, 0.0])
    y_img = unit(y_img - z_img * np.dot(y_img, z_img))
    x_img = np.cross(y_img, z_img)
    R = mk.rot_cols(x_img, y_img, z_img)
    t = v3(nock) - R @ v3((0, 0, A["nock"]))
    return ya, (R, t)


def yumi_bow_variant(detail=1.0):
    """JP_Yumi: RecurveBow in-hands profile (bow locomotion set). Grip = left hand centre in that frame."""
    G = (-0.037, 0.000, -0.049)
    m, info = build_yumi(G, None, detail)
    y_arrow = G[1] + YU["grip_half"] + 0.008
    z_arrow = G[2] + 0.015 + 0.0045
    nock = (info["xs"], y_arrow, z_arrow)
    ya, xf = nocked_ya(nock, (-1, 0, 0), detail)
    m.merge(ya, xf, sel="bullet")
    eye = (nock[0] + 0.149, nock[1] + 0.046, nock[2] - 0.032)
    return m, info, {"hlavne": nock, "eye": eye}


def yumi_xb_variant(detail=1.0):
    """JP_Yumi_XB: Crossbow_Base in-hands profile. Bow hand = left hand on the crossbow's fore-stock;
    the string is drawn back to the right hand."""
    G = (-0.210, 0.035, 0.010)
    y_arrow = G[1] + YU["grip_half"] + 0.008
    z_arrow = G[2] + 0.015 + 0.0045
    nock = (0.068, y_arrow, z_arrow)
    m, info = build_yumi(G, (nock[0] + 0.004, nock[1], G[2]), detail)
    ya, xf = nocked_ya(nock, (-1, 0, 0), detail)
    m.merge(ya, xf, sel="bullet")
    return m, info, {"hlavne": nock, "eye": (0.282, 0.164, 0.0)}


def yumi_memory(m, info, extra):
    lo, hi = m.bounds()
    h = extra["hlavne"]
    return {
        "eye": [extra["eye"]],
        "hlavne": [h],
        "string_axis": [(h[0] - 0.2, h[1], h[2]), (h[0] + 0.8, h[1], h[2])],
        "boundingbox_min": [tuple(lo)], "boundingbox_max": [tuple(hi)],
        "invview": [((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, -1.45)],
        "ce_center": [tuple((lo + hi) / 2)], "ce_radius": [tuple(hi)],
    }
