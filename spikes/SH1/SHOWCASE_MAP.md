# SH1 showcase map: ID -> class -> position

Resolve any ID Stephen names (TEST_CHECKLIST.md, the maps `research/production/contact_sheets/sh1_map_*.jpg`).
Positions are world metres (x east, z north), y_offset over the ground; yaw clockwise from north (180 = faces south).
Regenerate: `python spikes/SH1/layout_sh1.py` then `python spikes/SH1/showcase_map_md.py`.

## Street (map sh1_map_street.jpg)

| ID | What | x | z |
|---|---|---|---|
| D1 | ironmonger (S1 demo, replaced the bare Edo board-roof unit) `Land_JP_Townhouse_Edo_3ken_Middle_ToriL_Kanamono` | 1046.1 | 1087.6 |
| D2 | tobacco (S1 demo, inserted) `Land_JP_Townhouse_Kamigata_2ken_Middle_ToriR_Tabako` | 989.2 | 1087.6 |
| D3 | sweets / rice cakes (S1 demo, replaced the bare Kamigata corner unit) `Land_JP_Townhouse_Kamigata_3ken_EndR_ToriL_Mochiya` | 1003.2 | 1087.6 |
| D4 | apothecary (S1 demo, replaced the bare Edo 2-ken end unit) `Land_JP_Townhouse_Edo_3ken_EndL_ToriL_Kusuri` | 1040.6 | 1087.6 |
| D5 | tailor (S1 demo, inserted) `Land_JP_Townhouse_Edo_2ken_Middle_ToriR_Board_Shitate` | 1050.8 | 1087.6 |
| D6 | dolls (S1 demo, inserted) `Land_JP_Townhouse_Kamigata_3ken_Middle_ToriL_Kyo_Ningyo` | 984.6 | 1087.6 |
| C-a | rice dealer (C3) | 997.7 | 1087.6 |
| C-b | paper shop (C3) | 993.0 | 1087.6 |
| C-c | cloth dealer (C3) | 1054.6 | 1087.6 |
| C-d | sake shop, corner (C3) | 1059.2 | 1087.6 |
| C-e | bare Kamigata 3-ken end unit (moved to the new row end) | 979.0 | 1087.6 |
| C-f | post-town house (C3, furnished home) | 988.7 | 1072.4 |
| C-g | post-town row houses (bare) | 1000.0 | 1072.4 |
| C-h | ordinary inn (C3) | 1013.1 | 1071.5 |
| C-i | grand inn, two storeys (C3) | 1026.2 | 1071.5 |
| C-j | town kura (C3) | 1000.0 | 1097.5 |
| S01 | shrine: first stone torii | 1024.0 | 1099.5 |

## Shrine (map sh1_map_shrine.jpg; K = hill-stair modules, I = Inari-stair modules)

