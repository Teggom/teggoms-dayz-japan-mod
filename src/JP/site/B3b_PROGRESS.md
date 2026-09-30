# B3b progress: outdoor site objects, wave 1 (research/outdoor_kit/BUILD_LIST.md, the 20 W1 items)

Agent B3b (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_B3b.md`.

## Status
- Checkpoint 1 (round wood): oke, fire_tub, firewood_stack, bench, laundry_pole, tenbin, handcart = 42 models,
  checks 42/42, binarize 42/42 ODOL, CfgConvert OK.

## Next
wells (tsurube incl. `_roofed`, hanetsurube; Land_ classes + Well script), stone (jizo, stele, jizo hut; bib material),
street (gutter, shopfront, lantern_sign, nobori, stall, kosatsu), straw (straw_stack, shimenawa); then PBO, sheets.

## How to resume
- Pipeline: `spikes/B3b/` (skit.py = B3a's fkit/bits + outdoor helpers; build.py = checks, sidecars, config, binarize,
  pack; render.py = renders + sheets; props_*.py = one module per work group). B3a's files are imported, never edited.
- `python spikes/B3b/build.py [item ...] [--no-binarize] [--pack]`; `python spikes/B3b/render.py [item ...]`;
  `python spikes/B3b/render.py --sheets`.
- MLOD masters: `spikes/B3b/out/` (not committed, regenerated). ODOL + sidecars: `src/JP/site/<group>/`.
