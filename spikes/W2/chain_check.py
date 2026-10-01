#!/usr/bin/env python3
"""chain_check.py - C7 across module joins: chains stone-step modules by their sidecar connectors (each module's
stair_foot placed on the previous one's stair_head) and checks, from the written MLOD Roadway LODs, that every join
edge coincides (same y and z, same x span within 2 mm) and every ramp is <= 38 deg."""
import json
import math
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402

SC = json.load(open(os.path.join(DEV, "src", "JP", "site", "shrine", "jp_s_stone_steps.prop.json"), "rb"))
MOD = {os.path.basename(m["p3d"])[:-4]: m for m in SC["models"]}
CHAINS = [
    ["jp_s_stone_steps_dressed_6", "jp_s_stone_steps_landing", "jp_s_stone_steps_dressed_3", "jp_s_stone_steps_dressed_6"],
    ["jp_s_stone_steps_rough_3", "jp_s_stone_steps_rough_3", "jp_s_stone_steps_landing", "jp_s_stone_steps_ab_heaved"],
    ["jp_s_stone_steps_dressed_3_wide", "jp_s_stone_steps_landing_wide", "jp_s_stone_steps_dressed_6_wide"],
    ["jp_s_stone_steps_dressed_3_narrow", "jp_s_stone_steps_rough_3_narrow", "jp_s_stone_steps_dressed_3_narrow"],
]


def roadway(name):
    p = os.path.join(DEV, "spikes", "B3b", "out", "shrine", name + ".p3d")
    rw = next(l for l in mlod.read_mlod(p) if mlod.same_res(l.resolution, mlod.LOD_ROADWAY))
    return rw.points


def edge(pts, y, z):
    xs = [p[0] for p in pts if abs(p[1] - y) < 0.002 and abs(p[2] - z) < 0.002]
    return (round(min(xs), 3), round(max(xs), 3)) if xs else None


def main():
    ok_all = True
    for ch in CHAINS:
        off = [0.0, 0.0]               # (y, z) of the current foot
        prev_head = None
        for name in ch:
            m = MOD[name]
            pts = [(p[0], p[1] + off[0], p[2] + off[1]) for p in roadway(name)]
            foot = edge(pts, off[0], off[1])
            run, rise = m["run"], m["rise"]
            deg = math.degrees(math.atan2(rise, run))
            ok = foot is not None and deg <= 38.0 and (prev_head is None or prev_head == foot)
            print("  %-38s foot %s at (y %.3f z %.3f) ramp %.1f deg  %s" % (name, foot, off[0], off[1], deg,
                                                                           "OK" if ok else "BREAK"))
            ok_all &= ok
            head = m["connectors"]["stair_head"]
            off = [off[0] + head[1], off[1] + head[2]]
            prev_head = edge(pts, off[0], off[1])
        print("chain %s: %s" % (" > ".join(n.replace("jp_s_stone_steps_", "") for n in ch), "continuous" if ok_all
                                else "BROKEN"))
    print("C7 chain check:", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
