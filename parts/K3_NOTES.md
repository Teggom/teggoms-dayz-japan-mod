# K3 notes: the WALL KIT and the COVERED-CORRIDOR / KAIRO KIT (agent K3, 2026-10-01)

Research first, then the recorded choices the generators follow, then the API for D3 (section 6).
Code: `parts/kit/jpparts/striproof.py` (the shared strip-roof engine), `parts/kit/jpparts/sitewall.py` (wall kit),
`parts/kit/jpparts/roka.py` (corridor + kairo kit); proofs `parts/kit/k3_assembly.py`; sheets
`parts/kit/render_k3.py` -> `research/production/contact_sheets/k3_walls.jpg`, `k3_corridors.jpg`.

**Sources.** No web access in this run. **[R]** = in-repo: KEEP_CIVIC "Walls (the reusable wall kit)", KEEP_OUTDOOR
(fences group), research/outdoor/OUTDOOR_LIST.md R §8 + "U Gardens: Fences" (S165-S174), R_RURAL.md §8 (gates: post
gate, kabuki-mon, wicket), U_URBAN.md (itabei, kuro-itabei, tsuiji-bei, neri-bei, roka-bashi), BUILDING_LIST /
C_CIVIC_RELIGIOUS_LAYOUT #27 (kairo + tamagaki), #15 (dobei, loopholes every 1-2 ken), WORLD_CATALOGUE §2.8,
PARTS_GAP_AUDIT #3 (gate) / #5 (wall_site) / issue 9 (tile-capped earth walls need a clay bed + far cap block +
footings on uneven ground), PLAYBOOK §4 / §5 / §6.2 / §6.4 / §15. Local reference photos (data/playbook/refs, looked at
in this run): **c29_earthen_wall** (a Nara temple tsuiji: earth-coloured, horizontal rammed-earth lift lines, segment
joints every ~2 ken, a hongawara cap with round covers running front-to-back, a course of rough stones at the foot,
leaning timber props), **c25_tsuijibei** (a neri-bei: clay with roof-tile courses, tile cap, stone kerb),
**c16_hakone_sekisho** (black board fences of an official compound). **(GK)** = general knowledge of Japanese
building history, not checked against a source in this run; a later agent with web access should confirm those.

## 1. Era test (PLAYBOOK §1: did it exist, or still stand, in 1730?)

