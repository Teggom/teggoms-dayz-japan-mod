#!/usr/bin/env python3
r"""All 60 townhouse template combinations (frontage 2/3/4 x Kamigata/Edo x end-left/end-right/middle/corner-left/
corner-right x toriniwa left/right) built with the B2 party parts: closed convex components (Geometry / View / Fire),
the C12 roof-poke check, no placeholders left, face counts against each unit's budget class
(townhouse.budget_class: 'large' for Kamigata 4-ken end / corner, else 'townhouse'). Writes combos.json.

  python buildings/townhouse_unit_test/combos.py
"""
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import townhouse  # noqa: E402
from jpparts import mlod, raycheck  # noqa: E402
sys.path.insert(0, os.path.join(DEV, "buildings"))
import registry  # noqa: E402


def main():
    t0 = time.time()
    rows = []
    for fr, rg, pos, tori in itertools.product((2, 3, 4), ("kamigata", "edo"),
                                               ("end_l", "end_r", "middle", "corner_l", "corner_r"), ("left", "right")):
        kw = dict(frontage=fr, region=rg, tori=tori)
        if pos == "middle":
            kw["position"] = "middle"
        else:
            kw["position"], kw["free"] = pos.split("_")[0], {"l": "left", "r": "right"}[pos[-1]]
        H, info = townhouse.build(**kw)
        L = {mlod.lod_name(l.resolution): l for l in H.lods()}
        probs = []
        for w in ("Geometry", "View Geometry", "Fire Geometry"):
            comps = [c for c in L[w].selections if c.startswith("Component")]
            bad = [c for c in comps if mlod.component_report(L[w], c)]
            if bad:
                probs.append("%s: %d components not closed / convex" % (w, len(bad)))
        pk = raycheck.roof_pokes(H.solids)
        if pk:
            probs.append("C12: %d pokes, e.g. %s" % (len(pk), pk[:2]))
        if info["placeholders"]:
            probs.append("placeholders: %s" % info["placeholders"])
        f = [len(L["Resolution %d" % k].faces) for k in (1, 2, 3)]
        bc = townhouse.budget_class(**kw)
        rows.append({"params": kw, "faces": f, "budget_class": bc,
                     "in_budget": all(a <= b for a, b in zip(f, registry.BUDGETS[bc])), "problems": probs})
        print("%-4s %-80s %s%s" % ("OK" if not probs else "FAIL", kw, f, ("  " + "; ".join(probs)) if probs else ""))
    worst = max(rows, key=lambda r: r["faces"][0])
    over = [r for r in rows if not r["in_budget"]]
    res = {"built": len(rows), "with_problems": sum(1 for r in rows if r["problems"]),
           "budgets": {k: registry.BUDGETS[k] for k in ("townhouse", "large")},
           "over_budget": len(over), "worst": worst, "rows": rows}
    with open(os.path.join(HERE, "combos.json"), "wb") as f:
        f.write(json.dumps(res, indent=1).encode("utf-8"))
    print("%d combos, %d with problems, %d over their budget class; worst %s %s (%.0f s)" % (
        len(rows), res["with_problems"], len(over), worst["faces"], worst["params"], time.time() - t0))
    return 1 if res["with_problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
