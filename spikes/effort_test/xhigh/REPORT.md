# Effort test: xhigh (tansu)

Saved by the lead from the xhigh agent's hand-back text (the agent's own Write of REPORT.md was refused by the harness). Lightly condensed; nothing added.

## Built
- PBO `@Japan\addons\jp_efftest_xhigh.pbo` (113,378 bytes, prefix `JP\effort_test\xhigh`); folder not locked.
- CfgPatches `JP_EffTest_xhigh` (requires DZ_Data, JP_Common). Classes `JP_EffTest_xhigh_Tansu` (model `\JP\effort_test\xhigh\jp_f_tansu.p3d`) and `JP_EffTest_xhigh_Tansu_Ransacked` (`jp_f_tansu_ransacked.p3d`), both `HouseNoDestruct`, scope 1.
- Source `src/JP/effort_test/xhigh/`: `config.cpp`, `model.cfg` (not packed), both ODOL p3d, sidecar `jp_f_tansu.json` (not packed).
- Spike folder: `out/` MLOD masters, `tansu.py`, `build.py`, `verify.py` (writes `checks.json`), `render.py`, `spec.json`, `loot_note_mapgroupproto.xml`, `spawn_example.json`, `tansu_contact_sheet.png`.
- Model: origin base centre on floor, autocenter=0, +z front. Two stacked boxes 1.00 x 0.45 x 1.00 m, each 0.50 high; upper box 4 mm smaller at front and sides. Carcass of 2 cm boards. 5 drawers: upper box two small over one wide lock drawer; lower box two wide. Closed fronts 4 mm behind the frame.
- Iron: 8 ring pulls (octagonal plate, staple, flat ring); 3 round lock plates with keyhole; corner plates on the 8 front corners; U-shaped carrying handle each side of both boxes.
- State B: wide lock drawer upright on the floor in front, turned 8 deg, inside the front zone; slot is an empty dark cavity; three drawers pulled out (0.20, 0.18, 0.05 m); one small drawer shut; drawers are real open boxes.

## Faces per LOD (MLOD faces; triangles in brackets)
| LOD | A intact | B ransacked |
|---|---|---|
| Res 1 | 600 (1,200) | 663 (1,326) |
| Res 2 | 155 (310) | 178 (356) |
| Res 3 | 21 (42) | 44 (88) |
| Geometry / View / Fire | 6 faces, 1 component | 54 faces, 9 components |
- Every collision component closed and convex. A is one box (like vanilla case_a); B has body, 3 pulled-drawer boxes, dropped drawer as bottom slab + 4 walls. Mass 45 kg. Only named property autocenter=0. No Memory LOD (build list Q5, binding item 2). No shadow LOD.

## Loot-surface note
In `jp_f_tansu.json` and `loot_note_mapgroupproto.xml`; all `lootshelves`, tag `shelves`: top points at (-0.25, 1.00, 0) and (0.25, 1.00, 0), range 0.20, both states; dropped drawer (0.03, 0.01, 0.70), range 0.15, B only. Front zone x -0.55..0.55, z 0.225..1.125 (0.90 m deep; build list gives no size).

## Verified offline (`checks.json` 49/49)
- binarize (cwd P:\): both ODOL v55; log 42 lines, only the same config noise as the machiya log.
- ODOL read-back with `tools/placecheck/odol_read.py`: autoCenter 0, LOD set matches, bbox y 0.000..1.002, textures library paths.
- CfgConvert of config.cpp and model.cfg round-trips clean. PBO entries, prefix and SHA-1 trailer valid.
- Model checks C1 palette, C2 library materials, C4 dimensions/drawers, C5 LOD set/budgets, C6 base at y=0 / overlap <= 4 mm / loot points / drawer in front zone, C7 closed convex, C8 era lint, C19 matte wood; no degenerate or coplanar-overlapping faces.
- Blender 5.2 renders of the written MLODs with backface culling; 11-panel sheet plus reference strip (i07, i01). Three fixes from looking: plank joints reading as extra drawers (fronts fitted to one board), heavy pale scratch marks, darkest board reading as a black gap.
- Not tested in game.

## Materials
- Body/fronts `jp_m_wood_street_dark_w2` (dE 9.0 from timber_interior, tolerance 14; dusty).
- Carcass inside `jp_m_wood_sooted_w0` (fake darkness); drawer boxes `jp_m_wood_weathered_w1` (paler, reads against fronts); iron `jp_m_metal_iron_w1`. Fire Geometry vanilla `penetration\wood.rvmat`.

## Honest self-assessment
- Good: reads at once as a two-part isho-dansu matching i07/i01; single-board drawer fronts look like furniture; ransacked state clear; light (113 KB PBO); everything checked from the files.
- Weak: stand-in wood lighter and redder than references; no dust film on top; iron plain (square corner caps, octagon pulls); grain stretched about 2x on wide fronts; no spilled clothes (no textile material yet); glossy iron, fake dark cavity and Res 2 dark slot quad not seen in engine.
- More time: real interior wood (material-key swap + rebuild), dust film, iron detail/rivets/proper pull, spilled clothes, one in-game look.

## In-game checklist for Stephen
1. Copy `spawn_example.json` into `test/spawns/` (not done: outside brief paths); load @Japan.
2. Walk about 20 m NE of spawn (1024, 985) to (1040, 1000) and (1043, 1000); both face south.
3. Pass: on the ground, wood not too red, iron not too shiny, collision blocks you (incl. dropped drawer), LOD switch at 10-30 m not jarring.
Loot points only testable once a house proxies the tansu.

## Unknown
Whether the object spawner accepts these scope-1 statics; engine lighting of the cavity and iron; real LOD switch distances; whether a player can step over the dropped drawer's 0.25 m walls.

## Wall-clock
About 35 minutes (21:35 to about 22:10), including three look-and-fix passes.
