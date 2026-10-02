# FX6 progress: fixes from Stephen's 3c-1 walk + the small-gate family (agent FX6, 2026-10-02)

Time log `japan_dev/TIMELOG_FX6.md` (logger `python spikes/FX6/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Research, sizes, era tests, the gate-picker rule and the root causes: `spikes/FX6/FX6_NOTES.md`. Stop rule: weekly 86 %
-> checkpoint; never reached (81 % at start, 82 % at the end).

## Status: DONE (built, packed, world + mission rebuilt; untested in game)
- [x] 1 dyer's cloths (+ every 3c-1 prop resting on a real support)  - [x] 2 small-gate family + picker + 12 compounds
- [x] 3a kura doors folded back (every '_open' kura)   - [x] 3b koji room   - [x] 3c washbasin   - [x] 3d new checks
- [x] island rebuilt   - [x] checks   - [x] sheets   - [x] checklist   - [x] plan / token log

## What changed (files / functions)
- **Props** (`spikes/W3C1/props_w3c1.py`, binarized with `spikes/W3C1/binsingle.py`, jp_furniture repacked):
  monohoshi (lengths drape over the bar; fallen ones lie flat, 4 cm under the surface + folds), dye_rack (brackets
  carry the wringing bar), hangiri scattered (third tub upside down on the floor; its extra collision dropped for the
  kamaba's 25 % coverage), fune_press (a third block under the beam; slings reach the stones and the sling bar),
  shikomi_oke ladder (rails on the rim), shime_press (lever on the block), hoshiita_rack (bar touches the boards),
  kozo_beat (bark strips on the floor), and the unused ab states hatcho_oke_ab / koji_toko_ab / sukibune_ab.
- **Furnishing** (`buildings/w3c1_sets.py`): koji bed against the muro's back wall, shelves on its west (model xmin)
  wall; the staved tub faces the room (its staves went through the o-kura wall); flasks instead of the overhanging
  measure set on the cask rack; nothing on the komo cask's top (its surface sits 3 cm over the recessed lid).
- **Kura doors** (`parts/kit/jpparts/openings.part_kura_door`, '_open'): the plastered leaves lie folded back flat on
  the surround / wall. Rebuilt: Land_JP_Kura_Plain, _Namako, _Namako_Furnished, SakaGura_Okura / _Maegura (+ furnished),
  Kura_Plain_SakeCasks. Kura_Kuro_Hinged unchanged (its plaster leaves ARE working rotation doors, the engine test).
- **Gates** (`parts/kit/jpparts/sitewall.py`): gate_kido_kata, gate_kido_ryo, gate_shiorido, gate_opening,
  gate_post_w, _leaf_door; (`templates/dwelling.py`): pick_gate (the rule), _gate_part (new kinds), _twin_single,
  `_wall_path` gaps carry the gate's post width, compound() merges openings without a door; every compound's gates
  written as `(run, seg, off) + pick_gate(...)` (dwelling COMPOUNDS, trade YARDS, tradesite YARDS).
- **Checks** (new): `spikes/FX6/propfloat.py` (every prop body rests / tips / cloth hangs; whole catalogue),
  `propseat.py` (props in a furnished room seated on a floor / shelf / prop), `roomaccess.py` (0.6 m capsule from
  every door; --all = every furnished variant), `gatecheck.py` (FX1 handle check + D1 on the new gates).
- Docs: parts/K3_NOTES.md §6 (gate API + rule table), SHOWCASE_MAP (gate notes), TEST_CHECKLIST (FX6 re-check).

## Checks at the end
verify_all --full 297 buildings / 19,633 checks / 0 failures; bindcheck 297/297; verify_oprw 4239/4239; placecheck
island 421 failures = the W3B/W3C1 baseline (W3C1's same 6 rows: posts / bales sunk 4-8 cm, hangiri named 'hanging');
hangcheck 0; handlecheck 40/0; gatecheck 8 gates / 0; gradesweep: every compound 0.00 m2 up-facing at grade except
the paper yard's 0.12 (the yotsume culm feet, W3C1 baseline 0.11) and K3's two corridors (FX5 baseline); jointcheck
FX5 --all 56 OK + 4 by design, W3C1 13 OK + 5 by design; propfloat: 3c-1 props 0 failing (catalogue 107 older props
listed in `_propfloat_catalogue.txt`, not fixed); propseat 3c-1 77 props / 0; roomaccess --all 294 buildings: only the
muro failed before the fix (`_roomaccess_all_before.txt`), 0 after.

## Sheets
research/production/contact_sheets/fx6_gates.jpg, fx6_fixes.jpg (`python spikes/FX6/render_fx6.py gates|compounds|kura`
then `sheets`).

## How to resume / re-run
- Props: `cd spikes/W3C1 && python build_w3c1.py <prop> --no-binarize`, `python spikes/W3C1/binsingle.py <p3d...>`,
  `python tools/assemble_config.py jp_furniture --pack`.
- Buildings: `cd buildings && python pipeline.py <keys> --no-pack --jobs 4`, `python -c "import pipeline; pipeline.pack()"`.
- World: `python spikes/T_terrain/build_world.py`, `build_mission.py`, `tools/verify_oprw.py`.
