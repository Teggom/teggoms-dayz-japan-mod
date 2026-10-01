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

## 3 Rope: in progress
