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
- [x] equivalence: `snapshot.py --compare before after_assembler` and `before final`: 13 PBOs, TOTAL differences 0
  (classes, bases, bodies, declarations, file lists, furniture/site model.cfg, jp_site_wells.c). The packs were NOT
  blocked (the running server did not lock jp_furniture / jp_site). Packed entries == src files, src ODOLs == HEAD.
- [x] single-builder rebuild proof: `python spikes/B3a/build.py --pack` alone (113 models, binarize, pack) -> packed
  jp_furniture still 522 classes, B3a 113 + L1 185 + S1 175 + W2F 49 all present, cfgdiff vs before 0; then
  `python spikes/B3b/build.py --pack` alone (239) -> jp_site 320, B3b 239 + L2 81, 0 diffs. Byte-noise restored to
  HEAD (102 + 138 ODOLs, checks.json global block, binarize.log); both PBOs repacked from HEAD ODOLs.
- [x] budget tidy-up: fkit / skit / registry tables = PLAYBOOK §12's set; `over_budget_ok` per object (fkit.budget_fit,
  registry.budget_check, sacred.over_budget_ok); `tools/budget_report.py` = 9 overages, 0 not deliberate
- [x] checks: props re-run --no-binarize, `propcheck.py`: 842/842 pass, 0 face changes (only C5 budget text changed);
  TXT 191/191; verify_all (cache: 193, re-checked after the registry change, then 193 cached in 5 s) + --full;
  bindcheck 193/193; hangcheck 0; handlecheck 0/40
- [x] README "Config fragments", B0_PROGRESS "Config assembler + budget classes", PLAYBOOK §12 'How', PRODUCTION_PLAN
  log (the two config pitfalls removed); commit + push

## Decisions
- Fragments are JSON (not .cpp): structured class / base / body makes dedupe and the conflict check exact; `*.json` is
  already excluded from every pack, and `_frags` is excluded too. The assembled config.cpp is byte-identical to the old
  one except the GENERATED comment lines.
- Fragment ownership: B3a = its own MODULES list at import (incl. B4's props_fittings), B3b = its MODULES (incl. W2 /
  FP1 / FX2 modules); L1 / S1 / W2F / L2 = their category sets, as their built_models() already did.
- Statue = 'as needed (aim 3,000)' per §12: a reason is required above the aim; the 2x factor is only a runaway guard
  (the Amida dais is +54 % over the aim: image + cabinet + altar pieces in one model). Every other class: <= +50 %.
- small = 800 in both prop tables (PLAYBOOK §12, Stephen 2026-10-01); 'medium' (= detail) and skit 'box' kept as the
  older names (used by 89 / 57 models; folding them would churn every sidecar for no gain).
- PBOs with a single config writer were left alone (an assembler adds nothing there).

## Resume notes
- `python tools/assemble_config.py [jp_furniture|jp_site] [--pack|--check|--list]`
- `python spikes/CA1/snapshot.py <name>`; `python spikes/CA1/snapshot.py --compare before <name>`
