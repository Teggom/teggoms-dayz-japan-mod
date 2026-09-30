"""Face count per solid tag and LOD for a kura (or any kit Part): python spikes/C3/facetags.py '{...kura params}'"""
import json
import os
import sys
from collections import Counter

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import kura  # noqa: E402

params = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
M, floors, rooms, info = kura.model(**params)
for lod in (1, 2, 3):
    c = Counter()
    for s in M.solids:
        if lod in s.vis:
            c[s.tag] += len(s.faces)
    print("R%d" % lod, sum(c.values()), c.most_common(18))
