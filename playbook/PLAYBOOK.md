# JP Playbook v1: the art and rules bible

> **Stephen's G0 decisions (2026-09-27):**
> 1. Era anchor 1730, window 1680-1750: YES.
> 2. One 1.82 m grid everywhere: YES.
> 3. Doors 2.0 m high, >=0.80 m inside and >=1.0 m at entrances, ceilings 2.5-2.7 m: YES.
> 4. Low upper floors: DEFAULT sealed (no access). A walkable crouch attic is only for SOME rich buildings or shrines,
>    and only if it holds loot; not a priority.
> 5. Stairs <=38 deg: CONFIRMED in game (2026-09-27). Stephen's AI test: an infected followed him in and upstairs
>    but slowly, so door clear width is >=1.00 m everywhere and stairs are >=1.10 m wide (D1, D4 updated).
> 6. Clothing is ONE set shared by players and infected (zombies wear the same outfits, attached, not flowy).
>    Period gear for every walk of life: worker, farmer, guard, samurai, leader, noble, peasant, traveller. The v1
>    kimono must be redone (chest seam, arms too baggy, legs clip when walking). Low priority at the start.
> 7. Shared material library jp_common.pbo with three wear levels, B's textures migrated: YES.
> 8. First playable slice: YES, but ALL development happens on the 2 x 2 km test island for now.

> **Stephen's G1 decisions on the exterior build list (2026-09-27):**
> 1. New palette entry `earth_wall_aged` (115,98,80) is the default tier 1-2 exterior wall: YES.
> 2. New palette entry `roof_board_silver` (123,128,134): YES.
> 3. Oyster-shell board roof (kakigara) as the Edo-side tier-3 variant: YES.
> 4. Cantilevered eave beams (dashigeta) and projecting upper fronts (post-1750): ALLOWED SPARINGLY as a flagged
>    deviation, tier 3 only. Build them as optional parts so Stephen can see them. His rule: if it clearly reads
>    as Japanese and is cheap once modelled, he likely wants it.
> 5. Full-height upper floors: the lead decides. A full second storey is allowed only on at most one grand inn
>    (honjin/large hatago grade) per tier-3 town, and only where neighbours (2-storey kura, tall machiya) make the
>    height read naturally. Elevation and chokepoints come mainly from period-true tall structures: kura lofts by
>    ladder or stair, fire watchtowers (hinomi-yagura), bell towers, castle yagura. Not from making ordinary houses
>    tall.
> 6. Thatch eaves: a board pent eave (porch roof) over entrance sides, as on the 1731 Sasaki house, instead of
>    raising the walls: YES.


**Status:** v1, waiting for Stephen's approval (gate G0). Written 2026-09-27. No models were built for it.

**Who must follow it:** every agent after this point: researchers (A), material and part builders (B), architects
(C), decorators (D), site-set builders (S), and later the temple and shrine builders (R). The same rules apply to
wearables (W) and arms where they touch colour, era and checks.

**How to read a rule:**
- `[T05]` is a text source and `[c07]` or `[m01]` is an image. All of them are in `refs_index.json`. The images are
  stored locally in `data/playbook/refs/` and are never shipped.
- `(reason)` marks a rule we set for gameplay or pipeline reasons, not from history.
- `(assumed)` marks a sensible value that no source gives. Replace it when a source turns up.

**If a rule doesn't fit your asset:**
- Stop and describe the problem under a "Playbook conflicts" heading in your report. Never work around a rule
  silently.
- Only Stephen changes this file.

Companion files:
- `WORLD_CATALOGUE.md`: what the world needs.
- `palette.json` and `palette_swatches.png`: the colours.
- `templates/`: the dossier, spec, build-list templates and schemas.
- `tools/`: the scripts that made the palette and the refs.

---

## 0. The twelve rules that stop the known mistakes

| # | Rule | Stops |
|---|---|---|
| 1 | **Kawara roofs are geometry.** At LOD0 the tile corrugation, the eave-tile ends, the verge tiles and the stacked ridge are all modelled (§6.1). A tiled texture on a flat plane is banned | machiya v1: the roof read as modern shingles |
| 2 | **Townhouse upper storeys are low** (zushi-nikai), 1.5–1.8 m inside at the street side [T43, T05]. A full-height upper storey on a town machiya is banned (§4, D3) | machiya v1: the full-height upper floor |
| 3 | **A base is individual stones under a timber sill.** Never use a continuous smooth plinth (§6.4) | machiya v1: the concrete-looking base |
| 4 | **Nothing is clean.** Every exterior gets the weathering set W1–W8 (§6.5) | machiya v1: the spotless surfaces |
| 5 | **Gable ends are built up, not flat.** Show the frame, the bargeboards and the verge tiles, and add udatsu where towns need them (§6.2) | machiya v1: the plain gable walls |
| 6 | **Players' legs are covered.** The obi is cloth, sleeves are flat panels, and the collar laps left over right (§6.6) | kimono v1: the mini-tunic, the leather-look obi, the balloon sleeves, no leggings |
| 7 | **Use library materials only, by path.** No private texture copies (§9) | the swappability rule |
| 8 | **Use palette colours only**, within tolerance (§8) | colour drift between agents |
| 9 | **Everything snaps to the half-ken grid** (0.910 m) and to the standard heights (§4) | parts that don't fit together |
| 10 | **The era anchor is 1730.** Nothing first attested after 1750 (§1) | anachronisms |
| 11 | **Status features belong to samurai and official buildings only**: nageshi, shoin, genkan, plastered gates (§2.2) | a rich merchant house that looks like a daimyo's |
| 12 | **Every asset passes the automated checks** (§12) and has a compare sheet before Stephen sees it (§13) | agents who "run off and make something wrong" |

---

## 1. Era

**Recommendation:**
- **Anchor year:** 1730 (Kyōhō 15).
- **Allowed window:** 1680–1750.

This narrows the brief's 1650–1750, for these reasons:

| Fact | Year | Consequence | Source |
|---|---|---|---|
| Sangawara (the one-piece S tile) invented | 1674 | Tiled townhouse roofs are only plausible from about 1680 | [T07] |
| Sangawara replaces board roofs in big cities | late 17th c. | Tier-3 towns can be tiled | [T40] |
| Tatami reach townspeople's homes | end of 17th c. | Tatami in tier 2–3 town houses | [T01] |
| Tatami reach ordinary rural homes | late Edo | No tatami in tier 1 | [T58] |
| Edo encourages tile roofs and plastered (dozō) walls | 1720 (Kyōhō 5) | Around 1730 Edo mixes new tile roofs with old board roofs, which gives free variety | [T05] |
| Obi widths recorded | 1730s | Garment specs can use these numbers | [T50] |
| One fire tower per ~10 chō, ladders on the ward offices | Kyōhō (1716–36) | Fire towers and ladders in towns | [T12] |
| Institutions in place | 1604–1711 | Ichirizuka (1604), sekisho (1619), honjin (1634–35), tenma quotas (1638), jōbikeshi (1658), Hakone stone paving (1680), the Shōtoku kōsatsu boards (1711) | [T22, T15, T19, T20, T12, T53, T23] |
| Daihachiguruma handcarts common | 1,273 counted in Edo in 1703 | Handcarts are allowed street props | [T54] |

**Not yet in 1730, so banned:**
- coloured nishikigoi (early 19th c. [T55])
- Edo's continuous dozō-zukuri streets (late Edo [T05])
- full two-storey machiya (after the rules eased [T05])
- the Nanbu magariya (18th c., far north [T26])
- glass panes, kerosene lamps and anything Meiji

**Caution:**
- The surviving streets we photograph are mostly late-Edo or Meiji rebuilds: Narai, Tsumago, Ōuchi, Kanazawa and
  Kurashiki [c01–c12].
- Hiroshige's prints are from the 1830s [c18].
- Use them for material, colour and proportion. Never use them to date a feature.

---

## 2. Tiers (wealth by map location) and the status overlay

### 2.1 The tier table

