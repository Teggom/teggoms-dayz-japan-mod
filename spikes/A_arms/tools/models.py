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
# v2 (2026-09-27): every dimension comes from spikes/A_arms/katana_v2/katana_spec.json through katana_geom.py.
# The grip frame is unchanged: tsuka along +Y through x = z = 0, point +Y, edge +Z, machi at the vanilla guard base.
import katana_geom as kg  # noqa: E402

TEXK = {"blade": D + "jp_katana_blade_co.paa", "tsuka": D + "jp_katana_tsuka_co.paa", "fit": D + "jp_katana_fittings_co.paa"}
_KG = []


def katana_geom():
    if not _KG:
        _KG.append(kg.KatanaGeom())
    return _KG[0]


def _seg(g, key, detail, lo):
    return max(lo, int(round(kg.V(g.spec["build"][key]) * detail)))


def _ellipse_loft(m, ys, rx_fn, rz_fn, zc_fn, n, rect, mat, v_fn=None):
    rings = [mk.ellipse_ring((0.0, y, zc_fn(y)), (1, 0, 0), (0, 0, 1), rx_fn(y), rz_fn(y), n) for y in ys]
    uq = [qmap(rect, j / n, 0)[0] for j in range(n + 1)]
    vq = [qmap(rect, 0, v_fn(y) if v_fn else k / (len(ys) - 1))[1] for k, y in enumerate(ys)]
    m.loft(rings, uq, vq, TEXK["fit"], mat, outward_ref=[(0.0, y, zc_fn(y)) for y in ys[:-1]])
    return rings


def _planar_cap(m, ring, centre, normal, rect, r_uv, mat):
    """cap a ring with UVs projected from X/Z into rect (r_uv = radius that maps to the rect edge)"""
    cx, cz = centre[0], centre[2]
    uvs = [qmap(rect, 0.5 + 0.5 * (p[0] - cx) / r_uv, 0.5 + 0.5 * (p[2] - cz) / r_uv) for p in ring]
    m.cap(ring, centre, normal, qmap(rect, 0.5, 0.5), uvs, TEXK["fit"], mat)


