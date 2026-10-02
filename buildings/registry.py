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
# CA1 (2026-10-01): PLAYBOOK §12's simple set only (FX2's 'large_plus' folded back). Budgets are guidance (Stephen
# 2026-10-01): a building that deliberately needs more carries "over_budget_ok": "<reason>" in its registry entry and
# may go up to +50 %; C5 then passes and reports the overage (budget_check; tools/budget_report.py lists them all).
OVER_BUDGET_MAX = 1.5


def budget_check(b, got):
    """PLAYBOOK §12 face budget of a registry entry b for got = (R1, R2, R3) faces -> (ok, detail suffix)."""
    bud = BUDGETS[b["budget"]]
    if all(g <= m for g, m in zip(got, bud)):
        return True, ""
    reason = b.get("over_budget_ok")
    pct = max((g - m) * 100.0 / m for g, m in zip(got, bud))
    if reason and all(g <= m * OVER_BUDGET_MAX for g, m in zip(got, bud)):
        return True, " | OVER BUDGET +%.1f %% (deliberate: %s)" % (pct, reason)
    return False, " | OVER BUDGET +%.1f %% (%s)" % (pct, ("over the +50 %% limit: " + reason) if reason else
                                                     "no over_budget_ok reason in the registry entry")

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
            "ship": True, **({"over_budget_ok": b["over_budget_ok"]} if b.get("over_budget_ok") else {})}


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
    _furn("s1_th_kamigata_2k_middle_tabako", "th_kamigata_2k_middle_torir", "shop_tabako_2k_ab0", "Tabako",
          "shop set: tobacco"),
    _furn("s1_th_kamigata_3k_endr_mochiya", "th_kamigata_3k_endr_toril", "shop_mochiya_3k_ab0", "Mochiya",
          "shop set: sweets and rice cakes"),
    _furn("s1_th_edo_3k_endl_kusuri", "th_edo_3k_endl_toril", "shop_kusuri_3k_ab2", "Kusuri",
          "shop set: apothecary (heavier abandoned state)"),
    _furn("s1_th_edo_2k_middle_board_shitate", "th_edo_2k_middle_torir_board", "shop_shitate_2k_ab1", "Shitate",
          "shop set: tailor"),
    _furn("s1_th_kamigata_3k_middle_kyo_ningyo", "th_kamigata_3k_middle_toril_kyo", "shop_ningyo_3k_ab1", "Ningyo",
          "shop set: dolls"),
]
BUILDINGS += S1_SHOPS


# ------------------------------------------------------------------------------------------------ SH1 showcase
# SH1 (2026-10-01, spikes/SH1/SH1_PROGRESS.md): S1's six demo shops go onto the C1 test street. Three take the spot
# of a bare unit of their frontage / row-end type; the other three are middle units whose type is only on the street
# as C3's furnished shops, so they are inserted: the Kamigata row grows two units west (its bare end unit moves to
# the new west end), the Edo row one unit west. Positions: spikes/C1/layout.py place_row, lot line to lot line
# (python spikes/SH1/street_sh1.py prints and checks them). Three bare open board sheds hold the life-layer gallery.
_SH1_N = "test island: C1 test street z 1080, north side, front facing south"
SH1_SHOPS = {
    # demo shop key: (x, replaces / inserted)
    "s1_th_kamigata_3k_endr_mochiya": (1003.238, "replaces the bare th_kamigata_3k_cornerr_torir (row east end)"),
    "s1_th_kamigata_2k_middle_tabako": (989.236, "inserted west of the paper shop"),
    "s1_th_kamigata_3k_middle_kyo_ningyo": (984.558, "inserted west of the tobacco shop"),
    "s1_th_edo_2k_middle_board_shitate": (1050.824, "inserted west of the cloth dealer"),
    "s1_th_edo_3k_middle_kanamono": (1046.146, "replaces the bare th_edo_3k_middle_toril_board"),
    "s1_th_edo_3k_endl_kusuri": (1040.590, "replaces the bare th_edo_2k_endl_torir (row west end, one ken wider)"),
}
SH1_REMOVED = ["th_kamigata_3k_cornerr_torir", "th_edo_3k_middle_toril_board", "th_edo_2k_endl_torir"]
SH1_MOVED = {"th_kamigata_3k_endl_toril": (979.002, 25.0, 1087.640)}
SH1_GALLERY = {"shed_open_board": [(1072.0, 25.0, 1036.0), (1080.0, 25.0, 1036.0), (1088.0, 25.0, 1036.0)]}
for _k in SH1_REMOVED:
    get(_k)["placements"] = []
for _k, _p in SH1_MOVED.items():
    get(_k)["placements"] = [{"pos": _p, "yaw": 180.0, "where": _SH1_N + " (SH1: moved to the new row end)"}]
for _k, (_x, _why) in SH1_SHOPS.items():
    get(_k)["placements"] = [{"pos": (_x, 25.0, 1087.640), "yaw": 180.0, "where": _SH1_N + " (SH1 demo shop: %s)" % _why}]
for _k, _ps in SH1_GALLERY.items():
    get(_k)["placements"] = [{"pos": _p, "yaw": 180.0,
                              "where": "test island: SH1 life-layer gallery (east yard), open front facing south"}
                             for _p in _ps]


# ------------------------------------------------------------------------------------------------ W2C civic shells
# Phase C wave 2 (agent W2C, 2026-10-01): bare civic / roadside shells from parts/kit/jpparts/templates/civic.py
# (buildings/civickit.py builds them, buildings/shellcheck.py checks them; research notes spikes/W2C/W2C_NOTES.md).
# Not placed on the island (a later agent furnishes and places them): shipped in jp_buildings.pbo only.
from jpparts.templates import civic as _cv  # noqa: E402

