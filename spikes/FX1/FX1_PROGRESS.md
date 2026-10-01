# FX1 progress: wave-2 geometry + placement fixes from Stephen's walk (agent FX1, 2026-10-01)

Brief: fixes 1-6 from test/feedback/2026-10-01_wave2/NOTES.md (door handles, offering box, hanging things, U1 veranda,
rope torii head room, woodpile support). Time log `japan_dev/TIMELOG_FX1.md` (logger
`python spikes/FX1/tlog.py "<event>" FX1 "<tag>" <5h> <wk>`).

## Status
- [x] 1 handles  - [x] 2 offering box + litter  - [x] 3 hanging things  - [x] 4 en ends  - [x] 5 torii head room
- [x] 6 woodpile support  - [x] props rebuilt + jp_site / jp_furniture repacked (noise restored; pbocheck 522 / 312 = src)
- [x] checkpoint cce4930 pushed  - [x] buildings pipeline (full, --jobs 4; 33 changed ODOLs kept, 160 byte-noise restored,
  jp_buildings repacked = src)  - [x] layout_w2f (6 boxes moved / added as site objects) + map_md + world (4134 objects)
  + mission + verify_oprw PASS 4125/4125
- [x] checks: verify_all --full 193 / 11,822 checks / 0 failures; bindcheck 193/193; hangcheck 0; handlecheck 0/40;
  ropeclear 0 LOW; toriipost 0  - [x] sheet fx1_fixes.jpg  - [x] TEST_CHECKLIST 'FX1 re-check'  - [ ] pushed

Pipeline note: the first full run failed 2 checks (temple_do_2_board + its furnished variant: no loot point left on the
en once the koran returns came in, en rect inset 0.27); inset 0.20 -> all pass.
W2F binarize note: build_w2f.py's folder binarize crashed (access violation) on an EXISTING ODOL in civicfit / sacred
(jp_f_anvil_l, after bonsho_l); the six changed masters binarized fine alone (temp folder, removed) and were copied in;
every W2F p3d in src is ODOL, pbocheck 522 = src. Worth a look by whoever next runs build_w2f.py --pack.

## Tools (spikes/FX1)
- `handlecheck.py [--head]`: every fitting of a hinged double door (tobira variants + kido / temple-gate leaves) lies on
  its own leaf, touches it, moves with it; pulls in the free half, straps at the hinge. HEAD 24/30 fail -> 0/40.
- `hangcheck.py [mlod ...]`: every hung prop (mount beam) in the wave-2 furnished MLODs meets a building face within
  3 cm straight above each attachment point. HEAD: 16 failing.
- `ropeclear.py [--models|--placed]`: clear height under the nuki and under the lowest rope / shide / tassel tip, per
  rope torii model and per placed walk-through torii (walking surface = terrain or step Roadway, FB1 toriiclear).
- `toriipost.py`: placed torii feet after the rescale vs other objects (0 within 0.9 m) and the ground.
- `litter_audit.py [--all] [--sites] [--near]`: which placed models carry litter faces; --near flags litter ON a model
  with no tree within 10 m and no ground litter within 8 m.
- `probe_front.py`, `probe_geo.py`, `try_furn.py <key>` (sites, hung props and the member each hangs from, in memory),
  `try_hondo_variants.py` (face counts: mawari-en vs returns).
- Renders: `render_fx1.py [shot ...]` (FX1_TAG=after; before = the same script run from a `git archive HEAD` copy in the
  scratchpad with FX1_TAG=before FX1_OUT=<this renders dir>), jobs `fx1_jobs.py`, sheet `sheet_fx1.py` ->
  research/production/contact_sheets/fx1_fixes.jpg.

## Findings / causes / changes
1. **Door pulls**: tobira.py put each leaf's ring pull at `free - side * 0.12`, i.e. 0.12 m PAST its own free edge, on
   the other leaf, while keeping it in its own bone: closed it sat on the wrong leaf, opening it swung with its own leaf
   through the air (Stephen's P1 + t1). Fix: pull inboard of the free edge on BOTH faces; lattice leaves get a small
   pull board (hikite-ita) beside the stile so the pull is not over a gap; board pulls under the middle batten,
   sankarado pulls on the middle rail; no strap fittings on the sankarado (they floated 12 mm off the recessed panels).
   gates.py (kido + temple gates): the right leaf's hinge straps sat at its free edge (`astragal` 0 chose the wrong
   end): hinge side passed explicitly. Kura plaster leaves: no handles, hinge pins on the axis (fine).
