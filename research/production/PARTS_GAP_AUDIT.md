# Parts-kit gap audit (task A1, agent PA1, 2026-09-29)

**What this is.** Every shell Stephen kept (`research/catalogue/KEEP_DWELLINGS.md`, `KEEP_TRADES.md`, `KEEP_CIVIC.md`,
and the unique shells `KEEP_LANDMARKS.md` needs) checked against the parametric parts kit. It covers which shells are
buildable today, which parts are missing (ranked), the variant axes per shell, the exact part list for Phase C wave 1,
and the kit-level risks. It is analysis only: nothing was built or changed.

**Machine-readable twin:** `parts_gap.json` (same data; one shell or part per line; about 280 KB, so parse it with
Python). Both files come from one generator script, so their numbers agree.

**Sources read:**
- `PRODUCTION_PLAN.md`, `README.md`
- the four KEEP lists
- `parts/manifest.json` (138 variants, parsed), `parts/REPORT.txt`, `parts/kit/jpparts/*.py` (the function lists; the
  roof, wall, pent and rafter code read in full)
- `buildings/machiya_t3_01/machiya_t3_01.py` and `build.py`
- `playbook/PLAYBOOK.md`: §0–6, §10, §12, §15 in full, and the G0/G1 decisions at the top
- `research/buildings/BUILDING_LIST.md`: dwellings, lodging, the precinct, government, military and civic sections,
  §5.10 and §6.1, plus greps for every trade shell
- `research/exterior/BUILD_LIST.md`

## How to read it

- **Shell:** one KEEP building model. Every KEEP number is listed.
  - `DW` = dwellings, `TR` = trades, `SH` / `BU` / `GV` / `MI` / `CV` = Shinto / Buddhist / government / military /
    civic, `WK` = the civic wall kit, `LM` = landmark-only shells.
  - ☆ = stretch. `(W1)` = in Phase C wave 1.
- **Buildable now:** every *structural* need is met by a manifest part or by a helper already proven in the machiya
  build (the tatami / board / doma / loft floors, the rear lean-to and its sloped walls, the udatsu placer, the ridge
  walk). Props, interior fittings (PA2) and materials are not counted.
- **Lacks:** new parts the base shell needs.
- **New pieces** (in the variant column): parts that only unlock extra variants. They never block a shell.
- **Score** (ranking): core shell = 2, ☆ = 1, landmark-only shell = 1.
- **Effort:** S = under half an agent session including the checks; M = about one session; L = two or more.
- **Roof framing rule** (the call that shapes the counts): a roof seen from inside needs visible framing (the koyagumi
  part) where the research says the room is open to the roof or has exposed beams. That covers farmhouses, huts,
  sheds, stables, workshops, kilns and halls, the kuri and bunk halls. Town shells (townhouses, tenements, inns,
  samurai and official houses) are assumed to have ceilings, which are PA2's.

## 1. Summary

| Group | Kit shells | Buildable now | Need 1–2 new parts | Need 3+ |
|---|---|---|---|---|
| **Core** | 104 | **15** | 72 | 17 |
| ☆ Stretch | 45 | **20** | 24 | 1 |
| Landmark-only shells | 10 | 0 | 6 | 4 |

By KEEP file (core / ☆): now, 1–2, 3+

| File | Core now / 1–2 / 3+ | ☆ now / 1–2 / 3+ |
|---|---|---|
| KEEP_DWELLINGS | 7 / 18 / 5 | 3 / 8 / 1 |
| KEEP_TRADES | 2 / 25 / 2 | 7 / 11 / 0 |
| KEEP_CIVIC (incl. wall kit) | 6 / 29 / 10 | 10 / 5 / 0 |

Four more KEEP entries are outdoor-kit items that PA3 already has on its build-first list:
- the stall kit (TR02)
- the notice board (GV6)
- the pulley and lever wells (CV6, CV7)

They aren't counted above. KEEP_TRADES 29 is only a pointer (to 22 and 10). The Kabuki theatre (KEEP_TRADES 32) is
counted once, as landmark LM04.

**Buildable today (core):** DW02 Field hut + lean-to, DW05 Hermit hut, DW10 Tōkaidō post-town house, DW22 Plastered storehouse, DW23 Board storehouse, DW27 Bath hut, DW28 Roofed well, TR01 Roadside tea house, TR14 Raised-floor bench workshop, SH5 Purification pavilion, SH6 Priests' office and amulet window, BU1 Small sacred hall, BU8 Sutra repository, GV1 Guard hut, GV3 Open-front office with yard.
**Buildable today (☆):** DW-S02 Beach hut, DW-S03 Riverbank shacks, DW-S06 Retirement cottage, TR-S01 Restaurant with garden, TR-S05 Barber and hairdresser shop, TR-S06 Palanquin station, TR-S11 Umbrella and paper drying yard, TR-S12 Bleaching field, TR-S13 Horse pasture, TR-S18 Archery gallery, SH-S2 Votive picture hall, BU-S2 Abbot's quarters, BU-S3 Benten hall on a pond island, GV-S1 Rice storehouse row, GV-S2 Courier relay post, GV-S3 Ward meeting house, MI-S1 Horse-training track, MI-S2 Coastal lookout + signal-fire post, MI-S3 Mounted-archery course, CV-S2 Charity clinic with herb garden.

**What the numbers say:**
1. **One part blocks almost half the catalogue.** The kit draws no roof framing. From inside, every roof shows only
   an eave soffit and a flat, sloped sheathing slab (`roofs.rafters(only_eave=True)`; no tie beams, purlins, ridge
   beam or sasu). The machiya hid this behind its sealed loft ceiling.
   - `jp_p_frame_koyagumi` is needed by 47 shells.
   - It is the *only* gap for 15 core shells (plus 8 ☆ / landmark shells), including
     both poor huts, the Kantō farmhouse, the shed, the smithy and the dōjō.
   - It is an M-sized generator, and it should be the first new part.
2. **Compounds need one family of four parts.** Samurai houses, the honjin, official compounds, checkpoints, the jail,
   temple gates and the ward gate need the same pieces:
   - `jp_p_open_gate_leaf`
   - `jp_p_gate`
   - `jp_p_wall_site`
   - `jp_p_porch_genkan`
   
   Those four parts appear in 17 core shells, including 8 of the 17 that need 3+
   parts. The other nine 3+ shells are:
   - six religious and castle shells (point 3)
   - the two townhouse units, which need three small wave-1 parts each
   - the logging camp
3. **Shrines, temples and the castle need a new kind of roof and frame**, not variants:
   - curved roofs (`jp_p_roof_sori`)
   - bracket sets (`jp_p_frame_kumimono`)
   - storey stacks (`jp_p_frame_storey`)
   - railed verandas and steps (`jp_p_porch_koran`)
   
   The kit is straight-slope, single-storey and rectangle-only. The village grade of the shrine and temple ladders
   (wave 2) works with straight roofs plus `koran`, `tobira` and `nagare`. The town and hero grades, the pagoda, the
   sanmon and the keep need the L-sized generators.
4. **Wave 1 is close.**
   - Today: 3 of its 12 shells are buildable (the post-town house, the kura, the roofed well; the
     small hatago too).
   - After seven parts (2 M, 5 S; §5): all of them.
   - The same seven parts plus the S-sized floor pits lift the core count from 15 to **50** of
     104.

## 2. What the kit has, and what it can't do

**Have** (138 manifest variants plus the machiya helpers):

| Family | What exists |
|---|---|
| frame | posts planed / adzed, sawn / log beams, dashigeta (flagged) |
| walls | the `wall_run` recipe (shinkabe in 3 finishes and a ranma header, okabe for kura and nuriya, vertical boards, shitami), koshiita 0.60 / 0.90, namako ×2, gables (thatch / tile / board / kura), udatsu sode / hon |
| openings | 6 plank doors, 5 paper doors, 2 lattice day doors, 4 openable window types, amado and tobukuro, kura doors and windows, mushiko ×2, koshi ×5, renji ×3, suriagedo ×3, shitomido ×2, battari ×2, upper rail, mushiro |
| found | soseki, dodai on stones, kura footing, yukashita, steps with hidden ramps; porch: engawa ×2, nure-en |
| roofs | the generator in 4 forms (kirizuma, yosemune, irimoya, kabuto) × 6 coverings (sangawara, hongawara, ishioki, itabuki, kakigara, thatch), with ridges, onigawara, hafu, 3 smoke vents, 5 pents, the kura eave and a gutter |
| trim | grime bands |

**Can't do yet** (each item below is one of the missing parts):
- **Floors and lean-tos live only in the machiya.** They are building-level code, not kit modules. The lean-to only
  does sangawara.
- **Roofs are rectangles with planar slopes.** `slopes_for()` takes W × D, with the ridge along x. There are no
  L / T / valley roofs, curves or tiers, and no holes. PLAYBOOK §10.2 promises L / T unions; they were never built.
- **No visible roof framing inside** (see §1).
- **Nothing vertical:** no stairs (the `stair_foot` / `stair_head` connectors exist only on paper) and no ladders.
- **Only two kinds of rotation door exist** (the kura `_hinged` and tsukiage), and both are engine-untested. So there
  are no gate leaves, hall doors or half-doors.
- **No free-standing structures:** site walls, gates, towers, bridges, stone platforms or ramparts, kilns, water works.
- **Shrine and temple vocabulary is missing:** railings, kizahashi steps, bracket sets, the nagare roof, ridge
  ornaments.

## 3. Missing parts, ranked

The ranking is by score: core shells count double. Ties break on how many shells the part adds variants to. "Wave 1"
says **yes** when the part is on the B2 wave-1 list (§5), and "variant" when it only adds wave-1 variety.

