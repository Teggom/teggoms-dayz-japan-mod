# W2P1 notes: village-grade shrine + temple parts (agent W2P1, 2026-10-01)

Research-first record for the parts in `parts/kit/jpparts/{koran,tobira,nagare,ornament,stilts,shitomi,hokora}.py`.
No web requests were allowed in this run, and the machine holds no local photos of shrine or temple halls
(`data/research_okit/refs` has lanterns, basins, torii and steps only). Every form below is therefore **general
knowledge of surviving buildings and the standard terminology** (the JAANUS architecture dictionary entries named in
brackets are where a reviewer can check each term; no page was fetched). The binding rules are PLAYBOOK §1 (era test:
"did it exist, or still stand, in 1730"), §4 (D1 / D2 / D4 / D5 game standards), §15 (T1-T12) and C20.

## Period forms and the choices made

| Part | Period form (what a 1730 village shrine / temple shows) | Choice in the kit |
|---|---|---|
| **kōran** (高欄) `jp_p_porch_koran` | The railing of a hall's en (veranda). *Kumi-kōran*: a bottom sill on the floor edge (jifuku 地覆), a middle rail (hirageta 平桁), a round top rail (hokogi 架木) held up by short struts with a bearing block (totsuka 斗束). Corners: the rails cross and run out past the corner (the shrine form; the up-turned *hane-kōran* end is a curve). *Giboshi-kōran*: the runs end in posts (oyabashira 親柱) capped by an onion finial (giboshi 擬宝珠), usual at stair ends, bridges and better halls. Shrine en are *kirime-en* (切目縁): boards laid crosswise, end grain showing at the edge [JAANUS kouran, giboshi, kirimeen] | Both kōran forms; crossed-and-projecting corners (straight; `hane` = 0 hook for W2P2's curve), giboshi corner posts; kirime-en boards. Rail top 0.75 m (period 0.6-0.8 on small halls). Deck to the rail's inner face ≥ 1.00 m (D5): en edge on the grid at 1.365 m from the wall line (like `porch_engawa`) |
| **kizahashi** (階) | Wooden stairs from the ground (or a low hamayuka platform) to the front en, between side stringers, with their own kōran running down to giboshi posts at the foot; the en kōran stops at the stair (the gap) [JAANUS kizahashi] | Stair in the en kōran gap, side stringers + treads, stair kōran down to oyabashira (giboshi or plain). Hidden walk ramp ≤ 38° (D4; the run rounds UP to the 0.455 grid, so a 1.00 m floor gives 36.2°), ≥ 1.10 m clear between the stair rails. Stone at the foot |
| **wakishōji** (脇障子) | The board screen closing the rear end of a honden's side en | `_wakishoji` variant: post + framed board panel to the en's eave-beam height |
| **tobira** (扉) `jp_p_open_tobira` | Honden: paired hinged board doors (ita-tobira 板扉) turning on pivot blocks (warza 藁座), with metal straps (hasso 八双) and a meeting batten; latticed doors (kōshi-do) on many village honden and haiden fronts; temple halls: framed panel doors (sankarado 桟唐戸) [JAANUS itatobira, warza, sankarado] | Rotation leaves (DoorsTwinN, one animation, two bones; right-hand rule, PLAYBOOK §15 T4), opening OUT or IN by 90°. 1-ken bay: 1.70 m between the jambs, 2.00 m head (D1 / D2), so a game honden is enterable. Board, lattice and sankarado faces. **Engine-untested like every rotation door.** Iron stands in for the bronze fittings (no bronze material) |
| **nagare roof** (流造) `jp_p_roof_nagare` | The most common shrine form by far: a gable roof over the body (moya) whose FRONT slope runs on, unbroken, over the front aisle and the steps, carried at its end by the kōhai posts (向拝柱) with a beam and tie beams back to the body. Covering: cypress bark (hiwada) or shingles (kokera) on village halls; slight curve [JAANUS nagarezukuri, kouhai] | Straight (village) version, board covering `roof_kokera` (**hiwada is missing**). Same pitch front and back; the front slope's overhang `front` is a parameter (default: to the kizahashi foot + 0.45). Kōhai posts on stones, a beam under the rafters, sloping tie beams to the body's front posts (straight stand-ins for the curved ebi-kōryō) kept ≥ 2.05 m over the en and the stair. **Curve hook:** `nagare.nagare(curve=fn)` hands the full spec to a curved generator (W2P2's sori) instead of building the straight slopes |
| **kōhai** (向拝) `jp_p_roof_kohai` | A step canopy on the front of any hall: a short roof projecting from the main front eave over the stair bay, on two posts with a beam | A small board / tile slope parallel to the main front slope, its top tucked UNDER the main eave (no roof poke, C12), its own verges and hafu, two kōhai posts on stones, beam and tie beams |
| **hōgyō roof** (宝形造) `jp_p_roof_forms_hogyo` | The pyramid roof of square halls (Jizō-dō, Kannon-dō, Yakushi-dō, village dō), with a finial at the apex [JAANUS hougyouzukuri] | Square yosemune slopes from `roofs.slopes_for` (W = D degenerates to four triangles), board or tile coverings, hip rolls / hip ridges, apex cap; hōju from `ornament` |
| **chigi / katsuogi** (千木・鰹木) `jp_p_roof_ornament` | Crossed finials at the gable ends and logs across the ridge. Cut ends: vertical (soto-sogi) or horizontal (uchi-sogi); by the Ise convention vertical + odd katsuogi for a male kami, horizontal + even for a female kami. Built-in (shinmei, taisha, sumiyoshi) or placed on the ridge (okichigi 置千木). Nagare honden often have none; many village honden carry okichigi + katsuogi (regional, assumed) | okichigi pairs `_chigi_soto` / `_chigi_uchi`; katsuogi `_katsuogi_2/_3/_5` (generator takes any n 2-9). **W2S: make chigi / katsuogi a swap on nagare honden, not the default** |
| **ridge ends** | Board ridges end in a wooden ridge-end board (oni-ita 鬼板); tile hall ridges in a large onigawara | `_oniita` (board), `_oni_hall` (0.62 m kawara.onigawara, sui) |
| **hōju** (宝珠) | Square base (roban 露盤), inverted bowl (fukubachi), lotus seat and the flame-tipped jewel at the apex of hōgyō halls; bronze or tile | `_hoju_bronze` (iron stand-in), `_hoju_kawara` |
| **stilts** `jp_p_found_stilts` | Honden floors stand high (often ~1 m) on the extended main posts and floor posts, braced by underfloor nuki (床下貫), open beneath (yukashita); stores on posts with rat guards (nezumi-gaeshi) | Platform generator: posts on stones, two nuki rows, sleepers, board floor (Roadway), a Geometry-only block under the floor (nobody crawls under), dark void board; `_honden` open, `_hall` boarded skirt (haiden 0.60), `_ratguard` |
| **kidan** (基壇) `jp_p_found_kidan` | Bell towers and halls stand on a cut-stone platform: kerb stones (katsura-ishi 葛石), facing slabs, earth or stone top, a stone flight | Individual blocks (rule 3: never a smooth plinth), earth top, stone flight with a hidden ramp |
| **shitomido** (蔀戸) `jp_p_open_shitomi_grid` | Heian-derived lattice shutters of halls: a square grid on a backing board, the upper leaf hinged at the head and hooked up under the eave, the lower leaf lifted out; fixed lattice fronts (kōshi) on worship halls [JAANUS shitomido] | `_hinged` (upper leaf = rotation window, out and up 90°; lower fixed), `_closed`, `_open` (upper hooked up, lower removed: the bay is open), `_fixed` (see-through fixed grid over a board koshi) |
| **micro-shrines** `jp_p_site_hokora` | Stone shrines (sekishi 石祠): a roof stone on a body stone with carved doors, on base stones (gable, hip, nagare roofs, niche type); wooden hokora: a miniature nagare or shinmei shrine on a stone base, Inari ones painted shu, some inside a little shelter shed (saya) | 4 stone + 4 wood, site objects with no interior, convex collision, ≤ 1,500 faces |

## Gameplay over history (each one follows an existing PLAYBOOK deviation)
- Door head 2.00 m and 1.70 m between the jambs on a honden (D1 / D2): period honden doors are much smaller. A
  micro-shrine's doors stay decorative (D9).
- En 1.365 m deep (D5 ≥ 1.00 m clear) where a small honden's en is ~0.6-0.9 m.
- Kizahashi at ≤ 38° (D4) where period stairs are ~45°.

## Missing materials (not made: materials are not this agent's)
- **hiwada** cypress-bark roofing (shrine roofs; `roof_kokera` stands in)
- **bronze / copper patina** for giboshi caps, hōju, door fittings (`metal_iron` stands in)
- (town grade later) gold leaf

## Village-grade coverage (audit rows)
- SH2 haiden: was blocked only by kōran: unblocked. SH3 honden: nagare + kōran + tobira (+ stilts, ornament): unblocked.
- SH1 micro-shrines: hokora (4 stone + 4 wood). SH5 temizuya / SH6 office: buildable before this run.
- BU1 small hall: hōgyō + hōju + tobira + kōran. BU2 village hondō: kōran + tobira (+ shitomi). BU6 bell tower: kidan.
- Not made here: curved roofs and bracket sets (W2P2); see the end of this file for anything else left.
