# jp_common material library: credits and licences

Written by `build_materials.py` from `data/materials/polyhaven/manifest.json`.

## Downloaded (all CC0 1.0, public domain; credited anyway)

Fetched by `fetch_sources.py` from the Poly Haven API (1k JPG: diffuse, `nor_dx` normal, roughness) into
`data/materials/polyhaven/` (git-ignored), with a generic User-Agent only. Licence: https://polyhaven.com/license

| Asset | Name | Authors | Real size | Page | Became |
|---|---|---|---|---|---|
| bamboo_wall | Bamboo Wall | Amal Kumar | 2.00 m | https://polyhaven.com/a/bamboo_wall | jp_m_reed_yoshizu (reed rows) |
| black_painted_planks | Black Painted Planks | Dimitrios Savva | 1.60 m | https://polyhaven.com/a/black_painted_planks | jp_m_wood_kuro |
| clay_floor_001 | Clay Floor 001 | Dimitrios Savva, Rico Cilliers | 2.00 m | https://polyhaven.com/a/clay_floor_001 | jp_m_ground_doma_earth, jp_m_ground_doma_tataki |
| clay_plaster | Clay Plaster | Amal Kumar | 2.00 m | https://polyhaven.com/a/clay_plaster | jp_m_wall_arakabe, jp_m_wall_nakanuri (smoothed) |
| dry_decay_leaves | Dry Decay Leaves | Amal Kumar | 2.00 m | https://polyhaven.com/a/dry_decay_leaves | jp_m_ground_leaf_litter, jp_m_decal_litter (leaves) |
| hinoki_planks | Hinoki Planks | Charlotte Baglioni | 1.89 m | https://polyhaven.com/a/hinoki_planks | jp_m_floor_boards_int, jp_m_ceil_boards, jp_m_wood_interior |
| japanese_cedar_planks | Japanese Cedar Planks | Charlotte Baglioni, Rico Cilliers | 1.13 m | https://polyhaven.com/a/japanese_cedar_planks | jp_m_wood_street_dark, jp_m_wood_bengara, jp_m_wood_sooted |
| old_planks_02 | Old Planks 02 | Rob Tuytel | 2.00 m | https://polyhaven.com/a/old_planks_02 | jp_m_floor_boards_rough |
| reed_roof_04 | Reed Roof 04 | Rob Tuytel | 2.50 m | https://polyhaven.com/a/reed_roof_04 | jp_m_roof_thatch |
| rock_surface | Rock Surface | Amal Kumar | 2.00 m | https://polyhaven.com/a/rock_surface | jp_m_stone_cut |
| rough_linen | Rough Linen | colormass, Rico Cilliers | 0.27 m | https://polyhaven.com/a/rough_linen | jp_m_textile_cotton_indigo, jp_m_textile_cotton_plain, jp_m_textile_noren, jp_m_textile_kinari, jp_m_floor_tatami_heri (weave) |
| rust_coarse_01 | Rust Coarse 01 | Dimitrios Savva, Rico Cilliers | 2.20 m | https://polyhaven.com/a/rust_coarse_01 | jp_m_metal_iron (rust layer) |
| seaside_rock | Seaside Rock | Dimitrios Savva | 2.00 m | https://polyhaven.com/a/seaside_rock | jp_m_stone_river |
| tatami_mat | Tatami Mat | Charlotte Baglioni | 1.80 m | https://polyhaven.com/a/tatami_mat | jp_m_floor_tatami |
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

B1 (2026-09-29, `make_b1_materials.py`): procedural with numpy/PIL: `jp_m_floor_takeyuka`, `jp_m_ground_ash`,
`jp_m_ceramic_stoneware_dark` / `_pale`, `jp_m_lacquer_black`, `jp_m_straw_tawara`, `jp_m_bamboo_weave`,
`jp_m_decal_moss`, `jp_m_straw_rope`, `jp_m_wood_endgrain`, the four generic shop marks of `jp_m_textile_noren`
(drawn shapes, no font), the rib pass of `jp_m_paper_chochin`, and every B1 wear overlay. Built on library recipes:
`jp_m_wall_shikkui_int` (White Plaster 02), `jp_m_bamboo_sooted` (make_textures bamboo), `jp_m_paper_fusuma` /
`jp_m_paper_chochin` (make_textures shoji paper), `jp_m_stone_carved` (Rock Surface), `jp_m_straw_stack` (Reed Roof
04), `jp_m_paint_shu` (Weathered Planks). The rest use the Poly Haven scans listed above (see "Became").

