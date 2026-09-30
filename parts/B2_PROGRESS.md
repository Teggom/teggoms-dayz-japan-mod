# B2 progress (missing parts, wave 1; agent B2, 2026-09-29)

Task: PRODUCTION_PLAN Phase B item B2 = PARTS_GAP_AUDIT §5 parts 1-7 (+ optional floor pit / sunoko).

## Status
- [x] 1 jp_p_frame_koyagumi: parts/kit/jpparts/koyagumi.py, 7 variants (_wagoya, _wagoya_log, _wagoya_hip, _sasu,
  _sasu_sooted, _sasu_geya, _sasu_geya_sooted), 0 check failures. Wear: _w0/_w1/_w2 per instance + sooted
  (soot=True, and koyagumi.soot_roof(roof_part) for the roof's inside faces). Offline proof: parts/kit/b2_assembly.py
  (koya_farmhouse = thatch over koyagumi on posts with joya/geya, koya_farm_soot, koya_hut, koya_workshop, koya_hip):
  all checks pass, all binarize to ODOL. Sheets: parts/contact_sheets/9_koyagumi.jpg, 9a_koyagumi_assembly.jpg.
  Kit change: roofs.rafters gained d_start / tag (defaults unchanged; machiya MLOD byte-identical, all 138 old parts
  unchanged).
- [ ] 2 jp_p_wall_party, 3 jp_p_roof_party_end, 4 jp_p_roof_corner, seam_cap -> townhouse hooks filled
- [ ] 5 jp_p_frame_stall
- [ ] 6 jp_p_stair
- [ ] 7 jp_p_open_halfdoor
- [ ] 8 (optional) jp_p_floor_pit + jp_p_floor_sunoko

## How to use koyagumi in a building (Phase C)
    sls, info = roofs.roof(rp, W, D, form, fam, eave_y=ey)          # rp = the roof sub-Part
    K = koyagumi.koyagumi(rp, W, D, info, eave_y=ey, members="log", geya=(KEN, KEN), floor_y=0.05, soot=False)
    H.merge(rp)                                                      # ONE sub-part: rafters live in the roof body
K["posts"] = the joya posts it placed (add them to the C3 post list); K["frame_lines"] = x of the tie beams (the
building needs wall posts there). Gable / hip-end walls keep their own tie beams (walls.gable).

## How to resume
- Parts: `python parts/kit/build_parts.py --only <substr>` writes p3d + sidecar + checks + manifest entries.
- Sheets: `python parts/kit/render_sheets.py <sheet>`; assemblies `python parts/kit/b2_assembly.py` then
  `python parts/kit/render_b2.py <sheet>`.
- Machiya proof: `python buildings/pipeline.py machiya_t3_01` (78/78, outputs unchanged vs git).
- Townhouse: `python buildings/pipeline.py townhouse_unit_test`.

## Commits
- koyagumi checkpoint: (this commit)
