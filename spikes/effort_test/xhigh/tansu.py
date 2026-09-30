"""jp_f_tansu for the effort test (level xhigh): clothing chest of drawers (isho-dansu), two stacked parts.

BUILD_LIST row 26: 1.00 x 0.45 x 1.00 m (two parts of 0.50), 5 drawers, iron ring pulls, carrying handles on the
sides, wood body, iron fittings; T2-3. Two states:
  A  model("A")  intact: every drawer shut, dust-worn finish (the wear level carries the dust).
  B  model("B")  ransacked: the upper wide (lock) drawer lies on the floor in front, three drawers pulled out, one shut.

Frame (PLAYBOOK 10.4, vanilla furniture): origin = base centre on the floor, +y up, +z = the FRONT (drawers),
autocenter=0. +x is the chest's own right (a viewer facing the drawers sees +x on the LEFT; DayZ is left-handed).

Built on the parts kit's Solid / Part (read-only import of japan_dev/parts/kit/jpparts): flat-shaded faces with
world-scale UVs, Geometry / View / Fire from closed convex boxes. Hidden faces are simply not emitted (sheets).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import core, mlod  # noqa: E402

# ------------------------------------------------------------------------------------------------ materials
# jp_m_wood_interior / timber_interior is not built yet (BUILD_LIST B1). Closest library stand-ins:
WOOD = "wood_street_dark"    # show wood: dE76 8.8 (_w2) to timber_interior (69,52,46), tolerance 14; oiled dark sugi
INNER = "wood_sooted"        # inside faces of the carcass (seen only through an empty or pulled drawer): fakes the
#                              occlusion of a closed cabinet (timber_sooted, near-black brown)
RAW = "wood_weathered"       # drawer boxes (sides, back, bottom, the inside of the front): unfinished secondary wood
IRON = "metal_iron"          # iron_black, dE76 1.0 at _w1; glossy by design (PLAYBOOK 15.3 T12)
WEAR = {WOOD: "_w2", INNER: "_w0", RAW: "_w1", IRON: "_w1"}   # _w2 street_dark = "dusty, raised grain, pale edge wear"

TILE = 2.0                   # wood textures: 2.0 m tile, 1024 px, planks run along v
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
# street_dark (and sooted, the same source photo) is 14 boards of ~73 px (0.143 m): thin joint lines at these pixel
# columns (high-pass scan of jp_m_wood_street_dark_w2_co.png, 2026-09-29). A drawer front is ONE board in a real
# tansu, so each front is fitted into one board (stretched 1.3-2.0x across the grain); larger faces keep the native
# scale and show the joints as the several boards they are.
JOINTS_PX = [3, 76, 149, 222, 294, 366, 440, 515, 588, 660, 737, 810, 882, 953, 1027]
DARK_BOARD = (953 / 1024.0, 1027 / 1024.0)   # the last board averages 52 against ~75 for the rest: it read as a black
#                                              band (a gap) on the back boards, so no face uses it
# boards 7, 9, 10 average ~65: fine as a single drawer front, but on the wide boards they read as shadow bands
DARKISH = [(515 / 1024.0, 588 / 1024.0), (660 / 1024.0, 810 / 1024.0), DARK_BOARD]


def _hits_dark(u0, u1, spans=(DARK_BOARD,)):
    return any(u0 < b + s and u1 > a + s for a, b in spans for s in (-1.0, 0.0, 1.0))
BAND = {WOOD: (0.0, 1.0), INNER: (0.0, 1.0), RAW: (0.0, 1.0)}
_PALE = {}


def _pale_sat(mat):
    """Summed-area table of the texture's pale scratch marks, tiled 2 x 2 for wrap-around. The marks separate cleanly:
    1.51 % of the pixels have an RGB mean above 95, and still 1.51 % above 105 (the wood itself stays below)."""
    if mat in _PALE:
        return _PALE[mat]
    sat = None
    try:
        import numpy as np
        from PIL import Image
        png = os.path.join(TEXPNG, "jp_m_%s%s_co.png" % (mat, WEAR[mat]))
        a = np.asarray(Image.open(png).convert("RGB"), dtype=float).mean(2)
        pale = (a > 100.0).astype(np.int64)
        big = np.tile(pale, (2, 2))
        sat = np.zeros((big.shape[0] + 1, big.shape[1] + 1), dtype=np.int64)
        sat[1:, 1:] = big.cumsum(0).cumsum(1)
    except Exception:  # noqa: BLE001  (no numpy / PIL: fall back to random offsets)
        sat = None
    _PALE[mat] = sat
    return sat


def _pale_count(sat, u0, u1, v0, v1):
    """Pale pixels in the UV rectangle (texture units, any offset; spans up to one tile)."""
    n = 1024
    x0 = int((u0 % 1.0) * n)
    y0 = int((v0 % 1.0) * n)
    x1 = min(x0 + max(1, int((u1 - u0) * n)), 2 * n)
    y1 = min(y0 + max(1, int((v1 - v0) * n)), 2 * n)
    return int(sat[y1, x1] - sat[y0, x1] - sat[y1, x0] + sat[y0, x0])

# ------------------------------------------------------------------------------------------------ dimensions
T = 0.020        # carcass boards (the front frame reads 2 cm)
TB = 0.012       # back panel
REC = 0.004      # closed drawer fronts sit 4 mm behind the frame face (shadow line)
TF = 0.020       # drawer front board
TS = 0.012       # drawer sides and back
TBOT = 0.010     # drawer bottom (the dropped drawer's loot rests on it)
G = 0.002        # gap drawer front <-> frame
DEP = 0.400      # drawer depth incl. the front board
SIDE_DROP = 0.012  # drawer sides are this much lower than the front board

LOWER = dict(name="lower", x0=-0.500, x1=0.500, y0=0.00, y1=0.50, zf=0.225, zb=-0.225,
             rows=[(0.020, 0.240, 1), (0.260, 0.480, 1)])
# the upper part is 4 mm smaller at the front and sides: the step shows the two stacked boxes (kasane-dansu)
UPPER = dict(name="upper", x0=-0.496, x1=0.496, y0=0.50, y1=1.00, zf=0.221, zb=-0.225,
             rows=[(0.520, 0.790, 1), (0.810, 0.980, 2)])
PARTS = (LOWER, UPPER)

# state B: drawer -> ("pull", metres) | ("drop", None) | ("shut", None)
RANSACK = {"U1_xneg": ("pull", 0.20),    # small top drawer on the chest's left (viewer's right)
           "U1_xpos": ("shut", None),
           "U2": ("drop", None),         # the wide lock drawer: the looters' target, now on the floor
           "L1": ("pull", 0.18),
           "L2": ("pull", 0.05)}
DROP_POS = (0.03, 0.700)                 # (x, z) of the dropped drawer's bottom centre on the floor
DROP_YAW = -8.0                          # degrees (core.rot_y convention)
FRONT_ZONE = {"x": [-0.55, 0.55], "z": [0.225, 1.125]}   # 0.90 m in front: kept clear by the decorator

MASS = 45.0      # kg (an empty two-part isho-dansu, assumed)

ROLES = ("right", "left", "top", "bottom", "front", "back")
NRM = {"right": (1.0, 0.0, 0.0), "left": (-1.0, 0.0, 0.0), "top": (0.0, 1.0, 0.0), "bottom": (0.0, -1.0, 0.0),
       "front": (0.0, 0.0, 1.0), "back": (0.0, 0.0, -1.0)}
AXIS = {"x": (1.0, 0.0, 0.0), "y": (0.0, 1.0, 0.0), "z": (0.0, 0.0, 1.0)}


# ------------------------------------------------------------------------------------------------ primitives
def box_quads(x0, x1, y0, y1, z0, z1):
    return {"right": [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
            "left": [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)],
            "top": [(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)],
            "bottom": [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
            "front": [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
            "back": [(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)]}


_BOARD_PICK = {}     # face key -> (b0, b1, v0): the same drawer front keeps its board in every LOD and both states
_BOARD_USES = {}     # board index -> how many fronts use it (spread the fronts over different boards)


def wood_uv(pts, n, grain, mat, rng, board=False, key=None):
    """UV with the grain along v. board=True (drawer fronts): the face's across-grain extent is fitted into ONE
    texture board. Offsets are chosen to hold the fewest pale scratch marks (the _w2 'pale edge wear'), so a few
    remain but no face is covered in them."""
    g = AXIS[grain]
    if abs(core.dot(g, n)) > 0.5:                      # end grain: run the grain along the face's longer side
        cand = [a for a in AXIS.values() if abs(core.dot(a, n)) < 0.5]
        ext = [max(core.dot(p, a) for p in pts) - min(core.dot(p, a) for p in pts) for a in cand]
        g = cand[0] if ext[0] >= ext[1] else cand[1]
    a = [ax for ax in AXIS.values() if abs(core.dot(ax, n)) < 0.5 and abs(core.dot(ax, g)) < 0.5][0]
    us = [core.dot(p, a) / TILE for p in pts]
    vs = [core.dot(p, g) / TILE for p in pts]
    umin, vmin = min(us), min(vs)
    uspan, vspan = max(us) - umin, max(vs) - vmin
    sat = _pale_sat(mat) if mat == WOOD else None
    if board and mat in (WOOD, INNER):
        if key in _BOARD_PICK:
            b0, b1, v0 = _BOARD_PICK[key]
        else:
            cands = []
            for k in range(len(JOINTS_PX) - 2):         # the last (dark) board is never used
                b0, b1 = (JOINTS_PX[k] + 4) / 1024.0, (JOINTS_PX[k + 1] - 4) / 1024.0
                for j in range(32):
                    v0 = j / 32.0
                    pc = _pale_count(sat, b0, b1, v0, v0 + vspan) if sat is not None else 0
                    # a short scratch (< 40 px) is welcome wear; a board already used by another front costs more
                    cands.append((max(0, pc - 40) + 150 * _BOARD_USES.get(k, 0), rng.random(), k, b0, b1, v0))
            _, _, k, b0, b1, v0 = min(cands)
            _BOARD_USES[k] = _BOARD_USES.get(k, 0) + 1
            if key:
                _BOARD_PICK[key] = (b0, b1, v0)
        s = (b1 - b0) / uspan if uspan > 1e-9 else 1.0
        return [(b0 + (u - umin) * s, v0 + (v - vmin)) for u, v in zip(us, vs)]
    if sat is not None:
        cands = []
        for i in range(64):
            u0 = i / 64.0
            dark = 100000 if (mat == WOOD and _hits_dark(u0, u0 + uspan, DARKISH)) else 0
            for j in range(32):
                v0 = j / 32.0
                cands.append((dark + _pale_count(sat, u0, u0 + uspan, v0, v0 + vspan), rng.random(), u0, v0))
        _, _, u0, v0 = min(cands)
    else:
        u0, v0 = rng.random(), rng.random()
    return [(u0 + (u - umin), v0 + (v - vmin)) for u, v in zip(us, vs)]


def vbox(x0, x1, y0, y1, z0, z1, mats, grain="x", skip=(), vis=(1,), rng=None, name="", board=()):
    """Visual box as an open sheet: only the faces not in `skip`. mats: key or {role: key, 'default': key}.
    board: roles whose face is fitted into one texture board (drawer fronts)."""
    q = box_quads(min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1))
    quads, normals, uvs, fmats = [], [], [], []
    rng = rng or core.rng_for(name or "%.4f%.4f%.4f" % (x0, y0, z0))
    for role in ROLES:
        if role in skip:
            continue
        m = mats if isinstance(mats, str) else mats.get(role, mats.get("default"))
        quads.append(q[role])
        normals.append(NRM[role])
        fmats.append(m)
        uvs.append(None if m == IRON else wood_uv(q[role], NRM[role], grain, m, rng, board=role in board,
                                                  key=(name + role) if name else None))
    if not quads:
        return None
    return _sheet(quads, normals, fmats, uvs, vis)


def _sheet(quads, normals, fmats, uvs, vis):
    s = core.Solid([p for q in quads for p in q], [], "x", vis=vis, normals=normals)
    k = 0
    s.faces = []
    for q in quads:
        s.faces.append(list(range(k, k + len(q))))
        k += len(q)
    s.mats = {"default": fmats[0]}
    s.fm, s.fuv, s.fn = [], [], []
    for fi, q in enumerate(quads):
        n = s._outward(fi)
        s.fn.append(n)
        s.fm.append(fmats[fi])
        core.mat_info(fmats[fi])
        s.fuv.append(uvs[fi] if uvs[fi] is not None else core.face_uvs(s, fi, n, fmats[fi]))
    # split n-gons (> 4 points) into quad fans like Solid.finalize
    if any(len(f) > 4 for f in s.faces):
        nf, nfm, nfuv, nfn = [], [], [], []
        for f, m, uv, n in zip(s.faces, s.fm, s.fuv, s.fn):
            if len(f) <= 4:
                nf.append(f); nfm.append(m); nfuv.append(uv); nfn.append(n)
                continue
            j = 1
            while j < len(f) - 1:
                idx = [0, j, j + 1, j + 2] if j + 2 < len(f) else [0, j, j + 1]
                nf.append([f[i] for i in idx]); nfm.append(m); nfuv.append([uv[i] for i in idx]); nfn.append(n)
                j += len(idx) - 2
        s.faces, s.fm, s.fuv, s.fn = nf, nfm, nfuv, nfn
    s.normals = s.fn
    return s


def iron_disc(cx, cy, z0, r, n, thick, vis=(1,), phase=None):
    """Round iron plate on a front face (+z): the n-gon face and its rim; no back (it lies on the wood)."""
    ph = math.pi / n if phase is None else phase
    ring = [(cx + r * math.cos(ph + 2 * math.pi * k / n), cy + r * math.sin(ph + 2 * math.pi * k / n)) for k in range(n)]
    z1 = z0 + thick
    quads = [[(x, y, z1) for x, y in ring]]
    normals = [(0.0, 0.0, 1.0)]
    for k in range(n):
        a, b = ring[k], ring[(k + 1) % n]
        quads.append([(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)])
        mx, my = (a[0] + b[0]) / 2 - cx, (a[1] + b[1]) / 2 - cy
        normals.append(core.norm((mx, my, 0.0)))
    return _sheet(quads, normals, [IRON] * len(quads), [None] * len(quads), vis)


def iron_ring(cx, cy, z0, r_out, r_in, depth, n=8, vis=(1,)):
    """A pull ring lying flat against the drawer front (plane z0..z0+depth): outer, inner and front faces."""
    quads, normals = [], []
    z1 = z0 + depth
    for k in range(n):
        a0 = 2 * math.pi * k / n + math.pi / n
        a1 = 2 * math.pi * (k + 1) / n + math.pi / n
        o0 = (cx + r_out * math.cos(a0), cy + r_out * math.sin(a0))
        o1 = (cx + r_out * math.cos(a1), cy + r_out * math.sin(a1))
        i0 = (cx + r_in * math.cos(a0), cy + r_in * math.sin(a0))
        i1 = (cx + r_in * math.cos(a1), cy + r_in * math.sin(a1))
        am = (a0 + a1) / 2
        quads.append([(o0[0], o0[1], z0), (o1[0], o1[1], z0), (o1[0], o1[1], z1), (o0[0], o0[1], z1)])
        normals.append((math.cos(am), math.sin(am), 0.0))
        quads.append([(i0[0], i0[1], z0), (i1[0], i1[1], z0), (i1[0], i1[1], z1), (i0[0], i0[1], z1)])
        normals.append((-math.cos(am), -math.sin(am), 0.0))
        quads.append([(o0[0], o0[1], z1), (o1[0], o1[1], z1), (i1[0], i1[1], z1), (i0[0], i0[1], z1)])
        normals.append((0.0, 0.0, 1.0))
    return _sheet(quads, normals, [IRON] * len(quads), [None] * len(quads), vis)


def quad_front(x0, x1, y0, y1, z, mat, vis, rng=None, name=""):
    """One front-facing (+z) quad (far-LOD fittings, slot shadows, keyholes)."""
    return vbox(x0, x1, y0, y1, z - 0.001, z, mat, skip=("right", "left", "top", "bottom", "back"), vis=vis,
                rng=rng, name=name)


def coll_box(x0, x1, y0, y1, z0, z1):
    """Closed convex component for Geometry, View Geometry and Fire Geometry (wood penetration)."""
    return core.box(x0, x1, y0, y1, z0, z1, WOOD, vis=(), geo=True, view=True, fire="wood")


# ------------------------------------------------------------------------------------------------ fittings
def pull(cx, cy, zp, vis=(1,)):
    """Iron ring pull (kan) on a drawer front at z = zp: octagonal back plate, a lug, the ring hanging down."""
    out = []
    pc = cy + 0.012
    if 1 in vis:
        out.append(iron_disc(cx, pc, zp, 0.030, 8, 0.0025, vis=(1,)))
        # the staple (lug) that holds the ring's top, standing proud of the ring
        out.append(vbox(cx - 0.0045, cx + 0.0045, pc + 0.003, pc + 0.019, zp + 0.0025, zp + 0.0105, IRON,
                        skip=("back",), vis=(1,)))
        out.append(iron_ring(cx, pc - 0.016, zp + 0.0025, 0.030, 0.0235, 0.005, n=8, vis=(1,)))
    if 2 in vis:
        out.append(vbox(cx - 0.030, cx + 0.030, pc - 0.046, pc + 0.030, zp, zp + 0.004, IRON, skip=("back",),
                        vis=(2,)))
    if 3 in vis:
        out.append(quad_front(cx - 0.028, cx + 0.028, pc - 0.044, pc + 0.028, zp + 0.003, IRON, (3,)))
    return out


def lock_plate(cx, cy, zp, vis=(1,)):
    """Round lock plate (jomae) with a dark keyhole slot, at the centre of the wide drawers."""
    out = []
    if 1 in vis:
        out.append(iron_disc(cx, cy, zp, 0.045, 12, 0.003, vis=(1,)))
        out.append(quad_front(cx - 0.004, cx + 0.004, cy - 0.016, cy + 0.006, zp + 0.004, INNER, (1,)))
    if 2 in vis:
        out.append(iron_disc(cx, cy, zp, 0.045, 6, 0.003, vis=(2,), phase=0.0))
    if 3 in vis:
        out.append(quad_front(cx - 0.038, cx + 0.038, cy - 0.038, cy + 0.038, zp + 0.003, IRON, (3,)))
    return out


def corner_fittings(P, lod):
    """Iron corner plates (sumi-kanagu) wrapping the four front corners of one part; the upper part's top corners
    also get a plate on the top. Res 1: 2 mm plates; Res 2: single quads."""
    out = []
    S, TI = 0.055, 0.002
    x0, x1, y0, y1, zf = P["x0"], P["x1"], P["y0"], P["y1"], P["zf"]
    for sx in (-1, 1):
        xe = x1 if sx > 0 else x0
        for sy in (-1, 1):
            ya, yb = (y1 - S, y1) if sy > 0 else (y0, y0 + S)
            xa, xb = sorted((xe - sx * S, xe + sx * TI))
            sa, sb = sorted((xe, xe + sx * TI))
            top = sy > 0 and P is UPPER
            if lod == 1:
                sk_f = ["back"] + (["bottom"] if (sy < 0 and P is LOWER) else [])
                out.append(vbox(xa, xb, ya, yb, zf, zf + TI, IRON, skip=sk_f, vis=(1,)))
                sk_s = ["left" if sx > 0 else "right", "front"] + (["bottom"] if (sy < 0 and P is LOWER) else [])
                out.append(vbox(sa, sb, ya, yb, zf - S, zf, IRON, skip=sk_s, vis=(1,)))
                if top:
                    out.append(vbox(xa, xb, y1, y1 + TI, zf - S, zf + TI, IRON, skip=("bottom",), vis=(1,)))
            else:
                out.append(quad_front(xa, xb, ya, yb, zf + TI, IRON, (2,)))
                side = vbox(sa, sb, ya, yb, zf - S, zf, IRON, vis=(2,),
                            skip=("left" if sx > 0 else "right", "top", "bottom", "front", "back"))
                out.append(side)
                if top:
                    out.append(vbox(xa, xb, y1, y1 + TI, zf - S, zf + TI, IRON, vis=(2,),
                                    skip=("left", "right", "bottom", "front", "back")))
    return out


def side_handles(P, lod):
    """Carrying handles (sao-kanagu) on both sides of one part: a plate and a U bail hanging flat against the side."""
    out = []
    yc = P["y1"] - 0.075
    zc = (P["zf"] + P["zb"]) / 2
    for sx in (-1, 1):
        xe = P["x1"] if sx > 0 else P["x0"]
        inner = "left" if sx > 0 else "right"
        pa, pb = sorted((xe, xe + sx * 0.003))
        ba, bb = sorted((xe + sx * 0.003, xe + sx * 0.009))
        if lod == 1:
            out.append(vbox(pa, pb, yc - 0.020, yc + 0.020, zc - 0.075, zc + 0.075, IRON, skip=(inner,), vis=(1,)))
            for zl in (-0.060, 0.060):     # the bail's legs, from the plate down to the grip
                out.append(vbox(ba, bb, yc - 0.055, yc + 0.006, zc + zl - 0.003, zc + zl + 0.003, IRON,
                                skip=(inner, "bottom"), vis=(1,)))
            out.append(vbox(ba, bb, yc - 0.061, yc - 0.055, zc - 0.063, zc + 0.063, IRON, skip=(inner,), vis=(1,)))
        else:
            out.append(vbox(pa, pb, yc - 0.020, yc + 0.020, zc - 0.075, zc + 0.075, IRON, vis=(2,),
                            skip=(inner, "top", "bottom", "front", "back")))
            out.append(vbox(ba, bb, yc - 0.061, yc - 0.052, zc - 0.063, zc + 0.063, IRON, skip=(inner,), vis=(2,)))
    return out


# ------------------------------------------------------------------------------------------------ carcass
def carcass(P):
    """Res 1 carcass of one part from boards: the frame is the boards' front edges; inside faces are INNER."""
    x0, x1, y0, y1, zf, zb = P["x0"], P["x1"], P["y0"], P["y1"], P["zf"], P["zb"]
    nm = P["name"]
    out = []
    # top board (full width); the lower part's top shows only as the 4 mm ledge under the upper part
    out.append(vbox(x0, x1, y1 - T, y1, zb, zf, {"default": WOOD, "bottom": INNER}, grain="x", name=nm + "top"))
    # bottom board: its underside is on the floor / on the lower part
    out.append(vbox(x0, x1, y0, y0 + T, zb, zf, {"default": WOOD, "top": INNER}, grain="x", skip=("bottom",),
                    name=nm + "bot"))
    # side boards between top and bottom (vertical grain; the finger-jointed corners of i01)
    out.append(vbox(x0, x0 + T, y0 + T, y1 - T, zb, zf, {"default": WOOD, "right": INNER}, grain="y",
                    skip=("top", "bottom"), name=nm + "sl"))
    out.append(vbox(x1 - T, x1, y0 + T, y1 - T, zb, zf, {"default": WOOD, "left": INNER}, grain="y",
                    skip=("top", "bottom"), name=nm + "sr"))
    # back panel between the boards
    out.append(vbox(x0 + T, x1 - T, y0 + T, y1 - T, zb, zb + TB, {"default": WOOD, "front": INNER}, grain="x",
                    skip=("left", "right", "top", "bottom"), name=nm + "back"))
    # rails (dust boards) between the drawer rows, and the vertical divider of a two-drawer row
    rows = P["rows"]
    for k in range(len(rows) - 1):
        ya, yb = rows[k][1], rows[k + 1][0]
        out.append(vbox(x0 + T, x1 - T, ya, yb, zb + TB, zf, {"default": INNER, "front": WOOD}, grain="x",
                        skip=("left", "right", "back"), name=nm + "rail%d" % k))
    for (oy0, oy1, nc) in rows:
        if nc == 2:
            out.append(vbox(-0.010, 0.010, oy0, oy1, zb + TB, zf, {"default": INNER, "front": WOOD}, grain="y",
                            skip=("top", "bottom", "back"), name=nm + "div"))
    return out


