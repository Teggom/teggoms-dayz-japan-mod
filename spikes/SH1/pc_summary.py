"""Summarise data/placecheck/island/failures.csv for the SH1 objects (and the street units SH1 placed), per model.

  python spikes/SH1/pc_summary.py [source-substring ...]   (default: SH1.csv)
"""
import collections
import csv
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
keys = sys.argv[1:] or ["SH1.csv"]
rows = list(csv.DictReader(open(os.path.join(DEV, "data", "placecheck", "island", "failures.csv"), encoding="utf-8")))
print("failures:", len(rows), dict(collections.Counter(os.path.basename(r["source"].split(":")[0]) for r in rows)))
agg = collections.defaultdict(list)
for r in rows:
    if not any(k in r["source"] for k in keys):
        continue
    m = r["p3d"].replace("/", "\\").split("\\")[-1]
    agg[(m, r["category"], r["problem"][:40])].append(
        (float(r["float_m"] or 0), float(r["sink_m"] or 0), r["side"], r["row"], r["x"], r["z"]))
for k, v in sorted(agg.items(), key=lambda kv: -len(kv[1])):
    print("%-42s %-8s %-40s n=%2d float<=%.3f sink<=%.3f e.g. row %s (%s, %s)" % (
        k[0], k[1], k[2], len(v), max(a[0] for a in v), max(a[1] for a in v), v[0][3], v[0][4], v[0][5]))
