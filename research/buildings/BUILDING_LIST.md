# Building list: every 1730 building type and its interior (merged, for collapsing)

Merge agent BL-M, 2026-09-29. Text only. Merged from `A_DWELLINGS.md` (homes and outbuildings), `B_TRADE_INDUSTRY.md`
(commerce, lodging, food, crafts, industry) and `C_CIVIC_RELIGIOUS_LAYOUT.md` (layouts, Shinto, Buddhist, government,
military, civic). Anchor year 1730; 1680–1750 fully in; wider Edo is tagged.

**What this is.** Every building type the three agents found, one entry each, with the items that make its interior
read right. Nothing has been collapsed: that is Stephen's pass. §4–§7 exist to make that pass fast.

**How to read it.**
- §2 says which buildings appear in which settlement, and in what proportion. Read it first.
- §3 is the list: `- **Name (romaji)**: function. Rooms / setting. Items: ... tags`. Categories use `== Name ==`
  headings. Setting words from B: `town shop`, `town workshop`, `rural`, `site` (standalone works), `stall`,
  `itinerant` (no premises; a prop kit). Floor words: doma (earth) and raised (board or tatami).
- Where two lanes describe the same building, one entry is counted and the other says `not counted` with a pointer
  (§4 lists every case). Pointer lines and prop lists in italics are not counted.
- **Loot rule (binding):** furniture and containers are dressing, never loot containers. Loot lies on floors and
  surfaces, as in vanilla DayZ. No entry below marks anything as a container.
- Sources: the agents' short citations were trimmed to museum / survivor names and WORLD_CATALOGUE T-numbers where
  useful for modelling; full citations stay in the three input files.

**Tag legend (unified from all three agents).**

| Tag | Meaning |
|---|---|
| `[outside 1680-1750: date]` | Real, but outside the window (earlier or later). Listed so Stephen can decide. |
| `[off-map: region]` | In the window but far from the Kyoto–Osaka–Edo / Tōkaidō / Nakasendō map. A few were added by the merge where the agent named a far region without the tag; those say "region tag added by merge". |
| `[survivors late]` | What you can visit today is a late-Edo or Meiji rebuild; the type is older. (`[survivors mixed]` once.) |
| `(assumed)` | The agent's best reading, not pinned to a source. |
| `(verify)` | The agent had a source memory but did not re-check; B's `[uncertain]` is folded in here. All are in §7. |
| `in era` / `in window` | Positively dated inside 1680–1750 by the agent. |
| `{from C §x}` | Entry moved into this section from another lane's file. |

**Counts per section (counted entries; pointers, duplicates and prop lists excluded).**

| § | Section | Entries | Main source |
|---|---|---|---|
| 2 | Settlement layouts | 15 layouts | C |
| 3 | Dwellings: poor | 48 | A |
| 3 | Dwellings: lower-middle | 47 | A |
| 3 | Dwellings: upper | 21 | A |
| 3 | Dwellings: outbuildings | 21 | A |
| 3 | Shops and retail | 30 | B |
| 3 | Food and drink | 58 | B |
| 3 | Lodging | 12 | B (+2 from C) |
| 3 | Services | 38 | B |
| 3 | Crafts by family | 161 | B |
| 3 | Rural industry | 30 | B |
| 3 | Shinto | 32 | C |
| 3 | Buddhist | 46 | C |
| 3 | Government | 41 | C |
| 3 | Military | 38 | C |
| 3 | Civic and infrastructure | 59 | C |
| | **Total building entries** | **682** | |
| 4 | Seams / contradictions | 28 / 14 | |
| 5 | Shared-kit items counted | ~95 | A, B, C + count |
| 6 | Collapse groups | 60 (+ cut lists) | A 15, B 31, C 15 |
| 7 | Verify flags | 65 | |

Note: the agents' own counts differ from these because this file splits some lines and joins duplicates (for
example C's cult tells, sect notes and "names only" lines are kept as italic prop lists, not entries).

**Contents:** 2. Settlement layouts · 3. The building list · 4. Seams and duplicates · 5. Shared core kit ·
6. Collapse candidates · 7. To verify

---

# 2. Settlement layouts

Source: C §1, tightened. Numbers marked (assumed) are C's arithmetic or reading of period maps. Building names point
to entries in §3.

**Three 1730 facts that change what a map shows (C):**
1. **Shrines and temples are fused (shinbutsu shūgō).** A shrine of any size often has Buddhist buildings (pagoda, goma
   hall, a bettō-ji run by monks); many temples have a small tutelary shrine. Separation is 1868. A "pure" shrine
   precinct is anachronistic except at Ise and Izumo.
2. **Edo and Osaka castles have no keep in 1730.** Edo's burned 1657 (only the stone base rebuilt, 1659); Osaka's burned
   by lightning 1665. Kyoto's Nijō keep stands until 1750.
3. **Every household is registered at a Buddhist temple (terauke / danka, from the 1630s–60s).** Every village has, or
   belongs to, a temple, and temple graveyards are everywhere.

**Rule of thumb for every settlement (assumed):** sacred sites at the edges and on slopes; the working core on the
flat or along the road; government is one walled or gated compound, not a district, except in castle towns and the
three great cities.

## 2.1 Rice-farming village (hirachi no mura / heiya no nōson)

- **Scale:** Genroku registers (1700–02): ~63,000 villages for ~26 million koku, so ~400 koku average (assumed
  arithmetic; verify). Typical 40–100 households, 250–500 people; villages 1–2 km apart.
- **Forms:** nucleated cluster (shūson) on a terrace edge or levee; dispersed farmsteads each in a windbreak grove
  (Tonami, Izumo, Kantō yashikirin); street village along a road (rosō).
- **Layout:** houses on dry ground, paddies below, dry fields (hata) and woodlot (satoyama) behind; irrigation channels
  thread the houses; a water gate at the intake. Chinju shrine in a grove on rising ground at one edge; village temple
  with graveyard at the other edge or on a slope; dōsojin, Jizō and kōshin stones at entrances and crossroads;
  kōsatsuba at the entrance or before the headman's gate.
- **For a 60-house village:** 1 headman's house with gate and 1–2 kura, doubling as village office · 5–10 full-farmer
  (honbyakushō) houses · 40–50 small farmer / tenant (mizunomi) houses · 1 chinju shrine (+ haiden if rich) · 2–6
  hokora and field shrines · 1 village temple (sometimes 2 sects) or 1 small dō served from elsewhere · 1 gōkura in
  many villages · 1 kōsatsuba · 5–15 wells (lever or pulley) · 1–3 water-gate / sluice points, sometimes a watch hut ·
  0–1 smithy, 0–1 general store · threshing yards and drying racks everywhere · 1 temple graveyard plus scattered
  family graves at field edges · 1 cremation or burial ground (sanmaiba) outside the village in some regions · a
  fire-watch ladder with bell in larger villages (assumed).

## 2.2 New-field village (shinden-mura)

- Planned villages on reclaimed land; a boom under Yoshimune's Kyōhō reforms (1720s): very 1730.
- **Layout:** a straight road with long strip plots running back: house and windbreak at the front, then field, then
  woodlot. Musashino's Santome (1694, Kawagoe domain) is the model: each plot ~40 × 675 m (verify).
- **Buildings:** identical farmhouses at regular spacing (Dwellings, dry-field farmhouse), a new small shrine, often no
  temple yet (families stay registered at the old temple), a deep well per few houses on the dry plateau.

## 2.3 Mountain village (sanson)

- **Scale:** 10–40 households; hamlets (kumi / buraku) of 3–10 houses strung along a valley.
- **Layout:** houses stepped along the contour on stone-walled terraces; small terraced paddies on the valley floor;
  dry fields and yakihata on slopes; forest above.
- **Buildings:** farmhouses, charcoal-burner huts, watermill · yama-no-kami shrine, often a stone or tiny hokora under
  a big tree at the forest edge · a small dō or hermitage rather than a full temple · timber-control posts where the
  forest is the lord's (Kiso: Owari's timber office at Agematsu, forest guards enforcing the "five trees" felling ban,
  c.1708, verify) · log, vine or cantilever bridges, suspended water pipes (kakehi) · summit / pass shrine (tōge no
  jinja) and pass tea house.

## 2.4 Fishing village (gyoson / ura)

- **Scale:** 30–150 households, much denser than farm villages.
- **Layout:** houses packed in narrow lanes parallel to the shore, gable ends to the sea; boats hauled up on the beach;
  net sheds and drying racks along the beach line; a steep path to shrine and temple on the headland or hill behind.
- **Buildings:** 1–3 net-owner (amimoto) big houses with store sheds; many small fisher houses · net sheds, boat sheds,
  fish and seaweed drying racks, salt huts · fish-spotting tower (uomi-yagura) on the headland (assumed common for
  sardine and tuna nets) · Ebisu / Konpira / Sumiyoshi / Funadama shrine; a kōshin or Jizō at the landing · young
  men's lodge (wakamono-yado) · coastal lookout (tōmi-bansho) and beacon post in domains with sea frontiers · graves on
  the slope facing the sea.

## 2.5 Post town (shukuba-machi), Tōkaidō / Nakasendō

- **Numbers (Taigaichō 1843, a century late; scale down slightly):** Tōkaidō 53 stations: 111 honjin, 68 waki-honjin,
  2,988 hatago, ~48,000 houses, ~196,000 people; average station ~2 honjin, ~1.3 waki-honjin, ~56 hatago, ~900 houses.
  Small examples: Mariko 211 houses, 1 honjin, 2 waki-honjin, 24 hatago · Tsumago (Nakasendō) 83 houses, 1 honjin, 1
  waki-honjin, 31 hatago, 418 people · Kusatsu (the junction) 586 houses, 2 honjin, 2 waki-honjin, 72 hatago · Kuwana
  2,544 houses, 120 hatago. Kiso stations kept 50 porters and 50 horses, Tōkaidō stations 100 and 100.
- **Layout:** strictly linear along the highway for 0.4–2 km, one house deep (sometimes two), long narrow plots back to
  stables, kura, gardens, fields. Each end: mitsuke (bank or masugata crank), kōsatsuba, sometimes a bansho. Centre:
  toiya-ba with its yard, honjin and waki-honjin, the dense block of hatago, the headman. Ends: cheaper lodging, tea
  houses, smithy and farrier, then farms. Behind the street on the hill side: 1–5 temples, 1–3 shrines. Nearby:
  ichirizuka pairs outside town, pine or cedar avenues, a river crossing or sekisho in some cases. Between stations:
  tateba and ai-no-shuku.
- **Mid Nakasendō station (~150 houses; assumed):** 1 honjin, 1 waki-honjin, 1 toiya-ba, 25–40 hatago, 5–10 cheap
  lodgings, 10–20 tea houses and food stalls, 60–90 ordinary town houses and shops, 2–3 temples, 1–2 shrines, 1
  kōsatsuba, 1 fire ladder, many rear stables.

## 2.6 Intermediate stops (ai-no-shuku, tateba)

- Unofficial rest hamlets between stations: lodging banned, food and horse changes allowed. 5–30 houses, tea houses and
  a rest yard, a horse trough, a Jizō or Batō Kannon, maybe a small dō. No honjin, no toiya-ba. (assumed, from Vaporis)

## 2.7 Castle town (jōkamachi)

- **Numbers:** ~170 castles after the 1615 one-castle-per-province rule (from 3,000+). By 1730 ~170–190 castles are
  daimyo seats; ~100+ smaller daimyo govern from a jinya, so their "castle town" is a jinya town (assumed; verify).
- **Zoning from the centre (planned ideal; real towns bend to rivers and hills):** (1) castle core: honmaru / ninomaru /
  sannomaru inside moats · (2) upper samurai quarter: big yashiki inside the outer moat or by the ōte-mon · (3) middle
  samurai: grid blocks of walled yashiki, quiet streets of nagaya-mon and plaster walls · (4) townsmen's quarter along
  the main road; trades cluster in named streets (Kaji-machi smiths, Konya-machi dyers, Daiku-machi carpenters, Uo-machi
  fish, Tera-machi, Kōya-machi); market and merchant houses on the road, craftsmen on side streets · (5) ashigaru rows
  in belts on the approaches as a defensive screen · (6) temple district (tera-machi): a line of 10–30 walled temples
  with graveyards along the edge facing likely attack · (7) edge: kawata village and hinin huts, usually across a river
  or at the far edge near the execution ground on a highway approach (assumed; Botsman).
- **Streets:** T-junctions, cranks (kagi-no-te), dead ends; masugata gates where roads enter. Townsmen's blocks often
  square (Edo 60 ken ≈ 109 m), samurai blocks longer.
- **Proportions:** samurai land 60–70 % of area; townsmen 15–25 %; temples and shrines 10–15 % (Edo late-period 68 / 16 /
  16). Samurai and dependents often 40–50 % of people (assumed; McClain gives Kanazawa's as roughly half).
- **Per mid castle town (~20,000 people; assumed):** 1 castle (with or without keep) · 1 domain school in a few domains
  only (mostly after 1750) · 1 town magistrate's office + 1 rural magistrate (kōri-bugyō) office · 1 jail · 5–20 kido
  gates in the townsmen's quarter · 3–10 fire ladders · 20–40 temples · 5–15 shrines incl. a Tōshōgū in many domains ·
  1–3 dōjō · 1 horse ground · 1 archery range · domain storehouses and a rice market.

## 2.8 Jinya town (jinya-machi)

- Seat of a castle-less small daimyo or a shogunal daikan: one walled compound on a slight rise, a short street of
  samurai houses, a townsmen's street, a temple or two. Looks like a big post town with a government compound.
  Takayama (shogunal from 1692) is the surviving example.

## 2.9 The great cities (Edo, Kyoto, Osaka)

- **Unit = the chō (ward):** one block-length of street and its two frontages, run by its house-owners (iemochi), with a
  ward office, a ward elder (machi-doshiyori / chō-doshiyori), a kido gate at each end, a guard hut and a notice spot.
  Back-alley tenants have no vote.
- **Edo (~1 million by the 1720s; 1721 townsmen count ~500,000, samurai and clergy uncounted):** 1,678 chō by 1745
  (933 in 1713: growing fast in our window). Land use (late Edo): samurai 68 %, temples and shrines 16 %, townsmen
  16 %; daimyo yashiki alone ~36 %. Yamanote (western hills) = samurai estates and temples; Shitamachi (eastern
  reclaimed lowland) = townsmen, canals, markets, warehouses. Townsmen's block: 60-ken (≈109 m) square; street-front
  shops (omote-dana) round the edge; centre (kaisho-chi) filled with ura-nagaya on narrow roji lanes, each alley with a
  shared well, shared toilet, rubbish point and tiny Inari. Saying: "Ise-ya, Inari ni, inu no kuso" (Ise-ya shops,
  Inari shrines, dog dung). Firebreaks after the 1657 fire: broad plazas (hirokōji: Ueno, Ryōgoku), cleared strips and
  embankments (hiyoke-chi, hiyoke-dote); temples moved to the edges (Asakusa, Komagome, Fukagawa). Per chō: 2 kido, 1–2
  kidoban huts, 1 jishinban (often with a fire ladder), sometimes a well, often an Inari; samurai districts have
  tsuji-ban guard posts at crossroads instead. One fire tower per ~10 chō in Kyōhō. Outer moat has the 36 mitsuke
  gates; the keep is absent (1657).
- **Kyoto (~350,000 in the 1730s, assumed):** old-capital grid; the chō is the two sides of one street between
  cross-streets (ryōgawa-machi), not a block; groups of chō form a chō-gumi. Each chō has its own chō-ie / kaisho, kido
  gates and ward rules (chō-shikimoku). Temple districts (Teramachi-dōri and the eastern hills), the imperial palace and
  court nobles' enclosure, Nijō castle with the shoshidai and the two machi-bugyōsho nearby, remains of the Odoi
  earthwork.
- **Osaka (~400,000 in the 1730s, assumed):** Osaka sangō: 620 chō in three groups (Kita 250, Minami 261, Tenma 109;
  late-18th-c. count). A merchant city with few samurai (castle garrison, Osaka jōdai, machi-bugyō officials). Canals
  (horikawa) everywhere; "808 bridges", in fact ~200, a dozen or so shogunal, the rest townsmen's (assumed). ~100
  domain kura-yashiki on Nakanoshima and Dōjima (assumed). Dōjima rice exchange licensed 1730. Keep absent (1665).

## 2.10 Temple town (monzen-machi) and shrine-gate town (toriimae-machi)

- **Examples:** Zenkōji (main hall rebuilt 1707, in window), Narita (boosted by Edo exhibitions from 1703), Kotohira
  (Konpira), Nikkō, Kōyasan (a mountain town of hundreds of sub-temples), Ise's Uji-Yamada.
- **Layout:** one approach street (sandō) climbing to the gate, lined with souvenir, food, rosary, incense, talisman and
  medicine shops, tea houses and pilgrim lodgings; pilgrim-guide houses (shukubō at temples, oshi houses at Ise) with
  altar rooms and big kitchens. Side streets: sub-temples (tatchū) and their graveyards, a magistrate's office if
  shogunal land, outcast / entertainment edges.
- **Proportion (assumed):** 50–70 % of frontage pilgrim trade, 20–40 % sub-temples, the rest ordinary housing.
- **Ise:** shrines rebuilt in 1729 (20-year cycle: 1709, 1729, 1749), so in 1730 the buildings are brand-new and the
  empty alternate site beside each is bare with a small hut over the central-post spot. Pilgrim waves (okage-mairi) of
  millions in 1705.
- **Jinai-machi:** 16th-c. fortified Jōdo Shinshū temple towns, still ordinary towns in 1730 with a moat line and a
  central temple: Imai-chō, Tondabayashi.

## 2.11 Port town (minato-machi)

- **Examples:** Sakata, Mikuni, Hyōgo, Shimonoseki, Tomo-no-ura, Uraga, Nagasaki, Miya (Atsuta).
- **Layout:** streets parallel to the shore, lanes at right angles to the water; stone-stepped quays (gangi) and
  mooring stones; waterfront warehouse rows; shipping agents on the first street back; temples and a weather-watching
  hill (hiyori-yama) behind; lighthouse lantern (tōmyōdō) on the point; shipyards at one end, fish market at another.
- **Government:** ship-inspection office (funa-bansho) at controlled ports (Uraga from 1720); port magistrate in
  shogunal ports.
- **Markers:** western coastal (Kitamae) route opened 1672; taru-kaisen split from higaki-kaisen 1730.
- **Nagasaki:** Dejima (Dutch, 1636) and the Chinese quarter (Tōjin-yashiki, 1689), both walled with one guarded gate.

## 2.12 Mining town (kōzan-machi)

- **Examples:** Sado Aikawa (shogunal gold and silver, magistrate's office), Ikuno, Iwami Ōmori (silver; a daikansho
  town). Past peak by 1730.
- **Layout:** narrow valley town: magistrate's compound, ore-processing sheds, workers' row houses, temples up the
  slopes, adit mouths above. (assumed detail)

## 2.13 River-crossing town

- Stations where bridges were forbidden (Ōi River: Shimada and Kanaya; kawa-goshi system from 1696). High water
  (kawa-dome) stranded travellers for days, so these towns have extra inns, a river-crossing office (Government,
  kawa-kaisho) and porters' rows (Dwellings, river porters' row).

## 2.14 Hot-spring town (onsen-machi)

- Hakone's seven springs, Arima, Kusatsu (Jōshū): bath inns round a public bath (sotoyu) and the spring's shrine /
  Yakushi hall (Buddha of healing). See Lodging (hot-spring inn, communal bath) and Buddhist (Yakushi-dō).

## 2.15 Outcast and marginal settlements (neutral)

- **Kawata (eta) communities:** leatherworking, drum-making, prison and execution labour, some policing. Outside the
  townsmen's area, often on river flats. Buildings: ordinary houses, tanning yards, a temple (often Jōdo Shinshū), their
  own headman's compound (Edo: Danzaemon at Asakusa). Hinin huts near bridges and river beds.
- **Sick-prisoner infirmaries (tame)** run by the hinin headmen at Asakusa (1687) and Shinagawa (c.1698; verify).

---

# 3. The building list

Categories in the order: Dwellings (poor, lower-middle, upper, outbuildings), Shops and retail, Food and drink,
Lodging, Services, Crafts by family, Rural industry, Shinto, Buddhist, Government, Military, Civic and infrastructure.

## == Dwellings: poor ==

Source: A. Where a home has a shop, office or workshop, only the living side is here; the working side is under its
trade (see §4 Seams). Room words: *doma* / *niwa* = earth floor (entrance, kitchen); *itanoma* = board room; *hiroma* =
big board room with the irori (Kantō 3-room plan); *doza* = living on straw-covered earth; *nando / heya / nema* =
closed sleeping room with a sill to hold straw bedding; *dei / zashiki / oku* = front best / formal / back room;
*daidokoro* = family room by the kitchen; *tōri-niwa* / *hashiri-niwa* = machiya earth passage / its kitchen stretch;
*zushi-nikai* = low attic upper storey of a Kamigata townhouse; *hibukuro* = tall smoke void over a machiya kitchen.

Two rules shape every home (PLAYBOOK §2): no tatami in poor rural homes; commoners, however rich, stay plain (no
nageshi, no tsuke-shoin, no patterned paper, no lacquer or gold on the building). Bedding is a class marker in 1730:
towns have cotton futon; the rural poor sleep on straw under mats or a sleeved quilt (yogi / kaimaki).

### Rural: rice villages

- **Tenant rice farmer's hut (kosakunin no ie / mizunomi-byakushō no ie)**: landless or near-landless family renting
  paddy. One room about 3 × 4 ken, half earth. Rooms: doma + board or doza platform, no tatami, no ceiling (open to
  soot-black thatch). Items: irori, jizai-kagi pot hook, iron pot (nabe), one-hole clay kamado, water jar (mizugame),
  wooden sink board, mushiro, straw bedding, hoe (kuwa), sickle (kama), mino, kasa, waraji on a peg, straw-beating
  stone and mallet (yokozuchi), a few tawara rice bales, zaru baskets, box trays (hakozen), paper charm (ofuda) on a
  post.
- **Doza house (doza-zumai)**: poorest east-Japan form; no board floor, people live on straw heaped on packed earth,
  covered with mats. Rooms: one earth room with sunken irori, straw-heaped sleeping corner. Items: irori pit ringed with
  stones, deep straw layer, mushiro, straw bedding pile, pot, jar, rope coils, sandals drying by the fire. (Persisted
  into Meiji in Tōhoku: period-safe but long-lived.)
- **Dependent household's hut (nago / hikan no ie)**: hereditary dependent family on a big farmer's land, working for
  him in return for a plot; sits in or beside the master's yard. Rooms: doma + one board room. Items: as tenant hut,
  fewer tools (borrowed), straw work in progress (rope, sandals, bags), hemp spinning basket. `[outside 1680-1750:
  common 1600-1680; by 1730 fading in Kinai, still present in the east and mountains]`
- **Day labourer's hut on the village edge (hiyatoi / kado-ya)**: landless, hires out by the day for planting, harvest,
  road work. Rooms: doma + tiny platform. Items: carrying pole (tenbinbō), rope-net earth carrier (mokko), backpack
  frame (shoiko), sickle, straw bedding, one pot, one bowl set, sandal-making stool.
- **Widow's or elder's hut (poor inkyo-ya)**: one-room cottage for an old parent after the heir takes over, or a widow
  alone. Items: small irori, spinning wheel (itoguruma), hemp or cotton thread basket, small Buddhist shelf with a
  tablet (ihai), prayer beads, one pot, a teapot-less kettle, straw bedding.
- **Kinai tenant house with bamboo floor (take-yuka / sunoko-yuka)**: western Japan's cheap alternative to boards:
  split-bamboo slats over joists. Rooms: niwa + bamboo-slat room. Items: as tenant hut, plus cotton-ginning roller
  (watakuri), cotton bow (watauchi-yumi), spinning wheel, raw cotton in baskets (Kawachi cotton boom in era).
  (verify how common take-yuka still was by 1730)
- **Paddy / crop watch hut (ta-goya / shishi-goya)**: lived in for weeks in late summer/autumn to scare boar and deer.
  Rooms: one raised floor or earth, a fire. Items: bamboo clappers on long ropes (naruko), wooden drum or clapper
  board, straw bedding, small pot, torch (taimatsu), mino; a gun only for licensed pest-control hunters.
- **Famine refugee shelter (kiga-goya / sukui-goya)**: rough lean-to for the starving; in era, the Kyōhō famine
  1732–33 hit western Japan hard. Rooms: none. Items: reed mats, gruel pot, straw, begging bowl, bundle of bedding.
  (Official relief huts: see Civic, relief hut.)

### Rural: dry-field, upland, mountain and forest

- **Slash-and-burn upland farmer's hut (yakihata no ie)**: hill families growing millet, buckwheat, beans on burnt
  forest patches. Rooms: doma + board room. Items: rotary stone quern (hikiusu), wooden mortar and pounder (usu, kine),
  millet heads hanging, beans in straw bags, digging stick / mattock, fire rake, irori, pot.
- **Seasonal slash-and-burn field hut (yakihata-goya)**: hut at the burnt plot for clearing and harvest. Items: fire,
  straw bedding, mattock, seed bag, water gourd.
- **Charcoal-burner's kiln hut (sumiyaki-goya)**: lean-to beside the kiln for burn nights (kiln itself: Rural
  industry). Items: charcoal bales (sumi-dawara), bale-weaving frame, charcoal rake, billhook (nata), axe (ono), saw,
  shoiko, straw bedding, pot on three stones, water bucket.
- **Charcoal-burner's village house (sumiyaki no ie)**: family home in the hamlet. Rooms: doma + board room. Items:
  stacked charcoal bales in the doma, bale straw, axes, billhooks, saws, shoiko, irori, kamado, straw snow boots.
- **Logging-crew camp hut (yamagoya / soma-goya)**: long rough hut for fellers and sawyers (hiyō) far up the valley,
  e.g. Kiso forests (tightly restricted by Owari in era). Rooms: one long board sleeping platform, big central fire.
  Items: long irori, big pot, felling axes (yoki), two-man ripsaw (ōga), crosscut saws, log hooks (tobi), wedges, rope
  coils, millet and dried-radish sacks, mino, kasa, straw boots.
- **Woodcutter's family house (kikori no ie)**: as the charcoal-burner's house, with axes, wedges and firewood bundles
  (maki) in place of charcoal bales.
- **Wood-turner's forest hut (kiji-shi no koya)**: itinerant bowl-turners with forest rights from Kimigahata (Ōmi),
  moving valley to valley. Rooms: hut + open work area. Items: strap-driven lathe (rokuro), bowl blanks, rough-turned
  bowls in stacks, adzes, turning hooks, sharpening stone, irori. (Workshop side: see Crafts, wood-turner.)
- **Raftsman's riverside hut (ikada-shi no koya)**: crews floating timber down the Kiso, Tenryū, Ōi, Hozu rivers.
  Items: long poles (sao), rope coils, iron raft staples, straw cape, fire, rice and salt sacks.
- **Mountain hunter's hut (ryōshi-goya / kari-goya)**: seasonal shelter for village hunters; Tsunayoshi's 1687 gun
  registration made village guns licensed pest "scare-guns". Items: matchlock (licensed), spear, snares and traps,
  pelts drying, meat drying racks (momonji), bear-gall pouch, fire, straw bedding. Tōhoku *matagi* camps are the famous
  version `[off-map: Tōhoku]`.

### Rural: fishing, coast and salt

- **Poor fisherman's hut (ryōshi no koya)**: hired net hand or small line fisher. Board walls, boards weighted with
  stones or thatch. Rooms: doma (nets live here) + board room. Items: nets on pegs, net needles (amibari), wooden or
  gourd floats, stone or clay sinkers, oar (ro), lines on frames, fish baskets (biku), salted-fish tub, drying rack by
  the door, irori, mushiro, small Ebisu shelf.
- **Diver's beach fire hut (ama-goya)**: round or square beach hut where women divers warm up; some families lived in
  similar huts. Items: central fire, straw mats, wooden tub float (iso-oke), abalone chisel (isonomi), rope, head
  cloth, shellfish baskets. `[off-map: Shima / Ise coast; also Bōsō in Kantō]`
- **Salt-field labourer's hut (hama-ko no ie)**: workers raking and hauling brine; near Edo the Gyōtoku fields. Rooms:
  doma + board room. Items: sand rakes, shoulder buckets (ninai-oke) and yoke, straw salt bags (kamasu), wooden salt
  tubs, sand-levelling board, irori, straw bedding. (Boiling shed: Rural industry.)
- **Nori farmer's cottage (nori-shi no ie)**: seaweed growers on Edo Bay (Shinagawa, Ōmori). Items: reed drying screens
  (nori-su), drying frames outside, chopping board and knife, tubs, bundles of brush poles (hibi), board shelves of
  dried sheets. (verify start date: Shinagawa nori farming c. Genroku–Kyōhō)
- **Seasonal fishing-camp shed (bangoya)**: crew sleeps here during a run (sardine, bonito). Items: long sleeping
  board, fire, net piles, crew's straw bedding, pots, sake barrel.
- **Boat dwelling (ebune / ie-bune)**: families living aboard small boats in the Seto Inland Sea. Items: rush-mat cabin
  roof, clay stove on board, bedding, nets, water jar. `[off-map: Seto Inland Sea]`

### Rural: highway and post-town poor

- **Hired horse-leader's room (mago no ie)**: driver leading other people's horses; rents a small doma room. Items:
  straw horseshoes (umagutsu) in bundles, halter rope, whip, driver's lantern, mino, kasa, straw bedding.
- **Porters' bunkroom (ninsoku-beya / kumosuke-beya)**: shared sleeping hall for road porters and palanquin bearers at
  a post town (overlaps the toiyaba, Government). Rooms: earth doma + long board platform. Items: long sleeping
  platform, shared quilts, carrying poles, parked palanquin (kago), heaps of sandals, dice and bowl, sake jug, pipes.
- **River porters' row (kawagoshi ninsoku nagaya)**: men who carried travellers over the unbridged Ōi River (Shimada /
  Kanaya, Tōkaidō). Items: carrying platforms (rendai) stacked outside, loincloths drying, ropes, crossing-ticket board
  (kawa-fuda), sake, straw bedding.

### Urban: Edo, Kyoto, Osaka, castle towns

- **Edo back-alley single unit (ura-nagaya, kushaku-niken)**: the classic 9-shaku × 2-ken tenement, about 3 m wide
  incl. doma; peddlers, craftsmen, day labourers. Rooms: 1-tsubo doma at the door with kamado and sink, one 4.5- or
  6-mat room, no back door. Tatami plausible but not certain for the cheapest units (verify; boards + goza fallback).
  Items: one-hole kamado, water jar, sink board, one shelf, folded bedding behind a low screen (makura-byōbu), wicker
  trunk (kōri), andon, small hibachi, cheap bowls, the tenant's trade tools (variants below). [Fukagawa Edo Museum,
  c.1840 reconstruction] `[survivors late]`
- **Edo back-alley two-room unit (ura-nagaya, niken)**: craftsman family: doma + 4.5 mat + 6 mat, small back yard.
  Items: as single unit plus small tansu, Buddhist shelf, clothes rack (ikō), more bedding.
- **Back-to-back ridge-split tenement (mune-wari nagaya)**: row split along the ridge so units face both ways, no
  through-draught or back window; the cheapest urban housing. Items: as single unit.
- **Ura-nagaya occupant variants (dressing sets for the same shell)**: peddler (bote-furi): shoulder pole, two baskets,
  steelyard (sao-bakari), measure box (masu) · carpenter: toolbox (dōgubako), saws, planes, ink line (sumitsubo),
  square (sashigane) · plasterer: trowels (kote), mortar board, straw fibre bundle · boatman: long pole, straw cape,
  oilcloth, rope · shamisen teacher: shamisen, plectrum, practice books, one good kimono on a rack · seamstress /
  washerwoman: sewing box (haribako), pan iron (hinoshi), washing tubs, drying pole · fortune-teller: divination
  sticks (zeichiku), paper lantern sign, low desk · palanquin bearer / porter: shoulder pads, carrying pole, sandals ·
  town fireman (machi-bikeshi, Edo 1720, in era): fire hook (tobiguchi), padded fire coat (hikeshi-banten) ·
  paper-waste collector: back basket, bamboo tongs, sorted paper bundles · vacant unit: bare.
- **Shared alley facilities of an ura-nagaya court** (site, not a building): shared well, shared toilet with
  half-height doors, rubbish pit (gomi-tame), small Inari shrine, washing and drying poles, potted plants on the drain
  board.
- **Kyoto back-alley row (roji / zushi nagaya)**: rows reached by a narrow passage through a street house. Rooms: earth
  kitchen strip with Kyoto stove (kudo), one or two tatami rooms. Items: kudo, water jar, Atago fire-charm paper
  ("hi-no-yōjin") by the stove, shared well, sink, bedding, small Buddhist shelf. Nishijin home-weavers lived here
  (looms: Crafts, textiles).
- **Osaka back-alley row, rented bare (ura-nagaya, hadaka-gashi)**: the tenant brought his own tatami, sliding doors,
  fittings; an empty unit is a bare frame. Items: as Edo, with multi-hole Osaka stove (hettsui), tenant's own tatami
  and fusuma. [Osaka Museum of Housing and Living, c.1830s] (verify the hadaka-gashi detail)
- **Castle-town backstreet row (jōkamachi no ura-nagaya)**: the same tenements in a provincial castle town. Items: as
  Edo ura-nagaya.
- **Fire-ruin shack (yake-ato no kari-goya)**: board-and-mat hut on the ashes after a big city fire, lived in for weeks
  or months. Items: charred posts reused, reed screens (yoshizu), salvaged pot and kettle, scorched chest, straw bags of
  relief rice, bedding bundle.
- **Rōnin's rented room (rōnin no nagaya)**: masterless samurai in a tenement, earning by teaching or piecework. Items:
  one or two swords on a simple rack, umbrella frames and oiled paper (attested poor-samurai side job; the rōnin
  cliché is later fiction), books, go board, writing box, sparse bedding.

### Marginalised communities (neutral, historical)

Housing mostly looked like other poor or middling homes of the region; the difference is location, duties and tools.

- **Kawata (eta) village house (kawata-mura no ie)**: status-bound communities with hereditary duties (leather and hide
  work, drum-making, some policing and execution-ground work); many also farmed; villages often on riverbanks or
  marginal land. Rooms: as a poor or middle farmhouse of the region. Items: farm tools, leather-soled sandal (setta)
  making and repair kit, leather offcuts, drum hoops or heads, straw sandals, rope, bamboo; hide drying frames outside
  (tannery: Crafts, leather).
- **Hinin hut (hinin-goya)**: groups under a hut-boss (koya-gashira), born into or fallen into the status; duties incl.
  sweeping, prison and execution assistance, licensed street performing (torioi). Rooms: one mat hut. Items: straw
  mats, straw cape, broom, alms basket, begging bowl, woven hat (amigasa), shamisen for torioi.
- **Unregistered squatters' shelter under a bridge or on a riverbank (kawara-goya / hashi-shita)**: people dropped off
  the registers (nobinin). Items: reed mats, driftwood fire, one pot, bundle, begging bowl.
- **Cremation-ground attendant's hut (onbō no ie)**: families who ran village or town cremation grounds. Items:
  firewood stacks, straw, rakes, ash jars, small Buddhist image. (verify; mention neutrally or drop)

### Hermits, ascetics and huts

- **Grass hermitage (sōan / iori)**: poet or recluse's thatched hut; in era, Bashō's Fukagawa hut from 1680 (rebuilt
  1682). Rooms: one or two small mat rooms, tiny earth kitchen. Items: low desk, inkstone and brushes, poem slips
  (tanzaku), gourd for rice, water jar, one pot, tea kettle, hanging scroll, Buddha image, travel hat and staff by the
  door.
