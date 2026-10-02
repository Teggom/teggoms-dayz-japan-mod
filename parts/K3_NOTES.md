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

## 4. Recorded choices (found while building) -- see section 7, filled at the end of the run

## 5. Budgets (PLAYBOOK §12 is guidance)
- Fence / plain wall module per ken: aim <= 800 R1 faces (small prop class); tile-capped wall module per ken: <= 1,500
  (detail class: the cap is kawara geometry, rule 1).
- Corridor module per ken: <= 1,500 R1; a 3-ken straight <= 3,000 (small building class). A whole compound or corridor
  circuit assembled from modules is a building (standard / large class).
