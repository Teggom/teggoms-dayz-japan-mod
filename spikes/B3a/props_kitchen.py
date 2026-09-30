"""Kitchen, hearth and water props (BUILD_LIST rows 14-20): kama, jizai-kagi, mizugame, oke, tana, firewood, jar.

Reuse by B3b (outdoor kit): firewood.stack / firewood.bundle and oke.* take their size and materials as
arguments; call them with outdoor sizes and the weathered wear (see B3a_PROGRESS.md, 'Reuse').
"""
import math
import random

import fkit
import bits
from fkit import (core, box, prism, ngon, sheet, lathe, xf, xfs, flat_poly, W, col, cyl_col, board, FPart,
                  WOOD, IRON, DARK, PALE, HOOP, SOOT_BAMBOO, SOOT_WOOD, RIVER, LOGWOOD, ENDGRAIN, TAWARA, ASH,
                  LITTER)
from bits import disc, jag_rim, shards, stain, rope_ring

CAT = "kitchen"


def ground_to_floor(P):
    """Shift every solid so the lowest visual vertex sits on y = 0 (after a tip-over)."""
    lo = min(v[1] for s in P.solids for v in s.verts)
    if abs(lo) > 1e-6:
        P.solids = [xf(s, t=(0.0, -lo, 0.0)) for s in P.solids]
    return P


def add_all(P, ss):
    for s in ss:
        P.add(s)


# ================================================================================================ kama / nabe
def kama_body(wear=None, crust=False):
    """Rice pot (hagama): rounded bottom, the flange (ha) at 0.17 that seats it in a kamado rim, mouth d 0.38."""
    prof = [(0.0, 0.0), (0.11, 0.006), (0.175, 0.03), (0.205, 0.08), (0.212, 0.165), (0.252, 0.168), (0.252, 0.182),
            (0.206, 0.19), (0.194, 0.272), (0.198, 0.28), (0.178, 0.28), (0.176, 0.20), (0.15, 0.10), (0.0, 0.08)]
    out = [lathe(prof, 14, IRON, vis=(1,), wear=wear)]
    out.append(lathe([(0.0, 0.0), (0.21, 0.08), (0.25, 0.175), (0.195, 0.28), (0.0, 0.26)], 8, IRON, vis=(2,),
                     wear=wear))
    if crust:
        out.append(disc(0.12, 0.078, 0.083, ASH, n=8, vis=(1,), wear="_w2"))
    return out


def kama_lid(wear=None):
    out = [disc(0.23, 0.0, 0.04, WOOD, n=12, vis=(1, 2), wear=wear)]
    for x in (-0.09, 0.09):
        out.append(W(x - 0.018, x + 0.018, 0.04, 0.065, -0.17, 0.17, vis=(1,)))
    return out


def kama(state="intact"):
    P = FPart("kama", budget="small", mass=9.0)
    rust = "_w2" if state != "intact" else None
    add_all(P, kama_body(rust, crust=state != "intact"))
    if state == "intact":
        add_all(P, xfs(kama_lid(), t=(0.0, 0.28, 0.0)))
        top = 0.28 + 0.065
        P.add(cyl_col(0.23, 0.0, 0.32, n=8, mat=IRON))
    else:
        # lid knocked off: on the floor, leaning on the pot's belly
        lid = xfs(kama_lid(wear="_w2"), rx=-70.0, t=(0.0, 0.0, 0.0))
        add_all(P, fkit.rest(xfs(lid, ry=20.0, t=(0.14, 0.0, 0.52))))
        P.add(cyl_col(0.23, 0.0, 0.28, n=8, mat=IRON))
    P.dim("body_d", 0.42, 0.424, tol=0.01)
    P.dim("flange_d", 0.50, 0.504, tol=0.02)
    P.extra["seat_y"] = 0.168
    P.notes.append("seat_y 0.168: the flange underside; place the proxy at kamado rim top - 0.168 (rim hole d 0.44)")
    return P


def nabe_parts(wear=None, lid=True, crust=False, bail_up=True, vis_l2=True):
    prof = [(0.0, 0.0), (0.09, 0.004), (0.13, 0.03), (0.14, 0.10), (0.138, 0.16), (0.126, 0.16), (0.124, 0.06),
            (0.0, 0.05)]
    out = [lathe(prof, 12, IRON, vis=(1,), wear=wear)]
    if vis_l2:
        out.append(lathe([(0.0, 0.0), (0.14, 0.05), (0.138, 0.16), (0.0, 0.15)], 7, IRON, vis=(2,), wear=wear))
    # lugs + bail handle (an iron wire arc over the top)
    for sx in (-1, 1):
        out.append(box(sx * 0.138, sx * 0.152, 0.125, 0.155, -0.012, 0.012, IRON, vis=(1,)))
    ang = [math.radians(a) for a in range(0, 181, 30)]
    R = 0.148
    pts = [(R * math.cos(a), 0.15 + 0.14 * math.sin(a), 0.0) for a in ang]
    bail = []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        c = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)
        L = core.length(core.sub(b, a))
        seg = box(-L / 2, L / 2, -0.004, 0.004, -0.004, 0.004, IRON, vis=(1,))
        bail.append(xf(seg, rz=math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), t=c))
    if not bail_up:          # dropped over the side, resting on the body
        bail = xfs(bail, rx=-105.0, pivot=(0.0, 0.15, 0.0))
    out += bail
    if lid:
        out.append(disc(0.125, 0.16, 0.18, WOOD, n=10, vis=(1, 2)))
        out.append(W(-0.012, 0.012, 0.18, 0.2, -0.07, 0.07, vis=(1,)))
    if crust:
        out.append(disc(0.08, 0.05, 0.054, ASH, n=7, vis=(1,), wear="_w2"))
    for s in out:
        if wear and not getattr(s, "wear", None) and s.fm and s.fm[0] == IRON:
            s.wear = wear
    return out


