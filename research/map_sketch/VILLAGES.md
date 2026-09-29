# Real villages and in-between roads (research agent VIL, 2026-09-29)

Data for `map_sketch.py`: `roads.json` (12 roads) and `villages.json` (70 villages: 30 rice, 28 mountain, 12 fishing). Everything existed in 1730. Positions are modern GSI / Wikipedia coordinates for the village's modern ōaza or district. Spacing was checked with a script against the tables in `map_sketch.py`: every village is at least 10 km from every other village and at least 8 km from every station, castle town and city (one exception, flagged below). No yields, sizes or wealth, as asked.

## Roads

| Road | Japanese | Route | Source (existed in 1730) |
|---|---|---|---|
| Chūma road | 中馬街道 (三州街道 / 伊那街道) | Okazaki up the Tomoe and Asuke valleys, over the Inabu uplands (Neba, Hiraya, Namiai) to Iida, then north up the Ina valley to Shiojiri; the pack-horse (chūma) salt and goods road from the Mikawa coast into Shinano. | ja.wikipedia 飯田街道 / 三州街道 (Sanshū or Chūma kaidō, one of the Nagoya/Okazaki-Iida roads mapped 1701-1840); the Chūma carriers' rights were confirmed by the shogunate in 1764, but they had worked the road since the 1600s; Iijima jin'ya on it from 1677. |
| Akiba road | 秋葉街道 | Kakegawa - Mori - Inui to the Akiha fire-god shrine, then north along the Median Tectonic Line: Misakubo, Aokuzure pass, Tōyama (Wada, Kamimura), Ōshika, Bunkui pass, Takatō, Tsuetsuki pass to Suwa (Chino). An old salt road turned pilgrim road. | ja.wikipedia 秋葉街道 (Kakegawa - Mori - Ichinose - Inui - Sakashita - Akiha-san; earlier a salt road, Edo-period Akiha pilgrimage); pass positions from GSI. |
| Suruga road | 駿州往還 (河内路 / 身延道) | Okitsu on the Tōkaidō up the Fuji River gorge through Manzawa, Nanbu, Minobu, Shimoyama and Iwama to Kajikazawa, then across the basin to Kōfu. The Minobu pilgrims' road; the river beside it carried boats from 1607. | ja.wikipedia 駿州往還 (Kawauchi-ji / Minobu-michi, Kōfu - Okitsu, relay stations Iwama, Shimoyama, Nanbu, Manzawa listed under the Anayama; Sengoku-era road kept in the Edo period). |
| Kamakura road | 鎌倉往還 (御坂路) | Kōfu - Isawa - Kurokoma - Misaka pass - Kawaguchi - Yoshida - Lake Yamanaka - Kagosaka pass - Subashiri - Gotemba; beyond Gotemba it crossed the Ashigara pass (shared with the Yagurazawa road). The Fuji-pilgrim and Kai-to-Sagami road. | MLIT Kantō 'Misaka / Kamakura-ōkan' page and Agency for Cultural Affairs 'Rekishi no michi 100' (1996); post-horse stations at Isawa, Kawaguchi and near Kagosaka; oldest recorded Kai road (Engi-shiki). |
| Yagurazawa road | 矢倉沢往還 (大山街道) | Edo (Akasaka gate) - Sangenjaya - Futako ferry - Nagatsuta - Atsugi - Isehara (for Ōyama) - Hadano - Matsuda - Sekimoto - Yagurazawa checkpoint - Ashigara pass - Gotemba - Numazu. The Ōyama pilgrims' road and the Tōkaidō's back door. | ja.wikipedia 矢倉沢往還 (Akasaka-mon to Numazu via Ashigara pass, a waki-ōkan of the Tōkaidō; called Ōyama kaidō from the mid-Edo pilgrim boom). |
| Nakahara road | 中原街道 | Edo (Toranomon) - Maruko ferry - Kosugi - Saedo - Seya - Yoda - Sagami River - Nakahara (Hiratsuka): a straight inland short-cut used by carters and merchants dodging the Tōkaidō. | ja.wikipedia 中原街道 (so named after the shogunate's 1604 works; relay points Kosugi, Saedo, Seya, Yoda). |
| Shimo-kaidō | 下街道 (善光寺道) | Nagoya - Kachigawa - Sakashita - Utsu pass - Ikeda - Tajimi - Takayama - Toki - Kamado - Makigane fork on the Nakasendō near Ōi: the busy 'back road' from Nagoya to the Kiso road and Zenkō-ji. | ja.wikipedia 下街道 (善光寺道): side road of the Nakasendō, stages listed in the 1765 Tōkai Kiso ryōdōchū; unofficial (no licensed stations) but in use through the Edo period. |
| Kami-kaidō | 上街道 (木曽街道) | Nagoya - Kusunoki - Komaki - Gakuden - Haguro - Zenshiji - Fushimi on the Nakasendō: the Owari domain's official road to the Kiso valley. | ja.wikipedia 上街道 (木曽街道): Owari domain road, Komaki post laid out 1623-1628, joins the Nakasendō at Fushimi-juku. |
| Yamato road | 大和街道 (加太越奈良道) | Seki on the Tōkaidō - Kabuto pass - Tsuge - Sanago - Iga Ueno - Shimagahara - Kasagi - Kamo - Kizu - Nara: the Iga road, a short-cut from the Tōkaidō to Nara and on to Osaka. | Mie Prefecture 'Mie no rekishi kaidō: Yamato kaidō' (bunka.pref.mie.lg.jp); Edo name Kabuto-goe Nara-michi; ex-Tōkaidō of the Nara period. |
| Kuragari road | 暗越奈良街道 | Osaka (Tamatsukuri) east across the Kawachi plain to Hiraoka, over the steep Kuragari pass in the Ikoma hills and down to Nara: the shortest Osaka-Nara road, busy with Ise pilgrims. | ja.wikipedia 暗越奈良街道 (Nara-period origin; Edo-period secondary road with inns, daimyō and Ise-pilgrim traffic). |
| Godaisan road | 御代参街道 | Tsuchiyama on the Tōkaidō north through Kamagake, Ishihara (Hino), Okamoto, Yōkaichi and Obata to the Nakasendō near Echigawa: a true cross-road between the two highways, used by the court's proxy pilgrims to Ise and Taga. | ja.wikipedia 御代参街道 (opened 1640 for Kasuga-no-Tsubone's Ise-to-Taga pilgrimage; the name itself is only attested late, 1868). |
| Saku road | 佐久甲州街道 (佐久往還) | Nirasaki on the Kōshū road - Wakamiko - Nagasawa - Hirasawa pass (Nobeyama) - Umi-no-kuchi - down the Chikuma River via Takanomachi and Nozawa to Iwamurada on the Nakasendō: joins the Kōshū road to the Nakasendō behind Yatsugatake. | sakucci.or.jp 'Saku rekishi no michi: Saku-Kōshū-dō' (Nirasaki - Iwamurada, about 18 ri; relay villages Nakajō, Wakamiko, Nagasawa, Hirasawa, Umi-no-kuchi, Umijiri, Kaminohata, Takanomachi, Nozawa); medieval Zenkō-ji road and Takeda military road. |

