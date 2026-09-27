"""JP_Kasa: conical woven-sedge traveller's hat (sugegasa). Rigid, 100 % on the Head bone.

Fitted against the head + hair envelope of ALL 31 vanilla heads (data/W/heads_bodyspace.npz; the older heads
are stored 0.907 m low in their p3d and are shifted up by their neck bottom, see REPORT.md):
  - the cone's underside clears every head's hair by >= CLEAR (f_judy's top bun is the one exception, logged)
  - an inner head ring (atama-wa) of elliptical section sits on the crown, inside which every head fits
Male and female heads share the skeleton and the same envelope, so _m and _f are the same mesh (vanilla does
the same for its CowboyHat: ClothingTypes male = female = CowboyHat.p3d).
"""
import os

import numpy as np

from garment import Garment
from wlib import DATA

R = 0.245          # rim radius (a 49 cm hat)
H = 0.150          # cone height (outer apex to rim plane): ~31 deg slope
T = 0.008          # straw thickness
ZC = 0.004         # hat axis z (heads are centred slightly behind z = 0)
CLEAR = 0.006
RING = (0.093, 0.114, 1.752)   # inner ring semi-axes x, z and bottom y
EXCLUDE = ()                    # f_judy's hair bun (1.837 m) is the tallest; the fit includes it

# texture regions (u0, v0, u1, v1) in the 1024 x 1024 kasa atlas
DISC = (0.0, 0.0, 1.0, 1.0)
BIND = (0.02, 0.02, 0.10, 0.10)     # dark binding at the rim (corner swatch)
RINGTX = (0.90, 0.02, 0.98, 0.10)   # the inner ring (bamboo / cloth)
KNOB = (0.02, 0.90, 0.10, 0.98)


def fit_apex():
    heads = np.load(os.path.join(DATA, "heads_bodyspace.npz"))
    need = {}
    for n in heads.files:
        P = heads[n]
        q = P[P[:, 1] > 1.6]
        r = np.hypot(q[:, 0], q[:, 2] - ZC)
        inside = r < R
        # underside at radius r: y_a_inner - (H / R) * r  where y_a_inner = y_apex_outer - T / cos
        need[n] = float((q[inside, 1] + (H / R) * r[inside]).max() + CLEAR)
    ok = {k: v for k, v in need.items() if k not in EXCLUDE}
    return max(ok.values()), need


def swatch(reg, s, t):
    u0, v0, u1, v1 = reg
    return (u0 + (u1 - u0) * s, v0 + (v1 - v0) * t)


def disc_uv(x, z):
    return (0.5 + 0.49 * x / R, 0.5 + 0.49 * (z - ZC) / R)


