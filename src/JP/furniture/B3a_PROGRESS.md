# B3a progress: interior props, wave 1 (research/interior/BUILD_LIST.md)

Agent B3a (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_B3a.md`.

## How it works
- Pipeline: `spikes/B3a/` (`fkit.py` kit helpers, `bits.py` shared pieces, `props_<group>.py` builders,
  `tansu.py` from the effort test, `build.py`, `render.py`).
- `python spikes/B3a/build.py [prop ...] [--no-binarize] [--pack]`: MLOD masters to `spikes/B3a/out/<cat>/`,
  checks to `spikes/B3a/checks.json`, sidecars `src/JP/furniture/<cat>/<prop>.prop.json`, `config.cpp` +
  `model.cfg`, binarized ODOLs in `src/JP/furniture/<cat>/`. `--pack` writes `@Japan/addons/jp_furniture.pbo`.
- `python spikes/B3a/render.py [prop ...]` renders `spikes/B3a/renders/<prop>_row.png` / `_lod.png`;
  `render.py --sheets` composes `research/interior/contact_sheets/b3a_*.jpg`.

## Done
| Prop | Models | Checks |
|---|---|---|
| jp_f_tansu (storage) | 4 | pass |
| jp_f_kama, jizai_kagi, mizugame, oke, tana, firewood, jar (kitchen) | 42 | pass |

## Next
Storage (nagamochi, kori, box, tawara, rack), heat/light (andon, hibachi, tabakobon), bedding (futon_stack,
futon_laid, mushiro), shop (zukue, choba_goshi, misedana, goods_general), debris. Then PBO, sheets, report.

## How to resume
Run `python spikes/B3a/build.py --list` to see what is registered; build the missing modules; check
`checks.json` summary; `render.py <prop>` and look at the PNGs before calling a prop done.
