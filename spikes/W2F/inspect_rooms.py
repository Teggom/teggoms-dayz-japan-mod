"""W2F: print rooms (rect, level, tag, doors) + fittings + memory points of the W2S / W2C shells (rooms json).
  python spikes/W2F/inspect_rooms.py [family ...]"""
import glob
import json
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
fams = sys.argv[1:] or ["shrine", "temple", "teahouse", "smithy", "guardhut", "kido"]
for fam in fams:
    for p in sorted(glob.glob(os.path.join(DEV, "buildings", fam, "rooms", "*.json"))):
        with open(p, "rb") as f:
            d = json.loads(f.read().decode("utf-8"))
        print("=== %s  loot %s %s" % (os.path.basename(p)[:-5], d.get("loot_points"), d.get("loot_by_room")))
        for k in ("memory_points", "fittings", "info"):
            if k in d:
                print("   ", k, json.dumps(d[k])[:600])
        for r in d["rooms"]:
            rm = [round(v, 2) for v in r["rect_model"]]
            print("  room %-12s %-10s y %.2f rect %s doors %s %s" % (r["name"], r.get("tag"), r["level_m"], rm,
                                                                 r.get("doors"), "" if r.get("enclosed", True) else "open"))
            for ft in r.get("fittings", []):
                g = {k: v for k, v in ft.items() if k not in ("room", "note")}
                print("      fit %-14s %s | %s" % (ft["kind"], json.dumps(g), ft.get("note", "")[:90]))