| # | Part | Family | New gen? | Effort | Core | ☆ | LM | Score | Variant use | Wave 1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `jp_p_frame_koyagumi` | frame (+ roofs) | yes | M | 30 | 14 | 3 | 77 | 1 | **yes** |
| 2 | `jp_p_open_gate_leaf` | openings | variant | M | 11 | 1 | 1 | 24 | 1 |  |
| 3 | `jp_p_gate` | new: gates | yes | M | 10 | 1 | 0 | 21 | 1 |  |
| 4 | `jp_p_porch_koran` | porch | yes | M | 8 | 2 | 3 | 21 | 1 |  |
| 5 | `jp_p_wall_site` | walls (site) | yes | M | 9 | 1 | 1 | 20 | 1 |  |
| 6 | `jp_p_floor_pit` | found (floors) | variant | S | 9 | 0 | 0 | 18 | 2 | variant |
| 7 | `jp_p_roof_corner` | roofs + porch | variant | S | 6 | 2 | 0 | 14 | 10 | **yes** |
| 8 | `jp_p_porch_genkan` | roofs + found | variant | M | 7 | 0 | 0 | 14 | 1 |  |
| 9 | `jp_p_bridge` | new: bridges | yes | L | 5 | 2 | 2 | 14 | 0 |  |
| 10 | `jp_p_frame_storey` | frame | yes | L | 5 | 1 | 3 | 14 | 0 |  |
| 11 | `jp_p_stair` | found (new: stairs) | yes | M | 6 | 1 | 0 | 13 | 4 | **yes** |
| 12 | `jp_p_found_kidan` | found | yes | M | 4 | 3 | 2 | 13 | 1 |  |
| 13 | `jp_p_roof_union` | roofs | variant | L | 5 | 2 | 0 | 12 | 5 | variant |
| 14 | `jp_p_wall_party` | walls | variant | S | 5 | 1 | 0 | 11 | 1 | **yes** |
| 15 | `jp_p_roof_ornament` | roofs | variant | M | 3 | 2 | 2 | 10 | 3 |  |
| 16 | `jp_p_wall_sama` | openings | variant | S | 5 | 0 | 0 | 10 | 0 |  |
| 17 | `jp_p_frame_kumimono` | frame | yes | L | 2 | 0 | 4 | 8 | 3 |  |
| 18 | `jp_p_water_sluice` | new: water | yes | M | 3 | 1 | 0 | 7 | 0 |  |
| 19 | `jp_p_found_ishigaki` | found | yes | L | 2 | 2 | 0 | 6 | 2 | variant |
| 20 | `jp_p_frame_stall` | frame | yes | S | 3 | 0 | 0 | 6 | 2 | **yes** |
| 21 | `jp_p_roof_sori` | roofs | yes | L | 1 | 0 | 3 | 5 | 5 |  |
| 22 | `jp_p_open_tobira` | openings | variant | S | 2 | 0 | 1 | 5 | 1 |  |
| 23 | `jp_p_roof_nagare` | roofs | variant | M | 2 | 1 | 0 | 5 | 0 |  |
| 24 | `jp_p_ladder` | new: vertical | yes | M | 2 | 0 | 0 | 4 | 3 | variant |
| 25 | `jp_p_roof_party_end` | roofs | variant | S | 2 | 0 | 0 | 4 | 2 | **yes** |
| 26 | `jp_p_site_shura` | site | variant | S | 2 | 0 | 0 | 4 | 1 |  |
| 27 | `jp_p_wall_lattice_cell` | walls + openings | variant | S | 2 | 0 | 0 | 4 | 1 |  |
| 28 | `jp_p_frame_stage` | frame | yes | M | 0 | 3 | 1 | 4 | 0 |  |
| 29 | `jp_p_open_lowdoor` | openings | variant | S | 2 | 0 | 0 | 4 | 0 |  |
| 30 | `jp_p_wall_palisade` | walls (site) | yes | S | 2 | 0 | 0 | 4 | 0 |  |
| 31 | `jp_p_open_shitaji` | openings | variant | S | 1 | 0 | 0 | 2 | 2 |  |
| 32 | `jp_p_open_dema` | openings | variant | S | 1 | 0 | 0 | 2 | 1 |  |
| 33 | `jp_p_frame_tower` | frame | yes | M | 1 | 0 | 0 | 2 | 0 |  |
| 34 | `jp_p_mech_waterwheel` | new: mechanisms | yes | M | 1 | 0 | 0 | 2 | 0 |  |
| 35 | `jp_p_open_halfdoor` | openings | variant | S | 1 | 0 | 0 | 2 | 0 | **yes** |
| 36 | `jp_p_open_harimise` | openings | variant | S | 1 | 0 | 0 | 2 | 0 |  |
| 37 | `jp_p_site_adit` | new: site | yes | M | 1 | 0 | 0 | 2 | 0 |  |
| 38 | `jp_p_site_kiln_climbing` | site | variant | M | 1 | 0 | 0 | 2 | 0 |  |
| 39 | `jp_p_site_kiln_dome` | new: site | yes | M | 1 | 0 | 0 | 2 | 0 |  |
| 40 | `jp_p_site_kiln_shaft` | site | variant | S | 1 | 0 | 0 | 2 | 0 |  |
| 41 | `jp_p_site_kiln_updraught` | site | variant | S | 1 | 0 | 0 | 2 | 0 |  |
| 42 | `jp_p_site_stone_hokora` | site (shares PA3 stone-lantern kit) | yes | M | 1 | 0 | 0 | 2 | 0 |  |
| 43 | `jp_p_wall_drystone` | walls | variant | S | 1 | 0 | 0 | 2 | 0 |  |
| 44 | `jp_p_open_katomado` | openings | variant | S | 0 | 1 | 0 | 1 | 4 |  |
| 45 | `jp_p_found_stilts` | found | variant | S | 0 | 0 | 1 | 1 | 2 |  |
| 46 | `jp_p_state_damage` | trim (all families) | yes | M | 0 | 0 | 0 | 0 | 12 | variant |
| 47 | `jp_p_open_mairado` | openings | variant | S | 0 | 0 | 0 | 0 | 7 | variant |
| 48 | `jp_p_open_hood` | openings | variant | S | 0 | 0 | 0 | 0 | 5 | variant |
| 49 | `jp_p_roof_hafu_decor` | roofs | yes | L | 0 | 0 | 0 | 0 | 5 |  |
| 50 | `jp_p_roof_forms_katayosemune` | roofs | variant | S | 0 | 0 | 0 | 0 | 3 | variant |
| 51 | `jp_p_floor_sunoko` | found (floors) | variant | S | 0 | 0 | 0 | 0 | 2 | variant |
| 52 | `jp_p_open_shitomi_grid` | openings | variant | S | 0 | 0 | 0 | 0 | 2 |  |
| 53 | `jp_p_wall_takahe` | walls | variant | S | 0 | 0 | 0 | 0 | 2 | variant |
| 54 | `jp_p_roof_forms_hogyo` | roofs | variant | S | 0 | 0 | 0 | 0 | 1 |  |

**Materials the missing parts need.** These go through the materials pipeline with the T12 matte / glossy finish rule;
none exist yet:
- copper tile (green patina; glossy, vanilla rusty-metal analogue) for keeps (Nagoya, Edo)
- shu vermilion paint (shrines, some gates, the sacred bridge)
- hiwada cypress bark (shrine roofs)
- gold leaf (the shachi)
- `jp_m_wall_shikkui_int` (T6 gap). It is B1's, but kura and nurigome interiors in wave 1 wait on it.
- optionally a cedar-bark roof covering for huts (verify the period)

### Part details

**1. `jp_p_frame_koyagumi`** (frame (+ roofs); new generator; effort M)
- What: Visible roof framing for rooms open to the roof: log or sawn tie beams (hari / ushibari), purlins, ridge beam, struts (tsuka), full-length rafters under tile/board roofs, sasu A-frames + bamboo lath under thatch; the jōya core + geya aisle split under one slope; sooted variant (W5). Reads roofs.roof()'s info dict. Today every roof is only an eave soffit plus a flat sheathing slab seen from inside.
- Period form: BUILDING_LIST: tenant hut 'no ceiling (open to soot-black thatch)' (§3 poor); Hida 'big smoke-black beams'; kuri 'huge earth-floored kitchen with exposed beams and a smoke gable'; smithy 'soot, roof smoke vent'
- Needed by: DW01, DW30, DW04, DW06, DW07, DW08, DW09, DW16, DW17, DW24, DW25, DW-S01, DW-S04, DW-S05, DW-S09, DW-S10, TR03, TR09, TR11, TR12, TR13, TR15, TR16, TR17, TR18, TR19, TR20, TR21, TR22, TR24, TR27, TR28, TR-S02, TR-S03, TR-S04, TR-S07, TR-S08, TR-S09, TR-S10, TR-S14, TR-S16, BU3, MI8, MI9, LM04, LM05, LM06
- Enables variants on: BU2

**2. `jp_p_open_gate_leaf`** (openings; variant of an existing generator; effort M)
- What: Hinged gate leaves (monpi) as rotation doors: board pair, iron-strapped / studded (castle), lattice (kido); decorative kuguri wicket (D9), bar. Generalises the kura _hinged rotation leaf (engine-untested).
- Period form: BUILDING_LIST kido 'posts, beam, two leaves plus a wicket'; kōrai-mon 'iron-plated doors, bar, wicket'
- Needed by: DW15, DW19, DW20, DW29, DW-S08, TR06, BU5, GV2, GV4, GV5, GV7, MI4, LM01
- Enables variants on: BU4

**3. `jp_p_gate`** (new: gates; new generator; effort M)
- What: Gate structure generator: munamon / yakui-mon (main + control posts, gable roof), shikyaku-mon, kabuki-mon (beam, no roof), kōrai-mon (roofs over the swung leaves), kido (posts + tie beam); roof families from roofs.roof.
- Period form: BUILDING_LIST castle 'Other gates: yakui-mon, kabuki-mon... also front samurai houses and honjin'; KEEP_CIVIC Buddhist 5 small gate (yakui-mon / shikyaku-mon)
- Needed by: DW15, DW19, DW20, DW-S08, TR06, BU5, GV2, GV4, GV5, GV7, MI4
- Enables variants on: DW14

**4. `jp_p_porch_koran`** (porch; new generator; effort M)
- What: Railed raised veranda (kōran: plain, giboshi posts, hane-kōran) and kizahashi wooden steps with side rails; also bridge and stage railings.
- Period form: BUILDING_LIST honden 'veranda (en) with rail, steps'; Nihonbashi 'bronze finials (giboshi) on railings'
- Needed by: SH2, SH3, SH4, BU2, BU4, BU7, CV2, CV5, SH-S1, SH-S3, LM01, LM03, LM10
- Enables variants on: BU1

**5. `jp_p_wall_site`** (walls (site); new generator; effort M)
- What: Free-standing compound walls: dobei (earth/plaster, tile cap, port bays), tsuiji-bei (tile-capped earthen, 0-5 sujibei lines), neri-bei, itabei board fence with a small cap; footings, corners, gate junctions, ruin state. Reuses walls.kawara_cap and okabe.
- Period form: KEEP_CIVIC walls table; BUILDING_LIST dobei 'tile-capped; loopholes every 1-2 ken'; lower samurai 'board fence'
- Needed by: DW15, DW19, DW20, DW-S08, TR06, GV2, GV5, MI5, WK3, WK4, LM10
- Enables variants on: DW14

**6. `jp_p_floor_pit`** (found (floors); variant of an existing generator; effort S)
- What: Openings in the promoted floor module: irori / goma hearth pits, sunken vats (indigo, tannery), casting and saw pits, stone-lined bath / spring pools, drain floors; stairwell holes. The fitting inside is PA2's.
- Period form: BUILDING_LIST: indigo dyer 'vats sunk into the floor'; foundry 'casting pit'; sawyer's pit; hot-spring bath 'stone- or wood-lined pool'; sentō 'board floor sloping to drains'
- Needed by: TR07, TR08, TR10, TR12, TR15, TR16, TR17, TR24, CV13
- Enables variants on: DW07, DW27

**7. `jp_p_roof_corner`** (roofs + porch; variant of an existing generator; effort S)
- What: Corner pieces for the linear parts: hip-jointed pent (hisashi) corner, engawa + amado-track corner, kura-eave corner, so pents and verandas wrap two faces.
- Period form: BUILD_LIST roof 17 (Ioka: 'pent roofs front and side' [E03]; Sasaki: board eaves front and rear [E02]); PLAYBOOK §10.3 engawa
- Needed by: DW11, DW12, DW18, DW20, DW-S07, DW-S08, TR31, MI6
- Enables variants on: DW06, DW10, DW13, DW15, DW16, DW17, DW19, TR01, TR05, TR06

**8. `jp_p_porch_genkan`** (roofs + found; variant of an existing generator; effort M)
- What: Formal entrance porch: a projecting gable roof on posts perpendicular to the main roof (joins it by valley or flashing), with a shikidai board step. Status feature: samurai, official, honjin, temple kuri only.
- Period form: BUILDING_LIST honjin 'genkan with shikidai step'; mid-rank samurai 'genkan with shikidai'; bugyōsho 'genkan'; PLAYBOOK §2.2 status overlay
- Needed by: DW16, DW17, DW19, DW20, TR06, BU3, GV2
- Enables variants on: MI6

**9. `jp_p_bridge`** (new: bridges; new generator; effort L)
- What: Bridge generator: deck + pier bents with nuki bracing, plank / trestle / arched (curved deck) / earth-covered / boat-bridge / cantilever (Saruhashi) / vine; railings via KORAN.
- Period form: KEEP_CIVIC civic 1-5; BUILDING_LIST 'plank bridge', 'large wooden trestle bridge (Nihonbashi type)', 'cantilever bridge (hane-bashi): Saruhashi'
- Needed by: CV1, CV2, CV3, CV4, CV5, SH-S3, CV-S3, LM07, LM08

**10. `jp_p_frame_storey`** (frame; new generator; effort L)
- What: Storey-stack module: a full storey on the one below with floor slab, mid-level skirt roof (mokoshi / hakama) or railed balcony, shrinking plan; keeps, turrets, sanmon, drum tower, pagoda, 2-storey kura.
- Period form: BUILDING_LIST keep '3-5 storeys... outer walkway strip'; sanmon 'two-storey'; drum tower 'two-storey pavilion'; pagoda 'upper floors are timber lattice and ladders'
- Needed by: BU4, BU7, MI1, MI2, MI4, BU-S1, LM01, LM03, LM05

**11. `jp_p_stair`** (found (new: stairs); new generator; effort M)
- What: Stair with a hidden ≤38° walk ramp, ≥1.10 m wide, ≥2.05 m headroom (D4): box stair (hako-kaidan / kaidan-dansu look), steep open stair for kura lofts and towers, stairwell opening + guard rail; stair_foot / stair_head connectors (PLAYBOOK §10.2 already names them).
- Period form: PLAYBOOK G1-5 (kura lofts by stair or ladder; one grand inn per T3 town); BUILDING_LIST sanmon 'steep stair in a side hut', keep 'very steep stairs', drum tower 'stair', shop 'staircase chest (kaidan-dansu)'
- Needed by: TR03, TR05, TR31, BU4, MI1, MI2, BU-S1
- Enables variants on: DW04, DW22, TR08, TR30

**12. `jp_p_found_kidan`** (found; new generator; effort M)
- What: Cut-stone platform / podium and stone flights: bell-tower and hall platforms, notice-board plinths, quay steps (gangi), slips and ferry ramps, approach stairs (with hidden walk ramps).
- Period form: BUILDING_LIST bell tower 'on a stone platform'; notice board 'on a stone plinth'; quay 'stone steps into a canal or river'; ferry landing 'stone or earth ramp'
- Needed by: DW-S10, TR-S10, BU6, CV10, CV11, CV12, CV-S1, LM05, LM09
- Enables variants on: BU7

**13. `jp_p_roof_union`** (roofs; variant of an existing generator; effort L)
- What: L / T / parallel footprints in roofs.roof(): valleys (tani) in all six coverings, hip-to-gable intersections, parallel roofs joined by a gutter, one collision slab per convex piece. slopes_for() is rectangles only today.
- Period form: BUILD_LIST roof 1 'footprint: rectangle or L/T union on the ken grid'; PLAYBOOK §10.2; Hikone castle stable 'long L-shaped'; bunto 'joined by a gutter roof'
- Needed by: DW19, DW20, DW-S05, DW-S08, TR06, GV2, MI6
- Enables variants on: DW07, DW16, DW17, DW18, TR03