| Element | **T1 rural / poor** | **T2 village / post town** | **T3 town / main road / castle town** |
|---|---|---|---|
| **Floors** | Earth doma over ≥40 % of the plan. The living area is boards, or earth covered with straw and mushiro mats. **No tatami** [T17, T58] | Doma plus boards; tatami in 1–2 best rooms [T01] | Tatami in every living room; boards in the kitchen and corridors; an earth tōri-niwa passage in machiya [T04] |
| **Roofs** | Thatch (kaya or straw), or boards weighted with stones in mountain and coastal places. Never tile [T40, c05, c06] | Boards weighted with stones (Kiso), shingle or board; thatch in villages; tile only on a kura or a big inn | Kawara: sangawara on townhouses, hongawara on temples, castles, gates and samurai elite [T07, T10]. **Edo before 1720 is still mostly board.** In 1730 roughly half of commoner Edo roofs are tiled (assumed) |
| **Walls** | Earthen arakabe with straw showing, or plain sugi boards; no plaster | Board lower walls, earthen upper walls, plaster on upper storeys and kura; koshi lattice on street fronts | Shikkui plaster on upper storeys and kura, namako on kura lower walls, black boards on official buildings, **udatsu** between adjoining houses in Kamigata [T08] |
| **Doors** | Plank sliding doors (itado), hung mushiro mats, reed screens | Itado outside, shoji inside, some fusuma | Shoji and fusuma with **plain paper** (§2.2); itado and amado shutters in a tobukuro box; hinged plastered kura doors |
| **Windows** | Few: bamboo-barred renji-mado, board shutters, a smoke outlet in the gable | Koshi lattice; mushiko-mado on the upper storey (Kamigata) [T09] | Mushiko-mado, dense koshi (bengara in Kamigata), plain ranma transoms |
| **Interiors** | Irori, a clay kamado in the doma, shelves, straw goods, tubs, jars; almost bare | Irori or kamado, a tansu, an andon, zabuton, a kamidana; shop counters | Fully furnished: tansu, byōbu, andon, hibachi, a tokonoma in merchant best rooms, shop fittings |
| **Exteriors** | Threshing yard of packed earth, drying racks, straw stacks, a lever well (hanetsurube), hedges or bamboo fences, a field shrine | Noren, kanban, benches, fire buckets, a well, a kura at the rear, a small garden | Tsubo-niwa garden, stone lantern, roofed well, kura, board fences and plastered walls, gates |

### 2.2 Status overlay (class rules on top of wealth)

- **Commoner houses stay plain inside, however rich.** Edo's 1668 house rules barred townsmen from these [T48]:
  - nageshi (the rail above the lintels)
  - sugito (painted cedar doors)
  - tsuke-shoin (the built-in desk alcove)
  - carved decoration
  - karakami (patterned paper) and lacquer or gold

  Tier-3 merchant richness shows instead in size, tatami, good timber, kura, the garden and the shop.
- **Commoner main roof span ≤ 3 ken** [T48]. Extra depth comes from lean-to roofs (geya, hisashi).
- **Nagaya-mon gatehouses:** plaster walls are allowed for samurai residences; commoners (a village headman) use
  boards [T29].
- **Honjin only:** a formal front gate, a genkan with a shikidai step, and a jōdan-no-ma raised room [T19].
- **Official buildings:** black-stained boards, white gravel courts and heavy gates (jinya, bugyōsho, sekisho,
  bansho) [T28, T15, c16].
- **Colour:** shu vermilion only on shrines and some temple gates. Gold and lacquer only in elite interiors (§8).

---

## 3. Regional differences

| | **Kamigata (Kyoto / Osaka)** | **Edo (Kantō)** | **Rural / mountain (all regions)** |
|---|---|---|---|
| Ken and tatami | **Kyōma**, tatami-based planning: tatami 6.3 × 3.15 shaku = 1.91 × 0.955 m; ken 6.5 shaku [T03, T01] | **Inakama / edoma**, column-based: ken 6 shaku = 1.818 m centre to centre; tatami 1.76 × 0.88 m [T02, T01] | Local; usually column-based |
| Machiya | Earth tōri-niwa passage along one side, **zushi-nikai** with mushiko-mado, koshi lattice (often bengara), udatsu, inuyarai [T04, T05, T09, c07, c08] | Front doma, cantilevered eaves (**dashigeta**), a shop front that opens fully, plastered (nuriya) fronts after 1720 [T05] | Not applicable |
| Roofs in 1730 | Tile is common on town houses | Tile is new (post-1720), mixed with board | Thatch; boards weighted with stones in Kiso and on the coast |
| Signature details | Udatsu, inuyarai, battari-shōgi fold-down benches, bengara | Dashigeta, tensuioke fire buckets, kido ward gates, fire-tower ladders | Smoke gables, hasa drying racks, stone field shrines |

**Recommendation: one structural grid for every region.**
- **1 ken = 1.820 m, centre to centre (column-based). Half-ken = 0.910 m.**
- Tatami are laid to fill each room, on the floor texture or layout. The Kyoto/Edo mat-size difference only changes a
  floor texture, not the kit.
- Kamigata character comes from the facade and plan (tōri-niwa, zushi-nikai, mushiko, bengara koshi, udatsu,
  inuyarai), not from bays 8 % larger.
- **Why (reason):** one set of wall, door and roof parts, one grid check and one door and loot test. The Tokugawa
  ken was 1.818 m [T02].
- **The alternative is decision 1 for Stephen:** real kyōma bays (about 1.97 m) for Kamigata buildings. Every wall,
  door, lattice and roof module would then exist in two widths.

**Tatami layout** (reason, a period convention; verify when a source is found):
- In living rooms no four mat corners meet at one point (the shūgi layout).
- In an odd-sized room, a half mat (han-jō) fills the gap.
- There are no mats in the doma, kitchen or stable.

---

## 4. Dimension standards

All heights are measured from the local finished floor unless the table says otherwise.

