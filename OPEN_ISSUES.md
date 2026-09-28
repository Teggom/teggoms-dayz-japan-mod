# Open issues: things Stephen noticed or deferred

Each fix is one place, and it propagates: materials are shared files, parts are generator code, and buildings
rebuild from parts by script.

| Date | Issue | Where the fix goes | Status |
|---|---|---|---|
| 2026-09-27 | **Something sticks out of some roofs** on the parts contact sheets. Stephen wants a closer look later | The roof part generators in `parts/kit/`. If the size and connectors stay the same, fix the part and rerun the building builds; every building using it updates | To inspect |
| 2026-09-27 | Timber reads quite reddish on the parts sheets | One material (`jp_common` wood), after seeing a house in game | Check on the first house |
| 2026-09-27 | The bow on the back sits sideways and shows an extra arrow | Weapon carry offsets (`JP_Yumi` / `JP_Yumi_XB` config, memory points) | Deferred: how items sit on the body comes later |
| 2026-09-27 | Clothes need rework: chest seam, baggy arms, legs clip when walking | Wardrobe track, research-first. One set shared by players and infected. See `playbook/GEAR_SLOTS.md` | Deferred |
| 2026-09-27 | 5 gravel road pieces sit 0.1–0.2 m off the ground (placecheck) | Road placement in `spikes/T_terrain/tools/objects.py`, unless the engine drapes them | Check in game |
| 2026-09-27 | The navmesh predates the new machiya | Stephen reruns `NAVMESH_STEPS.md` (~15 min) | Optional, after the house check |
| 2026-09-27 | The bamboo pole is held one-handed (it inherits LongWoodenStick) | A script-registered two-handed profile (flora report) | Deferred |
