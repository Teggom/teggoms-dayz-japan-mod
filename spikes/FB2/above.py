"""python spikes/FB2/above.py <key> x z [y0]: solids hit by a vertical ray at model (x, z) from y0 up (R1)."""
import sys, os
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
from jpparts import parttop as PT
key, x, z = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
y0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
b = registry.get(key)
mod = P.load_module(b)
M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
hits = []
for s in M.solids:
    if 1 not in s.vis or not s.closed:
        continue
    h = PT._ray_up((s, s.bbox(), PT._planes(s)), (x, y0, z))
    if h is not None:
        b_ = s.bbox()
        hits.append((round(y0 + h, 3), s.tag, getattr(s, "src", ""), [round(v, 3) for v in b_]))
for h in sorted(hits):
    print(h)
