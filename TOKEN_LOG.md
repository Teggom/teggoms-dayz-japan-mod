# Token log: what each agent cost (Stephen's Pro plan)

"Tokens" is the agent's own subagent_tokens from its completion notice. "Weekly %" is the account's
"Weekly · all models" figure read with get_usage at that moment, so it also includes the lead session and anything else
running. All agents are Opus 5.5 at effort high (`opus-high`) unless noted.

| When | Agent | Job | Tokens | Time | Weekly % after |
|---|---|---|---|---|---|
| 2026-09-29 | effort test x4 | one tansu, intact + ransacked | medium 164k, high 252k, xhigh 438k, max 450k | - | - |
| 2026-09-29 | B0 | kit cleanup + pipeline + townhouse template + C19 fix | 409k | 50 min | - |
| 2026-09-29 | B1 | 34 materials x 3 wears + 2 text atlases | 453k | 39 min | - |
| 2026-09-30 ~04:08 UTC | (baseline) | B2 running, part 1 of 7 done | - | - | **18%** (5-hour window 1%) |
| 2026-09-30 ~04:48 UTC | B2 | wave-1 parts: koyagumi, party wall/roof end/corner/seam cap, stall, stair, half-door, floor pit + sunoko (10 parts) | **715k** (176 tool calls) | 72 min | **19%** (5-hour 9%). Only parts 2-8 ran after the 18% baseline |
| 2026-09-30 09:10 (local, -04:00) | B3a (baseline) | launched: 24 interior props, one agent, per-model time log in TIMELOG_B3a.md | - | - | before: **19%** (5-hour 1%) |
| 2026-09-30 09:52 (local) | B3a | 24 interior props = 110 models (24 new, 36 variants, 50 abandoned), jp_furniture.pbo | **498k** (160 tool calls) | 42 min | **21%** (5-hour 10%): B3a alone = ~2% weekly, ~9% of a 5-hour window |
| 2026-09-30 10:08 (local) | B3b (baseline) | launched: all 20 W1 outdoor items (122 models), one agent, time log in TIMELOG_B3b.md | - | - | before: **21%** (5-hour 10%) |
| 2026-09-30 10:48 (local) | B3b | 20 outdoor items = 129 models (20 new, 80 variants, 29 abandoned), jp_site.pbo + well script, 1 material | **519k** (147 tool calls) | 40 min | **22%** (5-hour 19%): B3b alone = ~1% weekly, ~9% of a 5-hour window |
| 2026-09-30 11:33 (local) | B4 (baseline) | launched: furnish + dress the machiya pilot, G4 checklist, time log in TIMELOG_B4.md | - | - | before: **22%** (5-hour 19%) |
| 2026-09-30 12:43 (local) | B4 | furnished machiya pilot: 32 room props + 5 shop-front proxies, 43 loot pts, 17 yard/street objects, toilet, decorator kit, G4 checklist | **576k** (225 tool calls) | 69 min | **24%** (5-hour 33%): B4 alone = ~2% weekly, ~14% of a 5-hour window |
| 2026-09-30 12:44 (local) | L1 (baseline) | launched: life layer interior, 50 items, one agent, time log TIMELOG_L1.md | - | - | before: **24%** (5-hour 33%, resets ~13:40) |
| 2026-09-30 13:38 (local) | L1 | life layer interior: 50 items = 185 models (50 new, 65 variants, 70 abandoned), decorator wall/beam mounting, 4 materials | **654k** (195 tool calls) | 55 min | **25%** (5-hour 46% just before the 13:40 reset): L1 alone = ~1% weekly, ~13% of a 5-hour window |
| 2026-09-30 13:45 (local) | L2 (baseline) | launched: life layer outdoor, 24 items (+ check B3b text mirroring), time log TIMELOG_L2.md | - | - | before: **25%** (5-hour 0%, fresh window) |
| 2026-09-30 14:41 (local) | L2 | life layer outdoor: 24 items = 81 models (22 new, 20 variants, 39 abandoned) + the text fix (B3b + L1 text was back-facing = invisible) | **581k** (213 tool calls) | 57 min | **27%** (5-hour 11%): L2 alone = ~2% weekly, ~11% of a 5-hour window |
| 2026-09-30 15:01 (local) | F1 (baseline) | launched: the 8 G4 walk fixes + a well diagnostic, time log TIMELOG_F1.md | - | - | before: **27%** (5-hour 13%) |
| 2026-09-30 15:44 (local) | F1 | the 8 G4 fixes + the well's real cause (class=house) + Roadway on sturdy furniture; everything rebuilt, all checks | **573k** (256 tool calls) | 43 min | **29%** (5-hour 25%): F1 alone = ~2% weekly |
| 2026-09-30 16:11 (local) | C1 (baseline) | launched: Phase C wave 1 town shells (60 townhouse units + post-town house + inn, test rows on the island, well diag removal), time log TIMELOG_C1.md | - | - | before: **29%** (5-hour 26%) |
| 2026-09-30 17:25 (local) | C1 | town shells: 69 townhouse units + 8 post-town houses + 4 inns = 81 shells, 4,717 checks, test street on the island | **532k** (194 tool calls) | 74 min | **31%** (5-hour 40%): C1 alone = ~2% weekly, ~14% of a 5-hour window |
| 2026-09-30 17:28 (local) | C2 (baseline) | launched: rural template + ~18-25 rural shells + the grand-inn storey source check + a hamlet on the island, time log TIMELOG_C2.md | - | - | before: **31%** (5-hour 42%, resets ~18:40) |
| 2026-09-30 18:31 (local) | C2 | rural template + 21 rural shells (1,050 checks), grand-inn source check, hamlet on the island | **658k** (257 tool calls) | 63 min | **33%** (5-hour 56%): C2 alone = ~2% weekly, ~14% of a 5-hour window |
| 2026-09-30 18:41 (local) | C3 (baseline) | launched: kura + furnished variants of every wave-1 type + street/hamlet dressing + the bundled walk, time log TIMELOG_C3.md | - | - | before: **33%** (5-hour 0%, fresh window) |
| 2026-09-30 19:53 (local) | C3 | 3 kura shells + 14 furnished variants (every wave-1 type) + street/hamlet dressing (101 objects) + the ~28 min walk | **793k** (295 tool calls) | 71 min | **36%** (5-hour 20%): C3 alone = ~3% weekly, ~20% of a 5-hour window |
| 2026-09-30 20:26 (local) | W2 + S1 (baseline, CONCURRENT) | W2: torii/lanterns/steps/basins/graves (+ Stephen's rope, moss and 2-3x grave variety); S1: the 22 shop dressing sets (spec + build + demo shops). Time logs TIMELOG_W2.md / TIMELOG_S1.md; their usage % readings include both agents | - | - | before: **36%** (5-hour 22%) |
| 2026-09-30 ~21:00 (local) | A4 (opus-medium, research only) | the lightweight 'what are we missing' audit: research/AUDIT_MISSING.md (17 + 8 system gaps, 9 + 1 Japanese details) | **138k** (33 tool calls) | 9 min | ran alongside W2 + S1 |
| 2026-09-30 ~21:01 (local) | W2 | 7 wave-2 outdoor items = 91 models (torii 30 with rope / shide / moss, lanterns 13, steps 13, basin 4, gravestones 24, grave wood 7), jp_site.pbo 301 classes | **529k** (176 tool calls) | 35 min | ran alongside S1 + A4 |
| 2026-09-30 ~21:12 (local) | W3 (baseline) | launched: 4-6 more wooden grave posts (bohyo), small job, alongside S1 | - | - | before: **39%** (5-hour 42%) |
| 2026-09-30 ~21:19 (local) | W3 | 6 wooden grave post (bohyo) variants, jp_site.pbo 307 classes | **163k** (65 tool calls) | 7 min | ran alongside S1 |
| 2026-09-30 ~21:27 (local) | M1 (baseline) | launched: the missing materials, accuracy first (bare earth, new + silver-grey wood, brown heri, kaimyo + bonji + bohyo ink text, wicker + firewood tweaks), waits for S1 before touching the pipeline | - | - | before: **39%** (5-hour 46%) |
| 2026-09-30 21:52 (local) | S1 | 28 shop sets (KEEP said 22, listed 28): spec SHOP_SETS.md, 84 new props / 175 models, 5 materials, set API (168 sets pass), 6 demo shops; jp_furniture.pbo 473 classes | **759k** (251 tool calls) | 86 min | ran alongside W2, A4, W3, M1 |
| 2026-09-30 ~22:10 (local) | M1 | missing materials, accuracy first: bare earth, new + silver-grey wood, brown heri, 14 kaimyo + 6 grave-post ink cells, wicker + firewood; props rebuilt, 4 PBOs (bonji blocked: no Siddham font) | **501k** (245 tool calls) | 44 min | **41%** (5-hour 62%) after W2 + S1 + A4 + W3 + M1 |
| 2026-09-30 ~23:16 (local) | M2 | Siddham bonji on the gorinto (KHA HA RA VA A) and hokyointo (HUM TRAH HRIH AH): 9 atlas cells, 6 models | **239k** (131 tool calls) | 14 min | ran alongside the Pompompurin agent |
| 2026-09-30 ~23:40 (local) | G1 | gorinto seating fix (truncated sphere, flat seats, stack seated) | **157k** (60 tool calls) | 8 min | |
| 2026-09-30 23:46 (local) | P1 (Pompompurin, fun) | STOPPED by Stephen (didn't like the renders); not in game | n/a (killed) | ~40 min | |
| 2026-09-30 23:46 (local) | SH1 (baseline) | launched: test-island showcase (shrine, graveyard, demo shops, life-layer gallery) + the 10-stop walk, time log TIMELOG_SH1.md | - | - | before: **43%** (5-hour 0%, fresh window) |
| 2026-10-01 ~00:28 (local) | SH1 | test-island showcase: shrine 149 objects, graveyard 148, 6 demo shops on the street, life-layer gallery (74), labelled maps, 44-min walk | **575k** (191 tool calls) | 42 min | |
| 2026-10-01 09:46 (local) | FP1 + FB1 (baseline, CONCURRENT) | Stephen's showcase walk: FP1 = 15 prop fixes/remakes + collapsed torii + aged plaster; FB1 = doors (only 31 of 128 classes matched their p3d name), building fixes, placements, world rebuild, re-check list | - | - | before: **44%** (5-hour 5%) |
| 2026-10-01 ~10:56 (local) | FP1 | 15 prop findings (broom, sheaves, bonsai/pots, sword rack, ropes, charcoal-bale ends, lantern, loom, leaf shapes, stone texture, straw stack, lever well, notice board, climbable fire-watch ladder) + 5 collapsed torii + 4 materials | **764k** (347 tool calls) | 69 min | ran alongside FB1 |
| 2026-10-01 ~11:00 (local) | FB1 | doors: 97 of 128 building files renamed to match their classes + bindcheck.py; Kinai gable, kura doors/shutters + aged plaster, tools re-seated, hill torii raised, collapsed torii placed, world rebuilt, 15-min re-check | **532k** (282 tool calls) | 74 min | ran alongside FP1 |
| 2026-10-01 11:14 (local) | FP2 + FB2 (baseline, CONCURRENT) | re-check fixes: FP2 = firewood piles, mochi mortar, rope 2.5x segments; FB2 = z-fighting check + fixes, Kinai gable, partition head beams, two-storey divider/gaps, world rebuild | - | - | before: **49%** (5-hour 39%) |
| 2026-10-01 ~11:55 (local) | FP2 | firewood piles remade (woodpile.py + redrawn end grain), usu/kine seated, rope 2.5x (ropekit.py) | **466k** (201 tool calls) | 41 min | ran alongside FB2 |
| 2026-10-01 ~12:18 (local) | FB2 | z-fighting 102,726 pairs -> 0 (check C20 + resolve), Kinai gable to real form, partition head beams (C21), grand inn divider + gaps (C22), world rebuilt | **475k** (206 tool calls) | 64 min | ran alongside FP2 |
| 2026-10-01 12:35 (local) | W2P1 + W2P2 + W2C (baseline, CONCURRENT) | Phase C wave 2 start: village shrine/temple parts; curved sori roof + kumimono; civic shells (tea house, smithy, guard hut, ward gate) | - | - | before: **52%** (5-hour 60%, resets 12:50) |
| 2026-10-01 ~13:19 (local) | W2P1 | village shrine/temple parts: 48 variants / 10 parts (koran, tobira, nagare, kohai, hogyo, ornaments, stilts, kidan, shitomi, 8 micro-shrines) + 3 offline halls | **579k** (143 tool calls) | 44 min | concurrent with W2P2 + W2C |
| 2026-10-01 ~13:19 (local) | W2C | civic shells: 7 tea houses, 3 smithies, 3 guard huts, 3 ward gates (16), gates.py, templates/civic.py | **476k** (153 tool calls) | 44 min | concurrent |
| 2026-10-01 ~13:30 (local) | W2P2 | curved sori roof (4 forms, 4 coverings) + kumimono (5 forms) + frame_storey_hakama; 18 manifest variants; 4 offline assemblies 23/23 | **559k** (152 tool calls) | 54 min | concurrent with W2P1 + W2C |
| 2026-10-01 ~13:31 (local) | W2S (baseline) | launched: shrine + temple shells, village + town grades, 3 materials | - | - | before: **56%** (5-hour 19%) |
| 2026-10-01 ~14:45 (local) | W2S | 25 shrine + temple shells (village + town grades), 3 materials (hiwada, copper, bronze), shellcheck head-room by rays; jp_buildings 169 classes | **639k** (235 tool calls) | 77 min | |
| 2026-10-01 ~16:25 (local) | V1 | faster checks: ray acceleration (C11/C15/C17), C20 candidate lists, no double model build, checkcache.py; full 169: 935 s -> 193 s, unchanged 3 s, one module changed 29 s; byte-identical results | **394k** (154 tool calls) | 98 min | |
| 2026-10-01 ~16:26 (local) | W2F (baseline) | launched: wave-2 specialty props, furnished variants, shrine precinct / temple / civic placement, ~30-35 min walk | - | - | |
| 2026-10-01 ~17:20 (local) | W2F | 49 specialty props, 24 furnished wave-2 variants, shrine precinct / village shrine / 2 temples / civic placed, ~32 min walk | **675k** (215 tool calls) | 53 min | weekly **61%** after |
| 2026-10-01 ~18:30 (local) | FX1 | wave-2 walk fixes 1-6 (door pulls, offering box, hung props, veranda returns, torii clearance, woodpile stakes) + handlecheck / hangcheck | **598k** (268 tool calls) | 55 min | |
| 2026-10-01 ~18:45 (local) | FX2 (baseline) | launched: statues from CC0 museum refs, komainu + kitsune pairs, lantern pairs, detail props, torii rope sag, U1 wrap veranda | - | - | before: **~63%** |
| 2026-10-01 ~19:20 (local) | FX3 phase 1 | inventory (11 UV helpers / 8 pipelines -> one hook), uvwood.py design, 11 wood atlases, macro weathering stage, irregular moss, ONE sample sheet | **298k** (102 tool calls) | 26 min | concurrent with FX2 |
| 2026-10-01 ~20:05 (local) | FX2 | 32 CC0 museum refs (Met 7, Cleveland 13 objects), 4 altar images + Jizo family remade from photos, komainu x3 + kitsune pairs placed, detail props, torii rope 3/4 sag (lowest tip 2.31 m), U1 wrap veranda | **685k** (297 tool calls) | 81 min | |
| 2026-10-01 ~20:06 (local) | FX3 phase 2 (resumed) | integrate uvwood + atlases + macro layer + moss into every pipeline, rebuild all | - | - | |
| 2026-10-01 ~21:35 (local) | FX3 phase 2 | wood atlases (11 x 3) + uvwood.py in Part.lods() + Stage3 macro weathering in every wood/thatch rvmat + moss; rebuilt parts 234 / buildings 193 / all props, 5 PBOs | **410k** (86 tool calls) | 26 min | FX3 total 708k |
| 2026-10-01 ~21:40 (local) | CA1 (baseline) | launched: one config assembler per PBO (builder fragments merged), budget-class tidy-up | - | - | before: **67%** |
| 2026-10-01 ~22:05 (local) | CA1 | config assembler: per-builder fragments + tools/assemble_config.py for jp_furniture (522) + jp_site (320), 0 class diffs over 13 PBOs, single-builder rebuild proof, budget classes folded back (9 deliberate overages reported) | **334k** (196 tool calls) | 28 min | |
| 2026-10-01 ~22:06 (local) | FX4 (baseline) | launched: bell interior, fire-tower head room, stone atlas + per-piece mapping | - | - | before: **68%** |
| 2026-10-01 ~22:45 (local) | FX4 | bonsho + hansho made hollow (lathe profile direction; lathecheck.py: 6 inside-out shapes -> 0), fire-watch roof 1.10 -> 2.20 m above the deck, stone atlases (make_stone_atlas.py) + per-face turn/offset/mirror | **341k** (175 tool calls) | 38 min | |
| 2026-10-01 ~22:47 (local) | K3 + D3 (baseline, CONCURRENT) | wave 3a: K3 = wall kit + watari-roka / kairo corridor kit; D3 = 14 dwelling types + honjin / waki-honjin, furnished, compounds + corridors + placement, walk | - | - | before: **69%** |
| 2026-10-01 ~23:45 (local) | K3 | wall kit (65 variants) + watari-roka / kairo corridor kit (32) + striproof.py, 4 offline proofs 89/89 | **642k** (168 tool calls) | 57 min | concurrent with D3 |
| 2026-10-02 ~00:28 (local) | D3 | 28 dwelling shells + honjin / waki-honjin, 16 furnished, 8 compounds / corridors (incl. temple U hondo<->kuri roka), 29 placed, 28-min walk | **161k reported** (319 tool calls; the count looks low for the run) | 106 min | weekly **74%** after 3a |
| 2026-10-02 00:31 (local) | W3B (baseline) | launched: wave 3b workshops + services (approved by Stephen before bed, usage-checked) | - | - | before: **74%** (projected ~78-80%) |
| 2026-10-02 ~01:30 (local) | W3B | wave 3b: 18 shells (sento x2, stable row x2, barber + misemono booths, doma + bench workshops x2 each, timber sheds x3, foundry x2, 3 yard compounds), 34 props / 63 models, 14 furnished, 38 placements | **644k** (182 tool calls) | 55 min | weekly **76%** after |
| 2026-10-02 ~11:35 (local) | FX5 | fixes from the 3a / 3b walk: gate sill pads (9 compounds), honjin wall / fence joints + hedge slits, continuous hedge + 2 new materials, U9 deferred, 5-min re-check | (see completion notice) | 45 min | weekly **77%** after (76% at start) |

## B3b time log, summarised (TIMELOG_B3b.md, with GROUP START lines)

| Stretch | What | Models | Minutes | 5-hour % |
|---|---|---|---|---|
| 10:09-10:17 | setup: reading + building the site pipeline on B3a's kit | - | 8.5 | 10 -> 13 |
| 10:17-10:28 | round wood: tubs, fire tub, firewood, bench, laundry pole, tenbin, handcart (7 items) | 42 | 11 | 13 -> 15 |
| 10:28-10:31 | wells: pulley (+ roofed), lever (2 items) | 9 | 3 | 15 |
| 10:31-10:36 | stone: jizo (+ bib material), stele family, jizo hut (3 items) | 19 | 5 | 15 -> 16 |
| 10:36-10:43 | street: gutter, shop front, lanterns/signs, nobori, stall, notice board (6 items) | 47 | 7 | 16 -> 18 |
| 10:43-10:45 | straw: stacks, shimenawa (2 items) | 12 | 2.5 | 18 |
| 10:45-10:48 | PBO pack + contact sheets | - | 2.5 | 18 -> 19 |

Compared with B3a: about the same tokens (519k vs 498k) and time (40 vs 42 min) for a few more models; setup took
longer (8.5 vs 3 min) because it read both build lists and B3a's pipeline, but the first group was no slower.
Once the pipeline exists, a group of 2-7 items takes 2-11 minutes, roughly 1% of a 5-hour window per few items.

## B3a time log, summarised (TIMELOG_B3a.md)

The agent didn't build one model at a time: it wrote the code for a GROUP of props, then one script run produced
the whole group at once. So the real unit of time is the group, not the model:

| Stretch | What | Models | Minutes | 5-hour % |
|---|---|---|---|---|
| 09:11-09:14 | setup (reading) | - | 3 | 1 -> 3 |
| 09:14-09:24 | the furniture pipeline + the tansu (reused from the effort test) | 4 | 10 | 3 |
| 09:24-09:36 | kitchen: kama, jizai-kagi, mizugame, oke, tana, firewood, jars | 42 | 12 | 3 -> 7 |
| 09:36-09:40 | storage: nagamochi, kori, boxes, tawara, rack | 24 | 4 | 7 |
| 09:40-09:47 | heat, light, bedding: andon, hibachi, tabakobon, futon x2, mushiro | 20 | 7 | 7 -> 9 |
| 09:47-09:50 | shop + debris: desk, lattice, stand, goods, debris | 20 | 3 | 9 -> 10 |
| 09:50-09:52 | PBO pack + contact sheets | - | 2 | 10 |

Lesson: after the first group (pipeline + learning), each later group of ~5 props took 3-12 minutes. Variants and
abandoned states cost almost nothing on top: they come out of the same script run as their prop.
The agent notes the usage tool sometimes returned a stale reading, so the % steps are approximate.

## B4 time log, summarised (TIMELOG_B4.md)

| Stretch | What | Minutes | 5-hour % |
|---|---|---|---|
| 11:34-11:44 | setup (reading) | 9.5 | 19 -> 22 |
| 11:44-11:45 | proxy convention (binarize test) | 1 | 22 |
| 11:45-11:54 | mise floor board strip + kamidana/nagashi props | 9 | 22 -> 23 |
| 11:54-12:27 | the decorator (placement, loot, 59 new checks), all 5 rooms, loot, yard + street | 33 | 23 -> 29 |
| 12:27-12:40 | build, binarize, pack, test-island world + mission rebuild, renders | 13 | 29 -> 32 |
| 12:40-12:43 | G4 checklist + progress | 2.5 | 32 -> 33 |

The decorator was the big stretch: it's the new shared code every later furnished building uses. The rooms
themselves came out of it in the same run (all five ROOM DONE lines share one timestamp).

## L1 time log, summarised (TIMELOG_L1.md)

| Stretch | What | Items | Minutes | 5-hour % |
|---|---|---|---|---|
| 12:44-12:48 | setup (reading) | - | 4 | 33 -> 35 |
| 12:48-12:49 | era checks (50 kept, 3 swaps inside items) | - | 0.5 | 35 |
| 12:49-12:58 | life-layer kit (lkit: text, mounting) | - | 10 | 35 -> 37 |
| 12:58-13:12 | A: walls, posts, beams + decorator mounting | 14 | 14 | 37 -> 41 |
| 13:12-13:17 | B: religious corner | 3 | 5 | 41 |
| 13:17-13:24 | C: meals and kitchen | 9 | 7 | 41 -> 43 |
| 13:24-13:28 | D: living rooms | 10 | 4 | 43 -> 44 |
| 13:28-13:32 | E: work at home | 8 | 4 | 44 -> 45 |
| 13:32-13:35 | F: tier markers | 6 | 3.5 | 45 |
| 13:35-13:38 | materials, PBO pack, sheets | - | 3 | 45 -> 46 |

Twice the items of B3a in 13 more minutes: 50 items / 185 models in 55 min. After the first group (which built
the wall/beam mounting), groups of 3-10 items took 3.5-7 minutes each.

## L2 time log, summarised (TIMELOG_L2.md)

| Stretch | What | Items | Minutes | 5-hour % |
|---|---|---|---|---|
| 13:45-13:50 | setup (reading) | - | 5 | 0 -> 3 |
| 13:50-14:08 | text fix: B3b + L1 text back-facing (invisible) and mirrored; new TXT check; 37 models rebuilt, 3 PBOs repacked | - | 18 | 3 -> 5 |
| 14:08-14:10 | era checks (24 kept, 7 swaps inside items) | - | 1.5 | 5 |
| 14:10-14:15 | 2 materials (net, foliage) | - | 5 | 5 |
| 14:15-14:20 | autumn yard: rice racks, persimmons, moon-viewing, scarecrow | 4 | 5 | 5 -> 7 |
| 14:20-14:23 | farm tools, broom, ladder, charcoal | 4 | 3 | 7 |
| 14:23-14:26 | potted plants, bird cage, bamboo pipe, stable yard | 4 | 3 | 7 -> 8 |
| 14:26-14:29 | road story: travel gear, palanquin, spilled tenbin, bench dressing, stool, footwear | 6 | 3 | 8 -> 9 |
| 14:29-14:31 | nets, boat | 2 | 2 | 9 |
| 14:31-14:34 | fire gear, sandals for sale, shutters, fallen lantern | 4 | 3.5 | 9 |
| 14:34-14:41 | PBO pack, sheets, shared-code re-runs | - | 7 | 9 -> 11 |

The text fix was the one big stretch (18 min). The 24 items themselves took 20 minutes of group work.

## Running total, Phase B + life layer (2026-09-29/30)

B0 409k, B1 453k, B2 715k, B3a 498k, B3b 519k, B4 576k, L1 654k, L2 581k = **about 4.4M tokens**, weekly **about 18% -> 27%**.

## C1 time log, summarised (TIMELOG_C1.md)

| Stretch | What | Minutes | 5-hour % |
|---|---|---|---|
| 16:11-16:13 | well diagnostic removed, jp_site repacked | 1.5 | 26 -> 27 |
| 16:13-16:25 | setup (reading) + a 9x faster ray check | 12 | 27 -> ? |
| 16:25-16:45 | (not logged: template options detached / tokaido / 5 ken / upper storey / stable, family pipeline) | 20 | |
| 16:45-17:23 | all 81 shells: 69 townhouse units, 8 post-town houses, 4 inns, checks, pack | 38 | -> 39 |
| 17:23-17:25 | island street + world/mission rebuild, sheets | 2 | 39 -> 40 |

81 shells in 74 minutes, for about the same tokens as 24 props: once the template can express a building,
its variants are nearly free.

## C2 time log, summarised (TIMELOG_C2.md, one stretch per family as asked)

| Stretch | What | Shells | Minutes | 5-hour % |
|---|---|---|---|---|
| 17:28-17:37 | setup (reading) | - | 9 | 42 -> 44 |
| 17:37-18:03 | the rural template (5 kinds) + 5 test shells | - | 26 | 44 -> 50 |
| 18:03-18:05 | DW06 Kanto farmhouse | 4 | 1.5 | 50 |
| 18:05-18:08 | DW07 Kinai farmhouse with ox | 4 | 3 | 50 |
| 18:08-18:08 | DW01 hut east | 4 | 0.5 | 50 |
| 18:08-18:12 | DW30 hut west | 5 | 3.5 | 50 -> 51 |
| 18:12-18:15 | DW24 shed / barn | 4 | 2.5 | 51 |
| 18:15-18:16 | grand inn storey source check | - | 1.5 | 51 -> 52 |
| 18:17-18:21 | hamlet placement + world/mission rebuild | 7 placed | 4 | 52 |
| 18:21-18:29 | re-runs after shared-code changes | - | 8.5 | 52 -> 55 |
| 18:29-18:31 | render sheets | - | 1 | 55 -> 56 |

The template was the cost (26 min, ~6% of the 5-hour window); after it, whole building families took 0.5-3.5
minutes each. Same lesson as C1: build the template once, the variants are nearly free.

## C3 time log, summarised (TIMELOG_C3.md)

| Stretch | What | Minutes | 5-hour % |
|---|---|---|---|
| 18:42-18:47 | setup (reading) | 5 | 0 -> 3 |
| 18:47-19:01 | kura template + 3 shells | 13.5 | 3 -> ? |
| 19:01-19:18 | furnishing kit (furnishkit, fittings, furnish_sets) | 17 | -> 12 |
| 19:18-19:33 | all 14 furnished variants in one run (per-type lines share timestamps) | 15 | 12 -> 14 |
| 19:33-19:40 | island swap + street + hamlet dressing, world/mission rebuild | 6.5 | 14 -> 15 |
| 19:40-19:50 | re-runs (105 buildings, 6,001 checks) | 9 | 15 -> 16 |
| 19:50-19:53 | sheets + checklist | 3.5 | 16 -> 20 |

## Running total: Phase B + life layer + G4 fixes + Phase C wave 1 (2026-09-29/30)

B0 409k, B1 453k, B2 715k, B3a 498k, B3b 519k, B4 576k, L1 654k, L2 581k, F1 573k, C1 532k, C2 658k, C3 793k =
**about 6.96M tokens**, weekly **about 18% -> 36%**.