- **Ten-foot-square hut (hōjō-an)**: Kamo no Chōmei's portable recluse hut; archetype only. Items: as sōan, plus sutra
  desk and small Amida image. `[outside 1680-1750: 1212]`
- **Mountain ascetic's hut (yamabushi no gyōja-goya)**: shugendō retreat by a falls or peak. Items: conch trumpet
  (horagai), ringed staff (shakujō), prayer beads, portable altar backpack (oi), fire-ritual hearth (goma), sutras,
  small cap (tokin).
- **Wandering carver-monk's hut**: e.g. Enkū (d. 1695), carved thousands of rough Buddhas in Mino and Hida. Items:
  chisels, adze, logs and half-carved figures, sutra box, rice pot. (Stephen's call: unique landmark?)

### Servants' and dependents' quarters inside other homes

- **Farm servants' loft (genin-beya / hōkōnin no nedoko)**: seasonal or yearly farm servants in the loft over the doma
  or by the stable. Items: straw bedding, wicker trunk, sandals, lantern, their own bowl box.
- **Merchant apprentices' loft (detchi-beya)**: boys and young clerks in the zushi-nikai over the shop. Items: shared
  futon rolled up, wooden box pillows (hako-makura), wicker trunks, lantern, practice copybooks.
- **Maids' room (jochū-beya)**: small room off the kitchen. Items: sewing box, small mirror stand, trunk, futon, one
  kimono on a peg.
- **Samurai-house lower servants' rooms (chūgen-beya / komono-beya)**: in the gatehouse (nagaya-mon); reputed gambling
  dens. Items: crest-marked coats (happi), lanterns with the lord's crest, procession luggage boxes (hasami-bako),
  spear-sheath and umbrella cases, sandals in rows, dice, sake.

## == Dwellings: lower-middle ==

### Rural: farmhouses by plan

- **Small landholder's three-room farmhouse, Kantō (honbyakushō no ie, hiroma-gata)**: registered tax-paying farmer;
  thatch, hipped roof. Rooms: big doma (kitchen + work + sometimes stable corner), hiroma (board room with irori),
  nando, front zashiki with mats or a couple of tatami at most. Items: irori with fish-shaped hook bar (yokogi),
  jizai-kagi, iron kettle (tetsubin), 2–3-hole kamado, sink, water jar, rice chest, tawara, pickle tubs
  (tsukemono-oke), miso jar, hakozen stack, kamidana, small butsudan, hand loom (izaribata), spinning wheel, andon,
  mino and kasa on pegs, threshing comb (senba-koki, new in Genroku), round straw cushions (enza), straw bedding or
  yogi in the nando. [Kitamura house, 1687, Nihon Minka-en: in-window survivor]
- **Four-room grid farmhouse (yotsuma-dori / ta-no-ji-gata)**: standard middle-farmer plan by the 18th c. in Kinai,
  spreading east. Rooms: doma + four rooms: dei, zashiki, daidokoro (irori), nando. Items: as three-room, plus small
  tokonoma-like shelf or hanging scroll in the zashiki (only if locally permitted), zabuton for guests (rare, verify),
  lacquered festival trays in a box.
- **Farmhouse with inside stable (uchi-umaya no ie)**: Kantō, Kai, Shinano; the horse lives in a doma corner. Rooms:
  doma with stable pen + three-room plan. Items: manger (kaiba-oke), fodder cutter (kaiba-giri), straw, harness, pack
  saddle, straw horseshoes, Batō Kannon or monkey charm on the stable post, manure fork, plus the three-room set.
- **Kinai farmhouse with ox (ushi-ya tsuki)**: the west ploughed with oxen more than horses. Items: ox stall in the
  niwa, plough (karasuki), yoke, nose-rope, manger, plus the four-room set.
- **Cotton-growing farmhouse, Kawachi / Settsu (momen-zukuri no ie)**: family spinning and weaving for the Osaka
  market, in era. Items: cotton gin roller (watakuri), cotton bow, spinning wheel, loom, indigo cloth bundles, dried
  sardine fertilizer bags (hoshika, from the Kantō coast), plus the four-room set.
- **Tea-grower's farmhouse (chanōka)**: Uji near Kyoto, Suruga on the Tōkaidō; tea steamed and dried at home. Items:
  paper-covered drying table over charcoal (hoiro), steaming basket (seiro), tea jars (chatsubo), tea boxes,
  winnowing trays, plus the farm set. In era: Nagatani Sōen's sencha method is 1738.
- **Flood-country farmhouse with raised storehouse (wajū no ie + mizuya)**: Mino / Owari lowlands inside ring levees;
  house on a mound, storehouse (mizuya) on a higher stone mound with food, papers, bedding, and the escape boat
  (agebune) hung under the eaves. Items: agebune, emergency rice jars, bedding chests, rope, plus the farm set.
  `[survivors late]`
- **Lakeside farmhouse with spring-water washing room (kabata no ie)**: Ōmi (Harie, Shiga), near the Nakasendō /
  Tōkaidō junction; spring water runs through a tank room beside the kitchen. Items: stone tanks, washing tubs, pots
  soaking, carp in the outer tank eating scraps, plus the farm set. `[survivors late; practice older]`
- **Separate-kitchen farmhouse (bunto / kamaya-bunri)**: main house + separate cooking building joined by a gutter
  roof; Chiba / Ibaraki in Kantō, southern Kyushu. Items: kamaya: kamado bank, water jars, firewood, pickle tubs; main
  house keeps the irori.
- **Archaic low-eaved farmhouse, Settsu / Tanba (hakogi-type)**: very low eaves, thick earth walls, dark interior;
  Hakogi house near Kobe is Japan's oldest minka. Items: standard farm set, sparse. `[outside 1680-1750: the survivor
  is c.1400s; the old form was still lived in]`
- **Dry-field farmhouse on a new-field settlement (shinden no ie)**: Musashino upland west of Edo, long strip plots
  (Santome-shinden 1694; Kyōhō new fields 1720s), in era. Rooms: three-room plan. Items: very long well rope and bucket
  (deep wells), stone quern, wheat and barley, udon board and rolling pin, flail (karasao), millet, windbreak trees
  outside; sweet potato arrives in Kantō 1735 (Aoki Kon'yō).
- **Sericulture farmhouse with rearing loft (yōsan nōka)**: silkworm trays on racks in the loft. Items: rearing trays
  (kaiko-kago), rack posts, mulberry-leaf baskets, cocoon frames (mabushi), hand-reel (zaguri). `[outside 1680-1750:
  big rearing-loft houses are late 18th–19th c.]`

### Rural: mountain, highland and snow

- **Kiso mountain-village house (itabuki ishi-oki no ie)**: boards weighted with stones, low upper floor for storage.
  Rooms: doma + irori room + back room + loft. Items: irori, tetsubin, shoiko, snowshoes (kanjiki), straw snow boots,
  tochi nuts and chestnuts drying, stone quern, bentwood boxes (magemono), bags of millet. `[survivors late]`
- **Hida farmhouse, board roof (Hida no itabuki minka)**: like Kiso, lower-pitched board roofs, big smoke-black beams.
  Items: as Kiso plus big irori frame with drying rack above (hidana), sake jug. [Hida no Sato]
- **Gasshō-zukuri house (Shirakawa-gō / Gokayama)**: steep thatch, 3–4 attic floors; extended families of up to 30–40
  under one head; attic for storage and paper-making; saltpetre (enshō) for Kaga made in pits under the floor, in era.
  Rooms: doma, big irori room (dei), butsuma, sleeping rooms, attic floors. Items: several irori, big Jōdo Shinshū
  gilded altar, attic storage bales, washi vats and screens (Gokayama), saltpetre pit, straw snow gear, mulberry
  (sericulture is later). Large ones are upper tier. `[survivors mostly 18th–19th c.; the silk-attic use is late]`
- **Honmune-zukuri (Shinano)**: huge almost-square board-roofed farmhouse with sparrow-dance gable ornament
  (suzume-odori); upper farmers on the Shinano Nakasendō. Items: as a headman's house. `[outside 1680-1750: mostly
  after 1750; the form begins in the 18th c.]` (verify)
- **Snow-country L-house (chūmon-zukuri)**: front wing holds entrance and stable so snow never blocks the door. Items:
  snow tools, snowshoes, stable set. `[off-map: Niigata, Yamagata, Akita]` `[outside 1680-1750: mostly late Edo]`
- **Nanbu L-house with horse wing (magariya)**: family and horses under one L roof. Items: stable set, big irori, horse
  altar. `[off-map: Iwate; 18th c.; WORLD_CATALOGUE says don't build]`
- **Helmet-roof silk house (kabuto-zukuri)**: roof ends cut open to light silkworm lofts. `[off-map: Yamagata, Gunma,
  Fukushima]` `[outside 1680-1750: late Edo–Meiji]`
- **Raised-ridge Kai silk house (Kōshū takahe-zukuri)**: raised central roof section for silk lofts. `[outside
  1680-1750: late Edo–Meiji]`
- **Other far regional forms**: kudo-zukuri U-roof (Saga), futamune twin-roof (Satsuma), Ryūkyū stone-walled houses,
  Ainu chise. `[off-map]`

### Rural: coast

- **Independent fisherman's house (ryōshi no ie)**: owns a boat and some gear; board or thatch, big doma for nets.
  Rooms: doma + two board rooms. Items: nets, floats, sinkers, net-mending needles, octopus pots (takotsubo), eel traps,
  oars, rods, fish-drying racks, salted-fish tubs, almanac (koyomi) for tides, Ebisu figure on the kamidana, irori,
  kamado, bedding.
- **Small salt-maker's house (shio-yaki no ie)**: family working its own small agehama salt field near Edo Bay or on
  the Tōkaidō coast. Items: brine buckets and yoke, sand rakes, salt bags, wooden salt tubs, firewood stacks. (Boiling
  shed: Rural industry.)
- **Coastal sailor's home in a port town (sendō no ie)**: crew and skippers of coastal freighters. Rooms: as a small
  machiya or nagaya. Items: rope coils, oilcloth coat, iron-bound sea chest (funa-dansu `[outside 1680-1750: mostly
  later 18th–19th c.]`), Konpira charms, bedding.

### Post towns

- **Kiso post-town house, home side (Kiso no shukuba-machiya)**: Tsumago / Narai / Magome type: stone-weighted boards,
  overhanging low upper floor (dashibari). Rooms: doma through to the back, irori room (daidokoro), back room(s), low
  upper storey for storage and sleeping; kura, stable, toilet in the back yard. Items: irori, tetsubin, kamado,
  hakozen, kamidana, butsudan, chōchin on a rack, mino and kasa, futon upstairs, bentwood boxes, combs (Yabuhara made
  combs in era) as local colour. `[survivors late]`
- **Tōkaidō post-town house (Tōkaidō no shukuba-machiya)**: deeper, tiled or board, plastered fronts (Seki-juku, Yui,
  Futagawa). Items: as Kiso without snow gear, plus fire buckets, a well in the yard. `[survivors late]`
- **Packhorse owner's house (umakata no ie)**: post-town family owing horses to the station quota, kept at the rear.
  Rooms: town house + back stable. Items: pack saddles (nigura), straw horseshoes, halters, fodder tubs, fodder cutter,
  horse bells, driver's lantern, horse charm, plus the home set.
- **Support-village farmer (sukegō-mura no ie)**: farm household liable to send men and horses to the post station.
  Same shell as the farmhouse with inside stable; flagged only because road duty justifies a horse.

### Urban townsmen (living side only)

- **Street-front row unit, home side (omote-nagaya no sumai)**: small shop at the front (see Shops), family behind.
  Rooms: one 4.5–6-mat back room, kitchen doma along one side, sleeping loft. Items: futon, small tansu, hibachi,
  butsudan, kamidana with Ebisu and Daikoku, andon, kitchen set, clothes rack.
- **Kyoto townhouse, home side (Kyō-machiya)**: long narrow "eel's bed". Rooms: tōri-niwa with hashiri-niwa kitchen
  under a smoke void (hibukuro), daidokoro (boards or tatami), naka-no-ma, oku-no-ma facing the tsubo-niwa garden,
  zushi-nikai above the front, kura at the back. Items: row of kudo stoves, well in the passage, stone sink, Atago fire
  charm, Kōjin kitchen-god shelf with small Fushimi-doll Hotei figures (verify date of that custom), tsubo-niwa lantern
  and basin, butsudan in the oku-no-ma, tansu, hanging scroll, byōbu swapped summer/winter. `[survivors late: most after
  the 1864 fire]`
- **Osaka townhouse, home side (Ōsaka machiya)**: like Kyoto's, different stove (hettsui) and fittings; many rented
  bare. Items: as Kyoto.
- **Edo townhouse, home side (Edo machiya)**: shallower than Kamigata, cantilevered eaves (dashigeta), kitchen doma at
  the side; after 1720 fire rules pushed tile roofs and plaster. Rooms: shop front (Shops), living room, kitchen, loft,
  often a small plastered fireproof room (nurigome). Items: Edo one-hole kamado plus big rice kamado, nurigome with
  chests, fire buckets, kamidana, butsudan, tansu, hibachi.
- **Castle-town townhouse (jōkamachi no machiya)**: as the Edo or Kyoto house by region, one storey, simpler.
- **Alley landlord-agent's house (ōya / iemori no ie)**: manages a tenement court for the owner: rent, residents'
  register, sells the court's night soil; sits at the alley mouth. Rooms: doma + two rooms. Items: account books,
  abacus (soroban), residents' register (ninbetsu-chō), writing box, low desk, lantern, keys.
- **Town doctor's house (machi-isha no ie)**: home plus consulting room. Items: many-drawer medicine cabinet
  (kusuri-dansu), boat-shaped herb grinder (yagen), small scales, paper medicine packets, Chinese medical books, pulse
  cushion, mortar and pestle.
- **Writing-school teacher's house (terakoya no sumai)**: the school was the teacher's main room (see Civic,
  terakoya). Items: many small desks (tsukue), inkstones, brushes, practice copybooks (ōraimono), blackened practice
  sheets, bookshelves, abacus.
- **Arts teacher's house (o-shishō no ie)**: shamisen, koto, dance or flower teacher. Items: instruments, music books,
  best kimono on a rack, hibachi, tea things.
- **Retirement cottage (inkyo-ya / hanare)**: detached small house for the retired head of a townsman or farm family
  (rural version the same). Items: tea kettle, books, go board, pipe tray (tabako-bon), small garden view.

### Low-rank samurai and part-samurai

- **Foot-soldier row house (ashigaru nagaya / kumi-yashiki)**: rows of units for a domain's foot soldiers, each with a
  tiny front garden and vegetable plot. Rooms: doma with kamado, one 6-mat and one 4.5-mat room. Items: lacquered
  issue hat (jingasa), crest-marked coat, wooden practice sword, a spear only if individually issued (mostly the
  armoury held them), side-job gear (umbrella or lantern frames, insect cages, kite paper), vegetable tools, kamidana,
  butsudan, andon. [Hikone ashigaru houses, on the Nakasendō, survive]
- **Edo low shogunal retainer's house (gokenin no ie, kumi-yashiki)**: small detached houses in a block granted to a
  unit (e.g. Okachimachi). Items: swords on a rack, hakama and crested coat on a rack, writing desk, side-job gear
  (potted plants, umbrellas), kamidana, butsudan.
- **Town-police officer's house, Edo (dōshin no ie, Hatchōbori)**: plot of about 100 tsubo, often part-rented to
  doctors or teachers. Items: truncheon (jitte) and cord kept at home, crested short coat, sword rack, writing box,
  lantern. (Their office: Government, magistrate.)
- **Lower samurai's house in a castle town (kachi / heishi no ie)**: small detached house, board fence, simple gate.
  Rooms: small genkan (no shikidai), 3–4 tatami rooms, kitchen doma, garden. Items: sword rack (katana-kake), armour
  chest (yoroi-bitsu), spear on hooks over the entrance, bow, writing desk, books, butsudan, kamidana, hibachi, andon,
  crested screen (tsuitate) in the entrance.
- **Farmer-samurai house (gōshi / Hachiōji sennin-dōshin no ie)**: part-time warriors who farmed; the Hachiōji
  "Thousand Men" guarded Nikkō in shifts. Farmhouse shell with a formal shikidai step. Items: farm set plus armour
  chest, spear, matchlock, formal kamishimo on a rack. [Edo-Tokyo Open-Air Museum kumigashira house] `[survivors late]`

### Religious families living apart

- **Shrine-priest family house (shake)**: hereditary priest families near big shrines; Kamigamo shake-machi (north
  Kyoto) is the model: earth walls, gates, a stream through each garden for purification. Items: court-style cap
  (eboshi) and white robe on a rack, paper streamers (gohei) and cutting knife, offering stands (sanbō), sakaki
  branches, prayer texts (norito), household shrine, ritual calendar. Senior houses are upper tier. `[survivors mostly
  late Edo]`
- **Village farmer-priest's house (kannushi-nōka)**: village shrine kept by a farmer family. Items: farmhouse set plus
  ritual robe, gohei, offering stands, drum, shrine keys.
- **Mountain-cult guide's house (oshi / sendōshi no ie)**: guides and hosts for Fuji (Fujiyoshida) or Ōyama (Sagami,
  near the Tōkaidō, hugely popular with Edo) pilgrims; home, pilgrim lodging and prayer room in one (lodging side: see
  Lodging, shukubō / oshi lodging). Items: altar with the mountain-deity scroll, charm stacks and printing blocks,
  pilgrim registers, white pilgrim clothes, bells, staffs.
- **Village mountain-ascetic household (sato-yamabushi no ie)**: shugen practitioners living in villages doing prayers
  and exorcisms. Items: conch, portable altar, goma hearth in a prayer room, charms, prayer beads, staff.

## == Dwellings: upper ==

### Rural elite

- **Village headman's house, Kantō (nanushi no ie)**: big thatch, board gatehouse (nagaya-mon), formal entrance with
  shikidai and a raised guest room (jōdan-no-ma), by permission, for receiving officials. Rooms: huge doma with stove
  bank, hiroma, daidokoro, several tatami rooms, formal zashiki with tokonoma, village-business room, kura behind.
  Items: large irori, 3–5-hole kamado bank, stacks of hakozen and lacquered guest trays, nagamochi chests, tansu, big
  butsudan, kamidana, byōbu, hanging scroll, vase, hibachi, crested lanterns, fire buckets, rice measures (masu),
  steelyard, village registers and tax ledgers in chests, seal box, writing desk. [Yoshino house, Edo-Tokyo Open-Air
  Museum; WORLD_CATALOGUE T29] `[survivors late]`
- **Kinai village headman's house (shōya no ie)**: thatch main roof with tiled lower roofs, white plaster, huge
  earth-floored kitchen with a row of stoves. Items: as the Kantō headman, stoves called kudo / hettsui. [Yoshimura
  house, Habikino: early Edo, in window]
- **Great headman over many villages (ōjōya no ie)**: bigger, with an office wing. Items: as headman, plus document
  chests and a visiting-officials' suite.
- **Hereditary intendant's family house (daikan-ke)**: e.g. Egawa at Nirayama, Izu; office side is a jinya
  (Government); family rooms here. Items: as headman plus weapons (spears, armour), Chinese books. [Egawa house: early
  Edo core]
- **Wealthy farmer-entrepreneur's compound (gōnō no ie)**: landlord who also brewed sake or soy, lent money, let land.
  Main house, several kura, brewery (Food: brewing), tenant cottages nearby. Items: account ledgers (daifukuchō), money
  chests (senryōbako), abacus, scales, fine lacquer, tea-ceremony things, haikai poetry books (village poetry circles
  in era), go board, tansu rows.
- **Net-boss house (amimoto no ie)**: owner of big sardine seines on the Kujūkuri coast, dozens of hands. Rooms: big
  thatch house, huge doma, rooms for hired men. Items: net stores, hoshika bags, ledgers, big stove bank, many trays and
  bowls for crews, Ebisu shrine. [Sakuta house, late 17th c., Nihon Minka-en: in window]
- **Salt-field owner's house (hamadanushi no ie)**: owner of salt fields and boiling sheds. Items: ledgers, salt
  samples, the headman set. `[off-map for the big ones: Akō and Seto; small version possible at Gyōtoku]`
- **Horse-dealer's house (bakurō no ie)**: dealer with several stables and a yard; some doubled as horse inns. Items:
  stable set in quantity, halters and bridles on racks, horse charms, ledgers. [Suzuki house, Nihon Minka-en: later
  horse-inn example] `[survivors late]`
- **Honjin / toiya family private rooms (honjin-ke no oku)**: family's own rooms behind a post-station inn or office
  (inn: Lodging; office: Government). Items: the headman set.
- **Large gasshō and honmune houses**: see Rural: mountain; the biggest belong in this tier. (Pointer, not counted.)

### Urban merchant elite

- **Great merchant's residence (ōdana no oku)**: family quarters behind or beside a big shop (Mitsui, Kōnoike,
  Sumitomo type); plain outside, rich materials inside ("hidden luxury"). Rooms: many tatami rooms, oku-zashiki on a
  garden, family altar room, tea room, several kura, servants' wing, kitchen with big stove bank. Items: rows of tansu,
  byōbu, hanging scrolls, flower vases, tea utensils (kettle, water jar, caddy, bowls), incense set, koto and shamisen,
  bookshelves, go and shōgi boards, lacquer trays and nested boxes (jūbako), hibachi, andon and candle stands,
  tabako-bon. (Houses of this rank mostly lost.)
- **Wealthy townsman's landlord house (jinushi / iemochi no ie)**: owns the plot and the tenements behind. Items: as
  merchant but smaller; ledgers, rent books.
- **Merchant's suburban villa (bessō)**: Mukōjima (Edo), Higashiyama (Kyoto), Osaka outskirts; sukiya rooms, big garden,
  tea hut. Items: tea set, garden-view rooms, sake sets, poetry things, fishing rods.
- **Tea hut (chashitsu / sōan-chashitsu)**: outbuilding of upper houses, samurai and merchant. Rooms: small mat room
  with sunken hearth (ro), crawl-in door (nijiriguchi), prep room (mizuya). Items: kettle (kama), water jar, bowls,
  whisk, tea scoop, caddy, one scroll, one flower; stone basin (tsukubai) and waiting bench outside.

### Samurai

- **Mid-rank samurai house in a castle town (chūkyū bushi no yashiki)**: plot with roofed gate (yakui-mon or
  kabuki-mon), front garden, main house, kura, maybe a stable. Rooms: genkan with shikidai, formal zashiki with tokonoma
  and built-in desk (tsuke-shoin), family rooms, kitchen doma, maids' room, servants' room. Items: sword racks, armour
  chest and armour, spears on hooks over the entrance (yari-kake), bow and quiver, writing desk, bookcase, crested
  entrance screen, byōbu, scrolls, hibachi, pipe tray, crested lacquer trays, kamishimo on a rack, butsudan, kamidana,
  horse gear if mounted rank. [Hikone, Hagi, Kakunodate survivors] `[survivors mixed]`
- **Shogun's bannerman's house, Edo (hatamoto yashiki)**: 300 to several thousand tsubo, gatehouse (nagaya-mon) housing
  retainers, main house with an office room, stable, kura. Items: as mid-rank plus horse gear, gate lanterns with crest,
  retainers' rooms.
- **Senior retainer's mansion (karō yashiki)**: big houses near the castle with own nagaya-mon, retainers, kura,
  garden. Items: as bannerman, larger; family armour display, many byōbu, several scrolls.
