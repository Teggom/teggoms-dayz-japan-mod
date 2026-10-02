"""Rural-site template shells for the building pipeline (W3C2, 2026-10-02): the recipe behind the wave-3c-2 kilns,
quarry face, mine adit, timber slide, salt bed, bunk hall, salt-boiling hut and their yards. Built by
parts/kit/jpparts/templates/ruralsite.py from the parameters its registry entry carries (buildings/registry.py
W3C2_*); the family folders (buildings/rs_*) hold a two-line module that re-exports this.

  model(name=..., kind=..., tags={room: tag}, **template params) -> (M, floors, rooms)   (model frame: footprint centre)

Module state read by the pipeline and shellcheck after each model() call (as buildings/tradekit.py): POSTS, PASSAGES,
PORTALS, STAIRS, INFO.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import ruralsite  # noqa: E402

POSTS = []
PASSAGES = []
PORTALS = []
STAIRS = []
INFO = {}
PASSAGE_LABEL = "C7 open passage (gate passage / open doorway) clear >= 1.00 + head >= 2.00"
FRAME_NOTE = ("model: origin = footprint centre at grade, +z = front; built by parts/kit/jpparts/templates/ruralsite.py;"
              " 'fittings' = kiln spots, the pan, the irori, fixed props ...")


def model(name=None, tags=None, **params):
    M, floors, rooms, info = ruralsite.model(name=name, **params)
    POSTS[:] = info["posts"]
    PASSAGES[:] = info["passages_model"]
    PORTALS[:] = info["portals_model"]
    STAIRS[:] = [info["stair_model"]] if info.get("stair_model") else []
    fits = info["fittings_model"]
    for r in rooms:
        if tags and r["name"] in tags:
            r["tag"] = tags[r["name"]]
        r["fittings"] = [f for f in fits if f.get("room") == r["name"]]
    for f in floors:
        if tags and f["name"] in tags:
            f["tag"] = tags[f["name"]]
    INFO.clear()
    INFO.update(info)
    return M, floors, rooms
