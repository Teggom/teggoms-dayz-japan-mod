#!/usr/bin/env python3
r"""budget_report.py - every DELIBERATE face-budget overage in the project (PLAYBOOK §12 'budgets are guidance',
Stephen 2026-10-01: +30-50 % is fine when an object needs it, not as the norm). Agent CA1, 2026-10-01. Read-only.

  python tools/budget_report.py

Reads the last check results: props = spikes/<builder>/checks.json (C5 detail "over_budget", set by fkit.budget_fit
when a part carries over_budget_ok), buildings = buildings/*/checks/*.json (C5 detail "OVER BUDGET", set by
buildings/registry.budget_check when the registry entry carries over_budget_ok). Exit 1 if any overage is NOT
deliberate (that check failed)."""
import glob
import json
import os
import re
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PROP_BUILDERS = ("B3a", "L1", "S1", "W2F", "B3b", "L2")


def main():
    rows, bad = [], 0
    for b in PROP_BUILDERS:
        p = os.path.join(DEV, "spikes", b, "checks.json")
        if not os.path.isfile(p):
            continue
        for k, v in sorted(json.load(open(p, encoding="utf-8"))["models"].items()):
            for c in v["checks"]:
                o = c["detail"].get("over_budget") if c["id"] == "C5" and isinstance(c["detail"], dict) else None
                if o:
                    rows.append(("prop " + b, k, "+%.1f %%" % o["over_pct"], "/".join(map(str, o["caps"])),
                                 o["deliberate"], o["reason"]))
                    bad += 0 if o["deliberate"] else 1
    for p in sorted(glob.glob(os.path.join(DEV, "buildings", "*", "checks", "*.json"))):
        for c in json.load(open(p, encoding="utf-8")).get("checks", []):
            if not c.get("check", "").startswith("C5 face budget"):
                continue
            m = re.search(r"OVER BUDGET \+([\d.]+) % \((deliberate: )?(.*)\)$", str(c.get("detail", "")))
            if m:
                cap = re.search(r"\((.*)\)", c["check"]).group(1)
                rows.append(("building", os.path.basename(p)[:-5], "+%s %%" % m.group(1), cap, bool(c["ok"]),
                             m.group(3)))
                bad += 0 if c["ok"] else 1
    print("%-10s %-30s %-8s %-26s %-6s %s" % ("kind", "model", "over", "class caps", "ok", "reason"))
    for r in rows:
        print("%-10s %-30s %-8s %-26s %-6s %s" % (r[0], r[1], r[2], r[3], "yes" if r[4] else "NO", r[5]))
    print("%d overage(s), %d not deliberate" % (len(rows), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
