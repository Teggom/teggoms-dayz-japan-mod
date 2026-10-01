"""python spikes/FB2/endgap.py [--jobs N] [key ...]: interior wall panels whose vertical END is free (a point 1.5 cm
past the end, at 5 heights, inside no other solid): a see-through slit at a wall end / missing post."""
import sys, os, collections
from multiprocessing import Pool
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
TAGS = ("infill", "kokabe", "panel", "infill_base", "board", "okabe")


def one(key):
    import registry, pipeline as P
    from jpparts import zfight as Z
    b = registry.get(key)
    mod = P.load_module(b)
    M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
    for s in M.solids:
        s.finalize()
    occ = Z._Occ(M, 1)
    idx = {id(s): i for i, s in enumerate(M.solids)}
    out = []
    for s in M.solids:
        if 1 not in s.vis or s.tag not in TAGS or not getattr(s, "interior", False) or not s.closed:
            continue
        bb = s.bbox()
        dx, dz, dy = bb[1] - bb[0], bb[5] - bb[4], bb[3] - bb[2]
        if dy < 0.3 or min(dx, dz) > 0.2 or max(dx, dz) < 0.2:
            continue
        ax = 0 if dx >= dz else 2
        c = ((bb[0] + bb[1]) / 2, (bb[2] + bb[3]) / 2, (bb[4] + bb[5]) / 2)
        for end, sg in ((bb[1] if ax == 0 else bb[5], 1), (bb[0] if ax == 0 else bb[4], -1)):
            free = 0
            for k in range(5):
                y = bb[2] + dy * (k + 0.5) / 5
                p = [c[0], y, c[2]]
                p[ax] = end + sg * 0.015
                if not occ.inside(tuple(p), (idx[id(s)],)):
                    free += 1
            if free >= 3:
                out.append((getattr(s, "src", ""), s.tag, tuple(round(v, 2) for v in (p[0], c[1], p[2])), free))
    return key, b.get("dir", key), out


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
    for key, d, out in res:
        fam[d] += len(out)
        if out and len(keys) < 15:
            print(key, len(out))
            for o in out[:12]:
                print("   ", o)
    for d in sorted(fam):
        print("%-20s free wall ends %d" % (d, fam[d]))
