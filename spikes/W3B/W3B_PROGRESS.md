# W3B progress: wave 3b everyday workshops + services (agent W3B, 2026-10-02)

Time log `japan_dev/TIMELOG_W3B.md` (logger `python spikes/W3B/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Research notes: `spikes/W3B/W3B_NOTES.md`. Stop rule: weekly usage 88 % -> checkpoint, commit + push, resume note here.
(Time-log note: the usage figures on the 01:09-01:24 lines were carried forward without a fresh read (77-78 %); the
fresh reads before and after were 76 %.)

## Status: DONE (built, packed, on the island, world + mission rebuilt; untested in game)
- [x] notes  - [x] shells (18)  - [x] props (34 / 63 models)  - [x] furnished (14)  - [x] placement + world + mission
- [x] checks  - [x] sheets (w3b_family, w3b_rooms, w3b_map)  - [x] checklist section 3b  - [x] pushed

## Shells (template `parts/kit/jpparts/templates/trade.py`, recipe `buildings/tradekit.py`, registry `W3B_SHELLS`)
| Family | Classes |
|---|---|
| tr_sento | Land_JP_Sento_Sangawara, Land_JP_Sento_Itabuki (6 x 3 ken: doma + bandai, changing room + nagashi, the zakuro-guchi partition (D9 decorative) + its board door, bath room, boiler lean-to, koshiyane) |
| tr_stable | Land_JP_StableRow_Itabuki, _Thatch (5.5 x 2.5 ken: four stalls open to the yard, tack room) |
| tr_booth | Land_JP_Booth_Barber (2 x 2 ken), Land_JP_Booth_Misemono (3 x 2.5 ken, straw-mat walls, stage) |
| tr_workshop | Land_JP_Workshop_Doma_Itabuki / _Sangawara (3 x 2.5 ken), Land_JP_Workshop_Bench_Itabuki / _Sangawara (3.5 x 3 ken, closed back room) |
| tr_timber | Land_JP_Timber_SawShed (4 x 2 ken), Land_JP_Timber_Store (4 x 1.5), Land_JP_Timber_ShingleShed (2 x 1.5) |
| tr_foundry | Land_JP_Foundry_Itabuki / _Sangawara (4 x 3 ken, eave 3.80, 1.5-ken koshiyane) |
| tr_site | Land_JP_Compound_StableYard / TimberYard / FoundryYard (K3 board fences + kabuki gates, via dwelling.compound) |
Budgets: the tiled bench workshop +11.5 % (furnished +12.2 %) and the tiled foundry +1.3 % over 'standard', both with
an over_budget_ok reason (`trade.over_budget_ok`).

## Props (`spikes/W3B/props_w3b.py`, cat tradefit, `python spikes/W3B/build_w3b.py [prop ...] [--no-binarize] [--pack]`)
34 props / 63 models, all pass (TXT none needed); jp_furniture 585 classes (fragment W3B, order 50).
yubune (+staved), bath_boiler (+ab), bath_stools (+tipped), bandai (+ab), nagashi (+warped), datsui_dana (+ransacked),
tack_wall (+taken), ekisha_table (+upset), barber_kit (+spilled), misemono_sign (+torn), show_cage (+open), kezuridai
(+knocked), sawhorses (+knocked), dogubako (+ransacked), frames_lean, rokuro (+broken), soroban_tray, bamboo_stock
(+scattered), basket_work (+abandoned), togidai (+upset), urushi_tray (+spilled), kinko_bench (+taken), saw_trestle
(+fallen), log_stack (+collapsed), timber_upright (+half), plank_stack (+scattered), shingle_split (+scattered),
koshikiro (+fallen), fumifuigo (+broken), imono_moulds (+broken), toribe_rack, cast_pots (+scattered), scrap_heap,
bell_mould. **Pitfall (FX1's):** a folder binarize crashes on an existing ODOL: rebuilding a few props, binarize them
with `python spikes/W3B/binsingle.py <p3d ...>` (temp folder) instead.

## Furnished (`buildings/w3b_sets.py` on D3's Room placer; registry `W3B_FURNISHED`, folder buildings/tr_furnished)
f_tr_sento, f_tr_stablerow, f_tr_booth_barber, f_tr_booth_misemono, f_tr_ws_joinery, f_tr_ws_turner, f_tr_ws_basket,
f_tr_ws_polisher, f_tr_ws_lacquer, f_tr_ws_kinko, f_tr_timber_saw, f_tr_timber_store, f_tr_timber_shingle, f_tr_foundry
(1,012 checks). Sparse spaces: the bath room, the boiler lean-to, the barber's bench, the open sheds, the foundry floor.

## Island (`python spikes/W3B/layout_w3b.py` -> test/placements/W3B.csv + test/ce/W3B_mapgrouppos.xml; then
`python spikes/W3B/map_w3b.py` -> w3b_map.jpg + SHOWCASE_MAP.md W3B section)
A artisans' street (z ~1003, x 1033-1092): A1-A6 workshops north side, A7 barber, A8 show booth, A9-A14 stalls.
B bathhouse B1 (1048.5, 1061) + stable yard B2/B3 (1069.3, 1056.4) by the post-town street. T timber yard (1000-1027,
902-922). F foundry yard (1035-1053, 903-918). 38 rows, 17 CE groups; layout checks 0 problems (checked against every
building of every CSV, not just C.csv). World + mission rebuilt: verify_oprw PASS 4216/4216.
Placecheck flags (by design): the bench workshops "sunk 0.272" (the shell's lowest solid, as W2F's tea house bench),
the stable tie post / trough embedded.

## Checks at the end
verify_all --full: 277 buildings, 18,522 checks, 0 failures (W3B 32 buildings / 1,825); bindcheck 277/277;
lathecheck_w3b 104 closed lathes ok, 0 inside out; hangcheck 0; handlecheck 40 / 0; props 63/63.

## Not done / open
- Hot-spring bath hut (TR10): not built (the brief's "if cheap"; time went to the rest).
- The sento's upstairs rest room (G1-5 cap; Stephen's call, asked in the checklist).
- Painted picture signboards (no picture atlas cell): the show booth's sign is plain panels.
- Navmesh not regenerated (GUI step).

## How to resume
- Shells: `cd buildings && python pipeline.py <tr_key...> --no-pack --jobs 4` (logs data/C/_build/verify_logs).
- Quick try: `cd spikes/W3B && python try_tr.py sento '{}'`; family sheet `python spikes/W3B/render_w3b.py family`;
  rooms sheet `python spikes/W3B/render_w3b_rooms.py rooms --jobs 4`; prop previews `python spikes/W3B/render_w3b_props.py`.
- Packs: `cd buildings && python -c "import pipeline; pipeline.pack()"`; `python tools/assemble_config.py jp_furniture --pack`.
