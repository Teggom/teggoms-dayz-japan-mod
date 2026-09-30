# TIMELOG F1 (G4 walk fixes)

2026-09-30 15:01:23 | START | F1 | G4-fixes | 5h 13% wk 27%
2026-09-30 15:08:05 | SETUP DONE | read contract, plan log, 5 progress files, PLAYBOOK 15, B3a/B3b/L1 pipelines | F1 | G4-fixes | 5h 16% wk 28%
2026-09-30 15:10:35 | FIX START | 1 noren texture streaks | F1 | G4-fixes | 5h 17% wk 28%
2026-09-30 15:21:00 | FIX DONE | 1 noren texture streaks | cause confirmed: v squeezed 1.1 m into 0.03, u 0.06 over 0.34; now real-scale per-face mapping (mirrored plain column, mark row, _w2 hem/bounce), Res 2 too, yatai noren too | F1 | G4-fixes | 5h 19% wk 28%
2026-09-30 15:21:00 | FIX START | 2 fire tub sliver (worked alongside 1, same B3b build) | F1 | G4-fixes | 5h 19% wk 28%
2026-09-30 15:21:00 | FIX DONE | 2 fire tub sliver | cause confirmed: fill disc at phase 0 vs lathe phase pi/n = gaps at every stave corner; vessel() + well water discs now match phase, reach 3 mm into the wall, inner wall runs 3-4 cm below | F1 | G4-fixes | 5h 19% wk 28%
2026-09-30 15:21:00 | FIX START | 3 laundry kimono + 4 forks (same B3b build) | F1 | G4-fixes | 5h 19% wk 28%
2026-09-30 15:21:00 | FIX DONE | 3 laundry kimono | cause confirmed (0.06 noren strip over 1.25 m, 5x3 grid funnel); new kimono_hung(): T, pole through sleeves, fold, plain indigo cotton at world scale | F1 | G4-fixes | 5h 19% wk 28%
2026-09-30 15:21:00 | FIX DONE | 4 laundry forks | cause confirmed (branches in x); forks + crossed stakes open across z, pole at the computed seat; ab_down pole pivots on the standing seat; hanetsurube prongs widened (sweep went through them) | F1 | G4-fixes | 5h 19% wk 28%
2026-09-30 15:21:40 | FIX START | 5 floating kama lid | F1 | G4-fixes | 5h 19% wk 28%
2026-09-30 15:31:39 | FIX DONE | 5 floating kama lid | cause confirmed (lid built at the pot's base height, pot seated 0.63 up); jp_f_kama_nolid = pot only, new jp_f_kama_lid (flat) placed on the doma by the machiya recipe (count=False) | F1 | G4-fixes | 5h 22% wk 28%
2026-09-30 15:31:40 | FIX START | 6 kamidana roof + 7 cloth drape + 8 roadway (worked in one B3a/L1/L2 pass) | F1 | G4-fixes | 5h 22% wk 28%
2026-09-30 15:31:40 | FIX DONE | 6 kamidana roof | cause confirmed (prism extruded along z); roof along x (hira-iri), ridge billet, 3 katsuogi, chigi; vases 8->6 sides to stay <=300; L1 shimenawa set unaffected (render) | F1 | G4-fixes | 5h 22% wk 28%
2026-09-30 15:31:40 | FIX DONE | 7 floating chest cloth | cause confirmed (flap level at rim height 0.13 m over empty space, 1-2.2 cm off the face); cloth_drape now lands on the inside cloth/floor, hugs the rim, 4 mm off the face, bellies over ring pulls; nagamochi, tansu ransacked, kori open | F1 | G4-fixes | 5h 22% wk 28%
2026-09-30 15:31:40 | FIX DONE | 8 roadway | cause confirmed (no Roadway LOD); fkit.road_tops on misedana (+toppled), zukue, nagamochi (lid / inner floor), tansu tops, box_l, box stack, tawara + stacks, kamasu stack, L1 armour chest + casks, L2 stool; decor.blocks: roadway = walk-on only if top <= 0.30 | F1 | G4-fixes | 5h 22% wk 28%
2026-09-30 15:43:18 | FIX DONE | 9 well diagnostic | cause found: well p3ds lacked Geometry named property class=house (vanilla pump: class=house, map=waterpump) so the .wrp object never bound to its Land_ class; added + TEMP [JPWell] DeferredInit print | F1 | G4-fixes | 5h 25% wk 29%
2026-09-30 15:43:18 | REBUILD DONE | B3a 113 + L1 185 -> jp_furniture.pbo (298 cl); B3b 129 + L2 81 -> jp_site.pbo (210 cl); pipeline.py: jp_buildings.pbo; C.csv/CE unchanged (no world rebuild needed) | F1 | G4-fixes | 5h 25% wk 29%
2026-09-30 15:43:18 | CHECKS DONE | B3a 113/113, L1 185/185, B3b 129/129, L2 81/81, TXT 66/66, shell 78/78, shop 137/137, toilet 19/19, combos 60/60 (combos.json unchanged); binarize 0 warnings | F1 | G4-fixes | 5h 25% wk 29%
2026-09-30 15:43:18 | CHECKLIST DONE | TEST_CHECKLIST.md = ~10 min G4 re-check of the 8 fixes + well; sheet spikes/F1/f1_fixes.jpg | F1 | G4-fixes | 5h 25% wk 29%
2026-09-30 15:44:04 | END | commits fcd7dd7, 3d3c46d (+ this log) | F1 | G4-fixes | 5h 25% wk 29%
