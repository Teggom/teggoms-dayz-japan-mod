"""jp_f_tansu (BUILD_LIST row 26): the clothing chest of drawers (isho-dansu), two stacked boxes, in two states.

  intact    - closed, weathered and dusty ("as left" 0-2 years)
  ransacked - three drawers pulled out, the fourth lying on the floor in the tansu's front zone

Frame (PLAYBOOK §10.4 furniture): origin = base centre on the floor, +y up, +z = the FRONT (drawer side), +x = right
(seen from the front the viewer has +x on the left, as in any p3d). autocenter=0, so the origin is the placement point.

Built with the parts kit's Part / Solid (parts/kit/jpparts/core.py, imported read-only): closed convex solids that
are flat-shaded visual meshes AND Geometry / View / Fire components, library materials by path, world-scale UVs with
the grain along each member's long axis.

Design (refs: i07 Fukagawa Edo Museum tenement tansu, i01 Kasuya house tansu; see REPORT.md):
  - two boxes 1.00 x 0.45 x 0.50, 20 mm boards, 12 mm back board, two full-width drawers each (4 drawers)
  - drawer fronts 4 mm behind the carcass face, 3 mm gap all round (reads as the drawer outline)
  - per drawer: two iron ring pulls (kan) hanging from small plates, one oval lock plate (jomae) with a keyhole
  - iron corner caps (sumi-kanagu) on all 8 corners of each box, a clasp plate across the joint at the front,
    and a hanging bail handle (tebiki) high on each side of each box (4) for carrying the boxes separately
"""
import copy
import math
import os
import sys

sys.dont_write_bytecode = True                   # never write __pycache__ into parts/ (read-only for this agent)
HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import core  # noqa: E402
from jpparts.core import Part, Solid, box, prism, sheet  # noqa: E402

# ------------------------------------------------------------------------------------------------ materials
WOOD = "wood_street_dark"      # body: stand-in for jp_m_wood_interior (not built yet); _w2 = dusty, pale edge wear
RAW = "wood_weathered"         # drawer boxes (sides, back, bottom): paler raw wood inside, _w2 passes timber_interior
DARK = "wood_sooted"           # the faces that look INTO the carcass cavity (back, walls, ceiling) + the keyholes
IRON = "metal_iron"            # every fitting (jp_m_metal_iron -> iron_black), glossy by design (T12)
WEAR = "_w2"
WEAR_BY_MAT = {IRON: "_w1", DARK: "_w0"}

# ------------------------------------------------------------------------------------------------ dimensions (m)
W, D, H = 1.00, 0.45, 1.00
HS = 0.50                       # one box
X0, X1 = -W / 2, W / 2
Z0, Z1 = -D / 2, D / 2          # Z1 = front face
T = 0.020                       # sides, top, bottom
TB = 0.012                      # back board
TR = 0.020                      # divider between the two drawers of a box
OH = (HS - 2 * T - TR) / 2      # drawer opening height 0.220
GAP = 0.003                     # drawer front to frame
REC = 0.004                     # drawer front behind the carcass face
TF = 0.020                      # drawer front thickness
DD = 0.410                      # drawer depth, front face to back face
TS = 0.012                      # drawer side / back
TBOT = 0.010                    # drawer bottom
SH = 0.200                      # drawer side height (front is 0.214)
XI = X1 - T                     # 0.48: inner face of the side boards
ZF = Z1 - REC                   # 0.221: closed drawer front face

# fittings
PLATE_T = 0.003
PULL_X = 0.285                  # ring pulls +-0.285 from the centre (about a fifth in from each end, as i07)
RING_R, RING_r, RING_N = 0.028, 0.004, 8     # ring 6.4 cm across: about a third of the drawer height, as i07
PLATE_R = 0.024
LOCK_RX, LOCK_RY = 0.030, 0.040
CAP = 0.045                     # corner cap leg length
CAP_OUT = 0.002                 # how far a cap stands proud of the wood
HANDLE_W = 0.150                # side handle: arm centres +-0.075 in z
HANDLE_BAR = 0.010              # its bar section

