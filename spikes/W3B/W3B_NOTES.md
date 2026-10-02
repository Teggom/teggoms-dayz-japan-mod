# W3B research notes: wave 3b everyday workshops + services (agent W3B, 2026-10-02)

Research-first notes per building: period form, plan, sources, the 1730 test, and what the kit does. No web access in
this run: sources are the project's research files (`research/buildings/B_TRADE_INDUSTRY.md` = BT, `BUILDING_LIST.md`
= BL, `playbook/WORLD_CATALOGUE.md` = WC with its T-numbers, `PLAYBOOK.md` §1 / §5 / §12) and general
architectural / craft-history knowledge, marked **(GK)**. Survivors and Hokusai / Hiroshige prints are late (1800s):
they give form and proportion, not dates (PLAYBOOK §1 caution).

Common rules applied to all of them:
- **One storey** (G1-5 cap). The sentō's men's upstairs rest room (BT 9a, WC T27) is the one period two-storey case
  here: NOT built (G1-5; PARTS_GAP_AUDIT §6 item 13 lists it as a ruling Stephen has not made). Flagged.
- **D9 (PLAYBOOK §5):** a tiny doorway (the zakuro-guchi) is decorative; the room always has a normal door too.
- **D1 / D2:** every passable door >= 1.00 m wide, head >= 2.00 m.
- **Roofs:** itabuki (boards) for the cheap / rural / edge-of-town versions, sangawara (1674+, T07) for the town
  versions; no hongawara (status roof). Earth walls over a board skirt (koshiita) for the fire trades (sentō boiler,
  foundry) as the smithy (W2C); boards for sheds and stables.
- **Dead world, autumn:** everything cold and dry (boiler out, tub drained or scummed, furnace cold, horses gone).

---

## TR08 Public bathhouse (sentō / yuya)
- **Form (BT 9a, BL, WC T27):** by 1730 the usual town bathhouse is a shallow hot-water bath behind a low gabled
  partition, the **zakuro-guchi** ("pomegranate door": a pun, GK: mirrors were polished with pomegranate vinegar,
  "kagami-iru", and bathers had to stoop in, also "kagami-iru"), which held in the steam: bathers stooped under it into a dim bath room. Street
  entrance with a noren; a raised pay stand (**bandai**) with the cashbox at the step-up; a changing area (datsuiba)
  with shelves or baskets for clothes; a board washing floor (**nagashi**) that drains; small wooden buckets; behind,
  the boiler room (**kama-ba**) with a big cauldron fired with demolition timber.
- **Dates:** the first Edo bathhouse 1591 (Ise Yoichi, WC T27; BT). The earliest town baths were steam baths
  (mushi-buro / todana-buro); the zakuro-guchi type with a shallow tub is the 17th-century development (GK: Kan'ei to
  Kanbun, 1620s-1670s) and lasted until the 1870s, when the Meiji authorities banned it for hygiene (GK). So in 1730
  it is the standard form: **IN**.
- **Mixed bathing:** common in 1730 (BT: "mixed bathing was common"); the first bans came with the Kansei reforms
  (1791, GK) and were repeated without much effect. So ONE bath, no men's / women's split: the shell has one changing
  room and one bath room. (A split bathhouse would be post-1791 Edo.)
- **Yuna:** the bath attendant women of the earlier "yuna-buro" were banned in Edo in 1657 (BT): no yuna dressing.
- **Bandai:** the raised attendant's seat is attested for Edo bathhouses (GK; the classic descriptions are
  late-Edo, e.g. Morisada Mankō 1837-53): kept as a simple pay counter at the step-up, not the tall late-Edo stand.
- **Upstairs rest room:** not built (above).
- **The sign:** Edo bathhouses hung a bow-and-arrow sign (yumi-iru = yu-iru, "go into the hot water", GK; date
  uncertain) or simply a noren with 湯. No atlas cell for it: a plain noren + a hanging lantern (flagged).