def openings(P):
    """[(drawer id, x0, x1, y0, y1)] of one part (the frame's clear openings)."""
    x0, x1 = P["x0"] + T, P["x1"] - T
    out = []
    tag = "U" if P is UPPER else "L"
    n = len(P["rows"])
    for k, (oy0, oy1, nc) in enumerate(P["rows"]):
        rid = "%s%d" % (tag, n - k)          # row 1 = the top row of the part
        if nc == 1:
            out.append((rid, x0, x1, oy0, oy1))
        else:
            out.append((rid + "_xneg", x0, -0.010, oy0, oy1))
            out.append((rid + "_xpos", 0.010, x1, oy0, oy1))
    return out


# ------------------------------------------------------------------------------------------------ drawers
def drawer_fittings(did, fx0, fx1, fy0, fy1, zp, vis):
    cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
    out = []
    if fx1 - fx0 > 0.6:                          # wide drawer: two pulls and the lock plate
        for dx in (-0.245, 0.245):
            out += pull(cx + dx, cy, zp, vis)
        out += lock_plate(cx, cy, zp, vis)
    else:
        out += pull(cx, cy, zp, vis)
    return out


def drawer_front_shut(did, ox0, ox1, oy0, oy1, zf):
    """State A (and the shut drawer of B): only the front board and its fittings."""
    fx0, fx1, fy0, fy1 = ox0 + G, ox1 - G, oy0 + G, oy1 - G
    zp = zf - REC
    out = [vbox(fx0, fx1, fy0, fy1, zp - TF, zp, WOOD, grain="x", skip=("back",), name="front" + did,
                board=("front",))]
    out += drawer_fittings(did, fx0, fx1, fy0, fy1, zp, (1,))
    return out


