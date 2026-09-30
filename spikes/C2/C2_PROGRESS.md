# C2 progress: Phase C wave 1, rural shells (agent C2, 2026-09-30)

Brief: bare rural shells (no furniture; C3 furnishes): a rural template, DW06 Kanto farmhouse, DW07 Kinai farmhouse
with the ox, DW01 hut east, DW30 hut west, DW24 shed / barn, through buildings/pipeline.py; the grand inn's storey
source check; a hamlet on the test island; render sheets. Time log: `japan_dev/TIMELOG_C2.md` (logger
`python spikes/C2/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).

## Done (all)
- Template `parts/kit/jpparts/templates/rural.py` (kinds kanto / kinai / hut_east / hut_west / shed), recipe
  `buildings/ruralkit.py`, family folders buildings/farmhouse|hut|shed (module `rural_shells`), registry C2_* entries.
- 21 shells, 1,050 checks, 0 failures (buildings/<family>/checks/<key>.json):
  - DW06 (4): Land_JP_Farmhouse_Kanto_Yosemune, _Yosemune_Umaya, _Yosemune_Umaya_DomaR, _Irimoya_DomaR
  - DW07 (4): Land_JP_Farmhouse_Kinai_Kirizuma_Tile_Takahe, _Kirizuma_Board, _Irimoya_Tile, _Irimoya_Board
  - DW01 (4): Land_JP_Hut_East_S_Earth_Mushiro, _S_Sunoko, _L_Board, _L_Earth
  - DW30 (5): Land_JP_Hut_West_Thatch_LeanL, _Ishioki_LeanR, _Itabuki, _Ishioki, _Thatch
  - DW24 (4): Land_JP_Shed_Open_Board, _Open_Thatch, _Walled_Ishioki_Woodshed, Land_JP_Barn_Walled_Thatch
  - budgets: farmhouses 'large' (worst Kinai irimoya tile 11,422 / 4,268 / 1,494), huts + sheds 'standard' (worst
    Hut_West_Ishioki_LeanR 5,371 / 1,425 / 509)
- Grand inn storey source: checked; verdict in spikes/C1/C1_PROGRESS.md build notes (Ohashiya is officially after
  1809, not 1716; the 1730 full upper storey is unproven; model unchanged, Stephen decides).
- Hamlet (registry C2_PLACEMENTS, spikes/C2/layout.py): west yard x 930-970, z 999-1048. World + mission rebuilt,
  verify_oprw PASS 3585/3585; placecheck failures back to the pre-existing 35.
- Re-runs after the shared-code changes: machiya 78/78, shop 137/137, toilet 19/19, combos 60/60, C1's 81 shells
  all pass (tracked check files byte-identical).
- Sheets: research/production/contact_sheets/c2_family.jpg, c2_hamlet.jpg, c2_interior.jpg.

## Shared-code changes (defaults unchanged)
- buildcheck.run_g3: `extra_portals` (a mushiro doorway, smoke gables, gable vents) + floors with `enclosed=False`
  (open sheds, lean-tos) skip C11.
- shellcheck: passes the module's PORTALS, counts soseki for C8, PASSAGE_LABEL hook, swatch wall + (C2 only) the C1
  street reserved.
- pipeline: sequential verify rebuilds a family member before its checks (module state was the last model's).

## Decisions / for Stephen
- Farmhouse keta 3.30 (Kanto) / 4.30 (Kinai) and huts 3.10: the thatch soffit stays >= 2.20 all round. PLAYBOOK
  G1-6 asks for a board pent over entrance sides INSTEAD of raising walls; a pent cannot sit under a full 45-deg
  thatch eave at the kit's 2.88 keta (they intersect). Kanto: no skirt pent (walls raised 0.42); Kinai: its lower
  roofs ARE pents (tile / board, 1.2 m) under a short thatch eave. Playbook conflict: Stephen to confirm.
- Kinai kabata washing pit not built (needs running water: a new pit kind + material).
- Kanto kabuto form skipped (the full kabuto silk house is later than 1730, KEEP_DWELLINGS cut list).
- Thatch roofs keep every other bamboo rafter (0.61 m) for the face budget; ishioki roofs keep every third field
  stone in Resolution 1 and a flat stone layer in Resolution 2/3 (C15).
- Small rooms (dei / nando) are open above their partitions (3.05 m) to the sooted roof; no ceilings (C3 / PA2).
- The big single-leaf itado (jp_p_open_itado _plain / _battened) got a DoorsTwin adapter (rural.big_leaf) with end
  stiles + a far-jamb filler (C17). Engine-untested like every door type new to the game.

## In-game checks for the next bundled walk (C3 owns the walk)
- Hamlet west of the yard: walk under every thatch eave (no head bump), in through the big plank doors, up the
  kutsunugi step onto the hiroma / daidokoro, look up at the sooted roof; the ox stall and the umaya.
- Mushiro hut: walk in through the open straw-mat doorway. Lean-tos and open sheds: loot on the floors.
- No navmesh yet (GUI step).

## How to resume
- One shell: `python buildings/pipeline.py <key>`; checks only: `python buildings/pipeline.py --verify-only <key>`
- A family: `python buildings/pipeline.py <keys...> --jobs 8`
- Quick look without the pipeline: `python spikes/C2/try_rural.py kanto '{"stable": true}'` (faces, budget)
- Debug: `python spikes/C2/dbg.py <key> leak|c15|c17 <door#>|c12`; sheets `python spikes/C2/render_c2.py --jobs 8`
- Hamlet: `python spikes/C2/layout.py`, then the registry block, `pipeline.py --combine-only`, T's build_world /
  build_mission / verify_oprw.
