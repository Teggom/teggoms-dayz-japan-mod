"""Core of the JP parts kit (grown from agent B's jpkit: geom.py, p3d.py, materials.py, machiya.sliding_door).

Part frame (PLAYBOOK §10.2): origin at the LEFT POST CENTRELINE, FINISHED FLOOR / SILL LEVEL; +x runs along the
wall, +y up, +z is the exterior face. autocenter=0. Parts that are not wall-like (roofs, stones, steps) use the same
axes; their datum is written in the sidecar ("datum").

A Solid is a closed convex polyhedron (so the same object can be a flat-shaded visual mesh AND a convex component in
Geometry / View / Fire), or a "sheet" (open visual-only faces with explicit outward normals, e.g. a corrugated tile
surface). Face materials and UVs are resolved in the part's own frame when the solid is added (finalize), so a part
can be moved, rotated or mirrored afterwards without its textures sliding.

Materials are library keys ("wood_weathered" = JP\\common\\materials\\wood\\jp_m_wood_weathered_w<n>.rvmat); the wear
level (_w0/_w1/_w2) is chosen per part instance (Part.wear, per-material overrides in Part.wear_by_mat) at write time.
"""
import copy
import json
import math
import os
import random

from . import mlod

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LIB = os.path.join(DEV, "src", "JP", "common", "materials")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")

# ---------------------------------------------------------------------------------------------------- standards
KEN = 1.82            # PLAYBOOK §3/§4: one grid, column-based
HALF = 0.91
QK = 0.455            # trims only
POST = 0.12           # standard post; 0.15 farmhouse main posts
POST_FARM = 0.15
DOOR_H = 2.00         # D2
WALL_H = 2.70         # sill top -> keta underside (kokabe band 2.00-2.70); eave line 2.88 (street eave 2.90-3.20 incl. dodai)
KETA_W, KETA_H = 0.12, 0.18
EAVE_Y = WALL_H + KETA_H          # 2.88: keta top = 'eave' connector
INFILL = 0.075        # shinkabe infill
SETBACK = 0.02        # infill face behind the post face
GAP = 0.012           # air gap wall face -> sliding leaf
OV = 0.02             # leaf overlap into the post rebates
MIN_CLEAR = 1.00      # D1
MIN_HEAD = 2.00       # D2

ROADWAY = {
    "doma": "dz\\surfaces\\data\\roadway\\dirt_int.paa",
    "dirt_ext": "dz\\surfaces\\data\\roadway\\dirt_ext.paa",
    "tatami": "dz\\surfaces\\data\\roadway\\textile_carpet_int.paa",
    "boards": "dz\\surfaces\\data\\roadway\\wood_planks_int.paa",
    "boards_ext": "dz\\surfaces\\data\\roadway\\wood_planks_ext.paa",
    "stair": "dz\\surfaces\\data\\roadway\\wood_planks_stairs_int.paa",
    "stone_ext": "dz\\surfaces\\data\\roadway\\stone_ext.paa",
    "tile_roof": "dz\\surfaces\\data\\roadway\\ceramic_tiles_roof_ext.paa",
    "board_roof": "dz\\surfaces\\data\\roadway\\wood_planks_ext.paa",
    "gravel": "dz\\surfaces\\data\\roadway\\gravel_small_ext.paa",
}


# ---------------------------------------------------------------------------------------------------- library
def _load_lib():
    out = {}
    if not os.path.isdir(LIB):
        return out
    for fam in sorted(os.listdir(LIB)):
        d = os.path.join(LIB, fam)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not (f.startswith("jp_m_") and f.endswith(".json")):
                continue
            sc = json.load(open(os.path.join(d, f), encoding="utf-8"))
            out[sc["id"][5:]] = {
                "id": sc["id"], "family": sc["family"], "tile": float(sc["tile_size_m"]),
                "tile_v": float(sc.get("tile_size_v_m", sc["tile_size_m"])),
                # decals (moss, litter) have no penetration material: fire None (never on a Fire Geometry solid)
                "grain": sc.get("grain", ""),
                "fire": os.path.basename(sc["penetration_rvmat"])[:-len(".rvmat")] if sc.get("penetration_rvmat")
                else None,
                "road": sc.get("roadway_surface"), "alpha": bool(sc.get("alpha")), "palette_id": sc.get("palette_id"),
                # the rvmat finish (build_materials.FINISH: matte / wall / glossy / glazed); older sidecars have none
                "finish": sc.get("finish"),
                # FX3 (2026-10-01): wood atlas (4 m x 2 m, 4 patches): uvwood.remap_part maps the UVs into it
                "atlas": sc.get("atlas"),
            }
    return out


