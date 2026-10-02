"""Props used by a wave: the proxies of its furnished MLODs + the p3ds of its placements CSV.
  python spikes/FX6/used_props.py <furnished out dir> <placements csv> [propfloat report]
With a report, prints the report's FAIL blocks for the used props only."""
import glob
import os
import re
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod, proxies as PX  # noqa: E402


def used(outdir, csv):
    u = set()
    for p in glob.glob(os.path.join(outdir, "*.p3d")):
        l = next(l for l in mlod.read_mlod(p) if mlod.lod_name(l.resolution) == "Resolution 1")
        for name, o, up, f in PX.listed(l):
            u.add(re.split(r"[\\/]", name.split(":", 1)[1].rsplit(".", 1)[0])[-1].lower())
    if csv and os.path.exists(csv):
        for line in open(csv, encoding="utf-8"):
            m = re.search(r"(jp_[a-z0-9_]+)\.p3d", line)
            if m:
                u.add(m.group(1))
    return u


if __name__ == "__main__":
    u = used(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    if len(sys.argv) > 3:
        cur = None
        for ln in open(sys.argv[3], encoding="utf-8").read().split("\n"):
            if ln.startswith("  FAIL"):
                cur = ln.split()[1]
                if cur in u:
                    print(ln)
            elif cur in u and ln.startswith("         "):
                print(ln)
    print("%d props used" % len(u))
