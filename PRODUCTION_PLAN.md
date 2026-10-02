# Production plan: from the catalogue to built content (lead + Stephen, 2026-09-29)

**Start here if you are a fresh session.** This is the agreed order of work after the 2026-09-29 research and review.
`README.md` holds the hard rules for every agent. This file holds WHAT to build next and in what order.

## Where we are (2026-09-29)

- **One building proven in game:** `buildings/machiya_t3_01` (Land_JP_Machiya_T3_01), passed gate G3 after two fix
  passes. The lessons are in PLAYBOOK §15.
- **The parts kit:** `parts/kit/` (generator), `parts/manifest.json` (129+ variants), `parts/REPORT.txt`.
- **The material library:** `research/materials/` → `src/JP/common/materials/`. Matte recipe: PLAYBOOK §15.3.
- **Research done** (text only): `research/REVIEW_INDEX.md` indexes it all. That's the building list (682 types), the
  outdoor list (1,706), 217 named landmarks, the route gap audit and the Chernarus baseline.
- **The catalogue is decided:** Stephen's five review sittings produced the KEEP lists in `research/catalogue/`:

| File | What |
|---|---|
| `KEEP_DWELLINGS.md` | 30 core shells + 12 ☆ stretch; townhouses as snap-together units |
| `KEEP_TRADES.md` | 32 core shells + 22 townhouse dressing sets + 18 ☆; sake shops, pleasure quarters, theatre, mines |
| `KEEP_CIVIC.md` | 44 core + 15 ☆; the wall kit; one castle keep with authentic swaps; 4 + 4 micro-shrines |
| `KEEP_OUTDOOR.md` | ~320 items incl. 55 trees + 7 tall bamboos; AUTUMN season; stand recipes; period traps binding |
| `KEEP_LANDMARKS.md` | Top 20 + hero builds + famous bridges; 3 volcanoes; 4 checkpoints; dead-world dressing |

