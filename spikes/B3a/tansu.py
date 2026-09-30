"""jp_f_tansu (BUILD_LIST row 26): clothing chest of drawers (isho-dansu), two stacked boxes.

Brought in from the effort test (spikes/effort_test/high/tansu.py, the 'high' tansu Stephen judged "looks pretty
good"), adapted to the B3a pipeline:
  - body in jp_m_wood_interior (B1 made it; the test used wood_street_dark as a stand-in); drawer fronts are
    mapped into one clean plank band each (fkit.WOOD_BANDS) and carcass front edges into a groove (dark line)
  - FPart: no Memory / Shadow LOD (Q5: vanilla furniture has none); loot points go to the sidecar
  - ransacked: clothes spilled from the pulled drawer and beside the dropped one (build list: "clothes spilled")
  - _single: one box only (T2), after the build list's variant list
Frame: origin = footprint centre on the floor, +z = drawer front. 1.00 x 0.45 x 1.00, two boxes of 0.50.
"""
import math

import fkit
from fkit import core, box, prism, ngon, sheet, WOOD, IRON, INDIGO, KINARI, FPart, band_fit

W_, D_, H_ = 1.00, 0.45, 1.00
X0, X1 = -W_ / 2, W_ / 2
Z0, Z1 = -D_ / 2, D_ / 2
SEC = 0.50
T = 0.018
TB = 0.012
RAIL = 0.018
REC = 0.004
GAP = 0.003
FT = 0.020
DT = 0.012
DB = 0.008
DDEPTH = 0.405
IT = 0.0025
FRONT_ZONE = 0.60
GROOVE = (75, 82)            # a plank groove of jp_m_wood_interior: carcass front edges read as a dark line

OPEN = {
    "d_up_l": (X0 + T, -RAIL / 2, 1.0 - T - 0.180, 1.0 - T),
    "d_up_r": (RAIL / 2, X1 - T, 1.0 - T - 0.180, 1.0 - T),
    "d_up_w": (X0 + T, X1 - T, SEC + T, 1.0 - T - 0.180 - RAIL),
    "d_lo_1": (X0 + T, X1 - T, (SEC + RAIL) / 2, SEC - T),
    "d_lo_2": (X0 + T, X1 - T, T, (SEC - RAIL) / 2),
}
PULLS = {"d_up_l": [0.0], "d_up_r": [0.0], "d_up_w": [-0.27, 0.27], "d_lo_1": [-0.27, 0.27], "d_lo_2": [-0.27, 0.27]}
RANSACK = {"d_up_l": 0.17, "d_up_w": 0.28, "d_lo_2": 0.07, "d_lo_1": "floor"}
RANSACK_SINGLE = {"d_up_l": 0.15, "d_up_w": "floor"}
FLOOR_YAW = -5.0
FLOOR_GAP = 0.025


def wood(x0, x1, y0, y1, z0, z1, vis=(1, 2), band=None, band_n=(0.0, 0.0, 1.0), front_dark=False, **kw):
    s = box(x0, x1, y0, y1, z0, z1, WOOD, vis=vis, **kw)
    if band:
        band_fit(s, band[0], band[1], band_n)
    if front_dark:
        band_fit(s, GROOVE[0], GROOVE[1], (0.0, 0.0, 1.0))
    return s


def iron_box(x0, x1, y0, y1, z0, z1, vis=(1,)):
    return box(x0, x1, y0, y1, z0, z1, IRON, vis=vis)


