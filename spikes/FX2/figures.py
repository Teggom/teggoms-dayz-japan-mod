"""figures.py - FX2 statue figures as SDF parts (statuekit.Part), from the photo references (research/statues/REFS.md)
and the proportion choices in research/statues/NOTES.md.

Frames: +y up, +z = the figure's front, x = the figure's LEFT is -x... (viewer's right is +x when facing the figure
from the front? No: facing the figure from +z, the viewer's right is -x). Conventions used below:
  'R' = the figure's own right hand = viewer's left = +x? -> we use x > 0 = the FIGURE'S LEFT (viewer's right).
Head unit: chin y = 0, crown (without ushnisha) y = 1; heads are built in head units and placed with sdf.xform.
"""
import math

import numpy as np

import sdf
from sdf import (sphere, ellipsoid, capsule, rbox, torus, cylinder, spheres, plane, U, S, I, xform, mirror_x,
                 displace, bezier, arc_capsules, squash)
from statuekit import Part


def _arc(pts, r0, r1=None):
    return U(*arc_capsules(pts, r0, r1))


# ================================================================================================ heads
def head(kind="nyorai", full=1.0):
    """A Buddhist head, chin y 0, crown y 1 (head units), face to +z.
    kind: 'nyorai' (snail curls + ushnisha + urna), 'monk' (shaven, urna; Jizo), 'bosatsu' (hair in strands, a tall
    topknot, crown band; Kannon), 'child' (round, chubby: the child Jizo), 'stone' (a softened roadside monk head).
    full: face fullness (1 = the Fujiwara 'full moon' face of the references)."""
    soft = kind in ("stone", "child")
    k0 = 0.10 if soft else 0.07
    cran = ellipsoid((0.0, 0.60, -0.03), (0.385, 0.41, 0.44))
    face = ellipsoid((0.0, 0.40, 0.05), (0.35 * full, 0.43, 0.37))
    jaw = ellipsoid((0.0, 0.17, 0.10), (0.27 * full, 0.18, 0.27))
    cheeks = mirror_x(ellipsoid((0.185, 0.31, 0.19), (0.13 * full, 0.12, 0.15)))
    chin = ellipsoid((0.0, 0.075, 0.25), (0.10, 0.075, 0.10))
    base = U(cran, face, jaw, cheeks, chin, k=k0)
    # brows: the willow-leaf arc, a soft ridge
    brow = mirror_x(_arc(bezier((0.025, 0.575, 0.398), (0.14, 0.625, 0.372), (0.28, 0.565, 0.262), 6), 0.020, 0.013))
    nose = U(capsule((0.0, 0.55, 0.405), (0.0, 0.335, 0.462), 0.030, 0.040),
             sphere((0.0, 0.325, 0.457), 0.045),
             mirror_x(sphere((0.047, 0.318, 0.418), 0.032)), k=0.03)
    lips = U(ellipsoid((0.0, 0.228, 0.380), (0.086, 0.028, 0.035)),
             ellipsoid((0.0, 0.183, 0.372), (0.070, 0.030, 0.035)), k=0.02)
    ears = mirror_x(U(ellipsoid((0.36, 0.47, -0.03), (0.045, 0.20, 0.11), rz=-6.0),
                      ellipsoid((0.37, 0.15, -0.01), (0.04, 0.15, 0.07), rz=4.0), k=0.05))
    neck = U(cylinder((0.0, -0.45, -0.04), (0.0, 0.18, -0.04), 0.245, 0.02),
             torus((0.0, -0.05, -0.04), 0.245, 0.014), torus((0.0, -0.15, -0.04), 0.245, 0.012), k=0.02)
    parts = [base, U(brow, k=0.0), nose, lips, ears, neck]
    if kind == "child":
        parts = [U(ellipsoid((0.0, 0.56, -0.07), (0.43, 0.45, 0.42)), ellipsoid((0.0, 0.33, 0.08), (0.36, 0.34, 0.33)),
                   mirror_x(ellipsoid((0.19, 0.27, 0.19), (0.15, 0.13, 0.15))), k=0.10),
                 U(capsule((0.0, 0.42, 0.395), (0.0, 0.32, 0.425), 0.028, 0.038), k=0.03),
                 mirror_x(capsule((0.04, 0.53, 0.37), (0.20, 0.52, 0.31), 0.018, 0.012)),
                 ellipsoid((0.0, 0.205, 0.38), (0.055, 0.03, 0.03)),
                 mirror_x(ellipsoid((0.40, 0.40, -0.02), (0.05, 0.13, 0.09))),
                 cylinder((0.0, -0.35, -0.03), (0.0, 0.15, -0.03), 0.25, 0.04)]
    body = U(*parts, k=0.025 if not soft else 0.045)
    # carved: eye sockets + the downcast lids, the mouth line, nostrils, the ear hollows and the pierced lobes
    cuts = []
    if kind != "child":
        cuts += [mirror_x(ellipsoid((0.135, 0.502, 0.44), (0.105, 0.040, 0.06), rz=-5.0))]
    lid = mirror_x(ellipsoid((0.132, 0.493, 0.358), (0.098, 0.030, 0.042), rz=-6.0))
    slit = mirror_x(_arc(bezier((0.045, 0.476, 0.398), (0.13, 0.468, 0.40), (0.225, 0.486, 0.35), 5), 0.007))
    mouth = _arc(bezier((-0.082, 0.207, 0.368), (0.0, 0.200, 0.418), (0.082, 0.207, 0.368), 6), 0.0065)
    nostr = mirror_x(sphere((0.030, 0.300, 0.448), 0.012))
    concha = mirror_x(ellipsoid((0.395, 0.46, 0.0), (0.03, 0.115, 0.06)))
    lobe = mirror_x(rbox((0.37, 0.15, -0.01), (0.06, 0.06, 0.016), 0.012))
    if kind == "child":
        slit = mirror_x(_arc(bezier((0.06, 0.415, 0.39), (0.13, 0.395, 0.395), (0.21, 0.42, 0.355), 4), 0.013))
        mouth = _arc(bezier((-0.07, 0.228, 0.385), (0.0, 0.205, 0.415), (0.07, 0.228, 0.385), 4), 0.010)
        out = S(body, slit, mouth, k=0.006)
    elif kind == "stone":
        # carved in stone: the same face, the cuts a little softer (weathered), the lobes not pierced
        out = S(U(body, lid, k=0.015), cuts[0], k=0.03)
        out = U(out, lid, k=0.012)
        out = S(out, slit, mouth, nostr, concha, k=0.006)
    else:
        out = S(U(body, lid, k=0.012), cuts[0], k=0.03)
        out = U(out, lid, k=0.01)
        out = S(out, slit, mouth, nostr, concha, k=0.004)
        out = S(out, lobe, k=0.004)
    urna = sphere((0.0, 0.59, 0.412), 0.020)
    if kind in ("nyorai", "monk"):
        out = U(out, urna, k=0.004)
    if kind == "nyorai":
        out = U(out, curls_cap(), k=0.02)
    elif kind == "bosatsu":
        out = U(out, bosatsu_hair(), k=0.02)
    return out


