import sys, os
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
from jpparts import zfight as Z
key, tag = sys.argv[1], sys.argv[2]
b = registry.get(key)
mod = P.load_module(b)
M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
for s in M.solids:
    s.finalize()
Z.resolve(M, passes=8)
r = Z.coplanar(M)
xs = [x for x in r["same"] if tag in (x[2], x[3])]
for x in xs[:4]:
    A, B = M.solids[x[10]], M.solids[x[11]]
    print(x[:10], x[12])
    for S in (A, B):
        print("   ", S.tag, "closed", S.closed, "door", S.door, "vis", S.vis, "bbox", [round(c, 4) for c in S.bbox()], "nf", len(S.faces), Z._order(S, 0))