def nabe(state="intact"):
    P = FPart("nabe", budget="small", mass=3.0)
    rust = "_w2" if state != "intact" else None
    add_all(P, nabe_parts(rust, lid=state == "intact", crust=state != "intact", bail_up=state == "intact"))
    P.add(cyl_col(0.14, 0.0, 0.16 if state != "intact" else 0.18, n=8, mat=IRON))
    ground_to_floor(P)
    P.dim("body_d", 0.28, 0.28, tol=0.01)
    P.dim("height", 0.16, 0.16, tol=0.01)
    return P


# ================================================================================================ jizai-kagi
L_TUBE = (-0.07, -0.95)       # bamboo tube (top, bottom), metres below the hook beam
HOOK_Y = -1.50                # hook bottom: 1.50 below the beam (build list 1.2-1.8)


def fish(y, x_off=0.0, wood_wear=None):
    """Yokogi, the fish-shaped lever: body (convex outline) + tail, extruded 0.05 in z; 0.35 x 0.10."""
    body = [(-0.10, 0.0), (-0.06, 0.045), (0.04, 0.05), (0.13, 0.025), (0.15, 0.0), (0.13, -0.025), (0.04, -0.05),
            (-0.06, -0.045)]
    tail = [(-0.10, 0.0), (-0.20, 0.05), (-0.17, 0.0), (-0.20, -0.05)]
    out = []
    for poly in (body, core.hull2d(tail[:2] + tail[3:] + [tail[0]])):
        p = prism([(a + x_off, b + y) for a, b in poly], "z", -0.025, 0.025, SOOT_WOOD, vis=(1, 2), uv="fit")
        out.append(p)
    eye = box(0.085 + x_off, 0.10 + x_off, y + 0.008, y + 0.02, -0.026, 0.026, IRON, vis=(1,))
    out.append(eye)
    for s in out[:2]:
        if wood_wear:
            s.wear = wood_wear
    return out


def jizai(kind="std", state="intact"):
    P = FPart("jizai", budget="small", anchor="hang", flat=True)
    ab = state != "intact"
    out = []
    # top hook over the beam + rope loop (iron)
    out.append(box(-0.008, 0.008, -0.07, 0.0, -0.008, 0.008, IRON, vis=(1, 2)))
    out.append(box(-0.03, 0.03, -0.075, -0.06, -0.01, 0.01, IRON, vis=(1,)))
    # bamboo tube (sooted), with node rings
    out.append(fkit.lcyl("y", 0.0, 0.0, 0.026, L_TUBE[1], L_TUBE[0], SOOT_BAMBOO, n=8, vis=(1, 2),
                         caps=SOOT_BAMBOO))
    for y in (-0.30, -0.62):
        out.append(rope_ring(0.026, y, 0.012, SOOT_BAMBOO, 8, proud=0.003))
    # the iron hook rod slides out of the tube
    out.append(box(-0.007, 0.007, HOOK_Y + 0.10, L_TUBE[1] + 0.02, -0.007, 0.007, IRON, vis=(1, 2)))
    # J hook
    for (x0, x1, y0, y1) in ((-0.007, 0.007, HOOK_Y, HOOK_Y + 0.10), (0.007, 0.06, HOOK_Y, HOOK_Y + 0.014),
                             (0.046, 0.06, HOOK_Y, HOOK_Y + 0.06)):
        out.append(box(x0, x1, y0, y1, -0.007, 0.007, IRON, vis=(1, 2)))
    # lever: the rope from the tube top passes through it; std = fish, plain = bar
    ly = -0.14 if ab else -0.42             # abandoned: jammed high
    if kind == "std":
        out += [xf(s, t=(0.0, 0.0, 0.033)) for s in fish(ly, wood_wear="_w2" if ab else None)]
    else:
        lev = box(-0.16, 0.16, ly - 0.02, ly + 0.02, 0.013, 0.053, SOOT_WOOD, vis=(1, 2))
        if ab:
            lev.wear = "_w2"
        out.append(lev)
    if ab:
        # a rusted nabe left on the hook: its bail apex on the hook bottom
        pot = nabe_parts("_w2", lid=False, crust=True, bail_up=True, vis_l2=False)
        out += xfs(pot, t=(0.053, HOOK_Y + 0.004 - 0.29, 0.0))
    add_all(P, out)
    tube = abs(L_TUBE[1] - L_TUBE[0])
    P.dim("length", 1.50, abs(HOOK_Y), tol=0.01)
    P.dim("lever_len", 0.35 if kind == "std" else 0.32, 0.35 if kind == "std" else 0.32, tol=0.01)
    P.notes.append("hangs from the hook beam of jp_p_fit_irori: origin = beam underside; no Geometry (BUILD_LIST); "
                   "keep >= 2.00 head room except over the pit. Hook bottom 1.50 below the beam (list 1.2-1.8)")
    return P


# ================================================================================================ mizugame
MZ_D, MZ_H = 0.55, 0.60


def mz_profile(broken=False):
    """Big stoneware water jar (kame): narrow foot, full belly, rounded shoulder, thick rolled lip, deep inside."""
    R = MZ_D / 2
    return [(0.0, 0.0), (0.60 * R, 0.0), (0.66 * R, 0.03), (0.82 * R, 0.12), (0.95 * R, 0.24), (R, 0.34),
            (0.98 * R, 0.43), (0.91 * R, 0.51), (0.82 * R, 0.565), (0.84 * R, 0.585), (0.88 * R, MZ_H - 0.004),
            (0.84 * R, MZ_H), (0.76 * R, MZ_H - 0.01), (0.74 * R, 0.52), (0.84 * R, 0.36), (0.70 * R, 0.12),
            (0.0, 0.08)]