def _cap_points(cx, cy, cz, rx, ry, rz, keep, n_rows, per_row0, r_curl, y_min_fn):
    pts = []
    for i in range(n_rows):
        th = math.radians(8 + 82 * i / (n_rows - 1))       # polar angle from the top
        n = max(1, int(round(per_row0 * math.sin(th))))
        off = 0.5 * (i % 2)
        for j in range(n):
            ph = 2 * math.pi * (j + off) / n
            x = cx + rx * math.sin(th) * math.sin(ph)
            z = cz + rz * math.sin(th) * math.cos(ph)
            y = cy + ry * math.cos(th)
            if keep(x, y, z):
                pts.append((x, y, z))
    return pts


def curls_cap():
    """The nyorai hair: a cap over the cranium above a straight forehead hairline, the ushnisha (nikkei) on top, both
    covered in snail-shell curls (rahotsu) in staggered rows; the jewel (nikkeishu) at the front of the ushnisha."""
    hairline = lambda x, y, z: y >= 0.57 + 0.38 * z           # noqa: E731  forehead 0.73, nape 0.40
    cap = I(ellipsoid((0.0, 0.62, -0.035), (0.395, 0.425, 0.455)), plane((0.0, -1.0, 0.38), -0.57))
    ush = ellipsoid((0.0, 1.0, -0.05), (0.25, 0.22, 0.27))
    rc = 0.055
    pts = _cap_points(0.0, 0.60, -0.035, 0.375, 0.405, 0.435, hairline, 7, 22, rc, None)
    pts = [p for p in pts if p[1] < 0.93 or (p[0] ** 2 + (p[2] + 0.05) ** 2) > 0.21 ** 2]
    pts += _cap_points(0.0, 0.99, -0.05, 0.23, 0.20, 0.25, lambda x, y, z: y > 0.95, 4, 12, rc, None)
    curls = spheres(pts, rc)
    gem = ellipsoid((0.0, 0.90, 0.23), (0.05, 0.035, 0.03))
    return U(U(cap, ush, k=0.05), curls, gem, k=0.03)


def bosatsu_hair():
    """Kannon: hair combed up in fine wavy strands from the forehead to a tall topknot (hokei), a crown band (hokan)
    with a front plaque carrying the small seated Amida (kebutsu)."""
    cap = I(ellipsoid((0.0, 0.63, -0.03), (0.395, 0.42, 0.45)), plane((0.0, -1.0, 0.30), -0.60))
    strands = lambda P: np.sin(np.arctan2(P[:, 0], P[:, 2] + 0.03) * 22.0)   # noqa: E731
    cap = displace(cap, strands, 0.006)
    knot = U(ellipsoid((0.0, 1.10, -0.06), (0.18, 0.20, 0.18)), ellipsoid((0.0, 1.32, -0.06), (0.13, 0.12, 0.13)),
             cylinder((0.0, 0.95, -0.06), (0.0, 1.12, -0.06), 0.15, 0.03), k=0.04)
    band = I(torus((0.0, 0.80, -0.03), 0.40, 0.03), plane((0.0, 0.0, -1.0), 0.25))
    plaque = U(rbox((0.0, 0.92, 0.36), (0.09, 0.11, 0.025), 0.02, rx=-15.0),
               mirror_x(rbox((0.21, 0.88, 0.30), (0.06, 0.08, 0.02), 0.015, rx=-15.0, ry=30.0)), k=0.01)
    kebutsu = U(sphere((0.0, 0.97, 0.395), 0.028), ellipsoid((0.0, 0.92, 0.39), (0.04, 0.035, 0.02)), k=0.01)
    return U(U(cap, knot, k=0.04), band, plaque, kebutsu, k=0.01)


# ================================================================================================ helpers
def ridges(u, freq, sharp=3.0):
    """Raised fold ridges along u (returns <= 0: pushes the surface out on the crests)."""
    return -np.power(0.5 + 0.5 * np.cos(u * freq), sharp)


def head_part(kind, hu, t, rx=0.0, h_unit=0.009, share=1.0, mat=None, full=1.0):
    n = xform(head(kind, full), rx=rx, t=t, s=hu)
    top = {"nyorai": 1.24, "bosatsu": 1.46}.get(kind, 1.03)
    lo = (t[0] - 0.52 * hu, t[1] - 0.47 * hu, t[2] - 0.55 * hu)
    hi = (t[0] + 0.52 * hu, t[1] + top * hu, t[2] + 0.62 * hu)
    return Part("head", n, lo, hi, h_unit * hu, share=share, mat=mat)


def floor_cut(node, y=0.0):
    return I(node, plane((0.0, -1.0, 0.0), -y))


