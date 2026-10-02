# FX7 progress: fixes from Stephen's 3c-2 / 3d walk (agent FX7, 2026-10-02)

Time log `japan_dev/TIMELOG_FX7.md` (logger `python spikes/FX7/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Stop rule: weekly usage 88 % -> checkpoint, commit + push, resume note here.

## Status
- [x] 1 checkpoint entry (guardhouse) + entrycheck island-wide
- [x] 2 cargo scale jp_f_kanme_hakari (+ _ab)
- [ ] 3 rock / earth masses (Ishiba, Mabu, Ishibai_Gama, Noborigama)

## 1. The checkpoint "I can't walk in, I need to jump"
- **Measured (spikes/FX7/entrycheck.py):** the culprit is the guardhouse `Land_JP_Bansho_Sekisho_Furnished` (SK2,
  755.28, 871.79). W3D seated it by its back kitchen doma (floorcheck: the ground rises ~6 % north there), so its seat
  is 25.030 while its gravel court (`Land_JP_Oshirasu_Sekisho`, its own flat object) lies at 24.715 = 0.315 under the
  guardhouse grade. The kit's kutsunugi ramp at the inspection front ends at grade + 0.05: a **0.36-0.38 m lip** from
  the gravel (the veranda 0.45 / tatami 0.60 unreachable without a jump). The kitchen front door: the same 0.36-0.38
  over the foundation band. The palisade's two kora-mon sill pads were fine (max rise 0.03), the foot-soldiers'
  guardhouse fine (0.22, its kamachi step).
- **Fix:** `buildings/w3d_sets._court_step()`: cut-stone treads down onto the gravel + the hidden walk ramp (34 deg,
  found.step's rule, Geometry + Roadway stone_ext) carried 5 cm into the court; at the inspection front (two treads,
  visual rises 0.165 / 0.17 / 0.25 / 0.18) and at the kitchen door (one tread). Plain blocks (the hall sits at its R1
  budget 6000). Seats unchanged (floorcheck stays 0, no world rebuild needed).
- **Also found by the check (3d):** the jinya's nagaya-mon room (0.45) had a bare 0.40 step from its doma: D3's
  `dwelling.nagayamon` turned its kamachi frame +90, so the kutsunugi + ramp lay UNDER the room floor. Fixed in the
  template (frame -90 from (XL, 0, 0), same spot) = also D3's samurai / headman nagaya-mon (trivial, same bug).
- **entrycheck (new, spikes/FX7/entrycheck.py):** every placed building / compound (146): a 2.5D walk map (0.10 m)
  from the real terrain + the Geometry of the object and all its placed neighbours (proxies' masters included, door
  leaves open); minimax route (largest single rise) from the terrain 3 m out to every room at its floor level (rooms
  over 1.5 m skipped); compounds without a rooms file: through each gate. STEP_MAX 0.30. Results
  (`_entry_after_fix1.txt`): **3d + 3c-2: 0 failures.** Older waves, LISTED not fixed:
  - D3 `jp_roka_honjin` deck 0.50 (the U9 corridor: deferred, Stephen).
  - W2F town shrine: `jp_shrine_haiden_town_hiwada_furnished` (haiden / en 0.75 unreached, en sides 1.05), 
    `jp_shrine_honden_nagare_town_furnished` (en 1.00: a honden is not entered; its stair may be a check miss),
    `jp_shrine_shamusho_sangawara_furnished` (doma: no free standing cell = furnished full / check artifact, office
    reached 0.11), `jp_shrine_kagura_town_furnished` (stage 1.00 reached with a 0.32 rise: marginal).
  Debug views: `python spikes/FX7/_map.py <stem>` (plan of heights over the seat, # = blocked), `_blk.py`.

## 2. The cargo scale (`jp_f_kanme_hakari` + `_ab`, spikes/W3D/props_w3d.py)
- Rebuilt on a timber tripod (choice + reason recorded in spikes/W3D/W3D_NOTES.md, site 2): the bale hangs 0.43 off
  the ground in a four-rope sling on the iron J-hook, a 2.00 m graduated beam (bronze pins every 0.10, long marks every
  0.50), the counterweight hanging on its loop on the long arm. `_ab`: tripod standing, beam + weight + bale on the
  ground. R1 405 / 215 faces. Build `python spikes/W3D/build_w3d.py jp_f_kanme_hakari` then
  `python spikes/W3D/binsingle.py jp_f_kanme_hakari jp_f_kanme_hakari_ab` (the folder run's binarize crash), pack
  `python tools/assemble_config.py jp_furniture --pack`. propfloat 2/0, propseat 77/0.
- Layout: TY3 re-seated (-0.039, the wider tripod footprint); SK6 (the straw mat on the gravel) moved 0.50 south
  (757.60, 866.60) off the new guardhouse steps (layout_w3d placecheck 0 problems). World + mission rebuilt at the end.
- Renders: spikes/FX7/renders/before_kanme_hakari*.png (W3D), fx7_kanme_hakari*.png (after).
