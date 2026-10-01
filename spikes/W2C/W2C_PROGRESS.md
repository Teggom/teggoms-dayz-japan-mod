# W2C progress: Phase C wave 2, civic shells (bare) (agent W2C, 2026-10-01)

Brief: bare shells (no furniture, no island placement): TR01 roadside tea house (3 sizes + the pass tea house),
TR11 smithy + swordsmith, GV1 guard hut, GV7 ward gate (kido) + gatekeeper hut; through buildings/pipeline.py +
registry.py; shellcheck (C1-C22) + bindcheck; research notes spikes/W2C/W2C_NOTES.md; family sheet
research/production/contact_sheets/w2c_family.jpg. Time log `japan_dev/TIMELOG_W2C.md` (logger
`python spikes/W2C/log.py "<event>" "<name>" "<tag>" <5h> <wk>`).

## Done
- Template `parts/kit/jpparts/templates/civic.py` (new; builds on templates/rural.py's Shell, unchanged): kinds
  teahouse, smithy, guardhut, kido; helpers open_front, front_leanto (bench roof), battari, fit (prop spots),
  koshiyane (smoke vent at the roof's ridge), trim_lods (civic far-LOD trim), _attach (merge a second shell: the
  kido-ban hut).
- Kit module `parts/kit/jpparts/gates.py` (new): gate_leaves (hinged pair, one DoorsTwin, two rotation bones),
  kido_head (tie beam + kasagi), kido_roof (cross pieces + purlins for the small gable roof).
- Recipe `buildings/civickit.py`; family folders buildings/teahouse|smithy|guardhut|kido (module civic_shells.py);
  registry block W2C_* (16 entries, ship=True, no placements).
- buildings/shellcheck.py: `door_world_rot` for a passable rotation door (the gate leaves); sliding doors unchanged.
- 16 shells, 738 checks, 0 failures; bindcheck 144/144; jp_buildings.pbo repacked (144 classes).
- Sheet research/production/contact_sheets/w2c_family.jpg (spikes/W2C/render_w2c.py family).

## How to resume
- Build + check a family: `python buildings/pipeline.py <keys> --jobs N` (keys: registry entries with dir teahouse /
  smithy / guardhut / kido); note `--family` takes ONE family (a second --family overrides the first).
- Quick look: `python spikes/W2C/try_civic.py teahouse '{"size": "shop"}'` (faces, budget);
  `python spikes/W2C/tags.py kind '{params}'` (faces per tag); `python spikes/W2C/dbg.py <key> leak|c15|c17 <n>|c12`.
- Renders: `python spikes/W2C/render_w2c.py try --kind kido --params '{"hut": "right"}' --view 3q,back`.
- Everything: `python spikes/FB2/verify_all.py 12`.

## Specialty-prop spots for the furnisher (info['fittings'] in buildings/<family>/rooms/<key>.json)
- smithy: forge (hodo), bellows (fuigo), anvil stump, quench tub, charcoal bin, tool wall
- swordsmith: forge, bellows, anvil, long quench trough, shimenawa over the forge (y given), clay-coating trough,
  blade rack
- tea houses: kamado (the kettle hearth), bench spots (inside the bench shed / under the bench roofs)
- guard huts: brazier, counter / watch hatch under the end shutter, lantern post, tool rack; M: fire ladder on the ridge
- kido: the ward-name lantern under the tie beam (+ the hut's spots, prefixed hut_)

## Commits
- fc6c66b: the whole W2C build (156 files: template, gates.py, recipe, registry, shellcheck, 16 shells' src ODOLs +
  model.cfgs, records / rooms / checks, config.cpp, C_mapgroupproto.xml, spikes/W2C, the sheet, the time log). It
  carries W2P1's message: W2C had staged its paths and W2P1's commit ran in the shared index at that moment. The
  file list is W2C's staged set (156 files); W2P1 may need to commit its own work separately. Pushed to origin/master.
- the follow-up commit with this note, the PUSHED / END time-log lines (committed with explicit paths only).
