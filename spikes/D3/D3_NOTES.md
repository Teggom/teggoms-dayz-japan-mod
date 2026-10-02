# D3 research notes: wave 3a dwellings + honjin (agent D3, 2026-10-01)

Research-first notes, one block per building: period form, plan, storeys (G1 A1 ruling 3: "whatever is historically
accurate", with a source), materials, the 1730 test, and what the kit can and can't do. No web access in this run:
sources are the project's research files (`research/buildings/BUILDING_LIST.md` = BL, `playbook/WORLD_CATALOGUE.md` =
WC, `playbook/refs_index.json` T-numbers, PLAYBOOK §1-§2) and general architectural-history knowledge, marked
**(GK)**. Survivors are mostly late Edo (PLAYBOOK §1 caution): they give proportion and material, not dates.

Common rules applied to all of them:
- **Storeys:** every shell in this wave is ONE storey (G1-5 cap; no source puts a full upper floor on any of these
  forms in 1730). Only loft / attic space under the roof (closed, not walkable).
- **Status features (PLAYBOOK §2.2, T48, T19, T29):** genkan with a shikidai step = samurai, honjin, and the headman
  "by permission" (BL nanushi entry); jōdan-no-ma = honjin (and the headman's "raised guest room ... by permission",
  BL); tokonoma + chigaidana (+ tsuke-shoin) = samurai and honjin only. **Commoner houses keep no tokonoma** (G1 A2,
  binding; PLAYBOOK §2.1's "tokonoma in merchant best rooms" is overridden by G1 A2): so the headman and the great
  merchant get none, even though BL lists a "formal zashiki with tokonoma" for the Kantō nanushi (that list is
  survivor-based: late Edo). Plastered nagaya-mon = samurai; boards for the headman (T29).
- **Roofs:** sangawara (1674+, T07) for samurai and town houses; hongawara is a status roof (temples, castles, the
  samurai elite, T10): used only on the large (karō) mansion. Thatch / stone-weighted boards for rural (T40: ishioki
  ~3.5 sun pitch, ~20°).
- **Floors:** tatami in the best rooms only at T2, everywhere in living rooms at T3 (PLAYBOOK §2.1, T01, T58); no
  tatami at T1 (mountain / coastal house living rooms are boards).

---

## DW08 Mountain board-roof house (Kiso / Hida itabuki ishi-oki no ie)
- **Form:** low-pitched kirizuma roof of split boards held by battens and river stones (ishioki, T40 ~20°), board
  walls, big smoke-blackened beams; doma along one end; Hida variant: an irori frame with a drying rack (hidana)
  hung above it (BL "Rural: mountain": Kiso + Hida entries; [Hida no Sato] open-air museum = survivor, late).
- **Plan (GK + BL):** doma (+ stable corner in some) / irori room (oe, boards) / back room (heya / nando) / front room
  (dei, boards; the T2 "best room" may have a few mats). BL: "doma + irori room + back room + loft".
- **Storeys:** one storey + a low storage loft (tsushi) in the roof (BL). Built: one storey, roof space closed
  (loft not modelled: the kit's loft floor is walkable-only in townhouses; noted for later).
- **1730:** stone-weighted board roofs are the old mountain form (in use long before and after); IN.
- **Kit:** rural.Shell + ishioki roof + koyagumi; hidana = new built-in rack under the tie beam (sooted wood).

## DW09 Coastal house (ryōshi no ie)
- **Form:** board or thatch, a big doma for nets; "doma + two board rooms" (BL "Rural: coast"); net store = a shed
  or lean-to by the house (KEEP_DWELLINGS 9: net store, salt kit). Coastal huts use board walls + ishioki
  (PARTS_GAP_AUDIT DW01 coastal note).
- **Storeys:** one (BL; GK).
- **1730:** IN (generic fishing-village form).
- **Kit:** rural.Shell; the net store as an open gable lean-to (rural._gable_leanto) with net racks (dressing).

## DW13 Street-front row (omote-nagaya): SKIPPED
- The C1 townhouse units already ARE the omote-nagaya row: party walls (wall_party), party roof ends, end / middle /
  corner units, 2-4 ken frontages, shop closures and Edo board / tile variants (registry C1_TOWNHOUSES, 69 shells).
  A rented street-front row differs from a row of owned machiya only by tenancy, which the dressing (S1 shop sets)
  carries. No new shell.

## DW14 Foot-soldier row (ashigaru nagaya / kumi-yashiki)
- **Form:** rows of units for a domain's foot soldiers, each with a tiny front garden and vegetable plot; unit = doma
  with kamado + one 6-mat and one 4.5-mat room (BL "Low-rank samurai"; [Hikone ashigaru houses survive, on the
  Nakasendō]). Hikone's survivors are detached or semi-detached small houses in a fenced plot; the row form is the Edo
  kumi-yashiki / domain nagaya (GK).
- **Storeys:** ONE storey (G1 A1 ruling 3, as researched: "ashigaru rows (kumi-yashiki): one storey").
- **Roof:** board (itabuki) common on cheap rows; tile in tiled castle towns (GK). Two variants.
- **Unit (built):** 2.5 ken frontage x 3 ken deep: doma 1 x 1.5 ken by the door (kamado spot), a 4.5-mat front room,
  a 7.5-mat back room (6 mats + a board strip in period plans; the kit lays 7.5 inakama mats), back window. Units
  separated by full-height party walls up to the roof.
- **Gate and fence:** the compound step (K3's wall kit: board fence / hedge + a simple gate).

## DW15 Small samurai house (dōshin / kachi / lower castle-town samurai)
- **Form:** small detached house, board fence, simple gate; rooms: small genkan WITHOUT shikidai (a recessed entrance),
  3-4 tatami rooms, kitchen doma, garden (BL "Lower samurai's house in a castle town"). Hatchōbori dōshin plots ~100
  tsubo (BL).
- **Storeys:** one (GK; BL).
- **Roof:** board or sangawara kirizuma (GK: Kakunodate / Hagi lower-samurai houses: board / thatch / tile all occur).
- **Status:** genkan = recessed entrance doma + entrance room, no porch, no shikidai (PARTS_GAP_AUDIT DW15 note).
  Tatami (samurai, T3 town). No tokonoma for this rank (GK: the dōshin house's best room is plain; kept plain to stay on
  the safe side of §2.2).

## DW16 East (Kantō) headman house (nanushi no ie)
- **Form:** big thatch (hipped), board gatehouse (nagaya-mon), formal entrance with shikidai and a raised guest room
  "by permission" for receiving officials; huge doma with stove bank, hiroma with irori, daidokoro, several tatami
  rooms, formal zashiki, kura behind (BL; WC [T29]; [Yoshino house, Edo-Tokyo Open-Air Museum: late]).
- **Storeys:** one (all Kantō minka of this class; GK).
- **Built:** the C2 Kantō hiroma plan enlarged to 8 x 5.5 ken under one hipped thatch with geya aisles; doma 3 ken with
  a kamado bank; hiroma (irori), dei, nando + a FORMAL zone at the far end: genkan doma (separate front door) ->
  shikidai board step -> genkan room (3 mats) -> zashiki (8 mats, raised guest room = +0.15 jōdan step "by permission").
  No tokonoma (G1 A2: commoner). The genkan sits inside the envelope under the thatch eave (a gabled porch would need a
  roof union the kit lacks; recessed shikidai genkan are period too, GK).

## DW17 Kinai headman house (shōya no ie)
- **Form:** thatch main roof with tiled lower roofs, white plaster, huge earth-floored kitchen with a row of stoves
  (kudo) (BL; [Yoshimura house, Habikino: early Edo, in window]). Yamato-mune takahe gables are the Kinai status look
  (C2 / FB2 notes).
- **Storeys:** one (Yoshimura house main building: one storey under a big thatch with tiled lower roofs; GK).
- **Built:** the C2 Kinai yotsuma-dori enlarged to 8 x 4 ken: niwa 3 ken with the kamado row, mise, daidokoro (irori),
  zashiki + tsugi-no-ma; shikidai genkan at the zashiki end under the tiled lower roof; plastered (shikkui) exterior
  walls (white plaster: the shōya marker); takahe yamato-mune gables. No tokonoma (G1 A2).

## DW18 Great merchant residence (ōdana no oku)
- **Form:** family quarters behind or beside a big shop; "plain outside, rich materials inside"; many tatami rooms,
  oku-zashiki on a garden, family altar room, tea room, several kura, servants' wing, kitchen with a big stove bank
  (BL "Urban merchant elite"; houses of this rank mostly lost).
- **Storeys:** one (G1-5; the shop front block, if any, keeps the zushi-nikai; the residence behind is one storey; GK).
- **Status:** commoner: no nageshi, no tsuke-shoin, no tokonoma (T48 1668 house rules + G1 A2); richness = size,
  tatami everywhere, the garden engawa, kura, good timber (PLAYBOOK §2.2).
- **Built:** a tiled (sangawara) 7 x 5 ken one-storey house: kitchen doma with a stove bank + board daidokoro, chanoma,
  butsuma (altar room), oku-zashiki + tsugi on the garden side with an engawa; ceilings in the tatami rooms. The kura
  is a separate existing shell (Land_JP_Kura_*) in the compound, linked by K3's covered corridor if it fits.

## DW19 Samurai mansion, three plot sizes (chūkyū bushi / hatamoto / karō yashiki)
- **Form:** plot with a roofed gate (yakui-mon or kabuki-mon; nagaya-mon for hatamoto / karō), front garden, main
  house, kura, maybe a stable; genkan with shikidai, formal zashiki with tokonoma and built-in desk (tsuke-shoin),
  family rooms, kitchen doma, maids' and servants' rooms (BL "Samurai"; WC [T29]; Hikone, Hagi, Kakunodate survivors,
  mixed dates).
- **Shoin style (GK):** the formal room (zashiki / shoin) with a tokonoma and staggered shelves (chigaidana) side by
  side on its end wall, the tsugi-no-ma before it, nageshi rail and a board ceiling: the shoin-zukuri reception
  sequence, fully formed by the early 17th c. (Kangaku-in 1600, Nijō Ninomaru 1626): IN for 1730 at samurai rank.
- **Storeys:** one (all three ranks; the big two-storey nagaya are the daimyo perimeter rows, DW20, not here; G1 A1-3).
- **Built:** S 7 x 4.5 ken, M 8 x 5 ken, L 9 x 5 ken (karō: bigger kitchen, a 15-mat zashiki; a 10-ken three-column
  plan ran past binarize's vertex limit, so the karō's further rooms belong in a wing linked by a corridor). Hongawara would be the karō's status roof, but the kit's
  straight-roof hongawara has no far-LOD field yet (C15 / C16 fail): all three are sangawara for now (a kit task). Genkan porch (kirizuma, two posts, cut-stone pad,
  the shikidai board step) on the gable end facing the gate; genkan room -> tsugi-no-ma -> zashiki (tokonoma +
  chigaidana; nageshi; board ceiling); family rooms + kitchen doma at the other end; engawa on the garden side.
  Kuge (court noble) houses use this shell with courtly dressing (KEEP_DWELLINGS 19).
- **Tsuke-shoin:** not built (an outward window bay needs a wall projection the kit doesn't have); noted.

## DW21 Tea hut (sōan chashitsu)
- **Form:** a small mat room with a sunken hearth (ro), a crawl-in door (nijiri-guchi), a prep room (mizuya), a
  tokonoma; earth (sabi) walls, shitaji-mado (unplastered lath windows), thatch or shingle (kokera) roof; outside a
  stone basin (tsukubai) and a waiting bench (BL "Tea hut"; GK: Taian 1582, Jo-an 1618: the sōan form is fixed
  long before 1730: IN).
- **Storeys:** one.
- **Tokonoma:** YES (the tea room's alcove is part of the type; this is not a commoner dwelling room).
- **Doors (KEEP / PARTS_GAP_AUDIT DW21, "D9"):** the nijiri-guchi is decorative (a static 0.66 x 0.72 m board door);
  a normal katabiki door into the mizuya is the way in.
- **Built:** 2.5 x 2 ken: a 4.5-mat room with the ro (0.42 m pit) and a tokonoma, a 1-ken board mizuya; thatch or
  kokera roof. Shitaji-mado as bamboo renji windows (the kit has no lath window; noted).

## DW23 Board storehouse (itagura)
- **Form:** rural, cheaper storehouse of boards, tier 1-2 (BL "Outbuildings"); raised on posts with rat guards
  (nezumi-gaeshi) where grain is kept (GK; PARTS_GAP_AUDIT DW23: stilts + rat guards).
- **Storeys:** one (+ sometimes a loft; not modelled).
- **Built:** 2 x 1.5 ken on stilts with rat guards (stilts kit), board walls, a wooden step, itabuki or sangawara.

## DW25 Stable (umaya / ushi-goya)
- **Form:** detached stable with manger, straw, harness; horse (east) or ox (west) (BL "Detached stable" / "Ox shed").
- **Built:** horse stable 3 x 2 ken, two stalls (stall _row2) + a tack corner, board walls, itabuki; ox shed 2 x 2 ken,
  thatch, one ox stall + fodder corner.

## DW27 Bath hut (furoba / yudono)
- **Form:** middle and upper rural homes had a tub bath in a small hut (BL); goemon (Kamigata, iron-bottomed) vs teppō
  (Edo, iron fire-pipe) tubs are from a late-Edo source (Morisada Mankō, BL "verify for 1730"): the TUB is a prop, so
  the shell stays neutral (a tub spot + a firing hole outside), a board washing floor (sunoko) and a smoke / steam
  vent.
- **Built:** 1.5 x 1 ken, board walls, board roof with a small koshiyane vent, sunoko floor, door.

## DW29 Gatehouse with rooms (nagaya-mon)
- **Form:** a long one-storey gatehouse with the gate passage in it and rooms either side: servants' rooms (chūgen-beya)
  and storage (BL); plaster walls (with namako lower walls) allowed for samurai; commoners (the headman) use boards
  (T29, PLAYBOOK §2.2). Black boards = official (jinya, bugyōsho).
- **Storeys:** one (+ attic); the two-storey nagaya are daimyo perimeter rows (G1 A1-3).
- **Built:** 7 x 2 ken: a 1.5-ken gate passage with hinged leaves (gates.gate_leaves) + a wicket, a raised servants'
  room on one side (door from the yard side), a storage / stable doma on the other. Samurai: plaster + namako, sangawara,
  barred mushiko-style windows to the street; headman: boards, itabuki / thatch.

## Honjin + waki-honjin (lords' inns, KEEP_TRADES 6)
- **Form:** official lodging of daimyo, court nobles and shogunal officials; the house of the station's leading family.
  Formal gate (yakui-mon or kabuki-mon) in a walled front; genkan with shikidai; a suite of tatami rooms ending in the
  jōdan-no-ma (raised room) with tokonoma, staggered shelves and built-in desk; attendants' rooms; the lord's bath and
  toilet; garden; large kitchen; a separate side entrance for the family (BL Lodging, from C §4.3; [T19, T57]; system
  from 1634-35, PLAYBOOK §1: IN). Waki-honjin: smaller, smaller jōdan room, no or smaller gate [T18].
- **Storeys:** one (the honjin survivors at Kusatsu (1635 founding, present buildings largely 19th c.) and Futagawa are
  one-storey formal blocks; GK).
- **Built (two linked blocks + the gate):** Honjin_Omote: the formal block (genkan porch with shikidai on the gable end
  -> genkan -> 2 attendants' rooms -> tsugi-no-ma -> jōdan-no-ma raised 0.15 with tokonoma + chigaidana, ceilings,
  engawa to the garden); Honjin_Oku: the family / kitchen block (big doma with the stove bank, daidokoro with the irori,
  family rooms, the family's own entrance). Linked by K3's covered corridor; the gate from K3's wall kit. Waki-honjin:
  one block with a smaller jōdan, its own kitchen doma, genkan with shikidai, NO gate (KEEP_TRADES 6).

## Compounds, corridors, placement (step 3, after K3)
- **Compounds** (`dw_site`, `Land_JP_Compound_*`, template `compound()` on K3's `sitewall`): samurai M (black board
  fence, the nagaya-mon fills the street side, kabuki back gate), Kanto headman (tall clipped hedge, hedge core is also
  Fire Geometry, nagaya-mon in front, back gate), honjin (plastered dobei street wall with the roofed kabuki-mon +
  board fence round sides / back + back gate), merchant (closed board fence, kabuki gate), kumi row (yotsume bamboo
  on the lane + gate), doshin (closed board fence + kabuki gate). K3's board-fence cap was too heavy (cap "none");
  the wickets were swapped for 1-ken kabuki gates (cleaner door checks). Each gate passage carries an earth floor at
  grade (loot + Roadway) and 3 stepping stones (C8 wants 4+ soseki-tagged pieces).
- **Corridors** (`Land_JP_Roka_Honjin`, `Land_JP_Roka_Temple_U`, template `roka()` on K3's `roka.run_roka`): the honjin
  watari-roka is half-walled, sangawara, floor 0.50 = both blocks' floor, connected both ends (connector_fit margin
  ~0.9 m at the omote, ~0.27 m at the oku). Stephen's proof at the town temple: U1 hondo east veranda (0.75) -> U2 kuri
  genkan porch, one level, itabuki, open on the garden side, a 0.70 m step off at the porch end (a stair there broke
  the connector fit; flagged in the checklist).
- **Kairo at shrine P:** not built (the precinct terraces leave no level run between the halls; K3's kairo kit is
  ready if wanted).
- **DW13** skipped (the townhouse units cover it, per the brief); **DW20** waits.
- **Placement** (`spikes/D3/layout_d3.py` -> test/placements/D3.csv, test/ce/D3_mapgrouppos.xml; map
  `map_d3.py` -> d3_map.jpg + SHOWCASE_MAP.md D3): samurai quarter S (row, two doshin, mansion + nagaya-mon + kura)
  south-west of the yard; Kanto headman H west by the hamlet; honjin J + waki-honjin south of the street's east end
  (honjin moved east of SH1's fire-watch rack); merchant M north of the Edo row with tea hut + kura; Kinai headman +
  coastal house south-east (no sea near the yard, so the coastal house is on dry land), mountain house east of the
  street (the north slope is too steep for its plan). 29 buildings, 43 rows, 29 CE groups; layout checks 0 problems;
  verify_oprw PASS 4178/4178. The one placecheck flag (M3.s1 kasuga lantern "hanging") is the classifier calling
  every kasuga lantern on the island "hanging" (19 rows across SH1 / W2F / FX2 too), not a real float.
