"""W2 torii (BUILD_LIST items 22-23; agent W2, 2026-09-30): wooden shinmei / myojin / vermilion myojin / yard-shrine
miniature, and the granite myojin stone torii at three spans, each with Stephen's additions: with or without a straw
rope (shimenawa) on the tie-beam, with or without paper shide on it, and mossy rural variants (moss on the kasagi, the
tie-beam and the post feet; jp_m_decal_moss). Era verdicts: research/outdoor_kit/W2_ERA.md (T1-T8).

Frame: origin = the centre between the two post feet on the terrain, +z = the approach side (front), the posts on x.
Rope anchor (sidecar 'rope_y', 'rope_z'): where jp_s_shimenawa hangs on this torii (the rope variants carry it built in).
Collision: posts, tie-beam (split at the posts), kasagi block and strut = Geometry + View + Fire; rope, shide = none.
"""
import math
import random

import skit
from skit import (core, box, prism, lathe, xf, xfs, W, col, col_solid, cyl_col, SPart, pole, beam, add_all, CARVED, CUT,
                  FIELD, WOOD, KURO, ROPE, SUMI, MOSS, LEAF, litter, moss_top)
from props_wood import M
import w2kit as K
from w2kit import SHU, X, Y, Z

ROPE_NONE, ROPE_ONLY, ROPE_SHIDE = 0, 1, 2


# ================================================================================================ wooden torii
WOOD_FORMS = {
    # S post spacing, H total height, r post radius, lean (inward batter over the height), kasagi overhang past a post,
    # rise (sori of the kasagi ends), nuki top y, nuki h x d, nuki projection past the posts
    "shinmei": dict(S=1.82, H=2.73, r=0.10, lean=0.0, over=0.36, rise=0.0, nuki_y=2.24, nuki=(0.11, 0.07), proj=0.0),
    "myojin": dict(S=2.73, H=3.45, r=0.12, lean=0.06, over=0.48, rise=0.14, nuki_y=2.68, nuki=(0.15, 0.09), proj=0.30),
    "mini": dict(S=0.60, H=0.90, r=0.032, lean=0.0, over=0.12, rise=0.04, nuki_y=0.66, nuki=(0.045, 0.028), proj=0.07),
}


def footing(x, seed, r, wear=None, mat=FIELD, vis=(1, 2)):
    """A rough footing stone round a post foot (kamaki-ishi): top 0.10 above the ground."""
    s = core.stone(random.Random(seed), x, 0.0, 2.4 * r + 0.16, 2.4 * r + 0.14, 0.18, 0.10, mat, bury=0.06, n=8,
                   flat_top=0.75, vis=vis)
    if wear:
        s.wear = wear
    return s


