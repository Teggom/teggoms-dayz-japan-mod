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
  - **Pitfall for later agents:** B3b's own `spikes/B3b/build.py` rewrites config.cpp WITHOUT the L2 classes. After
    any B3b rebuild, run `python spikes/L2/build_l2.py --pack`.
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
- 2026-09-29: Waterways G1 accepted (10 decisions; research/catalogue/G1_DECISIONS.md). Map sketch: Numazu castle
  dropped, Kanō + Minakuchi castle towns added.
