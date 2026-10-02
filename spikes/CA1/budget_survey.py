#!/usr/bin/env python3
"""CA1: survey the prop budget classes in use (sidecars' "budget") and the faces from every prop builder's checks.json,
against the old tables and PLAYBOOK §12's simple set. Read-only."""
import collections
import glob
import json
import os

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
NEW_F = {"furniture": 1000, "small": 800, "medium": 1500, "detail": 1500, "statue": 3000}
NEW_S = {"small": (800, 300, 300), "box": (600, 300, 120), "medium": (1500, 600, 200), "detail": (1500, 600, 250),
         "statue": (3000, 1150, 400)}

faces = {}
for b in ("B3a", "L1", "S1", "W2F", "B3b", "L2"):
    for k, v in json.load(open(os.path.join(DEV, "spikes", b, "checks.json"), encoding="utf-8"))["models"].items():
        faces[k] = (b, v["faces"], v["pass"])
budget = {}
for area in ("furniture", "site"):
    for f in glob.glob(os.path.join(DEV, "src", "JP", area, "*", "*.prop.json")):
        for m in json.load(open(f, encoding="utf-8"))["models"]:
            budget[os.path.basename(m["p3d"])[:-4]] = (area, m.get("budget"))
use = collections.Counter((a, str(c)) for a, c in budget.values())
print("classes in use:", dict(use))
for k, (area, cls) in sorted(budget.items()):
    if k not in faces:
        continue
    b, f, ok = faces[k]
    r1, r2, r3 = f.get("Resolution 1", 0), f.get("Resolution 2", 0), f.get("Resolution 3", 0)
    if area == "furniture":
        lim = NEW_F.get(cls, cls if isinstance(cls, int) else None)
        over = lim is not None and r1 > lim
        if over or cls in ("detail_l", "altar", "statue"):
            print("F %-4s %-40s %-9s R1 %5d  new %s  %s" % (b, k, cls, r1, lim, "OVER +%d%%" % round((r1 - lim) * 100 / lim) if over else ""))
    else:
        lim = NEW_S.get(cls)
        if lim is None:
            print("S ?", k, cls)
            continue
        over = [g > m for g, m in zip((r1, r2, r3), lim)]
        if any(over) or cls == "statue":
            pct = max((g - m) * 100.0 / m for g, m in zip((r1, r2, r3), lim))
            print("S %-4s %-40s %-9s R %5d %4d %4d  new %s  %s" % (b, k, cls, r1, r2, r3, lim, "OVER +%d%%" % round(pct) if any(over) else ""))
