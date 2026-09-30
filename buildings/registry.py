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
        "placements": [{"pos": (1024.0, 25.0, 1045.0), "yaw": 180.0,
                        "where": "test island: the building spot, front (model +z) facing south to the spawn"}],
        "verify": "verify",
        "budget": "large",
        "ship": True,
    },
    {
        # B0 step 0c: one unit from the townhouse template, built to show the template runs. The test bed for B2's
        # party wall / party roof end / roof corner. NOT shipped: no config class, no PBO, no island placement.
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


def get(key):
    for b in BUILDINGS:
        if b["key"] == key:
            return b
    raise KeyError("no building %r in buildings/registry.py (have: %s)" % (key, ", ".join(b["key"] for b in BUILDINGS)))
