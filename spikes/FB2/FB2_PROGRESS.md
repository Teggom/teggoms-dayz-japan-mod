# FB2 progress: building fixes from Stephen's re-check (agent FB2, 2026-10-01)

Brief: 1 z-fighting (check + kit fix), 2 Kinai takahe gable (research verdict + rebuild), 3 partitions that stop
short (top beam on posts), 4 two-storey divider + wall gaps, 5 after FP2's END: world + mission, checks, short
TEST_CHECKLIST. Time log `japan_dev/TIMELOG_FB2.md` (logger `python spikes/FB2/log.py "<event>" "<name>" "<tag>"
<5h> <wk>`). FP2 (props + materials) runs at the same time; its log is TIMELOG_FP2.md.

Screenshots (test/feedback/2026-10-01_recheck/) read as:
- 2_zfight_wall_stair: the KURA (open stair, grey shikkui_int wall): the stairwell rim beam (well_rim) lies in the
  plane of the back okabe's inner face, same normal, 0.45 m2 (census: kura okabe | well_rim). In perspective the
  horizontal rim reads diagonal.
- mochi building = s1_th_kamigata_3k_endr_mochiya (demo shop D-row): dodai top flush with the doma top (y 0.05),
  doma | threshold, dodai | threshold.
- doorway bottoms: tatami / floor_board / floor_lod | track, dodai | threshold (every family).

