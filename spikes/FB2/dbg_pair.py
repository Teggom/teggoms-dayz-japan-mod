import sys, os
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
from jpparts import zfight as Z
key, ta, tb = sys.argv[1:4]
b = registry.get(key)
mod = P.load_module(b)
M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
for s in M.solids:
    s.finalize()
r = Z.coplanar(M, lods=(1,))
for cat in ("same", "hidden", "opposite"):
    xs = [x for x in r[cat] if {x[2], x[3]} == {ta, tb}]
    print(cat, len(xs))
    for x in xs[:6]:
        print("  ", x[:10])
occ = Z._Occ(M, 1)
for x in [x for x in r["hidden"] if {x[2], x[3]} == {ta, tb}][:3]:
    c = x[6]; n = x[7]
    for sg in (1, -1):
        p = tuple(c[i] + sg * n[i] * 0.004 for i in range(3))
        hit = [ (M.solids[occ.sol[i][0]].tag, M.solids[occ.sol[i][0]].vis) for i in occ.cell.get((int(p[0]//1), int(p[2]//1)), ()) if occ.sol[i][0] not in (x[10], x[11]) and all(Z._dot(nn, p) - d < -1e-4 for nn, d in occ.sol[i][2])]
        print("side", sg, p, hit[:5])
