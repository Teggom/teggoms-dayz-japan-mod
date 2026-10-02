# W3C2 setup notes: wave 3c-2, the rural / industrial trade sites (agent W3C2, 2026-10-02)

Written BEFORE modelling (PRODUCTION_PLAN "research first"). Scope: research/catalogue/KEEP_TRADES.md 18 (pottery), 19
(tile works), 20 (stonemason, folded into the quarry), 22 (salt works), 23 (charcoal), 24 (logging), 25 (quarry), 26
(lime), 27 (mine); PARTS_GAP_AUDIT TR18-TR27 + items 26 (site_shura), 37 (site_adit), 38-41 (the kiln family).
Not in scope: the bonito smokehouse (28) and anything fishing (PRODUCTION_PLAN "Fishing industry suite"); the ☆ items.

Sources: the project's research (`research/buildings/B_TRADE_INDUSTRY.md` = BT §5 / §11, `PARTS_GAP_AUDIT.md` = PGA,
`PLAYBOOK.md`), web pages read this run (generic searches, no personal data in any request):
- **[OME]** Ome city, "知っていますか。青梅と石灰石のおはなし" (city.ome.tokyo.jp): Nariki lime for Edo castle (1607); the
  Edo-period burn: limestone stacked in a pyramid over the brushwood fuel, lit at the "fire hole" near the top at
  Setsubun, ~10 days to burn out, once a year (late autumn to early spring); the quicklime slaked with water, sieved,
  packed in straw bales (tawara). Search summary (histrip.jp / buyo-gas.co.jp): the kiln a frame ~5 ken square.
- **[GYO]** ja.wikipedia "行徳塩田" (Gyotoku salt fields): agehama -> irihama in the early Edo period, irihama in use by
  the Genroku era (the 1703 quake / 1704 flood broke its embankment gates); Gyotoku's own method was the **sieve
  method (zaru-tori)**: sea water poured over the salty sand in sieve baskets to draw the brine (the Inland Sea used
  the fixed filter box, numai); **pans of crushed shell in the Edo period** (iron pans from 1882); fuel **pine needles
  and bamboo leaves**.
- **[NABK]** Nara National Research Institute blog "瓦窯の革命" (nabunken.go.jp, 2018): the flat tile kiln was used ~800
  years "until the **daruma kiln appeared in the Sengoku period**" -> the daruma kiln is IN for 1730 (BT's "[form
  uncertain for 1730]" resolved: the TYPE is in era; its exact proportions are GK).
- General craft / archaeology knowledge marked **(GK)**; museum survivors and Meiji photos give form only (PLAYBOOK §1).

Common rules: one storey + attic cap (G1-5); dead world "as it was left", autumn: every kiln cold and opened, the pans
dry, the fires out, the camps empty; loot lies out on floors and surfaces (no containers); D1 / D2 doors >= 1.00 x 2.00;
every object < ~15,000 faces; a site object carries its own ground mass where its real form needs a slope (below).