Overlaps with roads already in the script: the Chūma road north of Iida is the same road as the script's `Ina road`, and its line is more accurate, so it could replace it. The Kamakura road and the Yagurazawa road meet at Gotemba and share the Ashigara pass. The script's `Ise road` (Yokkaichi-Tsu-Ise) is left as it is; the Yamato road is the Iga road.

## Villages by road

### Chūma road

- **Matsudaira** (松平) rice, 35.0456, 137.2624. Hill-valley village where the Matsudaira (later Tokugawa) clan began; clan temple Kōgetsu-in.
- **Asuke** (足助) mountain, 35.1354, 137.3182. Chūma road post village where coastal salt was repacked for the mountains ('Asuke salt').
- **Busetsu** (武節) mountain, 35.2075, 137.5072. Inabu uplands post village below the ruined Busetsu castle.
- **Hiraya** (平谷) mountain, 35.3233, 137.6303. High pass village on the Mikawa-Shinano border; forestry and charcoal. Namiai checkpoint is 8 km on.
- **Komaba** (駒場) mountain, 35.4454, 137.7383. Achi post village; the story says Takeda Shingen died near here in 1573.
- **Iijima** (飯島) rice, 35.6841, 137.8974. Ina valley village with the shogunate's intendant office (Iijima jin'ya, 1677).
- **Miyada** (宮田) rice, 35.7689, 137.9444. Ina road post village on the Tenryū terraces below the Central Alps.
- **Matsushima** (松島) rice, 35.9150, 137.9820. Minowa's Ina road post village at the north end of the Ina valley.

### Akiba road

