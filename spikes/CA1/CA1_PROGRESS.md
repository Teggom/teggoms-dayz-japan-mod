# CA1 progress: config assembler + budget-class tidy-up (agent CA1, 2026-10-01)

Brief: the lead's CA1 brief (PRODUCTION_PLAN 2026-10-01 "Next: the config assembler"). Time log `japan_dev/TIMELOG_CA1.md`
(logger `python spikes/CA1/tlog.py "<event>" CA1 "<tag>" <5h> <wk>`).

## Inventory (every PBO in ..\@Japan\addons)

| PBO | config writers before CA1 | CfgVehicles | status |
|---|---|---|---|
| jp_furniture | spikes/B3a/build.py (+ B4 props_fittings), spikes/L1/build_l1.py, spikes/S1/build_s1.py, spikes/W2F/build_w2f.py; pack-only: B4/build_fittings.py, FP1/pack.py, FP2/pack.py | 522 | **assembled** (_frags B3a 113, L1 185, S1 175, W2F 49) |
| jp_site | spikes/B3b/build.py (+ W2 / FP1 / FX2 modules), spikes/L2/build_l2.py; pack-only: FP1/pack.py, FP2/pack.py | 320 | **assembled** (_frags B3b 239, L2 81) + jp_site_wells.c |
| jp_buildings | buildings/pipeline.py only (already combines every registry record) | 193 | single writer, unchanged |
| jp_common | research/materials/build_materials.py only (static config; make_*_materials.py call its pack()) | 1 | single writer, unchanged |
| jp_characters / jp_weapons / jp_plants / jp_structures | W / A / F / B spike tools, one each | 4 / 3 / 4 / 2 | single writer, unchanged |
| jp_worlds_testisland | spikes/T_terrain/build_world.py | 0 | single writer, unchanged |
| jp_efftest_{medium,high,xhigh,max} | spikes/effort_test/<level>/build.py | 2 each | single writer, unchanged |

## Status
- [x] snapshot `before` (spikes/CA1/_snap/before, all 13 PBOs; packed == src for all: cfgdiff 0)
- [x] tools/cfgdiff.py (class-level diff of config.cpp / model.cfg / PBOs) + tools/assemble_config.py
- [x] 6 builders write fragments (`--config-only` re-emits from the masters); pack() of B3a / B3b = assembler pack
- [x] selftest (spikes/CA1/selftest.py): copy assembles identical; same-body dup kept once; conflicting dup fails
- [ ] equivalence: src configs vs before 0 diffs; packed after vs before 0 diffs (pack may be blocked by the server)
- [ ] single-builder rebuild proof (B3a, then B3b)
- [ ] budget tidy-up
- [ ] checks: verify_all (cache + --full once), bindcheck, prop suites (TXT, hangcheck, handlecheck)
- [ ] README + B0_PROGRESS + PRODUCTION_PLAN log; commit + push

## Resume notes
- `python tools/assemble_config.py [jp_furniture|jp_site] [--pack|--check|--list]`
- `python spikes/CA1/snapshot.py <name>`; `python spikes/CA1/snapshot.py --compare before <name>`
