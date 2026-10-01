2026-10-01 09:47:20 | START | FB1 | fixes | 5h 5% wk 45%
2026-10-01 09:51:33 | SETUP DONE | FB1 | setup | 5h 5% wk 45%
2026-10-01 09:51:33 | GROUP START | A class/p3d names | A | 5h 5% wk 45%
2026-10-01 09:51:33 | GROUP START | B second door cause | B | 5h 5% wk 45%
2026-10-01 10:11:00 | GROUP DONE | A class/p3d names | cause: 97/128 family p3ds named after registry keys (2k vs 2ken, jp_f_*, jp_s1_*) so no Land_<stem> class (logs: house, config class missing); result: p3d = class minus Land_ for all, bindcheck 128/128 + B1/B2 per-building check, all 128 pass, MLODs byte-identical | 5h 17% wk 46%
2026-10-01 10:11:01 | GROUP DONE | B second door cause | none found: machiya/shop/toilet config + model.cfg identical to 3d3c46d, ODOL identifiers identical, logs show them bound; every other placed door building was unbound | 5h 17% wk 46%
2026-10-01 10:11:01 | PBO PACKED | FB1 | jp_buildings.pbo 128 classes (A rename) | 5h 17% wk 46%
2026-10-01 10:22:55 | GROUP START | C Kinai band under the roof | investigated from ~09:58 alongside the rebuild (logged late) | 5h 22% wk 47%
2026-10-01 10:22:55 | GROUP DONE | C Kinai band under the roof | cause: yamato-mune takahe hung 0.45 m under the slope out to the eave (a 0.3 x ~1 m white block under each eave corner) and the thatch ridge bundle ran 0.25 m past the gable over/out of it; result: takahe starts at the thatch underside over the overhang, rises 0.12 over the ridge, ridge stops inside; Kinai takahe + furnished rebuilt, pass | 5h 22% wk 47%
2026-10-01 10:22:55 | GROUP START | D kura doors/shutters + colour | from ~10:20 (logged late) | 5h 22% wk 47%
2026-10-01 10:22:55 | GROUP DONE | D kura doors/shutters + colour | cause: leaves 0.16+0.03 step, shutters 0.12 (big-kura numbers); result: leaves 0.11+0.025 (~4.5 sun), shutters 0.08 (~2.5-3 sun), all exterior shikkui -> FP1's jp_m_wall_shikkui_aged on all 3 kura + 2 furnished; rebuilt, pass (needs FP1's jp_common pack) | 5h 22% wk 47%
2026-10-01 10:22:55 | GROUP START | F tools off the wall | from ~10:12 (logged late) | 5h 22% wk 47%
2026-10-01 10:22:55 | GROUP DONE | F tools off the wall | cause: C3 site() spots by eye, 0.42-0.51 m off the wall (spikes/FB1/leancheck.py); result: Kanto tools + charcoal, Kinai tools, komeya bundle, inn firewood x2, machiya tenbin, gallery L57 re-seated (touch, D8 overlap-free); 4+1 rebuilt, pass | 5h 22% wk 47%
2026-10-01 10:22:55 | GROUP START | G low hill-stair torii | from ~10:10 (logged late) | 5h 22% wk 47%
2026-10-01 10:22:55 | GROUP DONE | G low hill-stair torii | cause: S70 is the medium stone torii, nuki 1.93 m over its base -> 1.66 m clear on the slope (S63 1.81); result: S70 + S63 -> large stone torii (2.60 / 2.79 m clear, spikes/FB1/toriiclear.py), basin S74 moved 0.5 m clear | 5h 22% wk 47%
2026-10-01 10:24:03 | WAITED FOR FP1 | start | H needs FP1's END (collapsed torii, ladder, well) | 5h 22% wk 47%
2026-10-01 10:35:11 | CHECKS DONE | FB1 | 128/128 buildings pass (8,190 checks: machiya 78, furnished machiya 137, toilet 20, all family shellchecks), bindcheck 128/128, combos 60/60 (H world checks follow) | 5h 28% wk 47%
2026-10-01 10:56:43 | WAITED FOR FP1 | end | FP1 END 10:54; collapsed torii S100-S104 placed (shrine.py), ladder/well need no placement change | 5h 34% wk 48%
2026-10-01 10:58:32 | ISLAND BUILT | FB1 | build_world 4090 objects (545 placements), build_mission (30 CE groups now snap to their wrp buildings), verify_oprw PASS 4081/4081; maps re-rendered (S100-S104) | 5h 35% wk 48%
2026-10-01 10:59:20 | GROUP START | E roofless street house | from ~09:55, alongside A (logged late) | 5h 38% wk 49%
2026-10-01 10:59:20 | GROUP DONE | E roofless street house | NOT reproduced: likely D5 (Edo 2ken board-roof tailor, middle of the 5 Edo units right of S01); roof present + front-facing in R1/R2/R3 (sky census, culled renders from street/torii/above); pale silver kokera 0.17 m below tiled neighbours may read as sky; left to Stephen's re-check with a screenshot, no change made | 5h 38% wk 49%
2026-10-01 10:59:20 | GROUP START | H collapsed torii + world | 10:55 after FP1 END | 5h 38% wk 49%
2026-10-01 10:59:20 | GROUP DONE | H collapsed torii + world | S100-S104 placed (shrine.py, flattest hill-foot ground), ladder + well same p3ds (no change, 9 site Land_ classes bind), world + mission rebuilt, verify_oprw PASS 4081/4081 | 5h 38% wk 49%
2026-10-01 10:59:20 | CHECKLIST DONE | FB1 | TEST_CHECKLIST.md ~15 min re-check (doors first, FP1 1-15 + FB1 C-G with IDs) | 5h 38% wk 49%
2026-10-01 10:59:40 | END | FB1 | session | 5h 38% wk 49%
