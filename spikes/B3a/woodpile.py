"""woodpile - FP2 (2026-10-01): a believable Japanese woodpile (maki) of individual split billets, shared by B3a's
jp_f_firewood stacks and B3b's jp_s_firewood_stack wall / free-standing stacks.

Stephen (re-check): the firewood pile outside the houses "looks like mega shit": B3b's stacks were a flat sooted box
with flat yellow four-sided decals on the front (stack_caps), B3a's were 3-5 sided prisms. Now every billet is a split
piece of a round (a half, a quarter, a third, or a small whole round of branch wood) with its bark on the round side
(jp_m_wood_firewood's bark band, smooth normals so it reads round), flat split faces (the split-wood band), and a
real end-grain cap (jp_m_wood_endgrain_firewood mapped from the ORIGINAL round's pith, so a half shows half the rings
with the pith on its split face, a quarter the pith in its corner). Billets are stacked by dropping them onto the
pile's skyline (they nest into the gaps below), their front ends stagger by up to +-3 cm and are cut a little off
square, their lengths vary; a dark core 7 cm behind the front fills the gaps; a few loose billets lie across the top.

Frame: billets run along z (end grain to the front, and to the back when `back` is True); the pile spans x0..x1;
y = 0 is the ground. Faces: about 6-7 per billet (hidden down-facing sides are dropped); `max_faces` picks the
billet size so the pile fits its budget class.
"""
import itertools
import math
import random

import fkit
from fkit import core, sheet, box, xf, FIREWOOD, FIREEND, SOOT_WOOD, LOGWOOD, ENDGRAIN

ROPE = "straw_rope"

TILE = 2.0          # jp_m_wood_firewood: 2 m world tile; u 0-0.5 bark, 0.5-1 split wood


def _section(rr, kind, k_arc):
    """The billet's cross-section in its ROUND's frame (pith at 0,0; round radius 1): (points, edge kinds) with
    edge i from point i to i+1 ('bark' or 'split'), counter-clockwise."""
    # split faces roughly square to the pile (as billets settle): fills the cell (~0.79) instead of leaving holes
    a0 = rr.choice((0.0, 0.5, 1.0, 1.5)) * math.pi + rr.uniform(-0.22, 0.22)
    if kind == "half_up":                      # a half lying split face up (a flat top: dressing / loot)
        kind, a0 = "half", math.pi
    if kind == "round":
        n = k_arc
        pts = [(math.cos(a0 + 2 * math.pi * j / n), math.sin(a0 + 2 * math.pi * j / n)) for j in range(n)]
        return pts, ["bark"] * n
    span = {"half": math.pi, "third": 2 * math.pi / 3, "quarter": math.pi / 2}[kind]
    arc = [(math.cos(a0 + span * j / k_arc), math.sin(a0 + span * j / k_arc)) for j in range(k_arc + 1)]
    if kind == "half":
        return arc, ["bark"] * k_arc + ["split"]
    # wedge: the pith corner, then the arc; a split face on each side of the wedge
    pts = [(0.0, 0.0)] + arc
    return pts, ["split"] + ["bark"] * k_arc + ["split"]


def _piece(rr, w, h, kinds=None):
    """A billet's section fitted into a w x h cell with its lower-left at (0, 0): (polygon, edge kinds, pith, R)."""
    kind = rr.choice(kinds or ("half", "half", "quarter", "quarter", "third", "round"))
    k_arc = {"half": 4, "half_up": 4, "third": 3, "quarter": 3, "round": 7}[kind]
    pts, kinds_e = _section(rr, kind, k_arc)
    pts = [(x * rr.uniform(0.94, 1.0), y * rr.uniform(0.94, 1.0)) if (x, y) != (0.0, 0.0) else (x, y) for x, y in pts]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sc = min(w * 0.98 / (max(xs) - min(xs)), h * 0.98 / (max(ys) - min(ys)))
    P2 = [((x - min(xs)) * sc + (w - (max(xs) - min(xs)) * sc) / 2, (y - min(ys)) * sc) for x, y in pts]
    pith = ((0 - min(xs)) * sc + (w - (max(xs) - min(xs)) * sc) / 2, (0 - min(ys)) * sc)
    return P2, kinds_e, pith, sc


