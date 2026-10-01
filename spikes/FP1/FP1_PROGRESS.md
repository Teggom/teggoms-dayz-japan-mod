# FP1 progress: prop fixes and remakes from Stephen's showcase walk (2026-10-01)

Agent FP1 (opus). Time log `japan_dev/TIMELOG_FP1.md` (logger `spikes/FP1/tlog.py`). Runs alongside FB1 (buildings).
Owns: spikes/B3a, L1, L2, B3b (+W2/W3/G1 code), src/JP/furniture, src/JP/site, jp_furniture / jp_site / jp_common, materials.

## Identification (from SHOWCASE_MAP.md, C.csv, C3.csv, SH1.csv, spikes/C3/dress_island.py, buildings/furnish_sets.py)
| # | Finding | Model(s) | Where Stephen saw it |
|---|---|---|---|
| 1 | broom | L2 jp_s_leaf_pile_* (broom(), props_l2_yard.py #55); S1 broom() in props_s1_g1.py (aramono goods) | L55 gallery 1080.3,1025; hamlet 947.5,1008.2 |
| 2 | rice sheaves | L2 jp_s_hasa_* (#51, 5 models); B3b jp_s_straw_stack_stook | L51 1069.4,1025.4; hamlet 974,1012 / 974,1019 / 929,1011.5 |
| 3 | bonsai / pots | L2 jp_s_potted_* (#58, 4 models) | L58 1083.2,1030.3; street 984.6,1076.2 |
| 4 | sword rack | L1 jp_f_katanakake_* (#45) | L45 1088.8,1034.75 |
| 5 | torii rope | B3b/W2 w2kit.torii_rope (torii_wood / torii_stone rope variants), B3b shimenawa | shrine |
| 6 | "hay barrels" | L1 sumi_bale() (charcoal bales: lathe profile starts at r=0.9R, bottom OPEN) used by L1 jp_f_charcoal_* and L2 jp_s_charcoal_bales_*; behind the Kanto farmhouse = jp_s_charcoal_bales_stack (furnish_sets farm_kanto c.site); + every tawara/kamasu | hamlet 967.6,1041.8; Kanto farmhouse back wall |
| 7 | fallen lantern | L2 jp_s_lantern_fallen_* (#72) | L72 1073.4,1030; street 1006.3,1080.6 |
| 8 | loom / wheel float | L1 jp_f_izaribata (#38), jp_f_itoguruma (#37) | L38/L37 shed 3 |
| 9 | leaf litter dots | material jp_m_decal_litter (B1) | everywhere |
| 10 | stone torii texture | jp_s_torii_stone_* material (+ stone lanterns) | shrine S01 1024,1099.5 |
| 11 | two-tone "pot" | jp_s_straw_stack_ab_slumped (B3b) at 970.5,1036.5 (in front of the kura at 975,1041 yaw 270): cylinder with mismatched bands | hamlet |
| 12 | lever well | B3b jp_s_well_hanetsurube_* | hamlet 955,1001 |
| 13 | notice board | B3b jp_s_kosatsu_* (std placed at 1017.5,1087.5) | ward corner south of the graveyard |
| 14 | fire-watch ladder | L2 jp_s_fire_watch_ladder_tower (#68) | street 1033,1086.8 |
| 15 | collapsed torii | new, jp_site 'shrine' mount | - |
| M | jp_m_wall_shikkui_aged | new material for FB1's kura | - |

## For FB1
- **Material: `jp_m_wall_shikkui_aged`** (family wall, `JP\common\materials\wall\jp_m_wall_shikkui_aged_w{0,1,2}`),
  palette `shikkui_aged` [162,163,159] (sampled: c25 aged wall x3 boxes + c03, per-reference mean). 2.0 m tile, v = 0
  at the top of a storey-high wall (rain streaks from the top, grime at the foot); same rvmat finish as shikkui
  ('wall'). _w1 = the default. jp_common.pbo repacked (commit 1a9b8f0).
- **Collapsed torii (finding 15), jp_site, mount `shrine`** (place on the terrain, origin = between the post feet,
  +z = the approach; footprints ~5 x 5 m, the typhoon one ~4 m deep behind the line of the posts):
  - `StaticObj_JP_S_Torii_Fallen_Shinmei_Rot` (wooden shinmei, feet rotted)
  - `StaticObj_JP_S_Torii_Fallen_Myojin_Typhoon` (wooden myojin, blown over backwards: lies on -z)
  - `StaticObj_JP_S_Torii_Fallen_Shu_Snapped` (vermilion: Inari / Hachiman shrines only)
  - `StaticObj_JP_S_Torii_Fallen_Stone_Quake` (stone, span 2.5)
  - `StaticObj_JP_S_Torii_Fallen_Stone_Quake_Old` (stone, span 1.82, mossy, sunk: a long-ago collapse)
- **Fire-watch ladder** is now `Land_JP_S_Fire_Watch_Ladder_Tower` (was StaticObj_...); same p3d, so the .wrp placement
  in test/placements/C3.csv (1033, 1086.8) binds to it with no change. Only needs a world/mission rebuild if FB1 does one
  anyway (the p3d name is unchanged).
- **Loom / wheel:** no placement offsets needed (both models' bases are at y 0; placecheck ok; proxies sit on the
  floors). The loom's floating parts were fixed in the model.

## Forms and choices (finding by finding; general knowledge, no web request made)
- 1 take-boki: bamboo handle ~1.45 m with nodes, branchlet bundle bound twice, fan ~0.46 m; zashiki-boki for the
  shop goods (sorghum fan, three sewn cord rows, square-cut end). Leaf pile + broom models -> box class (343/363).
- 2 hung sheaves: split astride the rail, cut ends + tied neck on top, halves down both sides, ears down and spread,
  golden (_w0); stook sheaves butt down, ears up, tied a third up. View-only soft cover kept (boxes).
- 3 era LIFE_LAYER_ERA #58 followed: pine / satsuki / kiku, unglazed pots (new jp_m_ceramic_earthenware, palette
  earthenware_unglazed [134,98,74] ASSUMED), kiku heads white / yellow / rust (new jp_m_plant_kiku, palette
  kiku_flower ASSUMED). Potted stand -> medium class (1120).
- 4 koshirae: sori 1.8 / 1.2 cm, edge up, hilt to the viewer's left (+x), katana below / wakizashi above; indigo ito
  and sageo, black lacquer saya, horn kojiri; furniture class (932 / 912).
- 5 shimenawa: two left-laid (hidari-nai) strands; tassels as three straw bundles; frayed free ends.
- 10 stone: jp_m_stone_carved_aged (2 m tile, rosette lichen) + per-piece uv turn/shift on all stone torii + lanterns.
- 12 hanetsurube: stone in a 0.75 m sling (rests low, the weight end down), bucket up clear of the curb at rest.
- 14 ladder: vanilla pattern read from farm_watertower_small.p3d (memory ladder1, _con, _con_dir, _dir, _bottom_front,
  _top_front; View Geometry selection ladder1) + ActionEnterLadder (component name 'ladder*', 1.3 m reach, laddertype
  Geometry property). Added a railed lookout deck at 4.90 m to step off onto (no rungs/collision above it).
- 15 causes: wood = rot at the feet / typhoon; stone = the Genroku 1703 / Hoei 1707 quakes.

## Status (checkpoint 2, 10:47)
- Code + masters DONE for all 15 findings + the material. Next: binarize + pack (L1, S1 -> jp_furniture; B3b, L2 ->
  jp_site; materials -> jp_common), restore binarize-noise ODOLs to HEAD, checks, sheet, commit, END.

## Status (checkpoint 1, 10:17; superseded by checkpoint 2 above)
- DONE (code + masters, not yet binarized/packed): 5 rope, 6 charcoal bales, 7 fallen lantern, 8 loom, 9 litter
  decal (material, packed), 10 stone torii/lantern stone, 11 slumped stack, M aged shikkui (packed).
- Before renders: `spikes/FP1/render_fp1.py head <group>` renders HEAD masters rebuilt in the scratchpad
  (`git archive HEAD ... | tar -x`, builds with --no-binarize there); `after` renders current masters. Shots in
  `spikes/FP1/shots.py`; renders cull back faces (as the game draws).
- Pitfalls hit: build_l1.py writes config.cpp WITHOUT S1's classes (298) -> finish furniture with
  `python spikes/S1/build_s1.py <one prop> --pack` (or restore config.cpp); B3b build.py drops L2 -> build_l2 --pack.
