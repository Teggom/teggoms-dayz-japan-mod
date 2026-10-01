import sys, os
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
from jpparts import zfight as Z
key, x, z = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
res = "--res" in sys.argv
b = registry.get(key)
mod = P.load_module(b)
M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
if res:
    Z.resolve(M)
out = []
for s in M.solids:
    bb = s.bbox()
    if bb[0] - 0.05 <= x <= bb[1] + 0.05 and bb[4] - 0.05 <= z <= bb[5] + 0.05 and s.vis:
        out.append((round(bb[3], 3), s.tag, getattr(s, "src", ""), sorted(s.vis), getattr(s, "interior", False), [round(v, 3) for v in bb]))
for o in sorted(out)[-8:]:
    print(o)
