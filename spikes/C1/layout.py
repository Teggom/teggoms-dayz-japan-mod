"""C1 test-island layout: the test street north of the machiya (README "The test island": free ground in the yard).

  python spikes/C1/layout.py      -> prints C1_PLACEMENTS for buildings/registry.py + the world boxes, and checks them
                                     against every object already on the island (test/placements, test/spawns)

Street (east-west) along z = 1080: the north side faces south (yaw 180, model +z -> world -z), the south side faces
north (yaw 0). Street view from the street: a unit's street-view RIGHT is its kit low-x side. North side (yaw 180):
model +x -> world -x, so street-view right = east. South side (yaw 0): street-view right = west.
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
import shellkit  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

Y = 25.0
Z_N, Z_S = 1084.0, 1076.0          # street wall lines of the north / south side
# rows listed from the street-view RIGHT to LEFT (kit +x order); (key, gap_before_m)
NORTH_KAMIGATA = ([("th_kamigata_3k_cornerr_torir", 0), ("th_kamigata_3k_middle_toril", 0),
                   ("th_kamigata_2k_middle_torir", 0), ("th_kamigata_3k_endl_toril", 0)], 1006.0)
NORTH_EDO = ([("th_edo_3k_cornerr_toril", 0), ("th_edo_2k_middle_torir", 0), ("th_edo_3k_middle_toril_board", 0),
              ("th_edo_2k_endl_torir", 0)], 1062.0)
# south side, street-view right (= west) first
SOUTH = ([("pt_det_tile_nuriya", 0), ("pt_row_middle", 3.0), ("pt_row_endl", 0), ("inn_std_tile", 3.0),
          ("inn_grand", 4.0)], 986.0)


def unit(key):
    b = registry.get(key)
    M, floors, rooms = shellkit.model(name=b["name"], **b["params"])
    info = shellkit.INFO
    return b, M, info["lot_width"], (info["DO"] + info["DG"]) / 2


def place_row(row, x_start, z_wall, yaw):
    """Lot line to lot line from x_start: north side (yaw 180) runs west from the EAST end x_start, south side (yaw 0)
    runs east from the WEST end x_start."""
    out = []
    x = x_start
    sgn = -1.0 if yaw == 180.0 else 1.0
    for key, gap in row:
        b, M, lw, half_d = unit(key)
        x += sgn * gap
        cx = x + sgn * lw / 2
        # model origin = lot centre at grade; the street wall line is model z = +half_d
        cz = z_wall + half_d if yaw == 180.0 else z_wall - half_d
        out.append((key, (round(cx, 3), Y, round(cz, 3)), yaw, M))
        x += sgn * lw
    return out


def main():
    pl = []
    pl += place_row(NORTH_KAMIGATA[0], NORTH_KAMIGATA[1], Z_N, 180.0)
    pl += place_row(NORTH_EDO[0], NORTH_EDO[1], Z_N, 180.0)
    pl += place_row(SOUTH[0], SOUTH[1], Z_S, 0.0)
    boxes = []
    for key, pos, yaw, M in pl:
        bb = M.bbox()
        cs = [bloot.model_to_world((x, 0.0, z), pos, yaw) for x in (bb[0], bb[1]) for z in (bb[4], bb[5])]
        boxes.append((key, min(c[0] for c in cs), max(c[0] for c in cs), min(c[2] for c in cs), max(c[2] for c in cs)))
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if p.endswith("C.csv"):
            continue
        for r in csv.DictReader(open(p)):
            others.append((r["p3d"], float(r["x"]), float(r["z"])))
    for p in glob.glob(os.path.join(DEV, "test", "spawns", "*.json")):
        for o in json.load(open(p)).get("Objects", []):
            others.append((o["name"], o["pos"][0], o["pos"][2]))
    # the machiya shop + yard objects (C.csv minus our own rows)
    others += [("machiya shop + yard", x, z) for x in (1014.0, 1034.0) for z in (1036.0, 1062.0)]
    bad = []
    for k, x0, x1, z0, z1 in boxes:
        for n, x, z in others:
            if x0 - 3 < x < x1 + 3 and z0 - 3 < z < z1 + 3:
                bad.append((k, n, x, z))
        if not (930 < x0 and x1 < 1118 and 930 < z0 and z1 < 1118):
            bad.append((k, "outside the flat yard"))
    # C1 rows may touch lot line to lot line; different rows / buildings must not overlap
    for i, a in enumerate(boxes):
        for b_ in boxes[i + 1:]:
            ov = min(a[2], b_[2]) - max(a[1], b_[1]), min(a[4], b_[4]) - max(a[3], b_[3])
            if ov[0] > 0.8 and ov[1] > 0.8:
                bad.append(("overlap", a[0], b_[0], ov))
    print("C1_PLACEMENTS = {")
    for key, pos, yaw, M in pl:
        side = "north side, front facing south" if yaw == 180.0 else "south side, front facing north"
        print('    "%s": [{"pos": (%.3f, %.1f, %.3f), "yaw": %.1f, "where": "test island: C1 test street z 1080, %s"}],'
              % (key, pos[0], pos[1], pos[2], yaw, side))
    print("}")
    for b_ in boxes:
        print("  %-32s x %.1f-%.1f  z %.1f-%.1f" % b_)
    print("PROBLEMS:", bad if bad else "none")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
