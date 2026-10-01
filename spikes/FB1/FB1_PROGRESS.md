# FB1 progress: buildings + placement fixes from Stephen's showcase walk (agent FB1, 2026-10-01)

Brief: A-H (doors / binding, second door cause, Kinai roof band, kura doors + colour, roofless street house, farm
tools off the wall, low hill-stair torii, FP1's collapsed torii + ladder / well placement), then checks + a short
TEST_CHECKLIST. Time log `japan_dev/TIMELOG_FB1.md` (logger `python spikes/FB1/log.py "<event>" "<name>" "<tag>" <5h> <wk>`).
FP1 runs at the same time (props + materials); its log is TIMELOG_FP1.md.

## Status
- [x] A cause confirmed in both 2026-10-01 logs (server + client RPT: "jp\buildings\...\<p3d>: house, config class
  missing" for exactly the placed buildings whose class != Land_<p3d stem>). bindcheck before: 31 / 128 bind.
- [x] A scheme: p3d named after the class (registry "name" = class minus Land_, lower case; "recipe_name" keeps the
  old name for the recipe so geometry is unchanged). Class names, CE groups, mission files, maps unchanged.
- [x] A checks: buildings/bindcheck.py (B1 class == Land_<p3d stem>, B2 shipped p3d has Geometry class=house); run in
  pipeline.combine() (build fails) + one line per building in shellcheck / the generic checks.
- [x] A 97 old-named src ODOLs git rm'd; full rebuild `python buildings/pipeline.py --jobs 10` (log
  spikes/FB1/pipeline_full.log) - IN PROGRESS
- [x] B machiya / shop / toilet: config classes and model.cfg identical to 3d3c46d; ODOL identifier sets (bones,
  selections, memory points, class=house) identical; the packed PBO's machiya = src (byte noise only); logs show the
  machiya + toilet bound (not in the "config class missing" list). No second cause found on the model side.
- [ ] C Kinai band, [ ] D kura, [ ] E roofless house, [ ] F tools, [ ] G torii, [ ] H FP1 torii + world
- [ ] checks, checklist, commits

## Tools
- spikes/FB1/cullview.py: renders registry buildings from their MLOD with the engine's face orientation and backface
  culling (the C3 / SH1 renders draw both sides).
- spikes/FB1/roofwind.py: sky-view census (is the top-most face of every column front-facing?).
