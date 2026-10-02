# FX6 notes: fixes from Stephen's 3c-1 walk + the small-gate family (agent FX6, 2026-10-02)

Written BEFORE modelling (research first). Sources read this run (generic searches, no personal data in any request):
- **[KB-kido]** kotobank "木戸 (kido)": a simple wooden gate; single or double hinged leaves; board fences with a gate; the
  wicket (kuguri-do); roofless garden and yard gates; the ward kido ~2 ken wide, shut 10 pm to 6 am.
- **[KB-kabuki]** kotobank "冠木門 (kabuki-mon)": two posts with a cross beam (kabuki) on top; first recorded 1474;
  "originally the gate of lower-class houses", also the outer gate of daimyo; later restricted by rank (the exact Edo
  rules are not in the source: **GK**: in the Edo period a gate at all was a mark of rank; commoners other than
  village headmen and privileged townsmen were normally not allowed a kabuki-mon on the street).
- **[NAJGA]** North American Japanese Garden Association, "Japanese Gardens: Boundaries and Gates" and "The Tea Garden":
  the **shiorido**: a simple roofless hinged gate of split-bamboo strips woven into a diamond lattice on a frame of thin
  round bamboo, tied with black twine, hung in a break in a hedge or bamboo fence; a tea-garden form from the Rikyu
  era (late 16th c.).
- Earlier project research (K3_NOTES §1-2: R_RURAL §8 post gate / kabuki-mon / wicket; D3_NOTES compounds; W3B / W3C1
  yards).

## 1. Era test (1730)
| Gate | 1730? | Why |
|---|---|---|
| Single-leaf board gate (katabiraki ita-kido) | IN | [KB-kido]: the commonest wooden gate of yards, gardens and row-house lots |
| Two-leaf board gate without a kabuki beam (ryobiraki ita-kido) | IN | [KB-kido] (double leaves); the ward kido is the large case (W2C built it) |
| Shiorido (bamboo lattice garden gate) | IN | [NAJGA] tea-garden form from the late 16th c., "long used throughout Japan" |
| Plain opening between two posts (no leaf) | IN | trivially (a gap in a fence held by two posts: the lane entrance of a row yard) |
| kabuki-mon / roofed kabuki-mon / mune-mon / nagaya-mon | IN (kept) | K3 / D3; status gates |

## 2. Recorded choices (sizes; game rules PLAYBOOK D1 >= 1.00 m clear, D2 >= 2.00 m head, if there is a head)
All new gates sit in a **1-ken gap** of the run (or 1.5 ken for the two-leaf cart gate), posts on the half-ken grid
nodes, leaves swing into the compound (-z) with the gates.py hinge convention, one door each (DoorsTwinN), the leaves
lifted over FX5's sill pad (`leaf_y0`), the fence modules either side end `post` at the gate's own post width
(`_wall_path` now passes the gate's `post_w`, so a fence body stops exactly at the post face: `_abut` / jointcheck).

| Kind (`kind=` in a compound gate) | Form | Sizes (chosen) | Leaf |
|---|---|---|---|
| `kido_kata` single-leaf board gate | two square posts 0.15 standing to 2.15, a cap board (kasagi) 0.05 on their tops with slanted ends; inside the gap a latch post (0.12) 1.20 m from the hinge post; between the latch post and the far post a fixed board panel (sode-ita) of the fence's own boards | posts 2.15 (fence 1.80 + 0.35), head = cap underside 2.15 -> 2.05 clear over the sill | one battened board leaf 1.18 wide, 1.86 high (top ~2.0, about the fence top), hinged on the left post, clear >= 1.00 |
| `kido_ryo` two-leaf board gate | two square posts 0.18 to 2.35, a cap beam (kasagi) 0.12 deep on the post tops projecting 0.22 with cut ends; NO kabuki beam, no head tie | span 1 ken (clear ~1.6) or 1.5 ken for carts / horses (clear ~2.5) | gates.gate_leaves '_board' 1.90 high |
| `shiorido` bamboo lattice gate | two round posts (r 0.06) to 1.35 (fence 1.05 + 0.30); latch post 1.24 m from the hinge post, the fence's own bamboo grid between the latch post and the far post | no head (D2 open sky) | one leaf 1.12 x 1.20: a frame of round bamboo (r 0.02) with split-bamboo strips in a diamond lattice, rope ties; see-through (Geometry blocks, no View) |
| `opening` posts only | two posts (round r 0.06 to 1.35 for bamboo fences, square 0.15 to 2.10 for board fences), nothing between | 1 ken (clear 1.70) | none (no door) |

## 3. The gate-picker rule (`dwelling.pick_gate`; a compound gate entry may name its kind = explicit override)
Inputs: the fence the gate sits in (kind + height), the compound's **status** (`high` = samurai / official / honjin /
temple; `mid` = headman, rich merchant, ordinary townsman; `work` = a trade yard) and the gate's **role** (`front`, `back`,
`lane`) and **carts** (carts / horses / casks pass).

