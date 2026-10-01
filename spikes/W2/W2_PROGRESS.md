# W2 progress: outdoor wave 2 (BUILD_LIST items 11, 22-27) + Stephen's additions

Agent W2 (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_W2.md` (logger `spikes/W2/tlog.py`). Era verdicts:
`research/outdoor_kit/W2_ERA.md`. Ran concurrently with S1 (shop sets; S1 owns materials and jp_furniture).

## Status (checkpoint 1: all 7 items built, packed)
91 models, checks 91/91 (B3b's set + TXT + C7 on the steps), binarize 220/220 ODOL (B3b 129 + W2 91), 0 warnings;
`@Japan/addons/jp_site.pbo` = **301 classes** (B3b 129 + W2 91 + L2 81) after `python spikes/L2/build_l2.py --pack`.

| Item (folder) | Models | New / variants / abandoned | Res 1 faces (max) |
|---|---|---|---|
| jp_s_torii_wood (shrine) | 20 | 1 / 16 / 3 | 405 (medium <= 1,500) |
| jp_s_torii_stone (shrine) | 10 | 1 / 8 / 1 | 398 (medium) |
| jp_s_stone_lantern (shrine) | 13 | 1 / 10 / 2 | 339 box, 289 small |
| jp_s_chozubachi (shrine) | 4 | 1 / 2 / 1 | 116 |
| jp_s_stone_steps (shrine) | 13 | 1 / 10 / 2 | 255 |
| jp_s_grave_stones (grave) | 24 | 1 / 17 / 6 | 259 |
| jp_s_grave_wood (grave) | 7 | 1 / 5 / 1 | ~260 |

### Stephen's additions
- **Torii:** every rural form with no rope / rope / rope + 4-step zigzag shide; mossy variants (moss on the kasagi,
  tie-beam, post feet and footing stones) for wooden shinmei, wooden myojin and the small stone torii; vermilion
  myojin kept restricted (Inari / Hachiman) and only with an Inari plaque; the yard-shrine mini torii (plain, vermilion,
  rope + shide) carry mount 'yard'. Rope anchor height in each sidecar (`rope_y`, `rope_z`).
- **Lanterns:** mossy Kasuga 1.8 / 2.4 / 3.0, square 2.4 and oki (+ a mossy 1.8 with its jewel fallen).
- **Graves:** 24 stones (list: 8), only 1730 forms: board x5 (sizes, tall mossy, set-in-ground small, leaning, gable
  snapped off), boat-halo x3 (adult, child, sunk), round-headed x3 (incl. plain), square pillar x2 (rare: flat top with
  water hollow, Kyoho pointed top), gorinto x5 (0.6, 2.0 on a platform, re-stacked mismatched, fallen rings, a small
  fragment heap), hokyointo x2, a child's Jizo with bib, field stones x3 (single, earth mound, pair). Name / date crops
  of the two posthumous-name cells give with / without inscription variety; gorinto stay uninscribed.
- **Steps:** C7 check on the written Roadway: ramp 27.8 deg (rise 0.16, tread 0.303), the foot edge (z 0, y 0) and head
  edge (z -run, y rise) span the full width on every flight and landing, so modules chained by their connectors
  (sidecar `connectors`) give one continuous Roadway; treads at most one riser above the ramp.

## Pipeline (built INTO B3b's)
- `spikes/B3b/build.py`: MODULES += props_torii, props_shrine, props_grave; every model now also gets L2's TXT check;
  `P.checks_extra` hook (C7); sidecar rows carry `mount` + `master` when a prop sets a mount.
- `spikes/B3b/w2kit.py` (new helpers: sweep, hollow, moss_strip / moss_foot, shear, carved / inked, torii_rope).
- `spikes/B3b/render.py`: groups w2_torii / w2_shrine / w2_grave -> `research/outdoor_kit/contact_sheets/w2_*.jpg`
  (`python render.py --sheets w2`).
- `parts/kit/jpparts/decor.py`: OUTDOOR_MOUNTS += shrine, graveyard, slope (commit 6d1c6ce, additive only).
- Rebuild: `python spikes/B3b/build.py [item ...] [--pack]`, then ALWAYS `python spikes/L2/build_l2.py --pack`.

## Found
- **binarize.exe is not deterministic:** the same MLOD master binarized twice gives different ODOL bytes (same size;
  `spikes/W2/bindet.py`: 9 of 12 roadside models differ run to run). So the 140 B3b / L2 ODOLs that show as modified
  after a re-pack are noise; B3b's faces and pass results are unchanged (129/129). Compare masters or checks, never ODOLs.

## Missing materials / atlas cells (S1 owns materials: not added)
- More posthumous names / dates on the carved-text atlas (only 2 grave cells: the 24 stones reuse them by cropping).
- Sanskrit seed syllables (bonji) for gorinto / hokyointo faces (built blank).
- An outdoor bare-earth / grave-mound material (mounds use `jp_m_ground_leaf_litter`).

## Not done / open
- Nothing tested in game; no test-island placement (brief).
