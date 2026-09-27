# Spike T (terrain): credits and sources

## Elevation data (in the terrain)

**出典：国土地理院** (Source: Geospatial Information Authority of Japan, GSI).

The terrain uses edited elevation data. 国土地理院の標高タイルを加工して作成 (made by editing GSI elevation tiles).

| What | Detail |
|---|---|
| Tiles used | 標高タイル (GSI elevation tiles), PNG encoding: `https://cyberjapandata.gsi.go.jp/xyz/dem5a_png/15/{x}/{y}.png` (DEM5A, 5 m, laser survey). The holes are filled from `.../dem_png/14/{x}/{y}.png` (DEM10B, 10 m). Tile list: https://maps.gsi.go.jp/development/ichiran.html |
| Area | Hakone, Kanagawa. The outer caldera rim on the south-east side, towards Shiroganeyama and Yugawara. The patch centre is 35.1939 N, 139.0739 E. It is a 1.8 × 1.8 km window: 462 × 462 px at z15, about 3.9 m/px |
| Downloaded | 2026-09-26. 120 z15 tiles and 36 z14 tiles, cached in `japan_dev/data/T_terrain/gsi/` (git-ignored) |
| Licence | GSI content terms (compatible with PDL1.0 / CC BY 4.0): credit the source, and state that the data was edited. See FEASIBILITY.md §2.1 on the open Survey Act question for derived products before any public release |

**How the data was edited** (`tools/terrain.py`):
- The relief above the patch's 5th percentile was scaled vertically by 0.47, so the highest summit sits at about 177 m.
- The patch was moved onto a fictional 2048 m island. It is faded out towards the island's south side, the coast and the central test yard.
- It was combined with a generated coastline, beach and sea floor.
- It was flattened for a 200 m test yard at 25.0 m, a house pad, a gravel road bed, a sea-level canal and a pond basin.
- It was resampled to a 4 m grid.

## Other sources (read, not redistributed)

| Source | Licence | Used for |
|---|---|---|
| Bohemia Interactive, DayZ-Samples `Test_Terrain` (github.com/BohemiaInteractive/DayZ-Samples) | BI sample (read only) | Reference layout. I parsed `utes.wrp` (8WVR) to prove the file layout, the grid orientation, the cell-to-tile mapping and the object-height rule. Nothing from it ships |
| jetelain/bis-file-formats, `BIS.WRP/EditableWrp.cs`, `OPRW.cs`, `Matrix4P.cs` | MIT | Cross-checked the 8WVR field order and the dummy terminator object. My writer is my own Python code |
| BI community wiki: *Wrp File Format - 8WVR*, *DayZ:Generating navigation mesh*, *DayZ:Central Economy setup for custom terrains* (via web.archive.org) | wiki (read) | Format and procedure reference |
| pennyworth12345 terrain-surface gist (gist.github.com/pennyworth12345/27786cf99652e0018b9b2f0becaa0638) | public gist (read) | Confirmed the "black / R / G / B / alpha 128 / alpha 0" six-surface mask scheme. I decoded the exact slot mapping myself from vanilla data |
| InclementDab/DayZ-Editor `EditorTerrainBuilderFile.c` | read | The Terrain Builder object-import line format for route B |

## Game data referenced (not copied into our PBO)

These vanilla DayZ assets are referenced by path: surfaces `dz\surfaces\data\terrain\cp_*`, trees, bushes, rocks and gravel road parts, `house_1w01.p3d`, the pond water material, and ChernarusPlus's world config (inherited). The per-surface satellite colours (`tools/sat_colours.json`) are medians I measured from vanilla Chernarus satellite tiles.

No CC0 assets were downloaded for this spike.
