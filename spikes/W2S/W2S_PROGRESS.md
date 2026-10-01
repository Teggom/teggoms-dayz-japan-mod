# W2S progress: Phase C wave 2, shrine + temple shells, village AND town grades (bare) (agent W2S, 2026-10-01)

Resumable notes. Time log `japan_dev/TIMELOG_W2S.md` (logger `python spikes/W2S/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Research notes (per building: period form, proportions, sources, the 1730 test): `spikes/W2S/W2S_NOTES.md`.

## Status: shells DONE (25, all checks pass); re-runs + sheets + push at the end of the run
- [x] notes  - [x] materials  - [x] template  - [x] shrine shells (13)  - [x] temple shells (12)  - [x] pack
- [x] re-runs (spikes/FB2/verify_all.py)  - [x] sheets  - [x] pushed

## Built
- Template `parts/kit/jpparts/templates/sacred.py` (new; rural.Shell bookkeeping + the W2P1 / W2P2 kit): kinds haiden,
  honden, temizuya, shamusho, kagura, do, hondo, kuri, shoro, gate; helpers town_frame / town_walls (bracketed halls:
  board walls column face to column face, ceiling), front_bay (doors / shitomi / lattice / sealed tobira between posts
  or round columns), hide_underfloor, far_trim, far_lift, far_r2_in_r3, remat, light_platform, paving.
- Recipe `buildings/sacredkit.py`; families `buildings/shrine`, `buildings/temple` (module sacred_shells.py); registry
  block W2S_SHRINE / W2S_TEMPLE (ship=True, no placements: W2F places).
- Materials (research/materials/make_w2s_materials.py): jp_m_roof_hiwada (derived), jp_m_roof_copper,
  jp_m_metal_bronze (assumed); palette roof_hiwada, roof_copper_patina, bronze_patina; jp_common.pbo repacked.
  Kit stand-ins now use them: koran / tobira / ornament / shitomi METAL -> metal_bronze, sori hiwada / copper.
  Parts re-made (build_parts --only, 8 part families, 234 parts, 0 failures).
- buildings/shellcheck.py: door_world_rot measures the door head with vertical rays (W2C's bounding box counted a
  sloped kohai in front of a shrine door at its outer eave height).

## Shells (class = Land_JP_<...>; faces R1/R2/R3; checks)
| Family | Class | Grade | Budget | Faces | Checks |
|---|---|---|---|---|---|
| haiden | Shrine_Haiden_Village | village | standard | 3485/981/585 | 32/32 |
| haiden | Shrine_Haiden_Town_Hiwada / _Copper | town | large | 9659 / 9871 / 2891 / 1287 | 42/42 x2 |
| honden | Shrine_Honden_Nagare_Village (+ _Chigi) | village | standard | 3120 / 3284 | 28/28 x2 |
| honden | Shrine_Honden_Nagare_Town (sangen-sha, curved hiwada) | town | large | 6614/1840/852 | 28/28 |
| honden | Shrine_Honden_Shinmei | village | standard | 2428/913/613 | 28/28 |
| temizuya | Shrine_Temizuya_Village / _Town | v / t | standard | 801 / 2315 | 28/28 x2 |
| shamusho | Shrine_Shamusho_Itabuki / _Sangawara | v / t | standard | 3338 / 4767 | 49/49 x2 |
| kagura | Shrine_Kagura_Village / _Town | v / t | standard / large | 2123 / 4268 | 28/28 x2 |
| do | Temple_Do_2_Board / _2_Thatch / _3_Tile | village | std / std / large | 3148 / 2448 / 6209 | 36 / 32 / 43 |
| do | Temple_Do_Town (curved copper hogyo) | town | large | 9240/2686/1031 | 43/43 |
| hondo | Temple_Hondo_Village (4 x 4 ken) / _Town (3 x 3 bays, degumi) | v / t | large | 8722 / 11510 | 53 / 43 |
| kuri | Temple_Kuri_Village (thatch) / _Town (tile), genkan porch | v / t | large | 7626 / 11444 | 70/70 x2 |
| shoro | Temple_Shoro_Village (open) / _Town (hakama + outside stair) | v / t | std / large | 3045 / 6371/2435/1267 | 28/28 x2 |
| gate | Temple_Gate_Yakuimon / _Shikyakumon | v / t | standard | 1858 / 2575 | 33/33 x2 |
Total 950 checks, 0 failures.

## Not built (decisions)
- Kasuga honden (tsumairi + kohai on the gable): not cheap with the kit (the kohai generator expects an eave front).
- Wari-haiden passage: not built (split floor + two more stairs).
- Mitesaki town hondo: 17.6k faces > the large budget at 3 x 3 bays; degumi is the right set for that size.
- Optional sanmon / 3-storey pagoda / sutra repository: not built this run.

## How to rerun
- Build + check: `python buildings/pipeline.py --family shrine --jobs 7` (then `--family temple`; --family takes ONE family)
- Quick look: `python spikes/W2S/try_sacred.py haiden '{"grade": "town"}'` (faces, budget, tags)
- Debug: `python spikes/W2S/dbg.py <key> leak|c15`, `python spikes/W2S/dbg_door.py <key> <door#>`,
  `python spikes/W2S/probe.py <key> x z` (solids over a model-frame point per LOD)
- Sheets: `python spikes/W2S/render_w2s.py family --jobs 7` and `... closeup`; previews `... preview --keys k1,k2`
- Materials: `python research/materials/make_w2s_materials.py [--only id]`

## Commits
- 06f8b5f materials + kit stand-ins + notes; 8f37a27 shells (25) + template + registry + shellcheck + parts;
  474c44f untrack W2P1/W2P2 test MLODs swept into 8f37a27 (files kept on disk); then the sheets / final commit.

## For the lead
- `buildings/shrine/out/` and `buildings/temple/out/` are not in .gitignore (the other families' out/ dirs are);
  W2S did not edit the shared .gitignore: add `buildings/shrine/out/` and `buildings/temple/out/`.
