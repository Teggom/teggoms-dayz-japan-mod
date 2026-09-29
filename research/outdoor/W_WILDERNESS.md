# W: Wilderness man-made (outdoor list, flavour W)

Agent OD-W, 2026-09-29. Text only. Anchor year 1730; 1680–1750 fully in; wider Edo tagged.

**What this is.** Everything a person made that you find *between* settlements: on the highways, in the mountains, along
wild rivers and on the empty coast. It's the Japan equivalent of Chernarus's hunting stands, lone cabins, rest spots and
power lines. It's deliberately over-detailed. Stephen collapses it later (see "Obvious collapse candidates" at the end).

**Scope rule.** Anything with an interior stays in `research/buildings/BUILDING_LIST.md` (called **BL** below). Where BL
already has a `site` entry for an outdoor thing (ichirizuka, bridges, charcoal kilns, weirs, beacons), it's listed here
too, from the outdoor side, marked `(BL: section)`. The merge should count it once.

**Entry format.** `- **English (romaji)**: what and why. Setting, commonness, size. Hook: ... [source]`

- **Setting:** roadside / mountain / forest / river / coast (combined where both apply).
- **Commonness, per map region:**
  - *common*: every few km of road, or every valley
  - *occasional*: a few per region
  - *rare*: a handful per map
  - *landmark*: a named one-off
- **Size:**
  - *small prop*: under ~2 m, one object
  - *medium*: 2–6 m, or a small cluster
  - *large structure*: over 6 m
  - `[terrain]`: earthwork, ground shaping or a linear feature
- **Hooks:** shelter, landmark, water, loot spot, navigation, danger, food, warmth, fire, cover, lore.
- **Tags** (as in BL):
  - `[outside 1680-1750: date]`
  - `[off-map: region]` (the map is the Kyoto–Osaka–Edo / Tōkaidō / Nakasendō belt)
  - `(assumed)`: my reading, not pinned to a source
  - `(verify)`: I have a source memory but didn't re-check it
- **Hakone note.** The test terrain's DEM is Hakone, so Hakone-area landmarks are called out where I found them. They're
  unusually rich: stone paving, a cedar avenue, cliff Buddhas, a sekisho, castle ruins, an aqueduct tunnel, and 1707
  ash-damage works.

**Source shorthand:**
- **WC**: `playbook/WORLD_CATALOGUE.md`
- **Kaempfer**: Engelbert Kaempfer's Tōkaidō journeys, 1691–92 (in window)
- **WSZ**: *Wakan sansai zue* (1712, in window)
- **Bunken ezu**: *Gokaidō bunken nobe ezu* (1806), road maps that show every mound, sign and bridge
  `[outside 1680-1750: 1806]`, used only as a depiction source
- **Hiroshige**: *Tōkaidō gojūsan tsugi* (1833–34) `[outside]`, depiction only

Web sources are listed at the end.

**Counts per group (counted entries; cross-reference pointers not counted).**

| # | Group | Entries |
|---|---|---|
| 1 | Highway distance and direction markers | 17 |
| 2 | Road surface, avenues and pass works | 21 |
| 3 | Rest, water and wayside comfort | 16 |
| 4 | River crossings in the wild | 19 |
| 5 | Wayside religious stones and figures | 32 |
| 6 | Mountain religion and pilgrim marks | 21 |
| 7 | Sacred rocks, trees and waters | 13 |
| 8 | Forest work: charcoal, timber, wood | 25 |
| 9 | Hunting, trapping and river fishing | 23 |
| 10 | Mining, quarrying, digging, hot springs | 18 |
| 11 | Mountain produce | 9 |
| 12 | River and slope works | 13 |
| 13 | Boundaries, bans and control | 21 |
| 14 | Lookouts, beacons and signals | 11 |
| 15 | Ruins: castles, forts, barriers | 19 |
| 16 | Ruins: settlements, temples, work sites | 13 |
| 17 | Graves, mounds and memorials | 21 |
| 18 | Disaster, execution and punishment marks | 9 |
| 19 | Wild coast: work | 17 |
| 20 | Wild coast: navigation, wrecks, sacred | 14 |
| 21 | Traces, camps and props of passage | 20 |
| | **Total** | **372** |

---

== 1. Highway distance and direction markers ==

- **Mile mound pair (ichirizuka)**: a pair of earth mounds, one each side of a main highway every ri (~3.9 km). Each is
  ~9 m square and ~3 m high, topped with an enoki (hackberry), pine or cedar. Ordered in 1604 and kept up by the nearby
  villages. Roadside, common on the Tōkaidō, Nakasendō and Kōshū, large `[terrain]`. Hook: navigation (counting mounds
  gives distance), a tree visible from afar, shade, a rest spot. (BL: Civic, roads) [WC T22; Kaempfer]
- **Lone surviving mile mound (kata-ichirizuka)**: a pair where one mound has been ploughed away or washed out, leaving
  one mound and its tree. Roadside, occasional, medium `[terrain]`. Hook: navigation, landmark tree. (assumed for 1730;
  many survive singly today)
- **Mile mound on a minor road (waki-kaidō ichirizuka)**: smaller mounds, or just a planted tree, kept by the domain on
  side roads (Ōyama road, Kōshū branch roads). Roadside, occasional, medium `[terrain]`. Hook: navigation. (verify how
  regular they were on side roads)
- **Fork direction stone (oiwake-ishi / michi-shirube)**: a stone post at a fork carved "right, to Edo; left, to
  Zenkōji". The Shinano Oiwake, where the Hokkoku road leaves the Nakasendō, gave the type its name. Roadside, common at
  forks, small prop. Hook: navigation (readable in-game text). (BL: Civic, roads)
- **Deity direction stone (michi-shirube Jizō / kōshin michi-shirube)**: a Jizō, Kannon or kōshin stone with directions
  carved on its side or base, so one stone does two jobs. Roadside, occasional, small prop. Hook: navigation, offerings.
  (verify frequency before 1750)
- **Pointing-hand direction stone (yubisashi michi-shirube)**: a carved hand pointing down the road, with a destination.
  Roadside, rare, small prop. Hook: navigation. (verify; many surviving examples are later Edo)
- **Wooden signpost (michi-shirube-gui / kidō-hyō)**: a squared post with brush-written or cut destinations. Most were
  wood, so few survive. Roadside, common, small prop. Hook: navigation. (assumed)
- **Pilgrim-route marker (junrei michi-shirube)**: a stone saying "to temple no. N of the Kannon circuit, X chō". It
  marks the pilgrim path off the highway. Roadside/mountain, occasional, small prop. Hook: navigation to a temple.
  (assumed form; the circuits are in era)
- **Chō-stone countdown (chōishi)**: numbered stones every chō (~109 m) counting down to a temple or summit. The
  landmark set is Kōyasan's: 3 m stupa-shaped stones, 1285, ~180 originals of 216. Plainer chōishi stood on many
  mountain approaches. Mountain, occasional (landmark at Kōya), small prop (landmark set: medium each). Hook: navigation
  (a countdown to the top). Kōya `[off-map: Kii]`. [Wikipedia: Kōyasan chōishi-michi]
- **Mountain station marker (gōme-ishi / gōme-hyō)**: a marker for a climb's stations (1st to 10th gō), as on Fuji's
  pilgrim trails. Mountain, rare, small prop. Hook: navigation, altitude cue. (verify form and date before 1750)
- **Pass name post (tōge no hyōchū)**: a post at the summit naming the pass and the provinces on each side. Mountain,
  occasional, small prop. Hook: navigation, landmark. (assumed)
- **Trail cairn (ishizumi / kerun)**: a small stone pile marking the route over bare rock, scree or open ridge.
  Mountain, occasional, small prop. Hook: navigation off-road. (assumed)
- **Hatchet blaze (nata-me / kizuke)**: a cut or peeled patch on trunks marking a woodsman's or hunter's path. Forest,
  occasional, small prop (a decal on trees). Hook: navigation along hidden trails. (assumed)
- **Bent-branch route mark (shiori / eda-ori)**: branches snapped or bent to mark the way back. It's the origin of the
  word *shiori* (bookmark). Forest, occasional, small prop. Hook: navigation, a tell that someone passed. (assumed as a
  period practice; the etymology is standard)
- **Snow-route poles (yuki-michi shirube)**: tall poles or tagged stakes marking the road under deep snow on Kiso and
  Hokuriku passes. Mountain, rare (seasonal), small prop. Hook: navigation in snow. (assumed)
- **Distance board at a ferry or crossing (michinori-fuda)**: a board giving the distance to the next post town and the
  fares. Roadside/river, occasional, small prop. Hook: navigation. (assumed; the fare boards are in BL, ferry landing)
- **Survey stake (kenchi-gui / nawa-ba)**: stakes and rope lines left by land surveyors checking village land and
  forest limits. Forest/roadside, rare, small prop. Hook: lore. (assumed)

== 2. Road surface, avenues and pass works ==

- **Stone-paved pass road (ishidatami)**: rounded fieldstones laid as paving on steep pass sections. Hakone's was laid
  in 1680 (Enpō 8), replacing bamboo mats. Mountain/roadside, rare (passes only; landmark at Hakone), `[terrain]`. Hook:
  the road line, slippery and noisy in rain (danger), navigation. (BL: Civic, roads) [WC §1.6, T53; Hakone navi]
- **Bamboo-mat road (take-shiki no michi)**: Hakone's pre-1680 surface: bamboo mats laid over the mud and renewed
  every year by the villages. Mountain, rare, `[terrain]`. Hook: lore. `[outside 1680-1750: before 1680]`
- **Cross drains in paving (yoko-mizo / mizu-kiri)**: diagonal stone gutters across a paved or earth road that shed
  rain off the slope. Mountain, common on paved stretches, small prop. Hook: none (dressing). (assumed; visible on the
  surviving Hakone paving)
- **Cedar avenue (sugi-namiki)**: cedars planted along the road for shade and shelter:
  - Hakone's: about 400 remain by Lake Ashi, planted in 1618 (attributed to Matsudaira Masatsuna)
  - Nikkō's: ~37 km, 1625–48, by Masatsuna
  Roadside/mountain, rare (landmark at Hakone), large `[terrain]`. Hook: landmark, shade, cover, a line to follow.
  Nikkō `[off-map: Nikkō]`. [Hakone navi; Wikipedia: Cedar Avenue of Nikkō]
- **Pine avenue (matsu-namiki)**: black pines planted along the main highways on the plains and the coast. It's the
  Tōkaidō's signature. Roadside, common, large `[terrain]`. Hook: navigation (the road from afar), cover. [WC §2.6, T53]
- **Hackberry or mixed-tree row (enoki-namiki)**: shorter tree rows at village approaches and crossroads. Roadside,
  occasional, `[terrain]`. Hook: navigation. (assumed)
- **Road cutting (kiridōshi / horiwari)**: a road cut through a ridge between steep banks. The Kamakura cuttings
  (Asaina, Nagoe) are medieval examples near the map. Roadside/mountain, occasional, `[terrain]`. Hook: ambush point,
  chokepoint, cover.
- **Switchback trail (tsuzura-ori)**: a zigzag path up a steep slope, sometimes with a named count of turns. Mountain,
  common, `[terrain]`. Hook: slow movement, navigation.
- **Stone steps up a pass (ishidan / ishi-kaidan)**: rough stone stairs on the steepest pitches and at shrine
  approaches. Mountain, occasional, medium `[terrain]`. Hook: movement, landmark.
- **Log steps (maruta-dan)**: logs pegged across a mountain path as steps. Mountain, common, small prop (repeated).
  Hook: movement. (assumed)
- **Road retaining wall (michi no ishizumi)**: dry-stone walling holding a road shelf on a hillside or riverbank.
  Mountain/river, occasional, medium `[terrain]`. Hook: cover, a fall edge (danger). (assumed)
- **Cliff plank road (kakehashi / kake-michi)**: a timber gallery pinned to a cliff face over a river. The landmark is
  the Kiso no Kakehashi on the Nakasendō: burned 1647, rebuilt with stone walling, so by 1730 it's part stone. Mountain/
  river, landmark (small cliff galleries rare), large structure. Hook: danger (fall), chokepoint, landmark. (verify the
  1647/48 rebuild details)
- **Chain climbs on sacred peaks (kusari-ba)**: iron chains fixed down rock faces on pilgrim ascents (Ishizuchi,
  Myōgi). Mountain, rare, medium. Hook: climbing, fall danger, landmark. (verify dates; some chains may be later Edo)
- **Wooden ladders on rock steps (kake-bashigo)**: ladders tied in place on pilgrim routes where the rock is too steep.
  Mountain, rare, small prop. Hook: climbing, fall danger. (assumed)
- **Hand-dug rock tunnel (tonneru / dōmon)**: a road tunnel chiselled by hand. The famous Ao-no-Dōmon, dug by the monk
  Zenkai 1735–63, is in window but in Kyushu. Mountain, landmark, large `[terrain]`. Hook: chokepoint, shelter, lore.
  `[off-map: Kyushu]`
- **Corduroy track over bog (sodagi-michi / kijiki)**: logs or brushwood laid across wet ground. Forest/river,
  occasional, `[terrain]`. Hook: movement through marsh. (assumed)
- **Old abandoned road alignment (kyūdō / furumichi)**: an overgrown earlier route, such as the medieval Yusaka road over
  Hakone, disused after the Edo Tōkaidō was laid. Mountain/forest, rare, `[terrain]`. Hook: a hidden path, a sekisho
  bypass (danger: illegal). (verify the Yusaka route)
