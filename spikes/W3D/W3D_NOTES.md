# W3D setup notes: wave 3d, the government buildings (agent W3D, 2026-10-02)

Written BEFORE modelling (PRODUCTION_PLAN "research first"). Scope: research/catalogue/KEEP_CIVIC.md "Government" 2
(official compound), 3 (open-front office with yard), 4 (highway checkpoint kit), 5 (jail compound), 8 (fire
watchtower, tall + the fire brigade station), the wooden palisade of the wall kit; execution grounds only if usage
allows. Already built and REUSED, not rebuilt: the guard huts (Land_JP_Guardhut_*), the ward gate kido, the notice
board (jp_s_kosatsu_*), the fire-watch ladder (Land_JP_S_Fire_Watch_Ladder_Tower), the jishin-ban (guardhut M).
Not in scope: castle (3e), fishing, the ☆ items (rice storehouse row, courier relay post, ward meeting house).

Sources (generic web searches, no personal data in any request):
- **[HAK-WP]** ja.wikipedia "箱根関": built 1619, abolished 1869; the 1865 repair report 『相州御関所御修復出来形帳』
  (found 1983) is the basis of the 2004 / 2007 reconstruction; the Tōkaidō ran through the middle between the
  mountain and Lake Ashi; the **two gates ~18 m apart**; ōbansho + upper guards' rest house, the facing guardhouse
  with the cells, notice-board place, stables, **a wooden palisade round the whole**.
- **[HAK-V]** kusanomido.com visit report of the reconstruction: roofs of thin split cedar shingles, buildings
  **black (shibusumi-painted)**; the ōbansho = the men-bansho with the officials' platform facing the road, a board
  room with a hearth, bath, kitchen doma; the ashigaru-bansho the second-largest building (guards' control room +
  sleeping); the Kyōguchi gate a **kōrai-mon, 6.1 m high**; **sasumata, tsukubō, sodegarami** displayed by the
  guardhouse with six-shaku staffs; the jail (gokuya) "sturdily built"; a two-storey lookout (tōmi-bansho).
- **[ARAI-WP]** ja.wikipedia "新居関": the surviving men-bansho **rebuilt 1855** (irimoya, hongawara), its street
  front in three rooms (jō-no-ma, naka-no-ma, tsugi-no-ma) for the officials, the shoin and the office behind; the
  checkpoint moved 1699 and 1707-08 (Hōei tsunami).
- **[TAK-WP]** ja.wikipedia "高山陣屋": shogunal from 1692; the earthen kura built c.1600 at Takayama castle, moved
  here in 1695; **genkan, ginmi-sho (court room), offices and the great hall rebuilt in 1816**; all roofs boards
  (kokera / stone-weighted) for Hida's snow and timber.
- **[KB-HNM]** kotobank "火の見櫓": shogunal brigade towers **3 jō (~9 m)**, open on four sides, plain wood; daimyo
  and town towers **black and lower**; two watchmen; shogunal brigades a drum, daimyo a board (hangi), **towns the
  hanshō bell**; **Kyōhō period (1716-36): one tower per ~10 chō**, elsewhere a fire ladder on the jishin-ban roof.
  Search summary (sayama city fire history PDF, rekishikaido): the machi-bikeshi organised by Ōoka 1718-1720.
- **[WP-MATOI]** ja.wikipedia "纏": **April 1720 (Kyōhō 5) Ōoka gave the machi-bikeshi matoi**; "at that time the matoi
  was a banner type called **matoi-nobori**"; the baren (streamer) form developed gradually (the black lines in all
  baren only after 1872).
- **[TOIYA-S]** search summaries (imidas "問屋場", historist): the toiya-ba relayed official porters and horses;
  staffed by the toiya, toshiyori, chōtsuke (clerks), umazashi / hitozashi; **the office (chōba) a raised floor
  (koshi-daka)**, **scales for checking loads**, **stables and the porters' room at the back**.
