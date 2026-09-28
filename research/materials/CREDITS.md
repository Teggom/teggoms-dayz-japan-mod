# jp_common material library: credits and licences

Written by `build_materials.py` from `data/materials/polyhaven/manifest.json`.

## Downloaded (all CC0 1.0, public domain; credited anyway)

Fetched by `fetch_sources.py` from the Poly Haven API (1k JPG: diffuse, `nor_dx` normal, roughness) into
`data/materials/polyhaven/` (git-ignored), with a generic User-Agent only. Licence: https://polyhaven.com/license

| Asset | Name | Authors | Real size | Page | Became |
|---|---|---|---|---|---|
| black_painted_planks | Black Painted Planks | Dimitrios Savva | 1.60 m | https://polyhaven.com/a/black_painted_planks | jp_m_wood_kuro |
| clay_plaster | Clay Plaster | Amal Kumar | 2.00 m | https://polyhaven.com/a/clay_plaster | jp_m_wall_arakabe, jp_m_wall_nakanuri (smoothed) |
| japanese_cedar_planks | Japanese Cedar Planks | Charlotte Baglioni, Rico Cilliers | 1.13 m | https://polyhaven.com/a/japanese_cedar_planks | jp_m_wood_street_dark, jp_m_wood_bengara, jp_m_wood_sooted |
| reed_roof_04 | Reed Roof 04 | Rob Tuytel | 2.50 m | https://polyhaven.com/a/reed_roof_04 | jp_m_roof_thatch |
| rock_surface | Rock Surface | Amal Kumar | 2.00 m | https://polyhaven.com/a/rock_surface | jp_m_stone_cut |
| rust_coarse_01 | Rust Coarse 01 | Dimitrios Savva, Rico Cilliers | 2.20 m | https://polyhaven.com/a/rust_coarse_01 | jp_m_metal_iron (rust layer) |
| seaside_rock | Seaside Rock | Dimitrios Savva | 2.00 m | https://polyhaven.com/a/seaside_rock | jp_m_stone_river |
| weathered_planks | Weathered Planks | Dario Barresi, Dimitrios Savva | 2.00 m | https://polyhaven.com/a/weathered_planks | jp_m_wood_weathered |
| white_plaster_02 | White Plaster 02 | Rob Tuytel | 1.00 m | https://polyhaven.com/a/white_plaster_02 | jp_m_wall_shikkui |
| wood_planks_grey | Wood Planks Grey | Rob Tuytel | 1.50 m | https://polyhaven.com/a/wood_planks_grey | jp_m_roof_kureita, jp_m_roof_kokera, jp_m_roof_kakigara (board grain) |
| worn_rock_natural_01 | Worn Rock Natural 01 | Rob Tuytel, Dimitrios Savva | 2.00 m | https://polyhaven.com/a/worn_rock_natural_01 | jp_m_stone_field |

Downloaded and not used: `patterned_clay_plaster` (its scalloped trowel pattern is decorative, wrong for nakanuri;
deleted from `data/materials/`).

## Procedural (no outside source)

Made by `make_textures.py` with numpy/PIL: `jp_m_wall_namako_tile`, `jp_m_roof_kawara` (ceramic surface only; the
tiles are geometry), `jp_m_roof_thatch_cut`, the board courses of `jp_m_roof_kureita` / `jp_m_roof_kokera` (grain
from Wood Planks Grey), the shells of `jp_m_roof_kakigara`, `jp_m_paper_shoji`, `jp_m_bamboo_weathered`,
`jp_m_metal_iron` (rust colour from Rust Coarse 01), `jp_m_straw_mushiro`, every wear overlay (moss, lichen, cracks,
splits, drips, rust, edge wear, streaks), and the swatch plaques (Arial from Windows, rendered to a texture).

## Vanilla DayZ referenced, not shipped

`dz\data\data\env_land_co.paa` (rvmat stage 7), `dz\data\data\penetration\*.rvmat` and
`dz\surfaces\data\roadway\*.paa` (named in the sidecars), class `HouseNoDestruct`.
