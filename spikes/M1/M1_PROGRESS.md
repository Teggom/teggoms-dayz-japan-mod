# M1 progress: the missing materials (accuracy first)

Agent M1 (opus), 2026-09-30. Time log `japan_dev/TIMELOG_M1.md` (logger `spikes/M1/tlog.py`). Waited for S1 (owner of
the materials pipeline) before any write to research/materials, src/JP/common/materials or playbook/palette.json.

## Checkpoint 1 (research + drafts, nothing in the pipeline yet)
- Samples: `spikes/M1/sample.py` -> `samples.json`, crops in `crops/`, box overlays in `look/boxes_*.jpg`.
- Recipes + atlases: `spikes/M1/make_m1_materials.py` (`--draft` renders to `spikes/M1/draft/`; the real run goes
  through B1's `make_one` once copied to `research/materials/`).
- Bonji: NOT made. `spikes/M1/font_scan.py` read the cmap of 683 font files (C:\Windows\Fonts, user fonts, Program
  Files, all of D:\): the only fonts mapping Siddham (U+11580-115FF) are Unreal Engine's `LastResort.ttf` copies,
  which draw placeholder boxes, not letters. Needed: **Noto Sans Siddham** (SIL OFL 1.1, google/fonts
  `ofl/notosanssiddham/NotoSansSiddham-Regular.ttf`). Not downloaded (brief).

## Colours: sampled values and sources (playbook method: mid-70 % luminance median per box, mean of boxes)
| New palette id | sRGB | Kept boxes (ref: value) | Rejected |
|---|---|---|---|
| `earth_bare` | 148,130,108 | k41 Matsudo Kanto-loam topsoil, sunlit 197,171,127; k37 Shikaumi shrine brown forest soil 138,117,108 and 117,101,84; k27 worn path under a Hida torii 140,133,112 | k41 deep shade 77,69,57 (B1's doma rule); x03 (concrete); x08 (museum sand yard) |
| `wood_new_cut` | 172,146,129 | i04 three freshly split conifer sticks by the Tsunashima irori, white-balanced on the hearth ash in the same light (raw 144,150,152 -> ash_grey chromaticity): 190,165,143 / 161,134,115 / 164,141,127 | k36 (red pine end grain, low sun); x01 bottom (plywood); hinoki_planks scan (oiled-looking, 156,122,84) |
| `wood_silver_grey` | 126,125,120 | k31 old unpainted handcart, sun 130,124,112; c03 Tsumago gate post 146,146,145 and board leaf 103,104,103 (sun) | x01 storehouse gable (evening shade 57-64 even after WB on the plaster); c04 gate posts (backlit 44-53) |
| `wicker_aged` | 137,110,86 | CC0 Poly Haven scan bamboo_wall (aged dried bamboo), whole map | i07 basket (orange spotlight, no grey card), k28 (hand-tinted), k06 (print). **No kori photo exists locally**: proxy, flagged |
| `firewood_split` | 108,92,60 | i22 split pieces 98,74,42; mixed sticks 88,77,54; round log bark 137,126,84 (kamado body in the same light 51,53,55 = neutral, no WB) | - |
| `firewood_end` | 160,130,67 | i22 six small boxes inside six cut log ends (131-170) | - |
| heri cha -> existing `cha_koge` | 106,77,50 | reference (ja.wikipedia koge-cha #6A4D32), already in the palette | i03 Tenmyo heri = dark indigo/black (not brown); i12 Tsubaki honjin heri under orange light (a WB on the tatami turned it purple: unreliable); i07 (orange light) |

## Text (items 5 and 7)
Local research has no kaimyo source beyond W2_ERA G5/G6 (one person per stone, kaimyo + death date; -shinji /
-shinnyo; Shin-sect shaku- / shakuni-; era + cyclical year). The rest is **(knowledge)**, no web request made:
- **信士 shinji / 信女 shinnyo**: the ordinary rank of adult lay commoners on Edo stones; a 2-character name + rank.
- **禅定門 zenjomon / 禅定尼 zenjoni**: lay men / women who had taken precepts; common on 17th-c. stones and still
  found into the early 18th c. -> used on the OLDER stones (Kanbun 10, Enpo 6, Shotoku 1) and one Kyoho 9 post.
- **童子 doji / 童女 donyo**: children (roughly 5 to 15); infants (孩子 / 嬰子) not used (less sure of the age bands).
- **釈 shaku-** (no rank title): Jodo Shinshu men (釈尼 for women, already in B1's atlas).
- **帰元 kigen / 円寂 enjaku**: Zen prefixes ("returned to the source", "perfect rest") carved above the name on
  many Edo stones; used on two.
- Names: generic two-character dharma names built from the stock characters (浄 心 妙 貞 宗 円 寿 春 光 秋 月 了 善
  智 清 道 覚 照 法 山 念 岳 仙); no stone copied.
- Layout: era year (+ cyclical sign) in the right column, kaimyo centre and larger, month and day left; columns
  read right to left; a couple stone puts the husband right, the wife left.
- Every era / year / sign checked by arithmetic (1684 = 甲子): 寛文十年庚戌 1670, 延宝六年戊午 1678, 元禄八年乙亥 1695,
  元禄十一年戊寅 1698, 宝永四年丁亥 1707, 正徳元年辛卯 1711 (Shotoku from 4th month 1711: 十二月 ok), 正徳三年癸巳 1713,
  享保五年庚子 1720, 享保七年壬寅 1722, 享保八年癸卯 1723, 享保九年甲辰 1724, 享保十年乙巳 1725, 享保十二年丁未 1727,
  享保十三年戊申 1728, 享保十四年己酉 1729, 享保十五年庚戌 1730. Nothing after 1730. Days: 朔日 (1st), 廿 (20).
- Font: Yuji Syuku (OFL), all 60-odd characters present in its cmap (checked).

## Incident (my mistake, repaired)
At 21:44 I ran `python buildings/pipeline.py --help` to read its usage; the script has no --help and started a full
rebuild of every shipped building. Stopped after ~2 min, before combine / binarize / pack (jp_buildings.pbo untouched,
21:29). It had staged 69 townhouse MLODs into `src/JP/buildings/townhouse/` over the committed ODOLs: restored all 69
to HEAD (`git checkout --`, header check: 69/69 ODOL). Records it rewrote are byte-identical (no git change). The
other ODOL / checks changes in the tree at that time are S1's `rerun_all.py` verify run (its own processes), not
touched.

## Checkpoint 2 (done)
**Materials** (`research/materials/make_m1_materials.py`, C1 27/27 pass + 3 WARN on the ink atlas like B1's sumi;
jp_common repacked): jp_m_ground_earth_bare, jp_m_wood_new, jp_m_wood_silver, jp_m_floor_tatami_heri_cha,
jp_m_decal_carved_text_grave, jp_m_decal_sumi_text_grave, jp_m_wicker_aged, jp_m_wood_firewood,
jp_m_wood_endgrain_firewood. No existing material or palette entry changed (6 entries added).

**Props now using them**
- jp_s_grave_stones (spikes/B3b/props_grave.py `KAIMYO`): board, board_s, board_tall_moss, ab_leaning, boat_halo,
  boat_halo_child (now carries the child's name), ab_boat_halo_sunk, round, ab_round_lean, pillar, pillar_pointed ->
  their own kaimyo cell each (ab_board_broken keeps B1's woman); field_mound -> bare earth. Gorinto / hokyointo blank.
- jp_s_grave_wood: bohyo (silver, ink name 1727), bohyo_new (NEW wood, crisp ink, 1730), bohyo_s (silver, a child's
  name, faded), bohyo_roof (silver _w0, 1728), ab_bohyo_lean (silver _w2, ghost 1724); every mound -> bare earth.
  Name on the front face, era year on the right side face (as the pillar stones). Sotoba unchanged.
- jp_s_firewood_stack (6) and jp_f_firewood (4): sides jp_m_wood_firewood, ends jp_m_wood_endgrain_firewood (posts
  and cap boards of the free stack stay wood_weathered).
- jp_f_kori (3): jp_m_wicker_aged (bamboo_weave unchanged for every other prop).
- Floors: `jpparts.floors.MATS_TATAMI_CHA`; rural.py: Kanto `dei` and Kinai `zashiki` (the T2 farmhouse best rooms)
  -> cha heri. 8 farmhouse shells + f_farmhouse_kanto / _kinai rebuilt. Machiya, inns, townhouses keep black.
- Unused but available: kaimyo_shugetsu_donyo_shotoku3, kaimyo_couple_dosei_myosei (needs a stone >= 0.34 m wide),
  bohyo_myoho_shinnyo_kyoho15.

**Checks re-run (all pass):** B3b 226/226 (check_b3b: pass/faces vs committed unchanged), TXT 94 files 0 failing,
C7 chain PASS, L2 81/81 (jp_site 307 classes), B3a 113/113 (+ check_b3a 113), L1 185/185, S1 175/175 (jp_furniture
473 classes), farmhouses 8 + furnished 2 verify pass, machiya 78/78, furnished machiya 137/137, f_th_kamigata_3k
_middle_komeya 103/103, f_hut_east_l_board 61/61.
**Housekeeping:** 381 noise files (ODOL byte noise and check re-run JSONs, incl. the 21:46 building ODOLs) restored to
HEAD; jp_site / jp_furniture repacked from the restored tree.
**Sheets:** research/materials/contact_sheets/m1_1_materials.jpg (refs -> swatch, before, after x3),
m1_2_props.jpg (before / after renders, close-ups, heri mock-up), m1_3_text.jpg (both atlases + cell list).
**Not done:** bonji (needs Noto Sans Siddham, OFL); a kori / brown-heri photo for a true sample (both flagged as
proxy / reference); nothing tested in game.