def carcass(yb, lodset=(1, 2), upper=False):
    yt = yb + SEC
    out = [
        wood(X0, X1, yt - T, yt, Z0, Z1, lodset, front_dark=True),
        wood(X0, X1, yb, yb + T, Z0, Z1, lodset, front_dark=True),
        wood(X0, X0 + T, yb + T, yt - T, Z0, Z1, lodset, front_dark=True),
        wood(X1 - T, X1, yb + T, yt - T, Z0, Z1, lodset, front_dark=True),
        wood(X0 + T, X1 - T, yb + T, yt - T, Z0, Z0 + TB, lodset),
    ]
    if upper:
        yr = 1.0 - T - 0.180 - RAIL
        out.append(wood(X0 + T, X1 - T, yr, yr + RAIL, Z0 + TB, Z1, lodset, front_dark=True))
        out.append(wood(-RAIL / 2, RAIL / 2, yr + RAIL, 1.0 - T, Z0 + TB, Z1, lodset, front_dark=True))
    else:
        yr = (SEC - RAIL) / 2
        out.append(wood(X0 + T, X1 - T, yr, yr + RAIL, Z0 + TB, Z1, lodset, front_dark=True))
    for s in out:
        s.tag = "carcass"
    return out


def ring_pull(x, y, zf, lod=1):
    if lod >= 2:
        return [iron_box(x - 0.026, x + 0.026, y - 0.050, y + 0.026, zf, zf + 0.007, vis=(lod,))]
    out = [prism(ngon(x, y, 0.030, 8, math.pi / 8), "z", zf, zf + IT, IRON, vis=(1,))]
    out.append(iron_box(x - 0.004, x + 0.004, y - 0.001, y + 0.009, zf + IT, zf + IT + 0.010))
    R, r = 0.027, 0.0035
    cy, cz = y + 0.004 - R, zf + IT + r
    quads, normals = [], []
    nM, nm = 8, 3
    for i in range(nM):
        for j in range(nm):
            pts = []
            for (a, b) in ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)):
                th = 2 * math.pi * a / nM + math.pi / nM
                ph = 2 * math.pi * b / nm + math.pi / 2
                rr = R + r * math.cos(ph)
                pts.append((x + rr * math.cos(th), cy + rr * math.sin(th), cz + r * math.sin(ph)))
            tc = 2 * math.pi * (i + 0.5) / nM + math.pi / nM
            pc = 2 * math.pi * (j + 0.5) / nm + math.pi / 2
            normals.append((math.cos(tc) * math.cos(pc), math.sin(tc) * math.cos(pc), math.sin(pc)))
            quads.append(pts)
    out.append(sheet(quads, IRON, normals, vis=(1,), uvs=[[(0, 0), (0.05, 0), (0.05, 0.05), (0, 0.05)]] * len(quads)))
    return out


def lock_plate(x, y, zf, lod=1):
    if lod >= 2:
        return [iron_box(x - 0.045, x + 0.045, y - 0.040, y + 0.040, zf, zf + IT, vis=(lod,))]
    plate = prism(ngon(x, y, 0.045, 8, math.pi / 8, rx=0.052), "z", zf, zf + IT, IRON, vis=(1,))
    key = iron_box(x - 0.006, x + 0.006, y - 0.018, y + 0.012, zf + IT, zf + IT + 0.006)
    return [plate, key]


def drawer_front(name, dz=0.0, lod=1, k=0):
    x0, x1, y0, y1 = OPEN[name]
    zf = Z1 - REC + dz
    s = wood(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, zf - FT, zf, vis=(lod,) if lod > 1 else (1, 2))
    b = fkit.WOOD_BANDS[(2 * k + 1) % len(fkit.WOOD_BANDS)]
    band_fit(s, b[0], b[1], (0.0, 0.0, 1.0), voff=0.29 * k)
    s.tag = "front"
    out = [s]
    if lod > 1:
        return out
    yc = (y0 + y1) / 2 + 0.012
    for px in PULLS[name]:
        cx = (x0 + x1) / 2 + px
        out += ring_pull(cx, yc, zf, lod=1) + ring_pull(cx, yc, zf, lod=2)
    if name == "d_up_w":
        out += lock_plate(0.0, (y0 + y1) / 2, zf, lod=1) + lock_plate(0.0, (y0 + y1) / 2, zf, lod=2)
    return out


