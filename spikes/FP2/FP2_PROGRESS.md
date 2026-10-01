# FP2 progress: prop fixes from Stephen's re-check (2026-10-01)

Agent FP2 (opus). Time log `japan_dev/TIMELOG_FP2.md` (logger `spikes/FP2/tlog.py`). Runs alongside FB2 (buildings).
Owns: spikes/B3a, L1, L2, B3b (+W2/W3/G1/FP1 code), src/JP/furniture, src/JP/site, jp_furniture / jp_site, materials.
Screenshots: test/feedback/2026-10-01_recheck/1_firewood_pile, 3_mochi_usu_kine_float, 4_rope_coils_polygonal.

## Tools (spikes/FP2)
- `quick.py b3b|b3a|l1|l2|s1 <prop ...>`: write masters + checks of selected props only (no config / binarize / pack).
- `render_fp2.py before|after <group>` (shots in `shots.py`; back faces culled as the game draws). `before` renders
  were made from copies of the pre-FP2 masters (spikes/FP2/before/) BEFORE any FP2 change, textures included.
- `montage.py`, `pack.py furniture|site` (repack from the restored tree), `tlog.py`.

## 1 Firewood: DONE (masters built; pack at the end)
- Cause: B3b's stacks were a sooted box with flat 4-sided end decals (`stack_caps`), B3a's 3-5 sided prisms; and
  M1's end-grain texture drew ~25 rings 4.5 px apart on 256 px at 22 % contrast, which mips to flat yellow.
- `spikes/B3a/woodpile.py` (new, shared): split billets (halves, quarters, thirds, small rounds) dropped onto the pile's
  skyline, bark on the arc faces (smooth radial normals), split faces flat, end grain mapped from each ROUND's pith
  (the bark ring at the rim), front ends staggered +-3 cm and cut a little off square, a dark core 7 cm back, loose
  billets across the top (the first lies split face up = the B3a loot point). Res 2 = the same front end faces + a
  stepped block (free-standing stacks: back ends as one quad each). Billet size picked to fit the face budget.
- B3b `jp_s_firewood_stack_*` (wall h120 / h180 / half / ab_collapsed / free_posts): same origin, wall plane z = 0,
  stack z 0.05-0.38, x +-0.91, same collision boxes. Budget small -> **medium** (1,500): R1 1,242-1,377.
- B3a `jp_f_firewood_stack` / `_low`: budget small -> **furniture** (1,000): R1 650 / 356. Bundles: stick ends now
  map a whole small round (were world UVs).
- Materials (`research/materials/make_fp2_materials.py`, same ids / paths / palette): `jp_m_wood_endgrain_firewood`
  512 px, ~11 clear rings + faint ones, heartwood, sapwood band, bark ring, V drying check + radial checks, saw arcs
  (_w0), more checks + grey (_w1), mould (_w2); unused corners balance the whole-PNG mean for the prop C1 checks.
  `jp_m_wood_firewood`: u 0-0.5 oak bark (plates, fissures, lichen), u 0.5-1 split wood (fibres, splinters, checks);
  was the Weathered Planks photo (joints, nail holes). C1 PASS x5, WARN _w2 end grain (dE 5.0 / 8).

## 2 Usu / kine: DONE (masters built)
- `jp_f_usu_mallet`: the yokogine's head lies in the hollow (both end circles on the bowl, solved on the faceted
  lathe), the handle rests on the rim's inner edge, rising ~4 deg. `jp_f_usu`: the tategine stands on the floor 0.44 m
  out and leans 16 deg on the rim's outer edge (contact solved with its real radius). `jp_f_usu_fallen`: the pounder
  moved clear of the mortar (it passed through its foot). Mortar 10 -> 16 sides, base flat on y = 0 (checked).
  No penetration (sampled check), still small class (R1 163-216).

