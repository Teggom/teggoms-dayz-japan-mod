# Effort test: max (tansu)

Saved by the lead from the max agent's hand-back text (the agent's own Write of REPORT.md was refused by the harness). Lightly condensed; nothing added.

## Built
- PBO `@Japan\addons\jp_efftest_max.pbo` (140 KB, prefix `JP\effort_test\max`), CfgPatches `JP_EffTest_max` (requires DZ_Data, JP_Common). Classes `JP_EffTest_max_Tansu`, `JP_EffTest_max_Tansu_Ransacked`: HouseNoDestruct, **scope 2**.
- Source `src/JP/effort_test/max/`: `config.cpp`, `jp_f_tansu.p3d`, `jp_f_tansu_ransacked.p3d` (binarized), `jp_f_tansu.json` sidecar.
- Spike folder: `tansu.py`, `build.py`, `render.py`, `render_blend.py`, `spec.json`, `checks.json`, `out/`, `renders/` (incl. `tansu_contact_sheet.png`), `tansu_preview.blend`, `refs_crop/`. Rebuild: `python build.py`, then `python render.py`.
- Model: two boxes 1.00 x 0.45 x 0.50 m, 4 full-width drawers (2 per box, per ref i07). Each drawer: 2 iron ring pulls on hex plates + oval lock plate with keyhole. Iron corner caps on all 16 corners, clasp across the joint, bail handle high on each side of each box. Origin base centre on floor, autocenter=0, +z front.
- Intact: closed, dusty (`_w2`).
- Ransacked: top drawer U1 out 0.155 m; U2 upright on the floor turned 18 deg, slot left as dark cavity; L1 out 0.255 m and droops 6.2 deg (empty drawer's centre of mass is 0.172 m behind its front, tips until rear corner 1 mm under the board above); L2 out 0.05 m.

## Faces per LOD
| State | Res 1 | Res 2 | Res 3 | Geometry | View | Fire |
|---|---|---|---|---|---|---|
| intact | 778 | 246 | 36 | 12 (2 parts) | 12 (2) | 12 (2) |
| ransacked | 874 | 342 | 84 | 60 (10) | 36 (6) | 36 (6) |
- Res 1 face split: ring pulls 368, side handles 120, corner caps 96, locks/keyholes 92, carcass 72, drawer fronts 24, clasp 6, drawer boxes 96 (ransacked). Mass 45 kg.

## Verified offline
- binarize clean, bbox centre (0,0), only the usual "HouseNoDestruct ... creating empty class" note. CfgConvert round trip OK.
- `checks.json` 21/21 intact, 23/23 ransacked, run on files read back: library paths, LOD set, closed convex collision, wood penetration material, budgets, dimensions (1.000/0.450/1.000, joint 0.500), base on floor, overlap <= 1 cm, drawer boxes inside cavities, loot points on a surface with >= 0.25 m clear above, dropped drawer in front zone, matte wood, 6 LODs in binarized files.
- Placement checker (`tools/placecheck`): category prop, centre (0,0,0), lowest point 0.000.
- Palette (`tools/matcheck`): street_dark_w2 vs timber_interior dE 8.8/14; weathered_w2 10.2/14; iron_w1 vs iron_black 1.0/10.
- Blender 5.2 renders from disk with library textures and normals, single-sided faces, no holes. Four fixes from looking: rings and locks doubled in size, dropped drawer turned 9 -> 18 deg, drooping L1 drawer, heavier side handles.
- Not tested in game.

## Materials
- Body `jp_m_wood_street_dark_w2` (closest to the unbuilt interior wood; palette dE 8.8/14). Rejected weathered (nail-holed fence planks; w0/w1 fail palette at 20.3/15.1), sooted (too dark), kuro/bengara (restricted).
- Drawer boxes `wood_weathered_w2` (10.2). Inside faces and keyholes `wood_sooted_w0` (stand-in for shadow). Fittings `metal_iron_w1`. Fire Geometry vanilla `penetration\wood.rvmat`.
- Each drawer front sits between two plank seams so it reads as one board. Later swap: change `WOOD` in `tansu.py`, rerun.

## Decisions
- 4 drawers per ref i07 (medium/high/xhigh used 5). scope 2. No Memory LOD, no Roadway (build list furniture rules); loot recorded in the sidecar: top 2 points range 0.2, ransacked-only 1 point in dropped drawer range 0.15, `lootshelves`.
- Dropped drawer collision is 5 thin parts. Drawer fronts 4 mm back from the carcass face (refs are flush; logged in spec.json).
- Front zones: intact x -0.52..0.52, z 0.225..0.66; ransacked x -0.52..0.66, z 0.225..1.01. Assumed values (45 kg, board thicknesses, fitting sizes) listed in spec.json. Kit code imported read-only.

## In-game check (optional)
Add to the object spawner file (not written: `test/` outside brief paths):
```
{"name":"JP_EffTest_max_Tansu","pos":[1020,25,1000],"ypr":[0,0,0],"scale":1}
{"name":"JP_EffTest_max_Tansu_Ransacked","pos":[1028,25,1000],"ypr":[0,0,0],"scale":1}
```
Pass: both on the ground, iron reads as iron and nothing glows, empty slot dark but not solid black, can't walk through drawers. Unknown until then: colours in game light, LOD switch distances, whether loot spawns in the dropped drawer.

## Honest self-assessment
- Good: reads at a glance as an Edo two-part chest laid out like i07; fittings at the right scale; ransacked version tells a story and stays in its front zone; 44/44 checks.
- Weak: stand-in wood with pale scratch streaks like white strokes on the lower drawers, no extra dust on top; ring pulls use 47% of Res 1 faces; corner fittings plain blocks (no T/L straps, no rivets); dark inside faces are a trick and may go pure black in dim light; drooping drawer's rings tilt with it; nothing seen in game.
- More time: real interior wood + dusty-top variant; fittings atlas to save faces; T-shaped corner straps; spilled clothes once textiles exist; same-angle comparison against i07; a 5-drawer variant.

## Wall-clock
About 33 minutes (21:35:40 to 22:08:53).
