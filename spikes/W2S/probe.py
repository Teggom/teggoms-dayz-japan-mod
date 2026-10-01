"""W2S: solids over a model-frame point per LOD (top heights): python spikes/W2S/probe.py <key> x z"""
import os, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings")); sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import registry, sacredkit
b = registry.get(sys.argv[1]); x, z = float(sys.argv[2]), float(sys.argv[3])
M, _, _ = sacredkit.model(name=b.get("recipe_name", b["name"]), **b["params"])
for lv in (1, 2, 3):
    hits = []
    for s in M.solids:
        if lv not in s.vis: continue
        bb = s.bbox()
        if bb[0] <= x <= bb[1] and bb[4] <= z <= bb[5]:
            hits.append((round(bb[3], 2), s.tag, getattr(s, "src", "")))
    print(lv, sorted(hits, reverse=True)[:5])
