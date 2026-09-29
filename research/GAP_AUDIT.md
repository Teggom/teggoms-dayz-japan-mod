# Gap audit: the Edo–Kyoto–Osaka corridor checked against a fixed grid (1730)

Research agent GAP, 2026-09-29. Text only. This is a coverage check, not a brainstorm. Every station, province,
side road and stretch of coast along the map's two roads (`FEASIBILITY.md` §3) gets one row, and each row is checked
against the existing lists. Anything missing is written up in §3, in the format of the list it belongs to.

**Lists checked (keys used below).**
- `BL`: `research/buildings/BUILDING_LIST.md` (682 types; §2 settlement layouts).
- `OL`: `research/outdoor/OUTDOOR_LIST.md`, the merged outdoor list, which appeared during this run and is used in
  place of the four flavour files. Groups are cited as in OL, e.g. `OL W §8`, `OL R §16`, `OL N §X`.
- `E01–E102`: `research/landmarks/E_EDO_TOKAIDO.md`.
- `W01–W115`: `research/landmarks/W_KANSAI_NAKASENDO.md`. **That file has no IDs; the W numbers here are this audit's,
  counted in heading order** (W01 Imperial Palace … W35 Osaka Castle … W59 Ōtsu port … W78 Suribari pass … W115
  Itabashi). The full key is at the end of this file.

**Era rule (binding).** "Did it exist, or still stand, in 1730?" Old survivors are IN. Later things are tagged
`[not yet in 1730: date]`, things already gone `[gone by 1730: date]`. `(verify)` = from memory or one weak source.

**Meibutsu honesty note.** Period guides (the *Tōkaidō meisho-ki* c.1660, the *Tōkaidō bunken ezu* 1690, Ekiken's
*Kisoji no ki* 1709) were not open this session. Specialties were checked against web sources where possible
(Shizuoka and Kanagawa prefectural pages, museum pages, shop histories) and otherwise marked `(verify)`. Several
famous meibutsu are attested only by *Hizakurige* (1802) or Hiroshige (1830s); those are marked "attested later",
because the thing may or may not have been famous by 1730. Where nothing turned up the cell says "none found".
Many "none found" rows are plain small stations, and they are marked NOTHING NOTABLE, not GAP.

**How status was set.**
- **COVERED:** the landmark (or the lack of one) is handled, every meibutsu has a trade in BL that can make or sell it,
  and the settlement type is in BL §2.
- **GAP:** at least one named thing is missing (a landmark, a trade, an outdoor item or a settlement type). The cell
  says what; §3 writes it up.
- **NOTHING NOTABLE:** an ordinary station or stretch; the generic post-town or village layout covers it.

---

## 1. Summary

**Rows checked: 204.**

| Block | Rows | COVERED | GAP | NOTHING NOTABLE |
|---|---|---|---|---|
| A. Tōkaidō (Nihonbashi, 53 stations, Sanjō, 4 Kyōkaidō stations, 14 rest stops) | 73 | 49 | 12 | 12 |
| B. Nakasendō (67 own stations + 3 rest stops; Kusatsu and Ōtsu are shared with A) | 70 | 41 | 6 | 23 |
| C. Provinces (land off the roads; 17 asked + 7 added) | 24 | 5 | 17 | 2 |
| D. Land between the roads | 6 | 0 | 6 | 0 |
| E. Linking and side roads | 12 | 7 | 5 | 0 |
| F. Coast off the road | 19 | 9 | 10 | 0 |
| **Total** | **204** | **111** | **56** | **37** |

Gap entries written up in §3: 2 settlement layouts, 8 trades and 4 item additions (BL); 7 outdoor items (OL); and
35 landmarks (19 for E and the Kōshū side, 16 for W).

**Headline.** The two roads themselves are well covered: E and W between them name almost every station that
matters, and BL has a trade for nearly every meibutsu. The holes are **off the roads**. The Kai basin, the north side
of Fuji, the Ina valley, the Mino interior, Kawachi and the Settsu coast between Osaka and Kōbe have almost nothing
in any list. BL §2 also lacks two settlement layouts the corridor needs everywhere: the **market town** and the
**salt village**.

**The 10 most important gaps (map impact first).**
1. **The Kai / Kōfu basin is blank (D1, C16).** Kōfu is a shogunal castle town in 1730 (the Kōfu kinban garrison,
   from 1724). Minobu-san Kubo-ji is the Nichiren head temple and a mountain temple town. Erin-ji, the Takeda palace
   ruin, the Kōshū grape trellises and the Kai silk villages have no entries. Where the first-draft map puts the
   "central range", the real ground is this basin.
2. **The north side of Fuji (D4).** Kamiyoshida's oshi pilgrim-lodge town and the Kitaguchi Hongū Fuji Sengen shrine
   were the main start of the 1730 Fuji climb. The Hitoana cave, the holy site of the Fuji-kō cult, is also missing.
   E56 covers only the mountain and the south side.
3. **The Kōshū Kaidō (S1) and an era trap.** **Naitō-Shinjuku did not exist in 1730**: it was opened in 1699, shut in
   1718 and not reopened until 1772. The road's first station was Takaido. The Kobotoke checkpoint, Hachiōji (silk
   market and the sennin-dōshin) and the Sasago pass are also missing. Saruhashi is the only piece listed.
4. **No market-town layout in BL §2.** Hachiōji, Yokkaichi, Honjō, Urawa, Nakatsugawa and Kōfu's merchant quarter
   were market towns (zaigō-machi), not post towns or castle towns.
5. **No salt-village layout in BL §2.** BL has the salt fields and the huts, and OL R §16 has the outdoor kit, but
   there is no settlement plan. Gyōtoku (Edo's salt), Kira / Yoshida-hama (Mikawa), Futami (Ise's sacred salt) and
   the Yui–Kanbara beach all need one.
6. **The Mino interior pilgrim sites (D5, C13).** **Tanigumi-san Kegon-ji**, the last temple of the Saigoku 33
   pilgrimage, and **Yōrō falls**, a famous legend waterfall, are missing. Both are within a day of Tarui.
7. **Suwa's upper shrine and the Ina valley (D2, D3).** W98 covers only the lower shrine. Missing:
   - Kamisha Honmiya and Maemiya
   - Takatō, where **Ejima of the 1714 Ejima–Ikushima scandal was confined, alive in 1730**
   - Iida castle town
   - the paved **Gonbei pass** linking Kiso and Ina (1696)
8. **Kawachi and the Settsu coast (C12, C11, F18).** Missing:
   - The **Yamato river was rerouted in 1704**. Its dry old beds became the Kōnoike shinden (1707) and other
     cotton fields, a huge 26-year-old reclamation.
   - Nishinomiya Ebisu shrine, with its Ebisu-kaki puppeteers
   - the Minatogawa grave of Kusunoki Masashige, with Mitsukuni's 1692 stele
   - Arima hot spring (named only as an example in BL §2.14)
9. **Mid-Tōkaidō castles and temples no list names (A, C5, C6).** Missing:
   - Tanaka castle, a round concentric castle 1 km off the road at Fujieda
   - Yokosuka castle
   - Fukuroi's "Enshū three temples"
   - Hōrai-ji and the Nagashino battlefield
   - Tsushima shrine on the Sayaji
   - the Shirotori timber yard at Atsuta
   - Iga Ueno castle
10. **Small trades and outdoor items the meibutsu imply.**
    - BL trades: oiled-paper rain capes (kappa, Toriimoto), kudzu cloth (Kakegawa), calendars (Mishima-goyomi),
      Ōtsu-e souvenir paintings, a Hatchō-scale miso brewery
    - OL items: Lake Biwa's fixed **eri** fish traps, Kai's grape trellis, the obsidian of the Wada pass (in W99 but
      not in OL), and the Kinshōzan limestone quarries at Akasaka (Mino)

**Surprises.**
- **An elephant lives in Edo in 1730.** It walked the Tōkaidō in spring 1729: Nagasaki, Osaka, Kyoto (where Emperor
  Nakamikado received it and gave it court rank), Hirakata, Nagoya and Hakone, then Edo on 1729-05-25. It was kept
  at Hama-goten until 1742. No list mentions it; OL already has Hama-goten as a garden landmark.
- The **agemai** system (1722–1730) halved daimyo stays in Edo in exchange for rice. **It ended in 1730**, so the year
  sits exactly on the swing back to full sankin-kōtai traffic. It is a policy, but it is visible as the number of
  processions on the road.
- Kanpyō is tied to the wrong place in N, R and OL (see §5).
- Several "old" meibutsu are later than they sound. Correctly tagged in the lists already:
  - Takasaki daruma, c.1780s (W109)
  - Makinohara tea, 1869 (E70)
  - Amagi wasabi, 1744 (OL)

  Not in any list, and also later:
  - **Banko ware** (Yokkaichi/Kuwana): `[not yet in 1730: c.1736–41]`
  - **Kiryū's drawloom silk**: `[not yet in 1730: 1738]`
  - **Okegawa safflower**: `[not yet in 1730: c.1790s (verify)]`
  - **Suwa kanten**: `[not yet in 1730: 1840s]`
  - **Hakone yosegi marquetry**: `[not yet in 1730: c.1800s]`
  - **Jikigyō Miroku's fast to death on Fuji**: `[not yet in 1730: 1733]`
  - **Ogata Kenzan's move from Kyoto to Edo**: `[not yet in 1730: 1731]`
  - **Muneharu's licensed theatres and quarters in Nagoya**: `[not yet in 1730: 1731–32 (verify)]`

---

## 2. The grid

Abbreviations: PT = post town (BL §2.5); ai = ai-no-shuku / tateba (BL §2.6); CT = castle town (BL §2.7); ✓ = the
trade is in BL (entry named); ✗ = no trade in BL.

### A. Tōkaidō (east to west)

