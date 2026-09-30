# L1 progress: the interior life layer (research/interior/LIFE_LAYER.md, items 1-50) — DONE

Agent L1 (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_L1.md` (logger `spikes/L1/tlog.py`, per-model
lines `spikes/L1/log_models.py`; props whose every model is an 'as left' state, e.g. the meal left out, were logged
as 'abandoned' throughout).

## Status
- **50 items = 185 models**: 50 new, 65 variants, 70 abandoned ('as left'). All checks pass (spikes/L1/checks.json,
  B3a's check_model: C1/C2/C4/C5/C6a/C8/C19/GEO/C6b/LOOT), binarize 185/185 ODOL, no warnings; CfgConvert OK.
- **jp_furniture.pbo** repacked: 297 `StaticObj_JP_F_*` classes (110 B3a + 2 B4 + 185 L1), all ODOL.
- **jp_common.pbo** repacked with the 4 new materials.
- Sheets: `research/interior/contact_sheets/l1_{a_wall,a_wall_2,b_religious,c_meal,c_meal_2,d_living,d_living_2,
  e_work,e_work_2,f_tier}.jpg`.
- Era: `research/interior/LIFE_LAYER_ERA.md` (50 kept; swaps inside #20 cups, #34 toys, #48 tea; none dropped).

| Section | Items | Models | Folder (src/JP/furniture/) |
|---|---|---|---|
| A walls, posts, beams | 1-14 | 46 | wall |
| B religious corner | 15-17 | 14 | religious |
| C meals and kitchen | 18-26 | 37 | meal |
| D living and bedrooms | 27-36 | 37 | living |
| E work at home | 37-44 | 29 | work |
| F tier markers + rest | 45-50 | 22 | tier |

Mounts (sidecar `mount`): floor 95, wall 32, surface 32, beam 16, post 4, doorway 3, kamado 3. Loot surfaces: 24
(cask and bale tops, mortar rim, millstone, manger bottom, coin box and armour chest lids, go / shogi board, straw
bed). Face budgets: every small prop <= 300 (max 300), the furniture-class pieces (cask rack 529, three charcoal
bales 396, spinning wheel with thread 315, loom, screens, clothes rack, butsudan, armour chest) <= 1,000.

## Materials added (B1 pipeline, add only: research/materials/make_l1_materials.py; C1 in checks_l1.json)
`jp_m_decal_sumi_text_life` (second ink atlas, fonts Yuji Syuku + Yuji Hentaigana Akebono: 4 ofuda, the Kyoho 15
calendar, 2 shop names, 2 crests, the daifukucho cover, 'morohaku'), `jp_m_food_rice`, `jp_m_food_hoshigaki`,
`jp_m_textile_kaya`; palette entries `rice_grain`, `hoshigaki`, `kaya_moegi` (assumed, judge in game).

## How the decorator mounts them (parts/kit/jpparts/decor.py)
- The catalogue reads each L1 sidecar's `master` (spikes/L1/out) and `mount`; B3a/B3b props get a mount from their
  anchor (wall -> wall, hang -> beam, else floor). `by_mount("beam")` lists what fits.
- `on_wall(name, room, x, z, yaw)`: wall / post items; (x, z) = the wall face point, the prop's +z into the room,
  y = the floor (heights are built in). D10 still checks that a wall is behind it.
- `on_beam(name, room, x, z, yaw, beam_y, over=None)`: origin at the beam underside; `hang_len` in the sidecar;
  D16 wants the bottom >= 2.00 over the floor unless `over` names a hearth / corner / furniture.
- `in_doorway(...)` for the inner noren (origin at the door head underside); `on_surface(name, host, surface, dx, dz)`
  puts small things on a placed prop's loot surface (D15 checks it rests there).
- Visual-only life items do not count against the 5-7 props of a room. D15/D16 are only emitted when such items are
  placed, so B4's furnished machiya keeps its 137 checks.

## Shared-code re-runs (decor.py changed)
- Furnished machiya (`buildings/machiya_t3_01_shop/verify.py`, standalone): 136/137 BEFORE and AFTER the change, the
  same single failure: "CE loot frame -> world" 5.9 m, which compares against test/ce/C_mapgroupproto.xml and only
  passes inside `buildings/pipeline.py` (standalone ordering). checks.json restored to B4's committed version.
- B3a / B4 prop checks (`spikes/L1/check_b3a.py`, sandboxed): 112/112 pass, faces unchanged.
- Townhouse combos: 60/60, 0 over budget, combos.json unchanged.

## Decisions I made
- Built INTO B3a's pipeline without editing it: `build_l1.py` appends the L1 modules and redirects masters, checks,
  logs; only L1 models are binarized. B3a's props untouched.
- New categories (folders): wall, religious, meal, living, work, tier.
- Small wall / beam / surface items are visual only (Res 1 proxies, vanilla small-item rule).
- A new text atlas rather than new cells in B1's (B1's material stays unchanged).
- Inner noren use plain indigo cotton (textile_noren fails C1 at _w1: dE 6.6 / 6; its _w2 is used nowhere by L1).
- The kaya's red edge uses jp_m_textile_bib_red; chillies use bib red too (paint_shu is shrine-only).
- Weapon racks' 'as left' state is empty (weapons are loot).

## Found, not mine to fix
- **Mirrored text:** DayZ model space is left-handed, so a decal whose u runs along +x on a +z face reads mirrored
  (B3a's renderer shows it). L1 uses `lkit.text()` / `lkit.uvcell()` (u mirrored). B3b's signs, kosatsu, lanterns and
  stone inscriptions use `skit.text_on` with +x and are likely mirrored in game: check at the next walk.
- The crest on the lacquered armour chest is ink on black lacquer, so it barely shows (the plain one shows it).

## Not done
- No in-game test. No building uses the life items yet (a decorator task). No navmesh work.

## How to rebuild
- `python spikes/L1/build_l1.py [prop ...] [--no-binarize] [--pack]` (short names, e.g. `taru`)
- `python spikes/L1/render_l1.py [prop ...]`, then `python spikes/L1/render_l1.py --sheets`
- Materials: `python research/materials/make_l1_materials.py [--no-pack]`
