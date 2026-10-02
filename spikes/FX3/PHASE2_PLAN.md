# FX3 phase 2 plan: integration + rebuild (starts only when the lead says FX2 is done)

Phase 1 result (spikes/FX3): `uvwood.py` (shared pass), `make_atlases.py` (atlases, macro, moss, thatch _w2, draft
rvmats), `samples.py` + `render_fx3.py` (shipped recipes built into spikes/FX3/out only), `fx3_samples.jpg`
(before / after), `INVENTORY.md`, `atlas_report.json` (per-material joints, roll, patch L*, atlas-vs-tile dE = 0.01-
0.09, macro mean shift dE 0.4-3.3 wood / 4.0 thatch _w2, all far inside the palette tolerances 6-14).
Proven on the samples: 2,597 teahouse faces in 874 uv groups, zfight C20 'same' 0 -> 0 and 'hidden' (drawn-identical)
pairs 209 -> 209 (the plane grouping keeps every coplanar overlap identical); tansu / nagamochi plank bands kept
(band mode, 57 faces).

## 1. Files changed (in this order)

### Materials (research/materials + src/JP/common/materials)
1. **NEW `research/materials/make_wood_atlas.py`** = spikes/FX3/make_atlases.py promoted: runs AFTER the makers on
   `data/materials/textures/*.png`; writes the 2048 x 1024 atlases over the same PNG names (idempotent: a 2048-wide
   input is first restored from the maker, i.e. the step always starts from the maker's 1024 tile -> it must be called
   from build_materials' texture step, never on its own output). Also: `macro/jp_m_macro_wood{,_dark,_int}_w{0,1,2}_mc`,
   `macro/jp_m_macro_thatch_w{1,2}_mc`, the irregular moss decal, thatch _w2 without baked moss.
2. `research/materials/make_textures.py`: roof_thatch lv 2 without the moss patch (moss lives in the macro now).
3. `research/materials/make_b1_materials.py`: decal_moss -> the FX3 recipe, `M("jp_m_decal_moss", ..., 2.0, 1024, ...)`.
4. `research/materials/build_materials.py`: `STAGES[3]` per material from a MACRO table (texture + uvTransform
   aside/up: wood 0.2721 / 0.1156 = 14.7 m x 17.3 m; thatch 0.2151 / 0.2597 = 9.3 m x 7.7 m), `rvmat_text(...,
   macro=None)`; the atlas step + `to_paa` for the new `macro` family folder; sidecars gain
   `"atlas": {"w_m": 4.0, "h_m": 2.0, "patches": 4, "lock": "band"?}` and `"macro"`; `texture_px` -> [2048, 1024].
   tile_size_m stays 2.0 (upstream UV code is unchanged; only uvwood knows the atlas).
5. Rewrite rvmats (`build_materials.py --rvmats-only --no-pack`, plus make_part_materials.py / make_fix_materials.py
   `--rvmats-only` for any rvmat they own) -> **every wood + thatch rvmat gets Stage3**. Matte recipe (§15.3 T12)
   unchanged: Stage6 fresnel(0.01,0.01), Stage7 black.
6. ImageToPAA: 33 wood atlases x 3 maps + 11 macro + moss 3 x 3 + thatch _w2 3 into src/JP/common/materials (PAAs
   are git-ignored, regenerated). Run matcheck (tools/matcheck) on the library: atlas mean = tile mean by
   construction, expect no change.

### Kit + pipelines
7. **NEW `parts/kit/jpparts/uvwood.py`** (= spikes/FX3/uvwood.py; ATLAS read from the sidecars via mat_info, the
   phase-1 `install()` dropped).
8. `parts/kit/jpparts/core.py`: `_load_lib` reads `"atlas"`; `Part.lods()` starts with `uvwood.remap_part(self)`
   (idempotent) -> covers jpparts parts, buildings, and every FPart/SPart/LPart prop (B3a, B3b, L1, L2, S1, W2F,
   FP1/FP2/FX1/FX2 builders).
9. `spikes/B3a/fkit.py`: `band_fit` records `s.uvband` (face indices) -> band mode for wood_interior bands
   (fkit.board / WOOD_BANDS, tansu GROOVE). xf/transformed copy it (copy.copy).
10. `buildings/pipeline.py` build_model: `uvwood.remap_part(M, salt=name)` right BEFORE `ZF.resolve(M)` (zfight must
    see the final uv; proven on K2).
11. Moss: sidecar tile 0.5 -> 2.0 (skit/w2kit moss code already scales by mat_info tile, so no code change).

## 2. Rebuild order and pitfalls

1. Materials (1-6), then **jp_common pack** (build_materials pack / `--rvmats-only` without `--no-pack` at the end).
2. Parts: `parts/kit/build_parts.py` (src/JP/parts ODOLs).
3. Buildings: `python buildings/verify_all.py --full` after the pipeline rebuild (the V1 cache fingerprints jpparts
   modules, so core.py / uvwood.py changes re-run all 193). **`buildings/pipeline.py --help` STARTS A FULL REBUILD.**
4. Props, each pipeline's own build with binarize + pack, in this order:
   B3a `spikes/B3a/build.py` -> L1 `build_l1.py` -> S1 `build_s1.py` -> **W2F `build_w2f.py --pack` LAST of the
   furniture PBO** (B3a / L1 / S1 rebuilds drop W2F's classes; its folder binarize crashed on an existing ODOL in FX1:
   binarize singly if it repeats); B3b `spikes/B3b/build.py` -> **L2 `build_l2.py --pack` after B3b** (B3b drops the
   L2 classes); FP1 / FP2 / FX1 / FX2 builders for the props they own (check their pack.py).
5. **Binarize byte-noise:** ODOLs whose content did not change (no wood) are rewritten anyway -> `git checkout --` them
   (compare against HEAD before committing).
6. ODOL embeds the rvmat: every model with a changed rvmat must be re-binarized (all of the above do).
7. No mission / world rebuild needed (placements unchanged). Never start or stop the server; the PBO repack fails
   while a live DayZServer locks the PBO (verify the packed PBO, not the source).

## 3. Checks (no per-prop renders)

- `python buildings/verify_all.py --full` (4 jobs): C20 z-fighting must stay 0; all 193 / ~11,8xx checks pass.
- Each prop build's checks.json (palette C1 on the atlas, budgets unchanged: face counts do not change at all).
- **TXT check** (spikes/L2/textface.py via B3b / L2 / S1 builds): uv-sensitive; uvwood touches only ATLAS materials,
  so text decals must stay byte-identical: add `spikes/FX3/uvdiff.py`: for every rebuilt MLOD, the uv of every
  face whose material is NOT in ATLAS equals HEAD's (and face counts equal) -> proves nothing else moved.
- `verify_oprw` / bindcheck as the last builds did (unchanged geometry; quick sanity).
- matcheck on the library.
- One before / after sheet only if the lead wants it (the phase-1 sheet already shows the look).

## 4. In-game checklist items for Stephen (one walk, ~5 min)

1. Torii poles, posts and board walls: no repeating knot at the same height; no visible seam inside one board.
2. Flipped faces (about half the groups): the bump lighting must look the same as unflipped ones. If the
   grain bumps look inverted on some faces, set `uvwood.ALLOW_FLIP = False` and rebuild (one switch).
3. Macro: soft grime / sun-bleach / streaks at 15 m scale on wood; not blotchy up close.
4. K2 thatch: moss in irregular carpets, no 2 m repeat; moss decals on stones / torii irregular.
5. Furniture (tansu, nagamochi): plank bands clean, no grey patches indoors.

## 5. Known limits / options

- Repetition along one long face is still 2 m (the column tiles along v); a 4 m tall atlas would halve that for 2x
  memory.
- Proxied props (one p3d placed many times) look identical per placement: variety per placement needs variants.
- Variant patches reuse the material's own boards (shuffled, shifted, flipped, re-toned); new boards from other CC0
  plank scans recoloured to the palette is a later option.
- Firewood (semantic bark | split atlas, already random per billet) and end grain are untouched; bamboo / roof boards
  not in scope.
- Macro via uvSource="tex" follows each group's uv (per-plane offsets), so its tone varies per member rather than
  flowing continuously across a wall; a world-continuous macro would need a second UV set (#UVSet# 1 tagg in every
  MLOD writer + uvSource="tex1", as 316 vanilla structure rvmats do): recorded, not proposed.