def dipper(wear=None):
    """Hishaku: a wooden cup d 0.09, h 0.08 on a 0.45 m handle; lying with the cup at +x."""
    cup = lathe([(0.0, 0.0), (0.045, 0.0), (0.045, 0.08), (0.038, 0.08), (0.038, 0.01), (0.0, 0.01)], 8, WOOD,
                vis=(1,))
    cup = xf(cup, rz=90.0, t=(0.0, 0.045, 0.0))   # lying on its side, mouth to -x? (rotates +y to -x)
    handle = box(0.0, 0.45, 0.035, 0.05, -0.008, 0.008, fkit.HOOP, vis=(1,))
    out = [cup, handle]
    for s in out:
        if wear:
            s.wear = wear
    return out


def mz_lid(wear=None):
    r = 0.30
    out = [disc(r, 0.0, 0.03, WOOD, n=12, vis=(1, 2), wear=wear)]
    out.append(W(-0.02, 0.02, 0.03, 0.055, -0.18, 0.18, vis=(1,)))          # the grip batten
    return out


def mizugame(state="lid"):
    P = FPart("mizugame", budget="small", mass=35.0)
    ab = state != "lid"
    body = lathe(mz_profile(), 12, DARK, vis=(1,), wear="_w2" if ab else None)
    if state == "broken":
        jag_rim(body, MZ_H, 0.004, 7, drop=(0.5, 1.45, 0.20))
    P.add(body)
    P.add(lathe([(0.0, 0.0), (0.26, 0.06), (0.275, 0.34), (0.25, MZ_H), (0.0, MZ_H - 0.02)], 8, DARK, vis=(2,),
                wear="_w2" if ab else None))
    if state == "lid":
        add_all(P, xfs(mz_lid(), t=(0.0, MZ_H, 0.0)))
        add_all(P, xfs(dipper(), ry=-30.0, t=(-0.10, MZ_H + 0.03, 0.08)))
        P.add(cyl_col(0.275, 0.0, MZ_H + 0.03, n=10, mat=DARK))
        P.loot_rect("lid", MZ_H + 0.03, -0.2, 0.2, -0.2, 0.2, rng=0.2, points=[(0.10, MZ_H + 0.03, -0.14)])
    else:
        P.add(cyl_col(0.275, 0.0, MZ_H, n=10, mat=DARK))
        if state == "open":
            lid = xfs(mz_lid(wear="_w2"), rx=-72.0)
            add_all(P, fkit.rest(xfs(lid, ry=-35.0, t=(0.30, 0.0, 0.38))))
            add_all(P, fkit.rest(xfs(dipper("_w2"), ry=150.0, t=(-0.30, 0.0, 0.42))))
        else:
            # the broken-out piece on the floor, a few chips, a dried stain
            piece = lathe([(0.262, 0.0), (0.275, 0.10), (0.265, 0.18), (0.255, 0.18), (0.265, 0.10), (0.252, 0.0),
                           (0.262, 0.0)], 14, DARK, vis=(1,), wear="_w2", phase=-math.pi / 14 - 2 * math.pi / 14)
            piece.finalize()
            keep = [i for i in range(len(piece.faces)) if abs(math.atan2(sum(p[2] for p in piece.face_points(i)),
                                                                         sum(p[0] for p in piece.face_points(i)))) < 0.5]
            piece.faces = [piece.faces[i] for i in keep]
            piece.fn = [piece.fn[i] for i in keep]
            piece.fuv = [piece.fuv[i] for i in keep]
            piece.fm = [piece.fm[i] for i in keep]
            piece.vn = [piece.vn[i] for i in keep]
            piece.normals = piece.fn
            pc = xf(piece, rz=-80.0, pivot=(0.26, 0.0, 0.0))
            add_all(P, fkit.rest(xfs([pc], ry=-50.0, t=(0.15, 0.0, 0.25))))
            add_all(P, shards(11, 0.05, 0.40, 0.12, 5, DARK, wear="_w2"))
            P.add(stain(5, 0.10, 0.45, 0.28, sx=1.3))
            add_all(P, xfs(mz_lid(wear="_w2"), rx=0.0, ry=15.0, t=(0.62, 0.0, -0.05)))
            P.add(col(0.32, 0.92, 0.0, 0.03, -0.35, 0.25))
    P.dim("jar_d", MZ_D, MZ_D, tol=0.01)
    P.dim("jar_h", MZ_H, max(v[1] for s in P.solids if s.fm and s.fm[0] == DARK and 1 in s.vis for v in s.verts)
          if state != "broken" else MZ_H, tol=0.01)
    return P


# ================================================================================================ oke
def tub_profile(r_bot, r_top, h, wall=0.013, bottom=0.03, foot=0.012):
    """Coopered tub: staves stand on a short foot ring; the bottom board sits `bottom` up inside."""
    return [(0.0, foot), (r_bot - wall, foot), (r_bot, 0.0), (r_bot + 0.002, 0.0), (r_top, h), (r_top - wall, h),
            (r_bot - wall + (r_top - r_bot) * bottom / h, bottom), (0.0, bottom)]


def hoops(r_bot, r_top, h, ys, n, width=0.022, wear=None):
    out = []
    for y in ys:
        r = r_bot + (r_top - r_bot) * y / h
        s = rope_ring(r + 0.002, y, width, HOOP, n, proud=0.007)
        if wear:
            s.wear = wear
        out.append(s)
    return out


