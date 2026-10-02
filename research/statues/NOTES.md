# FX2 statue notes: proportions, iconometry and the modelling choices (2026-10-01)

References: `REFS.md` (32 CC0 / public-domain photos, Met + Cleveland open access; images in `data/refs/fx2/`).
Code: `spikes/FX2/figures.py` (the shapes), `statuekit.py` (mesher), `statues.py` (catalogue + face targets),
`fx2props.py` (meshes as kit solids + halos / lotus / pedestal tiers).

## How the statues are made
- Each figure is a signed-distance model (numpy) built from the reference photos: primitives (ellipsoids, round
  cones, tori, many-sphere curls) smooth-unioned, carved with smooth subtractions (eye lids, mouth line, ear hollows),
  robe folds as displacement ridges. Parts (head, body, hands, staff head) each get their own voxel size: the face
  ~2 mm at statue size, the robe ~5 mm.
- Meshed by surface nets, every vertex projected onto the true surface, voxel-remeshed (manifold) and reduced by
  Blender's quadric decimation (headless) to the face target per LOD. Smooth vertex normals (crease 80 deg).
- Cached in `spikes/FX2/meshes/<name>.json` (keyed by the modelling source), so prop builds need no Blender when
  nothing changed.
- **Handedness:** DayZ model space is left-handed. The kit's +x is the FIGURE'S RIGHT (the viewer's left in game).
  The Workbench peeks (`peek.py`) are flipped to match; `render_fx2.py` uses render_parts' mirrored axis map and
  needs no flip. Jizo's staff is in his right hand (+x), the jewel in his left (-x), as Met 53175 / 76084.

## Proportions (head unit hu = chin to crown, without the ushnisha)
| Figure | Height 1.0 = | hu | Notes / source |
|---|---|---|---|
| Seated nyorai (Amida, Shaka) | lap base to ushnisha top | 0.30 | knee span ~0.94 (Met 44890: knee span ~ seated height); shoulder span ~0.44 (about half the knees); chin at 0.63; head bowed 6 deg |
| Standing Jizo (altar) | soles to crown | 0.15 | ~6.7 heads (Met 53175: ~7 incl. the lotus); staff 1.06 + head 0.105 (taller than the figure, as both Jizo refs) |
| Stone roadside Jizo | soles to crown | 0.20 | stockier (body x 1.38), ~5 heads: the roadside form (general knowledge; stone carving keeps a big head) |
| Standing Kannon | soles to topknot | 0.128 | ~7.8 heads to the top of the topknot (CMA 152018 / Met 49257: slender, tall chignon + crown) |
| Child Jizo | base to crown | 0.27 | ~3.7 heads, round head, hands in gassho (general knowledge; no child-Jizo photo in either collection) |
| Komainu | base to top of head | (head 0.33) | seated on the haunches, front legs straight, head ~1/3 of the height (CMA 106262/3, Met 53190) |
| Kitsune | base to ear tips | (head 0.20) | slim, long neck, ears ~0.13, snout ~0.14 (Met 60375 netsuke + general knowledge) |

## Iconography choices
- **Nyorai head:** snail-shell curls (rahotsu) in staggered rows on a cap above a straight forehead hairline and on the
  ushnisha (nikkei), the nikkeishu jewel at the front of the ushnisha, the urna (byakugo) between the brows, the
  willow-leaf brows, half-closed downcast eyes, long pierced earlobes, three neck folds (sando). Curls: ~110 at
  r = 0.055 hu (the references have ~250 smaller curls: fewer, larger ones survive the face budget and still read).
- **Amida** (Jodo village temple): seated in kekka-fuza, **jobon-josho-in** (hands in the lap, palms up, thumbs and
  index fingers in two rings), robe over both shoulders with the chest open in a V and the under-robe band (Met
  44890). Halo: the wheel (rinko) with eight spokes and a knobbed rim, a head halo with a lotus centre (Met 44890).
- **Shaka** (Zen town temple): seated, right hand raised palm out (**semui-in**), left hand on the knee palm up
  (**yogan-in**) (CMA 153384). Halo: boat-shaped with a flame edge and a head ring (CMA 147590 frame).
- **Kannon** (Sho Kannon): crown band with the small seated Amida (kebutsu) on the front plaque, tall topknot, hair
  in strands, bare chest with a necklace, skirt (mo) with a turned band and vertical folds, scarf (tenne) down both
  sides and looped across the knees, left hand at the chest holding a lotus bud, right hand lowered palm out
  (yogan-in) (CMA 152018, Met 49257). Boat halo.
- **Jizo:** shaven head, monk's robe with the kesa band from the left shoulder to the right hip and its ring at the
  chest, the wish-granting jewel (hoju) in the left hand, the **shakujo** in the right: a CLOSED pointed loop (two
  arcs meeting at a stupa finial), a central spindle, three rings per side, a collar at the pole (Met 53175 shows
  the loop + rings; this fixes the old see-through top). Altar Jizo: black-brown lacquered wood, bronze staff, no
  halo (as both references). Stone Jizo: the staff head carved solid (a thin web in the loop, rings as beads: a
  pierced stone loop would not survive), the cuts softer.
- **Lotus seat:** three staggered petal tiers (12/14/16 petals, pointed tips) on a waisted drum, octagonal tiers below
  (CMA 147591, Met 44890 / 76084).
- **Gilt:** new material `jp_m_gilt_worn` (gold leaf over black lacquer, rubbed through; palette `gilt_worn` sampled
  from Met 44890 / CMA 147588), used on Amida, Shaka, Kannon, their lotus seats and halos.

## Komainu and kitsune
- **Era:** stone komainu at shrine approaches spread in the Edo period (the oldest stone pairs are 17th c.); the
  earlier guardians were wooden pairs inside the halls (the references are 13th-14th c. wood). Both forms existed by
  1730. Ball-under-paw / cub variants and the crouching 'ready to pounce' Osaka form are later: NOT built.
- **Pair rule:** 'a' (open mouth) and 'un' (closed). Facing the shrine, the 'a' stands on the right, the 'un' on the
  left (general knowledge; common, not universal). Style a (the references' upright form): heavy curled mane, the
  un with a short horn (the komainu proper, the a being the karashishi). Style b (compact Edo stone): lower head,
  rounder chest, tight curl rows, no horn, flame tail. Mossy variant: style a, aged stone _w2 + moss on the pedestal.
- **Kitsune:** Inari's messengers in pairs, one with the rice-store **key** in its mouth, one with the **jewel**
  (general knowledge: the other common items, a scroll or a rice sheaf, not built). Seated, tail raised to a jewel-
  shaped point. NO stone Inari fox in either open-access collection: **references missing** (see the FX2 report):
  Stephen may want to save 2-3 photos of Edo-period stone Inari foxes (e.g. Fushimi Inari, Toyokawa Inari) for a check.

## Face counts (Res 1 / 2 / 3)
Figures (`python spikes/FX2/statues.py`): seated nyorai 2,800 / 998 / 338; Kannon 2,598 / 948 / 318; altar Jizo
2,598 / 948 / 380; stone Jizo 2,398 / 858 / 290; child Jizo 1,100 / 420 / 148; komainu a 2,800 / 1,000 / 340, b 2,600 /
950 / 320; kitsune 2,000 / 750 / 250; lotus seat 700 / 260 / 176; masks 400 / 150 / 50 each.
Props: altar daises 3,490-4,622 (Amida the most: the wheel halo); stone Jizo 1,813-1,930; Jizo huts 1,877-2,029;
komainu 2,638-2,847; kitsune 2,036; kagura mask wall 2,128; bonsho 1,946; waniguchi 1,249; suzu 828; ema rail 830;
offering box 496. Altar daises (image + lotus + halo + cabinet + altar pieces) are budget class
`altar` (5,500 = statue 4,500 + furniture 1,000); stone Jizo / komainu / kitsune props class `statue` (4,500 / 1,700 /
700: 3,000 + 50 %, PLAYBOOK §12).
