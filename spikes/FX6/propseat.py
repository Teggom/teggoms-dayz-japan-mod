"""FX6 seat check for the props placed in a furnished building (Stephen's 3c-1 walk, 2026-10-02: "one of the washbasins
is floating in mid-air at an angle rather than resting on something").

For every Resolution-1 proxy whose catalogue anchor is 'floor' (or a surface item): the prop's own support points (the
master's Resolution-1 vertices at its floor plane, y <= 2 cm, clustered 5 cm) are taken into the building and a
vertical ray is cast DOWN from 2 cm above each one against the building's Resolution-1 faces, the other props' faces
and the grade plane (y 0, for yard objects). A cluster passes when it meets a face within GAP (3 cm) below; it fails
when the nearest face under it is further down (floating) or there is none. Sunk points (the face is above) pass: the
seated pots and the sunk-to-the-rim jars are deliberate. A prop that is tilted inside its master (a tub on edge) is
checked by spikes/FX6/propfloat.py (its pieces must rest on each other).

  python spikes/FX6/propseat.py <furnished mlod ...>      (default: the 3c-1 furnished set)
"""
import glob
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "buildings")):
    if p not in sys.path:
        sys.path.insert(0, p)
from jpparts import mlod, proxies as PX, decor as DC  # noqa: E402

GAP = 0.03
_M = {}


def res1(lods):
    return next(l for l in lods if mlod.lod_name(l.resolution) == "Resolution 1")


def tris(lod, drop_proxies=True):
    drop = PX.proxy_faces(lod) if drop_proxies else set()
    P = np.array(lod.points, dtype=float)
    T = []
    for i, (verts, _, _, _) in enumerate(lod.faces):
        if i in drop:
            continue
        ids = [v[0] for v in verts]
        T.append((ids[0], ids[1], ids[2]))
        if len(ids) == 4:
            T.append((ids[0], ids[2], ids[3]))
    return P[np.array(T)] if T else np.zeros((0, 3, 3))


def master(stem, path):
    if stem not in _M:
        l = res1(mlod.read_mlod(path))
        T = tris(l)
        P = np.array([l.points[i] for i in sorted({v[0] for f in l.faces for v in f[0]})], dtype=float)
        sup = P[P[:, 1] <= 0.02]
        cl = []
        for p in sup:
            for c in cl:
                if math.hypot(p[0] - c[0][0], p[2] - c[0][2]) < 0.05:
                    c.append(p)
                    break
            else:
                cl.append([p])
        _M[stem] = (T, np.array([np.mean(c, axis=0) for c in cl]) if cl else np.zeros((0, 3)))
    return _M[stem]


def place(P, o, yaw):
    r, u, f = PX.frame(yaw)
    R = np.array([r, u, f])                       # rows: local x, y, z axes in the model frame
    return P @ R + np.array(o)


def down_gap(T, pts, eps=0.02):
    """Per point: distance down from the point to the first face below (start eps above), inf if none."""
    out = np.full(len(pts), np.inf)
    if not len(T):
        return out
    a, b, c = T[:, 0], T[:, 1], T[:, 2]
    d = (b[:, 2] - c[:, 2]) * (a[:, 0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (a[:, 2] - c[:, 2])
    ok = np.abs(d) > 1e-12
    a, b, c, d = a[ok], b[ok], c[ok], d[ok]
    for k, p in enumerate(pts):
        l1 = ((b[:, 2] - c[:, 2]) * (p[0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (p[2] - c[:, 2])) / d
        l2 = ((c[:, 2] - a[:, 2]) * (p[0] - c[:, 0]) + (a[:, 0] - c[:, 0]) * (p[2] - c[:, 2])) / d
        l3 = 1 - l1 - l2
        m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        if not m.any():
            continue
        yy = l1[m] * a[m, 1] + l2[m] * b[m, 1] + l3[m] * c[m, 1]
        below = yy[yy <= p[1] + eps]
        if len(below):
            out[k] = p[1] - below.max()
    return out


def check(path, verbose=True):
    lods = mlod.read_mlod(path)
    l = res1(lods)
    B = tris(l)
    cat = DC.catalog()
    props = []
    for name, o, up, fw in PX.listed(l):
        stem = name.split(":", 1)[1].rsplit(".", 1)[0].replace("\\", "/").split("/")[-1].lower()
        inf = cat.get(stem)
        if not inf or not inf.get("master") or not os.path.exists(inf["master"]):
            continue
        yaw = math.degrees(math.atan2(fw[0], fw[2]))
        T, S = master(stem, inf["master"])
        props.append((stem, inf, o, yaw, place(T.reshape(-1, 3), o, yaw).reshape(-1, 3, 3), place(S, o, yaw)
                      if len(S) else S))
    res = []
    for i, (stem, inf, o, yaw, Tw, Sw) in enumerate(props):
        if inf.get("anchor") in ("hang", "wall") or inf.get("mount") in ("beam", "wall") or not len(Sw):
            continue
        others = [B] + [q[4] for j, q in enumerate(props) if j != i]
        # the grade plane (yard objects outside the building)
        g = 20.0
        grade = np.array([[(-g, 0, -g), (g, 0, -g), (g, 0, g)], [(-g, 0, -g), (g, 0, g), (-g, 0, g)]], dtype=float)
        T = np.concatenate([t for t in others if len(t)] + [grade])
        gaps = down_gap(T, Sw)
        bad = [(tuple(round(float(v), 2) for v in Sw[k]), None if not np.isfinite(gaps[k]) else round(float(gaps[k]), 3))
               for k in range(len(Sw)) if not (gaps[k] <= GAP)]
        ok = not bad
        res.append((stem, ok, o, bad))
        if verbose and not ok:
            print("  FAIL %-30s at (%.2f, %.2f, %.2f) yaw %.0f: %d/%d support points float: %s" %
                  (stem, o[0], o[1], o[2], yaw, len(bad), len(Sw), bad[:4]))
    return res


def main():
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(DEV, "buildings", "ts_furnished", "out", "*.p3d")))
    nf = nt = 0
    for p in paths:
        r = check(p)
        nt += len(r)
        f = sum(1 for x in r if not x[1])
        nf += f
        print("%-44s %d floor props, %d floating" % (os.path.basename(p), len(r), f))
    print("PROPSEAT: %d props, %d floating" % (nt, nf))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
