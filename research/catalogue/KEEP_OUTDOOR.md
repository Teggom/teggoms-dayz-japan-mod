# KEEP list: outdoor (review sitting 4, Stephen + lead, 2026-09-29)

**Status:** APPROVED by Stephen, 2026-09-29.

This collapses `research/outdoor/OUTDOOR_LIST.md` (1,706 entries). Outdoor items are mostly small props, so the
sitting set a **target count per group**. The species and item picks inside each group are made at that group's
build list (gate G1), from the OUTDOOR_LIST entries.

## Season: AUTUMN (Stephen, 2026-09-29: "so the map can be more alive")
DayZ maps have one season. Autumn fixes these:
- **Crops:** rice being harvested, drying racks (hasa) full, harvested stubble fields, persimmons hung to dry, radish
  drying
- **Trees:** red and yellow maples, ginkgo and zelkova colour in the hills; evergreens green
- **Festivals:** autumn festivals and harvest thanks
- **Tree textures:** autumn only for now; seasonal texture sets are future work

## Targets

**Counting note:** these are ITEMS ("a kashi oak", "a bamboo fence"). Chernarus counts every size, length and corner as
its own model (133 tree models ≈ 40–45 species; 142 wall models ≈ 15 styles). Counted that way, ~310 items ≈ 750–950
model files: on par with Chernarus's outdoor set once its road signs, power lines, rail, car wrecks and industrial
clutter are dropped.

| Group (OUTDOOR_LIST §7) | Items | Notes |
|---|---|---|
| **Trees** | **55** | Bumped from 45 (Stephen). See the tree mix below |
| **Bamboo** | **7 tall + 3 ground covers** | See below |
| Shrubs | 10 | |
| Rocks, dead wood | 15 | |
| Wells, water control, river works | 15 | |
| Bridges and crossings (unbuilt) | 8 | Stepping stones, fords, log bridges; built bridges are in KEEP_CIVIC |
| Roadside stones, figures, lanterns | 22 | Jizō, Kōshin, dōsojin, batō Kannon, mile stones, lanterns |
| Shrine and temple forecourt | 14 | Torii wood + stone, komainu, basins, offering boxes, lantern rows |
| Graveyards | 8 | |
| Fences, hedges, garden walls | 14 | Bamboo fence styles, hedges; the big walls are in KEEP_CIVIC |
| Farmyard and harvest | 30 | Autumn-heavy: hasa racks, straw stacks, scarecrows, boar fences, woodpiles, laundry poles |
| Shore and salt | 16 | Beached boats, net and fish racks, salt tools |
| Streets and shop fronts | 28 | Gutters, fire tubs with bucket pyramids, signs, noren, lanterns, benches |
| Canals and boats | 8 | |
| Gardens | 20 | Dry-garden stones, stepping stones, tsukubai, garden lanterns |
| Festivals and markets | 14 | |
| Castle props | 6 | |
| Wild work sites and traces | 28 | Leaning light (Stephen wants wild content): charcoal, hunting, traps, camps, weirs |
| **Total** | **~320** | |

**Beside the models:**
- about 30 clutter meshes (grasses, ferns, flowers, crop proxies, shore wrack)
- about 20 ground textures
- terrain tools: paddies, terraces, levees, ramparts, moats. Paddies and ponds are terrain work.

## The tree mix (55)
- **Conifers (~12):** sugi, hinoki, sawara, red pine (akamatsu), black pine (kuromatsu), momi fir, tsuga hemlock,
  larch (Shinano heights), asunaro, plus sizes and forms as needed
- **Broadleaf evergreens (~10):** evergreen oak (kashi, plus the scrubby coastal ubame), shii, tabu, camphor
  (kusunoki), camellia (tsubaki), sakaki, and others
- **Deciduous (~22):** zelkova (keyaki), beech (buna), konara coppice oak, mizunara, kunugi, chestnut (kuri), small and
  large maples, ginkgo (ichō), wild cherry (yamazakura), weeping edohigan (landmark cherry), hornbeam and forest-edge
  small trees, bank willow, weeping willow, birch, alder, hōnoki, horse chestnut (tochi)
- **Fruit and planted (~5):** persimmon (kaki), ume, mulberry, and others
- **Special forms (~6):** giant old sacred tree (camphor or cedar), dead snag, windswept coastal pine, coppice stump
  with regrowth, pollard, fallen log

Species picks are finalised at the flora build list. **Banned:** Somei-yoshino cherry (1840s+).

## Bamboo: in 1730, and viable (Stephen asked for more types)

| Bamboo | Where | Notes |
|---|---|---|
| **Madake** (Phyllostachys bambusoides) | Village groves behind houses, on levees | The main building and craft bamboo. The test island's cuttable clump should read as this, not mōsō: check |
| **Hachiku** (P. nigra var. henonis) | Cooler places | Finer, whitish culms |
| **Kurochiku**, black bamboo (P. nigra) | Gardens, temple grounds | Black culms; decorative fences |
| **Hoteichiku**, golden bamboo (P. aurea) | Planted | Knobbly bases; fishing rods |
| **Yadake**, arrow bamboo (Pseudosasa japonica) | Thickets by samurai houses, hills, coasts | Arrow shafts |
| **Medake** (Pleioblastus simonii) | Riverbanks, gravel bars, 3–5 m thickets | |
| **Suzutake** (Sasamorpha borealis) | Mountain forest floor, 1–2 m | Underbrush layer |
| Ground covers: **kumazasa**, **miyakozasa**, **Hakone dwarf bamboo** (hakonedake) | Forest floors, Fuji / Hakone slopes | Clutter meshes |

**Banned:** mōsō (P. edulis). It reached Satsuma in 1736.

## The natural feel: stand recipes
The feel comes as much from PLACEMENT as from species count. The flora build list turns N_NATURE's "stand types" into
placement recipes (species mix, density, understorey, floor texture) for:
- open red-pine hills with bare, raked floors near villages (the 1730 look: village hills were cut over, not thick
  forest)
- coppice woodland (satoyama)
- dark sugi and hinoki plantations
- shrine groves (chinju no mori)
- old beech forest
- riverbank willow and medake
- coastal black-pine belts
- bamboo groves behind farms

## Build first: the shared outdoor core kit
OUTDOOR_LIST §5, the top 20:
- firewood stack, bench, pulley and lever wells, roadside Jizō, laundry pole
- graveyard kit, street gutter, stone lanterns
- the stall family, shop lanterns, shop-front kit, shoulder-pole loads
- purification basin, wooden torii, stone steps, notice board
- Kōshin stone, corner fire tub with buckets, wash tubs, festival layer

These dress almost every setting. It's the outdoor twin of the interior core kit.

## Binding: period traps (OUTDOOR_LIST §6)
Never build:
- coloured koi (plain black carp only)
- Somei-yoshino cherry, mōsō bamboo
- the sake-flask tanuki (1930s), the beckoning cat (c.1850s)
- clipped tea-bush rows (1869+; in 1730 tea is scattered bushes on field edges)
- yukitsuri rope cones (Meiji)
- carp streamers (probably later)
- a rain tub at every house (1789+; in 1730, corner tubs with bucket pyramids)
- the hand fire pump (1750s+)
- glass window panes, glass wind chimes, tinplate

§6 lists the in-period alternative for each.

## Not in this count
- **Fauna:** a separate modelling job (N_NATURE fauna appendix)
- **Setting kits (OUTDOOR_LIST §4):** the set-dressing reference for the map work, adopted as is