# drawers: (id, box y0, slot 0 = lower slot of the box / 1 = upper slot)
DRAWERS = [("L2", 0.0, 0), ("L1", 0.0, 1), ("U2", HS, 0), ("U1", HS, 1)]
# ransacked: pull-out distance per drawer (m); U2 is on the floor. An empty drawer's centre of mass is ~0.17 m
# behind its front face (front board + box, see REPORT), so a drawer pulled further than that tips until the rear
# top edge of its sides catches the board above: L1 droops (angle computed in drawer_droop), U1 and L2 stay level.
PULL = {"U1": 0.155, "L1": 0.255, "L2": 0.050}
DRAWER_COM = 0.172
FLOOR_DRAWER = "U2"
FLOOR_YAW = 18.0                # deg, the dropped drawer lies askew (9 deg read as a fifth drawer pulled out)
FLOOR_X = 0.12
# UV: put each drawer front between two plank seams of the wood texture (seams at u = 367 and 516 px of 1024,
# measured on jp_m_wood_street_dark_w2_co.png), different grain stretch per drawer
SEAM_FREE_U = (367 + 516) / 2.0 / 1024.0
SEAM_FREE_TOP = (737 + 959) / 2.0 / 1024.0
V_OFF = {"L2": 0.07, "L1": 0.33, "U2": 0.58, "U1": 0.81}


def opening(y0, slot):
    """(bottom, top) of a drawer opening."""
    b = y0 + T + slot * (OH + TR)
    return b, b + OH


# ------------------------------------------------------------------------------------------------ helpers
def ngon_xy(cx, cy, rx, ry, n, phase):
    return [(cx + rx * math.cos(phase + 2 * math.pi * k / n), cy + ry * math.sin(phase + 2 * math.pi * k / n))
            for k in range(n)]


def plate(poly, z0, z1, mats, vis=(1,), tag=""):
    """A thin plate on a +z facing surface: front cap + rim, no back cap (it lies on the wood): visual sheet."""
    quads, normals = [], []
    n = len(poly)
    front = [(x, y, z1) for x, y in poly]
    k = 1
    while k < n - 1:                                   # front cap as a quad fan
        idx = [0, k, k + 1, k + 2] if k + 2 < n else [0, k, k + 1]
        quads.append([front[i] for i in idx])
        normals.append((0.0, 0.0, 1.0))
        k += len(idx) - 2
    cx = sum(p[0] for p in poly) / n
    cy = sum(p[1] for p in poly) / n
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2 - cx, (a[1] + b[1]) / 2 - cy
        ln = math.hypot(mx, my) or 1.0
        quads.append([(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)])
        normals.append((mx / ln, my / ln, 0.0))
    return sheet(quads, mats, normals, vis=vis, tag=tag)


def ring(px, py, zf, vis=(1,), n=RING_N, m=4):
    """Iron ring (kan) hanging from a pin at (px, py): an n x m torus sheet, its plane tilted so the top is held off
    the plate by the pin and the bottom rests on the drawer front."""
    zp = zf + PLATE_T + RING_r + 0.0005                  # centreline z at the pin
    s = (zp - (zf + RING_r)) / (2 * RING_R)               # bottom centreline at zf + r -> tube touches the wood
    a = math.asin(s)
    e1 = (1.0, 0.0, 0.0)
    e2 = (0.0, math.cos(a), math.sin(a))                  # ring "up", tilted: top further out than the bottom
    nr = (0.0, -math.sin(a), math.cos(a))                 # ring plane normal (faces the viewer)
    c = (px, py - RING_R * e2[1], zp - RING_R * e2[2])

    def pt(phi, psi):
        rho = tuple(math.cos(phi) * e1[i] + math.sin(phi) * e2[i] for i in range(3))
        return tuple(c[i] + RING_R * rho[i] + RING_r * (math.cos(psi) * rho[i] + math.sin(psi) * nr[i])
                     for i in range(3))

    def nrm(phi, psi):
        rho = tuple(math.cos(phi) * e1[i] + math.sin(phi) * e2[i] for i in range(3))
        return tuple(math.cos(psi) * rho[i] + math.sin(psi) * nr[i] for i in range(3))
    quads, normals = [], []
    ph0 = math.pi / 2 + math.pi / n                      # a flat segment across the top, through the pin
    ps0 = math.pi / m
    for i in range(n):
        f0, f1 = ph0 + 2 * math.pi * i / n, ph0 + 2 * math.pi * (i + 1) / n
        for j in range(m):
            s0, s1 = ps0 + 2 * math.pi * j / m, ps0 + 2 * math.pi * (j + 1) / m
            quads.append([pt(f0, s0), pt(f1, s0), pt(f1, s1), pt(f0, s1)])
            normals.append(nrm((f0 + f1) / 2, (s0 + s1) / 2))
    return sheet(quads, IRON, normals, vis=vis, tag="ring")