def drawer_body(name, dz=0.0, vis=(1, 2)):
    x0, x1, y0, y1 = OPEN[name]
    zf = Z1 - REC + dz - FT
    zb = Z1 - REC + dz - DDEPTH
    a, b = x0 + GAP + 0.004, x1 - GAP - 0.004
    yb, yt = y0 + GAP, y1 - GAP - 0.012
    out = [
        wood(a, a + DT, yb, yt, zb, zf, vis),
        wood(b - DT, b, yb, yt, zb, zf, vis),
        wood(a + DT, b - DT, yb, yt, zb, zb + DT, vis),
        wood(a + DT, b - DT, yb, yb + DB, zb + DT, zf, vis),
    ]
    for s in out:
        s.tag = "drawer"
    return out


def corner_fittings(yb, lowest=0.0):
    out = []
    L, B = 0.070, 0.024
    yt = yb + SEC
    for sx in (-1, 1):
        xe = X1 * sx
        for yy, sy in ((yt, -1), (yb, 1)):
            xa, xb = sorted((xe, xe - sx * L))
            ya, yb_ = sorted((yy, yy + sy * B))
            out.append(iron_box(xa, xb, ya, yb_, Z1, Z1 + IT))
            xa, xb = sorted((xe, xe - sx * B))
            ya, yb_ = sorted((yy + sy * B, yy + sy * L))
            out.append(iron_box(xa, xb, ya, yb_, Z1, Z1 + IT))
            xa, xb = sorted((xe, xe + sx * IT))
            ya, yb_ = sorted((yy, yy + sy * L))
            out.append(iron_box(xa, xb, ya, yb_, Z1 - 0.050, Z1 + IT))
            if abs(yy - lowest) > 1e-6:          # no wrap under the floor
                ya, yb_ = sorted((yy, yy - sy * IT))
                xa, xb = sorted((xe, xe - sx * 0.050))
                out.append(iron_box(xa, xb, ya, yb_, Z1 - 0.050, Z1 + IT))
    for sx in (-1, 1):
        for yy, sy in ((yt, -1), (yb, 1)):
            xa, xb = sorted((X1 * sx, X1 * sx - sx * 0.05))
            ya, yb_ = sorted((yy, yy + sy * 0.05))
            out.append(iron_box(xa, xb, ya, yb_, Z1, Z1 + IT, vis=(2,)))
    return out


def side_handles(yb):
    out = []
    yh = yb + SEC - 0.065
    for sx in (-1, 1):
        xo = X1 * sx
        xa, xb = sorted((xo, xo + sx * 0.010))
        xc, xd = sorted((xo, xo + sx * 0.016))
        for zc in (-0.075, 0.075):
            out.append(iron_box(xa, xb, yh - 0.020, yh + 0.020, zc - 0.018, zc + 0.018))
            out.append(iron_box(xc, xd, yh - 0.050, yh, zc - 0.005, zc + 0.005))
        out.append(iron_box(xc, xd, yh - 0.062, yh - 0.050, -0.090, 0.090))
        xe, xf = sorted((xo, xo + sx * 0.014))
        out.append(iron_box(xe, xf, yh - 0.060, yh + 0.020, -0.095, 0.095, vis=(2,)))
    return out


def collision(x0, x1, y0, y1, z0, z1):
    return box(x0, x1, y0, y1, z0, z1, WOOD, vis=(), geo=True, view=True, fire=True)