# ================================================================================================ seated nyorai
def seated_nyorai(mudra="jo"):
    """Seated Buddha, kekka-fuza, seated height 1.0 (base of the lap y 0 .. ushnisha top), robe over both shoulders
    with the chest open in a V and the under-robe band (Met 44890 Amida; CMA 153384 Shaka). mudra: 'jo' (Amida's
    jobon-josho-in: hands in the lap, palms up, index fingers and thumbs in two rings) | 'semui' (Shaka: right hand
    raised palm out, left on the knee palm up)."""
    hu = 0.30
    hp = head_part("nyorai", hu, (0.0, 0.632, 0.025), rx=6.0, share=1.25)
    chest = ellipsoid((0.0, 0.48, 0.0), (0.175, 0.16, 0.135))
    belly = ellipsoid((0.0, 0.35, 0.03), (0.165, 0.14, 0.14))
    shoulders = capsule((-0.15, 0.555, -0.015), (0.15, 0.555, -0.015), 0.07)
    torso = U(chest, belly, shoulders, k=0.06)
    skin = torso
    robe = Node_offset(torso, 0.012)
    vcut = I(I(plane((1.0, -0.55, 0.0), -0.205), plane((-1.0, -0.55, 0.0), -0.205)), plane((0.0, 0.0, -1.0), -0.04))
    robe = S(robe, vcut, k=0.012)
    diag = lambda P: ridges(P[:, 0] * 0.55 + P[:, 1] * 0.83, 70.0) * (P[:, 2] > -0.05)   # noqa: E731
    robe = displace(robe, diag, 0.006)
    lapel = mirror_x(_arc(bezier((0.10, 0.585, 0.10), (0.055, 0.49, 0.15), (0.0, 0.385, 0.16), 5), 0.012))
    band = _arc(bezier((-0.13, 0.44, 0.11), (0.0, 0.42, 0.15), (0.12, 0.39, 0.12), 5), 0.010)
    # arms + sleeves (the figure's right = +x)
    if mudra == "jo":
        arms = mirror_x(U(capsule((0.175, 0.54, -0.02), (0.235, 0.35, 0.04), 0.062, 0.055),
                          capsule((0.235, 0.35, 0.04), (0.12, 0.245, 0.19), 0.052, 0.042), k=0.03))
        sleeves = mirror_x(U(ellipsoid((0.235, 0.35, 0.01), (0.072, 0.20, 0.125)),
                             ellipsoid((0.25, 0.18, 0.10), (0.08, 0.08, 0.15)), k=0.05))
    else:
        rarm = U(capsule((0.175, 0.54, -0.02), (0.245, 0.36, 0.07), 0.062, 0.055),
                 capsule((0.245, 0.36, 0.07), (0.235, 0.50, 0.19), 0.052, 0.042), k=0.03)
        larm = U(capsule((-0.175, 0.54, -0.02), (-0.24, 0.35, 0.05), 0.062, 0.055),
                 capsule((-0.24, 0.35, 0.05), (-0.29, 0.20, 0.25), 0.052, 0.042), k=0.03)
        arms = U(rarm, larm)
        sleeves = U(ellipsoid((0.25, 0.35, 0.05), (0.07, 0.18, 0.12)), ellipsoid((-0.24, 0.33, 0.02), (0.075, 0.20, 0.13)),
                    ellipsoid((-0.27, 0.17, 0.12), (0.08, 0.08, 0.16)), ellipsoid((0.27, 0.20, 0.10), (0.07, 0.08, 0.13)),
                    k=0.05)
    sleeves = displace(sleeves, lambda P: ridges(P[:, 1] * 1.0 + 0.3 * np.abs(P[:, 0]), 55.0), 0.007)
    # the crossed legs under the robe, concentric folds over the shins
    lapb = ellipsoid((0.0, 0.085, 0.07), (0.47, 0.105, 0.25))
    shins = U(capsule((-0.36, 0.10, 0.10), (0.22, 0.155, 0.25), 0.078), capsule((0.36, 0.085, 0.08), (-0.22, 0.13, 0.225), 0.075),
              mirror_x(sphere((0.39, 0.085, 0.10), 0.095)), k=0.05)
    lap = U(lapb, shins, k=0.05)
    lapf = lambda P: ridges(np.sqrt(P[:, 0] ** 2 * 0.6 + (P[:, 2] + 0.15) ** 2), 48.0)   # noqa: E731
    lap = displace(lap, lapf, 0.006)
    foot = ellipsoid((-0.19, 0.19, 0.20), (0.055, 0.032, 0.105), ry=25.0)
    toes = spheres([(-0.19 + 0.04 * math.sin(math.radians(25)) + dx, 0.205, 0.30 + dz)
                    for dx, dz in ((-0.03, -0.005), (-0.012, 0.004), (0.006, 0.008), (0.022, 0.006), (0.036, 0.0))], 0.014)
    drape = ellipsoid((0.0, 0.05, 0.28), (0.17, 0.055, 0.05))
    body = U(robe, lapel, band, arms, sleeves, lap, drape, k=0.03)
    body = U(body, skin, k=0.0)
    body = floor_cut(body)
    parts = [hp, Part("body", body, (-0.55, 0.0, -0.25), (0.55, 0.72, 0.36), 0.0055, share=1.6)]
    # hands
    if mudra == "jo":
        hands = U(ellipsoid((0.0, 0.205, 0.225), (0.125, 0.028, 0.085)), ellipsoid((0.0, 0.232, 0.235), (0.12, 0.026, 0.08)),
                  mirror_x(torus((0.04, 0.262, 0.29), 0.019, 0.0085, rx=70.0)), k=0.01)
        hands = U(hands, foot, toes, k=0.01)
        parts.append(Part("hands", hands, (-0.26, 0.15, 0.13), (0.26, 0.31, 0.34), 0.0028, share=0.45))
    else:
        rh = U(rbox((0.25, 0.585, 0.212), (0.045, 0.06, 0.017), 0.013),
               spheres([(0.25 + dx, 0.655, 0.212) for dx in (-0.03, -0.01, 0.01, 0.03)], 0.012),
               U(*[capsule((0.25 + dx, 0.62, 0.212), (0.25 + dx * 1.1, 0.66, 0.212), 0.012) for dx in (-0.03, -0.01, 0.01, 0.03)]),
               capsule((0.29, 0.56, 0.215), (0.305, 0.60, 0.222), 0.013), k=0.008)
        lh = U(rbox((-0.30, 0.175, 0.31), (0.05, 0.018, 0.07), 0.014, rx=-20.0),
               U(*[capsule((-0.30 + dx, 0.17, 0.35), (-0.30 + dx, 0.15, 0.40), 0.011) for dx in (-0.03, -0.01, 0.01, 0.03)]),
               k=0.008)
        parts.append(Part("hands", U(rh, lh, foot, toes, k=0.008), (-0.40, 0.12, 0.10), (0.36, 0.71, 0.43), 0.0028,
                          share=0.45))
    return parts


def Node_offset(node, t):
    return sdf.Node(lambda P: node(P) - t, node.lo - t, node.hi + t)


