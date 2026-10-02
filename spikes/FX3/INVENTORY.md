# FX3 inventory: wood materials and every texture-mapping path (2026-10-01, phase 1, read-only survey)

## Headline

- **11 wood materials get atlases** (x 3 wears = 33 textures sets), 2 more wood materials are deliberately left
  alone (end grain, firewood), plus the moss decal and the thatch macro.
- **ONE choke point covers almost everything:** every pipeline's visual LOD is written by `core.Part._visual`
  (jpparts) or its override `fkit.FPart._visual` (B3a; inherited by skit.SPart / lkit.LPart, so B3b, L1, L2, S1,
  W2F, FP1/FP2 props). Both are reached through `Part.lods()`. Buildings (`buildings/pipeline.py`) build one big
  `Part` (merged parts) and call `M.lods()` after `zfight.resolve(M)`.
- **UVs are made in 11 places** (below) but all of them end up as `Solid.fuv` lists before `lods()`. So the shared
  pass works on `Solid.fuv` + `Solid.fm` + geometry and **no UV generator has to change**.
- **3 pixel/semantic-locked mappings** must be respected: `fkit.band_fit` (wood_interior plank bands in 1024-px
  pixel units: fkit.board / WOOD_BANDS, tansu GROOVE), text/atlas cells (`skit.cell/decal`, `lkit.uvcell`; not
  wood), firewood's bark|split bands + end-grain discs (`woodpile.py`; already randomised per billet by FP2).
- **One check depends on UVs:** `zfight.looks_same` (C20: coplanar overlapping faces are harmless only when they
  draw identical uv). The TXT check (spikes/L2/textface.py) reads text-decal uv direction; text is not wood, but a
  pass that flipped u on a text decal would fail it: the pass only touches materials in its ATLAS table.

## Wood materials (src/JP/common/materials, sidecar tile 2.0 m, 1024 px, grain along v = along the member)

| key | made by | source | users (code refs) | FX3 |
|---|---|---|---|---|
| wood_weathered | make_textures.py (materials agent) | Poly Haven weathered_planks | jpparts 180 refs (posts, beams, plank walls, doors, verandas, eaves), buildings, B3a LOGWOOD, B3b torii/props | atlas |
| wood_street_dark | make_textures.py | japanese_cedar_planks | jpparts 34 (town fronts), L1 | atlas, dark macro |
| wood_kuro | make_textures.py | black_painted_planks | B3b, L1, W2F | atlas, dark macro |
| wood_sooted | make_textures.py | japanese_cedar_planks | jpparts 41 (interior beams), B3a SOOT_WOOD, B3b, woodpile cores | atlas, dark macro |
| wood_bengara (paint family) | make_textures.py | japanese_cedar_planks | B3b | atlas, dark macro |
| wood_new | make_m1_materials.py | weathered_planks (recoloured) | B3b graves, W2F | atlas |
| wood_silver | make_m1_materials.py | weathered_planks | B3b fences/gates/carts, W2F | atlas |
| wood_interior | make_b1_materials.py | procedural planks (grooves every ~78.7 px) | B3a WOOD (all furniture), L1, L2; **band_fit pixel-locked** | atlas, band mode |
| ceil_boards | make_b1_materials.py | procedural | jpparts ceilings | atlas |
| floor_boards_int / _rough | make_b1_materials.py | procedural | jpparts floors | atlas |
| wood_endgrain / _firewood | make_b1 / make_m1 / make_fp2 | procedural rings, 0.5 m | beam ends, billet ends (centred disc uv) | **untouched** |
| wood_firewood | make_m1 + make_fp2 | procedural, u 0-0.5 bark, 0.5-1 split | woodpile billets (per-billet random ub offset) | **untouched** (macro only, phase 3 option) |
| decal_moss (stone family) | make_b1 + make_fp1 (alpha hardened) | procedural, 0.5 m / 256 px | skit/w2kit moss_face, moss_strip, moss_foot (torii, stones, walls) | redrawn 2 m / 1024 px irregular; per-decal flip + offset |
| roof_thatch _w2 | make_textures.py | reed_roof_04 | jpparts roofs (K2 tea house = wear _w2) | baked moss removed, moss moved to the macro |

Bamboo, roof boards (kureita/kokera, procedural courses), lacquer: not in scope (courses / no photo repeats).

## Texture-mapping helpers (how wood UVs are generated today)

