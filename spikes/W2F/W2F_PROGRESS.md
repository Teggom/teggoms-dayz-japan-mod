# W2F progress: Phase C wave 2, furnish + place + the walk (agent W2F, 2026-10-01)

Time log `japan_dev/TIMELOG_W2F.md` (logger `python spikes/W2F/tlog.py "<event>" W2F "<tag>" <5h> <wk>`). Research
notes for the props: `spikes/W2F/W2F_NOTES.md`.

## Status: DONE (built, packed, on the island, world + mission rebuilt; untested in game)
- [x] props  - [x] dressings  - [x] registry + build + checks  - [x] placement + world + mission
- [x] maps + SHOWCASE_MAP  - [x] sheets  - [x] checklist  - [x] verify_all --full  - [x] pushed

## Props (49 models, 49/49 pass incl. TXT; jp_furniture.pbo 522 classes)
- `spikes/W2F/props_w2f_sacred.py` (cat `sacred`): saisen_bako l/m/s, suzu_rope (+faded), odaiko, kagura_drums,
  gaku hachimangu / nenbutsu / worn_h (B1 atlas text), hassokuan s/l (sanbo, heishi, dried sakaki), shintai_zushi (+s),
  ema_rail, kagura_masks, dais amida / shaka / kannon / jizo (shumidan + zushi + image + the three altar pieces),
  tengai, sutra_desk, mokugyo_l, waniguchi, bonsho s/l (+ striker log), gyoban, umpan, ofuda_stack, terrace l/m
  (stone hall terraces with a front flight, Roadway gravel + stone ramp).
- `spikes/W2F/props_w2f_civic.py` (cat `civicfit`): forge (+l), fuigo (+l, +ab), anvil (+l), mizubune, tongs_wall
  (+taken), tsuchioki, blade_rack (+empty), shimenawa_hang, mitsudogu (+taken), ridge_ladder, hishaku_rack.
- Build: `python spikes/W2F/build_w2f.py [prop ...] [--no-binarize] [--pack]` (B3a + L1 + S1 + W2F into one config).
  **PITFALL:** a later B3a / L1 / S1 build rewrites jp_furniture's config.cpp WITHOUT the W2F classes: run
  `python spikes/W2F/build_w2f.py --pack` after it.
- Renders: `python spikes/W2F/render_w2f_props.py [prop ...]` then `--sheets` -> contact_sheets/w2f_props_*.jpg.

## Furnished variants (24; registry W2F_FURNISHED, dressings buildings/w2f_sets.py; 1,558 checks, 0 failures)
| Key | Class | Rooms: counted props (sparse = not a living room) |
|---|---|---|
| f_shrine_haiden_town | Land_JP_Shrine_Haiden_Town_Hiwada_Furnished | haiden 6 (drum, offering table, 2 candle stands, ritual chest*, cushions) + god shelf, rope, 2 ema rails; en sparse (bell rope); name board; offering box at the stair foot |
| f_shrine_haiden_village | ..._Haiden_Village_Furnished | haiden 5 (+ ema); en sparse; box at the stair foot |
| f_shrine_honden_nagare_town / _village_chigi | ..._Furnished | en sparse (offering table); sealed sanctum: 3 / 1 shrine cabinets as front proxies |
| f_shrine_temizuya_town | ..._Temizuya_Town_Furnished | pavilion sparse (basin, ladle rack) |
| f_shrine_shamusho_sangawara | ..._Shamusho_Sangawara_Furnished | office 6 (counter* + ofuda, desk* + writing box, robes, chest*, cushion, seal box) + god shelf; doma 5 |
| f_shrine_kagura_town | ..._Kagura_Town_Furnished | stage sparse 3 (drums, costume chest*, cushions) + masks |
| f_temple_hondo_village | Land_JP_Temple_Hondo_Village_Jodo | hall 6 (Amida dais, sutra desk, 2 candle stands, chest*, cushions) + canopy; en sparse (box, gong) |
| f_temple_hondo_town | ..._Hondo_Town_Zen | hall 7 (Shaka dais, sutra desk, big mokugyo, drum, 2 candle stands, chest*) + canopy; box at the stair foot |
| f_temple_do_2_board / do_3_tile | ..._Do_2_Board_Jizo / ..._Do_3_Tile_Kannon | hall 6 (dais, candle stand, box*, brazier*, cushions, lamp); en sparse |
| f_temple_kuri_village / _town | ..._Kuri_Village_Furnished / ..._Kuri_Town_Zen | doma 7 (2 kamado + 3 pots, jar, shelves*, firewood*, pickle tub; Zen: fish board + cloud gong); daidokoro 5 (irori hook, tray shelves*, account desk*, pot, cushion, lamp); guest 6; genkan sparse |
| f_temple_shoro_village / _town | ..._Shoro_Village_Bell / ..._Shoro_Town_Bell | platform / upper deck sparse: the bell on bell_hook |
| f_temple_gate_yakuimon / _shikyakumon | ..._Furnished | gate passage sparse; blank weathered name board |
| f_teahouse_bench_itabuki / shop_thatch / tateba_itabuki | ..._Furnished | kettle hearth + benches* + tea dressing; agari / zashiki rooms 5-6 |
| f_smithy_open_itabuki | ..._Furnished | doma 6 (forge*, bellows*, anvil*, dry tub*, charcoal*, rack*) + tool wall |
| f_swordsmith_sangawara | ..._Furnished | forge 5 + rope + god shelf; work 5 + blade rack |
| f_guardhut_m_itabuki | ..._Guardhut_M_Itabuki_Jishinban | doma 5 + capture tools; floor 5 (brazier* + kettle, counter* + candles) + fire gear; ridge ladder; lantern post |
| f_kido_lattice_bantaya | ..._Furnished | gate sparse (ward lantern); hut doma 5; hut floor sparse 3 |
(* = a raised loot surface.) Loot: floors + prop tops <= 1.40 m; nothing on altars / offerings.

