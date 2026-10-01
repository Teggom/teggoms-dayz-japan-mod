# Japan test island: wave 2 walk, shrine + temples + civic (~32 min)

Phase C wave 2 is built and placed: 24 furnished buildings (W2F), on the shells W2P1 / W2P2 / W2C / W2S made, with 49
new props (offering boxes, bells, drums, name boards, altar daises with Buddhist images, temple bells, forges,
bellows, anvils, capture tools, two stone terraces). Nothing here has been seen in the engine yet. Pictures:
`research/production/contact_sheets/w2f_precinct.jpg`, `w2f_temple.jpg`, `w2f_civic.jpg`, `w2f_rooms.jpg`,
`w2f_props_*.jpg`.

**Start:**
1. Run `start-japan-test-island.bat` in the server folder. It starts only the test server, on its own port.
2. When the server is up, run `start-japan-test-client.bat` to join.
3. Labelled maps: `research/production/contact_sheets/w2f_map_precinct.jpg`, `w2f_map_village.jpg`,
   `w2f_map_east.jpg` (every ID in `spikes/SH1/SHOWCASE_MAP.md`, W2F section).

**If it won't load, kicks you, or something is invisible:** just tell me. I read the server and client logs myself.

**The route (~900 m):** spawn -> north up the shrine approach to the precinct -> west to the village temple by the
graveyard -> the village shrine above the hamlet -> the street's west end -> along the street to its east end (gate,
tea houses) -> the town temple -> back to the spawn.

**Everywhere, all walk long:** anything floating, see-through, flickering, or popping at a distance; every door you
pass (open AND close it, from both sides); loot on floors and on furniture tops. Shrines, altars and offerings carry
no loot on purpose (left undisturbed).

## FX1 re-check (~10 min; the fixes from your wave-2 walk). IDs: spikes/SH1/SHOWCASE_MAP.md (W2F section)

Before / after pictures: `research/production/contact_sheets/fx1_fixes.jpg`. Do these first, then the rest of the walk
below only if you want to.
1. **Door pulls** (P1 haiden ~1024, 1192; T1 village hondo ~972, 1123.5): open each door pair halfway. Pass: each
   leaf carries its own ring pull (on a small board on the lattice doors), on BOTH faces, near the middle; nothing
   floats or swaps leaves when they move. Also the kido K1 (1069, 1080): the iron straps sit at each leaf's hinge side.
2. **Offering boxes** (P1.s1 1021.8, 1187.2 on the terrace; V1.s1 943.2, 1066.1; T1.s1 969.3, 1117.8; T5.s1 965.9,
   1107.8; U1.s1 1097.8, 1106.1; U5.s1 1087.8, 1102.3): the box stands on the ground BESIDE the foot of the steps,
   no leaves on it, and you walk straight up the stair without touching it. The P terraces have no leaf drifts now.
3. **Hanging things**: the T3 village bell tower (984, 1112) and U3 town bell tower (1085.5, 1118.5): the striker log
   hangs under the bell beam on two ropes that end in the beam; the bell on its hook. The U1 gong and the P1 / V1 bell
   ropes (suzu) hang from a short bar between the porch tie beams (or across the rafters on T1 / U5). Pass:
   nothing hangs in the air with a gap above it.
4. **U1 town hondo (1100, 1112) veranda ends**: the railing turns the corner and runs back to the wall at both ends
   (also on V1, T1, T5, U5). Pass: no deck / railing that stops in mid air.
5. **Rope torii**: walk under the V3 village torii (945, 1061), the approach torii (1024, 1161), the row at x 1036
   (z 1145-1185) and the hill-stair torii (x 1042 / 1058). Pass: the rope and the paper streamers (shide) are clearly
   above your head (>= 2.35 m at the lowest tip, they were 1.4-2.1 m); the torii are bigger (shinmei 2.46 x 3.69 m).
6. **Woodpiles** (outside the houses, in the kitchens, the free-standing one): two stakes at each end of every pile,
   tied with a straw rope; the collapsed one has its stakes leaning out.
- Tell me: any floating / clipping where the boxes, bars or stakes meet the buildings; whether the bigger torii feel
  right; whether you want the fuller wrap-round veranda on U1 (costs ~850 faces over the 'large' budget).