- **Mori** (森) rice, 34.8346, 137.9238. Market village at the foot of the Akiba road; Oguni shrine (Tōtōmi's first shrine) nearby.
- **Inui** (犬居) mountain, 34.9511, 137.9109. Gate village for Akiha-san, below the ruined Inui castle; pilgrims' inns.
- **Misakubo** (水窪) mountain, 35.1587, 137.8684. Mountain market village below Aokuzure pass; Nishiure dengaku field-dance.
- **Wada** (和田) mountain, 35.3197, 137.9345. Chief village of the Tōyama valley; Shimotsuki fire-and-hot-water festival.
- **Kashio** (鹿塩) mountain, 35.5850, 138.0400. Ōshika village with a mountain salt spring ('deer salt'), rare far from the sea.
- **Ichinose** (市野瀬) mountain, 35.7281, 138.0701. Hase valley relay village below Bunkui pass, on the way to Takatō.

### Suruga road

- **Manzawa** (万沢) mountain, 35.2043, 138.5049. Border relay village between Suruga and Kai on the Fuji River road.
- **Nanbu** (南部) rice, 35.2898, 138.4475. Relay village on the Fuji River; the place the Nanbu clan took its name from.
- **Kajikazawa** (鰍沢) rice, 35.5466, 138.4599. Head port of the Fuji River boats (from 1607): Kai's tax rice went down, Suruga salt came up.

### Kamakura road

- **Kurokoma** (黒駒) mountain, 35.6000, 138.7000. Misaka road village; named for the legendary black horse of Kai.
- **Subashiri** (須走) mountain, 35.3609, 138.8672. Fuji pilgrims' east trailhead; buried under the 1707 Hōei eruption ash and rebuilt.

### Yagurazawa road

- **Mizonokuchi** (溝口) rice, 35.5998, 139.6132. Ōyama road post village at the Futako ferry over the Tama River.
- **Atsugi** (厚木) rice, 35.4424, 139.3699. Sagami River ferry and market village on the Ōyama road.
- **Ōyama** (大山) mountain, 35.4280, 139.2460. Pilgrim-lodge (oshi) village at the foot of Ōyama and its Afuri shrine; Edo craftsmen came in summer.
- **Sekimoto** (関本) rice, 35.3212, 139.1035. Post village at the foot of Ashigara pass; gate of the Daiyūzan Saijō-ji temple.
- **Fukara** (深良) rice, 35.2065, 138.9151. Watered by the Hakone irrigation tunnel from Lake Ashi (finished 1670).

### Nakahara road

- **Seya** (瀬谷) rice, 35.4685, 139.4924. Relay village of the Nakahara road on the Sagami upland.

### Shimo-kaidō

- **Sakashita** (坂下) rice, 35.2841, 137.0235. Shimo-kaidō stage below Utsu pass.
- **Tajimi** (多治見) rice, 35.3328, 137.1322. Shimo-kaidō village on the Toki River; Mino-ware kilns in the hills around.

### Kami-kaidō

- **Komaki** (小牧) rice, 35.2957, 136.9172. Post village (laid out 1623-28) under Komaki-yama, Nobunaga's castle hill and Ieyasu's 1584 camp.

### Yamato road

- **Tsuge** (柘植) mountain, 34.8460, 136.2500. Iga border post village below Kabuto pass; ninja country, and one of Bashō's claimed birthplaces.
- **Kasagi** (笠置) mountain, 34.7539, 135.9396. Village under Kasagi-dera, Emperor Go-Daigo's 1331 mountain stronghold, on the Kizu River.
- **Kizu** (木津) rice, 34.7346, 135.8209. River port on the Kizu where timber and goods for Nara were landed.

### Kuragari road

- **Hiraoka** (枚岡) rice, 34.6691, 135.6562. Village at Hiraoka shrine (Kawachi's first shrine), foot of the Kuragari pass.

### Godaisan road

- **Hino** (日野) rice, 35.0104, 136.2579. Home village of the Hino merchants (Ōmi pedlars); lacquerware and travelling medicine.

### Saku road

- **Nagasawa** (長沢) mountain, 35.8729, 138.4249. Saku road relay village on the Yatsugatake skirts.
- **Umi-no-kuchi** (海ノ口) mountain, 35.9932, 138.4427. Upland relay village; Umi-no-kuchi castle, where young Takeda Shingen won his first fight (1536, legend).
- **Takanomachi** (高野町) rice, 36.1600, 138.4767. Relay and market village in the upper Chikuma valley.

### Between the roads (not on a listed road)

- **Oyashiki** (小屋敷) rice, 35.7315, 138.7137. Village around Erin-ji, the Takeda family temple with Shingen's grave; Katsunuma's vineyards are 7 km south.
- **Ashikura** (芦倉) mountain, 35.6378, 138.3803. Last village below the Southern Alps (today's Ashiyasu); forestry and charcoal.
- **Yamura** (谷村) rice, 35.5516, 138.9055. Gunnai market village on the Katsura River; Gunnai silk (kaiki). Castle town until 1704.
- **Dōshi** (道志) mountain, 35.5159, 139.0136. Long valley village on the Dōshi road between Sagami and Lake Yamanaka; charcoal.
- **Umegashima** (梅ヶ島) mountain, 35.3100, 138.3200. Head of the Abe valley; old gold diggings and a hot spring.
- **Utōgi** (有東木) mountain, 35.2052, 138.3770. Abe valley hamlet said to be where wasabi was first grown (early 1600s), presented to Ieyasu.
- **Ieyama** (家山) mountain, 34.9560, 138.0401. Ōi River valley village (Kawane); tea and timber rafts.
- **Futamata** (二俣) rice, 34.8645, 137.8158. Tenryū River landing for timber rafts; Futamata castle ruin (Nobuyasu's death, 1579). On the Hamamatsu branch of the Akiba road.
- **Kiga** (気賀) rice, 34.8028, 137.6326. Himekaidō checkpoint village at the north inlet of Lake Hamana (checkpoint from 1601).
- **Nagashino** (長篠) rice, 34.9320, 137.5657. Village under Nagashino castle; the 1575 battlefield of Shitaragahara is just west.
- **Taguchi** (田口) mountain, 35.0971, 137.5723. Chief village of the Shitara uplands on the Mikawa-Shinano back road.
- **Nagakute** (長久手) rice, 35.1842, 137.0486. Farming village on the 1584 Komaki-Nagakute battlefield.
- **Seki** (関) rice, 35.4958, 136.9178. Mino sword-smiths' village (Seki blades); also knives and tools.
- **Warabi** (蕨生) mountain, 35.5888, 136.8902. Makidani paper village: hon-Minogami, the best shōji paper.
- **Takasu** (高須) rice, 35.2171, 136.6226. Ring-levee (wajū) village in the Kiso-Nagara-Ibi delta; Takasu domain seat from 1700.
- **Tsushima** (津島) rice, 35.1771, 136.7414. Village-town around Tsushima shrine; summer lantern-boat festival; river port.
- **Shigaraki** (信楽) mountain, 34.8810, 136.0472. Shigaraki pottery kilns; its tea jars carried the shogun's Uji tea.
- **Kashiwara** (柏原) rice, 34.5783, 135.6292. Kawachi cotton village at the new Yamato River mouth (rerouted 1704); Kashiwara cargo boats.
- **Tokorozawa** (所沢) rice, 35.8001, 139.4687. Market village on the dry Musashino upland.
- **Ōme** (青梅) mountain, 35.7874, 139.2753. Tama River rafting village at the edge of the hills; Ōme-jima striped cloth.
- **Ōhara** (大原) mountain, 35.1215, 135.8349. Hill village north-east of Kyoto on the Wakasa (mackerel) road; Ōhara women carried firewood to the city; Sanzen-in.
- **Chichibu** (秩父大宮) mountain, 36.0031, 139.0861. Chichibu Ōmiya: Chichibu shrine, silk markets and the 34 Kannon pilgrimage.
- **Nojima** (野島) fishing, 35.3263, 139.6348. Kanazawa fishing village by the Eight Views of Kanazawa; salt pans nearby.
- **Misaki** (三崎) fishing, 35.1424, 139.6208. Tip of Miura: tuna and bonito boats, and an anchorage for ships bound for Edo.
- **Manazuru** (真鶴) fishing, 35.1517, 139.1418. Fishing and stone-quarry village; its Komatsu stone built Edo castle's walls.
- **Itō** (伊東) fishing, 34.9677, 139.1172. Izu fishing village where William Adams built Western ships for Ieyasu (1604-05).
- **Heda** (戸田) fishing, 34.9725, 138.7783. Fishing village in a sheltered hook-shaped harbour on west Izu.
- **Omaezaki** (御前崎) fishing, 34.6044, 138.2161. Cape fishing village with the shogunate's beacon (Miobi light, 1635).
- **Irago** (伊良湖) fishing, 34.5899, 137.0434. Fishing village at the tip of Atsumi; Bashō visited in 1687.
- **Morozaki** (師崎) fishing, 34.7024, 136.9666. Fishing village at the tip of Chita.
- **Tokoname** (常滑) fishing, 34.8961, 136.8545. Chita coast kiln-and-harbour village: Tokoname jars shipped by sea.
- **Shiroko** (白子) fishing, 34.8295, 136.5882. Ise-bay port and fishing village; Ise katagami dye-stencil makers.
- **Kitakomatsu** (北小松) fishing, 35.2594, 135.9617. Lake Biwa fishing village under the Hira mountains.
- **Sugaura** (菅浦) fishing, 35.4559, 136.1462. Self-governing lakeside fishing village with gated entrances, north Lake Biwa.

Fishing villages are in the last group with road `""`: Nojima, Misaki, Manazuru, Itō, Heda, Omaezaki, Irago, Morozaki, Tokoname, Shiroko, Kitakomatsu and Sugaura (the last two on Lake Biwa).

## Doubts and near-misses

- Sakashita and Komaki are 9.7 km apart, just under the 10 km rule. Drop one if it matters (verify).
- Tsuge was placed at the west edge of its district so it clears Sakanoshita station by 8.2 km; the modern station sits 8.0 km away (verify).
- Ōyama (the pilgrim village) is 5 km up a spur from the Yagurazawa road at Isehara; `road` says Yagurazawa road because that is the road its pilgrims walked.
- Futamata is on the Hamamatsu branch of the Akiba road, not the Kakegawa line drawn in roads.json, so its `road` is blank.
- Several "villages" were really market towns legally ranked as mura (Tsushima, Chichibu Ōmiya, Tokorozawa, Ōme, Yamura, Tajimi). Fine for a map; swap them out if you want strictly farm hamlets.
- Umegashima's hamlets run 10 km up the Abe valley (35.24-35.34); the point is the upper hamlets near the old gold diggings (verify).
- Kashio is placed between Ōshika village office and the salt spring (verify).
- Kurokoma's point is the settlement on the Misaka road, not the district centre, which lies up in the hills (verify).
- Road lines between the listed stages are approximate (5-15 points along the valley); the Chūma road's Okazaki-Asuke section via Matsudaira and the Godaisan road's Okamoto-Obata points are the least certain (verify).
- Asuke salt, the Komaba Shingen story, the Umi-no-kuchi 1536 battle and Tsuge as Bashō's birthplace are traditions, not settled history.
- The Chūma carriers' formal licence dates from 1764; the road and the pack-horse trade were already running in 1730.
- The Godaisan road dates from 1640, but its name is only attested in 1868. Call it the Hino road or the Taga road if you want a name people used in 1730.
- Left out for spacing (real and 1730-valid, usable if the spacing rule relaxes): Kawaguchi (Fuji lodge village, 7.6 km from Sasago), Namiai checkpoint (7.8 km from Hiraya), Katsunuma vineyards (7 km from Oyashiki), Nishijima paper (6.5 km from Kajikazawa), Seto pottery (8.7 km from Sakashita), Yaizu bonito port (5.5 km from Fujieda), Okishima island (6.3 km from Musa), Kamimura (8 km from Wada), Yao and Hirano (Kawachi, crowded), Fukude (6.6 km from Mitsuke).
- Sugaura is 4 km from the Chikubushima landmark, Kizu 6 km from Nara, Ōhara 6.5 km from Sakamoto: these are landmarks rather than stations, so the rule does not apply, but they will sit close on the map.
- Coastline: Morozaki, Irago and Tokoname sit where the script's rough coast polygon may draw sea. The coordinates are the real ones, so the coast will need a tweak rather than the villages.

## Sources

- GSI address search (msearch.gsi.go.jp) for village, pass and station coordinates; ja.wikipedia coordinates for 上村, 南信濃村, 大鹿村, 戸田村, 須走村, 鰍沢町, 長谷村, 秋葉山本宮秋葉神社, 大山阿夫利神社, 御前埼灯台.
- ja.wikipedia: 中原街道, 御代参街道, 矢倉沢往還, 秋葉街道, 下街道 (善光寺道), 上街道 (木曽街道), 暗越奈良街道, 飯田街道, 駿州往還, 飯島陣屋, 芦安村 (Ashikura + Antsū villages merged in 1875).
- sakucci.or.jp 'Saku-Kōshū-dō'; bunka.pref.mie.lg.jp 'Yamato kaidō'; MLIT Kantō 'Misaka / Kamakura-ōkan'; tokokai.org and omaesaki-lighthouse.jp (Miobi light, 1635); bunka.go.jp hon-Minogami (Warabi, Makidani).
