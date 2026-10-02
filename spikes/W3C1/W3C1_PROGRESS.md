# W3C1 progress: wave 3c-1, the town trade sites (agent W3C1, 2026-10-02)

Time log `japan_dev/TIMELOG_W3C1.md` (logger `python spikes/W3C1/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Setup / research notes: `spikes/W3C1/W3C1_NOTES.md` (sources, sizes, era tests, recorded choices, changes while
building). Stop rule: weekly usage 88 % -> checkpoint; never reached (77 % at start, 80 % at the end).

## Status: DONE (built, packed, on the island, world + mission rebuilt; untested in game)
- [x] notes  - [x] parts (3 new)  - [x] shells (12)  - [x] props (22 / 40 models)  - [x] furnished (8)
- [x] district + placement  - [x] world + mission  - [x] checks  - [x] sheets  - [x] checklist 3c-1  - [x] pushed

## New parts (`parts/kit/jpparts/mech.py`, manifest 336)
`jp_p_mech_waterwheel _overshot` (3.64 m, 24 buckets, axle, outer bearing; stopped), `jp_p_water_flume _run | _head`
(trough on a trestle; the head with the sluice board shut; dry), `jp_p_roof_union _gutter` (the parallel-roof join of
the kasane-gura: gutter on brackets, flashing, bamboo downpipe) + `roofs.roof(ov=(front, back))` (per-eave
overhangs, kirizuma only; koyagumi follows each slope's own ov). L / T valley unions NOT built. No engine ladder (a
static leaning ladder prop; the kura loft uses the stair).

## Shells (template `parts/kit/jpparts/templates/tradesite.py`, recipe `buildings/tradesitekit.py`, registry `W3C1_SHELLS`)
| Family | Classes |
|---|---|
| ts_brewery | Land_JP_SakaGura_Okura (9 x 4 ken, eave 5.40, log truss, loft 3.25 ken by stair, kura doors on both gables), Land_JP_SakaGura_Maegura (9 x 3 ken, eave 3.70, short back eave + gutter, araiba + kamaba with steam vent, koji ante-room + muro (two doors, ceiled, straw-lined), kaishoba), Land_JP_SakaGura_Seimai (4 x 2 ken open shed) |
| ts_mill | Land_JP_Suisha_Itabuki, _Thatch (3 x 2 ken hut + overshot wheel + 2-module flume + 3 cam-driven pestles over mortars) |
| ts_dyer | Land_JP_Konya_Sangawara, _Itabuki (4 x 3 ken: shop doma + vat room at 0.30 with four sunk vats round the fire pit, shell geometry) |
| ts_paper | Land_JP_KamiSuki_Itabuki, _Thatch (4 x 2.5 ken + lean-to for the bark steamer) |
| ts_site | Land_JP_Compound_Brewery (12 x 13 ken black board fence), _DyersYard (8 x 6), _PaperYard (9 x 6, yotsume) |
Budgets: o-kura 11.9k / mae-gura 12.0k R1 (large, within); Konya_Sangawara +22.7 % R1 (over_budget_ok: the vat bank);
both Suisha +47 % R3 (over_budget_ok: the wheel's buckets stay in every LOD for C15). Every object < 15k faces.

## Props (`spikes/W3C1/props_w3c1.py`, cat brewfit; `python spikes/W3C1/build_w3c1.py [prop ...] [--no-binarize]`)
22 props / 40 models, all pass; jp_furniture 625 classes (fragment W3C1, order 60). shikomi_oke (+ladder, +staved),
hangiri (+scattered), kai_poles, kamaba (+toppled), fune_press (+down), koji_toko (+ab), kojibuta_tana (+ab), karausu
(+broken), sakabayashi (big brewery sugidama, hung) + sakabayashi_fallen, hatcho_oke (+ab), hashigo, sukumo_bales
(+scattered), akumizu (+ab), monohoshi (+torn), shibori_front (+torn), dye_rack, sukibune (+ab), kozo_beat
(+scattered), shime_press (+ab), hoshiita_rack (+fallen), kozo_kama (+ab). Rebuilding a few: `--no-binarize` then
`python spikes/W3C1/binsingle.py <p3d ...>` (a folder binarize crashes on existing ODOLs). S1's small shop sugidama
(jp_f_sugidama) is separate and unchanged.

## Furnished (`buildings/w3c1_sets.py` on D3's placer; registry `W3C1_FURNISHED`, folder buildings/ts_furnished)
f_ts_okura, f_ts_maegura, f_ts_seimai, f_ts_kura_casks (C3's plain kura: Land_JP_Kura_Plain_SakeCasks), f_ts_sakaya
(W3B's tiled doma workshop: Land_JP_Workshop_Doma_Sangawara_Sakaya, the sugidama), f_ts_suisha (itabuki), f_ts_konya
(sangawara), f_ts_kamisuki (thatch).

## Island (`python spikes/W3C1/layout_w3c1.py` -> test/placements/W3C1.csv + test/ce/W3C1_mapgrouppos.xml; then
`python spikes/W3C1/map_w3c1.py` -> w3c1_map.jpg + SHOWCASE_MAP.md W3C1 section)
One district x 884-946, z 852-892 (lane z 861.5-866), BR1-BR8, DY1-DY7, PM1-PM5, WM1, LN1: 23 rows, 11 CE groups,
layout checks 0 problems. Seat rule for uneven ground (no terrain through any floor). World + mission rebuilt:
verify_oprw PASS 4239/4239. placecheck: 6 W3C1 rows flagged, all minor: 5 props sunk 4-8 cm on the slope, and
jp_f_hangiri called 'hanging' (a false flag: the classifier reads 'hang' in the name).

## Checks at the end
verify_all --full: 297 buildings, 19,640 checks, 0 failures (W3C1: 20 buildings / 1,118); a cached re-run after the
last fixes: all pass; bindcheck 297/297; hangcheck 0 (the sugidama + the two shop-cloth poles hang from real faces);
handlecheck 40 / 0; jointcheck_w3c1 (the three yards): every joint sealed in Geometry at 0.35 / 1.0 m, the paper
yard's bamboo grid see-through by design; gradesweep: compounds 0.00 m2 up-facing at grade (brewery / dyer yards);
the shells' remaining at-grade area is down-facing wall bases, the same baseline as W3B's shells.

## Sheets
research/production/contact_sheets/w3c1_family.jpg (every shell + the kasane-gura pair: as placed, back, roofs off),
w3c1_rooms.jpg (13 furnished rooms + 12 machinery prop rows), w3c1_map.jpg (district panel + island locator).
Tools: `spikes/W3C1/render_w3c1.py family|pair|try`, `render_w3c1_rooms.py rooms` (jobs `w3c1_jobs.py`),
`render_w3c1_props.py [prop ...]`, `try_ts.py <kind> '<json>'`, `overview.py x0 x1 z0 z1`.

## Not done / open
- ☆ Country sake brewer (not nearly free: a new small shell + placement; the complex's props are ready for it).
- The internal door between the two kura; the brewer's house (omoya); L / T roof valleys; an engine-climbable ladder.
- Shibori pattern texture (the shop cloths are plain indigo / undyed: a material job).
- The water mill on dry land (Stephen); into a stream on the map later (placement only: the flume is a kit part).
- Navmesh not regenerated (GUI step).

## How to resume
- Shells: `cd buildings && python pipeline.py <ts_key...> --no-pack --jobs 4`; pack `python -c "import pipeline; pipeline.pack()"`.
- Furniture pack: `python tools/assemble_config.py jp_furniture --pack`.
- World: `python spikes/T_terrain/build_world.py`, `python spikes/T_terrain/build_mission.py`,
  `python spikes/T_terrain/tools/verify_oprw.py`.
- Checks: `python buildings/verify_all.py --full`, `python buildings/bindcheck.py`,
  `python spikes/FX1/hangcheck.py buildings/ts_furnished/out/*.p3d`, `python spikes/FX1/handlecheck.py`,
  `python spikes/W3C1/jointcheck_w3c1.py --all`, `python spikes/FX5/gradesweep.py src/JP/buildings/ts_site`.