- **Built (kit, GK proportions):** W 6 x D 3 ken, the long side on the street. Left to right: entrance doma 1.5 ken
  (front door, noren, the bandai at the step-up, the geta shelf) | changing room + washing floor 3 ken (one raised
  board room, 0.40; the nagashi = a slatted drain board prop on the bath side) | the zakuro-guchi partition | the
  bath room 1.5 ken (boards, dim: one high vent window; the yubune tub = a prop against the end wall) | the kama-ba
  outside the end wall as a woodshed lean-to (earth floor, open) where the boiler's fire mouth comes through the
  wall. A koshiyane steam vent over the bath room. Earth walls over a board skirt. Variants: sangawara (town) /
  itabuki.
- **The zakuro-guchi (D9):** a low gabled opening, 0.91 wide x 0.95 m high over the floor, under a small painted
  gable with a decorated board (vermilion + black lacquer frame: the period ones were painted, GK) in the partition's
  middle bay; a normal katabiki board door at the partition's front end is the way in.

## TR09 Stable yard (post horses, packhorse carriers, horse dealers)
- **Form (BT 9c "Commercial stable and horse dealer", "Packhorse carrier"):** a stable building plus a yard. Stalls
  with a manger (kaiba-oke), tie rails (uma-tsunagi), a fodder cutter (magusa-kiri), straw and hay stacks, pack
  saddles (ni-gura) and riding saddles, **straw horseshoes (uma-waraji)**: Japanese horses were not iron-shod; a
  water trough, harness hooks, a ledger. Post-station horses (tenma, quotas from 1638, PLAYBOOK §1 [T20]) were kept
  by the town's horse households and the toiya; the commercial carriers (chūma, Shinano) ran their own stables.
- **1730:** all IN (tenma system 1638; chūma carriers busy by the 18th c., lawsuits 1760s, BT).
- **Built:** the stable row: W 5 x D 2.5 ken: four stalls in a row along the back wall (2 x the kit's jp_p_frame_stall
  _row2: 1 ken a horse, 1.5 ken deep, bars down = as left), the stall fronts on an earth aisle open to the yard
  (posts + head beam, no wall: the horses are led straight in), and at the end a groom's room (raised boards, door
  + window) with the tack. Variants: itabuki (post town) / thatch (country carrier). The yard: a K3 board fence with a
  wide kabuki gate (a compound object), the troughs, tie posts, saddle rack and straw stacks as site props.

## TR02 Stall kit (food stall, market stall, barber booth, fortune-teller, show booth)
- **Already props (B3b / L2, reused):** the roofed food stall `jp_s_stall_yatai` (soba and dumpling stalls: Edo
  yatai multiplied after the 1657 fire; nihachi soba by the 1720s-30s, GK; tempura stalls are cut, KEEP_TRADES), the
  reed-screen stall `jp_s_stall_reed`, the plank booth `jp_s_stall_booth`, the market row `jp_s_stall_row3`
  (BT 10 "Market stalls": straw mats, trestle boards, small roofs, baskets, scales).
- **Fortune-teller (eki-sha, BT 9d):** "a street booth or table with a lantern, divination sticks (zeichiku) in a
  cylinder, counting rods (sangi), a book": a PROP (a small table set), placed by a stall row.
- **Barber (kamiyui-doko, BT 9a):** three forms: town shop, booth at a bridge or crossroads (de-doko), itinerant. The
  booth: a small board hut with an open front, a raised floor where customers wait, razors, combs, pomade, paper
  cord, a water basin + hot water, a small mirror, whetstone and strop, the customer's low stool, a tobacco tray, a go
  or shōgi board. **A SHELL** (enterable, 2 x 1.5 ken: earth front where the barber works, a raised board bench at the
  back for the waiting customers) + a barber's kit prop (the bin-darai box with basin and drawers).
- **Show booth (misemono-goya, BT 9d):** "temporary booths for animals, acrobats and curiosities at temple fairs ...
  a painted signboard, a curtain, benches"; famous at Ryōgoku Hirokōji after the 1659 bridge (GK). Temporary: poles,
  straw-mat (mushiro) walls, a board roof. **A SHELL** (3 x 2.5 ken: a curtained entrance, benches on an earth floor,
  a low board stage at the back). No painted-picture atlas cell exists: the signboard carries the shop text atlas's
  plainest board + banners (nobori) (flagged: a painted kanban-e cell would be a material job).
- **1730:** all IN.