## Shared-code changes (additive)
- `parts/kit/jpparts/decor.py`: room flag `sparse` (D1 0-7, D3 not required, D4 no centre target and doors that open
  from a neighbour's wall skipped). Rooms without it are checked exactly as before.
- `buildings/shellcheck.py`: D6 measures a hinged (rotation) door with `door_world_rot`, as C7 already did.
- `buildings/furnish_sets.py`: imports `w2f_sets` (like shop_sets). `buildings/registry.py`: block W2F_FURNISHED.

## Island (own drop-ins: test/placements/W2F.csv, test/ce/W2F_mapgrouppos.xml; `python spikes/W2F/layout_w2f.py`)
- P precinct: P1 haiden (1024, 1192) on terrace P1t (1.35 m), P2 honden (1024, 1207) on P2t (1.8 m), P3 temizuya
  (1014, 1147), P4 shamusho (1011, 1165), P5 kagura (1011.5, 1188.5; uphill posts 0.56 m into the slope).
- V village shrine (945, 1061-1080): torii, 2 lanterns, haiden, honden. T village temple (947-987, 1101-1129): hondo,
  kuri, bell tower, gate, Jizo hall, lanterns, a stone Jizo. U town temple (1079-1121, 1095-1124): hondo, kuri, bell
  tower, gate, Kannon hall, lanterns, basin. K civic: kido (1069, 1080) + tea houses (1074-1091) east; smithy (969.5,
  1086), swordsmith (967, 1072), jishin-ban (977.5, 1072.5) west.
- Layout checks: 0 overlaps / clashes (vs C.csv buildings, every other CSV point, reserved spots, trees); 3 notes.
- World + mission rebuilt: verify_oprw PASS 4123/4123; all 24 CE groups snap exactly. Placecheck: 17 W2F flags, all
  by design (terraces sunk at the back, halls "floating" on the terraces, lantern / stone name rules, the kagura slope).
- Oku-miya: NOT placed. The hill-stair top rises ~45 % (2.3 m across a 5 m hall); the SH1 stand-in hut stays.
- Maps + IDs: contact_sheets/w2f_map_precinct.jpg, w2f_map_village.jpg, w2f_map_east.jpg; SHOWCASE_MAP.md W2F
  section (`python spikes/W2F/map_md.py`).

## Checks at the end
- verify_all --full: 193 buildings, 11,820 checks, 0 failures; bindcheck 193/193; props 49/49.

## Sheets (research/production/contact_sheets/)
w2f_props_sacred(_2,_3).jpg, w2f_props_civic(_2).jpg, w2f_rooms.jpg, w2f_plans.jpg, w2f_precinct.jpg, w2f_temple.jpg,
w2f_civic.jpg, w2f_map_*.jpg. Renderers: render_w2f_props.py, render_w2f_rooms.py (+ w2f_jobs.py), render_w2f.py.

## Decisions I made
- Offering boxes go to the stair foot (ground / terrace) where the en before a single door is too shallow (town haiden,
  village haiden, town hondo, Kannon hall); kept on the en for the two-door halls.
- Halls on the slope stand on stone terraces (period ishidan); W2S's anvil / charcoal spots that blocked a door were
  moved; the smithy forge shifted 0.18 m off the bellows spot (the two W2C spots overlapped).
- Sects: village Jodo, town Zen (Nichiren / Shinshu need a text cell / a shell option that do not exist).
- Temple gate boards are blank weathered (no temple-name cell in the atlases; flagged).

## Open / not done
- Engine-untested: everything; the hinged doors (shrine, temple, kido) are the first rotation doors walked.
- Navmesh not regenerated (GUI step). The forge clay reads close to the wall plaster in renders (judge in game).
- 'tower' face-budget class: asked in TEST_CHECKLIST.md.