# ================================================================================================ standing figures
def standing_monk(stone=False, staff=True, jewel=True):
    """Standing Jizo, height 1.0 (soles .. crown): the shaven monk in his robe with the kesa over the left shoulder
    (ring at the chest), the wish-granting jewel (hoju) in the left hand, the ringed staff (shakujo) in the right
    (Met 53175, Met 76084). stone=True: the roadside stone form (stockier, softer, the staff fused to the body)."""
    hu = 0.20 if stone else 0.15
    chin = 1.0 - hu * 1.03 + 0.075 * hu
    hp = head_part("stone" if stone else "monk", hu, (0.0, chin - 0.075 * hu, -0.01), rx=4.0, share=1.45 if not stone else 1.35)
    sw = 1.38 if stone else 1.0                                        # stockier body
    sh = chin - 0.06
    chest = ellipsoid((0.0, sh - 0.09, 0.0), (0.105 * sw, 0.11, 0.08 * sw))
    shoulders = capsule((-0.085 * sw, sh - 0.015, -0.01), (0.085 * sw, sh - 0.015, -0.01), 0.045 * sw)
    lower = squash(capsule((0.0, sh - 0.20, 0.0), (0.0, 0.05, 0.0), 0.10 * sw, 0.112 * sw), 1.0, 1.0, 0.76)
    robe = U(chest, shoulders, lower, k=0.05)
    def folds(P):
        x, y = P[:, 0], P[:, 1]
        u_fold = ridges(y - 2.6 * x * x, 62.0) * ((y > 0.30) & (y < sh - 0.15) & (P[:, 2] > 0))
        v_fold = ridges(x, 75.0) * (y <= 0.30) * (P[:, 2] > 0) * np.clip((0.33 - y) / 0.08, 0, 1)
        # the kesa: a raised band from the left shoulder (-x) to the right hip (+x), front only
        band = np.abs((x + 0.0) * math.sin(math.radians(32)) + (y - (sh - 0.14)) * math.cos(math.radians(32)))
        kesa = -np.clip((0.028 - band) / 0.006, 0, 1) * (P[:, 2] > 0.0)
        return u_fold + v_fold + 0.9 * kesa
    robe = displace(robe, folds, 0.004 if stone else 0.0065)
    hem = squash(torus((0.0, 0.055, 0.0), 0.11 * sw, 0.011), 1.0, 1.0, 0.76)
    kesa = torus((-0.06 * sw, sh - 0.075, 0.078 * sw), 0.015, 0.0045, rx=80.0)
    feet = mirror_x(ellipsoid((0.045, 0.022, 0.075), (0.036, 0.024, 0.06)))
    sx = 0.155 * sw
    rarm = U(capsule((0.11 * sw, sh - 0.02, -0.01), (0.15 * sw, sh - 0.20, 0.02), 0.042, 0.036),
             capsule((0.15 * sw, sh - 0.20, 0.02), (sx, sh - 0.27, 0.10), 0.034, 0.028), k=0.02)
    larm = U(capsule((-0.11 * sw, sh - 0.02, -0.01), (-0.15 * sw, sh - 0.20, 0.02), 0.042, 0.036),
             capsule((-0.15 * sw, sh - 0.20, 0.02), (-0.085, sh - 0.225, 0.13), 0.034, 0.027), k=0.02)
    sleeves = U(ellipsoid((0.14 * sw, sh - 0.31, 0.045), (0.038 * sw, 0.13, 0.06)),
                ellipsoid((-0.14 * sw, sh - 0.30, 0.05), (0.038 * sw, 0.12, 0.06)), k=0.03)
    sleeves = displace(sleeves, lambda P: ridges(P[:, 2] * 1.0 + 0.2 * P[:, 1], 90.0), 0.004)
    body = U(robe, hem, kesa, rarm, larm, sleeves, feet, k=0.02 if not stone else 0.035)
    body = floor_cut(body)
    parts = [hp, Part("body", body, (-0.26, 0.0, -0.16), (0.26, sh + 0.08, 0.20), 0.0045, share=1.5)]
    hy = sh - 0.27
    rhand = ellipsoid((sx, hy, 0.105), (0.03, 0.042, 0.034))
    hands = [rhand]
    if jewel:
        lh = ellipsoid((-0.085, sh - 0.235, 0.14), (0.045, 0.018, 0.04))
        gem = U(sphere((-0.085, sh - 0.205, 0.14), 0.026), capsule((-0.085, sh - 0.20, 0.14), (-0.085, sh - 0.165, 0.14),
                                                                        0.018, 0.003), k=0.012)
        hands += [lh, gem]
    hn = U(*hands, k=0.008)
    parts.append(Part("hands", hn, (-0.16, hy - 0.06, 0.05), (0.22, sh - 0.14, 0.20), 0.0025, share=0.35))
    if staff:
        z = 0.11
        top = 1.06 if not stone else 0.98
        r = 0.0075 if not stone else 0.013
        pole = capsule((sx, 0.0 if not stone else 0.03, z), (sx, top, z), r)
        if stone:
            pole = U(pole, capsule((sx, 0.03, z), (sx * 0.9, 0.03, 0.07), 0.016), k=0.01)
        parts.append(Part("staff", pole, (sx - 0.03, 0.0, z - 0.03), (sx + 0.03, top + 0.01, z + 0.03),
                          0.0035 if not stone else 0.004, share=0.12))
        parts.append(Part("staffhead", shakujo_head(sx, top, z, stone), (sx - 0.06, top - 0.015, z - 0.03),
                          (sx + 0.06, top + 0.13, z + 0.03), 0.0011 if not stone else 0.0018, share=0.45 if not stone else 0.2))
    return parts


def shakujo_head(x, y0, z, stone=False):
    """The shakujo head: a closed pointed loop (two arcs meeting at the top), a central spindle, three rings hanging
    on each side, and a small stupa finial (Met 53175: the loop + rings; FX2 fixes the old see-through top)."""
    w, h = (0.042, 0.105) if not stone else (0.045, 0.09)
    r = 0.0042 if not stone else 0.008
    L = [bezier((x, y0, z), (x - w * 1.5, y0 + h * 0.55, z), (x, y0 + h, z), 8)]
    Rr = [bezier((x, y0, z), (x + w * 1.5, y0 + h * 0.55, z), (x, y0 + h, z), 8)]
    loop = U(*arc_capsules(L[0], r), *arc_capsules(Rr[0], r))
    spindle = capsule((x, y0, z), (x, y0 + h * 0.55, z), r * 0.9)
    fin = U(sphere((x, y0 + h + 0.006, z), r * 1.6), capsule((x, y0 + h + 0.006, z), (x, y0 + h + 0.03, z), r * 1.2, 0.0012),
            k=0.003)
    collar = cylinder((x, y0 - 0.012, z), (x, y0 + 0.004, z), r * 1.9, 0.002)
    if stone:
        # carved in stone: the loop filled thin (a pierced slab is too fragile to survive), the rings as beads
        web = squash(ellipsoid((x, y0 + h * 0.5, z), (w * 0.95, h * 0.48, 0.02)), 1.0, 1.0, 0.35, about=(x, 0, z))
        beads = spheres([(x + s * w * 1.05, y0 + h * f, z + 0.004) for s in (-1, 1) for f in (0.30, 0.48, 0.66)], 0.011)
        return U(loop, web, beads, fin, collar, k=0.004)
    rings = []
    for s in (-1, 1):
        pts = (L[0] if s < 0 else Rr[0])
        for k in (2, 4, 6):
            px, py, pz = pts[k]
            rings.append(torus((px + s * 0.011, py - 0.012, pz), 0.0135, 0.0028, rx=90.0, rz=s * 20.0))
    return U(loop, spindle, fin, collar, *rings, k=0.0015)