| Fence (height) | high, front | high, back | mid (any role) | work, carts | work, on foot | lane (shared row entrance) |
|---|---|---|---|---|---|---|
| dobei / tsuiji (2.1-2.3, plastered / earth) | kabuki_roofed 1.5 ken (or munemon / a nagaya-mon object) | kabuki 1 ken | kabuki 1 ken | kido_ryo 1.5 ken | kido_kata | kido_kata |
| itabei board fence (1.80) | kabuki 1.5 ken | kido_kata (kido_ryo 1 ken if carts) | kido_kata (kido_ryo 1 ken if carts) | kido_ryo 1.5 ken | kido_kata | kido_kata |
| ikegaki tall hedge (~1.8) | kabuki 1.5 ken | kido_kata | kido_kata | kido_ryo 1.5 ken | kido_kata | kido_kata |
| light fences: yotsume / kenninji / shiba / takeho / low hedge (<= 1.5) | shiorido | shiorido | shiorido | opening 1.5 ken | shiorido | opening |

Gatehouses (nagaya-mon) stay separate objects in the gap of the line (samurai M, Kanto headman).

## 4. Re-assignment of every existing compound gate (by the rule)
| Compound (wave) | Fence | Status / role | Before | After |
|---|---|---|---|---|
| samurai_m (3a) back gate | itabei kuro | high, back | kabuki 1 ken | kido_kata |
| samurai_m front | - | - | nagaya-mon object | nagaya-mon (kept) |
| headman_east (3a) back gate | ikegaki tall | mid, back | kabuki 1 ken | kido_kata |
| headman_east front | - | - | nagaya-mon object | nagaya-mon (kept) |
| honjin (3a) front | dobei | high, front | kabuki_roofed 1.5 ken | kabuki_roofed 1.5 ken (kept) |
| honjin (3a) back | itabei | high, back, carts (an inn's deliveries) | kabuki 1 ken | kido_ryo 1 ken |
| merchant (3a) garden gate | itabei | mid, back | kabuki 1 ken | kido_kata |
| kumi row (3a) | yotsume | lane | kabuki 1 ken | opening |
| doshin (3a) | itabei | high, front | kabuki 1.5 ken | kabuki 1.5 ken (kept: the doshin's kabuki-mon) |
| stableyard (3b) | itabei | work, carts | kabuki 1.5 ken | kido_ryo 1.5 ken |
| timberyard (3b) | itabei | work, carts | kabuki 1.5 ken | kido_ryo 1.5 ken |
| foundryyard (3b) | itabei | work, carts | kabuki 1.5 ken | kido_ryo 1.5 ken |
| brewery (3c-1) | itabei kuro | work, carts (casks) | kabuki 1.5 ken | kido_ryo 1.5 ken |
| dyersyard (3c-1) | itabei | work, on foot | kabuki 1.5 ken | kido_kata |
| paperyard (3c-1) | yotsume | work, on foot | kabuki 1.5 ken | shiorido |

Spans change, so the gate's offsets on the grid are kept where the post A node stays (the gap moves its B post);
every change keeps the gap on the half-ken grid.

## 5. The other fixes (root causes found before changing anything)
- **Cloth in the dyer's yard:** `jp_f_monohoshi_torn` laid each fallen length as a flat strip on the yard plane plus a
  1 m piece rotated -55 deg off its end: a stiff cloth ramp standing in the air, ending 0.8 m up, touching nothing; on
  the island's slope the flat strip also floats at one end. Also every hung length on the frames (both variants) hung
  BESIDE the drying bar (a flat sheet each side, its top at the bar's centre, 0.3-4.5 cm off the bar's surface) with
  nothing over the bar. And the dye rack's wringing bar (with its cloth) stood 14 cm in front of the rack posts on
  nothing.
- **Kura doors:** every kura doorway (`openings.part_kura_door '_open'`, all kura shells) built the plastered outer
  leaves "static open ~90 deg", standing straight out from the wall like open doors beside the working sliding door:
  they look like doors that should work. Period practice: the heavy kannon leaves stood open by day, folded back
  against the wall; the wooden inner door was the one used. Fix: fold them flat back (180 deg) against the surround and
  wall, so only the working door is in the opening.
- **The koji room (muro) table:** the koji bed (1.80 x 1.20) was placed 0.35 m inside the muro's only door (the
  placer put it "towards the door"); the furnish check D4 (1.00 m band from the doors) skipped the room because
  `sparse()` rooms with no free cell next to a door were passed as "no door reaches into this sparse space".
- **The washbasin:** `jp_f_hangiri_scattered` (the shallow starter / washing tubs, knocked about; mae-gura kamaba and
  o-kura loft): its third tub stands on edge at 70 deg on one rim point, leaning on nothing.
