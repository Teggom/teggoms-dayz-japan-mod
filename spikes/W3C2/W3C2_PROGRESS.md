# W3C2 progress: wave 3c-2, the rural / industrial trade sites (agent W3C2, 2026-10-02)

Time log `japan_dev/TIMELOG_W3C2.md` (logger `python spikes/W3C2/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Setup / research notes: `spikes/W3C2/W3C2_NOTES.md` (sources, sizes, era tests, recorded choices, changes while
building). Stop rule: weekly usage 88 % -> checkpoint; not reached (82 % at start).

## Status: DONE (built, packed, on the island, world + mission rebuilt; untested in game)
- [x] notes  - [x] site 1 charcoal  - [x] 2 pottery  - [x] 3 tile works  - [x] 4 lime  - [x] 5 quarry (+ stonemason)
- [x] 6 mine  - [x] 7 logging  - [x] 8 salt  - [x] district + placement  - [x] world + mission  - [x] checks
- [x] sheets  - [x] checklist 3c-2  - [x] pushed

## New site parts (`parts/kit/jpparts/ruralsite_parts.py`, manifest 342)
The kiln kit (`mound`, `dome_prof`, `vault`, `mouth`, `bank`, `scatter_stones`, shared by every kiln):
`jp_p_site_kiln_dome _charcoal`, `jp_p_site_kiln_climbing _4ch`, `jp_p_site_kiln_updraught _daruma`,
`jp_p_site_kiln_shaft _stone`, `jp_p_site_adit _timbered`, `jp_p_site_shura _log4` (PGA 39 / 38 / 41 / 40 / 37 / 26).

## Shells (template `parts/kit/jpparts/templates/ruralsite.py`, recipe `buildings/ruralsitekit.py`, registry `W3C2_SHELLS`)
| Family | Classes |
|---|---|
| rs_kiln | Land_JP_SumiGama (earth-dome kiln under a 3 x 3 ken board roof), Land_JP_Noborigama (firebox + 4 chambers on its bank, stokers' shelter), Land_JP_Kawara_Gama (daruma kiln under a 3.5 x 2.5 ken roof), Land_JP_Ishibai_Gama (dry-stone kiln pit on its bank, draw-floor roof) |
| rs_site | Land_JP_Ishiba (quarry face + splitting floor + masons' shelter), Land_JP_Mabu (adit knoll, 4-ken timbered drift to a rockfall, hokora), Land_JP_Shura (slide's last 4 bays on trestles + landing), Land_JP_Enden (irihama salt-bed section, dry), Land_JP_Compound_PotteryYard (yotsume, pick_gate: 1.5-ken opening), Land_JP_Compound_TileYard (itabei, pick_gate: kido_ryo 1.5 ken) |
| rs_hall | Land_JP_BunkHall_Itabuki, Land_JP_BunkHall_Ishioki (6 x 3 ken), Land_JP_Kamaya_Itabuki (4 x 3 ken, shell pan on its firebox, smoke vent) |
Budgets: every object under its class cap except BunkHall_Itabuki +2 % and BunkHall_Ishioki +38 % R1 (over_budget_ok:
the longest standard hut; the stone roof's stones). Largest object ~8.3k R1 faces.

## Props (`spikes/W3C2/props_w3c2.py`, cat sitefit; `python spikes/W3C2/build_w3c2.py [prop ...] [--no-binarize]`)
18 props / 24 models, all pass + propfloat 0: keri_rokuro (+ab), neri_ban, ware_rack (+fallen), wares_straw,
kiln_shelves, kawara_rack (+collapsed), kawara_stack (+scattered), kawara_bench, limestone_heap, spoil_heap,
ishi_blocks, ishi_shura (+ab), senko_dai, nekonagashi, makiage, zaru_tori (+ab), shio_zaru, matsuba.
jp_furniture 649 classes (fragment W3C2, order 70). Rebuilding a few: `--no-binarize` then
`python spikes/W3C2/binsingle.py <p3d ...>`.

## Furnished (`buildings/w3c2_sets.py`; registry `W3C2_FURNISHED`, folder buildings/rs_furnished)
f_rs_sumiyaki (C2 hut_west_ishioki: Land_JP_Hut_West_Ishioki_Sumiyaki), f_rs_toki (W3B tr_ws_doma_itabuki: _Toki),
f_rs_kawara (W3B tr_ws_doma_sangawara: _Kawara), f_rs_kawara_dry (C2 shed_open_board: _KawaraDry), f_rs_ishibai
(C2 shed_open_thatch: _Ishibai), f_rs_ishiku (shed_open_board: _Ishiku), f_rs_senko (shed_open_board: _Senko),
f_rs_bunk_miners (Land_JP_BunkHall_Itabuki_Miners), f_rs_bunk_loggers (Land_JP_BunkHall_Ishioki_Loggers), f_rs_kamaya
(Land_JP_Kamaya_Itabuki_Furnished). W3B's Land_JP_Timber_SawShed_Furnished is placed as it is (the logging camp's saw).

## Island (`python spikes/W3C2/layout_w3c2.py` -> test/placements/W3C2.csv + test/ce/W3C2_mapgrouppos.xml; then
`python spikes/W3C2/map_w3c2.py` -> w3c2_map.jpg + SHOWCASE_MAP.md W3C2 section)
One district x 826-952, z 818-900 wrapped round 3c-1 (west + south), a loop of lanes from 3c-1's lane and back, a spur
to the logging camp. 21 buildings + 20 free props, 46 rows, 21 CE groups, layout 0 problems.

## Checks at the end
(see the PRODUCTION_PLAN log entry: verify_all --full, bindcheck, verify_oprw, placecheck, hangcheck, handlecheck,
gatecheck, roomaccess, propseat, propfloat, gradesweep, jointcheck)

## Sheets
research/production/contact_sheets/w3c2_family.jpg, w3c2_rooms.jpg, w3c2_map.jpg. Tools: `spikes/W3C2/render_w3c2.py
family|try`, `render_w3c2_rooms.py rooms` (jobs `w3c2_jobs.py`), `render_w3c2_props.py [prop ...]`.

## How to resume / re-run
- Parts: `cd parts/kit && python build_parts.py --only jp_p_site_`.
- Shells: `cd buildings && python pipeline.py <rs_key...> --no-pack --jobs 2`; pack `python -c "import pipeline; pipeline.pack()"`.
- Furniture pack: `python tools/assemble_config.py jp_furniture --pack`.
- World: `python spikes/T_terrain/build_world.py`, `python spikes/T_terrain/build_mission.py`,
  `python spikes/T_terrain/tools/verify_oprw.py`.
