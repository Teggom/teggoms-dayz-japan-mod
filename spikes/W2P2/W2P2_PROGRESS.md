# W2P2 progress: curved roof `jp_p_roof_sori` + bracket sets `jp_p_frame_kumimono` (2026-10-01)

## Status: DONE
- [x] Research: `parts/W2P2_NOTES.md` (no web in this run, no temple photos in the repo: forms and proportions are
  general knowledge, marked GK, plus the in-repo sources)
- [x] `parts/kit/jpparts/sori.py`: the curved roof generator
- [x] `parts/kit/jpparts/kumimono.py`: bracket sets on a column grid
- [x] `parts/kit/jpparts/storey.py`: hakama skirt + upper deck (the cheap part of `jp_p_frame_storey`)
- [x] Hooks: `sori.nagare(part, S)` for W2P1's `nagare.nagare(..., curve=sori.nagare)`; `sori.kohai_fit(info)`;
  `sori.under(info, x, z)`; `kumimono.frame()` returns `bear_y` / `g_out` / `keta_y` for `sori.roof()`
- [x] Manifest: 18 variants registered (registry.py + build_parts.py --only), 234 parts, 0 check failures
- [x] Offline assemblies (`parts/kit/w2p2_assembly.py`): hall, hall_kokera, hondo, shoro: 23/23 each, binarized ODOL
- [x] Sheets: `parts/contact_sheets/w2p2_1_sori.jpg`, `w2p2_2_kumimono.jpg`, `w2p2_3_assemblies.jpg`

## Built
- `sori.roof(part, W, D, form, covering, bear_y, g_out, ov, gov, pitch=(t0, t1), curve=p, corner_lift, lift_span,
  tiers, spacing, ridge_courses, front_ext, ridge_z, walkable, inside_rafters, hafu_mat / paint, curved_rafters,
  front_bear_z)`. Forms irimoya / yosemune (hogyo on a square plan) / kirizuma / nagare. Coverings hongawara / kokera /
  hiwada / copper. Defaults: t0 0.42 -> t1 0.80 (hongawara), p 1.6, corner lift 0.30 (0.20 on gable roofs), eave
  depth g_out + 1.25, two rafter tiers at 0.26 m.
- `kumimono.frame(part, W, D, nx, nz, col_h, form, c, y0, covering, t_j, nakazonae, nageshi)`; forms funa, oto,
  mitsudo, degumi, mitesaki; corner sets (both sides' projecting members + diagonal arms / odaruki); kaerumata,
  kentozuka; `bracket_set`, `kaerumata`, `kentozuka`, `column`, `beam` usable alone.
- Parts: jp_p_roof_sori _irimoya_{hongawara,kokera,hiwada,copper}, _kirizuma_{hongawara,hiwada}, _hogyo_copper,
  _nagare_hiwada; jp_p_frame_kumimono _funa, _oto, _mitsudo, _degumi, _mitesaki, _degumi_corner, _mitesaki_corner,
  _kaerumata, _kentozuka; jp_p_frame_storey_hakama.

## Face counts (R1 / R2 / R3)
- Roof samples: irimoya hongawara 3 x 2 ken 4,434 / 1,643 / 803; kokera 3,470 / 1,112 / 556; kirizuma hongawara
  2,217 / 881 / 413; hogyo copper 2,834 / 694 / 270; nagare hiwada 1,598 / 520 / 238.
- Brackets per side sample (2 sets): funa 60, mitsudo 140, degumi 290, mitesaki 558; corner frames (4 corner sets):
  degumi 928, mitesaki 1,976.
- Assemblies: hall 8,174 / 2,675 / 1,131; hall_kokera 5,564 / 1,822 / 808; hondo 11,259 / 3,023 / 1,183;
  shoro 5,807 / 2,135 / 1,047.

## Verified offline
- Part checks (build_parts): C2, C3, C4 dims, C5, C7 closed/convex + Roadway on Geometry, C13 for the kawara roofs.
- Assemblies (`parts/w2p2_assembly_checks.json`): the FB2 z-fight resolver first (as buildings/pipeline.py), then C2,
  C5 LOD set + face budget, C7 closed/convex x3, floor Roadway, Roadway on Geometry, run_g3 (C11-C22: C12 no poke into
  a roof body, C13 tile seating, C15 silhouette R2/R3 vs R1, C16 far kawara, C19, C20 no z-fight), S1 hips shared
  (front and side surfaces meet on every hip), S2 covering >= 5 cm over the rafters, S3 brackets / columns / walls
  under the rafter undersides, S4 base rafters bear on the gangyo and the wall keta (<= 1 cm), binarize -> ODOL.

## Decisions I made
1. Surface = a function of the plan distance from each slope's own eave (+ a symmetric corner lift): hips meet exactly,
   nothing is warped afterwards. Plan flare of the corners is not modelled (elevation sweep only).
2. Straight two-tier rafters pivot on the bearing (temple halls); nagare uses curved rafters (thin roof over the
   porch, `curved_rafters=`).
3. Budget: flat hongawara pans (the covers carry the relief), 3-face covers, 6-face makito, rafters at 0.26 m.
4. Proof platforms: a light cut-stone platform in the assemblies (W2P1's stilts.kidan costs ~2,000 faces in R1 AND R2
   on a hall-size platform; W2S should know).
5. The shoro is checked against the LARGE budget (12,000 / 4,600 / 1,600): it fits the standard R1 / R2 (6,000 /
   2,300) but its R3 is 1,047 > 800. PLAYBOOK §12 has no tower class: Stephen's call.
6. Stand-in materials: hiwada and copper use roof_kureita until `roof_hiwada` / `roof_copper` exist (auto-switch).

## Missing materials (for the materials agent)
- `jp_m_roof_hiwada` (cypress bark, very fine courses, dark red-brown)
- `jp_m_roof_copper` (copper sheet, green patina, batten seams; specular a bit higher than wood)
- Nice to have: a darker / coffered `ceil_boards` variant for the eave ceiling (noki-tenjo) between bracket steps.

## Open / for the lead and W2S
- W2P1's kohai canopy under a curved roof: use `sori.kohai_fit(info)` for its main_t / main_ov / eave_y.
- The curved nagare's front eave is low with W2P1's default eave_y (kohai beam 1.31 m over the floor at the kohai
  line in the 2 x 2 ken sample): raise eave_y if the steps need more head room.
- No reference photos of temple halls in the repo and no web in this run: the renders were judged against the recorded
  proportions only. A references pass (Horyuji, Toshodaiji, a town shoro) would be worth a check.
- Engine: untested (offline proofs only). The roofs are walkable (Roadway on every cell + the ridge).

## Resume / rerun
- `python parts/kit/build_parts.py --only jp_p_roof_sori,jp_p_frame_kumimono,jp_p_frame_storey`
- `python parts/kit/w2p2_assembly.py [hall hall_kokera hondo shoro] [--no-binarize]`
- `python parts/kit/render_w2p2.py w2p2_1_sori | w2p2_2_kumimono | w2p2_3_assemblies`
- `spikes/W2P2/try_sori.py` (single roofs + part checks), `spikes/W2P2/c15_column.py <assembly> x z` (which solid is on
  top of a C15 column in each LOD), `spikes/W2P2/tagcount.py` (faces per tag per LOD).

## Commits
- b98e43f generators + assemblies; 68661cb manifest registration; then the sheets / final commit.