| # | where | helper | mapping | grain | notes for the pass |
|---|---|---|---|---|---|
| 1 | parts/kit/jpparts/core.py | `face_uvs` (Solid uv='world'/'grain'/'fit', uvscale, uvoff, uvrot) | planar per face in the PART frame, u, v = metres / sidecar tile | 'grain' or sidecar 'along member' -> v along the solid's longest bbox axis | plane groups |
| 2 | jpparts/core.py | `Solid.transformed`, `Part.transformed/merge` | copy.copy: fuv shared, unchanged ("textures glued") | - | pass runs after merge, in the model frame -> every placed instance varies |
| 3 | jpparts koyagumi.pole / kumimono.beam, roofs.tube (uvscale) | Solid with 'grain' | as 1 | along | plane / solid groups |
| 4 | spikes/B3a/fkit.py | `lathe` (smooth, explicit uv), `flat_poly`, `band_fit` + `board` (WOOD_BANDS px), `xf` (copy, uv glued) | cylindrical u round x v along profile; flat polys world xz | v along profile | lathe = solid group; band_fit faces = band mode |
| 5 | spikes/B3a/bits.py | domed grid sheets (straw bags) | world xz / tile | - | not wood |
| 6 | spikes/B3a/woodpile.py | billets: bark/split bands + `eg_uv` end discs, random ub/vo per billet | semantic | along billet | firewood/endgrain untouched; LOGWOOD/SOOT core blocks = plane groups |
| 7 | spikes/B3a/tansu.py | `band_fit` + GROOVE (75-82 px) | pixel-locked | - | band mode |
| 8 | spikes/B3b/skit.py | `pole`, `beam` (Solid 'grain'), `grid_sheet`, `tube` (smooth), `cell`/`decal` (atlas cells), `face_text` | as 1 / arc-length / cells | along | cells/text never touched (not wood) |
| 9 | spikes/B3b/w2kit.py | `moss_face`, `moss_strip`, `moss_foot` (random u0/v0 already), `aged_stone` (FP1: turns + shifts stone uv per piece) | decal quads | - | moss = solid groups; aged_stone = precedent for this job |
| 10 | spikes/B3b/ropekit.py | rope tubes | arc-length | along rope | not wood |
| 11 | spikes/L1/lkit.py, L2/l2kit.py, S1/s1kit.py | `uvcell` (mirrored text cells), `quad_sheet`, `strip` (world-ish along strip) | cells / explicit | - | wood strips = solid groups |

Writers that bypass `Part._visual`: `parts/kit/assembly.py` path B (merges part MLOD files as stored: UVs of the
part file, no per-instance variation; test assembly only), `research/materials/build_materials.py` swatch,
`spikes/effort_test/*` (dead). Buildings get furniture / dressing as PROXIES: a proxy prop keeps one UV layout per
p3d (variety comes from the prop's own pass, not per placement).

Rvmats: every library rvmat is written by `build_materials.rvmat_text` (STAGES[3] = `color(0,0,0,0,MC)`, i.e. no
macro today); the make_* scripts and parts/kit/make_part_materials.py / make_fix_materials.py reuse it.

## The shared helper (draft: spikes/FX3/uvwood.py; phase 2: parts/kit/jpparts/uvwood.py)

- `remap_part(P, salt=P.name)`: in place, idempotent, run once on the finished model (model frame).
- ATLAS table: material key -> atlas size (4 m x 2 m for wood, 2 m x 2 m for moss), flip allowed, lock mode.
  Phase 2 moves the table into each sidecar (`"atlas": {"w_m": 4.0, "h_m": 2.0, "patches": 4}`) and mat_info.
- Upstream UVs stay as they are (metres / sidecar tile 2.0); the pass maps them: `u' = fu*u*(tile/W) + U0`,
  `v' = fv*v*(tile_v/H) + V0`; U0 picks the patch (any of the 4 columns) + offset across the grain, V0 the offset
  along it, fu/fv the flips.
- Groups (one random map each): **plane** (flat auto-UV faces: material + plane, offsets clustered within 2 mm ->
  coplanar overlaps keep identical uv, C20 stays valid), **solid** (smooth or explicit-uv solids: continuity round
  a turned member), **band** (band_fit faces: `u/2 + h/2`, no u flip).
- Seed: FNV(salt + rounded geometry key) -> rebuild-stable and order-independent.
- Grain along the member and the 1-2 m scale come from upstream (face_uvs 'grain'; tile 2 m along v); the pass
  never swaps axes.

## Macro stage: what the engine supports (survey of 31,045 vanilla rvmats under P:\DZ, Super shader, Stage3 = MC)

- `uvSource="tex"` + uvTransform: ~1,850 rvmats (1,449 at scale 1, the rest scaled 2/3/4, non-uniform 2x1, 4x2,
  even rotated, e.g. characters\belts\data\leather_quiver_beige_damage.rvmat). Mostly the damage macros.
- `uvSource="tex1"` (a second UV set): 316, the structures / furniture (e.g. furniture\various\data\workbench.rvmat).
- The MC texture's RGB is alpha-blended over the diffuse.
- Choice: `tex` + a non-uniform scale (no MLOD writer change, works on every pipeline at once): wood 0.2721 / 0.1156
  (macro repeats every 14.7 m across x 17.3 m along the grain), thatch 0.2151 / 0.2597 (9.3 m x 7.7 m). The `tex1`
  route (world-continuous macro) needs a `#UVSet#` tagg in every MLOD writer: recorded in PHASE2_PLAN.md §5.
- Three wood macros (outdoor, dark woods with half the bleach, interior with grime only) and two thatch macros
  (_w1 grime / bleach, _w2 moss carpets); _w0 thatch keeps the empty `color(0,0,0,0,MC)`.
