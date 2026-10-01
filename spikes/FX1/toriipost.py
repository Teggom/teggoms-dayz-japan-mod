"""FX1: after the torii rescale, where do the placed torii's posts land? Every placed walk-through torii's two post
feet (new span) vs every other placed object's origin within 0.9 m, and vs the terrain step under each foot.
  python spikes/FX1/toriipost.py"""
import csv
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "SH1"))
import terrain_sh1 as T  # noqa: E402

SPAN = {"shinmei": 1.82 * 1.35, "myojin": 2.73 * 1.17, "stone_s": 1.82 * 1.52, "stone_m": 2.50 * 1.45}
OLD = {"shinmei": 1.82, "myojin": 2.73, "stone_s": 1.82, "stone_m": 2.50}


def kind(b):
    if "fallen" in b or "mini" in b:
        return None
    for k in ("shinmei", "rotted"):
        if k in b:
            return "shinmei"
    if "myojin" in b or "leaning" in b:
        return "myojin"
    for k in ("stone_s", "stone_m"):
        if k in b:
            return k
    return None


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(DEV, "test", "placements", "*.csv"))):
        with open(p, newline="") as f:
            for r in csv.DictReader(f):
                rows.append((os.path.basename(p), os.path.basename(r["p3d"].replace("\\", "/")).lower(),
                             float(r["x"]), float(r["z"]), float(r["yaw_deg"]), float(r["y_offset"])))
    n = 0
    for src, b, x, z, yaw, yo in rows:
        k = kind(b) if "torii" in b else None
        if not k:
            continue
        a = math.radians(yaw)
        feet = []
        for sx in (-1, 1):
            px = x + sx * SPAN[k] / 2 * math.cos(a)
            pz = z - sx * SPAN[k] / 2 * math.sin(a)
            feet.append(T.ground(px, pz))
            for s2, b2, x2, z2, _, _ in rows:
                if (x2, z2) == (x, z):
                    continue
                d = math.hypot(x2 - px, z2 - pz)
                if d < 0.9:
                    n += 1
                    print("NEAR %s %s foot (%.2f, %.2f): %.2f m from %s %s" % (src, b, px, pz, d, s2, b2))
        base = T.ground(x, z) + yo
        print("%-6s %-40s span %.2f -> %.2f  feet ground %.2f / %.2f vs base %.2f" % (src, b, OLD[k], SPAN[k],
                                                                                     feet[0], feet[1], base))
    print("toriipost: %d feet within 0.9 m of another object" % n)


if __name__ == "__main__":
    main()
