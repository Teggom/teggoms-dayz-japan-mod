# japan_dev: Feudal Japan total conversion for DayZ

A new, standalone project. **It is unrelated to the Pokemon project** (`pokemon_dev/`). It shares no code, no
mod and no server with it. Pure vanilla DayZ plus our own `@Japan` mod: no CF, no Expansion, no other mods.

- Owner and GO/NOGO: Stephen.
- Plan and verdict: `FEASIBILITY.md`. §8 is the plan, §3 the draft map layout.

Stephen's calls (2026-09-26):
- Spike wave 1 (the five spikes below) is GO.
- Weapons use vanilla animation sets for now. Custom animations get added per weapon later, if needed.
- The §3 layout is fine for now. The real map is placed later. This phase is models and testing.
- Everything else in FEASIBILITY §9 is still open.

---

## Layout

| Path | What | Owner |
|---|---|---|
| `FEASIBILITY.md`, `README.md`, `TEST_CHECKLIST.md` | Plan, this contract, the bundled in-game checklist | lead |
| `tools/common/` | `mlod.py` (MLOD p3d writer) and `pbo.py` (PBO packer), copied from pokemon_dev 2026-09-26. **Read-only for agents**: to change one, copy it into your own tools folder | lead |
| `spikes/<X>/` | Your working area: scripts, .blend files, renders, `REPORT.md`, `CREDITS.md` | agent X |
| `src/JP/<area>/` | Game-ready source for your PBO. `P:\JP` is a junction to `src/JP` | agent X |
| `data/<X>/` | Big downloaded or generated data (DEM tiles, big images). Git-ignored | agent X |
| `test/` | Drop-in files that wire your work into the test island (below) | one file per agent |
| `mission/japantest.japantestisland/` | The test mission. `mpmissions\japantest.japantestisland` is a junction to it | T |
| `..\@Japan\addons\` | Built PBOs, one per area. **Not in git** | agent X, its own PBO only |
| `..\serverDZ_japantest.cfg`, `..\start-japan-test-island.bat`, `..\start-japan-test-client.bat` | Test server config, server + game launcher, rejoin launcher | lead |

## Areas and naming

| Spike | Source (`P:\JP\...`) | PBO in `@Japan\addons\` | CfgPatches | Classes |
|---|---|---|---|---|
| **T** terrain | `JP\worlds\testisland` | `jp_worlds_testisland.pbo` | `JP_Worlds_TestIsland` | world class `JapanTestIsland` |
| **B** building | `JP\structures` | `jp_structures.pbo` | `JP_Structures` | `Land_JP_*` (p3d `jp_*.p3d`) |
| **W** wearables | `JP\characters` | `jp_characters.pbo` | `JP_Characters` | `JP_*` |
| **A** arms | `JP\weapons` | `jp_weapons.pbo` | `JP_Weapons` | `JP_*` |
| **F** flora | `JP\plants` | `jp_plants.pbo` | `JP_Plants` | `JP_*` items, p3d `jp_*.p3d` |

- **Scripts**, if you need Enforce Script, live inside your own area (`JP\<area>\scripts\4_World\...`). Declare them
  with your own `CfgMods` class (`JP_<Area>`) in your own config.cpp. Never reopen another area's classes.
- **One `CfgPatches` class per PBO**, declared once (see the gotchas file below).

## The test island (shared by all spikes)

- **World:** `JapanTestIsland`, 2048 × 2048 m, an island with sea around it.
- **Coordinates:** DayZ world metres, x east, z north, y up (height above sea level).
- **The test yard:** a flat pad centred on **(1024, 1024)**, 200 × 200 m, ground at **exactly 25.0 m ASL**. T
  guarantees it.
- **Reserved spots in the yard:**

| Spot | Where | Who |
|---|---|---|
| Player spawn | (1024, 985), facing north | T |
| Item grid | rows starting at (1000, 975), 1.5 m spacing; T's generated `init.c` lays out every item from `test/items/*.txt` | T generates, all fill |
| The building | centred (1024, 1045), front facing south (towards the spawn), footprint ≤ 14 × 14 m | B |
| Sakura | (985, 1010) and (1063, 1010) | F |
| Bamboo grove | 5-8 clumps inside x 1080-1110, z 955-995 | F |
| Weapon range | targets and dummies inside x 995-1055, z 925-950 | A |

### Drop-in files (how your work reaches the island)

Each agent writes only its own files. T's build scripts merge everything they find.

| File | Format | Used for |
|---|---|---|
| `test/placements/<X>.csv` | `p3d,x,z,yaw_deg,y_offset`: `p3d` P:-relative (`JP\plants\...\jp_x.p3d`); y = ground + y_offset; yaw clockwise from north | Objects baked into the **terrain** (.wrp). Needed for anything the engine matches by p3d name: cuttable trees and bushes, map buildings |
| `test/spawns/<X>.json` | the vanilla object-spawner format `{"Objects":[{"name":"Class","pos":[x,y,z],"ypr":[yaw,0,0],"scale":1}]}` | Objects spawned at runtime by `cfggameplay.json` `objectSpawnersArr` |
| `test/items/<X>.txt` | one class per line, optional count (`JP_Katana 2`), `#` comments | Items laid out on the item grid at spawn |
| `test/types/<X>.xml` | bare `<type>` elements | Merged into the mission `types.xml` |
| `test/ce/<X>_mapgroupproto.xml`, `test/ce/<X>_mapgrouppos.xml` | bare `<group>` elements | Loot points and building instances |

Once all spikes are done, the lead reruns T's world and mission build so everything lands in one test world.
Stephen then does one bundled check from `TEST_CHECKLIST.md`.

---

## Rules for every agent (hard)

1. **Never start, stop or kill** `DayZServer_x64.exe`, the DayZ game (`DayZ_x64`, `DayZ_BE`, `DayZDiag_x64`),
   Workbench, Terrain Builder, Object Builder or any other GUI program. Stephen may be playing live. Command-line
   tools are fine: `binarize.exe`, `ImageToPAA.exe`, `CfgConvert.exe`, `blender.exe --background`, python. If a
   step truly needs a GUI, write exact click-by-click steps for Stephen in your REPORT and move on.
2. **Write only inside your own paths:**
   - `spikes/<X>/`
   - `src/JP/<area>/`
   - `data/<X>/`
   - your own `test/*/<X>*` files
   - your own PBO in `@Japan/addons/`
   - T also owns `mission/`

   Never modify `pokemon_dev/`, other server files, other agents' paths, or `tools/common/`. Read anything.
3. **No git commands.** The lead commits.
4. **Allowed downloads:**
   - GSI elevation tiles (cyberjapandata.gsi.go.jp), T only
   - ambientCG and Poly Haven CC0 assets, all agents
   - Bohemia's official DayZ-Samples repo, for reference

   Web pages can be read freely. **No executables or installers.** Python has numpy, Pillow and requests. If you
   truly need scipy: `python -m pip install --user scipy` is the only package install allowed. Blender's own
   Python has numpy. Log every downloaded asset with its licence in `spikes/<X>/CREDITS.md`.
5. **Python writes use binary mode with LF** (`open(p, 'wb')`). Text mode on Windows silently turns LF into CRLF.
6. **Bounded reads:** measure big files (`wc -c`) before reading. Mission XML, logs, `D:\DayZToolsExtract` dumps and
   config.cpp files can be huge; read line ranges or grep.
7. **Check `P:` first:** `Test-Path P:\DZ`. If it's missing, `subst P: D:\DayZToolsExtract`. `P:\JP` is a
   permanent junction to `japan_dev\src\JP`.
8. **Read the gotchas that already cost real restarts:**
   `C:\Users\Stephen\.claude\projects\D--DayZ-Server-AI-20260907-MultiMap\memory\reference-enforce-script-gotchas.md`
   (reserved words, no `bool.ToString()`, no ternary, no line-leading `+`, module order, one CfgPatches, action
   registration). Also `reference-dayz-jsonfileloader-missing-keys.md` in the same folder.
9. **A running server locks PBOs.** If your PBO write fails because the test server is up, report it. Don't kill
   anything.
10. **Stephen is not reachable during the run.** Make sensible calls and log each one in your REPORT under
    "Decisions I made".
11. **It is a proof, not a product.** Don't gold-plate, but looks matter: render previews in Blender and actually
    look at them (Read the PNG) before calling a model done.

## What every spike delivers

- **`spikes/<X>/REPORT.md`** with these sections:
  - **Built**: files and classes
  - **Verified offline**: how (binarize log, CfgConvert, renders)
  - **In-game checklist for Stephen**: short and concrete; where to stand, what to do, what "pass" looks like
  - **Failed / unknown**
  - **Decisions I made**
  - **Next step**: with effort in agent sessions
- **A short final message** (≤ 300 words) to the lead.

## Useful references on this machine

- Blender 5.2: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` (headless:
  `--background --python x.py`)
