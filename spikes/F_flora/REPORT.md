# Spike F (flora): report

(The agent returned this as text because its Write tool refused REPORT.md; the lead saved it on 2026-09-27.)

**Result:**
- A Somei-yoshino sakura in full bloom, in two sizes.
- A cuttable bamboo clump.
- A `JP_BambooPole` item.
- All three built from code, binarized cleanly and packed into `@Japan\addons\jp_plants.pbo`.
- Nothing has been tested in game yet.
- Previews: `renders/F_overview.jpg` (one sheet), with the per-view files next to it.

## Built

| File (`src/JP/plants/` = `P:\JP\plants`) | What |
|---|---|
| `tree/jp_sakura_01.p3d` | Hero sakura: 7.0 m tall, crown 9.8 × 11 m, 5 scaffold limbs plus a leader, dark bark with lenticel bands, 1023 blossom cards |
| `tree/jp_sakura_02.p3d` | Younger size variant: 5.2 m tall, crown 7.4 × 8.8 m |
| `bamboo/jp_bamboo_clump_01.p3d` | 21 culms, 4.5–9.9 m tall, in a 0.75 m radius clump. The culms lean out, nod at the tips, have visible nodes, and are leafy from half height |
| `items/jp_bamboo_pole.p3d` | 2.5 m pole, green at the top and yellow-green at the butt, with raised nodes and hollow cut ends |
| `*/data/*.paa`, `*/data/*.rvmat` | 13 textures and 13 rvmats |
| `config.cpp` | See "Config classes" below |
| `scripts/4_World/JP_Plants/jp_plants_classes.c` | 3 script classes, declared the way vanilla `trees.c` and `bushes.c` do |

**LOD chains.** They copy the layout of vanilla `t_prunusdomestica_2s` (the plum): resolution LODs 1–4, then Geometry,
Memory, View Geometry and Fire Geometry.

| Model | LOD1 tris / cards | LOD2 | LOD3 | LOD4 | Geometry components |
|---|---|---|---|---|---|
| sakura_01 | 7088 / 1023 | 2974 / 561 | 1560 / 266 | 6 (impostor) | 14 |
| sakura_02 | 3066 / 365 | 1394 / 222 | 648 / 132 | 6 | 12 |
| bamboo clump | 4162 / 191 | 1654 / 122 | 740 / 76 | 6 | 21 (one per culm, 0–2.6 m) |
| pole | 552 | 28 | 16 | – | 1 (mass 1.8 kg) |

**How the models are put together:**
- **Materials.** Bark and culms use `TreeAdvTrunk` and sway. Blossom and leaf cards use `TreeAdv` with a windmask in
  Stage4, so the tips flutter. The pole uses `Super`.
- **LOD4** is two crossed billboards plus one horizontal billboard, the same layout as the plum. Its texture is
  rendered in Blender from our own LOD1.
- **Geometry named properties** are copied from the plum, plus `autocenter=0`: `class=treehard` or `bushhard`,
  `dammage=tree`, `map=tree`, `style=plant`, `frequent`, `drawimportance`, `canclimb` and `canocclude`. The ODOL
  header carries `treehard` or `bushhard` at the same offset as the plum's.
- **Memory LOD:**
  - Sakura: `action` and `sound_TreeLargeLeavesDomestic`.
  - Bamboo: `action` and `sound_TreeMediumLeaves`. These are vanilla env-sound points, so birds, rain and wind in the
    leaves should come for free.
  - Pole: vanilla LongWoodenStick's set of points (`ce_center`, `ce_radius`, `invview`, `meleerange*`,
    `boundingbox_*`, `throwingimpulseposition`).

### Config classes

- **CfgPatches:** `JP_Plants`.
- **CfgMods:** `JP_Plants`, which declares the `worldScriptModule`.
- **CfgNonAIVehicles:**
  - `TreeHard_jp_sakura_01`, the same for `_02`, and `BushHard_jp_bamboo_clump_01`.
  - These are the classes the engine gives to terrain objects of those p3ds.
- **CfgVehicles:**
  - `JP_BambooPole: LongWoodenStick`.
  - `JP_Sakura_01_Static`, `JP_Sakura_02_Static` and `JP_BambooClump_01_Static`, all `HouseNoDestruct` and scope 1.
    They exist for the object spawner, the same way vanilla's `ChristmasTree` does.

### Test drop-ins

- **`test/placements/F.csv`:**
  - `jp_sakura_01` at (985, 1010) and `jp_sakura_02` at (1063, 1010).
  - 7 bamboo clumps in x 1083–1107, z 958–992, at least 8 m apart.
  - `y_offset = -0.05` everywhere.
- **`test/spawns/F.json`:** `JP_Sakura_01_Static` at (1110, 1050) and `JP_BambooClump_01_Static` at (1110, 1068), both
  at y = 24.95.