| Item | Period value | **Game standard** | Source / reason |
|---|---|---|---|
| Structural grid | ken 1.818–1.97 m | **1.820 m centre to centre**; half-ken 0.910; trims only at 0.455 | [T02, T03], §3 |
| Posts | 3.5 sun (10.5 cm) and 4 sun (12 cm); the daikoku post larger (≥18 cm) | **0.120 m** standard, **0.150** farmhouse main posts, **0.210** daikoku. Always centred on a grid node | [T46, T47] |
| Tatami | 1.76–1.91 × 0.88–0.955 m, 5.5–6 cm thick | Mats fill the room between post faces; thickness **0.055**; heri edge **0.03** wide | [T01] |
| Doma level | ground level | **grade + 0.05** | B spike |
| Raised floor | ~50 cm above the doma | **+0.45** above the doma, reached by a hidden ramp (≤34°) under a stepping stone | [T17], B spike |
| Door head (uchinori) | 5.7–5.8 shaku = **1.73–1.76 m** | **2.00 m** (deviation D2) | [T39] |
| Clear door width | shoji leaf about 0.85–0.9 m | **≥1.00 m for every door a player or infected must pass**, interior and exterior (D1) | Stephen's AI test 2026-09-27: infected got through B's 0.80 m door slowly; the navmesh agent is 0.6 m wide |
| Ground-floor room ceiling | about 8 shaku (2.42 m) | **2.50–2.70 m**, because the door head rose 0.27 m (D6). A machiya doma stays open to the roof (fukinuke) | [T39] |
| Ground-floor street eave | about 3 m (machiya) | **2.90–3.20 m** to the eave edge; soffit **≥2.20 m** where people walk underneath | B spike (3.05) |
| **Low upper storey (zushi-nikai)** | **1.5–1.8 m** inside at the street side | Upper floor at **+2.85–3.10**. Street wall above the upper floor **≤1.30 m** (mushiko level). The ridge gives ≥2.10 m clear at the back. Walkable only where clear ≥2.10 (D3) | [T43, T45, T05] |
| Full upper storey | inns, honjin and samurai buildings where a source shows one | **2.40 m** clear, only if the build list cites a source | reason |
| Commoner main span | ≤3 ken | **≤3 ken (5.46 m)** between the main-roof walls; more depth via lean-to | [T48] |
| Roof pitch, kawara | 4–5.5 sun | **4.5 sun (24.2°)** default; range 4–5.5 sun (21.8–28.8°) | B spike; period photos [c08, c14] |
| Roof pitch, boards weighted with stones | about 3.5 sun (~20°) | **3–3.5 sun (16.7–19.3°)**. Steeper and the stones slide | [T40] |
| Roof pitch, shingle / board | not sourced | **4–5 sun** | (assumed) |
| Roof pitch, thatch | ≤45° usual; gasshō up to 60° | **45°** default; 50–60° only for gasshō-type | [T41] |
| Eave overhang | deep | tile **0.90 m**; thatch **0.90–1.20**; boards weighted with stones **0.90–1.20**; gable overhang **0.30–0.45** | B spike; (assumed) |
| Kawara module | modern J-type 53A has a working width of ≈0.265 m | working width **0.260 m (ken ÷ 7)**, exposure **0.235**, roll height **0.05–0.06** | (reason: seven columns per ken) |
| Stair | box stairs were very steep | walk ramp **≤38°**, width **≥1.10 m**, head room **≥2.05 m** along the flight (D4) | B spike: 37.8° walks fine for players (Stephen 2026-09-27); 0.90 m wide was slow for infected, so +0.2 m |
| Engawa and corridors | 0.9–1.2 m | **≥1.00 m** clear | reason |
| Tōri-niwa passage | 1 ken | **≥1.00 m** clear beside the kamado and jars | B spike |
| Alleys (roji) | about 0.9–1.8 m | **≥1.20 m** where walkable; narrower gaps are blocked in Geometry | reason |
| Back-alley tenement unit | "9 shaku × 2 ken" (2.7 × 3.6 m) | 1.5 × 2 ken | (assumed; the common name, verify) |
| Machiya plot | 5.4–6 m wide × about 20 m deep | **3–3.5 ken × 10–11 ken** | [T04] |
| Kido guard hut | 6 × 9 shaku, eave 10 shaku | **1.82 × 2.73 m**, eave **3.03** | [T11] |
| Fire tower | official 3 jō (≈9.1 m); town towers lower | **9.1 m** official, **6–7.5 m** town (assumed) | [T12] |
| Ichirizuka | 5 ken square, 1 jō high, one each side of the road | **9.1 × 9.1 m, 3.0 m high**, a tree on top | [T22] |
| Highway | Hakone paving 2 ken (3.6 m) | main road **3.6–5.5 m**, town street **3.6–7.3 m** | [T53] |
| Daihachiguruma handcart | bed 8 × 2.5 shaku, wheels 3.5 shaku | **2.42 × 0.76 m** bed, wheels **Ø1.06 m** | [T54] |
| Odoi (Kyoto) | 5 m high, 20 m base, 5 m top, moat 10–15 m | as stated | [T14] |

---

## 5. Gameplay-over-history deviations (each one needs Stephen's OK)

These numbers come from B's offline checks: head room ≥2.25 m, a 0.6 × 1.8 m column through each doorway, a 37.8°
ramp, and vanilla doors of about 1.2 × 2.2 m. **None of them has been tested in game yet.** The first building check
decides them.

| # | Deviation | Real | Game | Why |
|---|---|---|---|---|
| D1 | Door width | ~0.85–0.9 m per leaf | **≥1.00 m every passable door** | Infected pathing (0.6 m navmesh agent) and the player camera. Tested 2026-09-27: 0.80 m worked but was slow. Leaves park along the facade or in a pocket, not across a 1-ken passage |
| D2 | Door head height | 1.73–1.76 m | **2.00 m** | A standing player is about 1.8 m and needs clearance with a raised weapon |
| D3 | Low upper storey | 1.5–1.8 m, storage and servants | Low street wall kept; walkable only under the ridge (≥2.10 m); the front strip under 1.40 m is blocked in Geometry; 1.40–2.10 m is a crouch zone (**to test**) | Keeps rule 2's look without head traps. Option B is a sealed loft |
| D4 | Stair angle and width | box stairs ~50–60°, narrow | **≤38°** walk ramp, **≥1.10 m** wide | DayZ walkability: 37.8° confirmed fine for players 2026-09-27; width raised for infected |
| D5 | Corridors and alleys | 0.9–1.8 m | ≥1.00 m corridors, ≥1.20 m walkable alleys | Movement and infected pathing |
| D6 | Room ceilings | ~2.4 m | 2.5–2.7 m | Follows from D2; compensated by a low street eave and a low upper storey so facades don't look inflated |
| D7 | Bare-legged labourers (porters, kago bearers, in the period prints [c18]) | common | **NPC only.** Every player garment covers the legs | Stephen's kimono v1 feedback |
| D8 | Floor-length robes | common for townswomen and priests | **NPC only** (standing and walking) | W: they break at walk, sprint, crouch and prone |
| D9 | Tiny doorways: zakuro-guchi, nijiri-guchi, kido wickets | real | Decorative only; the room always has a normal door too | The player can't pass |
| D10 | Tatami | individual mats | A floor mesh with a mat texture layout per room | Faces, and loot on the floor |

---

## 6. Construction and style rules per element

### 6.1 Roofs

**Kawara, both families:**
- **Hongawara** (flat pans plus round covers):
  - Used on temples, castles, gates, samurai elite and rich kura.
  - Round eave tiles carry a mon or tomoe; flat eave tiles have a patterned lip [T10].
- **Sangawara** (one S tile):
  - Used on townhouses after 1674 [T06, T07].
  - Eave tiles have a small round end and a flat lip.
  - Verge tiles (sode-gawara) turn down at the gable.
- **Ridge:** 2–7 stacked courses of noshi tiles plus a round cap, with an onigawara at each end. The number of courses
  rises with status [c26, c09].
- **LOD0 geometry (rule 1):**
  - the corrugated profile across the whole slope, with **≥4 segments per tile column**
  - modelled eave-tile ends and verge tiles
  - a ridge of stacked courses with a round cap and end tiles
  - row steps from the normal map and baked AO; geometry steps only within 3 rows of the eave and ridge
- **Lower LODs:**
  - LOD1: 2 segments per column; eave ends as one strip.
  - LOD2: a flat plane with the baked texture.
- **Roof face budget:** ≤3k faces at LOD0 for a machiya-sized roof.

**Boards weighted with stones (ishioki):**
- Split boards in overlapping courses; horizontal battens every 0.45–0.60 m (assumed); river stones of 15–30 cm on
  the battens [T40, c01–c03].
- Pitch ≤3.5 sun. Deep eaves. The boards are silver-brown (timber_weathered).

**Shingle / board (itabuki, kokera):**
- Thin courses with visible course lines.
- Pitch 4–5 sun (assumed).
- Temples and shrines use the curved, thick-edged kokera form. Houses use flat courses.

**Thatch:**
- Thickness shows at the eave: a clean-cut edge **0.4–0.8 m thick** (assumed from [c05, c06]).
- Hip (yosemune) or irimoya with a smoke gable (kemuridashi).
- Ridge: bamboo-bound [c27], tiled on thatch [c26 family, Morse], or grass. Crossed ridge members (umanori) count up
  with status [T17].
- North slopes carry moss (moss_on_stone).

**All roofs:**
- Gutters are bamboo or wood only (assumed). No metal.
- No chimneys: smoke leaves by roof vents (koshi-yane) and gable openings.

### 6.2 Walls and gables

- **Shinkabe** (posts and beams visible, plaster between) is the default for houses. **Ōkabe** (posts hidden) is for
  kura, castles, fireproof fronts and udatsu.
- **Finish by tier:**
  - arakabe (rough, straw showing) in T1
  - nakanuri (smoother, ochre) in T2
  - shikkui white or fine cream finishes in T3 [c09, c11, c08]
- **Thickness:** earthen walls 0.06–0.09 m; kura walls 0.20–0.30 m (assumed).
- **Lower walls:**
  - board wainscot (koshi-ita) 0.6–0.9 m high on exterior earthen walls in T2–3
  - namako tiles on T3 kura [c11]
  - black boards on official buildings [c16]
- **Gables (rule 5).** Every gable end has:
  - the exposed frame dividing the wall into panels no larger than 1 ken × 1 storey
  - bargeboards (hafu-ita)
  - verge tiles or the thatch edge as geometry
  - a gable vent or a smoke opening on farmhouses
  - W2 rain streaks
  - where town houses adjoin (T2–3, Kamigata), an **udatsu**: a plastered wing wall or parapet with its own small tile
    roof [T08, T05]