def drawer_body(did, ox0, ox1, oy0, oy1, zf, on_floor=False):
    """A whole open-topped drawer (front board, sides, back, bottom, fittings) in its SHUT position."""
    fx0, fx1, fy0, fy1 = ox0 + G, ox1 - G, oy0 + G, oy1 - G
    zp = zf - REC                    # front face
    zi = zp - TF                     # inside face of the front board
    ze = zp - DEP                    # back end of the drawer
    ys1 = fy1 - SIDE_DROP            # top edge of sides and back
    fl = ("bottom",) if on_floor else ()
    out = [vbox(fx0, fx1, fy0, fy1, zi, zp, {"default": WOOD, "back": RAW}, grain="x", skip=fl, name="front" + did,
                board=("front",))]
    out.append(vbox(fx0, fx0 + TS, fy0, ys1, ze, zi, RAW, grain="z", skip=("front",) + fl, name="dsl" + did))
    out.append(vbox(fx1 - TS, fx1, fy0, ys1, ze, zi, RAW, grain="z", skip=("front",) + fl, name="dsr" + did))
    out.append(vbox(fx0 + TS, fx1 - TS, fy0, ys1, ze, ze + TS, RAW, grain="x", skip=("left", "right") + fl,
                    name="db" + did))
    out.append(vbox(fx0 + TS, fx1 - TS, fy0, fy0 + TBOT, ze + TS, zi, RAW, grain="x",
                    skip=("left", "right", "front", "back") + fl, name="dbot" + did))
    out += drawer_fittings(did, fx0, fx1, fy0, fy1, zp, (1,))
    return out


