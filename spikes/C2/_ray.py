import os, sys
import numpy as np
DEV = os.path.abspath(".")
sys.path.insert(0, "buildings"); sys.path.insert(0, "parts/kit")
import registry, ruralkit
from jpparts import mlod, raycheck as RC
b = registry.get(sys.argv[1])
M, floors, rooms = ruralkit.model(name=b["name"], **b["params"])
L = {mlod.lod_name(l.resolution): l for l in M.lods()}
e = np.array([float(v) for v in sys.argv[2].split(",")]); q = np.array([float(v) for v in sys.argv[3].split(",")])
d = (q - e) / np.linalg.norm(q - e)
T = RC.lod_triangles(L["Resolution 1"])
print("hit t", RC.cast(T, e[None], d[None], 60.0), "dist to q", np.linalg.norm(q - e))
for t in np.arange(0, np.linalg.norm(q - e), 0.05):
    p = e + d * t
    near = []
    for s in M.solids:
        if 1 not in s.vis: continue
        bb = s.bbox()
        if bb[0]-0.01 <= p[0] <= bb[1]+0.01 and bb[2]-0.01 <= p[1] <= bb[3]+0.01 and bb[4]-0.01 <= p[2] <= bb[5]+0.01:
            near.append(s.tag)
    if near: print(round(t,2), [round(v,3) for v in p], near[:5])