| ID | Class | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| S01 | `StaticObj_JP_S_Torii_Stone_L` | 1024.00 | 1099.50 | 180 | -0.00 | ichi-no-torii: large stone torii, plain (at the town end of the approach) |
| S02 | `StaticObj_JP_S_Nobori_Shrine` | 1018.80 | 1103.00 | 180 | 0.00 | shrine banners (festival leftovers), west |
| S03 | `StaticObj_JP_S_Nobori_Shrine` | 1029.20 | 1103.00 | 180 | 0.00 | shrine banners, east |
| S04 | `StaticObj_JP_S_Stone_Lantern_Kasuga_18` | 1021.00 | 1122.00 | 90 | 0.00 | Kasuga lantern 1.8 m, west of the pair |
| S05 | `StaticObj_JP_S_Stone_Lantern_Kasuga_18` | 1027.00 | 1122.00 | 270 | 0.00 | Kasuga lantern 1.8 m, east of the pair |
| S06 | `StaticObj_JP_S_Stele_Group3` | 1016.60 | 1125.00 | 90 | -0.01 | stele corner: three old stones on one base |
| S07 | `StaticObj_JP_S_Stele_Koshin` | 1017.20 | 1127.60 | 90 | -0.00 | stele corner: Koshin stone |
| S08 | `StaticObj_JP_S_Stele_Relief_Panel` | 1017.10 | 1129.20 | 90 | -0.00 | stele corner: relief panel |
| S09 | `StaticObj_JP_S_Stele_Arched` | 1017.00 | 1130.70 | 90 | -0.00 | stele corner: arched stele |
| S10 | `StaticObj_JP_S_Stele_Round` | 1015.60 | 1128.60 | 90 | -0.00 | stele corner: round-topped stone |
| S11 | `StaticObj_JP_S_Stele_Pillar` | 1015.40 | 1126.90 | 90 | -0.00 | stele corner: pillar stone (waymark) |
| S12 | `StaticObj_JP_S_Stele_Ab_Tipped` | 1015.00 | 1131.60 | 60 | -0.01 | stele corner: a stele tipped over |
| S13 | `StaticObj_JP_S_Stele_Natural_Slab` | 1015.10 | 1123.40 | 100 | -0.00 | stele corner: natural slab |
| S14 | `StaticObj_JP_S_Torii_Stone_L_Rope_Shide` | 1024.00 | 1136.50 | 180 | -0.01 | ni-no-torii: large stone torii with straw rope + paper streamers (the precinct boundary) |
| S15 | `StaticObj_JP_S_Chozubachi_Large` | 1019.00 | 1140.50 | 90 | -0.02 | the water basin (chozubachi), large, dry and leaf-filled |
| S16 | `StaticObj_JP_S_Stone_Lantern_Kasuga_24` | 1021.00 | 1143.50 | 90 | -0.02 | Kasuga 2.4 m, west |
| S17 | `StaticObj_JP_S_Stone_Lantern_Kasuga_24` | 1027.00 | 1143.50 | 270 | -0.02 | Kasuga 2.4 m, east |
| S18 | `StaticObj_JP_S_Stone_Lantern_Square_24` | 1021.00 | 1149.50 | 90 | -0.02 | square lantern 2.4 m, west |
| S19 | `StaticObj_JP_S_Stone_Lantern_Square_24` | 1027.00 | 1149.50 | 270 | -0.02 | square lantern 2.4 m, east |
| S20 | `StaticObj_JP_S_Stone_Lantern_Kasuga_24_Moss` | 1021.00 | 1155.50 | 90 | -0.03 | Kasuga 2.4 m mossy, west |
| S21 | `StaticObj_JP_S_Stone_Lantern_Kasuga_24_Moss` | 1027.00 | 1155.50 | 270 | -0.03 | Kasuga 2.4 m mossy, east |
| S22 | `StaticObj_JP_S_Torii_Wood_Myojin_Moss_Rope_Shide` | 1024.00 | 1161.00 | 180 | -0.01 | san-no-torii: wooden myojin, mossy, rope + streamers |
| S23 | `StaticObj_JP_S_Stone_Lantern_Square_24_Moss` | 1021.00 | 1166.00 | 90 | -0.03 | square lantern 2.4 m mossy, west |
| S24 | `StaticObj_JP_S_Stone_Lantern_Square_24_Moss` | 1027.00 | 1166.00 | 270 | -0.03 | square lantern 2.4 m mossy, east |
| S25 | `StaticObj_JP_S_Stone_Lantern_Kasuga_18_Moss` | 1021.00 | 1172.00 | 90 | -0.02 | Kasuga 1.8 m mossy, west |
| S26 | `StaticObj_JP_S_Stone_Lantern_Ab_Hoju_Moss` | 1027.00 | 1172.00 | 270 | -0.06 | Kasuga 1.8 m mossy, its top jewel fallen (abandoned), east |
| S27 | `StaticObj_JP_S_Stone_Lantern_Kasuga_30` | 1020.80 | 1178.00 | 90 | -0.03 | Kasuga 3.0 m, west |
| S28 | `StaticObj_JP_S_Stone_Lantern_Kasuga_30` | 1027.20 | 1178.00 | 270 | -0.03 | Kasuga 3.0 m, east |
| S29 | `StaticObj_JP_S_Stone_Lantern_Joyato` | 1019.00 | 1183.00 | 90 | -0.05 | joyato (always-lit lantern on a two-step base), west |
| S30 | `StaticObj_JP_S_Stone_Lantern_Joyato` | 1029.00 | 1183.00 | 270 | -0.05 | joyato, east |
| S31 | `StaticObj_JP_S_Stone_Lantern_Oki` | 1021.80 | 1184.60 | 90 | -0.03 | small placed lantern (oki) at the hall front, west |
| S32 | `StaticObj_JP_S_Stone_Lantern_Oki_Moss` | 1026.20 | 1184.60 | 270 | -0.03 | small placed lantern (oki), mossy, east |
| S33 | `dz\plants\tree\t_fagussylvatica_3f.p3d` | 1033.00 | 1198.00 | 0 | -0.06 | the sacred tree: a vanilla beech (placement only) |
| S34 | `StaticObj_JP_S_Shimenawa_Wrap_D06` | 1033.33 | 1198.12 | 0 | -0.06 | straw rope (shimenawa) with streamers round the sacred tree |
| S40 | `StaticObj_JP_S_Torii_Wood_Shinmei` | 1036.00 | 1145.00 | 270 | -0.05 | sub-shrine row 1: wooden shinmei torii, plain |
| S40h | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1038.20 | 1145.00 | 270 | -0.02 | behind it: jizo_hut_stone_roof (stand-in for a small shrine) |
| S41 | `StaticObj_JP_S_Torii_Wood_Shinmei_Rope` | 1036.25 | 1149.00 | 270 | -0.05 | sub-shrine row 2: wooden shinmei, straw rope |
| S41h | `StaticObj_JP_S_Stele_Natural_Slab` | 1037.85 | 1149.00 | 270 | -0.01 | behind it: stele_natural_slab (stand-in for a small shrine) |
| S42 | `StaticObj_JP_S_Torii_Wood_Shinmei_Rope_Shide` | 1035.80 | 1153.00 | 270 | -0.05 | sub-shrine row 3: wooden shinmei, rope + streamers |
| S42h | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1038.00 | 1153.00 | 270 | -0.03 | behind it: jizo_hut_stone_roof (stand-in for a small shrine) |
| S43 | `StaticObj_JP_S_Torii_Stone_S` | 1036.00 | 1157.00 | 270 | -0.06 | sub-shrine row 4: small stone torii, plain |
| S43h | `StaticObj_JP_S_Stele_Round` | 1037.60 | 1157.00 | 270 | -0.01 | behind it: stele_round (stand-in for a small shrine) |
| S44 | `StaticObj_JP_S_Torii_Stone_S_Rope` | 1036.25 | 1161.00 | 270 | -0.06 | sub-shrine row 5: small stone torii, rope |
| S44h | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1038.45 | 1161.00 | 270 | -0.03 | behind it: jizo_hut_stone_roof (stand-in for a small shrine) |
| S45 | `StaticObj_JP_S_Torii_Stone_S_Rope_Shide` | 1035.80 | 1165.00 | 270 | -0.06 | sub-shrine row 6: small stone torii, rope + streamers |
| S45h | `StaticObj_JP_S_Stele_Natural_Slab` | 1037.40 | 1165.00 | 270 | -0.01 | behind it: stele_natural_slab (stand-in for a small shrine) |
| S46 | `StaticObj_JP_S_Torii_Wood_Shinmei_Moss` | 1036.00 | 1169.00 | 270 | -0.05 | sub-shrine row 7: wooden shinmei, mossy |
| S46h | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1038.20 | 1169.00 | 270 | -0.02 | behind it: jizo_hut_stone_roof (stand-in for a small shrine) |
| S47 | `StaticObj_JP_S_Torii_Wood_Shinmei_Moss_Rope` | 1036.25 | 1173.00 | 270 | -0.05 | sub-shrine row 8: wooden shinmei, mossy, rope |
| S47h | `StaticObj_JP_S_Stele_Arched` | 1037.85 | 1173.00 | 270 | -0.01 | behind it: stele_arched (stand-in for a small shrine) |
| S48 | `StaticObj_JP_S_Torii_Wood_Shinmei_Moss_Rope_Shide` | 1035.80 | 1177.00 | 270 | -0.06 | sub-shrine row 9: wooden shinmei, mossy, rope + streamers |
| S48h | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1038.00 | 1177.00 | 270 | -0.03 | behind it: jizo_hut_stone_roof (stand-in for a small shrine) |
| S49 | `StaticObj_JP_S_Torii_Stone_S_Moss` | 1036.00 | 1181.00 | 270 | -0.08 | sub-shrine row 10: small stone torii, mossy |
| S49h | `StaticObj_JP_S_Stele_Natural_Slab` | 1037.60 | 1181.00 | 270 | -0.02 | behind it: stele_natural_slab (stand-in for a small shrine) |
| S50 | `StaticObj_JP_S_Torii_Stone_S_Moss_Rope_Shide` | 1036.25 | 1185.00 | 270 | -0.10 | sub-shrine row 11: small stone torii, mossy, rope + streamers |
| S50h | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1038.45 | 1185.00 | 270 | -0.05 | behind it: jizo_hut_stone_roof (stand-in for a small shrine) |
| S51 | `StaticObj_JP_S_Torii_Wood_Ab_Rotted` | 1035.80 | 1189.00 | 270 | -0.12 | sub-shrine row 12: a rotted wooden torii (abandoned sub-shrine) |
| S51h | `StaticObj_JP_S_Jizo_Hut_Ab_Open` | 1038.00 | 1189.00 | 270 | -0.09 | behind it: jizo_hut_ab_open (stand-in for a small shrine) |
| S52 | `StaticObj_JP_S_Torii_Wood_Mini` | 1037.15 | 1145.00 | 270 | -0.02 | mini torii (yard shrine), plain, before row 1's hut |
| S53 | `StaticObj_JP_S_Torii_Wood_Mini_Rope` | 1036.65 | 1161.00 | 270 | -0.02 | mini torii, rope, before row 5's hut |
| S90 | `StaticObj_JP_S_Stone_Lantern_Kasuga_30_Moss` | 1030.82 | 1206.10 | 116 | -0.17 | path to the hill stair: Kasuga 3.0 m mossy / its twin toppled (abandoned) (west) |
| S91 | `StaticObj_JP_S_Stone_Lantern_Ab_Toppled` | 1036.04 | 1203.56 | 331 | -0.33 | path to the hill stair: Kasuga 3.0 m mossy / its twin toppled (abandoned) (east) |
| S92 | `StaticObj_JP_S_Stone_Lantern_Kasuga_18_Moss` | 1034.34 | 1213.30 | 116 | -0.16 | path to the hill stair: Kasuga 1.8 m mossy pair (west) |
| S93 | `StaticObj_JP_S_Stone_Lantern_Kasuga_18_Moss` | 1038.66 | 1211.20 | 296 | -0.14 | path to the hill stair: Kasuga 1.8 m mossy pair (east) |
| S94 | `StaticObj_JP_S_Stone_Lantern_Square_24_Moss` | 1037.64 | 1220.05 | 116 | -0.21 | path to the hill stair: square 2.4 m mossy pair (west) |
| S95 | `StaticObj_JP_S_Stone_Lantern_Square_24_Moss` | 1041.96 | 1217.95 | 296 | -0.21 | path to the hill stair: square 2.4 m mossy pair (east) |
| S62 | `StaticObj_JP_S_Torii_Wood_Ab_Leaning` | 1047.00 | 1205.50 | 195 | -0.32 | an old wooden torii leaning in the trees (abandoned) |
| S63 | `StaticObj_JP_S_Torii_Stone_L_Rope_Shide` | 1042.00 | 1226.00 | 180 | -0.12 | large stone torii, rope + streamers, at the foot of the hill stair (FB1: was medium, too low) |
| K01 | `StaticObj_JP_S_Stone_Steps_Dressed_3_Wide` | 1042.00 | 1227.60 | 180 | -0.08 | hill stair flight dressed_3_wide (0.91 m run) |
| K01E | `StaticObj_JP_S_Stone_Steps_Cheek_3` | 1043.46 | 1227.60 | 180 | -0.08 | hill stair cheek wall beside that flight |
| K01W | `StaticObj_JP_S_Stone_Steps_Cheek_3` | 1040.54 | 1227.60 | 180 | -0.08 | hill stair cheek wall beside that flight |
| K02 | `StaticObj_JP_S_Stone_Steps_Landing_Wide` | 1042.00 | 1228.51 | 180 | 0.15 | hill stair landing landing_wide (visible 0.80 m) |
| K03 | `StaticObj_JP_S_Stone_Steps_Dressed_3_Wide` | 1042.00 | 1229.31 | 180 | -0.08 | hill stair flight dressed_3_wide (0.91 m run) |
| K03E | `StaticObj_JP_S_Stone_Steps_Cheek_3` | 1043.46 | 1229.31 | 180 | -0.08 | hill stair cheek wall beside that flight |
| K03W | `StaticObj_JP_S_Stone_Steps_Cheek_3` | 1040.54 | 1229.31 | 180 | -0.08 | hill stair cheek wall beside that flight |
| K04 | `StaticObj_JP_S_Stone_Steps_Landing_Wide` | 1042.00 | 1230.22 | 180 | 0.14 | hill stair landing landing_wide (visible 0.80 m) |
| K05 | `StaticObj_JP_S_Stone_Steps_Rough_3` | 1042.00 | 1231.02 | 180 | -0.08 | hill stair flight rough_3 (0.91 m run) |
| K06 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1231.93 | 180 | 0.14 | hill stair landing landing (visible 0.70 m) |
| K07 | `StaticObj_JP_S_Stone_Steps_Dressed_3` | 1042.00 | 1232.63 | 180 | -0.07 | hill stair flight dressed_3 (0.91 m run) |
| K08 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1233.54 | 180 | 0.14 | hill stair landing landing (visible 0.65 m) |
| K09 | `StaticObj_JP_S_Stone_Steps_Rough_3` | 1042.00 | 1234.19 | 180 | -0.06 | hill stair flight rough_3 (0.91 m run) |
| K10 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1235.10 | 180 | 0.15 | hill stair landing landing (visible 0.70 m) |
| K11 | `StaticObj_JP_S_Stone_Steps_Dressed_3` | 1042.00 | 1235.80 | 180 | -0.06 | hill stair flight dressed_3 (0.91 m run) |
| K12 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1236.71 | 180 | 0.14 | hill stair landing landing (visible 0.55 m) |
| K13 | `StaticObj_JP_S_Stone_Steps_Rough_3` | 1042.00 | 1237.26 | 180 | -0.04 | hill stair flight rough_3 (0.91 m run) |
| K14 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1238.17 | 180 | 0.16 | hill stair landing landing (visible 0.65 m) |
| K15 | `StaticObj_JP_S_Stone_Steps_Dressed_3` | 1042.00 | 1238.82 | 180 | -0.05 | hill stair flight dressed_3 (0.91 m run) |
| K16 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1239.73 | 180 | 0.14 | hill stair landing landing (visible 0.50 m) |
| K17 | `StaticObj_JP_S_Stone_Steps_Rough_3` | 1042.00 | 1240.23 | 180 | -0.02 | hill stair flight rough_3 (0.91 m run) |
| K18 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1241.14 | 180 | 0.15 | hill stair landing landing (visible 0.55 m) |
| K19 | `StaticObj_JP_S_Stone_Steps_Dressed_3` | 1042.00 | 1241.69 | 180 | -0.03 | hill stair flight dressed_3 (0.91 m run) |
| K20 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1242.60 | 180 | 0.14 | hill stair landing landing (visible 0.50 m) |
| K21 | `StaticObj_JP_S_Stone_Steps_Rough_3` | 1042.00 | 1243.10 | 180 | -0.03 | hill stair flight rough_3 (0.91 m run) |
| K22 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1244.01 | 180 | 0.15 | hill stair landing landing (visible 0.45 m) |
| K23 | `StaticObj_JP_S_Stone_Steps_Dressed_3` | 1042.00 | 1244.46 | 180 | -0.01 | hill stair flight dressed_3 (0.91 m run) |
| K24 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1245.37 | 180 | 0.14 | hill stair landing landing (visible 0.45 m) |
| K25 | `StaticObj_JP_S_Stone_Steps_Rough_3` | 1042.00 | 1245.82 | 180 | -0.01 | hill stair flight rough_3 (0.91 m run) |
| K26 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1246.73 | 180 | 0.14 | hill stair landing landing (visible 0.40 m) |
| K27 | `StaticObj_JP_S_Stone_Steps_Ab_Heaved_Rough` | 1042.00 | 1247.13 | 180 | 0.00 | hill stair flight ab_heaved_rough (0.91 m run) |
| K28 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1248.04 | 180 | 0.16 | hill stair landing landing (visible 0.40 m) |
| K29 | `StaticObj_JP_S_Stone_Steps_Rough_3` | 1042.00 | 1248.44 | 180 | 0.01 | hill stair flight rough_3 (0.91 m run) |
| K30 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1249.35 | 180 | 0.15 | hill stair landing landing (visible 0.40 m) |
| K31 | `StaticObj_JP_S_Stone_Steps_Dressed_3` | 1042.00 | 1249.75 | 180 | 0.00 | hill stair flight dressed_3 (0.91 m run) |
| K32 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1250.66 | 180 | 0.15 | hill stair landing landing (visible 0.60 m) |
| K33 | `StaticObj_JP_S_Stone_Steps_Ab_Heaved` | 1042.00 | 1251.26 | 180 | -0.08 | hill stair flight ab_heaved (1.82 m run) |
| K34 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1253.08 | 180 | 0.19 | hill stair landing landing (visible 0.40 m) |
| K35 | `StaticObj_JP_S_Stone_Steps_Ab_Heaved_Rough` | 1042.00 | 1253.48 | 180 | 0.03 | hill stair flight ab_heaved_rough (0.91 m run) |
| K36 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1254.39 | 180 | 0.16 | hill stair landing landing (visible 0.55 m) |
| K37 | `StaticObj_JP_S_Stone_Steps_Ab_Heaved` | 1042.00 | 1254.94 | 180 | -0.06 | hill stair flight ab_heaved (1.82 m run) |
| K38 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1256.76 | 180 | 0.19 | hill stair landing landing (visible 0.40 m) |
| K39 | `StaticObj_JP_S_Stone_Steps_Dressed_3` | 1042.00 | 1257.16 | 180 | 0.03 | hill stair flight dressed_3 (0.91 m run) |
| K40 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1258.07 | 180 | 0.15 | hill stair landing landing (visible 0.50 m) |
| K41 | `StaticObj_JP_S_Stone_Steps_Dressed_6` | 1042.00 | 1258.57 | 180 | -0.05 | hill stair flight dressed_6 (1.82 m run) |
| K41E | `StaticObj_JP_S_Stone_Steps_Cheek_6` | 1043.01 | 1258.57 | 180 | -0.05 | hill stair cheek wall beside that flight |
| K41W | `StaticObj_JP_S_Stone_Steps_Cheek_6` | 1040.99 | 1258.57 | 180 | -0.05 | hill stair cheek wall beside that flight |
| K42 | `StaticObj_JP_S_Stone_Steps_Landing` | 1042.00 | 1260.39 | 180 | 0.18 | hill stair landing landing (visible 0.55 m) |
| K43 | `StaticObj_JP_S_Stone_Steps_Dressed_6_Wide` | 1042.00 | 1260.94 | 180 | -0.05 | hill stair flight dressed_6_wide (1.82 m run) |
| S64 | `StaticObj_JP_S_Torii_Wood_Myojin` | 1042.00 | 1233.84 | 180 | -0.08 | wooden myojin torii over the stair, plain |
| S65 | `StaticObj_JP_S_Torii_Wood_Myojin_Rope` | 1042.00 | 1238.47 | 180 | -0.09 | wooden myojin over the stair, rope |
| S66 | `StaticObj_JP_S_Torii_Wood_Myojin_Rope_Shide` | 1042.00 | 1244.23 | 180 | -0.10 | wooden myojin over the stair, rope + streamers |
| S67 | `StaticObj_JP_S_Torii_Wood_Myojin_Moss` | 1042.00 | 1250.96 | 180 | -0.13 | wooden myojin over the stair, mossy |
| S68 | `StaticObj_JP_S_Torii_Wood_Myojin_Moss_Rope` | 1042.00 | 1254.66 | 180 | -0.15 | wooden myojin over the stair, mossy, rope |
| S70 | `StaticObj_JP_S_Torii_Stone_L` | 1042.00 | 1263.96 | 180 | -0.28 | large stone torii, plain, at the head of the stair (oku-miya; FB1: was medium, too low) |
| S71 | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1042.00 | 1266.96 | 180 | -0.20 | oku-miya: a stone-roofed hut (stand-in for the upper shrine) |
| S72 | `StaticObj_JP_S_Stone_Lantern_Oki_Moss` | 1040.40 | 1265.56 | 180 | -0.18 | oku-miya oki lantern, mossy, west |
| S73 | `StaticObj_JP_S_Stone_Lantern_Oki_Moss` | 1043.60 | 1265.56 | 180 | -0.17 | oku-miya oki lantern, mossy, east |
| S74 | `StaticObj_JP_S_Chozubachi_Natural` | 1045.10 | 1263.36 | 180 | -0.18 | a natural-stone basin at the oku-miya |
| S80 | `StaticObj_JP_S_Torii_Wood_Myojin_Shu_Rope_Shide` | 1058.00 | 1226.10 | 180 | -0.08 | Inari: vermilion myojin torii, rope + streamers, at the foot of the narrow stair |
| I01 | `StaticObj_JP_S_Stone_Steps_Rough_3_Narrow` | 1058.00 | 1227.30 | 180 | -0.08 | Inari stair flight rough_3_narrow (0.91 m run) |
| I02 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1228.21 | 180 | 0.16 | Inari stair landing landing (visible 0.90 m) |
| I03 | `StaticObj_JP_S_Stone_Steps_Dressed_3_Narrow` | 1058.00 | 1229.11 | 180 | -0.09 | Inari stair flight dressed_3_narrow (0.91 m run) |
| I04 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1230.02 | 180 | 0.14 | Inari stair landing landing (visible 0.75 m) |
| I05 | `StaticObj_JP_S_Stone_Steps_Rough_3_Narrow` | 1058.00 | 1230.77 | 180 | -0.07 | Inari stair flight rough_3_narrow (0.91 m run) |
| I06 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1231.68 | 180 | 0.16 | Inari stair landing landing (visible 0.80 m) |
| I07 | `StaticObj_JP_S_Stone_Steps_Dressed_3_Narrow` | 1058.00 | 1232.48 | 180 | -0.07 | Inari stair flight dressed_3_narrow (0.91 m run) |
| I08 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1233.39 | 180 | 0.14 | Inari stair landing landing (visible 0.65 m) |
| I09 | `StaticObj_JP_S_Stone_Steps_Rough_3_Narrow` | 1058.00 | 1234.04 | 180 | -0.06 | Inari stair flight rough_3_narrow (0.91 m run) |
| I10 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1234.95 | 180 | 0.15 | Inari stair landing landing (visible 0.70 m) |
| I11 | `StaticObj_JP_S_Stone_Steps_Dressed_3_Narrow` | 1058.00 | 1235.65 | 180 | -0.05 | Inari stair flight dressed_3_narrow (0.91 m run) |
| I12 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1236.56 | 180 | 0.15 | Inari stair landing landing (visible 0.65 m) |
| I13 | `StaticObj_JP_S_Stone_Steps_Rough_3_Narrow` | 1058.00 | 1237.21 | 180 | -0.05 | Inari stair flight rough_3_narrow (0.91 m run) |
| I14 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1238.12 | 180 | 0.15 | Inari stair landing landing (visible 0.65 m) |
| I15 | `StaticObj_JP_S_Stone_Steps_Dressed_3_Narrow` | 1058.00 | 1238.77 | 180 | -0.06 | Inari stair flight dressed_3_narrow (0.91 m run) |
| I16 | `StaticObj_JP_S_Stone_Steps_Landing` | 1058.00 | 1239.68 | 180 | 0.14 | Inari stair landing landing (visible 0.55 m) |
| S81 | `StaticObj_JP_S_Torii_Wood_Myojin_Shu` | 1058.00 | 1235.20 | 180 | -0.10 | Inari: vermilion myojin torii, plain, over the stair |
| S82 | `StaticObj_JP_S_Torii_Wood_Ab_Leaning_Shu` | 1062.50 | 1213.00 | 165 | -0.39 | Inari: a vermilion torii leaning at the foot of the Inari path (abandoned) |
| S83 | `StaticObj_JP_S_Torii_Wood_Mini_Shu` | 1058.00 | 1241.23 | 180 | -0.03 | Inari: mini vermilion torii before the shrine |
| S84 | `StaticObj_JP_S_Jizo_Hut_Stone_Roof` | 1058.00 | 1242.43 | 180 | -0.15 | Inari: stone-roofed hut (stand-in for the Inari shrine) |
| S85 | `StaticObj_JP_S_Chozubachi_Ab_Dry` | 1055.60 | 1239.63 | 180 | -0.30 | Inari: a basin cracked and dry (abandoned) |
| S100 | `StaticObj_JP_S_Torii_Fallen_Stone_Quake` | 1052.00 | 1172.00 | 270 | -0.12 | collapsed stone torii (the 1707 quake), behind the sub-shrine row |
| S101 | `StaticObj_JP_S_Torii_Fallen_Stone_Quake_Old` | 1003.00 | 1150.00 | 180 | -0.14 | collapsed stone torii, mossy and sunk (a long-ago collapse), north of the graveyard |
| S102 | `StaticObj_JP_S_Torii_Fallen_Myojin_Typhoon` | 1008.00 | 1178.00 | 135 | -0.21 | wooden myojin torii blown over by a typhoon, west of the approach |
| S103 | `StaticObj_JP_S_Torii_Fallen_Shinmei_Rot` | 1056.00 | 1188.00 | 200 | -0.29 | wooden shinmei torii fallen with its feet rotted, in the trees east of the hall site |
| S104 | `StaticObj_JP_S_Torii_Fallen_Shu_Snapped` | 1066.00 | 1190.00 | 170 | -0.28 | Inari: a vermilion torii snapped at the posts, below the Inari path |