- **Pack-ox path (ushi-michi / bokka-michi)**: narrow steep trade paths worked by oxen instead of horses. The salt road
  from the Japan Sea into Shinano (Chikuni road) is one. Mountain, occasional, `[terrain]`. Hook: navigation off the
  highways. (verify the ox use before 1750)
- **Road-repair gravel heaps (michi-bushin no suna)**: sand and gravel piles left by villages doing their road-repair
  duty, especially before a daimyō procession. Roadside, occasional, small prop. Hook: none (dressing). (assumed)
- **Stone cart rails (kuruma-ishi)**: grooved stone paving for ox carts on the Ōtsu–Kyoto road. Roadside, rare,
  `[terrain]`. Hook: lore. `[outside 1680-1750: laid 1805]`
- **Ditch-side road drains (sokkō / michi-bata no mizo)**: earth or stone-lined ditches along the highway. Roadside,
  common, `[terrain]`. Hook: cover (prone). (assumed)

== 3. Rest, water and wayside comfort ==

*Cross-reference, not counted: tea stalls in the middle of nowhere are buildings. See BL: roadside tea house (kake-jaya
/ chamise) and rest-station tea house (tateba-jaya). Only their outdoor spill (benches, tie posts) is below.*

- **Rest bench (koshikake / shōgi)**: a plank bench under a mile-mound tree, at a pass or by a spring. Roadside, common,
  small prop. Hook: rest, a landmark cluster.
- **Legend sitting stone (koshikake-ishi)**: a stone where a famous figure is said to have sat (Yoshitsune, Kōbō Daishi,
  a daimyō). It's often roped or fenced with a small board telling the story. Roadside, occasional, small prop. Hook:
  lore, landmark.
- **Porter's load-rest stone (niyasume-ishi / kata-yasume)**: a flat-topped stone or bank on a steep climb where porters
  set down their loads without unshouldering. Mountain/roadside, occasional, small prop. Hook: rest. (assumed)
- **Piped roadside spring (kakehi no shimizu)**: a spring led by a split-bamboo pipe into a stone or wooden basin, with a
  ladle on a stick. Many were named ("X-shimizu"). Roadside/mountain, common, small prop. Hook: WATER. (assumed form)
- **Kōbō spring (Kōbō-shimizu / Kōbō-ido)**: a spring said to have been struck from the rock by Kōbō Daishi's staff,
  marked with a stone or a tiny shrine. Roadside/mountain, occasional, small prop. Hook: WATER, lore.
- **Horse trough (uma no mizu-bune)**: a hollow log or stone trough fed from a stream, at a pass foot or a tea stall.
  Roadside, occasional, small prop. Hook: WATER. [WC §1.7 lists troughs as town dressing; this is the wild copy]
- **Horse tie stone (uma-tsunagi-ishi)**: a stone with a hole bored through it, or a tie post. Roadside, occasional,
  small prop. Hook: none (dressing).
- **Horse-washing ramp (uma-arai-ba)**: a shallow graded bank into a stream where packhorses were watered and washed.
  River, occasional, `[terrain]`. Hook: water access.
- **Open rain shelter (amayadori / azumaya)**: a thatched roof on four posts with no walls, at a pass, crossing or
  viewpoint. Roadside/mountain, occasional, medium. Hook: SHELTER (rain only). (assumed; if a bench-and-hearth version is
  wanted, it becomes a BL tea-stall shell)
- **Rock overhang camp (iwa-kage)**: an overhang with a soot-blackened roof, a fire ring and old straw, used by
  travellers, hunters and ascetics. Mountain, occasional, `[terrain]`. Hook: SHELTER, fire.
- **Travellers' fire ring (takibi-ato)**: a ring of blackened stones with charcoal and bones. Roadside/forest, common,
  small prop. Hook: fire, evidence of a camp.
- **Stone lantern at a dangerous spot (jōyatō)**: an "always-lit" stone lantern kept by a village or kō at a pass top,
  lake shore, crossroads or ferry. Roadside/mountain, occasional, medium. Hook: NAVIGATION (lit at night), light.
  (verify how many were really lit nightly in 1730)
- **Crossroads lantern post (tsuji-andon)**: a wooden lantern box on a post at a lonely junction. Roadside, occasional,
  small prop. Hook: light, navigation. (assumed)
- **Sandal-hanging tree or post (waraji-kake)**: worn and spare straw sandals hung on a tree or Jizō at a pass, as an
  offering or just discarded. Roadside, occasional, small prop. Hook: loot (spare sandals), lore.
- **Alms-giving stand (settai-dai)**: a plank table where villagers gave pilgrims tea, rice balls or straw sandals on set
  days. Roadside, rare, small prop. Hook: food/water (event). (settai is a Shikoku custom; elsewhere assumed)
- **Viewpoint clearing (miharashi / tōge no nagame)**: a cleared knoll at a pass with a bench and view. Hiroshige
  prints are full of them. Mountain, occasional, `[terrain]`. Hook: landmark, a scouting spot. (assumed as maintained)

== 4. River crossings in the wild ==

- **Stepping stones (tobi-ishi / ishi-watari)**: flat stones set across a shallow stream. River, common, small prop
  (repeated). Hook: crossing; washes over in spate.
- **Marked ford (watari-se)**: a gravel crossing with stakes or poles marking the shallow line. River, common,
  `[terrain]`. Hook: crossing, drowning danger when the river is high. (assumed)
- **Porter-wading crossing (kachi-watashi)**: an unbridged river crossed on porters' shoulders or on a litter (rendai).
  In the wild it shows as a worn gravel bank, a porter shelter and platforms. Tōkaidō rivers: Sakawa (near Odawara), Ōi,
  Abe. River, rare (landmark on the Tōkaidō), `[terrain]`. Hook: crossing, drowning danger, landmark. (BL: Government,
  river-crossing office) [Hiroshige Ōi views depict it]
- **Log bridge (maruki-bashi)**: one or two logs, sometimes with a pole handrail. River, common, small prop/medium.
  Hook: crossing, fall danger. (BL: Civic, roads)
- **Plank bridge (ita-bashi)**: boards on beams and posts. River, common, medium. Hook: crossing. (BL: Civic, roads)
  [WC §2.6]
- **Earth-covered bridge (dobashi)**: logs covered with brushwood, earth and turf. River, occasional, medium. Hook:
  crossing. (BL: Civic, roads)
- **Stone slab bridge (ishi-ita-bashi)**: one or two granite slabs over a ditch or narrow stream. River, occasional,
  small prop. Hook: crossing. [WC §2.6]
- **Cantilever bridge (hane-bashi)**: stacked cantilevered beams from each bank. The Saruhashi (Kōshū road) is the
  landmark; smaller ones span mountain gorges. River/mountain, landmark (small ones rare), large structure. Hook:
  crossing, landmark. (BL: Civic, roads)
- **Vine bridge (kazura-bashi)**: a suspension walkway of mountain vines with slat decking. Iya is the famous site.
  River/mountain, rare, large structure. Hook: crossing, fall danger (sway). `[off-map: Shikoku]` (generic mountain vine
  bridges elsewhere assumed) (BL: Civic, roads)
- **Basket rope crossing (kago-watashi / yaen)**: a basket slung on a rope across a gorge and hauled over. Etchū/Hida
  and Totsukawa are known sites. River/mountain, rare, medium. Hook: crossing, fall danger. (verify window; the famous
  print is Hiroshige, 1850s)
- **Hand-line across a stream (tsuna-watashi)**: a rope strung across a stream to hold while wading. River, occasional,
  small prop. Hook: crossing. (assumed)
- **Ferry landing, wild bank (watashi-ba)**: an earth or stone ramp with a mooring post, a waiting bench, and a bell or
  drum on a post to call the ferryman from the far bank. River, occasional, medium. Hook: crossing, SOUND (the bell),
  shelter (shed). (BL: Civic, ferry landing and ferry-keeper's hut)
- **Rope-guided ferry (hiki-bune)**: a rope across a narrow river that the ferry pulls itself along. River, occasional,
  medium. Hook: crossing. (BL: Civic) (assumed)
- **Boat bridge (funa-bashi)**: boats chained side by side with planks on top. River, rare (landmark at the Jinzū),
  large structure. Hook: crossing. (BL: Civic)
- **Seasonal low-water bridge (kari-bashi / fuyu-bashi)**: a temporary plank bridge built for the dry season and taken
  down before the summer floods. River, occasional, medium. Hook: crossing (seasonal). (verify which rivers)
- **Washed-out bridge remains (nagare-bashi no ato)**: stumps of piles and a broken abutment where a bridge went in a
  flood. Rokugō's bridge was lost in 1688 and replaced by a ferry. River, rare, medium. Hook: a broken crossing,
  landmark, cover. (BL notes the Rokugō ferry from 1688)
- **Stone abutment (hashi-dai no ishigaki)**: dry-stone bridge ends standing alone after the deck is gone. River,
  occasional, medium. Hook: cover.
- **Log flume bridge (kakehi-bashi)**: a wooden water trough on trestles across a ravine, carrying irrigation or mine
  water. Walkable in a pinch. River/mountain, rare, large structure. Hook: water, a crossing (danger). (BL: Civic,
  aqueduct bridge; rural agent owns the farm version)
- **Rafted river crossing (ikada-watashi)**: a log raft poled across by locals where there's no ferry. River,
  occasional, medium. Hook: crossing. (assumed)

== 5. Wayside religious stones and figures ==

- **Roadside Jizō (michi no Jizō)**: a stone Jizō with a red bib and cap, an offering stone, flowers and coins; the
  travellers' guardian. Roadside, common, small prop. Hook: landmark, lore, small offerings (coins: Stephen decides on
  loot). (BL: Buddhist, roadside) [WC §2.5, T35]
- **Jizō hut (Jizō-dō)**: a waist-to-head-high roofed box or tiny open hall sheltering a Jizō. Roadside, occasional,
  small prop/medium. Hook: a tiny rain shelter, landmark.
- **Six-Jizō row (roku Jizō)**: six figures in a row at a village edge, crossroads or graveyard entrance, one for each
  realm of rebirth. Roadside, occasional, medium. Hook: a tell that a village or graveyard is near. (BL: Buddhist props)
- **Pass-top Jizō (tōge no Jizō)**: a bigger Jizō at a pass summit, often with piled stones and hung sandals. Mountain,
  occasional, small prop. Hook: navigation (the summit), lore.
- **Couple dōsojin (sōtai dōsojin)**: a carved man and woman, arm in arm, at a village boundary or crossroads, guarding
  against disease and evil and blessing marriage. Densest in Shinano (Azumino) and Sagami/Kōzuke. Roadside, occasional,
  small prop. Hook: a village boundary means a village is near. Many are late Edo, some 18th c. [Wikipedia: Dōsojin]
- **Inscribed dōsojin (moji dōsojin)**: a natural stone with just the word dōsojin carved on it. Roadside, occasional,
  small prop. Hook: as above.
- **Round-stone dōsojin (maru-ishi dōsojin)**: river-rounded stones heaped on a plinth as the road god. A Kai
  (Yamanashi) type, next to the Fuji/Hakone region. Roadside, occasional, small prop. Hook: boundary, lore. (verify the
  period)
- **Phallic boundary stone (yōseki / seki-bō)**: a natural or carved phallic stone at a crossroads or village edge for
  fertility and protection. Roadside, occasional, small prop. Hook: lore.
- **Kōshin stone (kōshin-tō)**: a square pillar with the blue-faced Shōmen Kongō, the three monkeys and cocks. Put up by
  kōshin-kō groups after their 60-day all-night vigils. The oldest dated one is 1664; they were mostly erected up to ~1800,
  so our window is the peak. Roadside, common, small prop. Hook: landmark. [Inagi city; Wikipedia: Kōshin]
- **Kōshin mound (kōshin-zuka)**: a low earth mound with a kōshin stone on top, often at a crossroads. Roadside,
  occasional, medium `[terrain]`. Hook: landmark, a small rise to see from.
- **Horse-head Kannon (batō Kannon)**: a stone to the horse-headed Kannon, put up where packhorses died or on dangerous
  pack roads. Stone ones start mid-Edo; common in the east; many on the Nakasendō. Roadside/mountain, common in the east,
  small prop. Hook: a DANGER tell (steep or deadly stretch ahead). (BL: Buddhist props) [MFA Boston; Tsukublog]
- **Horse grave (uma-zuka / uma no haka)**: a small mound or stone for a particular horse, by the road where it fell or
  near the owner's village. Roadside, occasional, small prop. Hook: danger tell, lore.
- **Ox mound (ushi-zuka)**: the same for pack oxen on the ox roads. Mountain, rare, small prop. Hook: lore. (assumed)
- **Moon-waiting stone (tsukimachi-tō: nijūsan-ya / jūkyū-ya)**: a stone put up by women's or village kō who stayed up
  for the moonrise on set nights. Roadside, occasional, small prop. Hook: landmark. (verify the date peak; BL lists the
  23rd-night stone)
- **Sun-waiting stone (himachi-tō)**: the same for the sunrise vigil. Roadside, rare, small prop. (verify)
- **Nenbutsu stone (nenbutsu-tō / myōgō-hi)**: "Namu Amida Butsu" carved large, put up by a nenbutsu kō, often counting
  a million recitations. Roadside, occasional, small prop/medium. Hook: landmark.
