# Outdoor list: everything outside the buildings, 1730 (merged, for collapsing)

Merge agent OD-M, 2026-09-29. Text only. Merged from the four outdoor research files in this folder:
`N_NATURE.md` (plants, ground, landforms, water, seasons, fauna), `W_WILDERNESS.md` (man-made things between
settlements), `R_RURAL.md` (fields, yards, village commons, shrine grounds, fishing and salt shores) and `U_URBAN.md`
(streets, water and bridges, gardens, forecourts, castle town, festivals and markets). Anchor year 1730; 1680–1750
fully in. Companion to `research/buildings/BUILDING_LIST.md` (BL).

**What this is.** Every outdoor item the four agents found, one entry each, ready for Stephen to collapse together with
BL. Nothing is collapsed here. Where two or more flavours listed the same thing, the entries are merged into one (it
sits under the first flavour named and carries a `{seam}` tag); the other copies became one-line pointers.

**How to read it.**
- §1 (this screen): legend and counts. §2: the list, by flavour then group. §3: seams, BL duplicates and
  contradictions. **§4: setting kits** (what makes each kind of place read right; the part map and set-dressing work
  pulls from). §5: the shared "build once" core kit. §6: period traps. §7: collapse candidates. §8: verify checklist.
- Entry format: `- **Name (romaji)**: what it is. Setting, commonness, size. Hook: ...` Italic lines are pointers or
  notes and are not counted. Source keys (Totman, Kaempfer, web pages) were trimmed; they stay in the input files.
- **Loot rule (binding, from BL):** props are dressing, never loot containers. Loot lies on or by them, as in vanilla
  DayZ. Where an input said "loot" it means "loot lies here".
- Commonness words: N uses dominant / common / occasional / rare / landmark per zone; W per map region; R per village
  of the right kind; U per town. They are not on one scale.

**Tag legend (unified).**

| Tag | Meaning |
|---|---|
| `[terrain]` | Heightmap, ground texture, road or linear earthwork; not a placed model. `[terrain decal]` = a surface decal. |
| `[clutter]` | DayZ auto-scattered ground clutter (small grass / flower meshes), not placed by hand (N). |
| `[outside 1680-1750: date]` | Used for two cases only: (a) did not exist yet in 1730 (later invention or fashion), or (b) truly gone by 1730 (destroyed or fully obsolete). |
| `[old: date, still standing 1730]` | **Era test = "did it exist or still stand in 1730?"** Older things that survived into 1730 are fully IN; this tag just gives the date where it helps. Two input entries that tagged old survivors as outside were fixed (W ajiro, R chain pump). |
| `[off-map: region]` | In the window but far from the Kyoto–Osaka–Edo / Tōkaidō / Nakasendō map. Variants kept as written: `[edge of map]`, `[off-map-ish]`, `[off-map mostly]`. |
| `(assumed)` | The agent's best reading, not pinned to a source. |
| `(verify)` | Source memory not re-checked. All are in the §8 checklist. |
| `(mem)` | N only: general knowledge, not re-fetched (most untagged N entries are this). |
| `(BL: section)` / `→ BL` | Pointer to a BUILDING_LIST entry. Site duplicates are listed in §3.2. |
| `{seam S###: ...}` | A merged entry; the flavours and groups it came from. Index in §3.1. |

Size classes: **small** = small prop, under ~2 m, one object; **medium** = 2–6 m or a small cluster; **large** = over
6 m, trees and big structures; **terrain** = `[terrain]` / `[clutter]` work; **other** = N's season variants,
landmark list and fauna appendix (not models). Sizes were read off each entry's own wording (N gives none, so N is
classed by group), so treat the split as rough.

**Counts after the merge** (counted entries; pointers and merged-away copies not counted).

| Flavour | Entries | Small prop | Medium | Large | Terrain / clutter | Other | Merged away | Pointers |
|---|---|---|---|---|---|---|---|---|
| N Nature | 601 | 152 | 52 | 141 | 149 | 107 | 42 | 14 |
| W Wilderness man-made | 302 | 145 | 62 | 11 | 84 | 0 | 70 | 9 |
| R Rural man-made | 307 | 146 | 84 | 16 | 61 | 0 | 98 | 20 |
| U Urban man-made | 496 | 170 | 200 | 41 | 85 | 0 | 90 | 47 |
| **Total** | **1706** | 613 | 398 | 209 | 379 | 107 | 300 | 90 |

Seams: **217** merged entries (182 across two flavours, 34 across three, 1 across four). Before the merge the four files held N 657, W 381, R 425, U 633 lines (pointers included). Other = N's seasons, landmark list and fauna. Setting kits: 19 (§4).

**Contents:** 1. This page · 2. The list (N, W, R, U) · 3. Seams, BL duplicates, contradictions · 4. Setting kits ·
5. Shared outdoor core kit · 6. Period traps · 7. Collapse candidates · 8. To verify

---

# 2. The list

By flavour, then by the agent's own groups (group numbers kept so the input files can be checked). Merged entries carry `{seam ...}`; their other copies are italic pointer lines. Italic lines are not counted.

## 2.N Nature (N_NATURE.md): 601 entries

### == N §A Conifers ==

- **Japanese cedar (sugi, Cryptomeria japonica)**: The signature tall straight conifer of wet valleys, shrine approaches, roadside avenues and planted slopes from lowland to about 1,500 m. Dominant in planted and shrine settings; common wild in wet mountain valleys. Hook: building timber, bark roofing, firewood, deep cover; giant shrine sugi are landmarks. Avenues on the Hakone Tōkaidō date from 1618; Nikkō's avenue 1625–48 (mem).
- **Hinoki cypress (hinoki, Chamaecyparis obtusa)**: Drier ridges and slopes, 300–1,800 m; the prize timber of the Kiso valley. Common (dominant in Kiso). Hook: best building timber, bark for hiwadabuki roofs; in Kiso, cutting one without licence was a capital crime from 1708.
- **Sawara cypress (sawara, Chamaecyparis pisifera)**: Wet valley bottoms and stream sides in the mountains, often mixed with hinoki. Occasional. Hook: water-resistant wood for tubs and buckets (oke). One of the Kiso five.
- **Hiba / asunaro (asunaro, Thujopsis dolabrata)**: Shady wet mountain slopes, Kiso and higher Nakasendō. Occasional. Hook: rot-proof timber; one of the Kiso five.
- **Japanese arborvitae (nezuko / kurobe, Thuja standishii)**: Rocky subalpine slopes of Kiso and the Alps. Rare. Hook: light timber for hats and shingles; one of the Kiso five.
- **Umbrella pine (kōyamaki, Sciadopitys verticillata)**: Steep rocky ridges in Kiso; also planted at temples. Rare / landmark. Hook: bath tubs and coffins; one of the Kiso five (added 1718).
- **Japanese red pine (akamatsu, Pinus densiflora)**: The dominant tree of the over-cut, dry, poor hills around villages; open woodland with grass under it. Dominant (village hills). Hook: firewood and pine-root torches (taimatsu), pitch, matsutake mushrooms grow under it, resinous kindling.
- **Japanese black pine (kuromatsu, Pinus thunbergii)**: The coast tree: dunes, sea cliffs, beach shelterbelts, and planted in rows along the Tōkaidō. Dominant (coast). Hook: windbreak cover, firewood, soot for ink (matsuen); the Tōkaidō pine avenue.
- **Japanese white pine (goyōmatsu / himekomatsu, Pinus parviflora)**: Rocky mountain ridges 500–2,000 m; also a garden and bonsai pine. Occasional. Hook: none special; silhouette variety on crags.
- **Siberian dwarf pine (haimatsu, Pinus pumila)**: Creeping mats above the tree line on the Alps and Fuji's upper slopes. Rare on the map. Hook: impassable low cover at altitude.
- **Japanese fir (momi, Abies firma)**: Lowland to mid-mountain; tall and dark around old shrines and temples and in Hakone forest. Common. Hook: light white wood for boxes, coffins, sotoba grave boards.
- **Nikko fir (urajiromomi, Abies homolepis)**: Mid-mountain, 700–1,800 m, Hakone heights, Fuji, Kiso. Occasional.
- **Veitch's fir (shirabe, Abies veitchii)**: and **Maries' fir (ōshirabiso, Abies mariesii)**: Dark subalpine forest of Fuji and the Kiso/Ontake heights, 1,500–2,500 m. Common at altitude. Hook: cold-zone cover.
- **Southern Japanese hemlock (tsuga, Tsuga sieboldii)**: Rocky ridges and steep slopes, often with momi; Hakone. Common. Hook: timber, tannin bark.
- **Northern Japanese hemlock (kometsuga, Tsuga diversifolia)**: Subalpine, with shirabe. Occasional.
- **Japanese larch (karamatsu, Larix kaempferi)**: Wild only on Fuji's high slopes and the Yatsugatake/Asama volcanoes; a pioneer on fresh volcanic ground. Rare in 1730. Hook: golden autumn needles. The larch plantations of Nagano are `[outside 1680-1750: Meiji]`.
- **Japanese spruce (tōhi, Picea jezoensis var. hondoensis)**: Subalpine Fuji and the Alps. Rare.
- **Japanese nutmeg-yew (kaya, Torreya nucifera)**: Understorey tree in warm forest and shrine groves. Occasional. Hook: edible nuts and nut oil; wood for go boards.
- **Japanese plum-yew (inugaya, Cephalotaxus harringtonia)**: Shady understorey. Occasional. Hook: seed lamp oil.
- **Japanese yew (ichii, Taxus cuspidata)**: Mountain forest, scattered. Rare. Hook: bows and shaku batons; poisonous foliage and seeds.
- **Podocarp / yew pine (inumaki, Podocarpus macrophyllus)**: Warm coast; wild on Izu cliffs, planted as tall hedges around coastal farms and shrines on the Tōkaidō. Occasional. Hook: windbreak hedge; termite-proof wood.
- **Nagi (nagi, Nageia nagi)**: Planted in shrine grounds (sacred at Kumano and Kasuga). Rare / landmark.
- **Chinese juniper (ibuki / byakushin, Juniperus chinensis)**: Coastal rocks, and planted in temple grounds. Occasional.
- **Needle juniper (nezu, Juniperus rigida)**: Dry sunny hills and degraded ground among red pine. Occasional.

### == N §B Broadleaf evergreen trees (the laurel forest, shōyōjurin) ==

*The natural lowland forest of the Tōkaidō side below about 700 m. By 1730 it survived mainly as shrine groves (chinju no mori), temple groves, steep ravines and coastal cliffs. (mem)*
- **Japanese blue oak (arakashi, Quercus glauca)**: The commonest evergreen oak of lowland hills and shrine groves. Common. Hook: very hard wood for tool handles, oars, cart parts; acorns (leached) as famine food.
- **Bamboo-leaf oak (shirakashi, Quercus myrsinifolia)**: Kantō's main evergreen oak; planted as farmstead windbreak (yashikirin) around Musashi farms. Common. Hook: tool handles, charcoal, windbreak.
- **Japanese evergreen oak (akagashi, Quercus acuta)**: Mountain slopes up to ~900 m, Hakone and Izu. Common. Hook: plane bodies and hard timber.
- **Silver-backed oak (urajirogashi, Quercus salicina)**: Warm ravines. Occasional.
- **Ubame oak (ubamegashi, Quercus phillyreoides)**: Dry coastal cliffs and rocky sea slopes. Occasional (coast). Hook: the best hard charcoal (binchōtan; Kishū is `[off-map: Kii]` but the tree is local).
- **Tsuburajii (tsuburajii / kojii, Castanopsis cuspidata)**: Warm lowland slopes and shrine groves, Kantō–Tōkai. Common. Hook: sweet edible nuts (shii no mi), shiitake logs, dense shade.
- **Sudajii (sudajii / itajii, Castanopsis sieboldii)**: Coastal and warm shrine groves; big dome crowns that go cream-yellow in May bloom. Common (coast, groves). Hook: edible nuts, shiitake logs.
- **Camphor tree (kusunoki, Cinnamomum camphora)**: Warm coast and shrine groves; huge sacred specimens (Kinomiya shrine, Atami, said to be ~2,000 years old). Occasional / landmark. Hook: camphor (medicine, insect repellent), shrine landmark tree. (mem)
- **Red machilus (tabunoki, Machilus thunbergii)**: Sea-facing slopes and coastal shrine groves. Common (coast). Hook: bark powder for incense sticks (senkō).
- **Japanese cinnamon (yabunikkei, Cinnamomum yabunikkei)**: Understorey of warm forest. Occasional. Hook: seed oil.
- **Silver tree (shirodamo, Neolitsea sericea)**: Coastal and shrine forest; silvery new leaves. Occasional.
- **Wild camellia (yabutsubaki, Camellia japonica)**: Coast, shrine groves and village hedges; red flowers in winter and spring. Common. Hook: tsubaki oil (hair, cooking, rust-proofing blades), hard wood, ash for dyeing and glazes.
- **Sasanqua (sazanka, Camellia sasanqua)**: Planted as hedges and garden trees; wild only far south-west. Occasional.
- **Japanese holly (mochinoki, Ilex integra)**: Coastal and shrine groves, planted in gardens. Occasional. Hook: birdlime (tori-mochi) from the bark for catching birds.
- **Kurogane holly (kuroganemochi, Ilex rotunda)**: Warm groves, gardens. Occasional.
- **Sakaki (sakaki, Cleyera japonica)**: Shrine groves and warm forest; the sacred Shinto offering branch. Common (shrines). Hook: ritual branches for kamidana and shrine offerings (a gatherable item).
- **Hisakaki (hisakaki, Eurya japonica)**: Village woods everywhere; in Kantō it often stands in for sakaki. Common. Hook: offerings; firewood.
- **Mokkoku (mokkoku, Ternstroemia gymnanthera)**: Coastal forest; a favourite garden tree. Occasional.
- **Yuzuriha (yuzuriha, Daphniphyllum macropodum)**: Mountain and grove understorey. Occasional. Hook: New Year decoration leaves.
- **Holly olive (hiiragi, Osmanthus heterophyllus)**: Hill forest; planted as spiny hedges near gates. Occasional. Hook: setsubun charm (spiny sprig at the door).
- **Japanese privet (nezumimochi, Ligustrum japonicum)**: Warm woods, planted hedges. Common. Hook: hedging.
- **Japanese star anise (shikimi, Illicium anisatum)**: Temple grounds and cemeteries, wild in warm forest. Common (temples). Hook: Buddhist grave offering; highly poisonous fruit; bark for incense.
- **Bayberry (yamamomo, Morella rubra)**: Warm coastal hills, Izu and Sagami. Occasional. Hook: edible red fruit in June; bark dye.
- **Tachibana orange (tachibana, Citrus tachibana)**: Japan's native wild citrus; very rare wild on the Izu coast, planted at shrines and palaces. Rare / landmark.
- **Isu tree (isunoki, Distylium racemosum)**: Warm forest south-west; rare this far east. Rare. Hook: ash glaze.

### == N §C Deciduous forest trees ==

- **Zelkova (keyaki, Zelkova serrata)**: River terraces, village edges, farmstead windbreaks in Kantō, shrine and temple grounds; huge old specimens. Common. Hook: prime timber for temple and wealthy-house beams, drum bodies, mortars; landmark shade tree.
- **Siebold's beech (buna, Fagus crenata)**: The cool-temperate climax forest above ~800 m (Hakone summit ridges, Tanzawa, Kiso, the Fuji shoulder). Dominant (mountain). Hook: firewood, bowls and trays (kiji-ya turners), beechnuts; big open grey-trunk forest.
- **Japanese beech (inubuna, Fagus japonica)**: Lower and drier than buna, Pacific side. Occasional.
- **Konara oak (konara, Quercus serrata)**: THE coppice tree of village hills; cut every 15–20 years, regrows as multi-stemmed stools. Dominant (satoyama). Hook: firewood, charcoal, shiitake logs, acorns.
- **Sawtooth oak (kunugi, Quercus acutissima)**: Coppice and farmstead woods, planted for charcoal. Common. Hook: the best everyday charcoal; acorn caps for dye; sap attracts beetles.
- **Mongolian oak (mizunara, Quercus crispula)**: Upper mountain forest with beech. Common (mountain). Hook: timber, acorns for bears.
- **Daimyo oak (kashiwa, Quercus dentata)**: Dry grassland edges, volcanic foothills, coast. Occasional. Hook: big leaves wrap kashiwa-mochi (Boys' Day); tannin bark.
- **Chinese cork oak (abemaki, Quercus variabilis)**: Dry hills among konara. Occasional. Hook: thick cork bark.
- **Japanese maple (irohamomiji, Acer palmatum)**: Stream sides, gorges, temple grounds; the classic autumn red. Common. Hook: autumn landmark colour; hard wood.
- **Full-moon / large maple (ōmomiji / yamamomiji, Acer amoenum)**: Mountain valleys, larger leaves. Common.
- **Painted maple (itayakaede, Acer pictum)**: Mountain forest; turns yellow. Common. Hook: hard wood; yellow autumn.
- **Downy maple (hauchiwakaede, Acer japonicum)**: Beech zone. Occasional.
- **Snake-bark maple (urihadakaede, Acer rufinerve)**: Mountain forest edges, striped bark. Occasional.
- **Ginkgo (ichō, Ginkgo biloba)**: Planted only (temples, shrines, castle grounds, post-town landmarks); not wild. Common in towns and temples / landmark. Hook: edible nuts (gin'nan), foul-smelling fallen fruit, gold autumn; fire-resistant leaves.
- **Chinese hackberry (enoki, Celtis sinensis)**: Village edges, river levees, planted on ichirizuka distance mounds. Common. Hook: shade; the ichirizuka tree; firewood.
- **Muku tree (mukunoki, Aphananthe aspera)**: Lowland villages, shrine grounds, river terraces. Occasional. Hook: rough leaves used as sandpaper for polishing; sweet berries.
- **Paulownia (kiri, Paulownia tomentosa)**: Planted beside farmhouses (one for each daughter, for her dowry chest); seeds itself on disturbed ground. Common near villages. Hook: light wood for tansu, geta, koto; purple May flowers.
- **Japanese horse chestnut (tochinoki, Aesculus turbinata)**: Mountain valley bottoms, Kiso and Hakone ravines. Common (mountain valleys). Hook: tochi nuts (famine staple after long leaching), tochi-mochi; wood for bowls.
- **Japanese walnut (onigurumi, Juglans mandshurica var. sachalinensis)**: Stream banks and valley bottoms. Common. Hook: edible walnuts; husk poison for stunning fish (a period fishing method).
- **Japanese big-leaf magnolia (hōnoki, Magnolia obovata)**: Mountain valleys. Common. Hook: soft wood for scabbards and geta; huge leaves as food wrappers and plates (hōba).
- **Kobushi magnolia (kobushi, Magnolia kobus)**: Hill forest edges; white spring flowers used as the sign to sow rice seedbeds. Occasional. Hook: planting-calendar cue.
- **Katsura (katsura, Cercidiphyllum japonicum)**: Mountain stream bottoms; huge multi-trunk trees, sweet autumn smell. Occasional / landmark. Hook: go boards, carving wood.
- **Wingnut (sawagurumi, Pterocarya rhoifolia)**: Mountain stream sides in gorges. Common (gorges).
- **Japanese alder and living-tree rack row (hannoki; hasa-gi / inaki)**: alder (or ash) planted in lines on paddy dikes and marsh margins as living posts for rice-drying poles. Field, common as a paddy-edge tree (paddy plains); rare as a rack row on our map `[off-map: mostly Echigo, Hokuriku]` (verify for Kantō), large. Hook: hasa racks, bark dye, firewood. {seam S045: N §C + R §4}
- **Yashabushi alder (yashabushi, Alnus firma)**: Hakone, Izu and volcanic slopes; a nitrogen-fixing pioneer on bare and eroded ground. Common (Hakone). Hook: cones for black dye (with iron).
- **Hornbeams (akashide Carpinus laxiflora, inushide C. tschonoskii, kumashide C. japonica)**: Mixed hill forest and coppice. Common. Hook: firewood, charcoal; in Kantō coppice with konara.
- **Giant dogwood (mizuki, Cornus controversa)**: Mountain valleys; tiered branches. Occasional. Hook: kokeshi and turnery wood.
- **Kousa dogwood (yamabōshi, Cornus kousa)**: Hill and mountain forest; white June bracts, red fruit. Occasional. Hook: edible fruit.
- **Japanese snowbell (egonoki, Styrax japonicus)**: Hill woods; drooping white flowers. Common. Hook: saponin fruit crushed to stun fish; umbrella-rib wood.
- **Ryōbu (ryōbu, Clethra barbinervis)**: Dry ridges and coppice. Common. Hook: young leaves boiled into rice as famine food (ryōbu-meshi); smooth mottled bark.
- **Rowan (nanakamado, Sorbus commixta)**: Mountain and subalpine; red berries and red autumn. Occasional (mountain).
- **Erman's birch (dakekanba, Betula ermanii)**: Subalpine and tree-line birch (Fuji, Kiso heights). Occasional. Hook: bark tinder that burns wet.
- **Japanese white birch (shirakaba, Betula platyphylla var. japonica)**: Highland meadows and burned ground of Shinano (Kirigamine, Asama foothills, above Suwa). Occasional (Nakasendō highlands). Hook: bark tinder, white-trunk look.
- **Japanese cherry birch (mizume, Betula grossa)**: Mountain forest. Occasional. Hook: bows (azusa-yumi, verify).
- **Willows (yanagi, Salix spp.)**: River gravel bars and banks: kawayanagi (Salix gifuensis), nekoyanagi (pussy willow, S. gracilistyla), ōbayanagi; weeping willow (shidare-yanagi, S. babylonica) is planted along moats, canals and at crossings. Common. Hook: wicker baskets (yanagi-gōri), riverbank cover, fishing-rod shoots.
- **Japanese elm (harunire, Ulmus davidiana var. japonica)**: River flats in the mountains. Occasional. Hook: inner bark fibre for cord.
- **Chinese elm (akinire, Ulmus parvifolia)**: Lowland riversides, warm. Occasional.
- **Castor aralia (harigiri, Kalopanax septemlobus)**: Mountain forest; thorny young trunk. Occasional. Hook: edible shoots.
- **Ash (shioji Fraxinus platypoda, yachidamo F. mandshurica, aodamo F. lanuginosa)**: Mountain valley bottoms; aodamo is scrubby hill ash. Occasional. Hook: tool handles, bows (verify).
- **Amur cork tree (kihada, Phellodendron amurense)**: Mountain forest, Kiso and Ontake. Occasional. Hook: yellow inner bark = the bitter stomach medicine sold on the Nakasendō (Ontake's darani-suke, Kiso's hyakusōgan, verify dates); yellow dye.
- **Nurude sumac (nurude, Rhus javanica var. chinensis)**: Forest edges and clearings; red autumn. Common. Hook: leaf galls (fushi) give tannin for ohaguro tooth-blackening and black dye.
- **Lacquer tree (urushi)**: planted on field edges, bunds and hill plots; trunks scored in rows of horizontal cuts where summer sap is collected. Field/forest edge, occasional, large (tree) + tapping-scar decal. Hook: lacquer sap, seed wax, a tell; DANGER: contact rash if touched. (BL: lacquer tapper) Tapper's tub: W §11. {seam S018: N §C + R §3 + W §11}
- **Wild lacquer (yamaurushi, Toxicodendron trichocarpum)**: Hill and mountain forest edges; scarlet autumn. Common. Hook: hazard: contact rash.
- **Wax tree (haze / hazenoki)**: planted for vegetable candle wax (mokurō) in the warm south-west. Field, rare on our map, large (tree). `[off-map: Kyūshū, Shikoku for plantations]` Hook: wax. (BL: wax works) {seam S019: N §C + R §3}
- **Mallotus (akamegashiwa, Mallotus japonicus)**: Pioneer of clearings, road cuts, landslides and burnt ground. Common. Hook: leaves as food plates; bark medicine.
- **Harlequin glorybower (kusagi, Clerodendrum trichotomum)**: Clearings and edges; smelly leaves, blue berries. Common. Hook: berries give blue dye; young leaves eaten.
- **Silk tree (nemunoki, Albizia julibrissin)**: River banks and sunny edges; pink summer flowers, sleeps at night. Common. Hook: bark medicine.
- **Chinaberry (sendan / ōchi, Melia azedarach)**: Warm coast and villages. Occasional. Hook: medicine, insect repellent; the tree associated with displaying executed criminals' heads at the prison (verify).
- **Japanese hazel (hashibami, Corylus heterophylla var. thunbergii)**: Sunny grassland edges and burnt slopes. Occasional. Hook: edible nuts.
- **Witch hazel (mansaku, Hamamelis japonica)**: Mountain forest; yellow flowers in late winter. Occasional. Hook: flexible twigs for binding rafts and firewood bundles.
- **Wild mulberry (yamaguwa, Morus australis)**: Forest edges, riverbanks. Common. Hook: berries; wild silkworm fodder.
- **Japanese chestnut, wild (shibaguri, Castanea crenata)**: Hill forest and coppice. Common. Hook: nuts; rot-proof timber for sill beams (dodai) and pile posts. See D for orchard kuri.
- **Tree-of-heaven, pagoda tree, sophora**: `[outside 1680-1750: Meiji plantings]` except eniju (Styphnolobium japonicum), planted at temples since antiquity. Rare.

### == N §D Cherries, fruit and nut trees (wild and planted) ==

- **Hill cherry (yamazakura, Prunus jamasakura)**: Wild on hills everywhere; flowers open with red-brown new leaves. This, not Somei-yoshino, is the cherry of 1730 hanami. Common. Hook: spring landmark; bark for kabazaiku craft and medicine; wood for printing blocks.
- **Oshima cherry (ōshimazakura, Prunus speciosa)**: Izu peninsula and the Sagami coast; white flowers, green leaves. Occasional (coast). Hook: salted leaves wrap sakura-mochi (sold at Chōmeiji, Edo, from 1717, mem).
- **Fuji cherry (mamezakura / fujizakura, Prunus incisa)**: Small shrubby cherry native to Hakone, Fuji and Izu volcanic slopes. Common (Hakone) / landmark species for our terrain. Hook: small pale spring flowers on shrubs.
- **Kasumi cherry (kasumizakura, Prunus verecunda)**: Hill forest, slightly later than yamazakura. Occasional.
- **Sargent's cherry (ōyamazakura, Prunus sargentii)**: Mountain forest, Shinano highlands. Occasional (mountain).
- **Edo higan cherry (edohigan, Prunus spachiana)**: Long-lived, planted at temples and in villages; giant ancient specimens. Occasional / landmark. Hook: landmark ancient tree (Jindai-zakura, Yamanashi, reputed 2,000 years, mem).
- **Weeping cherry (shidarezakura, Prunus spachiana f. pendula)**: Temple and daimyo gardens, village landmarks. Rare / landmark.
- **Double garden cherries (satozakura / yaezakura cultivars)**: Temple grounds, daimyo gardens, Edo pleasure spots (Ueno, Asukayama planted by Yoshimune 1720, mem). Occasional (towns).
- **Somei-yoshino (Prunus × yedoensis)**: `[outside 1680-1750: bred c. 1840s–60s]`. Do not use.
- **Ume and plum grove (ume / ume-bayashi / baien)**: in every farm garden and temple, in groves for umeboshi (Soga and Odawara, next to Hakone), and as groves beside cherry and maple slopes in stroll gardens. Yard/field/garden, common, large (grove; `[terrain]` in gardens). Hook: umeboshi (food, travel ration), February landmark bloom. (BL: umeboshi works) {seam S013: N §D + R §3 + U Gardens: Stroll garden}
- **Peach (momo, Prunus persica)**: Farm gardens, small orchards. Occasional. Hook: fruit, Doll's Festival branches.
- **Apricot (anzu, Prunus armeniaca)**: Shinano villages (Mori, Kōshoku). Occasional (Nakasendō). Hook: fruit, seed medicine (verify local date).
- **Japanese plum (sumomo, Prunus salicina)**: Farm gardens. Occasional. Hook: fruit.
- **Japanese pear (nashi, Pyrus pyrifolia)**: Farm gardens and small orchards on trellis in Kantō (Kawasaki) and Echigo. Occasional. Hook: fruit.
- **Japanese crab apple (wakaringo, Malus asiatica)**: Rare garden fruit. Rare. Western apple is `[outside 1680-1750: Meiji]`.
- **Persimmon (kaki)**: at almost every farmhouse; astringent kinds dried as hoshigaki strung under the eaves, sweet ones eaten fresh; orange fruit on bare trees is the autumn village look. Yard, dominant (villages), large (tree). Hook: food (fresh, dried), kakishibu tannin for waterproofing paper, fans and nets, climbable. {seam S012: N §D + R §3}
- **Date plum (mamegaki, Diospyros lotus)**: Farm edges, grown for kakishibu. Occasional.
- **Chestnut, orchard (kuri)**: big-nut varieties in yards, farm orchards, field edges and hill plots (Tanba is famous). Yard/field, common, large. Hook: food (autumn), dried kachiguri. {seam S014: N §D + R §3}
- **Loquat (biwa, Eriobotrya japonica)**: Warm coast farm gardens, Izu and Suruga. Occasional (coast). Hook: fruit; leaves for medicinal tea (biwa-yōtō sellers).
- **Kishu mandarin (kishū mikan, Citrus kinokuni)**: Warm coastal slopes, Suruga and Sagami gardens. Occasional. Hook: fruit. The seedless unshū mikan existed but was avoided as "sonless" (mem); treat as rare.
- **Yuzu (yuzu, Citrus junos)**: Hill villages, Kantō and Tōkai. Occasional. Hook: fruit, winter-solstice bath.
- **Bitter orange (daidai, Citrus aurantium)**: Gardens. Occasional. Hook: New Year decoration.
- **Fig (ichijiku, Ficus carica)**: Garden tree brought in the 1600s via Nagasaki. Rare (verify).
- **Pomegranate (zakuro, Punica granatum)**: Temple and house gardens. Occasional. Hook: bark dye, polish mirrors with the fruit acid.
- **Jujube (natsume, Ziziphus jujuba)**: Farm gardens. Rare. Hook: fruit, medicine.
- **Kōshū grape (budō, Vitis vinifera 'Koshu')**: Grown on overhead trellis in Kai (Kōfu basin) for centuries. Rare (Kōshū-kaidō only). Hook: fruit. Trellis structure: rural agent.
- **Silverberry (natsugumi / akigumi, Elaeagnus spp.)**: Riverbanks and field edges, wild and planted. Common. Hook: tart red berries.

### == N §E Forest and vegetation types (stands; what a whole hillside looks like) ==

*These are not species but the mixes a map builder paints. Each one names its main trees.*
- **Sugi–hinoki plantation (uebayashi)**: even-aged close-planted rows on valley slopes near timber towns and rafting rivers (Ōme / Nishikawa for Edo, in era; Yoshino well under way by 1700 `[off-map: Yoshino]`). Forest, occasional in 1730 (planting spread through the 1700s), `[terrain]`. Hook: dense straight trunks, cover, dark floor. (verify spread elsewhere) {seam S011: N §E + W §8}
- **Natural Kiso hinoki forest under domain protection (tomeyama / sukiyama)**: Closed forest of hinoki, sawara, asunaro, nezuko and kōyamaki; villagers barred. Common in Kiso. Hook: the "forbidden forest" (patrols and guard posts: wilderness agent).
- **Coppice woodland (zōkibayashi, satoyama)**: Konara, kunugi, hornbeam and chestnut cut in patches on 15–20-year cycles, so the hill is a patchwork of ages from stumps to pole woods. Dominant (village hills). Hook: firewood, charcoal, clean raked floor.
- **Red pine open woodland (akamatsu-bayashi)**: Thin pines over grass, azalea and bare sandy soil on over-used hills. Dominant (dry village hills). Hook: matsutake, pine litter fuel, easy sight lines.
- **Bald / eroded hill (hageyama)**: hillside stripped for fuel and timber: bare granite sand, gullies, a few scrub pines. Common in Kinai and round pottery and salt towns; occasional on our map (Mikawa granite, Ōmi end of the Tōkaidō). Mountain, `[terrain]`. Hook: no cover, open ground, long view, landslide danger. (Totman; verify detail) {seam S010: N §E + W §8}
- **Grass-cutting commons (kusakari-ba / kaya-ba / magusa-ba)**: open hills of susuki and tall grass kept open by cutting and spring burning, for thatch (kaya), green manure (karishiki) and fodder, with bundle stacks; a big share of 1730 hill land (Sengokuhara, Fuji foothills). Commons/mountain, common, `[terrain]`. Hook: thatch, fodder, tall cover but none from above, open ground, fire danger in spring. (BL: Rural industry, thatch meadow) {seam S007: N §E + W §11 + R §3}
- **Shrine grove (chinju no mori)**: A relic patch of the old evergreen forest (shii, kashi, tabu, kusunoki, sugi, momi) around a village shrine; never cut. Common (one per village) / landmark in the plains. Hook: dense dark cover in otherwise open land; sacred, so no firewood (a rule hook).
- **Temple grove and cemetery trees**: Sugi, momi, ginkgo, shikimi, keyaki, weeping cherry. Common (per temple).
- *Farmstead windbreak (yashikirin)* → S004, under R §8.
- *Village bamboo grove (take-yabu)* → S005, under R §3.
- *Levee bamboo and willow (tsutsumi no yabu)* → S006, under R §1.
- **Roadside pine avenue (matsu-namiki)**: black pines planted in rows on both sides of the Tōkaidō on the plains and coast; cedar replaces pine on the Hakone mountain section, where pine failed. Roadside, common along the highway / landmark, large `[terrain]`. Hook: shade, navigation (the road seen from afar), cover. Trees: N; avenue layout: W/R/U. {seam S001: N §E + W §2}
- **Coastal pine shelterbelt (bōsa-rin / bōfū-rin)**: black pine planted on dunes behind beaches against sand and wind (Enshū coast; Niji-no-Matsubara at Karatsu, early 1600s, is the far model). Coast, common on sandy coast, large `[terrain]`. Hook: windbreak COVER, navigation. (verify local dates) {seam S003: N §E + W §19}
- **Laurel ravine forest**: Surviving evergreen oak, camphor and camellia in steep coastal ravines (Izu, Manazuru's Ohayashi, kept as a protected domain forest since the 1600s, mem). Occasional / landmark.
- **Beech–oak mountain forest (buna–mizunara)**: Tall grey beech, mizunara, maples, dwarf bamboo floor, above ~800 m. Dominant (mountains). Hook: beechnuts, bears, deep cover.
- **Fir–hemlock belt (momi–tsuga)**: Dark conifer ridges between the laurel and beech zones (Hakone, Tanzawa). Common. Hook: dark cover.
- **Subalpine conifer forest (shirabe–ōshirabiso)**: Dense dark fir with moss and lichen beards, Fuji 1,600–2,500 m, Ontake. Common (high). Hook: cold, dark, easy to get lost.
- **Tree-line birch and dwarf pine scrub**: Dakekanba, haimatsu, rowan. Rare on the map. Hook: exposure.
- **Lava-flow forest (Aokigahara type)**: Hinoki, tsuga, momi and moss on a young jagged lava field; roots over rock, no soil, compasses a myth. Landmark (Fuji north-west). Hook: disorientation, caves, no digging.
- **Riparian gallery (kawabe-rin)**: Willow, alder, walnut, wingnut, nemunoki along streams. Common. Hook: cover along water.
- **Secondary scrub (yabu)**: Tangles of kuzu, bramble, sumac, mallotus and bamboo grass on abandoned fields, landslides and burnt land. Common. Hook: slow movement, hiding, forage.
- **Swidden plot (yakihata / kirikae-bata)**: a mountain slope cleared and burned, cropped 2–4 years with soba, millet and beans, then left to regrow; often far from the village. Mountain villages (Kiso, Hida, Tanzawa type), occasional (common in those villages), `[terrain]`. Hook: open ground, charred stumps, ash ground, food in the forest. (BL: Dwellings, yakihata huts) {seam S008: N §E + W §8 + R §3}
- **Ash-buried farmland (Hōei sunafuri / suna-ume no hatake)**: fields east of Fuji (Gotemba, Oyama, Ashigara, Mikuriya) still buried or half-cleared under the 1707 black scoria, with dead stalks, broken fences, heaps of dug-out ash and silted rivers. Plain/foothill, common on the east flank (the abandoned-field form rare), `[terrain]`. Hook: ruined farmland, poor loot, a tell of disaster; 1730-specific. Dug heaps: W §12. {seam S009: N §E + W §12}

### == N §F Bamboo and dwarf bamboo ==

- **Madake / Japanese timber bamboo (madake, Phyllostachys bambusoides)**: The main village bamboo, groves behind houses and on levees, 10–20 m tall. Dominant (bamboo groves). Hook: poles for building, fences, ladders, water pipes (kakei), baskets, spears, shoots (bitter); the key building material.
- **Henon bamboo (hachiku, Phyllostachys nigra var. henonis)**: Groves in cooler places; fine whitish culms. Common. Hook: tea whisks, fine splits, sweet shoots.
- **Black bamboo (kurochiku, Phyllostachys nigra)**: Planted in gardens. Occasional. Hook: decorative fences.
- **Moso bamboo (mōsōchiku, Phyllostachys edulis)**: The fat bamboo of modern groves. Introduced to Satsuma in 1736 and spread later. `[outside 1680-1750: 1736 in Satsuma, central Honshu later]`. Do not use as the default grove.
- **Golden bamboo (hoteichiku, Phyllostachys aurea)**: Planted; knobbly bases. Occasional. Hook: fishing rods, walking sticks.
- **Arrow bamboo (yadake, Pseudosasa japonica)**: Thickets planted near samurai houses and wild on hills and coasts. Common. Hook: arrow shafts; screens.
- **Simon bamboo (medake / onna-dake, Pleioblastus simonii)**: River banks and gravel bars, dense 3–5 m thickets. Common (rivers). Hook: laths, flutes, fishing rods, cover.
- **Azuma-nezasa (azumanezasa, Pleioblastus chino)**: The low running bamboo grass of Kantō hills, fields edges and red-pine woods. Common (Kantō). Hook: ground cover [clutter].
- **Hakone bamboo (hakonedake, Pleioblastus chino var. vaginatus)**: The small bamboo of the Hakone slopes, named for them. Common (Hakone) (verify taxon). Hook: thin poles, woven work, ground cover.
- **Kuma-zasa (kumazasa, Sasa veitchii)**: Variegated-edged dwarf bamboo of shady mountain forest. Common. Hook: leaf wrappers (sushi, dango), cover [clutter].
- **Kuril bamboo (chishimazasa / nemagaridake, Sasa kurilensis)**: Snow country mountain slopes, bent at the base by snow; beech forest floor. Common (Kiso heights, snowy side) `[off-map mostly: Sea of Japan side]`. Hook: edible shoots; exhausting to walk through.
- **Miyako-zasa (miyakozasa, Sasa nipponica)**: Pacific-side beech and grass slopes, Fuji and Hakone. Common. Hook: ground cover.
- **Suzutake (suzutake, Sasamorpha borealis)**: Tall 1–2 m dwarf bamboo of mountain forest floors. Common (mountain). Hook: basket weaving (Kiso, Togakushi craft); impassable cover.
- **Bamboo flowering die-off (take no hana)**: Once in decades a whole stand of one species flowers and dies at once; seeds were eaten as famine food and fed rat plagues. Rare (event). Hook: dead brown grove variant, rats.
- **Bamboo shoot (takenoko)**: The spring shoots in groves. Common (April–June). Hook: food item, a harvest interaction.

### == N §G Shrubs ==

- **Mountain azalea (yamatsutsuji, Rhododendron kaempferi)**: Red-pine woods, grass slopes, forest edges; red flowers in May. Common. Hook: spring colour.
- **Three-leaf azalea (mitsubatsutsuji, Rhododendron dilatatum and allies)**: Hill forest, purple April flowers. Common.
- **Japanese azalea (rengetsutsuji, Rhododendron molle subsp. japonicum)**: Grassland and highland meadows (Kirigamine, Hakone grass slopes); orange flowers; cattle avoid it. Occasional. Hook: poisonous.
- **Garden azaleas (satsuki, kirishima-tsutsuji)**: Planted in gardens; Edo had an azalea craze around the 1690s (Itō Ihei's 1692 azalea book, mem). Occasional (towns).
- **Rhododendron (shakunage: azuma-shakunage R. degronianum, amagi-shakunage var. pentamerum)**: Rocky mountain ridges, Hakone and Amagi. Occasional. Hook: poisonous; ridge landmark.
- **Enkianthus (dōdantsutsuji E. perulatus, sarasadōdan E. campanulatus)**: Rocky hills and mountains; brilliant red autumn. Occasional.
- **Japanese andromeda (asebi, Pieris japonica)**: Dry hill forest and volcanic ground; Hakone has a lot. Common (Hakone). Hook: poisonous; boiled leaves as insecticide for crops and livestock lice.
- **Hydrangea, wild (gakuajisai, Hydrangea macrophylla f. normalis)**: Wild on the Sagami, Izu and Bōsō coast cliffs; the parent of the garden mophead (which also existed in Edo gardens). Common (coast). Hook: rainy-season colour.
- **Mountain hydrangea (yamaajisai, Hydrangea serrata)**: Stream sides in hill forest. Common. Hook: leaves for a sweet tea (amacha, Buddha's birthday).
- **Deutzia (utsugi / unohana, Deutzia crenata)**: Hedges, field edges, forest edges; white May flowers. Common. Hook: hollow stems; living hedge boundary.
- **Hakone weigela (hakone-utsugi, Weigela coraeensis)**: Coastal thickets (named for Hakone, though coastal). Common (coast). Hook: flowers change from white to red.
- **Weigela (tani-utsugi, Weigela hortensis)**: Snowy mountain slopes. Occasional (Nakasendō).
- **Kerria (yamabuki, Kerria japonica)**: Stream banks and damp forest edges; golden April flowers. Common. Hook: pith for lamp wicks (verify).
- **Bush clover (yamahagi, Lespedeza bicolor, and allies)**: Sunny grassland and red-pine woods; one of the seven autumn plants. Common. Hook: fodder, brooms, roof lining, fence wattle.
- **Nandina (nanten, Nandina domestica)**: Planted by the toilet and door of every house ("turn misfortune"); wild in warm woods. Common (villages). Hook: red berries, medicine for coughs.
- **Spotted laurel (aoki, Aucuba japonica)**: Shady forest floor, shrine groves. Common. Hook: leaves for burns.
- **Fatsia (yatsude, Fatsia japonica)**: Coastal and shady forest floor, planted by doors. Common. Hook: insecticide from leaves (verify).
- **Senryō (Sarcandra glabra), manryō (Ardisia crenata), yabukōji (Ardisia japonica)**: Low red-berried shrubs of shrine groves and warm forest. Common (groves). Hook: New Year decoration.
- **Japanese pepper (sanshō, Zanthoxylum piperitum)**: Forest edges and farm gardens. Common. Hook: spice (leaves, fruit), wood for pestles (surikogi), fish poison from bark.
- **Kuromoji (kuromoji, Lindera umbellata)**: Hill forest understorey. Common. Hook: aromatic toothpicks, oil.
- **Spicebush (danköbai Lindera obtusiloba, aburachan Lindera praecox)**: Hill forest. Occasional. Hook: aburachan seed oil for lamps.
- **Japanese quince (kusaboke, Chaenomeles japonica)**: Grass slopes and field edges. Occasional. Hook: fruit liquor, medicine.
- **Elderberry (niwatoko, Sambucus racemosa subsp. sieboldiana)**: Forest edges, village hedges. Common. Hook: "bone-setting tree" (setsukotsuboku): bark and wood for bruises and fractures.
- **Privet (ibota, Ligustrum obtusifolium)**: Hedges and scrub. Common. Hook: ibota wax (scale insects) for polishing and lubricating sliding doors.
- **Spindle trees (mayumi Euonymus hamiltonianus, nishikigi E. alatus)**: Forest edges; pink fruit, red autumn. Common. Hook: mayumi wood for bows (the name means "true bow").
- **Box (tsuge, Buxus microphylla var. japonica)**: Limestone and rocky hills; planted hedges. Occasional. Hook: combs, seals, shogi pieces.
- **Japanese holly (inutsuge, Ilex crenata)**: Wet hill and mountain forest; hedges. Common. Hook: hedging.
- **Longstalk holly (sōyogo, Ilex pedunculosa)**: Dry ridges with red pine. Common. Hook: firewood.
- **Dwarf yew (kyaraboku, Taxus cuspidata var. nana)**: Snowy subalpine. Rare.
- **Multiflora rose (noibara, Rosa multiflora)**: Riverbanks, field edges, grassland; thorny hedges. Common. Hook: hips for medicine; thorns as barrier.
*- **Brambles (momijiichigo Rubus palmatus, kusaichigo R. hirsutus, nawashiroichigo R. parvifolius, kumaichigo R. crataegifolius)**: Clearings, edges, road banks, burnt land. Common. Hook: berries (early summer food).*
- **Gardenia (kuchinashi, Gardenia jasminoides)**: Warm Tōkai woods and gardens. Occasional. Hook: yellow dye and food colouring.
- **Winter daphne (jinchōge, Daphne odora)**: Garden shrub. Occasional (towns).
- **Oriental paperbush (mitsumata, Edgeworthia chrysantha)**: Planted on hill plots for paper; see Q. Occasional.
- *Tea, wild or escaped (chanoki, Camellia sinensis)* → S015, under N §Q.
- **Aralia (taranoki, Aralia elata)**: Clearings, landslides, burnt land; thorny sticks. Common. Hook: tara-no-me shoots (spring food).
- **Aralia (udo, Aralia cordata)**: Forest edges; tall herb-shrub. Common. Hook: shoots (food).
- *Sumac, mallotus, kusagi*: pioneer shrubs; see C.
- *Silverberry (gumi)*: see D.

### == N §H Vines and climbers ==

- **Kudzu (kuzu, Pueraria montana var. lobata)**: Everywhere on edges, riverbanks and abandoned fields; smothers scrub. Dominant (edges). Hook: root starch (kuzuko, medicine kakkontō), vine fibre for kuzu-fu cloth (Kakegawa on the Tōkaidō was famous for it, mem), fodder, rope.
- **Japanese wisteria (fuji, Wisteria floribunda)**: and **silky wisteria (yamafuji, W. brachybotrys)**: Climbing forest edges and riverside trees; mauve May cascades. Common. Hook: vine fibre for rough cloth (fujifu) and rope; strong vine for binding.
- **Akebi (akebi Akebia quinata, mitsuba-akebi A. trifoliata)**: Forest edges and hedges. Common. Hook: sweet autumn fruit, vines for baskets.
- **Boston ivy (tsuta, Parthenocissus tricuspidata)**: Rocks, trees, walls; scarlet autumn. Common. Hook: sap was the old sweetener (amazura, verify).
- **Japanese ivy (kizuta, Hedera rhombea)**: Evergreen on trees and rocks. Common.
- **Oriental bittersweet (tsuruumemodoki, Celastrus orbiculatus)**: Forest edges. Common. Hook: orange berries.
- **Crimson glory vine (yamabudō, Vitis coignetiae)**: Mountain forest edges. Common (mountain). Hook: wild grapes, bark fibre.
- **Wild grape (ebizuru, Vitis ficifolia)**: Lowland edges. Common. Hook: small grapes.
- **Hardy kiwi (sarunashi, Actinidia arguta)**: Mountain forest. Occasional. Hook: fruit; tough vines (the Iya vine bridges use it, `[off-map: Shikoku]`).
- **Silver vine (matatabi, Actinidia polygama)**: Mountain stream sides; white-topped leaves in summer. Occasional. Hook: fruit medicine, cats go mad for it.
- **Kadsura (sanekazura, Kadsura japonica)**: Warm forest. Occasional. Hook: sticky stem sap as hair pomade (binankazura).
- **Japanese honeysuckle (suikazura, Lonicera japonica)**: Hedges and edges. Common. Hook: medicine (nindō).
- **Yam, wild (yamanoimo / jinenjo, Dioscorea japonica)**: Vine on forest edges; long tuber deep underground. Common. Hook: the prized digging food (tororo at Mariko on the Tōkaidō, mem).
- **Snake gourd (karasuuri, Trichosanthes cucumeroides)**: Hedges; red gourds hanging in winter. Common. Hook: root starch, seeds.
- **Clematis (senninsō, Clematis terniflora)**: Edges. Common. Hook: poisonous.
- **Star jasmine (teikakazura, Trachelospermum asiaticum)**: Climbing rocks and trees in warm forest. Common.
- **Japanese hop (kanamugura, Humulus japonicus)**: Waste ground and riverbanks, prickly. Common. Hook: nuisance cover.
- **Bushkiller (yabugarashi, Causonis japonica)**: Hedges and gardens. Common [clutter].

### == N §I Grasses, reeds, rushes, sedges ==

- **Japanese silver grass (susuki / obana / kaya, Miscanthus sinensis)**: Grass-cutting commons, burnt hills, road banks, volcanic slopes (Sengokuhara). Dominant (grassland). Hook: THE thatch grass (kaya), fodder, autumn plumes (one of the seven autumn plants), fire risk.
- **Amur silver grass (ogi, Miscanthus sacchariflorus)**: Wet river flats and levees, taller than susuki. Common (rivers). Hook: thatch, screens.
- **Hachijō silver grass (hachijōsusuki, Miscanthus condensatus)**: Coastal cliffs and Izu. Common (coast). Hook: thatch, cattle fodder.
- **Cogon grass (chigaya, Imperata cylindrica)**: Sunny dry banks, dikes, dunes. Common. Hook: thatch; the chi-no-wa purification ring at shrines; young flower spikes (tsubana) chewed as a sweet.
- **Themeda (karukaya, Themeda triandra var. japonica)**: Dry grass slopes. Common. Hook: thatch, brooms.
- **Kariyasu (kariyasu, Miscanthus tinctorius)**: Mountain grass slopes (Ibuki and the Nakasendō side). Occasional. Hook: yellow dye grass (verify range on our map).
- **Japanese lawn grass (shiba / noshiba, Zoysia japonica)**: Grazed and cut turf on dike tops, shrine lawns, headlands, horse pastures. Common. Hook: turf blocks cut to bind embankments and grave mounds [clutter].
- **Common reed (yoshi / ashi, Phragmites australis)**: Marshes, lake edges, estuaries, river flats (Naniwa reeds, Ashinoko shores). Dominant (wetland). Hook: yoshizu and sudare screens, thatch, fuel, reed-bed cover.
- **Wild rice (makomo, Zizania latifolia)**: Shallow ponds, lake margins, slow rivers. Common. Hook: mats and Bon festival horses; edible swollen shoots.
- **Cattail (gama Typha latifolia, himegama T. domingensis)**: Ponds, ditches, paddy-edge wetland. Common. Hook: pollen for wounds, fluff as stuffing and tinder, leaves for mats.
- **Soft rush (igusa, Juncus effusus var. decipiens)**: Wild in wet ground; grown in paddies for tatami covers. Common (wild). Hook: tatami facing, wicks. See Q for the crop.
- **Hat sedge (kasasuge, Carex dispermoides)**: Grown in wet fields for suge-gasa hats and mino capes. Occasional. Hook: rain gear material.
- **Sedges, misc. (suge, kayatsurigusa Cyperus, futoi Schoenoplectus, sankakui, hotarui)**: Wet paddy edges, marsh, pond margins. Common [clutter]. Hook: mats, cord.
- **Plantain (ōbako, Plantago asiatica)**: Trampled paths and roads. Common [clutter]. Hook: medicine (shazenshi).
- **Crab and goose grasses (mehishiba, ohishiba, enokorogusa foxtail)**: Field edges, roadsides, yards. Dominant (disturbed ground) [clutter].
- **Barnyard grass, wild (inubie / tainubie, Echinochloa)**: Paddy weed; cut green. Common [clutter]. See O for hie.
- *Bamboo grass (sasa)*: see F.
- **Mountain meadow grass mix (kōgen sōgen)**: Short grass with day lilies, orchids, gentians on Shinano highlands (Kirigamine, Utsukushigahara). Occasional (Nakasendō highlands). Hook: open grazing, horse pasture (maki).
- *Seashore sedges and grasses*: see N.

### == N §J Ferns, horsetails, clubmosses, mosses, lichens ==

- **Bracken (warabi, Pteridium aquilinum)**: Burnt slopes, grass-cutting commons, red-pine woods. Dominant (open hills). Hook: spring shoots (food), root starch (warabiko, famine and mochi), root fibre for rope (warabi-nawa).
- **Royal fern (zenmai, Osmunda japonica)**: Damp stream banks and forest edges. Common. Hook: dried shoots (food); fluff (zenmai-wata) spun into cloth.
- **Ostrich fern (kusasotetsu / kogomi, Matteuccia struthiopteris)**: Moist mountain valleys. Common (mountain). Hook: shoots (food).
- **Urajiro fern (urajiro, Gleichenia japonica)**: and **kosida (Dicranopteris pedata)**: Dense on sunny slopes of warm hills and cuttings. Common (warm hills). Hook: New Year decoration fronds; basket stems (kosida).
- **Autumn fern and wood ferns (benishida Dryopteris erythrosora, others)**: Forest floor everywhere. Dominant (forest floor) [clutter].
- **Holly fern (yabusotetsu, Cyrtomium fortunei)**: Stone walls, shrine groves, warm forest. Common.
- **Hare's-foot fern (shinobu, Davallia mariesii)**: On trees and rocks. Occasional. Hook: tsuri-shinobu hanging fern balls (an Edo summer decoration).
- **Roof fern (nokishinobu, Lepisorus thunbergianus)**: On old thatch, bark and stone walls. Common. Hook: weathering detail on thatch roofs and old trees.
- **Horsetail (sugina / tsukushi, Equisetum arvense)**: Dikes, field edges, riverbanks. Common [clutter]. Hook: spring tsukushi shoots (food).
- **Scouring rush (tokusa, Equisetum hyemale)**: Damp shade, planted by gardens. Occasional. Hook: dried stems used as fine sandpaper by carpenters, lacquerers, comb makers.
- **Rock spikemoss (iwahiba, Selaginella tamariscina)**: Dry cliff faces. Occasional.
- **Running clubmoss (hikagenokazura, Lycopodium clavatum)**: Mountain forest edges. Occasional. Hook: worn in Shinto rites; spores as flash powder (verify).
- **Haircap moss (sugigoke / ōsugigoke, Polytrichum)**: Forest floors, shrine grounds, damp banks. Common [clutter].
- **Carpet mosses (haigoke Hypnum plumaeforme, hosobaokinagoke Leucobryum)**: Stones, stone lanterns, roots, temple moss gardens. Dominant (shady ground). Hook: weathering layer; moss rolls sold for gardens.
- **Liverworts (zenigoke, jagoke)**: Wet stone, well sides, gutters, damp shade. Common. Hook: damp-texture decal.
- **Sphagnum (mizugoke, Sphagnum)**: Bogs (Sengokuhara moor, Kirigamine). Occasional. Hook: wound packing, tinder when dry (verify period use).
- **Beard lichen (saruogase, Usnea / Dolichousnea)**: Hanging from subalpine firs. Common (high forest). Hook: fog forest look; tinder.
- **Crustose and leafy lichens (chizugoke, umenokigoke)**: On rocks, stone lanterns, old roof tiles, ume bark. Common. Hook: weathering decal.

### == N §K Wild flowers and herbs (food, medicine, poison, famine food, look) ==

***The seven spring herbs (haru no nanakusa), eaten in rice gruel on 7th of the first month; all common field-edge plants [clutter]:***
- **Water dropwort (seri, Oenanthe javanica)**: Paddy ditches, stream edges. Common. Hook: food.
- **Shepherd's purse (nazuna, Capsella bursa-pastoris)**: Dry fields, roadsides. Common. Hook: food.
- **Cudweed (gogyō / hahakogusa, Pseudognaphalium affine)**: Fields. Common. Hook: food; old kusamochi herb.
- **Chickweed (hakobera, Stellaria media)**: Fields, gardens. Common. Hook: food, bird feed.
- **Nipplewort (hotokenoza, Lapsanastrum apogonoides)**: Winter paddies. Common. Hook: food.
- *Turnip greens (suzuna) and daikon greens (suzushiro)*: crops, see P.
***The seven autumn plants (aki no nanakusa); a grassland look:***
- *Bush clover (hagi)*: see G. **Silver grass (obana = susuki)**: see I. **Kudzu (kuzu)**: see H.
- **Fringed pink (kawaranadeshiko, Dianthus superbus var. longicalycinus)**: River gravel and sunny grassland. Common. Hook: autumn flowers.
- **Patrinia (ominaeshi, Patrinia scabiosifolia; otokoeshi P. villosa)**: Grassland. Common. Hook: yellow autumn flowers; root medicine.
- **Thoroughwort (fujibakama, Eupatorium japonicum)**: Riverbanks, wet meadows. Occasional. Hook: fragrant dried leaves (sachets).
- **Balloon flower (kikyō, Platycodon grandiflorus)**: Sunny grassland. Common (in grassland). Hook: root medicine for coughs.
***Others, food and useful:***
- **Mugwort (yomogi, Artemisia indica var. maximowiczii)**: Everywhere on banks, roadsides, clearings. Dominant (disturbed ground) [clutter]. Hook: moxa (mogusa) for moxibustion, kusamochi, bath herb, wound styptic. Moxa from Ibuki on the Nakasendō was famous (mem).
- **Butterbur (fuki, Petasites japonicus)**: Damp stream banks, shade near villages; huge leaves. Common. Hook: food (stalks, flower buds fuki-no-tō), leaf as an emergency umbrella or wrapper.
- **Japanese knotweed (itadori, Fallopia japonica)**: River gravel, road cuts, and bare volcanic ground; a pioneer at Ōwakudani-type sites. Common. Hook: sour edible shoots, root medicine.
- **Sorrel and dock (suiba Rumex acetosa, gishigishi R. japonicus)**: Field edges. Common [clutter]. Hook: food, dock root for skin disease.
- **Wild garlic (nobiru, Allium macrostemon)**: Dikes and banks. Common [clutter]. Hook: food.
- **Honewort (mitsuba, Cryptotaenia japonica)**: Damp forest edges. Common. Hook: food.
- **Myōga ginger (myōga, Zingiber mioga)**: Semi-wild in shade under village trees. Common (villages). Hook: food.
- **Day lily (yabukanzō, Hemerocallis fulva var. kwanso; nokanzō)**: Dikes, field edges. Common. Hook: edible buds and shoots.
- **Hosta (gibōshi / urui, Hosta montana and allies)**: Damp mountain slopes and stream sides. Common. Hook: edible shoots. Poisonous look-alike: baikeisō (below).
- **Golden-rayed lily (yamayuri, Lilium auratum)**: Hakone, Izu and Kantō hill grass and forest edges; huge fragrant July flowers. Common (Hakone) / landmark species for our terrain. Hook: edible bulb.
- **Tiger lily (oniyuri, Lilium lancifolium)**: Field edges, near villages (grown for bulbs). Common. Hook: bulb food.
- **Dogtooth violet (katakuri, Erythronium japonicum)**: Spring floor of deciduous mountain woods. Occasional. Hook: bulb starch (katakuriko).
- **Thistles (azami, Cirsium spp.)**: Grassland, roadsides. Common [clutter]. Hook: edible root (verify).
- **Wild chrysanthemums and asters (nogiku: yomena, nokongiku, ryūnōgiku, abura-giku)**: Autumn grass banks and forest edges. Common [clutter]. Hook: yomena greens; autumn colour.
- **Burnet (waremokō, Sanguisorba officinalis)**: Grassland. Common. Hook: root styptic.
*- **Iris (ayame Iris sanguinea in meadows; kakitsubata I. laevigata in wet ground; shaga I. japonica in shady woods)**: Common. Hook: early-summer colour. Cultivated hanashōbu displays are `[outside 1680-1750: late 18th–19th c.]`.*
- **Sweet flag (shōbu, Acorus calamus)**: Ditches and pond edges. Common. Hook: laid on roofs and put in the bath on the 5th of the 5th month (Boys' Day); medicine.
- **Chinese lantern (hōzuki, Physalis alkekengi)**: Grown in yards, escaped to edges. Occasional. Hook: medicine; orange lantern pods.
- **Gromwell (murasaki, Lithospermum erythrorhizon)**: Wild on the Musashino grass plain, the old purple dye plant of Edo (Edo-murasaki). Rare / landmark species. Hook: purple dye root.
- **Madder (akane, Rubia argyi)**: Hedges and edges. Common. Hook: red dye root.
- **Houttuynia (dokudami, Houttuynia cordata)**: Damp shade near houses, under eaves. Dominant (shady yards) [clutter]. Hook: jūyaku, "ten medicines": poultice for boils, tea.
- **Geranium (gennoshōko, Geranium thunbergii)**: Field edges and banks. Common [clutter]. Hook: the standard diarrhoea medicine ("proof of efficacy").
- **Swertia (senburi, Swertia japonica)**: Sunny grass slopes. Occasional. Hook: bitter stomach medicine.
- **Gentian (rindō, Gentiana scabra)**: Autumn grassland. Occasional. Hook: root stomach medicine.
- **Self-heal, plantain, dock, loosestrife and similar field herbs**: Common [clutter]. Hook: folk medicine.
- **Wasabi, wild (sawawasabi, Eutrema japonicum)**: Cold spring-fed mountain streams. Occasional. Hook: food. Cultivated wasabi: see P.
*- **Orchids (shunran Cymbidium goeringii; ebine Calanthe; sagisō Pecteilis radiata in wet meadows; sekkoku Dendrobium and fūran Vanda falcata on trees)**: Forest floors, rocks, trunks. Occasional / rare. Hook: collected for wealthy growers (fūran was a daimyo hobby).*
- **Pheasant's eye (fukujusō, Adonis ramosa)**: Mountain forest floor, flowers at New Year. Occasional. Hook: potted for New Year; poisonous.
- **Spring ephemerals (nirinsō Anemone flaccida, setsubunsō Eranthis pinnatifida)**: Deciduous woods. Common in spring [clutter]. Hook: nirinsō shoots eaten (confused with toxic torikabuto).
- **Asian skunk cabbage (mizubashō, Lysichiton camtschatcensis)**: Snowmelt bogs. Rare `[off-map mostly: Oze, north]`.
- **Day flower (tsuyukusa, Commelina communis)**: Damp roadsides and yards. Common [clutter]. Hook: blue dye for yūzen underdrawing (aobana, from Ōmi, mem).
***Poison and famine plants (a gameplay category of their own):***
- **Red spider lily (higanbana, Lycoris radiata)**: Planted on paddy dikes and around graves; red in late September. Common (paddy dikes, graveyards). Hook: poisonous bulb, eaten as famine food after long washing; keeps moles and mice off dikes; autumn landmark.
- **Aconite (torikabuto, Aconitum japonicum and allies)**: Mountain forest edges and meadows. Occasional. Hook: deadly poison (hunting and assassination lore); toxic look-alike of nirinsō.
- **Water hemlock (dokuzeri, Cicuta virosa)**: Marsh and ditches. Occasional. Hook: deadly look-alike of seri.
- **False hellebore (baikeisō, Veratrum)**: Damp mountain slopes. Occasional. Hook: toxic look-alike of gibōshi.
- **Scopolia (hashiridokoro, Scopolia japonica)**: Damp mountain woods. Occasional. Hook: poison that makes you run about (the name); anaesthetic ingredient.
- *Star anise, asebi, rengetsutsuji, yew seeds, clematis*: poisonous shrubs, see B, E, G.
- **Famine food set**: acorns, tochi nuts, warabi and kuzu starch, higanbana bulbs, ryōbu leaves, pine inner bark, bamboo seed. Hook: a famine-food crafting chain. The Kyōhō famine of 1732–33 (western Japan, mem) sits right on the anchor year.

### == N §L Mushrooms and fungi ==

- **Matsutake (matsutake, Tricholoma matsutake)**: Under red pine on dry, raked, poor hills; peaked because the hills were degraded. Common (autumn, red-pine hills). Hook: valuable food; rights were auctioned by villages.
- **Shiitake (shiitake, Lentinula edodes)**: Wild on dead shii, konara and kunugi; log cultivation had begun in Izu, Suruga and Bungo; an Izu forester was teaching shiitake cultivation in Utogi in 1744. Occasional. Hook: food, trade good; logs leaning in forest (structure: wilderness agent).
- **Hen-of-the-woods (maitake, Grifola frondosa)**: Base of old mizunara in beech forest. Rare. Hook: prized food.
- **Shimeji (honshimeji, Lyophyllum shimeji)**: Mixed pine-oak woods. Occasional. Hook: food.
- **Nameko (nameko, Pholiota microspora)**: Dead beech, snow country. Occasional (mountain). Hook: food.
- **Oyster mushroom (hiratake, Pleurotus ostreatus)**: Dead broadleaf logs. Common. Hook: food.
- **Wood ear (kikurage, Auricularia)**: Dead elder and broadleaf. Common. Hook: food.
- **Winter mushroom (enokitake, Flammulina velutipes)**: Enoki and other stumps in winter; brown wild form. Occasional. Hook: winter food.
- **Brick cap (kuritake, Hypholoma lateritium)**: Oak stumps, autumn. Common. Hook: food.
- **Pine truffle (shōro, Rhizopogon roseolus)**: Coastal black-pine sand, spring. Occasional (coast). Hook: food.
- **Reishi (mannentake, Ganoderma)**: Old stumps, rare. Rare. Hook: auspicious medicine.
- **Moonlight mushroom (tsukiyotake, Omphalotus japonicus)**: Dead beech in autumn; gills glow faint green at night. Occasional (beech forest). Hook: poisonous look-alike of hiratake/shiitake; night-glow landmark.
- **Fly agaric (benitengutake, Amanita muscaria)**: Birch and fir at altitude. Rare. Hook: poison.
- **Destroying angel (dokutsurutake, Amanita virosa)**: Mixed forests. Occasional. Hook: deadly.
- **Bracket fungi (sarunokoshikake, kawaratake Trametes)**: On old trunks and stumps. Common. Hook: tinder (verify), prop detail on logs.

### == N §M Water and wetland plants ==

- **Lotus (hasu; renkon-ta, hasu-ike)**: in temple ponds (Shinobazu at Ueno), castle moats, and lotus-root fields in wet lowland (Kinai, Owari). Pond/moat/field, common in ponds, occasional as fields, landmark at temple ponds, `[terrain]` + plants. Hook: renkon (food), seeds, leaves as wrappers, Buddhist symbol, summer bloom. (fields: verify period; moats: assumed) {seam S043: N §M + R §1 + U Gardens: Stroll garden + U Water: Moats}
- **Water caltrop (hishi, Trapa japonica)**: Ponds and moats. Common. Hook: edible nuts; spiky dried nuts as caltrops (makibishi, ninja lore).
- **Water shield (junsai, Brasenia schreberi)**: Clear ponds. Occasional. Hook: food.
- **Japanese pond lily (kōhone, Nuphar japonica)**: Shallow streams and ponds. Common. Hook: root medicine (sensotsu).
- **Water lily (hitsujigusa, Nymphaea tetragona)**: The only native water lily, small white. Occasional.
- **Arrowhead (omodaka, Sagittaria trifolia)**: Paddy weed, pond edges. Common [clutter]. Crop form kuwai: see P.
- **Duckweeds and floating ferns (ukikusa Spirodela, sanshōmo Salvinia natans, akaukikusa Azolla)**: Paddies, ditches, ponds. Common. Hook: green or red water-surface decal.
- **Water crowfoot (baikamo, Ranunculus nipponicus var. submersus)**: Only in cold, clear, spring-fed streams (the Fuji spring rivers at Mishima on the Tōkaidō). Rare / landmark. Hook: white flowers streaming in clear water.
- **Submerged weeds (kuromo Hydrilla, ebimo Potamogeton)**: Ponds, slow rivers, lakes. Common. Hook: underwater clutter; fertilizer (mo-tori, weed-gathering from boats).
- *Water dropwort, cattail, reeds, wild rice, rushes, sedges, sweet flag*: see I and K.
- **River-rock algae (kōke)**: Slimy film on stones of clear rivers; food of ayu. Common [terrain decal]. Hook: slippery footing.
- **Pond scum and green water (aomidoro)**: Stagnant ponds, rice paddies in summer. Common [terrain decal].

### == N §N Coast plants and seaweeds ==

- *Black pine (kuromatsu)*: see A. The coast's dominant tree.
- **Japanese cheesewood (tobera, Pittosporum tobira)**: Sea cliffs and dune edges; hedges. Common (coast). Hook: smelly branches hung at doors at setsubun.
- **Japanese spindle (masaki, Euonymus japonicus)**: Coastal rocks, hedges. Common (coast). Hook: hedging.
- **Yeddo hawthorn (sharinbai, Rhaphiolepis indica var. umbellata)**: Coastal rocks. Common (coast). Hook: bark dye.
- **Beach eurya (hamahisakaki, Eurya emarginata)**: Coastal scrub. Common (coast).
- **Hamabō hibiscus (hamabō, Hibiscus hamabo)**: Estuary mud edges. Rare. Hook: yellow summer flowers.
- **Beach vitex (hamagō, Vitex rotundifolia)**: Sand dunes, creeping. Common (dunes) [clutter]. Hook: fruit as pillow stuffing and medicine.
- **Beach morning glory (hamahirugao, Calystegia soldanella)**: Sand dunes. Common (dunes) [clutter].
- **Beach sedge (kōbōmugi, Carex kobomugi)**: Dunes. Dominant (dunes) [clutter]. Hook: brush fibre (fudekusa).
- **Glehnia (hamabōfū, Glehnia littoralis)**: Sand dunes. Occasional. Hook: edible shoots, medicine root.
- **Beach pea (hamaendō, Lathyrus japonicus)**: Dunes. Common [clutter].
- **Saltwort (okahijiki, Salsola komarovii)**: Upper beach sand. Occasional. Hook: food.
- **Crinum lily (hamayū, Crinum asiaticum var. japonicum)**: Warm sand beaches; its north-east limit is about the Izu, Miura and Bōsō coast. Occasional. Hook: summer flowers.
- **Seaside chrysanthemum (isogiku, Chrysanthemum pacificum)**: Cliff tops, Izu and Sagami. Common (cliffs).
- **Leopard plant (tsuwabuki, Farfugium japonicum)**: Sea cliffs and coastal forest floor; yellow autumn flowers. Common (coast). Hook: edible stalks, poultice.
- **Ashitaba (ashitaba, Angelica keiskei)**: Sea slopes of Izu, Miura, Bōsō and the Izu islands. Common (coast). Hook: food (famous regrowth), medicine.
- **Japanese rose (hamanasu, Rosa rugosa)**: Northern beaches `[off-map: north of Kantō]`. Rare.
- **Hachijō silver grass, camellia, ubame oak, tabunoki, Oshima cherry, bayberry, hydrangea**: coast plants listed in B, D, G, I.
- **Laver (nori, Pyropia tenera and wild iwanori)**: Wild on rocks; farmed on bamboo stakes in Edo Bay (Shinagawa, Ōmori) (farming structures: rural/urban agents). Common. Hook: food, trade.
- **Wakame (wakame, Undaria pinnatifida)**: Rocky shores. Common. Hook: food.
- **Hijiki (hijiki, Sargassum fusiforme)**: Low-tide rocks. Common. Hook: food.
- **Arame and kajime (Eisenia bicyclis, Ecklonia cava)**: Kelp forests off Izu and Sagami rocky coasts. Common. Hook: food, fertilizer, iodine ash (verify period use).
- **Agar weed (tengusa, Gelidium)**: Izu and Bōsō rocks; dived for. Common (Izu). Hook: tokoroten jelly; kanten (agar) was a Kyoto invention of the 1650s (mem).
- **Funori (funori, Gloiopeltis)**: Rocks. Common. Hook: glue for plaster, sizing cloth, washing hair; a building material link (shikkui binder).
- **Gulfweed (hondawara, Sargassum fulvellum)**: Rocky coast. Common. Hook: New Year decoration, fertilizer.
- **Sea lettuce and green laver (aosa, aonori)**: Estuaries, tidal flats. Common. Hook: food.
- **Eelgrass (amamo, Zostera marina)**: Sandy shallows and tidal flats. Common (bays). Hook: fertilizer, fish and shrimp habitat; cast-up drift lines.
- **Kombu (kombu)**: `[off-map: Hokkaidō]`. Traded dried only.
- **Drift seaweed and wrack line (uchiage kaisō)**: Seaweed thrown up on beaches after storms. Common [terrain decal]. Hook: gatherable fertilizer and food.

### == N §O Crops: grains (plants only; fields, dikes, racks and sheds are the rural agent's) ==

- *Paddy rice (ine, Oryza sativa, uruchi and mochi types)* → S020, under R §1.
- **Red rice (akagome / taitōmai, Oryza sativa, Champa type)**: Hardy, early, reddish rice sown in poor, flood-prone or newly opened wet land; common among poor farmers in the 17th–18th c. (mem, verify share). Occasional. Hook: poor-tier rice; reddish-bronze heads read differently.
- **Upland rice (okabo / rikutō)**: Dry fields on terraces and plateaus. Occasional. Hook: rice without paddies.
- *Barley (ōmugi, Hordeum vulgare) and naked barley (hadakamugi)* → S021, under R §3.
- *Wheat (komugi, Triticum aestivum)* → S021, under R §3.
- *Foxtail millet (awa, Setaria italica)* → S022, under R §3.
- *Japanese barnyard millet (hie, Echinochloa esculenta)* → S022, under R §3.
- *Proso millet (kibi, Panicum miliaceum)* → S022, under R §3.
- **Sorghum (takakibi / morokoshi, Sorghum bicolor)**: Tall field edges. Occasional. Hook: grain, brooms from heads.
- *Buckwheat (soba, Fagopyrum esculentum)* → S023, under R §3.
- **Job's tears (hatomugi / juzudama, Coix)**: Wet field edges; wild juzudama by ditches. Occasional. Hook: medicine, rosary beads.
- **Finger millet (shikokubie, Eleusine coracana)**: Mountain swiddens. Rare. Hook: famine grain.
- *Maize (tōmorokoshi / nanbankibi, Zea mays)* → S039, under R §3.

### == N §P Crops: vegetables, beans, tubers, spices ==

- *Soybean (daizu, Glycine max)* → S024, under R §3.
- *Azuki bean (azuki, Vigna angularis)* → S024, under R §3.
- *Cowpea (sasage, Vigna unguiculata)* → S025, under R §3.
- **Broad bean and pea (soramame, endō)**: Winter-spring gardens. Occasional. Hook: food.
- *Hyacinth / kidney bean (ingenmame)* → S025, under R §3.
- **Peanut (rakkasei)**: `[outside 1680-1750: brought early 1700s, grown seriously from Meiji]`. Rare.
- *Sesame (goma, Sesamum indicum)* → S031, under R §3.
- **Perilla (egoma, Perilla frutescens var. frutescens)**: Hill fields; the old lamp and waterproofing oil. Common (mountains). Hook: oil for lamps, oiled paper and umbrellas. **Shiso (shiso)**: gardens, red for umeboshi.
- *Daikon radish (daikon, Raphanus sativus)* → S026, under R §3.
- **Turnip (kabu, Brassica rapa)**: Cool fields; Kiso's sunki (salt-free turnip-leaf pickle). Common. Hook: food.
- *Komatsuna (komatsuna, Brassica rapa var. perviridis)* → S027, under R §3.
- **Nozawana (Brassica rapa)**: `[outside 1680-1750: tradition dates it to 1756]`. Rare.
- *Welsh onion (negi, Allium fistulosum)* → S028, under R §3.
- **Garlic, chives, rakkyō (ninniku, nira, rakkyō)**: Gardens. Common. Hook: food, medicine.
- **Eastern carrot (ninjin, Daucus carota, long red-purple Asian type)**: Gardens. Occasional. Hook: food.
- *Burdock (gobō, Arctium lappa)* → S029, under R §3.
- *Taro (satoimo, Colocasia esculenta)* → S030, under R §3.
- **Yam, cultivated (nagaimo / tsukuneimo, Dioscorea polystachya)**: Gardens, trellised. Occasional. Hook: food.
- *Sweet potato (satsumaimo, Ipomoea batatas)* → S038, under R §3.
- **Potato (jagaimo)**: Came c. 1600 via Nagasaki; minor. Rare (verify).
- *Konjac (konnyaku, Amorphophallus konjac)* → S037, under R §3.
- **Squash (kabocha / tōnasu, Cucurbita moschata)**: Gardens, on fences. Common. Hook: food.
- *Bottle gourd (hyōtan / yūgao, Lagenaria siceraria)* → S042, under R §3.
*- **Cucumber (kyūri), eggplant (nasu), white melon (shirouri), oriental melon (makuwauri), watermelon (suika), wax gourd (tōgan)**: Summer gardens. Common. Hook: food; eggplant the most common summer vegetable.*
- **Ginger (shōga)**: Gardens. Common. Hook: food, medicine.
- **Chilli (tōgarashi, Capsicum annuum)**: Gardens (Naitō tōgarashi grown at Shinjuku for Edo, mem). Common. Hook: spice; hung to dry.
- *Wasabi, cultivated (wasabi, Eutrema japonicum)* → S041, under R §3.
- **Arrowhead (kuwai, Sagittaria trifolia 'Caerulea')**: Wet fields near Edo. Occasional. Hook: New Year food.
- *Lotus root (renkon)*: see M (hasu).
- **Udo, forced (udo)**: Grown in dark pits in Musashino. Occasional. Hook: food.
- **Spinach (hōrensō), leaf lettuce (chisha), garland chrysanthemum (shungiku)**: Gardens. Occasional.
- **Chinese cabbage, cabbage, tomato, onion (hakusai, kyabetsu, tomato, tamanegi)**: `[outside 1680-1750: Meiji]`.
- *Korean ginseng (chōsen ninjin, Panax ginseng)* → S040, under R §3.

### == N §Q Crops: industrial and cash ==

- **Tea bushes (chanoki; aze-cha / kuro-cha)**: in 1730 tea grew as loose scattered bushes along bunds, field borders and hill plots, and gone wild at wood edges; not clipped rows (rows began at Makinohara, 1869). Suruga hill villages (Ashikubo, Honyama) and Uji. Field, common in Suruga / occasional elsewhere, small–medium. Hook: tea leaves (bancha for commoners), low cover, bush hedges. (BL: tea-firing sheds) Clipped rows: §6. {seam S015: N §Q + R §3 + N §G}
- **Mulberry (kuwa; kuwa-batake)**: pollarded low stumps for silkworms on dry river terraces, alluvial fans, field edges and small plots, spreading fast in Kōzuke, Shinano, Kai and Musashi; the big mulberry landscapes are later. Field, occasional (common in Nakasendō silk country), medium bushes. Hook: leaves for silkworms, berries, bark paper, cover. (assumed; verify) {seam S016: N §Q + R §3}
- *Cotton (wata, Gossypium arboreum)* → S033, under R §3.
- *Hemp (asa, Cannabis sativa)* → S035, under R §3.
- **Ramie (karamushi / choma, Boehmeria nivea)**: Field edges, semi-wild in villages. Occasional (Echigo fine cloth is `[off-map: Echigo]`). Hook: fibre.
- *Indigo (ai, Persicaria tinctoria)* → S034, under R §3.
- **Safflower (benibana, Carthamus tinctorius)**: Dewa is the main source `[off-map: Mogami]`; Musashi (Okegawa, on the Nakasendō) grew it too (verify start). Rare. Hook: red dye, rouge.
- *Rapeseed (natane / aburana, Brassica rapa var. oleifera)* → S032, under R §3.
- *Tobacco (tabako, Nicotiana tabacum)* → S036, under R §3.
- *Paper mulberry (kōzo, Broussonetia kazinoki × papyrifera)* → S017, under R §3.
- *Paperbush (mitsumata, Edgeworthia chrysantha)* → S017, under R §3.
- **Gampi (ganpi, Diplomorpha sikokiana)**: Wild only, dry hills; not cultivable. Occasional. Hook: fine washi.
- *Lacquer tree (urushi)*: see C. **Paulownia (kiri)**: see C.
- **Hemp palm (shuro, Trachycarpus fortunei)**: Planted near farmhouses and temples in Tōkai and Kinai. Common (warm villages). Hook: fibre for rope, brooms, mino rain capes; a strong "southern Japan" silhouette.
- *Rush, crop (igusa)* → S044, under R §1.
- *Hat sedge, crop (kasasuge)*: see I.
- **Sugar cane (satōkibi, Saccharum officinarum)**: Ryūkyū and Satsuma `[off-map]`; Yoshimune's mainland trials from the 1720s (mem). Rare. Hook: sugar.
- **Grass for fodder and green manure (magusa / karishiki)**: cut from the kusakariba (see E, I). Hook: the grass itself is the crop of the commons.

### == N §R Dead wood and plant debris (natural props) ==

- **Fallen log (taoreki), mossy**: Forest floors; rare in raked village woods, common in mountains. Common (mountain). Hook: firewood, cover, mushrooms.
- **Windthrow tangle (kaze-taore)**: Uprooted trees after a typhoon (nowaki), with root plates. Occasional. Hook: obstacle; firewood.
- **Snag / dead standing tree (kareki)**: Mountain and volcanic gas areas. Occasional. Hook: firewood, landmark.
- **Hollow ancient trunk**: Old keyaki, kusunoki, sugi. Rare / landmark. Hook: shelter, hidden cache.
- **Stump (kirikabu) and coppice stool**: Coppice woods (cut stumps sprouting). Common (satoyama). Hook: signals managed woodland. Cut stumps may belong to W.
- **Broken branches and deadfall (sodagi, eda)**: Forest floor. Common in mountain forest [clutter]. Hook: kindling.
- **Driftwood (ryūboku)**: River gravel bars and beaches after floods. Common. Hook: firewood.
- **Flood debris line**: Straw, branches, bamboo left in trees and on banks after a flood. Occasional. Hook: storytelling.
- **Leaf litter heaps**: Gathered for compost in village woods (the raking is human, the leaves are nature). Occasional. Hook: compost, fire.
- **Dead bamboo culms**: Fallen yellow culms in groves. Common (groves). Hook: poles, firewood.
- **Pine cones and needle litter**: Under red and black pine. Dominant (pine woods) [clutter]. Hook: kindling (the period gathered it as fuel).
- **Fallen chestnut burrs and acorns**: Under chestnut and oaks in autumn. Common [clutter]. Hook: gatherable food.
- **Fallen persimmons / ume / ginkgo fruit**: Under trees, seasonal. Common [clutter]. Hook: food; ginkgo smell.

### == N §S Ground surfaces and soils [terrain] ==

- **Kuroboku black volcanic soil (andosol)**: Black crumbly soil of the Fuji, Hakone and Asama foothills and the Kantō uplands; much of it formed under centuries of burnt grassland. Dominant (volcanic foothills) [terrain].
- **Kantō loam red clay (akatsuchi)**: Red-brown clay seen in road cuts, bluffs and dug ground across Musashi. Common [terrain]. Hook: wall mud, roof-tile clay nearby.
- **Hōei black scoria / ash cover (sunafuri)**: Loose black cinder over fields and slopes east of Fuji, often in dug heaps. Common (east flank) [terrain].
- *Paddy mud, flooded / drained / cracked* → S020, under R §1.
- **Dry field soil, tilled in ridges**: Upland fields. Common [terrain].
- *Swept earth (village and threshing yards)* → S046, under R §4.
- **Raked woodland floor**: Bare soil with a thin leaf layer and exposed roots; the 1730 satoyama floor. Dominant (village woods) [terrain].
- **Deep leaf litter**: Beech and oak mountain forest. Dominant (mountain) [terrain].
- **Cedar and cypress litter**: Reddish-brown needle-scale litter under plantations and shrine groves. Common [terrain].
- **Pine-needle floor**: Under red pine; sandy, bright. Common [terrain].
- **Moss carpet**: Shrine groves, subalpine forest, lava-flow forest, stream sides. Common [terrain].
- **Bamboo-grass floor (sasa)**: Knee- to head-high ground cover in beech forest. Dominant (mountain) [clutter/terrain].
- **Grass turf (shiba)**: Dike tops, pastures, shrine lawns. Common [terrain].
- **Tall grass meadow (susuki)**: Grass-cutting commons. Common [clutter/terrain].
- **Burnt grassland (yakihara)**: Black ground with fresh shoots after spring burning. Occasional (spring) [terrain].
- **Decomposed granite sand (masado)**: Pale gritty soil on granite hills, bald slopes and in Kiso. Common (granite areas) [terrain].
- **River gravel and cobble**: Braided river beds. Common [terrain].
- **River sand and silt flats**: Lower rivers, bars, flood deposits. Common [terrain].
- **Beach sand, dark grey volcanic (Sagami Bay, Shōnan)**: Common (Sagami coast) [terrain].
- **Beach sand, pale (Enshū-nada)**: Common (western Tōkaidō coast) [terrain].
- **Beach pebbles and cobbles (Odawara, Kōzu, Miho)**: Common [terrain].
- **Tidal mud flat (higata)**: Grey mud with channels and shells, Edo Bay. Common (bays) [terrain].
- **Salt-stained sand**: Around salt works (rural). Occasional [terrain].
- **Peat and bog surface**: Sengokuhara moor. Rare [terrain].
- **Sulphur-crusted ground**: Yellow-white crust, grey mud, no plants; fumarole fields. Rare / landmark [terrain].
- **Lava rock surface (yōgan)**: Jagged black-brown basalt, moss-covered where older. Occasional (Fuji) [terrain].
- **Frost heave (shimobashira)**: Needle ice lifting loam on winter mornings on the Kantō plain. Common (winter) [terrain decal].
- *Snow cover*: see Y.
- **Mud and puddles**: Rainy season. Common [terrain decal].

### == N §T Rock and landforms ==

*Rock types by area (for texture sets): Hakone, Izu and Fuji are volcanic (andesite, basalt, scoria, tuff); Kiso and the Mikawa/Owari hills are granite; Tanzawa has tuff and diorite; Chichibu has limestone and chert; the coastal plains are sand, gravel and loam. (mem)*
- **Andesite boulders and outcrops (anzangan)**: Hakone and Izu slopes, stream beds, caldera walls; the stone quarried as Komatsu-ishi at Manazuru and Izu-ishi for Edo castle (mem). Common (Hakone). Hook: cover, climbable; quarry sites are W.
- **Columnar-jointed andesite / basalt cliffs**: Lava flow edges, Izu coast (Jōgasaki), gorges. Occasional. Hook: landmark cliffs.
- **Granite boulders and slabs (kakōgan)**: Kiso river gorge and valley floors; smooth white-grey. Common (Kiso). Hook: cover; the Nezame-no-toko granite terraces (landmark, X).
- **River-rounded boulders**: Every mountain stream and torrent bed. Dominant (mountain streams). Hook: stepping stones, cover; the source of stone for walls and foundations.
- **Scree / talus slope (gareba, kuzure)**: Below cliffs and on steep volcanic slopes. Common (mountains) [terrain + placed rocks]. Hook: sliding footing.
- **Landslide scar (hōkai-chi / yama-kuzure)**: raw slope with fallen trees and a debris fan, frequent after typhoons and quakes (the 1703 Genroku quake hit Odawara and Sagami); sometimes a small Jizō for the buried. Mountain, common (with a Jizō: occasional), `[terrain]` + small. Hook: blocked road, DANGER (unstable ground), lore. {seam S048: N §T + W §18}
- **Cliff / crag (gake)**: Mountain sides and gorge walls. Common [terrain + rock models].
- **Rock overhang and shallow cave (iwaya / iwa-kage)**: gorges and cliff bases, used as shelters and shrines; the camp version has a soot-blackened roof, a fire ring and old straw from travellers, hunters and ascetics. Mountain, occasional, `[terrain]`. Hook: SHELTER, fire. {seam S049: N §T + W §3}
- **Lava tube cave (fūketsu, hyōketsu, tainai)**: wind and ice caves on Fuji's lava flows; "womb" caves (Funatsu, Yoshida tainai) crawled through by pilgrims, with a small shrine inside. Mountain/forest, occasional / landmark, `[terrain]`. Hook: cold SHELTER, ice, darkness, pilgrimage, landmark. (verify discovery dates; Funatsu is traditionally late 17th c.) {seam S050: N §T + W §6}
- **Limestone cave and karst**: Chichibu, Buko-san `[edge of map]`. Rare.
- *Sacred rock (iwakura) and paired rocks (meoto-iwa)* → S051, under W §7.
- **Potholes (ōketsu) and riverbed rock channels**: Gorge floors. Occasional. Hook: detail on river rock.
- **Gorge / ravine (kyōkoku, tani)**: Kiso, Hayakawa, Tenryū, Fuji river gorges. Common [terrain]. Hook: bridges and plank ways (W).
- **Mountain pass saddle (tōge)**: Hakone, Usui, Satta, Suzuka, Torii, Wada passes [terrain]. Common. Hook: checkpoint and tea-house sites (other agents).
- **Ridge and knife-edge crest (one)**: Mountains. Common [terrain].
- **Caldera rim and floor**: Hakone's double caldera with Ashinoko on the floor. Landmark [terrain].
- **Volcanic cones (Fuji, Hakone Kamiyama and Komagatake, Futagoyama, Ashitaka)**: Landmark [terrain].
- **Alluvial fan (senjōchi)**: Where mountain rivers reach the plain; dry gravel soil good for mulberry, poor for rice. Common [terrain].
- **River terraces (dankyū)**: Step benches along big rivers (Sagami, Tama); villages on the steps. Common [terrain].
- **Natural levees and back marsh (shizen teibō, hainshitchi)**: Low ridges beside lowland rivers, wet ground behind; villages on levees, paddies behind. Common [terrain].
- **Floodplain, oxbows and old channels**: Lowland rivers. Common [terrain].
- **Delta and river mouth sandbars**: Where rivers meet the sea. Common [terrain].
- **Sand dunes (sakyū)**: Enshū-nada (Nakatajima), Sagami coast. Common (sandy coast) [terrain].
- **Raised beach terraces (kaigan dankyū)**: Uplifted benches on the Sagami, Miura and Bōsō coasts (lifted again in 1703, mem). Occasional [terrain].
- **Isolated hill (kotokuyama / ukiyama)**: Small wooded hills rising from paddy plains, often with a shrine grove. Common [terrain].
- **Stone for building, natural sources**: Riverbed cobbles, fieldstone cleared from fields (heaped at field edges), outcrops. Common. Hook: stone gathering; quarries are W.
- **Clay banks**: River cut banks and hill slopes with exposed clay. Occasional. Hook: clay for walls, tiles, kilns (industries: BUILDING_LIST).

### == N §U Rivers, springs, lakes and wetland water ==

- **Mountain torrent (keiryū)**: Boulder-choked, white water, deep pools (fuchi) and rapids (se). Common (mountains). Hook: drinkable water, fish (iwana, yamame), hard crossing.
- **Braided gravel river (Ōi, Tenryū, Fuji, Sakawa, Abe, Sagami)**: Wide stony beds with several shifting channels; the Tōkaidō forded the Ōi on porters' shoulders because bridges were forbidden. Common (Tōkaidō) / landmark (Ōi). Hook: fordable at low water, deadly in flood; the Sakawa was choked with Hōei ash in 1730.
- **Meandering lowland river (Tama, Sumida lower, Tone)**: Slow, levee-banked, reed-edged. Common (plains). Hook: ferry crossings (W), fishing, reeds.
- **Paddy-plain creek (ogawa)**: Small natural stream winding through paddies before it is channelled. Common. Hook: loach and minnow fishing, water. (Irrigation canals: R.)
- **Waterfall, plunge (baku)**: Single drop into a pool (e.g. Hakone's Tamadare and Hayakawa falls, Kiso falls). Common (mountains) / landmark. Hook: water, ascetic training spot (takigyō kit: BUILDING/W).
- **Waterfall, veil (Shiraito type)**: Many threads of spring water pouring from a cliff face. Landmark.
- **Cascade and rapids**: Mountain rivers. Common.
- **Deep pool (fuchi)**: Below falls and bends. Common. Hook: swimming, fish, legends (kappa, nushi).
- *Spring (yūsui / wakimizu)* → S047, under R §2.
- **Seep and mossy trickle (shimizu)**: Roadside rock faces and cuttings. Common. Hook: drink water on the road.
- **Cold volcanic spring river**: Clear, cold, even-temperature, with baikamo. Rare / landmark (Mishima).
- **Caldera lake (Ashinoko)**: Deep, cold, ringed by forest, with Fuji reflected; the Hakone checkpoint on its shore; a submerged forest of old trees ("sakasa-sugi") is known (verify Edo-era visibility). Landmark. Hook: boats, fishing, water.
- **Fuji five lakes (Kawaguchi, Yamanaka, Sai, Shōji, Motosu)**: Lava-dammed lakes on Fuji's north side. Landmark (if the map reaches).
- **Lake Suwa (Suwako)**: Shallow basin lake on the Nakasendō/Kōshū junction; freezes in winter with the omiwatari ice ridge that Suwa shrine records every year. Landmark. Hook: winter ice crossing, fishing.
- **Lake Hamana (Hamanako)**: Brackish lagoon opened to the sea by the 1498 quake; the Arai checkpoint and ferry. Landmark (Tōkaidō). Hook: brackish fish, oysters, ferry.
- **Lake Biwa (Biwako)**: `[edge of map: Ōmi]`. Landmark.
- **Natural pond (ike, numa)**: Hollows on terraces and in marsh. Common. Hook: water, lotus, ducks. (Irrigation ponds tameike are R.)
- **Marsh / reed swamp (numa, ashihara)**: Lake edges, back marsh, estuaries. Common (lowland). Hook: reeds, birds, hiding, slow going.
- **Moor / bog (shitsugen)**: Sengokuhara (Hakone), Kirigamine. Occasional / landmark. Hook: bog plants, wet ground.
- **Estuary (kakō)**: Brackish reed beds and mud at river mouths. Common (coast).
- **Frozen water**: Ice on ponds and Suwa, icicles on cliffs and eaves, frozen falls in Kiso. Seasonal (see Y).
- **Flood water**: Muddy brown, spread over paddies; frequent on the Sakawa and big rivers. Occasional (event).
- **Water colour set**: clear mountain, jade pool, muddy flood, peat-brown bog, rust-red iron spring, milky sulphur hot spring. Hook: shader variants.

### == N §V Volcanic and geothermal ==

- **Fumarole valley, Ōjigoku / Jigokudani (now Ōwakudani)**: The steaming, sulphur-yellow explosion crater on Hakone's Kamiyama; called Jigokudani or Ōjigoku ("great hell") in the Edo period, renamed Ōwakudani only in 1873. Landmark. Hook: danger (gas, scalding ground), a hell-landscape pilgrimage spot. Use the Edo name.
- **Steam vent / fumarole (funkiko)**: Hissing white steam from cracks and rubble. Common within geothermal fields. Hook: particle effect; warmth; damage if too close.
- **Solfatara crust and sulphur crystals (iō)**: Yellow crust around vents. Common in fields. Hook: sulphur (gunpowder, matches, medicine); gathering it is a W/R industry (verify Hakone Edo extraction).
- **Boiling mud pot (dorotō)**: Grey bubbling pools. Occasional. Hook: danger.
- **Boiling spring and hot stream**: Steaming water running in stream beds below vent fields. Occasional. Hook: danger and warmth.
- **Natural hot spring source (gensen)**: Hot water issuing at river level, e.g. along the Hayakawa at Yumoto and the other Hakone Seven Hot Springs (Yumoto, Tōnosawa, Miyanoshita, Dōgashima, Sokokura, Kiga, Ashinoyu). Landmark cluster. Hook: warmth, healing; the bath buildings are BUILDING_LIST §2.14 and the onsen town inn. (mem)
- **Hot spring deposits (yunohana, travertine, iron-red staining)**: White or orange crust where hot water runs. Occasional. Hook: bath salts (verify period trade).
- **Gas hollow (gasu-damari)**: Low spots near vents where gas pools; dead birds and insects. Rare. Hook: invisible danger zone.
- **Dead and stunted trees in vent fields**: Bleached snags, dwarfed pines, knotweed and grass as pioneers. Common in geothermal fields. Hook: visual boundary of danger.
- **Hōei crater and fresh scoria field (Hōei-zan)**: The 1707 vent on Fuji's south-east flank, bare black cinder slopes still almost unvegetated in 1730. Landmark.
- **Young lava flow, bare**: Black jagged rock with lichens (Fuji's younger flows). Occasional. Hook: hard going.
- *Old lava flow, forested*: see E (Aokigahara).
- **Pumice and scoria gravel**: Loose light rock on volcanic slopes. Common (volcanic) [terrain].
- **Volcanic bombs and blocks**: Scattered big rocks around craters. Occasional. Hook: cover.
- **Smoking volcano on the horizon (Asama)**: Asama was active through the 1700s (its great eruption is `[outside 1680-1750: 1783]`). Landmark (skybox). (mem)
- **Mount Fuji snowcap and summit crater**: Skybox or far terrain; snow from about October to June, a bare dark cone in late summer. Landmark.

### == N §W Coast landforms ==

- **Sand beach (sunahama)**: Sagami Bay (dark grey), Enshū-nada (pale), long and straight. Common [terrain]. Hook: sand, shellfish, drift.
- **Pebble / cobble beach (jarihama)**: Odawara, Kōzu, Miho; steep and noisy. Common [terrain].
- **Rocky shore with tide pools (isobe)**: Manazuru, Izu, Miura. Common (rocky coast). Hook: shellfish, seaweed, sea urchins, octopus.
- **Sea cliff (kaigai)**: Izu, Satta (the Tōkaidō squeezed along cliff foot at Satta, a known danger point). Common / landmark (Satta). Hook: waves, rockfall.
- **Sea stack, arch, sea cave (hanare-iwa, dōmon, dōkutsu)**: Izu and Miura coasts. Occasional / landmark.
- **Wave-cut bench (hamaishi)**: Flat rock platforms exposed at low tide, raised by quakes (Jōgashima, Miura). Occasional.
- **Tidal flat (higata)**: Edo Bay (Shinagawa, Fukagawa); clam digging in spring (shiohigari). Common (bays). Hook: clams, crabs, walking at low tide.
- **Salt marsh and brackish reed bed**: Bay edges, river mouths. Common.
- **Spit (sasu)**: Miho no Matsubara, a pine-covered gravel spit on Suruga Bay. Landmark.
- **Tombolo (rikukei sasu)**: Enoshima joined to the shore by a sand bar walkable at low tide. Landmark.
- **Dune coast with pine belt**: Enshū-nada. Common.
- **Offshore islands (Hatsushima, Enoshima, Izu islands on the horizon)**: Landmark / skybox.
- **Shore drift line**: Seaweed, driftwood, shells. Common [terrain decal].

### == N §X Named natural landmarks (candidates; the map may hold only some) ==

- **Mount Fuji with the Hōei crater**: Skybox or terrain. Landmark.
- **Hakone caldera, Ashinoko, Kamiyama and Komagatake**: Landmark (our test terrain).
- **Ōjigoku / Jigokudani fumarole valley**: Landmark.
- **Sengokuhara susuki grassland and moor**: Landmark (Hakone).
- *Hakone cedar avenue (planted 1618) on the old Tōkaidō* → S002, under W §2.
- **Hakone's Seven Hot Springs along the Hayakawa**: Landmark cluster.
- **Manazuru peninsula laurel forest and rocks**: Landmark (coast).
- **Great camphor of Kinomiya shrine, Atami**: Landmark tree.
- **Shiraito falls (Fuji)**: Landmark.
- **Oshino Hakkai springs and the Mishima (Kakita) springs**: Landmarks.
- **Aokigahara lava forest and caves**: Landmark.
- **Miho no Matsubara pine spit (the Hagoromo pine)**: Landmark.
- **Enoshima tombolo island**: Landmark.
- **Satta pass sea cliffs**: Landmark.
- **Ōi river's broad unbridged bed**: Landmark.
- **Lake Hamana and its sea gap**: Landmark.
- **Kiso valley gorge and Nezame-no-toko granite terraces**: Landmark (Nakasendō).
- **Kiso hinoki forbidden forest**: Landmark zone.
- **Lake Suwa (winter omiwatari)**: Landmark.
- **Usui pass and Asama on the skyline**: Landmark.
- **Mount Ontake (Kiso pilgrim mountain)**: Landmark / skybox.
- **Tanzawa and Ōyama (Afuri) mountain**: Landmark / skybox (Ōyama pilgrimage was huge in Edo).
- **Jindai-zakura (Yamataka, Kai), ancient edohigan cherry**: Landmark tree (if the map reaches Kai).
- *Ichirizuka enoki trees* → S054, under W §1.

### == N §Y Seasons and weather variants (only where they change which models are needed) ==

- **Sakura bloom (late March–April)**: Flower variants of yamazakura (pink-white with red-brown leaves), edohigan and shidarezakura, Oshima (white with green leaves), Fuji cherry. Needs: bloom model or texture set, petal-fall particles, petal ground decal.
- **Ume bloom (February)**: White and pink ume on bare branches. Needs: bloom texture.
- **Spring yellow and green**: Rapeseed fields yellow, barley green-gold, new leaves pale green, wisteria mauve, azalea red, kerria gold. Needs: crop stage variants.
- **Flooded paddies (May–June)**: Mirror water, seedlings in rows. Needs: paddy water state + seedling clutter.
- **Rainy season (tsuyu, June–July)**: Hydrangea, iris, mud, mist. Needs: weather only, plus hydrangea flower variant.
- **High summer**: Tall green rice, dense kuzu, cicada sound, thunderstorms. Needs: rice growth stage.
- **Autumn momiji (late October–November; earlier in the mountains)**: Red maples, yellow itayakaede and ginkgo, orange zelkova and cherry, red sumac and enkianthus, gold larch high up. Needs: autumn texture sets for every deciduous tree model; this is the biggest seasonal asset job.
- **Harvest (September–October)**: Gold rice heads, red higanbana on dikes, susuki plumes, persimmons orange on trees, chestnut burrs. Needs: rice gold stage, plume variant of susuki, fruit-on-tree variants.
- **After harvest**: Stubble paddies, rice drying on hasa racks (rural), barley sown in drained fields. Needs: stubble clutter.
- **Winter, Pacific side (Tōkaidō)**: Dry, sunny, frost and needle ice, bare deciduous trees, evergreens dark; camellias in flower; little snow in the lowlands. Needs: bare-branch variants of all deciduous trees.
- **Winter, snow country (Kiso, Usui, Hakone heights, Fuji)**: 0.5–1 m+ snow, snow-loaded sugi and hinoki, icicles, frozen falls, bamboo bent under snow, Suwa frozen. Needs: snow-laden conifer variants, snow terrain, icicle props.
- **Hakone fog (kiri)**: Frequent dense fog on the pass and caldera. Needs: weather preset only.
- **Typhoon aftermath (nowaki)**: Windthrow, snapped bamboo, flooded rivers, debris. Needs: fallen-tree and debris props (R).
- **Spring grass burning (noyaki / yamayaki)**: Black burnt slopes and smoke in early spring on grass commons. Needs: burnt terrain texture, smoke.
- **Volcanic haze**: Rare; after Hōei the sky was dark for weeks (1707) but not in 1730. Needs: nothing by default.
*Format: `name (romaji, Latin)`: habitat. Role: hunt / food / danger / pest / none.*

### == N Fauna: Mammals ==

- **Sika deer (shika / nihonjika, Cervus nippon)**: Forests and grass commons everywhere; crop raider. Role: hunt, food, hide, antler. Common.
- **Wild boar (inoshishi, Sus scrofa leucomystax)**: Lowland and hill forest, raids fields; villages built long boar walls (shishigaki). Role: hunt, food ("mountain whale"), danger when cornered, crop pest. Common.
- **Asian black bear (tsukinowaguma, Ursus thibetanus japonicus)**: Beech and oak mountain forest. Role: hunt (bear gall bladder = valuable medicine), danger. Occasional.
- **Japanese serow (kamoshika, Capricornis crispus)**: Steep rocky mountain forest. Role: hunt, food, hide. Occasional.
- **Japanese macaque (nihonzaru, Macaca fuscata)**: Mountain and hill forest, raids fields; Hakone troops. Role: pest, minor danger (steals). Common.
- **Honshū wolf (ōkami / yamainu, Canis lupus hodophilax)**: Mountains and forest edges; still widespread in 1730, revered as a crop guardian (shrines at Mitsumine, Ōyama) and feared. Rabies reached Japan in 1732 (Nagasaki) and later spread to wolves, making them man-eaters. Role: danger (rabid wolves are an in-period threat right after 1730), hunt. Occasional.
- **Red fox (kitsune, Vulpes vulpes japonica)**: Fields, woods, villages; Inari messenger. Role: fur, minor pest (chickens). Common.
- **Raccoon dog (tanuki, Nyctereutes procyonoides viverrinus)**: Village woods and edges. Role: hunt (tanuki soup, fur for brushes). Common.
- **Japanese badger (anaguma / mujina, Meles anakuma)**: Hill forest. Role: hunt, food, fat. Common.
- **Japanese hare (nousagi, Lepus brachyurus)**: Grassland, fields, forest edges. Role: hunt, food. Common.
- **Japanese marten (ten, Martes melampus)**: Forest. Role: fur. Occasional.
- **Japanese weasel (itachi, Mustela itatsi)**: Rivers, fields, villages. Role: fur, poultry pest. Common.
- **Stoat (okojo, Mustela erminea)**: Subalpine. Role: none. Rare.
- **Japanese river otter (kawauso, Lutra nippon)**: Rivers, lakes and coasts, still common in 1730. Role: fur, fish-stealer. Common.
- **Giant flying squirrel (musasabi, Petaurista leucogenys)**: Shrine groves and big-tree forest. Role: fur, none. Common.
- **Japanese squirrel and dwarf flying squirrel (nihonrisu, momonga)**: Forest. Role: none. Common.
- **Moles, shrews, voles, field mice, rats (mogura, nezumi)**: Everywhere. Role: pest (rice stores, dikes). Dominant.
- **Bats (kōmori)**: Caves, roofs. Role: none. Common.
- **Japanese sea lion (ashika, Zalophus japonicus)**: Rocky coasts and islands incl. Izu and Sagami; now extinct. Role: hunt (oil). Occasional (coast).
- **Whales and dolphins (kujira, iruka)**: Sagami and Suruga bays; drive hunts in Izu (verify). Role: food, oil, strandings. Occasional.
- **Domestic animals (horses, oxen, dogs, cats, chickens)**: Villages and roads. Cross-reference: rural and urban agents.

### == N Fauna: Birds ==

- **Green pheasant (kiji, Phasianus versicolor)**: Grassland, field edges. Role: hunt, food. Common.
- **Copper pheasant (yamadori, Syrmaticus soemmerringii)**: Mountain forest. Role: hunt, food. Occasional.
- **Japanese quail (uzura, Coturnix japonica)**: Grassland and fields; also kept as songbirds. Role: hunt, food. Common.
- **Ducks (kamo: mallard, spot-billed, teal), geese (gan), swans (hakuchō)**: Paddies, marsh, lakes in winter. Role: hunt, food (duck netting). Common (winter).
- **Cranes (tsuru: manazuru, nabezuru, tanchō)**: Wintered on Kantō paddies; shogunal crane hunts (tsuru-nari) near Edo. Role: protected prey (shogun's), food for lords. Occasional (winter).
- **Crested ibis (toki, Nipponia nippon)**: Paddies and forest edges across Honshū; common then, a paddy pest. Role: pest, feathers. Common.
- **Oriental stork (kōnotori, Ciconia boyciana)**: Paddies and marsh, nesting in big trees. Role: none. Occasional.
- **Herons and egrets (sagi)**: Paddies, rivers, marsh. Role: none. Common.
- **Cormorants (u)**: Rivers and coasts; used for ukai fishing on the Nagara (Gifu). Role: fishing tool. Common.
- **Black kite (tobi)**: Everywhere, towns and coast. Role: scavenger, snatches food. Dominant.
- **Hawks and eagles (taka: goshawk ōtaka, sparrowhawk, hawk-eagle kumataka, golden eagle inuwashi)**: Forest and mountain; falconry revived by Yoshimune (1716–). Role: falconry, protected hunting grounds. Occasional.
- **Owls (fukurō, mimizuku)**: Shrine groves, forest. Role: none; omens. Common.
- **Crows (karasu: hashibuto, hashiboso)**: Everywhere. Role: pest, scavenger (execution grounds, battlefields). Dominant.
- **Tree sparrow (suzume)**: Villages and paddies. Role: rice pest (scarecrows, clappers). Dominant.
*- **Songbirds (uguisu warbler, hototogisu cuckoo, hibari skylark, mejiro white-eye, hiyodori bulbul, tsubame swallow, kawasemi kingfisher, kitsutsuki woodpeckers)**: Season and habitat markers. Role: none (ambience), some kept caged. Common.*
- **Japanese green pigeon (aobato)**: and **turtle dove (kijibato)**: Forest; aobato drinks seawater at Ōiso's rocks (mem). Role: hunt, food. Common.
- **Gulls and shorebirds (kamome, chidori, shigi)**: Coast, tidal flats. Role: none. Common.
- **Rock ptarmigan (raichō)**: Alpine peaks only. Rare `[edge of map]`.

### == N Fauna: Reptiles, amphibians, invertebrates ==

- **Mamushi pit viper (mamushi, Gloydius blomhoffii)**: Grass, stream sides, stone walls. Role: DANGER (venomous); also eaten and steeped in sake as medicine. Common.
- **Tiger keelback (yamakagashi, Rhabdophis tigrinus)**: Paddies and streams. Role: danger (venomous, but thought harmless in the period). Common.
- **Japanese rat snake (aodaishō)**: Villages, farmhouse roofs, kura (eats rats; a house guardian). Role: none. Common.
- **Frogs, toads, newts (kaeru, hikigaeru, imori)**: Paddies, ponds. Role: sound ambience, medicine (toad venom). Dominant.
- **Japanese giant salamander (ōsanshōuo)**: Clear rivers of western Honshū, east to Gifu. Role: food. Rare `[edge of map]`.
- **Turtles (ishigame, suppon soft-shell)**: Ponds, rivers. Role: food (suppon). Common.
- **Giant hornet (ōsuzumebachi)**: Forest and edges, autumn. Role: DANGER; larvae eaten. Common.
- **Mountain leech (yamabiru)**: Wet mountain forest (Tanzawa). Role: nuisance. Occasional.
- **Mosquitoes, ticks, fleas, lice**: Everywhere. Role: nuisance, disease. Dominant.
- **Fireflies (hotaru)**: Clean streams and paddies in June. Role: ambience. Common.
- **Cicadas, crickets, dragonflies**: Seasonal sound. Role: ambience. Dominant.
- **Locusts and rice planthoppers (unka)**: Paddies; the 1732 Kyōhō famine was a planthopper plague (western Japan). Role: crop pest. Common. (mem)
- **Honeybee (nihon-mitsubachi)**: Log hives in mountain villages. Role: honey, wax. Occasional.
- **Silkworm (kaiko)**: Domestic; see Q. **Freshwater crab (sawagani)**: mountain streams. Role: food. Common.

### == N Fauna: Freshwater fish ==

- **Sweetfish (ayu, Plecoglossus altivelis)**: Clear rivers (Sagami, Tama, Kiso, Nagara), summer. Role: food, prized. Common.
- **Char and trout (iwana, yamame, amago)**: Cold mountain streams; amago west of Hakone, yamame east (mem). Role: food. Common (mountain).
- *Carp (koi, drab food carp) and crucian carp (funa)* → S055, under U Gardens: Garden fauna and small living features.
- **Loach (dojō)**: Paddies, ditches. Role: food (cheap). Dominant.
- **Eel (unagi)**: Rivers, lakes, estuaries. Role: food (kabayaki was already Edo street food). Common.
- **Catfish (namazu)**: Lowland rivers, lakes. Role: food; earthquake folklore. Common.
- **Dace and minnows (ugui, oikawa, haya)**: Rivers. Role: food. Common.
- **Salmon (sake / masu)**: Some Pacific-side rivers run cherry salmon (sakuramasu); big salmon runs are `[off-map: north]`. Role: food. Occasional.
- **Lake fish of Ashinoko**: Few native species (dace, crucian, eel, verify). Role: food. Occasional.

### == N Fauna: Sea life (for coast gameplay) ==

- **Bonito (katsuo)**: Sagami and Suruga bays, early summer (hatsugatsuo craze in Edo). Role: food, trade. Common.
- **Sardine and anchovy (iwashi)**: Huge schools; dried as hoshika fertilizer. Role: food, fertilizer. Dominant.
- **Horse mackerel, mackerel, sea bream, yellowtail, tuna (aji, saba, tai, buri, maguro)**: Coastal and offshore. Role: food. Common.
- **Squid and octopus (ika, tako)**: Rocky coast. Role: food. Common.
- **Abalone, turban shell, sea urchin (awabi, sazae, uni)**: Rocky shores, dived by ama. Role: food, trade. Common.
- **Clams (asari, hamaguri, shijimi)**: Tidal flats, estuaries; shijimi in brackish water. Role: food. Dominant (bays).
- **Oysters (kaki)**: Estuaries, Hamana. Role: food. Common.
- **Crabs and shrimp (kani, ebi; mokuzu-gani mitten crab in rivers)**: Shore, rivers. Role: food. Common.
- **Jellyfish, sharks, rays**: Offshore and bays. Role: minor danger. Occasional.
- **Sea turtles (umigame)**: Nest on sandy beaches of Enshū-nada and Sagami (verify). Role: none / omen. Rare.

## 2.W Wilderness man-made (W_WILDERNESS.md): 302 entries

### == W §1 Highway distance and direction markers ==

- **Mile mound pair (ichirizuka)**: a pair of earth mounds, one each side of a main highway every ri (~3.9 km), each ~9 m square and ~3 m high, topped with an enoki, pine or cedar. Ordered 1604, kept up by the nearby villages. Roadside, common on the Tōkaidō, Nakasendō and Kōshū, large `[terrain]`. Hook: navigation (count mounds for distance), landmark tree seen from afar, shade, rest spot. (BL: Civic, roads) {seam S054: W §1 + N §X}
- **Lone surviving mile mound (kata-ichirizuka)**: a pair where one mound has been ploughed away or washed out, leaving one mound and its tree. Roadside, occasional, medium `[terrain]`. Hook: navigation, landmark tree. (assumed for 1730; many survive singly today)
- **Mile mound on a minor road (waki-kaidō ichirizuka)**: smaller mounds, or just a planted tree, kept by the domain on side roads (Ōyama road, Kōshū branch roads). Roadside, occasional, medium `[terrain]`. Hook: navigation. (verify how regular they were on side roads)
- **Direction stone (oiwake-ishi / michi-shirube / dōhyō)**: stone post at a fork or in town carved with directions and distances ("right, to Edo; left, to Zenkōji"); the Shinano Oiwake gave the type its name; Nihonbashi is the zero point. Roadside/street, common at forks, small. Hook: navigation (readable in-game text). (BL: Civic, signpost stone) {seam S061: W §1 + U Streets: Notices}
- **Deity direction stone (michi-shirube Jizō / kōshin michi-shirube)**: a Jizō, Kannon or kōshin stone with directions carved on its side or base, so one stone does two jobs. Roadside, occasional, small. Hook: navigation, offerings. (verify frequency before 1750)
- **Pointing-hand direction stone (yubisashi michi-shirube)**: a carved hand pointing down the road, with a destination. Roadside, rare, small. Hook: navigation. (verify; many surviving examples are later Edo)
- **Wooden signpost (michi-shirube-gui / kidō-hyō)**: a squared post with brush-written or cut destinations. Most were wood, so few survive. Roadside, common, small. Hook: navigation. (assumed)
- **Pilgrim-route marker (junrei michi-shirube)**: a stone saying "to temple no. N of the Kannon circuit, X chō". It marks the pilgrim path off the highway. Roadside/mountain, occasional, small. Hook: navigation to a temple. (assumed form; the circuits are in era)
- **Chō-stone countdown (chōishi)**: numbered stones every chō (~109 m) counting down to a temple or summit. The landmark set is Kōyasan's: 3 m stupa-shaped stones, 1285, ~180 originals of 216. Plainer chōishi stood on many mountain approaches. Mountain, occasional (landmark at Kōya), small (landmark set: medium each). Hook: navigation (a countdown to the top). Kōya `[off-map: Kii]`.
- **Mountain station marker (gōme-ishi / gōme-hyō)**: a marker for a climb's stations (1st to 10th gō), as on Fuji's pilgrim trails. Mountain, rare, small. Hook: navigation, altitude cue. (verify form and date before 1750)
- **Pass name post (tōge no hyōchū)**: a post at the summit naming the pass and the provinces on each side. Mountain, occasional, small. Hook: navigation, landmark. (assumed)
- **Trail cairn (ishizumi / kerun)**: a small stone pile marking the route over bare rock, scree or open ridge. Mountain, occasional, small. Hook: navigation off-road. (assumed)
- **Hatchet blaze (nata-me / kizuke)**: a cut or peeled patch on trunks marking a woodsman's or hunter's path. Forest, occasional, small (a decal on trees). Hook: navigation along hidden trails. (assumed)
- **Bent-branch route mark (shiori / eda-ori)**: branches snapped or bent to mark the way back. It's the origin of the word *shiori* (bookmark). Forest, occasional, small. Hook: navigation, a tell that someone passed. (assumed as a period practice; the etymology is standard)
- **Snow-route poles (yuki-michi shirube)**: tall poles or tagged stakes marking the road under deep snow on Kiso and Hokuriku passes. Mountain, rare (seasonal), small. Hook: navigation in snow. (assumed)
- **Distance board at a ferry or crossing (michinori-fuda)**: a board giving the distance to the next post town and the fares. Roadside/river, occasional, small. Hook: navigation. (assumed; the fare boards are in BL, ferry landing)
- *Survey stake (kenchi-gui / nawa-ba)* → S128, under R §3.

### == W §2 Road surface, avenues and pass works ==

- **Stone-paved pass road (ishidatami)**: rounded fieldstones laid on steep pass sections; Hakone's laid 1680 (Enpō 8), 2 ken wide with 30–70 cm kerb stones, replacing bamboo mats; continues where the pass road enters a settlement. Mountain/roadside/street, rare (passes only; landmark at Hakone), `[terrain]`. Hook: the road line, slippery and noisy in rain (danger), navigation. (BL: Civic, roads) {seam S056: W §2 + U Streets: Street surface}
- **Bamboo-mat road (take-shiki no michi)**: Hakone's pre-1680 surface: bamboo mats laid over the mud and renewed every year by the villages. Mountain, rare, `[terrain]`. Hook: lore. `[outside 1680-1750: gone, replaced by the 1680 paving]`
- **Cross drains in paving (yoko-mizo / mizu-kiri)**: diagonal stone gutters across a paved or earth road that shed rain off the slope. Mountain, common on paved stretches, small. Hook: none (dressing). (assumed; visible on the surviving Hakone paving)
- **Cedar avenue (sugi-namiki)**: cedars planted along the road for shade and shelter. Hakone's, by Lake Ashi: planted 1618 (attributed to Matsudaira Masatsuna), ~400 remain `[old: 1618, still standing 1730]`. Nikkō's: ~37 km, 1625–48 `[off-map: Nikkō]`. Roadside/mountain, rare (landmark at Hakone), large `[terrain]`. Hook: landmark, shade, cover, a line to follow. {seam S002: W §2 + N §X}
- *Pine avenue (matsu-namiki)* → S001, under N §E.
- **Hackberry or mixed-tree row (enoki-namiki)**: shorter tree rows at village approaches and crossroads. Roadside, occasional, `[terrain]`. Hook: navigation. (assumed)
- **Road cutting (kiridōshi / horiwari)**: a road cut through a ridge between steep banks. The Kamakura cuttings (Asaina, Nagoe) are medieval examples near the map. Roadside/mountain, occasional, `[terrain]`. Hook: ambush point, chokepoint, cover.
- **Switchback trail (tsuzura-ori)**: a zigzag path up a steep slope, sometimes with a named count of turns. Mountain, common, `[terrain]`. Hook: slow movement, navigation.
- **Stone steps (ishidan / ishi-kaidan / ishidan-zaka)**: rough or dressed stone flights on the steepest pass pitches, up shrine hills, and as stepped lanes in temple and port towns (Kyoto's Higashiyama). Mountain/shrine/street, common at shrines, occasional elsewhere, medium `[terrain]`. Hook: movement, climbing, elevation, chokepoint, landmark. {seam S060: W §2 + R §10 + U Religious: Shrine forecourt + U Streets: Street surface}
- **Log steps (maruta-dan)**: logs pegged across a mountain path as steps. Mountain, common, small (repeated). Hook: movement. (assumed)
- *Road retaining wall (michi no ishizumi)* → S173, under R §8.
- **Cliff plank road (kakehashi / kake-michi)**: a timber gallery pinned to a cliff face over a river. The landmark is the Kiso no Kakehashi on the Nakasendō: burned 1647, rebuilt with stone walling, so by 1730 it's part stone. Mountain/ river, landmark (small cliff galleries rare), large structure. Hook: danger (fall), chokepoint, landmark. (verify the 1647/48 rebuild details)
- **Chain climbs on sacred peaks (kusari-ba)**: iron chains fixed down rock faces on pilgrim ascents (Ishizuchi, Myōgi). Mountain, rare, medium. Hook: climbing, fall danger, landmark. (verify dates; some chains may be later Edo)
- **Wooden ladders on rock steps (kake-bashigo)**: ladders tied in place on pilgrim routes where the rock is too steep. Mountain, rare, small. Hook: climbing, fall danger. (assumed)
- **Hand-dug rock tunnel (tonneru / dōmon)**: a road tunnel chiselled by hand. The famous Ao-no-Dōmon, dug by the monk Zenkai 1735–63, is in window but in Kyushu. Mountain, landmark, large `[terrain]`. Hook: chokepoint, shelter, lore. `[off-map: Kyushu]`
- **Corduroy track over bog (sodagi-michi / kijiki)**: logs or brushwood laid across wet ground. Forest/river, occasional, `[terrain]`. Hook: movement through marsh. (assumed)
- **Old abandoned road alignment (kyūdō / furumichi)**: an overgrown earlier route, such as the medieval Yusaka road over Hakone, disused after the Edo Tōkaidō was laid. Mountain/forest, rare, `[terrain]`. Hook: a hidden path, a sekisho bypass (danger: illegal). (verify the Yusaka route)
- **Pack-ox path (ushi-michi / bokka-michi)**: narrow steep trade paths worked by oxen instead of horses. The salt road from the Japan Sea into Shinano (Chikuni road) is one. Mountain, occasional, `[terrain]`. Hook: navigation off the highways. (verify the ox use before 1750)
- **Road-repair and procession sand heaps (michi-bushin no suna / morizuna)**: sand and gravel piles left by villages on road-repair duty, and sand cones or spread sand laid on the road before a daimyō or shogunal procession. Roadside/street, occasional / rare (event), small. Hook: dressing, event marker. (road heaps assumed; morizuna verify) {seam S059: W §2 + U Streets: Street surface}
- **Stone cart rails (kuruma-ishi)**: grooved stone paving for ox carts on the Ōtsu–Kyoto road. Roadside/street, rare, `[terrain]`. Hook: lore. `[outside 1680-1750: laid 1805]` (verify) The ox carts themselves are in: R §7. {seam S057: W §2 + U Streets: Street surface + R §17}
- *Ditch-side road drains (sokkō / michi-bata no mizo)* → S058, under U Streets: Street surface.

### == W §3 Rest, water and wayside comfort ==

**Cross-reference, not counted: tea stalls in the middle of nowhere are buildings. See BL: roadside tea house (kake-jaya / chamise) and rest-station tea house (tateba-jaya). Only their outdoor spill (benches, tie posts) is below.**
- *Rest bench (koshikake / shōgi)* → S063, under U Streets: Street furniture.
- **Sitting stone (koshikake-ishi)**: a flat stone to sit on at a crossroads, town edge or temple approach; many carry legends (Yoshitsune, Kōbō Daishi, a daimyō) and are roped or fenced with a small board telling the story. Roadside/commons/street, occasional, small. Hook: rest, lore, landmark. (BL: Civic "names only") {seam S064: W §3 + R §13 + U Streets: Street furniture}
- **Porter's load-rest stone (niyasume-ishi / kata-yasume)**: a flat-topped stone or bank on a steep climb where porters set down their loads without unshouldering. Mountain/roadside, occasional, small. Hook: rest. (assumed)
- *Piped roadside spring (kakehi no shimizu)* → S068, under R §2.
- **Kōbō spring (Kōbō-shimizu / Kōbō-ido)**: a spring said to have been struck from the rock by Kōbō Daishi's staff, marked with a stone or a tiny shrine. Roadside/mountain, occasional, small. Hook: WATER, lore.
- *Horse trough (uma no mizu-bune)* → S065, under U Streets: Street furniture.
- *Horse tie stone (uma-tsunagi-ishi)* → S066, under U Streets: Street furniture.
- **Horse-washing ramp (uma-arai-ba)**: shallow graded bank into a stream, pond or moat where packhorses and horses were watered and washed. River/commons/castle, occasional, small `[terrain]` / medium. Hook: water access, landmark. (moat version assumed) {seam S067: W §3 + R §7 + U Water: Moats}
- *Open rain shelter (amayadori / azumaya)* → S217, under U Gardens: Stroll garden.
- *Rock overhang camp (iwa-kage)* → S049, under N §T.
- **Travellers' fire ring (takibi-ato)**: a ring of blackened stones with charcoal and bones. Roadside/forest, common, small. Hook: fire, evidence of a camp.
- **Always-lit lantern and lighthouse lantern (jōyatō / tōmyōdō)**: stone or wooden lantern tower kept burning all night by a village, ward or kō at a pass top, crossroads, town entrance, lake shore, ferry, quay or headland; coastal ones oil-lit by a keeper (Miya's from 1625 `[old: 1625, still standing 1730]`). Roadside/street/coast, occasional (roads, towns), rare (coast), medium–large. Hook: NAVIGATION (lit at night), light, landmark. Many survivors are late Edo; R tags the tall stone towers `[outside 1680-1750: mostly 19th c.]` (verify); the type is in. (verify how many were lit nightly) (BL: Civic, lighthouse lantern) {seam S070: W §3 + U Streets: Street lighting and lanterns + W §20 + R §17}
- *Crossroads lantern post (tsuji-andon)* → S071, under U Streets: Street lighting and lanterns.
- **Sandal-hanging tree or post (waraji-kake)**: worn and spare straw sandals hung on a tree or Jizō at a pass, as an offering or just discarded. Roadside, occasional, small. Hook: loot (spare sandals), lore.
- **Alms-giving stand (settai-dai)**: a plank table where villagers gave pilgrims tea, rice balls or straw sandals on set days. Roadside, rare, small. Hook: food/water (event). (settai is a Shikoku custom; elsewhere assumed)
- **Viewpoint clearing (miharashi / tōge no nagame)**: a cleared knoll at a pass with a bench and view. Hiroshige prints are full of them. Mountain, occasional, `[terrain]`. Hook: landmark, a scouting spot. (assumed as maintained)

### == W §4 River crossings in the wild ==

- **Stepping stones across water (tobi-ishi / ishi-watari / sawatari)**: flat stones set across a shallow stream or a garden pond. River/garden, common, small (repeated). Hook: crossing; washes over in spate. {seam S072: W §4 + U Gardens: Paths and stepping stones}
- **Marked ford (watari-se)**: a gravel crossing with stakes or poles marking the shallow line. River, common, `[terrain]`. Hook: crossing, drowning danger when the river is high. (assumed)
- **Porter-wading crossing (kachi-watashi)**: an unbridged river crossed on porters' shoulders or on a litter (rendai). In the wild it shows as a worn gravel bank, a porter shelter and platforms. Tōkaidō rivers: Sakawa (near Odawara), Ōi, Abe. River, rare (landmark on the Tōkaidō), `[terrain]`. Hook: crossing, drowning danger, landmark. (BL: Government, river-crossing office)
- **Log bridge (maruki-bashi)**: one or two logs, sometimes with a pole handrail. River, common, small/medium. Hook: crossing, fall danger. (BL: Civic, roads)
- *Plank bridge (ita-bashi)* → S074, under U Water: Bridges.
- *Earth-covered bridge (dobashi)* → S075, under U Water: Bridges.
- *Stone slab bridge (ishi-ita-bashi)* → S073, under U Water: Bridges.
- **Cantilever bridge (hane-bashi)**: stacked cantilevered beams from each bank. The Saruhashi (Kōshū road) is the landmark; smaller ones span mountain gorges. River/mountain, landmark (small ones rare), large structure. Hook: crossing, landmark. (BL: Civic, roads)
- **Vine bridge (kazura-bashi)**: a suspension walkway of mountain vines with slat decking. Iya is the famous site. River/mountain, rare, large structure. Hook: crossing, fall danger (sway). `[off-map: Shikoku]` (generic mountain vine bridges elsewhere assumed) (BL: Civic, roads)
- **Basket rope crossing (kago-watashi / yaen)**: a basket slung on a rope across a gorge and hauled over. Etchū/Hida and Totsukawa are known sites. River/mountain, rare, medium. Hook: crossing, fall danger. (verify window; the famous print is Hiroshige, 1850s)
- **Hand-line across a stream (tsuna-watashi)**: a rope strung across a stream to hold while wading. River, occasional, small. Hook: crossing. (assumed)
- **Ferry landing, wild bank (watashi-ba)**: an earth or stone ramp with a mooring post, a waiting bench, and a bell or drum on a post to call the ferryman from the far bank. River, occasional, medium. Hook: crossing, SOUND (the bell), shelter (shed). (BL: Civic, ferry landing and ferry-keeper's hut)
- **Rope-guided ferry (hiki-bune)**: a rope across a narrow river that the ferry pulls itself along. River, occasional, medium. Hook: crossing. (BL: Civic) (assumed)
- **Boat bridge (funa-bashi)**: boats chained side by side with planks on top. River, rare (landmark at the Jinzū), large. Hook: crossing. (BL: Civic) {seam S076: W §4 + U Water: Bridges}
- **Seasonal low-water bridge (kari-bashi / fuyu-bashi)**: a temporary plank bridge built for the dry season and taken down before the summer floods. River, occasional, medium. Hook: crossing (seasonal). (verify which rivers)
- **Washed-out bridge remains (nagare-bashi no ato)**: stumps of piles and a broken abutment where a bridge went in a flood. Rokugō's bridge was lost in 1688 and replaced by a ferry. River, rare, medium. Hook: a broken crossing, landmark, cover. (BL notes the Rokugō ferry from 1688)
- *Stone abutment (hashi-dai no ishigaki)* → S077, under U Water: Bridges.
- *Log flume bridge (kakehi-bashi)* → S069, under R §2.
- **Rafted river crossing (ikada-watashi)**: a log raft poled across by locals where there's no ferry. River, occasional, medium. Hook: crossing. (assumed)

### == W §5 Wayside religious stones and figures ==

- **Roadside Jizō (michi no Jizō / tsuji-jizō)**: standing stone monk with staff and jewel at crossroads, bridges and village entrances, often under a little roof, with an offering stone, flowers and coins; the travellers' guardian. W shows a red bib and cap; R says the red bib may be later (verify). Roadside/commons, common, small. Hook: landmark, lore, small offerings (coins: Stephen decides on loot). (BL: Buddhist, roadside Jizō; Jizō-dō) {seam S078: W §5 + R §12}
- **Jizō hut / street-corner Jizō box (Jizō-dō / tsuji Jizō)**: waist-to-head-high roofed box or tiny open hall sheltering a Jizō; in Kyoto one per ward at a street corner, bibbed and fed, honoured at Jizō-bon (8th month). Roadside/street, occasional (roads) / common (Kyoto), small–medium. Hook: tiny rain shelter, landmark. (BL: Buddhist, roadside Jizō; with an interior it moves to BL) {seam S079: W §5 + U Religious: Stone monuments}
- *Six-Jizō row (roku Jizō)* → S080, under U Religious: Temple forecourt.
- **Pass-top Jizō (tōge no Jizō)**: a bigger Jizō at a pass summit, often with piled stones and hung sandals. Mountain, occasional, small. Hook: navigation (the summit), lore.
- **Couple dōsojin (sōtai dōsojin)**: a carved man and woman, arm in arm, at a village boundary or crossroads, against disease and evil and for marriage; densest in Shinano (Azumino), Kōzuke and Sagami. Roadside, occasional in 1730, small. Hook: a village boundary: a village is near. Most survivors are 1804–30; R tagged the type outside, but it existed in 1730, so it is IN (scarcer than today). {seam S081: W §5 + R §12}
- **Character dōsojin (moji dōsojin)**: a natural stone carved with the word 道祖神. Roadside/commons, common (Sagami, Kōshū, Shinano), small. Hook: village-entrance marker, boundary. {seam S082: W §5 + R §12}
- **Round-stone dōsojin (maru-ishi dōsojin)**: river-rounded stones heaped on a plinth as the road god; a Kai (Kōshū) type beside Fuji and Hakone. Roadside, occasional, small. Hook: boundary, lore. (verify period) {seam S083: W §5 + R §12}
- **Phallic stone (konsei-sama / yōseki / seki-bō)**: natural or carved phallic stone at a crossroads or village edge for fertility and protection. Roadside/commons, occasional, small. Hook: lore. {seam S084: W §5 + R §12}
- **Kōshin stone (kōshin-tō)**: square pillar with the blue-faced Shōmen Kongō, the three monkeys, sun, moon and cocks, put up by kōshin-kō groups after their 60-day all-night vigils. Oldest dated one 1664; the peak is disputed (§3.3). Roadside/commons/street, common (Kantō, Kinai), small. Hook: landmark, lore. (verify peak) (BL: Kōshin hall) {seam S085: W §5 + R §12 + U Religious: Stone monuments}
- **Kōshin mound (kōshin-zuka)**: low earth mound with a kōshin stone (or several stones) on top, often at a crossroads. Roadside/commons, occasional, medium `[terrain]`. Hook: landmark, a small rise to see from. {seam S086: W §5 + R §12}
- **Horse-headed Kannon (batō Kannon)**: stone with the horse-headed Kannon or its name, where packhorses died or on dangerous pack roads and passes; stone ones start mid-Edo, common in the east, many on the Nakasendō; most survivors are later 18th–19th c. Roadside/mountain, common in the east (W) / occasional (R), small. Hook: a DANGER tell (steep or deadly stretch ahead), pass landmark. Straw horse-shoe offerings hang on them (R §7). (BL: Buddhist props) {seam S087: W §5 + R §12}
- **Horse grave and animal memorial (uma-zuka / uma kuyō / chikushō kuyōtō)**: a small mound or stone for a horse or ox, by the road where it fell or by the owner's yard. Roadside/yard, occasional, small. Hook: danger tell, lore. {seam S088: W §5 + R §9}
- **Ox mound (ushi-zuka)**: the same for pack oxen on the ox roads. Mountain, rare, small. Hook: lore. (assumed)
- **Moon-waiting stone (tsukimachi-tō: nijūsan-ya / jūkyū-ya)**: stone put up by women's or village kō who stayed up for the moonrise on set nights. Roadside/commons, occasional, small. Hook: landmark. (verify the date peak; BL lists the 23rd-night stone) Women's Nyoirin Kannon stone (29th night): R §12. {seam S089: W §5 + R §12}
- **Sun-waiting stone (himachi-tō)**: the same for the sunrise vigil. Roadside, rare, small. (verify)
- **Nenbutsu stone (nenbutsu-tō / myōgō-hi)**: "Namu Amida Butsu" carved large, put up by a nenbutsu kō, often counting a million recitations. Roadside/commons/street/temple, common (R) / occasional, small–medium. Hook: landmark. Tokuhon-style script stones are `[outside 1680-1750: c.1800]`. {seam S090: W §5 + R §12 + U Religious: Stone monuments}
- **Daimoku stone (daimoku-tō)**: pillar carved "Namu Myōhō Renge Kyō" in bold Nichiren script, near Nichiren temples and at execution grounds as a memorial. Roadside/commons/temple, occasional, small–medium. Hook: landmark. (verify the Suzugamori date) {seam S091: W §5 + R §12 + U Religious: Stone monuments}
- **Hōkyōin-tō (treasure-seal stupa)**: stepped square stone stupa with horned corners, a memorial for important dead, at crossroads, hilltops, graves and temples; medieval, with an Edo revival; medieval ones still stand by roads `[old: medieval, still standing 1730]`. Roadside/graveyard/temple, occasional (rare in villages), medium. Hook: landmark, an "old" feel. {seam S092: W §5 + R §11 + R §12 + U Religious: Temple forecourt}
- **Sutra mound (kyōzuka)**: mound over buried sutras; Heian ones hold bronze tubes, Edo ones are often one-stone-one-character (ichiji-isseki-kyō) pebble mounds with a marker stone on top. Roadside/mountain/temple, occasional (rare in towns), medium `[terrain]`. Hook: landmark, digging (Stephen decides whether it's diggable). (verify the Edo frequency) {seam S093: W §5 + R §11 + U Religious: Temple forecourt}
- **Miniature pilgrimage circuit (utsushi reijō / utsushi fudasho)**: 33 (Saigoku copy) or 88 (Shikoku copy) small stone Kannon or Kōbō figures along a hill path or in a temple precinct, so locals can "do" the pilgrimage in a day. Dating disputed (§3.3): suggested reading, 33-Kannon copies IN but rare; 88-temple copies `[outside 1680-1750: mostly 19th c.]`. Mountain/commons/temple, a set of smalls along a path. Hook: a line of statues leads up a hill (navigation). (verify earliest dates) {seam S094: W §5 + R §12 + R §17 + U Religious: Stone monuments}
- **Stone Buddha (sekibutsu)**: seated or standing Amida, Kannon, Yakushi or Dainichi alone by the road, under a tree or on a hillside. Roadside/commons, common (W) / occasional (R), small. Hook: landmark. Rows along a temple wall: U (Temple forecourt). {seam S095: W §5 + R §12}
- **Fudō stone (Fudō Myōō)**: the fierce Fudō with sword and rope at waterfalls, springs, steep places and mountain-cult sites. Mountain/river/commons, occasional, small. Hook: a tell for water or a falls nearby. {seam S096: W §5 + R §12}
- **Water-god stone (suijin-hi)**: stone to the water kami at a spring, pond, weir, irrigation intake or riverbank. River/field/commons, common (R) / occasional (W), small. Hook: a WATER tell. (BL: Shinto, mountain/water tell) {seam S097: W §5 + R §12}
- **Mountain-god stone or hokora (yama no kami)**: the forest workers' deity: a stone or tiny shrine at the forest edge or a charcoal area, with offered sickles and axes. Forest/mountain/field edge, common in mountains, small. Hook: marks where the forest starts and that forest work is near; loot (an offered axe or sickle, Stephen decides). (BL: Shinto props) {seam S098: W §5 + R §12}
- **Roadside micro-shrine (hokora)**: a tiny wooden or stone shrine house on a stone base at a field corner, tree root, spring or pass. Roadside/forest, common, small. Hook: landmark. (BL: Shinto, micro-shrine)
- **Wild Inari shrine (no-Inari)**: a hokora with fox figures and a small red torii in the woods or at a field edge. Forest/roadside, occasional, small. Hook: landmark.
- **Lone torii in the forest (mori no torii)**: a single wooden or stone torii where a path enters sacred ground. A hokora or rock lies beyond. Forest/mountain, occasional, medium. Hook: NAVIGATION (a shrine ahead), landmark.
- *Trailhead lantern pair (tozan-guchi tōrō)* → S100, under R §10.
- **Banner-pole socket stones (nobori-tate ishi)**: paired stones with square sockets for festival banner poles at a shrine or path start. Shrine/roadside, occasional, small. Hook: navigation. (verify date) {seam S101: W §5 + R §10}
- **Crossroads chapel (tsuji-dō)**: a tiny open-fronted hall at a lonely crossroads holding a statue, no bigger than a shed. Roadside, occasional, medium. Hook: SHELTER (small), landmark. (If Stephen wants an interior, it moves to BL.)
- *Wooden grave tablet at a death spot (sotoba)* → S102, under R §11.
- **Rough carved Buddhas of a wandering monk (Enkū-butsu)**: axe-hewn wooden Buddhas left in forest halls, tree hollows and village shrines by Enkū (d. 1695) in Mino and Hida. Forest, rare, small. Hook: lore, a collectible find. (BL: Dwellings, wandering carver-monk's hut)

### == W §6 Mountain religion and pilgrim marks ==

- **Summit or pass shrine (okumiya / tōge no yashiro)**: a stone or board shrine on a peak or pass, the inner sanctuary of a lowland shrine. Mountain, rare, medium. Hook: landmark, offerings. (BL: Shinto, summit/pass shrine)
- **Summit windbreak wall (mine no ishigaki)**: a ring of dry-stone walling around a summit shrine or pilgrim hut against the wind. Mountain, rare, medium `[terrain]`. Hook: COVER from wind and fire, landmark. (assumed)
- **Offered iron swords at the summit (hōnō tōken)**: iron swords, spear heads and bells left by climbers at summit shrines (Tateyama, Hakusan). Mountain, rare, small. Hook: loot (iron), lore. (BL: Shinto, summit shrine items)
- **Mountain-path torii (ichi no torii, ni no torii)**: numbered torii marking the stages of a sacred climb. Mountain, occasional, medium. Hook: NAVIGATION (progress up the mountain).
- **Horse turn-back point (umagaeshi)**: the spot where riders dismount and the climb continues on foot. Fuji's Yoshida trail has a stone torii at ~1,450 m; the name recurs on Nikkō, Haguro and other sacred mountains. Mountain, rare, medium. Hook: navigation, landmark, a zone boundary (the sacred climb begins).
- **Women's limit stone (nyonin kekkai-seki)**: a stone marking where women must turn back on a sacred mountain. The Ōmine and Kōya bans are the famous ones; Fuji allowed women only to the lower stations. Mountain, rare, small. Hook: lore, landmark. (BL: Buddhist, nyonin-dō)
- **Pilgrim-club stone (kō-hi: Ise-kō, Ōyama-kō, Fuji-kō)**: stones put up by confraternities along their routes and at shrines; the 1705 Ise okage-mairi is in window; Fuji-kō spread after Jikigyō Miroku fasted to death on Fuji in 1733. Roadside/mountain/shrine, occasional, small. Hook: NAVIGATION (the pilgrim trail to a peak), lore. Ontake-kō `[outside 1680-1750: lay climbing opened 1785+]`; Fuji and Ontake stones mostly `[outside 1680-1750: late 18th–19th c.]`. {seam S103: W §6 + R §10}
- **Ōyama road markers (Ōyama-michi hyō / dōhyō)**: direction stones, signposts and Fudō figures leading to Sagami's Ōyama (Afuri shrine and Fudō temple), a big Edo pilgrimage in the Hakone/Sagami area. Roadside/commons, occasional, small. Hook: navigation. (verify: the Ōyama-mairi boom may be mostly after 1750) (BL: signpost stone) {seam S062: W §6 + R §12}
- **Waterfall ascetic site (taki-gyōba)**: a shimenawa across the fall, a Fudō figure, a standing stone in the plunge pool and a changing hut. Mountain/river, rare, medium. Hook: WATER, landmark. (BL: Buddhist, waterfall practice site)
- **Ascetic practice rocks (gyōba-iwa / nozoki)**: Shugendō test spots: cliff edges where novices are hung over the drop (Ōmine's Nishi-no-nozoki), rock clefts to squeeze through, balancing rocks. Mountain, rare, `[terrain]`. Hook: danger (fall), landmark. `[off-map: Ōmine]` for the famous one; generic ones on any Shugendō peak (assumed)
- *Rebirth lava cave (tainai / tainai-kuguri)* → S050, under N §T.
- **Cave shrine (iwaya)**: a natural cave with a shrine or Buddha inside. Enoshima's Iwaya (Benzaiten) was a big Edo pilgrimage near Kamakura. Mountain/coast, rare (landmark at Enoshima), `[terrain]`. Hook: SHELTER, landmark. (BL: Buddhist, cave halls)
- **Cliff Buddhas (magaibutsu)**: Buddhas carved in relief on a rock face. The landmark is Moto-Hakone, on the old road by Shōjin pond: ; Rokudō Jizō, 3.5 m, 1299 ; three Hitaki Jizō, 1311 ; 25 bodhisattvas split by the road The area was seen as "hell" for its volcanic ground. Mountain/roadside, landmark (small ones rare), large structure. Hook: LANDMARK on the Hakone map, lore.
- **Medieval stone-pagoda group (sekitō-gun)**: the tall hōkyōin-tō and gorintō beside the Moto-Hakone Buddhas, traditionally the graves of Tada Mitsunaka and of the Soga brothers and Tora. Roadside, landmark, medium each. Hook: landmark.
- **Riverbank of souls (sai no kawara)**: a desolate shore or volcanic flat covered in small stone stacks for dead children, with Jizō. Hakone has one by Lake Ashi near Moto-Hakone; Osorezan is the famous one. Mountain/lake, rare, `[terrain]` + props. Hook: an EERIE landmark. Osorezan `[off-map: Tōhoku]`.
- **Hell-valley warning and Jizō (jigoku-dani)**: Jizō, a stone warning and sometimes a rope line at volcanic vents. Hakone's Ōwakudani was called Ōjigoku ("great hell") until 1873. Mountain, rare, smalls at a nature site. Hook: DANGER (gas), landmark. (the vent itself belongs to the nature agent)
- **Pass offering heap (tamuke)**: a pile of stones, twigs or sandals at a pass, each traveller adding one for a safe crossing. Mountain, occasional, small. Hook: lore, navigation (the summit).
- **Summit cairn (sanchō no ishizumi)**: a stone pile at a peak, sometimes with a small figure on it. Mountain, occasional, small. Hook: navigation.
- **Fire-ritual hearth (goma-dan / saitō-ba)**: a stone-edged hearth in a clearing where yamabushi burn prayer sticks. Mountain, rare, medium. Hook: FIRE, landmark. (assumed placement)
- **"No leeks or wine" stone (kaidan-seki / kinsei-hi)**: "leeks (garlic), meat and wine may not enter the gate", at Zen temple gates and on paths to mountain temples. Temple/mountain, common at Zen temples / occasional in the mountains, small. Hook: navigation (a temple ahead). {seam S104: W §6 + U Streets: Notices}
- **Kumano subsidiary shrine sites (ōji / ōji-ato)**: the waystation shrines of the Kumano routes, many ruined by Edo and marked by a stone or a tiny hokora. Mountain, occasional, small. Hook: navigation. `[off-map: Kii]`
- *Pilgrim huts (murodō / tsuya-dō)*: *cross-reference, not counted*. They have interiors: BL, Buddhist roadside.

### == W §7 Sacred rocks, trees and waters ==

- **Sacred rock (iwakura / shinseki)**: odd boulder, balanced rock or outcrop roped with shimenawa as a kami seat, sometimes with shide and a tiny offering shelf; in forests, on mountains and in shrine forecourts. Paired rocks (meoto-iwa): W §7. Forest/mountain/shrine, occasional / landmark, medium–large. Hook: LANDMARK, cover. The rock is nature; rope, torii and offerings are the religious kit. (BL: Shinto props) {seam S051: W §7 + N §T + U Religious: Shrine forecourt}
- **Wedded rocks (meoto-iwa)**: two rocks joined by a heavy rope. Futami (Ise coast) is the landmark; small inland pairs exist too. Coast/mountain, rare (landmark), large. Hook: landmark. Futami `[off-map: Ise]`.
- **Sacred tree (shinboku / goshinboku)**: a huge cedar, camphor or ginkgo roped with shimenawa and shide and left uncut, often inside a low fence or with a hokora at its foot; in shrine grounds and forests. Shrine/forest/roadside, common at shrines / occasional in the wild, large (tree) + small rope and fence. Hook: LANDMARK (visible), cover. Tree species: N. {seam S052: W §7 + R §10 + U Religious: Shrine forecourt}
- **Uncut god tree on a felled slope (yama no kami no ki / tome-ki)**: one tree deliberately left standing on a cut-over slope as the mountain god's seat. Forest, occasional, large. Hook: a landmark on bare ground. (assumed)
- **Cursing nails in a sacred tree (ushi no toki mairi no ato)**: a straw doll pinned with five-inch nails to a sacred tree, from the Edo "hour of the ox" curse (associated with Kifune, Kyoto). Forest, rare, small. Hook: EERIE find, a nail (loot), lore.
- **Sacred spring (reisen / meisui)**: a spring roped with shimenawa, with a stone basin and ladle, often at a shrine in the woods. Forest/mountain, occasional, small. Hook: WATER, landmark.
- **Pond with a Benten islet (Benten-jima / shin-ike)**: small Benzaiten shrine or stone on an islet in a village-shrine or forest pond, reached by a small bridge, stepping stones or a plank. Shrine/forest/field, occasional (rare in the wild), medium `[terrain]`. Hook: landmark, water. (BL: Shinto props, sacred pond; Benten hall) {seam S105: W §7 + R §10 + R §12}
- **Footprint or hoof stone (ashiato-ishi)**: a rock with a hollow said to be a hero's footprint, a god's hoof mark or a tengu's. Roadside/mountain, occasional, small. Hook: lore.
- *Strength stones by the road (chikara-ishi)* → S106, under R §10.
- **Night-crying stone (yonaki-ishi)**: the Sayo-no-Nakayama stone on the Tōkaidō between Kanaya and Nissaka. A legend has it crying at night for a murdered mother; Hiroshige shows it sitting in the road. Roadside, landmark, medium. Hook: LANDMARK, lore.
- **Killing stone and gas vent fence (sesshō-seki)**: a rock at volcanic vents, fenced by stones or rope. The Nasu stone is tied to the nine-tailed fox; the name was used for gassy vents generally. Mountain, rare, small + fence. Hook: DANGER (gas), lore. Nasu `[off-map: Nasu]`.
- **Rope across a waterfall or gorge (taki no shimenawa)**: a shimenawa spanning a falls or a narrow gorge mouth, marking sacred water. Mountain/river, rare, medium. Hook: landmark.
- **Offering shelf at a big rock (iwa no sonae-dana)**: a plank shelf pinned to a boulder with sake cups and salt. Forest, occasional, small. Hook: lore. (assumed)

### == W §8 Forest work: charcoal, timber, wood ==

- **Black-charcoal kiln (kuro-zumi-gama)**: an earth-dome kiln with a flue, cut into a hillside, smothered to cool. Forest, occasional, medium. Hook: WARMTH, a smoke column seen from afar (navigation), charcoal. (BL: Rural industry; the hut is in BL Dwellings)
- **White-charcoal kiln (shiro-zumi-gama / binchō)**: a stone and clay kiln whose charcoal is raked out red-hot into a sand-and-ash pit. Kishū binchō dates from the Genroku era. Forest, rare, medium. Hook: warmth, a burn danger at the quench pit. (BL: Rural industry)
- **Charcoal-kiln ruin (sumigama-ato)**: a round pit with a slumped rim, charred earth and a flue gap. Kilns moved with the wood supply, so old pits dot every worked forest. Forest, common, `[terrain]`. Hook: cover, a tell of past work.
- **Pit-burn charcoal site (fuse-yaki / ana-yaki)**: a simpler trench burn under earth and turf. Forest, occasional, `[terrain]`. Hook: warmth, fire. (assumed)
- **Charcoal bales (sumi-dawara)**: straw-wrapped charcoal bales stacked at a track end for porters or horses, or in the yard. Forest/roadside/yard, occasional, small. Hook: fuel (LOOT lies on them). {seam S107: W §8 + R §6}
- *Firewood stacks (maki-zumi / takigi-zumi)* → S108, under R §6.
- **Kiln-wood cutting heaps (gen-boku)**: short oak and konara logs cut to kiln length, stacked by a kiln. Forest, occasional, small. Hook: fuel. (assumed)
- **Branded stump or log end (gokuin / kokuin)**: stumps and log ends stamped with the owner's hammer brand (domain or shogunate), proof that a felling was licensed. Forest/river, occasional, small. Hook: a tell that you're in an official forest (see §13).
- **Log deck at a landing (bōzumi / doba)**: a stack of felled logs at a river landing or chute foot waiting to go down. Forest/river, occasional, medium. Hook: COVER, climbable.
- **Timber chute (shura)**: logs laid lengthwise down a slope as a trough for skidding timber, sometimes wetted. Forest/ mountain, occasional, large `[terrain]`. Hook: DANGER (a running log), fast descent, landmark. (BL: logging camp)
- **Sledge track (kinma-michi)**: log crossties laid like a ladder track on which timber sledges (kinma) were hauled down. Forest, occasional, `[terrain]`. Hook: navigation (a track). (verify that kinma was in use before 1750)
- **Log flush dam (teppō-zeki)**: a timber dam across a mountain stream, filled then released to flush logs down in a surge. Forest/river, rare, large structure. Hook: DANGER (the release), a crossing on top, landmark. (verify the Edo date)
- **Loose log drive (kuda-nagashi)**: logs floated singly down a river at high water before rafting. River, occasional (seasonal), smalls on the water. Hook: danger (a crush), a crossing hazard.
- **Log-catching boom (tsuna-ba / ami-ba)**: a rope or log boom across a river where loose logs were caught and bound into rafts. Owari's Kiso timber was caught at Nishikori. River, rare (landmark on the Kiso), large structure. Hook: crossing, landmark. (verify Nishikori)
- **Log raft (ikada)**: logs bound with rope and vines, moored at a bank with poles aboard, or floated down to city timber yards. River/canal, occasional, medium. Hook: river travel, a crossing, a platform. (BL: timber rafting station) {seam S109: W §8 + U Water: Canals}
- **Sawpit and whipsaw trestle (kobiki-ba)**: a sloped log trestle where two sawyers ripped planks with the big ōga frame saw. Forest, occasional, medium. Hook: loot (a saw, wedges). (BL: logging camp)
- **Shingle-splitting site (hegi-ita tsukuri-ba)**: sawara or hinoki bolts split into roof shingles, with shavings and bundles. Forest, occasional, small. Hook: none (dressing). (assumed as a forest site)
- **Bark-stripped cypress (hiwada-muki no ki)**: hinoki with the outer bark peeled in sheets for bark roofing (hiwada). Done without killing the tree. Forest, occasional, small (a tree decal). Hook: a tell.
- **Wood-turners' workings (kiji-shi no ato)**: bowl blanks, shavings and pole-lathe pits in beech forest, left by itinerant turners. Forest, rare, small. Hook: loot (bowls). (BL: Dwellings, wood-turner's forest hut)
- *Clear-cut bare slope (hage-yama)* → S010, under N §E.
- *Planted cedar stand (sugi no ue-bayashi)* → S011, under N §E.
- *Slash-and-burn plot (yakihata)* → S008, under N §E.
- **Shiitake log stack (shiitake hodagi)**: oak logs slashed with a hatchet (nata-me method) and leaned in a damp gully so spores settle and mushrooms grow. Forest, occasional, small. Hook: FOOD. Izu Amagi and Bungo are the centres. (verify the date in Izu)
- **Sledge (sori / kinma / shura)**: wooden hauling sledge for timber, stones, logs or manure over mud and grass; one left at a slope foot. Forest/yard/field, occasional, small–medium. Hook: haul item, loot (wood), dressing. {seam S110: W §8 + R §7}
- **Felling notch and wedges in a half-felled tree (kirikake)**: a tree abandoned mid-cut with wedges still in, a sign of a crew that left in a hurry. Forest, rare, small. Hook: loot (wedges), danger (a fall). (assumed)

### == W §9 Hunting, trapping and river fishing ==

**Cross-reference, not counted: the hunter's hut (ryōshi-goya / matagi-goya) is BL, Dwellings / Rural industry.**
- **Ground blind at a game trail (machi-ba / tachi-ma)**: a brush screen or rock blind where a gunner waits during a drive hunt (makigari) as beaters push game along. Forest/mountain, occasional, small. Hook: COVER, a sniping position. (assumed; *tatsu-ma* is the Matagi term)
- **Tree perch (ki no ue no machi-ba)**: a plank or crotch seat lashed in a tree over a trail or crop edge. It's the closest analogue to Chernarus hunting stands. Forest, rare, small. Hook: a high vantage, cover. (assumed; may be anachronistic as a built stand, so flag for Stephen)
- **Pit trap (otoshi-ana / shishi-ana)**: covered pit on an animal path for boar or deer, often along a boar wall, sometimes with stakes. Forest/field edge, occasional, small `[terrain]`. Hook: DANGER (fall), a trap. (verify stakes) {seam S111: W §9 + R §5}
- **Deadfall (osa / hira-otoshi)**: a heavy log or flat stone propped on a trigger stick over bait. Forest, occasional, small. Hook: DANGER, food.
- **Spring snare (hane-wana / kukuri-wana)**: a noose on a bent sapling set on a runway. Forest, common, small. Hook: DANGER (the leg), food.
- **Bird-lime rods (tori-mochi zao)**: rods smeared with lime, used by bird-catchers (tori-sashi) for small birds, left propped in bushes. Forest, occasional, small. Hook: food, lore.
- **Ridge mist-net (kasumi-ami)**: fine nets strung across a ridge saddle to catch migrating thrushes in autumn (Hida, Mino). Mountain, rare, medium. Hook: food, a tangle hazard. (verify the date)
- **Duck-netting pond (sakaami / kamo-ba)**: a pond edge with a bank and hide where hunters throw Y-framed nets at rising ducks. Kaga's sakaami is said to date from the Genroku era. River/forest, rare, medium. Hook: food. Kaga `[off-map: Kaga]`. (verify)
- *Boar wall (shishigaki)* → S112, under R §5.
- *Boar ditch (shishi-bori)* → S113, under R §5.
- *Game fence of brush and stakes (shika-gaki)* → S114, under R §5.
- *Scare clapper line (naruko)* → S115, under R §5.
- **Shogun's hunt field (kariba / shishigari-ba)**: open grass or pasture ground with earthworks and stands used for great drive hunts. Yoshimune's Koganehara hunts were in the 1720s. Forest/plain, landmark, `[terrain]`. Hook: landmark, open ground. (verify the dates) `[off-map: Shimōsa]`
- **Bear or boar memorial (kuma-zuka / kemono kuyō-tō)**: a stone put up by hunters for the animals they killed. Mountain, occasional, small. Hook: a tell of a hunting area, lore.
- **Skinning and drying frame (kawa-hoshi-waku)**: a pole frame with a stretched hide by a stream, far from the village. Forest, rare, small. Hook: loot (hide), a danger tell (predators). (BL: rawhide yard is the town version)
- **Fish weir (yana)**: a bamboo-slat ramp across a river that strands descending ayu and eels, with a watch hut. River, occasional, large structure. Hook: FOOD, a crossing. (BL: Rural industry)
- *Basket fish trap (uke / dō / mondori)* → S116, under R §15.
- **Eel tube (unagi-zutsu / takappo)**: bamboo tubes sunk in the mud for eels. River, common, small. Hook: FOOD.
- **Stone fish-drive channel (ishi-yose)**: stone arms piled in a stream funnelling fish into a trap or shallow. River, occasional, `[terrain]`. Hook: food. (assumed)
- **Stake-lattice weir (ajiro)**: the ancient Uji and Tanakami stake weirs for ice-fish (hio). River, rare, large. Hook: lore. (verify: largely medieval) `[old: medieval, still standing 1730?]` (merge fix: older survivors are IN; verify whether the Uji and Tanakami weirs were still worked in 1730)
- *Night-fishing torch baskets (kagari)* → S117, under U Streets: Street lighting and lanterns.
- **Fishing platform over a pool (tsuri-dai)**: a plank shelf pegged over a deep pool. River, occasional, small. Hook: food. (assumed)
- **Hunting-licence post (teppō aratame no fuda)**: a board at a village edge naming the licensed hunters' guns under the 1687 registration. It's the rural face of Tsunayoshi's controls. Roadside, rare, small. Hook: lore. (assumed form; the registration is in BL)

### == W §10 Mining, quarrying, digging, hot springs ==

- **Mine adit (mabu)**: a timber-framed tunnel mouth with a spoil heap and a drainage trickle. Mountain, rare, medium. Hook: SHELTER, darkness, collapse DANGER, loot spot. (BL: Rural industry, mines)
- **Hand-dug prospect burrows (tanuki-bori)**: narrow twisting tunnels following a vein, "badger-dug". Typical of early Edo gold workings. Mountain, occasional, small (a hole) + `[terrain]`. Hook: danger (a squeeze, a collapse), shelter. (verify the term)
- **Open-cut split mountain (rotenbori / wareto)**: a hilltop split open by surface mining. Sado's Dōyū no Wareto is the landmark. Mountain, rare, `[terrain]`. Hook: LANDMARK, a fall danger. `[off-map: Sado]`
- **Mine spoil heap (zuri / ha-ishi yama)**: waste-rock heaps below the adits. Mountain, occasional, `[terrain]`. Hook: cover, a tell of a mine.
- **Abandoned mine (haikō / kyūkō)**: a collapsed adit with rotten props, a flooded shaft and rusted tools. Many Izu workings were past their peak by 1730. Mountain, rare, medium. Hook: SHELTER, DANGER, LOOT. (Toi gold mine was in use; verify which were closed)
- **Mine drainage outlet (mizunuki-kō)**: a low tunnel mouth spilling orange mine water into a stream. Mountain, rare, small. Hook: bad WATER (danger). (assumed)
- **Placer gold workings (sakin-tori-ba)**: riverbank gravels dug over and washed for gold dust. Kai's gold streams are famous from the Takeda era. River, rare, `[terrain]`. Hook: loot (panning?). (verify how active in 1730)
- **Castle-stone quarry (ishi-chōba)**: hillside and shore quarries in Izu (Atami, Itō; 170 sites) that cut stone for Edo Castle's walls in the early 1600s. Abandoned by 1730. Mountain/coast, landmark (near the Hakone map), `[terrain]` + large props. Hook: LANDMARK, cover among the blocks.
- **Abandoned marked block (kokuin-ishi / "zannen-ishi")**: a huge dressed block left behind, with its daimyō's crest cut on it and a line of wedge holes. Mountain/coast, occasional (in Izu), medium. Hook: cover, lore. (verify the name *zannen-ishi*)
- **Stone-loading point (ishi-dashi-ba)**: a rough ramp or stone jetty on the Izu coast where quarry blocks went onto barges. Coast, rare, `[terrain]`. Hook: landmark. (assumed form)
- **Whetstone or millstone quarry (toishi-yama / usu-ishi chōba)**: small quarries for whetstones (Kyoto's Narutaki) or millstones. Mountain, occasional, `[terrain]`. Hook: loot (a whetstone). (verify locations)
- **Clay pit (tsuchi-tori-ba)**: a dug-out bank for tile or pottery clay. Forest edge, occasional, `[terrain]`. Hook: cover.
- **Old kiln ruin and shard heap (koyō-ato / monohara)**: a collapsed medieval tunnel kiln on a hillside, with drifts of broken pots (Seto, Tokoname, Shigaraki areas). Forest/mountain, rare, `[terrain]`. Hook: lore, shards (loot?).
- **Sulphur workings (iō-tori-ba)**: yellow crust dug at vents, with baskets and a melting pot. Mountain, rare, smalls at a nature site. Hook: DANGER (gas). (BL: Rural industry, sulphur; verify Ōwakudani in 1730)
- **Hot-spring source troughs (yumoto no toi)**: wooden gutters and bamboo pipes carrying hot water from a vent down to bath huts. The Hakone Nanayu (seven hot springs) are next to our map. Mountain, rare, medium. Hook: WARMTH (see Stephen's hot-spring request). (BL: Services, hot-spring baths)
- **Wild riverside hot pool (kawa-yu / nozura-buro)**: a stone-dammed pool at a riverside hot spring, used by locals, hunters and animals, with no building. River/mountain, rare, `[terrain]`. Hook: WARMTH, healing, landmark. (assumed; period form to verify, per WC "Additions")
- **Hot-spring steaming ground (yu-no-hana tori)**: a flat of vents where "hot-spring flowers" (mineral crust) were harvested under thatch covers. Mountain, rare, medium. Hook: warmth, danger. (verify: the Beppu and Kusatsu dates are 18th c)
- **Ice pit (himuro)**: a stone-lined pit with a thatched roof in a cool hollow. Winter ice was stored for summer, and Kaga sent ice to the shogun each 6th month. Mountain/forest, rare, medium. Hook: lore, cold. Kaga `[off-map: Kaga]`; generic ones elsewhere (verify).

### == W §11 Mountain produce ==

- **Log beehive (hachi-dō / hachi-bako)**: hollow sugi or hinoki log (~70 cm) or a box for Japanese honeybees, stood on a stone under an overhang, by a shrine, or under the eaves; Kishū (Kumano) and Tosa honey are famous. Forest/yard, occasional (forest) / rare (yard), small. Hook: FOOD (honey), mild danger (stings). (depicted 1799 `[outside]`, practice earlier; verify) {seam S118: W §11 + R §7}
- **Cliff hive row (iwa-dō)**: a row of box or log hives set on a rock ledge under an overhang. Mountain, rare, medium. Hook: food, a climbing hazard. (assumed from the Kumano practice)
- *Lacquer tree with tapping scars (urushi no ki)* → S018, under N §C.
- **Tapper's sap tub on a tree (urushi-oke)**: a small wooden cup or tub hung at a scored lacquer tree. Forest, rare, small. Hook: loot (lacquer), danger (rash). (assumed)
- **Resin-tapped pine (matsu-yani)**: pine with V-scars for resin or cut-out fatwood for torches (taimatsu). Forest, occasional, small. Hook: FIRE (torch material). (assumed for the period)
- **Famine root-digging ground (warabi-ne hori-ba)**: a slope pocked with holes where bracken and kudzu roots were dug for starch in hunger years (Kyōhō famine 1732). Mountain, occasional, `[terrain]`. Hook: food (poor), a tell of hardship. (verify the extent)
- **Nut-gathering claim marks (tochi / kuri no shime)**: straw knots tied to horse-chestnut or chestnut trees, claiming the harvest for a household. Forest, occasional, small. Hook: food. (assumed; see §13 claim stakes)
- *Wild-grass cutting ground (kaya-ba / kari-shiki-ba)* → S007, under N §E.
- **Medicinal-herb garden in the hills (yakuen / yakusō-bata)**: a domain or shogunal herb plot in the hills, fenced and signed. Yoshimune pushed native herb cultivation in the 1720s. Mountain, rare, medium `[terrain]`. Hook: FOOD/medicine loot, landmark. (verify; Komaba and Koishikawa are urban)

### == W §12 River and slope works ==

- **River crib spur and groyne (seigyū / waku / dashi / hane)**: triangular or box timber frames (about 6 × 4 m) weighted with stone-filled gabions, and stone or pile spurs jutting from a bank, pushing the current off the bank. River, occasional, medium–large. Hook: cover in water, crossing hazard, landmark, fishing spot. (verify names and period) (BL: Civic "names only") {seam S119: W §12 + R §2 + U Water: Canals}
- **Bamboo gabion (jakago)**: long bamboo "snake baskets" packed with river stones, laid along banks and round weirs. River, common, medium. Hook: cover, stones and bamboo. {seam S120: W §12 + R §2}
- *Open staggered levee (kasumi-tei)* → S121, under R §1.
- *Groyne (dashi / hane)* → S119, under W §12.
- **Great embankment with a founder's shrine (Bunmei-zutsumi)**: Sakawa River bank near Odawara, rebuilt by Tanaka Kyūgu and finished in 1726 after 1707 Fuji ash choked the river and floods broke the old bank (1711). It has a shrine to Yu the Great (Bunmei). River, landmark (near the Hakone map), large `[terrain]`. Hook: LANDMARK, a raised path.
- **Irrigation tunnel (manbo / mabu / zuidō) and the Hakone Yōsui**: hand-dug tunnel bringing water through a ridge; the Hakone (Fukara) Yōsui, 1666–70, takes Lake Ashi water ~1.3 km under the western caldera rim to the Susono / Fukara fields, intake and outlet in the wild. Mountain/field, rare / landmark (Hakone map), `[terrain]` + portal. Hook: WATER, hidden route, a crawlable tunnel?, landmark. (verify length and dates) {seam S122: W §12 + R §2}
- *Stone diversion weir (seki / iseki)* → S123, under R §2.
- *Bamboo-grove bank protection (mizu-bōbi no takeyabu)* → S006, under R §1.
- **Flood-level mark (kōzui-hi / mizu-jirushi)**: a carved line or stone recording a great flood's height. River, rare, small. Hook: lore, danger tell. (verify for the window)
- **Slope-planting or erosion barrier (sunadome)**: rows of stakes, brush and planted pines on bare slopes, following the 1666 shogunal order on mountains and rivers against root-digging. Mountain, occasional, `[terrain]`. Hook: cover. (verify)
- **Volcanic sand dump heaps (suna-yama / suna-zuka)**: after Fuji's 1707 Hōei eruption, farmers east of Fuji (the Mikuriya area, Gotemba) shovelled ash off their fields into heaps and trenches. In 1730 they're still there. Plain/ foothill, occasional (Fuji region), `[terrain]`. Hook: a unique wasteland look, cover.
- *Ash-buried abandoned field (suna-ume no hatake)* → S009, under N §E.
- **Landslide dam remains (sekitome-ko no ato)**: a debris dam across a valley with the drowned trees of a temporary lake, like the ash dams on the Sakawa. River/mountain, rare, `[terrain]`. Hook: danger, landmark. (verify)

### == W §13 Boundaries, bans and control ==

- *Province boundary post (kokkyō-gui / kokkyō-hi)* → S124, under R §12.
- **Paired border mounds (sakai-zuka)**: small earth mounds, like mile mounds, on each side of a road at a province or domain line. Roadside, rare, medium `[terrain]`. Hook: navigation. (verify)
- **Border ditch between provinces (Nemonogatari no sato)**: on the Nakasendō at Imasu, a ditch only a few feet wide split Mino from Ōmi, so people could talk across it lying in bed. Roadside, landmark, small `[terrain]`. Hook: lore, landmark. (verify)
- *Domain boundary stake (ryōbun-gui / ryōkai-hi)* → S124, under R §12.
- *Village boundary stone (mura-zakai ishi)* → S125, under R §12.
- *Village boundary rope (kanjō-nawa / kanjō-kake)* → S126, under R §13.
- **Straw giant at a village edge (Kashima-sama / Shōki-sama)**: huge straw warrior figures guarding the road into a village. Mostly Akita and Echigo. Roadside, rare, medium/large. Hook: an EERIE landmark. `[off-map: Tōhoku / Echigo]` (verify the Edo dating)
- **Disease-sending straw offerings (okuri-ningyō / hōsō-gami okuri, sandawara)**: straw dolls, straw boats, rice-bale lids with red paper streamers and red gohei, left at the village edge or roadside or floated away after a rite to send off smallpox or pests. Roadside/river, occasional, small. Hook: eerie, lore, disease flavour. (placement assumed) {seam S127: W §13 + R §13}
- **Forbidden-forest marker (tomeyama / sudome-yama sakai-gui)**: stakes and boards marking a reserved forest. Owari banned cutting four Kiso trees in 1708 and a fifth in 1718, under the slogan "one tree, one head". Forest, rare, small. Hook: DANGER (the law, patrols), prime timber.
- **Forest notice board (yama-kōsatsu)**: a roofed board at the forest entrance listing banned trees and penalties. Forest, rare, medium. Hook: lore, a danger tell. (assumed form) (a forest-guard hut, if needed, belongs in BL)
- **Reserved-tree mark (tome-ki shirushi)**: a blaze, brand or rope on individual protected trees. Forest, occasional, small. Hook: a tell. (assumed)
- **Shogun's falconry-ground boundary post (otakaba sakai-gui)**: posts marking the shogun's hawking preserve around Edo (~1,600 km², all hunting banned inside). Abolished under Tsunayoshi and restored by Yoshimune in 1716. Bird wardens (torimi) patrolled it. Roadside/forest, rare, small. Hook: a no-hunting zone, lore. (verify the post form) `[off-map-ish: Edo plain]`
- **"Killing forbidden" stone (sesshō kindan-seki)**: a stone pillar at a temple's river or hill banning fishing and hunting. Laws of Compassion era, 1687–1709. River/forest, occasional, small. Hook: a no-hunting zone, lore. (verify examples)
- **Commons claim stake (shime / shime-gui)**: a stick with a straw knot claiming grass, firewood or mushroom rights on common land. Forest, common, small. Hook: a tell of village use. (assumed; the *shime* sign is well known)
- **Checkpoint palisade up the slope (sekisho no yarai / sakumono)**: fences and walls running up the hillside from a sekisho to block bypasses, as at Hakone (between the lake and the steep ridge). Mountain, rare (landmark at Hakone), large `[terrain]` (linear). Hook: a BARRIER, danger (sekisho-yaburi was punishable by death). (verify the Hakone extent) (BL: Government, sekisho)
- **Bypass-path warning board (nuke-michi kinshi fuda)**: a notice on a side path warning that evading the checkpoint is forbidden. Mountain, rare, small. Hook: danger tell, navigation (a bypass exists). (assumed)
- *Remote lookout post of a checkpoint (tōmi-ban)*: *cross-reference, not counted*: BL (Military, coastal lookout; sekisho lookout).
- *Domain border checkpoint (kuchi-dome bansho)*: *cross-reference, not counted*: BL, Government.
- **Pole barrier across a road (kari-kido)**: a temporary pole or rope across a road during an inspection, epidemic or manhunt. Roadside, rare (event), small. Hook: an event barrier. (assumed)
- **Grass-fire firebreak (hi-yoke no kari-michi)**: a mown strip between grassland commons and forest, kept before spring burning. Mountain, occasional, `[terrain]`. Hook: navigation, fire. (assumed)
- *Tax-land survey boundary stone (kenchi sakai-ishi)* → S128, under R §3.
- **Hunting-ground notice board (kariba kōsatsu)**: a board at the entrance of a domain hunting preserve. Forest, rare, small. Hook: danger (a ban). (assumed)
- **Wolf-charm post (ōkami ofuda-gui)**: a post or tree hung with Mitsumine or Ontake wolf talismans against thieves and boar, at the field edge. Forest edge, occasional, small. Hook: lore. (verify the placement; the charms are Edo)

### == W §14 Lookouts, beacons and signals ==

- **Beacon hill (noroshi-ba / noroshi-dai)**: a cleared summit with a stone or earth hearth, wood stacks and a hut. The 17th-c chains ran toward Nagasaki; many coastal chains are 1800s. Mountain/coast, rare, medium. Hook: FIRE, a long VIEW, navigation (a summit landmark). (BL: Military, beacon post)
- **Sengoku beacon mound (noroshi-dai ato)**: a levelled earth platform on a peak from Warring States signal chains (Takeda, Hōjō). Mountain, occasional, `[terrain]`. Hook: a VIEW point, cover.
- **Open lookout platform (monomi-dai)**: a pole platform or cleared knoll with no hut, on a headland or pass. Mountain/ coast, rare, medium. Hook: a VIEW point, a sniping spot. (assumed)
- **Weather-watch hill with a direction stone (hiyori-yama / hōi-ishi)**: a hill above a port with a compass-rose stone carved with the 12 directions, used by pilots to read the weather. Coast, rare, small on a hill. Hook: NAVIGATION (a literal compass), view. (BL: Civic, weather-watching hill)
- **Fish-spotting knoll (uomi-dai)**: a clear headland seat where a spotter watched for sardine or yellowtail shoals and signalled the boats. Coast, occasional, small/`[terrain]`. Hook: view. (BL has the tower version)
- **Whale lookout (kujira yamami)**: headland lookouts of the net-whaling groups. Coast, rare, medium. Hook: view. `[off-map: Kii / Kyushu]`
- **Flag-signal relay hill (hata-furi yama)**: hills used to relay Osaka rice prices by flags or mirrors. Mountain, rare, small. Hook: landmark. (verify: may be after 1750)
- **Harbour and beach guide fire (kagari-bi no ba / hama-bi)**: stone-ringed fire place or iron basket on a point or beach, lit to guide boats home at night. Coast, occasional, small. Hook: FIRE, light, navigation. (assumed) {seam S130: W §14 + R §15}
- *Sekisho hill lookout*: *cross-reference, not counted*: BL.
- **Survey marker (sokuryō-hyō)**: Inō Tadataka's survey stations and marks. Mountain/coast, rare, small. Hook: navigation. `[outside 1680-1750: 1800–1816]`
- *Signal bell or drum post at a wild ferry*: see §4 (not counted twice).
- *Mountain-top prayer fire for rain (amagoi-bi)* → S129, under R §13.
- **Echo or call rock (yobi-iwa)**: a rock from which shepherds and woodsmen called across a valley. Mountain, rare, `[terrain]`. Hook: lore. (assumed; cut candidate)

### == W §15 Ruins: castles, forts, barriers ==

- **Mountain castle ruin (yamashiro-ato)**: Sengoku earthworks along a ridge: terraces, cut moats, earth ramparts, overgrown and treed. Mostly abandoned after 1615's one-castle-per-province order. Mountain, occasional, large `[terrain]`. Hook: LANDMARK, a defensible position, VIEW, loot spot.
- **Ridge-cut moat (horikiri)**: deep trench across a ridge cutting a hill castle off from its approach; on abandoned Sengoku sites `[old: Sengoku, still visible 1730]`. Mountain, occasional, `[terrain]`. Hook: cover, chokepoint, fall danger. {seam S132: W §15 + U Castle: Earthworks}
- **Vertical slope moats (tatebori / une-bori)**: trenches down a slope, sometimes in ribbed rows (Yamanaka castle near Hakone, abandoned 1590). Mountain, occasional, `[terrain]`. Hook: cover. {seam S133: W §15 + U Castle: Earthworks}
- *Earth rampart (dorui)* → S134, under U Castle: Earthworks.
- **Castle terraces (kuruwa)**: levelled enclosures stepping down a hill, now grass or forest. Mountain, occasional, `[terrain]`. Hook: open camp sites, views.
- **Deliberately broken stone walls (hajō no ishigaki)**: stone walls with their corners pulled down when the castle was slighted. Mountain, rare, medium. Hook: cover, landmark.
- *Castle well (jō-ido)* → S131, under U Castle: Earthworks.
- **Gate site with foundation stones (koguchi-ato)**: a bent entrance through the ramparts with post stones. Mountain, occasional, small `[terrain]`. Hook: cover, navigation.
- **Ridge fortlet (toride-ato)**: a small single-terrace fort or outpost. Mountain, occasional, `[terrain]`. Hook: view, cover.
- **Yamanaka Castle ruin (Hakone)**: the Hōjō castle straddling the Tōkaidō on the Hakone pass, taken by Hideyoshi in half a day in 1590. Famous for its grid "shōji-bori" moats. Mountain/roadside, LANDMARK (Hakone map), large `[terrain]`. Hook: landmark, cover, a chokepoint.
- **One-night castle (Ishigakiyama Ichiya-jō)**: Hideyoshi's 1590 siege castle overlooking Odawara, the first stone-walled castle in the Kantō. Mountain, LANDMARK (near Hakone), large `[terrain]`. Hook: landmark, view.
- **Siege-camp earthworks (jin-ato / jinsho-ato)**: banks and terraces of besiegers' camps ringing an old siege site, such as the 1590 Odawara ring. Mountain/plain, rare, `[terrain]`. Hook: cover.
- **Ancient barrier site (kosekisho-ato)**: long-abolished classical barriers: ; Fuwa no seki on the Nakasendō near Sekigahara (673–789), visited by Bashō in 1684 ; Ashigara no seki on the Ashigara pass (899), next to Hakone ; Suzuka no seki Roadside/mountain, rare (landmark), `[terrain]` + a marker. Hook: lore, landmark.
- **Medieval moated residence (yakata-ato / hōkei-yakata)**: a square moat and bank of a Kamakura–Muromachi warrior house, now a copse in fields. Forest edge, occasional, `[terrain]`. Hook: cover.
- **Castle-road stone steps (jōdō no ishidan)**: overgrown stone stairs climbing to a castle ruin from the valley. Mountain, rare, `[terrain]`. Hook: navigation.
- **Ancient mountain fortress stone wall (kōgoishi / kodai sanjō)**: a 7th-c Korean-style stone ring wall around a hill. Mountain, rare, large `[terrain]`. Hook: landmark. `[off-map: western Japan]`
- **Castle ruin memorial shrine (shiro-ato no hokora)**: a hokora or stone on the top terrace for the fallen lord. Mountain, occasional, small. Hook: landmark.
- **Demolished-castle foundation (tenshu-dai ato)**: an empty keep base of stone on a lowland castle abandoned under the 1615 order. Plain/hill, rare, medium. Hook: landmark, view.
- **Battlefield field marker (kosenjō no hi)**: a stone or pine marking a famous battle spot (Sekigahara, Okehazama). Roadside, rare, small. Hook: lore, landmark. (verify which were marked before 1750)

### == W §16 Ruins: settlements, temples, work sites ==

- **Abandoned hamlet (haison / tsubure-mura)**: collapsed thatched houses, overgrown fields and a dry well. Villages were lost to famine (Kyōhō, 1732, in window), landslide, flood and the 1707 ash. Forest/mountain, rare, large. Hook: LOOT spot, shelter (partial), landmark.
- **Abandoned farmstead (tsubure-byakushō no ato)**: one fallen house, foundation stones, a bamboo grove and a persimmon tree. Forest edge, occasional, medium. Hook: loot, a partial shelter.
- **Terraced fields gone back to forest (arehata)**: stone-walled terraces under young trees. Mountain, occasional, `[terrain]`. Hook: cover, navigation (a village was near).
- **Ancient temple foundation stones (haiji-ato / soseki)**: the cornerstones and pagoda base of a Nara-period temple (such as the provincial kokubunji) in a field or wood. Plain/forest, occasional, medium. Hook: landmark, lore.
- **Ruined mountain temple (sanrin haiji)**: terraces, toppled stupas, a broken gate base and moss-covered steps of a temple burned in the Sengoku wars. Mountain, rare, large `[terrain]`. Hook: landmark, loot spot.
- **Collapsed hermitage (iori-ato)**: a hearth stone, a scatter of tiles or thatch and a spring. Mountain, occasional, small. Hook: water, loot.
- **Old well in the woods (furu-ido)**: a stone ring half hidden in undergrowth. Forest, occasional, small. Hook: WATER, DANGER (fall).
- **Fallen shrine (yashiro-ato)**: a collapsed hokora and a toppled torii in a grove. Forest, occasional, small. Hook: lore, landmark.
- **Burned hut remains (yake-goya)**: charred posts and a stone hearth. Forest, occasional, small. Hook: loot, a danger tell.
- **Old ironworks slag heap (kanakuso-yama)**: glassy slag heaps from small bloomeries. Mountain, rare, `[terrain]`. Hook: lore. (the big tatara are `[off-map: Chūgoku]`) (assumed elsewhere)
- **Old road station ruin (kyū-shuku ato)**: foundations of a post-station hamlet bypassed when the road moved. Roadside, rare, medium. Hook: loot, shelter. (assumed)
- *Abandoned salt works*: see §19 (not counted twice).
- **Abandoned work camp (soma-goya ato)**: a logging-camp clearing with a collapsed long hut, a rusted saw blade and sawdust drifts. Forest, occasional, medium. Hook: loot (tools), shelter (partial).
- **Abandoned mountain shrine path (haidō)**: an overgrown stair and torii line leading to nothing. Mountain, rare, `[terrain]`. Hook: navigation, eerie.

### == W §17 Graves, mounds and memorials ==

- **Keyhole tomb mound (zenpō-kōen-fun)**: a huge forested mound, sometimes moated, with a shrine or trees on top. The shogunate surveyed and repaired imperial tombs in 1697–99 (in window). Plain/forest, landmark (Kinai), large `[terrain]`. Hook: LANDMARK, cover, forest. (verify the details of the Genroku repair)
- **Small round tomb mound (enpun / gunshūfun)**: clusters of small round mounds in woods and fields, often with a hokora on one. Common in the Kinai and Kantō. Forest/plain, common (regionally), medium `[terrain]`. Hook: cover, landmark.
- **Exposed stone burial chamber (sekishitsu)**: a tomb whose earth has eroded away, leaving huge stones and an open chamber (Asuka's Ishibutai type). Plain/forest, rare (landmark), large. Hook: SHELTER (cave-like), landmark.
- **Cliff tomb holes (yokoana-bo)**: rows of small chambers cut into a soft-rock cliff (Yoshimi Hyakuana, Saitama). Mountain/river, rare, `[terrain]`. Hook: SHELTER, eerie. (verify how visible they were pre-1887)
- **Kamakura rock-cut tombs (yagura)**: square caves cut into cliffs around Kamakura and Miura, 13th–16th c, with gorintō inside. Mountain, occasional (Kamakura area), small caves. Hook: SHELTER, lore.
- *Lone medieval gorintō (gorintō)* → S135, under R §11.
- **Traveller's grave (yukidaore-baka / tabibito no haka)**: small roadside stone for someone who died on the journey, buried by the nearest village, sometimes with name and home province. Roadside/commons, occasional, small. Hook: lore, danger tell. (detail assumed) {seam S136: W §17 + R §12}
- *Unclaimed-dead heap (muen-zuka)* → S137, under U Religious: Graveyards and grave markers.
- *Burial-only grave in the hills (ume-baka)* → S138, under R §9.
- **Battle head mounds (kubizuka / dōzuka)**: mounds over the heads or bodies of the slain. Sekigahara's east and west kubizuka (1600) sit on the Nakasendō. Roadside, landmark, medium `[terrain]`. Hook: LANDMARK, eerie.
- **Thousand-person mound (sennin-zuka)**: a mass grave from battle, plague or famine, with a stone. Forest/roadside, rare, medium `[terrain]`. Hook: eerie, landmark.
- *Famine memorial (kikin kuyō-tō / gashi-zuka)* → S139, under R §11.
- **Earthquake and tsunami memorial (jishin kuyō-tō / tsunami-hi)**: stones for the Genroku quake (1703, which wrecked Odawara) and the Hōei quake and tsunami (1707). Roadside/coast, occasional (W) / rare (R), small. Hook: lore. (verify surviving in-window stones; many famous tsunami stones are 1854) {seam S140: W §17 + R §15}
- *Animal memorial (chikurui kuyō-tō)*: *see §9 (hunters') and §5 (horses)*, not counted again.
- **Whale grave (kujira-haka)**: graves for whale foetuses and whales killed by whalers. Seigetsu-an in Nagato dates to 1692. Coast, rare, small. Hook: lore. `[off-map: Nagato]`
- *Drowned-sailor memorial (suinan kuyō-tō)*: *see §20* (not counted here).
- *Wooden grave tablets (sotoba) at a hill grave* → S102, under R §11.
- **Hokora on a tomb mound (fun-jō no hokora)**: a tiny shrine on a kofun, which villagers treated as a kami's hill. Plain/forest, occasional, small. Hook: landmark.
- **Hermit or ascetic's grave (nyūjō-zuka)**: a mound where an ascetic was buried alive, meditating, with a breathing tube and bell. Edo examples exist. Mountain, rare, medium `[terrain]`. Hook: EERIE landmark, lore. (verify the in-window examples)
- **Sutra-and-grave mound on a pass (tōge no tsuka)**: a mound at a pass top for dead travellers, with a stone Buddha. Mountain, rare, medium. Hook: navigation, lore. (assumed)
- *Plague-dead burial pit marker (ekishi-zuka)* → S139, under R §11.
- **Buried-coin and urn hoard (maizō-sen)**: a medieval coin hoard in a jar, turned up by ploughs and landslides. Forest, rare, small. Hook: LOOT (coins). (assumed as a find, not a placed object)
- **Grave of the executed (keishi-sha no haka)**: a daimoku stone or Jizō near an execution ground for the unclaimed executed. Roadside, rare, medium. Hook: eerie. (see §18)

### == W §18 Disaster, execution and punishment marks ==

- **Execution-ground memorial (keijō no kuyō-hi)**: the stones outside the fence at an execution ground by the highway approaches: ; Suzugamori (Tōkaidō, 1651) has a daimoku stone ; Kozukappara's great Jizō dates from 1741 Roadside, landmark (urban edge), medium. Hook: EERIE landmark. (BL: Government, execution grounds)
- **Rural exposure or execution spot**: a bare clearing near the scene of a rural crime, with a post-base stone and a small Jizō. Roadside, rare, small. Hook: eerie. (assumed)
- **Otama pond marker (Otama-ga-ike)**: the pond near the Hakone sekisho named for Otama, executed in 1702 (Genroku 15) for trying to slip round the checkpoint. The pond is nature; the marker and story are man-made. Mountain, LANDMARK (Hakone map), small at a nature site. Hook: lore, a danger tell (don't bypass). (verify the 1702 date)
- **Head-display stand remains (gokumon-dai no ato)**: a plank stand base by a road near a jail town. Roadside, rare, small. Hook: eerie. (BL: Government)
- *Landslide scar with a Jizō (yama-kuzure no Jizō)* → S048, under N §T.
- **Flood-death memorial (suigai kuyō-tō)**: a stone by a river for flood dead. River, occasional, small. Hook: danger tell.
- **Eruption shelter or ash trench (suna-yoke bori)**: ditches and banks thrown up against ash drift on fields in the Fuji foothills after 1707. Plain, rare, `[terrain]`. Hook: cover. (assumed; tied to §12)
- **Burned-forest boundary (yamabi-ato)**: a black stand of burned trunks from a spread grass fire, with a firebreak. Forest, occasional, `[terrain]`. Hook: open ground. (the nature agent overlaps)
- **Avalanche or rockfall warning post (nadare-chūi no fuda)**: a board at a dangerous stretch of road. Mountain, rare, small. Hook: DANGER tell. (assumed; very uncertain for the period)

### == W §19 Wild coast: work ==

**Cross-reference, not counted: the lone fisherman's hut (ryōshi no koya), divers' fire hut (ama-goya) and salt-boiling hut (kama-ya) are BL.**
- **Divers' beach fire ring (ama no takibi-ba)**: a stone ring on the sand where women divers warm up between dives. Coast, occasional, small. Hook: WARMTH, fire.
- *Boat haul-up beach (funa-age-ba)* → S141, under R §15.
- **Upturned boat on the shore (fuse-bune)**: a small boat turned over above the tide line. Coast, occasional, medium. Hook: SHELTER (crawl under), cover. (assumed)
- *Net-drying poles (ami-hoshi-ba)* → S142, under R §15.
- *Seaweed-drying poles and mats (kaisō hoshi-ba)* → S143, under R §15.
- *Nori stakes in the shallows (nori-hibi)* → S144, under R §15.
- **Abandoned salt field (shio-hama ato)**: a salt field gone back to rough sand, with a collapsed boiling hut, a cracked clay pan and a brine pit. Coast, rare, medium. Hook: loot, shelter (partial), landmark. (BL: salt fields, live)
- *Driftwood stacks (yorigi no tsumi)* → S053, under R §15.
- *Octopus pots stacked on the shore (tako-tsubo)* → S145, under R §15.
- *Tidal stone fish trap (ishi-hibi / sukui)* → S146, under R §15.
- **Tiny stone jetty in a cove (ko-hatoba)**: a rough dry-stone arm sheltering a landing. Coast, occasional, medium. Hook: a landing, cover.
- *Mooring stones and posts (funa-tsunagi ishi / tomo-gui)* → S147, under U Water: Canals.
- *Sand fence (suna-yoke gaki)* → S148, under R §8.
- *Planted coastal pine belt (bōfū-rin / bōsa-rin)* → S003, under N §E.
- *Shell-burning lime pit (kaibai-yaki)* → S149, under R §15.
- *Beach net-hauling capstan (ami-biki no rokuro)* → S141, under R §15.
- *Tengusa diving float (ama no tarai)* → S150, under R §15.

### == W §20 Wild coast: navigation, wrecks, sacred ==

- *Stone lighthouse lantern (tōmyōdō / jōyatō)* → S070, under W §3.
- **Channel stakes (miotsukushi)**: tall stakes marking the deep channel into a river mouth or bay; they're Osaka's emblem. Coast/river, occasional, medium. Hook: NAVIGATION (the safe line), a wading hazard.
- **Reef warning pole (ansho-gui)**: a pole or brush bundle on a submerged rock. Coast, occasional, small. Hook: navigation, danger. (assumed)
- **Stranded cargo ship (nanpa-sen)**: a beached or reef-wrecked coastal freighter (bezaisen / higaki-kaisen type) with a broken mast, rice bales and sake barrels spilled. Wrecks were frequent in era. Coast, rare, large structure. Hook: LOOT SPOT, shelter, landmark.
- **Wreck debris line (hyōchaku-butsu)**: planks, barrels, cordage, a rudder and a mat sail strewn along a beach after a storm. Coast, occasional, smalls. Hook: LOOT.
- *Beached anchor (ikari)* → S151, under R §15.
- **Salvage marker (hyōchaku-fuda)**: a village board noting wreck goods held for the owner, as law required. Coast, rare, small. Hook: lore. (verify)
- **Drowned-sailor memorial (suinan kuyō-tō)**: a stone on a headland for the lost at sea. Coast, occasional, small. Hook: landmark, lore.
- *Ebisu stone (Ebisu-ishi)* → S152, under R §15.
- **Dragon-god hokora on a headland (Ryūjin no hokora)**: a fishermen's shrine to the sea dragon. Coast, occasional, small. Hook: landmark.
- **Sea torii (iso no torii / umi no ōtorii)**: torii standing on rocks or in the shallows facing a sea shrine. Coast, rare, medium–large. Hook: LANDMARK. Itsukushima `[off-map: Aki]`; small reef torii elsewhere (assumed). {seam S153: W §20 + U Religious: Torii by style}
- **Konpira sea-safety stone (Konpira-hi)**: a stone to the sailors' god Konpira on a harbour point. Coast, occasional, small. Hook: landmark. (verify how far Konpira had spread east by 1730)
- **Island hermitage path (shima-mairi michi)**: a tidal path or stepping stones to a small shrine island, usable only at low tide. Coast, rare, `[terrain]`. Hook: navigation, danger (the tide).
- *Sea cave with a shrine (umi no iwaya)*: see §6, Enoshima (not counted twice).
- **Pilot's alignment marks (yama-ate no shirushi)**: whitewashed rocks or a lone planted tree on a hill used by boatmen to line up a harbour entrance. Coast, rare, small. Hook: navigation. (assumed; *yama-ate* the practice is real)

### == W §21 Traces, camps and props of passage ==

- **Discarded straw sandals (sute-waraji)**: worn-out sandals thrown aside every few ri along a road. Roadside, common, small. Hook: a tell that the road is used, tinder.
- **Horse straw shoes (uma-gutsu / uma-waraji)**: packhorses wore straw shoes that wore through fast, and the cast shoes littered the road. Roadside, common, small. Hook: a tell.
- **Horse droppings (bafun)**: constant on post-town streets and highways; collected by farmers as manure near villages, left lying far from them. Roadside/street, common, small decal. Hook: a tell. (assumed) {seam S154: W §21 + U Streets: Street surface}
- **Broken palanquin or pack saddle (yabure-kago / ni-gura)**: a smashed kago or a wooden pack saddle dumped below a road edge. Roadside, rare, small. Hook: LOOT (rope, wood), lore.
- **Dead packhorse**: a horse carcass in a ravine below a steep bend, the reason for a batō Kannon. Roadside/mountain, rare, small. Hook: danger tell, scavengers (danger).
- **Lost pilgrim kit (kongō-zue, sugegasa)**: a pilgrim's staff and sedge hat in the undergrowth. Mountain, occasional, small. Hook: LOOT.
- **Straw raincoat on a branch (mino-kake)**: a straw cape hung on a tree to dry or left behind. Forest, occasional, small. Hook: LOOT (rain gear).
- **Woodsman's lean-to (sashikake-goya)**: two forked poles, a ridge pole and a bark or bough roof against a slope. It's the most basic shelter. Forest/mountain, occasional, medium. Hook: SHELTER. (no interior, so it stays here; BL has hut versions)
- **Bough bivouac under a big tree (ki-shita no nejiro)**: a flattened bed of cut boughs and a small fire under a sheltering conifer. Forest, occasional, small. Hook: shelter (poor), fire.
- **Bandit lair (sanzoku no nejiro / oihagi no kakure-ga)**: a lean-to in a gully above a pass with a lookout rock, stolen bundles and a fire pit. Highwaymen (oihagi) are well attested; the lair form is gameplay invention. Mountain, rare, medium. Hook: DANGER, LOOT SPOT. (assumed)
- **Ambush screen (fuse-zei no kakure)**: cut brush propped at a road bend. Roadside, rare, small. Hook: danger, cover. (assumed)
- **Porter's waiting spot (kumosuke tamari)**: a trampled bank at a pass foot with a fire ring, straw ends and a bench, where freelance porters waited for fares. Roadside, occasional, small. Hook: a tell, fire. (assumed)
- **Carved graffiti on a rock or tree (rakugaki)**: names and dates cut by pilgrims into rocks, trees and pass shrines (a well-known Edo habit at shrines). Mountain, occasional, small decal. Hook: lore.
- **Offering coins and rice on a stone (sai-sen)**: coins and rice grains left on a roadside stone. Roadside, common, small. Hook: loot (a moral choice, Stephen decides).
- **Tethered-horse scrape (uma-tsunagi no ato)**: churned ground and a gnawed post where horses waited. Roadside, occasional, `[terrain]`. Hook: a tell.
- *Abandoned carrying pole and baskets (tenbin-bō, kago)* → S155, under U Streets: Peddlers'.
- **Hidden cache in a tree hollow or cairn (kakushi-ba)**: a bundle wrapped in oiled paper, pushed into a hollow. Forest, rare, small. Hook: LOOT. (gameplay; assumed)
- **Trail of paper talismans (ofuda)**: talismans pasted on trees, rocks and gate posts along a pilgrim trail. Mountain, occasional, small decal. Hook: navigation. (assumed)
- **Woodsman's water gourd hung on a branch (hyōtan-kake)**: a gourd hung by a spring for anyone to drink. Forest, occasional, small. Hook: WATER tell. (assumed)
- **Abandoned tea-stall shell (hai-chaya)**: a collapsed roadside stall frame, benches rotting, on a stretch where the traffic moved. Roadside, rare, medium. Hook: shelter (partial), loot. (a ruin state of BL's kake-jaya)

## 2.R Rural man-made (R_RURAL.md): 307 entries

### == R §1 Rice paddies and paddy landforms ==

- **Flat paddy and paddy rice (hira-ta; ine)**: flooded plots on every plain and valley floor water can reach, irregular in shape in 1730 (the rectangular grid is Meiji, 1899 law: verify date). Uruchi and mochi rice. Ground in three states (flooded, drained, cracked) and growth stages (N §Y). Field, dominant (lowland), `[terrain]`. Hook: the staple and the currency (koku); straw is the universal material; muddy undrinkable water, slow wading, wide open sightlines. {seam S020: R §1 + N §O + N §S}
- **Stone-walled terraced paddy (tanada, ishizumi)**: small paddies stepped up a hillside behind dry-stone walls, built by families over generations; mountain villages and valley sides. Field, common in hills, `[terrain]` + large walls. Hook: climbing route, cover behind walls, landmark views.
- **Earth-bunded terraced paddy (dozumi tanada)**: cheaper terraces with grassed earth risers instead of stone. Field, common in hills, `[terrain]`. Hook: grassy slopes are fast but exposed.
- **Wet deep-mud paddy (shitsuden / fukada / numata)**: undrainable valley-bottom and delta paddies with knee- to waist-deep mud, worked with paddy boats and mud boards; one crop a year only. Field, occasional, `[terrain]`. Hook: very slow movement, stamina drain, a real trap in a chase.
- **Paddy bund (aze / kuro)**: the raised earth path, 30–60 cm wide, that divides and holds each paddy; re-plastered with mud every spring (aze-nuri). Field, common, `[terrain]`. Hook: the only fast path across paddy country.
- *Bund-top soybeans (aze-mame)* → S024, under R §3.
- **Seedling bed (nawashiro)**: a small, carefully levelled plot near the house or the water inlet where rice is sown thick in spring before transplanting. Field, common (spring), `[terrain]` small. Hook: season marker; food nothing. See minakuchi offering (§14).
- **Double-cropped paddy with winter barley ridges (nimōsaku-den)**: in Kinai the drained paddy grows barley or wheat on ridges over winter, flooded again in early summer. Field, common in Kinai, `[terrain]` (seasonal variant). Hook: food (barley), a second paddy look for winter. Src: NGZ (Kinai double cropping) (verify).
- **Harvested stubble paddy (inakabu no ta)**: autumn-winter paddy of cut stubble rows, dry or half-dry. Field, common (seasonal), `[terrain]`. Hook: walkable in autumn, the season swap for paddy ground.
- **Raised strip fields with creeks (horiage-ta / kuriku / hori-ta)**: in low deltas, soil was dug out to raise strips for rice or crops, leaving narrow creeks between them used by small boats. Field, occasional (Osaka lowland, Kiso delta, Kanto river lowlands), `[terrain]`. Hook: boat routes, water everywhere, maze-like. (verify for Osaka)
- **Ring dyke (wajū tei)**: an embankment enclosing a village and its fields against floods, Kiso–Nagara–Ibi delta (Mino/Owari). Field, rare (regional), `[terrain]` large. Hook: landmark, high dry route. BL: flood farmhouse.
- **Sea dyke of reclaimed land (shinden tsutsumi / shio-dome)**: earth-and-stone bank holding back the sea or a lagoon for new paddy; the Kyōhō reforms (1720s) pushed exactly this kind of reclamation. Shore/field, occasional, `[terrain]` large. Hook: long straight high route along the coast. Src: Kyōhō shinden kaihatsu (1722 notice) (verify).
- **River levee with planted bamboo (tsutsumi / dote, suibō-rin)**: earth levees along rivers planted with bamboo (and willow) whose roots bind the soil in floods: Kiso, Nagara, Ibi, Tama, Sakawa. In towns the bank carries willow or cherry instead (Sumida cherries, 1717). River/field/town, common on big rivers, `[terrain]` + bamboo. Hook: high ground, flood-bank cover, bamboo, landmark (town cherry banks). (assumed practice, verify period) {seam S006: R §1 + N §E + W §12 + U Water: Canals}
- **Open staggered levee (kasumi-tei)**: overlapping, broken levee sections with gaps that let floodwater back-flow and drain; the Takeda "Shingen-zutsumi" on the Kamanashi is the model, still used in the Edo period. River/field, occasional (Kōshū, Kantō), `[terrain]`. Hook: odd levee geometry, landmark, cover, navigation. (verify) {seam S121: R §1 + W §12}
- *Lotus-root field (hasu-da / renkon-ta)* → S043, under N §M.
- *Taro wet field (ta-imo, mizu-imo)* → S030, under R §3.
- **Rush field for tatami (igusa-da)**: flooded fields of soft rush for tatami covers. Field, rare (occasional at the Ōmi end), `[terrain]`. Hook: crafting (mats, wicks). `[off-map: Bingo/Bitchū; some Ōmi]` (verify) Wild rush: N §I. {seam S044: R §1 + N §Q}

### == R §2 Irrigation and water control ==

- **Main irrigation channel (yōsui / segi / ide)**: an earth or stone-lined channel from a weir, threading through the village and past the houses; it also served for washing. Field/yard, common, `[terrain]`. Hook: water (boil first), the spine of village layout. BL: §2.1.
- **Field ditch and drain (mizo / hori / haisui)**: small earth ditches along plots. Field, common, `[terrain]`. Hook: shallow water, cover when crouched.
- **Stone-lined village channel (ishi-gumi mizo)**: a channel walled with river stones where it passes the houses, with a step down to the water at each house. Yard/commons, common, `[terrain]` + stone. Hook: water, washing.
- **Sluice gate (hi / hi-guchi / suimon / mizu-mon)**: boards slid up and down in a timber or stone frame at a channel intake, a canal, or between moat levels. Field/canal/castle, common (fields) / occasional, medium. Hook: interactable (open / close water), landmark, puzzle. (BL: Civic, water gate) {seam S156: R §2 + U Water: Canals + U Castle: Earthworks}
- **Paddy water notch (mizu-kuchi / mizu-jiri)**: a cut in the bund with a board, sod or straw plug to let water in or out of one paddy. Field, common, small. Hook: detail only.
- **Water divider (bunsui)**: a board or stone set in a channel with notches of fixed widths so each village or field gets its share; the object of fierce water disputes. Field, occasional, small–medium. Hook: lore (water quarrels), landmark. (assumed form)
- **Incense water-clock (senkō-mizu)**: each farmer's turn at the shared water was timed by burning incense sticks; a prop at a sluice or water-guard hut. Field, rare, small. Hook: lore. Src: Sanuki custom (verify date). BL: water guard hut.
- **Irrigation pond (tame-ike)**: an earth dam across a small valley holding water for dry-season paddies; many in Kinai and Sanuki; Mannō-ike was rebuilt in 1631. Field, common in Kinai, `[terrain]` large. Hook: water, fish; the autumn drain-down (ike-hoshi) when villagers catch the carp and crucian is a good event. BL: Civic, reservoir.
- **Pond outlet with plug tower (soko-hi / tate-hi)**: a wooden or stone outlet tower in the pond, opened by pulling plugs one by one. Field, occasional, medium. Hook: interactable, landmark. (assumed form; verify name)
- **Pond spillway (yosui-bake)**: a cut in the dam crest for floodwater, lined with stone. Field, occasional, `[terrain]`. (assumed; name verify)
- **River weir, stone and timber (seki / iseki)**: stone and timber across a river turning water into an irrigation channel. River/field, common (R) / occasional (W), large. Hook: crossing point, water, fish, noise. (BL: Civic, weir) {seam S123: R §2 + W §12}
- **Brushwood-and-stake weir (shiba-zeki / kui-zeki)**: a cheap weir of stakes and bundled brush, rebuilt after each flood. Field, common, medium. Hook: crossing, crafting (stakes). (assumed)
- *Bamboo gabions (jakago)* → S120, under W §12.
- *Timber river-crib spurs (seigyū / waku)* → S119, under W §12.
- **Bamboo pipe and piped spring (kakehi / kakei)**: split bamboo on forked sticks carrying spring water to a house, trough, temple or garden basin; by the road it ends in a stone or wooden basin with a ladle on a stick, many named "X-shimizu". Yard/roadside/garden, common in hills / occasional in towns, small–medium. Hook: WATER (clean). (BL: §2.3 mountain village) (roadside form assumed) {seam S068: R §2 + W §3 + U Streets: Wells and street water supply + U Gardens: Basins}
- **Flume on trestles (toi / kakehi-bashi / suidō-bashi)**: board trough on posts carrying irrigation, mine or city water across a gully, road or river; walkable in a pinch. The Edo landmark carries the Kanda aqueduct over the Kanda River. Field/mountain/canal, occasional (rural), rare (wild), landmark (Edo), medium–large. Hook: water, landmark, climbable, a crossing (danger). (BL: Civic, aqueduct bridge) {seam S069: R §2 + W §4 + U Streets: Wells and street water supply}
- *Irrigation tunnel (manbo / mabu / zuidō)* → S122, under W §12.
- **Treadwheel (fumi-guruma)**: small paddle wheel trodden by a man to lift water from a ditch into the paddy; in use from the 1660s (Osaka). Field, common in Kinai lowlands, medium. Hook: interactable. BL: Civic, treadwheel.
- **River lift wheel (agemizu-guruma / mizu-guruma)**: a current-driven wheel with buckets or tubes lifting water into a high channel; the Yodo castle wheel on the Yodo river was a famous sight. Field, occasional, large. Hook: landmark, sound. (Yodo wheel date: verify)
- **Dragon-backbone chain pump (ryūkotsu-sha)**: Chinese-style chain of paddles in a trough; used in early Edo but replaced by the treadwheel by the late 1600s. Field, rare, medium. IN but rare by 1730, largely replaced by the treadwheel `[old: early Edo]` (merge fix: verify it was still in use somewhere in 1730)
- **Field sweep (hane-tsurube, field version)**: the counterweighted lever well used to lift water from a ditch or pit into a higher field. Field, common, medium. Hook: water.
- **Two-person swing bucket (furi-oke; name verify)**: a bucket on two ropes swung by two people to throw ditch water up into a paddy. Field, common, small. Hook: lore. (assumed name)
- **Spring and spring pool (yūsui / izumi / shimizu)**: water rising at the foot of volcanic slopes and terraces; a village spring gets a stone surround, a dipper and often a tiny Suijin stone. Landmarks: Mishima's Kakita springs and Oshino Hakkai (a Fuji pilgrims' purification stop). Commons, common, small–medium. Hook: clean drinking water, spring shrines. (mem) {seam S047: R §2 + N §U}
- *Stepping stones and slab bridge over a channel (tobi-ishi / ishi-bashi)* → S073, under U Water: Bridges.
- **Paddy boat (ta-bune)**: a small flat punt for moving sheaves, seedlings and manure through deep paddies and delta creeks. Field, occasional (deltas), medium. Hook: vehicle in creek country, wood.
*- *Also relevant, not counted: public wash place (arai-ba), Ōmi kabata, water guard hut, flood boat under the eaves (age-bune): all in BL.**

### == R §3 Dry fields, kitchen gardens, orchards and cash crops ==

- **Dry field with ridges (hata / hatake, une)**: upland fields ridged for barley, millet, beans, buckwheat and vegetables. Field, common, `[terrain]`. Hook: food (seasonal forage).
- **Kitchen garden plot (saien / kado-batake / senzai-batake)**: the family plot beside or behind the house: daikon, eggplant, cucumber, negi, burdock, taro, gourds, greens. Yard, common, `[terrain]` small. Hook: food.
- **Eggplant and cucumber stakes (nasu-bō, kyūri-dana)**: stakes and a low cross-pole frame for climbing vines. Yard, common, small. Hook: food.
- **Gourd trellis (yūgao-dana / hyōtan-dana)**: flat overhead bamboo trellis by the house hung with bottle or moonflower gourds; kanpyō strips from yūgao (Mibu, Shimotsuke, from 1712; verify). Yard, common, medium. Hook: shade, food, a hyōtan water flask to craft. {seam S042: R §3 + N §P}
- **Loofah trellis (hechima-dana)**: loofah vines on a trellis, for scrubbers and "loofah water". Yard, occasional, medium. Hook: crafting. (verify date for Edo commoners)
- **Climbing beans on poles (sasage, ingen-mame)**: cowpeas and runner beans on tall poles or tepees in gardens; the ingen bean is named for the monk Ingen, who arrived 1654 (legend; verify which bean). Yard/field, common, small–medium. Hook: food. {seam S025: R §3 + N §P}
- **Taro (satoimo; ta-imo)**: big-leaved taro in damp field corners beside paddies, in dry-field rows, and in wet plots in some regions. Yard/field, common, `[terrain]` + plants. Hook: staple tuber, Moon-viewing offering, leaves as rain shields. (wet plots assumed) {seam S030: R §3 + R §1 + N §P}
- **Daikon (daikon-batake)**: long white radish everywhere in autumn fields; Nerima daikon near Edo (Tsunayoshi-era legend). Field, dominant (autumn dry fields), `[terrain]`. Hook: food, takuan pickles (drying racks R §4), leaves; winter survival food. {seam S026: R §3 + N §P}
- **Winter greens (na / komatsuna)**: Edo's green, near towns. The name is said to come from Yoshimune (N: Kyōhō era; R: 1719; both legend, verify). Field, common near Edo, `[terrain]`. Hook: winter greens. {seam S027: R §3 + N §P}
- **Welsh onion (negi)**: gardens and field rows; Senju negi for Edo, Kujō for Kyoto. Field, common near towns, `[terrain]`. Hook: food. {seam S028: R §3 + N §P}
- **Burdock (gobō)**: deep-rooted, a Japanese-only crop, on sandy river-flat fields. Field, common (N) / occasional (R), `[terrain]`. Hook: food. {seam S029: R §3 + N §P}
- **Buckwheat (soba; soba-batake)**: cool mountain fields, poor upland and new swiddens; a 75-day crop; Shinano and Kiso are famous. Field, common in hills, `[terrain]`. Hook: food (sobagaki, soba-kiri), landmark white flowers on red stems. {seam S023: R §3 + N §O}
- **Millets (awa, hie, kibi)**: foxtail, barnyard and proso millet on dry, swidden and cold mountain fields, hie also in cold-water paddies; staples of the poor and of hills. Field, common (hills), `[terrain]`. Hook: food (awa-mochi, kibi-dango); hie is the famine-safe grain that keeps for decades. {seam S022: R §3 + N §O}
- **Barley and wheat (ōmugi, hadakamugi, komugi; mugi-batake)**: winter crops on dry fields; barley also in drained paddies as the second crop in warm areas; golden in May–June. Field, common, `[terrain]`. Hook: staple of the poor (mugimeshi), udon and sōmen flour, soy sauce, miso, straw. Double-cropped paddy: R §1. {seam S021: R §3 + N §O}
- **Soybean and azuki (daizu, azuki; aze-mame)**: dry-field crops, and soybeans in a line along paddy bund tops, a signature look. Field, common, `[terrain]` / small plants on bunds. Hook: miso, soy sauce, tofu, natto, sweets, festival red rice; autumn forage. (bund soy assumed, verify) {seam S024: R §3 + R §1 + N §P}
- **Sesame (goma-batake)**: dry fields. Field, occasional, `[terrain]`. Hook: oil, food. Drying bundles: R §4. {seam S031: R §3 + N §P}
- **Rapeseed (natane-batake)**: winter crop on drained paddies, very large in Settsu and Kawachi; yellow spring fields. Field, common in Tōkai–Kinai / occasional in Kantō, `[terrain]`. Hook: lamp oil (the main one by 1730; crafting), oil-cake fertilizer, spring landmark colour. (BL: oil press) {seam S032: R §3 + N §Q}
- **Cotton (wata-batake)**: Kinai, Mikawa and Owari (on the Tōkaidō) and parts of Musashi; a 17th–18th-c. boom crop that replaced hemp for commoners. Field, common in Kinai and the Tōkai plains, `[terrain]`. Hook: cloth, wicks, padding, bandage crafting; white bolls in autumn. {seam S033: R §3 + N §Q}
- **Indigo (ai-batake)**: Musashi, Settsu and the Kantō plain for local dyers; Awa is the big producer `[off-map: Shikoku]`. Field, occasional, `[terrain]`. Hook: blue dye (sukumo). (BL: indigo barn) {seam S034: R §3 + N §Q}
- **Hemp (asa-batake)**: dense 2–3 m stands in mountain villages (Shinano, Nikkō). Field, common (mountains) / occasional, `[terrain]` tall. Hook: fibre for rope, cloth, sandals, nets and bowstrings; tall cover. Retting: R §4. {seam S035: R §3 + N §Q}
- **Tobacco (tabako-batake)**: legal and widely grown by 1730 on hill fields; Hadano (Sagami, just east of Hakone) a noted area (verify start date). Field, occasional, `[terrain]` + tall plants. Hook: trade good, leaves drying on racks. (BL: tobacco drying shed) {seam S036: R §3 + N §Q}
- **Konjac (konnyaku-batake)**: corms on shaded hill slopes, Kōzuke and Hitachi. Field, occasional, `[terrain]`. Hook: food. Powdered konnyaku `[outside 1680-1750: 1776 process]`. {seam S037: R §3 + N §P}
- **Sweet potato (satsuma-imo)**: in Satsuma (c.1705) and Nagasaki, the Inland Sea c.1711; Aoki Konyō's Kantō trial plots from 1735, after the Kyōhō famine. Field, rare, `[terrain]`. `[outside 1680-1750 on our map: from 1735]` Hook: famine crop. Stephen's call. {seam S038: R §3 + N §P}
- **Maize (tōmorokoshi / nanban-kibi)**: present since the late 1500s, grown a little in mountain fields; cobs hung under the eaves. Field, rare, `[terrain]`. Hook: food. (verify spread by 1730) {seam S039: R §3 + N §O}
- **Korean ginseng bed (chōsen ninjin; ninjin-hata)**: Yoshimune had seed brought and trial-planted at Nikkō (N: from 1729; R: around 1728, distributed from 1738); grown under low thatch shade roofs. Field, rare (official gardens only in 1730) / landmark, medium. Hook: priceless medicine, rare find. (verify dates) {seam S040: R §3 + N §P}
- **Wasabi terrace (wasabi-da)**: stepped gravel beds in cold spring-fed mountain streams; Utogi (Abe river, Suruga) from the Keichō era, reaching Amagi (Izu) only in 1744. Mountain stream, rare on our map in 1730 (Utogi only), `[terrain]`. Hook: valuable food crop, clean water. (verify) {seam S041: R §3 + N §P}
- *Tea bushes on field edges (aze-cha / kuro-cha)* → S015, under N §Q.
- **Uji shaded tea garden (ōishita-en)**: tea bushes under canopies of reed screens and straw on pole frames, for top-grade matcha leaf; Uji only. Field, rare, large. Hook: landmark, shade and cover. (Gyokuro, 1835, is later)
- **Tea row plantation (chabatake, clipped rows)**: `[outside 1680-1750: Meiji]`. Listed so it is not built by mistake. Field, —, `[terrain]`.
- *Mulberry field and mulberry hedge (kuwa-batake)* → S016, under N §Q.
- **Paper-mulberry and paperbush patches (kōzo / mitsumata)**: shrubs cut for washi bark on hill-field edges, riverbanks and rocky or shady plots (mitsumata in Suruga and Kai); gampi is wild only (N §Q). Field, common in paper villages, medium bushes. Hook: bark fibre, paper crafting. {seam S017: R §3 + N §Q}
- *Lacquer trees along bunds (urushi)* → S018, under N §C.
- *Wax trees (haze / hazenoki)* → S019, under N §C.
- *Yard persimmon tree (kaki)* → S012, under N §D.
- *Plum grove (ume-bayashi)* → S013, under N §D.
- *Chestnut trees (kuri)* → S014, under N §D.
- **Citrus terraces (mikan-batake)**: Kishū (Arida) mandarins on stone terraces, shipped to Edo. Field, rare on our map, large `[terrain]` + trees. Hook: food, landmark. `[off-map: Kii, edge of map]` (verify)
- **Yard citrus and other fruit trees (yuzu, biwa, nashi, momo)**: single trees by the house. Yard, occasional, large (tree). Hook: food.
- **Pear orchard on overhead trellis (nashi-dana)**: pears trained on a flat head-high trellis. Field, rare, large. Hook: food, cover under the trellis. (verify that trellis pears predate 1750)
- **Village bamboo grove (take-yabu)**: madake or hachiku planted and cut behind houses and on levees, often the north windbreak. Yard, common, large. Hook: poles, baskets, shoots (food), cover. Species: N §F. {seam S005: R §3 + N §E}
- *Grass-cutting slope (kusakari-ba / magusa-ba)* → S007, under N §E.
- *Thatch meadow (kaya-ba)* → S007, under N §E.
- **Hotbed frames with oiled paper (onsho / abura-shōji)**: forcing beds warmed with fermenting manure under oiled-paper covers, for early vegetables; Sunamura on the Edo outskirts. Field, rare, medium. Hook: warmth. (verify; the bakufu restricted early-season vegetables, 1686)
- **Compost heap (tsumi-goe / taihi)**: straw, leaves and stable muck piled to rot. Yard, common, medium. Hook: fertiliser crafting, smell.
- **Stable manure heap (umaya-goe)**: muck from the stable heaped by its door. Yard, common, medium. Hook: as above.
- **Field manure jar (koe-game; name verify)**: a big jar sunk at a field corner holding night soil to ripen before spreading. Field, common, small. Hook: hazard (fall in), smell. (assumed name)
- **Night-soil buckets and pole (koe-oke / koe-tago)**: two lidded buckets on a shoulder pole, carried out of town by the farmers who bought the waste. Yard/field/street, common, small. (BL: manure shed) {seam S216: R §3 + U Streets: Rubbish}
- **Field and survey boundary marker (sakai-kui / bōji-kui / kenchi sakai-ishi / kenchi-gui)**: wooden stake or stone at plot, field or forest corners after a land survey, or at village limits; surveyors also leave stakes and rope lines. Field/forest edge, common (R) / occasional (W; stakes rare), small. Hook: navigation, map detail, lore. (W forms assumed) {seam S128: R §3 + W §13 + W §1}
- *Burnt clearing fields (yakihata)* → S008, under N §E.
*- *Also relevant, not counted: field hut (nora-goya), paddy watch hut (ta-goya / shishi-goya), medicinal herb garden (o-yakuen), shiitake logs: all in BL.**

### == R §4 Harvest, drying and processing outdoors ==

- **Rice-drying rack, pole type (hasa / hazakake / inakake)**: horizontal poles or bamboo lashed to uprights, sheaves hung head-down in autumn; one to three tiers in Kinai and Kanto. Field, common (autumn), medium–large. Hook: cover in autumn, straw. Src: Kubota; NGZ 1697; rack drying is recorded from 841.
- **Tall multi-tier rack (hasa, 5–10 rungs)**: the ladder-like racks of wet snow country. Field, rare on our map, large. `[off-map: Echigo, Hokuriku]`.
- *Living-tree rack row (hasa-gi / inaki)* → S045, under N §C.
- **Ground-standing sheaves (ji-boshi / ta-boshi)**: sheaves stood in small stooks or cones on the dry paddy. Field, common, small. Hook: low cover.
- **Rice-sheaf stack (ine-zuka / nio)**: a round stack of sheaves waiting for threshing. Field/yard, common, medium. Hook: cover, straw.
- **Straw stack (wara-nio / wara-bocchi / suzumi)**: conical or cylindrical stack of threshed straw round a centre pole with a straw cap; many regional names. Yard/field, common, medium. Hook: cover, hide inside, straw crafting, burns.
- **Straw bundles in stooks (wara-taba)**: bundles leaning together to dry. Yard/field, common, small. Hook: straw.
- **Threshing yard / swept earth (kado / niwa)**: swept, hard-packed bare earth in front of the farmhouse; the farm's working floor at harvest, spread with mats. Yard, common, `[terrain]`. Hook: open ground, loot on mats. {seam S046: R §4 + N §S}
- **Threshing comb (senba-koki)**: iron-toothed comb on a stand; invented in the Genroku years (1688–1704) at Takaishi, Izumi, and spreading fast by 1730; nicknamed "widow-toppler" (goke-daoshi) because it put widow threshers out of work. Yard, common, small–medium. Hook: crafting source of iron.
- **Chopstick thresher (koki-bashi)**: two sticks pinched over the stalks; the older method, still used by poor households. Yard, occasional, small.
- **Flail (karazao / kururi-bō)**: swinging-bar flail for beans, barley and wheat. Yard, common, small. Hook: improvised weapon.
- **Winnowing machine (tōmi)**: box fan turned by a crank; first noted in the *Aizu Nōsho* (1684) as still rare, spreading from the late 1600s. Yard, occasional, medium. Hook: grain processing station. Src: Aizu Nōsho 1684.
- **Winnowing basket (mi)**: wide shovel-shaped basket for tossing grain. Yard, common, small.
- **Sloped grain sieve (sengoku-dōshi / mangoku-dōshi)**: a sloping wire or bamboo screen that sorts hulled rice from husks; shown in the WKS (1712) as a new box type. Yard/doma, occasional, medium.
- **Hulling mill (suri-usu / tsuchi-usu)**: clay-and-wood grinding mill for husking rice; used indoors or on the yard on fine days. Yard, occasional, medium.
- **Wooden mortar and pestle (usu, kine / tate-kine)**: big log mortar for hulling and for New Year mochi, rolled into the yard. Yard, common, medium. Hook: food processing station.
- **Treadle mortar under the eaves (karausu / fumi-usu)**: see-saw pestle worked by foot. Yard, occasional, medium. BL: pounding shed.
- **Hand quern (ishi-usu / hiki-usu)**: pair of stone millstones for flour, buckwheat and kinako; mostly in the doma, sometimes on the veranda. Yard, occasional, small. Hook: flour crafting.
- **Water-driven pounding lever (battari / sōzu-usu; name verify)**: a stream fills a scoop at one end of a beam, it tips, and the pestle end drops into a mortar; mountain villages. Field (stream), occasional, medium. Hook: landmark, rhythmic sound. (regional names vary; verify)
- **Grain drying on mats (mushiro-boshi)**: rice, beans, sesame and peppers spread on straw mats in the yard. Yard, common, small. Hook: food lying on surfaces.
- **Dried persimmon strings (hoshigaki / tsurushi-gaki)**: peeled persimmons hung in curtains from the eaves or a rack. Yard, common (autumn), small–medium. Hook: food. BL: drying shed.
- **Radish drying rack (daikon-hoshi / kake-daikon)**: whole daikon hung over racks or hasa to wilt for takuan. Yard/field, common (early winter), medium. Hook: food.
- **Cut-radish strips on mats (kiriboshi-daikon)**: shredded radish drying in the sun. Yard, occasional, small. Hook: food.
- **Gourd-strip drying poles (kanpyō-hoshi)**: white ribbons of shaved gourd hung on poles. Yard, occasional (Shimotsuke), medium. Hook: food.
- **Agar winter drying fields (kanten-ba)**: agar jelly frozen and dried on mats laid over winter paddies; Settsu and Tanba hill villages. Field, rare, `[terrain]` + mats. Hook: food, odd winter landmark. (verify dates)
- **Freeze-dried tofu racks (kōri-dōfu / shimi-dōfu)**: tofu frozen outdoors on winter nights. Yard, rare, small. Hook: food. (verify date for commoners)
- **Noodle-drying poles (sōmen-boshi)**: hanks of thin wheat noodles hung on poles in winter yards; Miwa (Yamato) and Harima. Yard, occasional, medium. Hook: food. BL: drying shed mentions noodles.
- **Chilli and bean bundles (tōgarashi, daizu)**: bunches hung under the eaves. Yard, common, small. Hook: food.
- **Umeboshi mats (ume-boshi)**: salted plums drying on bamboo mats in midsummer. Yard, occasional, small. Hook: food. BL: umeboshi works.
- **Tannin tubs (kaki-shibu)**: tubs of fermenting green-persimmon juice for waterproofing paper, nets and cloth. Yard, occasional, small. Hook: waterproofing crafting.
- **Pickle barrels with weight stones (tsukemono-oke, omoshi-ishi)**: takuan and salted greens under stones, under the eaves. Yard, common, small. Hook: food, throwable stones.
- **Stacked rice bales and casks (kome-dawara, komo-daru)**: straw bales (lined up in the headman's yard for the tax inspector in autumn) and straw-wrapped casks piled at shopfronts and quays. Yard/street/canal, common, medium. Hook: food, cover, climb, loot on top. {seam S214: R §4 + U Streets: Peddlers'}
- **Straw-pounding stone and mallet (wara-uchi-ishi, yokozuchi)**: a stone set in the doma or yard where straw is beaten soft for rope and sandals. Yard, common, small. Hook: crafting station.
- **Straw work in progress (nawa, waraji, kamasu)**: rope coils, sandals on a string, straw sacks. Yard, common, small. Hook: rope and sandals.
- **Sesame bundles standing (goma-date)**: sesame stalks stood upright to split and drop seed on mats. Field, occasional, small. Hook: food. (assumed)
- **Cotton bolls on mats (wata-boshi)**: picked cotton drying before ginning. Yard, occasional (Kinai), small. Hook: cloth crafting.
- **Hemp steaming and retting (asa-mushi / asa-hitashi)**: hemp stalks steamed in a pit or soaked in a pond, then stripped. Yard/field, occasional, medium. Hook: fibre crafting. (verify form)
- **Firewood and pine-needle fuel bales (matsuba)**: raked pine litter bundled as fuel. Yard, common, small. Hook: fuel.
- **Seed bags hung from the eaves (tane-bukuro)**: next year's seed kept dry in straw or paper bags. Yard, common, small. Hook: crafting (seeds). (assumed)
*- *Also relevant, not counted: tobacco drying, tea processing, silkworm rooms: in BL.**

### == R §5 Crop protection: scarers and animal defences ==

- **Scarecrow (kakashi)**: a straw figure in a kasa and straw raincoat, sometimes holding a bow; in Edo prints. Field, common, small–medium. Hook: landmark, spooky at night, decoy.
- **Smell scarer (kagashi)**: burnt hair, fish heads or rags stuck on a split stick at the field edge, the older kind of "scarecrow". Field, common, small. Hook: lore, smell.
- **Bird-scare clapper line (naruko)**: small boards hung with bamboo tubes on a rope across the fields, rattled by a pull-rope from the watch hut or by the wind. Field/forest edge, common, small + rope line. Hook: SOUND: a noise alarm a player can trip. {seam S115: R §5 + W §9}
- **Bird-scare rope lines (tori-odoshi nawa)**: ropes with straw tassels, cloth strips or feathers stretched over seedbeds and ripening rice. Field, common, small. Hook: alarm line.
- **Knocking bamboo scarer (sōzu / shishi-odoshi)**: a bamboo tube fills with water, tips, and knocks a stone as it swings back; a farm deer-scarer, first used in a garden at Shisendō by Ishikawa Jōzan, 1641 `[old: 1641, in use 1730]`. Field stream edge occasional / garden rare, small. Hook: periodic rhythmic noise. {seam S215: R §5 + U Gardens: Basins}
- *Night watch fires (kagari)* → S117, under U Streets: Street lighting and lanterns.
- **Scaring gun (odoshi-deppō)**: villages kept registered guns for scaring animals; Tsunayoshi's gun registration of 1687 counted them. Field, occasional, small. Hook: rare weapon lore. (verify)
- **Stone boar wall (shishigaki)**: dry-stone (or earth) wall about 1.5 m high running for kilometres between fields and forest; mostly 18th–19th c. (Shōdoshima had walls by 1745 and 120 km by 1790), so partly in window. Field/forest edge, occasional, large `[terrain]` linear. Hook: NAVIGATION (follow it to a village), landmark, cover, barrier. {seam S112: R §5 + W §9}
- **Earth boar bank and ditch (tsuchi-shishigaki / shishi-bori)**: trench with an earth bank on the forest side, where stone is scarce. Field/forest edge, occasional, `[terrain]` linear. Hook: barrier, cover, fall hazard. {seam S113: R §5 + W §9}
- **Stake-and-brush game fence (shishi-gaki / shika-gaki / shika-ami)**: stakes woven with brush, or nets and ropes on stakes, round fields against boar and deer; the cheap version. Field/forest edge, common, medium linear. Hook: barrier, stakes, cover. (W and net forms assumed) {seam S114: R §5 + W §9}
- **Boar-wall gate (shishigaki no kido)**: a small gate where the path passes through the wall, closed at night. Field edge, occasional, medium. Hook: chokepoint.
- *Deer net or rope fence (shika-ami)* → S114, under R §5.
- *Pit trap (otoshi-ana)* → S111, under W §9.
- **Bird net over seedbeds (tori-ami)**: net on low stakes. Field, occasional, small. (assumed)
- **Insect-repelling charms on sticks (mushi-yoke fuda)**: shrine or temple charms on split bamboo stuck in bunds. Field, common, small. Hook: lore.
- **Insect lamps (mushi-okuri torches, fixed)**: see §14 for the procession; a few regions set fires on bunds on summer nights. Field, occasional, small. (assumed)
- **Whale-oil paddy spread (abura-chū)**: whale oil dripped on flooded paddies against planthoppers, recorded in Kyushu from the 1670s and spread during the Kyōhō locust famine (1732). Field, rare, small (oil jar). Hook: lore, oil. (verify dates)
*- *Also relevant, not counted: paddy watch hut (ta-goya / shishi-goya): BL, Dwellings poor.**

### == R §6 Farmyard: water, laundry, fuel and refuse ==

- **Lever well (hanetsurube)**: counterweighted pole on a post with a bucket on a bamboo pole; mostly rural, also at town edges and temple yards. Yard/street, common (villages) / occasional (towns), medium. Hook: water, landmark silhouette. (BL: Civic, lever well) {seam S157: R §6 + U Streets: Wells and street water supply}
- **Pulley well (tsurube-ido)**: curb and crossbeam with a pulley, two buckets on one rope, with or without a small gable roof. Yard/street/alley, common, medium. Hook: water. (BL: Civic, pulley well; outbuildings, roofed well) {seam S158: R §6 + U Streets: Wells and street water supply}
- **Well curb and lid (igeta / ido-waku / ishi-gawa / ido-buta)**: square plank box curb, or dressed stone ring or box, with a board or split-bamboo lid held by a stone. Yard/street, common, small. Hook: water, low cover; fall hazard when open. (stone form assumed) Pottery-ring curbs: U (Wells; verify). {seam S159: R §6 + U Streets: Wells and street water supply}
- **Spiral walk-down well (maimai-zu ido)**: a funnel-shaped pit with a spiral path down to a well at the bottom, on the dry Musashino plateau. Commons, rare, large `[terrain]`. Hook: landmark, water. (medieval origin, Edo use; verify)
- **Rain barrel and water jar (tensui-oke / mizu-game)**: a tub under the eaves catching roof water, or a big glazed jar at the door refilled from water sellers where wells were bad (Osaka, Edo lowlands). Yard/street, common (R; jars in towns), small. Hook: water. A tensui-oke at every town house is `[outside 1680-1750: general from Kansei 1789–1801]`; 1730 towns have corner fire tubs with bucket pyramids and eave-hung buckets (U, Fire-fighting). See §3.3. {seam S161: R §6 + U Streets: Street furniture + U Streets: Fire-fighting and night-watch fixtures}
- **Stone trough fed by a pipe (ishi-bune / mizu-bune)**: a stone or wooden trough with running spring water for washing vegetables. Yard, occasional, small–medium. Hook: clean water.
- **Wash tub and summer bath tub (tarai / gyōzui-darai)**: wooden tubs in the yard for washing clothes and bodies. Yard, common, small. Hook: water. No washboard: the ridged washboard is Meiji (verify).
- *Laundry pole on forked stakes (monohoshi-zao / sao-kake)* → S162, under U Streets: Street surface.
- **Cloth-stretching boards (hari-ita)**: unstitched kimono panels, washed and starched, pasted on long boards leaned in the sun (arai-hari). Yard, common, medium. Hook: cloth.
- **Bamboo cloth stretchers (shinshi)**: bowed bamboo pins stretching a length of cloth between two posts. Yard, occasional, medium. Hook: cloth.
- **Firewood stack (maki-zumi)**: split wood stacked to dry among the trees or under the eaves, sometimes a whole wall of it. Yard/forest, common, small–medium. Hook: fuel, cover. {seam S108: R §6 + W §8}
- **Brushwood bundles (soda / shiba-taba)**: bundled twigs cut on the commons, the everyday fuel. Yard, common, medium. Hook: fuel.
- **Chopping block and axe (makiwari-dai)**: stump block with an axe or hatchet. Yard, common, small. Hook: crafting station, weapon.
- **Thatch bundles stored for re-roofing (kaya-taba)**: bundles stood in stooks for the next cooperative roofing (yui). Yard/commons, occasional, medium. Hook: roofing crafting, cover.
- **Timber stack (zaimoku-zumi)**: sawn or split timber seasoning for repairs. Yard, occasional, medium. Hook: wood.
- *Charcoal bales (sumi-dawara)* → S107, under W §8.
- **Refuse pit (hakidame / gomi-ana)**: a pit in the yard corner for scraps, later dug out as manure. Yard, common, small `[terrain]`. Hook: scavenging, smell.
- **Hearth-ash heap (hai-zuka)**: ash kept for fertiliser, lye and dyeing. Yard, occasional, small. Hook: crafting (lye). BL: ash shed.
- *Eaves bench (endai / shōgi)* → S063, under U Streets: Street furniture.
- **Ladder (hashigo)**: pole-and-rung ladder leaning on the eaves or a tree. Yard, common, small. Hook: climbing.
- **Upturned buckets drying on stakes (oke-hoshi)**: buckets and tubs upside down on posts. Yard, common, small. Hook: dressing.
- **Outdoor cooking fire (soto-kamado)**: a temporary clay or stone stove in the yard for boiling, dyeing and festival cooking. Yard, occasional, small–medium. Hook: cooking station.

### == R §7 Farmyard: tools, transport and livestock ==

- **Tools under the eaves (kuwa, kama, tsuruhashi)**: hoes, sickles and mattocks hanging on pegs or leaning on the wall. Yard, common, small. Hook: melee weapons and tools.
- **Three-tined hoe (Bitchū-guwa)**: a tined hoe for heavy soil, an Edo-period tool spreading in the 18th c. Yard, common, small. Hook: weapon, tool. (verify spread date)
- **Plough (karasuki / suki)**: ox- or horse-drawn plough stored under the eaves; oxen in the west, horses in the east. Yard, occasional, small–medium. Hook: crafting (iron share).
- **Paddy harrow (maguwa)**: toothed bar dragged by an ox to puddle the paddy. Yard, occasional, medium.
- **Levelling rake (eburi)**: wooden board-rake for smoothing paddy mud. Yard, common, small.
- **Mud clogs and paddy boards (ta-geta / ō-ashi)**: wide board clogs for walking on soft paddy. Yard, occasional, small. Hook: wearable (move faster in mud).
- **Carrying frame (shoiko / seoi-bashigo)**: a wooden backpack frame for loads of wood and grass. Yard, common, small. Hook: carry-capacity item.
- *Shoulder pole and baskets (tenbin-bō / mokko)* → S155, under U Streets: Peddlers'.
- **Pack saddle on a rest (ni-gura)**: horse pack saddle on a trestle by the stable. Yard, occasional, small. BL: stable.
- *Hand-cart (niguruma)* → S163, under U Streets: Peddlers'.
- **Ox cart (ushi-guruma)**: heavy two-wheeled freight cart on the Kyoto–Fushimi–Ōtsu roads. Commons/road, rare (Kyoto region), medium. Hook: vehicle, landmark. The stone cart-track (kuruma-ishi) at Ōtsu is `[outside 1680-1750: 1805]` (verify).
- *Sledge (sori / shura)* → S110, under W §8.
- *Tethering post (uma-tsunagi)* → S066, under U Streets: Street furniture.
- *Tethering stone (tsunagi-ishi)* → S066, under U Streets: Street furniture.
- *Animal trough (kaiba-oke / mizu-bune)* → S065, under U Streets: Street furniture.
- **Fodder cutter (kaiba-kiri)**: blade on a hinged block for chopping straw. Yard, occasional, small. Hook: crafting station. BL: stable.
- *Horse-washing place (uma-arai-ba)* → S067, under W §3.
- **Straw horse-shoe offerings (uma-no-waraji)**: worn straw horse shoes hung on a tree or on a Batō Kannon stone. Commons, occasional, small. Hook: lore.
- **Loose hens (niwatori)**: a few hens scratching in the yard (eggs sold; time-keeping cocks). Yard, occasional, small. Hook: food. BL: hen coop (egg-eating: verify).
- *Log beehive (hachi-dō / hachi-bako)* → S118, under W §11.
- **Farm fish pond (ike)**: a small pond by the house for carp or crucian and fire water. Yard, occasional, medium. Hook: food, water. Paddy carp farming at Saku is `[outside 1680-1750: tradition dates 1746]` (verify).
- **Grindstone on a stand (toishi)**: whetstone on a trestle for tools. Yard, common, small. Hook: sharpening station.
- **Stone roller (ishi-guruma / kororin)**: a stone roller for levelling the threshing yard. Yard, occasional, small. (assumed)
- **Rope-making frame (nawa-nai)**: rope twisted by hand, one end fixed to a post. Yard, occasional, small. (assumed)
- *Cart shed, stable, ox shed*: BL, outbuildings. Not counted.
- *Wheelbarrow (neko-guruma)*: `[outside 1680-1750: late Edo or Meiji]`; counted in §17, not counted here.

### == R §8 Fences, hedges, walls, gates and windbreaks ==

- *Open bamboo grid fence (yotsume-gaki)* → S165, under U Gardens: Fences.
- *Closed split-bamboo fence (kenninji-gaki)* → S166, under U Gardens: Fences.
- **Brushwood fence (shiba-gaki)**: brush and twigs packed between posts or bamboo battens; older and rustic. Yard/garden, common, medium linear. Hook: sight block, fuel. {seam S167: R §8 + U Gardens: Fences}
- **Reed fence (yoshi-gaki / yoshizu-gaki)**: reed screens or panels on posts, by water and in towns. Yard/shore/garden/street, common, medium linear. Hook: sight block. {seam S168: R §8 + U Gardens: Fences}
- **Bamboo lattice fence (ajiro-gaki / kōshi-gaki)**: woven or diagonal lattice of split bamboo. Yard, occasional, medium linear.
- **Stake-and-rope fence (kui-nawa)**: stakes with one or two straw ropes, marking plots. Yard/field, common, small linear.
- **Live hedge (ikegaki)**: clipped evergreen hedge of kashi, podocarpus, camellia, holly, cypress, tea or cedar; tall oak hedges in Kantō; the commonest yard fence. Yard/garden/street, common, medium linear. Hook: cover, sight cover, concealment. {seam S169: R §8 + U Gardens: Fences}
- **Tea hedge (cha-gaki)**: tea bushes kept as a boundary hedge. Yard, occasional, medium linear. Hook: tea leaves.
- *Sleeve fence (sode-gaki)* → S170, under U Gardens: Fences.
- *Board fence (itabei)* → S171, under U Gardens: Fences.
- *Earth wall with capping (dobei / tsuiji)* → S172, under U Gardens: Fences.
- **Dry-stone wall (ishigaki / nozura-zumi)**: rough unworked stones piled with small packers: holding up house plots, terraces and road shelves on slopes and riverbanks, and in older castle walls. Yard/field/mountain/castle, common in hills and castles / occasional by roads, medium–large `[terrain]`. Hook: cover, climbing (hard), a fall edge (danger). River-cobble version: R §8. {seam S173: R §8 + W §2 + U Castle: Castle stone walls}
- **River-cobble wall (tama-ishi-zumi)**: rounded river stones stacked in courses. Yard, common near rivers, medium. Hook: cover.
- **Farmstead windbreak grove (yashiki-rin)**: a wall of kashi (shirakashi), keyaki, sugi, bamboo and chestnut round a farmhouse on the north and west (windward) sides; Kantō's dispersed and new-field villages. Yard, common (Musashi, Kantō), large. Hook: cover, firewood, building timber from the family's own trees; each farm a landmark clump. {seam S004: R §8 + N §E}
- **Sendai windbreak (igune)**: the Sendai-plain name and form. Yard, —, large. `[off-map: Tōhoku]`.
- **Tonami windbreak (kainyo)**: the Tonami-plain grove of mixed trees round each dispersed farm (probably the "kaizu" in the brief). Yard, —, large. `[off-map: Etchū]`.
- **Clipped pine windbreak (tsuiji-matsu)**: tall pine hedges clipped flat on the west side of Izumo farms. Yard, —, large. `[off-map: Izumo]`.
- **Sand fence (suna-yoke gaki / kaze-gaki)**: straw, reed, brush or bamboo fence against blowing sand at the dune edge. Shore, occasional, medium linear. Hook: cover. (Noto's tall magaki `[off-map: Noto]`) {seam S148: R §8 + W §19}
- **Snow fence (yuki-gakoi)**: boards and straw round houses in winter. Yard, —, medium. `[off-map: snow country]`.
- **Post gate (kado-guchi / hashira-mon)**: two posts marking the yard entrance, no doors. Yard, common, small.
- **Crossbar gate with small roof (kabuki-mon)**: two posts and a crossbeam, sometimes a small roof, board doors; headmen and richer farmers (commoner gates were restricted by rank: verify local rules). Yard, occasional, medium. Hook: landmark for "a better farm".
- **Ridge-roofed gate (mune-mon / yakui-mon)**: roofed gate of temples, samurai and top headmen. Yard, rare, medium. Hook: landmark.
- **Wicket gate (shiori-do / kido)**: light swinging gate or door of woven bamboo, branches or brushwood, hung from a bamboo frame in a fence. Yard/garden, common, small–medium. Hook: door. {seam S174: R §8 + U Gardens: Tea garden + U Gardens: Fences}
- **Bar across the entrance (yarai / sao)**: a bamboo pole laid across the gate posts at night. Yard, common, small.
- **Boundary rope on stakes around a new plot (nawa-bari)**: rope marking a house site before building. Yard, rare, small. (assumed)
- **Hedge-and-ditch plot boundary (mizo-gaki)**: a ditch with a hedge on its bank. Yard/field, occasional, `[terrain]` + hedge. (assumed)
*- *Also relevant, not counted: gatehouse with rooms (nagaya-mon): BL. Coastal black-pine belts: nature flavour.**

### == R §9 Yard sacred items and family graves ==

- **Yard shrine (yashiki-gami / uchi-gami)**: a small stone or wooden shrine in a corner of the plot, often the northwest, often Inari, with paper streamers and a little torii. Yard, common, small. Hook: landmark, lore. BL: Shinto, house-plot shrine.
- **Miniature torii at a yard shrine (ko-torii)**: a small wooden torii, painted red at Inari shrines. Yard, occasional, small.
- **Offering stand and sakaki vases (sonae-dai)**: stone slab or shelf with a pair of bamboo vases and a sake cup. Yard, common, small.
- **Well-god offering (ido-gami / Suijin)**: salt, a paper charm, a bamboo vase, or a tiny offering shelf or stone at the well curb. Yard/alley, common (R) / occasional (U), small. (U form assumed) {seam S099: R §9 + U Streets: Wells and street water supply}
- **Small fox figures at a yard Inari (kitsune)**: wooden or ceramic fox figures, not stone ones (see §17). Yard, occasional, small. (verify material in 1730)
- **Family grave plot on own land (yashiki-baka / hatake-baka)**: family graves at the corner of the house plot or a field edge; common in Kanto and Kōshū. Yard/field, common (Kanto), small–medium. Hook: landmark, lore.
- **Two-grave burial grave (ume-baka, ryōbosei)**: in Kinai the body lay in a plain earth grave under a wooden marker, stick or stone, out on the hills or in a burial ground; the stone "visiting grave" stood at the temple. Field/forest/commons, occasional (Kinai), small. Hook: eerie, lore. (verify distribution for 1730) (BL: Civic) {seam S138: R §9 + W §17}
- *Animal memorial stone (chikushō kuyōtō / uma kuyō)* → S088, under W §5.
- **New Year pine (kadomatsu)**: pine branches (with bamboo in cities) at each side of the gate over New Year. Yard/street, common (seasonal), small–medium. Hook: season marker. {seam S175: R §9 + U Festivals: Festival sets and seasonal dressing}
- **New Year straw rope (shimenawa / shimekazari)**: straw rope with paper strips (and fern and orange in towns) over the door, gate or well. Yard/street, common (seasonal), small. {seam S176: R §9 + U Festivals: Festival sets and seasonal dressing}
- **Bon altar (bon-dana / shōryō-dana)**: outdoor shelf of offerings for the returning dead, with straw horses from cucumbers and aubergines; in the yard or at the entrance in some regions. Yard/street, occasional (villages) / common (towns, Obon), small–medium. Hook: event. {seam S177: R §9 + U Festivals: Festival sets and seasonal dressing}
- **Tall Bon lantern (taka-dōrō)**: a lantern on a tall bamboo pole at a house during the first Bon after a death. Yard/street, occasional (summer), medium. Hook: light at night, landmark. (verify for 1730 regions) {seam S178: R §9 + U Festivals: Festival sets and seasonal dressing}
- **Welcome and send-off fires (mukae-bi / okuri-bi)**: small fires of hemp stalks (ogara) at the gate or door at Bon. Yard/street, common (summer), small. Hook: fire, light. {seam S179: R §9 + U Festivals: Festival sets and seasonal dressing}
- **Tanabata bamboo (tanabata-dake)**: bamboo with coloured paper strips on the 7th of the 7th month; popular in towns, less in villages; the tall rooftop forest of Edo is known from 1850s prints (verify for 1730). Yard/street, occasional (summer), small–medium. Hook: season marker. {seam S180: R §9 + U Festivals: Festival sets and seasonal dressing}

### == R §10 Village shrine grounds (outdoor items) ==

- **Wooden torii (ki-no-torii, shinmei or myōjin form)**: unpainted wooden gate at the approach of a village shrine. Shrine, common, medium. Hook: landmark.
- *Stone torii (ishi-dorii)* → S181, under U Religious: Torii by style.
- *Vermilion torii (shu-nuri torii)* → S182, under U Religious: Torii by style.
- **Rope gate (shimenawa-torii / tsuna-kake)**: two posts or two trees with a thick straw rope, instead of a torii. Shrine, rare (Kinai hills), medium. Hook: landmark. (verify)
- *Sacred tree rope (goshinboku no shimenawa)* → S052, under W §7.
- *Approach path (sandō)* → S183, under U Religious: Shrine forecourt.
- *Stone steps (ishi-dan)* → S060, under W §2.
- *Guardian lions (komainu, stone approach type)* → S184, under U Religious: Shrine forecourt.
- **Stone lantern pair and approach lanterns (ishi-dōrō / kennō-tōrō)**: donated stone lanterns, mostly Kasuga type, flanking a shrine or temple approach, in long rows with donors' names in towns, and as a pair where a mountain or shrine path leaves the road. Shrine/temple/roadside, common, medium. Hook: landmark, navigation (a path start), festival light, cover. (commoner donation boom is Edo: assumed) {seam S100: R §10 + U Religious: Shrine forecourt + W §5}
- **Wooden post lantern (moku-tōrō)**: cheap wooden lantern on a post. Shrine, occasional, small.
- *Purification basin (chōzubachi)* → S185, under U Religious: Shrine forecourt.
- *Offering box (saisen-bako)* → S186, under U Religious: Shrine forecourt.
- *Bell and rope (suzu / waniguchi)* → S187, under U Religious: Shrine forecourt.
- *Votive plaque rack (ema-kake)* → S188, under U Religious: Shrine forecourt.
- **Hundred-visits stone (hyakudo-ishi)**: marker stone for the hundred-times prayer walk. Shrine/temple forecourt, occasional, small. (most surviving ones are late Edo: verify date) {seam S189: R §10 + U Religious: Shrine forecourt}
- **Strength stones (chikara-ishi)**: heavy round stones lifted in contests by porters and youths at shrines and by the road, often carved with a weight, a date or a legend name (Benkei's). Shrine/roadside, occasional, small–medium. Hook: strength challenge, lore. (many are 18th–19th c.: verify) {seam S106: R §10 + W §7}
- *Banner-pole stones (nobori-tate ishi)* → S101, under W §5.
- *Pilgrimage memorial stones (Ise-kō / Ōyama-kō / Ontake-kō)* → S103, under W §6.
- *Shrine pond with a small bridge (shin-ike)* → S105, under W §7.
- **Stone offering table (sonae-ishi)**: flat stone before a hall or sacred stone. Shrine, occasional, small.
- **Mikoshi resting place (otabisho)**: a small plot with a stone platform and sakaki branches where the portable shrine rests during the procession. Commons/shrine, occasional, small–medium. Hook: festival waypoint.
- **Taiko drum on a stand**: festival drum set out in front of the hall. Shrine, occasional, small. Hook: noise.
- *Divination slips tied to branches (o-mikuji musubi)* → S190, under U Religious: Shrine forecourt.
- *Shrine-name stone pillar (shagō-hyō)* → S191, under U Religious: Shrine forecourt.
*- *Also relevant, not counted: sub-shrines, kagura stage, sumo ring, mikoshi store, ema hall, temizuya pavilion, hokora: all in BL, Shinto. The shrine grove itself: nature flavour.**

### == R §11 Temple yard and graveyard (outdoor items) ==

- *Communal graveyard (bochi / hakaba)* → S192, under U Religious: Graveyards and grave markers.
- *Six Jizō row (roku-jizō)* → S080, under U Religious: Temple forecourt.
- *Boat-backed relief gravestone (funagata kōhai)* → S193, under U Religious: Graveyards and grave markers.
- **Arched-top slab gravestone (kushigata)**: flat slab with a rounded top and a carved name. Commons, common, small.
- *Square-pillar gravestone (kakuchū-gata)* → S194, under U Religious: Graveyards and grave markers.
- **Five-ring stupa (gorintō)**: stacked cube, sphere, pyramid, crescent and jewel; for samurai, priests, elite and old graves, and alone in the woods for a forgotten warrior or monk `[old: medieval, still standing 1730]`. Graveyard/forest, occasional, small–medium. Hook: landmark. {seam S135: R §11 + W §17 + U Religious: Graveyards and grave markers}
- *Jewel-casket stupa (hōkyōintō)* → S092, under W §5.
- **Seated or standing figure grave (Jizō, Amida)**: small figure stones, often for children. Commons, common, small.
- **Earth grave mound and wooden grave post (dozō-baka / bohyō)**: low mound with a plain wooden post: the grave of most poor people, and any fresh grave before the stone is set. Graveyard, common, small. Hook: atmosphere. {seam S195: R §11 + U Religious: Graveyards and grave markers}
- **Wooden grave tablet (sotoba / itatōba)**: tall slim notched wooden slats stood behind graves at memorial rites (in a slat rack in towns), grey and leaning at remote hill graves, or planted where someone died on the road. Graveyard/roadside/forest, common, small. Hook: eerie, danger tell, lore; wood (taboo to take). (BL: graveyard) {seam S102: R §11 + W §5 + W §17 + U Religious: Graveyards and grave markers}
- **Fresh-grave guard (inu-hajiki / mogari-gaki / sutegaki / tamaya)**: bent split-bamboo arches, a small bamboo fence or a small roof frame over a new burial to keep dogs and wolves off. Graveyard, occasional, small. Hook: atmosphere. (names and regions: verify) (BL: Civic) {seam S196: R §11 + U Religious: Graveyards and grave markers}
- **Grave buckets and ladle rack (teoke, hishaku, teoke-kake)**: wooden buckets and ladles on a rack by the graveyard well or water point, for washing the stones. Graveyard, common, small. Hook: water container prop. {seam S197: R §11 + U Religious: Graveyards and grave markers}
- **Grave flower tubes and water cup (hana-zutsu / hana-tate, mizu-bachi)**: bamboo tubes with shikimi (star anise) branches and a hollow in the base. Graveyard, common, small. {seam S198: R §11 + U Religious: Graveyards and grave markers}
- **Stone incense stand (kōro-ishi / senkō-tate)**: small stone incense holder at a grave. Graveyard, common, small. {seam S199: R §11 + U Religious: Graveyards and grave markers}
- **Famine, epidemic and disaster memorial (gashi / ekibyō kuyōtō, ekishi-zuka)**: stones, stupas or mounds for famine, plague and fire dead: the Meireki fire dead at Ekō-in (1657); the Kyōhō famine (1732–33, western Japan) leaves the first wave just after the anchor year; a stone over an epidemic pit outside the village. Roadside/commons/temple/forest edge, occasional (after 1732) / rare (pits), small–medium. Hook: lore, eerie. Tenmei famine stones `[outside 1680-1750: 1780s]`. (BL notes the Kyōhō stones) {seam S139: R §11 + W §17 + U Religious: Stone monuments}
- *Sutra mound (kyōzuka, ichiji-isseki)* → S093, under W §5.
- *Heap of unclaimed old stones (muen-zuka)* → S137, under U Religious: Graveyards and grave markers.
- **Temple bell hung in the open (tsurigane on a frame)**: small villages without a bell tower sometimes hung a bell on a simple frame. Commons, rare, medium. Hook: noise, alarm. (assumed) BL: bell tower.
*- *Also relevant, not counted: crematory, bier shed, bell tower, temple gates, Jizō-dō, Kōshin hall: BL, Buddhist and Civic.**

### == R §12 Roadside and boundary stones, statues and figures ==

- *Roadside Jizō (michi-jizō / tsuji-jizō)* → S078, under W §5.
- **Child-giving Jizō (koyasu Jizō)**: Jizō holding a child, prayed to for safe birth. Commons, occasional, small.
- **Women's Kannon stone (Nyoirin Kannon, nijūku-ya / nijūku-nichi)**: stones set up by women's moon-vigil groups. Commons, occasional, small. (18th–19th c.; verify earliest)
- *Horse-headed Kannon (Batō Kannon)* → S087, under W §5.
- *Kōshin stone with three monkeys (kōshin-tō)* → S085, under W §5.
- *Kōshin mound (kōshin-zuka)* → S086, under W §5.
- *Character dōsojin (moji-dōsojin)* → S082, under W §5.
- *Paired-figure dōsojin (sōtai dōsojin)* → S081, under W §5.
- *Round-stone dōsojin (maru-ishi dōsojin)* → S083, under W §5.
- *Phallic stones (konsei-sama / seki-bō)* → S084, under W §5.
- *Mountain god stone (yama-no-kami)* → S098, under W §5.
- *Water god stone (suijin)* → S097, under W §5.
- **Field god (ta-no-kami)**: elsewhere a plain stone or no fixed figure; the carved Satsuma "tanokansā" is `[off-map: Satsuma]`. Field, occasional, small.
- **Earth god stone (jijin / ji-no-kami)**: small stone for the land's own god. Yard/field, occasional, small. (assumed)
- *Benzaiten stone or hokora on a pond islet (Benten)* → S105, under W §7.
- *Fudō Myōō stone* → S096, under W §5.
- *Nenbutsu name stone (myōgō-hi)* → S090, under W §5.
- *Lotus Sutra title stone (daimoku-tō)* → S091, under W §5.
- **Lotus-sutra pilgrim memorial (rokujūrokubu kuyōtō)**: stones for pilgrims who carried the Lotus Sutra to the 66 provinces; many Kyōhō–Genbun dates. Commons, occasional, small. (verify peak)
- *Moon-vigil stones (nijūsan-ya-tō / jūku-ya-tō)* → S089, under W §5.
- *Ōyama pilgrimage road marker (Ōyama-michi dōhyō)* → S062, under W §6.
- **Village boundary post or stone (mura-zakai bōji / mura-zakai ishi)**: wooden post or stone "village X starts here", often beside a dōsojin; fights over commons (iriai) were many. Roadside/commons/forest, common (R) / occasional (W), small. Hook: navigation, map information. {seam S125: R §12 + W §13}
- **Province and domain boundary post (kokkyō-gui / kokkyō-hi / ryōbun-gui)**: wooden or stone post or pillar reading "From here east: Sagami", or naming the domain or shogunal land; pairs face each other across a province line; disputes were frequent. Roadside/forest/commons, rare (province) / occasional (domain), small–medium. Hook: NAVIGATION (a province crossing; whose land), landmark. (wording assumed) {seam S124: R §12 + W §13}
- **Insect memorial stone (mushi kuyōtō)**: for insects killed in farming. Commons, rare, small.
- *Traveller's grave by the road (yukidaore-baka)* → S136, under W §17.
- *Kannon pilgrimage copy stones (utsushi reijō)* → S094, under W §5.
- *Seated stone Buddha (sekibutsu)* → S095, under W §5.
- *Stone Ebisu (ebisu-ishi)*: see §15; not counted here.
- **Dairokuten stone**: a guardian stone in Kanto villages. Commons, rare, small. (verify)
- *Hōkyōintō or gorintō by the road (roadside memorial)* → S092, under W §5.
- *Wooden Enkū figures*: rough-carved wooden Buddhas by the monk Enkū (died 1695) in Mino and Hida village halls: interior, so BL; noted here because they are a genuinely period rustic figure. Not counted.
- *Pilgrim-mountain mound (Fuji-zuka)*: `[outside 1680-1750: first built 1779]`. Counted in §17.

### == R §13 Village commons, signals and boundary customs ==

- **Communal well (mura-ido / idobata)**: shared well at a village lane junction or in a back-alley tenement, with a wash area round it; the social centre. Commons/alley, common, medium. Hook: water, meeting point. (BL: Civic wells; Dwellings, shared alley facilities) {seam S160: R §13 + U Streets: Wells and street water supply}
- *Fire-watch ladder with bell (hi-no-mi bashigo, hanshō)* → S200, under U Streets: Fire-fighting and night-watch fixtures.
- **Alarm bell on a frame or tree (hanshō)**: a small bell hung on a post or a tree. Commons, occasional, small. Hook: alarm. (assumed for villages)
- *Wooden clappers of the night watch (hyōshigi)* → S201, under U Streets: Fire-fighting and night-watch fixtures.
- **Conch trumpet (hora-gai)**: blown to call villagers together or signal. Commons, occasional, small. Hook: signal item.
- **Village assembly tree**: a big tree at the shrine or crossroads where villagers met. Commons, common, large (the tree is nature flavour; a stone seat is the prop). Hook: landmark.
- **Village boundary rope (kanjō-nawa / kanjō-kake)**: thick straw rope across the road at the village entrance, hung with straw charms, sandals and wooden tags, renewed at New Year to keep epidemics and evil out; Kinki (Wakasa, Shiga, Iga, Nara, Mie, southern Yamashiro). Roadside/commons, occasional (Kinai), medium. Hook: a tell that a village is ahead, landmark, lore. (verify examples) {seam S126: R §13 + W §13}
- **Straw serpent on trees (ja / jagi)**: a long straw snake wound on trees at the village entrance, in Nara and Shiga. Commons, occasional, medium. Hook: landmark. (verify)
- **Giant straw sandal charm (ō-waraji)**: a huge straw sandal at the village entrance to tell demons a giant lives here. Commons, occasional, small–medium. Hook: landmark. (verify date)
- *Smallpox-god offerings (hōsō-gami, sandawara)* → S127, under W §13.
- **Rain-prayer bonfire site (amagoi-bi / senba-bi)**: a cleared hilltop where villages lit rain-prayer fires in drought, with drums and banners (R §14). Mountain/commons, occasional (R) / rare (W), `[terrain]` + pyre. Hook: fire, landmark. (verify) {seam S129: R §13 + W §14}
- *Headman's yard at tax time*: rice bales lined up for inspection (see §4 rice bales). Not counted.
- *Village granary*: BL. Not counted.
- *Notice board (kōsatsuba)*: BL (Government / civic). Cross-reference only, not counted.
- *Stone slab bench at a crossroads (koshikake-ishi)* → S064, under W §3.
- *Stone water trough at the village entrance (for travellers' horses)* → S065, under U Streets: Street furniture.
- *Periodic market site (ichi-ba)* → S202, under U Festivals: Markets and fairs.
- *Village sumo ring*: BL. Not counted.
- **Commons pasture (maki)**: open grazing land with an earth bank (noma-dote) in horse-rearing areas. Commons, occasional, `[terrain]`. Hook: open land, horses. (verify for our map)
- *Wakamono-yado yard*: BL (young men's lodge). Not counted.
- **Stone for sharpening at a stream (to-ishi-ba)**: a flat stone at the water used by all. Commons, occasional, small. (assumed)

### == R §14 Festivals and seasonal temporary structures ==

- *Portable shrine in procession (mikoshi)* → S203, under U Festivals: Festival sets and seasonal dressing.
- *Village festival float (danjiri / dashi / yatai)* → S204, under U Festivals: Festival sets and seasonal dressing.
- *Bon-dance tower (bon-odori yagura)* → S205, under U Festivals: Festival sets and seasonal dressing.
- **Festival banners (nobori / matsuri nobori)**: long vertical banners on bamboo poles lining a shrine approach, and pairs of huge banners on tall poles at ward or shrine entrances. Shrine/commons/street, common (seasonal), medium–large. Hook: landmark visible from afar. Donated and shop banners: U. {seam S206: R §14 + U Festivals: Festival sets and seasonal dressing}
- **Festival lanterns (chōchin tsunagi / mandō / kennō-chōchin dana)**: paper lanterns on ropes along eaves or bamboo poles, or on wooden frames of named donated lanterns, lit at festivals. Shrine/street, common (seasonal) / occasional, small–medium. Hook: light. (strings: WC §1.7 "assumed; confirm with a pre-1750 image", still unconfirmed) {seam S207: R §14 + U Festivals: Festival sets and seasonal dressing + U Religious: Shrine forecourt}
- **New Year bonfire (sagichō / dondo-yaki)**: a cone of bamboo, straw and New Year decorations burned in mid-January in a field, riverbed or town space. Field/commons/street, common (villages) / occasional (towns), medium–large. Hook: fire, warmth, event. {seam S208: R §14 + U Festivals: Festival sets and seasonal dressing}
- **Insect-sending procession (mushi-okuri)**: summer torches, drums and a straw figure (often "Sanemori") carried to the village edge and burned or thrown in a river. Field/commons, occasional (seasonal), medium. Hook: event, light. (Edo-period custom; verify local forms)
- **Sanemori straw figure (Sanemori-ningyō)**: the mounted-warrior straw doll of the insect procession. Field, occasional, medium. Hook: landmark, spooky.
- **Seedbed inlet offering (minakuchi-matsuri)**: branches, flowers and a shrine charm stuck at the seedbed water inlet in spring. Field, common (seasonal), small. Hook: lore.
- **Harvest offering sheaves (kariage)**: first or last sheaves offered to the field god. Field/yard, common (seasonal), small.
- **Rice-planting festival gear (ta-ue matsuri / hana-taue)**: decorated ox saddles and drums of the flower rice-planting; the big forms are `[off-map: Chūgoku]`. Field, rare, medium.
- **Bon send-off straw boats (shōryō-bune)**: small straw boats with offerings pushed out on river or sea. Shore/ field, occasional (seasonal), small–medium. Hook: water event.
- **Tug-of-war rope (tsuna-hiki)**: a huge straw rope for inter-village tugs at New Year or Bon. Commons, rare, large prop. `[mostly off-map: Kyushu, Okinawa]` (verify Kinai examples)
- **Carp streamers (koinobori)**: carp-shaped streamers, born among Edo townsmen in the mid-Edo period as an answer to the samurai banners. `[outside 1680-1750: mid-to-late 18th c.]` (verify). For 1730 use warrior banners and plain fukinagashi streamers. {seam S209: R §14 + U Festivals: Festival sets and seasonal dressing}
- **Boys' Festival banners (musha-e nobori / sekku nobori, fukinagashi)**: tall painted warrior banners, crested banners and plain streamers raised by samurai and rich commoner houses on the 5th of the 5th month. Yard/street, occasional (seasonal), medium–large. Hook: landmark. {seam S210: R §14 + U Festivals: Festival sets and seasonal dressing}
- **Moon-viewing offering (tsukimi-dai)**: pampas grass and dumplings on a stand on the veranda or by water (8th month). Yard/street, common (seasonal), small. {seam S211: R §14 + U Festivals: Festival sets and seasonal dressing}
- **Rain-prayer props (amagoi)**: drums, banners and fires on the hill; see §13 for the fire site. Commons, occasional, small–medium.
- **Doll-floating boats (hina-nagashi)**: straw-and-paper dolls floated away in spring. Shore/field, rare, small. (verify date)
- **Temporary stage (kari-butai)**: planks on trestles for travelling players, kagura or puppets at shrine festivals. Shrine/festival, occasional (seasonal), medium. Hook: event, elevation. The permanent rural kabuki stage (nōson butai) is mostly late 18th–19th c. (verify; BL). (U form assumed) {seam S212: R §14 + U Festivals: Entertainment grounds and stages}
- **Offered sake barrels (komo-daru / kazari-daru)**: straw-wrapped sake barrels stacked as offerings at a shrine. R: occasional, but the stacked-wall display may be later (verify); U: `[outside 1680-1750: likely later]` (verify). Suggested reading: a few barrels IN, the decorated wall later. Shrine, medium. Hook: drink, cover. {seam S213: R §14 + U Religious: Shrine forecourt}
- **Stone mortar for festival mochi (matsuri-usu)**: the communal mortar at the shrine. Shrine, occasional, medium.
- *Sumo straw-bale ring (temporary)*: BL. Not counted.
- **Ancestors' lanterns at graves (bon-dōrō)**: paper lanterns on stakes at graves in Bon. Commons, common (seasonal), small. Hook: night light.

### == R §15 Fishing villages: shore ==

- **Beached boats (hama-age no fune)**: small fishing boats hauled above the tide line on timber skids. Shore, common, medium. Hook: cover, boat (vehicle), wood.
- *Boat skids and rollers (koro / bangi)* → S141, under R §15.
- **Boat haul-up beach and capstan (funa-age-ba; kagurasan; koro)**: a sand or shingle slope, or a cobbled or stone ramp, with timber skids and rollers and a vertical wooden capstan pushed round with long bars to wind boats up the beach; the same capstan hauls beach seines (Kujūkuri sardine nets `[off-map-ish: Bōsō]`). Shore, common, medium (ramp `[terrain]`). Hook: interactable, a boat, cover, wood. (kagurasan word from *Wakan Senyōshū*, 1766; net capstans verify) (BL: harbour breakwater and boat-hauling slip) {seam S141: R §15 + W §19}
- **Boat on trestles under repair (fune-dai)**: a hull propped on blocks for caulking and tarring. Shore, occasional, medium. Hook: cover.
- **Oars, poles and boat gear (kai, ro, sao; tomo)**: punting poles, sculling oars, bailers, mats and rope stacked against a hut or boat or loose in moored boats. Shore/canal, common, small. Hook: improvised weapon, loot. {seam S164: R §15 + U Water: Boats moored in town}
- **Beach-seine boats (jibiki-ami bune)**: the bigger net boats of the Kujūkuri sardine seines. Shore, occasional (Kazusa), large. Hook: vehicle, landmark.
- **Net-drying rack (ami-hoshi-ba / ami-kake)**: poles and crossbars along the beach with nets hung over them. Shore, common, medium–large. Hook: cover, loot (net, rope). {seam S142: R §15 + W §19}
- **Nets spread on sand or grass (ami-hoshi)**: Shore, common, small. Hook: net.
- **Net-dyeing tubs and fire (ami-zome)**: persimmon tannin or bark dye boiled to preserve nets. Shore, occasional, small. Hook: crafting. BL: net shed.
- **Floats and sinkers (uki, iwa)**: wooden or bamboo floats, clay or stone sinkers in heaps. Shore, common, small. Glass floats are `[outside 1680-1750: Meiji]`.
- **Fish-drying racks (himono-dana / hoshi-ba)**: split fish on bamboo racks and mats. Shore, common, medium. Hook: food. BL: Rural industry, fish-drying racks.
- **Sardine drying on the beach (hoshika / iwashi-boshi)**: whole sardines spread on the sand or mats to dry for fertiliser; huge in Kujūkuri. Shore, common (Kanto coast), `[terrain]`. Hook: food, trade, smell. BL: dried-sardine works.
- **Squid-drying lines (surume-boshi)**: split squid pegged on lines. Shore, occasional, medium. Hook: food.
- **Seaweed drying (kaisō hoshi-ba)**: wakame, hijiki, arame and tengusa (agar weed, big in Izu) on lines, poles and mats on the beach. Shore, common in villages / occasional on wild coast, small–medium. Hook: FOOD. Kanten date disputed (§3.3; verify). {seam S143: R §15 + W §19}
- **Nori stakes (nori-hibi)**: rows of bamboo and brushwood stakes planted in bay shallows and tidal flats for laver; Edo Bay (Shinagawa, Ōmori), begun about the Genroku–Kyōhō years. Shore, occasional (Edo Bay), `[terrain]` + rows. Hook: food, landmark, wading hazard. (verify start date) (BL: nori farm) {seam S144: R §15 + W §19}
- **Nori-drying frames (nori-hoshi)**: small reed mats with pressed laver on slanted racks. Shore, occasional, medium. Hook: food.
- **Octopus-pot stacks (takotsubo)**: unglazed clay pots with rope loops, roped in long lines and stacked on the beach; Akashi and the Inland Sea. Shore, occasional (Kinai coast), small. Hook: clay; dressing (not a container, per the loot rule). {seam S145: R §15 + W §19}
- **Basket fish trap (uke / dō / mondori / tsubo)**: cone-mouthed bamboo traps weighted in streams or stacked by the huts. River/shore, common, small. Hook: FOOD, trap item. {seam S116: R §15 + W §9}
- **Fish-keeping cages (ikesu)**: fenced or floating cages holding live fish. Shore, occasional, medium. Hook: food.
- **Tidal stake weir (hibi-ami / sashi-ami)**: stake-and-net fence on the tidal flat trapping fish at ebb. Shore, occasional, `[terrain]` + stakes. BL: fish weir (river).
- **Stone tidal fish trap (ishi-hibi / sukui)**: semicircular stone walls on the tidal flat that strand fish at the ebb. Shore, rare, `[terrain]`. Hook: food. `[off-map: Kyushu, Seto, Okinawa mostly]` {seam S146: R §15 + W §19}
- **Anchor (ikari)**: stone or wood-and-stone anchors on the sand, or an iron four-pronged grapnel half buried. Shore, common in villages / rare (iron, wild coast), small. Hook: LOOT (iron). {seam S151: R §15 + W §20}
- *Boat-hauling slip (fune-ba / age-ba)* → S141, under R §15.
- **Ebisu stone (ebisu-ishi)**: the fishers' god as a stone at the landing, often one fished up or washed ashore; drowned bodies found at sea were also treated as Ebisu. Shore, common in villages / occasional, small. Hook: landmark, lore. {seam S152: R §15 + W §20}
- **Funadama or Konpira votive lantern (umi no tōrō)**: a stone lantern at the landing for sea safety; Konpira lanterns boom later. Shore, occasional, medium. Hook: light. (the Konpira boom is `[outside 1680-1750: late 18th c.]`; verify)
- **Diver's tub and float (ama-oke / ama no tarai)**: wooden tub floated by women divers, with a rope and bag; beached at a diving cove. Shore, occasional (Shima, Ise, Izu), small. Hook: lore, loot (rope). (BL: ama-goya) {seam S150: R §15 + W §19}
- **Shell heap and lime-burning pit (kaigara-zuka / kaibai-yaki)**: shells piled and burned in a pit for lime. Shore, occasional (villages) / rare (remote beach), small–medium `[terrain]`. Hook: fire, crafting (lime, plaster). {seam S149: R §15 + W §19}
- **Driftwood stacks (yorigi)**: storm driftwood gathered above the tide line for fuel. Shore, common in fishing villages / occasional on wild coast, small. Hook: FUEL. Natural driftwood: N §R. {seam S053: R §15 + W §19}
- *Beach clothes-and-net lines (hoshi-zao)* → S162, under U Streets: Street surface.
- **Tar or pitch pot on a fire (chan-nabe)**: pot of pine tar for boats. Shore, occasional, small. Hook: crafting. (assumed name)
- *Tsunami memorial stone (tsunami-hi)* → S140, under W §17.
- *Beach watch fire (hama-bi)* → S130, under W §14.
- **Seaweed-cutting poles and hooks (mo-kari zao)**: long poles for cutting seaweed from boats. Shore, occasional, small. (assumed)
*- *Also relevant, not counted: net shed, boat shed, diver's hut, fish-spotting tower, whaling station, katsuobushi works, lighthouse lantern, weather hill: BL.**

### == R §16 Salt villages ==

- **Tidal salt field (irihama)**: embanked sand fields filled through sluices by the tide, with channels and graded sand beds; the Inland Sea standard (Akō). Shore, common (salt villages), `[terrain]` large. Hook: landmark, salt. BL: Rural industry, salt field tidal.
- **Spread salt field (agehama)**: a levelled sand field above the tide onto which seawater was carried and splashed by hand; Ise, Kanto, Noto (`[off-map]`). Shore, common (salt villages), `[terrain]` large. BL: salt field spread.
- **Salt-field embankment and sluice (enden tsutsumi, hi)**: the stone and earth bank round a tidal salt field with its wooden tide gate. Shore, common, large. Hook: high path, interactable gate.
- **Sand filter pit (numai)**: a boxed pit where salted sand is heaped and seawater poured through it to make brine (irihama). Shore, common, medium.
- **Brine box (tare-fune)**: the square filter box of the spread type. Shore, common, medium.
- **Seawater shoulder buckets (ninai-oke)**: pairs of buckets on a pole for carrying seawater and brine. Shore, common, small. Hook: water (salt) carrier item.
- **Splashing bucket (shiomaki-oke)**: bucket for throwing seawater across the spread field. Shore, common, small. (name verify)
- **Sand harrow (maguwa)**: toothed harrow dragged to level and turn the sand. Shore, common, small–medium.
- **Sand rake (eburi / iburi)**: long wooden rake, about 1.8 m, for gathering salted sand. Shore, common, small.
- **Filter-pit hoe (nui-hori-guwa)**: hoe for digging out spent sand. Shore, common, small.
- **Brine storage pit (kansui-tame / mae-tsubo)**: a covered pit or tub holding brine for the boiling hut. Shore, common, medium. Hook: hazard.
- **Fuel stacks for boiling (pine brush, matsuba)**: huge piles of brushwood and pine needles by the boiling hut; salt villages stripped their hills (the Shōdoshima boar-wall story). Shore, common, medium. Hook: fuel, cover.
- **Salt bales (shio-dawara / shio-kamasu)**: straw bales and bags of salt awaiting shipment. Shore, common, small. Hook: salt (food preservation), trade.
*- *Also relevant, not counted: salt-boiling hut (kama-ya): BL.**

### == R §17 Later and anachronistic figures and props (tagged, for reference) ==

*Listed so nobody models them by reflex. Stephen decides whether any come in anyway.*
- **Tanuki with a sake flask (Shigaraki tanuki)**: `[outside 1680-1750: 1930s–50s]` Shigaraki potters' creation, famous after an imperial visit in 1951. Yard, —, small–medium.
- **Beckoning cat (maneki-neko)**: `[outside 1680-1750: c.1850s]`, first recorded as Imado ware sold at Asakusa; urban anyway. Yard/shop, —, small.
- **Stone Inari foxes (ishi-kitsune)**: `[outside 1680-1750: mostly after mid-18th c.]`; one of the oldest Kanto pairs (Ōji Inari) is dated 1764. For 1730 use small wooden or ceramic foxes, or none (verify). Shrine, —, medium.
- **Fukusuke figure**: `[outside 1680-1750: c.1800s]`. Shop, —, small.
- **Daruma doll**: `[outside 1680-1750: Takasaki papier-mâché from the 1780s–90s]` (verify). Yard/shop, —, small.
- **Kappa and frog statues (kaeru)**: `[outside 1680-1750: modern]`. —.
- *Carp streamers (koinobori)*: `[outside 1680-1750: mid-to-late 18th c.]`, counted in §14; not counted again.
- **Glass fishing floats**: `[outside 1680-1750: Meiji]`. Shore, —, small.
- *Tall stone night-lamp towers (jōyatō)* → S070, under W §3.
- *Shrine-name pillar and donor stone fences (shagō-hyō, tamagaki with names)* → S191, under U Religious: Shrine forecourt.
- **Pilgrim Fuji mound (Fuji-zuka)**: `[outside 1680-1750: first built 1779, Takata]`. Shrine, —, large `[terrain]`.
- *Miniature 88-temple circuits (Shikoku utsushi)* → S094, under W §5.
- **Ridged washboard (sentaku-ita)**: `[outside 1680-1750: Meiji]` (verify). Yard, —, small.
- **Wheelbarrow (neko-guruma)**: `[outside 1680-1750: late Edo–Meiji]` (verify). Yard, —, small.
- **Triple water wheel (Asakura sanren suisha)**: `[outside 1680-1750: 1789]` `[off-map: Chikugo]`. Field, —, large.
- *Clipped tea-row plantations*: `[outside 1680-1750: Meiji, from 1869]`. Counted in §3; not counted again.
- *Rectangular paddy grid*: `[outside 1680-1750: Meiji, 1899 law onwards]`. Counted in §1 notes; not counted again.
- *Village fire-watch towers (hi-no-mi yagura)*: `[outside 1680-1750: rural, Meiji–Shōwa]`. Counted in §13; not counted again.
- *Family-name gravestones ("X-ke no haka")*: `[outside 1680-1750: Meiji]`. Counted in §11 notes; not counted.
- **Gyokuro shaded-tea (the famous Uji gyokuro)**: `[outside 1680-1750: 1835]`; the shading itself is older (§3).
- *Stone cart tracks (kuruma-ishi)* → S057, under W §2.
- **Paddy carp farming (Saku koi)**: `[outside 1680-1750: 1746 tradition]` (verify). Field, —.
- *Sweet potato fields in Kanto/Kinai*: `[outside 1680-1750: 1735+ on our map]`, counted in §3.
- *Paired dōsojin in quantity*: mostly 1804–30, counted in §12.
- *Stone "tanokansā" field gods*: `[off-map: Satsuma]`, counted in §12.
- *Snow-country gear (yuki-gakoi, tall hasa)*: `[off-map]`, counted in §4 and §8.
**Counting note: §17 counts 17 entries (the ones not already counted in an earlier group).**

## 2.U Urban man-made (U_URBAN.md): 496 entries

### == U Streets: Street surface, drains and alleys ==

- **Earth street (tsuchi no michi)**: packed earth and gravel, dusty in summer and deep mud after rain; town streets were not paved. Street, common, `[terrain]`. Hook: footprints and cart ruts, mud slows movement.
- **Main street of a post town (shukuba ōkan)**: the highway itself running through town, often 4–5 ken wide with a central or side gutter. Street, common, `[terrain]`. Hook: long sightline, chokepoint. (assumed width)
- **Cranked street / blind turns (kagi no te, tōmi-kakushi)**: deliberate right-angle jogs and T-junctions in castle towns and at post-town ends to break sightlines. Street, common in castle towns, `[terrain]`. Hook: ambush corners, cover.
- **Firebreak wide street (hirokōji)**: street widened after the Meireki fire of 1657 (Ueno, Ryōgoku, Asakusa, Nihonbashi area). Street, occasional (big cities), `[terrain]`. Hook: open ground, event space. → BL Civic "firebreak plaza" for the site.
- *Sloped street with stone steps (ishidan-zaka)* → S060, under W §2.
- **Stone-paved temple approach (ishidatami sandō)**: fitted stone slabs on the approach to a big temple or shrine; not on ordinary streets. Temple/shrine forecourt, occasional, `[terrain]`. Hook: quiet footsteps vs gravel (assumed).
- *Stone-paved pass road through a town (ishidatami)* → S056, under W §2.
- **Roadside ditch and street gutter (sokkō / omote-dobu)**: earth or stone-lined ditch along the highway, and along town house fronts carrying rain and wash water to the canal. Roadside/street, common, `[terrain]`. Hook: cover (prone), wet feet, a place to drop small loot. (lining assumed) {seam S058: U Streets: Street surface + W §2}
- **Stone-lined gutter (ishi-mizo)**: dressed-stone channel along better streets and temple approaches (assumed). Street, occasional, `[terrain]`.
- **Alley centre drain with board covers (dobu-ita)**: the famous plank cover over the drain running down the middle of an Edo back-alley (ura-nagaya); planks rattle when walked on. Alley, common, medium. Hook: noise underfoot, hide small items under a loose board. (BL: Dwellings, ura-nagaya)
- *Slab bridge over a gutter (mizo-ita, ishi-ita)* → S073, under U Water: Bridges.
- **Drain grating / cover stone (futa-ishi)**: pierced or slotted stone cover over a gutter where it passes under a lane (assumed). Street, occasional, small.
- **Back-to-back sewer (seiwari gesui, "Taikō gesui")**: stone-lined drains running between the backs of house plots in Osaka, laid from 1583 and still in use in 1730. Street/back plots, landmark (Osaka), `[terrain]`. Hook: a crawlable ditch route between blocks (gameplay licence). (verify stone date)
- **Drain outfall into canal (gesui-guchi)**: opening in the canal wall where a street drain empties. Canal, common, small. Hook: none.
- **Alley entrance (roji-guchi)**: narrow opening between two street-front houses leading to the back tenements, often with a small wooden gate. Alley, common, medium. Hook: chokepoint.
- **Alley gate (roji kido)**: light wooden door frame at an alley mouth, shut at night (assumed; smaller than the ward kido). Alley, common, medium. Hook: door, choke.
- **Alley resident board (roji kanban)**: boards over the alley mouth listing the trades of the tenants (tailor, teacher, masseur) (verify date; common in late-Edo prints). Alley, occasional, small. Hook: navigation.
- **Kyoto narrow lane (zushi, roji)**: dead-end lane into the middle of a Kyoto block. Alley, common (Kyoto), `[terrain]`.
- **Street crossroads (tsuji)**: named crossing, often with a notice board, a small shrine or a corner toilet. Street, common, `[terrain]`. Hook: meeting point.
- **Water-sprinkling kit (uchimizu oke to hishaku)**: bucket and ladle for sprinkling the street against dust and heat. Street, common, small. Hook: water, loot spot.
- **Street broom and dustpan (hōki, chiri-tori)**: every house swept its own frontage. Street, common, small.
- *Sand heaps for processions (morizuna)* → S059, under W §2.
- **Door-side sand cones (tate-zuna)**: pair of neat sand cones beside the gate of a house expecting an honoured guest (Kyoto; verify). Street, rare, small.
- **Cart-guard stones at corners (kuruma-yoke ishi)**: stone posts at building corners to stop cart wheels scraping the walls (verify date). Street, occasional, small. Hook: low cover.
- *Stone cart-track paving (kuruma-ishi)* → S057, under W §2.
- *Horse-dung on the highway (bafun)* → S154, under W §21.
- **Laundry pole (monohoshi-zao / sao-kake / hoshi-zao)**: bamboo pole on two forked posts, tripods or crossed supports, kimono threaded through the sleeves; yards, back alleys, courtyards, and by fishing houses with small nets. Yard/alley/shore, common, medium. Hook: cloth loot, visual cover. {seam S162: U Streets: Street surface + R §6 + R §15}
- **Rooftop drying platform (monohoshi-dai)**: board platform on the roof of a town house for drying clothes (verify date; late-Edo prints). Street (roofs), occasional, medium. Hook: climb, sightline.
- **Potted-plant shelves by the door (hachiue-dana, uekibachi)**: rows of potted plants along alley fronts; the Genroku gardening boom made them common in Edo (verify). Alley, common, small. Hook: dressing.
- **Hanging bird cage (tori-kago)**: songbird cages hung under eaves (bush warbler, white-eye); Edo bird keeping was a craze (verify date). Street, occasional, small. Hook: noise.
- **Street tree at a corner (tsuji no ki)**: willow at a canal corner or a single pine at a crossing (assumed). Street, occasional, medium. Hook: landmark. → nature flavour for the tree itself.

### == U Streets: Fire-fighting and night-watch fixtures ==

- **Street-corner fire tub with bucket pyramid (tsuji no ōoke, later tensui-oke)**: a large wooden tub of about 6 koku (~1,000 L) at a crossing, with small hand-buckets stacked on its lid. Street, common in cities, medium. Hook: water, fire-fighting.
- *Rain tub per house (tensui-oke)* → S161, under R §6.
- **Hand-bucket stack (teoke no tsumi)**: the pyramid of small handled buckets (often painted with the house mark) on a fire tub. Street, common, small. Hook: water, carry.
- **Eave-hung water buckets (noki no teoke)**: buckets filled with water hung from the eaves, required of each house after the Meireki fire (FDM). Street, common, small. Hook: water.
- **Temple fire tub (tensui-oke, cast)**: big bronze, iron or stone fire tub before a temple hall, often with donors' names. Temple forecourt, occasional, medium. Hook: water. (most survivors are late Edo; verify)
- **Fire ladder on a roof (yane-bashigo)**: fixed wooden ladder from eave to ridge so a house could be reached and wetted. Street, common, medium. Hook: climb.
- **Rooftop watch platform (hinomi-dai)**: small railed platform on a merchant's roof for spotting fires (assumed; distinct from the tall towers). Street, occasional, medium. Hook: climb, sightline.
- **Fire-bell ladder (hanshō-dai / hi-no-mi bashigo)**: tall free-standing ladder with a small platform and a half-bell (hanshō) on top, by the ward office; Edo put them on ward guardhouse roofs in 1723 (one per ~10 wards). Street, common in Edo wards; a post town may have one; rural ones `[outside 1680-1750: rural, Meiji+]` (R; BL §2.1 assumes one in larger villages: §3.3), large. Hook: climb, sightline, lookout, alarm (bell). (BL: Government "fire watchtower" for the samurai tower) {seam S200: U Streets: Fire-fighting and night-watch fixtures + R §13}
- **Fire watchtower (hi-no-mi yagura)**: tall timber tower at shogunal fire brigade compounds, 3 jō or more. Street, occasional, large. → BL Government.
- **Fire hook (tobiguchi)**: long pole with an iron hook for pulling down burning walls, racked outside the ward office. Street, common, small. Hook: weapon-like tool, loot.
- **Ladders and poles rack (hashigo-kake)**: rack of fire ladders and long hooks under the eaves of the ward office (jishinban). Street, common, medium. Hook: loot spot.
- **Fire standard (matoi)**: the brigade's crested standard on a pole; Edo's townsmen brigades (machi-bikeshi, iroha groups) date from 1718–1720. Street, occasional, small. Hook: landmark, trophy. (BL: Government)
- **Brigade lanterns (hikeshi chōchin)**: tall lanterns with the brigade's mark. Street, occasional, small. Hook: light.
- **Hand pump (ryūdosui)**: wooden hand-pumped water sprayer. `[outside 1680-1750: sold from ~1751, issued to Edo brigades 1764]` [TFD; FDM]
- **Wet straw mats and sacks (nure-mushiro)**: soaked mats thrown over roofs and walls in a fire (assumed). Street, event, small.
- **Firebreak earth bank (hiyoke-dote)**: long earth bank with pines, raised after 1657 to stop fire spreading (Edo, Kanda). Street, rare, `[terrain]`. Hook: cover, elevation. → BL Civic.
- **Firebreak open ground (hiyoke-chi)**: cleared land kept empty as a firebreak, in practice filled with stalls. Street, occasional, `[terrain]`. → BL Civic.
- **Night-watch clappers (hyōshigi)**: pair of hardwood blocks struck on the fire round ("hi no yōjin", mind the fire). Street/commons, common, small. Hook: noise item, noise lure. {seam S201: U Streets: Fire-fighting and night-watch fixtures + R §13}
- **Night-watch iron staff (kanabō, shakujō-type)**: staff with iron rings shaken on patrol (assumed). Street, occasional, small. Hook: noise.
- **Fire-caution notice (hi no yōjin fuda)**: wooden board or paper slip "beware of fire" at ward offices and kitchens (assumed). Street, common, small.
- *Fireproof storehouse row (dozō-zukuri)*: plastered kura used as a fire wall along a street. → BL (kura family).

### == U Streets: Street lighting and lanterns ==

*Towns were dark at night. Light came from shop signs, gate lanterns, lanterns people carried and a few fixed lamps at crossings and bridges.*
- **Crossroads lamp (tsuji-andon)**: wooden framed paper lamp on a post at a crossing, lonely junction or ward gate, lit by the ward. Street/roadside, occasional, small–medium. Hook: light, navigation, landmark. (verify how common in 1730; roadside form assumed) {seam S071: U Streets: Street lighting and lanterns + W §3}
- *Always-lit lamp (jōyatō)* → S070, under W §3.
- **Akiba fire-god lantern (Akiba jōyatō)**: roofed wooden lantern on a stone base dedicated to Akiba-sanjaku, the fire god, along the Tōkaidō in Tōtōmi and Mikawa. Street, occasional. `[outside 1680-1750: mostly 19th c.]` (verify)
- **Ward-gate lantern (kido chōchin)**: lantern hung on the ward gate, lit at closing time. Street, common, small. Hook: light.
- **Hanging shop-sign lamp (kake-andon)**: box lamp hung by the door with the shop's or inn's name, lit at dusk. Street, common, small. Hook: light, navigation.
- **Standing sign lamp (oki-andon, andon-kanban)**: floor-standing framed paper sign lit from inside, set out at dusk by eating houses, inns and brothels. Street, common, small. Hook: light.
- **Shop lantern (mise-chōchin)**: large paper lantern with the shop name hung at the eave. Street, common, small. Hook: light.
- **Inn front lantern (hatago chōchin)**: lanterns with the inn's name and association badge hung at post-town inns. Street, common, small. Hook: light.
- **Bow-stretched lantern (yumihari-chōchin)**: lantern held open on a bow-shaped frame, used by officials and night watches (17th c. on). Street, occasional, small. Hook: light, carryable.
- **Box lantern (hako-chōchin)**: lantern with lidded wooden top and bottom, carried by samurai households with the crest. Street, occasional, small. Hook: light.
- **Collapsible travel lantern (odawara-chōchin)**: cylindrical folding lantern that packs into its own lid; linked with Odawara in the Kyōhō era (verify). Street, common, small. Hook: light, carryable loot.
- **Hand lantern on a stick (bura-chōchin)**: small lantern dangled from a stick. Street, common, small. Hook: light.
- **Giant gate lantern (ōchōchin)**: huge red paper lantern hung under a temple gate. Temple forecourt, landmark. `[outside 1680-1750: Sensō-ji Kaminarimon lantern 1795]` (verify; smaller hanging lanterns at gates are fine)
- **Iron fire basket and watch fire (kagaribi / kagari)**: iron basket on three legs, a post or a boat burning pine splints: at castle gates, guard posts, temple night rites and river bends for night fishing; small fires or torches at field edges against boar. Castle/temple/river/field, occasional, small–medium. Hook: FIRE, light, heat. (BL: cormorant-fishing house) {seam S117: U Streets: Street lighting and lanterns + W §9 + R §5}
- **Torch on a stand (taimatsu-tate)**: pine torch set in an iron holder (assumed). Castle/festival, occasional, small. Hook: light.
- **Bridge-end lantern (hashi-zume tōrō)**: lantern post at the ends of big bridges (assumed). Canal, occasional, medium. Hook: light, landmark.
- **Candle and oil trade signs (rōsoku kanban)**: giant candle-shaped sign outside a candle shop (assumed). Street, occasional, medium.
- **Lantern-maker's drying frames (chōchin-hoshi)**: new lanterns hung out on poles to dry (assumed). Street, occasional, medium.

### == U Streets: Shop fronts: curtains, signs, banners, screens (outdoor fixtures) ==

- **Shop curtain (noren)**: split cloth curtain over the door, indigo with the shop mark in white; taken in at closing. Street, common, small. Hook: sightline break, open/closed signal.
- **Short eave curtain (mizuhiki-noren)**: long, shallow strip of cloth along the top of the whole shopfront. Street, common, small.
- **Rope curtain (nawa-noren)**: curtain of hanging ropes at cheap eating and drinking houses (verify date). Street, occasional, small.
- **Sun curtain (hiyoke-noren)**: big cloth awning dropped from the eave to the street on the sunny side of large dry-goods shops. Street, occasional (big shops). `[outside 1680-1750: best evidence 19th-c. prints]` (verify; Echigoya is the classic image)
- **Reed screen (yoshizu)**: standing or leaning reed screen shading a shopfront or tea stand. Street, common, medium. Hook: soft cover (sight only).
- **Bamboo blind (sudare)**: rolled blinds on the upper floor and eave. Street, common, small. Hook: sight cover.
- **Hanging signboard (kake-kanban)**: wooden board hung under the eave carrying the shop name or goods. Street, common, small. Hook: navigation.
- **Standing signboard (oki-kanban, tate-kanban)**: framed board on feet set out by the door. Street, common, small. Hook: low cover.
- **Roof signboard (yane-kanban)**: big board mounted on the roof ridge or eave front; Edo made rules on sign size (verify 1680s ruling). Street, occasional, medium. Hook: landmark.
- **Shape signs (katachi-kanban)**: three-dimensional signs shaped like the goods: a giant brush (brushmaker), a big geta, tabi sock, spectacles, a gourd (medicine), a pestle, an umbrella, a fan. Street, common, small / medium. Hook: navigation, landmark.
- **Gilt medicine board (kusuri kanban)**: lacquered board with gold characters naming a patent medicine, often roofed. Street, occasional, medium.
- **Cedar ball (sugidama, sakabayashi)**: ball of cedar sprigs hung by a sake brewer or seller (verify when common). Street, occasional, small. Hook: navigation.
- **Shop banner (nobori)**: tall narrow cloth banner on a bamboo pole with a sideways crossbar, used by shops for sales, by shrines and by theatres. Street, common, small. Hook: landmark, wind indicator.
- **Theatre banners (shibai nobori)**: rows of actors' name banners in front of a kabuki theatre. Street, landmark, medium. → BL Services kabuki theatre.
- *Theatre drum tower (yagura)*: the licensed drum tower on a theatre roof. → BL.
- **Shop display shelf (misedana)**: shelf across the open shopfront, folded down by day. Street, common, medium. → BL (part of the machiya front).
- **Fold-down bench (battari-shōgi)**: bench hinged to the house front that drops down by day (Kamigata). Street, common (Kyoto/Osaka), medium. Hook: rest.
- **Curved bamboo wall guard (inuyarai)**: arched bamboo fence at the foot of a Kyoto house wall against dogs and splashes. Street, common (Kyoto), medium. Hook: low obstacle.
- **Horse-stop rail (komayose)**: low wooden or bamboo rail in front of big houses and samurai gates. Street, occasional, medium. Hook: tie horses, low cover.
- **Door charms (kado-fuda, somin shōrai, Gion chimaki)**: paper charms and straw chimaki hung over the door all year (Kyoto; verify date for chimaki). Street, common, small.
- **Clay Shōki on the eave (yane-Shōki)**: small clay demon-queller figure on a Kyoto eave. Street, occasional. `[outside 1680-1750: 19th c.]` (verify)
- *Shop mark painted on the storehouse (kura no yagō)*: big crest painted on a kura gable. → BL (surface decal).

### == U Streets: Street furniture, tea-stand dressing and seats ==

- **Bench (shōgi / endai)**: low wide plank bench outside tea houses and shops (often with a red felt cover), under a mile-mound tree, at a pass or spring, and by the farmhouse door for rest and work. Street/roadside/yard, common, small–medium. Hook: rest, loot spot, a landmark cluster. {seam S063: U Streets: Street furniture + W §3 + R §6}
- **Red felt cover (hi-mōsen)**: red woollen cloth laid over a bench or on the ground for picnics. Street/festival, occasional, small. (imported wool; verify when cheap enough for tea stands)
- **Big paper parasol (nodate-gasa, ō-gasa)**: large oiled-paper parasol on a pole shading a bench or an outdoor tea service. Street/garden, occasional, medium. Hook: shade, landmark (red).
- **Tea kettle stand (chagama-dai)**: brazier and kettle set out at the front of a roadside tea stand. Street, common, small. Hook: heat, loot spot.
- **Smoking tray (tabako-bon)**: tray with a small fire pot and ash tube set on a bench for customers. Street, common, small. Hook: fire source (small).
- **Reed-screened tea stand (yoshizu-bari chaya)**: tea stand enclosed only by reed screens and a light roof, on bridges ends, riverbanks and temple grounds. Street/riverbed, common, medium. Hook: rest, soft cover. → BL Food "kake-jaya" for the stall itself.
- **Waiting bench for palanquins (kago-date)**: stand where street palanquin bearers wait for fares at crossings and bridge ends (assumed form). Street, occasional, medium. Hook: rest.
- *Rest stone (koshikake-ishi)* → S064, under W §3.
- **Horse and animal trough (mizu-bune / kaiba-oke)**: hollow log, wooden or stone trough fed from a stream or filled by hand: at inns and post offices, pass feet, tea stalls and village entrances, and by the stable for water or fodder. Street/roadside/yard, common, small–medium. Hook: WATER (animal grade). (BL: Civic, roadside horse trough) {seam S065: U Streets: Street furniture + W §3 + R §7 + R §13}
- **Hitching post and tie stone (uma-tsunagi / tsunagi-ishi)**: wooden post or stake with an iron ring, or a stone with a bored hole, by gates, stables, inns and roads. Street/roadside/yard, common, small. Hook: tie animals; dressing. (BL: Civic) {seam S066: U Streets: Street furniture + W §3 + R §7}
- **Mounting stone (fumi-ishi, noridai)**: stone block to mount a horse by a gate (assumed). Samurai quarter, occasional, small.
- **Foot-washing tub (ashi-arai-oke)**: tub and ladle set out at an inn's entrance for arriving travellers. Street, common, small. Hook: water.
- **Shoe rack and straw sandals for sale (waraji-kake)**: straw sandals hung in bunches outside a tea stand or general store. Street, common, small. Hook: loot (sandals).
- *Water jar at the door (mizugame)* → S161, under R §6.
- **Street kiosk / fortune-teller's table (ekisha no dai)**: small table with a lantern and divining sticks set up at a bridge end at night. Street, occasional, small. Hook: light.
- **Stand for a sign lantern and umbrella (kasa-tate)**: rack of paper umbrellas at an inn door (assumed). Street, occasional, small.
- **Stone boundary post (sakai-ishi)**: post marking the edge of a ward, a temple's land or a domain's (assumed urban form). Street, occasional, small. Hook: navigation.

### == U Streets: Peddlers', stalls' and street performers' kit (props) ==

*These are loose props that a street scene needs. The trades are in BL (Food, Services); here only the kit.*
- **Shoulder pole and loads (tenbin-bō / mokko)**: pole with two baskets, buckets or boxes, or a rope-net soil carrier; every peddler's and farmer's carrier, sometimes dropped by the road. Street/yard/roadside, common (dropped: rare), small. Hook: carrying, loot carrier, LOOT. {seam S155: U Streets: Peddlers' + R §7 + W §21}
- **Fishmonger's shallow tubs (bote-furi oke)**: two shallow tubs of fish on a pole. Street, common, small. Hook: food loot.
- **Tofu seller's box (tōfu-oke)**: water box on a pole. Street, common, small. Hook: food, water.
- **Water seller's buckets (mizu-uri, hiyamizu-uri)**: in summer, cold sugared water sold from brass-banded buckets with cups. Street, occasional, small. Hook: water.
- **Shouldered noodle stall (katsugi-yatai)**: two boxes on a pole, one with a charcoal fire and pot, one with bowls and noodles; the Edo night soba seller (the "nihachi" name appears Kyōhō era, verify). Street, common, small. Hook: heat, light, food.
- **Roofed street stall (yatai)**: small wheel-less stall with a roof, set up nightly (tempura, sushi, eel). Street, common, medium. Hook: food loot spot, cover. → BL Food "yatai family" (tempura yatai date there).
- **Goldfish seller's tubs (kingyo-uri oke)**: shallow tubs of goldfish on a pole (verify date for street goldfish sellers; mid-18th c.). Street, occasional, small.
- **Insect seller's cage stand (mushi-uri)**: stand of small cages of singing insects. `[outside 1680-1750: street sellers late 18th c.]` (verify)
- **Wind-chime seller's frame (fūrin-uri)**: frame of chimes carried on the back. Street, occasional. `[outside 1680-1750: glass chimes late 18th–19th c.; iron and bronze earlier]` (verify)
- **Fan seller's rack (uchiwa-uri)**: pole hung with round fans (assumed). Street, occasional, small.
- **Candy seller's parasol and costume (ame-uri)**: candy sellers with drums, parasols and song (assumed). Street, occasional, small.
- **Medicine peddler's wicker trunks (baiyaku no yanagi-gōri)**: stacked wicker boxes wrapped in a cloth, the Toyama medicine peddler (from about 1690, verify). Street, occasional, small. Hook: medical loot.
- **Rag and paper buyer's basket (kamikuzu-kai kago)**: basket and tongs of the waste-paper collector (assumed). Street, occasional, small.
- **Ash buyer's basket (hai-kai)**: basket for buying household ash as fertiliser and for dyers (assumed). Street, occasional, small.
- **Broom and bamboo-ware peddler's load**: towering bundle of brooms, dippers and baskets on a back frame (assumed). Street, occasional, small.
- **Monkey trainer's kit (sarumawashi)**: monkey on a lead, small pole and drum. Street, occasional, small. Hook: noise.
- **Lion-dance kit (daikagura, shishimai)**: wooden lion head with cloth body, drum and flute; also umbrella-spinning. Street/festival, occasional, small.
- **Street storyteller's stand (tsuji-kōshaku)**: small desk and fan-clap board; Fukai Shidōken lectured in Asakusa in the 1740s (verify). Street, occasional, small.
- **New Year comic dancers' kit (manzai)**: fan and hand drum of the travelling New Year duo. Festival, occasional (seasonal), small.
- **Peep-box show (nozoki-karakuri)**: box with lenses and pictures, pulled by strings. `[outside 1680-1750: common late 18th c.]` (verify)
- **Portable sweet stand (dango-dai)**: tray on legs for skewered dumplings (assumed). Street, common, small. Hook: food.
- **Handcart (daihachi-guruma / niguruma)**: large two-wheeled plank cart pulled by men; an Edo city vehicle attested by 1703; rare in the countryside, where packhorses and backs carried almost everything. Street/yard, common (Edo) / rare (villages), medium. Hook: vehicle, movable cover, loot carrier, storage surface. (rural rarity assumed; verify) {seam S163: U Streets: Peddlers' + R §7}
- **Osaka big cart (beka-guruma)**: the Osaka counterpart of the daihachi (verify date). Street, occasional (Osaka), medium.
- **Street palanquin (tsuji-kago)**: open bamboo hire-palanquin for commoners. Street, common, medium. Hook: carryable seat.
- **Lacquered palanquin (norimono)**: closed wooden palanquin of samurai and rich commoners. Street, occasional, medium. Hook: cover, loot spot.
- *Rice bales and sake casks stacked for loading (tawara, komo-daru)* → S214, under R §4.
- **Long chest on a pole (nagamochi)**: carried by two men. Street, occasional, medium. Hook: container look-alike (dressing only).

### == U Streets: Wells and street water supply ==

- *Communal alley well (idobata)* → S160, under R §13.
- *Pulley well with roof (tsurube-ido)* → S158, under R §6.
- *Lever well (hanetsurube)* → S157, under R §6.
- **Aqueduct box well (jōsui-ido, suidō-ido)**: square wooden well box fed by buried wooden pipes of the Kanda or Tamagawa aqueduct (the only two running in 1730; four others shut in 1722). Street/alley, common (Edo), medium. Hook: water. → BL Civic.
- *Well curb, wooden box (ido-waku)* → S159, under R §6.
- *Well curb, stone ring or stone box (ishi-gawa)* → S159, under R §6.
- **Well curb, pottery rings (kawara-gawa)**: fired clay ring sections stacked as a curb (verify date). Street, occasional, small.
- *Well lid (ido-buta)* → S159, under R §6.
- **Well bucket and rope (tsurube-oke)**: wooden bucket with an iron band. Street, common, small. Hook: water carrier loot.
- **Wash stone and drain slab (nagashi-ishi)**: flat stone around a well where washing is done, with a gutter away. Alley, common, small.
- *Well god offering (ido-gami)* → S099, under R §9.
- **Annual well cleaning (ido-sarai)**: on the 7th of the 7th month the alley emptied and cleaned its well; buckets, ropes and men down the shaft (verify). Alley, event, small set.
- **Buried wooden water main (tōi, mokuhi)**: square wooden pipe under the street; seen only where the road is dug up. Street, occasional, `[terrain]`. Hook: repair site dressing.
- **Aqueduct junction box (tame-masu, masu)**: wooden box under a lid where the mains branch (verify term). Street, occasional, small.
- *Bamboo water pipe (kakehi)* → S068, under R §2.
- *Aqueduct bridge (suidō-bashi, kakehi-bashi)* → S069, under R §2.
- **Famous spring well (meisui)**: a named spring well in Kyoto, often with a small shrine, where people queue with jars (e.g. Somei-i at Nashinoki; verify which were flowing in 1730). Street/shrine, landmark, medium. Hook: water, landmark.
- **Public wash steps (arai-ba)**: stone steps into a stream or canal for washing vegetables and cloth. Canal, common, medium. Hook: water. → BL Civic.
- **Water-seller's boat and landing (mizu-bune)**: in Osaka and eastern Edo, where wells were brackish, water came by boat to landing steps (assumed detail). Canal, occasional, medium. Hook: water. → BL Civic.

### == U Streets: Rubbish, nightsoil and toilets ==

- **Alley rubbish box (gomi-tame)**: wooden bin at the end of each Edo alley, emptied by contractors; Edo ordered rubbish taken to Eitai-jima landfill from 1655. Alley, common, medium. Hook: loot spot (junk). → BL Civic.
- **Rubbish boat (gomi-bune)**: boat carrying town rubbish to landfill. Canal, occasional, medium.
- **Landfill ground (gomi-suteba, Eitai-jima)**: raw reclaimed ground in the bay (assumed look). Canal/coast, landmark (Edo), `[terrain]`.
- **Street-corner toilet (tsuji-setchin)**: half-walled booth over a buried pot, set up by nightsoil dealers in Kyoto and Osaka. Street, occasional, medium. → BL Civic.
- **Urine tubs at the roadside (shōben-tago)**: open tubs set out at Kyoto and Osaka street edges to collect urine for farms (verify date; strongest evidence is 19th-c. Morisada). Street, occasional, small.
- *Nightsoil buckets and pole (koe-oke, koe-tago)* → S216, under R §3.
- **Nightsoil boat (koe-bune, kasai-bune)**: flat boat carrying nightsoil up the canals to farm villages (verify name). Canal, occasional, medium. Hook: smell (sound/particles), cover.
- *Ash and waste-paper collection points*: see peddlers' kit above.
- *Dead-animal disposal*: out of scope for town dressing; see BL marginal settlements.

### == U Streets: Notices, control and punishment fixtures ==

- **Official notice board (kōsatsu)**: roofed board on a stone or earth base, fenced, with the shogunate's edicts; at bridge ends, main crossings and town entrances. Street, common, medium. Hook: landmark, lore text. → BL Government "notice board (kōsatsuba)".
- **Ward rules board (chō-okite fuda)**: smaller board at a ward gate or ward office (assumed). Street, common, small. Hook: lore text.
- **Wanted and crime slips (sute-fuda, hari-fuda)**: paper notices pasted on walls and gates (assumed). Street, occasional, small.
- **Petition box (meyasubako)**: locked box set out at the Hyōjōsho gate from **1721** (Yoshimune) on set days; led to the charity clinic of 1722. Street, landmark (Edo), small. Hook: lore. (BL: Civic)
- **Dismount sign (geba-fuda, geba-ishi)**: board or stone reading "dismount" at temple and castle gates and mausolea. Temple/castle, common, small. Hook: landmark.
- *Prohibition stele at Zen gates (kaidan-seki)* → S104, under W §6.
- **Exposure place (sarashi-ba)**: spot at the south end of Nihonbashi where convicted people were exposed to the public (assumed layout: mat, stakes, a fence). Street, landmark (Edo), medium. Hook: grim landmark.
- **Head-display stand (gokumon-dai)**: wooden stand for displaying executed heads at execution grounds. Execution ground, rare, medium. → BL Government "execution grounds". (neutral)
- *Crucifixion posts (haritsuke-bashira)*: at execution grounds. → BL Government. (neutral)
- **Lost-child stone (maigo-shirabe-ishi)**: stone for posting notices about lost children. `[outside 1680-1750: 1857, Ichikoku-bashi]`
- *Road distance post in town (michi-shirube, dōhyō)* → S061, under W §1.
- **Zero milestone (dōgen)**: the origin of the five highways at Nihonbashi. Street, landmark. (Current marker is modern; model a plain post. verify)
- **Weighing and measuring stand (hakari-ba)**: public scale at a market or quay (assumed). Market, occasional, medium.

### == U Streets: Town gates, boundaries and quarter edges (outdoor parts) ==

- **Ward gate (kido)**: posts, beam and two leaves plus a wicket door at each end of a ward, shut about 10 pm. Street, common in the three cities, medium. Hook: chokepoint, door. → BL Government (gate and gatekeeper's hut).
- **City entrance gate with stone walls (ōkido)**: stone walls on both sides of the highway where it entered Edo: Yotsuya Ōkido (1616) and Takanawa Ōkido (moved there 1710); the gate leaves were removed in 1792, so in 1730 they are still gates. Street, landmark, large. Hook: chokepoint.
- **Post-town end bend and bank (mitsuke, masugata)**: an earth bank, often stone-faced, with a bend in the road at each end of a post town. Street, common (post towns), medium. Hook: chokepoint, cover.
- **Kyoto's old earth rampart (Odoi)**: broken bamboo-topped earth bank and ditch from 1591, cut through by roads. Street edge, landmark, `[terrain]`. Hook: cover, elevation.
- *Castle outer ring gates (mitsuke)*: guarded gates on the outer moat of Edo Castle. → Castle groups, BL Military.
- **Pleasure-quarter moat (ohaguro-dobu)**: the walled ditch round the New Yoshiwara (1657). Street/canal, landmark (Edo), `[terrain]`. Hook: boundary, water.
- **Looking-back willow (mikaeri-yanagi)**: the willow at the Yoshiwara approach where departing clients looked back. Street, landmark, medium (tree). → nature flavour for the tree.
- **Yoshiwara embankment road (Nihon-zutsumi)**: raised road across paddies to the Yoshiwara, lined with reed tea stands. Street, landmark, `[terrain]`.
- *Quarter main gate (ōmon)*: the single gate of a licensed quarter. → BL (gate family).
- **Chō boundary marker (chō-zakai)**: post or stone marking where one ward ends (assumed). Street, occasional, small.

### == U Water: Bridges: types ==

- **Great wooden trestle bridge (Nihonbashi type)**: long timber bridge on many post piers with a raised middle; Edo's Ryōgoku (1661), Shin-Ōhashi (1693), Eitai (1698), the Tōkaidō's Yahagi (~370 m). Canal/river, landmark, large. Hook: landmark, chokepoint, sightline, underside cover. → BL Civic.
- **Arched wooden bridge (sori-hashi, taiko-bashi)**: steeply arched timber bridge; vermilion at shrines, plain or vermilion in gardens. Garden/shrine, occasional, medium. Hook: landmark, climb. → BL Civic and Shinto "sacred bridge".
- **Plank bridge (ita-bashi / kōran-bashi)**: beams and boards on posts over a canal, stream or garden pond, with or without post-and-rail parapets. River/canal/garden, common, medium. Hook: crossing, chokepoint. (BL: Civic, roads) {seam S074: U Water: Bridges + W §4 + U Gardens: Garden bridges}
- *Flat bridge with railings (kōran-bashi)* → S074, under U Water: Bridges.
- **Earth-covered bridge (dobashi)**: logs or a timber deck covered with brushwood, earth and turf, like a strip of ground; country streams, castle approaches and gardens. River/castle/garden, occasional, medium. Hook: crossing. (BL: Civic) {seam S075: U Water: Bridges + W §4 + U Gardens: Garden bridges}
- **Stone slab bridge (ishi-bashi / ishi-ita-bashi)**: one to three granite slabs (or a single board) across a street gutter, ditch, channel, narrow stream, garden stream or dry-garden bed; one in front of each town door over the gutter; channel versions come with stepping stones. Street/field/garden/river, common, small to medium. Hook: crossing; dressing. (BL: Civic, bridges) {seam S073: U Water: Bridges + W §4 + R §2 + U Gardens: Garden bridges + U Gardens: Dry garden + U Streets: Street surface}
- **Stone arch bridge (megane-bashi)**: true masonry arch; Nagasaki 1634. Canal, rare `[off-map: Kyushu]`. → BL Civic.
- **Five-arch bridge (Kintaikyō)**: Iwakuni's timber five-arch bridge, rebuilt 1674. Landmark `[off-map: Suō]`. → BL Civic.
- **Full-moon stone bridge (Engetsukyō)**: semicircular stone arch in the Koishikawa Kōrakuen, Edo, designed with the Ming scholar Zhu Shunshui (1660s–70s). Garden, landmark, medium. Hook: landmark.
- **Roofed corridor bridge (rōka-bashi)**: bridge with a roof and walls, linking castle enclosures or temple precincts (e.g. Tōfuku-ji's Tsūten-kyō, a roofed bridge over a maple ravine). Castle/temple, rare, medium. Hook: cover, chokepoint.
- **Zigzag plank bridge (yatsuhashi)**: boards laid in a zigzag across an iris bed or marsh, after the Ise monogatari poem. Garden, occasional, medium.
- **Drawbridge / lifting bridge (hane-bashi, hiki-bashi)**: castle bridge that can be raised or drawn back (verify how many existed in 1730). Castle, rare, medium. Hook: chokepoint.
- *Boat bridge (funa-bashi)* → S076, under W §4.
- **Long lake-outlet bridge (Seta no Karahashi)**: the long bridge at the Seta River on the Tōkaidō, a named scenic spot. River, landmark, large. Hook: chokepoint, landmark.
- **Kyoto's great bridges (Sanjō Ōhashi, Gojō Ōhashi)**: timber decks on stone piers (Sanjō from 1590) with bronze finials. River, landmark, large.
- **Osaka's public bridges (kōgi-bashi) vs town bridges (machi-bashi)**: about a dozen bridges were built and kept by the shogunate (Tenma-bashi, Tenjin-bashi, Naniwa-bashi); the rest (around 200) by the townsmen (verify counts). Canal, common (Osaka), medium to large.

### == U Water: Bridges: parts and fixtures ==

- **Bronze finial (giboshi)**: onion-shaped bronze cap on bridge railing posts; only on the most important bridges (Nihonbashi, Sanjō, Gojō) and at shrines. Canal, rare, small. Hook: landmark, loot-like shine. (BL: Civic)
- **Railing (kōran)**: post-and-rail parapet, sometimes with a top rail curved up at the ends. Canal, common, medium.
- **Bridge name post (hashi-bashira, hashi-mei)**: end post carved or plated with the bridge's name and date. Canal, common, small. Hook: navigation.
- **Bridge pier with cutwater (hashi-gui, kiri-mizu)**: timber piles braced with cross timbers, sometimes with a pointed debris guard upstream (assumed). River, common, medium. Hook: climb under, cover.
- **Stone bridge abutment (hashi-dai no ishigaki)**: dressed or dry-stone bridge ends on which the deck lands; in the wild they stand alone after a flood takes the deck. Canal/river, common (towns) / occasional (wild), medium. Hook: cover. {seam S077: U Water: Bridges + W §4}
- **Bridge-end plaza (hashi-zume, hashi-zume hirokōji)**: open space at the end of a big bridge with a notice board, tea stands, barbers' booths and palanquin stands. Street/canal, common at big bridges, `[terrain]`. Hook: gathering place.
- **Barber's booth at a bridge end (kamiyui-doko)**: barbers set up at bridge ends and were given bridge-watch duty (verify). Street, occasional, medium. → BL Services barber.
- **Bridge toll box (hashi-sen bako)**: toll box on a townsmen-run bridge; Eitai became a toll bridge in 1719. Canal, occasional, small. → BL Civic bridge-keeper's hut.
- **Bridge fire buckets and hooks (hashi no teoke)**: buckets kept on big bridges in case of fire (assumed from BL). Canal, occasional, small. Hook: water.
- **Flotsam boom (ikada-yoke)**: log chain upstream of a bridge to catch timber (assumed). River, rare, medium.

### == U Water: Canals, rivers, embankments and landings ==

- **Dug canal (horiwari, horikawa)**: straight cut channel between stone or timber walls, the streets of Osaka and eastern Edo. Canal, common (cities), `[terrain]`. Hook: water route, swimming.
- **Stone canal wall (ishigaki gomi, kishi no ishigaki)**: vertical or battered dressed-stone embankment. Canal, common, `[terrain]`. Hook: climb (hard), cover.
- **Timber-piled embankment (kui-dome, shigarami)**: posts driven in a row with wattle or boards behind, for cheaper banks (assumed). Canal, common, `[terrain]`.
- **Quay steps (gangi)**: stone steps down into the water for loading at any tide or river level. Canal, common, medium. Hook: water access, climb. → BL Civic "river quay with steps". (Note: "gangi" also names Echigo's covered snow arcades and castle-rampart stairs; see below.)
- **Named quay (kashi)**: a stretch of bank named for its trade: fish quay (uogashi), rice quay (komegashi), salt-fish quay, timber quay. Canal, common, `[terrain]`. Hook: loot spot (goods). → BL Civic.
- **Osaka riverside frontage (hama)**: the landing strip below each kura-yashiki and merchant house, with its own steps. Canal, common (Osaka), `[terrain]`.
- *Mooring post (funa-tsunagi-gui)* → S147, under U Water: Canals.
- **Mooring stone and post (funa-tsunagi-ishi / tomo-gui)**: stone with a drilled hole or carved knob, or a wooden stake, for tying boats at a canal edge or in a cove. Canal/coast, common (towns) / occasional (coves), small. Hook: navigation (a landing). {seam S147: U Water: Canals + W §19}
- **Boat turning basin (funairi)**: side basin off a canal where boats turn and load; Kyoto's Takase canal (1614) had several, e.g. Ichi-no-funairi. Canal, landmark, `[terrain]`. Hook: landmark.
- **Towpath (hikifune-michi)**: path along a canal or river where men hauled boats upstream (Takase canal boats were hauled back up by men). Canal, occasional, `[terrain]`.
- **Timber pond (kiba)**: water yards where logs floated in storage; Edo's lumber merchants moved to Fukagawa Kiba around 1701 (verify). Canal, landmark (Edo), `[terrain]`. Hook: walkable log rafts (risky).
- *Log raft (ikada)* → S109, under W §8.
- *River embankment with trees (tsutsumi)* → S006, under R §1.
- **Riverbed flats (kawara)**: dry gravel flats of a wide river (Kamo, Sumida mouths) used for shows, dyers' rinsing and summer evenings. Riverbed, common, `[terrain]`. Hook: open ground.
- **Summer riverbed platforms (noryō-yuka)**: benches and board platforms set out over the Kamo riverbed at Shijō for evening cool, with lanterns (Edo period, verify start). Riverbed, landmark (Kyoto, seasonal), medium. Hook: light, rest.
- *Canal sluice / water gate (suimon, hi)* → S156, under R §2.
- **Tide gate (shio-dome, shio-mon)**: gate keeping sea water out of a canal or letting it into a tidal garden pond (assumed). Canal, rare, medium.
- **Water-level post (mizu-bakari-gui)**: marked post in a river for flood watching (assumed). River, occasional, small.
- *Stone groyne (seigyū, jakago)* → S119, under W §12.
- *Canal-side warehouse row (kura-nami)*: plastered kura with doors to the water. → BL Civic.
- **Covered snow arcade (gangi, komise)**: the roofed walkway along house fronts in snow towns (Takada, Kuroishi). `[off-map: Echigo / Tsugaru]`

### == U Water: Boats moored in town (props) ==

- **Fast small boat (chokibune)**: long narrow boat rowed by one man; the Edo water taxi, e.g. to the Yoshiwara. Canal, common, medium. Hook: transport, cover.
- **Roofed pleasure boat (yanebune)**: boat with a light roof and blinds for parties. Canal, common, medium. Hook: cover.
- **Great pleasure barge (yakatabune)**: big house-boat with a solid cabin; the largest were restricted in the late 17th c. (verify). Canal, occasional, large. Hook: landmark, cover.
- **Takase canal boat (takasebune)**: flat shallow boat of Kyoto's Takase canal. Canal, common (Kyoto), medium.
- **Yodo river passenger boat (sanjikkoku-bune)**: 30-koku boat between Fushimi and Osaka. River, common, large. Hook: transport.
- **Food-seller boat (kurawanka-bune)**: small boat selling food and drink to Yodo passenger boats. River, occasional, medium. Hook: food.
- **Flat cargo boat (hiratabune, taka-se)**: broad flat lighter for bales and casks. Canal, common, medium. Hook: cover.
- **Lighter (tenmasen)**: small boat ferrying cargo from ships offshore to the quay. Canal/port, common, medium.
- *Water, nightsoil and rubbish boats*: see above.
- **Ferry boat (watashi-bune)**: flat ferry at a river crossing inside a town. River, occasional, medium. → BL Civic ferry landing.
- **Shogunal state barge (gozabune)**: huge decorated barge; Tenchi-maru (1630s) survived into the 18th c. (verify). Canal/bay, landmark, large.
- **Coastal cargo ship at anchor (higaki-kaisen, taru-kaisen)**: big one-masted ships anchored off the city. Port, occasional, large. → WC §2.6.
- *Boat awning and poles (tomo, sao)* → S164, under R §15.

### == U Water: Moats (town side) ==

- **Wet moat (mizubori)**: broad water-filled moat with stone or earth walls. Castle/town, common in castle towns, `[terrain]`. Hook: water, barrier.
- **Outer moat used as a canal (soto-bori)**: in Edo the outer moat doubled as a boat route (Kanda River cut, 1620). Canal, landmark, `[terrain]`.
- *Lotus in the moat (hori no hasu)* → S043, under N §M.
- *Moat-side horse-washing place (uma-arai-ba)* → S067, under W §3.
*Three kinds matter in 1730: the **stroll garden** (kaiyū-shiki) of daimyō estates and big temples, the **dry garden** (karesansui) of Zen temples, and the **tea garden** (roji). A fourth, the **courtyard garden** (tsubo-niwa) of a town house, is the one most players will see. The 1735 manual TSD (part 1) is squarely in our window and covers hills, stones, lanterns, fences and tea gardens; many fence and lantern *names* were codified later (TSD part 2, 1828), so treat named styles as "form existed, name may be later" unless marked.*

### == U Gardens: Stroll garden: water, land forms, islands ==

- **Garden pond (ike)**: irregular pond with bays and points, the centre of a stroll garden. Garden, occasional (estates, temples), `[terrain]`. Hook: water, landmark.
- **Crane island and turtle island (tsuru-jima, kame-jima)**: paired islands for long life; the turtle has a head stone and flipper stones, the crane a tall "wing" stone and a pine. Garden, occasional, medium. Hook: landmark, reachable by bridge.
- **Island of the immortals (Hōrai-jima, Hōrai-san)**: an unreachable rock island in the pond. Garden, occasional, medium.
- **Middle island (naka-jima)**: plain island joined by bridges. Garden, occasional, medium.
- **Artificial hill (tsukiyama)**: raised mound with stones and clipped shrubs; the subject of TSD 1735. Garden, occasional, `[terrain]`. Hook: elevation, sightline.
- **Miniature Mount Fuji (Fuji-yama, tsukiyama)**: a cone-shaped turfed hill modelled on Fuji (Suizen-ji, Kumamoto; in Edo estates too, verify). Garden, rare, `[terrain]`. Hook: landmark.
- **Pebble beach (suhama)**: gently sloping beach of flat rounded stones into the pond, sometimes ending in a lantern on a point (Katsura). Garden, occasional, `[terrain]`.
- **Rocky shore (ariso)**: rough rocks set along a pond edge to suggest a sea coast. Garden, occasional, medium.
- **Pond edge of piles (kui-gakoi)**: wooden posts lining a pond bank (assumed). Garden, occasional, `[terrain]`.
- **Meandering stream (yarimizu)**: shallow stream winding over pebbles into the pond. Garden, occasional, `[terrain]`. Hook: water.
- **Spring (izumi)**: stone-lined spring feeding the pond. Garden, occasional, small.
- **Waterfall (taki)**: a set of stones with water falling; named styles by how the water falls (cloth fall, thread fall, stepped fall) (form named in older manuals; verify TSD). Garden, occasional, medium. Hook: noise masks footsteps (gameplay licence).
- **Stone island in a pond (ishi-jima)**: a single rock breaking the water. Garden, common in gardens, small.
- **Tidal pond (shio-iri no ike)**: pond fed by sea water through a sluice so its level follows the tide: Hama-goten (from 1654, shogunal from 1709) and Rakuju-en (1678) in Edo. Garden, landmark, `[terrain]`. Hook: changing water level.
- **Garden paddy and tea field (niwa no ta, chabatake)**: small working rice field and tea bushes inside a daimyō garden (Okayama Kōrakuen, finished 1700). Garden, rare, `[terrain]`.
- *Plum grove (baien) and cherry and maple slopes* → S013, under N §D.
- **Iris bed (shōbu-da)**: marsh bed of irises, crossed by a zigzag bridge. Garden, occasional, `[terrain]`. (Famous Horikiri iris garden is later.)
- *Lotus pond (hasu-ike)* → S043, under N §M.
- **West-Lake causeway (Seiko no tsutsumi)**: a narrow causeway modelled on Hangzhou's West Lake (Koishikawa Kōrakuen). Garden, rare, `[terrain]`.
- **Moon-viewing platform (tsukimi-dai)**: bamboo or board platform at the pond edge (Katsura's is on the veranda). Garden, rare, medium. Hook: sightline.
- **Borrowed scenery (shakkei)**: design idea, not an object: a garden framed to show a distant mountain or pagoda. Garden, `[terrain]` note. Hook: placement advice for landmarks.
- **Garden boat landing (funatsuki)**: stone steps and a mooring post for pleasure boats on a large pond. Garden, rare, medium.
- **Open rain shelter and arbour (azumaya / amayadori / chin)**: thatched or small roof on four posts, benches, no walls: at a pass, crossing or viewpoint, and in gardens. Roadside/mountain/garden, occasional, medium. Hook: SHELTER (rain only), rest, shade. (roadside form assumed; with a hearth it becomes a BL tea-stall shell; with rooms, BL) {seam S217: U Gardens: Stroll garden + W §3}
- **Wisteria trellis (fuji-dana)**: bamboo or timber trellis roof carrying wisteria; Kameido Tenjin's (1660s) was famous. Garden/shrine, occasional, medium. Hook: shade.
- **Garden archery range (niwa no yaba)**: a straight lane and butt inside a daimyō garden (assumed). Garden, rare, medium.

### == U Gardens: Dry garden (karesansui) and set stones ==

- **Raked gravel field (shira-kawa-suna)**: crushed white granite gravel (Shirakawa sand) raked into patterns, representing water. Temple garden, occasional, `[terrain]`. Hook: footprints show.
- **Rake patterns (samon)**: straight lines, ripples round stones, waves; named pattern sets are modern codifications (verify which were used in 1730). Temple garden, occasional, `[terrain]` decal.
- **Wooden gravel rake (samon-kaki)**: wooden rake with broad teeth. Temple garden, occasional, small. Hook: loot (tool).
- **Stone group of three (sanzon-seki)**: tall central stone with two flanking, echoing a Buddha triad. Garden, common in gardens, medium. Hook: cover.
- **Dry waterfall (kare-taki)**: stones set as a waterfall with no water, gravel as the pool. Temple garden, occasional, medium.
- **Dry pond and dry stream (kare-ike, kare-nagare)**: gravel or pebbles laid as a pond or stream bed. Garden, occasional, `[terrain]`.
- *Stone bridge in a dry garden* → S073, under U Water: Bridges.
- **Ryōan-ji type stone garden**: 15 stones in five groups on raked gravel within a tile-capped earthen wall. Temple garden, landmark (Kyoto), large. (Date of the layout is debated; it existed by the 17th c. and appears in the 1799 guide.) Hook: landmark.
- **Daisen-in type narrative garden**: tight stones-and-gravel "river" with a stone boat. Temple garden, landmark, medium.
- **Sand platform and sand cone (ginshadan, kōgetsudai)**: flat-topped sand terrace and truncated sand cone at Ginkaku-ji (date of the present forms is uncertain, verify; possibly Edo). Temple garden, landmark, medium.
- **Sacred sand cones (tatezuna)**: two cones of sand before the Hosodono at Kamigamo Shrine. Shrine forecourt, landmark, small.
- **Great clipped hedge-hills (ō-karikomi)**: massed azaleas clipped into rolling hills, standing for mountains or waves (Daichi-ji, Shisendō). Garden, occasional, medium.
- *Moss ground (koke-niwa)*: moss as the ground cover. → nature flavour.
- **Edging of set stones and tiles (kiri-ishi, kawara-dome)**: edge between gravel and moss or veranda drip line. Garden, common in gardens, small.
- **Eave drip-line gravel strip (amaochi)**: strip of pebbles under the eaves to catch roof water (assumed). Garden, common, `[terrain]`.
- *Garden wall behind the gravel (hei, tsuiji)*: tile-capped earthen wall (see Castle / walls and WC §2.8).

### == U Gardens: Paths and stepping stones ==

- **Stepping stones (tobi-ishi)**: flat-topped stones set a stride apart through moss or gravel; laid out in named rhythms (twos-and-threes, "wild geese") in the manuals. Garden, common in gardens, small.
- **Stone strip pavement (nobedan)**: rectangular pavement of cut stone, pebbles, or a mix (formal / semi / informal). Garden, occasional, medium.
- **Paved path (shiki-ishi)**: set flat stones forming a path. Garden/temple, common, `[terrain]`.
- **Shoe-removing stone (kutsunugi-ishi)**: big flat stone at the foot of the veranda where footwear is left. Garden, common, small. Hook: loot spot (sandals).
- *Stepping stones across water (sawatari)* → S072, under W §4.
- **Barrier stone (sekimori-ishi, tome-ishi)**: fist-sized stone tied in a cross of black rope, set on a path to say "do not pass". Garden, common in tea gardens, small. Hook: path blocker signal.
- **Stone steps in a garden (ishidan)**: rough steps up an artificial hill. Garden, occasional, medium.
- **Garden gravel path (jari-michi)**: raked or plain gravel path. Garden, common, `[terrain]`.

### == U Gardens: Tea garden (roji) ==

- **Outer and inner tea garden (soto-roji, uchi-roji)**: two walled or fenced zones leading to a tea house. Garden, occasional, `[terrain]` set.
- **Waiting arbour (koshikake-machiai)**: small roofed bench where guests wait, open at the front. Garden, occasional, medium. Hook: rest, cover.
- **Middle gate (naka-kuguri, chūmon)**: small gate between the outer and inner roji, through which guests stoop. Garden, occasional, medium. Hook: chokepoint.
- **Braided-hat gate (amigasa-mon)**: small gate with a roof shaped like a woven hat (verify date). Garden, rare, medium.
- *Swing gate of brushwood (shiori-do)* → S174, under R §8.
- **Lift-up gate (agesu-do)**: bamboo door propped up on a pole (assumed period form). Garden, occasional, medium.
- **Stone water basin set (tsukubai)**: low basin with a front stone for kneeling (mae-ishi), a stone for the hot-water bucket (yuoke-ishi) and one for the hand lantern (teshoku-ishi), around a pebbled drain (umi). Garden, occasional, small. Hook: water.
- **Dust pit (chiri-ana)**: small pit edged with stones where leaves are swept, with a pair of chopsticks and a leaf beside it. Garden, occasional, small.
- **Ornamental privy (kazari-setchin)**: tiny unused privy with a stone floor, kept for inspection; its use counterpart (kafuku setchin) is in the outer roji. Garden, occasional, medium. → BL if treated as a hut.
- **Sword rack outside a tea room (katana-kake)**: shelf under the eave where samurai left swords before entering. Garden, occasional, small. Hook: weapon loot spot (gameplay licence).
- *Crawl-in door (nijiriguchi)*: → BL (tea house building).
- **Pine-needle spread (shiki-matsuba)**: dry pine needles laid on moss in winter to protect it (verify date). Garden, occasional (seasonal), `[terrain]` decal.
- **Roji sandals (roji-geta, roji-zōri)**: set out on the stepping stones for guests. Garden, occasional, small.
- *Hand lantern stand*: see Lanterns below.

### == U Gardens: Stone lanterns by type ==

*All stone; bronze and wood are in the religious group. TSD 1735 illustrates "rare early stone lanterns". Kasuga-type standing lanterns dominate shrines; low and sunk-post types dominate gardens.*
- **Kasuga lantern (kasuga-dōrō)**: tall six-sided lantern on a post and base, deer and mountains carved on the fire box; named for Kasuga Taisha. Shrine/temple/garden, common, medium. Hook: landmark, low cover, light (if lit).
- **Snow-viewing lantern (yukimi-dōrō)**: low lantern with a very broad roof on three or four curved legs, set by water; oldest survivors at Katsura, early 17th c. Garden, common in gardens, small to medium.
- **Round-roof snow-viewing lantern (maru-yukimi)**: yukimi with a round roof. Garden, occasional, small.
- **Koto-bridge lantern (kotoji-dōrō)**: yukimi variant with two unequal legs, one standing in the water, like a koto bridge (Kenroku-en is the famous one, off-map; verify date). Garden, rare, small.
- **Sunk-post lantern (ikekomi-dōrō)**: post sunk directly in the ground with no base. Garden, common in tea gardens, small.
- **Oribe lantern (oribe-dōrō)**: ikekomi lantern with a square fire box and a figure carved at the foot of the post, credited to Furuta Oribe (d. 1615); the "Christian lantern" reading of the figure is disputed. Garden, common in tea gardens, small.
- **Cape lantern (misaki-dōrō)**: small low lantern set on a point jutting into a pond. Garden, occasional, small.
- **Placed lantern (oki-dōrō)**: small lantern with no post, simply set on a stone. Garden/courtyard, common, small.
- **Leaning lantern over water (rankei-dōrō)**: lantern on a bent arm leaning over a pond (verify date). Garden, rare, small.
- **Wet-heron lantern (nuresagi-dōrō)**: slender plain lantern (verify form and date). Garden, rare, small.
- **Six- and eight-sided temple lanterns (rokkaku, hakkaku; Taima-dera, Tōdai-ji types)**: old standing forms copied in Edo. Temple forecourt/garden, occasional, medium.
- **Square standing lantern (kaku-dōrō, tachi-dōrō)**: square-section standing lantern (assumed common Edo donation form). Shrine/temple, common, medium.
- **Natural-stone lantern (yama-dōrō)**: built of rough unworked stones stacked as a lantern (verify date). Garden, occasional, small.
- **Stone lantern parts reused (mitate)**: an old pagoda base or lantern roof reused as a basin or stepping stone; favoured by tea masters. Garden, occasional, small.

### == U Gardens: Basins, spouts and water devices ==

- **Tall hand basin by a veranda (en-saki chōzubachi)**: tall stone basin set at veranda height so it can be reached without stepping down. Garden, common in gardens, small. Hook: water.
- **Jujube-shaped basin (natsume-gata chōzubachi)**: rounded basin shaped like a jujube fruit. Garden, occasional, small.
- **Coin-shaped basin (zeni-gata)**: round basin with a square hole, the Ryōan-ji "I only know contentment" type (verify date). Garden, rare, small.
- **Boat-shaped or natural-stone basin (fune-gata, shizen-seki)**: hollowed natural boulder. Garden, occasional, small.
- **Basin made from a pagoda part (tōba-gata)**: reused stone stupa or lantern piece. Garden, occasional, small.
- *Bamboo spout (kakei)* → S068, under R §2.
- *Deer scarer (shishi-odoshi, sōzu)* → S215, under R §5.
- **Water harp (sui-kinkutsu)**: upturned jar buried under a basin drain so drips ring. `[outside 1680-1750: popular Meiji; Edo origin claimed]` (verify)
- **Garden well (niwa-ido)**: well with a frame of stone or bamboo, used in tea gardens for fresh water. Garden, occasional, small. Hook: water.
- **Hot-water bucket (yuoke)**: wooden bucket on the yuoke stone in winter tea gatherings. Garden, rare, small.
- **Ladle (hishaku)**: bamboo ladle laid on a basin. Garden/shrine, common, small.

### == U Gardens: Garden bridges ==

- *Garden drum bridge (taiko-bashi)*: high semicircular wooden bridge; see Bridges.
- *Garden earth bridge (dobashi)* → S075, under U Water: Bridges.
- *Single slab bridge (ishi-bashi)* → S073, under U Water: Bridges.
- **Natural-stone bridge (shizen-seki bashi)**: an unworked long stone across a stream. Garden, occasional, small.
- *Zigzag plank bridge (yatsuhashi)*: see Bridges.
- *Full-moon bridge (Engetsukyō)*: see Bridges.
- *Plank bridge with rails (ita-bashi)* → S074, under U Water: Bridges.
- **Wisteria bridge (fuji-bashi)**: bridge under a wisteria trellis (assumed; Kameido-like). Garden/shrine, rare, medium.

### == U Gardens: Fences, hedges and garden gates ==

*Bamboo fences fall into see-through fences (sukashi-gaki) and screens (shahei-gaki). The named "temple" styles take their names from where a notable example stood; the name is often later than the form (verify each).*
- **Open bamboo grid fence (yotsume-gaki)**: bamboo posts and horizontal rails tied with black palm rope, see-through; the commonest divider. Yard/garden/street, common, medium linear. Hook: see-through, a low barrier that blocks movement. {seam S165: U Gardens: Fences + R §8}
- **Kenninji fence (kenninji-gaki)**: solid screen of vertical split bamboo held by horizontal battens; better houses, temples, gardens. Yard/garden/street, occasional (villages) / common (towns), medium linear. Hook: sight cover. {seam S166: U Gardens: Fences + R §8}
- **Bamboo-branch fence (takeho-gaki)**: screen of bundled bamboo twigs. Garden, occasional, medium. Hook: sight cover.
- **Katsura fence (katsura-gaki)**: bamboo-branch fence with living bamboo bent into it, along the Katsura villa road (early 17th c.). Garden/street, landmark, medium.
- **Kōetsu-ji fence (kōetsu-gaki)**: low curving fence of diagonal split bamboo, after Hon'ami Kōetsu's village (early 17th c.; verify name date). Garden, occasional, medium.
- **Ginkaku-ji fence (ginkakuji-gaki)**: low bamboo fence on a stone base along the Ginkaku-ji approach (verify date). Temple, rare, medium.
- **Kinkaku-ji fence (kinkakuji-gaki)**: low see-through fence of vertical bamboo with a split-bamboo top (verify date). Garden, occasional, small.
- **Ryōan-ji fence (ryōanji-gaki)**: low lattice of diagonal bamboo (verify; possibly Meiji name). Garden, rare, small.
- **Ōtsu fence (ōtsu-gaki)**: woven fence of split bamboo passed in and out of horizontals (verify date). Garden, occasional, medium.
- **Gun-barrel fence (teppō-gaki)**: thick bamboo poles set alternately on either side of a rail (verify date). Garden, occasional, medium.
- **Blind fence (misu-gaki)**: thin horizontal bamboo slats between posts, like a blind (verify date). Garden, occasional, medium.
- **Daitoku-ji fence (daitokuji-gaki)**: bamboo-branch fence (verify date). Temple, rare, medium.
- **Straw-coat fence (mino-gaki)**: branches hung downward like a straw raincoat (verify date). Garden, rare, medium.
- **Sleeve fence (sode-gaki)**: short decorative panel beside a gate, house corner or building, screening a view. Yard/garden/street, rare in villages (better houses) / common in towns, small–medium. Hook: small sight cover. {seam S170: U Gardens: Fences + R §8}
- *Brushwood fence (shiba-gaki)* → S167, under R §8.
- *Reed fence (yoshi-gaki)* → S168, under R §8.
- **Bush-clover fence (hagi-gaki)**: bush-clover stems bundled (verify date). Garden, occasional, medium.
- **Cypress lattice fence (higaki)**: woven cypress board strips. Garden/shrine, occasional, medium.
- *Hedge (ikegaki)* → S169, under R §8.
- **Board fence (itabei)**: plain or black-tarred boards on posts; headmen's houses, post-town edges, towns. Street/garden/yard, common (towns) / occasional (villages), medium linear. Hook: cover. Black official version: U (Fences). {seam S171: U Gardens: Fences + R §8}
- **Black-painted board fence (kuro-itabei)**: black fence of official and samurai houses. Samurai quarter, common, medium.
- **Capped earth wall (tsuiji-bei / dobei)**: rammed-earth wall, plastered, with a tile (or thatch) cap; temples, palaces, estates and village headmen. Street/temple/yard, common (towns) / rare in villages, large linear. Hook: hard cover, climb. {seam S172: U Gardens: Fences + R §8}
- **Tile-course wall (neri-bei)**: wall of mud and roof tiles in layers. Temple/street, occasional, large.
- **Striped earthen wall (suji-bei)**: earthen wall with five white lines, showing an imperial-linked temple rank. Temple, rare, large. Hook: landmark.
- **Stone-based earthen wall**: earthen wall on a dressed-stone footing (assumed). Samurai quarter, common, large.
- **Garden gate, roofed (niwa-mon)**: small roofed gate into a garden from the house yard. Garden, occasional, medium. Hook: door.
- **Brushwood gate (shiba-do)**: rustic gate. Garden, occasional, medium.
- *Wattle gate (kido, garden sense)* → S174, under R §8.

### == U Gardens: Planting craft and tree supports ==

- **Clipped shrubs (karikomi)**: azaleas and boxwood clipped into rounded forms. Garden, common in gardens, small to medium. Hook: low cover.
- **Clipped balls (tamamono)**: single spherical shrubs. Garden, common, small.
- **Box hedge (hako-gaki)**: square-clipped hedge. Garden/street, occasional, medium.
- **Gate-covering pine (monkaburi no matsu)**: pine trained to reach over a gate. Street/samurai quarter, occasional, medium (tree). → nature flavour for the tree; the training here.
- **Trained garden pine (niwaki matsu)**: pine shaped by years of needle-plucking and branch-bending into layered clouds. Garden, common in gardens, medium.
- **Crutch supports (sasae, shichū)**: timber or bamboo props under a long pine limb, often over water. Garden, occasional, small.
- **Branch ties and guide poles (take no shichū)**: bamboo splints and cords training branches. Garden, occasional, small.
- **Snow-rope cones (yukitsuri)**: ropes from a central pole to each branch. `[outside 1680-1750: ornamental garden form Meiji]`; the Edo form was farm fruit-tree propping. Garden, rare in window.
- **Straw snow shelters (yuki-gakoi)**: straw and bamboo tents over shrubs in snow country (verify date). Garden, occasional (snow maps), small.
- **Straw trunk wraps against insects (komo-maki)**: straw band round a pine trunk in autumn, burned in spring (verify date). Garden/street, occasional, small.
- **Cycad winter wraps (sotetsu no wara-maki)**: straw hoods on cycads in winter (assumed; cycads were fashionable in temple and daimyō gardens). Garden, rare, small.
- *Bamboo grove with a fence (takeyabu)*: bamboo planted and fenced. → nature flavour.
- **Pot plants on stands (hachiue, bonsai-dana)**: potted dwarf trees and flowers on shelves; the Genroku-era gardening craze. Street/garden, common, small.
- *Nursery rows (ueki-ya)*: nursery gardens in Edo's suburbs (Somei). → rural flavour.

### == U Gardens: Garden fauna and small living features ==

- **Plain carp and crucian carp (magoi, funa)**: dark grey-black food carp in garden ponds, moats, lakes, paddies and slow rivers. Pond/river, common, small (animated). Hook: food. Coloured koi are `[outside 1680-1750: 1804–1830]` (§6). {seam S055: U Gardens: Garden fauna and small living features + N §Fauna}
- **Coloured patterned koi (nishikigoi)**: `[outside 1680-1750: Bunka–Bunsei, 1804–1830]` Do not use.
- **Goldfish (kingyo)**: introduced 1502 from China; a luxury in early Edo, a commoner hobby spreading in the 18th c.; Yamato-Kōriyama breeding from about 1724 (verify). Kept in tubs and ceramic basins, not glass bowls. Street/garden, occasional, small.
- **Goldfish tub (kingyo-oke) or basin (kingyo-bachi)**: shallow wooden tub or glazed basin. Street/garden, occasional, small. Hook: water.
- **Glass goldfish bowl (kingyo-dama)**: `[outside 1680-1750: 19th c.]` (verify)
- **Turtles in temple ponds (kame)**: pond turtles, often released as an act of merit. Temple/garden, common, small (animated).
- **Release pond (hōjō-ike)**: temple pond where fish and turtles are released at the hōjō-e rite. Temple forecourt, occasional, `[terrain]`. Hook: water.
- **Cranes kept in a garden (tsuru)**: cranes kept in daimyō gardens (Okayama Kōrakuen, verify date). Garden, rare, medium (animal).
- **Temple pigeons and feed sellers (hato, mame-uri)**: pigeons at big temples like Sensō-ji, with sellers of beans for them (verify date). Temple forecourt, occasional, small.
- *Temple deer (Nara)*: → nature flavour.

### == U Gardens: Courtyard and small town gardens ==

- **Courtyard garden (tsubo-niwa)**: tiny garden inside a town house plot, open to the sky: a stone lantern, a basin, a few stones and shrubs. Garden (inside a house plot), common in merchant houses, medium. Hook: light well, climb.
- **Front plantings (senzai)**: a planted bed seen from a room. Garden, common, `[terrain]`.
- **Back yard (ura-niwa) of a machiya**: work yard with a well, a kura door, a toilet and a small garden. Garden, common, `[terrain]`. → BL Dwellings for its huts.
- *Small house shrine in the yard (yashiki-gami)*: → BL Shinto.

### == U Gardens: Named landmark gardens in or near the window ==

*Pointers for hero sites. All existed in 1730 unless tagged.*
- **Koishikawa Kōrakuen (Edo)**: Mito Tokugawa estate garden, begun 1629, finished by Mitsukuni; Chinese touches (Engetsukyō, West-Lake causeway). Garden, landmark, `[terrain]` set.
- **Rikugien (Edo)**: Yanagisawa Yoshiyasu's stroll garden of 88 poetic scenes, 1702. Garden, landmark.
- **Hama-goten (Edo)**: tidal-pond garden from 1654, shogunal from 1709. Garden, landmark.
- **Rakuju-en / Shiba (Edo)**: Ōkubo Tadatomo's garden, 1678, tidal pond. Garden, landmark.
- **Okayama Kōrakuen**: Ikeda Tsunamasa, 1687–1700; lawns, paddy, tea field, pond, island. Garden, landmark `[off-map: Bizen]` unless the map reaches west.
- **Genkyū-en (Hikone)**: 1677, near the Nakasendō. Garden, landmark.
- **Katsura villa (Kyoto)**: early 17th c.; lanterns, pebble beach, fences. Garden, landmark.
- **Shugaku-in (Kyoto)**: 1655–59; huge borrowed-scenery garden with rice terraces. Garden, landmark.
- **Shisendō (Kyoto)**: 1641; clipped azaleas, gravel, the first garden sōzu. Garden, landmark.
- **Konchi-in (Kyoto)**: 1630s, crane-and-turtle dry garden (Kobori Enshū). Garden, landmark.
- **Ryōan-ji, Daisen-in, Ginkaku-ji, Kinkaku-ji, Tenryū-ji, Saihō-ji (Kyoto)**: medieval temple gardens still kept. Garden, landmark.
- **Kenroku-en**: Kanazawa, from 1676 (name 1822). `[off-map: Kaga]`
- **Ritsurin**: Takamatsu, completed about 1745. `[off-map: Sanuki]`
- **Suizen-ji Jōju-en**: Kumamoto, from 1636. `[off-map: Higo]`
- **Shukkei-en**: Hiroshima, 1620. `[off-map: Aki]`
- **Daimyō estate garden (generic)**: Edo had hundreds of daimyō residences, most with a stroll garden. Garden, occasional (Edo), `[terrain]` set. Hook: walled private ground.
*In 1730 shrines and temples were mixed (shinbutsu shūgō): many shrines had a pagoda or a Buddhist hall, and many temples had a shrine. Forecourt kit crosses freely between the two. Halls and gates are in BL; this is what stands in the open.*

### == U Religious: Torii by style ==

- **Shinmei torii**: straight lintel, straight posts, no tie-beam overhang; the Ise style, often plain wood. Shrine forecourt, common, large. Hook: landmark.
- **Black-log torii (kuroki torii)**: shinmei form in unbarked logs (Nonomiya). Shrine forecourt, rare, large.
- **Kashima torii**: straight lintel with the tie-beam passing through the posts. Shrine forecourt, common, large.
- **Myōjin torii**: upswept top lintel over a straight one, tie-beam with a central strut; the commonest form. Shrine forecourt, common, large. Hook: landmark.
- **Inari torii**: myōjin form with a ring (daiwa) where lintel meets post; vermilion. Shrine forecourt, common (Inari shrines are everywhere), large.
- **Rows of donated torii (senbon torii)**: tunnels of small vermilion torii (Fushimi Inari). Shrine forecourt, landmark. (The dense tunnel form is mostly later; donation of torii was growing in the Edo period; verify for 1730.)
- **Hachiman torii**: myōjin form with slanted lintel ends. Shrine forecourt, occasional, large.
- **Kasuga torii**: straight-cut lintel ends, vermilion (Kasuga Taisha). Shrine forecourt, occasional, large.
- **Sannō torii**: myōjin form with a triangular gable on top (Hie shrines). Shrine forecourt, occasional, large.
- **Four-legged torii (ryōbu torii, yotsuashi)**: each post braced front and back by small posts (Itsukushima, Kehi). Shrine forecourt, occasional, large.
- **Triple torii (mitsu-torii, Miwa torii)**: three torii joined side by side with a fence (Ōmiwa). Shrine forecourt, rare, large.
- **Three-legged torii (mihashira torii)**: three torii in a triangle (Kaiko-no-yashiro, Kyoto). Shrine, rare, medium. `[outside 1680-1750: present form 1831]` (verify)
- **Stone torii (ishi-torii)**: granite torii, usually myōjin form, donated by villagers or pilgrimage groups with names on the post; stone torii go back to the 12th c. and many village ones bear 17th–18th-c. dates. Shrine, common (towns) / occasional (villages), medium–large. Hook: landmark. (verify village frequency with dated examples) {seam S181: U Religious: Torii by style + R §10}
- **Bronze torii (karakane torii)**: cast-bronze torii at great sites (Nikkō Tōshōgū, 1636). Shrine forecourt, landmark, large.
- **Vermilion wooden torii (nuri torii)**: painted vermilion, black on the top beams; Inari and Hachiman shrines. Shrine, common (towns) / occasional (villages), medium–large. Hook: landmark. {seam S182: U Religious: Torii by style + R §10}
- *Sea torii (umi no ōtorii)* → S153, under W §20.
- **Torii plaque (gakuzuka)**: name tablet between the lintels. Shrine forecourt, common, small.

### == U Religious: Shrine forecourt ==

- **Shrine approach (sandō)**: earth, gravel or stone path from the torii to the hall, often lined with cedars. Shrine, common, `[terrain]`. Hook: path. Stone-paved big-temple approach: U (Streets). {seam S183: U Religious: Shrine forecourt + R §10}
- *Stone steps up to the shrine (ishidan)* → S060, under W §2.
- **Guardian lion-dogs (komainu)**: pair of stone lion-dogs flanking the approach, one mouth open, one shut; the outdoor standing-pair placement begins in the Edo period. Frequency disputed (§3.3): R says many villages had none in 1730 (occasional); U says common (towns). Shrine, small–medium. Hook: landmark, low cover. (verify frequency in 1730) {seam S184: U Religious: Shrine forecourt + R §10}
- **Fox guardians (kitsune)**: stone foxes with a key or a jewel in the mouth at Inari shrines. Shrine forecourt, common (Inari), small.
- **Other messenger statues (tsukai)**: stone monkeys (Hie), bulls (Tenjin, verify date for stroking bulls), wolves (Mitsumine, rural) (verify). Shrine forecourt, occasional, small.
- **Purification basin (chōzubachi)**: stone ablution basin with a ladle, often dated and donated; many village shrines had no roof over it, and some used a stream. Shrine forecourt, common, small–medium. Hook: WATER (clean). (BL: temizuya for the roofed pavilion) {seam S185: U Religious: Shrine forecourt + R §10}
- **Sacred rope (shimenawa) and paper streamers (shide)**: straw rope on a torii, a sacred tree or rock. Shrine forecourt, common, small.
- *Sacred tree with a fence (goshinboku)* → S052, under W §7.
- *Sacred rock (iwakura)* → S051, under W §7.
- **Offering box (saisen-bako)**: slatted wooden box before a shrine or temple hall; first recorded 1540 at Tsurugaoka Hachimangū and spread in the Edo period; country shrines long kept offerings of rice wrapped in paper (o-hineri) instead. Shrine/temple forecourt, common in towns / rare in villages, small. Hook: lore; coins may lie by it (gameplay licence), never a loot container. {seam S186: U Religious: Shrine forecourt + U Religious: Temple forecourt + R §10}
- **Hall bell or gong with rope (suzu / waniguchi)**: a big bell, or a flat bronze "crocodile-mouth" gong, hung over the front of a shrine or temple hall and rung with a thick cloth rope. Shrine/temple forecourt, common, small. Hook: noise. {seam S187: U Religious: Shrine forecourt + R §10 + U Religious: Temple forecourt}
- **Votive plaque rack (ema-kake)**: rail or frame where small wooden votive plaques hang. Shrine forecourt, common (towns) / occasional (villages), small–medium. (BL: ema-dō for the big picture-plaque hall) {seam S188: U Religious: Shrine forecourt + R §10}
- **Fortune slips and lot box (omikuji / mikuji-bako)**: hexagonal box shaken to drop a numbered stick; slips given out. Shrine/temple forecourt, occasional, small. Tying slips to branches or lines is probably later, likely `[outside 1680-1750]` (verify). {seam S190: U Religious: Shrine forecourt + R §10}
- *Stone lanterns on the approach (kennō-tōrō)* → S100, under R §10.
- **Lantern avenue (tōrō no namiki)**: the great massed lanterns: Kasuga Taisha (about 2,000 stone and 1,000 hanging), Nikkō Tōshōgū (daimyō gifts). Shrine forecourt, landmark, `[terrain]` set. Hook: landmark, cover field.
- *Donated paper lantern frames (kennō-chōchin dana)* → S207, under R §14.
- **Donated banners (hōnō nobori)**: rows of banners with donors' names, especially red at Inari (verify how dense in 1730). Shrine forecourt, occasional, small.
- **Donor-named stone fence and shrine-name pillar (hōnō tamagaki / shagō-hyō)**: stone fence round a shrine carved with donors' names and sums, and a tall stone pillar naming the shrine. U: fence occasional (verify date); R: both `[outside 1680-1750: mostly Meiji+]` (verify). Shrine forecourt, medium. Suggested reading: rare / late until checked. {seam S191: U Religious: Shrine forecourt + R §17 + R §10}
- *Hundred-times stone (hyakudo-ishi)* → S189, under R §10.
- **Stone horse or bronze horse (shinme-zō)**: statue of the sacred horse (the live horse stable → BL). Shrine forecourt, occasional, medium.
- *Portable shrine (mikoshi)* → S203, under U Festivals: Festival sets and seasonal dressing.
- **Summer purification ring (chinowa)**: large ring of reeds under which people pass on the last day of the 6th month. Shrine forecourt, seasonal, medium.
- *Sumo ring (dohyō)*: → BL Shinto.
- *Kagura or Noh stage*: → BL Shinto.
- *Donated sake casks display (kazari-daru)* → S213, under R §14.
- **Pilgrim name slips on gates (senja-fuda)**: `[outside 1680-1750: craze late 18th c.]` (verify)
- **Fuji mound (Fuji-zuka)**: miniature climbable Mount Fuji at a shrine. `[outside 1680-1750: first 1780, Takata]` (verify)

### == U Religious: Temple forecourt ==

- *Big gates (sanmon, niōmon, sōmon)*: → BL Buddhist. Outdoor note: guardian kings are inside the niōmon; straw sandals hung on them by pilgrims (verify).
- **Great incense burner (jōkōro)**: large bronze incense burner on legs before the main hall, smoke fanned over the body. Temple forecourt, common at big temples, medium. Hook: smoke, landmark.
- **Standing bronze lanterns (kane-dōrō)**: rows of bronze lanterns donated by daimyō at shogunal mausolea: Zōjō-ji and Kan'ei-ji received ranks of them at the funerals of Ietsuna (1680), Tsunayoshi (1709), Ienobu (1712) and Ietsugu (1716). Temple forecourt, landmark, medium each. Hook: cover field, landmark.
- *Hanging bronze lanterns (tsuri-dōrō)*: hung under temple eaves. → BL (building attachment); listed for the forecourt look.
- *Gong with rope (waniguchi, zen no tsuna)* → S187, under U Religious: Shrine forecourt.
- *Offering box (saisen-bako)* → S186, under U Religious: Shrine forecourt.
- **Big Buddha in the open (roza no daibutsu)**: Kamakura's bronze Amida, in the open since the hall was lost (1498). Temple, landmark (near Edo), large. Hook: landmark.
- **Six Jizō of Edo (Edo roku Jizō)**: six seated bronze Jizō about 2.7 m high, cast 1708–1720 by the priest Jizōbō Shōgen and set at the six highway entrances to Edo (Shinagawa, Yotsuya/Shinjuku, Sugamo, Fukagawa, Eitai-ji, Senju area). Street/temple, landmark, large. Hook: landmark, in window. (verify each site)
- **Six-Jizō row (roku Jizō)**: six small stone Jizō in a row, one per realm of rebirth, at a graveyard gate, village edge or crossroads. Graveyard/roadside, common (graveyards) / occasional (roads), small–medium. Hook: landmark; a tell that a village or graveyard is near. (BL: Buddhist props) {seam S080: U Religious: Temple forecourt + W §5 + R §11}
- **Stone Buddha rows (sekibutsu)**: rows of small stone Jizō, Kannon or arhats along a wall. Temple forecourt, occasional, medium.
- *Prohibition stele at the gate (kaidan-seki)*: see Notices.
- **Stone pagoda (sekitō, jūsan-jū-no-tō)**: stone stupa of 5, 9 or 13 roofs. Temple/garden, occasional, medium. Hook: landmark.
- *Treasure-seal pagoda (hōkyōin-tō)* → S092, under W §5.
- *Sutra mound (kyō-zuka)* → S093, under W §5.
- *Stroking statue (nade-botoke, Binzuru)*: wooden Binzuru on the hall veranda, rubbed for healing. → BL (on the building).
- **Temple approach shops (nakamise)**: rows of small shops lining a temple approach; at Sensō-ji locals were allowed stalls in return for cleaning duty in the Genroku–Kyōhō years (verify). Temple forecourt, landmark (Asakusa), medium each. Hook: loot spots. → BL Shops for the booths.
- *Pine or cedar avenue (namiki)*: trees lining a long temple approach. → nature flavour.
- *Stone bridge over a temple pond (ishi-bashi)*: see Bridges.
- *Benten island shrine*: → BL Buddhist.
- *Bell and bell tower (bonshō, shōrō)*: → BL Buddhist; time bells → BL Civic.
- **Tall festival lantern at the gate (ōtōrō, takatōrō)**: tall standing wooden lantern structure (assumed; Konpira's great lantern is 1860). Temple, occasional, large.
- *Fire tub (tensui-oke)*: see Fire.

### == U Religious: Graveyards and grave markers ==

- **Temple and village graveyard (bochi / hakaba)**: packed rows of stones and wooden markers with paths and water points, on a slope beside or behind the temple. Graveyard/commons, common, large `[terrain]` set + props. Hook: landmark, atmosphere, cover field, eerie. (BL: Civic, graveyard; Buddhist "graveyard and its hut") {seam S192: U Religious: Graveyards and grave markers + R §11}
- **Square-pillar gravestone (kakuchū-gata)**: plain upright square pillar on two or three bases; the Edo commoner stone, spreading through the 18th c. Graveyard, occasional (R, 1730) / common (U), small. The "X family grave" inscription is `[outside 1680-1750: Meiji]`. {seam S194: U Religious: Graveyards and grave markers + R §11}
- **Roofed gravestone (kasa-tsuki)**: pillar with a small stone roof cap. Graveyard, occasional, small.
- **Boat-halo relief gravestone (funagata kōhai)**: stone with a boat-shaped top carved with a Buddha or Jizō in relief; the commoner favourite of the 17th and early 18th c. Graveyard, common, small. (typology from Edo grave archaeology; verify) {seam S193: U Religious: Graveyards and grave markers + R §11}
- *Five-ring stupa (gorintō)* → S135, under R §11.
- *Treasure-seal stupa (hōkyōin-tō)*: see Temple.
- **Egg-shaped monk's stupa (muhōtō, rantō)**: seamless egg on an octagonal base, for abbots. Graveyard, occasional, medium.
- **Stone slab stupa (itabi)**: flat stone slab with Sanskrit seed letters; mostly medieval, standing on in old graveyards. Graveyard, occasional, small.
- *Wooden grave post (bohyō)* → S195, under R §11.
- *Memorial slats (sotoba)* → S102, under R §11.
- **Slat rack (tōba-tate)**: frame holding the slats behind a grave. Graveyard, common, small.
- *Flower tubes and water cup (hana-tate, mizu-bachi)* → S198, under R §11.
- *Incense stand (senkō-tate)* → S199, under R §11.
- *Buckets and ladles at the water point (teoke, hishaku, teoke-kake)* → S197, under R §11.
- *Fresh-grave fence and roof (sutegaki, tamaya)* → S196, under R §11.
- **Heap of unclaimed gravestones (muen-zuka / muen-tō)**: pyramid of old stones gathered from lost graves. Graveyard/roadside/forest edge, medium. Frequency disputed (§3.3): W and U occasional; R rare, mostly a later accumulation `[outside 1680-1750: later]`. Hook: landmark, eerie. {seam S137: U Religious: Graveyards and grave markers + W §17 + R §11}
- **Daimyō grave precinct**: stone fence, gate, lanterns and a huge gorintō or hōkyōin-tō. Graveyard, rare, large. Hook: landmark.
- **Great graveyard of Kōya-san Okunoin**: avenue of daimyō gorintō under cedars. Landmark `[off-map: Kii]`.
- **Shogunal mausoleum grounds**: bronze stupa (hōtō), bronze lantern ranks and gates at Zōjō-ji, Kan'ei-ji, Nikkō. Graveyard, landmark, large. → BL Buddhist mausoleum.
- *Burial grave in the field (ume-baka)*: the two-grave system's bare burial plot. → rural flavour; BL Civic.

### == U Religious: Stone monuments, stelae and statues ==

- **Inscribed stele (sekihi)**: tall slab recording a founding, a bridge, a benefactor. Temple/street, occasional, medium. Hook: lore text.
- **Stele on a turtle (kifu)**: stele set on a stone tortoise, Chinese style, for great lords (verify how common in 1730 Japan). Temple, rare, medium.
- *Memorial stupa for disaster dead (kuyō-tō)* → S139, under R §11.
- **Haiku stone (kuhi)**: stone carved with a haiku; Bashō died in 1694 and early memorial "Bashō mounds" (Bashō-zuka) appear in the 18th c. (verify first dates). Garden/temple, occasional, small.
- **Poem stone (kahi)**: waka carved on a stone. Garden, rare, small.
- *Daimoku stone (daimoku-tō)* → S091, under W §5.
- *Nembutsu memorial stone (nembutsu kuyō-tō, myōgō-hi)* → S090, under W §5.
- *Kōshin stone (kōshin-tō)* → S085, under W §5.
- *Street-corner Jizō box (tsuji Jizō)* → S079, under W §5.
- *Road-guardian stones (dōsojin, batō Kannon)*: → rural / wilderness flavours.
- **Stone arhats (rakan)**: stone arhat groups (Rakan-ji's 1695 set is wooden, indoors; big stone groups like Kita-in are 1782–1825). Temple, rare. (verify)
- *Pilgrimage miniature course (utsushi fudasho)* → S094, under W §5.
- **Boundary stone of a temple precinct (keidai-ishi)**: marker of temple land (assumed). Temple, occasional, small.

### == U Castle: Castle stone walls (ishigaki) by technique ==

- *Rough piled stone (nozura-zumi)* → S173, under R §8.
- **Dressed-joint stone (uchikomi-hagi)**: stones with faces and edges knocked roughly to fit, packers between. Castle, common, `[terrain]`.
- **Fitted cut stone (kirikomi-hagi)**: stones cut to fit with no gaps; Edo-period showpieces (Edo Castle gates). Castle, occasional, `[terrain]`. Hook: unclimbable.
- **Coursed laying (nuno-zumi)**: stones laid in level courses. Castle, common, `[terrain]` pattern.
- **Random laying (ran-zumi)**: uncoursed. Castle, common, `[terrain]` pattern.
- **Tortoise-shell laying (kikkō-zumi)**: hexagonal cut stones. Castle, rare, `[terrain]` pattern.
- **Diagonal laying (tanigi-zumi, otoshi-zumi)**: stones set diagonally in a zigzag. `[outside 1680-1750: late Edo]` (verify)
- **Long-and-short corner (sangi-zumi)**: alternate long stones at wall corners; standard by 1600. Castle, common, medium.
- **Curved "warrior-return" profile (musha-gaeshi, sori)**: wall base gently sloped, top near vertical. Castle, common, `[terrain]`.
- **Belt stone walls on an earth rampart (hachimaki / koshimaki ishigaki)**: low stone walls at the top (headband) or foot (waistband) of an earth bank (Edo Castle, Hikone). Castle, occasional, `[terrain]`.
- **Giant mirror stone (kagami-ishi)**: huge flat stone set at a gate for show (Osaka's Tako-ishi, 1620s). Castle, landmark, large.
- **Mason's marks (kokuin)**: crests and signs carved by each lord's crews on stones. Castle, common, decal. Hook: lore.
- **Rampart stairs (gangi)**: wide stone stairs built against the inside of a wall, up to the top (paired, V-shaped at some castles). Castle, common, medium. Hook: climb route.
- **Stone steps and ramps (ishidan, sakaguchi)**: within gates and baileys. Castle, common, medium.
- **Drain holes in walls (mizu-nuki)**: small stone-lined drains through the wall base (assumed). Castle, common, small.

### == U Castle: Earthworks, moats and castle water ==

- **Earth rampart (dorui)**: rammed-earth bank round a castle terrace, turfed (shiba-doi) or planted with pines; overgrown on ruins. Castle/mountain ruin, common (castles) / occasional (ruins), `[terrain]`. Hook: elevation, cover. {seam S134: U Castle: Earthworks + W §15}
- **Pine-topped bank (dote no matsu)**: rampart with a pine row on top. Castle, common, `[terrain]`.
- **Wet moat (mizu-bori)**: water moat. Castle, common, `[terrain]`. Hook: water, barrier.
- **Dry moat (kara-bori)**: moat without water. Castle, common, `[terrain]`. Hook: cover, trench route.
- *Ridge-cut ditch (hori-kiri)* → S132, under W §15.
- *Vertical slope ditches (tate-bori) and ribbed ditches (une-bori)* → S133, under W §15.
- **Town-enclosing earthwork (sōgamae)**: outer earth-and-moat ring around a whole town (Odawara, Kanazawa); only some towns. Street edge, rare, `[terrain]`.
- **Berm at the wall foot (inu-bashiri)**: narrow ledge between wall base and moat. Castle, common, `[terrain]`. Hook: sneak route.
- **Walkway behind the wall (musha-bashiri)**: path along the inside of a wall top. Castle, common, `[terrain]`. Hook: patrol route.
- *Moat water gate (mizu-mon, hi)* → S156, under R §2.
- **Moat dam (tsutsumi, dote-bashi)**: earth dam separating moats at different levels, often with a path on top. Castle, occasional, medium.
- **Castle well (jō-ido)**: stone-lined well inside a bailey, or on a ruined castle terrace, sometimes still wet. Castle / hill ruin, common (live castles) / rare (ruins), small–medium. Hook: WATER, fall danger. The roofed well turret is BL. {seam S131: U Castle: Earthworks + W §15}

### == U Castle: Castle walls, ports and gate plazas ==

- **Earthen wall with loopholes (dobei, sama)**: plastered wall with tile coping and gun and arrow ports. Castle, common, large. Hook: cover, firing ports.
- **Gun port (teppō-zama)**: small round, triangular or square port at kneeling height. Castle, common, decal/small. Hook: shoot-through.
- **Arrow port (ya-zama)**: tall rectangular port. Castle, common, decal/small.
- **Hidden port (kakushi-zama)**: port plastered over on the outside, knocked out when needed (verify common). Castle, rare, decal.
- *Stone-drop chute (ishi-otoshi)*: projecting bay at a wall or turret base. → BL Military (turret part).
- **Board wall of a bailey (ita-bei)**: plain board wall in lesser baileys. Castle, common, large.
- **Box gate plaza (masugata)**: square court between an outer gate (kōrai-mon) and an inner turret gate (yagura-mon), forcing a right-angle turn. Castle, common in castles, `[terrain]` + gates. Hook: killing ground, chokepoint. → BL Military for the gates.
- **Horse-exit barbican (umadashi)**: earth or stone outwork in front of a gate (round or square); survivors at Nagoya, Hiroshima (verify for 1730 state). Castle, rare, `[terrain]`.
- *Earth causeway to a gate (dobashi)*: see Bridges.
- *Dismount sign at the main gate (geba-fuda)*: see Notices.
- *Gate fire baskets (kagaribi)*: see Lighting.
- *Guard post outside the gate (bansho)*: → BL Military.
- **Front-gate slope (ōte-zaka)**: approach slope to the main gate, often stepped. Castle, common, `[terrain]`.
- *Outer-moat gates of Edo (the "36 mitsuke")*: → BL Military; outdoor parts are masugata, moat and bridge.

### == U Castle: Samurai quarter and parade grounds ==

- **Samurai-house frontage**: long nagaya-mon or board wall with a gate; the streets are walls, not shops. Samurai quarter, common, `[terrain]` set. → BL Dwellings upper, nagaya-mon.
- **Plastered tile-grid wall (namako-kabe)**: square tiles set diagonally with raised white plaster joints; on outer walls of kura and samurai gatehouses. Samurai quarter/street, occasional, large. Hook: landmark finish.
- *Hitching rail at a samurai gate (komayose)*: see Street furniture.
- *Crossroads guard post (tsuji-ban)*: → BL Government.
- **Procession dressing (daimyō gyōretsu)**: spears with sheaths, lacquered boxes on poles (hasami-bako), palanquins, banners, horses: a moving outdoor set. Street, occasional (event), medium set. Hook: event.
- **Horse ground (baba)**: long straight riding track with an earth bank and pines; Edo's Takada-no-baba (1636). Samurai quarter, occasional, `[terrain]`. Hook: open ground. → BL Military.
- **Mounted archery course (yabusame-ba)**: long lane with three targets; Yoshimune revived yabusame in **1728** at Takada-no-baba (verify details). Samurai quarter/shrine, rare, `[terrain]` + targets. → BL Military.
- **Archery target butt (azuchi) and targets (mato)**: earth bank with a small roof and paper or board targets. Samurai quarter/temple, occasional, medium. Hook: none (dressing), or a mini-game.
- **Long-range temple archery lane (tōshiya)**: the 120 m veranda range at Kyoto's Sanjūsangendō (Wasa Daihachirō's record, 1686) and its Edo copy at Fukagawa (moved 1698, rebuilt 1701, verify). Temple, landmark, `[terrain]`. → BL for the hall.
- **Gun range (teppō-ba)**: open ground with a bank for gunnery practice (Edo had several; verify names). Samurai quarter, rare, `[terrain]`. (Note: the mod has no guns; keep as scenery only.)
- **Drill ground (chōren-ba)**: `[outside 1680-1750: Western-style drill grounds are 1840s–60s]` (assumed)
- *Falconry grounds (taka-ba)*: → rural / wilderness flavour.

### == U Festivals: Markets and fairs ==

- **Periodic market (ichi / rokusai-ichi)**: a cleared street, plaza or shrine forecourt where stalls met on fixed days. Market/commons, common (towns) / rare in villages, `[terrain]` set + stalls. Hook: trade. (BL: Shops "market stalls") {seam S202: U Festivals: Markets and fairs + R §13}
- **Reed-screen stall (yoshizu-bari mise)**: stall of poles and reed screens with a board counter. Market/street, common, medium. Hook: soft cover, loot spot.
- **Temporary board stall (kake-mise, kari-goya)**: plank booth put up for a fair and taken down after. Market, common, medium.
- **Ground-mat vendor (roten, muhiro)**: goods spread on straw mats or a cloth. Market, common, small. Hook: loot spot.
- **Fish-display boards (itafune)**: long wooden boards on trestles on which fish were laid out at Nihonbashi fish market; the right to a board was a traded licence. Market, landmark (Edo), medium. Hook: food loot. → BL Food "fish market".
- **Fish-market tubs, baskets and hooks**: shallow tubs, bamboo baskets, hooks and knives (assumed). Market, common, small.
- **Vegetable market piles (yacchaba)**: produce heaped under awnings at Kanda. Market, landmark (Edo), medium. → BL Food.
- **Year-end market (toshi-no-ichi)**: New Year goods (pine, straw ropes, bows, battledores) sold at temple grounds (Asakusa, 12th month). Market, seasonal, `[terrain]` set.
- **Doll market (hina-ichi)**: stalls selling festival dolls before the 3rd of the 3rd month (Jukkendana, Edo; verify date). Market, seasonal, set.
- **Plant market (ueki-ichi)**: potted plants and trees at temple fairs (assumed; Genroku boom). Market, occasional, set.
- **Bon market (kusa-ichi)**: stalls selling Bon altar goods (reed mats, lotus leaves, lanterns) before Obon (verify). Market, seasonal, set.
- **Rake fair (tori-no-ichi)**: bamboo rakes (kumade) sold at Ōtori shrines in the 11th month (verify date; late 18th c. growth). Market, seasonal, set.
- **Temple fair day (ennichi)**: monthly holy day of a temple with stalls, shows and lanterns at night. Temple forecourt, common, set. Hook: crowd, light.
- **Temple treasure showing (kaichō)**: a temple's hidden icon displayed for weeks, with banners, offering tables, stalls and show booths; very popular in 18th-c. Edo. Temple forecourt, occasional (event), set. Hook: event.
- **Temple lottery (tomikuji, tomi-tsuki)**: a stage with a box of numbered tags, pierced with an awl through a hole to draw winners, before a crowd. **1730**: shogunate permits the lottery at Gokoku-ji (Edo) to fund Ninna-ji; from then licensed lotteries (gomen-tomi) fund temple repairs (Yushima Tenjin, Yanaka Kannō-ji, Meguro Fudō follow). Temple forecourt, rare (event), medium set. Hook: event, crowd.
- **Rice exchange street (Dōjima kome-ichiba)**: Osaka rice market, officially recognised in **1730**; trading spilled onto the riverside street. Market, landmark (Osaka), `[terrain]` set. (Flag or signal relays of prices to other towns: verify date.)
- *Horse fair (uma-ichi)*: → BL Services.
- **Rag market (boro-ichi)**: Setagaya year-end market (from 1578; verify continuity). Market, seasonal, set.

### == U Festivals: Festival sets and seasonal dressing ==

- **Great floats (yama, hoko)**: Kyoto's Gion festival floats: towering wheeled halberd-floats (hoko) and portable mountain-floats (yama) with tapestries. Festival, landmark (Kyoto, 7th month), large. Hook: landmark, climb. → BL Shinto "float store".
- **Festival float (dashi / danjiri / yatai)**: wheeled or carried float: Kinai village danjiri (Kishiwada's from 1703), and Edo's tall wheeled dashi with a doll on top at the Sannō and Kanda festivals (alternating years from 1681, entering the castle). Festival/commons, occasional (Kinai) / landmark (Edo), large. Hook: event, landmark. (BL: float store) Kyoto's Gion hoko: U (Festival sets). {seam S204: U Festivals: Festival sets and seasonal dressing + R §14}
- **Portable shrine (mikoshi, mikoshi togyo)**: the mikoshi on its carrying poles, kept in a store and out only at festivals, carried by bearers through streets and villages. Festival/shrine/commons, occasional (seasonal), medium. Hook: event. (BL: mikoshi store) Resting place: R §10 (otabisho). {seam S203: U Festivals: Festival sets and seasonal dressing + U Religious: Shrine forecourt + R §14}
- **Viewing stands (sajiki)**: temporary raised stands of poles, boards and mats along a festival route or riverbank. Festival, occasional, large. Hook: elevation.
- *Festival lantern strings (chōchin tsunagi)* → S207, under R §14.
- **Tall pole lanterns (takahari-chōchin)**: big lanterns hoisted on poles at ward entrances for festivals. Festival, occasional, medium. Hook: light, landmark.
- *Ward festival banners (matsuri nobori)* → S206, under R §14.
- **Sacred rope across a street (shimenawa)**: rope with paper streamers between bamboo poles, marking the festival bounds (assumed). Festival, occasional, medium.
- *Bon shelf (bon-dana, shōryō-dana)* → S177, under R §9.
- *Tall Bon lantern (takatōrō)* → S178, under R §9.
- *Welcome and send-off fires (mukaebi, okuribi)* → S179, under R §9.
- **Great hillside fires (Gozan no okuribi, Daimonji)**: huge character-shaped bonfires on the hills round Kyoto on the 16th of the 7th month (attested in the 17th c.). Festival, landmark (Kyoto), `[terrain]`. Hook: visible landmark at night.
- **Floating lanterns (tōrō nagashi)**: paper lanterns set on rivers at the end of Bon. Festival, occasional, small. Hook: light on water.
- **Bon-dance tower (bon-odori yagura)**: temporary central scaffold with a drum and singer for the circle dance. The ring dance was everywhere; the tall central tower is poorly attested before late Edo, so a 1730 dance may just have a singer and drum on a bench or low stand. Commons/shrine/temple, occasional (summer), medium–large. Hook: event, landmark. (verify; tagged) {seam S205: U Festivals: Festival sets and seasonal dressing + R §14}
- *New Year pine gate (kadomatsu)* → S175, under R §9.
- *New Year straw rope (shimekazari)* → S176, under R §9.
- **Setsubun charm (hiiragi iwashi)**: holly sprig with a sardine head at the door. Festival, common, small.
- *New Year bonfire (sagichō, dondo-yaki)* → S208, under R §14.
- *Boys' Festival banners (sekku nobori, fukinagashi)* → S210, under R §14.
- *Carp streamers (koinobori)* → S209, under R §14.
- *Tanabata bamboo (tanabata-dake)* → S180, under R §9.
- **Blossom-viewing enclosure (hanami-maku)**: cloth curtains strung between cherry trees, with felt mats, lanterns and picnic boxes; Asukayama (planted 1720) and the Sumida embankment (1717) were Yoshimune's new blossom grounds. Festival, seasonal, medium. Hook: soft cover, food loot.
- **Kimono-curtain picnic (kosode-maku)**: robes hung on cords as a picnic screen (verify date). Festival, occasional, medium.
- *Moon-viewing offering stand (tsukimi-dai)* → S211, under R §14.
- *Mid-summer river opening sets (kawabiraki)*: see Fireworks.

### == U Festivals: Entertainment grounds and stages (temporary) ==

- **Riverbed entertainment ground (Shijō-gawara)**: Kyoto's Kamo riverbed, with show booths, tea stands and summer platforms. Riverbed, landmark (Kyoto), `[terrain]` set.
- **Bridge-end show ground (Ryōgoku hirokōji)**: Edo's busiest open space: show booths, archery booths, storytellers, food stalls. Street, landmark (Edo), `[terrain]` set. Hook: crowd, loot spots. → BL Services "show booth".
- **Show booth (misemono-goya)**: → BL Services. Outdoor front: painted signboards and a barker's stand. Street, common at fairs, medium.
- **Small-bow archery booth (yōkyūba)**: booth where customers shot small bows at targets (verify date). Street, occasional, medium.
- **Benefit sumo ground (kanjin-zumō)**: temporary ring with bamboo-and-mat stands, licensed at Fukagawa Hachiman from 1684. Festival/temple, occasional (event), large. Hook: arena. → BL Shinto "sumo ring".
- **Benefit Noh stage (kanjin-nō butai)**: temporary Noh stage and stands, a rare grand event (assumed; Edo held a few). Festival, rare, large.
- *Kagura and puppet stage in the open (kari-butai)* → S212, under R §14.
- **Street performers' pitch**: marked only by a mat, a lantern and a crowd ring (assumed). Street, common, small.

### == U Festivals: Fireworks and river events ==

- **River opening fireworks (Ryōgoku kawabiraki)**: from 1733 by tradition: fireworks off Ryōgoku bridge on the Sumida for the water-god festival after the 1732 famine; fired by Kagiya (6th generation). River, landmark (Edo, from the 28th of the 5th month), `[terrain]` event. Hook: light, noise, crowd.
- **Fireworks boat (hanabi-bune)**: boat carrying the fireworks maker and his mortars, anchored in the river. River, rare (event), medium.
- **Fireworks mortar (tsutsu)**: wooden or bamboo launch tube bound with rope (assumed materials). River, rare, small. Hook: noise, light.
- **Set-piece frame (shikake-hanabi)**: frame with fireworks arranged to burn as a picture (verify date). River, rare, medium.
- **Hand fireworks sold in the street (te-hanabi, hanabi-uri)**: small hand fireworks sold by peddlers in summer (verify date). Street, occasional, small. Hook: light, noise lure.
- **Townsmen's fireworks ban**: Edo banned fireworks in town except on the riverbanks (1648 and repeated; verify). Design note, not an object.
- **Moored party boats with lanterns (yakatabune, yanebune)**: see Boats; on event nights they carry rows of lanterns. River, occasional, medium. Hook: light.
- **Food-selling boats among the party boats (uroro-bune)**: small boats selling snacks to the pleasure boats (verify name). River, occasional, medium.
- **Riverbank viewing stands and tea stalls**: sajiki and reed tea stands along the embankment. River, event, medium.
- **Handheld tube fireworks (tezutsu hanabi)**: big hand-held tubes (Mikawa tradition) (verify date). Festival, rare `[off-map?]`, small.
- *Farmers' rockets (ryūsei)*: bamboo rockets (Chichibu) (verify date). → rural flavour.

---

# 3. Seams, duplicates and contradictions

## 3.1 Items two or more flavours both listed (merged)

Each merged entry sits in §2 under the flavour named first; the others point to it. Merged entries keep every tag, hook, date and verify flag of their members (the verify flags are also in §8).

| Seam | Merged entry | Kept under | Merged from |
|---|---|---|---|
| S001 | Roadside pine avenue (matsu-namiki) | N §E | W §2 *Pine avenue* |
| S002 | Cedar avenue (sugi-namiki) | W §2 | N §X *Hakone cedar avenue* |
| S003 | Coastal pine shelterbelt (bōsa-rin / bōfū-rin) | N §E | W §19 *Planted coastal pine belt* |
| S004 | Farmstead windbreak grove (yashiki-rin) | R §8 | N §E *Farmstead windbreak* |
| S005 | Village bamboo grove (take-yabu) | R §3 | N §E *Village bamboo grove* |
| S006 | River levee with planted bamboo (tsutsumi / dote, suibō-rin) | R §1 | N §E *Levee bamboo and willow*; W §12 *Bamboo-grove bank protection*; U Water: Canals *River embankment with trees* |
| S007 | Grass-cutting commons (kusakari-ba / kaya-ba / magusa-ba) | N §E | W §11 *Wild-grass cutting ground*; R §3 *Grass-cutting slope*; R §3 *Thatch meadow* |
| S008 | Swidden plot (yakihata / kirikae-bata) | N §E | W §8 *Slash-and-burn plot*; R §3 *Burnt clearing fields* |
| S009 | Ash-buried farmland (Hōei sunafuri / suna-ume no hatake) | N §E | W §12 *Ash-buried abandoned field* |
| S010 | Bald / eroded hill (hageyama) | N §E | W §8 *Clear-cut bare slope* |
| S011 | Sugi–hinoki plantation (uebayashi) | N §E | W §8 *Planted cedar stand* |
| S012 | Persimmon (kaki) | N §D | R §3 *Yard persimmon tree* |
| S013 | Ume and plum grove (ume / ume-bayashi / baien) | N §D | R §3 *Plum grove*; U Gardens: Stroll garden *Plum grove* |
| S014 | Chestnut, orchard (kuri) | N §D | R §3 *Chestnut trees* |
| S015 | Tea bushes (chanoki; aze-cha / kuro-cha) | N §Q | R §3 *Tea bushes on field edges*; N §G *Tea, wild or escaped* |
| S016 | Mulberry (kuwa; kuwa-batake) | N §Q | R §3 *Mulberry field and mulberry hedge* |
| S017 | Paper-mulberry and paperbush patches (kōzo / mitsumata) | R §3 | N §Q *Paper mulberry*; N §Q *Paperbush* |
| S018 | Lacquer tree (urushi) | N §C | R §3 *Lacquer trees along bunds*; W §11 *Lacquer tree with tapping scars* |
| S019 | Wax tree (haze / hazenoki) | N §C | R §3 *Wax trees* |
| S020 | Flat paddy and paddy rice (hira-ta; ine) | R §1 | N §O *Paddy rice*; N §S *Paddy mud, flooded / drained / cracked* |
| S021 | Barley and wheat (ōmugi, hadakamugi, komugi; mugi-batake) | R §3 | N §O *Barley*; N §O *Wheat* |
| S022 | Millets (awa, hie, kibi) | R §3 | N §O *Foxtail millet*; N §O *Japanese barnyard millet*; N §O *Proso millet* |
| S023 | Buckwheat (soba; soba-batake) | R §3 | N §O *Buckwheat* |
| S024 | Soybean and azuki (daizu, azuki; aze-mame) | R §3 | R §1 *Bund-top soybeans*; N §P *Soybean*; N §P *Azuki bean* |
| S025 | Climbing beans on poles (sasage, ingen-mame) | R §3 | N §P *Cowpea*; N §P *Hyacinth / kidney bean* |
| S026 | Daikon (daikon-batake) | R §3 | N §P *Daikon radish* |
| S027 | Winter greens (na / komatsuna) | R §3 | N §P *Komatsuna* |
| S028 | Welsh onion (negi) | R §3 | N §P *Welsh onion* |
| S029 | Burdock (gobō) | R §3 | N §P *Burdock* |
| S030 | Taro (satoimo; ta-imo) | R §3 | R §1 *Taro wet field*; N §P *Taro* |
| S031 | Sesame (goma-batake) | R §3 | N §P *Sesame* |
| S032 | Rapeseed (natane-batake) | R §3 | N §Q *Rapeseed* |
| S033 | Cotton (wata-batake) | R §3 | N §Q *Cotton* |
| S034 | Indigo (ai-batake) | R §3 | N §Q *Indigo* |
| S035 | Hemp (asa-batake) | R §3 | N §Q *Hemp* |
| S036 | Tobacco (tabako-batake) | R §3 | N §Q *Tobacco* |
| S037 | Konjac (konnyaku-batake) | R §3 | N §P *Konjac* |
| S038 | Sweet potato (satsuma-imo) | R §3 | N §P *Sweet potato* |
| S039 | Maize (tōmorokoshi / nanban-kibi) | R §3 | N §O *Maize* |
| S040 | Korean ginseng bed (chōsen ninjin; ninjin-hata) | R §3 | N §P *Korean ginseng* |
| S041 | Wasabi terrace (wasabi-da) | R §3 | N §P *Wasabi, cultivated* |
| S042 | Gourd trellis (yūgao-dana / hyōtan-dana) | R §3 | N §P *Bottle gourd* |
| S043 | Lotus (hasu; renkon-ta, hasu-ike) | N §M | R §1 *Lotus-root field*; U Gardens: Stroll garden *Lotus pond*; U Water: Moats *Lotus in the moat* |
| S044 | Rush field for tatami (igusa-da) | R §1 | N §Q *Rush, crop* |
| S045 | Japanese alder and living-tree rack row (hannoki; hasa-gi / inaki) | N §C | R §4 *Living-tree rack row* |
| S046 | Threshing yard / swept earth (kado / niwa) | R §4 | N §S *Swept earth* |
| S047 | Spring and spring pool (yūsui / izumi / shimizu) | R §2 | N §U *Spring* |
| S048 | Landslide scar (hōkai-chi / yama-kuzure) | N §T | W §18 *Landslide scar with a Jizō* |
| S049 | Rock overhang and shallow cave (iwaya / iwa-kage) | N §T | W §3 *Rock overhang camp* |
| S050 | Lava tube cave (fūketsu, hyōketsu, tainai) | N §T | W §6 *Rebirth lava cave* |
| S051 | Sacred rock (iwakura / shinseki) | W §7 | N §T *Sacred rock*; U Religious: Shrine forecourt *Sacred rock* |
| S052 | Sacred tree (shinboku / goshinboku) | W §7 | R §10 *Sacred tree rope*; U Religious: Shrine forecourt *Sacred tree with a fence* |
| S053 | Driftwood stacks (yorigi) | R §15 | W §19 *Driftwood stacks* |
| S054 | Mile mound pair (ichirizuka) | W §1 | N §X *Ichirizuka enoki trees* |
| S055 | Plain carp and crucian carp (magoi, funa) | U Gardens: Garden fauna and small living features | N §Fauna *Carp* |
| S056 | Stone-paved pass road (ishidatami) | W §2 | U Streets: Street surface *Stone-paved pass road through a town* |
| S057 | Stone cart rails (kuruma-ishi) | W §2 | U Streets: Street surface *Stone cart-track paving*; R §17 *Stone cart tracks* |
| S058 | Roadside ditch and street gutter (sokkō / omote-dobu) | U Streets: Street surface | W §2 *Ditch-side road drains* |
| S059 | Road-repair and procession sand heaps (michi-bushin no suna / morizuna) | W §2 | U Streets: Street surface *Sand heaps for processions* |
| S060 | Stone steps (ishidan / ishi-kaidan / ishidan-zaka) | W §2 | R §10 *Stone steps*; U Religious: Shrine forecourt *Stone steps up to the shrine*; U Streets: Street surface *Sloped street with stone steps* |
| S061 | Direction stone (oiwake-ishi / michi-shirube / dōhyō) | W §1 | U Streets: Notices *Road distance post in town* |
| S062 | Ōyama road markers (Ōyama-michi hyō / dōhyō) | W §6 | R §12 *Ōyama pilgrimage road marker* |
| S063 | Bench (shōgi / endai) | U Streets: Street furniture | W §3 *Rest bench*; R §6 *Eaves bench* |
| S064 | Sitting stone (koshikake-ishi) | W §3 | R §13 *Stone slab bench at a crossroads*; U Streets: Street furniture *Rest stone* |
| S065 | Horse and animal trough (mizu-bune / kaiba-oke) | U Streets: Street furniture | W §3 *Horse trough*; R §7 *Animal trough*; R §13 *Stone water trough at the village entrance* |
| S066 | Hitching post and tie stone (uma-tsunagi / tsunagi-ishi) | U Streets: Street furniture | W §3 *Horse tie stone*; R §7 *Tethering post*; R §7 *Tethering stone* |
| S067 | Horse-washing ramp (uma-arai-ba) | W §3 | R §7 *Horse-washing place*; U Water: Moats *Moat-side horse-washing place* |
| S068 | Bamboo pipe and piped spring (kakehi / kakei) | R §2 | W §3 *Piped roadside spring*; U Streets: Wells and street water supply *Bamboo water pipe*; U Gardens: Basins *Bamboo spout* |
| S069 | Flume on trestles (toi / kakehi-bashi / suidō-bashi) | R §2 | W §4 *Log flume bridge*; U Streets: Wells and street water supply *Aqueduct bridge* |
| S070 | Always-lit lantern and lighthouse lantern (jōyatō / tōmyōdō) | W §3 | U Streets: Street lighting and lanterns *Always-lit lamp*; W §20 *Stone lighthouse lantern*; R §17 *Tall stone night-lamp towers* |
| S071 | Crossroads lamp (tsuji-andon) | U Streets: Street lighting and lanterns | W §3 *Crossroads lantern post* |
| S072 | Stepping stones across water (tobi-ishi / ishi-watari / sawatari) | W §4 | U Gardens: Paths and stepping stones *Stepping stones across water* |
| S073 | Stone slab bridge (ishi-bashi / ishi-ita-bashi) | U Water: Bridges | W §4 *Stone slab bridge*; R §2 *Stepping stones and slab bridge over a channel*; U Gardens: Garden bridges *Single slab bridge*; U Gardens: Dry garden *Stone bridge in a dry garden*; U Streets: Street surface *Slab bridge over a gutter* |
| S074 | Plank bridge (ita-bashi / kōran-bashi) | U Water: Bridges | W §4 *Plank bridge*; U Gardens: Garden bridges *Plank bridge with rails*; U Water: Bridges *Flat bridge with railings* |
| S075 | Earth-covered bridge (dobashi) | U Water: Bridges | W §4 *Earth-covered bridge*; U Gardens: Garden bridges *Garden earth bridge* |
| S076 | Boat bridge (funa-bashi) | W §4 | U Water: Bridges *Boat bridge* |
| S077 | Stone bridge abutment (hashi-dai no ishigaki) | U Water: Bridges | W §4 *Stone abutment* |
| S078 | Roadside Jizō (michi no Jizō / tsuji-jizō) | W §5 | R §12 *Roadside Jizō* |
| S079 | Jizō hut / street-corner Jizō box (Jizō-dō / tsuji Jizō) | W §5 | U Religious: Stone monuments *Street-corner Jizō box* |
| S080 | Six-Jizō row (roku Jizō) | U Religious: Temple forecourt | W §5 *Six-Jizō row*; R §11 *Six Jizō row* |
| S081 | Couple dōsojin (sōtai dōsojin) | W §5 | R §12 *Paired-figure dōsojin* |
| S082 | Character dōsojin (moji dōsojin) | W §5 | R §12 *Character dōsojin* |
| S083 | Round-stone dōsojin (maru-ishi dōsojin) | W §5 | R §12 *Round-stone dōsojin* |
| S084 | Phallic stone (konsei-sama / yōseki / seki-bō) | W §5 | R §12 *Phallic stones* |
| S085 | Kōshin stone (kōshin-tō) | W §5 | R §12 *Kōshin stone with three monkeys*; U Religious: Stone monuments *Kōshin stone* |
| S086 | Kōshin mound (kōshin-zuka) | W §5 | R §12 *Kōshin mound* |
| S087 | Horse-headed Kannon (batō Kannon) | W §5 | R §12 *Horse-headed Kannon* |
| S088 | Horse grave and animal memorial (uma-zuka / uma kuyō / chikushō kuyōtō) | W §5 | R §9 *Animal memorial stone* |
| S089 | Moon-waiting stone (tsukimachi-tō: nijūsan-ya / jūkyū-ya) | W §5 | R §12 *Moon-vigil stones* |
| S090 | Nenbutsu stone (nenbutsu-tō / myōgō-hi) | W §5 | R §12 *Nenbutsu name stone*; U Religious: Stone monuments *Nembutsu memorial stone* |
| S091 | Daimoku stone (daimoku-tō) | W §5 | R §12 *Lotus Sutra title stone*; U Religious: Stone monuments *Daimoku stone* |
| S092 | Hōkyōin-tō (treasure-seal stupa) | W §5 | R §11 *Jewel-casket stupa*; R §12 *Hōkyōintō or gorintō by the road*; U Religious: Temple forecourt *Treasure-seal pagoda* |
| S093 | Sutra mound (kyōzuka) | W §5 | R §11 *Sutra mound*; U Religious: Temple forecourt *Sutra mound* |
| S094 | Miniature pilgrimage circuit (utsushi reijō / utsushi fudasho) | W §5 | R §12 *Kannon pilgrimage copy stones*; R §17 *Miniature 88-temple circuits*; U Religious: Stone monuments *Pilgrimage miniature course* |
| S095 | Stone Buddha (sekibutsu) | W §5 | R §12 *Seated stone Buddha* |
| S096 | Fudō stone (Fudō Myōō) | W §5 | R §12 *Fudō Myōō stone* |
| S097 | Water-god stone (suijin-hi) | W §5 | R §12 *Water god stone* |
| S098 | Mountain-god stone or hokora (yama no kami) | W §5 | R §12 *Mountain god stone* |
| S099 | Well-god offering (ido-gami / Suijin) | R §9 | U Streets: Wells and street water supply *Well god offering* |
| S100 | Stone lantern pair and approach lanterns (ishi-dōrō / kennō-tōrō) | R §10 | U Religious: Shrine forecourt *Stone lanterns on the approach*; W §5 *Trailhead lantern pair* |
| S101 | Banner-pole socket stones (nobori-tate ishi) | W §5 | R §10 *Banner-pole stones* |
| S102 | Wooden grave tablet (sotoba / itatōba) | R §11 | W §5 *Wooden grave tablet at a death spot*; W §17 *Wooden grave tablets*; U Religious: Graveyards and grave markers *Memorial slats* |
| S103 | Pilgrim-club stone (kō-hi: Ise-kō, Ōyama-kō, Fuji-kō) | W §6 | R §10 *Pilgrimage memorial stones* |
| S104 | "No leeks or wine" stone (kaidan-seki / kinsei-hi) | W §6 | U Streets: Notices *Prohibition stele at Zen gates* |
| S105 | Pond with a Benten islet (Benten-jima / shin-ike) | W §7 | R §10 *Shrine pond with a small bridge*; R §12 *Benzaiten stone or hokora on a pond islet* |
| S106 | Strength stones (chikara-ishi) | R §10 | W §7 *Strength stones by the road* |
| S107 | Charcoal bales (sumi-dawara) | W §8 | R §6 *Charcoal bales* |
| S108 | Firewood stack (maki-zumi) | R §6 | W §8 *Firewood stacks* |
| S109 | Log raft (ikada) | W §8 | U Water: Canals *Log raft* |
| S110 | Sledge (sori / kinma / shura) | W §8 | R §7 *Sledge* |
| S111 | Pit trap (otoshi-ana / shishi-ana) | W §9 | R §5 *Pit trap* |
| S112 | Stone boar wall (shishigaki) | R §5 | W §9 *Boar wall* |
| S113 | Earth boar bank and ditch (tsuchi-shishigaki / shishi-bori) | R §5 | W §9 *Boar ditch* |
| S114 | Stake-and-brush game fence (shishi-gaki / shika-gaki / shika-ami) | R §5 | W §9 *Game fence of brush and stakes*; R §5 *Deer net or rope fence* |
| S115 | Bird-scare clapper line (naruko) | R §5 | W §9 *Scare clapper line* |
| S116 | Basket fish trap (uke / dō / mondori / tsubo) | R §15 | W §9 *Basket fish trap* |
| S117 | Iron fire basket and watch fire (kagaribi / kagari) | U Streets: Street lighting and lanterns | W §9 *Night-fishing torch baskets*; R §5 *Night watch fires* |
| S118 | Log beehive (hachi-dō / hachi-bako) | W §11 | R §7 *Log beehive* |
| S119 | River crib spur and groyne (seigyū / waku / dashi / hane) | W §12 | R §2 *Timber river-crib spurs*; U Water: Canals *Stone groyne*; W §12 *Groyne* |
| S120 | Bamboo gabion (jakago) | W §12 | R §2 *Bamboo gabions* |
| S121 | Open staggered levee (kasumi-tei) | R §1 | W §12 *Open staggered levee* |
| S122 | Irrigation tunnel (manbo / mabu / zuidō) and the Hakone Yōsui | W §12 | R §2 *Irrigation tunnel* |
| S123 | River weir, stone and timber (seki / iseki) | R §2 | W §12 *Stone diversion weir* |
| S124 | Province and domain boundary post (kokkyō-gui / kokkyō-hi / ryōbun-gui) | R §12 | W §13 *Province boundary post*; W §13 *Domain boundary stake* |
| S125 | Village boundary post or stone (mura-zakai bōji / mura-zakai ishi) | R §12 | W §13 *Village boundary stone* |
| S126 | Village boundary rope (kanjō-nawa / kanjō-kake) | R §13 | W §13 *Village boundary rope* |
| S127 | Disease-sending straw offerings (okuri-ningyō / hōsō-gami okuri, sandawara) | W §13 | R §13 *Smallpox-god offerings* |
| S128 | Field and survey boundary marker (sakai-kui / bōji-kui / kenchi sakai-ishi / kenchi-gui) | R §3 | W §13 *Tax-land survey boundary stone*; W §1 *Survey stake* |
| S129 | Rain-prayer bonfire site (amagoi-bi / senba-bi) | R §13 | W §14 *Mountain-top prayer fire for rain* |
| S130 | Harbour and beach guide fire (kagari-bi no ba / hama-bi) | W §14 | R §15 *Beach watch fire* |
| S131 | Castle well (jō-ido) | U Castle: Earthworks | W §15 *Castle well* |
| S132 | Ridge-cut moat (horikiri) | W §15 | U Castle: Earthworks *Ridge-cut ditch* |
| S133 | Vertical slope moats (tatebori / une-bori) | W §15 | U Castle: Earthworks *Vertical slope ditches* |
| S134 | Earth rampart (dorui) | U Castle: Earthworks | W §15 *Earth rampart* |
| S135 | Five-ring stupa (gorintō) | R §11 | W §17 *Lone medieval gorintō*; U Religious: Graveyards and grave markers *Five-ring stupa* |
| S136 | Traveller's grave (yukidaore-baka / tabibito no haka) | W §17 | R §12 *Traveller's grave by the road* |
| S137 | Heap of unclaimed gravestones (muen-zuka / muen-tō) | U Religious: Graveyards and grave markers | W §17 *Unclaimed-dead heap*; R §11 *Heap of unclaimed old stones* |
| S138 | Two-grave burial grave (ume-baka, ryōbosei) | R §9 | W §17 *Burial-only grave in the hills* |
| S139 | Famine, epidemic and disaster memorial (gashi / ekibyō kuyōtō, ekishi-zuka) | R §11 | W §17 *Famine memorial*; W §17 *Plague-dead burial pit marker*; U Religious: Stone monuments *Memorial stupa for disaster dead* |
| S140 | Earthquake and tsunami memorial (jishin kuyō-tō / tsunami-hi) | W §17 | R §15 *Tsunami memorial stone* |
| S141 | Boat haul-up beach and capstan (funa-age-ba; kagurasan; koro) | R §15 | W §19 *Boat haul-up beach*; R §15 *Boat skids and rollers*; R §15 *Boat-hauling slip*; W §19 *Beach net-hauling capstan* |
| S142 | Net-drying rack (ami-hoshi-ba / ami-kake) | R §15 | W §19 *Net-drying poles* |
| S143 | Seaweed drying (kaisō hoshi-ba) | R §15 | W §19 *Seaweed-drying poles and mats* |
| S144 | Nori stakes (nori-hibi) | R §15 | W §19 *Nori stakes in the shallows* |
| S145 | Octopus-pot stacks (takotsubo) | R §15 | W §19 *Octopus pots stacked on the shore* |
| S146 | Stone tidal fish trap (ishi-hibi / sukui) | R §15 | W §19 *Tidal stone fish trap* |
| S147 | Mooring stone and post (funa-tsunagi-ishi / tomo-gui) | U Water: Canals | W §19 *Mooring stones and posts*; U Water: Canals *Mooring post* |
| S148 | Sand fence (suna-yoke gaki / kaze-gaki) | R §8 | W §19 *Sand fence* |
| S149 | Shell heap and lime-burning pit (kaigara-zuka / kaibai-yaki) | R §15 | W §19 *Shell-burning lime pit* |
| S150 | Diver's tub and float (ama-oke / ama no tarai) | R §15 | W §19 *Tengusa diving float* |
| S151 | Anchor (ikari) | R §15 | W §20 *Beached anchor* |
| S152 | Ebisu stone (ebisu-ishi) | R §15 | W §20 *Ebisu stone* |
| S153 | Sea torii (iso no torii / umi no ōtorii) | W §20 | U Religious: Torii by style *Sea torii* |
| S154 | Horse droppings (bafun) | W §21 | U Streets: Street surface *Horse-dung on the highway* |
| S155 | Shoulder pole and loads (tenbin-bō / mokko) | U Streets: Peddlers' | R §7 *Shoulder pole and baskets*; W §21 *Abandoned carrying pole and baskets* |
| S156 | Sluice gate (hi / hi-guchi / suimon / mizu-mon) | R §2 | U Water: Canals *Canal sluice / water gate*; U Castle: Earthworks *Moat water gate* |
| S157 | Lever well (hanetsurube) | R §6 | U Streets: Wells and street water supply *Lever well* |
| S158 | Pulley well (tsurube-ido) | R §6 | U Streets: Wells and street water supply *Pulley well with roof* |
| S159 | Well curb and lid (igeta / ido-waku / ishi-gawa / ido-buta) | R §6 | U Streets: Wells and street water supply *Well curb, wooden box*; U Streets: Wells and street water supply *Well curb, stone ring or stone box*; U Streets: Wells and street water supply *Well lid* |
| S160 | Communal well (mura-ido / idobata) | R §13 | U Streets: Wells and street water supply *Communal alley well* |
| S161 | Rain barrel and water jar (tensui-oke / mizu-game) | R §6 | U Streets: Street furniture *Water jar at the door*; U Streets: Fire-fighting and night-watch fixtures *Rain tub per house* |
| S162 | Laundry pole (monohoshi-zao / sao-kake / hoshi-zao) | U Streets: Street surface | R §6 *Laundry pole on forked stakes*; R §15 *Beach clothes-and-net lines* |
| S163 | Handcart (daihachi-guruma / niguruma) | U Streets: Peddlers' | R §7 *Hand-cart* |
| S164 | Oars, poles and boat gear (kai, ro, sao; tomo) | R §15 | U Water: Boats moored in town *Boat awning and poles* |
| S165 | Open bamboo grid fence (yotsume-gaki) | U Gardens: Fences | R §8 *Open bamboo grid fence* |
| S166 | Kenninji fence (kenninji-gaki) | U Gardens: Fences | R §8 *Closed split-bamboo fence* |
| S167 | Brushwood fence (shiba-gaki) | R §8 | U Gardens: Fences *Brushwood fence* |
| S168 | Reed fence (yoshi-gaki / yoshizu-gaki) | R §8 | U Gardens: Fences *Reed fence* |
| S169 | Live hedge (ikegaki) | R §8 | U Gardens: Fences *Hedge* |
| S170 | Sleeve fence (sode-gaki) | U Gardens: Fences | R §8 *Sleeve fence* |
| S171 | Board fence (itabei) | U Gardens: Fences | R §8 *Board fence* |
| S172 | Capped earth wall (tsuiji-bei / dobei) | U Gardens: Fences | R §8 *Earth wall with capping* |
| S173 | Dry-stone wall (ishigaki / nozura-zumi) | R §8 | W §2 *Road retaining wall*; U Castle: Castle stone walls *Rough piled stone* |
| S174 | Wicket gate (shiori-do / kido) | R §8 | U Gardens: Tea garden *Swing gate of brushwood*; U Gardens: Fences *Wattle gate* |
| S175 | New Year pine (kadomatsu) | R §9 | U Festivals: Festival sets and seasonal dressing *New Year pine gate* |
| S176 | New Year straw rope (shimenawa / shimekazari) | R §9 | U Festivals: Festival sets and seasonal dressing *New Year straw rope* |
| S177 | Bon altar (bon-dana / shōryō-dana) | R §9 | U Festivals: Festival sets and seasonal dressing *Bon shelf* |
| S178 | Tall Bon lantern (taka-dōrō) | R §9 | U Festivals: Festival sets and seasonal dressing *Tall Bon lantern* |
| S179 | Welcome and send-off fires (mukae-bi / okuri-bi) | R §9 | U Festivals: Festival sets and seasonal dressing *Welcome and send-off fires* |
| S180 | Tanabata bamboo (tanabata-dake) | R §9 | U Festivals: Festival sets and seasonal dressing *Tanabata bamboo* |
| S181 | Stone torii (ishi-torii) | U Religious: Torii by style | R §10 *Stone torii* |
| S182 | Vermilion wooden torii (nuri torii) | U Religious: Torii by style | R §10 *Vermilion torii* |
| S183 | Shrine approach (sandō) | U Religious: Shrine forecourt | R §10 *Approach path* |
| S184 | Guardian lion-dogs (komainu) | U Religious: Shrine forecourt | R §10 *Guardian lions* |
| S185 | Purification basin (chōzubachi) | U Religious: Shrine forecourt | R §10 *Purification basin* |
| S186 | Offering box (saisen-bako) | U Religious: Shrine forecourt | U Religious: Temple forecourt *Offering box*; R §10 *Offering box* |
| S187 | Hall bell or gong with rope (suzu / waniguchi) | U Religious: Shrine forecourt | R §10 *Bell and rope*; U Religious: Temple forecourt *Gong with rope* |
| S188 | Votive plaque rack (ema-kake) | U Religious: Shrine forecourt | R §10 *Votive plaque rack* |
| S189 | Hundred-visits stone (hyakudo-ishi) | R §10 | U Religious: Shrine forecourt *Hundred-times stone* |
| S190 | Fortune slips and lot box (omikuji / mikuji-bako) | U Religious: Shrine forecourt | R §10 *Divination slips tied to branches* |
| S191 | Donor-named stone fence and shrine-name pillar (hōnō tamagaki / shagō-hyō) | U Religious: Shrine forecourt | R §17 *Shrine-name pillar and donor stone fences*; R §10 *Shrine-name stone pillar* |
| S192 | Temple and village graveyard (bochi / hakaba) | U Religious: Graveyards and grave markers | R §11 *Communal graveyard* |
| S193 | Boat-halo relief gravestone (funagata kōhai) | U Religious: Graveyards and grave markers | R §11 *Boat-backed relief gravestone* |
| S194 | Square-pillar gravestone (kakuchū-gata) | U Religious: Graveyards and grave markers | R §11 *Square-pillar gravestone* |
| S195 | Earth grave mound and wooden grave post (dozō-baka / bohyō) | R §11 | U Religious: Graveyards and grave markers *Wooden grave post* |
| S196 | Fresh-grave guard (inu-hajiki / mogari-gaki / sutegaki / tamaya) | R §11 | U Religious: Graveyards and grave markers *Fresh-grave fence and roof* |
| S197 | Grave buckets and ladle rack (teoke, hishaku, teoke-kake) | R §11 | U Religious: Graveyards and grave markers *Buckets and ladles at the water point* |
| S198 | Grave flower tubes and water cup (hana-zutsu / hana-tate, mizu-bachi) | R §11 | U Religious: Graveyards and grave markers *Flower tubes and water cup* |
| S199 | Stone incense stand (kōro-ishi / senkō-tate) | R §11 | U Religious: Graveyards and grave markers *Incense stand* |
| S200 | Fire-bell ladder (hanshō-dai / hi-no-mi bashigo) | U Streets: Fire-fighting and night-watch fixtures | R §13 *Fire-watch ladder with bell* |
| S201 | Night-watch clappers (hyōshigi) | U Streets: Fire-fighting and night-watch fixtures | R §13 *Wooden clappers of the night watch* |
| S202 | Periodic market (ichi / rokusai-ichi) | U Festivals: Markets and fairs | R §13 *Periodic market site* |
| S203 | Portable shrine (mikoshi, mikoshi togyo) | U Festivals: Festival sets and seasonal dressing | U Religious: Shrine forecourt *Portable shrine*; R §14 *Portable shrine in procession* |
| S204 | Festival float (dashi / danjiri / yatai) | U Festivals: Festival sets and seasonal dressing | R §14 *Village festival float* |
| S205 | Bon-dance tower (bon-odori yagura) | U Festivals: Festival sets and seasonal dressing | R §14 *Bon-dance tower* |
| S206 | Festival banners (nobori / matsuri nobori) | R §14 | U Festivals: Festival sets and seasonal dressing *Ward festival banners* |
| S207 | Festival lanterns (chōchin tsunagi / mandō / kennō-chōchin dana) | R §14 | U Festivals: Festival sets and seasonal dressing *Festival lantern strings*; U Religious: Shrine forecourt *Donated paper lantern frames* |
| S208 | New Year bonfire (sagichō / dondo-yaki) | R §14 | U Festivals: Festival sets and seasonal dressing *New Year bonfire* |
| S209 | Carp streamers (koinobori) | R §14 | U Festivals: Festival sets and seasonal dressing *Carp streamers* |
| S210 | Boys' Festival banners (musha-e nobori / sekku nobori, fukinagashi) | R §14 | U Festivals: Festival sets and seasonal dressing *Boys' Festival banners* |
| S211 | Moon-viewing offering (tsukimi-dai) | R §14 | U Festivals: Festival sets and seasonal dressing *Moon-viewing offering stand* |
| S212 | Temporary stage (kari-butai) | R §14 | U Festivals: Entertainment grounds and stages *Kagura and puppet stage in the open* |
| S213 | Offered sake barrels (komo-daru / kazari-daru) | R §14 | U Religious: Shrine forecourt *Donated sake casks display* |
| S214 | Stacked rice bales and casks (kome-dawara, komo-daru) | R §4 | U Streets: Peddlers' *Rice bales and sake casks stacked for loading* |
| S215 | Knocking bamboo scarer (sōzu / shishi-odoshi) | R §5 | U Gardens: Basins *Deer scarer* |
| S216 | Night-soil buckets and pole (koe-oke / koe-tago) | R §3 | U Streets: Rubbish *Nightsoil buckets and pole* |
| S217 | Open rain shelter and arbour (azumaya / amayadori / chin) | U Gardens: Stroll garden | W §3 *Open rain shelter* |

## 3.2 Items that duplicate BUILDING_LIST entries

**a) Same object in both lists (count once).** BL holds these as `site` or civic entries with no real interior; the
outdoor list holds the same object from outside. Checked by grep against BL on 2026-09-29. Suggestion: the outdoor
list keeps the model; BL keeps the placement rule.

- Mile mound pair (ichirizuka) → BL Civic, roads "Mile mound (ichirizuka)" (seam: W §1 + N §X)
- Direction stone (oiwake-ishi) → BL Civic "Signpost stone (michi-shirube / oiwake-ishi)"
- Stone-paved pass road (ishidatami) → BL Civic "Stone-paved pass road (ishidatami)"
- Plank, earth-covered, log, cantilever, vine and boat bridges; great trestle and arched bridges (W §4, U Bridges) → BL Civic, roads (one entry each)
- Ferry landing, rope-guided ferry (W §4) → BL Civic "Ferry landing", "Rope-guided ferry (hiki-bune)"
- Horse trough and tie posts (seams) → BL Civic "Roadside horse trough and tie posts"
- Pulley well, lever well, aqueduct box well, aqueduct bridge (R §6, U Wells) → BL Civic, water supply
- Public wash steps (arai-ba) (U Wells) → BL Civic "Public spring / wash place (arai-ba, kawabata)"
- Water gate / sluice, weir, reservoir pond (tame-ike), treadwheel (R §2, W §12, U Canals) → BL Civic, agriculture and water control
- Quay steps (gangi), named quays (U Canals) → BL Civic "River quay with steps (gangi / kashi)"
- Lighthouse lantern (tōmyōdō / jōyatō) (seam, W §20) → BL Civic "Lighthouse lantern"
- Weather-watch hill with direction stone (W §14) → BL Civic "Weather-watching hill (hiyori-yama)"
- Boat haul-up slip and capstan (seam, R §15) → BL Civic "Harbour breakwater and boat-hauling slip"
- Beacon hill (W §14) → BL Military "Beacon post (noroshi-ba)"
- Black- and white-charcoal kilns (W §8) → BL Rural industry "Charcoal kiln" entries
- Timber chute and logging-camp clearing (W §8, §16) → BL Rural industry "Logging camp (soma-goya)"
- Moored log raft (seam) → BL Rural industry "Timber rafting station (ikada-ba)"
- Mine adit, abandoned mine (W §10) → BL Rural industry "Gold or silver mine (kinzan, ginzan)"
- Sulphur workings (W §10) → BL Rural industry "Sulphur workings (iō-yama)"
- Fish weir (yana) (W §9) → BL Rural industry "Fish weir (yana)"
- Grass-cutting commons (seam) → BL Rural industry "Thatch meadow and store (kaya-ba)"
- Tidal and spread salt fields (R §16) → BL Rural industry "Salt field" entries
- Fish-drying racks, sardines on the beach (R §15) → BL Rural industry "Fish-drying racks (himono-ba)"
- Nori stakes (seam) → BL nori farm / nori farmer's cottage
- Execution-ground memorial, head-display stand (W §18, U Notices) → BL Government "Execution grounds"
- Notice board (kōsatsu) (U Notices) → BL Government "Notice board (kōsatsuba)"
- Firebreak wide street, bank and open ground (U Streets) → BL Civic "Firebreak plaza and embankment"
- Street-corner toilet, alley rubbish box (U Rubbish) → BL Civic "Public toilet", "Rubbish collection point"
- Graveyard (seam) → BL Civic "Graveyard outside a temple" and Buddhist "Graveyard (bochi) and its hut"
- Roadside Jizō (seam) → BL Buddhist "Roadside Jizō (michi-no-Jizō)"
- Hokora / roadside micro-shrine (W §5) → BL Shinto "Roadside or field micro-shrine (hokora)"
- Yard shrine (R §9) → BL Dwellings outbuildings "Household shrine in the yard (yashiki-gami / Inari hokora)"
- Summit or pass shrine (W §6) → BL Shinto "Mountain summit / pass shrine"
- Waterfall ascetic site (W §6) → BL Buddhist "Waterfall practice site (taki-gyōba)"
- Cliff Buddhas (W §6) → BL Buddhist "Cliff Buddhas and cave halls (magaibutsu, iwaya-dō)"
- Fish-spotting knoll (W §14) → BL Civic "Fish-spotting tower (uomi-yagura)" (BL has the tower; W the bare knoll)
- Fire watchtower (U Fire-fighting) → BL Government "Fire watchtower (hi-no-mi yagura)"

**b) Pointers only (related, not the same object).** Every other `(BL: ...)` or `→ BL` pointer in §2 names a building
that sits next to the outdoor item (the stable beside the tether post, the tea stall behind the bench). They stay as
pointers in the entries; the list below collects them so none is lost.

(97 such pointers sit inline in §2 entries; they are not repeated here.)

## 3.3 Contradictions between the agents

Both claims shown. "Reading" is the merge's suggestion only; nothing below was re-checked (text-only job), so every
line is also a verify item.

- **Always-lit lantern (jōyatō).** W: stone lantern at a pass, lake shore or ferry, occasional (verify how many were
  lit nightly); U: always-lit lamp at town entrances and quays, occasional, "many survivors are late Edo; the type is
  older, e.g. Miya 1625"; BL agrees on Miya 1625. R §17: "tall stone night-lamp towers (jōyatō)
  `[outside 1680-1750: mostly 19th c.]`". Reading: the type is IN; the very tall stone towers are the late form.
- **Stone Inari foxes.** R §17: stone foxes are mostly after the mid-18th c. (one of the oldest Kantō pairs, Ōji
  Inari, 1764); use small wooden or ceramic foxes, or none. U (Shrine forecourt): "stone foxes with a key or jewel",
  common at Inari shrines, no date flag. Reading: follow R for 1730.
- **Komainu frequency.** R: the standing outdoor pair "begins in the Edo period; many villages had none in 1730",
  occasional. U: "standing stone pairs outdoors became common in the Edo period", common. Reading: common in towns and
  big shrines, occasional in villages.
- **Kōshin stones: when is the peak?** W: oldest dated 1664, "mostly erected up to ~1800, so our window is the peak".
  R: peak in the Kanbun–Genroku years (1661–1704). U: "peaked in the 17th–18th c." All three keep them common in 1730.
- **Heap of unclaimed gravestones (muen-zuka).** W and U: occasional. R: rare, "mostly a later accumulation",
  `[outside 1680-1750: later]`.
- **Miniature pilgrimage circuits (utsushi reijō).** W: occasional, "the boom was 18th c., some later". R: rare,
  `[outside 1680-1750: mostly late 18th–19th c.]`; 88-temple copies mostly 19th c. U: occasional (verify earliest).
- **Roadside Jizō's red bib.** W and BL: red bib and cap. R: "the red bib may be later (verify)".
- **Horse-headed Kannon (batō Kannon).** W: common in the east, many on the Nakasendō, stone ones from mid-Edo.
  R: occasional; most survivors are later 18th–19th c.
- **Paired dōsojin.** W: occasional; many late Edo, some 18th c. R tagged the type `[outside 1680-1750: mostly
  1804–30]`. Under the "did it exist in 1730" rule the type is IN, just scarce; merged entry says so.
- **Rain barrel (tensui-oke).** R: rain barrel and water jar under the eaves, common in yards. U: the tensui-oke in
  front of each house is `[outside 1680-1750: general from Kansei 1789–1801]`; 1730 towns had corner tubs with bucket
  pyramids and buckets hung at the eaves. Reading: rural rain barrels in; the per-house town fire tub out.
- **Fire ladder with bell.** R: rural fire ladders/towers are `[outside 1680-1750: Meiji+]`; a post town may have one.
  BL §2.1: "a fire-watch ladder with bell in larger villages (assumed)". U: common in Edo wards (1723 rule). Reading:
  towns yes, villages no.
- **Kanten (agar) origin.** N: "kanten was a Kyoto invention of the 1650s (mem)". W: "kanten from tengusa is said to
  date from c. 1685 (Fushimi) (verify)". Either way it is in window.
- **Korean ginseng at Nikkō.** N: trial-planted at Nikkō from 1729 (verify). R: seeds planted at Nikkō around 1728,
  distributed from 1738 (verify).
- **Fuji-zuka (pilgrim Fuji mound).** R: first built 1779, Takata. U: first 1780, Takata. Out either way.
- **Ōyama pilgrimage stones.** W: "verify: the Ōyama-mairi boom may be mostly after 1750" (yet calls it "hugely
  popular" in §6). R: treats Ōyama-kō stones and road markers as in-window Kantō cult items.
- **Offered sake barrels.** R: occasional, "the stacked-wall display may be later (verify)". U: donated sake-cask
  display `[outside 1680-1750: likely later]` (verify).
- **Donor stone fences and shrine-name pillars.** U: donor-named fence posts occasional (verify date). R: both
  `[outside 1680-1750: mostly Meiji+]` (verify).
- **Square-pillar gravestone.** R: occasional in 1730, "spreading through the 18th c."; the boat-halo stone is the
  commoner favourite. U: "the Edo commoner stone", common. Reading: boat-halo stones dominate 1730 graveyards,
  square pillars rising.
- **Shiitake log growing in Izu.** N: log cultivation "had begun in Izu, Suruga and Bungo"; an Izu forester was
  teaching it at Utogi in 1744. W: Izu Amagi and Bungo are the centres (verify the date in Izu).
- **Frequency words, not facts.** Many seams show "common (R) / occasional (W)" or "common (towns) / rare
  (villages)": these reflect each agent's setting (village vs map region vs town), not a disagreement. Merged
  entries keep both.

## 3.4 Near-overlaps kept separate, and duplicates inside one file

**Kept as separate entries** (related, but a different object, state or scale; flagged so Stephen can merge if he
wants):
- Yard fruit trees: R §3 "Yard citrus and other fruit trees (yuzu, biwa, nashi, momo)" bundles what N §D lists one by
  one (yuzu, loquat, pear, peach). R's pear trellis is a structure, N's pear the tree.
- Torii styles: R §10 "Wooden torii (shinmei or myōjin form)" vs U's style entries (shinmei, myōjin, Kashima...).
  R's is the village generic; U's are variants of it.
- Springs and wells with the same name: W §7 "Sacred spring (reisen / meisui)" (a roped forest spring) vs U "Famous
  spring well (meisui)" (a named Kyoto town well).
- Sandals hung up: W §3 "Sandal-hanging tree or post (waraji-kake)" (offering or discard at a pass) vs U "Shoe rack
  and straw sandals for sale (waraji-kake)" (shop stock) vs R §7 "Straw horse-shoe offerings" vs W §21 "Horse straw
  shoes" (road litter). One straw-sandal prop covers all four.
- Snow gear with one name: R §8 "Snow fence (yuki-gakoi)" round houses vs U "Straw snow shelters (yuki-gakoi)" over
  garden shrubs. Both mostly snow country.
- "Gangi" names three things: canal quay steps (U), castle rampart stairs (U) and Echigo snow arcades (U, off-map).
- Ruin vs live states: W §19 abandoned salt field (R §16 live); W §18 head-display stand remains (U live stand, BL);
  W §21 abandoned tea-stall shell (BL tea stall); W §16 abandoned work camp (BL logging camp). A ruin is a damage
  state of the live model.
- Natural vs worked: N §R driftwood (drift) vs the driftwood stacks seam; N §T clay banks vs W §10 clay pit; N §V
  sulphur crust vs W §10 sulphur workings; N §V hot-spring source vs W §10 troughs and wild pool; N §U waterfall vs
  W §6 waterfall ascetic site; N §E Kiso forbidden forest vs W §13 forbidden-forest markers; N §E burnt grassland
  vs W §18 burned-forest boundary.
- Ash heaps: W §12 volcanic sand dump heaps are the dug piles; N §S Hōei scoria cover is the ground; the ash-buried
  field seam is the field.
- Festivals: U's Gion hoko and yama (Kyoto hero floats) kept apart from the merged generic festival float.
- Fox figures: W §5 wild Inari hokora with foxes and R §9 small wooden foxes: same prop family; stone foxes are §6.
- Bench family: W's porter's load-rest stone and U's palanquin waiting bench stay separate from the merged bench.

**Duplicates inside one input file** (left as the agent wrote them):
- N §S (surfaces) and N §W (coast landforms) both list sand beach, pebble beach and tidal flat; §S is the texture,
  §W the landform.
- N §X (named landmarks) repeats items from N's own groups as a placement list (Ōjigoku, Aokigahara, Sengokuhara...).
  It is not counted as models.
- W §1 trail cairn vs W §6 summit cairn; W §11 nut-gathering claim marks vs W §13 commons claim stake.
- U lists some items twice on purpose (U's own note): Engetsukyō, yatsuhashi and dobashi (bridges and gardens);
  offering box, lanterns and chōzubachi (shrine and temple); geba-fuda and kaidan-seki; kagaribi; komayose; the
  town-side wet moat and the castle wet moat.
- R §17 re-lists later items already counted in its own groups (koinobori, clipped tea rows, paddy grid, village fire
  towers); those lines are pointers here.

---

# 4. Setting kits

For each settlement type in BL §2, plus the highway and the wilderness: the outdoor items that make the place read right. **Core** = always there; **flavour** = sometimes (region, wealth, season). Names are kit families; §2 has the entries behind them and §5 counts how often each recurs. BL buildings are not listed.

### Rice-farming village (hirachi no mura)
*BL §2.1.* Kinai: add rapeseed/cotton fields, tame-ike, treadwheels, kanjō-nawa. Kantō: windbreak groves, family graves at field edges.

- **Core:** Flat paddy (irregular plots) · Paddy bunds with soybeans · Irrigation channel + sluice + water notch · Stone-lined village channel with wash steps · Well, pulley or lever (tsurube-ido / hanetsurube) · Well-god offering · Persimmon tree · Bamboo grove · Rice-drying rack (hasa) · Straw stack / sheaf stack · Threshing yard + harvest tool set · Drying mats on the ground · Hanging produce (persimmons, daikon, chillies, seed bags) · Pickle barrels with weight stones · Firewood stack · Brushwood / thatch bundles · Compost / manure heap · Night-soil buckets and pole · Tools under the eaves (hoes, sickles, flail) · Bench (shōgi / endai) · Laundry pole · Wash tubs + buckets drying on stakes · Post gate / wicket gate · Brushwood fence (shiba-gaki) · Live hedge (ikegaki) · Scarecrow · Bird-clapper line (naruko) · Roadside Jizō (+ Jizō hut) · Dōsojin (character / couple / round-stone) · Kōshin stone / mound · Water-god stone · Yard shrine + mini torii + offering stand · Wooden torii · Stone lantern pair / approach lanterns · Purification basin (chōzubachi) + ladle · Sacred tree with shimenawa · Shrine approach (sandō) · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Six-Jizō row · Village boundary post / stone · Plank bridge · Stone slab bridge · Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires)
- **Flavour:** Terraced paddy (stone or earth risers) · Irrigation pond (tame-ike) + outlet · Water lifting: field sweep / treadwheel · River weir / brushwood weir · Kitchen garden + vegetable stakes · Gourd trellis · Ume tree / grove · Tea bushes on field edges · Cash-crop field (cotton / rapeseed / indigo / hemp / tobacco) · Farmstead windbreak grove (yashiki-rin) · Rice bales stacked · Communal well (mura-ido / idobata) · Stone torii · Komainu pair · Strength stones · Pond with Benten islet · Village boundary rope (kanjō-nawa) · Crossbar gate with small roof (kabuki-mon) · Board fence (itabei) · Boar wall / bank / brush fence · Loose hens · Fire basket / watch fire (kagari) · Festival layer (nobori, lanterns, mikoshi, stages) · Notice board (kōsatsuba, BL site) · Gorintō / hōkyōin-tō · Nenbutsu / daimoku stone · Batō Kannon · Stone steps

### New-field village (shinden-mura)
*BL §2.2.* Straight road, identical plots; deep wells on the dry plateau; new small shrine, often no temple yet. Very 1720s–30s.

- **Core:** Dry-field ridges + crop proxies · Farmstead windbreak grove (yashiki-rin) · Well, pulley or lever (tsurube-ido / hanetsurube) · Well curb and lid · Persimmon tree · Kitchen garden + vegetable stakes · Firewood stack · Brushwood / thatch bundles · Compost / manure heap · Tools under the eaves (hoes, sickles, flail) · Straw bundles in stooks · Threshing yard + harvest tool set · Post gate / wicket gate · Brushwood fence (shiba-gaki) · Yard shrine + mini torii + offering stand · Village boundary post / stone · Dōsojin (character / couple / round-stone) · Bench (shōgi / endai) · Laundry pole · Wash tubs + buckets drying on stakes
- **Flavour:** Flat paddy (irregular plots) · Mulberry bushes · Cash-crop field (cotton / rapeseed / indigo / hemp / tobacco) · Wooden torii · Roadside Jizō (+ Jizō hut) · Kōshin stone / mound · Tea bushes on field edges · Bamboo grove · Grass-cutting commons

### Mountain village (sanson)
*BL §2.3.* Stepped houses on stone-walled terraces; water by bamboo pipe; the forest edge starts at the yama-no-kami stone.

- **Core:** Terraced paddy (stone or earth risers) · Dry-stone wall (plots, terraces, road shelves) · Dry-field ridges + crop proxies · Bamboo pipe / piped spring (kakehi) · Firewood stack · Brushwood / thatch bundles · Charcoal bales · Persimmon tree · Bamboo grove · Mountain-god stone / hokora · Roadside Jizō (+ Jizō hut) · Batō Kannon · Tools under the eaves (hoes, sickles, flail) · Carrying frame (shoiko) · Sledge (sori) · Boar wall / bank / brush fence · Bird-clapper line (naruko) · Log bridge · Stepping stones across water · Rice-drying rack (hasa) · Straw stack / sheaf stack · Hanging produce (persimmons, daikon, chillies, seed bags) · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Bench (shōgi / endai) · Laundry pole · Wash tubs + buckets drying on stakes
- **Flavour:** Swidden plot · Grass-cutting commons · Mulberry bushes · Cash-crop field (cotton / rapeseed / indigo / hemp / tobacco) · Log beehive · Charcoal kiln + kiln ruins · Shiitake log stack · Log deck / timber chute / sledge track · Forest markers (tomeyama stakes, brands, claim stakes, notice board) · Sacred tree with shimenawa · Wooden torii · Shrine approach (sandō) · Stone steps · Fire basket / watch fire (kagari) · Hunting kit (blind, snares, deadfall, pit trap) · Fish weir (yana) / basket traps · Cantilever / vine bridge · Dōsojin (character / couple / round-stone) · Kōshin stone / mound · Spring pool with stone surround · Stone lantern pair / approach lanterns

### Fishing village (gyoson / ura)
*BL §2.4.* Houses packed gable-end to the sea; boats on the beach; a steep path up to shrine and temple on the headland.

- **Core:** Beached boats + skids + capstan · Net-drying rack · Fish-drying racks / sardines on the beach · Seaweed drying · Shore clutter (floats, sinkers, traps, pots, anchors, oars) · Driftwood stacks · Ebisu stone · Laundry pole · Well, pulley or lever (tsurube-ido / hanetsurube) · Firewood stack · Pickle barrels with weight stones · Wash tubs + buckets drying on stakes · Shoulder pole and loads (tenbin-bō) · Stone steps · Wooden torii · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Roadside Jizō (+ Jizō hut) · Reed fence / yoshizu screens · Sand fence · Bench (shōgi / endai)
- **Flavour:** Coastal pine shelterbelt · Harbour / beach guide fire · Shell heap and lime pit · Divers' tubs and beach fire ring · Small stone jetty / boat slip · Drowned-sailor / tsunami memorial · Stone lantern pair / approach lanterns · Nori stakes + drying frames · Fire basket / watch fire (kagari) · Sea torii · Sacred rock (iwakura) · Purification basin (chōzubachi) + ladle · Kōshin stone / mound · Dry-field ridges + crop proxies · Persimmon tree

### Salt village (coast variant)
*R §16; BL Rural industry.* Keep one salt-field type (tidal irihama on the Kinai side) unless the Kantō coast needs the spread type.

- **Core:** Salt field + filter pit + salt tools · Fuel stacks for salt boiling · Salt bales · Well, pulley or lever (tsurube-ido / hanetsurube) · Shoulder pole and loads (tenbin-bō) · Firewood stack · Sand fence · Ebisu stone · Graveyard kit (stones, sotoba, buckets, flower tubes, incense)
- **Flavour:** Beached boats + skids + capstan · Net-drying rack · Shore clutter (floats, sinkers, traps, pots, anchors, oars) · Coastal pine shelterbelt · Persimmon tree · Bench (shōgi / endai)

### Post town (shukuba-machi)
*BL §2.5.* One house deep along the road; stables and kura behind; tea houses and smithy at the ends; banks and a bend at each end.

- **Core:** Earth street with gutters and slab crossings · Roadside ditch / street gutter · Stone slab bridge · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Bench (shōgi / endai) · Reed screens (yoshizu) at stands · Horse / animal trough (mizu-bune) · Hitching post / tie stone · Foot-washing tubs at inn doors · Horse droppings · Road litter (horse droppings, cast sandals and horse shoes) · Well, pulley or lever (tsurube-ido / hanetsurube) · Corner fire tub with bucket pyramid + eave buckets · Post-town end bank and bend (mitsuke / masugata) · Notice board (kōsatsuba, BL site) · Direction stone / wooden signpost · Roadside Jizō (+ Jizō hut) · Kōshin stone / mound · Road-repair / procession sand heaps · Palanquin (tsuji-kago / norimono) · Shoulder pole and loads (tenbin-bō) · Firewood stack · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Wooden torii · Stone lantern pair / approach lanterns · Purification basin (chōzubachi) + ladle · Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires) · Rain barrel / water jar
- **Flavour:** Fire-bell ladder (hanshō-dai) · Always-lit lantern (jōyatō) · Crossroads lamp (tsuji-andon) · Night-watch clappers · Stall family (yoshizu stall, yatai, kake-mise) · Board fence (itabei) · Live hedge (ikegaki) · Potted-plant shelves · Handcart (daihachi / niguruma) · Post gate / wicket gate · Six-Jizō row · Batō Kannon · Festival layer (nobori, lanterns, mikoshi, stages) · Ward gate (kido, BL) + gate lantern · Plank bridge · Mile mound pair (ichirizuka) · Pine avenue (matsu-namiki) · Cedar avenue (sugi-namiki) · Stone-paved pass road (ishidatami) · Sitting stone (koshikake-ishi) · Stone torii · Sacred tree with shimenawa · Stone steps · Laundry pole · Wash tubs + buckets drying on stakes

### Intermediate stop (ai-no-shuku, tateba)
*BL §2.6.* 5–30 houses of tea stalls and a rest yard; a horse trough and a Jizō or Batō Kannon are the tells.

- **Core:** Bench (shōgi / endai) · Reed screens (yoshizu) at stands · Horse / animal trough (mizu-bune) · Hitching post / tie stone · Foot-washing tubs at inn doors · Roadside Jizō (+ Jizō hut) · Road litter (horse droppings, cast sandals and horse shoes) · Horse droppings · Firewood stack · Well, pulley or lever (tsurube-ido / hanetsurube) · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon)
- **Flavour:** Batō Kannon · Open rain shelter (azumaya) · Sitting stone (koshikake-ishi) · Direction stone / wooden signpost · Bamboo pipe / piped spring (kakehi) · Sacred tree with shimenawa · Hokora micro-shrine (BL site) · Stall family (yoshizu stall, yatai, kake-mise) · Sandal-hanging tree / pass offering heap

### Castle town (jōkamachi)
*BL §2.7.* Zones: castle core behind moats and ishigaki; walled samurai streets; townsmen's street of shop fronts; temple row at the edge; kido gates and cranked streets.

- **Core:** Wet moat · Castle stone walls (ishigaki) · Loopholed earthen wall (dobei) · Masugata gate plaza · Earth rampart with pines · Samurai-quarter frontage (nagaya-mon, black board walls) · Capped earth wall (tsuiji / dobei) · Board fence (itabei) · Earth street with gutters and slab crossings · Roadside ditch / street gutter · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Corner fire tub with bucket pyramid + eave buckets · Fire-bell ladder (hanshō-dai) · Ward gate (kido, BL) + gate lantern · Night-watch clappers · Notice board (kōsatsuba, BL site) · Well, pulley or lever (tsurube-ido / hanetsurube) · Plank bridge · Earth-covered bridge (dobashi) · Fire basket / watch fire (kagari) · Stone torii · Vermilion torii (Inari) · Stone lantern pair / approach lanterns · Komainu pair · Purification basin (chōzubachi) + ladle · Offering box (saisen-bako) · Hall bell or gong with rope · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Gorintō / hōkyōin-tō · Stone steps · Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires) · Bench (shōgi / endai) · Shoulder pole and loads (tenbin-bō) · Firewood stack · Laundry pole
- **Flavour:** Horse ground / archery butt · Courtyard garden kit (lantern, basin, stones) · Stroll garden kit (pond, islands, lanterns, bridges) · Dry garden (raked gravel, stone groups) · Canal-edge kit (stone wall, gangi steps, mooring stones) · Moored boats (chokibune, yanebune, cargo boats) · Stall family (yoshizu stall, yatai, kake-mise) · Peddler kits · Periodic market set · Festival layer (nobori, lanterns, mikoshi, stages) · Palanquin (tsuji-kago / norimono) · Handcart (daihachi / niguruma) · Potted-plant shelves · Always-lit lantern (jōyatō) · Crossroads lamp (tsuji-andon) · Great incense burner (jōkōro) · Stone Buddha / stone Buddha rows · Inscribed stele / memorial stupa · Votive plaque rack (ema-kake) · Kōshin stone / mound · Roadside Jizō (+ Jizō hut) · Six-Jizō row · Live hedge (ikegaki) · Kenninji fence · Execution-ground memorial stones · Rain barrel / water jar

### Jinya town (jinya-machi)
*BL §2.8.* A big post town with one walled government compound on a slight rise; no moat or ishigaki (Takayama is the survivor).

- **Core:** Capped earth wall (tsuiji / dobei) · Board fence (itabei) · Samurai-quarter frontage (nagaya-mon, black board walls) · Earth street with gutters and slab crossings · Roadside ditch / street gutter · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Corner fire tub with bucket pyramid + eave buckets · Notice board (kōsatsuba, BL site) · Well, pulley or lever (tsurube-ido / hanetsurube) · Wooden torii · Stone lantern pair / approach lanterns · Purification basin (chōzubachi) + ladle · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Roadside Jizō (+ Jizō hut) · Bench (shōgi / endai) · Firewood stack · Shoulder pole and loads (tenbin-bō) · Laundry pole
- **Flavour:** Live hedge (ikegaki) · Fire-bell ladder (hanshō-dai) · Stall family (yoshizu stall, yatai, kake-mise) · Periodic market set · Festival layer (nobori, lanterns, mikoshi, stages) · Kōshin stone / mound · Plank bridge · Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires)

### Great city: Edo, Kyoto, Osaka
*BL §2.9.* Edo: canals, bridge-end plazas, hirokōji, alley wells and Inari, kido at every ward. Kyoto: zushi lanes, inuyarai, corner Jizō boxes, the Kamo riverbed. Osaka: canals, hama frontages, ~200 townsmen's bridges. Keeps absent at Edo and Osaka.

- **Core:** Earth street with gutters and slab crossings · Roadside ditch / street gutter · Stone slab bridge · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Ward gate (kido, BL) + gate lantern · Night-watch clappers · Corner fire tub with bucket pyramid + eave buckets · Fire-bell ladder (hanshō-dai) · Alley drain boards (dobu-ita) · Alley rubbish box · Communal well (mura-ido / idobata) · Well-god offering · Laundry pole · Potted-plant shelves · Peddler kits · Stall family (yoshizu stall, yatai, kake-mise) · Handcart (daihachi / niguruma) · Palanquin (tsuji-kago / norimono) · Shoulder pole and loads (tenbin-bō) · Canal-edge kit (stone wall, gangi steps, mooring stones) · Moored boats (chokibune, yanebune, cargo boats) · Plank bridge · Great wooden trestle bridge + bridge-end plaza · Wash steps into stream or canal (arai-ba) · Notice board (kōsatsuba, BL site) · Direction stone / wooden signpost · Vermilion torii (Inari) · Yard shrine + mini torii + offering stand · Stone torii · Stone lantern pair / approach lanterns · Komainu pair · Purification basin (chōzubachi) + ladle · Offering box (saisen-bako) · Hall bell or gong with rope · Votive plaque rack (ema-kake) · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Great incense burner (jōkōro) · Horse droppings · Periodic market set · Festival layer (nobori, lanterns, mikoshi, stages) · Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires) · Rain barrel / water jar · Night-soil buckets and pole · Bench (shōgi / endai) · Firewood stack
- **Flavour:** Kamigata street fixtures (battari-shōgi, inuyarai) · Crossroads lamp (tsuji-andon) · Always-lit lantern (jōyatō) · Courtyard garden kit (lantern, basin, stones) · Stroll garden kit (pond, islands, lanterns, bridges) · Dry garden (raked gravel, stone groups) · Wet moat · Castle stone walls (ishigaki) · Samurai-quarter frontage (nagaya-mon, black board walls) · Capped earth wall (tsuiji / dobei) · Horse ground / archery butt · Execution-ground memorial stones · Stone Buddha / stone Buddha rows · Inscribed stele / memorial stupa · Roadside Jizō (+ Jizō hut) · Six-Jizō row · Gorintō / hōkyōin-tō · Nori stakes + drying frames · Log raft · Channel stakes (miotsukushi)

### Temple town / shrine-gate town (monzen-machi)
*BL §2.10.* One approach street climbing to the gate, lined with pilgrim trade; sub-temples and graveyards on side streets. Ise in 1730: brand-new 1729 shrines beside bare alternate sites.

- **Core:** Shrine approach (sandō) · Stone steps · Stone torii · Stone lantern pair / approach lanterns · Komainu pair · Purification basin (chōzubachi) + ladle · Offering box (saisen-bako) · Hall bell or gong with rope · Votive plaque rack (ema-kake) · Great incense burner (jōkōro) · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Stall family (yoshizu stall, yatai, kake-mise) · Bench (shōgi / endai) · Reed screens (yoshizu) at stands · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Gorintō / hōkyōin-tō · Six-Jizō row · Stone Buddha / stone Buddha rows · Pilgrim-club stone (kō-hi) · Banner-pole socket stones · Earth street with gutters and slab crossings · Festival layer (nobori, lanterns, mikoshi, stages) · Sacred tree with shimenawa · Well, pulley or lever (tsurube-ido / hanetsurube) · Shoulder pole and loads (tenbin-bō)
- **Flavour:** Periodic market set · Peddler kits · Vermilion torii (Inari) · Pond with Benten islet · Inscribed stele / memorial stupa · Nenbutsu / daimoku stone · Sutra mound · Always-lit lantern (jōyatō) · Crossroads lamp (tsuji-andon) · Corner fire tub with bucket pyramid + eave buckets · Well, pulley or lever (tsurube-ido / hanetsurube) · Palanquin (tsuji-kago / norimono) · Potted-plant shelves · Dry garden (raked gravel, stone groups) · Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires) · Strength stones · Laundry pole

### Port town (minato-machi)
*BL §2.11.* Streets parallel to the shore, lanes at right angles; stone quays (gangi) and mooring stones; a weather hill with a direction stone behind; lighthouse lantern on the point.

- **Core:** Canal-edge kit (stone wall, gangi steps, mooring stones) · Moored boats (chokibune, yanebune, cargo boats) · Rice bales stacked · Shoulder pole and loads (tenbin-bō) · Earth street with gutters and slab crossings · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Well, pulley or lever (tsurube-ido / hanetsurube) · Corner fire tub with bucket pyramid + eave buckets · Lighthouse lantern (tōmyōdō) · Beached boats + skids + capstan · Shore clutter (floats, sinkers, traps, pots, anchors, oars) · Net-drying rack · Ebisu stone · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Wooden torii · Stone lantern pair / approach lanterns · Purification basin (chōzubachi) + ladle · Notice board (kōsatsuba, BL site) · Bench (shōgi / endai) · Firewood stack · Laundry pole
- **Flavour:** Small stone jetty / boat slip · Channel stakes (miotsukushi) · Harbour / beach guide fire · Drowned-sailor / tsunami memorial · Wreck debris / stranded ship · Fish-drying racks / sardines on the beach · Stall family (yoshizu stall, yatai, kake-mise) · Periodic market set · Handcart (daihachi / niguruma) · Festival layer (nobori, lanterns, mikoshi, stages) · Always-lit lantern (jōyatō) · Coastal pine shelterbelt · Stone steps

### Mining town (kōzan-machi)
*BL §2.12.* Narrow valley town: magistrate's compound, sorting sheds, row houses, temples up the slopes, adit mouths above. Past peak by 1730.

- **Core:** Mine adit + spoil heap + drainage · Dry-stone wall (plots, terraces, road shelves) · Firewood stack · Charcoal bales · Bamboo pipe / piped spring (kakehi) · Tools under the eaves (hoes, sickles, flail) · Carrying frame (shoiko) · Mountain-god stone / hokora · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Earth street with gutters and slab crossings · Well, pulley or lever (tsurube-ido / hanetsurube) · Stone steps · Bench (shōgi / endai)
- **Flavour:** Charcoal kiln + kiln ruins · Log deck / timber chute / sledge track · Sledge (sori) · Capped earth wall (tsuiji / dobei) · Notice board (kōsatsuba, BL site) · Roadside Jizō (+ Jizō hut) · Inscribed stele / memorial stupa · Abandoned hamlet / farmstead / hut

### River-crossing town
*BL §2.13.* Stations where bridges were forbidden (Ōi River: Shimada, Kanaya): a worn gravel bank with porter shelters and platforms; extra inns for kawa-dome stranding.

- **Core:** Earth street with gutters and slab crossings · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Bench (shōgi / endai) · Horse / animal trough (mizu-bune) · Hitching post / tie stone · Foot-washing tubs at inn doors · Horse droppings · Notice board (kōsatsuba, BL site) · Roadside Jizō (+ Jizō hut) · River works (gabions, crib spurs, groynes) · Ferry landing + bell post (BL site) · Corner fire tub with bucket pyramid + eave buckets · Well, pulley or lever (tsurube-ido / hanetsurube) · Firewood stack · Shoulder pole and loads (tenbin-bō)
- **Flavour:** Stall family (yoshizu stall, yatai, kake-mise) · Water-god stone · Traveller's grave / horse grave · Inscribed stele / memorial stupa · Palanquin (tsuji-kago / norimono) · River weir / brushwood weir · Log raft · Laundry pole

### Hot-spring town (onsen-machi)
*BL §2.14.* Bath inns round a public bath and the spring's shrine / Yakushi hall; hot-water gutters and bamboo pipes; steam.

- **Core:** Hot-spring troughs / wild riverside hot pool · Bamboo pipe / piped spring (kakehi) · Earth street with gutters and slab crossings · Shop front kit (noren, kanban, shape signs, sudare) · Shop and inn lanterns / sign lamps (kake-andon) · Bench (shōgi / endai) · Stone steps · Wooden torii · Stone lantern pair / approach lanterns · Purification basin (chōzubachi) + ladle · Foot-washing tubs at inn doors · Firewood stack · Well, pulley or lever (tsurube-ido / hanetsurube) · Wash tubs + buckets drying on stakes
- **Flavour:** Sulphur workings + hell-valley Jizō · Stone Buddha / stone Buddha rows · Stall family (yoshizu stall, yatai, kake-mise) · Palanquin (tsuji-kago / norimono) · Fudō stone · Sacred rock (iwakura) · Roadside Jizō (+ Jizō hut) · Open rain shelter (azumaya) · Laundry pole

### Outcast and marginal settlements (neutral)
*BL §2.15.* Ordinary houses and yards on river flats outside the townsmen's area; hinin huts near bridges and riverbeds. Handle neutrally.

- **Core:** Earth street with gutters and slab crossings · Well, pulley or lever (tsurube-ido / hanetsurube) · Firewood stack · Wash tubs + buckets drying on stakes · Laundry pole · Graveyard kit (stones, sotoba, buckets, flower tubes, incense) · Tools under the eaves (hoes, sickles, flail) · Reed fence / yoshizu screens
- **Flavour:** Execution-ground memorial stones · Open rain shelter (azumaya) · Abandoned hamlet / farmstead / hut · Roadside Jizō (+ Jizō hut) · Wooden torii · Night-soil buckets and pole · Stall family (yoshizu stall, yatai, kake-mise)

### Highway between towns
*W §1–3, §21.* Tōkaidō on the plains: pine avenue and mounds; Hakone section: cedar avenue and 1680 paving; tea stalls (BL) every few km with their bench-and-trough spill.

- **Core:** Pine avenue (matsu-namiki) · Mile mound pair (ichirizuka) · Direction stone / wooden signpost · Roadside Jizō (+ Jizō hut) · Batō Kannon · Kōshin stone / mound · Roadside ditch / street gutter · Road litter (horse droppings, cast sandals and horse shoes) · Horse droppings · Bench (shōgi / endai) · Horse / animal trough (mizu-bune) · Bamboo pipe / piped spring (kakehi) · Travellers' fire ring · Traveller's grave / horse grave · Log bridge · Plank bridge · Earth-covered bridge (dobashi) · Stepping stones across water · Sitting stone (koshikake-ishi)
- **Flavour:** Cedar avenue (sugi-namiki) · Stone-paved pass road (ishidatami) · Switchbacks / log steps / cross drains · Open rain shelter (azumaya) · Always-lit lantern (jōyatō) · Crossroads lamp (tsuji-andon) · Pass-top Jizō + offering heap · Sandal-hanging tree / pass offering heap · Pass name post / province post · Province / domain boundary post · Ferry landing + bell post (BL site) · Road-repair / procession sand heaps · Bandit lair / ambush screen · Execution-ground memorial stones · Checkpoint palisade + bypass warning board · Cliff Buddhas (magaibutsu) · Sacred tree with shimenawa · Hokora micro-shrine (BL site) · Pilgrim-club stone (kō-hi) · Village boundary post / stone · Village boundary rope (kanjō-nawa) · Dōsojin (character / couple / round-stone) · Six-Jizō row · Gorintō / hōkyōin-tō · Cliff plank road (kakehashi) · River works (gabions, crib spurs, groynes) · Hōei ash heaps / ash-buried fields · Landslide scar with Jizō

### Deep wilderness: mountain and forest
*W §6–16.* Sparse on purpose: one worked thing per valley (a kiln, a log deck, a shrine) reads better than scatter.

- **Core:** Charcoal kiln + kiln ruins · Firewood stack · Charcoal bales · Mountain-god stone / hokora · Cairns and blazes · Switchbacks / log steps / cross drains · Woodsman's lean-to / bough bivouac · Rock overhang camp · Hunting kit (blind, snares, deadfall, pit trap) · Forest markers (tomeyama stakes, brands, claim stakes, notice board) · Log bridge · Stepping stones across water
- **Flavour:** Log deck / timber chute / sledge track · Sawpit and whipsaw trestle · Shiitake log stack · Log beehive · Swidden plot · Grass-cutting commons · Pass-top Jizō + offering heap · Summit / pass shrine (BL site) + windbreak wall · Numbered mountain-path torii / lone forest torii · Waterfall ascetic site · Fudō stone · Sacred rock (iwakura) · Sacred tree with shimenawa · Castle-ruin earthworks (horikiri, dorui, kuruwa) · Abandoned hamlet / farmstead / hut · Old well in the woods · Gorintō / hōkyōin-tō · Tomb mounds (kofun) with hokora · Mine adit + spoil heap + drainage · Quarry blocks (marked, abandoned) · Hot-spring troughs / wild riverside hot pool · Sulphur workings + hell-valley Jizō · Bandit lair / ambush screen · Cantilever / vine bridge · Cliff plank road (kakehashi) · Fish weir (yana) / basket traps · Log raft · River works (gabions, crib spurs, groynes) · Boar wall / bank / brush fence · Cliff Buddhas (magaibutsu) · Landslide scar with Jizō · Hōei ash heaps / ash-buried fields · Traveller's grave / horse grave · Hokora micro-shrine (BL site)

### Deep wilderness: empty coast and river
*W §4, §19–20.* Wild-coast items only count as W away from a village; in a fishing village the same objects belong to R.

- **Core:** Driftwood stacks · Shore clutter (floats, sinkers, traps, pots, anchors, oars) · Harbour / beach guide fire · Ebisu stone · Drowned-sailor / tsunami memorial · Stepping stones across water · Fish weir (yana) / basket traps
- **Flavour:** Wreck debris / stranded ship · Lighthouse lantern (tōmyōdō) · Sea torii · Small stone jetty / boat slip · Divers' tubs and beach fire ring · Shell heap and lime pit · Sand fence · Coastal pine shelterbelt · Salt field + filter pit + salt tools · Channel stakes (miotsukushi) · Ferry landing + bell post (BL site) · Log raft · River works (gabions, crib spurs, groynes) · Rock overhang camp · Beached boats + skids + capstan · Net-drying rack

---

# 5. Shared outdoor core kit

Items that recur across the 19 setting kits of §4, most-used first: the "build once, reuse everywhere" list. Count = settings that use it (core + flavour). Only items used in 4 or more settings are shown; the rest are setting-specific.

| # | Item | Settings (of 19) | Core in | Flavour in |
|---|---|---|---|---|
| 1 | Firewood stack | 16 | 16 | 0 |
| 2 | Bench (shōgi / endai) | 16 | 15 | 1 |
| 3 | Well, pulley or lever (tsurube-ido / hanetsurube) | 15 | 14 | 1 |
| 4 | Roadside Jizō (+ Jizō hut) | 14 | 8 | 6 |
| 5 | Laundry pole | 13 | 9 | 4 |
| 6 | Graveyard kit (stones, sotoba, buckets, flower tubes, incense) | 12 | 12 | 0 |
| 7 | Earth street with gutters and slab crossings | 10 | 10 | 0 |
| 8 | Stone lantern pair / approach lanterns | 10 | 8 | 2 |
| 9 | Stall family (yoshizu stall, yatai, kake-mise) | 10 | 2 | 8 |
| 10 | Shop and inn lanterns / sign lamps (kake-andon) | 9 | 9 | 0 |
| 11 | Shop front kit (noren, kanban, shape signs, sudare) | 9 | 9 | 0 |
| 12 | Shoulder pole and loads (tenbin-bō) | 9 | 9 | 0 |
| 13 | Purification basin (chōzubachi) + ladle | 9 | 8 | 1 |
| 14 | Wooden torii | 9 | 6 | 3 |
| 15 | Stone steps | 9 | 5 | 4 |
| 16 | Notice board (kōsatsuba, BL site) | 8 | 6 | 2 |
| 17 | Kōshin stone / mound | 8 | 3 | 5 |
| 18 | Corner fire tub with bucket pyramid + eave buckets | 7 | 6 | 1 |
| 19 | Wash tubs + buckets drying on stakes | 7 | 6 | 1 |
| 20 | Festival layer (nobori, lanterns, mikoshi, stages) | 7 | 2 | 5 |
| 21 | Sacred tree with shimenawa | 7 | 2 | 5 |
| 22 | Plank bridge | 6 | 4 | 2 |
| 23 | Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires) | 6 | 4 | 2 |
| 24 | Gorintō / hōkyōin-tō | 6 | 2 | 4 |
| 25 | Palanquin (tsuji-kago / norimono) | 6 | 2 | 4 |
| 26 | Six-Jizō row | 6 | 2 | 4 |
| 27 | Always-lit lantern (jōyatō) | 6 | 0 | 6 |
| 28 | Horse droppings | 5 | 5 | 0 |
| 29 | Roadside ditch / street gutter | 5 | 5 | 0 |
| 30 | Tools under the eaves (hoes, sickles, flail) | 5 | 5 | 0 |
| 31 | Bamboo pipe / piped spring (kakehi) | 5 | 4 | 1 |
| 32 | Persimmon tree | 5 | 3 | 2 |
| 33 | Stone torii | 5 | 3 | 2 |
| 34 | Batō Kannon | 5 | 2 | 3 |
| 35 | Periodic market set | 5 | 1 | 4 |
| 36 | Crossroads lamp (tsuji-andon) | 5 | 0 | 5 |
| 37 | Inscribed stele / memorial stupa | 5 | 0 | 5 |
| 38 | Ebisu stone | 4 | 4 | 0 |
| 39 | Foot-washing tubs at inn doors | 4 | 4 | 0 |
| 40 | Horse / animal trough (mizu-bune) | 4 | 4 | 0 |
| 41 | Stepping stones across water | 4 | 4 | 0 |
| 42 | Direction stone / wooden signpost | 4 | 3 | 1 |
| 43 | Komainu pair | 4 | 3 | 1 |
| 44 | Shore clutter (floats, sinkers, traps, pots, anchors, oars) | 4 | 3 | 1 |
| 45 | Beached boats + skids + capstan | 4 | 2 | 2 |
| 46 | Board fence (itabei) | 4 | 2 | 2 |
| 47 | Capped earth wall (tsuiji / dobei) | 4 | 2 | 2 |
| 48 | Dōsojin (character / couple / round-stone) | 4 | 2 | 2 |
| 49 | Fire-bell ladder (hanshō-dai) | 4 | 2 | 2 |
| 50 | Net-drying rack | 4 | 2 | 2 |
| 51 | Fire basket / watch fire (kagari) | 4 | 1 | 3 |
| 52 | Handcart (daihachi / niguruma) | 4 | 1 | 3 |
| 53 | Live hedge (ikegaki) | 4 | 1 | 3 |
| 54 | Potted-plant shelves | 4 | 1 | 3 |
| 55 | River works (gabions, crib spurs, groynes) | 4 | 1 | 3 |
| 56 | Stone Buddha / stone Buddha rows | 4 | 1 | 3 |
| 57 | Coastal pine shelterbelt | 4 | 0 | 4 |
| 58 | Execution-ground memorial stones | 4 | 0 | 4 |
| 59 | Log raft | 4 | 0 | 4 |
| 60 | Open rain shelter (azumaya) | 4 | 0 | 4 |

**Reading it.** The top of the table is one small family of parts: benches, lanterns, stone figures and inscribed stones, buckets and tubs, stone steps, bamboo and brush fences, straw bundles and stacks, fire baskets. Built as kits (§7.5, 7.7, 7.10, 7.11) with swappable loads and text decals, they dress almost every setting. Everything below the cut belongs to one or two settings and can wait.

---

# 6. Period traps

Things people assume are "Edo" but are wrong for 1730, from all four files. "Date" is when the thing arrived (or
when it vanished); "Use instead" is the in-period alternative. Where an agent only flagged it `(verify)`, so does this
table.

**Landscape and plants**

| Trap | Real date | Use instead (1730) | From |
|---|---|---|---|
| Dense, dark, overgrown woods round villages | modern Japan's look; 1730 hills near people were over-cut and open | open red-pine woods, coppice patchwork, grass-cutting commons, raked clean floors; dark forest only high up and in shrine groves | N |
| Cedar plantations on every slope | planting only spreading through the 1700s; far less than today | mixed coppice and red pine; plantations only near timber towns and rafting rivers | N, W |
| Somei-yoshino cherry | bred c. 1840s–60s | yamazakura (flowers with red-brown leaves), edohigan, Oshima cherry; double satozakura in towns | N |
| Mōsō (fat) bamboo groves | Satsuma 1736, central Honshū later | madake and hachiku groves | N |
| Clipped tea rows | Meiji, from 1869 (Makinohara) | loose tea bushes along bunds and field edges | N, R |
| Rectangular paddy grid | Meiji, 1899 law (verify) | irregular paddies following the ground | R |
| Coloured patterned koi (nishikigoi) | Bunka–Bunsei, 1804–30; national after 1914 | plain grey-black magoi and crucian carp | U, N |
| Goldfish in glass bowls | 19th c. (verify) | goldfish in wooden tubs and glazed basins | U |
| Yukitsuri rope cones on garden pines | ornamental form Meiji (Kenroku-en) | plain bamboo props, straw snow shelters; farm fruit-tree propping | U |
| Iris-garden displays (hanashōbu, Horikiri) | late 18th–19th c. | wild ayame, kakitsubata, shaga; zigzag-bridge iris beds in daimyō gardens | N, U |
| Larch plantations (Nagano) | Meiji | wild larch only high on Fuji and Asama | N |
| Tree-of-heaven, false acacia, sophora street trees | Meiji plantings | keyaki, enoki, ginkgo, willow (eniju only at temples) | N |
| Western apple | Meiji | rare wakaringo; persimmon is the village fruit | N |
| Chinese cabbage, cabbage, tomato, onion | Meiji | daikon, turnip, komatsuna, negi | N |
| Peanut fields | brought early 1700s, grown seriously from Meiji | soy and azuki | N |
| Sweet-potato fields on our map | Kantō trials from 1735 | taro, millet, hie, famine foods | N, R |
| Nozawana greens | tradition 1756 | turnip and Kiso sunki | N |
| Powdered konnyaku | 1776 process | fresh konnyaku from corms | N |
| Paddy carp farming (Saku koi) | tradition 1746 (verify) | drab carp in farm ponds | R |
| Gyokuro shaded tea | 1835 | Uji ōishita shaded tea gardens (the shading is older) | R |
| "Ōwakudani" as a name | renamed 1873 | Ōjigoku / Jigokudani | N, W |
| Asama's great eruption | 1783 | a smoking Asama on the skyline is fine | N |

**Village, yard and field props**

| Trap | Real date | Use instead (1730) | From |
|---|---|---|---|
| Tanuki with a sake flask (Shigaraki tanuki) | 1930s–50s | nothing; real tanuki are fauna | R |
| Beckoning cat (maneki-neko) | c. 1850s (Imado ware, Asakusa) | shape signs (katachi-kanban) for shops | R |
| Fukusuke figure | c. 1800s | none | R |
| Papier-mâché Daruma dolls | Takasaki, 1780s–90s (verify) | none | R |
| Kappa and frog statues | modern | none | R |
| Carp streamers (koinobori) | mid-to-late 18th c. (verify) | warrior-picture banners (musha-e nobori) and plain fukinagashi streamers | R, U |
| Stone Inari foxes | mostly after mid-18th c.; Ōji Inari pair 1764 | small wooden or ceramic foxes, or none | R (U disagrees, §3.3) |
| Village fire-watch towers and ladders | rural: Meiji–Shōwa | alarm bell on a frame or tree; clappers; conch | R |
| Ridged washboard | Meiji (verify) | tarai tub; clothes trodden or rubbed by hand | R |
| Wheelbarrow | late Edo–Meiji (verify) | shoulder pole, carrying frame, sledge, packhorse | R |
| Glass fishing floats | Meiji | wooden and bamboo floats, clay and stone sinkers | R |
| "X family grave" inscriptions | Meiji | individual boat-halo and slab stones | R, U |
| Paired dōsojin everywhere | mostly 1804–30 | mostly character dōsojin; a few couples | R, W |
| Tokuhon-style nenbutsu stones | c. 1800 | plain myōgō stones | R |
| Miniature 88-temple circuits | mostly 19th c. | a few 33-Kannon copies (contested, §3.3) | R, W, U |
| Pilgrim Fuji mounds (Fuji-zuka) | 1779 / 1780, Takata | none; Fuji-kō only spreads after 1733 | R, U |
| Ontake-kō pilgrim stones | lay climbing from 1785 | Ōyama-kō and Ise-kō stones | W, R |
| Tenmei famine memorials | 1780s | Kyōhō famine stones (1732–33, just after the anchor) | W |
| Permanent village kabuki stage | late 18th–19th c. (verify) | temporary plank stage (kari-butai) | R |
| Tall central bon-odori tower | poorly attested before late Edo (verify) | singer and drum on a bench or low stand | R, U |
| Omikuji tied to branches | probably later (verify) | slips kept, not tied | R, U |
| Stacked decorated sake-cask walls | likely later (verify) | a few offered barrels | R, U |
| Shrine-name stone pillars, donor-name stone fences | mostly Meiji+ (verify) | wooden fences; names on lanterns and torii | R (U disagrees) |
| Asakura triple water wheel | 1789, off-map | treadwheel, river lift wheel | R |

**Town, garden and road props**

| Trap | Real date | Use instead (1730) | From |
|---|---|---|---|
| A rain / fire tub (tensui-oke) at every house | general from Kansei, 1789–1801 | big corner tubs with bucket pyramids; buckets hung at the eaves | U |
| Hand fire pump (ryūdosui) | sold ~1751, issued 1764 | buckets, fire hooks, ladders, wet mats | U |
| Giant red lantern under a temple gate | Sensō-ji Kaminarimon, 1795 (verify) | smaller hanging lanterns | U |
| Akiba fire-god lanterns along the Tōkaidō | mostly 19th c. (verify) | jōyatō, Jizō | U |
| Very tall stone night-lamp towers | mostly 19th c. (verify) | the always-lit lantern type itself is in (Miya 1625) | R (§3.3) |
| Big sun-curtain noren on dry-goods shops | best evidence 19th-c. prints (verify) | noren, mizuhiki-noren, reed screens | U |
| Clay Shōki on the eaves | 19th c. (verify) | door charms (kado-fuda) | U |
| Glass wind chimes | late 18th–19th c. (verify) | iron or bronze chimes | U |
| Insect sellers' cage stands; peep-box shows | late 18th c. (verify) | goldfish tubs, candy sellers, storytellers | U |
| Water harp (sui-kinkutsu) | popular Meiji (verify) | plain tsukubai | U |
| Diagonal castle stone laying (tanigi-zumi) | late Edo (verify) | nozura, uchikomi-hagi, kirikomi-hagi | U |
| Three-legged torii (present form) | 1831 (verify) | myōjin, shinmei, Kashima torii | U |
| Pilgrim name slips on gates (senja-fuda) | late 18th c. (verify) | votive plaques (ema) | U |
| Dense senbon torii tunnels | mostly later (verify) | a few donated torii | U |
| Big stone arhat groups | 1782–1825 (Kita-in) | Jizō and Kannon rows | U |
| Lost-child notice stone | 1857 | notices pasted on walls | U |
| Western drill grounds | 1840s–60s | horse grounds, archery ranges | U |
| Tanabata rooftop bamboo forest (Edo) | 1850s prints (verify) | a few bamboo at doors | U, R |
| Named bamboo-fence styles (Kōetsu-ji, Ginkaku-ji, Ryōan-ji...) | forms older, many names later (verify) | yotsume, kenninji, shiba, sode fences | U |
| Grooved stone cart tracks (kuruma-ishi) | 1805 | ox carts on earth roads | W, R, U |
| Bamboo-mat road surface at Hakone | gone: replaced by paving 1680 | ishidatami | W |
| Inō Tadataka survey markers | 1800–16 | none | W |
| Keeps on Edo and Osaka castles (skyline) | gone: Edo burned 1657, Osaka 1665 | keep bases only; Kyoto's Nijō keep stands until 1750 | BL §2 |
| Ryōgoku fireworks | from 1733 by tradition (verify) | three years after the anchor: an event, not dressing | U |
| Copying Hiroshige (1833–34) or road maps of 1806 | outside the window | use as depiction only; check each detail (e.g. the basket crossing print is 1850s) | W |

---

# 7. Collapse candidates (suggestions only: Stephen decides)

The four agents' suggestions (N 24, W 12, R 19, U about 25), deduplicated and grouped. Each group says what merges,
what the merged item keeps, and what is lost. Source tags show whose idea it was. Items marked *(merge)* are small
additions by the merge agent where two agents' kits overlapped.

## 7.1 Trees (N 1–13, U planting)
- **Merges:** 5 evergreen oaks → 1 kashi (+ scrubby coastal ubame variant). 7 shii / laurel trees → 2 (dome-crowned
  shii/tabu, small understorey evergreen). 5 deciduous oaks → 2 (coppice oak with a multi-stem stool form, mountain
  oak). 5 maples → 2 (small palmate, large mountain). 4 firs and hemlocks → 2 (lowland fir, subalpine fir). Kiso five →
  hinoki + 1 retexture. 3 wild cherries → 1; edohigan / weeping → 1 landmark cherry; Oshima and mamezakura as
  retextures or cut. Hornbeam, dogwood, snowbell, ryōbu, mallotus, kusagi, nurude, alder → 2–3 small deciduous + an
  edge-scrub model. 4 willows → 2 (bank shrub, weeping). 3 birches → 1. 5 fruit trees → 1 blossoming fruit tree
  (2 bloom colours). 4 citrus → 1. U's trained garden pine and gate pine are a clipped variant of the pine. (N, U)
- **Keeps:** akamatsu vs kuromatsu (hill vs coast) + a wind-shaped kuromatsu; kaki and kuri as their own trees (the
  village signature); sugi, keyaki, ginkgo, enoki, kusunoki as landmark-capable species; seasonal texture sets.
- **Lost:** species-level detail (Kiso five legality, goyōmatsu crags, Oshima's green leaves); ubame only if cliffs
  need it.

## 7.2 Bamboo, shrubs, grasses, ferns, flowers, fungi (N 14–20)
- **Merges:** 4 grove bamboos → 1 tall grove (+ black-culm texture); yadake and medake → 1 thicket; all sasa → 2
  clutter types. 6 azaleas → 1 shrub with 3 bloom textures (+ optional rhododendron); U's clipped karikomi and
  tamamono are its clipped form. 4 coastal shrubs → 1 salt-scrub. 5 tall grasses → susuki (plume and green) + reed.
  Forest ferns → 2–3 clutter ferns. 15 mushrooms → 4–5 item models. ~60 herbs and flowers → 8–10 clutter meshes by
  colour and height + item icons. (N, U)
- **Keeps:** the famine / poison / medicine gameplay as icons; bracken and urajiro; the glowing tsukiyotake.
- **Lost:** per-species flowers and seasons at clutter scale.

## 7.3 Crops and fields (N 21–22, R 1–2)
- **Merges:** paddy → 4 terrain textures (flat with flooded / stubble / winter-barley states, terraced with stone or
  earth risers, deep-mud, creek strips); lotus, taro and rush fields → 1 wet-crop texture with plant proxies. Dry
  fields → 1 ridged texture + ~8 crop proxies (daikon, greens, negi, taro, millet, barley, soy, buckwheat); cash crops
  (rapeseed, cotton, indigo, hemp, tobacco) are the same field with a tall or coloured proxy. Grains: barley/wheat →
  1, millets → 1; rice (with growth stages) and soba separate. Garden vegetables → 3 bed types (leafy, vine on fence,
  root in ridges). (N, R)
- **Keeps:** rice stages; spring rapeseed yellow; hemp as tall cover; the tea-bush and mulberry-bush models (§4 kits).
- **Lost:** crop-by-crop forage variety (icons can keep it).

## 7.4 Rocks, landforms and dead wood (N 23, W 5–6)
- **Merges:** landforms are heightmap and texture work. Placeable set: andesite boulders (3 sizes), granite boulders
  (3), river cobbles, scree scatter, 2 cliff faces, lava slabs, sea stacks. Mounds (ichirizuka, kōshin-zuka, border
  mounds, kyōzuka, kubizuka, kofun, sennin-zuka) → 1 earth-mound shape at 2–3 sizes told apart by what sits on top
  (tree, stone, hokora). (N, W)
- **Keeps:** the named landmark terrain (Hakone caldera, Ōjigoku, Hōei crater) as bespoke terrain.
- **Lost:** nothing modelled; this is terrain effort.

## 7.5 Water control, wells and river works (R 3–4, U gutter kit, W 9)
- **Merges:** earth channel, stone channel, ditch, street gutter → 1 spline with 2 bank materials; sluice, water
  notch, divider, pond outlet, canal and moat water gates → 1 "boards in a frame" part at 3 sizes. Water lifting → 3
  props (lever well doubling as field sweep, treadwheel, river lift wheel); drop the chain pump and swing bucket (or
  keep the bucket as a hand prop). Gutter kit: slab crossing, cover stone, outfall; only the dobu-ita alley drain gets
  its own mesh (it makes noise). Seigyū, jakago and groynes → 1 river-works kit; kasumi-tei, levees and the Bunmei
  bank are terrain. (R, U, W)
- **Keeps:** interactable sluice; the three wells (pulley, lever, box well) and one curb/lid set.
- **Lost:** regional pump and weir variants.

## 7.6 Bridges and crossings (W 7, U bridges)
- **Merges:** 3 kits: (1) flat plank bridge with optional rails and giboshi, scalable from gutter plank to
  Nihonbashi; earth bridge = plank + turf deck; log bridge = the smallest deck; (2) arched wooden bridge, plain or
  vermilion; (3) stone slab bridge, 1–3 slabs. Stepping stones, fords and hand-lines → terrain + props. (W, U)
- **Keeps:** landmark one-offs as optional heroes (Saruhashi cantilever, a boat bridge, Engetsukyō, Seta, Sanjō).
- **Lost:** off-map types (vine bridge, stone arch, Kintaikyō).

## 7.7 Roadside stones, figures, stupas and lanterns (W 1–4, R 13, U monuments, U lanterns)
- **Merges:** ~30 inscribed stones (direction, fork, chō and pilgrim markers, kōshin, moon and sun waiting,
  nenbutsu, daimoku, water and mountain god, boundary, killing-forbidden, famine and quake memorials) → 1 stele
  family of ~6 shapes (square pillar, natural slab, relief panel, round stone, phallic stone, small pagoda) with
  text decals. Figure stones → 5 carvings on one plinth set (Jizō, dōsojin couple, batō Kannon, Fudō, a generic
  Buddha) + caps, bibs and offerings as props. Gorintō, hōkyōin-tō and the chōishi → 2–3 stupa meshes. Lanterns:
  trailhead pair, jōyatō and tōmyōdō → 1 kit in 3 heights; garden set of 5 (kasuga, yukimi, oribe/ikekomi,
  oki-dōrō, misaki), with kotoji, rankei, nuresagi and yama-dōrō as variants or cuts. (W, R, U)
- **Keeps:** readable in-game text (directions, distances, names); the danger tell of batō Kannon.
- **Lost:** carving detail between regional types (couple vs character dōsojin become a decal choice).

## 7.8 Shrine and temple forecourt (R 15, U torii / guardians / forecourt)
- **Merges:** torii → 3 meshes (shinmei, myōjin, Kashima) in wood, vermilion and stone; Inari = myōjin + rings;
  Sannō, ryōbu and Miwa as optional heroes. Komainu and kitsune → 1 pair base with 2 heads. Forecourt kit: offering
  box, bell rope, ema rack, lantern row, chōzubachi, jōkōro, waniguchi, strength stone; shrine vs temple is which
  ones you place. Hundred-times stone, banner stones and offering box are optional adds. (R, U)
- **Keeps:** the shinbutsu shūgō mix (temple kit and shrine kit on one site).
- **Lost:** torii style detail; messenger-statue variety.

## 7.9 Graveyards (R 14, U graveyard kit)
- **Merges:** reuse the stele family (boat-halo, slab, square pillar, figure grave) + gorintō / hōkyōin-tō / muhōtō,
  sotoba and rack, earth mound with post, bamboo dog-guard, bucket rack, flower tubes; the daimyō precinct and
  muen pile are arrangements, not models. (R, U)
- **Keeps:** the 1730 mix (boat-halo stones common, square pillars rising, no family-name stones).
- **Lost:** stone-by-stone typology.

## 7.10 Fences, walls and gates (R 11–12, U fences / walls / castle wall kit)
- **Merges:** fences → 4 kits: open bamboo grid; closed panel (kenninji, brush, reed, board by material); live
  hedge; stone wall (terrace, plot, cobble by material). Named temple-style bamboo fences → 1 "fancy fence" slot at
  most (several names may be post-1750). Gates → 3 (post gate, kabuki-mon, wicket); the roofed ridge gate is BL.
  Walls → dobei section with swap-in port shapes, board wall, namako as a material; tsuiji and neri-bei share the
  earth-wall mesh. (R, U)
- **Keeps:** sight-block vs see-through as the gameplay split; sode-gaki as a small screen.
- **Lost:** snow and Izumo pine fences (off-map).

## 7.11 Farmyard, harvest and crop protection (R 5–10)
- **Merges:** 1 drying-rack kit (hasa poles with swappable loads: sheaves, daikon, persimmons, noodles, kanpyō,
  squid, fish, seaweed, nori mats, nets, laundry): ~15 entries across R §4, §6, §15. 1 stack kit (straw, sheaves,
  thatch, firewood, brushwood, fuel piles, rice and salt bales) with material swaps. 1 ground mat with texture
  overlays (grain, beans, cotton, sardines, radish strips, umeboshi, agar). Harvest set of ~6 props (comb, winnower,
  sieve, mortar, quern, flail). Scarers → 3 (scarecrow with the Sanemori doll as a variant, clapper line with the
  rope lines, knocking bamboo); smell scarer and charms are stick props. Boar defences → 2 kits (stone wall reusing
  the terrace wall, stake-and-brush fence reusing shiba-gaki); the earth bank is terrain. (R)
- **Keeps:** harvest as a season layer; alarm lines as gameplay.
- **Lost:** the chopstick thresher, hulling mill, treadle mortar and water-driven pounding lever as separate models
  (they could join the harvest set as variants); regional scarer forms.

## 7.12 Shore, salt and wreckage (R 17–18, W 10–11)
- **Merges:** 3 shore kits: beach boat + skids + capstan; net rack (from the drying-rack kit); shore clutter
  (floats, pots, traps, anchors, driftwood). Salt field → 1 terrain + 1 filter-pit prop + a tool rack; keep the tidal
  (Kinai-side) type unless the Kantō coast needs the spread type. Wreckage: debris line, beached anchor, broken kago
  and dropped pole-and-baskets → 1 scatter loot-spot set. (R, W)
- **Keeps:** the stranded cargo ship as one hero wreck.
- **Lost:** regional net and salt-tool variants.

## 7.13 Streets and shop fronts (U streets)
- **Merges:** 1 fire-corner kit (big tub + bucket pyramid + hook rack + ladder; the hanshō-dai ladder tower is the
  one hero; roof ladder and rooftop platform share its parts). 1 hanging-lantern mesh with swapped paper and text
  (shop, inn, brigade, gate); carry lanterns → 2 (hand, folding travel). 1 box-lamp frame at 3 heights (kake-, oki-,
  tsuji-andon). 1 noren + 2 cheap variants. Kanban: hanging, standing, roof board + 4–6 shape signs (brush, geta,
  gourd, umbrella, tabi, spectacles): the shape signs make a street read as Edo. Stall family (reed stall, kake-mise,
  tea stand, yatai, night-soba kit) sharing poles, reed panels and a counter. 1 peddler shoulder pole with swap-in
  loads (~15 entries). (U)
- **Keeps:** noise props (dobu-ita, clappers); the bench (§4 shared kit).
- **Lost:** trade-specific peddler and sign detail beyond the chosen shapes.

## 7.14 Canals and boats (U water)
- **Merges:** 1 canal-edge kit (stone wall section, gangi steps, mooring post, mooring stone, outfall); kashi, hama
  and funairi are placements of it. Boats: chokibune, yanebune, a flat cargo boat and one big passenger boat;
  gozabune and yakatabune optional heroes. (U)
- **Keeps:** canal cities (Osaka, eastern Edo) as a distinct look.
- **Lost:** local boat types (Takase, kurawanka).

## 7.15 Gardens (U gardens)
- **Merges:** lantern set of 5 (7.7); basin set of 3 (tsukubai group, tall veranda basin, natural-stone basin) + kakei
  spout and sōzu add-ons; stone kit of 6–8 rocks (tall, flat, reclining, arching) for triads, crane and turtle
  islands, dry waterfalls and shores; flat-stone kit (stepping stones, nobedan, shoe stone). Named gardens: one Edo
  daimyō garden (Rikugien or Koishikawa) and one Kyoto dry garden (Ryōan-ji type) as heroes; the rest are placements.
- **Keeps:** the three garden types (stroll, dry, tea) and the town courtyard garden.
- **Lost:** named lantern and fence varieties.

## 7.16 Festivals and markets (R 16, U temporary kit)
- **Merges:** 1 temporary-structure kit (poles, reed screens, board counters, mat roofs, sajiki boards) for stalls,
  show-booth fronts, viewing stands, tea stands, sumo stands and the lottery stage. 1 seasonal event layer toggled by
  date: banners, lanterns, mikoshi, pyre, Bon lanterns, kadomatsu, shimenawa, Bon shelf, hanami curtain. Floats (Gion
  hoko, Edo dashi) and the bon tower as optional big pieces, one of each at most. (R, U)
- **Keeps:** the 1730 events (tomikuji lottery at Gokoku-ji, Dōjima licensed) as story hooks.
- **Lost:** most market-day specifics (they become placements).

## 7.17 Castles and castle ruins (U castle, W 6)
- **Merges:** ishigaki as 3 materials (nozura, uchikomi-hagi, kirikomi-hagi) on the same wall profiles, coursing as
  texture; masugata is a placement of 2 BL gates + wall sections; umadashi is terrain. Ruins: horikiri, tatebori,
  dorui, kuruwa, koguchi, toride and siege camps → 1 terrain-sculpting toolkit + 3–4 props (broken wall corner, well,
  post stones). (U, W)
- **Keeps:** Yamanaka and Ichiya (Hakone) as named layouts.
- **Lost:** laying-pattern variety as geometry.

## 7.18 Wild work sites, traps and traces (W 8, W 11)
- **Merges:** snare, deadfall and pit → 1 trap system; charcoal kiln live and ruin as one model with a ruin state;
  log deck, chute and sledge track as one timber-landing kit; road litter (cast sandals, horse shoes, droppings) as
  decals. *(merge, partly)* (W)
- **Keeps:** smoke columns from kilns (navigation); forest markers as the "you are in a banned forest" tell.
- **Lost:** per-craft forest sites (shingles, turners' workings) unless kept as clutter.

## 7.19 Fauna (N 24)
- Game animals → deer, boar, bear, serow, hare, pheasant, duck, fish (a few sizes); wolves and macaques as AI
  threats; everything else ambience or icon-only. Separate job; not counted below.

## 7.20 Cut candidates (off-map, outside the window, or low value)
- **W:** Ao-no-Dōmon, kuruma-ishi, Inō survey marks, flag-relay hills; whale lookout and whale grave; Kashima / Shōki
  straw giants; Kaga duck nets, ajiro, ishi-hibi, kōgoishi, Sado wareto; Osorezan, Itsukushima, Kumano ōji, echo
  rock, avalanche warning post; mist net and bird lime.
- **R:** everything in R §17; all off-map windbreaks and snow gear; ginseng beds, hotbeds, agar fields and wasabi
  terraces unless kept as rare landmarks; the tsunami stone; pear trellis; the incense water clock (keep as lore).
- **U:** kuruma-ishi, insect sellers, glass chimes, peep box, yane-Shōki, lost-child stone, ōchōchin, Akiba
  lanterns, sun-curtain noren (all tagged late); per-house tensui-oke; off-map landmark gardens and bridges.
- **N:** off-map species (hamanasu, kombu, sugar cane, wax plantations) and the late crops in §6.

## 7.21 Rough model count

Placed outdoor models only (props, structures, trees, shrubs); fauna, BL buildings and terrain excluded. Built
bottom-up from the groups above, so treat it as an order of magnitude.

| Group | Light collapse | Heavy collapse |
|---|---|---|
| Trees and large plants (7.1) | ~65 | ~35 |
| Shrubs and bushes (7.2) | ~15 | ~6 |
| Rocks, dead wood, natural props (7.4) | ~20 | ~10 |
| Water control, wells, river works (7.5) | ~22 | ~10 |
| Bridges and crossings (7.6) | ~14 | ~6 |
| Roadside stones, figures, stupas, lanterns (7.7) | ~27 | ~12 |
| Shrine and temple forecourt (7.8) | ~20 | ~10 |
| Graveyards (7.9) | ~10 | ~5 |
| Fences, walls, gates (7.10) | ~19 | ~10 |
| Farmyard, harvest, crop protection (7.11) | ~45 | ~20 |
| Shore, salt, wreckage (7.12) | ~25 | ~10 |
| Streets and shop fronts (7.13) | ~40 | ~18 |
| Canals and boats (7.14) | ~12 | ~6 |
| Gardens (7.15) | ~30 | ~12 |
| Festivals and markets (7.16) | ~20 | ~10 |
| Castles and ruins, props only (7.17) | ~8 | ~4 |
| Wild work sites, traps, traces (7.18) | ~40 | ~18 |
| **Placed models** | **~430** | **~200** |

**Range: about 200 (heavy) to 430 (light) placed outdoor models, ~300 as a middle road.** Beside that, kept apart:
- **Clutter meshes:** ~40 (light) to ~20 (heavy): sasa, grasses, ferns, flowers, crop proxies, shore wrack.
- **Terrain work (not models):** ~30 ground textures (N §S) collapsing to ~15; ~10–20 earthwork and linear tools
  (mounds, moats, ramparts, terraces, levees, roads, channels, paddies); plus the landmark terrain.
- **Multipliers, not new models:** seasonal texture sets (bloom, autumn, bare, snow) on every deciduous tree and
  crop, and ruin / damage states of live models.

For scale: Chernarus used ~165 building models plus about 6,000 small structures (sheds, outhouses, wells, stands);
its 2,586 garden sheds come from only 10 models (CHERNARUS_BASELINE.md). The heavy end here is closer to that
spirit: few models, placed many times.

---

# 8. To verify

Every `(verify)` flag in the four inputs (and the merge's own), as a checklist, by source file and section. The clause in quotes is what needs checking. Items the agents marked only `(assumed)` are not listed.

## 8.N N_NATURE.md

- [ ] **Japanese cherry birch (mizume, Betula grossa)** (N §C): azusa-yumi, verify
- [ ] **Ash (shioji Fraxinus platypoda, yachidamo F. mandshurica, aodamo F. lanuginosa)** (N §C): Hook: tool handles, bows (verify)
- [ ] **Amur cork tree (kihada, Phellodendron amurense)** (N §C): Ontake's darani-suke, Kiso's hyakusōgan, verify dates
- [ ] **Chinaberry (sendan / ōchi, Melia azedarach)** (N §C): the tree associated with displaying executed criminals' heads at the prison (verify)
- [ ] **Apricot (anzu, Prunus armeniaca)** (N §D): verify local date
- [ ] **Fig (ichijiku, Ficus carica)** (N §D): Rare (verify)
- [ ] **Hakone bamboo (hakonedake, Pleioblastus chino var. vaginatus)** (N §F): verify taxon
- [ ] **Kerria (yamabuki, Kerria japonica)** (N §G): Hook: pith for lamp wicks (verify)
- [ ] **Fatsia (yatsude, Fatsia japonica)** (N §G): Hook: insecticide from leaves (verify)
- [ ] **Boston ivy (tsuta, Parthenocissus tricuspidata)** (N §H): amazura, verify
- [ ] **Kariyasu (kariyasu, Miscanthus tinctorius)** (N §I): verify range on our map
- [ ] **Running clubmoss (hikagenokazura, Lycopodium clavatum)** (N §J): spores as flash powder (verify)
- [ ] **Sphagnum (mizugoke, Sphagnum)** (N §J): verify period use
- [ ] **Thistles (azami, Cirsium spp.)** (N §K): Hook: edible root (verify)
- [ ] **Bracket fungi (sarunokoshikake, kawaratake Trametes)** (N §L): Hook: tinder (verify)
- [ ] **Arame and kajime (Eisenia bicyclis, Ecklonia cava)** (N §N): verify period use
- [ ] **Red rice (akagome / taitōmai, Oryza sativa, Champa type)** (N §O): mem, verify share
- [ ] **Maize (tōmorokoshi / nanbankibi, Zea mays)** (N §O): Rare (verify)
- [ ] **Hyacinth / kidney bean (ingenmame)** (N §P): verify which bean
- [ ] **Potato (jagaimo)** (N §P): Rare (verify)
- [ ] **Korean ginseng (chōsen ninjin, Panax ginseng)** (N §P): mem, verify dates
- [ ] **Safflower (benibana, Carthamus tinctorius)** (N §Q): verify start
- [ ] **Tobacco (tabako, Nicotiana tabacum)** (N §Q): verify start date
- [ ] **Caldera lake (Ashinoko)** (N §U): verify Edo-era visibility
- [ ] **Solfatara crust and sulphur crystals (iō)** (N §V): verify Hakone Edo extraction
- [ ] **Hot spring deposits (yunohana, travertine, iron-red staining)** (N §V): verify period trade
- [ ] **Whales and dolphins (kujira, iruka)** (N §Fauna): drive hunts in Izu (verify)
- [ ] **Lake fish of Ashinoko** (N §Fauna): dace, crucian, eel, verify
- [ ] **Sea turtles (umigame)** (N §Fauna): Nest on sandy beaches of Enshū-nada and Sagami (verify)

## 8.W W_WILDERNESS.md

- [ ] **Mile mound on a minor road (waki-kaidō ichirizuka)** (W §1): verify how regular they were on side roads
- [ ] **Deity direction stone (michi-shirube Jizō / kōshin michi-shirube)** (W §1): verify frequency before 1750
- [ ] **Pointing-hand direction stone (yubisashi michi-shirube)** (W §1): verify; many surviving examples are later Edo
- [ ] **Mountain station marker (gōme-ishi / gōme-hyō)** (W §1): verify form and date before 1750
- [ ] **Cliff plank road (kakehashi / kake-michi)** (W §2): verify the 1647/48 rebuild details
- [ ] **Chain climbs on sacred peaks (kusari-ba)** (W §2): verify dates; some chains may be later Edo
- [ ] **Old abandoned road alignment (kyūdō / furumichi)** (W §2): verify the Yusaka route
- [ ] **Pack-ox path (ushi-michi / bokka-michi)** (W §2): verify the ox use before 1750
- [ ] **Stone lantern at a dangerous spot (jōyatō)** (W §3): verify how many were really lit nightly in 1730
- [ ] **Basket rope crossing (kago-watashi / yaen)** (W §4): verify window; the famous print is Hiroshige, 1850s
- [ ] **Seasonal low-water bridge (kari-bashi / fuyu-bashi)** (W §4): verify which rivers
- [ ] **Round-stone dōsojin (maru-ishi dōsojin)** (W §5): verify the period
- [ ] **Moon-waiting stone (tsukimachi-tō: nijūsan-ya / jūkyū-ya)** (W §5): verify the date peak; BL lists the 23rd-night stone
- [ ] **Sun-waiting stone (himachi-tō)** (W §5): Roadside, rare, small. (verify)
- [ ] **Daimoku stone (daimoku-tō)** (W §5): verify the Suzugamori date
- [ ] **Sutra mound (kyōzuka)** (W §5): verify the Edo frequency
- [ ] **Hill-circuit Kannon (utsushi reijō / sanjūsan Kannon)** (W §5): verify: the boom was 18th c, some later
- [ ] **Ōyama pilgrimage stones (Ōyama-michi hyō)** (W §6): verify: the Ōyama-mairi boom may be mostly after 1750
- [ ] **Rebirth lava cave (tainai / tainai-kuguri)** (W §6): verify the discovery dates; Funatsu is traditionally late 17th c
- [ ] **Sledge track (kinma-michi)** (W §8): verify that kinma was in use before 1750
- [ ] **Log flush dam (teppō-zeki)** (W §8): verify the Edo date
- [ ] **Log-catching boom (tsuna-ba / ami-ba)** (W §8): verify Nishikori
- [ ] **Clear-cut bare slope (hage-yama)** (W §8): Totman, *The Green Archipelago*, verify detail
- [ ] **Planted cedar stand (sugi no ue-bayashi)** (W §8): planting spread elsewhere (verify)
- [ ] **Shiitake log stack (shiitake hodagi)** (W §8): verify the date in Izu
- [ ] **Pit trap (otoshi-ana / shishi-ana)** (W §9): verify stakes
- [ ] **Ridge mist-net (kasumi-ami)** (W §9): verify the date
- [ ] **Duck-netting pond (sakaami / kamo-ba)** (W §9): Kaga `[off-map: Kaga]`. (verify)
- [ ] **Shogun's hunt field (kariba / shishigari-ba)** (W §9): verify the dates
- [ ] **Stake-lattice weir (ajiro)** (W §9): verify: largely medieval
- [ ] **Stake-lattice weir (ajiro)** (W §9): merge fix: older survivors are IN; verify whether the Uji and Tanakami weirs were still worked in 1730
- [ ] **Hand-dug prospect burrows (tanuki-bori)** (W §10): verify the term
- [ ] **Abandoned mine (haikō / kyūkō)** (W §10): Toi gold mine was in use; verify which were closed
- [ ] **Placer gold workings (sakin-tori-ba)** (W §10): verify how active in 1730
- [ ] **Abandoned marked block (kokuin-ishi / "zannen-ishi")** (W §10): verify the name *zannen-ishi*
- [ ] **Whetstone or millstone quarry (toishi-yama / usu-ishi chōba)** (W §10): verify locations
- [ ] **Sulphur workings (iō-tori-ba)** (W §10): BL: Rural industry, sulphur; verify Ōwakudani in 1730
- [ ] **Wild riverside hot pool (kawa-yu / nozura-buro)** (W §10): assumed; period form to verify, per WC "Additions"
- [ ] **Hot-spring steaming ground (yu-no-hana tori)** (W §10): verify: the Beppu and Kusatsu dates are 18th c
- [ ] **Ice pit (himuro)** (W §10): generic ones elsewhere (verify)
- [ ] **Famine root-digging ground (warabi-ne hori-ba)** (W §11): verify the extent
- [ ] **Medicinal-herb garden in the hills (yakuen / yakusō-bata)** (W §11): verify; Komaba and Koishikawa are urban
- [ ] **Open staggered levee (kasumi-tei)** (W §12): Hook: cover, navigation. (verify)
- [ ] **Aqueduct tunnel through a crater rim (Hakone yōsui / Fukara yōsui)** (W §12): verify the length
- [ ] **Flood-level mark (kōzui-hi / mizu-jirushi)** (W §12): verify for the window
- [ ] **Slope-planting or erosion barrier (sunadome)** (W §12): Hook: cover. (verify)
- [ ] **Landslide dam remains (sekitome-ko no ato)** (W §12): Hook: danger, landmark. (verify)
- [ ] **Paired border mounds (sakai-zuka)** (W §13): Hook: navigation. (verify)
- [ ] **Border ditch between provinces (Nemonogatari no sato)** (W §13): Hook: lore, landmark. (verify)
- [ ] **Straw giant at a village edge (Kashima-sama / Shōki-sama)** (W §13): verify the Edo dating
- [ ] **Shogun's falconry-ground boundary post (otakaba sakai-gui)** (W §13): verify the post form
- [ ] **"Killing forbidden" stone (sesshō kindan-seki)** (W §13): verify examples
- [ ] **Checkpoint palisade up the slope (sekisho no yarai / sakumono)** (W §13): verify the Hakone extent
- [ ] **Wolf-charm post (ōkami ofuda-gui)** (W §13): verify the placement; the charms are Edo
- [ ] **Flag-signal relay hill (hata-furi yama)** (W §14): verify: may be after 1750
- [ ] **Mountain-top prayer fire for rain (amagoi-bi)** (W §14): Hook: fire, landmark. (verify)
- [ ] **Battlefield field marker (kosenjō no hi)** (W §15): verify which were marked before 1750
- [ ] **Keyhole tomb mound (zenpō-kōen-fun)** (W §17): verify the details of the Genroku repair
- [ ] **Cliff tomb holes (yokoana-bo)** (W §17): verify how visible they were pre-1887
- [ ] **Burial-only grave in the hills (ume-baka)** (W §17): verify for 1730
- [ ] **Earthquake/tsunami memorial (jishin kuyō-tō)** (W §17): verify surviving in-window stones
- [ ] **Hermit or ascetic's grave (nyūjō-zuka)** (W §17): verify the in-window examples
- [ ] **Otama pond marker (Otama-ga-ike)** (W §18): verify the 1702 date
- [ ] **Seaweed-drying poles and mats (kaisō hoshi-ba)** (W §19): verify the kanten date
- [ ] **Nori stakes in the shallows (nori-hibi)** (W §19): verify; the urban/rural agents overlap
- [ ] **Planted coastal pine belt (bōfū-rin / bōsa-rin)** (W §19): verify local dates
- [ ] **Beach net-hauling capstan (ami-biki no rokuro)** (W §19): `[off-map-ish: Bōsō]` (verify)
- [ ] **Salvage marker (hyōchaku-fuda)** (W §20): Hook: lore. (verify)
- [ ] **Konpira sea-safety stone (Konpira-hi)** (W §20): verify how far Konpira had spread east by 1730

## 8.R R_RURAL.md

- [ ] **Flat paddy (heichi no ta / hira-ta)** (R §1): verify date
- [ ] **Bund-top soybeans (aze-mame)** (R §1): assumed; common practice in Edo farm manuals, verify
- [ ] **Double-cropped paddy with winter barley ridges (nimōsaku-den)** (R §1): Src: NGZ (Kinai double cropping) (verify)
- [ ] **Raised strip fields with creeks (horiage-ta / kuriku / hori-ta)** (R §1): verify for Osaka
- [ ] **Sea dyke of reclaimed land (shinden tsutsumi / shio-dome)** (R §1): Src: Kyōhō shinden kaihatsu (1722 notice) (verify)
- [ ] **River levee with planted bamboo (tsutsumi / dote, suibō-rin)** (R §1): assumed practice, verify period
- [ ] **Open levee with gaps (kasumi-tei)** (R §1): Hook: odd levee geometry, landmark. (verify)
- [ ] **Lotus-root field (hasu-da / renkon-ta)** (R §1): verify period
- [ ] **Rush field for tatami (igusa-da)** (R §1): some Ōmi]` (verify)
- [ ] **Incense water-clock (senkō-mizu)** (R §2): verify date
- [ ] **Pond outlet with plug tower (soko-hi / tate-hi)** (R §2): assumed form; verify name
- [ ] **Pond spillway (yosui-bake)** (R §2): assumed; name verify
- [ ] **Timber river-crib spurs (seigyū / waku)** (R §2): verify names and period
- [ ] **Irrigation tunnel (manbo / mabu / zuidō)** (R §2): verify exact dates
- [ ] **River lift wheel (agemizu-guruma / mizu-guruma)** (R §2): Yodo wheel date: verify
- [ ] **Dragon-backbone chain pump (ryūkotsu-sha)** (R §2): merge fix: verify it was still in use somewhere in 1730
- [ ] **Gourd trellis (yūgao-dana / hyōtan-dana)** (R §3): Src: Mibu kanpyō 1712 (verify)
- [ ] **Loofah trellis (hechima-dana)** (R §3): verify date for Edo commoners
- [ ] **Bean poles (sasage / ingen supports)** (R §3): Ingen bean brought 1654 by the monk Ingen: legend, verify
- [ ] **Greens and leaf mustard (na / komatsuna)** (R §3): Komatsuna naming legend: Yoshimune, 1719; verify
- [ ] **Tobacco field (tabako-batake)** (R §3): verify Hadano's Edo start
- [ ] **Corn patch (tōmorokoshi / nanban-kibi)** (R §3): verify spread by 1730
- [ ] **Ginseng bed with shade roof (ninjin-hata)** (R §3): verify dates
- [ ] **Wasabi terrace (wasabi-da)** (R §3): Hook: food, clean water. (verify)
- [ ] **Mulberry field and mulberry hedge (kuwa-batake)** (R §3): assumed; verify
- [ ] **Citrus terraces (mikan-batake)** (R §3): `[off-map: Kii, edge of map]` (verify)
- [ ] **Pear orchard on overhead trellis (nashi-dana)** (R §3): verify that trellis pears predate 1750
- [ ] **Hotbed frames with oiled paper (onsho / abura-shōji)** (R §3): verify; the bakufu restricted early-season vegetables, 1686
- [ ] **Living-tree rack row (hasa-gi / inaki)** (R §4): verify for Kanto
- [ ] **Water-driven pounding lever (battari / sōzu-usu; name verify)** (R §4): regional names vary; verify
- [ ] **Agar winter drying fields (kanten-ba)** (R §4): verify dates
- [ ] **Freeze-dried tofu racks (kōri-dōfu / shimi-dōfu)** (R §4): verify date for commoners
- [ ] **Hemp steaming and retting (asa-mushi / asa-hitashi)** (R §4): verify form
- [ ] **Scaring gun (odoshi-deppō)** (R §5): Hook: rare weapon lore. (verify)
- [ ] **Whale-oil paddy spread (abura-chū)** (R §5): verify dates
- [ ] **Spiral walk-down well (maimai-zu ido)** (R §6): medieval origin, Edo use; verify
- [ ] **Wash tub and summer bath tub (tarai / gyōzui-darai)** (R §6): No washboard: the ridged washboard is Meiji (verify)
- [ ] **Three-tined hoe (Bitchū-guwa)** (R §7): verify spread date
- [ ] **Hand-cart (niguruma)** (R §7): rural rarity assumed; verify
- [ ] **Ox cart (ushi-guruma)** (R §7): The stone cart-track (kuruma-ishi) at Ōtsu is `[outside 1680-1750: 1805]` (verify)
- [ ] **Loose hens (niwatori)** (R §7): egg-eating: verify
- [ ] **Log beehive (hachi-dō / hachi-bako)** (R §7): Hook: honey. (verify)
- [ ] **Farm fish pond (ike)** (R §7): Paddy carp farming at Saku is `[outside 1680-1750: tradition dates 1746]` (verify)
- [ ] **Crossbar gate with small roof (kabuki-mon)** (R §8): commoner gates were restricted by rank: verify local rules
- [ ] **Small fox figures at a yard Inari (kitsune)** (R §9): verify material in 1730
- [ ] **Burial grave of the two-grave system (ume-baka, ryōbosei)** (R §9): verify distribution
- [ ] **Tall lantern pole for the newly dead (taka-dōrō)** (R §9): verify for 1730 regions
- [ ] **Stone torii (ishi-dorii)** (R §10): verify with dated examples
- [ ] **Rope gate (shimenawa-torii / tsuna-kake)** (R §10): Hook: landmark. (verify)
- [ ] **Guardian lions (komainu, stone approach type)** (R §10): verify frequency in 1730
- [ ] **Hundred-visits stone (hyakudo-ishi)** (R §10): most surviving ones are late Edo: verify
- [ ] **Strength stones (chikara-ishi)** (R §10): many are 18th–19th c.: verify
- [ ] **Banner-pole stones (nobori-tate ishi)** (R §10): verify date
- [ ] **Divination slips tied to branches (o-mikuji musubi)** (R §10): verify; likely `[outside 1680-1750]`
- [ ] **Shrine-name stone pillar (shagō-hyō)** (R §10): `[outside 1680-1750: mostly Meiji and later]` (verify)
- [ ] **Boat-backed relief gravestone (funagata kōhai)** (R §11): typology from Edo grave archaeology; verify
- [ ] **Dog guard over a new grave (inu-hajiki / mogari-gaki)** (R §11): names and regions: verify
- [ ] **Roadside Jizō (michi-jizō / tsuji-jizō)** (R §12): the red bib may be later: verify
- [ ] **Women's Kannon stone (Nyoirin Kannon, nijūku-ya / nijūku-nichi)** (R §12): 18th–19th c.; verify earliest
- [ ] **Kōshin stone with three monkeys (kōshin-tō)** (R §12): verify peak
- [ ] **Round-stone dōsojin (maru-ishi dōsojin)** (R §12): verify date
- [ ] **Lotus-sutra pilgrim memorial (rokujūrokubu kuyōtō)** (R §12): verify peak
- [ ] **Kannon pilgrimage copy stones (utsushi reijō)** (R §12): `[outside 1680-1750: mostly late 18th–19th c.]` (verify)
- [ ] **Dairokuten stone** (R §12): Commons, rare, small. (verify)
- [ ] **Village boundary rope (kanjō-nawa / kanjō-kake)** (R §13): verify examples
- [ ] **Straw serpent on trees (ja / jagi)** (R §13): Hook: landmark. (verify)
- [ ] **Giant straw sandal charm (ō-waraji)** (R §13): verify date
- [ ] **Commons pasture (maki)** (R §13): verify for our map
- [ ] **Bon-dance tower (bon-odori yagura)** (R §14): verify; tagged
- [ ] **Insect-sending procession (mushi-okuri)** (R §14): Edo-period custom; verify local forms
- [ ] **Tug-of-war rope (tsuna-hiki)** (R §14): verify Kinai examples
- [ ] **Carp streamers (koinobori)** (R §14): Koinobori `[outside 1680-1750: mid-to-late 18th c.]` (verify)
- [ ] **Doll-floating boats (hina-nagashi)** (R §14): verify date
- [ ] **Temporary kagura or performance stage (kari-butai)** (R §14): verify; BL
- [ ] **Festival sake barrels (komo-daru) stacked as offerings** (R §14): the stacked-wall display may be later: verify
- [ ] **Nori stakes in the shallows (hibi)** (R §15): verify start date
- [ ] **Funadama or Konpira votive lantern (umi no tōrō)** (R §15): the Konpira boom is `[outside 1680-1750: late 18th c.]`; verify
- [ ] **Tsunami memorial stone (tsunami-hi)** (R §15): verify locations; many famous ones are 1854
- [ ] **Splashing bucket (shiomaki-oke)** (R §16): name verify
- [ ] **Stone Inari foxes (ishi-kitsune)** (R §17): For 1730 use small wooden or ceramic foxes, or none (verify)
- [ ] **Daruma doll** (R §17): `[outside 1680-1750: Takasaki papier-mâché from the 1780s–90s]` (verify)
- [ ] **Tall stone night-lamp towers (jōyatō)** (R §17): `[outside 1680-1750: mostly 19th c.]` (verify)
- [ ] **Shrine-name pillar and donor stone fences (shagō-hyō, tamagaki with names)** (R §17): `[outside 1680-1750: mostly Meiji+]` (verify)
- [ ] **Ridged washboard (sentaku-ita)** (R §17): `[outside 1680-1750: Meiji]` (verify)
- [ ] **Wheelbarrow (neko-guruma)** (R §17): `[outside 1680-1750: late Edo–Meiji]` (verify)
- [ ] **Stone cart tracks (kuruma-ishi)** (R §17): `[outside 1680-1750: 1805]` (verify)
- [ ] **Paddy carp farming (Saku koi)** (R §17): `[outside 1680-1750: 1746 tradition]` (verify)

## 8.U U_URBAN.md

- [ ] **Back-to-back sewer (seiwari gesui, "Taikō gesui")** (U Streets: Street surface): verify stone date
- [ ] **Alley resident board (roji kanban)** (U Streets: Street surface): verify date; common in late-Edo prints
- [ ] **Sand heaps for processions (morizuna)** (U Streets: Street surface): sand cones or spread sand laid on the road before a daimyō or shogunal procession passed (verify)
- [ ] **Door-side sand cones (tate-zuna)** (U Streets: Street surface): Kyoto; verify
- [ ] **Cart-guard stones at corners (kuruma-yoke ishi)** (U Streets: Street surface): verify date
- [ ] **Rooftop drying platform (monohoshi-dai)** (U Streets: Street surface): verify date; late-Edo prints
- [ ] **Potted-plant shelves by the door (hachiue-dana, uekibachi)** (U Streets: Street surface): the Genroku gardening boom made them common in Edo (verify)
- [ ] **Hanging bird cage (tori-kago)** (U Streets: Street surface): verify date
- [ ] **Temple fire tub (tensui-oke, cast)** (U Streets: Fire-fighting and night-watch fixtures): most survivors are late Edo; verify
- [ ] **Crossroads lamp (tsuji-andon)** (U Streets: Street lighting and lanterns): verify how common in 1730
- [ ] **Akiba fire-god lantern (Akiba jōyatō)** (U Streets: Street lighting and lanterns): `[outside 1680-1750: mostly 19th c.]` (verify)
- [ ] **Collapsible travel lantern (odawara-chōchin)** (U Streets: Street lighting and lanterns): linked with Odawara in the Kyōhō era (verify)
- [ ] **Giant gate lantern (ōchōchin)** (U Streets: Street lighting and lanterns): verify; smaller hanging lanterns at gates are fine
- [ ] **Rope curtain (nawa-noren)** (U Streets: Shop fronts): verify date
- [ ] **Sun curtain (hiyoke-noren)** (U Streets: Shop fronts): verify; Echigoya is the classic image
- [ ] **Roof signboard (yane-kanban)** (U Streets: Shop fronts): verify 1680s ruling
- [ ] **Cedar ball (sugidama, sakabayashi)** (U Streets: Shop fronts): verify when common
- [ ] **Door charms (kado-fuda, somin shōrai, Gion chimaki)** (U Streets: Shop fronts): Kyoto; verify date for chimaki
- [ ] **Clay Shōki on the eave (yane-Shōki)** (U Streets: Shop fronts): `[outside 1680-1750: 19th c.]` (verify)
- [ ] **Red felt cover (hi-mōsen)** (U Streets: Street furniture): imported wool; verify when cheap enough for tea stands
- [ ] **Shouldered noodle stall (katsugi-yatai)** (U Streets: Peddlers'): the "nihachi" name appears Kyōhō era, verify
- [ ] **Goldfish seller's tubs (kingyo-uri oke)** (U Streets: Peddlers'): verify date for street goldfish sellers; mid-18th c.
- [ ] **Insect seller's cage stand (mushi-uri)** (U Streets: Peddlers'): `[outside 1680-1750: street sellers late 18th c.]` (verify)
- [ ] **Wind-chime seller's frame (fūrin-uri)** (U Streets: Peddlers'): iron and bronze earlier]` (verify)
- [ ] **Medicine peddler's wicker trunks (baiyaku no yanagi-gōri)** (U Streets: Peddlers'): from about 1690, verify
- [ ] **Street storyteller's stand (tsuji-kōshaku)** (U Streets: Peddlers'): Fukai Shidōken lectured in Asakusa in the 1740s (verify)
- [ ] **Peep-box show (nozoki-karakuri)** (U Streets: Peddlers'): `[outside 1680-1750: common late 18th c.]` (verify)
- [ ] **Osaka big cart (beka-guruma)** (U Streets: Peddlers'): verify date
- [ ] **Well curb, pottery rings (kawara-gawa)** (U Streets: Wells and street water supply): verify date
- [ ] **Annual well cleaning (ido-sarai)** (U Streets: Wells and street water supply): buckets, ropes and men down the shaft (verify)
- [ ] **Aqueduct junction box (tame-masu, masu)** (U Streets: Wells and street water supply): verify term
- [ ] **Famous spring well (meisui)** (U Streets: Wells and street water supply): e.g. Somei-i at Nashinoki; verify which were flowing in 1730
- [ ] **Urine tubs at the roadside (shōben-tago)** (U Streets: Rubbish): verify date; strongest evidence is 19th-c. Morisada
- [ ] **Nightsoil boat (koe-bune, kasai-bune)** (U Streets: Rubbish): verify name
- [ ] **Zero milestone (dōgen)** (U Streets: Notices): Current marker is modern; model a plain post. verify
- [ ] **Drawbridge / lifting bridge (hane-bashi, hiki-bashi)** (U Water: Bridges): verify how many existed in 1730
- [ ] **Osaka's public bridges (kōgi-bashi) vs town bridges (machi-bashi)** (U Water: Bridges): verify counts
- [ ] **Barber's booth at a bridge end (kamiyui-doko)** (U Water: Bridges): barbers set up at bridge ends and were given bridge-watch duty (verify)
- [ ] **Timber pond (kiba)** (U Water: Canals): Edo's lumber merchants moved to Fukagawa Kiba around 1701 (verify)
- [ ] **Summer riverbed platforms (noryō-yuka)** (U Water: Canals): Edo period, verify start
- [ ] **Great pleasure barge (yakatabune)** (U Water: Boats moored in town): the largest were restricted in the late 17th c. (verify)
- [ ] **Shogunal state barge (gozabune)** (U Water: Boats moored in town): Tenchi-maru (1630s) survived into the 18th c. (verify)
- [ ] **Miniature Mount Fuji (Fuji-yama, tsukiyama)** (U Gardens: Stroll garden): Suizen-ji, Kumamoto; in Edo estates too, verify
- [ ] **Waterfall (taki)** (U Gardens: Stroll garden): form named in older manuals; verify TSD
- [ ] **Rake patterns (samon)** (U Gardens: Dry garden): verify which were used in 1730
- [ ] **Sand platform and sand cone (ginshadan, kōgetsudai)** (U Gardens: Dry garden): date of the present forms is uncertain, verify; possibly Edo
- [ ] **Braided-hat gate (amigasa-mon)** (U Gardens: Tea garden): verify date
- [ ] **Pine-needle spread (shiki-matsuba)** (U Gardens: Tea garden): verify date
- [ ] **Koto-bridge lantern (kotoji-dōrō)** (U Gardens: Stone lanterns by type): Kenroku-en is the famous one, off-map; verify date
- [ ] **Leaning lantern over water (rankei-dōrō)** (U Gardens: Stone lanterns by type): verify date
- [ ] **Wet-heron lantern (nuresagi-dōrō)** (U Gardens: Stone lanterns by type): verify form and date
- [ ] **Natural-stone lantern (yama-dōrō)** (U Gardens: Stone lanterns by type): verify date
- [ ] **Coin-shaped basin (zeni-gata)** (U Gardens: Basins): verify date
- [ ] **Water harp (sui-kinkutsu)** (U Gardens: Basins): Edo origin claimed]` (verify)
- [ ] **Kōetsu-ji fence (kōetsu-gaki)** (U Gardens: Fences): early 17th c.; verify name date
- [ ] **Ginkaku-ji fence (ginkakuji-gaki)** (U Gardens: Fences): verify date
- [ ] **Kinkaku-ji fence (kinkakuji-gaki)** (U Gardens: Fences): verify date
- [ ] **Ryōan-ji fence (ryōanji-gaki)** (U Gardens: Fences): verify; possibly Meiji name
- [ ] **Ōtsu fence (ōtsu-gaki)** (U Gardens: Fences): verify date
- [ ] **Gun-barrel fence (teppō-gaki)** (U Gardens: Fences): verify date
- [ ] **Blind fence (misu-gaki)** (U Gardens: Fences): verify date
- [ ] **Daitoku-ji fence (daitokuji-gaki)** (U Gardens: Fences): verify date
- [ ] **Straw-coat fence (mino-gaki)** (U Gardens: Fences): verify date
- [ ] **Bush-clover fence (hagi-gaki)** (U Gardens: Fences): verify date
- [ ] **Straw snow shelters (yuki-gakoi)** (U Gardens: Planting craft and tree supports): verify date
- [ ] **Straw trunk wraps against insects (komo-maki)** (U Gardens: Planting craft and tree supports): verify date
- [ ] **Goldfish (kingyo)** (U Gardens: Garden fauna and small living features): Yamato-Kōriyama breeding from about 1724 (verify)
- [ ] **Glass goldfish bowl (kingyo-dama)** (U Gardens: Garden fauna and small living features): `[outside 1680-1750: 19th c.]` (verify)
- [ ] **Cranes kept in a garden (tsuru)** (U Gardens: Garden fauna and small living features): Okayama Kōrakuen, verify date
- [ ] **Temple pigeons and feed sellers (hato, mame-uri)** (U Gardens: Garden fauna and small living features): verify date
- [ ] **Rows of donated torii (senbon torii)** (U Religious: Torii by style): The dense tunnel form is mostly later; donation of torii was growing in the Edo period; verify for 1730.
- [ ] **Three-legged torii (mihashira torii)** (U Religious: Torii by style): `[outside 1680-1750: present form 1831]` (verify)
- [ ] **Other messenger statues (tsukai)** (U Religious: Shrine forecourt): Tenjin, verify date for stroking bulls
- [ ] **Other messenger statues (tsukai)** (U Religious: Shrine forecourt): stone monkeys (Hie), bulls (Tenjin, verify date for stroking bulls), wolves (Mitsumine, rural) (verify)
- [ ] **Fortune slips (omikuji) and lot box (mikuji-bako)** (U Religious: Shrine forecourt): Tying slips to trees or lines: verify for 1730.
- [ ] **Donated banners (hōnō nobori)** (U Religious: Shrine forecourt): verify how dense in 1730
- [ ] **Donor-named stone fence posts (hōnō tamagaki)** (U Religious: Shrine forecourt): verify date
- [ ] **Hundred-times stone (hyakudo-ishi)** (U Religious: Shrine forecourt): verify date
- [ ] **Donated sake casks display (kazari-daru)** (U Religious: Shrine forecourt): `[outside 1680-1750: likely later]` (verify)
- [ ] **Pilgrim name slips on gates (senja-fuda)** (U Religious: Shrine forecourt): `[outside 1680-1750: craze late 18th c.]` (verify)
- [ ] **Fuji mound (Fuji-zuka)** (U Religious: Shrine forecourt): `[outside 1680-1750: first 1780, Takata]` (verify)
- [ ] **Big gates (sanmon, niōmon, sōmon)** (U Religious: Temple forecourt): straw sandals hung on them by pilgrims (verify)
- [ ] **Six Jizō of Edo (Edo roku Jizō)** (U Religious: Temple forecourt): verify each site
- [ ] **Temple approach shops (nakamise)** (U Religious: Temple forecourt): at Sensō-ji locals were allowed stalls in return for cleaning duty in the Genroku–Kyōhō years (verify)
- [ ] **Stele on a turtle (kifu)** (U Religious: Stone monuments): verify how common in 1730 Japan
- [ ] **Haiku stone (kuhi)** (U Religious: Stone monuments): verify first dates
- [ ] **Stone arhats (rakan)** (U Religious: Stone monuments): Temple, rare. (verify)
- [ ] **Pilgrimage miniature course (utsushi fudasho)** (U Religious: Stone monuments): verify earliest dates
- [ ] **Diagonal laying (tanigi-zumi, otoshi-zumi)** (U Castle: Castle stone walls): `[outside 1680-1750: late Edo]` (verify)
- [ ] **Hidden port (kakushi-zama)** (U Castle: Castle walls): verify common
- [ ] **Horse-exit barbican (umadashi)** (U Castle: Castle walls): verify for 1730 state
- [ ] **Mounted archery course (yabusame-ba)** (U Castle: Samurai quarter and parade grounds): verify details
- [ ] **Long-range temple archery lane (tōshiya)** (U Castle: Samurai quarter and parade grounds): moved 1698, rebuilt 1701, verify
- [ ] **Gun range (teppō-ba)** (U Castle: Samurai quarter and parade grounds): Edo had several; verify names
- [ ] **Doll market (hina-ichi)** (U Festivals: Markets and fairs): Jukkendana, Edo; verify date
- [ ] **Bon market (kusa-ichi)** (U Festivals: Markets and fairs): stalls selling Bon altar goods (reed mats, lotus leaves, lanterns) before Obon (verify)
- [ ] **Rake fair (tori-no-ichi)** (U Festivals: Markets and fairs): verify date; late 18th c. growth
- [ ] **Rice exchange street (Dōjima kome-ichiba)** (U Festivals: Markets and fairs): Flag or signal relays of prices to other towns: verify date.
- [ ] **Rag market (boro-ichi)** (U Festivals: Markets and fairs): from 1578; verify continuity
- [ ] **Tall Bon lantern (takatōrō)** (U Festivals: Festival sets and seasonal dressing): verify date
- [ ] **Bon dance tower (bon-odori yagura)** (U Festivals: Festival sets and seasonal dressing): verify; the tower-in-the-circle form may be later
- [ ] **Carp streamers (koinobori)** (U Festivals: Festival sets and seasonal dressing): verify: likely `[outside 1680-1750: mid–late 18th c.]`; banners and streamers are safe for 1730
- [ ] **Tanabata bamboo (tanabata-dake)** (U Festivals: Festival sets and seasonal dressing): verify for 1730
- [ ] **Kimono-curtain picnic (kosode-maku)** (U Festivals: Festival sets and seasonal dressing): verify date
- [ ] **Small-bow archery booth (yōkyūba)** (U Festivals: Entertainment grounds and stages): verify date
- [ ] **Set-piece frame (shikake-hanabi)** (U Festivals: Fireworks and river events): verify date
- [ ] **Hand fireworks sold in the street (te-hanabi, hanabi-uri)** (U Festivals: Fireworks and river events): verify date
- [ ] **Townsmen's fireworks ban** (U Festivals: Fireworks and river events): 1648 and repeated; verify
- [ ] **Food-selling boats among the party boats (uroro-bune)** (U Festivals: Fireworks and river events): verify name
- [ ] **Handheld tube fireworks (tezutsu hanabi)** (U Festivals: Fireworks and river events): verify date
- [ ] **Farmers' rockets (ryūsei)** (U Festivals: Fireworks and river events): verify date

## 8.M Merge agent

- [ ] Every contradiction in §3.3 (each is a two-source disagreement nobody re-checked).
- [ ] W ajiro stake weirs: still worked in 1730, or only a memory? (era-rule fix, §2 W §9)
- [ ] R chain pump: rare but present in 1730, or truly gone? (era-rule fix, §2 R §2)
- [ ] Size classes in §1 were read off each entry's wording (N by group); spot-check before using the table for budgets.
