"""V1: copy every shipped building's checks file to data/V1/eq/<tag>/<key>.json (tag HEAD: from git HEAD).
  python spikes/V1/snap_checks.py <tag>"""
import os, subprocess, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path[:0] = [os.path.join(DEV, p) for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit")]
import registry, pipeline as P
tag = sys.argv[1]
out = os.path.join(DEV, "data", "V1", "eq", tag)
os.makedirs(out, exist_ok=True)
n = 0
for b in registry.BUILDINGS:
    if not b["ship"]:
        continue
    p = P.checks_file(b)
    if tag == "HEAD":
        rel = os.path.relpath(p, DEV).replace("\\", "/")
        data = subprocess.run(["git", "show", "HEAD:" + rel], cwd=DEV, capture_output=True).stdout
    else:
        data = open(p, "rb").read() if os.path.isfile(p) else b""
    with open(os.path.join(out, b["key"] + ".json"), "wb") as f:
        f.write(data)
    n += 1
print("snapshot", tag, n)
