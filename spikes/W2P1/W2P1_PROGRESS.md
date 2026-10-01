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
- [ ] 1 koran  - [ ] 2 tobira  - [ ] 3 nagare  - [ ] 4 ornament  - [ ] 5 stilts  - [ ] 6 shitomi  - [ ] 7 extras
- [ ] assemblies  - [ ] sheets  - [ ] pushed

## Commits
