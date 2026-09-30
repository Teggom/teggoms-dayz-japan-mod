"""C1: face breakdown per sub-part (Solid.src) and tag for a template build, LOD 1 and 3."""
import collections
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jpparts.templates import townhouse  # noqa: E402
import smoke  # noqa: E402,F401  (prints its cases too)

kw = smoke.CASES[sys.argv[1]]
H, info = townhouse.build(**kw)
for lod in (1, 3):
    c = collections.Counter()
    for s in H.solids:
        if lod in s.vis:
            s.finalize()
            c[(getattr(s, "src", "") or "")[:28] + " / " + s.tag] += len(s.faces)
    print("LOD", lod, sum(c.values()))
    for k, v in c.most_common(25):
        print("  %6d %s" % (v, k))
