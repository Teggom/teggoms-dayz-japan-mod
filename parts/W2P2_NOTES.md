# W2P2 notes: curved roofs (`jp_p_roof_sori`) and bracket sets (`jp_p_frame_kumimono`)

Agent W2P2, 2026-10-01. Research first, then the recorded choices the generators follow.

**Sources.** No web access in this run (brief: no downloads). The repo has no photos of temple halls, so:
- **[R]** = in-repo sources: PLAYBOOK §1 (era test), §6.1 ("Temples and shrines use the curved, thick-edged kokera
  form"), §15 (T1 tile bed + fascia, T7b silhouette, T8 no poke); PARTS_GAP_AUDIT #17 / #21 / #10; KEEP_CIVIC (shrine
  and temple ladders, bell tower, sanmon, pagoda); C_CIVIC_RELIGIOUS_LAYOUT §2.2 #10-11, §3.2 #11, #14, #24-26;
  BUILD_LIST §325 ("hongawara temple roofs with a 7-course ridge, curved kokera and bark roofs").
- **(GK)** = general knowledge of Japanese temple carpentry (kiwari proportion systems, standard textbook forms),
  not checked against a source in this run. Every number marked (GK) is an assumption a later agent with web access
  should confirm.

## 1. Era (PLAYBOOK §1)

All forms here were established long before 1730 and still built or standing in 1730: wayō (Japanese style) bracket
sets and two-tier rafters from the Nara/Heian period, the hidden roof (noyane) with cantilever levers (hanegi) from
the Heian period, zenshūyō fan rafters and strong corner sweep from the Kamakura period, hakama-goshi bell towers from
the Momoyama/early Edo period (GK). Copper sheet roofing (dōbuki) is in: Tōshōgū (1636) and castle keeps used copper
(KEEP_CIVIC: Nagoya / Edo copper roofs) [R]. Copper is a rich / top-tier covering only.

## 2. The curved roof (sori)

| Feature | Period form (GK unless marked) | What the generator does |
|---|---|---|
| Roof profile | Temple and shrine slopes are **concave** (sori): steep near the ridge, flattening toward the eave. Upper pitch about 7-10 sun (0.7-1.0), eave pitch about 3-5 sun (0.3-0.5). The opposite (convex, mukuri) belongs to some houses and tea rooms. | Slope rate rises from `t0` at the eave edge to `t1` at the main ridge: t(d) = t0 + (t1 - t0) (d / R)^p, d = plan distance in from the eave edge, R = the main slope run; default t0 0.42, t1 0.80, p 1.6. Every slope of a hipped form uses the SAME function of d, so front and side slopes meet exactly on the hip. |
| Eave sweep (nokizori) | The eave line rises toward the corners. In wayō halls the eave is straight over the middle bays and lifts over the last bay or so at each corner; zenshūyō sweeps the whole eave. Corner lift on a town-size hall roughly 0.2-0.5 m (about 1/8-1/5 of the eave depth). | lift(e, d) = L f(e) g(d): e = distance along the eave from the nearest corner, f = (1 - e/Ls)^2, g = (1 - d/Ld)^2. Symmetric in e and d, so the hip line stays shared. `corner_lift` L (default 0.30), `lift_span` Ls (default 0.30 x the short side incl. eaves), Ld = Ls. Kirizuma: the lift is at the verge ends (the hafu sweep up too). |
| Corner members | Sumigi: the large diagonal hip rafter, in two tiers (jisumi / hien-sumi), carries the lifted corner; the hidden lever (hanegi) is inside the roof and not seen. | Two-tier sumigi along the hip in the eave zone, section 0.16 x 0.22, tip 0.10 past the eave corner. Hanegi not modelled (hidden). |
| Two-tier rafters (futanoki) | Base rafters (jidaruki) run from inside the wall line to an eave beam (kioi); flying rafters (hiendaruki) sit on the kioi and project to the eave fascia (kayaoi). Rafter pitch 1 shi; a 6-shaku bay holds about 8-10 shi. Round base rafters are older / zenshūyō; square in wayō. | Rafter spacing = bay / 8 (0.2275 m on a 1-ken bay), section 0.085 x 0.10 (base) and 0.080 x 0.09 (flying). Flying zone = the outer 42 % of the eave depth. Parallel rafters (wayō); they stop at the sumigi on hipped corners. `rafters=1` gives a single tier (village halls). |
| Eave edge stack | Kayaoi (fascia on the flying rafter ends); for kawara: urakō board and the kawara-zan bed under the eave tiles; for bark / shingle: the thick layered eave edge (nokizuke / koba), built of many courses, cut clean, 0.15-0.40 m thick. | Kayaoi along the curved eave in every LOD. Kawara: clay bed + fascia (T1) + round-end covers (tomoe) and karakusa pan lips. Kokera / hiwada: a three-band koba stack (each band 1-2 cm further out than the one above), 0.30 m / 0.24 m thick. |
| Ridge | Hongawara ridges: 5-11 noshi courses + a round cap (ganburi) + onigawara at the ends; status rises with courses (PLAYBOOK §6.1: 2-7 for houses) [R]. Bark / shingle / copper ridges: a box ridge (hako-mune) clad in the same material or copper. | Hongawara: 7 courses (param), onigawara 0.55 m. Board / bark / copper: a box ridge 0.38 wide x 0.36 tall with a cap. Irimoya also gets descending ridges (kudarimune) down the upper gable verges with small oni, and corner ridges (sumimune) down the hips. |
| Irimoya gable | The upper gable stands back from the side eave by about a quarter of the depth; it carries curved bargeboards (hafu) with a hanging fin (gegyo) at the apex; the gable face is boarded or latticed (kitsune-goshi). | Gable foot at D/4 (as the straight kit), boarded tsuma face, curved hafu boards following the verge, gegyo board at the apex. |
| Coverings | **Hongawara** (temples, castles, gates) [R]; **kokera** (thin sawara / sugi shingles, ~3 mm, exposure ~3 cm) curved and thick-edged on shrines and temples [R §6.1]; **hiwada** (cypress bark, very fine courses ~1 cm, dark red-brown) on shrines and temple halls of high rank; **copper** (sheet with batten seams, green patina) on the richest work. | `covering` = hongawara / kokera / hiwada / copper. Kawara: modelled pans + covers per 0.303 column on the curve, far material in Res 2/3. Board-like: curved smooth field with course steps in the eave rows, koba edge. Copper: seam ribs every 0.45 m. |