def bucket_parts(wear=None):
    rb, rt, h = 0.14, 0.15, 0.30
    out = [lathe(tub_profile(rb, rt, h), 12, WOOD, vis=(1,), wear=wear)]
    out.append(lathe([(0.0, 0.0), (rb, 0.0), (rt, h), (0.0, h - 0.02)], 8, WOOD, vis=(2,), wear=wear))
    out += hoops(rb, rt, h, (0.05, 0.24), 12, wear=wear)
    # two long staves (ears) up to 0.45 with the cross handle
    for sx in (-1, 1):
        e = W(-0.028, 0.028, h - 0.04, 0.45, -0.007, 0.007, vis=(1, 2))
        out.append(xf(e, ry=90.0, t=(sx * (rt - 0.006), 0.0, 0.0)))
    out.append(W(-rt - 0.01, rt + 0.01, 0.39, 0.415, -0.013, 0.013, vis=(1, 2)))
    for s in out:
        if wear:
            s.wear = wear
    return out


def oke(kind="bucket", state="intact"):
    ab = state != "intact"
    wear = "_w2" if ab else None
    P = FPart("oke", budget="small", mass={"bucket": 2.5, "tarai": 5.0, "pickle": 25.0}[kind])
    if kind == "bucket":
        parts = bucket_parts(wear)
        if state == "tipped":
            parts = xfs(parts, rx=90.0)          # on its side, mouth to the front
            parts = xfs(parts, ry=-25.0, t=(0.0, 0.0, 0.0))
            add_all(P, parts)
            c = xf(cyl_col(0.15, 0.0, 0.30, n=8), rx=90.0)
            P.add(xf(c, ry=-25.0))
            ground_to_floor(P)
            # a dried water stain spilling out of the mouth
            P.add(stain(3, 0.14, 0.30, 0.22, sx=1.2))
        else:
            add_all(P, parts)
            P.add(cyl_col(0.15, 0.0, 0.30, n=8))
        P.dim("d", 0.30, 0.30, tol=0.01)
        P.dim("ears", 0.45, 0.45, tol=0.01)
    elif kind == "tarai":
        rb, rt, h = 0.27, 0.30, 0.20
        skip = (3,) if ab else ()
        body = lathe(tub_profile(rb, rt, h), 16, WOOD, vis=(1,), wear=wear, skip=skip)
        if ab:
            jag_rim(body, h, 0.015, 21)
        P.add(body)
        P.add(lathe([(0.0, 0.0), (rb, 0.0), (rt, h), (0.0, 0.03)], 8, WOOD, vis=(2,), wear=wear))
        if ab:
            # a gap where a stave fell out (cheeks close it), the stave on the floor, the top hoop slipped off
            a0 = math.pi / 16 + 2 * math.pi * 3 / 16
            a1 = a0 + 2 * math.pi / 16
            for a in (a0, a1):
                q = [(rb * math.cos(a), 0.0, rb * math.sin(a)), (rt * math.cos(a), h - 0.015, rt * math.sin(a)),
                     ((rt - 0.013) * math.cos(a), h - 0.015, (rt - 0.013) * math.sin(a)),
                     ((rb - 0.013) * math.cos(a), 0.03, (rb - 0.013) * math.sin(a))]
                n = (-math.sin(a), 0.0, math.cos(a)) if a == a0 else (math.sin(a), 0.0, -math.cos(a))
                P.add(sheet([q, q[::-1]], WOOD, [n, core.mul(n, -1.0)], vis=(1,)))
            st = W(-0.05, 0.05, 0.0, 0.014, -0.10, 0.10, vis=(1,))
            st.wear = "_w2"
            P.add(xf(st, ry=30.0, t=(0.46, 0.0, 0.22)))
            P.add(hoops(rb, rt, h, (0.05,), 16, wear=wear)[0])
            hp = rope_ring(0.31, 0.0, 0.022, HOOP, 16, proud=0.007)
            hp.wear = "_w2"
            add_all(P, fkit.rest([xf(hp, rx=6.0, t=(0.05, 0.0, 0.03))], 0.001))
            P.add(stain(9, 0.0, 0.0, 0.40, sx=1.1))
        else:
            add_all(P, hoops(rb, rt, h, (0.05, 0.16), 16))
            P.loot_rect("bottom", 0.03, -0.2, 0.2, -0.2, 0.2, rng=0.25, kind="floor", points=[(0.0, 0.03, 0.0)])
        # collision: the bottom slab + four low walls (the loot point sits inside)
        P.add(col(-0.25, 0.25, 0.0, 0.03, -0.25, 0.25))
        for sx in (-1, 1):
            P.add(col(sx * 0.255, sx * 0.30, 0.0, h, -0.20, 0.20))
            P.add(col(-0.20, 0.20, 0.0, h, sx * 0.255, sx * 0.30))
        P.dim("d", 0.60, 0.60, tol=0.01)
        P.dim("h", 0.20, 0.20, tol=0.01)
    else:   # pickle tub
        rb, rt, h = 0.215, 0.225, 0.50
        P.add(lathe(tub_profile(rb, rt, h), 12, WOOD, vis=(1,), wear=wear))
        P.add(lathe([(0.0, 0.0), (rb, 0.0), (rt, h), (0.0, h - 0.02)], 8, WOOD, vis=(2,), wear=wear))
        add_all(P, hoops(rb, rt, h, (0.06, 0.25, 0.44), 12, wear=wear))
        rng = random.Random(4)
        lid = [disc(0.235, 0.0, 0.05, WOOD, n=12, vis=(1, 2), wear=wear)]
        stone = core.stone(rng, 0.0, 0.0, 0.20, 0.17, 0.13, 0.13, RIVER, bury=0.0, n=8, vis=(1, 2))
        if state == "intact":
            add_all(P, xfs(lid, t=(0.0, h, 0.0)))
            P.add(xf(stone, t=(-0.05, h + 0.05, -0.03)))
            P.add(cyl_col(0.225, 0.0, h + 0.05, n=8))
            P.add(fkit.col_solid(xf(stone, t=(-0.05, h + 0.05, -0.03)), RIVER))
            P.loot_rect("lid", h + 0.05, -0.2, 0.2, -0.2, 0.2, rng=0.15, points=[(0.13, h + 0.05, 0.09)])
        else:
            # lid off, leaning; the stone on the floor; a dark crust inside
            add_all(P, fkit.rest(xfs(xfs(lid, rx=-75.0), ry=40.0, t=(0.40, 0.0, 0.34))))
            P.add(xf(stone, t=(-0.38, 0.0, 0.18)))
            P.add(disc(0.19, 0.031, 0.036, ASH, n=10, vis=(1,), wear="_w2"))
            P.add(cyl_col(0.225, 0.0, h, n=8))
            P.add(fkit.col_solid(xf(stone, t=(-0.38, 0.0, 0.18)), RIVER))
        ground_to_floor(P)
        P.dim("d", 0.45, 0.45, tol=0.01)
        P.dim("h", 0.50, 0.50, tol=0.01)
    return P