| Form | Verdict |
|---|---|
| tsuiji-bei (rammed earth, plastered or bare, tile / board cap) | IN: ancient (Nara-Heian palace and temple walls), still the temple and noble wall in 1730 [R KEEP_CIVIC; c29] |
| sujibei lines (3-5 white horizontal lines on a temple tsuiji) | IN as a rare temple swap: the line count as a mark of imperial-linked temples (monzeki) is an Edo-period custom (GK, verify the date the 5-line rank was fixed) [R KEEP_CIVIC "up to 5 lines"] |
| neri-bei (clay with roof-tile courses) | IN [R U_URBAN; c25] (built as an earth-wall finish variant here) |
| dobei / nuri-bei (timber-framed, plastered, tile cap) with namako lower panels | IN: plastered walls with tile caps on samurai, merchant and castle compounds (GK); namako panels on T3 work [R PLAYBOOK §6.2] |
| itabei, kuro-itabei (black-tarred, official / samurai) | IN [R U_URBAN, WC §2.8, c16] |
| yotsume-gaki, kenninji-gaki | IN: both named in Edo garden writing (GK: the gardening manual tradition of the late 17th-early 18th c.); the many "temple-named" styles are often later names (OUTDOOR_LIST warning) and are NOT built |
| shiba-gaki (brushwood), takeho-gaki (bamboo-branch bundles) | IN: old rustic forms (OUTDOOR_LIST "older and rustic") |
| ikegaki (clipped hedge) | IN: "the commonest yard fence" [R OUTDOOR_LIST S169] |
| nozura-zumi (rough natural stone, dry) | IN: plot / terrace / road-shelf walls [R OUTDOOR_LIST S173, T34] |
| uchikomi-hagi (roughly dressed faces, gaps packed with small stones) | IN: the castle / temple technique from c. 1600 (GK). The fully cut kirikomi-hagi is also pre-1730 at castles but belongs to the castle kit (WK1), not here |
| stone-faced earth bank (dote with a stone toe) | IN (GK: river and plot banks) |
| kabuki-mon (two posts + crossbeam, roofed or not), mune-mon (ridge gate on one row of posts) | IN [R R_RURAL §8; BUILDING_LIST "yakui-mon and kabuki-mon also front samurai houses and honjin"]; commoner gate rights by rank: verify local rules (OUTDOOR_LIST) |
| watari-roka (covered corridor between halls) | IN: shoin palaces and villas of the early 17th c. link halls by corridors (GK: Nijo-jo Ninomaru, Katsura); Zen temples link hondo, kuri and hojo by corridors round courtyards (GK) |
| nobori-ro (climbing covered stair corridor) | IN as a form (GK: Hase-dera's climbing corridor is medieval in origin; the standing one is a later rebuild: use the form, not that building) |
| kairo (cloister round an inner precinct) | IN: Horyu-ji (7th c.), Kasuga, Itsukushima are standing in 1730 (GK) [R C_CIVIC #27, KEEP_LANDMARKS hero shrine] |

Nothing here is banned: no glass, no modern block walls, no cement. Concrete-looking plinths stay banned (rule 3):
every stone footing is individual stones.

## 2. Wall forms and proportions (choices binding for sitewall.py)

Frame (all wall parts): the run along +x from 0 to L on the wall centreline z = 0, +z = the OUTSIDE (street / road)
face, y 0 = grade at the module. Module lengths 1/2 ken (0.91), 1 ken, 2 ken; ends on the half-ken grid (rule 9).
Every footing runs 0.40 m below grade so a module sits on +-0.3 m of uneven ground without showing daylight
(PARTS_GAP issue 9).

| Wall | Period form | Game numbers (choice) |
|---|---|---|
| **tsuiji-bei** | Rammed earth (hanchiku) between boards in lifts of ~10-15 cm, battered both faces, built in segments with vertical joints; finished bare (earth colour, lift lines show: c29), plastered earth colour, or white; a small roof on a timber cap frame: hongawara or sangawara tiles, or boards; a low course of rough stones at the foot (c29). Height ~2.1-2.7 m to the cap (GK) | Body 2.30 m, base 0.90 m thick, top 0.56 m (batter ~4 deg), stone foot course 0.25 m; cap = a strip roof over the top 0.56 + 0.26 eaves each side, ridge at ~2.80. Finishes: `_earth` (bare rammed earth, lift lines as relief, segment joints every 2 ken), `_plaster` (white shikkui), `_nakanuri` (earth-coloured plaster), `_suji5` (5 white lines over the earth-coloured plaster, rare temple swap), `_neri` (tile courses in clay: the c25 form). Caps `_tile` (sangawara-sized kawara field + noshi ridge), `_hongawara` (temple), `_board`. |
| **dobei** (nuri-bei) | Post-and-nuki frame plastered both faces, ~0.3 m thick, tile cap; hikae-bashira buttress posts on the inner face (GK); namako panels on the lower face of rich work | 0.30 thick, body 2.10, stone footing course 0.30 (individual cut stones), cap strip roof; finishes `_shikkui`, `_namako` (namako lower 0.90 on the outside face, the kit's walls.namako), `_kuro` (black board lower half: shitami boards over the lower plaster, official look); hikae posts on the inside every 2 ken (option). |
| **itabei** | Posts at 1 ken, nuki rails, vertical boards with battens (oshibuchi), a cap (kasagi board) or a small board / tile roof; black-tarred on samurai / official compounds (c16) | Posts 0.12 at every ken, boards to 1.80, kasagi board, or a strip-roof cap (`_cap_board`, `_cap_tile`). Wood `wood_weathered`; `_kuro` uses `wood_kuro`. |
| **yotsume-gaki** | Open grid: posts (log or thick bamboo), vertical bamboos at ~1 shaku, 3-4 horizontal bamboos, black palm-rope ties; 3-4 shaku high | Height 1.05, posts 0.09 log at every ken, vertical culms 0.035 at 0.30, 3 rails (two-sided: alternate faces), rope knots (`straw_rope` stand-in for black shuro rope). See-through: Geometry = one thin slab (blocks walking), View / Fire = posts only. |
| **kenninji-gaki** | Closed screen of vertical split bamboo, 3-5 pairs of split-bamboo battens tied with rope, bamboo cap (tamabuchi), log posts; ~6 shaku | 1.80 high, log posts 0.11 at every ken, the screen as split-culm strips (R1) on a backing panel, 4 batten pairs, cap. Full Geometry / View / Fire. |
| **takeho-gaki** | Bundled bamboo branches between battens | Variant of the brushwood build in `bamboo_weathered` |
| **shiba-gaki** | Brushwood packed between posts and bamboo battens; older, rustic | 1.50 high, posts + 3 batten pairs, irregular brush bundles (`wood_firewood` stand-in: no brushwood material) |
| **ikegaki** | Clipped evergreen hedge (kashi, podocarp, camellia, holly, tea), often grown on a bamboo frame | Trimmed: 1.40 high x 0.70 thick, a clipped box with chamfered top edges and lumpy faces in `plant_foliage`; `_tall` 2.0 (Kanto oak hedge); overgrown = shaggy, taller, gaps. Geometry = the box (blocks walking and view). |
| **nozura-zumi** | Unworked stones, dry, small packers, battered | Free-standing low wall 0.90 / retaining revetment (ishigaki) 1.20 / 1.80, batter ~75 deg, individual stones (rule 3), earth fill behind a revetment. |
| **uchikomi-hagi** | Stones with knocked-flat faces in rough courses, gaps packed | Same sizes, flatter faces, tighter joints, `stone_cut` faces with `stone_field` packers |
| **stone-faced bank** | Earth bank with a stone toe | 1.20 high bank, 2.4 m deep, earth faces (`ground_earth_bare`), a 0.50 nozura toe, moss decal patches |

**Gates in a run (PARTS_GAP #3, reusing W2C gates.gate_leaves):**
- **kabuki-mon**: two 0.21 posts 1.5 ken apart, the kabuki beam across the post tops (ends cut, projecting), two hinged
  board leaves (gates.gate_leaves '_board', into the compound); `_roofed` adds a small strip-roof gable on the beam.
- **mune-mon**: two main posts on the gate line carrying a ridge beam; a gable roof (front and back eaves, no rear
  posts); leaves as above.
- **wicket door (kuguri / wakido)**: a 1-ken wall module with a single hinged board door, clear 1.00 x 2.00 (D1 / D2:
  the period stoop-through wicket is too small, PLAYBOOK D9, so it is built at the game size).
- **wall ends at a gate**: the earth / plaster walls end in a squared return (`end` connector) against the gate post.

**Abandoned states** (dead world): `_ab_collapsed` (a 1-ken section down to a rubble / earth mound, broken ends, the cap
gone over the gap), `_ab_tiles` (cap tiles fallen: bare clay bed patches on the cap, broken tiles at the foot),
`_ab_overgrown` (hedge shaggy and gappy; fences leaning, vines and moss on the wall faces). Fences: `_ab_leaning`
(the panel out of plumb), `_ab_broken` (missing culms / boards).

**Slopes (terrain-step pieces):** `jp_p_wallstep_*`: one module with the body and cap stepped up by 0.30 or 0.60 at
mid-length (a vertical riser + the cap's end returns). Place the next module that much higher. Fences step at a post.

## 3. Corridor forms (choices binding for roka.py)

| Feature | Period form (GK) | Choice |
|---|---|---|
| Width | 1 ken between post centres is the common watari-roka; 1.5-2 ken for formal corridors | `width` 1 ken default (1.70 m clear between rails: D5 >= 1.00), 1.5 ken option |
| Floor | Raised boards on short posts (tsuka) on stones, often level with the halls' floors; some kairo are earth / stone floored (Horyu-ji) | Raised boards at `floor` (0.45 default = the kit's agari level), Roadway boards_ext, continuous across modules (joints on the post lines); a Geometry block under the floor (nobody crawls under) |
| Posts / head | Square posts 4-5 sun, a head tie (kashira-nuki) and the eave beam (keta) | 0.12 posts at every ken on soseki, tie beam underside at floor + 2.10 (D2 head room 2.05+), keta top at floor + 2.42 |
| Roof | A low gable roof along the corridor; boards (kokera / itabuki) on residences and villas, hongawara on temple kairo, hiwada / kokera / copper on shrine kairo; corners turn with a hip on the outside and a valley inside | The strip-roof engine: kirizuma along the run; L corners = hip + valley, T = two valleys, cross = four valleys; profile straight (board 0.40 pitch, tile 0.45) or curved sori (W2P2's profile maths); coverings itabuki / kokera / hiwada (board family) and sangawara / hongawara (tile family, straight profile) |
| Sides | Open with a low railing, a half wall (koshi-kabe boards) with the upper part open or shuttered, or enclosed: plaster or boards with vertical-bar windows (renji-mado) | `open` (W2P1's koran rail, plain), `half` (board koshi to 0.90 + top rail), `enclosed` (plaster wall with a renji window per ken), `blank` (plaster, no window), `none` |
| Kairo | One bay wide (tanro), outer side a wall with renji windows, inner side open to the court (GK: Horyu-ji) | `kairo=True` = outer side `enclosed`, inner side `open` |
| Level change | Climbing corridors (nobori-ro) run as covered stairs; roofs step | `jp_p_roka_stair`: a 2-ken stair module rising 0.455 / 0.91 (14 / 26.6 deg <= 38, D4) whose roof is at the UPPER level and oversails the lower module's roof with a hafu + board gable infill (the stepped roof) |
| Connector | A corridor meets a hall at its veranda / wall, roof tucked under the hall's eave | `jp_p_roka_connector`: a half-ken end piece whose roof ends plain against the host wall with a flashing board; floor butts the host floor edge. API `roka.connector_fit(host_eave_soffit_y, ...)` says whether the corridor ridge fits under the host's eave |

## 4. Recorded choices (found while building)
1. **One roof engine for both kits** (`striproof.py`): the surface is d(p) = max over corridors of min over their
   eaves of the plan distance in from that eave (min = ridges and hips, max = valleys). Every module evaluates the same
   function, so ridges, hips and valleys line up across module joints with nothing warped afterwards. A straight
   module next to a junction cell cuts its own overhang on the VALLEY line (`branches=`); the overhang square at an
   inner corner is shared by the two straight modules, never by the junction cell. Modules never overlap.
2. **Coverings are clipped, not refitted:** kawara.field / eave_tiles (rule 1 geometry) are generated over the slope's
   frame and clipped in plan to each facet (hip and valley cuts); valleys get a half lining on each side (valley
   kawara / boards) so no two modules draw the same strip. Curved (sori) roofs use W2P2's profile maths in planar
   d-bands (band breaks depend on d only, so hips stay shared); tiles on a curve work the same way per band.
3. **Wall caps are strip roofs** (body 'solid': the clay / plaster bed and the collision go down to the wall top), so a
   wall corner gets a real hipped corner cap. T and cross caps exist in the engine; the WALL kit only uses corners
   (T / cross walls not built: rare); the corridor kit uses all three.
4. **Corner ownership:** the module whose END (x = L) is a corner builds the cap's corner cell; bodies mitre on the
   diagonal (battered tsuiji faces meet exactly because both runs share the section).
5. **Gate posts are the grid nodes:** a wall ending at a gate uses end 'post' (its body stops at the post face, its cap
   ends in a flush gable there). The kabuki beam sits at 2.91-3.15, above every wall cap of the kit (tsuiji ridge
   ~2.85), so nothing pokes a cap (C12).
6. **Steps** (`step()`): both caps end at the step in flush gables (no overhang, no oni) and the upper body's end
   closes the step; footings / fence Geometry run 0.30-0.40 below grade so a module tolerates +-0.3 m of uneven ground.
7. **Corridor heights:** floor 0.45 (agari level), head tie underside floor + 2.10, keta top (the roof's bearing line)
   floor + 2.42, eave 0.75, board pitch 0.40 / tile 0.45; 1 ken between post centres = 1.70 m clear (D5).
8. **Stair** (`stair()`): 2 ken, landings at both ends, risers <= 0.16 at 0.30 going (rise 0.455: 3 risers; 0.91: 6;
   both 26.6 deg), a hidden 'stair' Roadway ramp; its roof at the UPPER level oversails the lower roof with a gable and
   a board infill (each board a quad on both roof lines); the roof before a stair stops 7 cm short of the stair's posts
   and tie beam (C12). A rise of 0.455 clears a tile ridge by ~0.10.
9. **Connector** (`connector()` / `run_roka(connect=...)`): half a ken minus the host's wall half-thickness
   (`host_face`, 0.08 default); posts only away from the host; the roof ends plain at the host face with a flashing
   board; the floor reaches the face (the host's threshold must carry its Roadway to the same face).
10. **One object per building:** an MLOD of two halls + a 14-ken corridor (18k R1 faces) fails binarize with "Too many
   vertices". Keep one map object under ~15,000 R1 faces: split long corridor rings into several objects (one per side
   of the court is natural) and keep halls separate.
11. Wicket doors are built at the game size (1.04 x 1.96 clear, D1 / D2; the period stoop-through kuguri is D9's
   decorative case). All hinged leaves (gates.gate_leaves and the wicket) are **engine-untested** like every rotation
   door in the kit.
12. The tile corrugation restarts at every module start (columns from the module's own x 0): seams on whole ken keep
   the 7-column phase; a half-ken module shifts it by half a column (barely visible).

## 4a. Missing materials (stand-ins used; none added in this run)
- brushwood / twig bundles for shiba-gaki (`wood_firewood` stands in)
- black palm rope (shuro-nawa) for bamboo-fence ties (`straw_rope` stands in)
- yellow-ochre plaster of temple sujibei walls (`wall_nakanuri` stands in)
- bare rammed earth with its lift layers (`wall_arakabe` + modelled lift ridges stand in)
- grass / turf for bank tops (`ground_earth_bare` + `decal_moss`)
- copper valley lining for curved temple roofs (kawara / board valley linings used)

## 5. Budgets (PLAYBOOK §12 is guidance)
- Fence / plain wall module per ken: aim <= 800 R1 faces (small prop class); tile-capped wall module per ken: <= 1,500
  (detail class: the cap is kawara geometry, rule 1).
- Corridor module per ken: <= 1,500 R1; a 3-ken straight <= 3,000 (small building class). A whole compound or corridor
  circuit assembled from modules is a building (standard / large class).

## 6. API for D3 (and every later shell agent)

All builders return a kit `Part` (frame: x along the run, z 0 = the wall / corridor centreline, +z = outside, y 0 =
grade). Place one with `building.merge(sub.transformed(yaw_deg, (x, y, z)))` (yaw 90 turns +x into +z). Every part
variant is also in `parts/manifest.json` (`jp_p_wall_site_*`, `jp_p_fence_*`, `jp_p_hedge_ikegaki`, `jp_p_gate_*`,
`jp_p_roka_*`, `jp_p_kairo`) for single-module use. Checks: run your building through `buildcheck.run_g3` after
`zfight.resolve` as usual (the proofs in `parts/kit/k3_assembly.py` show the pattern plus the extra walk checks).

### How to run a wall around a plot
```python
from jpparts import sitewall as W
# grid nodes (half-ken grid), axis-aligned; walk the plot CLOCKWISE seen from above (x east, z north) so the
# outside (+z of each module) faces out
nodes = [(0, 0), (0, 6 * KEN), (8 * KEN, 6 * KEN), (8 * KEN, 0)]
wall = W.run_wall(nodes, "tsuiji", closed=True, finish="plaster", cap="tile",
                  gates=[(1, 3 * KEN, "kabuki_roofed", 1.5 * KEN),     # (segment, offset from its start, kind, span)
                         (2, KEN, "wicket", KEN)])
building.merge(wall.transformed(0.0, (x0, 0.0, z0)))
```
- kinds: `tsuiji` (finish plaster | earth | nakanuri | suji5 | neri; cap tile | hongawara | board), `dobei` (finish
  shikkui | namako | kuro; `hikae=True`), `itabei` (`kuro=True`; cap none | board | tile), `yotsume`, `kenninji`,
  `shiba`, `takeho`, `ikegaki` (`size` low | tall), `ishigaki` (`stone` nozura | uchikomi, `H`, `retaining=True`),
  `bank`. `state=` collapsed | tiles | overgrown | leaning | broken for the dead-world look.
- Segment lengths must be multiples of 0.91; modules are split 2 ken / 1 ken / half ken automatically. Corners get the
  mitred bodies + the hipped corner cap; open path ends get finished ends.
- Single modules: `W.wall(kind, L, ends=(e0, e1), ...)` with ends `seam` | `end` | `post` | `corner+z` | `corner-z`
  (the other run leaves to that local side; the module whose END is the corner builds the cap corner).
- Slopes: place level modules at their own grade and put `W.step(kind, KEN, rise)` between them (rise 0.30 / 0.60;
  the next module goes `rise` higher). Modules tolerate +-0.3 m of ground under them.
- Map objects: walls are site objects; build a compound's walls as their own p3d (or a few, each < ~15,000 R1 faces),
  not inside the house p3d unless the house is small.

### How to cap a run with a gate
- In `run_wall`: `gates=[(segment, offset, "kabuki" | "kabuki_roofed" | "munemon" | "wicket", span)]`. kabuki /
  munemon spans: 1.5 ken (2.73 between post centres, ~2.5 m clear with the leaves open) standard, 1 ken minimum; the
  gate's posts sit on the grid nodes at offset and offset + span; the walls either side end with `post`
  automatically. A wicket takes a 1-ken slot (span = KEN).
- By hand: `W.gate_kabuki(span, roofed=True)`, `W.gate_munemon(span, covering="hongawara")`, `W.wicket(kind)` (kind
  itabei | dobei | kenninji, a 1-ken module with a 1.04 m door); give the neighbouring wall modules end `post` at the
  gate posts. Leaves swing into -z (the compound side): make sure -z is inside.

### Small gates + the gate-picker rule (FX6, 2026-10-02; use this for every new compound)
Stephen's 3c-1 walk: one 3.15 m kabuki-mon on every fence ("waaaay too big" for the paper yard's 1.05 m bamboo fence).
Research, sizes, sources: `spikes/FX6/FX6_NOTES.md`. New builders in `sitewall.py` (frame as every gate: posts on the
wall line z 0 at x 0 and x span, +z outside, leaves on the -z face swinging 90 deg into the compound; `leaf_y0` lifts
them over the compound's sill pad):
- `W.gate_kido_kata(span=KEN, fence, kuro, leaf_y0)`: single-leaf board gate: square posts 0.15 to 2.15 + cap board,
  latch post 1.26 m from the hinge post, one board leaf 1.86 high (clear 1.08 x 2.05 over the sill), a fixed panel of
  the fence's boards beside it. For board fences and hedges.
- `W.gate_kido_ryo(span, kuro, leaf_y0)`: two-leaf board gate, posts 0.18 to 2.35 under a cap beam, NO kabuki beam;
  1 ken (clear 1.54) or 1.5 ken for carts / horses (clear 2.45). Leaves take the fence's wood (black in a kuro fence).
- `W.gate_shiorido(span=KEN, fence, leaf_y0)`: low bamboo lattice garden gate: round posts to 1.35, one diamond-lattice
  leaf 1.20 high (clear 1.11), the fence's own grid beside it, open above. For yotsume / kenninji / brushwood fences.
- `W.gate_opening(span, fence)`: two posts, no leaf (round to 1.35 in light fences, square to 2.10 in board fences).
- `W.gate_post_w(kind, fence)`: the post width the fence modules beside the gate stop at.
- Kept for status gates: `gate_kabuki` (+ roofed), `gate_munemon`, the nagaya-mon objects.

**In a compound** (`templates/dwelling.compound`), write each gate as `(run, segment, offset) + DW.pick_gate(fence,
fence_opt, status=..., role=..., carts=...)` (returns `(kind, span)`); naming the kind and span by hand is the explicit
override. `compound()` places doors for leaf gates, merges the opening as a plain part, lays FX5's sill pad under every
gate and stops the fences at the gate's own post faces (`_wall_path` gaps carry `post_w`; `_abut` seals run ends).

| Fence (height) | status high, front | high, back | mid (any role) | work, carts | work, on foot | lane (shared row entrance) |
|---|---|---|---|---|---|---|
| dobei / tsuiji (2.1-2.3) | kabuki_roofed 1.5 ken (or munemon / a nagaya-mon object) | kabuki 1 ken | kabuki 1 ken | kido_ryo 1.5 ken | kido_kata | kido_kata |
| itabei board fence (1.80) | kabuki 1.5 ken | kido_kata (kido_ryo 1 ken if carts) | kido_kata (kido_ryo 1 ken if carts) | kido_ryo 1.5 ken | kido_kata | kido_kata |
| ikegaki tall hedge | kabuki 1.5 ken | kido_kata | kido_kata | kido_ryo 1.5 ken | kido_kata | kido_kata |
| light: yotsume / kenninji / shiba / takeho / low hedge (<= 1.5) | shiorido | shiorido | shiorido | opening 1.5 ken | shiorido | opening |

status: `high` = samurai / official / honjin / temple; `mid` = headman, rich merchant, townsman; `work` = a trade yard.
role: `front` | `back` | `lane`. Gates are 1 ken unless the table says 1.5; spans stay on the half-ken grid.
`run_wall(gates=...)` still knows only kabuki / munemon / wicket: put the small gates in through `compound()` (or by
hand with `_wall_path(gaps=[(seg, off, span, W.gate_post_w(kind, fence))])` + the gate part, as
`spikes/FX6/render_fx6.gate_demo` does). Checks:
`python spikes/FX6/gatecheck.py` (handle conventions, D1, doors), jointcheck, gradesweep as before.

### How to link building A's veranda to building B with a corridor
```python
from jpparts import roka as R
fits, ridge_top, margin = R.connector_fit(host_soffit_y, floor=0.45, roof="itabuki")   # check BEFORE laying out
path = [(xa, za), (xc, za), (xc, zb), (xb, zb)]   # grid nodes; the first / last lie ON the hosts' wall lines
roka = R.run_roka(path, sides=("enclosed", "open"), roof="itabuki", profile="straight",
                  stairs=[(1, 2 * KEN, 2 * KEN, 0.455)],      # (segment, offset, length, rise) per level change
                  connect=(True, True), host_face=0.08)       # connector pieces at both hosts
```
- `sides` = (right of travel, left of travel): `open` (koran) | `half` | `enclosed` (plaster + renji) | `board` |
  `blank` | `none`. A KAIRO is the same call with the court on the open side (`("enclosed", "open")` when the court is
  on your left). Corners take the turn's outside kind on their outer sides. Segments between corners need >= 1 ken.
- `roof`: itabuki | kokera | hiwada | sangawara | hongawara; `profile="sori"` curves it (temple / shrine kairo).
- Floors: 0.45 over grade by default (`floor=`); match the hosts' floors at both ends. Each stair adds its rise to the
  floor after it (hall B sits that much higher).
- Host requirements: (1) the host's eave SOFFIT over the corridor (at the host's eave edge) must clear the corridor
  ridge top: `connector_fit(soffit)` gives the margin (floor 0.45: sangawara ridge top ~3.68 m, itabuki ~3.43);
  otherwise raise the host's keta, drop the corridor floor, or use a board roof; (2) the host's threshold carries its
  Roadway out to its wall face (`host_face` past the node); (3) the wall opening is >= 1.00 m wide, 2.00 m high (D1 /
  D2) and has no post in it.
- Veranda hosts: put the path end on the veranda's outer edge line (the connector floor meets the veranda deck at the
  same height; the veranda's own eave is the soffit to check).
- **Joining a corridor to its host halls is deferred to the end of production** (Stephen, 2026-10-02): the hosts' railing /
  wall openings, the alignment and the stairs at level changes are made once, on modular variants of the FINAL host
  designs. See PRODUCTION_PLAN.md "Confirmed future work": "Modular host variants for corridors (end of production)"
  (U9's three faults are listed there; the honjin J3 corridor worked).
- Single modules: `R.straight(L, sides, roof, profile, ends, branches)`, `R.junction(arms, sides={side: kind})`,
  `R.stair(L, rise)`, `R.connector(L)`. Junction cells are centred on the crossing of the centrelines; a straight next
  to a junction needs `branches=[(end, side)]` so its overhang is cut on the valley, and `posts0=False` when it starts
  at a junction (the cell has the posts).
- Keep one corridor object under ~15,000 R1 faces (about 10-12 ken of tile corridor): split a long ring by sides.

### Proofs (parts/kit/k3_assembly.py; results in parts/k3_assembly_checks.json)
`compound_corner` 24/24, `slope_fences` 19/19, `corridor_court` 24/24 (two stand-in halls + the corridor; binarized
as two objects), `kairo_segment` 22/22: C2, C5, C7, Roadway on Geometry, C10-C22 via buildcheck.run_g3 (C20 after
zfight.resolve), plus K3's walk checks KW1 wall line closed except at gates, KW2 terrain steps closed, KW3 Roadway
continuous hall -> corridor -> hall, KW4 slope <= 38 deg, KW5 head room >= 2.05, KW6 clear width >= 1.00, KW7
connector_fit; every object binarizes to ODOL. Sheets: research/production/contact_sheets/k3_walls.jpg,
k3_corridors.jpg (`python parts/kit/render_k3.py k3_walls|k3_corridors`).