def torii_wood(form, rope=ROPE_NONE, moss=False, shu=False, ab=None, plaque=None):
    """ab: None | 'leaning' (one post rotted at the foot: the frame racks 6 deg, kasagi sags, rope dropped) |
    'peeled' (vermilion peeled to grey in patches, leaning) | 'rotted' (shinmei: kasagi slipped at one end)."""
    F = WOOD_FORMS[form]
    S, H, r = F["S"], F["H"], F["r"]
    mini = form == "mini"
    wear = "_w2" if (ab or moss) else "_w1"
    mat = SHU if shu else WOOD
    P = SPart("torii_wood", budget=("box" if rope else "small") if mini else "medium", res3=not mini,   # FP2: rope
              mass={"shinmei": 600.0, "myojin": 1100.0, "mini": 15.0}[form], bury=0.15 if not mini else 0.05)
    P.wear = wear
    solids, cols = [], []
    n_post = 6 if mini else 8
    ytop_post = {}
    # ---- kasagi (top beam) and shimaki (second beam) centre lines
    L = S + 2 * F["over"]
    if form == "shinmei":
        kh = 0.20
        kas_cl = [(-L / 2, H - kh / 2), (L / 2, H - kh / 2)]
        ky_post = H - kh                       # post tops reach the kasagi underside
        kas = pole((-L / 2, H - kh / 2, 0.0), (L / 2, H - kh / 2, 0.0), kh / 2, mat, n=8, vis=(1,), caps=None)
        kas2 = pole((-L / 2, H - kh / 2, 0.0), (L / 2, H - kh / 2, 0.0), kh / 2, mat, n=5, vis=(2,))
        kas3 = pole((-L / 2, H - kh / 2, 0.0), (L / 2, H - kh / 2, 0.0), kh / 2, mat, n=4, vis=(3,))
        solids += [kas, kas2, kas3]
        kas_top = [(x, H, 0.0) for x in (-L / 2 + 0.05, -L / 4, 0.0, L / 4, L / 2 - 0.05)]
        kmin, kmax = H - kh, H
    else:
        kh, kd = (0.16, 0.22) if not mini else (0.05, 0.065)
        sh_h, sh_d = (0.12, 0.17) if not mini else (0.04, 0.05)
        rise = F["rise"]
        cl = K.curve(-L / 2, L / 2, H - kh / 2 - rise * 0.0, rise, n=8 if not mini else 6)
        top_mat = KURO if shu else mat
        solids.append(K.sweep(cl, kh, kd, top_mat, vis=(1,), top_w=kd * 1.15))
        solids.append(K.sweep(K.curve(-L / 2, L / 2, H - kh / 2, rise, n=4), kh, kd, top_mat, vis=(2,)))
        if not mini:
            solids.append(K.sweep(K.curve(-L / 2, L / 2, H - kh / 2, rise, n=2), kh, kd, top_mat, vis=(3,)))
        L2 = L - (0.22 if not mini else 0.06)
        scl = K.curve(-L2 / 2, L2 / 2, H - kh - sh_h / 2, rise * 0.85, n=8 if not mini else 6)
        solids.append(K.sweep(scl, sh_h, sh_d, mat, vis=(1,)))
        solids.append(K.sweep(K.curve(-L2 / 2, L2 / 2, H - kh - sh_h / 2, rise * 0.85, n=4), sh_h, sh_d, mat, vis=(2,)))
        tt = (S / 2) / (L2 / 2)
        ky_post = H - kh - sh_h + rise * 0.85 * (tt ** 2)
        kas_top = [(x, y + kh / 2, 0.0) for x, y in cl]
        kmin, kmax = H - kh - sh_h, H + rise
    # ---- posts (with the inward batter of the myojin form)
    lean = F["lean"]
    for sx in (-1, 1):
        x0 = sx * S / 2
        x1 = sx * (S / 2 - lean)
        y1 = ky_post + 0.02
        y0 = -0.06 if not mini else -0.02
        solids.append(pole((x0, y0, 0.0), (x1, y1, 0.0), r, mat, n=n_post, vis=(1,), r1=r * 0.94))
        solids.append(pole((x0, y0, 0.0), (x1, y1, 0.0), r, mat, n=6 if not mini else 4, vis=(2, 3) if not mini else (2,),
                           r1=r * 0.94))
        ytop_post[sx] = y1
        c = cyl_col(r, 0.0, ky_post, n=8, cx=(x0 + x1) / 2, mat=WOOD)
        cols.append(c)
        if shu and not mini:
            # black base band (nemaki) on the vermilion form
            solids.append(pole((x0, y0, 0.0), (x0 - sx * lean * 0.12, 0.42, 0.0), r * 1.03, KURO, n=n_post, vis=(1, 2)))
        if not mini:
            solids.append(footing(x0, 7 + sx, r, wear=wear))
        else:
            solids.append(core.stone(random.Random(11 + sx), x0, 0.0, 0.10, 0.10, 0.05, 0.03, FIELD, bury=0.02, n=6,
                                     vis=(1,)))
    # ---- tie-beam (nuki), wedges, strut, plaque
    nh, nd = F["nuki"]
    ny1 = F["nuki_y"]
    ny0 = ny1 - nh
    xp = S / 2 - lean * (ny0 + nh / 2) / ky_post         # the post axis at the nuki height
    xe = xp + F["proj"]
    solids.append(W(-xe, xe, ny0, ny1, -nd / 2, nd / 2, mat, vis=(1, 2) if mini else (1, 2, 3)))
    if form != "shinmei":
        for sx in (-1, 1):
            # wedges (kusabi) driven beside the posts on the outside
            if not mini:
                solids.append(W(sx * (xp + r) - 0.03, sx * (xp + r) + 0.03, ny0 - 0.015, ny1 + 0.015, -nd / 2 - 0.012,
                                nd / 2 + 0.012, mat, vis=(1,)))
        sw = 0.11 if not mini else 0.035
        solids.append(W(-sw / 2, sw / 2, ny1, kmin + 0.01, -nd * 0.35, nd * 0.35, mat, vis=(1, 2) if not mini else (1,)))
        cols.append(col(-sw / 2, sw / 2, ny1, kmin, -nd * 0.35, nd * 0.35))
        if plaque and not mini:
            # framed plaque (gaku) on the strut, text faded
            pw, ph = 0.30, 0.42
            pc = (ny1 + kmin) / 2
            pz = nd * 0.35 + 0.035
            solids.append(W(-pw / 2, pw / 2, pc - ph / 2, pc + ph / 2, nd * 0.35, pz, WOOD, vis=(1, 2)))
            fm = KURO if shu else mat
            solids.append(W(-pw / 2 - 0.02, pw / 2 + 0.02, pc + ph / 2, pc + ph / 2 + 0.03, nd * 0.35, pz + 0.012, fm,
                            vis=(1,)))
            solids.append(W(-pw / 2 - 0.02, pw / 2 + 0.02, pc - ph / 2 - 0.03, pc - ph / 2, nd * 0.35, pz + 0.012, fm,
                            vis=(1,)))
            if plaque != "blank":
                # sumi on the weathered board: _w1 (faded) standing, _w2 (ghost) when abandoned or mossy
                solids.append(K.inked((0.0, pc, pz), X, Y, ph * 0.86, plaque, wear="_w2" if (ab or moss) else "_w1"))
    # nuki collision: the span between the posts and the two stubs outside (they would overlap the posts otherwise)
    cols.append(col(-xp + r * 0.95, xp - r * 0.95, ny0, ny1, -nd / 2, nd / 2))
    if F["proj"] > 0:
        for sx in (-1, 1):
            a, b = sorted((sx * (xp + r * 1.0), sx * xe))
            cols.append(col(a, b, ny0, ny1, -nd / 2, nd / 2))
    cols.append(col(-L / 2, L / 2, max(ytop_post.values()) + 0.001, kmax, -0.13 if not mini else -0.04,
                    0.13 if not mini else 0.04))
    # ---- straw rope on the tie-beam
    rope_y = ny0 - 0.03 - (0.04 if not mini else 0.012)
    rope_z = nd / 2 + (0.05 if not mini else 0.015)
    rr_ = 0.045 if form == "myojin" else (0.035 if form == "shinmei" else 0.012)
    if rope and not ab:
        solids += K.torii_rope(-xp + r, xp - r, rope_y, rope_z, r=rr_, drop=0.10 * S / 1.82 if not mini else 0.03,
                               with_shide=rope == ROPE_SHIDE, wear="_w2", seed=len(form) * 3 + rope,
                               n_tassel=None if not mini else 3)
        for sx in (-1, 1):
            # the rope's turn round each post
            ring = xf(lathe([(r + rr_ * 0.7, rope_y - rr_), (r + rr_ * 0.7, rope_y + rr_)], 8, ROPE, vis=(1,)),
                      t=(sx * xp, 0.0, 0.0))
            ring.wear = "_w2"
            solids.append(ring)
    # ---- moss: kasagi top (two patches), tie-beam top, post feet, footing stones
    if moss:
        w_top = 0.16 if form != "mini" else 0.05
        solids.append(K.moss_strip(kas_top, w_top, seed=3, wear="_w2", frac=(0.08, 0.42)))
        solids.append(K.moss_strip(kas_top, w_top * 0.8, seed=4, wear="_w1", frac=(0.58, 0.95)))
        solids.append(K.moss_strip([(-xp + r, ny1, 0.0), (-0.2 * xp, ny1, 0.0), (0.4 * xp, ny1, 0.0)], nd * 0.85, seed=5,
                                   wear="_w1"))
        for sx in (-1, 1):
            solids += K.moss_foot(sx * S / 2, 0.0, r, 0.38 if not mini else 0.10, n=n_post, sides=3, seed=6 + sx,
                                  wear="_w2", y0=0.06 if not mini else 0.0)
            if not mini:
                solids.append(moss_top(9 + sx, sx * S / 2, -0.10, r + 0.06, 0.098, wear="_w2", sx=1.2, sz=0.7))
    add_all(P, solids + cols)
    # ---- abandoned
    if ab in ("leaning", "peeled", "rotted"):
        k = math.tan(math.radians(6.0 if ab != "rotted" else 3.5))
        vis_s = [s for s in P.solids if s.vis]
        col_s = [s for s in P.solids if not s.vis]
        if ab == "rotted":
            # the kasagi slipped off one post: the far end down 0.25, the near end still on its post
            kk = [s for s in vis_s if s.bbox()[2] >= kmin - 0.002 and s.bbox()[1] - s.bbox()[0] > S]
            rest_ = [s for s in vis_s if not any(s is q for q in kk)]
            kk = K.tilt(kk, rz=-5.5, pivot=(-S / 2, ky_post, 0.0))
            vis_s = rest_ + kk
        P.solids = K.shear(vis_s, k) + K.shear(col_s, k)
        # the rope rotted through at one end: it hangs from the left post down to the ground
        if rope:
            hang = [(-xp + r, rope_y, rope_z), (-xp + r + 0.15, rope_y - 0.5, rope_z + 0.04),
                    (-xp + r + 0.25, rope_y - 1.3, rope_z + 0.08), (-xp + r + 0.38, 0.35, rope_z + 0.15),
                    (-xp + r + 0.75, 0.03, rope_z + 0.35)]
            hang = [(x + k * y, y, z) for x, y, z in hang]
            # FP1 (2026-10-01): twisted straw strands, frayed where it snapped; the short stub left tied at the other
            # post frays too, a few loose straws on the ground under it
            for s in K.twisted_rope(hang, rr_, seed=77, wear="_w2", fray1=True):
                P.add(s)
            stub = [(xp - r, rope_y, rope_z), (xp - r - 0.10, rope_y - 0.06, rope_z + 0.01),
                    (xp - r - 0.14, rope_y - 0.20, rope_z + 0.02)]
            stub = [(x + k * y, y, z) for x, y, z in stub]
            for s in K.twisted_rope(stub, rr_, seed=78, wear="_w2", fray1=True, lod2=False):
                P.add(s)
        P.add(litter(21, 0.3, 0.6, 0.9, sx=1.4))
        P.notes.append("abandoned: racked %.1f deg on a rotted post foot; feet stay on the ground" %
                       math.degrees(math.atan(k)))
    # ---- dims and anchors
    P.dim("post_span", S, S, tol=0.005)
    P.dim("height", H, kmax if form == "shinmei" else H + F["rise"] * 0.0, tol=0.01 if form != "shinmei" else 0.005)
    P.dim("post_d", 2 * r, 2 * r, tol=0.001)
    P.dim("kasagi_overhang", F["over"], F["over"], tol=0.001)
    P.extra.update({"rope_y": round(rope_y, 3), "rope_z": round(rope_z, 3), "rope_span": round(2 * (xp - r), 3),
                    "rope": ["none", "rope", "rope+shide"][rope], "moss": moss, "shu": shu})
    if shu:
        P.notes.append("vermilion: ONLY at Inari and Hachiman shrines (restricted colour, BUILD_LIST)")
    return P


