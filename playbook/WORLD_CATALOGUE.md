# JP World Catalogue v1: everything the world needs

**What this is:** the inventory for the 1730 Kyoto–Osaka–Edo map, with the Tōkaidō and Nakasendō. Nothing on it gets
forgotten.
- Rules and dimensions are in `PLAYBOOK.md`. Colours are in `palette.json`.
- Source IDs such as `[T11]` or `[c16]` are in `refs_index.json`.
- `(assumed)` = sensible but not yet sourced; the research agent (A) for that category must source it or drop it.

**Columns in the tables:**
- **Tier:** 1 rural/poor, 2 village/post town, 3 town/castle town.
- **Ext:** `distinct` means it needs its own exterior. `shell` means it reuses a generic shell with different
  furnishing or small add-on parts. `kit` means a parametric part family.
- **Var:** the number of variants needed for v1.
- **Pri:**
  - P1 = the first playable slice: one post town, one village, the road between them, one sekisho.
  - P2 = the castle town and the capitals.
  - P3 = landmarks and extras.
- **Stage** (pipeline):
  - A → B → C = research, then parts and materials, then architect.
  - D = decorator (furniture proxies).
  - S = site and exterior sets.
  - R = temples and shrines (later).
  - W = wearables.
  - F = flora.
  - T = terrain and placement.

---

## 1. Stephen's questions, answered

### 1.1 Did cities have walls or gates?

**Walls: mostly no. Gates: yes, everywhere, at a smaller scale.**

- **Castle towns:**
  - Moats, stone walls and earthen walls surrounded the **castle enclosures**, not the town. Only some towns built a
    full outer perimeter (sōgamae) [T16].
  - Streets were cranked, with dead ends and masugata box gates on the approaches [T16].
  - In game, a castle town has **no outer wall**. It has masugata gates where the roads enter, and walls around the
    castle.
- **Edo:** the castle's outer moat had guarded gates, the "36 mitsuke" [T24]. That is the castle's outer ring, not a
  town wall.
- **Kyoto:** Hideyoshi's **Odoi** (1591):
  - an earth rampart about 5 m high on a 20 m base, with bamboo on top and a 10–15 m moat
  - 22.5 km around, with 10 official gates
  - in the Edo period it was cut through and partly removed as the city grew [T14]

  Model it as broken, bamboo-covered earth banks and a dry or wet ditch, with roads cutting through. No gatehouses on
  it.
- **Ward gates (kido), the gates players meet most:**
  - In Edo, Kyoto and Osaka, **every chō had a kido at both ends**, closed at about 10 pm; after that people passed
    through a wicket door.
  - Each had a guard hut (bantaya) of 6 × 9 shaku with a 10-shaku eave, with two old gatekeepers who also kept fire
    watch [T11].

  → Kit: a kido gate (posts, beam, two leaves plus a wicket), a kidoban hut, and a jishinban ward office with a fire
  ladder.
- **Post-town ends:** mitsuke guard points [T24]. In practice these were an earth bank, often stone-faced, with a bend
  at each end of the post town (assumed; the A agent verifies with one surviving example).
- **Highway checkpoints (sekisho):**
  - Hakone opened about 1619, with two gates about 18 m apart, guard houses, a lookout, and wooden palisades running
    from the mountain to the lake [T15, c16].
  - It checked "guns going in, women going out".
  - → The map's pass chokepoints, one distinct complex per pass.

### 1.2 Were government buildings distinct?

**Yes.** Authority shows in **gates, walled compounds, formal entrances, black boards, white gravel and scale**. The
roofs and walls still come from the shared parts.