def standing_kannon():
    """Standing Sho Kannon, height 1.0 (soles .. topknot): crowned bosatsu head, bare chest with a necklace, the skirt
    (mo) with its turned-over band and vertical folds, the scarf (tenne) over the arms hanging to the ankles with a
    loop across the knees; left hand at the chest holding a lotus bud, right hand lowered palm out (yogan-in)
    (CMA 152018, Met 49257)."""
    hu = 0.128
    chin = 1.0 - hu * 1.46
    hp = head_part("bosatsu", hu, (0.0, chin, -0.005), rx=3.0, share=1.25)
    sh = chin - 0.055
    chest = ellipsoid((0.0, sh - 0.085, 0.0), (0.108, 0.10, 0.072))
    belly = ellipsoid((0.0, sh - 0.19, 0.012), (0.092, 0.09, 0.07))
    shoulders = capsule((-0.10, sh - 0.01, -0.01), (0.10, sh - 0.01, -0.01), 0.04)
    wy = sh - 0.26
    skirt = squash(capsule((0.0, wy, 0.0), (0.0, 0.05, 0.0), 0.098, 0.088), 1.0, 1.0, 0.78)
    skirt = displace(skirt, lambda P: ridges(P[:, 0] + 0.15 * P[:, 1], 80.0) * (P[:, 1] < wy - 0.08), 0.005)
    turn = squash(torus((0.0, wy - 0.03, 0.0), 0.096, 0.009), 1.0, 1.0, 0.8)
    hem = squash(torus((0.0, 0.06, 0.0), 0.088, 0.012), 1.0, 1.0, 0.78)
    neck = U(*arc_capsules(bezier((-0.075, sh + 0.005, 0.05), (0.0, sh - 0.10, 0.10), (0.075, sh + 0.005, 0.05), 6), 0.0065),
             sphere((0.0, sh - 0.075, 0.093), 0.011))
    scarf = []
    for s in (-1, 1):
        scarf += arc_capsules(bezier((s * 0.11, sh, -0.03), (s * 0.16, sh - 0.25, 0.03), (s * 0.15, 0.10, 0.02), 7), 0.008)
    scarf += arc_capsules(bezier((-0.115, wy - 0.06, 0.06), (0.0, wy - 0.20, 0.115), (0.115, wy - 0.06, 0.06), 7), 0.008)
    rarm = U(capsule((0.10, sh - 0.01, -0.01), (0.13, sh - 0.20, 0.0), 0.035, 0.03),
             capsule((0.13, sh - 0.20, 0.0), (0.14, sh - 0.36, 0.04), 0.029, 0.023),
             torus((0.118, sh - 0.11, -0.005), 0.033, 0.006, rz=-10.0), k=0.012)
    larm = U(capsule((-0.10, sh - 0.01, -0.01), (-0.13, sh - 0.20, 0.0), 0.035, 0.03),
             capsule((-0.13, sh - 0.20, 0.0), (-0.07, sh - 0.12, 0.09), 0.029, 0.022),
             torus((-0.118, sh - 0.11, -0.005), 0.033, 0.006, rz=10.0), k=0.012)
    feet = mirror_x(ellipsoid((0.042, 0.02, 0.07), (0.034, 0.022, 0.058)))
    body = U(chest, belly, shoulders, skirt, turn, hem, neck, rarm, larm, feet, *scarf, k=0.012)
    body = floor_cut(body)
    parts = [hp, Part("body", body, (-0.24, 0.0, -0.14), (0.24, sh + 0.06, 0.19), 0.0042, share=1.55)]
    rh = U(rbox((0.142, sh - 0.40, 0.052), (0.028, 0.045, 0.011), 0.009, rx=-10.0),
           U(*[capsule((0.142 + dx, sh - 0.425, 0.055), (0.142 + dx, sh - 0.47, 0.06), 0.0075) for dx in (-0.018, -0.006, 0.006, 0.018)]),
           k=0.004)
    lh = ellipsoid((-0.065, sh - 0.115, 0.105), (0.028, 0.035, 0.026))
    lotus = U(capsule((-0.062, sh - 0.12, 0.11), (-0.055, sh + 0.06, 0.12), 0.004),
              ellipsoid((-0.055, sh + 0.085, 0.12), (0.016, 0.028, 0.016)), k=0.004)
    parts.append(Part("hands", U(rh, lh, lotus, k=0.004), (-0.11, sh - 0.49, 0.02), (0.18, sh + 0.12, 0.15), 0.0022,
                      share=0.35))
    return parts


def child_jizo():
    """A child's Jizo (grave marker): about 4 heads tall, a round head, hands together in prayer (gassho) at the
    chest, a plain robe with soft U folds (general knowledge + the Met 53175 robe; no child-Jizo photo fetched)."""
    hu = 0.27
    chin = 1.0 - hu
    hp = head_part("child", hu, (0.0, chin - 0.02, 0.0), rx=6.0, share=1.0)
    sh = chin - 0.03
    robe = U(squash(capsule((0.0, sh - 0.06, 0.0), (0.0, 0.05, 0.0), 0.16, 0.19), 1.0, 1.0, 0.80),
             capsule((-0.12, sh - 0.02, -0.01), (0.12, sh - 0.02, -0.01), 0.07), k=0.08)
    robe = displace(robe, lambda P: ridges(P[:, 1] - 3.0 * P[:, 0] ** 2, 40.0) * (P[:, 2] > 0) * (P[:, 1] < sh - 0.18), 0.006)
    arms = mirror_x(U(capsule((0.15, sh - 0.05, 0.0), (0.16, sh - 0.20, 0.07), 0.055, 0.05),
                      capsule((0.16, sh - 0.20, 0.07), (0.03, sh - 0.17, 0.17), 0.048, 0.038), k=0.03))
    palms = rbox((0.0, sh - 0.12, 0.185), (0.032, 0.07, 0.035), 0.022, rx=-12.0)
    body = floor_cut(U(robe, arms, palms, k=0.03))
    return [hp, Part("body", body, (-0.26, 0.0, -0.18), (0.26, sh + 0.08, 0.26), 0.006, share=1.0)]


