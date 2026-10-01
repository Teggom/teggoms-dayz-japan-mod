"""python spikes/FB2/mlod_of.py <key> <out.p3d> [--no-resolve]: build a registry model in memory (+ zfight.resolve as
the pipeline does) and write its MLOD (no proxies) to out.p3d, for renders. Writes nothing else."""
import sys, os
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
from jpparts import zfight as Z, mlod
key, out = sys.argv[1], sys.argv[2]
b = registry.get(key)
mod = P.load_module(b)
M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
if "--no-resolve" not in sys.argv:
    Z.resolve(M)
mlod.write_mlod(out, M.lods(geo_props=P.GEO_PROPS, mass=b["mass"]))
print("wrote", out, M.bbox())
