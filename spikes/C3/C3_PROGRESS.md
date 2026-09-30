# C3 progress: Phase C wave 1, kura + furnishing + dressing + the walk (agent C3, 2026-09-30)

Brief: the kura (DW22) shells; one or two furnished variants per wave-1 type (the machiya-shop pattern); swap them
into the C1 street and the C2 hamlet and dress both; re-run every check; render sheets; ONE bundled walk in
TEST_CHECKLIST.md. Time log: `japan_dev/TIMELOG_C3.md` (logger `python spikes/C3/tlog.py "<event>" "<name>" "<tag>"
<5h> <wk>`).

## Done
- [x] Kura: `parts/kit/jpparts/templates/kura.py` + `buildings/kurakit.py` + family `buildings/kura` (registry
  C3_KURA): Land_JP_Kura_Namako, Land_JP_Kura_Kuro_Hinged (hinged plaster leaves = the rotation-door engine test),
  Land_JP_Kura_Plain. 3 x 2 ken, okabe with shikkui_int inside, cut-block footing, plastered eave + soffit, two floors
  by jp_p_stair _open. 115 checks, 0 failures. Sheet research/production/contact_sheets/c3_kura.jpg. Commit 61e5b49.
- [x] Furnished variants: `buildings/furnishkit.py` (any registry shell + fittings + decorator; module IS
  buildings/furnished/furnished_shells.py), `buildings/furnish_sets.py` (13 dressings), kit
  `parts/kit/jpparts/fittings.py` (jp_p_fit_kamado promoted from the machiya), registry C3_FURNISHED (14) + C3_SWAP
  (the furnished variant takes the base's island spot) + C3_FURN_PLACEMENTS (the two kura). shellcheck runs the
  decorator checks (D1-D16) on a furnished variant (proxy triangles stripped for the shell checks).
  14 variants, 1,341 checks, 0 failures (`python spikes/C3/summary.py`).

## Next
- [ ] Island: `python spikes/C3/dress_island.py` (free street + hamlet objects -> test/placements/C3.csv), full
  pipeline + pack, T's build_world / build_mission / verify_oprw.
- [ ] Re-runs (machiya 78, shop 137, toilet 19, combos 60, C1 81, C2 21), sheets (street, hamlet), checklist.

## How to resume
- One variant: `python buildings/pipeline.py f_<key> --no-pack` (checks in data/C/_build/verify_logs or stdout)
- All C3: `python buildings/pipeline.py <C3_KURA + C3_FURNISHED keys> --jobs 7` (see summary.py for the list)
- Inspect a shell for dressing: `python spikes/C3/inspect_shell.py <key>` (rooms, door openings, fittings, stairs)
- Renders: `python spikes/C3/render_c3.py kura|rooms|plans|street|hamlet --jobs 8` (jobs in spikes/C3/c3_jobs.py)
