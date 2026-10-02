# W3D progress: wave 3d, the government buildings (agent W3D, 2026-10-02)

Time log `japan_dev/TIMELOG_W3D.md` (logger `python spikes/W3D/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Setup / research notes: `spikes/W3D/W3D_NOTES.md` (sources, sizes, era tests, recorded choices, changes while
building). Stop rule: weekly usage 88 % -> checkpoint; not reached (84 % at start).

## Status: sites 1-5 DONE (built, packed, on the island, world + mission rebuilt; untested in game); site 6 (execution
grounds) see the end
- [x] notes  - [x] 1 checkpoint kit  - [x] 2 post-station office  - [x] 3 jinya (one size)  - [x] 4 jail
- [x] 5 tall fire watchtower + brigade  - [x] district + placement  - [x] world + mission  - [x] checks
- [x] sheets  - [x] checklist 3d  - [x] pushed

## New wall-kit pieces (`parts/kit/jpparts/sitewall.py`)
- `wall("saku", ...)`: the palisade (round logs 0.22 apart, pointed, two inside rails, logs 1 m into the ground).
- `gate_koraimon(span=1.5 ken)`: the kora-mon (roofed kabuki-mon + two rear posts under their own small roofs).
- `pick_gate`: fence `saku`, status high, role front -> `koraimon` 1.5 ken; other palisade gates `kido_ryo` 1 ken.
- `itabei` takes `skirt=` (boards / posts / collision run that much deeper: a fence seated on its high side).
- `dwelling.compound` plots take `pads=[(name, x0, x1, z0, z1, note)]` (gravel courts) and `pad_posts=[(x, z)]`.
- `dwelling.nagayamon(rank="official")`: black boards, board roof (the jinya's gatehouse).

## Shells (template `parts/kit/jpparts/templates/govsite.py`, recipe `buildings/govsitekit.py`, registry `W3D_SHELLS`)
| Family | Classes |
|---|---|
| gv_hall | Land_JP_Bansho_Sekisho (5 x 3.5 ken: stepped inspection front, office, kitchen doma), Land_JP_GinmiSho (4 x 3.5 ken court room), Land_JP_Toiyaba (5 x 3 ken, open front), Land_JP_Roya (4 x 3 ken, double lattice, 2 cells) |
| gv_site | Land_JP_Compound_Sekisho (palisade, 2 kora-mon), Land_JP_Compound_ToiyaYard, Land_JP_Compound_Jinya, Land_JP_Compound_Roya, Land_JP_Compound_Hikeshi, Land_JP_Oshirasu_Sekisho / _Jinya (gravel courts) |
| dw_samurai | Land_JP_NagayaMon_Jinya (D3 template, rank official) |

## Props
- furniture (`spikes/W3D/props_w3d.py`, cat govfit, `python spikes/W3D/build_w3d.py [prop ...] [--no-binarize]`):
  jp_f_mitsudogu_tate (+_ab), jp_f_kanme_hakari (+_ab), jp_f_matoi_nobori (+_fallen).
- site (`spikes/W3D/props_w3d_site.py`, cat gov_site, `python spikes/W3D/build_w3d_site.py`): the climbable
  Land_JP_S_Hinomi_Yagura (deck 6.40, roof 2.20 over it, hansho bell).

## Furnished (`buildings/w3d_sets.py`; registry `W3D_FURNISHED`, folder buildings/gv_furnished)
f_gv_bansho, f_gv_bunk_ashigaru (BunkHall_Itabuki_Ashigaru), f_gv_toiyaba, f_gv_ginmisho, f_gv_jinya
(Samurai_S_Jinya), f_gv_nagayamon_jinya, f_gv_kura_nengu (Kura_Plain_Nengu), f_gv_roya, f_gv_hikeshi
(Shed_Open_Board_Hikeshi). The jail's guard office = W2F's Land_JP_Guardhut_M_Itabuki_Jishinban as it is. The W3D halls
get a cut-stone foundation band (`_plinth`) for the slope.

## Island (`python spikes/W3D/layout_w3d.py` -> test/placements/W3D.csv + test/ce/W3D_mapgrouppos.xml; then
`python spikes/W3D/map_w3d.py` -> w3d_map.jpg + SHOWCASE_MAP.md W3D section; `python spikes/W3D/floorcheck.py`)
District x 744-826, z 845-892; one lane LG (z 862-866) from 3c-2's corner (826, 864) west through the checkpoint.

## Sheets
research/production/contact_sheets/w3d_family.jpg (`python spikes/W3D/render_w3d.py family`), w3d_rooms.jpg
(`python spikes/W3D/render_w3d_rooms.py rooms`, jobs `w3d_jobs.py`), w3d_map.jpg.

## How to resume / re-run
- Shells: `cd buildings && python pipeline.py <gv_key...> --no-pack --jobs 4`; pack `python -c "import pipeline; pipeline.pack()"`.
- Furniture / site packs: `python tools/assemble_config.py jp_furniture --pack`, `... jp_site --pack`.
- World: `python spikes/T_terrain/build_world.py`, `python spikes/T_terrain/build_mission.py`,
  `python spikes/T_terrain/tools/verify_oprw.py`.
