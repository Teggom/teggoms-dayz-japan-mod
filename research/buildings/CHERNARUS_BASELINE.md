# Chernarus baseline: what buildings vanilla uses, and how many

Source: every placed object in the vanilla world file (`addons/worlds_chernarusplus.pbo`, OPRW, 2,971,218 objects),
read with `pokemon_dev/tools/spawns/extract_world_objects.py`'s reader on 2026-09-29. "Lootable" means the class has
a group in the vanilla `mapgroupproto.xml`. It's a reference for sizing the Japan building list
(`BUILDING_LIST.md`), not a target.

## The headline

- **About 5,300 real buildings** from about **165 models**. Some models are just colour variants of the same house
  (`house_1w10` and `house_1w10_brown`).
- **Plus about 6,000 small structures:** sheds, outhouses, greenhouses, garages, hunting stands and open roofs.
- **Six in ten real buildings are homes.** The 1–2 storey village house alone is 42% of all real buildings, from
  27 models.
- **Rare types really are rare:** 2 hotels, 5 schools, 6 hospitals, 1 prison, 10 castle ruins, 40 churches and
  chapels.

## Real buildings (5,276)

| Category | Count | % | Models | Notes |
|---|---|---|---|---|
| Dwellings | 3,139 | 59.5 | ~52 | See the split below |
| Workshops and industry (enclosed) | 908 | 17.2 | ~31 | Workshops 559, cement works 85, water stations 76, industrial gatehouses 70, repair |
| Military | 426 | 8.1 | ~42 | Small watchtowers 155, army tents 95, barracks 70, guardhouses 51, hangars 23 |
| Commerce and services | 376 | 7.1 | ~15 | Kiosks 153, pubs 102, shops 48, car repair 48, fuel stations 19, hotels 2 |
| Farm buildings | 311 | 5.9 | 8 | Barns 200, cowsheds 111 |
| Civic and government | 76 | 1.4 | ~14 | Police 20, offices 18, clinics 17, fire stations 7, hospitals 6, schools 5, prison 2 |
| Religious | 40 | 0.8 | 5 | Churches 25, chapels 15 |

**Dwellings split:**

| Type | Count | Share of dwellings |
|---|---|---|
| Village house, 1–2 storey | 2,220 | 70.7% |
| Town apartment block, 1–3 storey | 667 | 21.2% |
| City tenement | 170 | 5.4% |
| Holiday cabin | 82 | 2.6% |

**Also:** 10 castle ruins (245 wall and tower pieces) and 1,531 ruin and rubble pieces, none of them lootable.

## Small structures (about 6,000)

| Type | Count |
|---|---|
| Garden sheds (10 models) | 2,586 |
| Open-sided roof sheds (industrial/farm) | 1,727 |
| Greenhouses and polytunnels | 457 |
| Outhouses (dry toilets) | 439 |
| Private garages | 349 |
| Hunting stands | 226 |
| Feed shacks | 117 |
| Wells and pumps | 79 |
| Farm water towers | 32 |

**Roughly one outhouse per 7 homes and nearly one garden shed per home.** The small stuff is as common as the
buildings themselves.

## Per model, most-placed first

**Village houses:**
- house_1w11 156, house_1w03 141, house_2w01 136, house_1w04 134, house_1w06 126, house_2b01 122, house_1w02 122,
  house_2w02 121, house_1w01 118, house_1w07 111
- house_1w10 76 (+brown 73), house_1w05 68 (+yellow 66), house_1w09 65 (+yellow 65), house_1w08 65 (+brown 64)
- house_2b04 48, house_2b03 43, house_2w03 39 (+brown 40), house_2w04 35 (+yellow 35), house_1w12 29 (+brown 28),
  house_2b02 26

**Town blocks:**
- houseblock_1f1 73, 1f3 70, 1f2 59, 2f_corner 56, 1f4 48, 2f5 41, 2f4 38, 2f2 37, 2f1 36, 2f6 35, 2f8 25, 3f1 23,
  1f_corner 23, 2f3 21, 3f2 20, 2f7 19, 2f9 18, 3f_corner1 12, 3f_corner2 11, 5f 2

**Commerce and services:**
- **Pubs:** house_1b01_pub 68, village_pub 34
- **Kiosks:** city_stand_news2 45, city_stand_grocery 45, city_stand_news1 34, city_stand_fastfood 29
- **Shops:** village_store 29, city_store 11, city_store_withstairs 8
- **The rest:** repair_center 25, garage_office 23, fuelstation_build 19

**Workshops:** workshop1 144, workshop_box 112 (no loot), workshop2 101, workshop4 84, workshop3 71, workshop5 47

**Farms:**
- **Barns:** barn_brick2 62, barn_wood1 46, barn_wood2 46, barn_brick1 40, barn_metal_big 6
- **Cowsheds:** cowshed a 33, b 45, c 33

**Military:**
- **Towers and guardhouses:** mil_tower_small 155, mil_guardhouse1 36
- **Barracks:** 1–6 plus round, 70 in total
- **Army tents:** 95 in total, across 12 models

**Religious:** chapel 15, church1_yellow 8, church3 7, church2_2 6, church2_1 4

## What it suggests for Japan (my reading, not a decision)

- **About 165 models built Chernarus.** That sits inside the 80–180 shell range that `BUILDING_LIST.md` §6 gives for
  collapsing.
- **The homes do the heavy lifting.** A lot of variety comes from roughly 25–50 home models, some of them just colour
  variants.
- **Special buildings can be one-offs.** Chernarus has a single prison, 2 hotels, 5 schools and 10 castles, and
  they're still memorable. A Japan map could carry one sekisho, one castle and a handful of temples the same way.
- **Workshops are a big share, 17%, from only 6 generic models.** That fits Stephen's idea of a few generic trade
  shells that take different tools inside.
- **Small structures matter.** Japan equivalents would be sheds, toilets (setchin), wells, drying racks, charcoal
  kilns and hut shrines. They're cheap models that make places feel lived in.
