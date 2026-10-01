# Audit: what are we still missing? (agent A4, 2026-09-30)

Research only. Checked against PRODUCTION_PLAN.md, FEASIBILITY.md §5 and §9, OPEN_ISSUES.md, research/REVIEW_INDEX.md,
the five KEEP lists, G1_DECISIONS.md, LIFE_LAYER.md, the outdoor kit build list, `src/JP/*`, the test mission
(`mission/japantest.japantestisland/`) and the vanilla gear/animal folders on `P:\DZ`. Greps and headings only, no
deep reads.

## Summary

The **world side is very well covered**: the master lists (OUTDOOR_LIST 1,706 entries, BUILDING_LIST 682) already name
almost every "little Japanese thing" I could think of, so most of Part 2 is not missing, it is **listed but not yet
picked** (KEEP_OUTDOOR set only target counts per group, and only the ~25-item core kit + the 24 outdoor life-layer
items have been built). The real hole is the **player/item side**: there is not one JP consumable, tool, light,
container, medical item or loot table yet. The test mission still spawns players with a BandageDressing, a chemlight
and an Apple, and runs vanilla CE types (cans, guns, electronics). Two built things break binding rules: the built
**sakura is a Somei-yoshino in full bloom** (banned as 1840s+, and the season is autumn), and FEASIBILITY §5 still says
"Spring". Status keys: **BUILT**, **IN CATALOGUE** (named in a KEEP list / plan, not built), **LISTED** (in a master
list but not named in any KEEP list, so it can be lost at the group pick), **MISSING** (no hit anywhere).

---

## Part 1: DayZ systems

Ranked by how much a player notices it in the first ten minutes.