_LOOT_ROAD = {"usage": ["Village", "Town"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_LOOT_SMITH = {"usage": ["Village", "Town"], "categories": ["tools", "containers"], "tags": ["floor"]}
_LOOT_GUARD = {"usage": ["Town", "Village"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}


def _civic(key, dir_, cls, display, params, loot, mass):
    return {"key": key, "dir": dir_, "module": "civic_shells", "class": cls, "name": "jp_" + key, "display": display,
            "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
            "placements": [], "verify": "shellcheck", "budget": _cv.budget_class(**params), "ship": True}


W2C_TEAHOUSES = [
    # TR01 roadside tea house, 3 sizes (bench shed / open shop / tateba with rooms) x roof (thatch / boards /
    # stone-weighted boards); the battari bench on the shop fronts; the pass tea house (toge-jaya) as a size
    _civic("teahouse_bench_thatch", "teahouse", "Land_JP_Teahouse_Bench_Thatch",
           "Roadside tea house: bench shed (kake-jaya, thatch)", {"kind": "teahouse", "size": "bench", "roof": "thatch"},
           _LOOT_ROAD, 8000.0),
    _civic("teahouse_bench_itabuki", "teahouse", "Land_JP_Teahouse_Bench_Itabuki",
           "Roadside tea house: bench shed with the bench roof (kake-jaya, boards)",
           {"kind": "teahouse", "size": "bench", "roof": "itabuki"}, _LOOT_ROAD, 8000.0),
    _civic("teahouse_shop_thatch", "teahouse", "Land_JP_Teahouse_Shop_Thatch",
           "Roadside tea house: open shop (chamise, thatch)", {"kind": "teahouse", "size": "shop", "roof": "thatch"},
           _LOOT_ROAD, 15000.0),
    _civic("teahouse_shop_itabuki", "teahouse", "Land_JP_Teahouse_Shop_Itabuki",
           "Roadside tea house: open shop with the bench roof (chamise, boards)",
           {"kind": "teahouse", "size": "shop", "roof": "itabuki"}, _LOOT_ROAD, 15000.0),
    _civic("teahouse_pass_ishioki", "teahouse", "Land_JP_Teahouse_Pass_Ishioki",
           "Mountain-pass tea house (toge-jaya, stone-weighted boards, woodshed lean-to)",
           {"kind": "teahouse", "size": "pass", "roof": "ishioki"}, _LOOT_ROAD, 15000.0),
    _civic("teahouse_tateba_thatch", "teahouse", "Land_JP_Teahouse_Tateba_Thatch",
           "Rest-stop tea house with rooms (tateba-jaya, hipped thatch)",
           {"kind": "teahouse", "size": "tateba", "roof": "thatch"}, _LOOT_ROAD, 40000.0),
    _civic("teahouse_tateba_itabuki", "teahouse", "Land_JP_Teahouse_Tateba_Itabuki",
           "Rest-stop tea house with rooms (tateba-jaya, boards, bench roof)",
           {"kind": "teahouse", "size": "tateba", "roof": "itabuki"}, _LOOT_ROAD, 40000.0),
]
W2C_SMITHIES = [
    # TR11 smithy (open front, koyagumi, smoke vent) x roof; the swordsmith with the darkened forge room
    _civic("smithy_open_itabuki", "smithy", "Land_JP_Smithy_Open_Itabuki", "Smithy (kaji-ya, open front, boards)",
           {"kind": "smithy", "form": "open", "roof": "itabuki"}, _LOOT_SMITH, 20000.0),
    _civic("smithy_open_sangawara", "smithy", "Land_JP_Smithy_Open_Sangawara", "Smithy (kaji-ya, open front, tiled)",
           {"kind": "smithy", "form": "open", "roof": "sangawara"}, _LOOT_SMITH, 25000.0),
    _civic("swordsmith_sangawara", "smithy", "Land_JP_Swordsmith_Sangawara",
           "Swordsmith (katana-kaji): work room + darkened forge room, tiled",
           {"kind": "smithy", "form": "sword", "roof": "sangawara"}, _LOOT_SMITH, 40000.0),
]
W2C_GUARDHUTS = [
    # GV1 guard hut (kido-ban, jishin-ban, tsuji-ban, bridge / ferry / border / water guard: the props decide)
    _civic("guardhut_s_itabuki", "guardhut", "Land_JP_Guardhut_S_Itabuki", "Guard hut (6 x 9 shaku, boards)",
           {"kind": "guardhut", "size": "s", "roof": "itabuki"}, _LOOT_GUARD, 5000.0),
    _civic("guardhut_s_sangawara", "guardhut", "Land_JP_Guardhut_S_Sangawara", "Guard hut (6 x 9 shaku, tiled)",
           {"kind": "guardhut", "size": "s", "roof": "sangawara"}, _LOOT_GUARD, 6000.0),
    _civic("guardhut_m_itabuki", "guardhut", "Land_JP_Guardhut_M_Itabuki",
           "Guard hut, larger (self-watch post / jishin-ban, boards)", {"kind": "guardhut", "size": "m",
                                                                          "roof": "itabuki"}, _LOOT_GUARD, 8000.0),
]
W2C_KIDO = [
    # GV7 ward gate (kido): leaves (lattice / boards) x head (kasagi / small board roof) x the kido-ban hut
    _civic("kido_lattice", "kido", "Land_JP_Kido_Lattice", "Ward gate (kido, lattice leaves)",
           {"kind": "kido", "leaves": "lattice"}, _LOOT_GUARD, 6000.0),
    _civic("kido_board_roofed", "kido", "Land_JP_Kido_Board_Roofed", "Ward gate (kido, board leaves, small roof)",
           {"kind": "kido", "leaves": "board", "roofed": True}, _LOOT_GUARD, 7000.0),
    _civic("kido_lattice_bantaya", "kido", "Land_JP_Kido_Lattice_Bantaya",
           "Ward gate (kido, lattice leaves) with the gatekeeper's hut (kido-ban)",
           {"kind": "kido", "leaves": "lattice", "hut": "right"}, _LOOT_GUARD, 11000.0),
]
BUILDINGS += W2C_TEAHOUSES + W2C_SMITHIES + W2C_GUARDHUTS + W2C_KIDO


# ------------------------------------------------------------------------------------------------ W2S shrine + temple
# Phase C wave 2 (agent W2S, 2026-10-01): bare shrine + temple shells, village and town grades, from
# parts/kit/jpparts/templates/sacred.py (buildings/sacredkit.py builds them, buildings/shellcheck.py checks them; research
# notes spikes/W2S/W2S_NOTES.md). Not placed on the island (W2F furnishes and places them): shipped in jp_buildings.pbo.
from jpparts.templates import sacred as _sa  # noqa: E402

_LOOT_SHRINE = {"usage": ["Village", "Town"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_LOOT_TEMPLE = {"usage": ["Village", "Town"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}


def _sacred(key, dir_, cls, display, params, loot, mass):
    return {"key": key, "dir": dir_, "module": "sacred_shells", "class": cls, "name": "jp_" + key, "display": display,
            "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
            "placements": [], "verify": "shellcheck", "budget": _sa.budget_class(**params), "ship": True,
            **({"over_budget_ok": _sa.over_budget_ok(**params)} if _sa.over_budget_ok(**params) else {})}


W2S_SHRINE = [
    # SH2 worship hall (haiden)
    _sacred("shrine_haiden_village", "shrine", "Land_JP_Shrine_Haiden_Village",
            "Shrine worship hall (haiden), village: 3 x 2 ken, board roof", {"kind": "haiden", "grade": "village"},
            _LOOT_SHRINE, 30000.0),
    _sacred("shrine_haiden_town_hiwada", "shrine", "Land_JP_Shrine_Haiden_Town_Hiwada",
            "Shrine worship hall (haiden), town: curved cypress-bark roof, brackets",
            {"kind": "haiden", "grade": "town", "cover": "hiwada"}, _LOOT_SHRINE, 50000.0),
    _sacred("shrine_haiden_town_copper", "shrine", "Land_JP_Shrine_Haiden_Town_Copper",
            "Shrine worship hall (haiden), town: curved copper roof, brackets",
            {"kind": "haiden", "grade": "town", "cover": "copper"}, _LOOT_SHRINE, 50000.0),
    # SH3 main sanctuary (honden), sealed
    _sacred("shrine_honden_nagare_village", "shrine", "Land_JP_Shrine_Honden_Nagare_Village",
            "Shrine main sanctuary (honden), nagare, village", {"kind": "honden", "style": "nagare", "grade": "village"},
            _LOOT_SHRINE, 12000.0),
    _sacred("shrine_honden_nagare_village_chigi", "shrine", "Land_JP_Shrine_Honden_Nagare_Village_Chigi",
            "Shrine main sanctuary (honden), nagare with chigi + katsuogi, village",
            {"kind": "honden", "style": "nagare", "grade": "village", "chigi": True}, _LOOT_SHRINE, 12000.0),
    _sacred("shrine_honden_nagare_town", "shrine", "Land_JP_Shrine_Honden_Nagare_Town",
            "Shrine main sanctuary (honden), nagare sangen-sha, curved cypress-bark roof",
            {"kind": "honden", "style": "nagare", "grade": "town"}, _LOOT_SHRINE, 25000.0),
    _sacred("shrine_honden_shinmei", "shrine", "Land_JP_Shrine_Honden_Shinmei",
            "Shrine main sanctuary (honden), shinmei with chigi + katsuogi", {"kind": "honden", "style": "shinmei"},
            _LOOT_SHRINE, 12000.0),
    # SH5 purification pavilion (temizuya)
    _sacred("shrine_temizuya_village", "shrine", "Land_JP_Shrine_Temizuya_Village",
            "Purification pavilion (temizuya), village: four posts, board roof", {"kind": "temizuya", "grade": "village"},
            _LOOT_SHRINE, 4000.0),
    _sacred("shrine_temizuya_town", "shrine", "Land_JP_Shrine_Temizuya_Town",
            "Purification pavilion (temizuya), town: curved tile roof on brackets", {"kind": "temizuya", "grade": "town"},
            _LOOT_SHRINE, 8000.0),
    # SH6 priests' office + amulet window
    _sacred("shrine_shamusho_itabuki", "shrine", "Land_JP_Shrine_Shamusho_Itabuki",
            "Shrine priests' office with the amulet window (village, boards)", {"kind": "shamusho", "roof": "itabuki"},
            _LOOT_SHRINE, 15000.0),
    _sacred("shrine_shamusho_sangawara", "shrine", "Land_JP_Shrine_Shamusho_Sangawara",
            "Shrine priests' office with the amulet window (town, tiled)", {"kind": "shamusho", "roof": "sangawara"},
            _LOOT_SHRINE, 20000.0),
    # SH4 kagura stage
    _sacred("shrine_kagura_village", "shrine", "Land_JP_Shrine_Kagura_Village",
            "Kagura dance stage (kagura-den), village", {"kind": "kagura", "grade": "village"}, _LOOT_SHRINE, 12000.0),
    _sacred("shrine_kagura_town", "shrine", "Land_JP_Shrine_Kagura_Town",
            "Kagura dance stage (kagura-den), town: curved roof on brackets", {"kind": "kagura", "grade": "town"},
            _LOOT_SHRINE, 18000.0),
]
W2S_TEMPLE = [
    # BU1 small sacred hall (do): Jizo / Kannon / Yakushi / Koshin / Enma halls, the village assembly hall
    _sacred("temple_do_2_board", "temple", "Land_JP_Temple_Do_2_Board",
            "Small sacred hall (do), 2 x 2 ken, board hogyo roof", {"kind": "do", "size": 2, "roof": "board"},
            _LOOT_TEMPLE, 20000.0),
    _sacred("temple_do_2_thatch", "temple", "Land_JP_Temple_Do_2_Thatch",
            "Small sacred hall (do), 2 x 2 ken, thatched hogyo roof", {"kind": "do", "size": 2, "roof": "thatch"},
            _LOOT_TEMPLE, 20000.0),
    _sacred("temple_do_3_tile", "temple", "Land_JP_Temple_Do_3_Tile",
            "Small sacred hall (do), 3 x 3 ken, tiled hogyo roof", {"kind": "do", "size": 3, "roof": "tile"},
            _LOOT_TEMPLE, 40000.0),
    _sacred("temple_do_town", "temple", "Land_JP_Temple_Do_Town",
            "Small sacred hall (do), town: 3 x 3 bays, curved copper hogyo roof, brackets", {"kind": "do", "grade": "town"},
            _LOOT_TEMPLE, 50000.0),
    # BU2 main hall (hondo)
    _sacred("temple_hondo_village", "temple", "Land_JP_Temple_Hondo_Village",
            "Temple main hall (hondo), village: 4 x 4 ken, tiled irimoya", {"kind": "hondo", "grade": "village"},
            _LOOT_TEMPLE, 70000.0),
    _sacred("temple_hondo_town", "temple", "Land_JP_Temple_Hondo_Town",
            "Temple main hall (hondo), town: 3 x 3 bays, curved hongawara, degumi brackets",
            {"kind": "hondo", "grade": "town"}, _LOOT_TEMPLE, 90000.0),
    # BU3 priests' quarters + kitchen (kuri)
    _sacred("temple_kuri_village", "temple", "Land_JP_Temple_Kuri_Village",
            "Temple priests' quarters + kitchen (kuri), village: thatch, genkan porch", {"kind": "kuri", "grade": "village"},
            _LOOT_TEMPLE, 60000.0),
    _sacred("temple_kuri_town", "temple", "Land_JP_Temple_Kuri_Town",
            "Temple priests' quarters + kitchen (kuri), town: tiled, genkan porch", {"kind": "kuri", "grade": "town"},
            _LOOT_TEMPLE, 70000.0),
    # BU6 bell tower (shoro)
    _sacred("temple_shoro_village", "temple", "Land_JP_Temple_Shoro_Village",
            "Temple bell tower (shoro), village: open four-post", {"kind": "shoro", "grade": "village"}, _LOOT_TEMPLE,
            15000.0),
    _sacred("temple_shoro_town", "temple", "Land_JP_Temple_Shoro_Town",
            "Temple bell tower (shoro), town: hakama skirt, curved roof, brackets", {"kind": "shoro", "grade": "town"},
            _LOOT_TEMPLE, 30000.0),
    # BU5 small gate
    _sacred("temple_gate_yakuimon", "temple", "Land_JP_Temple_Gate_Yakuimon",
            "Temple small gate (yakui-mon), village: tiled", {"kind": "gate", "grade": "village"}, _LOOT_TEMPLE, 8000.0),
    _sacred("temple_gate_shikyakumon", "temple", "Land_JP_Temple_Gate_Shikyakumon",
            "Temple small gate (shikyaku-mon), town: curved tile roof, brackets", {"kind": "gate", "grade": "town"},
            _LOOT_TEMPLE, 12000.0),
]
BUILDINGS += W2S_SHRINE + W2S_TEMPLE


# ------------------------------------------------------------------------------------------------ W2F furnished
# Phase C wave 2 (agent W2F, 2026-10-01): furnished variants of the W2S / W2C shells (the C3 pattern, furnishkit; the
# dressings are buildings/w2f_sets.py, the specialty props spikes/W2F/props_w2f_*.py in jp_furniture). Placed on the
# test island by spikes/W2F/layout_w2f.py (test/placements/W2F.csv + test/ce/W2F_mapgrouppos.xml), NOT through
# 'placements' here (the shrine precinct lies outside the flat test yard that shellcheck's placement check guards).
W2F_FURNISHED = [
    _furn("f_shrine_haiden_town", "shrine_haiden_town_hiwada", "w2f_haiden_town", "Furnished",
          "furnished (Hachimangu: drum, offerings, bell rope, name board)"),
    _furn("f_shrine_haiden_village", "shrine_haiden_village", "w2f_haiden_village", "Furnished", "furnished"),
    _furn("f_shrine_honden_nagare_town", "shrine_honden_nagare_town", "w2f_honden_town", "Furnished",
          "furnished (offering table; the sealed sanctum dressed)"),
    _furn("f_shrine_honden_nagare_village_chigi", "shrine_honden_nagare_village_chigi", "w2f_honden_village",
          "Furnished", "furnished (offering table; the sealed sanctum dressed)"),
    _furn("f_shrine_temizuya_town", "shrine_temizuya_town", "w2f_temizuya", "Furnished", "furnished (basin, ladles)"),
    _furn("f_shrine_shamusho_sangawara", "shrine_shamusho_sangawara", "w2f_shamusho", "Furnished",
          "furnished (amulet counter, talisman desk)"),
    _furn("f_shrine_kagura_town", "shrine_kagura_town", "w2f_kagura", "Furnished", "furnished (drums, masks)"),
    _furn("f_temple_hondo_village", "temple_hondo_village", "w2f_hondo_village", "Jodo",
          "furnished, Jodo (Amida, sutra desk)"),
    _furn("f_temple_hondo_town", "temple_hondo_town", "w2f_hondo_town", "Zen", "furnished, Zen (Shaka, big mokugyo)"),
    _furn("f_temple_do_2_board", "temple_do_2_board", "w2f_do_jizo", "Jizo", "furnished: Jizo hall"),
    _furn("f_temple_do_3_tile", "temple_do_3_tile", "w2f_do_kannon", "Kannon", "furnished: Kannon hall"),
    _furn("f_temple_kuri_village", "temple_kuri_village", "w2f_kuri_village", "Furnished", "furnished"),
    _furn("f_temple_kuri_town", "temple_kuri_town", "w2f_kuri_town", "Zen", "furnished, Zen (fish board, cloud gong)"),
    _furn("f_temple_shoro_village", "temple_shoro_village", "w2f_shoro", "Bell", "with its bell"),
    _furn("f_temple_shoro_town", "temple_shoro_town", "w2f_shoro", "Bell", "with its bell"),
    _furn("f_temple_gate_yakuimon", "temple_gate_yakuimon", "w2f_gate", "Furnished", "with its name board"),
    _furn("f_temple_gate_shikyakumon", "temple_gate_shikyakumon", "w2f_gate", "Furnished", "with its name board"),
    _furn("f_teahouse_bench_itabuki", "teahouse_bench_itabuki", "w2f_teahouse_bench", "Furnished", "furnished"),
    _furn("f_teahouse_shop_thatch", "teahouse_shop_thatch", "w2f_teahouse_shop", "Furnished", "furnished"),
    _furn("f_teahouse_tateba_itabuki", "teahouse_tateba_itabuki", "w2f_teahouse_tateba", "Furnished", "furnished"),
    _furn("f_smithy_open_itabuki", "smithy_open_itabuki", "w2f_smithy", "Furnished", "furnished (cold forge)"),
    _furn("f_swordsmith_sangawara", "swordsmith_sangawara", "w2f_swordsmith", "Furnished", "furnished (cold forge)"),
    _furn("f_guardhut_m_itabuki", "guardhut_m_itabuki", "w2f_guardhut_m", "Jishinban",
          "furnished: self-watch post with the ridge fire ladder"),
    _furn("f_kido_lattice_bantaya", "kido_lattice_bantaya", "w2f_kido_bantaya", "Furnished",
          "furnished (ward lantern, the keeper's hut)"),
]
BUILDINGS += W2F_FURNISHED


# ------------------------------------------------------------------------------------------------ D3 dwellings
# Phase C wave 3a (agent D3, 2026-10-01): dwellings, outbuildings, gatehouses and the honjin from
# parts/kit/jpparts/templates/dwelling.py (buildings/dwellingkit.py builds them, buildings/shellcheck.py checks them;
# research notes spikes/D3/D3_NOTES.md). Placed on the test island by spikes/D3/layout_d3.py (test/placements/D3.csv +
# test/ce/D3_mapgrouppos.xml), not through 'placements' here (the compounds lie outside the flat test yard).
from jpparts.templates import dwelling as _dw  # noqa: E402

_LOOT_DW_RURAL = {"usage": ["Farm", "Village"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_LOOT_DW_TOWN = {"usage": ["Town", "Village"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_LOOT_DW_OUT = {"usage": ["Farm", "Village"], "categories": ["tools", "containers", "food"], "tags": ["floor"]}


def _dwl(key, dir_, cls, display, params, loot, mass):
    e = {"key": key, "dir": dir_, "module": "dwelling_shells", "class": cls, "name": "jp_" + key, "display": display,
         "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
         "placements": [], "verify": "shellcheck", "budget": _dw.budget_class(**params), "ship": True}
    ob = _dw.over_budget_ok(**params)
    if ob:
        e["over_budget_ok"] = ob
    return e


D3_SHELLS = [
    # DW08 mountain board-roof house (Kiso / Hida): roof x the woodshed lean-to
    _dwl("dw_mountain_ishioki", "dw_rural", "Land_JP_Mountain_Ishioki", "Mountain house (Kiso / Hida, stone-weighted "
         "board roof, hidana over the irori)", {"kind": "mountain", "roof": "ishioki"}, _LOOT_DW_RURAL, 50000.0),
    _dwl("dw_mountain_ishioki_lean", "dw_rural", "Land_JP_Mountain_Ishioki_Lean", "Mountain house with a woodshed "
         "lean-to (stone-weighted board roof)", {"kind": "mountain", "roof": "ishioki", "leanto": "left"},
         _LOOT_DW_RURAL, 55000.0),
    _dwl("dw_mountain_itabuki", "dw_rural", "Land_JP_Mountain_Itabuki", "Mountain house (board roof, no stones)",
         {"kind": "mountain", "roof": "itabuki"}, _LOOT_DW_RURAL, 50000.0),
    # DW09 coastal house (fisherman): roof x the net store lean-to
    _dwl("dw_coastal_ishioki", "dw_rural", "Land_JP_Coastal_Ishioki_NetStore", "Coastal house (fisherman, "
         "stone-weighted boards, net store)", {"kind": "coastal", "roof": "ishioki"}, _LOOT_DW_RURAL, 30000.0),
    _dwl("dw_coastal_thatch", "dw_rural", "Land_JP_Coastal_Thatch_NetStore", "Coastal house (fisherman, thatch, "
         "net store)", {"kind": "coastal", "roof": "thatch"}, _LOOT_DW_RURAL, 30000.0),
    # DW14 foot-soldier row (kumi-yashiki), one storey, 3 units
    _dwl("dw_kumi_itabuki", "dw_samurai", "Land_JP_KumiYashiki_3_Itabuki", "Foot-soldier row (ashigaru kumi-yashiki, "
         "3 units, board roof)", {"kind": "kumi", "units": 3, "roof": "itabuki"}, _LOOT_DW_TOWN, 60000.0),
    _dwl("dw_kumi_sangawara", "dw_samurai", "Land_JP_KumiYashiki_3_Sangawara", "Foot-soldier row (ashigaru "
         "kumi-yashiki, 3 units, tiled)", {"kind": "kumi", "units": 3, "roof": "sangawara"}, _LOOT_DW_TOWN, 65000.0),
    # DW15 small samurai house (doshin)
    _dwl("dw_doshin_itabuki", "dw_samurai", "Land_JP_Doshin_Itabuki", "Small samurai house (doshin, board roof)",
         {"kind": "doshin", "roof": "itabuki"}, _LOOT_DW_TOWN, 45000.0),
    _dwl("dw_doshin_sangawara", "dw_samurai", "Land_JP_Doshin_Sangawara", "Small samurai house (doshin, tiled)",
         {"kind": "doshin", "roof": "sangawara"}, _LOOT_DW_TOWN, 50000.0),
    # DW19 samurai mansion, three plot sizes
    _dwl("dw_samurai_s", "dw_samurai", "Land_JP_Samurai_S", "Samurai mansion, small plot (genkan + shikidai, "
         "zashiki with tokonoma)", {"kind": "samurai", "size": "s"}, _LOOT_DW_TOWN, 70000.0),
    _dwl("dw_samurai_m", "dw_samurai", "Land_JP_Samurai_M", "Samurai mansion, middle plot (hatamoto)",
         {"kind": "samurai", "size": "m"}, _LOOT_DW_TOWN, 80000.0),
    _dwl("dw_samurai_l", "dw_samurai", "Land_JP_Samurai_L", "Samurai mansion, large plot (karo)",
         {"kind": "samurai", "size": "l"}, _LOOT_DW_TOWN, 100000.0),
    # DW18 great merchant residence
    _dwl("dw_merchant", "dw_upper", "Land_JP_Merchant_Residence", "Great merchant residence (odana no oku)",
         {"kind": "merchant"}, _LOOT_DW_TOWN, 80000.0),
    # KEEP_TRADES 6: honjin (two blocks) + waki-honjin
    _dwl("dw_honjin_omote", "dw_honjin", "Land_JP_Honjin_Omote", "Honjin (lords' inn): formal block with the "
         "jodan-no-ma", {"kind": "honjin_omote"}, _LOOT_DW_TOWN, 90000.0),
    _dwl("dw_honjin_oku", "dw_honjin", "Land_JP_Honjin_Oku", "Honjin (lords' inn): family and kitchen block",
         {"kind": "honjin_oku"}, _LOOT_DW_TOWN, 80000.0),
    _dwl("dw_wakihonjin", "dw_honjin", "Land_JP_Wakihonjin", "Waki-honjin (deputy lords' inn)",
         {"kind": "wakihonjin"}, _LOOT_DW_TOWN, 90000.0),
    # DW16 / DW17 headman houses
    _dwl("dw_headman_east", "dw_upper", "Land_JP_Headman_East", "Headman house, Kanto (nanushi: hipped thatch, "
         "shikidai genkan, formal zashiki)", {"kind": "headman_east", "ridge": "umanori"}, _LOOT_DW_RURAL, 100000.0),
    _dwl("dw_headman_east_shiba", "dw_upper", "Land_JP_Headman_East_Shiba", "Headman house, Kanto (shiba ridge)",
         {"kind": "headman_east", "ridge": "shiba"}, _LOOT_DW_RURAL, 100000.0),
    _dwl("dw_headman_kinai", "dw_upper", "Land_JP_Headman_Kinai", "Headman house, Kinai (shoya: thatch + tile, "
         "white plaster, the genkan lean-to)", {"kind": "headman_kinai"}, _LOOT_DW_RURAL, 100000.0),
    # DW21 tea hut
    _dwl("dw_chashitsu_thatch", "dw_upper", "Land_JP_Chashitsu_Thatch", "Tea hut (soan, thatch)",
         {"kind": "chashitsu", "roof": "thatch"}, _LOOT_DW_TOWN, 12000.0),
    _dwl("dw_chashitsu_kokera", "dw_upper", "Land_JP_Chashitsu_Kokera", "Tea hut (soan, shingle roof)",
         {"kind": "chashitsu", "roof": "kokera"}, _LOOT_DW_TOWN, 12000.0),
    # DW23 / DW25 / DW27 outbuildings
    _dwl("dw_itagura_itabuki", "dw_out", "Land_JP_Itagura_Itabuki", "Board storehouse (itagura) on rat-guarded posts",
         {"kind": "itagura", "roof": "itabuki"}, _LOOT_DW_OUT, 8000.0),
    _dwl("dw_itagura_sangawara", "dw_out", "Land_JP_Itagura_Sangawara", "Board storehouse (itagura), tiled",
         {"kind": "itagura", "roof": "sangawara"}, _LOOT_DW_OUT, 9000.0),
    _dwl("dw_stable_horse", "dw_out", "Land_JP_Stable_Horse", "Stable (two horse stalls, board roof)",
         {"kind": "stable", "animal": "horse"}, _LOOT_DW_OUT, 15000.0),
    _dwl("dw_stable_ox", "dw_out", "Land_JP_Stable_Ox", "Ox shed (thatch)", {"kind": "stable", "animal": "ox"},
         _LOOT_DW_OUT, 10000.0),
    _dwl("dw_furoba", "dw_out", "Land_JP_Furoba", "Bath hut (furoba)", {"kind": "furoba"}, _LOOT_DW_OUT, 5000.0),
    # DW29 gatehouse with rooms
    _dwl("dw_nagayamon_samurai", "dw_samurai", "Land_JP_NagayaMon_Samurai", "Gatehouse with rooms (nagaya-mon), "
         "samurai: plaster + namako, tiled", {"kind": "nagayamon", "rank": "samurai"}, _LOOT_DW_TOWN, 40000.0),
    _dwl("dw_nagayamon_headman", "dw_upper", "Land_JP_NagayaMon_Headman", "Gatehouse with rooms (nagaya-mon), "
         "headman: boards", {"kind": "nagayamon", "rank": "headman"}, _LOOT_DW_RURAL, 30000.0),
]
BUILDINGS += D3_SHELLS

# D3 furnished variants (the C3 / W2F pattern: furnishkit + buildings/d3_sets.py), one per type
D3_FURNISHED = [
    _furn("f_dw_mountain", "dw_mountain_ishioki", "d3_mountain", "Furnished", "furnished (snow gear, hidana)"),
    _furn("f_dw_coastal", "dw_coastal_ishioki", "d3_coastal", "Furnished", "furnished (nets, the net store)"),
    _furn("f_dw_kumi", "dw_kumi_itabuki", "d3_kumi", "Furnished", "furnished (three units)"),
    _furn("f_dw_doshin", "dw_doshin_itabuki", "d3_doshin", "Furnished", "furnished"),
    _furn("f_dw_samurai_m", "dw_samurai_m", "d3_samurai", "Furnished", "furnished (armour chest, sword stand)"),
    _furn("f_dw_merchant", "dw_merchant", "d3_merchant", "Furnished", "furnished (money chest, ledgers)"),
    _furn("f_dw_honjin_omote", "dw_honjin_omote", "d3_honjin_omote", "Furnished", "furnished (the lord's suite)"),
    _furn("f_dw_honjin_oku", "dw_honjin_oku", "d3_honjin_oku", "Furnished", "furnished (the big kitchen)"),
    _furn("f_dw_wakihonjin", "dw_wakihonjin", "d3_wakihonjin", "Furnished", "furnished"),
    _furn("f_dw_headman_east", "dw_headman_east", "d3_headman_east", "Furnished", "furnished (village registers)"),
    _furn("f_dw_headman_kinai", "dw_headman_kinai", "d3_headman_kinai", "Furnished", "furnished (village business)"),
    _furn("f_dw_chashitsu", "dw_chashitsu_thatch", "d3_chashitsu", "Furnished", "furnished (as left after tea)"),
    _furn("f_dw_itagura", "dw_itagura_itabuki", "d3_itagura", "Furnished", "furnished (grain)"),
    _furn("f_dw_stable", "dw_stable_horse", "d3_stable", "Furnished", "furnished (mangers, tack)"),
    _furn("f_dw_furoba", "dw_furoba", "d3_furoba", "Furnished", "furnished"),
    _furn("f_dw_nagayamon", "dw_nagayamon_samurai", "d3_nagayamon", "Furnished", "furnished (servants' room)"),
]
# D3 compounds (K3's wall kit: walls / fences / hedges + gates) and covered corridors (K3's roka kit), one object each
_LOOT_DW_GATE = {"usage": ["Village", "Town"], "categories": ["tools", "containers"], "tags": ["floor"]}
D3_SITE = [
    _dwl("dw_cmp_samurai_m", "dw_site", "Land_JP_Compound_Samurai_M", "Samurai mansion compound: black board fence, "
         "back wicket (the nagaya-mon stands in the front gap)", {"kind": "compound", "plot": "samurai_m"}, _LOOT_DW_GATE,
         20000.0),
    _dwl("dw_cmp_headman_east", "dw_site", "Land_JP_Compound_Headman_East", "Headman compound: clipped hedge (the "
         "board nagaya-mon stands in the front gap)", {"kind": "compound", "plot": "headman_east"}, _LOOT_DW_GATE, 20000.0),
    _dwl("dw_cmp_honjin", "dw_site", "Land_JP_Compound_Honjin", "Honjin compound: plastered street wall + the roofed "
         "kabuki-mon, board fence round the sides and back, a back gate", {"kind": "compound", "plot": "honjin"},
         _LOOT_DW_GATE, 30000.0),
    _dwl("dw_cmp_merchant", "dw_site", "Land_JP_Compound_Merchant", "Merchant garden: board fence + wicket",
         {"kind": "compound", "plot": "merchant"}, _LOOT_DW_GATE, 20000.0),
    _dwl("dw_cmp_kumi", "dw_site", "Land_JP_Compound_KumiYashiki", "Foot-soldier row front: bamboo fence + gate",
         {"kind": "compound", "plot": "kumi"}, _LOOT_DW_GATE, 5000.0),
    _dwl("dw_cmp_doshin", "dw_site", "Land_JP_Compound_Doshin", "Doshin plot: board fence + kabuki gate",
         {"kind": "compound", "plot": "doshin"}, _LOOT_DW_GATE, 10000.0),
    _dwl("dw_roka_honjin", "dw_site", "Land_JP_Roka_Honjin", "Covered corridor (watari-roka): honjin omote <-> oku",
         {"kind": "roka", "run": "honjin"}, _LOOT_DW_GATE, 8000.0),
    _dwl("dw_roka_temple_u", "dw_site", "Land_JP_Roka_Temple_U", "Covered corridor (watari-roka): town temple hondo "
         "<-> kuri genkan", {"kind": "roka", "run": "temple_u"}, _LOOT_DW_GATE, 8000.0),
]
BUILDINGS += D3_SITE

for _f in D3_FURNISHED:                       # D3's own model folder (batch binarize, no noise in C3 / W2F's)
    _f["dir"] = _f["model_dir"] = "dw_furnished"
BUILDINGS += D3_FURNISHED


# ------------------------------------------------------------------------------------------------ W3B workshops + services
# Phase C wave 3b (agent W3B, 2026-10-02): the public bathhouse, the stable row + yard, the barber's and show booths,
# the earth-floor and raised-floor workshops, the timber-yard sheds, the foundry and the yard fences, from
# parts/kit/jpparts/templates/trade.py (buildings/tradekit.py builds them, buildings/shellcheck.py checks them; research
# notes spikes/W3B/W3B_NOTES.md). Placed on the test island by spikes/W3B/layout_w3b.py (test/placements/W3B.csv +
# test/ce/W3B_mapgrouppos.xml), not through 'placements' here.
from jpparts.templates import trade as _tr  # noqa: E402

_LOOT_TR_TOWN = {"usage": ["Town", "Village"], "categories": ["tools", "containers", "clothes", "food"], "tags": ["floor"]}
_LOOT_TR_WORK = {"usage": ["Town", "Village"], "categories": ["tools", "containers"], "tags": ["floor"]}
_LOOT_TR_YARD = {"usage": ["Village", "Town"], "categories": ["tools", "containers"], "tags": ["floor"]}


def _trd(key, dir_, cls, display, params, loot, mass):
    e = {"key": key, "dir": dir_, "module": "trade_shells", "class": cls, "name": "jp_" + key, "display": display,
         "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
         "placements": [], "verify": "shellcheck", "budget": _tr.budget_class(**params), "ship": True}
    ob = _tr.over_budget_ok(**params)
    if ob:
        e["over_budget_ok"] = ob
    return e


W3B_SHELLS = [
    # TR08 public bathhouse: entrance doma + bandai, changing room + washing floor, the zakuro-guchi, the bath room,
    # the boiler lean-to; town (tiled) / board roof
    _trd("tr_sento_sangawara", "tr_sento", "Land_JP_Sento_Sangawara", "Public bathhouse (sento, zakuro-guchi bath, "
         "tiled)", {"kind": "sento", "roof": "sangawara"}, _LOOT_TR_TOWN, 60000.0),
    _trd("tr_sento_itabuki", "tr_sento", "Land_JP_Sento_Itabuki", "Public bathhouse (sento, zakuro-guchi bath, "
         "board roof)", {"kind": "sento", "roof": "itabuki"}, _LOOT_TR_TOWN, 55000.0),
    # TR09 stable row (four stalls + the tack room)
    _trd("tr_stablerow_itabuki", "tr_stable", "Land_JP_StableRow_Itabuki", "Stable row: four stalls open to the yard, "
         "tack room (post town, board roof)", {"kind": "stablerow", "roof": "itabuki"}, _LOOT_TR_YARD, 30000.0),
    _trd("tr_stablerow_thatch", "tr_stable", "Land_JP_StableRow_Thatch", "Stable row: four stalls, tack room "
         "(packhorse carrier, thatch)", {"kind": "stablerow", "roof": "thatch"}, _LOOT_TR_YARD, 30000.0),
    # TR02 the booths that are buildings
    _trd("tr_booth_barber", "tr_booth", "Land_JP_Booth_Barber", "Barber's booth (de-doko)",
         {"kind": "booth", "form": "barber"}, _LOOT_TR_TOWN, 5000.0),
    _trd("tr_booth_misemono", "tr_booth", "Land_JP_Booth_Misemono", "Show booth (misemono-goya): mat walls, stage",
         {"kind": "booth", "form": "misemono"}, _LOOT_TR_TOWN, 8000.0),
    # TR13 earth-floor workshop / TR14 raised-floor bench workshop
    _trd("tr_ws_doma_itabuki", "tr_workshop", "Land_JP_Workshop_Doma_Itabuki", "Earth-floor workshop (board roof)",
         {"kind": "workshop", "form": "doma", "roof": "itabuki"}, _LOOT_TR_WORK, 20000.0),
    _trd("tr_ws_doma_sangawara", "tr_workshop", "Land_JP_Workshop_Doma_Sangawara", "Earth-floor workshop (tiled)",
         {"kind": "workshop", "form": "doma", "roof": "sangawara"}, _LOOT_TR_WORK, 24000.0),
    _trd("tr_ws_bench_itabuki", "tr_workshop", "Land_JP_Workshop_Bench_Itabuki", "Raised-floor bench workshop with the "
         "dust-free back room (board roof)", {"kind": "workshop", "form": "bench", "roof": "itabuki"}, _LOOT_TR_WORK,
         25000.0),
    _trd("tr_ws_bench_sangawara", "tr_workshop", "Land_JP_Workshop_Bench_Sangawara", "Raised-floor bench workshop "
         "with the dust-free back room (tiled)", {"kind": "workshop", "form": "bench", "roof": "sangawara"},
         _LOOT_TR_WORK, 30000.0),
    # TR15 timber yard sheds
    _trd("tr_timber_saw", "tr_timber", "Land_JP_Timber_SawShed", "Timber yard: the sawing shed (open)",
         {"kind": "timbershed", "form": "saw"}, _LOOT_TR_YARD, 8000.0),
    _trd("tr_timber_store", "tr_timber", "Land_JP_Timber_Store", "Timber yard: the timber store (upright timber)",
         {"kind": "timbershed", "form": "store"}, _LOOT_TR_YARD, 9000.0),
    _trd("tr_timber_shingle", "tr_timber", "Land_JP_Timber_ShingleShed", "Timber yard: the shingle splitter's shed",
         {"kind": "timbershed", "form": "shingle"}, _LOOT_TR_YARD, 5000.0),
    # TR12 foundry
    _trd("tr_foundry_itabuki", "tr_foundry", "Land_JP_Foundry_Itabuki", "Foundry (imoji: cupola furnace, treadle "
         "bellows, sand casting floor; board roof)", {"kind": "foundry", "roof": "itabuki"}, _LOOT_TR_WORK, 30000.0),
    _trd("tr_foundry_sangawara", "tr_foundry", "Land_JP_Foundry_Sangawara", "Foundry (imoji, tiled)",
         {"kind": "foundry", "roof": "sangawara"}, _LOOT_TR_WORK, 35000.0),
    # the yard fences (K3's wall kit)
    _trd("tr_cmp_stableyard", "tr_site", "Land_JP_Compound_StableYard", "Stable yard: board fence + wide gate",
         {"kind": "compound", "plot": "stableyard"}, _LOOT_TR_YARD, 15000.0),
    _trd("tr_cmp_timberyard", "tr_site", "Land_JP_Compound_TimberYard", "Timber yard: board fence + wide gate",
         {"kind": "compound", "plot": "timberyard"}, _LOOT_TR_YARD, 25000.0),
    _trd("tr_cmp_foundryyard", "tr_site", "Land_JP_Compound_FoundryYard", "Foundry yard: board fence + gate",
         {"kind": "compound", "plot": "foundryyard"}, _LOOT_TR_YARD, 15000.0),
]
BUILDINGS += W3B_SHELLS

# W3B furnished variants (the C3 / W2F / D3 pattern: furnishkit + buildings/w3b_sets.py)
W3B_FURNISHED = [
    _furn("f_tr_sento", "tr_sento_sangawara", "w3b_sento", "Furnished", "furnished (bandai, cubbies, the drained tub)"),
    _furn("f_tr_stablerow", "tr_stablerow_itabuki", "w3b_stablerow", "Furnished", "furnished (tack, fodder)"),
    _furn("f_tr_booth_barber", "tr_booth_barber", "w3b_barber", "Furnished", "furnished (the barber's kit)"),
    _furn("f_tr_booth_misemono", "tr_booth_misemono", "w3b_misemono", "Furnished", "furnished (cage, benches, sign)"),
    _furn("f_tr_ws_joinery", "tr_ws_doma_sangawara", "w3b_joinery", "Joinery", "furnished: joiner"),
    _furn("f_tr_ws_turner", "tr_ws_doma_itabuki", "w3b_turner", "Turner", "furnished: woodturner + abacus maker"),
    _furn("f_tr_ws_basket", "tr_ws_doma_itabuki", "w3b_basket", "Basket", "furnished: bamboo + basket maker"),
    _furn("f_tr_ws_polisher", "tr_ws_bench_sangawara", "w3b_polisher", "Polisher", "furnished: sword polisher"),
    _furn("f_tr_ws_lacquer", "tr_ws_bench_itabuki", "w3b_lacquer", "Lacquer", "furnished: lacquerer"),
    _furn("f_tr_ws_kinko", "tr_ws_bench_sangawara", "w3b_kinko", "Kinko", "furnished: sword-fittings maker"),
    _furn("f_tr_timber_saw", "tr_timber_saw", "w3b_saw_shed", "Furnished", "furnished (the sawing trestle)"),
    _furn("f_tr_timber_store", "tr_timber_store", "w3b_timber_store", "Furnished", "furnished (upright timber, planks)"),
    _furn("f_tr_timber_shingle", "tr_timber_shingle", "w3b_shingle_shed", "Furnished", "furnished (splitting block)"),
    _furn("f_tr_foundry", "tr_foundry_itabuki", "w3b_foundry", "Furnished", "furnished (cupola, bellows, moulds)"),
]
for _f in W3B_FURNISHED:                      # W3B's own model folder
    _f["dir"] = _f["model_dir"] = "tr_furnished"
BUILDINGS += W3B_FURNISHED


# ------------------------------------------------------------------------------------------------ W3C1 trade sites
# Phase C wave 3c-1 (agent W3C1, 2026-10-02): the sake brewery complex (the kasane-gura: o-kura + mae-gura, the
# rice-polishing shed), the water mill, the indigo dyer, the paper mill and their yards, from
# parts/kit/jpparts/templates/tradesite.py (buildings/tradesitekit.py builds them, buildings/shellcheck.py checks them;
# research + recorded choices spikes/W3C1/W3C1_NOTES.md). Placed in the trade quarter south-west of the yard by
# spikes/W3C1/layout_w3c1.py (test/placements/W3C1.csv + test/ce/W3C1_mapgrouppos.xml), not through 'placements'.
from jpparts.templates import tradesite as _ts  # noqa: E402

_LOOT_TS_WORK = {"usage": ["Town", "Village"], "categories": ["tools", "containers", "food"], "tags": ["floor"]}
_LOOT_TS_YARD = {"usage": ["Village", "Town"], "categories": ["tools", "containers"], "tags": ["floor"]}


def _tsd(key, dir_, cls, display, params, loot, mass):
    e = {"key": key, "dir": dir_, "module": "tradesite_shells", "class": cls, "name": "jp_" + key, "display": display,
         "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
         "placements": [], "verify": "shellcheck", "budget": _ts.budget_class(**params), "ship": True}
    ob = _ts.over_budget_ok(**params)
    if ob:
        e["over_budget_ok"] = ob
    return e


W3C1_SHELLS = [
    # TR03 the sake brewery: the kasane-gura (o-kura north, mae-gura south), the rice-polishing shed
    _tsd("ts_okura", "ts_brewery", "Land_JP_SakaGura_Okura", "Sake brewery: the large kura (o-kura: fermentation "
         "floor, press bay, the starter loft)", {"kind": "okura"}, _LOOT_TS_WORK, 120000.0),
    _tsd("ts_maegura", "ts_brewery", "Land_JP_SakaGura_Maegura", "Sake brewery: the front kura (mae-gura: washing, "
         "steaming hearth, koji room, brewers' rest room)", {"kind": "maegura"}, _LOOT_TS_WORK, 90000.0),
    _tsd("ts_seimai", "ts_brewery", "Land_JP_SakaGura_Seimai", "Sake brewery: the rice-polishing shed (foot-treadle "
         "mortars)", {"kind": "seimai"}, _LOOT_TS_YARD, 12000.0),
    # TR04 the water mill (overshot wheel, flume, stamps)
    _tsd("ts_suisha_itabuki", "ts_mill", "Land_JP_Suisha_Itabuki", "Water mill (overshot wheel, flume, stamps; board "
         "roof)", {"kind": "suisha", "roof": "itabuki"}, _LOOT_TS_YARD, 20000.0),
    _tsd("ts_suisha_thatch", "ts_mill", "Land_JP_Suisha_Thatch", "Water mill (overshot wheel, flume, stamps; thatch)",
         {"kind": "suisha", "roof": "thatch"}, _LOOT_TS_YARD, 20000.0),
    # TR17 the indigo dyer (sunk vats)
    _tsd("ts_konya_sangawara", "ts_dyer", "Land_JP_Konya_Sangawara", "Indigo dyer (kon'ya: shop + vat room with four "
         "sunk vats; tiled)", {"kind": "konya", "roof": "sangawara"}, _LOOT_TS_WORK, 30000.0),
    _tsd("ts_konya_itabuki", "ts_dyer", "Land_JP_Konya_Itabuki", "Indigo dyer (kon'ya; board roof)",
         {"kind": "konya", "roof": "itabuki"}, _LOOT_TS_WORK, 26000.0),
    # TR21 the paper mill
    _tsd("ts_kamisuki_itabuki", "ts_paper", "Land_JP_KamiSuki_Itabuki", "Paper mill (kami-suki-ba; board roof)",
         {"kind": "kamisuki", "roof": "itabuki"}, _LOOT_TS_WORK, 22000.0),
    _tsd("ts_kamisuki_thatch", "ts_paper", "Land_JP_KamiSuki_Thatch", "Paper mill (kami-suki-ba; thatch)",
         {"kind": "kamisuki", "roof": "thatch"}, _LOOT_TS_WORK, 22000.0),
    # the yards (K3's wall kit)
    _tsd("ts_cmp_brewery", "ts_site", "Land_JP_Compound_Brewery", "Sake brewery yard: black board fence + wide gate",
         {"kind": "compound", "plot": "brewery"}, _LOOT_TS_YARD, 25000.0),
    _tsd("ts_cmp_dyersyard", "ts_site", "Land_JP_Compound_DyersYard", "Dyer's drying yard: board fence + gate",
         {"kind": "compound", "plot": "dyersyard"}, _LOOT_TS_YARD, 15000.0),
    _tsd("ts_cmp_paperyard", "ts_site", "Land_JP_Compound_PaperYard", "Paper mill drying yard: bamboo fence + gate",
         {"kind": "compound", "plot": "paperyard"}, _LOOT_TS_YARD, 12000.0),
]
BUILDINGS += W3C1_SHELLS

# W3C1 furnished variants (the C3 / W2F / D3 / W3B pattern: furnishkit + buildings/w3c1_sets.py); the cask kura and the
# brewer's shop are earlier shells (C3's plain kura, W3B's tiled earth-floor workshop) dressed for the brewery
W3C1_FURNISHED = [
    _furn("f_ts_okura", "ts_okura", "w3c1_okura", "Furnished", "furnished (big tubs, the lever press, starter loft)"),
    _furn("f_ts_maegura", "ts_maegura", "w3c1_maegura", "Furnished", "furnished (steaming hearth, koji room, rest room)"),
    _furn("f_ts_seimai", "ts_seimai", "w3c1_seimai", "Furnished", "furnished (four treadle mortars)"),
    _furn("f_ts_kura_casks", "kura_plain", "w3c1_kura_casks", "SakeCasks", "furnished: the brewery's cask store"),
    _furn("f_ts_sakaya", "tr_ws_doma_sangawara", "w3c1_sakaya", "Sakaya", "furnished: the brewer's shop (sugidama)"),
    _furn("f_ts_suisha", "ts_suisha_itabuki", "w3c1_suisha", "Furnished", "furnished (hand quern, bales)"),
    _furn("f_ts_konya", "ts_konya_sangawara", "w3c1_konya", "Furnished", "furnished (sukumo, lye tubs, shop cloths)"),
    _furn("f_ts_kamisuki", "ts_kamisuki_thatch", "w3c1_kamisuki", "Furnished", "furnished (vat, beating board, press)"),
]
for _f in W3C1_FURNISHED:                     # W3C1's own model folder
    _f["dir"] = _f["model_dir"] = "ts_furnished"
BUILDINGS += W3C1_FURNISHED


# ------------------------------------------------------------------------------------------------ W3C2 rural sites
# Phase C wave 3c-2 (agent W3C2, 2026-10-02): the rural / industrial trade sites (charcoal, pottery, tile works, lime,
# quarry + stonemason, mine, logging camp, salt works) from parts/kit/jpparts/templates/ruralsite.py (buildings/
# ruralsitekit.py builds them; research + recorded choices spikes/W3C2/W3C2_NOTES.md). The huts and sheds a site reuses
# are earlier shells furnished in buildings/w3c2_sets.py. Placed in ONE district west + south of 3c-1 by
# spikes/W3C2/layout_w3c2.py (test/placements/W3C2.csv + test/ce/W3C2_mapgrouppos.xml), not through 'placements'.
from jpparts.templates import ruralsite as _rs  # noqa: E402

_LOOT_RS_SITE = {"usage": ["Village", "Industrial"], "categories": ["tools"], "tags": ["floor"]}
_LOOT_RS_HUT = {"usage": ["Village"], "categories": ["tools", "containers", "food"], "tags": ["floor"]}


def _rsd(key, dir_, cls, display, params, loot, mass):
    e = {"key": key, "dir": dir_, "module": "ruralsite_shells", "class": cls, "name": "jp_" + key, "display": display,
         "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
         "placements": [], "verify": "shellcheck", "budget": _rs.budget_class(**params), "ship": True}
    ob = _rs.over_budget_ok(**params)
    if ob:
        e["over_budget_ok"] = ob
    return e


W3C2_SHELLS = [
    # TR23 the charcoal kiln under its roof (the burner's hut = C2's west hut, furnished)
    _rsd("rs_sumigama", "rs_kiln", "Land_JP_SumiGama", "Charcoal kiln (earth dome) under its board roof",
         {"kind": "sumigama"}, _LOOT_RS_SITE, 40000.0),
    # TR18 the climbing kiln (the work shed = W3B's earth-floor workshop, furnished as the potter)
    _rsd("rs_noborigama", "rs_kiln", "Land_JP_Noborigama", "Climbing kiln (noborigama, 4 chambers on its bank)",
         {"kind": "noborigama"}, _LOOT_RS_SITE, 200000.0),
    _rsd("rs_cmp_potteryyard", "rs_site", "Land_JP_Compound_PotteryYard", "Potter's yard: bamboo fence + cart opening",
         {"kind": "compound", "plot": "potteryyard"}, _LOOT_RS_SITE, 10000.0),
    # TR19 the tile works: the daruma kiln (the moulding shed = W3B's tiled earth-floor workshop, the drying shed = C2's
    # open board shed, both furnished) + the board-fenced yard
    _rsd("rs_darumagama", "rs_kiln", "Land_JP_Kawara_Gama", "Tile kiln (daruma type) under its board roof",
         {"kind": "darumagama"}, _LOOT_RS_SITE, 60000.0),
    _rsd("rs_cmp_tileyard", "rs_site", "Land_JP_Compound_TileYard", "Tile works yard: board fence + two-leaf cart gate",
         {"kind": "compound", "plot": "tileyard"}, _LOOT_RS_SITE, 20000.0),
    # TR26 the lime kiln (the slaking / packing shed = C2's open thatch shed, furnished)
    _rsd("rs_ishibaigama", "rs_kiln", "Land_JP_Ishibai_Gama", "Lime kiln (dry-stone pit on its bank) + draw floor",
         {"kind": "ishibaigama"}, _LOOT_RS_SITE, 300000.0),
    # TR25 the quarry face (the quarrymen's shed = C2's open board shed with the sharpening forge, furnished)
    _rsd("rs_ishiba", "rs_site", "Land_JP_Ishiba", "Quarry face (two cut benches, wedge-hole rows) + splitting floor",
         {"kind": "ishiba"}, _LOOT_RS_SITE, 900000.0),
    # TR27 the mine adit (the sorting shed = C2's open board shed, the miners' bunk hall = new, both furnished)
    _rsd("rs_mabu", "rs_site", "Land_JP_Mabu", "Mine adit (timbered drift into a knoll, dead end) + mine shrine",
         {"kind": "mabu"}, _LOOT_RS_SITE, 900000.0),
    # the bunk hall (KEEP_DWELLINGS 4): miners (board roof) and loggers (stone-weighted boards)
    _rsd("rs_bunkhall_itabuki", "rs_hall", "Land_JP_BunkHall_Itabuki", "Bunk hall (miners / loggers; board roof)",
         {"kind": "bunkhall", "roof": "itabuki"}, _LOOT_RS_HUT, 25000.0),
    _rsd("rs_bunkhall_ishioki", "rs_hall", "Land_JP_BunkHall_Ishioki", "Bunk hall (stone-weighted board roof)",
         {"kind": "bunkhall", "roof": "ishioki"}, _LOOT_RS_HUT, 28000.0),
    # TR24 the timber slide (the camp = the stone-roofed bunk hall furnished for loggers + W3B's saw shed as it is)
    _rsd("rs_shura", "rs_site", "Land_JP_Shura", "Timber slide (shura): the lowest 4 bays on trestles + the landing",
         {"kind": "shura"}, _LOOT_RS_SITE, 30000.0),
    # TR22 the salt works (Gyotoku irihama, dry land): the salt bed + the boiling hut with its shell pan
    _rsd("rs_enden", "rs_site", "Land_JP_Enden", "Salt field section (irihama): raked bed, dry ditch, embankment, sluice",
         {"kind": "enden"}, _LOOT_RS_SITE, 300000.0),
    _rsd("rs_kamaya", "rs_hall", "Land_JP_Kamaya_Itabuki", "Salt-boiling hut (kamaya) with its shell pan",
         {"kind": "kamaya"}, _LOOT_RS_HUT, 22000.0),
]
BUILDINGS += W3C2_SHELLS

# W3C2 furnished variants (furnishkit + buildings/w3c2_sets.py): earlier huts / sheds / workshops dressed per site
W3C2_FURNISHED = [
    _furn("f_rs_sumiyaki", "hut_west_ishioki", "w3c2_sumiyaki", "Sumiyaki", "furnished: the charcoal burner's hut"),
    _furn("f_rs_toki", "tr_ws_doma_itabuki", "w3c2_toki", "Toki", "furnished: the potter's work shed"),
    _furn("f_rs_kawara", "tr_ws_doma_sangawara", "w3c2_kawara", "Kawara", "furnished: the tile maker's moulding shed"),
    _furn("f_rs_kawara_dry", "shed_open_board", "w3c2_kawara_dry", "KawaraDry", "furnished: the tile drying shed"),
    _furn("f_rs_ishibai", "shed_open_thatch", "w3c2_ishibai", "Ishibai", "furnished: the lime slaking + packing shed"),
    _furn("f_rs_ishiku", "shed_open_board", "w3c2_ishiku", "Ishiku", "furnished: the quarrymen's shed (forge)"),
    _furn("f_rs_senko", "shed_open_board", "w3c2_senko", "Senko", "furnished: the mine's sorting shed"),
    _furn("f_rs_bunk_miners", "rs_bunkhall_itabuki", "w3c2_bunk_miners", "Miners", "furnished: the miners' bunk hall"),
    _furn("f_rs_bunk_loggers", "rs_bunkhall_ishioki", "w3c2_bunk_loggers", "Loggers", "furnished: the loggers' bunk hall"),
    _furn("f_rs_kamaya", "rs_kamaya", "w3c2_kamaya", "Furnished", "furnished: the salt-boiling hut (fuel, baskets, bags)"),
]
for _f in W3C2_FURNISHED:                     # W3C2's own model folder
    _f["dir"] = _f["model_dir"] = "rs_furnished"
BUILDINGS += W3C2_FURNISHED


# ------------------------------------------------------------------------------------------------ W3D government
# Phase C wave 3d (agent W3D, 2026-10-02): the government buildings (the highway checkpoint kit, the post-station
# office, the intendant's jinya, the jail, the fire brigade station + the tall fire watchtower) from
# parts/kit/jpparts/templates/govsite.py (buildings/govsitekit.py builds them; research + recorded choices
# spikes/W3D/W3D_NOTES.md). The shells a site reuses are earlier shells furnished in buildings/w3d_sets.py. Placed in
# ONE district west of 3c-2 by spikes/W3D/layout_w3d.py (test/placements/W3D.csv + test/ce/W3D_mapgrouppos.xml).
from jpparts.templates import govsite as _gv  # noqa: E402

_LOOT_GV_OFFICE = {"usage": ["Town", "Village"], "categories": ["tools", "containers"], "tags": ["floor"]}
_LOOT_GV_YARD = {"usage": ["Village", "Town"], "categories": ["tools"], "tags": ["floor"]}


def _gvd(key, dir_, cls, display, params, loot, mass):
    e = {"key": key, "dir": dir_, "module": "govsite_shells", "class": cls, "name": "jp_" + key, "display": display,
         "params": dict(params), "model_dir": dir_, "mass": mass, "sound": "doorWoodSlide", "loot": loot,
         "placements": [], "verify": "shellcheck", "budget": _gv.budget_class(**params), "ship": True}
    ob = _gv.over_budget_ok(**params)
    if ob:
        e["over_budget_ok"] = ob
    return e


W3D_SHELLS = [
    # site 1 the highway checkpoint kit: the guardhouse with the inspection room, the palisade + kora-mon compound
    _gvd("gv_bansho_sekisho", "gv_hall", "Land_JP_Bansho_Sekisho", "Checkpoint guardhouse with the inspection room "
         "(obansho: stepped veranda + tatami over the gravel court, office, kitchen doma)",
         {"kind": "bansho", "size": "sekisho"}, _LOOT_GV_OFFICE, 30000.0),
    _gvd("gv_cmp_sekisho", "gv_site", "Land_JP_Compound_Sekisho", "Checkpoint: palisade, two kora-mon gates across "
         "the road, the gravel court", {"kind": "compound", "plot": "sekisho"}, _LOOT_GV_YARD, 60000.0),
    _gvd("gv_oshirasu_s", "gv_site", "Land_JP_Oshirasu_Sekisho", "Gravel court before the checkpoint's inspection "
         "room", {"kind": "compound", "plot": "oshirasu_s"}, _LOOT_GV_YARD, 20000.0),
    # site 2 the post-station office + its yard
    _gvd("gv_toiyaba", "gv_hall", "Land_JP_Toiyaba", "Post-station office (toiya-ba: raised office open to the yard)",
         {"kind": "toiyaba"}, _LOOT_GV_OFFICE, 30000.0),
    _gvd("gv_cmp_toiyayard", "gv_site", "Land_JP_Compound_ToiyaYard", "Post-station yard: board fence + two-leaf "
         "gate", {"kind": "compound", "plot": "toiyayard"}, _LOOT_GV_YARD, 15000.0),
    # site 3 the intendant's jinya: the court room, the compound (the black nagaya-mon is a D3 dwelling entry below)
    _gvd("gv_ginmisho", "gv_hall", "Land_JP_GinmiSho", "Court room (ginmi-sho) of the intendant's office: stepped "
         "veranda + tatami over the white-gravel court", {"kind": "bansho", "size": "ginmi"}, _LOOT_GV_OFFICE, 30000.0),
    _gvd("gv_cmp_jinya", "gv_site", "Land_JP_Compound_Jinya", "Intendant's office (jinya): black board fence, back "
         "gate, the white-gravel court", {"kind": "compound", "plot": "jinya"}, _LOOT_GV_YARD, 30000.0),
    _gvd("gv_oshirasu_j", "gv_site", "Land_JP_Oshirasu_Jinya", "White-gravel court (oshirasu) before the court room",
         {"kind": "compound", "plot": "oshirasu_j"}, _LOOT_GV_YARD, 40000.0),
    # site 4 the jail
    _gvd("gv_roya", "gv_hall", "Land_JP_Roya", "Jail cell block (roya: outer + inner timber lattice, two cells)",
         {"kind": "roya"}, _LOOT_GV_OFFICE, 30000.0),
    _gvd("gv_cmp_roya", "gv_site", "Land_JP_Compound_Roya", "Jail compound: black capped board fence, one gate",
         {"kind": "compound", "plot": "roya"}, _LOOT_GV_YARD, 25000.0),
    # site 5 the fire brigade station (the tall tower is a climbable site object: spikes/W3D/props_w3d_site.py)
    _gvd("gv_cmp_hikeshi", "gv_site", "Land_JP_Compound_Hikeshi", "Fire brigade station: board fence + wide gate",
         {"kind": "compound", "plot": "hikeshi"}, _LOOT_GV_YARD, 15000.0),
    # the jinya's black gatehouse (D3's nagaya-mon template, rank 'official')
    _dwl("gv_nagayamon_jinya", "dw_samurai", "Land_JP_NagayaMon_Jinya", "Gatehouse with rooms (nagaya-mon), the "
         "intendant's office: black boards, tiled", {"kind": "nagayamon", "rank": "official"}, _LOOT_DW_TOWN, 40000.0),
]
BUILDINGS += W3D_SHELLS

# W3D furnished variants (furnishkit + buildings/w3d_sets.py); the jail's guard office is the W2F jishin-ban as it is
# (Land_JP_Guardhut_M_Itabuki_Jishinban), the jinya gatehouse's servants' room D3's nagaya-mon dressing
W3D_FURNISHED = [
    _furn("f_gv_bansho", "gv_bansho_sekisho", "w3d_bansho", "Furnished", "furnished (desks, ledgers, the kitchen)"),
    _furn("f_gv_bunk_ashigaru", "rs_bunkhall_itabuki", "w3d_bunk_ashigaru", "Ashigaru",
          "furnished: the checkpoint's foot-soldiers' guardhouse"),
    _furn("f_gv_toiyaba", "gv_toiyaba", "w3d_toiyaba", "Furnished", "furnished (clerks' desks, relay ledgers, loads)"),
    _furn("f_gv_ginmisho", "gv_ginmisho", "w3d_ginmisho", "Furnished", "furnished (the official's desk, records)"),
    _furn("f_gv_jinya", "dw_samurai_s", "w3d_jinya", "Jinya", "furnished: the intendant's office (desks, ledgers, "
          "measures)"),
    _furn("f_gv_nagayamon_jinya", "gv_nagayamon_jinya", "w3d_nagayamon", "Furnished", "furnished (servants' room)"),
    _furn("f_gv_kura_nengu", "kura_plain", "w3d_kura_nengu", "Nengu", "furnished: the jinya's tax-rice store"),
    _furn("f_gv_roya", "gv_roya", "w3d_roya", "Furnished", "furnished (mats, the tub, bowls; empty, doors open)"),
    _furn("f_gv_hikeshi", "shed_open_board", "w3d_hikeshi", "Hikeshi", "furnished: the fire brigade's tool shed "
          "(matoi-nobori, hooks, buckets)"),
]
for _f in W3D_FURNISHED:                     # W3D's own model folder
    _f["dir"] = _f["model_dir"] = "gv_furnished"
BUILDINGS += W3D_FURNISHED


# ------------------------------------------------------------------------------------------------ FB1 binding names
# FB1 (2026-10-01): a terrain-placed p3d binds to its config + script class ONLY through the class named
# Land_<p3d file name> (case-insensitive). C1-S1 named the family p3ds after their registry keys (jp_townhouse_
# kamigata_2k_..., jp_f_farmhouse_kanto, jp_s1_th_...), so 97 of 128 classes never bound in game: no doors, no loot
# (Stephen's showcase walk; "house, config class missing" in both logs). The class names stay (CE groups, mission
# files, maps, checklists use them); every family member's p3d is now named after its class: name = class minus
# "Land_", lower case. "recipe_name" keeps the old name for the recipe's model(name=...) so the geometry is unchanged.
# buildings/bindcheck.py fails the build if a shipped class and its p3d stem ever differ again.
for _b in BUILDINGS:
    if "params" in _b:
        _b["recipe_name"] = _b["name"]
        _b["name"] = _b["class"][len("Land_"):].lower()