**14. `jp_p_wall_party`** (walls; variant of an existing generator; effort S)
- What: Party / unit partition cut to the roof section (an interior gable-profile wall, interior materials both sides, sealed to the roof underside); a ridge-line version for back-to-back rows. Variant of walls.gable.
- Period form: KEEP_DWELLINGS 3/11/12/13 (tenement units, snap-together townhouse units, street-front rows); BUILDING_LIST 'back-to-back ridge-split tenement (mune-wari nagaya)'
- Needed by: DW03, DW11, DW12, DW13, DW14, DW-S01
- Enables variants on: DW10

**15. `jp_p_roof_ornament`** (roofs; variant of an existing generator; effort M)
- What: Ridge ornaments: chigi + katsuogi (shrines, Ise), shachi gold / plain (castle), hōju / roban (square halls), sōrin finial (pagoda), each with a simplified shape in every LOD (T7b).
- Period form: BUILDING_LIST keep 'gold-leaf roof fish (shachihoko)'; Ise 'unpainted shinmei-zukuri, thatch'; pagoda 'bronze finial (sōrin)'
- Needed by: DW-S09, DW-S11, SH1, BU7, MI1, LM03, LM10
- Enables variants on: SH2, SH3, BU1

**16. `jp_p_wall_sama`** (openings; variant of an existing generator; effort S)
- What: Loopholes (triangle / square / round) with sliding covers in okabe and dobei; ishi-otoshi stone-drop bay.
- Period form: BUILDING_LIST keep 'round / triangular / square gun and arrow loopholes (sama) with sliding covers', 'stone-drop hatches (ishi-otoshi)'
- Needed by: MI1, MI2, MI3, MI4, MI5

**17. `jp_p_frame_kumimono`** (frame; new generator; effort L)
- What: Temple / shrine frame: round posts, head-tie with kibana ends, bracket sets (funa-hijiki, degumi, mitesaki), kaerumata, nageshi bands.
- Period form: BUILDING_LIST precinct entries (continuing medieval forms, era test: 'older survivors are IN'); Tōshōgū 'rich carving and colour'
- Needed by: BU4, BU7, LM01, LM02, LM03, LM05
- Enables variants on: SH2, BU2, BU6

**18. `jp_p_water_sluice`** (new: water; new generator; effort M)
- What: Sluice gate (timber frame, boards, windlass) and weir / fish-weir cribs (stone-and-timber, bamboo slats).
- Period form: BUILDING_LIST 'Water gate / sluice', 'Weir (seki / iseki)'; KEEP_TRADES fish weir (yana)
- Needed by: TR04, TR-S15, CV8, CV9

**19. `jp_p_found_ishigaki`** (found; new generator; effort L)
- What: Stone rampart module: battered face with curved batter, sangi-zumi corners, nozura / uchikomi-hagi / kirikomi-hagi faces, overgrown ruin state; low revetment variant for mounds and terraces.
- Period form: KEEP_CIVIC walls (ishigaki; technique variants in OUTDOOR_LIST); BUILDING_LIST 'keep base without a keep: a bare stone platform'; flood-country 'house on a mound'
- Needed by: DW-S04, DW-S12, MI7, WK1
- Enables variants on: DW22, MI1

**20. `jp_p_frame_stall`** (frame; new generator; effort S)
- What: Stable fittings: stall posts, removable bar rails (mase-bō), board stall partitions, manger trough; for inside stables, detached stables and inn stables. Structural built-in (coordinate the manger with PA2).
- Period form: BUILDING_LIST: farmhouse with inside stable ('horse lives in a doma corner'), Kinai 'ox stall in the niwa', castle stable 'stalls with boards and posts'
- Needed by: DW07, DW25, TR09
- Enables variants on: DW06, DW10

**21. `jp_p_roof_sori`** (roofs; new generator; effort L)
- What: Curved roof generator: sori eave curve, corner upswing, layered thick eave, two-tier rafters; hongawara, thick kokera, hiwada bark, copper. Needs its own tile bed + fascia (T1) and silhouette LODs (T7b).
- Period form: BUILD_LIST 'Later: curved kokera and bark roofs'; PLAYBOOK §6.1 'Temples and shrines use the curved, thick-edged kokera form'
- Needed by: BU7, LM01, LM03, LM05
- Enables variants on: SH2, SH3, BU2, BU4, BU6

**22. `jp_p_open_tobira`** (openings; variant of an existing generator; effort S)
- What: Hinged board double doors (ita-tobira) and framed panel doors (sankarado) for halls, honden and stores; static + rotation. Built on the gate-leaf builder.
- Period form: BUILDING_LIST honden 'closed inner doors with metal fittings'
- Needed by: SH3, BU2, LM05
- Enables variants on: BU1

**23. `jp_p_roof_nagare`** (roofs; variant of an existing generator; effort M)
- What: Asymmetric gable with the front slope run out over the steps (nagare-zukuri) and a kōhai step canopy for any hall front.
- Period form: BUILDING_LIST honden 'steps with a small roof (kōhai) in nagare style'
- Needed by: DW-S11, SH1, SH3

**24. `jp_p_ladder`** (new: vertical; new generator; effort M)
- What: Fixed ladder using the engine's ladder action (vanilla ladders[] config + memory points); wood / bamboo. Never tested in this pipeline.
- Period form: BUILDING_LIST fire tower 'with ladder'; fire ladder with bell; lighthouse lantern 'ladder'; G1-5 kura lofts
- Needed by: GV8, CV12
- Enables variants on: DW22, TR03, GV1

**25. `jp_p_roof_party_end`** (roofs; variant of an existing generator; effort S)
- What: Flush roof end at a party line for abutting units: no sode-gawara verge, no hafu; a ridge-end cap and a flashing/step closure where neighbouring ridges differ in height. Variant of the roof generator's verge.
- Period form: KEEP_DWELLINGS 11/12 ('snap-together units'); PLAYBOOK §6.2 udatsu between adjoining town houses
- Needed by: DW11, DW12
- Enables variants on: DW10, DW13

**26. `jp_p_site_shura`** (site; variant of an existing generator; effort S)
- What: Log / stone slide chute (shura) on trestles or ground rails.
- Period form: KEEP_TRADES 24 'timber slide'; BUILDING_LIST quarry 'slide (shura) track'
- Needed by: TR24, TR25
- Enables variants on: TR20

**27. `jp_p_wall_lattice_cell`** (walls + openings; variant of an existing generator; effort S)
- What: Heavy square-timber lattice wall module (single and double lattice) with a sliding lattice door ≥1.00 m and a food hatch.
- Period form: BUILDING_LIST §5.10 'One lattice cell front as a wall module (jails, holding rooms, sekisho jail, pilgrim-hall fronts)'; jail 'double timber lattice cells'
- Needed by: GV4, GV5
- Enables variants on: GV2

**28. `jp_p_frame_stage`** (frame; new generator; effort M)
- What: Theatre and stage elements: raised stage, hanamichi runway, box-seat grid, yagura drum box over the entrance, sajiki stands, noh bridgeway.
- Period form: BUILDING_LIST kabuki 'drum tower (yagura) over the entrance; pit floor with box seating... hanamichi'
- Needed by: TR-S16, TR-S17, SH-S1, LM04

**29. `jp_p_open_lowdoor`** (openings; variant of an existing generator; effort S)
- What: Decorative low openings (D9): bathhouse zakuro-guchi (gabled), tea-hut nijiri-guchi, gate kuguri; always beside a normal D1 door.
- Period form: BUILDING_LIST sentō 'low gabled pomegranate door (zakuro-guchi)'; tea hut 'crawl-in door (nijiriguchi)'
- Needed by: DW21, TR08

**30. `jp_p_wall_palisade`** (walls (site); new generator; effort S)
- What: Wooden palisade (saku): sharpened stakes on rails, bar gate; lake-shore and hill runs.
- Period form: BUILDING_LIST sekisho 'palisades (saku) from the mountain to the lake'
- Needed by: GV4, WK2

**31. `jp_p_open_shitaji`** (openings; variant of an existing generator; effort S)
- What: Shitaji-mado: unplastered reed-lath window in an earth wall with a paper panel inside; round / cusped outlines share KATO.
- Period form: BUILDING_LIST tea hut (Rikyū-type tea rooms, 'small mat room'); form assumed from surviving 17th-c. tea rooms
- Needed by: DW21
- Enables variants on: DW05, DW-S07

**32. `jp_p_open_dema`** (openings; variant of an existing generator; effort S)
- What: Projecting barred window with a small hood (nagaya-mon, guardhouses, official fronts); degoshi + mini_pent.
- Period form: BUILDING_LIST bugyōsho 'black nagaya-mon gate with guard rooms' (window form assumed)
- Needed by: DW29
- Enables variants on: GV2

**33. `jp_p_frame_tower`** (frame; new generator; effort M)
- What: Tapering four-leg timber tower with nuki braces, platform, railing, small roof and a ladder; 6 / 7.5 / 9.1 m.
- Period form: BUILDING_LIST fire watchtower 'four-leg tapering timber tower with ladder, small roofed platform on top'; PLAYBOOK §4 fire tower heights
- Needed by: GV8

**34. `jp_p_mech_waterwheel`** (new: mechanisms; new generator; effort M)
- What: Water wheel (undershot / overshot), axle, flume (kakehi) on trestles; static first.
- Period form: BUILDING_LIST water mill 'undershot or overshot wheel, cam shaft... sluice gate' [T38]
- Needed by: TR04

**35. `jp_p_open_halfdoor`** (openings; variant of an existing generator; effort S)
- What: Half-height hinged board door for toilets and booths (static open + rotation), in a bay that keeps D1, or a declared non-enterable booth. Needs Stephen's D1 call for tiny shells.
- Period form: BUILDING_LIST: 'urban shared toilets with half doors'; alley court 'shared toilet with half-height doors'
- Needed by: DW26

**36. `jp_p_open_harimise`** (openings; variant of an existing generator; effort S)
- What: Full-height display lattice front (harimise) over a raised floor; variant of koshi _degoshi.
- Period form: KEEP_TRADES 30 'latticed front room (harimise): the signature look'
- Needed by: TR30

**37. `jp_p_site_adit`** (new: site; new generator; effort M)
- What: Timber-framed mine adit portal into a rock face, drainage trough, spoil-heap edge.
- Period form: KEEP_TRADES 27 mine site 'adit, sorting shed'
- Needed by: TR27

**38. `jp_p_site_kiln_climbing`** (site; variant of an existing generator; effort M)
- What: Climbing kiln: stepped chambers up a slope with firebox and side stoke holes.
- Period form: BUILDING_LIST 'stepped multi-chamber kiln with firebox' [T37]
- Needed by: TR18

**39. `jp_p_site_kiln_dome`** (new: site; new generator; effort M)
- What: Earth-dome charcoal kiln with flue and fire mouth (the base of the kiln family).
- Period form: BUILDING_LIST 'earth or clay dome kiln with a flue' [WORLD_CATALOGUE]
- Needed by: TR23

**40. `jp_p_site_kiln_shaft`** (site; variant of an existing generator; effort S)
- What: Stone / earth shaft lime kiln.
- Period form: BUILDING_LIST lime burner 'stone or earth shaft lime kiln'
- Needed by: TR26

**41. `jp_p_site_kiln_updraught`** (site; variant of an existing generator; effort S)
- What: Small updraught tile kiln (daruma type; form to verify for 1730).
- Period form: BUILDING_LIST roof-tile maker 'small updraught or daruma kiln (verify form for 1730)'
- Needed by: TR19

**42. `jp_p_site_stone_hokora`** (site (shares PA3 stone-lantern kit); new generator; effort M)
- What: Carved stone micro-shrine (roof stone, body with door recess, base) in 4 variants.
- Period form: KEEP_CIVIC Shinto 1 'micro-shrine: 4 stone variants'; BUILDING_LIST hokora 'miniature wooden or stone shrine house 0.3-1 m high on a stone base'
- Needed by: SH1

**43. `jp_p_wall_drystone`** (walls; variant of an existing generator; effort S)
- What: Piled dry-stone wall recipe (summit huts, windbreaks, field terraces, ruin courses).
- Period form: BUILDING_LIST summit shrine 'windbreak stone wall'; KEEP_LANDMARKS Fuji pilgrim huts
- Needed by: MI7

**44. `jp_p_open_katomado`** (openings; variant of an existing generator; effort S)
- What: Cusped (katōmado) and round (maru-mado) window outlines for Zen / Ōbaku halls, academy, tea hut, villa; a new outline for the plastered-panel opening.
- Period form: BUILDING_LIST Ōbaku 'Chinese lattice railings, peach-shaped openings... very current in 1730'
- Needed by: CV-S1
- Enables variants on: DW05, DW21, DW-S07, BU2