def build_katana(detail=1.0):
    g = katana_geom()
    A = kg.ATLAS
    m = Mesh()
    # ---------------------------------------------------------------- blade: body (machi -> yokote) + kissaki (yokote -> point)
    nb = _seg(g, "blade_body_segments", detail, 10)
    nk = _seg(g, "kissaki_segments", detail, 8)

    def rings_for(stations):
        rings, U, vs = [], [], []
        for s in stations:
            pts, us = g.section(s)
            rings.append([tuple(g.to_model(s, d, x)) for d, x in pts])
            U.append(list(us) + [us[0]])
            vs.append(1.0 - s / g.L_arc)
        return rings, U, vs
    body = rings_for(g.body_stations(nb))
    inside_b = [g.to_model(s, 0.5 * g.width(s), 0.0) for s in g.body_stations(nb)[:-1]]
    m.loft(body[0], body[1], body[2], TEXK["blade"], MAT["steel"], closed=True, hard=True, outward_ref=inside_b, sel=["blade"])
    kst = g.kissaki_stations(nk)
    kis = rings_for(kst)
    inside_k = [g.to_model(s, 0.5 * g.width(s), 0.0) for s in kst[:-1]]
    m.loft(kis[0], kis[1], kis[2], TEXK["blade"], MAT["steel"], closed=True, hard=True, outward_ref=inside_k, sel=["blade"])
    # base cap (inside the habaki)
    c0 = g.to_model(0.0, 0.5 * g.motohaba, 0.0)
    m.cap(body[0][0], tuple(c0), (0, -1, 0), (0.5, 1.0), [(u, 1.0) for u in body[1][0][:-1]], TEXK["blade"], MAT["steel"])
    # ---------------------------------------------------------------- habaki: gold-foiled sleeve around the blade base
    hw = g.habaki_wall

    def habaki_ring(s, shrink):
        pts, _ = g.section(s)
        w = g.width(s)
        out = []
        for d, x in pts[:5]:                         # mune top -> hira (+X side)
            out.append((d - (hw - shrink) * (1 - d / w), x + (hw - shrink)))
        out += [(w + hw - shrink, 0.6 * (hw - shrink)), (w + hw - shrink, -0.6 * (hw - shrink))]
        for d, x in pts[6:]:                         # hira -> mune top (-X side)
            out.append((d - (hw - shrink) * (1 - d / w), x - (hw - shrink)))
        return [tuple(g.to_model(s, d, x)) for d, x in out]
    sd = g.spec["build"]["shape_details"]
    cb, cs = [0.01 * v for v in kg.V(sd["habaki_front_chamfer_cm"])]
    hs = [(0.0, 0.0), (g.habaki_len - cb, 0.0), (g.habaki_len, cs)]
    hr = [habaki_ring(s, sh) for s, sh in hs]
    nh = len(hr[0])
    uq = [qmap(A["gold"], j / nh, 0)[0] for j in range(nh + 1)]
    m.loft(hr, uq, [qmap(A["gold"], 0, t)[1] for t in (0.0, 0.9, 1.0)], TEXK["fit"], MAT["brass"],
           outward_ref=[tuple(g.to_model(s, 0.5 * g.width(s), 0.0)) for s, _ in hs[:-1]])
    for ring, s, nrm in ((hr[-1], g.habaki_len, g.tangent(g.habaki_len)), (hr[0], 0.0, -g.tangent(0.0))):
        _planar_cap(m, ring, tuple(g.to_model(s, 0.5 * g.width(s), 0.0)), tuple(nrm), A["gold"], 0.03, MAT["brass"])
    # ---------------------------------------------------------------- seppa (copper), tsuba (round iron)
    rx_f = 0.5 * g.tsuka_width * g.fuchi_flare
    rz_f = 0.5 * g.tsuka_depth * g.fuchi_flare
    ns = _seg(g, "tsuka_segments_round", detail, 10)
    for y0, y1 in (g.y_seppa_a, g.y_seppa_b):
        rs = _ellipse_loft(m, [y0, y1], lambda y: rx_f + g.seppa_margin, lambda y: rz_f + g.seppa_margin, lambda y: 0.0, ns, A["copper"], MAT["brass"])
        _planar_cap(m, rs[0], (0.0, y0, 0.0), (0, -1, 0), A["copper"], rz_f + g.seppa_margin, MAT["brass"])
        _planar_cap(m, rs[1], (0.0, y1, 0.0), (0, 1, 0), A["copper"], rz_f + g.seppa_margin, MAT["brass"])
    nt = _seg(g, "tsuba_segments_round", detail, 16)
    r, rr = g.tsuba_r, g.tsuba_round
    ty0, ty1 = g.y_tsuba
    prof = [(ty0, r - rr), (ty0 + rr, r), (ty1 - rr, r), (ty1, r - rr)]   # kaku-mimi, slightly rounded
    rings = [mk.ellipse_ring((0.0, y, 0.0), (1, 0, 0), (0, 0, 1), rad, rad, nt) for y, rad in prof]
    uq = [qmap(A["iron"], j / nt, 0)[0] for j in range(nt + 1)]
    m.loft(rings, uq, [qmap(A["iron"], 0, t)[1] for t in (0.40, 0.45, 0.55, 0.60)], TEXK["fit"], MAT["iron"],
           outward_ref=[(0.0, y, 0.0) for y, _ in prof[:-1]])
    _planar_cap(m, rings[0], (0.0, ty0, 0.0), (0, -1, 0), A["iron"], r, MAT["iron"])
    _planar_cap(m, rings[-1], (0.0, ty1, 0.0), (0, 1, 0), A["iron"], r, MAT["iron"])
    # ---------------------------------------------------------------- fuchi (shakudo, low, angled sides)
    lip = 0.01 * kg.V(sd["fuchi_lip_cm"])
    fy0, fy1 = g.y_fuchi
    rs = _ellipse_loft(m, [fy1, fy0], lambda y: (0.5 * g.tsuka_width + lip) * (g.fuchi_flare if y == fy1 else 1.0),
                       lambda y: (0.5 * g.tsuka_depth + lip) * (g.fuchi_flare if y == fy1 else 1.0), g.tsuka_offset_z, ns,
                       A["shakudo"], MAT["iron"])
    _planar_cap(m, rs[0], (0.0, fy1, 0.0), (0, 1, 0), A["shakudo"], rz_f + lip, MAT["iron"])
    # ---------------------------------------------------------------- tsuka: leather hineri-maki over same (texture), ryugo
    wy0, wy1 = g.y_wrap
    nring = _seg(g, "tsuka_rings", detail, 6)
    ys = [wy1 + (wy0 - wy1) * k / nring for k in range(nring + 1)]
    rings = [mk.ellipse_ring((0.0, y, g.tsuka_offset_z(y)), (1, 0, 0), (0, 0, 1), 0.5 * g.tsuka_width * g.tsuka_scale(y),
                             0.5 * g.tsuka_depth * g.tsuka_scale(y), ns) for y in ys]
    m.loft(rings, [j / ns for j in range(ns + 1)], [(wy1 - y) / (wy1 - wy0) for y in ys], TEXK["tsuka"], MAT["silk"],
           outward_ref=[(0.0, y, g.tsuka_offset_z(y)) for y in ys[:-1]], sel=["tsuka"])
    # ---------------------------------------------------------------- kashira: black lacquered horn, wrap over the top (texture)
    ky0, ky1 = g.y_kashira
    ks = g.kashira_scale
    kprof = [(ky1 - f * g.kashira_len, sc) for f, sc in kg.V(sd["kashira_profile"])]
    rings = [mk.ellipse_ring((0.0, y, g.tsuka_offset_z(y)), (1, 0, 0), (0, 0, 1), 0.5 * g.tsuka_width * ks * f,
                             0.5 * g.tsuka_depth * ks * f, ns) for y, f in kprof]
    uq = [qmap(A["horn_side"], j / ns, 0)[0] for j in range(ns + 1)]
    m.loft(rings, uq, [qmap(A["horn_side"], 0, t)[1] for t in (0.0, 0.5, 0.85, 1.0)], TEXK["fit"], MAT["iron"],
           outward_ref=[(0.0, y, g.tsuka_offset_z(y)) for y, _ in kprof[:-1]])
    _planar_cap(m, rings[-1], (0.0, ky0 - 0.0006, g.tsuka_offset_z(ky0)), (0, -1, 0), A["horn_cap"],
                0.5 * g.tsuka_depth * ks * kprof[-1][1], MAT["iron"])
    return m


def katana_memory(m):
    g = katana_geom()
    lo, hi = m.bounds()
    tip = g.tip()
    mp = kg.V(g.spec["build"]["memory_points_kept"])
    return {
        "boundingbox_min": [tuple(lo)], "boundingbox_max": [tuple(hi)],
        "invview": [tuple(mp["invview"])],
        "meleerangestart": [tuple(mp["meleerangestart"])], "meleerangeend": [tuple(tip + np.array(mp["meleerangeend_offset"]))],
        "ce_center": [(0.0, (lo[1] + hi[1]) / 2, 0.0)], "ce_radius": [tuple(hi)],
        "throwingimpulseposition": [tuple(mp["throwingimpulseposition"])],
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