# ================================================================================================ stone torii
STONE_FORMS = {
    "s": dict(S=1.82, H=2.71, r=0.16, over=0.40, rise=0.10, nuki_y=2.06, nuki=(0.17, 0.13), proj=0.22,
              text="hono_tenna2_muraju"),
    "m": dict(S=2.50, H=2.80, r=0.20, over=0.42, rise=0.11, nuki_y=2.12, nuki=(0.19, 0.15), proj=0.24,
              text="hono_genroku10"),
    "l": dict(S=3.60, H=4.20, r=0.25, over=0.60, rise=0.16, nuki_y=3.20, nuki=(0.26, 0.20), proj=0.34,
              text="hono_genroku10"),
}


def torii_stone(size, rope=ROPE_NONE, moss=False, ab=None):
    """Granite myojin: one-piece kasagi + shimaki, round posts with a slight batter on dome bases (kamebara), the
    tie-beam through the posts, a strut, donor text on the right-hand post (seen from the approach). ab 'broken':
    the kasagi fallen in two pieces beside the posts (quake), the strut down too."""
    F = STONE_FORMS[size]
    S, H, r = F["S"], F["H"], F["r"]
    wear = "_w2" if (ab or moss) else "_w1"
    P = SPart("torii_stone", budget="medium", res3=True, mass={"s": 3500.0, "m": 5000.0, "l": 11000.0}[size], bury=0.12)
    P.wear = wear
    solids, cols = [], []
    L = S + 2 * F["over"]
    rise = F["rise"]
    kh = max(0.20, round(r * 1.30, 3))
    kd = round(r * 1.6, 3)
    sh_h = round(r * 1.0, 3)
    cl = K.curve(-L / 2, L / 2, H - kh / 2, rise, n=8)
    solids.append(K.sweep(cl, kh, kd, CARVED, vis=(1,), top_w=kd * 1.12))
    solids.append(K.sweep(K.curve(-L / 2, L / 2, H - kh / 2, rise, n=4), kh, kd, CARVED, vis=(2,)))
    solids.append(K.sweep(K.curve(-L / 2, L / 2, H - kh / 2, rise, n=2), kh, kd, CARVED, vis=(3,)))
    L2 = L - 0.30
    scl = K.curve(-L2 / 2, L2 / 2, H - kh - sh_h / 2, rise * 0.8, n=8)
    solids.append(K.sweep(scl, sh_h, kd * 0.82, CARVED, vis=(1,)))
    solids.append(K.sweep(K.curve(-L2 / 2, L2 / 2, H - kh - sh_h / 2, rise * 0.8, n=4), sh_h, kd * 0.82, CARVED, vis=(2,)))
    ky_post = H - kh - sh_h + rise * 0.8 * ((S / 2) / (L2 / 2)) ** 2
    kmin, kmax = H - kh - sh_h, H + rise
    lean = 0.035 * H / 2.71
    kas_group = list(solids)
    for sx in (-1, 1):
        x0, x1 = sx * S / 2, sx * (S / 2 - lean)
        solids.append(pole((x0, -0.10, 0.0), (x1, ky_post + 0.02, 0.0), r, CARVED, n=8, vis=(1,), r1=r * 0.93))
        solids.append(pole((x0, -0.10, 0.0), (x1, ky_post + 0.02, 0.0), r, CARVED, n=6, vis=(2, 3), r1=r * 0.93))
        cols.append(cyl_col(r, 0.201, ky_post, n=8, cx=(x0 + x1) / 2, mat=CARVED))
        # dome base (kamebara)
        b = lathe([(0.0, -0.08), (r * 1.75, -0.08), (r * 1.75, 0.04), (r * 1.45, 0.16), (r * 1.08, 0.22), (0.0, 0.22)],
                  10, CARVED, vis=(1,), smooth=True)
        solids.append(xf(b, t=(x0, 0.0, 0.0)))
        b2 = lathe([(0.0, -0.08), (r * 1.75, -0.08), (r * 1.6, 0.1), (r * 1.08, 0.22), (0.0, 0.22)], 6, CARVED, vis=(2,),
                   smooth=False)
        solids.append(xf(b2, t=(x0, 0.0, 0.0)))
        cols.append(cyl_col(r * 1.7, 0.0, 0.20, n=8, cx=x0, mat=CARVED))
    # tie-beam: rectangular, through the posts, projecting
    nh, nd = F["nuki"]
    ny1 = F["nuki_y"]
    ny0 = ny1 - nh
    xp = S / 2 - lean * (ny0 + nh / 2) / ky_post
    xe = xp + F["proj"]
    solids.append(W(-xe, xe, ny0, ny1, -nd / 2, nd / 2, CARVED, vis=(1, 2, 3)))
    sw = r * 0.9
    strut = W(-sw / 2, sw / 2, ny1, kmin + 0.01, -nd * 0.4, nd * 0.4, CARVED, vis=(1, 2))
    solids.append(strut)
    # donor text: carved on the front of the right-hand post as seen from the approach (the -x post: a viewer facing
    # the torii from +z has -x on the right in DayZ's left-handed frame), the date column + the donor column
    fz = r * 0.98 * math.cos(math.pi / 8)
    xr = -(S / 2 - lean * 0.45)
    cw = 0.62 * 2 * r * math.sin(math.pi / 8)
    solids.append(K.carved((xr, 1.08, fz), X, Y, 0.74 * H / 2.71, F["text"], wear=wear, crop=(0.0, 0.0, 0.45, 1.0)
                           if F["text"] == "hono_genroku10" else (0.34, 0.0, 0.66, 1.0), width=cw, off=0.004))
    solids.append(K.carved((-xr, 1.30, fz), X, Y, 0.34 * H / 2.71, F["text"], wear=wear,
                           crop=(0.5, 0.15, 1.0, 0.65) if F["text"] == "hono_genroku10" else (0.66, 0.0, 1.0, 0.45),
                           width=cw, off=0.004))
    cols.append(col(-xp + r * 0.95, xp - r * 0.95, ny0, ny1, -nd / 2, nd / 2, CARVED))
    for sx in (-1, 1):
        a, b = sorted((sx * (xp + r), sx * xe))
        cols.append(col(a, b, ny0, ny1, -nd / 2, nd / 2, CARVED))
    kcol = col(-L / 2, L / 2, ky_post + 0.021, kmax, -kd / 2, kd / 2, CARVED)
    scol = col(-sw / 2, sw / 2, ny1, ky_post + 0.02, -nd * 0.4, nd * 0.4, CARVED)
    # lichen streaks under the kasagi are in the _w2 stone; moss on the kasagi top (mossy variants: thick, else a hint)
    kas_top = [(x, y + kh / 2, 0.0) for x, y in cl]
    if moss:
        solids.append(K.moss_strip(kas_top, kd * 0.9, seed=31, wear="_w2", frac=(0.05, 0.48)))
        solids.append(K.moss_strip(kas_top, kd * 0.8, seed=32, wear="_w2", frac=(0.52, 0.96)))
        solids.append(K.moss_strip([(-xe + 0.02, ny1, 0.0), (-xp, ny1, 0.0), (0.0, ny1, 0.0), (xp, ny1, 0.0)], nd * 0.9,
                                   seed=33, wear="_w1"))
        for sx in (-1, 1):
            solids += K.moss_foot(sx * S / 2, 0.0, r, 0.45, n=8, sides=3, seed=34 + sx, wear="_w2", y0=0.18)
            solids.append(moss_top(36 + sx, sx * S / 2, -r * 0.6, r * 1.2, 0.221, wear="_w2", sx=1.2, sz=0.6))
    else:
        solids.append(K.moss_strip(kas_top, kd * 0.5, seed=37, wear="_w0", frac=(0.3, 0.55)))
    rope_y = ny0 - 0.05
    rope_z = nd / 2 + 0.06
    rr_ = 0.05 if size != "l" else 0.07
    if rope and not ab:
        solids += K.torii_rope(-xp + r, xp - r, rope_y, rope_z, r=rr_, drop=0.10 * S / 1.82,
                               with_shide=rope == ROPE_SHIDE, wear="_w2", seed=40 + rope)
        for sx in (-1, 1):
            ring = xf(lathe([(r + rr_ * 0.7, rope_y - rr_), (r + rr_ * 0.7, rope_y + rr_)], 8, ROPE, vis=(1,)),
                      t=(sx * xp, 0.0, 0.0))
            ring.wear = "_w2"
            solids.append(ring)
    if ab == "broken":
        # the kasagi broke at its middle and fell in front of the posts (two pieces, each kasagi + shimaki); the strut
        # lies beside them
        rest_ = [s for s in solids if not any(s is q for q in kas_group) and s is not strut
                 and not (s.mats == MOSS and s.bbox()[2] > kmin - 0.05)]
        out = []
        for half, sl in ((0, slice(0, 5)), (1, slice(4, 9))):
            sgn = -1 if half == 0 else 1
            kc, sc = cl[sl], scl[sl]
            pc = [K.sweep(kc, kh, kd, CARVED, vis=(1,), top_w=kd * 1.12), K.sweep(kc[::2], kh, kd, CARVED, vis=(2,)),
                  K.sweep([kc[0], kc[-1]], kh, kd, CARVED, vis=(3,)), K.sweep(sc, sh_h, kd * 0.82, CARVED, vis=(1,)),
                  K.sweep(sc[::2], sh_h, kd * 0.82, CARVED, vis=(2,))]
            xs = [v[0] for q in pc for v in q.verts]
            ys = [v[1] for q in pc for v in q.verts]
            pc.append(col(min(xs), max(xs), min(ys), max(ys), -kd / 2, kd / 2, CARVED))   # the piece's collision box
            cx = sum(p[0] for p in kc) / len(kc)
            pc = xfs(pc, t=(-cx, -(H - kh / 2), 0.0))
            pc = xfs(pc, rx=(78.0 if half == 0 else 4.0), ry=sgn * 14.0 + (6.0 if half else -4.0))
            lo = min(v[1] for s in pc if s.vis for v in s.verts)
            pc = xfs(pc, t=(sgn * (L / 4 + 0.15), -lo - 0.07, 1.10 + 0.30 * half))
            out.append(pc)
        st = xf(xf(strut, t=(0.0, -ny1, 0.0)), rz=88.0, ry=30.0)
        lo = min(v[1] for v in st.verts)
        st = xf(st, t=(0.35, -lo - 0.03, 0.40))
        solids = rest_ + out[0] + out[1] + [st]
        solids.append(litter(41, 0.0, 1.0, 1.2, sx=1.6))
        P.notes.append("abandoned (rare, a landmark oddity): kasagi fallen in two pieces in front of the posts")
    else:
        cols += [kcol, scol]
    K.aged_stone(solids, 9100 + int(H * 100) + rope * 7 + (3 if moss else 0))   # FP1: no repeating lichen dots
    add_all(P, solids + cols)
    P.dim("post_span", S, S, tol=0.005)
    P.dim("height", H, H, tol=0.01)
    P.dim("post_d", 2 * r, 2 * r, tol=0.001)
    P.extra.update({"rope_y": round(rope_y, 3), "rope_z": round(rope_z, 3), "rope_span": round(2 * (xp - r), 3),
                    "rope": ["none", "rope", "rope+shide"][rope], "moss": moss,
                    "donor_text": F["text"]})
    return P