- **The map sketch:** `research/map_sketch/` (`python map_sketch.py diag` → a 20.48 km square, Osaka SW → Edo NE along
  the diagonal, 70 real villages, 12 real in-between roads). The map is PAUSED. Stephen wants more horizontal
  in-between roads later. Size and terrain-tool scaling are set aside for now (Stephen: "size doesn't matter, ignore
  that for now").

## Standing decisions (Stephen, 2026-09-29): apply to every task

- **Ignore loot tiers entirely for now.** Map and items first.
- **Loot lies OUT on floors and surfaces,** like vanilla DayZ. Furniture is dressing, not containers. Containers are
  rare.
- **Dead world:** empty towns like Chernarus. No NPC crowds or lords; maybe bandits later. Everything is dressed "as it
  was left".
- **Era test:** did it exist, or still stand, in 1730? Older survivors are IN (PLAYBOOK §1).
- **Season:** autumn.
- **Cost rule:** a shell assembled from existing kit parts is cheap. New PARTS and PROPS are the lift. ☆ stretch items
  are cut first if shells turn out slow.
- **Process:** ask Stephen before launching agents; only Opus agents; bundle his in-game checks.

## The order

### Phase A: plan (research only; 3 agents in parallel) — DONE 2026-09-29; G1 PASSED (research/catalogue/G1_DECISIONS.md)
| Task | Owner | Output |
|---|---|---|
| **A1. Parts-kit gap audit.** Every KEEP shell against the kit: which are buildable today, which parts are missing (ranked by how many shells need each), and the variant axes per shell (the doors, windows, lattice and roof swaps that give Stephen's variety) | agent PA1 | `research/production/PARTS_GAP_AUDIT.md` + `parts_gap.json` |
| **A2. Interior build list.** Scoped to the KEEP rooms. Interior materials (tatami, floor boards, doma, interior shikkui, ceiling), built-in fittings (tokonoma, shelves, irori, kamado, agari-kamachi, kutsunugi stone), the interior core props with sizes, loot surfaces, abandoned states, and Q5 (which LODs vanilla puts furniture proxies in) | agent PA2 | `research/interior/` in the exterior build-list format |
| **A3. Outdoor core kit build list.** The ~25 most-shared outdoor items (KEEP_OUTDOOR "build first") with sizes, references, materials, variants and abandoned states | agent PA3 | `research/outdoor_kit/` in the same format |

→ **Gate: Stephen reviews the three build lists** (G1, about 10 minutes each).

### Phase B: foundations (after the A gate; agents at effort high, `opus-high`)
0. **B0. Kit cleanup (A1 step 0a + 0b + the townhouse-unit template from 0c). FIRST; nothing new is built before it.**
   Move the machiya's floors, lean-to, udatsu placer and ridge walk into `jpparts` (lean-to learns all six coverings);
   replace the one-building `build.py` with a registry that builds many buildings without overwriting the others'
   config, placements and CE files; add the townhouse-unit template (frontage, end / middle / corner) as the test bed
   for B2 parts 2-4. Proof: rebuild the machiya and get an identical result (`verify.py` 78/78 PASS).
1. **B1. Interior materials** (through the materials pipeline and the matte recipe): the 21 interior materials
   (incl. `jp_m_wall_shikkui_int`) plus the outdoor kit's new ones (moss decal, weathered granite, straw rope). Needs
   nothing; runs alongside B0.
2. **B2. Missing parts, wave 1** (after B0): koyagumi first, then party wall, party roof end, roof corner, stall,
   stair, open half-door (required: toilets are walk-in), then the floor pit as optional variety.
3. **B3a / B3b. Core props, wave 1** (need nothing; run alongside B0 and B1): 24 interior (A2) and about 20 outdoor
   (A3), each with its abandoned state. B3b includes the handcart disrepair variants and the Japanese brush-font
   signs. **Each agent owns its own output folder; nobody edits the shared materials registry or config except B1.**
4. **B4. Pilot** (after B0, B1, B3a AND B3b): furnish `machiya_t3_01` and dress its yard, including the regenerated mise
   floor with the board strip (needs B0's `floors`). This proves the props, proxy and loot-surface pipeline on a
   building Stephen already knows.

→ **Gate G4: one in-game walk** of the furnished house.

### Phase C: shell waves (each ends in ONE bundled walk-through)
1. **Wave 1, the most-placed shells (~10–12):**
   - Kantō and Kinai farmhouses; poor huts (east 1 + west 30)
   - Edo and Kamigata townhouse units; the post-town house
   - the inn (hatago)
   - the kura, shed, toilet and roofed well
2. **Wave 2:**
   - the shrine ladder, the temple ladder
   - guard hut, gates and walls
   - smithy, roadside tea house
3. **Wave 3+:**
   - the other trades with their own props (the brewery is the big one)
   - the castle kit
   - then the ☆ stretch shells
4. **Landmarks last:** built from finished shells + dressing.

**Specialty props are built WITH the shell that needs them, not up front.** A cut shell never pays for its props.

### Confirmed future work (Stephen, 2026-09-30; not scheduled yet)
- **Japanese infected:** already decided in FEASIBILITY §9 (option a: new Japanese-dressed infected; AI ronin / bandit
  bands later). Not yet in this work order.
- **Food overhaul:** period food replaces vanilla food (not discussed in detail yet).
- **Cooking:** the irori and kamado become working fire/cooking spots (like the well); research a traditional
  Japanese open-fire / campfire form to remake the vanilla campfire model.
- **Audio:** ambient sound with animals that actually live in Japan (no American owl), Japanese-flavoured
  sounds where it makes sense (e.g. weapon-swing grunts); reuse vanilla where it already fits.
- Not worried yet: navmesh, the map (both planned), performance at scale.
- **The A4 audit backlog: ALL items accepted** (Stephen, 2026-09-30: "I like all of the gaps"). Source:
  `research/AUDIT_MISSING.md` (Part 1: 17 missing + 8 planned-with-gap DayZ systems; Part 2: 9 missing Japanese
  details + the wrong sakura). Its top 10: (1) remake the sakura as yamazakura / edohigan in autumn leaf (the built
  ones are banned Somei-yoshino in bloom) + check the bamboo reads as madake; (2) strip vanilla items, start a JP
  types.xml; (3) spawn gear; (4) the food list; (5) medical / tools / containers lists; (6) the animal roster (sika,
  serow, black bear; no sheep / reindeer / dairy cows); (7) period dynamic events (baggage train, cargo-ship wreck,
  burned house, battle camp); (8) autumn landscape (pine avenues, ichirizuka, higanbana + susuki, fruiting persimmons);
  (9) weather / time config + footstep sounds per surface, and fix FEASIBILITY §5's "Spring"; (10) the unpicked shrine
  and village items (ema, straw village guardians, roku-jizo, ward gates, fire lookout, sugidama, sozu). Order not
  picked yet.
- **W2's material gaps, accepted** (do after S1, which owns materials until it finishes): more posthumous-name cells
  in the carved-text atlas (grave variety), Sanskrit seed syllables for the gorinto / hokyointo stones (built blank),
  an outdoor bare-earth material for grave mounds (they use leaf litter now).
- **More wooden grave posts (bohyo): DONE** (W3, 163k / 7 min): 6 variants (_bohyo_new, _bohyo_s, _bohyo_roof,
  _ab_bohyo_lean, _ab_bohyo_split, _ab_bohyo_rotted), roof cap era IN but uncommon (~1 in 8; W2_ERA.md W5),
  jp_site.pbo 307 classes. Commits 15c1c8a, 411f75b. Material gaps added to the list above: a pale NEW-wood and a true
  silver-grey weathered wood (the new vs grey posts differ little now), ink posthumous names (new sumi cells).
  Lead note: binarize rewrites every ODOL with byte noise; 169 unchanged site models were restored to HEAD (no geometry
  change) to keep the repo clean.
- **Modular host variants for corridors (end of production)** (Stephen, 2026-10-02, after walking 3a): do NOT fix
  corridor-to-host joins building by building now. Once the host designs are final (end of production, like the
  duplicate thatched-roof variants), make the modular host variants: duplicate the final hall, open the railing / wall
  where each corridor meets it, align the corridor to it, and add the stair where the floors differ. His reasoning:
  host buildings with openings made now would mean e.g. 8 shrine / hall variants with different railing openings,
  and every later design change would then have to be made 8 times. The case that raised it, the town temple
  corridor **U9** (`Land_JP_Roka_Temple_U`, hondo U1 east veranda -> kuri U2), left exactly as built until then:
  (1) the hall's veranda railing was never opened, so the corridor is fenced off at the veranda; (2) its far end stops
  short of the kuri's genkan porch and is misaligned with it; (3) the level change is a 0.70 m step-off instead of a
  stair (K3's stair broke the connector fit on a 2-ken run). The honjin corridor **J3** (`Land_JP_Roka_Honjin`,
  omote <-> oku, both floors 0.50, connected both ends) worked: Stephen did not flag it. K3_NOTES.md §6 points here.
- **Fishing industry suite (must-have)** (Stephen, 2026-10-02: "Japan was a massive fishing industry, so having
  accurate boats in towns or docks or near the shore is a must"). Today the pieces are scattered and mostly unbuilt:
  the coastal house (built in 3a, with net store + a beached boat), KEEP_DWELLINGS beach hut (ama-goya), boat shed
  (funa-goya), net shed; KEEP_OUTDOOR "Shore and salt" (16: beached boats, net and fish racks) and "Canals and boats"
  (8); KEEP_TRADES fishmonger, boatbuilder's yard (☆), river fish weir house (☆); G1 site type g (shore landing:
  harbour, beach, lake shore); the Nihonbashi fish market (landmark). Make it ONE planned suite, researched first
  (sourced, 1730 era test) and built as its own wave once there is a shore to place it on: **period-accurate boats**
  (small coastal and river fishing boats, a ferry, a lighter / cargo boat, the big coastal freighter as a
  landmark-scale piece; beached, moored and abandoned / wrecked states), **landings** (beach slipways, stone landing
  steps, timber jetties / piers, mooring posts), **the fishing village** (net boss compound with net stores, net
  drying and mending racks, fish-drying racks, processing sheds such as dried-fish / fish-fertiliser / bonito works if
  they pass the era test, boat sheds, the fish market / wholesaler), **river and lake fishing** (weirs, traps,
  cormorant-fishing kit if in era), and the props (nets, floats, baskets, rods, oars, the sculling oar, anchors,
  lanterns). Placement needs a shore: the test island has none near the showcase, so either a shore district on the
  test island or wait for the map. Not scheduled yet; Stephen picks when.

### Parked (not in this plan until Stephen raises them)
- Terrain-tool size test; the real map build; more horizontal in-between roads
- Wardrobe rework, weapon carry offsets, the bamboo two-handed hold (OPEN_ISSUES)
- Fauna, seasons beyond autumn, the Nishijin burn scar, loot tiers, bandits

## Log
- 2026-09-29: plan agreed; Phase A launched (PA1, PA2, PA3).
- 2026-09-29: Phase A done.
  - **A1** `research/production/PARTS_GAP_AUDIT.md`: 15/104 core shells buildable now; koyagumi (visible roof framing)
    is the top missing part; step 0 = move the machiya's floor, lean-to and udatsu helpers into the kit and replace
    the single-building build.py; 4 rulings for Stephen.
  - **A2** `research/interior/BUILD_LIST.md`: 13 fittings, 36 props (24 wave 1), 21 materials, Q5 answered; 14
    decisions.
  - **A3** `research/outdoor_kit/BUILD_LIST.md`: 27 items / 162 variant models; 11 decisions. 31 reference images are
    pending: rerun `research/outdoor_kit/tools/fetch_refs.py` (Wikimedia 429'd), then `gen_build_list.py`.
- 2026-09-29: G1 passed. All 29 decisions and rulings are in `research/catalogue/G1_DECISIONS.md` (binding for Phase B).
- 2026-09-29: **Effort test PENDING (run before Phase B).** Stephen wants to compare the same task at 4 reasoning-effort
  levels (tokens + quality).
  - **Set up:** agent types `opus-medium`, `opus-high`, `opus-xhigh`, `opus-max` in
    `D:\DayZ-Server_AI-20260907-MultiMap\.claude\agents\` (frontmatter `effort:`). The brief is
    `spikes/effort_test/BRIEF.md`: one prop, the tansu, intact + ransacked, into `spikes/effort_test/<level>/`.
  - **Blocked:** the agents folder didn't exist when the session started, so the new types only load after a SESSION
    RESTART.
  - **After the restart:** launch the 4 in parallel (subagent_type `opus-<level>`, prompt = "LEVEL = <level>, follow
    BRIEF.md"), then compare subagent_tokens and the contact sheets.
  - The session itself runs at effort xhigh. Earlier general-purpose agents most likely inherited that.
  - Also on restart: check `data/research_okit/slow_fetch.log`. If the image downloader died, rerun
    `python research/outdoor_kit/tools/slow_fetch.py` in the background (it's resumable).
- 2026-09-29: Outdoor kit refs sorted.
  - Wikimedia blocks our downloader, so Stephen saved 21 by hand (7 flagged weak in meta.json); 16 Morse figures + an
    LoC festival print were added; straw_aged sampled.
- 2026-09-29: **Waterway research (agent WW) launched** → `research/waterways/`: ~6 town waterway types (city canal,
  shallow canal, big river, street channel, village stream, moat) with cross-sections, edges, planting, bridges and
  house frontage, plus EVERY map settlement assigned a type (Stephen: "each city we have will need to fall into one of
  these categories"). A G1-style review for Stephen when done.
- 2026-09-29: **Effort test RESULT.** Tokens: medium 164k, high 252k, xhigh 438k, max 450k. In game, Stephen found
  **high** "looks pretty good" and about the same as xhigh at ~42% fewer tokens.
  **POLICY: every modelling/building agent runs at effort HIGH** (`subagent_type: opus-high`, defined in
  `D:\DayZ-Server_AI-20260907-MultiMap\.claude\agents\`). The four tansus stay on the test island
  (`test/spawns/E.json`) as reference.
- 2026-09-29: Phase B breakdown agreed with Stephen (B0, B1, B2, B3a, B3b, B4); B0 gained the townhouse-unit template
  and B4 gained the B3b + mise-floor dependencies. Not launched yet.
- 2026-09-29: **B0 and B1 DONE** (opus-high; B0 409k tokens / 50 min, B1 453k / 39 min). B3a/B3b held back (usage window).
  - **B0:** helpers in `jpparts` (floors, leanto x6 coverings, udatsu, ridge walk, `assemble.Builder`); multi-building
    pipeline `python buildings/pipeline.py [key...]` + `buildings/registry.py`; townhouse template
    `jpparts/templates/townhouse.py` with 4 placeholder hooks for B2. Machiya 78/78, outputs byte-identical. C19 reads
    the material `finish` field. Commits 0ef810a, 49daa03, 4ce8b31, 07ab8d1.
  - **B1:** 34 materials x 3 wears (16 of the 50 named already existed), both text atlases (fonts in `research/fonts/`,
    Yuji Syuku + Yuji Hentaigana Akebono, OFL), jp_common.pbo repacked. Sheets in
    `research/materials/contact_sheets/b1_*.jpg`. Commits ec9f6a8, 73d2165, ee28a45.
  - **Open for Stephen:** townhouse unit face budget (test unit 8,062 faces vs the standard 6,000; audit §6 risk 2);
    the doma floor is bright (137,132,128 vs vanilla 76-127), judge at G4; a faded-red jizō-bib cloth and a brown heri
    still need palette entries (the bib is B3b's).
- 2026-09-29: Townhouse face budget class added (Stephen): 9,000 / 3,450 / 1,200 (PLAYBOOK §12, registry `townhouse`).
- 2026-09-30: **B2 DONE** (opus-high, 715k tokens / 72 min). Commits c2f1bb6, de169eb, af6a588; detail in `parts/B2_PROGRESS.md`.
  - 10 parts, 0 check failures: koyagumi (7 variants + sooted), party wall, party roof end, pent corner, seam cap
    (townhouse hooks all filled), stall, stair, half door, floor pit, sunoko.
  - Machiya 78/78, MLOD byte-identical. All 60 townhouse combos build; test unit 41/41 at 7,912 faces; toilet 17/17.
  - Kit fixes: C13/C16 on non-tile roofs, half-door portal in C11, board eaves in every LOD (9 board-roof sample parts
    changed), gable vents under the roof line (3 samples changed).
  - **Open for Stephen:** 8 combos over the townhouse budget, all Kamigata 4-ken end/corner (worst 10,468 / 3,687 /
    1,342); raise the budget for 4-ken Kamigata, or trim them. _tile/_kura gables leave 0.12 m slits at the post lines
    (fixing it changes the machiya). Engawa and kura-eave corners not built. The half door is untested in the engine.
  - B3a (interior props) next, on Stephen's go; B3b after.
- 2026-09-30: Stephen's calls on the B2 open items:
  - Kamigata 4-ken end/corner units may be over: `townhouse.budget_class()` gives them 'large'; combos 60/60 clean.
  - Gable slits FIXED in `walls.gable` (_tile/_kura infill now continuous). This changes the machiya: rebuilt, 78/78,
    PBO repacked. **Check the machiya's gable ends (loft) at the G4 walk.**
  - The half door gets tested in game later (next walk).
- 2026-09-30: **B3a DONE** (opus-high, 498k tokens / 42 min; TOKEN_LOG.md, TIMELOG_B3a.md). 24 props = 110 models
  (24 new, 36 variants, 50 abandoned), all checks pass, 62 loot surfaces in the `.prop.json` sidecars;
  `@Japan/addons/jp_furniture.pbo` (JP_Furniture, `StaticObj_JP_F_*`). Pipeline in `spikes/B3a/`; progress + B3b
  reuse notes in `src/JP/furniture/B3a_PROGRESS.md`; sheets `research/interior/contact_sheets/b3a_*.jpg`.
  Commits 564eec5, 940d634, 4409d95, e80c005, 64a5b3b. Untested in game.
  - Gaps: no rice/grain material (spills use paper), kori wicker looks pale grey in bamboo_weave, firewood redder
    than ref i22. Refs i31/i35/i38 are saved HTML error pages.
- 2026-09-30: **B3b DONE** (opus-high, 519k tokens / 40 min). 20 outdoor items = 129 models (20 new, 80 variants,
  29 abandoned; 7 over the list: 6 separate shape signs, handcart `_ab_wreck`, shop-front `_ab_kanban_askew`); all
  checks pass, max 828 faces. `@Japan/addons/jp_site.pbo` (JP_Site, 121 `StaticObj_JP_S_*` + 8 `Land_JP_S_Well_*`).
  Wells copy vanilla's pump well (HouseNoDestruct + script class `extends Well`, in
  `src/JP/site/scripts/4_World/JP_Site/jp_site_wells.c`); all pulley variants incl. `_roofed` are wells, the lever
  well's `_field` sweep isn't. Material added: `jp_m_textile_bib_red` (palette `bib_red_faded`). Pipeline
  `spikes/B3b/`, progress `src/JP/site/B3b_PROGRESS.md`, sheets `research/outdoor_kit/contact_sheets/b3b_*.jpg`.
  Commits aeb23e9 .. c5a7dbe. Untested in game.
  - **In-game checks:** crouch at a well curb: drink, wash hands, fill a bottle.
  - Open: gutter pieces need a terrain ditch cut (terrain/placement work); notice boards reuse crops of the one edict
    text in the atlas; rice stooks and rope tassels render thin.
  - **Phase B next: B4 pilot** (furnish machiya_t3_01 + dress its yard + the mise-floor board strip), then gate G4.
- 2026-09-30: **B4 DONE** (opus-high, 576k tokens / 69 min). Commits be762bc, dd18e5f; `buildings/machiya_t3_01/B4_PROGRESS.md`.
  - The furnished house is its own p3d `Land_JP_Machiya_T3_01_Shop` on the machiya's spot (the bare shell stays in the
    PBO, unplaced). 32 room props (5-7 a room) as proxies in the vanilla LODs (Q5) + 5 shop-front proxies; 43 loot
    points (12 floor, 31 raised), none above 1.40 m. New kit: `jpparts/decor.py` + `proxies.py`.
  - Mise floor: 0.455 board strip. The machiya now uses B1's floor materials (judge the doma colour at G4).
  - Checks: shell 78/78, furnished 137/137 (78 + 59 decorator checks), toilet 19/19, townhouse combos 60/60.
  - Yard + street: 17 map objects incl. the pulley well; B2's toilet shipped as `Land_JP_Toilet_T1_01`. Test island
    world + mission rebuilt; a WaterBottle added to the item grid for the well test.
  - Not done: navmesh (GUI step); no sandal prop (life layer covers it); the machiya's old render sheet.
  - **Gate G4 = Stephen's walk: TEST_CHECKLIST.md (~15 min).**
- 2026-09-30: **Life layer approved as drafted** (research/interior/LIFE_LAYER.md, 74 items). Order: L1 = interior 50
  (one agent), then L2 = outdoor 24. Built into B4's decorator catalogue so they're placeable at once.
- 2026-09-30: **L1 DONE** (opus-high, 654k tokens / 55 min). 50 interior items = 185 models (50 new, 65 variants, 70
  abandoned); era verdicts in `research/interior/LIFE_LAYER_ERA.md` (all kept, 3 swaps inside items); decorator mounts
  (wall / post / beam / doorway / surface / floor / kamado) + `on_wall`, `on_beam`, `in_doorway`, `on_surface`;
  materials added: `jp_m_decal_sumi_text_life`, `jp_m_food_rice`, `jp_m_food_hoshigaki`, `jp_m_textile_kaya`.
  jp_furniture.pbo = 297 classes. Sheets `research/interior/contact_sheets/l1_*.jpg`. Commits a20d910 .. dbb6149.
  Furnished machiya re-verified by the lead through the pipeline: 137/137.
  - Found: DayZ models are left-handed, so text laid along +x reads mirrored; B3b's signs are probably mirrored (L2
    checks and fixes first). The armour-chest crest barely shows (black on black).
- 2026-09-30: L2 (outdoor 24 + the B3b text check) launched.
- 2026-09-30: **L2 DONE** (opus-high, 581k tokens / 57 min). Commits c2bae75 .. b9be512; `spikes/L2/L2_PROGRESS.md`.
  - **Text fix:** B3b's text was mirrored AND back-facing (the game wouldn't draw it at all); L1's was back-facing.
    Fixed with `skit.face_text` / `text_ok` in B3b's and L1's builds, plus a TXT check (66/66). 37 B3b models rebuilt
    (class names unchanged); jp_site, jp_furniture and jp_buildings repacked (machiya 137/137). Evidence:
    `l2_textcheck_before.jpg` / `_after.jpg` in research/outdoor_kit/contact_sheets/.
  - 24 outdoor items = 81 models (22 new, 20 variants, 39 abandoned); era: all kept, 7 swaps inside items.
    Decorator: `on_site()`, `under_eaves()`. Materials: `jp_m_textile_net`, `jp_m_plant_foliage`. jp_site.pbo = 210
    classes. Sheets `research/outdoor_kit/contact_sheets/l2_*.jpg`.
  - Life layer items aren't placed anywhere yet (the machiya keeps B4's dressing); Phase C shells will use them.
- 2026-09-30: **G4 walk (Stephen): ~95% good.** 8 findings (noren streaks, fire-tub see-through, laundry cloth +
  forks, floating kama lid, kamidana roof turned, floating chest cloth, no Roadway on the goods stand) + the well gives
  no actions. Lead's investigation: causes found for 7; the well matches vanilla on paper. **F1** launched: fix all 8,
  add a temporary well diagnostic, re-check. Then a short re-walk closes G4.
- 2026-09-30: **F1 DONE** (opus-high, 573k tokens / 43 min). Commits fcd7dd7, 3d3c46d, f47e6bb; spikes/F1/F1_PROGRESS.md,
  before/after spikes/F1/f1_fixes.jpg. All 8 causes confirmed and fixed (noren real-scale UVs; vessel() fill disc
  phase-matched and sealed for every vessel incl. well water; hung T-kimono; forks across the pole; new prop
  jp_f_kama_lid on the doma; kamidana ridge parallel to the front; cloth_drape into the chest; Roadway via
  kit.road_tops on sturdy furniture, and decor.blocks treats a Roadway as walk-on only if the top is <= 0.30 m).
  - **The well:** the well p3ds lacked the Geometry named property class=house (vanilla has it, plus
    map=waterpump), so the WRP object never bound to its Land_ script class. Added to all 8 wells. TEMPORARY
    diagnostic WELL_DIAG in spikes/B3b/build.py prints [JPWell] <class> at <pos> IsWell=1: remove after the
    re-walk (steps in F1_PROGRESS.md).
  - Checks: B3a 113, L1 185, B3b 129, L2 81, TXT 66, shell 78, furnished 137, toilet 19, combos 60, all pass.
  - **Next: Stephen's ~10 min re-walk (TEST_CHECKLIST.md) closes G4.**
- 2026-09-30: **G4 PASSED** (Stephen's re-walk: "everything looks good"). The well binds: server + client log
  `[JPWell] Land_JP_S_Well_Tsurube_Curb_Stone at <1026.4, 25, 1053.3> IsWell=1`. **PHASE B DONE.**
  - TODO: remove the WELL_DIAG diagnostic (F1_PROGRESS.md steps) when no server is running; the test server was
    still up at the time (never stop it; do it on the next pack).
  - Next: Phase C wave 1 (proposal to Stephen; nothing launched without his yes).
- 2026-09-30: **Phase C wave 1 agreed** (Stephen): C1 = town shells, ALL 60 townhouse units + post-town house (~6-8) +
  inn (~3-4), bare, with test rows on the island; C2 = rural shells (~18-25: Kanto + Kinai farmhouses, huts east +
  west, shed) + a farmhouse template + a hamlet on the island; C3 = kura + furnished versions of every wave-1 type
  (decorator + life layer) + street/yard dressing + ONE bundled walk. Sequential, opus-high, time-logged.
  **C1 launched** (also removes the WELL_DIAG diagnostic).
- 2026-09-30: **C1 DONE** (opus-high, 532k tokens / 74 min). Commits 7598034 .. f56a565; spikes/C1/C1_PROGRESS.md.
  - 81 shells: 69 townhouse units (Land_JP_Townhouse_<Region>_<N>ken_<Pos>_<Tori>[_Suffix]: the 60 + 6 Edo board-roof
    middles, 1 Edo kakigara, Kamigata 3-ken _Kyo / _Komeya fronts), 8 post-town houses (Land_JP_PostTownHouse_*), 4
    inns (Land_JP_Hatago_*, incl. Hatago_Grand with the stair). 4,717 checks, 0 failures (uildings/shellcheck.py).
  - Budgets: worst townhouse-class 8,580 / 3,157 / 1,196; large-class Std_Mushiko R1 11,892, grand inn R3 1,565.
  - Kit changes (template options, family pipeline, rafter/verge/pent fixes, faster ray check) changed the machiya
    slightly: re-verified 78/78, furnished 137/137. WELL_DIAG removed. jp_buildings.pbo 51.5 MB, 84 classes.
  - Island: test street at z 1080 north of the machiya (Kamigata + Edo rows north side; post-town houses + 2 inns south).
  - **Open:** the grand inn's storey source (Ohashiya 1716) was cited from memory: verify before it ships to a map.
    No navmesh. Sheets esearch/production/contact_sheets/c1_*.jpg.
- 2026-09-30: **C2 launched** (rural shells + hamlet; the grand-inn storey source check folded in, per Stephen).
- 2026-09-30: **C2 DONE** (opus-high, 658k tokens / 63 min). Commits 6541883 .. 02e984a; spikes/C2/C2_PROGRESS.md.
  - 21 rural shells, 1,050 checks, 0 failures: Kanto farmhouse 4, Kinai farmhouse 4 (all with the ox stall; yamato-mune
    takahe on one), hut east 4, hut west 5, shed/barn 4. Template jpparts/templates/rural.py (kanto, kinai, hut_east,
    hut_west, shed); each shell lists its fittings for C3 (irori pit + hook point, kamado spot, stall).
  - Budgets: farmhouses (large) worst 11,422 / 4,268 / 1,494; huts + sheds (standard) worst 5,371 / 1,425 / 509.
  - Hamlet on the island: west yard x 930-970, z 999-1048 (2 farmhouses, 3 huts, 2 sheds). jp_buildings.pbo 64.6 MB.
  - Not built: Kinai kabata pit (needs running water); Kanto kabuto form (post-1730).
  - **For Stephen: (1) Grand inn:** the Ohashiya is two-storey but dates after the 1809 fire (Toyokawa city, Cultural
    Heritage Online); 1716 is tradition only; no dated two-storey Tokaido inn before 1730 found. Model unchanged.
    **(2) G1-6 conflict:** a skirt pent can't sit under a full thatch eave at the kit's wall height, so Kanto walls went
    up 0.42 m with no pent (Kinai lower roofs are the pents). Judge the look at the wave-1 walk.
- 2026-09-30: Stephen: **grand inn keeps two storeys** (deliberate exception, G1_DECISIONS A1-3); the Kanto farmhouse look
  is checked on the wave-1 walk. **C3 launched.**
- 2026-09-30: **C3 DONE** (opus-high, 793k tokens / 71 min). Commits 61e5b49 .. bcd659a; spikes/C3/C3_PROGRESS.md.
  - Kura: 3 shells (Land_JP_Kura_Namako, _Kuro_Hinged = the first hinged plaster doors, _Plain), two floors by
    jp_p_stair _open, 115 checks; template jpparts/templates/kura.py.
  - 14 furnished variants: Kamigata rice + paper shops, Edo cloth + corner sake shops, post-town home, ordinary inn,
    grand inn (upstairs dressed), Kanto + Kinai farmhouses, east + west huts (T1), walled shed, 2 kura. 1,341 checks.
    Code: uildings/furnishkit.py, urnish_sets.py, jpparts/fittings.py; per-room summary spikes/C3/summary.py.
  - Island: 12 shells swapped for furnished variants, 2 kura, 59 free objects (	est/placements/C3.csv) + 42 tied to
    buildings. Re-runs: 105 buildings, 6,001 checks, 0 failures; combos 60/60.
  - Not done: navmesh (zombies won't path inside); townhouse shops keep a tatami front room (no board strip: shell change).
  - **Next: Stephen's bundled wave-1 walk (TEST_CHECKLIST.md, ~28 min, 9 verdicts).**
- 2026-09-30: Stephen is away from the PC (walk pending). Walk-independent work launched CONCURRENTLY:
  - **W2**: the 7 W2 outdoor items + Stephen's additions: torii with/without shimenawa and shide, mossy rural torii,
    mossy stone lanterns, graveyard stones at 2-3x variety (era-checked). Owns the site pipeline + jp_site.pbo; NO materials.
  - **S1**: the 22 KEEP_TRADES shop dressing sets (spec SHOP_SETS.md, props, set definitions, a few demo shops). Owns the
    furniture pipeline + jp_furniture.pbo + ALL material work. decor.py shared: additive edits only.
- 2026-09-30: **W2 DONE** (opus-high, 529k / 35 min). 91 models: wooden torii 20 + stone torii 10 (no rope / rope /
  rope + shide; mossy rural ones; vermilion Inari/Hachiman only), lanterns 13 (5 mossy), steps 13 (Roadway chain OK),
  basin 4, gravestones 24 (1730 forms only; square pillars rare ~5%), grave wood 7. Era: esearch/outdoor_kit/W2_ERA.md.
  jp_site.pbo 301 classes; decor mounts shrine / graveyard / slope. Commits 6d1c6ce, d402bb3, e2d17d5, c5c8528.
  Gaps (S1 owns materials): more posthumous-name cells, Sanskrit syllables for gorinto / hokyointo (built blank), an
  outdoor bare-earth material. Not placed on the island.
- 2026-09-30: **A4 audit DONE** (opus-medium, 138k / 9 min): esearch/AUDIT_MISSING.md. Top item: the built sakura are
  Somei-yoshino in bloom (banned, 1840s+): remake as yamazakura / edohigan in autumn leaf. Stephen to pick from it.
- 2026-09-29: Waterways G1 accepted (10 decisions; research/catalogue/G1_DECISIONS.md). Map sketch: Numazu castle
  dropped, Kanō + Minakuchi castle towns added.

- 2026-09-30: **S1 DONE** (opus-high, 759k / 86 min). Commits 6971798 .. 1f07f64. KEEP_TRADES §A lists 28 trades (header says 22):
  all 28 have a set; the 3 star sets are written as recombinations only. Spec + as-built API: research/interior/SHOP_SETS.md.
  - 84 new props / 175 models (goods clusters, fittings, 35 hanging signs, sugidama green / brown / fallen); jp_furniture.pbo
    473 classes. Materials added: shop text atlas, red lacquer, sometsuke porcelain, tanned leather, tofu (palette
    lacquer_shu + porcelain_sometsuke are guesses).
  - Set API uildings/shop_sets.py: pply_mise(c, trade, ab), ront(), sets() -> 168 shop_<trade>_<3k|2k>_ab<0-2>;
    the townhouse template has a mise_floor (board strip) option, off by default. 6 demo shops registered, not placed.
  - Era calls: prints ink only (colour 1744+), Kyoho-bina in, no daruma / Banko / oden, tobacco hand-cut; flagged: Odawara
    lantern founding date, the moneychanger's fundo-shaped sign vs the research's 'coin-shaped'.
  - Not done: whole-house dressing fits only 3-ken toriniwa-left and 2-ken toriniwa-right units (4-ken + 2-ken ends need
    layouts). Sheets research/interior/contact_sheets/s1_sets_1..5.jpg.

- 2026-09-30: **M1 DONE** (opus-high, 501k / 44 min). Commits 1a74138, ec3df93, b6cd2dd, fad881f; spikes/M1/M1_PROGRESS.md.
  - New: jp_m_ground_earth_bare (148,130,108; k41/k37/k27), jp_m_wood_new (172,146,129; i04), jp_m_wood_silver`n    (126,125,120; k31/c03), jp_m_floor_tatami_heri_cha (palette cha_koge, no local brown-heri photo), carved kaimyo atlas
    jp_m_decal_carved_text_grave (14 names, 1670-1729, era/sign checked by arithmetic; rank usage from general knowledge),
    grave-post ink jp_m_decal_sumi_text_grave (6 cells 1724-1730), jp_m_wicker_aged (proxy: no kori photo),
    jp_m_wood_firewood + _endgrain_firewood (i22).
  - Applied: gravestones carry kaimyo, grave mounds bare earth, bohyo new/silver + ink, kori wicker, firewood (site +
    furniture), brown heri in the Kanto dei / Kinai zashiki (8 farmhouses + 2 furnished). All re-runs pass; jp_buildings
    verified by the lead: 128/128 models ODOL, tree clean.
  - **Bonji NOT done:** no Siddham font on the machine. Needs Stephen's OK to download **Noto Sans Siddham** (SIL OFL 1.1,
    google/fonts ofl/notosanssiddham).
  - **Pitfall:** python buildings/pipeline.py --help STARTS A FULL REBUILD (no argparse help). M1 hit it, stopped it and
    restored 69 townhouse masters. **FIXED 2026-09-30 (lead):** --help / -h prints the usage and builds nothing; unknown
    options build nothing (exit 2).
- 2026-09-30: **M2 DONE** (opus-high, 239k / 14 min). Bonji (Noto Sans Siddham) on gorinto front (KHA, HA, RA, VA, A, top to
  bottom) and hokyointo (HUM E / TRAH S / HRIH W / AH N); 9 cells in jp_m_decal_carved_text_grave; 6 models; general
  knowledge (W2_ERA G16-G19). Commits 82751c7, d188959. The material gap list is now closed except the brown-heri photo.
- 2026-09-30: **G1 DONE** (gorinto seating, Stephen spotted the floating roof): suirin now a sphere cut flat top + bottom at 0.62 of
  the diameter, 12 sides, bonji on the middle band; every ring seats flush (new seat check: sphere->roof 0 -> 0.73);
  gorinto_stack's 1.25x roof sits flat, 5 deg yaw. Heights s 0.565 / fallen 0.650 / l 2.00 m. Commits cec274a, 4d4e860.
- 2026-09-30: **Agreed with Stephen: ONE showcase agent after the Pompompurin agent (P1, fun\pompompurin) finishes:** convert +
  place Pompompurin life size (own jp_fun.pbo), a shrine (W2 torii / lanterns / steps / basin) + a graveyard (W2/W3/M1/M2/G1
  stones + bohyo), swap a few street units for S1's demo shops, a life-layer gallery row (all 74), then ONE walk checklist
  with 10 stops: street, hamlet, kura, machiya shop + yard, M1 materials (spot checks), shrine, graveyard, shops, life
  layer, Pompompurin (~40 min).
- 2026-09-30: Stephen stopped the Pompompurin agent (didn't like the renders): NOT in game, files left in fun\pompompurin\.
  **SH1 launched** (showcase without Pompompurin; 9 stops).
- 2026-10-01: **SH1 DONE** (opus-high, 575k / 42 min). Commits ca6e2f3, 9703bc0, 487261f. Shrine x 1024 z 1099-1198 + hill stair
  x 1042 z 1228-1263 + Inari stair x 1058 (149 objects); graveyard x 990-1013 z 1108-1130 (148); gallery = 3 open sheds at
  x 1072/1080/1088 z 1036 (L1-L74); demo shops D1-D6 on the street (3 swapped, 3 inserted). verify_oprw PASS 4076/4076;
  build_mission.py fixed (CE positions snap to the nearest building of the class). Maps sh1_map_{shrine,graveyard,gallery,
  street}.jpg + ID table spikes/SH1/SHOWCASE_MAP.md. **Walk: TEST_CHECKLIST.md, ~44 min, 14 verdicts.**
- 2026-10-01: **Stephen's showcase walk.** Street + graveyard + most torii good. Findings: ZERO doors open anywhere; lead found
  only 31 of 128 building classes match Land_<p3d stem> (town units say 2ken vs file 2k; furnished + demo shops differ
  entirely) -> unbound objects (no doors, no loot). Props: broom, rice sheaves, bonsai/pots, sword rack, torii rope need
  higher fidelity; tawara end caps missing; fallen lantern side + clear decal; loom/wheel float; leaf decals are blobs;
  stone torii texture too regular; two-tone pot; lever well rock/rope; notice board floating; fire-watch ladder not
  climbable; wants collapsed torii. Buildings: Kinai 'thick thing under roof', kura doors/shutters thick + too white, a
  roofless street house, tools off the wall, top hill-stair torii too low. **FP1 (props) + FB1 (buildings) launched.**
- 2026-10-01: **GitHub remote added** (Stephen): origin = https://github.com/Teggom/teggoms-dayz-japan-mod.git, branch master.
  First push after FP1 + FB1 finish. README rule 3 rewritten: every agent commits its own paths AND pushes after each
  checkpoint (pull --rebase on rejection; never force-push).
- 2026-10-01: **FP1 DONE** (764k / 69 min; commits 1a9b8f0 .. 4cefb88) and **FB1 DONE** (532k / 74 min; commits a138258 .. b41f638).
  - Doors: each building .p3d renamed to its class minus Land_ (97 of 128); uildings/bindcheck.py fails any build where
    class != Land_<p3d stem> or Geometry lacks class=house; 128/128 bind. No second cause (machiya/shop/toilet identical
    to 3d3c46d and bound in both logs).
  - FP1: broom, sheaves, bonsai/pots, sword rack, ropes, charcoal-bale ends, lantern, loom supports, leaf shapes, stone
    texture, straw stack, lever well, notice board, climbable ladder Land_JP_S_Fire_Watch_Ladder_Tower (deck 4.9 m), 5
    collapsed torii (placed S100-S104), materials shikkui_aged / stone_carved_aged / ceramic_earthenware / plant_kiku.
  - FB1: Kinai gable fix, kura doors 0.135 / shutters 0.08 + aged plaster, tools re-seated (leancheck.py), hill torii
    S63/S70 -> large (2.60 / 2.79 m clear). E (roofless house) not reproduced: likely D5's pale board roof 0.17 m lower
    reading as sky; checklist asks for a screenshot. Open: gallery wall items hang 6.5 cm off the walls.
  - **Re-check: TEST_CHECKLIST.md (~15 min), doors first.**
- 2026-10-01: **Stephen's re-check:** doors + the rest 'look really good'. New: firewood piles look bad; z-fighting (stair stringer vs
  wall, doorway sills, a wall/floor in the mochi building); usu/kine float; Kinai gable white band too massive ('real?');
  farmhouse partitions stop short of the roof; two-storey divider short + wall gaps; rope 2.5x more segments.
  Screenshots in test/feedback/2026-10-01_recheck/. **FP2 + FB2 launched** (they push to GitHub themselves).
- 2026-10-01: **FP2 DONE** (466k / 41 min: woodpile.py firewood + redrawn end grain, usu/kine seated, ropekit.py 2.5x) and **FB2 DONE**
  (475k / 64 min: zfight.py C20 102,726 -> 0 coplanar pairs; Kinai gable rebuilt to the real yamato-mune form (plastered gable
  wall 0.26 m above the thatch + tile cap; still shallower thatch + no lower kitchen roof: Stephen's call); partitions end at
  head beams (C21) + an 8 cm loft slit closed in every town house / inn / machiya; grand inn divider to the roof + missing
  posts (C22)). 128/128 buildings, 8,574 checks; machiya now 81, furnished 140. **Re-check: TEST_CHECKLIST.md (~10 min).**
- 2026-10-01: **Phase C wave 2 launched** (Stephen: shrine/temple village grade AND town grade now). Order: W2P1 (village
  shrine/temple parts: koran + kizahashi, tobira, nagare, chigi/katsuogi/hoju, stilts, shitomi) + W2P2 (curved sori roof +
  kumimono brackets; registers in the parts manifest after W2P1) + W2C (civic shells: tea house x3 sizes, smithy +
  swordsmith, guard hut, ward gate kido) in parallel -> then W2S (shrine + temple shells, village + town grades) -> then
  W2F (furnish + place: a hall on the showcase shrine site, a village temple, civic by the street) + one walk.
- 2026-10-01: **W2P1 DONE** (579k / 44 min): 48 variants, 10 parts + 8 micro-shrines (site_hokora); offline honden 26/26, haiden 25/25,
  temple hall 32/32 (register tiled halls as 'large'). Not built: small gate (use W2C's gates.py), kuri porch. Missing materials:
  cypress bark (hiwada), bronze/copper patina. **W2C DONE** (476k / 44 min): 16 civic shells (Teahouse x7, Smithy x2 +
  Swordsmith, Guardhut x3, Kido x3), 144/144 buildings bind + pass; prop spots in rooms json; roofed kido = general knowledge.
  **Git hazard found:** agents share one index; W2P1's fc6c66b swept in W2C's staged files (nothing lost). README rule 3 now
  requires git commit --only <paths>.
- 2026-10-01: **W2P2 DONE** (559k / 54 min): sori.py roof (irimoya / yosemune-hogyo / kirizuma / nagare; hongawara / kokera / hiwada /
  copper; 8 variants), kumimono.py (funa, oto, mitsudo, degumi, mitesaki; 9 variants), rame_storey_hakama; offline hall 8,174,
  hall_kokera 5,564, hondo 11,259, shoro 5,807 faces (R3 1,047 > standard 800: no tower class yet — ask Stephen). W2P1's kidan
  costs ~2,000 faces. **W2S launched** (shrine + temple shells, both grades; adds hiwada / copper / bronze materials).
- 2026-10-01: **QUEUED (Stephen: yes, after W2S + W2F): kit-wide wood texture variety** = option 2 + 4: per wood material ONE atlas with
  3-4 distinct patches (weathered / sooted / new wood), each piece picks a random patch + offset along the grain + optional flip;
  grain always along the member's length; believable tile scale (1-2 m); PLUS a large-scale macro weathering layer (rvmat MC stage:
  grime, sun-bleach, streaks) at a non-matching scale. In the kit's UV helpers so every building, prop and part gets it; rebuild
  + before/after renders. ~0.5-0.7M tokens. (Stone torii already got a per-piece lichen fix in FP1.)
- 2026-10-01: **WANTED, do LAST (Stephen: eventually; nothing now): orientation-aware moss on thatch.** Moss heaviest on the slope
  that faces NORTH in the world (+ shaded lower eaves), lighter south; shibamune planted ridges as a Kanto variant; abandoned =
  no hearth smoke = faster growth. Plan: the roof generator takes per-slope moss weights; the pipeline emits a few direction
  variants per thatched building automatically (which side faces north: front / back / left / right, + an east-west 'tie'
  variant), and the MAP PLACEMENT step picks the variant from each building's final yaw. Same trick later for lichen on north
  faces of stone and sun-bleach on south faces. Do it once the map placement exists (variants are generated, not hand-kept).
- 2026-10-01: **QUEUED (Stephen: yes) right after W2S, BEFORE W2F: faster checks.** (1) cache: a fingerprint of each building's
  inputs (recipe source, the kit modules it imports, params) stored with its last passing result; unchanged = skipped, so a
  kit change only re-checks the buildings that use the changed module; (2) make the slow checks smarter (spatial grid for the
  C20 face-pair test, adaptive ray counts for C11, profile the hotspots). Keep a 'full' flag that ignores the cache. Max 4 parallel processes, normal priority (Stephen).
  Why: verify_all re-checked all 169 buildings x 60-90 checks from scratch, 10 processes, ~20+ min, growing linearly.
- 2026-10-01: **W2S DONE** (639k / 77 min; commits 06f8b5f .. d9974e6). 25 shells, 950 checks: Haiden Village / Town_Hiwada / Town_Copper;
  Honden Nagare_Village (+_Chigi) / Nagare_Town / Shinmei (sealed, loot on the veranda); Temizuya x2; Shamusho x2; Kagura x2; Do x4
  (2-ken board / thatch, 3-ken tile, Town curved copper hogyo); Hondo Village / Town (degumi); Kuri x2 (genkan porch); Shoro Village /
  Town (hakama); Gate Yakuimon / Shikyakumon. Not built: kasuga honden, wari-haiden, mitesaki hondo (17.6k faces), sanmon, pagoda,
  sutra store. Materials: jp_m_roof_hiwada, jp_m_roof_copper, jp_m_metal_bronze. Town shoro 6,371 / 2,435 / 1,267 (registered large;
  **tower class = Stephen's call, still open**). Prop spots listed for W2F. .gitignore now covers buildings/*/out/ + renders/.
- 2026-10-01: **V1 DONE** (394k / 98 min; commits 8e1eccc, 7dc1921, 14e6ba2). Rays were 86% of check time. Full verify of 169:
  935 s -> 193 s (4 jobs); nothing changed: 3 s; sori.py changed: 29 s (exactly the 25 shrines/temples). uildings/checkcache.py;
  python buildings/verify_all.py [--jobs N<=4] [--full] [--family X] [keys]; pipeline --full. Old vs new checks.json byte-identical
  (10,262 checks). Fixed a furnishkit passage-label carry-over bug. **W2F launched.**
- 2026-10-01: **W2F DONE — PHASE C WAVE 2 BUILT** (675k / 53 min; commits d9cd7b5 .. 8b8836e). 49 props (jp_furniture 522 classes;
  builder spikes/W2F/build_w2f.py), 24 furnished variants (1,558 checks), placed: P town shrine on the hall site (haiden P1, honden
  P2 on terraces + temizuya / shamusho / kagura), V village shrine north of the hamlet, T village temple by the graveyard, U town temple
  (~1100, 1110), K kido + tea houses + smithy + swordsmith + jishin-ban at the street ends; oku-miya too steep. verify_oprw 4123/4123;
  193 buildings / 11,820 checks / bindcheck 193. Maps w2f_map_*.jpg + SHOWCASE_MAP.md. **Walk: TEST_CHECKLIST.md (~32 min).**
  Not done: navmesh; blank temple name boards (no atlas cell); Nichiren / Shinshu sect swaps.
- 2026-10-01: **Stephen's wave-2 walk** (notes: test/feedback/2026-10-01_wave2/NOTES.md). Curved roofs + most of P good. Findings:
  tobira handles on the wrong leaf (P1, t1); offering box litter + blocks the stairs; masks (P5) low-res; Buddha / Jizo statues
  are blobs (need picture references + care; Jizo staff top see-through); shoro striker rope + U1 bell floating; U1 veranda sides
  cut off; rope torii feel too short; woodpiles need side support; torii pole + moss textures repeat. **Policy (Stephen): small
  detail props deserve more faces; they're what make the world pop.** VPP admin tools added to the Japan test launchers
  (@CF;@VPPAdminTools;@Japan; permissions copied from ServerProfile). **FX1 launched** (geometry/placement fixes 1-6).
  Next: FX2 statues/detail pass (needs reference images: Stephen's call), FX3 = the queued wood-texture job + moss variety.
- 2026-10-01: **FX1 DONE** (cce4930, 984b072, 4771e25). tobira pulls on their own leaf + gate hinge straps (handlecheck 24 -> 0 of 40);
  offering boxes beside the stair foot, sourceless litter removed; hung props hang from real members (hangcheck 16 -> 0); six
  front-only verandas got railing returns (a wrap-round veranda pushes U1 to 12,428 > 12,000: Stephen's call); torii scaled up,
  rope on the nuki front with half the sag: lowest shide 2.35-2.64 m, nuki clear 2.49-2.94 m; woodpiles have tied end stakes.
  verify_all --full 193 / 11,822; verify_oprw 4125/4125. Pitfall: build_w2f.py's folder binarize crashed on an existing ODOL
  (FX1 binarized its six props singly).
- 2026-10-01: **Stephen's decisions:** small props 800 / detail-hero props 1,500 / statues as needed (PLAYBOOK §12); budgets are guidance:
  +30-50 % is fine when an object needs it, not as the norm (so: no separate tower class; U1 wrap-round veranda YES). Statue
  references: **option B approved** = CC0 images from the Met Museum Open Access API + Cleveland Museum of Art Open Access
  (fallback: Stephen saves photos). **Komainu wanted** (+ paired lanterns). Torii rope now looks too SHORT: hang it a little lower
  (keep head clearance). Next: FX2 (statues + komainu + detail props + rope + U1 veranda), then FX3 (textures), config assembler.
- 2026-10-01: **FX3 phase 1 launched** (Stephen): wood atlas (3-4 patches per material) + shared uvwood helper (patch / offset /
  flip / grain along member / 1-2 m tiles) + macro weathering layer + irregular moss, prepared and proven on samples in
  spikes/FX3/ only, ONE sample sheet (no per-prop renders). **Phase 2 (integration + rebuild) waits for FX2**; the lead resumes
  the same agent then.
- 2026-10-01: **FX2 DONE** (685k / 81 min; 5b6a02f .. 3e7f94b). Refs: 32 CC0 images / 20 objects (research/statues/REFS.md; Met v1 search
  retired 2026-10-01 -> v1.1). Altar images 3.5-4.6k faces (new 'altar' class 5,500; material gilt_worn), stone Jizo ~1.9k with faces,
  shakujo closed. Komainu (2 forms + mossy) FX-P1/P2/V1, kitsune FX-I1 + lantern pair FX-I2 (no CC0 stone-fox photo: **Stephen may
  save 2-3**). Mask wall 2,128 + temple bell 1,946 (new 2,250 class). Torii rope 3/4 sag, shide tucked, lowest tip 2.31 m. U1 wrap
  veranda 12,428 ('large_plus'); village hall kept returns (wrap failed 2 checks). 193 bldgs / 11,830 checks pass. **FX3 phase 2
  resumed.**
- 2026-10-01: **FX3 DONE** (phase 1 298k + phase 2 410k; bbce5c3, 0449ae0). Wood: 11 materials x 3 wears as 4 m x 2 m 4-patch atlases
  (esearch/materials/make_wood_atlas.py); parts/kit/jpparts/uvwood.py runs from Part.lods() (every pipeline); Stage3 macro
  weathering added by build_materials.rvmat_text (dark woods half bleach, interiors grime only); thatch moss -> macro; moss decal 2 m
  irregular. All rebuilt; verify_all --full 193 / 11,830; uvdiff: 0 changes on non-atlas materials.
  - **Pitfalls:** re-running any wood material maker needs make_wood_atlas.py after it + a jp_common repack (uvwood refuses a
    non-atlas texture). If flipped faces' bumps light wrong in game: uvwood.ALLOW_FLIP = False + rebuild. jp_efftest_medium (test
    tansus) still has old UVs.
  - **Re-check: TEST_CHECKLIST.md has FX1, FX2 and FX3 sections.** Next: the config assembler, then wave 3 or the items track.
- 2026-10-01: **Stephen's walk of FX1-FX3:** good overall. Three fixes queued as **FX4 (after CA1)**: (1) the big temple bell shows a
  backwards texture: you can see into it (inside faces / open mouth); (2) the climbable fire-watch tower is too short at the top:
  you clip into its roof (head room on the deck); (3) stone torii columns still show duplicated textures (FX3 covered wood only:
  extend the atlas + per-piece patch approach to stone). Other minor things deferred by Stephen.
- 2026-10-01: **Stephen: stop agent work for the week at 90% weekly usage** (other lighter projects need tokens); below that, order
  doesn't matter. **Next = wave 3 (more buildings), not items** (Stephen: spawn locations stay the same; items swap in later; the map can
  even come before items). Proposed wave-3 order (lead): FX4 (bell, fire-watch roof, stone atlas) -> 3a upper/samurai dwellings +
  honjin + the WALL KIT (earth / plaster walls, hedges, bamboo fences, stone walls, gates) -> 3b everyday workshops + services (sento,
  stable yard, stall kit, earth-floor + raised-floor workshops, timber yard, foundry) -> 3c trade sites (brewery, water mill, dyer,
  kilns, paper, salt, charcoal, logging, quarry, mine) -> 3d government (official compound, post-station office, checkpoint kit, jail,
  fire watchtower) -> 3e the castle kit (keep with swaps, turrets, tamon, box gate, palace wing, ruins). Pleasure quarters + kabuki
  theatre go with landmarks.
- 2026-10-01: **Stephen: after CA1 -> FX4 -> then 3a.** 3a now also includes a **modular covered-corridor kit (watari-roka) + kairo
  cloister** (historical: temple hondo<->kuri corridors around tsuboniwa courtyards, abbot's quarters, shrine kairo around the inner
  precinct, samurai / honjin / daimyo wings linked around gardens): straight 1/2/3 ken, corner, T, cross, end, stepped-roof piece for
  slopes; sides open-railed / half-walled / enclosed; raised board floor; roofs straight board / tile / curved sori. Proof on the island:
  link one temple's hondo to its kuri (and a kairo segment at the town shrine if cheap).
- 2026-10-01: **CA1 DONE** (config assembler + budget classes; spikes/CA1/CA1_PROGRESS.md, TIMELOG_CA1.md).
  - `tools/assemble_config.py`: jp_furniture (B3a+B4 113, L1 185, S1 175, W2F 49 = 522) and jp_site (B3b+W2/FP1/FX2 239, L2 81 = 320)
    are merged from per-builder fragments `src/JP/<area>/_frags/<builder>.json`; every builder writes only its own; conflicting
    duplicate classes fail loudly. One command: `python tools/assemble_config.py jp_furniture|jp_site --pack`. The other 11 PBOs
    have one writer each (unchanged). README "Config fragments" has the usage.
  - Proof: all 13 PBOs 0 class differences before/after (`tools/cfgdiff.py`, `spikes/CA1/snapshot.py --compare`); B3a alone and
    B3b alone rebuilt + packed keep 522 / 320 classes (L1 / S1 / W2F / L2 all present); byte-noise ODOLs restored.
  - **The two config pitfalls are REMOVED from this log** (B3b dropping L2's classes; B3a / L1 / S1 dropping W2F's): obsolete.
  - Budgets: FX2's ad-hoc 'altar', 'detail_l' and 'large_plus' folded into PLAYBOOK §12's set (statue / detail / large) with a
    per-object `over_budget_ok` reason; C5 passes and reports deliberate overages (`python tools/budget_report.py`: 9, all
    deliberate). Props small = 800 as §12 says. Checks: props 842/842 (faces unchanged), TXT 191/191, verify_all 193 (cache + --full),
    bindcheck 193, hangcheck 0, handlecheck 0/40.
- 2026-10-01: **FX4 DONE** (341k / 38 min; 71b049a, 597e937): bells hollow (fkit.lathe profile direction; new spikes/FX4/lathecheck.py
  fixed 6 inside-out shapes incl. waniguchi, collars, lids, sedge hat), fire-watch roof 2.20 m above the deck, stone atlases
  (esearch/materials/make_stone_atlas.py: carved / carved_aged / cut) + uvwood stone mode. Pitfall: re-run make_stone_atlas.py
  after any stone material maker + repack jp_common. **Wave 3a launched: K3 (kits) + D3 (dwellings; waits for K3 to build compounds).**
- 2026-10-01 (night): **Stephen approved: launch 3b automatically once D3 finishes** (sento, stable yard, stall kit, earth-floor +
  raised-floor workshops, timber yard, foundry; shells + furnished + placement + walk), after a usage check: only if the
  projected weekly stays safely under 90 % (estimate 3b ~4-6 %).
- 2026-10-01 (night): **K3 DONE** (3b39ef1, 0fd4a89, 131e29d): 97 variants (332 parts). Wall kit 65 (tsuiji x5 finishes, dobei, itabei,
  yotsume, kenninji, shiba / takeho, ikegaki, nozura + uchikomi stone, earth bank; corners, ends, +0.30 / +0.60 steps; kabuki-mon,
  mune-mon, wickets; abandoned states). Corridor kit 32 (1/2/3 ken, corner, T, cross, ends, covered stairs, connector, kairo).
  jpparts/striproof.py roofs both. API in parts/K3_NOTES.md §6 (run_wall, run_roka, connector_fit). **Pitfall: keep each object
  under ~15,000 faces: binarize fails 'Too many vertices' (two halls + a corridor in one p3d).** Missing materials (stand-ins):
  brushwood, black palm rope, ochre plaster, turf, copper valley lining. Hinged gate/wicket leaves untested in the engine.
- 2026-10-02: **D3 DONE — WAVE 3a BUILT** (66e8772, 4ea993d, ffc121c, 0f8349e). 28 shells (Mountain x3, Coastal x2, KumiYashiki_3 x2,
  Doshin x2, Samurai_S / M / L (L 9x5 ken: binarize vertex limit at 10), Merchant_Residence, Headman_East (+_Shiba), Headman_Kinai,
  Chashitsu x2, Itagura x2, Stable_Horse / _Ox, Furoba, NagayaMon x2, Honjin_Omote / _Oku, Wakihonjin; all one storey + attic, sourced in
  spikes/D3/D3_NOTES.md); 16 furnished (buildings/d3_sets.py); 8 compounds / corridors incl. **Roka_Temple_U (Stephen's corridor proof)**
  and Roka_Honjin (shrine-P kairo skipped: terraced halls, no level run). Placed S1-S10, H1-H6, J1-J5, M1-M4, E1-E3, U9.
  verify_all --full 245 buildings / 16,697 checks; bindcheck 245; verify_oprw 4178/4178. Known false flag: placecheck calls every kasuga
  lantern 'hanging'. **Walk: TEST_CHECKLIST.md (~28 min) + FX4 re-check.** **W3B (wave 3b) launched** at 74 % weekly.
- 2026-10-02: **W3B DONE — WAVE 3b BUILT** (cf3b704 .. 0ac243b). 18 shells (template jpparts/templates/trade.py): Sento x2 (one mixed
  bath in 1730, bans from 1791; zakuro-guchi decorative + a board door), StableRow x2, Booth_Barber / _Misemono, Workshop_Doma x2,
  Workshop_Bench x2, Timber_SawShed / _Store / _ShingleShed (trestle sawing, not a sawpit), Foundry x2 (koshiki-ro cupola + treadle
  bellows), 3 yard compounds; 34 props / 63 models (jp_furniture 585); 14 furnished. Placed A1-A14 artisans' street, B1-B5 bathhouse +
  stable yard, T1-T8 timber yard, F1-F6 foundry (W3B.csv; map w3b_map.jpg). 277 buildings / 18,522 checks; bindcheck 277;
  verify_oprw 4216/4216. Not done: hot-spring bath hut, painted show-booth sign texture, navmesh. Pitfall: binarizing the props folder
  crashes on already-binarized models: use spikes/W3B/binsingle.py. **Walk: TEST_CHECKLIST.md = D3 (~28 min) + FX4 re-check + 3b
  (~15 min).** Weekly 76 %. Next (Stephen's call): 3c trade sites (brewery etc.), 3d government, 3e castle.
- 2026-10-02: **FX5 DONE: Stephen's 3a / 3b walk fixes** (a5639a1, 7747dea, 9f5cffe). Root causes and fixes:
  (1) **gate floors flickered**: `dwelling.compound()` laid every gate passage as an earth slab whose top lay exactly AT
  grade (z-fight with the terrain; all 9 compounds incl. the 3 W3B yards); now `floors.sill_pad()`: packed earth, top
  +0.10 (0.06 would have been coplanar again at the timber / foundry yards, sunk ~6 cm on their slope), sloped 20 deg
  margins into the ground, Roadway on top + slopes, stones 3.5 cm proud, gate leaves lifted (`gate_kabuki(leaf_y0)`).
  (2) **honjin plaster-to-fence gap**: the side board fences started half a ken short of the dobei street wall (0.70 m
  walk-through gap, measured in the built ODOLs); `dwelling._abut()` extends any open run to the wall it meets. Also the
  hedge's corners / back-gate post had 8 cm slits. `spikes/FX5/jointcheck.py --all`: 56/56 joints sealed in Geometry /
  View / Res 1 (kumi yotsume open by design). (3) **hedge**: lumps restarted per module + module-local UVs + an alpha-cut
  card material on solid boxes; now one continuous clipped form on the run coordinate (`wall(run=...)`), smooth normals
  (new `Solid.vn`), new `jp_m_plant_hedge` + `_fringe` (make_fx5_materials.py), sprig fringe; parts + compound rebuilt.
  (4) **U9**: recorded under Confirmed future work (modular host variants, end of production), untouched.
  Checks: verify_all --full 277 buildings / 18,522 checks / 0 failures; bindcheck 277/277; verify_oprw 4216/4216; placecheck island unchanged
  (415, same as W3B); hangcheck 0; handlecheck 40/0; gradesweep: 0.00 m2 at grade on all compounds. Not fixed: K3's
  corridor soseki faces at grade (0.35-0.44 m2 in the two roka objects; fixing them would change U9). Sheets
  contact_sheets/fx5_hedge.jpg, fx5_hedge_variants.jpg, fx5_gates_joints.jpg. **Walk: TEST_CHECKLIST.md = FX5 re-check
  (~5 min); wave 3c-1 adds its section below.**
- 2026-10-02: **W3C1 DONE: WAVE 3c-1 BUILT, the trade quarter** (e97f33f, aba3726 + the W3C1 3/4, 4/4 commits). Research first
  (spikes/W3C1/W3C1_NOTES.md: sake-museum.jp / nada-ken / Mitaka water-mill pages + project research; every size recorded).
  **Brewery = the Nada kasane-gura**: Land_JP_SakaGura_Okura (9 x 4 ken, eave 5.40, log truss, four 1.8 m tubs, the lever press
  with a 5.8 m beam + hanging stones, the starter loft by stair) + Land_JP_SakaGura_Maegura (steaming hearth + koshiki under a
  steam vent, koji ante-room + straw-lined muro behind two doors, brewers' rest room) side by side, joined by
  jp_p_roof_union _gutter (roofs.roof learns per-eave overhangs); Land_JP_SakaGura_Seimai (FOOT-treadle polishing: Nada's
  water-wheel polishing is Meiwa 1764-72, after 1730); the cask kura (C3 kura dressed) and the brewer's shop (W3B doma
  workshop dressed) with a big brown sugidama; a Hatcho miso vat as dressing. **Water mill** Land_JP_Suisha_Itabuki / _Thatch:
  jp_p_mech_waterwheel _overshot + jp_p_water_flume (dry, sluice shut, on dry land per Stephen), three cam-lifted pestles; the
  stone mill is a HAND quern (gear-driven millstones are late Edo: flagged). **Dyer** Land_JP_Konya_* : four ai-game sunk to the
  rim round a fire pit (shell floor pits in a 0.30 raised earth floor: the island terrain would show in a jar sunk below
  grade), drying frames in its yard. **Paper mill** Land_JP_KamiSuki_*: vat + mould on a spring pole, beating board, couching
  press, bark steamer lean-to, drying boards in its yard. 3 yards (K3 kit). 12 shells, 8 furnished, 22 props / 40 models
  (jp_furniture 625 classes). **New district rule applied:** everything in ONE district south-west of the yard (x 884-946,
  z 852-892, lane z ~864; ~160 m from the spawn), free ground for 3c-2 recorded west and south of it (SHOWCASE_MAP W3C1,
  w3c1_map.jpg); buildings on the slight slope are seated so no floor has terrain through it. Checks: verify_all --full 297 /
  19,640 / 0; bindcheck 297; verify_oprw 4239/4239; hangcheck 0; handlecheck 40/0; yard joints sealed (jointcheck_w3c1);
  gradesweep: no up-facing at-grade faces on the yards. Over budget (with reasons): Konya_Sangawara +23 % R1 (the vat bank),
  Suisha R3 +47 % (the wheel's buckets in every LOD for C15). Not done: ☆ country sake brewer, an inside door between the two
  kura, L / T roof valleys, an engine ladder (static prop only), shibori pattern texture, navmesh. Pitfalls: a shitami skirt
  wall_run across a doorway needs internal_posts=False (a hidden post stood in the kura doorway: 0.44 m clear); a kura door
  bay's skirt must skip the whole bay; C15 compares top heights from above, so an open-bucket wheel needs its buckets in every
  LOD; gradesweep counts down-facing faces too (start floor slabs below grade); prop names containing 'hang' read as hanging
  props in placecheck. **Walk: TEST_CHECKLIST.md = FX5 re-check (~5 min) + 3c-1 (~15 min).** Weekly 77 % -> 80 %.
  Next (Stephen's call): 3c-2 (kilns, salt, charcoal, logging, quarry, mine), 3d government, 3e castle.
- 2026-10-02: **FX6 DONE: Stephen's 3c-1 walk fixes + the small-gate family.** FX5 confirmed in game by Stephen 2026-10-02
  (gate sills, honjin joints, hedge). Root causes and fixes: (1) **dyer's cloths**: the torn frame's fallen lengths were a
  flat strip + a stiff 1 m cloth ramp standing in the air, and every hung length hung BESIDE the bar (up to 4.5 cm off);
  now they drape over the bar and the fallen ones lie flat (5 cm, 4 cm under the yard surface). The same sweep fixed
  every 3c-1 prop that rested on nothing (dye-rack bar, press beam + slings, tub ladder, couching lever, drying-board bar,
  bark strips, three ab states). (2) **gates**: new `sitewall` family sized to the fence: kido_kata (single-leaf board
  gate + side panel), kido_ryo (two-leaf board gate, no kabuki beam, 1 / 1.5 ken), shiorido (bamboo lattice gate),
  opening (posts only); `dwelling.pick_gate` = the rule (fence kind + height x status x role x carts; table in
  parts/K3_NOTES.md §6 and spikes/FX6/FX6_NOTES.md §3); all 12 compounds re-assigned (status gates kept: honjin roofed
  kabuki-mon, doshin kabuki-mon, nagaya-mon objects; the paper yard now has a shiorido, the kumi row an opening, the
  cart yards two-leaf board gates, back / garden gates single-leaf). Fences stop at each gate's own post (post_w),
  FX5 sill pads + `_abut` unchanged. (3) **kura doors**: every `_open` kura doorway built its plastered leaves standing
  straight out (looked like doors that should work); now folded back flat (period practice; the wooden sliding door is
  the door). Rebuilt Kura_Plain, Kura_Namako (+ furnished), SakaGura_Okura / _Maegura (+ furnished), the cask kura;
  Kura_Kuro_Hinged unchanged (its plaster leaves are the working rotation-door test). (4) **koji room**: the bed stood
  0.35 m inside the muro's only door; furnish check D4 skipped it ('sparse' room, no free cell = "no door reaches");
  bed to the back wall, shelves to the side. (5) **washbasin**: hangiri_scattered's third tub stood on edge on one rim
  point; now upside down on the floor. New checks: spikes/FX6/propfloat.py (prop bodies rest / don't tip / cloth hangs),
  propseat.py (props in rooms seated), roomaccess.py (0.6 m capsule from every door), gatecheck.py. Checks: verify_all
  --full 297 / 19,633 / 0; bindcheck 297; verify_oprw 4239/4239; placecheck baseline (421, W3C1's same 6 rows); hang 0;
  handle 40/0; gatecheck 8/0; gradesweep 0.00 m2 on compounds (paper yard 0.12 = yotsume culm feet, baseline);
  jointcheck FX5 56 OK + W3C1 13 OK (+ by-design open bamboo); roomaccess --all 294 buildings 0 failing (only the muro
  failed before); propfloat 3c-1 0 (107 older props listed in spikes/FX6/_propfloat_catalogue.txt), propseat 3c-1 0
  (older: 173 of 1,607, 96 of them pots seated in kamado holes by design; spikes/FX6/_propseat_older.txt). Sheets
  contact_sheets/fx6_gates.jpg, fx6_fixes.jpg. **Walk: TEST_CHECKLIST.md = FX6 re-check (~8 min); 3c-2 adds its
  section below.** Weekly 81 % -> 82 %.
- 2026-10-02: **W3C2 DONE: wave 3c-2, the rural / industrial trade sites** (Stephen approved; agent W3C2, Opus, no
  sub-agents). Sourced setup first (spikes/W3C2/W3C2_NOTES.md: web sources Ome city on the Nariki lime burn, ja.wikipedia
  Gyotoku salt fields, Nara National Research Institute on the daruma kiln; B_TRADE_INDUSTRY; era tests). Built site by
  site, each whole: (1) **charcoal** Land_JP_SumiGama (earth-dome kiln under its board roof) + the burner's hut
  Land_JP_Hut_West_Ishioki_Sumiyaki; (2) **pottery** Land_JP_Noborigama (Seto / Mino climbing kiln: firebox + 4 chambers
  on its own bank, stokers' shelter; Tokoname used the tunnel kiln in 1730, flagged) + the potter
  Land_JP_Workshop_Doma_Itabuki_Toki + Land_JP_Compound_PotteryYard; (3) **tile works** Land_JP_Kawara_Gama (daruma
  updraught kiln, Sengoku-period type) + Land_JP_Workshop_Doma_Sangawara_Kawara + Land_JP_Shed_Open_Board_KawaraDry +
  Land_JP_Compound_TileYard; (4) **lime** Land_JP_Ishibai_Gama (Nariki-type dry-stone kiln pit on its bank, the burnt
  heap) + Land_JP_Shed_Open_Thatch_Ishibai; (5) **quarry** Land_JP_Ishiba (two cut benches, wedge-hole rows, a
  half-split block) + Land_JP_Shed_Open_Board_Ishiku (sharpening forge); the stonemason folded in with the existing
  lanterns + new blocks and stone sledge; (6) **mine** Land_JP_Mabu (knoll, **4-ken timbered drift ending at a
  rockfall**, walkable; portal shimenawa, drainage trough, yama-no-kami hokora) + Land_JP_Shed_Open_Board_Senko +
  the new Land_JP_BunkHall_Itabuki(_Miners); (7) **logging** Land_JP_Shura (the slide's last 4 bays on trestles) +
  Land_JP_BunkHall_Ishioki(_Loggers) + W3B's furnished saw shed (the raised trestle, no sawpit); (8) **salt** (Gyotoku
  1730 = irihama with the sieve method and a crushed-shell pan, fuel pine needles) Land_JP_Enden (raked bed, dry ditch,
  embankment + sluice) + Land_JP_Kamaya_Itabuki(_Furnished) (the shell pan on its firebox under the smoke vent),
  **on dry land like the water mill** (a shore later = placement only). New kiln kit
  parts/kit/jpparts/ruralsite_parts.py (6 site parts: PGA 26 / 37 / 38 / 39 / 40 / 41), template
  templates/ruralsite.py (12 shells), 18 props / 24 models (sitefit, jp_furniture 649 classes), 10 furnished.
  Yards' gates by pick_gate (pottery: bamboo fence, 1.5-ken cart opening; tile works: board fence, two-leaf kido_ryo).
  **District:** x 826-952, z 818-900, wrapped round 3c-1's west and south; a loop of lanes from 3c-1's lane west end,
  south, east and back up to its east end, a spur north to the logging camp (SHOWCASE_MAP W3C2, w3c2_map.jpg).
  Commits: d8e9715, 8b70fbd, e86fa69, d1296b5 + the placement / checks commit. Checks: verify_all --full 320
  buildings / 20,700 checks / 0 failures (then cached re-run all pass); bindcheck 320; verify_oprw 4285/4285; hangcheck
  0 (W3C2 furnished); handlecheck 40/0; gatecheck 8/0; roomaccess 23 buildings / 0 failing (21 open rooms skipped);
  propfloat sitefit 24/0; propseat 78 props, 3 'floating' = pots seated in kamado holes (FX6 baseline by design);
  jointcheck_w3c2 tile yard 6 OK, pottery yard open by design (yotsume); gradesweep: no up-facing at-grade faces but
  soseki stone tops (baseline); placecheck island 442 = baseline 421 + W3C2's 21 (props sunk 2-9 cm on the slope, the
  two stone lanterns false-flagged 'hanging', the two yard fences sunk 0.32 / 0.40 on their high corner = within the
  posts' -0.40 footing). Over budget (reasons recorded): BunkHall_Itabuki +2 % R1, BunkHall_Ishioki +38 % R1 (stone roof).
  Not done: kiln roofs over the climbing kiln (period images vary), a smelting hut at the mine, a second tile kiln,
  half-carved lanterns, a sand material for the salt bed (material job), the C2 huts' irori hook sits 4-9 cm under its
  beam (old-hut baseline; fixed in the W3C2 dressings only), navmesh. Pitfalls: the shell checks C3 / C8 need real
  posts on stones (every site object got an honest timber element); kit HALF is half a KEN (0.91), the post grid is 0.455;
  gradesweep counts down-facing faces; a seat box on the work floor lets a bank sink into the rising ground; never put a
  flat ash / spill at grade under a 0.05 floor (hidden). **Walk: TEST_CHECKLIST.md = FX6 re-check (~8 min) + 3c-2
  (~20 min).** Weekly 82 % -> 84 %. Next (Stephen's call): 3d government, 3e castle, or the fishing suite.
