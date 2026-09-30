# B3a progress: interior props, wave 1 (research/interior/BUILD_LIST.md) — DONE

Agent B3a (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_B3a.md`.

## Status
All 24 wave-1 props, **110 models** (24 new, 36 variants, 50 abandoned states). Checks: 110/110 pass
(`spikes/B3a/checks.json`); binarize 110/110 ODOL, 0 warnings; CfgConvert OK.
PBO: `@Japan/addons/jp_furniture.pbo` (prefix `JP\furniture`, CfgPatches `JP_Furniture`, requires DZ_Data +
JP_Common, 110 classes `StaticObj_JP_F_<Name>` : HouseNoDestruct, scope 1, like vanilla StaticObj_Furniture_*).
Sheets: `research/interior/contact_sheets/b3a_{kitchen,heat_shop,storage,bedding_debris}.jpg`.

| Category (folder) | Props |
|---|---|
| kitchen | kama (kama, nabe), jizai_kagi (std, plain), mizugame, oke (bucket, tarai, pickle), tana (0.91/1.365/1.82 x 1/3 boards), firewood (stack, bundle), jar (s/m/l, pale glaze) |
| heat_light | andon (kaku, ariake), hibachi (round, box), tabakobon |
| storage | nagamochi, tansu (+ single box), kori (1, stack of 2), box (s/m/l, stack3, lacquer s/m), tawara (bale, stack6, kamasu, kamasu stack3), rack (1 ken, half) |
| bedding | futon_stack, futon_laid, mushiro (flat, rolled, pile) |
| shop | zukue (choba, plain), choba_goshi (3, 2 folds), misedana (1 ken, half), goods_general (cloth, paper) |
| debris | leaves, straw, paper, shards (decal + bits, <= 100 faces) |

## Conventions (for B4, the decorator)
- Frame: origin = base centre on the floor, +z = front, autocenter=0. Sidecar `anchor`: `wall` (tana: wall
  plane z = 0) or `hang` (jizai-kagi: origin = hook-beam underside).
- LODs: Res 1-2 (Res 3 for tana, nagamochi, tansu, rack, misedana), Geometry / View / Fire (closed convex
  components); no Memory (Q5). Flat props (mats, litter, swept goods) and the jizai-kagi have no collision:
  put them in Resolution 1 only. futon_laid has a 0.08 Geometry slab + Roadway (textile_carpet_int).
- Sidecars `src/JP/furniture/<cat>/<prop>.prop.json`: per model the class, p3d, state, faces, bbox,
  `footprint_xz` (collision; subtract + 0.4 m from lootFloor), `loot_surfaces` (y, rect, range, points), dims,
  notes. 62 loot surfaces; each point is checked to sit on a Res 1 up-face at its height, <= 1.40 m.
- kama `seat_y` 0.168: place at kamado rim top - 0.168. nagamochi_open needs 0.08 m behind (lid).
- Smooth vertex normals on round objects (lathe) and soft goods (auto_smooth); everything else flat.

## Reuse by B3b (outdoor)
- Firewood: `props_kitchen.stack(length, depth, height, log_d, seed, rows_keep, mats, core_mat, wear)` and
  `bundle(rng, d, L, broken, mats, band)`; wrap them in an FPart with `budget` 1500 (G1 A3 ceiling) for the big
  eave stacks. Materials default to wood_weathered + wood_endgrain; pass `wear="_w2"` outdoors.
- Oke: `bucket_parts(wear)`, `tub_profile(r_bot, r_top, h)` + `hoops(...)`, or `oke(kind, state)` whole.
- Tawara: `props_storage.tawara_bale(n, segs, mat, rope, wear, bands)`, `tawara_col()`, `kamasu_bag()`.
- The kit: `spikes/B3a/fkit.py` (FPart with loot/anchor/budget, lathe with smooth normals, xf, rest,
  auto_smooth, board bands) and `bits.py`; `build.py` checks. B3b can import them (sys.path to spikes/B3a) or
  copy them into its own folder; to add models to jp_furniture.pbo instead, add a `props_*.py` to `MODULES`.

## Decisions I made
- Output folders by build-list category, not room tag (props span many rooms).
- Pipeline lives in `spikes/B3a/` (agent path); MLOD masters in `spikes/B3a/out/` (not committed, regenerate).
- Budgets from the build list per prop (small <= 300 even for the firewood stack and tawara stack6).
- Tana loot only on boards <= 1.40 m (vanilla cap); the 1.70 board is dressing.
- Abandoned states added where the list named only the prop's abandoned look (e.g. nabe_rusted, tarai_dry,
  pickle_open, kori_open, mushiro_rolled_loose / pile_spread, zukue_plain_tipped).
- Jizai-kagi fixed at 1.50 m (list 1.2-1.8); no Shadow Volume LOD (vanilla furniture has none).

## Material gaps (closest used)
- Rice / salt / grain spill: `jp_m_paper_shoji _w0` (pale). Wicker trunk reads pale grey with
  `jp_m_bamboo_weave` (per the list). Firewood (`wood_weathered`) reads redder than the pale split wood of i22.
- Garments / cloth: the bedding textiles (indigo, kinari), no printed kimono cloth.

## Not done / open
- Not tested in game. Decal alpha checked only in Blender renders.
- Refs i31, i35 (and the tabakobon's i38) are saved HTML error pages, so some sheet rows show one or no picture.

## How to rebuild
`python spikes/B3a/build.py [prop ...] [--no-binarize] [--pack]`; `python spikes/B3a/render.py [prop ...]`;
`python spikes/B3a/render.py --sheets`.
