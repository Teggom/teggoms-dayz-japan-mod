# Spike T (terrain): report

(The agent returned this as text because subagents can't write report files; the lead saved it on 2026-09-27.)

**Answer: offline, a DayZ terrain can be built fully by script (route A), with 0 GUI clicks per rebuild. Nothing is
proven in game yet.** Python writes:
- the 8WVR source world
- the 25 layer tiles (paa) and their rvmats
- the objects
- the config and the mission

`binarize.exe` then turns the 8WVR into OPRW v29 with exit 0, and `pbo.py` packs
`@Japan\addons\jp_worlds_testisland.pbo` (96 files, 6.1 MB). `verify_oprw.py` finds all 4,792 non-road objects in the
binarized world with bit-identical transforms, plus all 9 road pieces, 44 models and 25 rvmats.

**Proven offline on Bohemia's own sample and vanilla data:**
- the file layout, grid orientation and cell-to-tile rule
- the object-height rule
- the 6-surface mask encoding

**Only Stephen's boot can prove:**
- the world loads
- the ground textures render
- `init.c` compiles
- loot appears in the house
- the pond holds water
- a missing navmesh is non-fatal

**Risk:** the world bakes in B's and F's p3ds, so their PBOs must be present when the game loads it.

## Commands

Rerun, in this order:

```
python D:\DayZ-Server_AI-20260907-MultiMap\japan_dev\spikes\T_terrain\build_world.py
python D:\DayZ-Server_AI-20260907-MultiMap\japan_dev\spikes\T_terrain\build_mission.py
python D:\DayZ-Server_AI-20260907-MultiMap\japan_dev\spikes\T_terrain\tools\verify_oprw.py
```

- The world build takes about 15 s and re-reads `test/placements/*.csv`. The mission build takes under 1 s.
- `build_world.py` writes `spikes/T_terrain/world_info.json`, which `build_mission.py` needs for the control house
  and for snapping buildings.
- `build_world.py` exits 1 if the PBO is locked by a running Japan server or game.
- `build_mission.py` never touches `storage_*`.
- Both need `P:` mapped, with `P:\JP` pointing at `src\JP`.
- `build_world.py --previews` builds the terrain, previews and route B set only.
- `build_world.py --pack-only` is route B: it binarizes and packs whatever Terrain Builder exported into `src`.

## Scripted vs GUI steps per rebuild

| Step | Route A (built, works offline) | Route B (TB fallback, inputs ready, never run) |
|---|---|---|
| Heightmap, mask, satellite | script | script |
| Layer tiles + `p_*.rvmat` | script | **TB GUI**: Generate layers |
| Objects (incl. other agents' CSVs) | script | script writes `objects.txt`, **TB GUI** imports it |
| Source `.wrp` | script (`tools/wrp8.py`) | **TB GUI**: Export WRP |
| Binarize + pack | script | script (`--pack-only`) |
| Mission | script | script |
| Navmesh (only for moving AI) | **GUI** (DayZDiag + NavMeshGenerator) | same |
| Server / game start | Stephen | Stephen |
| **Time per rebuild** | **~15 s, 0 clicks**, plus a restart | ~10-20 min of clicking (first setup ~45 min), plus scripts |

## Built

**`@Japan\addons\jp_worlds_testisland.pbo`**, prefix `JP\worlds\testisland`, CfgPatches `JP_Worlds_TestIsland`,
world `JapanTestIsland`. It holds:
- `world\japantestisland.wrp`: OPRW v29, 1.56 MB
- 25 `s_*_lco.paa` (DXT1), 25 `m_*_lca.paa` (DXT5), 25 `p_*.rvmat`
- the normal map and the outside satellite
- `data\pond\jp_pond.p3d` (ODOL)
- `ce\` (vanilla core files for `ceFiles`)
- `texHeaders.bin`

**`src/JP/worlds/testisland/`** holds the generated `config.cpp`, plus the build products binarize must see on `P:`:
the 8WVR, layers, pond MLOD and ce. These are git-ignored by a local `.gitignore`, because a rebuild takes 15 s.

**`spikes/T_terrain/`** holds:
- `build_world.py`, `build_mission.py`
- `tools/`: wrp8, odol, terrain, layers, objects, pond, gsi_dem, route_b, verify_oprw, render_island, calibrate_sat,
  plus one-off experiments
- `previews/`: `render_oblique.png`, `render_yard.png`, `heightmap.png`, `satellite_bright.png`, `surface_mask.png`,
  `objects.png`, `yard_closeup.png`, `patch_grid.png`
- `CREDITS.md`, `world_info.json`

**`data/T_terrain/`** holds the GSI tile cache, binarize logs, PBO staging and `route_b/`.

**`test/items/T.txt`**: Canteen, Hatchet, ChernarusMap, OrienteeringCompass, Binoculars.

**The island:**
- **Heightmap:** 512² at 4 m, 1.50 km² of land. The island centre is at (1024, 1150), so the yard lies on the
  southern plain.
- **Hills:** GSI DEM5A from Hakone's SE outer rim (35.1939 N, 139.0739 E), scaled ×0.47, highest point 177 m, all
  north of the yard.
- **Sea and beach:** the sea floor goes down to −29 m; a ~1:13 beach runs all round.
- **Yard:** 200 × 200 m at exactly 25.0 m on all 2601 vertices, 70 m blend, dirt surface.
- **Road:** 9 `grav` pieces over 188 m, from (1100, 1100) heading north, climbing 25→40 m. The grade is capped at 13%
  by cutting into the slope, 8.7 m deep at most.
- **Canal:** 14 m wide with its floor at −2.5 m, from (1616, 900) to (1446, 903).
- **Pond:** radius 16 m at (800, 905), water level 25.10 m. The pond p3d copies vanilla `lake_50x50`: `class=pond`,
  `water_lake.rvmat`, and a `water_ext` roadway.
- **Surfaces (base game only):**
  - `cp_grass`
  - `cp_grass_tall`, which also covers the paddy block in the SW
  - `cp_broadleaf_sparse1`, a forest floor with ferns
  - `cp_rock` on steep slopes
  - `cp_gravel` for the shingle beach and the seabed
  - `cp_dirt`
- **Objects:** 4,801 in total.
  - 4,451 vanilla trees: beech, oak, hornbeam and ash in the valleys, pine on ridges, spruce on high north slopes,
    and a 360-tree pine belt along the coast
  - 293 bushes and 36 rocks
  - the control house `Land_House_1W01` at (1236, 918), on a pad
  - the pond
  - the 10 drop-in placements from B and F

**The mission:**
- **Kept vanilla:** cfgeconomycore, cfglimitsdefinition(user), cfgspawnabletypes, cfgrandompresets, cfgignorelist,
  cfgundergroundtriggers, mapclusterproto, mapgroupdirt, and `db/globals`.
- **Emptied:** eventspawns, eventgroups, environment, effectarea.
- **Player spawns:** every spawn is at (1024, 985).
- **Weather:** enabled and clear spring.
- **Object spawners:** `cfggameplay.json` lists `spawns/A|B|F.json`.
- **Merged drop-ins:** `types.xml` (vanilla + F), `mapgroupproto` (vanilla + B), `mapgrouppos` (house + B's two
  groups).
- **`areaflags.map`:** 512² cells of 4 m, laid out 32+8 bit like Chernarus. Town|Village and Tier1|Tier2 everywhere.
- **Economy:** zombies, animals and vehicles have init and respawn set to 0. Every event is inactive except `Loot`.

**`init.c`:**
- It is vanilla, without the September date reset.
- New characters spawn at (1024±1.5, 985) facing north.
- On the first connect it lays out the items (rows from (1000, 975), 1.5 m spacing) and stands the creatures at ground
  height: 23 items and 3 creatures today.
- Both use `ECE_NOPERSISTENCY_WORLD` and a 45-day lifetime, so restarts never duplicate them.
- It logs `[JPTest] items ok N, items missing M, creatures ok K, creatures missing L`.

## What worked and what didn't (offline)

| Piece | Result |
|---|---|
| 8WVR writer | Re-writes BI's `Test_Terrain/utes.wrp` byte-identical, except the dummy object's id |
| Orientation and cell→tile rule | All 16,384 utes cells match `(⌊x/480⌋, ⌊(W−z)/480⌋)`. Elevation row 0 is south; flipping it gives a 118 m error |
| Object height rule, y = ground + scale × ODOL boundingCenter.y | 30/30 utes models within 0.05 m. MLOD centre = bbox of **all** LODs (memory included), 0 if `autocenter=0`, proven by binarizing 4 test MLODs |
| binarize 8WVR→OPRW | exit 0, 0.7 s. `verify_oprw` PASS: 4792/4792 objects bit-identical, 44/44 models, 25/25 rvmats |
| 6-surface mask | Decoded from vanilla masks plus the engine surface scan: black / R / G / B@255 / B@128 / B@0. The DXT5 tile decodes back 100% |
| Satellite | Colours are the medians of vanilla Chernarus satellite pixels |
| Pond p3d | Binarizes to ODOL |
| config.cpp | CfgConvert `-bin` exit 0 |
| PBO | `pbo.py list` shows all 96 files |
| Mission | All XML/JSON parse. `init.c` passes the gotcha checks (there is no offline compiler) |
| Route B | Inputs written. Never opened in TB (GUI not allowed) |
| Navmesh / OPRW heightmap decode | Not done. The navmesh config is ready |

## In-game checklist for Stephen (~10 min)

1. **Start.** Run `start-japan-test-island.bat`.
   - Pass: you stand on a flat dirt square, the machiya to the north, the sea on the horizon.
2. **Look around the yard.**
   - Forested hills to the north.
   - Sharp ground textures near you.
   - Grass clutter off the yard.
   - No floating or sunken trees.
3. **Check the item grid** behind you (x 1000-1033, z 975).
   - Items are present.
   - Open the ChernarusMap: it should show this island.
4. **Walk the road** from the yard's NE corner northwards. The pieces should follow the ground.
5. **Control house**, 212 m ESE at (1236, 918).
   - The doors open.
   - **Loot is inside** (this proves CE and `areaflags.map`).
6. **Canal**, east coast at z≈900.
   - Sea water fills the cut; you can swim.
   - A canteen fills with salt water.
7. **Pond** (stretch goal) at (800, 905).
   - Water is visible.
   - Drinking and filling the canteen works (fresh water).
8. **South beach.** Grey shingle, a pine belt, sea all round.
9. **Chop one tree** with the hatchet.
10. **Sun.** At 10:00 on 5 April it should be in the south-east.

## What only the boot can prove, and which lines tell us

**Server RPT: `ServerProfileJapanTest\DayZServer_x64_*.RPT`**
- **Must not appear:**
  - any error naming `japantestisland`, `JP\worlds\testisland`, `jp_pond` or `p_0`
  - `Cannot open object`
  - `No entry 'CfgWorlds.JapanTestIsland'`
  - `ENGINE (F)`
- **Navmesh:** at most a warning that `navmesh\japantestisland.nm` is missing, and nothing fatal after it.
- **Prototypes:** `[CE][LoadPrototype] :: loaded ~437 prototypes`.
- **Buildings:** `[CE][LoadMap] "Group" :: loaded 3 groups, groups failed: 0`.
- **Ignored types:** `[CE][offlineDB] Type ... will be ignored` only for JP classes whose PBO did not load.

**Script log: `ServerProfileJapanTest\script_*.log`**
- Expect `[JPTest] items ok 23, items missing 0, creatures ok 3, creatures missing 0`.

**Client RPT: `%LOCALAPPDATA%\DayZ\DayZ_x64_*.RPT`**
- Must not contain `Cannot load texture jp\worlds\testisland\...`.

## Failed / unknown

- **Nothing is tested in game.**
- **Binarize config gaps.**
  - Binarize sees only `P:\bin` plus my config. It notes "ChernarusPlus declared but not found" and falls back to
    defaults for 39 lookups (sky, sea materials, Clutter). AddonBuilder calls binarize the same way.
  - Possible cost: the grass-cover map binarize precomputes into the OPRW (GrassApprox) may be built without clutter
    data. I repeated SoundMapValues in my config so the sound map is right.
  - Binarize notes `OutsideTerrain satellite need TGA|PNG`. BI's sample uses `.paa` there too, and the output size was
    identical when I tested `.png`.
  - Binarize output is not byte-deterministic between runs, but the contents are identical.
- **OPRW appId is 0.** Vanilla is 1.
- **Road draping:** I assume the engine drapes road pieces onto the ground, as vanilla utes places them upright on
  slopes. The road bed is graded anyway.
- **Dependency on other agents' PBOs.** The world bakes in B's and F's p3ds, so their PBOs must load with it. If one
  is removed, rerun `build_world.py` without its CSV.
- **Facing north:** the spawn direction is set with `SetOrientation`, which the engine may ignore.
- **Route B:** the menu labels come from BI's documentation and are unconfirmed.
- **OPRW heights:** not decoded. The orientation was proven on BI's sample instead.

## Decisions I made

1. **4 m grid.**
   - It matches the 5 m DEM.
   - It stays above binarize's "min grid 3.125" hint.
   - The yard edges fall exactly on vertices, so the pad is planar.
2. **Layer grid.** Land cells are 128² at 16 m. Tiles are 512 px at 1 m/px with a 16 px overlap: 5×5 tiles, as in
   vanilla.
3. **Relief source.** Hakone's SE rim has natural forest relief; Sengokuhara shows golf courses in the lidar.
   - Scaled ×0.47.
   - The island is moved north so the yard sits on a coastal plain.
4. **Surfaces.** Base-game `cp_*` surfaces only, so no DLC is required.
5. **World class.** It inherits `ChernarusPlus` for sky, weather, ambient life and sounds. Everything map-specific is
   overridden.
   - Latitude −35.19, since the engine counts positive as south.
   - `OutsideTerrain` synth is off, so the sea continues past the map edge.
6. **CE source.** Vanilla CE files come from `P:\DZ\worlds\chernarusplus\ce`. The server's `mpmissions` copy is
   identical apart from this server's mod additions.
7. **Test spawns.** Items and creatures spawn on the first connect and are not persisted.
8. **Economy.** Dynamic loot only; every event off except `Loot`.
9. **Navmesh.** The Navmesh class is present with vanilla GenParams and no file. `build_world.py` packs
   `src/.../navmesh/japantestisland.nm` automatically once it exists.
10. **Road.** Short, with a 13% cut instead of switchbacks.
11. **Control house.** `Land_House_1W01` sits on its own pad.
12. **Building snapping.** `mapgrouppos` drop-ins snap to the exact baked position if the object is within 10 m. B's
    machiya already matched exactly.
13. **Git.** Generated files in `src` are git-ignored.
14. **Items.** Added `test/items/T.txt`.
15. **Density.** About 4.7k trees and bushes.
16. **Weather.** `cfgweather.xml` is enabled; vanilla ships it disabled.

## Route B, click by click

The inputs are in `data\T_terrain\route_b\`:
- `terrain.asc` (xllcorner 200000)
- `satellite_lco.png` and `mask_lco.png`, each with a `.pgw` world file
- `layers.cfg`, `mapLegend.png`
- `japantestisland.tml` (44 templates)
- `objects.txt`: `"name";X+200000;Z;yaw;pitch;roll;scale;ASL height`

Steps:
1. Copy `layers.cfg` and `mapLegend.png` to `P:\JP\worlds\testisland\source\`.
2. In TB, create a new project at `P:\JP\worlds\testisland\source\japantestisland.tv4p`.
3. Add a mapframe and set its properties:
   - Easting 200000, Northing 0
   - Terrain grid 512² at 4 m
   - Satellite and mask 2048² at 1 m/px
   - Texture layer 16 m
   - `layers.cfg` from step 1; output `P:\JP\worlds\testisland\data\layers`
   - Tile 512 px, overlap 16 px
4. Import `terrain.asc`.
5. Import the satellite PNG and the mask PNG.
6. Run **Generate layers**.
7. Load the library `japantestisland.tml`.
8. Import `objects.txt` with absolute heights.
9. Export the WRP to `P:\JP\worlds\testisland\world\japantestisland.wrp`.
10. Run `build_world.py --pack-only`. It converts TB's PNG tiles to paa and repoints the rvmats.

Time: about 45 min the first time, then about 10-20 min per rebuild.

## Navmesh, for later

1. Create an empty mission `empty.japantestisland`. Its `init.c` holds an empty `main()` and spawns the player at
   (1024, 0, 985).
2. Start a local DayZDiag server:
   ```
   DayZDiag_x64.exe -server -mod=@Japan -startNavmeshDataServer -port=<free port, not 2302> -config=<its cfg>
   ```
3. In NavMeshGenerator: Generation → Connect Data Server.
4. Generation → Start generation. For 2 km this should take minutes.
5. File → Save NavMesh to `P:\JP\worlds\testisland\navmesh\japantestisland.nm`.
6. Run `build_world.py` to pack it.

The navmesh must be regenerated after every world rebuild.

## Next step

- **Now:** Stephen boots the island and runs the checklist.
- **Then:**
  - fixes from the boot: 0.5-1 agent session
  - scaling route A to the 12.8 km grey-box map (chunked imagery, ~730 tiles, road network, erosion): 3-5 sessions
- **Optional:** decode the OPRW heightmap so the elevations can be verified too: 0.5 session.
