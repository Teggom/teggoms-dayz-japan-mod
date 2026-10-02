"""FX3 check: the uv pass touched ONLY atlas materials (+ the moss decal).

  python spikes/FX3/uvdiff.py OLD_DIR NEW_DIR      (master folders, matched by relative path)

For every MLOD present in both: same LODs, same faces, same points; every face whose texture is NOT an atlas wood
texture or the moss decal has byte-identical uv (so text decals, cells, stone, roofs ... and the TXT check's inputs
did not move). Prints a summary and exits 1 on any violation.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402

ATLAS = re.compile(r"\\jp_m_(wood_weathered|wood_street_dark|wood_kuro|wood_sooted|wood_bengara|wood_new|wood_silver|"
                   r"wood_interior|ceil_boards|floor_boards_int|floor_boards_rough|decal_moss)_w\d_c[oa]\.paa$", re.I)


def main(old, new):
    files = [os.path.relpath(p, old) for p in glob.glob(os.path.join(old, "**", "*.p3d"), recursive=True)]
    bad, n, nf, nchg, natl = [], 0, 0, 0, 0
    for rel in files:
        pn = os.path.join(new, rel)
        if not os.path.isfile(pn):
            continue
        a, b = mlod.read_mlod(os.path.join(old, rel)), mlod.read_mlod(pn)
        n += 1
        if len(a) != len(b):
            bad.append("%s: LOD count %d -> %d" % (rel, len(a), len(b)))
            continue
        for la, lb in zip(a, b):
            if len(la.faces) != len(lb.faces) or len(la.points) != len(lb.points):
                bad.append("%s LOD %g: faces %d -> %d" % (rel, la.resolution, len(la.faces), len(lb.faces)))
                continue
            for fa, fb in zip(la.faces, lb.faces):
                nf += 1
                if fa[2] != fb[2]:
                    bad.append("%s: texture %s -> %s" % (rel, fa[2], fb[2]))
                    continue
                same = all(va[2] == vb[2] and va[3] == vb[3] for va, vb in zip(fa[0], fb[0]))
                if ATLAS.search(fa[2] or ""):
                    natl += 1
                    nchg += not same
                elif not same:
                    bad.append("%s LOD %g: non-atlas uv moved (%s)" % (rel, la.resolution, fa[2]))
    print("uvdiff %s: %d models, %d faces, %d atlas faces (%d remapped), %d violations" % (
        os.path.basename(new.rstrip("\\/")), n, nf, natl, nchg, len(bad)))
    for l in bad[:15]:
        print("  " + l)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