**45. `jp_p_found_stilts`** (found; variant of an existing generator; effort S)
- What: Tall stilt floor (≥1 m) on posts with rat guards (nezumi-gaeshi); variant of yukashita.
- Period form: BUILDING_LIST gōkura 'on short posts with rat guards'; treasure store 'on stilts'
- Needed by: LM10
- Enables variants on: DW23, SH3

**46. `jp_p_state_damage`** (trim (all families); new generator; effort M)
- What: Abandoned-state geometry: broken or missing amado and door leaves, missing shutter boards, holed thatch and shingles with lath showing, fallen plaster exposing komai lath, a sagging lean-to. Keeps every C10/C11 rule.
- Period form: KEEP_LANDMARKS dead-world dressing 'shutters half-open or broken'; KEEP_OUTDOOR damage / ruin multiplier
- Needed by: none (variety piece)
- Enables variants on: DW01, DW30, DW02, DW03, DW06, DW07, DW08, DW09, DW24, DW25, DW-S03, TR01

**47. `jp_p_open_mairado`** (openings; variant of an existing generator; effort S)
- What: Mairado: sliding board door faced with fine horizontal battens (twin / single / shutter); a leaf_plank style.
- Period form: (assumed; the standard Edo-period board door on samurai houses and temples; verify with a dated source)
- Needed by: none (variety piece)
- Enables variants on: DW15, DW19, DW20, DW29, TR05, TR06, GV2

**48. `jp_p_open_hood`** (openings; variant of an existing generator; effort S)
- What: Window hood (mado-bisashi): a small board / tile / stone-weighted pent over any window; openings.mini_pent generalised.
- Period form: BUILD_LIST 37 kura window 'tiny tile pent' (house use assumed)
- Needed by: none (variety piece)
- Enables variants on: DW01, DW30, DW06, DW11, DW12

**49. `jp_p_roof_hafu_decor`** (roofs; new generator; effort L)
- What: Decorative gables: chidori-hafu (triangular gable on a slope) and kara-hafu (cusped gable) for keeps, turrets, karamon and elite genkan.
- Period form: BUILDING_LIST Tōshōgū 'a karamon'; mausoleum 'karamon'; KEEP_CIVIC military keep
- Needed by: none (variety piece)
- Enables variants on: DW19, DW20, MI1, MI2, MI6

**50. `jp_p_roof_forms_katayosemune`** (roofs; variant of an existing generator; effort S)
- What: Roof form with a gable at one end and a hip at the other (corner townhouse / corner inn / half-hip farmhouse variant). A slopes_for() case next to kabuto, without the smoke gable.
- Period form: KEEP_DWELLINGS 11/12 corner unit (form assumed; verify against a pre-1750 street print)
- Needed by: none (variety piece)
- Enables variants on: DW11, DW12, TR05

**51. `jp_p_floor_sunoko`** (found (floors); variant of an existing generator; effort S)
- What: Split-bamboo slat floor (take-yuka / sunoko) as a floor-module variant; the doza straw-on-earth look is PA2 dressing.
- Period form: BUILDING_LIST: 'Kinai tenant house with bamboo floor (take-yuka / sunoko-yuka)'; KEEP_DWELLINGS 1 floor axis
- Needed by: none (variety piece)
- Enables variants on: DW01, DW30

**52. `jp_p_open_shitomi_grid`** (openings; variant of an existing generator; effort S)
- What: Grid-lattice hinged-up shutters for halls (temple shitomi); variant of the shop shitomido.
- Period form: BUILD_LIST 42 shitomido (Inoue house 1721 [E13]); temple form older (assumed)
- Needed by: none (variety piece)
- Enables variants on: SH2, BU2

**53. `jp_p_wall_takahe`** (walls; variant of an existing generator; effort S)
- What: Yamato-mune: tile-capped plastered parapets flanking a steep thatch gable, over tiled lower roofs; variant of udatsu _hon.
- Period form: BUILDING_LIST Kinai headman 'thatch main roof with tiled lower roofs, white plaster' (Yoshimura house; reading as yamato-mune: verify)
- Needed by: none (variety piece)
- Enables variants on: DW07, DW17

**54. `jp_p_roof_forms_hogyo`** (roofs; variant of an existing generator; effort S)
- What: Pyramidal roof form (hōgyō) for square halls and pavilions, with a hōju finial (ORN).
- Period form: KEEP_CIVIC Buddhist 1 small sacred hall 2x2 / 3x3 bays (form assumed; common on Jizō / Kannon halls)
- Needed by: none (variety piece)
- Enables variants on: BU1

## 4. Per shell

The bundles in "Uses" expand to exact manifest IDs in the legend at the end of this section, and in
`parts_gap.json` (`parts_have`).

### Dwellings (KEEP_DWELLINGS)

| ID | Shell | Uses (bundles, see legend) | Lacks | Build now? | Variant axes |
|---|---|---|---|---|---|
| DW01 (W1) | Rural hut, east type (thatch, hipped), 2 sizes | `rural_base`, `thatch_hip`, `pent_skirt` | **frame_koyagumi** | no (1) | floor earth / board / bamboo slats (floor_sunoko); coastal: board walls + ishioki roof; thatch ridge bamboo / shiba / umanori; door itado plain / mushiro; wear: thatch_body_new, _w2 · *new pieces:* floor_sunoko, state_damage, open_hood · *note:* irori pit hole (floor_pit) for PA2's hearth |
| DW30 (W1) | Rural hut, west/mountain type (gable, board walls, side lean-to) | `rural_base`, `thatch_gable`, `gable_thatch`, `gable_board`, `ishioki`, `itabuki`, `helper:leanto` | **frame_koyagumi** | no (1) | roof thatch gable / ishioki / itabuki; lean-to left / right / none; board plain / battened; renji bamboo / tsukiage · *new pieces:* floor_sunoko, state_damage, open_hood · *note:* lean-to helper must learn board/thatch coverings (sangawara only today) |
| DW02 | Field hut + lean-to | `rural_base`, `thatch_gable`, `ishioki`, `itabuki`, `helper:leanto` | — | **yes** | open lean-to front; roof thatch / board / stone-weighted; per-role dressing · *new pieces:* state_damage · *note:* ≤1.5 ken: a plank door needs a 2-ken wall (door + park bay); use an open front |
| DW03 | Back-alley tenement kit (ura-nagaya) | `town_base`, `itabuki`, `sangawara`, `gable_board`, `soseki` | **wall_party** | no (1) | 1- / 2-room / empty unit; roof itabuki plain / bamboo / kakigara / sangawara; front: koshidaka shoji single / itado single; ridge-split (mune-wari) via wall_party on the ridge · *new pieces:* state_damage · *note:* 1.5-ken unit front = exactly one katabiki door (D1 ok, no window) |
| DW04 | Bunk hall | `rural_base`, `itabuki`, `ishioki`, `thatch_gable`, `gable_board` | **frame_koyagumi** | no (1) | roof board / stone-weighted / thatch; length in ken; two-storey barracks variant (stair, G1-5 flag) · *new pieces:* stair · *note:* long irori pit (floor_pit) |
| DW05 | Hermit hut | `rural_base`, `thatch_gable`, `itabuki`, `gable_thatch`, `nureen` | — | **yes** | thatch / shingle; shitaji-mado / round window; nure-en or not · *new pieces:* open_shitaji, open_katomado |
| DW06 (W1) | Kantō farmhouse, 3-room (hiroma type) | `rural_base`, `thatch_hip`, `kabuto`, `pent_skirt`, `pent_board`, `itado_pair`, `helper:leanto` | **frame_koyagumi** | no (1) | with / without inside stable (frame_stall); hip / kabuto thatch; ridge 4 kinds, umanori count by status; skirt pent front only / front + back; silk and tea prop sets · *new pieces:* frame_stall, roof_corner, state_damage, open_hood · *note:* irori pit (floor_pit); PLAYBOOK §2.2 ≤3-ken main span vs deep thatch farmhouses: see risks |
| DW07 (W1) | Kinai farmhouse, 4-room with ox | `rural_base`, `thatch_irimoya`, `thatch_gable`, `gable_thatch`, `sangawara`, `pent_tile`, `pent_board`, `helper:leanto` | **frame_koyagumi**, **frame_stall** | no (2) | yamato-mune takahe gables (wall_takahe); add-ons: kabata room (floor_pit), kamaya, mizuya; irimoya / kirizuma thatch; tile vs board lower roofs · *new pieces:* wall_takahe, floor_pit, roof_union, state_damage |
| DW08 | Mountain board-roof house | `rural_base`, `ishioki`, `gable_board`, `pent_ishioki`, `helper:leanto` | **frame_koyagumi** | no (1) | ishioki std / worn, battens stoneset8 / sparse; board gable; Kiso dashibari (flagged, see risks) · *new pieces:* state_damage · *note:* hidana rack over the irori = PA2 |
| DW09 | Coastal house | `rural_base`, `ishioki`, `itabuki`, `thatch_gable`, `gable_board` | **frame_koyagumi** | no (1) | board walls + ishioki / thatch; net store add-on (shed); salt kit · *new pieces:* state_damage |
| DW10 (W1) | Tōkaidō post-town house (home side) | `town_base`, `sangawara`, `itabuki`, `nuriya`, `koshi`, `pent_tile`, `pent_board`, `gable_tile`, `helper:leanto`, `helper:udatsu` | — | **yes** | tiled / board roof; plastered nuriya / board front; koshi pattern; stable add-on (frame_stall); row version (wall_party + roof_party_end) · *new pieces:* frame_stall, wall_party, roof_party_end, roof_corner · *note:* detached version is the machiya pattern; zushi-nikai sealed (G0-4) |
| DW11 (W1) | Kamigata townhouse (machiya): snap-together units 2/3/4 ken + corner | `town_base`, `sangawara`, `koshi`, `mushiko`, `shopfront`, `pent_tile`, `pent_gable`, `gable_tile`, `udatsu`, `helper:leanto`, `helper:udatsu`, `helper:ridge_walk` | **wall_party**, **roof_party_end**, **roof_corner** | no (3) | frontage 2 / 3 / 4 ken; corner unit (roof_forms_katayosemune + roof_corner); lattice kyo / oyako / komeya / bengara / degoshi; shop closure suriagedo / shitomido / open; udatsu sode / hon; onigawara plain / sui, ridge c3 / c5 · *new pieces:* roof_forms_katayosemune, open_hood · *note:* the proven machiya is a 4-ken end unit; the corner unit needs the pent to wrap (roof_corner), a gable on the side street is fine |
| DW12 (W1) | Edo townhouse (machiya): snap-together units | `town_base`, `sangawara`, `itabuki`, `nuriya`, `koshi`, `shopfront`, `pent_tile`, `pent_board`, `dashigeta`, `gable_tile`, `gable_board`, `helper:leanto` | **wall_party**, **roof_party_end**, **roof_corner** | no (3) | tile / board / kakigara roof (1730 Edo ~half tiled); nuriya plastered / board front; dashigeta (flagged); frontage 2 / 3 / 4 ken + corner (roof_corner) · *new pieces:* roof_forms_katayosemune, open_hood · *note:* nurigome room needs B1's jp_m_wall_shikkui_int (T6 gap) |
| DW13 | Street-front row (omote-nagaya) | `town_base`, `itabuki`, `sangawara`, `koshi`, `shopfront`, `pent_board`, `pent_tile`, `gable_board` | **wall_party** | no (1) | unit count; shop closure per unit; roof board / tile · *new pieces:* roof_party_end, roof_corner |
| DW14 | Foot-soldier row (kumi-yashiki) | `town_base`, `itabuki`, `sangawara`, `gable_board` | **wall_party** | no (1) | unit count; gate and fence (gate / wall_site); board / tile roof · *new pieces:* gate, wall_site |
| DW15 | Small samurai house with gate | `town_base`, `sangawara`, `itabuki`, `veranda`, `gable_tile` | **gate**, **open_gate_leaf**, **wall_site** | no (3) | plot size; gate kabuki / munamon; board fence / plaster wall; mairado doors · *new pieces:* open_mairado, roof_corner · *note:* lower samurai: 'small genkan (no shikidai)' = recessed entrance, no porch_genkan porch |
| DW16 | East headman house (thatch) | `rural_base`, `thatch_hip`, `kabuto`, `pent_skirt`, `pent_ishioki`, `veranda`, `helper:leanto` | **frame_koyagumi**, **porch_genkan** | no (2) | hip / kabuto; L wing (roof_union); net-boss / horse-dealer fills · *new pieces:* roof_union, roof_corner · *note:* shikidai 'by permission' (status); nagaya-mon = DW29; kura = DW22 |
| DW17 | Kinai headman house (thatch + tile) | `rural_base`, `thatch_irimoya`, `thatch_gable`, `sangawara`, `shikkui_walls`, `pent_tile`, `veranda`, `helper:leanto` | **frame_koyagumi**, **porch_genkan** | no (2) | yamato-mune takahe; tile lower roofs; white plaster · *new pieces:* wall_takahe, roof_union, roof_corner |
| DW18 | Great merchant residence | `town_base`, `sangawara`, `veranda`, `kura_walls`, `gable_tile`, `helper:leanto` | **roof_corner** | no (1) | garden-facing engawa wrap; wings (roof_union); attached kura · *new pieces:* roof_union |
| DW19 | Samurai mansion, 3 plot sizes | `town_base`, `sangawara`, `hongawara`, `veranda`, `irimoya`, `gable_tile` | **gate**, **open_gate_leaf**, **porch_genkan**, **wall_site**, **roof_union** | no (5) | plot size; gate yakui / kabuki / nagaya-mon; plaster + namako / board wall; kuge courtly dressing · *new pieces:* open_mairado, roof_corner, roof_hafu_decor |
| DW20 | Daimyo mansion (hero complex) | `town_base`, `hongawara`, `veranda`, `irimoya`, `kura_walls` | **gate**, **open_gate_leaf**, **porch_genkan**, **wall_site**, **roof_union**, **roof_corner** | no (6) | naka / shimo-yashiki dressing · *new pieces:* roof_hafu_decor, open_mairado · *note:* barracks = DW04 |
| DW21 | Tea hut | `rural_base`, `thatch_gable`, `itabuki`, `nureen` | **open_shitaji**, **open_lowdoor** | no (2) | thatch / kokera; round window (open_katomado); garden side · *new pieces:* open_katomado · *note:* ro hearth + tokonoma = PA2; nijiri-guchi decorative, a normal door too (D9) |
| DW22 (W1) | Plastered storehouse (dozō kura), sizes | `frame_town`, `kura_footing`, `kura_walls`, `kura_open`, `kura_eave`, `sangawara`, `hongawara`, `grime`, `helper:floors` | — | **yes** | size; sangawara / hongawara; namako imo / shihan / shitami kuro lower wall; door open / hinged; 2-storey with loft by stair or ladder (G1-5); stone kura for the powder magazine / armoury (KEEP_CIVIC military note: cut-stone face from found_ishigaki) · *new pieces:* stair, ladder, found_ishigaki · *note:* plastered interior needs B1's jp_m_wall_shikkui_int (T6 gap) |
| DW23 | Board storehouse (itagura) | `frame_rural`, `soseki`, `yukashita`, `board_walls`, `doors_rural`, `itabuki`, `sangawara`, `ishioki`, `grime`, `helper:floors` | — | **yes** | board vertical / shitami; roof board / tile; stilts + rat guards (found_stilts) · *new pieces:* found_stilts |
| DW24 (W1) | Shed / barn | `rural_base`, `itabuki`, `ishioki`, `thatch_gable`, `gable_board`, `helper:leanto` | **frame_koyagumi** | no (1) | open-sided / walled; lean-to woodshed; roof board / thatch / stone; dressed per use · *new pieces:* state_damage |
| DW25 | Stable | `rural_base`, `itabuki`, `ishioki`, `thatch_gable` | **frame_koyagumi**, **frame_stall** | no (2) | horse / ox; stall count · *new pieces:* state_damage |
| DW26 (W1) | Toilet (setchin) | `frame_rural`, `soseki`, `board_walls`, `itabuki`, `grime` | **open_halfdoor** | no (1) | rural jar pit / urban shared row; board / earth walls · *note:* D1 vs tiny booth: Stephen's call |
| DW27 | Bath hut | `rural_base`, `itabuki`, `koshiyane` | — | **yes** | board / earth walls; tub type (PA2) · *new pieces:* floor_pit |
| DW28 (W1) | Roofed well | `frame_rural`, `soseki`, `kirizuma`, `itabuki`, `sangawara` | — | **yes** | tile / board roof; stone / wood curb (PA3) · *note:* well curb + pulley are PA3's outdoor items |
| DW29 | Gatehouse with rooms (nagaya-mon) | `town_base`, `kura_walls`, `sangawara`, `hongawara`, `gable_tile` | **open_gate_leaf**, **open_dema** | no (2) | board (headman) / plaster + namako (samurai); black boards (official) · *new pieces:* open_mairado |
| ☆ DW-S01 | Rural labourers' row (kado-ya nagaya) | `rural_base`, `thatch_gable`, `itabuki` | **frame_koyagumi**, **wall_party** | no (2) | unit count; thatch / board |
| ☆ DW-S02 | Beach hut (ama-goya / bangoya) | `rural_base`, `itabuki`, `thatch_gable`, `helper:leanto` | — | **yes** | square / lean-to; board / thatch |
| ☆ DW-S03 | Riverbank shacks (kawara-goya) | `rural_base`, `helper:leanto`, `itabuki` | — | **yes** | cluster size; reed / board walls · *new pieces:* state_damage |
| ☆ DW-S04 | Flood-country farmhouse | `rural_base`, `thatch_hip`, `thatch_irimoya`, `helper:leanto` | **frame_koyagumi**, **found_ishigaki** | no (2) | mound height; escape boat under the eave (prop) |
| ☆ DW-S05 | Separate-kitchen farmhouse (bunto) | `rural_base`, `thatch_hip`, `thatch_gable` | **frame_koyagumi**, **roof_union** | no (2) | two roofs joined by a gutter |
| ☆ DW-S06 | Retirement cottage (inkyo-ya) | `rural_base`, `thatch_gable`, `itabuki`, `nureen` | — | **yes** | hut or farmhouse parts |
| ☆ DW-S07 | Merchant's suburban villa (bessō) | `town_base`, `sangawara`, `itabuki`, `veranda` | **roof_corner** | no (1) | garden wrap engawa; round windows · *new pieces:* open_katomado, open_shitaji |
| ☆ DW-S08 | Daimyo garden villa (shimo-yashiki) | `town_base`, `hongawara`, `veranda`, `irimoya` | **gate**, **open_gate_leaf**, **wall_site**, **roof_union**, **roof_corner** | no (5) | garden estate |
| ☆ DW-S09 | Shinano great house (honmune-zukuri) | `rural_base`, `ishioki`, `itabuki`, `gable_board` | **frame_koyagumi**, **roof_ornament** | no (2) | suzume-odori gable ornament · *note:* BUILDING_LIST: honmune mostly after 1750 (verify) |
| ☆ DW-S10 | Boat shed (funa-goya) | `rural_base`, `itabuki`, `thatch_gable` | **frame_koyagumi**, **found_kidan** | no (2) | slip into water |
| ☆ DW-S11 | Yard shrine (yashiki-gami / Inari hokora) | `itabuki`, `frame_town` | **roof_nagare**, **roof_ornament** | no (2) | as the wood micro-shrines (SH1) |
| ☆ DW-S12 | Flood storehouse on a mound (mizuya) | `kura_walls`, `kura_open`, `kura_eave`, `sangawara`, `kura_footing` | **found_ishigaki** | no (1) | mound height |