| # | Item | Status | Why it matters (vanilla → 1730) | Size | ⚠ era note |
|---|---|---|---|---|---|
| 1 | **JP loot table (CE types.xml) + vanilla-item purge** | MISSING | Mission runs vanilla types: cans, guns, radios, NBC gear will spawn. Need a cfgignorelist/types pass that zeroes every period-wrong vanilla class and adds the JP set. Tiers stay ignored (standing decision); this is just "what exists" | M | |
| 2 | **Player spawn gear** | MISSING | init.c gives BandageDressing + chemlight + Apple. → cloth strip (sarashi/tenugui), flint-and-steel kit, rice ball in a bamboo-sheath wrap, straw sandals, short kimono | S | |
| 3 | **Carryable light sources** | MISSING | Flashlight, headtorch, chemlight, gas lamp → folding paper lantern with candle (odawara/hako chōchin), pine-resin torch (taimatsu; vanilla Torch is already period, reskin), rapeseed-oil dish lamp (tōmyō). Andon exists only as static dressing | M | ⚠ candles were costly; tallow/wax candle as rare loot |
| 4 | **Fire-making items** | MISSING (prop only) | Matchbox, petrol lighter → hiuchi flint + steel + tinder box (hokuchi) and sulphur splints (tsukegi). LIFE_LAYER #26 is a static prop only. Hand drill kit stays | S | |
| 5 | **Food overhaul** (PLANNED: sub-items not yet thought of) | PLANNED, gap | Remove: all cans + can opener, banana, orange, kiwi, tomato, zucchini, potato, powdered milk, crackers, chips, spaghetti, marmalade, cereal. Keep/rename: rice (vanilla has it), carp, mackerel (saba), sardine (iwashi), pollock (tara), honey, plum (ume), pear (nashi), pumpkin (kabocha), chili, mushrooms. Add: umeboshi, takuan, miso, dried fish (himono), katsuobushi, hoshigaki, chestnuts, mikan, soba, mochi, onigiri, konbu, tofu (spoils fast), matsutake/shiitake; iwana/yamame replace steelhead trout | L | ⚠ potato (1598 Nagasaki, rare), sweet potato (spreads 1735: Satsuma only), Western apple (no; small wa-ringo yes) |
| 6 | **Drink containers** | MISSING | Water bottle, canteen, soda, vodka, milk → gourd (hyōtan), bamboo water tube (planned in bamboo economy), sake tokkuri/taru, tea. Wells already give water | S | |
| 7 | **Medical set** | MISSING | Bandage → sarashi strips; disinfectant → shōchū; painkillers/charcoal tabs → herbal packets (gennoshōko etc.); splint → bamboo splint; tetracycline/blood bags/IV/saline/defibrillator/epinephrine/tablets → removed; boiling replaces purification tablets. Add moxa (mogusa) as a regen/comfort item and the medicine peddler's box (Toyama, 1690s+) as the "first aid kit" | M | ⚠ opium as morphine stand-in: existed as medicine, rare: maybe skip |
| 8 | **Animals** (fauna parked) | PLANNED, gap | Vanilla spawns sheep, reindeer, goats, pigs, red/roe deer and dairy cows. 1730: no sheep, no reindeer, pigs barely on Honshu, cattle are draft oxen (no milk). Keep wolf (Japanese wolf, extinct 1905), boar, fox, hare, chicken. Reskin: deer → sika, roe → serow, bear → Asian black bear, horse → small native breed | L | ⚠ goats rare |
| 9 | **Cooking + campfire** (PLANNED: sub-items) | PLANNED, gap | Vanilla pot, frying pan, cauldron, tripod, gas cooker, stone oven, barrel-with-holes → iron nabe and kama, clay roasting pan (hōroku; no frying pans), pot hook over the irori (jizai-kagi), clay brazier (shichirin/hibachi), bamboo skewers for fish stuck round the fire (very iconic), steamer (seiro, prop exists) | M | ⚠ "shichirin" name may be later; the clay brazier itself existed |
| 10 | **Tools** | MISSING | Keep/reskin: hatchet → ono + nata (machete-like billhook), handsaw → pull saw (nokogiri), sickle (kama), hoe (kuwa), pickaxe → tsuruhashi, hammer (genno), whetstone (toishi), sewing kit, knife → hōchō/kogatana, shovel → wooden-edged spade. Remove: pliers, screwdriver, wrench, lug wrench, blowtorch, crowbar, lockpick, epoxy, duct tape (→ rice glue / cord), fire extinguisher (→ fire hook + bucket) | M | ⚠ all-iron spade rare |
| 11 | **Containers / carry** | MISSING (props only) | First-aid kit, protector case, waterproof bag, ammo box, drum, backpacks → furoshiki bundle, kinchaku pouch, inrō, wicker kōri trunk, straw bale (tawara), oi back frame, seoi-kago back basket, travel bundle on a stick. Kōri/baskets exist only as static props | M | |
| 12 | **Base building** (PLANNED in FEASIBILITY §5: palisade, plaster wall, yakuimon gate, yagura) | PLANNED, gap | Not yet mapped: tents → reed/straw lean-to and the war curtain (jinmaku with crest); flag/territory flag → nobori or clan banner; code/combination lock → wooden bar (kannuki) + Japanese box padlock (jō-mae); barbed wire → abatis (sakamogi) / bamboo stakes; camo net → straw mats (mushiro); sea chest/barrel storage → nagamochi, tansu, taru; fence kit → bamboo fence kit. Nails: iron wa-kugi existed but were dearer: wooden pegs as alternative | L | |
| 13 | **Dynamic events (CE events)** | MISSING | Heli crash, police car, convoy, train wreck, contaminated zone, Christmas trees → ambushed daimyo baggage train (nagamochi chests, spears, palanquin), wrecked coastal cargo ship (bezaisen) on the shore, burned-out house, abandoned battle camp, overturned merchant handcart convoy. Gas zone → Ōjigoku sulphur valley (already a landmark with a gas hazard) | M | |
| 14 | **Infected** (PLANNED: sub-items) | PLANNED, gap | Need a role roster mapped to vanilla infected classes: farmer, townswoman, monk, pilgrim, porter/kago bearer, fisherman, firefighter (hikeshi), merchant, ashigaru in armour (= armoured/soldier infected), samurai, priest. Plus their loot and Japanese voice/grunt set | L | |
| 15 | **Audio** (PLANNED: sub-items) | PLANNED, gap | Autumn crickets (suzumushi/matsumushi) at night, stag deer calls (autumn rut, a poetry cliché), large-billed crows, black kites whistling, the hour bell (toki no kane) as a world sound, clappers (hyōshigi) at night, wind in bamboo, rain on thatch vs tile, shishi-odoshi clack. Footsteps: see #16. Menu music: shakuhachi/shamisen | M | ⚠ hyōshigi fire patrols are mostly a town thing |
| 16 | **Surface footsteps (CfgSurfaces)** | MISSING | No CfgSurfaces in src: tatami, board floor, doma earth, raked gravel, stone steps will sound like vanilla concrete/wood. Tatami should be soft and near-silent; gravel crunchy | S | |
| 17 | **Navigation items + map UI** | MISSING | Map → folded paper road map (dōchūzu style; the 1690 Tōkaidō bunken ezu sets the look), compass → small hōi compass, GPS/watch/alarm clock/radio/walkie/megaphone → removed, binoculars → telescope (tōmegane, rare loot). Optional: conch trumpet (horagai) as a noise/signal item. Map UI texture painted in ezu style | M | ⚠ hand compass existed but rare; no portable clocks |
| 18 | **Weather and time config** | MISSING | Autumn date, ~35° N latitude, autumn showers (shigure), a typhoon (nowaki) storm preset, Hakone-style fog, temperatures. FEASIBILITY §5 still lists "Spring": superseded by autumn | S | |
| 19 | **Crafting recipes** | MISSING | Vanilla recipes assume rags, burlap, duct tape, wire. New: straw rope (nawa), straw sandals (repair/replace footwear), mino raincoat, bamboo spear (takeyari: iconic), bamboo canteen, bamboo splint, pine-resin torch, kimono → cloth strips, fish trap (ue) from bamboo | M | |
| 20 | **Traps** | MISSING | Bear trap, landmine, tripwire → snare (kukuri-wana), deadfall (otoshi), pit, bamboo fish trap. KEEP_OUTDOOR's "period traps" are world props only | S | |
| 21 | **Cultivation** | MISSING | Seeds tomato/pepper/zucchini/potato/cannabis → daikon, eggplant (nasu), soybean, millet (awa/hie), chili, kabocha, tobacco. Garden lime → wood ash or night soil | S | ⚠ sweet potato as #5 |
| 22 | **UI text and screens** | MISSING | Main menu, loading screens (period prints), item names/descriptions (romaji + English), inventory icons for every new item, hint texts mentioning Chernarus, server/map name. The B1 brush fonts cover world text only | M | ⚠ Hiroshige/Hokusai are post-1730: use Moronobu-era prints or pre-1730 scrolls for screens |
| 23 | **Weapons** (PLANNED in FEASIBILITY §5) | PLANNED, gap | Built: katana, yari, yumi + ya. Not yet: wakizashi, tantō, naginata, kanabō, bō, matchlock, shuriken. Gaps: matchlock kit (powder flask, lead balls, match cord), sword-on-obi carry (OPEN_ISSUES), whetstone sharpening; the test crossbow variant (JP_Yumi_XB) is not period and should not ship | M | ⚠ shuriken: mostly a later/fictional image; rare at most |
| 24 | **Clothing slot map** (wardrobe parked) | PLANNED, gap | Built: kimono x2, kasa, tabi-waraji. Vanilla slots still unmapped: headgear (zukin hood, hachimaki, kabuto), mask (menpō, tenugui), gloves (tekkō), vest (dō armour = plate carrier), belt (obi), back (oi), raincoat (mino), eyewear (none). GEAR_SLOTS.md has the obi call only | L | |
| 25 | **Junk / comfort loot** | MISSING | Cigarettes → kiseru pipe + tobacco pouch; book → woodblock book or almanac; teddy bear → cloth doll; wallet/money → strings of mon coins, a purse; fireworks → remove | S | ⚠ Ryōgoku fireworks start 1733 |
| 26 | **Boats** | LISTED | Vanilla motor boat → flat-bottom river boat or ferry (watashibune) as a rowed boat; beached boats exist as props (LIFE_LAYER #67) | L | |

**Part 1: 17 MISSING + 8 PLANNED-with-gap + 1 LISTED** (items 1-4, 6, 7, 10, 11, 13, 16-22, 25 MISSING; 5, 8, 9, 12, 14, 15, 23, 24 planned with a gap; 26 listed).

---

## Part 2: little Japanese things

Almost everything below is already in the master OUTDOOR_LIST, so the risk is that it gets lost when each KEEP group
makes its picks. LISTED items are worth naming explicitly at those picks. MISSING items had zero hits.

| # | Item | Status | Why it matters | Size | ⚠ era note |
|---|---|---|---|---|---|
| 1 | **Autumn cherry: rebuild the sakura** | BUILT, WRONG | `src/JP/plants/tree/jp_sakura_01/02` are Somei-yoshino in full bloom (F_flora REPORT): banned (1840s+) and wrong season. Rebuild as yamazakura / edohigan in autumn orange-red leaf, keep the bloom as a future seasonal variant | M | |
| 2 | **Highway pine/cedar avenues (namiki)** | LISTED | The single strongest "Tōkaidō" look: rows of pines or sugi lining every highway. A placement recipe, not a model | S | |
| 3 | **Distance mounds (ichirizuka)** | LISTED | Paired earth mounds with an enoki or pine on top, every ri along the highways. Cheap, instantly period | S | |
| 4 | **Higanbana on paddy dikes + susuki plumes** | LISTED (N §Y) | The autumn colour signal on every dike and field edge; clutter meshes, not models | S | |
| 5 | **Persimmon trees with fruit (+ one left for the birds, kimamori)** | LISTED / MISSING (kimamori) | Orange fruit on bare branches is THE autumn village picture; hoshigaki curtains are built, the tree with fruit is not | S | |
| 6 | **Komainu guardian pair** | IN CATALOGUE (shrine forecourt group) | Every shrine approach; also Inari fox pairs | S | ⚠ OUTDOOR_LIST §3.3 flags komainu in villages as a contradiction: stone village komainu are mostly later; use at town shrines, wooden/none in villages |
| 7 | **Rice terraces (tanada) + paddy levees + water inlets** | IN CATALOGUE (terrain tools) | Hillside paddies define the countryside; stubble + hasa racks already built | L | |
| 8 | **Bamboo pipes (kakei) and the deer scarer (sōzu / shishi-odoshi)** | kakei IN CATALOGUE (LIFE_LAYER #60); sōzu LISTED | Water trickling into troughs, the clack in temple gardens | S | ⚠ sōzu as a garden device dates to Ishikawa Jōzan (1600s): OK |
| 9 | **Bamboo fence styles (yotsume-gaki, brushwood shibagaki, curved inu-yarai)** | IN CATALOGUE (fences group, 14) / styles LISTED | Kyoto's curved bamboo "dog-fence" at house bases and lattice fences read instantly Japanese | S | |
| 10 | **Hedges (ikegaki), stone walls (ishigaki technique variants)** | IN CATALOGUE | Field and yard boundaries | M | |
| 11 | **Water wheels (suisha) and treadwheels (fumiguruma)** | LISTED | Mills and irrigation on village streams | M | ⚠ fumiguruma for paddies is mid-1600s+: OK |
| 12 | **Ema plaques at shrines (+ ema-den hall ☆)** | LISTED (hall is ☆) | Hung wooden votive plaques; the hall is stretch, the plaque rack is cheap | S | |
| 13 | **Shrine bell with pull rope (suzu) + offering box** | IN CATALOGUE (forecourt) | The haiden front everyone recognises | S | |
| 14 | **Temple bell tower (shōrō) and its bell** | IN CATALOGUE (Buddhist) | Plus the hour-bell sound (Part 1 #15) | M | |
| 15 | **Scarecrows (kakashi) + bird clappers (naruko)** | IN CATALOGUE (LIFE_LAYER #62) / naruko LISTED | Autumn fields | S | |
| 16 | **Village-boundary straw guardians (Kashima / Shōki straw figures) and boundary ropes** | LISTED | Giant straw figures and ropes across the road at the village edge to keep sickness out: eerie and perfect for a dead world | S | ⚠ regional (Tōhoku/Kantō, some Kinai) |
| 17 | **Inscribed boundary / signpost stones (michishirube, kokkyō stones)** | LISTED | "To Edo, x ri"; province-border pillars | S | |
| 18 | **Roku-jizō row, kasa-jizō (jizō in straw hats), stacked pebbles (sai no kawara)** | Jizō BUILT; row + hats + pebbles LISTED / MISSING | Small variants of a built family; the straw hat is a cheap swap | S | |
| 19 | **Five-ring stones (gorintō), kuyōtō memorial towers, wooden grave tablets (sotoba)** | LISTED (W2 is doing graveyard stones now) | Check W2's picks include gorintō + sotoba | S | |
| 20 | **Ward gates (kido) and town guard boxes (jishinban / tsujiban)** | LISTED | Every Edo street block had a gate and guard box: the city-block look | M | |
| 21 | **Fire lookout (hinomi-yagura) + fire ladder + clappers** | LISTED (fire-watch gear in LIFE_LAYER #68) | Town skyline marker | M | ⚠ OUTDOOR_LIST §3.3 flags fire ladders: check |
| 22 | **Sake cedar ball (sugidama) over brewery doors** | LISTED | Tiny prop, big signal | S | ⚠ widespread later; existed |
| 23 | **Kōsatsu edict boards** | BUILT | (appendix) | | |
| 24 | **Festival floats (dashi), mikoshi store, dohyō sumo ring** | IN CATALOGUE (festival layer later) / dohyō LISTED | Shrine-ground remnants | M | |
| 25 | **Door talismans (Somin Shōrai, ofuda on gates), house name plates** | ofuda IN CATALOGUE (LIFE_LAYER #2); door talisman LISTED; name plates MISSING | Paper charms over every doorway | S | ⚠ house name plates (hyōsatsu) may be later: check |
| 26 | **Giant straw sandals at Niō gates (ōwaraji)** | MISSING | Donated huge sandals hung on temple gate guardians | S | ⚠ date the custom before building |
| 27 | **Night-soil buckets and field manure pits (koeoke, koedame)** | LISTED | Very real, very Edo (urban-rural night-soil trade), and a smell-free way to add farm realism | S | |
| 28 | **Straw mats drying grain (mushiro) + futon/bedding airing** | mushiro LISTED; airing MISSING | Yard dressing for harvest | S | ⚠ futon for commoners is later; air straw/cotton bedding or kimono |
| 29 | **Kotatsu / foot warmer** | MISSING | Late-autumn interiors | S | ⚠ existed (Muromachi+), but likely not set up yet in autumn: low priority |
| 30 | **Lacquer trees with scored bark, mulberry rows, tea bushes on field edges, indigo** | LISTED | Cash-crop landscape; tea as scattered bushes is already a binding rule | S | |
| 31 | **Log rafts (ikada) on rivers** | LISTED | Timber floated down the Kiso/Tenryū | M | |
| 32 | **Red dragonflies (aka-tonbo) particles; autumn insects** | MISSING (1 vague hit) | Ambient life over autumn paddies | S | |
| 33 | **Donated sake-barrel stacks at shrines (kazaridaru)** | LISTED | | S | ⚠ date it |
| 34 | **Teru-teru bōzu (weather doll) under eaves** | MISSING | | S | ⚠ attested mid-Edo; check before 1730 |
| 35 | **Salt cones at doorways (morijio)** | MISSING | | S | ⚠ uncertain for 1730 commoner houses |

**Part 2: 9 MISSING** (5 kimamori, 18 hats/pebbles partly, 25 name plates, 26, 28 airing, 29, 32, 34, 35) **+ 1 BUILT-WRONG; the rest are LISTED or IN CATALOGUE (row 23 is BUILT, kept for reference).** Considered and rejected on era: thousand paper cranes (1797 manual), glass wind
chimes, coloured koi, sake tanuki, beckoning cat, carp streamers, yukitsuri (all already in the binding traps list or
later).

---

## Appendix: already covered (found existing)

- **BUILT (site/plants/arms/clothes):** torii (stone + wood, rope + shide + moss variants, W2 adding more), stone
  lanterns (kasuga, oki, square, jōyatō, mossy), jizō (3 sizes, bibs, halos, huts), Kōshin and other steles,
  chōzubachi basins, shimenawa, kōsatsu boards, nobori, shop fronts (noren, kanban, shape signs, sudare), stalls,
  benches, fire tubs, firewood, gutters, handcarts (abandoned vehicle), laundry poles (cloth, daikon, kaki, net), oke
  tubs, straw stacks (nio, stook, tawara), tenbin loads, stone steps, wells (working, drink/wash), lever well; 50
  interior + 24 outdoor life-layer items (hasa racks, persimmon curtains, scarecrow, kakei, palanquin, dropped travel
  gear, nets, boat); 32+ furniture props; bamboo clump + pole; katana, yari, yumi + ya; kimono x2, kasa, tabi-waraji.
  Sliding doors already use vanilla slide sounds.
- **IN CATALOGUE (planned, not built):** 55 trees incl. **yamazakura and weeping edohigan** (cherry IS there; Somei-yoshino
  banned), 7 bamboos, komainu, offering boxes, lantern rows, graveyard kit (W2 now), micro-shrines (4 stone + 4
  wood, fox pairs), bamboo fences/hedges group, wall kit (ishigaki, dobei, tsuiji, itabei, palisade), bridges, sluices,
  weirs, ferry landing, gangi, lighthouse lantern, shōrō, kagura stage, temizuya, festival layer, castle props, wild
  work sites (charcoal, traps, weirs), paddies/terraces/levees as terrain tools, 22 shop dressing sets (S1 now).
- **PLANNED systems:** Japanese infected (FEASIBILITY §9 option a), food overhaul, cooking/campfire, audio, base
  building (FEASIBILITY §5), bamboo economy, horse riding (later), no cars, matchlock and bow, navmesh, the real map.

## Top 10 to do next

1. **Rebuild the sakura** as autumn yamazakura/edohigan (the built one is banned Somei-yoshino in bloom); confirm the
   bamboo clump reads as madake, not mōsō.
2. **Vanilla purge + JP types.xml skeleton** (zero out cans, guns, electronics, NBC; tiers still ignored).
3. **Spawn gear + the "first hour" kit:** cloth strips, flint-and-steel, rice ball, gourd, paper lantern.
4. **Food list** with Part 1 #5's keep/rename/remove/add split (the planned overhaul's missing detail).
5. **Medical, tools and containers** item lists (Part 1 #7, #10, #11): mostly reskins of vanilla behaviour.
6. **Animal roster fix:** drop sheep, reindeer, dairy cows, most pigs and goats; sika, serow, black bear reskins.
7. **CE dynamic events** as period scenes (baggage train, cargo-ship wreck, burned house, battle camp).
8. **Autumn landscape layer:** namiki avenues, ichirizuka, higanbana + susuki clutter, persimmon trees with fruit.
9. **Weather/time config + CfgSurfaces footsteps** (autumn, typhoon/fog presets; tatami/gravel/doma sounds); fix
   FEASIBILITY §5's "Spring" row.
10. **Name the LISTED shrine/village items at their KEEP group picks:** ema racks, straw village guardians + boundary
    ropes, roku-jizō + kasa-jizō, kido + guard boxes, fire lookout, sugidama, sōzu.
