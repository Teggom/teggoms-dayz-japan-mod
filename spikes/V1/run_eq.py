"""V1: run an equivalence script (eq_zfight.py / eq_rays.py) over keys in at most 4 processes.
  python spikes/V1/run_eq.py <script> <tag> [key ...]   (no keys = every shipped building) -> spikes/V1/_<tag>_<i>.log"""
import os, subprocess, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
import registry
script, tag, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
keys = keys or [b["key"] for b in registry.BUILDINGS if b["ship"]]
procs = []
for i in range(4):
    g = keys[i::4]
    if g:
        lf = open(os.path.join(DEV, "spikes", "V1", "_%s_%d.log" % (tag, i)), "wb")
        procs.append((subprocess.Popen([sys.executable, os.path.join(DEV, "spikes", "V1", script)] + g, stdout=lf,
                                       stderr=subprocess.STDOUT, cwd=DEV), lf))
rc = 0
for p, lf in procs:
    rc |= p.wait()
    lf.close()
print("exit", rc)
