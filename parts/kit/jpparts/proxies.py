"""Furniture / dressing proxies in a building MLOD (B4 pilot, 2026-09-30).

A proxy in an MLOD LOD is one triangle plus a named selection "proxy:<p3d path without .p3d>.<nnn>" holding its three
points and the face. binarize.exe turns it into a proxy record (model path + 4x3 transform) in the ODOL and drops the
triangle. The triangle's frame (verified by binarizing a test model and reading the ODOL proxy transforms back,
spikes/B4/proxy_test.py, 2026-09-30):
  v0 = origin (the prop's base centre), v1 = origin + 2 x up (+y of the prop), v2 = origin + 1 x forward (+z of the prop)
so the long edge is the prop's up axis and the short one its front.

Which LODs carry a proxy (research/interior/BUILD_LIST.md Q5, binding for B3/B4): furniture with collision goes in
Resolution 1, Geometry, View Geometry and Fire Geometry; flat and hanging props (mats, litter, jizai-kagi, kamidana)
in Resolution 1 only. Never in Resolution 2+, Memory, Roadway or Paths.

Helpers:
  add(lods, proxies)      proxies = [{p3d, pos (x, y, z model), yaw (deg, clockwise from +z seen from above), lods}]
  is_proxy_face(lod, fi)  / strip(lod) -> a copy without proxy faces (for checks that read the MLOD back)
  frame(yaw)              (right, up, forward) unit vectors
"""
import copy
import math

from . import mlod

LODS_COLLISION = ("Resolution 1", "Geometry", "View Geometry", "Fire Geometry")
LODS_VISUAL = ("Resolution 1",)
UP_LEN, FWD_LEN = 2.0, 1.0


def frame(yaw):
    a = math.radians(yaw)
    fwd = (math.sin(a), 0.0, math.cos(a))
    right = (math.cos(a), 0.0, -math.sin(a))
    return right, (0.0, 1.0, 0.0), fwd


def to_model(local, pos, yaw):
    """A point in the prop frame -> the building model frame."""
    r, u, f = frame(yaw)
    x, y, z = local
    return (pos[0] + r[0] * x + f[0] * z, pos[1] + y, pos[2] + r[2] * x + f[2] * z)


def triangle(pos, yaw):
    _, u, f = frame(yaw)
    o = tuple(float(v) for v in pos)
    return [o, (o[0] + u[0] * UP_LEN, o[1] + u[1] * UP_LEN, o[2] + u[2] * UP_LEN),
            (o[0] + f[0] * FWD_LEN, o[1] + f[1] * FWD_LEN, o[2] + f[2] * FWD_LEN)]


def sel_name(p3d, idx):
    path = p3d[:-4] if p3d.lower().endswith(".p3d") else p3d
    if not path.startswith("\\"):
        path = "\\" + path
    return "proxy:%s.%03d" % (path, idx)


def add(lods, proxies):
    """Append proxy triangles to the named LODs (mlod.Lod list, as Part.lods() returns it). Each proxy model gets its
    own running index per LOD (vanilla: .001, .002 ...). Returns {lod name: count}."""
    by = {mlod.lod_name(l.resolution): l for l in lods}
    count = {}
    idx = {}
    for p in proxies:
        for ln in p["lods"]:
            lod = by[ln]
            pts = triangle(p["pos"], p.get("yaw", 0.0))
            pis = [lod.add_point(q) for q in pts]
            n = mlod._normalize(mlod._face_formula_normal(pts))
            ni = lod.add_normal(n)
            fi = lod.add_face([(pi, ni, 0.0, 0.0) for pi in pis], "", "")
            k = (ln, p["p3d"].lower())
            idx[k] = idx.get(k, 0) + 1
            lod.select(sel_name(p["p3d"], idx[k]), {pi: 1.0 for pi in pis}, [fi])
            if lod.mass is not None:                 # Geometry: one mass per point; proxy points weigh nothing
                lod.mass += [0.0] * len(pis)
            count[ln] = count.get(ln, 0) + 1
    return count


def proxy_faces(lod):
    fs = set()
    for name, (pw, f) in lod.selections.items():
        if name.lower().startswith("proxy:"):
            fs |= f
    return fs


def strip(lod):
    """A copy of an mlod.Lod without its proxy triangles (points left in place; selections re-indexed)."""
    drop = proxy_faces(lod)
    if not drop:
        return lod
    out = copy.copy(lod)
    keep = [i for i in range(len(lod.faces)) if i not in drop]
    remap = {old: new for new, old in enumerate(keep)}
    out.faces = [lod.faces[i] for i in keep]
    out.selections = {}
    for name, (pw, fs) in lod.selections.items():
        if name.lower().startswith("proxy:"):
            continue
        out.selections[name] = (dict(pw), {remap[i] for i in fs if i in remap})
    return out


def listed(lod):
    """[(selection name, origin, up, forward)] of the proxies in an MLOD LOD (read back)."""
    out = []
    for name, (pw, fs) in lod.selections.items():
        if not name.lower().startswith("proxy:") or not fs:
            continue
        f = lod.faces[sorted(fs)[0]]
        p = [lod.points[v[0]] for v in f[0]]
        # the right angle is at the origin; the longer leg is up
        best = None
        for i in range(3):
            a, b, c = p[i], p[(i + 1) % 3], p[(i + 2) % 3]
            e1 = [b[q] - a[q] for q in range(3)]
            e2 = [c[q] - a[q] for q in range(3)]
            d = abs(sum(e1[q] * e2[q] for q in range(3)))
            if best is None or d < best[0]:
                best = (d, a, e1, e2)
        _, o, e1, e2 = best
        l1, l2 = math.sqrt(sum(v * v for v in e1)), math.sqrt(sum(v * v for v in e2))
        up, fw = (e1, e2) if l1 >= l2 else (e2, e1)
        out.append((name, o, tuple(v / max(l1, l2) for v in up), tuple(v / min(l1, l2) for v in fw)))
    return out