## The slope question (the test island is flat: the free ground falls 2-3 % to the south)
The climbing kiln, the quarry face, the mine adit and the timber slide want a hillside. **Choice: each of these site
objects carries its own honest ground mass** (an earth bank / rock knoll built into the object, its base sunk 0.30
into the terrain), so it reads right on flat ground today and, on the real map, the same object is set into a real
slope (only placement changes; the bank then sinks into the hill). The climbing kiln sits on its own stepped earth
bank (the kiln builders' practice where a slope was too shallow, GK); the quarry face is a rock outcrop with the cut
face; the adit goes into an earth-and-rock knoll; the slide ends at its landing (the run's lowest 12 m).

**FX7 (2026-10-02, Stephen's walk: the quarry / mine / kiln banks "look kind of like shit; no idea what they are"):**
the masses were all one warm beige (stone_cut / stone_field / ground_earth_bare, the sandy stand-in) and blobby forms
ending in a hard line on the flat island. Now real materials (research/materials/make_fx7_materials.py:
jp_m_stone_quarry_face, jp_m_stone_outcrop, jp_m_ground_earth_bank; two ASSUMED grey rock palette entries) and soil
slopes / feathered toes at the foot (ruralsite_parts.apron / hull_solid). **Rule for the real map: hillsides come
from the TERRAIN.** There these objects shrink to what is built or cut: the quarry to its cut face + benches set into
a terrain slope, the adit to its portal + the first metres of knoll, the kiln banks to the bank under the kiln; the
island's aprons and soil slopes are island-only and get dropped (or cut back) when the object is set into a hill.

---

## TR23 Charcoal kiln site (sumi-yaki ba) - SITE 1
- **Form (BT §11 kuro-zumi-gama; GK):** black charcoal from an earth dome kiln: an oval / round chamber dug into the
  slope, an earth-and-clay dome over it, a fire mouth (kuchi) at the front, the flue (entotsu) at the back foot rising as
  a short clay chimney; the wood stood upright inside, fired, then the mouth and flue were sealed to smother it. A roof
  of boards or thatch on posts (kama-yane) over the kiln kept the rain off (GK: usual on Japanese earth kilns). Beside
  it the burner's hut (BT "sumiyaki-goya": small hearth, straw mats, water jar, axe and saw), wood stacks of billets,
  charcoal in straw bales (sumi-dawara), rakes and long hoes.
- **Era test:** IN (black charcoal kilns are medieval and earlier; GK). White (binchō) charcoal = Kishū, not here.
- **Recorded choices:** chamber 2.70 across x 2.30 deep, 1.45 high inside; the dome's earth 0.45 thick, its outer
  foot 3.7 x 3.3 m, top 2.0 m; the fire mouth 0.55 x 0.70 at the front, half closed by its stones, opened (dead
  world: the last burn was taken out); the flue a clay chimney 0.30 sq to 2.3 m at the back foot. The kiln roof: a
  board gable on four posts, 2 x 2 ken, eave 2.60, open sides (a loot floor of packed earth round the kiln).
  The kiln chamber is NOT enterable (a 0.55 m mouth). Object `Land_JP_SumiGama`.
- **The hut:** reuse C2's west-type hut `hut_west_thatch` (earth floor, itado), furnished as the burner's hut
  (`Land_JP_Hut_West_Thatch_Sumiyaki`: mats, water jar, axe and saw on the wall, charcoal bales). Wood stacks + bales
  outside: existing props (jp_f_firewood_stack, jp_f_log_stack, jp_f_charcoal_bales3 / _burst / _bale).

## TR18 Pottery kiln site (yakimono-ba, noborigama) - SITE 2
- **Era test:** the multi-chamber climbing kiln (renbō-shiki noborigama) reached Mino / Seto from Karatsu c.1600-1610
  (Motoyashiki kiln, GK): **IN for Seto / Mino in 1730**. Tokoname adopted the noborigama only in 1834 (GK); in 1730
  Tokoname fired big single-chamber kilns (ōgama / anagama, BT "Old-style tunnel kiln works": merge with
  noborigama). **Choice: the Seto / Mino noborigama**; Tokoname flagged (its 1730 kiln is the tunnel kiln).
- **Form (BT §5; GK):** a firebox (ōguchi) at the foot, then a row of chambers stepping up the slope, each a vaulted
  room with a wide flat floor of sand, separated by walls with flame holes at their feet; side stoke holes (sama) on
  both sides; one loading door (dekuchi) per chamber on one side, walled up for a firing; a short flue at the top.
  Firewood: red pine. A workshop shed with a doma: kick wheel (keri-rokuro) and hand wheel, wedging board, clay
  settling tanks (suihi), glaze tubs, long drying planks on racks, kiln shelves and props, wares in straw.
- **Recorded choices:** firebox 1.3 m + **4 chambers** each 2.3 m along the slope x 2.9 m across (inside ~2.2 x 1.9,
  1.6 high at the crown), each step up 0.55 m (the bank rises 0 -> 2.5 m over ~11 m, ~13 deg); clay-and-brick shell
  (ceramic_earthenware outside, ash-glazed dark inside the openings); loading doors on the east side (three walled up,
  the lowest one open showing the ware stacks gone), stoke holes both sides with clay plugs; a 0.7 m flue box at the
  top. The kiln on its own earth bank (stone-kerbed). No kiln roof (cost; period images vary; flagged). Not
  enterable (the open loading door is 0.70 x 1.10, a look-in). Object `Land_JP_Noborigama`.
- **The work shed:** reuse W3B's earth-floor workshop `tr_ws_doma_itabuki` furnished as the potter
  (`Land_JP_Workshop_Doma_Itabuki_Toki`): the kick wheel, a wedging board with clay, wares drying on long planks,
  glaze tubs, finished wares in straw in the raised room. Yard: a light bamboo fence (yotsume) round the shed and the
  drying racks, gate by `pick_gate('yotsume', status='work', carts=True)` (an opening, 1.5 ken: the firewood carts).

## TR19 Tile works (kawara-ba) - SITE 3
- **Era test:** sangawara 1674; Edo's 1720 tile encouragement (BT): tile works booming in 1730: IN. The daruma kiln
  (updraught, two fire mouths) appeared in the Sengoku period [NABK]: IN.
- **Form (BT §5; GK):** wooden tile moulds (kata), a wire clay cutter, a slab-cutting frame, a burnishing spatula,
  drying sheds with racks of green tiles, the kiln, the onigawara carving table.
- **Recorded choices:** the daruma kiln as a squat oblong clay body 4.2 x 2.6 m, 2.1 m high, rounded shoulders, the
  firing chamber in the middle, a fire mouth at each end (0.50 x 0.60, arched), a loading door in one long side
  (walled up, the top course pulled down), three smoke holes in the crown; built of clay over tile-sherd courses (kit:
  the same clay vault + arch pieces as the climbing kiln = **the shared kiln kit**). Not enterable. Object
  `Land_JP_Kawara_Gama`. Two kilns are NOT built (one is the site; the second costs nothing to place later).
- **Sheds (reuse):** the moulding shed = W3B's tiled earth-floor workshop `tr_ws_doma_sangawara` furnished as the tile
  maker (`Land_JP_Workshop_Doma_Sangawara_Kawara`: mould bench, onigawara carving table, clay); the drying shed = C2's
  open board shed `shed_open_board` furnished with green-tile racks (`Land_JP_Shed_Open_Board_KawaraDry`).
  Yard: a board fence (itabei) with `pick_gate('itabei', status='work', carts=True)` (kido_ryo 1.5 ken: tile carts).

## TR26 Lime kiln (ishibai-yaki) - SITE 4
- **Era test / form [OME]:** Nariki (Ome) lime for Edo castle from 1607, burnt since 1590; the Edo burn = limestone in a
  pyramid over brushwood in a framed kiln ~5 ken square, lit at a fire hole near the top, ~10 days, once a year; the
  quicklime slaked, sieved, packed in straw bales. Akasaka (Mino) is the other named centre (BT; its kilns not read).
- **Recorded choices:** a dry-stone walled kiln pit (the "frame") built against its own earth bank: inside 3.0 x 3.0
  m (scaled from Nariki's ~9 m: one island-size kiln), walls 0.60 thick to 2.0 m, the bank up to the rim on the back
  and both sides (the charging side), a draw / fire hole 0.60 x 0.80 at the front foot; inside the burnt-out heap:
  white quicklime lumps and ash heaped to 1.1 m (the last burn not taken out). Not enterable. Object
  `Land_JP_Ishibai_Gama`. The "stone or earth shaft" of BT is the same thing at a smaller size.
- **The shed (reuse):** C2's open thatch shed `shed_open_thatch` furnished as the slaking + packing shed
  (`Land_JP_Shed_Open_Thatch_Ishibai`): lime in straw sacks (tawara_kamasu), sieves, the slaking tub, shovels.
  Outside: a limestone heap (new prop) and brushwood bundles.

## TR25 Quarry (ishiba) + TR20 stonemason folded in - SITE 5
- **Era test:** Izu andesite quarries supplied Edo castle in the early 17th c. (BT; uncertain how busy in 1730);
  Okazaki's stone craft (lanterns) Edo period (GK): IN as a working quarry.
- **Form (BT §5):** a quarry face on a hillside with a shed; wedge-hole rows (ya-ana), split blocks, wedges, sledges,
  a slide (shura) track, a tool-sharpening forge, the lord's carved mark on blocks.
- **Recorded choices:** a rock outcrop 11 x 6 m, 4.5 m high, its south side cut in two benches (2.0 m + 2.3 m) with
  sheer split faces; wedge-hole rows along the bench edges (dark slots 0.09 x 0.06, 0.25 apart, 2 mm proud on the face);
  a half-split block on the lower bench with its wedges in; rubble at the foot. Not enterable (solid rock).
  Object `Land_JP_Ishiba`. The shed (reuse) = C2's open board shed furnished as the quarrymen's shed with the
  sharpening forge (`Land_JP_Shed_Open_Board_Ishiku`: W2F forge + anvil, tool wall, wedges).
- **Stonemason folded in (cheap):** finished lanterns waiting by the shed = the existing jp_s_stone_lantern_* props
  (kasuga, toppled); cut blocks (new prop) + the stone sledge on rollers (new prop, the stone shura). No half-carved
  lantern model (cost).

## TR27 Mine site (kōzan) - SITE 6
- **Era test:** Izu gold (Toi, Yugashima) peaked in the early 17th c. [BT: "uncertain how active" in 1730]; Kai's gold
  likewise early; Hakone sulphur [uncertain whether worked in 1730]. **Choice: a small gold mine, worked out and left**
  (fits the dead world and the uncertainty: a played-out mine is honest either way). Flagged.
- **Form (BT §11):** adit mouth (mabu) with timber supports, shell oil lamps, picks and hammers, ore baskets, a drainage
  pump / troughs, ore-crushing stones and grinding mills, a women's sorting and washing shed with sluices, a smelting
  hut (not built: cost). Dressing per KEEP_TRADES: mine shrine (yama-no-kami), ore baskets, windlass, drainage troughs,
  spoil heaps.
- **The adit depth (recorded, as the brief asks):** a timbered portal and a **short dead-end gallery: 7.3 m (4 ken) of
  timbered drift, ending at a rockfall**. Clear section 1.30 wide x 2.10 high (game D1 / D2; real Edo drifts were
  often lower and narrower, GK: a deliberate game concession), timber sets (two posts + cap, tome-gi) every 1.0 m,
  lagging boards over the caps, an earth floor (walkable, a loot floor), a board drainage trough along the left foot
  running out of the mouth. The knoll: earth + rock masses round the drift, 9 x 9.5 m, 4.4 m high. The mine shrine:
  the kit's wooden hokora on a stone base beside the portal + a shimenawa over the portal cap. Object `Land_JP_Mabu`.
- **Sorting shed (reuse):** C2's open board shed furnished as the sorting shed (`Land_JP_Shed_Open_Board_Senko`):
  sorting table with hammers (new prop), the stone ore mill (existing jp_f_usu_ishiusu), ore baskets, the washing
  sluice trough (new prop).
- **Miners' bunk hall:** NEW shell (below), furnished `_Miners`. Outside: spoil heaps (new prop), the windlass over a
  small prospect shaft (new prop, a covered shaft), ore baskets.

## Bunk hall (KEEP_DWELLINGS 4: porters, logging crews, miners) - NEW shell, used by sites 6 + 7
- **Form (GK):** a long one-room hut: an earth-floor entrance doma with the hearth (kamado) and water jar, then a long
  raised board sleeping floor (0.40) down one side with an irori, the men's bedding rolled along the wall, pegs for
  clothes and tools. **Recorded:** 6 x 3 ken, board walls, earth doma 2 ken at one end (front door + back door), raised
  boards 4 ken x 3 ken with one irori, a window per 2 ken; eave 3.10; roof itabuki | ishioki (stone-weighted boards,
  the mountain roof). Classes `Land_JP_BunkHall_Itabuki`, `Land_JP_BunkHall_Ishioki`.

## TR24 Logging camp (soma-goya) - SITE 7
- **Form (BT §11 + §3):** fellers in state / domain forests; axes (primary), felling saws spreading in the Edo period,
  wedges, log chutes (**shura**) down a slope, a camp hut. Sawing: W3B learnt the Japanese sawyers used a raised trestle
  with the log propped at an angle, NOT a sawpit: **reuse W3B's furnished saw shed** (`Land_JP_Timber_SawShed_Furnished`,
  the trestle + log) as the camp's sawing place (no new model).
- **The shura (GK):** a chute of logs laid side by side lengthwise to form a trough, carried on log cribs / trestles
  across hollows, down which the logs slid (greased or wetted). **Recorded choices:** the slide's lowest 4 bays as a site
  object: 13.6 m long, 7 logs wide (the trough 0.75 wide, 0.30 deep), on cribs, falling from 2.4 m at its upper end to
  grade at the landing (~10 deg), a log stopped in it; the landing log stack below. Object `Land_JP_Shura` (= PGA 26
  jp_p_site_shura, also the part for a future stone slide).
- Camp: the bunk hall furnished `_Loggers` (ishioki variant), log stacks, axes.

## TR22 Salt works (enden) - SITE 8
- **Which type fits 1730 [GYO]:** Gyotoku was **irihama** (tidal, embanked) by the Genroku era; its brine was drawn by
  the **sieve method (zaru-tori)**, not the Inland Sea filter box; pans of **crushed shell** (iron only from 1882); fuel
  pine needles and bamboo leaves. Kira and Yui-Kanbara not checked separately (GK: irihama spread east through the
  17th-18th c.). **Choice: the Gyotoku irihama with zaru-tori and a shell pan.**
- **Placement (Stephen's water-mill rule):** the test island has no sea near the showcase: built on dry land, dead
  world (the bed dry, the ditches empty, the pan cold), so a later move to a real shore is only a placement change.
- **The salt bed (recorded):** one section of an irihama field: a levelled bed 12.7 x 7.3 m (7 x 4 ken) of raked sand,
  0.15 over grade, with its tidal ditch (hama-mizo, 0.60 wide, 0.35 deep, plank-lined, dry) along the sea side and one
  end, a low embankment (tsutsumi) beyond the ditch with a small timber sluice (shut, dry), sand raked into lines, two
  sand heaps scraped up; walkable (Roadway). The zaru-tori stands (sieve baskets on a frame over a tub) and the rakes are
  props on the bed. No sand material in the library: the bed uses the tamped-earth floor material (flagged: a sand
  material is a material job). Object `Land_JP_Enden`.
- **The boiling hut (kamaya), NEW shell:** 4 x 3 ken, board walls, earth floor, a long smoke vent (koshiyane) over
  the pan; the **shell pan (kai-gama)**: 2.4 x 1.8 m, 0.15 deep, shell-lime plaster (white-grey), on a clay firebox 0.55
  high with its fire mouth to the stoking side (shell geometry, like the dyer's vats); brine tubs, salt draining
  baskets (new prop), the fuel heap of pine needles + bamboo leaves (new prop), salt bags. A wide front doorway (carry
  in fuel) + a side door. Classes `Land_JP_Kamaya_Itabuki` (+ furnished).

---

## New site parts (the kiln kit = PGA 38-41 + 26 + 37), `parts/kit/jpparts/ruralsite_parts.py`
| PGA item | Built | Used by |
|---|---|---|
| 39 jp_p_site_kiln_dome | `_charcoal` (earth dome, mouth, flue) | SumiGama |
| 38 jp_p_site_kiln_climbing | `_4ch` (firebox + 4 chambers on the bank) | Noborigama |
| 41 jp_p_site_kiln_updraught | `_daruma` (two fire mouths) | Kawara_Gama |
| 40 jp_p_site_kiln_shaft | `_stone` (dry-stone pit kiln on its bank) | Ishibai_Gama |
| 37 jp_p_site_adit | `_timbered` (portal + 4-ken drift + knoll) | Mabu |
| 26 jp_p_site_shura | `_log4` (4 bays of log chute on cribs) | Shura |
Shared kit pieces: the clay vault (a barrel vault of convex segments), the arched fire mouth, the earth bank.

## New props (spikes/W3C2/props_w3c2.py, cat 'sitefit')
kick wheel; wedging board + clay; ware-drying plank rack; wares packed in straw; kiln furniture stack; green-tile
drying rack; tile stack; tile moulding bench + onigawara table; limestone heap; quarry blocks; stone sledge on
rollers; ore sorting table; washing sluice trough; spoil heap; windlass over a covered shaft; zaru-tori sieve stand;
salt draining baskets; pine-needle fuel heap. Each with an 'as left' / fallen state where it makes sense.

## Changes while building (recorded, W3C2)
- **Every site object carries a timber element on posts** (the shell checks C3 / C8 want real posts on stones; each is
  honest and useful): the charcoal and tile kilns stand under board roofs (kama-yane, GK), the climbing kiln and the
  lime kiln get a small stokers' / draw-floor roof on four posts over their work floor, the quarry a masons' shelter
  (2 x 1 ken), the adit's timber sets stand on sill stones, the slide on trestles, the salt bed's sluice on four posts.
- Charcoal kiln roof 3 x 3 ken (not 2 x 2): the loot floor round the dome needs room. Daruma kiln roof 3.5 x 2.5 ken.
- **The adit's clear width is 1.67 m** (not 1.30): the set posts stand on the half-ken grid (C3), 2 x 0.91 apart; clear
  height 2.15. Recorded as a game concession (real Edo drifts were narrower and lower).
- The climbing kiln's bank falls away behind its stack (on flat ground; on the map it runs into the hill); the lime
  kiln's bank is three mitred wedges (back + sides) meeting on the corner diagonals.
- Bunk hall roofs: itabuki (miners) 6.1k R1 (+2 %), ishioki (loggers) 8.3k R1 (+38 %) with every 2nd weighting stone
  kept in R1; both over_budget_ok with the reason recorded in the template.
- The salt pan is the shell pan [GYO] on a clay firebox built into the boiling hut's floor (shell geometry, interior
  clay: C14); the salt bed's ditch floor is 0.10 over grade (dry board floor; never at grade: gradesweep), its bed 0.30 over grade with a ramped
  landward edge.
- No sand material in the library: the salt bed and its heaps use the tamped-earth floor (material job, flagged).
- The pot hook over every new irori hangs from the real tie beam (the kit's irori hook point sits 6-9 cm under it in
  the C2 huts: hangcheck baseline; fixed in the W3C2 dressings, not in the old huts).
- Props fixed by FX6's propfloat before placing: ware-rack planks (missing), sledge rollers / runners seated, heap lumps
  sunk into the heap, sieve baskets on cross bars, fuel bundles lying, tile stack as flat plates.
- Placement: the island here falls 2-3 % to the south: the site objects are seated on their work floor (stoking floor,
  draw floor, adit mouth, splitting floor, landing) so their banks / knolls sink into the rising ground; huts and sheds
  float <= 0.13 on their low side (hidden by the 0.20 doma slab); the tile yard's fence sinks 0.40 on its high corner
  (its posts are footed to -0.40).
