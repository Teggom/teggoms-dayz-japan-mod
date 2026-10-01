"""FB1: the bindcheck rules (B1 class == Land_<p3d stem>, B2 Geometry class=house) on jp_site's Land_ classes
(the wells and FP1's climbable fire-watch ladder). Read-only.  python spikes/FB1/sitebind.py"""
import os
import re
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
t = open(os.path.join(DEV, "src", "JP", "site", "config.cpp"), "rb").read().decode("utf-8")
bad = n = 0
for m in re.finditer(r'class (Land_\w+)\s*:\s*\w+\s*\{[^}]*?model\s*=\s*"([^"]+)"', t, re.S):
    cls, mp = m.group(1), m.group(2)
    rel = mp.lstrip("\\").replace("\\", os.sep)
    stem = os.path.splitext(os.path.basename(rel))[0]
    data = open(os.path.join(DEV, "src", rel), "rb").read()
    ok1 = cls.lower() == ("land_" + stem).lower()
    ok2 = b"class\x00house\x00" in data.lower()
    n += 1
    bad += not (ok1 and ok2)
    print("%-4s %-45s %s.p3d class=house %s" % ("OK" if ok1 and ok2 else "FAIL", cls, stem, ok2))
print("sitebind: %d Land_ classes, %d fail" % (n, bad))
sys.exit(1 if bad else 0)