# ================================================================================================ tana (wall shelf)
TANA_Y = (0.90, 1.30, 1.70)
TANA_D = 0.30


def bowl(cx, cz, y, r=0.06, h=0.055, mat=PALE, tipped=False, wear=None, n=8):
    b = lathe([(0.0, 0.0), (r * 0.5, 0.0), (r * 0.55, 0.008), (r, h), (r * 0.9, h), (0.0, 0.012)], n, mat, vis=(1,))
    if tipped:
        b = xf(b, rx=180.0, t=(0.0, h, 0.0))
    b = xf(b, t=(cx, y, cz))
    if wear:
        b.wear = wear
    return b


def tana(width=0.91, boards=1, state="intact"):
    P = FPart("tana", budget="furniture", res3=True, mass=6.0 * boards, anchor="wall")
    ab = state != "intact"
    ys = TANA_Y[:boards]
    brk = [-width / 2 + 0.07, width / 2 - 0.07] + ([0.0] if width > 1.5 else [])
    sag_board = 0 if boards == 1 else 1           # which board drops
    x0, x1 = -width / 2, width / 2
    for bi, y in enumerate(ys):
        sag = ab and bi == sag_board
        bd = board(x0, x1, y - 0.025, y, 0.0, TANA_D, k=bi * 3 + 1, vis=(1, 2))
        far = W(x0, x1, y - 0.025, y, 0.0, TANA_D, vis=(3,))
        cb = col(x0, x1, y - 0.025, y, 0.0, TANA_D)
        if sag:
            # the bracket at x0 is gone: the board hangs from its x1 end, the x0 end dropped 0.30
            ang = math.degrees(math.asin(0.30 / width))
            piv = (x1 - 0.07, y, 0.0)
            bd, far, cb = (xf(s, rz=ang, pivot=piv) for s in (bd, far, cb))
            bd.wear = "_w2"
        P.add(bd)
        P.add(far)
        P.add(cb)
        for bx in brk:
            if sag and bx < -0.1:
                continue
            # bracket: wall cleat, arm under the board, diagonal brace (visual)
            P.add(W(bx - 0.02, bx + 0.02, y - 0.25, y - 0.025, 0.0, 0.03, vis=(1, 2)))
            P.add(W(bx - 0.018, bx + 0.018, y - 0.065, y - 0.025, 0.03, TANA_D - 0.03, vis=(1,)))
            br = W(-0.015, 0.015, -0.02, 0.02, -0.12, 0.12, vis=(1,))
            P.add(xf(br, rx=-45.0, t=(bx, y - 0.14, 0.12)))
        if not sag and y <= 1.40:
            P.loot_rect("board_%d" % (bi + 1), y, x0 + 0.05, x1 - 0.05, 0.03, TANA_D - 0.03, rng=0.18,
                        points=None)
    # dressing: a few bowls and a small jar on the top usable board; the abandoned one has most on the floor
    top = ys[-1] if not ab or boards > 1 else None
    dress_y = ys[-1] if boards > 1 else ys[0]
    if not ab:
        P.add(bowl(x1 - 0.12, 0.15, dress_y))
        P.add(bowl(x1 - 0.12, 0.15, dress_y + 0.035))
        js, jt = bits.jar(0.14, 0.17, DARK, n=8, lid=True, vis=(1,))
        add_all(P, xfs([js[0], js[1]], t=(x1 - 0.28, dress_y, 0.15)))
    else:
        if boards > 1:
            P.add(bowl(x1 - 0.12, 0.15, ys[0]))
        add_all(P, shards(31 + boards, 0.0, 0.45, 0.25, 7, PALE))
        P.add(bowl(x0 + 0.25, 0.55, 0.0, tipped=True))
        P.add(stain(17, 0.0, 0.45, 0.35, sx=1.4))
    P.dim("width", width, width, tol=0.005)
    P.dim("depth", TANA_D, TANA_D, tol=0.005)
    P.notes.append("wall-hung: origin on the floor, wall plane z = 0; loot only on boards <= 1.40 m (vanilla cap), so "
                   "the 1.70 board is dressing")
    if ab:
        P.notes.append("abandoned: one bracket gone, board %d hanging; shards, a bowl and a stain on the floor below "
                       "(visual, no Geometry)" % (sag_board + 1))
    return P


