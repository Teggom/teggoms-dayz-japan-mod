# Japan test island: one bundled check (~25 min)

This is a **mechanics** test. Several looks are already known to be wrong: the house style, the kimono cut, and the
katana tip (being rebuilt). Those get fixed through the playbook process. Here, just tell me whether things *work*.

**Start:**
1. Run `start-japan-test-island.bat` in the server folder. It starts only the test server, on its own port, so the
   live server is unaffected.
2. When the server is up, run `start-japan-test-client.bat` to join.

**If it won't load, kicks you, or something is invisible:** just tell me. I read the server and client logs myself,
so you don't need to dig.

**Directions** are from the spawn. You spawn on a flat dirt square facing north.

## 1. First look (1 min)

- **The house** is ~55 m north. There's a sakura on each side of the path. The bamboo grove is ~70 m east. Items lie
  on the ground just south of you, and the sea is on the horizon.
- **Ground:** sharp ground textures, grass clutter off the square, trees sitting on the ground (not floating or sunk).

## 2. House (5 min)

- **Doors:** open and close a few. Try the front door (left end of the front), a paper door inside, and the one
  upstairs. **Do they slide sideways along the wall?** Or into the frame or the wrong way?
- **Walking:**
  - through the earthen passage to the back door
  - step up onto the raised rooms (the flat stones)
  - **walk up the steep stair** and back down

  Any falling through, sticking, or bouncing?
- **Loot:** anything lying on the floors? Is any of it floating or sunk?
- **The second copy** stands ~70 m north-east. Do its doors work too?

## 3. Weapons (6 min)

**The range** is ~40 m south: hay bales, 2 standing infected and a deer. There's no navmesh of our own yet; the island
borrows Livonia's as a stopgap, so they may stand still or wander oddly.

- **Katana vs the vanilla Sword:** light attack, heavy attack, kill an infected. Are the hands on the handle?
- **Yari vs SpearStone:** the same test.
- **JP_Yumi** (the long bow, held like a bow):
  1. Put the Ya (arrows) in your inventory.
  2. Raise it, press R, wait ~1 s, then fire at a hay bale.
  3. Walk up and take the arrow back.

  **Any freeze?**
- **JP_Yumi_XB** (the same bow, held like a crossbow): the same steps. Does load, fire and recover work? Can you live
  with how it looks as a fallback?

## 4. Clothes (5 min)

- **Put on** the Kasa (straw hat), the **short** kimono and the Tabi/Waraji.
- **Move:** run, crouch, go prone, raise a weapon.
  - Anything poking through?
  - Does the V at the neck show your own skin tone?
  - Is the hat rim in the way in first person?
- **Long kimono:** a quick look walking and crouching. I expect it to break when moving; I just want your verdict.
- **Optional:** repeat on a female character.

## 5. Trees and bamboo (4 min)

- **Chop a bamboo clump** with the Hatchet from the item grid. You should get 3 poles, then the clump falls. Pick up
  and hold a pole.
- **Sakura:** stand under one, then look back at it from ~150 m. Still a sakura? Do the trees sway in wind?

## 6. Island extras (optional, 5 min)

| What | Where | What to check |
|---|---|---|
| Road | north from the square's north-east corner | Does it sit on the ground? |
| Vanilla control house | ~210 m east-south-east | Loot inside? That proves the loot system works on this map |
| Canal | east coast, ~500 m east-south-east | Sea water fills it |
| Pond | ~240 m west-south-west | Water visible, fresh water to drink |

## Tell me

- What failed.
- What looked wrong.
- Your verdicts on:
  1. JP_Yumi vs JP_Yumi_XB
  2. the long kimono
  3. the stair steepness

Screenshots help but aren't required.