### Trades, lodging, services (KEEP_TRADES)

| ID | Shell | Uses (bundles, see legend) | Lacks | Build now? | Variant axes |
|---|---|---|---|---|---|
| TR01 (W2) | Roadside tea house, 3 sizes | `rural_base`, `thatch_gable`, `thatch_hip`, `itabuki`, `ishioki`, `pent_board`, `pent_skirt`, `shopfront`, `nureen`, `helper:leanto` | — | **yes** | bench shed / open shop / tateba; thatch / board / stone roof; battari bench; pass tea house = a size · *new pieces:* roof_corner, state_damage |
| TR02 | Stall kit | — | — | PA3 (KEEP_OUTDOOR 'the stall family') | — |
| TR03 | Brewery complex | `town_base`, `kura_walls`, `kura_open`, `kura_eave`, `sangawara`, `koshiyane`, `helper:leanto` | **frame_koyagumi**, **stair** | no (2) | hall count; sugidama (prop); town / country size · *new pieces:* ladder, roof_union |
| TR04 | Water mill | `rural_base`, `itabuki`, `thatch_gable` | **mech_waterwheel**, **water_sluice** | no (2) | overshot / undershot; thatch / board |
| TR05 (W1) | Inn (hatago), 2 sizes | `town_base`, `sangawara`, `itabuki`, `irimoya`, `koshi`, `pent_tile`, `pent_board`, `upper_rail`, `veranda`, `gable_tile`, `helper:leanto`, `helper:udatsu` | **stair** | no (1) | size 1 (sealed low upper, buildable now) / size 2 grand inn (full upper storey, G1-5: one per T3 town); meshimori / pilgrim sign sets; corner inn (roof_corner + roof_forms_katayosemune) · *new pieces:* roof_corner, roof_forms_katayosemune, open_mairado · *note:* size 1 is buildable now; the stair gates size 2 |
| TR06 | Honjin (+ waki-honjin) | `town_base`, `sangawara`, `hongawara`, `irimoya`, `veranda` | **gate**, **open_gate_leaf**, **porch_genkan**, **roof_union**, **wall_site** | no (5) | with / without gate (waki); garden wrap · *new pieces:* roof_corner, open_mairado |
| TR07 | Hot-spring inn + bath house | `town_base`, `sangawara`, `itabuki`, `koshiyane`, `veranda` | **floor_pit** | no (1) | bath house over a pool; inn size |
| TR08 | Public bathhouse (sentō) | `town_base`, `sangawara`, `itabuki`, `koshiyane`, `pent_tile` | **open_lowdoor**, **floor_pit** | no (2) | upstairs rest room (stair; G1-5 flag) · *new pieces:* stair |
| TR09 | Stable yard | `rural_base`, `itabuki`, `sangawara` | **frame_koyagumi**, **frame_stall** | no (2) | stall count |
| TR10 | Hot-spring bath hut | `rural_base`, `itabuki`, `thatch_gable` | **floor_pit** | no (1) | open / walled |
| TR11 (W2) | Smithy (+ swordsmith) | `rural_base`, `itabuki`, `sangawara`, `koshiyane` | **frame_koyagumi** | no (1) | dark forge room (swordsmith); open front · *note:* forge = specialty prop built with the shell |
| TR12 | Foundry | `rural_base`, `itabuki`, `koshiyane` | **frame_koyagumi**, **floor_pit** | no (2) | casting pit |
| TR13 | Earth-floor workshop | `town_base`, `itabuki`, `sangawara`, `koshiyane` | **frame_koyagumi** | no (1) | dressed per trade |
| TR14 | Raised-floor bench workshop | `town_base`, `itabuki`, `sangawara`, `koshi` | — | **yes** | dressed per trade |
| TR15 | Timber yard | `rural_base`, `itabuki` | **frame_koyagumi**, **floor_pit** | no (2) | sawpit; open log sheds |
| TR16 | Tannery | `rural_base`, `itabuki`, `koshiyane` | **frame_koyagumi**, **floor_pit** | no (2) | pits; smoke hut |
| TR17 | Dyer's yard | `town_base`, `itabuki`, `sangawara` | **frame_koyagumi**, **floor_pit** | no (2) | sunken vats |
| TR18 | Pottery kiln site | `rural_base`, `itabuki`, `thatch_gable` | **frame_koyagumi**, **site_kiln_climbing** | no (2) | chamber count |
| TR19 | Tile works | `rural_base`, `sangawara`, `itabuki` | **frame_koyagumi**, **site_kiln_updraught** | no (2) | long drying sheds |
| TR20 | Stonemason's yard | `rural_base`, `itabuki` | **frame_koyagumi** | no (1) | shed + open yard · *new pieces:* site_shura |
| TR21 | Paper mill | `rural_base`, `itabuki`, `thatch_gable` | **frame_koyagumi** | no (1) | drying boards (props) |
| TR22 | Salt works | `rural_base`, `itabuki`, `koshiyane` | **frame_koyagumi** | no (1) | boiling hut |
| TR23 | Charcoal kiln site | `rural_base`, `thatch_gable`, `helper:leanto` | **site_kiln_dome** | no (1) | kiln + field hut |
| TR24 | Logging camp | `rural_base`, `itabuki`, `ishioki` | **frame_koyagumi**, **floor_pit**, **site_shura** | no (3) | bunk hall + sawpit + slide |
| TR25 | Quarry | `rural_base`, `itabuki` | **site_shura** | no (1) | rock face (terrain) |
| TR26 | Lime kiln | `rural_base`, `itabuki` | **site_kiln_shaft** | no (1) | stone / earth shaft |
| TR27 | Mine site | `rural_base`, `itabuki`, `ishioki` | **frame_koyagumi**, **site_adit** | no (2) | gold (Izu / Kai) / sulphur (Hakone) |
| TR28 | Bonito smokehouse | `rural_base`, `itabuki`, `koshiyane` | **frame_koyagumi** | no (1) | smoke racks (props) |
| TR30 | Brothel house with harimise | `town_base`, `sangawara`, `koshi`, `pent_tile`, `upper_rail` | **open_harimise** | no (1) | upper storey (stair; G1-5 flag) · *new pieces:* stair |
| TR31 | Banquet house (ageya) | `town_base`, `sangawara`, `koshi`, `veranda`, `upper_rail` | **stair**, **roof_corner** | no (2) | Sumiya-plan upper rooms (G1-5 flag) |
| ☆ TR-S01 | Restaurant with garden (ryōri-jaya) | `town_base`, `sangawara`, `veranda` | — | **yes** | garden engawa |
| ☆ TR-S02 | Market hall | `rural_base`, `itabuki` | **frame_koyagumi** | no (1) | bay count |
| ☆ TR-S03 | Country sake brewer | `town_base`, `kura_walls`, `sangawara`, `koshiyane` | **frame_koyagumi** | no (1) | small brewery |
| ☆ TR-S04 | Pilgrim lodge (shukubō / oshi house) | `rural_base`, `thatch_hip`, `veranda` | **frame_koyagumi** | no (1) | headman-house parts |
| ☆ TR-S05 | Barber and hairdresser shop | `town_base`, `itabuki`, `shopfront` | — | **yes** | corner booth |
| ☆ TR-S06 | Palanquin station (kago-ya) | `town_base`, `itabuki` | — | **yes** | open shed front |
| ☆ TR-S07 | Loom house | `town_base`, `itabuki`, `sangawara` | **frame_koyagumi** | no (1) | Nishijin rich variant |
| ☆ TR-S08 | Oil and candle works | `town_base`, `itabuki` | **frame_koyagumi** | no (1) | press (prop) |
| ☆ TR-S09 | Cooperage | `town_base`, `itabuki` | **frame_koyagumi** | no (1) | — |
| ☆ TR-S10 | Boatbuilder's yard | `rural_base`, `itabuki` | **frame_koyagumi**, **found_kidan** | no (2) | slip |
| ☆ TR-S11 | Umbrella and paper drying yard | `rural_base`, `itabuki` | — | **yes** | mostly props |
| ☆ TR-S12 | Bleaching field (sarashi-ba) | — | — | **yes** | props / terrain |
| ☆ TR-S13 | Horse pasture (maki) | `rural_base`, `itabuki` | — | **yes** | fences (PA3) + herder's hut |
| ☆ TR-S14 | Tea processing shed | `rural_base`, `itabuki`, `thatch_gable` | **frame_koyagumi** | no (1) | — |
| ☆ TR-S15 | River fish weir house (yana) | `rural_base`, `itabuki` | **water_sluice** | no (1) | weir + watch hut |
| ☆ TR-S16 | Puppet theatre | `town_base`, `sangawara` | **frame_koyagumi**, **frame_stage** | no (2) | — |
| ☆ TR-S17 | Sumō arena (kanjin-zumō) | `rural_base`, `itabuki` | **frame_stage** | no (1) | stands, ring roof |
| ☆ TR-S18 | Archery gallery (yōkyūba) | `town_base`, `itabuki` | — | **yes** | verify 1730 date |

