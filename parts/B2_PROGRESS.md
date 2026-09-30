# B2 progress (missing parts, wave 1; agent B2, 2026-09-29/30)

Task: PRODUCTION_PLAN Phase B item B2 = PARTS_GAP_AUDIT §5 parts 1-7 (+ optional floor pit / sunoko).

## Status: ALL DONE (1-8)
- [x] 1 jp_p_frame_koyagumi (jpparts/koyagumi.py): 7 variants (_wagoya, _wagoya_log, _wagoya_hip, _sasu, _sasu_sooted,
  _sasu_geya, _sasu_geya_sooted). Wear: _w0/_w1/_w2 per instance + sooted (soot=True, and koyagumi.soot_roof(roof)).
  Offline proof: parts/kit/b2_assembly.py koya_farmhouse (thatch over koyagumi on posts, joya 3 ken + geya 1 ken each
  side under one slope), koya_farm_soot, koya_hut, koya_workshop, koya_hip: all checks pass, all binarize to ODOL.
- [x] 2-4 + seam cap (jpparts/party.py): jp_p_wall_party (_omoya, _geya), jp_p_roof_party_end (_kawara, _board),
  jp_p_roof_corner (_tile, _board, _skirt), jp_p_roof_seam_cap (_kawara, _board). townhouse.HOOKS now point at them
  (no placeholders). Kit support: roofs.roof(plain_ends=...), leanto.roof per-end keta_ext + plain-end flashing,
  roofparts.pent(flush=, node0=), kawara.ridge per-end end tiles (all defaults unchanged).
  Template fixes (B2): keta / pent purlins / brackets / flashing stop inside the lot line (they overlapped the
  neighbour's coplanar); an udatsu owner's pent stops at its udatsu; seam cap in both regions (owner only).
  Proof: buildings/townhouse_unit_test/combos.py -> combos.json: 60/60 build, closed convex, C12 clean, no
  placeholders; 8 over the townhouse budget (all Kamigata 4-ken end / corner; worst 4-ken corner 10,468 / 3,687 /
  1,342; B0's placeholder version was 10,239 / 3,644 / 1,359). Test unit through the pipeline: 41/41
  (7,912 / 2,765 / 953). Full pipeline checks also run on a Kamigata 4-ken corner (only C5 budget fails), Edo 3-ken
  middle itabuki, Edo 2-ken corner, Edo 4-ken corner kakigara (all pass).
- [x] 5 jp_p_frame_stall (jpparts/stall.py): _ox, _ox_closed, _umaya (sooted), _row2.
- [x] 6 jp_p_stair (jpparts/stair.py): _box (kaidan-dansu look), _open (kura), _well (floor hole + rim + guard rail
  via floors holes 'stair' + stair.well_fn). Assemblies stair_hatago, stair_kura: ramp <= 38, width, head room 2.05,
  ramp meets both floors, well cut.
- [x] 7 jp_p_open_halfdoor (jpparts/halfdoor.py): _hinged (rotation, swings out 90, engine-untested), _open (static).
  Assembly toilet (1 x 1.5 ken walk-in, G1 A1-1): 17/17 incl. C10 both sides, C11, C17, D1 1.04 m with leaf open.
- [x] 8 jp_p_floor_pit (_irori, _irori_doma, _slot) + jp_p_floor_sunoko (_take, _slat) (jpparts/pits.py).

## Also changed (found by B2's wider testing; machiya MLOD stays byte-identical)
- buildcheck: C13 / C16 pass on buildings with no kawara (board / thatch roofs); C11 portal of a half door = its
  whole doorway.
- roofs.cover_boards eave stack, roofs.hafu / leanto board verge battens now in every LOD (C15 failed on every
  board-roofed building): the board roof part samples gained those R3 pieces.
- walls.gable: collar top and vent kept 2 cm under the roof line (T8; the _board vent poked through its roof, the
  kura vent too): jp_p_wall_gable_board / _kura / _thatch samples changed.

## Open / for the lead
- walls.gable _tile and _kura leave 0.12 m slits at the interior post lines (no gable posts drawn for them): see-
  through into the loft / kura attic. Not touched (it would change the machiya).
- Rotation doors (half door) still engine-untested (audit §6 risk 4).
- Engawa / amado-track corner and the kura-eave corner of jp_p_roof_corner not built (pent corners only).

## How to resume / rerun
- Parts: `python parts/kit/build_parts.py [--only substr]`; sheets `python parts/kit/render_sheets.py 9_koyagumi
  9b_townhouse_parts 9c_stall_stair_door`; assemblies `python parts/kit/b2_assembly.py` then
  `python parts/kit/render_b2.py 9a_koyagumi_assembly` / `9d_stair_toilet_stall`.
- Townhouse: `python buildings/townhouse_unit_test/combos.py`, `python buildings/pipeline.py townhouse_unit_test`,
  `python buildings/townhouse_unit_test/render_unit.py`.
- Machiya proof: `python buildings/pipeline.py machiya_t3_01` (78/78, outputs unchanged vs git).

## Commits
- c2f1bb6 koyagumi checkpoint
- parts 2-8: (this commit; one checkpoint, the shared registry / manifest / sheet files made a split commit inconsistent)