def drawer_box_far(did, ox0, ox1, oy0, oy1, zf, lods, rec, on_floor=False):
    """Far-LOD drawer (Res 2 / 3): one box, the top face showing the pale inside."""
    fx0, fx1, fy0, fy1 = ox0 + G, ox1 - G, oy0 + G, oy1 - G
    zp = zf - rec
    ze = zp - DEP
    sk = ("back", "bottom") if on_floor else ("back",)
    out = [vbox(fx0, fx1, fy0, fy1 - SIDE_DROP, ze, zp, {"default": WOOD, "top": RAW}, grain="x", skip=sk, vis=lods,
                name="front" + did, board=("front",))]
    for k in lods:
        out += drawer_fittings(did, fx0, fx1, fy0, fy1, zp, (k,))
    return out


def moved(solids, dz=0.0, yaw=0.0, t=(0.0, 0.0, 0.0)):
    out = []
    for s in solids:
        if s is None:
            continue
        s.finalize()
        if yaw:
            out.append(s.transformed(yaw, t))
        else:
            out.append(s.transformed(0.0, (t[0], t[1], t[2] + dz)))
    return out


def dropped_local(did, ox0, ox1, oy0, oy1, zf):
    """The dropped drawer's solids moved so its bottom centre sits at the origin (shut frame -> local frame)."""
    fx0, fx1, fy0 = ox0 + G, ox1 - G, oy0 + G
    zp = zf - REC
    cx, cz = (fx0 + fx1) / 2, zp - DEP / 2
    return (-cx, -fy0, -cz)


