"""fp1sword - FP1 (2026-10-01) remake of the sword rack (L1 #45, Stephen: "just squares").

Forms (general knowledge, no web request; recorded in spikes/FP1/FP1_PROGRESS.md 'Forms'):
- A katana (daito, ~1.00 m in its mounts: blade ~0.70 in the scabbard, hilt ~0.25) and a wakizashi (~0.65 m) in their
  koshirae: a black-lacquered scabbard (saya) of oval section, taller than wide (the blade's height), tapering to a
  horn end cap (kojiri); a mouth band (koiguchi) and the cord knob (kurikata) a hand's width from the mouth, the
  flat cotton cord (sageo) threaded through it and wound round the scabbard; a round iron guard (tsuba, d ~7.5 cm,
  5 mm) between two washers (seppa); the hilt (tsuka) of oval section, its white rayskin (samegawa) showing in the
  diamonds of the crossed cord wrap (tsuka-ito, hishigami), an iron collar (fuchi) and pommel cap (kashira).
- The curve (sori, ~1.8 cm on a katana) is in the whole mount; the edge is on the convex side.
- On a sword stand (katana-kake) the swords lie edge up, hilt to the viewer's LEFT (the peaceful display), the long
  sword on the lower arms, the short one above. The stand: a lacquered base board on two feet, two uprights with
  shaped tops, each upright with forward arms that curl up at the tip to cradle the scabbard.
Frame (L1): origin = base centre on the floor, +z = front, the swords along x, hilt at +x (the viewer's left when
facing the rack from +z in DayZ's left-handed frame).
"""
import math
import random

import lkit
from lkit import core, box, prism, lathe, xf, xfs, W, pole  # noqa: F401

LACQ = "lacquer_black"
IRON = "metal_iron"
INDIGO = "textile_cotton_indigo"
PLAIN = "textile_cotton_plain"
HORN = "wood_kuro"


def _sweep(path, prof, sides, mat, vis=(1,), wear=None, caps=(True, True), up=(0.0, 1.0, 0.0)):
    """An oval tube along `path` (points along x mostly): prof(t) -> (h, w), h along the in-plane normal (up), w
    along z; smooth normals; closed ends."""
    n = len(path)
    T = []
    for i in range(n):
        a, b = path[max(0, i - 1)], path[min(n - 1, i + 1)]
        T.append(core.norm(core.sub(b, a)))
    quads, normals, uvs, vn = [], [], [], []
    rings, dirs = [], []
    acc = [0.0]
    for i in range(1, n):
        acc.append(acc[-1] + core.length(core.sub(path[i], path[i - 1])))
    for i, c in enumerate(path):
        t = acc[i] / acc[-1] if acc[-1] else 0.0
        h, w = prof(t)
        nz = (0.0, 0.0, 1.0)
        ny = core.norm(core.cross(nz, T[i]))             # in-plane normal (up for a path along +x)
        if ny[1] < 0:
            ny = core.mul(ny, -1.0)
        ring, dr = [], []
        for k in range(sides):
            a = 2 * math.pi * k / sides + math.pi / sides
            d = core.add(core.mul(ny, math.sin(a) * h / 2), core.mul(nz, math.cos(a) * w / 2))
            ring.append(core.add(c, d))
            dr.append(core.norm(core.add(core.mul(ny, math.sin(a) / max(h, 1e-4)), core.mul(nz, math.cos(a) / max(w, 1e-4)))))
        rings.append(ring)
        dirs.append(dr)
    for i in range(n - 1):
        for k in range(sides):
            k2 = (k + 1) % sides
            q = [rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]]
            quads.append(q)
            normals.append(core.norm(core.add(core.add(dirs[i][k], dirs[i][k2]), core.add(dirs[i + 1][k], dirs[i + 1][k2]))))
            uvs.append([(k / sides * 0.2, acc[i] / 0.5), ((k + 1) / sides * 0.2, acc[i] / 0.5),
                        ((k + 1) / sides * 0.2, acc[i + 1] / 0.5), (k / sides * 0.2, acc[i + 1] / 0.5)])
            vn.append([dirs[i][k], dirs[i][k2], dirs[i + 1][k2], dirs[i + 1][k]])
    for end, on in ((0, caps[0]), (n - 1, caps[1])):
        if not on:
            continue
        tn = core.mul(T[end], -1.0 if end == 0 else 1.0)
        c = path[end]
        for k in range(sides):
            quads.append([c, rings[end][k], rings[end][(k + 1) % sides]])
            normals.append(tn)
            uvs.append([(0.5, 0.5), (0.5 + 0.05 * math.cos(2 * math.pi * k / sides), 0.5),
                        (0.5, 0.5 + 0.05 * math.sin(2 * math.pi * k / sides))])
            vn.append([tn, tn, tn])
    s = core.sheet(quads, mat, normals, vis=vis, uvs=uvs)
    s.finalize()
    s.vn = vn
    if wear:
        s.wear = wear
    return s


