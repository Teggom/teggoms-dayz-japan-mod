# B4 progress: the pilot (machiya_t3_01 furnished + street + yard), agent B4, 2026-09-30

Brief: PRODUCTION_PLAN Phase B item B4 -> gate G4. Time log: `japan_dev/TIMELOG_B4.md` (logger `spikes/B4/tlog.py`).

## Status: DONE (everything built, binarized, packed, on the island at the next boot; untested in game)

### What was built
- **Mise floor** (`jp_p_fit_mise_floor _455`): the new kit recipe `floors.mise()` builds a 0.455 board display strip
  along the street edge, two rows of standard mats (0.87 cells, the same as the zashiki's), and a 0.415
  tatami-yose board at the back. The room is 2.61 deep, so the leftover after the strip and whole mat rows is closed
  with a board, as carpenters did in off-module rooms.
- **Floor materials:** the machiya now uses B1's materials (`floors` got `mats=`; the defaults are unchanged):
  - tataki doma: `jp_m_ground_doma_tataki`
  - tatami + heri: `jp_m_floor_tatami` (one mat per texture tile) and `jp_m_floor_tatami_heri`
  - storage / strip boards: `jp_m_floor_boards_int`

  Needed for the G4 doma-colour verdict.
- **Furnished variant** `buildings/machiya_t3_01_shop` (`Land_JP_Machiya_T3_01_Shop`, `jp_machiya_t3_01_shop.p3d`).
  It is the shell recipe plus a proxy set (PLAYBOOK §10.4). It takes the machiya's island spot; the bare shell stays
  shipped with no placement.

  | Room | Props | Loot (floor / raised) |
  |---|---|---|
  | toriniwa | 5 | 2 / 1 |
  | mise | 7 | 2 / 9 |
  | zashiki | 6 | 3 / 6 |
  | kitchen | 7 | 2 / 5 |
  | storage | 7 | 3 / 10 |

  That's 32 room props plus 5 shop-front proxies. Loot: 43 points = 12 lootFloor + 31 lootshelves (tag shelves),
  none above 1.40 m.
- **Proxies in the Q5 LODs:**
  - collision props: Resolution 1 + Geometry + View + Fire
  - flat and hanging props (litter, mat, kamidana, shop-front cloth and lanterns): Resolution 1 only

  Kit: `parts/kit/jpparts/proxies.py`. Convention proven by binarizing a test model (`spikes/B4/proxy_test.py`): the
  long leg (2 m) is up and the short leg (1 m) is forward. The binarized shop ODOL carries 37 / 29 / 29 / 29 proxy
  records in R1 / Geo / View / Fire, none elsewhere.
- **Decorator:** `parts/kit/jpparts/decor.py`.
  - prop catalogue from the B3a / B3b sidecars
  - footprints and components from the MLOD masters
  - loot generation
  - checks D1-D14: count, coverage, raised surface, 1.00 m band, door zone 0.4, door sweep / D1 / C10 with the
    furniture in, props vs walls / each other, C6 bases, loot validity, proxy LODs + poses, yard bounds, well standing
    spots
- **New props** (through B3a's pipeline, `spikes/B3a/props_fittings.py`): `jp_f_kamidana_plain` and
  `jp_f_nagashi_wood`. The build list calls them merged fittings, but the machiya has 32 Resolution-1 faces of
  budget left, and proxies don't count. B3a's other 110 models are untouched (`spikes/B4/build_fittings.py`
  binarizes only `fittings/`).
- **Street + yard:** 17 map objects in the shop's model frame (registry `site()` -> C.csv rows per placement):
  - gutter covers + slab, tipped bench, fire tub, tattered nobori, cart, carrying pole, Jizo box
  - firewood, tubs x3, the pulley well (`Land_JP_S_Well_Tsurube_Curb_Stone`), laundry pole, the rope on the well
- **Toilet:** B2's walk-in toilet shipped as `buildings/toilet_t1_01` (`Land_JP_Toilet_T1_01`, half door, sound
  doorWoodNolatch). It stands at the back of the yard (1021.7, 1056.2), yaw 180. Generic checks 19/19.

### Pipeline changes (buildings/pipeline.py)
- **Recipes may expose:**
  - `proxies()`: added to the LODs after M.lods(); face counts / budgets exclude them
  - `loot_points(floors)`: floor + raised points
  - `site()`: yard objects -> C.csv
- **CE:** a `lootshelves` container (tag shelves) next to `lootFloor`.
- **requiredAddons:** gets JP_Furniture / JP_Site when proxies use them.
- **verify:** modules now load by path (two buildings both have a verify.py; import_module cached the first).
- **machiya verify.py:**
  - takes `name / cls / here / extra`
  - strips proxy triangles before the geometry checks
  - the Roadway loot check covers the floor points only
  - a shadowed `cls` variable was renamed

### Results
- Shell: 78/78.
- Shop: 137/137 (the same 78 on the furnished p3d + 59 decorator checks).
- Toilet: 19/19.
- Townhouse combos: 60/60, combos.json unchanged.
- Binarize: 3 ODOL (standard noise only).
- PBOs: jp_buildings (4 files) and jp_furniture (113) repacked.
- T's `build_world.py` + `build_mission.py` + `verify_oprw.py` rerun (PASS): the wrp has the shop, 17 site objects
  and the toilet; the mission has the CE groups and a WaterBottle on the item grid (`test/items/B4.txt`).
- Placecheck notes, all by design:
  - gutter pieces and the Jizo box "sunk": they sit in a ditch / on buried stones
  - the rope "floats": it hangs on the well beam
  - the cart floats 4 cm (wheels)
- Sheets: `buildings/machiya_t3_01_shop/machiya_t3_01_shop_rooms.jpg`, `..._site.jpg` (13 renders in `renders/`).

### Decisions I made
- A separate furnished p3d (PLAYBOOK §10.4), not proxies inside the shell: the shell stays reusable for other trades.
- Mise strip _455 + standard mats + a yose board, rather than stretched 1.08 m mats or the _910 strip.
- Kamidana and nagashi as proxied props (face budget); the kamidana is Resolution 1 only, undisturbed, no loot.
- Kitchen tubs and jars went outside (yard tubs) and into storage (big jar) to keep the kitchen at 7 props.
- There are no sandals in the kit, so the toriniwa has buckets and litter instead.
- The yard objects with collision are separate map objects (vanilla-like); the shop-front cloth and lanterns are
  proxies (G1 A3-8).
- T's world / mission builds were rerun so the placements are on the island at the next boot.
- The navmesh was NOT regenerated: infected pathing in the furnished house is untested (NAVMESH_STEPS.md, GUI).

## Next / open
- **G4 walk:** see `TEST_CHECKLIST.md`.
- The machiya's old `machiya_t3_01_sheet.jpg` still shows the pre-B4 floor.
- Navmesh regeneration after G4.

## Commits
- be762bc: everything above. The time-log END + this line follow in the next commit.

## How to resume / rerun
- `python buildings/pipeline.py`: all shipped buildings, then binarize, pack and verify (~10 min).
- `python spikes/B3a/build.py kamidana nagashi --no-binarize` then `python spikes/B4/build_fittings.py --pack`.
- `python buildings/machiya_t3_01_shop/render_shop.py`: renders + sheets.
- Island: `python spikes/T_terrain/build_world.py`, then `build_mission.py`, then `tools/verify_oprw.py`.