- **Daimoku stone (daimoku-tō)**: "Namu Myōhō Renge Kyō" in bold Nichiren-style script. On roads near Nichiren temples,
  and at execution grounds as a memorial. Roadside, occasional, medium. Hook: landmark. (verify the Suzugamori date)
- **Hōkyōin-tō pagoda (hōkyōin-tō)**: a stepped stone pagoda with horned corners at a crossroads, hilltop or grave.
  Medieval, with an Edo revival. Roadside/mountain, occasional, medium. Hook: landmark.
- **Sutra mound (kyōzuka)**: a mound over buried sutras. The Heian ones held bronze tubes. Edo ones are often
  "one-stone-one-character" (ichiji-isseki-kyō) mounds with a stone marker on top. Roadside/mountain, occasional, medium
  `[terrain]`. Hook: landmark, digging (Stephen decides whether it's diggable). (verify the Edo frequency)
- **Hill-circuit Kannon (utsushi reijō / sanjūsan Kannon)**: 33 (Saigoku copy) or 88 (Shikoku copy) small stone Kannon
  or Kōbō figures spaced along a hill path, so locals could "do" the pilgrimage in a day. Mountain/forest, occasional (a
  set of small props along a path). Hook: a line of statues leads up a hill (navigation). (verify: the boom was 18th c,
  some later)
- **Stone Buddha, generic (sekibutsu)**: an Amida, Kannon, Yakushi or Dainichi figure alone by the road or under a tree.
  Roadside, common, small prop. Hook: landmark.
- **Fudō stone (Fudō Myōō)**: the fierce Fudō with sword and rope, at waterfalls, springs and steep places. Mountain/
  river, occasional, small prop. Hook: a tell for water or a falls nearby.
- **Water-god stone (suijin-hi)**: a stone to the water kami at a spring, weir or riverbank. River, occasional, small
  prop. Hook: a WATER tell. (BL: Shinto, mountain/water tell)
- **Mountain-god stone or hokora (yama no kami)**: the forest workers' deity. A stone or tiny shrine at the forest edge
  or a charcoal area, with offered sickles and axes. Forest/mountain, common in mountains, small prop. Hook: a tell that
  forest work is nearby; loot (an offered axe or sickle, Stephen decides). (BL: Shinto props)
- **Roadside micro-shrine (hokora)**: a tiny wooden or stone shrine house on a stone base at a field corner, tree root,
  spring or pass. Roadside/forest, common, small prop. Hook: landmark. (BL: Shinto, micro-shrine)
- **Wild Inari shrine (no-Inari)**: a hokora with fox figures and a small red torii in the woods or at a field edge.
  Forest/roadside, occasional, small prop. Hook: landmark.
- **Lone torii in the forest (mori no torii)**: a single wooden or stone torii where a path enters sacred ground. A
  hokora or rock lies beyond. Forest/mountain, occasional, medium. Hook: NAVIGATION (a shrine ahead), landmark.
- **Trailhead lantern pair (tozan-guchi tōrō)**: two stone lanterns where a mountain or shrine path leaves the road.
  Roadside/mountain, occasional, medium. Hook: navigation (a path start).
- **Banner-pole socket stones (nobori-tate ishi)**: paired stones with square sockets for festival banner poles at a
  path start. Roadside, occasional, small prop. Hook: navigation.
- **Crossroads chapel (tsuji-dō)**: a tiny open-fronted hall at a lonely crossroads holding a statue, no bigger than a
  shed. Roadside, occasional, medium. Hook: SHELTER (small), landmark. (If Stephen wants an interior, it moves to BL.)
- **Wooden grave tablet at a death spot (sotoba)**: a notched wooden board planted where someone died on the road.
  Roadside, occasional, small prop. Hook: danger tell, lore.
- **Rough carved Buddhas of a wandering monk (Enkū-butsu)**: axe-hewn wooden Buddhas left in forest halls, tree hollows
  and village shrines by Enkū (d. 1695) in Mino and Hida. Forest, rare, small prop. Hook: lore, a collectible find.
  (BL: Dwellings, wandering carver-monk's hut)

== 6. Mountain religion and pilgrim marks ==

- **Summit or pass shrine (okumiya / tōge no yashiro)**: a stone or board shrine on a peak or pass, the inner sanctuary
  of a lowland shrine. Mountain, rare, medium. Hook: landmark, offerings. (BL: Shinto, summit/pass shrine)
- **Summit windbreak wall (mine no ishigaki)**: a ring of dry-stone walling around a summit shrine or pilgrim hut
  against the wind. Mountain, rare, medium `[terrain]`. Hook: COVER from wind and fire, landmark. (assumed)
- **Offered iron swords at the summit (hōnō tōken)**: iron swords, spear heads and bells left by climbers at summit
  shrines (Tateyama, Hakusan). Mountain, rare, small prop. Hook: loot (iron), lore. (BL: Shinto, summit shrine items)
- **Mountain-path torii (ichi no torii, ni no torii)**: numbered torii marking the stages of a sacred climb. Mountain,
  occasional, medium. Hook: NAVIGATION (progress up the mountain).
- **Horse turn-back point (umagaeshi)**: the spot where riders dismount and the climb continues on foot. Fuji's
  Yoshida trail has a stone torii at ~1,450 m; the name recurs on Nikkō, Haguro and other sacred mountains. Mountain,
  rare, medium. Hook: navigation, landmark, a zone boundary (the sacred climb begins). [JNTO; Fuji Yoshida trail]
- **Women's limit stone (nyonin kekkai-seki)**: a stone marking where women must turn back on a sacred mountain. The
  Ōmine and Kōya bans are the famous ones; Fuji allowed women only to the lower stations. Mountain, rare, small prop.
  Hook: lore, landmark. (BL: Buddhist, nyonin-dō)
- **Pilgrim-club stone (kō-hi / Fuji-kō hi)**: stones put up by confraternities along their route: Fuji-kō, Ōyama-kō,
  later Ontake-kō. Fuji-kō spread after the ascetic Jikigyō Miroku fasted to death on Fuji in 1733 (in window).
  Roadside/mountain, occasional, small prop. Hook: NAVIGATION (the pilgrim trail to a peak). [Tokyo Weekender Fujikō;
  Wikipedia: Fujikō] Ontake-kō `[outside 1680-1750: lay climbing opened 1785+]`
- **Ōyama pilgrimage stones (Ōyama-michi hyō)**: "Ōyama road" direction stones and Fudō figures leading to Sagami's
  Ōyama (Afuri shrine and Fudō temple), a hugely popular Edo pilgrimage in the Hakone/Sagami area. Roadside, occasional,
  small prop. Hook: navigation. (verify: the Ōyama-mairi boom may be mostly after 1750)
- **Waterfall ascetic site (taki-gyōba)**: a shimenawa across the fall, a Fudō figure, a standing stone in the plunge
  pool and a changing hut. Mountain/river, rare, medium. Hook: WATER, landmark. (BL: Buddhist, waterfall practice site)
- **Ascetic practice rocks (gyōba-iwa / nozoki)**: Shugendō test spots: cliff edges where novices are hung over the
  drop (Ōmine's Nishi-no-nozoki), rock clefts to squeeze through, balancing rocks. Mountain, rare, `[terrain]`. Hook:
  danger (fall), landmark. `[off-map: Ōmine]` for the famous one; generic ones on any Shugendō peak (assumed)
- **Rebirth lava cave (tainai / tainai-kuguri)**: lava-tube caves on Fuji's flanks that pilgrims crawled through as a
  "womb", with a small shrine inside (Funatsu tainai, Yoshida tainai). Mountain/forest, rare, `[terrain]`. Hook:
  SHELTER, darkness, landmark. (verify the discovery dates; Funatsu is traditionally late 17th c)
- **Cave shrine (iwaya)**: a natural cave with a shrine or Buddha inside. Enoshima's Iwaya (Benzaiten) was a big Edo
  pilgrimage near Kamakura. Mountain/coast, rare (landmark at Enoshima), `[terrain]`. Hook: SHELTER, landmark. (BL:
  Buddhist, cave halls)
- **Cliff Buddhas (magaibutsu)**: Buddhas carved in relief on a rock face. The landmark is Moto-Hakone, on the old road
  by Shōjin pond:
  - Rokudō Jizō, 3.5 m, 1299
  - three Hitaki Jizō, 1311
  - 25 bodhisattvas split by the road
  The area was seen as "hell" for its volcanic ground. Mountain/roadside, landmark (small ones rare), large structure.
  Hook: LANDMARK on the Hakone map, lore. [Wikipedia: Moto-Hakone Stone Buddhas]
- **Medieval stone-pagoda group (sekitō-gun)**: the tall hōkyōin-tō and gorintō beside the Moto-Hakone Buddhas,
  traditionally the graves of Tada Mitsunaka and of the Soga brothers and Tora. Roadside, landmark, medium each. Hook:
  landmark. [Hakone Japan: Stone Buddhist Sculptures]
- **Riverbank of souls (sai no kawara)**: a desolate shore or volcanic flat covered in small stone stacks for dead
  children, with Jizō. Hakone has one by Lake Ashi near Moto-Hakone; Osorezan is the famous one. Mountain/lake, rare,
  `[terrain]` + props. Hook: an EERIE landmark. Osorezan `[off-map: Tōhoku]`.
- **Hell-valley warning and Jizō (jigoku-dani)**: Jizō, a stone warning and sometimes a rope line at volcanic vents.
  Hakone's Ōwakudani was called Ōjigoku ("great hell") until 1873. Mountain, rare, small props at a nature site. Hook:
  DANGER (gas), landmark. (the vent itself belongs to the nature agent)
- **Pass offering heap (tamuke)**: a pile of stones, twigs or sandals at a pass, each traveller adding one for a safe
  crossing. Mountain, occasional, small prop. Hook: lore, navigation (the summit).
- **Summit cairn (sanchō no ishizumi)**: a stone pile at a peak, sometimes with a small figure on it. Mountain,
  occasional, small prop. Hook: navigation.
- **Fire-ritual hearth (goma-dan / saitō-ba)**: a stone-edged hearth in a clearing where yamabushi burn prayer sticks.
  Mountain, rare, medium. Hook: FIRE, landmark. (assumed placement)
- **"No meat or wine" stone (kaidan-seki / kinsei-hi)**: "Leeks and wine may not enter the gate", at a path to a
  mountain temple. Mountain, occasional, small prop. Hook: navigation (a temple ahead).
- **Kumano subsidiary shrine sites (ōji / ōji-ato)**: the waystation shrines of the Kumano routes, many ruined by Edo
  and marked by a stone or a tiny hokora. Mountain, occasional, small prop. Hook: navigation. `[off-map: Kii]`
- **Pilgrim huts (murodō / tsuya-dō)**: *cross-reference, not counted*. They have interiors: BL, Buddhist roadside.

== 7. Sacred rocks, trees and waters ==

- **Sacred rock with shimenawa (iwakura / shinseki)**: a boulder or outcrop roped as a kami seat, sometimes with shide
  and a tiny offering shelf. Forest/mountain, occasional, medium/large. Hook: LANDMARK, cover. (BL: Shinto props)
- **Wedded rocks (meoto-iwa)**: two rocks joined by a heavy rope. Futami (Ise coast) is the landmark; small inland pairs
  exist too. Coast/mountain, rare (landmark), large. Hook: landmark. Futami `[off-map: Ise]`.
- **Sacred tree with shimenawa (shinboku / goshinboku)**: a huge cedar, camphor or ginkgo roped and left uncut, often
  with a hokora at its foot. Forest/roadside, occasional, large. Hook: LANDMARK (visible), cover.
- **Uncut god tree on a felled slope (yama no kami no ki / tome-ki)**: one tree deliberately left standing on a
  cut-over slope as the mountain god's seat. Forest, occasional, large. Hook: a landmark on bare ground. (assumed)
- **Cursing nails in a sacred tree (ushi no toki mairi no ato)**: a straw doll pinned with five-inch nails to a sacred
  tree, from the Edo "hour of the ox" curse (associated with Kifune, Kyoto). Forest, rare, small prop. Hook: EERIE find,
  a nail (loot), lore. [Wikipedia: Ushi no toki mairi]
- **Sacred spring (reisen / meisui)**: a spring roped with shimenawa, with a stone basin and ladle, often at a shrine
  in the woods. Forest/mountain, occasional, small prop. Hook: WATER, landmark.
- **Mountain pond with an islet shrine (Benten-jima)**: a small shrine on an islet in a forest pond, reached by stepping
  stones or a plank. Forest, rare, medium. Hook: landmark, water. (BL: Shinto props, sacred pond)
- **Footprint or hoof stone (ashiato-ishi)**: a rock with a hollow said to be a hero's footprint, a god's hoof mark or a
  tengu's. Roadside/mountain, occasional, small prop. Hook: lore.
- **Strength stones by the road (chikara-ishi)**: heavy round stones that porters and youths lifted in contests, some
  with legend names (Benkei's). Roadside, occasional, small prop. Hook: lore. (shrine versions: rural agent)
- **Night-crying stone (yonaki-ishi)**: the Sayo-no-Nakayama stone on the Tōkaidō between Kanaya and Nissaka. A
  legend has it crying at night for a murdered mother; Hiroshige shows it sitting in the road. Roadside, landmark,
  medium. Hook: LANDMARK, lore.
- **Killing stone and gas vent fence (sesshō-seki)**: a rock at volcanic vents, fenced by stones or rope. The Nasu stone
  is tied to the nine-tailed fox; the name was used for gassy vents generally. Mountain, rare, small prop + fence. Hook:
  DANGER (gas), lore. Nasu `[off-map: Nasu]`. [Wikipedia: Sesshō-seki]
- **Rope across a waterfall or gorge (taki no shimenawa)**: a shimenawa spanning a falls or a narrow gorge mouth,
  marking sacred water. Mountain/river, rare, medium. Hook: landmark.
- **Offering shelf at a big rock (iwa no sonae-dana)**: a plank shelf pinned to a boulder with sake cups and salt.
  Forest, occasional, small prop. Hook: lore. (assumed)

== 8. Forest work: charcoal, timber, wood ==

- **Black-charcoal kiln (kuro-zumi-gama)**: an earth-dome kiln with a flue, cut into a hillside, smothered to cool.
  Forest, occasional, medium. Hook: WARMTH, a smoke column seen from afar (navigation), charcoal. (BL: Rural industry;
  the hut is in BL Dwellings)
- **White-charcoal kiln (shiro-zumi-gama / binchō)**: a stone and clay kiln whose charcoal is raked out red-hot into a
  sand-and-ash pit. Kishū binchō dates from the Genroku era. Forest, rare, medium. Hook: warmth, a burn danger at the
  quench pit. (BL: Rural industry)
- **Charcoal-kiln ruin (sumigama-ato)**: a round pit with a slumped rim, charred earth and a flue gap. Kilns moved with
  the wood supply, so old pits dot every worked forest. Forest, common, `[terrain]`. Hook: cover, a tell of past work.
- **Pit-burn charcoal site (fuse-yaki / ana-yaki)**: a simpler trench burn under earth and turf. Forest, occasional,
  `[terrain]`. Hook: warmth, fire. (assumed)
- **Charcoal bales waiting at a trailhead (sumi-dawara no tsumi)**: straw-wrapped charcoal bales stacked at a track
  end for porters or horses. Forest/roadside, occasional, small prop. Hook: LOOT (fuel).
- **Firewood stacks (maki-zumi / takigi-zumi)**: split wood stacked to dry among the trees. Forest, common, small prop.
  Hook: fuel.
- **Kiln-wood cutting heaps (gen-boku)**: short oak and konara logs cut to kiln length, stacked by a kiln. Forest,
  occasional, small prop. Hook: fuel. (assumed)
- **Branded stump or log end (gokuin / kokuin)**: stumps and log ends stamped with the owner's hammer brand (domain or
  shogunate), proof that a felling was licensed. Forest/river, occasional, small prop. Hook: a tell that you're in an
  official forest (see §13).
- **Log deck at a landing (bōzumi / doba)**: a stack of felled logs at a river landing or chute foot waiting to go down.
  Forest/river, occasional, medium. Hook: COVER, climbable.
- **Timber chute (shura)**: logs laid lengthwise down a slope as a trough for skidding timber, sometimes wetted. Forest/
  mountain, occasional, large `[terrain]`. Hook: DANGER (a running log), fast descent, landmark. (BL: logging camp) [the
  Kiso forestry picture scroll of 1854 depicts it; the method is older]
- **Sledge track (kinma-michi)**: log crossties laid like a ladder track on which timber sledges (kinma) were hauled
  down. Forest, occasional, `[terrain]`. Hook: navigation (a track). (verify that kinma was in use before 1750)
- **Log flush dam (teppō-zeki)**: a timber dam across a mountain stream, filled then released to flush logs down in a
  surge. Forest/river, rare, large structure. Hook: DANGER (the release), a crossing on top, landmark. (verify the Edo
  date)
- **Loose log drive (kuda-nagashi)**: logs floated singly down a river at high water before rafting. River, occasional
  (seasonal), small props on the water. Hook: danger (a crush), a crossing hazard.
- **Log-catching boom (tsuna-ba / ami-ba)**: a rope or log boom across a river where loose logs were caught and bound
  into rafts. Owari's Kiso timber was caught at Nishikori. River, rare (landmark on the Kiso), large structure. Hook:
  crossing, landmark. (verify Nishikori)
- **Moored log raft (ikada)**: logs bound with rope and vines, moored at a bank with poles aboard. River, occasional,
  medium. Hook: river travel, a crossing. (BL: timber rafting station)
- **Sawpit and whipsaw trestle (kobiki-ba)**: a sloped log trestle where two sawyers ripped planks with the big ōga
  frame saw. Forest, occasional, medium. Hook: loot (a saw, wedges). (BL: logging camp)
- **Shingle-splitting site (hegi-ita tsukuri-ba)**: sawara or hinoki bolts split into roof shingles, with shavings and
  bundles. Forest, occasional, small prop. Hook: none (dressing). (assumed as a forest site)
- **Bark-stripped cypress (hiwada-muki no ki)**: hinoki with the outer bark peeled in sheets for bark roofing (hiwada).
  Done without killing the tree. Forest, occasional, small prop (a tree decal). Hook: a tell.
- **Wood-turners' workings (kiji-shi no ato)**: bowl blanks, shavings and pole-lathe pits in beech forest, left by
  itinerant turners. Forest, rare, small prop. Hook: loot (bowls). (BL: Dwellings, wood-turner's forest hut)
- **Clear-cut bare slope (hage-yama)**: a hillside stripped for fuel and timber, eroding. Common in Edo western Japan.
  Mountain, occasional, `[terrain]`. Hook: open ground, landslide danger, a long view. (Totman, *The Green
  Archipelago*, verify detail)
- **Planted cedar stand (sugi no ue-bayashi)**: close-planted cedar rows. Yoshino planting was well under way by 1700.
  Forest, occasional, `[terrain]`. Hook: cover, dark forest. Yoshino `[off-map: Yoshino]`; planting spread elsewhere
  (verify).
- **Slash-and-burn plot (yakihata)**: a burned slope with charred stumps and millet or buckwheat, far from the village.
  Mountain, occasional, `[terrain]`. Hook: open ground, food. (BL: Dwellings, yakihata huts; the rural agent owns the
  field)
- **Shiitake log stack (shiitake hodagi)**: oak logs slashed with a hatchet (nata-me method) and leaned in a damp gully
  so spores settle and mushrooms grow. Forest, occasional, small prop. Hook: FOOD. Izu Amagi and Bungo are the centres.
  (verify the date in Izu)
- **Timber sledge left on a track (sori / kinma)**: a wooden hauling sledge left at a slope foot. Forest, occasional,
  small prop. Hook: loot (wood), dressing.
- **Felling notch and wedges in a half-felled tree (kirikake)**: a tree abandoned mid-cut with wedges still in, a sign
  of a crew that left in a hurry. Forest, rare, small prop. Hook: loot (wedges), danger (a fall). (assumed)

== 9. Hunting, trapping and river fishing ==

*Cross-reference, not counted: the hunter's hut (ryōshi-goya / matagi-goya) is BL, Dwellings / Rural industry.*

- **Ground blind at a game trail (machi-ba / tachi-ma)**: a brush screen or rock blind where a gunner waits during a
  drive hunt (makigari) as beaters push game along. Forest/mountain, occasional, small prop. Hook: COVER, a sniping
  position. (assumed; *tatsu-ma* is the Matagi term)
- **Tree perch (ki no ue no machi-ba)**: a plank or crotch seat lashed in a tree over a trail or crop edge. It's the
  closest analogue to Chernarus hunting stands. Forest, rare, small prop. Hook: a high vantage, cover. (assumed; may be
  anachronistic as a built stand, so flag for Stephen)
- **Pit trap (otoshi-ana / shishi-ana)**: a covered pit for boar or deer, often along a boar wall, sometimes with
  stakes. Forest, occasional, `[terrain]`. Hook: DANGER (fall), a trap. (verify stakes)
- **Deadfall (osa / hira-otoshi)**: a heavy log or flat stone propped on a trigger stick over bait. Forest, occasional,
  small prop. Hook: DANGER, food.
- **Spring snare (hane-wana / kukuri-wana)**: a noose on a bent sapling set on a runway. Forest, common, small prop.
  Hook: DANGER (the leg), food.
- **Bird-lime rods (tori-mochi zao)**: rods smeared with lime, used by bird-catchers (tori-sashi) for small birds, left
  propped in bushes. Forest, occasional, small prop. Hook: food, lore.
- **Ridge mist-net (kasumi-ami)**: fine nets strung across a ridge saddle to catch migrating thrushes in autumn (Hida,
  Mino). Mountain, rare, medium. Hook: food, a tangle hazard. (verify the date)
- **Duck-netting pond (sakaami / kamo-ba)**: a pond edge with a bank and hide where hunters throw Y-framed nets at
  rising ducks. Kaga's sakaami is said to date from the Genroku era. River/forest, rare, medium. Hook: food. Kaga
  `[off-map: Kaga]`. (verify)
- **Boar wall (shishigaki)**: dry-stone or earth walls, kilometres long, between forest and fields. Mostly 18th–19th c;
  Shōdoshima's was ~120 km by 1790. Forest edge, occasional, large `[terrain]` (linear). Hook: NAVIGATION (follow it to
  a village), cover. (the rural agent may also claim it) [Stone Islands of Setouchi; Mt Hira study]
- **Boar ditch (shishi-bori)**: a trench and bank version where stone is scarce. Forest edge, occasional, `[terrain]`.
  Hook: cover, a fall hazard. (assumed)
- **Game fence of brush and stakes (shika-gaki)**: a woven brush fence around distant fields against deer. Forest
  edge, occasional, `[terrain]`. Hook: cover. (assumed; the rural agent overlaps)
- **Scare clapper line (naruko)**: wooden clappers on a cord pulled from a watch hut, or rattled by the wind. Forest
  edge, occasional, small prop. Hook: SOUND (an alarm if touched?). (the rural agent overlaps)
- **Shogun's hunt field (kariba / shishigari-ba)**: open grass or pasture ground with earthworks and stands used for
  great drive hunts. Yoshimune's Koganehara hunts were in the 1720s. Forest/plain, landmark, `[terrain]`. Hook:
  landmark, open ground. (verify the dates) `[off-map: Shimōsa]`
- **Bear or boar memorial (kuma-zuka / kemono kuyō-tō)**: a stone put up by hunters for the animals they killed.
  Mountain, occasional, small prop. Hook: a tell of a hunting area, lore.
- **Skinning and drying frame (kawa-hoshi-waku)**: a pole frame with a stretched hide by a stream, far from the village.
  Forest, rare, small prop. Hook: loot (hide), a danger tell (predators). (BL: rawhide yard is the town version)
- **Fish weir (yana)**: a bamboo-slat ramp across a river that strands descending ayu and eels, with a watch hut. River,
  occasional, large structure. Hook: FOOD, a crossing. (BL: Rural industry)
- **Basket fish trap (uke / dō / mondori)**: cone-mouthed bamboo traps weighted in streams. River, common, small prop.
  Hook: FOOD.
- **Eel tube (unagi-zutsu / takappo)**: bamboo tubes sunk in the mud for eels. River, common, small prop. Hook: FOOD.
- **Stone fish-drive channel (ishi-yose)**: stone arms piled in a stream funnelling fish into a trap or shallow. River,
  occasional, `[terrain]`. Hook: food. (assumed)
- **Stake-lattice weir (ajiro)**: the ancient Uji and Tanakami stake weirs for ice-fish (hio). River, rare, large.
  Hook: lore. (verify: largely medieval) `[outside 1680-1750: mostly medieval]`
- **Night-fishing torch baskets (kagari)**: iron fire baskets on poles at a river bend or on boats for night fishing.
  River, occasional, small prop. Hook: FIRE, light. (BL: cormorant-fishing house)
- **Fishing platform over a pool (tsuri-dai)**: a plank shelf pegged over a deep pool. River, occasional, small prop.
  Hook: food. (assumed)
- **Hunting-licence post (teppō aratame no fuda)**: a board at a village edge naming the licensed hunters' guns under the
  1687 registration. It's the rural face of Tsunayoshi's controls. Roadside, rare, small prop. Hook: lore. (assumed
  form; the registration is in BL)

== 10. Mining, quarrying, digging, hot springs ==

- **Mine adit (mabu)**: a timber-framed tunnel mouth with a spoil heap and a drainage trickle. Mountain, rare, medium.
  Hook: SHELTER, darkness, collapse DANGER, loot spot. (BL: Rural industry, mines)
- **Hand-dug prospect burrows (tanuki-bori)**: narrow twisting tunnels following a vein, "badger-dug". Typical of early
  Edo gold workings. Mountain, occasional, small prop (a hole) + `[terrain]`. Hook: danger (a squeeze, a collapse),
  shelter. (verify the term)
- **Open-cut split mountain (rotenbori / wareto)**: a hilltop split open by surface mining. Sado's Dōyū no Wareto is
  the landmark. Mountain, rare, `[terrain]`. Hook: LANDMARK, a fall danger. `[off-map: Sado]`
- **Mine spoil heap (zuri / ha-ishi yama)**: waste-rock heaps below the adits. Mountain, occasional, `[terrain]`. Hook:
  cover, a tell of a mine.
- **Abandoned mine (haikō / kyūkō)**: a collapsed adit with rotten props, a flooded shaft and rusted tools. Many Izu
  workings were past their peak by 1730. Mountain, rare, medium. Hook: SHELTER, DANGER, LOOT. (Toi gold mine was in
  use; verify which were closed)
- **Mine drainage outlet (mizunuki-kō)**: a low tunnel mouth spilling orange mine water into a stream. Mountain, rare,
  small prop. Hook: bad WATER (danger). (assumed)
- **Placer gold workings (sakin-tori-ba)**: riverbank gravels dug over and washed for gold dust. Kai's gold streams are
  famous from the Takeda era. River, rare, `[terrain]`. Hook: loot (panning?). (verify how active in 1730)
- **Castle-stone quarry (ishi-chōba)**: hillside and shore quarries in Izu (Atami, Itō; 170 sites) that cut stone for
  Edo Castle's walls in the early 1600s. Abandoned by 1730. Mountain/coast, landmark (near the Hakone map), `[terrain]`
  + large props. Hook: LANDMARK, cover among the blocks. [Wikipedia: Stone Quarries for Edo Castle]
- **Abandoned marked block (kokuin-ishi / "zannen-ishi")**: a huge dressed block left behind, with its daimyō's crest
  cut on it and a line of wedge holes. Mountain/coast, occasional (in Izu), medium. Hook: cover, lore. (verify the name
  *zannen-ishi*)
- **Stone-loading point (ishi-dashi-ba)**: a rough ramp or stone jetty on the Izu coast where quarry blocks went onto
  barges. Coast, rare, `[terrain]`. Hook: landmark. (assumed form)
- **Whetstone or millstone quarry (toishi-yama / usu-ishi chōba)**: small quarries for whetstones (Kyoto's Narutaki)
  or millstones. Mountain, occasional, `[terrain]`. Hook: loot (a whetstone). (verify locations)
- **Clay pit (tsuchi-tori-ba)**: a dug-out bank for tile or pottery clay. Forest edge, occasional, `[terrain]`. Hook:
  cover.
- **Old kiln ruin and shard heap (koyō-ato / monohara)**: a collapsed medieval tunnel kiln on a hillside, with drifts of
  broken pots (Seto, Tokoname, Shigaraki areas). Forest/mountain, rare, `[terrain]`. Hook: lore, shards (loot?).
- **Sulphur workings (iō-tori-ba)**: yellow crust dug at vents, with baskets and a melting pot. Mountain, rare, small
  props at a nature site. Hook: DANGER (gas). (BL: Rural industry, sulphur; verify Ōwakudani in 1730)
- **Hot-spring source troughs (yumoto no toi)**: wooden gutters and bamboo pipes carrying hot water from a vent down to
  bath huts. The Hakone Nanayu (seven hot springs) are next to our map. Mountain, rare, medium. Hook: WARMTH (see
  Stephen's hot-spring request). (BL: Services, hot-spring baths)
- **Wild riverside hot pool (kawa-yu / nozura-buro)**: a stone-dammed pool at a riverside hot spring, used by locals,
  hunters and animals, with no building. River/mountain, rare, `[terrain]`. Hook: WARMTH, healing, landmark. (assumed;
  period form to verify, per WC "Additions")
- **Hot-spring steaming ground (yu-no-hana tori)**: a flat of vents where "hot-spring flowers" (mineral crust) were
  harvested under thatch covers. Mountain, rare, medium. Hook: warmth, danger. (verify: the Beppu and Kusatsu dates are
  18th c)
- **Ice pit (himuro)**: a stone-lined pit with a thatched roof in a cool hollow. Winter ice was stored for summer, and
  Kaga sent ice to the shogun each 6th month. Mountain/forest, rare, medium. Hook: lore, cold. Kaga `[off-map: Kaga]`;
  generic ones elsewhere (verify).

== 11. Mountain produce ==

- **Log beehive (hachi-dō)**: a hollow sugi or hinoki log (~70 cm) stood on a stone, under an overhang or by a shrine,
  for Japanese honeybees. Kishū (Kumano) was the famous honey country. Forest/mountain, occasional, small prop. Hook:
  FOOD (honey), mild danger (stings). [*Nihon sankai meisan zue* 1799 depicts it `[outside]`; the practice is earlier]
- **Cliff hive row (iwa-dō)**: a row of box or log hives set on a rock ledge under an overhang. Mountain, rare, medium.
  Hook: food, a climbing hazard. (assumed from the Kumano practice)
- **Lacquer tree with tapping scars (urushi no ki)**: a lacquer tree with rows of horizontal knife cuts where the sap
  was collected in summer. Forest edge, occasional, small prop (a tree decal). Hook: DANGER (lacquer rash if touched), a
  tell. (BL: lacquer tapper)
- **Tapper's sap tub on a tree (urushi-oke)**: a small wooden cup or tub hung at a scored lacquer tree. Forest, rare,
  small prop. Hook: loot (lacquer), danger (rash). (assumed)
- **Resin-tapped pine (matsu-yani)**: pine with V-scars for resin or cut-out fatwood for torches (taimatsu). Forest,
  occasional, small prop. Hook: FIRE (torch material). (assumed for the period)
- **Famine root-digging ground (warabi-ne hori-ba)**: a slope pocked with holes where bracken and kudzu roots were dug
  for starch in hunger years (Kyōhō famine 1732). Mountain, occasional, `[terrain]`. Hook: food (poor), a tell of
  hardship. (verify the extent)
- **Nut-gathering claim marks (tochi / kuri no shime)**: straw knots tied to horse-chestnut or chestnut trees, claiming
  the harvest for a household. Forest, occasional, small prop. Hook: food. (assumed; see §13 claim stakes)
- **Wild-grass cutting ground (kaya-ba / kari-shiki-ba)**: a thatch-grass or green-manure slope kept open by cutting and
  burning, with bundle stacks. Mountain, occasional, `[terrain]`. Hook: open ground, fire danger. (the rural/nature
  agents overlap)
- **Medicinal-herb garden in the hills (yakuen / yakusō-bata)**: a domain or shogunal herb plot in the hills, fenced and
  signed. Yoshimune pushed native herb cultivation in the 1720s. Mountain, rare, medium `[terrain]`. Hook: FOOD/medicine
  loot, landmark. (verify; Komaba and Koishikawa are urban)

== 12. River and slope works ==

- **Crib spur dike (seigyū)**: a triangular timber pyramid (about 6 × 4 m) set in a river and weighted with stone-filled
  bamboo gabions, to push the current off a bank. River, occasional, large structure. Hook: cover, a crossing hazard.
  [ScienceDirect, *Seigyu* study]
- **Bamboo gabion (jakago)**: long bamboo "snake baskets" packed with river stones, laid along banks. River, common,
  medium. Hook: cover.
- **Open staggered levee (kasumi-tei)**: overlapping levee sections with gaps that let floods back-flow and drain. The
  "Shingen-zutsumi" on the Kamanashi is the model. River, occasional, `[terrain]`. Hook: cover, navigation. (verify)
- **Groyne (dashi / hane)**: a stone or pile spur jutting from a bank. River, occasional, medium. Hook: cover, fishing
  spot.
- **Great embankment with a founder's shrine (Bunmei-zutsumi)**: Sakawa River bank near Odawara, rebuilt by Tanaka
  Kyūgu and finished in 1726 after 1707 Fuji ash choked the river and floods broke the old bank (1711). It has a shrine
  to Yu the Great (Bunmei). River, landmark (near the Hakone map), large `[terrain]`. Hook: LANDMARK, a raised path.
  [Kanagawa trip; Hakone Geopark]
- **Aqueduct tunnel through a crater rim (Hakone yōsui / Fukara yōsui)**: a ~1.3 km hand-dug tunnel carrying Lake Ashi
  water through the western rim to the Fukara fields (Susono), 1666–70. The intake and outlet are in the wild. Mountain,
  landmark (Hakone map), medium `[terrain]`. Hook: WATER, a tunnel (crawlable?), landmark. (verify the length)
- **Stone diversion weir (seki / iseki)**: stone and timber across a river feeding an irrigation channel. River,
  occasional, large. Hook: a crossing, water. (BL: Civic, weir)
- **Bamboo-grove bank protection (mizu-bōbi no takeyabu)**: dense bamboo planted along a levee or bank to hold soil in
  floods. River, common, `[terrain]`. Hook: cover. (assumed)
- **Flood-level mark (kōzui-hi / mizu-jirushi)**: a carved line or stone recording a great flood's height. River, rare,
  small prop. Hook: lore, danger tell. (verify for the window)
- **Slope-planting or erosion barrier (sunadome)**: rows of stakes, brush and planted pines on bare slopes, following the
  1666 shogunal order on mountains and rivers against root-digging. Mountain, occasional, `[terrain]`. Hook: cover.
  (verify)
- **Volcanic sand dump heaps (suna-yama / suna-zuka)**: after Fuji's 1707 Hōei eruption, farmers east of Fuji (the
  Mikuriya area, Gotemba) shovelled ash off their fields into heaps and trenches. In 1730 they're still there. Plain/
  foothill, occasional (Fuji region), `[terrain]`. Hook: a unique wasteland look, cover. [Mt Fuji World Heritage Centre]
- **Ash-buried abandoned field (suna-ume no hatake)**: a field left under grey ash with dead stalks and a broken fence.
  Plain, rare, `[terrain]`. Hook: a tell of disaster. (same source)
- **Landslide dam remains (sekitome-ko no ato)**: a debris dam across a valley with the drowned trees of a temporary
  lake, like the ash dams on the Sakawa. River/mountain, rare, `[terrain]`. Hook: danger, landmark. (verify)

== 13. Boundaries, bans and control ==

- **Province boundary post (kokkyō-gui / kokkyō-hi)**: a wooden or stone post reading "From here east: Sagami". Pairs
  face each other across the line. Roadside/mountain, rare, small prop/medium. Hook: NAVIGATION (a province crossing).
  (assumed wording; the posts are well attested)
- **Paired border mounds (sakai-zuka)**: small earth mounds, like mile mounds, on each side of a road at a province or
  domain line. Roadside, rare, medium `[terrain]`. Hook: navigation. (verify)
- **Border ditch between provinces (Nemonogatari no sato)**: on the Nakasendō at Imasu, a ditch only a few feet wide
  split Mino from Ōmi, so people could talk across it lying in bed. Roadside, landmark, small `[terrain]`. Hook: lore,
  landmark. (verify)
- **Domain boundary stake (ryōbun-gui / ryōkai-hi)**: a post naming the domain or the shogunal land. Disputes over the
  line were frequent. Roadside/forest, occasional, small prop. Hook: navigation (whose land).
- **Village boundary stone (mura-zakai ishi)**: a marker stone at a village line, often beside a dōsojin; there were
  many fights over commons (iriai). Roadside/forest, occasional, small prop. Hook: navigation.
- **Village boundary rope (kanjō-nawa / kanjō-kake)**: a rope across the road at the village edge hung with straw
  charms, sandals and wooden tags, to keep epidemics out. Kinki (Wakasa, Shiga, Iga, eastern Nara, southern Yamashiro).
  Roadside, occasional, medium. Hook: a tell that a village is ahead, lore. [Wikipedia: Kanjo Nawa]
- **Straw giant at a village edge (Kashima-sama / Shōki-sama)**: huge straw warrior figures guarding the road into a
  village. Mostly Akita and Echigo. Roadside, rare, medium/large. Hook: an EERIE landmark. `[off-map: Tōhoku / Echigo]`
  (verify the Edo dating)
- **Disease-sending straw doll (okuri-ningyō / hōsō-gami okuri)**: straw dolls, boats and red gohei left at the village
  edge or a riverbank after a rite to send away smallpox or insect pests. Roadside/river, occasional, small prop. Hook:
  eerie, lore. (assumed placement)
- **Forbidden-forest marker (tomeyama / sudome-yama sakai-gui)**: stakes and boards marking a reserved forest. Owari
  banned cutting four Kiso trees in 1708 and a fifth in 1718, under the slogan "one tree, one head". Forest, rare, small
  prop. Hook: DANGER (the law, patrols), prime timber. [Wikipedia: Five Sacred Trees of Kiso]
- **Forest notice board (yama-kōsatsu)**: a roofed board at the forest entrance listing banned trees and penalties.
  Forest, rare, medium. Hook: lore, a danger tell. (assumed form) (a forest-guard hut, if needed, belongs in BL)
- **Reserved-tree mark (tome-ki shirushi)**: a blaze, brand or rope on individual protected trees. Forest, occasional,
  small prop. Hook: a tell. (assumed)
- **Shogun's falconry-ground boundary post (otakaba sakai-gui)**: posts marking the shogun's hawking preserve around
  Edo (~1,600 km², all hunting banned inside). Abolished under Tsunayoshi and restored by Yoshimune in 1716. Bird
  wardens (torimi) patrolled it. Roadside/forest, rare, small prop. Hook: a no-hunting zone, lore. (verify the post
  form) [Japanese Wiki Corpus: Torimi] `[off-map-ish: Edo plain]`
- **"Killing forbidden" stone (sesshō kindan-seki)**: a stone pillar at a temple's river or hill banning fishing and
  hunting. Laws of Compassion era, 1687–1709. River/forest, occasional, small prop. Hook: a no-hunting zone, lore.
  (verify examples)
- **Commons claim stake (shime / shime-gui)**: a stick with a straw knot claiming grass, firewood or mushroom rights on
  common land. Forest, common, small prop. Hook: a tell of village use. (assumed; the *shime* sign is well known)
- **Checkpoint palisade up the slope (sekisho no yarai / sakumono)**: fences and walls running up the hillside from a
  sekisho to block bypasses, as at Hakone (between the lake and the steep ridge). Mountain, rare (landmark at Hakone),
  large `[terrain]` (linear). Hook: a BARRIER, danger (sekisho-yaburi was punishable by death). (verify the Hakone
  extent) (BL: Government, sekisho)
- **Bypass-path warning board (nuke-michi kinshi fuda)**: a notice on a side path warning that evading the checkpoint is
  forbidden. Mountain, rare, small prop. Hook: danger tell, navigation (a bypass exists). (assumed)
- **Remote lookout post of a checkpoint (tōmi-ban)**: *cross-reference, not counted*: BL (Military, coastal lookout;
  sekisho lookout).
- **Domain border checkpoint (kuchi-dome bansho)**: *cross-reference, not counted*: BL, Government.
- **Pole barrier across a road (kari-kido)**: a temporary pole or rope across a road during an inspection, epidemic or
  manhunt. Roadside, rare (event), small prop. Hook: an event barrier. (assumed)
- **Grass-fire firebreak (hi-yoke no kari-michi)**: a mown strip between grassland commons and forest, kept before
  spring burning. Mountain, occasional, `[terrain]`. Hook: navigation, fire. (assumed)
- **Tax-land survey boundary stone (kenchi sakai-ishi)**: a stone set at a field or forest corner after a land survey.
  Forest edge, occasional, small prop. Hook: navigation. (assumed)
- **Hunting-ground notice board (kariba kōsatsu)**: a board at the entrance of a domain hunting preserve. Forest, rare,
  small prop. Hook: danger (a ban). (assumed)
- **Wolf-charm post (ōkami ofuda-gui)**: a post or tree hung with Mitsumine or Ontake wolf talismans against thieves and
  boar, at the field edge. Forest edge, occasional, small prop. Hook: lore. (verify the placement; the charms are Edo)

== 14. Lookouts, beacons and signals ==

- **Beacon hill (noroshi-ba / noroshi-dai)**: a cleared summit with a stone or earth hearth, wood stacks and a hut. The
  17th-c chains ran toward Nagasaki; many coastal chains are 1800s. Mountain/coast, rare, medium. Hook: FIRE, a long
  VIEW, navigation (a summit landmark). (BL: Military, beacon post)
- **Sengoku beacon mound (noroshi-dai ato)**: a levelled earth platform on a peak from Warring States signal chains
  (Takeda, Hōjō). Mountain, occasional, `[terrain]`. Hook: a VIEW point, cover.
- **Open lookout platform (monomi-dai)**: a pole platform or cleared knoll with no hut, on a headland or pass. Mountain/
  coast, rare, medium. Hook: a VIEW point, a sniping spot. (assumed)
- **Weather-watch hill with a direction stone (hiyori-yama / hōi-ishi)**: a hill above a port with a compass-rose stone
  carved with the 12 directions, used by pilots to read the weather. Coast, rare, small prop on a hill. Hook: NAVIGATION
  (a literal compass), view. (BL: Civic, weather-watching hill)
- **Fish-spotting knoll (uomi-dai)**: a clear headland seat where a spotter watched for sardine or yellowtail shoals and
  signalled the boats. Coast, occasional, small prop/`[terrain]`. Hook: view. (BL has the tower version)
- **Whale lookout (kujira yamami)**: headland lookouts of the net-whaling groups. Coast, rare, medium. Hook: view.
  `[off-map: Kii / Kyushu]`
- **Flag-signal relay hill (hata-furi yama)**: hills used to relay Osaka rice prices by flags or mirrors. Mountain,
  rare, small prop. Hook: landmark. (verify: may be after 1750)
- **Harbour guide fire (kagari-bi no ba)**: a stone-ringed fire place or iron basket on a point, lit to guide boats in.
  Coast, occasional, small prop. Hook: FIRE, navigation. (assumed)
- **Sekisho hill lookout**: *cross-reference, not counted*: BL.
- **Survey marker (sokuryō-hyō)**: Inō Tadataka's survey stations and marks. Mountain/coast, rare, small prop. Hook:
  navigation. `[outside 1680-1750: 1800–1816]`
- **Signal bell or drum post at a wild ferry**: see §4 (not counted twice).
- **Mountain-top prayer fire for rain (amagoi-bi)**: a hilltop fire site where villages lit rain-prayer bonfires in
  drought. Mountain, rare, `[terrain]`. Hook: fire, landmark. (verify)
- **Echo or call rock (yobi-iwa)**: a rock from which shepherds and woodsmen called across a valley. Mountain, rare,
  `[terrain]`. Hook: lore. (assumed; cut candidate)

== 15. Ruins: castles, forts, barriers ==

- **Mountain castle ruin (yamashiro-ato)**: Sengoku earthworks along a ridge: terraces, cut moats, earth ramparts,
  overgrown and treed. Mostly abandoned after 1615's one-castle-per-province order. Mountain, occasional, large
  `[terrain]`. Hook: LANDMARK, a defensible position, VIEW, loot spot. [period: 1615 ikkoku ichijō rei]
- **Ridge-cut moat (horikiri)**: a deep trench across a ridge that cuts a castle off from its approach. Mountain,
  occasional, `[terrain]`. Hook: cover, a chokepoint, fall danger.
- **Vertical slope moats (tatebori / unejō tatebori)**: trenches running down a slope, sometimes in rows. Mountain,
  occasional, `[terrain]`. Hook: cover.
- **Earth rampart (dorui)**: a raised earth bank around a castle terrace. Mountain, occasional, `[terrain]`. Hook:
  cover.
- **Castle terraces (kuruwa)**: levelled enclosures stepping down a hill, now grass or forest. Mountain, occasional,
  `[terrain]`. Hook: open camp sites, views.
- **Deliberately broken stone walls (hajō no ishigaki)**: stone walls with their corners pulled down when the castle was
  slighted. Mountain, rare, medium. Hook: cover, landmark.
- **Castle well (jō-ido)**: a stone-lined well on a ruined castle terrace, sometimes still wet. Mountain, rare, small
  prop. Hook: WATER, fall danger.
- **Gate site with foundation stones (koguchi-ato)**: a bent entrance through the ramparts with post stones. Mountain,
  occasional, small `[terrain]`. Hook: cover, navigation.
- **Ridge fortlet (toride-ato)**: a small single-terrace fort or outpost. Mountain, occasional, `[terrain]`. Hook:
  view, cover.
- **Yamanaka Castle ruin (Hakone)**: the Hōjō castle straddling the Tōkaidō on the Hakone pass, taken by Hideyoshi in
  half a day in 1590. Famous for its grid "shōji-bori" moats. Mountain/roadside, LANDMARK (Hakone map), large
  `[terrain]`. Hook: landmark, cover, a chokepoint.
- **One-night castle (Ishigakiyama Ichiya-jō)**: Hideyoshi's 1590 siege castle overlooking Odawara, the first
  stone-walled castle in the Kantō. Mountain, LANDMARK (near Hakone), large `[terrain]`. Hook: landmark, view.
- **Siege-camp earthworks (jin-ato / jinsho-ato)**: banks and terraces of besiegers' camps ringing an old siege site,
  such as the 1590 Odawara ring. Mountain/plain, rare, `[terrain]`. Hook: cover.
- **Ancient barrier site (kosekisho-ato)**: long-abolished classical barriers:
  - Fuwa no seki on the Nakasendō near Sekigahara (673–789), visited by Bashō in 1684
  - Ashigara no seki on the Ashigara pass (899), next to Hakone
  - Suzuka no seki
  Roadside/mountain, rare (landmark), `[terrain]` + a marker. Hook: lore, landmark.
- **Medieval moated residence (yakata-ato / hōkei-yakata)**: a square moat and bank of a Kamakura–Muromachi warrior
  house, now a copse in fields. Forest edge, occasional, `[terrain]`. Hook: cover.
- **Castle-road stone steps (jōdō no ishidan)**: overgrown stone stairs climbing to a castle ruin from the valley.
  Mountain, rare, `[terrain]`. Hook: navigation.
- **Ancient mountain fortress stone wall (kōgoishi / kodai sanjō)**: a 7th-c Korean-style stone ring wall around a
  hill. Mountain, rare, large `[terrain]`. Hook: landmark. `[off-map: western Japan]`
- **Castle ruin memorial shrine (shiro-ato no hokora)**: a hokora or stone on the top terrace for the fallen lord.
  Mountain, occasional, small prop. Hook: landmark.
- **Demolished-castle foundation (tenshu-dai ato)**: an empty keep base of stone on a lowland castle abandoned under the
  1615 order. Plain/hill, rare, medium. Hook: landmark, view.
- **Battlefield field marker (kosenjō no hi)**: a stone or pine marking a famous battle spot (Sekigahara, Okehazama).
  Roadside, rare, small prop. Hook: lore, landmark. (verify which were marked before 1750)

== 16. Ruins: settlements, temples, work sites ==

- **Abandoned hamlet (haison / tsubure-mura)**: collapsed thatched houses, overgrown fields and a dry well. Villages
  were lost to famine (Kyōhō, 1732, in window), landslide, flood and the 1707 ash. Forest/mountain, rare, large. Hook:
  LOOT spot, shelter (partial), landmark.
- **Abandoned farmstead (tsubure-byakushō no ato)**: one fallen house, foundation stones, a bamboo grove and a
  persimmon tree. Forest edge, occasional, medium. Hook: loot, a partial shelter.
- **Terraced fields gone back to forest (arehata)**: stone-walled terraces under young trees. Mountain, occasional,
  `[terrain]`. Hook: cover, navigation (a village was near).
- **Ancient temple foundation stones (haiji-ato / soseki)**: the cornerstones and pagoda base of a Nara-period temple
  (such as the provincial kokubunji) in a field or wood. Plain/forest, occasional, medium. Hook: landmark, lore.
- **Ruined mountain temple (sanrin haiji)**: terraces, toppled stupas, a broken gate base and moss-covered steps of a
  temple burned in the Sengoku wars. Mountain, rare, large `[terrain]`. Hook: landmark, loot spot.
- **Collapsed hermitage (iori-ato)**: a hearth stone, a scatter of tiles or thatch and a spring. Mountain, occasional,
  small. Hook: water, loot.
- **Old well in the woods (furu-ido)**: a stone ring half hidden in undergrowth. Forest, occasional, small prop. Hook:
  WATER, DANGER (fall).
- **Fallen shrine (yashiro-ato)**: a collapsed hokora and a toppled torii in a grove. Forest, occasional, small prop.
  Hook: lore, landmark.
- **Burned hut remains (yake-goya)**: charred posts and a stone hearth. Forest, occasional, small prop. Hook: loot, a
  danger tell.
- **Old ironworks slag heap (kanakuso-yama)**: glassy slag heaps from small bloomeries. Mountain, rare, `[terrain]`.
  Hook: lore. (the big tatara are `[off-map: Chūgoku]`) (assumed elsewhere)
- **Old road station ruin (kyū-shuku ato)**: foundations of a post-station hamlet bypassed when the road moved. Roadside,
  rare, medium. Hook: loot, shelter. (assumed)
- **Abandoned salt works**: see §19 (not counted twice).
- **Abandoned work camp (soma-goya ato)**: a logging-camp clearing with a collapsed long hut, a rusted saw blade and
  sawdust drifts. Forest, occasional, medium. Hook: loot (tools), shelter (partial).
- **Abandoned mountain shrine path (haidō)**: an overgrown stair and torii line leading to nothing. Mountain, rare,
  `[terrain]`. Hook: navigation, eerie.

== 17. Graves, mounds and memorials ==

- **Keyhole tomb mound (zenpō-kōen-fun)**: a huge forested mound, sometimes moated, with a shrine or trees on top. The
  shogunate surveyed and repaired imperial tombs in 1697–99 (in window). Plain/forest, landmark (Kinai), large
  `[terrain]`. Hook: LANDMARK, cover, forest. (verify the details of the Genroku repair)
- **Small round tomb mound (enpun / gunshūfun)**: clusters of small round mounds in woods and fields, often with a hokora
  on one. Common in the Kinai and Kantō. Forest/plain, common (regionally), medium `[terrain]`. Hook: cover, landmark.
- **Exposed stone burial chamber (sekishitsu)**: a tomb whose earth has eroded away, leaving huge stones and an open
  chamber (Asuka's Ishibutai type). Plain/forest, rare (landmark), large. Hook: SHELTER (cave-like), landmark.
- **Cliff tomb holes (yokoana-bo)**: rows of small chambers cut into a soft-rock cliff (Yoshimi Hyakuana, Saitama).
  Mountain/river, rare, `[terrain]`. Hook: SHELTER, eerie. (verify how visible they were pre-1887)
- **Kamakura rock-cut tombs (yagura)**: square caves cut into cliffs around Kamakura and Miura, 13th–16th c, with
  gorintō inside. Mountain, occasional (Kamakura area), small caves. Hook: SHELTER, lore.
- **Lone medieval gorintō (gorintō)**: a five-ring stupa in the woods for a forgotten warrior or monk. Forest,
  occasional, small prop. Hook: landmark.
- **Traveller's grave (yukidaore / tabibito no haka)**: a small stone at the roadside for someone who died on the
  journey, buried by the nearest village, sometimes with the name and home province. Roadside, occasional, small prop.
  Hook: lore, a danger tell. (assumed detail)
- **Unclaimed-dead heap (muen-zuka)**: a pyramid of old gravestones gathered from lost graves. Roadside/forest edge,
  occasional, medium. Hook: landmark, eerie.
- **Burial-only grave in the hills (ume-baka)**: in two-grave districts (Kinai) the body was buried out on the hills
  under a stick or stone, and a separate visiting grave was kept at the temple. Forest, occasional, small prop. Hook:
  eerie. (verify for 1730)
- **Battle head mounds (kubizuka / dōzuka)**: mounds over the heads or bodies of the slain. Sekigahara's east and west
  kubizuka (1600) sit on the Nakasendō. Roadside, landmark, medium `[terrain]`. Hook: LANDMARK, eerie.
- **Thousand-person mound (sennin-zuka)**: a mass grave from battle, plague or famine, with a stone. Forest/roadside,
  rare, medium `[terrain]`. Hook: eerie, landmark.
- **Famine memorial (kikin kuyō-tō / gashi-zuka)**: stones or mounds for the famine dead. The Kyōhō famine (1732, in
  window) left the first wave; Tenmei (1780s) left many more. Roadside, occasional (after 1732), small prop/medium. Hook:
  lore. Tenmei `[outside 1680-1750: 1780s]`. (BL notes the Kyōhō stones)
- **Earthquake/tsunami memorial (jishin kuyō-tō)**: stones for the Genroku quake (1703, which wrecked Odawara) and the
  Hōei quake and tsunami (1707). Roadside/coast, occasional, small prop. Hook: lore. (verify surviving in-window stones)
- **Animal memorial (chikurui kuyō-tō)**: *see §9 (hunters') and §5 (horses)*, not counted again.
- **Whale grave (kujira-haka)**: graves for whale foetuses and whales killed by whalers. Seigetsu-an in Nagato dates to
  1692. Coast, rare, small prop. Hook: lore. `[off-map: Nagato]`
- **Drowned-sailor memorial (suinan kuyō-tō)**: *see §20* (not counted here).
- **Wooden grave tablets (sotoba) at a hill grave**: grey weathered boards leaning at a remote grave. Forest, common,
  small prop. Hook: eerie. (BL: graveyard)
- **Hokora on a tomb mound (fun-jō no hokora)**: a tiny shrine on a kofun, which villagers treated as a kami's hill.
  Plain/forest, occasional, small prop. Hook: landmark.
- **Hermit or ascetic's grave (nyūjō-zuka)**: a mound where an ascetic was buried alive, meditating, with a breathing
  tube and bell. Edo examples exist. Mountain, rare, medium `[terrain]`. Hook: EERIE landmark, lore. (verify the
  in-window examples)
- **Sutra-and-grave mound on a pass (tōge no tsuka)**: a mound at a pass top for dead travellers, with a stone Buddha.
  Mountain, rare, medium. Hook: navigation, lore. (assumed)
- **Plague-dead burial pit marker (ekishi-zuka)**: a stone over a pit for the epidemic dead, out of the village.
  Forest edge, rare, small prop. Hook: eerie. (assumed)
- **Buried-coin and urn hoard (maizō-sen)**: a medieval coin hoard in a jar, turned up by ploughs and landslides.
  Forest, rare, small prop. Hook: LOOT (coins). (assumed as a find, not a placed object)
- **Grave of the executed (keishi-sha no haka)**: a daimoku stone or Jizō near an execution ground for the unclaimed
  executed. Roadside, rare, medium. Hook: eerie. (see §18)

== 18. Disaster, execution and punishment marks ==

- **Execution-ground memorial (keijō no kuyō-hi)**: the stones outside the fence at an execution ground by the highway
  approaches:
  - Suzugamori (Tōkaidō, 1651) has a daimoku stone
  - Kozukappara's great Jizō dates from 1741
  Roadside, landmark (urban edge), medium. Hook: EERIE landmark. (BL: Government, execution grounds) [Wikipedia:
  Suzugamori execution grounds]
- **Rural exposure or execution spot**: a bare clearing near the scene of a rural crime, with a post-base stone and a
  small Jizō. Roadside, rare, small prop. Hook: eerie. (assumed)
- **Otama pond marker (Otama-ga-ike)**: the pond near the Hakone sekisho named for Otama, executed in 1702 (Genroku 15)
  for trying to slip round the checkpoint. The pond is nature; the marker and story are man-made. Mountain, LANDMARK
  (Hakone map), small prop at a nature site. Hook: lore, a danger tell (don't bypass). (verify the 1702 date)
- **Head-display stand remains (gokumon-dai no ato)**: a plank stand base by a road near a jail town. Roadside, rare,
  small prop. Hook: eerie. (BL: Government)
- **Landslide scar with a Jizō (yama-kuzure no Jizō)**: a raw slope and debris fan with a small Jizō for the buried.
  Mountain, occasional, `[terrain]` + a small prop. Hook: DANGER (unstable ground), lore.
- **Flood-death memorial (suigai kuyō-tō)**: a stone by a river for flood dead. River, occasional, small prop. Hook:
  danger tell.
- **Eruption shelter or ash trench (suna-yoke bori)**: ditches and banks thrown up against ash drift on fields in the
  Fuji foothills after 1707. Plain, rare, `[terrain]`. Hook: cover. (assumed; tied to §12)
- **Burned-forest boundary (yamabi-ato)**: a black stand of burned trunks from a spread grass fire, with a firebreak.
  Forest, occasional, `[terrain]`. Hook: open ground. (the nature agent overlaps)
- **Avalanche or rockfall warning post (nadare-chūi no fuda)**: a board at a dangerous stretch of road. Mountain, rare,
  small prop. Hook: DANGER tell. (assumed; very uncertain for the period)

== 19. Wild coast: work ==

*Cross-reference, not counted: the lone fisherman's hut (ryōshi no koya), divers' fire hut (ama-goya) and salt-boiling
hut (kama-ya) are BL.*

- **Divers' beach fire ring (ama no takibi-ba)**: a stone ring on the sand where women divers warm up between dives.
  Coast, occasional, small prop. Hook: WARMTH, fire.
- **Boat haul-up beach (funa-age-ba)**: a slope of sand or shingle with wooden rollers and a wooden capstan for dragging
  boats up. Coast, common, medium. Hook: a boat, cover.
- **Upturned boat on the shore (fuse-bune)**: a small boat turned over above the tide line. Coast, occasional, medium.
  Hook: SHELTER (crawl under), cover. (assumed)
- **Net-drying poles (ami-hoshi-ba)**: pole frames and racks hung with nets. Coast, common, medium. Hook: cover, loot
  (net, rope).
- **Seaweed-drying poles and mats (kaisō hoshi-ba)**: poles and mats of wakame and tengusa (agar weed, big in Izu).
  Kanten from tengusa is said to date from c. 1685 (Fushimi). Coast, occasional, medium. Hook: FOOD. (verify the kanten
  date)
- **Nori stakes in the shallows (nori-hibi)**: rows of bamboo and brush stakes in bay shallows for laver. Edo Bay
  (Shinagawa, Ōmori) farming began in the Genroku–Kyōhō years. Coast, occasional, `[terrain]` (a field of stakes).
  Hook: food, a wading hazard. (verify; the urban/rural agents overlap)
- **Abandoned salt field (shio-hama ato)**: a salt field gone back to rough sand, with a collapsed boiling hut, a
  cracked clay pan and a brine pit. Coast, rare, medium. Hook: loot, shelter (partial), landmark. (BL: salt fields,
  live)
- **Driftwood stacks (yorigi no tsumi)**: storm driftwood gathered above the tide line for fuel. Coast, occasional,
  small prop. Hook: FUEL. (assumed)
- **Octopus pots stacked on the shore (tako-tsubo)**: rows of clay pots with rope loops. Coast, occasional, small prop.
  Hook: dressing (not a container, per the BL loot rule).
- **Tidal stone fish trap (ishi-hibi / sukui)**: a stone crescent on the tidal flat that strands fish at the ebb.
  Coast, rare, `[terrain]`. Hook: food. `[off-map: Kyushu / Seto]`
- **Tiny stone jetty in a cove (ko-hatoba)**: a rough dry-stone arm sheltering a landing. Coast, occasional, medium.
  Hook: a landing, cover.
- **Mooring stones and posts (funa-tsunagi ishi / tomo-gui)**: bored stones and stakes in a cove for tying boats. Coast,
  occasional, small prop. Hook: navigation (a landing).
- **Sand fence (suna-yoke gaki)**: a brush or bamboo fence against blowing sand at the dune edge. Coast, occasional,
  medium (linear). Hook: cover. (assumed)
- **Planted coastal pine belt (bōfū-rin / bōsa-rin)**: black pines planted behind beaches against wind and sand, such as
  Niji-no-Matsubara in Karatsu (early 1600s). Coast, occasional, large `[terrain]`. Hook: COVER, navigation. (verify
  local dates)
- **Shell-burning lime pit (kaibai-yaki)**: a pit where shells were burned for lime, on a remote beach. Coast, rare,
  small `[terrain]`. Hook: fire. (assumed)
- **Beach net-hauling capstan (ami-biki no rokuro)**: wooden capstans for hauling beach seines (jibiki-ami, the
  Kujūkuri sardine seines). Coast, occasional, medium. Hook: none (dressing). `[off-map-ish: Bōsō]` (verify)
- **Tengusa diving float (ama no tarai)**: tubs and floats beached at a diving cove. Coast, occasional, small prop.
  Hook: dressing, loot (rope).

== 20. Wild coast: navigation, wrecks, sacred ==

- **Stone lighthouse lantern (tōmyōdō / jōyatō)**: a stone or wooden lantern tower on a headland or quay, oil-lit and
  tended by a keeper or the village. Miya's is from 1625. Coast, rare, medium/large. Hook: NAVIGATION (light), landmark.
  (BL: Civic) [WC §2.6]
- **Channel stakes (miotsukushi)**: tall stakes marking the deep channel into a river mouth or bay; they're Osaka's
  emblem. Coast/river, occasional, medium. Hook: NAVIGATION (the safe line), a wading hazard.
- **Reef warning pole (ansho-gui)**: a pole or brush bundle on a submerged rock. Coast, occasional, small prop. Hook:
  navigation, danger. (assumed)
- **Stranded cargo ship (nanpa-sen)**: a beached or reef-wrecked coastal freighter (bezaisen / higaki-kaisen type) with
  a broken mast, rice bales and sake barrels spilled. Wrecks were frequent in era. Coast, rare, large structure. Hook:
  LOOT SPOT, shelter, landmark. [WC §2.6 ship types]
- **Wreck debris line (hyōchaku-butsu)**: planks, barrels, cordage, a rudder and a mat sail strewn along a beach after a
  storm. Coast, occasional, small props. Hook: LOOT.
- **Beached anchor (ikari)**: an iron four-pronged grapnel or a stone-and-wood anchor half buried. Coast, rare, small
  prop. Hook: LOOT (iron).
- **Salvage marker (hyōchaku-fuda)**: a village board noting wreck goods held for the owner, as law required. Coast,
  rare, small prop. Hook: lore. (verify)
- **Drowned-sailor memorial (suinan kuyō-tō)**: a stone on a headland for the lost at sea. Coast, occasional, small
  prop. Hook: landmark, lore.
- **Ebisu stone (Ebisu-ishi)**: a stone enshrined because it was fished up or washed ashore. Drowned bodies found at sea
  were also treated as Ebisu. Coast, occasional, small prop. Hook: lore.
- **Dragon-god hokora on a headland (Ryūjin no hokora)**: a fishermen's shrine to the sea dragon. Coast, occasional,
  small prop. Hook: landmark.
- **Reef torii (iso no torii)**: a torii standing on rocks or in the shallows facing a sea shrine. Coast, rare, medium.
  Hook: LANDMARK. Itsukushima `[off-map: Aki]`; small reef torii elsewhere (assumed).
- **Konpira sea-safety stone (Konpira-hi)**: a stone to the sailors' god Konpira on a harbour point. Coast, occasional,
  small prop. Hook: landmark. (verify how far Konpira had spread east by 1730)
- **Island hermitage path (shima-mairi michi)**: a tidal path or stepping stones to a small shrine island, usable only
  at low tide. Coast, rare, `[terrain]`. Hook: navigation, danger (the tide).
- **Sea cave with a shrine (umi no iwaya)**: see §6, Enoshima (not counted twice).
- **Pilot's alignment marks (yama-ate no shirushi)**: whitewashed rocks or a lone planted tree on a hill used by
  boatmen to line up a harbour entrance. Coast, rare, small prop. Hook: navigation. (assumed; *yama-ate* the practice is
  real)

== 21. Traces, camps and props of passage ==

- **Discarded straw sandals (sute-waraji)**: worn-out sandals thrown aside every few ri along a road. Roadside, common,
  small prop. Hook: a tell that the road is used, tinder.
- **Horse straw shoes (uma-gutsu / uma-waraji)**: packhorses wore straw shoes that wore through fast, and the cast shoes
  littered the road. Roadside, common, small prop. Hook: a tell. [Kaempfer notes horse straw shoes]
- **Horse droppings on the road**: they were collected by farmers for manure near villages and left lying far from them.
  Roadside, common, small decal. Hook: a tell. (assumed)
- **Broken palanquin or pack saddle (yabure-kago / ni-gura)**: a smashed kago or a wooden pack saddle dumped below a
  road edge. Roadside, rare, small prop. Hook: LOOT (rope, wood), lore.
- **Dead packhorse**: a horse carcass in a ravine below a steep bend, the reason for a batō Kannon. Roadside/mountain,
  rare, small prop. Hook: danger tell, scavengers (danger).
- **Lost pilgrim kit (kongō-zue, sugegasa)**: a pilgrim's staff and sedge hat in the undergrowth. Mountain, occasional,
  small prop. Hook: LOOT.
- **Straw raincoat on a branch (mino-kake)**: a straw cape hung on a tree to dry or left behind. Forest, occasional,
  small prop. Hook: LOOT (rain gear).
- **Woodsman's lean-to (sashikake-goya)**: two forked poles, a ridge pole and a bark or bough roof against a slope. It's
  the most basic shelter. Forest/mountain, occasional, medium. Hook: SHELTER. (no interior, so it stays here; BL has
  hut versions)
- **Bough bivouac under a big tree (ki-shita no nejiro)**: a flattened bed of cut boughs and a small fire under a
  sheltering conifer. Forest, occasional, small prop. Hook: shelter (poor), fire.
- **Bandit lair (sanzoku no nejiro / oihagi no kakure-ga)**: a lean-to in a gully above a pass with a lookout rock,
  stolen bundles and a fire pit. Highwaymen (oihagi) are well attested; the lair form is gameplay invention. Mountain,
  rare, medium. Hook: DANGER, LOOT SPOT. (assumed)
- **Ambush screen (fuse-zei no kakure)**: cut brush propped at a road bend. Roadside, rare, small prop. Hook: danger,
  cover. (assumed)
- **Porter's waiting spot (kumosuke tamari)**: a trampled bank at a pass foot with a fire ring, straw ends and a bench,
  where freelance porters waited for fares. Roadside, occasional, small prop. Hook: a tell, fire. (assumed)
- **Carved graffiti on a rock or tree (rakugaki)**: names and dates cut by pilgrims into rocks, trees and pass shrines
  (a well-known Edo habit at shrines). Mountain, occasional, small decal. Hook: lore.
- **Offering coins and rice on a stone (sai-sen)**: coins and rice grains left on a roadside stone. Roadside, common,
  small prop. Hook: loot (a moral choice, Stephen decides).
- **Tethered-horse scrape (uma-tsunagi no ato)**: churned ground and a gnawed post where horses waited. Roadside,
  occasional, `[terrain]`. Hook: a tell.
- **Abandoned carrying pole and baskets (tenbin-bō, kago)**: a porter's shoulder pole with two baskets, dropped.
  Roadside, rare, small prop. Hook: LOOT.
- **Hidden cache in a tree hollow or cairn (kakushi-ba)**: a bundle wrapped in oiled paper, pushed into a hollow.
  Forest, rare, small prop. Hook: LOOT. (gameplay; assumed)
- **Trail of paper talismans (ofuda)**: talismans pasted on trees, rocks and gate posts along a pilgrim trail. Mountain,
  occasional, small decal. Hook: navigation. (assumed)
- **Woodsman's water gourd hung on a branch (hyōtan-kake)**: a gourd hung by a spring for anyone to drink. Forest,
  occasional, small prop. Hook: WATER tell. (assumed)
- **Abandoned tea-stall shell (hai-chaya)**: a collapsed roadside stall frame, benches rotting, on a stretch where the
  traffic moved. Roadside, rare, medium. Hook: shelter (partial), loot. (a ruin state of BL's kake-jaya)

---

## Obvious collapse candidates (advice only: Stephen decides)

1. **"Inscribed roadside stone" kit.** One square-pillar stone shell with swappable carved faces covers most of §5 and
   parts of §1, §13 and §17:
   - direction, fork, chō and pilgrim stones
   - kōshin, moon-waiting and sun-waiting stones
   - nenbutsu and daimoku stones
   - water-god and mountain-god stones
   - boundary, "killing forbidden" and famine/quake memorials
   About 30 entries become 1 mesh plus text decals.
2. **"Figure stone" kit.** Jizō, dōsojin couple, batō Kannon, Fudō and a generic Buddha. That's 5 carvings on one
   plinth set. Add caps, bibs and offerings as props.
3. **"Small stupa" kit.** Gorintō, hōkyōin-tō and the stupa-shaped chōishi share parts. That's 2–3 meshes.
4. **Lanterns.** Trailhead pair, jōyatō and tōmyōdō differ in scale. One lantern kit in three heights.
5. **Mounds `[terrain]`.** Ichirizuka, kōshin-zuka, border mounds, kyōzuka, kubizuka, small kofun, sennin-zuka. Mostly
   one earth-mound shape at 2–3 sizes, told apart by what sits on top (a tree, a stone, a hokora).
6. **Castle ruins.** Horikiri, tatebori, dorui, kuruwa, koguchi, toride and siege camps are one terrain-sculpting
   toolkit plus 3–4 props (a broken wall corner, a well, post stones). Keep Yamanaka and Ichiya as named layouts.
7. **Small crossings.** Log, plank, slab and earth bridges become one "short bridge" kit with 4 decks. Stepping stones,
   fords and hand-lines are terrain plus props.
8. **Traps.** Snare, deadfall and pit form one "trap" system. The mist net, bird lime and duck net can probably be cut.
9. **River works.** Seigyū, jakago and groynes become one kit. Kasumi-tei, levees and the Bunmei bank are terrain.
10. **Coast work.** Net poles, seaweed poles and drying mats are one pole-rack kit with different hangings.
11. **Wreckage.** The debris line, beached anchor, broken kago and dropped pole-and-baskets become one "scatter" loot-spot
    set.
12. **Cut candidates** (off-map, outside the window, or low value):
    - Ao-no-Dōmon, kuruma-ishi, Inō survey marks, flag-relay hills
    - whale lookout and whale grave, Kashima/Shōki straw giants
    - Kaga duck nets, ajiro, ishi-hibi, kōgoishi, Sado wareto
    - Osorezan, Itsukushima, Kumano ōji, echo rock, avalanche warning post

## Cross-references (belong to another flavour or to BUILDING_LIST)

**To BUILDING_LIST (they have interiors, or BL already holds the site entry; count once):**
- **Huts:** charcoal-burner's hut, logging-crew camp hut, wood-turner's hut, raftsman's hut, hunter's hut,
  ferry-keeper's hut, bridge-keeper's hut, fisherman's and divers' huts, salt-boiling hut, crop-watch hut, field hut
- **Religious buildings:** pilgrim overnight hall (tsuya-dō), mountain pilgrim hut (murodō), hermitages (sōan / iori),
  the mountain ascetic's hut, and the nyonin-dō women's hall
- **Tea houses:** roadside tea house (kake-jaya) and rest-station tea house (tateba-jaya), the "tea stalls in the
  middle of nowhere"
- **Control posts:** sekisho, domain checkpoint (kuchi-dome bansho), coastal lookout hut (tōmi-bansho), river-crossing
  office, ferry control point
- **Site entries already in BL, here from the outdoor side (seam for the merge):**
  - ichirizuka, oiwake stone, ishidatami
  - log, plank, earth, cantilever and vine bridges; boat bridge; ferry landing; rope ferry; weir
  - charcoal kilns, logging camp (shura), rafting station, mines, sulphur workings, fish weir
  - beacon post, weather-watching hill, lighthouse lantern, execution grounds
  - summit/pass shrine, hokora, roadside Jizō, waterfall practice site, cliff Buddhas
- If Stephen wants an interior for the **tsuji-dō crossroads chapel**, the **Jizō-dō** or the **open rain shelter**,
  they move to BL.

**To RURAL man-made:**
- **Crop defences:** boar walls (shishigaki), boar ditches and deer fences where they touch fields; scare clappers
  (naruko)
- **Fields and processing:** slash-and-burn fields, thatch-grass commons (kaya-ba), lacquer, wax and mulberry plantings
  at field edges, shiitake near villages
- **Village-edge sites:** village graveyards and the two-grave ume-baka, field shrines (ta-no-kami), kanjō-nawa and
  straw dolls at the village edge, hyakudo and strength stones at village shrines, commons claim stakes
- **Water and coast works:** irrigation channels, sluices, water-guard huts and treadwheels; nori stakes, net racks and
  boat haul-ups in the fishing village itself (they only count as W on empty coast)

**To URBAN man-made:**
- execution grounds (Suzugamori, Kozukappara) as city-edge sites
- nori beds of Shinagawa as the Edo waterfront
- city bridges (Nihonbashi type), Nihonbashi's distance origin, city fire towers and kido gates
- quays (gangi), canal kura and urban Inari

**To NATURE:**
- the volcanic vents themselves (Ōwakudani), hot springs as water bodies, caves, lava tubes, waterfalls, ponds (Otama
  pond), landslides and debris fans, burned forest, driftwood as a natural drift
- sacred trees and rocks as objects (the rope and offerings are W)
- the tree species of the avenues (WC §2.12 stage F)
- shell middens (kaizuka)

---

## Web sources used (for the source notes above)

- [Hakone navi: Kyukaido Ishidatami](https://www.hakonenavi.jp/international/en/spot/171);
  [Hakone navi: Cedar Avenue](https://www.hakonenavi.jp/international/en/spot/138);
  [Wikipedia: Cedar Avenue of Nikkō](https://en.wikipedia.org/wiki/Cedar_Avenue_of_Nikk%C5%8D)
- [Wikipedia: Moto-Hakone Stone Buddhas](https://en.wikipedia.org/wiki/Moto-Hakone_Stone_Buddhas);
  [Hakone Japan: Stone Buddhist Sculptures](https://hakone-japan.com/discover/national-park/area-information/stone-buddhist-sculptures/)
- [Wikipedia: Kōyasan chōishi-michi](https://en.wikipedia.org/wiki/K%C5%8Dyasan_ch%C5%8Dishi-michi)
- [Wikipedia: Stone Quarries for Edo Castle](https://en.wikipedia.org/wiki/Stone_Quarries_for_Edo_Castle);
  [Izu Geopark: Muroiwado](https://english.izugeopark.org/geosites/muroiwado/)
- [Kanagawa trip: Bunmei-zutsumi](https://trip.pref.kanagawa.jp/destination/bunmei-zutsumi/972);
  [Hakone Geopark: Bunmeitsutsumi](https://hakone-geopark-app.com/en/area_minamiasigara-en/bunmeitsutsumi/)
- [Mt Fuji World Heritage Centre (Hōei ash recovery)](http://mtfuji-whc.jp/guidance/en/zone08.html);
  [Wikipedia: Hōei eruption](https://en.wikipedia.org/wiki/H%C5%8Dei_eruption)
- [Wikipedia: Suzugamori execution grounds](https://en.wikipedia.org/wiki/Suzugamori_execution_grounds)
- [Wikipedia: Five Sacred Trees of Kiso](https://en.wikipedia.org/wiki/Five_Sacred_Trees_of_Kiso)
- [Stone Islands of Setouchi: boar wall](https://stone-islands.jp/en/point/detail/46/);
  [Dry stone wall relics, Mt Hira study](https://www.researchgate.net/publication/363598854_Dry_Stone_Wall_Relics_as_a_Part_of_Cultural_Landscapes_A_Case_Study_from_the_Foot_of_Mt_Hira_Region_in_Japan)
- [Inagi City: Kōshin-tō](https://www.city.inagi.tokyo.jp/en/kanko/rekishi/1011408/1003752/1003754/1003773.html);
  [Wikipedia: Kōshin](https://en.wikipedia.org/wiki/K%C5%8Dshin)
- [Wikipedia: Dōsojin](https://en.wikipedia.org/wiki/D%C5%8Dsojin)
- [MFA Boston: Batō Kannon](https://www.mfa.org/collections/object/bato-kannon-the-horse-headed-bodhisattva-of-compassion-28068);
  [Tsukublog: Batō Kannon stone](https://tsukublog.wordpress.com/2017/03/15/ive-discovered-one-in-tsukuba-at-last-a-horse-headed-kannon-sacred-stone-with-an-actual-horse-headed-image/)
- [Japanese Wiki Corpus: Torimi](https://www.japanesewiki.com/title/Torimi.html);
  [Wikipedia: Shōrui Awaremi no Rei](https://en.wikipedia.org/wiki/Sh%C5%8Drui_Awaremi_no_Rei)
- [Wikipedia: Kanjo Nawa](https://en.wikipedia.org/wiki/Kanjo_Nawa)
- [Wikipedia: Ushi no toki mairi](https://en.wikipedia.org/wiki/Ushi_no_toki_mairi)
- [Wikipedia: Sesshō-seki](https://en.wikipedia.org/wiki/Sessho-seki)
- [ScienceDirect: Seigyu crib spur dike](https://www.sciencedirect.com/science/article/pii/S2772411524000715)
- [JNTO: Mt Fuji Yoshida Trail](https://www.japan.travel/en/spot/2328/);
  [Wikipedia: Fujikō](https://en.wikipedia.org/wiki/Fujiko_(religion))
- [ResearchGate: Edo beekeeping figure (Nihon sankai meisan zue)](https://www.researchgate.net/figure/Beekeeping-in-the-Edo-period-using-Japanese-honeybees-Apis-cerana-japonica-From-Noted_fig1_342473268)
- [Wikipedia: Toi gold mine](https://en.wikipedia.org/wiki/Toi_gold_mine)
- [Hakone Japan: Hakone Sekisho](https://hakone-japan.com/things-to-do/sightseeing/hakone-sekisho-checkpoint/)