def sword(L=1.00, sori=0.018, wear=None, seed=1, vis=(1,)):
    """A sword in its mounts lying along +x from x = 0 (the scabbard end) to x = L (the pommel), edge up (the
    convex side up: the middle is higher than the ends by `sori`). Centre line at y = 0 at the ends."""
    rg = random.Random(seed)
    hilt = 0.255 if L > 0.8 else 0.19
    xg = L - hilt                                        # the guard plane
    def cy(x):
        t = x / L
        return sori * 4 * t * (1 - t)
    out = []
    # scabbard: oval, 3.2 x 2.3 cm at the mouth tapering to 2.6 x 1.8 near the end; 8 sides, 9 stations
    xs = [0.012 + (xg - 0.020) * i / 8 for i in range(9)]
    out.append(_sweep([(x, cy(x), 0.0) for x in xs], lambda t: (0.026 + 0.006 * t, 0.018 + 0.005 * t), 6, LACQ,
                      vis=vis, wear=wear))
    out.append(_sweep([(0.0, cy(0.0), 0.0), (0.014, cy(0.014), 0.0)], lambda t: (0.024 + 0.004 * t, 0.017 + 0.003 * t), 8,
                      HORN, vis=vis, wear=wear))                                        # kojiri (horn end cap)
    km = xg - 0.020
    out.append(_sweep([(km - 0.012, cy(km - 0.012), 0.0), (km + 0.004, cy(km), 0.0)], lambda t: (0.034, 0.025), 8, HORN,
                      vis=vis, wear=wear))                                              # koiguchi (mouth band)
    xk = xg - 0.12                                                                      # kurikata (cord knob)
    out.append(box(xk - 0.012, xk + 0.012, cy(xk) - 0.010, cy(xk) + 0.006, 0.010, 0.022, HORN, vis=vis))
    # sageo: the flat cord through the knob, wound twice round the scabbard toward the end, the tail hanging free
    pts = []
    for i in range(17):
        a = 2 * math.pi * 2 * i / 16
        x = xk - 0.05 - 0.13 * i / 16
        pts.append((x, cy(x) + 0.0175 * math.sin(a), 0.0145 * math.cos(a)))
    pts = [(xk, cy(xk) - 0.002, 0.019)] + pts
    out.append(_cord(pts, 0.0035, INDIGO, vis, wear))
    tail = [pts[-1], (pts[-1][0] - 0.03, cy(pts[-1][0]) - 0.04, 0.02), (pts[-1][0] - 0.05, cy(pts[-1][0]) - 0.09, 0.03)]
    out.append(_cord(tail, 0.0035, INDIGO, vis, wear))
    # guard: two washers and the tsuba (round iron plate, two small openings suggested by a darker inner ring)
    for dx, r, th in ((-0.006, 0.020, 0.003), (0.0, 0.0375, 0.005), (0.006, 0.020, 0.003)):
        ring = lathe([(0.0, -th / 2), (r, -th / 2), (r, th / 2), (0.0, th / 2)], 10 if r > 0.03 else 6, IRON,
                     vis=vis, smooth=False)
        out.append(xf(ring, rz=90.0, t=(xg + dx, cy(xg), 0.0)))
    # hilt: collar, the wrapped grip (white rayskin core, crossed indigo cord diamonds on both faces), pommel cap
    out.append(_sweep([(xg + 0.008, cy(xg + 0.008), 0.0), (xg + 0.024, cy(xg + 0.024), 0.0)], lambda t: (0.030, 0.023), 8,
                      IRON, vis=vis, wear=wear))
    x0, x1 = xg + 0.024, L - 0.022
    gx = [x0 + (x1 - x0) * i / 4 for i in range(5)]
    hprof = lambda t: (0.029 - 0.004 * math.sin(math.pi * t), 0.022 - 0.002 * math.sin(math.pi * t))   # noqa: E731
    out.append(_sweep([(x, cy(x), 0.0) for x in gx], hprof, 6, PLAIN, vis=vis, wear=wear, caps=(False, False)))
    nd = 7 if L > 0.8 else 5
    for i in range(nd):                                   # the cord crossings (hishigami): two strips per face
        xa = x0 + (x1 - x0) * i / nd
        xb = x0 + (x1 - x0) * (i + 1) / nd
        xm = (xa + xb) / 2
        h, w = hprof((xm - x0) / (x1 - x0))
        for side in (1, -1):                              # front (+z) and back (-z) faces
            zf = side * (w / 2 + 0.0012)
            for d in (1, -1):
                q = [(xa, cy(xa) + d * h * 0.46, zf), (xa + 0.012, cy(xa) + d * h * 0.46, zf),
                     (xb, cy(xb) - d * h * 0.46, zf), (xb - 0.012, cy(xb) - d * h * 0.46, zf)]
                s = core.sheet([q if side > 0 else q[::-1]], INDIGO, (0.0, 0.0, float(side)), vis=vis,
                               uvs=[[(0, 0), (0.05, 0), (0.05, 0.3), (0, 0.3)]])
                s.finalize()
                if wear:
                    s.wear = wear
                out.append(s)
        # the cord over the top and bottom edges at the crossing ends (one quad each)
        for yy in (1, -1):
            yv = cy(xa) + yy * (h / 2 + 0.0012)
            q = [(xa - 0.002, yv, -w / 2), (xa + 0.010, yv, -w / 2), (xa + 0.010, yv, w / 2), (xa - 0.002, yv, w / 2)]
            s = core.sheet([q], INDIGO, (0.0, float(yy), 0.0), vis=vis, uvs=[[(0, 0), (0.05, 0), (0.05, 0.3), (0, 0.3)]])
            s.finalize()
            if wear:
                s.wear = wear
            out.append(s)
    xm = x0 + (x1 - x0) * 0.45                            # menuki (the grip ornament) on the front face
    out.append(box(xm - 0.015, xm + 0.015, cy(xm) - 0.006, cy(xm) + 0.006, 0.011, 0.0145, IRON, vis=vis))
    out.append(_sweep([(L - 0.024, cy(L - 0.024), 0.0), (L, cy(L), 0.0)], lambda t: (0.029 - 0.006 * t, 0.022 - 0.004 * t),
                      8, IRON, vis=vis, wear=wear))       # kashira
    return lkit.wear_all(out, wear)


