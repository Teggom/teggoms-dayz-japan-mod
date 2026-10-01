# W2S notes: shrine + temple shells, village and town grades (agent W2S, 2026-10-01)

Research-first record for the shells built by `parts/kit/jpparts/templates/sacred.py` (registry block W2S_*).
No web access in this run and no photos of shrine or temple halls on this machine (the local refs are lanterns,
basins, torii, steps, trees), so:
- **[R]** = in-repo sources: research/buildings/BUILDING_LIST.md (Shinto §"Buildings inside a shrine precinct",
  Buddhist §"Temples by scale" / §"Buildings in a temple precinct"), research/catalogue/KEEP_CIVIC.md (the shrine and
  temple ladders), research/production/PARTS_GAP_AUDIT.md rows SH2-SH6, BU1-BU8, parts/W2P1_NOTES.md,
  parts/W2P2_NOTES.md, PLAYBOOK §1 / §4 / §6 / §12 / §15.
- **(GK)** = general knowledge of standard Japanese shrine / temple architecture (textbook forms and the JAANUS
  dictionary terms), not checked against a source in this run. Every (GK) proportion is an assumption a later agent with
  web access should confirm.

The **1730 test** (PLAYBOOK §1: "did it exist, or still stand, in 1730") is answered per building below. Every form
used here is medieval or older and was still being built in the Edo period, so all pass; the notes say where a detail
would NOT pass.

## Game standards that override period sizes (PLAYBOOK §4 / §5, as W2P1)
- Door head 2.00 m, clear 1.00 m min (D1 / D2): period shrine doors are smaller. Honden tobira are built at the D1 size
  but SEALED (static, closed; see 2).
- Stairs (kizahashi) at <= 38 deg (D4), 1.10 m between the rails; en (veranda) >= 1.00 m clear (D5, 1.365 m deck).
- Head room >= 2.10 over every walkable floor (C7), so eaves over an en sit higher than on small period halls.

## Grades
| Grade | Shrine | Temple | Roof | Frame |
|---|---|---|---|---|
| village | straight kokera / board roofs (W2P1), plain koran, bays of 1 ken (1.82) | straight sangawara / board / thatch | `roofs.roof`, `nagare.nagare/hogyo/kohai` | posts + keta, no brackets (funa at most) |
| town | curved hiwada / copper / hongawara (W2P2 `sori.roof`), giboshi koran, bays of 7.5 shaku (2.275) | curved hongawara | `sori.roof` (+ `sori.kohai_fit` for the step canopy) | `kumimono.frame` (mitsudo / degumi / mitesaki) |

## SHINTO

### 1. Worship hall (haiden) [R BUILDING_LIST "Worship hall"; KEEP_CIVIC Shinto 2; audit SH2]
- **Period form:** an open-fronted board-floored hall in front of the honden, usually wider than deep (hirairi: the
  entrance on the long side), raised on a low floor with a front en, rail and steps; the front bays have lattice doors or
  shitomido, the middle bay is the worship bay (bell rope + offering box in front of it). Some have an earth passage
  through the middle (wari-haiden). Village haiden: kirizuma or irimoya, board / bark roof, plain posts on stones.
  Town haiden: irimoya with a curved roof, bracket sets, a kohai step canopy, often cypress-bark or copper roofs.
