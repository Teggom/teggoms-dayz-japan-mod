"""FP2: compare each pipeline's checks.json (faces, pass) against the pre-FP2 baseline (spikes/FP2/_build/base/)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
rows = []
for x in ("B3a", "B3b", "L1", "L2", "S1"):
    base = json.load(open(os.path.join(HERE, "_build", "base", x + ".json"), encoding="utf-8"))["models"]
    now = json.load(open(os.path.join(DEV, "spikes", x, "checks.json"), encoding="utf-8"))["models"]
    for k, v in now.items():
        b = base.get(k)
        f1 = v["faces"].get("Resolution 1", 0)
        b1 = b["faces"].get("Resolution 1", 0) if b else None
        fails = [c["id"] for c in v["checks"] if not c["pass"]]
        if b1 != f1 or fails:
            bud = next((c["detail"].get("budget") for c in v["checks"] if c["id"] == "C5" and isinstance(c["detail"], dict)), None)
            rows.append((x, k, b1, f1, v["faces"].get("Resolution 2", 0), bud, fails))
only_fail = "--fail" in sys.argv
for r in rows:
    if only_fail and not r[6]:
        continue
    print("%-4s %-46s R1 %5s -> %5s  R2 %4s  budget %-5s %s" % (r[0], r[1], r[2], r[3], r[4], r[5], ",".join(r[6])))
print(len(rows), "rows")