def _hull_at(P2, xx, upper):
    ys = []
    n = len(P2)
    for k in range(n):
        a, b = P2[k], P2[(k + 1) % n]
        if (a[0] - xx) * (b[0] - xx) <= 0 and abs(b[0] - a[0]) > 1e-6:
            ys.append(a[1] + (b[1] - a[1]) * (xx - a[0]) / (b[0] - a[0]))
    if not ys:
        return None
    return max(ys) if upper else min(ys)


def _billet(rr, piece, ox, oy, z_back, z_front, back, wear, loose=False):
    """One billet: the piece's section moved by (ox, oy), extruded along z: (solid, polygon in x-y, faces)."""
    P0, kinds_e, pith0, R = piece
    P2 = [(x + ox, y + oy) for x, y in P0]
    pith = (pith0[0] + ox, pith0[1] + oy)
    n = len(P2)
    cx = sum(p[0] for p in P2) / n
    cy = sum(p[1] for p in P2) / n
    # front cap: staggered, cut a little off square
    zf = z_front + rr.uniform(-0.03, 0.025)
    tx, ty = rr.uniform(-0.12, 0.12), rr.uniform(-0.12, 0.12)
    zb = z_back + rr.uniform(-0.02, 0.02) if back else z_back
    bx, by = (rr.uniform(-0.1, 0.1), rr.uniform(-0.1, 0.1)) if back else (0.0, 0.0)
    F = [(x, y, zf + tx * (x - cx) + ty * (y - cy)) for x, y in P2]
    Bk = [(x, y, zb + bx * (x - cx) + by * (y - cy)) for x, y in P2]
    quads, normals, uvs, vns, kinds_f = [], [], [], [], []

    def eg_uv(p, mirror):              # end grain from the ROUND's pith: its bark edge at r = 0.49 (bark ring 0.45-0.5)
        dx, dy = (p[0] - pith[0]) / R, (p[1] - pith[1]) / R
        return (0.5 + 0.49 * dx * (-1 if mirror else 1), 0.5 - 0.49 * dy)

    def cap(ring, nz, mirror):
        order = list(range(n)) if nz > 0 else list(range(n))[::-1]
        k = 1
        while k < n - 1:                 # quad fan (MLOD faces are tris / quads)
            idx = [0, k, k + 1, k + 2] if k + 2 < n else [0, k, k + 1]
            q = [ring[order[i]] for i in idx]
            quads.append(q)
            normals.append((0.0, 0.0, nz))
            uvs.append([eg_uv(p, mirror) for p in q])
            vns.append([(0.0, 0.0, nz)] * len(q))
            kinds_f.append(FIREEND)
            k += len(idx) - 2
    cap(F, 1.0, False)
    if back:
        cap(Bk, -1.0, True)
    ub = rr.uniform(0.02, 0.30)                  # where in the bark band this billet's bark starts
    us = rr.uniform(0.52, 0.80)
    vo = rr.uniform(0.0, 1.0)
    arc_s = 0.0

    def rad(p):
        return core.norm((p[0] - pith[0], p[1] - pith[1], 0.0))
    for i in range(n):
        j = (i + 1) % n
        a, b = P2[i], P2[j]
        ex, ey = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ex, ey)
        if L < 1e-5:
            continue
        nrm = (ey / L, -ex / L, 0.0)
        mid = ((a[0] + b[0]) / 2 - cx, (a[1] + b[1]) / 2 - cy)
        if mid[0] * nrm[0] + mid[1] * nrm[1] < 0:
            nrm = (-nrm[0], -nrm[1], 0.0)
        bark = kinds_e[i] == "bark"
        if nrm[1] < -0.45 and not loose:         # resting on the billets below: hidden
            arc_s += L if bark else 0.0
            continue
        q = [F[i], F[j], Bk[j], Bk[i]]
        quads.append(q)
        normals.append(nrm)
        if bark:
            u0 = ub + arc_s / TILE
            arc_s += L
            vns.append([rad(F[i]), rad(F[j]), rad(Bk[j]), rad(Bk[i])])
        else:
            u0 = us
            vns.append([nrm] * 4)
        u1 = u0 + L / TILE
        kinds_f.append(FIREWOOD)
        uvs.append([(u0, vo + q[0][2] / TILE), (u1, vo + q[1][2] / TILE), (u1, vo + q[2][2] / TILE),
                    (u0, vo + q[3][2] / TILE)])
    s = sheet(quads, {"front": FIREEND, "back": FIREEND, "default": FIREWOOD}, normals, vis=(1,), uvs=uvs)
    s.finalize()
    s.fm = list(kinds_f)
    s.vn = vns
    if wear:
        s.wear = wear
    # Res 2: one quad per end from the polygon's four extreme points (left, bottom, right, top), same end grain
    def area(ix):
        return abs(sum(P2[ix[k]][0] * P2[ix[(k + 1) % len(ix)]][1] - P2[ix[(k + 1) % len(ix)]][0] * P2[ix[k]][1]
                       for k in range(len(ix)))) / 2
    ex = max(itertools.combinations(range(n), 4), key=area) if n > 4 else tuple(range(n))   # the largest quad
    r2q, r2n, r2uv = [], [], []
    if len(ex) >= 3:
        # the front end exactly as Res 1 (the end grain is what the pile shows), the back end as the largest quad
        for qi in range(len(quads)):
            if normals[qi] == (0.0, 0.0, 1.0):
                r2q.append(quads[qi])
                r2n.append(normals[qi])
                r2uv.append(uvs[qi])
        if back:
            q = [Bk[i] for i in ex][::-1]
            r2q.append(q)
            r2n.append((0.0, 0.0, -1.0))
            r2uv.append([eg_uv(p, True) for p in q])
    s.r2 = None
    if r2q:
        c2 = sheet(r2q, FIREEND, r2n, vis=(2,), uvs=r2uv)
        c2.finalize()
        if wear:
            c2.wear = wear
        s.r2 = c2
    return s, P2, len(quads)