### Religious, government, military, civic, wall kit (KEEP_CIVIC)

| ID | Shell | Uses (bundles, see legend) | Lacks | Build now? | Variant axes |
|---|---|---|---|---|---|
| SH1 | Micro-shrine: 4 stone + 4 wood variants | `itabuki`, `frame_town` | **roof_nagare**, **roof_ornament**, **site_stone_hokora** | no (3) | stone / wood; fox pair, sakaki, shimenawa, small torii (props) · *note:* site objects, no interior |
| SH2 (W2) | Worship hall (haiden), 2 sizes | `town_base`, `irimoya`, `kirizuma`, `itabuki`, `sangawara`, `yukashita`, `steps` | **porch_koran** | no (1) | size; straight roof (village) / curved + brackets (town: roof_sori, frame_kumimono); wari-haiden passage · *new pieces:* roof_sori, frame_kumimono, open_shitomi_grid, roof_ornament |
| SH3 (W2) | Main sanctuary (honden), 2 sizes | `town_base`, `itabuki`, `yukashita` | **roof_nagare**, **porch_koran**, **open_tobira** | no (3) | nagare / shinmei (roof_ornament chigi) / kasuga; raised on stilts (found_stilts) · *new pieces:* found_stilts, roof_ornament, roof_sori |
| SH4 (W2) | Kagura dance stage | `town_base`, `irimoya`, `itabuki`, `yukashita` | **porch_koran** | no (1) | open sides |
| SH5 (W2) | Purification pavilion (temizuya) | `frame_town`, `kirizuma`, `itabuki`, `sangawara` | — | **yes** | tile / board; splayed posts · *note:* basin = PA3 |
| SH6 (W2) | Priests' office and amulet window | `town_base`, `itabuki`, `sangawara`, `shopfront` | — | **yes** | amulet window as a shop opening |
| BU1 (W2) | Small sacred hall, 2x2 or 3x3 bays | `town_base`, `yosemune`, `irimoya`, `itabuki`, `sangawara`, `nureen`, `koshi` | — | **yes** | hōgyō pyramid (roof_forms_hogyo + roof_ornament); lattice front (koshido) / board doors (open_tobira); railed en (porch_koran) · *new pieces:* roof_forms_hogyo, roof_ornament, open_tobira, porch_koran |
| BU2 (W2) | Main hall (hondō), 2 sizes | `town_base`, `irimoya`, `hongawara`, `yukashita`, `veranda` | **porch_koran**, **open_tobira** | no (2) | straight (village) / curved + brackets (town); sect swaps (props) · *new pieces:* roof_sori, frame_kumimono, open_shitomi_grid, open_katomado, frame_koyagumi |
| BU3 (W2) | Priests' quarters and kitchen (kuri) | `town_base`, `kirizuma`, `irimoya`, `sangawara`, `gable_tile`, `koshiyane`, `veranda` | **frame_koyagumi**, **porch_genkan** | no (2) | gable front with exposed frame; kitchen size |
| BU4 | Two-storey main gate (sanmon) | `frame_town`, `hongawara`, `irimoya` | **frame_storey**, **frame_kumimono**, **porch_koran**, **stair** | no (4) | open / leaves · *new pieces:* roof_sori, open_gate_leaf |
| BU5 (W2) | Small gate (yakui-mon / shikyaku-mon) | `frame_town`, `hongawara`, `sangawara`, `itabuki` | **gate**, **open_gate_leaf** | no (2) | yakui / shikyaku; tile / board |
| BU6 (W2) | Bell tower (shōrō) | `frame_town`, `irimoya`, `hongawara` | **found_kidan** | no (1) | open / hakama skirt (frame_storey); tile / board · *new pieces:* frame_kumimono, roof_sori · *note:* bell + striker = specialty props |
| BU7 | Pagoda, 3-storey | `frame_town`, `hongawara` | **frame_storey**, **frame_kumimono**, **roof_sori**, **roof_ornament**, **porch_koran** | no (5) | tile / bark roof · *new pieces:* found_kidan |
| BU8 | Sutra repository | `frame_town`, `kura_footing`, `kura_walls`, `kura_open`, `kura_eave`, `hongawara`, `sangawara` | — | **yes** | kura type / small hall type · *note:* rinzō = prop |
| GV1 (W2) | Guard hut | `town_base`, `itabuki`, `sangawara` | — | **yes** | prop decides: sundries / fire ladder / toll box / spyglass; 1.82 x 2.73 m (PLAYBOOK §4) · *new pieces:* ladder · *note:* the katabiki door fits the 1.5-ken side |
| GV2 | Official compound, sizes | `town_base`, `hongawara`, `sangawara`, `kura_walls`, `veranda` | **gate**, **open_gate_leaf**, **porch_genkan**, **roof_union**, **wall_site** | no (5) | with / without court + cells (wall_lattice_cell); black boards · *new pieces:* wall_lattice_cell, open_dema, open_mairado |
| GV3 | Open-front office with yard | `town_base`, `sangawara`, `itabuki`, `shopfront` | — | **yes** | toiya-ba / river-crossing / weight station |
| GV4 | Highway checkpoint kit | `town_base`, `sangawara`, `itabuki`, `veranda` | **gate**, **open_gate_leaf**, **wall_palisade**, **wall_lattice_cell** | no (4) | four named instances |
| GV5 | Jail compound | `town_base`, `itabuki`, `sangawara` | **wall_lattice_cell**, **wall_site**, **gate**, **open_gate_leaf** | no (4) | cell count |
| GV6 | Notice board (kōsatsuba) | — | — | PA3 (KEEP_OUTDOOR build-first) | — |
| GV7 (W2) | Ward gate (kido) + gatekeeper hut | `town_base`, `itabuki` | **gate**, **open_gate_leaf** | no (2) | hut = GV1 |
| GV8 | Fire watchtower, 2 heights | `frame_town`, `itabuki`, `upper_rail` | **frame_tower**, **ladder** | no (2) | 6-7.5 / 9.1 m; bell / drum |
| MI1 | Castle keep: one model + swaps + bare base | `frame_town`, `hongawara`, `irimoya`, `kura_walls`, `kura_open` | **frame_storey**, **stair**, **wall_sama**, **roof_ornament** | no (4) | grey tile / green copper; shachi gold / plain; white plaster / black boards; bare keep base (found_ishigaki) · *new pieces:* roof_hafu_decor, found_ishigaki · *note:* copper needs a new material |
| MI2 | Corner turret, 2 heights | `frame_town`, `hongawara`, `irimoya`, `kura_walls` | **frame_storey**, **stair**, **wall_sama** | no (3) | 2 / 3 storeys · *new pieces:* roof_hafu_decor |
| MI3 | Long wall turret (tamon) module | `frame_town`, `hongawara`, `kura_walls`, `kura_open`, `kura_footing` | **wall_sama** | no (1) | length |
| MI4 | Box-gate pair | `frame_town`, `hongawara`, `kura_walls` | **gate**, **open_gate_leaf**, **frame_storey**, **wall_sama** | no (4) | kōrai-mon + yagura-mon |
| MI5 | Castle plaster wall (dobei) module | `hongawara` | **wall_site**, **wall_sama** | no (2) | triangle / square ports |
| MI6 | Palace wing module | `town_base`, `hongawara`, `irimoya`, `veranda` | **roof_union**, **roof_corner** | no (2) | repeat count · *new pieces:* porch_genkan, roof_hafu_decor |
| MI7 | Castle ruin set | — | **found_ishigaki**, **wall_drystone** | no (2) | overgrown / tumbled |
| MI8 | Training hall (dōjō) | `town_base`, `sangawara`, `irimoya` | **frame_koyagumi** | no (1) | sword / spear / grappling fills |
| MI9 | Archery range | `town_base`, `itabuki`, `sangawara` | **frame_koyagumi** | no (1) | shajō + azuchi mound roof |
| CV1 | Plank bridge | — | **bridge** | no (1) | length |
| CV2 | Arched bridge | — | **bridge**, **porch_koran** | no (2) | span; giboshi |
| CV3 | Earth-covered bridge | — | **bridge** | no (1) | — |
| CV4 | Boat bridge | — | **bridge** | no (1) | boats = props |
| CV5 | Trestle bridge | — | **bridge**, **porch_koran** | no (2) | hero lengths (landmarks) |
| CV6 | Pulley well | — | — | PA3 (KEEP_OUTDOOR build-first) | — |
| CV7 | Lever well | — | — | PA3 (KEEP_OUTDOOR build-first) | — |
| CV8 | Sluice | — | **water_sluice** | no (1) | — |
| CV9 | Weir | — | **water_sluice** | no (1) | — |
| CV10 | Ferry landing | `rural_base`, `itabuki` | **found_kidan** | no (1) | waiting shed + ferry hut |
| CV11 | Quay steps (gangi) | — | **found_kidan** | no (1) | — |
| CV12 | Lighthouse lantern (tōmyōdō / jōyatō) | `frame_town`, `itabuki`, `koshi` | **found_kidan**, **ladder** | no (2) | stone / wooden |
| CV13 | Cremation hut | `rural_base`, `itabuki` | **floor_pit** | no (1) | — |
| WK1 | Wall kit: stone rampart (ishigaki) | — | **found_ishigaki** | no (1) | technique variants |
| WK2 | Wall kit: wooden palisade | — | **wall_palisade** | no (1) | — |
| WK3 (W2) | Wall kit: ornate earthen wall (tsuiji-bei) | `sangawara`, `hongawara` | **wall_site** | no (1) | 0-5 sujibei lines |
| WK4 (W2) | Wall kit: board fence (itabei) | — | **wall_site** | no (1) | — |
| ☆ SH-S1 | Noh stage | `town_base`, `itabuki` | **frame_stage**, **porch_koran** | no (2) | — |
| ☆ SH-S2 | Votive picture hall (ema-den) | `frame_town`, `itabuki`, `sangawara` | — | **yes** | open pavilion |
| ☆ SH-S3 | Red arched sacred bridge | — | **bridge**, **porch_koran** | no (2) | shu material needed |
| ☆ BU-S1 | Drum tower | `frame_town`, `hongawara` | **frame_storey**, **stair** | no (2) | hakama skirt |
| ☆ BU-S2 | Abbot's quarters (hōjō) | `town_base`, `hongawara`, `irimoya`, `veranda` | — | **yes** | shoin rooms |
| ☆ BU-S3 | Benten hall on a pond island | `town_base`, `itabuki`, `hongawara` | — | **yes** | bridge = CV2 |
| ☆ GV-S1 | Rice storehouse row | `kura_walls`, `kura_open`, `kura_eave`, `sangawara`, `kura_footing` | — | **yes** | boat inlets (found_kidan) |
| ☆ GV-S2 | Courier relay post | `town_base`, `itabuki` | — | **yes** | — |
| ☆ GV-S3 | Ward meeting house | `town_base`, `sangawara` | — | **yes** | — |
| ☆ MI-S1 | Horse-training track | `frame_town`, `itabuki` | — | **yes** | viewing stand (open pavilion) |
| ☆ MI-S2 | Coastal lookout + signal-fire post | `rural_base`, `itabuki` | — | **yes** | — |
| ☆ MI-S3 | Mounted-archery course (yabusame) | — | — | **yes** | posts and targets (props) |
| ☆ CV-S1 | Chinese-style academy hall | `town_base`, `hongawara`, `irimoya` | **open_katomado**, **found_kidan** | no (2) | — |
| ☆ CV-S2 | Charity clinic with herb garden | `town_base`, `itabuki` | — | **yes** | — |
| ☆ CV-S3 | Vine bridge for a gorge | — | **bridge** | no (1) | — |