# ------------------------------------------------------------------------------------------------ carcass
def carcass(p, y0, vis=(1, 2)):
    """One box, hollow (sides, top, bottom, divider, back). Faces that look into a drawer cavity are DARK, except the
    cavity floors (the bottom board and the divider top), which stay wood."""
    y1 = y0 + HS
    ym = y0 + T + OH + TR / 2
    p.add(box(X0, X0 + T, y0, y1, Z0, Z1, {"right": DARK, "default": WOOD}, vis=vis, tag="side"))
    p.add(box(X1 - T, X1, y0, y1, Z0, Z1, {"left": DARK, "default": WOOD}, vis=vis, tag="side"))
    # top board: u = z / 2 + uoff; the upper box's top (the visible one) sits in the widest seam-free band of the
    # texture (columns 737-959 of 1024), so the 0.45 m depth shows one board with its seams at the edges
    p.add(box(-XI, XI, y1 - T, y1, Z0, Z1, {"bottom": DARK, "default": WOOD}, vis=vis, tag="top",
              uvoff=(SEAM_FREE_TOP if y0 else 0.41, 0.0)))
    p.add(box(-XI, XI, y0, y0 + T, Z0, Z1, WOOD, vis=vis, tag="bottom", uvoff=(0.63, 0.2)))
    p.add(box(-XI, XI, ym - TR / 2, ym + TR / 2, Z0 + TB, Z1, {"bottom": DARK, "default": WOOD}, vis=vis,
              tag="divider", uvoff=(0.27, 0.5)))
    p.add(box(-XI, XI, y0 + T, y1 - T, Z0, Z0 + TB, {"front": DARK, "default": WOOD}, vis=vis, tag="back"))


def carcass_lod3(p, y0, cavity_slot=None):
    """Resolution 3: one block per box (or, with an empty drawer slot, the block around the dark slot)."""
    y1 = y0 + HS
    if cavity_slot is None:
        p.add(box(X0, X1, y0, y1, Z0, Z1, WOOD, vis=(3,), tag="lod3_box"))
        return
    b, t = opening(y0, cavity_slot)
    if b - y0 > 0.001:
        p.add(box(X0, X1, y0, b, Z0, Z1, WOOD, vis=(3,), tag="lod3_box"))
    if y1 - t > 0.001:
        p.add(box(X0, X1, t, y1, Z0, Z1, WOOD, vis=(3,), tag="lod3_box"))
    p.add(box(X0, X0 + T, b, t, Z0, Z1, WOOD, vis=(3,), tag="lod3_box"))
    p.add(box(X1 - T, X1, b, t, Z0, Z1, WOOD, vis=(3,), tag="lod3_box"))
    p.add(box(-XI, XI, b, t, Z0, Z0 + TB, {"front": DARK, "default": WOOD}, vis=(3,), tag="lod3_box"))


# ------------------------------------------------------------------------------------------------ drawers
def front_solid(did, yb, yt, zf, vis):
    uo = SEAM_FREE_U + (yb + yt) / 4.0                  # u = -y / 2 + uoff on a +z face (grain along x)
    return box(-XI + GAP, XI - GAP, yb, yt, zf - TF, zf, WOOD, vis=vis, tag="front", uvoff=(uo, V_OFF[did]))


def drawer_box(yb, zf, vis):
    """Sides, back and bottom of a drawer whose front face is at zf (raw wood)."""
    xs = XI - GAP                    # 0.477
    zb = zf - DD                     # back face
    out = [box(-xs + 0.003, -xs + 0.003 + TS, yb, yb + SH, zb, zf - TF, RAW, vis=vis, tag="dside"),
           box(xs - 0.003 - TS, xs - 0.003, yb, yb + SH, zb, zf - TF, RAW, vis=vis, tag="dside"),
           box(-xs + 0.003 + TS, xs - 0.003 - TS, yb + TBOT, yb + SH - 0.010, zb, zb + TS, RAW, vis=vis, tag="dback"),
           box(-xs + 0.003 + TS, xs - 0.003 - TS, yb, yb + TBOT, zb, zf - TF, RAW, vis=vis, tag="dbottom")]
    return out


