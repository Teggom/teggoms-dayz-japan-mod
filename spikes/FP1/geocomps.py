"""print the Geometry components' bboxes of an MLOD (FP1 diagnostics)"""
import os
import sys
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402
for f in sys.argv[1:]:
    g = [l for l in mlod.read_mlod(f) if abs(l.resolution - 1e13) < 1e7][0]
    for n, (pw, fs) in sorted(g.selections.items()):
        if n.lower().startswith("component"):
            ps = [g.points[i] for i in pw]
            print(os.path.basename(f)[:30], n, " ".join("%.2f..%.2f" % (min(p[k] for p in ps), max(p[k] for p in ps)) for k in range(3)))
