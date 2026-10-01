# SHOP SETS: the KEEP_TRADES §A shop dressing sets (agent S1, 2026-09-30)

What makes each trade read right in an ordinary townhouse shop room (mise), what is reused, what is new, where it sits,
how it looks abandoned, where the loot lies, and the 1730 verdict. Binding inputs: `research/catalogue/KEEP_TRADES.md`
§A (the list and its cut list), `G1_DECISIONS.md` A2 (board strip + stepped stands + chōba corner; "as left";
loot rules), `BUILD_LIST.md` (misedana, goods_general, choba, Q5), `LIFE_LAYER*.md`, PLAYBOOK §1 (era test).

**Count.** KEEP_TRADES §A is headed "22 + 3 ☆" but its bullets name 28 trades (12 everyday, 3 food, 2 drink, 3
services, 8 crafts; several "X and Y" entries are one shop). All 28 get a set here; the three ☆ (tatami maker,
lantern and umbrella shop, toy and clay-doll shop) are listed at the end as cheap recombinations, not built.

Sources: `research/buildings/B_TRADE_INDUSTRY.md` (BTI + line), `BUILDING_LIST.md` §5 counts (BL §5.x),
`BUILD_LIST.md` (A2), `LIFE_LAYER_ERA.md` (L1). "general" = general period knowledge, said where the local research
is silent.

## 1. The common shop room (every set)

The 1730 shop (BTI §0.1, line 41): noren at the door, a kanban, a lattice or shutter front, the raised mise with a
board display strip at the street edge, a chōba corner (low lattice, account desk, abacus, ledgers, inkstone), a
tobacco tray for customers, cushions, a hibachi, scales, fire buckets outside, a kura at the back for stock.

| Slot | Where (model frame of any townhouse: the mise rect, street = +z) | What goes there |
|---|---|---|
| **strip** | the shell's board strip (`floors.mise _455`, 0.455 deep along the street edge; demo shops get it by the new townhouse option `mise_floor`) | the stepped stand(s) (`jp_f_misedana` 1 ken, or half in a 2-ken unit; two in a 4-ken) with the trade's goods on the three steps; or the trade's own floor display (casks, bales, tubs, baskets) |
| **steps** | the stand's three treads (0.15 / 0.30 / 0.45 up, 0.20 deep) | small goods clusters (`jp_f_sg_*`, surface mount, visual only): 1 per step; the stand's loot points stay free (goods sit off the point positions) |
| **stock** | the party wall (the side without the door from the toriniwa) | the trade's stock furniture: a shelf (`jp_f_tana_*`, `jp_f_rack_*`) or the trade piece (drawer cabinet, bolt shelf, cask rack, clothes pole, drying cupboard) |
| **choba** | the back corner on the party side, kept out of the door zones | `jp_f_zukue_choba` + `jp_f_choba_set_desk` on it, the coin box (`jp_f_choba_set_zenibako`), the lattice (`jp_f_choba_goshi_2`) where the room is deep enough (>= 2.6 m); a 2-ken room gets the desk only |
| **work** | the room middle-back, out of the 1.00 m band | the craft's work piece (sewing board, painter's mat, tobacco cutter, drug chopper, soba board, loom) |
| **floor** | strip ends, beside the stand | 1-2 extra counted props (bales, casks, crates, baskets) |
| **wall** | the back partition (high), the party wall over the stock | kamidana (undisturbed), calendar, charms, the trade's wall pieces (pawn-tag board, tool board, prints, menu board) |
| **beam** | the loft joists (3.00 m in the townhouse) | lanterns, drying goods (`over="furniture"` when they hang low) |
| **front** | the facade (Res 1 proxies) and the street (map objects) | noren, the trade's kanban / shape sign / sugidama, fold-down bench, display tubs, gutter slabs |