# ================================================================================================ firewood
def split_log(rng, cx, cy, r, z0, z1, mats=(LOGWOOD, ENDGRAIN), full=False, vis=(1, 2), wear=None):
    """One split log along z: a 3-5 sided convex section (quarters and halves of a round). full=False emits only
    the two end caps + the up-facing side faces (the rest is hidden in the stack)."""
    k = rng.choice((3, 4, 4, 5))
    a0 = rng.uniform(0, 2 * math.pi)
    pts = core.hull2d([(cx + r * rng.uniform(0.75, 1.0) * math.cos(a0 + 2 * math.pi * j / k),
                        cy + r * rng.uniform(0.75, 1.0) * math.sin(a0 + 2 * math.pi * j / k)) for j in range(k)])
    s = prism(pts, "z", z0, z1, {"front": mats[1], "back": mats[1], "default": mats[0]}, vis=vis)
    s.finalize()
    if not full:
        keep = [i for i in range(len(s.faces)) if abs(s.fn[i][2]) > 0.7 or s.fn[i][1] > 0.35]
        s.faces = [s.faces[i] for i in keep]
        s.fn = [s.fn[i] for i in keep]
        s.fm = [s.fm[i] for i in keep]
        s.fuv = [s.fuv[i] for i in keep]
        s.normals = s.fn
    if wear:
        s.wear = wear
    return s, pts


def stack(length=0.91, depth=0.40, height=0.60, log_d=(0.09, 0.13), seed=1, rows_keep=None, mats=(LOGWOOD, ENDGRAIN),
          core_mat=SOOT_WOOD, wear=None):
    """Firewood stack along x, logs along z (end grain to the front and back). Returns (solids, top_points,
    collision boxes). rows_keep: keep only that many rows (half used)."""
    rng = random.Random(seed)
    out, tops = [], []
    z0, z1 = -depth / 2, depth / 2
    rows = []
    y = 0.0
    while y < height - 0.05:
        dh = rng.uniform(*log_d)
        rows.append((y, min(dh, height - y)))
        y += dh * 0.92
    if rows_keep is not None:
        rows = rows[:rows_keep]
    top_y = 0.0
    for ri, (yb, dh) in enumerate(rows):
        x = -length / 2
        last = ri == len(rows) - 1
        while x < length / 2 - 0.03:
            dw = rng.uniform(*log_d)
            if x + dw > length / 2:
                dw = length / 2 - x
            r = min(dw, dh) / 2
            cx, cy = x + dw / 2, yb + dh / 2
            zj = rng.uniform(-0.03, 0.03)
            edge = last or x == -length / 2 or x + dw >= length / 2 - 1e-6
            s, pts = split_log(rng, cx, cy, r * 1.06, z0 + zj, z1 + zj, mats, full=edge, wear=wear, vis=(1,))
            out.append(s)
            if last:
                tops.append((cx, max(p[1] for p in pts)))
            top_y = max(top_y, max(p[1] for p in pts))
            x += dw
    # the dark core fills the gaps between log ends
    if rows:
        ytop = rows[-1][0] + rows[-1][1] * 0.55
        cs = W(-length / 2 + 0.02, length / 2 - 0.02, 0.0, ytop, z0 + 0.035, z1 - 0.035, core_mat, vis=(1,))
        cs.wear = "_w2"
        out.append(cs)
        out.append(W(-length / 2, length / 2, 0.0, ytop + rows[-1][1] * 0.3, z0, z1, mats[1], vis=(2,)))
    colbox = col(-length / 2, length / 2, 0.0, top_y - 0.02, z0 + 0.02, z1 - 0.02, mats[0])
    return out, tops, top_y, colbox


def firewood(kind="stack", state="intact"):
    P = FPart("firewood", budget="small", mass=35.0 if kind == "stack" else 12.0)
    if kind == "stack":
        ss, tops, ty, cb = stack(rows_keep=3 if state != "intact" else None, seed=3)
        add_all(P, ss)
        P.add(cb)
        # the highest log near the middle carries the loot point: a flat facet
        best = None
        for s in ss:
            if 1 not in s.vis:
                continue
            for fi in range(len(s.faces)):
                n = s.fn[fi]
                if n[1] > 0.97:
                    pts = s.face_points(fi)
                    cx = sum(p[0] for p in pts) / len(pts)
                    cz = sum(p[2] for p in pts) / len(pts)
                    y = pts[0][1]
                    if abs(cx) < 0.3 and (best is None or y > best[1]):
                        best = (cx, y, cz)
        if state == "intact":
            P.dim("stack", 0.91, 0.91, tol=0.01)
            P.dim("height", 0.60, ty, tol=0.03)
        else:
            rng = random.Random(8)
            for i in range(4):
                s, _ = split_log(rng, 0.0, 0.05, 0.05, -0.21, 0.21, full=True)
                s = xf(s, ry=rng.uniform(60, 120), t=(rng.uniform(-0.4, 0.4), 0.0, 0.45 + rng.uniform(-0.1, 0.15)))
                P.add(s)
            ground_to_floor(P)
            P.add(stain(12, 0.0, 0.40, 0.35, sx=1.6, wear="_w1"))
            P.dim("stack", 0.91, 0.91, tol=0.01)
        if best:
            P.loot_rect("top", best[1], -0.35, 0.35, -0.15, 0.15, rng=0.2, points=[best])
        P.notes.append("logs along z (end grain front and back); hidden faces dropped, a dark core fills the gaps")
    else:
        rng = random.Random(5)
        spots = [(-0.20, 0.0, 0.0), (0.20, 0.0, 0.0)]
        loose = state != "intact"
        for bi, (bx, by, bz) in enumerate(spots):
            broken = loose and bi == 1
            ss = bundle(rng, broken=broken)
            add_all(P, xfs(ss, t=(bx, 0.0, bz)))
            if not broken:
                P.add(xf(fkit.col_solid(fkit.lcyl("z", 0.0, 0.17, 0.17, -0.45, 0.45, LOGWOOD, n=7)), t=(bx, 0.0, bz)))
        if loose:
            for i in range(9):
                st = box(-0.012, 0.012, 0.0, 0.02, -0.40, 0.40, LOGWOOD, vis=(1,))
                P.add(xf(st, ry=rng.uniform(-50, 50), t=(0.25 + rng.uniform(-0.15, 0.35), 0.0,
                                                         rng.uniform(-0.3, 0.45))))
            P.add(fkit.col_solid(box(0.05, 0.40, 0.0, 0.10, -0.42, 0.42, LOGWOOD)))
        P.dim("bundle_d", 0.35, 0.35, tol=0.02)
        P.dim("bundle_L", 0.90, 0.90, tol=0.02)
        ground_to_floor(P)
    return P