## 3. Bracket sets (kumimono / tokyō)

Members (GK): **daito** (big bearing block on the column top, with a bowl-cut lower part, about 1.4-1.6 x the column
top), **hijiki** (bracket arm, curved underside), **makito / masu** (small bearing blocks on the arm ends and middle),
**odaruki** (tail rafter: a diagonal member through the set, sloping down outward, that cantilevers the outer purlin),
**gangyō** (the outer purlin the last step carries, on which the rafters rest), **shirin** (curved infill boards
between steps), **kashiranuki** (head tie through the column tops with carved ends, kibana), **nageshi** (horizontal
bands on the column faces), **nakazonae** (inter-columnar supports: **kaerumata** frog-leg strut, kentozuka post with a
block).

| Form | What it is (GK) | Where (GK, [R] ladders) | Generator |
|---|---|---|---|
| funa-hijiki | A boat-shaped arm directly on the column top, no block: carries the keta | Shrine honden, simple halls, village grade | `form="funa"` |
| ōto-hijiki (daito-hijiki) | daito + one arm carrying the keta | Simple halls, bell towers (lower grade), gates | `form="oto"` |
| hira-mitsudo | daito + an arm parallel to the wall with three makito | Common on town halls, worship halls | `form="mitsudo"` |
| demitsudo / degumi (one step) | mitsudo + an arm projecting out one step | Town-grade halls, sanmon lower storey | `form="degumi"` |
| mitesaki (three steps) | Three projecting steps with odaruki, shirin, gangyō on the third step: the deepest eaves | Main halls of large temples, pagodas, sanmon upper storey, bell towers of rank | `form="mitesaki"` |

Proportions (GK, kiwari; all from the column diameter c, which defaults to 0.11 x the bay, min 0.18 m):
- daito: 1.5 c square, 0.75 c tall (the lower 40 % bowl-cut).
- hijiki: 0.45 c wide, 0.55 c tall; arm length 3.2 c for the three-block (mitsudo) arm.
- makito: 0.75 c square, 0.42 c tall.
- step projection (tesaki): 1.05 c per step; 3 steps put the gangyō about 3.15 c out from the column line.
- odaruki: 0.5 c x 0.6 c, at about 25 deg, its nose 0.5 c past the third step.
- kaerumata: 1.6 c wide x 1.1 c tall frog-leg profile on the head tie between columns, with a makito on top.

## 4. Bell tower (shōrō) [R C_CIVIC §3.2 #24]

"Open four-post pavilion (or with a flared skirt wall, hakama-goshi) over a stone platform." Choices (GK proportions):
- Hakama-goshi type: a lower storey 3 x 2 bays of 1 ken (5.46 x 3.64 m at the floor line) whose walls flare out
  (batter about 12 deg) to the base, boarded (or plastered); an upper floor at about 2.9 m with a balcony; four
  posts (plus intermediates) at the upper level holding a 2 x 1 bay bell room; irimoya curved roof; degumi or
  mitesaki brackets at the upper storey.
- Bell beam across the upper bay with a memory point `bell_hook` for the specialty prop (W2F).
- Total height about 9-10 m. The open four-post type is the same upper storey on a kidan (stone platform).

## 5. Choices recorded (binding for this generator)

1. The surface is a function of plan distance from each slope's own eave (Section 2): all hips meet exactly; nothing
   is warped after the fact.
2. Collision: one convex slab per plan cell (cells ~1.8 m along the eave x 4-5 bands up the slope), a least-squares
   plane per cell for top and bottom, so every component is planar-faced and convex.
3. Tile bed (T1): one convex clay cell per field cell, between the board top and 4 mm under the tile underside.
   Fascia (kayaoi) square to the rafters along the whole curved eave, in every LOD.
4. Silhouette LODs (T7b): Res 2 = far-material field on a 1-ken x 5-band grid plus every outline piece (ridge stack,
   onigawara, eave strip, kayaoi, hafu, koba); Res 3 = 2-ken x 3-band field + the same outline pieces as blocks.
5. Budget: the curved hongawara roof of a 3 x 3-bay (5.46 x 5.46 m core) hall with 2-ken eaves targets ≤ 6,000 faces at
   Res 1, so the hall plus kumimono plus walls stays in the large-building budget (12,000 / 4,600 / 1,600).
6. Plan flare of the eave (corners projecting further in plan) is NOT modelled: the elevation sweep alone gives the
   read, and the plan stays the kit's convex slope polygons.
7. Missing materials (stand-ins until S-agent makes them): `roof_hiwada` (cypress bark; stand-in roof_kureita),
   `roof_copper` (green patina copper sheet; stand-in roof_kureita), a thicker `roof_kokera_thick` edge texture is not
   needed (roof_kokera on the koba). The generator switches to the real key as soon as it exists in the library.
