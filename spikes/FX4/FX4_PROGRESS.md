# FX4 progress: three fixes from Stephen's walk of FX1-FX3 (agent FX4, 2026-10-01)

Brief: PRODUCTION_PLAN 2026-10-01 'Stephen's walk of FX1-FX3' (bell, fire-watch roof, stone atlas). Time log
`japan_dev/TIMELOG_FX4.md` (logger `python spikes/FX4/tlog.py "<event>" "5h x% wk y%"`).

## Status: DONE (built, packed, checked; untested in game: TEST_CHECKLIST.md 'FX4 re-check')

## 1. Bells and gong seen inside out
- Cause: `fkit.lathe` wants the profile traversed with the material on the LEFT (up the outside). The bonsho body
  (spikes/FX2/detail_fx2.bonsho_body) ran DOWN the outside, so every face pointed into the bell (outside culled,
  you saw its inside), and its "mouth" was a flat disc 6 cm up. Same fault, found by the new scanner: the waniguchi
  gong, the bonsho LOD 2, the hansho alarm bell on the guard-house fire ladder (W2F civic), the fringe collar of
  every FX2 tassel, two bowl / soup lids (L1 meal) and the sedge hat (S1 g2).
- Fix: bonsho = a hollow casting (inside crown -> inner wall facing the cavity -> komaki lip with a flat underside ->
  up the outside); hansho the same; the others reversed (`prof[::-1]`). The shrine suzu is a closed crotal (already
  outward); the fire-watch tower's iron bell is a closed solid (already outward).
- Check: `python spikes/FX4/lathecheck.py` builds all 842 furniture + site props (geometry only) and lists every
  closed lathe profile with a clockwise (inside-out) traversal: 6 call sites -> 0.

## 2. Fire-watch ladder tower head room
- Cause: roof 1.10 m over the 4.90 m deck; the bell hung over the deck at head height.
- Fix (spikes/L2/props_l2_street.fire_watch 'ladder_tower'): roof underside + tie beams at deck + 2.20 m on four
  corner posts (front posts at x +-0.44, outside the ladder's 0.42 m climb), bell outside the back rail hung from
  the roof's back overhang, striker on the back rail. Deck height, ladder rails, ladder1* memory points, View
  'ladder1' component unchanged (DayZ ladders are memory-point driven; the config class has no ladders[]).
  New dim deck_head_room 2.20; height 6.3 -> 7.64.
- Other standing decks: buildings shellcheck C7 'head room >= 2.10 over every floor' passes on all 190 (kura 2.23,
  town shoro 2.20, village shoro 2.72, inns 2.50 incl. upstairs; lowest anywhere 2.12, temple_do_2_board).

## 3. Stone texture variety
- Cause: every stone face mapped world-planar from one small tile (stone_carved_aged 2 m, carved / cut 1 m); faces
  of an octagonal post whose tangents line up sample the same strip, rosettes come back every 1-2 m.
- `research/materials/make_stone_atlas.py` (post step, like make_wood_atlas.py): stone_carved_aged 1024 -> 2048,
  stone_carved + stone_cut 512 -> 1024 = 2 x 2 tiles: the tile + 3 turned / mirrored / rolled variants cut in along
  wobbled lines inside each quadrant (tiles in u and v); normal vectors turned with the content; mean colour fixed
  to the tile (dE 0.02-0.15). Isotropic aged stone: variants any 90 deg; carved / cut (rain streaks, tool marks
  along v): 0 / 180 deg + mirror only. Sidecars: "atlas" {"kind": "stone", "turn": "any"|"small", "px"}.
- Macro Stage3 jp_m_macro_stone_w{0,1,2}_mc (isotropic grime + lichen-grey clouds, ~11 m), via
  make_wood_atlas.macro_for -> make_stone_atlas.macro_for_stone; mean shift dE 0.1-0.4 (cut 1.3-2.4).
- `parts/kit/jpparts/uvwood.py` stone mode: same plane / solid groups, each group also TURNED ("any" 0-360 deg,
  "small" +-8 deg or 180 +-8 deg) + offset anywhere + maybe mirrored. Text / bonji decals are other materials:
  untouched.
- Covers every model on those three materials: both stone torii families (standing + collapsed), stone lanterns,
  graves / steles / Jizo bases, komainu / kitsune plinths, jpparts foundations (dodai stones, kura footing, cut
  steps) -> most buildings. (Field / river stones = core.stone rocks, each its own random shape: not atlased.)

## Rebuild / checks (all after the last change)
- Materials: make_stone_atlas.py (30 PAAs + 3 macro PAAs, 9 stone rvmats with Stage3), jp_common packed.
- Rebuilt: parts (234, 26 stone MLODs changed), buildings pipeline (193, 188 stone ODOLs kept), props B3a / L1 / S1 /
  W2F / B3b / L2 (all suites pass: 113 / 185 / 175 / 49 / 239 / 81), `tools/assemble_config.py --pack` (522 / 320
  classes, unchanged). Byte-noise: `python spikes/FX4/noise.py <old_out> src/JP/site src/JP/furniture
  src/JP/buildings` kept 314 (302 stone + 12 geometry-changed), restored 615 to HEAD; jp_furniture, jp_site and
  jp_buildings repacked from the restored tree. jp_common / jp_buildings / jp_furniture / jp_site packed 22:20-22:33.
- verify_all: cached pass 193 / 193, then `--full` 193 / 11,830 checks / 0 failures (C20 z-fighting included).
- TXT (spikes/L2/textface.py on all six prop out folders): 214 text models, 0 failing.
- uvdiff (spikes/FX4/uvdiff.py = FX3's + stone): B3a 0 / B3b 0 violations (95,900 stone + wood faces remapped, text
  untouched); L1 / S1 / W2F / L2 violations ONLY on the models FX4 changed on purpose (lids, sedge hat, tassel collar
  of suzu, bonsho, waniguchi, ridge-ladder hansho, fire-watch tower: `spikes/FX4/uvdiff_models.py`).
- hangcheck 0 failing (bonsho still on its hook), handlecheck 40 / 0, lathecheck 0 inside out, bindcheck 193 / 193.
- Sheet: research/production/contact_sheets/fx4_fixes.jpg (`render_fx4.py before|after`, `sheet_fx4.py`; the before
  masters are the out/ copies saved in spikes/FX4/before/ before the rebuild).

## Pitfalls
- A maker re-run of stone_cut / stone_carved (build_materials) or stone_carved_aged (make_fp1_materials) writes the
  old tile: run `python research/materials/make_stone_atlas.py` after it + pack jp_common (uvwood refuses a non-atlas
  stone PNG, loudly).
