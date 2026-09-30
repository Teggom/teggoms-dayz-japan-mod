# Every settlement on the map sketch -> waterway types. Research agent WW, 2026-09-29.
# One row per settlement (duplicates across tables merged). Columns, separated by " | ":
#   name | listed in | primary | all types | real waterway(s) | source keys | water (sea / pond / lake / none) | flag
# listed-in codes: C cities, CT castle towns, T Tokaido, K Kyokaido, N Nakasendo, KO Koshu, O onsen, TT temple towns,
#   P ports, S salt, V:<kind> villages.json, L KEEP_LANDMARKS; a trailing * = KEY_POST.
# Source "mem" = general knowledge, not re-checked this session: verify before a build list relies on it.
# Every town also has d1 (house-front gutters) by default; d1 is listed only where it is the main or only waterway.

ROWS = r"""
Edo | C,T,N,KO | a | a1,a2,c1,f1,g1,d1 | Nihonbashi River, Dosanbori, Kyobashi River, Sanjukkenbori (30 ken, 1612), Hacchobori, Kaede-gawa, Onagi-gawa, Tatekawa (1659), Fukagawa log ponds (kiba); Sumida River (Ryogoku 1659-61, Shin-Ohashi 1693, Eitai 1698, levee cherries 1717); castle inner and outer moats (1636) | S-30K S-SUMI S-EDOM OL | sea |
Kyoto | C,T,K | b | b1,c1,f1,d1 | Takase River (1611; 9 funairi); Kamo River (Kanbun new levee 1670; Sanjo Ohashi 61 x 3 ken); Nijo castle moat; the small Horikawa | S-TAK S-KAMO S-YUKA | pond |
Osaka | C,K | a | a1,c1,f1,g1,d1 | Higashi-yokobori (1585), Nishi-yokobori (1600), Dotonbori (1612-15), Edobori (1617), Nagahori, Dojima River and the Nakanoshima kura-yashiki boat basins; Okawa (Yodo) with Tenma-bashi and Naniwa-bashi; castle moats; back-to-back sewers | S-OSK S-KURA OL | sea |
Nara | L | d | d1,e1 | Saho and Yoshiki rivers; Sarusawa pond | mem | pond |
Ise (Yamada and Uji) | L | a | a3,c3,d1 | Seta River with the Kawasaki kura quarter (kura straight onto the water); Isuzu River with the stone-paved mitarashi washing place | S-ISE | pond | Kawasaki can be sea-level if Ise sits on the bay
Koya | L | e | e2,d1 | mountain streams; the Tamagawa at Okunoin | mem | pond | nudged inside the SW corner (KEEP_LANDMARKS)
Odawara | CT,T | f | f1,c2,c3,g2 | castle moats; Sakawa River porters' crossing to the east; Hayakawa; the beach | OL mem | sea |
Sunpu (Tokaido Fuchu) | CT,T | f | f1,c2,d1 | Sunpu castle's triple moats; Abe River porters' crossing | OL mem | pond |
Nagoya | CT | a | a1,f2,d1 | Horikawa canal (1610; 12-48 ken) from the castle to Atsuta, merchant kura upstream of Nayabashi and the domain rice stores below | S-NGY mem | sea | Horikawa was tidal to Atsuta: sea-level if Nagoya is placed near the bay
Hikone | CT | f | f1,g3,d1 | three wet moats; the Matsubara inner lake; Lake Biwa shore | mem | lake |
Kofu | CT,KO | f | f1,d1,e1 | Kofu castle moats (shogunal from 1724) | mem | pond |
Hamamatsu | CT,T | f | f1,d1 | castle on the terrace edge, moats partly dry | mem | pond |
Okazaki | CT,T | f | f1,c1,c3,d1 | castle moats; Yahagi River with Yahagi-bashi (208 ken, the Tokaido's longest); Sugo River under the castle | S-YAH l04 l05 | pond |
Kuwana | CT,T | f | f1,g1,c1 | water castle on the Ibi / Nagara / Kiso mouths; Shichiri ferry landing (the sea crossing from Miya) | mem | sea |
Takasaki | CT,N | f | f1,c3,d1 | castle moats; Karasu River | mem | pond |
Matsumoto | CT | f | f1,c3,d1 | wet moats up to ~50 m; Metoba River; town springs and wells | S-MTM mem | pond |
Ogaki | CT | f | f1,b2,g1 | water castle; the Suimon-gawa boat route to Kuwana with the Funamachi river port and the Sumiyoshi lantern (~8 m, 1688-1704) | S-OGK | pond |
Yoshida | CT,T | f | f1,c1,d1 | castle on the Toyo River; Yoshida Ohashi | mem | pond |
Kakegawa | CT,T | f | f1,c3,d1 | castle moats; Sakagawa | mem | pond |
Kameyama | CT,T | f | f1,d1 | hill castle with ponds as moats | mem | pond |
Zeze | CT | f | f1,g3 | water castle, stone walls standing in Lake Biwa | mem | lake |
Iida | CT | f | f2,e2,d1 | spur castle with dry moats above the Tenryu | mem | none |
Takato | CT | f | f2,e2 | hill castle, dry moats | mem | none |
Ueda | CT | f | f1,c1,d1 | castle moats; the Chikuma River under the Amagafuchi cliff | mem | pond |
Komoro | CT | f | f2,c1 | castle set below the town with dry ravine moats; Chikuma River below | mem | none |
Tanaka | CT | f | f3,d1,e1 | four concentric round wet moats, ~600 m across | S-TNK | pond |
Iga Ueno | CT | f | f1,d1 | wet moat under very high stone walls (Todo, 1611) | mem | pond |
Inuyama | CT | f | f2,c1 | hill castle over the Kiso River | mem | pond |
Yodo | CT,K | f | f1,c1 | water castle at the Katsura / Uji / Kizu confluence; two great waterwheels (8 and 6 ken across) | S-YODO | pond |
Numazu | CT,T | c | c1,g1,d1 | Kano River mouth landing | S-NMZ mem | sea | NO castle in 1730: Numazu castle was built 1777-79 (the older Sanmaibashi castle was abandoned 1614). Treat as a post town + river port
Shinagawa | T* | g | g2,c3,d1 | Edo Bay shore, houses backing onto the beach; Meguro River mouth | mem | sea |
Kawasaki | T* | c | c1,d1 | Tama River: Rokugo ferry (the bridge was lost in 1688) | OL | sea |
Kanagawa | T,P | g | g1,d1 | Kanagawa port and bay landing | mem | sea | merges the PORTS entry "Kanagawa port"
Hodogaya | T | d | d1,e1 | Katabira River | mem | pond |
Totsuka | T* | d | d1,c3 | Kashio River (Totsuka Ohashi) | mem | pond |
Fujisawa | T | d | d1,c3 | Sakai River | mem | pond |
Hiratsuka | T | c | c1,d1 | Sagami River: Banyu ferry | mem | pond |
Oiso | T | d | d1,g2 | the beach | mem | sea |
Hakone | T | g | g3,d1 | Lake Ashi landing beside the checkpoint | KL mem | lake |
Mishima | T* | d | d3,d1 | spring streams from Kohama pond: Genbei-gawa (late-16th-c. channel, 1.5 km), Sakura-gawa; Mishima shrine | S-MSM | pond |
Hara | T | d | d1,e1 | Ukishima marsh behind the dunes | mem | none |
Yoshiwara | T* | c | c2,d1,e1 | Fuji River crossing (ferry) to the west | mem | pond |
Kanbara | T | c | c2,g2,d1 | Fuji River mouth; salt beach | mem | sea |
Yui | T* | d | d1,c3,g2 | Yui River; the beach under Satta pass | mem | sea |
Okitsu | T | c | c2,g2,d1 | Okitsu River porters' crossing; the beach | mem | sea |
Ejiri | T | c | c3,g1,d1 | Tomoe River down to Shimizu port | mem | pond |
Mariko | T* | d | d1,e1 | Mariko River (small) | mem | none |
Okabe | T | d | d1,e2 | Okabe River | mem | none |
Fujieda | T | d | d1,c3 | Seto River | mem | pond |
Shimada | T* | c | c2,d1 | Oi River east bank: river-crossing office, porter huts, gravel flats | KL OL | pond |
Kanaya | T* | c | c2,d1 | Oi River west bank | KL | pond |
Nissaka | T | d | d1,e2 | Sayo-no-Nakayama hills | mem | none |
Fukuroi | T* | d | d1,e1 | Hara River | mem | none |
Mitsuke | T | c | c1,d1 | Tenryu River (Ikeda ferry) to the west | mem | pond |
Maisaka | T | g | g3,d1 | Lake Hamana: Imagiri ferry landing | mem | sea |
Arai | T* | g | g3,d1 | lagoon shore; the checkpoint on the water; ferry landing | KL | sea |
Shirasuka | T | d | d1,g2 | coast; the village moved up the hill after the 1707 tsunami | mem | sea |
Futagawa | T | d | d1,e1 | small streams | mem | none |
Goyu | T | d | d1,e1 | small streams | mem | none |
Akasaka (Tokaido) | T* | d | d1,e1 | Otowa River (small) | mem | none |
Fujikawa | T | d | d1,e1 | small streams | mem | none |
Chiryu | T* | d | d1,e1 | small streams | mem | none |
Narumi | T | d | d1,e1 | tidal flats nearby | mem | none |
Miya | T,P | g | g1,a2,d1 | Miya harbour: the Shichiri ferry landing and lantern; the Horikawa mouth from Nagoya; Shirotori timber ponds | GAP mem | sea | merges the PORTS entry "Miya harbour"
Yokkaichi | T* | d | d1,c3,g1 | Mitaki River; small port | mem | sea |
Ishiyakushi | T | d | d1,e1 | small streams | mem | none |
Shono | T | d | d1,e1 | small streams | mem | none |
Seki (Tokaido) | T* | d | d1,c3 | Suzuka River | mem | pond |
Sakanoshita | T | e | e2,d1 | mountain stream below Suzuka pass | mem | pond |
Tsuchiyama | T | d | d1,e2 | valley stream | mem | none |
Minakuchi | T* | d | d1,f1,e1 | small castle (shogun's lodge 1634, domain seat from 1682) | mem | pond | a small castle town missing from CASTLE_TOWNS
Ishibe | T | d | d1,e1 | small streams | mem | none |
Kusatsu (Omi) | T*,N* | c | c3,d1 | Kusatsu River, a raised-bed river the road climbs over (the bed rose mostly from the late 1700s; tunnel 1886) | S-KST | pond | in 1730 the bank is lower than the famous 10 m: don't overbuild it
Otsu | T* | g | g3,d1 | Lake Biwa harbour | mem | lake |
Fushimi (Kyokaido) | K* | a | a3,b1,c1 | Fushimi port on the Horikawa / Uji-gawa branch; the south end of the Takase; Uji River; sanjikkoku passenger boats | S-FSM S-TAK | pond |
Hirakata | K* | c | c1,d1 | Yodo River landing; passenger boats and kurawanka food boats | OL | pond |
Moriguchi | K* | c | c1,d1,e1 | the Bunroku levee along the Yodo, with the road on top | mem | pond |
Itabashi | N* | d | d1,c3 | Shakujii River: the plank bridge that names the station | mem | pond |
Warabi (Nakasendo) | N | c | c1,d1 | Ara River: Toda ferry | mem | pond |
Urawa | N | d | d1,e1 | upland; paddies in the valleys | mem | none |
Omiya | N | d | d1,e1 | Hikawa shrine ponds | mem | none |
Ageo | N | d | d1,e1 | upland | mem | none |
Okegawa | N | d | d1,e1 | upland | mem | none |
Konosu | N | d | d1,e1 | Ara River plain | mem | none |
Kumagaya | N* | c | c1,d1 | Ara River levee (Kumagaya tsutsumi) | mem | pond |
Fukaya | N | d | d1,e1 | plain | mem | none |
Honjo | N* | c | c2,d1 | Kanna River crossing | mem | pond |
Shinmachi | N | d | d1,c3 | Karasu River | mem | pond |
Kuragano | N | c | c1,d1 | Karasu River landing (kashi): the top of the Tone boat route (takasebune) | S-KRG | pond |
Itahana | N | d | d1,c3 | Usui River | mem | pond |
Annaka | N | d | d1,c3 | Usui River | mem | pond |
Matsuida | N | d | d1,e2 | hill streams | mem | none |
Sakamoto (Nakasendo) | N | d | d1,e2 | foot of Usui pass | mem | none |
Karuizawa | N* | d | d1,e2 | Asama highland streams | mem | none |
Kutsukake | N | d | d1,e2 | Asama highland streams | mem | none |
Oiwake | N* | d | d1,e2 | Asama highland streams | mem | none |
Odai | N | d | d1,e2 | valley stream | mem | none |
Iwamurada | N | d | d1,e1 | Saku paddies | mem | none |
Shionada | N | c | c1,d1 | Chikuma River | mem | pond |
Yawata | N | d | d1,e1 | Saku paddies | mem | none |
Mochizuki | N* | d | d1,e1 | Kagami River | mem | none |
Ashida | N | d | d1,e1 | valley stream | mem | none |
Nagakubo | N | d | d1,e1 | Yoda River | mem | none |
Wada (Nakasendo) | N* | d | d1,e2 | below Wada pass | mem | none |
Shimo-Suwa | N*,KO* | d | d4,g3,d1 | hot-spring gutters; Lake Suwa | mem | lake |
Shiojiri | N | d | d1,e1 | upland | mem | none |
Seba | N | d | d1,e1 | valley | mem | none |
Motoyama | N | d | d1,e2 | valley | mem | none |
Niekawa | N | d | d1,e2 | upper Narai River | mem | none |
Narai | N* | d | d2,e2 | spring-fed water stations along the street (one roofed with stone-weighted boards); Narai River | S-NRI | none |
Yabuhara | N | d | d2,e2 | assumed like Narai | (assumed) | none |
Miyanokoshi | N | d | d1,e2 | Kiso River | mem | pond |
Fukushima (Kiso) | N | e | e2,d1 | Kiso River gorge under the checkpoint | KL mem | pond |
Agematsu | N | e | e2,d1 | Kiso River, Nezame no Toko | KL | pond |
Suhara | N | d | d2,e2 | log water troughs along the street | mem | none |
Nojiri | N | d | d1,e2 | Kiso valley | mem | none |
Midono | N | d | d1,e2 | Kiso valley | mem | none |
Tsumago | N* | d | d2,e2 | street channels and troughs; Ranagawa | mem | none |
Magome | N* | d | d2,e2 | stepped street with a side channel | mem | none |
Ochiai | N | d | d1,e2 | valley stream | mem | none |
Nakatsugawa | N* | d | d2,c3 | channel down the centre of the main street (fire water, on the Nakasendo survey map; filled 1880); Nakatsu River | S-NKT | none |
Oi (Ena) | N | d | d1,e1 | Ena basin | mem | none |
Okute | N | d | d1,e2 | hills | mem | none |
Hosokute | N | d | d1,e2 | hills | mem | none |
Mitake | N | d | d1,e1 | valley | mem | none |
Fushimi (Mino) | N* | c | c1,d1 | Kiso River landing | mem | pond |
Ota | N | c | c1,d1 | Kiso River: Ota ferry | mem | pond |
Unuma | N | d | d1,c1 | Kiso River nearby | mem | pond |
Kano | N | f | f1,d1 | Kano castle (1601) | mem | pond | a small castle town missing from CASTLE_TOWNS
Godo | N | c | c1,d1 | Nagara River: Godo ferry | mem | pond |
Mieji | N | d | d1,e1 | plain | mem | none |
Akasaka (Nakasendo) | N* | c | c3,d1 | Kuise River boat landing | mem | pond |
Tarui | N* | d | d3,d1 | Tarui spring | mem | pond |
Sekigahara | N | d | d1,e1 | valley | mem | none |
Imasu | N | d | d1,e2 | valley | mem | none |
Kashiwabara | N | d | d1,e1 | valley | mem | none |
Samegai | N | d | d3,d1 | Isame spring and the Jizo-gawa: ~500 m along the street, ~14 C, baikamo weed | S-SMG | pond |
Banba | N | d | d1,e2 | hills | mem | none |
Toriimoto | N* | d | d1,e1 | plain | mem | none |
Takamiya | N | d | d1,c3 | Inukami River | mem | pond |
Echigawa | N | d | d1,c3 | Echi River | mem | pond |
Musa | N | d | d1,e1 | plain | mem | none |
Moriyama | N | d | d1,c2 | Yasu River crossing | mem | pond |
Takaido | KO | d | d1,e1 | the Tamagawa aqueduct's open channel (1653) beside the road | mem | pond |
Fuchu (Musashi) | KO | d | d1,c1 | Tama River to the south | mem | pond |
Hachioji | KO* | d | d1,c3 | Asa River | mem | pond |
Kobotoke | KO | e | e2,d1 | checkpoint in the hills | mem | none |
Sasago | KO | e | e2 | pass hamlet | mem | none |
Nirasaki | KO | c | c2,d1 | Kamanashi River braided bed; Shingen-zutsumi levees upstream (an old survivor) | mem | pond |
Hakone Yumoto | O | d | d4,c3 | hot-water gutters; Hayakawa and Sukumo rivers | mem | pond |
Atami | O | d | d4,g2 | the Oyu hot spring; the sea | mem | sea |
Shuzenji | O | d | d4,c3 | Katsura River with a riverbed bath | mem | pond |
Arima | O | d | d4,e2 | mountain stream | mem | none |
Kusatsu-onsen | O | d | d4,e2 | hot-water troughs in the town centre (yubatake; verify the form in 1730) | mem | none |
Ojigoku | O | none | - | not a settlement: a sulphur valley with hot streams | KL | none | NOT A SETTLEMENT: no waterway type; landmark terrain
Minobu | TT | e | e2,d1 | Haki River below Kuon-ji | mem | pond |
Kamiyoshida | TT | d | d5,d1,e2 | the Yana-gawa crossing each oshi plot, where pilgrims purified before entering (Fuji spring water from the Sengen shrine) | S-KYD | none |
Zenko-ji | TT | d | d1,e1 | temple town | mem | none |
Tanigumi-san | TT | e | e2 | mountain temple | mem | none |
Taga | TT | d | d1,e1 | shrine town | mem | none |
Sakamoto (Omi) | TT | d | d2,g3 | stone-lined lane channels coming off Mt Hiei between the dry-stone walls; the lake shore | mem | lake |
Shimizu | P | g | g1,c3 | Tomoe River mouth harbour | mem | sea |
Uraga | P | g | g1,d1 | inlet harbour; the Uraga magistracy from 1720 | mem | sea |
Sakai | P | a | a2,g1,d1 | the moat-canal ring round the town (Doi-kawa) and the harbour | mem | sea |
Hyogo | P | g | g1,d1 | Hyogo harbour | mem | sea |
Katata | P | g | g3,a2 | lake port; the Ukimido hall on stilts; inner water lanes | mem | lake |
Ominato (Ise) | P | g | g1,c3 | Ise's port at the Seta and Isuzu mouths | mem | sea |
Gyotoku salt | S | g | g2,e1,a2 | salt fields with sea-water ditches; the Gyotoku boat to Edo by the Shin-kawa and Onagi-gawa | mem | sea |
Yoshida-hama salt | S | g | g2,e1 | salt fields with sea-water ditches | mem | sea |
Yui-Kanbara salt beach | S | g | g2 | salt beach | mem | sea |
Matsudaira | V:rice | e | e1 | hill-valley paddies | VJ | pond |
Asuke | V:mountain | e | e2,d1 | Asuke River; Chuma road post village | VJ mem | pond |
Busetsu | V:mountain | e | e2 | upland streams | VJ | none |
Hiraya | V:mountain | e | e2 | pass village streams | VJ | none |
Komaba | V:mountain | e | e2,d1 | Achi post village | VJ | none |
Iijima | V:rice | e | e1,d1 | Ina valley terraces; intendant's office | VJ | pond |
Miyada | V:rice | e | e1,d1 | Tenryu terraces | VJ | pond |
Matsushima | V:rice | e | e1,d1 | north Ina valley | VJ | pond |
Mori | V:rice | e | e1,d1 | market village at the foot of the Akiba road | VJ | pond |
Inui | V:mountain | e | e2,d1 | Keta River gorge | VJ mem | pond |
Misakubo | V:mountain | e | e2 | mountain streams | VJ | none |
Wada (Toyama) | V:mountain | e | e2 | Toyama valley | VJ | none |
Kashio | V:mountain | e | e2 | mountain salt spring | VJ | none |
Ichinose | V:mountain | e | e2 | Hase valley | VJ | none |
Manzawa | V:mountain | c | c2,e2 | Fuji River road | VJ | pond |
Nanbu | V:rice | c | c2,e1 | Fuji River relay village | VJ | pond |
Kajikazawa | V:rice | c | c2,e1 | head port of the Fuji River boats (from 1607): a river boat landing | VJ | pond |
Kurokoma | V:mountain | e | e2 | Misaka road | VJ | none |
Subashiri | V:mountain | e | e2 | streams buried by the 1707 ash | VJ | none |
Mizonokuchi | V:rice | c | c1,d1 | Tama River: Futako ferry | VJ | pond |
Atsugi | V:rice | c | c1,d1 | Sagami River ferry | VJ | pond |
Oyama | V:mountain | e | e2,d2 | pilgrim-lodge village with stepped stream lanes | VJ mem | none |
Sekimoto | V:rice | e | e2,d1 | foot of Ashigara pass | VJ | none |
Fukara | V:rice | e | e1 | fields watered by the Hakone irrigation tunnel (1670) | VJ OL | pond |
Seya | V:rice | e | e1 | Sagami upland | VJ | none |
Sakashita | V:rice | e | e1 | below Utsu pass | VJ | none |
Tajimi | V:rice | c | c3,e1 | Toki River | VJ | pond |
Komaki | V:rice | e | e1,d1 | planned post village | VJ | none |
Tsuge | V:mountain | e | e2 | Iga border | VJ | none |
Kasagi | V:mountain | c | c3,e2 | Kizu River gorge | VJ | pond |
Kizu | V:rice | c | c1,e1 | Kizu River landing for Nara's timber | VJ | pond |
Hiraoka | V:rice | e | e1 | foot of Kuragari pass | VJ | none |
Hino | V:rice | d | d1,e1 | Omi merchants' home town | VJ | none |
Nagasawa | V:mountain | e | e2 | Yatsugatake skirts | VJ | none |
Umi-no-kuchi | V:mountain | e | e2 | upland | VJ | none |
Takanomachi | V:rice | c | c1,e1 | upper Chikuma River | VJ | pond |
Oyashiki | V:rice | e | e1 | Kai basin paddies | VJ | none |
Ashikura | V:mountain | e | e2 | below the Southern Alps | VJ | none |
Yamura | V:rice | c | c3,e1 | Katsura River | VJ | pond |
Doshi | V:mountain | e | e2 | long valley | VJ | none |
Umegashima | V:mountain | e | e2 | head of the Abe valley; hot spring | VJ | none |
Utogi | V:mountain | e | e2 | spring-fed wasabi terraces | VJ | none |
Ieyama | V:mountain | c | c2,e2 | Oi River timber rafts | VJ | pond |
Futamata | V:rice | c | c1,e1 | Tenryu River raft landing | VJ | pond |
Kiga | V:rice | g | g3,e1 | Lake Hamana's north inlet; checkpoint village | VJ | sea |
Nagashino | V:rice | c | c3,e1 | river confluence under the castle ruin | VJ mem | pond |
Taguchi | V:mountain | e | e2 | Shitara uplands | VJ | none |
Nagakute | V:rice | e | e1 | farming village | VJ | none |
Seki (Mino) | V:rice | e | e1,d1 | sword-smiths' village | VJ | none |
Warabi (Mino) | V:mountain | e | e2 | paper village: paper washed in the river | VJ mem | pond |
Takasu | V:rice | c | c1,e1 | ring-levee (waju) village in the Kiso delta | VJ | pond |
Tsushima | V:rice | c | c3,d1 | Tenno River port; lantern-boat festival | VJ | pond |
Shigaraki | V:mountain | e | e2 | kiln valley | VJ | none |
Kashiwara | V:rice | c | c1,e1 | the new Yamato River mouth (1704); Kashiwara cargo boats | VJ | pond |
Tokorozawa | V:rice | d | d1 | dry Musashino upland: deep wells, no stream | VJ mem | none | FITS NONE: no waterway at all; d1 gutters + wells only
Ome | V:mountain | c | c3,e2 | Tama River rafting | VJ | pond |
Ohara | V:mountain | e | e2 | hill village | VJ | none |
Chichibu | V:mountain | c | c1,e2 | Ara River | VJ mem | pond |
Nojima | V:fishing | g | g2 | Kanazawa bay; salt pans | VJ | sea |
Misaki | V:fishing | g | g1,g2 | anchorage for ships bound for Edo | VJ | sea |
Manazuru | V:fishing | g | g2 | fishing and stone-quarry village | VJ | sea |
Ito | V:fishing | g | g2 | Izu fishing village | VJ | sea |
Heda | V:fishing | g | g1,g2 | hook-shaped sheltered harbour | VJ | sea |
Omaezaki | V:fishing | g | g2 | cape beach; the Miobi beacon | VJ | sea |
Irago | V:fishing | g | g2 | Atsumi tip | VJ | sea |
Morozaki | V:fishing | g | g2 | Chita tip | VJ | sea |
Tokoname | V:fishing | g | g1,g2 | kiln harbour | VJ | sea |
Shiroko | V:fishing | g | g1,g2 | Ise bay port | VJ | sea |
Kitakomatsu | V:fishing | g | g3 | Lake Biwa fishing village | VJ | lake |
Sugaura | V:fishing | g | g3 | gated lakeside village | VJ | lake |
"""


def parse():
    out = []
    for ln in ROWS.strip().splitlines():
        p = [x.strip() for x in ln.split("|")]
        while len(p) < 8:
            p.append("")
        name, listed, prim, types, ww, src, water, flag = p[:8]
        out.append(dict(name=name, listed=listed, primary=prim,
                        types=[t for t in types.split(",") if t and t != "-"],
                        waterway=ww, sources=src.split(), water=water, flag=flag))
    return out
