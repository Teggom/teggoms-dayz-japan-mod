"""Re-run L1's model checks WITHOUT touching its outputs: build_l1.write_all with masters, sidecars and checks.json
redirected into spikes/L2/_build/l1_recheck/. Compares with L1's committed spikes/L1/checks.json (pass and faces)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
L1 = os.path.join(DEV, "spikes", "L1")
sys.path[:0] = [L1]
import build_l1 as L  # noqa: E402

tmp = os.path.join(HERE, "_build", "l1_recheck")
os.makedirs(tmp, exist_ok=True)
old = json.load(open(os.path.join(L1, "checks.json"), encoding="utf-8"))["models"]
L.OUT_L1 = os.path.join(tmp, "out")
L.B.SRC = os.path.join(tmp, "src")
L.B.CHECKS = os.path.join(tmp, "checks.json")
if os.path.isfile(L.B.CHECKS):
    os.remove(L.B.CHECKS)
L.write_all(L.l1_props(L.B.registry()))
new = json.load(open(L.B.CHECKS, encoding="utf-8"))["models"]
diff = [k for k in new if old.get(k, {}).get("pass") != new[k]["pass"]]
fc = [k for k in new if old.get(k, {}).get("faces") != new[k]["faces"]]
print("L1 models re-checked: %d, pass %d (committed checks.json: %d models, pass %d); pass changed: %s; faces "
      "changed: %s" % (len(new), sum(1 for v in new.values() if v["pass"]), len(old),
                       sum(1 for v in old.values() if v["pass"]), diff, fc))