def front_fittings(yb, yt, zf, lod):
    """Ring pulls and the lock plate on one drawer front. lod 1: full; lod 2: blocks."""
    yc = (yb + yt) / 2
    out = []
    pin_y = yc + 0.028                 # the ring hangs from yc + 0.028 to yc - 0.028
    lock_y = yc + 0.052                # upper half of the front, as i07
    for sx in (-1, 1):
        px = sx * PULL_X
        if lod == 1:
            out.append(plate(ngon_xy(px, pin_y, PLATE_R, PLATE_R, 6, math.pi / 6), zf, zf + PLATE_T, IRON, vis=(1,),
                             tag="pull_plate"))
            out.append(ring(px, pin_y, zf, vis=(1,)))
            zp = zf + PLATE_T + RING_r + 0.0005
            out.append(box(px - 0.0045, px + 0.0045, pin_y - 0.004, pin_y + 0.007, zf + PLATE_T, zp + RING_r + 0.0012,
                           IRON, vis=(1,), tag="pull_eye"))
        else:
            out.append(box(px - RING_R - RING_r, px + RING_R + RING_r, pin_y - 2 * RING_R - RING_r, pin_y + 0.006,
                           zf, zf + 0.007, IRON, vis=(2,), tag="pull_lod2"))
    if lod == 1:
        out.append(plate(ngon_xy(0.0, lock_y, LOCK_RX, LOCK_RY, 8, math.pi / 8), zf, zf + PLATE_T, IRON, vis=(1,),
                         tag="lock"))
        out.append(box(-0.0028, 0.0028, lock_y - 0.017, lock_y + 0.004, zf + PLATE_T, zf + PLATE_T + 0.0008, DARK,
                       vis=(1,), tag="keyhole"))
        out.append(box(-0.0050, 0.0050, lock_y + 0.001, lock_y + 0.010, zf + PLATE_T, zf + PLATE_T + 0.0008, DARK,
                       vis=(1,), tag="keyhole"))
    else:
        out.append(box(-LOCK_RX, LOCK_RX, lock_y - LOCK_RY, lock_y + LOCK_RY, zf, zf + PLATE_T, IRON, vis=(2,),
                       tag="lock_lod2"))
    return out


def tilt_x(s, deg, py, pz):
    """A finalized copy of solid s turned about the x axis through (y, z) = (py, pz); deg > 0 lowers the +z end.
    Like Solid.transformed (the kit only yaws): materials and UVs stay as resolved, normals turn with it."""
    s.finalize()
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)

    def R(p):
        y, z = p[1] - py, p[2] - pz
        return (p[0], py + y * c - z * sn, pz + y * sn + z * c)
    t = copy.copy(s)
    t.verts = [R(v) for v in s.verts]
    t.center = R(s.center)
    t.fn = [(n[0], n[1] * c - n[2] * sn, n[1] * sn + n[2] * c) for n in s.fn]
    if s.normals is not None:
        t.normals = t.fn
    t.faces = [list(f) for f in s.faces]
    return t


def drawer_droop(yb, t, zf):
    """Tip angle (deg) of a drawer pulled out past its centre of mass: it turns about the carcass front edge under
    it (y = yb, z = Z1) until the rear top corner of its sides is 1 mm under the board above (y = t)."""
    if zf - Z1 <= DRAWER_COM:
        return 0.0
    dy, dz = SH, (zf - DD) - Z1                  # rear top corner of the sides, relative to the pivot (dz < 0)
    r = math.hypot(dy, dz)
    phi = math.atan2(-dz, dy)
    target = (t - 0.001) - yb
    return math.degrees(phi - math.acos(min(1.0, target / r)))


