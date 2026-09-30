# C1 progress: Phase C wave 1, town shells (agent C1, 2026-09-30)

Brief: bare town shells (no furniture): all 60 townhouse units + cheap extras, the post-town house (DW10), the inn
(TR05), through buildings/pipeline.py, test rows on the island, render sheets. Time log: `japan_dev/TIMELOG_C1.md`
(logger `python spikes/C1/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).

## Done
- [x] 0 WELL_DIAG removed (spikes/B3b/build.py False, wells rebuilt, jp_site.pbo repacked by build_l2 --pack:
  210 classes, no `JPWell` string in the PBO). Commit 7598034.
- [x] 1-4 81 shells, all through the pipeline, all checks pass (4,717 checks; buildings/<family>/checks/<key>.json):
  - townhouse (69): the 60 template combinations + 9 extras (Edo board-roofed middles 2/3/4 ken x toriniwa L/R,
    one Edo kakigara 3-ken middle, Kamigata 3-ken middles with kyo / komeya lattice fronts)
  - posttown (8): 4 detached (tile/board roof x plastered/board upper front), 2 with the stable (umaya in a 2-ken
    kitchen doma), a row end + a row middle (party parts)
  - hatago (4): 3 ordinary 5-ken inns (tile / board / mushiko fronts; oku split in two guest rooms) + the grand inn
    (full upper storey, jp_p_stair _box, 2 upstairs rooms)
  - machiya 78/78, furnished 137/137, toilet 19/19, test unit 41/41, combos 60/60, parts 168/0 failures
- [x] 5 island: the C1 test street at z 1080 (registry C1_PLACEMENTS, spikes/C1/layout.py): pending world build
- [x] 6 sheets research/production/contact_sheets/c1_family|street|seams|inns.jpg (spikes/C1/render_c1.py)

## Kit / pipeline changes (all re-verified)
- raycheck.cast: culled + staged (same nearest hits, test spikes/C1/test_cast.py; ~9x faster checks)
- templates/townhouse.py: position 'detached', region 'tokaido', frontage 5, upper (mushiko/nuriya/board/full),
  pent override, stable, split; defaults unchanged (combos identical before the kit fixes below)
- party.py: seam cap on the street pent for any region without udatsu; corner pent keeps an R3 fascia strip
- kit fixes found by C15/visual: rafters and end brackets kept inside a slope (roofs.rafters, roofparts.pent),
  kawara verge far strip matches the tile section (kawara.verge), no board-wall rail above a low wall's top rail
  (walls.wall_run board_vertical)
- pipeline.py: families (dir/params/name/class entries, records|rooms|checks/<key>.json), batch binarize of a
  model folder, --jobs N parallel checks, --verify-only, --family; buildings/shellkit.py (recipe), shellcheck.py
  (the machiya's check set generalised + stair checks ST1-ST5)

## How to resume
- Everything: `python buildings/pipeline.py --jobs 10` (~9 min: builds 84, binarizes, packs, checks)
- One shell: `python buildings/pipeline.py <key>`; checks only: `python buildings/pipeline.py --verify-only <key>`
- Combos: `python buildings/townhouse_unit_test/combos.py`; sheets: `python spikes/C1/render_c1.py --jobs 10`
- Island layout: `python spikes/C1/layout.py` (prints C1_PLACEMENTS, checks overlaps)
