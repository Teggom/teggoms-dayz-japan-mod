"""FX1 probe: Geometry components (bbox) of a building MLOD inside a model-frame box.
  python spikes/FX1/probe_geo.py <mlod.p3d> x0 x1 z0 z1 [y0 y1] [lod]
lod default Geometry (also 'Roadway', 'View Geometry', or a resolution number like 1)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402


def comps(l):
    out = []
    for name in l.selections:
        if name.lower().startswith("component"):
            out.append(name)
    return out


def main():
    a = sys.argv[1:]
    path = a[0]
    x0, x1, z0, z1 = map(float, a[1:5])
    y0, y1 = (float(a[5]), float(a[6])) if len(a) > 6 else (-99, 99)
    want = a[7] if len(a) > 7 else "Geometry"
    for l in mlod.read_mlod(path):
        nm = mlod.lod_name(l.resolution)
        if nm != want and str(l.resolution) != want:
            continue
        sels = l.selections
        for name in sorted(sels):
            if want == "Geometry" and not name.lower().startswith("component"):
                continue
            idx = [i for i, w in sels[name][0].items() if w > 0]
            if not idx:
                continue
            pts = [l.points[i] for i in idx]
            bx = (min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts),
                  min(p[2] for p in pts), max(p[2] for p in pts))
            if bx[1] < x0 or bx[0] > x1 or bx[5] < z0 or bx[4] > z1 or bx[3] < y0 or bx[2] > y1:
                continue
            print("%-16s x %.3f..%.3f y %.3f..%.3f z %.3f..%.3f" % ((name,) + bx))


if __name__ == "__main__":
    main()