- Project research: research/buildings/C_CIVIC_RELIGIOUS_LAYOUT.md §4.1 (machi-bugyōsho / jinya: nagaya-mon, genkan,
  offices, **oshirasu = white gravel below stepped floor levels: commoners on a straw mat on the gravel, samurai on the
  veranda, the official on the tatami above**), §4.3 (sekisho, toiya-ba, kanme-aratame-sho), §4.5 (jail: double timber
  lattice cells, a provincial lock-up = a small lattice-fronted board building with 2-4 cells), §4.6 (fire towers,
  brigades: **no hand pump in 1730**), the official prop list (three capture tools, desks, ledgers, scales, masu).
- **(GK)** = general knowledge; reconstructions and post-1730 survivors give form only (PLAYBOOK §1).

**Post-1730 evidence flagged:** Hakone's buildings are reconstructed from an **1865** report; Arai's surviving
men-bansho is **1855**; Takayama's court room / offices are **1816**. The arrangement each shows (officials raised over
a gravel court, black boarded guardhouses, the kōrai-mon, the palisade) is older than its building (Hakone 1619,
Takayama jinya 1692), so the FORMS pass the 1730 test; exact proportions are from these later buildings.

Common rules: one storey + attic cap; dead world "as it was left", autumn: offices abandoned, ledgers spilled, the
cells empty and open (no bodies, no gore); loot lies out on floors and surfaces; D1 / D2 doors >= 1.00 x 2.00; every
object < ~15,000 faces.

---

## Site 1: highway checkpoint kit (sekisho), one generic instance
- **Era test:** IN (Hakone 1619, Arai 1600, Usui / Kiso-Fukushima early 17th c.; "guns in, women out" in force 1730).
- **The palisade (saku), NEW wall-kit kind** (KEEP_CIVIC walls: "sharpened timber fence"; [HAK-WP] palisade round
  the whole): round logs Ø ~0.15 set close (0.22 centres) into the ground (footing -0.40), standing 2.40 with the tops
  cut to a point, two horizontal rails (nuki, 0.07 x 0.10) on the inside face at 0.55 and 1.85. Half-ken modules like
  every wall kind; collision = one slab per module (no gaps a player fits through). `sitewall.wall("saku", ...)`.
- **The gates: kōrai-mon, NEW status gate kind `koraimon`** (sources demand it: Hakone's Kyōguchi gate is a kōrai-mon
  [HAK-V]; the form dates from the 1590s castle gates, GK: IN). Form: two main posts with the kabuki beam and a small
  gable roof over the gate line (the K3 roofed kabuki-mon), plus two rear posts (hikae-bashira) set back behind the
  main posts, tied to them at 2.6 m, each pair under its own small gable roof at right angles: the leaves swing 90 deg
  in and stand under the rear roofs. **Span 2 ken** (clear ~3.4 m: a highway gate for horses, palanquins and pack
  trains; Hakone's is far taller, 6.1 m: ours keeps the kit's beam at 2.91-3.15 so it matches the palisade, a game
  scale choice). **pick_gate row:** fence `saku` + status high + role front -> `koraimon` 2 ken; anything else in a
  palisade -> `kido_ryo` 1 ken. Both checkpoint gates are "front" (the Edo-side and the Kyoto-side gate).
- **The compound (`Land_JP_Compound_Sekisho`):** a palisaded rectangle 13 x 13 ken (23.7 m) with the road through
  the middle east-west, a kōrai-mon in the east line (Edo side) and the west line (Kyoto side) (Hakone's are 18 m
  apart: ours 23.7). North of the road the guardhouse with its **gravel court** (a pale stone pad 0.10 over grade in
  front of the inspection room where travellers knelt); south of the road the foot-soldiers' guardhouse.
