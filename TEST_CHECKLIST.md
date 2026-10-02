# Japan test island: FX5 re-check (~5 min) + wave 3c-1, the trade quarter (~15 min)

Short re-check of the four things you flagged on the 3a / 3b walk (2026-10-02). The old 3a / 3b walk text is in git
history. **Then section 3c-1 at the end: the new trade quarter (brewery, dyer, paper mill, water mill).**

What changed: every compound gate (all 9: samurai, Kanto headman, honjin x2, merchant, foot-soldier row, doshin x2,
stable / timber / foundry yards) now has a packed-earth sill 10 cm high with sloped edges instead of a floor lying
exactly at ground height (that was the flicker). The honjin's side board fences now run right up to the plastered
street wall (there was a 0.7 m gap). The Kanto headman's hedge is rebuilt as one continuous clipped hedge with a new
leaf texture and a leafy top edge. Pictures: `research/production/contact_sheets/fx5_gates_joints.jpg` and
`fx5_hedge.jpg` (before left, after right).

**Start:**
1. Run `start-japan-test-island.bat` in the server folder. It starts only the test server, on its own port.
2. When the server is up, run `start-japan-test-client.bat` to join. You spawn at ~1024, 985.

**If it won't load, kicks you, or something is invisible:** just tell me. The lead reads the server and client logs.

## 1. Gates: no flicker under the gate (2 min)

At each gate: look at the floor under the gate first from ~30-50 m away, then walk up to it, then walk through it
both ways (open the leaves).
- **Honjin front gate** (1103.6, 1067.8; the roofed gate in the white plastered street wall).
- **Honjin back gate** (1109.5, 1020.5; the plain gate in the board fence at the back).
- **Timber yard gate** (1012.3, 922.0; wave 3b, the yard on the slope south of the spawn). Also, if you pass it,
  the **stable yard gate** (1068.8, 1062.8).
- One more on the way back: **doshin house gate** (963.2, 952.1).

Pass: the earth under each gate doesn't flicker or shimmer, near or far; the sill is a low, rounded hump you walk over
without a stumble or a hop; the gate leaves open and close without scraping into it; you can still drop / pick up loot
on it.

## 2. Honjin: plaster wall meets the board fence (1 min)

- **North-east corner** (1124.9, 1067.8) and **north-west corner** (1094.0, 1067.8) of the honjin compound: where the
  white plastered street wall meets the wooden side fence. Look from inside and from outside, try to walk through and
  look through at the joint.

Pass: no gap. The fence's last post stands against the plaster; you can't walk, see or shoot through the joint.

## 3. Kanto headman hedge (2 min)

- The tall clipped hedge round the Kanto headman's compound: the **west side** (x ~924, z 961-992) and the **back gate**
  (942.2, 991.9). Walk along it at eye level, close up and from ~15 m, and look at a corner.

Pass: it reads as one continuous clipped hedge: no repeating segments, no bulges, no visible seams every 1.8 m; leafy
top edge; corners closed. You still can't walk, see or shoot through it, and there's no slit beside the back-gate posts.
If it now looks too flat or too uniform, say so.

## 4. Town temple corridor U9: deliberately unchanged

U9 (the hondo -> kuri corridor) is left exactly as it was, on your call: corridor-to-hall joins get done at the end of
production on modular variants of the final halls (PRODUCTION_PLAN.md "Confirmed future work"). No need to look at it.

## 3c-1. Wave 3c-1: the trade quarter — sake brewery, indigo dyer, paper mill, water mill (~15 min)

Built and placed by W3C1 (2026-10-02): 12 new shells (the brewery's two kura, the rice-polishing shed, water mill x2,
dyer x2, paper mill x2, three yard fences), 8 furnished variants, 22 new props (40 models), 3 new parts (the water
wheel, the flume, the gutter that joins the two brewery roofs). Nothing here has been seen in the engine yet.
Pictures: `research/production/contact_sheets/w3c1_family.jpg` (every shell + the kasane-gura pair),
`w3c1_rooms.jpg` (the furnished rooms + the machinery), labelled map `w3c1_map.jpg` (every ID below is in
`spikes/SH1/SHOWCASE_MAP.md`, W3C1 section).

**New this wave: everything is in ONE district,** away from the earlier showcase: south-west of the spawn, just off
the corner of the flat yard, x 884-946, z 852-892. An east-west lane runs through it at z ~864. The brewery and the
dyer are north of the lane, the water mill south of it, the paper mill at the east end.