# ================================================================================================ guardians
def komainu(mouth="a", style="a"):
    """Seated guardian lion-dog, seated height 1.0 (base .. top of the head), facing +z (CMA 106262 / 106263, Met
    53190). mouth 'a' = open (the karashishi), 'un' = closed. style 'a': the upright temple-guardian form of the
    references (mane in heavy hanging locks, un with a short horn); 'b': the compact Edo stone form (lower head, a
    rounder chest, mane in tight curl rows, no horn, a flame tail)."""
    b = style == "b"
    k0 = 0.06 if not b else 0.075
    hy = 0.0 if not b else -0.07
    rear = ellipsoid((0.0, 0.22, -0.17), (0.21, 0.22, 0.23))
    thighs = mirror_x(ellipsoid((0.15, 0.17, -0.10), (0.095, 0.16, 0.20)))
    hpaws = mirror_x(ellipsoid((0.17, 0.035, 0.02), (0.065, 0.035, 0.095)))
    chest = ellipsoid((0.0, 0.47 + hy * 0.5, 0.04), (0.19 if not b else 0.21, 0.23, 0.17))
    torso = ellipsoid((0.0, 0.40, -0.06), (0.18, 0.24, 0.20), rx=-15.0)
    legs = mirror_x(capsule((0.115, 0.42 + hy * 0.5, 0.12), (0.11, 0.06, 0.20), 0.066 if not b else 0.075, 0.056))
    elbows = mirror_x(spheres([(0.155, 0.33, 0.07), (0.16, 0.27, 0.06)], 0.045))
    paws = mirror_x(U(ellipsoid((0.11, 0.04, 0.245), (0.07, 0.04, 0.08)),
                      spheres([(0.11 + dx, 0.035, 0.31) for dx in (-0.045, -0.015, 0.015, 0.045)], 0.022), k=0.015))
    body = U(rear, thighs, hpaws, chest, torso, legs, elbows, paws, k=k0)
    # the head (big), the face
    hc = (0.0, 0.79 + hy, 0.11 + (0.03 if b else 0.0))
    skull = ellipsoid(hc, (0.20, 0.165, 0.17))
    muzzle = ellipsoid((0.0, hc[1] - 0.06, hc[2] + 0.13), (0.15, 0.10, 0.10))
    nose = ellipsoid((0.0, hc[1] - 0.005, hc[2] + 0.215), (0.07, 0.045, 0.04))
    brows = mirror_x(capsule((0.03, hc[1] + 0.11, hc[2] + 0.15), (0.155, hc[1] + 0.10, hc[2] + 0.08), 0.03))
    eyes = mirror_x(sphere((0.085, hc[1] + 0.065, hc[2] + 0.135), 0.042))
    ears = mirror_x(ellipsoid((0.19, hc[1] + 0.05, hc[2] - 0.05), (0.05, 0.075, 0.03), rz=-35.0))
    cheeks = mirror_x(ellipsoid((0.13, hc[1] - 0.06, hc[2] + 0.08), (0.08, 0.08, 0.08)))
    headn = U(skull, muzzle, nose, brows, eyes, ears, cheeks, k=0.03)
    if mouth == "a":
        cav = ellipsoid((0.0, hc[1] - 0.12, hc[2] + 0.19), (0.11, 0.05, 0.09))
        jaw = ellipsoid((0.0, hc[1] - 0.175, hc[2] + 0.11), (0.115, 0.045, 0.10))
        headn = S(headn, cav, k=0.01)
        headn = U(headn, jaw, ellipsoid((0.0, hc[1] - 0.155, hc[2] + 0.14), (0.07, 0.02, 0.06)), k=0.015)
        fangs = mirror_x(U(capsule((0.075, hc[1] - 0.085, hc[2] + 0.205), (0.072, hc[1] - 0.135, hc[2] + 0.205), 0.013, 0.003),
                           capsule((0.07, hc[1] - 0.17, hc[2] + 0.18), (0.068, hc[1] - 0.125, hc[2] + 0.18), 0.012, 0.003)))
        teeth = spheres([(dx, hc[1] - 0.085, hc[2] + 0.215) for dx in (-0.04, -0.013, 0.013, 0.04)], 0.012)
        headn = U(headn, fangs, teeth, k=0.003)
    else:
        line = _arc(bezier((-0.12, hc[1] - 0.10, hc[2] + 0.13), (0.0, hc[1] - 0.115, hc[2] + 0.255), (0.12, hc[1] - 0.10, hc[2] + 0.13), 6), 0.008)
        headn = S(headn, line, k=0.004)
        fangs = mirror_x(capsule((0.07, hc[1] - 0.095, hc[2] + 0.20), (0.068, hc[1] - 0.14, hc[2] + 0.19), 0.012, 0.003))
        headn = U(headn, fangs, k=0.003)
        if not b:
            headn = U(headn, capsule((0.0, hc[1] + 0.15, hc[2] + 0.02), (0.0, hc[1] + 0.25, hc[2] - 0.01), 0.028, 0.007), k=0.02)
    # mane: a mass behind the head and round the neck, covered in curl bumps / hanging locks; the chest beard
    mane = ellipsoid((0.0, 0.70 + hy, -0.01), (0.25, 0.23, 0.17))

    def on_mane(y, a, lift=0.0):
        f = max(0.0, 1.0 - ((y - 0.70) / 0.235) ** 2) ** 0.5
        return ((0.25 * f + lift) * math.sin(a), y + hy, -0.01 - (0.17 * f + lift) * math.cos(a))
    pts = []
    if not b:
        # big spiral curls in three staggered rows over the back and sides of the neck + a ruff round the face
        # (CMA 106262/3: heavy curled locks)
        for row, y in enumerate((0.86, 0.75, 0.64, 0.54)):
            for i in range(9):
                a = math.radians(-120 + 240 * i / 8 + 13 * (row % 2))
                pts.append(on_mane(y, a, 0.01))
        mane = U(mane, spheres(pts, 0.05), k=0.02)
        ruff = spheres([on_mane(y, math.radians(sg * 128), 0.0) for sg in (-1, 1) for y in (0.84, 0.74, 0.64)], 0.045)
        mane = U(mane, ruff, k=0.02)
    else:
        for row, y in enumerate((0.84, 0.76, 0.68, 0.60, 0.53)):
            for i in range(12):
                a = math.radians(-115 + 230 * i / 11 + 9 * (row % 2))
                pts.append(on_mane(y, a, 0.005))
        mane = U(mane, spheres(pts, 0.04), k=0.02)
    beard = spheres([(dx, 0.60 + hy + dy, 0.19 + (0.03 if b else 0.0)) for dx, dy in ((-0.07, 0.0), (0.0, -0.02), (0.07, 0.0), (-0.035, -0.07), (0.035, -0.07))],
                    0.04)
    # the tail: a flame plume behind the rump, rising, with side lobes
    tail = U(*arc_capsules(bezier((0.0, 0.20, -0.36), (0.0, 0.40, -0.48), (0.0, 0.62 + hy, -0.40), 6), 0.075, 0.035),
             mirror_x(ellipsoid((0.07, 0.42, -0.42), (0.05, 0.12, 0.05), rz=-25.0)),
             mirror_x(ellipsoid((0.06, 0.55 + hy, -0.40), (0.045, 0.09, 0.045), rz=-30.0)), k=0.03)
    figure = U(body, headn, mane, beard, tail, k=0.025 if not b else 0.035)
    figure = floor_cut(figure)
    return [Part("figure", figure, (-0.34, 0.0, -0.56), (0.34, 1.10, 0.42), 0.0065, share=1.0)]


