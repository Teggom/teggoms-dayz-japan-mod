# F1 progress: G4 walk fixes (agent F1, 2026-09-30)

Brief: fix Stephen's 8 G4 findings + a temporary well diagnostic, rebuild through the pipelines, re-run every check,
before/after sheet `spikes/F1/f1_fixes.jpg`, short re-check in TEST_CHECKLIST.md. Time log: `japan_dev/TIMELOG_F1.md`
(logger `spikes/F1/log.py`).

## Fixes (all causes confirmed in code and in back-face-culled renders)
| # | Finding | Cause | Fix |
|---|---|---|---|
| 1 | noren streaks | `noren_panel_uv` squeezed d 0.5-1.6 m into v 0.46-0.49 and stretched u 0.47-0.53 over 0.33 m | `props_street.noren_face_uv` + `panel_sheet` (per-face uvs), real scale: plain = the mark-free column u 0.42-0.59 as two mirrored half columns, mark row on cell 0 (d 0.08-0.38), _w2 ends in the torn hem (v 0.86-1) and bounces in the clean band v 0.50-0.86; Res 2 = the same panels flat; the yatai stall's noren too |
| 2 | fire tub see-through | `vessel()` fill disc at phase 0, lathe at phase pi/n: sliver open at every stave corner (outer wall culled from inside) | disc on the lathe's own angles, 3 mm into the stave, inner wall 3 cm below the fill. Every `vessel()` user (oke, teoke, ninai, fire tubs + bucket pyramid, well buckets, tenbin, L1 fire gear, L2 fire watch). Well water discs likewise (tub curb 12 vs 16 sides, stone curb phase). B3a tubs (`tub_profile`) close their bottom in the same lathe: already sealed |
| 3 | laundry cloth | the 0.06 noren strip over 1.25 m, 5x3 grid with a sleeve/body step = funnel | `props_wood.kimono_hung`: T kimono (sleeves 1.28 x 0.48, body 0.62 x 1.30) hung through its sleeves, a fold over the pole, plain `textile_cotton_indigo` at world scale, a darker collar band (_w0) |
| 4 | laundry forks | branches at x +-0.11 (in the pole's plane) | forks and crossed stakes open across z; pole centre at the computed seat (`fork_seat`, `cross_seat`); ab_down's pole pivots on the standing fork's seat; hanetsurube prongs splay then rise parallel (the sweep ran through them) |
| 5 | floating kama lid | lid built leaning on the pot at the POT's base; the pot is seated 0.63 m up | `jp_f_kama_nolid` = pot only; new `jp_f_kama_lid` (StaticObj_JP_F_Kama_Lid, flat); the machiya recipe puts it on the doma at the kamado end (count=False) |
| 6 | kamidana roof 90 deg | roof prism extruded along z | roof along x (hira-iri), ridge billet, 3 katsuogi, crossed chigi at the gables; offering vases 8 -> 6 sides (budget 300: 287); L1 shimenawa set sits as before |
| 7 | floating chest cloth | `cloth_drape` ran level at rim height 0.13 m over the open chest, 1-2.2 cm off the face | `tansu.cloth_drape(..., ft, land_y, out_gap, bump)`: lies on the inside cloth / floor, up the inner face, over the rim, 4 mm off the outer face, bellies over a ring pull; nagamochi_open (pale cloth moved to lie against the front), tansu ransacked, kori_open |
| 8 | no Roadway | no Roadway LOD | `fkit.road_tops` (flat collision tops, covered ones skipped): misedana (+toppled), zukue, nagamochi (lid; inner floor when open), tansu tops, box_l, box stack, tawara + stack6, kamasu stack3, L1 armour chest + casks (not the staved one), L2 stool. `decor.blocks`: a Roadway only means walk-on when the top is <= 0.30 m |
| 9 | well: no actions | NEW finding: our well p3ds had no Geometry named property `class=house` (vanilla `misc_well_pump_yellow.p3d`: class=house, map=waterpump; every JP building has class=house); a .wrp object without it is not bound to its Land_ class | `build.WELL_GEO` on all 8 well models + TEMP diagnostic (`build.WELL_DIAG`, DeferredInit prints `[JPWell] <type> at <pos> IsWell=1`) |

## Rebuilt
- B3a 113 (new kama_lid) + L1 185 -> jp_furniture.pbo (298 classes); B3b 129 + L2 81 -> jp_site.pbo (210 classes).
- Masters changed vs the snapshot: B3a 24, B3b 28, L1 10, L2 3 (`python spikes/F1/diffmasters.py`).

## Rules kept
- Class names unchanged (one class added); no material changed; no server / game / GUI started.
- `spikes/F1/_before/` = snapshot of every MLOD master before F1 (not committed).

## Remove the well diagnostic later
`spikes/B3b/build.py`: `WELL_DIAG = False`, then `python spikes/B3b/build.py well_tsurube well_hanetsurube` and
`python spikes/L2/build_l2.py --pack`. Keep `WELL_GEO`.