- **No blank smooth plane larger than 2 × 2 m** without a frame line, lattice, board or opening. (reason)

### 6.3 Openings

- Openings sit on half-ken bays. A 1-ken bay takes 2 sliding leaves. A 2-ken bay takes 4 leaves on 2 tracks.
- **Main circulation routes** use openings of 1.5 ken or more, so that one open leaf gives ≥0.85 m (D1).
- **Exterior entrance:** one wide plank leaf slides along the outside face of the next bay, like an amado in its
  tobukuro. That gives ≥1.0 m clear.
- **Window types:**
  - mushiko-mado (plastered slats, upper storey) [T09]
  - koshi lattice (many variants by trade)
  - renji-mado (bamboo bars, rural)
  - plain ranma transoms
- **Doors** follow B's engine conventions: `type="translation"`, one bone per leaf, a memory axis of exactly 1.00 m,
  `doorWoodSlide` sounds.
- Kura doors are the only hinged doors: thick, plastered and stepped.

### 6.4 Plinths and foundations (rule 3)

- **Rural (T1–2):**
  - Posts stand on single rounded field stones (soseki). 5–20 cm of each stone shows.
  - Raised floors sit on short posts over small stones, with a dark ventilated gap under the floor.
- **Town (T2–3):**
  - A timber sill (dodai) on a low course of **individual** cut stones, with visible irregular joints.
  - An earth splash zone in front.
- **Kura and official buildings:** a cut-granite footing course of 0.3–0.6 m, in individual blocks.
- **Stone:** stone_granite or stone_lantern colours. Each visible stone is its own shape at LOD0.
- **Banned:**
  - continuous smooth grey plinths
  - cement-grey mortar
  - poured-looking steps
  - uniform block courses in rural work

### 6.5 Weathering set (rule 4): mandatory on every exterior

| ID | Effect | Where |
|---|---|---|
| W1 | Grime and splash band, 0–0.4 m, earth-tinted | Wall bottoms, posts, plinth stones |
| W2 | Rain streaks | Under sills, eave ends, window bottoms, gable corners |
| W3 | Sun bleaching (lighter, greyer timber) | South and west faces, upper boards |
| W4 | Dust on horizontal surfaces | Sills, beams, verandas |
| W5 | Soot | Around smoke vents, kamado walls, kitchen ceilings (timber_sooted) |
| W6 | Moss and lichen | North-facing roofs, stone, thatch, damp plinths (moss_on_stone) |
| W7 | Edge wear | Door edges, steps, thresholds, lattice corners |
| W8 | Variation, so no two identical adjacent planks or tiles | Each board or tile row gets a random offset or tint within tolerance |

**Implementation for v1:**
- Each library material has 3 shared wear levels: `_w0` clean, `_w1` normal, `_w2` heavy. All are canonical files,
  all referenced by path.
- Buildings pick levels per surface.
- A second-UV grime macro (the MC stage) is a later upgrade. It first needs proof that our p3d writer handles two UV
  sets.

### 6.6 Garments (rule 6; wearables W)

- **Legs:** every player lower body is covered by momohiki (fitted cotton leggings), kyahan (shin gaiters) with tabi,
  hakama, or tattsuke-bakama. Bare legs are for NPC labourers only (D7).
- **Length:** a commoner body garment reaches the knee when hitched up (shiri-hashori), or is a knee-length jacket
  (hanten, happi, haori) over trousers.
  - Nothing above mid-thigh.
  - Floor length is NPC only (D8, W report).
- **Obi:**
  - It is woven cloth: matte, visibly wrapped 2–3 turns, with a cloth knot at the back or side.
  - Men's obi were at their widest, about 16 cm, in the 1730s; women's about 25 cm [T50].
  - Banned: a buckle, gloss, stitched leather-look edges, or a stiff band narrower than 6 cm.
- **Sleeves:**
  - Flat rectangular panels hanging from the shoulder seam, with a small cuff opening and rounded lower outer
    corners [T51, m03].
  - No balloon volume. Sleeve thickness = the fabric plus the lining offset.
  - Labourers wear narrow tube sleeves.
- **Collar:** left over right. Always.
- **Colour:** commoners use indigo, the cha browns, the nezumi greys and kinari [T49] (§8).
- **Proof:** the M and F models, W's pose sheet, and a compare sheet against [m01, m03] and the period prints.

---

## 7. Banned modern tells

- **Roofs:**
  - kawara as a flat textured plane
  - metal roofing (copper only on major temples, later)
  - metal gutters
  - chimneys
  - dormers
  - Chinese-style exaggerated upturned corners on houses
- **Walls and bases:**
  - continuous smooth plinths
  - cement mortar
  - concrete or brick
  - painted white timber
  - pure-white untextured plaster
  - modern clean panel joints
- **Openings:**
  - glass panes
  - hinged house doors with knobs or butt hinges
  - Western balusters or balconies
- **Surfaces:**
  - spotless surfaces
  - identical repeated planks
  - visible texture tiling
  - perfectly straight new timber on old buildings
- **Streets:**
  - asphalt
  - kerbs
  - concrete retaining walls
  - square-cut uniform masonry in rural walls
  - wires, electric or glass lamps (use andon, chōchin, tōrō)
  - romanised or modern-font signs (period brush kanji and kana only)
- **Gardens:**
  - lawns
  - coloured koi [T55]
  - modern flower cultivars
- **Colour:**
  - anything outside `palette.json`
  - shu vermilion on houses, shops or castles
  - bright primaries or pastels
- **Garments:**
  - the mini-tunic over bare legs
  - a leather-look or buckled obi
  - balloon sleeves
  - zips, buttons or modern trousers
  - collar lapped right over left
- **Era:** anything in §1's banned list, and features copied from a later rebuild shown in a photo.

---

## 8. Palette rules (`palette.json`, `palette_swatches.png`)

- **Every material declares one palette ID.**
  - The mean colour of its `_co` texture over the material area must fall within `tolerance_dE76` of the entry.
  - Painted-on dirt and detail masks are excluded from that mean.
  - Grain, stains and variation inside the texture are expected; only the mean is fixed.
- **Weathering** may pull a surface toward the entry's `weathering.worst`, by no more than `max_mix`.
- **Restricted colours:**
  - shu_vermilion: shrines, and some temple gates or halls
  - bengara_wall: a few prestige tea-house fronts (T3)
  - bengara_lattice: Kamigata T2–3 lattices, sparingly
  - kuro_board and sumi_black: official buildings, kura, castle plaster
  - gold and lacquer: elite interiors only; they get palette entries when first needed
- **Textiles:**
  - Commoners (player default) use the aizome family, the cha browns, the nezumi greys and kinari.
  - Red, purple, gold thread and embroidery belong to elite or NPC specials. The 1683 and 1745 edicts pushed
    townspeople toward browns and greys [T49].
- **Adding a colour:**
  - It needs a sampled source (a museum photo or a photo of a surviving building) and goes through the build-list gate.
  - "Assumed" and "reference" entries are upgraded to "sampled" when a licensed sample appears.
- **Lighting (reason):**
  - The values are texture targets.
  - **Vanilla calibration:** vanilla "white" wall textures average only **144–155** (`stucco_white_clean_01`,
    `coalplant_plaster_white`, `housebt_plaster1`); old planks average 85–112 (measured, in `palette.json`).
    - So never author a "white" wall near 230: it will glow next to vanilla.
    - The palette's photo-sampled whites (shikkui 192, namako joint 136) sit in the right range.
  - At the first in-game building check, compare screenshots against the swatches.
  - If the engine's tone mapping shifts everything, apply **one global exposure factor** in the texture generator,
    never per-material tweaks. (F already lifted the petals for this.)
  - B's machiya v1 plaster preview was about 217, which is probably too bright. Recheck it against vanilla at the
    material stage.
- **How it was measured:**
  - The median of the photo pixels in a checked box, with the extreme luminance dropped. Tolerance comes from the
    observed spread.
  - Every crop is shown on the swatch sheet so neighbour contamination can be checked (the katana lesson).