def kitsune(item="key"):
    """Seated Inari fox (kitsune), seated height 1.0 (base .. ear tips), slim, long-necked, pointed ears and snout,
    the bushy tail raised behind ending in a jewel-shaped point; item in the mouth: 'key' (the rice-store key,
    kagi) or 'jewel' (tama). No stone Inari fox in either open-access collection: proportions from the Met 60375 fox
    netsuke (muzzle, ears, tail) and general knowledge of Inari fox pairs (NOTES.md)."""
    rear = ellipsoid((0.0, 0.19, -0.13), (0.15, 0.19, 0.19))
    hind = mirror_x(ellipsoid((0.10, 0.14, -0.06), (0.06, 0.13, 0.17)))
    hpaw = mirror_x(ellipsoid((0.10, 0.028, 0.05), (0.04, 0.028, 0.08)))
    body = ellipsoid((0.0, 0.42, -0.03), (0.125, 0.22, 0.13), rx=-22.0)
    chest = ellipsoid((0.0, 0.48, 0.06), (0.105, 0.15, 0.095))
    legs = mirror_x(capsule((0.058, 0.42, 0.10), (0.055, 0.03, 0.135), 0.032, 0.025))
    paws = mirror_x(ellipsoid((0.055, 0.024, 0.165), (0.03, 0.024, 0.048)))
    neck = capsule((0.0, 0.52, 0.03), (0.0, 0.76, 0.08), 0.07, 0.057)
    skull = ellipsoid((0.0, 0.80, 0.085), (0.083, 0.074, 0.088))
    snout = capsule((0.0, 0.785, 0.135), (0.0, 0.755, 0.275), 0.048, 0.017)
    nose = sphere((0.0, 0.758, 0.288), 0.016)
    ears = mirror_x(capsule((0.048, 0.85, 0.06), (0.072, 0.985, 0.045), 0.032, 0.006))
    headn = U(skull, snout, nose, ears, k=0.02)
    hollow = mirror_x(capsule((0.055, 0.87, 0.075), (0.071, 0.965, 0.062), 0.017, 0.003))
    eyes = mirror_x(_arc([(0.035, 0.815, 0.155), (0.06, 0.83, 0.13)], 0.006))
    mouthl = mirror_x(_arc([(0.0, 0.75, 0.25), (0.035, 0.755, 0.17)], 0.004))
    headn = S(headn, hollow, eyes, mouthl, k=0.004)
    tail = U(*arc_capsules(bezier((0.0, 0.10, -0.29), (0.02, 0.40, -0.44), (0.0, 0.66, -0.30), 7), 0.06, 0.085),
             capsule((0.0, 0.66, -0.30), (0.0, 0.80, -0.22), 0.08, 0.012), k=0.05)
    tail = displace(tail, lambda P: ridges(P[:, 1] * 1.0 + 0.4 * P[:, 2], 38.0, 2.0), 0.0035)
    fig = U(rear, hind, hpaw, body, chest, legs, paws, neck, headn, tail, k=0.03)
    if item == "key":
        key = U(capsule((-0.075, 0.762, 0.20), (0.07, 0.762, 0.20), 0.009),
                torus((0.085, 0.762, 0.20), 0.016, 0.005, rz=90.0),
                rbox((-0.085, 0.745, 0.20), (0.008, 0.022, 0.006), 0.002), k=0.003)
    else:
        key = U(sphere((0.0, 0.755, 0.235), 0.034), capsule((0.0, 0.775, 0.235), (0.0, 0.805, 0.235), 0.024, 0.004), k=0.01)
    fig = U(fig, key, k=0.004)
    fig = floor_cut(fig)
    return [Part("figure", fig, (-0.20, 0.0, -0.45), (0.20, 1.0, 0.33), 0.0042, share=1.0)]


# ================================================================================================ test
def test_head(kind="nyorai"):
    n = head(kind)
    return [Part("head", n, (-0.5, -0.5, -0.55), (0.5, 1.45 if kind == "bosatsu" else 1.25, 0.55), 0.008,
                 share=1.0)]


# ================================================================================================ lotus seat
def lotus_seat(n=12, rows=3):
    """The lotus seat (rengeza) of an image: top radius 0.5, petals in staggered tiers round a shallow cup, the seat
    top flat at y 0.30, a waisted drum (keban) under it down to y 0 (CMA 147591, Met 44890, Met 76084). Kit
    octagonal tiers go under it in the props."""
    cup = U(cylinder((0.0, 0.16, 0.0), (0.0, 0.30, 0.0), 0.34, 0.03), ellipsoid((0.0, 0.17, 0.0), (0.33, 0.10, 0.33)), k=0.04)
    petals = []
    for r in range(rows):
        m = n + 2 * r
        ring_r = 0.47 - 0.07 * r
        y = 0.10 + 0.075 * r
        tilt = 62.0 - 14.0 * r
        for i in range(m):
            a = 360.0 * (i + 0.5 * (r % 2)) / m
            c = (ring_r * math.sin(math.radians(a)), y + 0.07, ring_r * math.cos(math.radians(a)))
            w = 2 * math.pi * ring_r / m * 0.62
            p = ellipsoid((0.0, 0.0, 0.0), (w, 0.12, 0.022))
            p = U(p, capsule((0.0, 0.08, 0.0), (0.0, 0.15, 0.012), 0.02, 0.004), k=0.03)   # the pointed tip
            petals.append(xform(p, rx=tilt, ry=-a, t=c))
    drum = U(cylinder((0.0, 0.0, 0.0), (0.0, 0.06, 0.0), 0.36, 0.02),
             cylinder((0.0, 0.05, 0.0), (0.0, 0.14, 0.0), 0.22, 0.02),
             torus((0.0, 0.095, 0.0), 0.23, 0.02), k=0.02)
    seat = floor_cut(U(cup, drum, *petals, k=0.012))
    return [Part("seat", seat, (-0.62, 0.0, -0.62), (0.62, 0.40, 0.62), 0.006, share=1.0)]


