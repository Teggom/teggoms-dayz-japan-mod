# BUILD LIST: exterior parts for dwellings and shops, v1

**Stage:** B (materials, then parts), then C (architect)

**Author and date:** research agent A-EXT, 2026-09-27

**Scope:** exteriors of dwellings and shops, tiers 1-3: minka farmhouses, machiya, nagaya, shop fronts, hatago, tea houses and the family kura. Every part the architect needs to assemble them. Temples, government buildings, street dressing, gardens and interiors are in "Later".

**Files:** `build_list.json` (validates against `playbook/templates/build_list_schema.json`; the builders read it), `materials_needed.json` (the materials agent's task list), `refs_index.json` (new sources x01-x38 and E01-E18). Images are in `data/research_ext/refs/`. All four files come from `tools/gen_build_list.py`. Edit the data there and rerun it, so the markdown and the JSON stay identical.

**Reading the tables:** `[E03]`, `[T59]` or `x08` are sources. `(assumed)` means no source gives the value. D1-D10 are PLAYBOOK §5 deviations.


## What a house looks like, tier by tier (1730)

**Tier 1, rural and poor.** A low house under a heavy thatch roof. In the Kanto the roof is hipped, like the Kitamura
house of 1687; in Koshu it is a gable, like the Hirose house. The thatch is cut square at the eave and shows about
0.6 m of thickness. Walls are grey-brown earth between adzed posts and rails, with a plank skirt at the bottom. The
posts stand on single field stones. There are few openings: one wide plank door into the earth-floored doma, a
barred window or two, and a smoke hood on the ridge. There is no tile, no white plaster and no veranda. In mountain
and coast villages the same house has a low-pitched board roof, held down by rows of river stones on battens.
Back-alley tenements in towns are the urban tier 1: shingle roofs, board walls and board-bottomed paper doors.

**Tier 2, village and post town.** The Kiso post-town house has a low stone-weighted board roof with the eave
side to the street. The street front is dark vertical boards and lattice, with plank doors. By night the shop front
closes with vertical-sliding board shutters (suriage-do). The upper storey stays low. The village headman's house,
like the Sasaki house of 1731-32, is a big hipped thatch roof with stone-weighted board pent eaves front and back.
It has earth walls with board wainscots, a veranda with storm shutters and a shutter box, and shoji behind them.
Tile appears only on the family kura or a big inn.

**Tier 3, town and main road.** The Kamigata machiya, like the Ioka house of the late 17th or early 18th century,
has a gable roof of sangawara tiles. The ridge is stacked, with an end tile at each end, and the eave tiles have
small round ends. A tiled pent roof runs over the ground floor. The upper storey is low and plastered, pierced by
small oval mushiko windows. The ground floor is dark lattice, with bengara used sparingly, and a plank front door.
Plastered udatsu wing walls stand between neighbours. The sill rests on a course of separate stones. Edo in 1730
looks different. Tile was banned there from 1657 to 1720 except on storehouses, so about half the roofs are still
boards, possibly strewn with oyster shells (decision 3), and half are new tile. Fronts are boards or the new
plastered nuriya. The kura behind has thick plaster walls, a namako lower wall, a tile roof and hinged plaster doors.

**What changes from machiya v1:** the roof is corrugated tile geometry with real eave, verge and ridge parts
(`jp_p_roof_sangawara_*`, `jp_p_roof_kawara_ridge`, `jp_p_roof_onigawara`). The upper storey is low, with oval
mushiko (`jp_p_open_mushiko`). The plaster is darker and mostly earth rather than white (`earth_wall_aged`; shikkui
<=192 and only at tier 3). The base is separate stones under a timber sill (`jp_p_found_dodai_stones`,
`jp_p_found_soseki`).

## Decisions only Stephen can make

1. **Wall colour:** approve the new sampled palette entry `earth_wall_aged` (115,98,80) as the default exterior
   earth wall for tiers 1-2, with shikkui (<=192) only on tier-3 upper storeys and kura.
2. **Board roof colour:** approve `roof_board_silver` (123,128,134) for board and stone-weighted roofs.
3. **Edo oyster-shell roofs (kakigara-buki), 1657 to the Kyoho era:** add them as the Edo tier-3 board-roof
   variant? It is cheap: one extra material.
4. **Dashigeta and projecting upper fronts:** the surviving examples date from after 1750 (Kagiya, 1856).
   Drop them, or keep them as a flagged deviation for Edo and Kiso?
5. **Full-height upper storey on tier-2 hatago:** the only evidence is 1830s prints (Goyu) and an undated text
   source [T30]. Allow a 2.40 m upper storey, or keep hatago low like the machiya?
6. **Thatch eave height:** a 45 deg thatch eave that keeps the 2.20 m soffit needs a wall plate of about
   3.0 m, where the real value is about 2.4-2.7 m. Accept the taller wall, or use the period board pent eave
   (the Sasaki type) over every entrance side?


## Roofs

| # | ID | Name | What and where | Imp. | Tier | Pri | Period evidence | Key dimensions | Materials (library -> palette) | Connectors | Variants |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `jp_p_roof_forms` | Roof forms and footprint rules (kirizuma / yosemune / irimoya) | The roof generator spec: which form and covering each tier and region uses, pitches, overhangs and spans. | hero | 1,2,3 | P1 | Kitamura house 1687, yosemune thatch [E01]; Kiyomiya late 17th c. yosemune thatch [E01]; Ito late 17th-early 18th c. irimoya thatch [E01]; Hirose late 17th c. kirizuma thatch [x08]; Sasaki 1731/32 yosemune thatch with stone-weighted board eaves [E02]; Ioka late 17th-early 18th c. kirizuma sangawara machiya [E03]; tile banned in Edo 1657 except storehouses, encouraged 1720 [E09] | grid_m 1.820 ken / 0.910 half-ken; footprints are unions of ken rectangles [PLAYBOOK §3-4]; pitch_kawara_sun 4.5 default (4-5.5) = 24.2 deg [PLAYBOOK §4]; pitch_ishioki_sun 3-3.5 (16.7-19.3 deg); steeper and the stones slide [T40, PLAYBOOK §4]; pitch_itabuki_sun 4-5 (assumed); +6 more in JSON | (generator spec) | footprint: rectangle or L/T union on the ken grid<br>eave line = keta top outer edge<br>ridge line centred on the span<br>kawara columns 0.260 m = 7 per ken, so a column edge lands on every ken line<br>lean-to (geya/hisashi) roofs attach below the main eave at a wall line | `kirizuma` gable: machiya, nagaya, kura, Kiso post town, Koshu farmhouse, tea house<br>`yosemune` hip: Kanto farmhouse (Kitamura 1687, Kiyomiya), headman house (Sasaki)<br>`irimoya` hip-and-gable with a smoke opening in the small gable: Kansai/Kanto farmhouse (Ito), bigger inns<br>`kabuto` Sasaki-type gable cut into a hip (kabuto-zukuri) at one end; P2 |
| 2 | `jp_p_roof_eave_soffit` | Eave soffit: rafters, sheathing and fascia (noki-ura) | The visible underside and edge of every eave: exposed rafters, sheathing boards and the fascia the eave tiles or boards sit on. | standard | 1,2,3 | P1 | Surviving period buildings all show exposed rafter soffits [x01, x08, x07] | rafter_section_m 0.045 x 0.060 (tile/board); thatch: round poles d 0.06-0.08 (assumed); rafter_spacing_m 0.303 (ken/6) (assumed); sheathing_m boards 0.012 thick visible between rafters; thatch: bamboo lath at 0.10 (assumed); fascia_m 0.030 x 0.120 (tile: carries the eave tiles); none on thatch (assumed); +1 more in JSON | rafters, fascia, sheathing: `jp_m_wood_weathered` -> timber_weathered<br>thatch lath: `jp_m_bamboo_weathered` -> bamboo_weathered | eave: rafter seats on keta top; rafter feet on the eave line<br>soffit follows the roof pitch; the generator emits it for every eave run | `_tile` square rafters + boards + fascia<br>`_board` thinner rafters, no fascia, boards overhang 0.03<br>`_thatch` pole rafters + bamboo lath |
| 3 | `jp_p_roof_sangawara_field` | Sangawara field tiles | The corrugated one-piece S-tile field of every tiled town roof, kura and inn. | hero | 2,3 | P1 | Sangawara invented 1674 [T07, E06]; Ioka machiya (Nara, late 17th-early 18th c.) is sangawara [E03]; Kyoto commoner tile spreads after sangawara, standard look by the 18th c. [E10]; Edo tile encouraged 1720 [E09] | working_width_m 0.26 [PLAYBOOK §4 (ken/7)]; exposure_m 0.235 [PLAYBOOK §4]; roll_height_m 0.05-0.06 [PLAYBOOK §4]; tile_thickness_m 0.018 (assumed); +2 more in JSON | tiles: `jp_m_roof_kawara` -> kawara_ibushi<br>white pointing (variant): `jp_m_wall_shikkui` -> shikkui_white | eave: first course overhangs the fascia by 0.06<br>ridge: last course tucks under the ridge noshi<br>verge: field stops 0.13 inside the verge line for jp_p_roof_sangawara_verge<br>columns 0.260 aligned to ken lines | `_std` plain field; per-row tint offset (W8)<br>`_pointed` white mortar pointing on the 2-3 rows at the eave and ridge; Morse: common on better roofs [T59] |
| 4 | `jp_p_roof_sangawara_eave` | Sangawara eave tiles (noki-gawara, manju type) | The first course of a tiled roof: small round end plus a turned-down lip carrying a relief band. | hero | 2,3 | P1 | Special eave tile named with sangawara [E06]; form drawn by Morse [x16, x18] | lip_depth_m 0.045 (assumed); round_end_diameter_m 0.075 (assumed); overhang_past_fascia_m 0.06 (assumed) | tile: `jp_m_roof_kawara` -> kawara_ibushi | eave: one per column (0.260), placed by the generator on the eave line | `_tomoe` round end with a mitsudomoe relief<br>`_plain` round end plain<br>`_lod1_strip` LOD1: the whole eave as one extruded strip |
| 5 | `jp_p_roof_sangawara_verge` | Verge tiles (sode-gawara / keraba) | Tiles that turn down over the bargeboard along every tiled gable edge. | standard | 2,3 | P1 | Named among the sangawara special tiles [E06] | flange_drop_m 0.07 (assumed); module_m 0.235 per course (matches exposure) [PLAYBOOK §4] | tile: `jp_m_roof_kawara` -> kawara_ibushi | verge: one per course along the gable line, over jp_p_roof_hafu<br>meets the eave tile at the corner and the ridge end below the onigawara | `_L` left hand<br>`_R` right hand |
| 6 | `jp_p_roof_kawara_ridge` | Tiled ridge (noshi courses + ganburi cap) and hip ridge | Stacked flat noshi courses capped by a round tile along the ridge, and the same build-up down the hips of hipped tile roofs. | hero | 2,3 | P1 | Noshi and ganburi named with sangawara [E06]; course count rises with status [PLAYBOOK §6.1]; Morse on ridges [T59] | noshi_course_m 0.025 thick each, 0.22 wide (assumed); courses T2 kura/inn 3; T3 machiya 3-5; hongawara elite 7 (later) [PLAYBOOK §6.1]; cap_diameter_m 0.16 (assumed); height_above_field_m 3 courses 0.30; 5 courses 0.38 (assumed); +1 more in JSON | tiles: `jp_m_roof_kawara` -> kawara_ibushi<br>mortar bedding lines: `jp_m_wall_shikkui` -> shikkui_white | ridge: runs the ridge line between the two onigawara<br>hip: from the ridge end to the eave corner on yosemune/irimoya | `_c3` 3 noshi courses<br>`_c5` 5 noshi courses<br>`_hip` hip ridge (kudarimune) with an end tile |
| 7 | `jp_p_roof_onigawara` | Ridge-end tile (onigawara) | The shouldered end block at each end of a tiled ridge. | standard | 2,3 | P1 | Onigawara named among sangawara special tiles [E06]; Morse: ridges always end in a shouldered mass [T59] | height_m T2 0.30; T3 0.38 (scales with the ridge) (assumed); width_m 0.30-0.36 (assumed) | tile: `jp_m_roof_kawara` -> kawara_ibushi | ridge: one at each ridge end, over the verge | `_plain` plain shouldered block<br>`_sui` with the character for water in relief (fire charm; Morse notes it on ridge ends)  |
| 8 | `jp_p_roof_hongawara` | Hongawara set (flat pans + round covers, eave and ridge) | The two-piece true tile for rich kura and, later, temples, gates and samurai elite. | standard | 3 | P3 | Hongawara is the older tile, on temples, castles and rich kura [T10, PLAYBOOK §6.1] | column_m 0.303 (ken/6) (assumed); cover_diameter_m 0.15 (assumed) | tiles: `jp_m_roof_kawara` -> kawara_ibushi | same eave, ridge and verge connectors as sangawara, 6 columns per ken | `_field` field<br>`_eave` round-end + flat eave with karakusa lip<br>`_ridge` taller ridge, 5-7 courses |
| 9 | `jp_p_roof_ishioki_field` | Stone-weighted board roof: board field (ishioki-yane, kureita) | Split boards in overlapping courses at a low pitch, the roof of Kiso post towns, mountain and coast villages. | hero | 1,2 (rural) | P1 | Stone-weighted board roofs in Kyoto in the early Edo period [E14]; Sasaki house 1731/32 has stone-weighted board eaves [E02]; Kiso post towns [c01-c03] | board_length_m 0.30-0.50 [E18 (low-grade web source)]; board_width_m 0.09-0.21, random per board (W8) [E18 figure read as cm; assumed]; board_thickness_m 0.004 real; model course edge 0.012 [E18; model value for silhouette (reason)]; course_exposure_m 0.15 (assumed); +2 more in JSON | boards: `jp_m_roof_kureita` -> roof_board_silver | eave: first course overhangs the rafter feet by 0.05<br>ridge: jp_p_roof_board_ridge<br>verge: jp_p_roof_hafu _ishioki<br>battens and stones: jp_p_roof_ishioki_battens | `_std` standard<br>`_worn` missing/lifted boards, moss (W6) on north slope |
| 10 | `jp_p_roof_ishioki_battens` | Stone-weighted roof: battens and stones (osae-gi + ishi) | Split-pole battens laid across the boards parallel to the eave, with river stones resting on them. | hero | 1,2 (rural) | P1 | as jp_p_roof_ishioki_field | batten_diameter_m 0.06-0.08 split pole (assumed); batten_spacing_m 0.60 up the slope (assumed); stone_size_m 0.15-0.30 [PLAYBOOK §6.1 [T40, c01-c03]]; stone_spacing_m 0.30-0.45 along each batten, jittered (assumed) | battens: `jp_m_wood_weathered` -> timber_weathered<br>stones: `jp_m_stone_river` -> stone_lantern | battens run eave-parallel between verges; stones sit on the upslope side of each batten<br>generator scatters stones from the 8-shape set with random yaw | `_stoneset8` 8 stone shapes<br>`_sparse` fewer stones (poor / neglected) |
| 11 | `jp_p_roof_itabuki_field` | Thin shingle / board roof (itabuki, kokera) | Thin split-shingle roofs: Edo townhouses before tile, back-alley nagaya, T2 houses and sheds. | standard | 1,2,3 | P1 | Board and kokera roofs on early machiya [T05]; in Edo tile was banned 1657-1720 except storehouses, board roofs with oyster shells recommended, still in use in the Kyoho era [E09] | shingle_thickness_m 0.002-0.003 (kokera) [E17]; course_exposure_m 0.09 (assumed); eave_edge_m 0.03-0.05 visible stack (assumed); pitch_sun 4-5 (assumed) | shingles: `jp_m_roof_kokera` -> roof_board_silver<br>bamboo strips (variant): `jp_m_bamboo_weathered` -> bamboo_weathered<br>oyster shells (variant): `jp_m_roof_kakigara` -> kakigara_shell | as ishioki: eave, board ridge, verge | `_plain` plain courses<br>`_bamboo` bamboo strips nailed obliquely ridge to eave against gales (Morse fig. 63)<br>`_kakigara` Edo only: oyster shells over the boards (fire measure 1657-Kyoho) - only if decision 3 is yes |
| 12 | `jp_p_roof_board_ridge` | Board ridge (for ishioki and shingle roofs) | Thin strips nailed over the ridge in a mass, held by battens; on ishioki roofs weighted with stones. | standard | 1,2,3 | P1 | Morse fig. 65 (1880s); form follows from the board roof [E14] | width_m 0.30-0.40 (assumed); height_m 0.06-0.10 (assumed) | strips: `jp_m_roof_kureita` -> roof_board_silver<br>stones: `jp_m_stone_river` -> stone_lantern | ridge: full ridge length, ends flush with the verge boards | `_strips` shingle roof ridge<br>`_stoned` ishioki ridge with a stone row |
| 13 | `jp_p_roof_thatch_body` | Thatch roof body (kaya-buki): field, cut eave, verge and hips | The thick thatch mass generated over any footprint, with the squared eave cut that shows its thickness. | hero | 1,2 (rural) | P1 | Kitamura 1687, Kiyomiya late 17th c. (yosemune), Ito (irimoya), Hirose (kirizuma), Sasaki 1731/32: all thatch [E01, E02, x08] | eave_cut_thickness_m 0.60 (0.40-0.80) [Morse: eaves trimmed square or slightly rounded, often two feet or more [T59]; PLAYBOOK §6.1]; field_thickness_m 0.35-0.45 (assumed); verge_overhang_m 0.30-0.45 [PLAYBOOK §4, x08]; pitch_deg 45 [T41]; +1 more in JSON | thatch surface: `jp_m_roof_thatch` -> thatch_weathered<br>eave cut face: `jp_m_roof_thatch_cut` -> thatch_weathered | eave: rests on the rafter feet; cut face vertical at the eave line + overhang<br>ridge: jp_p_roof_thatch_ridge<br>hips rounded (radius 0.3) | `_yosemune` Kanto hip (Kitamura type)<br>`_kirizuma` Koshu gable (Hirose type)<br>`_irimoya` hip-and-gable (Ito type)<br>`_new` freshly re-thatched (thatch_new tint via _w0), 1 roof in 10 |
| 14 | `jp_p_roof_thatch_ridge` | Thatch ridge treatments (bamboo, tiled, turf, umanori) | The ridge caps that close the top of a thatch roof; each region has its own style. | standard | 1,2 (rural) | P1 | Kiyomiya house, late 17th c.: iris growing on the (turf) ridge [E01]; ridge members count up with status [T17] | height_above_thatch_m 0.50-0.80 (assumed); umanori_spacing_m 0.91 (half-ken) (assumed); umanori_count T1 3-5, T2 5-7 per ridge (assumed) | bamboo binding: `jp_m_bamboo_weathered` -> bamboo_weathered<br>tiles (variant): `jp_m_roof_kawara` -> kawara_ibushi<br>thatch/turf cap: `jp_m_roof_thatch` -> thatch_weathered<br>crossed members: `jp_m_wood_weathered` -> timber_weathered | ridge: full ridge length; ends flush with the thatch verge or hip apex | `_bamboo` bamboo-bound ridge (Kanto)<br>`_tile` noshi/round tiles over the thatch ridge (Musashi)<br>`_shiba` turf ridge with iris (Kiyomiya type)<br>`_umanori` grass ridge with crossed timbers |
| 15 | `jp_p_roof_kemuridashi` | Smoke vents (ridge smoke hood, raised ridge vent, irimoya smoke gable) | How hearth smoke leaves a roof with no chimney: a hood on a thatch ridge, a raised louvred ridge on board/tile roofs, or the open irimoya gable. | standard | 1,2,3 | P1 | No chimneys; smoke leaves by roof vents and gable openings [PLAYBOOK §6.1]; Morse: triangular latticed opening at the gable [T59] | hood_width_m 0.60-0.90 (assumed); koshiyane_lift_m 0.30-0.45 above the main ridge (assumed); koshiyane_length_m 1.82 (1 ken) or 3.64 (assumed); irimoya_gable_opening_m triangle 0.9-1.4 wide, lattice 0.03 bars (assumed) | frame, louvres: `jp_m_wood_weathered` -> timber_weathered<br>inner soot faces: `jp_m_wood_sooted` -> timber_sooted<br>covering: `jp_m_roof_thatch` -> thatch_weathered | ridge: placed by the generator at a ridge position over the doma/kamado bay<br>irimoya variant is part of the irimoya roof form | `_hood` thatch ridge hood<br>`_koshiyane` raised ridge vent on board/tile roofs (smithy, kitchens)<br>`_irimoya` latticed triangle in the small gable |
| 16 | `jp_p_roof_hafu` | Bargeboards and gable edge (hafu-ita, purlin ends) | The plain boards finishing every gable edge, with the purlin ends that show under the verge. | standard | 1,2,3 | P1 | Gable rule 5 [PLAYBOOK §6.2]; visible on the dated Ioka and Hirose gables [x01, x08] | board_m 0.030 x 0.24 (assumed); purlin_end_projection_m 0.30 (assumed); purlin_section_m 0.10 x 0.12 (assumed) | boards, purlins: `jp_m_wood_weathered` -> timber_weathered | verge: follows the verge line from eave to ridge; purlin ends at each purlin (every 0.91 up the slope) | `_tile` under sode-gawara<br>`_board` with a verge batten for shingle/ishioki roofs<br>`_thatch` hidden; only purlin ends show under the thatch verge |
| 17 | `jp_p_roof_hisashi` | Pent roofs (hisashi): street pent, board pent, farmhouse board skirt, gable pent | The light lean-to roofs below the main eave: over the machiya shopfront, over verandas, as the board skirt of thatch houses and along tiled gables. | hero | 1,2,3 | P1 | Sasaki 1731/32: stone-weighted board eaves front and rear of the thatch roof [E02]; Suzuki: board-shingled eaves [E03]; Ioka: pent roofs front and side [E03]; Morse: hisashi of wide thin boards on slender brackets or posts [T59] | projection_m 0.91 (half-ken); veranda hisashi to 1.2 on posts (assumed); street_eave_edge_m 2.90-3.20; soffit >=2.20 where walked under [PLAYBOOK §4]; pitch tile 4 sun; board 2.5-3 sun; ishioki 3 sun (assumed); bracket_udegi_m 0.06 x 0.09 arm, from each post (0.91 or 1.82 c/c) (assumed); +1 more in JSON | tile variant: `jp_m_roof_kawara` -> kawara_ibushi<br>board variants: `jp_m_roof_kureita` -> roof_board_silver<br>brackets, fascia: `jp_m_wood_weathered` -> timber_weathered<br>stones (ishioki variant): `jp_m_stone_river` -> stone_lantern | post: udegi bracket plugs into each post at the pent height<br>eave: pent eave line parallel to the wall<br>top: flashed under the upper wall or main eave | `_tile` sangawara street pent (T3 machiya)<br>`_board` thin boards on brackets (Morse)<br>`_ishioki` Kiso stone-weighted pent<br>`_skirt` board skirt under a thatch roof, low pitch (Sasaki/Suzuki type)<br>`_gable` small tiled pent along a gable (Ioka) |
| 18 | `jp_p_roof_kura_eave` | Kura plastered eave and wall-head band | The fire-proof kura eave: rafters and soffit plastered over, with a thick plaster band at the wall head. | standard | 2,3 | P1 | Kura as the only tiled building allowed in Edo 1657-1720 [E09]; kura form [T59, c11] | band_height_m 0.30-0.45 (assumed); band_projection_m 0.05-0.10 per step, 2 steps (assumed); eave_overhang_m 0.45-0.60 (assumed) | plaster: `jp_m_wall_shikkui` -> shikkui_white<br>tiles above: `jp_m_roof_kawara` -> kawara_ibushi | eave: sits on the okabe wall top; tile eave course on top | `_std` plain stepped band<br>`_okiyane` separate roof raised on posts above a plastered roof: region/date unverified, P3 |
| 19 | `jp_p_roof_gutter` | Bamboo gutter and downpipe | A split-bamboo half-pipe on hooks along an eave, draining into a bamboo downpipe with a wooden funnel. | filler | 3 | P3 | Morse fig. 66 (1880s) only; 1730 use assumed | gutter_diameter_m 0.10 (assumed); hook_spacing_m 0.91 (assumed) | bamboo: `jp_m_bamboo_weathered` -> bamboo_weathered<br>hooks: `jp_m_metal_iron` -> iron_black | eave: hangs 0.05 below the eave edge on hooks at post positions | `_std` gutter + one downpipe |

## Walls and frame

| # | ID | Name | What and where | Imp. | Tier | Pri | Period evidence | Key dimensions | Materials (library -> palette) | Connectors | Variants |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 | `jp_p_wall_shinkabe` | Earthen wall between exposed posts (shinkabe), with header panel (kokabe) | The default house wall recipe: posts and rails visible, earth or plaster infill, generated for any run of half-ken bays. | hero | 1,2,3 | P1 | Hirose late 17th c.: earth infill between exposed posts and rails [x08]; Sasaki 1732 [x07] | infill_thickness_m 0.075 (0.06 T1 arakabe) [PLAYBOOK §6.2]; infill_setback_m 0.02 behind the post face, both sides (assumed); panel_max 1 ken x 1 storey [PLAYBOOK §6.2]; rail_heights_m sill 0 / door head 2.00 / wall plate [PLAYBOOK §4]; +1 more in JSON | T1 exterior: `jp_m_wall_arakabe` -> earth_wall_aged<br>T2 exterior: `jp_m_wall_nakanuri` -> earth_wall_aged<br>T3 upper storey: `jp_m_wall_shikkui` -> shikkui_white<br>posts, rails: `jp_m_wood_weathered` -> timber_weathered | post: panels span between post connectors on any half-ken run<br>sill: bottom on dodai or grade<br>head: door heads at 2.00; above = kokabe<br>eave: top under the keta | `_arakabe` rough, straw showing<br>`_nakanuri` smoother, T2<br>`_shikkui` white lime finish, T3 upper storeys<br>`_kokabe_ranma` header band as a plain lattice transom instead of plaster |
| 21 | `jp_p_wall_okabe` | Thick plastered wall, posts hidden (okabe): kura, nuriya fronts | Fire-proof walls with the frame buried in plaster: kura, the post-1720 plastered town fronts, udatsu. | standard | 2,3 | P1 | Edo encouraged plastered (dozo/nuriya) fronts from 1720 [T05, E09]; kura [c11] | thickness_m kura 0.24 (0.20-0.30); nuriya front 0.15 [PLAYBOOK §6.2 (kura); nuriya assumed]; corner sharp arris, slight irregularity (assumed) | plaster: `jp_m_wall_shikkui` -> shikkui_white | post: wall hides posts but still snaps to post connectors; openings cut on half-ken bays | `_kura` 0.24 thick<br>`_nuriya` Edo plastered townhouse front, 0.15 |
| 22 | `jp_p_wall_board_vertical` | Vertical board cladding (tate-ita-bari) with cover battens | Vertical boards on posts: Kiso street fronts, nagaya, farmhouse lower walls, gables. | standard | 1,2,3 | P1 | Ioka house (late 17th-early 18th c.) lower walls are vertical dark boards [x01] | board_width_m 0.24-0.30 random (assumed); board_thickness_m 0.015 (assumed); batten_m 0.036 x 0.018 at each joint (assumed) | boards: `jp_m_wood_weathered` -> timber_weathered<br>town fronts: `jp_m_wood_street_dark` -> timber_street_dark | post: boards fixed to the outer face of posts/rails; runs any half-ken length | `_battened` with cover battens<br>`_plain` butt boards, T1 |
| 23 | `jp_p_wall_shitami` | Lapped horizontal boards with battens (shitami-ita-bari) | Horizontal overlapping boards held by vertical battens: lower walls and gables in T2-3. | standard | 2,3 | P2 | Widely used through the Edo period (black form on official buildings [c16]); unpainted on houses (assumed) | exposure_m 0.20 (assumed); lap_m 0.025 (assumed); batten_spacing_m 0.455 (ken/4) (assumed) | boards: `jp_m_wood_street_dark` -> timber_street_dark<br>kura variant: `jp_m_wood_kuro` -> kuro_board | post: as board cladding | `_house` unpainted/dark weathered<br>`_kura` black-stained, kura only (restricted colour) |
| 24 | `jp_p_wall_koshiita` | Board wainscot on earth walls (koshi-ita) | A band of boards protecting the bottom of earth and plaster walls from splash. | standard | 1,2,3 | P1 | Board lower panels on the Hirose (late 17th c.) and Suzuki houses [x08, x06] | height_m 0.60 or 0.90 [PLAYBOOK §6.2]; drip_cap_m 0.02 x 0.04 top rail (assumed) | boards: `jp_m_wood_weathered` -> timber_weathered | post: between posts, bottom at sill | `_h060` 0.60 high<br>`_h090` 0.90 high |
| 25 | `jp_p_wall_namako` | Namako tile wall (namako-kabe) | Square dark tiles with raised half-round white plaster joints on kura lower walls. | standard | 2,3 | P2 | Appears from the Edo period; imo-bari (grid) is the oldest laying, shihan-bari (diagonal) the most widespread [E15] | tile_side_m 0.2145 (assumed); joint_width_m 0.035 (assumed); joint_relief_m 0.02 (assumed); height_m 0.9-1.8 (kura lower wall) (assumed) | tiles: `jp_m_wall_namako_tile` -> namako_tile<br>joints: `jp_m_wall_shikkui` -> shikkui_white | post: on okabe walls, bottom on the kura footing | `_imo` square grid (oldest form)<br>`_shihan` diagonal (most common) |
| 26 | `jp_p_wall_gable` | Gable end: frame, infill and vent (rule 5) | Every gable built up from exposed posts, ties and panels, with the right infill for its roof family. | hero | 1,2,3 | P1 | Hirose (late 17th c.) thatch gable [x08]; Ioka tile gable with pent roof [x01] | panel_max 1 ken x 1 storey [PLAYBOOK §6.2]; tie_beam_m 0.12 x 0.21 (assumed); vent_m 0.6-0.9 wide, lattice 0.03 (assumed) | frame: `jp_m_wood_weathered` -> timber_weathered<br>T1 infill: `jp_m_wall_arakabe` -> earth_wall_aged<br>T3 infill: `jp_m_wall_shikkui` -> shikkui_white<br>board infill: `jp_m_wood_weathered` -> timber_weathered | post: gable posts on the ken grid up to the ridge post<br>verge: meets jp_p_roof_hafu<br>eave: sits on the end tie beam | `_thatch` earth panels, thick thatch verge (Hirose)<br>`_tile` plaster above the pent, boards below (Ioka)<br>`_board` all boards (Kiso)<br>`_kura` plain okabe, small vent |
| 27 | `jp_p_wall_udatsu` | Udatsu fire wing walls (sode-udatsu, hon-udatsu) | Plastered wing walls with a small tile cap between adjoining town houses. | standard | 3 (kamigata) | P2 | Mid-Edo onward the udatsu became mainly decorative (a wealth sign) [E04]; T08 | projection_m 0.45-0.60 beyond the facade (assumed); thickness_m 0.18 (assumed); height sode: from the ground-floor pent to the upper eave (1.3-1.6); hon: 0.3-0.5 above the roof plane (assumed); cap_width_m 0.30-0.35 tile cap (assumed) | plaster: `jp_m_wall_shikkui` -> shikkui_white<br>cap: `jp_m_roof_kawara` -> kawara_ibushi | post: on the party-wall post line at the facade<br>eave: bottom on the ground-floor pent, top under the main eave | `_sode` wing wall at the upper storey (default)<br>`_hon` parapet on the gable with its own roof (rich, P3) |
| 28 | `jp_p_frame_post` | Exterior posts | Corner and wall posts that the walls, doors and pents all snap to. | standard | 1,2,3 | P1 | Kitamura 1687: adze-marked posts between the main room and doma [E01]; post sizes [T46] | section_m 0.120 (T2-3); 0.150 farmhouse main posts [PLAYBOOK §4 [T46]]; position centred on grid nodes [PLAYBOOK §4] | posts: `jp_m_wood_weathered` -> timber_weathered<br>town fronts: `jp_m_wood_street_dark` -> timber_street_dark | post: the grid node itself; bottom on soseki or dodai | `_planed` straight, T2-3<br>`_adzed` adze facets, slight irregularity (Kitamura) |
| 29 | `jp_p_frame_beam` | Exposed beams and rails (keta, hari ends, nuki, dodai) | The horizontal members visible outside: wall plates, beam ends at gables, rails and sills. | standard | 1,2,3 | P1 | as jp_p_wall_gable | keta_m 0.12 x 0.18 (assumed); nuki_m 0.03 x 0.105 (assumed); dodai_m 0.12 x 0.12 (assumed); hari_end_projection_m 0.15-0.25 (assumed) | timber: `jp_m_wood_weathered` -> timber_weathered | post: members span post to post; beam ends project at gables | `_sawn` sawn<br>`_log` log beam ends (farmhouse) |
| 30 | `jp_p_frame_dashigeta` | Cantilevered eave purlin (dashigeta) / projecting upper floor | Arms from the posts carrying a purlin that holds a deep street eave; Edo shop fronts and Kiso post towns. | standard | 2,3 (edo) | P3 | Surviving examples are late Edo (Kagiya 1856); the form spread in Edo shops from late Edo [E11]. NOT verified for 1730 | cantilever_m 0.45-0.90 (assumed) | timber: `jp_m_wood_street_dark` -> timber_street_dark | post: arms plug into the front posts at the upper floor line | `_std` dashigeta arm + purlin |

## Openings

| # | ID | Name | What and where | Imp. | Tier | Pri | Period evidence | Key dimensions | Materials (library -> palette) | Connectors | Variants |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | `jp_p_open_itado` | Plank sliding door (itado), incl. oodo with wicket | The exterior plank door of every tier; the main entrance is one wide leaf sliding along the outside of the next bay. | hero | 1,2,3 | P1 | T1 doors are plank itado [PLAYBOOK §2.1]; shop fronts of 1690 [x33] | bay 1 half-ken leaf; main entrance: one leaf on a 1.5-ken opening, >=1.00 clear [PLAYBOOK §6.3, D1]; head_m 2.0 [D2]; leaf_thickness_m frame 0.033, boards 0.012 (assumed); battens 3-5 horizontal (assumed); +1 more in JSON | leaf: `jp_m_wood_weathered` -> timber_weathered<br>town leaf: `jp_m_wood_street_dark` -> timber_street_dark<br>fittings: `jp_m_metal_iron` -> iron_black | post: between post connectors, 0.5/1/1.5/2 ken<br>sill: runs in a grooved sill at floor level<br>head: 2.00 | `_plain` boards only<br>`_battened` frame + battens<br>`_oodo` big leaf with a decorative kuguri wicket (D9)<br>`_pair` two leaves in a 1-ken bay |
| 32 | `jp_p_open_koshido` | Lattice sliding door (koshi-do) | A day door of vertical bars used at T2-3 entrances behind the itado. | standard | 2,3 | P2 | Koshi fronts on hatago and machiya [T30, E10] | bar_face_m 0.03 [E16 (1 sun face)]; bar_gap_m 0.03 (assumed); lower_board_m 0.3 (assumed); head_m 2.0 [D2] | lattice: `jp_m_wood_street_dark` -> timber_street_dark | post/sill/head as jp_p_open_itado | `_open` bars only<br>`_papered` paper behind the bars |
| 33 | `jp_p_open_shoji_ext` | Exterior paper doors (koshidaka-shoji, akari-shoji) | Paper sliding doors facing outside: the board-bottomed door of nagaya and doma entrances, and the shoji line behind amado. | standard | 1,2,3 | P1 | Shoji at T2-3 [PLAYBOOK §2.1]; paper shop doors in 1830s road prints [x35] | lower_board_m koshidaka 0.60; akari 0.15 (assumed); kumiko_m 3 verticals per leaf, horizontals at 0.25 (assumed); head_m 2.0 [D2] | paper: `jp_m_paper_shoji` -> washi_shoji<br>frame: `jp_m_wood_weathered` -> timber_weathered | post/sill/head as jp_p_open_itado | `_koshidaka` board-bottomed door (nagaya, doma)<br>`_akari` plain shoji behind amado |
| 34 | `jp_p_open_amado` | Storm shutters (amado) | Thin board shutters on one outer track that close a veranda or window line at night. | standard | 2,3 | P1 | Amado from 1587 (Jurakudai) [E07] | leaf_m 0.91 wide x door head [half-ken bay (PLAYBOOK §6.3)]; board_m 0.009 boards on a light frame with a few bars [Morse [T59] (thickness assumed)]; track single groove on the outer edge of the veranda [Morse [T59]] | leaf: `jp_m_wood_weathered` -> timber_weathered | sill: outer groove of jp_p_porch_engawa<br>head: 2.00 under a small transom band<br>stows into jp_p_open_tobukuro at one end | `_stowed` static: all leaves in the box (default)<br>`_closed` static closed line (abandoned houses; blocks the opening) |
| 35 | `jp_p_open_tobukuro` | Shutter box (tobukuro) | The board box at the end of an amado run that holds the stowed leaves. | standard | 2,3 | P1 | Box types named with amado [E07]; Morse swinging closet [x25] (1880s) | inner_width_m leaf + 0.05 (assumed); depth_m n leaves x 0.03 + 0.05 (assumed); height_m leaf + 0.10 (assumed) | box: `jp_m_wood_weathered` -> timber_weathered | post: outside the end post of the run, on the veranda edge line | `_box` covered box (to-bako)<br>`_swing` Morse swinging closet, P3 |
| 36 | `jp_p_open_kura_door` | Kura doors (hinged plastered doors + inner sliding doors) | The only hinged doors: thick stepped plaster leaves, an inner lattice/board sliding door and a small pent roof above. | hero | 2,3 | P1 | Kura doors [PLAYBOOK §6.3]; old Kyoto kura doorway [x23] (1880s drawing of an old kura) | clear_m >=1.00 x 2.00 [D1, D2]; leaf_thickness_m 0.15-0.20 (assumed); jamb_steps 3-5 steps of 0.03-0.04 (assumed); door_pent_m 0.60 deep on 2 brackets (assumed) | leaves, jambs: `jp_m_wall_shikkui` -> shikkui_white<br>inner doors: `jp_m_wood_weathered` -> timber_weathered<br>hinges, hasp: `jp_m_metal_iron` -> iron_black<br>pent: `jp_m_roof_kawara` -> kawara_ibushi | post: centred on a 1-ken bay of an okabe wall<br>sill: raised stone threshold 0.15 | `_open` outer leaves static open; inner sliding door is the game door (P1)<br>`_hinged` outer leaves as rotation doors (P2, engine test) |
| 37 | `jp_p_open_kura_window` | Kura window (barred, plaster shutters, tiny pent) | Small barred kura window with thick plaster shutters and a mini tile pent. | standard | 2,3 | P2 | as kura | opening_m 0.60 x 0.75 (assumed); bars_m 0.03 at 0.09 (assumed); shutter_thickness_m 0.12 (assumed) | shutters: `jp_m_wall_shikkui` -> shikkui_white<br>bars: `jp_m_metal_iron` -> iron_black<br>pent: `jp_m_roof_kawara` -> kawara_ibushi | post: centred in a half-ken or 1-ken bay; sill at 1.2 (ground) or 0.6 (upper) | `_slide` sliding plaster shutter<br>`_hinged` pair of hinged shutters (static open) |
| 38 | `jp_p_open_mushiko` | Mushiko window, 1730 form (small oval) | The plastered slatted window of the low upper storey of Kamigata machiya; in 1730 small and oval, not the later rectangle. | hero | 3 (kamigata) | P1 | Early mushiko-mado were small and oval; they became larger and rectangular in the Meiji period [E05]; standard on 18th c. Kyoto machiya [E10] | opening_m 0.90 wide x 0.45 high, round ends (assumed); slat_face_m 0.045 (assumed); slat_gap_m 0.045 (assumed); depth_m wall thickness 0.15 (assumed); +1 more in JSON | plaster: `jp_m_wall_shikkui` -> shikkui_white | post: centred on a half-ken bay of the upper okabe front; 1 per 1-2 bays | `_oval` single oval<br>`_oval_pair` two ovals in one 1-ken bay |
| 39 | `jp_p_open_koshi` | Koshi lattice fronts and windows (incl. de-goshi) | Wooden lattice modules for street fronts and windows, with trade variants and the projecting de-goshi. | hero | 2,3 | P1 | De-goshi part of the 18th c. standard Kyoto front [E10]; lattice fronts on hatago [T30] | module_widths 0.5 / 1 / 1.5 / 2 ken [PLAYBOOK §10.2]; bar_face_m 0.03 [E16]; bar_depth_m 0.05 (assumed); degoshi_projection_m 0.3 (assumed); +2 more in JSON | lattice: `jp_m_wood_street_dark` -> timber_street_dark<br>Kamigata finish: `jp_m_wood_bengara` -> bengara_lattice | post: between post connectors<br>sill: own sill rail on the dodai or a board base<br>head: 2.00 rail | `_kyo` fine bars, few rails<br>`_oyako` parent bars + cut-top children (cloth/thread shops)<br>`_komeya` thick bars (rice, charcoal)<br>`_degoshi` projecting lattice on its own sill<br>`_bengara` bengara finish (Kamigata, sparingly) |
| 40 | `jp_p_open_renji` | Barred and slatted windows (renji-mado, muso-mado) | Plain barred windows with a sliding board shutter; the everyday window of farmhouses and kitchens. | standard | 1,2,3 | P1 | Lattice windows on the Ito house (late 17th-early 18th c.) [E01]; renji-mado for rural T1 [PLAYBOOK §2.1] | opening_m 0.91 x 0.60-0.90 (assumed); sill_m 0.9 (assumed); bars_m bamboo d 0.028 or wood 0.03 square at 0.08 c/c (assumed); muso_slat_m 0.045 slats, 0.045 gaps, one panel slides (assumed) | bars: `jp_m_bamboo_weathered` -> bamboo_weathered<br>frame, shutter: `jp_m_wood_weathered` -> timber_weathered | post: half-ken or 1-ken bay; the shutter slides inside the wall line | `_bamboo` bamboo bars<br>`_wood` square wood bars<br>`_muso` double slatted panels (kitchens; date unverified) |
| 41 | `jp_p_open_suriagedo` | Vertical-sliding shop shutters (suriage-do / agedo) | The night closure of an open shop front: stacked boards that slide up in post grooves into a box behind the upper beam. | hero | 2,3 | P1 | Standard through the Edo period to mid-Meiji (Seki-juku) [E12]; agedo on the Suzuki house front [E03]; Inoue house, Kurashiki (1721 renovation) has shitomi and suriage shutters [E13] | boards 3 per opening, each ~0.68 high (2.04 / 3) [E12 (3 boards); height derived from D2]; bay 1 ken per stack (assumed); storage box behind the upper beam inside, occupying the upper front wall [E12]; groove_m 0.03 wide in the posts (assumed) | boards: `jp_m_wood_street_dark` -> timber_street_dark<br>box: `jp_m_wood_weathered` -> timber_weathered | post: grooves in the two posts of a 1-ken bay<br>head: stack top under the 2.00 beam; box above it inside | `_closed` static closed<br>`_part` static, one board lowered<br>`_door` animated: whole stack as one leaf, vertical translation (engine test) |
| 42 | `jp_p_open_shitomido` | Hinged-up shop shutter (shitomido) | Kamigata shop closure: an upper panel hinged at the top and hooked up by day, a lower panel lifted out. | standard | 3 (kamigata) | P2 | Inoue house, Kurashiki (1721 renovation) has shitomido [E13]; upper panel larger than the lower [E08] | bay 1 ken (assumed); upper_panel_m 1.1 high (assumed); lower_panel_m 0.8 high (assumed); panel_build lattice with boards behind [E08] | panels: `jp_m_wood_street_dark` -> timber_street_dark<br>hooks: `jp_m_metal_iron` -> iron_black | post: between the posts of a 1-ken bay; hinge at the 2.00 head rail | `_up` static: upper hooked up under the pent, lower removed<br>`_closed` static closed |
| 43 | `jp_p_open_battari` | Fold-down shop bench (battari-shogi) | A bench hinged to the Kamigata shop front, folded up at night. | filler | 2,3 (kamigata) | P2 | Kamigata signature detail [PLAYBOOK §3]; no pre-1750 image found | size_m 1.82 x 0.50, seat 0.42 (assumed) | boards: `jp_m_wood_street_dark` -> timber_street_dark | post: hinged on the facade between two posts, under a lattice window | `_down` static down<br>`_up` static folded |
| 44 | `jp_p_open_upper_rail` | Upper-floor front rail (tesuri) for inns and tea houses | A low plain wooden rail along an upper-floor opening or veranda of an inn or tea house. | standard | 2,3 | P2 | Railed tea-house rooms in prints of 1726 and c.1748 [x30, x31] | rail_height_m 0.60 visible (assumed); baluster_m 0.03 square at 0.12 (assumed); geometry_blocker_m 1.00 (assumed) | rail: `jp_m_wood_weathered` -> timber_weathered | post: between upper-floor posts at the upper floor level | `_plain` plain verticals |
| 45 | `jp_p_open_mushiro` | Hung straw mat door (mushiro, rolled up) | The poorest doorway closure: a straw mat hung over an opening, shown rolled up. | filler | 1 (rural) | P3 | T1 doors include hung mushiro [PLAYBOOK §2.1] | roll_m d 0.15 x 0.91-1.82 (assumed) | mat: `jp_m_straw_mushiro` -> thatch_new | head: hangs from the head rail above an open bay; no collision | `_rolled` rolled up, static |

## Foundations and other

| # | ID | Name | What and where | Imp. | Tier | Pri | Period evidence | Key dimensions | Materials (library -> palette) | Connectors | Variants |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 46 | `jp_p_found_soseki` | Foundation stones (soseki, ishiba-date) | Individual rounded field stones under each post of rural houses and verandas. | hero | 1,2 | P1 | Rural posts on single stones [PLAYBOOK §6.4]; Morse foundation stone [x10] | stone_m 0.30-0.50 across, 0.15-0.30 tall (assumed); exposed_m 0.05-0.20 [PLAYBOOK §6.4]; shapes 8 distinct (assumed) | stone: `jp_m_stone_field` -> stone_granite | post: one per post node, top at post base; buried to grade - exposed height | `_set8` 8 shapes<br>`_mossy` north-side moss (W6) |
| 47 | `jp_p_found_dodai_stones` | Sill on a course of individual stones (dodai + ishi) | Town-house base: a timber sill on a low course of separate cut stones with irregular joints. | hero | 2,3 | P1 | PLAYBOOK §6.4 (rule 3); Ioka base [x01] | stone_m 0.30-0.60 long x 0.25-0.35 deep; 0.10-0.20 showing (assumed); joint_m 0.005-0.02 irregular (assumed); sill_m 0.12 x 0.12 [PLAYBOOK §4] | stones: `jp_m_stone_cut` -> stone_granite<br>sill: `jp_m_wood_weathered` -> timber_weathered | sill: dodai top = finished grade + stone height; posts stand on it<br>runs any half-ken length; stone joints never align with posts on purpose | `_rough` roughly dressed, T2<br>`_dressed` better dressed, T3 |
| 48 | `jp_p_found_kura_footing` | Kura footing course (cut granite) | The 0.3-0.6 m cut-stone footing under kura walls, in individual blocks. | standard | 2,3 | P1 | PLAYBOOK §6.4 | height_m 0.30-0.60 (1-2 courses) [PLAYBOOK §6.4]; block_m 0.6-0.9 long (assumed); projection_m 0.05-0.10 beyond the wall (assumed) | stone: `jp_m_stone_cut` -> stone_granite | sill: under the okabe wall; grade to wall bottom | `_c1` one course<br>`_c2` two courses |
| 49 | `jp_p_found_yukashita` | Under-floor zone (raised floor gap, tsuka posts) | The dark ventilated gap under raised floors and verandas, open or closed by boards. | standard | 1,2,3 | P1 | Raised floors on short posts over small stones [PLAYBOOK §6.4, T17] | floor_m +0.50 above grade (doma +0.05, step +0.45) [PLAYBOOK §4]; tsuka_m 0.09 square on small stones at 0.91 (assumed) | posts, boards: `jp_m_wood_weathered` -> timber_weathered<br>stones: `jp_m_stone_field` -> stone_granite | floor: under every raised-floor edge that faces outside | `_open` open dark gap (T1-2, verandas)<br>`_boarded` vertical boards with vent gaps (T2-3) |
| 50 | `jp_p_found_step` | Entrance stones and steps (kutsunugi-ishi, threshold stone, veranda step) | The stones and steps at doors and verandas that also hide the walk ramps. | standard | 1,2,3 | P1 | B spike; Morse steps to verandah (fig. 179) | kutsunugi_m 0.60 x 0.40 x 0.15-0.20 [B spike]; step_rise_m 0.15-0.18 (assumed); tread_m 0.30-0.40 (assumed); ramp_deg <=34 hidden under the stone [PLAYBOOK §4] | stone: `jp_m_stone_field` -> stone_granite<br>cut stone: `jp_m_stone_cut` -> stone_granite<br>wood step: `jp_m_wood_weathered` -> timber_weathered | sill: at door sills and veranda edges; ramp in Geometry/Roadway | `_natural` natural slab<br>`_cut` cut slab<br>`_wood` wooden step box at a veranda |
| 51 | `jp_p_porch_engawa` | Veranda (engawa) | The raised board veranda along garden and yard sides of better houses, closed by amado. | standard | 2,3 | P1 | Engawa on T2-3 [PLAYBOOK §10.3]; railed tea-house engawa in 1726 and c.1748 prints [x30, x31] | width_clear_m >=1.00 (1.00-1.20) [PLAYBOOK §4 (reason)]; height_m 0.5 [PLAYBOOK §4]; edge_beam_m 0.09 x 0.15 (assumed); boards kure-en: boards along the wall inside the amado line; kiri-en: boards across, exposed (assumed) | boards: `jp_m_wood_weathered` -> timber_weathered | floor: level ID of the raised floor<br>post: veranda posts on the outer line carry the eave or hisashi (Morse)<br>outer edge carries the amado groove | `_kure` lengthwise boards, inside the amado<br>`_kiri` crosswise boards, exposed |
| 52 | `jp_p_porch_nureen` | Open deck (nure-en) | A narrow unroofed board deck outside a room. | filler | 1,2,3 | P3 | assumed common; no dated source gathered | width_m 0.45-0.60 (assumed); height_m 0.45 (assumed) | boards: `jp_m_wood_weathered` -> timber_weathered | floor: against a raised-floor edge | `_std` plain |

## Notes per entry (only where the table is not enough)

**`jp_p_roof_forms`**
- **Banned tells to watch:** kawara as a flat textured plane; chimneys, dormers, metal; Chinese upturned corners; curb (mansard) roofs: Morse says never seen
- **Deviations / rules used:** Tier and region rules: T1 thatch or ishioki, never tile; T2 ishioki/board/thatch, tile only on kura and big inns; T3 Kamigata sangawara, T3 Edo about half board (see kakigara decision) and half new sangawara (PLAYBOOK §2.1, E09)
- **Open questions:** Decision 6: thatch eave height versus the 2.20 m soffit rule
- **LOD:** roof share of the building budget: machiya roof <=3k faces LOD0 (PLAYBOOK §6.1)

**`jp_p_roof_eave_soffit`**
- **Banned tells to watch:** flat untextured soffit at LOD0; painted white timber
- **LOD:** LOD0 every rafter; LOD1 every 2nd; LOD2 flat textured soffit

**`jp_p_roof_sangawara_field`**
- **Banned tells to watch:** flat textured plane; identical rows (no W8 variation); glazed or coloured tiles
- **LOD:** <=3k faces for a machiya roof incl. ridge and ends; LOD1 2 segments/column; LOD2 plane

**`jp_p_roof_sangawara_eave`**
- **Banned tells to watch:** family crests of status on commoner eaves; the Tokugawa crest (Morse: rarely seen)
- **Open questions:** Straight-cut ichimonji eave tiles are common in Kyoto today; their first date is unverified, so they are not listed

**`jp_p_roof_kawara_ridge`**
- **Banned tells to watch:** plaster wave reliefs (Morse saw them on big fire-proof buildings of the 1880s; not on 1730 commoner houses)

**`jp_p_roof_onigawara`**
- **Banned tells to watch:** demon faces and crests of temple scale on commoner houses

**`jp_p_roof_ishioki_field`**
- **Banned tells to watch:** pitch steeper than 3.5 sun; uniform brown boards (they weather silver-grey, x04)
- **LOD:** courses as geometry steps only within 3 rows of the eave and ridge (as kawara); rest normal map

**`jp_p_roof_ishioki_battens`**
- **LOD:** stones: LOD0 ~20 faces each, LOD1 merged lumps, LOD2 texture only

**`jp_p_roof_itabuki_field`**
- **Banned tells to watch:** temple-style thick curved kokera on houses (PLAYBOOK §6.1)
- **Open questions:** Decision 3: kakigara-buki for Edo T3

**`jp_p_roof_thatch_body`**
- **Banned tells to watch:** thin flat thatch plane; clean uniform colour: north slopes carry moss (W6)
- **LOD:** LOD0 surface undulation low; cut edge 2-3 steps; LOD2 single shell

**`jp_p_roof_kemuridashi`**
- **Banned tells to watch:** chimneys, stove pipes

**`jp_p_roof_hafu`**
- **Banned tells to watch:** kengyo (hanging gable ornament) on commoner houses (status); painted boards

**`jp_p_roof_hisashi`**
- **Banned tells to watch:** metal flashing; thick heavy fascia
- **Open questions:** Decision 6: the _skirt pent is also the period-correct way to keep a thatch house entrance above 2.20 m

**`jp_p_roof_kura_eave`**
- **Open questions:** Oki-yane (detached kura roof): date and region not checked; do not build before verified

**`jp_p_roof_gutter`**
- **Banned tells to watch:** metal gutters (PLAYBOOK §7)

**`jp_p_wall_shinkabe`**
- **Banned tells to watch:** pure-white untextured plaster; any blank plane > 2 x 2 m; bright ochre (see requested palette entry earth_wall_aged)
- **Deviations / rules used:** D2/D6 raise openings; the kokabe band absorbs the difference

**`jp_p_wall_okabe`**
- **Banned tells to watch:** glowing white: author the mean at <=192, houses default _w1

**`jp_p_wall_board_vertical`**
- **Banned tells to watch:** identical repeated boards (W8); perfectly straight new timber

**`jp_p_wall_shitami`**
- **Banned tells to watch:** kuro_board on ordinary houses (restricted: official, kura)

**`jp_p_wall_namako`**
- **Banned tells to watch:** flat texture only: joints are geometry at LOD0

**`jp_p_wall_gable`**
- **Banned tells to watch:** a flat plain gable (machiya v1 mistake)

**`jp_p_frame_post`**
- **Banned tells to watch:** perfectly straight new timber on old buildings

**`jp_p_frame_dashigeta`**
- **Open questions:** Decision 4: build only if a pre-1750 source is found or Stephen accepts it as a deviation

**`jp_p_open_itado`**
- **Banned tells to watch:** hinged doors, knobs, butt hinges
- **Deviations / rules used:** D1; D2; D9
- **Open questions:** Engine: translation door, one bone per leaf, memory axis exactly 1.00 m, doorWoodSlide sounds (PLAYBOOK §6.3)

**`jp_p_open_koshido`**
- **Open questions:** Engine: translation door, one bone per leaf, memory axis exactly 1.00 m, doorWoodSlide sounds (PLAYBOOK §6.3); Fire Geometry wood

**`jp_p_open_shoji_ext`**
- **Banned tells to watch:** glass panes; pure white paper
- **Open questions:** Engine: translation door, one bone per leaf, memory axis exactly 1.00 m, doorWoodSlide sounds (PLAYBOOK §6.3); Fire Geometry fabric_thin (bullets pass)

**`jp_p_open_amado`**
- **Open questions:** Gameplay: amado are static, not doors (a run of 6-10 leaves would be 6-10 door bones)

**`jp_p_open_kura_door`**
- **Open questions:** Engine: hinged rotation doors are untested in this kit

**`jp_p_open_mushiko`**
- **Banned tells to watch:** large rectangular mushiko (Meiji form); see-through: View Geometry closed, Fire Geometry dirt

**`jp_p_open_koshi`**
- **Banned tells to watch:** bengara outside Kamigata T2-3; glass behind the lattice

**`jp_p_open_suriagedo`**
- **Open questions:** Engine: a vertical translation door is untested; fall back to static states

**`jp_p_open_battari`**
- **Open questions:** Catalogue lists it as street furniture (S); moved to the shell because it hinges on the facade. First date unverified

**`jp_p_open_upper_rail`**
- **Banned tells to watch:** Western turned balusters, balconies
- **Open questions:** Decision 5: full-height upper storeys on T2 hatago

**`jp_p_found_soseki`**
- **Banned tells to watch:** continuous smooth plinth (rule 3); cement mortar

**`jp_p_found_dodai_stones`**
- **Banned tells to watch:** continuous smooth plinth; uniform block courses

**`jp_p_found_step`**
- **Banned tells to watch:** poured-looking steps

**`jp_p_porch_engawa`**
- **Deviations / rules used:** D5 (>=1.00 clear)

## Engine and gameplay notes (all parts)

- **Doors:** every sliding leaf follows B's convention: `type="translation"`, one bone per leaf, a memory axis of
  exactly 1.00 m, and `doorWoodSlide` sounds. Heads are at 2.00 (D2). Clear widths are >=0.80 inside and >=1.00 at
  main entrances (D1). The kuguri wicket is decorative only (D9).
- **Static by design:** amado runs, shitomido and battari-shogi come as static open or closed variants.
  Suriage-do is static first; a vertical-translation door is an engine test.
- **Hinged:** only the kura outer leaves are hinged. They ship static open in P1; rotation doors come in P2 after an
  engine test.
- **Sealed lofts:** low upper storeys (zushi-nikai) are sealed by default (G0 decision 4). Mushiko are closed in View
  Geometry, so nobody sees or shoots into a sealed loft.
- **Fire Geometry:** plaster and earth use `dirt`, timber and bamboo `wood`, tile and namako `pottery`, thatch
  `hay`, paper `fabric_thin`, stone `granite`, iron `iron`. All are vanilla penetration rvmats.
- **Soffits:** keep >=2.20 m under any walked eave (PLAYBOOK §4). The thatch eave is decision 6.
- **LOD:** roof geometry detail only within 3 rows of the eave and ridge. Stones and battens are merged at LOD1 and
  become texture at LOD2. Lattice becomes a panel at LOD1 (B spike). Building budgets are in PLAYBOOK §12.
- **Grid:** walls are recipes over any run of half-ken bays. Fixed details come in 0.5, 1, 1.5 and 2 ken widths
  between post connectors. Roofs are generated from any footprint on the ken grid, with kawara columns at ken/7
  (PLAYBOOK §10.2).

## Materials the materials agent must make (22 materials, 66 texture sets)

| Material | Family | Palette ID | Tile (m) | px/m | Fire | _w0 / _w1 / _w2 | Used by |
|---|---|---|---|---|---|---|---|
| `jp_m_wood_weathered` | wood | timber_weathered | 2.0 | 512 | wood | warm brown, crisp grain / sun faces silvering (W3), grime band (W1) / grey toward stone_lantern (max 0.35), splits, heavy grime | 25 parts |
| `jp_m_wood_street_dark` | wood | timber_street_dark | 2.0 | 512 | wood | oiled dark brown / edge wear on lattice corners (W7) / dusty, raised grain, pale edge wear | 10 parts |
| `jp_m_wood_bengara` | paint | bengara_lattice | 2.0 | 512 | wood | even red-brown / worn to wood on edges / patchy, wood showing | 1 parts |
| `jp_m_wood_kuro` | wood | kuro_board | 2.0 | 512 | wood | matte black / grey bloom / grey, wood showing on edges | 1 parts |
| `jp_m_wood_sooted` | wood | timber_sooted | 2.0 | 512 | wood | dark brown-black, albedo >=30 / soot streaks / crusted soot | 1 parts |
| `jp_m_wall_arakabe` | wall | earth_wall_aged **(new)** | 2.0 | 512 | dirt | fresh clay, straw visible / rain streaks (W2), splash band (W1) / eroded, straw and lath showing in patches | 2 parts |
| `jp_m_wall_nakanuri` | wall | earth_wall_aged **(new)** | 2.0 | 512 | dirt | smooth clay / streaks, splash / cracks, patched areas | 1 parts |
| `jp_m_wall_shikkui` | wall | shikkui_white | 2.0 | 512 | dirt | clean lime, mean <=192 (never 217) / default on houses: grey streaks under eaves and sills / toward earth_wall_ochre (max 0.25), grime band, hairline cracks | 11 parts |
| `jp_m_wall_namako_tile` | wall | namako_tile | 0.91 | 512 | pottery | dark even tile / lime wash drips / chipped tiles, stained joints | 1 parts |
| `jp_m_roof_kawara` | roof | kawara_ibushi | 2.0 | 256 | pottery | silver-grey ibushi / darker, per-tile tint (W8) / toward kawara_weathered, lichen on north (W6) | 12 parts |
| `jp_m_roof_thatch` | roof | thatch_weathered | 2.0 | 256 | hay | thatch_new golden (recent re-thatch, 1 in 10) / grey-brown / dark, moss on north slopes (W6), sagging patches | 3 parts |
| `jp_m_roof_thatch_cut` | roof | thatch_weathered | 1.0 | 512 | hay | fresh cut, light / 2-3 light/dark layer bands (Morse) / ragged, dark | 1 parts |
| `jp_m_roof_kureita` | roof | roof_board_silver **(new)** | 2.0 | 256 | wood | pale new wood (rare) / silver-grey / dark grey, moss, lifted boards | 3 parts |
| `jp_m_roof_kokera` | roof | roof_board_silver **(new)** | 2.0 | 256 | wood | pale / silver-grey / curled, dark | 1 parts |
| `jp_m_roof_kakigara` | roof | kakigara_shell **(new)** | 2.0 | 256 | wood | pale shells / grey shells, dirt / sparse shells, moss | 1 parts |
| `jp_m_stone_field` | stone | stone_granite | 1.0 | 512 | granite | clean / splash band, lichen spots / moss (W6) | 3 parts |
| `jp_m_stone_cut` | stone | stone_granite | 1.0 | 512 | granite | crisp tool marks / rounded arrises, grime / moss in joints | 3 parts |
| `jp_m_stone_river` | stone | stone_lantern | 1.0 | 256 | granite | grey cobbles / lichen / moss | 3 parts |
| `jp_m_paper_shoji` | paper | washi_shoji | 1.0 | 512 | fabric_thin | clean warm white / yellowed, patched squares / torn squares, stains | 1 parts |
| `jp_m_bamboo_weathered` | bamboo | bamboo_weathered | 1.0 | 512 | wood | pale / grey-beige / split, dark | 5 parts |
| `jp_m_metal_iron` | metal | iron_black | 0.5 | 512 | iron | dark iron / rust bloom / rust streaks on plaster below | 5 parts |
| `jp_m_straw_mushiro` | straw | thatch_new | 1.0 | 512 | hay | golden / grey-gold / dark, frayed | 1 parts |

## Requested new materials or palette entries

| Palette ID | sRGB | Method | Why | Sample source |
|---|---|---|---|---|
| earth_wall_aged | [115, 98, 80] | sampled | Exterior earth walls of surviving 17th-18th c. farmhouses are grey-brown, not the sunlit ochre of c29 (215,180,115). The v1 walls read too bright; vanilla white walls sit at ~150. | x08_hirose_earthwall box [0.2, 0.52, 0.29, 0.64] -> [116, 100, 80], x08_hirose_earthwall box [0.52, 0.64, 0.64, 0.74] -> [114, 96, 79] |
| roof_board_silver | [123, 128, 134] | sampled | Weathered roof boards go silver-grey; timber_weathered (118,82,73) is the brown of wet facade boards and is wrong for roofs. | x04_misawa_a box [0.25, 0.22, 0.55, 0.3] -> [123, 128, 134] |
| kakigara_shell | [172, 168, 158] | assumed | Only if decision 3 (Edo oyster-shell board roofs) is yes. | needs a licensed sample of weathered oyster shells |

## Checks the builder must run

- C1-C5, C8 and C9 on every part (PLAYBOOK §12); C3 grid snap is the one that makes "any wall fits any post spacing" true.
- C8 specials: kawara LOD0 corrugation density; ishioki and thatch eave edges modelled (not flat); plinth and soseki made of separate stones; no rectangular mushiko; no bengara or kuro_board outside their tiers.
- C1: shikkui mean must be <=192 (the v1 machiya plaster was about 217).

## Later (out of scope for this list)

- **Temples and shrines (stage R):** hongawara temple roofs with a 7-course ridge, curved kokera and bark roofs,
  shu vermilion, torii, halls, gates and bell towers.
- **Government, status and castle:** honjin (gate, shikidai genkan, jodan-no-ma), toiyaba, sekisho, jinya,
  bugyosho, bansho, kido and kidoban, fire towers, samurai nagaya-mon and yashiki, castle walls and keeps.
  They reuse these parts, plus kuro_board and status features that are banned for commoners.
- **Street dressing (stage S):** noren, kanban, chochin, andon signs, sudare, yoshizu, inuyarai, komayose,
  tensuioke with buckets, benches, carts and seasonal dressing.
- **Gardens and site sets (stage S):** fences, hedges, tsuijibei and neribei walls, gates, wells, tsubo-niwa,
  stepping stones, drying racks, stone lanterns and yards.
- **Interiors (stage D):** fusuma, interior shoji, ceilings, tatami layouts, stairs and furniture proxies.
- **Unverified or rejected for 1730:** rectangular mushiko (Meiji), dashigeta (decision 4), kura oki-yane (date
  and region not checked), ichimonji eave tiles (date not checked), plaster wave reliefs on ridges (1880s), and
  Morse's stone-slab kura roofs (Shimotsuke, outside the map region).
- **Housekeeping:** `playbook/refs_index.json` labels `c14_minkaen_b` as an Edo farmhouse. It is the museum's
  modern main building. Its kawara colour sample is still usable, but don't use it to date anything.

