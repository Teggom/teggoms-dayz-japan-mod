# Spike A (arms): katana, yari, yumi + ya

Agent A, spike wave 1, 2026-09-26/27. Vanilla animation sets only; nothing tested in game yet.

(The agent returned this as text because subagents can't write report files; the lead saved it on 2026-09-27.)

## Bow verdict

**The vanilla bow path does not work, and it can't animate a draw or a shot without new animation-set or graph
work.**

1. **No weapon state machine.**
   - `RecurveBow`, `QuickieBow` and `PVCBow` have no script class of their own, so the engine uses `Archery_Base`
     (`4_world/entities/firearms/archery/archery_base.c`).
   - `Archery_Base` never builds `m_fsm`, so `Weapon_Base.CanProcessWeaponEvents()` is false and every load or fire
     request is ignored.
   - The crossbow works only because `Crossbow_Base` builds its own FSM (`crossbow.c`).
2. **No ammunition.**
   - `Ammo_ArrowComposite`, `Ammo_ArrowPrimitive` and `Ammo_ArrowBoned` (the bows' `chamberableFrom`) are defined
     nowhere.
   - `Mag_Arrows_Quiver` exists, but its `ammo="Arrow_Composite"` is undefined.
3. **The animation set can't reach the weapon operations.**
   - `player_main_bow.asi` binds full bow locomotion, hits, deaths and falls, so holding and raising work.
   - Its draw, hold, loose and nock clips (`reloads/bow_quick/*`; `reloads/bow_recurved/*` is not referenced anywhere)
     sit in `Combat.{Erc,Cro}.{In,Loop,Shoot,Chamber,Reload,Cancelled}`.
   - No node in any player `.agr` plays those slots. In `player_main.asi` the same slots hold old unarmed
     charged-attack clips, also unused: a dead legacy "charge" path.
   - The weapon states in `weapons.agr` play `WeaponOperations.*` slots, and the bow set binds none of them.
   - The bow clips carry **no animation events**. The vanilla chambering states need `Weapon_BulletShow` /
     `Weapon_BulletInChamber`, which the crossbow clips have.
4. **The item behaviour is half set up.** `archeryItemBehaviour` (`dayzplayercfgbase.c:461`) is a bare
   `DayzPlayerItemBehaviorCfg`: type 0, hand IK off in every stance, no camera user data.
   - The hands follow the clips.
   - Measured: the left hand holds the same grip point in every erect and crouch bow clip (±1 cm). Prone releases it.
5. **The vanilla RecurveBow's IK pose is misaligned.**
   - `bow_erc_recurve_IK.anm` closes the left hand about 20 cm behind the recurve riser.
   - The Quickie and PVC bows (`bow_erc_IK.anm`) are aligned to about 1 cm.
   - See `renders/vanilla_recurve_hands.png`.

| Class | Animation set | FSM | Expected |
|---|---|---|---|
| `JP_Yumi` (config: `RecurveBow`) | vanilla bow set: correct hold | own script FSM. The nock is a 0.9 s script timer with no animation and no events needed. The loose is the vanilla `WeaponFireLast` state (`TryFireWeapon` on state entry, leaves on its own timeout) | Holds and raises like a bow. **Partly works, unproven:** R nocks with no animation, LMB looses with no draw. The unknown is the graph's handling of a `FIRE` action with an unbound clip. Every exit has a timeout |
| `JP_Yumi_XB` (config: `Crossbow_Base`) | vanilla crossbow set | vanilla crossbow FSM, untouched | **Should fully work:** cocking animation, fire, recover. Looks odd: held like a crossbow, left hand about 60° off the grip |
| `JP_Ammo_Ya` (config: `Ammo_HuntingBolt`) | bolt pile pose | — | Pile, stack of 10. `Bullet_JP_Ya`: `shotArrow`, 80 m/s, `spawnPileType="JP_Ammo_Ya"`. Recovery is vanilla: the engine drops a pile where the ya stops, and `AddArrow` sticks it into infected and animals |

**What would make the yumi animate:**
1. **A child `.asi` of `player_main_bow.asi`, no graph edit.**
   - It would bind:
     - `WeaponOperations.ErcRas.Chambering_Open` ← `p_erc_chambering_recurvedbow_ras.anm`
     - `WeaponOperations.ErcRas.Fire` ← `p_erc_shoot_recurvedbow_ras.anm`
     - the Cro / Pne equivalents
   - It would be registered for `JP_Yumi` through a modded `ModItemRegisterCallbacks.RegisterArcheryItem`.
   - The script-timer nock stays (no events in the clips).
   - It uses vanilla clips only, but it is a new animation-set file, so it's Stephen's call.
   - Unknown: whether a mod can ship a text `.asi` unbuilt.
2. **Draw-and-hold** (hold LMB, release to loose) needs player-graph states playing the orphaned `In` / `Loop` /
   `Shoot` clips. That means owning the single player-graph slot (FEASIBILITY §5, shared with riding). Big.

## Built

- **`src/JP/weapons/config.cpp`**:
  - `CfgPatches JP_Weapons`
  - `CfgMods JP_Weapons` (world script module `JP/weapons/scripts/4_World`)
  - `JP_Katana`, `JP_Yari`, `JP_Yumi`, `JP_Yumi_XB`, `JP_Ammo_Ya`, `Bullet_JP_Ya`, `FxRound_JP_Ya`
- **`src/JP/weapons/scripts/4_World/JP_Weapons/jp_archery.c`**: the `JP_YaNock` state, the `JP_Yumi` FSM, and
  `JP_Yumi_XB` (hides the nocked ya on loose).
- **`src/JP/weapons/{katana,yari,yumi,ya}/*.p3d`**: ODOL.
  - 3 resolution LODs; Geometry (box, mass, `autocenter=0`); Memory (the parent's point names); View and Fire
    Geometry.
  - `yumi/model.cfg` makes `bullet` a section.
- **`src/JP/weapons/data/`**: 6 procedural `_co.paa` textures (`.png` kept for renders, skipped by `pbo.py`) and 9
  rvmats.
- **`@Japan/addons/jp_weapons.pbo`**: 23 files, 1.06 MB.
- **`spikes/A_arms/tools/`**:
  - `build.py` runs the full pipeline: textures → MLOD → binarize → CfgConvert → pack.
  - `models.py` + `meshkit.py`: the model generator.
  - `textures.py`: the procedural textures.
  - `odol.py`: a vanilla ODOL v54 reader (LOD table, vertices, faces, selections, memory points, LZO). Reusable.
  - `hands.py`, `vanilla_frames.py`, `grip_proof.py`: IK hands in a model frame.
  - `overlay.py`, `render_blender.py`, plus copies of `mlod.py` and `pbo.py`.
  - The MLOD sources are in `work/mlod/`.

**Models:**
- **Katana**: 0.99 m. Curved shinogi-zukuri blade (sori 17 mm), ko-kissaki, notare hamon, brass habaki, iron mokko
  tsuba, silk diamond wrap over samegawa with menuki, iron fuchi and kashira.
- **Yari**: 1.80 m. Lacquered shaft, brass collar, 25 cm diamond-section su-yari blade, ishizuki.
- **Yumi**: 2.24 m. Grip 0.73 m from the bottom tip, so the upper limb is 1.47 m. Rattan wraps, leather grip,
  reflexed tips, hemp string, nocked ya on the right side.
- **Ya**: 0.99 m. Bamboo with nodes, iron leaf head, three barred feathers, horn nock. Frame as the vanilla bolt: tip
  at the origin, shaft along +Z.

## Verified offline

- **Binarize**: all 5 are ODOL, with only "UV mapping too varied" warnings (`work/binarize_*.log`).
  - Read back with `odol.py`: LODs, `autoCenter=0` and memory points all correct.
  - The `bullet` selection is sectional, like the vanilla crossbow's.
- **CfgConvert**: OK. Round trip in `work/cfgcheck/`.
- **Enforce Script**: `pokemon_dev/tools/enforce_check.py` finds no problems; braces balanced. Not compiled.
- **Grip frames**:
  - The IK item frame is `p3d = (dx, dz, -dy)`. It's fixed by the sword, spear and bat (knuckle lines along p3d Y)
    and the asymmetric crossbow.
  - On vanilla models, the finger-curl centres land within 1-2 cm of the handles (`renders/vanilla_*_hands.png`).
  - Our models over the vanilla LOD 0 plus hands (`renders/grip_*.png`), as distance from each hand's grip centre to
    our grip axis:

  | Model | Right hand | Left hand | Other |
  |---|---|---|---|
  | Katana | 12 mm | 17 mm | Tsuba at the vanilla guard base (y 0.125) |
  | Yari | 12 mm | 9 mm | |
  | Yumi (bow set) | at the nock | 0.3 mm | |
  | Yumi (crossbow set) | at the drawn nock | 0.4 mm | |

- **Blender renders looked at**: `renders/jp_{katana,yari,yumi,yumi_xb,ya}_*.png` and `textures_contact.png`.

## In-game checklist for Stephen

The items are on the grid near the spawn (x 1000+, z 975). Shoot from z ≈ 955, facing south. The range has:
- hay bales at (1004, 944), (1016, 940) and (1030, 933)
- a target frame at (1043, 928)
- a concrete backstop at (1024, 926.5)
- infected at (1010, 950) and (1022, 938), a deer at (1037, 942)

1. **Katana**
   - Take it in hands. **Pass:** the tsuka is in both fists, the tsuba sits just above the right hand, and the blade
     curves back with the edge facing away from you.
   - Light attack (LMB), heavy (hold LMB), sprint attack.
   - Kill the infected at (1010, 950).
   - Repeat with the vanilla **Sword**. **Pass:** the same swings and a similar number of hits to kill.
2. **Yari**
   - The same, against **SpearStone**. **Pass:** the hands are on the shaft, the blade is forward, and thrusts land.
     It does one tier more damage than the stone spear.
3. **JP_Yumi**
   - Hold it, then RMB to raise. **Pass:**
     - the bow is in the left fist
     - the long limb is up
     - the right hand is at the string
   - With Ya in the inventory, press R, or drag the ya onto the bow. **Pass:** about 1 s later a ya is on the string,
     with no animation.
   - LMB while raised. **Pass:**
     - the ya flies
     - the nocked one vanishes
     - it sticks in a hay bale or the deer
     - "Take" recovers it
   - **Report:**
     - any pose freeze
     - R doing nothing
     - an arrow that doesn't leave
   - Also check prone raised (no bow clips).
4. **JP_Yumi_XB**
   - R plays the crossbow cocking animation and the ya appears; LMB fires; the arrow is recoverable. **Pass:** load,
     fire and recover all work.
   - Say whether the look is acceptable as a fallback.
5. **Vanilla RecurveBow**
   - Expect the hands about 20 cm off the riser; R does nothing.
   - Script errors are possible (it has no FSM). This confirms the verdict.
6. **Vanilla Crossbow + Ammo_HuntingBolt**: the baseline.
7. **Damage**: 2-3 ya into the deer and 1-2 into the infected at (1022, 938). Same hit damage as the bolt, but slower
   (80 vs 105 m/s), so more drop.
8. **Optional**: the back and shoulder carry pose, and the inventory previews.

## Failed / unknown

- **JP_Yumi's graph behaviour** with an unbound `FIRE` clip is unproven. It has timeouts, but a pose hang can't be
  ruled out offline.
- **No unload on JP_Yumi**: a nocked ya can only be shot.
- **The bow set has no prone-raised clips.**
- **JP_Yumi_XB**:
  - keeps the crossbow's `weaponStateAnim`; `boneRemap` is cleared
  - the left hand is about 60° off the grip
  - the crossbow cocking animation on a bow looks odd
- **Ya stuck in a player** don't restore after relog: `ArrowManagerPlayer` has a private static hash that lists only
  the vanilla bolts.
- **Not verified**: the carry offsets for the 2.2 m / 1.8 m items, the `invview` points, and the grid overlap of long
  items.
- **Object spawner y** assumes the position is the bounding centre of autocentred props (hay bale y = 25.77). If the
  props float or sink by about 0.7 m, that assumption is wrong.
- **No damage variants in the visuals**: `healthLevels` repeat the same rvmats.
- **Script not compiled** until the next server start.

## Decisions I made

1. **Two yumi classes**: the bow set (the right look) and the crossbow set (guaranteed to work). One test session
   decides.
2. **JP_Yumi's grip follows the recurve IK's actual left-hand position**, not the misaligned vanilla recurve mesh.
3. **No quiver**: the crossbow pattern is ammo piles, and the vanilla quiver is dead config.
4. **Katana edge on +Z**, the knuckle side. Evidence:
   - the wrists and elbows sit on -Z in the sword IK
   - the fire axe's blade is on the knuckle side
   - the sori curves the tip toward the back
5. **Stats**:
   - Katana: the Sword's melee ammo, 1.2 kg.
   - Yari: `MeleeSharp*_3`, reach 2.0 m, sprint 3.9 m, 1.6 kg.
   - Ya: 80 m/s, air friction -0.0016, the hunting-bolt damage, stack of 10.
   - JP_Yumi uses the crossbow's shot sound and recoil.
6. **Yari 1.80 m**, 13% over vanilla.
7. **Procedural textures only**, no downloads.
8. **MLOD sources in `work/mlod`**; `src` holds only ODOLs.
9. **Test list uses `SpearStone`** instead of `Spear` (scope=0).
10. **Targets**: hay bales, a target frame and a concrete backstop. Dummies: two infected and one broadside red deer.

## Next step (effort in agent sessions)

- **After the test:** fix restart findings (0.5), then tune ya ballistics and damage (0.5).
- **If JP_Yumi works**: the child-`.asi` route for nock and loose animations: 1 session plus 1 restart. First prove
  that a mod `.asi` loads unbuilt.
- **If it hangs**: ship `JP_Yumi_XB` for now, and try the `.asi` route for the bow locomotion: 1 session.
- **Draw-and-hold on the player graph**: 2-3 sessions. Decide together with riding.
- **More blades from the same generator**:
  - nodachi and naginata: 0.5 session
  - wakizashi and tanto: 1 session (measure the 1H IK frames first)
