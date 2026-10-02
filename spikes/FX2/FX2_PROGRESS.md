# FX2 progress: statues, komainu + kitsune, detail props, torii rope, U1 veranda (agent FX2, 2026-10-01)

Brief: the lead's FX2 brief (PRODUCTION_PLAN 2026-10-01 'Stephen's decisions'). Time log `japan_dev/TIMELOG_FX2.md`
(logger `python spikes/FX2/tlog.py "<event>" FX2 "<tag>" <5h> <wk>`).

## Status
- [x] references: 32 images / 20 objects (Met 7 + Cleveland 13), research/statues/REFS.md (Met v1 search retired
  2026-10-01 -> v1.1)
- [x] statue kit (sdf.py, statuekit.py, figures.py, statues.py, fx2props.py, peek.py, render_fx2.py)
- [x] material jp_m_gilt_worn (research/materials/make_fx2_materials.py; jp_common repacked)
- [x] altar daises (W2F props_w2f_sacred.image/dais), stone Jizo family + huts + steles + graves (B3b props_stone /
  props_grave jizo_figure -> mesh) built --no-binarize, checks pass
- [ ] komainu + kitsune props (spikes/B3b/props_guardian.py) + placement + lantern pairs
- [ ] detail props (masks, bells / gongs, ema, rope ends, offering box)
- [ ] torii rope (more sag, shide >= 2.30 m)
- [ ] U1 mawari-en
- [ ] rebuild + pack (B3b -> L2 --pack; W2F --pack; buildings), world + mission, checks, sheets, docs, push

## Resume notes
- Statue meshes are cached in meshes/<name>.json keyed by the source of sdf.py + figures.py: ANY edit there rebuilds
  every statue on next use (~3 min for all; `python spikes/FX2/statues.py`). Look: `sh spikes/FX2/peekall.sh [names]`
  -> _build/peekall.png.
- Budget classes added (additive): fkit.BUDGET detail 1500 / statue 4500 / altar 5500; skit.BUDGET statue
  (4500, 1700, 700) / detail (1500, 600, 250).
- B3b build.py rewrites jp_site config without L2: always finish with `python spikes/L2/build_l2.py --pack`.
  W2F: `python spikes/W2F/build_w2f.py --pack` after any B3a / L1 / S1 build.
