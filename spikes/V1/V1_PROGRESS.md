# V1 progress: fast building checks (cache + smarter slow checks)

Time log: `TIMELOG_V1.md` (logger `spikes/V1/timelog.py`).

## 1. Profile (2026-10-01, one process each, 4 at a time; `spikes/V1/profile_one.py`, results `spikes/V1/prof/old|new/<key>.json`)

Per building, seconds. "old" = HEAD code (JP_RAY_ENGINE=brute JP_ZFIGHT_ENGINE=old), "new" = V1 engines.
Model generation = recipe model() + zfight.resolve + Part.lods + write_mlod (recipe itself is only 0.1-0.3 s;
zfight.resolve is ~85 % of it). Check groups = sum of that check id's lines.

| building | checks | build old/new | verify old | verify new | old top checks | new top checks |
|---|---|---|---|---|---|---|
| machiya_t3_01 | 81 | 2.9 / 2.5 | 44.8 | 7.3 | C11 24.8, C17 12.1, C15 6.3, C20 0.5 | C17 3.3, C11 2.2, C15 0.4, C20 0.4 |
| th_kamigata_3k_middle_toril | 61 | 1.5 / 1.4 | 22.1 | 3.8 | C11 11.7, C17 6.2, C15 3.3 | C17 1.9, C11 0.9, C15 0.2 |
| farmhouse_kanto_yosemune_umaya | 81 | 2.5 / 2.1 | 41.6 | 5.8 | C11 25.5, C17 7.2, C15 6.9 | C17 2.1, C11 1.3, C15 0.7 |
| inn_grand | 91 | 2.9 / 2.4 | 48.8 | 8.7 | C11 27.2, C17 13.9, C15 6.0 | C17 4.0, C11 2.7, C15 0.5 |
| temple_hondo_town | 43 | 2.3 / 1.8 | 25.9 | 4.1 | C17 9.6, C11 8.6, C15 6.1 | C17 1.4, C11 0.8, C15 0.5 |
| f_inn_grand (furnished) | 156 | 3.3 / 2.7 | 40.1 | 9.0 | C11 19.4, C17 12.5, C15 5.9 | C17 4.0, C11 2.4, C15 0.5 |
| machiya_t3_01_shop (furnished) | 140 | 3.2 / 2.6 | 35.8 | 7.7 | C11 18.4, C17 10.3, C15 5.1 | C17 3.3, C11 2.2, C15 0.4 |

(new = after the first engine pass; later tweaks: C17 -0.4..0.8 s more.)

Hotspots (cProfile, townhouse unit): `raycheck.cast` = 86 % of verify time: C11 envelope leak (44-63k rays), C17 jamb
slits (180-380k rays), C15 silhouette (56-120k vertical columns). C10 door reach, C12 roof pokes, C20 z-fight, the
decorator checks D1-D16: each < 0.6 s. Binarize is not part of verify. zfight.resolve (model generation) 1.3-2.7 s.
C2's per-face isfile ~0.2 s.

## 2. Smarter slow checks (done; equivalence per engine shown ray by ray)
- `raycheck.escapes()` (C11, C17): any-hit (both checks only ask "is anything hit before tmax"), per eye: the box of the
  eye's segments, distance stages, and the exact edge-wedge test (a direction can hit a triangle only if it is on the
  inner side of the 3 planes through the eye and each edge; pad 1e-5; eye within 5 cm of a triangle's box or nearly
  in its plane = always tested). Same Moller-Trumbore predicate (`hit_pairs`) as `_cast_brute`.
- `raycheck.cast_down()` (C15): a vertical column is tested only against triangles whose x/z box holds it. Bitwise
  identical heights.
- C17 ray construction vectorised (bitwise identical rays, checked).
- `zfight.coplanar`: the 81-cell candidate list is built once per plane key (not per face) + a numpy pre-filter of the
  cheap per-pair rejections (same IEEE arithmetic, same pair order). Results identical (records + order); resolve()
  moves the same solids.
- Switches: `JP_RAY_ENGINE=brute`, `JP_ZFIGHT_ENGINE=old` run the pre-V1 code paths (used for the equivalence runs).

