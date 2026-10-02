# Japan test island: FX5 re-check (~5 min) — gate floors, the honjin wall joints, the headman hedge

Short re-check of the four things you flagged on the 3a / 3b walk (2026-10-02). The old 3a / 3b walk text is in git
history. **Wave 3c-1's section will be added below by the next agent.**

What changed: every compound gate (all 9: samurai, Kanto headman, honjin x2, merchant, foot-soldier row, doshin x2,
stable / timber / foundry yards) now has a packed-earth sill 10 cm high with sloped edges instead of a floor lying
exactly at ground height (that was the flicker). The honjin's side board fences now run right up to the plastered
street wall (there was a 0.7 m gap). The Kanto headman's hedge is rebuilt as one continuous clipped hedge with a new
leaf texture and a leafy top edge. Pictures: `research/production/contact_sheets/fx5_gates_joints.jpg` and
`fx5_hedge.jpg` (before left, after right).

**Start:**
1. Run `start-japan-test-island.bat` in the server folder. It starts only the test server, on its own port.
2. When the server is up, run `start-japan-test-client.bat` to join. You spawn at ~1024, 985.

**If it won't load, kicks you, or something is invisible:** just tell me. The lead reads the server and client logs.

## 1. Gates: no flicker under the gate (2 min)

At each gate: look at the floor under the gate first from ~30-50 m away, then walk up to it, then walk through it
both ways (open the leaves).
- **Honjin front gate** (1103.6, 1067.8; the roofed gate in the white plastered street wall).
- **Honjin back gate** (1109.5, 1020.5; the plain gate in the board fence at the back).
- **Timber yard gate** (1012.3, 922.0; wave 3b, the yard on the slope south of the spawn). Also, if you pass it,
  the **stable yard gate** (1068.8, 1062.8).
- One more on the way back: **doshin house gate** (963.2, 952.1).

Pass: the earth under each gate doesn't flicker or shimmer, near or far; the sill is a low, rounded hump you walk over
without a stumble or a hop; the gate leaves open and close without scraping into it; you can still drop / pick up loot
on it.

## 2. Honjin: plaster wall meets the board fence (1 min)

- **North-east corner** (1124.9, 1067.8) and **north-west corner** (1094.0, 1067.8) of the honjin compound: where the
  white plastered street wall meets the wooden side fence. Look from inside and from outside, try to walk through and
  look through at the joint.

Pass: no gap. The fence's last post stands against the plaster; you can't walk, see or shoot through the joint.

## 3. Kanto headman hedge (2 min)

- The tall clipped hedge round the Kanto headman's compound: the **west side** (x ~924, z 961-992) and the **back gate**
  (942.2, 991.9). Walk along it at eye level, close up and from ~15 m, and look at a corner.

Pass: it reads as one continuous clipped hedge: no repeating segments, no bulges, no visible seams every 1.8 m; leafy
top edge; corners closed. You still can't walk, see or shoot through it, and there's no slit beside the back-gate posts.
If it now looks too flat or too uniform, say so.

## 4. Town temple corridor U9: deliberately unchanged

U9 (the hondo -> kuri corridor) is left exactly as it was, on your call: corridor-to-hall joins get done at the end of
production on modular variants of the final halls (PRODUCTION_PLAN.md "Confirmed future work"). No need to look at it.
