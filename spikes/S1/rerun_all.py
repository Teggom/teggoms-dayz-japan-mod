"""S1 copy of spikes/C3/rerun_all.py (C3 file untouched): every earlier building re-checked after S1 changed furnishkit, furnish_sets, registry and the townhouse template (option mise_floor, off by default), in parallel:
machiya shell + shop + toilet + all C1 / C2 family shells (verify-only), then the townhouse combos.
  python spikes/S1/rerun_all.py [jobs]
"""
import json
import os
import subprocess
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
import registry  # noqa: E402
import pipeline  # noqa: E402

jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
keys = ["machiya_t3_01", "machiya_t3_01_shop", "toilet_t1_01"] + [
    b["key"] for b in registry.C1_TOWNHOUSES + registry.C1_POSTTOWN + registry.C1_HATAGO + registry.C2_FARMHOUSES +
    registry.C2_HUTS + registry.C2_SHEDS + registry.C3_KURA + registry.C3_FURNISHED + registry.S1_SHOPS]
ok = pipeline.verify_parallel(keys, jobs)
tot = fails = 0
res = {}
for b in [registry.get(k) for k in keys]:
    if "dir" in b:
        p = os.path.join(DEV, "buildings", b["dir"], "checks", b["key"] + ".json")
    else:
        p = os.path.join(DEV, "buildings", b["key"], "checks.json")
    c = json.load(open(p, encoding="utf-8"))
    n = c.get("checks_n") or len(c.get("checks", []))
    f = c.get("failures")
    if f is None:
        f = sum(1 for x in c.get("checks", []) if not x.get("ok"))
    res[b["key"]] = (n, f)
    tot += n
    fails += f
print("buildings %d, checks %d, failures %d" % (len(keys), tot, fails))
for k in ("machiya_t3_01", "machiya_t3_01_shop", "toilet_t1_01"):
    print(k, res[k])
fam = {}
for b in [registry.get(k) for k in keys if "dir" in registry.get(k)]:
    d = b["dir"]
    fam.setdefault(d, [0, 0, 0])
    fam[d][0] += 1
    fam[d][1] += res[b["key"]][0]
    fam[d][2] += res[b["key"]][1]
for d, v in fam.items():
    print("family %-10s shells %d checks %d failures %d" % (d, v[0], v[1], v[2]))
r = subprocess.run([sys.executable, os.path.join(DEV, "buildings", "townhouse_unit_test", "combos.py")], cwd=DEV,
                   capture_output=True, text=True)
print("combos:", (r.stdout.strip().splitlines() or ["?"])[-1], "rc", r.returncode)
sys.exit(0 if ok and not fails and r.returncode == 0 else 1)
