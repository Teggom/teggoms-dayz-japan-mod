# FX5 progress: fixes from Stephen's 3a / 3b walk (agent FX5, 2026-10-02)

Time log `japan_dev/TIMELOG_FX5.md` (logger `python spikes/FX5/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Stop rule: weekly usage 88 % -> checkpoint, commit + push, resume note here.

## Status
- [x] 1 compound gate floors flicker (z-fight)      - [x] 2 plaster-to-fence gap at the honjin (+ hedge slits)
- [x] 3 hedge rebuilt (continuous, new textures)     - [x] 4 U9 corridor: recorded as deferred work (NOT fixed, Stephen)
- [x] island rebuilt (world + mission, verify_oprw)  - [x] checks  - [x] TEST_CHECKLIST.md  - [x] plan / token log

## 1. Gate floors flicker (all compound gates)
- **Root cause (verified):** `templates/dwelling.compound()` laid each gate passage as `FL.doma(..., y=0.0)`: an earth slab
  whose top face lay exactly AT grade (11.8 m2 at the honjin, ~4.7-7.1 m2 per compound) = coplanar with the terrain
  (z-fight). The 3 stepping stones' flat tops were only 2 cm over grade too. All 9 compounds share the template
  (D3: samurai_m, headman_east, honjin, merchant, kumi, doshin; W3B: stableyard, timberyard, foundryyard).
- **Fix (kit level):** `floors.sill_pad()` (new): a packed-earth sill pad, flat top 0.10 over grade, sloped margins
  (0.35 m, 20 deg) running down to 3 cm UNDER grade at the rect edge (no lip on flat ground, walked over without a
  stumble), one convex solid in Resolution 1-2 + Geometry (R3 shows the terrain alone), Roadway 'doma' on the top and
  the four slopes; `floors.sill_height()` for things lying on it. `compound()` uses it for every gate; loot floor at
  0.10; stepping stones sit 3.5 cm proud of whatever surface they lie on. Gate leaves lifted over the sill:
  `sitewall.gate_kabuki / gate_munemon(leaf_y0=...)` (+ the action point / clear-width floor at the sill), passed by
  `dwelling._gate_part` (0.13; default unchanged for every other user of the gates).
- **Why 0.10 and not a few cm:** the W3B timber and foundry yards stand sunk 0.09 / 0.055 on their slope, so the terrain
  at their gates is +0.055..0.062 over the object's grade: a 0.06 pad would have been coplanar there again.
- **Sweep (spikes/FX5/gradesweep.py over the built ODOLs):** at-grade up-facing area now 0.00 m2 on all 9 compounds
  (was 4.7-11.8). Remaining 'near-grade' area = the board fences' downward-facing bottom edges at +0.04 (invisible).
  **Not fixed:** the two corridors (`jp_roka_honjin` 0.44 m2, `jp_roka_temple_u` 0.35 m2): small soseki stone faces at
  grade from K3's corridor kit; fixing them changes U9, which Stephen said to leave exactly as it is.

## 2. Plaster-to-wood joint (honjin) + every material transition
- **Measured in the built geometry** (`spikes/FX5/jointcheck.py --all`: every run end, corner and gate post of all 9
  compounds, placed as on the island with every object within 25 m; Geometry, View Geometry and Resolution 1 sliced at
  0.35 / 1.0 / 1.6 m; a flood fill from 1.5 m inside must not reach 1.5 m outside; gap = the dilation that seals it).
- **Before** (`_joint_before.txt`): honjin NE + NW, dobei street wall vs the side board fences: **0.68-0.72 m gap** in
  Geometry, View and Resolution 1 (walk-through and see-through: the fence runs started half a ken south of the wall
  line and the 0.30 dobei ends squared at the fence centreline). Kanto headman hedge: **0.08 m slits** at all 4 corners
  and at the back-gate post (the hedge core stopped short of the corner mitre / the post face). Samurai fence and
  headman hedge vs their nagaya-mon: sealed. Kumi yotsume: open by design (see-through bamboo grid, free lane ends).
- **Fix (template level, generic):** `dwelling._abut()` finds an open run end whose line meets another run's wall
  within 1.5 ken and extends that run to the other wall's near face (`_wall_path(abut=...)`, an off-grid end module;
  its end post stands against the face). Honjin: both side fences now reach the dobei's inner face (+0.76 m each). The
  hedge: corners mitred exactly like the wall bodies and the body / core stop 1 cm INSIDE gate posts.
- **After** (`_joint_after.txt`): all 56 checked joints sealed in Geometry, View and Resolution 1 (plus kumi's 4, open by
  design).

## 3. Hedge (jp_p_hedge_ikegaki; Kanto headman H3)
- **Root cause (verified):** `sitewall._hedge` built every module from its own rng (seed per module): lumps (convex
  rings) restarted in each module, the core box was inset at the module ends, UVs were module-local, and the body was
  `plant_foliage`, an alpha-CUT card material (30 % holes) on solid boxes: the holes showed the inside, so it read as
  speckled paint.
- **Fix:** new `_hedge` (sitewall.py): one battered section with rounded top edges swept along the module; surface
  moved by smooth value noise of the RUN coordinate (s along the whole wall path: `wall(run=(s0, seed))`, passed by
  `run_wall` and `dwelling._wall_path`), amplitude 4.5 cm (overgrown 9 cm), faded to zero at corners / posts / free
  ends; continuous UVs (u = s / tile, v = arc round the section); smooth per-vertex normals (new optional `vn` on a
  Solid, written by `core.Part._visual` like fkit's smooth lathes and turned by `Solid.transformed`); far LODs = the
  clean section; Geometry + View = a mitred core (Fire added by the compound as before); fringe = two-sided alpha
  sprig cards along the top edges and top (overgrown: also the faces), placed by the run coordinate.
- **New materials** (`research/materials/make_fx5_materials.py`, palette foliage_green, C1 PASS):
  `jp_m_plant_hedge` (opaque 1 m tile of small leathery leaves in three depth layers) and `jp_m_plant_hedge_fringe`
  (alpha-cut 2 x 2 sprig atlas). jp_common repacked.
- Faces: headman compound R1 8,800 (budget 12,000). Parts rebuilt:
  `jp_p_hedge_ikegaki_low / _tall / _end / _corner / _ab_overgrown`, `jp_p_wall_site_step_ikegaki_030`.
- Sheets: `research/production/contact_sheets/fx5_hedge.jpg` (eye-level before / after along a run, front, corner,
  wide), `fx5_hedge_variants.jpg`, `fx5_gates_joints.jpg`. Judgement: continuous, no visible module seams or bulges;
  reads as a well-kept clipped hedge. Possibly a touch too flat / uniform at eye level: judge in game.

## 4. U9 corridor: deferred (Stephen's decision)
PRODUCTION_PLAN.md "Confirmed future work": "Modular host variants for corridors (end of production)"; K3_NOTES.md §6
note. U9 and the halls untouched.

## Commits
See PRODUCTION_PLAN.md log (FX5 DONE).

## How to resume / re-run
- Compounds: `cd buildings && python pipeline.py dw_cmp_samurai_m dw_cmp_headman_east dw_cmp_honjin dw_cmp_merchant
  dw_cmp_kumi dw_cmp_doshin tr_cmp_stableyard tr_cmp_timberyard tr_cmp_foundryyard --no-pack --jobs 4`, then
  `python -c "import pipeline; pipeline.pack()"`.
- Parts: `python parts/kit/build_parts.py --only jp_p_hedge_ikegaki,jp_p_wall_site_step`.
- Materials: `python research/materials/make_fx5_materials.py` (packs jp_common).
- Checks: `python spikes/FX5/jointcheck.py --all [--png]`, `python spikes/FX5/gradesweep.py`.
- Renders: `python spikes/FX5/render_fx5.py hedge|gate|joint --tag after`.