## 1. The shrine precinct, town grade (10 min) — map w2f_map_precinct.jpg

From the spawn walk north through the street and up the approach (x 1024) past the torii and lanterns. The empty hall
site at its head now has the halls, each on a **stone terrace** (the ground rises ~1 m across the site; the terrace
back sinks into the slope).
- **P3 temizuya** (~1014, 1147, west of the approach): the curved tile roof on brackets, the stone basin inside, the
  ladle rack.
- **P4 shamusho** (~1011, 1165): the priests' office. Step up into the office: the amulet counter under the push-up
  shutter (talismans on it), the talisman desk, robes, the god shelf. Open the push-up shutter from inside.
- **P5 kagura stage** (~1011, 1188): kagura drum + flute, the costume chest, masks on the back wall. The stage stands
  on stilts and is seated on its lowest corner: its uphill (north) posts go ~0.5 m into the slope. **OK, or odd?**
- **P1t / P1 the town haiden** (~1024, 1192): climb the terrace's stone flight (9 steps) and the haiden's own stair
  (kizahashi, the railed steps). Look at the **curved bark roof, the bracket sets (kumimono), the step canopy (kohai),
  the railing with its bronze post caps (koran)**, the name board 八幡宮 over the worship bay, the bell with its
  faded red-and-white rope (visual only: walk through it). The **offering box** stands at the foot of the haiden stair,
  on the terrace (the en in front of the one door is too shallow for it).
  - The middle doors are **hinged lattice doors (tobira) that open inwards**: open and close them from both sides.
    **Do they swing the right way and close cleanly?** The side bays are fixed shitomi.
  - Inside: the drum on its stand, the offering table under the god shelf (sanbo, white flasks, dried sakaki), two
    candle stands, the ritual chest (loot on its lid), straw cushions, votive boards (ema) on both side walls.
- **P2t / P2 the town honden** (~1024, 1207), behind, on a higher terrace (12 steps): the **sealed sanctum**. Its three
  lattice doors do NOT open (by design). Look through the lattice: three shrine cabinets with a mirror and gohei.
  Walk the railed veranda round it (loot on the veranda only). The offering table before the doors.
- **The terraces:** do the flights walk smoothly (no stumble at the top or bottom)? Can you walk off the terrace
  sides? Any gap or floating edge where a terrace meets the slope?

## 2. The village temple, Jodo (5 min) — map w2f_map_village.jpg

West of the graveyard (~972, 1104-1124).
- **T4 gate (yakui-mon):** the hinged board gate leaves (open / close both). The name board over the tie beam is a
  blank weathered board (there is no temple-name text yet, flagged).
- **T1 hondo** (~972, 1123.5): the straight tile roof, the en and stair. The two front doors are **hinged (sankarado,
  open inwards)**, plus a side door at the back of the right-hand wall. Inside: the altar dais with **Amida in its zushi** (doors open), the
  canopy over it, the sutra desk with the bowl gong and a small mokugyo, candle stands, the vestment chest (loot).
  On the en: the donation box and the gong with its rope.
- **T3 bell tower** (~984, 1112): the **bell** (bonsho) hangs from the bell beam, the striker log on two ropes beside
  it. It has collision: walk round it. **Does the bell hang right on its beam (no gap, no poking through)?**
- **T2 kuri** (~955, 1122): the earth-floored kitchen with **two kamado and their pots**, shelves, firewood; step up
  into the board room with the irori (pot hook, persimmons), the meal-tray shelves, the account desk; the tatami
  guest room behind (chest, folded bedding, screen). The genkan porch door into the guest room.
- **T5 Jizo hall** (~962, 1109.5): the two lattice doors (hinged). Inside: **a standing Jizo with staff and red bib**
  on the dais; a stone Jizo (T8) outside.

## 3. The village shrine (2 min) — map w2f_map_village.jpg

North of the hamlet (~945, 1061-1080): **V3** shinmei torii with rope and streamers, two mossy lanterns, **V1** the
village haiden (straight board roof, hinged lattice doors, the drum, the offering table, the box at the stair foot)
and **V2** the nagare honden with chigi + katsuogi on the ridge (sealed, board doors).

