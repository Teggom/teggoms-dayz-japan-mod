# FB1 progress: buildings + placement fixes from Stephen's showcase walk (agent FB1, 2026-10-01)

Brief: A-H (doors / binding, second door cause, Kinai roof band, kura doors + colour, roofless street house, farm
tools off the wall, low hill-stair torii, FP1's collapsed torii + ladder / well placement), then checks + a short
TEST_CHECKLIST. Time log `japan_dev/TIMELOG_FB1.md` (logger `python spikes/FB1/log.py "<event>" "<name>" "<tag>" <5h> <wk>`).
FP1 runs at the same time (props + materials); its log is TIMELOG_FP1.md.

## Status
- [x] **A** cause confirmed in both 2026-10-01 logs (server + client RPT: "jp\buildings\...\<p3d>: house, config class
  missing" for exactly the placed buildings whose class != Land_<p3d stem>). bindcheck before: 31 / 128 bind.
  Scheme: p3d named after the class (registry "name" = class minus Land_, lower case; "recipe_name" keeps the old name
  for the recipe, so all 125 family MLODs came out byte-identical). Class names, CE groups, mission, maps unchanged.
  Checks: buildings/bindcheck.py (B1 class == Land_<p3d stem>, B2 shipped p3d has Geometry class=house) in
  pipeline.combine() (the build fails) + one line per building in shellcheck / the generic checks. Full rebuild
  128/128 bind, 128 pass. Commit a138258.
- [x] **B** machiya / shop / toilet: config classes and model.cfg identical to 3d3c46d; ODOL identifier sets (bones,
  selections, memory points, class=house) identical; the packed PBO's machiya = src (byte noise only); the logs show
  the machiya + toilet bound (not in the "config class missing" list). No second cause found on the model side: the
  only placed door buildings that bound were the machiya shop and the toilet.
- [x] **C** Kinai takahe (templates/rural.py _takahe + kinai): no white block under the eave corners, takahe stands
  0.12 over the ridge bundle, the bundle stops inside it. Renders spikes/FB1/renders/c_*_after.png.
- [x] **D** kura leaves 0.11 + 0.025 step (was 0.16 + 0.03), shutters 0.08 (was 0.12) (openings.py LEAF_T / STEP_T /
  SHUT_T); every exterior shikkui face of the 3 kura (+2 furnished) -> jp_m_wall_shikkui_aged (templates/kura.py
  PLASTER_OUT). NEEDS FP1's jp_common.pbo with that material before the walk.
- [ ] **E** not reproduced: D5 (Land_JP_Townhouse_Edo_2ken_Middle_ToriR_Board_Shitate, the middle of the 5 Edo units
  right of S01) has its roof in every visual LOD, front-facing (spikes/FB1/roofwind.py sky census; cullview renders
  with backface culling from the street, the torii and above). Its board roof (jp_m_roof_kokera_w1, silver-grey
  128/133/139) sits 0.17 m below its tiled neighbours and reads like sky. Left for Stephen's re-check with a
  screenshot; a darker board-roof material would be FP1's / a material agent's.
- [x] **F** spikes/FB1/leancheck.py (rays from each wall-anchored prop's back-most point to the building Geometry):
  Kanto tools 0.51 -> 0.006, Kinai tools 0.42 -> 0.006, Kanto charcoal bales, komeya bundle, inn firewood x2 (to the
  posts; D8 forbids more), machiya tenbin, gallery L57 seated. Machiya firewood was already touching a post (kept).
- [x] **G** S70 (stair head) and S63 (stair foot) medium stone torii (nuki 1.93 over the base, 1.66 / 1.81 m clear) ->
  large stone torii (2.60 / 2.79 m clear; spikes/FB1/toriiclear.py); S74 basin moved 0.5 m east to clear it.
  The 11 small sub-shrine torii (S40-S50, before their huts, not on a path) stay low (1.75-2.06 m).
- [ ] **H** waits for FP1's END: collapsed torii, ladder / well placement, world + mission rebuild.
- [ ] checks, checklist, commits

## Found, not fixed (outside the brief)
- Wall-hung life-layer items in the gallery sheds (pegs, calendar, shelves) hang 6.5 cm off the board wall: decor's
  WALL_INSET is 5 mm inside the POST face and the shed's boards sit 6 cm behind it (leancheck). Interior board walls
  dressed by the decorator probably do the same.

## Tools
- spikes/FB1/cullview.py: renders registry buildings from their MLOD with the engine's face orientation and backface
  culling (the C3 / SH1 renders draw both sides). `--lod 2|3`, `--mlod path@x,z,yaw`.
- spikes/FB1/roofwind.py: sky-view census (is the top-most face of every column front-facing?).
- spikes/FB1/leancheck.py: wall-leaning props vs their wall. spikes/FB1/toriiclear.py: head room under every torii.