- **Proportions (GK):** 3 x 2 bays is the common small haiden; floor 0.5-0.9 m up; eave 3-3.5 m.
- **Choices:** village 3 x 2 ken (5.46 x 3.64), floor +0.60 on the boarded `stilts.platform('hall')`, kirizuma kokera
  (W2P1's assembly), lattice tobira in the middle bay (opens in), fixed lattice fronts in the side bays, front en with
  plain koran + kizahashi, board kohai. Town 3 x 2 bays of 2.275 (6.83 x 4.55), floor +0.75, en on three sides with
  giboshi koran, curved irimoya (hiwada; a copper variant), hira-mitsudo bracket sets, middle-bay lattice tobira +
  hinged shitomido in the side bays, curved-roof kohai via `sori.kohai_fit`. Wari-haiden: NOT built (a passage needs a
  split floor + two extra stairs; the furnisher can read a 3-bay haiden as one).
- **1730:** in. Haiden as separate halls are medieval (GK); Edo village shrines added them when the village could afford
  one [R: "+ haiden if rich"].

### 2. Main sanctuary (honden) [R BUILDING_LIST "Main sanctuary"; audit SH3; W2P1 tobira / nagare / ornament / stilts]
- **Period form:** a small closed sanctuary raised on posts (floor ~1 m), en round three sides with a rail, wakishoji
  closing the side en at the rear, a stair (kizahashi) at the front under a kohai; closed doors with metal fittings;
  nobody but the priest goes in. Styles [R]: nagare (the commonest by far: the front slope runs on over the steps),
  shinmei (straight gable, hirairi, chigi + katsuogi, the ridge posts munamochi-bashira standing free at the gable
  ends, unpainted), kasuga (tsumairi: gable-entry 1 x 1 ken with a kohai, painted vermilion).
- **Proportions (GK):** issha (1 x 1 ken) is the village norm; sangen-sha (3 x 1/2 ken) for larger shrines.
- **Choices:**
  - SEALED: the tobira are built closed and static (no door action), so no player enters the sanctum (Stephen's
    brief: "honden sealed, can see through the tobira lattice"); the sanctum is a closed box with a board floor and an
    inner wall finish, not a walkable room. The en is the walkable floor (loot points on it).
  - nagare village: 1 x 1 ken, floor +1.00, straight nagare kokera (W2P1 assembly), giboshi koran, board tobira.
    Variant `_Chigi`: okichigi (soto) + 3 katsuogi as a swap (W2P1 note: on a nagare honden a swap, not the default).
  - nagare town: 3 x 1 ken sangen-sha with lattice tobira in all three bays, curved nagare hiwada (`curve=sori.nagare`).
  - shinmei: 1 x 1 ken, straight kirizuma kokera, munamochi-bashira at both gables, okichigi (uchi or soto) + katsuogi,
    koran round four sides, board tobira.
  - kasuga: see the progress file (built only if cheap).
- **1730:** in. All three styles are ancient; Ise was rebuilt in 1729 [R].

### 3. Purification pavilion (temizuya / chozuya) [R "four-post roof over a stone basin fed by a bamboo pipe"; audit SH5]
- **Period form:** four posts (often splayed inward at the top on grander ones) carrying a gable roof over the stone
  basin; paved floor; ladle rack (hishaku) on the basin. Village: board roof; town: tile or curved roof with simple
  brackets.
- **Choices:** 1 x 1.5 ken (1.82 x 2.73), posts on stones, a cut-stone paved pad with the basin SPOT left empty in the
  middle (the basin is a W2 site prop: `jp_s_basin_*`), village kirizuma kokera, town curved kirizuma hongawara on
  funa-hijiki. Posts plumb (the splay would need a non-axis post solid; not worth it here).
- **1730:** in.

### 4. Priests' office + amulet window (shamusho) [R "Priests' residence and office" + "Talisman / amulet window (juyo-sho)"]
- **Period form:** in 1730 amulets were sold from the priest's house or a small booth at the haiden; a separate juyo-sho
  is mostly modern (assumed [R]). So the shell is a small house-office: an earth-floored entry and a raised board office
  room whose front has a counter window (push-up shutter) where ofuda / omamori were handed out.
- **Choices:** 3 x 2 ken, doma 1 ken by the door, raised board office (0.40) with the counter shutter on the front,
  kirizuma sangawara (town) / itabuki (village), board or plastered walls. The "office" + "amulet window" are prop spots.
- **1730:** in as a priest's office in a house form; the separate amulet-window building would not be (so it is not built
  as one).

