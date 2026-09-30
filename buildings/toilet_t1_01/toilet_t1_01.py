#!/usr/bin/env python3
r"""Land_JP_Toilet_T1_01 - B2's walk-in outhouse (G1 A1 ruling 1: 1 x 1.5 ken, one hinged half door,
jp_p_open_halfdoor _hinged), shipped through the registry by B4 so the half door gets its first in-game test in the
machiya pilot's back yard.

The assembly itself is B2's (parts/kit/b2_assembly.py toilet(), 17/17 offline there); this recipe only moves it to
the model frame the pipeline wants: origin = footprint centre at grade, +z = the door side.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import b2_assembly as B2  # noqa: E402

NAME = "jp_toilet_t1_01"
CLASS = "Land_JP_Toilet_T1_01"
FRAME_NOTE = "model: origin = footprint centre at grade, +z = the door side"
SLOT = (0.76, 1.06, -2.10, -1.93)       # the drop slot in B2's floor (kit frame), kept free of loot


def model():
    a, ctx = B2.toilet()
    W, D = ctx["W"], ctx["D"]
    dx, dz = -W / 2, D / 2
    M = a.transformed(0.0, (dx, 0.0, dz))

    def mv(r):
        return (r[0] + dx, r[1] + dx, r[2] + dz, r[3] + dz)
    floors, rooms = [], []
    for r in ctx["rooms"]:
        rect = mv(r["rect"])
        obs = [mv((SLOT[0] - 0.05, SLOT[1] + 0.05, SLOT[2] - 0.05, SLOT[3] + 0.05))]
        floors.append({"name": r["name"], "tag": "toilet", "rect": rect, "y": r["y"], "obstacles": obs})
        rooms.append({"name": r["name"], "tag": "toilet", "floor": "boards", "level_m": r["y"],
                      "rect_model": [round(v, 3) for v in rect], "doors": ["DoorsTwin1"],
                      "note": "walk-in outhouse, drop slot at the back"})
    return M, floors, rooms
