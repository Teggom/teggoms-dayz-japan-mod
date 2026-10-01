"""Civic / roadside template shells for the building pipeline (W2C, 2026-10-01): the recipe behind the roadside tea
houses (TR01), the smithy + swordsmith (TR11), the guard hut (GV1) and the ward gate (GV7). Every one is built by
parts/kit/jpparts/templates/civic.py from the parameters its registry entry carries (buildings/registry.py W2C_*);
the family folders (buildings/teahouse, smithy, guardhut, kido) hold a two-line module that re-exports this.

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
from jpparts.templates import civic  # noqa: E402

POSTS = []
PASSAGES = []
PORTALS = []
STAIRS = []
INFO = {}
PASSAGE_LABEL = "C7 open passage (no leaf: the gate way) clear >= 1.00 + head >= 2.00"
FRAME_NOTE = ("model: origin = footprint centre at grade, +z = front (entrance side); built by "
              "parts/kit/jpparts/templates/civic.py; 'fittings' = fixed-prop spots for the furnisher (kamado, forge, bellows, "
              "anvil, quench tub, benches, fire ladder, shimenawa)")


def model(name=None, tags=None, **params):
    M, floors, rooms, info = civic.model(name=name, **params)
    POSTS[:] = info["posts"]
    PASSAGES[:] = info["passages_model"]
    PORTALS[:] = info["portals_model"]
    STAIRS[:] = []
    fits = info["fittings_model"]
    for r in rooms:
        if tags and r["name"] in tags:
            r["tag"] = tags[r["name"]]
        r["fittings"] = [f for f in fits if f.get("room") == r["name"]]
    # W2C: spots outside every room (a lantern by the door, the fire ladder on the ridge) ride on the first room
    if rooms:
        rooms[0]["fittings"] += [dict(f, outside=True) for f in fits if not f.get("room")]
    for f in floors:
        if tags and f["name"] in tags:
            f["tag"] = tags[f["name"]]
    INFO.clear()
    INFO.update(info)
    return M, floors, rooms
