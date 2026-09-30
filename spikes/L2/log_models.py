"""Append one time-log line per finished L2 model (built AND all checks pass), numbered, via tlog.py.
python log_models.py <5h%> <wk%> prop [prop ...]
Tag: the prop's first intact model = 'new model', other intact models = 'variant', any other state = 'abandoned';
' (batch)' because one build run produced them. Models already logged (spikes/L2/_logged.json) are skipped."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
h5, wk, props = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path[:0] = [HERE, os.path.join(HERE, "..", "B3b")]
import build_l2  # noqa: E402

chk = json.load(open(os.path.join(HERE, "checks.json"), encoding="utf-8"))["models"]
lp = os.path.join(HERE, "_logged.json")
logged = json.load(open(lp, encoding="utf-8")) if os.path.isfile(lp) else []
reg = build_l2.l2_props(build_l2.B.registry())
want = {p if p.startswith("jp_s_") else "jp_s_" + p for p in props}
for prop in reg:
    if prop["id"] not in want:
        continue
    first = True
    for m in prop["models"]:
        intact = m["state"] == "intact"
        tag = ("new model" if first else "variant") if intact else "abandoned"
        if intact:
            first = False
        if m["p3d"] in logged:
            continue
        if not chk.get(m["p3d"], {}).get("pass"):
            print("NOT logged (checks fail or not built):", m["p3d"])
            continue
        logged.append(m["p3d"])
        subprocess.run([sys.executable, os.path.join(HERE, "tlog.py"), "#%d" % len(logged), m["p3d"],
                        tag + " (batch)", h5, wk], check=True)
with open(lp, "wb") as f:
    f.write(json.dumps(logged, indent=0).encode("utf-8"))
