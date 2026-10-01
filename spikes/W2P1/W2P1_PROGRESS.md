# W2P1 progress (Phase C wave 2: shrine + temple parts, village grade; 2026-10-01)

Resumable notes. Time log: TIMELOG_W2P1.md (logger spikes/W2P1/tlog.py). Research notes: parts/W2P1_NOTES.md.

## Plan (modules under parts/kit/jpparts/, registered in registry.py; manifest via build_parts.py --only)
1. koran.py      jp_p_porch_koran      en deck + kumi-koran rails (plain / giboshi), corners, kizahashi, wakishoji
2. tobira.py     jp_p_open_tobira      hinged double board doors (out / in), lattice; jp_p_open_gate_leaf shares it
3. nagare.py     jp_p_roof_nagare      straight nagare gable (curve hook for W2P2), jp_p_roof_kohai step canopy,
                                       jp_p_roof_forms_hogyo (pyramid hall roof)
4. ornament.py   jp_p_roof_ornament    chigi (soto / uchi), katsuogi (n), oniita, hall onigawara, hoju + roban
5. stilts.py     jp_p_found_stilts     raised floor on posts + yukashita; jp_p_found_kidan (stone platform)
6. shitomi.py    jp_p_open_shitomi_grid  hinged grid shitomi (upper top-hinged), static, fixed lattice front
7. hokora.py     jp_p_site_hokora      4 stone + 4 wood micro-shrines; gate.py jp_p_gate (munamon / yakuimon /
                                       shikyaku) if time
Assemblies: parts/kit/w2p1_assembly.py (village haiden + honden on stilts; small temple hall); renders
parts/kit/render_w2p1.py -> parts/contact_sheets/w2p1_*.jpg

## Status
- [x] 1 koran  - [x] 2 tobira  - [x] 3 nagare (+kohai, hogyo)  - [x] 4 ornament  - [x] 5 stilts (+kidan)
- [x] 6 shitomi  - [x] 7 hokora (gate / genkan NOT built: W2C gates.py is the base)
- [x] assemblies (honden 26/26, haiden 25/25, temple_hall 32/32, ODOL)  - [x] sheets  - [x] pushed

## How to rerun
- parts: `python parts/kit/build_parts.py --only jp_p_porch_koran,jp_p_open_tobira,jp_p_roof_nagare,jp_p_roof_kohai,`
  `jp_p_roof_forms_hogyo,jp_p_roof_ornament,jp_p_found_stilts,jp_p_found_kidan,jp_p_open_shitomi_grid,jp_p_site_hokora`
- extra part checks incl. C20 after resolve: `python spikes/W2P1/ptest.py <module>`
- assemblies: `python parts/kit/w2p1_assembly.py` (writes parts/w2p1_assembly_checks.json, binarizes)
- sheets: `python parts/kit/render_w2p1.py w2p1_koran|w2p1_tobira|w2p1_roofs|w2p1_found_open|w2p1_hokora|w2p1_asm`

## Commits
- df69a85 koran; 66462c5 tobira + roofs + ornaments; (next) stilts/kidan/shitomi/hokora; final: assemblies + sheets
