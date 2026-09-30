"""C2 quick try: build rural shells in memory, print faces per LOD, bbox, rooms, and the budget verdict.

  python spikes/C2/try_rural.py kanto '{"stable": true}' ...
"""
import json
import os
import sys
import time

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import ruralkit  # noqa: E402
from jpparts import mlod  # noqa: E402
from jpparts.templates import rural  # noqa: E402

BUD = {"standard": (6000, 2300, 800), "large": (12000, 4600, 1600), "small": (3000, 1150, 400)}


def one(kind, params):
    t0 = time.time()
    M, floors, rooms = ruralkit.model(kind=kind, **params)
    lods = M.lods(geo_props={"class": "house", "map": "house", "damage": "no", "autocenter": "0"}, mass=20000.0)
    f = {mlod.lod_name(l.resolution): len(l.faces) for l in lods}
    b = BUD[rural.budget_class(kind)]
    got = (f.get("Resolution 1", 0), f.get("Resolution 2", 0), f.get("Resolution 3", 0))
    ok = all(g <= m for g, m in zip(got, b))
    bb = M.bbox()
    print("%s %s: R %s / budget %s %s | geo %d | doors %d | bbox x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f | %.1fs" % (
        kind, json.dumps(params), got, b, "OK" if ok else "OVER", f.get("Geometry", 0), len(M.doors), bb[0], bb[1],
        bb[2], bb[3], bb[4], bb[5], time.time() - t0))
    tags = {}
    for s in M.solids:
        if 1 in s.vis:
            tags[s.tag] = tags.get(s.tag, 0) + len(s.faces)
    top = sorted(tags.items(), key=lambda kv: -kv[1])[:14]
    print("   R1 by tag:", ", ".join("%s %d" % kv for kv in top))
    tags3 = {}
    for s in M.solids:
        if 3 in s.vis:
            tags3[s.tag] = tags3.get(s.tag, 0) + len(s.faces)
    print("   R3 by tag:", ", ".join("%s %d" % kv for kv in sorted(tags3.items(), key=lambda kv: -kv[1])[:10]))
    return M


if __name__ == "__main__":
    a = sys.argv[1:]
    for i in range(0, len(a), 2):
        one(a[i], json.loads(a[i + 1]) if i + 1 < len(a) else {})
