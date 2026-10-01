"""W2S debug: which Geometry components set the head / clear of a rotation door (shellcheck.door_world_rot).
  python spikes/W2S/dbg_door.py <key> [door index 1..]"""
import os, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import pipeline, registry, shellcheck  # noqa
from jpparts import mlod, checks as C, raycheck as RC  # noqa
key = sys.argv[1]
k = int(sys.argv[2]) if len(sys.argv) > 2 else 1
bd = pipeline.build_model(registry.get(key), stage=False)
M = bd["M"]
L = {mlod.lod_name(l.resolution): l for l in mlod.read_mlod(bd["mlod"])}
gcomps = C.components(L["Geometry"])
d = M.doors[k - 1]
print(shellcheck.door_world_rot(d, gcomps))
obst = RC.open_state(gcomps, [d], 1.0)
ax = d.action
y0 = ax[1] - getattr(d, "act_h", 1.0)
print("action", ax, "y0", y0)
for c in obst:
    b = c["bbox"]
    if abs(b[0] - ax[0]) < 1.3 and b[4] < ax[2] + 0.4 and b[5] > ax[2] - 0.4 and y0 + 0.3 < b[2] < y0 + 2.3:
        print(c["name"], c["door"], [round(v, 3) for v in b])
