# Gear slots: planning note (Stephen, 2026-09-27)

**Stephen's rule:** map period gear onto DayZ's player slots so that items **don't overlap**. If about 90 % of the
outfits for a slot's body area include something by default (for example the obi), either bake it in and retire
the slot, or ship the garments without it and make it a separate item in that slot. Decide per slot before any
wardrobe work starts. Clothing is **one shared set for players and infected** (G0 decision 6).

**Vanilla player slots** (`SurvivorBase attachments[]`, `P:\DZ\characters\data\config.cpp`): Headgear, Mask,
Eyewear, Gloves, Armband, Body, Vest, Back, Hips, Legs, Feet, Shoulder and Melee (the two long-item carry slots on
the back). Not wearable slots: Head (the head model itself), Hands and LeftHand (held items), Splint_Right (medical).

| Slot | Vanilla use | Period candidates (to research) | Overlap / notes |
|---|---|---|---|
| Headgear | Hats, helmets | Kasa straw hats, jingasa, kabuto helmet, eboshi, zukin hood, the komuso basket hat | The komuso basket covers the whole head, so it may need to hide the Mask slot |
| Mask | Masks, balaclavas | Menpo/menpō face armour, fukumen face cloth, tenugui tied over the mouth | Could conflict with helmet cheek guards (kabuto fukigaeshi); check the fit |
| Eyewear | Glasses | Little period use | Probably **leave empty**; a slot can simply go unused |
| Gloves | Gloves | Tekkō hand guards, kote (armoured sleeves) | Kote cover the forearm and hand, so they must fit under a kimono sleeve |
| Armband | Team armband | **Tasuki**, the cord that ties sleeves back for work and fighting; or a clan-mon cloth | Tasuki is a good visual and needs no new slot logic |
| Body | Shirts, jackets | Kosode, kimono, juban, work jackets (hanten, happi) | Knee length at most for players and infected (floor-length breaks when legs move) |
| Vest | Plate carriers, vests with cargo | Samurai dō (with sode), **or** haori/jinbaori over the kimono | **Conflict:** armour and haori can't both be worn. Decide whether the haori is Vest or part of Body |
| Back | Backpacks | Oizuru pilgrim frame, furoshiki bundle, seoi-kago basket, **sashimono** banner | A sashimono and a backpack both want the back |
| Hips | Belts (holster/knife/canteen attachments) | **Obi** | See the obi decision below |
| Legs | Trousers | Hakama, momohiki trousers, fundoshi-only (bare legs, NPC/infected only per the playbook) | Kyahan shin wraps: part of Legs, or part of Feet? |
| Feet | Shoes, boots | Waraji, zōri or geta, worn with tabi | Tabi are best built into the footwear item (as the spike did), so no skin seam shows |
| Shoulder / Melee | Long weapons carried on the back | Yumi, yari, naginata, matchlock | **Swords were worn at the obi, not on the back.** A katana on the back is the ninja myth. See below |

## The obi decision (Stephen's example)

- **Option A: baked in.** Every kimono mesh includes its obi, and the Hips slot is retired or left for rare items.
  - Simple and always looks right.
  - The obi carries no gameplay.
- **Option B: a separate Hips item** (lead's recommendation, for Stephen to decide).
  - Kimonos ship with only a thin under-cord (koshihimo), so they still look closed without an obi.
  - The obi is the Hips item, exactly like vanilla belts, with **attachment slots**:
    - katana and wakizashi thrust through it (period-correct sword carry, instead of a sword on the back)
    - tantō
    - inrō/netsuke pouch
    - gourd canteen
  - It is also a loot or crafting drop.
  - The obi becomes the samurai's gear anchor. Vanilla belts already work this way, so it is proven engine behaviour.

## Still to decide before the wardrobe work

1. Obi: A or B.
2. Haori: Vest or part of Body.
3. Sashimono: yes or no, and whether it blocks backpacks.
4. Kyahan: Legs or Feet.
5. Eyewear: leave empty?
6. Swords at the obi (needs B) vs vanilla back carry.