2. **Offering box**: `saisen_bako` carried a LITTER stain on its top (all three sizes); W2F placed it 0.5 m in front of
   the 1.10 m kizahashi foot, centred, 1.5 m wide (P1: on the terrace top between the terrace flight and the hall stair).
   Fix: no litter; `w2f_sets.box_beside_stair()` puts every box (P1, V1, U1, U5 and the two en boxes of T1 / T5, which
   stood across the doors) on the ground at the stair foot, BESIDE the stair, its inner end 0.12 m clear of the stringer,
   the kohai post and its stone: the stair mouth and a 1.1 m+ straight path stay clear. Litter audit: the terraces (P1t,
   P2t: leaf drifts on top) and the swordsmith's indoor quench trough also had litter with no source; removed.
   Containers that collect leaves (stone basins, troughs, well curbs) keep their fill. Earlier-wave placements with litter
   ON them and no source near (litter_audit --near): C oke_tarai (1053.9, 1092.6), C3 kakei_trough (953.2, 1036),
   well_hanetsurube (955, 1001), stable tie post + trough (931, 1020), SH1 chozubachi_large (1019, 1140.5): left (all
   containers or earlier waves walked OK), listed for Stephen.
3. **Hung things**: W2S fitting heights were guesses; nothing checked a member above. 16 failing in wave 2 (hangcheck):
   the U1 gong had 1.56 m of air above it, the P1 suzu 1.08 m, the T3 striker log's ropes ended under the roof (the log
   ran across the bell beam), the U3 log's outer rope ran past the beam's end, kuri gyoban / umpan / jizai-kagi /
   hoshigaki, the swordsmith shimenawa, the hondo tengai. Fix: `w2f_sets.hang_real()` hangs a prop only where EVERY
   attachment point meets one structural member (beam, tie, purlin, rafter, ceiling; never roof sheathing) within 3 cm,
   searching round the spot; for the suzu / waniguchi over an en it adds the period hanging bar (kake-gi) between the
   kohai tie beams (tsunagi), or across the rafters on the low village halls with no tie beams, kept >= 2.10 m over the
   en. bonsho: the log runs UNDER the bell beam (yaw 90 in both towers), 1.0 m long, both ropes straight up to the beam
   with an iron eye.
4. **U1 'sides cut off'**: the town hondo's en was front-only (its docstring said three sides): deck and koran stopped
   in the air at the hall corners. Same on 5 other halls (village haiden, village hondo, do 2/3, do town, shinmei honden).
   Choice: koran returns (the rail turns the corner and runs back to the wall, crossed corner on plain koran, corner post
   on giboshi) on all six. A mawari-en (three sides, even one bay deep to a wakishoji: `koran.en_wrap(side_len=)`) is the
   fuller period form but takes the town hondo to R1 12,428 / R3 1,638 > the large budget (12,000 / 1,600); returns
   keep it at 11,586 / 1,590.
5. **Rope torii**: the rope hung 5-7 cm UNDER the nuki with a 10 cm / 1.82 m sag and shide below: the lowest shide tip
   was 1.42-2.08 m over the walking surface (14 placed rope torii LOW). Fix: rope across the FRONT of the nuki (0.35 of
   its height up), half the sag, and the torii scaled uniformly (proportions kept) by k: wooden shinmei 1.35 (1.82 x
   2.73 -> 2.46 x 3.69), myojin 1.17 (2.73 x 3.45 -> 3.19 x 4.04), stone s 1.52 (-> 2.77 x 4.12), m 1.45 (-> 3.63 x
   4.06), stone l unchanged (3.60 x 4.20), mini unchanged (yard shrine). Below-ground parts keep their burial depth.
6. **Woodpiles**: `woodpile.end_stakes()`: two stakes per free end (front + back corner), upright against the end
   billets, tops 8 cm over the pile, tied across the end with a straw rope, INSIDE the old footprint (pile shortened):
   B3b wall h120 / h180 / half / ab_collapsed (its right-hand stakes lean out 18 deg: why it fell) / free_posts (was one
   post per end), B3a jp_f_firewood_stack + _low. Footprints and the 5 cm wall gap unchanged.

## Numbers
- Torii clear under the lowest rope / shide tip, placed (before -> after, spikes/FX1/ropeclear.py --placed): SH1 approach
  stone l rope shide 2.41 -> 2.64, myojin moss rope shide 2.01 -> 2.57; x 1036 row shinmei rope 1.67 -> 2.46, shinmei
  rope shide 1.59 -> 2.37, stone s rope 1.47 -> 2.49, stone s rope shide 1.42 -> 2.43, shinmei moss rope 1.68 -> 2.46,
  shinmei moss rope shide 1.58 -> 2.36, stone s moss rope shide 1.36 -> 2.35; hill stair stone l rope shide 2.22 ->
  2.46, myojin rope 1.89 -> 2.47, myojin rope shide 1.81 -> 2.38, myojin moss rope 1.79 -> 2.36; Inari myojin shu rope
  shide 1.87 -> 2.43; W2F V3 village shinmei rope shide 1.67 -> 2.46. LOW (< 2.30): 14 -> 0. Under the nuki: 1.75-2.94
  -> 2.49-2.94 (the 2.49 is the unchanged stone l at the hill-stair head).

## Decisions
- Box beside the stair rather than centred further out (P1's terrace leaves 1.3 m in front of the kohai posts).
- Koran returns, not mawari-en (budget); recorded above.
- Torii: uniform scale (period proportions) rather than taller-only; the stone m now nearly matches l's span (squatter,
  thicker posts); not placed anywhere.
- Litter: only the draped / sourceless litter on wave-2 props removed; containers keep their leaf fill.