def _cord(pts, r, mat, vis, wear):
    import sys
    import os
    b3b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "B3b")
    if b3b not in sys.path:
        sys.path.append(b3b)
    import w2kit
    import ropekit                    # FP2 (2026-10-01): 2.5x the segments (3 -> 1.2 cm) and 1.75x the sides (4 -> 7):
    path = w2kit._catmull(pts, 0.03 / ropekit.ROPE_K)          # the full 2.5x sides would take the rack over 1,500
    T, _, _ = w2kit._frames(path)
    return w2kit._tube(path, T, r, ropekit.rk(4, 1.75), mat, vis, wear, tile=0.2)


def arm(x, y, zf=0.10, th=0.022, w=0.040, curl=0.030, vis=(1,)):
    """A rack arm (kake) from the upright face (z = 0.03) forward to zf, its tip curling up `curl` to cradle the
    scabbard: a swept board, lacquered."""
    import os
    import sys
    b3b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "B3b")
    if b3b not in sys.path:
        sys.path.append(b3b)
    import w2kit
    cl = []
    for i in range(7):
        t = i / 6
        z = 0.02 + (zf - 0.02) * t
        yy = y + curl * max(0.0, (t - 0.55) / 0.45) ** 2 - 0.004 * math.sin(math.pi * t)
        cl.append((z, yy))
    s = w2kit.sweep(cl, th, w, LACQ, vis=vis)
    return xf(s, ry=90.0, t=(x, 0.0, 0.0))


def upright(x, h, vis=(1, 2)):
    """A shaped upright board: 5 cm wide, 2.6 cm thick, its top a pointed arch (the 'cloud' top of a kake)."""
    pts = [(x - 0.025, 0.03), (x + 0.025, 0.03), (x + 0.025, h - 0.03), (x + 0.012, h - 0.008), (x, h),
           (x - 0.012, h - 0.008), (x - 0.025, h - 0.03)]
    return prism([(a, b) for a, b in pts], "z", -0.013, 0.013, LACQ, vis=vis)
