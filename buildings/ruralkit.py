"""Rural template shells for the building pipeline (C2, 2026-09-30): the recipe behind the Kanto and Kinai farmhouses
(DW06 / DW07), the poor huts east and west (DW01 / DW30) and the sheds (DW24). Every one is built by
parts/kit/jpparts/templates/rural.py from the parameters its registry entry carries (buildings/registry.py C2_*);
the family folders (buildings/farmhouse, buildings/hut, buildings/shed) hold a two-line module that re-exports this.

  model(name=..., kind=..., tags={room: tag}, **template params) -> (M, floors, rooms)   (model frame: footprint centre)

Module state read by the pipeline and shellcheck after each model() call (as buildings/shellkit.py):
  POSTS     kit-frame post nodes (x, z, y0, y1) for the C3 grid check
  PASSAGES  model-frame open doorways without a door leaf [(x, z, y)] (a mushiro doorway: clear >= 1.00, head >= 2.00)
  PORTALS   model-frame C11 portals of declared openings that are not doors: the mushiro doorway, the irimoya smoke
            gables [(name, (x0, x1, y0, y1, z0, z1))]
  STAIRS    none
  INFO      the template's info dict (fittings_model: irori pits + hook points, kamado spots, stalls)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import rural  # noqa: E402

POSTS = []
PASSAGES = []
PORTALS = []
STAIRS = []
INFO = {}
PASSAGE_LABEL = "C7 open doorway (mushiro, no leaf) clear >= 1.00 + head >= 2.00"
FRAME_NOTE = ("model: origin = footprint centre at grade, +z = front (entrance side); built by "
              "parts/kit/jpparts/templates/rural.py; 'fittings' = irori pit (rect, hook point), kamado spot, stall")


def model(name=None, tags=None, **params):
    M, floors, rooms, info = rural.model(name=name, **params)
    POSTS[:] = info["posts"]
    PASSAGES[:] = info["passages_model"]
    PORTALS[:] = info["portals_model"]
    STAIRS[:] = []
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