def _layout(x0, x1, hfun, cell, seed, back, z_back, z_front, wear, over=0.035):
    """Drop billets left to right onto the pile's skyline (each comes to rest where its underside first touches),
    pass after pass, until the pile reaches hfun everywhere."""
    rr = random.Random(seed)
    dx = 0.01
    nx = int(round((x1 - x0) / dx))
    sky = [0.0] * nx
    out, faces = [], 0
    for guard in range(80):
        placed = False
        x = x0
        first = True
        while x < x1 - 0.04:
            w = cell * rr.uniform(0.80, 1.25)
            if first and guard % 2:              # odd passes start with a narrow piece: the joints stagger
                w = cell * rr.uniform(0.5, 0.75)
            first = False
            if x + w > x1 - 0.5 * cell:
                w = x1 - x
            h = cell * rr.uniform(0.75, 1.15)
            piece = _piece(rr, w, h)
            P0 = piece[0]
            base = 0.0
            for i in range(max(0, int((x - x0) / dx)), min(nx, int(math.ceil((x + w - x0) / dx)))):
                lo = _hull_at(P0, x0 + (i + 0.5) * dx - x, False)
                if lo is not None:
                    base = max(base, sky[i] - lo - 0.004)   # 4 mm bite: no daylight between billets
            top = base + max(p[1] for p in P0)
            lim = hfun(x + w / 2)
            if top > lim + over:
                x += w * 0.5
                continue
            s, P2, nf = _billet(rr, piece, x, base, z_back, z_front, back, wear)
            out.append(s)
            if s.r2 is not None:
                out.append(s.r2)
            faces += nf
            for i in range(max(0, int((x - x0) / dx)), min(nx, int(math.ceil((x + w - x0) / dx)))):
                up = _hull_at(P2, x0 + (i + 0.5) * dx, True)
                if up is not None:
                    sky[i] = max(sky[i], up)
            placed = True
            x += w
        if not placed:
            break
    return out, faces, sky