def drawer(did, y0, slot, dz, with_box):
    """All solids of one drawer pulled out by dz: front (Res 1-2), box (Res 1-2) if with_box, fittings (Res 1 full,
    Res 2 blocks), a Res 3 block and, when pulled out, its collision block (the part outside the carcass). A drawer
    pulled past its centre of mass droops (drawer_droop). Returns (solids, (yb, yt, zf), droop_deg)."""
    b, t = opening(y0, slot)
    yb, yt = b + GAP, t - GAP
    zf = ZF + dz
    out = [front_solid(did, yb, yt, zf, (1, 2))]
    if with_box:
        out += drawer_box(yb, zf, (1, 2))
    out += front_fittings(yb, yt, zf, 1) + front_fittings(yb, yt, zf, 2)
    if dz < 0.001:                                           # closed: Res 3 front block, 3 mm proud
        out.append(box(-XI + GAP, XI - GAP, yb, yt, Z1, Z1 + 0.003, WOOD, vis=(3,), tag="lod3_front",
                       uvoff=(SEAM_FREE_U + (yb + yt) / 4.0, V_OFF[did])))
        return out, (yb, yt, zf), 0.0
    out.append(box(-XI + GAP, XI - GAP, yb, yt, Z1, zf, {"top": RAW, "default": WOOD}, vis=(3,), tag="lod3_front"))
    out.append(box(-XI + GAP, XI - GAP, yb, yt, Z1, zf, WOOD, vis=(), geo=True, view=True, fire=True,
                   tag="coll_drawer"))
    droop = drawer_droop(yb, t, zf) if with_box else 0.0
    if droop:
        out = [tilt_x(s, droop, yb, Z1) for s in out]
    return out, (yb, yt, zf), droop


# ------------------------------------------------------------------------------------------------ fittings on the boxes
def corner_caps(y0, lod_vis):
    """Iron caps folded round the 8 corners of one box. The front leg covers the side board's edge only."""
    out = []
    y1 = y0 + HS
    for sx in (-1, 1):
        xa, xb = (X1 - T + 0.001, X1 + CAP_OUT) if sx > 0 else (X0 - CAP_OUT, X0 + T - 0.001)
        for zs in (-1, 1):
            za, zb = (Z1 - CAP, Z1 + CAP_OUT) if zs > 0 else (Z0 - CAP_OUT, Z0 + CAP)
            for ys in (0, 1):
                if ys == 0:
                    ya, yb = y0, y0 + CAP                   # floor or the joint: never below the box
                else:
                    ya, yb = y1 - CAP, (y1 + CAP_OUT if y0 > 0 else y1)   # only the top box's top caps stand proud
                if lod_vis == (2,) and zs < 0:
                    continue                                  # Res 2: front caps only
                out.append(box(xa, xb, ya, yb, za, zb, IRON, vis=lod_vis, tag="cap"))
    return out


def side_handle(sx, y0, lod):
    """Bail handle (tebiki) hanging on a side of one box: two rosettes, two arms, the grip."""
    xs = X1 if sx > 0 else X0
    yp = y0 + HS - 0.060                                    # pivots 6 cm under the box top
    out = []

    def xr(a, b):                                          # offset range away from the side face
        return (xs + a, xs + b) if sx > 0 else (xs - b, xs - a)
    hb = HANDLE_BAR
    drop = 0.045                                           # arm length: the grip hangs 4.5 cm under the pivots
    if lod == 1:
        for zc in (-HANDLE_W / 2, HANDLE_W / 2):
            x0, x1 = xr(0.0, 0.003)
            out.append(box(x0, x1, yp - 0.017, yp + 0.017, zc - 0.017, zc + 0.017, IRON, vis=(1,), tag="rosette"))
            x0, x1 = xr(0.003, 0.003 + hb)
            out.append(box(x0, x1, yp - drop, yp + 0.005, zc - 0.004, zc + 0.004, IRON, vis=(1,), tag="arm"))
        x0, x1 = xr(0.003, 0.003 + hb)
        out.append(box(x0, x1, yp - drop - hb, yp - drop, -HANDLE_W / 2 - 0.004, HANDLE_W / 2 + 0.004, IRON,
                       vis=(1,), tag="grip"))
    else:
        x0, x1 = xr(0.0, 0.003 + hb)
        out.append(box(x0, x1, yp - drop - hb, yp + 0.017, -HANDLE_W / 2 - 0.017, HANDLE_W / 2 + 0.017, IRON,
                       vis=(2,), tag="handle_lod2"))
    return out


def clasp(vis):
    """Plate across the joint of the two boxes, front centre (i07)."""
    return [box(-0.020, 0.020, HS - 0.019, HS + 0.019, Z1, Z1 + PLATE_T, IRON, vis=vis, tag="clasp")]