# ================================================================================================ registry
def TW(sfx, form, rope=0, moss=False, shu=False, ab=None, plaque=None, display="", mount="shrine"):
    st = "abandoned" if ab else "intact"
    return M("jp_s_torii_wood_" + sfx, form, st, display,
             lambda: torii_wood(form, rope=rope, moss=moss, shu=shu, ab=ab, plaque=plaque), mount=mount)


def TS(sfx, size, rope=0, moss=False, ab=None, display=""):
    st = "abandoned" if ab else "intact"
    return M("jp_s_torii_stone_" + sfx, size, st, display, lambda: torii_stone(size, rope=rope, moss=moss, ab=ab),
             mount="shrine")


R0, R1, R2 = ROPE_NONE, ROPE_ONLY, ROPE_SHIDE
HM = "gaku_hachimangu"
PROPS = [
    {"id": "jp_s_torii_wood", "cat": "shrine", "mount": "shrine", "per_row": 5,
     "notes": ["vermilion (_myojin_shu*, _mini_shu) ONLY at Inari and Hachiman shrines; mini torii only before a yard "
               "shrine (mount 'yard')", "rope variants carry the straw rope on the tie-beam; '_shide' adds 4-step "
               "zigzag paper streamers (W2_ERA T1-T3)", "mossy variants for rural shrines (W2_ERA T5)",
               "a village shrine gets a wooden or a stone torii, not both"],
     "models": [
         TW("shinmei", "shinmei", display="Wooden torii, shinmei (straight), 1 ken"),
         TW("shinmei_rope", "shinmei", R1, display="Wooden shinmei torii with a straw rope"),
         TW("shinmei_rope_shide", "shinmei", R2, display="Wooden shinmei torii, straw rope and paper shide"),
         TW("shinmei_moss", "shinmei", moss=True, display="Wooden shinmei torii, mossy (rural)"),
         TW("shinmei_moss_rope", "shinmei", R1, moss=True, display="Wooden shinmei torii, mossy, straw rope"),
         TW("shinmei_moss_rope_shide", "shinmei", R2, moss=True, display="Wooden shinmei torii, mossy, rope and shide"),
         TW("myojin", "myojin", plaque=HM, display="Wooden torii, myojin (upswept), 1.5 ken, plaque"),
         TW("myojin_rope", "myojin", R1, plaque=HM, display="Wooden myojin torii with a straw rope"),
         TW("myojin_rope_shide", "myojin", R2, plaque=HM, display="Wooden myojin torii, straw rope and paper shide"),
         TW("myojin_moss", "myojin", moss=True, plaque="blank", display="Wooden myojin torii, mossy (rural)"),
         TW("myojin_moss_rope", "myojin", R1, moss=True, plaque="blank", display="Wooden myojin torii, mossy, rope"),
         TW("myojin_moss_rope_shide", "myojin", R2, moss=True, plaque="blank",
            display="Wooden myojin torii, mossy, rope and shide"),
         TW("myojin_shu", "myojin", shu=True, plaque="gaku_inari",
            display="Vermilion myojin torii, black kasagi (Inari / Hachiman only)"),
         TW("myojin_shu_rope_shide", "myojin", R2, shu=True, plaque="gaku_inari",
            display="Vermilion myojin torii with rope and shide (Inari / Hachiman only)"),
         TW("mini", "mini", display="Miniature wooden torii (yard shrine)", mount="yard"),
         TW("mini_shu", "mini", shu=True, display="Miniature vermilion torii (Inari yard shrine)", mount="yard"),
         TW("mini_rope", "mini", R2, display="Miniature torii with a straw rope and shide (yard shrine)", mount="yard"),
         TW("ab_leaning", "myojin", R1, moss=True, ab="leaning", plaque="blank",
            display="Wooden myojin torii leaning on a rotted post, rope dropped"),
         TW("ab_leaning_shu", "myojin", R2, shu=True, ab="peeled", plaque="gaku_inari",
            display="Vermilion torii peeled to grey, leaning, rope dropped"),
         TW("ab_rotted", "shinmei", R1, moss=True, ab="rotted",
            display="Wooden shinmei torii, kasagi slipped off one post, rope dropped"),
     ]},
    {"id": "jp_s_torii_stone", "cat": "shrine", "mount": "shrine", "per_row": 5,
     "notes": ["donor text on the right-hand post (carved-text atlas: 1682 village / 1697)",
               "mossy variants only for the small village size (W2_ERA T5)", "_ab_broken is rare: a landmark oddity"],
     "models": [
         TS("s", "s", display="Stone torii, span 1.82 (village)"),
         TS("s_rope", "s", R1, display="Stone torii 1.82 with a straw rope"),
         TS("s_rope_shide", "s", R2, display="Stone torii 1.82, straw rope and shide"),
         TS("s_moss", "s", moss=True, display="Stone torii 1.82, mossy (rural)"),
         TS("s_moss_rope_shide", "s", R2, moss=True, display="Stone torii 1.82, mossy, rope and shide"),
         TS("m", "m", display="Stone torii, span 2.5"),
         TS("m_rope_shide", "m", R2, display="Stone torii 2.5, straw rope and shide"),
         TS("l", "l", display="Stone torii, span 3.6 (town)"),
         TS("l_rope_shide", "l", R2, display="Stone torii 3.6, straw rope and shide"),
         TS("ab_broken", "m", ab="broken", display="Stone torii, kasagi fallen in two pieces (quake)"),
     ]},
]
