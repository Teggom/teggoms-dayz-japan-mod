# FX2 progress: statues, komainu + kitsune, detail props, torii rope, U1 veranda (agent FX2, 2026-10-01)

Brief: the lead's FX2 brief (PRODUCTION_PLAN 2026-10-01 'Stephen's decisions'). Time log `japan_dev/TIMELOG_FX2.md`
(logger `python spikes/FX2/tlog.py "<event>" FX2 "<tag>" <5h> <wk>`).

## Status: DONE (built, packed, on the island, world + mission rebuilt; untested in game)
- [x] references: 32 images / 20 objects (Met 7 + Cleveland 13), research/statues/REFS.md (the Met v1 search was
  retired 2026-10-01 -> v1.1). Missing: any photo of a stone Inari fox (neither collection has one)
- [x] statue kit (sdf.py, statuekit.py, figures.py, statues.py, fx2props.py, peek.py, render_fx2.py); notes
  research/statues/NOTES.md
- [x] material jp_m_gilt_worn (research/materials/make_fx2_materials.py; palette gilt_worn; jp_common repacked)
- [x] 1 statues: altar daises (W2F dais -> image()), stone Jizo family + huts + steles + graves (B3b jizo_figure ->
  mesh; child Jizo, boat-halo relief, bato Kannon relief = a Kannon now), bibs refitted, staff head closed
- [x] 2 komainu (style a / b / a mossy) + kitsune (key / jewel): spikes/B3b/props_guardian.py (registered in B3b
  build MODULES); placed by spikes/FX2/layout_fx2.py -> test/placements/FX2.csv (10 rows: P1, P2, V1 komainu pairs, I1
  fox pair, I2 lantern pair on the Inari path); SHOWCASE_MAP 'FX2' section; map fx2_map_guardians.jpg
- [x] 3 detail props (spikes/FX2/detail_fx2.py; W2F delegates): kagura masks (4 sculpted) + bell tree, waniguchi,
  suzu, bonsho body, ema rail + gaku-ema, offering box; w2kit.tassel 5 bundles + binding
- [x] 4 rope: sag 0.075 per 1.82 m (orig 0.10, FX1 0.05), rope 0.20 of the nuki height up (FX1 0.35), shide pushed
  into the lay (w2kit.torii_rope); shimenawa len_* + the swordsmith's hung rope use the same sag. ropeclear: lowest
  placed tip 2.31 m, 0 LOW (FX1: 2.35)
- [x] 5 U1 mawari-en: town hondo en on three sides, sides one bay deep to wakishoji: 12,428 / 3,688 / 1,638 faces,
  budget class large_plus (registry: 15,000 / 5,750 / 2,000). Village hondo tried (9,512) but failed C15 + D1/D3
  (side-en rooms) -> kept FX1's returns. Shinmei honden not changed (its free-standing munamochi posts stand where a
  side en would go)
- [x] packs: jp_site 320 classes (B3b build + L2 --no-binarize --pack), jp_furniture 522 (W2F folder binarize crashed
  again on 8 masters -> spikes/FX2/bin_single.py), jp_buildings (pipeline 12 keys; 10 noise ODOLs restored, U1 shell +
  furnished kept), W2F.csv re-laid (box shifts of 2-4 mm), world 4144 objects, mission, verify_oprw PASS 4135/4135
- [x] checks: verify_all 193 / 11,830 checks / 0 failures (and --full at the end), bindcheck 193/193, hangcheck 0,
  handlecheck 0/40, toriipost 0, ropeclear 0 LOW; props B3b 239/239, L2 81/81, W2F 49/49
- [x] sheets fx2_statues / fx2_komainu / fx2_detail / fx2_rope (spikes/FX2/sheet_fx2.py; 'before' from a git archive
  of c01351c built --no-binarize in the scratchpad), TEST_CHECKLIST 'FX2 re-check'

## Resume notes / tools
- Statue meshes are cached in meshes/<name>.json keyed by the build function's source + sdf.py + the shared helpers in
  figures.py (head, hair, staff head, folds): a helper edit rebuilds every statue (~4 min: `python spikes/FX2/statues.py`).
  Look: `sh spikes/FX2/peekall.sh [names]` -> _build/peekall.png (flipped to the game's handedness).
- Budget classes added (additive): fkit.BUDGET detail 1500 / detail_l 2250 / statue 4500 / altar 5500; skit.BUDGET
  statue (4500, 1700, 700) / detail (1500, 600, 250); registry.BUDGETS large_plus.
- B3b build.py rewrites jp_site config without L2: finish with `python spikes/L2/build_l2.py --pack` (after a noise
  restore: `--no-binarize --pack`). W2F: `python spikes/W2F/build_w2f.py <props> --pack`; when its folder binarize
  crashes, `python spikes/FX2/bin_single.py furniture <cat>/<stem> ...`, then re-pack with --no-binarize.
- Noise: `python spikes/FX2/noise.py <folders>` keeps the ODOLs of the models FX2 changed (KEEP list) and restores
  every other modified ODOL to HEAD (binarize rewrites whole folders with float noise: a byte count can't tell).

## Decisions
- Amida seated (Met 44890, the dais was seated) rather than the standing raigo Amida of CMA 136319.
- Figure right = +x (DayZ is left-handed): Jizo's staff in his right hand as both references.
- Gilt (new material) on Amida / Shaka / Kannon + their seats and halos; Jizo black-brown lacquer with a bronze staff.
- Komainu: two forms (upright reference form with the un's horn; compact Edo stone, no horn) + a mossy pair; ball /
  cub and crouching forms are later than 1730 (not built). Foxes: key + jewel.
- Lanterns: every lantern on the existing approaches already stood in a mirrored pair; added one pair on the Inari path.
- Budgets over the class line (Stephen: +30-50 % allowed): kagura masks 2,128 and bonsho 1,946 (detail_l 2,250);
  altar daises 3,490-4,622 (altar 5,500); U1 12,428 (large_plus).