# ------------------------------------------------------------------------------------------------ far LODs
def far_carcass(P, lod, slots_dark=()):
    """Res 2: one box per part with the drawer plane 6 mm behind thin frame strips; Res 3: one flush box."""
    x0, x1, y0, y1, zf, zb = P["x0"], P["x1"], P["y0"], P["y1"], P["zf"], P["zb"]
    nm = P["name"] + "far%d" % lod
    out = []
    if lod == 3:
        out.append(vbox(x0, x1, y0, y1, zb, zf, WOOD, grain="x", skip=("bottom",), vis=(3,), name=nm))
        return out
    r2 = 0.006
    out.append(vbox(x0, x1, y0, y1, zb, zf - r2, WOOD, grain="x", skip=("bottom",), vis=(2,), name=nm))
    zs = zf - r2
    strips = [(x0, x1, y1 - T, y1, ("back",)),                           # top rail (its top/ends continue the box)
              (x0, x1, y0, y0 + T, ("back", "bottom")),                  # bottom rail
              (x0, x0 + T, y0 + T, y1 - T, ("back", "top", "bottom")),   # stiles (outer face continues the side)
              (x1 - T, x1, y0 + T, y1 - T, ("back", "top", "bottom"))]
    rows = P["rows"]
    for k in range(len(rows) - 1):
        strips.append((x0 + T, x1 - T, rows[k][1], rows[k + 1][0], ("back", "left", "right")))
    for (oy0, oy1, nc) in rows:
        if nc == 2:
            strips.append((-0.010, 0.010, oy0, oy1, ("back", "top", "bottom")))
    for i, (a, b, c, d, sk) in enumerate(strips):
        out.append(vbox(a, b, c, d, zs, zf, WOOD, grain="x" if (b - a) > (d - c) else "y", skip=sk, vis=(2,),
                        name=nm + "s%d" % i))
    for (ox0, ox1, oy0, oy1) in slots_dark:
        out.append(quad_front(ox0, ox1, oy0, oy1, zf - 0.002, INNER, (2,), name=nm + "slot"))
    return out