## 4. The street's west end (5 min) — map w2f_map_village.jpg

- **K5 smithy** (~969.5, 1086, north side): open front. The **cold forge** (clay hearth, dead charcoal, the tuyere),
  the **box bellows** beside it, the **anvil** in its stump (tongs on the stump), the dry quench tub, a charcoal bale,
  half-emptied tool wall, a rack. Loot on the forge ledge, the bellows lid, the stump.
- **K6 swordsmith** (~967, 1072, south side): the work room (clay-coating trough with whetstones, the rack of bare
  blades, a work bench) and, through the inner door, the **dark forge room**: forge, the big bellows, the anvil, the
  long dry quench trough, **the straw rope with paper streamers over the forge**, the god shelf.
- **K7 jishin-ban guard house** (~977.5, 1072.5): the **fire ladder with its alarm bell on the ridge** (look from the
  street), the ward lantern by the door. Inside: the three capture tools on the wall rack, fire buckets, the brazier
  with a kettle, the sundries counter under the push-up shutter (candles).

## 5. The street's east end (5 min) — map w2f_map_east.jpg

- **K1 ward gate (kido) + keeper's hut** (~1069, 1080), across the street east of the last houses: **the first engine
  test of hinged gate leaves (rotation doors)**. Open and close the big pair from both sides; use the small wicket.
  **Do both leaves swing the right way, together, and close flush?** The ward lantern under the tie beam. The keeper's
  hut: the capture tools (one gone), the brazier, candles on the counter boards.
- **K2 tea house** (~1075.5, 1087): the kettle on its hearth, a bench with tea things, the raised room (brazier, tray
  meal, a tobacco tray knocked over). **K3** the bench tea house across the road, **K4** the tateba with its sake casks,
  the raised room and the tatami room behind its sliding doors.

## 6. The town temple, Zen (5 min) — map w2f_map_east.jpg

North-east (~1100, 1097-1118).
- **U4 gate (shikyaku-mon):** curved roof on brackets, hinged leaves.
- **U1 hondo:** the curved tile roof on degumi brackets, the copper step canopy. The middle **hinged doors** (open
  inwards). Inside: **Shaka** in the zushi, canopy, sutra desk, the **big red mokugyo**, the drum, the chest. The
  donation box at the stair foot, the gong on the en.
- **U2 kuri:** as the village one, plus the Zen **wooden fish board and cloud gong** hung by the kitchen door.
- **U3 bell tower** (hakama skirt, outside stair): climb to the deck. The town bell is big and fills much of the deck
  (the striker log at waist height). **Walkable, or in the way?**
- **U5 Kannon hall:** a standing Kannon with a halo on the dais.
- **From ~100 m away, look back at U3:** does the bell tower pop or change shape at distance?

## Tell me

1. **Shrine precinct:** the curved roofs, brackets, rails and stairs: right? The terraces: OK as a way to put halls on
   a slope? The sealed honden (lattice, cabinets inside): right?
2. **Hinged doors:** shrine / temple doors and the kido gate leaves: swing the right way, close from both sides? (If a
   leaf swings the wrong way, say which: the fix is one line.)
3. **Altars and bells:** the Buddhist images, the temple bells, the offering boxes, the shrine bell ropes: do they
   read right? Anything floating, clipping or see-through?
4. **Smithy / swordsmith / guard house:** do the forge set, the tools and the ridge ladder read right?
5. **Tea houses:** right? Want more on the benches?
6. **Loot:** found where you'd expect (floors, chest lids, counters, the forge ledge)? Nothing on the altars (on
   purpose)?
7. **The 'tower' budget class (open since W2P2):** the town bell tower's far model (Resolution 3) is 1,267 faces,
   over the 'standard' 800, so it is filed as 'large'. **Do you want a separate 'tower' face-budget class** for bell
   towers, drum towers, fire watchtowers and pagodas (proposal: 9,000 / 3,450 / 1,300), or keep them under 'large'?
8. **The kagura stage** half into the slope (P5): fine, or should it get a terrace too?
9. Anything else that looks wrong.
