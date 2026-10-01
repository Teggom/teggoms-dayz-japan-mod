"""python spikes/FB2/partcensus.py [--jobs N] [key ...]: jpparts.parttop.top_ends over shipped buildings (in memory)."""
import sys, os, collections
from multiprocessing import Pool
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))


def one(key):
    import registry, pipeline as P
    from jpparts import parttop as PT
    b = registry.get(key)
    mod = P.load_module(b)
    M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
    tags = collections.Counter(s.tag for s in M.solids if getattr(s, "interior", False) and 1 in s.vis)
    bad = PT.top_ends(M)
    return key, b.get("dir", key), len(bad), PT.summary(bad, 6), tags.most_common(12)


if __name__ == "__main__":
    args = sys.argv[1:]
    jobs = 8
    if args[:1] == ["--jobs"]:
        jobs, args = int(args[1]), args[2:]
    import registry
    keys = args or [b["key"] for b in registry.BUILDINGS if b["ship"]]
    with Pool(jobs) as p:
        res = p.map(one, keys, chunksize=1)
    fam = collections.Counter()
    famb = collections.Counter()
    for key, d, n, sm, tags in res:
        fam[d] += n
        famb[d] += 1 if n else 0
        if n and (len(keys) < 12 or "-v" in os.environ.get("PCV", "")):
            print(key, n); print("   " + "\n   ".join(sm)); print("   tags", tags)
    for d in sorted(fam):
        print("%-20s open-topped partition samples %5d in %d buildings" % (d, fam[d], famb[d]))
