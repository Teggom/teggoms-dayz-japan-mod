"""C1: what already stands on the test island (placements, spawns, item grid)."""
import collections
import csv
import glob
import json
import os

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
pts = []
for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
    for r in csv.DictReader(open(p)):
        pts.append((os.path.basename(p), r["p3d"].replace("\\", "/").split("/")[-1], float(r["x"]), float(r["z"])))
for p in glob.glob(os.path.join(DEV, "test", "spawns", "*.json")):
    d = json.load(open(p))
    for o in d.get("Objects", []):
        pts.append((os.path.basename(p), o["name"], o["pos"][0], o["pos"][2]))
for p in glob.glob(os.path.join(DEV, "test", "spawns", "*_creatures.txt")):
    for ln in open(p):
        ln = ln.split("#")[0].split()
        if len(ln) >= 3:
            pts.append((os.path.basename(p), ln[0], float(ln[1]), float(ln[2])))
by = collections.defaultdict(list)
for f, n, x, z in pts:
    by[f].append((n, x, z))
for f, lst in by.items():
    print(f, len(lst))
    for n, x, z in lst:
        print("   %-50s %8.1f %8.1f" % (n, x, z))
