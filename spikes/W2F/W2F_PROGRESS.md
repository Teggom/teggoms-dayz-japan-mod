# W2F progress: Phase C wave 2, furnish + place + the walk (agent W2F, 2026-10-01)

Resumable notes. Time log `japan_dev/TIMELOG_W2F.md` (logger `python spikes/W2F/tlog.py "<event>" W2F "<tag>" <5h> <wk>`).

## Plan (decided at setup)
- **Props**: new specialty props in `spikes/W2F/props_w2f_*.py`, built INTO the furniture pipeline after S1
  (`spikes/W2F/build_w2f.py` = B3a + L1 + S1 + W2F modules -> jp_furniture.pbo; masters in spikes/W2F/out).
  PITFALL: a later `spikes/S1/build_s1.py` / L1 / B3a rebuild rewrites config.cpp WITHOUT the W2F classes:
  afterwards run `python spikes/W2F/build_w2f.py --pack`.
- **Dressings**: `buildings/w2f_sets.py` (SETS hooked into buildings/furnish_sets.py like shop_sets), registry block
  `W2F_FURNISHED` (family dir `furnished`, class = base class + suffix).
- **decor.py** (additive): a dressing may mark a non-room space `sparse` (veranda en, temizuya pavilion, gate passage,
  bell platform): D1 then takes 0-7 props and D3 (raised loot surface) is not required there.
- **Placement**: own CSV `test/placements/W2F.csv` + `test/ce/W2F_mapgrouppos.xml` (spikes/W2F/layout_w2f.py), NOT
  registry placements (shellcheck's "inside the test yard" check would fail for the hill-foot precinct, z > 1124).
- **Sects**: village temple = Jodo (nenbutsu plaque, small mokugyo), town temple = Zen/Soto (fish board gyoban,
  cloud gong umpan, big mokugyo). Nichiren needs a daimoku atlas cell (none exists), Shinshu needs a tatami-floor
  shell option (none): not used.

## Status
- [ ] props  - [ ] dressings  - [ ] registry + build + checks  - [ ] placement + world + mission
- [ ] maps + SHOWCASE_MAP  - [ ] sheets  - [ ] checklist  - [ ] verify_all --full  - [ ] pushed
