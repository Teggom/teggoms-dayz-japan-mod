#!/usr/bin/env python3
"""CA1: compare every prop builder's checks.json with git HEAD: model count, pass, faces, and which checks changed
(only C5's budget text may change with the budget tidy-up). Lists every deliberate overage (C5 "over_budget").

  python spikes/CA1/propcheck.py [--keep-global]
--keep-global: put HEAD's "global" block (BIN / PBO results of the shipped ODOLs) back into checks.json after a
               --no-binarize re-run (the ODOLs are HEAD's, so their binarize result is HEAD's).
Exit 1 if a model is missing, a pass flips or faces change."""
import json
import os
import subprocess
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
BUILDERS = {"B3a": True, "L1": False, "S1": False, "W2F": False, "B3b": False, "L2": False}   # -> ensure_ascii


def head(rel):
    r = subprocess.run(["git", "show", "HEAD:" + rel], cwd=DEV, capture_output=True)
    return json.loads(r.stdout.decode("utf-8")) if r.returncode == 0 else None


def main(argv):
    bad = 0
    overs = []
    for b, asc in BUILDERS.items():
        rel = "spikes/%s/checks.json" % b
        p = os.path.join(DEV, rel)
        new = json.load(open(p, encoding="utf-8"))
        old = head(rel) or {"models": {}}
        nm, om = new["models"], old["models"]
        missing = sorted(set(om) - set(nm))
        flips = sorted(k for k in nm if k in om and om[k]["pass"] != nm[k]["pass"])
        faces = sorted(k for k in nm if k in om and om[k]["faces"] != nm[k]["faces"])
        changed = {}
        for k in nm:
            if k not in om:
                continue
            a = {c["id"] + c["name"]: c for c in om[k]["checks"]}
            for c in nm[k]["checks"]:
                key = c["id"] + c["name"]
                if key not in a or a[key]["detail"] != c["detail"] or a[key]["pass"] != c["pass"]:
                    changed[c["id"]] = changed.get(c["id"], 0) + 1
            for c in nm[k]["checks"]:
                if c["id"] == "C5" and isinstance(c["detail"], dict) and c["detail"].get("over_budget"):
                    o = c["detail"]["over_budget"]
                    overs.append((b, k, o["over_pct"], o["caps"], o["deliberate"], o["reason"]))
        npass = sum(1 for v in nm.values() if v["pass"])
        print("%-4s models %3d (HEAD %3d), pass %3d; missing %s; pass flips %s; faces changed %s; checks changed %s" % (
            b, len(nm), len(om), npass, missing, flips, faces, changed))
        bad += len(missing) + len(flips) + len(faces)
        if "--keep-global" in argv and "global" in old and new.get("global") != old["global"]:
            new["global"] = old["global"]
            new["summary"] = dict(new.get("summary", {}), **{k: v for k, v in old.get("summary", {}).items()
                                                             if k not in ("models", "pass")})
            with open(p, "wb") as f:
                f.write(json.dumps(new, indent=1, ensure_ascii=asc).encode("utf-8"))
            print("     global block restored from HEAD")
    print("deliberate overages (C5 over_budget):")
    for o in overs:
        print("  %-4s %-28s +%5.1f%% over %s  %s  %s" % (o[0], o[1], o[2], o[3], "ok" if o[4] else "NOT OK", o[5]))
    print("PROPCHECK", "PASS" if not bad else "FAIL (%d)" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