LIBRARY = _load_lib()


def mat_info(key):
    if key not in LIBRARY:
        raise KeyError("material %r is not in the jp_common library (%s)" % (key, LIB))
    return LIBRARY[key]


def tex_path(key, wear):
    m = mat_info(key)
    return "JP\\common\\materials\\%s\\%s%s_%s.paa" % (m["family"], m["id"], wear, "ca" if m["alpha"] else "co")


def rvmat_path(key, wear):
    m = mat_info(key)
    return "JP\\common\\materials\\%s\\%s%s.rvmat" % (m["family"], m["id"], wear)


def png_path(key, wear):
    m = mat_info(key)
    return os.path.join(TEXPNG, "%s%s_%s.png" % (m["id"], wear, "ca" if m["alpha"] else "co"))


def fire_rvmat(fire):
    return "dz\\data\\data\\penetration\\%s.rvmat" % fire


# ---------------------------------------------------------------------------------------------------- vectors
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def length(a):
    return math.sqrt(dot(a, a))


def norm(a):
    l = length(a) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


def newell(pts):
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[(i + 1) % len(pts)]
        nx += (y0 - y1) * (z0 + z1)
        ny += (z0 - z1) * (x0 + x1)
        nz += (x0 - x1) * (y0 + y1)
    return (nx, ny, nz)


