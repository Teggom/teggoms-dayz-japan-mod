"""Re-run B3a's (and B4's props_fittings) model checks WITHOUT touching their outputs: B3a's build.write_all with its
masters, checks.json and sidecars redirected into spikes/L1/_build/b3a_recheck/. Compares the pass count with
B3a's committed spikes/B3a/checks.json. (L1 changed the shared decor.py, so the brief asks for this re-run.)"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
B3A = os.path.join(DEV, "spikes", "B3a")
sys.path[:0] = [B3A]
import build as B  # noqa: E402

tmp = os.path.join(HERE, "_build", "b3a_recheck")
os.makedirs(tmp, exist_ok=True)
old = json.load(open(os.path.join(B3A, "checks.json"), encoding="utf-8"))["models"]
B.OUT = os.path.join(tmp, "out")
B.SRC = os.path.join(tmp, "src")
B.CHECKS = os.path.join(tmp, "checks.json")
if os.path.isfile(B.CHECKS):
    os.remove(B.CHECKS)
reg = B.registry()
B.write_all(reg)
new = json.load(open(B.CHECKS, encoding="utf-8"))["models"]
diff = [k for k in new if old.get(k, {}).get("pass") != new[k]["pass"]]
fc = [k for k in new if old.get(k, {}).get("faces") != new[k]["faces"]]
print("B3a/B4 models re-checked: %d, pass %d (committed checks.json: %d models, pass %d); pass changed: %s; faces "
      "changed: %s" % (len(new), sum(1 for v in new.values() if v["pass"]), len(old),
                       sum(1 for v in old.values() if v["pass"]), diff, fc))
