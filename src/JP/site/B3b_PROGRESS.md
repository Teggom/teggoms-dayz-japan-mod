# B3b progress: outdoor site objects, wave 1 (research/outdoor_kit/BUILD_LIST.md, the 20 W1 items) — DONE

Agent B3b (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_B3b.md`.

## Status
All 20 W1 items, **129 models** (20 new, 80 variants, 29 abandoned). The list asked for 122: +5 because `_shape_x6`
became six models (one shape sign per trade), +1 handcart `_ab_wreck` (G1: several levels of disrepair), +1 shop-front
`_ab_kanban_askew` (the list's "signboard hanging from one cord"). Checks 129/129 pass (`spikes/B3b/checks.json`);
binarize 129/129 ODOL, 0 warnings; CfgConvert OK.
PBO: `@Japan/addons/jp_site.pbo` (prefix `JP\site`, CfgPatches `JP_Site`, requires DZ_Data + DZ_Scripts + JP_Common,
CfgMods `JP_Site` with a 4_World script module). 121 classes `StaticObj_JP_S_<Name>` : HouseNoDestruct, scope 1 (vanilla
StaticObj_Misc_*); 8 well classes `Land_JP_S_Well_*` : HouseNoDestruct.
Sheets: `research/outdoor_kit/contact_sheets/b3b_{yard,water,roadside,street}.jpg`.

| Group (folder) | Items (models) |
|---|---|
| yard | firewood_stack 6, laundry_pole 7, straw_stack 6, oke 7, tenbin 5, handcart 7 |
| water | well_tsurube 6, well_hanetsurube 3, fire_tub 5 |
| roadside | stone_jizo 7, jizo_hut 4, stele 8, shimenawa 6, kosatsu 4 |
| street | gutter 8, bench 5, shopfront 16, lantern_sign 8, stall 6, nobori 5 |

## Wells (drink + wash, G1 A3 answer 3)
Vanilla mechanism, found in `P:\scripts\4_world`: config `Land_Misc_Well_Pump_Yellow: HouseNoDestruct` plus a one-line
script class `class Land_Misc_Well_Pump_Yellow extends Well` (`entities\building\residential\misc\`). `Well`
(`entities\building\well.c`) adds ActionDrinkWellContinuous + ActionWashHandsWell and makes the object a WELL water
source (bottles fill too). Ours mirror it exactly: `src/JP/site/scripts/4_World/JP_Site/jp_site_wells.c` (generated,
8 lines `class Land_JP_S_Well_* extends Well {};`), same pattern as JP_Plants' tree classes. Class name = `Land_` + p3d
name, so a .wrp-baked well finds its class. All tsurube variants and hanetsurube `_well` / `_ab_down` are wells;
hanetsurube `_field` (sweep over a ditch) is not. The curb is one closed collision cylinder (nobody falls in; the camera
ray hits it = the drink target). Water = a glossy black disc 8 cm up inside the curb (terrain has no holes).
**Untested in game** (first in-game check: crouch at a curb, drink / wash bloody hands / fill a bottle).

## Conventions (for B4 and the map agent)
- Frame: origin = base centre on the terrain, +z = front (road side), autocenter 0. Sidecars
  `src/JP/site/<group>/<item>.prop.json`: class, p3d, state, anchor, wall_gap, faces, bbox, collision LODs, footprint,
  loot surfaces (bench tops, stall counters), `text_cells`, `hang_y`, `disrepair` (handcart 1-4), notes.
- anchor 'wall': wall plane z = 0, y = 0 at the wall foot. Firewood stacks 5 cm off the wall. Shop-front pieces and
  hanging lanterns are **proxies** for shop buildings: lintel assumed 2.00 m, eave pieces at `hang_y`; move y to the
  real lintel / eave.
- Collision: stone, wood, carts, wells = Geometry + View + Fire; straw stacks = View only (soft cover); cloth, rope,
  hung signs = none; gutter = Geometry + Roadway only on the slab and the dobu-ita.
- Gutter pieces sit in a terrain ditch (tops flush with grade); the ditch is the terrain / placement agent's cut.
- Wear: standing = `_w1`, abandoned states and cloth/paper leftovers = `_w2`. Leaf litter (`jp_m_ground_leaf_litter`)
  in every open vessel; `jp_m_decal_litter` / `jp_m_decal_moss` patches.

## Text (G1 A3 answer 5: Japanese)
B1's atlases only, no new cells: `jp_m_decal_sumi_text` (kosatsu_chuko_1711 on the notice boards, cropped for
variety; kanban_okashidokoro / osobakiri / oyasumidokoro / oyado / miki; chochin_honcho; nobori_hono_inari;
oke_yosui, mark_marudai) and `jp_m_decal_carved_text` (enmei_jizo, koshin_kuyoto, bato_kanzeon, namuamidabutsu,
dosojin, michishirube_edo_oyama, sakai_kore_yori_higashi). Fonts: Yuji Syuku + Yuji Hentaigana Akebono (SIL OFL 1.1,
Yuji Project Authors), credited in B1's material sidecars.

## Materials added (through B1's pipeline, additive only)
`jp_m_textile_bib_red` (_w0-_w2, alpha cut) + palette entry `bib_red_faded` [142,80,68] (assumed, tol 12), by
`research/materials/make_b3b_materials.py` (uses make_b1_materials.make_one; C1 PASS on PNG and PAA,
`src/JP/common/materials/checks_b3b.json`); jp_common.pbo repacked. The Jizo bib uses its `_w2` (grey-pink rag).

## Decisions I made
- Signboards and notice boards use `jp_m_wood_weathered`, not `wood_street_dark`: black sumi text does not read on
  the dark board. Shop nobori are kinari for the same reason.
- Loads (laundry, tenbin, cart) are whole models, not swappable parts (one placement dresses a spot).
- Dried persimmons use `jp_m_wood_bengara`, shrivelled daikon `jp_m_paper_shoji _w2`, the fishing net rope strands:
  no dedicated material (none needed for filler).
- Stele family is Res 1-2 (filler-sized stones; R3 would equal R2). Jizo, huts, wells, carts, kosatsu, stalls,
  fire tub: Res 1-3.
- Straw rope / shide and the noren shop mark: the noren atlas tiles 4 marks, so noren panels map one mark on the
  middle panel and plain cloth elsewhere; kimono loads use the plain strip.

## Not done / open
- Nothing tested in game. No test-island placement (B4 next).
- A tsurube `_lid` well is still a Well class (lift the lid and drink) — judge in game.
- Only one edict text exists (the 1711 loyalty board); other boards reuse crops of it.
- Stook sheaves and shimenawa tassels read thin in renders (filler; can be thickened on request).

## How to rebuild
`python spikes/B3b/build.py [item ...] [--no-binarize] [--pack]`; `python spikes/B3b/render.py [item ...]`;
`python spikes/B3b/render.py --sheets`; material: `python research/materials/make_b3b_materials.py`.
Pipeline: `spikes/B3b/` (skit.py = B3a's fkit/bits, imported read-only, + outdoor helpers; build.py; render.py;
props_wood / wells / stone / street / straw). MLOD masters in `spikes/B3b/out/` (not committed).
