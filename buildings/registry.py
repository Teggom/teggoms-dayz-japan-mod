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

# ------------------------------------------------------------------------------------------------ C2 families
# Phase C wave 1 (agent C2, 2026-09-30): rural shells from parts/kit/jpparts/templates/rural.py (buildings/ruralkit.py
# builds them, buildings/shellcheck.py checks them). Test-island hamlet spots: C2_PLACEMENTS (spikes/C2/layout.py).
from jpparts.templates import rural as _ru  # noqa: E402

_LOOT_FARM = {"usage": ["Farm", "Village"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_LOOT_SHED = {"usage": ["Farm"], "categories": ["tools", "containers", "food"], "tags": ["floor"]}
C2_PLACEMENTS = {
    "farmhouse_kanto_yosemune_umaya": [{"pos": (942.000, 25.0, 1029.000), "yaw": 180.0, "where": "test island: C2 hamlet (west yard), Kanto farmhouse, front south onto the yard"}],
    "farmhouse_kinai_kirizuma_tile_takahe": [{"pos": (963.500, 25.0, 1028.000), "yaw": 180.0, "where": "test island: C2 hamlet (west yard), Kinai farmhouse, front south onto the yard"}],
    "hut_east_s_earth_mushiro": [{"pos": (933.500, 25.0, 1003.000), "yaw": 0.0, "where": "test island: C2 hamlet (west yard), hut east (small, earth floor), front north"}],
    "hut_west_thatch_leanl": [{"pos": (947.000, 25.0, 1003.000), "yaw": 0.0, "where": "test island: C2 hamlet (west yard), hut west (thatch, lean-to), front north"}],
    "hut_east_l_board": [{"pos": (962.500, 25.0, 1002.500), "yaw": 0.0, "where": "test island: C2 hamlet (west yard), hut east (large, board floor), front north"}],
    "shed_open_thatch": [{"pos": (941.000, 25.0, 1045.500), "yaw": 180.0, "where": "test island: C2 hamlet (west yard), open shed behind the Kanto farmhouse"}],
    "shed_walled_ishioki_woodshed": [{"pos": (962.000, 25.0, 1045.500), "yaw": 180.0, "where": "test island: C2 hamlet (west yard), walled shed with woodshed lean-to behind the Kinai house"}],
}


def _rural(key, dir_, cls, display, params, loot, mass):
    return {"key": key, "dir": dir_, "module": "rural_shells", "class": cls, "name": "jp_" + key, "display": display,
            "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
            "placements": [], "verify": "shellcheck", "budget": _ru.budget_class(**params), "ship": True}


C2_FARMHOUSES = [
    # DW06 Kanto farmhouse (hiroma type): roof form x inside stable x doma end (street view; canonical = doma left,
    # DayZ is left-handed: the kit frame's high x is the street-view left); ridge kinds for variety
    _rural("farmhouse_kanto_yosemune", "farmhouse", "Land_JP_Farmhouse_Kanto_Yosemune",
           "Kanto farmhouse (hiroma type, hipped thatch)",
           {"kind": "kanto", "form": "yosemune", "ridge": "bamboo"}, _LOOT_FARM, 80000.0),
    _rural("farmhouse_kanto_yosemune_umaya", "farmhouse", "Land_JP_Farmhouse_Kanto_Yosemune_Umaya",
           "Kanto farmhouse with inside stable (hipped thatch)",
           {"kind": "kanto", "form": "yosemune", "ridge": "shiba", "stable": True}, _LOOT_FARM, 80000.0),
    _rural("farmhouse_kanto_yosemune_umaya_domar", "farmhouse", "Land_JP_Farmhouse_Kanto_Yosemune_Umaya_DomaR",
           "Kanto farmhouse with inside stable (hipped thatch, doma right)",
           {"kind": "kanto", "form": "yosemune", "ridge": "umanori", "stable": True, "doma": "right"}, _LOOT_FARM,
           80000.0),
    _rural("farmhouse_kanto_irimoya_domar", "farmhouse", "Land_JP_Farmhouse_Kanto_Irimoya_DomaR",
           "Kanto farmhouse (irimoya thatch with smoke gables, doma right)",
           {"kind": "kanto", "form": "irimoya", "ridge": "bamboo", "doma": "right"}, _LOOT_FARM, 80000.0),
    # DW07 Kinai farmhouse with the ox: main roof form x lower roofs (tile / board); yamato-mune on the tiled kirizuma
    _rural("farmhouse_kinai_kirizuma_tile_takahe", "farmhouse", "Land_JP_Farmhouse_Kinai_Kirizuma_Tile_Takahe",
           "Kinai farmhouse with ox (yamato-mune: thatch gable, takahe, tiled lower roofs)",
           {"kind": "kinai", "form": "kirizuma", "lower": "tile", "takahe": True}, _LOOT_FARM, 80000.0),
    _rural("farmhouse_kinai_kirizuma_board", "farmhouse", "Land_JP_Farmhouse_Kinai_Kirizuma_Board",
           "Kinai farmhouse with ox (thatch gable, board lower roofs)",
           {"kind": "kinai", "form": "kirizuma", "lower": "board", "doma": "left"}, _LOOT_FARM, 80000.0),
    _rural("farmhouse_kinai_irimoya_tile", "farmhouse", "Land_JP_Farmhouse_Kinai_Irimoya_Tile",
           "Kinai farmhouse with ox (irimoya thatch, tiled lower roofs)",
           {"kind": "kinai", "form": "irimoya", "lower": "tile", "doma": "left"}, _LOOT_FARM, 80000.0),
    _rural("farmhouse_kinai_irimoya_board", "farmhouse", "Land_JP_Farmhouse_Kinai_Irimoya_Board",
           "Kinai farmhouse with ox (irimoya thatch, board lower roofs)",
           {"kind": "kinai", "form": "irimoya", "lower": "board"}, _LOOT_FARM, 80000.0),
]
C2_HUTS = [
    # DW01 poor hut, east (thatch hipped): 2 sizes x floor (earth / bamboo slats / boards) x door (itado / mushiro)
    _rural("hut_east_s_earth_mushiro", "hut", "Land_JP_Hut_East_S_Earth_Mushiro",
           "Poor hut, east type (small, earth floor, straw-mat door)",
           {"kind": "hut_east", "size": "s", "floor": "earth", "door": "mushiro"}, _LOOT_FARM, 15000.0),
    _rural("hut_east_s_sunoko", "hut", "Land_JP_Hut_East_S_Sunoko", "Poor hut, east type (small, bamboo-slat floor)",
           {"kind": "hut_east", "size": "s", "floor": "sunoko", "door": "itado"}, _LOOT_FARM, 15000.0),
    _rural("hut_east_l_board", "hut", "Land_JP_Hut_East_L_Board", "Poor hut, east type (large, board floor)",
           {"kind": "hut_east", "size": "l", "floor": "board", "door": "itado"}, _LOOT_FARM, 20000.0),
    _rural("hut_east_l_earth", "hut", "Land_JP_Hut_East_L_Earth", "Poor hut, east type (large, earth floor)",
           {"kind": "hut_east", "size": "l", "floor": "earth", "door": "itado"}, _LOOT_FARM, 20000.0),
    # DW30 poor hut, west / mountain (gable, board walls): roof x side lean-to x floor / door
    _rural("hut_west_thatch_leanl", "hut", "Land_JP_Hut_West_Thatch_LeanL",
           "Poor hut, west type (thatch gable, lean-to left, board floor)",
           {"kind": "hut_west", "roof": "thatch", "leanto": "left", "floor": "board", "door": "itado"}, _LOOT_FARM,
           15000.0),
    _rural("hut_west_ishioki_leanr", "hut", "Land_JP_Hut_West_Ishioki_LeanR",
           "Poor hut, west type (stone-weighted boards, lean-to right, earth floor, straw-mat door)",
           {"kind": "hut_west", "roof": "ishioki", "leanto": "right", "floor": "earth", "door": "mushiro"}, _LOOT_FARM,
           15000.0),
    _rural("hut_west_itabuki", "hut", "Land_JP_Hut_West_Itabuki", "Poor hut, west type (board roof, bamboo-slat floor)",
           {"kind": "hut_west", "roof": "itabuki", "floor": "sunoko", "door": "itado"}, _LOOT_FARM, 15000.0),
    _rural("hut_west_ishioki", "hut", "Land_JP_Hut_West_Ishioki", "Poor hut, west type (stone-weighted boards)",
           {"kind": "hut_west", "roof": "ishioki", "floor": "board", "door": "itado"}, _LOOT_FARM, 15000.0),
    _rural("hut_west_thatch", "hut", "Land_JP_Hut_West_Thatch", "Poor hut, west type (thatch gable, earth floor)",
           {"kind": "hut_west", "roof": "thatch", "floor": "earth", "door": "itado"}, _LOOT_FARM, 15000.0),
]
C2_SHEDS = [
    # DW24 shed / barn: open-sided / walled x roof (board / thatch / stone) x woodshed lean-to
    _rural("shed_open_board", "shed", "Land_JP_Shed_Open_Board", "Shed, open front (board roof)",
           {"kind": "shed", "roof": "itabuki", "open": True}, _LOOT_SHED, 8000.0),
    _rural("shed_open_thatch", "shed", "Land_JP_Shed_Open_Thatch", "Shed, open front (thatch)",
           {"kind": "shed", "roof": "thatch", "open": True}, _LOOT_SHED, 8000.0),
    _rural("shed_walled_ishioki_woodshed", "shed", "Land_JP_Shed_Walled_Ishioki_Woodshed",
           "Shed, walled (stone-weighted boards) with a woodshed lean-to",
           {"kind": "shed", "roof": "ishioki", "leanto": "right"}, _LOOT_SHED, 10000.0),
    _rural("barn_walled_thatch", "shed", "Land_JP_Barn_Walled_Thatch", "Barn, walled (thatch, 4 x 3 ken)",
           {"kind": "shed", "size": "l", "roof": "thatch"}, _LOOT_SHED, 15000.0),
]
for _b in C2_FARMHOUSES + C2_HUTS + C2_SHEDS:
    _b["placements"] = C2_PLACEMENTS.get(_b["key"], [])
BUILDINGS += C2_FARMHOUSES + C2_HUTS + C2_SHEDS


# ------------------------------------------------------------------------------------------------ C3 kura
# Phase C wave 1 (agent C3, 2026-09-30): DW22 plastered storehouse from parts/kit/jpparts/templates/kura.py
# (buildings/kurakit.py builds it, buildings/shellcheck.py checks it). Sangawara only: hongawara is a status roof
# (PLAYBOOK §2.1 T3 / §2.2), not a merchant's kura.
from jpparts.templates import kura as _ku  # noqa: E402

_LOOT_KURA = {"usage": ["Town", "Village"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
C3_PLACEMENTS = {}


def _kura(key, cls, display, params):
    return {"key": key, "dir": "kura", "module": "kura_shells", "class": cls, "name": "jp_" + key, "display": display,
            "params": dict(params), "model_dir": "kura", "mass": 40000.0, "sound": "doorWoodSlide", "loot": _LOOT_KURA,
            "placements": [], "verify": "shellcheck", "budget": _ku.budget_class(**params), "ship": True}


C3_KURA = [
    _kura("kura_namako", "Land_JP_Kura_Namako", "Kura (plastered storehouse, namako lower walls)",
          {"lower": "namako", "door": "_open", "roof": "sangawara", "window": "_slide"}),
    _kura("kura_kuro_hinged", "Land_JP_Kura_Kuro_Hinged",
          "Kura (plastered storehouse, black boarded lower walls, hinged plaster door leaves)",
          {"lower": "shitami", "door": "_hinged", "roof": "sangawara", "window": "_hinged"}),
    _kura("kura_plain", "Land_JP_Kura_Plain", "Kura (plastered storehouse, plain)",
          {"lower": "plain", "door": "_open", "roof": "sangawara", "window": "_slide"}),
]
for _b in C3_KURA:
    _b["placements"] = C3_PLACEMENTS.get(_b["key"], [])
BUILDINGS += C3_KURA


# ------------------------------------------------------------------------------------------------ C3 furnished variants
# The B4 pattern for every wave-1 type (buildings/furnishkit.py + buildings/furnish_sets.py): the base shell's recipe
# with the SAME params (identical shell geometry) + fittings + props as proxies + loot on floors and prop surfaces +
# street / yard objects. Class = the base class + the dressing. A furnished variant takes its base's island spot
# (C3_SWAP: base key -> furnished key); the bare shell stays shipped in the PBO.
def _find(key):
    return next(x for x in BUILDINGS if x["key"] == key)


def _furn(key, base, dress, suffix, display):
    b = _find(base)
    return {"key": key, "dir": "furnished", "module": "furnished_shells", "class": b["class"] + "_" + suffix,
            "name": "jp_" + key, "display": b["display"] + ", " + display,
            "params": {"base": base, "dress": dress}, "model_dir": "furnished", "mass": b["mass"],
            "sound": b["sound"], "loot": b["loot"], "placements": [], "verify": "shellcheck", "budget": b["budget"],
            "ship": True}


C3_FURNISHED = [
    _furn("f_th_kamigata_3k_middle_komeya", "th_kamigata_3k_middle_toril", "kamigata_komeya", "Komeya",
          "furnished: rice dealer"),
    _furn("f_th_kamigata_2k_middle_kamiya", "th_kamigata_2k_middle_torir", "kamigata_kamiya", "Kamiya",
          "furnished: paper and sundries shop"),
    _furn("f_th_edo_2k_middle_gofuku", "th_edo_2k_middle_torir", "edo_gofuku", "Gofuku", "furnished: cloth dealer"),
    _furn("f_th_edo_3k_cornerr_sakaya", "th_edo_3k_cornerr_toril", "edo_sakaya", "Sakaya", "furnished: sake shop"),
    _furn("f_pt_det_tile_nuriya_home", "pt_det_tile_nuriya", "posttown_home", "Home", "furnished: home"),
    _furn("f_inn_std_tile", "inn_std_tile", "inn_std", "Furnished", "furnished"),
    _furn("f_inn_grand", "inn_grand", "inn_grand", "Furnished", "furnished (upstairs guest rooms)"),
    _furn("f_farmhouse_kanto", "farmhouse_kanto_yosemune_umaya", "farm_kanto", "Furnished", "furnished"),
    _furn("f_farmhouse_kinai", "farmhouse_kinai_kirizuma_tile_takahe", "farm_kinai", "Furnished", "furnished"),
    _furn("f_hut_east_l_board", "hut_east_l_board", "hut_east", "Furnished", "furnished (T1)"),
    _furn("f_hut_west_thatch_leanl", "hut_west_thatch_leanl", "hut_west", "Furnished", "furnished (T1)"),
    _furn("f_shed_walled_woodshed", "shed_walled_ishioki_woodshed", "shed_barn", "Furnished", "furnished (storage)"),
    _furn("f_kura_namako", "kura_namako", "kura_storage", "Furnished", "furnished (storage)"),
    _furn("f_kura_kuro_hinged", "kura_kuro_hinged", "kura_storage", "Furnished", "furnished (storage)"),
]
# base key -> furnished key: the furnished variant takes the base's island spot
C3_SWAP = {"th_kamigata_3k_middle_toril": "f_th_kamigata_3k_middle_komeya",
           "th_kamigata_2k_middle_torir": "f_th_kamigata_2k_middle_kamiya",
           "th_edo_2k_middle_torir": "f_th_edo_2k_middle_gofuku",
           "th_edo_3k_cornerr_toril": "f_th_edo_3k_cornerr_sakaya",
           "pt_det_tile_nuriya": "f_pt_det_tile_nuriya_home",
           "inn_std_tile": "f_inn_std_tile",
           "inn_grand": "f_inn_grand",
           "farmhouse_kanto_yosemune_umaya": "f_farmhouse_kanto",
           "farmhouse_kinai_kirizuma_tile_takahe": "f_farmhouse_kinai",
           "hut_east_l_board": "f_hut_east_l_board",
           "hut_west_thatch_leanl": "f_hut_west_thatch_leanl",
           "shed_walled_ishioki_woodshed": "f_shed_walled_woodshed"}
# new spots for furnished variants whose base had none (the kura: behind the town row, in the hamlet)
C3_FURN_PLACEMENTS = {
    "f_kura_namako": [{"pos": (1000.0, 25.0, 1097.5), "yaw": 180.0,
                       "where": "test island: behind the C1 Kamigata row (town kura at the back of the lots), door south"}],
    "f_kura_kuro_hinged": [{"pos": (975.0, 25.0, 1041.0), "yaw": 270.0,
                            "where": "test island: C2 hamlet, east edge, door west onto the lane"}],
}
for _f in C3_FURNISHED:
    _base = _f["params"]["base"]
    if C3_SWAP.get(_base) == _f["key"]:
        _bb = _find(_base)
        _f["placements"] = [dict(p, where=p["where"] + " (C3: furnished)") for p in _bb["placements"]]
        _bb["placements"] = []
    _f["placements"] += C3_FURN_PLACEMENTS.get(_f["key"], [])
BUILDINGS += C3_FURNISHED


def get(key):
    for b in BUILDINGS:
        if b["key"] == key:
            return b
    raise KeyError("no building %r in buildings/registry.py (have: %s)" % (key, ", ".join(b["key"] for b in BUILDINGS)))


# ------------------------------------------------------------------------------------------------ S1 shop-set demos
# The KEEP_TRADES shop sets (buildings/shop_sets.py, research/interior/SHOP_SETS.md): one demo shop per 4-5 trades,
# each a furnished variant (furnishkit) whose shell takes the board display strip (townhouse option mise_floor _455).
# Not placed on the island (S1 brief): ship = the class exists in jp_buildings.pbo, placements empty.
S1_SHOPS = [
    _furn("s1_th_edo_3k_middle_kanamono", "th_edo_3k_middle_toril", "shop_kanamono_3k_ab1", "Kanamono",
          "shop set: ironmonger"),
]
BUILDINGS += S1_SHOPS
