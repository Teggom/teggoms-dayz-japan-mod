# B0 progress (kit cleanup, agent B0, 2026-09-29)

Task: PRODUCTION_PLAN Phase B item B0 = PARTS_GAP_AUDIT §5 step 0a + 0b + the townhouse-unit template from 0c.

## Baseline
- Pre-change outputs (committed at 8c9494a) were regenerated with the old build.py: MLOD, config.cpp, model.cfg,
  C.csv, CE files, rooms.json byte-identical, so the old pipeline is deterministic. Any diff after B0 is B0's.

## Status
- [x] 0a kit: jpparts.floors (tatami/boards/doma/loft + holes), jpparts.leanto (roof: 6 coverings, sloped_wall),
  walls.udatsu_placed, roofs.ridge_walk, roofs.roof per-side gov, jpparts.assemble.Builder. machiya_t3_01.py uses
  them; its MLOD is byte-identical to the baseline (scratch test, 2026-09-29).
- [ ] 0b multi-building pipeline (buildings/pipeline.py + buildings/registry.py); machiya rebuilt identical, 78/78
- [ ] 0c townhouse-unit template (parts/kit/jpparts/templates/townhouse.py) + one unit built (not on the island)

## Next
- 0b: buildings/pipeline.py + buildings/registry.py, machiya build.py becomes a shim; full rebuild + verify 78/78
