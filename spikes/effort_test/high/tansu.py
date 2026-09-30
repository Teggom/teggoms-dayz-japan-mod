"""jp_f_tansu (BUILD_LIST row 26): clothing chest of drawers (isho-dansu), two stacked boxes, two states.

Frame (PLAYBOOK §10.2, prop datum): origin = footprint centre on the floor, +y up, +z = the drawer front,
autocenter=0. Overall 1.00 (x) x 0.45 (z) x 1.00 (y), two carcasses of 0.50.

Layout (5 drawers, after the Fukagawa Edo Museum tenement tansu, refs i07):
  upper box : two half-width drawers on top (1 ring pull each), one full-width drawer (2 ring pulls + lock plate)
  lower box : two full-width drawers (2 ring pulls each)
  iron      : ring pulls (warabite) on round plates, corner fittings (sumi-kanagu) at the 8 front corners,
              folding bar carrying handles (sao-kan) on both sides of each box

States:
  'intact'    closed, dusty (all up-facing wood uses the _w2 'dusty' wear, the rest _w1)
  'ransacked' upper-left small drawer and upper wide drawer pulled out, bottom drawer pulled out a little,
              lower top drawer lying on the floor in the front zone (<= 0.60 m in front, within the width)

Built on the parts kit (parts/kit/jpparts/core.py: Part/Solid, LOD writer); nothing in parts/ is modified.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import core, mlod  # noqa: E402
from jpparts.core import box, prism, ngon, sheet, Solid  # noqa: E402

WOOD = "wood_street_dark"     # closest existing wood to timber_interior (jp_m_wood_interior not built yet)
IRON = "metal_iron"

W, D, H = 1.00, 0.45, 1.00
X0, X1 = -W / 2, W / 2
Z0, Z1 = -D / 2, D / 2
SEC = 0.50                    # each carcass
T = 0.018                     # carcass boards
TB = 0.012                    # back board
RAIL = 0.018                  # horizontal / vertical dividers
REC = 0.004                   # drawer fronts sit 4 mm behind the carcass front edge
GAP = 0.003                   # drawer front clearance each side
FT = 0.020                    # drawer front thickness
DT = 0.012                    # drawer side / back
DB = 0.008                    # drawer bottom
DDEPTH = 0.405                # drawer depth incl. front (carcass inner depth 0.426)
IT = 0.0025                   # iron plate thickness
MASS = 45.0                   # kg, empty (paulownia/cedar isho-dansu, assumed)
FRONT_ZONE = 0.60             # m in front of the carcass face kept for the dropped drawer (decision, REPORT)

# clean bands (texture px, u) between the plank grooves of jp_m_wood_street_dark _w1 (measured in the _co map);
# every drawer front is mapped inside one, so no plank seam runs across a single-board front
BANDS_W1 = [(230, 360), (378, 506), (818, 944), (230, 360), (378, 506)]   # 126-130 px each; fronts are 89-132 px tall

# drawers: name -> (x0, x1, y0, y1) of the OPENING in the carcass
OPEN = {
    "d_up_l": (X0 + T, -RAIL / 2, 1.0 - T - 0.180, 1.0 - T),
    "d_up_r": (RAIL / 2, X1 - T, 1.0 - T - 0.180, 1.0 - T),
    "d_up_w": (X0 + T, X1 - T, SEC + T, 1.0 - T - 0.180 - RAIL),
    "d_lo_1": (X0 + T, X1 - T, (SEC + RAIL) / 2, SEC - T),
    "d_lo_2": (X0 + T, X1 - T, T, (SEC - RAIL) / 2),
}
PULLS = {"d_up_l": [0.0], "d_up_r": [0.0], "d_up_w": [-0.27, 0.27], "d_lo_1": [-0.27, 0.27], "d_lo_2": [-0.27, 0.27]}

# ransacked: pulled-out distance per drawer; 'floor' = removed and dropped in front
RANSACK = {"d_up_l": 0.17, "d_up_w": 0.28, "d_lo_2": 0.07, "d_lo_1": "floor"}
FLOOR_YAW = -5.0              # deg, the dropped drawer lies a little askew
FLOOR_GAP = 0.025             # m between the carcass face and the nearest corner of the dropped drawer


class TansuPart(core.Part):
    """Part with one extra rule: up-facing WOOD faces use the dusty wear (_w2) - dust settles on tops, ledges and
    drawer bottoms; every other face uses the part wear (_w1)."""
    DUST = "_w2"

    def face_wear(self, s, fi):
        m = s.fm[fi]
        if m == WOOD and s.fn[fi][1] > 0.5 and not getattr(s, "no_dust", False):
            return self.DUST
        return self.wear_of(m)

    def _visual(self, k):
        lod = mlod.Lod(float(k))
        for s in self.solids:
            if k not in s.vis:
                continue
            for fi in range(len(s.faces)):
                m = s.fm[fi]
                w = self.face_wear(s, fi)
                lod.add_flat_face(s.face_points(fi), s.fn[fi], s.fuv[fi], core.tex_path(m, w), core.rvmat_path(m, w))
        return lod

    def lods(self, geo_props=None, mass=None):
        out = super().lods(geo_props, mass)
        # Shadow Volume (res 10000): the closed convex collision boxes, no texture
        sv = mlod.Lod(10000.0)
        for s in self.solids:
            if s.closed and s.geo:
                sv.add_closed_solid(s.verts, s.faces, "", "")
        i = next(k for k, l in enumerate(out) if l.resolution > 3.5)
        out.insert(i, sv)
        return out


DARK = (515, 534)             # the darkest groove band of the _w1 map (mean sRGB 60/40/30 vs 87/59/44): carcass
#                               front edges (end grain / shadow line) take it, so the drawers read as separate fronts


def band_uv(s, band_px, normal=(0.0, 0.0, 1.0)):
    """Shift u of the solid's face(s) with outward `normal` (only those faces) so they sample the texture band
    band_px (centred in it). Works on the finalized per-face UVs."""
    s.finalize()
    lo, hi = band_px[0] / 1024.0, band_px[1] / 1024.0
    for fi in range(len(s.faces)):
        if core.dot(s.fn[fi], normal) > 0.9:
            us = [a for a, b in s.fuv[fi]]
            span = max(us) - min(us)
            u0 = lo + (hi - lo - span) / 2 if span < hi - lo else lo
            d = u0 - min(us)
            s.fuv[fi] = [(a + d, b) for a, b in s.fuv[fi]]
    return s


def wood(x0, x1, y0, y1, z0, z1, vis=(1, 2), band=None, band_n=(0.0, 0.0, 1.0), front_dark=False, **kw):
    s = box(x0, x1, y0, y1, z0, z1, WOOD, vis=vis, **kw)
    if band:
        band_uv(s, band, band_n)
    if front_dark:
        band_uv(s, DARK, (0.0, 0.0, 1.0))
    return s


def iron_box(x0, x1, y0, y1, z0, z1, vis=(1,)):
    return box(x0, x1, y0, y1, z0, z1, IRON, vis=vis)


# ------------------------------------------------------------------------------------------------ pieces
def carcass(yb, lodset=(1, 2), upper=False):
    """One box: top, bottom, two sides, back, and the drawer dividers (full depth, so an open slot shows a floor)."""
    yt = yb + SEC
    out = [
        wood(X0, X1, yt - T, yt, Z0, Z1, lodset, band=(222, 512) if upper else None,
             band_n=(0.0, 1.0, 0.0), front_dark=True),                                    # top (dusty _w2 map)
        wood(X0, X1, yb, yb + T, Z0, Z1, lodset, front_dark=True),                        # bottom
        wood(X0, X0 + T, yb + T, yt - T, Z0, Z1, lodset, front_dark=True),                # left side
        wood(X1 - T, X1, yb + T, yt - T, Z0, Z1, lodset, front_dark=True),                # right side
        wood(X0 + T, X1 - T, yb + T, yt - T, Z0, Z0 + TB, lodset),                        # back
    ]
    if upper:
        yr = 1.0 - T - 0.180 - RAIL
        out.append(wood(X0 + T, X1 - T, yr, yr + RAIL, Z0 + TB, Z1, lodset, front_dark=True))   # rail under the pair
        out.append(wood(-RAIL / 2, RAIL / 2, yr + RAIL, 1.0 - T, Z0 + TB, Z1, lodset, front_dark=True))  # divider
    else:
        yr = (SEC - RAIL) / 2
        out.append(wood(X0 + T, X1 - T, yr, yr + RAIL, Z0 + TB, Z1, lodset, front_dark=True))
    for s in out:
        s.tag = "carcass"
    return out


def ring_pull(x, y, zf, lod=1):
    """Warabite ring pull on a round plate: 8-gon plate, staple, 8x3 ring hanging against the plate."""
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
            pts, cs = [], []
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
    s = wood(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, zf - FT, zf, vis=(lod,) if lod > 1 else (1, 2),
             band=BANDS_W1[k % len(BANDS_W1)])
    # different stretch of the board along the grain per drawer, so fronts sharing a band don't repeat
    for fi in range(len(s.faces)):
        if s.fn[fi][2] > 0.9:
            s.fuv[fi] = [(a, b + 0.29 * k) for a, b in s.fuv[fi]]
    s.tag = "front"
    out = [s]
    if lod > 1:                      # Res 3: the front board only
        return out
    yc = (y0 + y1) / 2 + 0.012
    for px in PULLS[name]:
        cx = (x0 + x1) / 2 + px
        out += ring_pull(cx, yc, zf, lod=1) + ring_pull(cx, yc, zf, lod=2)
    if name == "d_up_w":
        out += lock_plate(0.0, (y0 + y1) / 2, zf, lod=1) + lock_plate(0.0, (y0 + y1) / 2, zf, lod=2)
    return out


def drawer_body(name, dz=0.0, vis=(1, 2)):
    """Sides, back and bottom behind the front (only needed when a drawer is open)."""
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


def corner_fittings(yb):
    """Sumi-kanagu at the 4 front corners of one box: an L on the front plus wraps onto the side and top/bottom."""
    out = []
    L, B = 0.070, 0.024
    yt = yb + SEC
    for sx in (-1, 1):
        xe = X1 * sx
        for yy, sy in ((yt, -1), (yb, 1)):
            xa, xb = sorted((xe, xe - sx * L))
            ya, yb_ = sorted((yy, yy + sy * B))
            out.append(iron_box(xa, xb, ya, yb_, Z1, Z1 + IT))                         # front, horizontal leg
            xa, xb = sorted((xe, xe - sx * B))
            ya, yb_ = sorted((yy + sy * B, yy + sy * L))
            out.append(iron_box(xa, xb, ya, yb_, Z1, Z1 + IT))                         # front, vertical leg
            xa, xb = sorted((xe, xe + sx * IT))
            ya, yb_ = sorted((yy, yy + sy * L))
            out.append(iron_box(xa, xb, ya, yb_, Z1 - 0.050, Z1 + IT))                 # side wrap
            ya, yb_ = sorted((yy, yy - sy * IT))
            xa, xb = sorted((xe, xe - sx * 0.050))
            out.append(iron_box(xa, xb, ya, yb_, Z1 - 0.050, Z1 + IT))                 # top / bottom wrap
    # far LOD: one plate per corner on the front
    for sx in (-1, 1):
        for yy, sy in ((yt, -1), (yb, 1)):
            xa, xb = sorted((X1 * sx, X1 * sx - sx * 0.05))
            ya, yb_ = sorted((yy, yy + sy * 0.05))
            out.append(iron_box(xa, xb, ya, yb_, Z1, Z1 + IT, vis=(2,)))
    return out


def side_handles(yb):
    """Folding bar handle (sao-kan) on each side near the top of the box, hanging down against the board."""
    out = []
    yt = yb + SEC
    yh = yt - 0.065
    for sx in (-1, 1):
        xo = X1 * sx
        xa, xb = sorted((xo, xo + sx * 0.010))
        xc, xd = sorted((xo, xo + sx * 0.016))
        for zc in (-0.075, 0.075):
            out.append(iron_box(xa, xb, yh - 0.020, yh + 0.020, zc - 0.018, zc + 0.018))   # boss plates
            out.append(iron_box(xc, xd, yh - 0.050, yh, zc - 0.005, zc + 0.005))          # drop links
        out.append(iron_box(xc, xd, yh - 0.062, yh - 0.050, -0.090, 0.090))              # bar
        xe, xf = sorted((xo, xo + sx * 0.014))
        out.append(iron_box(xe, xf, yh - 0.060, yh + 0.020, -0.095, 0.095, vis=(2,)))    # far LOD: one block
    return out


def collision(x0, x1, y0, y1, z0, z1):
    return box(x0, x1, y0, y1, z0, z1, WOOD, vis=(), geo=True, view=True, fire=True)


def dropped_drawer(name):
    """Build the drawer (front + body) at its slot, then move it to the floor in front: yaw FLOOR_YAW about +y,
    bottom on the floor, the whole footprint inside the front zone."""
    x0, x1, y0, y1 = OPEN[name]
    ss = drawer_front(name, 0.0, lod=1, k=2) + drawer_body(name, 0.0)
    zf = Z1 - REC
    zb = zf - DDEPTH
    far = [box(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, zb, zf, WOOD, vis=(3,))]
    dy = -(y0 + GAP)
    # move so the drawer's back-left bottom corner = origin, rotate, then place
    pre = (-(x0 + GAP), dy, -zb)
    out = []
    for s in ss + far:
        m = s.transformed(0.0, pre)
        out.append(m)
    # footprint after rotation, to place it inside the zone
    wdt, dep = (x1 - x0 - 2 * GAP), DDEPTH
    corners = [core.rot_y(p, FLOOR_YAW) for p in ((0, 0, 0), (wdt, 0, 0), (0, 0, dep), (wdt, 0, dep))]
    minx = min(c[0] for c in corners)
    maxx = max(c[0] for c in corners)
    minz = min(c[2] for c in corners)
    tx = -(minx + maxx) / 2
    # clear of the carcass AND of the pulled-out bottom drawer (it sticks out at floor level)
    lo = RANSACK.get("d_lo_2", 0.0)
    face = max(Z1, Z1 - REC + (lo if isinstance(lo, float) else 0.0))
    tz = face + FLOOR_GAP - minz
    placed = [s.transformed(FLOOR_YAW, (tx, 0.0, tz)) for s in out]
    # collision: the rotated drawer box (convex hexahedron)
    top = y1 - y0 - 2 * GAP
    cs = [core.add(core.rot_y(p, FLOOR_YAW), (tx, 0.0, tz)) for p in
          ((0, 0, 0), (wdt, 0, 0), (wdt, 0, dep), (0, 0, dep))]
    hexa = core.hexa(cs + [(c[0], top, c[2]) for c in cs], WOOD, vis=(), geo=True, view=True, fire=True)
    # loot point: centre of the drawer floor
    cen = core.add(core.rot_y((wdt / 2, DB + 0.002, dep / 2 - 0.01), FLOOR_YAW), (tx, 0.0, tz))
    return placed, hexa, cen


# ------------------------------------------------------------------------------------------------ model
def model(state="intact"):
    P = TansuPart("jp_f_tansu", "" if state == "intact" else "_ransacked")
    P.wear = "_w1"
    P.floors = []
    ransack = RANSACK if state == "ransacked" else {}
    for s in carcass(0.0) + carcass(SEC, upper=True):
        P.add(s)
    # Res 3: two plain boxes (+ proud fronts); carcass board sets carry Res 1-2
    P.add(wood(X0, X1, 0.0, SEC, Z0, Z1, vis=(3,)))
    P.add(wood(X0, X1, SEC, H, Z0, Z1, vis=(3,)))
    for yb in (0.0, SEC):
        for s in corner_fittings(yb) + side_handles(yb):
            P.add(s)
    loot = {"loot_top_1": [(-0.25, H, 0.0)], "loot_top_2": [(0.25, H, 0.0)]}
    for k, name in enumerate(["d_up_l", "d_up_r", "d_up_w", "d_lo_1", "d_lo_2"]):
        act = ransack.get(name, 0.0)
        if act == "floor":
            placed, hexa, cen = dropped_drawer(name)
            for s in placed:
                s.tag = "dropped"
                P.add(s)
            P.add(hexa)
            loot["loot_drawer"] = [cen]
            continue
        dz = float(act)
        for s in drawer_front(name, dz, lod=1, k=k):
            P.add(s)
        if dz > 0:
            for s in drawer_body(name, dz):
                P.add(s)
            # far LOD front, proud of the Res 3 box
        far = drawer_front(name, dz + (0.0015 + REC if dz == 0 else 0.0), lod=3, k=k)
        for s in far:
            P.add(s)
        if dz > 0:
            x0, x1, y0, y1 = OPEN[name]
            P.add(box(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, Z1, Z1 - REC + dz, WOOD, vis=(3,)))
            P.add(collision(x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP, Z1, Z1 - REC + dz))
    # collision / view / fire: one convex box per carcass
    P.add(collision(X0, X1, 0.0, SEC, Z0, Z1))
    P.add(collision(X0, X1, SEC, H, Z0, Z1))
    P.memory.update(loot)
    return P


def geo_props():
    return {"autocenter": "0"}       # as vanilla furniture ODOLs (case_bedroom_b: autocenter=0 only)


if __name__ == "__main__":
    for st in ("intact", "ransacked"):
        p = model(st)
        ls = p.lods(geo_props(), MASS)
        print(st, {mlod.lod_name(l.resolution): len(l.faces) for l in ls})
