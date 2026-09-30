"""C2 test-island hamlet: a small farming hamlet in the free west part of the flat yard (README "The test island"),
clear of the machiya + yard, the toilet, C1's test street (z 1062-1098), the sakura, the swatch wall and the grid.

  python spikes/C2/layout.py     -> prints C2_PLACEMENTS for buildings/registry.py + world boxes, checks overlaps
                                    against each other and against every object already on the island

Plan: a north-south lane along x = 952 is implied by the gaps; the two farmhouses face south onto a threshing yard
(z ~1012-1020), the huts face north across it, the sheds stand behind the farmhouses. yaw: clockwise from north,
model +z (the front) points to yaw.
"""
import csv
import glob
import json
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))
import registry  # noqa: E402
import ruralkit  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

Y = 25.0
HAMLET = [
    # key, (x, z) centre, yaw, note
    ("farmhouse_kanto_yosemune_umaya", (942.0, 1029.0), 180.0, "Kanto farmhouse, front south onto the yard"),
    ("farmhouse_kinai_kirizuma_tile_takahe", (963.5, 1028.0), 180.0, "Kinai farmhouse, front south onto the yard"),
    ("hut_east_s_earth_mushiro", (933.5, 1003.0), 0.0, "hut east (small, earth floor), front north"),
    ("hut_west_thatch_leanl", (947.0, 1003.0), 0.0, "hut west (thatch, lean-to), front north"),
    ("hut_east_l_board", (962.5, 1002.5), 0.0, "hut east (large, board floor), front north"),
    ("shed_open_thatch", (941.0, 1045.5), 180.0, "open shed behind the Kanto farmhouse"),
    ("shed_walled_ishioki_woodshed", (962.0, 1045.5), 180.0, "walled shed with woodshed lean-to behind the Kinai house"),
]


def main():
    boxes = []
    for key, (x, z), yaw, note in HAMLET:
        b = registry.get(key)
        M, _, _ = ruralkit.model(name=b["name"], **b["params"])
        bb = M.bbox()
        cs = [bloot.model_to_world((xx, 0.0, zz), (x, Y, z), yaw) for xx in (bb[0], bb[1]) for zz in (bb[4], bb[5])]
        boxes.append((key, min(c[0] for c in cs), max(c[0] for c in cs), min(c[2] for c in cs), max(c[2] for c in cs)))
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        for r in csv.DictReader(open(p)):
            if os.path.basename(p) == "C.csv" and any(k in r["p3d"] for k in ("farmhouse", "\\hut\\", "\\shed\\")):
                continue
            others.append((r["p3d"], float(r["x"]), float(r["z"])))
    for p in glob.glob(os.path.join(DEV, "test", "spawns", "*.json")):
        for o in json.load(open(p)).get("Objects", []):
            others.append((o["name"], o["pos"][0], o["pos"][2]))
    reserved = {"sakura W": (980, 990, 1005, 1015), "C1 street": (978, 1068, 1062, 1098),
                "machiya": (1014, 1034, 1036, 1062), "item grid": (998, 1052, 966, 978), "spawn": (1019, 1029, 980, 990)}
    bad = []
    for k, x0, x1, z0, z1 in boxes:
        for n, x, z in others:
            if x0 - 3 < x < x1 + 3 and z0 - 3 < z < z1 + 3:
                bad.append((k, n, x, z))
        for n, (a0, a1, c0, c1) in reserved.items():
            if x0 < a1 and x1 > a0 and z0 < c1 and z1 > c0:
                bad.append((k, "reserved " + n))
        if not (926 < x0 and x1 < 1122 and 926 < z0 and z1 < 1122):
            bad.append((k, "outside the flat yard"))
    for i, a in enumerate(boxes):
        for b_ in boxes[i + 1:]:
            if min(a[2], b_[2]) - max(a[1], b_[1]) > -1.5 and min(a[4], b_[4]) - max(a[3], b_[3]) > -1.5:
                bad.append(("too close", a[0], b_[0]))
    print("C2_PLACEMENTS = {")
    for key, (x, z), yaw, note in HAMLET:
        print('    "%s": [{"pos": (%.3f, %.1f, %.3f), "yaw": %.1f, "where": "test island: C2 hamlet (west yard), %s"}],'
              % (key, x, Y, z, yaw, note))
    print("}")
    for b_ in boxes:
        print("  %-40s x %.1f-%.1f  z %.1f-%.1f" % b_)
    print("PROBLEMS:", bad if bad else "none")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
