#!/usr/bin/env python3
r"""build.py - effort test (LEVEL medium): jp_f_tansu (isho-dansu), intact + ransacked.

  python build.py [--no-binarize] [--no-pack]

1. MLOD p3ds -> out/ and src/JP/effort_test/medium/ (jp_efftest_medium_tansu[_ransacked].p3d)
2. config.cpp (CfgPatches JP_EffTest_medium, two HouseNoDestruct static classes) -> CfgConvert
3. binarize.exe (cwd P:\) -> ODOL replaces the MLOD in src
4. pack src/JP/effort_test/medium -> ..\@Japan\addons\jp_efftest_medium.pbo (prefix JP\effort_test\medium)
5. sidecar jp_f_tansu.json (dims, materials, loot_surfaces, faces)
Frame: origin = base centre on the floor, x right, y up, +z = the front (drawers). autocenter=0.
Never touches the server, the game or any GUI program.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(DEV, ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "tools", "common"))
from jpparts import mlod  # noqa: E402  (read-only import)

LEVEL = "medium"
SRC = os.path.join(DEV, "src", "JP", "effort_test", LEVEL)
OUT = os.path.join(HERE, "out")
TEMP = os.path.join(HERE, "_build")
PBO_OUT = os.path.join(ROOT, "@Japan", "addons", "jp_efftest_%s.pbo" % LEVEL)
PREFIX = "JP\\effort_test\\%s" % LEVEL
TOOLS = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
BINARIZE = os.path.join(TOOLS, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS, "CfgConvert", "CfgConvert.exe")

MATDIR = "JP\\common\\materials\\"
MATS = {  # key -> (texture, rvmat, tile metres)
    "wood": (MATDIR + "wood\\jp_m_wood_street_dark_w1_co.paa", MATDIR + "wood\\jp_m_wood_street_dark_w1.rvmat", 2.0),
    "iron": (MATDIR + "metal\\jp_m_metal_iron_w1_co.paa", MATDIR + "metal\\jp_m_metal_iron_w1.rvmat", 0.5),
}
FIRE_WOOD = "dz\\data\\data\\penetration\\wood.rvmat"

W, D, H = 1.00, 0.45, 0.50        # one box (two stacked -> 1.00 high)
T = 0.018                        # carcass board
BACK = 0.012
INSET = 0.003                    # the upper box is 3 mm smaller all round -> a visible joint
FT = 0.020                       # drawer front thickness
PROUD = 0.002                    # drawer front stands proud of the carcass face
GAP = 0.003                      # drawer front clearance in its opening

# ---------------------------------------------------------------------------------------------------- solids
FACES = {  # name: (corner indices of the unit box, outward normal, the two in-plane axes)
    "-x": ((0, 2, 6, 4), (-1, 0, 0), (2, 1)), "+x": ((1, 5, 7, 3), (1, 0, 0), (2, 1)),
    "-y": ((0, 4, 5, 1), (0, -1, 0), (0, 2)), "+y": ((2, 3, 7, 6), (0, 1, 0), (0, 2)),
    "-z": ((0, 1, 3, 2), (0, 0, -1), (0, 1)), "+z": ((4, 6, 7, 5), (0, 0, 1), (0, 1)),
}


class Solid:
    """A convex hexahedron (8 corners, in the unit-box index order x + 2y + 4z) with per-face uv."""

    def __init__(self, corners, mat, grain, skip=(), uvoff=(0.0, 0.0), tag=""):
        self.c = [tuple(p) for p in corners]
        self.mat, self.grain, self.skip, self.uvoff, self.tag = mat, grain, set(skip), uvoff, tag
        self.local = None       # local (axis-aligned) corners for uv, set by box()

    def faces(self):
        tile = MATS[self.mat][2]
        out = []
        for name, (idx, nrm, (a1, a2)) in FACES.items():
            if name in self.skip:
                continue
            pts = [self.c[i] for i in idx]
            loc = [self.local[i] for i in idx]
            g = "xyz".index(self.grain)
            if g == a1:
                va, ua = a1, a2
            elif g == a2:
                va, ua = a2, a1
            else:
                va, ua = a2, a1
            uvs = [(p[ua] / tile + self.uvoff[0], -p[va] / tile + self.uvoff[1]) for p in loc]
            n = _rot_normal(self, nrm)
            out.append((pts, n, uvs))
        return out


def _rot_normal(s, nrm):
    # outward normal in world space from the solid's actual corners (handles rotated solids)
    c = [sum(p[k] for p in s.c) / 8.0 for k in range(3)]
    idx = [v[0] for v in FACES.values() if v[1] == nrm][0]
    fc = [sum(s.c[i][k] for i in idx) / 4.0 for k in range(3)]
    d = [fc[k] - c[k] for k in range(3)]
    l = math.sqrt(sum(x * x for x in d)) or 1.0
    return tuple(x / l for x in d)


def box(x0, x1, y0, y1, z0, z1, mat="wood", grain="x", skip=(), xf=None, uvoff=None, tag=""):
    loc = [(x1 if i & 1 else x0, y1 if i & 2 else y0, z1 if i & 4 else z0) for i in range(8)]
    wc = [xf(p) for p in loc] if xf else loc
    if uvoff is None:
        h = abs(hash((round(x0, 3), round(y0, 3), round(z0, 3)))) % 997
        uvoff = ((h % 31) / 31.0, (h % 17) / 17.0)
    s = Solid(wc, mat, grain, skip, uvoff, tag)
    s.local = loc
    return s


def bar(p0, p1, size, side, mat="iron", xf=None, ends=False):
    """Square-section bar from p0 to p1; `side` = a vector not parallel to it (orients the section)."""
    d = [p1[k] - p0[k] for k in range(3)]
    L = math.sqrt(sum(x * x for x in d))
    u = [x / L for x in d]
    a = _cross(u, side); a = _norm(a)
    b = _cross(u, a)
    h = size / 2.0
    loc, wc = [], []
    for i in range(8):
        sx = h if i & 1 else -h
        sy = h if i & 2 else -h
        base = p1 if i & 4 else p0
        p = tuple(base[k] + a[k] * sx + b[k] * sy for k in range(3))
        wc.append(xf(p) if xf else p)
        loc.append((sx, sy, (L if i & 4 else 0.0)))
    s = Solid(wc, mat, "z", () if ends else ("-z", "+z"), (0.0, 0.0), "bar")
    s.local = loc
    return s


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(a):
    l = math.sqrt(sum(x * x for x in a)) or 1.0
    return tuple(x / l for x in a)


def yaw_xf(deg, tx, ty, tz):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return lambda p: (c * p[0] + s * p[2] + tx, p[1] + ty, -s * p[0] + c * p[2] + tz)


# ---------------------------------------------------------------------------------------------------- the tansu
def boxes_spec():
    """The two stacked boxes and their drawer openings: [(name, x0, x1, y0, y1, zb, zf, [openings])]."""
    lo = ("lower", -W / 2, W / 2, 0.0, H, -D / 2, D / 2)
    up = ("upper", -W / 2 + INSET, W / 2 - INSET, H, 2 * H - 0.0, -D / 2 + INSET, D / 2 - INSET)
    xa, xb = lo[1] + T, lo[2] - T
    lo_open = [("L1", xa, xb, T, H / 2 - T / 2), ("L2", xa, xb, H / 2 + T / 2, H - T)]
    xa2, xb2 = up[1] + T, up[2] - T
    ym = H + 0.280                 # long drawer / small-drawer row split
    up_open = [("U1", xa2, xb2, H + T, ym - T / 2),
               ("U2", xa2, -T / 2, ym + T / 2, 2 * H - T), ("U3", T / 2, xb2, ym + T / 2, 2 * H - T)]
    return [(lo, lo_open, ("mid",)), (up, up_open, ("vdiv",))]


def carcass(b, openings, lod):
    name, x0, x1, y0, y1, zb, zf = b
    out = []
    if lod == 1:
        out.append(box(x0, x0 + T, y0, y1, zb, zf, grain="z"))                        # sides
        out.append(box(x1 - T, x1, y0, y1, zb, zf, grain="z"))
        out.append(box(x0 + T, x1 - T, y1 - T, y1, zb, zf, grain="x"))                # top
        out.append(box(x0 + T, x1 - T, y0, y0 + T, zb, zf, grain="x"))                # bottom
        out.append(box(x0 + T, x1 - T, y0 + T, y1 - T, zb, zb + BACK, grain="y"))     # back
        ys = sorted({round(o[4], 4) for o in openings} | {round(o[3], 4) for o in openings})
        # full-depth dust boards between drawer rows
        rows = sorted({(round(o[3], 4), round(o[4], 4)) for o in openings})
        for (a0, a1), (b0, b1) in zip(rows, rows[1:]):
            out.append(box(x0 + T, x1 - T, a1, b0, zb + BACK, zf, grain="x"))
        # vertical divider between side-by-side drawers
        tops = [o for o in openings if o[1] > x0 + T + 0.01]
        for o in tops:
            out.append(box(o[1] - T, o[1], o[3], o[4], zb + BACK, zf, grain="y"))
        del ys
    else:
        out.append(box(x0, x1, y0, y1, zb, zf, grain="x"))
    return out


def pull(cx, cy, zf, xf=None, lod=1):
    """Warabite ring pull: an iron back plate and a drooping half-ring bail."""
    out = [box(cx - 0.038, cx + 0.038, cy - 0.022, cy + 0.022, zf, zf + 0.003, "iron", "x", ("-z",), xf)]
    r, zc = 0.034, zf + 0.003 + 0.005
    n = 6 if lod == 1 else 3
    pts = [(cx + r * math.cos(math.pi * i / n), cy - r * math.sin(math.pi * i / n), zc) for i in range(n + 1)]
    for p0, p1 in zip(pts, pts[1:]):
        out.append(bar(p0, p1, 0.009, (0, 0, 1), "iron", xf))
    return out


def drawer(o, pulled, lod, body, xf=None, tag="", full=False):
    """A drawer in opening o = (id, x0, x1, y0, y1), front face flush(+PROUD) at zf0 + pulled."""
    oid, x0, x1, y0, y1, zf0 = o
    dz = pulled
    zfront = zf0 + PROUD + dz
    fx0, fx1, fy0, fy1 = x0 + GAP, x1 - GAP, y0 + GAP, y1 - GAP
    out = []
    if lod >= 2 and full:
        out.append(box(fx0, fx1, fy0, fy1, zfront - FT - 0.39, zfront, grain="x", xf=xf, tag=tag))
    elif lod >= 2 and body and pulled > 0:
        # far LOD: front + exposed body as one block from the carcass face
        out.append(box(fx0, fx1, fy0, fy1, zf0 - 0.01, zfront, grain="x", xf=xf, tag=tag))
    else:
        out.append(box(fx0, fx1, fy0, fy1, zfront - FT, zfront, grain="x", xf=xf, skip=() if body else ("-z",), tag=tag))
    if body and lod == 1:
        zb = zfront - FT - 0.39
        t = 0.012
        out.append(box(fx0 + 0.004, fx0 + 0.004 + t, fy0 + 0.004, fy1 - 0.03, zb, zfront - FT, grain="z", xf=xf))
        out.append(box(fx1 - 0.004 - t, fx1 - 0.004, fy0 + 0.004, fy1 - 0.03, zb, zfront - FT, grain="z", xf=xf))
        out.append(box(fx0 + 0.004 + t, fx1 - 0.004 - t, fy0 + 0.004, fy1 - 0.03, zb, zb + t, grain="x", xf=xf))
        out.append(box(fx0 + 0.004 + t, fx1 - 0.004 - t, fy0 + 0.004, fy0 + 0.014, zb + t, zfront - FT, grain="x",
                       xf=xf))
    if lod <= 2:
        wid = fx1 - fx0
        cy = (fy0 + fy1) / 2 + 0.015
        if wid > 0.6:
            for px in (-0.25, 0.25):
                out += pull(px, cy, zfront, xf, lod)
            if lod == 1 and oid in ("U1", "L2"):   # lock plate (kagami) on the two show drawers
                out.append(box(-0.045, 0.045, cy - 0.04, cy + 0.03, zfront, zfront + 0.002, "iron", "x", ("-z",), xf))
        else:
            out += pull((fx0 + fx1) / 2, cy, zfront, xf, lod)
    return out


def fittings(b, lod):
    """Iron corner plates (front corners) and folding carry handles on both sides."""
    name, x0, x1, y0, y1, zb, zf = b
    out = []
    t, L = 0.0025, 0.085
    if lod == 1:
        for sx, xe in ((-1, x0), (1, x1)):
            for sy, ye in ((-1, y0), (1, y1)):
                if name == "lower" and sy < 0:
                    ya, yb = y0 + 0.012, y0 + L      # clear of the floor
                else:
                    ya, yb = (y0, y0 + L) if sy < 0 else (y1 - L, y1)
                fx0, fx1 = (xe, xe + 0.016) if sx < 0 else (xe - 0.016, xe)
                out.append(box(fx0, fx1, ya, yb, zf, zf + t, "iron", "y", ("-z",)))           # front strip
                sx0, sx1 = (xe - t, xe) if sx < 0 else (xe, xe + t)
                out.append(box(sx0, sx1, ya, yb, zf - L, zf + t, "iron", "y", ("+x",) if sx < 0 else ("-x",)))
                if sy > 0 and name == "upper":                                               # top plate
                    tx0, tx1 = (xe, xe + L) if sx < 0 else (xe - L, xe)
                    out.append(box(tx0, tx1, y1, y1 + t, zf - L, zf + t, "iron", "x", ("-y",)))
    # carry handles: two plates, two legs, a flat bar, near the top of each box's sides
    hy = y1 - 0.11
    for sx, xe in ((-1, x0), (1, x1)):
        xo = xe + sx * 0.003
        if lod == 1:
            for zc in (-0.11, 0.11):
                a, bb = sorted((xe, xo))
                out.append(box(a, bb, hy - 0.03, hy + 0.03, zc - 0.022, zc + 0.022, "iron", "y",
                               ("+x",) if sx < 0 else ("-x",)))
                out.append(bar((xo, hy, zc), (xe + sx * 0.012, hy, zc), 0.010, (0, 1, 0), "iron"))
        out.append(bar((xe + sx * 0.018, hy, -0.125), (xe + sx * 0.018, hy, 0.125), 0.012, (0, 1, 0), "iron",
                       ends=True))
    return out


RANSACK = {"L1": 0.0, "L2": 0.24, "U1": 0.14, "U3": 0.09}      # pulled out (m); U2 lies on the floor
FLOOR = ("U2", -0.16, 0.60, 17.0)                            # drawer id, x, z of its centre, yaw (deg)


def model(state, lod):
    """All visual solids for a state ('intact' / 'ransacked') at resolution lod (1, 2, 3)."""
    sol = []
    body = state == "ransacked"
    for b, openings, _ in boxes_spec():
        zf = b[6]
        sol += carcass(b, openings, lod)
        if lod <= 2:
            sol += fittings(b, lod)
        for o in openings:
            oo = o + (zf,)
            if state == "ransacked" and o[0] == FLOOR[0]:
                continue
            d = RANSACK.get(o[0], 0.0) if state == "ransacked" else 0.0
            if lod == 3 and d == 0:
                continue                                  # far LOD: closed fronts are part of the block
            sol += drawer(oo, d, lod, body)
    if state == "ransacked":
        sol += floor_drawer(lod)
    return sol


def floor_drawer_frame():
    o = [x for b, ops, _ in boxes_spec() for x in ops if x[0] == FLOOR[0]][0]
    zf = boxes_spec()[1][0][6]
    x0, x1, y0, y1 = o[1:]
    cx = (x0 + x1) / 2
    zfront = zf + PROUD
    zc = zfront - (FT + 0.39) / 2
    # local drawer -> centred on origin at floor level, then yaw + move into the front zone
    base = yaw_xf(FLOOR[3], FLOOR[1], 0.0, FLOOR[2])
    xf = lambda p: base((p[0] - cx, p[1] - (y0 + GAP), p[2] - zc))   # noqa: E731
    return o + (zf,), xf


def floor_drawer(lod):
    o, xf = floor_drawer_frame()
    return drawer(o, 0.0, lod, True, xf, "floor_drawer", full=True)


# ---------------------------------------------------------------------------------------------------- LODs
def visual_lod(state, res):
    lod = mlod.Lod(float(res))
    for s in model(state, res):
        tex, mat, _ = MATS[s.mat]
        for pts, n, uvs in s.faces():
            lod.add_flat_face(pts, n, uvs, tex, mat)
    return lod


def hull_boxes(state):
    """Collision boxes (closed, convex): [(corners, mass)]."""
    out = []
    for b, openings, _ in boxes_spec():
        name, x0, x1, y0, y1, zb, zf = b
        out.append((box(x0, x1, y0, y1, zb, zf).c, 22.0))
        if state == "ransacked":
            for o in openings:
                d = RANSACK.get(o[0], 0.0)
                if d > 0.04:
                    out.append((box(o[1] + GAP, o[2] - GAP, o[3] + GAP, o[4] - GAP, zf, zf + PROUD + d).c, 1.5))
    if state == "ransacked":
        o, xf = floor_drawer_frame()
        zfront = o[5] + PROUD
        out.append((box(o[1] + GAP, o[2] - GAP, o[3] + GAP, o[4] - GAP, zfront - FT - 0.39, zfront, xf=xf).c, 2.0))
    return out


QUADS = [v[0] for v in FACES.values()]


def comp_lod(res, state, fire=False, mass=False, props=None):
    lod = mlod.Lod(res)
    masses = []
    for k, (c, m) in enumerate(hull_boxes(state), 1):
        pis, fis = lod.add_closed_solid(c, [list(q) for q in QUADS], "", FIRE_WOOD if fire else "")
        lod.select("Component%02d" % k, {pi: 1.0 for pi in pis}, fis)
        masses += [m / 8.0] * 8
    if mass:
        lod.mass = masses
    for k, v in (props or {}).items():
        lod.properties[k] = v
    return lod


def memory_lod(state):
    lod = mlod.Lod(mlod.LOD_MEMORY)
    pts = {"loot_top_1": (-0.25, 2 * H, 0.0), "loot_top_2": (0.25, 2 * H, 0.0)}
    if state == "ransacked":
        o, xf = floor_drawer_frame()
        zfront = o[5] + PROUD
        pts["loot_drawer"] = xf(((o[1] + o[2]) / 2, o[3] + GAP + 0.014, zfront - FT - 0.195))
    for name, p in pts.items():
        pi = lod.add_point(p)
        lod.select(name, {pi: 1.0})
    return lod, pts


def lods(state):
    out = [visual_lod(state, r) for r in (1, 2, 3)]
    out.append(comp_lod(mlod.LOD_GEOMETRY, state, mass=True,
                        props={"autocenter": "0", "class": "house", "map": "hide", "damage": "no"}))
    mem, pts = memory_lod(state)
    out.append(mem)
    out.append(comp_lod(mlod.LOD_VIEW_GEOMETRY, state))
    out.append(comp_lod(mlod.LOD_FIRE_GEOMETRY, state, fire=True))
    return out, pts


# ---------------------------------------------------------------------------------------------------- output
def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text if isinstance(text, bytes) else text.replace("\r\n", "\n").encode("utf-8"))


CLASSES = [("JP_EffTest_%s_Tansu" % LEVEL, "intact", "jp_efftest_%s_tansu" % LEVEL, "Tansu (clothing chest)"),
           ("JP_EffTest_%s_Tansu_Ransacked" % LEVEL, "ransacked", "jp_efftest_%s_tansu_ransacked" % LEVEL,
            "Tansu (clothing chest), ransacked")]


def config_cpp():
    cls = ""
    for c, _, p3d, disp in CLASSES:
        cls += ("\tclass %s: HouseNoDestruct\n\t{\n\t\tscope=1;\n\t\tdisplayName=\"%s\";\n"
                "\t\tmodel=\"\\%s\\%s.p3d\";\n\t};\n" % (c, disp, PREFIX, p3d))
    return ("// JP_EffTest_%s - effort test prop (jp_f_tansu, intact + ransacked).\n"
            "// GENERATED by japan_dev/spikes/effort_test/%s/build.py - edit the generator, not this file.\n"
            "class CfgPatches\n{\n\tclass JP_EffTest_%s\n\t{\n\t\tunits[]={\"%s\",\"%s\"};\n\t\tweapons[]={};\n"
            "\t\trequiredVersion=0.1;\n\t\trequiredAddons[]={\"DZ_Data\",\"JP_Common\"};\n\t};\n};\n"
            "class CfgVehicles\n{\n\tclass HouseNoDestruct;\n%s};\n"
            % (LEVEL, LEVEL, LEVEL, CLASSES[0][0], CLASSES[1][0], cls))


def cfgconvert(path):
    os.makedirs(TEMP, exist_ok=True)
    dst = os.path.join(TEMP, "config.bin")
    r = subprocess.run([CFGCONVERT, "-bin", "-dst", dst, path], capture_output=True, text=True, errors="replace")
    ok = r.returncode == 0 and os.path.isfile(dst)
    r2 = subprocess.run([CFGCONVERT, "-txt", "-dst", os.path.join(TEMP, "config_roundtrip.cpp"), dst],
                        capture_output=True, text=True, errors="replace")
    ok = ok and r2.returncode == 0
    msg = "CfgConvert config.cpp: %s %s" % ("OK" if ok else "FAILED", (r.stdout + r.stderr + r2.stdout + r2.stderr).strip())
    print(msg)
    wb(os.path.join(OUT, "cfgconvert.log"), msg + "\n")
    return ok


def binarize():
    out = os.path.join(TEMP, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\" + PREFIX, "-binpath=P:\\bin", "P:\\" + PREFIX, out, "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    wb(os.path.join(OUT, "binarize.log"), " ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr)
    # the 8 environment lines every JP binarize prints (machiya_t3_01's log has the same 8): no world config on P:
    known = re.compile(r"Trying to access error value|Terrain grid 0\.5 will be too slow|CfgVehicles missing in PreloadConfig")
    bad = [l for l in (r.stdout + r.stderr).splitlines()
           if re.search(r"error|warning|cannot|not loaded", l, re.I) and not known.search(l)]
    ok = True
    for _, _, p3d, _ in CLASSES:
        found = None
        for root_, _, files in os.walk(out):
            if p3d + ".p3d" in files:
                found = os.path.join(root_, p3d + ".p3d")
        if found and open(found, "rb").read(4) == b"ODOL":
            shutil.copyfile(found, os.path.join(SRC, p3d + ".p3d"))
            print("binarize OK: %s (%d bytes)" % (p3d, os.path.getsize(found)))
        else:
            print("binarize FAILED for", p3d)
            ok = False
    print("binarize: %d warning/error lines" % len(bad))
    for l in bad[:20]:
        print("   ", l)
    return ok and not bad


def pack():
    stage = os.path.join(TEMP, "pbo_stage")
    shutil.rmtree(stage, ignore_errors=True)
    shutil.copytree(SRC, stage, ignore=shutil.ignore_patterns("*.json", "*.log"))
    import pbo
    try:
        pbo.cmd_pack(stage, PBO_OUT, PREFIX)
    except PermissionError as e:
        alt = os.path.join(HERE, os.path.basename(PBO_OUT))
        pbo.cmd_pack(stage, alt, PREFIX)
        print("PBO write to addons FAILED (locked by a running server?): %s; left in %s" % (e, alt))
        return False
    print("packed", PBO_OUT, os.path.getsize(PBO_OUT), "bytes")
    return True


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SRC, exist_ok=True)
    report = {}
    for cls, state, p3d, _ in CLASSES:
        ls, pts = lods(state)
        mp = os.path.join(OUT, p3d + ".p3d")
        mlod.write_mlod(mp, ls)
        shutil.copyfile(mp, os.path.join(SRC, p3d + ".p3d"))
        faces = {mlod.lod_name(l.resolution): len(l.faces) for l in ls}
        probs = {}
        for l in ls:
            for s in l.selections:
                if s.startswith("Component"):
                    p = mlod.component_report(l, s)
                    if p:
                        probs["%s/%s" % (mlod.lod_name(l.resolution), s)] = p
        geo = mlod.find_lod(ls, mlod.LOD_GEOMETRY)
        report[state] = {"class": cls, "p3d": "%s\\%s.p3d" % (PREFIX, p3d), "faces": faces,
                         "mass_kg": round(sum(geo.mass), 2), "component_problems": probs,
                         "memory": {k: [round(v, 3) for v in p] for k, p in pts.items()}}
        print(state, faces, "mass", round(sum(geo.mass), 1), "problems", probs or "none")
    wb(os.path.join(SRC, "config.cpp"), config_cpp())
    ok = cfgconvert(os.path.join(SRC, "config.cpp"))
    sidecar = {
        "id": "jp_f_tansu", "build_list_row": 26, "level": LEVEL,
        "size_m": [W, D, 2 * H], "frame": "origin base centre on the floor, +z front, autocenter 0",
        "materials": {"body": MATS["wood"][1], "fittings": MATS["iron"][1],
                      "intended": {"body": "jp_m_wood_interior (not built yet)", "fittings": "jp_m_metal_iron"}},
        "loot_surfaces": [
            {"state": "both", "height": 2 * H, "rect": [-0.45, 0.45, -0.19, 0.19], "range": 0.2,
             "points": [report["intact"]["memory"]["loot_top_1"], report["intact"]["memory"]["loot_top_2"]]},
            {"state": "ransacked", "height": "floor (inside the dropped drawer)", "range": 0.2,
             "points": [report["ransacked"]["memory"]["loot_drawer"]]}],
        "states": report,
    }
    wb(os.path.join(HERE, "jp_f_tansu.json"), json.dumps(sidecar, indent=1))
    if "--no-binarize" not in argv:
        ok = binarize() and ok
    if "--no-pack" not in argv:
        ok = pack() and ok
    print("ALL OK" if ok else "SOME STEP FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
