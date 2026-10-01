"""FB2 z-fight census: python spikes/FB2/zcensus.py [--jobs N] [--out name] [key ...]
Builds every shipped building's model in memory (no files written except the census json) and runs
jpparts.zfight.coplanar on Resolution 1-3. Writes data/FB2/zcensus_<out>.json and prints per-family counts."""
import json
import os
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "tools", "common"))
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))


def one(key):
    import registry
    import pipeline as P
    from jpparts import zfight as Z
    b = registry.get(key)
    mod = P.load_module(b)
    if "params" in b:
        M, floors, rooms = mod.model(name=b.get("recipe_name", b["name"]), **b["params"])
    else:
        M, floors, rooms = mod.model()
    for s in M.solids:
        s.finalize()
    r = Z.coplanar(M)
    return key, b.get("dir", b["key"]), {"same": len(r["same"]), "opposite": len(r["opposite"]), "hidden": len(r["hidden"]),
                                         "same_area": round(sum(x[1] for x in r["same"]), 3),
                                         "same_top": Z.summary(r, "same", 40), "hid_top": Z.summary(r, "hidden", 8), "opp_top": Z.summary(r, "opposite", 5),
                                         "same_all": [x[:10] for x in r["same"]]}


def main(argv):
    jobs, out, keys = 8, "now", []
    it = iter(argv)
    for a in it:
        if a == "--jobs":
            jobs = int(next(it))
        elif a == "--out":
            out = next(it)
        else:
            keys.append(a)
    import registry
    if not keys:
        keys = [b["key"] for b in registry.BUILDINGS if b["ship"]]
    with Pool(jobs) as p:
        res = p.map(one, keys, chunksize=1)
    fam = {}
    doc = {}
    for key, d, r in res:
        doc[key] = dict(r, family=d)
        f = fam.setdefault(d, [0, 0, 0, 0.0, 0])
        f[4] += r["hidden"]
        f[0] += 1
        f[1] += r["same"]
        f[2] += r["opposite"]
        f[3] += r["same_area"]
    os.makedirs(os.path.join(DEV, "data", "FB2"), exist_ok=True)
    with open(os.path.join(DEV, "data", "FB2", "zcensus_%s.json" % out), "wb") as f:
        f.write(json.dumps(doc, indent=1).encode("utf-8"))
    print("family          n  visible same-normal pairs (area m2)  opposite  hidden(same mat+uv)")
    for d, (n, s, o, a, h) in sorted(fam.items()):
        print("%-18s %3d  %6d (%8.3f)  %8d  %6d" % (d, n, s, a, o, h))
    print("TOTAL same %d opposite %d" % (sum(v[1] for v in fam.values()), sum(v[2] for v in fam.values())))


if __name__ == "__main__":
    main(sys.argv[1:])
