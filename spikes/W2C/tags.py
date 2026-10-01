"""W2C: faces per tag in R1 / R2 / R3 of one civic shell. python spikes/W2C/tags.py kind '{params}'"""
import json, os, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings")); sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import civickit
M, fl, ro = civickit.model(kind=sys.argv[1], **json.loads(sys.argv[2]))
lods = M.lods(geo_props={"class": "house", "map": "house", "damage": "no", "autocenter": "0"}, mass=1000.0)
from jpparts import mlod
print({mlod.lod_name(l.resolution): len(l.faces) for l in lods})
for r in (1, 2, 3):
    t = {}
    for s in M.solids:
        if r in s.vis:
            t[s.tag] = t.get(s.tag, 0) + len(s.faces)
    print("R%d" % r, ", ".join("%s %d" % kv for kv in sorted(t.items(), key=lambda kv: -kv[1])[:16]))
