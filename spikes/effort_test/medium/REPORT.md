# Effort test: medium (tansu)

Saved by the lead from the medium agent's hand-back text (the agent's own Write of REPORT.md was refused by the harness).

## Built
- Scripts in `spikes/effort_test/medium/`: `build.py` (models, config, CfgConvert, binarize, pack, sidecar), `render.py`
  (Blender previews), `sheet.py` (contact sheet), `jp_f_tansu.json` (sidecar with loot surfaces), `out/` (unbinarized models).
- `src/JP/effort_test/medium/`: `config.cpp`, `jp_efftest_medium_tansu.p3d`, `jp_efftest_medium_tansu_ransacked.p3d` (ODOL).
- PBO: `@Japan\addons\jp_efftest_medium.pbo`. CfgPatches `JP_EffTest_medium` (requires DZ_Data, JP_Common).
- Classes: `JP_EffTest_medium_Tansu`, `JP_EffTest_medium_Tansu_Ransacked` (both HouseNoDestruct, scope 1).

## Model
- 1.00 x 0.45 x 1.00 m, two boxes of 0.50; upper box 3 mm smaller all round so the joint shows.
- Five drawers: lower box two long; upper box one long + two small side by side. Carcass is real boards, so an open drawer shows an empty space.
- Iron: ring pulls (back plate + hanging half-ring), lock plates on two drawers, front corner plates, flat carry bar each side of each box.
- Ransacked: drawers pulled out 0.14 / 0.24 / 0.09 m; bottom drawer stays shut; left small drawer on the floor at (-0.16, 0.60), rotated 17 deg, inside the front zone.
- Memory points: `loot_top_1`, `loot_top_2` at 1.00 m, x +-0.25; `loot_drawer` (ransacked only).

## Faces per LOD
- Res 1/2/3 = 531/197/12 intact, 656/202/36 ransacked (budget 1,500).
- Geometry, View, Fire: 2 boxes (44 kg) intact, 6 (50.5 kg) ransacked.

## Verified offline
- All collision parts pass `component_report` (closed, convex). Geometry has mass, autocenter 0. Fire Geometry uses `dz\data\data\penetration\wood.rvmat`.
- CfgConvert passed incl. round trip (`out/cfgconvert.log`). binarize produced both ODOLs; only the same 8 environment warnings as the machiya (`out/binarize.log`).
- PBO packed; nothing locked the folder.
- Blender renders of the shipped models: front, 3/4, back, fittings close-up, side handle, lower LODs, both states -> `contact_sheet.png`.
- Two fixes after looking at the sheet: removed Blender default cube; thickened the pull rings.
- Not done: palette check script; nothing tested in game.

## Materials
- Body `jp_m_wood_street_dark_w1`: closest to the unbuilt timber_interior colour; weathered wood too light/grey; sooted and kuro woods near black (kuro restricted); w1 wear fits dusty "as left".
- Fittings `jp_m_metal_iron_w1` (named in the build list; glossy by design per 15.3).
- When the interior material exists, swap the path and re-run `build.py` (binarized models embed materials).

## Decisions
- Geometry properties copied from the machiya except map flag set to hide. Each pulled-out drawer and the floor drawer gets its own collision box. No shadow LOD, no model.cfg (matches the kit's buildings). Resolutions 1, 2, 3.

## Honest self-assessment
- Good: reads clearly as a tansu; ransacked state convincing; cheap in faces; every pipeline step clean.
- Weak: pale scratch streaks in the stand-in texture are noisy on drawer fronts up close; rings subtle next to plates; corner plates plain rectangles; no keyhole; no dust shading on top.
- More time: real interior wood material, bigger lighter rings, shaped corner plates, palette and floor-contact check scripts, in-game look beside a vanilla chest of drawers.

## In-game check for Stephen
Spawn both classes in the test yard: size against player; drawers read as drawers; iron not too shiny; can stand in front of ransacked one without snagging; item dropped on top rests at 1.00 m.

## Wall-clock
About 8 minutes (21:35 to 21:43).
