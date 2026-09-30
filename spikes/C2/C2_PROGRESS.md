# C2 progress: Phase C wave 1, rural shells (agent C2, 2026-09-30)

Brief: bare rural shells (no furniture; C3 furnishes): a rural template, DW06 Kanto farmhouse, DW07 Kinai farmhouse
with the ox, DW01 hut east, DW30 hut west, DW24 shed / barn, through buildings/pipeline.py; the grand inn's storey
source check; a hamlet on the test island; render sheets. Time log: `japan_dev/TIMELOG_C2.md` (logger
`python spikes/C2/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).

## Done
- [x] Template `parts/kit/jpparts/templates/rural.py` (kinds kanto / kinai / hut_east / hut_west / shed), recipe
  `buildings/ruralkit.py`, family folders buildings/farmhouse|hut|shed (module `rural_shells`), registry C2_* entries.
  Shared-code changes (defaults unchanged): buildcheck.run_g3 `extra_portals` + floors `enclosed=False` skip C11;
  shellcheck passes the module's PORTALS, counts soseki for C8, a PASSAGE_LABEL hook, the C1 street reserved for C2;
  pipeline: sequential verify rebuilds a family member before its checks (module state was the last model's).

## Next
- families one by one (pipeline by key), the inn source check, the hamlet (spikes/C2/layout.py), sheets, re-runs.

## How to resume
- One shell: `python buildings/pipeline.py <key>`; checks only: `python buildings/pipeline.py --verify-only <key>`
- A family: `python buildings/pipeline.py <keys...> --jobs 8`
- Quick look without the pipeline: `python spikes/C2/try_rural.py kanto '{"stable": true}'` (faces, budget)
- Debug: `python spikes/C2/dbg.py <key> leak|c15|c17 <door#>|c12`; renders `python spikes/C2/render_c2.py ...`
