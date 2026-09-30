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
