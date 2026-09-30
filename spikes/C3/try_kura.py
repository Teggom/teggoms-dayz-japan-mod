"""Quick look at a kura shell without the pipeline: faces per LOD, doors, rooms.
  python spikes/C3/try_kura.py '{"lower": "shitami", "door": "_hinged"}'
"""
import json
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import kura  # noqa: E402
from jpparts import mlod  # noqa: E402

params = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
M, floors, rooms, info = kura.model(**params)
lods = M.lods(geo_props={"class": "house", "map": "house", "damage": "no", "autocenter": "0"}, mass=20000.0)
print({mlod.lod_name(l.resolution): len(l.faces) for l in lods})
for d in M.doors:
    print("door", getattr(d, "label", ""), d.twin, [a["bone"] + ":" + a["type"] for a in d.anims])
for r in rooms:
    print("room", r["name"], r["tag"], r["rect_model"], r["level_m"], r["doors"])
for f in floors:
    print("floor", f["name"], f["y"], [tuple(round(v, 2) for v in o) for o in f["obstacles"]])
print("portals", len(info["portals_model"]), "stair", info["stair_model"])
print("bbox", [round(v, 2) for v in M.bbox()])