### Landmark-only shells (KEEP_LANDMARKS)

| ID | Shell | Uses (bundles, see legend) | Lacks | Build now? | Variant axes |
|---|---|---|---|---|---|
| LM01 | Hero shrine tower gate (rōmon) | `frame_town`, `hongawara` | **frame_storey**, **frame_kumimono**, **roof_sori**, **porch_koran**, **open_gate_leaf** | no (5) |  · *note:* Kunōzan |
| LM02 | Cloister (kairō) module | `frame_town`, `hongawara`, `win_rural` | **frame_kumimono** | no (1) |  · *note:* hero shrine |
| LM03 | Five-storey pagoda | `frame_town`, `hongawara` | **frame_storey**, **frame_kumimono**, **roof_sori**, **roof_ornament**, **porch_koran** | no (5) |  · *note:* Tō-ji W06, Kōfuku-ji |
| LM04 | Kabuki theatre | `town_base`, `sangawara`, `itabuki` | **frame_koyagumi**, **frame_stage** | no (2) |  · *note:* moved from KEEP_TRADES 32 |
| LM05 | Great Buddha Hall (Hōkō-ji; also Tōdai-ji 1709) | `frame_town`, `hongawara` | **frame_storey**, **frame_kumimono**, **roof_sori**, **found_kidan**, **open_tobira**, **frame_koyagumi** | no (6) |  · *note:* ~49 m; unique |
| LM06 | Dōjima rice trading floor | `town_base`, `sangawara`, `kura_walls` | **frame_koyagumi** | no (1) |  · *note:* unique hall + kura |
| LM07 | Saruhashi cantilever bridge | — | **bridge** | no (1) |  · *note:* Kōshū road |
| LM08 | Kiso kakehashi cliff walkway | — | **bridge** | no (1) |  · *note:* W90 |
| LM09 | Kunōzan 1,159-step stair | — | **found_kidan** | no (1) |  · *note:* E63 |
| LM10 | Ise Grand Shrine halls (shinmei-zukuri, rebuilt 1729) | `thatch_gable`, `frame_town` | **roof_ornament**, **porch_koran**, **found_stilts**, **wall_site** | no (4) |  · *note:* unpainted hinoki; fences |

### Landmarks: which shells they use

Everything in KEEP_LANDMARKS except LM01–LM10 above is assembled from kept shells:

| Landmark | Built from | Parts it waits on |
|---|---|---|
| Hakone, Arai, Kiso-Fukushima, Usui checkpoints | GV4 kit + WK2 palisade + MI-S2 lookout (Arai adds the CV10 landing) | gate, gate_leaf, palisade, lattice_cell |
| Seta Karahashi, Nihonbashi, Sanjō, Ryōgoku, Yahagi, Uji, Tenma bridges | CV5 trestle / CV2 arched at hero length | bridge, koran |
| Edo and Osaka castles (bare keep base), Osaka's granite powder magazine | MI1 bare-base variant, WK1, MI3–MI5, DW22 stone variant | ishigaki, wall_site, sama |
| Nijō and Nagoya keeps (standing) | MI1 with the copper / gold-shachi swaps | storey, stair, sama, ornament + copper material |
| Kodenmachō jail | GV5 | lattice_cell, wall_site, gate, gate_leaf |
| Mt Hiei, Kōya, the hero temple complex | BU1–BU8 spread over terrain | as the temple shells |
| Kunōzan Tōshōgū | LM01 + LM02 + LM09 + SH2 / SH3 | storey, kumimono, sori, koran, kidan |
| Nara: Tōdai-ji hall (rebuilt 1709), Kōfuku-ji pagoda | LM05 (second instance), LM03 | as those |
| Nihonbashi fish market | TR-S02 market hall + the PA3 stalls | koyagumi |
| Mt Fuji pilgrim huts, Ōi River porters | DW02 huts (dry-stone variant), DW04, GV3 | koyagumi, drystone |
| Moto-Hakone stone Buddhas, Sekigahara, Ōjigoku, the volcanoes | terrain + outdoor (not shells) | — |

### New modular pieces that multiply variety

Stephen wants variety "rather than just recoloring, having windows or doors be different". These pieces are cheap and
each changes a silhouette or an opening on many shells. The counts are the shells already flagged in the table; their
reach is wider.

| Piece | Effort | What it changes | Shells it touches |
|---|---|---|---|
| `jp_p_roof_corner` (also on the wave-1 list) | S | Pents and verandas wrap a corner, so a building reads from two streets or a garden | DW06, DW10–DW13, DW15–DW19, TR01, TR05, TR06 and every engawa house |
| promoted lean-to (housekeeping step 0a) | S | A lean-to on any side, in any covering (sangawara only today) | DW30, DW02, DW06–DW10, DW16–DW18, DW24, TR01, TR03, the stable add-ons |
| `jp_p_open_mairado` | S | A new door face: fine horizontal battens on a board leaf, as twin / single / shutter | DW15, DW19, DW20, DW29, TR05, TR06, GV2, the temple kuri and hōjō, townhouse side doors |
| `jp_p_open_hood` | S | A small board / tile / stone-weighted hood over any window | every hut, farmhouse and townhouse gable (DW01, DW30, DW06, DW11, DW12 flagged) |
| `jp_p_open_shitaji` + `jp_p_open_katomado` | S + S | Lath windows, round windows, cusped windows | DW05, DW21, DW-S07, BU2, CV-S1, farmhouse back rooms |
| `jp_p_roof_forms_katayosemune` | S | A half-hip / hip-end silhouette | DW11, DW12 corner units, TR05 corner inns, farmhouse and tea-house variants |
| `jp_p_wall_takahe` | S | Yamato-mune tile-capped gables: the signature Kinai outline | DW07, DW17 |
| `jp_p_floor_sunoko` | S | A bamboo-slat floor axis for poor houses | DW01, DW30, DW03 (Kyoto roji) |
| 2 more koshi patterns (a board-bottomed ita-goshi; the heavy harimise) | S | Each townhouse trade set gets its own front | the 22 shop dressing sets on DW11–DW13, TR30 |
| `jp_p_state_damage` | M | Dead-world geometry: missing amado and shutter boards, holed thatch, fallen plaster showing lath, a sagging lean-to. It doubles every shell for free and fits KEEP_LANDMARKS "shutters half-open or broken" | all shells; flagged on 12 |
| `jp_p_gate` family (5 gate types) | M | The same compound reads as a different rank or district | DW14, DW15, DW19, DW20, TR06, BU5, GV2, GV4, GV5, GV7 |
| inuyarai / komayose (curved bamboo splash fence, horse-tie rails) | S | Kamigata street fronts | DW11, TR05. It is street dressing: coordinate with PA3 |

**Axes that cost nothing today** (use them first): roof covering × roof form × ridge type; door family (plain /
battened / oodo / twin / single / koshidaka / koshido); window family; koshi pattern; shop closure; foundation; wall
finish × koshiita height; pent type; wear level.

For example, the two poor-hut shells × (thatch hip / board / stone-weighted) × (arakabe / board) × 3 door types × 2
floors already give well over 20 visibly different huts.

### Legend: bundles of existing parts

| Bundle | Existing part IDs (all `jp_p_...`) |
|---|---|
| `frame_rural` | frame_post_adzed, frame_beam_log, frame_beam_sawn |
| `frame_town` | frame_post_planed, frame_beam_sawn |
| `dashigeta` | frame_dashigeta_std, frame_dashigeta_upper_front |
| `soseki` | found_soseki_set8, found_soseki_mossy |
| `dodai` | found_dodai_stones_rough, found_dodai_stones_dressed |
| `kura_footing` | found_kura_footing_c1, found_kura_footing_c2 |
| `yukashita` | found_yukashita_open, found_yukashita_boarded |
| `steps` | found_step_natural, found_step_cut, found_step_wood |
| `earth_walls` | wall_shinkabe_arakabe, wall_shinkabe_nakanuri, wall_koshiita_h060, wall_koshiita_h090 |
| `shikkui_walls` | wall_shinkabe_shikkui, wall_shinkabe_kokabe_ranma |
| `board_walls` | wall_board_vertical_battened, wall_board_vertical_plain, wall_shitami_house |
| `kura_walls` | wall_okabe_kura, wall_gable_kura, wall_shitami_kura, wall_namako_imo, wall_namako_shihan |
| `nuriya` | wall_okabe_nuriya |
| `udatsu` | wall_udatsu_sode, wall_udatsu_hon |
| `gable_thatch` | wall_gable_thatch |
| `gable_tile` | wall_gable_tile |
| `gable_board` | wall_gable_board |
| `thatch_hip` | roof_forms_yosemune, roof_thatch_body_yosemune, roof_thatch_body_new, roof_eave_soffit_thatch, roof_kemuridashi_hood, roof_thatch_ridge_bamboo, roof_thatch_ridge_tile, roof_thatch_ridge_shiba, roof_thatch_ridge_umanori |
| `thatch_gable` | roof_forms_kirizuma, roof_thatch_body_kirizuma, roof_eave_soffit_thatch, roof_hafu_thatch, roof_thatch_ridge_bamboo, roof_thatch_ridge_umanori |
| `thatch_irimoya` | roof_forms_irimoya, roof_thatch_body_irimoya, roof_kemuridashi_irimoya, roof_eave_soffit_thatch |
| `kabuto` | roof_forms_kabuto |
| `ishioki` | roof_ishioki_field_std, roof_ishioki_field_worn, roof_ishioki_battens_stoneset8, roof_ishioki_battens_sparse, roof_board_ridge_stoned, roof_hafu_board, roof_eave_soffit_board |
| `itabuki` | roof_itabuki_field_plain, roof_itabuki_field_bamboo, roof_itabuki_field_kakigara, roof_board_ridge_strips, roof_hafu_board, roof_eave_soffit_board |
| `sangawara` | roof_sangawara_field_std, roof_sangawara_field_pointed, roof_sangawara_eave_tomoe, roof_sangawara_eave_plain, roof_sangawara_eave_lod1_strip, roof_sangawara_verge_L, roof_sangawara_verge_R, roof_kawara_ridge_c3, roof_kawara_ridge_c5, roof_kawara_ridge_hip, roof_onigawara_plain, roof_onigawara_sui, roof_hafu_tile, roof_eave_soffit_tile |
| `hongawara` | roof_hongawara_field, roof_hongawara_eave, roof_hongawara_ridge, roof_onigawara_plain, roof_kawara_ridge_hip, roof_hafu_tile, roof_eave_soffit_tile |
| `kirizuma` | roof_forms_kirizuma |
| `yosemune` | roof_forms_yosemune |
| `irimoya` | roof_forms_irimoya |
| `koshiyane` | roof_kemuridashi_koshiyane |
| `pent_tile` | roof_hisashi_tile |
| `pent_board` | roof_hisashi_board |
| `pent_ishioki` | roof_hisashi_ishioki |
| `pent_skirt` | roof_hisashi_skirt |
| `pent_gable` | roof_hisashi_gable |
| `kura_eave` | roof_kura_eave_std |
| `gutter` | roof_gutter_std |
| `doors_rural` | open_itado_plain, open_itado_battened, open_itado_oodo, open_itado_single, open_shoji_ext_koshidaka, open_mushiro_rolled |
| `doors_town` | open_itado_twin, open_itado_single, open_itado_oodo, open_shoji_ext_twin, open_shoji_ext_single, open_shoji_ext_hikiwake, open_koshido_open, open_koshido_papered |
| `itado_pair` | open_itado_pair |
| `win_rural` | open_renji_bamboo, open_renji_wood, open_window_slide_board, open_tsukiage_board |
| `win_town` | open_window_slide_shoji, open_window_slide_board, open_amado_window_twin, open_tsukiage_board, open_renji_wood, open_renji_muso |
| `koshi` | open_koshi_kyo, open_koshi_oyako, open_koshi_komeya, open_koshi_degoshi, open_koshi_bengara |
| `mushiko` | open_mushiko_oval, open_mushiko_oval_pair |
| `shopfront` | open_suriagedo_closed, open_suriagedo_part, open_suriagedo_door, open_shitomido_up, open_shitomido_closed, open_battari_down, open_battari_up |
| `kura_open` | open_kura_door_open, open_kura_door_hinged, open_kura_window_slide, open_kura_window_hinged |
| `veranda` | porch_engawa_kure, porch_engawa_kiri, porch_nureen_std, open_amado_stowed, open_amado_closed, open_tobukuro_box, open_tobukuro_swing, open_shoji_ext_akari |
| `nureen` | porch_nureen_std |
| `upper_rail` | open_upper_rail_plain |
| `grime` | trim_grime_wall, trim_grime_post |
| `helper:floors` | tatami_room / board_floor / doma_floor / loft (machiya_t3_01.py) |
| `helper:leanto` | geya_roof + sloped_wall (machiya_t3_01.py; sangawara only) |
| `helper:udatsu` | udatsu placer on the street pent (machiya_t3_01.py) |
| `helper:ridge_walk` | ridge_walk strip (machiya_t3_01.py) |
| `town_base` | the bundles `frame_town`, `dodai`, `earth_walls`, `shikkui_walls`, `board_walls`, `doors_town`, `win_town`, `grime`, `helper:floors` |
| `rural_base` | the bundles `frame_rural`, `soseki`, `earth_walls`, `board_walls`, `doors_rural`, `win_rural`, `grime`, `helper:floors` |

