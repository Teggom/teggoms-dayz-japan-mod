"""FX1 handle check: every fitting of a hinged double door (ring pulls, pull boards, hinge straps) lies ON its own
leaf (inside that leaf's collision box in x and y, touching one of its broad faces) and moves with it (same door bone);
hinge straps start at the leaf's hinge edge, pulls sit in the free half.

  python spikes/FX1/handlecheck.py        (tobira variants + the kido / temple-gate leaf pairs)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import tobira as TB, gates as G  # noqa: E402

if "--head" in sys.argv:
    # the committed (pre-FX1) tobira.py / gates.py, loaded against the current kit: the 'before' numbers
    import subprocess
    import types

    def _head(mod):
        src = subprocess.run(["git", "show", "HEAD:parts/kit/jpparts/%s.py" % mod], cwd=DEV, capture_output=True,
                             check=True).stdout.decode("utf-8")
        for rel in ("core", "shapes", "openings"):
            src = src.replace("from .%s import" % rel, "from jpparts.%s import" % rel)
            src = src.replace("from .core import LIBRARY", "from jpparts.core import LIBRARY")
        m = types.ModuleType("head_" + mod)
        exec(compile(src, "HEAD:" + mod, "exec"), m.__dict__)
        return m
    TB, G = _head("tobira"), _head("gates")

FIT = {"ring_pull": "pull", "hikite_ita": "pull", "hasso": "hinge", "hinge": "hinge"}
LEAF = ("leaf", "gate_leaf_geo")


def bb(s):
    xs = [v[0] for v in s.verts]
    ys = [v[1] for v in s.verts]
    zs = [v[2] for v in s.verts]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


def check(p, label):
    fails = []
    leaves = {}
    for s in p.solids:
        if getattr(s, "door", None) and s.tag in LEAF:
            leaves[s.door] = bb(s)
    axes = {b: p.memory.get(b + "_axis") for b in leaves}
    n = 0
    for s in p.solids:
        kind = FIT.get(s.tag)
        if not kind:
            continue
        n += 1
        b = bb(s)
        bone = getattr(s, "door", None)
        if bone not in leaves:
            fails.append("%s %s not in a leaf bone" % (label, s.tag))
            continue
        L = leaves[bone]
        if b[0] < L[0] - 1e-4 or b[1] > L[1] + 1e-4 or b[2] < L[2] - 1e-4 or b[3] > L[3] + 1e-4:
            fails.append("%s %s x %.3f..%.3f outside its leaf x %.3f..%.3f" % (label, s.tag, b[0], b[1], L[0], L[1]))
        # touching: some other solid of the same leaf meets it face to face (or it is inside the leaf's box)
        touch = 9.9
        for q in p.solids:
            if q is s or getattr(q, "door", None) != bone or q.tag in LEAF:
                continue
            c = bb(q)
            if c[1] < b[0] or c[0] > b[1] or c[3] < b[2] or c[2] > b[3]:
                continue
            touch = min(touch, abs(b[4] - c[5]), abs(b[5] - c[4]), 0.0 if (b[4] < c[5] and b[5] > c[4]) else 9.9)
        inside = b[4] >= L[4] - 1e-4 and b[5] <= L[5] + 1e-4
        if touch > 0.0025 and not inside:
            fails.append("%s %s floats %.3f m off its leaf face" % (label, s.tag, touch))
        hx = axes[bone][0][0] if axes.get(bone) else None
        if hx is not None:
            cx = (b[0] + b[1]) / 2
            far = L[1] - L[0]
            d = abs(cx - hx)
            if kind == "pull" and d < far / 2:
                fails.append("%s %s in the hinge half of its leaf" % (label, s.tag))
            if kind == "hinge" and min(abs(b[0] - hx), abs(b[1] - hx)) > 0.06:
                fails.append("%s %s not at the hinge edge (%.3f from the axis)" % (label, s.tag,
                                                                                   min(abs(b[0] - hx), abs(b[1] - hx))))
    return n, fails


def main():
    allf = []
    tot = 0
    for v in TB.VARIANTS:
        if not TB.VARIANTS[v][2]:
            continue                                    # the static ajar dressing has no bones
        p = TB.part_tobira(v)
        n, f = check(p, "tobira%s" % v)
        tot += n
        allf += f
        print("%-24s fittings %2d  %s" % ("tobira" + v, n, "PASS" if not f else "FAIL"))
    for v in ("_lattice", "_board"):
        p = G.gate_leaves(v, 1.5 * 1.82)
        n, f = check(p, "gate%s" % v)
        tot += n
        allf += f
        print("%-24s fittings %2d  %s" % ("gate" + v, n, "PASS" if not f else "FAIL"))
    for f in allf:
        print("  " + f)
    print("HANDLECHECK: %d fittings, %d failures" % (tot, len(allf)))
    return 1 if allf else 0


if __name__ == "__main__":
    sys.exit(main())