# ================================================================================================ kagura masks
def kagura_mask(kind="okina"):
    """A kagura / noh-type mask, height 1.0 (chin .. top), width ~0.75, face to +z, the back flat at z 0 (hung on a
    wall peg). kind: 'okina' (the smiling old man: tufted brows, crescent eyes, the cut chin with its beard; CMA
    149100), 'oni' (the demon of the kagura plays: bulging ringed eyes, knotted brows, flared nose, fangs and two
    horns; CMA 147048 ko-beshimi for the face), 'okame' (the plump woman: high round cheeks, high brow dots, a small
    mouth; CMA 147046 waka-onna), 'hyottoko' (the pursed, sideways-blowing mouth, uneven eyes; CMA 148010 usobuki)."""
    face = ellipsoid((0.0, 0.50, 0.0), (0.36, 0.50, 0.30))
    cut_back = plane((0.0, 0.0, -1.0), 0.0)          # keep z >= 0
    parts = []
    cuts = []
    if kind == "okina":
        face = displace(face, lambda P: ridges(P[:, 1] + 0.15 * np.abs(P[:, 0]), 70.0) * (P[:, 1] > 0.62), 0.008)
        parts += [mirror_x(ellipsoid((0.15, 0.66, 0.20), (0.11, 0.045, 0.05), rz=-12.0)),   # tufted brows
                  mirror_x(ellipsoid((0.15, 0.40, 0.20), (0.10, 0.08, 0.07))),               # round cheeks
                  capsule((0.0, 0.58, 0.25), (0.0, 0.42, 0.29), 0.035, 0.05),                # nose
                  sphere((0.0, 0.41, 0.285), 0.05),
                  capsule((0.0, 0.12, 0.17), (0.0, -0.10, 0.12), 0.06, 0.015)]              # beard tuft
        cuts += [mirror_x(_arc(bezier((0.06, 0.54, 0.26), (0.14, 0.59, 0.27), (0.23, 0.54, 0.22), 5), 0.024)),
                 _arc(bezier((-0.17, 0.27, 0.22), (0.0, 0.20, 0.27), (0.17, 0.27, 0.22), 6), 0.028),   # grin
                 _arc(bezier((-0.25, 0.15, 0.18), (0.0, 0.10, 0.23), (0.25, 0.15, 0.18), 6), 0.010)]   # the cut chin
    elif kind == "oni":
        parts += [mirror_x(sphere((0.13, 0.55, 0.18), 0.075)),                              # bulging eyes
                  mirror_x(ellipsoid((0.15, 0.66, 0.19), (0.13, 0.05, 0.07), rz=-20.0)),    # knotted brows
                  ellipsoid((0.0, 0.40, 0.25), (0.11, 0.08, 0.07)),                          # flared nose
                  mirror_x(sphere((0.08, 0.37, 0.24), 0.05)),
                  mirror_x(ellipsoid((0.20, 0.30, 0.15), (0.10, 0.09, 0.08))),
                  mirror_x(capsule((0.18, 0.92, 0.0), (0.24, 1.18, -0.02), 0.06, 0.012)),   # horns
                  mirror_x(capsule((0.10, 0.17, 0.20), (0.10, 0.07, 0.21), 0.022, 0.004))]  # fangs (up from the jaw)
        cuts += [mirror_x(torus((0.13, 0.55, 0.245), 0.035, 0.010, rx=90.0)),
                 _arc(bezier((-0.17, 0.22, 0.20), (0.0, 0.25, 0.25), (0.17, 0.22, 0.20), 6), 0.022)]
    elif kind == "okame":
        face = ellipsoid((0.0, 0.48, 0.0), (0.38, 0.48, 0.28))
        parts += [mirror_x(ellipsoid((0.17, 0.33, 0.17), (0.14, 0.13, 0.10))),             # the plump cheeks
                  mirror_x(ellipsoid((0.11, 0.80, 0.19), (0.04, 0.025, 0.02))),            # high brow dots
                  capsule((0.0, 0.50, 0.22), (0.0, 0.40, 0.24), 0.025, 0.032),
                  ellipsoid((0.0, 0.20, 0.22), (0.05, 0.03, 0.03))]                          # small lips
        cuts += [mirror_x(_arc(bezier((0.06, 0.55, 0.25), (0.12, 0.535, 0.26), (0.19, 0.55, 0.22), 4), 0.022)),
                 ellipsoid((0.0, 0.20, 0.27), (0.03, 0.012, 0.05))]
    else:  # hyottoko
        face = ellipsoid((0.0, 0.48, 0.0), (0.35, 0.48, 0.29))
        parts += [capsule((0.03, 0.22, 0.25), (0.12, 0.21, 0.33), 0.05, 0.035),             # the pursed mouth, to one side
                  capsule((0.0, 0.52, 0.26), (0.0, 0.40, 0.31), 0.03, 0.04),
                  mirror_x(ellipsoid((0.20, 0.30, 0.18), (0.10, 0.09, 0.09)))]
        cuts += [sphere((0.13, 0.56, 0.275), 0.045), sphere((-0.14, 0.58, 0.27), 0.032),
                 torus((0.12, 0.215, 0.36), 0.018, 0.008, rz=90.0, rx=0.0)]
    m = U(face, *parts, k=0.04)
    if cuts:
        m = S(m, *cuts, k=0.008)
    m = I(m, cut_back)
    top = 1.22 if kind == "oni" else 1.02
    return [Part("mask", m, (-0.42, -0.15, 0.0), (0.42, top, 0.40), 0.008, share=1.0)]
