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

### Phase B: foundations (parallel, after the A gate)
1. **B1. Interior materials** (through the materials pipeline and the matte recipe)
2. **B2. Missing parts, wave 1:** only what Phase C wave 1 needs (from A1)
3. **B3. Core props, wave 1:** about 20 interior + 20 outdoor, each with its abandoned state
4. **B4. Pilot:** furnish `machiya_t3_01` and dress its yard. This proves the props, proxy and loot-surface pipeline on
   a building Stephen already knows.

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