## TR13 Earth-floor workshop (doma workshop)
- **Form (BT 3 + KEEP_TRADES 13):** a town workshop with the work done on the earth floor: joinery (tategu-shi:
  "doma for planing, raised for assembly": long planes, groove planes, fine saws, chisels, frames leaning on the wall),
  the abacus maker (Ōtsu; "beads turned on a small lathe, bamboo rods, frames"), the woodturner (Hakone; the lathe),
  the bamboo + basket maker (Arima, Minakuchi: "bamboo poles, splitting knife, sizing knives, soaking tub,
  half-woven baskets, finished baskets hung outside").
- **The planing beam (GK):** Japanese planes are pulled; long work lies on an inclined planing beam (kezuri-dai) or on
  sawhorses (uma, BT). **The lathe (GK):** the period woodturner's lathe (rokuro) is the strap lathe: a horizontal
  spindle between two posts, turned back and forth by a helper pulling a cord / strap (te-biki rokuro) while the
  turner, seated, holds the long tool; the treadle and the continuous belt lathe come later (GK). Built as such.
- **Built:** W 3 x D 2.5 ken: an earth work floor 2 ken wide, open front with two bays (the shutters taken in by day),
  and a raised board room 1 ken wide at the end (finished goods, the master's desk) with its kamachi; a back door.
  Variants: itabuki / sangawara. Three furnished dressings: joinery, woodturner + abacus maker, bamboo + baskets.
- **1730:** IN (all trades attested earlier; Ōtsu abacus from the early 17th c., GK).

## TR14 Raised-floor bench workshop
- **Form (BT 1 + 6):** the crafts done SITTING on a raised floor: sword polisher (togishi: "a sloping stone-holder
  (togi-dai) on a small stool, a set of whetstones from coarse to fine, water tubs, finger stones, paper and cloth, a
  blade stand"), sword-fittings maker ("small charcoal forge, chasing hammers and punches, a pitch bowl (yani-dai),
  files, gravers, small crucibles, a patination pot, finished tsuba on a board"), the lacquerer ("raised floor, kept
  dust-free. Items: a humid drying cupboard (urushi-buro), spatulas, human-hair brushes, lacquer pots, whetstones and
  charcoal, a turning stand, wares drying on racks").
- **The dust-free room (GK):** lacquer is coated in a closed back room (nurima) away from the street dust, the wares go
  into the furo (a wooden cupboard kept humid with wet cloths) to cure.
- **Built:** W 3 x D 3 ken: a front entrance doma (1 ken, the full depth of the front half), the work room (raised
  boards, 2 x 1.5 ken) lit by a wide lattice window on the front, and behind it a closed back room (2 x 1.5 ken,
  boards, one high window, a katabiki door) = the dust-free coating room; a back door from the doma. Variants:
  itabuki / sangawara. Dressings: sword polisher, lacquerer, metal bench (fittings maker).
- **1730:** IN.

## TR15 Timber yard (sawpit, log stacks, shingle splitting)
- **Sawing (BT 3 "Sawyer's shed"):** "a log propped high on trestles at an angle, maebiki-ōga saws, wedges, ink line,
  finished plank stacks, sawdust". **No pit:** Japanese sawyers (kobiki) did not use the European sawpit; the log is
  raised on a tall trestle at an angle and ripped with the one-man maebiki-ōga (the frame saw oga of the 15th-16th c.
  had given way to it in the Edo period, GK; Hokusai's Tōtōmi-sanchū shows the method, 1830s print, form only). So
  the brief's "sawpit frame" is built as the **sawing trestle with the log**, under an open shed.
- **Timber yard (BT "Lumber dealer and timber yard (zaimoku-ya, kiba)"):** "log pond, standing timber racks
  (tate-kake), stacked planks under roofs, log hooks (tobi-guchi), rafts, tally boards, the dealer's mark branded on
  log ends" (Fukagawa Kiba from 1701). No pond on the dry test yard (a site note: log ponds go on the map's rivers).
- **Shingles (BT "Shingle splitter"):** "splits cedar or sawara into thin shingles ... froe (hegi-nata), splitting
  block, bundles of shingles, bamboo nails, cypress bark bundles".
- **Built (three open sheds + the yard):** the sawing shed (3 x 2 ken, board roof on posts, open on three sides),
  the timber store (4 x 1.5 ken, a back wall where the timber stands upright, open front), the shingle shed (2 x 1.5
  ken, walled on three sides); a board-fence compound with a wide gate; log stacks, the standing rack, plank stacks,
  the sawing trestle + log, shingle bundles, the splitting block as props.
- **1730:** IN.

## TR12 Foundry (imoji: Kuwana cast iron; pots, kettles; bells as a site kit)
- **Form (BT 1 "Caster of pots and kettles (imoji)"):** "town workshop or edge-of-town site; doma, casting pit. Items:
  a cupola or crucible furnace (**koshiki-ro**), foot-operated bellows (**fumi-fuigo**), clay moulds (imono-gata) in
  parts, crucibles, ladles, a sand floor, scrap iron, cooling rack of new pots". Kuwana's casting trade is an early-Edo
  domain industry (Honda Tadakatsu's founding of the casters' quarter is the usual story, GK); Takaoka (from 1611) and
  Kyoto's kettle makers are the other period centres (BT).
- **The furnace (verified against BT + GK):** the koshiki-ro is the Japanese cupola: a short shaft of stacked
  fire-clay rings (koshiki) on a base, charged from the top with charcoal and scrap / pig iron, blown at the bottom
  through a clay tuyere by **treadle bellows**; the molten iron is tapped into a clay-lined ladle (tori-be) and poured
  into the moulds on the sand floor. It is NOT the tatara (the bloomery smelting iron from iron sand, a separate
  rural ironworks, KEEP_TRADES "Moved: tatara ironworks (off-map, cut)"). The treadle bellows (fumi-fuigo, a seesaw
  board worked by several men standing on it) is the period form (the balance-board tenbin-fuigo is a 1690s
  improvement for the tatara, GK): built as a treadle bellows box with its board.
- **Kettles:** the side-spouted iron kettle (tetsubin) is mid-18th c. on, uncertain (BT): NOT made here; the goods are
  pots (nabe), rice kettles (kama) and tea-ceremony kettles (chagama).
- **Bells (BT "Bell caster, on site"):** "temple bells were usually cast at a temporary casting site near the temple
  ... a dug casting pit, a clay mould built up in the pit, a ring of furnaces and foot-bellows, a thatched shelter,
  fuel stacks": a SITE KIT (props): the bell mould in its pit, built beside the foundry yard as a demo.
- **Built:** W 4 x D 3 ken, eave 3.80 (the furnace stack under a 2-ken koshiyane), two open front bays, earth walls
  over a board skirt, sooted koyagumi; the furnace + bellows at the back, the casting floor (sand) in front of it, a
  storage corner with scrap and charcoal. Variants: itabuki / sangawara; a board-fence yard (compound).
- **1730:** IN.

## TR10 Hot-spring bath hut (if cheap)
- **Form (KEEP_TRADES 10, WC "Onsen town inn"):** the communal spring (soto-yu): a roofed pool, walls low or none; the
  open-air rock pool is mostly modern (WC note). Built if time allows: an open shed roof over a stone-lined pool prop.

## Props (built WITH the shells; reuse first)
Reused (no new model): forge / fuigo / anvil (W2F) are the SMITHY's; the foundry needs its own furnace and bellows.
Reused as they are: manger_trough / manger_straw / manger_cutter, stable_yard_saddle_rack / tie_post /
trough_stone, straw_stack_*, oke_* buckets and tubs, tana shelves, basket_*, kori, urushiburo (S1: the lacquer drying
cupboard), sg_lacquer goods, rack_*, zukue desks, charcoal_*, firewood_*, kama / kama_nabe pots, stall_*, bench_*,
nobori, noren, chochin, hibachi, tabakobon, goban.
New (each with an abandoned / "as left" state where it makes sense): yubune tub (+ drained), bath boiler mouth,
bath stools, bandai pay stand, nagashi drain board, clothes-basket shelf; tack wall (straw horseshoes, bridles);
fortune-teller's table, barber's kit; planing beam, sawhorse pair, joiner's tool chest, strap lathe, abacus work tray,
bamboo stock + half-woven basket; polisher's stand, lacquer brush tray, fittings maker's bench; sawing trestle + log
+ maebiki-ōga, log stack, standing timber rack, plank stack, shingle bundles + splitting block; koshiki-ro furnace,
treadle bellows, mould set, ladle rack, cast-pot pile, scrap heap, bell mould in its pit.
