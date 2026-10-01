# W2P2 progress (curved roof jp_p_roof_sori + kumimono)

## Status
- [x] setup, research (parts/W2P2_NOTES.md)
- [x] sori.py generator (irimoya / yosemune(hogyo) / kirizuma / nagare x hongawara / kokera / hiwada / copper)
- [x] kumimono.py (funa, oto, mitsudo, degumi, mitesaki + corner sets, kaerumata, kentozuka)
- [x] storey.py (hakama skirt, deck)
- [x] hooks: sori.nagare(part, S) for W2P1 nagare(curve=); sori.kohai_fit(info); sori.under(info,x,z)
- [x] assemblies (parts/kit/w2p2_assembly.py): hall, hall_kokera, hondo, shoro: 22/22 each (no binarize yet)
- [ ] manifest registration (W2P1 END seen 13:19)
- [ ] binarize, sheets, final commit, push

## Resume
- python parts/kit/w2p2_assembly.py [names]  (checks -> parts/w2p2_assembly_checks.json)
- python parts/kit/render_w2p2.py <sheet>  (w2p2_1_sori, w2p2_2_kumimono, w2p2_3_assemblies)
- spikes/W2P2/try_sori.py: quick single-roof part checks