- DayZ Tools: `C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\` (Binarize, ImageToPAA, CfgConvert,
  TerrainBuilder, TerrainProcessor, NavMeshGenerator, CeEditor, AddonBuilder)
- Vanilla data, extracted: `D:\DayZToolsExtract\` = `P:\` (DZ, scripts, ...). Binarized p3ds (ODOL) there are
  references only; plain-text configs, rvmats, `.asi`/`.agr` graphs and scripts are readable.
- Vanilla scripts: `P:\scripts\4_world\...`. For example `entities\manbase\dayzplayer\dayzplayercfgbase.c` holds
  the in-hands animation table.
- Prior research, read-only, from the Pokemon project (not related, but the engine facts carry over):
  - `pokemon_dev/research/item_overhaul/WORLD_BUILDINGS.md` §0 (loot-point transform) and §4 (custom enterable
    building: LODs, doors, generated loot points, placement)
  - `pokemon_dev/research/item_overhaul/FEASIBILITY.md` §2c (clothing: `DayzTemporarySkeleton`, M/F models,
    slots) and §2d (melee weapons: in-hands profiles follow inheritance)
  - `pokemon_dev/RIGGING.md`, `pokemon_dev/tools/build_models.py`, `pokemon_dev/tools/build.py`: how that project
    writes MLOD from Blender, binarizes (cwd = `P:\`) and packs