### 5. Kagura dance stage (kagura-den) [R "raised square stage open on 3-4 sides, board floor, dressing room behind"]
- **Choices:** 2 x 2 ken stage at +1.00 on the open `stilts.platform('honden')`, open on three sides, a board back wall
  (the dressing-room side), koran on the three open edges, a kizahashi at the back (the performers' side), irimoya
  roof: straight kokera (village) / curved kokera on funa-hijiki (town).
- **1730:** in (kagura stages at town shrines [R]).

## BUDDHIST

### 6. Small sacred hall (do) [R "Unstaffed hall (do / dosho)": 2 x 2 or 3 x 3 ken, one room, board floor, raised altar at the back, veranda; also the village meeting place]
- **Period form:** a square one-room hall under a pyramid (hogyo) roof with a finial (hoju), front lattice doors, a
  front en with a rail and steps.
- **Choices:** village 2 x 2 ken board hogyo (lattice tobira in both front bays), 2 x 2 ken THATCH hogyo (rural Kannon /
  Koshin halls), 3 x 3 ken straight sangawara (W2P1's temple hall: sankarado + hinged shitomido); town 3 x 3 bays of
  2.275 curved hogyo (copper) on oto-hijiki (daito + arm) brackets. Altar dais spot at the back wall.
- **1730:** in.

### 7. Main hall (hondo) [R "Main hall": inner sanctum (naijin) with raised altar dais, outer worship space (gejin)]
- **Period form:** village temples: a 4 x 4 to 6 x 6 ken hall, irimoya tile (or thatch) roof, front en, the front bays
  sankarado / shitomido, the inner sanctum at the back behind a lattice screen. Town temples: the same plan under a
  curved hongawara roof on bracket sets (degumi; mitesaki only on the main hall of a large temple [W2P2 §3]).
- **Choices:** village 4 x 4 ken (7.28 square), floor +0.60, straight irimoya sangawara, front en + kizahashi + tiled
  kohai, sankarado in the two middle bays, shitomido outside. Town 3 x 3 bays of 2.275, floor +0.75, degumi, curved
  irimoya hongawara, en on three sides, curved kohai. A mitesaki variant only if the face budget allows. The naijin is
  a raised dais SPOT (shumidan) across the back third: prop spots for the furnisher, no partition (the gejin / naijin
  split is a furnishing line in a hall this size).
- **1730:** in. Sect swaps are props [R KEEP_CIVIC].

### 8. Priests' quarters + kitchen (kuri) [R "huge earth-floored kitchen with exposed beams and a smoke gable; board office; tatami living rooms; guest room"]
- **Period form:** a big house: a huge doma kitchen open to the roof frame, a smoke vent, raised board rooms and tatami
  rooms; the formal entrance (genkan, a status feature allowed for temple kuri [R audit #8]) is a projecting porch with
  a shikidai board step, separate from the doma's working door.
- **Choices:** 6 x 4 ken, doma 2.5 ken (with the kamado row spot), a board daidokoro with the irori and a tatami
  guest room behind a partition, koyagumi (sooted) in the doma, a koshiyane smoke vent. The genkan porch (W2P1 skipped
  it) stands on the rooms' gable end (under the gable, where no eave drops over it): a small kirizuma roof on two posts,
  a shikidai step and its door into the guest room. Village: thatch kirizuma; town: sangawara kirizuma.
- **1730:** in.

### 9. Bell tower (shoro) [R "open four-post pavilion (or with a flared skirt wall, hakama-goshi) on a stone platform"; W2P2 shoro]
- **Choices:** village: the open four-post type on a low stone platform, straight irimoya sangawara, the bell beam with
  a `bell_hook` memory point (bell + striker are W2F props), struck from the platform. Town: W2P2's hakama type (skirt,
  upper deck with koran, degumi corner sets, curved irimoya hongawara) with an outside stair (kizahashi) up to the deck
  so the bell can be reached (period: an inside stair or a ladder; the game needs a walkable 38 deg flight, D4).
- **Budget:** R3 of the town shoro exceeds the standard 800 (W2P2: 1,047) -> registered 'large'; a 'tower' class is a
  question for Stephen.
- **1730:** in (hakama-goshi towers Momoyama / early Edo [W2P2 GK]).

### 10. Small gate (yakui-mon / shikyaku-mon) [R audit BU5; KEEP_CIVIC Buddhist 5]
- **Period form:** yakui-mon: two main posts carrying the gable roof with two control posts behind (the roof ridge sits
  in front of the main posts' line); shikyaku-mon: one main pair + four control posts, the ridge on the main line, a
  grander temple gate. Hinged board leaves between the main posts.
- **Choices:** village yakui-mon with straight kirizuma sangawara, town shikyaku-mon with curved kirizuma hongawara on
  oto-hijiki; leaves from W2C's `gates.gate_leaves` (board, swing inward); a packed-earth threshold strip.
- **1730:** in.

## Optional (not in the core brief)
- 2-storey sanmon, 3-storey pagoda, sutra repository: see W2S_PROGRESS.md for what was done.

## Materials added (research/materials/make_w2s_materials.py)
- `jp_m_roof_hiwada` (palette `roof_hiwada`): cypress-bark roofing. Chromaticity sampled from the sunlit sugi / hinoki
  trunks of k38_shrine_steps (Kashima, CC; the bark the roofs are stripped from, 166,133,119 and 158,125,112); value
  derived darker for a laid, weathered roof of fine overlapping courses (GK: hiwada roofs read dark red-brown).
- `jp_m_roof_copper` (palette `roof_copper_patina`): aged green copper (rokusho) roof. ASSUMED (GK); the only local
  copper roof (k38, far background) is sky-lit sheen and was rejected as a sample.
- `jp_m_metal_bronze` (palette `bronze_patina`): patinated bronze (bells, giboshi caps, hoju, door fittings). ASSUMED (GK).

## Choices made while building (game / budget / check driven)
- **Village kagura stage roof = kirizuma** (straight board gable + board gables), not irimoya: roofs.roof's straight
  board irimoya leaves its hips uncovered (no hip rolls; seen in the render). Small village kagura-den with gable roofs
  are common (GK). The town stage keeps the curved irimoya.
- **Thatched do (2 x 2) has no en:** the thatch eave (45 deg, 2.88 m keta) hangs to ~1.9 m over a 1.365 m en (C7 head
  room 2.10). It gets a lattice door with a cut step and a fixed lattice front, as rural Kannon / Koshin halls often do.
- **Town halls hang their shitomido in front of the round columns** (column centre to centre, the board wall behind the
  fixed lower leaf): a top-hinged leaf between 0.25 m columns would swing through them, and between them leaves a slit
  at the jambs (C17). Doors (tobira) sit between the column faces.
- **Town hondo:** degumi (not mitesaki: 17.6k faces), the en on the FRONT only, plain koran, a copper-clad kohai (a tiled
  kohai tucked under a curved eave loses its clay bed, C13; copper kohai on tiled halls are period, GK), ridge 7
  courses, rafters at 0.30. 11,510 faces (large 12,000).
- **Shinmei honden:** front en only (the munamochi-bashira stand beside the gable walls under the verge); okichigi +
  5 katsuogi (soto: the Ise convention for a male kami).
- **Town nagare honden:** walls / keta / gables 6 cm lower than the straight kit's (the curved front slope dips under
  the straight gable pitch, C12).
- **Bell towers:** the bell beam's underside is 2.20 m over the deck / platform (C7 head room); the town tower's outside
  stair keeps its real treads and rails in every LOD (a 3.4 m flight's far slab sags 0.18 m, C15).
- **Far LODs of small curved roofs** (temizuya, gate, the shoro village roof): the far field is lifted 4 cm (R2) or
  Resolution 3 uses Resolution 2's finer field; corner lift 0.08-0.12 m on the small / square curved roofs (the default
  0.30 cannot be followed by the far LODs within C15's 0.10 m).
- **Boarded-skirt platforms** show the skirt as one slab and hide the posts / stones behind it (budget, ~1,600 faces on a
  town hall); the en's own stones stay (C8).
- **Sealed honden:** static closed tobira (no door action); the en carries the loot; the sanctum is a fitting spot.

## Prop spots for the furnisher (rooms json 'fittings', model frame; + 'bell_hook' memory point)
- haiden: saisen_bako (en), suzu (bell rope, hung over the box), drum, kamidana (back wall), gaku (town, over the door)
- honden: sanctum (behind the closed doors), offering_table (en)
- temizuya: basin (the W2 jp_s_basin_* site prop)
- shamusho: amulet_counter (behind the push-up shutter), desk, kamidana
- kagura: drum (musicians' corner), masks (back wall)
- do: altar (dais at the back wall), saisen_bako, gong (waniguchi)
- hondo: altar (naijin dais: shumidan, zushi, canopy, altar pieces), sutra_desk, saisen_bako, gong
- kuri: kamado_row + two kamado spots, irori pit + hook point, zen_trays (office corner)
- shoro: bell (bonsho on bell_hook; the striker log on ropes)
- gate: gaku (name board)