# ------------------------------------------------------------------------------------------------ the model
def model(state="A"):
    """-> (Part, info). state 'A' = intact, 'B' = ransacked."""
    assert state in ("A", "B")
    part = core.Part("jp_f_tansu", "" if state == "A" else "_ransacked")
    part.wear = "_w1"
    part.wear_by_mat = dict(WEAR)
    sol = []
    info = {"state": state, "drawers": {}, "loot": [], "components": []}
    ops = {}
    for P in PARTS:
        for op in openings(P):
            ops[op[0]] = (P,) + op[1:]
    # ---- Res 1
    for P in PARTS:
        sol += carcass(P)
        sol += corner_fittings(P, 1)
        sol += side_handles(P, 1)
    drop_solids_local = []
    for did, (P, ox0, ox1, oy0, oy1) in sorted(ops.items()):
        how, amt = ("shut", None) if state == "A" else RANSACK[did]
        info["drawers"][did] = {"state": how, "pull_m": amt, "opening": [ox0, ox1, oy0, oy1], "part": P["name"]}
        if how == "shut":
            sol += drawer_front_shut(did, ox0, ox1, oy0, oy1, P["zf"])
        elif how == "pull":
            sol += moved(drawer_body(did, ox0, ox1, oy0, oy1, P["zf"]), dz=amt)
        else:
            t = dropped_local(did, ox0, ox1, oy0, oy1, P["zf"])
            loc = moved(drawer_body(did, ox0, ox1, oy0, oy1, P["zf"], on_floor=True), t=t)
            loc2 = moved(drawer_box_far(did, ox0, ox1, oy0, oy1, P["zf"], (2,), 0.006, on_floor=True),
                         t=(t[0], t[1], t[2] + 0.002))
            loc3 = moved(drawer_box_far(did, ox0, ox1, oy0, oy1, P["zf"], (3,), 0.0, on_floor=True),
                         t=(t[0], t[1], t[2] - 0.004))
            drop_solids_local = (loc + loc2 + loc3, did, ox0, ox1, oy0, oy1, P)
    # ---- Res 2 / 3
    for lod in (2, 3):
        for P in PARTS:
            dark = []
            for did, (PP, ox0, ox1, oy0, oy1) in sorted(ops.items()):
                if PP is P and state == "B" and RANSACK[did][0] in ("drop", "pull"):
                    dark.append((ox0, ox1, oy0, oy1))
            if lod == 2:
                sol += far_carcass(P, 2, slots_dark=dark)
                sol += corner_fittings(P, 2)
                sol += side_handles(P, 2)
            else:
                sol += far_carcass(P, 3)
                for (ox0, ox1, oy0, oy1) in dark:
                    sol.append(quad_front(ox0, ox1, oy0, oy1, P["zf"] + 0.002, INNER, (3,), name="slot3"))
        for did, (P, ox0, ox1, oy0, oy1) in sorted(ops.items()):
            how, amt = ("shut", None) if state == "A" else RANSACK[did]
            rec = 0.006 if lod == 2 else 0.0
            if how == "shut":
                fx0, fx1, fy0, fy1 = ox0 + G, ox1 - G, oy0 + G, oy1 - G
                sol += drawer_fittings(did, fx0, fx1, fy0, fy1, P["zf"] - rec, (lod,))
            elif how == "pull":
                sol += moved(drawer_box_far(did, ox0, ox1, oy0, oy1, P["zf"], (lod,), rec), dz=amt)
    # ---- the dropped drawer: local frame -> floor, yawed
    if drop_solids_local:
        loc, did, ox0, ox1, oy0, oy1, P = drop_solids_local
        tt = (DROP_POS[0], 0.0, DROP_POS[1])
        sol += moved(loc, yaw=DROP_YAW, t=tt)
        fw = (ox1 - G) - (ox0 + G)
        info["dropped"] = {"drawer": did, "pos": [DROP_POS[0], 0.0, DROP_POS[1]], "yaw_deg": DROP_YAW,
                           "outer_m": [round(fw, 3), round(DEP, 3), round(oy1 - oy0 - 2 * G, 3)]}
    for s in sol:
        if s is not None:
            part.add(s)
    # ---- Geometry / View / Fire: closed convex boxes
    comps = [("body", coll_box(-0.500, 0.500, 0.0, 1.000, -0.225, 0.225))]
    if state == "B":
        for did, (P, ox0, ox1, oy0, oy1) in sorted(ops.items()):
            how, amt = RANSACK[did]
            if how == "pull":
                zp = P["zf"] - REC + amt
                comps.append(("pulled_" + did, coll_box(ox0 + G, ox1 - G, oy0 + G, oy1 - G, P["zf"], zp)))
        loc, did, ox0, ox1, oy0, oy1, P = drop_solids_local
        fw = (ox1 - G) - (ox0 + G)
        h = oy1 - oy0 - 2 * G - SIDE_DROP
        hx, hz = fw / 2, DEP / 2
        # walls 3 cm thick (inward) so nothing tunnels; the bottom slab carries the loot
        local = [("drop_bottom", (-hx, hx, 0.0, TBOT, -hz, hz)),
                 ("drop_front", (-hx, hx, 0.0, h + SIDE_DROP, hz - 0.030, hz)),
                 ("drop_back", (-hx, hx, TBOT, h, -hz, -hz + 0.030)),
                 ("drop_left", (-hx, -hx + 0.030, TBOT, h, -hz + 0.030, hz - 0.030)),
                 ("drop_right", (hx - 0.030, hx, TBOT, h, -hz + 0.030, hz - 0.030))]
        tt = (DROP_POS[0], 0.0, DROP_POS[1])
        for nm, b in local:
            c = coll_box(*b)
            c.finalize()
            comps.append((nm, c.transformed(DROP_YAW, tt)))
    for nm, c in comps:
        part.add(c)
        info["components"].append(nm)
    # ---- loot (BUILD_LIST row 26): the top at 1.00, 2 points (range 0.2); B: 1 point in the dropped drawer
    info["loot"] = [{"name": "loot_top_1", "model": [-0.25, 1.000, 0.0], "range": 0.20, "surface": "top"},
                    {"name": "loot_top_2", "model": [0.25, 1.000, 0.0], "range": 0.20, "surface": "top"}]
    if state == "B":
        info["loot"].append({"name": "loot_drawer", "model": [DROP_POS[0], TBOT, DROP_POS[1]], "range": 0.15,
                             "surface": "dropped drawer bottom (floor)"})
    # no Memory LOD: BUILD_LIST (Q5, binding item 2) gives props "Res 1-2 (3 for furniture), Geometry, View, Fire;
    # no Memory", like vanilla case_d / case_a. The loot points live in the sidecar (loot_surfaces).
    return part, info