## 3. Cache (done)
`buildings/checkcache.py` (docstring = the full rules). Cache files `data/C/_build/check_cache/<key>.json` (data/ is
git-ignored: machine-local, it hashes this machine's ODOLs and generated materials). Fingerprint = registry entry
(+ base entry of a furnished variant) + budget + the source of every module in the recipe's / checks' import closure
(AST, also function-level imports and literal spec_from_file_location paths; registry.py itself excluded) + engine
switches + Python / numpy versions. Data deps recorded per building while it is built and checked (audit hook on
open / listdir / scandir / glob, wrappers on os.path.isfile / exists / isdir): file content hashes, existence probes,
listings, glob results; import-time reads (core's material library) count for every building; shared generated files
count only by the building's own part (config.cpp class block, CE group, model.cfg bone classes); the building's own
outputs (out/, checks / records / rooms json) are excluded; decor / shop_sets lazy file caches are emptied before each
building. Only a PASS is stored. Hit = "RESULT <key>: PASS (...) [cached]" and the checks file restored if it differs.
Wired into pipeline.py (--verify-only, the build's verify step, verify_parallel; new flag --full) and the new
buildings/verify_all.py (default 4 processes, max 4). spikes/FB2/verify_all.py forwards to it.
Module -> buildings map (from the fingerprints): sori/kumimono/nagare/... -> the 25 shrine + temple shells only;
templates/townhouse + shellkit -> 94 (townhouse, posttown, hatago, 13 furnished); core/walls/roofs/raycheck/
buildcheck/zfight/pipeline/shellcheck -> all 169.

Also: pipeline's verify step no longer rebuilds family members (C2 did): build_model keeps a per-building snapshot
of the recipe module state (bd["mod"]). Tested on `pipeline.py --family kido --no-pack --full` (build + binarize +
checks, no rebuild): checks identical to HEAD except the ODOL byte count (binarize noise); ODOLs + checks restored.

## 4. Equivalence (all 169 shipped buildings)
- Old run: `JP_RAY_ENGINE=brute JP_ZFIGHT_ENGINE=old buildings/verify_all.py --full` (snapshots data/V1/eq/old, old2).
- New run: `buildings/verify_all.py --full` (data/V1/eq/new). `spikes/V1/compare_checks.py old2 new`:
  **169 / 169 checks files byte-identical (10,262 checks: pass/fail, names, every detail string).**
- Each building alone in its own process (`JP_VERIFY_BATCH=1`, data/V1/eq/solo) vs batched: 169 / 169 byte-identical
  (no build-order dependence: needed for a per-building cache).
- zfight (`spikes/V1/eq_zfight.py`, all 169): coplanar() records identical (same order); resolve() moves exactly the
  same solids (every vertex identical).
- Ray level (`spikes/V1/eq_rays.py`): C11 escaped-ray sets, C17 slit lists + the rays themselves (bitwise), C15 column
  heights (bitwise): see below.
- **One intentional difference vs HEAD (3 buildings: s1_th_edo_2k_middle_board_shitate, s1_th_edo_3k_endl_kusuri,
  s1_th_kamigata_3k_middle_kyo_ningyo): a check NAME.** furnishkit forwarded the base shell's PASSAGE_LABEL with the
  previous furnished building's label as the fallback, so a town-house-based furnished variant got the hut's label
  "C7 open doorway (mushiro, no leaf) ..." when a hut-based one ran before it in the same process (W2S's batching).
  Fixed (furnishkit's own default "C7 open passage clear >= 1.00 + head >= 2.00"); same pass, same detail.

## 5. Timings (4 processes max; Stephen's PC, 20 threads)
| case | before (HEAD engines) | after |
|---|---|---|
| one building, machiya_t3_01 (`pipeline.py --verify-only --full`, whole process) | 35.7 s | 9.2 s |
| family townhouse (69) `verify_all.py --full --family townhouse` | 463 s | 90 s |
| family shrine (13) | 28 s | 9 s |
| all 169, no cache (`--full`) | 935 s (W2S: 1,393 s at 10 processes) | 193 s |
| all 169, nothing changed (cache) | (no cache: 935 s) | 3 s |
| one kit module changed (sori.py: 25 shrine + temple re-checked, 144 cached) | 935 s (everything re-run) | 29 s |
| each building in its own process (`JP_VERIFY_BATCH=1`) | - | 216 s |

## Status / next
- [x] profile  - [x] ray engines  - [x] zfight  - [x] cache wiring  - [x] equivalence (checks files, zfight)
- [ ] ray-level equivalence all 169 (running)  - [x] timings  - [x] docs (B0_PROGRESS, README 2b)  - [ ] commit + push
