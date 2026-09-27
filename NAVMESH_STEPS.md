# Generating the test island's navmesh (Stephen, ~15 min, one time)

**Why:** the navmesh is the walking map that zombies and animals use. The island currently borrows vanilla
Livonia's as a stopgap, which lets it boot but is wrong for AI. These steps make our own. They need to be redone
only after the terrain or baked objects change. Our build switches to the new file automatically.

**Before you start:** the live server can keep running (it uses its own port). The **Japan test server
(`start-japan-test-island.bat`) must be off.** The P: drive must exist: if `P:\JP` isn't there, run
`subst P: D:\DayZToolsExtract` in a command prompt first.

## Steps

1. Double-click `D:\DayZ-Server_AI-20260907-MultiMap\start-japan-navmesh-server.bat`.
   - A DayZDiag window opens. It is the game engine running as a data server on port 2412, loading the island with
     an empty mission.
2. Wait about 30-60 s until it has finished loading. The window stops changing.
3. Open `C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\NavMeshGenerator\NavMeshGenerator_x64.exe`.
4. In NavMeshGenerator, menu **Generation → Connect Data Server**.
   - It should report it is connected. If it asks for a port or address, use `127.0.0.1` and `2412`.
5. Menu **Generation → Start generation**.
   - On a 2 × 2 km island this should take minutes, not hours. Wait until it says it has finished.
6. Menu **File → Save NavMesh** and save as exactly:
   `P:\JP\worlds\testisland\navmesh\japantestisland.nm`
   (create the `navmesh` folder if the dialog needs it).
7. Close NavMeshGenerator, then close the DayZDiag window.
8. Tell me it's saved.
   - I rebuild the world: about 15 s, using our own navmesh instead of Livonia's.
   - Then the next test boot has zombies and animals walking the island properly.

## If something differs

- The menu names come from Bohemia's documentation and weren't checked on this machine. If a label is different,
  pick the closest one, or send me a screenshot.
- If DayZDiag shows an error or closes, just tell me. Its log is in
  `D:\DayZ-Server_AI-20260907-MultiMap\ServerProfileJapanNavmesh\`, and I'll read it.
- Source for the procedure: https://community.bistudio.com/wiki/DayZ:Generating_navigation_mesh