- **Known limits of v1:**
  - thatch_weathered, tatami_aged and timber_interior are mixed-light samples, so they have wide tolerances.
  - 12 of the 39 entries aren't photo samples:
    - 7 are assumed: thatch_new, gofun_white, tatami_heri, washi_shoji, aizome_asagi, kinari_cloth, timber_sooted.
    - 5 are references: sumi_black, the three dictionary textile colours, and iron_black (the katana dossier value).

---

## 9. Material library

- **One canonical texture set per material:**
  - `jp_m_<family>_<name>{_w0|_w1|_w2}_{co,nohq,smdi}.paa` plus one `.rvmat` per wear level
  - under `JP\common\materials\<family>\`
  - packed into a new `jp_common.pbo` (CfgPatches `JP_Common`), which every area lists in `requiredAddons`
  - **This is a proposal for the lead** (README areas table).
- **Families:** `wood`, `wall`, `roof`, `stone`, `ground`, `floor`, `paper`, `textile`, `bamboo`, `straw`, `paint`,
  `metal`.
- **No private copies:**
  - A part, building, garment or prop references materials only by these paths.
  - B's current `JP\structures\data\jp_*` sets migrate into the library at stage B; the machiya is then rebuilt against
    the library paths.
- **Each material has a sidecar** `jp_m_<...>.json` holding:
  - its palette ID
  - its real-world tile size in metres
  - its grain direction
  - its penetration material and roadway surface
  - its sources
- **rvmat conventions** (proven in the B, W and F spikes):
  - **Buildings and props:** the Super shader, with Stages 1–7 as in B's `jp_plaster_white.rvmat`:
    - Stage1 `_nohq`
    - Stage2 constant DT
    - Stage3 constant MC
    - Stage4 constant AS
    - Stage5 `_smdi`
    - Stage6 fresnel
    - Stage7 `dz\data\data\env_land_co.paa`
    - `uvSource="tex"` everywhere, because there is no second UV set
  - **Wearables:** Super shader, with pristine, `_damage` and `_destruct` rvmats using vanilla damage macros (W).
  - **Flora:** copy the vanilla TreeAdv / TreeAdvTrunk parameter blocks exactly (F).
- **Fire Geometry uses only the vanilla penetration rvmats** (`dz\data\data\penetration\*.rvmat`):

  | Material | Penetration rvmat |
  |---|---|
  | Earthen or plaster wall | `dirt` |
  | Timber or boards | `wood` |
  | Tile | `pottery` |
  | Paper | `fabric_thin` |
  | Stone | `granite` |

  (B)
- **Roadway surfaces use vanilla files only:**

  | Floor | Roadway surface |
  |---|---|
  | Doma | `dirt_int` |
  | Tatami | `textile_carpet_int` |
  | Boards | `wood_planks_int` |
  | Stair | `wood_planks_stairs_int` |
  | Exterior stone | `stone_ext` |

  (B)
- **Normal maps:** DayZ's green-channel convention is still unconfirmed (B used DirectX). Every normal map goes
  through one converter, so flipping it is one switch. The first in-game check decides.
- **Resolution:**
  - Tileable materials are 1024² at about **512 px/m** for walls and floors, and **256 px/m** for roofs and ground.
  - 2048² only for hero items. (assumed; B's 1k maps made a 19 MB PBO, so an atlas comes later.)

---

## 10. Library, parts and proxy conventions

### 10.1 What exists where

| Kind | P: path | File prefix | How it reaches the game |
|---|---|---|---|
| Materials | `JP\common\materials\<family>\` | `jp_m_` | By path, from `jp_common.pbo` |
| Parts (posts, walls, openings, floors, stairs, roofs, plinths, trims) | `JP\parts\<group>\` | `jp_p_<group>_` | **Merged** into each building at build time (they must join its Geometry, Roadway and door selections). Parts are MLOD sources; they aren't packed |
| Buildings | `JP\structures\<type>\` | `jp_<type>_<nn>` | Class `Land_JP_<Type>_<NN>`, in `jp_structures.pbo` |
| Furniture | `JP\furniture\<roomtag>\` | `jp_f_` | As **proxies** inside building p3ds, like vanilla `\dz\structures\furniture\...`; in `jp_furniture.pbo` |
| Site and exterior objects (walls, fences, wells, lanterns, garden parts, street dressing) | `JP\site\<group>\` | `jp_s_` | As separate map objects (T's placements CSV or the spawner) |
| Temples and shrines (later) | `JP\religious\<set>\` | `jp_r_` | Buildings plus site objects |

- **Swappability:**
  - Materials are by path, so a new look needs **no rebuild**.
  - Parts are merged, so editing a part means rerunning the building build scripts. That is automated, with no
    hand rework (the B kit rebuilds in under 2 minutes).
  - Furniture is proxied, so a new tansu updates every house.
  - Only the §4 dimensions are expensive to change.

### 10.2 Part sidecar and connectors

- **Every part has a `jp_p_<...>.part.json` sidecar** holding:
  - its dimensions in ken and metres
  - its tier(s)
  - its material paths
  - its LOD face counts
  - its sources
  - its connectors
- **Part frame:**
  - Origin at the **left post centreline, finished floor level**.
  - +X runs along the wall.
  - +Y is up.
  - +Z is the exterior face.
  - `autocenter=0`.
- **Connector types** (they live in the sidecar, not in the p3d):

  | Connector | Where |
  |---|---|
  | `post` | Grid node |
  | `sill` | Floor level |
  | `head` | Door head 2.00 |
  | `eave` | Eave line |
  | `ridge` | Ridge line |
  | `floor` | Level ID |
  | `stair_foot` / `stair_head` | Ends of a flight |

- **Walls are recipes, not fixed meshes.** A wall type (its layers, materials, frame visibility and wainscot) is
  generated for any run of half-ken bays. So any wall fits any post spacing on the grid.
- **Fixed details** (lattice modules, mushiko, door leaves, ranma) come in 0.5, 1, 1.5 and 2-ken widths and snap
  between `post` connectors.
- **Roofs are generated from the footprint:** a rectangle, or an L or T union of rectangles, on the ken grid, plus
  the family, pitch and overhangs. So any roof fits any footprint.
  - Fixed roof parts (onigawara, eave tiles, ridge caps) are placed by the generator at `ridge` and `eave` connectors.
  - Tile columns are 0.260 m, so a column edge lands on every ken line.

### 10.3 Room tags (the architect sets one per room; the decorator furnishes by tag and tier)

| Tag | Floor | Tiers | Notes |
|---|---|---|---|
| `doma` | earth | 1–3 | Entry, work area and kitchen hearth (kamado) |
| `daidokoro` | boards | 1–3 | Kitchen and living with an irori |
| `living` | boards or tatami | 1–3 | Hiroma, ima |
| `zashiki` | tatami | 2–3 | Best or guest room; tokonoma in T3 |
| `sleeping` | tatami or boards | 1–3 | Nando |
| `shop` | tatami or boards, facing the street | 2–3 | Mise-no-ma; takes a `shop:<trade>` subtag |
| `office` | tatami | 2–3 | Chōba counting desk and screen |
| `workshop` | earth or boards | 1–3 | Takes a `workshop:<trade>` subtag |
| `storage` | boards | 1–3 | Kura interior, monooki |
| `loft` | boards | 2–3 | Zushi-nikai, low (D3) |
| `stable` | earth and straw | 1–2 | Umaya, inside or detached |
| `bath` | boards and stone | 2–3 | Inns, bathhouses, wealthy houses |
| `toilet` | boards | 1–3 | Setchin; detached or at the rear |
| `engawa` | boards | 2–3 | Veranda |
| `corridor` | boards | 2–3 | |
| `guard` | earth or boards | 2–3 | Bansho, kido hut |
| `court` | white gravel | 3 | Official courts |
| `yard` | earth | 1–3 | Exterior |
| `garden` | mixed | 2–3 | Exterior (site stage) |

### 10.4 Proxies and loot

- **Furniture:**
  - The origin is at the object's base centre, and the base sits on its supporting floor.
  - Its Geometry is closed and convex.
  - It has its own LODs.
- **Which LODs carry the proxy:** first read a vanilla house's proxy table per LOD (W's ODOL probes can find the
  proxy name strings). Then put ours in the same LODs. **This is open question Q5: the first decorator agent answers
  it before building anything.**
- **Loot:** loot points are generated from Roadway floor faces minus the furniture footprints (plus a 0.4 m
  clearance). Shelves and tokonoma get their own container points (B's next step).
- **Furnished variants** are separate p3ds: the same shell parts plus a proxy set, e.g.
  `jp_machiya_01_t3_shop_cloth.p3d`. The shell is shared, so the variants cost no rework.

---

## 11. Research depth by importance

| Level | What | Required before building |
|---|---|---|
| **Hero** | Held or worn signature items (weapons, armour, the main garments) and landmarks (castle keep, honjin, sekisho, the main machiya archetype, torii, temple main hall) | A full dossier on the katana model (`templates/DOSSIER_TEMPLATE.md`): ≥3 dated references including ≥1 museum or surviving-building photo; `spec.json` with a source per dimension; generated drawing; build from the spec; compare sheet with metrics |
| **Standard** | Every building type, every garment, major props (well, tōrō, torii, cart, kamado, tansu), every material | A short dossier: ≥2 references, one of them period (print, museum object or surviving building); `spec.json` for the key dimensions (`assumed` allowed with a reason); compare sheet |
| **Filler** | Buckets, crates, stones, straw bundles, crockery | One reference check, plus a spec entry with the dimensions and palette IDs; appears in the part contact sheet |

---

## 12. Required automated checks (per asset, scripted, logged as `checks.json` next to the asset)

| Check | Rule | Applies to | Exists? |
|---|---|---|---|
| **C1 Palette** | Mean `_co` colour per material region within `tolerance_dE76` of its palette ID | Every textured asset | New: stage B writes `check_palette.py`, reusing `sample_palette.py`'s Lab code |
| **C2 Library only** | Every texture or rvmat path in every LOD resolves under `JP\common\materials\` or the allowed vanilla list (penetration rvmats, roadway surfaces, `env_land_co.paa`, W's damage macros) | Every p3d | New (read the MLOD strings) |
| **C3 Grid snap** | Post centres, wall ends and opening edges on the 0.910 m grid within ±5 mm; floors at standard levels within ±5 mm | Parts and buildings | New; extends B's `verify_b.py` |
| **C4 Dimensions against spec** | Each spec dimension measured on the mesh: ±5 mm for grid items, ±2 % otherwise; ODOL read-back for heroes (katana method) | Everything with a spec | Katana `compare.py` pattern |
| **C5 LODs and budgets** | LOD set matches the class's vanilla set (buildings: Res 1–3, Geometry, Memory, Roadway, View Geometry, Fire Geometry; worn clothing: Res + Geometry; ground items: + Memory, View, Fire). Face budgets below | All | Partly (`verify_b.py`, W `verify_odol.py`) |
| **C6 Placement** | Proxies and site objects: base within 0–2 cm of the supporting Roadway or terrain; no interpenetration with other Geometry beyond 1 cm; loot clearance kept | Decorated buildings, site sets | New |
| **C7 Walkability** (buildings) | B's checks: convex closed components, door sweep clear, 0.6 × 1.8 m column through each doorway, Roadway coverage, head room ≥2.10, stair ramp ≤38° | Buildings | Yes (`verify_b.py`) |
| **C8 Era and tells** | Banned-list lint: no glass or metal material names; roof LOD0 corrugation present (vertex density on kawara faces ≥ threshold); plinth made of separate stones; garment leg coverage; obi width | By class | New, small |
| **C9 Compare sheet** | Renders from the reference viewpoints beside the references; for heroes, a silhouette overlay against the drawing (IoU) | Hero, standard | Katana pattern |

**Face budgets (v1).** The ratios are derived from vanilla `house_1w01` at 2019 / 777 / 262, so LOD1 is about 38 % and
LOD2 about 13 % of LOD0:

| Class | LOD0 | LOD1 | LOD2 |
|---|---|---|---|
| Small building (≤1 storey, ≤20 m²) | ≤3,000 | ≤1,150 | ≤400 |
| Standard house | ≤6,000 | ≤2,300 | ≤800 |
| Large / landmark building | ≤12,000 | ≤4,600 | ≤1,600 |
| Furniture | ≤1,000 | | |
| Small prop | ≤300 | | |
| Body garment (≥3 LODs; W's kimono 8.6k ≈ vanilla woolcoat) | ≤9,000 | | |
| Head or feet item | ≤3,500 | | |
| Hero tree (F's sakura LOD1 at 7.1k is "heavy") | ≤8,000 | | |
| Filler tree | ≤3,000 | | |

**Open task for the first B agent:** read the face counts of about 10 more vanilla buildings with W's ODOL tools and
tighten these budgets.

---

## 13. Review gates for Stephen (each one ≤10 minutes of his time)

| Gate | What he gets | He answers |
|---|---|---|
| **G0** | This playbook, the palette sheet and the catalogue | Approve, or change the decisions list |
| **G1** | Each build list (one category): a table plus one reference strip per entry | Scope and look OK? |
| **G2** | Each part and material contact sheet: renders of every part beside its reference, with the C1–C9 results | OK, or name the parts to redo |
| **G3** | The first building of each type: a render sheet, then **one bundled in-game walk** (doors, stairs, loft, loot, LODs, colours in engine light) | Pass or fail per item |
| **G4** | The first furnished interior per room tag and tier | OK |
| **G5** | The first site set (a street, a yard, a garden) | OK |

**Rules for gates:**
- No agent starts the next stage of a category before its gate passes.
- In-game checks are batched into `TEST_CHECKLIST.md`, as in wave 1.

---

## 14. Open questions only the engine can answer (put them in the next in-game checklist)

- **Q1:** Is a 0.80 m door comfortable? Or is 0.90 the minimum? (D1)
- **Q2:** The crouch height, and the lowest clearance a crouching player passes under. This sets the D3 crouch band.
- **Q3:** Is a 38° ramp walkable up and down? Is 40° too steep? (D4)
- **Q4:** Which normal-map green channel does DayZ use? (§9)
- **Q5:** Which LODs do vanilla houses put their furniture proxies in? (§10.4; readable offline)
- **Q6:** Does the engine's tone mapping keep the palette's look? (§8)

---

## 15. Lessons from the first in-game house (G3, 2026-09-27)

Stephen walked `Land_JP_Machiya_T3_01`, the first house built from the parts library.

**His verdict:** the house looks good and nothing glows. The entrance, walking, every door opening, floor loot and roof
climbing all work.

**What he found** is below. The fix pass (agent C-FIX) turned every finding into a rule here and, where possible, into
an automated check.
- The checks run for every part (`parts/kit/jpparts/checks.py`) and every building
  (`parts/kit/jpparts/buildcheck.py`).
- Every building's `verify.py` calls `buildcheck.run_g3(M, L, floors, rec)`.
- Details and numbers: `buildings/machiya_t3_01/REPORT_FIX.txt`.

**Binding for every agent after this point.**

### 15.1 The rules

**T1 Tiles sit on a clay bed; the eave is closed.**
- **Stephen:** "Roof tiles are not on the roof; there's a gap when I get close."
- **The cause:** the kawara layer floated 8 cm above the sheathing boards. Nothing filled the gap, and nothing closed it
  at the eaves.
- **The rule:**
  - Kawara are laid in a bed of straw-tempered clay (fuki-tsuchi) on the sheathing, as the period did. The bed fills
    everything from the board top to the tile underside.
  - Every tiled eave has a fascia board (kayaoi / hana-kakushi) square to the rafters. Its top meets the underside of
    the eave tiles, and their lips hang in front of it.
  - No daylight shows anywhere between the rafters, boards, bed and tiles.
- **Implementation:**
  - `roofs.tile_bed()` and `roofs.kawara_fascia()`.
  - They are called by `roofs.cover_kawara` (so every roof from `roofs.roof`), by `roofparts.pent`,
    `openings.mini_pent` and the kura eave, and by the field sample parts.
  - **A hand-built tiled slope must call both.** The machiya's lean-to does.
- **Check:** C13.

**T2 Every door can be closed from both sides.** This is an engine rule, read from the vanilla scripts:
- **How DayZ finds a door:**
  - It uses only the component the camera ray hits: 5 m, in View Geometry. See `ActionTargets` (`ObjIntersectView`),
    `ActionOpenDoors` / `ActionCloseDoors` and `Building.GetDoorIndex(componentIndex)`.
  - `CCTCursor` and `IsInReach` also need the hit point, and the leaf's memory point `doorsN`, within 2 m of the head
    or feet.
  - Nothing falls back to "nearest door".
- **What went wrong:** a leaf that parks completely behind the wall cannot be closed from the other side (Stephen:
  "doors can only be closed from one direction").
- **What vanilla does:** its sliding leaves never clear the doorway. Barn_Brick2 leaves 0.22 m, the rail warehouse
  0.30 m, the boxcar 0.4–0.5 m.
- **The rule:**
  - A fully open sliding leaf keeps `STUB` = **0.22 m** of its broad face inside the opening (`core.STUB`).
  - The memory point `<bone>` sits on the leaf's trailing edge at hand height, so it stays in the doorway.
  - D1 is measured with the stub in place: clear = opening − stub.
  - Every leaf has a View Geometry component, even open-bar lattices.
- **Check:** C10. For every door and window, open and closed, from both sides, with the other doors open:
  - the camera ray must hit the leaf's **broad face first**
  - from the far side, the hit must be **inside the doorway**
  - it must work from at least 4 of 15 standing positions (0.7–1.4 m out, ±0.6 m along)
  - the hit and the leaf point must be within 2 m

  The parts check adds "the open leaf keeps ≥0.15 m in the opening". C10 reproduces Stephen's defect: the pre-G3 doors
  score 0/15 from the far side and 14/15 from the park side.

**T3 Door styles by use (period).** Stephen likes the variety.

| Style | Leaves | Where | Part | Clear (measured) | Needs |
|---|---|---|---|---|---|
| **hikichigai** | 2, stacking to one side on 2 tracks | **Main entrances only**: street / shop entrance, inn entrance | `jp_p_open_itado_twin`, `jp_p_open_shoji_ext_twin` | 1.46 m | a plain half-ken beside it, on the leaf face |
| **hikiwake** | 2, parting in the middle in opposite directions | **Interior fusuma / shoji pairs** between rooms | `jp_p_open_shoji_ext_hikiwake` | 1.24 m | a plain half-ken on **both** sides |
| **katabiki (single)** | 1, beside a fixed half-panel | **Side, back and kitchen doors**, room entrances off a doma, storage | `jp_p_open_itado_single`, `jp_p_open_shoji_ext_single` | 1.06 m | a plain half-ken on the park side |
| single big leaf | 1 × 1.74 m | Poor houses, barns, big shop doors (ōdo) | `jp_p_open_itado_plain / _battened / _oodo` | 1.46 m | a plain 1-ken on the park side |

- Every door and window uses the **DoorsTwinN** config convention, single leaves too:
  - one config class per door
  - one selection `doorstwinN` over all its leaves
  - bones `doorsN`
  - one animation source
- The machiya uses:
  - the entrance: hikichigai
  - mise ↔ zashiki: hikiwake
  - both room entrances off the toriniwa, the back door and kitchen → storage: single

**T4 Openable windows** (Stephen: "as long as there's a few somewhere, in correct spots"):
- **How they work:**
  - They animate exactly like doors: DoorsTwinN, doorWoodSlide sound, the same C7/C10 checks.
  - They are not passable.
  - Sliding panels keep the STUB too.

| Type | Part | Where it belongs | Worked from |
|---|---|---|---|
| Sliding shoji behind a fine koshi lattice | `jp_p_open_window_slide_shoji` (half-ken) | T2–3 town street windows and room windows on streets or alleys | inside only (the lattice covers it from outside, as in a real house) |
| Sliding board shutter behind renji bars | `jp_p_open_window_slide_board` (half-ken) | Kitchens, stables, workshops, T1 houses | inside only |
| Two amado storm shutters stowing in a tobukuro box | `jp_p_open_amado_window_twin` (1 ken) | Zashiki, inn rooms, better T2–3 rooms on garden or side walls. **Not** shop fronts | both sides |
| Top-hinged push-up shutter (tsukiage / hanemage) over bars | `jp_p_open_tsukiage_board` (half-ken) | Storage, farmhouses, shop side walls. High sill (≥1.1 m above the floor), under an eave. Its bars are Geometry-only so the camera ray reaches the shutter from inside | both sides |

- **Stay static:**
  - mushiko (loft)
  - koshi and degoshi shop fronts
  - the kura window variants
  - shitomido
- **On the machiya:**
  - street window B2b: sliding shoji
  - zashiki gable: amado
  - kitchen back wall: board shutter
  - storage gable: tsukiage
- **Rotation sign (hinged leaves and shutters):**
  - model.cfg `type="rotation"`, `angle1 > 0` turns by the **right-hand rule about axis point 1 → 2**, in memory
    vertex order.
  - Source: 10 of 10 vanilla vehicle doors, hoods and trunks.
  - Kit: `core.ROT_SIGN`, `core.anim_point_fn`.
  - Untested on our buildings until Stephen's re-check. If a shutter swings the wrong way, swap the two axis points in
    the part and change nothing else.

**T5 The envelope is sealed except through its openings.**
- **Stephen:** "From inside I can see outside." In the tatami room, the degoshi bays left a slit between the lattice
  box's head and the wall above, at standing eye height. The toriniwa gable had a second slit, where the outside board
  wall met the plaster above.
- **The rule:**
  - A room sees outside only through its declared doors, windows and lattices.
  - Where two wall kinds meet, or a lattice, bay or pent meets a wall, one member spans the **full wall thickness**.
    Examples: the board wall's top rail; the degoshi head board running up to the wall's head rail (2.00 m) and back
    to the inner face.
- **Note for any model that builds something similar** (Stephen asked for it):
  - This covers projecting lattice bays (degoshi, dashi-mado), bay windows, shop fronts and pents.
  - Close the **head** to the wall above with a head board or lintel that meets the wall's head rail. Never stop it
    short underneath.
  - Then prove it with C11. Don't judge it by eye in a render.
- **Check C11:**
  - Rays go out from a grid of eye points (0.5 / 1.1 / 1.65 m) in every room, against the Resolution 1 faces, with
    doors and windows closed.
  - A ray that escapes without passing through a door or window portal is a leak.
  - Paper counts as opaque.

**T6 Interior faces never use exterior weathering.**
- **Stephen:** interior walls looked dark and greenish. The weathered exterior clay (#7 `jp_m_wall_nakanuri`) turns
  green in DayZ's cool interior light.
- **The rule:**
  - Every earth-wall face that looks into a room uses `jp_m_wall_nakanuri_int`: warmer, unweathered, about the same
    lightness. It is palette `earth_wall_aged` +a*/+b*, matcheck dE 6.6/14.
  - Interior clay fixtures such as the kamado use it too.
  - Stephen: "it's supposed to be a dark game". He judges the colour in game.
- **Kit:** `walls.wall_run(interior='back'|'both')` and `walls.interior_mats()`. Building helpers default exterior
  walls to `'back'` and partitions to `'both'`.
- **Gap:** shikkui has no interior twin yet. Add `jp_m_wall_shikkui_int` the first time a plastered wall faces a room.
- **Check:** C14.

**T7 LOD material matching and a stable silhouette.**
- **(a) Matte far roof.** Far away, the roof looked "too shiny and flat", then darkened when the close LOD took over.
  - Kawara fields in Resolution 2 and 3 use `jp_m_roof_kawara_far`:
    - matte specular: 0.22 / 35 against 0.6 / 90
    - the LOD0 corrugation (pan shadow, roll highlight) and the course shadows baked into colour and normal map
    - its mean about 4 L* darker
  - The Resolution 3 field is one quad per slope.
  - **Check:** C16.
- **(b) Stable silhouette.** The onigawara and ridge-end tops popped in and out.
  - Everything that forms the outline keeps a simplified version in **every** LOD:
    - the ridge stack (one block per LOD for the courses)
    - the ridge ends
    - the onigawara (two prisms and its back block)
    - the verge strip, the eave strip and the fascia
    - the udatsu cap courses
  - A cap may never float over a course that a lower LOD dropped.
  - **Check C15:** top-down height maps of Resolution 2 and 3 stay within 0.10 m of Resolution 1.

**T8 No part pokes into a roof.**
- **Stephen:** "Something on the side of the house clips into the roof and pokes through, and pops with distance."
  He also saw it on the parts sheets.
- **The culprit:** the tile gable's board band and rail (`walls.gable _tile`). They were full rectangles, so they rose
  36 cm through the roof at both eave corners. They were in LOD 1–2 only, so they popped.
- **The rule:** gable and wall details are clipped 2 cm under the roof lines.
- **Check C12:** no solid of another sub-part may enter a roof body (from rafter underside to tile top) by more than
  3 cm, in any LOD. Sub-parts are tracked by `Solid.src`, which `Part.merge` stamps.

**T9 Earlier lessons from today, confirmed in game:**
- **D1 and D4:**
  - Doors are ≥1.00 m clear. 0.80 m worked, but infected were slow.
  - Stairs are ≥1.10 m wide and ≤38° (37.8° walks fine), with ≥2.05 m head room.
  - Both are measured with leaf stubs and fixed panels in place.
- **Infected follow a player inside and upstairs** once the navmesh includes the building. Regenerate the navmesh
  (`NAVMESH_STEPS.md`) after placing or changing a building, before any AI test.
- **Tile and board roofs are walkable** (Roadway on the slopes plus a ridge strip), for rooftop running. Roof climbing
  was confirmed on the machiya. Thatch stays non-walkable.
- **Palette calibration holds in engine light:** nothing glowed.
- **Budget:** the machiya sits at R1 11,926 / 12,000 and R3 1,570 / 1,600. New detail has to be paid for elsewhere.
  - Fixed panels and kumiko use 4-face open bars (`openings.open_bar`).
  - Flashing strips have no cap.

### 15.2 The checks added (they extend §12)

| Check | Rule | Runs in |
|---|---|---|
| **C10 Door reach** | T2: the camera ray hits the leaf's broad face first from both sides, open and closed, within 2 m; ≥4/15 positions; far side inside the doorway; the open leaf keeps ≥0.15 m in the opening | parts (`checks.py`) + buildings (`buildcheck.py`) |
| **C11 Envelope leak** | T5: rooms see outside only through doors, windows and lattices | buildings |
| **C12 Roof / wall intersection** | T8: nothing from another sub-part inside a roof body by more than 3 cm, in any LOD | buildings |
| **C13 Tile seating** | T1: kawara within reach of the clay bed; a fascia at every eave with eave tiles | parts + buildings |
| **C14 Interior material** | T6: no exterior-weathered earth face looks into a room | buildings |
| **C15 Stable silhouette** | T7b: Resolution 2 / 3 top heights within 0.10 m of Resolution 1 | buildings |
| **C16 Far-LOD kawara** | T7a: the matte far material in Resolution 2 / 3 only, specular below the close material | buildings |
| **C17 Closed-leaf jamb seal** | T11: with every leaf closed, no ray gets through the doorway: steep rays (to ~80° off the wall normal) at every jamb and meeting stile, and straight-on rays over the whole leaf band (board gaps) | buildings (`raycheck.jamb_slits`) |
| **C18 Pull on the stub edge** | T10: every pull (solid tag `pull`) is still inside the doorway when its leaf is open | parts + buildings (`raycheck.pull_positions`) |
| **C19 Matte finish** | T12: every non-glossy library rvmat in the visual LODs has the black env map | buildings |

### 15.3 Second walk (G3 fix 2, 2026-09-29)

Stephen walked the fixed house: roof, door styles, windows, lattice gaps and far LOD pass. Three things failed; the
rules below are binding. Details and numbers: `buildings/machiya_t3_01/REPORT_FIX2.txt`.

**T10 The pull goes on the edge that stays in the doorway.**
- **Stephen:** "Every door with a handle is backwards", both outside doors included.
- **The cause:** `openings.leaf_plank` put the iron pull at the leaf's `l1` edge whatever way the leaf slid. Every
  plank leaf slides +x in its part, so the pull sat on the LEADING edge, which parks behind the wall. Nothing was
  mirrored; the building's yaw and mirroring were innocent.
- **The rule:** the pull (hikite) sits on the **trailing edge**, the one that closes against the jamb and keeps the
  `STUB` in the doorway when the leaf is open, so the open leaf can be pulled shut. Centre 0.10 m in from that edge.
- **Kit:** `openings.pull_x(l0, l1, dirn)`. `core.sliding_leaf` and `openings._leaf_set` pass `dirn` to every leaf
  builder (`build(..., bone, dirn=+1)`); a new builder must take it and use `pull_x`. Tag the pull `pull`.
- **Check:** C18.

**T11 A closed opening is opaque at its jambs.**
- **Stephen:** from inside the front door, "post on the left, closed leaf on the right, daylight between them".
- **The cause:** a leaf overlapped its post by only `OV` = 2 cm while running 1.2 cm (inner track) to 6.4 cm (outer
  track) in front of the post face: an open slot, seen at 17° and more off the wall normal. The hikichigai meeting
  stiles overlapped 2 cm across a 1.2 cm track gap, and leaf boards had 4 mm gaps straight through the leaf.
- **The rule, as real doors do it:**
  - At the **closing** jamb, the leaf closes against a **stop** (todome) on the post, from the wall face out past the
    outermost leaf: `openings.jamb_stop`.
  - At a post or fixed stile a leaf **slides past**, a **lip** on its face fills the gap under the leaf (2 mm
    clearance): `openings.jamb_lip`.
  - Twin leaves overlap `MEET` = 5 cm at the meeting stiles (hikichigai and hikiwake).
  - Leaf boards butt tight (`LEAF_GAP` = 0). A through-gap needs something behind it.
  - Stops and lips are 3-face visual strips in Resolution 1 and 2 (no collision), so the sweep and reach checks do
    not change.
- **Judge it with C17, not by eye.** The old defect only shows at steep angles; C17 scores the pre-fix house at
  1,378 see-through rays at the entrance and 1,042 at the hikiwake pair.

**T12 Matte materials have no environment reflection.**
- **Stephen:** "every material is too reflective"; interior clay went green at glancing angles, with the normal-map
  swirls in the sheen, although its SMDI specular is only ~0.01.
- **The cause:** every JP rvmat used `fresnel(1.3,0.7)` with the outdoor, mostly green `env_land_co.paa`, and the
  SMDI map does not keep that reflection off at grazing angles.
- **The rule (this supersedes the Stage6/Stage7 line of §9 for matte materials):**
  - **Matte** (wood, bamboo, board and shingle roofs, thatch, straw, paper, stone): Stage6
    `#(ai,32,128,1)fresnel(0.01,0.01)`, Stage7 `#(argb,8,8,3)color(0,0,0,1,CO)`, as vanilla `planks.rvmat`,
    `logs*.rvmat`, `slama.rvmat` and `podezdivka_beton.rvmat` (65 vanilla Super rvmats).
  - **Earth and plaster walls:** Stage6 `#(ai,32,128,1)fresnel(0.49,0.14)` (vanilla `walls\data\wall_*.rvmat`),
    Stage7 black. Vanilla house plaster uses the Multi shader, which has no environment map at all.
  - **Glossy by design** (keep `env_land_co.paa` and `fresnel(1.3,0.7)`): kawara (ibushi, silvered), namako tile,
    iron. A new glossy material needs a vanilla analogue: glazed tiles `fresnel(1.42,0)`, rusty metal
    `fresnel(1.3,2.83)`.
  - Effective sun specular (specular × SMDI green) stays at or under about 0.02 for matte wood, like vanilla benches
    and deer stands.
- **Kit:** `build_materials.FINISH` / `finish_for(mid)`; `--rvmats-only` on `build_materials.py`,
  `make_part_materials.py` and `make_fix_materials.py` rewrites the rvmats without touching textures.
  **Re-binarize every ODOL that uses a changed rvmat** (the house, the swatch wall): ODOL embeds its materials.
- **Check:** C19.