def lods(state):
    part, info = model(state)
    L = part.lods(geo_props={"autocenter": "0"}, mass=MASS)
    geo = mlod.find_lod(L, mlod.LOD_GEOMETRY)
    # mass by component volume (Part.lods spreads it evenly over the points)
    vols = {}
    for name, (pw, fs) in geo.selections.items():
        if name.startswith("Component"):
            vols[name] = (poly_volume(geo, fs), pw)
    tot = sum(v for v, _ in vols.values())
    m = [0.0] * len(geo.points)
    for name, (v, pw) in vols.items():
        for pi in pw:
            m[pi] = MASS * v / tot / len(pw)
    geo.mass = m
    return part, info, L


def poly_volume(lod, faces):
    pts = [lod.points[v[0]] for fi in faces for v in lod.faces[fi][0]]
    c = tuple(sum(p[k] for p in pts) / len(pts) for k in range(3))
    vol = 0.0
    for fi in faces:
        fp = [lod.points[v[0]] for v in lod.faces[fi][0]]
        for k in range(1, len(fp) - 1):
            a, b, d = core.sub(fp[0], c), core.sub(fp[k], c), core.sub(fp[k + 1], c)
            vol += abs(core.dot(a, core.cross(b, d))) / 6.0
    return vol


if __name__ == "__main__":
    for st in ("A", "B"):
        p, inf, L = lods(st)
        print(st, {mlod.lod_name(l.resolution): len(l.faces) for l in L},
              "tris R1 =", sum(len(f[0]) - 2 for f in L[0].faces))