- **Daimyo's main Edo residence (kami-yashiki)**: lord in his Edo years, wife and heir always. Rooms: omote (formal
  halls: Government), oku (lord's private rooms) and ōoku-like women's quarters, kitchens, perimeter of barrack nagaya.
  Items (home side): lacquered bridal furniture sets, shell-game boxes (kaiōke), painted fusuma, byōbu, koto, incense
  sets, hibachi, silk bedding, mirror stands, many attendants' rooms. [Kaga mansion Akamon is 1827] `[survivors late]`
- **Daimyo's secondary Edo residences (naka-yashiki / shimo-yashiki)**: for the heir or retired lord, plus a suburban
  villa-warehouse-refuge. Items: as kami-yashiki, lighter; stroll garden, tea hut.
- **Retainers' barracks inside a daimyo mansion (edo-zume nagaya)**: long two-storey rows round the mansion edge for men
  on Edo duty, 2–3 to a room, many cooking for themselves. Items: futon, trunks, sword rack, writing box (letters and
  diaries home), cheap sake, go and shōgi, small stove, kettle, rice bag. [texture from Sakai Banshirō's diary,
  `outside 1680-1750: 1860`]
- **Domain warehouse-residence in Osaka (kura-yashiki)**: rice warehouses: Government, tax and stores; the resident
  officer's family rooms are the mid-rank samurai set. (Pointer, not counted.)
- **Daimyo's castle palace (honmaru goten)**: mostly Government / Military; only the lord's private oku rooms are home.
  (Pointer to Military, lord's palace; not counted.)

### Nobility

- **Court noble's residence, Kyoto (kuge yashiki)**: round the imperial palace; most kuge had tiny incomes and modest
  houses, a few (Konoe, Kujō) large. Rooms: gate, genkan, shoin rooms, garden. Items: court robes on racks, lacquered
  cap boxes, koto and biwa, incense-game sets, waka poetry papers and boxes, calligraphy set, go board, kemari ball for
  the families that taught it. [Reizei house, rebuilt 1790 after the Tenmei fire, `outside 1680-1750: 1790`, closest
  survivor]

### Marginalised communities: their elite

- **Kawata leader's compound (Danzaemon yashiki, Asakusa)**: hereditary head of Kantō kawata communities; large
  compound with offices and a big residence. Osaka's Watanabe-mura had rich leather dealers with big townhouses.
  Items: as a headman's house plus registers and leather goods.

## == Dwellings: outbuildings (all tiers) ==

- **Earth-walled plastered storehouse (dozō / kura)**: fireproof; tier 2–3. Items: nagamochi, lidded chests, rice
  bales, jars, boxed lacquer tray sets, bagged byōbu, boxed dolls, armour boxes, seed rice, documents.
- **Board storehouse (itagura)**: rural, cheaper; tier 1–2. Items: grain bales, straw bags, tools, seed.
- **Log storehouse (azekura)**: old style, rare in homes by 1730. (verify, probably drop)
- **Rice storehouse (kome-gura)**: kura for tax and seed rice at headman houses. Items: bales, measuring masu,
  strickle (tokaki), ledgers.
- **Fireproof inner room (nurigome)**: Edo; plastered room inside the house. Items: chests, ledgers, money box.
- **Dug cellar (ana-gura / tsuchi-gura)**: pit for root vegetables, sometimes under the floor. Items: sweet potatoes
  (post-1735 in Kantō), radishes, jars.
- **Barn / work shed (naya / sagyō-goya)**: threshing and straw work. Items: threshing comb (senba-koki), winnowing
  machine (tōmi, late 17th c. Kinai), grain sieve (mangoku-dōshi, 18th c.), winnowing basket (mi), treadle mortar
  (karausu), rope and mat looms, straw piles.
- **Pounding shed (tsukiya / usu-ya)**: shed for the treadle mortar. Items: karausu, mortar, pestles, grain.
- **Detached stable (umaya)**: Items: manger, straw, harness, pack saddle, fodder cutter, straw horseshoes, horse charm,
  manure fork.
- **Ox shed (ushi-goya)**: western version. Items: manger, plough, yoke, nose-rope.
- **Woodshed (maki-goya)**: Items: split firewood stacks, kindling, axes, chopping block. (Firewood also stacks under
  eaves.)
- **Ash shed (haiya)**: small fire-safe shed for hearth ash kept as fertilizer; Kinki and Chūbu. (verify)
- **Manure shed and pits (koe-goya / koetsubo)**: Items: night-soil vats, compost, shoulder buckets (koe-oke), dipper.
- **Toilet (setchin / kawaya)**: rural outhouse over a jar or pit, often by the gate or the manure pit; urban shared
  toilets with half doors; upper houses have indoor guest toilets. Items: wooden lid, wiping sticks or recycled paper
  (Asakusa-gami in Edo), water bucket.
- **Bath hut (furoba / yudono)**: poor families washed in a yard tub (gyōzui) or used town bathhouses; middle and upper
  rural homes had a tub bath. Kamigata iron-bottom tub (goemon-buro) vs Edo tub with iron firepipe (teppō-buro) per
  *Morisada Mankō* `[late Edo source]` (verify for 1730); steam baths (mushi-buro) are older. Items: wooden tub,
  firebox, buckets, dipper, stool, washcloths, rice-bran bag (nuka-bukuro).
- **Drying shed or eaves (hoshi-ba)**: persimmons (hoshigaki), tobacco leaves, radishes, noodles. Items: strings of
  fruit, bamboo poles, racks.
- **Net shed (ami-goya)**: Items: nets, floats, sinkers, tar or persimmon-tannin tubs for net dyeing.
- **Boat shed (funa-goya)**: family's small boat and oars. (Commercial version: see Crafts, boatyard.)
- **Silkworm shed (sanshitsu)**: `[outside 1680-1750: late]`
- **Hen coop (tori-goya)**: a few chickens, mostly eggs to sell and for time-telling. (verify: egg-eating rises later)
- **Roofed well (ido-ya)**: pulley well with bucket, or lever well (hanetsurube). (Same as Civic, pulley well and lever
  well: merged there, not counted.)
- **Separate kitchen (kamaya)**: see separate-kitchen farmhouse. (Pointer, not counted.)
- **Flood storehouse (mizuya)**: see flood-country farmhouse. (Pointer, not counted.)
- **Spring-water washing room (kabata)**: see Ōmi lakeside farmhouse. (Pointer, not counted.)
- **Gatehouse with rooms (nagaya-mon)**: headman (board) and samurai (plaster) houses; servants' rooms and storage.
  (Servants' set: chūgen-beya above.)
- **Retirement cottage (inkyo-ya)**: see Urban townsmen; rural version the same. (Pointer, not counted.)
- **Household shrine in the yard (yashiki-gami / Inari hokora)**: tiny shrine in a corner of the plot (site object).
  (Same as Shinto, house-plot shrine: merged there, not counted.)
- **Field hut (nora-goya)**: tool and rest hut at distant fields. Items: hoe, bucket, straw mat, water jar. (Same as
  Civic, field hut: merged there, not counted.)

**A's date traps for 1730:** tetsubin and tansu are spreading (fine for tier 2–3); zabuton for commoners uncertain;
candles expensive; cotton futon scarce in poor rural homes; no glass; no side-handled teapot (verify); sweet potato
only in Kantō from 1735.

## == Shops and retail ==

Source: B §10 (plus the shop-front kit from B §0.1). Shop side only; the family behind the shop is Dwellings, urban
townsmen. Food shops are under Food and drink; maker-and-seller shops are under their craft.

**Standard shop-front kit (every `town shop`; entries list only what is trade-specific):** noren at the door, kanban
signboard (hanging, standing, or shaped like the goods), lattice front (kōshi) or removable shutters (shitomido /
amado), fold-down street bench (battari-shōgi), raised mise-no-ma with a counter area (chōba) behind a low lattice
screen (chōba-gōshi), low account desk, abacus (soroban), ledgers hung on a nail (daifukuchō), inkstone and brush,
customers' tobacco tray (tabako-bon), cushions (zabuton), brazier (hibachi), balance scales (tenbin) or steelyard
(sao-bakari), fire buckets (tenshu-oke) stacked outside, fireproof kura at the back for stock. Big merchants add
clerks' desks, a staircase chest (kaidan-dansu), and the shop mark on everything. Floor: a doma passage (tōri-niwa) and
a raised shop room (mise-no-ma) at the front.

- **General household goods (ara-mono-ya, yorozu-ya)**: brooms, buckets, pots, sieves, mats, straw goods. Items: goods
  hung from the eaves and piled on the doma, brooms in bundles, stacked tubs.
- **Ironmonger (kanamono-ya)**: tools, nails, pots, locks, knives. Items: tools on the wall, nails in boxes by size,
  iron pots stacked, scales.
- **Ceramics shop (setomono-ya)**: "Seto-mono" was the eastern word for ceramics. Items: bowls and dishes in
  straw-packed stacks, shelves, packing corner with straw.
- **Lacquerware shop (nurimono-ya)**: bowls, trays, boxes. Items: lacquered stacks on shelves, display trays, boxes.
- **Silk draper (gofuku-dana)**: Echigoya (Mitsui) in Edo sold at fixed cash prices and cut to any length from 1683
  (in era). Big shop; long raised tatami sales floor with clerks. Items: rolled silk bolts (tan-mono), sample books,
  cloth rule (kujira-jaku), hand shears, room for high-ranking customers, rows of clerks' desks, shop-boy corps (detchi)
  at the front, clothes-rack display (ikō). (Family side: Dwellings, great merchant's residence; boys: apprentices'
  loft.)
- **Cotton and hemp cloth shop (futomono-dana)**: plain "thick goods" for commoners. Items: as draper, cheaper.
- **Old-clothes shop (furugi-ya)**: most commoners bought used clothing; Edo's Tomizawa-chō and Yanagihara embankment
  stalls. Items: garments on poles and bamboo racks, folded piles, patching corner.
- **Haberdasher (komamono-ya)**: combs, hairpins, pouches, purses, netsuke, towels (tenugui), thread, needles. Items:
  small goods in shallow display boxes and on boards, hairpins in a straw stand.
- **Paper and stationery shop (kami-ya, fude-sumi-ya)**: paper, brushes, ink, inkstones, envelopes. Items: paper reams,
  brush racks, ink sticks in boxes.
- **Lamp-oil shop (abura-ya)**: rapeseed and fish oil sold by measure into customers' jugs. Items: oil casks, ladles
  and funnels, measures, oil jugs, rush-pith lamp wicks (tōshin).
- **Wick seller (tōshin-ya)**: rush-pith wicks. (B: merge with oil shop.)
- **Candle shop (rōsoku-ya)**: retail side of the candle maker (Crafts). Items: candles by size in boxes, candle
  stands.
- **Charcoal and firewood dealer (sumi-ya, takigi-ya)**: town shop with a yard. Items: stacked charcoal bales
  (sumi-dawara), firewood bundles, scales, charcoal saw, sifter.
- **Tobacco shop (tabako-ya)**: cut tobacco (kizami), hand-cut with the Sakai knife from pressed leaf. Items: leaf
  bales, cutting board with a clamp and the big knife, paper packets, pipes on display.
- **Pipe shop (kiseru-ya)**: retail side of the pipe maker (Crafts, metal). Items: pipes on racks, pouches.
- **Umbrella, clog, sandal and hat shop (kasa-ya, geta-ya, zōri-ya)**: retail side of the makers (Crafts). Items: goods
  hung and stacked at the front.
- **Travel-goods shop (tabi-dōgu-ya)**: post towns: sandals, straw raincoats, hats, pouches, pack frames, maps and
  guidebooks, lanterns. Items: straw sandals hung in bunches, mino and kasa, travel pillows, guidebook stack.
- **Souvenir and local-specialty shop (meibutsu-ya)**: each post town's famous product (Odawara uirō, Hakone woodcraft,
  Arimatsu shibori, Kuwana clams). Items: the product on a front stand, a sign naming the meibutsu.
- **Toy and doll shops**: retail side of the toy and doll makers (Crafts, fine). Seasonal doll markets (hina-ichi) are
  stalls.
- **Plant nursery (ueki-ya)**: Edo's Somei village nurseries; Itō Ihei's azalea book 1695 (in era). `rural` / town-edge
  yard. Items: potted plants on stepped stands, bonsai, trees in straw root-balls, watering buckets, shed.
- **Goldfish seller (kingyo-ya)**: Kōriyama goldfish breeding from 1724 (in era). Shop or `itinerant`. Items: tubs and
  ceramic basins, shallow ponds, dip nets.
- **Bird shop (kotori-ya)**: songbirds (bush warbler) in cages. Town shop. Items: stacked bamboo cages, feed boxes.
- **Insect seller (mushi-uri)**: singing insects in tiny cages. `itinerant`. (verify: mostly mid–late Edo)
- **Flower seller (hana-ya)**: altar and grave flowers, mostly by peddlers; shops near temples. `stall`.
- **Sword and arms dealer (tōken-ya, katana-ya)**: blades, fittings, armour. Town shop. Items: swords on racks, fittings
  in boxes, appraisal papers.
- **Second-hand goods dealer (furu-dōgu-ya)**: used furniture, tools, household goods. Town shop. Items: piles of
  assorted goods.
- **Old-metal dealer (furugane-ya)**: scrap iron and copper bought from peddlers. Town yard. Items: scrap heaps,
  scales.
- **Fertilizer dealer (hoshika-don'ya, shime-kasu)**: dried sardine fertilizer (hoshika) and oil-cake (abura-kasu,
  shime-kasu) for cotton and rice. Town shop plus kura. Items: straw bags of dried sardines, pressed oil-cake discs,
  scales.
- **Market stalls (ichi, rokusai-ichi, toshi-no-ichi)**: periodic markets (six a month in many towns) and year-end
  markets. `stall` kit: straw mats on the ground, trestle boards, small roofs, baskets, scales.
- **Street peddlers (furi-uri, bote-furi)**: much daily retail came by shoulder pole: fish, vegetables, tofu, nattō,
  water, mosquito nets, goldfish, brooms. Not a building; a prop kit: shoulder pole, baskets or tubs, a trade call.
  (Their home: Dwellings, ura-nagaya peddler variant.)
- **Tea, sake, soy, miso, fish, vegetables, rice, dried goods, salt shops**: see Food and drink. (Cross-reference, not
  counted.)

## == Food and drink ==

Source: B §7. Shop-front entries take the standard shop-front kit (see Shops).

### Brewing and fermenting

- **Sake brewery (saka-gura)**: winter-brewed sake (kan-zukuri); Itami, Ikeda, Nada, Fushimi. Complex of kura round a
  yard. `site` / town complex; doma inside, raised mezzanines. Items: rice-polishing mortars (foot-driven or water mill),
  big rice steamer (koshiki) on a cauldron, insulated koji room (kōji-muro) with koji trays (kōji-buta), starter tubs
  (moto-oke), huge fermentation tubs (ō-oke) with ladders and walkways, stirring poles (kai), press box (fune) with cloth
  bags and a stone-weighted lever press (tenbin-shibori), well, casks (taru), cedar ball (sugidama) under the eaves.
  [WORLD_CATALOGUE T25] (Also the gōnō compound's brewery: Dwellings.)
- **Sake shop (saka-ya)**: retail by measure into customers' flasks; drinking in the shop grew into the izakaya during
  the 18th c. Town shop; doma. Items: casks on a rack, a tap, wooden measures (masu), tin and ceramic flasks (tokkuri),
  ladle, a crate or cask to sit on, sugidama or sake-brand kanban.
- **Shōchū still (shōchū-gura)**: distils sake lees (kasutori) or, in Kyushu, sweet potato. `rural` or brewery-side.
  Items: helmet-type pot still (kabuto-gama), cooling-water tub, fuel, jars. (B: regional; may cut.)
- **Mirin and sweet-sake maker (mirin-ya)**: fortified sweet rice liquor, also drunk. Items: as brewery on a small
  scale, shōchū casks. (verify how widespread in 1730)
- **Koji maker (kōji-ya)**: grows koji on rice or barley, sells to miso, soy and home brewers. Town workshop; doma plus
  an underground or thick-walled warm room. Items: earth-walled cellar (kōji-muro), stacked wooden trays (kōji-buta),
  straw mat covers, steamer, spreading table.
- **Soy-sauce brewery (shōyu-gura)**: Noda, Chōshi, Yuasa; Tatsuno light soy from 1666. `site` / town complex; doma.
  Items: wheat roasting pan, bean steamer, koji trays, huge cedar mash vats (moromi-oke) with walkways, mixing poles,
  press box with cloth bags and lever press, heating cauldron (hi-ire), casks.
- **Miso maker (miso-ya)**: town workshop and shop; doma. Items: bean steamer, mortar or foot-masher for beans, koji
  trays, tall miso vats with stones on the lids, wooden spatula, tubs of miso at the counter scooped by weight.
- **Vinegar brewery (su-ya)**: rice vinegar; sake-lees vinegar (Mitsukan type) is `[outside 1680-1750: 1804]`. Town
  workshop; doma. Items: fermenting vats, casks, ladles, jars.
- **Pickle maker and shop (tsukemono-ya)**: takuan, salt pickles, miso pickles. Town shop; doma. Items: pickle vats with
  heavy stones on lids, bran beds, radishes drying on racks outside, tubs at the counter.

### Milling and staples

- **Water mill (suisha-goya)**: polishes and grinds rice, grain, buckwheat; later also oil seed and incense powder.
  `site` on a stream; wheel plus hut; doma. Items: undershot or overshot wheel, cam shaft lifting pestles (kine) into
  pounding mortars (usu), stone grinding mill (ishi-usu), sieves (furui), sacks and straw bags, sluice gate.
  [WORLD_CATALOGUE T38]
- **Rice polisher (tsuki-gome-ya)**: polishes brown rice by treadle mortar (fumi-usu / kara-usu) in town; Edo's
  polishers also went door to door. Town workshop; doma. Items: several treadle mortars in a row, sieves, bran baskets,
  rice bales.
- **Flour shop (kona-ya)**: wheat, buckwheat, bean flours (kinako). Town shop; doma. Items: hand quern (ishi-usu),
  sieves, flour bins, scoop and measure.
- **Tofu shop (tōfu-ya)**: opens early; doma, wet. Items: stone hand mill (ishi-usu) for soaked beans, big cauldron on
  a kamado, straining bag and wooden press, coagulant (nigari), holed wooden forming boxes, water tanks of tofu blocks,
  frying pot for abura-age and ganmodoki. (*Tōfu hyakuchin* is 1782, but the shop is old.)
- **Konnyaku maker (konnyaku-ya)**: devil's-tongue jelly. Town or `rural`; doma. Items: grating board, cauldron, lime
  water, forming trays, water tanks.
- **Tofu-skin maker (yuba-ya)**: Kyoto and Nikkō. Items: shallow heated trays of soy milk, bamboo lifting skewers,
  drying rack. (B: niche; merge with tofu.)
- **Wheat-gluten maker (fu-ya)**: raw and baked fu for temple cooking. Town workshop. Items: kneading tub in water,
  steamer, baking plates. (Niche.)
- **Nattō maker (nattō-ya)**: fermented beans in straw, sold on Edo streets at dawn. Town workshop; warm room. Items:
  bean steamer, straw wrappers (wara-zuto), warm cellar.
- **Hand-stretched noodle maker (sōmen-ya)**: dried thin noodles (Miwa, Banshū), made in winter. `rural` workshop with
  a yard. Items: kneading tubs, oiled coils in tubs, stretching poles in frames (hashi), long drying racks with curtains
  of noodles, cutting board, straw-bundled noodles.
- **Kudzu and starch maker (kuzu-ya)**: Yoshino kudzu from roots washed repeatedly. `rural` `site` by clean water.
  Items: root-crushing mortar, row of washing tubs, settling tanks, drying boxes. (Niche.)
- **Agar maker (kanten-ya)**: freeze-dried seaweed jelly (invented 1650s at Fushimi), made in winter fields. `rural`
  `site`. Items: seaweed boiling cauldron, straining bags, trays, frost drying racks. (Niche.)

### Sweets and snacks

- **Fine confectioner (jōgashi-ya / kashi-ya)**: refined sweets for elite and gifts (e.g. Toraya, Kyoto). Town shop;
  raised, quiet, clean. Items: carved wooden moulds (kashi-gata), bean-paste pans, sugar jars, sweets on lacquered
  trays, tiered boxes, display case.
- **Cheap sweet shop (dagashi-ya, zatsugashi)**: sweets for commoners and children. Town shop. Items: jars and baskets
  of sweets, small griddle, children's toys.
- **Rice-cake and dumpling shop (mochi-ya, dango-ya)**: pounded mochi, skewered dango, seasonal cakes (sakura-mochi from
  1717, in era). Town shop or roadside; doma. Items: mortar and mallet (usu, kine), steamer, charcoal grill with
  skewers, bean-paste pots, sweet soy glaze.
- **Steamed-bun shop (manjū-ya)**: bean-paste buns. Town shop; doma. Items: steamers stacked on a cauldron, paste pots,
  buns on trays. (B: merge with mochi-ya.)
- **Rice-cracker shop (senbei-ya)**: grilled crackers, often wheat-based in period; salty rice senbei spread later
  (verify). Items: griddle irons, charcoal, jars.
- **Candy maker (ame-ya)**: starch-syrup candy (mizu-ame), pulled candy, sold by candy peddlers. Town workshop or
  `itinerant`. Items: syrup cauldron, pulling hook, cutting board. Sugar-sculpture street craft: date uncertain
  (verify).
- **Amazake shop (amazake-ya)**: hot sweet fermented rice drink; Hakone's Amazake-chaya on the old Tōkaidō is said to
  date to early Edo. Roadside tea house or `itinerant` with a pot. Items: big pot on a hearth, cups, amazake tubs.

### Eating places

- **Soba shop (soba-ya, soba-kiri)**: common in Edo by the 1700s; soba often steamed in stacked trays (seiro) rather
  than boiled. Town shop; doma kitchen, raised floor for eaters. Items: lacquered kneading bowl (kone-bachi), rolling
  board (noshi-ita) and pins (menbō), wide noodle knife (soba-kiri bōchō) and cutting guide (koma-ita), seiro steamers,
  boiling cauldron, dipping-sauce pots, buckwheat stone mill.
- **Udon and cheap bowl shop (udon-ya, kendon-ya)**: noodles in bowls, fast and cheap; kendon shops from the 1660s.
  Town shop. Items: as soba, plus bowls on a counter. (B: merge with soba.)
- **Cheap cook-shop (ichizen-meshiya, meshi-ya)**: rice, soup and a side for labourers. Town shop; doma with benches
  and a raised edge. Items: rice cauldron, soup pot, rice tub (ohitsu), bowls on trays, menu board of wood strips.
- **Cooked-food and sake shop (nimeuri-ya / niuri-sakaya)**: simmered fish and vegetables with sake; izakaya
  forerunner, early 18th c. Town shop; doma, benches, barrels as seats. Items: simmering pots (nabe), skewers, sake
  casks, flasks, dishes.
- **Tea-rice shop (Nara-chameshi-ya)**: rice cooked in tea with tofu soup; Asakusa after 1657. Town shop. Items: as
  meshiya. (B: merge.)
- **Restaurant (ryōri-jaya)**: sit-down party rooms. Town building with tatami rooms and a doma kitchen. Items:
  kitchen: multiple kamado, legged cutting boards (manaita), knives, fish tubs, live-fish tank (ikesu); rooms:
  individual tray tables (zen), lacquered bowls, sake flasks, braziers, lanterns. Grand ryōtei are `[outside
  1680-1750: late 18th c. on]`.
- **Eel shop (unagi-ya, kabayaki)**: split, grilled, soy-glazed eel; stalls in Genroku, shops multiplying later (verify:
  shops mostly c.1770s+). Town shop or stall. Items: long charcoal grill with fan (uchiwa), skewers, eel tubs and
  live-eel basket, eel-splitting board with a spike, glaze pot.
- **Sushi seller (sushi-ya)**: 1730 sushi = pressed and quick-vinegared (haya-zushi, oshi-zushi, box sushi); fermented
  nare-zushi still exists; nigiri is `[outside 1680-1750: c.1820s]`. Town shop or peddler with a box. Items: pressing
  boxes and heavy stones, rice tubs (hangiri), vinegar jar, bamboo leaves, cut fish, lacquered carrying boxes.
- **Tempura stall (tempura yatai)**: Items: oil pot on a charcoal stove, skewers, batter bowl. `[outside 1680-1750:
  stalls from c.1770s–80s]`
- **Dengaku stall or shop (dengaku-ya)**: skewered tofu or konnyaku grilled with miso. Stall or roadside shop. Items:
  charcoal grill, skewers, miso pot. Simmered oden in broth is later (verify).
- **Wild-meat shop (momonji-ya)**: boar and deer ("mountain whale") sold as winter medicine. Town shop. Items: hanging
  carcass quarters, pot, chopping block. (verify: mostly later Edo)
- **Chinese-style banquet house (shippoku)**: Items: round shared table, shared dishes. `[outside 1680-1750: Nagasaki
  style spread to Kyoto and Edo later in the 18th c.]` (verify) (B: probably cut.)
- **Food stall (yatai) family**: portable roofed stall on two poles or a shoulder-pole stand: night soba (yotaka soba),
  sushi, dengaku, amazake, summer cold water (hiyamizu-uri), barley tea (mugiyu). `stall`. Items: small roof, charcoal
  stove, pot, bowls on a shelf, lantern with the dish name.

### Tea houses (one family, many forms)

- **Roadside tea house (kake-jaya / chamise)**: open-fronted thatch or board shed on the highway or a temple approach.
  `stall` / small building; doma with benches (shōgi) covered in red felt or mats. Items: benches, kettle on a hearth or
  portable stove, tea bowls on a tray, tea caddy, dumpling grill, straw sandals for sale under the eaves, reed screen
  (yoshizu). [Kaempfer 1691–92; WORLD_CATALOGUE T18]
- **Rest-station tea house (tateba-jaya)**: bigger tea houses at official rest stops between post towns (Hatajuku on
  the Hakone road), where porters and horses changed. Roadside building; doma plus raised rooms. Items: as kake-jaya,
  plus raised tatami rooms, meal trays, horse tie posts, palanquin rack, local-specialty display.
- **Water tea house (mizu-jaya)**: tea houses at shrines, temples, city parks. Items: as kake-jaya. (B: merge.)
- **Sencha stall (Baisaō style)**: from 1735 the monk Baisaō sold brewed sencha from a portable stall in Kyoto;
  Nagatani Sōen's steamed sencha is 1738 (both in era). `stall`. Items: portable stove, small kettle, teapot for leaf
  tea, cups, bamboo carrying frame.
- **Theatre tea house (shibai-jaya)**: booked seats, meals and rests for kabuki audiences, beside a theatre. Items:
  tatami rooms, meal boxes, lanterns with theatre crests. (See Services, theatre.)
- **Sumō tea house (sumō-jaya)**: as shibai-jaya, for sumō. (B: merge.)
- **Guide tea house for the pleasure quarter (hiki-te-jaya)**: see Services, pleasure quarter.
- **Rendezvous tea house (deai-jaya)**: rooms rented by the hour. Neutral. (B: cut candidate.)
- **Tea-leaf dealer (cha-ya, cha-don'ya)**: leaf and powdered tea; Uji for the elite. Town shop. Items: big sealed tea
  jars (chatsubo), tea boxes, stone tea mill (cha-usu) for matcha, scales, sample dishes, roasting pan (hōji-nabe,
  verify), paper packets.

### Food retail (shop fronts; see also Shops)

- **Rice dealer (kome-ya)**: retail rice by measure. Town shop; doma. Items: stacked tawara, rice bins, masu, strike
  stick (tokaki), sieve, scoop.
- **Fishmonger (sakana-ya)**: town shop; doma, wet; most fish sold by peddlers (bote-furi). Items: cutting boards
  (manaita), deba knives, fish tubs and baskets (bote), live-fish tank (ikesu) or tub, salt fish, dried fish on a rack,
  shoulder pole for the rounds.
- **Fish market (uogashi, uo-ichi)**: wholesale at dawn (Edo Nihonbashi; Osaka Zakoba). Waterside `site`: open sheds,
  quay stalls. Items: boards on trestles, tubs, baskets, big knives, tally boards, boats at the quay.
- **Kamaboko maker (kamaboko-ya)**: steamed or grilled fish paste (Odawara fame is late 18th c., verify). Town
  workshop; doma. Items: stone mortar and pestle (suribachi), boards, steamers, charcoal grill, fish-scrap bin.
- **Greengrocer (yaoya, aomono-ya)**: town shop; doma. Items: baskets and shelves of vegetables, radishes, eggplant,
  scales, shoulder pole.
- **Vegetable market (yacchaba)**: wholesale greens (Kanda in Edo). `site`: sheds and stalls. (B: merge with market
  stalls.)
- **Dried-goods shop (kanbutsu-ya)**: kombu (Hokkaidō via the Kitamae ships), katsuobushi, dried fish, beans, dried
  mushrooms. Town shop plus kura. Items: bundled kombu, boxed katsuobushi, dried fish on strings, jars, scales.
- **Salt shop (shio-ya)**: salt by the straw bag. Town shop. Items: salt bags (shio-dawara), bins, measures.
- **Water seller (mizu-ya)**: in low-lying Edo (Fukagawa) good water sold by the bucket from boats. `itinerant` with a
  boat and barrels.

## == Lodging ==

Source: B §8. The official inns (honjin, waki-honjin) are C's and sit here too, merged in from C §4.3 so that all
lodging is in one place (see §4 Seams).

- **Post-town inn (hatago)**: standard inn with meals; two storeys, lattice front, rooms upstairs. Tōkaidō's 53 stations
  held thousands (WORLD_CATALOGUE T30 cites ~3,000, an 1843 figure). Distinct building; doma entrance with raised hall.
  Items: entrance doma with foot-washing tub (ashi-arai darai) and stool, step (agari-kamachi), front desk (chōba) with
  guest register (yado-chō), large kitchen with a row of kamado and a well, tatami guest rooms, andon, tobacco trays,
  braziers, folded rental bedding (yogi) and mosquito net (kaya), meal trays (zen), bath room (wooden tub: goemon-buro
  west, teppō-buro east), privy, sign-lantern outside, confraternity plaques (see kō-yado). Touts (tome-onna) pulled
  travellers in.
- **Post-town inn with serving women (meshimori hatago)**: many hatago legally employed "rice-serving women"
  (meshimori-onna), also a form of licensed post-town prostitution; the shogunate limited numbers per inn. Same
  building as a hatago; a staffing variant. Neutral. (B: cut candidate: keep the building, drop the role.)
- **Firewood-fee lodging (kichin-yado)**: cheapest lodging: travellers brought rice and paid only for firewood
  (kichin). Shared rooms; nagaya shell. Items: shared hearth and cauldron, firewood stack, straw mats, shared quilts,
  cooking-pot rental. [WORLD_CATALOGUE T18, T30]
- **Hot-spring inn (yu-yado / tōji-yado)**: Hakone's seven springs (Yumoto, Tōnosawa, Miyanoshita, Dōgashima, Sokokura,
  Kiga, Ashinoyu); Ichinoyu (Tōnosawa) from 1630. Guests stayed weeks for cures, often cooking for themselves; inns
  rented pots and sold fuel. Building: inn rooms round a bath house fed by a spring pipe. Items: indoor bath (uchiyu),
  wooden or stone tub fed by bamboo or wooden pipes, changing area with shelves, communal self-catering kitchen (rental
  pots, charcoal), guest register, long-stay rooms with bedding. One-night stays by ordinary travellers were a legal
  fight with the post towns `[outside 1680-1750: Hakone ruling 1811]`.
- **Communal hot-spring bath (soto-yu, kyōdō-yu)**: the village's public spring bath, shared by inns and locals. Small
  bath house over a pool. Items: stone- or wood-lined pool, roof, changing shelf, bucket, small shrine to the spring.
  Open-air rock pools as in modern resorts are not the typical period form.
- **Confraternity inn (kō-yado)**: inns affiliated with pilgrim or travel confraternities, signboards under the eaves; a
  hatago variant. Items: as hatago plus a row of kō plaques (kō-kanban). Naniwa-kō network is `[outside 1680-1750:
  1804]`; earlier Ise-kō affiliated inns (verify).
- **Charity lodging for pilgrims (zenkon-yado)**: farmers or temples lodging pilgrims free as merit (common on the
  Shikoku route). A farmhouse room (Dwellings) or temple room (Buddhist). (Cross-reference, not counted.)
- **Lawsuit inn (kuji-yado)**: Edo, Osaka, Kyoto inns lodging provincial litigants and helping with paperwork and court;
  guilds formed 1699 (in era); Edo had ~100, many in Bakurō-chō. Town inn. Items: as hatago, plus a writing room with
  document boxes, legal forms, scribe's desk.
- **Boat inn and boat hire (funa-yado)**: waterside houses renting pleasure boats (yakata-bune), fishing boats and gear,
  with rooms to wait, eat, drink. Waterside building with a landing. Items: moored boats, oars and poles, fishing rods,
  lanterns, raised waiting room, sake and trays.
- **Horse-dealers' inn (bakurō-yado)**: inns near horse markets for dealers and drovers, with stabling. Town inn with a
  stable yard. Items: as hatago plus tie rails, mangers, fodder store. (B: merge with commercial stable.)
- **Servants' lodging and hiring house (hito-yado)**: lodging for job seekers, run by the employment broker (Services).
  Nagaya / machiya. Items: shared rooms, register of job seekers.
- **Daimyo inn (honjin)** {from C §4.3}: official lodging of daimyo, court nobles and shogunal officials; the house of
  the station's leading family (often also toiya or headman). Ordinary travellers never lodge here. Space: formal gate
  (yakui-mon or kabuki-mon) in a walled front; genkan with shikidai step; suite of tatami rooms ending in the
  jōdan-no-ma (raised room) for the lord, with tokonoma, staggered shelves and built-in desk; attendants' rooms; special
  bath and toilet for the lord; garden; large kitchen; separate side entrance for the family (family rooms: Dwellings,
  honjin family private rooms). Items: lord's raised seat with armrest (kyōsoku), sword stand (katana-kake), folding
  screens, hanging scroll and flowers in the tokonoma, lacquered trays and bowls, the lord's bath tub, mosquito-net
  frames, name placards (sekifuda) announcing which lord is staying, hung at the station entrance and the gate, crest
  curtains (maku) across the gate, crest lanterns, bedding stacks, ledgers of stays. [WORLD_CATALOGUE T19, T57; Kusatsu
  honjin survives]
- **Deputy daimyo inn (waki-honjin)** {from C §4.3}: smaller honjin, used when the honjin was full or for lesser
  officials; in between it took ordinary travellers of standing (B: "often took ordinary paying guests like a hatago").
  Items: as honjin; smaller jōdan room, no or smaller gate. [T18]

## == Services ==

Source: B §9.

### Bathing, grooming and health

- **Public bathhouse (sentō, yuya)**: by 1730 a shallow hot bath entered through a low gabled "pomegranate door"
  (zakuro-guchi) holding in the steam; mixed bathing common; men's upstairs rest room with tea, snacks, board games. The
  earlier bath women (yuna) were banned in Edo in 1657. Town building; board floor sloping to drains. Items: street
  entrance with noren, raised pay stand (bandai) with cashbox, changing area with shelves (tana) or baskets, board
  washing floor (nagashi), small wooden buckets, the zakuro-guchi and dim bath beyond, boiler room (kama-ba) with big
  cauldron and demolition-timber firewood, upstairs rest room with go board, tea kettle, tobacco tray.
  [WORLD_CATALOGUE T27]
- **Steam bath (mushi-buro, todana-buro)**: older steam-cabinet bath; natural stone steam baths (ishi-buro) by the sea
  in some regions. Items: small closed steam room, hot-stone or boiling-water box, sliding door. (verify: largely
  replaced in cities by 1730)
- **Barber (kamiyui-doko)**: shaved the pate and dressed topknots; a social hub. Three forms: town shop (uchi-doko),
  booth at a bridge or crossroads (de-doko), itinerant (mawari). Town shop or booth; raised floor for waiting. Items:
  razors (kamisori), combs, pomade (bintsuke-abura), paper cord (motoyui), water basin and hot water, small mirror,
  whetstone and strop, customer's low stool, tobacco tray, go or shōgi board for those waiting.
- **Women's hairdresser (onna-kamiyui)**: before this, women did their own hair or had a maid do it. `[outside
  1680-1750: professional women's hairdressers from the 1780s, repeatedly banned]`
- **Masseur and acupuncturist (anma, harii)**: largely a blind men's guild (tōdō-za); masseurs walked the streets at
  night blowing a whistle. Base in a nagaya room; `itinerant`. Items: acupuncture needles in a case, guide tube
  (shinkan, Sugiyama Waichi, 17th c.), staff, whistle, cushion.
- **Moxa shop (mogusa-ya)**: moxa for home treatment; Ibuki moxa (Kameya at Kashiwabara on the Nakasendō) famous. Town
  shop. Items: moxa bales, paper packets, incense sticks for lighting, mortars.
- **Doctor's practice (isha)**: Chinese-style medicine (kanpō): pulse, compounded remedies. Home practice in a
  machiya; raised tatami rooms. Items: drug chopper (yagen: boat-shaped iron trough with a wheel), mortars, many-drawer
  medicine cabinet (hyakumi-dansu), scales, paper packets, portable medicine chest (yakurō) for house calls, medical
  books, patient's cushion. Dutch-learning (ranpō) doctors are `[outside 1680-1750: from the 1770s]`. (Home side:
  Dwellings, town doctor's house.)
- **Eye doctor and dentist (me-isha, kuchi-isha, ireba-shi)**: specialists; dentists carved boxwood dentures. Town
  practice. Items: fine tools, lamp, denture carving kit, sample teeth.
- **Midwife (sanba)**: home-based; a Dwellings home with a prop set. (Cross-reference, not counted.)
- **Medicine shop (kusuri-ya, kigusuri-ya)**: ready remedies by brand; huge three-dimensional shop signs. Town shop.
  Items: drug chopper (yagen), drawer cabinet, jars, scales, paper packets, pill-rolling board, brand signboards, stone
  mortar. Odawara's Uirō shop (pill and sweet of the same name, on the map) has a distinctive castle-style front.
- **Medicine wholesaler (kusuri-don'ya)**: Osaka's Dōshō-machi, Edo's Honchō 3-chōme. Town shop plus kura. Items:
  bales of raw herbs, imported drugs, sorting tables.
- **Travelling medicine seller (Toyama baiyaku)**: "use first, pay later" peddlers (from c.1690, in era) left a box of
  medicines in each house. `itinerant`, base in Toyama. Items: tall stacked pack of wooden boxes, ledgers; paper
  balloons as gifts are later.

### Money, brokerage and business

- **Moneychanger (ryōgae-ya)**: exchanged gold, silver, copper; big ones (hon-ryōgae) did loans and bills, small ones
  (zeni-ryōgae) sold copper coin. Town shop plus kura; raised floor behind a stout lattice. Items: balance scales and
  graded weights (fundō), strong money chest (senryō-bako), coin strings (zeni-sashi), silver lumps (chōgin,
  mameitagin), gold coins (koban), touchstone, abacus, ledgers, coin tray, heavy counter lattice, coin-shaped kanban.
- **Pawnshop (shichi-ya)**: loans against goods; the kura is essential. Town shop with kura; raised floor, often a
  discreet side entrance. Items: pawn tickets (shichi-fuda), tag board, ledger, kura full of tagged goods (clothes,
  swords, tools), abacus, scales.
- **Rice broker and rice exchange (kome-don'ya; Dōjima kome-ichiba)**: rice wholesale and trading; the Dōjima exchange
  in Osaka was officially recognized in 1730, the anchor year, and traded rice futures. Town building and open trading
  floor. Items: rice samples in dishes, rice tickets (kome-kitte), tally boards, water towers or flags signalling prices
  (verify), ledgers, abacus, big canal-side warehouse kura.
- **Rice-stipend agent (fudasashi)**: Edo's Kuramae; collected shogunate rice stipends for retainers, sold them, lent
  against them. Town shop plus kura. Items: stipend papers on a straw bundle (the "fuda" on a stick), ledgers, rice
  samples, money chest.
- **Wholesaler (ton'ya / don'ya), generic**: every trade had wholesale houses by street. Big machiya plus a row of kura.
  Items: goods in bales and boxes, loading doma, carts, tally boards, house mark on everything.
- **Shipping agent (kaisen-don'ya)**: organized coastal shipping; sake-barrel ships (taru-kaisen) split from general
  cargo ships (higaki-kaisen) in 1730 (in era). Harbour-town shop plus warehouses. Items: shipping registers, cargo
  tags, samples, lookout, warehouse row.
- **Warehouse for rent (kura-kashi)**: rented kura on canals. Kura shell. Items: bales, ladders, shutters, tallies.
- **Private courier (machi-bikyaku, hikyaku-don'ya)**: express couriers for letters, money, goods between Edo, Osaka,
  Kyoto (from 1663, in era). Town office. Items: letter boxes (fubako), courier's shoulder-pole box, bell, schedules,
  ledgers, waiting bench for runners.
- **Employment broker (kuchiire-ya / hito-yado)**: placed servants, labourers, samurai-house footmen on contract. Town
  office. Items: registers of workers, contract papers, waiting room. (Lodging side: hito-yado, Lodging.)
- **Scribe and petition writer (daisho-ya)**: wrote letters, deeds, petitions for the illiterate, often attached to
  lawsuit inns. Town booth or room. Items: writing desk, inkstone, paper, seals. (verify as a separate trade)

### Transport

- **Palanquin stand (kago-ya, tsuji-kago)**: hired palanquins with bearers; city street stands and highway relay
  points. Town office and a rack. Items: kago on racks, carrying poles, bearers' straw sandals, bench, lantern.
- **Packhorse carrier, commercial (uma-kata; chūma)**: private packhorse transport; Shinano's chūma competed with the
  official post horses (lawsuits in the 1760s). Commercial stable and yard. Items: see commercial stable. (Official
  post horses: Government, toiyaba.)
- **Commercial stable and horse dealer (bakurō, uma-ichi)**: dealers and seasonal horse markets; Edo's Bakurō-chō is
  named for them. Stable plus yard. Items: stalls with manger (kaiba-oke), tie rails (uma-tsunagi), lever fodder cutter
  (magusa-kiri), straw and hay stacks, pack saddles (ni-gura) and riding saddles, straw horseshoes (uma-no-kutsu /
  uma-waraji; horses were not iron-shod), water trough, harness hooks, dealer's ledger. (Dealer's home: Dwellings,
  horse-dealer's house.)
- **Cart haulage (kuruma-hiki)**: carters with daihachi carts. Yard. Items: carts, ropes, straw pads. (B: merge with
  cart maker or stable.)
- **Ox-cart haulage (ushi-kata)**: Kyoto–Ōtsu ox carts on stone-slab cart tracks. Regional; `site` ox stable. Items:
  oxen stalls, carts, yokes.

### Entertainment and other services

- **Kabuki theatre (shibai-goya)**: licensed theatres in Edo, Kyoto, Osaka, plus touring stages. Big building with a
  drum tower (yagura) over the entrance; pit floor with box seating. Items: stage and runway (hanamichi), box-seat
  partitions (masu-seki), curtain, lanterns, drum tower, play-boards (banzuke). (B listed as commercial; could be
  Civic.)
- **Puppet theatre (ningyō jōruri)**: Takemoto-za, Osaka, from 1684 (in era); as kabuki, smaller. Items: stage with a
  hand-rail screen, puppets, chanter's dais, shamisen.
- **Show booth (misemono-goya)**: temporary booths for animals, acrobats, curiosities at temple fairs. `stall`. Items:
  painted signboard, curtain, benches.
- **Storytelling hall (yose)**: earlier, street storytellers (tsuji-kōshaku) at a small table. `[outside 1680-1750:
  from the 1790s]`
- **Archery gallery (yōkyū-ba)**: small-bow shooting galleries with women attendants. Items: small bows, arrows,
  target, drum. (verify: mostly mid–late Edo)
- **Go and shōgi parlour (go-kaisho)**: rooms for board games for a fee. Town room. Items: go boards (goban), shōgi
  boards, bowls of stones, cushions, tea kettle.
- **Gambling den (bakuchi-ba)**: illegal but widespread in samurai mansions' servants' rooms and temples. Items: dice
  cups, cloth mat, coins. (B: cut candidate; see Dwellings, chūgen-beya.)
- **Fortune-teller (eki-sha, uranai-ya)**: street booth or table. `stall`. Items: lantern, divination sticks
  (zeichiku) in a cylinder, counting rods (sangi), book.
- **Pleasure quarters (yūkaku)**: licensed walled quarters with a single gate (Edo Yoshiwara, Kyoto Shimabara, Osaka
  Shinmachi). Building types inside: brothel houses with a latticed front room where the women sat (jorō-ya / mise),
  banquet houses where top courtesans met clients (age-ya), guide tea houses that booked them (hikite-jaya), staff
  houses. Unlicensed districts (okabasho) in many towns; the meshimori inns are the Tōkaidō version. Items: lattice
  fronts (harimise), lanterns, tatami banquet rooms, shamisen, sake trays, bedding rooms. Neutral listing. (B: strong
  cut candidate.)
- **Rental shop (sonryō-ya)**: rented bedding, pots, clothes, furniture to the poor and travellers. Town shop. Items:
  stacks of futon, pots, ledger. (verify date)
- **Recycling trades (kuzu-hiroi, furugane-kai, hai-kai, shimogoe)**: Edo recycled nearly everything: waste-paper,
  old-metal, ash (to dyers and farmers), candle-drip and old-umbrella buyers, and the night-soil trade to farmers.
  `itinerant` with a dealer's yard or shed. Items: baskets, sacks, shoulder pole, sorting yard, manure boat or buckets.
- **Street repairers**: clog-tooth replacer (geta no ha-ire), pot mender (ikake-ya), knife grinder, mirror polisher,
  pipe-stem replacer (rao-ya), china mender (yakitsugi `[outside 1680-1750: late 18th c.]`). All `itinerant`; props,
  not buildings.

## == Crafts by family ==

Source: B §1–6. Only the working side is listed; the family's living rooms are the matching Dwellings entry. Setting:
`town workshop` = makes things in a machiya or back-alley nagaya, may sell at the front; `town shop` = sells at the
street (takes the standard shop-front kit, see Shops); `rural`; `site` = standalone works; `stall`; `itinerant` = no
premises (listed so Stephen can cut it or make it a prop). Floor: doma (earth: wet, heavy, fire work) or raised (board
or tatami).

### Metal

- **Village and farm-tool smith (kaji-ya, nō-kaji)**: makes and re-steels hoes, sickles, hatchets, nails, hinges.
  Village smithy or town workshop at a street edge; open front, doma, soot, roof smoke vent. Items: forge hearth
  (hodo), box bellows (fuigo, push-pull piston), anvil (kanatoko) set in a stump, quench tub (mizu-oke), tongs (hibashi
  / yattoko), sledges and hand hammers (tsuchi), charcoal bin and pine charcoal, grindstone and whetstones (toishi),
  finished hoes and sickles hung on the wall, scrap iron pile.
- **Anchor and ship-iron smith (ikari-kaji / funa-kaji)**: big four-fluked iron anchors (ikari), nails, ship fittings.
  Harbour-side town workshop; doma, extra-large hearth. Items: big hearth, several bellows, heavy anvil, long tongs on
  chains or a crane pole, swage blocks, finished anchors, spikes and clench nails (funa-kugi). (verify which
  *Shokunin burui* plate)
- **Carpenter's-tool smith (daiku-dōgu kaji)**: plane irons (kanna), chisels (nomi), gimlets (kiri), laminating hard
  steel onto soft iron. Town workshop; doma. Items: small forge, fuigo, anvil, laminating steel bars, chisel blanks,
  files, whetstone trough, finished tool rack. Miki (Harima) famous for this in the 18th c. (verify how early)
- **Saw smith (noko-kaji / metate-shi)**: forges saws, cuts and sets the teeth (saw doctors also travelled). Town
  workshop; doma. Items: forge, long thin anvil, saw blanks, files (yasuri), tooth-setting hammer and anvil, wooden saw
  vice, whetstones. Saws in use: kataba (single edge), maebiki (big rip); the double-edged ryōba is `[outside
  1680-1750: late Edo / Meiji]` (verify).
- **Knife smith (hōchō-kaji)**: kitchen knives (deba, usuba, sashimi) and, in Sakai, tobacco-cutting knives with a
  shogunate quality seal (Sakai kiwame) in the 18th c. Town workshop; doma. Items: forge, fuigo, anvil, quench trough
  with clay-coating pot, big hand-turned wet grinding wheel, whetstones, handle wood (hō), horn ferrules, finished
  knives in straw.
- **File maker (yasuri-shi)**: cuts file teeth with a chisel (tagane) into soft steel, then hardens. Town workshop;
  doma. Items: small forge, lead-bed anvil to hold the blank, cutting chisels, hammer, quench tub, finished files.
  (verify)
- **Swordsmith (katana-kaji)**: forges blades from tamahagane; sacred work. Town or castle-town workshop, often behind a
  fence; doma, darkened forge room to read the steel's colour. Items: forge with shimenawa over it, kamidana, box
  bellows, anvil, several strikers' sledges, tamahagane lumps, straw ash and clay slurry for folding, clay-coating
  trough (tsuchioki), long quench trough, tongs, file, blade rack, white ceremonial clothing (eboshi).
- **Spear and polearm maker (yari-kaji)**: usually the same smiths; heads for yari and naginata. Items: as swordsmith,
  plus oak spear shafts (e), ferrules (ishizuki). (B: merge with swordsmith unless a "cheap weapons" smithy is wanted.)
- **Sword polisher (togishi)**: polishes blades through a sequence of stones. Quiet town workshop; raised board floor.
  Items: sloping stone-holder (togi-dai) on a small stool, whetstone set coarse to fine, water tubs, finger stones
  (hazuya, jizuya), paper and cloth, blade stand.
- **Scabbard maker (sayashi)**: carves magnolia (hō) scabbards and plain storage mounts (shirasaya). Town workshop;
  raised. Items: hō-wood planks, rice-paste glue (sokui) and spatula, small planes, chisels, carving knives, cramps and
  binding cord, lacquer shelf.
- **Hilt wrapper (tsukamaki-shi)**: wraps hilts in ray skin (samegawa) and silk or leather braid. Town workshop;
  raised. Items: hilt cores, rolls of ray skin, silk braid spools, paper wedges (hishigami), glue pot, hilt vice.
- **Sword-fittings maker (tsuba-kō, kinkō-shi, habaki-shi)**: guards, collars, pommels, small fittings in iron, copper,
  shakudō, gold; the Gotō school did official work. Town workshop; raised. Items: small charcoal forge, chasing hammers
  and punches (tagane), pitch bowl (yani-dai), files, gravers, small crucibles, patination pot (niage: plum vinegar and
  copper salts), finished tsuba on a board.
- **Armourer (katchū-shi / gusoku-shi)**: makes and repairs armour; by 1730 mostly ceremonial and revival pieces
  (Myōchin school). Town workshop; doma for metal, raised floor for lacing. Items: small forge, stake anvils,
  planishing hammers, iron scales and plates (sane, ita-zane), rawhide (nerikawa) plates, lacquer pots, rivets, silk
  lacing braid (odoshi-ito) on reels, lacing frame, finished armour on a box stand (yoroi-bitsu).
- **Caster of pots and kettles (imoji)**: iron cooking pots (nabe), rice kettles (kama), tea kettles (chagama), small
  bronze goods; Takaoka (from 1611) and Kyoto kettle makers are period centres. Town workshop or edge-of-town site;
  doma, casting pit. Items: cupola or crucible furnace (koshiki-ro), foot bellows (fumi-fuigo), clay moulds
  (imono-gata) in parts, crucibles (rutsubo), ladles, sand floor, scrap iron, cooling rack of new pots. Everyday
  side-spouted tetsubin comes later `[outside 1680-1750: mid-18th c. on]` (verify; see Contradictions).
- **Bell caster, on site (bonshō imono)**: temple bells cast at a temporary site near the temple, not in a shop. Site
  kit: dug casting pit, clay mould built up in the pit, ring of furnaces and foot bellows, thatched shelter, fuel
  stacks. (See Buddhist, bell tower.)
- **Mirror maker (kagami-shi)**: casts and polishes bronze mirrors; itinerant polishers (kagami-togi) re-polished with
  mercury-tin amalgam. Town workshop; raised for polishing. Items: small crucible furnace, moulds, polishing board,
  whetstones, powdered amalgam jars, finished mirrors in boxes, mirror stands (kyōdai).
- **Coppersmith (dōki-shi, akagane-shi)**: raises sheet copper into kettles, water jars, hibachi liners, lantern tops;
  also copper roofing. Town workshop; doma. Items: sheet copper stack, stake anvils in a stump (tokodai), wooden and
  steel hammers, annealing hearth, shears, tin solder and soldering iron, finished kettles. (verify)
- **Pewterer (suzu-shi)**: pewter and tin sake flasks, tea caddies, offering vessels; Osaka and Kyoto. Town workshop;
  raised. Items: small melting pot, stone or clay moulds, trimming lathe, scrapers, burnishers, finished flasks
  (suzu-dokkuri). (verify period)
- **Tinplate smith (buriki-ya)**: listed only because it was in the brief; 1730 equivalents are coppersmith and
  pewterer. `[outside 1680-1750: tinplate is Meiji]`
- **Ornamental metalworker (kazari-shi / kazari-shoku)**: hairpins (kanzashi), door-pull plates (hikite), nail covers
  (kugi-kakushi), tansu fittings, pipe bowls. Town workshop; raised. Items: small charcoal hearth with blowpipe, pitch
  bowl, chasing punches, files, saws, sheet brass and copper, silver wire, finished fittings on boards.
- **Gold and silver leaf beater (haku-uchi-shi)**: beats leaf between paper. Town workshop; raised, still air. Items:
  stone or wood beating block, heavy hammers, packets of beating paper (haku-uchi-gami), bamboo tweezers, cutting frame,
  leaf books. Shogunate gold-leaf guild (haku-za) c. 1696 (verify date).
- **Needle maker (hari-shi)**: sewing and tatami needles; Kyoto's Misuya needles are the period brand. Town workshop;
  raised. Items: iron wire coils, draw plate, wire cutters, small anvil and eye punch, files, hardening hearth, tumbling
  tub for polishing, needles packed in paper.
- **Wire drawer (harigane-shi)**: iron and copper wire for needles, cages, fittings. Town workshop; doma. Items: draw
  plates, long draw bench with winch, annealing hearth, coils. (B: could merge with needle maker.)
- **Nail maker (kugi-kaji)**: hand-forged square nails (wa-kugi) by the barrel. Town workshop; doma. Items: small
  forge, nail header (heading block), anvil, nail rod bundles, barrels of nails by size.
- **Lock maker (jōmae-shi)**: box and door padlocks (wa-jō) with spring mechanisms. Town workshop; raised. Items:
  small forge, files, sheet iron, keys on strings, finished locks.
- **Scale maker (hakari-shi, the Hakari-za)**: steelyards and balances were a shogunate monopoly: Moriya (Edo, east)
  and Shuzui (Kyoto, west) guilds. Town shop and workshop. Items: steelyard beams (sao), waisted brass weights (fundō),
  balance pans, measuring rules, official stamps, register.
- **Pipe maker (kiseru-shi)**: metal bowl and mouthpiece joined by a bamboo stem (rao). Town workshop; raised. Items:
  brass and copper sheet, small forge or blowpipe, mandrels, files, stock of bamboo stems, finished pipes on a rack.
  The street stem-replacer (rao-ya) is itinerant (its steam-whistle cart is late Edo).
- **Stirrup and bit maker (abumi-shi, kutsuwa-shi)**: open-sided slipper-shaped iron stirrups and bits, often
  silver-inlaid; Kaga and Kyoto known. Town workshop; doma. Items: forge, anvil, iron sheet, inlay tools, stirrups hung
  in pairs.
- **Clockmaker (tokei-shi)**: wadokei with adjustable temporal hours, for daimyo and temples; rare. Castle-town
  workshop; raised. Items: brass gears, files, small lathe, verge-and-foliot parts, clock on a tall stand
  (yagura-dokei). (B: niche, flag for cutting.)
- **Gunsmith (teppō-kaji)**: matchlocks; Kunitomo (Ōmi) and Sakai. Out of scope for the game; listed only. Items:
  barrel forge, boring bench, lock parts, stocks.
- **Pot mender (ikake-ya)**: patched iron pots and kettles with solder at the roadside. `itinerant`. Items: small
  portable bellows and hearth, solder, shoulder-pole kit.
- **Knife and blade sharpener (togi-ya)**: tools and razors. `itinerant` or tiny booth. Items: whetstones in a wooden
  holder, water tub.

### Leather and hides

Status note (neutral): work with dead animals and hides was tied to hereditary kawata (officially eta) communities,
who held hereditary rights to the carcasses of dead cattle and horses in a district; many lived in separate hamlets,
often by rivers. Kantō: under Danzaemon at Asakusa; Osaka: Watanabe village, a major leather and drum centre. Deer hides
were also imported in quantity through Nagasaki in the 17th c. Period-true leather workshops sit outside or at the
edge of towns. Stephen decides how, or whether, the game shows this. (Homes: Dwellings, kawata village house and
leader's compound.)

- **Carcass processing and rawhide yard (kawa-hagi-ba)**: skinning dead stock, scraping, salting. Riverside `site` at
  the edge of a kawata hamlet; open yard and a shed; doma. Items: skinning knives, fleshing beam, fleshing knife
  (kawa-sen), salt, stretching stakes and pegs, drying frames, bone and horn piles, water channel.
- **Tanner, white leather (shiro-nameshi / kawa-ya)**: Himeji white leather: river water, salt, rapeseed oil, trodden
  by foot, sun-bleached. Riverside `site`: river soaking pens, a shed, a drying field. Items: soaking pens in the river,
  tubs, salt, oil jars, treading tub, fleshing knives, drying frames and pegs, rolled finished hides.
- **Smoked-leather maker (fusube-gawa)**: colours deerskin by smoking with straw and pine resin. `rural` / town edge;
  small smoke shed. Items: tall smoke drum or hut, hide-wrapped rotating pole, straw and resin fuel, hides hanging.
- **Lacquered deerskin maker (inden-ya)**: Kōfu (Kai) speciality (from 1582): lacquer patterns stencilled onto deerskin
  for pouches and armour. Town workshop; raised. Items: tanned deerskins, lacquer pots, paper stencils, spatulas,
  drying cupboard, cut pouch parts.
- **Hide and deerskin dealer (kawa-don'ya)**: wholesale hides, imported deerskins via Nagasaki. Town shop plus kura.
  Items: stacked bundles of hides, hide-grading table, scales, tally sticks.
- **Drum maker (taiko-shi)**: hollows keyaki trunks (kuri-bachi drums), stretches cowhide heads, nailed or roped. Town
  or kawata-village workshop; doma. Items: hollowed log bodies, adze and chisels, rawhide heads soaking in a tub,
  stretching jack (ropes and lever, or a jack under the drum), iron tacks (byō), drum stands, beaters (bachi), finished
  drums from hand drums to temple drums.
- **Leather-soled sandal maker and repairer (setta-ya / setta-naoshi)**: setta = zōri with leather sole and iron
  heel-plate; repair was a kawata trade in Edo. Town workshop or `itinerant`. Items: leather soles, woven bamboo-sheath
  uppers, awls, thread, heel-plates, low bench.
- **Leather tabi and glove maker (kawa-tabi, yugake-shi)**: leather socks (largely replaced by cotton tabi after the
  1657 Meireki fire raised leather prices, often repeated (verify)) and deerskin archery gloves (yugake). Town
  workshop; raised. Items: deerskin, patterns, shears, awls, waxed thread, wooden hand forms, finished gloves.
- **Saddler and tack maker (kura-shi, bagu-shi)**: lacquered wooden saddle trees (kura) plus leather flaps, girths,
  cruppers. Town workshop; doma. Items: saddle trees on stands, lacquer shelf, leather straps, braided girths, flaps
  (aori), cushions, awls, finished saddles on a saddle horse. (Stirrups: Metal, abumi-shi.)
- **Pouch and tobacco-pouch maker (tabako-ire-shi, kinchaku-ya)**: leather and cloth pouches, tobacco cases, purses,
  belt sagemono. Town workshop and shop; raised. Items: leather and cloth offcuts, patterns, shears, awls, clasps
  (kanagu) from the kazari-shi, netsuke toggles, finished pouches on a rack.
- **Hide-glue maker (nikawa-shi)**: boils hide and bone scraps for glue (painters, ink makers, joiners). Kawata-village
  `site`; doma, smelly. Items: big boiling cauldron on a hearth, scrap bins, straining cloths, setting trays, drying
  rack of glue sticks.
- **Leather garment maker (kawa-baori)**: firemen's and hunters' leather coats. Town workshop. Items: large hides,
  patterns, lacquer or smoke for colour, awls. (B: probably merge with pouch maker.)
- **Shamisen maker (shamisen-shi)**: hardwood neck and body (often imported woods), cat or dog skin heads. Town
  workshop; raised. Items: neck blanks, body frames, skins soaking, stretching press with wedges and cords, pegs, silk
  strings, finished shamisen on the wall. (B: leather link noted; could sit under fine crafts.)

### Wood, bamboo and building timber

- **Carpenter's workshop and yard (daiku, sakuba)**: carpenters mostly worked on site; the master (tōryō) kept a yard
  for pre-cutting joints and storing timber. Town workshop with yard; doma. Items: ink line (sumitsubo) and marking pen
  (sumisashi), square (sashigane), saws (kataba, maebiki), planes (dai-kanna), adze (chōna), axes (ono), chisels
  (nomi), mallet (genno), gimlets (kiri), wooden sawhorses (uma), tool box (dōgu-bako), plan board (ita-zu), stacked
  squared timbers, shavings.
- **Sawyer's shed (kobiki-ba)**: one- or two-man rip sawing of logs into planks with the maebiki-ōga. Timber-yard or
  `rural` shed; doma. Items: log propped high on trestles at an angle, maebiki-ōga saws, wedges, ink line, plank
  stacks, sawdust.
- **Lumber dealer and timber yard (zaimoku-ya, kiba)**: timber wholesale; Edo's Fukagawa Kiba yards (moved there 1701)
  kept logs floating in ponds and canals. Waterside `site` and town office; open yard. Items: log pond, standing timber
  racks (tate-kake), stacked planks under roofs, log hooks (tobi-guchi), rafts, tally boards, dealer's mark branded on
  log ends.
- **Joiner, doors and screens (tategu-shi)**: sliding shōji, fusuma frames, wooden doors, lattice (kōshi). Town
  workshop; doma for planing, raised for assembly. Items: long planes, groove planes (mizo-kanna), fine saws, chisels,
  kumiko lattice jig, frames leaning on the wall, paper rolls for shōji.
- **Cabinet maker (sashimono-shi)**: tansu, boxes, shelves, trays, joined without nails; tansu spread widely in this
  period. Town workshop; raised. Items: fine saws, small planes, chisels, marking gauge, clamps, paulownia and zelkova
  boards, half-built tansu, iron fittings to fit.
- **Paulownia box maker (kiri-bako-ya)**: fitted boxes for scrolls, tea bowls, dolls. Town workshop. Items: kiri
  boards, fine saws, planes, box string (sanada-himo), boxes stacked by size. (B: merge with sashimono.)
- **Cooper, closed barrels (taru-ya)**: cedar sake and soy casks with bamboo hoops; the big trade feeding breweries.
  Town or brewery-side workshop; doma. Items: cedar staves drying in stacks, giant upturned jointer plane (shōjiki),
  drawknife (sen), hoop driver (taga-hame), split bamboo for hoops, bevelling knife, compass for heads, finished casks
  in straw wrap (komo).
- **Tub and bucket maker (oke-ya)**: open tubs, bath tubs, well buckets (tsurube), rice tubs, ladles. Town workshop;
  doma. Items: as cooper, plus tubs of all sizes stacked in the street, hoop-coiling stand. (B: could merge with
  taru-ya.)
- **Bentwood maker (magemono-shi)**: thin cypress bent into round boxes, steamers (seiro), sieves (furui), lunch boxes
  (wappa), stitched with cherry bark. Town or mountain `rural` workshop. Items: cypress-strip soaking tub, heated
  bending iron or hot-water trough, wooden forms, clothes-peg clamps, cherry-bark strips, awl, stacked boxes and
  steamers.
- **Woodturner (kijishi / rokuro-shi)**: turns bowl and tray blanks on a rope lathe; often mountain people who moved
  with the timber and sold blanks to lacquerers. `rural` mountain or town workshop; doma. Items: two-person rope lathe
  (tebiki-rokuro: one pulls the strap, one turns), hooked turning chisels (rokuro-kanna), axe and adze for rough-outs,
  drying racks of rough bowls, shavings. (Their hut: Dwellings, wood-turner's forest hut.)
- **Hakone woodcraft maker (Hakone zaiku)**: turned toys, boxes, souvenirs for Tōkaidō travellers at Hatajuku and
  Yumoto. Roadside town workshop and shop. Items: lathe, turning hooks, local woods by colour, finished toys and boxes on
  front shelves. Marquetry (yosegi) is `[outside 1680-1750: Ishikawa Nihei, late Edo]`.
- **Comb maker (kushi-ya)**: boxwood (tsuge) combs; tortoiseshell combs are Fine crafts (bekkō). Town workshop and shop;
  raised. Items: boxwood blanks drying, fine comb saw, tooth-spacing guide, files, rasps, scouring-rush (tokusa)
  polishing, finished combs on a board.
- **Clog maker (geta-ya)**: paulownia geta with separate or carved teeth; hanao thongs fitted. Town shop and workshop;
  doma plus raised. Items: paulownia blocks, saw, broad knife, thong-hole drill, hanao bundles, finished geta hung in
  pairs, fitting stool. Tooth replacement (ha-ire) was itinerant.
- **Boat builder's shed (funa-daiku)**: river boats, fishing boats, ferries. Waterside `site`, open shed at the water's
  edge. Items: hull on building stocks, planks bent over fire, clamping ropes and wedges, chisel-shaped flat-headed
  boat nails (funa-kugi), caulking iron and cypress-bark caulking (maki-hada), adzes, oars and sculls (ro), steaming
  fire.
- **Shipyard for coasters (funaba / zōsen-ba)**: big coasters (bezaisen, higaki-kaisen) on stocks. Harbour `site`,
  open slipway with sheds. Items: keel-plank on stocks, frames, huge planks, pulleys, mast timber, sail loft (see
  sailcloth maker), smith's shed. (Larger version of the boat shed.)
- **Cart maker and wheelwright (kuruma-ya)**: two-wheeled handcarts (daihachi-guruma, Edo from the 1650s; smaller
  beka-guruma in Osaka), ox-carts (ushi-guruma, Kyoto area). Town workshop; doma. Items: spoked wheel on a stand, hubs,
  felloes, iron tyres or straps, axle timbers, finished cart.
- **Palanquin maker (kago-shi, norimono-shi)**: cheap open bamboo kago and the enclosed lacquered norimono of the rich.
  Town workshop. Items: bamboo frames, carrying poles, woven bamboo sides, lacquered panels and blinds, cushions.
- **Bowyer (yumi-shi)**: laminated bamboo-and-wood asymmetric yumi, glued and bound with wedges. Town workshop; raised.
  Items: bamboo and haze-wood strips, glue pot, bundle of bamboo wedges and clamping rope, bow forms, finished bows,
  hemp strings.
- **Fletcher (ya-shi)**: bamboo shafts straightened over heat, fletched, iron heads fitted. Town workshop; raised.
  Items: bamboo stock, charcoal pot and straightening block (yatame-ki), feathers in boxes, glue, silk binding,
  arrowheads (yajiri), finished arrows in a quiver stand.
- **Shingle splitter and shingle roofer (kokera-shi, hiwada-shi)**: splits cedar or sawara shingles; cypress-bark
  (hiwada) roofing for temples. Town or `rural` workshop. Items: froe (hegi-nata), splitting block, shingle bundles,
  bamboo nails, cypress-bark bundles.
- **Mortar and pestle maker (usu-ya)**: big wooden rice mortars (usu) and pounders (kine). `rural` or town workshop.
  Items: keyaki or pine log sections, adze, chisels, finished mortars.
- **Abacus maker (soroban-shi)**: frames and beads. Town workshop. Items: beads turned on a small lathe, bamboo rods,
  frames. (B: niche, merge with sashimono.)
- **Measuring-box maker (masu-shi, the Masu-za)**: official rice and sake measures; the Kyō-masu standard was a
  licensed guild. Town workshop. Items: boards, jointing planes, official branding iron, stacked masu of each size.
- **Bamboo worker, baskets and sieves (take-zaiku, kago-ya, zaru-ya)**: baskets, sieves, trays, carrying baskets. Town
  workshop or `rural`; doma. Items: bamboo poles, splitting knife (take-wari nata), sizing knives, soaking tub,
  half-woven baskets, finished baskets hung outside.
- **Blind maker (sudare-ya)**: reed and bamboo blinds, and silk-edged fine blinds (misu) for mansions. Town workshop.
  Items: blind-weaving frame with weighted bobbins, split bamboo or reeds, silk edge cloth.
- **Tea-whisk and tea-ware bamboo maker (chasen-shi)**: whisks, scoops (chashaku); Takayama (Nara) monopoly. Town
  workshop; raised. Items: bamboo sections, small knives, whisk-shaping stand, finished whisks in paper. (Niche.)
- **Ladle and spoon whittler (shakushi-zaiku)**: wooden rice paddles and ladles; Miyajima famous. `rural` workshop.
  Items: blanks, knives, shaves, bundles of paddles.

### Textiles, fibre, straw and rush

- **Cotton ginner (wata-kuri)**: removes seeds on a two-roller hand gin. `rural` or town workshop; raised. Items:
  roller gin (wata-kuri-ki), baskets of seed cotton, seed sacks, ginned cotton.
- **Cotton bower and wadding shop (wata-uchi, wata-ya)**: fluffs ginned cotton with a big bow struck by a mallet; sells
  wadding for futon and clothes. Town workshop and shop; raised, dusty. Items: large cotton bow hung from a pole
  (wata-uchi yumi), wooden mallet, piles of fluffed cotton, pressing board, folded cotton sheets (wata).
- **Cotton-cloth wholesaler (momen-don'ya)**: bulk cotton from Kinai, Mikawa, Owari; Edo's Ōdenma-chō was the cotton
  street. Town shop plus kura. Items: bales of cloth bolts (tan) in straw wrap, measuring table, whalebone cloth rule
  (kujira-jaku), ledgers.
- **Spinner (ito-tsumugi)**: home work on a spinning wheel (ito-guruma); as a building it is a nagaya or farmhouse room
  (see Dwellings). Items: spinning wheel, rolled cotton slivers (yori-ko), skeins.
- **Silk reeler (ito-hiki / seishi)**: hand-reels silk from cocoons in hot water (te-biki). `rural` farmhouse or town
  workshop. Items: small brazier with a pot of hot water, cocoons, reeling frame or large wooden reel (waku), chopsticks
  to find ends, skeins. Seated geared zaguri is `[outside 1680-1750: spread late Edo, esp. after 1859]`.
- **Floss-silk maker (mawata-ya)**: stretches boiled waste cocoons over frames for padding. `rural`. Items: boiling pot,
  wooden or bamboo stretching frames (mawata-kake), drying racks of floss.
- **Silk thread dealer and twister (ito-ya, ito-don'ya, nenshi)**: twists and sells silk thread. Town shop or workshop.
  Items: skeins on poles, twisting frame, bobbins, scales. Kiryū water-powered twisting mills are `[outside 1680-1750:
  c.1780s]` (verify).
- **Hemp and ramie processor (asa-hiki, o-umi)**: retting, scraping the fibre, splitting and joining it into thread.
  `rural` `site`: retting pond or stream pit, work shed. Items: retting pit, scraping board and blade (o-hiki), fibre
  hanks drying, thread basket (o-oke).
- **Cloth bleacher (sarashi-ya)**: bleaches hemp, ramie, cotton by washing, fulling on a block (kinuta) and sun-laying
  (Nara sarashi, Ōmi); Echigo ramie bleached on snow (yuki-sarashi). `rural` `site`: bleaching field by a river.
  Items: fulling block and mallets (kinuta), cloth lengths pegged on the grass, lye tubs, washing boards.
- **Silk drawloom weaver (Nishijin hata-ya)**: Kyoto figured-silk brocade (nishiki, kinran) on the tall two-person
  drawloom (sorabiki-bata: one weaves, one sits above pulling pattern cords); looms on the doma for humidity. Town
  workshop; doma, tall ceiling. Items: drawloom, pattern cords, shuttles (hi), reed (osa), warp beam, bobbin winder,
  silk yarn on racks, gold-thread box. (Homes: Dwellings, Kyoto back-alley row.)
- **Town or village weaver (hata-ori)**: plain cotton, hemp or silk on a frame loom (taka-bata) or the older backstrap
  ground loom (izari-bata / ji-bata). `rural` or town workshop; raised or doma corner. Items: loom, shuttle, reed,
  warping frame (hebata), bobbin winder (ito-guruma), finished bolts.
- **Ikat weaver (kasuri)**: pre-tied, pre-dyed yarn woven into blurred patterns. Items: as weaver, plus
  thread-binding frame. Kurume and Iyo kasuri `[outside 1680-1750: c.1800]`; simpler kasuri earlier (verify).
- **Wild-fibre weaver (fuji-fu, shina-fu)**: wisteria and linden bark cloth for poor mountain people. `rural`. Items:
  bark bundles, boiling pot with ash, splitting knives, ground loom.
- **Indigo dyer (kon'ya / ai-ya)**: the most common dyer. Town workshop with a yard; doma with vats sunk into the floor,
  often four round a warming fire pit. Items: sunken indigo vats (ai-game), fire pits (hi-tsubo), fermented indigo
  (sukumo) in bales, lye tubs (akumizu), wheat bran and lime, stirring poles, cloth dripping over the vats, tall drying
  poles and frames in the yard or on the roof. (verify: Hiroshige's Kanda Kon'ya-chō is 1857; check *Jinrin kinmōzui*
  for an earlier plate)
- **Stencil (paste-resist) dyer (katazome-ya, komon-ya)**: small repeats for samurai kamishimo (komon), larger for
  cotton (chūgata). Town workshop; long raised floor. Items: very long boards (nagaita, ~6 m) on trestles, paper
  stencils (katagami), rice-paste resist tub, spatulas (hera), bamboo stretchers (shinshi) in the yard, steaming box,
  brushes.
- **Stencil cutter (katagami-shi)**: cuts stencils from persimmon-tannin laminated paper; Ise katagami from Shiroko
  and Jike (Suzuka), sold by travelling agents. Town workshop; raised. Items: cutting board, knives and punches
  (kiri-bori, dōgu-bori), stacks of shibu paper, silk-thread reinforcement.
- **Yūzen dyer (yūzen-ya)**: freehand painted resist on silk, credited to Miyazaki Yūzensai in Genroku (in era). Kyoto
  town workshop; raised. Items: rice-paste cones (tsutsu), fine brushes, dye pots, silk stretched on shinshi, steaming
  box, rinsing stream (Kamo river).
- **Tie-dyer (shibori-ya)**: tie and stitch resist; Arimatsu shibori on the Tōkaidō (from 1608) sold to travellers at a
  roadside shop. Town workshop plus shop; raised. Items: binding stands and hooks, thread, cloth, indigo vats or a dyer
  contact, finished tenugui and yukata cloth hung at the front.
- **Safflower-red dyer (beni-ya, momi-ya)**: safflower red (Mogami, Yamagata), sold as beni cakes, used for red silk
  (momi) and lip colour. Town workshop; raised. Items: safflower cakes (beni-mochi), shallow tubs, sieves, rice or plum
  vinegar, dye cups.
- **General and black dyer, crest painter (someya, kurozome-ya, monkaki-shi)**: black dye for formal wear;
  hand-painted crests on black garments. Town workshop. Items: dye tubs, drying poles, compass and crest pattern books,
  fine brushes, white pigment.
- **Tailor (shitate-ya, nui-mono-shi)**: sews kimono to order (much sewing was women's home work). Town workshop;
  raised tatami. Items: low sewing board, measuring rule (kujira-jaku), hand shears (nigiri-basami), pin cushion
  (hari-yama), small irons (hera and kote heated in a brazier), flat pan iron (hinoshi), thread box, folded garments.
- **Embroiderer (nuihaku-shi)**: silk and gold-thread embroidery for temple cloths, costumes, rich garments. Town
  workshop; raised. Items: embroidery frame on trestles, silk floss, gold thread, needles, pattern drawings.
- **Braid maker (kumihimo-ya)**: silk braid for armour lacing, sword hilts, obi cords, haori ties. Town workshop;
  raised. Items: round braiding stand (marudai) with weighted bobbins (tama), square stand (kakudai), high stand
  (takadai, verify date), silk skeins, counterweight bag.
- **Futon and bedding maker (futon-ya)**: sews and stuffs quilts and sleeved quilts (yogi); cotton bedding spreading in
  the mid-18th c., still costly (verify how common in 1730). Town workshop; raised. Items: cotton wadding piles,
  covers, long needles, stuffing board, stack of finished futon.
- **Sock maker (tabi-ya)**: cotton tabi with clasps (kohaze; earlier ties). Town shop and workshop. Items: foot-shaped
  patterns, cut soles, clasps, sample tabi hung outside as a sign.
- **Mosquito-net maker and seller (kaya-ya)**: hemp nets, often green with red edge, from Ōmi (Nishikawa house); street
  sellers cried them in summer. Town shop; raised. Items: bolts of net, frames for hanging samples, measuring rule.
  (The Hakone "origin" story of the green colour is legend, unverified.)
- **Sedge-hat and rain-hat maker (kasa-ya, suge-gasa)**: sedge, bamboo and wood-strip hats. Town shop or `rural`.
  Items: sedge bundles, hat forms, bamboo frames, finished hats stacked and hung.
- **Rope and cordage maker (nawa-ya, tsuna-ya)**: hemp and straw rope, ship cordage. `rural` or harbour town; long open
  twisting yard. Items: rope-twisting device (hand-cranked hooks), long rope walk, hemp hanks, coils of rope.
- **Net maker (ami-ya)**: hemp or cotton fishing nets dyed with persimmon tannin. Fishing village or town workshop;
  raised or yard. Items: netting needles (ami-bari), mesh gauges (me-ita), hemp twine, tannin tub, nets drying on
  poles.
- **Sailcloth maker (ho-ya)**: in 1730 sails were narrow cotton strips sewn together (verify); earlier straw or
  rush-mat sails; thick woven "Matsuemon-ho" is `[outside 1680-1750: Kudō Matsuemon, 1785]`. Harbour workshop. Items:
  sail-sewing floor, palms and needles, bolts, finished sail.
- **Straw-goods maker (wara-zaiku)**: waraji, zōri, mino, tawara, kamasu, mushiro, rope; mainly winter farm work, sold
  in towns and at every tea house. `rural` farmhouse doma or a nagaya room. Items: straw stacks, straw-beating stone
  and wooden mallet (wara-uchi ishi, yoko-zuchi), straw-mat loom (mushiro-bata), bale-making frame, sandal-knitting
  hooks, bundles of waraji hung from the eaves.
- **Rush-mat weaver (goza-ya, omote-ya)**: rush tatami covers (best: Bingo-omote) and goza mats. `rural` or town
  workshop. Items: rush (igusa) bundles, weighted mat loom (goza-bata), hemp warps, cut mats.
- **Tatami maker (tatami-ya)**: straw-core tatami, rush covers, sewn cloth border. Town workshop; raised board floor,
  kneeling work. Items: tatami needle (tatami-bari), elbow pad (hiji-ate), tatami knife (tatami-bōchō), work trestle
  (tatami-dai), straw cores (toko), rolls of rush covers, border cloth (heri), finished mats on edge.
- **Palm-fibre worker (shuro-ya)**: hemp-palm fibre for ropes, brooms, brushes, raincoats. `rural` or town. Items:
  palm-fibre bundles, combing boards, brooms. The shuro scrubbing brush (tawashi) is `[outside 1680-1750: 1907]`.

### Ceramics, stone, plaster and glass

- **Potter's works with climbing kiln (yakimono-ya, noborigama)**: glazed stoneware (Seto, Mino, Kyoto, Shigaraki,
  Bizen, Tokoname). `site` on a slope; workshop shed with doma. Items: stepped multi-chamber kiln with firebox, stacked
  red-pine firewood, kick wheel (keri-rokuro) and hand wheel (te-rokuro), wedging board, clay settling tanks (suihi),
  glaze tubs, long drying planks on racks, kiln shelves and props, finished wares in straw; in some villages a
  water-powered clay stamp (kara-usu) on the nearest stream. [WORLD_CATALOGUE T37]
- **Old-style tunnel kiln works (anagama, ōgama)**: single-chamber kilns still used (Bizen, Tamba, Tokoname). `site`.
  Items: tunnel kiln up a slope, firewood, simpler shed. (B: merge with noborigama.)
- **Porcelain works (jiki; Arita / Imari)**: porcelain with saggars (saya); separate enamelling trade. Sold everywhere.
  `site`. Items: as noborigama plus porcelain-stone crushing stamps on the stream, saggar stacks, blue-painting
  (sometsuke) desks with brushes and cobalt pots. `[off-map: Kyushu]`
- **Overglaze enameller (aka-e-ya)**: paints enamels on finished porcelain, re-fires in a small muffle kiln; Arita's
  enamellers' street Akae-machi, 1672. Town workshop; raised. Items: small round muffle kiln, enamel pigment pots, fine
  brushes, painting rests, wares waiting on shelves.
- **Earthenware maker (doki-ya, kawarake-shi, hōroku-shi)**: unglazed sacred dishes (kawarake), roasting pans (hōroku),
  braziers, portable stoves (kamado / hettsui; small clay shichirin type, verify date), flower pots, clay bells.
  `rural` or edge-of-town workshop; doma and a small kiln or open firing pit. Items: clay heap, wheel, moulds, small
  updraught kiln, stacks of dishes.
- **Roof-tile maker (kawara-yaki)**: one-piece pantile (sangawara) invented by Nishimura Hanbei of Ōmi 1674 (in era);
  1720 Edo began encouraging tile against fire, so demand booms round 1730. `site` on the town edge near clay; long
  drying sheds. Items: wooden tile moulds (kata), wire clay cutter, slab-cutting frame, burnishing spatula, drying sheds
  with racks of green tiles, small updraught or "daruma" kiln (verify form for 1730), ridge-end tiles (onigawara) and
  a small carving table.
- **Tile layer (kawara-buki)**: lays roofs on site; as a building, a yard with tile stacks, mud (fuki-tsuchi) pit,
  ladders. (B: merge with tile maker.)
- **Stonemason's yard (ishiku, ishi-ya)**: lanterns (tōrō), grave stones (hakaishi, spreading among commoners),
  foundation stones, well curbs, stone mills, steps. Town-edge yard, open ground with a shed. Items: chisels (nomi),
  points, stone hammer (sekkō), splitting wedges (ya) and feathers, pry bar, sledge (shura) and rollers, square and
  ink line, half-carved lanterns and grave stones, stone dust. Castle-wall specialists (Anō-shū) are a separate guild.
- **Stone quarry (ishiba, chōba)**: Izu andesite supplied Edo castle walls in the early 17th c.; Hakone and Izu are on
  the map. `site`: hillside quarry face with a shed. Items: quarry face with wedge-hole rows (ya-ana), split blocks,
  wedges, sledges, slide (shura) track, tool-sharpening forge, the lord's carved mark on blocks. (verify how active in
  1730)
- **Whetstone quarry and dealer (toishi-ya)**: Kyoto (Narutaki), Amakusa and other stones, sold by grade. Town shop.
  Items: stones graded in boxes, test trough, scales. (B: niche, merge with ironmonger.)
- **Lime burner (ishibai-yaki, kaibai-yaki)**: burns limestone (Hachiōji / Ōme for Edo) or seashells into plaster lime.
  `site`. Items: stone or earth shaft lime kiln, charcoal and wood, sacks of lime, slaking pit, shells heaped at coastal
  sites.
- **Plasterer's yard (sakan)**: mud walls and white lime plaster (shikkui) for kura; works on site, yard stores
  materials. Items: trowels (kote) of many shapes, hawk board (kote-ita), mixing pit for mud and chopped straw
  (arakabe), seaweed-glue pot (funori), hemp fibre (susa), lime sacks, bamboo lath bundles (komai).
- **Glassmaker (biidoro-ya, garasu-ya)**: beads, hairpins, the popping toy (popin), cups, spectacle lenses; Nagasaki
  first, then Osaka and Edo; rare. Town workshop; doma. Items: small crucible furnace, blowpipes, marver stone, tongs,
  cooling box, bead rods. (verify for Edo in 1730; Osaka glass c.1750s) Edo cut glass (kiriko) is `[outside
  1680-1750: 1834]`.

### Paper, lacquer, printing and the fine crafts

- **Paper mill (kami-suki-ba, washi)**: paper from kōzo bark (also gampi, mitsumata); Izu's Shuzenji gampi paper is on
  the map. `rural` `site` by clean cold water; doma. Items: bark-steaming vat (koshiki) over a cauldron, stripping
  knives, stream soaking pit, ash-lye cooking cauldron, picking tub (chiri-tori), beating block and wooden mallets,
  paper vat (suki-bune) with mucilage (neri from tororo-aoi root), mould and bamboo screen (suketa, su), couching stack
  (shitoku) on a stone-weighted lever press, drying boards leaned in the sun (hoshi-ita), brushes. (Also in the
  Gokayama gasshō attic: Dwellings.)
- **Recycled paper maker (suki-kaeshi, Asakusa-gami)**: grey recycled paper from waste bought by paper buyers.
  Town-edge workshop by water. Items: as paper mill, plus waste-paper soaking tubs, grey sheets drying.
- **Paper wholesaler (kami-don'ya)**: paper by the bundle; Ozu Washi in Nihonbashi from 1653. Town shop plus kura.
  Items: paper bales (maru) and reams (jō) in wrappers, grading table, paper cutter's board and knife.
- **Persimmon-tannin maker (kakishibu-ya)**: presses unripe persimmons, ferments the juice for waterproofing paper,
  fans, umbrellas, nets, stencil paper; makes shibu-gami. `rural` or town workshop; doma. Items: crushing tubs and
  mallets, big fermenting barrels, straining sacks, jars of kakishibu, drying boards of brown paper.
- **Paper-clothing maker (kamiko)**: robes of crumpled oiled paper; cheap winter wear and a monk's garment. Town or
  `rural` workshop. Items: tannin-treated paper sheets, crumpling boards, sewing tools. (Niche.)
- **Scroll and screen mounter (hyōgu-shi / kyōji)**: mounts scrolls, pastes papers onto fusuma and folding screens. Town
  workshop; raised board floor. Items: long lacquered table, paste bucket (nori), paste brushes (nade-bake, uchi-bake),
  drying board (karibari) with sheets pasted on, knives, rulers, scroll rollers (jiku), silk brocade offcuts.
- **Lacquer tapper (urushi-kaki)**: scores lacquer trees in summer, collects the sap. `rural` itinerant based in a hut.
  Items: curved scoring knife (kaki-kama), spatula (hera), small sap buckets, tree-climbing ladder.
- **Lacquer refiner and dealer (urushi-ya)**: strains raw sap, stirs it in the sun to dry and smooth it (kurome,
  nayashi). Town shop and workshop. Items: shallow wooden tubs, paddles, straining paper and twisting press, lacquer
  kegs, warm drying spot.
- **Lacquerer (nushi / nuri-shi)**: builds up lacquer on trays, bowls, boxes, scabbards; centres Wajima, Aizu, Kishū
  (Kuroe), Odawara (Odawara lacquer on Hakone wood, on the map). Town workshop; raised, dust-free. Items: humid drying
  cupboard (urushi-buro), spatulas, human-hair brushes (urushi-bake), lacquer pots, whetstones and charcoal for
  polishing, turning stand, wares drying on racks.
- **Gold-lacquer artist (maki-e shi)**: sprinkled gold and silver designs on lacquer. Town workshop; raised. Items:
  fine rat-hair brushes, powder tubes (funzutsu), gold powder boxes, tiny spatula, burnishing stones, drawings
  (oshi-gata). (B: could merge with lacquerer.)
- **Painter's studio (e-shi / machi-eshi)**: town painters for fans, screens, signboards, votive plaques, prints
  (official Kanō studios: see Government). Town workshop; tatami. Items: brushes, inkstone (suzuri), shell-white
  (gofun), mineral pigments (iwa-enogu) in dishes, glue (nikawa) warmer, felt mat (mōsen), paper or silk on a
  stretcher, copybooks.
- **Signboard maker (kanban-shi)**: carves and paints shop signs, gold or black lettering. Town workshop. Items:
  boards, carving chisels, lacquer and gold leaf, sample signs, three-dimensional signs (giant pipe, sandal, brush).
- **Folding-fan maker (sensu-ya, ōgi-ya)**: bamboo ribs, pleated paper, painted leaves; Kyoto. Town shop and workshop;
  raised. Items: rib-splitting knives, bundles of ribs (hone), pleating moulds (two folded papers as a press), glue,
  painted leaves, open fans on display.
- **Flat-fan maker (uchiwa-ya)**: round bamboo-and-paper fans; Marugame fans sold to Konpira pilgrims. Town workshop.
  Items: split bamboo with spread ribs, paper, glue, tannin, fans in racks.
- **Umbrella maker (kasa-shi, wagasa)**: bamboo-ribbed paper umbrellas oiled with perilla or linseed; cheap bangasa and
  bull's-eye janome-gasa. Town workshop; raised plus a yard where open umbrellas dry in rows. Items: bamboo ribs,
  turned wooden head (rokuro), thread, paper, glue, oil pot, brushes, open umbrellas drying. (Also a poor-samurai side
  job: Dwellings, rōnin and ashigaru.)
- **Lantern maker (chōchin-ya)**: collapsible paper lanterns; the travellers' Odawara chōchin is on the map (verify
  founding date, early 18th c.). Town workshop; raised. Items: collapsible wooden form, spiral or split bamboo ribs,
  paper, glue, crest-painting brushes, lanterns hanging.
- **Woodblock publisher (hanmoto / shomotsu-ya)**: shop sells, back rooms produce. Town shop plus workshop. Items: books
  in stacks and bags, blocks stored in racks (hangi-gura), publishing ledger. In era: black (sumizuri-e), hand-coloured
  (tan-e, beni-e, urushi-e) and 2–3-colour benizuri-e (from c.1744) prints; full-colour nishiki-e is `[outside
  1680-1750: 1765]`.
- **Block carver (hangi-shi / hori-shi)**: carves text and images into cherry blocks. Town workshop; raised. Items:
  cherry blocks, knives (hangi-tō), chisels and gouges, mallet, block stand, pasted-down design.
- **Printer (suri-shi)**: hand-prints from blocks. Town workshop; raised. Items: baren, brushes, dishes of ink and
  colour, damp paper stack, registration marks (kentō) cut in the block, drying lines.
- **Bookbinder (seihon-shi)**: pouch-fold (fukuro-toji) stab-sewn books; usually part of the publisher. Items: folded
  sheets, awl and mallet, thread, cutting board and big knife (tachi-bōchō), press boards, covers and title slips.
- **Bookseller (shomotsu-ya, jihon-ya, ezōshi-ya)**: learned books (Kyoto, Osaka) vs Edo's popular books and prints
  (jihon, ezōshi). Town shop. Items: books laid flat on the raised floor, prints hung on lines at the front, book bags.
- **Lending library (kashihon-ya)**: lent books from a pack carried door to door. `itinerant` with a base room. Items:
  tall wrapped book pack, ledger. `[outside 1680-1750: heyday; hundreds in Edo by 1808, but it existed earlier]`
- **Ink-stick maker (sumi-ya)**: Nara ink: pine or rapeseed-oil soot, hide glue, kneaded, pressed, dried in ash for
  weeks (Kobaien). Town workshop. Items: soot room with rows of oil lamps under clay covers, kneading board, wooden
  moulds, ash trays for drying, sticks hung in straw.
- **Brush maker (fude-shi)**: horse, deer, weasel, goat hair brushes (leather link: animal hair). Town workshop;
  raised. Items: hair bundles, sorting combs, small singeing iron, bamboo shafts, glue, finished brushes.
- **Inkstone carver (suzuri-shi)**: Town workshop. Items: stone blanks, chisels, polishing stones. (Niche.)
- **Seal carver (inban-shi, hanko-ya)**: seals in wood, stone, horn. Town shop. Items: seal stock, fine knives, seal
  vice, seal paste (shuniku), sample impressions on paper.
- **Doll maker (ningyō-shi)**: Girls' Festival dolls (Kyōhō-bina 1716–36 is in era), gosho dolls, costumed dolls. Town
  workshop and shop; raised. Items: carved wooden or paulownia-paste heads, gofun coats, fine brushes, straw-bundle
  bodies, silk costume pieces, display tiers; seasonal doll markets (hina-ichi).
- **Clay-doll maker (tsuchi-ningyō)**: moulded, painted Fushimi dolls sold to pilgrims. Town workshop with small kiln.
  Items: plaster/clay moulds, small kiln, paint pots, dolls in rows.
- **Mask carver (men-uchi)**: nō and kyōgen masks. Town workshop. Items: cypress blocks, chisels, gofun, paint. (Niche.)
- **Buddhist sculptor and altar maker (busshi, butsudan-ya)**: statues and household altars (see Buddhist). Town
  workshop. Items: carving blocks, chisels, lacquer, gold leaf, half-carved figures.
- **Rosary maker (juzu-ya)**: prayer beads. Town shop near temples. Items: bead lathe, drills, thread, tassels.
- **Incense maker (senkō-ya, kō-ya)**: sticks from powdered cedar leaf or tabu bark (Sakai a centre) and fine
  aromatics. Town workshop and shop. Items: leaf-powder mill (stone, or water mill in the country), kneading tub,
  rolling boards, drying racks of stick incense, aromatic wood (jinkō) in boxes. Mechanical extruder: date uncertain
  (verify).
- **Candle maker (rōsoku-ya)**: sumac (haze) wax hand-coated in layers round a paper-and-rush wick. Town workshop;
  raised. Items: heated wax pan, wooden skewers (kushi) with wicks, rolling board, candle racks, finished candles by
  size.
- **Tortoiseshell and horn carver (bekkō-shi, tsuno-zaiku)**: combs, hairpins, small goods, heat-welded; netsuke
  carvers (netsuke-shi, rising in this period) similar. Town workshop. Items: shell plates, heated press, saws, files,
  polishing.
- **Musical-instrument makers (koto-shi, shakuhachi, biwa, fue)**: each a small town workshop. Items: kiri koto bodies,
  bridges, strings; bamboo root sections for shakuhachi; flute bamboo and burning irons. (B: merge all.)
- **Toy and kite maker (omocha-ya, tako-ya)**: kites, tops, paddles (hagoita), rattles, papier-mâché (hariko). Town
  shop. Items: paper, bamboo, paint, toys strung up at the front.
- **Playing-card maker (karuta-ya)**: printed, hand-coloured unsun karuta; Kyoto's Gojō; gambling links. Town workshop.
  Items: card stock, blocks, colour pots. Hanafuda is `[outside 1680-1750: later]`.
- **Cosmetics maker and shop (oshiroi-ya, beni-ya)**: white face powder, safflower lip colour, tooth-blackening
  (ohaguro) materials, hair oil (bintsuke). Town shop. Items: powder jars, beni cups, oil pots, small mirrors.
- **Toothpick and toothbrush shop (yōji-ya)**: willow-twig brushes (fusa-yōji), tooth powder; Asakusa's temple approach
  famous for them. Town shop. Items: bundles of fusa-yōji, tooth-powder packets. `[outside 1680-1750: heyday c.1760s]`
- **Spectacle maker (megane-ya)**: lenses ground from crystal or glass; rare. Items: grinding stones, horn or
  tortoiseshell frames. (verify date)
- **Cloisonné worker (shippō-shi)**: enamelled metal fittings; the Hirata family worked for the shogunate. (B: niche,
  merge with ornamental metal.)
- **Firework maker (hanabi-ya)**: Kagiya (from 1659); Ryōgoku river-opening fireworks began 1733 (in era). Town-edge
  workshop with fire rules. Items: powder jars, paper tubes, rolling board, fuses, finished rockets. (Gunpowder link;
  may be cut.)

## == Rural industry ==

Source: B §11. Works sites and sheds; the workers' homes are Dwellings (rural poor). Quarry and lime kiln are under
Crafts, ceramics and stone.

### Forest, mines and smelting

- **Charcoal kiln, black charcoal (kuro-zumi-gama)**: earth dome kiln on a hillside, smothered to cool. `site` in the
  forest. Items: earth or clay dome kiln with a flue, stack of cut wood, straw or kaya charcoal bales (sumi-dawara),
  rakes (eburi) and long hoes, thatched shelter hut. [WORLD_CATALOGUE]
- **Charcoal kiln, white charcoal (shiro-zumi-gama / binchō)**: stone kiln; charcoal pulled out red-hot and smothered in
  sand and ash (keshi-bai); Kishū binchō-tan from Genroku (in era). `site`. Items: stone and clay kiln, long iron rake,
  sand-and-ash quench pit, oak (ubame-gashi) stacks.
- **Charcoal burner's hut (sumiyaki-goya)**: shelter by the kiln. Items: small hearth, straw mats, water jar, axe and
  saw. (Duplicate of Dwellings, charcoal-burner's kiln hut: merged there, see Seams; not counted twice.)
- **Logging camp (soma-goya)**: fellers and log-skidders in state or domain forests. `site`. Items: axes (ono), felling
  saws (spread in Edo; axes primary), wedges, log chutes (shura) down a slope, camp hut. (Camp hut = Dwellings,
  logging-crew camp hut.)
- **Timber rafting station (ikada-ba)**: logs bound into rafts on rivers. Riverbank `site`. Items: log rafts, rope and
  vine bindings, poles, shed. (Raftsmen's hut: Dwellings.)
- **Gold or silver mine (kinzan, ginzan)**: Sado, Iwami, Ikuno; Izu's gold mines (Toi, Yugashima) peaked in the early
  17th c. `site`. Items: adit mouth (mabu) with timber supports, shell oil lamps (kantera), picks and hammers (tsuchi,
  tagane), ore baskets, drainage pump (Archimedes-screw suishō-rin or bamboo pumps), ore-crushing stones and grinding
  mills, women's sorting and washing sheds with sluices, smelting hut (fuki-ya) with small furnaces and bellows.
  `[outside 1680-1750: largely; peak earlier]` (verify how active)
- **Copper mine and smelter (dōzan)**: Besshi opened 1691 (in era); Ashio. `site`. Items: as gold mine, plus roasting
  beds, larger smelter, copper ingots.
- **Sulphur workings (iō-yama)**: sulphur dug from volcanic vents for match-tinder and gunpowder; Hakone's Ōwakudani
  (verify whether worked in 1730). `site`. Items: sulphur crust, baskets, melting pot, shelter.
- **Iron smelter (tatara, takadono)**: iron-sand smelting in a clay furnace rebuilt every firing; balance bellows
  (tenbin-fuigo) dated 1691 (in era). `site`: tall barn over the furnace, iron-sand washing channels (kanna-nagashi) on
  the hillside. Items: clay furnace, two balance bellows, charcoal stores, iron-sand heaps, the bloom (kera), sacred
  tree and shrine (Kanaya-go). `[off-map: Izumo and the Chūgoku mountains]`
- **Hunter's hut (ryōshi-goya / matagi-goya)**: boar, deer, bear hunters; guns needed a domain licence
  (teppō-aratame); traps and spears common. `rural` forest hut. Items: spears, snares and deadfall traps, skinning
  board, drying hides, meat hanging to smoke, small hearth, straw boots. (Merged with Dwellings, mountain hunter's hut;
  see Seams; not counted twice.) Matagi `[off-map: Tōhoku]`.

### Farm processing

- **Silkworm house (yōsan-ya / kaiko-beya)**: farmhouse upper floor or a special room with tray racks. `rural`. Items:
  bamboo tray racks (kaiko-dana), flat woven trays (ebira / kaiko-kago), mulberry leaves in baskets, leaf-chopping board
  and knife, straw cocooning frames (mabushi), charcoal brazier for warmth. Tall multi-storey sericulture farmhouses are
  `[outside 1680-1750: 19th c.]` (see Dwellings, sericulture farmhouse, and Contradictions).
- **Indigo-processing barn (sukumo-ya / ai-nedoko)**: Awa (Tokushima) indigo: leaves composted for months on a clay
  floor, turned and watered into sukumo. `rural` `site`: tall barn with a thick clay floor. Items: clay composting bed
  (nedoko), wooden shovels and rakes, water buckets, straw mat covers, sukumo in straw bags, leaf drying yard.
  `[off-map: Awa / Shikoku]` (region tag added by merge)
- **Safflower processing (benibana)**: petals washed, fermented, pressed into cakes. `rural`. Items: tubs, straw mats,
  beni-mochi press, drying boards. Regional (Yamagata) `[off-map]`. (B: merge.)
- **Wax works (rō-shibori, haze)**: crushes and steams sumac berries, presses out wax, sun-bleaches it; Kyushu and
  Shikoku. `rural` `site`. Items: stamp mill or mortar, steamer, wedge press (shime-gi) with hemp bags, wax cakes,
  bleaching field of shallow trays. `[off-map]` (region tag added by merge)
- **Oil press (abura-shime-ya)**: rapeseed and sesame for lamp and cooking oil; oil-cake sold as fertilizer. Town
  workshop or `rural`; doma. Items: roasting pan, stone mortar or water stamp, steamer, hemp or straw bags, wedge press
  (shime-gi) driven by a big hammer, oil casks, oil-cake stack. Water-driven oil mills of Hyōgo and Nishinomiya are
  `[outside 1680-1750: c.1790s+]` (verify). [WORLD_CATALOGUE]
- **Tea processing shed (seicha-goya)**: steaming, hand-rolling, drying on a heated board; Uji, Shizuoka (Nagatani
  1738). `rural`. Items: steamer on a cauldron, cooling fan, paper-lined drying board (hoiro) over a charcoal box, woven
  trays, tea jars. (Overlaps Dwellings, tea-grower's farmhouse.)
- **Tobacco drying shed**: leaves hung on ropes under the eaves or in a barn. `rural`. Items: strung leaves, poles,
  bales. (B: merge with farm barn; see Dwellings, drying shed.)
- **Sugar press (satō-shime)**: Items: ox-driven roller press, boiling pans. `[outside 1680-1750 for the main islands:
  domestic sugar spread after Yoshimune's promotion and the Sanuki wasanbon of the 1790s; Satsuma and Ryūkyū earlier]`
  (B: probably cut.)
- **Umeboshi works (ume-boshi)**: plums salted in vats, dried on mats in summer; Odawara's Soga plums nearby. `rural`.
  Items: salting vats with stones, big bamboo drying mats (su) on trestles, jars.
- **Thatch meadow and store (kaya-ba)**: common land where thatch grass was cut, stored in stooks. Items: stooks,
  sickles, grass barn. (See Civic, village commons.)
- **Mushroom logs (shiitake)**: Items: oak logs leaning in a shaded frame. `[outside 1680-1750: Izu Amagi shiitake
  from the 1790s]` (verify)

### Salt

- **Salt field, spread type (agehama)**: sea water carried to a levelled sand field, spread, dried; salty sand raked
  into a filter box. Coastal `site`. Items: levelled sand field, sea-water buckets on a shoulder pole (shio-oke), wide
  rakes (manga), filter box (numai / tare-bune) with a tap, brine vats.
- **Salt field, tidal type (irihama)**: Seto Inland Sea (Akō); embanked fields filled by tide through channels. `site`.
  Items: embankment, sluice gate, ditches, sand beds, as agehama. `[off-map: Seto]` (B: regional; merge.)
- **Salt-boiling hut (kama-ya)**: boils brine in a big flat pan. Coastal `site`. Items: wide shallow pan (iron, or the
  Inland Sea "stone pan" of stones and clay), firebox under it, huge pine and pine-needle fuel stacks, brine vats,
  draining baskets for wet salt, salt store (shio-naya), straw salt bags.

### Coast and river fishing

- **Fishing-village net shed (ami-goya / naya)**: net storage and repair. Coastal `site`. Items: nets on poles, wood or
  gourd floats (uki), clay or stone sinkers, oars, baskets, tannin tub. (Same as Dwellings, net shed: merged, see
  Seams; not counted twice.)
- **Fish-drying racks (himono-ba)**: split fish dried on racks; sardines dried on the beach. Coastal `site`. Items:
  bamboo racks, salt tubs, split fish, baskets.
- **Dried-sardine fertilizer works (hoshika)**: huge Kujūkuri sardine catches dried on sand or boiled and pressed.
  Coastal `site`. Items: seine nets, drying sand, boiling cauldrons, presses, straw bags. (Owner: Dwellings, net-boss
  house.)
- **Dried-bonito works (katsuobushi-goya)**: boiling, deboning, smoking over hardwood fires for days, mould curing
  (credited to Tosa c.1674, in era); Izu's Tago and Nishi-Izu on the map. Coastal `site`. Items: boiling cauldron,
  filleting boards and knives, bamboo trays, smoke room with a hearth, shelves of smoked fillets.
- **Nori farm and drying yard (nori-hibi, nori-hoshi)**: seaweed grown on bamboo stakes (hibi) at Shinagawa and Ōmori
  (c. Genroku–Kyōhō, in era); chopped, dried in sheets on reed screens on frames. Coastal `site`. Items: hibi stakes in
  the sea, small boats, chopping boards and knives, tubs, wooden frames (waku), reed mats (su), racks leaning to the
  sun. (Grower's cottage: Dwellings.)
- **Whaling station (kujira-gumi)**: organized net whaling (Taiji, Kyushu, Tosa); flensing on the beach. `site`. Items:
  flensing sheds, oil cauldrons, huge knives, whale-bone racks. `[off-map]` (B: probably cut.)
- **Oyster beds (kaki)**: Hiroshima oyster farming; oyster boats sold in Osaka. `[off-map]` (B: cut candidate.)
- **Fish weir (yana)**: river weir of bamboo slats for sweetfish (ayu) and eels. River `site`. Items: bamboo slat
  ramp, stakes, baskets, watch hut.
- **Cormorant-fishing house (u-shō)**: cormorant masters on the Nagara and other rivers. Riverside house with cages.
  Items: cormorant baskets, torches (kagaribi) and iron fire baskets, narrow boats, leashes. Regional. (B: cut
  candidate.)

## == Shinto ==

Source: C §2. Scale ladder: stone kami marker → hokora → house-plot shrine → field shrine → village chinju → town shrine
→ provincial first shrine (ichinomiya) / great shrine. In 1730 most shrines above village size also carry Buddhist
buildings (see Buddhist buildings inside shrines, below, and §4 Seams).

### Shrine types by scale

- **Roadside or field micro-shrine (hokora / hokura)**: a single kami's dwelling at a field corner, tree root, spring
  or pass. Space: miniature wooden or stone shrine house 0.3–1 m high on a stone base; no interior. Items: small doors,
  gohei wand, shimenawa, sake cup, rice or salt dish, small vase of sakaki, fox figures (Inari). [WORLD_CATALOGUE §1.5]
- **House-plot shrine (yashiki-gami)**: the family's tutelary kami (often Inari) in the corner of a farm or samurai
  yard. Space: hokora under a tree, sometimes in a small roofed shed (saya). Items: as hokora, plus mini-torii, fox pair.
  (Dwellings, household shrine in the yard, merged here.)
- **Alley Inari (roji Inari)**: Edo back-alley shrine for the tenement court. Items: tiny red hokora, mini torii, fox
  pair, offering shelf, lantern hook. (Part of Dwellings, shared alley facilities.)
- **Village tutelary shrine (chinju / ujigami-sha)**: the village kami; centre of the festival year and the shrine guild
  (miyaza); most have no resident priest (a villager serves in rotation, or a travelling priest comes; see Dwellings,
  farmer-priest's house). Space: torii + short sandō + a small honden inside a sheltering hall (saya-dō / ōi-ya) +
  sometimes a haiden; board floors; bare-earth precinct; big sacred tree (goshinboku); an offering-sumo ring (hōnō-zumō)
  in some. Items: honden set (below); haiden with bell rope, offering box, ema, straw mats (goza), drum; stone lanterns;
  stone basin.
- **Town shrine (machi no jinja)**: chinju for several chō, with a resident priest's house, kagura stage, mikoshi store,
  sub-shrine row, festival ground. In Kyoto / Osaka the float store sits in the ward, away from the shrine. (assumed)
- **Major shrine complex (taisha, ichinomiya, sōja)**: full precinct behind a tower gate; cloisters; many sub-shrines;
  Buddhist buildings; priests' residences; Noh or kagura stage; festival grounds. On our map: Atsuta (Miya), Mishima
  Taisha, Suwa Taisha (Nakasendō region), Kasuga, Kitano, Yasaka (Gion-sha), Hie, Sengen at Fuji.
- **Tōshōgū (Ieyasu shrine)**: many domains built one; gongen-zukuri (honden and haiden joined by a stone-floored
  ishi-no-ma), rich carving and colour, a karamon. Nikkō (1636 rebuild) is the extreme.
- **Ise (Jingū)**: unpainted shinmei-zukuri, thatch, raw hinoki, multiple fences; rebuilt 1729 (see Layouts 2.10).
  Unique; no Buddhist buildings allowed near it.
- **Mountain summit / pass shrine (okumiya, tōge no yashiro)**: stone or small board shrine on a peak or pass, often
  with a windbreak stone wall and a pilgrim hut (Buddhist, roadside structures). Items: iron swords and votive plaques
  left by climbers, straw sandals, coins, small bell.

### Buildings inside a shrine precinct

- **Main sanctuary (honden / shinden)**: houses the kami's object (shintai); closed to worshippers. Space: raised board
  floor on posts, veranda (en) with rail, steps with a small roof (kōhai) in nagare style; styles shinmei, taisha,
  kasuga, nagare, hachiman, hie, gongen. Items: closed inner doors with metal fittings, bamboo blinds (misu), shintai
  box (mishōtai) in a zushi, bronze mirror on a stand, gohei on stands, sakaki vases, eight-legged offering tables
  (hassoku-an), white-wood trays (sanbō), sake flasks (heishi), clay plates (kawarake), crest curtains (tobari), inner
  wooden guardian lion-dogs (komainu), hanging lanterns.
- **Worship hall (haiden)**: where worshippers and priests pray before the honden. Space: open-fronted board-floored
  hall, often wider than deep; sometimes an earth passage through it (wari-haiden). Items: large slatted offering box
  (saisen-bako), bell with thick cloth rope (suzu; flat gong waniguchi on older halls), big drum on a stand, ema on
  walls and beams, donor boards, rolled mats and round straw cushions (enza), crest lanterns, sakaki-offering stand,
  sword or arrow offering, name board (gaku) over the entrance.
- **Offering hall (heiden)**: narrow hall between haiden and honden where offerings (heihaku) are placed. Items:
  offering tables, sanbō stacks, cloth offerings on stands, gohei.
- **Stone-floored link hall (ishi-no-ma)**: gongen-style connector; stone or plaster floor lower than the halls. Items:
  hanging lanterns and blinds only.
- **Kagura stage (kagura-den / maidono)**: sacred dance and music for the kami. Space: raised square stage open on 3–4
  sides, board floor, dressing room (gakuya) behind. Items: large drum (ōdaiko) and small drums, flutes (fue) on a rack,
  kagura bells (suzu) on a stand, masks on pegs, gohei, folded fans, lanterns.
- **Noh stage (nōbutai) at great shrines**: square roofed stage, bridgeway (hashigakari), painted pine backboard, three
  small pines along the bridge; Itsukushima's stage is 1680 (in window). Items: the painted pine, drums, mask box
  (dressing only), curtain (agemaku).
- **Ema hall (ema-dō)**: open pavilion hung with large votive paintings (Momoyama on). Items: big framed ema (horses,
  ships, battles, festivals), small ema, benches for pilgrims.
- **Purification pavilion (temizuya / chōzuya)**: four-post roof over a stone basin fed by a bamboo pipe. Items: stone
  basin, wooden ladles on a rack (hishaku), small towel bar (assumed), donor inscription. (Temples have the same.)
- **Offering kitchen (shinsen-sho / shinsen-den)**: where food offerings are cooked. Items: kamado, water jars,
  white-wood cutting boards, sanbō and kawarake stacks, rice steamer, sake casks.
- **Portable-shrine storehouse (mikoshi-gura / mikoshi-den)**: kura or roofed shed with wide doors. Items: mikoshi on
  its carrying poles on trestles, lion-dance heads (shishigashira), festival lanterns, banners on poles, drums, spare
  poles.
- **Treasure store (hōko / shinpō-gura)**: log or plastered kura on stilts (azekura in old shrines). Items: sword
  boxes, mirror boxes, costume chests, scrolls, dedicated armour.
- **Priests' residence and office (shake / kannushi-yashiki; "shamusho" is the modern name)**: a house (Dwellings,
  shrine-priest family house) with an office room. Items: talisman-making desk, printing blocks and brushes, stacks of
  paper amulets (ofuda), registers, shrine seal, ritual robes on a rack.
- **Talisman / amulet window (juyo-sho)**: mostly modern as a separate building (assumed); in 1730 amulets sold from the
  priest's house or a small booth at the haiden. Items: ofuda stacks, omamori, counter.
- **Sub-shrines (sessha, massha)**: small shrines along the precinct, one hokora each or a row under one roof
  (narabi-sha). Items: as hokora.
- **Distant-worship point (yōhai-jo)**: a stone or small fence facing a far shrine or mountain. No interior.
- **Pilgrims' overnight hall (sanrō-den / tsuya-dō)**: board-floored hall for vigils. Items: straw mats, hearth,
  lanterns, pegs for hats and straw raincoats.
- **Tower gate (rōmon) / guardian gate (zuishin-mon)**: two-storey or roofed gate with seated archer guardians
  (zuishin) in side bays. Items: two zuishin statues behind grilles, hanging lanterns, name board.
- **Cloister (kairō) and sacred fence (tamagaki, mizugaki)**: roofed corridor or lattice / board fence round the inner
  sanctum.
- **Sacred bridge (shinkyō)**: vermilion arched bridge reserved for the kami or the lord at big shrines.
- **Festival float store (yama-hoko-gura)**: Kyoto / Osaka wards; tall kura holding a dismantled float. Items: wheels,
  pole timbers, rolled tapestries in boxes, lanterns.
- **Sumo ring (dohyō) at a village shrine**: earth ring of straw bales, sometimes a four-post roof. (assumed common for
  offering sumo)

### Buddhist buildings inside shrines (1730 syncretism)

- **Attached administering temple (bettō-ji / jingū-ji)**: monks who run the shrine, living beside it; ordinary temple
  buildings (see Buddhist). Gion-sha was run by the Tendai Kanshin-in; Tsurugaoka Hachiman had a pagoda and many monk
  houses.
- **Pagoda at a shrine**: e.g. Itsukushima (1407), Hachiman shrines. (Same building as Buddhist, pagoda; not counted.)
- **Original-Buddha hall (honji-dō) / goma hall at a shrine**: hall for the Buddha of whom the kami is a manifestation;
  esoteric fire-ritual hall. Items: as Buddhist, goma-dō.

### Non-building sacred structures and cult tells (props, not counted)

- *Structures (names only):* torii (shinmei, myōjin, ryōbu, sannō, Kashima, hachiman; stone, wood, vermilion; tunnels
  of donated torii at Inari shrines), shimenawa (incl. the thick Izumo type), shide paper strips, komainu (stone
  lion-dogs, a/un pair), kitsune pair (Inari), ox (Tenjin), monkey (Hie / Sannō), deer (Kasuga), stone lanterns
  (kasuga-dōrō), hanging bronze lanterns, onbashira pillars (4 per Suwa shrine, Shinano), sacred tree with shimenawa,
  sacred rock (iwakura), stone-pile boundary, offering stones, stone steps, donor stones (hōnō-hi), sacred horse stable
  (shinme-sha, live or wooden white horse), sacred pond with a Benten island.
- *Inari tell:* vermilion, fox pairs with a key or jewel, rows of small torii, fried-tofu offering dishes.
- *Sea tell (Konpira / Sumiyoshi / Ebisu):* ship ema, anchors, net floats, sea-bream offerings.
- *Fire tell (Akiba / Atago):* fire-prevention ofuda at every door, tengu images; popular in fire-prone Edo.
- *Mountain / water tell (Yama-no-kami / Suijin):* stone markers, offered axes or sickles, bamboo water pipes, snake
  motifs.

## == Buddhist ==

Source: C §3. Scale ladder: roadside Jizō → hall (dō) with no priest → hermitage (an) → village temple → town temple →
sub-temple (tatchū) → major temple / head temple (honzan). Every household is registered at a temple (terauke), so
every village has or belongs to one.

### Temples by scale

- **Hermitage (an / iori / anshitsu)**: a priest's, nun's or lay recluse's hut, attached to a temple or alone in the
  hills; Bashō-an (1680s, Fukagawa) is the period icon. Space: 1–3 rooms, thatch, small board or tatami room with a
  butsudan niche, earth kitchen corner. Items: small Buddha in a zushi, incense burner, candle stand, sutra desk, bowl
  gong, prayer beads, brazier or hearth, writing box, a few books. (Same building as Dwellings, grass hermitage: counted there,
  not counted here.)
- **Unstaffed hall (dō / dōshō)**: Jizō-, Kannon-, Yakushi-, Amida-, Kōshin- or Fudō-dō in a village or on a road, kept
  by villagers; also the village meeting place. Space: 2 × 2 or 3 × 3 ken, one room, board floor, raised altar at the
  back, veranda. Items: statue on an altar shelf, bowl gong, incense burner, candle stands, vases, votive plaques,
  hanging lanterns, straw cushions, donation box, rows of small votive statues.
- **Village temple (mura-dera; often Sōtō Zen, Jōdo, Shingon or Shinshū)**: registers families (terauke), funerals and
  memorial rites, keeps the graveyard, often teaches children. Space: main hall and priest's quarters joined or under
  one roof (hondō-kuri), bell tower, small gate, graveyard behind. Items: main-hall and kuri sets (below), plus death
  register (kakochō) and copies of the temple registers (shūmon aratame-chō).
- **Town temple**: separate gate, main hall, kuri, bell tower, sometimes a founder's hall, a wall-hemmed graveyard;
  tera-machi rows (Layouts 2.7).
- **Sub-temple (tatchū / shiin)**: small walled temple inside a big temple's grounds, a memorial to a past abbot or
  patron family: gate, small hall, abbot's quarters with a garden, kitchen. Kyoto Zen head temples have 10–40 each
  (assumed range).
- **Major complex / head temple (honzan, daijiin)**: full precinct, walls, several gates, dozens of buildings,
  sub-temples, monks' schools (danrin), gardens.
- **Pilgrim-lodging temple (shukubō)**: a sub-temple that also lodges pilgrims (Kōyasan, Zenkōji). Items: altar room
  with statue, big tatami halls, sutra books. (Lodging side merged here: see Seams; Dwellings, oshi house is the
  shrine-side twin.)
- **Nunnery (ama-dera) and divorce temples (kakekomi-dera)**: Tōkeiji (Kamakura) and Mantokuji (Kōzuke) took in wives
  fleeing marriages. Walled, one gate, main hall, nuns' quarters.
- **Mausoleum temples (bodaiji, reibyō)**: a daimyo family's temple with a mausoleum enclosure (tamaya). Shogunal:
  Zōjōji (Hidetada; Ienobu 1712, Ietsugu 1716) and Kan'eiji (Ietsuna 1680, Tsunayoshi 1709), all in window.
- **Memorial temple for the unclaimed dead (muen-dera)**: Ekōin (1657, Ryōgoku) for the Meireki fire dead; mounds and
  memorial stones.
- **Shinshū lay chapel (dōjō)**: village Jōdo Shinshū meeting chapel, house-like, run by lay members. (Split out from
  C's Shinshū sect note so it is visible as a type; items as a small Shinshū hall: Amida scroll, altar, tatami, drum.)
  (assumed items)

### Buildings in a temple precinct

- **Main gate, two-storey (sanmon)**: Zen and Pure Land head temples; upper floor is a shrine room with the Shaka triad
  and 16 arhats, reached by a steep stair in a side hut. Items: statues in a row, ceiling paintings, altar table,
  incense burner.
- **Guardian-king gate (niōmon)**: two muscular guardians behind wire or lattice. Items: statues, huge straw sandals
  (ō-waraji) offered by pilgrims, hanging lanterns, paper slips on the grille.
- **Outer / middle / Chinese / imperial gates (sōmon, chūmon, karamon, chokushimon)**: simple gate, inner gate,
  cusped-gable gate, imperial-messenger gate kept shut.
- **Main hall (hondō; butsuden in Zen; kondō in old temples; Amida-dō, Kannon-dō etc.)**: enshrines the principal image
  (honzon); rites and congregational prayer. Space: inner sanctum (naijin) with raised board floor and altar dais;
  outer worship space (gejin) with tatami (Pure Land, Shinshū) or boards; Zen butsuden has a stone-tiled floor and
  people stand. Items: principal statue on a Sumeru dais (shumidan), shrine cabinet (zushi) with doors, canopy
  (tengai), openwork hanging ornaments (keman), banners (ban), the three altar pieces (mitsugusoku: incense burner,
  candle-stand pair, flower-vase pair) or the five-piece set, lotus vase, offering stands (kuge-dai), front table
  (maezukue), sutra desk (kyōzukue), priest's platform (raiban), bowl gong (keisu / kin) on a cushion, wooden-fish drum
  (mokugyo; spread via Ōbaku from the 1650s), hand bells, cymbals, large drum, rows of memorial tablets (ihai), altar
  cloths (uchishiki), hanging lanterns, donation box, votive plaques, prayer-bead rack, zabuton rows.
- **Lecture / Dharma hall (kōdō; hattō in Zen)**: large sermon hall; Zen hattō has a raised abbot's seat platform, a
  dragon on the ceiling, stone floor. Items: preaching seat (kōza) with steps, lectern, drums, bells, rows of cushions.
- **Founder's hall (kaisandō / mieidō / soshidō / daishidō)**: houses the founder's portrait statue; in Pure Land and
  Shinshū head temples it is the largest building (Chion-in mieidō 1639; Higashi Honganji). Items: founder's seated
  statue in a zushi, portraits, altar set, tablets.
- **Priests' quarters and kitchen (kuri / kuin)**: kitchen, office and living quarters; the working heart. Space: huge
  earth-floored kitchen with exposed beams and a smoke gable; board office; tatami living rooms; guest room. Items:
  rows of kamado with big iron cauldrons, water jars, rice-washing tubs, huge rice-steaming baskets, cutting boards,
  stacked lacquer meal trays (zen), kitchen guardian statues (Idaten in Zen; Daikokuten), wooden cloud-shaped gong
  (unpan) and hanging board struck with a mallet (han) in Zen, account books, writing desk, temple seal box.
- **Abbot's quarters (hōjō)**: Zen six-room tatami building facing a raked-gravel garden; central room has an altar.
  Items: fusuma paintings (allowed here), altar, tokonoma with scroll, desk, fly whisk (hossu), teaching stick
  (keisaku / kyōsaku), folding chair (kyokuroku).
- **Guest hall (kyakuden) and study hall (shoin)**: tatami reception rooms with alcove and staggered shelves. Items:
  tokonoma scroll, flower vase, armrest, tea utensils, screens.
- **Monks' hall / meditation hall (sōdō / zendō)**: Zen: long raised platforms (tan) along both walls, one tatami per
  monk, bedding in cupboards above, central Monju image. Items: sitting cushions (zafu), clappers (taku), small bell,
  incense sticks as timers, the monitor's (jikijitsu) stick.
- **Refectory (jikidō / saidō)**: long hall with low tables. Items: nested bowls (ōryōki), meal boards, hanging wooden
  fish (gyoban / kaipan) struck for meals (Ōbaku / Zen), statue of Binzuru or Kasyapa.
- **Monks' dormitory (sōbō / ryō)**: rows of small rooms (like a Dwellings row house) at big teaching temples.
- **Sutra repository (kyōzō / kyōko)**: stores the canon. Space: small square hall or plastered kura, many with a
  revolving octagonal sutra case (rinzō) on a pivot, Fu Daishi and sons at the entrance. Items: rinzō, shelves of
  numbered wooden sutra boxes, folded (orihon) sutras; the Ōbaku Tetsugen edition of the canon (completed 1681) spread to
  many temples in our window.
- **Bell tower (shōrō / kanetsuki-dō)**: open four-post pavilion (or with a flared skirt wall, hakama-goshi) on a stone
  platform. Items: great bronze bell (bonshō), suspended log striker (shumoku) on ropes, rope, stone step. Also the town
  time bell (see Civic). (Bell casting: Crafts, bell caster.)
- **Drum tower (korō / taikorō)**: two-storey pavilion with a big drum; common in Shinshū and Zen. Items: large drum on
  a stand, drumsticks, stair.
- **Pagoda (tō: three-storey sanjūnotō, five-storey gojūnotō)**: relic monument, not entered. Space: square core round
  the central pillar (shinbashira); ground-floor altar with four Buddhas facing out; upper floors are timber lattice
  and ladders. Items: four statues, painted pillars (sometimes), railing, bronze finial (sōrin) outside, wind bells at
  eave corners. (Also at shrines.)
- **Two-storey treasure pagoda (tahōtō)**: Shingon / Tendai; square lower storey, round collar, square roof. Items:
  Dainichi statue on an altar.
- **Esoteric fire-ritual hall (goma-dō)**: Shingon / Tendai and shugendō. Items: goma hearth altar (goma-dan) with a
  copper hearth, stacked goma sticks, Fudō statue with flame halo, vajras and bells on a table, soot-blackened ceiling,
  donors' board. (Also at shrines as honji-dō.)
- **Kannon / Yakushi / Jizō / Fudō / Enma halls (dō)**: single-deity halls. Enma-dō: Enma the judge of hell and the hag
  Datsueba; items: statues, a pair of judgement scrolls (hell paintings), mirror. Yakushi-dō: medicine-jar statue,
  votive eyes or limbs (also the hot-spring town's hall).
- **Memorial-tablet hall (ihai-dō / reiden)**: stepped shelves of family memorial tablets. Items: tablets, small
  lanterns, altar.
- **Mausoleum (reibyō / tamaya / otamaya)**: walled enclosure with a gate, a small richly decorated hall or a stone
  stupa (hōkyōintō / gorintō) on a platform. Items: rows of stone lanterns donated by retainers, worship-hall table,
  karamon.
- **Temple bathhouse (yokushitsu / yudono)**: Zen seven-hall set; steam bath (mushiburo) with slatted floor over a
  boiler, and a tub room; Tōfukuji's survives from 1459. Items: slatted floor, iron cauldron and fire pit, wooden
  buckets, small statue of Batsudabara (bath bodhisattva), towel pegs.
- **Latrine (tōsu / sesshin)**: Zen rows of floor pits (Tōfukuji's 14th-c. latrine survives). Items: pit slots, water
  jars, statue of Ususama Myōō, ladles. (In game, a board building with slots.)
- **Ordination platform (kaidan-in)**: only at a few major temples; walled stone terrace inside a hall.
- **Worship-stage hall (kake-zukuri / butai-zukuri)**: hall built out over a cliff on a timber lattice (Kiyomizu-dera,
  rebuilt 1633). Interior as a main hall.
- **Temple tea room (chashitsu)**: 2–4.5-mat room with small crawl-in door. Items: sunken hearth, kettle, tea caddy,
  scroll, flower. (Same shell as Dwellings, tea hut.)
- **Temple storehouse (hōzō / kura)**: plastered kura. Items: statue crates, festival goods, lacquered chests.
- **Kōshin hall (kōshin-dō)**: for the 60-day Kōshin vigil groups. Items: Shōmen Kongō statue, three monkeys, vigil
  mats, brazier.
- **Benten hall on a pond island**: small hall on an island reached by a bridge.
- **Tutelary shrine inside a temple (chinju-sha)**: a small shrine in the temple grounds (syncretism); a Shinto hokora
  or small honden.
- **Graveyard (bochi) and its hut (sotoba shed)**: graves (WORLD_CATALOGUE §1.6), six Jizō (roku Jizō) at the entrance,
  water point with buckets and ladles, rack of tall wooden memorial slats (sotoba), hut for tools and a coffin bier
  (kan-dai) (assumed), pyramid of unclaimed-grave stones (muen-botoke).
- **Temple school room (tenarai-dokoro)**: many terakoya ran in the temple's guest room or kuri. (Merged into Civic, terakoya; not counted.)

### Sect modifiers (change the set, not new building types; not counted)

- *Zen (Rinzai, Sōtō):* the seven-hall set (shichidō garan): sanmon, butsuden, hattō, hōjō, kuri, sōdō, yokushitsu,
  tōsu, plus kyōzō and bell tower, on one axis; stone floors in butsuden and hattō; raked gravel at the hōjō; gongs
  unpan, han, gyoban. Sōtō is the commonest village sect in the east.
- *Ōbaku Zen (Manpukuji, from 1661):* Ming Chinese style: chairs and tables, round windows, hanging wooden fish
  (kaipan), Chinese lattice railings, peach-shaped openings, Chinese inscription boards. Very current in 1730.
- *Pure Land (Jōdo):* huge mieidō, big sanmon, tatami gejin for chanting crowds, large bells (Chion-in's 1636 great
  bell), Amida triad, hanging lotus ornaments.
- *True Pure Land (Jōdo Shinshū, Honganji):* no pagoda, no goma hall, often no bell tower but a drum tower; founder's
  hall bigger than the Amida hall at head temples; vast tatami gejin; huge kuri for communal meals; few graves and in
  principle no grave rites (Shinshū regions cremated more); village lay dōjō (entry above).
- *Nichiren (Hokke):* founder's hall central; daimoku stone pillar carved "Namu Myōhō Renge Kyō"; Kishimojin hall; fan
  drums (uchiwa-daiko) instead of mokugyo; gohonzon calligraphy mandala as main object in small temples.
- *Shingon and Tendai (esoteric):* mountain sites; tahōtō; goma-dō; inner sanctuary (okunoin) up the mountain; Kōbō
  Daishi halls; two mandala scrolls facing each other (Taizōkai / Kongōkai); esoteric altar (dan) with vajras, bells,
  five vases.
- *Shugendō (yamabushi):* practice halls (gyōja-dō, En-no-Gyōja statue), conch shells, ringed staffs (shakujō),
  waterfall and cliff practice sites with chains (kusari-ba), summit huts. (Homes: Dwellings, yamabushi hut and
  village household.)
- *Ji-shū and others:* minor; odori-nenbutsu stages (assumed). C: skip unless needed.

### Roadside, pilgrim and folk structures

- **Roadside Jizō (michi-no-Jizō)**: stone figure with red bib and cap, small offering stone, sometimes under a tiny
  roof (Jizō-dō). Items: bib, cap, flowers, coins, water cup, pinwheel (assumed Edo).
- **Pilgrim overnight hall (tsuya-dō / henro-goya / zenkon-yado)**: free shelter on the Shikoku and Saigoku routes: a
  roofed board platform or hut. Items: straw mats, fire pit, hook for hats, donation box, Kōbō Daishi statue. (Merges
  with Lodging, charity lodging, and Shinto, pilgrims' overnight hall: see Seams.)
- **Mountain pilgrim hut (murodō)**: stone-and-timber hut high on a sacred mountain; Tateyama's (rebuilt 1617/1726) is
  Japan's oldest mountain hut. Items: sleeping platform, hearth, straw bedding, pilgrim staffs, small altar.
- **Waterfall practice site (taki-gyōba)**: Fudō statue at the fall, small changing hut, shimenawa across the fall.
- **Cliff Buddhas and cave halls (magaibutsu, iwaya-dō)**: a hall built against or into a cliff (assumed common in
  Shugendō areas).
- *Stone monuments (props, not counted):* six Jizō row (roku Jizō) at cemetery entrances and village edges;
  horse-headed Kannon (Batō Kannon) stones on pack-horse roads for dead horses (many on the Nakasendō); kōshin stones
  (kōshin-tō), 23rd-night stones (nijūsan-ya tō), memorial stupas (kuyō-tō), nenbutsu and myōgō stones (village-group
  monuments, mostly Edo); boat-shaped grave Buddhas, gorintō and hōkyōintō in graveyards.
- *Outdoor items (props, not counted):* stone and bronze lanterns, water basin (chōzubachi), incense-burner pavilion
  (big bronze jōkōro under a roof, at busy temples), offering-coin box, flagpole banners (nobori), prayer-slip stands,
  rows of small donated Jizō; memorial stones for the Kyōhō famine (kiga kuyō-tō, 1732) would appear right after the
  anchor year (neutral, very local); temple exhibitions (kaichō; Narita in Edo from 1703) set up temporary stands and
  banners (event dressing).

## == Government ==

Source: C §4. What reads as "official" (PLAYBOOK §2.2): black boards, a heavy gate, a white-gravel court, a genkan with
a shikidai step, the three capture tools (sodegarami, sasumata, tsukubō) on a rack, crest curtains, a notice board out
front. The honjin and waki-honjin (C §4.3) are listed under Lodging.

### Shogunal and city administration

- **Town magistrate's office (machi-bugyōsho)**: Edo's North and South offices (Ōoka Tadasuke South Magistrate
  1717–1736, in office in 1730); also Kyoto, Osaka, Nara, Sakai, Fushimi, Nagasaki, Sado, Uraga. Police, courts, city
  administration. Space: black nagaya-mon gate with guard rooms; front court; genkan; office wings for yoriki and dōshin
  (their homes: Dwellings, dōshin house); trial court = white-gravel yard (oshirasu) below stepped floor levels
  (commoners kneel on a straw mat on the gravel, samurai on the veranda, the magistrate in the tatami room above); the
  magistrate lives at the rear of the same compound. Items: magistrate's raised seat and armrest, low writing desks,
  inkstones, stacked document boxes (bunko), record ledgers, the three capture tools on a rack at the gate, crest
  curtain (maku) at the gate, torches and lanterns with the office name, straw mats on the gravel, rope bundles for
  tying suspects (hojō), small holding room, clerk's counter, messenger bench, hanshō bell or drum.
- **Shogunal council chamber (hyōjōsho)**: highest court (Tatsunokuchi, Edo); the bugyōsho pattern, grander. The
  petition box (meyasubako, 1721) set at its gate on the 2nd, 11th and 21st of each month. Items: locked petition box (a
  small lidded box on a stand), bench, guard.
- **Finance magistrate's office (kanjōsho)**: tax, roads, rivers, daikan oversight. Items: rows of abacus, ledgers,
  scales, maps rolled in boxes, seal box.
- **Shrine and temple magistrate (jisha-bugyō)**: served from the daimyo's own residence; no separate building. (Note
  only; not counted.)
- **Kyoto deputy (shoshidai) and Osaka castellan (jōdai) residences-offices**: big walled yashiki with offices near
  Nijō and Osaka castles.
- **Holding and interrogation stations (ōbanya / sayadō)**: several in Edo; a board building where constables held and
  questioned suspects before sending them on. Items: lattice holding cell, rope, capture tools, desk, brazier, lamp.
- **Mints (kinza, ginza, zeniza)**: gold, silver, copper-coin mints (Ginza in Edo and Kyoto). Walled works with
  offices, furnaces, guards. Items: coin moulds, scales, ingot trays, coin strings, account books. (C: the mint
  industry could be B's; the guarded office is here.)
- **Foreign compounds at Nagasaki: Dejima (1636) and Tōjin-yashiki (1689)**: walled; one guarded gate with an
  inspection office. Items: gate guard room with ledgers and seals, capture tools. `[off-map: Nagasaki]` (region tag
  added by merge)

### Domain and district administration

- **Shogunal district office / jinya (daikansho, gundai)**: a shogunal intendant's (daikan) seat collecting tax and
  judging cases for a region (~50,000–100,000 koku); also the seat of a castle-less daimyo. Space: nagaya-mon gate;
  genkan; ōhiroma hall; officials' rooms (yakusho); clerks' office; white-gravel court; rice storehouses; the
  intendant's residence behind (Dwellings, daikan-ke); kitchen; guard room; sometimes a small jail. Items: tax registers
  (kenchi-chō, nengu warituke-jō), village detail books (meisai-chō), rice-sampling spikes (sashi), standard measures
  (kyōmasu), scales and weights, survey poles (kenzao) and ropes, document chests, seal box, abacus, sword rack at the
  entrance, hibachi, zabuton, tobacco tray, notice board outside. [Takayama Jinya, shogunal from 1692; its rice store
  came from the castle in 1695 (verify)]
- **Domain government office (han-chō)**: in the castle's ninomaru or a separate yakusho: offices for elders (karō),
  finance (kanjō-kata), rural magistrates (kōri-bugyō). Items: as the jinya, more of them.
- **Rural magistrate's office (kōri-bugyōsho / gundai-sho)**: domain equivalent of a daikansho in outlying districts; a
  smaller jinya.
- **Village office (mura-kaisho / gōya)**: most villages had no separate building: the headman's house (Dwellings) is
  the office, its office room holding village registers (shūmon aratame-chō, gonin-gumi-chō), tax allocation papers,
  village seal, writing desk, abacus, document chest, and a kura with the village records. Some villages had a village
  office building or used the shrine haiden or a dō for meetings.
- **Ward meeting house (chō-ie / chō-kaisho)**: Kyoto and Osaka wards owned a small house for meetings and ward
  records; a caretaker lived in it. Items: ward rulebook, member registers, meeting room with zabuton, ward lantern,
  fire buckets. Edo's city-wide machi-kaisho (relief fund office) is `[outside 1680-1750: 1791]`.
- **Notice board (kōsatsuba / seisatsuba)**: posts shogunal and domain law boards (Christian ban; arson, poison and
  counterfeit bans; fugitive rewards; porter and horse fares at stations); the 1711 Shōtoku boards stay up 150 years.
  Space: roofed frame on a stone plinth behind a low fence at bridges, crossroads, post-town and village entrances.
  Items: 5–7 black-lettered wooden boards (kōsatsu), fence (saku), tile or board roof, stone base, temporary paper
  notices on a side board; at stations add the fare board (dachin-fuda). [WORLD_CATALOGUE T23]
- **Border / domain checkpoint (kuchi-dome bansho, sakai bansho)**: domain-level control posts at borders (not shogunal
  sekisho): gate, guard hut, bar. Items: capture tools, ledgers of passes, bar gate, lantern, bench. (C lists it again
  under coast and frontier; one entry here.)

### Highway control

- **Highway checkpoint (sekisho)**: shogunal barrier checking passes ("guns in, women out"); about 50 in Japan
  (assumed); on our map Hakone and Arai (Imagiri) on the Tōkaidō, Usui and Kiso-Fukushima on the Nakasendō. Space: two
  gates (Edo side and Kyoto side) ~18 m apart (Hakone) with the road between; upper guardhouse (ōbansho) for officials
  with raised tatami rooms facing the road; foot-soldiers' guardhouse (ashigaru-bansho); lookout (tōmi-bansho) on the
  slope; palisades (saku) from the mountain to the lake; stables; a small jail (rōya) at Hakone; a women's inspection
  room where female inspectors (hitomi-onna) checked women; kitchen; stores. Items: weapon display under the eave (rows
  of spears, matchlocks, bows and the three capture tools on racks), board where passes are presented, officials'
  desks, pass ledgers (tegata) and pass seals to compare, inkstones, bench outside, lanterns, gate bar and wicket,
  mounting block, drum or bell to close the gate. [Hakone Sekisho reconstruction 2007; Arai surviving building 1855]
- **Lake-shore sekisho with boat landing (Arai variant)**: travellers arrived by the Imagiri ferry; a landing stage
  inside the fence. Items: as sekisho.
- **Post-station office (toiya-ba)**: relays official porters, horses and cargo station to station; staffed by the
  toiya (head), toshiyori (elders), chōtsuke (clerks), umazashi and hitozashi (horse and porter dispatchers). Space:
  open-fronted office on the main street, raised board floor facing an earth yard; yard for horses and porters with tie
  posts; baggage stands; back office. Items: counters and desks, relay ledgers (tsugitate-chō), fare boards, large
  steelyard scales for cargo, stacked pack saddles (ni-gura), porters' carrying poles and frames, rope bundles,
  lanterns with the station name, tie rings, mounting block, baggage benches, timetable board, station seal.
  [WORLD_CATALOGUE T21, T20] (Porters' housing: Dwellings, porters' bunkroom.)
- **Cargo weight-check station (kanme-aratame-sho)**: at five stations (Shinagawa, Itabashi, Fuchū, Kusatsu, Oiwake;
  c.1712, verify) officials weighed official cargo against the limit. Items: very large beam scale on a frame, weights,
  register, benches.
- **Official courier relay point (tsugi-hikyaku)**: a room in the toiya-ba where official letter boxes were handed on.
  Items: lacquered letter box (fubako) on a pole, bells, register.
- **Post-town end marker (mitsuke)**: stone-faced earth bank, sometimes with a bansho (WORLD_CATALOGUE §1.1).
- **River-crossing office (kawa-kaisho) and porters' station**: at unbridged rivers (Ōi: Shimada and Kanaya, from
  1696): sets fares by depth, sells crossing tickets (kawa-fuda), dispatches river porters (kawa-goshi ninsoku) and
  litters. Space: office on the bank road with a raised floor; porters' waiting sheds (bango-ya), about 10 per bank
  (one per group); gauge post in the river. Items: ticket counter, ticket boards, depth-gauge post (marked knee, thigh,
  waist, chest), fare board by depth, carrying platforms (rendai) of several sizes stacked outside, ropes, ledgers,
  lanterns. (Porters' homes: Dwellings, river porters' row.)
- **Ferry control point (watashi-ba bansho)**: on ferried rivers (Rokugō from 1688 after its bridge washed away;
  Tenryū) and the Shichiri-no-watashi sea ferry (Miya–Kuwana); guard hut and fare office by the landing. Items: fare
  board, ledgers, bell, lantern post (Miya's jōyatō constant lantern, 1625).
- **River traffic inspection station (funa-bansho, kawa-bansho)**: Edo's Nakagawa funa-bansho (1661) checked boats
  entering Edo; guard building on the bank with a boat slip. Items: capture tools, ledgers, signal bell, chain or boom
  (assumed).
- **Port ship inspection (Uraga bugyōsho, from 1720)**: inspected every ship entering Edo Bay. Office with a waterfront
  inspection shed. Items: ledgers, cargo lists, measuring rods, flag or lantern signal post.

### Tax and stores

- **Village storehouse (gōkura)**: holds the village's tax rice before shipment and, in many villages, seed and relief
  reserves. Space: board or plastered kura on a raised stone base, sometimes on short posts with rat guards; broad door
  with a heavy lock; slatted floor; vents. Items: rice bales (tawara) on duckboards, masu and strickle, rice-sampler
  spike, scales, tally board on the wall, heavy lock and key, brooms. [WORLD_CATALOGUE 2.7]
- **Shogunal rice storehouses (o-kura, Asakusa o-kura)**: long row of kura along the Sumida with comb-tooth boat inlets
  (hori) so boats unload straight in; guard houses, a kura-bugyō office. Items: bales stacked to the roof, carrying
  hooks, masu, scales, ledgers, lamps with fire covers. (Asakusa: ~50 storehouses and 8 inlets, assumed; verify.)
- **Domain warehouse-residence (kura-yashiki)**: in Osaka (and Edo), each big domain's walled compound with a canal gate
  (funa-iri), kura, and an office for tax-rice sales. Items: rice bales, bills of sale, counting room, domain crest on
  lanterns and gate curtains. (Resident officer's family: Dwellings, kura-yashiki.)
- **Treasury storehouse (kinzō / okane-gura)**: plastered kura with iron-clad doors in castles and bugyōsho; Osaka's
  survives from 1751 (edge of window). Items: iron-banded money chests on the floor (dressing), coin strings, ingot
  boxes, guard's stool. (C lists it twice, in tax and in castle parts; one entry here.)

### Law and punishment (neutral)

- **Jail (rōya / rōya-shiki)**: holds suspects and prisoners awaiting judgement or punishment (prison terms were rare).
  Space (Edo Kodenmachō, ~2,600 tsubo; ~2,677 from 1775): walled compound with a moat-like ditch; offices and guard
  rooms; cell blocks by status: ōrō (large commoner cell), nikenrō (second commoner cell), agari-ya (lower samurai,
  priests, doctors), agari-zashiki (from 1683, bannermen and high clergy, tatami and better fittings), hyakushō-rō for
  peasants `[outside 1680-1750: 1775]`; interrogation room (sensaku-sho); torture store (gōmon-gura); execution yard
  inside the walls; women's cell. Items: double timber lattice cells (inner lattice + corridor + outer lattice), small
  food hatch, toilet tub in the cell, stacked tatami the cell boss sat on (ōrō), straw mats, wooden bowls, guards'
  lanterns and clappers, keys on a board, rope, capture tools, ledgers, brazier in the guard room.
- **Provincial jail / lock-up**: at a jinya, castle town or sekisho: small lattice-fronted board building with 2–4
  cells. Items: as jail, fewer.
- **Temporary house confinement (oshikome / azukari)**: suspects held in a headman's house or ward office; no
  building, a lattice room in a Dwellings house. (Note only; not counted.)
- **Execution grounds (keijō / shiokiba)**: Edo's Kozukappara (north, Nikkō / Ōshū road) and Suzugamori (south,
  Tōkaidō), both 1651, deliberately on highway approaches; Kyoto's Awataguchi; Osaka's Sennichi. Space: fenced open
  ground beside the road. Items (neutral): bamboo fence, stone post bases, covered exposure platform (sarashi-ba) or
  head-display stand (gokumon-dai), well, memorial Jizō (Kozukappara's great Jizō, 1741, in window) and a memorial
  temple nearby.
- **Public exposure platform in town (sarashi-ba)**: at Nihonbashi's south end by the notice board; roofed board
  platform with a low fence.
- **Sick-prisoner infirmary (tame)**: run by the hinin headmen at Asakusa (1687) and Shinagawa (c.1698; verify). (C
  gives no items beyond Layouts 2.15.)

### Fire and ward watch

- **Fire watchtower (hi-no-mi yagura)**: lookout and alarm. Shogunal fire-brigade towers from 1658, 3 jō (~9 m), plain
  wood; daimyo and town towers black and lower; in Kyōhō one per ~10 chō, otherwise a ladder on the ward office. Space:
  four-leg tapering timber tower with ladder, small roofed platform on top. Items: alarm bell (hanshō) and hammer, drum
  (shogunal towers used drums, town towers bells, assumed), railing, lantern, flag or wind vane (assumed).
  [WORLD_CATALOGUE T12, T13]
- **Fire ladder with bell (hanshō-dai / hi-no-mi hashigo)**: tall ladder on a ward-office roof or a post, with a small
  bell; the cheap everywhere version.
- **Shogunal fire brigade compound (jōbikeshi yashiki)**: from 1658; about 10 in 1730 (assumed). Walled yashiki with a
  tall tower, firemen's (gaen) quarters, equipment sheds. Items: tower with drum, matoi standards on racks, fire hooks
  (tobi-guchi), long ladders, water buckets, padded fire coats hung up, lanterns, commander's office.
- **Townsmen's fire brigade station (machi-bikeshi; the Iroha 47 groups, 1720)**: Ōoka's reform, perfect for 1730; a
  shed or room in a jishinban. Items: the group's matoi, ladders, fire hooks, big rakes, buckets, water barrels, banner
  with the group letter, padded jackets, bell. No hand pump: the ryūdosui pump is `[outside 1680-1750: 1754+ in Edo,
  mostly later]`. (Firemen's homes: Dwellings, ura-nagaya fireman variant.)
- **Ward gate (kido)**: posts, beam, two leaves plus a wicket; closed about 10 pm (WORLD_CATALOGUE §1.1).
- **Gatekeeper's hut (kido-ban / bantaya)**: 6 × 9 shaku with a 10-shaku eave, two old watchmen [WORLD_CATALOGUE T11].
  In Edo the gatekeepers sold cheap goods on the side (straw sandals, candles, sweets, paper, charcoal: "bantarō"
  shops). Items: lantern with the ward name, wooden clappers (hyōshigi) for night rounds, small counter of sundries,
  brazier and kettle, sleeping mat, fire hook, staff.
- **Townsmen's self-watch post (jishin-ban)**: run by ward house-owners in rotation, often opposite the kido; doubles
  as the ward office. Items: the three capture tools on a rack, fire ladder on the roof, fire buckets and hooks, ward
  ledger, lamp, brazier, residents' register, bench, notice board.
- **Samurai-district crossroads guard post (tsuji-ban)**: staffed by samurai households or hired men; several hundred
  in Edo (assumed). Items: capture tools, six-foot staff (rokushaku-bō), lantern, bench, brazier.

## == Military ==

Source: C §5. The 1615 one-castle-per-province rule cut 3,000+ castles to ~170 (some sources: ~400 destroyed in days);
new building needed shogunal permission and repairs a filing (Buke shohatto 1615/1635). So in 1730: ~170–190 castles
stand, almost all daimyo residences-and-offices, maintained, not new; many keeps are gone (Edo 1657, Osaka 1665) and a
castle without a keep is a normal sight (Nijō keeps its tenshu until 1750); abandoned pre-1615 sites survive
everywhere as earthworks; there are no barracks in the modern sense (retainers live in their yashiki, foot soldiers in
row houses: Dwellings; castle guard is rotating watches in gate bansho).

### Castle parts

- **Abandoned castle site (shiro-ato / haijō)**: earthworks and stone-wall ruins of a pre-1615 mountain or hill castle,
  overgrown, sometimes a small shrine on the old honmaru. Items: tumbled stone, a hokora, memorial stone (assumed).
- **Castle keep (tenshu)**: symbol and last redoubt; in peacetime mostly a store and lookout, rarely lived in. Space:
  stone base (tenshudai) with stone-lined basement store; 3–5 storeys of plain board floors, heavy posts, very steep
  stairs, outer walkway strip (musha-bashiri); top floor with view railing and sometimes a small shrine. Types:
  stand-alone, linked (renketsu), connected (fukugō), ring-linked (renritsu). Items: weapon racks (spears, guns, bows),
  armour chests (gusoku-bitsu), arrow boxes, stone-drop hatches (ishi-otoshi) at the floor edge, round / triangular /
  square gun and arrow loopholes (sama) with sliding covers, powder and bullet boxes, basement well at some castles,
  small top-floor shrine, water barrels, lanterns; gold-leaf roof fish (shachihoko) outside.
- **Keep base without a keep (tenshudai)**: Edo and Osaka in 1730: a bare stone platform. A strong landmark.
- **Corner turret (sumi-yagura)**: 2–3 storeys at enclosure corners; turrets were storehouses in peacetime. Items:
  weapon racks, stored goods (armour, bows, salt, rice, archives), loopholes, stone-drops.
- **Long wall turret (tamon-yagura)**: long single-storey turret along the rampart, storage and watch barracks. Items:
  stacked chests, racks, straw mats, lanterns.
- **Drum turret (taiko-yagura)**: houses the drum signalling times and musters. Items: great drum, stand, bell.
- **Named storage turrets**: salt (shio-yagura), gun (teppō-yagura), bow (yumi-yagura), armour (gusoku-yagura),
  moon-viewing (tsukimi-yagura, with open verandas). Items: match the name.
- **Well turret / well house (ido-yagura)**: roofed well inside an enclosure. Items: well curb, pulley, buckets.
- **Outer gate of a box gate (kōrai-mon)**: low-roofed gate with small roofs over the leaves. Items: iron-plated doors,
  bar, wicket.
- **Inner turret gate of a box gate (yagura-mon)**: gate under a turret; the masugata between the two gates is a square
  killing yard. Items: iron-plated leaves, upper room with loopholes and stone-drop slots, weapon racks.
- **Main gate (ōte-mon) and rear gate (karamete-mon)**: usually box gates; the ōte has a big guardhouse.
- **Buried gate (uzumi-mon)**: tunnel-like gate through a stone wall. Items: heavy door, bar.
- **Other gates**: yakui-mon, kabuki-mon, garden gate (niwa-mon), hidden gate (kakushi-mon), water gate (mizu-mon) for
  boats in moat-fronted castles. (Yakui-mon and kabuki-mon also front samurai houses and honjin.)
- **Barbican (umadashi)**: earth or stone outwork in front of a gate. No interior.
- **Earth-and-plaster wall (dobei) with loopholes**: tile-capped; loopholes every 1–2 ken; sometimes a stone-drop bay.
  (WORLD_CATALOGUE 2.4)
- **The lord's palace (goten / honmaru goten / ninomaru goten)**: residence and government seat when the daimyo is in
  his domain. Space: single-storey buildings joined by corridors: front (omote): genkan with tōzamurai waiting room,
  great audience hall (ōhiroma) with jōdan-no-ma, formal studies (shiro-shoin, kuro-shoin), elders' office rooms;
  middle (naka-oku): the lord's private rooms; inner (oku): wife and women's quarters; kitchen (daidokoro) wing; a Noh
  stage in the courtyard at bigger castles; gardens. Items: painted fusuma (gold ground in formal rooms, ink in private
  ones), coffered ceilings, tokonoma with staggered shelves and built-in desk, raised dais with armrest, sword stands,
  lacquered boxes, folding screens, hibachi, andon, tobacco sets, bells to summon attendants (assumed), Noh stage pine
  board. [Nijō Ninomaru goten (surviving); Nagoya honmaru goten (reconstructed)] (Private oku rooms: Dwellings,
  daimyo's castle palace cross-reference.)
- **Castle rice storehouses (kome-gura / hyōrō-gura)**: kura rows inside an enclosure. Items: bales, masu, scales.
- **Powder magazine (enshō-gura)**: stone or thick-plastered building set apart; Osaka Castle's stone magazine (1685)
  survives. Items: powder barrels and boxes on slatted shelves, copper scoops, no fire, bamboo and wooden tools only,
  lead ingot stacks nearby.
- **Armoury (bugu-gura / buki-gura / gusoku-gura)**: plastered kura or a turret. Items: armour on stands and in chests,
  helmets on stands, spears in long racks, naginata, matchlocks in racks, matchcord coils, bows and quivers, arrow
  bundles, bullet moulds, powder flasks, cartridge boxes (hayago), rolled campaign curtains (jinmaku), banners (nobori,
  sashimono), war drums, conch trumpets (horagai), war fans (gunbai), saddles and horse armour, pack-horse loads.
- **Gate guardhouse (bansho)**: board hut or long room at each important gate; Edo's hyakunin-bansho ("hundred-man
  guardhouse", surviving) at the Ōte-san-no-mon. Items: weapon display under the eave (spears, guns, bows in racks),
  capture tools, raised tatami guard room, register of passers, lanterns, brazier, bell, watch timetable board.
- **Castle stable (umaya)**: Hikone's (late 17th c., the only surviving castle stable) is a long L-shaped building with
  21 stalls. Items: stalls with boards and posts, mangers, straw, tack on pegs, saddles on stands, buckets, grooms'
  board-floored room.
- **Castle kitchen and workshops**: big earth-floored kitchen, carpenters' shed, repair smithy (assumed).
- **Castle shrine (shiro no jinja)**: small shrine to the castle's protector inside an enclosure (the keep's top-floor
  shrine or a hokora in a bailey).
- *Names only (not counted):* stone walls (ishigaki), wet and dry moats (mizu-bori, kara-bori), earth ramparts (dorui);
  bridges: earth causeway (dobashi), wooden, removable / drawbridge (hiki-bashi, hane-bashi), roofed corridor bridge
  (rōka-bashi); moat-side willow and pine rows, bamboo thickets on earthworks as defence.

### Training grounds

- **Swordsmanship hall (kenjutsu dōjō)**: domain halls in the castle town and private town schools (machi-dōjō) in
  Edo. Space: single board-floored hall with entrance and changing area; teacher's raised seat or shelf at the kamiza
  with a kamidana to the war deities (Katori, Kashima). Items: wooden practice swords (bokutō) and leather-covered
  bamboo swords (fukuro-shinai; true shinai with protective gear begin with Naganuma's school 1711–16), sword racks,
  student name-plate board (nafuda-kake), school-rules scroll, drum marking sessions, water bucket and ladle, towels on
  pegs. Protective armour (men, kote, dō) sets are early and rare in 1730 `[common from c.1750s]`.
- **Spear and naginata hall (sōjutsu-jō)**: as the dōjō; long rack of padded-tip training spears (tanpo-yari),
  naginata. (assumed separate at larger domains)
- **Grappling hall (jūjutsu-jō)**: tatami floor, kamidana, rules scroll.
- **Gunnery hall and range (hōjutsu-jō / teppō-ba)**: shed with a firing line and a target mound at 20–50 m. Items:
  matchlocks on racks, target boards, powder boxes, cleaning rods, matchcord, sand-filled target mound with a small
  roof. (assumed layout)
- **Archery range (yumi-ba / kyūdō-jō / shajō)**: roofed shooting hall (shajō) with board floor, open strip (yamichi)
  usually ~28 m, roofed earth target mound (azuchi), arrow-fetching path (yatori-michi). Items: bows upright on racks,
  arrow cases (yazutsu), gloves (yugake), targets (mato) on stakes in the mound, straw practice target (makiwara),
  score board, drum or flag for the target keeper.
- **Long-range through-shooting hall (tōshiya)**: Sanjūsangendō's 120-m veranda in Kyoto; Wasa Daihachirō's record
  8,133 hits in 1686 (in window); Edo's own Sanjūsangendō (Fukagawa, rebuilt 1701). Items: long veranda, counting
  boards, arrows by the thousand, judges' seat.
- **Horse-training ground (baba / uma-ba)**: long straight earth track with banks or rails (rachi) both sides, viewing
  stand (sajiki); Edo's Takadanobaba (1636). Items: railings, tie posts, mounting block, water trough, saddle rack,
  bench, pines along the track.
- **Mounted archery course (yabusame-ba) and dog-shooting ground (inuoumono-ba)**: yabusame revived by Yoshimune (1720s,
  in window) at shrines: three targets on posts along a track. Inuoumono is Kamakura / Muromachi, rare by 1730
  `[outside 1680-1750: mostly; revived only briefly]`.
- **Swimming / water-training (suijutsu) site**: domain river stretches with a changing shed. (assumed)
- **Falconry grounds and lodges (takaba, onari-goten)**: Yoshimune revived shogunal falconry in 1716; hunting grounds
  round Edo with guard posts (takaba-bansho) and rest lodges. Items: falcon perches, leather gloves, hoods, mews cages
  (taka-beya), feed boxes.

### Coast and frontier

- **Coastal lookout (tōmi-bansho)**: from 1638 (Nomo, Nagasaki) at ports and headlands to spot foreign ships; tiny hut
  ~1 ken × 1 jō, board walls and floor, two watchmen, often seasonal (spring–summer). Items: a spyglass or none (Dutch
  telescopes existed, rare), log book, lantern, signal fire pit or flag pole, bench, brazier. (Sekisho lookout on the
  slope is the same small hut.)
- **Beacon post (noroshi-ba / noroshi-dai)**: cleared hilltop with a stone or earth hearth, wood stacks, a hut; chains
  relayed news to Nagasaki (17th c.); many later chains are coastal defence `[outside 1680-1750: many 1800s]`. Items:
  firewood stacks, green pine for smoke, straw, hut, buckets.
- **Harbour guard stations at Nagasaki (bansho, from the 1640s–50s)**: run by Fukuoka and Saga domains. Items: few
  cannons on wooden carriages, gun racks, guard rooms. `[off-map: Nagasaki]` (region tag added by merge)
- **Coastal artillery batteries (daiba)**: `[outside 1680-1750: 1800s, Shinagawa 1853]`
- **Ship sheds for official vessels (o-funa-gura)**: long boat sheds with water gates; the shogunal warship Atakemaru was
  scrapped 1682, its shed and the official boats stayed at Fukagawa (verify); Hagi domain's ship shed survives. Items:
  hull on stocks or afloat, oars on racks, masts, sails in rolls, anchors, ropes.
- *Cross-references (not counted):* domain boundary guard huts = Government, border checkpoint; sekisho palisade and
  lookout = Government, sekisho.

## == Civic and infrastructure ==

Source: C §6.

### Schools and learning

- **Writing school (terakoya / tenarai-juku)**: reading, writing and abacus for commoner children, run by priests,
  rōnin, doctors or townsmen; common in cities by 1730, the rural boom is later (late 18th–19th c.). Space: a tatami
  room in a temple (temple school room, tenarai-dokoro, in the guest room or kuri), a house (Dwellings,
  writing-school teacher's house) or a rented shop; 10–50 children. Items: rows of small low desks (tsukue), inkstones
  and water droppers, brushes, practice books blackened with ink (tenarai-sōshi), copybooks (ōrai-mono), abacus rack,
  teacher's desk facing the room, hanging scroll of Tenjin (Sugawara Michizane) with an offering, switch or pointer,
  finished calligraphy on the walls, shoe racks. (C's temple school room merged here.)
- **Domain school (hankō)**: Confucian learning and martial arts for samurai sons. Few exist in 1730 (most of ~270
  founded after 1750); in window: Hagi Meirinkan (1719), Okayama's, Yonezawa's roots (1697), Sendai's Yōkendō (1736);
  Owari's from Kan'ei. Space: compound with a Confucian shrine hall (seibyō / taiseiden), lecture hall (kōdō), reading
  rooms, dormitories (ryō), library, martial-arts halls, archery range, horse ground. Items: lecture platform and
  lectern, low desks, book boxes and stacked Chinese classics, Confucius statue or tablet on an altar with sekiten
  ritual vessels (bronze food vessels, wine cups), calligraphy boards, drum marking classes.
- **Shogunal Confucian academy (Yushima Seidō, moved 1690)**: taiseiden on a stone platform, black-lacquered, with gates
  (Nyūtoku-mon, Kyō-mon) and a lecture hall. Items: as domain school, grander. Became the official Shōheikō `[outside
  1680-1750: 1797]`.
- **Local school for commoners (gōkō)**: Shizutani School (Okayama; founded 1670, lecture hall 1701, Bizen tile roof,
  lacquered floor) is the model. Items: lecture hall with lacquered board floor, desks, lecture platform, Confucius
  hall, library, stone wall.
- **Merchant academy (Kaitokudō, Osaka, 1724; semi-official 1726)**: townsmen's academy in a large machiya with a
  lecture room. Items: lecture desk, rows of desks, bookcases, notice of school rules.
- **Private academy (shijuku)**: a scholar's house with a lecture room: Itō Jinsai's Kogidō (Kyoto), Ogyū Sorai's school
  (Edo). Items: lecture desk, book stacks, students' desks, portrait of the master (assumed).
- **Library / book storehouse (bunko)**: domain and temple libraries in fireproof kura. Items: book boxes on shelves,
  labelled chests, ladders.

### Health and relief

- **Charity clinic (Koishikawa Yōjōsho, 1722)**: set up from a meyasubako petition; free care for the poor in the
  shogunal herb garden. Board-floored wards. Items: rows of bedding on straw mats, doctor's room with many-drawer
  medicine chest, boat-shaped grinder (yagen), mortar and pestle, decoction stove with pots, scales, paper packets,
  register.
- **Medicinal herb garden (o-yakuen)**: Koishikawa (1684), Komaba. Plots, drying shed, keeper's house. Items: drying
  racks and baskets, labelled beds.
- **Famine relief huts (sukui-goya / o-sukui-goya)**: temporary board shelters and gruel kitchens in famines (Kyōhō
  famine 1732, two years after the anchor). Items: huge cauldrons, ladles, bowls, straw mats, rice bales. Seasonal /
  event dressing. (The refugees' own lean-to: Dwellings, famine refugee shelter.)
- **Relief granary (gisō, shasō)**: community or domain famine reserves; Aizu's shasō from 1655 (in use in 1730); most
  others `[outside 1680-1750: Kansei era, 1790s]`. Space and items: as gōkura, plus a lending ledger.
- **Isolation / birth / menstrual huts (ubuya, taya)**: separate huts in some coastal and mountain villages where women
  stayed during birth and menstruation (neutral). Items: hearth, straw bedding, water jar.

### Water supply

- **Pulley well with roof (tsurube-ido)**: stone or wooden curb, pulley on a crossbeam, small roof, drain stone.
  Items: two buckets on a rope, washing tub, ladle, small water-kami stone or offering. (Same as Dwellings, roofed
  well: merged here.)
- **Lever well (hanetsurube)**: counterweighted pole on a post; rural. Items: bucket on a pole, stone weight.
- **Box well on the city aqueduct (jōsui-ido)**: Edo water came through wooden pipes (tōi) and bamboo pipes (kakehi)
  from the Kanda (1590s) and Tamagawa (1653) systems into square wooden well boxes; four of six systems (Aoyama, Mita,
  Senkawa, Kameari) shut in 1722, so in 1730 only Kanda and Tamagawa run. Items: square wooden curb, pulley, buckets,
  wooden cover. (The alley shared well in Dwellings is this in Edo.)
- **Aqueduct water gate and inspection station (mizu-ban-ya)**: at Yotsuya Ōkido the Tamagawa aqueduct entered the city
  through a guarded inspection station. Items: sluice boards, gauge, guards' capture tools, lantern.
- **Aqueduct bridge (kakehi / suidō-bashi)**: wooden trough carried over a river on a bridge (Suidōbashi over the
  Kanda). Special structure, no interior.
- **Water-sellers' landing (mizu-ya)**: Edo boat water sellers filled tubs at pipe ends. (assumed detail) (The seller
  himself: Food and drink, water seller.)
- **Public spring / wash place (arai-ba, kawabata)**: stone steps into a stream or a stone-lined pool where villagers
  washed. Items: washing stone, tubs, ladle, small Suijin stone. (Ōmi's in-house version: Dwellings, kabata.)

### Roads, bridges, ferries

- **Mile mound (ichirizuka)**: paired mounds every ri (~3.9 km), ~9 m square, ~3 m high, with enoki (55 %), pine or
  cedar [WORLD_CATALOGUE §1.6, T22]. Items: the tree, a stone marker (some), bench stone.
- **Signpost stone (michi-shirube / oiwake-ishi)**: at forks, carved directions ("right to Edo, left to ...").
- **Stone-paved pass road (ishidatami)**: Hakone 1680 (WORLD_CATALOGUE §1.6).
- **Plank bridge (ita-bashi)**: simple beams and boards on posts.
- **Earth-covered bridge (dobashi)**: logs covered with earth and turf. (Also the castle causeway.)
- **Log bridge (maruki-bashi)**: rural; one or two logs.
- **Large wooden trestle bridge (Nihonbashi type)**: Edo's great bridges built in window: Ryōgoku (1661), Shin-Ōhashi
  (1693), Eitai (1698); the Tōkaidō's Yahagi bridge (Okazaki, longest on the road, ~370 m). Bronze finials (giboshi) on
  railings only on the most important (Nihonbashi, Kyoto's Sanjō and Gojō). Items: giboshi, railings, bridge-name post,
  lanterns (assumed), notice board at the end.
- **Arched wooden bridge (sori-hashi / taiko-bashi)**: shrines, gardens; Kintaikyō (Iwakuni, rebuilt 1674, five arches)
  as a landmark. (Shrine version: Shinto, sacred bridge.)
- **Stone arch bridge (ishi-bashi / megane-bashi)**: Nagasaki's Megane-bashi (1634); mostly Kyushu, rare elsewhere.
  `[off-map: Kyushu]` (region tag added by merge)
- **Cantilever bridge (hane-bashi)**: Saruhashi (Kōshū road): stacked cantilevered beams over a gorge.
- **Vine bridge (kazura-bashi)**: Iya valley (Shikoku); remote mountain crossing. `[off-map: Shikoku]` (region tag added
  by merge)
- **Boat bridge (funa-bashi)**: boats chained side by side, planks on top (Toyama's Jinzū river, 60+ boats); where fixed
  bridges were forbidden or impractical.
- **Bridge-keeper's hut (hashi-ban-goya)**: at big and toll bridges (Eitai became a townsmen-run toll bridge in 1719, in
  window). Items: toll box, lantern, broom and rake, staff, register, bench, fire buckets.
- **Ferry landing (watashi-ba / tosen-ba)**: stone or earth ramp, mooring posts, waiting shed, ferry hut. Items: fare
  board, flat-bottom ferry boats, poles, ropes, bell or drum to call the boat, benches, lantern. (Controlled crossings:
  Government, ferry control point.)
- **Ferry-keeper's hut (watashi-mori goya)**: small board hut. Items: poles, brazier, straw raincoats, sleeping mat.
- **Rope-guided ferry (hiki-bune)**: rope strung across the river for the ferry (assumed on narrow rivers).
- **Relay stables for official horses (tenma)**: no single big station stable: post-town houses kept horses at the rear
  (WORLD_CATALOGUE §1.4; Dwellings, packhorse owner's house); the toiya-ba yard has tie posts; support villages
  (sukegō) sent extra horses and men. Items: stalls, mangers, pack saddles, straw horse sandals (uma-waraji), bells,
  rope.
- **Roadside horse trough and tie posts**: stone or wooden trough, iron rings.
- *Names only (not counted):* road avenue (namiki; Nikkō cedar avenue 1625–51); rest stones and benches at passes
  (koshikake-ishi).

### Harbours and shipping

- **River quay with steps (gangi / kashi)**: stone steps into a canal or river, mooring posts; a kashi is a quay named
  for its trade (fish quay, rice quay). Items: mooring stones and posts, bales, barrels, handcarts, planks.
- **Warehouse row on a canal (kura-nami)**: plastered kura side by side, doors to the water. (Merchant ones: Services,
  warehouse for rent; official ones: Government, tax and stores.)
- **Lighthouse lantern (tōmyōdō / jōyatō)**: stone or wooden lantern tower on a quay or headland, oil-lit; Miya's jōyatō
  (1625). Items: oil lamp, oil jar, ladder, keeper's hut.
- **Weather-watching hill (hiyori-yama)**: hill above a port with a stone direction marker (hōi-ishi) carved with
  compass points. Items: the stone, shelter bench, small shrine.
- **Harbour breakwater and boat-hauling slip**: stone jetty (hatoba), capstan (manrikisha) for hauling boats (assumed).
- **Shipwright's slip**: B's boat builder / shipyard (Crafts); a waterfront site. (Cross-reference, not counted.)
- **Fish-spotting tower (uomi-yagura)** {from C §1.4}: tower on the headland for net fisheries (assumed common for
  sardine and tuna nets). (C named it only in the layout; listed here so it has an entry. No items given.)

### Agriculture and water control

- **Water gate / sluice (hi, hi-guchi, suimon)**: wooden sluice boards in a stone or timber frame at a channel head.
  Items: sluice boards, windlass or lever, gauge stake, sandbags.
- **Water guard hut (mizu-ban goya)**: in droughts villages guarded sluices day and night (water disputes were fierce;
  Kelly). Items: straw mat, lantern, staff, brazier, record board.
- **Weir (seki / iseki)**: stone-and-timber weir across a river diverting water into a channel. Structure only. (The
  fishing weir is Rural industry, yana.)
- **Reservoir pond (tame-ike)**: Kinai and Sanuki; earth dam with a sluice tower (assumed) and small Suijin shrine.
- **Treadwheel for irrigation (fumi-guruma)**: from the 1660s (Osaka), so in; small wooden paddle wheel trodden by a
  person. (WORLD_CATALOGUE 2.7)
- **Field hut (nora-goya)**: tool and rest hut at distant fields. Items: hoes, straw raincoat, pot, mat. (A's identical
  entry, items hoe, bucket, straw mat, water jar, merged here.)
- *Names only (not counted):* river embankments (tsutsumi) and flood works: bamboo-planted levees, stone groynes
  (seigyū), stone-filled bamboo gabions (jakago); dragon-spine chain pump (ryūkotsusha), older, wooden.

### Community buildings

- **Village assembly place (yoriai-dokoro) / village hall (mura-kaisho / gōdō)**: usually not a separate building (the
  headman's house, shrine haiden or a village dō); some villages had a hall. Items: rows of straw mats, hearth or
  brazier, village rules board (mura-okite), record chest, tea kettle. (Overlaps Government, village office: see
  Seams.)
- **Young men's lodge (wakamono-yado / wakashu-yado)**: unmarried young men slept here and organised festival and fire
  duties; strongest in fishing and coastal villages. Plain house or room. Items: sleeping mats, straw bedding, hearth,
  festival drums and lion head (assumed), rules board, sake barrel.
- **Young women's lodge (musume-yado)**: less common, same idea. (assumed)
- **Time-bell tower (toki no kane)**: Edo had about nine official time bells (Hon-ishichō from the 1620s, Asakusa, Ueno,
  Shiba and others; verify count); castle towns rang a bell or drum. A bell tower plus the keeper's hut. Items: bonshō,
  striker log, incense clock (kō-dokei) or water clock, time-table board, lantern. Bell-keepers collected a fee from
  each household in range.
- **Firebreak plaza and embankment (hirokōji, hiyoke-chi, hiyoke-dote)**: open spaces kept clear after 1657, in practice
  filled with temporary stalls, shows and tea stands (Shops, market stalls; Services, show booth). A site.
- **Public toilet at street corners (tsuji-setchin / kōshū benjo)**: in Kyoto and Osaka, night-soil dealers set up
  roadside toilets to collect fertiliser. Items: half-wall booth, buried pot, lid.
- **Rubbish collection point (gomi-tame) and landfill (Eitai-jima, 1655 rule)**: a wooden rubbish box in each Edo alley;
  collected by boat to reclaimed land. Items: board bin, broom, baskets. (Part of Dwellings, shared alley facilities.)

### Death

- **Graveyard outside a temple (bochi / hakaba)**: village communal graves, family graves at field edges; Kinki
  two-grave system (ryōbosei): burial grave (ume-baka) in a field away from the village and visiting grave
  (mairi-baka) with the stone at the temple. Items: grave stones (WORLD_CATALOGUE §1.6), wooden grave posts (bohyō)
  for fresh graves, sotoba slats, bamboo flower tubes, water cups, small roofed frame over a fresh grave (assumed),
  bamboo fences round fresh graves against animals, buckets and ladles at a water point. (Temple graveyard: Buddhist.)
- **Cremation ground / crematory hut (sanmai-ba, hiya, kasō-ba)**: outside the village or town; several in Edo (Senju,
  Kirigaya and others, assumed list); run by cremation attendants (onbō; their home: Dwellings, cremation-ground
  attendant's hut). Roofed shed over a stone or clay pit, or an open pit. Cremation common in Jōdo Shinshū regions and
  cities; burial the norm in most rural areas. Items (neutral): stone-lined pit, firewood stacks, straw bundles, iron
  poles and tongs, ash urns, water buckets, small Jizō, attendant's hut.
- **Coffin-bier shed and funeral goods store**: at a temple or village: bier (kan-dai / gan), palanquin-shaped coffin
  carrier (kan-goshi), white banners, lanterns, funeral canopy (tengai). (assumed)

---

# 4. Seams and duplicates

Where the three lanes touch. "Kept both" means both entries stay in §3 because they describe different halves or
different buildings; "merged" means one entry is counted and the other is marked `not counted` in §3 with a pointer.

## 4.1 Seams (how each was handled)

1. **Shop-houses split between A (home side) and B (shop side).** Kept both halves; cross-linked. The machiya is one
   building: A's Kyoto / Osaka / Edo / castle-town machiya and street-front row unit (omote-nagaya) are the living
   rooms behind every B `town shop` (61 entries carry a town-shop or shop-plus-kura setting). Same split for: great
   merchant's residence ↔ silk draper, wholesaler, moneychanger; apprentices' loft ↔ draper's shop-boys; landlord
   house ↔ rent ledgers; Kiso / Tōkaidō post-town house ↔ hatago and tea-house fronts; gōnō compound ↔ sake and soy
   brewery; town doctor's house ↔ doctor's practice; arts teacher's house ↔ shamisen maker / teacher variant.
   *For the model plan:* one machiya shell with a front (B) and back (A) dressing covers both lanes.
2. **Back-alley tenants ↔ B's itinerant trades.** B lists 26 `itinerant` / `stall` trades (peddlers, repairers,
   masseurs, fortune-tellers, candy sellers, lending library, recycling buyers). They have no premises: they live in
   A's ura-nagaya occupant variants (peddler, carpenter, plasterer, boatman, fortune-teller, porter, fireman,
   paper-waste collector). Kept both; B's are prop kits, A's are the room they sit in.
3. **Samurai homes (A) vs offices (C).** Kept both, cross-linked: dōshin house ↔ town magistrate's office; daikan-ke ↔
   jinya / daikansho; kura-yashiki family rooms (A pointer, not counted) ↔ C kura-yashiki; honmaru goten (A pointer,
   not counted) ↔ C lord's palace; ashigaru row and edo-zume nagaya ↔ C's note that there are no barracks (tamon-yagura
   serve as watch barracks). **Gap:** A assigns a daimyo Edo mansion's formal *omote* halls to C, but C has no Edo
   mansion entry; the nearest is C's lord's palace (castle), whose omote rooms would serve.
4. **Headman's house = village office.** A has the house; C says most villages had no separate office and lists the
   office function, the village hall (rare), the gōkura and the kōsatsuba in front of the headman's gate. Kept both;
   C's "village office" entry is the office-room dressing on A's headman shell. A's rice storehouse (kome-gura) at the
   headman's house and C's village storehouse (gōkura) are the same kura type with different ownership.
5. **Honjin and inns (B vs C).** B owns all commercial lodging and cross-refers the honjin to C; C describes the honjin
   and waki-honjin in highway control; A has the honjin family's private rooms. Merged: honjin and waki-honjin now sit
   under Lodging (from C), family rooms stay in Dwellings. C's toiya-ba ↔ A's porters' bunkroom; C's kawa-kaisho
   porters' waiting sheds (bango-ya) ↔ A's river porters' row (kept both: shed at the bank vs where they lived).
6. **Stables (all three lanes).** A: inside stable, detached stable, ox shed, packhorse owner's house, horse-dealer's
   house, support-village farmer. B: commercial stable and horse dealer, packhorse carrier, horse-dealers' inn,
   ox-cart haulage. C: castle stable (Hikone, 21 stalls), relay stables for official horses (tenma), roadside trough
   and tie posts. Kept all; they share one item set (manger, fodder cutter, straw horseshoes, pack saddle, harness,
   tie rails, water trough). Collapse group in §6.
7. **Bathhouses and toilets.** Baths: A bath hut (goemon / teppō / steam, verify), B public bathhouse, steam bath,
   hot-spring inn, communal spring bath, the hatago's bath room, C Zen temple bathhouse (steam). Toilets: A outhouse
   and shared alley toilet, C Zen latrine, street-corner public toilet. Kept all; see contradictions for the tub types.
8. **Granaries vs storehouses (the kura family).** A: dozō, itagura, azekura, kome-gura, nurigome, mizuya. B: rented
   kura, the kura behind every big shop, pawnshop kura, wholesalers' kura rows. C: gōkura, relief granary, Asakusa
   o-kura, kura-yashiki, treasury, shrine treasure store (log azekura in old shrines), mikoshi store, festival float
   store, temple storehouse, sutra repository, library (bunko), armoury, powder magazine, castle rice store, turrets
   used as stores. Kept all; one shell family (see §6). A's "azekura rare in homes, probably drop" and C's "azekura
   for old shrine treasure stores" agree: keep the log kura only for shrines.
9. **Shrine-temple mixing.** C's 1730 rule: shrines carry Buddhist buildings (bettō-ji, pagoda, honji-dō / goma hall)
   and temples carry a tutelary shrine. Pagoda counted once (Buddhist); honji-dō kept as a shrine entry. A's religious
   households (shake, farmer-priest, oshi, village yamabushi) are the homes of C's shrine and Shugendō staff; B's
   temple-street trades (busshi, rosary, incense, candle, clay dolls, toothbrushes) line C's temple-town approach.
10. **Hermitages and ascetics.** A's grass hermitage and C's hermitage (an) are the same building: counted once (A).
    A's hōjō-an, yamabushi hut and carver-monk hut ↔ C's Shugendō modifier, waterfall practice site, mountain pilgrim
    hut. Kept all.
11. **Pilgrim lodging.** A's oshi house (home side), C's shukubō, B's kō-yado and zenkon-yado, C's pilgrim overnight
    hall (Buddhist) and pilgrims' overnight hall (Shinto). B's zenkon-yado is marked not counted (B calls it a
    farmhouse or temple room); C's two halls kept. See contradiction 11 on what "zenkon-yado" is.
12. **Work huts and their sites (A hut ↔ B site).** Charcoal kiln hut (A counted, B's duplicate not counted) ↔ black
    and white charcoal kilns; logging-crew camp hut ↔ logging camp; raftsman's hut ↔ rafting station; mountain
    hunter's hut (A counted, B's duplicate not counted); wood-turner's forest hut ↔ woodturner; net shed (A counted,
    B's duplicate not counted); salt-field labourer's hut and small salt-maker's house ↔ salt fields and boiling hut;
    nori cottage ↔ nori farm; net-boss house ↔ dried-sardine works; tea-grower's farmhouse ↔ tea processing shed;
    sericulture farmhouse ↔ silkworm house and silk reeler; cotton farmhouse and Kinai tenant house ↔ ginner, bower,
    spinner, weaver; gasshō attic paper-making and saltpetre pit ↔ paper mill and powder magazine; kawata house ↔
    leather trades.
13. **Field and watch huts.** A's field hut merged into C's field hut (identical); A's paddy watch hut and C's water
    guard hut kept (different jobs, same shell).
14. **Relief.** A's famine refugee shelter (the lean-to) ↔ C's famine relief huts (the official gruel kitchen); A's
    fire-ruin shack. Kept all.
15. **Death and marginal status.** A's cremation-ground attendant's hut ↔ C's cremation ground; A's kawata house,
    kawata leader's compound, hinin hut ↔ B's leather section ↔ C's outcast settlement layout, execution grounds,
    sick-prisoner infirmary. All listed neutrally, as the agents did.
16. **Wells and water.** A's roofed well merged into C's pulley and lever wells; A's alley shared well = C's aqueduct
    box well (Edo); A's kabata room ↔ C's public wash place; B's water seller ↔ C's water-sellers' landing.
17. **The back-alley court.** A's shared alley facilities (well, toilet, rubbish pit, Inari, drying poles) ↔ C's alley
    Inari, rubbish collection point, box well, ward gate and gatekeeper's hut. Kept all; they are one site kit.
18. **Schools.** A's writing-school teacher's house (home) ↔ C's terakoya; C's temple school room merged into C's
    terakoya entry.
19. **Medicine.** A's town doctor's house ↔ B's doctor's practice, medicine shop, moxa shop ↔ C's charity clinic and
    herb garden. Naming differs only: A calls the drawer cabinet *kusuri-dansu*, B *hyakumi-dansu*.
20. **Fire.** A's fireman nagaya variant ↔ C's townsmen's fire brigade station; C's fire towers and ladders; fire
    buckets appear in A, B's shop kit and C.
21. **Stages and theatres.** B's kabuki and puppet theatres (B: "may belong to civic") ↔ C's Noh and kagura stages; B's
    theatre and sumō tea houses. Kept in Services.
22. **Bells, statues, coins.** B's on-site bell caster ↔ C's bell tower and time-bell tower; B's Buddhist sculptor ↔ C's
    statues; C's mint (C: "the industry could be B's") kept in Government.
23. **Boats.** A's boat shed ↔ B's boat builder's shed and shipyard ↔ C's shipwright's slip (pointer, not counted),
    official ship sheds, harbour slip.
24. **Markets and plazas.** B's market stalls, show booths, yatai ↔ C's firebreak plazas (filled with stalls).
25. **Gatehouses and gambling.** A's nagaya-mon and lower servants' rooms (reputed gambling dens) ↔ B's gambling den ↔
    C's gate types (yakui-mon, kabuki-mon) and bugyōsho nagaya-mon gate.
26. **Tea rooms.** A's tea hut and C's temple tea room are one shell (both kept, one context each); B's tea houses are
    commercial and a different building.
27. **Entries C named only in a layout.** Fish-spotting tower (uomi-yagura) given its own Civic entry. The young men's
    lodge already had one.
28. **Pointers between lanes that land nowhere (gaps).** B's midwife → "BL-A" (A has no midwife); B's thatch meadow →
    "BL-A/BL-C village commons" (neither has a commons entry); A's daimyo mansion omote → C (see seam 3). Listed so
    Stephen can decide whether they need entries.

## 4.2 Contradictions between the agents

1. **Iron kettle (tetsubin).** A: tetsubin is in the Kitamura 1687 three-room farmhouse set and the Kiso houses;
   date trap says "spreading, fine for tier 2–3". B (pot caster): "the everyday side-spouted iron kettle (tetsubin)
   comes later [mid-18th c. on, uncertain]".
2. **Zabuton for commoners.** A: "zabuton for commoners is uncertain" (four-room farmhouse: "zabuton for guests (rare,
   verify)"). B: cushions (zabuton) are part of the standard shop-front kit in every town shop. C: zabuton rows in
   temple main halls and in the jinya.
3. **Bath-tub types.** A: goemon-buro (Kamigata) vs teppō-buro (Edo) comes from *Morisada Mankō*, a late Edo source,
   "verify for 1730". B: states for every hatago "a wooden tub: goemon-buro in the west, teppō-buro in the east" as fact.
4. **Zaguri silk reeler.** A lists a hand-reel (zaguri) in the sericulture farmhouse. B: the seated geared zaguri
   "spread late Edo, especially after 1859"; hand reeling (te-biki) is the 1730 method. (A's entry is itself tagged
   outside the window, so the impact is small.)
5. **Silk-loft farmhouse date.** A: big rearing-loft houses are "late 18th–19th c.". B: tall multi-storey sericulture
   farmhouses are "19th c.".
6. **"Kara-usu" names two machines.** A (barn, pounding shed) and B (rice polisher): kara-usu = foot-treadle mortar. B
   (potter's works): "a water-powered clay stamp (kara-usu)".
7. **Who stayed at the waki-honjin.** B: "when no daimyo was staying, the waki-honjin often took ordinary paying
   guests like a hatago". C: the honjin never took ordinary travellers; the waki-honjin took "ordinary travellers of
   standing" in between times.
8. **Glass.** A's date trap: "no glass". B: a glassmaker trade exists in 1730, rare: beads, hairpins, cups, spectacle
   lenses, Nagasaki first then Osaka and Edo (verify for Edo). Likely A means window or household glass; flag.
9. **Teapots.** A's date trap: "no side-handled teapot (verify)". B: Baisaō's 1735 sencha stall has "a teapot for leaf
   tea". Not necessarily side-handled, but the props could clash.
10. **Who licensed village guns.** A: Tsunayoshi's 1687 registration made village guns licensed pest "scare-guns"
    (shogunal). B: guns "required a domain licence (teppō-aratame)". Possibly both true (shogunal policy, domain
    administration); flag.
11. **What a zenkon-yado is.** B: "farmers or temples lodging pilgrims for free as merit": a farmhouse room. C: "pilgrim
    overnight hall (tsuya-dō / henro-goya / zenkon-yado)": a free-standing roofed platform or hut on the route.
12. **Nori start date (certainty only).** A: Shinagawa nori c. Genroku–Kyōhō, "verify start date". B: states the same
    span as in era, no flag.
13. **Hunter's weapons (emphasis only).** A: matchlock (licensed), spear, snares. B: spears, snares and deadfall traps
    "were common"; guns needed a licence. Not a contradiction, but B's dressing has no gun.
14. **Internal slips in C.** §1.13 points to "§4.14" for the river-crossing office (it is §4.3 #24); the treasury is
    listed twice (§4.4 #31 and §5.1 #22) and the domain border guard hut twice (§4.2 #15 and §5.3 #43). Each counted
    once here.

No agent contradicted another on the big anchor facts: Dōjima licensed 1730, taru-kaisen split 1730, Iroha fire
brigades 1720, Kyōhō famine 1732, Edo and Osaka keeps absent, the 1843 Taigaichō hatago counts (B ~3,000, C 2,988).

---

# 5. Shared core kit

**How the counts were made.** A helper script counted how many of the 682 counted entries in §3 name each item
(keyword match on the entry text, so synonyms are grouped and a mention in a "Space" note also counts). Numbers are
rough, and they are a **floor**: many entries inherit a kit without naming it. The biggest inheritances are:

- the **standard shop-front kit** (noren, kanban, lattice, counter screen, account desk, abacus, ledgers, inkstone,
  tobacco tray, cushions, hibachi, scales, fire buckets, back kura): about **61** entries are town shops or shops with
  a kura, and every one takes it;
- the **farm set / home set / headman set** that A's entries say "plus": about **16** entries;
- "as hatago", "as soba", "as kake-jaya", "as noborigama" and similar: a few more.

"Agents" = which input files named the item in their own recurring-items list (A §"Items that show up almost
everywhere", B §12, C §"Items that recur").

## 5.1 Hearth, kitchen and water

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Wooden tubs (oke, tarai; washing, soaking, salt, pickle) | 64 | crafts, food, homes | A, B, C |
| Pot (nabe) | 63 | homes, crafts, food | A |
| Trays (zen, hakozen, lacquer; sanbō on the sacred side) | 58 | food, homes, temples | A, C |
| Bowls and dishes | 44 | homes, food, crafts | A |
| Wooden buckets (incl. well bucket) | 38 | homes, civic, government | A, B, C |
| Kamado / kudo / hettsui (fixed clay stove) | 24 | homes (18), inns, temple kuri, shrine kitchen | A, B, C |
| Mortar and pestle, pounder (usu, kine, suribachi, treadle mortar) | 22 | food, services, homes | A, B |
| Steamer (seiro, koshiki) on a cauldron | 21 | food, crafts, rural | B |
| Cauldron (big iron pot on a hearth) | 20 | food, rural works, temple kuri | B |
| Kettle (tetsubin, chagama) | 20 | homes, food | A (see contradiction 1) |
| Irori (sunken hearth) with jizai-kagi hook | 19 | homes only | A |
| Ladle / dipper (hishaku) | 16 | civic, crafts, temples | A, B |
| Water jar (mizugame) | 15 | homes, temples | A, B, C |
| Well | 14 | homes, castles, civic | B |
| Cutting board (manaita) | 12 | food, rural works | — |
| Stone hand mill / quern (ishi-usu, hikiusu) | 10 | food, homes | B |
| Sink board (nagashi) | 5 (plus every home with a kitchen doma) | homes | A |

## 5.2 Heat, fuel and light

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Andon / hanging lantern / chōchin (paper or bronze, often with a crest or name) | 74 | homes, government, shrines, civic | A, C |
| Brazier (hibachi) or portable charcoal stove | 33 (plus ~61 shops) | homes, government, military | A, B, C |
| Charcoal and charcoal bales | 25 | food, crafts, rural | B |
| Firewood stacks | 18 | homes, crafts | A |
| Candles and candle stands | 7 | temples, rich homes (A: candles are expensive) | — |
| Torch / fire basket | 3 | watch huts, cormorant boats | — |

## 5.3 Storage and packing

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Wooden boxes (lidded, stacked, document, letter, sutra, meal) | 93 | everywhere | B |
| Racks (tool wall, product rack, weapon rack, drying rack) | 80 | crafts, homes, military | B, C |
| Poles (drying, carrying, bamboo stock) | 42 | crafts, food | B |
| Jars (miso, oil, salt, powder, ash) | 40 | homes, food, crafts | B |
| Chests (nagamochi, tansu, armour chest, money chest) | 36 | homes, government | A |
| Baskets (zaru, kago, biku) | 34 | homes, rural, food | A, B |
| Straw bales (tawara) | 30 | homes, government, services | A, B, C |
| Casks and barrels (taru) | 22 | food, crafts | B, C |
| Straw bags and sacks (kamasu) | 20 | homes, crafts, rural | B |
| Fireproof kura behind the building | (every big shop, headman, temple, office) | all lanes | A, B |

## 5.4 Floor, bedding and seating

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Straw or rush mats (mushiro, goza, komo) | 49 | homes, civic, crafts | A, B, C |
| Futon / quilt / rental bedding (yogi) | 44 | homes (31), inns | A |
| Clothes rack (ikō) or robe on a rack | 38 | homes, military, crafts | A |
| Benches (shōgi, battari-shōgi) | 25 (plus ~61 shops) | government, civic, tea houses | C |
| Folding screen (byōbu) / entrance screen (tsuitate) | 21 | homes | A |
| Straw bedding (rural poor) | 17 | homes | A |
| Cushions (zabuton, round straw enza, zafu) | 16 (plus ~61 shops) | temples, services | C (see contradiction 2) |
| Tatami | (every town home, inn, office, temple gejin; none in poor rural homes) | — | A |

## 5.5 Religious

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Butsudan / Buddhist shelf / altar or altar dais | 34 | homes (19), temples | A, C |
| Bell (hand bell, alarm hanshō, temple bonshō) | 31 | temples, government, shrines | C |
| Drum (hand, festival, temple, tower, war) | 28 | spread over 8 sections | C |
| Statue or image in a zushi | 25 | temples | C |
| Hanging scroll and tokonoma | 22 | upper homes, temples, palace | A (tier marker) |
| Kamidana (god shelf; Ebisu / Kōjin shelf) | 15 (B: "almost every workshop and shop") | homes, workshops | A, B |
| Offering stand / offering box / offering dish (sanbō, saisen-bako) | 14 | shrines | C |
| Paper charm (ofuda) on a post | 12 | homes | A, C |
| Incense and incense burner (mitsugusoku set) | 11 | temples, homes | C |
| Gohei / shimenawa / sakaki vase | 9 | shrines, forges | C |
| Votive plaques (ema) | 8 | shrines, temples | C |
| Memorial tablets (ihai) on stepped shelves | 5 | temples, widow's hut | C |

## 5.6 Office, trade and watch

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Ledgers, registers, account books (daifukuchō) | 57 (plus ~61 shops) | government (19), homes, services | B, C |
| Scales: steelyard, balance and weights (fundō) | 33 (plus ~61 shops) | government, shops, food | B, C |
| Low writing desk (and sutra desk) | 30 | homes, government, civic | C |
| Inkstone, brushes, writing box | 29 | crafts, homes | C |
| Sword rack / weapon rack / spears / matchlocks | 28 | homes (11), military (9) | A, C (one kit, three fills) |
| Bows and arrows | 24 | homes, military, crafts | — |
| Notice board / fare board / signboard (kanban) | 23 (plus ~61 shops) | government, civic | B, C |
| Fire buckets, fire hooks, ladders | 20 (plus ~61 shops) | government, civic | B, C |
| Tobacco tray / pipes (tabako-bon, kiseru) | 18 (plus ~61 shops) | homes, services | A, B, C |
| Armour / armour chest | 17 | homes, military | A (tier marker) |
| Masu measures and strickle | 14 | food, government | B, C |
| Seal / seal box | 12 | government | C |
| Capture tools on a rack (sodegarami, sasumata, tsukubō) | 11 | government | C |
| Abacus (soroban) | 10 (plus ~61 shops) | services, government | B, C |
| Document box (bunko) | 6 | government | C |
| Lattice cell front (wall module) | jails, holding rooms, sekisho jail, pilgrim-hall fronts | — | C |

## 5.7 Road, farm, sea and stable

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Rope coils | 41 | homes, crafts, government | C |
| Boats, oars and poles | 26 | civic, homes | — |
| Straw sandals (waraji, zōri) and straw horse shoes | 24 | homes (13) | A, C |
| Nets, floats, sinkers | 21 | homes (fishing), rural | — |
| Manger, fodder cutter, stall, tie post, trough | 20 | homes, food, stables | C |
| Carrying pole / shoulder pole / yoke | 19 | homes, food, services | — |
| Mino (straw raincoat) | 18 | homes | A |
| Pack saddle, saddle, harness, halter | 12 | homes, military | C |
| Kasa and other hats | 12 | homes | A |
| Hoe, sickle, mattock | 8 (plus the farm set) | homes | A (rural core) |

## 5.8 Tools and workshop mechanisms

| Item | ~Entries | Clusters in | Agents |
|---|---|---|---|
| Knives | 33 | crafts, food | B |
| Sewing box, needles, thread | 28 | crafts, homes | — |
| Planes, chisels, adze | 24 | crafts | B |
| Hammers, mallets, sledges | 24 | crafts | B |
| Forge, box bellows (fuigo), anvil | 22 | crafts (every metal trade) | B |
| Files, awls, shears | 22 | crafts | B |
| Saws | 16 | crafts, homes | B |
| Press: stone-weighted lever press or wedge press (shime-gi) | 15 | food, crafts, rural | B ("one mechanism, several trades") |
| Loom, spinning wheel | 13 | homes, crafts | A |
| Axe, hatchet, billhook | 11 | homes, crafts | B |
| Whetstones, grindstones | 10 | crafts | B |
| Paper (sheets, packets, rolls) | 51 | crafts, homes, services | — |

## 5.9 Domestic extras and tier markers

| Item | ~Entries | Notes |
|---|---|---|
| Sake flasks, casks, sake sets | 25 | homes, food, shrines (heishi) |
| Tea utensils (kettle, caddy, bowls, whisk, tea jars) | 13 | upper homes, temples (A: tier marker) |
| Go / shōgi board | 11 | homes, services |
| Mirror / mirror stand | 9 | homes, shrines |

**A's tier markers (keep for dressing by rank):** tokonoma scroll and vase (upper, or a headman with permission);
shikidai entrance step (samurai, headman, honjin); crested lacquer (samurai); sword rack and armour chest (any samurai);
tea utensils (upper); many kura (upper). **A's rural-only core:** jizai-kagi, straw rope and straw work, hoe, sickle,
tawara, winnowing basket, mortar and pestle. **A's town-only core:** tatami, cotton futon, hibachi, tansu, andon,
chōchin, kōri trunk, clothes rack (ikō), folding screen for bedding. **A's everyday small items** (no count, in nearly
every home): fire-striker and tinder (hiuchi-ishi, hiuchi-gane, hokuchi), bowls and chopsticks, tobacco pipe (kiseru).

## 5.10 Build-once mechanisms and modules (from B and C)

- **One press** (stone-weighted lever press; wedge press) serves sake, soy, paper, oil, wax. (B)
- **One steamer-on-cauldron** serves sake, soy, miso, koji, paper bark, noodles, sweets, tofu. (B)
- **One pounding set** (usu and kine, treadle mortar, water-mill stamp, stone hand mill) serves rice, flour, clay, ore,
  incense, oil seed, porcelain stone. (B)
- **One drying kit** (bamboo poles and racks, boards leaned in the sun, rope lines, shinshi stretchers, mats on
  trestles) serves dyers, paper, noodles, fish, nori, umbrellas, tiles, pottery, hides, persimmons. (B)
- **One smithy core** (forge, fuigo, anvil, quench tub) serves every metal trade. (B)
- **One weapon rack, three fills** (display, armoury, dōjō). (C)
- **One lattice cell front** as a wall module (jails, holding rooms, sekisho jail, pilgrim-hall fronts). (C)
- **One great bell with log striker** serves temples, time bells, alarms. (C)
- **Glue and finish pots** (rice paste, hide glue, persimmon tannin, lacquer, oil) as one prop family. (B)
- **The religious corner** (kamidana, shimenawa, lucky rake) in almost every workshop and shop; the beckoning cat
  (maneki-neko) is `[outside 1680-1750]`. (B)

---

# 6. Collapse candidates (SUGGESTIONS ONLY: Stephen decides)

Merged from A's 15, B's 31 and C's 15 suggestions, deduplicated and grouped. Source tags in brackets (A4 = A's
suggestion 4). Each group: **Merges** · **Keeps** (signature items that make the merged building read right) ·
**Loses** (what goes if Stephen takes it). Nothing here has been applied to §3.

## 6.1 Dwellings

1. **Poor rural hut** [A1]. Merges: tenant, doza, nago, day labourer, widow, Kinai bamboo-floor, woodcutter's,
   charcoal-burner's village house, slash-and-burn house. Keeps: one shell in 2 sizes; doza vs board floor as a floor
   swap; irori, pot, water jar, straw bedding; occupant prop sets (farm / charcoal / woodcutter / cotton / fisher).
   Loses: the bamboo-slat floor as its own look; the dependent (nago) hut's siting in a master's yard.
2. **Seasonal huts and shelters** [A2]. Merges: paddy watch, kiln hut, yakihata field hut, hunter's hut, raftsman's hut,
   field hut, famine shelter, fire-ruin shack, riverbank squatter. Keeps: one lean-to and one small hut, dressed per
   role (clappers, charcoal bales, pelts, raft poles, gruel pot, scorched chest). Loses: individual silhouettes.
3. **Bunk hall** [A3]. Merges: logging-crew camp, porters' bunkroom, river porters' row (+ fishing-camp shed,
   retainers' barracks could join). Keeps: long board sleeping platform, long hearth, shared quilts; fill = saws and
   log hooks / kago and dice / rendai platforms. Loses: the river porters' rendai stacks outside as a distinct
   street front.
4. **Middle farmhouses** [A4]. Keep as shells: Kantō three-room (with and without inside stable) and Kinai four-room
   (with ox). Merges as prop sets or add-ons: cotton, tea, dry-field, flood (mizuya add-on), kabata room, separate
   kitchen (kamaya add-on), sericulture, support-village farmer. Loses: the flood-country mound and the Ōmi kabata as
   standalone landmarks unless kept as add-ons.
5. **Mountain houses** [A5]. Merges: Kiso and Hida board-roof houses; the Kiso post-town house shares the kit. Keeps:
   stone-weighted board roof, irori with hidana rack, snow gear, quern. Loses: Hida's lower pitch as a variant.
6. **Headman houses** [A6]. Merges: Kantō nanushi, Kinai shōya, ōjōya, daikan family, gōnō, net boss, salt-field owner,
   horse dealer, honjin family rooms. Keeps: two shells (east thatch; Kinai thatch-and-tile), shikidai, stove bank, kura,
   ledgers; wealth shown by fill (brewery ledgers, net stores, stables). Loses: ōjōya's office wing and daikan-ke's
   weapons as structure (they become props).
7. **Back-alley tenements** [A7]. Merges: Edo single and two-room, mune-wari, Kyoto roji, Osaka bare, castle-town row.
   Keeps: one kit with 1- and 2-room units, a Kyoto stove swap, an empty unit; occupations as dressing sets; the alley
   court site kit (well, toilet, rubbish box, Inari, kido). Loses: Osaka's bare-frame rental and the ridge-split row as
   distinct forms.
8. **Townhouses** [A8]. Merges: Kyoto and Osaka machiya; castle-town machiya reuses the region's. Keeps: Kamigata
   machiya (tōri-niwa, kudo row, hibukuro, tsubo-niwa) and a separate Edo machiya (dashigeta eaves, nurigome). Loses:
   Osaka's hettsui as a separate kitchen.
9. **Small professional homes** [A9]. Merges: doctor, terakoya teacher, arts teacher, landlord agent, rōnin: dressing
   sets on the small machiya or nagaya unit. Keeps: medicine cabinet and yagen; desks and copybooks; instruments;
   account books; sword rack and umbrella frames. Loses: nothing structural.
10. **Low samurai** [A10]. Merges: ashigaru row, gokenin, dōshin (one row / small-house kit); lower castle-town samurai
    and gōshi (one small detached house with gate). Keeps: jingasa, crested coat, side-job gear; sword rack, armour
    chest, spear over the door. Loses: Hatchōbori dōshin plots with rented-out rooms.
11. **Upper samurai** [A11]. Merges: mid-rank, hatamoto, karō = one kit at three plot sizes; daimyo kami / naka /
    shimo-yashiki = one hero complex; edo-zume barracks reuse the ashigaru row. Keeps: roofed gate, nagaya-mon,
    genkan with shikidai, tokonoma and tsuke-shoin, armour display. Loses: the naka / shimo-yashiki garden-villa
    character.
12. **Religious homes** [A12]. Merges: shake, farmer-priest, oshi, village yamabushi onto the headman or small-farm shell
    with a ritual prop set. Keeps: the Kamigamo shake as a distinct look if a Kyoto district is built. Loses: the oshi
    house's pilgrim-lodging scale.
13. **Hermitages** [A13]. Merges: sōan and hōjō-an one hut; yamabushi and carver huts are prop sets; C's hermitage (an)
    is the same building. Keeps: low desk, inkstone, Buddha image, kettle; conch and goma hearth; half-carved figures.
    Loses: nothing.
14. **Outbuildings** [A15]. About 7 kits for A's 25: kura (dozō + itagura), one shed (barn / pounding / wood / net /
    drying by props), stable (horse or ox), toilet, bath hut, roofed well, nagaya-mon. Loses: ash shed, cellar, hen coop
    as structures.

## 6.2 Shops, food, lodging and services

15. **Retail shop shells** [B27]. A few shells (small shop, big draper-style shop, wholesaler with kura) with swapped
    goods cover: general goods, ironmonger, ceramics, lacquerware, draper, old clothes, haberdasher, paper, oil,
    charcoal, tobacco, travel goods, souvenirs, arms, second-hand. Keeps: standard shop-front kit + goods display.
    Loses: shop-specific fronts (Uirō's castle-style front, giant 3-D signs) unless kept as signs.
16. **Brewery complex and ferment shop** [B18]. Merges: sake, soy, miso, vinegar, mirin, koji, pickles into one
    brewery complex (tubs, press, steamer, koji room); small miso, pickle and koji shops into one ferment shop. Keeps:
    the sake brewery's sugidama as the hero. Loses: soy's wheat roaster, vinegar as its own trade.
17. **Wet food shop** [B19]. Merges: tofu, konnyaku, yuba, fu, nattō. Keeps: stone hand mill, cauldron, press, water
    tanks. Loses: nattō's warm cellar, yuba trays.
18. **Mills** [B20]. Merges: water mill, rice polisher, flour shop, and the milling steps of oil, incense and clay.
    Keeps: water-mill site (wheel, cam stamps, stone mill) and a town treadle-mortar shop. Loses: the flour shop front.
19. **Eatery and sweets** [B21]. Merges: soba, udon, kendon, meshiya, nimeuri, chameshi → one eatery (kitchen doma +
    raised eating edge), restaurant as the upscale version; mochi, manjū, senbei, candy, cheap sweets → one sweet shop,
    fine confectioner a dressing upgrade. Loses: soba's seiro and noodle knife as a distinct shop.
20. **Tea houses** [B22]. Merges: kake-jaya, tateba-jaya, mizu-jaya, amazake shop, sencha stall → one roadside tea house
    in three sizes (bench shed, open shop, tateba with rooms); theatre, sumō and rendezvous tea houses → one town tea
    house. Loses: Hakone's Amazake-chaya as a named landmark unless kept.
21. **Stall kit** [B23]. Merges: every yatai, market stall, fortune-teller, barber booth, flower seller, show booth.
    Keeps: small roof, stove, pot, lantern with the dish name, mats and trestles. Loses: nothing structural.
22. **Lodging** [B24; C15]. Merges: hatago, meshimori hatago, kō-yado, kuji-yado, horse-dealers' inn → one hatago with
    sign variants; kichin-yado and hito-yado → a nagaya cheap lodging; hot-spring inn and communal bath → an onsen inn
    plus bath house (Hakone-specific; B says worth keeping distinct); honjin and waki-honjin share one shell
    (waki-honjin = honjin without the gate, smaller jōdan room). Loses: kuji-yado's writing room, kō plaques (become
    props).
23. **Merchant with kura** [B25]. Merges: moneychanger, pawnshop, rice broker, stipend agent, lender. Keeps: strong
    lattice, money chest, scales, ledgers, kura. Loses: Dōjima's open trading floor (the 1730 anchor) unless kept.
24. **Apothecary** [B26]. Merges: doctor, medicine shop, moxa, acupuncture, dentist (+ A's doctor's house). Keeps: drug
    chopper (yagen), many-drawer cabinet, paper packets. Loses: the dentist's denture kit as its own place.
25. **Stable yard** [B28, with A15 and C]. Merges: commercial stable, horse dealer, packhorse carrier, palanquin stand,
    cart haulage (+ A's stables and C's tenma relay stables; the castle stable could share it at size). Keeps: straw
    horseshoes, pack saddles, mangers, tie rails, trough. Loses: Hikone's L-shaped 21-stall castle stable as a
    landmark.

## 6.3 Crafts by family

26. **Smithy** [B1]. Village, tool, knife, saw, file, nail, anchor smiths → one smithy (forge, bellows, anvil, quench
    tub + a wall of the product). Swordsmith = same shell with shimenawa and a dark forge room. Loses: the anchor
    smith's crane and oversize hearth.
27. **Sword finishing** [B1]. Polisher, scabbard, hilt and fittings makers → one raised-floor room. Loses: nothing big.
28. **Foundry** [B2]. Pot caster, mirror maker, pewterer → one foundry (crucible furnace, moulds, sand floor); bell
    casting stays a site kit. Loses: mirror polishing bench.
29. **Metal bench workshop** [B3]. Ornamental metal, gold leaf, needle, wire, lock, pipe, stirrup, cloisonné, clock →
    one raised-floor bench with a small hearth; product boards swap. Loses: the wire drawer's long draw bench.
30. **Leather** [B4]. Carcass yard, white tanner, smoked leather, glue maker → one riverside tannery site (pits, frames,
    smoke hut, cauldron). Drum, saddle, pouch, inden, setta, glove, garment, shamisen → one leather workshop with a
    drum or saddle as the hero prop. This is the "3 leather buildings → 1" case.
31. **Timber yard and joinery** [B5]. Carpenter's yard, sawyer, lumber yard, shingle splitter → one timber yard.
    Joiner, cabinet maker, box maker, abacus, masu, mortar maker, instrument makers → one joinery workshop. Loses:
    the Kiba log pond unless kept as a site.
32. **Round wood** [B6]. Cooper, tub maker, bentwood → one cooperage. Woodturner and Hakone woodcraft → one lathe
    workshop (+ souvenir shop front on the Hakone road).
33. **Bamboo** [B7]. Baskets, sieves, blinds, fans, umbrellas, tea whisks, lanterns, bows and arrows → one bamboo
    workshop with umbrella / lantern / fan dressings, plus the umbrella drying yard.
34. **Straw and rush** [B8]. Straw goods, rope, rush mats, tatami, sedge hats, palm fibre → one straw and rush workshop
    (tatami maker could stay separate as a common town shop). Loses: the rope walk's long yard.
35. **Cotton and silk prep** [B9]. Ginner, bower, wadding, futon → one cotton shop. Silk reeling, floss, thread,
    sericulture → a silk farmhouse variant (A's shell).
36. **Weaving** [B10]. Village weaver, ikat, wild fibre → one loom room; Nishijin drawloom the rich variant.
37. **Dyeing** [B11]. Indigo, stencil, yūzen, shibori, safflower, black and crest dyers (+ stencil cutter) → one dyer's
    shell with sunken vats and yard frames; the Awa indigo barn stays rural. Loses: the 6-m stencil boards as a
    distinct room.
38. **Sewing room** [B12]. Tailor, embroiderer, tabi maker, braid maker, mosquito nets → one tatami sewing room.
39. **Kilns** [B13]. Noborigama, anagama, porcelain, enameller → one pottery site; earthenware and tile maker → a
    small-kiln tile works; lime and charcoal kilns are look-alike earth domes.
40. **Stone** [B14]. Mason's yard, quarry, whetstone dealer, inkstone carver → mason's yard plus a quarry site.
41. **Paper and print** [B15]. Paper mill, recycled paper, kakishibu → paper mill site. Publisher, carver, printer,
    binder, bookseller, lending library → one publisher-bookshop with a back print room. Mounter and painter → a
    painting studio.
42. **Lacquer** [B16]. Refiner, lacquerer, maki-e → one lacquer workshop (the dust-free drying cupboard is the tell).
43. **Temple-street workshop** [B17]. Buddhist sculptor, rosary, incense, candle, doll, mask → one workshop with swapped
    goods.

## 6.4 Rural industry

44. **Fishing-village kit** [B29]. Net shed, fish-drying racks, sardine works, katsuobushi smokehouse, nori drying yard
    → one kit with rack variants; salt pans plus boiling hut stay distinct. Loses: the katsuobushi smoke room as its
    own building.
45. **Mine site** [B30]. Gold, silver, copper, sulphur → one mine site (adit, sorting shed, smelter hut); tatara is
    off-map and could be cut.

## 6.5 Shinto and Buddhist

46. **Micro-shrine family** [C5]. Roadside, field, house-plot, alley Inari, sub-shrine, summit shrine → one micro-shrine
    in wood and one in stone, plus 4–5 prop swaps (fox pair, sakaki, shimenawa, torii).
47. **Shrine ladder to three** [C7]. Village chinju (saya-dō + small haiden); town shrine (haiden + honden + kagura
    stage + mikoshi store); one hero shrine (add rōmon, kairō, sub-shrine row, a pagoda for syncretism). Loses: the
    Tōshōgū's gongen colour and Ise as unique builds unless kept as heroes.
48. **Small sacred hall** [C4]. Jizō / Kannon / Yakushi / Kōshin / Enma dō, village haiden, ema hall, pilgrim overnight
    hall, village assembly place → one 2 × 2 or 3 × 3 ken board hall with veranda; fill decides. Loses: nothing
    structural.
49. **Temple ladder to three** [C6]. (a) village temple: hondō-kuri + bell tower + graveyard; (b) town temple: gate +
    hondō + kuri + bell + graveyard; (c) one hero complex (Zen seven-hall or Pure Land mieidō). Sect differences as
    prop swaps (unpan and han for Zen; fan drum and daimoku pillar for Nichiren; drum tower and big tatami gejin for
    Shinshū). Loses: the many single-purpose precinct halls (tahōtō, kaidan-in, kake-zukuri) outside the hero.

## 6.6 Government, military and civic

50. **Guard-post hut** [C1]. Kidoban, jishinban, tsuji-ban, bridge-keeper, ferry hut, water-guard hut, tōmi-bansho,
    domain border post, holding station → one 1–2-room board hut (bench, lantern, brazier, tool rack); the difference
    is one prop (sundries counter, fire ladder, toll box, spyglass).
51. **Official compound** [C2]. Bugyōsho, jinya / daikansho, kōri-bugyōsho, domain office, shoshidai office, Uraga
    bugyōsho, kanjōsho → black nagaya-mon + genkan + office rooms + white-gravel court + kura, varied by size and by
    whether it has a court and cells.
52. **Open-front office with a yard** [C15]. Toiya-ba, kawa-kaisho, kanme-aratame-sho → one shell; fill (fare board,
    depth gauge, big scale) decides.
53. **Kura family** [C3, A15]. Gōkura, o-kura, kura-yashiki, treasury, powder magazine (stone variant), armoury, shrine
    treasure store, mikoshi store, temple store, library (+ A's dozō / itagura / kome-gura, B's rented kura) → one kura
    shell; interior fill changes. Loses: the Asakusa comb-tooth boat inlets unless kept as a site.
54. **Castle** [C8]. One keep (or, cheaper and period-correct for Edo / Osaka, a bare keep base), one turret in two
    heights, one box-gate pair, one tamon module, one palace wing module repeated, plus the ruin set for abandoned
    castles; named storage turrets become prop fills. Loses: moon-viewing turret, named turrets.
55. **Training grounds** [C9]. One dōjō hall (sword / spear / jūjutsu fills), one archery range, one horse track. Drop
    gunnery range, tōshiya, yabusame and swimming site unless a landmark is wanted.
56. **Schools** [C10]. One terakoya room fill (any temple guest room or machiya upstairs) and at most one Confucian hall
    (Shizutani as hero). Drop domain schools as a type for 1730 (most post-1750).
57. **Bridges** [C11]. Plank, trestle (hero), arched, earth-covered, boat bridge; drop vine, cantilever and stone arch
    unless the terrain wants a landmark.
58. **Water** [C12]. Three wells (pulley, lever, aqueduct box) + one sluice + one weir; drop aqueduct bridge, water
    sellers' landing and reservoir unless mapped.
59. **Death** [C13]. One graveyard kit (sotoba rack, six Jizō), one cremation hut; the execution ground built from
    existing fence, stone base and Jizō parts.
60. **Fire** (merge note, not in the agents' lists). Fire watchtower and fire ladder could share one tower kit at two
    heights; the brigade compound is an official compound with a tower.

## 6.7 Likely outright cuts (as the agents proposed)

- **B's list [B31]:** gunsmith, tinplate, clockmaker, spectacles, whaling, oysters, cormorants, sugar press, shippoku,
  tempura stalls, women's hairdresser, yose, insect sellers, shiitake, hanafuda, the pleasure quarters (keep or cut is
  Stephen's call), gambling den. B also flags as "may cut": shōchū still, firework maker, deai-jaya, meshimori staffing
  (keep the building, drop the role).
- **A's list [A14]:** everything tagged `[off-map]` or `[outside 1680-1750]` except as late-game colour: chūmon,
  magariya, kabuto, takahe, Kyushu forms, ebune, sericulture lofts. A also: azekura in homes ("probably drop"); onbō
  hut ("mention neutrally or drop").
- **C's list [C14]:** out of window: machi-kaisho (1791), gisō / shasō (mostly 1790s), daiba batteries (1850s),
  ryūdosui pump (1750s+), Shōheikō (1797), hyakushō-rō (1775), full kendō armour (1750s+), most beacon chains
  (1800s). C also: Ji-shū stages ("skip unless needed"), domain schools as a type.

## 6.8 Rough shell count

682 counted entries today. Rough number of distinct building models (shells) after collapsing, by category. "Light"
= only the obvious same-shell merges, regional and hero variants kept. "Heavy" = the agents' full suggestions plus
shared shells across lanes (one kura, one hut, one workshop per floor type). Cuts in 6.7 are removed in both.

| Category | Entries now | Light | Heavy |
|---|---|---|---|
| Dwellings, poor (incl. hermits) | 48 | 9 | 3 |
| Dwellings, lower-middle | 47 | 12 | 5 |
| Dwellings, upper | 21 | 11 | 5 |
| Outbuildings | 21 | 8 | 5 |
| Shops and retail | 30 | 5 | 3 |
| Food and drink | 58 | 13 | 6 |
| Lodging | 12 | 6 | 3 |
| Services | 38 | 9 | 4 |
| Crafts by family | 161 | 30 | 12 |
| Rural industry | 30 | 10 | 5 |
| Shinto | 32 | 10 | 5 |
| Buddhist | 46 | 15 | 6 |
| Government | 41 | 11 | 6 |
| Military | 38 | 13 | 7 |
| Civic and infrastructure | 59 | 17 | 8 |
| **Total** | **682** | **~180** | **~80** |

**Range: roughly 80 (heavy) to 180 (light) shells**, with most of the difference in crafts (one shell per trade
family vs one per floor type) and dwellings. Many "shells" in the civic and military rows are open structures
(bridges, wells, gates, tracks) rather than enterable buildings.

---

# 7. To verify

Every `(verify)` flag in this file, in order, with where it sits. B's `[uncertain]` flags were folded into `(verify)`.
The contradictions in §4.2 are also open checks and are not repeated here.

**Settlement layouts (§2)**
- [ ] 2.1 Rice-farming village: ~400 koku average village (arithmetic from the Genroku registers).
- [ ] 2.2 New-field village: Santome plot size ~40 × 675 m.
- [ ] 2.3 Mountain village: Owari's Agematsu timber office and the "five trees" felling ban, c.1708.
- [ ] 2.7 Castle town: ~170–190 castles and ~100+ jinya daimyo in 1730.
- [ ] 2.15 Outcast settlements, and Government / Law: Shinagawa hinin infirmary (tame) date, c.1698.

**Dwellings**
- [ ] Poor / rice villages: Kinai tenant house: how common the bamboo floor (take-yuka) still was by 1730.
- [ ] Poor / coast: Nori farmer's cottage: start date of Shinagawa nori (c. Genroku–Kyōhō).
- [ ] Poor / urban: Edo single ura-nagaya unit: tatami in the cheapest units (fallback boards + goza).
- [ ] Poor / urban: Osaka back-alley row: the hadaka-gashi (rented bare) detail.
- [ ] Poor / marginalised: Cremation-ground attendant's hut (onbō): mention neutrally or drop.
- [ ] Lower-middle / farmhouses: Four-room grid farmhouse: zabuton for guests (rare).
- [ ] Lower-middle / mountain: Honmune-zukuri: whether the form reaches the window (mostly after 1750).
- [ ] Lower-middle / urban: Kyoto machiya: date of the Fushimi-doll Hotei row on the Kōjin shelf.
- [ ] Outbuildings: Log storehouse (azekura) in homes: probably drop.
- [ ] Outbuildings: Ash shed (haiya): Kinki and Chūbu.
- [ ] Outbuildings: Bath hut: goemon-buro / teppō-buro split (late source) for 1730.
- [ ] Outbuildings: Hen coop: egg-eating rises later.
- [ ] A's date traps: no side-handled teapot.

**Shops and retail**
- [ ] Insect seller: mostly mid–late Edo.

**Food and drink**
- [ ] Mirin maker: how widespread in 1730.
- [ ] Rice-cracker shop: when salty rice senbei spread.
- [ ] Candy maker: date of the sugar-sculpture street craft.
- [ ] Eel shop: shops mostly c.1770s+.
- [ ] Dengaku stall: simmered oden in broth is later.
- [ ] Wild-meat shop (momonji-ya): mostly later Edo.
- [ ] Chinese-style banquet house (shippoku): when it spread to Kyoto and Edo.
- [ ] Tea-leaf dealer: the roasting pan (hōji-nabe).
- [ ] Kamaboko maker: Odawara fame is late 18th c.

**Lodging**
- [ ] Confraternity inn (kō-yado): earlier Ise-kō affiliated inns.

**Services**
- [ ] Steam bath: largely replaced in cities by 1730.
- [ ] Rice exchange: water towers or flags used to signal prices.
- [ ] Scribe and petition writer: a separate trade at all.
- [ ] Archery gallery (yōkyū-ba): mostly mid–late Edo.
- [ ] Rental shop (sonryō-ya): date.

**Crafts: metal**
- [ ] Anchor smith: which *Shokunin burui* plate.
- [ ] Carpenter's-tool smith: how early Miki's fame is.
- [ ] Saw smith: the double-edged ryōba date (late Edo / Meiji).
- [ ] File maker: the source plate.
- [ ] Pot caster: tetsubin date (see contradiction 1).
- [ ] Coppersmith: the source plate.
- [ ] Pewterer: period.
- [ ] Gold-leaf beater: the haku-za guild, c.1696.

**Crafts: leather**
- [ ] Leather tabi and glove maker: cotton tabi replacing leather after the 1657 fire.

**Crafts: textiles**
- [ ] Silk thread twister: Kiryū water-powered mills c.1780s.
- [ ] Ikat weaver: simpler kasuri before c.1800.
- [ ] Indigo dyer: an in-era plate (Hiroshige's Kanda Kon'ya-chō is 1857; check *Jinrin kinmōzui*).
- [ ] Braid maker: date of the takadai stand.
- [ ] Futon maker: how common cotton bedding was in 1730.
- [ ] Sailcloth maker: 1730 sails as narrow sewn cotton strips.

**Crafts: ceramics, stone, glass**
- [ ] Earthenware maker: date of the small clay shichirin stove.
- [ ] Roof-tile maker: kiln form for 1730 (updraught or "daruma").
- [ ] Stone quarry: how active the Izu quarries were in 1730.
- [ ] Glassmaker: Edo glass in 1730 (Osaka glass c.1750s).

**Crafts: paper, lacquer, fine**
- [ ] Lantern maker: Odawara chōchin founding date (early 18th c.).
- [ ] Incense maker: date of the mechanical extruder.
- [ ] Spectacle maker: date.

**Rural industry**
- [ ] Gold or silver mine: how active in 1730.
- [ ] Sulphur workings: whether Ōwakudani was worked in 1730.
- [ ] Oil press: Hyōgo / Nishinomiya water-driven oil mills c.1790s+.
- [ ] Mushroom logs: Izu Amagi shiitake from the 1790s.

**Government**
- [ ] Jinya: Takayama's rice store moved from the castle in 1695.
- [ ] Cargo weight-check station: the five stations and the c.1712 date.
- [ ] Asakusa o-kura: ~50 storehouses and 8 inlets.

**Military**
- [ ] Official ship sheds: the Atakemaru's shed and official boats staying at Fukagawa after 1682.

**Civic**
- [ ] Time-bell tower: Edo's count of official time bells (about nine).
