# S1 progress: the KEEP_TRADES shop dressing sets (agent S1, 2026-09-30)

Brief: SHOP_SETS.md spec, the new goods props into jp_furniture.pbo, a set definition per trade the decorator applies
to any townhouse shop room, a demo shop per 4-5 trades, signs via the shop text atlas, contact sheets. Time log:
`japan_dev/TIMELOG_S1.md` (logger `python spikes/S1/tlog.py "<event>" S1 "<tag>" <5h> <wk>`).

## Status (checkpoint)
- Spec: `research/interior/SHOP_SETS.md` (28 trades: KEEP_TRADES §A is headed 22 but names 28).
- Materials (add only): `research/materials/make_s1_materials.py` -> jp_m_decal_sumi_text_shop, jp_m_lacquer_shu,
  jp_m_ceramic_porcelain, jp_m_leather_tan, jp_m_food_tofu; palette lacquer_shu, porcelain_sometsuke (assumed).
- Pipeline: `spikes/S1/build_s1.py` (B3a's build.py + L1's build_l1.py, untouched; S1 masters in spikes/S1/out, checks
  in spikes/S1/checks.json incl. TXT), kit `s1kit.py`, props `props_s1_g1..g6.py`, renders `render_s1.py`.
- Sets: `buildings/shop_sets.py` (trade specs + the mise planner + whole-house dressings), hooked into
  `buildings/furnish_sets.py` (SETS shop_<trade>_<3k|2k>_ab<0-2>); furnishkit takes a set's `shell` options.
- Shell option: `parts/kit/jpparts/templates/townhouse.py` mise_floor ('_455' | '_910'): the board display strip
  (floors.mise) instead of the front tatami row; off by default.
- Demo shops (registry S1_SHOPS, not placed): s1_th_edo_3k_middle_kanamono 103/103.

## Groups
| Group | Trades | State |
|---|---|---|
| g1 | aramono, draper, furugi, kanamono, setomono | props 34 models pass; sets in shop_sets.py; demo kanamono PASS |

## How to rerun
- Props: `python spikes/S1/build_s1.py [prop ...] [--no-binarize] [--pack]`
- Renders: `python spikes/S1/render_s1.py [prop ...]`
- A demo shop: `python buildings/pipeline.py s1_<key> --no-pack`
- Materials: `python research/materials/make_s1_materials.py [--no-pack]`
