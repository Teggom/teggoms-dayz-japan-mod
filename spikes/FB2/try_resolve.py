import sys, os, time
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
from jpparts import zfight as Z
for key in sys.argv[1:]:
    b = registry.get(key)
    mod = P.load_module(b)
    M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
    for s in M.solids:
        s.finalize()
    t = time.time()
    lg = []
    Z.resolve(M, log=lg)
    r = Z.coplanar(M)
    print(key, lg, "after: same %d opp %d hidden %d (%.1f s)" % (len(r["same"]), len(r["opposite"]), len(r["hidden"]), time.time() - t))
    for l in Z.summary(r, "same", 10):
        print("   ", l)