## Fonts (SIL Open Font License 1.1), rendered into textures

`jp_m_decal_sumi_text` and `jp_m_decal_carved_text` (B1, 2026-09-29) are text atlases rendered from:
- **Yuji Syuku** (`research/fonts/yujisyuku/`), Copyright the Yuji Project Authors (Kinuta Font Factory), SIL OFL 1.1:
  every kanji.
- **Yuji Hentaigana Akebono** (`research/fonts/yujihentaiganaakebono/`), Copyright the Yuji Project Authors (Kinuta
  Font Factory), SIL OFL 1.1: the kana, drawn as hentaigana.

Fetched from the google/fonts repository (ofl/) by the lead; the licence text (OFL.txt) sits next to each font. Only
rendered text ships in the PBO, never the font files.

## Palette samples used by B1 (reference photos, local only, never shipped)

`doma_earth` and `ash_grey` were (re)sampled from the interior research photos in `data/research_int/refs/`
(Wikimedia Commons; full list in `research/interior/refs_index.json`): i01 / i02 Former Kasuya Family House by
Asanagi (CC0); i04 / i05 / i06 Farmhouse of Tsunashima Family by Kentaro Ohno (CC BY 2.0). Only a mean colour
was taken from them. `leaf_litter_autumn` comes from the CC0 Poly Haven scan dry_decay_leaves. Details in
`playbook/palette.json`.

## Vanilla DayZ referenced, not shipped

`dz\data\data\env_land_co.paa` (rvmat stage 7), `dz\data\data\penetration\*.rvmat` and
`dz\surfaces\data\roadway\*.paa` (named in the sidecars), class `HouseNoDestruct`.

## M1 (2026-09-30, `make_m1_materials.py`): the W2 / W3 / B3a material gaps
- **Text:** `jp_m_decal_carved_text_grave` and `jp_m_decal_sumi_text_grave` are rendered from **Yuji Syuku**
  (`research/fonts/yujisyuku/`, SIL OFL 1.1, the Yuji Project Authors). No new font. The Sanskrit seed syllables
  (bonji) were NOT made: no Siddham-capable font exists on this machine; the one that would do is Noto Sans Siddham
  (SIL OFL 1.1, google/fonts `ofl/notosanssiddham`), not downloaded.
- **Scans (CC0, already local):** `clay_floor_001` (jp_m_ground_earth_bare), `hinoki_planks` (jp_m_wood_new),
  `weathered_planks` (jp_m_wood_silver, jp_m_wood_firewood), `rough_linen` (jp_m_floor_tatami_heri_cha weave),
  `rock_surface` (the carved grave text), `bamboo_wall` (the wicker_aged colour).
- **Palette samples** (a mean colour only, never shipped; boxes in `playbook/palette.json` and `spikes/M1/sample.py`):
  k41 Sendabori Koshin-to, Matsudo (CC0); k37 Shikaumi Shrine sacred tree (CC BY 4.0); k27 Hida torii (PD); i04
  Tsunashima farmhouse (Kentaro Ohno, CC BY 2.0); k31 Toei Uzumasa (PD); c03 Tsumago-juku (CC0); i22 Kamado
  (CC0). Licences as listed in `research/outdoor_kit/refs_index.json`, `research/interior/refs_index.json`,
  `playbook/refs_index.json`.

## M2 (2026-09-30): Sanskrit seed syllables (bonji) on the grave atlas
- **Font: Noto Sans Siddham**, Copyright the Noto Project Authors, **SIL Open Font License 1.1**
  (`research/fonts/notosanssiddham/NotoSansSiddham-Regular.ttf`, licence text `OFL.txt` beside it; google/fonts
  `ofl/notosanssiddham`, fetched 2026-09-30 with Stephen's OK). The 9 `bonji_*` cells of
  `jp_m_decal_carved_text_grave` are rendered from it (shaped by Chromium's HarfBuzz via `spikes/M2/render_bonji.html`;
  masks in `research/materials/bonji_masks/`). OFL allows text rendered from the font in textures; the font itself is
  not shipped. Syllable choices: `research/outdoor_kit/W2_ERA.md` G16-G19.
