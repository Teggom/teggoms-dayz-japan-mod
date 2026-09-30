# Effort test brief: one prop, four effort levels (lead, 2026-09-29)

Stephen wants to compare the same task at 4 reasoning-effort levels: tokens burned and final quality. Four agents get
this identical brief. Only `<LEVEL>` (medium / high / xhigh / max) and the folders differ. **Work independently. Never
read or copy another level's folder.**

## Project and rules
- **Project:** the Feudal Japan DayZ mod, `D:\DayZ-Server_AI-20260907-MultiMap\japan_dev`
- **Read `README.md`**: "Rules for every agent (hard)" applies:
  - never start, stop or kill any game, server or GUI program (headless `blender.exe --background`, `binarize.exe`,
    `CfgConvert.exe`, `ImageToPAA.exe` and python are fine)
  - no git
  - Python writes in binary mode with LF
  - bounded reads: measure big files first
  - no web access needed; if you use it, never put personal information in a request
- Check `P:` first (`Test-Path P:\DZ`; if missing, `subst P: D:\DayZToolsExtract`). `P:\JP` is a junction to
  `japan_dev\src\JP`.

## The task: build ONE prop, the tansu (clothing chest of drawers), in two states
- **The spec** is `research/interior/BUILD_LIST.md`, row 26, `jp_f_tansu`. Also read that file's top decisions and
  PLAYBOOK §15.3.
  - Two stacked boxes (isho-dansu), about 1.00 × 0.45 × 1.00 m (two parts of 0.50), 4–5 drawers, iron ring pulls,
    carrying handles on the sides, wood body, iron fittings. In 1730 it's still costly: T2–3 houses.
  - **State A, intact:** closed, weathered and dusty ("as left" for 0–2 years).
  - **State B, ransacked:** drawers pulled out, one lying on the floor in front (inside the tansu's front zone).
- **Materials:** the interior materials (e.g. `jp_m_wood_interior`) are NOT built yet. Use the closest existing
  jp_common materials under `src/JP/common/materials/` (wood and metal families), and note your choice.
- **Look:** follow `playbook/PLAYBOOK.md` §8–9 (palette, materials), §12 (checks), §15 (lessons, incl. the 15.3 matte
  recipe). Research level: standard (§11).
- **How:** reuse the project's tools. `tools/common/mlod.py` (MLOD writer), `tools/common/pbo.py` (PBO packer) and
  `parts/kit/jpparts/mlod.py`. `buildings/machiya_t3_01/build.py` shows the binarize → pack flow (cwd `P:\`). Read
  them, but don't modify `tools/common/` or `parts/`.
- **LODs:**
  - visual LODs (at least 2 resolutions)
  - Geometry (closed, convex components, with mass)
  - View Geometry, Fire Geometry
  - memory points as needed
  - a loot-surface note per the build-list row (the top at 1.00 m: 2 points)
  
  Budget: at most 1,500 faces for the best LOD. Simple is better if it looks right.
- **Config:** one PBO `jp_efftest_<LEVEL>.pbo` with CfgPatches `JP_EffTest_<LEVEL>` (requiredAddons: DZ_Data +
  anything you need) and two placeable static classes, `JP_EffTest_<LEVEL>_Tansu` and
  `JP_EffTest_<LEVEL>_Tansu_Ransacked`. Pack it into `..\@Japan\addons\`. If a running server locks the folder, report
  it and leave the PBO in your spike folder.
- **Verify offline:**
  - binarize clean (log)
  - CfgConvert the config
  - render previews in Blender (front, 3/4, back, close-up of the fittings; both states) into one contact sheet PNG
  - **LOOK at the sheet** (Read the PNG) and fix what's wrong before you finish

## Write only here
- `spikes/effort_test/<LEVEL>/`: scripts, .blend, renders, `REPORT.md`
- `src/JP/effort_test/<LEVEL>/`: game-ready source
- `..\@Japan\addons\jp_efftest_<LEVEL>.pbo`

## REPORT.md (in your spike folder)
- **Built:** files and classes
- **Faces per LOD**
- **Verified offline:** how
- **Materials used and why**
- **Honest self-assessment:** what looks good, what's weak, what you'd do with more time
- **Wall-clock time** spent

## Final message: 150 words or fewer
Faces, verification result, the contact-sheet path, and a one-line self-assessment.