| Row | Landmark | Meibutsu → trade covered? | Settlement type | Other (1730 trace, industry, nature) | Status |
|---|---|---|---|---|---|
| A00 Edo / Nihonbashi | E01–E24 | Too many to list; fish market E03, Echigoya E04 | Great city §2.9 ✓ | **The elephant (1729–42) at Hama-goten** is in no list; Hama-goten itself is in OL (U Gardens). Agemai ends 1730. | GAP |
| A01 Shinagawa | E25–E27 | Shinagawa / Asakusa nori → Nori farm ✓, Nori farmer's cottage ✓ | PT + fishing shore (§2.4) ✓ | Meshimori town; Gotenyama cherries (E26) | COVERED |
| A-a Ōmori / Kamata (tateba) | none needed | Wachūsan stomach powder (rival shops, Genroku claims (verify)) → Medicine shop ✓; Ōmori nori ✓; straw-work boxes (mugiwara-zaiku) (verify date) → Straw-goods maker ✓ | ai ✓ | Plum garden at Kamata (fame later, verify) | COVERED |
| A02 Kawasaki | E28, E29 | Nara-chameshi at Mannen-ya → Tea-rice shop ✓ (fame usually dated from the 1760s (verify)) | PT ✓ | Tanaka Kyūgu, Kawasaki honjin owner and river engineer, d.1729 | COVERED |
| A-b Tsurumi / Namamugi (tateba) | none needed | Yone-manjū, famous from the early 1700s → Steamed-bun shop ✓; Namamugi fresh fish → Fishmonger ✓ | ai ✓ | Namamugi incident `[not yet in 1730: 1862]` | COVERED |
| A03 Kanagawa | none | None found; bluff tea houses over the bay → Roadside tea house ✓ | PT + small bay port (§2.11) ✓ | Yokohama `[not yet in 1730: 1859]` | NOTHING NOTABLE |
| A04 Hodogaya | none | Botamochi at the Sakaigi tateba on the Musashi–Sagami border → Rice-cake shop ✓ | PT ✓ | Border Jizō at Sakaigi | COVERED |
| A05 Totsuka | E32 (Kamakura fork) | None found | PT ✓ | First night out of Edo; Kamakura road fork | NOTHING NOTABLE |
| A06 Fujisawa | E30, E31, E33 | None (the 1843 register names the Ōyama and Enoshima pilgrimages as its "meibutsu") | PT + temple town (Yugyō-ji) ✓ | Fork stones → OL Fork direction stone ✓ | COVERED |
| A07 Hiratsuka | none | None found | PT ✓ | Banyū (Sagami river) ferry → OL ferry landing ✓ (unnamed) | NOTHING NOTABLE |
| A08 Ōiso | E34 | None found (Tora-ga-ishi, the Soga-tale stone, is a relic, not a product (verify)) | PT ✓ | 1703 Genroku quake damage | NOTHING NOTABLE |
| A-c Umezawa (tateba) | none | None found; a big daimyo rest tea house | ai ✓ | — | NOTHING NOTABLE |
| A09 Odawara | E35–E37 | Uirō (E37) → Medicine shop ✓; kamaboko → Kamaboko maker ✓; umeboshi → Umeboshi works ✓; folding Odawara lantern → Lantern maker ✓ | CT + PT ✓ | Castle rebuilt after the 1703 quake; Sakawa floods after the 1707 ash; Kyūgu's 1726 levee (see C2) | COVERED |
| A-d Hatajuku (ai, Hakone) | E39 (Amazake-chaya) | Hakone woodturning → Hakone woodcraft maker ✓; yosegi marquetry `[not yet in 1730: c.1800s]` | ai ✓ | — | COVERED |
| A10 Hakone | E38–E46 | See Hatajuku | PT + checkpoint + onsen §2.14 ✓ | — | COVERED |
| A-e Yamanaka (ai, west slope) | E47 | None found | ai ✓ | — | COVERED |
| A11 Mishima | E48, E49 | **Mishima-goyomi**, the calendar printed by the Kawai family at Mishima Taisha since medieval times → ✗ (no calendar maker; the woodblock printer is closest) | PT + shrine-gate town ✓ | Eel fame is often claimed but undated (verify) | GAP |
| A12 Numazu | E53 | None found | PT ✓ (castle status per E53) | Kano river boat landing | NOTHING NOTABLE |
| A13 Hara | E54, E55 | None found | PT ✓ | Hakuin at Shōin-ji from 1716 | COVERED |
| A14 Yoshiwara | E55, E57 | None found | PT ✓ (moved inland 1680) | Tsunami relocation (E55) | COVERED |
| A-f Iwabuchi (ai) | E59 | Chestnut mochi (kuri-no-ko-mochi) (verify) → Rice-cake shop ✓ | ai ✓ | **Fuji river boat landing**: Kai rice came down and salt went up by Suminokura's rapid-boat route (1607). Not in any list. | GAP |
| A15 Kanbara | none | None found | PT ✓ (rebuilt inland after the 1699 flood (verify)) | Beach salt making (verify) | NOTHING NOTABLE |
| A16 Yui | E60 | Satō-mochi / tamago-mochi (attested later: *Hizakurige*, 1802) → Rice-cake shop ✓ | PT ✓ | Sea salt (see F9) | COVERED |
| A-g Kurasawa (tateba) | E60 | Turban shells (sazae) and abalone grilled in the shell → Roadside tea house ✓ + Fishmonger ✓ | ai + fishing village ✓ | Satta-view tea houses | COVERED |
| A17 Okitsu | E61 | None firm ("okitsu-dai", the tilefish named after the town (verify)) | PT ✓ | — | COVERED |
| A18 Ejiri | E62, E63 | None found | PT + port (Shimizu) §2.11 ✓ | — | COVERED |
| A19 Fuchū (Sunpu) | E64–E66 | Abekawa-mochi (E66) → Rice-cake shop ✓; Suruga lacquer and woodwork (verify) → Lacquerer ✓; Abe tea → Tea-leaf dealer ✓ | CT ✓ | Abe gold (Umegashima), past peak | COVERED |
| A20 Mariko | E67 | Tororo-jiru (E67; Chōjiya from 1596) → cook-shop ✓ | PT ✓ | — | COVERED |
| A21 Okabe | E68 | Tōdango (E68) → Rice-cake shop ✓ | PT ✓ | — | COVERED |
| A22 Fujieda | none | Seto no **somemeshi** (gardenia-yellow rice cakes, at the Seto tateba, "from the Sengoku period") → Rice-cake shop ✓ | PT ✓ | **Tanaka castle**: concentric round castle, Tanaka domain seat, ~1 km off the road. In no list. | GAP |
| A23 Shimada | E69 | None found | PT + river-crossing town §2.13 ✓ | — | COVERED |
| A24 Kanaya | E69, E70 | None found | PT + river-crossing ✓ | Makinohara tea `[not yet in 1730: 1869]` (E70 ✓) | COVERED |
| A-h Kikugawa (ai) | E71 (near) | Nameshi (greens rice) with dengaku, "already a meibutsu by mid-Edo" (verify for 1730) → Dengaku shop ✓ | ai ✓ | — | COVERED |
| A25 Nissaka | E71 | Kosodate-ame (child-rearing candy) at Sayo-no-Nakayama → Candy maker ✓; warabi-mochi (verify) → Rice-cake shop ✓ | PT ✓ | Night-Weeping Stone | COVERED |
| A26 Kakegawa | E72, E73 | **Kuzu-fu** (kudzu-fibre cloth for hakama and rain gear) → ✗ (Wild-fibre weaver covers fuji-fu and shina-fu only) | CT ✓ | **Yokosuka castle** (south-east, round-stone walls) is in no list | GAP |
| A27 Fukuroi | none | Tamago-fuwafuwa (egg soufflé; attested later: 1813 diary) → Cheap cook-shop ✓ | PT ✓ (the midpoint, 27th of 53) | **Enshū three temples** (Kasuisai, Hattasan Sonei-ji, Yusan-ji) are in no list | GAP |
| A28 Mitsuke | E74 | None found | PT ✓ | Tōtōmi Kokubun-ji site; Mitsuke Tenjin festival (verify) | NOTHING NOTABLE |
| A-i Ikeda (Tenryū ferry village) | E74 | None found | ferry village ✓ | Tenryū timber rafts → Timber rafting station ✓ | COVERED |
| A29 Hamamatsu | E75 | None found | CT ✓ | — | COVERED |
| A30 Maisaka | E76 | None found | PT + fishing ✓ | — | COVERED |
| A31 Arai | E77 | Eel kabayaki (attested later: Hiroshige, "Arai meibutsu kabayaki") → Eel shop ✓ | PT + lake sekisho ✓ | Checkpoint moved 1701 and 1708 (E77) | COVERED |
| A32 Shirasuka | E79 | None found | PT ✓ (moved uphill after 1707) | — | COVERED |
| A-j Sarugababa (tateba) | none | Kashiwa-mochi (oak-leaf rice cakes) (verify for 1730) → Rice-cake shop ✓ | ai ✓ | — | COVERED |
| A33 Futagawa | none | None found (see Sarugababa) | PT ✓ | — | NOTHING NOTABLE |
| A34 Yoshida | E80 | None found | CT + river port ✓ | Toyokawa Inari named only in passing (see C6) | COVERED |
| A35 Goyu | E81 | None found | PT ✓ | — | COVERED |
| A36 Akasaka | E81 | None found | PT (meshimori) ✓ | — | COVERED |
| A37 Fujikawa | none | None firm (the "murasaki" gromwell tie is poetic or modern (verify)) | PT ✓ | — | NOTHING NOTABLE |
| A38 Okazaki | E82–E84 | **Hatchō miso** (two families in Hatchō village; giant cedar vats weighted with stone cones) → Miso maker is a town shop, ✗ at brewery scale; Okazaki stone lanterns → Stonemason ✓; Mikawa cotton → Cotton-cloth wholesaler ✓ | CT ✓ | — | GAP |
| A39 Chiryū | E85 | Horse fair (E85) → Commercial stable and horse dealer ✓ | PT ✓ | — | COVERED |
| A-k Arimatsu (ai) | E86, E87 | Arimatsu shibori → Tie-dyer ✓ | ai / craft street ✓ | — | COVERED |
| A40 Narumi | E86 | Narumi shibori → Tie-dyer ✓ | PT ✓ | — | COVERED |
| A41 Miya | E88–E90 | None firm | PT + port §2.11 ✓ | **Shirotori timber yard**, Owari's landing pond for Kiso timber, is in no list; Muneharu becomes lord 1730 | GAP |
| A42 Kuwana | E91 | Yaki-hamaguri and shigure-hamaguri (clams simmered in soy) → Souvenir shop ✓ (clams named), Food stall ✓; Kuwana cast iron → Caster of pots and kettles ✓ | CT + port ✓ | Keep burned 1701 (E91) | COVERED |
| A-l Tomida (tateba) | none | Grilled clams were largely sold here (verify) → Food stall ✓ | ai ✓ | — | COVERED |
| A43 Yokkaichi | E92 | Hinaga **nagamochi** (Sasaya, founded 1550) → Rice-cake shop ✓; Banko ware `[not yet in 1730: c.1736–41]` | PT + **market town** (the 4th-day market) → ✗ no layout | — | GAP |
| A44 Ishiyakushi | none | None found | PT ✓ | Ishiyakushi-ji (small temple of the stone Yakushi) | NOTHING NOTABLE |
| A45 Shōno | none | **Yakigome** (roasted rice in fist-sized straw bales) → ✗ (no trade lists it; an item for Rice polisher or Dried-goods shop) | PT ✓ | — | GAP |
| A46 Kameyama | E93 | None found | CT ✓ | — | COVERED |
| A47 Seki | E94 | Seki-no-to (bean-paste rice cake, Fukaya, from the 1630s (verify)) → Fine confectioner ✓ | PT ✓ | East and west forks: the Ise betsukaidō and the Yamato / Iga road (see D6, S3) | COVERED |
| A48 Sakashita | E95 | None found | PT ✓ | Suzuka packhorse song | COVERED |
| A49 Tsuchiyama | E96 | None firm (hill tea (verify)) | PT ✓ | — | COVERED |
| A50 Minakuchi | E97 | Kanpyō (E97) → Drying shed ✓, OL gourd-strip drying ✓ (but see §5); tsuzura baskets (verify) → Bamboo worker ✓; loach soup (verify) | CT (small) ✓ | — | COVERED |
| A51 Ishibe | none | None found (see Megawa) | PT ✓ | "Leave Kyoto, sleep at Ishibe" | NOTHING NOTABLE |
| A-m Megawa (tateba) | none | Nameshi-dengaku (claimed origin) → Dengaku shop ✓ | ai ✓ | — | COVERED |
| A52 Kusatsu (= Nakasendō 68) | E98, W70 | Ubagamochi → Rice-cake shop ✓ | PT junction ✓ | — | COVERED |
| A53 Ōtsu (= Nakasendō 69) | E99, E100, W59–W69 | **Ōtsu-e** folk paintings sold at Ōtani / Oiwake → ✗ as a roadside shop (Painter's studio is a town studio); Ōtsu abacus (from 1612) → Abacus maker ✓ | PT + lake port ✓ | Cart stones `[not yet in 1730: 1805 (verify)]` (OL ✓) | GAP |
| A-n Ōtani / Oiwake / Yamashina | W60 | See Ōtsu | ai ✓ | — | COVERED |
| A54 Kyoto, Sanjō Ōhashi | W16, W01–W33 | Kyoto crafts are throughout BL | Great city ✓ | Kenzan leaves for Edo `[not yet in 1730: 1731]` | COVERED |
| A55 Fushimi (Kyōkaidō) | W18, W19 | Fushimi sake → Sake brewery ✓; Fushimi clay dolls → Clay-doll maker ✓ | River port (fits §2.11) ✓ | Fushimi castle `[gone by 1730: 1623]` | COVERED |
| A56 Yodo | W32 | None found | CT ✓ | Waterwheels (W32) | COVERED |
| A57 Hirakata | W34 | Kurawanka food boats (W34) → Food stall ✓ | PT + river port ✓ | The elephant passed in 1729 | COVERED |
| A58 Moriguchi | none | **Moriguchi-zuke** (daikon pickled in sake lees) → Pickle maker ✓ | PT ✓ | **Station and the Bunroku levee road** (Hideyoshi's 1596 Yodo levee, whose top carries the Kyōkaidō) are in no list | GAP |

### B. Nakasendō (Edo end first)

| Row | Landmark | Meibutsu → trade covered? | Settlement type | Other | Status |
|---|---|---|---|---|---|
| B01 Itabashi | W115 | None found | PT ✓ | Kaga shimo-yashiki | COVERED |
| B02 Warabi | W114 | None firm (Futako-ori twill is 19th c. (verify)) | PT ✓ | — | COVERED |
| B03 Urawa | none | Twice-monthly market (2nd / 7th days) with a market-god stone (verify) → Market stalls ✓ | PT ✓ | — | NOTHING NOTABLE |
| B04 Ōmiya | W113 | None found | PT ✓ | — | COVERED |
| B05 Ageo | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B06 Okegawa | none | Safflower `[not yet in 1730: c.1790s (verify)]` | PT ✓ | — | NOTHING NOTABLE |
| B07 Kōnosu | none | Kōnosu hina dolls (early-Edo origin claimed (verify)) → Doll maker ✓ | PT ✓ | — | COVERED |
| B-a Fukiage (ai) | W112 | None found | ai ✓ | Road fork to Oshi castle (Gyōda), off the road | NOTHING NOTABLE |
| B08 Kumagaya | W112 | None found | PT ✓ | — | COVERED |
| B09 Fukaya | none | None found | PT ✓ (many meshimori) | — | NOTHING NOTABLE |
| B10 Honjō | W111 | Silk and cloth market → Silk thread dealer ✓ | PT ✓ | — | COVERED |
| B11 Shinmachi | none | None found | PT ✓ | Kanna river crossing | NOTHING NOTABLE |
| B12 Kuragano | W110 | None found | PT + river port ✓ | — | COVERED |
| B13 Takasaki | W109 | Daruma `[not yet in 1730: c.1780s]` (W109 ✓) | CT ✓ | — | COVERED |
| B14 Itahana | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B15 Annaka | none | None found | CT (small) + PT ✓ | **Isobe hot spring** (an old mineral spring; a 1661 map is claimed to carry the first onsen mark (verify)) is in no list | GAP |
| B-b Haraichi (ai) | none | None found | ai ✓ | Cedar avenue, Annaka–Matsuida (verify planting) → OL road avenue ✓ | COVERED |
| B16 Matsuida | W108 | None found | PT ✓ | — | COVERED |
| B17 Sakamoto | W106, W107 | Chikara-mochi on the pass (the shops claim ~350 years) → Rice-cake shop ✓ | PT ✓ | — | COVERED |
| B18 Karuizawa | W103 | None found | PT ✓ | — | COVERED |
| B19 Kutsukake | W103 | None found | PT ✓ | — | COVERED |
| B20 Oiwake | W101, W102 | Oiwake-bushi, the packhorse song (intangible) | PT ✓ | Asama ash falls 1729–33 (W102) | COVERED |
| B21 Otai | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B22 Iwamurada | none | None found | PT + jinya town (Naitō, from 1703) §2.8 ✓ | Saku–Kōshū road junction | COVERED |
| B23 Shionada | W100 | None found | PT + river crossing ✓ | — | COVERED |
| B24 Yawata | W100 | None found | PT ✓ | — | COVERED |
| B25 Mochizuki | W100 | None found | PT ✓ | Old pasture → OL commons pasture ✓ | COVERED |
| B26 Ashida | none | None found | PT ✓ | Kasatori pass pine avenue → OL road avenue ✓ (unnamed) | NOTHING NOTABLE |
| B27 Nagakubo | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B28 Wada | W99 | None found | PT ✓ | **Obsidian** on the pass: named in W99, but no OL item | GAP |
| B29 Shimosuwa | W98 | Kanten `[not yet in 1730: 1840s]`; frozen tofu (date unclear (verify)) | PT + onsen + end of the Kōshū road ✓ | Onbashira renewed 1728 | COVERED |
| B30 Shiojiri | W97 | None found | PT + junction ✓ | Ina (Sanshū) road and Matsumoto road fork here; the name is read as "end of the salt road" | COVERED |
| B31 Seba | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B32 Motoyama | none | **Soba-kiri** said to originate here (Morikawa Kyoriku, 1706) → Soba shop ✓ | PT ✓ | — | COVERED |
| B-c Hirasawa (lacquer village) | W95 (Kiso lacquer) | Kiso lacquer → Lacquerer ✓ | craft village (fits PT street form) ✓ | — | COVERED |
| B33 Niekawa | W96 | None found | PT + timber checkpoint (W96, verify) ✓ | — | COVERED |
| B34 Narai | W94, W95 | Kiso lacquer, combs, bentwood → Lacquerer ✓, Comb maker ✓, Bentwood maker ✓ | PT ✓ | — | COVERED |
| B35 Yabuhara | W94 | Oroku combs → Comb maker ✓ | PT ✓ | — | COVERED |
| B36 Miyanokoshi | (W94 names Yoshinaka's battle only) | None found | PT ✓ | **Kiso Yoshinaka's home ground**: Tokuon-ji (family temple and grave) and Hatage Hachimangū. No entry. | GAP |
| B37 Fukushima | W92, W93 | Kiso horse market → Horse dealer ✓, Horse-dealers' inn ✓ | PT + sekisho + daikan seat ✓ | — | COVERED |
| B38 Agematsu | W91 | None found | PT + timber office (BL §2.3) ✓ | — | COVERED |
| B39 Suhara | W90 | Hanazuke (salt-pickled cherry blossoms) (verify for 1730) → Pickle maker ✓ | PT ✓ | — | COVERED |
| B40 Nojiri | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B41 Midono | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B42 Tsumago | W89 | None found | PT ✓ | — | COVERED |
| B43 Magome | W88 | None found | PT ✓ | — | COVERED |
| B44 Ochiai | W87 | None found | PT ✓ | — | COVERED |
| B45 Nakatsugawa | none | None firm (chestnut sweets are modern) | PT + **market town** for east Mino → ✗ no layout | **Naegi castle** (small crag castle over the Kiso, Tōyama clan) is in no list | GAP |
| B46 Ōi | none | None found | PT ✓ | "Thirteen passes" (Jūsan-tōge) to Ōkute → terrain | NOTHING NOTABLE |
| B47 Ōkute | none | None found | PT ✓ | Thirteen passes | NOTHING NOTABLE |
| B48 Hosokute | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B49 Mitake | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B50 Fushimi (Mino) | none | None found | PT ✓ | Kiso river boat landing (verify) | NOTHING NOTABLE |
| B51 Ōta | W86 | Hachiya-gaki (dried persimmons of Hachiya, sent to the shogun) → Drying shed ✓, OL hoshigaki ✓ | PT + ferry ✓ | — | COVERED |
| B52 Unuma | W85 | None found | PT ✓ | — | COVERED |
| B53 Kanō | W84 | Kanō umbrellas (makers brought in 1639 (verify)) → Umbrella maker ✓; Gifu lanterns (verify date) → Lantern maker ✓ | CT + PT ✓ | Nagara cormorant fishing → Cormorant-fishing house ✓ | COVERED |
| B54 Kōdo | none | None found | PT ✓ | Nagara ferry | NOTHING NOTABLE |
| B55 Mieji | none | None found | PT ✓ | — | NOTHING NOTABLE |
| B56 Akasaka (Mino) | none | Lime from the Kinshōzan limestone hill, shipped from Akasaka's river port (verify start) → Lime burner ✓ (names only Hachiōji / Ōme) | PT + river port ✓ | **Kinshōzan limestone hill and quarries** in no list; Ieyasu's 1600 camp hill | GAP |
| B57 Tarui | W83 | None found | PT + junction ✓ | Nangū Taisha (W83) | COVERED |
| B58 Sekigahara | W82 | None found | PT ✓ | — | COVERED |
| B59 Imasu | W82 | None found | PT ✓ | Fuwa barrier ruin | COVERED |
| B60 Kashiwabara | W81 | Ibuki moxa → Moxa shop ✓ | PT ✓ | — | COVERED |
| B61 Samegai | W80 | None found | PT ✓ | — | COVERED |
| B62 Banba | W78 | None found | PT ✓ | — | COVERED |
| B63 Toriimoto | W79 | Akadama pill → Medicine shop ✓; **kappa** (oiled-paper rain capes) → ✗ | PT ✓ | Watermelon, the third "red" meibutsu (date unclear (verify)) | GAP |
| B64 Takamiya | W74 | Takamiya-nuno (fine Ōmi ramie cloth) → Hemp and ramie processor ✓, Cloth bleacher ✓ | PT ✓ | Taga pilgrims | COVERED |
| B65 Echigawa | none | None found | PT ✓ | Gokashō merchant villages (W71 ✓) | NOTHING NOTABLE |
| B66 Musa | none | None found | PT ✓ | Hachiman road fork | NOTHING NOTABLE |
| B67 Moriyama | none | None found | PT ✓ (first night out of Kyoto) | — | NOTHING NOTABLE |

(B68 Kusatsu = A52 and B69 Ōtsu = A53; they are not counted twice.)

### C. Provinces: the land off the two roads

| Row | Landmark | Meibutsu → trade covered? | Settlement type | Other | Status |
|---|---|---|---|---|---|
| C1 Musashi | E01–E29, W110–W115 | Nerima daikon and komatsuna (named 1719) → Greengrocer ✓; Ōme-jima cloth, Chichibu silk, Hachiōji silk → Town or village weaver ✓ | New-field village §2.2 ✓ (Musashino shinden, the 1720s–30s boom); **market town ✗** (Hachiōji, Ōme) | Tamagawa aqueduct ✓ BL. **Naitō-Shinjuku `[gone by 1730: 1718; reopened 1772]`**. Missing: Kawagoe CT, Takao-san, Chichibu 34 Kannon (off corridor). | GAP |
| C2 Sagami | E25–E47 | Ōyama spinning tops (verify) → Toy maker ✓; Odawara items (A09) | PT, CT ✓ | **Sakawa levee (Bunmei-zutsumi) rebuilt 1726 by Tanaka Kyūgu** after the Hōei-ash floods, and the ash-buried Ashigara fields: in no list (OL has an eruption ash trench only) | GAP |
| C3 Izu | E50–E52 | Katsuobushi → Dried-bonito works ✓; tengusa (OL ✓); Shuzen-ji gampi paper → Paper mill ✓; Amagi wasabi `[not yet in 1730: 1744]` (OL ✓); Izu stone → OL castle-stone quarry ✓ | Fishing, onsen ✓ | **Shimoda's ship-inspection post `[gone by 1730: moved to Uraga 1720]`**; Toi / Yugashima gold (past peak) → OL mine items ✓. Shimoda has no entry. | GAP |
| C4 Suruga | E53–E68 | Abe tea (Ashikubo) → Tea processing shed ✓; Utogi wasabi (OL ✓) | CT, PT ✓ | **Fuji river boat route** (Kajikazawa–Iwabuchi, 1607) is in no list | GAP |
| C5 Tōtōmi | E69–E78 | Kakegawa kuzu-fu ✗ (A26); Enshū cotton (verify) ✓ | CT ✓ | Missing: Yokosuka castle; Ryōtan-ji (Ii family temple and garden); Hōkō-ji at Okuyama; Enshū three temples (A27); the Kaketsuka timber port at the Tenryū mouth | GAP |
| C6 Mikawa | E79–E85 | Hatchō miso ✗ at scale (A38); Okazaki stone ✓; cotton ✓; **Kira / Yoshida-hama salt** → Salt field ✓; Mikawa manzai New Year performers (people, not buildings) | CT ✓; **salt village ✗** | Missing: Hōrai-ji and its Tōshōgū (1651); Nagashino battlefield (1575); Toyokawa Inari (only named in E80); Kegon-ji at Kira (home temple of Kira Yoshinaka of the 47-rōnin story; a good lord at home) | GAP |
| C7 Owari | E86–E90 | Seto ware (in a slump; porcelain `[not yet in 1730: 1807]`) → Climbing-kiln potter ✓; Tokoname ✓; Chita sake and cotton ✓ | Wajū villages ✓ (BL, OL) | Missing: **Tsushima shrine** (head of the Tsushima–Tennō cult, lantern-boat festival); Shirotori timber yard (A41). Kiyosu castle `[gone by 1730: 1610]`. Muneharu, lord from 1730. | GAP |
| C8 Ise | E91–E95, E101, E102 | Ise katagami (Shiroko) → Stencil cutter ✓; Matsusaka cotton → Cotton-cloth wholesaler ✓ | Temple town (Uji-Yamada) ✓ | Missing: **Tsu** CT (Tōdō seat), **Matsusaka** (the Mitsui home town), Kanbe CT, Yunoyama hot spring | GAP |
| C9 Ōmi | E96–E100, W59–W81 | Funa-zushi (fermented crucian carp) → Sushi seller (nare-zushi named) ✓; Shigaraki ware ✓; Hino medicine and Hino lacquer bowls (verify) → Medicine shop ✓, Lacquerer ✓; Nagahama guns (W76) ✓ | Lake port ✓ | Missing: Lake Biwa **eri** fixed fish traps (OL ✗); lake cargo boats (maruko-bune) as a boat prop | GAP |
| C10 Yamashiro | W01–W34 | Uji tea ✓; Kyoto crafts ✓; Kitayama polished cedar logs (verify) → Lumber dealer ✓; Ōhara firewood women (people) | Great city ✓ | Missing: **Manpuku-ji** (Ōbaku Zen head temple, Uji, 1661, Ming Chinese style). BL mentions it only as a sect note. | GAP |
| C11 Settsu | W35–W50 | Itami and Ikeda sake → Sake brewery ✓; Ikeda charcoal (from Nose) → Charcoal dealer ✓; Arima baskets → Bamboo worker ✓ | Great city, port ✓; brewing towns (Itami) have no layout | Missing: **Arima hot spring** (BL §2.14 example only), **Nishinomiya Ebisu shrine**, **Minatogawa** (Kusunoki grave, 1692 stele), Amagasaki CT, Katsuō-ji | GAP |
| C12 Kawachi | none | Kawachi cotton → Cotton-growing farmhouse ✓; Dōmyōji dried rice (verify) → Flour shop ✓ | New-field village ✓; jinai-machi (Tondabayashi) ✓ | Missing: **the new Yamato river (1704)** and the old-riverbed cotton reclamation, **Kōnoike shinden (1707)** with its kaisho office; Hiraoka shrine (Kawachi ichinomiya) | GAP |
| C13 Mino | W82–W87 | Mino paper → Paper mill ✓; Seki blades → Swordsmith ✓, Knife smith ✓; Mino ware ✓; Hachiya-gaki ✓ | Wajū ✓ | Missing: **Tanigumi-san Kegon-ji** (Saigoku 33rd); **Yōrō falls**; Gujō-Hachiman CT (off corridor) | GAP |
| C14 Shinano | W88–W105 | Ueda pongee (verify) → Town or village weaver ✓; Kiso lacquer, combs, soba, Kiso horses ✓ | PT, CT ✓ | Togakushi (off corridor); salt road → OL pack-ox path ✓. The Ina and Suwa gaps sit under D2 and D3. | COVERED |
| C15 Kōzuke | W106–W110 | Kiryū silk: plain weaves only, drawloom `[not yet in 1730: 1738]` → Town or village weaver ✓ | PT, CT ✓; onsen (Kusatsu named in BL §2.14) | Missing: Isobe (B15), **Ikaho** (stone-stepped onsen town, 1576), Haruna shrine | GAP |
| C16 Kai | none | Kōshū grapes (OL tree ✓, **trellis ✗**); dried persimmons (korogaki) ✓; Gunnai silk → weaver ✓; Kōshū inden → Lacquered deerskin maker ✓ | CT (Kōfu) ✓ | Missing: **Kōfu castle town, shogunal from 1724**; **Minobu-san Kubo-ji**; Erin-ji; the Takeda palace ruin (Tsutsujigasaki); Shichimen-zan. Shingen levee (OL ✓), Saruhashi (BL, OL ✓), Kurokawa gold (past, OL mine items ✓) are listed. | GAP |
| C17 Hida | none | Hida shunkei lacquer → Lacquerer ✓; Ichii carving `[not yet in 1730: c.1830s]` | Jinya town (Takayama) ✓ | Off the corridor; gasshō and board-roof houses already in BL | NOTHING NOTABLE |
| C18 Iga (added) | E95, E97 edges | Iga ware (verify) → Climbing-kiln potter ✓ | CT (Ueno) | See D6 | GAP |
| C19 Yamato (added) | W52–W57 | Miwa sōmen (OL ✓); Nara ink sticks → Ink-stick maker ✓; Nara bleached cloth → Cloth bleacher ✓ | ✓ | — | COVERED |
| C20 Izumi (added) | W51 | Sakai knives → Knife smith ✓ (Sakai named); incense ✓ | CT Kishiwada; jinai Kaizuka ✓ | — | COVERED |
| C21 Shimōsa (added) | none | Gyōtoku salt → Salt field ✓; Noda / Chōshi soy → Soy-sauce brewery ✓ | Temple town (Narita) ✓; **salt village ✗** | Visible across Edo Bay from the city | GAP |
| C22 Kazusa / Awa (Bōsō, added) | none | Hoshika sardine fertiliser → Dried-sardine fertilizer works ✓; whaling → Whaling station ✓ | Fishing ✓ | Nokogiri-yama quarry (the 500 rakan carving is `[not yet in 1730: 1779–98]`) | COVERED |
| C23 Tanba (added) | W15 (Tanba road) | Tanba ware ✓; chestnuts | — | Off-map west | NOTHING NOTABLE |
| C24 Shima (added) | E102 edge | Ama divers → Diver's beach fire hut ✓ | Fishing ✓ | Toba castle | COVERED |

### D. The land between the roads

| Row | Landmark | Meibutsu → trade covered? | Settlement type | Other | Status |
|---|---|---|---|---|---|
| D1 Kai / Kōfu basin | none | Grapes (trellis ✗), korogaki ✓, inden ✓ | Kōfu: CT under a shogunal garrison (kinban, 1724) ✓ layout, but no landmark | **The whole basin is unlisted**: Kōfu castle, Minobu, Erin-ji, Takeda ruin, grape trellises, Kai Zenkō-ji | GAP |
| D2 Lake Suwa and the Suwa shrines | W98 | Frozen tofu (verify) | CT Takashima (W98 ✓), PT ✓ | **Kamisha Honmiya and Maemiya** (the upper shrine: no honden, the mountain is the body; the Ontōsai deer-head offering, verify form) are missing; the lake → OL N §U ✓ | GAP |
| D3 Ina valley | none | Iida paper cord (motoyui / mizuhiki) (verify date) → ✗ (motoyui only as a barber's item); Ina chūma packhorse guild → Packhorse carrier (chūma) ✓ | CT (Iida, Takatō) ✓ | Missing: **Takatō and Ejima's confinement (1714–41)**; **Gonbei pass** (paved Kiso–Ina link, 1696); Iida; Kōzen-ji (Komagane) | GAP |
| D4 North and west sides of Fuji | E56 | Gunnai silk ✓; Fuji-kō talismans → Talisman window ✓ | Oshi town ≈ shrine-gate town §2.10 + Mountain-cult guide's house ✓ | Missing: **Kamiyoshida oshi town**, **Kitaguchi Hongū Fuji Sengen shrine** (Yoshida trail head), **Hitoana cave** (Kakugyō's cave, Fuji-kō holy site). Five lakes, Aokigahara, ice caves, Oshino springs → OL N §X ✓. | GAP |
| D5 Mino and Owari interior | W84, W85 | Seto / Mino ware ✓; Seki blades ✓; Mino paper ✓ | Wajū ✓ | Missing: Tanigumi-san, Yōrō falls (C13), Tajimi kilns as a place (the kilns themselves are covered) | GAP |
| D6 Iga and Kōka | E95, E97 edges | Shigaraki tea jars → Climbing-kiln potter ✓, tea jars in BL tea entries ✓; Iga ware (verify) | Kōka farmer-samurai → Farmer-samurai house ✓ | Missing: **Iga Ueno castle** (Tōdō Takatora's ~30 m ishigaki; keep `[gone by 1730: 1612 storm]`), the Iga / Yamato road from Seki to Nara, Bashō's birthplace (Ueno). Reality check: in 1730 Iga's "ninja" are Edo gate guards (Iga-gumi), and Kōka's medicine peddling is later (verify). | GAP |

### E. Linking and side roads

| Row | Landmark | Meibutsu → trade covered? | Settlement type | Other | Status |
|---|---|---|---|---|---|
| S1 Kōshū Kaidō (Edo to Shimo-Suwa) | Saruhashi (BL, OL) only | Hachiōji silk ✓; Kōshū grapes (trellis ✗) | PT chain ✓; **Hachiōji market town ✗** | **Naitō-Shinjuku `[gone by 1730: closed 1718; reopened 1772]`**, so the first station is Takaido. Missing: **Kobotoke checkpoint** and pass; Sasago pass; Hachiōji sennin-dōshin (the BL house ✓, the town ✗); Kōfu (D1). Ends at Shimosuwa (W98 ✓). | GAP |
| S2 Minoji (Tarui to Miya) | W83 (junction) | None firm | **Ōgaki** CT + river port (the Suimon river landing) | Missing: Ōgaki (Toda clan castle; Bashō ended *Oku no hosomichi* here in 1689); Okoshi ferry over the Kiso. Kiyosu `[gone by 1730: 1610]`, now a post town. | GAP |
| S3 Ise road (Hinaga to Yamada) + Ise betsukaidō (Seki to Tsu) | E92, E101 | Katagami ✓, Matsusaka cotton ✓ | PT chain; Tsu CT; Matsusaka merchant town ✗ layout (market town) | Missing: Tsu, Matsusaka, **Shiroko** port (a Kishū enclave, home of the katagami merchants), the betsukaidō | GAP |
| S4 Sayaji (Miya to Saya, then 3-ri boat to Kuwana; opened 1666) | E89 (the sea route it avoids) | None firm | PT chain (Iwatsuka, Manba, Kanie, Saya) ✓ | Missing: the Saya river landing and the three-ri river boat; **Tsushima shrine** close by (C7) | GAP |
| S5 Hime-kaidō | E78 | — | PT ✓ | — | COVERED |
| S6 Ōyama road | E33 | Ōyama tops (verify) → Toy maker ✓ | Oshi / sendōshi town ✓ | — | COVERED |
| S7 Kamakura and Enoshima roads | E31, E32 | See F5 | ✓ | — | COVERED |
| S8 Hokkoku kaidō | W101, W104, W105 | — | ✓ | — | COVERED |
| S9 Nikkō reiheishi road | W110 | — | ✓ | — | COVERED |
| S10 Sanshū / Ina road (Shiojiri to Okazaki) | W97 (fork) | Salt carried up from Mikawa → OL pack-ox path ✓, BL chūma ✓ | PT chain ✓ | The road itself has no entry; its gaps are logged under D3 | GAP |
| S11 Akiba road / southern salt road (Sagara to Akiba to Shinano) | E73 | Sagara salt → Salt field ✓ | — | Tanuma's Sagara castle `[not yet in 1730: 1767+]` | COVERED |
| S12 Saigoku kaidō (Kyoto to Yamazaki to Nishinomiya) | W33 | — | ✓ | Nishinomiya end: see C11 | COVERED |

### F. The coast off the road

| Row | Landmark | Meibutsu → trade covered? | Settlement type | Other | Status |
|---|---|---|---|---|---|
| F1 Edo Bay west shore (Shinagawa to Kanazawa) | E25, E27 | Nori ✓; Honmoku fish ✓ | Fishing ✓ | Missing: **Kanazawa Hakkei** (the Eight Views of Kanazawa: Nōken-dō viewpoint, Shōmyō-ji); Haneda fishing village and its Benten | GAP |
| F2 Edo waterfront (Tsukuda, Shiba, Fukagawa, Susaki) | E16–E18 | Tsukudani (preserved simmered small fish; commercial date (verify)) → ✗; **shirauo** whitebait torch-and-dip-net fishing for the shogun → ✗ | Fishing island inside the city (fits §2.4) | Missing: **Tsukudajima** (Settsu fishermen settled 1644); the elephant at Hama-goten (A00). Kiba log ponds ✓. | GAP |
| F3 Edo Bay east shore (Gyōtoku, Funabashi, Kisarazu) | none | Gyōtoku salt ✓; Kisarazu boats | **Salt village ✗** | Kisarazu-bune ferry privilege to Edo (from 1614) | GAP |
| F4 Uraga and Miura | none needed | Misaki fish ✓ | Port ✓ (Uraga in BL) | Uraga ship inspection 1720 ✓ BL | COVERED |
| F5 Enoshima and Kamakura | E31, E32 | Sazae and abalone ✓; Enoshima shell-work souvenirs (verify date) → ✗ | Fishing + temple town ✓ | Koshigoe fishing village | GAP |
| F6 Sagami Bay (Ōiso to Odawara to Manazuru) | E34, E36 | Odawara items ✓ | Fishing ✓ | Manazuru / Nebukawa andesite quarries for Edo castle → OL castle-stone quarry ✓ | COVERED |
| F7 Izu east coast (Atami, Ajiro, Itō) | E50 | Atami water sent to Edo castle in barrels (verify) | Onsen + fishing ✓ | Ajiro, a shelter and fishing port (verify) | COVERED |
| F8 Izu south and west (Shimoda, Toi, Heda) | none | Katsuobushi, tengusa ✓ | Port / fishing ✓ | Shimoda (C3) | GAP |
| F9 Suruga Bay north-east (Numazu, Senbon, Tago-no-ura) | E53, E55 | — | Fishing ✓ | Tsunami relocations (E55) | COVERED |
| F10 Suruga Bay west (Kurasawa, Shimizu, Yaizu) | E60, E62 | Yaizu katsuobushi → Dried-bonito works ✓; sazae ✓ | Fishing + port ✓ | — | COVERED |
| F11 Enshū-nada coast (Omaezaki, Sagara, Fukude, Kaketsuka) | none | Sagara salt ✓ | Fishing, dune coast (OL ✓) | Missing: **Kaketsuka** timber port. Omaezaki lighthouse `[not yet in 1730: 1874]` | GAP |
| F12 Lake Hamana | E76–E78 | **Hamana-nattō** (salted fermented black beans of Daifuku-ji, sent to Ieyasu) → Nattō maker ✓ (add the variant); wild eels ✓ | Fishing + sekisho ✓ | Kanzan-ji; the 1498 breach ✓ | COVERED |
| F13 Atsumi and Mikawa Bay | E79 | Kira salt ✓ | **Salt village ✗** | Irago cape (Bashō visited Tokoku there, 1687); Tahara CT | GAP |
| F14 Ise Bay north and Chita | E88–E91 | Chita sake shipped to Edo ✓; Tokoname ✓; Kuwana clams ✓ | Port, fishing, wajū ✓ | Nagashima CT | COVERED |
| F15 Ise Bay west (Yokkaichi, Shiroko, Tsu, Matsusaka) | E92 | Katagami ✓; cotton ✓ | Ports ✓ | Entry under S3 | GAP |
| F16 Ise Bay south (Futami, Toba) | E101, E102 | Futami sacred salt → Salt field ✓; ama ✓ | Fishing ✓ | — | COVERED |
| F17 Osaka Bay east (Osaka, Sakai, Kishiwada) | W35–W51 | Sakai knives ✓ | Great city, port ✓ | The 1707 Hōei tsunami ran up the Osaka canals and smashed boats into the bridges. The Taishō-bashi memorial stone is `[not yet in 1730: 1854]`. | COVERED |
| F18 Osaka Bay north (Amagasaki, Nishinomiya, Hyōgo) | none | Nishinomiya sake; taru-kaisen split 1730 (BL ✓) | Port ✓ (Hyōgo in BL §2.11) | Entries under C11 | GAP |
| F19 Lake Biwa shore (the lake as a coast) | W59–W77 | Funa-zushi ✓; Seta shijimi ✓ | Lake fishing villages (Katata) ✓ | Eri traps (C9) | GAP |

---

## 3. Gap entries, ready to add

Written in each list's own format. Where a gap is only an item missing from an existing entry, it says "add to".

### 3.1 BUILDING_LIST

**New settlement layouts for BL §2**
- **Market town (zaigō-machi / ichiba-machi)**: a rural town that lives by a fixed-day market (rokusai-ichi on the
  same digits each month: Yokkaichi on the 4s, Hachiōji on the 4s and 8s, Urawa on the 2s and 7s) rather than by a
  castle or a highway station. Layout: one or two long market streets wide enough for stalls down the centre, a
  market-god stone (ichigami) or shrine at the head, wholesalers (silk, cloth, grain, charcoal) with deep storehouses
  behind, a few inns and a toiya if it is also a station; 150–600 houses. Examples: Hachiōji (silk cloth, "Kuwa no
  miyako"), Ōme, Chichibu-Ōmiya, Yokkaichi, Honjō, Matsusaka (a merchant town), Itami (a sake-brewing town: the same
  plan, with brewery kura along the streets). Items: stall frames and awnings set up on market days, weigh scales,
  the market-god stone, bale stacks, cloth-dealer shop fronts.
- **Salt-making village (shiohama-mura)**: a beach village organised round spread-type salt fields (agehama). Layout:
  levelled sand fields in strips behind the beach, each with a brine pit and a boiling hut (kama-ya); a firewood and
  pine-needle stack yard; labourers' huts in a row behind; the field owner's big house; a salt storehouse and a
  shipping landing. The Edo-supply example is Gyōtoku (Shimōsa); on the corridor also Kira / Yoshida-hama (Mikawa),
  Chita, Futami (the Ise shrine's sacred salt), and small works on the Yui–Kanbara and Sagara beaches. Items: see BL
  Salt, OL R §16. Loot tier: low.

**New trades**
- **Oiled-paper rain-cape maker (kappa-ya)**: capes and covers of persimmon-tanned, oiled paper, often red; Toriimoto's
  meibutsu, sold to travellers, and made in every big town. Town workshop and shop. Items: paper sheets pasted in
  layers, oil pots and brushes, drying lines of capes, cape patterns, stacked folded capes, a red sample hung at the
  front.
- **Kudzu-cloth weaver (kuzu-fu-ya)**: cloth woven from kudzu-vine fibre (warp of silk or cotton, weft of kuzu), light
  and water-shedding, for hakama, rain gear and fusuma; Kakegawa's meibutsu. Rural workshop and town shop. Items: vine
  bundles soaking in a stream-side tub, fermenting pits, fibre skeins, a loom, rolls of glossy tan cloth. (Extends
  Wild-fibre weaver, which lists fuji-fu and shina-fu only.)
- **Calendar maker (koyomi-shi)**: licensed printers of annual calendars; the Mishima-goyomi (Kawai family, beside
  Mishima Taisha) and the Ise-goyomi were the famous ones. Town workshop. Items: calendar blocks, printing tables,
  folded almanacs in bundles, a licence board. (verify the Kawai family's 1730 output)
- **Folk-painting souvenir shop (Ōtsu-e-ya)**: roadside shop and studio selling cheap, fast-painted folk pictures
  (demon monk, wisteria maiden, falconer) and amulet prints, at Ōtani and Oiwake between Ōtsu and Kyoto. Road-front
  shop, raised. Items: stencils and stamps, pigment pots, sheets pegged to dry, finished pictures pinned up at the
  front.
- **Miso brewery (miso-gura), Hatchō type**: a brewery kura where soybean miso is aged for two summers in giant cedar
  vats (about 2 m) weighted by cones of river stones. Two families in Hatchō village by Okazaki castle. Site. Items:
  the vats, the stone cones, bean steamers, a stone-pounding floor, carrying poles. (Miso maker in BL is a town
  shop.)
- **Paper-cord maker (motoyui-ya)**: twisted and glued paper cords for hair ties (motoyui) and gift knots (mizuhiki);
  Iida (Ina valley) is the corridor's centre (from the 1660s is claimed (verify)). Rural workshop. Items: paper strips,
  twisting wheel, starch pots, dyed cord hanks drying on poles.
- **Preserved-fish maker, Tsukuda type (tsukudani-ya)**: small fish and shellfish simmered hard in soy and salt as a
  keeping food; Tsukudajima's fishermen. Waterside workshop. Items: iron simmering pans, fish baskets, tubs, packed
  jars. (verify when tsukudani became a commercial product)
- **Shell-craft souvenir maker (kai-zaiku)**: shell boxes, shell-flower ornaments and shell spoons sold to Enoshima
  pilgrims. Stall or small shop. Items: shells sorted in trays, glue, small drills, finished pieces. (verify the date)

**Item additions (no new entry)**
- Rice-cake and dumpling shop: add **somemeshi** (gardenia-yellow rice, Seto near Fujieda), **nagamochi** (Hinaga)
  and **kashiwa-mochi** (Sarugababa) as named variants.
- Dried-goods shop or Rice polisher: add **yakigome** (roasted rice in small straw bales, Shōno).
- Nattō maker: add **Hamana-nattō / temple nattō** (salted fermented black beans, Daifuku-ji by Lake Hamana).
- Lime burner: add **Akasaka (Mino)**, fed from the Kinshōzan limestone hill, to Hachiōji / Ōme.

### 3.2 OUTDOOR (OL)

- **Fixed lake fish trap (eri)**: arrow-shaped fences of bamboo and reed screens driven into the shallows of Lake Biwa;
  fish follow the leader fence into a heart-shaped trap chamber, emptied from boats. Lake shore, common (Lake Biwa),
  large (fences run tens of metres out). Hook: food, and a maze of wading cover along the shallows.
- **Grape trellis (budō-dana)**: flat, head-high overhead trellis of bamboo and poles carrying Kōshū grape vines,
  Katsunuma and the east Kōfu basin. Field, rare (Kai only), large. Hook: food in autumn, shade and cover under the
  canopy. (The plant is already in OL N §D; the structure is not.)
- **Obsidian scatter (kokuyōseki / "hoshi-kuso", star dung)**: black glass shards and small nodules in the soil and
  streambeds of the Wada pass. Mountain ground, rare, `[terrain decal]` plus small rocks. Hook: lore; sharp stone.
  (Already in W99, but not in OL.)
- **Limestone hill and lime quarry (sekkai-yama)**: a bare, pale, terraced quarry face on a small limestone hill with a
  lime kiln at its foot, as at Kinshōzan (Akasaka, Mino); Chichibu is the other corridor source. Hill, rare, large
  `[terrain]` + kiln. Hook: landmark, stone; ties to BL Lime burner. (verify that 1730 working at Kinshōzan was large)
- **River rapids boat and landing (kawa-bune no funatsuki)**: long, narrow, flat-bottomed boats that ran down the Fuji
  (and Tenryū) rapids loaded, and were hauled back up by men on a towline. The landings are gravel banks with a
  storehouse and mooring posts. River, occasional (Fuji, Tenryū), medium–large. Hook: fast river travel, vehicle
  candidate. (OL's towpath is canal-only.)
- **Whitebait torch fishing (shirauo-ryō)**: winter-night fishing at the Sumida mouth and off Tsukudajima with four-arm
  dip nets (yotsude-ami) and bonfire baskets hung over the bow; the catch went first to the shogun. Shore / river
  mouth, occasional (Edo), small props (torch basket, dip-net frame). Hook: night light sources on the water.
- **Levee-top highway (dote-michi)**: a main road running along a river levee crest, as on the Kyōkaidō's Bunroku levee
  (Yodo, 1596) and the Kumagaya levee (W112). River/field, occasional, `[terrain]`. Hook: exposed high road, sightlines.

### 3.3 LANDMARKS

Format as E/W: 1730 / Era / Fame / Play. Grouped by which file should hold them (E = east of Ōtsu, W = Kyoto side and
Nakasendō).

**For E (Edo, Tōkaidō, and the east side)**
- **Hama-goten and the shogun's elephant (Hama-goten, zō-goya)**: Edo Bay shore, Shiba. **1730:** the shogunal seaside
  villa with its tidal pond (OL already has the garden), and in it a stable house for the bull elephant sent from
  Vietnam, which walked the Tōkaidō in spring 1729 and is the sensation of the city. **Era:** IN; the elephant stayed
  until 1742, then went to a farmer at Nakano (verify). **Fame:** national (prints, books, dung sold as medicine
  (verify)). **Play:** a unique set; an escaped-elephant event is a cheap, memorable map story. Set: compound.
- **Tsukudajima (Tsukudajima)**: island at the Sumida mouth. **1730:** fishing village of Settsu fishermen (settled
  1644) with a Sumiyoshi shrine, net sheds, and the whitebait fishery for the shogun. **Era:** IN. **Fame:** regional.
  **Play:** a low-tier fishing island inside the high-tier city. Set: district.
- **Kanazawa Hakkei (Kanazawa hakkei, Nōken-dō, Shōmyō-ji)**: Musashi coast south of Edo. **1730:** a famous bay of
  islets and pine headlands viewed from the Nōken-dō hill tea houses; Shōmyō-ji (Kanazawa Hōjō family temple). **Era:**
  IN. **Fame:** regional to national (the eight views, 17th c.). **Play:** a viewpoint and a sniper hill over a bay.
  Set: natural site + temple.
- **Kobotoke checkpoint and pass (Kobotoke sekisho, Kobotoke-tōge)**: Kōshū Kaidō, Musashi–Sagami/Kai border.
  **1730:** a small highway barrier in a narrow valley below a wooded pass; papers checked especially for women.
  **Era:** IN. **Fame:** regional. **Play:** the Kōshū road's PvP chokepoint. Set: compound.
- **Hachiōji market town and the Sennin-dōshin (Hachiōji)**: Kōshū Kaidō. **1730:** fifteen joined post-and-market
  quarters with a big silk-cloth market, and the "thousand men" farmer-samurai guard (BL house ✓). **Era:** IN.
  **Fame:** regional. **Play:** a mid-tier market town on the inland road. Set: district.
- **Kōfu castle town (Kōfu-jō, Kōfu kinban)**: Kai. **1730:** a keepless stone-walled castle garrisoned by shogunal
  guards (kinban) since the Yanagisawa left in 1724; a townsmen's grid below. **Era:** IN (the keep question is
  debated; treat as keepless (verify)). **Fame:** regional. **Play:** the high-tier castle of the inland basin. Set:
  district.
- **Minobu-san Kubo-ji (Minobu-san Kuon-ji)**: Kai, Fuji river valley. **1730:** the Nichiren head temple: a
  mountainside of halls, a 287-step stone stair (Bodai-tei), and a monzen-machi of pilgrim lodges. **Era:** IN
  (halls rebuilt over time (verify)). **Fame:** national. **Play:** a mountain temple town and a stair climb.
  Set: district.
- **Erin-ji and the Takeda palace ruin (Erin-ji, Tsutsujigasaki-yakata ato)**: Kōfu basin. **1730:** Shingen's family
  temple and grave with a Musō garden; the Takeda palace site as moats and earthworks. **Era:** IN (ruin);
  Takeda shrine `[not yet in 1730: 1919]`. **Fame:** regional. **Play:** a ruin plus a temple. Set: compound.
- **Kamiyoshida oshi town and Kitaguchi Hongū Fuji Sengen shrine (Kamiyoshida, Kitaguchi Hongū Fuji Sengen jinja)**:
  north foot of Fuji. **1730:** a cedar-avenue shrine at the Yoshida trail head and a street of oshi houses (pilgrim
  lodges with altar rooms) serving the Fuji-kō. **Era:** IN; Jikigyō Miroku's fast `[not yet in 1730: 1733]`.
  **Fame:** national among Edo commoners. **Play:** the summit route's base camp. Set: district.
- **Hitoana cave (Hitoana Fuji-kō iseki)**: west foot of Fuji. **1730:** the lava-tube cave where Hasegawa Kakugyō
  practised, with votive stones of the Fuji-kō. **Era:** IN (most stelae later (verify)). **Fame:** within the Fuji-kō.
  **Play:** a cave dungeon. Set: natural site.
- **Tanaka castle (Tanaka-jō)**: Fujieda. **1730:** a rare concentric round castle of rings of moats and earth walls.
  **Era:** IN. **Fame:** local. **Play:** a mid-tier castle with a unique round plan. Set: compound.
- **Yokosuka castle (Yokosuka-jō)**: Tōtōmi coast. **1730:** a castle with walls of rounded river stones on a long
  ridge. **Era:** IN. **Fame:** local. **Play:** a small coastal castle. Set: compound.
- **Enshū three temples (Kasuisai, Hattasan Sonei-ji, Yusan-ji)**: hills north of Fukuroi. **1730:** a Sōtō training
  temple and two mountain Kannon / Yakushi temples. **Era:** IN. **Fame:** regional. **Play:** a temple cluster off
  the midpoint of the road. Set: compound.
- **Hōrai-ji and Nagashino (Hōrai-ji, Nagashino kosenjō)**: Mikawa hills. **1730:** a mountain shugen temple up a long
  stone stair with its Tōshōgū (1651), and the 1575 battlefield below Nagashino castle ruin. **Era:** IN.
  **Fame:** regional / national (battle). **Play:** a stair temple plus a battlefield. Set: compound + natural site.
- **Shirotori timber yard (Shirotori chozōjo)**: by Atsuta, Owari. **1730:** the domain's log ponds and yards where
  Kiso timber arrived by raft and sea. **Era:** IN. **Fame:** regional. **Play:** walkable log rafts and a timber
  depot. Set: compound.
- **Tsushima shrine (Tsushima jinja)**: Owari, near the Sayaji. **1730:** head shrine of the Tsushima–Tennō cult,
  with the summer lantern-boat festival (makiwara-bune). **Era:** IN. **Fame:** regional. **Play:** a shrine town;
  festival night lights. Set: compound.
- **Tsu and Matsusaka (Tsu jōkamachi, Matsusaka)**: Ise road. **1730:** Tsu, the Tōdō castle town; Matsusaka, a
  merchant town of Edo-connected houses (the Mitsui home town) and cotton dealers. **Era:** IN. **Fame:** regional.
  **Play:** mid-tier towns on the Ise road. Set: district each.
- **Shimoda port (Shimoda-minato)**: Izu. **1730:** a sheltered harbour whose ship-inspection post moved to Uraga in
  1720, leaving a fishing and refuge port. **Era:** IN; the bugyō `[gone by 1730: 1720]`. **Fame:** regional.
  **Play:** a far-corner port. Set: district.
- **Kaketsuka timber port (Kaketsuka-minato)**: Tenryū river mouth. **1730:** where Tenryū rafts were broken up and the
  timber shipped to Edo. **Era:** IN (verify the scale). **Fame:** local. **Play:** a log beach. Set: compound.

**For W (Kyoto side, Nakasendō, Kansai)**
- **Suwa Kamisha (Suwa Taisha Kamisha Honmiya, Maemiya)**: the south shore of Lake Suwa. **1730:** the upper shrine,
  which has no main sanctuary because the mountain behind is the kami. It has worship halls and its own four
  onbashira pillars, and holds the spring Ontōsai rite with deer-head offerings (verify the 1730 form). **Era:** IN.
  **Fame:** national. **Play:** the pair to W98. Set: compound.
- **Tanigumi-san Kegon-ji (Tanigumi-san Kegon-ji)**: Mino, north-west of Ōgaki. **1730:** the 33rd and last temple of
  the Saigoku Kannon pilgrimage, where pilgrims hang up their robes and staffs. **Era:** IN. **Fame:** national.
  **Play:** a pilgrim terminus and temple town. Set: district.
- **Yōrō falls and Yōrō shrine (Yōrō no taki)**: Mino, west of Ōgaki. **1730:** a ~30 m waterfall of the filial-son
  legend (the water that turned to sake). **Era:** IN. **Fame:** national. **Play:** a scenic falls and a rest point.
  Set: natural site.
- **Ōgaki castle town and river port (Ōgaki)**: Minoji. **1730:** a Toda-clan castle town on the water, with a boat
  landing on the Suimon river to Kuwana; Bashō's journey ended here in 1689. **Era:** IN. **Fame:** regional.
  **Play:** a mid-tier castle town on the side road. Set: district.
- **Naegi castle (Naegi-jō)**: above the Kiso near Nakatsugawa. **1730:** a small castle built onto giant granite
  boulders on a crag. **Era:** IN. **Fame:** local. **Play:** a rock-top castle. Set: compound.
- **Kiso Yoshinaka's home ground (Tokuon-ji, Hatage Hachimangū)**: Miyanokoshi. **1730:** the family temple and grave,
  and the shrine where he raised his banner in 1180. **Era:** IN. **Fame:** regional. **Play:** a small shrine-temple
  pair. Set: compound.
- **Manpuku-ji (Ōbaku-san Manpuku-ji)**: Uji. **1730:** the Ōbaku Zen head temple (1661), built in Ming Chinese style
  with Chinese monks. **Era:** IN. **Fame:** national. **Play:** a visually distinct temple compound. Set: compound.
- **Moriguchi post town and the Bunroku levee (Moriguchi-juku, Bunroku-zutsumi)**: Kyōkaidō. **1730:** the last
  station before Osaka, on Hideyoshi's levee road along the Yodo; pickle shops. **Era:** IN. **Fame:** regional.
  **Play:** the Osaka approach, with a high road. Set: district.
- **Nishinomiya Ebisu shrine (Nishinomiya jinja)**: Settsu coast. **1730:** the head Ebisu shrine; its puppeteer
  village (Ebisu-kaki) toured the country; the new taru-kaisen sake ships sail from this port (1730). **Era:** IN.
  **Fame:** national. **Play:** a port-shrine town. Set: compound.
- **Minatogawa, grave of Kusunoki Masashige (Minatogawa, Nankō no haka)**: Hyōgo. **1730:** the loyalist's grave with
  Tokugawa Mitsukuni's 1692 stele, "Aa chūshin Nanshi no haka". **Era:** IN; Minatogawa shrine
  `[not yet in 1730: 1872]`. **Fame:** national. **Play:** a small memorial site. Set: single.
- **Arima hot spring (Arima onsen)**: Settsu, behind Rokkō. **1730:** a famous old spa town of bath inns round the
  public baths, with basket and brush makers. **Era:** IN. **Fame:** national. **Play:** an onsen town in the hills.
  Set: district.
- **Iga Ueno castle and town (Iga Ueno-jō)**: Iga. **1730:** Tōdō Takatora's towering stone walls (~30 m), with the
  keep `[gone by 1730: 1612 storm]`; a castle town, Bashō's birthplace. **Era:** IN (walls). **Fame:** regional.
  **Play:** the tallest wall climb on the map. Set: district.
- **Kōnoike shinden and the new Yamato river (Kōnoike shinden, shin-Yamato-gawa)**: Kawachi. **1730:** a straight new
  river cut to the sea (1704) and, on the old riverbeds, cotton new-fields run from the Kōnoike family's walled
  estate office (kaisho, 1707). **Era:** IN. **Fame:** regional. **Play:** a planned farm grid and one big compound.
  Set: compound + terrain.
- **Ejima's confinement house at Takatō (Takatō, Ejima kakoi-yashiki)**: Ina valley. **1730:** the small castle town
  where the palace lady Ejima (the 1714 scandal) is held for life; she dies there in 1741. **Era:** IN. **Fame:**
  national scandal. **Play:** a guarded house, a rescue story. Set: compound.
- **Gonbei pass (Gonbei-tōge)**: Kiso–Ina divide. **1730:** a mountain road paved by Ina villagers in 1696 to carry
  rice into the Kiso. **Era:** IN. **Fame:** regional. **Play:** a high pass linking the valleys. Set: terrain.
- **Isobe and Ikaho hot springs (Isobe onsen, Ikaho onsen)**: Kōzuke. **1730:** Isobe, a mineral spring near Annaka;
  Ikaho, a hillside town of bath inns on a stone stairway laid in 1576. **Era:** IN. **Fame:** regional. **Play:**
  onsen towns. Set: district.

---

## 4. Meibutsu index

The "trade" column names the BL entry that covers it; ✗ means §3.1 adds it. "Status" is the era check.

| Meibutsu | Station(s) | Trade building | Status |
|---|---|---|---|
| Nori (Asakusa nori) | Shinagawa, Ōmori | Nori farm and drying yard; Nori farmer's cottage | IN |
| Wachūsan stomach powder | Ōmori / Kamata | Medicine shop | IN (verify date) |
| Straw-work boxes (mugiwara-zaiku) | Ōmori | Straw-goods maker | verify date |
| Nara-chameshi (tea rice) | Kawasaki (Mannen-ya) | Tea-rice shop | fame c.1760s (verify) |
| Yone-manjū | Tsurumi | Steamed-bun shop | IN (early 1700s) |
| Botamochi | Sakaigi (Hodogaya) | Rice-cake and dumpling shop | IN (verify) |
| Uirō | Odawara | Medicine shop; Souvenir shop | IN |
| Kamaboko | Odawara | Kamaboko maker | IN |
| Umeboshi | Odawara | Umeboshi works | IN |
| Odawara folding lantern | Odawara | Lantern maker | IN |
| Hakone woodturning | Yumoto, Hatajuku | Hakone woodcraft maker | IN; yosegi c.1800s |
| Mishima calendar | Mishima | ✗ Calendar maker | IN |
| Chestnut mochi | Iwabuchi | Rice-cake shop | verify |
| Satō-mochi / tamago-mochi | Yui | Rice-cake shop | attested later (1802) |
| Grilled sazae and abalone | Kurasawa | Roadside tea house; Fishmonger | IN (attested 1802) |
| Abekawa-mochi | Fuchū | Rice-cake shop | IN |
| Suruga lacquer | Fuchū | Lacquerer | verify |
| Abe (Ashikubo) tea | Fuchū, Suruga hills | Tea processing shed; Tea-leaf dealer | IN |
| Tororo-jiru | Mariko | Cook-shop (Chōjiya, E67) | IN (1596 shop) |
| Tōdango | Utsunoya / Okabe | Rice-cake shop | IN |
| Somemeshi | Seto (Fujieda) | Rice-cake shop (add variant) | IN (Sengoku origin) |
| Nameshi-dengaku | Kikugawa; Megawa | Dengaku stall or shop | mid-Edo (verify 1730) |
| Kosodate-ame | Sayo-no-Nakayama | Candy maker | IN (verify) |
| Warabi-mochi | Nissaka | Rice-cake shop | verify |
| Kuzu-fu (kudzu cloth) | Kakegawa | ✗ Kudzu-cloth weaver | IN |
| Tamago-fuwafuwa | Fukuroi | Cheap cook-shop | attested 1813 |
| Eel kabayaki | Arai | Eel shop | attested 1830s |
| Hamana-nattō | Lake Hamana (Daifuku-ji) | Nattō maker (add variant) | IN |
| Kashiwa-mochi | Sarugababa (Futagawa) | Rice-cake shop | verify |
| Hatchō miso | Okazaki | ✗ Miso brewery (Hatchō type) | IN |
| Okazaki stone lanterns | Okazaki | Stonemason's yard | IN |
| Mikawa cotton | Okazaki area | Cotton-cloth wholesaler | IN |
| Horses (horse fair) | Chiryū | Commercial stable and horse dealer | IN |
| Arimatsu / Narumi shibori | Arimatsu, Narumi | Tie-dyer | IN (from 1608) |
| Yaki- and shigure-hamaguri | Kuwana, Tomida | Food stall; Souvenir shop | IN |
| Kuwana cast iron | Kuwana | Caster of pots and kettles | IN |
| Nagamochi | Hinaga (Yokkaichi) | Rice-cake shop (add variant) | IN (1550 shop) |
| Banko ware | Yokkaichi / Kuwana | Potter | not yet (c.1736–41) |
| Yakigome | Shōno | ✗ item for Dried-goods shop | IN |
| Seki-no-to | Seki | Fine confectioner | IN (verify) |
| Kanpyō | Minakuchi | Drying shed; OL gourd-strip drying poles | IN (pre-1712) |
| Tsuzura baskets | Minakuchi | Bamboo worker | verify |
| Ubagamochi | Kusatsu | Rice-cake shop | IN |
| Ōtsu-e | Ōtani / Oiwake (Ōtsu) | ✗ Folk-painting souvenir shop | IN |
| Ōtsu abacus | Ōtsu | Abacus maker | IN (1612) |
| Fushimi sake | Fushimi | Sake brewery | IN |
| Fushimi clay dolls | Fushimi | Clay-doll maker | IN |
| Kurawanka food boats | Hirakata | Food stall | IN |
| Moriguchi-zuke | Moriguchi | Pickle maker | IN |
| Urawa market | Urawa | Market stalls | verify |
| Kōnosu hina dolls | Kōnosu | Doll maker | verify |
| Safflower | Okegawa | Safflower processing | not yet (c.1790s) |
| Silk and cloth market | Honjō, Takasaki | Silk thread dealer | IN |
| Daruma | Takasaki | Toy and doll makers | not yet (c.1780s) |
| Chikara-mochi | Usui pass (Sakamoto) | Rice-cake shop | IN (verify) |
| Kanten | Shimosuwa | Agar maker | not yet (1840s) |
| Soba-kiri | Motoyama | Soba shop | IN (1706 text) |
| Kiso lacquer | Hirasawa, Narai | Lacquerer | IN |
| Oroku combs | Yabuhara | Comb maker | IN |
| Kiso horses | Fukushima | Horse dealer; Horse-dealers' inn | IN |
| Hanazuke (pickled blossoms) | Suhara | Pickle maker | verify |
| Hachiya-gaki | Ōta | Drying shed; OL hoshigaki | IN |
| Kanō umbrellas | Kanō (Gifu) | Umbrella maker | IN (1639, verify) |
| Gifu lanterns | Kanō (Gifu) | Lantern maker | verify |
| Akasaka lime | Akasaka (Mino) | Lime burner (add place) | verify |
| Ibuki moxa | Kashiwabara | Moxa shop | IN |
| Akadama pill | Toriimoto | Medicine shop | IN (1658, verify) |
| Kappa rain capes | Toriimoto | ✗ Oiled-paper rain-cape maker | IN |
| Takamiya ramie cloth | Takamiya | Hemp and ramie processor; Cloth bleacher | IN |
| Funa-zushi | Lake Biwa | Sushi seller (nare-zushi) | IN |
| Seki blades | Seki (Mino) | Swordsmith; Knife smith | IN |
| Mino paper | Mino | Paper mill | IN |
| Kōshū grapes | Katsunuma (Kai) | OL grape; ✗ grape trellis | IN |
| Korogaki (dried persimmons) | Kai | Drying shed | IN |
| Gunnai silk | Kai (Gunnai) | Town or village weaver | IN |
| Kōshū inden | Kōfu | Lacquered deerskin maker | IN |
| Hachiōji silk cloth | Hachiōji | Town weaver; Cotton-cloth wholesaler | IN |
| Iida paper cord | Iida | ✗ Paper-cord maker | verify |
| Ise katagami | Shiroko | Stencil cutter | IN |
| Matsusaka cotton | Matsusaka | Cotton-cloth wholesaler | IN |
| Itami / Ikeda sake | Itami, Ikeda | Sake brewery | IN |
| Ikeda charcoal | Ikeda (from Nose) | Charcoal and firewood dealer | IN |
| Arima baskets | Arima | Bamboo worker | IN |
| Sakai knives | Sakai | Knife smith | IN |
| Gyōtoku salt | Gyōtoku | Salt field (spread type) | IN |
| Kira salt | Kira (Mikawa) | Salt field (spread type) | IN |
| Yaizu / Izu katsuobushi | Yaizu, west Izu | Dried-bonito works | IN |
| Tsukudani | Tsukudajima | ✗ Preserved-fish maker | verify date |
| Shell crafts | Enoshima | ✗ Shell-craft maker | verify date |
| Kiryū silk | Kiryū | Town or village weaver | IN (drawloom 1738) |

---

## 5. Corrections to the existing lists

1. **BL, Execution grounds (line ~2210):** "Osaka's Sennichi" should be **Tobita**. Sennichi was the cemetery and
   cremation ground; W48 already flags this.
2. **N / R / OL, kanpyō (OL "Gourd trellis" and "Gourd-strip drying poles"):** the lists tie kanpyō to Mibu
   (Shimotsuke, 1712) and rate it "occasional (Shimotsuke)", which reads as off-map. The usual story is the other way
   round: in 1712 the Torii lord moved **from Minakuchi (Ōmi, Tōkaidō station 50) to Mibu** and took kanpyō growing
   with him. So kanpyō on our map is older than 1712, and it is at Minakuchi. E97 already says so. Suggest the
   commonness note reads "occasional (Minakuchi; Shimotsuke from 1712)" (verify).
3. **E list scope vs the map:** E stops at Ōtsu and W covers Fushimi, Yodo and Hirakata. The fourth Kyōkaidō station,
   **Moriguchi**, is in neither, so the Osaka approach has a hole (see §3.3). This is a seam, not an error.
4. **W83:** "Nanguu shrine" is a typo for **Nangū** (Nangū Taisha).
5. **BL Tea-rice shop:** it dates the shop to "Asakusa after 1657" but doesn't name Kawasaki's Mannen-ya, the
   Tōkaidō's most famous one. Mannen-ya's fame is usually given from the Meiwa era (1764–72). If it is used on the
   Tōkaidō, tag it (verify).
6. **FEASIBILITY.md §3 layout:** the sketch puts the "central range" and the Hakone-style pass between the capitals.
   The real inland ground between the roads is the Kai basin and the Suwa–Ina valleys, and the lists have almost
   nothing for them (§1 gaps 1, 2 and 7). This is not an error in a list, but the draft layout and the research
   don't meet there.
7. **OL "Commons pasture (maki)" "(verify for our map)":** this can be settled. Mochizuki (W100) and the Kiso horse
   country (W92) are on the corridor.

No other contradictions were found in the rows checked. The era tags in E and W were consistent with what this
audit found, for example Kuwana's keep (1701), Numazu castle, Arai's moves, Takasaki daruma and Makinohara tea.

---

## Key: W numbers used in this audit

`W_KANSAI_NAKASENDO.md` has no IDs. These are its `###` headings in file order.

W01 Imperial Palace · W02 Nijō Castle · W03 Kiyomizu-dera · W04 Hōkō-ji Daibutsu · W05 Sanjūsangendō · W06 Tō-ji ·
W07 Rashōmon site · W08 Kinkaku-ji · W09 Ginkaku-ji · W10 Nishi Honganji · W11 Higashi Honganji · W12 Chion-in ·
W13 Yasaka Shrine · W14 Gion / Shijō / Pontochō · W15 Shimabara · W16 Sanjō Ōhashi · W17 Awataguchi / Keage ·
W18 Fushimi Inari · W19 Fushimi river port · W20 Nanzen-ji · W21 Kitano Tenmangū · W22 Nishijin · W23 Kamigamo /
Shimogamo · W24 Daitoku-ji, Myōshin-ji, Ryōan-ji · W25 Tōfuku-ji · W26 Arashiyama · W27 Atago · W28 Kurama-dera ·
W29 Daigo-ji · W30 Katsura / Shugaku-in · W31 Uji · W32 Yodo castle · W33 Iwashimizu / Yamazaki · W34 Hirakata ·
W35 Osaka Castle · W36 Dōjima · W37 Nakanoshima · W38 Zakoba / Tenma markets · W39 Osaka Tenmangū · W40 Naniwa
bridges · W41 Dōtonbori · W42 Shinmachi · W43 Sonezaki · W44 Shitennō-ji · W45 Sumiyoshi · W46 Sumitomo refinery ·
W47 Kawaguchi · W48 Tobita / Sennichi · W49 Kaitokudō · W50 Ikutama · W51 Sakai · W52 Tōdai-ji · W53 Kōfuku-ji ·
W54 Kasuga · W55 Hōryū-ji / Yakushi-ji · W56 Kōya-san · W57 Yoshino · W58 Ise (reference) · W59 Ōtsu port ·
W60 Ōsaka pass · W61 Seta bridge · W62 Ishiyama-dera · W63 Mii-dera · W64 Karasaki pine · W65 Katata Ukimidō ·
W66 Hiei / Enryaku-ji · W67 Sakamoto / Hiyoshi · W68 Zeze castle · W69 Gichū-ji · W70 Kusatsu junction ·
W71 Ōmi-Hachiman · W72 Azuchi ruins · W73 Hikone castle · W74 Taga Taisha · W75 Chikubushima · W76 Nagahama /
Kunitomo · W77 Hira / Awazu / Yabase · W78 Suribari pass · W79 Toriimoto · W80 Samegai · W81 Kashiwabara ·
W82 Sekigahara · W83 Tarui · W84 Gifu castle ruin · W85 Inuyama · W86 Ōta ferry · W87 Ochiai pavement · W88 Magome ·
W89 Tsumago · W90 Nezame no Toko · W91 Kiso kakehashi · W92 Kiso-Fukushima sekisho · W93 Ontake · W94 Torii pass ·
W95 Narai · W96 Kiso forbidden forest · W97 Shiojiri pass · W98 Shimosuwa / Suwa Taisha · W99 Wada pass ·
W100 Mochizuki / Chikuma crossing · W101 Oiwake · W102 Asama · W103 Karuizawa / Kutsukake · W104 Zenkō-ji ·
W105 Komoro, Ueda, Matsumoto · W106 Usui pass · W107 Usui sekisho · W108 Myōgi · W109 Takasaki · W110 Kuragano ·
W111 Honjō · W112 Kumagaya levee · W113 Ōmiya Hikawa · W114 Toda ferry · W115 Itabashi.

## Sources (web, this session)

- Shizuoka prefecture food-culture page on Tōkaidō meibutsu (Yui, Mariko, Fujieda somemeshi, Fukuroi, Arai):
  fujinokuni.shokunomiyako-shizuoka.pref.shizuoka.jp/culture/article/2434
- Kanagawa tourism and Kantō regional bureau Tōkaidō pages (Sakaigi botamochi, Fujisawa's 1843 "meibutsu")
- Tsurumi yone-manjū histories (Seigetsu shop, Yokohama Tsurumi ward): famous from the early 1700s
- Kawasaki Nara-chameshi (MAFF regional cuisine page; Mannen-ya)
- Kabuki-za "Edo shoku bunka kikō" no.228 (Shōno yakigome, Minakuchi kanpyō)
- Shizuoka Japan Heritage (Nishi-Kurasawa sazae and abalone in *Hizakurige*)
- Shiojiri, Kiso and Hikone tourism pages (Motoyama soba-kiri, Yabuhara Oroku combs, Suhara hanazuke, Usui
  chikara-mochi, Toriimoto red pill, kappa and watermelon)
- Elephant of 1728–29: ja.wikipedia 広南従四位白象; Wa-raku web; NDL reference database (route); Hirakata local
  history note
