"""D3 debug: which Geometry components block a sliding door's doorway column (machiya verify.door_world).
  python spikes/D3/dbg_door.py <key> <door index 1..>"""
import math, os, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import pipeline, registry, shellcheck  # noqa
from jpparts import mlod, checks as C  # noqa
key, k = sys.argv[1], int(sys.argv[2])
bd = pipeline.build_model(registry.get(key), stage=False)
M = bd["M"]
L = {mlod.lod_name(l.resolution): l for l in mlod.read_mlod(bd["mlod"])}
gc = C.components(L["Geometry"])
d = M.doors[k - 1]
print(getattr(d, "label", ""), shellcheck.MV.door_world(d, gc))
bones = [a["bone"] for a in d.anims]
ax = d.action
y0 = ax[1] - 1.0
print("action", [round(v, 3) for v in ax], "y0", round(y0, 3))
for c in gc:
    if c["door"] in bones:
        continue
    b = c["bbox"]
    if b[0] < ax[0] + 0.5 and b[1] > ax[0] - 0.5 and b[4] < ax[2] + 0.5 and b[5] > ax[2] - 0.5 and b[3] > y0 + 0.05 and b[2] < y0 + 1.95:
        print(c["name"], c["door"], [round(v, 3) for v in b])
for nm in sys.argv[3:]:
    for c in gc:
        if c["name"] == nm:
            print(nm, c["door"], [round(v, 3) for v in c["bbox"]])
if "--head" in sys.argv:
    for c in gc:
        b = c["bbox"]
        if c["door"] in bones:
            continue
        if b[2] > y0 + 0.5 and b[2] < y0 + 2.05 and b[0] < ax[0] + 0.7 and b[1] > ax[0] - 0.7 and b[4] < ax[2] + 0.7 and b[5] > ax[2] - 0.7:
            print("HEAD?", c["name"], [round(v, 3) for v in b])
