# W2S progress: Phase C wave 2, shrine + temple shells, village AND town grades (bare) (agent W2S, 2026-10-01)

Resumable notes. Time log `japan_dev/TIMELOG_W2S.md` (logger `python spikes/W2S/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Research notes (per building: period form, proportions, sources, 1730 test): `spikes/W2S/W2S_NOTES.md`.

## Plan
- Template `parts/kit/jpparts/templates/sacred.py` (new; on templates/rural.py's Shell like civic.py) with kinds:
  haiden, honden, temizuya, shamusho, kagura (Shinto); do (small hall), hondo, kuri, shoro, gate (Buddhist).
- Recipe `buildings/sacredkit.py`; family folders `buildings/shrine`, `buildings/temple` (module sacred_shells.py);
  registry block W2S_* (ship=True, no placements; W2F places).
- Materials (research/materials/make_w2s_materials.py, B1's make_one, add only): jp_m_roof_hiwada, jp_m_roof_copper,
  jp_m_metal_bronze; then the kit's stand-ins point at them (sori auto-switch; koran / tobira / ornament / shitomi METAL).
- Checks: shellcheck (C1-C22 + bindcheck) per shell; re-run everything (spikes/FB2/verify_all.py) after kit changes.
- Sheets: research/production/contact_sheets/w2s_family.jpg + w2s_town_closeup.jpg.

## Status
- [ ] notes  - [ ] materials  - [ ] template  - [ ] shrine shells  - [ ] temple shells  - [ ] pack  - [ ] re-runs
- [ ] sheets  - [ ] pushed

## Commits
