# D3 progress: wave 3a dwellings + honjin (agent D3, 2026-10-01)

Time log `japan_dev/TIMELOG_D3.md` (logger `python spikes/D3/tlog.py "<EVENT>" "5h x% wk y%"`). Research notes:
`spikes/D3/D3_NOTES.md`. Stop rule: Stephen stops agent work at 90 % weekly usage.

## Status
- [x] notes  - [x] shells (28)  - [x] furnished (16)  - [x] wait for K3  - [x] compounds (6) + corridors (2) + placement
- [x] world + mission (verify_oprw PASS)  - [x] checks  - [x] sheets (d3_family, d3_rooms, d3_map)  - [x] checklist
- [ ] pushed (commit 3 = site objects + placement + sheets + checklist)

## Code
- Template `parts/kit/jpparts/templates/dwelling.py` (rural.Shell + civic / sacred helpers; new helpers ceiling,
  interior_gable, tokonoma, genkan_porch, shikidai_edge, hidana, plaster_exterior, jodan, nijiriguchi).
- Recipe `buildings/dwellingkit.py`; family folders buildings/dw_rural | dw_samurai | dw_upper | dw_out | dw_honjin
  (module dwelling_shells.py); registry block D3_SHELLS (before the FB1 binding-names loop).
- Tools: `spikes/D3/try_dw.py <kind> '<json>' ...` (faces / budget), `spikes/D3/render_d3.py try --kind "a;b"
  --params '{..};{..}' --view 3q,back --name x` (renders in spikes/D3/renders, <= 4 Blender processes).

## How to resume
- One shell: `cd buildings && python pipeline.py <key> --no-pack`; checks only `--verify-only`.
- Logs: data/C/_build/verify_logs/verify_*.log (grep FAIL).
- Placement: `python spikes/D3/layout_d3.py` (CSV + CE + d3_items.json), `python spikes/D3/map_d3.py` (map + SHOWCASE),
  then build_world.py, build_mission.py, tools/verify_oprw.py.
- Sheets: `python spikes/D3/render_d3.py --jobs 4` (d3_family.jpg), `python spikes/D3/render_d3_rooms.py rooms --jobs 4`
  (d3_rooms.jpg, jobs in d3_jobs.py).
- Not done: kairo at shrine P (no level run between the terraced halls); DW13 skipped, DW20 waits (brief).
