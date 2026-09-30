# F1 progress: G4 walk fixes (agent F1, 2026-09-30)

Brief: fix Stephen's 8 G4 findings + a temporary well diagnostic, rebuild through the pipelines, re-run every check,
before/after sheet `spikes/F1/f1_fixes.jpg`, short re-check in TEST_CHECKLIST.md. Time log: `japan_dev/TIMELOG_F1.md`
(logger `spikes/F1/log.py`).

## Status (checkpoint 1: B3b source fixes done, masters rebuilt with --no-binarize)
| # | Finding | Cause | Fix | State |
|---|---|---|---|---|
| 1 | noren streaks | confirmed: `noren_panel_uv` squeezed d 0.5-1.6 m into v 0.46-0.49 and stretched u 0.47-0.53 over 0.33 m | per-face real-scale mapping (`props_street.noren_face_uv` / `panel_sheet`): plain = the mark-free column u 0.42-0.59 mirrored in two half columns, the mark row on cell 0, _w2 ends in the torn hem and bounces inside the clean band; Res 2 = the same panels flat; the yatai stall's noren too | masters rebuilt |
| 2 | fire tub see-through | confirmed: `vessel()` fill disc at phase 0, lathe at phase pi/n: the disc's corners poked into the staves and left a sliver open at every stave corner (outer wall culled from inside) | disc on the lathe's own angles, 3 mm into the stave, inner wall 3 cm below the fill; well water discs (curb tub 12 vs 16 sides, stone curb phase) likewise | masters rebuilt |
| 3 | laundry cloth | confirmed: the 0.06 noren strip over 1.25 m, a 5x3 grid with a sleeve/body step = funnel | `props_wood.kimono_hung`: T-shaped kimono (sleeves 1.28 x 0.48, body 0.62 x 1.30) hung through its sleeves, fold over the pole, plain indigo cotton at world scale, darker collar band | masters rebuilt |
| 4 | laundry forks | confirmed: branches at x +-0.11 (the pole's plane) | forks and crossed stakes open across z; the pole sits at the computed seat (tangent to both arms); ab_down's pole pivots on the standing fork's seat; hanetsurube prongs splay then rise parallel (the sweep ran through them) | masters rebuilt |
| 9 | well: no actions | NEW: our well p3ds had no Geometry named property `class=house` (vanilla misc_well_pump_yellow.p3d has class=house, map=waterpump); a .wrp object without it is not bound to its Land_ config / script class | `build.WELL_GEO` on every well model + TEMP diagnostic `WELL_DIAG` (DeferredInit prints `[JPWell] ...`) | masters rebuilt |

Next: B3a / L1 fixes (5-8), then binarize + pack everything, machiya pipeline, checks, sheet, checklist.

## Rules kept
- Class names unchanged; no material changed; no server / game / GUI started.
- `spikes/F1/_before/` = snapshot of every MLOD master before F1 (not committed; `diffmasters.py` compares).