**Start:** spawn (~1024, 985). Walk south-west ~160 m (past the samurai quarter, down off the yard's corner) to the
lane's middle at about **(915, 864)**. The route below starts and ends there.

**Route (~350 m, ~15 min):** lane middle -> brewer's shop -> brewery gate -> the yard (polishing shed, cask kura) ->
the front kura -> round to the big kura's west door, through it, out the east door -> back out of the gate -> dyer's
shop, vat room, back door to the drying yard -> paper mill + its yard -> water mill across the lane -> lane middle.

**1. Brewer's shop (1 min).** BR6 (910.3, 868.9), front open south to the lane. Look up at the **sugidama**: a big
brown ball of cedar sprigs hung under the front beam (brown = the season's sake is ready; new ones are green). Inside:
casks on racks, a cask with measures on it, the raised room (step up) with the counting desk.

**2. Brewery yard (2 min).** BR1, black board fence; the **wide gate on the lane at (893.6, 868.0)**: open and close
it, walk through both ways (the earth sill under it should not flicker). In the yard: **BR4 polishing shed** (900.9,
871.0, open to the north): four **foot-treadle mortars** (a long lever on a pivot, the pestle over a stone mortar, a
hand rail for the treader at the back; one lever lies off its pivot). Walk round them: solid? **BR5 cask kura**
(888.0, 870.9, door north): casks on both floors, stair up.

**3. Front kura, the mae-gura (3 min).** BR3, the long white kura with black boards along the yard; three kura doors
on its front (south) face. From east to west:
- **East door (901.3, 876.9) and the middle door (897.7, 876.9)**: one long earth floor: the washing floor and the
  **steaming hearth** — a big clay-and-stone hearth with its fire mouth to the front, the iron cauldron in it and the
  tall wooden **steamer (koshiki)** on top with its lid. The louvred steam vent on the ridge above it.
- In the west wall of that floor, a board door into a small **ante-room**, and from there a second door into the
  **koji room** (the double doors): low board ceiling, straw-mat lining on its partitions and ceiling, the koji bed
  (a broad table with its cloth folded back) and shelves of koji trays, half pulled down. Both doors both ways.
- **West door (889.5, 876.9)**: a small earth entrance and the brewers' rest room (step up onto the boards: bedding,
  a trunk, rain capes).

**4. The big kura, the o-kura (3 min).** BR2, behind the front kura (the two stand side by side, Nada style). Walk
round the **west end** of the front kura to the big kura's **west gable door (886.4, 886.6)**: in from the stone
step. Inside, one tall earth-floored hall under the bare log roof frame:
- the **lever press** along the north wall: the press box, two heavy posts with a cross-beam at its head, the ~6 m
  beam over the box, six **weight stones** hanging in rope slings at the free end; the receiving jar under the spout.
- **four big fermentation tubs** (1.8 m across), one with a ladder leaning on it, one fallen apart (staves on the
  floor); casks on racks; a **Hatcho-style miso vat** with a cone of river stones on its lid.
- at the **east end** the loft: a stair along the north wall up to the starter loft (shallow tubs), the loft edge
  railed. Up and down the stair; walk the loft (head room under the roof beams?).
- out through the **east gable door (903.4, 886.6)**. Between the two kura: the gutter where the front kura's back
  eave meets the big kura's wall (look from either gable end; the narrow slot between them is boarded at both ends).

**5. Dyer (2 min).** Back out of the brewery gate, east along the lane. **DY1 indigo dyer** (918.7, 869.3): the shop
open to the lane with dyed cloths hung at the front (indigo and undyed; plain, no tie-dye pattern yet). Step up
over the stone kerb into the **vat room**: **four indigo jars sunk to the rim in the floor** round a square fire pit,
two with lids; the dark dye 15 cm down; sukumo indigo in straw bales, the lye drip tubs, the pole rack. **Walk over
the vats and the pit edge: do you sink, stick, or see under the floor?** Out the back door (916.8, 872.1) and through
the yard gate behind it into the **DY2 drying yard**: two tall drying frames (5.6 m) with long indigo lengths hung
doubled, a third with cloths fallen and torn.

**6. Paper mill (2 min).** **PM1** (935.0, 868.9), door on the lane (933.2, 866.6): the paper vat under the windows
with the mould hung from a bamboo spring pole, the bark-beating board with mallets, the couching stack under its
small lever press with stones, a picking tub; outside the west end, under the lean-to, the bark steamer. Its **drying
yard PM2** behind it (bamboo fence; gate at the south-east corner, take the path east of the mill): drying boards
leaned to the sun with paper sheets on them, one rack fallen flat.

**7. Water mill (2 min).** Back west along the lane. **WM1** (916.0, 857.8), south of the lane, door on the lane side.
Outside on its **east gable the overshot water wheel** (3.6 m), stopped; its **dry flume** comes in from the north on
trestles, over the lane, to the top of the wheel (the sluice board at the far end is shut). On dry land for now: it
moves into a real stream on the map later (your call). Inside: the wheel's axle runs through the wall; on it the
cams that lift **three tall pestles** standing in a guide frame over stone mortars set in the floor; a hand-turned
stone mill (quern) by the door; bales and sacks. Walk round the pestles: solid? Head room under the axle (~2.2 m)?

**Tell me (3c-1):**
1. **The district:** easy to find and walk? Too far from the spawn, or fine? (Next districts go west or south of it.)
2. **Brewery:** does it read as a big sake brewery? The two kura side by side with the gutter between: right, or
   should they be joined inside (a door through)? The press, the steamer, the tubs, the koji room: believable?
   Anything you can walk through?
3. **Sugidama:** right look (it is brown, autumn)? Big enough?
4. **Dyer:** the sunk vats: right look, and do they behave underfoot? The drying frames?
5. **Paper mill:** vat + mould, drying boards: right?
6. **Water mill:** wheel + flume look; the stamps; is a hand quern OK, or do you want a wheel-driven millstone
   (gear-driven mills in Japan are late 18th c. at the earliest, so I left it hand-turned)?
7. **Doors / gates / steps:** the kura doors (they slide inside), the koji double doors, the kerb step in the dyer,
   the loft stair; anything that sticks or opens into a prop.
8. **Loot:** on floors, hearths, the press box lid, the koji bed, shelves; nothing up high.
9. **Uneven ground:** the district is on a slight slope; any floor with grass poking through or a wall floating?
