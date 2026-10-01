# Japan test island: the showcase walk (~44 min)

Everything built so far, in one walk: the furnished wave-1 town and hamlet, the two storehouses (kura), the machiya
shop, the new materials, and four new things: a **shrine** with a hill stair, a **graveyard**, S1's **six demo shops**
on the street, and a **gallery** of all 74 life-layer items.

**Start:**
1. Run `start-japan-test-island.bat` in the server folder. It starts only the test server, on its own port, so the
   live server is unaffected.
2. When the server is up, run `start-japan-test-client.bat` to join.
3. **Open the four labelled maps** (keep them on a second screen):
   `research/production/contact_sheets/sh1_map_street.jpg`, `sh1_map_shrine.jpg`, `sh1_map_graveyard.jpg`,
   `sh1_map_gallery.jpg`. Every new object has a short ID on them (S.., G.., L.., D..). To point at something, just
   say the ID ("graveyard G3-07 floats", "I like L31"), or send a screenshot and say roughly where you stood.
   Pictures of everything: `sh1_shrine.jpg`, `sh1_graveyard.jpg`, `sh1_shops.jpg`, `sh1_gallery.jpg`, plus C3's
   `c3_rooms.jpg`, `c3_street.jpg`, `c3_hamlet.jpg`, `c3_kura.jpg` (same folder).

**If it won't load, kicks you, or something is invisible:** just tell me. I read the server and client logs myself,
so you don't need to open any log.

**The route** (you spawn facing north; the machiya shop is ~55 m ahead, the town street ~95 m ahead behind it):
gallery (east) -> machiya -> town street + shops -> town kura -> graveyard -> shrine + hill stair -> hamlet + its kura
-> back to the spawn. Walking total ~800 m.

**Not in this walk:** zombies inside buildings (no new navmesh). The shrine has no hall building yet: its hall site is
left empty on purpose.

## 1. The life-layer gallery (6 min) — stop 9

Turn half right (north-east) and walk ~65 m: three open board sheds facing you (LS1-LS3, west to east), with a strip
of yard and street things on the ground in front. One of each of the 74 life-layer items, at its proper mount, each
labelled **L + its number in research/interior/LIFE_LAYER.md** (map `sh1_map_gallery.jpg`).

- **Shed 1 (west): walls, posts and beams.** Back wall, west to east: L7 sandals in bunches, L6 rope coils, L4
  kitchen utensil board, L5 tool wall, L1 mino raincoat + hat. West side wall: L47 bow rack, L11 umbrella. East side
  wall: L14 fire buckets + hook, L3 printed calendar. Front post (right of the middle): L2 paper charms. Hanging from
  the front beam, west to east: L9 drying daikon / fish, L8 dried persimmons, L12 inner noren (middle bay), L13
  folded mosquito net. Floor: L19 meal left behind, L22 steamer on a pot (it belongs on a stove: none here), L27
  cushions, L25 charcoal bale, L23 casks.
- **Shed 2 (middle): shelves and the living room.** Back wall shelves: left shelf (LH1) top: L20 sake flasks, L17
  kamidana offerings, L16 Buddhist altar set; bottom: L26 fire-striker, L44 measures, L43 account desk clutter. Right
  shelf (LH2) top: L24 baskets, L42 writing box, L48 tea things. Shelf on the east wall (LH3): L18 tableware stack,
  L21 grinding bowl, L31 sewing box. Front beam: L10 paper lantern. Floor: L15 Buddhist cabinet, L35 candle stand,
  L28 screen, L34 toys, L36 straw bed, L30 dropped kimono, L32 mirror stand, L33 go board.
- **Shed 3 (east): work and tier markers.** Floor: L49 manger, L39 straw work, L29 clothes rack, L46 armour chest,
  L40 winnowing basket, L37 spinning wheel, L45 sword rack, L50 fallen shoji leaf, L38 hand loom, L41 rice mortar.
  Under the front eave: L59 bird cage, L69 sandals for sale, L52 persimmon curtain.
