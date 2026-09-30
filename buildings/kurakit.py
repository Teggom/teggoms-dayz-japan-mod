"""Kura shells for the building pipeline (C3, 2026-09-30): DW22 plastered storehouse from
parts/kit/jpparts/templates/kura.py with the parameters of its buildings/registry.py entry (C3_KURA); the family folder
buildings/kura holds a two-line module that re-exports this one.

  model(name=..., tags={room: tag}, **template params) -> (M, floors, rooms)   (model frame: footprint centre)

Module state read by the pipeline and shellcheck after each model() call (as buildings/ruralkit.py):
  POSTS     kit-frame post nodes (hidden in the okabe) for the C3 grid check
  PASSAGES  none
  PORTALS   model-frame C11 portals of the static openings: the kura windows (bars) and the gable vents
  STAIRS    the stair to the upper floor (shellcheck ST1-ST5): {foot, dir, run, width, y_low, y_up, well}
  INFO      the template's info dict
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import kura  # noqa: E402

POSTS = []
PASSAGES = []
PORTALS = []
STAIRS = []
INFO = {}
DOOR_CHECK_OTHERS_OPEN = True     # shellcheck: the '_hinged' outer leaves are open while the inner door is measured
PASSAGE_LABEL ="C7 open passage clear >= 1.00 + head >= 2.00"
FRAME_NOTE = ("model: origin = footprint centre at grade, +z = front (the door side); built by "
              "parts/kit/jpparts/templates/kura.py; two floors: 'kura' (ground) and 'nikai' (upper, by the stair)")


def model(name=None, tags=None, **params):
    M, floors, rooms, info = kura.model(name=name, **params)
    POSTS[:] = info["posts"]
    PASSAGES[:] = []
    PORTALS[:] = info["portals_model"]
    STAIRS[:] = [info["stair_model"]]
    for r in rooms:
        if tags and r["name"] in tags:
            r["tag"] = tags[r["name"]]
        r["fittings"] = []
    for f in floors:
        if tags and f["name"] in tags:
            f["tag"] = tags[f["name"]]
    INFO.clear()
    INFO.update(info)
    return M, floors, rooms