def rot_y(p, deg):
    """Yaw about +y. deg=90 turns +x into +z (the part's run then points to +z)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[2] * s, p[1], p[0] * s + p[2] * c)


# ---------------------------------------------------------------------------------------------------- solids
class Solid:
    """mats: a library key, or {'top','bottom','front','back','left','right','side','default'} -> key by outward normal.
    vis: resolution LODs (1, 2, 3). geo / view: component in Geometry / View Geometry. fire: True (the main
    material's library penetration), a penetration name, or None. door: bone. uv: 'world' | 'fit' | 'grain' |
    list of explicit per-face uv lists. normals: explicit per-face outward normals (sheets: open, visual only)."""

    def __init__(self, verts, faces, mats, vis=(1, 2), geo=False, view=False, fire=None, door=None, uv="world",
                 tag="", normals=None, uvscale=None, uvoff=(0.0, 0.0), uvrot=0.0, grain=None, sel=None):
        self.verts = [tuple(float(c) for c in v) for v in verts]
        self.faces = [list(f) for f in faces]
        self.mats = mats
        self.vis = set(vis)
        self.geo = geo
        self.view = view
        self.fire = fire
        self.door = door
        self.uv = uv
        self.tag = tag
        self.normals = normals
        self.uvscale = uvscale
        self.uvoff = uvoff
        self.uvrot = uvrot
        self.grain = grain
        self.sel = sel                  # extra named selection (e.g. 'stone3' in a stone set)
        self.fm = None                  # per-face material key (resolved)
        self.fuv = None                 # per-face uv lists (resolved)
        self.fn = None                  # per-face outward normals (resolved)
        self.center = tuple(sum(v[k] for v in self.verts) / len(self.verts) for k in range(3))

    @property
    def closed(self):
        return self.normals is None

    def face_points(self, fi):
        return [self.verts[i] for i in self.faces[fi]]

    def _outward(self, fi):
        pts = self.face_points(fi)
        n = norm(newell(pts))
        if self.normals is not None:
            want = self.normals[fi] if isinstance(self.normals, list) else self.normals
            return n if dot(n, want) >= 0 else mul(n, -1.0)
        fc = tuple(sum(p[k] for p in pts) / len(pts) for k in range(3))
        if dot(n, sub(fc, self.center)) < 0:
            n = mul(n, -1.0)
        return n

    @staticmethod
    def role(n):
        if n[1] > 0.5:
            return "top"
        if n[1] < -0.5:
            return "bottom"
        if n[2] > 0.7:
            return "front"
        if n[2] < -0.7:
            return "back"
        if n[0] > 0.7:
            return "right"
        if n[0] < -0.7:
            return "left"
        return "side"

    def _mat(self, n):
        if isinstance(self.mats, str):
            return self.mats
        r = self.role(n)
        if r in self.mats:
            return self.mats[r]
        if r in ("front", "back", "left", "right") and "side" in self.mats:
            return self.mats["side"]
        return self.mats.get("default", next(iter(self.mats.values())))

    def main_mat(self):
        if isinstance(self.mats, str):
            return self.mats
        return self.mats.get("default", next(iter(self.mats.values())))

    def fire_mat(self):
        if not self.fire:
            return None
        if self.fire is True:
            return mat_info(self.main_mat())["fire"]
        return self.fire

    def finalize(self):
        if self.fm is not None:
            return self
        self.fn, self.fm, self.fuv = [], [], []
        for fi in range(len(self.faces)):
            n = self._outward(fi)
            self.fn.append(n)
            m = self._mat(n)
            mat_info(m)
            self.fm.append(m)
            if isinstance(self.uv, list):
                self.fuv.append(self.uv[fi])
            else:
                self.fuv.append(face_uvs(self, fi, n, m))
        # MLOD faces are tris or quads: split larger convex planar polygons into a quad fan
        if any(len(f) > 4 for f in self.faces):
            nf, nfm, nfuv, nfn = [], [], [], []
            for f, m, uv, n in zip(self.faces, self.fm, self.fuv, self.fn):
                if len(f) <= 4:
                    nf.append(f); nfm.append(m); nfuv.append(uv); nfn.append(n)
                    continue
                k = 1
                while k < len(f) - 1:
                    idx = [0, k, k + 1, k + 2] if k + 2 < len(f) else [0, k, k + 1]
                    nf.append([f[i] for i in idx]); nfm.append(m); nfuv.append([uv[i] for i in idx]); nfn.append(n)
                    k += len(idx) - 2
            self.faces, self.fm, self.fuv, self.fn = nf, nfm, nfuv, nfn
            if self.normals is not None:
                self.normals = self.fn
        return self

    def bbox(self):
        xs = [v[0] for v in self.verts]
        ys = [v[1] for v in self.verts]
        zs = [v[2] for v in self.verts]
        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    def transformed(self, deg=0.0, t=(0.0, 0.0, 0.0), mirror=False):
        s = copy.copy(self)
        f = (lambda p: (-p[0], p[1], p[2])) if mirror else (lambda p: p)
        s.verts = [add(rot_y(f(v), deg), t) for v in self.verts]
        s.center = add(rot_y(f(self.center), deg), t)
        if self.fn is not None:
            s.fn = [rot_y(f(n), deg) for n in self.fn]
        if self.normals is not None:
            s.normals = s.fn
        s.faces = [list(ff) for ff in self.faces]
        return s


def face_uvs(solid, fi, n, mat):
    """World-scale planar UVs (MLOD: u right, v down). Tile size from the library sidecar or solid.uvscale."""
    pts = solid.face_points(fi)
    mi = mat_info(mat)
    if solid.uv == "fit":
        mode = "fit"
    else:
        mode = "world"
    if abs(n[1]) > 0.7:
        ua = norm(sub((1.0, 0.0, 0.0), mul(n, n[0])))
        if length(sub((1.0, 0.0, 0.0), mul(n, n[0]))) < 1e-6:
            ua = (0.0, 0.0, 1.0)
        va = norm(cross(n, ua))
        if va[1] > 1e-6 or (abs(va[1]) <= 1e-6 and va[2] < 0):
            va = mul(va, -1.0)
    else:
        va = norm(sub((0.0, -1.0, 0.0), mul(n, -n[1])))
        ua = norm(cross(va, n))
        if dot(cross(ua, va), n) < 0:
            ua = mul(ua, -1.0)
    grain = solid.grain if solid.grain is not None else ("long" if "along" in mi["grain"] else None)
    if grain == "long" or solid.uv == "grain":
        x0, x1, y0, y1, z0, z1 = solid.bbox()
        ext = sorted([(x1 - x0, (1.0, 0.0, 0.0)), (y1 - y0, (0.0, 1.0, 0.0)), (z1 - z0, (0.0, 0.0, 1.0))],
                     key=lambda e: -e[0])
        L = ext[0][1]
        if abs(dot(L, n)) < 0.3:
            va = norm(sub(L, mul(n, dot(L, n))))
            ua = norm(cross(va, n))
    if mode == "fit":
        us = [dot(p, ua) for p in pts]
        vs = [dot(p, va) for p in pts]
        du = (max(us) - min(us)) or 1.0
        dv = (max(vs) - min(vs)) or 1.0
        return [((u - min(us)) / du + solid.uvoff[0], (v - min(vs)) / dv + solid.uvoff[1]) for u, v in zip(us, vs)]
    su, sv = solid.uvscale if solid.uvscale else (mi["tile"], mi["tile_v"])
    out = []
    ca, sa = math.cos(math.radians(solid.uvrot)), math.sin(math.radians(solid.uvrot))
    for p in pts:
        u, v = dot(p, ua) / su, dot(p, va) / sv
        if solid.uvrot:
            u, v = u * ca - v * sa, u * sa + v * ca
        out.append((u + solid.uvoff[0], v + solid.uvoff[1]))
    return out


# ---------------------------------------------------------------------------------------------------- primitives
def prism(poly, axis, t0, t1, mats, **kw):
    """Extrude a convex 2D polygon along an axis. poly=[(a,b)]; axis 'x': (a,b)=(y,z); 'y': (x,z); 'z': (x,y)."""
    def p3(a, b, t):
        if axis == "x":
            return (t, a, b)
        if axis == "y":
            return (a, t, b)
        return (a, b, t)
    n = len(poly)
    verts = [p3(a, b, t0) for a, b in poly] + [p3(a, b, t1) for a, b in poly]
    faces = [list(range(n)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    return Solid(verts, faces, mats, **kw)


def box(x0, x1, y0, y1, z0, z1, mats, **kw):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    z0, z1 = min(z0, z1), max(z0, z1)
    return prism([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "z", z0, z1, mats, **kw)


def hexa(corners, mats, **kw):
    """Convex hexahedron: bottom quad c0..c3 then top quad c4..c7 (same order)."""
    faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return Solid(corners, faces, mats, **kw)


def ngon(cx, cy, r, n, phase=0.0, rx=None):
    rx = r if rx is None else rx
    return [(cx + rx * math.cos(phase + 2 * math.pi * k / n), cy + r * math.sin(phase + 2 * math.pi * k / n))
            for k in range(n)]


def cyl(axis, c0, c1, r, t0, t1, mats, n=8, phase=None, **kw):
    """n-gon prism (round members: covers, poles, bamboo). c0,c1 = centre in the cross-section plane."""
    ph = math.pi / n if phase is None else phase
    return prism(ngon(c0, c1, r, n, ph), axis, t0, t1, mats, **kw)


def rings(rings_, mats, **kw):
    """Convex 'stone': stacked homothetic rings [(y, cx, cz, scale)] of one base polygon (convex if the scale
    profile is concave). rings_ = (base_poly [(x,z)], [(y, scale)])."""
    base, prof = rings_
    cx = sum(p[0] for p in base) / len(base)
    cz = sum(p[1] for p in base) / len(base)
    n = len(base)
    verts = []
    for y, s in prof:
        for (x, z) in base:
            verts.append((cx + (x - cx) * s, y, cz + (z - cz) * s))
    faces = [list(range(n))[::-1], list(range(n * (len(prof) - 1), n * len(prof)))]
    for r in range(len(prof) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append([r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i])
    return Solid(verts, faces, mats, **kw)


def rand_convex(rng, n, rx, rz, jitter=0.18):
    """Random convex polygon (angles sorted, radii jittered, then hull)."""
    pts = []
    for k in range(n):
        a = 2 * math.pi * (k + rng.uniform(-0.3, 0.3)) / n
        f = 1.0 + rng.uniform(-jitter, jitter)
        pts.append((rx * f * math.cos(a), rz * f * math.sin(a)))
    return hull2d(pts)


def hull2d(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def stone(rng, x, z, w, d, h, top_y, mats, bury=0.12, n=9, flat_top=0.55, **kw):
    """One convex stone centred at (x, z): footprint ~w x d, top at top_y, buried `bury` below its visible foot.
    Rounded by homothetic rings (profile concave -> convex solid)."""
    base = [(x + a, z + b) for a, b in rand_convex(rng, n, w / 2, d / 2)]
    y0 = top_y - h - bury
    prof = [(y0, 0.86), (top_y - h * 0.62, 1.0), (top_y - h * 0.22, 0.93), (top_y, flat_top + rng.uniform(-0.08, 0.08))]
    return rings((base, prof), mats, **kw)


def sheet(quads, mats, normal, vis=(1,), uvs=None, tag="", **kw):
    """Open visual-only faces (tris/quads) sharing one outward hint normal (or a list)."""
    verts, faces = [], []
    for q in quads:
        faces.append(list(range(len(verts), len(verts) + len(q))))
        verts.extend(q)
    normals = normal if isinstance(normal, list) else [normal] * len(faces)
    return Solid(verts, faces, mats, vis=vis, geo=False, view=False, fire=None, uv=uvs if uvs else "world",
                 normals=normals, tag=tag, **kw)


# ---------------------------------------------------------------------------------------------------- doors
class Door:
    """One config door (animation source DoorsN). anims: [{bone, type 'translation'|'rotation', axis (p0, p1),
    amount (m or rad)}]. Leaf solids carry solid.door = bone."""

    def __init__(self, **kw):
        self.anims = []
        self.kind = "plank"
        self.anim_period = 1.0
        self.init_opened = 0.3
        self.sound = "doorWoodSlide"
        self.display = "door"
        self.note = ""
        self.clear = None
        self.action = None
        self.centre = None
        self.__dict__.update(kw)

    def bones(self):
        return [a["bone"] for a in self.anims]


def anim_point_fn(a, frac=1.0):
    """p -> p moved by one door animation at phase frac (0 closed .. 1 open). translation: along (axis1 - axis0) by
    amount (the axis is 1.00 m). rotation: about the line axis0 -> axis1 by amount (rad), right-hand rule in the raw
    p3d model coordinates (G3 fix pass; the engine's sign convention is recorded in PLAYBOOK §15)."""
    p0, p1 = a["axis"][0], a["axis"][1]
    d = sub(p1, p0)
    if a["type"] == "translation":
        off = mul(d, a["amount"] * frac)
        return lambda p: add(p, off)
    u = norm(d)
    th = a["amount"] * frac * ROT_SIGN
    c, s = math.cos(th), math.sin(th)

    def f(p):
        v = sub(p, p0)
        r = add(add(mul(v, c), mul(cross(u, v), s)), mul(u, dot(u, v) * (1 - c)))
        return add(p0, r)
    return f


ROT_SIGN = 1.0      # +1: model.cfg angle1 > 0 turns by the right-hand rule about axis0 -> axis1 (see PLAYBOOK §15)


# ---------------------------------------------------------------------------------------------------- part
class Part:
    def __init__(self, pid, variant="", group="", **meta):
        self.pid = pid
        self.variant = variant
        self.group = group
        self.meta = meta
        self.solids = []
        self.roadway = []            # [(pts, surface key)]
        self.memory = {}             # name -> [pts]
        self.doors = []
        self.connectors = []         # [{type, pos, ...}]
        self.dims = []               # [{name, expected, measured, tol, source}]
        self.notes = []
        self.walkable = False
        self.wear = "_w1"
        self.wear_by_mat = {}
        self.floors = []             # loot / walk floors [{name, rect, y}]
        self.bays = []               # (x0, x1) opening/park bays for sweep checks

    @property
    def name(self):
        return self.pid + self.variant

    def add(self, s):
        s.finalize()
        self.solids.append(s)
        return s

    def extend(self, ss):
        for s in ss:
            self.add(s)

    def road(self, pts, surf):
        if surf not in ROADWAY:
            raise KeyError(surf)
        pts = [tuple(float(c) for c in p) for p in pts]
        k = 1
        while k < len(pts) - 1:                      # convex polygon -> quad fan (MLOD faces are tris / quads)
            idx = [0, k, k + 1, k + 2] if k + 2 < len(pts) else [0, k, k + 1]
            self.roadway.append(([pts[i] for i in idx], surf))
            k += len(idx) - 2
        self.walkable = True

    def conn(self, ctype, pos, **kw):
        d = {"type": ctype, "pos": [round(float(c), 4) for c in pos]}
        d.update(kw)
        self.connectors.append(d)

    def dim(self, name, expected, measured, tol=0.01, source="build_list"):
        self.dims.append({"name": name, "expected": expected, "measured": round(float(measured), 4), "tol": tol,
                          "source": source})

    def next_bone(self):
        return "doors%d" % (sum(len(d.anims) for d in self.doors) + 1)

    def wear_of(self, mat):
        return self.wear_by_mat.get(mat, self.wear)

    # ------------------------------------------------------------------ transforms / merge
    def transformed(self, deg=0.0, t=(0.0, 0.0, 0.0), mirror=False):
        p = copy.copy(self)
        f = (lambda q: (-q[0], q[1], q[2])) if mirror else (lambda q: q)
        T = lambda q: add(rot_y(f(q), deg), t)          # noqa: E731
        p.solids = [s.transformed(deg, t, mirror) for s in self.solids]
        p.roadway = [([T(q) for q in pts], surf) for pts, surf in self.roadway]
        p.memory = {k: [T(q) for q in v] for k, v in self.memory.items()}
        p.doors = []
        for d in self.doors:
            nd = copy.copy(d)
            nd.anims = []
            for a in d.anims:
                na = dict(a)
                na["axis"] = [T(q) for q in a["axis"]]
                if a["type"] == "rotation" and mirror:
                    na["amount"] = -a["amount"]
                nd.anims.append(na)
            nd.action = T(d.action) if d.action else None
            nd.centre = T(d.centre) if d.centre else None
            p.doors.append(nd)
        p.connectors = [dict(c, pos=[round(v, 4) for v in T(c["pos"])]) for c in self.connectors]
        return p

    def merge(self, other, prefix=""):
        """Append another part (already placed). Door bones are renumbered."""
        remap = {}
        base = sum(len(d.anims) for d in self.doors)
        k = base
        for d in other.doors:
            for a in d.anims:
                k += 1
                remap[a["bone"]] = "doors%d" % k
        for s in other.solids:
            ns = copy.copy(s)
            if s.door:
                ns.door = remap[s.door]
            if not getattr(ns, "src", None):
                ns.src = other.name          # which sub-part it came from (roof / wall intersection checks)
            self.solids.append(ns)
        self.roadway += other.roadway
        for key, v in other.memory.items():
            nk = key
            for ob, nb in remap.items():
                if key == ob or key.startswith(ob + "_"):
                    nk = nb + key[len(ob):]
            if nk in self.memory:
                nk = prefix + nk
            self.memory[nk] = v
        for d in other.doors:
            nd = copy.copy(d)
            nd.anims = [dict(a, bone=remap[a["bone"]]) for a in d.anims]
            self.doors.append(nd)
        self.walkable = self.walkable or other.walkable
        self.floors += other.floors
        return self

    # ------------------------------------------------------------------ LODs
    def bbox(self, vis_only=True):
        xs, ys, zs = [], [], []
        for s in self.solids:
            if vis_only and not s.vis:
                continue
            b = s.bbox()
            xs += b[0:2]
            ys += b[2:4]
            zs += b[4:6]
        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    def lods(self, geo_props=None, mass=None):
        """Every LOD the part contributes to: Res 1-3, Geometry, Memory, Roadway, View, Fire (empty ones omitted,
        Res 1 always written)."""
        from . import uvwood                # FX3: wood atlas patches / offsets / flips per uv group (idempotent)
        uvwood.remap_part(self)
        out = []
        for k in (1, 2, 3):
            lod = self._visual(k)
            if lod.faces or k == 1:
                out.append(lod)
        g = self._components(mlod.LOD_GEOMETRY, "geo")
        if g.faces:
            if geo_props:
                g.properties.update(geo_props)
            if mass:
                g.mass = [mass / len(g.points)] * len(g.points)
            out.append(g)
        if self.memory:
            out.append(self._memory())
        if self.roadway:
            out.append(self._roadway())
        for res, which in ((mlod.LOD_VIEW_GEOMETRY, "view"), (mlod.LOD_FIRE_GEOMETRY, "fire")):
            l = self._components(res, which)
            if l.faces:
                out.append(l)
        return out

    def _door_sels(self, lod):
        for d in self.doors:
            for b in d.bones():
                lod.selections.setdefault(b, ({}, set()))

    def _visual(self, k):
        lod = mlod.Lod(float(k))
        self._door_sels(lod)
        for s in self.solids:
            if k not in s.vis:
                continue
            for fi in range(len(s.faces)):
                m = s.fm[fi]
                w = self.wear_of(m)
                face, pis = lod.add_flat_face(s.face_points(fi), s.fn[fi], s.fuv[fi], tex_path(m, w), rvmat_path(m, w))
                if s.door:
                    lod.select(s.door, {pi: 1.0 for pi in pis}, [face])
                if s.sel:
                    lod.select(s.sel, {pi: 1.0 for pi in pis}, [face])
        for d in self.doors:
            for b in d.bones():
                if not lod.selections[b][1] and k == 1:
                    raise ValueError("%s: door bone %s has no faces in resolution 1" % (self.name, b))
        # drop empty door selections in lower LODs (a door may be omitted there)
        for b in [b for b, (pw, fs) in lod.selections.items() if not fs and not pw]:
            del lod.selections[b]
        return lod

    def _components(self, res, which):
        lod = mlod.Lod(res)
        self._door_sels(lod)
        n = 0
        for s in self.solids:
            if not s.closed:
                continue
            if which == "geo" and not s.geo:
                continue
            if which == "view" and not s.view:
                continue
            if which == "fire" and not s.fire:
                continue
            n += 1
            mat = fire_rvmat(s.fire_mat()) if which == "fire" else ""
            pis, fis = lod.add_closed_solid(s.verts, s.faces, "", mat)
            lod.select("Component%02d" % n, {pi: 1.0 for pi in pis}, fis)
            if s.door:
                lod.select(s.door, {pi: 1.0 for pi in pis}, fis)
            if s.sel:
                lod.select(s.sel, {pi: 1.0 for pi in pis}, fis)
        for b in [b for b, (pw, fs) in lod.selections.items() if not fs and not pw]:
            del lod.selections[b]
        return lod

    def _memory(self):
        lod = mlod.Lod(mlod.LOD_MEMORY)
        for name in sorted(self.memory):
            pis = [lod.add_point(p) for p in self.memory[name]]
            lod.select(name, {pi: 1.0 for pi in pis})
        return lod

    def _roadway(self):
        lod = mlod.Lod(mlod.LOD_ROADWAY)
        for pts, surf in self.roadway:
            n = norm(newell(pts))
            if n[1] < 0:
                n = mul(n, -1.0)
            lod.add_flat_face(pts, n, [(0.0, 0.0)] * len(pts), ROADWAY[surf], "")
        return lod

    def write(self, path, geo_props=None, mass=None):
        lods = self.lods(geo_props, mass)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mlod.write_mlod(path, lods)
        return lods


# ---------------------------------------------------------------------------------------------------- sliding leaf
STUB = 0.22          # G3 (2026-09-27): an OPEN sliding leaf keeps 0.22 m inside the opening, like vanilla (Land_Barn_Brick2
#                      0.22 m, rail warehouse 0.30 m): DayZ finds a door only by the View Geometry component the camera
#                      ray hits, so a leaf parked fully behind the wall cannot be closed from the other side (PLAYBOOK §15)


def sliding_leaf(part, x0, x1, y0, height, z_face, side, direction, mats, thick=0.04, kind="plank", fire=True,
                 note="", build=None, park_span=None, anim_period=None, init_opened=None, stub=STUB):
    """One translation door (B's proven format): the leaf covers the opening [x0, x1] (+OV each side), runs on the
    face at z_face on `side` (+1 outside / -1 inside), slides `direction` (+1/-1 along x) until only `stub` of it is
    left in the opening (vanilla rule, see STUB). build(leaf_x0, leaf_x1, y_bot, y_top, z0, z1, bone) -> list of
    Solids (visual detail + one closed leaf solid flagged geo/view/fire). The memory point <bone> sits on the leaf's
    trailing edge at hand height (vanilla), so it stays in the doorway when open. Returns the Door."""
    bone = part.next_bone()
    l0, l1 = x0 - OV, x1 + OV
    width = l1 - l0
    slide = width - OV - stub
    zc = z_face + side * (GAP + thick / 2)
    z0, z1 = zc - thick / 2, zc + thick / 2
    bot, top = y0 + 0.004, y0 + height + 0.03
    o0, o1 = l0 + direction * slide, l1 + direction * slide
    if park_span and (o0 < park_span[0] - 1e-3 or o1 > park_span[1] + 1e-3):
        raise ValueError("%s: open leaf [%.2f, %.2f] leaves the park span %s" % (part.name, o0, o1, park_span))
    solids = build(l0, l1, bot, top, z0, z1, bone, dirn=direction) if build else [
        box(l0, l1, bot, top, z0, z1, mats, vis=(1, 2, 3), geo=True, view=True, fire=fire, uv="fit", tag="door")]
    for s in solids:
        s.door = bone
        part.add(s)
    centre = ((l0 + l1) / 2, (bot + top) / 2, zc)
    axis = [centre, (centre[0] + direction, centre[1], centre[2])]
    action = ((x0 + x1) / 2, y0 + 1.0, z_face)
    trail = (l0 + 0.04, y0 + 1.0, zc) if direction > 0 else (l1 - 0.04, y0 + 1.0, zc)
    part.memory[bone + "_axis"] = axis
    part.memory[bone + "_action"] = [action]
    part.memory[bone] = [trail]
    d = Door(kind=kind, anims=[{"bone": bone, "type": "translation", "axis": axis, "amount": slide}],
             action=action, centre=centre, width=width, slide=slide, direction=(float(direction), 0.0, 0.0),
             anim_period=anim_period or (1.0 if kind == "plank" else 0.8),
             init_opened=init_opened if init_opened is not None else (0.3 if kind == "plank" else 0.5),
             display="%s door" % kind, note=note, opening=(x0, x1, y0, y0 + height), z_face=z_face, side=side,
             leaf_z=(z0, z1), leaf_x=(l0, l1), leaf_y=(bot, top), sweep=(min(l0, o0), max(l1, o1)), stub=stub,
             style="single")
    part.doors.append(d)
    return d


def rng_for(name, k=0):
    return random.Random(hash_str(name) + k)


def hash_str(s):
    h = 2166136261
    for ch in s.encode("utf-8"):
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h
