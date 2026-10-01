"""FX1 probe: the front stair (kizahashi) + en of a building MLOD, from its Roadway LOD.
  python spikes/FX1/probe_front.py <mlod.p3d> [zmin]
Prints every Roadway face whose centre z > zmin (default 1.0): x range, y range, z range."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402


def main():
    path = sys.argv[1]
    zmin = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    for l in mlod.read_mlod(path):
        if mlod.lod_name(l.resolution) != "Roadway":
            continue
        rows = []
        for verts, _, _, _ in l.faces:
            pts = [l.points[v[0]] for v in verts]
            cz = sum(p[2] for p in pts) / len(pts)
            if cz < zmin:
                continue
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            zs = [p[2] for p in pts]
            rows.append((min(zs), max(zs), min(xs), max(xs), min(ys), max(ys)))
        for r in sorted(set(tuple(round(v, 3) for v in r) for r in rows)):
            print("z %.3f..%.3f  x %.3f..%.3f  y %.3f..%.3f" % r)


if __name__ == "__main__":
    main()