- **Leaning on the end walls (outside):** L56 ladder, L57 charcoal bales (shed 1, west end); L54 farm tools, L71
  shutter (shed 3, east end).
- **Ground strip, front row (west to east):** L63 dropped travel gear, L74 scattered clogs, L72 fallen lantern, L73
  stool, L70 tea things on the bench (LH4), L53 moon-viewing stand, L58 potted plants, L61 tie post, L62 scarecrow,
  L68 fire-watch rack. **Back row:** L51 rice rack, L60 bamboo pipe + trough, L55 leaf pile + broom, L65 spilled
  vendor's load, L64 palanquin. Further out: L67 boat (south-west), L66 fishing net (east end).

## 2. The machiya shop and yard (2 min) — stop 4 (the baseline you already passed)

Walk west ~55 m to the machiya (the building straight north of the spawn). Just a quick look round the shop room and
the back yard (well, toilet, firewood): it is the reference the newer houses are measured against. **M1 spot check:**
the firewood stack by the yard wall has the new firewood texture (warmer, less red).

## 3. The town street (6 min) — stop 1

Walk round the machiya to the street behind it (the rows of townhouses, east-west).

- **Seams:** look along both rows from the street and from the back: where the units meet (pent ends, the fire walls
  between Kamigata units), any gaps, flicker, or light through a party wall from inside? The rows are longer now
  (section 4), so there are more joins to look at.
- **The south row (facing north):** the **post-town house** (west end: a lived-in home, bench and sandals for sale
  under its eave), two bare row houses, then the **inn** and the **grand inn**.
  - Inn: the office with the counting desk and its lattice; two guest rooms with bedding and left-over meals; the big
    kitchen with three stove mouths.
  - **Grand inn upstairs:** go in, through the back room behind the office, and **climb the box stair**. Walk both
    upstairs guest rooms (bedding, a dragged-off futon, a go board with the stones scattered). Open the upstairs
    street windows.
- **C3's shops on the north row:** the **rice dealer** and the **paper shop** (Kamigata, middle of the west part),
  the **cloth dealer** and the **sake shop** on the corner (Edo, east part).
- **The ward corner** (north side, between the two rows): fire-watch ladder with its bell, bucket rack, notice
  board, Jizo, a crossroads lantern. Behind it you can already see the shrine's first stone torii. **In the street:**
  tipped palanquin, dropped hat and stick, burst bundle, spilled loads, a fallen shutter, clogs, torn lanterns, a
  broken handcart.

## 4. S1's demo shops (5 min) — stop 8 (map `sh1_map_street.jpg`)

Six shops dressed by the new shop-set kit, each with its goods on a board display strip, a counting desk and its own
signs out front. Three took the place of bare units of the same type; three are new units added to the rows.

- **North row, west part (Kamigata), from the west:** a bare end unit (moved to the new row end), **D6 dolls**
  (new), **D2 tobacco** (new), the paper shop, the rice dealer, **D3 sweets / rice cakes** (east end of the row; it
  replaced the bare corner unit).
- **North row, east part (Edo), from the west:** **D4 apothecary** (west end, the heaviest abandoned state; it
  replaced the bare 2-ken end unit and is one ken wider), **D1 ironmonger** (replaced the bare board-roof unit),
  **D5 tailor** (new, board roof), the cloth dealer, the sake shop.
- At each: do the **front signs** read the right way round, and do they fit the trade? Go into two or three: the
  goods on the display strip, the shelves, the desk. Anything floating or clipping?

## 5. The town kura (2 min) — stop 3, part 1

Behind the Kamigata row (behind the rice dealer): all white with the diagonal tile pattern. Its outer leaves are fixed
open (static). Walk the stone step at the door, climb the stair along the back wall to the upper floor (chests,
shelving, the guard rail round the stairwell).

## 6. The graveyard (4 min) — stop 7 (map `sh1_map_graveyard.jpg`)