- **The guardhouse with the inspection room (ōbansho), NEW shell `Land_JP_Bansho_Sekisho`:** W 5 x D 3 ken, board
  walls stained black (wood_kuro, [HAK-V]), board roof (itabuki for the cedar shingles), kirizuma. Front (to the road)
  open over 3.5 ken: **the inspection room**: a board veranda (engawa) 0.5 ken deep at 0.45 and behind it the
  officials' tatami floor at 0.60 (2 ken deep) **= the stepped floor levels facing the gravel court** (Arai's three
  street rooms are one long room here, cost); a kutsunugi step from the gravel up to the veranda; behind a partition
  (sliding doors) the back office (boards, 0.5 ken deep shelf wall for the pass ledgers). The right 1.5 ken bay full
  depth: the kitchen doma (earth, kamado) with its own front door and a back door. Fittings: the weapon-rack spot in
  front on the gravel, the desks on the tatami.
- **The foot-soldiers' guardhouse (ashigaru-bansho):** REUSE W3C2's bunk hall (Land_JP_BunkHall_Itabuki) furnished as
  `Land_JP_BunkHall_Itabuki_Ashigaru` (bedding, staff rack, the capture tools on the wall, lanterns, a brazier):
  [HAK-V] "control room + sleeping quarters", the second-largest building. Honest at this size.
- **Weapon racks:** existing `jp_f_mitsudogu` (wall rack, W2F) inside; NEW free-standing rack
  `jp_f_mitsudogu_tate` (+ `_ab`): two posts on a sill, a small board roof, the sodegarami, sasumata and tsukubō hung
  heads up with two six-shaku staffs (rokushaku-bō) [HAK-V], standing on the gravel by the inspection room.
  **No matchlocks / bows displayed:** the overhaul is gunless (a gun rack would read as loot that is not there).
