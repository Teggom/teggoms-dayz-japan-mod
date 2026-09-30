"""Dump the decorator catalogue (name, area/folder, mount, geo, roadway, bbox size, loot surfaces) to a text file."""
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import decor as DC  # noqa: E402

out = []
for n, e in sorted(DC.catalog().items(), key=lambda kv: (kv[1]["area"], kv[1]["folder"], kv[0])):
    b = e["bbox"]
    loot = ";".join("%s@%.2f(%dp)" % (s["name"], s["y"], len(s["points"])) for s in e["loot"])
    out.append("%s/%s %s mount=%s geo=%d rw=%d size=%.2fx%.2fx%.2f y0=%.2f hang=%s st=%s tiers=%s loot=%s" % (
        e["area"], e["folder"], n, e["mount"], e["geo"], e["roadway"], b[1] - b[0], b[3] - b[2], b[5] - b[4], b[2],
        e.get("hang_y"), e.get("state"), e.get("tiers"), loot))
p = os.path.join(DEV, "spikes", "C3", "_catalog.txt")
with open(p, "wb") as f:
    f.write(("\n".join(out) + "\n").encode("utf-8"))
print(len(out), "entries ->", p)