# ------------------------------------------------------------------------------------------------ the floor drawer
def floor_drawer_solids():
    """The dropped drawer (U2) standing upright on the floor in front, askew. Built closed in its slot, moved to
    the origin (footprint centre), turned FLOOR_YAW and set down at (FLOOR_X, 0, cz). Returns (solids, info)."""
    did = FLOOR_DRAWER
    y0, slot = [(a, b) for d, a, b in DRAWERS if d == did][0]
    b, t = opening(y0, slot)
    yb, yt = b + GAP, t - GAP
    local = [front_solid(did, yb, yt, ZF, (1, 2))] + drawer_box(yb, ZF, (1, 2))
    local += front_fittings(yb, yt, ZF, 1) + front_fittings(yb, yt, ZF, 2)
    # Res 3: bottom + four walls (the hollow reads at a distance)
    xs = XI - GAP
    zb = ZF - DD
    local += [box(-xs, xs, yb, yb + TBOT, zb, ZF - TF, RAW, vis=(3,), tag="lod3_fd"),
              box(-xs, xs, yb, yt, ZF - TF, ZF, WOOD, vis=(3,), tag="lod3_fd",
                  uvoff=(SEAM_FREE_U + (yb + yt) / 4.0, V_OFF[did])),
              box(-xs, xs, yb + TBOT, yb + SH, zb, zb + TS, RAW, vis=(3,), tag="lod3_fd"),
              box(-xs, -xs + TS, yb + TBOT, yb + SH, zb + TS, ZF - TF, RAW, vis=(3,), tag="lod3_fd"),
              box(xs - TS, xs, yb + TBOT, yb + SH, zb + TS, ZF - TF, RAW, vis=(3,), tag="lod3_fd")]
    # collision (invisible): Geometry = bottom + 4 walls so loot can lie inside; View / Fire = one block
    local += [box(-xs, xs, yb, yb + TBOT, zb, ZF - TF, RAW, vis=(), geo=True, tag="geo_fd"),
              box(-xs, xs, yb, yt, ZF - TF, ZF, WOOD, vis=(), geo=True, tag="geo_fd"),
              box(-xs, xs, yb + TBOT, yb + SH, zb, zb + TS, RAW, vis=(), geo=True, tag="geo_fd"),
              box(-xs, -xs + TS, yb + TBOT, yb + SH, zb + TS, ZF - TF, RAW, vis=(), geo=True, tag="geo_fd"),
              box(xs - TS, xs, yb + TBOT, yb + SH, zb + TS, ZF - TF, RAW, vis=(), geo=True, tag="geo_fd"),
              box(-xs, xs, yb, yb + SH, zb, ZF, WOOD, vis=(), view=True, fire=True, tag="vf_fd")]
    # local frame -> footprint centre at the origin, bottom on y = 0
    cxl, czl = 0.0, (zb + ZF) / 2
    half_x, half_z = xs, (ZF - zb) / 2
    a = math.radians(FLOOR_YAW)
    ext_z = half_x * abs(math.sin(a)) + half_z * abs(math.cos(a))
    ext_x = half_x * abs(math.cos(a)) + half_z * abs(math.sin(a))
    # behind it: the L2 drawer front (pulled PULL['L2']) plus its rings (~1.2 cm) and a 2 cm margin
    z_rear = ZF + PULL["L2"] + 0.012 + 0.020
    cz = z_rear + ext_z
    moved = []
    for s in local:
        s.finalize()                                    # materials + UVs in the slot frame, so they move with it
        s0 = s.transformed(0.0, (-cxl, -yb, -czl))
        moved.append(s0.transformed(FLOOR_YAW, (FLOOR_X, 0.0, cz)))
    # the loot point: middle of the inside bottom (bottom board top face)
    zin = ((zb + TS) + (ZF - TF)) / 2 - czl
    lp = core.rot_y((0.0, TBOT, zin), FLOOR_YAW)
    xi = xs - 0.003 - TS
    poly = []
    for px, pz in ((-xi, zb + TS), (xi, zb + TS), (xi, ZF - TF), (-xi, ZF - TF)):     # inner bottom, 4 corners
        q = core.rot_y((px, 0.0, pz - czl), FLOOR_YAW)
        poly.append([round(q[0] + FLOOR_X, 4), round(q[2] + cz, 4)])
    info = {"centre": (FLOOR_X, cz), "yaw_deg": FLOOR_YAW, "extent_x": ext_x, "extent_z": ext_z,
            "z_rear": z_rear, "z_front": cz + ext_z, "loot_point": (lp[0] + FLOOR_X, TBOT, lp[2] + cz),
            "inner_half": (xi, ((ZF - TF) - (zb + TS)) / 2), "inner_poly_xz": poly}
    return moved, info