def build(segs=48, rings=10, ring_segs=None, knob=True):
    apex_inner, need = fit_apex()
    slope = H / R
    thick_y = T * np.sqrt(1 + slope * slope)   # vertical offset between the two cone surfaces
    y_apex = apex_inner + thick_y              # outer apex
    g = Garment("kasa")
    th = np.linspace(0, 2 * np.pi, segs, endpoint=False)
    # radii: denser near the rim (more silhouette there)
    rr = R * (1 - (1 - np.linspace(0, 1, rings + 1)[1:]) ** 1.3)

    def ring_pts(r, y):
        return np.stack([r * np.sin(th), np.full(segs, y), ZC - r * np.cos(th)], 1)

    # ---- outer cone: apex point + rings. Seen from above/outside, theta increasing (front -> +X) runs to
    # the viewer's right when looking down the slope from outside... handled by explicit orientation below
    apex = g.add_points([[0, y_apex, ZC]])
    rows = [g.add_points(ring_pts(r, y_apex - slope * r)) for r in rr]

    def uvp(i):
        p = g.P[i]
        return disc_uv(p[0], p[2])

    def quad(a, b, c, d, mat, uvf=uvp):
        g.add_face([a, b, c, d], [uvf(a), uvf(b), uvf(c), uvf(d)], mat)

    def tri(a, b, c, mat, uvf=uvp):
        g.add_face([a, b, c], [uvf(a), uvf(b), uvf(c)], mat)

    for k in range(segs):
        k1 = (k + 1) % segs
        tri(apex, rows[0] + k, rows[0] + k1, "straw")
    for j in range(len(rows) - 1):
        for k in range(segs):
            k1 = (k + 1) % segs
            quad(rows[j] + k, rows[j + 1] + k, rows[j + 1] + k1, rows[j] + k1, "straw")
    # ---- inner cone (underside), same radii, pushed down by the thickness, reversed winding
    iapex = g.add_points([[0, apex_inner, ZC]])
    irows = [g.add_points(ring_pts(r, apex_inner - slope * r)) for r in rr]
    for k in range(segs):
        k1 = (k + 1) % segs
        tri(iapex, irows[0] + k1, irows[0] + k, "straw")
    for j in range(len(irows) - 1):
        for k in range(segs):
            k1 = (k + 1) % segs
            quad(irows[j] + k, irows[j] + k1, irows[j + 1] + k1, irows[j + 1] + k, "straw")
    # ---- rim binding: a rolled edge joining outer and inner rims (bulges out by 3 mm)
    r_out = rows[-1]
    r_in = irows[-1]
    rim_mid = g.add_points(ring_pts(R + 0.004, y_apex - slope * R - thick_y * 0.5))

    def bind_uv(i):
        p = g.P[i]
        a = (np.arctan2(p[0], -(p[2] - ZC)) / (2 * np.pi)) % 1.0
        return swatch(BIND, a, 0.5)
    for k in range(segs):
        k1 = (k + 1) % segs
        quad(r_out + k, rim_mid + k, rim_mid + k1, r_out + k1, "straw", bind_uv)
        quad(rim_mid + k, r_in + k, r_in + k1, rim_mid + k1, "straw", bind_uv)
    # ---- inner head ring (atama-wa): elliptical band, outer + inner wall + bottom lip
    rs = ring_segs or segs
    ax, az, yb = RING
    tt = np.linspace(0, 2 * np.pi, rs, endpoint=False)
    y_top = apex_inner - slope * np.hypot(ax, az) * 0.5 - slope * 0.5 * np.hypot(ax, az) + 0.004  # tucked into the cone

    def ell(a, b, y):
        return np.stack([a * np.sin(tt), np.full(rs, y), ZC - b * np.cos(tt)], 1)
    w = 0.006
    top_o = g.add_points(ell(ax + w, az + w, y_top))
    bot_o = g.add_points(ell(ax + w, az + w, yb))
    bot_i = g.add_points(ell(ax, az, yb))
    top_i = g.add_points(ell(ax, az, y_top))

    def ring_uv(i):
        p = g.P[i]
        a = (np.arctan2(p[0], -(p[2] - ZC)) / (2 * np.pi)) % 1.0
        return swatch(RINGTX, a, (p[1] - yb) / max(1e-6, y_top - yb))
    for k in range(rs):
        k1 = (k + 1) % rs
        quad(bot_o + k, bot_o + k1, top_o + k1, top_o + k, "straw", ring_uv)     # outer wall (faces out)
        quad(top_i + k, top_i + k1, bot_i + k1, bot_i + k, "straw", ring_uv)     # inner wall (faces the head)
        quad(bot_i + k, bot_i + k1, bot_o + k1, bot_o + k, "straw", ring_uv)     # bottom lip (faces down)
    # ---- knob (tsumami) on the apex
    if knob:
        ks = 10
        kt = np.linspace(0, 2 * np.pi, ks, endpoint=False)
        kr = 0.013
        base_y = y_apex - slope * kr

        def kring(r, y):
            return np.stack([r * np.sin(kt), np.full(ks, y), ZC - r * np.cos(kt)], 1)
        k0 = g.add_points(kring(kr, base_y - 0.002))
        k1_ = g.add_points(kring(kr * 0.9, y_apex + 0.018))
        ktop = g.add_points([[0, y_apex + 0.024, ZC]])

        def knob_uv(i):
            p = g.P[i]
            a = (np.arctan2(p[0], -(p[2] - ZC)) / (2 * np.pi)) % 1.0
            return swatch(KNOB, a, (p[1] - base_y) / 0.03)
        for k in range(ks):
            kk = (k + 1) % ks
            quad(k0 + k, k0 + kk, k1_ + kk, k1_ + k, "straw", knob_uv)
            tri(ktop, k1_ + k, k1_ + kk, "straw", knob_uv)
    g.set_weights([{"head": 1.0} for _ in g.P])
    g.meta = {"apex_inner": apex_inner, "y_apex": y_apex, "rim_y": y_apex - H, "need": need}
    return g


if __name__ == "__main__":
    g = build()
    print(g.stats())
    print("apex outer %.3f, rim %.3f" % (g.meta["y_apex"], g.meta["rim_y"]))
    for k, v in sorted(g.meta["need"].items(), key=lambda kv: -kv[1])[:6]:
        print("  needs apex_inner >= %.3f : %s" % (v, k))
