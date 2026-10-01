# SH1 progress: the test-island showcase + Stephen's bundled walk (agent SH1, 2026-09-30 / 10-01)

Brief: one boot of the test island shows everything built so far: a shrine, a graveyard, S1's six demo shops on the
test street, a life-layer gallery (all 74 items), then ONE ~40 min walk in TEST_CHECKLIST.md. Time log:
`japan_dev/TIMELOG_SH1.md` (logger `python spikes/SH1/log.py "<event>" "<name>" "<tag>" <5h> <wk>`).

## Status: DONE (built, on the island, world + mission rebuilt, verify_oprw PASS 4076/4076; untested in game)

## Checks
- `layout_sh1.py`: 0 problems (375 CSV objects + 3 registry sheds; all 74 life-layer items present).
- `spikes/C3/dress_island.py`: 0 problems after the street change. `pipeline.py --combine-only`: config / model.cfg
  unchanged, C.csv 101 placements. Mission: 93 files parse; the 3 sheds now snap to their own wrp objects.
- Placecheck (run by build_world): 377 flags, 279 on SH1 objects, all by design or rule mismatches:
  156 "sunk" = the props' built-in footing / stake depth (gravestones 4-6 cm, slats and posts 15-26 cm, steles,
  basins) plus slope seating on the hill (oku-miya / Inari basins S74 / S85 up to 0.48 m on the uphill side);
  54 "rock" rule on stair landings (visible front <= 3.7 cm, the rest hidden under the next flight by design),
  torii footings, Jizo bases and huts; 32 "floats" = mounted items (wall / beam / shelf / eave / bench / the rope
  round the beech): placecheck only counts terrain and building Roadways as support; 27 "hanging" = the stone
  lanterns and the fallen paper lantern classed as hanging by their names; 8 edge floats <= 5 cm (boat hull, leaf
  piles, spilled loads: model shape); 2 leaning torii (S62, S82) lie 0.42-0.49 m into the slope at their uphill end.
  The C.csv / C3.csv flags are C3's known kinds (+9 gutters of the demo shops, sunk by design).
- Stair fitter: oku-miya stair 43 modules, worst gap under a block 0.059 m (6-step flights near the top), terrain
  at most 0.087 m over a first tread; Inari stair 16 modules, 0.030 / 0.090.

## Renders / maps (research/production/contact_sheets/)
sh1_shrine.jpg (9 views), sh1_graveyard.jpg (5), sh1_shops.jpg (9), sh1_gallery.jpg (6); labelled overhead maps
sh1_map_shrine.jpg, sh1_map_graveyard.jpg, sh1_map_gallery.jpg, sh1_map_street.jpg (`render_sh1.py`, labels by
`map_labels.py`); `SHOWCASE_MAP.md` = every ID -> class -> position (`showcase_map_md.py`).

## Not done / open
- Navmesh: the packed one dates from 2026-09-27 and is stale (as before SH1).
- The trees in the renders are stand-ins; the sacred-tree rope fit is measured, not seen in game.
- No hokora / shrine hall exist: stone-roofed huts and steles stand in.

## Where things are (world metres; spawn (1024, 985))
- **Shrine** north of the town street: first stone torii at (1024, 1099.5) behind the ward corner, the precinct
  (sando x 1024, z 1114-1198, hall site z 1186-1198 left empty), a sub-shrine row along x 1036, the oku-miya stair
  x 1042 z 1227.6-1262.8 (rises 34.1 -> 46 m), the Inari stair x 1058 z 1227-1240.
- **Graveyard** west of the approach: x 990-1013, z 1108-1130 (gate + water point + six Jizo on its east side).
- **Demo shops** on the C1 street (north side, z 1087.64): see "Street" below.
- **Gallery**: three open board sheds at (1072 / 1080 / 1088, 1036), fronts south; ground strip z 1020-1031.

