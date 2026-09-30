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
| 2026-09-30 09:10 (local, -04:00) | B3a (baseline) | launched: 24 interior props, one agent, per-model time log in TIMELOG_B3a.md | pending | | before: **19%** (5-hour 1%) |