- **`test/items/F.txt`:** `Hatchet`, `WoodAxe`, `Machete`, `JP_BambooPole 2`.
- **`test/types/F.xml`:** `JP_BambooPole` (nominal 0), a copy of vanilla LongWoodenStick's entry.

### Tools

All in `spikes/F_flora/tools/`. Run `build.py --tex` to rebuild everything in about 20 s.

| Tool | Job |
|---|---|
| `textures.py` | Textures |
| `sakura.py` | Sakura models |
| `bamboo.py` | Bamboo clump and pole |
| `meshlib.py` | Mesh building blocks and winding |
| `render_blender.py` | Impostors and preview renders |
| `impostor.py` | Assembles the impostor texture |
| `build.py` | Runs everything: rvmats, config, CfgConvert, binarize, pack, test files, renders and the overview sheet |
| `mlod.py` | Copied from `tools/common` unchanged. It already handles any LOD resolution and named property |

Always use `build.py`. Running `sakura.py` or `bamboo.py` alone leaves MLOD files in `src/`. Intermediate files and
MLOD masters live in `data/F/work/`, which is git-ignored.

## Verified offline

- **CfgConvert:** `config.cpp` converts cleanly.
- **Binarize** (cwd `P:\`): all 4 p3ds come out as ODOL.
  - Logs: `data/F/work/binarize_*.log`.
  - No texture or material "not found" lines, and no convexity warnings.
  - The only noise is the generic PreloadConfig and "error value" lines. The Pokemon binarize logs have the same 6.
  - `BoundingCenter 0,0`, so `autocenter=0` held.
- **ODOL strings:**
  - LOD list: 1, 2, 3, 4, 1e13, 1e15, 6e15, 7e15, identical to the plum.
  - Named properties, rvmat stages and penetration materials are all present.
  - The memory LOD is 311 bytes, the same as the plum's.
- **Face winding:** checked against the rule from `pokemon_dev/tools/check_winding.py`, which was proven in game. 0 bad
  faces.
- **PBO:** 32 entries under prefix `JP\plants`, listed with `pbo.py list`.
- **Renders I looked at:**
  - Every model at eye height from 5 m, 30 m and 150 m. The 150 m shots come as LOD3 and LOD4, with 4× crops.
  - A sheet of every LOD side by side.
  - The pole: its LODs, and a close-up of a node and the cut end.
  - The atlases themselves.
- **What the renders show:**
  - **Sakura:**
    - At 5 m you stand under a pale-pink canopy of five-petal clusters on dark branches.
    - At 30 m it is a broad, spreading crown on a short dark trunk.
    - At 150 m it is a pale-pink cloud with a dark stem.
    - It reads as a sakura, not a pink blob.
  - **Bamboo:** at 5 m, green culms with nodes and drooping lanceolate sprays. Further out, bare culm bases under a
    leafy head.

## In-game checklist for Stephen

**Where things are:** sakura west at (985, 1010) and east at (1063, 1010); bamboo grove x 1083–1107, z 958–992;
spawned copies at (1110, 1050) and (1110, 1068); tools and poles on the item grid.

1. **Sakura, near.** Stand under each tree.
   - **Pass:**
     - Pale-pink blossom clusters on dark branches.
     - Banded dark bark.
     - The trunk sits on the ground: not floating, not sunk.
     - No black or white fringes on the cards.
     - Not a flat pink blob.
     - It casts a shadow.
2. **Far.** Go to about (925, 925). The east sakura is about 160 m away and the grove about 175 m.
   - **Pass:** both are still recognisable, and the LOD switches are not jarring.
   - **Fail signs:** a crown that goes thin, grey or cross-shaped.
3. **Wind.** On a breezy day, watch for 20 s.
   - **Pass:** the crowns sway gently and the blossom and leaves flutter. The bamboo culms sway more than the sakura.
   - **Fail:** nothing moves, or the trunk "rubber-bands" at the base.
4. **Bamboo collision.** Walk into a clump.
   - **Pass:** the culms stop you, and you can walk between clumps.
5. **Chopping.** Use a hatchet, then a wood axe, then a machete, each on a different clump. Aim at a culm.
   - **Pass:**
     - The prompt is "Harvest Bamboo Pole".
     - 3 cycles of about 3 s, one pole dropping at your feet each cycle.
     - On the third cycle the clump falls or flattens like a vanilla bush, with the bush-falling sound, and a stack of
       3 Wooden Sticks appears.
     - The tool loses a little health.
6. **Sakura chopping (optional).** Hatchet on a sakura trunk.
   - **Pass:** the tree falls like a vanilla tree; 1 wooden log and 1 long stick.
7. **Holding the pole.**
   - Pick it up. **Pass:** it is held like the vanilla long stick, gripped about 0.9 m from the butt with the long end
     up and forward.
   - Shoulder it and take it off again. Drop it. **Pass:** it lies on the ground and does not stand up, float or sink.
   - Inventory: 1×10, about 1.8 kg.
   - Optional: use a knife on it. **Pass:** "sharpen" and "split" appear.
8. **Spawned copies.**
   - **Pass:** they look the same as the terrain ones, on the ground. They are **not** cuttable, and that is expected.

## Failed / unknown

- **Nothing is tested in game.** Blender is not the engine: `TreeAdv`'s lighting will differ. If the blossom looks too
  dark or bright, the first knob is the constant `MCA` value in `jp_sakura_blossom*.rvmat` (0.65, the plum LOD4's
  value).
- **Trunk sway with `autocenter=0` is unverified.** Vanilla ivy uses `autocenter=0` with `TreeAdv` and a windmask, so
  the combination exists in vanilla.
  - **Fallback:** set `autocenter` to 1 in `GEO_PROPS` in `sakura.py` / `bamboo.py`, and T then uses `y_offset` = the
    model's half height.
- **Terrain matching by p3d name** (`TreeHard_jp_sakura_01`, `BushHard_jp_bamboo_clump_01`) can only be proven by the
  engine. It follows the vanilla naming, header and script classes.
- **Far LODs:** blossom density at distance and the switch distances are the engine's call.
- **Sakura LOD1 is heavy:** about 7.1k tris and 1023 alpha cards. Fine for hero trees, too heavy for orchards.
- **Pole:** the grip, the inventory preview framing and the ground pose are copied from the vanilla stick by analogy
  only.

## Decisions I made

1. **Bamboo is `BushHard`, not `TreeSoft`.**
   - **Tools:** as a tree, only the hatchet, wood axe and firefighter axe could fell it, and the machete would only get
     "harvest bark". As a hard bush, everything with `ActionMineBush` cuts it: hatchet, both axes, all machetes,
     knives, saws, sickle, sword and bayonets.
   - **Collision:** "hard" keeps it blocking walkers.
   - **Bonus:** A's katanas get it for free if they inherit `Sword`.
2. **Drops:** 3 poles, one per 3 s cycle. `toolDamage` 4, the vanilla value. Secondary output `WoodenStick` ×3 as one
   stack, standing for the leafy tops.
3. **Sakura is cuttable** with the plum's values: 1 `WoodenLog` plus 1 `LongWoodenStick`, cycle 3 s, bark from the
   inherited `Bark_Oak`.
4. **`JP_BambooPole` inherits `LongWoodenStick`.**
   - **Profile correction:** the brief's two-handed assumption was wrong. That class's in-hands profile is the
     one-handed pipe set (`player_main_1h_pipe.asi` with the `LongWoodenStick.anm` IK). The two-handed spear profile
     belongs to `SharpWoodenStick`, which would make the pole a sharp weapon.
   - **What it gains:** the stick's slots and quantity rules, plus all 14 long-stick recipes, because recipes match
     with `IsKindOf`.
   - **Changed:** weight 1800 g and size 1×10.
   - **Grip:** the frame is copied from `Wooden_stick_blunt.p3d`: +Y long axis, grip at the origin, 0.9 m from the
     butt.
5. **`autocenter=0` everywhere.** The origin is the base, so placements and spawns are exact.
6. **Both sakura variants are placed.** `_01` is the spawned fallback copy.
7. **Materials copy vanilla parameter blocks exactly:**
   - Plum trunk, leaves and LOD4 for the sakura.
   - Larch trunk wind for the culms.
   - Birch leaf wind for the bamboo leaves.
   - No second UV set: constant `MC` / `MCA`, the vanilla hazel and plum-LOD4 precedent.
   - Single-sided cards, because the plum's LOD4 billboards are single quads.
8. **Textures:** the bark is Poly Haven's CC0 "Sakura Bark", darkened. Everything else is procedural. Petals are
   slightly pinker than life so they survive in-game tone mapping.
9. **Bamboo is a clumping type,** 0.75 m radius, one cuttable object; a grove is several clumps.
10. **Intermediates moved to `data/F/work`** (git-ignored) and renders saved as JPEG (1.4 MB).

## Next step

In agent sessions:

- **In-game pass, then tuning:** 0.5. The `autocenter` fallback, if needed, is 0.25 plus a rebake by T.
- **Falling petals under sakura:** 1.
- **More species from the same generators:** about 1 each for sakura ages, sugi, black pine and maple.
- **Bamboo extras** (madake grove model, dead culms, shoots): 1–2.
- **A true two-handed pole carry** through a script-registered in-hands profile: 1, and it needs testing in game.
- **Bamboo recipes:** 1–2.
