# B1 (Phase B materials): progress

Agent B1, 2026-09-29. Brief: PRODUCTION_PLAN.md Phase B item B1. Owns research/materials/, src/JP/common/materials/,
playbook/palette.json (the shared palette). B0 works in parts/kit/jpparts/, buildings/, src/JP/buildings/ in parallel.

## Status: DONE (2026-09-29), all three checkpoints committed

## Done
- Doma re-sample (G1): a 3rd photo i05 (Tsunashima, lit doma) + a 2nd diffuse box on i02 -> doma_earth
  (137,132,128); it confirms A2's request (dE 0.7). Details in the palette entry note.
- Palette: 6 entries added by `add_palette_entries.py` (B1 section): doma_earth, ash_grey (kept assumed, checked
  against 2 photos), straw_aged, leaf_litter_autumn (sampled from its CC0 scan), stoneware_pale, stoneware_dark.
- Sources: 7 new CC0 Poly Haven scans in `fetch_sources.py` (tatami_mat, hinoki_planks, old_planks_02,
  clay_floor_001, rough_linen, dry_decay_leaves, bamboo_wall).
- `make_b1_materials.py`: 34 materials x 3 wears = 102 sets (21 interior + 13 outdoor, incl. the two text atlases
  from the OFL fonts in research/fonts/, lead's go). C1 matcheck 0 FAIL, 14 WARN (all "flat": dark cloth, lacquer,
  ink) in `src/JP/common/materials/checks_b1.json`. jp_common.pbo repacked (194 MB).
- `B1_STATUS.md`: every jp_m_ name in both build lists (50): 16 existed, 34 made now, 0 not made.
- Sheets: `contact_sheets/b1_0_overview_w1.jpg`, `b1_1..b1_4_*.jpg`.
- build_materials.py: FINISH "glazed" (fresnel 1.42,0 + env_land) for stoneware + lacquer; CREDITS text for B1 and
  the fonts. render_spheres.py: optional tile_v_m (non-square tatami).

## Open for others (not B1's files)
- parts/kit/jpparts/buildcheck.py C19 hard-codes GLOSSY = kawara, namako, iron: add the two stoneware materials and
  jp_m_lacquer_black (or read build_materials.FINISH_BY_ID), or a furnished building will fail C19.

## Rebuild
`python make_b1_materials.py` (all), `--only ID,ID`, `--set interior|outdoor`, `--sheets-only`, `--status`,
`--rvmats-only`. Never while a server holds jp_common.pbo (pack() reports it).