def dropped_drawer(name, face_z):
    x0, x1, y0, y1 = OPEN[name]
    ss = drawer_front(name, 0.0, lod=1, k=2) + drawer_body(name, 0.0)
    zf = Z1 - REC
    zb = zf - DDEPTH
    far = [box(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, zb, zf, WOOD, vis=(3,))]
    pre = (-(x0 + GAP), -(y0 + GAP), -zb)
    out = [s.transformed(0.0, pre) for s in ss + far]
    wdt, dep = (x1 - x0 - 2 * GAP), DDEPTH
    corners = [core.rot_y(p, FLOOR_YAW) for p in ((0, 0, 0), (wdt, 0, 0), (0, 0, dep), (wdt, 0, dep))]
    minx = min(c[0] for c in corners)
    maxx = max(c[0] for c in corners)
    minz = min(c[2] for c in corners)
    tx = -(minx + maxx) / 2
    tz = face_z + FLOOR_GAP - minz
    placed = [s.transformed(FLOOR_YAW, (tx, 0.0, tz)) for s in out]
    top = y1 - y0 - 2 * GAP
    cs = [core.add(core.rot_y(p, FLOOR_YAW), (tx, 0.0, tz)) for p in
          ((0, 0, 0), (wdt, 0, 0), (wdt, 0, dep), (0, 0, dep))]
    hexa = core.hexa(cs + [(c[0], top, c[2]) for c in cs], WOOD, vis=(), geo=True, view=True, fire=True)
    cen = core.add(core.rot_y((wdt / 2, DB, dep / 2 - 0.01), FLOOR_YAW), (tx, 0.0, tz))
    inner = [core.add(core.rot_y(p, FLOOR_YAW), (tx, 0.0, tz)) for p in
             ((0.03, 0, 0.03), (wdt - 0.03, 0, dep - 0.05))]
    return placed, hexa, cen, (tx, tz, wdt, dep, top), inner


def cloth_drape(x0, x1, zf, y_top, drop, mat=INDIGO, wear="_w2"):
    """A garment hanging over a pulled drawer's front board (zf = its outer face, y_top = its top): a double-sided
    strip from inside the drawer, over the board, down in front (visual only)."""
    prof = [(y_top + 0.006, zf - 0.13), (y_top + 0.008, zf - FT / 2), (y_top - 0.03, zf + 0.010),
            (y_top - drop, zf + 0.022)]
    quads, normals = [], []
    for i in range(len(prof) - 1):
        (ya, za), (yb, zb) = prof[i], prof[i + 1]
        q = [(x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb)]
        n = core.norm((0.0, zb - za, -(yb - ya)))
        if n[1] + n[2] < 0:
            n = core.mul(n, -1.0)
        quads += [q, q[::-1]]
        normals += [n, core.mul(n, -1.0)]
    s = sheet(quads, mat, normals, vis=(1, 2))
    s.wear = wear
    return s


def garment(cx, cz, yaw, wear="_w2"):
    """A kimono dropped on the floor: the folded body, a sleeve flung out, a pale lining edge (visual only)."""
    out = [fkit.rotated_box(-0.03, -0.02, 0.44, 0.31, 0.0, 0.010, -7.0, KINARI, vis=(1,)),
           fkit.rotated_box(0.0, 0.0, 0.42, 0.30, 0.010, 0.024, 0.0, INDIGO, vis=(1, 2)),
           fkit.rotated_box(0.20, 0.13, 0.30, 0.16, 0.004, 0.018, 38.0, INDIGO, vis=(1,))]
    res = []
    for s in out:
        s = fkit.xf(s, ry=yaw, t=(cx, 0.0, cz))
        s.wear = wear
        res.append(s)
    return res


