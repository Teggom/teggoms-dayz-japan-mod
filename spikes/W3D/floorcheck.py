"""W3D floor-vs-terrain check: no room floor of a placed W3D building has the terrain poking through it.

For every building row of test/placements/W3D.csv: its rooms (buildings/<dir>/rooms/<key>.json, rect_model + level_m)
are sampled on a 0.4 m grid, each sample taken to the world (layout_w2f.to_world) and the terrain height there compared
with the floor: a room FAILS where the terrain stands above (seat + floor level - 0.01). Open rooms / yards included.

  python spikes/W3D/floorcheck.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "SH1"),
          os.path.join(DEV, "spikes", "W2F"), os.path.join(DEV, "spikes", "W3C1"), HERE):
    sys.path.insert(0, p)
import terrain_sh1 as T  # noqa: E402
import layout_w2f as LW  # noqa: E402
import layout_w3c1 as L1  # noqa: E402
import layout_w3d as L3  # noqa: E402


def main():
    items = {i["id"]: i for i in json.load(open(L3.ITEMS, encoding="utf-8"))}
    bad = 0
    for bid, key, x, z, yaw, label in L3.BUILDINGS:
        it = items[bid]
        r = L1.rec(key)
        base = T.ground(x, z) + it["y_off"]
        rooms = json.load(open(os.path.join(DEV, "buildings", r["model_dir"], "rooms", key + ".json"),
                               encoding="utf-8"))["rooms"]
        worst = []
        for rm in rooms:
            x0, x1, z0, z1 = rm["rect_model"]
            lvl = rm["level_m"]
            m = -9.0
            n = max(1, int((x1 - x0) / 0.4))
            k = max(1, int((z1 - z0) / 0.4))
            for i in range(n + 1):
                for j in range(k + 1):
                    wx, wz = LW.to_world(x0 + (x1 - x0) * i / n, z0 + (z1 - z0) * j / k, (x, 25.0, z), yaw)
                    m = max(m, T.ground(wx, wz) - base - lvl)
            if m > -0.01:
                worst.append("%s %+.2f" % (rm["name"], m))
        print("%-4s %-28s %s" % (bid, key, "FAIL terrain through " + ", ".join(worst) if worst else "ok"))
        bad += bool(worst)
    print("FLOORCHECK: %d buildings, %d with terrain through a floor" % (len(L3.BUILDINGS), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
