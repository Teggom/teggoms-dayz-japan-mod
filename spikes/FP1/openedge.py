"""FP1 open-edge check (finding 6, the see-through bale ends): in every visual LOD of every MLOD master, the faces
whose texture matches PATTERN must form closed surfaces: an edge (keyed by its two end positions, 0.1 mm) used by
exactly one such face is an open boundary, i.e. a hole the player can see through (single-sided faces).

  python spikes/FP1/openedge.py [--pat REGEX] <p3d or folder> ...      prints per model / LOD: open edges, length
Exit 1 if any model has open edges. Default pattern: straw_tawara|straw_mushiro (bales, sacks).
"""
import glob
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402


def key(p):
    return (round(p[0], 4), round(p[1], 4), round(p[2], 4))


def open_edges(lod, pat):
    cnt = {}
    for fv, fl, tex, mat in lod.faces:
        if not re.search(pat, tex):
            continue
        ps = [key(lod.points[v[0]]) for v in fv]
        for i in range(len(ps)):
            a, b = ps[i], ps[(i + 1) % len(ps)]
            if a == b:
                continue
            e = (a, b) if a < b else (b, a)
            cnt[e] = cnt.get(e, 0) + 1
    edges = [e for e, n in cnt.items() if n == 1]
    return edges, sum(math.dist(a, b) for a, b in edges)


def check_file(p, pat):
    out = []
    for lod in mlod.read_mlod(p):
        if lod.resolution >= 1000:
            continue
        edges, L = open_edges(lod, pat)
        if edges:
            out.append((lod.resolution, len(edges), L, edges[:3]))
    return out


def main(argv):
    pat = r"straw_tawara|straw_mushiro"
    if argv and argv[0] == "--pat":
        pat, argv = argv[1], argv[2:]
    files = []
    for a in argv:
        files += sorted(glob.glob(os.path.join(a, "**", "*.p3d"), recursive=True)) if os.path.isdir(a) else [a]
    bad = 0
    for f in files:
        if open(f, "rb").read(4) != b"MLOD":
            continue
        res = check_file(f, pat)
        if res:
            bad += 1
            print("OPEN %-48s %s" % (os.path.basename(f), "; ".join("R%g: %d edges %.2f m" % r[:3] for r in res)))
    print("files %d, with open %s edges: %d" % (len(files), pat, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