def bundle(rng, d=0.35, L=0.90, broken=False, mats=(LOGWOOD, ENDGRAIN), band=TAWARA, core_mat=SOOT_WOOD):
    """A brushwood bundle (soda) along z: two rings of sticks round a dark core, ragged ends, two straw bands.
    broken=True: the band gone, a thin remnant bundle (the rest is scattered by the caller)."""
    r = d / 2
    out = []
    rings = ((r - 0.025, 10), (r * 0.5, 4)) if not broken else ((0.06, 6),)
    for rr, k in rings:
        for j in range(k):
            a = 2 * math.pi * (j + rng.uniform(-0.2, 0.2)) / k
            cx, cy = rr * math.cos(a), r + rr * math.sin(a) if not broken else 0.07 + rr * math.sin(a)
            t = rng.uniform(0.013, 0.02)
            z0 = -L / 2 + rng.uniform(-0.04, 0.04)
            z1 = L / 2 + rng.uniform(-0.04, 0.04)
            st = box(cx - t, cx + t, cy - t, cy + t, z0, z1, {"front": mats[1], "back": mats[1], "default": mats[0]},
                     vis=(1,))
            out.append(xf(st, rz=rng.uniform(-20, 20), pivot=(cx, cy, 0.0)))
    if not broken:
        cs = fkit.lcyl("z", 0.0, r, r - 0.03, -L / 2 + 0.06, L / 2 - 0.06, core_mat, n=7, vis=(1,))
        cs.wear = "_w2"
        out.append(cs)
        out.append(fkit.lcyl("z", 0.0, r, r, -L / 2, L / 2, mats[0], n=6, vis=(2,), caps=mats[1]))
        for zb in (-L / 4, L / 4):
            s = rope_ring(r, zb, 0.04, band, 7, proud=0.012)
            out.append(xf(s, rx=90.0, t=(0.0, r, 0.0)))
    else:
        out.append(fkit.lcyl("z", 0.0, 0.07, 0.07, -L / 2, L / 2, mats[0], n=5, vis=(2,)))
    return out


# ================================================================================================ jar
JAR = {"s": (0.18, 0.22, 8), "m": (0.30, 0.40, 10), "l": (0.45, 0.60, 12)}


def storage_jar(size="m", glaze="dark", state="intact"):
    d, h, n = JAR[size]
    mat = DARK if glaze == "dark" else PALE
    P = FPart("jar", budget="small", mass={"s": 1.5, "m": 6.0, "l": 18.0}[size])
    ab = state != "intact"
    if state == "broken":
        prof = bits.jar_profile(d, h)[:5] + [(0.97 * d / 2, 0.45 * h), (0.93 * d / 2, 0.45 * h), (0.9 * d / 2, 0.10 * h),
                                             (0.0, 0.08 * h)]
        prof = [p for p in prof if p[1] <= 0.45 * h + 1e-6]
        body = lathe(prof, n, mat, vis=(1,), wear="_w2")
        jag_rim(body, 0.45 * h, 0.05 * h, 13, drop=(2.0, 3.4, 0.2 * h))
        P.add(body)
        P.add(lathe([(0.0, 0.0), (0.36 * d, 0.0), (0.5 * d, 0.40 * h), (0.0, 0.38 * h)], 6, mat, vis=(2,), wear="_w2"))
        add_all(P, shards(40, 0.05, 0.25, 0.22, 9, mat, size=(0.04, 0.11), wear="_w2"))
        P.add(stain(41, 0.10, 0.30, 0.30, sx=1.3))
        P.add(cyl_col(d / 2, 0.0, 0.45 * h, n=8, mat=mat))
    else:
        ss, top = bits.jar(d, h, mat, n=n, lid=state == "intact", wear="_w2" if ab else None, vis=(1,))
        add_all(P, ss)
        add_all(P, bits.jar_lod2(d, h, mat, n=6, lid=state == "intact"))
        if state == "open":
            r = 0.6 * d / 2 + 0.05 * d / 2 + 0.012
            lid = [disc(r, 0.0, 0.02, WOOD, n=max(8, n - 2), vis=(1, 2), wear="_w2")]
            add_all(P, fkit.rest(xfs(lid, rx=-8.0, ry=30.0, t=(d / 2 + r * 0.9, 0.0, d * 0.25))))
            P.add(stain(n + 50, d * 0.3, d * 0.5, d * 0.5, sx=1.2))
        P.add(cyl_col(d / 2 * 0.98, 0.0, top, n=8, mat=mat))
        if size == "l" and state == "intact":
            rr = 0.6 * d / 2
            P.loot_rect("lid", top, -rr, rr, -rr, rr, rng=0.15, points=[(rr * 0.5, top, 0.0)])
    P.dim("d", d, d, tol=0.005)
    P.dim("h", h, h, tol=0.005)
    return P


