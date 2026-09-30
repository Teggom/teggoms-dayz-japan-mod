"""List the MLOD masters that differ from the pre-F1 snapshot (spikes/F1/_before/<area>).
  python spikes/F1/diffmasters.py B3a B3b L1 L2"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))


def h(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


for area in sys.argv[1:] or ["B3a", "B3b", "L1", "L2"]:
    a = os.path.join(HERE, "_before", area)
    b = os.path.join(DEV, "spikes", area, "out")
    ch = []
    for r, _, fs in os.walk(b):
        for f in fs:
            p = os.path.join(r, f)
            rel = os.path.relpath(p, b)
            q = os.path.join(a, rel)
            if not os.path.exists(q):
                ch.append(rel.replace(os.sep, "/") + " (NEW)")
            elif h(p) != h(q):
                ch.append(rel.replace(os.sep, "/"))
    print("%s: %d changed" % (area, len(ch)))
    for c in sorted(ch):
        print("  ", c)
