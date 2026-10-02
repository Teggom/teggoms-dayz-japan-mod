# W3C1 setup notes: wave 3c-1, the town trade sites (agent W3C1, 2026-10-02)

Written BEFORE modelling (PRODUCTION_PLAN "research first"). Scope: research/catalogue/KEEP_TRADES.md 3 (brewery
complex), 4 (water mill), 17 (dyer's yard), 21 (paper mill); PARTS_GAP_AUDIT TR03 / TR04 / TR17 / TR21.
Sources: the project's research (`B_TRADE_INDUSTRY.md` = BT, `PARTS_GAP_AUDIT.md` = PGA, `PLAYBOOK.md`), a few web
pages read this run (listed per item; generic searches, no personal data in any request), and general
architectural / craft-history knowledge marked **(GK)**. Survivors, museum pieces and prints dated after 1730 give
form and proportion, not dates (PLAYBOOK §1 caution). Every dimension below is a recorded CHOICE; the models follow it.

Common rules: one storey + attic cap (G1-5; a kura loft by stair is the allowed elevation, as C3's kura); dead world
"as it was left", autumn, everything cold, dry and stopped; loot lies out on floors and surfaces; D1 / D2 doors
>= 1.00 x 2.00 m; every object < ~15,000 faces (binarize vertex limit): a complex is several objects.

---

## TR03 Sake brewery complex (saka-gura) - the hero

### Form: the kasane-gura (two long kura side by side) around a yard
- **Source (web):** sake-museum.jp (Hakushika Memorial Museum of Sake) "Facilities and Functions of Sake Brewery
  Building" and "The Former Main Sake Brewery Building of Tatsuuma-Honke Brewing Built in 1869"; nada-ken.com
  "Rokko-oroshi / kasane-gura"; foodinjapan.org "Kura". The Nada form: two long east-west kura built side by side,
  the large brewery (o-kura) to the NORTH, the front brewery (mae-gura) to the SOUTH. The mae-gura holds the washing
  area (araiba), the rice-steaming place (kamaba), the koji room (koji-muro) and the resting room (kaishoba) for the
  seasonal brewers; the o-kura holds the main mash fermentation and the pressing area (funaba / shiboriba), and its
  upper floor the yeast-starter work in shallow tubs. Many windows in the o-kura's north wall take the cold
  Rokko-oroshi wind; the mae-gura shades the o-kura from the south sun. An open yard before the kura (kura-mae) dries
  casks and tubs.
- **Era test:** the survivor is 1869; Nada brewing "first began to flourish during the middle of the Edo period"
  (sources above). Large kura breweries with these functions are IN for 1730 (Itami / Ikeda were the great brewing
  towns then, BT 7a); the exact doubled Nada plan may be a little later than 1730 (GK: uncertain). Kept: it is the
  documented period plan of a big brewery and the brief asks for a complex of storehouse buildings around a yard.
  **Flagged** in the checklist.
- **Walls / roof (GK, the surviving Nada / Fushimi kura):** thick earth walls (okabe), white plaster above a lower
  band of black boards (the yakisugi / shitami skirt), granite footing, sangawara kirizuma roofs. Kit: C3's kura
  pieces (okabe 0.24, kura footing, shitami _kura, plaster gable, the plastered kura eave), sangawara.

### Recorded choices (sizes)
| Piece | Choice | Why / source |
|---|---|---|
| o-kura | 9 x 4 ken (16.4 x 7.3 m), eave 5.40, earth floor 0.30 on the footing, a loft (the moto-ba, yeast starter) over the west 2.5 ken at 2.85 by the kura's open stair | Tatsuuma: two-storey large brewery, starter upstairs; real Nada kura run 20-30 ken long (GK), scaled to 9 ken for the island. Eave 5.40 so the loft keeps >= 2.10 m under the tie beams |
| o-kura openings | doors on both gables (west: starter / store end, east: press end; the kura door part), 3 barred kura windows in the north wall + 1 loft window in the west gable; the south wall blind (the mae-gura stands against it) | Tatsuuma north windows |
| mae-gura | 9 x 3 ken (16.4 x 5.5 m), eave 3.70, one storey; from the west: araiba + kamaba (one 5-ken earth floor, two front doors, a koshiyane steam vent over the hearth), the koji-muro block (an ante-room + the muro behind it = the double doors), the kaishoba (a raised board room for the brewers with a small entrance doma) | sake-museum: front building functions; 3.70 eave puts its ridge under the o-kura's eave |
| the join (roof union) | the mae-gura's back eave stops 6 cm short of the o-kura's south wall; a wooden gutter (tani-doi) on brackets under that eave + a flashing board on the o-kura wall carry the water away; the two kura are separate objects 4 cm apart (each closed, each its own doors) | see "New parts" below; the internal link between the two kura is NOT made (each opens to the yard) |
| big fermentation tubs (shikomi-oke) | 1.82 m across x 1.70 m high, cedar staves, bamboo hoops, a plank lid; 4 on the o-kura floor (one with a ladder leaning on it, one collapsed / staved) | GK: 20-koku tubs (1 koku = 180 l; 3.6 kl working volume + headroom). Staved tubs with hoops: barrel technology nationwide by the 15th-16th c., big brewing tubs 17th c. on (mizu.gr.jp "Mizu no bunka" 63) |
| starter tubs (hangiri) | shallow wide tubs 1.10 across x 0.30, stacked; the starter tubs (moto-oke) 0.75 x 0.60 | GK; Tatsuuma "shallow wooden tubs" upstairs |
| steamer (koshiki) over the hearth (kamaba) | clay-and-stone hearth 2.2 x 2.0 x 0.85 with the fire mouth to the front, an iron cauldron 1.4 across sunk in it, the cedar koshiki 1.45 across x 1.15 high on it with its lid; a step block | sake-museum: "a cauldron of water placed on a fire with a large steamer filled with rice placed on top" |
| koji-muro | an inner room 2 x 2 ken, walls and ceiling lined with straw mats (the husk insulation), a board ceiling at 2.30, entered through an ante-room: two doors in series (the double doors); inside the koji bed (toko: a table 1.8 x 1.2 with cloths) and shelves of koji trays (koji-buta 0.45 x 0.30) | sake-museum: "rice husks and other insulating materials were affixed on the ceiling, the walls and the floor", "double doors at the entrance" |
| the lever press (fune + tenbin) | the press box (fune) 2.4 x 0.95 x 0.95 m with its spout over a sunk receiving jar; the beam 6.4 m (0.30 sq) pivoting under a cross-beam held between two heavy posts (otoko-bashira) at the box's head, pressing the lid blocks; at the free end the weight stones (6) hang in rope slings. Abandoned state: the beam down, slings cut, stones on the floor | GK: the lever press with hanging stones (tenbin-shibori) is the Itami / Nada method of the period; brewing manuals from the late 17th c. (Domo shuzoki, c.1687, GK) describe pressing in the fune; the form follows the Nihon sankai meisan zue plates (1799; form only). IN |
| rice polishing | the seimai-goya: an open board shed 4 x 2 ken in the yard with 4 foot-treadle mortars (kara-usu): a 2.4 m lever on a pivot between two posts, the pestle head over a mortar sunk to its rim, a hand rail for the treader | Nada's water-wheel polishing begins in the Meiwa era (1764-72) (sake-museum.jp "History of rice polishing, Edo"; nada-ken "suisha seimai"); before that, and in Itami, foot polishing. So in 1730: FOOT polishing (the water mill is a separate rural mill, TR04) |
| sugidama | a ball of cedar sprigs 0.75 m across hung from the shop's front eave by a rope; **brown** (hung green with the new sake in early spring, brown by autumn) + a fallen state | GK; the cedar sign is attested in Edo-period pictures; first date uncertain (flag) |
| casks | the 4-to taru (B3a / L1 props: jp_f_taru_cask, _komo, _rack3) in the cask kura | reuse |
| soy / Hatcho miso dressing | a Hatcho-style miso vat: a big cedar vat (1.6 x 1.5) with a cone of river stones on the lid; soy moromi = another shikomi-oke | Hatcho miso: Okazaki makers from the 14th / 17th c. (GK). Dressing only (brief) |
| ladder | a STATIC leaning ladder (hashigo) as a prop (on a tub, in the kura); no engine-climbable ladder: the loft is reached by the kura's stair (G1-5 allows stair or ladder; the engine ladder is untested in this pipeline, PGA item 24) | recorded choice |

### Buildings of the complex (classes)
o-kura (`Land_JP_SakaGura_Okura`), mae-gura (`Land_JP_SakaGura_Maegura`), the rice-polishing shed
(`Land_JP_SakaGura_Seimai`), the cask kura (C3's plain kura shell furnished with casks), the brewer's shop at the
lane (W3B's tiled earth-floor workshop shell furnished as the brewer's shop: casks, measures, the counting desk, the
sugidama on the eave), the board-fenced yard with its gate (`Land_JP_Compound_Brewery`, K3 kit). Each furnished.

---

## TR04 Water mill (suisha-goya)
- **Sources (web):** Mitaka city "Shinguruma" water mill pages (pestles: zelkova 15 cm square, ~3 m long, ~44 kg;
  lifted by cams (nade-bo, 4 per pestle) on the shaft catching a tappet board (hago-ita) on the pestle, then dropped;
  12 + 2 pestles; mortars); ja.wikipedia "Suisha-goya" (overshot ~2.5x the efficiency of undershot; vertical wheels
  need gears to turn millstones); Boso-no-mura (late-Edo mill: stamps + grinding mills). The Mitaka mill is 1808 (GK):
  form only. Era: water-driven stamps for rice / grain are old (the 610 water-mill entry, GK) and common in villages in
  the Edo period: IN.
- **Stephen's decision:** the wheel is stopped and the flume dry; on dry land on the test island; moved into a stream
  later, so the wheel + flume are built so a move needs only placement (the flume is a separate kit part for a longer
  run; the mill object carries a short run).
- **Recorded choices:** hut 3 x 2 ken (5.5 x 3.6 m), board walls, earth floor, itabuki / thatch; eave 3.60.
  OVERSHOT wheel 3.64 m across (2 ken), 0.55 wide, 24 buckets, octagonal axle 0.28 through the hut's gable at 2.10
  (the wheel's foot 0.28 over grade on dry land: in a stream it stands in its tail-race). Inside on the same shaft: 3
  sets of 4 cams lifting 3 vertical pestles (0.15 sq, 3.0 m) in a guide frame over 3 mortars sunk to a 0.20 rim.
  The flume (kakehi): an open board trough 0.40 wide on trestles, its mouth over the wheel's top, a sluice board
  (shut) at the run's head; dry, leaves in it.
- **The stone mill: hand-turned, not wheel-driven.** Gear-driven millstones in Japanese water mills are a late-Edo
  feature (GK: uncertain before the late 18th c.); in 1730 the mill hut's grinding is the hand quern (ishi-usu, the
  existing jp_f_usu_ishiusu) beside the stamps. **Flagged for Stephen** (easy to add a gear train later).

---

## TR17 Dyer's yard (kon'ya / ai-ya)
- **Sources:** BT 4 "Indigo dyer": doma with **vats sunk into the floor, often four with a fire pit in the middle**,
  sukumo in bales, lye tubs (akumizu), bran and lime, stirring poles, dripping cloth, tall drying poles and frames in
  the yard; ja.wikipedia "Kon'ya": the dyers' guild in Osaka 1615, **Edo 1721**, Kyoto 1756; indigo (sukumo / aidama)
  shipped from Awa: IN. BT "Tie-dyer": Arimatsu shibori on the Tokaido from 1608, sold at the shop front: IN.
- **Recorded choices:** the workshop 4 x 3 ken, town (sangawara) / board roof; the front 1 ken = a shop doma with the
  shop-front cloths (the Arimatsu flavour: indigo + undyed cloth on a pole; **no shibori pattern texture exists**, the
  cloth is plain: a material job if wanted); behind, the vat room: its earth floor raised 0.30 on a stone kerb (one
  step up from the shop doma), the **four stoneware vats (ai-game) sunk to the rim** (mouth 0.62) in a 2 x 2 group
  around a square **fire pit** (hi-tsubo, 0.45, ash, 0.25 deep), dye surface 0.15 under the rim. Why the raised
  floor: the island's terrain would show inside a jar sunk below grade (no terrain cut), so the floor rises to hold
  the jar depth above it. The vats are SHELL geometry (a floor pit), not props. A back door to the yard.
- Yard (K3 board fence + gate): two tall drying-pole frames (monohoshi: posts 6.0 m, two cross bars, long cloth hung
  doubled), sukumo bales (straw-wrapped), the lye drip tubs, a stirring-pole rack.

## TR21 Paper mill (kami-suki-ba)
- **Sources:** BT 6 "Paper mill": by clean cold water; bark-steaming vat (koshiki) over a cauldron, stripping knives,
  a soaking pit, ash-lye cauldron, picking tub (chiri-tori), beating block and wooden mallets, the paper vat
  (suki-bune) with mucilage (neri), the mould and screen (suketa, su), a couching stack (shitoku) on a lever press with
  stones, **drying boards leaned in the sun (hoshi-ita)**, brushes. Mino and Shuzenji (gampi) paper: IN.
- **Recorded choices (GK sizes):** workshop 4 x 2.5 ken, rural, itabuki / thatch, earth floor, wide window bays on the
  front (light for sheet forming); the vat 1.80 x 0.90 x 0.60 with the mould 0.75 x 0.55 hung from a bamboo spring
  pole over it (nagashi-zuki); the beating board + mallets + bark bundles; the couching stack under a small lever press
  with stones; the picking tub; the bark steamer (a small koshiki over a cauldron on a hearth) outside under a lean-to.
  Yard (K3 open bamboo fence + gate): drying boards (1.80 x 0.45 planks, a few with sheets brushed on) leaned on
  racks facing south; a dry stone soaking tank (the stream comes with the real map).

---

## New parts (PGA flags) - what is built and what is not
| PGA item | This wave | Why |
|---|---|---|
| 34 jp_p_mech_waterwheel | **built**: `jp_p_mech_waterwheel` _overshot (wheel + axle + bearing posts) | the mill |
| 18 jp_p_water_sluice | **built as the flume**: `jp_p_water_flume` _run (1.5-ken trough module on a trestle) and _head (with the sluice board, shut) | the mill's kakehi; weirs / big sluice gates stay for the canal / river work (CV8 / CV9) |
| 13 jp_p_roof_union | **built for the parallel case only**: `jp_p_roof_union` _gutter (the gutter + flashing where a lower parallel roof's eave meets a taller wall: the kasane-gura join) + roofs.roof learns per-eave overhangs (ov=(front, back)) | the kasane-gura is a parallel join; L / T valleys (hip-to-gable intersections) are NOT built (no shell of this wave needs them) |
| 24 jp_p_ladder | **not built as a part**: a static leaning ladder PROP only | the engine ladder action is untested here; the kura loft uses the stair (G1-5) |
| frame_koyagumi, floor_pit, stair | reused | exist (manifest) |

## District (Stephen's 2026-10-02 rule: one new district, off the showcase)
Ground survey (spikes/SH1/terrain_sh1.ground, 5 m grid): the pad (25.00) is full; the flattest free ground near the
spawn is SOUTH-WEST, off the pad's corner: x 885-950, z 845-895 lies at 25.6-26.2 m (within 0.3 m over most
50 x 30 m blocks), ~150 m from the spawn, nothing placed there, no trees. The trade quarter goes there: an east-west
lane with the brewery and the dyer on its north side, the paper mill and the water mill on its south side. Extent and
IDs: SHOWCASE_MAP.md "W3C1" + w3c1_map.jpg.

## Not built / cut (cost rule)
- The internal door between the two kura; the brewer's house (omoya) beyond the shop; a shochu still; the vinegar /
  mirin trades.
- ☆ Country sake brewer: only if nearly free at the end.