- **Notice boards:** the existing kōsatsu (jp_s_kosatsu_std) outside the east gate.
- Not built (recorded): the stables, the women's inspection room, the lookout (tōmi-bansho), the jail at the checkpoint
  (site 4's jail is the jail kit), the lake / mountain ends of the palisade (landmark placement work).

## Site 2: post-station office (toiya-ba)
- **Era test:** IN (the tenma relay system from 1601; every Tōkaidō station had one or two, GK + [TOIYA-S]).
- **NEW shell `Land_JP_Toiyaba` (sangawara) :** W 5 x D 3 ken, kirizuma, board walls. Front open on its posts the full
  5 ken to the yard: the **raised office (chōba) 3.5 ken x 3 ken at 0.45** open to the yard along its kamachi (a
  kutsunugi step) [TOIYA-S koshi-daka], its back 1 ken the ledger wall (registers, the relay ledgers); the right 1.5
  ken an earth doma full depth (the clerks' way in from the yard, a back door to the stable side). Windows in the back
  and the left end.
- **The yard (`Land_JP_Compound_ToiyaYard`):** board fence 9 x 7 ken round the office and the yard; the gate to the
  street by pick_gate("itabei", status="work", carts=True) = two-leaf kido_ryo 1.5 ken (horses and pack loads pass).
  Dressing: tie posts (jp_s_stable_yard_tie_post), the saddle rack, a manger trough, loads (bales, the handcart),
  a palanquin (kago) waiting, the fare board (the kōsatsu reused as the dachin-fuda board, recorded).
- **The big beam scale, NEW prop `jp_f_kanme_hakari` (+ `_ab`):** a steelyard (chigi-bakari) hung from a timber
  tripod-frame with a bale on its hook and the counterweight on the beam (C_CIVIC §4.3 18-19: large steelyard scales
  for cargo; the kanme-aratame-sho of c.1712 at five stations [verify], so the cargo weight station = this scale in
  the same yard: a dressing swap, nearly free).
- River-crossing office: not built (needs a river; a dressing swap of this shell later).

## Site 3: official compound (intendant's jinya / daikansho), ONE size
- **Era test:** IN (Takayama jinya shogunal from 1692; daikansho everywhere on shogunal land, C_CIVIC §4.1 9).
- **Gate:** the nagaya-mon object in the gap of the front line (D3's nagaya-mon template) in a NEW rank **"official"**:
  black boards (wood_kuro) instead of plaster, sangawara, dark gate posts = KEEP_CIVIC's "black nagaya-mon gate"
  (`Land_JP_NagayaMon_Jinya`). Explicit override of pick_gate (a gatehouse object, like the samurai mansion: the rule
  keeps gatehouses as separate objects, FX6 §3).
- **Office:** REUSE D3's small samurai mansion (`Land_JP_Samurai_S`: genkan + shikidai, tatami rooms, kitchen doma)
  furnished as the intendant's office `Land_JP_Samurai_S_Jinya` (clerks' desks, document boxes, ledgers, abacus,
  masu and scales for the tax rice, the sword rack at the genkan). Honest: the jinya offices were shoin-style rooms
  behind a genkan (C_CIVIC §4.1 9).
- **The court room (ginmi-sho) + the white-gravel court:** the bansho shell in size **"ginmi"** (`Land_JP_GinmiSho`):
  W 4 x D 3 ken, plastered (nakanuri + board dado), sangawara; the front open to the court: veranda 0.45 + tatami
  0.60 (the stepped levels), back office; the **oshirasu** gravel pad in the compound in front of it, straw mats on the
  gravel. (Takayama's are boards; the generic jinya gets the tile roof of the lowlands; recorded.)
- **Kura:** REUSE C3's plain kura furnished as the tax-rice store `Land_JP_Kura_Plain_Nengu` (rice bales, masu,
  sampling spikes = existing masu set).
- **Walls:** black board fence (itabei kuro) round the plot, the back gate by pick_gate("itabei", kuro, high, back) =
  kido_kata. Plot 17 x 16 ken (`Land_JP_Compound_Jinya`).
- Other sizes (town magistrate, domain office, rural magistrate): not built (usage); they are size variants of this
  template (plot + office shell choice).

## Site 4: jail compound (small generic; Kodenmachō = landmark later)
- **Era test:** IN (Kodenmachō 1613-1875; provincial lock-ups at jinya / sekisho).
- **Cell block, NEW shell `Land_JP_Roya`:** W 4 x D 3 ken, board walls stained black, itabuki. The period double
  lattice [C_CIVIC §4.5]: the **outer lattice** along the front (heavy squared bars 0.075 at 0.15 centres, rails,
  floor to head) with the block's door; a 1-ken earth corridor (soto-zumari) behind it; the **inner lattice** with two
  cells 2 x 2 ken, each closed by a sliding lattice door; cell floors raised boards 0.30 with straw mats, a toilet tub
  (an existing lidded tub), wooden bowls; a small high barred window in the back wall of each cell. **Game concession
  (recorded):** the real cell door was a low crawl door (tsume-guchi); ours a full lattice leaf (D1 / D2) so the
  cells are enterable. Neutral: empty, the doors left open.
- **Guard office:** REUSE the jishin-ban (guardhut M) furnished `Land_JP_Guardhut_M_Itabuki_Roban` (keys board,
  clappers, lantern, brazier, ledger).
- **Compound (`Land_JP_Compound_Roya`):** a plastered wall (dobei, tile-capped; Kodenmachō had a high earth wall + a
  moat) 10 x 9 ken, ONE gate by pick_gate("dobei", status="high", role="front") = roofed kabuki-mon 1.5 ken.

## Site 5: fire watchtower (tall) + fire brigade station
- **Era test:** towers IN (1658 on; Kyōhō one per ~10 chō [KB-HNM]); machi-bikeshi IN (1718-20); **matoi IN as the
  matoi-nobori** [WP-MATOI] (the baren form is later: we build the 1720s banner form); hand pump OUT (1754+).
- **Tower, NEW climbable site object `Land_JP_S_Hinomi_Yagura`** (the ladder tower's conventions: a View component
  'ladder1' + the vanilla ladder memory points, Geometry class=house + laddertype=wood): the **town type** (black,
  lower than the 3-jō shogunal tower [KB-HNM]): four tapered legs (2.6 m square at the foot, 1.5 m at the deck) on
  stone footings, side and back ties (none across the ladder face), the ladder up the front face, a **lookout deck at
  6.40 m** (1.5 x 1.5 m, boards, a black board parapet 0.95 on three sides, the ladder side open), four posts carrying
  a small board roof with its underside **2.20 m over the deck** (FX4's head room), the **hanshō bell** hung outside
  the back parapet from the roof overhang with its striker. Taller than the 4.9 m ladder (deck 6.40, roof top ~9.1).
- **Station (`Land_JP_Compound_Hikeshi`):** a board fence 8 x 7 ken, the gate by pick_gate("itabei", status="work",
  carts=True) = kido_ryo 1.5 ken (ladders and hooks go out at a run). Inside: the tower, the tool shed = C2's open board
  shed furnished `Land_JP_Shed_Open_Board_Hikeshi` (fire hooks, ladders, buckets on the rack, the matoi, padded
  coats); the existing fire-gear rack and a leaning ladder outside.
- **NEW prop `jp_f_matoi_nobori` (+ `_fallen`):** the 1720s matoi: a pole (~2.7 m) with a carved wooden head
  (the group mark, a box-and-disc dashi) and a long narrow banner (nobori) hung from a cross bar below it, in a
  ground stand; fallen: lying.

## Site 6: execution grounds: only if usage allows at the end (else listed as not done).

---

## District (Stephen's one-district rule)
Ground survey (spikes/W3C2/_survey.py): west of 3c-2's west lane, **x 748-826, z 838-896**, 24.2-25.7 m, a ~1.3 %
fall west along z 864 and ~3 % to the south; no trees, no earlier placements. The lane: 3c-2's LW lane corner
(826, 864) continues WEST along z 862-866 through the district and through both checkpoint gates, ending past the
Kyoto-side kōrai-mon (the route's far landmark). Order from the trade districts: the post-station office (north) and
the fire brigade (south) first, then the jinya (north) and the jail (south), the checkpoint at the far west.

## Changes while building (recorded)
- **Kora-mon span 1.5 ken, not 2:** a 2-ken pair fails C10 (the open leaves are out of reach from outside: the
  existing 2-ken kabuki-mon fails the same way); 1.5 ken (clear ~2.5 m) passes and still takes horses and palanquins.
  The rear posts stand 0.11 outboard of the main posts' lines (the open leaves clear them); their small roofs start
  0.32 behind the gate line so their verges clear the palisade points (C12).
- **Palisade:** 6-sided logs r ~0.08 at 0.22 centres, tops 2.40 +-0.03, points 0.20; Resolution 2 / 3 = a slab with a
  ridge prism (C15); 284 R1 faces per 2 ken.
- **Jinya roofs are boards** (itabuki): Takayama's are all boards [TAK-WP], and a tiled black nagaya-mon was +59 % R1
  (over the +50 % limit). So the black nagaya-mon = black boards + board roof (6.0k R1), the court room itabuki too
  (its plaster walls + board dado kept).
- **The jail fence is a black board fence without a cap** (Land_JP_Compound_Roya): a plastered dobei was 19.3k R1
  faces (over the 15k binarize limit), a board-capped fence +81 % R3. Its one gate by the picker = kabuki-mon 1.5 ken.
- **The jail's guard office = W2F's furnished jishin-ban as it is** (Land_JP_Guardhut_M_Itabuki_Jishinban: capture
  tools, brazier, counter); no new variant.
- **The cells' partition is an earth wall** (a board partition failed C22 at the back wall); the lattices and the
  barred windows are declared C11 portals (see-through by design).
- Kitchen stove of the guardhouse on the doma's partition side (the door-to-door band, D4).
- Over budget (reasons in govsite.over_budget_ok): Land_JP_Toiyaba 7.1k R1 (+18 %: a 5 x 3 ken tiled hall open on
  its posts). Everything else inside its class cap. Largest object: Land_JP_Compound_Sekisho 9.0k R1.
- No white gravel (shirasu) material in the library: the oshirasu pads use stone_river with a gravel Roadway
  (a material job, flagged).
