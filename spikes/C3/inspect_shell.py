"""Print what a decorator needs to know about a registry shell (model frame): rooms (rect, level, tag, doors), the doors'
clear openings (wall line, interval), passages, portals, fittings, floor obstacles, stairs, bbox.
  python spikes/C3/inspect_shell.py key [key ...]
"""
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    sys.path.insert(0, p)
import registry  # noqa: E402
import pipeline  # noqa: E402
from jpparts import mlod, checks as C, decor as DC  # noqa: E402


def r2(v):
    return [round(x, 2) for x in v]


for key in sys.argv[1:]:
    b = registry.get(key)
    mod = pipeline.load_module(b)
    M, floors, rooms = mod.model(name=b["name"], **b["params"]) if "params" in b else mod.model()
    lods = M.lods(geo_props=pipeline.GEO_PROPS, mass=b["mass"])
    L = {mlod.lod_name(l.resolution): l for l in lods}
    g = C.components(L["Geometry"])
    print("=== %s (%s) bbox %s faces R1 %d" % (key, b["class"], r2(M.bbox()), len(L["Resolution 1"].faces)))
    for k, d in enumerate(M.doors, 1):
        o = DC.door_opening(d, g)
        s = ""
        if o:
            ax, (lo, hi), wall = o
            s = ("wall z=%.2f x %.2f..%.2f" % (wall, lo, hi)) if ax else ("wall x=%.2f z %.2f..%.2f" % (wall, lo, hi))
        print("  DoorsTwin%d %-34s pass=%s %s" % (k, getattr(d, "label", ""), getattr(d, "passable", True), s))
    for r in rooms:
        print("  room %-12s %-14s y %.2f rect %s doors %s" % (r["name"], r["tag"], r["level_m"], r2(r["rect_model"]),
                                                            r.get("doors")))
        for f in r.get("fittings", []):
            print("      fitting", {k: v for k, v in f.items() if k != "note"})
    for f in floors:
        print("  floor %-12s y %.2f obst %s" % (f["name"], f["y"], [r2(o) for o in f["obstacles"]]))
    for nm in ("PASSAGES", "STAIRS"):
        v = getattr(mod, nm, None)
        if v:
            print("  %s %s" % (nm, v))
    for n, bx in getattr(mod, "PORTALS", []):
        print("  portal %s %s" % (n, r2(bx)))
    info = getattr(mod, "INFO", {})
    if info.get("levels"):
        print("  levels", info["levels"])
