# Effort test: high (tansu)

Saved by the lead from the high agent's hand-back text (the agent's own Write of REPORT.md was refused by the harness).

## Built
- PBO `@Japan\addons\jp_efftest_high.pbo`, prefix `JP\effort_test\high`, holding config.cpp and two ODOL p3ds.
- CfgPatches `JP_EffTest_high` (requires DZ_Data, JP_Common). Classes `JP_EffTest_high_Tansu`, `JP_EffTest_high_Tansu_Ransacked` (HouseNoDestruct, scope 1).
- Source `src/JP/effort_test/high/`: `config.cpp`, `data/*.p3d`, `data/model.cfg`, `data/jp_f_tansu.loot.json` (last two not packed).
- Spike folder: `tansu.py` (model on the kit's Part/Solid), `build.py` (MLOD, CfgConvert, binarize, pack, checks), `render.py`, `out/*.p3d`, `binarize.log`, `checks.json`, `renders/`, `tansu_sheet.png`.
- Model: origin at footprint centre on floor, +z front. Two carcasses 1.00 x 0.45 x 0.50 m. Five drawers (two half-width, one wide with lock plate, two wide). Iron ring pulls on round plates, corner fittings at the 8 front corners, folding bar carrying handles both sides of each box.
- Ransacked: three drawers pulled out 0.17 / 0.28 / 0.07 m; lower-top drawer on the floor at -5 deg, footprint x +-0.496, z 0.316-0.803 (inside 0.60 m front zone and chest width); empty slot shows divider floor.
- Loot: `loot_top_1`, `loot_top_2` at y 1.00, x +-0.25, range 0.2; ransacked adds `loot_drawer` at y 0.01 inside the dropped drawer.

## Faces per LOD (intact / ransacked)
- Res 1: 792 / 888 (under PLAYBOOK furniture budget of 1,000). Res 2: 234 / 330. Res 3: 42 / 60.
- Shadow Volume 12 / 36. Geometry, View, Fire 12 / 36 each (2 / 6 components). Memory 2 / 3 points.

## Verified offline
- `checks.json` 27/27 pass: C2 material paths from library; C4 carcass 1.000 x 0.450 x 1.000; C5 LOD set complete and in budget; C6 base at y 0 and no collision overlap over 1 cm; collision components closed and convex, mass 45 kg, autocenter 0; loot points per build list, dropped drawer inside front zone; C19 wood matte; C1 palette dE in tolerance.
- CfgConvert passes both ways, MLODs read back, binarize produced both ODOLs with no model messages (only the 8 environment lines also in the machiya log).
- Checks caught two layout bugs, both fixed (dropped drawer through the pulled-out bottom drawer by 6 cm; later 1.8 cm outside the front zone).
- Sheet: 12 Blender renders from the written MLODs (front, 3/4 with 1.8 m figure, back, fittings close-up per state, plus Res 2, Res 3, collision overlay). Three fixes from looking: drawer fronts not separating, plank seam across one front, framing.
- Not tested in game.

## Materials
- Body `jp_m_wood_street_dark_w1`: mean colour 87/59/44, dE 9.0 from timber_interior (tolerance 14); weathered too grey, sooted too black, kuro restricted; matte per T12.
- Dust: up-facing wood faces use `_w2` via a small Part subclass in the script (kit unchanged).
- Carcass front edges use the texture's dark groove band so drawers read as separate fronts.
- Iron `jp_m_metal_iron_w1`, dE 3.5 from iron_black; glossy by design. Fire Geometry vanilla `penetration\wood.rvmat`.

## Decisions
- Geometry property only autocenter=0 (as vanilla case_bedroom_b). Mass 45 kg assumed. Front zone 0.60 m deep (build list gives none). Layout follows the Fukagawa Edo Museum tansu (ref i07). Added a Shadow Volume LOD from the collision boxes (kit doesn't write one). No spec.json dossier; i07 as period reference, N06 for dates.
- Data defect: reference image i35 (Morse) is a saved Wikimedia error page, not a picture.

## Honest self-assessment
- Good: proportions match the reference; drawers read clearly; iron looks right; ransacked state tells the story; LODs step down cleanly; collision exact.
- Weak: plank-wall texture shows pale flecks and coarse grain; lock plate looks like a rusty lump up close; rings faceted; Res 3 barely shows drawers; shadow volume and collision untested in game.
- More time: build `jp_m_wood_interior` and darker iron; proper lock plate shape; spilled cloth in the ransacked state; in-game check.

## Wall-clock
About 15 minutes, 21:35 to 21:50 on 2026-09-29.
