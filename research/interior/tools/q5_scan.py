"""Q5 step 1: find vanilla building ODOLs that reference furniture proxies (plain strings in the file).

Run: python research/interior/tools/q5_scan.py  -> prints path, size, count of furniture proxy names.
Read-only on P:\\DZ. Research agent A-INT, 2026-09-29.
"""
import os, re, sys

ROOTS = [r"P:\DZ\structures\residential", r"P:\DZ\structures\specific", r"P:\DZ\structures\industrial",
         r"P:\DZ\structures\military"]
PAT = re.compile(rb"dz\\structures\\furniture\\[a-z0-9_\\]+", re.I)

rows = []
for root in ROOTS:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.lower().endswith(".p3d"):
                continue
            p = os.path.join(dp, f)
            sz = os.path.getsize(p)
            if sz > 60_000_000:
                continue
            d = open(p, "rb").read()
            if d[:4] != b"ODOL":
                continue
            hits = PAT.findall(d)
            if hits:
                rows.append((len(hits), len(set(h.lower() for h in hits)), sz, p))
rows.sort(reverse=True)
for r in rows[:int(sys.argv[1]) if len(sys.argv) > 1 else 60]:
    print("%5d %4d %10d %s" % r)
print("files with furniture proxies:", len(rows))