# ------------------------------------------------------------------------------------------------ the model
def build(state):
    """state 'intact' | 'ransacked' -> (Part, meta)"""
    assert state in ("intact", "ransacked")
    p = Part("jp_f_tansu", "" if state == "intact" else "_ransacked", "furniture",
             used_for="isho-dansu (clothing chest of drawers), zashiki / sleeping rooms of T2-3 town houses")
    p.wear = WEAR
    p.wear_by_mat = dict(WEAR_BY_MAT)
    meta = {"state": state}
    rans = state == "ransacked"
    # carcass, both boxes (Res 1-2 hollow; Res 3 blocks)
    for y0 in (0.0, HS):
        carcass(p, y0)
        cav = None
        if rans:
            cav = [s for d, a, s in DRAWERS if d == FLOOR_DRAWER and a == y0]
            cav = cav[0] if cav else None
        carcass_lod3(p, y0, cav)
        p.extend(corner_caps(y0, (1,)))
        p.extend(corner_caps(y0, (2,)))
        for sx in (-1, 1):
            p.extend(side_handle(sx, y0, 1))
            p.extend(side_handle(sx, y0, 2))
    p.extend(clasp((1, 2)))
    # drawers
    fronts = {}
    for did, y0, slot in DRAWERS:
        if rans and did == FLOOR_DRAWER:
            continue
        dz = PULL.get(did, 0.0) if rans else 0.0
        ss, fr, droop = drawer(did, y0, slot, dz, with_box=rans)     # pulled drawers bring their collision block
        p.extend(ss)
        fronts[did] = fr
        if droop:
            meta.setdefault("droop_deg", {})[did] = round(droop, 2)
    # collision: one block per box (+ the pulled drawers above, + the floor drawer below)
    for y0 in (0.0, HS):
        p.add(box(X0, X1, y0, y0 + HS, Z0, Z1, WOOD, vis=(), geo=True, view=True, fire=True, tag="coll_box"))
    if rans:
        fd, info = floor_drawer_solids()
        p.extend(fd)
        meta["floor_drawer"] = info
    meta["fronts"] = fronts
    return p, meta


def loot_surfaces(state, meta):
    """BUILD_LIST row 26: top at 1.00: 2 points (range 0.2); ransacked: + 1 point in the dropped drawer (floor)."""
    out = [{"name": "top", "container": "lootshelves", "tag": "shelves", "height": H,
            "rect_xz": [X0, Z0, X1, Z1], "range": 0.2,
            "points": [[-0.25, H, 0.0], [0.25, H, 0.0]]}]
    if state == "ransacked":
        fi = meta["floor_drawer"]
        lp = fi["loot_point"]
        out.append({"name": "dropped_drawer", "container": "lootshelves", "tag": "shelves", "height": round(lp[1], 4),
                    "poly_xz": fi["inner_poly_xz"],
                    "range": 0.15, "points": [[round(lp[0], 4), round(lp[1], 4), round(lp[2], 4)]],
                    "note": "inside the dropped drawer on the floor (bottom board top face); range 0.15 keeps it "
                            "inside the %.2f x %.2f m inner bottom" % (2 * fi["inner_half"][0], 2 * fi["inner_half"][1])})
    for s in out:
        s["ce_points"] = [[round(p[2], 4), round(p[1], 4), round(-p[0], 4)] for p in s["points"]]   # (mz, my, -mx)
    return out


def front_zone(state, meta):
    """The floor the decorator must keep for this prop in front of it: the drawers pulled fully out (0.41) when
    intact; the real extent of the pulled and dropped drawers when ransacked (plus the side handles)."""
    def lo(v):
        return math.floor(v * 100.0) / 100.0              # outward to the cm

    def hi(v):
        return math.ceil(v * 100.0) / 100.0
    if state == "intact":
        return {"x": [lo(X0 - 0.02), hi(X1 + 0.02)], "z": [Z1, hi(ZF + DD + 0.02)],
                "why": "a drawer pulled fully out (+ its ring pulls)"}
    fi = meta["floor_drawer"]
    m = 0.02                                               # ring pulls + margin
    return {"x": [lo(min(X0 - 0.02, fi["centre"][0] - fi["extent_x"] - m)),
                  hi(max(X1 + 0.02, fi["centre"][0] + fi["extent_x"] + m))],
            "z": [Z1, hi(fi["z_front"] + m)], "why": "pulled drawers + the dropped drawer (inside this zone)"}
