"""FP1 finding 8: where do the loom / wheel proxies sit in the furnished houses, against the Res 1 floor under them?
python spikes/FP1/proxyfloor.py <name substring> ...   (reads buildings/furnished/out/*.p3d, read-only)"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402


def floor_under(l, x, z, y0):
    best = []
    for fv, fl, tex, mat in l.faces:
        ps = [l.points[v[0]] for v in fv]
        ys = [p[1] for p in ps]
        if max(ys) - min(ys) > 0.005 or ys[0] > y0 + 0.3 or ys[0] < y0 - 1.0:
            continue
        xs = [p[0] for p in ps]
        zs = [p[2] for p in ps]
        if min(xs) <= x <= max(xs) and min(zs) <= z <= max(zs):
            best.append((round(ys[0], 3), os.path.basename(tex)[:36]))
    return sorted(set(best))[-3:]


def main(keys):
    for f in sorted(glob.glob(os.path.join(DEV, "buildings", "furnished", "out", "*.p3d"))):
        l = mlod.read_mlod(f)[0]
        for name, (pw, fs) in l.selections.items():
            if not name.lower().startswith("proxy") or not any(k in name for k in keys):
                continue
            for fi in sorted(fs):
                o = l.points[l.faces[fi][0][0][0]]
                print("%-40s %-34s origin (%.2f %.3f %.2f) floor %s" % (
                    os.path.basename(f)[:40], name.split("\\")[-1][:34], o[0], o[1], o[2], floor_under(l, o[0], o[2], o[1])))


if __name__ == "__main__":
    main(sys.argv[1:])