def model(state="shut", single=False):
    name = "jp_f_tansu" + ("_single" if single else "") + ("" if state == "shut" else "_ransacked")
    P = FPart(name, budget="furniture", res3=True, mass=30.0 if single else 45.0)
    ransack = (RANSACK_SINGLE if single else RANSACK) if state == "ransacked" else {}
    names = ["d_up_l", "d_up_r", "d_up_w"] + ([] if single else ["d_lo_1", "d_lo_2"])
    body = carcass(SEC, upper=True) + ([] if single else carcass(0.0))
    body.append(wood(X0, X1, SEC, H_, Z0, Z1, vis=(3,)))
    if not single:
        body.append(wood(X0, X1, 0.0, SEC, Z0, Z1, vis=(3,)))
    for yb in ((SEC,) if single else (0.0, SEC)):
        body += corner_fittings(yb, SEC if single else 0.0) + side_handles(yb)
    moved = []            # solids at their slot (shifted down by SEC for the single box)
    floor = []            # solids already on the floor (dropped drawer, cloth)
    pull_front = Z1
    for k, nm in enumerate(names):
        act = ransack.get(nm, 0.0)
        if act == "floor":
            continue
        dz = float(act)
        moved += drawer_front(nm, dz, lod=1, k=k)
        if dz > 0:
            moved += drawer_body(nm, dz)
            x0, x1, y0, y1 = OPEN[nm]
            moved.append(box(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, Z1, Z1 - REC + dz, WOOD, vis=(3,)))
            moved.append(collision(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, Z1, Z1 - REC + dz))
            if y0 < 0.1 + (SEC if single else 0.0):
                pull_front = max(pull_front, Z1 - REC + dz)
        moved += drawer_front(nm, dz + (0.0015 + REC if dz == 0 else 0.0), lod=3, k=k)
    moved.append(collision(X0, X1, SEC, H_, Z0, Z1))
    if not single:
        moved.append(collision(X0, X1, 0.0, SEC, Z0, Z1))
    dy = -SEC if single else 0.0
    for s in body + moved:
        P.add(s.transformed(0.0, (0.0, dy, 0.0)) if dy else s)
    top = H_ + dy
    P.loot_rect("top", top, X0 + 0.05, X1 - 0.05, Z0 + 0.05, Z1 - 0.05, rng=0.2,
                points=[(-0.25, top, 0.0), (0.25, top, 0.0)])
    if state == "ransacked":
        drop = [n for n, a in ransack.items() if a == "floor"][0]
        placed, hexa, cen, (tx, tz, wdt, dep, dtop), inner = dropped_drawer(drop, pull_front)
        for s in placed:
            s.tag = "dropped"
            P.add(s)
        P.add(hexa)
        P.loot_rect("dropped_drawer", DB, inner[0][0], inner[1][0], inner[0][2], inner[1][2], rng=0.15,
                    kind="floor", points=[tuple(cen)])
        # clothes: one garment hanging out of the most-pulled drawer, one crumpled beside the dropped drawer
        hang = max(((n, a) for n, a in ransack.items() if a != "floor"), key=lambda t: t[1])
        x0, x1, y0, y1 = OPEN[hang[0]]
        zf = Z1 - REC + hang[1]
        P.add(cloth_drape(x0 + 0.10, x0 + 0.34, zf, y1 - GAP + dy, min(0.20, y0 + dy - 0.03)))
        for s in garment(X1 + 0.16, tz + dep * 0.6, 25.0):
            P.add(s)
        P.notes.append("dropped drawer inside the %.2f m front zone; clothes are visual only" % FRONT_ZONE)
        P.extra["front_zone_m"] = FRONT_ZONE
    P.dim("width", 1.00, P_w(P), tol=0.01)
    P.dim("height", 0.50 if single else 1.00, top, tol=0.01)
    return P


def P_w(P):
    xs = [v[0] for s in P.solids if s.tag == "carcass" for v in s.verts]
    return max(xs) - min(xs)


PROP = {"id": "jp_f_tansu", "cat": "storage", "notes": [
    "Brought in from spikes/effort_test/high (Stephen: 'looks pretty good'), body now jp_m_wood_interior.",
    "_single = the upper box alone (T2 rooms)."], "models": [
    {"p3d": "jp_f_tansu", "variant": "shut", "state": "intact", "display": "Tansu (clothing chest)",
     "build": lambda: model("shut")},
    {"p3d": "jp_f_tansu_ransacked", "variant": "shut", "state": "ransacked",
     "display": "Tansu (ransacked)", "build": lambda: model("ransacked")},
    {"p3d": "jp_f_tansu_single", "variant": "single", "state": "intact", "display": "Tansu, single box",
     "build": lambda: model("shut", single=True)},
    {"p3d": "jp_f_tansu_single_ransacked", "variant": "single", "state": "ransacked",
     "display": "Tansu, single box (ransacked)", "build": lambda: model("ransacked", single=True)},
]}
