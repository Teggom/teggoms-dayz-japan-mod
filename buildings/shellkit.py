"""Template shells for the building pipeline (C1, 2026-09-30): the recipe behind the townhouse units (DW11 / DW12),
the Tokaido post-town houses (DW10) and the inns (TR05). Every one is built by parts/kit/jpparts/templates/townhouse.py
from the parameters its registry entry carries (buildings/registry.py FAMILIES); the family folders
(buildings/townhouse, buildings/posttown, buildings/hatago) hold a two-line module that re-exports this one.

  model(name=..., tags={room: tag}, **template params) -> (M, floors, rooms)   (model frame: lot centre at grade)

Module state read by the pipeline and shellcheck after each model() call:
  POSTS     kit-frame post nodes (x, z, y0, y1) for the C3 grid check (the kit frame is on the half-ken grid)
  PASSAGES  model-frame open passages without a door [(x, z, y)]: the toriniwa -> kitchen passage (clear >= 1.00,
            head >= 2.00, measured along x at the omoya back wall line)
  INFO      the template's info dict
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import townhouse  # noqa: E402
from jpparts.core import KEN  # noqa: E402

POSTS = []
PASSAGES = []
STAIRS = []         # model-frame stairs: {foot (x, z), dir +-1 along x, run, width (+z from the foot z), y_low, y_up, well}
INFO = {}
FRAME_NOTE = ("model: origin = lot centre at grade, +z = street front; lot width = neighbour spacing "
              "(rooms.json 'lot_width' via the record's params); built by parts/kit/jpparts/templates/townhouse.py")


def model(name=None, tags=None, **params):
    M, floors, rooms, info = townhouse.model(name=name, **params)
    POSTS[:] = info["posts"]
    cx, cz = info["centre"]
    tori_high = townhouse.SV[params.get("tori", "left")] == "right"        # street-view left = kit high x
    xk = info["W"] - KEN / 2 if tori_high else KEN / 2
    PASSAGES[:] = [(xk - cx, -info["DO"] - cz, townhouse.DOMA)]
    STAIRS[:] = []
    st = info.get("stair")
    if st:
        # canonical kit frame -> model frame: a tori-high unit was mirrored (x -> W - x), so its flight runs -x
        mx = (lambda x: info["W"] - x) if tori_high else (lambda x: x)
        w0, w1 = sorted((mx(st["well"][0]), mx(st["well"][1])))
        STAIRS.append(dict(st, foot=(mx(st["foot"][0]) - cx, st["foot"][1] - cz), dir=-1.0 if tori_high else 1.0,
                           well=(w0 - cx, w1 - cx, st["well"][2] - cz, st["well"][3] - cz)))
    for r in rooms:
        if tags and r["name"] in tags:
            r["tag"] = tags[r["name"]]
        r["lot_width"] = round(info["lot_width"], 4)
    for f in floors:
        if tags and f["name"] in tags:
            f["tag"] = tags[f["name"]]
    INFO.clear()
    INFO.update(info)
    return M, floors, rooms
