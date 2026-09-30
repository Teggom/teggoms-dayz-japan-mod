# L2 progress: the outdoor life layer (research/interior/LIFE_LAYER.md, items 51-74) + the B3b text check

Agent L2 (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_L2.md` (logger `spikes/L2/tlog.py`).

## Step 0: text mirroring — DONE (verdict: B3b's text was mirrored AND back-facing; L1's was back-facing)
- **Evidence.** `spikes/L2/textface.py` (the TXT check, reads the written MLOD): for every text-atlas face, outward =
  minus the stored normal; FACE = a host surface lies behind it (ray along -outward within 5 cm); READ = the texture
  +u runs to the viewer's right, right = cross(up, -outward) (left-handed: up +y, looking +z -> right +x = east).
  Before: B3b 37 of 37 text models FAIL FACE (read OK only from INSIDE the board = mirrored from outside), L1 23 of
  23 FAIL FACE (u already mirrored by lkit.text, but facing in). Renders with back faces culled, as the game draws
  single-sided faces: `research/outdoor_kit/contact_sheets/l2_textcheck_before.jpg` (the text is gone) and
  `..._after.jpg` (御酒, 御菓子所, 庚申供養塔, 用水 read correctly). An earlier unculled render of the old masters showed
  御酒 on the chochin mirrored.
- **Cause.** `skit.decal()` takes its normal from newell(tl, tr, br, bl), which for right x up = +z gives -z: the
  quad faces into its host. `text_on()` lays u along `right`, which a viewer outside sees as his left.
- **Fix (no class names changed).** `skit.face_text(solids, mirror_u)` flips every text-atlas solid's faces and
  (optionally) mirrors u inside the solid's own cell range; `skit.text_ok()` = text_on already fixed (for new code).
  B3b's `build.py` calls `face_text(mirror_u=True)` on every model after building; L1's `build_l1.py` calls it with
  `mirror_u=False`. B3b's chochin text strip lifted 4 -> 9 mm (it came within 0.02 mm of the paper: z-fight).
- **Rebuilt:** B3b all 129 (37 MLOD masters changed = exactly the text models; 92 byte-identical), jp_site.pbo
  repacked; L1 ofuda, koyomi, chochin, fire_gear, taru, choba_set, yoroibitsu, 185/185 binarized, jp_furniture.pbo
  repacked; machiya_t3_01_shop through `buildings/pipeline.py` (137/137, --no-pack and packed), jp_buildings.pbo.
- **Re-runs:** B3b 129/129; L1 185/185; TXT 60/60 text models pass (B3b 37 + L1 23); B3a/B4 prop checks 112/112,
  faces unchanged (`spikes/L2/check_b3a.py`); townhouse combos 60/60, 0 over budget (`spikes/L2/_combos.log`).

## Step 1: era — DONE
`research/interior/LIFE_LAYER_ERA.md` (L2 section): 24 kept, 0 dropped; swaps inside #53 (plain Edo jugoya offering),
#54 (no threshing comb), #58 (no morning glories, unglazed pots), #62 (clappers, no drawn face), #64 (open kago, not a
norimono), #66 (wood / gourd floats, never glass), #70 (stoneware cup, no choko).

## Step 2: the 24 outdoor items — DONE (81 models: 22 new, 20 variants, 39 abandoned per the time-log tags)
| Group | Items (models) | Folder |
|---|---|---|
| G1 | hasa 5, kaki_curtain 3, tsukimi 3, scarecrow 4 | src/JP/site/yard_life |
| G2 | farm_tools 3, leaf_pile 3, ladder 3, charcoal_bales 3 | yard_life |
| G3 | potted 4, bird_cage 3, kakei 3, stable_yard 4 | yard_life |
| H1 | travel_gear 3, kago 3, tenbin_spill 3 (extends B3b's tenbin), bench_dress 4, stool 3, footwear 3 | street_life |
| H2 | fishnet 4, boat 4 | street_life |
| H3 | fire_watch 3, sandals_sale 3, amado 4, lantern_fallen 3 | street_life |
- Checks 81/81 (B3b's set + TXT), binarize 81/81 ODOL, 0 warnings. Max Res 1 faces 594 (potted stand); nothing over its
  class (small 300 / box 600 / medium 1,500). Collision: stone, wood, carts, boats, stands = Geometry + View + Fire;
  rice sheaves View only (soft cover); cloth, nets, small dropped things = none.
- Mounts (sidecar `mount`): street 22, yard 21, eaves 9, field 9, shore 8, road 8, surface 4 (bench dressing on
  B3b's bench seats). `decor.on_site()` / `decor.under_eaves()` / `decor.on_surface()`; `decor.by_mount("shore")`.
- Text: jp_s_tenbin_spill_boxes (伊勢屋), fire_watch (火之用心, 大), lantern_fallen (本町, 御休処, crest) via existing cells.

## Materials added (B1 pipeline, add only: research/materials/make_l2_materials.py; C1 in checks_l2.json)
`jp_m_textile_net` (alpha-cut knotted net, palette cha_koge), `jp_m_plant_foliage` (alpha-cut leaf / needle cards,
new palette `foliage_green` [72,86,56], assumed). _w2 foliage (dead) is WARN dE 9.8 (within 12).

## PBOs
jp_site.pbo = 210 classes (129 B3b + 81 L2 `StaticObj_JP_S_*`); jp_common.pbo repacked; jp_furniture.pbo and
jp_buildings.pbo repacked at step 0.

## Shared code touched and re-runs (all after the last change)
skit (face_text, text_ok), lkit (comment), B3b build.py + L1 build_l1.py (text post-process), decor.py (on_site,
under_eaves; no new checks). Re-runs: B3b 129/129 (spikes/L2/check_b3b.py, sandboxed), L1 185/185 (check_l1.py,
sandboxed), B3a/B4 112/112 (check_b3a.py), furnished machiya 137/137 (--no-pack; the packed ODOL is the step-0 one,
restored after the re-run), townhouse combos 60/60, TXT 66/66 text models (B3b 37, L1 23, L2 6).

## Decisions I made
- Fixed L1's text facing as well (same bug, same fix; brief named only B3b).
- Chochin text strip lifted 4 -> 9 mm (z-fight at 0.02 mm).
- #53 moon-viewing stand uses mount 'eaves' (it stands on the veranda: on_site(..., y=veranda floor)).
- Scarecrow, hasa and nets: filler budgets; nets are one alpha sheet per span (new material) instead of strands.
- Sheaves are soft cover (View only), like B3b's straw stacks.
- Eaves pieces assume the eave / bracket underside at 2.40 m (sidecar hang_y); under_eaves() lifts them.

## Not done / open
- Nothing tested in game. No building or site uses the L2 items yet (a decorator task).
- B3b's own build.py regenerates config.cpp WITHOUT the L2 classes: after any B3b rebuild, run
  `python spikes/L2/build_l2.py --pack`.

## How to resume / rebuild
- `python spikes/L2/build_l2.py [prop ...] [--no-binarize] [--pack]`; `python spikes/L2/render_l2.py [prop ...]`,
  `--sheets`; `python spikes/L2/log_models.py <5h> <wk> prop ...`
- `python spikes/L2/textface.py <p3d or folder>`; `python spikes/L2/textcheck.py <tag>`
- Materials: `python research/materials/make_l2_materials.py [--no-pack]`