Rules kept by every set (decor checks D1-D16): 5-7 counted props in the mise (goods on steps, wall, beam and front
items don't count); collision cover <= 25 %; a 1.00 m band door-to-door and door-to-centre; >= 1 raised loot surface
(the stand steps always give 3); floor loot 0.4 m clear of footprints; nothing above 1.40 m; kamidana and butsudan
undisturbed, no loot on them.

**Abandoned (G1 A2, "moderate as left").** Every set has an `ab` level: 0 = as it was shut (the less-abandoned
places), 1 = one or two signs (a goods cluster swept, the coin box forced, one fold of the lattice down), 2 = the
heavier room (one in five: stand toppled, stock pulled out, signs askew). Food goods never "keep": fish, tofu, mochi
and greens show their empty / stained / rotted state at ab >= 1. The money box is always forced or gone at ab >= 1.

**Loot.** Floor points on the strip and tatami (the decorator), raised points on the stand steps (3 levels, 0.15-0.45),
on desk / chest / bale / cask tops, and on the new fittings' tops listed below. No loot on goods clusters (dressing),
none on kamidana / butsudan / signs.

## 2. The 28 trades

Legend: **R** reused (existing B3a / B4 / L1 / B3b / L2 props), **N** new in this pass (S1), **sign** = the front sign
(text from the shop atlas `jp_m_decal_sumi_text_shop` unless B1's atlas has it).

### 2a. Everyday shops

| # | Trade (set key) | Signature (what makes it read) | R | N | Where | Abandoned | Sign | 1730 verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | General household goods, ara-mono-ya (`aramono`) | brooms in bundles, stacked tubs and sieves, straw goods hung and piled | oke_bucket, oke_tarai, basket_zaru_stack, mi_furui, mushiro_rolled, sandals_hung_wall | sg_aramono (broom bundle, tub nest, sieve, zaru) | steps: sg_aramono x3; floor: tub + rolled mats; wall: sandals | swept (brooms down, tubs rolled) | 荒物 hang | KEPT. BTI 912-913 (Edo yorozu / ara-mono); tubs 64, baskets 34 (BL §5.1, §5.3) |
| 2 | Draper, gofuku / futomono (`draper`) | bolts end-on in a shelf behind, bolts on the stand, the cloth rule, the balance | goods_general_cloth, choba_set_tenbin, box_s_lacquer, iko_robe | bolt_shelf (cubbies of bolts, 1.82 x 0.45 x 1.50) | stock: bolt_shelf; steps: goods_general_cloth on the strip, sg_bolts on steps | bolts pulled out and trampled; shelf half empty | 呉服 (B1) / 太物 | KEPT. Echigoya fixed-price cutting 1683 (BTI 919-923) |
| 3 | Old clothes, furugi-ya (`furugi`) | garments hung on bamboo poles, folded piles, a patching corner | iko_robe, clothes_kimono, sewing_box | furugi_rack (pole on two stands, 4 garments), sg_folded (folded piles) | stock: furugi_rack along the party wall; steps: sg_folded; work: sewing_box | pole down, garments heaped | 古着 | KEPT. BTI 924-925 (Tomizawa-cho, Yanagihara) |
| 4 | Ironmonger, kanamono-ya (`kanamono`) | tools on the wall, nails in boxes by size, iron pots stacked, scales | kama_nabe, box_s, choba_set_tenbin | kanamono_wall (board: sickles, knives, saws, hoes heads, locks), sg_ironware (pot stack, nail boxes, locks) | wall: kanamono_wall; steps: sg_ironware; floor: kama_nabe | half the tools taken, two fallen; pot stack toppled | 金物 | KEPT. BTI 914-915 |
| 5 | Ceramics and lacquerware, setomono / nurimono (`setomono`) | bowls in straw-packed stacks, a packing crate with straw, lacquer trays and bowls | jar_s/m, jar_m_pale, tableware_bowls | sg_porcelain (sometsuke bowl stacks), sg_lacquer (black + shu bowls, trays), ware_crate (straw-packed crate) | steps: porcelain / lacquer; floor: ware_crate; stock: tana with jars | crate smashed, shards (debris_shards) | 瀬戸物 / 塗物 | KEPT. BTI 916-918. Blue-and-white porcelain (Arita from the 1610s; cheap Hasami bowls 18th c., general). **No Banko ware** (c.1736-41, KEEP cut) |
| 6 | Paper and brushes, kami-ya / fude-sumi-ya (`kamiya`) | paper reams and bundles, brush racks, ink sticks in boxes | goods_general_paper, writing_box, box_s, shopfront_shape_brush | sg_brushes (brush rack + ink-stick boxes) | steps: sg_brushes + goods paper on the strip | swept paper (goods_general_paper_swept) | 筆墨 + B3b brush shape | KEPT. BTI 928-929; paper in 51 entries (BL §5.8) |
| 7 | Oil and candles, abura-ya / rōsoku-ya (`abura`) | oil casks with ladle and funnel, measures, oil jugs, candles by size in boxes, rush-pith wicks | taru_cask, taru_rack3, jar_l, masu_set | sg_oil (jugs, funnel, ladle), sg_candles (candles by size, boxes) | stock: taru_rack3; steps: sg_oil + sg_candles; floor: taru_cask | jugs knocked over (oil stain), candles scattered | 油 / 蝋燭 | KEPT. BTI 930-933, 540-542 (haze-wax candles). Candles plain cream (no painted e-rōsoku: later, general) |
| 8 | Charcoal and firewood, sumi-ya (`sumiya`) | charcoal in straw bales stacked, firewood bundles, a sifter | charcoal_bales3, charcoal_bale, charcoal_burst, firewood_bundle, firewood_stack, mi_furui, charcoal_scuttle | none | floor: bales on the strip (no stand); stock: firewood stack | a bale burst | 炭薪 | KEPT. BTI 934-935 |
| 9 | Tobacco, tabako-ya (`tabako`) | the cutting board with its clamp and the big Sakai knife, leaf bales, paper packets, pipes on display | tawara, tabakobon, choba set | tobacco_cutter (bench, clamp, knife), sg_tobacco (packets + kiseru), shape sign giant pipe | work: tobacco_cutter; steps: sg_tobacco; floor: leaf bale | knife gone, leaf scattered | たばこ (B1) + pipe shape | KEPT. BTI 936-937; the giant-pipe sign BTI 487. Hand knife only (machine cutting later, general) |
| 10 | Travel goods and souvenirs, tabi-dōgu / meibutsu (`tabidogu`) | sandals hung in bunches, mino and kasa, Ōtsu-e prints, Odawara lanterns | sandals_hung_wall, mino_pegs, basket_back, sandals_sale_eave | sg_travel (sandal bunches, kasa), sg_odawara (folded travel lanterns), print_line _otsue (wall) | steps: travel + Odawara; wall: Ōtsu-e line; front: sandals for sale under the eave | prints torn, lanterns crushed | 旅道具 / 大津絵 | KEPT. BTI 942-946. Ōtsu-e: Ōtsu roadside folk pictures since the 17th c. (general); ink-only here. Odawara chōchin: founding date "early 18th c., uncertain" (BTI 497-499): kept, flagged |
| 11 | Rice dealer, kome-ya (`komeya`) | bales stacked, rice bins, masu and strickle, sieve, scoop | tawara_stack6, tawara_kamasu_stack3, masu_to, masu_set, mi_furui | rice_bin (komebitsu, lidded bin with loot top) | floor: bales, bin; steps: masu | bin lid off, rice spilled | 米 | KEPT. BTI 713-714 |
| 12 | Fishmonger and greengrocer, sakana-ya / yaoya (`sakana`, `yaoya`) | fish tubs and flat baskets, the cutting board and deba, salt fish; baskets and shelves of vegetables | drying_fish, drying_daikon, basket_kago, basket_zaru | fish_tub (tub with salt fish / empty stained), fish_board (manaita on legs + deba), veg_basket (big baskets of daikon, turnip, taro, burdock, persimmons) | floor: tubs / baskets on the strip; work: fish_board; beam: drying fish / daikon | ab >= 1: tubs empty and stained, vegetables rotted black | 魚 / 青物 | KEPT. BTI 715-717, 724-725; most fish sold by peddlers (BTI 716) |

### 2b. Food and drink

| # | Trade | Signature | R | N | Where | Abandoned | Sign | 1730 verdict |
|---|---|---|---|---|---|---|---|---|
| 13 | Tofu and wet food, tōfu-ya (`tofu`) | the water tank of tofu blocks, the forming box and press, the stone mill, the big cauldron | usu_ishiusu, kama (kamado), oke_tarai | tofu_tank (wooden tank with blocks; dry stained), tofu_press (forming box + weight stones) | floor: tank and press on the doma side of the strip | tank dry, green stain | 豆腐 | KEPT. BTI 608-611 (old shop; *Tōfu hyakuchin* 1782 is later, not used) |
| 14 | Soba and rice eatery, soba-ya / meshi-ya (`soba`) | kneading bowl, rolling board and pins, noodle knife and guide, seiro trays, eaters on the raised floor with trays | seiro_stack, tableware_zen, meal_left_zen, enza, bench_1ken (street) | soba_board (lacquered kneading bowl, noshi board, pins, knife) | work: soba_board; floor: trays and cushions where eaters sat; front: bench, half noren | trays left, bowls scattered | 御そば切 (B1) + soba stand (B3b) | KEPT. Soba steamed in seiro in this period (BTI 650-654); kendon shops from the 1660s |
| 15 | Sweets and rice cakes, mochi-ya / dango-ya (`mochiya`) | mortar and mallet, trays of mochi / dango / manjū, a tiered box, the charcoal grill with skewers | usu_mallet, seiro_stack, jar_s | sg_sweets (trays: mochi, dango skewers, manjū), konro _grill (dango grill) | steps: sg_sweets; floor: usu; work: konro grill | trays empty, crumbs, mould | 名物 御餅 / B1 御菓子所 / まんぢう | KEPT. BTI 635-639 (sakura-mochi 1717 in era) |
| 16 | Sake shop, saka-ya (`sakaya`) | **the sugidama** (cedar ball) under the eave; casks on a rack with a tap, masu, flasks, customers drinking sitting on casks | taru_rack3, taru_komo, taru_cask, tokkuri_pair, masu_set, taru_rack3_ab | sugidama (green / browned / fallen) | stock: taru_rack3; floor: casks as seats; front: sugidama + 御酒 | rack ab, flasks tipped, sugidama brown or down | sugidama + 御酒 (B1) | KEPT. BTI 576-579; sugidama under brewery eaves BTI 575 |
| 17 | Cooked-food and sake house, nimeuri-ya (`nimeuri`) | a row of simmering pots on a long charcoal stove, the menu strips, casks as seats, flasks, dishes | kama_nabe, taru_cask, tokkuri_large, tableware_bowls, meal_left_two | konro _nabe3 (long stove, 3 pots), menu_board (wall strips with dish names) | work: the stove at the strip; wall: menu; floor: casks as seats | pots cold, one tipped | 煮売 | KEPT. Early-18th c. izakaya forerunner (BTI 659-661). Oden in broth later (BTI 679): pots hold nimono, not oden |

### 2c. Services

| # | Trade | Signature | R | N | Where | Abandoned | Sign | 1730 verdict |
|---|---|---|---|---|---|---|---|---|
| 18 | Apothecary and doctor, kusuri-ya / isha (`kusuri`) | the drawer cabinet of many small drawers, the drug chopper, paper packets, jars, scales, brand signs | jar_s, jar_s_pale, choba_set_tenbin, writing_box | yakudansu (hyakumi-dansu), yagen (drug chopper), sg_medicine (packets, Hangontan / Mankintan labels) | stock: yakudansu; work: yagen; steps: sg_medicine | drawers pulled out, packets spilled | 薬種 (B1) + gourd shape (B3b) | KEPT. BTI 806-817; Toyama medicine from c.1690 (BTI 820). Dutch-learning medicine later (1770s): none |
| 19 | Pawnbroker and moneychanger, shichi-ya / ryōgae-ya (`shichiya`, `ryogae`) | pawn tags on a board, tagged bundles, the ledger; the balance and weights, coin strings, the strong chest, a heavy lattice; **the kura behind** | choba_set_tenbin, choba_set_desk, choba_goshi_3, box stacks, nagamochi | pawn_board (wall: tag board), sg_pawn (tagged bundles), sg_coins (coin strings, silver on a tray), senryobako (strong money chest, loot lid), fundō-shape sign | wall: pawn_board; steps: sg_pawn / sg_coins; stock: senryobako + boxes | chest forced, tags torn | 質 / 両替 + fundō shape | KEPT. BTI 826-833. Set flag `kura_behind`: place a furnished kura (`f_kura_*`) on the lot. Sign: BTI says "coin-shaped"; the fundō (balance-weight) outline is used (general), flagged |
| 20 | Publisher and bookshop, hanmoto / shomotsu-ya (`honya`) | books laid flat on the floor, prints hung on lines at the front, book bags, the publishing ledger | writing_box, box_m, choba_set_desk | sg_books (stacks with title slips), print_line _books (front / wall, sumizuri-e sheets) | steps + strip: books; wall: print line | books scattered, prints torn | 書林 | KEPT. BTI 500-512. **Ink-only prints** (sumizuri-e / tan-e; benizuri-e 1744 and nishiki-e 1765 are later) |

### 2d. Crafts that fit a townhouse

| # | Trade | Signature | R | N | Where | Abandoned | Sign | 1730 verdict |
|---|---|---|---|---|---|---|---|---|
| 21 | Leather goods, fukuromono / setta-ya (`fukuromono`) | pouches and tobacco cases on a board, leather-soled setta in pairs, rolled hides, awls | zukue_plain, box_s | sg_pouches (pouches, cases, setta pairs), hides (rolled hides on the floor) | steps: sg_pouches; floor: hides; work: zukue_plain | pouches swept | 袋物 + B3b geta shape (setta) | KEPT. BTI 187-198 (pouch maker, setta) |
| 22 | Weaving, hata-ya (`hataori`) | the loom, the spinning wheel, yarn skeins, finished bolts | izaribata, itoguruma_thread, goods_general_cloth | sg_yarn (skeins, bobbins), bolt_shelf (shared with the draper) | work: loom in the mise; stock: bolt_shelf | izaribata_cut, yarn tangled | 木綿 | KEPT. BTI 327-329 (frame / ground loom). The tall Nishijin drawloom needs a doma with a tall ceiling (☆ loom house), not a townhouse |
| 23 | Sewing, shitate-ya (`shitate`) | the low sewing board, the cloth rule, hand shears, pin cushion, folded garments | sewing_box, sewing_work, iko_robe | tailor_board (tachi-ita with rule, shears, cloth) | work: tailor_board; stock: iko; steps: sg_folded | garment cut and dropped | 仕立物 | KEPT. BTI 358-360 |
| 24 | Painting, machi-eshi (`eshi`) | the red felt mat with paper, pigment dishes, brushes, glue warmer; fans and scrolls hung | writing_box, box_s_lacquer | paint_mat (felt mat + paper + dishes + brushes), print_line _fans (wall: fans and a scroll) | work: paint_mat; wall: fans | dishes spilled, paper trampled | 絵所 | KEPT. BTI 482-485 (mōsen felt, pigments, gofun) |
| 25 | Lacquer, nushi (`nushi`) | the dust-free drying cupboard (urushi-buro), wares drying on racks, spatulas, lacquer pots | rack_1ken, tana | urushiburo (drying cupboard), sg_lacquer (wares) | stock: urushiburo; steps / rack: lacquer wares | cupboard door off, wares fallen | 塗師 | KEPT. BTI 475-478 ("the dust-free drying cupboard is its tell", KEEP_TRADES 14) |
| 26 | Combs, kushi-ya (`kushiya`) | finished boxwood combs on a board, blanks drying, fine saw and files | zukue_plain, box_s | sg_combs (combs on a board, blanks) | steps: sg_combs; work: zukue_plain | combs scattered | 櫛 | KEPT. BTI 248-250 (boxwood). Tortoiseshell combs are the fine-craft variant (same props) |
| 27 | Dolls, ningyō-ya (`ningyo`) | dolls on display tiers with red cloth (Kyōhō-bina), gosho dolls, heads drying | box_s_lacquer, toys_doll | doll_tiers (3-tier stand, red cloth, dolls), sg_dolls (small gosho dolls) | strip: doll_tiers instead of the stand; steps of the tiers: dolls | tiers toppled, dolls face down | 人形 | KEPT. Kyōhō-bina 1716-36 in era (BTI 526-528). **No daruma** (c.1780s), no Ichimatsu doll (1740s, L1) |
| 28 | Temple-street crafts: images, rosaries, incense, candles (`butsugu`) | rosaries on a stand, incense bundles in boxes, small images in a case, candles | butsu_set_simple, candles (sg_candles) | sg_butsugu (rosaries, incense bundles, a small image) | steps: sg_butsugu + sg_candles | swept | 仏具 数珠 | KEPT. BTI 533-542 |

### 2e. ☆ (not built; recombinations if wanted)
- **Tatami maker**: mushiro / tatami stacks + a work board + rush bundles (straw_stack): needs a tatami-stack prop.
- **Lantern and umbrella shop**: L1 chōchin hung in rows + bangasa (L1) + B3b umbrella shape sign + sg_odawara.
- **Toy and clay-doll shop**: L1 toys + sg_dolls; Fushimi clay dolls would need their own small figures.

## 3. New props (S1), sizes and materials

All in `jp_furniture.pbo` (`StaticObj_JP_F_*`), built on B3a's pipeline (`spikes/S1/build_s1.py`). Frames as B3a /
L1: floor = base centre; wall = facade / wall plane z = 0, heights built in; surface = base centre on a step or top.

| Prop | Kinds / states | Size (m) | Materials | Mount | Loot |
|---|---|---|---|---|---|
| `jp_f_sg` goods clusters | aramono, bolts, folded, ironware, porcelain, lacquer, brushes, oil, candles, tobacco, travel, odawara, sweets, medicine, pawn, coins, books, pouches, yarn, combs, dolls, butsugu; each + `_ab` | <= 0.55 x 0.18 (a 0.20 tread), <= 0.25 high | the goods' own (cloth, paper, iron, ceramics, lacquer, straw, wood, leather, food) | surface | none (dressing) |
| `jp_f_bolt_shelf` | std, _ab | 1.82 x 0.45 x 1.50, 4 x 3 cubbies | wood_interior, cottons | floor | shelf boards <= 1.40 |
| `jp_f_furugi_rack` | std, _ab | 1.82 x 0.45 x 1.70 | bamboo, cottons | floor | none |
| `jp_f_kanamono_wall` | std, _ab | 1.20 x 0.10 board at 0.8-1.7 | wood, iron | wall | none |
| `jp_f_ware_crate` | std, _ab | 0.60 x 0.45 x 0.40 | wood, straw, ceramics | floor | top |
| `jp_f_tobacco_cutter` | std, _ab | 0.80 x 0.35 x 0.32 | wood, iron, straw | floor | top |
| `jp_f_rice_bin` | std, _ab | 0.75 x 0.50 x 0.60 | wood, rice | floor | lid top |
| `jp_f_fish_tub` | fish, _ab (empty, stained) | d 0.70 x 0.22 | wood, bamboo | floor | rim (std) |
| `jp_f_fish_board` | std, _ab | 0.90 x 0.35 x 0.30 | wood, iron | floor | top |
| `jp_f_veg_basket` | std, _ab (rotted) | d 0.55 x 0.40 | bamboo weave, food | floor | none |
| `jp_f_tofu_tank` | std, _ab (dry) | 1.20 x 0.60 x 0.55 | wood, tofu | floor | rim board |
| `jp_f_tofu_press` | std, _ab | 0.50 x 0.40 x 0.45 | wood, stone | floor | top |
| `jp_f_soba_board` | std, _ab | 0.90 x 0.60 x 0.30 | wood, lacquer, shu | floor | board top |
| `jp_f_konro` | grill, grill_ab, nabe3, nabe3_ab | 0.80 x 0.35 x 0.35 / 1.60 x 0.45 x 0.60 | stoneware dark (clay), ash, iron | floor | stove top ends |
| `jp_f_yakudansu` | std, _ab | 0.91 x 0.40 x 1.20 (6 x 6 drawers) | wood, iron | floor | top (1.20) |
| `jp_f_yagen` | std, _ab | 0.45 x 0.12 x 0.15 | iron, wood | floor (visual) | none |
| `jp_f_pawn_board` | std, _ab | 0.90 x 0.03, 0.9-1.6 up | wood, paper, ink | wall | none |
| `jp_f_senryobako` | std, _ab | 0.60 x 0.42 x 0.40 | wood, iron | floor | lid |
| `jp_f_print_line` | books, otsue, fans; each _ab | 1.40 x 0.40 (a cord between two pegs) | paper, ink, cord | wall | none |
| `jp_f_menu_board` | std, _ab | 0.80 x 0.45 strips | wood, ink | wall | none |
| `jp_f_hides` | std, _ab | 0.70 x 0.40 x 0.30 | leather, rope | floor | top |
| `jp_f_tailor_board` | std, _ab | 1.20 x 0.45 x 0.20 | wood, cottons, iron | floor | board top |
| `jp_f_paint_mat` | std, _ab | 1.20 x 0.80 felt, dishes | red felt (bib red), paper, ceramics | floor (visual, Res 1) | none |
| `jp_f_urushiburo` | std, _ab | 0.91 x 0.50 x 1.40 | wood, lacquer | floor | top shelf inside <= 1.0 |
| `jp_f_doll_tiers` | std, _ab | 0.91 x 0.60 x 0.55, 3 tiers | wood, red cloth, gofun, cloth | floor | the tiers |
| `jp_f_sugidama` | green, brown, fallen | d 0.45 ball on a 0.3 cord | foliage (green = _w0, brown = _w2), rope | wall (front, eave) | none |
| `jp_f_kanban_<trade>` | hang, _askew per trade | 0.30 x 0.90 board on an L bracket, text both faces | wood, shop atlas | wall (front) | none |
| `jp_f_kanban_shape_pipe`, `_fundo` | std, _askew | pipe 1.2 long; fundō 0.6 | wood, lacquer, iron | wall (front) | none |

## 4. Materials (S1, add only; `research/materials/make_s1_materials.py`)
- `jp_m_decal_sumi_text_shop`: a third ink atlas (B1's recipe and fonts: Yuji Syuku + Yuji Hentaigana Akebono, OFL):
  the shop kanban texts above, the pawn tags, the menu strips, the medicine labels and packets, book title slips, print
  pages, Ōtsu-e and fan pictures (ink only).
- `jp_m_lacquer_shu`: red (shu) lacquer of bowls, trays, kneading bowls, doll stands (palette `lacquer_shu`, new,
  assumed: a dull brick vermilion darker than the shrine `shu_vermilion`).
- `jp_m_ceramic_porcelain`: blue-and-white porcelain (sometsuke) (palette `porcelain_sometsuke`, new, assumed).
- `jp_m_leather_tan`: tanned leather of pouches, setta soles, hides (palette `cha_koge`, existing).
- `jp_m_food_tofu`: tofu and mochi (palette `gofun_white`, existing).

## 5. Cut and traps (binding)
No beckoning cat (maneki-neko, 19th c.), no daruma (c.1780s), no Banko ware (c.1736-41), no nishiki-e or benizuri-e
(1744+), no tempura stall, no kabayaki shop, no shōchū, no hanafuda, no sencha kyūsu (1738+), no tetsubin, no kendama,
no glass anything, no painted (e-)candles, no oden. Shop names on lanterns only from the existing life atlas (伊勢屋,
大和屋).
