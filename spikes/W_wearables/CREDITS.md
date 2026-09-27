# Spike W: credits and licences

## Downloaded assets

None. No ambientCG or Poly Haven files were used.

## Textures (all procedural, made for this project)

Written by `tools/textures.py` with numpy and Pillow, then converted to `.paa` with DayZ Tools' `ImageToPAA.exe`.
They are original work of this project, so they carry no third-party licence.

| Texture set | Content |
|---|---|
| `JP\characters\kasa\data\jp_kasa_{co,nohq,smdi}` | Radial sedge strips, stitch rings, and swatches for the binding, head ring and knob |
| `JP\characters\kimono\data\jp_kimono_{short,long}_{co,nohq,smdi}` | Indigo plain weave with seams and a back crest (a circle and two bars). Also a black collar with a white under-collar edge, and a rust striped obi |
| `JP\characters\tabi\data\jp_tabi_waraji_{co,nohq,smdi}` | White tabi cotton with brass kohaze clasps and a grey sole. Also a braided straw sole and twisted straw cords |

## Vanilla DayZ data: referenced by path, not copied

The shipped rvmats and p3ds point at these vanilla files. They load from the game's own PBOs. None of them is
inside `jp_characters.pbo`.

- Damage macro textures:
  - `dz\characters\tops\data\tops_{damage,destruct}_mc.paa`
  - `dz\characters\shoes\data\shoes_{damage,destruct}_mc.paa`
  - `dz\characters\vests\data\vests_damage_mc.paa`
  - `dz\characters\data\generic_destruct_mc.paa`
- Reflection texture: `dz\data\data\env_land_co.paa`
- Skin material and texture: `dz\characters\heads\data\hhl_dummy_skin_material.rvmat` and the default skin colour.
  These are what vanilla tops use on their `personality` faces.
- Bullet penetration material: `dz\data\data\penetration\fabric_thin.rvmat`

## Vanilla DayZ data: used offline as reference only, never shipped

This data was read from `P:\` (the extracted game data). The derived files live in `data/W/`, which git ignores.

- **The naked body parts** `torso3`, `legs3`, `feet3` and `hands3`, for both `_m` and `_f`.
  - Their positions, faces, UVs and skin weights were extracted from the binarized p3ds.
  - Uses:
    - fitting the garments
    - transferring weights by closest point
    - UVs for the forearm skin
    - the preview renders
- **All 31 head models**, positions only, for the envelope the hat has to clear.
- **The `DayzTemporarySkeleton` bone list**, read from vanilla worn clothing. `model.cfg` reproduces it, because the
  worn models have to bind to the game's own skeleton.
- **The player bind pose**, from `bodies/player_testing.xob` and `player_f_testing.xob`.
- **Animation clips** `P:\DZ\anims\anm\player\...`, which pose the test renders.
- **Vanilla configs**, which gave the parent classes and the damage values copied into our `DamageSystem`.

## Code reused (read-only)

- **`tools/common/mlod.py`**, copied as `tools/mlod_w.py` without changes.
- **`tools/common/pbo.py`**, called as-is.
- **`tools/anm_pose.py`**, trimmed from three `pokemon_dev` files:
  - `pokemon_dev/tools/player_anim/xob_player.py`
  - `anm_decode.py`
  - `player_fk.py`

  A copy was needed because importing these files in place would write a `__pycache__` into `pokemon_dev`.