| Building | What makes it distinct | Source |
|---|---|---|
| **Honjin** (daimyo inn, one per post town, sometimes two) | Front gate, a genkan with a shikidai step and a jōdan-no-ma raised room: **features banned for ordinary inns**; a walled compound | [T19, T57] |
| **Waki-honjin** | Smaller honjin; ordinary travellers with enough status or money could stay | [T18, T57, c04] |
| **Toiyaba** (post office for horses and porters) | Open-fronted office on the main street, a yard for horse and porter relays, baggage stands. Tōkaidō stations had to keep 100 porters and 100 horses, Kiso stations 50 and 50 | [T21, T20] |
| **Kōsatsuba** (notice board) | Roofed board stand at bridges, crossroads and post-town centres, often on a stone base behind a fence. The 1711 boards stayed up for 150 years | [T23] |
| **Jinya / daikansho** (domain or shogunal district office) | One compound: gate, office, residence, storehouses, walls; smaller than a castle. Takayama Jinya survives | [T28] |
| **Bugyōsho** (town magistrate, Edo, Kyoto, Osaka) | Compound with a heavy gate, offices and a white-gravel court (oshirasu, assumed from the term; verify) | [T31] |
| **Samurai yashiki** | Nagaya-mon gatehouse (plaster allowed for samurai, boards for commoners), genkan, shoin rooms | [T29], PLAYBOOK §2.2 |
| **Fire towers** | Shogunal (jōbikeshi) towers from 1658, 3 jō (~9 m), plain wood; daimyo and town towers black and lower; in the Kyōhō period one per ~10 chō, otherwise a ladder on the ward office | [T12, T13] |
| **Kido and jishinban** | Gate plus guard hut plus ward office with a fire ladder | [T11, T12] |
| **Sekisho** | Two gates, guard houses, palisades, lookout | [T15] |

### 1.3 Do workshops differ outside, or can one shell be furnished?

**Mostly one shell.** A machiya, nagaya or farmhouse shell gets the trade interior plus a small **trade kit** of
exterior parts. **Six** trades need distinct structures.