## Graveyard (map sh1_map_graveyard.jpg; G<row>-<col>, row 1 = south / front, col 1 = west; s/t/i = slats / flower tubes / incense of that grave)

| ID | Class | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| G1-01 | `StaticObj_JP_S_Grave_Wood_Bohyo_New` | 990.94 | 1109.37 | 180 | 0.00 | new wooden grave post, fresh ink, high mound |
| G1-02 | `StaticObj_JP_S_Grave_Wood_Bohyo` | 992.12 | 1109.20 | 185 | 0.00 | wooden grave post (bohyo) on an earth mound, silver-grey |
| G1-04 | `StaticObj_JP_S_Grave_Stones_Field_Mound` | 994.35 | 1109.37 | 186 | -0.00 | earth mound with a field stone |
| G1-05 | `StaticObj_JP_S_Grave_Wood_Bohyo_S` | 995.52 | 1109.36 | 171 | -0.00 | short wooden grave post |
| G1-06 | `StaticObj_JP_S_Grave_Stones_Round_S_Plain` | 996.88 | 1109.83 | 170 | -0.00 | small round-headed slab, plain |
| G1-07 | `StaticObj_JP_S_Grave_Wood_Ab_Bohyo_Rotted` | 998.01 | 1109.19 | 174 | 0.00 | grave post rotted to a stump, the mound sunk (abandoned) |
| G1-08 | `StaticObj_JP_S_Grave_Stones_Round` | 999.00 | 1109.86 | 190 | -0.00 | round-headed slab (kushigata, newer) |
| G1-08s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 998.95 | 1110.16 | 186 | 0.00 | memorial slats (sotoba) behind G1-08 |
| G1-09 | `StaticObj_JP_S_Grave_Stones_Round` | 1001.49 | 1109.85 | 180 | 0.00 | round-headed slab (kushigata, newer) |
| G1-10 | `StaticObj_JP_S_Grave_Stones_Boat_Halo_Child` | 1002.53 | 1109.93 | 183 | -0.00 | small boat-halo stone (a child's) |
| G1-10t | `StaticObj_JP_S_Grave_Wood_Tubes` | 1002.53 | 1109.61 | 180 | -0.00 | bamboo flower tubes before G1-10 |
| G1-12 | `StaticObj_JP_S_Grave_Stones_Round` | 1004.87 | 1109.87 | 170 | -0.00 | round-headed slab (kushigata, newer) |
| G1-12s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1004.93 | 1110.17 | 177 | -0.00 | memorial slats (sotoba) behind G1-12 |
| G1-13 | `StaticObj_JP_S_Grave_Wood_Bohyo_Roof` | 1006.15 | 1109.33 | 188 | -0.00 | wooden grave post with a little gabled roof (uncommon) |
| G1-14 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1007.04 | 1109.95 | 177 | -0.00 | boat-halo figure stone (funagata) |
| G1-15 | `StaticObj_JP_S_Grave_Stones_Round_S_Plain` | 1008.44 | 1109.97 | 172 | -0.00 | small round-headed slab, plain |
| G2-01 | `StaticObj_JP_S_Grave_Stones_Field` | 990.96 | 1112.61 | 192 | 0.00 | plain field stone (a poor grave) |
| G2-02 | `StaticObj_JP_S_Grave_Stones_Field_Pair` | 992.19 | 1112.72 | 182 | 0.00 | two field stones |
| G2-03 | `StaticObj_JP_S_Grave_Wood_Bohyo_S` | 993.44 | 1112.06 | 176 | -0.00 | short wooden grave post |
| G2-04 | `StaticObj_JP_S_Grave_Wood_Ab_Bohyo_Lean` | 994.58 | 1111.97 | 176 | 0.00 | grave post leaning (abandoned) |
| G2-06 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 996.87 | 1112.59 | 190 | -0.00 | boat-halo figure stone (funagata) |
| G2-07 | `StaticObj_JP_S_Grave_Stones_Field_Mound` | 998.00 | 1112.00 | 184 | -0.00 | earth mound with a field stone |
| G2-08 | `StaticObj_JP_S_Grave_Stones_Board` | 999.13 | 1112.72 | 179 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G2-08t | `StaticObj_JP_S_Grave_Wood_Tubes` | 999.13 | 1112.39 | 180 | 0.00 | bamboo flower tubes before G2-08 |
| G2-09 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1001.50 | 1112.56 | 173 | -0.00 | boat-halo figure stone (funagata) |
| G2-10 | `StaticObj_JP_S_Grave_Stones_Round` | 1002.56 | 1112.61 | 175 | -0.00 | round-headed slab (kushigata, newer) |
| G2-10s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1002.60 | 1112.91 | 173 | 0.00 | memorial slats (sotoba) behind G2-10 |
| G2-11 | `StaticObj_JP_S_Grave_Stones_Ab_Round_Lean` | 1003.84 | 1112.57 | 185 | 0.00 | round-headed slab leaning (abandoned) |
| G2-12 | `StaticObj_JP_S_Grave_Stones_Board_S` | 1004.77 | 1112.72 | 181 | -0.00 | small board stone |
| G2-12t | `StaticObj_JP_S_Grave_Wood_Tubes` | 1004.77 | 1112.39 | 180 | -0.00 | bamboo flower tubes before G2-12 |
| G2-12i | `StaticObj_JP_S_Grave_Wood_Incense` | 1004.79 | 1112.10 | 180 | -0.00 | stone incense stand before G2-12 |
| G2-13 | `StaticObj_JP_S_Grave_Wood_Bohyo` | 1006.09 | 1111.92 | 185 | 0.00 | wooden grave post (bohyo) on an earth mound, silver-grey |
| G2-15 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1008.19 | 1112.66 | 182 | -0.00 | boat-halo figure stone (funagata) |
| G2-15s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1008.22 | 1112.96 | 182 | -0.00 | memorial slats (sotoba) behind G2-15 |
| G2-15t | `StaticObj_JP_S_Grave_Wood_Tubes` | 1008.19 | 1112.34 | 180 | -0.00 | bamboo flower tubes before G2-15 |
| G2-15i | `StaticObj_JP_S_Grave_Wood_Incense` | 1008.21 | 1112.05 | 180 | -0.00 | stone incense stand before G2-15 |
| G2-16 | `StaticObj_JP_S_Grave_Stones_Jizo_Child` | 1009.60 | 1112.61 | 180 | -0.00 | child's Jizo with a bib |
| G3-01 | `StaticObj_JP_S_Grave_Stones_Field` | 991.07 | 1115.10 | 185 | 0.00 | plain field stone (a poor grave) |
| G3-03 | `StaticObj_JP_S_Grave_Stones_Board` | 993.17 | 1115.10 | 169 | 0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G3-04 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 994.37 | 1115.15 | 190 | -0.00 | boat-halo figure stone (funagata) |
| G3-04s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 994.42 | 1115.45 | 180 | 0.00 | memorial slats (sotoba) behind G3-04 |
| G3-05 | `StaticObj_JP_S_Grave_Stones_Board_S` | 995.64 | 1115.18 | 174 | 0.00 | small board stone |
| G3-06 | `StaticObj_JP_S_Grave_Wood_Bohyo` | 996.63 | 1114.51 | 184 | -0.00 | wooden grave post (bohyo) on an earth mound, silver-grey |
| G3-07 | `StaticObj_JP_S_Grave_Stones_Field_Pair` | 997.85 | 1115.03 | 172 | -0.00 | two field stones |
| G3-08 | `StaticObj_JP_S_Grave_Wood_Ab_Bohyo_Split` | 998.92 | 1114.47 | 194 | -0.00 | grave post split and rotting black (abandoned) |
| G3-09 | `StaticObj_JP_S_Grave_Stones_Jizo_Child` | 1001.41 | 1115.05 | 179 | -0.00 | child's Jizo with a bib |
| G3-10 | `StaticObj_JP_S_Grave_Stones_Boat_Halo_Child` | 1002.41 | 1115.15 | 184 | -0.00 | small boat-halo stone (a child's) |
| G3-11 | `StaticObj_JP_S_Grave_Stones_Jizo_Child` | 1003.67 | 1115.12 | 189 | -0.00 | child's Jizo with a bib |
| G3-12 | `StaticObj_JP_S_Grave_Stones_Boat_Halo_Child` | 1004.76 | 1115.18 | 182 | -0.00 | small boat-halo stone (a child's) |
| G3-12s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1004.70 | 1115.48 | 180 | -0.00 | memorial slats (sotoba) behind G3-12 |
| G3-14 | `StaticObj_JP_S_Grave_Stones_Board` | 1007.23 | 1115.12 | 168 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G3-15 | `StaticObj_JP_S_Grave_Stones_Round_S_Plain` | 1008.19 | 1115.08 | 168 | -0.00 | small round-headed slab, plain |
| G3-16 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1009.32 | 1115.17 | 188 | -0.00 | boat-halo figure stone (funagata) |
| G3-16s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1009.30 | 1115.47 | 176 | -0.00 | memorial slats (sotoba) behind G3-16 |
| G4-01 | `StaticObj_JP_S_Grave_Stones_Board` | 991.08 | 1117.81 | 180 | 0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G4-02 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 992.27 | 1117.69 | 183 | -0.00 | boat-halo figure stone (funagata) |
| G4-03 | `StaticObj_JP_S_Grave_Stones_Ab_Leaning` | 993.34 | 1117.67 | 193 | 0.00 | board stone leaning (abandoned) |
| G4-04 | `StaticObj_JP_S_Grave_Stones_Board` | 994.45 | 1117.72 | 171 | 0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G4-04s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 994.51 | 1118.02 | 176 | 0.00 | memorial slats (sotoba) behind G4-04 |
| G4-04t | `StaticObj_JP_S_Grave_Wood_Tubes` | 994.45 | 1117.39 | 180 | -0.00 | bamboo flower tubes before G4-04 |
| G4-04i | `StaticObj_JP_S_Grave_Wood_Incense` | 994.47 | 1117.10 | 180 | -0.00 | stone incense stand before G4-04 |
| G4-06 | `StaticObj_JP_S_Grave_Stones_Field` | 996.78 | 1117.76 | 174 | -0.00 | plain field stone (a poor grave) |
| G4-07 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 997.85 | 1117.66 | 191 | 0.00 | boat-halo figure stone (funagata) |
| G4-08 | `StaticObj_JP_S_Grave_Stones_Board_S` | 998.95 | 1117.79 | 188 | -0.00 | small board stone |
| G4-08s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 998.92 | 1118.09 | 174 | -0.00 | memorial slats (sotoba) behind G4-08 |
| G4-09 | `StaticObj_JP_S_Grave_Stones_Board` | 1001.44 | 1117.63 | 184 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G4-10 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1002.54 | 1117.81 | 187 | 0.00 | boat-halo figure stone (funagata) |
| G4-11 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1003.75 | 1117.63 | 189 | -0.00 | boat-halo figure stone (funagata) |
| G4-13 | `StaticObj_JP_S_Grave_Stones_Jizo_Child` | 1005.95 | 1117.68 | 173 | -0.00 | child's Jizo with a bib |
| G4-14 | `StaticObj_JP_S_Grave_Stones_Board_S` | 1007.13 | 1117.73 | 177 | 0.00 | small board stone |
| G4-15 | `StaticObj_JP_S_Grave_Stones_Ab_Boat_Halo_Sunk` | 1008.25 | 1117.78 | 162 | 0.00 | boat-halo stone sunk and tilted (abandoned) |
| G4-16 | `StaticObj_JP_S_Grave_Stones_Field_Mound` | 1009.50 | 1117.04 | 173 | -0.00 | earth mound with a field stone |
| G5-01 | `StaticObj_JP_S_Grave_Stones_Board_Tall_Moss` | 991.14 | 1120.37 | 178 | 0.00 | tall board stone, mossy |
| G5-02 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 992.30 | 1120.37 | 174 | 0.00 | boat-halo figure stone (funagata) |
| G5-02s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 992.30 | 1120.67 | 177 | -0.00 | memorial slats (sotoba) behind G5-02 |
| G5-02t | `StaticObj_JP_S_Grave_Wood_Tubes` | 992.30 | 1120.04 | 180 | 0.00 | bamboo flower tubes before G5-02 |
| G5-02i | `StaticObj_JP_S_Grave_Wood_Incense` | 992.32 | 1119.75 | 180 | -0.00 | stone incense stand before G5-02 |
| G5-03 | `StaticObj_JP_S_Grave_Stones_Board` | 993.29 | 1120.45 | 183 | 0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G5-03s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 993.32 | 1120.75 | 183 | -0.00 | memorial slats (sotoba) behind G5-03 |
| G5-04 | `StaticObj_JP_S_Grave_Stones_Pillar_Pointed` | 994.60 | 1120.47 | 178 | -0.00 | square pillar, pointed Kyoho top (rare) |
| G5-06 | `StaticObj_JP_S_Grave_Stones_Board` | 996.86 | 1120.41 | 190 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G5-07 | `StaticObj_JP_S_Grave_Wood_Ab_Bohyo_Rotted` | 997.83 | 1119.77 | 187 | -0.00 | grave post rotted to a stump, the mound sunk (abandoned) |
| G5-08 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 999.04 | 1120.41 | 189 | -0.00 | boat-halo figure stone (funagata) |
| G5-09 | `StaticObj_JP_S_Grave_Stones_Board` | 1001.36 | 1120.37 | 182 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G5-09s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1001.39 | 1120.67 | 174 | -0.00 | memorial slats (sotoba) behind G5-09 |
| G5-10 | `StaticObj_JP_S_Grave_Stones_Ab_Board_Broken` | 1002.58 | 1120.55 | 190 | -0.00 | board stone, top broken off (abandoned) |
| G5-11 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1003.59 | 1120.46 | 173 | 0.00 | boat-halo figure stone (funagata) |
| G5-11s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1003.61 | 1120.76 | 175 | -0.00 | memorial slats (sotoba) behind G5-11 |
| G5-12 | `StaticObj_JP_S_Grave_Stones_Field` | 1004.74 | 1120.37 | 185 | -0.00 | plain field stone (a poor grave) |
| G5-13 | `StaticObj_JP_S_Grave_Stones_Board` | 1006.15 | 1120.43 | 185 | 0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G5-15 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1008.29 | 1120.44 | 177 | -0.00 | boat-halo figure stone (funagata) |
| G5-15t | `StaticObj_JP_S_Grave_Wood_Tubes` | 1008.29 | 1120.11 | 180 | -0.00 | bamboo flower tubes before G5-15 |
| G5-15i | `StaticObj_JP_S_Grave_Wood_Incense` | 1008.31 | 1119.82 | 180 | -0.00 | stone incense stand before G5-15 |
| G5-16 | `StaticObj_JP_S_Grave_Stones_Board_S` | 1009.57 | 1120.41 | 192 | -0.00 | small board stone |
| G6-01 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 990.88 | 1123.04 | 192 | -0.00 | boat-halo figure stone (funagata) |
| G6-02 | `StaticObj_JP_S_Grave_Stones_Board` | 992.00 | 1123.06 | 175 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G6-03 | `StaticObj_JP_S_Grave_Stones_Gorinto_S` | 993.37 | 1123.00 | 191 | -0.00 | gorinto 0.6 m (five rings, Sanskrit seed syllables) |
| G6-05 | `StaticObj_JP_S_Grave_Stones_Board_Tall_Moss` | 995.52 | 1123.12 | 172 | -0.00 | tall board stone, mossy |
| G6-06 | `StaticObj_JP_S_Grave_Stones_Pillar` | 996.66 | 1123.12 | 186 | -0.00 | square pillar, flat top with a water hollow (rare) |
| G6-07 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 997.93 | 1123.05 | 172 | -0.00 | boat-halo figure stone (funagata) |
| G6-07s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 997.90 | 1123.35 | 186 | 0.00 | memorial slats (sotoba) behind G6-07 |
| G6-08 | `StaticObj_JP_S_Grave_Stones_Field_Pair` | 999.15 | 1123.16 | 190 | -0.00 | two field stones |
| G6-09 | `StaticObj_JP_S_Grave_Stones_Board_Tall_Moss` | 1001.47 | 1123.11 | 181 | -0.00 | tall board stone, mossy |
| G6-10 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1002.50 | 1122.97 | 186 | 0.00 | boat-halo figure stone (funagata) |
| G6-10s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1002.42 | 1123.27 | 179 | 0.00 | memorial slats (sotoba) behind G6-10 |
| G6-11 | `StaticObj_JP_S_Grave_Stones_Ab_Leaning` | 1003.70 | 1123.12 | 171 | -0.00 | board stone leaning (abandoned) |
| G6-12 | `StaticObj_JP_S_Grave_Stones_Board` | 1004.91 | 1123.07 | 185 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G6-12t | `StaticObj_JP_S_Grave_Wood_Tubes` | 1004.91 | 1122.73 | 180 | -0.00 | bamboo flower tubes before G6-12 |
| G6-12i | `StaticObj_JP_S_Grave_Wood_Incense` | 1004.93 | 1122.44 | 180 | -0.00 | stone incense stand before G6-12 |
| G6-14 | `StaticObj_JP_S_Grave_Stones_Gorinto_Stack` | 1007.10 | 1123.07 | 184 | -0.00 | gorinto re-stacked from mismatched rings |
| G6-15 | `StaticObj_JP_S_Grave_Stones_Ab_Boat_Halo_Sunk` | 1008.33 | 1123.11 | 175 | -0.00 | boat-halo stone sunk and tilted (abandoned) |
| G6-16 | `StaticObj_JP_S_Grave_Wood_Bohyo_S` | 1009.43 | 1122.44 | 186 | -0.00 | short wooden grave post |
| G7-01 | `StaticObj_JP_S_Grave_Stones_Gorinto_Heap` | 991.01 | 1125.67 | 179 | -0.00 | a small heap of old gorinto fragments |
| G7-03 | `StaticObj_JP_S_Grave_Stones_Gorinto_S` | 993.32 | 1125.71 | 188 | -0.00 | gorinto 0.6 m (five rings, Sanskrit seed syllables) |
| G7-04 | `StaticObj_JP_S_Grave_Stones_Board_Tall_Moss` | 994.47 | 1125.69 | 178 | -0.00 | tall board stone, mossy |
| G7-05 | `StaticObj_JP_S_Grave_Stones_Ab_Gorinto_Fallen` | 995.68 | 1125.68 | 173 | -0.00 | gorinto with its top rings fallen (abandoned) |
| G7-06 | `StaticObj_JP_S_Grave_Stones_Pillar` | 996.68 | 1125.70 | 176 | -0.00 | square pillar, flat top with a water hollow (rare) |
| G7-06t | `StaticObj_JP_S_Grave_Wood_Tubes` | 996.68 | 1125.24 | 180 | -0.00 | bamboo flower tubes before G7-06 |
| G7-07 | `StaticObj_JP_S_Grave_Stones_Hokyointo` | 997.98 | 1125.61 | 187 | -0.00 | hokyointo 1.5 m (four seed syllables on the body) |
| G7-09 | `StaticObj_JP_S_Grave_Stones_Board` | 1001.25 | 1125.63 | 181 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G7-10 | `StaticObj_JP_S_Grave_Stones_Gorinto_L` | 1003.17 | 1125.61 | 192 | -0.00 | gorinto 2.0 m on its platform (a samurai or priest's grave) |
| G7-12 | `StaticObj_JP_S_Grave_Stones_Ab_Hokyointo_Broken` | 1004.82 | 1125.68 | 166 | -0.01 | hokyointo, finial fallen (abandoned) |
| G7-13 | `StaticObj_JP_S_Grave_Stones_Boat_Halo` | 1005.99 | 1125.67 | 188 | -0.00 | boat-halo figure stone (funagata) |
| G7-13s | `StaticObj_JP_S_Grave_Wood_Sotoba_X3` | 1006.01 | 1125.97 | 180 | -0.00 | memorial slats (sotoba) behind G7-13 |
| G7-13t | `StaticObj_JP_S_Grave_Wood_Tubes` | 1005.99 | 1125.34 | 180 | -0.00 | bamboo flower tubes before G7-13 |
| G7-14 | `StaticObj_JP_S_Grave_Stones_Field` | 1007.11 | 1125.53 | 186 | -0.00 | plain field stone (a poor grave) |
| G7-16 | `StaticObj_JP_S_Grave_Stones_Board` | 1009.55 | 1125.69 | 168 | -0.00 | board-shaped stone (itabi), with a carved posthumous name |
| G7-16t | `StaticObj_JP_S_Grave_Wood_Tubes` | 1009.55 | 1125.36 | 180 | -0.00 | bamboo flower tubes before G7-16 |
| GW1 | `StaticObj_JP_S_Chozubachi_Small` | 1012.00 | 1112.00 | 90 | 0.00 | graveyard water point: small stone basin |
| GW2 | `StaticObj_JP_S_Grave_Wood_Bucket_Rack` | 1012.20 | 1109.90 | 90 | -0.00 | bucket-and-ladle rack by the water |
| GW3 | `StaticObj_JP_S_Grave_Wood_Rack` | 1011.90 | 1114.40 | 90 | -0.00 | rack of spare memorial slats |
| GJ1 | `StaticObj_JP_S_Stone_Jizo_M` | 1012.00 | 1117.00 | 90 | 0.00 | the six Jizo at the gate (roku-jizo), 1 of 6 |
| GJ2 | `StaticObj_JP_S_Stone_Jizo_Bib` | 1012.00 | 1117.72 | 90 | 0.00 | the six Jizo at the gate (roku-jizo), 2 of 6 |
| GJ3 | `StaticObj_JP_S_Stone_Jizo_M` | 1012.00 | 1118.44 | 90 | 0.00 | the six Jizo at the gate (roku-jizo), 3 of 6 |
| GJ4 | `StaticObj_JP_S_Stone_Jizo_Halo` | 1012.00 | 1119.16 | 90 | 0.00 | the six Jizo at the gate (roku-jizo), 4 of 6 |
| GJ5 | `StaticObj_JP_S_Stone_Jizo_Bib` | 1012.00 | 1119.88 | 90 | -0.00 | the six Jizo at the gate (roku-jizo), 5 of 6 |
| GJ6 | `StaticObj_JP_S_Stone_Jizo_M` | 1012.00 | 1120.60 | 90 | 0.00 | the six Jizo at the gate (roku-jizo), 6 of 6 |
| GJ7 | `StaticObj_JP_S_Stone_Jizo_Ab_Tipped` | 1013.20 | 1121.90 | 30 | -0.00 | a seventh Jizo knocked over (abandoned) |
| GF1 | `StaticObj_JP_S_Grave_Wood_Ab_Fallen` | 996.40 | 1113.90 | 30 | -0.00 | slats blown down into the aisle |
| GF2 | `StaticObj_JP_S_Grave_Wood_Ab_Fallen` | 1005.80 | 1119.00 | 200 | -0.00 | slats blown down into the aisle |
| GF3 | `StaticObj_JP_S_Grave_Wood_Ab_Fallen` | 993.00 | 1124.20 | 110 | -0.00 | slats blown down into the aisle |
| GL1 | `StaticObj_JP_S_Leaf_Pile_Ab_Scattered` | 1000.20 | 1121.00 | 0 | -0.00 | autumn leaf litter |
| GL2 | `StaticObj_JP_S_Leaf_Pile_Ab_Scattered` | 994.80 | 1126.70 | 70 | -0.01 | autumn leaf litter |
| GL3 | `StaticObj_JP_S_Leaf_Pile_Small` | 1000.30 | 1114.60 | 20 | 0.00 | autumn leaf litter |
| GL4 | `StaticObj_JP_S_Leaf_Pile_Small` | 1006.60 | 1124.10 | 150 | -0.00 | autumn leaf litter |
| GL5 | `StaticObj_JP_S_Leaf_Pile_Ab_Scattered` | 1004.80 | 1129.20 | 210 | -0.02 | autumn leaf litter |
| GL6 | `StaticObj_JP_S_Leaf_Pile_Small` | 990.00 | 1118.60 | 300 | -0.00 | autumn leaf litter |
| GT1 | `dz\plants\tree\t_quercusrobur_2f.p3d` | 987.30 | 1129.60 | 40 | -0.06 | an old oak over the back of the graveyard (vanilla tree, placement only) |

## Life-layer gallery (map sh1_map_gallery.jpg; L<n> = LIFE_LAYER.md item n; LS = shed, LH = host prop)

| ID | Class | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| LS1 | `Land_JP_Shed_Open_Board` | 1072.00 | 1036.00 | 180 | 0.00 | gallery shed 1 (Land_JP_Shed_Open_Board, bare: placed through the registry) |
| LS2 | `Land_JP_Shed_Open_Board` | 1080.00 | 1036.00 | 180 | 0.00 | gallery shed 2 (Land_JP_Shed_Open_Board, bare: placed through the registry) |
| LS3 | `Land_JP_Shed_Open_Board` | 1088.00 | 1036.00 | 180 | 0.00 | gallery shed 3 (Land_JP_Shed_Open_Board, bare: placed through the registry) |
| L1 | `StaticObj_JP_F_Mino_Pegs` | 1073.92 | 1037.76 | 180 | 0.05 | shed 1, back wall: Mino raincoat, kasa hat and tools on wall pegs |
| L5 | `StaticObj_JP_F_Tool_Wall` | 1072.54 | 1037.76 | 180 | 0.05 | shed 1, back wall: Tool wall: saw, adze, axe, hatchet on pegs |
| L4 | `StaticObj_JP_F_Utensil_Board` | 1071.33 | 1037.76 | 180 | 0.05 | shed 1, back wall: Kitchen utensil board: ladles, dipper, cutting board, knives on hooks |
| L6 | `StaticObj_JP_F_Rope_Pegs_2` | 1070.45 | 1037.76 | 180 | 0.05 | shed 1, back wall: Rope coils hung on pegs |
| L7 | `StaticObj_JP_F_Sandals_Hung_Wall` | 1069.73 | 1037.76 | 180 | 0.05 | shed 1, back wall: Straw sandals hung in bunches (new pairs for sale or spares) |
| L14 | `StaticObj_JP_F_Fire_Gear` | 1074.66 | 1036.60 | 270 | 0.05 | shed 1, east side wall: Fire buckets and a fire hook on the wall |
| L3 | `StaticObj_JP_F_Koyomi` | 1074.66 | 1035.15 | 270 | 0.05 | shed 1, east side wall, front: Printed calendar or almanac sheet on the wall |
| L47 | `StaticObj_JP_F_Yumi_Rack_Wall` | 1069.34 | 1036.55 | 90 | 0.05 | shed 1, west side wall: Bow and arrows on a rack |
| L11 | `StaticObj_JP_F_Bangasa_Hung` | 1069.34 | 1034.95 | 90 | 0.05 | shed 1, west side wall, front: Oiled-paper umbrella (bangasa), hung or leaning |
| L2 | `StaticObj_JP_F_Ofuda_Single` | 1072.91 | 1034.11 | 180 | 0.05 | shed 1, front face of the middle-east post: Paper charms (ofuda) pasted on a post, fresh and faded |
| L13 | `StaticObj_JP_F_Kaya_Draped` | 1073.82 | 1034.18 | 180 | 2.52 | shed 1, hanging from the front beam: Mosquito net (kaya), folded and hung up for autumn |
| L8 | `StaticObj_JP_F_Hoshigaki_3` | 1070.65 | 1034.18 | 180 | 2.52 | shed 1, hanging from the front beam: Autumn: dried persimmons (hoshigaki) on strings |
| L9 | `StaticObj_JP_F_Drying_Daikon` | 1069.85 | 1034.18 | 180 | 2.52 | shed 1, hanging from the front beam: Autumn: drying daikon, chillies and dried fish on strings |
| L12 | `StaticObj_JP_F_Noren_Inner_2` | 1072.00 | 1034.18 | 180 | 2.52 | shed 1, hanging in the middle bay of the front beam (as in a doorway): Inner noren curtain between the shop and the back rooms |
| L23 | `StaticObj_JP_F_Taru_Cask` | 1073.90 | 1036.75 | 180 | 0.05 | shed 1, floor: Casks: sake, soy and oil barrels on a low rack |
| L25 | `StaticObj_JP_F_Charcoal_Bale` | 1072.95 | 1036.80 | 180 | 0.05 | shed 1, floor: Charcoal bale and charcoal scuttle |
| L22 | `StaticObj_JP_F_Seiro_Kama2` | 1071.80 | 1036.70 | 180 | 0.05 | shed 1, floor: Steamer (seiro) stacked on a cauldron |
| L19 | `StaticObj_JP_F_Meal_Left_Zen` | 1070.65 | 1036.30 | 180 | 0.05 | shed 1, floor: Meal left behind: a tray with bowls, rice, pickles, a knocked-over cup |
| L27 | `StaticObj_JP_F_Enza` | 1071.80 | 1035.45 | 195 | 0.05 | shed 1, floor: Straw cushion (enza) and cotton cushion (zabuton, T3 only) |
| LH1 | `StaticObj_JP_F_Tana_182_3` | 1079.00 | 1037.76 | 180 | 0.05 | shed 2, shelf on the back wall, west half (host): jp_f_tana_182_3 |
| LH2 | `StaticObj_JP_F_Tana_182_3` | 1081.00 | 1037.76 | 180 | 0.05 | shed 2, shelf on the back wall, east half (host): jp_f_tana_182_3 |
| LH3 | `StaticObj_JP_F_Tana_136_1` | 1082.66 | 1036.55 | 270 | 0.05 | shed 2, shelf on the east side wall (host): jp_f_tana_136_1 |
| L16 | `StaticObj_JP_F_Butsu_Set_Full` | 1079.55 | 1037.61 | 180 | 1.35 | shed 2, LH1 upper shelf: Memorial tablets, incense burner, candle and flower vase set for the butsudan |
| L17 | `StaticObj_JP_F_Kamidana_Set_Offerings` | 1078.95 | 1037.61 | 180 | 1.35 | shed 2, LH1 upper shelf: Kamidana offerings: sake flasks, sakaki branch, small dishes |
| L20 | `StaticObj_JP_F_Tokkuri_Pair` | 1078.42 | 1037.61 | 180 | 1.35 | shed 2, LH1 upper shelf: Sake flasks (tokkuri) and cups |
| L43 | `StaticObj_JP_F_Choba_Set_Desk` | 1079.50 | 1037.61 | 180 | 0.95 | shed 2, LH1 lower shelf: Account clutter: ledgers, abacus, coin box, scales |
| L44 | `StaticObj_JP_F_Masu_Set` | 1078.85 | 1037.61 | 180 | 0.95 | shed 2, LH1 lower shelf: Measures (masu) and strickle |
| L26 | `StaticObj_JP_F_Hiuchi_Box` | 1078.38 | 1037.61 | 180 | 0.95 | shed 2, LH1 lower shelf: Fire-striker kit (flint, steel, tinder box) on the kamado ledge |
| L48 | `StaticObj_JP_F_Tea_Matcha` | 1081.55 | 1037.61 | 180 | 1.35 | shed 2, LH2 upper shelf: Tea utensils (clay pot, cups, caddy), no tetsubin |
| L42 | `StaticObj_JP_F_Writing_Box` | 1080.95 | 1037.61 | 180 | 1.35 | shed 2, LH2 upper shelf: Writing box with inkstone and brushes, paper stack |
| L24 | `StaticObj_JP_F_Basket_Zaru` | 1080.40 | 1037.61 | 180 | 1.35 | shed 2, LH2 upper shelf: Baskets: zaru, kago and a back basket |
| L18 | `StaticObj_JP_F_Tableware_Hakozen_Stack` | 1082.52 | 1036.13 | 270 | 0.95 | shed 2, LH3 shelf: Tableware: box trays, legged trays, bowls, chopsticks |
| L21 | `StaticObj_JP_F_Suribachi_Bowl` | 1082.52 | 1036.60 | 270 | 0.95 | shed 2, LH3 shelf: Grinding bowl (suribachi) and pestle, cutting board with a knife |
| L31 | `StaticObj_JP_F_Sewing_Box` | 1082.52 | 1037.00 | 270 | 0.95 | shed 2, LH3 shelf: Sewing box with a half-sewn garment, needles and thread |
| L15 | `StaticObj_JP_F_Butsudan_Lacquer` | 1077.70 | 1037.10 | 90 | 0.05 | shed 2, floor: Household Buddhist cabinet or shelf |
| L28 | `StaticObj_JP_F_Byobu_Makura` | 1078.55 | 1035.05 | 180 | 0.05 | shed 2, floor: Bedding screen and entrance screen |
| L30 | `StaticObj_JP_F_Clothes_Kimono` | 1080.20 | 1035.45 | 190 | 0.05 | shed 2, floor: Dropped clothes: a kimono and an obi on the mat |
| L33 | `StaticObj_JP_F_Goban_Go` | 1081.75 | 1035.05 | 180 | 0.05 | shed 2, floor: Go or shōgi board with pieces scattered |
| L34 | `StaticObj_JP_F_Toys_Koma` | 1079.05 | 1036.15 | 210 | 0.05 | shed 2, floor: Children's toys: spinning top, battledore, a cloth doll |
| L32 | `StaticObj_JP_F_Mirror_Stand` | 1081.55 | 1036.20 | 180 | 0.05 | shed 2, floor: Mirror stand |
| L35 | `StaticObj_JP_F_Shokudai_Tall` | 1077.70 | 1035.65 | 180 | 0.05 | shed 2, floor: Candle stand (rich houses) |
| L36 | `StaticObj_JP_F_Straw_Bed_Pile` | 1079.70 | 1036.85 | 180 | 0.05 | shed 2, floor: Straw bedding pile (the poor's bed) |
| L10 | `StaticObj_JP_F_Chochin_Crest` | 1080.00 | 1034.18 | 180 | 2.52 | shed 2, hanging from the front beam: Hanging paper lantern (chōchin) with a family crest or shop name |
| L29 | `StaticObj_JP_F_Iko_Robe` | 1086.40 | 1037.45 | 180 | 0.05 | shed 3, floor: Clothes rack with a robe over it |
| L38 | `StaticObj_JP_F_Izaribata` | 1089.55 | 1037.20 | 180 | 0.05 | shed 3, floor: Hand loom (izaribata) with cloth on it |
| L37 | `StaticObj_JP_F_Itoguruma` | 1087.95 | 1037.35 | 180 | 0.05 | shed 3, floor: Spinning wheel |
| L39 | `StaticObj_JP_F_Straw_Work_Sandal` | 1086.25 | 1035.95 | 180 | 0.05 | shed 3, floor: Straw work in progress: a half-made sandal, a straw bundle, a low stool |
| L40 | `StaticObj_JP_F_Mi` | 1087.70 | 1036.15 | 180 | 0.05 | shed 3, floor: Winnowing basket (mi) and rice sieve |
| L41 | `StaticObj_JP_F_Usu` | 1089.90 | 1035.80 | 180 | 0.05 | shed 3, floor: Rice mortar and pounder, stone hand mill |
| L45 | `StaticObj_JP_F_Katanakake_Stand` | 1088.80 | 1034.75 | 180 | 0.05 | shed 3, floor: Sword rack |
| L46 | `StaticObj_JP_F_Yoroibitsu` | 1087.55 | 1034.90 | 180 | 0.05 | shed 3, floor: Armour chest |
| L49 | `StaticObj_JP_F_Manger_Trough` | 1085.95 | 1035.05 | 270 | 0.05 | shed 3, floor: Stable corner: manger, fodder cutter, straw pile |
| L50 | `StaticObj_JP_F_Fallen_Leaf_Shoji` | 1088.95 | 1035.75 | 260 | 0.05 | shed 3, floor: Fallen shoji or fusuma leaf, paper torn |
| L52 | `StaticObj_JP_S_Kaki_Curtain_1ken` | 1089.82 | 1034.11 | 180 | 0.52 | shed 3, under the front eave: Autumn: persimmon curtains under the eaves (outdoor version of #8) |
| L69 | `StaticObj_JP_S_Sandals_Sale_Eave` | 1088.00 | 1034.11 | 180 | 0.52 | shed 3, under the front eave: Straw sandals hung for sale outside a tea house |
| L59 | `StaticObj_JP_S_Bird_Cage_Hung` | 1086.18 | 1034.11 | 180 | 0.52 | shed 3, under the front eave: Empty bird cage hung under the eaves |
| L56 | `StaticObj_JP_S_Ladder_Lean` | 1069.20 | 1035.40 | 270 | 0.00 | shed 1, leaning on shed 1's west end wall (outside): Ladder leaned against the eaves |
| L57 | `StaticObj_JP_S_Charcoal_Bales_Stack` | 1069.26 | 1037.00 | 270 | 0.00 | shed 1, stacked by shed 1's west end wall (outside): Charcoal bales stacked by a door |
| L54 | `StaticObj_JP_S_Farm_Tools_Lean` | 1090.80 | 1036.90 | 90 | 0.00 | shed 3, leaning on shed 3's east end wall (outside): Farm tools leaned on a wall: hoe, sickle, flail, rake |
| L71 | `StaticObj_JP_S_Amado_Half_Open` | 1090.80 | 1035.10 | 90 | 0.00 | shed 3, a shutter stood against shed 3's east end wall (outside): Shop shutters (amado) half open, one fallen in the street |
| L63 | `StaticObj_JP_S_Travel_Gear_Set` | 1068.60 | 1030.00 | 180 | -0.00 | ground strip: Dropped travel gear: straw hat, walking stick, a cloth bundle, a sandal |
| L74 | `StaticObj_JP_S_Footwear_Pairs` | 1071.00 | 1030.30 | 180 | 0.00 | ground strip: Wooden clogs (geta) and sandals scattered at an entrance |
| L72 | `StaticObj_JP_S_Lantern_Fallen_Chochin` | 1073.40 | 1030.00 | 160 | -0.00 | ground strip: A torn paper lantern fallen in the street |
| L73 | `StaticObj_JP_S_Stool_Std` | 1075.50 | 1030.30 | 200 | -0.00 | ground strip: A wooden stool knocked over |
| L53 | `StaticObj_JP_S_Tsukimi_Stand` | 1081.00 | 1030.60 | 180 | -0.00 | ground strip: Autumn: moon-viewing stand: pampas grass in a vase, a dango offering |
| L58 | `StaticObj_JP_S_Potted_Stand` | 1083.20 | 1030.30 | 180 | 0.00 | ground strip: Potted plants on a stand |
| L61 | `StaticObj_JP_S_Stable_Yard_Tie_Post` | 1085.90 | 1030.20 | 180 | -0.00 | ground strip: Stable yard: tie post, trough, pack saddle on a rack |
| L62 | `StaticObj_JP_S_Scarecrow_Kasa` | 1089.00 | 1030.00 | 180 | 0.00 | ground strip: Scarecrow (kakashi) |
| L68 | `StaticObj_JP_S_Fire_Watch_Rack` | 1092.40 | 1030.40 | 180 | 0.00 | ground strip: Fire watch gear on a street corner: buckets, fire hook, ladder rack |
| L51 | `StaticObj_JP_S_Hasa_Low` | 1069.40 | 1025.40 | 180 | 0.00 | ground strip: Autumn: rice drying racks (hasa-kake) hung with sheaves |
| L60 | `StaticObj_JP_S_Kakei_Trough` | 1075.00 | 1025.40 | 180 | 0.00 | ground strip: Bamboo water pipe (kakei) into a wooden trough |
| L55 | `StaticObj_JP_S_Leaf_Pile_Broom` | 1080.30 | 1025.00 | 180 | 0.00 | ground strip: Broom and a raked leaf pile |
| L65 | `StaticObj_JP_S_Tenbin_Spill_Boxes` | 1085.00 | 1025.20 | 180 | 0.00 | ground strip: Overturned vendor's load: tenbin pole with spilled boxes or baskets |
| L64 | `StaticObj_JP_S_Kago_Down` | 1089.80 | 1025.00 | 90 | 0.00 | ground strip: Abandoned palanquin (kago), poles on the ground |
| L66 | `StaticObj_JP_S_Fishnet_Poles` | 1095.60 | 1023.50 | 90 | 0.00 | ground strip: Fishing nets drying on poles, with floats |
| L67 | `StaticObj_JP_S_Boat_Up` | 1072.50 | 1020.40 | 90 | 0.00 | ground strip: Small boat pulled up on a bank |
| LH4 | `StaticObj_JP_S_Bench_1ken` | 1078.20 | 1030.50 | 180 | 0.00 | a bench on the ground strip (host): jp_s_bench_1ken |
| L70 | `StaticObj_JP_S_Bench_Dress_Tea` | 1077.85 | 1030.50 | 180 | 0.43 | on the LH4 bench seat: Tea-house bench dressing: a tea cup, a tobacco tray, a folded cloth |

<!-- W2F BEGIN -->

## W2F wave 2: furnished shrine, temples and civic buildings (agent W2F, 2026-10-01)

Regenerate: `python spikes/W2F/layout_w2f.py` then `python spikes/W2F/map_md.py`. Buildings are the furnished variants (`buildings/w2f_sets.py`); `.sN` = a site object that belongs to that building; `t` = the stone terrace under it. y_off is over the ground at the object.

### Town shrine precinct (map w2f_map_precinct.jpg): the SH1 hall site + west of the approach

| ID | Class / p3d | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| P1t | `StaticObj_JP_F_Terrace_L` | 1024.00 | 1191.10 | 180 | -0.73 | stone terrace under P1 (1.4 m at the front) |
| P1 | `Land_JP_Shrine_Haiden_Town_Hiwada_Furnished` | 1024.00 | 1192.00 | 180 | 0.54 | town haiden (Hachimangu): drum, offerings, bell rope, name board |
| P1.s1 | `jp_f_saisen_bako_l.p3d` | 1021.81 | 1187.23 | 180 | 0.96 | the offering box at the foot of the steps (FX1: beside the stair foot, 0.88 m clear of it) |
| P2t | `StaticObj_JP_F_Terrace_M` | 1024.00 | 1205.71 | 180 | -1.11 | stone terrace under P2 (1.8 m at the front) |
| P2 | `Land_JP_Shrine_Honden_Nagare_Town_Furnished` | 1024.00 | 1207.00 | 180 | 0.48 | town honden (nagare sangen-sha, curved bark roof), sanctum sealed |
| P3 | `Land_JP_Shrine_Temizuya_Town_Furnished` | 1014.00 | 1147.00 | 90 | -0.07 | temizuya: basin + ladles |
| P4 | `Land_JP_Shrine_Shamusho_Sangawara_Furnished` | 1011.00 | 1165.00 | 90 | -0.12 | shamusho: amulet counter, talisman desk |
| P5 | `Land_JP_Shrine_Kagura_Town_Furnished` | 1011.50 | 1188.50 | 90 | -0.23 | kagura stage: drums, masks |

### Village shrine north of the C2 hamlet (map w2f_map_village.jpg)

| ID | Class / p3d | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| V1 | `Land_JP_Shrine_Haiden_Village_Furnished` | 945.00 | 1070.00 | 180 | 0.00 | village haiden: drum, offerings, bell rope |
| V1.s1 | `jp_f_saisen_bako_m.p3d` | 943.19 | 1066.12 | 180 | 0.00 | the offering box at the foot of the steps (FX1: beside the stair foot, 0.65 m clear of it) |
| V2 | `Land_JP_Shrine_Honden_Nagare_Village_Chigi_Furnished` | 945.00 | 1078.50 | 180 | 0.00 | village honden (nagare, chigi + katsuogi), sanctum sealed |
| V3 | `StaticObj_JP_S_Torii_Wood_Shinmei_Rope_Shide` | 945.00 | 1061.00 | 180 | 0.00 | village shrine torii (shinmei, rope + streamers) |
| V4 | `StaticObj_JP_S_Stone_Lantern_Oki_Moss` | 942.60 | 1063.20 | 90 | 0.00 | village shrine lantern (west) |
| V5 | `StaticObj_JP_S_Stone_Lantern_Oki_Moss` | 947.40 | 1063.20 | 270 | -0.00 | village shrine lantern (east) |

### Village temple, Jodo, west of the graveyard (map w2f_map_village.jpg)

| ID | Class / p3d | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| T1 | `Land_JP_Temple_Hondo_Village_Jodo` | 972.00 | 1123.50 | 180 | -0.00 | village hondo (Jodo): Amida, sutra desk |
| T1.s1 | `jp_f_saisen_bako_m.p3d` | 969.28 | 1117.80 | 180 | -0.00 | the donation box (FX1: was on the en, across both doors) (FX1: beside the stair foot, 1.56 m clear of it) |
| T2 | `Land_JP_Temple_Kuri_Village_Furnished` | 955.00 | 1122.00 | 180 | 0.00 | village kuri: kamado row, irori, guest room |
| T3 | `Land_JP_Temple_Shoro_Village_Bell` | 984.00 | 1112.00 | 180 | 0.00 | village bell tower with its bell |
| T4 | `Land_JP_Temple_Gate_Yakuimon_Furnished` | 972.00 | 1104.50 | 180 | 0.00 | village temple gate (yakui-mon) |
| T5 | `Land_JP_Temple_Do_2_Board_Jizo` | 962.00 | 1109.50 | 90 | 0.00 | Jizo hall |
| T5.s1 | `jp_f_saisen_bako_s.p3d` | 965.91 | 1107.79 | 90 | 0.00 | the donation box (FX1: on the ground beside the stair foot in both hall sizes; the 2-ken hall had it on the en, across the doors) (FX1: beside the stair foot, 0.65 m clear of it) |
| T6 | `StaticObj_JP_S_Stone_Lantern_Kasuga_18_Moss` | 969.00 | 1109.50 | 90 | 0.00 | temple lantern (west of the walk) |
| T7 | `StaticObj_JP_S_Stone_Lantern_Kasuga_18_Moss` | 975.00 | 1109.50 | 270 | -0.00 | temple lantern (east of the walk) |
| T8 | `StaticObj_JP_S_Stone_Jizo_Bib` | 958.40 | 1106.80 | 90 | -0.19 | a stone Jizo with its bib by the Jizo hall |

### Town temple, Zen, east of the street end (map w2f_map_east.jpg)

| ID | Class / p3d | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| U1 | `Land_JP_Temple_Hondo_Town_Zen` | 1100.00 | 1112.00 | 180 | 0.00 | town hondo (Zen): Shaka, big mokugyo, drum |
| U1.s1 | `jp_f_saisen_bako_l.p3d` | 1097.81 | 1106.09 | 180 | 0.00 | the donation box at the foot of the steps (FX1: beside the stair foot, 0.88 m clear of it) |
| U2 | `Land_JP_Temple_Kuri_Town_Zen` | 1114.50 | 1111.00 | 180 | 0.00 | town kuri (Zen): fish board, cloud gong |
| U3 | `Land_JP_Temple_Shoro_Town_Bell` | 1085.50 | 1118.50 | 90 | 0.00 | town bell tower (hakama), the bell upstairs |
| U4 | `Land_JP_Temple_Gate_Shikyakumon_Furnished` | 1100.00 | 1097.50 | 180 | 0.00 | town temple gate (shikyaku-mon) |
| U5 | `Land_JP_Temple_Do_3_Tile_Kannon` | 1083.00 | 1104.00 | 90 | 0.00 | Kannon hall |
| U5.s1 | `jp_f_saisen_bako_s.p3d` | 1087.82 | 1102.29 | 90 | 0.00 | the donation box (FX1: on the ground beside the stair foot in both hall sizes; the 2-ken hall had it on the en, across the doors) (FX1: beside the stair foot, 0.65 m clear of it) |
| U6 | `StaticObj_JP_S_Stone_Lantern_Kasuga_24` | 1097.00 | 1102.50 | 90 | -0.00 | temple lantern (west) |
| U7 | `StaticObj_JP_S_Stone_Lantern_Kasuga_24` | 1103.00 | 1102.50 | 270 | 0.00 | temple lantern (east) |
| U8 | `StaticObj_JP_S_Chozubachi_Small` | 1094.00 | 1103.00 | 90 | 0.00 | temple water basin |

### Civic set at both street ends (maps w2f_map_east.jpg = K1-K4, w2f_map_village.jpg = K5-K7)

| ID | Class / p3d | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| K1 | `Land_JP_Kido_Lattice_Bantaya_Furnished` | 1069.00 | 1080.00 | 90 | 0.00 | ward gate (kido) across the street's east end + the keeper's hut (hinged gate leaves) |
| K1.s1 | `jp_s_lantern_sign_tsuji.p3d` | 1066.60 | 1076.70 | 180 | 0.00 | the ward lantern beside the keeper's hut |
| K2 | `Land_JP_Teahouse_Shop_Thatch_Furnished` | 1075.50 | 1086.80 | 180 | 0.00 | tea house (chamise, thatch) at the street end |
| K3 | `Land_JP_Teahouse_Bench_Itabuki_Furnished` | 1074.50 | 1073.00 | 0 | 0.00 | bench tea house across the road |
| K4 | `Land_JP_Teahouse_Tateba_Itabuki_Furnished` | 1091.00 | 1086.50 | 180 | 0.00 | rest-stop tea house with rooms (tateba) |
| K5 | `Land_JP_Smithy_Open_Itabuki_Furnished` | 969.50 | 1086.00 | 180 | 0.00 | village smithy (cold forge, bellows, anvil) |
| K5.s1 | `jp_s_charcoal_bales_stack.p3d` | 968.00 | 1088.40 | 0 | 0.00 | charcoal bales against the back wall outside |
| K6 | `Land_JP_Swordsmith_Sangawara_Furnished` | 967.00 | 1072.00 | 0 | 0.00 | swordsmith (forge room + work room) |
| K7 | `Land_JP_Guardhut_M_Itabuki_Jishinban` | 977.50 | 1072.50 | 0 | 0.00 | jishin-ban guard house with the ridge fire ladder |
| K7.s1 | `jp_s_lantern_sign_tsuji.p3d` | 976.03 | 1074.87 | 0 | 0.00 | the ward lantern |

<!-- W2F END -->

<!-- FX2 BEGIN -->

## FX2: komainu, kitsune and lantern pairs (agent FX2, 2026-10-01)

Regenerate: `python spikes/FX2/layout_fx2.py`. Pairs are symmetric about their approach axis: the 'a' (open mouth) on the right and the 'un' on the left as one faces the shrine, toed in 15 deg. Every lantern on the SH1 / W2F approaches already stood in a mirrored pair (S04/S05 ... S29/S30, S92-S95, V4/V5, T6/T7, U6/U7); the Inari path had none: FX-I2 adds one.

### Town shrine approach (map fx2_map_guardians.jpg, panel P; with SH1 S01-S32)

| ID | Class | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| FX-P1a | `StaticObj_JP_S_Komainu_B_Un` | 1021.45 | 1102.10 | 165 | -0.00 | komainu pair, compact Edo form, just inside the ichi-no-torii S01 (west / left, facing the shrine) |
| FX-P1b | `StaticObj_JP_S_Komainu_B_A` | 1026.55 | 1102.10 | 195 | 0.00 | komainu pair, compact Edo form, just inside the ichi-no-torii S01 (east / right) |
| FX-P2a | `StaticObj_JP_S_Komainu_A_Un` | 1021.30 | 1138.90 | 165 | -0.02 | komainu pair, upright form (un with horn), inside the ni-no-torii S14 (west / left, facing the shrine) |
| FX-P2b | `StaticObj_JP_S_Komainu_A_A` | 1026.70 | 1138.90 | 195 | -0.02 | komainu pair, upright form (un with horn), inside the ni-no-torii S14 (east / right) |

### Village shrine (panel V; with W2F V1-V5)

| ID | Class | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| FX-V1a | `StaticObj_JP_S_Komainu_A_Un_Moss` | 942.80 | 1059.50 | 165 | 0.00 | komainu pair, upright form, mossy (old village shrine), outside the torii V3 (west / left, facing the shrine) |
| FX-V1b | `StaticObj_JP_S_Komainu_A_A_Moss` | 947.20 | 1059.50 | 195 | 0.00 | komainu pair, upright form, mossy (old village shrine), outside the torii V3 (east / right) |

### Inari corner (panel I; with SH1 S80-S85, I01-I16)

| ID | Class | x | z | yaw | y_off | What |
|---|---|---|---|---|---|---|
| FX-I1a | `StaticObj_JP_S_Kitsune_Key` | 1056.20 | 1223.90 | 165 | -0.11 | Inari fox pair (key / jewel), below the vermilion torii S80 (west / left, facing the shrine) |
| FX-I1b | `StaticObj_JP_S_Kitsune_Jewel` | 1059.80 | 1223.90 | 195 | -0.11 | Inari fox pair (key / jewel), below the vermilion torii S80 (east / right) |
| FX-I2a | `StaticObj_JP_S_Stone_Lantern_Kasuga_18_Moss` | 1056.00 | 1221.40 | 90 | -0.13 | lantern pair on the Inari path, Kasuga 1.8 mossy (west) |
| FX-I2b | `StaticObj_JP_S_Stone_Lantern_Kasuga_18_Moss` | 1060.00 | 1221.40 | 270 | -0.15 | lantern pair on the Inari path (east) |

<!-- FX2 END -->