# ================================================================================================ registry
def M(p3d, variant, state, display, fn):
    return {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}


PROPS = [
    {"id": "jp_f_kama", "cat": CAT, "notes": ["kama seats in a kamado rim by its flange: see seat_y"], "models": [
        M("jp_f_kama", "kama", "intact", "Rice pot (kama) with lid", lambda: kama("intact")),
        M("jp_f_kama_nolid", "kama", "abandoned", "Rice pot, lid off, rusted", lambda: kama("nolid")),
        M("jp_f_kama_nabe", "nabe", "intact", "Small pot (nabe) with bail", lambda: nabe("intact")),
        M("jp_f_kama_nabe_rusted", "nabe", "abandoned", "Small pot, rusted, burnt crust", lambda: nabe("rusted")),
    ]},
    {"id": "jp_f_jizai_kagi", "cat": CAT, "notes": ["hanging prop: Resolution 1 only in the house (Q5)"], "models": [
        M("jp_f_jizai_kagi", "std", "intact", "Pot hook (jizai-kagi) with fish lever", lambda: jizai("std")),
        M("jp_f_jizai_kagi_abandoned", "std", "abandoned", "Pot hook, lever jammed high, rusted pot",
          lambda: jizai("std", "abandoned")),
        M("jp_f_jizai_kagi_plain", "plain", "intact", "Pot hook, plain bar lever", lambda: jizai("plain")),
        M("jp_f_jizai_kagi_plain_abandoned", "plain", "abandoned", "Pot hook (plain), jammed, rusted pot",
          lambda: jizai("plain", "abandoned")),
    ]},
    {"id": "jp_f_mizugame", "cat": CAT, "models": [
        M("jp_f_mizugame", "lid", "intact", "Water jar (mizugame), lid and dipper", lambda: mizugame("lid")),
        M("jp_f_mizugame_open", "lid", "open", "Water jar, lid off leaning, dry", lambda: mizugame("open")),
        M("jp_f_mizugame_broken", "lid", "broken", "Water jar, cracked, piece on the floor", lambda: mizugame("broken")),
    ]},
    {"id": "jp_f_oke", "cat": CAT, "notes": ["coopered family; B3b can call oke(kind, state) for yard tubs"], "models": [
        M("jp_f_oke_bucket", "bucket", "intact", "Handled bucket (oke)", lambda: oke("bucket")),
        M("jp_f_oke_tipped", "bucket", "tipped", "Bucket on its side", lambda: oke("bucket", "tipped")),
        M("jp_f_oke_tarai", "tarai", "intact", "Shallow washing tub (tarai)", lambda: oke("tarai")),
        M("jp_f_oke_tarai_dry", "tarai", "dry", "Tarai, dried out, stave and hoop off", lambda: oke("tarai", "dry")),
        M("jp_f_oke_pickle", "pickle", "intact", "Pickle tub with lid and stone", lambda: oke("pickle")),
        M("jp_f_oke_pickle_open", "pickle", "open", "Pickle tub, lid off, stone on the floor",
          lambda: oke("pickle", "open")),
    ]},
    {"id": "jp_f_tana", "cat": CAT, "per_row": 4, "wall": True, "view": (0.25, 1.0, 0.55),
     "notes": ["wall-hung; widths 0.91 / 1.365 / 1.82 (half-ken steps)"], "models": [
        M("jp_f_tana_%s_%d%s" % (wn, b, "_sag" if st else ""), "%s_%d" % (wn, b), "sag" if st else "intact",
          "Wall shelf %.3g m, %d board%s%s" % (w, b, "s" if b > 1 else "", ", sagging" if st else ""),
          (lambda w=w, b=b, st=st: tana(w, b, "sag" if st else "intact")))
        for (wn, w) in (("091", 0.91), ("136", 1.365), ("182", 1.82)) for b in (1, 3) for st in (False, True)
    ]},
    {"id": "jp_f_firewood", "cat": CAT, "notes": ["B3b: fkit-based stack(length, depth, height, log_d, mats) and "
                                                  "bundle() take outdoor sizes"], "models": [
        M("jp_f_firewood_stack", "stack", "intact", "Firewood stack (maki)", lambda: firewood("stack")),
        M("jp_f_firewood_low", "stack", "low", "Firewood stack, half used, logs rolled", lambda: firewood("stack", "low")),
        M("jp_f_firewood_bundle", "bundle", "intact", "Brushwood bundles (soda)", lambda: firewood("bundle")),
        M("jp_f_firewood_bundle_loose", "bundle", "loose", "Brushwood bundle burst, sticks scattered",
          lambda: firewood("bundle", "loose")),
    ]},
    {"id": "jp_f_jar", "cat": CAT, "models": [
        M("jp_f_jar_%s%s%s" % (sz, "_pale" if g == "pale" else "", "" if st == "intact" else "_" + st), sz,
          st, "Storage jar %s%s%s" % (sz.upper(), " (pale glaze)" if g == "pale" else "",
                                     "" if st == "intact" else ", lid off" if st == "open" else ", broken"),
          (lambda sz=sz, g=g, st=st: storage_jar(sz, g, st)))
        for (sz, g, st) in (("s", "dark", "intact"), ("m", "dark", "intact"), ("l", "dark", "intact"),
                            ("s", "pale", "intact"), ("m", "pale", "intact"), ("s", "dark", "open"),
                            ("m", "dark", "open"), ("l", "dark", "open"), ("m", "dark", "broken"))
    ]},
]
