"""python spikes/FB2/verify_all.py [jobs] [key ...]: pipeline --verify-only over every shipped building (or the keys)
in parallel (pipeline.verify_parallel; logs data/C/_build/verify_logs), then a per-family summary from the logs."""
import os, re, sys, glob
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
keys = sys.argv[2:] or [b["key"] for b in registry.BUILDINGS if b["ship"]]
P.verify_parallel(keys, jobs)
res = {}
for f in glob.glob(os.path.join(P.TEMP, "verify_logs", "verify_*.log")):
    t = open(f, "rb").read().decode("utf-8", "replace")
    for m in re.finditer(r"RESULT (\S+): (PASS|FAIL) \((\d+) checks, (\d+) failures\)", t):
        res[m.group(1)] = (m.group(2), int(m.group(3)), int(m.group(4)))
    for m in re.finditer(r"RESULT: (PASS|FAIL) \((\d+) checks, (\d+) failures\)", t):
        res.setdefault("_machiya_like_" + os.path.basename(f), (m.group(1), int(m.group(2)), int(m.group(3))))
fam = {}
for k, v in res.items():
    b = registry.get(k) if not k.startswith("_") else {"key": k}
    d = b.get("dir", b["key"])
    a = fam.setdefault(d, [0, 0, 0, 0])
    a[0] += 1; a[1] += v[0] == "PASS"; a[2] += v[1]; a[3] += v[2]
for d, a in sorted(fam.items()):
    print("%-40s %3d buildings, %3d pass, %5d checks, %d failures" % (d, a[0], a[1], a[2], a[3]))
print("buildings with results: %d / %d" % (len(res), len(keys)))
for k, v in sorted(res.items()):
    if v[0] != "PASS":
        print("FAIL", k, v)
