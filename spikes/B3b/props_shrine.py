"""W2 shrine stones (BUILD_LIST items 24, 11, 25; agent W2, 2026-09-30): stone lanterns (Kasuga 1.8 / 2.4 / 3.0,
square, small placed, joyato; mossy variants per Stephen), the purification basin (chozubachi) and the stone steps
(modules with a continuous Roadway ramp, C7 <= 38 deg). Era: research/outdoor_kit/W2_ERA.md (L1-L4, B1, S1).

Frame: origin = base centre on the terrain, +z = front (the approach; lantern windows face +-z, text on the front).
Steps: origin = the foot of the flight (front nosing line, centre) on the terrain; the flight climbs towards -z; the
sidecar connectors stair_foot (0, 0, 0) and stair_head (0, rise, -run) chain flights and landings.
"""
import math
import random

import skit
from skit import (core, box, prism, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, beam, add_all,
                  leaves, litter, moss_top, moss_face, CARVED, CUT, FIELD, RIVER, BAMBOO, WOOD, MOSS, LEAF, CTEXT)
from props_wood import M
import w2kit as K
from w2kit import X, Y, Z

HEX = 0.0                 # lathe phase for a hexagon with flat faces on +-z (vertex angles 0, 60, ...)
SQ = math.pi / 4          # square with flat faces on +-x / +-z
OCT = math.pi / 8         # octagon with a flat face on +z


def lt(profile, n, ph, mat=CARVED, vis=(1,), wear=None, smooth=False):
    s = lathe(profile, n, mat, vis=vis, phase=ph, smooth=smooth)
    if wear:
        s.wear = wear
    return s


def moss_cap(profile, n, ph, wear="_w2", off=0.006, vis=(1,)):
    """Moss as a skin a few mm outside part of a lathe profile (roof slopes, platform tops): the alpha-cut decal
    texture makes it patchy."""
    pr = []
    for i, (r, y) in enumerate(profile):
        a = profile[max(0, i - 1)]
        b = profile[min(len(profile) - 1, i + 1)]
        dr, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dr, dy) or 1.0
        pr.append((r + dy / L * off, y - dr / L * off))
    s = lathe(pr, n, MOSS, vis=vis, phase=ph, smooth=False)
    s.wear = wear
    return s


def firebox_panels(R, y0, y1, th, n, ph, windows, mat=CARVED, vis=(1,), wear=None):
    """Side panels of a lantern fire box (n-gon of circumradius R, faces k = between vertex k and k+1); faces whose
    centre direction is in `windows` (angles, deg) stay open (the fire windows)."""
    out = []
    for k in range(n):
        a0, a1 = ph + 2 * math.pi * k / n, ph + 2 * math.pi * (k + 1) / n
        am = math.degrees((a0 + a1) / 2) % 360
        if any(abs(am - w) < 1.0 for w in windows):
            continue
        Ri = R - th / math.cos(math.pi / n)
        c = [(R * math.cos(a0), y0, R * math.sin(a0)), (R * math.cos(a1), y0, R * math.sin(a1)),
             (Ri * math.cos(a1), y0, Ri * math.sin(a1)), (Ri * math.cos(a0), y0, Ri * math.sin(a0))]
        c += [(p[0], y1, p[2]) for p in c]
        s = core.hexa(c, mat, vis=vis)
        if wear:
            s.wear = wear
        out.append(s)
    return out


# ================================================================================================ stone lantern
def lantern_parts(kind, T):
    """[(name, profile, n, phase)] bottom up, plus the fire box (y0, y1, R, n, phase) and key heights."""
    if kind == "kasuga":
        f = {"kiso": 0.05, "sao": 0.36, "chudai": 0.10, "hibukuro": 0.17, "kasa": 0.13, "hoju": 0.20}
        y = [0.0]
        for k in ("kiso", "sao", "chudai", "hibukuro", "kasa", "hoju"):
            y.append(y[-1] + f[k] * T / 1.01)
        kiso = [(0.0, -0.06), (0.17 * T, -0.06), (0.17 * T, y[1] * 0.55), (0.12 * T, y[1]), (0.0, y[1])]
        sr = 0.048 * T
        sao = [(0.0, y[1] - 0.01), (sr * 1.15, y[1] - 0.01), (sr, y[1] + 0.03 * T), (sr, (y[1] + y[2]) / 2 - 0.015 * T),
               (sr * 1.22, (y[1] + y[2]) / 2), (sr, (y[1] + y[2]) / 2 + 0.015 * T), (sr, y[2] - 0.02 * T),
               (sr * 1.1, y[2]), (0.0, y[2])]
        if T <= 1.85:            # small-prop budget (300): no flare at the shaft ends
            sao = [(0.0, y[1]), (sr, y[1]), (sr, (y[1] + y[2]) / 2 - 0.015 * T), (sr * 1.22, (y[1] + y[2]) / 2),
                   (sr, (y[1] + y[2]) / 2 + 0.015 * T), (sr, y[2]), (0.0, y[2])]
        chu = [(0.0, y[2]), (0.075 * T, y[2]), (0.09 * T, y[2] + 0.03 * T), (0.15 * T, y[3] - 0.025 * T),
               (0.15 * T, y[3]), (0.0, y[3])]
        fb = (y[3], y[4], 0.105 * T, 6, HEX)
        kasa = [(0.0, y[4]), (0.19 * T, y[4]), (0.215 * T, y[4] + 0.025 * T), (0.15 * T, y[4] + 0.06 * T),
                (0.075 * T, y[4] + 0.10 * T), (0.05 * T, y[5]), (0.0, y[5])]
        hoju = [(0.0, y[5]), (0.045 * T, y[5]), (0.065 * T, y[5] + 0.05 * T), (0.04 * T, y[5] + 0.07 * T),
                (0.06 * T, y[5] + 0.11 * T), (0.045 * T, y[5] + 0.16 * T), (0.0, y[6])]
        return [("kiso", kiso, 6, HEX), ("sao", sao, 8, OCT), ("chudai", chu, 6, HEX), ("kasa", kasa, 6, HEX),
                ("hoju", hoju, 8 if T > 1.85 else 6, OCT if T > 1.85 else HEX)], fb, y
    if kind == "square":
        f = {"kiso": 0.07, "sao": 0.36, "chudai": 0.09, "hibukuro": 0.17, "kasa": 0.13, "hoju": 0.18}
        y = [0.0]
        for k in ("kiso", "sao", "chudai", "hibukuro", "kasa", "hoju"):
            y.append(y[-1] + f[k] * T)
        q = math.sqrt(2)
        kiso = [(0.0, -0.06), (0.16 * T * q, -0.06), (0.16 * T * q, y[1] * 0.6), (0.11 * T * q, y[1]), (0.0, y[1])]
        sr = 0.055 * T * q
        sao = [(0.0, y[1]), (sr, y[1]), (sr * 0.95, y[2]), (0.0, y[2])]
        chu = [(0.0, y[2]), (0.08 * T * q, y[2]), (0.14 * T * q, y[3] - 0.02 * T), (0.14 * T * q, y[3]), (0.0, y[3])]
        fb = (y[3], y[4], 0.10 * T * q, 4, SQ)
        kasa = [(0.0, y[4]), (0.19 * T * q, y[4]), (0.20 * T * q, y[4] + 0.03 * T), (0.10 * T * q, y[4] + 0.08 * T),
                (0.04 * T * q, y[5]), (0.0, y[5])]
        hoju = [(0.0, y[5]), (0.05 * T, y[5]), (0.06 * T, y[5] + 0.05 * T), (0.05 * T, y[5] + 0.10 * T),
                (0.0, y[6])]
        return [("kiso", kiso, 4, SQ), ("sao", sao, 4, SQ), ("chudai", chu, 4, SQ), ("kasa", kasa, 4, SQ),
                ("hoju", hoju, 8, OCT)], fb, y
    raise KeyError(kind)