## Status: DONE (built, packed, island rebuilt; untested in game)
- [x] 1 z-fighting: C20 + zfight.resolve; 102,726 visible same-facing pairs before -> 0 in all 128 buildings
- [x] 2 takahe: verdict below; rebuilt as the plastered gable wall
- [x] 3 partitions: C21; every partition ends at a beam / closes up (0 open wall tops)
- [x] 4 grand inn divider closed to the roof + missing posts (C22: 0 free wall ends)
- [x] 5 after FP2's END (11:54): full pipeline (128 built, binarized, jp_buildings.pbo 78.4 MB, 128/128 pass, 8,574
  checks, bindcheck 128/128), combos 60/60, build_world (4,090 objects, placecheck verdicts identical to FB1's),
  build_mission (128 CE groups, the 30 placed groups snap exactly), verify_oprw PASS 4081/4081, TEST_CHECKLIST.md
  (~10 min). leancheck: the remaining gaps are the gallery wall-hung items (FB1's open note) and site props against
  exterior walls whose Geometry FB2 did not change (the resolver keeps collision as built).

## Checks added (all in jpparts/buildcheck.run_g3, so every building runs them)
- C20 no z-fighting (zfight.py), C21 partitions end at a beam or a ceiling (parttop.top_ends), C22 interior wall ends
  meet a post or a wall (parttop.free_ends). C15 now ignores sub-1 cm slivers (5 jittered rays per column).
- Machiya 78 -> 81 checks, furnished machiya 137 -> 140, all pass.

## 1. Z-fighting
- `parts/kit/jpparts/zfight.py`: `coplanar(M)` finds face pairs of DIFFERENT solids in Resolution 1-3 that lie in one
  plane (<= 1 mm, normals within 0.5 deg) and overlap (convex clip, >= 1 cm2). Classes:
  - same: same-facing, visibly different (material or uv mapping differ), and not covered by a third solid (a point
    4 mm in front of the overlap is not inside another closed solid; downward faces at grade skipped) -> FAILS C20
  - opposite: touching faces (point at each other): backface culling draws only one of them from any eye point ->
    reported, not failed (the kura stringer touches its wall this way: not the flicker)
  - hidden: same-facing but drawn identically (same material + same uv) or covered by another solid
- `zfight.resolve(M)` (called by `buildings/pipeline.build_model` before the LODs are written): per plane, the
  overlapping solids are coloured greedily from the biggest down (door leaves first, never moved); colour c stands
  c x 5 mm proud (12 mm for Resolution 2/3-only solids); an upward face steps DOWN instead (sills / tracks sink into
  the floor; tie beams don't rise into the roof, C12); a Geometry / View / Fire solid is split first so collision
  stays exactly as built (door sweeps, head room, Roadway checks unchanged). Repeats until no visible pair is left.
- C20 in `jpparts/buildcheck.run_g3` (every building: shellcheck, the machiya's verify, generic).
- Census tool: `python spikes/FB2/zcensus.py --jobs 10 --out <name>` (builds every shipped model in memory, no
  resolve) -> data/FB2/zcensus_<name>.json (big; per-building summary of the BEFORE run: spikes/FB2/zcensus_before_summary.json). `spikes/FB2/try_resolve.py <key...>`, `probe.py`, `dbg_pair.py`.
- BEFORE (visible same-facing pairs / touching pairs / hidden): farmhouse 4,223 / 30,678 / 2,100; furnished 14,655 /
  48,117 / 7,738; hatago 5,264; hut 1,977; kura 405; machiya 1,068; machiya shop 1,068; posttown 8,665; shed 1,186;
  toilet 265; townhouse 63,950. Total 102,726 visible same-facing pairs.
- AFTER (full pipeline, resolve on): 0 visible same-facing pairs in every building (C20 passes 128/128). The touching
  (opposite-facing) and covered pairs are left as they are (not visible).
- Machiya and furnished machiya MLODs change by these few-mm moves + the mid-partition loft beam.

## 2. The Kinai takahe gable (A_kinai_gable_white_band) - verdict for Stephen's "is that how it looked?"
**Verdict: no, not as built.** A real yamato-mune (takahe-zukuri) gable has no white band laid along the roof edge of
an earth gable. The takahe IS the gable wall: the plastered gable is carried up past the steep thatch, so from the
gable end you see one plastered gable face (frame lines showing) whose top edge stands a little above the thatch, with
a narrow tile cap; from the side you see the thatch framed by two thin white parapet edges with their tile copings.
The old model laid a 0.30 m thick white slab, centred on the gable line (so 0.15 m proud of the wall), that reached
0.45 m down onto an ochre earth gable and widened to ~0.65 m over the thatch at the apex (to clear a 0.55 m bamboo
ridge bundle): a separate massive white chevron on a brown gable.

Basis:
- Project research: PARTS_GAP_AUDIT #53 ("tile-capped plastered parapets flanking a steep thatch gable, over tiled
  lower roofs"); BUILDING_LIST / A_DWELLINGS Kinai headman house ("thatch main roof with tiled lower roofs, white
  plaster"; Yoshimura house, Habikino, early Edo = in the 1730 window); KEEP_DWELLINGS DW07 / DW17. (The "Kai
  takahe-zukuri" in A_DWELLINGS is a different, raised-ridge silk house, late Edo: not this.)
- Local reference images: none of a yamato-mune on this machine (searched data/playbook/refs, data/research_ext,
  data/research_int: Minka-en, Hida, Morse Kanto thatch only). No web lookups were allowed in this task.
- General knowledge (NOT from a local source; treat as such): Nara-basin / Kawachi farmhouses; steep kirizuma thatch
  (steeper than 45 deg); both gables plastered (usually white shikkui) and raised as takahe a few tens of cm over the
  thatch, top edges straight and parallel to the slope, capped with a few noshi courses and a round cap tile; the
  thatch ends die into the takahe's inner face; a slim ridge between them; tiled lower roofs (the kitchen-end
  ochimune and pents). Wall thickness at the top roughly 0.2-0.3 m.

Rebuilt (templates/rural.py `_takahe`, `kinai(takahe=True)`; constants TAKAHE_T 0.24, TAKAHE_PROUD 0.075,
TAKAHE_RISE 0.26):
- the takahe's outer face 1.5 cm over the gable frame (the plaster skin, not a slab standing 15 cm proud), 0.24 thick
  inwards (the thatch ends die into it);
- its top runs PARALLEL to the slope 0.26 over the thatch (was 0.12 at the eave rising to ~0.65 at the apex), tile cap
  (2 noshi courses + round cap, 0.32 wide) on it;
- inside the wall line it reaches only 0.12 under the roof line (was 0.45);
- the gable face above the tie beam is plastered with it (aged shikkui outside, frame lines kept: panels stay under 1
  ken x 1 storey), so the white reads as the gable wall, not a band;
- the thatch ridge bundle is kept slim (squashed to 0.22 over the thatch apex, 0.04 under the takahe apex);
- material jp_m_wall_shikkui_aged (FB1's aged plaster, as the kura) instead of the bright shikkui.
Renders: spikes/FB2/renders/a_takahe_gable_after.png, a_takahe_side_after.png (before: spikes/FB1/renders/
c_gable_after.png).
Not changed (for the lead / Stephen): the kit thatch pitch stays 45 deg (a real yamato-mune is steeper); no ochimune
(the lower tiled kitchen-end roof with its smoke vent): the Kinai lower roofs remain the long-side pents (C2's design).

## 3. Partitions that stop short (B_partitions_stop_short)
- Check C21 (`jpparts/parttop.py`, in run_g3): from every interior wall panel's top, climb the solids stacked on it;
  it must end against a ceiling / floor / roof / beam within 2.5 cm, or in a beam running >= 0.6 m along it.
  Census before: farmhouse 712 open samples (8 buildings), furnished 304 (15), townhouse 546 (69: the mise / oku
  partition 8 cm under the loft boards), posttown 48, hatago 96, machiya 17. Tool: `spikes/FB2/partcensus.py`.
- Kinai: the x = XM partition stands on a koyagumi frame line under its ushibari: it now closes up INTO the log
  (wall + posts to the log's underside + 0.10; the logs are not flat). The z = ZS partition runs across the ushibari:
  it ends at a head beam (part_head, 0.13 x 0.15, sooted) on its posts, open above (the period sashigamoi form).
- Kanto: both partitions end at a head beam on their posts (the ushibari over x = XR covers only the joya span).
- Huts / sheds / kura: no interior partitions.
- Town (every townhouse unit, post-town house, inn, the machiya, all furnished variants): the mise / oku partition
  stopped at CEIL 3.00 with only joists over it (an 8 cm slit between the rooms): a loft beam (floor_beam section) on
  the partition line now carries the joists and closes it (templates/townhouse.py; buildings/machiya_t3_01).

## 4. The two-storey house (C_two_storey_divider_gaps) = Land_JP_Hatago_Grand_Furnished (f_inn_grand) and the bare
Land_JP_Hatago_Grand (inn_grand): the only full upper storey (kura upper floors are open rooms with no partitions;
townhouse / post-town lofts are sealed, G0-4).
- The upstairs divider stands right under the ridge and stopped at LOFT + 2.35 (1.67 m under the roof boards);
  its two ends met the gable walls with NO post (a 6 cm vertical slit each end, the "vertical gaps"), and its kokabe
  ended against nothing (the "slit at the head rail" in the red circle).
- Now: an end post against each gable wall + the door posts run up to the roof boards; a head beam (part_head) caps
  the room-height wall; a plastered kokabe closes it up to the boards (4 mm into them). Render
  spikes/FB2/renders/c_inn_divider_after.png.

## How to resume
- All checks: `python spikes/FB2/verify_all.py 10` (logs data/C/_build/verify_logs).
