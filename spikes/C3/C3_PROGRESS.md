# C3 progress: Phase C wave 1, kura + furnishing + dressing + the walk (agent C3, 2026-09-30)

Brief: the kura (DW22) shells; one or two furnished variants per wave-1 type (the machiya-shop pattern); swap them
into the C1 street and the C2 hamlet and dress both; re-run every check; render sheets; ONE bundled walk in
TEST_CHECKLIST.md. Time log: `japan_dev/TIMELOG_C3.md` (logger `python spikes/C3/tlog.py "<event>" "<name>" "<tag>"
<5h> <wk>`).

## Status: DONE (built, binarized, packed, on the island; untested in game)

### Kura (DW22)
- `parts/kit/jpparts/templates/kura.py` + `buildings/kurakit.py` + family `buildings/kura` (registry C3_KURA):
  Land_JP_Kura_Namako, Land_JP_Kura_Kuro_Hinged, Land_JP_Kura_Plain. 3 x 2 ken, 0.24 okabe (shikkui outside,
  jp_m_wall_shikkui_int inside), one-course cut-block footing, plastered eave bands + soffit + fascia + bargeboards,
  kura door (inner sliding game door + outer plaster leaves: static open / ROTATION doors in _Kuro_Hinged), kura
  windows (static, C11 portals), two floors (0.45 / 2.85) by jp_p_stair _open with a railed stairwell, sangawara
  only (hongawara is a status roof). Budget 'standard': worst R1 5,532 / R2 1,531 / R3 635. 115 checks, 0 failures.

### Furnished variants (14; registry C3_FURNISHED, family `buildings/furnished`)
- `buildings/furnishkit.py`: a furnished variant = the base registry shell's recipe with the SAME params + fittings
  (`parts/kit/jpparts/fittings.py`: jp_p_fit_kamado, promoted from the machiya, on C2's kamado spots / in town
  kitchens) + props as proxies (decor) + loot on floors and prop surfaces + site() yard / street objects.
  `buildings/furnish_sets.py`: 13 dressings. `buildings/shellcheck.py` runs decor.check_all (D1-D16) on them.
- Kamigata 3k Komeya (rice), Kamigata 2k Kamiya (paper), Edo 2k Gofuku (cloth), Edo 3k corner Sakaya (sake),
  post-town Home (T2), Hatago_Std_Tile (T2), Hatago_Grand (T3, upstairs rooms), Kanto + Kinai farmhouses (T2),
  hut east + west (T1), walled shed, kura namako + kura kuro hinged. 1,341 checks, 0 failures. Per room 5-7 counted
  props, >= 1 raised loot surface, life-layer items on walls / beams / surfaces (`python spikes/C3/summary.py`).

### Island
- C3_SWAP: 12 bare shells replaced by their furnished variants on the C1 street and C2 hamlet; kura at
  (1000, 1097.5) behind the Kamigata row and (975, 1041) in the hamlet. Bare on purpose: Kamigata 3k end + corner,
  Edo 2k end + 3k board middle, post-town row middle + end, the small mushiro hut, the open thatch shed.
- `spikes/C3/dress_island.py` -> test/placements/C3.csv: 33 street + 26 hamlet objects (its own overlap / door-apron
  / reserved-spot checks: 0 problems). World + mission rebuilt, verify_oprw PASS 3689/3689.
- placecheck: 93 flags (35 before). The new ones are by design: gutter covers sunk (they need a ditch), buried posts
  (scarecrow, tie post, crossroads lantern, stones), eaves pieces hanging (persimmon curtains, sandals), tilted fallen
  props (palanquin, spilled loads) with one corner 4-5 cm up.

### Re-runs
- 105 earlier buildings, 6,001 checks, 0 failures: machiya 78/78, shop 137/137, toilet 19/19, C1 81 shells, C2 21
  shells; combos 60/60. Prop suites (B3a, L1, B3b, L2, TXT) not re-run: no prop / decor code changed.

### Sheets (research/production/contact_sheets/)
c3_kura.jpg, c3_rooms.jpg (every furnished room), c3_plans.jpg (loot plans), c3_street.jpg, c3_hamlet.jpg.

### Decisions I made
- A furnished variant rebuilds the base recipe rather than copying the p3d, so the shell stays byte-for-byte the same
  shell and the variant carries its own fittings; the kamado is merged geometry on the variant only.
- Wall-anchored props sit 5 mm inside the post face (decor D10 Roadway lookup at the edge).
- Walk-on props (laid futon, straw beds) join the floor's loot obstacles so no floor loot spawns under them.
- The townhouse mise keeps its tatami (no board display strip): a new floor recipe would change the shell.
- The kura's hinged leaves are separate doors (doorstwin2 / 3); shellcheck measures the inner door with them open.
- Ground-floor kura window on the back wall (the namako on the front and gables has no holes).
- KEEP_TRADES' 22 shop sets don't exist yet: trades come from existing goods + life-layer items.

### Not done / open
- Navmesh not regenerated (GUI step): zombies can't path in the new interiors.
- Engine-untested: the kura rotation leaves, every furnished interior.

## How to resume / rerun
- One variant: `python buildings/pipeline.py f_<key> --no-pack`; all C3: the C3_KURA + C3_FURNISHED keys --jobs 8.
- Island: `python spikes/C3/dress_island.py`, then T's build_world.py, build_mission.py, tools/verify_oprw.py.
- Re-runs: `python spikes/C3/rerun_all.py 12`. Renders: `python spikes/C3/render_c3.py [set] --jobs 8`.
