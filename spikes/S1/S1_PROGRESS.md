# S1 progress: the KEEP_TRADES shop dressing sets (agent S1, 2026-09-30)

Brief: SHOP_SETS.md spec, the new goods props into jp_furniture.pbo, a set definition per trade the decorator applies
to any townhouse shop room, a demo shop per 4-5 trades, signs via the shop text atlas, contact sheets. Time log:
`japan_dev/TIMELOG_S1.md` (logger `python spikes/S1/tlog.py "<event>" S1 "<tag>" <5h> <wk>`).

## Status: DONE (built, binarized, packed; nothing placed on the island; untested in game)

- **Spec:** `research/interior/SHOP_SETS.md` (KEEP_TRADES §A is headed "22 + 3 ☆" but names 28 trades: all 28 have a
  set; the 3 ☆ are listed as recombinations, not built). Section 6 = as built + the set API.
- **Materials (add only, B1 pipeline):** `research/materials/make_s1_materials.py` -> `jp_m_decal_sumi_text_shop`
  (a third ink atlas: 32 kanban / menu cells, pawn tags, packets, title slips, drug labels, an Otsu-e, a fan, a page;
  fonts Yuji Syuku + Yuji Hentaigana Akebono), `jp_m_lacquer_shu`, `jp_m_ceramic_porcelain`, `jp_m_leather_tan`,
  `jp_m_food_tofu`; palette `lacquer_shu`, `porcelain_sometsuke` (assumed). C1 in `checks_s1.json`. jp_common repacked.
- **Props:** 84 props = 175 models (84 new, 3 variants, 88 abandoned), all checks pass incl. TXT
  (`spikes/S1/checks.json`), 175/175 ODOL, 0 binarize warnings. jp_furniture.pbo = 473 classes.
  Pipeline `spikes/S1/build_s1.py` (on B3a's build.py + L1's build_l1.py, both untouched), kit `s1kit.py`, props
  `props_s1_g1..g5.py` (g5 holds groups 5 and 6).
- **Sets:** `buildings/shop_sets.py` (28 trade specs, `apply_mise`, `front`, `dress`, `sets`), hooked into
  `buildings/furnish_sets.py` (168 SETS: shop_<trade>_<3k|2k>_ab<0-2>). furnishkit takes a set's `shell` options.
  `spikes/S1/setcheck.py`: 168/168 pass on th_kamigata_3k_middle_toril / th_kamigata_2k_middle_torir.
- **Shell option:** `parts/kit/jpparts/templates/townhouse.py` `mise_floor` ('_455' | '_910', default None): the board
  display strip (floors.mise) instead of the front tatami row.
- **Demo shops** (registry `S1_SHOPS`, shipped, not placed): kanamono 103/103, tabako 94/94, mochiya 110/110, kusuri
  (ab 2) 103/103, shitate 94/94, ningyo 103/103. jp_buildings.pbo repacked.
- **Sheets:** `research/interior/contact_sheets/s1_sets_1..5.jpg` (each set: room, cut, street front, reference),
  `s1_props_goods*.jpg`, `s1_props_fit*.jpg`, `s1_props_sign*.jpg` (renderers `render_sets.py`, `render_s1.py`).
- **decor.py:** not changed.

## Re-runs (after the furnishkit / furnish_sets / registry / townhouse-template changes; decor.py unchanged)
- B3a + B4 props 113/113, L1 185/185 (sandboxed copies `check_b3a.py`, `check_l1.py`; pass and faces unchanged).
- Furnished machiya `python buildings/pipeline.py machiya_t3_01_shop --no-pack`: 137/137.
- `spikes/S1/rerun_all.py 10`: 128 buildings (machiya 78, shop 137, toilet 19, C1 81, C2 21, kura 3, C3 furnished 14,
  S1 demos 6), 8,064 checks; 10 'src p3d is not ODOL' failures were a race (another process re-staged and
  re-binarized 59 building p3ds in src at 21:46 while the re-run read them); those 10 re-verified alone: all pass.
  Townhouse combos 60/60, 0 over budget. The 59 rewritten building ODOLs in src are not mine and not committed.

## Decisions I made
- All 28 named trades get a set (the "22" header undercounts).
- Shop signs are jp_furniture front proxies (mount wall, facade frame like B3b's shopfront), hung perpendicular to the
  facade with the text on both faces on a gofun-white panel (ink on bare dark wood did not read).
- Stock furniture is half-ken (0.91) so it fits the party wall of a 3-ken shop with the chōba behind it.
- The stand faces the street (low step out); goods clusters are visual-only and sit off the steps' loot points.
- Abandoned twins are read from the sidecars (same prop, variant and mount); the tipped desk is never used (its
  footprint reaches the mise-oku door zone).
- The moneychanger's sign is a fundō outline although BTI 830 says "coin-shaped" (flagged).
- The sugidama uses L2's alpha-cut foliage (_w0 green, _w2 brown).

## Not done / open
- Whole-house dressing exists only for 3-ken ToriL and 2-ken ToriR units (the mise set is generic); 4-ken and the
  2-ken end units need their own toriniwa / oku / kitchen layout.
- No in-game test; no navmesh; nothing placed on the island (per brief).
- The ☆ sets (tatami maker, lantern and umbrella, toy and clay-doll) are not built.

## How to rerun
- Props: `python spikes/S1/build_s1.py [prop ...] [--no-binarize] [--pack]`
- Set checks: `python spikes/S1/setcheck.py [trade ...] --jobs 8`
- A demo shop: `python buildings/pipeline.py s1_<key> --no-pack`
- Renders: `python spikes/S1/render_s1.py [prop ...]` + `--sheets`; `python spikes/S1/render_sets.py --jobs 6`
- Materials: `python research/materials/make_s1_materials.py [--no-pack]`
- Re-runs: `python spikes/S1/check_b3a.py`, `python spikes/S1/check_l1.py`, `python spikes/S1/rerun_all.py 10`