def woodpile(x0, x1, hfun, z_back, z_front, seed=1, max_faces=1200, back=False, wear=None, loose_top=2,
             core_mat=SOOT_WOOD, cells=None, over=0.035):
    """Billets along z between z_back and z_front, the pile from x0 to x1 up to hfun(x). Returns
    (solids, info): info = {'cell', 'faces', 'sky' (heights per cm), 'top_y', 'tops' [(x, y)]}."""
    best = None
    for cell in (cells or [0.105 + 0.005 * k for k in range(14)]):
        out, faces, sky = _layout(x0, x1, hfun, cell, seed, back, z_back, z_front, wear, over)
        best = (cell, out, faces, sky)
        if faces + 12 * loose_top + 12 <= max_faces:
            break
    cell, out, faces, sky = best
    dx = 0.01
    nx = len(sky)
    # the dark core behind the ends (fills the gaps between billets), stepped under the skyline
    steps = 6
    zc0 = z_front - 0.07
    zc1 = (z_back + 0.07) if back else z_back + 0.005
    for k in range(steps):
        a, b = k * nx // steps, (k + 1) * nx // steps
        hh = max(0.05, min(sky[a:b]) - 0.04)
        mats = {"front": core_mat, "back": core_mat, "default": core_mat}
        e0 = 0.07 if k == 0 else 0.01                  # inset at the pile's ends (the end billets' sides show)
        e1 = 0.07 if k == steps - 1 else 0.01
        s = box(x0 + a * dx + e0, x0 + b * dx - e1, 0.0, hh, min(zc0, zc1), max(zc0, zc1), mats, vis=(1,))
        s.wear = "_w2"
        out.append(s)
        faces += 6
        hh2 = max(0.05, sum(sky[a:b]) / max(1, b - a) - 0.02)    # Res 2: a fuller block behind the end quads
        z2 = (z_front - 0.045, (z_back + 0.045) if back else z_back + 0.005)   # behind every staggered end
        s2 = box(x0 + a * dx, x0 + b * dx, 0.0, hh2, min(z2), max(z2),
                 {"front": core_mat, "back": core_mat, "default": FIREWOOD}, vis=(2,))
        s2.wear = "_w2"
        out.append(s2)
    # loose billets lying across the top (along x), and their tops for loot / dressing
    rr = random.Random(seed * 7 + 3)
    tops = []
    loot = None
    for k in range(loose_top):
        xc = (x0 + x1) / 2 + (x1 - x0) * (0.06 if k == 0 else rr.choice((-1, 1)) * rr.uniform(0.18, 0.32))
        Lb = rr.uniform(0.30, 0.36)
        i = min(nx - 1, max(0, int((xc - x0) / dx)))
        hw = int(Lb / 2 / dx) + 2
        y0 = max(sky[max(0, i - hw):min(nx, i + hw)])
        zc = z_back + (z_front - z_back) * rr.uniform(0.40, 0.60)
        r = cell * rr.uniform(0.42, 0.55)
        piece = _piece(rr, 2 * r, 2 * r, kinds=("half_up",) if k == 0 else ("half", "quarter", "round"))
        s, P2, nf = _billet(rr, piece, -r, -r, -Lb / 2, Lb / 2, True, wear, loose=True)
        lo, hi = min(p[1] for p in P2), max(p[1] for p in P2)
        dy = y0 - lo - 0.01
        s = xf(s, ry=90.0 + rr.uniform(-20, 20), t=(xc, dy, zc))
        out.append(s)
        faces += nf
        tops.append((xc, hi + dy))
        if k == 0:
            loot = (xc, hi + dy, zc)            # the split face up: flat
    return out, {"cell": cell, "faces": faces, "sky": sky, "top_y": max(sky), "tops": tops, "loot": loot}


