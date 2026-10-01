# Japan test island: the second re-check (~10 min)

Your re-check findings, fixed. Two agents: **FP2** (firewood, mochi mortar, ropes) and **FB2** (flicker, the Kinai
gable, the partitions, the two-storey inn). Before / after pictures: `research/production/contact_sheets/fp2_fixes.jpg`
(props) and `spikes/FB2/renders/` (buildings).

**Start:**
1. Run `start-japan-test-island.bat` in the server folder. It starts only the test server, on its own port.
2. When the server is up, run `start-japan-test-client.bat` to join.
3. Labelled maps as before: `research/production/contact_sheets/sh1_map_street.jpg`, `sh1_map_gallery.jpg`
   (IDs in `spikes/SH1/SHOWCASE_MAP.md`).

**If it won't load, kicks you, or something is invisible:** just tell me. I read the server and client logs myself.

**The route:** town street -> town kura -> grand inn -> hamlet. ~400 m.

## 1. Flicker (3 min) — every building

**What it was:** in many places two parts were modelled in exactly the same plane (a beam face flush with a wall
face, a door sill flush with the floor), so the game couldn't decide which to draw. A new check now finds every such
pair in every building (over 100,000 of them, mostly tiny), and the build moves the smaller part a few millimetres so
it sits just in front (a sill or track just below the floor). The build fails if a pair ever comes back.

- **Town kura C-j** (behind the Kamigata row, ~1000, 1097): go up the stair and look at the back wall beside the
  stairwell rail, from above and from below. That was your grey wall with the beam flickering through it (the
  stairwell's rim beam lay in the wall's plane). **Steady now?** (The hamlet kura is the same model.)
- **Any interior doorway:** look at the bottom of a sliding door (sill, track) in two or three houses. **Steady?**
- **The rice-cake shop D3** (Kamigata row, ~1003, 1088), the board-walled corner by the mortar: the wall foot and the
  floor no longer flicker.
- Walk past anything else you remember flickering.

## 2. FP2's props (3 min)

- **Firewood** (outside the houses, the hamlet woodshed, the kitchen stacks): split billets with bark and ringed
  ends now, no flat painted ends.
- **D3, the mortar:** the mallet's head lies in the mortar's hollow with its handle on the rim; the tall pounder
  stands on the floor and leans on the rim. Nothing floating?
- **Ropes** (2.5x rounder): the rope coils on the gallery pegs, the shrine ropes (S14, S22), the lever well's ropes
  (~955, 1001), the rice-bale ties.

## 3. The grand inn C-i (2 min) (~1026, 1071)

Upstairs, in the back room by the stair rail (your screenshot C):
- The **dividing wall** now goes all the way up to the sloping ceiling boards, with a beam across it at the old top.
- **No slits** where it meets the outer walls, and no vertical gaps along it (posts were missing at its ends and
  on two frame lines, upstairs and downstairs).
- Downstairs in any town house or inn: the wall between the front shop room and the back room now meets a beam
  under the loft (there was an 8 cm slit above it).

## 4. The hamlet (2 min)

- **Kinai farmhouse (tall thatch, tiled lower roofs):** you asked if the big white band was real. It wasn't, as
  built. On a real yamato-mune house the white is the **gable wall itself**, carried up a little past the thatch
  with a narrow tile cap. It is not a thick white band laid on a brown gable. Now the whole gable above the tie beam
  is plastered (frame lines showing), the white edge stands 26 cm over the thatch all the way up with its tile cap,
  and the ridge between the two gables is slimmer. **Look from the yard and from the side: does it read right now?**
  (Still not like the real thing: real yamato-mune thatch is steeper than ours, and there is no lower kitchen roof
  on the gable end. Say if you want either.)
- **Inside the Kinai and Kanto farmhouses** (your screenshot B): the room walls now end at a **beam on their posts**.
  In the Kinai house, the wall under a big log beam goes **up into the log**. **Better?**

## Tell me

1. **Flicker:** the kura stair wall, door sills, the D3 wall foot: steady? Anywhere else still flickering?
2. **FP2:** firewood, the D3 mortar and pounder, ropes: right now?
3. **Grand inn:** does the upstairs divider meet the ceiling? Any slits left?
4. **Kinai gable:** right now? Do you want the steeper thatch or the kitchen-end lower roof?
5. **Farmhouse partitions:** right now?
6. Anything new that looks wrong.
