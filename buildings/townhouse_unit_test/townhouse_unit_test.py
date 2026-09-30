#!/usr/bin/env python3
r"""One unit from the townhouse template (B0 step 0c), built through the pipeline to show the template runs:

  python buildings/pipeline.py townhouse_unit_test      (registry: ship=False -> out/ + checks.json only; it is not
                                                         in config.cpp, the PBO or on the test island)

B2 (2026-09-29) filled townhouse.HOOKS with the real party parts (jp_p_wall_party, jp_p_roof_party_end,
jp_p_roof_corner, jp_p_roof_seam_cap; jpparts/party.py): no placeholders are left. Change PARAMS to try another unit
(frontage 2/3/4, kamigata/edo, end/middle/corner); combos.py builds all 60 combinations.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import townhouse  # noqa: E402

# a Kamigata 3-ken END unit, free gable and toriniwa on the right seen from the street: one free gable (with its
# udatsu and the Ioka gable pent), one party side (B2's party wall and flush party roof end). Sides are street-view.
PARAMS = {"frontage": 3, "region": "kamigata", "position": "end", "free": "right", "tori": "right"}
NAME = "jp_townhouse_unit_test"
CLASS = "Land_JP_Townhouse_Unit_Test"
FRAME_NOTE = ("model: origin = lot centre at grade, +z = street front; lot width = neighbour spacing "
              "(rooms.json 'lot_width'); built by parts/kit/jpparts/templates/townhouse.py")
POSTS = []                  # kit-frame post nodes (C3 grid check)
INFO = {}


def model():
    M, floors, rooms, info = townhouse.model(name=NAME, **PARAMS)
    del POSTS[:]
    POSTS.extend(info["posts"])
    INFO.clear()
    INFO.update(info)
    for p in info["placeholders"]:
        print("  PLACEHOLDER:", p)
    print("  lot width %.3f m (party gap %.3f), party %s, free %s" % (info["lot_width"], townhouse.PARTY_GAP,
                                                                     info["party"], info["free"]))
    return M, floors, rooms


if __name__ == "__main__":
    M, floors, rooms = model()
    print(len(M.doors), "doors;", ", ".join("%g: %d faces" % (l.resolution, len(l.faces)) for l in M.lods()))
