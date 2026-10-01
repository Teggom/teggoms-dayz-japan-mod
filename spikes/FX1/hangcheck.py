"""FX1 hang check: does every hung prop (mount 'beam' / anchor 'hang') in a building hang from something real?

For each Resolution-1 proxy whose catalogue mount is 'beam' (or anchor 'hang'), the prop's attachment points (its
master's Resolution-1 vertices within 1 cm of its top, y >= top - 0.01, clustered) are taken to the model frame and a
vertical ray is cast UP from 1 cm below each point against the building's own Resolution-1 faces (proxies stripped).
PASS when every attachment cluster meets a face within GAP (3 cm) above it.

  python spikes/FX1/hangcheck.py [mlod ...]     default: the wave-2 furnished MLODs in buildings/furnished/out
"""
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "buildings")):
    if p not in sys.path:
        sys.path.insert(0, p)
from jpparts import mlod, proxies as PX, decor as DC  # noqa: E402

GAP = 0.03
W2 = ("shrine", "temple", "teahouse", "smithy", "swordsmith", "guardhut", "kido")


def res1(lods):
    return next(l for l in lods if mlod.lod_name(l.resolution) == "Resolution 1")


def tris(lod):
    out = []
    drop = PX.proxy_faces(lod)
    for i, (verts, _, _, _) in enumerate(lod.faces):
        if i in drop:
            continue
        p = [lod.points[v[0]] for v in verts]
        out.append((p[0], p[1], p[2]))
        if len(p) == 4:
            out.append((p[0], p[2], p[3]))
    return out


def up_hit(T, x, y, z):
    """Distance up from (x, y, z) to the first triangle (vertical ray), None if nothing."""
    best = None
    for a, b, c in T:
        # barycentric in xz
        d = (b[2] - c[2]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[2] - c[2])
        if abs(d) < 1e-12:
            continue
        l1 = ((b[2] - c[2]) * (x - c[0]) + (c[0] - b[0]) * (z - c[2])) / d
        l2 = ((c[2] - a[2]) * (x - c[0]) + (a[0] - c[0]) * (z - c[2])) / d
        l3 = 1 - l1 - l2
        if min(l1, l2, l3) < -1e-6:
            continue
        yy = l1 * a[1] + l2 * b[1] + l3 * c[1]
        if yy >= y - 1e-6 and (best is None or yy - y < best):
            best = yy - y
    return best


_ATT = {}


def attach_points(master):
    """Top vertices of a hung prop (local frame), clustered 5 cm."""
    if master in _ATT:
        return _ATT[master]
    l = res1(mlod.read_mlod(master))
    used = set(v[0] for f in l.faces for v in f[0])
    pts = [l.points[i] for i in used]
    top = max(p[1] for p in pts)
    tops = [p for p in pts if p[1] >= top - 0.01]
    cl = []
    for p in tops:
        for c in cl:
            if math.hypot(p[0] - c[0][0], p[2] - c[0][2]) < 0.05:
                c.append(p)
                break
        else:
            cl.append([p])
    out = [(sum(q[0] for q in c) / len(c), top, sum(q[2] for q in c) / len(c)) for c in cl]
    _ATT[master] = out
    return out


def check(path, verbose=True):
    lods = mlod.read_mlod(path)
    l = res1(lods)
    T = tris(l)
    cat = DC.catalog()
    res = []
    for name, o, up, fw in PX.listed(l):
        stem = name.split(":", 1)[1].rsplit(".", 1)[0].replace("\\", "/").split("/")[-1].lower()
        inf = cat.get(stem)
        if not inf or not (inf.get("mount") == "beam" or inf.get("anchor") == "hang"):
            continue
        yaw = math.degrees(math.atan2(fw[0], fw[2]))
        worst = 0.0
        miss = []
        for ax, ay, az in attach_points(inf["master"]):
            m = PX.to_model((ax, ay, az), o, yaw)
            d = up_hit(T, m[0], m[1] - 0.01, m[2])
            gap = None if d is None else d - 0.01
            if gap is None or gap > GAP:
                miss.append((round(m[0], 3), round(m[1], 3), round(m[2], 3), None if gap is None else round(gap, 3)))
            worst = max(worst, 9.9 if gap is None else gap)
        ok = not miss
        res.append((stem, ok, o, miss))
        if verbose:
            print("  %-4s %-28s at (%.2f, %.2f, %.2f)%s" % ("PASS" if ok else "FAIL", stem, o[0], o[1], o[2],
                                                          "" if ok else "  free attach points: %s" % miss))
    return res


def main():
    paths = sys.argv[1:] or sorted(p for p in glob.glob(os.path.join(DEV, "buildings", "furnished", "out", "*.p3d"))
                                   if os.path.basename(p)[3:].split("_")[0] in W2)
    nf = 0
    for p in paths:
        print(os.path.basename(p))
        r = check(p)
        nf += sum(1 for x in r if not x[1])
    print("HANGCHECK: %d failing hung props" % nf)
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
