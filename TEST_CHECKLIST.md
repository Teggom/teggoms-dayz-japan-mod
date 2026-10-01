# Japan test island: the re-check after the showcase walk (~15 min)

Everything you flagged on the showcase walk, fixed, in one short loop. Two agents worked on it: **FB1** (buildings,
doors, placements) and **FP1** (props and materials).

**Start:**
1. Run `start-japan-test-island.bat` in the server folder. It starts only the test server, on its own port.
2. When the server is up, run `start-japan-test-client.bat` to join.
3. Keep the labelled maps open: `research/production/contact_sheets/sh1_map_street.jpg`, `sh1_map_shrine.jpg`,
   `sh1_map_gallery.jpg` (IDs as before; the full table is `spikes/SH1/SHOWCASE_MAP.md`).

**If it won't load, kicks you, or something is invisible:** just tell me. I read the server and client logs myself.

**The route:** gallery (east) -> machiya -> town street -> shrine + hill stair -> hamlet -> back. ~700 m.

## 1. Doors (4 min) — the big one

**Why none opened:** 97 of the 128 building classes didn't match their model file names (e.g. class `..._2ken_...`,
file `..._2k_...`). The game drew those houses but never connected them to their class, so they had no doors and no
loot. Every model file is now named after its class, and a new check fails the build if they ever drift apart again.
The machiya shop and the outhouse were already correct; nothing else was found wrong with the doors themselves.

Try these, in this order (open AND close each, from both sides):
1. **The machiya shop** (straight north of the spawn): the front door. It worked at G4; it should still work.
2. **The rice dealer C-a** on the street (Kamigata row, north side): the front sliding door, then the inner doors.
3. **The tailor D5** (Edo row, the middle of the five east of the first torii S01) and **the apothecary D4**.
4. **The grand inn C-i:** front door, the back-room door, then upstairs.
5. **The hamlet:** the **Kanto farmhouse's** big plank door; the **Kinai farmhouse's** front door; the **kura**'s
   hinged plaster leaves (they start open: close both, open them again) and its inner sliding door.
6. **The outhouse** behind the machiya: the half door.

**Loot:** with the classes connected, loot should now spawn on floors and on furniture in every house (it didn't
before, except in the machiya). Glance into two or three houses.

## 2. The gallery (3 min) — FP1's prop fixes (map `sh1_map_gallery.jpg`)

Walk ~65 m north-east from the spawn to the three open sheds. Pictures of every fix, before | after:
`research/production/contact_sheets/fp1_fixes.jpg`.

- **Broom L55** (back row, with the leaf pile): a real bamboo broom now (handle with nodes, bound twig fan).
- **Rice sheaves L51** (rice rack, back row west): sheaves hung astride the rail, ears down, golden.
- **Potted plants L58:** pine, azalea and chrysanthemum in unglazed pots (the pot and flower colours are guesses:
  say if they're off).
- **Sword rack L45** (shed 3): curved swords in lacquered scabbards, round guards, cords.
- **Fallen lantern L72:** you can see into its open end; no clear sheet under it.
- **Loom L38 and spinning wheel L37** (shed 3): nothing floating? (FP1 fixed the loom's loose parts; it found no
  fault in the wheel - if it still floats, say where.)
- **Bale ends** (L25 on the shed 1 floor, L57 against shed 1's west wall): closed, not see-through.
- **Leaf litter** on the shed floors and in the street: leaf shapes, not dots.

## 3. The town street (2 min)

- **D5, the "house without a roof":** stand in the street in front of the five Edo houses east of the first torii
  (D4, D1, **D5**, C-c, C-d). FB1 could not find a missing roof on any house there: D5's roof is in every model LOD and
  faces the right way. D5 is the only board-roofed (pale silver shingle) house between tiled roofs, and its roof sits
  0.17 m lower, so from the street it can read like sky. **Is it D5? Does it still look roofless? If yes, a screenshot
  from where you stand, please** (and I'll take it from there).
- **Fire-watch ladder** (the ward corner, ~1033, 1087, ladder facing the street): look at the ladder -> **Enter
  ladder**, climb to the railed deck by the bell, step off; then climb back down. (New: it's now a real ladder.)
- **Notice board** (ward corner, ~1017, 1088): boards hang on rails, the roof sits on rafters and braces.
- **Potted plants** outside the west-end house (~985, 1076) and the **fallen lantern** in the street (~1006, 1081).

## 4. The shrine and the hill stair (3 min) — map `sh1_map_shrine.jpg`

- **The hill stair torii:** the torii at the foot (S63) and at the top (S70) of the hill stair are now the large
  stone torii (2.6 m and 2.8 m clear underneath; the old medium ones gave 1.7 / 1.8 m). **Walk up and back down
  under S70 standing.** The basin S74 moved half a metre east to make room.
- **Stone torii texture:** S01 (and the stone lanterns): no repeating dots any more.
- **Torii ropes:** the twisted straw ropes on S14, S22 and the rope torii of the sub-shrine row (S41, S42 ...); the
  vermilion leaning torii S82's rope now hangs snapped.
- **Collapsed torii (new):** S100 stone, felled by the 1707 quake (behind the sub-shrine row), S101 an old mossy one
  half sunk (west of the approach, north of the graveyard), S102 a wooden myojin blown over by a typhoon (west of
  the approach), S103 a shinmei fallen with its feet rotted (east, in the trees), S104 a vermilion one snapped at the
  posts (below the Inari path). The three wooden ones lie partly in the slope (0.3-0.4 m on their uphill side).
  **Do they read as old wrecks? Any floating?**

## 5. The hamlet (3 min)

- **Kinai farmhouse (the tall house with the tiled lower roofs):** the "thick thing under the roof" was the white
  plastered gable (takahe) hanging down under each eave corner as a block, with the thatch ridge poking over and out
  of it. Now the white gable runs along the roof edge and stands just above the thatch and its ridge. **Does the
  gable end look right now, from the yard and from the side?**
- **Kanto farmhouse:** the farm tools by the big door now lean on the wall (they stood half a metre off), and the
  charcoal bales stand against the back wall. Same for the tools by the Kinai house's door.
- **The hamlet kura:** the plaster door leaves are now 13.5 cm thick (were 19 cm) and the window shutters 8 cm (were
  12 cm), closer to a small country kura; all its outside plaster is the new **aged plaster** (warmer, greyer, rain
  streaks), and the town kura behind the Kamigata row too. **Thickness and colour right now?**
- **Lever well** (by the huts, ~955, 1001): the counterweight stone hangs low in a rope sling, the bucket above the
  curb; crouch: Drink and fill a bottle still work?
- **Straw stack** in front of the hamlet kura (~970, 1036): one even texture (no grey bands).
- **Charcoal bales** behind the Kanto farmhouse and at the hamlet's east edge (~968, 1042): ends closed.
- **Broom and rice stooks/racks** in the yard (~947, 1008 and ~974, 1012).

## Tell me

1. **Doors:** which of the buildings in section 1 open and close? Any that don't (which door)?
2. **Loot:** does it show up inside the houses now?
3. **D5 / the roofless house:** still roofless? Which house (or a screenshot)?
4. **Hill stair torii S70:** clear walking down?
5. **Kinai gable, kura thickness and colour, tools on the walls:** right now?
6. FP1's items (sections 2-5): which are fixed, which still look wrong (IDs)?
7. Anything new that looks wrong.