## 5. Wave-1 readiness (Phase C wave 1)

| Shell | Now? | What it still lacks (base) | Optional, cheap |
|---|---|---|---|
| DW06 Kantō farmhouse | no | koyagumi | stall (inside-stable variant), corner (skirt pent wrap), hood, damage |
| DW07 Kinai farmhouse with ox | no | koyagumi, stall | takahe, floor pit (kabata tank), union (kamaya gutter) |
| DW01 Poor hut, east | no | koyagumi | sunoko, floor pit (irori hole), hood, damage |
| DW30 Poor hut, west | no | koyagumi; the lean-to helper must learn board / thatch | as DW01 |
| DW12 Edo townhouse units 2 / 3 / 4 ken + corner | no | party wall, party roof end, corner pent | katayosemune, hood |
| DW11 Kamigata townhouse units 2 / 3 / 4 ken + corner | no | party wall, party roof end, corner pent | katayosemune, hood |
| DW10 Tōkaidō post-town house | **yes** (detached) | — | stall (stable add-on), party parts for a row |
| TR05 Inn (hatago) | size 1 **yes** | the stair (size 2, the one grand inn per T3 town, G1-5) | corner, mairado |
| DW22 Kura | **yes** | — (interior waits on B1's `jp_m_wall_shikkui_int`) | stair or ladder for the loft (G1-5 elevation) |
| DW24 Shed / barn | no | koyagumi | damage |
| DW26 Toilet | no | half-door, after Stephen's D1 call (below) | — |
| DW28 Roofed well | **yes** | — (curb and pulley are PA3's) | — |

### What Phase B2 must make for wave 1, in order

**Step 0: kit housekeeping.** These aren't parts, but every wave-1 shell leans on them.
- **0a. Promote the machiya helpers into `jpparts`:**
  - `floors` (tatami, board, doma and loft floors, with hooks for stairwell and pit holes)
  - `leanto` (the geya roof for all six coverings, plus the sloped wall)
  - the udatsu placer and the ridge walk

  Today they are private functions in `machiya_t3_01.py`. The lean-to only knows sangawara. S.
- **0b. A multi-building build pipeline.** `build.py` writes `src/JP/buildings/config.cpp` with one class and
  overwrites `test/placements/C.csv` and the CE files. A second building would erase the machiya. It needs a
  registry that collects every building's class, doors and placements. S.
- **0c. Parametric shell templates.** At least the townhouse unit (frontage, region, end / middle / corner), the
  farmhouse and the hut. The machiya is 700 lines of hand placement, and "variants by script run" needs templates.
  This is Phase C's work, but B2 needs the townhouse unit as the test bed for parts 2–4.

**The parts:**
1. **`jp_p_frame_koyagumi`** (M). It unlocks 5 wave-1 shells: DW01, DW30, DW06, DW07, DW24. It is also the biggest
   unlock in the catalogue, so build it first. Include the jōya-core / geya-aisle split under one thatch slope, and a
   sooted wear level.
2. **`jp_p_wall_party`** (S). The unit partition cut to the roof section, sealed to the roof underside. For DW11 and
   DW12, and DW10's row version.
3. **`jp_p_roof_party_end`** (S). A flush roof end at the party line, no verge and no hafu, with step closures. For
   DW11 and DW12.
4. **`jp_p_roof_corner`** (S). A pent corner and an engawa / amado-track corner. For the corner units, the corner
   hatago and the farmhouse skirt-pent wrap.
5. **`jp_p_frame_stall`** (S). For DW07's ox (required), and the DW06 and DW10 stable variants.
6. **`jp_p_stair`** (M). For the grand hatago (size 2) and the kura loft Stephen wants for elevation (G1-5).
7. **`jp_p_open_halfdoor`** (S). Only if Stephen wants an enterable toilet (below). Otherwise drop it and make the
   toilet a sealed booth.

**Optional wave-1 variety**, in value order:
- `jp_p_floor_pit` with `jp_p_floor_sunoko` (S; they also give PA2 its irori holes)
- `jp_p_open_hood` (S)
- `jp_p_roof_forms_katayosemune` (S)
- `jp_p_open_mairado` (S)
- `jp_p_state_damage` (M)

**Size:** parts 1–7 are 2 M + 5 S, about 3–4 agent sessions after step 0. The ladder, gates, site walls, curved roofs
and everything else wait for wave 2 and later.

**Dependencies outside B2:**
- **B1:** `jp_m_wall_shikkui_int` for the kura and Edo nurigome interiors.
- **PA2:** the irori and kamado sized to the floor-pit holes; the ceilings for the town shells.
- **PA3:** the well curb and pulley for DW28.

## 6. Kit-level risks

1. **Snap-together townhouse units are the wave-1 risk.** Several PLAYBOOK §15 rules land on the seam between two
   separately placed p3ds:
   - **Party walls:** each unit must seal on its own (C11 / T5), because a neighbour may be missing. So each unit
     owns its end wall, set back half a wall from the lot line. Two coplanar walls flicker.
   - **Roofs:** they must stop flush at the party line without verge tiles (`jp_p_roof_party_end`). Different depths
     or heights leave a step that has to be closed. In Kamigata the udatsu covers the seam. **Edo units have no
     udatsu, so the seam shows** unless a board or plaster cap strip is added.
   - **Pents:** the street pents of neighbouring units must meet without a gap or an overlap.
   - **Terrain:** on sloping streets the dodai stone course must absorb grade steps between units.
   - **Corner unit:** needs a pent wrap (T8: nothing may poke through a roof, C12).
2. **Face budget.**
   - The machiya is at R1 11,926 of 12,000, a "large" building (PLAYBOOK §12, §15 T9).
   - A 2–3-ken unit is a "standard house" with a 6,000 budget, but it carries the same per-ken detail. A tiled hip or
     irimoya roof alone is about 4,000–4,400 faces at LOD0.
   - Townhouse streets will place dozens of units in view.
   - Decide the budget class for units before B2, or cut the modelled eave rows on units to one (REPORT decision 5).
3. **The roof generator is rectangles only, with planar slopes.**
   - Every L / T plan, genkan, valley, curved temple roof, tiered roof and decorative gable is new geometry.
   - Each needs its own T1 tile bed and fascia (C13), T7b silhouette in every LOD (C15), T8 no-poke (C12), and one
     convex collision slab per piece.
   - Temples, shrines, the castle and every compound depend on this. It is the biggest *effort* risk in the catalogue
     (the L-sized parts: sori, kumimono, storey, union, hafu_decor, ishigaki, bridge).
4. **Rotation doors are engine-untested.** The kura `_hinged` and the tsukiage (T4 rotation sign) wait on Stephen's
   check. Gate leaves, hall doors and half-doors all copy them.
   - **Put a hinged test door in the next bundled walk before building the gate family.**
   - Big gate leaves (1.5 ken each) also have to meet T2's 2 m reach from both sides (C10).
   - Open compound gates are not rooms, so decide whether C11 / C17 apply to them.
5. **Ladders have never been tested in this pipeline.** The engine ladder needs a `ladders[]` config and memory
   points. Towers and the lighthouse need them; the kura loft can use the stair instead.
6. **Stairs versus small plans.**
   - D4 (≥1.10 m wide, ≤38°, 2.05 m headroom) needs about 3.5 m of run to reach a 2.7 m floor. That takes a whole bay
     of a 2 × 3-ken kura or a small inn.
   - Upper floors also need the navmesh regenerated (T9).
7. **Tiny shells versus D1.** The door is ≥1.00 m clear, plus the 0.22 m STUB, plus a park bay. That can't fit:
   - a toilet booth
   - a field hut under 2 ken
   - a micro-shrine
   
   Decorative low doors (nijiri-guchi, zakuro-guchi) must follow D9 with a normal door beside them. **Stephen's call:
   is the toilet enterable** (then it is 1 × 1.5 ken with a single door) **or a sealed booth?**
8. **Thatch hips on small huts.** The kit's thatch has a 0.60 m cut and a 0.9–1.2 m overhang. On a 2–3-ken hut the
   roof mass dominates, and the eave soffit breaks the 2.20 m rule unless the G1-6 skirt pent is used on the door
   side. That makes the skirt pent part of every hut's entrance side.
   - A thinner cut (≈0.35 m) for huts is a one-parameter variant. Check it with Stephen at the wave-1 walk.
   - Thatch stays non-walkable. Its collision is a slab, so check that it doesn't snag players on low hut eaves.
9. **Tile-capped earth walls** (udatsu, takahe, dobei, tsuiji). `walls.kawara_cap` exists, but the caps must sit on a
   clay bed (T1) and keep a cap block in every LOD (T7b, "the udatsu cap courses" is already named there). The site
   walls also need footings on uneven terrain.
10. **Farmhouse span rule.** PLAYBOOK §2.2's "commoner main roof span ≤3 ken" comes from the 1668 Edo townsman rules
    [T48]. Applied to rural houses, it forces farmhouses into a 3-ken core plus lean-tos. Real Kantō farmhouses carry
    the aisle (geya) under the same thatch slope. Koyagumi must model that split. **Confirm the rule is urban-only**
    before wave-1 farmhouses are laid out.
11. **The T6 shikkui interior gap.** Kura, nurigome and every plastered room wait on `jp_m_wall_shikkui_int` (B1).
12. **Dashigeta versus Kiso.** G1-4 allows the dashigeta and the projecting upper front "tier 3 only". Kiso post towns
    (DW08, the Kiso post-town house) are tier 2 but need the dashibari overhang. This needs Stephen's ruling.
13. **The G1-5 upper-storey cap versus period two-storey trades.** Stephen allowed a full upper floor on "at most one
    grand inn per tier-3 town". Several period buildings had one too, and each needs a ruling or stays low:
    - the sentō upstairs rest room (TR08)
    - Yoshiwara / Shimabara houses (TR30)
    - the Sumiya ageya (TR31)
    - the Edo barracks rows (DW04 variant)

## 7. Decisions I made

- The buildable-now test counts the machiya's proven helpers as existing. Promoting them is step 0a, not a new part.
- Roof framing (koyagumi) is required only where the research says the room is open to the roof, or for work and
  farm buildings. Town shells assume ceilings (PA2).
- The stall kit, notice board and pulley / lever wells go to PA3: they are on KEEP_OUTDOOR's build-first list. The
  roofed well (DW28) stays a shell: a kit roof on posts over PA3's curb.
- The wall kit counts as four civic shells (WK1–WK4). The castle plaster wall is MI5.
- Landmarks add only 10 unique shells (LM01–LM10). The rest reuse kept shells (table in §4).
- Multi-size shells list what *all* their KEEP sizes need. The hatago's size 1 is buildable now; its size 2 waits for
  the stair.
- Shrines and temples at village grade use straight roofs. Curved roofs and brackets are upgrade variants, except
  where the shell can't exist without them (pagoda, sanmon, the landmark halls and gates).
- The corner townhouse unit needs a pent wrap. The hip-ended roof is optional variety, since a gable on the side street
  is also a period form.
- Period forms marked "assumed" or "verify" in the part details (katayosemune, hōgyō, mairado, the takahe reading of
  the Yoshimura house, the updraught tile kiln) need a dated source before they are built.
