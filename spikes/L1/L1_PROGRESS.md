# L1 progress: the interior life layer (research/interior/LIFE_LAYER.md, items 1-50)

Agent L1 (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_L1.md` (logger `spikes/L1/tlog.py`,
per-model lines `spikes/L1/log_models.py`).

## Done
- Era checks: `research/interior/LIFE_LAYER_ERA.md` (50 kept; swaps inside #20 cups, #34 toys, #48 tea).
- Materials (B1 pipeline, `research/materials/make_l1_materials.py`, add only): `jp_m_decal_sumi_text_life` (a second
  ink atlas: ofuda, the Kyoho 15 calendar, lantern shop names + crests, ledger cover, cask mark), `jp_m_food_rice`,
  `jp_m_food_hoshigaki`, `jp_m_textile_kaya`; palette entries `rice_grain`, `hoshigaki`, `kaya_moegi`.
- Pipeline: `spikes/L1/build_l1.py` wraps B3a's build.py (unchanged): L1 props_life_*.py appended to MODULES; masters
  in spikes/L1/out; checks in spikes/L1/checks.json; sidecars gain master / mount / mount_note / tiers / hang_len.
- Decorator (`parts/kit/jpparts/decor.py`): catalogue reads the sidecar master + mount; helpers on_wall / on_beam /
  in_doorway / on_surface + by_mount; checks D15 / D16 only when life items are placed. Furnished machiya re-run
  (standalone verify.py): 136/137, the same as before the change (the one failure is the standalone-only CE
  frame-order check, 5.9 m, identical before and after; it passes inside buildings/pipeline.py).
- Section A (items 1-14): 46 models. Section B (15-17): 14 models. Section C (18-26): 37 models. All checks pass,
  binarized.

## Next
- Sections D (27-36), E (37-44), F (45-50); then pack jp_furniture.pbo + jp_common.pbo, contact sheets
  (`python spikes/L1/render_l1.py [prop ...]`, then `--sheets`), townhouse combos, final checks, report.

## How to resume
- `python spikes/L1/build_l1.py [prop ...] [--no-binarize] [--pack]` (props = the short names, e.g. `taru`).
- Readable text: use `lkit.text()` / `lkit.uvcell()`, never skit.text_on directly: DayZ model space is left-handed,
  so a decal whose u runs along +x on a +z face reads mirrored in game (and in the renders).