def end_stakes(x0, x1, z_back, z_front, h0, h1, wear=None, r=0.032, seed=9, lean_out=(0.0, 0.0), fallen=None):
    """FX1 (2026-10-01, Stephen: 'woodpiles look much better, but nothing supports them: perfectly stacked squares
    would fall without side support'): the period end support of a maki pile: at each free end two stakes (kui) driven
    in at the front and back corners, upright against the end billets, their tops ~8 cm over the pile, tied across the
    end with a straw rope. The stakes stand INSIDE x0..x1 (the footprint and the wall gap stay); the pile is built
    between the returned px0..px1. h0 / h1: the pile height at the x0 / x1 end. fallen: None | 0 | 1 = that end's
    stakes lean out 18 deg (a collapsed pile). Returns (solids, px0, px1)."""
    rr = random.Random(seed)
    out = []
    zs = [z_front - 0.05, z_back + 0.05]
    for end, (xe, he, sg) in enumerate(((x0 + r + 0.004, h0, -1.0), (x1 - r - 0.004, h1, 1.0))):
        lean = 18.0 if fallen == end else lean_out[end]
        top = he + 0.08 + rr.uniform(-0.02, 0.03)
        for zc in zs:
            st = fkit.lcyl("y", xe, zc, r * rr.uniform(0.9, 1.1), 0.0, top, LOGWOOD, n=6, vis=(1, 2),
                           caps=ENDGRAIN)
            st = xf(st, rz=-sg * (lean + rr.uniform(0.0, 1.0)), pivot=(xe, 0.0, zc))      # never into the pile
            if wear:
                st.wear = wear
            out.append(st)
        # the straw tie across the end, from the front stake to the back one (on the stakes' outer side)
        if fallen != end:
            yt = he * 0.66
            dx = math.tan(math.radians(lean)) * yt
            tie = fkit.lcyl("z", xe + sg * (dx + r * 0.9), yt, 0.011, min(zs) - r, max(zs) + r, ROPE, n=5, vis=(1,))
            tie.wear = "_w2"
            out.append(tie)
    return out, x0 + 2 * r + 0.012, x1 - 2 * r - 0.012


def coarse_front(x0, x1, hfun, z_front, z_back, wear=None, cell=0.30, back=False, core_mat=SOOT_WOOD, seed=5):
    """The Res 2 stand-in: a stepped core block (sooted front, bark sides / top) with big end-grain caps."""
    out = []
    steps = 4
    rr = random.Random(seed)
    dxs = (x1 - x0) / steps
    for k in range(steps):
        a, b = x0 + k * dxs, x0 + (k + 1) * dxs
        hh = min(hfun(a + 0.01), hfun(b - 0.01))
        s = box(a, b, 0.0, hh, min(z_back, z_front), max(z_back, z_front),
                {"front": core_mat, "back": core_mat, "default": FIREWOOD}, vis=(2,))
        s.wear = "_w2"
        out.append(s)
        for zf, nz in ((z_front + 0.008, 1.0),) + (((z_back - 0.008, -1.0),) if back else ()):
            y = 0.0
            while y < hh - 0.06:
                ch = min(cell * rr.uniform(0.6, 0.8), hh - y)
                x = a
                while x < b - 0.05:
                    cw = min(cell * rr.uniform(0.6, 0.8), b - x)
                    cxp, cyp, r = x + cw / 2, y + ch / 2, min(cw, ch) * 0.47
                    q = [(cxp - r, cyp - r, zf), (cxp + r, cyp - r, zf), (cxp + r, cyp + r, zf), (cxp - r, cyp + r, zf)]
                    uv = [(0.5 - 0.32, 0.5 + 0.32), (0.5 + 0.32, 0.5 + 0.32), (0.5 + 0.32, 0.5 - 0.32),
                          (0.5 - 0.32, 0.5 - 0.32)]
                    if nz < 0:
                        q, uv = q[::-1], uv[::-1]
                    c = sheet([q], FIREEND, (0.0, 0.0, nz), vis=(2,), uvs=[uv])
                    c.finalize()
                    if wear:
                        c.wear = wear
                    out.append(c)
                    x += cw
                y += ch
    return out
