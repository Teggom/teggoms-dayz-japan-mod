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
- [x] 5 island: the C1 test street at z 1080 (registry C1_PLACEMENTS, spikes/C1/layout.py): north side (fronts
  facing south) Kamigata row x 985-1007 (3k end L, 2k middle, 3k middle, 3k corner R) and Edo row x 1043-1063 (2k end,
  3k middle board roof, 2k middle, 3k corner); south side (facing north) post-town detached x 986-992, post-town row
  middle + end x 994-1007, inn (tile) x 1008-1019, grand inn x 1021-1032. World + mission rebuilt, verify_oprw PASS
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

## Build notes (G1 A1 ruling 3: storeys as historically accurate, with a source)
- Ordinary hatago and every townhouse / post-town house: one storey + the sealed low zushi-nikai (G0-4, G1-5).
- Grand inn (Land_JP_Hatago_Grand, one per tier-3 town, G0-5): a full upper storey with guest rooms. Sources:
  research/buildings/B_TRADE_INDUSTRY.md section 8 (post-town inn: "two storeys, lattice front, rooms upstairs",
  source KA); the surviving Ohashiya hatago at Akasaka-juku on the Tokaido (Toyokawa), whose main house is
  traditionally dated 1716 and has its guest rooms upstairs (cited from memory, no web lookup in this run: verify
  before quoting). Hiroshige (1830s) is not used as dating evidence (PLAYBOOK section 1).
- Detached post-town houses use the 'townhouse' face budget (same template and per-ken detail as the units);
  5-ken inns and the grand inn are 'large' (townhouse.budget_class).
- Upper-storey gable windows of the grand inn are worked from inside only (C10 reach_sides 'far'): nobody stands
  outside at 3.9 m except on a roof.

## In-game checks for the next bundled walk (C3 owns the walk)
- Walk the test street (north of the machiya, z 1080): seams from the street (udatsu, pent ends, seam caps) and
  from the back yards; no light through party walls from inside an end/middle unit.
- Grand inn: climb the stair from the oku (back room), walk both upstairs rooms, open the street and gable windows;
  infected need a navmesh regeneration first (NAVMESH_STEPS.md).
- Post-town house with stable: walk into the umaya from the kitchen doma, then out the back door.
- Loot spawns on the floors of a townhouse unit, the inn and the post-town house.

## Not done / open
- No furniture or dressing (C3). No navmesh (GUI step). 4-ken Kamigata end/corner units remain 'large' (Stephen).
- Aerial render framing is loose (the rows read small); the street-level sheets show the seams.