## 3 Rope 2.5x: DONE
- `spikes/B3b/ropekit.py` (new): ROPE_K = 2.5 on BOTH the sides round the rope and the segments along it; smooth
  tubes (per-vertex normals) along a Catmull-Rom curve, caps as a quad fan; `cull` drops faces that can't be seen.
  Rope / cord materials only (straw_rope, textile_*); a bent handle, grass stems or the pine trunk drawn with
  rope_path get the smooth tube but keep their counts. Res 2/3 keep the old cheap shapes.

| Helper (users) | Before (sides x along) | After |
|---|---|---|
| w2kit.twisted_rope (shimenawa, rope torii, trunk wraps) | 3 / 4 per strand, a segment per pitch/4 | 8 / 10, pitch/10; strand faces inside the lay culled (and those pressed on a trunk) |
| lkit.coil / flat_coil (rope pegs, skeins, wheel rims) | 10 x 4 (inner 8 x 3) | 25 x 10 (20 x 8), smooth; wall-facing faces culled on the pegs |
| skit.rope_path (wells, laundry ties + net, nio, carts, sandal thongs, ...) | prism per segment, 3-5 sides | one tube, 8-13 sides, 2.5x the segments on bends (straight 2-point ropes stay 1 segment) |
| lkit.cord (hanging strings, sign cords) | 3 sides | 8 sides |
| bits.rope_ring (tawara / komo / bale ties) | 3-segment flat band | round 8-segment section; round the host it keeps the host's n (a rounder tie would float off the bale's facets) |
| fp1sword._cord (sword sageo) | 4 sides, 3 cm | 7 sides (1.75x: 2.5x would take the rack over 1,500), 1.2 cm |

- Budget classes raised (all within the 1,500 prop ceiling): shimenawa x6 -> medium (945-1,402); mini rope torii
  small -> box (572); laundry kaki / daikon -> box, net -> medium; nio cyl / cone and the tawara stack -> box; B3a
  tawara (all) small -> furniture (330 / 468); L1 rope pegs, hoshigaki, taru komo, charcoal burst -> furniture;
  katanakake furniture -> medium (1,418 / 1,438) (fkit.BUDGET gains 'medium' 1,500 = skit's); L2 footwear -> box, charcoal
  bales -> medium; S1 sg_yarn -> furniture. Rope torii stay medium (1,193-1,251).

## Build, checks, pack (11:52)
- Full builds: B3a 113/113, L1 185/185, S1 175/175 (--pack: jp_furniture 473 classes), B3b+W2+W3+FP1 231/231, L2
  81/81 (--pack: jp_site 312 classes); binarize 0 warnings; CfgConvert OK; TXT 211 text models 0 failing; C7 chain
  PASS. config.cpp / model.cfg identical to HEAD.
- Byte-noise: masters compared with pre-FP2 masters rebuilt from af3193e in the scratchpad (`changed.py`): 240 changed
  (B3a 10, B3b 63, L1 53, L2 27, S1 87); their ODOLs kept, 436 others restored to HEAD; PBOs repacked from the restored
  tree (`pack.py`) and read back (`pbocheck.py`: 473 / 312 ODOL, all = src). jp_common repacked (2 materials).
- Sheet: research/production/contact_sheets/fp2_fixes.jpg (`python spikes/FP2/sheet_fp2.py`).

## In-game checks for Stephen (no world rebuild needed: same p3d paths; FB2 rebuilds the world anyway)
1. Firewood outside the houses (and the kitchen stacks): split billets with bark and ringed ends, no flat decals.
2. Mochi building: the mallet's head in the mortar, handle on the rim; the pounder leaning on the rim, foot on floor.
3. Rope coils on pegs (round now), shimenawa / rope torii, well ropes, tawara ties.

## Not done / open
- Tawara / bale ties keep their host's sides round the bale (see table). The sword sageo is 1.75x sides.
- Wall coils: through the gap between the two loops you may glimpse the wall behind (culled back faces).