def lantern(kind, T=1.8, moss=False, ab=None, text=True):
    """kind: kasuga | square | oki | joyato. ab: 'toppled' (hoju + kasa on the ground beside it) | 'hoju' (only the
    jewel fallen, the fire box twisted on its seat)."""
    budget = "small" if T <= 1.85 or kind == "oki" else "box"
    wear = "_w2" if (moss or ab) else "_w1"
    P = SPart("stone_lantern", budget=budget, res3=(budget == "box"), mass=120.0 * (T / 1.8) ** 3,
              bury=0.12 if kind == "oki" else 0.08)
    small = budget == "small"
    P.wear = wear
    vis, cols, fall = [], [], []
    base_y = 0.0
    if kind == "oki":
        # small placed lantern: on a rough stone, broad roof, no shaft (garden / courtyard)
        st = core.stone(random.Random(5), 0.0, 0.0, 0.50, 0.42, 0.22, 0.16, FIELD, bury=0.05, n=8, flat_top=0.8,
                        vis=(1, 2))
        vis.append(st)
        cols.append(col(-0.20, 0.20, 0.0, 0.16, -0.16, 0.16, FIELD))
        y0 = 0.16
        parts = [("chudai", [(0.0, y0), (0.16, y0), (0.17, y0 + 0.05), (0.0, y0 + 0.05)], 4, SQ)]
        fb = (y0 + 0.05, y0 + 0.31, 0.15, 4, SQ)
        y4 = y0 + 0.31
        parts += [("kasa", [(0.0, y4), (0.33, y4), (0.34, y4 + 0.035), (0.16, y4 + 0.11), (0.05, y4 + 0.16),
                            (0.0, y4 + 0.16)], 6, HEX),
                  ("hoju", [(0.0, y4 + 0.16), (0.04, y4 + 0.16), (0.05, y4 + 0.20), (0.035, y4 + 0.25), (0.0, y4 + 0.28)],
                   8, OCT)]
        top = y4 + 0.28
        ys = [0.0, y0, y0, y0 + 0.05, y4, y4 + 0.16, top]
    elif kind == "joyato":
        # always-lit lantern on a two-step base; square, tall (4.0); text on the shaft
        for i, (w, h) in enumerate(((1.70, 0.30), (1.25, 0.30))):
            yb = i * 0.30
            vis.append(W(-w / 2, w / 2, yb - (0.06 if i == 0 else 0.0), yb + h, -w / 2, w / 2, CARVED, vis=(1, 2, 3)))
            cols.append(col(-w / 2, w / 2, yb, yb + h, -w / 2, w / 2, CARVED))
            cols[-1].tag = "step%d" % i
        base_y = 0.60
        parts, fb, ys = lantern_parts("square", T - base_y)
        parts = [(nm, [(r, y + base_y) for r, y in pr], n, ph) for nm, pr, n, ph in parts]
        fb = (fb[0] + base_y, fb[1] + base_y, fb[2], fb[3], fb[4])
        ys = [y + base_y for y in ys]
    else:
        parts, fb, ys = lantern_parts(kind, T)
    # ---- visual parts in each LOD
    groups = {}
    for nm, pr, n, ph in parts:
        g = [lt(pr, n, ph, vis=(1,))]
        simple = [pr[0], pr[1], pr[-2], pr[-1]] if len(pr) > 4 else pr
        g.append(lt(simple, max(4, n if n <= 6 else 6), ph if n <= 6 else HEX, vis=(2,)))
        if P.res3 and nm not in ("hoju",):
            g.append(lt([pr[0], pr[1], pr[-2], pr[-1]] if len(pr) > 3 else pr, 4, SQ, vis=(3,)))
        groups[nm] = g
    # fire box: top + bottom slabs, side panels, windows open on +-z
    y0, y1, R, n, ph = fb
    th = 0.035 * (y1 - y0) / 0.3 + 0.02
    fbg = [lt([(0.0, y0), (R, y0), (R, y0 + th), (0.0, y0 + th)], n, ph, vis=(1,)),
           lt([(0.0, y1 - th), (R, y1 - th), (R, y1), (0.0, y1)], n, ph, vis=(1,))]
    fbg += firebox_panels(R, y0 + th, y1 - th, th * 0.9, n, ph, windows=(90.0, 270.0))
    fbg.append(lt([(0.0, y0), (R, y0), (R, y1), (0.0, y1)], n, ph, vis=(2,)))
    if P.res3:
        fbg.append(lt([(0.0, y0), (R * 0.9, y0), (R * 0.9, y1), (0.0, y1)], 4, SQ, vis=(3,)))
    groups["hibukuro"] = fbg
    # warabite: the curled-up corners of a Kasuga roof
    if kind == "kasuga":
        kp = dict((nm, pr) for nm, pr, n, ph in parts)["kasa"]
        ye = kp[2][1]
        Re = kp[2][0]
        for k in range(6):
            a = HEX + 2 * math.pi * k / 6
            cx, cz = Re * math.cos(a), Re * math.sin(a)
            groups["kasa"].append(pole((cx * 0.97, ye - 0.01, cz * 0.97), (cx * 1.03, ye + 0.035 * T, cz * 1.03),
                                       0.012 * T + 0.004, CARVED, n=3 if small else 4, vis=(1,)))
    # ---- text (front of the shaft / the joyato shaft); moss
    tx = []
    if text and kind in ("kasuga", "square", "joyato"):
        sp = dict((nm, pr) for nm, pr, n, ph in parts)["sao"]
        sy0, sy1 = sp[0][1], sp[-1][1]
        if kind == "kasuga":
            sr = sp[2][0]
            fz = sr * math.cos(math.pi / 8)
            fw = 2 * sr * math.sin(math.pi / 8) * 0.85
            tx.append(K.carved((0.0, sy0 + (sy1 - sy0) * 0.68, fz), X, Y, None or fw / 0.31, "kento_kyoho12_ujiko",
                               wear=wear, crop=(0.62, 0.0, 1.0, 0.55), width=fw))
            if not small:
                tx.append(K.carved((fz, sy0 + (sy1 - sy0) * 0.45, 0.0), (0.0, 0.0, -1.0), Y, fw / 0.143,
                                   "kento_kyoho12_ujiko", wear=wear, crop=(0.30, 0.0, 0.62, 1.0), width=fw))
        else:
            sr = sp[1][0]
            fz = sr * math.cos(math.pi / 4)
            fw = 2 * fz * 0.8
            if kind == "joyato":
                h = min((sy1 - sy0) * 0.75, fw / (0.1269 / 0.3711))
                tx.append(K.carved((0.0, sy0 + (sy1 - sy0) * 0.55, fz), X, Y, h, "joyato", wear=wear, width=fw))
            else:
                tx.append(K.carved((0.0, sy0 + (sy1 - sy0) * 0.60, fz), X, Y, fw / 0.31, "kento_kyoho12_ujiko",
                                   wear=wear, crop=(0.62, 0.0, 1.0, 0.55), width=fw))
    mo = []
    pr_k = dict((nm, (pr, n, ph)) for nm, pr, n, ph in parts)
    kp, kn, kph = pr_k["kasa"]
    if moss:
        mo.append(moss_cap(kp[1:4] if small else kp[1:-1], kn, kph, wear="_w2"))
        cp, cn, cph = pr_k["chudai"]
        mo.append(moss_cap(cp[-3:-1], cn, cph, wear="_w2"))
        if "kiso" in pr_k and not small:
            kip, kin, kiph = pr_k["kiso"]
            mo.append(moss_cap(kip[2:4], kin, kiph, wear="_w2"))
        if kind != "joyato":
            mo.append(moss_top(55, 0.0, -0.12, 0.17 * T + 0.22, 0.004, wear="_w2", sx=1.2, sz=0.8))
    else:
        mo.append(moss_cap(kp[2:4], kn, kph, wear="_w0"))      # thin lichen at the eaves
    # ---- collision: stacked components, each its own y band (touching only)
    for nm, pr, n, ph in parts:
        if nm == "hoju":
            continue
        rmax = max(r for r, _ in pr)
        ylo = max(0.0, min(y for _, y in pr))
        yhi = max(y for _, y in pr)
        if nm == "sao":
            rmax = max(r for r, _ in pr[1:-1]) * 0.95
        c = cyl_col(rmax * 0.97, ylo, yhi, n=n if n <= 8 else 8, mat=CARVED)
        c.tag = nm
        cols.append(c)
    fc = cyl_col(R * 0.97, y0, y1, n=n, mat=CARVED)
    fc.tag = "hibukuro"
    cols.append(fc)
    # stacked bands touch, never overlap (C6b): clamp each band's bottom to the band below
    stack = sorted([c for c in cols if getattr(c, "tag", "")], key=lambda c: c.bbox()[2])
    for a, b in zip(stack, stack[1:]):
        ya = a.bbox()[3]
        if b.bbox()[2] < ya:
            b.verts = [(v[0], max(v[1], ya), v[2]) for v in b.verts]
    # ---- abandoned
    if ab in ("toppled", "hoju"):
        drop = ("kasa", "hoju") if ab == "toppled" else ("hoju",)
        fallen = []
        for nm in drop:
            fallen += groups.pop(nm)
        fallen_cols = [c for c in cols if getattr(c, "tag", "") in drop]
        cols = [c for c in cols if getattr(c, "tag", "") not in drop]
        mo = [m for m in mo if m.bbox()[2] < ys[4] - 0.01] if ab == "toppled" else mo
        # the hoju alone has no collision: give the fallen jewel a small box
        hy = [y for nm, pr, n, ph in parts if nm == "hoju" for _, y in pr]
        hr = [r for nm, pr, n, ph in parts if nm == "hoju" for r, _ in pr]
        fallen_cols.append(col(-max(hr), max(hr), min(hy), max(hy), -max(hr), max(hr), CARVED))
        if ab == "toppled":
            # kasa + hoju: the roof lands upside down-ish beside the lantern, the jewel rolled further
            roof = [s for s in fallen if s.bbox()[3] <= ys[5] + 0.06 * T]
            jewel = [s for s in fallen if not any(s is q for q in roof)]
            rc = [c for c in fallen_cols if getattr(c, "tag", "") == "kasa"]
            jc = [c for c in fallen_cols if getattr(c, "tag", "") != "kasa"]
            roof = xfs(roof + rc, t=(0.0, -ys[4], 0.0))
            roof = xfs(roof, rz=118.0, ry=25.0)
            lo = min(v[1] for s in roof for v in s.verts)
            roof = xfs(roof, t=(0.30 * T + 0.25, -lo - 0.03, 0.18 * T))
            jw = xfs(jewel + jc, t=(0.0, -ys[5], 0.0))
            jw = xfs(jw, rz=95.0, ry=-40.0)
            lo = min(v[1] for s in jw for v in s.verts)
            jw = xfs(jw, t=(-0.20 * T - 0.15, -lo - 0.02, 0.32 * T))
            moved = roof + jw
            # the fire box shifted on the platform and tipped a little
            groups["hibukuro"] = xfs(groups["hibukuro"], ry=17.0, rz=4.0, pivot=(0.0, y0, 0.0))
        else:
            jw = xfs(fallen + fallen_cols, t=(0.0, -ys[5], 0.0))
            jw = xfs(jw, rz=90.0, ry=30.0)
            lo = min(v[1] for s in jw for v in s.verts)
            moved = xfs(jw, t=(0.25 * T + 0.10, -lo - 0.02, 0.20 * T))
            groups["hibukuro"] = xfs(groups["hibukuro"], ry=11.0, pivot=(0.0, y0, 0.0))
        for s in moved:
            (cols if not s.vis else fall).append(s)
        fall.append(litter(57, 0.25 * T, 0.2 * T, 0.35 * T + 0.2, sx=1.3))
        P.notes.append("abandoned: %s fallen beside the post (quake), the most common stone-lantern ruin" %
                       " + ".join(drop))
    for g in groups.values():
        vis += g
    K.aged_stone(vis + fall, 9200 + int(T * 100) + len(kind) + (5 if moss else 0))   # FP1: no repeating lichen dots
    add_all(P, vis + tx + mo + fall + cols)
    P.dim("height", T, max(v[1] for s in vis if 1 in s.vis for v in s.verts) if not ab else T, tol=0.03)
    if kind == "kasuga":
        P.dim("kasuga_proportion_sao", 0.36, round((ys[2] - ys[1]) / T * 1.01, 3), tol=0.01)
    P.extra.update({"moss": moss, "kind": kind})
    P.notes.append("pairs mirrored across the approach; no light (never emissive)")
    return P