From the kura walk ~20 m north: an old village graveyard, rows facing south. Its gate is on the east side, onto the
shrine approach: six Jizo in a row (GJ1-6, a seventh knocked over), the water point (basin GW1, bucket rack GW2, a
rack of spare slats GW3). IDs are **G + row - plot** (row 1 = the front/south row, plot 1 = west end).

- **The mix:** mostly board-shaped and boat-halo stones, round-headed slabs (newer), field stones and earth mounds,
  child Jizo; square pillars are rare (G5-04, G6-06, G7-06). The old section is the back row: the **2 m gorinto on
  its platform (G7-10)**, hokyointo G7-07, gorinto G6-03 / G7-03, the re-stacked one G6-14, the fallen one G7-05, the
  fragment heap G7-01, the broken hokyointo G7-12.
- **Text:** the carved posthumous names on the faces of the board / boat-halo / round stones; the Sanskrit seed
  syllables on the gorinto rings and the hokyointo body. Readable, the right way round?
- **Gorinto seating:** do the rings sit flat on each other (G1's fix)? Any gap?
- **Wooden grave posts (bohyo) on bare-earth mounds, front rows:** new pale post G1-01, grey posts (G1-02, G2-13,
  G3-06), short ones (G1-05, G2-03, G6-16), the one with a little roof G1-13, leaning G2-04, split and black G3-08,
  rotted to a stump G1-07 / G5-07. **Do new and silver-grey posts look different enough now?**
- Slats behind about a third of the stones, flower tubes and incense stands before some, slats blown into the
  aisles (GF), leaf litter under the old oak (GT1, a vanilla tree).

## 7. The shrine and the hill stair (7 min) — stop 6 (map `sh1_map_shrine.jpg`)

From the graveyard gate step east onto the approach.

- **The approach (south to north):** the large stone torii (S01) at the town end, shrine banners, a corner of old
  roadside stones (S06-S13), the second large stone torii with straw rope and paper streamers (S14, the precinct
  boundary), the water basin (S15), lantern pairs (Kasuga 2.4, square, mossy ones, one with its top jewel fallen
  S26), the wooden myojin torii, mossy with rope (S22), tall Kasuga 3.0 and the two joyato (S27-S30), small placed
  lanterns (S31/S32) at the **hall site (empty, z 1186-1198)**. Beside it the **sacred tree**: a vanilla beech with a
  straw rope round its trunk (S33/S34). **Does the rope sit on the bark, or float / cut in?**
- **The sub-shrine row** along the east side (S40-S51, facing the approach): every small torii form side by side:
  wooden shinmei plain / rope / rope + streamers / mossy / mossy + rope / mossy + rope + streamers, small stone torii
  plain / rope / rope + streamers / mossy / mossy + rope + streamers, a rotted one (S51). Behind each a stone-roofed
  hut or a stone stands in for a small shrine (no hokora exists yet). Mini torii S52 / S53.
- **The hill stair:** from the hall site follow the lantern pairs north-east (one lantern toppled, S91; an old torii
  leaning in the trees, S62) to the medium stone torii with rope (S63) and **climb the stair**: wide dressed flights
  with cheek walls at the bottom, then plain and rough flights, old heaved ones near the top, a 6-step flight with
  cheek walls and a wide one at the very top. Five plain-wood myojin torii span it (S64-S68). At the top (~20 m
  above the town): the oku-miya (S70-S74). **Does it walk smoothly up AND down? Any step you snag on, sink into or
  float over?** Look back over the town.
- **The Inari corner:** east of the hill stair, a narrow stair through vermilion torii (S80, S81), a vermilion torii
  leaning at its foot (S82), a mini vermilion torii and a stone hut at the top (S83-S85).

## 8. The hamlet and its kura (10 min) — stops 2, 3 (part 2) and 5

Walk back down and south-west to the thatched houses (~180 m from the hall site; the hamlet is west of the machiya). Threshing yard in
the middle with a big straw stack.

- **Kanto farmhouse** (the big hipped-thatch house at the back left, facing you):
  - **Its look first.** C2 raised its walls 0.42 m and gave it no skirt roof over the door, because a skirt roof
    can't fit under the thatch eave. **Does the house look too tall / leggy from the yard?**
  - Persimmons under the front eave; tools by the big plank door. Inside: the doma with the two-mouth stove, the horse
    stall, a rice mortar, rice bales; up on the board floor the irori with its pot hook, drying persimmons and daikon,
    a meal tray, the Buddhist shelf.
  - **M1 spot checks:** the best room (tatami): **do the tatami borders read brown now?** The bedroom:
    **the open wicker trunk: warmer, less grey?** The firewood by the stove: **the new firewood**.
  - Outside at the west end: the stable yard (tie post, pack saddle on a rack, stone trough).
- **Kinai farmhouse** (the tall house to the right with the tiled lower roofs): ox stall, stove, stone hand mill,
  the ground loom; **its best room (zashiki) also has the brown tatami borders.**
- **The huts across the yard** (south side): the left (east hut, board floor) and middle (west hut, woodshed
  lean-to) are furnished, poor and sparse; the right one is bare on purpose.
- **Sheds behind the farmhouses:** the walled one has bales, shelving and a winnow; the open one is bare.
- **Around the yard:** rice racks, stooks and a scarecrow, persimmons and daikon on poles, a bamboo pipe into a
  trough, the **lever well** by the huts: crouch at it: does **Drink** show? Does a bottle fill?
- **Hamlet kura** (white with black boards, east edge of the hamlet, door facing the hamlet):
  - **The plaster door leaves are real doors.** They start open. Close both, then open them again, from outside. Do
    they swing the right way (outwards)? Do they clip into the stepped plaster surround?
  - The inner sliding plank door: open, walk in, close it behind you, open it again.
  - **Climb the stair** to the upper floor: walks smoothly? Long chest, shelving, toppled boxes, the guard rail, the
    small barred windows in both gables.

Then back to the spawn (~80 m south-east).

## 9. Everywhere, as you go (2 min of attention) — stop 10

- **How full do rooms feel, per type?** (townhouse shops incl. the six demo shops, post-town house, inn, grand inn
  upstairs, Kanto farmhouse, Kinai farmhouse, huts, shed, kura.)
- Anything **floating, sinking or see-through**: give the ID if it has one. Known and on purpose: gutter covers sit
  low (they belong in a ditch), the leaning / fallen torii (S62, S82) lie partly in the slope, the sotoba slats and
  wooden posts stand 15-20 cm deep, stone lanterns on the hill top are set into the slope.
- **Doors:** every door opens and closes from both sides; nothing blocks a door.
- **Loot:** on floors AND on furniture (shelves, chest tops, bales, desks). The gallery sheds get loot too.

## Tell me

- What failed, and what still looks wrong (with IDs where there is one).
- Your verdicts on:
  1. **Kanto farmhouse:** too tall / leggy without a skirt roof, or fine?
  2. **How full do rooms feel**, per type (list above): too sparse / right / too cluttered?
  3. **Hinged kura leaves:** swing the right way, open and close from outside?
  4. **Kura stair and upper floor:** walks fine? Worth the extra height?
  5. **Grand inn stair and upstairs rooms:** fine?
  6. **Street seams** between the townhouse units: any gap, flicker or light?
  7. **The lever well** in the hamlet: Drink / fill?
  8. **The dead-world street:** does the litter tell the "people fled" story, or is it too much / too little?
  9. **M1 materials:** brown tatami borders, new firewood, warmer wicker trunks: better, worse, the same?
  10. **The shrine:** does it read as a village shrine? The hill stair: walks fine up and down? Which torii and
      lantern variants do you like or not (IDs)?
  11. **The graveyard:** right mix and density? Names and seed syllables readable? Gorinto rings seated? New vs
      grey wooden posts different enough?
  12. **The demo shops:** which shops and signs read right, which don't (D1-D6)?
  13. **The gallery:** which life-layer items do you like, which should change or go (L numbers)?
  14. Anything floating, sinking or see-through (where / which ID)?

Screenshots help but aren't required.
