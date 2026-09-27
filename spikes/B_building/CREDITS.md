# Spike B credits and licences

## Textures shipped in `jp_structures.pbo`

Downloaded by `tools/fetch_textures.py` (1k JPG: diffuse, `nor_dx` normal, roughness) into `data/B/polyhaven/`. All
are **CC0 1.0** (public domain, no attribution required; credited anyway). `tools/make_textures.py` recolours them
into `data/B/textures/*.png`, then `tools/build_b.py` converts them to `JP\structures\data\*_co/_nohq/_smdi.paa`.

| PAA set | Poly Haven asset | Authors | Real size | Page | Changes |
|---|---|---|---|---|---|
| `jp_tatami` | Tatami Mat | Charlotte Baglioni | 1.8 m | https://polyhaven.com/a/tatami_mat | none |
| `jp_plaster_white` | White Plaster 02 | Rob Tuytel | 1.0 m | https://polyhaven.com/a/white_plaster_02 | lifted to warm white |
| `jp_plaster_earth` | Clay Plaster | Amal Kumar | 2.0 m | https://polyhaven.com/a/clay_plaster | +8 % brightness |
| `jp_kawara` | Grey Roof Tiles | Rob Tuytel | 3.0 m | https://polyhaven.com/a/grey_roof_tiles | moss desaturated |
| `jp_timber_dark` | Japanese Cedar Planks | Charlotte Baglioni, Rico Cilliers | 1.13 m | https://polyhaven.com/a/japanese_cedar_planks | recoloured to dark stained timber |
| `jp_boards_floor` | Hinoki Planks | Charlotte Baglioni | 1.89 m | https://polyhaven.com/a/hinoki_planks | slightly aged |
| `jp_boards_ext` | Dark Planks | Rob Tuytel | 2.0 m | https://polyhaven.com/a/dark_planks | -10 % brightness |
| `jp_doma` | Clay Floor 001 | Dimitrios Savva, Rico Cilliers | 2.0 m | https://polyhaven.com/a/clay_floor_001 | -15 % brightness |
| `jp_stone` | Japanese Stone Wall | Rico Cilliers, Charlotte Baglioni, Dario Barresi | 1.9 m | https://polyhaven.com/a/japanese_stone_wall | none |

**Procedural (made by `make_textures.py`, no outside source):** `jp_shoji` (paper, kumiko grid, kick panel from the
hinoki texture), `jp_fusuma` (wave-patterned paper, lacquer frame, round pulls), `jp_plankdoor` (rotated Dark Planks
plus timber battens), `jp_koshi` (lattice slats from the timber texture over paper), `jp_mushiko` (plaster with
slots), `jp_tansu` (drawer fronts on the timber texture), `jp_ash`. Their `_nohq`/`_smdi` maps are flat constants.

## Vanilla DayZ assets referenced, not shipped

- Door sound sets `doorWoodSlideOpen/Close/Rattle/OpenABit` (`DZ\sounds`).
- Roadway surface textures `dz\surfaces\data\roadway\*.paa`.
- Penetration materials `dz\data\data\penetration\{dirt,wood,pottery,fabric_thin,granite}.rvmat`.
- `dz\data\data\env_land_co.paa` (rvmat environment stage).

## Reference only (not shipped, not redistributed)

- Bohemia Interactive **DayZ-Samples `Test_Building`** (`config.cpp`, `model.cfg`, `sample_building.p3d` MLOD),
  (c) 2019 Bohemia Interactive a.s., all rights reserved. Downloaded 2026-09-26 into `data/B/samples/` (git-ignored)
  to read the LOD, component, selection and memory-point conventions. https://github.com/BohemiaInteractive/DayZ-Samples
- Vanilla configs and binarized p3ds under `P:\DZ\structures\` (read for conventions only).
