"""The building registry (B0 step 0b): every building the pipeline (buildings/pipeline.py) builds, in config order.

One entry per building. The pipeline builds the ones you ask for, stores what it learned from each model in
buildings/<key>/record.json (its config class, model.cfg skeleton, loot points), and then regenerates the SHARED
outputs from every shipped building's record, so building N never erases building N-1:
  src/JP/buildings/config.cpp                 every shipped class (CfgPatches JP_Buildings)
  src/JP/buildings/<model_dir>/model.cfg      every shipped building in that model folder
  test/placements/C.csv                       every placement below
  test/ce/C_mapgroupproto.xml                 one loot group per shipped class
  test/ce/C_mapgrouppos.xml                   one group position per placement
  ..\\@Japan\\addons\\jp_buildings.pbo            src/JP/buildings packed

Fields:
  key         folder under buildings/ (holds the recipe module, out/, record.json, rooms.json, checks.json)
  module      recipe module in that folder: model() -> (M, floors, rooms) in the model frame; NAME (p3d name), CLASS;
              optional POSTS (post nodes for the C3 grid check)
  display     config displayName
  model_dir   src/JP/buildings/<model_dir>/ = P:\\JP\\buildings\\<model_dir>\\ (p3d + model.cfg)
  mass        Geometry mass (kg)
  sound       door sound set (vanilla doorWoodSlide*)
  loot        CE loot group: usage flags, categories, tags (loot lies out on the floors, PRODUCTION_PLAN)
  placements  [{pos: (x, y, z) world, yaw: deg, where: note}]; they go to C.csv (baked into the terrain) and to
              C_mapgrouppos.xml. Test-island spots are in README "The test island".
  verify      module in the folder with run(M, floors, pts) -> bool, or None for the pipeline's generic checks
  budget      face budget class (PLAYBOOK §12): 'small' | 'standard' | 'townhouse' | 'large'
  ship        True: staged into src, config, PBO and the drop-ins. False: built and checked offline only (out/)
"""

BUILDINGS = [
    {
        "key": "machiya_t3_01",
        "module": "machiya_t3_01",
        "display": "Machiya (tier 3)",
        "model_dir": "machiya",
        "mass": 60000.0,
        "sound": "doorWoodSlide",
        "loot": {"usage": ["Town"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]},
        # B4 (2026-09-30): the bare shell stays shipped (its class is the base of every furnished variant) but its
        # island spot now holds the furnished pilot below
        "placements": [],
        "verify": "verify",
        "budget": "large",
        "ship": True,
    },
    {
        # B4 pilot: the same shell + the furniture as proxies (PLAYBOOK §10.4 furnished variant), loot on the floors
        # and the props' surfaces, the street front and back yard dressed (site objects -> C.csv)
        "key": "machiya_t3_01_shop",
        "module": "machiya_t3_01_shop",
        "display": "Machiya (tier 3), general-goods shop",
        "model_dir": "machiya",
        "mass": 60000.0,
        "sound": "doorWoodSlide",
        "loot": {"usage": ["Town"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]},
        "placements": [{"pos": (1024.0, 25.0, 1045.0), "yaw": 180.0,
                        "where": "test island: the building spot, front (model +z) facing south to the spawn"}],
        "verify": "verify",
        "budget": "large",
        "ship": True,
    },
    {
        # B2's walk-in toilet (half door), shipped by B4 into the pilot's back yard for the half door's first
        # in-game test. Model (2.3, -11.2) in the machiya's frame, door facing the house.
        "key": "toilet_t1_01",
        "module": "toilet_t1_01",
        "display": "Outhouse (setchin)",
        "model_dir": "toilet",
        "mass": 3000.0,
        "sound": "doorWoodNolatch",
        "loot": {"usage": ["Town", "Village"], "categories": ["tools", "containers", "clothes", "food"],
                 "tags": ["floor"]},
        "placements": [{"pos": (1021.7, 25.0, 1056.2), "yaw": 180.0,
                        "where": "test island: the machiya pilot's back yard, door facing the house (south)"}],
        "verify": None,
        "budget": "small",
        "ship": True,
    },
    {
        # B0 step 0c: one unit from the townhouse template, built to show the template runs; since B2 it carries
        # the real party wall / party roof end (combos.py: all 60 combinations). NOT shipped: no config class, no
        # PBO, no island placement.
        "key": "townhouse_unit_test",
        "module": "townhouse_unit_test",
        "display": "Townhouse unit (test)",
        "model_dir": "townhouse",
        "mass": 40000.0,
        "sound": "doorWoodSlide",
        "loot": {"usage": ["Town"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]},
        "placements": [],
        "verify": None,
        "budget": "townhouse",
        "ship": False,
    },
]

