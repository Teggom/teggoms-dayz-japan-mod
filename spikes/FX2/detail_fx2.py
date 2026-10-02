"""detail_fx2.py - FX2 (2026-10-01): the wave-2 detail props remade under PLAYBOOK §12's detail budget (<= 1,500;
Stephen: 'small detail items ... are what make the world pop'). spikes/W2F/props_w2f_sacred.py delegates to these
(same p3d names, frames, mounts and hang points as before):

  kagura_masks()  four sculpted masks (okina, oni, okame, hyottoko; CMA 149100 / 147048 / 147046 / 148010) on pegs
                  + a real kagura bell tree (15 bells in 3 tiers, 5 ribbons)
  waniguchi()     the flat 'crocodile mouth' gong: hollow body, the mouth slit round the lower rim, relief rings and
                  a lotus boss on the face, hanging lugs; a twisted 3-colour pull rope with a fringed tassel
  suzu_rope()     the shrine bell: a slotted crotal with its loop and rim, the red / white rope twisted, a knot and a
                  fringed tassel
  bonsho_body()   the temple bell: 32 sides, the nipples (nyu) in four panels, vertical + horizontal bands, the lotus
                  striking seats, the two-headed dragon lug (ryuzu) with its jewel
  ema_rail()      pentagonal ema boards with a roof bevel, painted panels (a horse, a lion, a fox), red cords, in two
                  overlapping rows + one framed gaku-ema with a little roof above (Met 36108, 1631)
  saisen_box()    the offering box: six inclined slats a side, iron corner straps with nail heads, the front crest
                  (mitsudomoe, the Hachiman crest) in bronze, a hasp
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "spikes", "S1"), os.path.join(DEV, "spikes", "L1"), os.path.join(DEV, "spikes", "B3b"),
          os.path.join(DEV, "spikes", "B3a"), HERE):
    if p not in sys.path:
        sys.path.append(p)
from s1kit import (core, box, prism, lathe, xf, W, col, LPart, pole, cord, lod_box, wear_all, peg, rng,  # noqa: E402
                   WOOD, WEATH, IRON, DARK, KINARI, INDIGO, RED, PAPER, FUSUMA)
import ropekit  # noqa: E402

BRONZE = "metal_bronze"
PAINT = "paint_shu"
KURO = "wood_kuro"
NEW = "wood_new"
SILVER = "wood_silver"
LACQ_SHU = "lacquer_shu"


def mv(ss, t):
    return [xf(s, t=t) for s in ss]


def _w(s, wear):
    if wear:
        s.wear = wear
    return s


def twisted(p0, p1, r, mats, turns=3.0, seg=14, wear=None, vis=(1,)):
    """len(mats) strands twisted round the line p0 -> p1 (a cloth / straw rope)."""
    out = []
    n = len(mats)
    L = [p1[i] - p0[i] for i in range(3)]
    for k, m in enumerate(mats):
        pts = []
        for i in range(seg + 1):
            t = i / seg
            a = 2 * math.pi * (turns * t + k / n)
            off = r * 0.75
            pts.append((p0[0] + L[0] * t + off * math.cos(a), p0[1] + L[1] * t, p0[2] + L[2] * t + off * math.sin(a)))
        s = ropekit.tube(pts, r * 0.62, 6, m, vis=vis, wear=wear)
        if s is not None:
            out.append(s)
    return out


def fringe(p, length, r, mat, n=8, wear=None, seed=1, vis=(1,)):
    """A cloth / straw tassel: a bound collar and n strands fanning out and down."""
    rg = random.Random(seed)
    out = [_w(lathe([(0.0, 0.0), (r * 1.15, 0.0), (r * 1.2, -0.03), (r * 1.1, -0.06), (0.0, -0.06)], 8, mat, vis=vis),
              wear)]
    out[-1] = xf(out[-1], t=p)
    for k in range(n):
        a = 2 * math.pi * k / n + rg.uniform(-0.2, 0.2)
        q0 = (p[0] + r * 0.8 * math.cos(a), p[1] - 0.05, p[2] + r * 0.8 * math.sin(a))
        q1 = (p[0] + r * 1.6 * math.cos(a), p[1] - length * rg.uniform(0.85, 1.0), p[2] + r * 1.6 * math.sin(a))
        out.append(pole(q0, q1, r * 0.28, mat, n=4, vis=vis, r1=r * 0.12, wear=wear))
    return out


# ================================================================================================ kagura masks
def kagura_masks():
    import fx2props as FX
    P = LPart("kagura_masks", budget="detail_l", mass=3.0, anchor="wall", flat=True)   # 4 masks + the bell tree
    y = 1.50
    out = [W(-0.55, 0.55, y + 0.08, y + 0.14, 0.0, 0.022, WEATH)]
    masks = [(-0.42, "mask_okina", FUSUMA), (-0.17, "mask_oni", PAINT), (0.08, "mask_okame", FUSUMA),
             (0.31, "mask_hyottoko", NEW)]
    for x, name, mat in masks:
        out.append(peg(x, y + 0.11, L=0.05, z0=0.0))
        out.append(cord((x, y + 0.11, 0.045), (x, y + 0.075, 0.03), 0.003))
        hi = FX.figure(name, 0.20, mat, vis=((1,), (2,), ()), t=(x, y - 0.13, 0.012), wear="_w1")
        out += [s for s in hi]
        # a dark backing behind the mask: its eye and mouth holes read black against any wall
        back = lathe([(0.055, 0.001), (0.0, 0.001)], 8, DARK, vis=(1,), smooth=False)            # one face-on disc
        out.append(xf(xf(back, rx=90.0), t=(x, y - 0.03, 0.009)))
        out[-1].verts = [(v[0], (v[1] - (y - 0.03)) * 1.55 + (y - 0.03), v[2]) for v in out[-1].verts]
    # the kagura bell tree (kagura-suzu), hung by its crown: three tiers of bells (3 / 5 / 7) on wire rings under
    # the peg, the handle below them, five ribbons from the handle's end
    bx = 0.47
    z = 0.065
    out.append(peg(bx, y + 0.11, L=0.05, z0=0.0))
    out.append(cord((bx, y + 0.11, 0.045), (bx, y + 0.07, z), 0.003))
    bell = lambda c: lathe([(0.0, -0.013), (0.012, -0.006), (0.010, 0.008), (0.0, 0.013)], 5, BRONZE,  # noqa
                           vis=(1,))
    out.append(pole((bx, y + 0.07, z), (bx, y - 0.03, z), 0.006, BRONZE, n=6, vis=(1,)))      # the bell stem
    for tier, (n, rr, yy) in enumerate(((3, 0.018, y + 0.05), (5, 0.030, y + 0.015), (7, 0.042, y - 0.02))):
        ring = lathe([(rr - 0.002, -0.002), (rr + 0.002, -0.002), (rr + 0.002, 0.002), (rr - 0.002, 0.002),
                      (rr - 0.002, -0.002)], 10, BRONZE, vis=(1,), smooth=False)
        out.append(xf(ring, t=(bx, yy + 0.016, z)))
        for k in range(n):
            a = 2 * math.pi * (k + 0.5 * tier) / n
            out.append(xf(bell(0), t=(bx + rr * math.cos(a), yy, z + rr * math.sin(a))))
    hy0, hy1 = y - 0.03, y - 0.21
    out.append(pole((bx, hy0, z), (bx, hy1, z), 0.010, KURO, n=6, vis=(1,)))
    for k, m in enumerate((RED, KINARI, INDIGO, PAINT, KINARI)):
        x0 = bx - 0.02 + 0.01 * k
        q = [(x0, hy1, z), (x0 + 0.012, hy1, z), (x0 + 0.014 + 0.01 * (k - 2), hy1 - 0.30, z + 0.005),
             (x0 + 0.002 + 0.01 * (k - 2), hy1 - 0.30, z + 0.005)]
        out.append(core.sheet([q, q[::-1]], m, [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)], vis=(1,)))
    wear_all(out, "_w2")
    P.adds(out)
    P.add(W(-0.55, 0.55, y - 0.25, y + 0.14, 0.0, 0.10, WEATH, vis=(2,)))
    P.dim("width", 1.10, 1.10, tol=0.005)
    P.notes.append("FX2: four sculpted kagura masks (okina, oni, okame, hyottoko) on pegs + the kagura bell tree "
                   "(15 bells, 5 ribbons), stage back wall (mount wall)")
    return P


# ================================================================================================ waniguchi
def waniguchi():
    P = LPart("waniguchi", budget="detail", mass=6.0, anchor="hang", flat=True)
    out = []
    gy = -0.10 - 0.22
    R, T = 0.22, 0.05
    # the body: a flattened hollow bell seen face on: the face with relief rings and a lotus boss, the rim bulging
    # out round the edge, the mouth slit along the lower half of the rim (a dark band)
    prof = [(0.0, T + 0.006), (0.035, T + 0.010), (0.05, T + 0.004), (0.075, T), (0.078, T + 0.005), (0.083, T),
            (0.13, T - 0.004), (0.135, T + 0.002), (0.14, T - 0.004), (0.185, T - 0.010), (R - 0.008, T - 0.008),
            (R, T * 0.45), (R + 0.006, 0.0), (R, -T * 0.45), (R - 0.008, -T + 0.008), (0.14, -T + 0.004),
            (0.0, -T)]
    g = lathe(prof, 28, BRONZE, vis=(1,))
    out.append(xf(g, rx=90.0, t=(0.0, gy, 0.0)))
    # the mouth: a dark slit band round the lower rim (from 4 to 8 o'clock)
    for k in range(9):
        a0 = math.radians(205 + k * 14.5)
        a1 = math.radians(205 + (k + 1) * 14.5)
        rr = R + 0.0065
        q = [(rr * math.cos(a0), gy + rr * math.sin(a0), -0.006), (rr * math.cos(a1), gy + rr * math.sin(a1), -0.006),
             (rr * math.cos(a1), gy + rr * math.sin(a1), 0.006), (rr * math.cos(a0), gy + rr * math.sin(a0), 0.006)]
        n = (math.cos((a0 + a1) / 2), math.sin((a0 + a1) / 2), 0.0)
        out.append(core.sheet([q], DARK, n, vis=(1,)))
    # the two hanging lugs (mimi) at the top sides, with their cords up to the beam
    for sx in (-1, 1):
        lug = lathe([(0.012, -0.008), (0.024, -0.008), (0.024, 0.008), (0.012, 0.008), (0.012, -0.008)], 10, BRONZE,
                    vis=(1,), smooth=False)
        cx, cy = sx * 0.13, gy + 0.18
        out.append(xf(lug, rx=90.0, t=(cx, cy, 0.0)))
        out.append(cord((cx, cy + 0.02, 0.0), (sx * 0.12, 0.0, 0.0), 0.006))
    # the pull rope (zenno-tsuna): three faded strands twisted, a knot and a fringed tassel, hanging in front
    z = 0.10
    out += twisted((0.0, gy + 0.06, z), (0.0, gy - 1.32, z), 0.026, (RED, KINARI, INDIGO), turns=6.0, seg=30,
                   wear="_w2")
    out.append(_w(xf(lathe([(0.0, -0.03), (0.032, -0.02), (0.036, 0.0), (0.032, 0.02), (0.0, 0.03)], 8, KINARI,
                           vis=(1,)), t=(0.0, gy - 1.34, z)), "_w2"))
    out += fringe((0.0, gy - 1.37, z), 0.24, 0.028, KINARI, n=9, wear="_w2", seed=7)
    out.append(cord((0.0, gy + 0.06, z), (0.0, gy + 0.21, 0.02), 0.006))
    wear_all([s for s in out if not getattr(s, "wear", None)], "_w1")
    P.adds(out)
    P.add(box(-0.22, 0.22, gy - 0.22, gy + 0.22, -0.05, 0.05, BRONZE, vis=(2,)))
    P.add(box(-0.03, 0.03, gy - 1.60, gy, z - 0.03, z + 0.03, KINARI, vis=(2,)))
    P.finish_hang()
    P.dim("d", 0.44, 0.44, tol=0.02)
    P.notes.append("FX2: the flat 'crocodile mouth' gong (waniguchi): hollow body, mouth slit, relief rings + lotus "
                   "boss, lugs; the twisted pull rope with a fringed tassel (mount beam); hangs %.2f m" % P.hang_len)
    return P


# ================================================================================================ suzu
def suzu_rope(faded=False):
    P = LPart("suzu", budget="detail", mass=2.0, anchor="hang", flat=True)
    wr = "_w2" if faded else "_w1"
    out = [box(-0.006, 0.006, -0.07, 0.0, -0.006, 0.006, IRON, vis=(1,)),
           pole((0.0, -0.07, 0.0), (0.0, -0.09, 0.0), 0.02, IRON, n=8, vis=(1,))]
    r = 0.12
    cy = -0.09 - 0.03 - r
    prof = [(0.0, -r)] + [(r * math.sin(math.pi * k / 10), -r * math.cos(math.pi * k / 10)) for k in range(1, 10)] + \
        [(0.0, r)]
    out.append(xf(lathe(prof, 16, BRONZE, vis=(1,)), t=(0.0, cy, 0.0)))
    out.append(xf(lathe([(r * 1.005, -0.006), (r * 1.02, -0.006), (r * 1.02, 0.006), (r * 1.005, 0.006)], 16, BRONZE,
                        vis=(1,), smooth=False), t=(0.0, cy, 0.0)))                       # the equator rim
    # the slot (a dark band low on the front and back) and the two sound holes
    for sz in (-1, 1):
        out.append(box(-r * 0.70, r * 0.70, cy - r * 0.56, cy - r * 0.48, sz * r * 0.55 - 0.03, sz * r * 0.55 + 0.03,
                       DARK, vis=(1,)))
    lp = lathe([(0.016, -0.005), (0.030, -0.005), (0.030, 0.005), (0.016, 0.005), (0.016, -0.005)], 10, BRONZE,
               vis=(1,), smooth=False)
    out.append(xf(lp, rx=90.0, t=(0.0, cy + r + 0.022, 0.0)))                           # the top loop
    # the rope (suzu-no-o): red and white cloth twisted, a knot, a fringed tassel
    y0, y1 = cy - r - 0.01, cy - r - 1.10
    out += twisted((0.0, y0, 0.0), (0.0, y1, 0.0), 0.030, (RED, KINARI), turns=7.0, seg=34, wear=wr)
    out.append(_w(xf(lathe([(0.0, -0.035), (0.04, -0.02), (0.045, 0.0), (0.04, 0.02), (0.0, 0.035)], 10, KINARI,
                           vis=(1,)), t=(0.0, y1 - 0.03, 0.0)), wr))
    out += fringe((0.0, y1 - 0.06, 0.0), 0.30, 0.034, RED, n=10, wear=wr, seed=3)
    P.adds(out)
    P.add(box(-0.12, 0.12, cy - r, -0.07, -0.12, 0.12, BRONZE, vis=(2,)))
    P.add(box(-0.03, 0.03, y1 - 0.36, cy - r, -0.03, 0.03, RED, vis=(2,)))
    P.finish_hang()
    P.dim("bell_d", 0.24, 2 * r, tol=0.01)
    P.notes.append("FX2: the shrine bell (slotted crotal, rim, loop) with its twisted red / white rope, knot and fringed "
                   "tassel (mount beam); hangs %.2f m; faded = the red gone pink-grey" % P.hang_len)
    return P


# ================================================================================================ bonsho body
def bonsho_body(H, D, y0, mat=BRONZE):
    """The bell itself (hook at y 0 above it, the body from y0 down H): 32 sides, the nyu (nipples) in four panels
    in the upper zone, four vertical bands + two horizontal belts (kesadasuki), the lotus striking seats (tsukiza) on
    both sides, the two-headed dragon lug (ryuzu) with its jewel. Returns (solids, striking-seat y)."""
    R = D / 2
    out = []
    prof = [(0.0, y0), (R * 0.55, y0), (R * 0.80, y0 - 0.02), (R * 0.92, y0 - 0.06), (R * 0.95, y0 - 0.12),
            (R * 0.97, y0 - H * 0.6), (R * 0.99, y0 - H * 0.85), (R, y0 - H + 0.04), (R * 1.025, y0 - H + 0.01),
            (R * 1.02, y0 - H), (R * 0.90, y0 - H), (R * 0.88, y0 - H + 0.06), (0.0, y0 - H + 0.06)]
    out.append(lathe(prof, 32, mat, vis=(1,)))
    for f in (0.38, 0.66):                                                     # horizontal belts
        yb = y0 - H * f
        rb = R * (0.965 + 0.02 * f)
        out.append(lathe([(rb, yb - 0.022), (rb + 0.012, yb - 0.018), (rb + 0.012, yb + 0.018), (rb, yb + 0.022)],
                         32, mat, vis=(1,), smooth=False))
    for k in range(4):                                                         # vertical bands
        a = math.pi / 4 + k * math.pi / 2
        for (ya, yb_) in ((y0 - 0.10, y0 - H * 0.38), (y0 - H * 0.38, y0 - H * 0.66)):
            rr = R * 0.975
            b = box(-0.018, 0.018, yb_, ya, rr - 0.004, rr + 0.012, mat, vis=(1,))   # at +z, turned to angle a
            out.append(xf(b, ry=math.degrees(a) - 90.0))
    # nyu: 4 panels between the vertical bands, 3 rows x 3 knobs each, in the upper zone
    knob = lathe([(0.0, 0.0), (0.016, 0.0), (0.014, 0.010), (0.007, 0.016), (0.0, 0.018)], 6, mat, vis=(1,))
    for k in range(4):
        ac = k * math.pi / 2
        for row in range(3):
            yk = y0 - 0.16 - row * (H * 0.38 - 0.20) / 2.5
            for c in (-1, 0, 1):
                a = ac + c * 0.20
                rr = R * 0.958
                kk = xf(knob, rx=90.0)                       # point it along +z, then turn +z to angle a
                out.append(xf(kk, ry=math.degrees(a) - 90.0, t=(rr * math.cos(a), yk, rr * math.sin(a))))
    ys = y0 - H * 0.80
    for sx in (-1, 1):                                                         # lotus striking seats
        seat = lathe([(0.0, 0.0), (0.075, 0.0), (0.08, 0.008), (0.06, 0.02), (0.03, 0.026), (0.0, 0.028)], 12, mat,
                     vis=(1,))
        out.append(xf(seat, rz=-90.0 * sx, t=(sx * R * 0.985, ys, 0.0)))
        for p in range(8):
            a = 2 * math.pi * p / 8
            pt = lathe([(0.0, 0.0), (0.012, 0.0), (0.0, 0.016)], 4, mat, vis=(1,))
            out.append(xf(pt, rz=-90.0 * sx, t=(sx * (R * 0.985 + 0.005), ys + 0.055 * math.cos(a),
                                               0.055 * math.sin(a))))
    # ryuzu: two dragon heads back to back biting the crown, their bodies forming the arch the hook goes through,
    # a jewel (hoju) on top
    for sx in (-1, 1):
        head = lathe([(0.0, -0.05), (0.04, -0.035), (0.05, 0.0), (0.035, 0.04), (0.0, 0.05)], 8, mat, vis=(1,))
        out.append(xf(head, rz=sx * 60.0, t=(sx * 0.075, y0 + 0.03, 0.0)))
        snout = pole((sx * 0.075, y0 + 0.02, 0.0), (sx * 0.13, y0 + 0.005, 0.0), 0.022, mat, n=6, vis=(1,), r1=0.012)
        out.append(snout)
        out.append(pole((sx * 0.06, y0 + 0.06, 0.0), (sx * 0.025, y0 + 0.105, 0.0), 0.022, mat, n=6, vis=(1,)))
    out.append(pole((-0.03, y0 + 0.11, 0.0), (0.03, y0 + 0.11, 0.0), 0.022, mat, n=8, vis=(1,)))
    out.append(xf(lathe([(0.0, 0.0), (0.022, 0.008), (0.019, 0.024), (0.0, 0.034)], 8, mat, vis=(1,)),
                  t=(0.0, y0 + 0.12, 0.0)))                                    # the jewel: top 4.6 cm under the hook
    return out, ys


# ================================================================================================ ema
HORSE = [(-0.040, -0.012), (-0.030, 0.010), (-0.010, 0.014), (0.022, 0.012), (0.036, 0.030), (0.046, 0.026),
         (0.040, 0.006), (0.030, -0.004), (0.026, -0.028), (0.018, -0.028), (0.014, -0.006), (-0.020, -0.006),
         (-0.026, -0.028), (-0.034, -0.028)]


def _poly_fan(pts, z, mat, vis=(1,)):
    """A flat polygon facing +z, as a fan of triangles from its centroid (works for a concave outline drawn round the
    centroid, as the horse is)."""
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    tris = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        tris.append([(cx, cy, z), (a[0], a[1], z), (b[0], b[1], z)])
    s = core.sheet(tris, mat, (0.0, 0.0, 1.0), vis=vis)
    return s


def ema_rail(n=14):
    P = LPart("ema_rail", budget="detail", mass=4.0, anchor="wall", flat=True)
    L, y = 1.20, 1.45
    out = [W(-L / 2, L / 2, y, y + 0.05, 0.0, 0.035, WEATH), W(-L / 2, L / 2, y - 0.22, y - 0.17, 0.0, 0.035, WEATH)]
    for sx in (-1, 1):
        out.append(W(sx * (L / 2 - 0.03) - 0.025, sx * (L / 2 - 0.03) + 0.025, y - 0.30, y + 0.06, 0.0, 0.02, WEATH,
                     vis=(1,)))
    r = rng("ema_rail_fx2")
    w, h, t = 0.15, 0.105, 0.010
    pent = [(-w / 2, 0.0), (w / 2, 0.0), (w / 2, h * 0.72), (0.0, h), (-w / 2, h * 0.72)]
    for row, (ry, k) in enumerate(((y - 0.01, n // 2), (y - 0.18, n - n // 2))):
        for i in range(k):
            x = -L / 2 + 0.09 + i * (L - 0.18) / (k - 1) + r.uniform(-0.015, 0.015) + 0.03 * (row % 2)
            mat = (NEW, SILVER, WEATH)[(i + row) % 3]
            zf = 0.04 + 0.011 * (i % 2)
            rz = r.uniform(-7, 7)
            e = [prism(pent, "z", 0.0, t, mat, vis=(1,)),
                 prism([(-w / 2 + 0.008, h * 0.72 - 0.004), (w / 2 - 0.008, h * 0.72 - 0.004), (0.0, h - 0.008)],
                       "z", t, t + 0.004, mat, vis=(1,))]                         # the roof bevel strip
            pick = (i + 2 * row) % 3
            if pick == 0:
                e.append(xf(_poly_fan(HORSE, t + 0.0015, DARK), t=(0.0, 0.040, 0.0)))   # the painted horse
            elif pick == 1:
                e.append(xf(_poly_fan([(x_ * 0.8, y_ * 0.8) for x_, y_ in HORSE], t + 0.0015, PAINT), t=(0.0, 0.04, 0.0)))
            else:
                e.append(W(-0.045, 0.045, 0.015, 0.06, t, t + 0.0015, KURO, vis=(1,)))     # a written wish (faded)
            e.append(cord((-0.02, h * 0.80, t + 0.003), (0.0, h + 0.03, 0.004), 0.0025, mat=RED))
            e.append(cord((0.02, h * 0.80, t + 0.003), (0.0, h + 0.03, 0.004), 0.0025, mat=RED))
            for s in e:
                out.append(xf(xf(s, t=(0.0, -h - 0.03, 0.0)), rz=rz, t=(x, ry, zf)))
    # the framed gaku-ema above the rail (Met 36108, 1631): a board in a frame under a little roof
    gy = y + 0.12
    gw, gh = 0.62, 0.42
    out.append(W(-gw / 2, gw / 2, gy, gy + gh, 0.0, 0.025, WEATH))
    for (x0, x1, y0_, y1_) in ((-gw / 2 - 0.02, gw / 2 + 0.02, gy - 0.02, gy), (-gw / 2 - 0.02, gw / 2 + 0.02, gy + gh,
                                                                                   gy + gh + 0.02),
                               (-gw / 2 - 0.02, -gw / 2, gy, gy + gh), (gw / 2, gw / 2 + 0.02, gy, gy + gh)):
        out.append(W(x0, x1, y0_, y1_, 0.0, 0.035, KURO, vis=(1,)))
    out.append(xf(_poly_fan([(x_ * 4.2, y_ * 4.2) for x_, y_ in HORSE], 0.0265, DARK), t=(0.06, gy + 0.20, 0.0)))
    out.append(W(-gw / 2 + 0.04, -gw / 2 + 0.14, gy + 0.10, gy + 0.26, 0.025, 0.0265, PAINT, vis=(1,)))   # peony
    ap = (0.0, gy + gh + 0.10, 0.0)                                           # the two roof boards over it
    out.append(xf(W(0.0, gw / 2 + 0.08, -0.008, 0.008, 0.0, 0.10, WEATH, vis=(1,)), rz=-22.0, t=ap))
    out.append(xf(W(-gw / 2 - 0.08, 0.0, -0.008, 0.008, 0.0, 0.10, WEATH, vis=(1,)), rz=22.0, t=ap))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(W(-L / 2, L / 2, y - 0.32, y + 0.05, 0.0, 0.05, WEATH, vis=(2,)))
    P.add(W(-gw / 2, gw / 2, gy, gy + gh + 0.12, 0.0, 0.05, WEATH, vis=(2,)))
    P.dim("length", L, L, tol=0.005)
    P.notes.append("FX2: votive boards (ema) in two rows on a rail (pentagonal, roof bevel, painted horses / wishes, "
                   "red cords) + a framed gaku-ema under a little roof above it (Met 36108); haiden wall (mount wall)")
    return P


# ================================================================================================ offering box
def saisen_box(w, d, h, wear="_w1", crest=True):
    P = LPart("saisen_bako", budget="detail", mass=35.0, anchor="floor")
    t = 0.035
    out = [W(-w / 2, w / 2, 0.0, 0.07, -d / 2 + 0.03, -d / 2 + 0.09, WEATH),          # two runners
           W(-w / 2, w / 2, 0.0, 0.07, d / 2 - 0.09, d / 2 - 0.03, WEATH),
           W(-w / 2, w / 2, 0.07, h, d / 2 - t, d / 2, WEATH),                            # front
           W(-w / 2, w / 2, 0.07, h, -d / 2, -d / 2 + t, WEATH),                          # back
           W(-w / 2, -w / 2 + t, 0.07, h, -d / 2 + t, d / 2 - t, WEATH),                  # ends
           W(w / 2 - t, w / 2, 0.07, h, -d / 2 + t, d / 2 - t, WEATH),
           W(-w / 2 + t, w / 2 - t, 0.07, 0.10, -d / 2 + t, d / 2 - t, WEATH, vis=(1,)),   # bottom
           W(-w / 2 - 0.012, w / 2 + 0.012, h - 0.04, h, d / 2 - 0.004, d / 2 + 0.014, WEATH, vis=(1,)),  # top rails
           W(-w / 2 - 0.012, w / 2 + 0.012, h - 0.04, h, -d / 2 - 0.014, -d / 2 + 0.004, WEATH, vis=(1,)),
           W(-w / 2 - 0.006, w / 2 + 0.006, 0.07, 0.095, d / 2, d / 2 + 0.008, WEATH, vis=(1,))]      # bottom rail
    inner = d / 2 - t
    k = 6
    pitch = inner / k
    for side in (-1, 1):                                          # six inclined slats a side, falling to the middle
        for i in range(k):
            zc = side * (pitch * (i + 0.5))
            yc = h - 0.03 - (inner - abs(zc)) * 0.30
            s = W(-w / 2 + t, w / 2 - t, -0.006, 0.006, -pitch * 0.40, pitch * 0.40, WEATH, vis=(1,))
            out.append(xf(s, rx=side * 22.0, t=(0.0, yc, zc)))
    for sx in (-1, 1):                                            # iron corner straps with nail heads
        for sz in (-1, 1):
            x0, z0 = sx * w / 2, sz * d / 2
            out.append(box(min(x0, x0 - sx * 0.10), max(x0, x0 - sx * 0.10), h - 0.13, h, z0 - 0.004, z0 + 0.004,
                           IRON, vis=(1,)))
            out.append(box(x0 - 0.004, x0 + 0.004, h - 0.13, h, min(z0, z0 - sz * 0.08), max(z0, z0 - sz * 0.08),
                           IRON, vis=(1,)))
            for (dx, dy) in ((0.03, 0.04), (0.07, 0.09)):
                nail = lathe([(0.0, 0.0), (0.008, 0.0), (0.006, 0.004), (0.0, 0.005)], 5, IRON, vis=(1,))
                out.append(xf(nail, rx=sz * 90.0, t=(x0 - sx * dx, h - dy, z0 + sz * 0.004)))
    if crest:                                                     # the mitsudomoe crest in bronze on the front
        cy = (h + 0.07) / 2 + 0.02
        disc = lathe([(0.0, 0.0), (0.075, 0.0), (0.075, 0.006), (0.068, 0.010), (0.0, 0.010)], 16, BRONZE, vis=(1,))
        out.append(xf(disc, rx=90.0, t=(0.0, cy, d / 2)))
        for c in range(3):
            a = 2 * math.pi * c / 3 + 0.5
            head = lathe([(0.0, 0.0), (0.020, 0.0), (0.018, 0.006), (0.0, 0.008)], 8, BRONZE, vis=(1,))
            out.append(xf(head, rx=90.0, t=(0.035 * math.cos(a), cy + 0.035 * math.sin(a), d / 2 + 0.010)))
            for j in range(3):                                    # the comma's tail curling round
                b_ = a + 0.6 + 0.35 * j
                rr = 0.045 + 0.006 * j
                out.append(box(-0.006, 0.006, -0.006, 0.006, 0.0, 0.006, BRONZE, vis=(1,)))
                out[-1] = xf(out[-1], t=(rr * math.cos(b_), cy + rr * math.sin(b_), d / 2 + 0.010))
    hasp = W(w / 2 - 0.004, w / 2 + 0.006, h - 0.22, h - 0.12, -0.02, 0.02, IRON, vis=(1,))
    out.append(hasp)
    wear_all(out, wear)
    P.adds(out)
    P.add(lod_box([s for s in out if 1 in s.vis], WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.dim("w", w, w, tol=0.03)
    P.dim("h", h, h, tol=0.005)
    P.notes.append("FX2: offering box (saisen-bako): six slats a side, iron straps with nails, the bronze mitsudomoe "
                   "crest on the front, a hasp; undisturbed, no loot (G1 A2-12)")
    return P
