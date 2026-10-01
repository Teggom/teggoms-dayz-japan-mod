"""W2P1 quick part test: build variants in memory, write MLOD to spikes/W2P1/tmp, run checks.check_part + C20 zfight.
usage: python spikes/W2P1/ptest.py module [variant ...]"""
import importlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "parts", "kit"))
from jpparts import checks, mlod, zfight as ZF  # noqa
mod = importlib.import_module("jpparts." + sys.argv[1])
regs = []
mod.register(lambda pid, vs, fn: regs.extend((pid, v, fn) for v in vs))
want = sys.argv[2:]
nf = 0
for pid, v, fn in regs:
    if want and v not in want:
        continue
    p = fn(v)
    path = os.path.join(HERE, "tmp", p.name + ".p3d")
    p.write(path)
    lods = mlod.read_mlod(path)
    res, counts = checks.check_part(p, path, lods)
    z = ZF.coplanar(p)
    import copy
    q = copy.deepcopy(p)
    ZF.resolve(q)
    z2 = ZF.coplanar(q)
    res.append(("C20 zfight after zfight.resolve (as the building pipeline)", not z2["same"],
                "%d raw same-facing pairs (%s) -> %d after resolve" % (len(z["same"]), "; ".join(ZF.summary(z, "same", 2)),
                                                                     len(z2["same"]))))
    if z["same"]:
        print("      note: raw C20 pairs: %s" % "; ".join(ZF.summary(z, "same", 3)))
    fails = [r for r in res if not r[1]]
    nf += len(fails)
    print("%-4s %-40s %s" % ("OK" if not fails else "FAIL", p.name, counts))
    for c, o, d in fails:
        print("      %s: %s" % (c, d))
print("failures", nf)
