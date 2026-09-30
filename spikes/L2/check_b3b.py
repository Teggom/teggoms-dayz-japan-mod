"""Re-run B3b's model checks WITHOUT touching its outputs (B3b's build.py would regenerate config.cpp without the L2
classes): B3b's build.write_all with masters, sidecars and checks.json redirected into spikes/L2/_build/b3b_recheck/.
Compares with B3b's committed spikes/B3b/checks.json (pass and faces)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
B3B = os.path.join(DEV, "spikes", "B3b")
sys.path[:0] = [B3B]
import build as B  # noqa: E402

tmp = os.path.join(HERE, "_build", "b3b_recheck")
os.makedirs(tmp, exist_ok=True)
old = json.load(open(os.path.join(B3B, "checks.json"), encoding="utf-8"))["models"]
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
print("B3b models re-checked: %d, pass %d (committed checks.json: %d models, pass %d); pass changed: %s; faces "
      "changed: %s" % (len(new), sum(1 for v in new.values() if v["pass"]), len(old),
                       sum(1 for v in old.values() if v["pass"]), diff, fc))
