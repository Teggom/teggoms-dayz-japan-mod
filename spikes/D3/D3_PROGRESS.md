# D3 progress: wave 3a dwellings + honjin (agent D3, 2026-10-01)

Time log `japan_dev/TIMELOG_D3.md` (logger `python spikes/D3/tlog.py "<EVENT>" "5h x% wk y%"`). Research notes:
`spikes/D3/D3_NOTES.md`. Stop rule: Stephen stops agent work at 90 % weekly usage.

## Status
- [x] notes  - [ ] shells  - [ ] furnished  - [ ] wait for K3 (`| END |` in TIMELOG_K3.md)  - [ ] compounds + placement
- [ ] world + mission  - [ ] checks  - [ ] sheets  - [ ] checklist  - [ ] pushed

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