# ================================================================================================ chozubachi
def ladle(cup_r=0.042, cup_h=0.07, handle=0.45, wear="_w1", vis=(1,)):
    """Hishaku: a bamboo cup with a long thin handle (along +x from the cup), cup open at the top, base at y = 0."""
    cup = lathe([(cup_r, 0.0), (cup_r, cup_h), (cup_r - 0.006, cup_h), (cup_r - 0.006, 0.008), (0.0, 0.008)], 6, BAMBOO,
                vis=vis, smooth=True)
    bot = core.sheet([[(cup_r * math.cos(a), 0.0, cup_r * math.sin(a)) for a in
                       [math.pi / 6 + k * math.pi / 3 for k in range(6)]]], BAMBOO, (0.0, -1.0, 0.0), vis=vis)
    bot.finalize()
    h = pole((cup_r - 0.004, cup_h * 0.6, 0.0), (cup_r + handle, cup_h * 0.6 + 0.04, 0.0), 0.008, BAMBOO, n=4, vis=vis)
    out = [cup, bot, h]
    for q in out:
        q.wear = wear
    return out


def chozubachi(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else "_w1"
    P = SPart("chozubachi", budget="small", res3=False, mass={"small": 450.0, "ab_dry": 450.0, "large": 1700.0,
                                                             "natural": 700.0}[kind], bury=0.10)
    P.wear = wear
    out, cols = [], []
    if kind in ("small", "ab_dry", "large"):
        if kind == "large":
            L, D, H, rim, depth, py = 1.50, 0.75, 0.75, 0.107, 0.35, 0.0
            cell = "hono_genroku10"
        else:
            L, D, H, rim, depth, py = 0.82, 0.48, 0.42, 0.09, 0.24, 0.15
            cell = "hono_tenna2_muraju"
        if py:
            # one flat plinth stone under the basin (the 1682 basin stands 0.57 in all)
            pl = core.stone(random.Random(3), 0.0, 0.0, L + 0.22, D + 0.20, 0.20, py, FIELD, bury=0.04, n=8, flat_top=0.9,
                            vis=(1, 2))
            out.append(pl)
            cols.append(col(-(L + 0.1) / 2, (L + 0.1) / 2, 0.0, py, -(D + 0.08) / 2, (D + 0.08) / 2, FIELD))
        y0 = py - (0.02 if py else 0.06)
        top = py + H
        outer = [(y0, K.rect(-L / 2, L / 2, -D / 2, D / 2)), (top - 0.03, K.rect(-L / 2, L / 2, -D / 2, D / 2)),
                 (top, K.rect(-L / 2 + 0.015, L / 2 - 0.015, -D / 2 + 0.015, D / 2 - 0.015))]
        inner = K.rect(-L / 2 + rim, L / 2 - rim, -D / 2 + rim, D / 2 - rim)
        out += K.hollow(outer, inner, top, top - depth, CARVED, vis=(1,), wear=wear,
                        fill=top - depth * (0.55 if not ab else 0.75), fill_wear="_w1" if not ab else "_w2")
        out.append(W(-L / 2, L / 2, y0, top, -D / 2, D / 2, CARVED, vis=(2,)))
        out.append(K.carved((0.0, py + H * 0.50, D / 2), X, Y, H * 0.62, cell, wear=wear))
        out.append(moss_face((0.0, py + H * 0.3, -D / 2), (-1.0, 0.0, 0.0), Y, L * 0.8, H * 0.45, seed=3,
                             wear="_w2" if ab else "_w1"))
        cols.append(col(-L / 2, L / 2, py, top, -D / 2, D / 2, CARVED))
        P.dim("basin_l", L, L, tol=0.005)
        P.dim("basin_d", D, D, tol=0.005)
        P.dim("height", 0.57 if kind != "large" else 0.75, top, tol=0.01)
        P.dim("hollow_depth", 0.35 if kind == "large" else 0.24, depth, tol=0.005)
        if not ab:
            # ladles laid across the hollow, cups resting on the rim
            for k, zz in enumerate((-0.06, 0.07) if kind != "large" else (-0.12, 0.0, 0.12)):
                lad = ladle(wear="_w1")
                x0 = -L / 2 + rim * 0.5 if k % 2 == 0 else L / 2 - rim * 0.5
                lad = xfs(lad, ry=180.0 if k % 2 else 0.0, t=(x0, top, zz))
                out += lad
        else:
            # dry: ladles fallen beside the basin, one split; moss heavy on the rim; leaves blown round it
            out += xfs(ladle(wear="_w2"), ry=35.0, t=(L / 2 + 0.25, 0.0, D / 2 + 0.15))
            out += xfs(ladle(wear="_w2")[:2], rz=95.0, t=(-L / 2 - 0.18, 0.045, D / 2 + 0.25))
            out.append(pole((-L / 2 - 0.30, 0.012, D / 2 + 0.35), (-L / 2 + 0.05, 0.012, D / 2 + 0.55), 0.008, BAMBOO,
                            n=4, vis=(1,), wear="_w2"))
            out.append(K.moss_strip([(-L / 2 + 0.03, top, -D / 2 + rim / 2), (0.0, top, -D / 2 + rim / 2),
                                     (L / 2 - 0.05, top, -D / 2 + rim / 2)], rim * 0.9, seed=8, wear="_w2", off=0.003))
            out.append(litter(9, 0.15, 0.35, 0.55, sx=1.5))
    else:   # natural stone with a round cut hollow (mountain shrine)
        rr = random.Random(12)
        n = 10
        base = [(0.50 * (1 + rr.uniform(-0.22, 0.18)) * math.cos(2 * math.pi * k / n),
                 -0.38 * (1 + rr.uniform(-0.22, 0.18)) * math.sin(2 * math.pi * k / n)) for k in range(n)]
        prof = [(-0.08, 0.80), (0.10, 0.97), (0.30, 1.0), (0.45, 0.88), (0.52, 0.70)]
        outer = [(y, [(x * k, z * k) for x, z in base]) for y, k in prof]
        inner = [(0.03 + 0.17 * math.cos(2 * math.pi * k / n), -0.17 * math.sin(2 * math.pi * k / n)) for k in range(n)]
        top = 0.52
        out += K.hollow(outer, inner, top, top - 0.15, CARVED, vis=(1,), wear=wear, fill=top - 0.10, fill_wear="_w1")
        b2 = [base[k] for k in range(0, n, 2)]
        out.append(core.rings((core.hull2d(b2), [(-0.08, 0.80), (0.30, 1.0), (0.52, 0.70)]), CARVED, vis=(2,)))
        cols.append(core.rings((core.hull2d(base), [(0.0, 0.84), (0.10, 0.97), (0.30, 1.0), (0.45, 0.88), (0.52, 0.70)]), CARVED,
                               vis=(), geo=True, view=True, fire=True))
        lad = xfs(ladle(wear="_w1"), ry=200.0, t=(0.0, top, 0.10))
        out += lad
        out.append(moss_top(14, -0.15, -0.20, 0.16, top - 0.004, wear="_w2", sx=1.2, sz=0.6))
        P.dim("hollow_d", 0.34, 0.34, tol=0.01)
        P.dim("height", 0.52, top, tol=0.01)
    add_all(P, out + cols)
    P.notes.append("dry: leaves and silt in the hollow, not a water source (BUILD_LIST decision 3)")
    P.notes.append("beside the approach, right-hand side walking in, 3-6 m before the hall; one per shrine")
    return P


# ================================================================================================ stone steps
RISE = 0.16
TREAD = 0.91 / 3          # 0.3033: three treads = half a ken, six = one ken (grid, rule 9)
MAX_DEG = 38.0            # C7 / PLAYBOOK T9 (37.8 walks fine)


def c7_check(P, L):
    """C7 for a step module, read from the written MLOD Roadway: ramp <= 38 deg; the foot edge (z 0, y 0) and the head
    edge (z -run, y rise) span the full width, so modules chained foot-to-head by their connectors give one
    continuous Roadway; every tread top lies within one riser above the ramp (the feet never sink deeper)."""
    ex = P.extra
    W_, run, rise = ex["width"], ex["run"], ex["rise"]
    rw = L.get("Roadway")
    det = {"width": W_, "run": run, "rise": rise}
    if rw is None:
        return {"id": "C7", "name": "walkability: Roadway ramp", "pass": False, "detail": "no Roadway"}
    pts = rw.points
    ang = math.degrees(math.atan2(rise, run)) if run > 0 else 0.0
    det["ramp_deg"] = round(ang, 2)

    def edge(zv, yv):
        xs = [p[0] for p in pts if abs(p[2] - zv) < 0.002 and abs(p[1] - yv) < 0.002]
        return (min(xs), max(xs)) if xs else None
    foot = edge(0.0, 0.0)
    head = edge(-run, rise)
    det["foot_edge_x"] = foot
    det["head_edge_x"] = head
    full = lambda e: e is not None and e[0] <= -W_ / 2 + 0.002 and e[1] >= W_ / 2 - 0.002   # noqa: E731
    # every Roadway point lies on the ramp plane y = rise * (-z / run)
    off = max(abs(p[1] - (rise * (-p[2] / run) if run > 0 else 0.0)) for p in pts)
    det["off_plane_m"] = round(off, 4)
    nose = ex.get("nosing_above_ramp", 0.0)
    det["max_tread_above_ramp_m"] = nose
    ok = ang <= MAX_DEG + 1e-6 and full(foot) and full(head) and off < 0.002 and nose <= RISE + 0.03
    return {"id": "C7", "name": "walkability: ramp <= 38 deg, Roadway edges full width at the foot (z 0, y 0) and the "
            "head (z -run, y rise) so chained modules join, treads within a riser of the ramp", "pass": ok,
            "detail": det}


def steps(kind, n=3, width=1.82, ab=None):
    """kind dressed | rough | landing | cheek. Dressed: cut granite blocks, each tucked 8 cm under the next; rough:
    field stones, 2-3 per step; landing: one slab course 1.82 deep, top flush (y 0); cheek: one side stone along a
    flight of n steps (place one each side at x = +-(width / 2 + 0.10))."""
    wear = "_w2" if ab else "_w1"
    P = SPart("stone_steps", budget="small", res3=False, mass=300.0 * max(n, 4) * width, bury=0.22)
    P.wear = wear
    vis, cols = [], []
    rr = random.Random(n * 7 + int(width * 100) + len(kind) + (5 if ab else 0))
    run, rise = n * TREAD, n * RISE
    if kind == "landing":
        D = 1.82
        run, rise = D, 0.0
        k = 3 if width > 2 else 2
        for i in range(k):
            x0 = -width / 2 + width * i / k
            x1 = -width / 2 + width * (i + 1) / k
            vis.append(W(x0 + 0.004, x1 - 0.004, -0.18, 0.0, -D, 0.0, CUT, vis=(1,)))
        vis.append(W(-width / 2, width / 2, -0.18, 0.0, -D, 0.0, CUT, vis=(2,)))
        cols.append(col(-width / 2, width / 2, -0.18, 0.0, -D, 0.0, CUT))
        P.road([(-width / 2, 0.0, 0.0), (width / 2, 0.0, 0.0), (width / 2, 0.0, -D), (-width / 2, 0.0, -D)], "stone_ext")
        vis.append(skit.stain(31, 0.2, -1.1, 0.6, y=0.004, mat=skit.LITTER, wear="_w2", sx=1.5))
        vis.append(moss_top(32, -width / 2 + 0.15, -0.9, 0.2, 0.002, wear="_w1", sx=0.6, sz=2.0))
        P.dim("landing_depth", 1.82, D, tol=0.002)
    elif kind == "cheek":
        # a sloped side stone (sode-ishi) along the flight: top 0.30 above the ramp, 0.20 wide
        top0, top1 = 0.30, rise + 0.30
        c = core.hexa([(-0.10, -0.15, 0.05), (0.10, -0.15, 0.05), (0.10, rise - 0.15, -run - 0.05),
                       (-0.10, rise - 0.15, -run - 0.05),
                       (-0.10, top0, 0.05), (0.10, top0, 0.05), (0.10, top1, -run - 0.05), (-0.10, top1, -run - 0.05)],
                      CUT, vis=(1, 2))
        vis.append(c)
        cols.append(col_solid(c))
        vis.append(K.moss_strip([(0.0, top0, 0.0), (0.0, top0 + rise * 0.5, -run * 0.5), (0.0, top1, -run)], 0.12,
                                seed=33, wear="_w1"))
        P.dim("cheek_len", run + 0.10, run + 0.10, tol=0.002)
        P.notes.append("one side stone; place one each side of a flight at x = +-(flight width / 2 + 0.10)")
    else:
        # the hidden walk ramp (Geometry / View / Fire) and its Roadway, from the foot to the head
        wedge = core.Solid([(-width / 2, 0.0, 0.0), (width / 2, 0.0, 0.0), (width / 2, 0.0, -run), (-width / 2, 0.0, -run),
                            (-width / 2, rise, -run), (width / 2, rise, -run)],
                           [[0, 1, 2, 3], [3, 2, 5, 4], [0, 4, 5, 1], [0, 3, 4], [1, 5, 2]], CUT, vis=(), geo=True,
                           view=True, fire=True)
        cols.append(wedge)
        P.road([(-width / 2, 0.0, 0.0), (width / 2, 0.0, 0.0), (width / 2, rise, -run), (-width / 2, rise, -run)],
               "stone_ext")
        nose = 0.0
        missing = {3} if (ab and n >= 5) else set()
        for k in range(1, n + 1):
            za, zb = -(k - 1) * TREAD, -k * TREAD
            top = k * RISE
            if k in missing:
                # the step is gone: bare earth and leaves on the slope where it lay
                q = [(-width / 2, (k - 1) * RISE + 0.01, za), (width / 2, (k - 1) * RISE + 0.01, za),
                     (width / 2, k * RISE - 0.03, zb), (-width / 2, k * RISE - 0.03, zb)]
                s_ = core.sheet([q], LEAF, core.norm(core.newell(q)) if core.newell(q)[1] > 0 else
                                core.mul(core.norm(core.newell(q)), -1.0), vis=(1,))
                s_.wear = "_w2"
                vis.append(s_)
                continue
            if kind == "dressed":
                m = max(1, int(round(width / 0.91)))         # one cut stone per half ken, 4 mm joints
                for i in range(m):
                    x0 = -width / 2 + width * i / m + (0.002 if i else 0.0)
                    x1 = -width / 2 + width * (i + 1) / m - (0.002 if i < m - 1 else 0.0)
                    b = W(x0, x1, (k - 1) * RISE - 0.12, top, zb - (0.08 if k < n else 0.0), za, CUT, vis=(1,),
                          uvoff=(rr.random(), rr.random()))
                    if ab:
                        b = xf(b, rx=rr.uniform(-3.0, 2.0), rz=rr.uniform(-1.2, 1.2), pivot=((x0 + x1) / 2, top,
                                                                                          (za + zb) / 2))
                    vis.append(b)
                    nose = max(nose, max(v[1] - rise * (-v[2] / run) for v in b.verts if v[1] > top - 0.05))
            else:
                m = 2 if width < 1.0 else 3
                for i in range(m):
                    x0 = -width / 2 + width * i / m
                    x1 = -width / 2 + width * (i + 1) / m
                    st = core.stone(rr, (x0 + x1) / 2, (za + zb) / 2 - 0.075, (x1 - x0) * 1.08, TREAD + 0.14, RISE + 0.12,
                                    top + rr.uniform(-0.02, 0.015), FIELD, bury=0.0, n=6, flat_top=0.97, vis=(1,))
                    vis.append(st)
                    nose = max(nose, max(v[1] - rise * (-v[2] / run) for v in st.verts))
            # leaves drifted on the tread, moss in the joint at the back
            if ab or k % 2 == 0:
                vis.append(skit.stain(40 + k, rr.uniform(-width / 4, width / 4), (za + zb) / 2, min(0.30, width / 3),
                                      y=top + 0.004, mat=skit.LITTER, wear="_w2", sx=1.6, sz=0.45))
            if kind == "dressed" and k < n and (ab or k % 2 == 1):
                vis.append(K.moss_strip([(-width / 2 + 0.05, top, zb + 0.02), (0.0, top, zb + 0.02),
                                         (width / 2 - 0.05, top, zb + 0.02)], 0.05, seed=50 + k, wear="_w1"))
        # Resolution 2: the stepped profile as one prism per step pair
        prof = [(0.0, -0.12)]
        for k in range(1, n + 1):
            prof += [(-(k - 1) * TREAD, k * RISE), (-k * TREAD, k * RISE)]
        prof += [(-run, (n - 1) * RISE - 0.12)]
        for k in range(1, n + 1):
            vis.append(W(-width / 2, width / 2, (k - 1) * RISE - 0.12, k * RISE, -k * TREAD, -(k - 1) * TREAD,
                         CUT if kind == "dressed" else FIELD, vis=(2,)))
        P.extra["nosing_above_ramp"] = round(nose, 4)
        P.dim("riser", RISE, RISE, tol=0.001)
        P.dim("tread", TREAD, TREAD, tol=0.001)
        P.dim("ramp_deg", 27.8, round(math.degrees(math.atan2(rise, run)), 2), tol=0.1)
        P.dim("width", width, width, tol=0.001)
        P.checks_extra = [c7_check]
        if ab:
            P.notes.append("abandoned: treads tilted by roots and frost%s, leaves on every step; the ramp under them "
                           "is unchanged (still walkable)" % (", step 3 gone" if missing else ""))
    add_all(P, vis + cols)
    P.extra.update({"width": width, "run": round(run, 4), "rise": round(rise, 4),
                    "connectors": {"stair_foot": [0.0, 0.0, 0.0], "stair_head": [0.0, round(rise, 4), round(-run, 4)]},
                    "chain": "place the next module's stair_foot on this one's stair_head (same yaw): the Roadway "
                             "continues (C7)"})
    if kind == "landing":
        P.checks_extra = [c7_check]
    return P


# ================================================================================================ registry
def SL(sfx, kind, T, moss=False, ab=None, display=""):
    return M("jp_s_stone_lantern_" + sfx, kind, "abandoned" if ab else "intact", display,
             lambda: lantern(kind, T, moss=moss, ab=ab), mount="shrine")


PROPS = [
    {"id": "jp_s_stone_lantern", "cat": "shrine", "mount": "shrine", "per_row": 7,
     "notes": ["in mirrored pairs at the torii and the hall steps; rows of 4-20 only on landmark approaches; oki in "
               "courtyard gardens", "mossy variants (Stephen): Kasuga 1.8 / 2.4 / 3.0, square, oki",
               "1 in 6 placements toppled (_ab_toppled / _ab_hoju_moss)"],
     "models": [
         SL("kasuga_18", "kasuga", 1.8, display="Stone lantern, Kasuga 1.8"),
         SL("kasuga_24", "kasuga", 2.4, display="Stone lantern, Kasuga 2.4"),
         SL("kasuga_30", "kasuga", 3.0, display="Stone lantern, Kasuga 3.0"),
         SL("square_24", "square", 2.4, display="Stone lantern, square standing 2.4"),
         SL("oki", "oki", 0.75, display="Small placed stone lantern (oki-doro)"),
         SL("joyato", "joyato", 4.0, display="Always-lit lantern (joyato) on a two-step base, 4.0"),
         SL("kasuga_18_moss", "kasuga", 1.8, moss=True, display="Stone lantern, Kasuga 1.8, mossy"),
         SL("kasuga_24_moss", "kasuga", 2.4, moss=True, display="Stone lantern, Kasuga 2.4, mossy"),
         SL("kasuga_30_moss", "kasuga", 3.0, moss=True, display="Stone lantern, Kasuga 3.0, mossy"),
         SL("square_24_moss", "square", 2.4, moss=True, display="Stone lantern, square 2.4, mossy"),
         SL("oki_moss", "oki", 0.75, moss=True, display="Small placed stone lantern, mossy"),
         SL("ab_toppled", "kasuga", 2.4, ab="toppled", display="Kasuga lantern, roof and jewel fallen (quake)"),
         SL("ab_hoju_moss", "kasuga", 1.8, moss=True, ab="hoju", display="Kasuga lantern 1.8, mossy, jewel fallen"),
     ]},
    {"id": "jp_s_chozubachi", "cat": "shrine", "mount": "shrine",
     "notes": ["no roof (many village shrines had none); a temizuya shell can stand over it later (KEEP_CIVIC)",
               "no dragon spout, no running bamboo spout (W2_ERA B1)"],
     "models": [
         M("jp_s_chozubachi_small", "small", "intact", "Stone basin, Tenna 2 (1682) size, on a plinth stone",
           lambda: chozubachi("small"), mount="shrine"),
         M("jp_s_chozubachi_large", "large", "intact", "Stone basin, long (town shrine)", lambda: chozubachi("large"),
           mount="shrine"),
         M("jp_s_chozubachi_natural", "natural", "intact", "Natural stone basin with a cut hollow (mountain shrine)",
           lambda: chozubachi("natural"), mount="shrine"),
         M("jp_s_chozubachi_ab_dry", "small", "abandoned", "Stone basin, dry and leaf-filled, ladles fallen",
           lambda: chozubachi("ab_dry"), mount="shrine"),
     ]},
    {"id": "jp_s_stone_steps", "cat": "shrine", "mount": "slope", "per_row": 7,
     "notes": ["only where the terrain rises > 0.5 m between an approach and its hall or between lane levels; seated "
               "into the slope (block bottoms 0.12 under the ramp line), never floating",
               "rise 0.16, tread 0.303 (3 treads = half a ken), ramp 27.8 deg (C7 <= 38); chain modules foot-to-head",
               "widths: 0.91 / 1.82 / 2.73 (half, 1, 1.5 ken)"],
     "models": [
         M("jp_s_stone_steps_dressed_3", "dressed_3", "intact", "Stone steps, dressed, 3 steps, 1 ken wide",
           lambda: steps("dressed", 3, 1.82)),
         M("jp_s_stone_steps_dressed_6", "dressed_6", "intact", "Stone steps, dressed, 6 steps, 1 ken wide",
           lambda: steps("dressed", 6, 1.82)),
         M("jp_s_stone_steps_dressed_3_wide", "dressed_3", "intact", "Stone steps, dressed, 3 steps, 1.5 ken wide",
           lambda: steps("dressed", 3, 2.73)),
         M("jp_s_stone_steps_dressed_6_wide", "dressed_6", "intact", "Stone steps, dressed, 6 steps, 1.5 ken wide",
           lambda: steps("dressed", 6, 2.73)),
         M("jp_s_stone_steps_dressed_3_narrow", "dressed_3", "intact", "Stone steps, dressed, 3 steps, half ken wide",
           lambda: steps("dressed", 3, 0.91)),
         M("jp_s_stone_steps_rough_3", "rough_3", "intact", "Stone steps, rough field stones, 3 steps, 1 ken wide",
           lambda: steps("rough", 3, 1.82)),
         M("jp_s_stone_steps_rough_3_narrow", "rough_3", "intact", "Stone steps, rough field stones, half ken wide",
           lambda: steps("rough", 3, 0.91)),
         M("jp_s_stone_steps_landing", "landing", "intact", "Stone landing slab course, 1 ken square",
           lambda: steps("landing", 0, 1.82)),
         M("jp_s_stone_steps_landing_wide", "landing", "intact", "Stone landing, 1.5 ken wide, 1 ken deep",
           lambda: steps("landing", 0, 2.73)),
         M("jp_s_stone_steps_cheek_3", "cheek", "intact", "Side cheek stone for a 3-step flight",
           lambda: steps("cheek", 3)),
         M("jp_s_stone_steps_cheek_6", "cheek", "intact", "Side cheek stone for a 6-step flight",
           lambda: steps("cheek", 6)),
         M("jp_s_stone_steps_ab_heaved", "dressed_6", "abandoned", "Stone steps heaved by roots, one step missing",
           lambda: steps("dressed", 6, 1.82, ab="heaved")),
         M("jp_s_stone_steps_ab_heaved_rough", "rough_3", "abandoned", "Rough stone steps, heaved, leaves drifted",
           lambda: steps("rough", 3, 1.82, ab="heaved")),
     ]},
]