BUDGETS = {"small": (3000, 1150, 400), "standard": (6000, 2300, 800), "townhouse": (9000, 3450, 1200),
           "large": (12000, 4600, 1600)}

# ------------------------------------------------------------------------------------------------ C1 families
# Phase C wave 1 (agent C1, 2026-09-30): template shells, one registry entry each (buildings/shellkit.py builds them,
# buildings/shellcheck.py checks them at the machiya's standard). Test-island spots: C1_PLACEMENTS.
import os as _os  # noqa: E402
import sys as _sys  # noqa: E402

_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "parts", "kit"))
from jpparts.templates import townhouse as _th  # noqa: E402

_LOOT_TOWN = {"usage": ["Town"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_LOOT_POST = {"usage": ["Town", "Village"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_POS = {"end_l": ("end", "left", "EndL"), "end_r": ("end", "right", "EndR"), "middle": ("middle", None, "Middle"),
        "corner_l": ("corner", "left", "CornerL"), "corner_r": ("corner", "right", "CornerR")}
# key -> [{pos, yaw, where}]: the C1 test street on the island (spikes/C1/layout.py prints this block)
C1_PLACEMENTS = {
    "th_kamigata_3k_cornerr_torir": [{"pos": (1003.238, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "th_kamigata_3k_middle_toril": [{"pos": (997.682, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "th_kamigata_2k_middle_torir": [{"pos": (993.004, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "th_kamigata_3k_endl_toril": [{"pos": (988.358, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "th_edo_3k_cornerr_toril": [{"pos": (1059.238, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "th_edo_2k_middle_torir": [{"pos": (1054.592, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "th_edo_3k_middle_toril_board": [{"pos": (1049.914, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "th_edo_2k_endl_torir": [{"pos": (1045.268, 25.0, 1087.640), "yaw": 180.0, "where": "test island: C1 test street z 1080, north side, front facing south"}],
    "pt_det_tile_nuriya": [{"pos": (988.730, 25.0, 1072.360), "yaw": 0.0, "where": "test island: C1 test street z 1080, south side, front facing north"}],
    "pt_row_middle": [{"pos": (997.254, 25.0, 1072.360), "yaw": 0.0, "where": "test island: C1 test street z 1080, south side, front facing north"}],
    "pt_row_endl": [{"pos": (1002.810, 25.0, 1072.360), "yaw": 0.0, "where": "test island: C1 test street z 1080, south side, front facing north"}],
    "inn_std_tile": [{"pos": (1013.122, 25.0, 1071.450), "yaw": 0.0, "where": "test island: C1 test street z 1080, south side, front facing north"}],
    "inn_grand": [{"pos": (1026.222, 25.0, 1071.450), "yaw": 0.0, "where": "test island: C1 test street z 1080, south side, front facing north"}],
}


def _entry(key, dir_, module, cls, name, display, params, loot, mass, tags=None):
    pr = dict(params)
    if tags:
        pr["tags"] = tags
    return {"key": key, "dir": dir_, "module": module, "class": cls, "name": name, "display": display, "params": pr,
            "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot, "placements": [],
            "verify": "shellcheck", "budget": _th.budget_class(**params), "ship": True}


def _townhouse(frontage, region, pos, tori, extra=None, suffix=""):
    position, free, ptag = _POS[pos]
    params = {"frontage": frontage, "region": region, "position": position, "tori": tori}
    if free:
        params["free"] = free
    params.update(extra or {})
    t = "ToriL" if tori == "left" else "ToriR"
    cls = "Land_JP_Townhouse_%s_%dken_%s_%s%s" % (region.capitalize(), frontage, ptag, t, suffix)
    key = "th_%s_%dk_%s_%s%s" % (region, frontage, ptag.lower(), t.lower(), suffix.lower())
    disp = "Townhouse (%s, %d ken, %s, toriniwa %s%s)" % (region.capitalize(), frontage, ptag, tori,
                                                         (", " + suffix.strip("_").lower()) if suffix else "")
    return _entry(key, "townhouse", "townhouse_units", cls, "jp_townhouse_" + key[3:], disp, params, _LOOT_TOWN,
                  40000.0)


C1_TOWNHOUSES = []
for _fr in (2, 3, 4):                        # the 60 template combinations (combos.py order)
    for _rg in ("kamigata", "edo"):
        for _pos in ("end_l", "end_r", "middle", "corner_l", "corner_r"):
            for _tori in ("left", "right"):
                C1_TOWNHOUSES.append(_townhouse(_fr, _rg, _pos, _tori))
# cheap variety (PARTS_GAP_AUDIT DW11 / DW12 variant axes): Edo board-roofed middles in every frontage (1730 Edo was
# about half tiled, PLAYBOOK section 1 [T05]), one kakigara (oyster-shell board, G0 G1-3) middle, two Kamigata fronts
for _fr in (2, 3, 4):
    for _tori in ("left", "right"):
        C1_TOWNHOUSES.append(_townhouse(_fr, "edo", "middle", _tori, {"covering": "itabuki"}, "_Board"))
C1_TOWNHOUSES.append(_townhouse(3, "edo", "middle", "left", {"covering": "kakigara"}, "_Kakigara"))
C1_TOWNHOUSES.append(_townhouse(3, "kamigata", "middle", "left", {"shopfront": "_kyo"}, "_Kyo"))
C1_TOWNHOUSES.append(_townhouse(3, "kamigata", "middle", "right", {"shopfront": "_komeya"}, "_Komeya"))

_PT = "tokaido"
_LIV = {"mise": "living"}                    # the post-town house is the home side: its front room is lived in
C1_POSTTOWN = [
    _entry("pt_det_tile_nuriya", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Det_TileNuriya",
           "jp_posttown_det_tile_nuriya", "Post-town house (Tokaido, detached, tile roof, plastered front)",
           {"frontage": 3, "region": _PT, "position": "detached", "tori": "left", "shopfront": "_komeya"},
           _LOOT_POST, 40000.0, _LIV),
    _entry("pt_det_tile_board", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Det_TileBoard",
           "jp_posttown_det_tile_board", "Post-town house (Tokaido, detached, tile roof, board front)",
           {"frontage": 3, "region": _PT, "position": "detached", "tori": "right", "upper": "board",
            "shopfront": "_kyo"}, _LOOT_POST, 40000.0, _LIV),
    _entry("pt_det_board_nuriya", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Det_BoardNuriya",
           "jp_posttown_det_board_nuriya", "Post-town house (Tokaido, detached, board roof, plastered front)",
           {"frontage": 3, "region": _PT, "position": "detached", "tori": "left", "covering": "itabuki",
            "shopfront": "_oyako"}, _LOOT_POST, 40000.0, _LIV),
    _entry("pt_det_board_board", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Det_BoardBoard",
           "jp_posttown_det_board_board", "Post-town house (Tokaido, detached, board roof, board front)",
           {"frontage": 3, "region": _PT, "position": "detached", "tori": "right", "covering": "itabuki",
            "upper": "board", "shopfront": "_komeya"}, _LOOT_POST, 40000.0, _LIV),
    _entry("pt_det_stable_tile", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Det_Stable_Tile",
           "jp_posttown_det_stable_tile", "Post-town house with stable (Tokaido, detached, tile roof)",
           {"frontage": 3, "region": _PT, "position": "detached", "tori": "left", "geya_ken": 2, "stable": "_umaya",
            "shopfront": "_komeya"}, _LOOT_POST, 40000.0, _LIV),
    _entry("pt_det_stable_board", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Det_Stable_Board",
           "jp_posttown_det_stable_board", "Post-town house with stable (Tokaido, detached, board roof)",
           {"frontage": 3, "region": _PT, "position": "detached", "tori": "right", "geya_ken": 2, "stable": "_umaya",
            "covering": "itabuki", "upper": "board", "shopfront": "_komeya"}, _LOOT_POST, 40000.0, _LIV),
    _entry("pt_row_endl", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Row_EndL",
           "jp_posttown_row_endl", "Post-town house, row end (Tokaido, free gable left)",
           {"frontage": 3, "region": _PT, "position": "end", "free": "left", "tori": "left", "shopfront": "_komeya"},
           _LOOT_POST, 40000.0, _LIV),
    _entry("pt_row_middle", "posttown", "posttown_houses", "Land_JP_PostTownHouse_Row_Middle",
           "jp_posttown_row_middle", "Post-town house, row middle (Tokaido)",
           {"frontage": 3, "region": _PT, "position": "middle", "tori": "left", "covering": "itabuki",
            "upper": "board", "shopfront": "_kyo"}, _LOOT_POST, 40000.0, _LIV),
]

_INN = {"frontage": 5, "region": _PT, "position": "detached", "geya_ken": 2}
_INN_TAGS = {"mise": "office"}               # the front room of an inn is the reception hall with the choba
C1_HATAGO = [
    _entry("inn_std_tile", "hatago", "hatago_inns", "Land_JP_Hatago_Std_Tile", "jp_hatago_std_tile",
           "Inn (hatago), tile roof, plastered front",
           dict(_INN, tori="left", split=True, shopfront="_kyo"), _LOOT_POST, 60000.0, _INN_TAGS),
    _entry("inn_std_board", "hatago", "hatago_inns", "Land_JP_Hatago_Std_Board", "jp_hatago_std_board",
           "Inn (hatago), board roof, board front",
           dict(_INN, tori="right", split=True, covering="itabuki", upper="board", shopfront="_oyako"), _LOOT_POST,
           60000.0, _INN_TAGS),
    _entry("inn_std_mushiko", "hatago", "hatago_inns", "Land_JP_Hatago_Std_Mushiko", "jp_hatago_std_mushiko",
           "Inn (hatago), tile roof and pent, mushiko front",
           dict(_INN, tori="left", split=True, pent="tile", upper="mushiko", shopfront="_kyo"), _LOOT_POST,
           60000.0, _INN_TAGS),
    _entry("inn_grand", "hatago", "hatago_inns", "Land_JP_Hatago_Grand", "jp_hatago_grand",
           "Grand inn (hatago), two storeys",
           dict(_INN, tori="left", upper="full", pent="board", shopfront="_kyo"), _LOOT_POST, 60000.0,
           dict(_INN_TAGS, nikai_front="zashiki", nikai_back="zashiki")),
]

for _b in C1_TOWNHOUSES + C1_POSTTOWN + C1_HATAGO:
    _b["placements"] = C1_PLACEMENTS.get(_b["key"], [])
BUILDINGS += C1_TOWNHOUSES + C1_POSTTOWN + C1_HATAGO


def get(key):
    for b in BUILDINGS:
        if b["key"] == key:
            return b
    raise KeyError("no building %r in buildings/registry.py (have: %s)" % (key, ", ".join(b["key"] for b in BUILDINGS)))