## Files
- `spikes/SH1/shrine.py`, `graveyard.py`, `gallery.py`: the three areas (IDs S.., G.., L..).
- `spikes/SH1/terrain_sh1.py`: heightmap sampling, footprint seating (lowest corner), the stair fitter.
- `spikes/SH1/layout_sh1.py`: assembles them, checks (overlaps, buildings / door aprons / site objects via
  spikes/C3/dress_island.py, other drop-ins, T's tree trunks, p3d on P:), writes `test/placements/SH1.csv` and
  `spikes/SH1/showcase_items.json` (every object: id, class, p3d, position, label).
- `spikes/SH1/quickplot.py` (footprint plot), `pc_summary.py` (placecheck failures per model), `catdump.py`.

## Street (registry SH1 block, buildings/registry.py)
| ID | Demo shop | Where | How |
|---|---|---|---|
| D1 | Land_JP_Townhouse_Edo_3ken_Middle_ToriL_Kanamono (ironmonger) | x 1046.146 | replaced the bare Edo 3k board-roof middle unit |
| D2 | Land_JP_Townhouse_Kamigata_2ken_Middle_ToriR_Tabako (tobacco) | x 989.236 | inserted (no bare 2k middle on the street) |
| D3 | Land_JP_Townhouse_Kamigata_3ken_EndR_ToriL_Mochiya (sweets) | x 1003.238 | replaced the bare Kamigata 3k corner unit (row east end) |
| D4 | Land_JP_Townhouse_Edo_3ken_EndL_ToriL_Kusuri (apothecary) | x 1040.590 | replaced the bare Edo 2k end unit (row west end, one ken wider) |
| D5 | Land_JP_Townhouse_Edo_2ken_Middle_ToriR_Board_Shitate (tailor) | x 1050.824 | inserted |
| D6 | Land_JP_Townhouse_Kamigata_3ken_Middle_ToriL_Kyo_Ningyo (dolls) | x 984.558 | inserted |
- The bare Kamigata 3k end unit moved to the new west end (x 979.002). Positions from spikes/C1/layout.py place_row.
- `spikes/C3/dress_island.py`: the 5 free gutters in front of the replaced bare units dropped (the shops carry their
  own), the end unit's 2 gutters moved with it, the crossroads lantern and the scattered fire tub moved west of the
  apothecary. `python spikes/C3/dress_island.py` -> 0 problems; `pipeline.py --combine-only` -> C.csv, CE drop-ins.

## Decisions I made
- Shrine on the flat at the foot of the hill (sato-miya) + an oku-miya stair up the hillside: the island's hill north
  of the yard is 12-27 % near the foot and 30-45 % higher up; the W2 step modules climb at 52.7 %, so the stair only
  starts where the slope reaches ~27 % (z 1227) and every flight is followed by a short landing (visible 0.25-0.80 m)
  so the terrain catches up; the landing slabs run on, hidden, under the next flight. Worst gap under a block 6 cm
  (the 6-step flights near the top), terrain at most 9 cm over the first tread of a flight.
- A village shrine gets one torii in real life; the showcase deliberately carries every torii form: the main axis has
  3 (stone L plain at the town end, stone L rope + streamers at the precinct boundary, wooden myojin mossy rope +
  streamers inside), the 12 small ones stand as a row of sub-shrines (stone-roofed huts and steles stand in for
  hokora, which don't exist yet), the 5 plain-colour myojin span the hill stair, the vermilion ones are the Inari corner.
- Sacred tree: a vanilla beech (t_fagussylvatica_3f) with B3b's shimenawa_wrap_d06 round its trunk (trunk 0.65-0.69 m
  at 1.0-1.8 m, measured from the ODOL LOD 1; ring inner ~0.60 m: the rope bites in slightly). An old vanilla oak
  over the graveyard. Placement only.
- Graveyard: 7 rows, 16 plots a row in two blocks; 70 stones + 14 wooden posts; the old section at the back.
- Gallery: three bare Land_JP_Shed_Open_Board sheds (C2 shell, already shipped) through the registry, so no new prop
  was needed. Items are separate map objects at their decorator mounts.
- Bug fixed in `spikes/T_terrain/build_mission.py`: mapgrouppos snapping took the LAST wrp object of a class within
  10 m instead of the nearest; two of the three sheds (8 m apart) got their neighbour's CE position. Now the nearest.
