# W2C research notes: civic / roadside shells (agent W2C, 2026-10-01)

Research-first notes per building: period form, sizes, sources, the 1730 test. No web lookups were allowed in this
run: sources are the project's own research files (cited by path) and the playbook's reference index
(`playbook/refs_index.json`, IDs like [T11]). Anything from general knowledge is marked **(general knowledge)**.
Code: `parts/kit/jpparts/templates/civic.py` (template), `parts/kit/jpparts/gates.py` (new kit module, the kido),
`buildings/civickit.py` (recipe), registry block `W2C_*` in `buildings/registry.py`.

## TR01 Roadside tea house (KEEP_TRADES B1: 3 sizes; the pass tea house is a size)

**Period form.** BUILDING_LIST "Tea houses (one family, many forms)": the kake-jaya / chamise is an open-fronted thatch
or board shed on the highway or a temple approach, a doma with benches (shogi) covered in red felt or mats, a kettle on a
hearth or portable stove, tea bowls, a dumpling grill, sandals for sale under the eaves, reed screens [Kaempfer
1691-92; WORLD_CATALOGUE T18]. The tateba-jaya is the bigger tea house at the official rest stops between post towns
(Hatajuku on the Hakone road), where porters and horses changed: a doma plus raised rooms, meal trays, horse tie posts,
a palanquin rack. Lodging was banned at the rest hamlets (BUILDING_LIST settlement notes: "lodging banned, food and horse
changes allowed"), so the tateba's tatami room is a rest room, not an inn room. KEEP_TRADES: it also serves sake. The
battari-shogi (fold-down bench) is a shop-front fitting (KEEP_TRADES main rule; PLAYBOOK §3 Kamigata signature) and is
used here on the open shop and tateba fronts.

**1730 test.** All IN: tea houses on the Tokaido are attested by Kaempfer (1690s) [T18]; thatch, board and
stone-weighted board roofs are all period rural/roadside coverings (PLAYBOOK §2.1 T1-T2). No glass, no later fittings.

| Shell (class) | Size (ken) | Roof | What it is |
|---|---|---|---|
| Land_JP_Teahouse_Bench_Thatch | 2 x 1.5 | thatch kirizuma | kake-jaya bench shed: open front, board walls 3 sides, push-up shutter on one end |
| Land_JP_Teahouse_Bench_Itabuki | 2 x 1.5 + 1-ken bench roof | boards | the same with the front lean-to on posts over the benches (the "hung" roof) |
| Land_JP_Teahouse_Shop_Thatch | 3 x 2 | thatch | chamise: doma 2 ken (open front, battari in bay 1), raised board agari 1 ken with kamachi + step |
| Land_JP_Teahouse_Shop_Itabuki | 3 x 2 + lean-to | boards | the same with the bench roof |
| Land_JP_Teahouse_Pass_Ishioki | 3 x 2 + 2 lean-tos | stone-weighted boards | toge-jaya: stones on the roof (wind), front bench roof + woodshed lean-to on the doma gable |
| Land_JP_Teahouse_Tateba_Thatch | 5 x 3 | hipped thatch, shiba ridge | tateba: doma 2 ken full depth (open front, battari), agari (boards) + zashiki (tatami, hikiwake from the agari) |
| Land_JP_Teahouse_Tateba_Itabuki | 5 x 3 + lean-to | boards | the same with gables and the bench roof |

Variant axes: size (bench / shop / pass / tateba) x roof (thatch / itabuki / ishioki) x the front lean-to (board roofs
only: a pent cannot sit under a thatch eave, C2's finding). Walls: weathered boards; the tateba has earth walls
(nakanuri) over a board skirt (koshiita), a step up for the bigger house. Floors: earth doma; agari 0.40, tateba rooms
0.45 (PLAYBOOK §4); tatami only in the tateba zashiki (T2: tatami in 1-2 best rooms). Sizes are reasoned, not sourced
(no dimensioned tea house in the project research): a bench shed of ~10 m2 and a 3 x 2 ken shop sit between the field
hut and the post-town house; the tateba at 5 ken matches the C1 inn frontage.

## TR11 Smithy + swordsmith (KEEP_TRADES B11)

**Period form.** BUILDING_LIST "Village and farm-tool smith (kaji-ya)": street-edge workshop, open front, doma, soot, a
roof smoke vent; forge hearth (hodo), box bellows (fuigo), anvil (kanatoko) set in a stump, quench tub, tongs, sledges,
charcoal bin, finished hoes and sickles on the wall. WORLD_CATALOGUE: "open front, earth floor, soot, ridge smoke vent
(koshi-yane)". Swordsmith (katana-kaji): town or castle-town workshop, "darkened forge room to read the steel's
colour", forge with a shimenawa over it, kamidana, box bellows, anvil, strikers' sledges, clay-coating trough
(tsuchioki), long quench trough, blade rack. KEEP_TRADES: "Seki and Sakai blades".

**1730 test.** IN (smithing in every village; Seki / Sakai sword and knife trades long established; the koshi-yane vent
is a kit part already approved at G1). Earth walls over a board skirt for fire (general knowledge).

| Shell (class) | Size | Roof | Notes |
|---|---|---|---|
| Land_JP_Smithy_Open_Itabuki | 3 x 2 ken | boards + koshi-yane | village smithy: 2 front bays open, 1 walled with a push-up shutter; back door; end window |
| Land_JP_Smithy_Open_Sangawara | 3 x 2 ken | sangawara + koshi-yane | the town smithy (tile, T3) |
| Land_JP_Swordsmith_Sangawara | 4 x 3 ken | sangawara + koshi-yane | closed: front work doma (itado pair entrance, window) + the darkened forge room behind a partition (katabiki door), one high shutter, a side door to the yard |

All earth-floored, koyagumi framing sooted (sawn members). The koshi-yane is built in the template (`civic.koshiyane`)
at the roof's own ridge height (the kit part `jp_p_roof_kemuridashi _koshiyane` is a free-standing sample with posts
that would enter the roof body, C12); the main roof stays closed under it (a visual vent; C11 / C12 clean).

## GV1 Guard hut (KEEP_CIVIC government 1)

**Period form.** PLAYBOOK §4 + [T11] (ja.wikipedia "Kido-ban"): the kido guard hut (bantaya) is 6 x 9 shaku with a
10-shaku eave, two old gatekeepers who also kept the fire watch; in Edo they sold cheap goods on the side (sandals,
candles, sweets, paper, charcoal). The jishin-ban (townsmen's self-watch post) doubles as the ward office, often with a
fire ladder on the roof (Kyoho: "ladders on jishinban" [T12]). The tsuji-ban, bridge keeper, ferry hut, border post and
water guard are the same small board hut with other props (KEEP_CIVIC: one prop decides).

| Shell (class) | Size | Notes |
|---|---|---|
| Land_JP_Guardhut_S_Itabuki | 1.5 x 1 ken = 2.73 x 1.82 m (9 x 6 shaku), eave 3.03 (10 shaku) | katabiki door on the long side, doma by the door, a raised board platform (0.40) on the far end with the push-up counter shutter |
| Land_JP_Guardhut_S_Sangawara | same, tiled | the town version (T3) |
| Land_JP_Guardhut_M_Itabuki | 2 x 1.5 ken | the jishin-ban size: + an end window, the fire-ladder spot on the ridge |

## GV7 Ward gate (kido) + gatekeeper hut

**Period form.** BUILDING_LIST + WORLD_CATALOGUE §1.1 [T11]: in Edo, Kyoto and Osaka every cho had a kido at both ends:
"posts, beam, two leaves plus a wicket", closed at about 10 pm, after which people passed through the wicket; a
bantaya beside it. PARTS_GAP_AUDIT #2/#3 name the kido leaves as lattice.

**As built.** Two 0.18 main posts 1.5 ken apart, a tie beam (kashira-nuki, underside 2.40) through all posts and a
kasagi cap beam on the post tops (2.95), the two hinged leaves (lattice over a board base, or battened boards) on the
ward face, turning 90 deg into the ward together (one DoorsTwin, two rotation bones: `gates.gate_leaves`), and a
wicket bay beside it: a fixed half-ken board panel, the wicket as a katabiki door, its park half-ken; board panels up
to the tie beam. A 5 cm earth threshold strip is the floor. Gate width 3.5 ken (6.37 m): a town street is 3.6-7.3 m
(PLAYBOOK §4).

| Shell (class) | Leaves | Head | Notes |
|---|---|---|---|
| Land_JP_Kido_Lattice | lattice | tie beam + kasagi | the common kido |
| Land_JP_Kido_Board_Roofed | boards | small board gable roof on cross pieces | **(general knowledge)**: roofed kido read as the better-kept ward gate; flag for Stephen |
| Land_JP_Kido_Lattice_Bantaya | lattice | kasagi | + the kido-ban hut (= Guardhut_S) inside the ward, half a ken past the wicket end and 1 ken back, its door facing the passage, its counter shutter facing the gate |

**Deviations (logged).** D1: the period wicket was a small door to stoop through; here it is a 1.08 m katabiki door
(D1 >= 1.00). The gate leaves are the second hinged leaf type after the kura's: engine-untested (rotation sense
recorded in PLAYBOOK §15 T4; if a leaf swings the wrong way, swap its two axis points in `gates.gate_leaves`).

## Budgets (PLAYBOOK §12; faces R1 / R2 / R3, from buildings/<family>/checks/*.json)
- small (3,000 / 1,150 / 400): bench sheds, guard huts, kido without the hut.
- standard (6,000 / 2,300 / 800): shops, pass tea house, open smithies, Kido_Lattice_Bantaya (two structures in one
  object).
- large (12,000 / 4,600 / 1,600): the 5-ken tateba and the 4 x 3 ken swordsmith (as C1's 5-ken inns and 4-ken end units).
- civic far-LOD trim (`civic.trim_lods`): window bars as their slab from Resolution 2, small roof-frame members R1 only,
  tie beams / collars / door tracks / board-wall top rails / verge battens out of R3; on the pass tea house every second
  remaining roof stone in R1.