| Trade | Exterior | Street-visible tells | Source |
|---|---|---|---|
| Smithy (kajiya) | shell + kit | Open front, earth floor, soot (W5), **ridge smoke vent** (koshi-yane) | (assumed; A to source) |
| Swordsmith | shell + kit | Smithy, plus a shimenawa over the forge and a small shrine shelf; a separate polishing room | (assumed) |
| Cooper, carpenter, tatami maker, weaver, lacquerer | shell | Goods and tools at the open front, noren, kanban | [T04] |
| Dyer (kon'ya) | shell + **yard frames** | Tall cloth-drying frames in the yard or on a roof platform; indigo vats sunk in the floor | (assumed; Hiroshige's Kanda Kon'ya-chō is 1857, check an earlier source) |
| Paper maker | shell + yard | Drying boards leaning in the sun | (assumed) |
| Oil press | shell | Interior only: the wedge press (shime-gi) | (assumed) |
| **Sake brewery (sakagura)** | **distinct** | Several large kura, the **sugidama** cedar ball under the eaves (early Edo; green when the sake is new, then brown), barrels, a well | [T25] |
| **Pottery kiln (noborigama)** | **distinct** | Stepped multi-chamber kiln up a slope, a shed, stacked firewood | [T37] |
| **Charcoal kiln (sumigama)** | **distinct** | Earth dome and a small shed in the forest | (assumed) |
| **Watermill (suisha-goya)** | **distinct** | Wheel plus hut on a stream; rice polishing and milling | [T38] |
| **Salt pans** (Edo bay) | **distinct** (site) | Levelled sand fields, boiling huts | (assumed; P3) |
| **Boat-builder's shed** | **distinct** | Open shed at the water, a hull on the stocks | (assumed; P3) |

### 1.4 Stables

- **Detached umaya:** a small board or thatch stable at farms, post towns and samurai houses of mounted rank. This is
  the P1 default.
- **Stable inside the farmhouse** (uchi-umaya, under the main roof off the doma): common in eastern Japan (assumed;
  A to source). → A tier-1/2 Kantō farmhouse variant.
- **Post-station horses:** stations had to supply 100 horses on the Tōkaidō [T20], drawn from townspeople and
  support villages. So post-town houses keep **stables at the rear** and the toiyaba has a yard with tie posts. There
  is no single big station stable.
- **Magariya** (L-plan house with the stable in the wing) is 18th-century Nanbu (Iwate) [T26]: **outside our map.
  Don't build it.**

### 1.5 Temple and shrine sets (stage R, later)

- **Buddhist temple:**
  - Buildings: gate (sanmon or sōmon), main hall (hondō), bell tower (shōrō), sutra store, priests' quarters (kuri),
    and a pagoda only at major temples.
  - Grounds: a cemetery, stone and bronze lanterns, a water basin.
  - Roofs are hongawara or bark. Timber is mostly unpainted, with vermilion on some gates.
- **Shinto shrine:**
  - Torii: shinmei (straight) or myōjin (curved) [T33].
  - Approach (sandō) lined with stone lanterns [T32, c22].
  - Purification basin (chōzuya), guardian dogs (komainu).
  - Worship hall (haiden), main sanctuary (honden), dance stage (kagura-den), fence (tamagaki), shimenawa ropes.
  - Vermilion (Inari [c10]) or plain wood; bark or shingle roofs.
- **Roadside and village sacred objects** (P1: cheap and everywhere):
  - stone jizō [c24]
  - hokora (a miniature shrine)
  - dōsojin: village-edge, pass and crossroads stones, mostly Edo or Meiji, densest in Nagano [T35]
  - kōshin-tō and batō-kannon steles (assumed)

### 1.6 Stone masonry

- **Tōrō:**
  - kasuga (tall, on a post) at shrines [c22]
  - yukimi (legged, by water) and ikekomi or oribe (post sunk in the ground) in gardens
  - oki-dōrō (small, standing loose)
  - bronze hanging lanterns at temples [T32]
- **Torii:** stone torii have existed since the 12th c.; wooden torii are painted vermilion with black only on the top
  beams [T33].
- **Ishigaki:**
  - nozura-zumi (rough) for terraces and rural walls
  - uchikomi-hagi (dressed joints) and kirikomi-hagi (fitted blocks) for Edo-period castles [T34, c09]
  - east Japan used less stone [T34]
- **Stone steps and bridges:**
  - steps up to shrines and temples
  - small slab bridges over drains
  - big bridges are wooden (assumed)
- **Gravestones:** commoner stone markers spread in the Edo period [T36]. Upright pillars on 2–3 bases,
  boat-shaped markers with a carved Buddha, and gorintō only for elite or old graves [T36, c24]. No family grave plots
  until Meiji [T36].
- **Road markers:**
  - **ichirizuka:** paired mounds about 9 m square and about 3 m high, one per ri (~3.9 km) on both sides of the
    road; trees are 55 % enoki, 27 % pine, 8 % cedar [T22, c17]
  - stone signposts at forks (assumed)
- **Paving:** the Hakone road was stone-paved in 1680, 2 ken wide, with 30–70 cm kerb stones [T53]. Use it for pass
  roads only; town streets are earth.

### 1.7 Street dressing, including anything hung between buildings

- **At the house front:**
  - noren (indigo with a white crest [c16])
  - kanban: hanging, standing, roof-top and 3-D signs
  - chōchin and andon signs
  - sudare and yoshizu screens
  - benches (shōgi); fold-down battari-shōgi in Kamigata
  - inuyarai bamboo guards (Kyoto) [c07, c08]
  - komayose rails
- **Fire:** tensuioke rain and fire barrels [T13] with stacked buckets (the stacking is assumed; verify in period
  prints); fire hooks and ladders.
- **Carrying:**
  - daihachiguruma handcarts (by 1703) [T54]
  - kago palanquins
  - shoulder poles
  - tawara rice bales
  - taru barrels
- **Horses:** water troughs, tie posts.
- **Laundry:** poles on upper drying platforms and in back alleys.
- **Between buildings:** no permanent lines crossed streets in the period views we have. Strings of festival lanterns,
  shimenawa and nobori banners are **seasonal event dressing** on bamboo poles (assumed; A to confirm with a
  pre-1750 image).

### 1.8 Other things the world needs

All of these are in the tables below:
- bridges, tea houses, inns, bathhouses, wells, markets
- docks and boats
- paddy features, granaries, drying racks
- fences, gardens and graveyards

---

## 2. Inventory

### 2.1 Dwellings

| Item | What / period evidence | Tier | Ext | Var | Pri | Stage |
|---|---|---|---|---|---|---|
| Poor farmhouse | Small minka: earth doma, a board or doza platform with an irori, thatch or boards weighted with stones [T17, c15] | 1 | distinct | 4 | P1 | A-B-C-D |
| Farmhouse with inside stable | Kantō type, the stable off the doma (assumed) | 1–2 | distinct | 2 | P2 | A-B-C-D |
| Village headman's house (nanushi / shōya) | Big thatch, a board nagaya-mon, a tatami best room, a kura [T29] | 2 | distinct | 2 | P1 | A-B-C-D |
| Fisherman's house | Boards, boards weighted with stones, a net shed (assumed) | 1 | distinct | 2 | P2 | A-B-C-D |
| Mountain hut / charcoal burner's hut | One room, earth floor | 1 | distinct | 2 | P3 | C |
| Machiya, small | 1 storey, 2–3 ken front [T04] | 2 | kit | 4 | P1 | C-D |
| Machiya, Kamigata | Zushi-nikai, mushiko, bengara koshi, udatsu, inuyarai [T05, c07, c08] | 3 | kit | 6 | P2 | C-D |
| Machiya, Edo | Dashigeta, open shop front, board or new tile roof [T05] | 2–3 | kit | 6 | P2 | C-D |
| Post-town house (Kiso type) | Boards, boards weighted with stones, low upper storey [c01–c03] | 2 | kit | 6 | P1 | C-D |
| Omote-nagaya (street-front row of shops) | Shared walls, a shop per unit [T56] | 2 | kit | 3 | P1 | C-D |
| Ura-nagaya (back-alley tenement) | Unit about 1.5 × 2 ken, kitchen at the door, shared well, toilet and rubbish point [T56] | 1 | kit | 2 | P1 | C-D-S |
| Low-rank samurai row (kumi-yashiki) | Plain row, small plots and gates (assumed) | 2 | distinct | 2 | P2 | A-B-C-D |
| Mid/high samurai yashiki | Plastered nagaya-mon, genkan, shoin rooms, garden [T29] | 3 | distinct | 2 | P2 | A-B-C-D-S |
| Daimyo yashiki (Edo) | Long nagaya-mon along the street, several halls | 3 | distinct | 1 | P3 | A-B-C-D-S |

### 2.2 Commerce, lodging, services

| Item | What / period evidence | Tier | Ext | Var | Pri | Stage |
|---|---|---|---|---|---|---|
| Shops: rice, sake, cloth, pharmacy, tools, tea, pawn, confectioner, bookseller | Machiya with `shop:<trade>` interiors, noren, kanban | 2–3 | shell | 1 interior per trade | P1–P2 | D-S |
| **Hatago** (inn) | Two storeys, lattice fronts, guest rooms; about 3,000 on the Tōkaidō [T30, c28] | 2 | distinct | 3 | P1 | A-B-C-D |
| Kichin-yado (cheap lodging, no meals) | [T18, T30] | 1 | shell (nagaya) | 1 | P2 | D |
| **Honjin / waki-honjin** | See §1.2 [T19] | 3 | distinct | 1 + 1 | P1 | A-B-C-D-S |
| **Roadside tea house** (kakejaya) | Open-front thatch or board shed with benches, tea and food [T18, c18] | 1–2 | distinct (small) | 3 | P1 | A-B-C-S |
| Town tea house | Machiya with a zashiki interior | 3 | shell | 1 | P2 | D |
| Bathhouse (sentō) | Since 1591; low zakuro-guchi into the bath, a men's rest room upstairs [T27] | 2–3 | shell + interior | 1 | P3 | A-D |
| Market | Periodic stalls (yatai) and the fish-market quay (assumed) | 2–3 | kit (stalls) | 4 stalls | P2 | S |
| Moneychanger / pawnbroker | Machiya plus kura | 3 | shell | 1 | P2 | D |
| Rice-warehouse row | Kura in a line along a canal | 3 | kit (kura) | 2 | P2 | C |

### 2.3 Workshops and industry: see §1.3 (shell trades are interiors in 2.10)

| Item | Tier | Ext | Var | Pri | Stage |
|---|---|---|---|---|---|
| Smithy (plus the swordsmith version) | 1–3 | shell + roof vent | 2 | P1 | B (vent part), D |
| Dyer's yard frames | 2–3 | site kit | 2 | P2 | S |
| Sake brewery | 2–3 | distinct complex | 1 | P2 | A-B-C-D-S |
| Noborigama | 1–2 | distinct | 1 | P3 | A-B-C |
| Charcoal kiln | 1 | distinct | 1 | P2 | A-B-C |
| Watermill | 1–2 | distinct | 2 | P2 | A-B-C |
| Salt pans, boat shed | 1 | distinct | 1 each | P3 | A-S |

### 2.4 Government, military, control

| Item | What / period evidence | Tier | Ext | Var | Pri | Stage |
|---|---|---|---|---|---|---|
| **Sekisho** checkpoint | §1.1 [T15, c16] | 3 | distinct complex | 2 (Tōkaidō, Nakasendō) | P1 | A-B-C-D-S |
| Toiyaba | §1.2 [T21] | 2 | distinct (small) | 1 | P1 | A-C-D-S |
| Kōsatsuba | §1.2 [T23] | 2–3 | site | 1 | P1 | S |
| Kido + kidoban + jishinban | §1.1 [T11] | 3 | kit | 1 set | P2 | C-S |
| Fire tower / fire ladder | [T12] | 2–3 | site | 2 | P1 (ladder), P2 (tower) | S |
| Jinya / daikansho | [T28] | 3 | distinct | 1 | P2 | A-B-C-D-S |
| Bugyōsho | [T31] | 3 | distinct | 1 | P3 | A-B-C-D-S |
| Guardhouse (bansho) at gates | Small board hut | 2–3 | kit | 2 | P1 | C |
| **Castle** set | Ishigaki, turrets (yagura), keep (tenshu), masugata gates (kōrai-mon + yagura-mon), plastered walls (dobei) with loopholes, moats, bridges [c09, T34, T16] | 3 | distinct (hero) | 1 keep + kit | P2 | A-B-C (hero) |
| Castle-town masugata gate | [T16] | 3 | kit | 2 | P2 | C |
| Mitsuke bank at a post-town end | [T24] | 2 | site | 1 | P1 | S |
| Prison (rōya) | Edo, Kodenmachō (assumed) | 3 | distinct | 1 | P3 | A-C |

### 2.5 Religious (stage R, later; the roadside items are P1)

| Item | Tier | Ext | Var | Pri | Stage |
|---|---|---|---|---|---|
| Jizō, hokora, dōsojin, kōshin-tō, batō-kannon [T35, c24] | 1–3 | site | 2 each | **P1** | S |
| Village shrine: torii, hokora or a small haiden, stone lanterns | 1–2 | distinct (small) | 2 | P1 | R-lite |
| Town shrine set (§1.5) | 3 | distinct | 1 set | P3 | R |
| Temple set (§1.5) | 2–3 | distinct | 1 set (+1 small village temple) | P3 | R |
| Graveyard: stones, wooden sotoba tablets, walls [T36, c24] | 1–3 | site | 6 stone forms | P2 | S |

### 2.6 Infrastructure: roads, bridges, water, docks, boats

| Item | What / period evidence | Tier | Ext | Var | Pri | Stage |
|---|---|---|---|---|---|---|
| Highway (earth) with pine rows | [T53, FEASIBILITY §3] | all | T | — | P1 | T, F |
| Stone-paved pass road | 1680 Hakone paving [T53] | — | site / T | 1 | P2 | S, T |
| Ichirizuka pair | [T22, c17] | — | site | 1 | P1 | S, F |
| Plank bridge (small) | (assumed) | 1–2 | site | 2 | P1 | S |
| Large wooden trestle bridge (the Nihonbashi type) | (assumed) | 3 | distinct (hero) | 1 | P2 | A-B-C |
| Arched drum bridge (taiko-bashi) | Shrines and gardens (assumed) | 3 | site | 1 | P3 | S |
| Stone slab bridge | Small drains (assumed) | 2–3 | site | 1 | P2 | S |
| Ferry landing + ferry boat | Wide rivers without bridges (assumed) | — | site | 1 | P2 | S |
| Well: pulley (tsurube) with roof; lever (hanetsurube); town supply well (jōsui-ido) | (assumed) | 1–3 | site | 3 | P1 | S |
| Irrigation channel, sluice | (assumed) | 1 | T / site | 2 | P1 | S, T |
| Quay steps (gangi), canal kura quay | (assumed) | 3 | site | 2 | P2 | S |
| Boats: river boat (flat-bottom), small fishing boat, ferry | (assumed) | — | site | 3 | P2 | A-S |
| Coastal cargo ship (higaki-kaisen type) | (assumed) | — | distinct (hero) | 1 | P3 | A-S |
| Lighthouse (tōmyōdō) | (assumed) | — | site | 1 | P3 | S |

### 2.7 Agriculture and rural

| Item | Tier | Ext | Var | Pri | Stage |
|---|---|---|---|---|---|
| Paddy bunds (aze), terraces with stone walls | 1 | T / site | — | P1 | T, S |
| Hasa rice-drying racks (poles and rails) | 1 | site | 2 | P1 | S |
| Straw stacks, straw bundles | 1 | site | 3 | P1 | S |
| Scarecrow, field hut, field shrine | 1 | site | 1 each | P2 | S |
| Kura (family storehouse) | 2–3 | kit | 3 | P1 | C-D |
| Gōgura (village granary) | 1–2 | distinct | 1 | P2 | A-C |
| Detached stable (umaya), barn / woodshed | 1–2 | kit | 2 | P1 | C |
| Detached toilet and bath hut | 1–2 | kit | 2 | P1 | C |
| Fumiguruma treadwheel for irrigation (verify its date) | 1 | site | 1 | P3 | S |

### 2.8 Walls, fences, gates, gardens (stage S)

| Item | What | Tier | Var | Pri |
|---|---|---|---|---|
| Ikegaki hedge; bamboo fences (yotsume-gaki, kenninji-gaki) | Garden and yard fences (assumed) | 1–3 | 3 | P1 |
| Board fence (itabei), black board fence | Towns, official buildings [c16] | 2–3 | 2 | P1 |
| Earthen wall with tile cap (tsuijibei), tile-course wall (neribei), plastered wall | [c29, c25] | 3 | 3 | P2 |
| Garden stone walls, nozura terrace walls | [T34] | 1–3 | 2 | P1 |
| Gates: board gate, roofed gate, nagaya-mon (board or plaster), kabuki-mon (assumed) | [T29] | 1–3 | 4 | P1–P2 |
| Tsubo-niwa (courtyard garden inside a machiya) | Stones, lantern, basin, shrub | 3 | 2 | P2 |
| Stroll-garden pieces: pond, stone lanterns, stepping stones, bridge, **plain-grey carp only** [T55] | Daimyo and temple gardens | 3 | 1 kit | P3 |
| Dry garden (gravel + stones) | Temples | 3 | 1 | P3 |

### 2.9 Street dressing and props (stage S): see §1.7

| Group | Items | Var | Pri |
|---|---|---|---|
| Shop fronts | Noren (plain and with crest), kanban (hanging, standing, roof-top), chōchin, andon signs, sudare, yoshizu | 3–6 each | P1 |
| Street furniture | Benches, battari-shōgi, inuyarai, komayose, tensuioke + buckets, rain barrels, water troughs, tie posts, fire ladders | 1–3 each | P1 |
| Transport | Daihachiguruma [T54], kago, shoulder-pole loads, pack-horse saddle and loads, tawara, taru, crates, nagamochi chests | 1–3 each | P1–P2 |
| Seasonal dressing | Festival lantern strings, nobori banners, shimenawa, New Year pine decorations | 1 set | P3 |

### 2.10 Furniture by room tag (stage D; each piece is a proxy, see PLAYBOOK §10.3)

| Room tag | T1 | T2 adds | T3 adds |
|---|---|---|---|
| `doma` | Kamado (clay), water jar (mizugame), tubs, buckets, firewood, straw sandals, a wooden sink | Shelves, a well bucket | Stone sink, a larger kamado |
| `daidokoro` | Irori with its pot hook (jizai-kagi), pots, mats, low shelf | Cupboard (mizuya), kamidana shrine shelf | Tansu, hibachi |
| `living` / `zashiki` | — | Zabuton, andon, a small chest, a butsudan | Tokonoma dressing (scroll, vase), byōbu screen, lacquer boxes (elite only), a tea set |
| `sleeping` | Straw mats | Futon stack, a kimono rack (ikō) | Tansu, a mirror stand |
| `shop:<trade>` | — | Counter (misedana), goods per trade | Counting desk (chōba) with a lattice screen, abacus, scales |
| `workshop:<trade>` | Tools per trade | Workbench, the trade kit | — |
| `storage` / `loft` | Straw bales, baskets | Chests, crates, barrels | Nagamochi, kura shelving |
| `stable` | Manger, straw, harness, a pack saddle | — | — |
| `guard` | — | Lamp, weapon rack, a clapper (hyōshigi) | Document box |

**Count:** about 60–80 furniture proxies for v1. P1 is the doma, daidokoro, living, sleeping and one shop.

### 2.11 Materials (stage B builds these first; one sheet per family)

| Family | Materials | Palette IDs |
|---|---|---|
| Wood | Weathered exterior timber, dark street timber, interior timber, sooted beams, new timber (rare) | timber_* |
| Walls | Shikkui, earthen ochre, arakabe (straw showing), neribei, namako, black boards, bengara plaster, board wainscot | shikkui_white, earth_wall_*, namako_*, kuro_board, bengara_wall |
| Roofs | Kawara (ibushi, weathered), thatch (weathered, new), boards weighted with stones, shingle | kawara_*, thatch_*, timber_weathered |
| Stone and ground | Granite, lantern stone, packed earth, doma, white gravel, moss overlay | stone_*, earth_road, gravel_white, moss_on_stone |
| Floors and paper | Tatami, heri, boards, shoji washi, fusuma paper (plain) | tatami_*, washi_shoji |
| Other | Bamboo, sudare, straw rope, iron, the textiles for noren and garments | bamboo_weathered, sudare_reed, iron_black, aizome_*, cha_*, nezumi_*, kinari_cloth |

Each material comes in 3 wear levels (`_w0` clean, `_w1` normal, `_w2` heavy), so there are about 30 materials.
**P1.**

### 2.12 Flora and ground

These are covered by stage F:
- sakura
- bamboo
- black pine for the road rows and the coast
- sugi cedar
- maple
- the enoki on ichirizuka [T22]
- paddy rice ground cover

---

## 3. Size of v1 (P1 only)

| Kind | Count |
|---|---|
| Distinct building types | about 10: poor farmhouse, headman house, Kiso post-town house kit, small machiya kit, omote-nagaya, ura-nagaya, hatago, honjin, tea house, toiyaba, sekisho |
| Kits reused | kura, stable, toilet and bath hut, guardhouse |
| Site sets | wells, fences, gates, kōsatsuba, ichirizuka, roadside sacred stones, drying racks, street dressing |
| Furniture proxies | about 35 |
| Materials | about 30 × 3 wear levels |

That is enough for one Nakasendō stretch: a post town, a village, a checkpoint and the road.

The castle town, the capitals, the temples and the boats follow in P2 and P3.


## Additions requested by Stephen (2026-09-27), research pending

| Item | Why | Notes for the research agent |
|---|---|---|
| **Onsen town inn (yuyado)** | Hakone (our test terrain's DEM source) was famous for its hot springs in the Edo period (the Hakone Nanayu); Arima near Osaka is among the oldest | Verify what a c.1730 onsen inn and its bath looked like. Communal bathhouses (sotoyu) and inn baths were more typical than the modern open-air rock pool; confirm with sources |
| **Hot spring pool** (steaming water) | Gameplay: a warmth or healing spot, and a landmark | Needs a pond-style water object plus steam particles. Check period form (bath hut vs open pool) |
| **Futons, tea sets** | Already listed under interiors (sleeping: futon stack; living: tea set) | Tea ware must be period-correct for 1730: kettles and matcha ware for the elite, cheap cups for tea houses. The side-handled teapot came later; verify |
