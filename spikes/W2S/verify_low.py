"""W2S: pipeline --verify-only over keys in at most 4 processes at BELOW_NORMAL priority (README rule 2b).
  python spikes/W2S/verify_low.py k1 k2 ..."""
import os, subprocess, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
keys = sys.argv[1:]
n = min(4, len(keys))
procs = []
for i in range(n):
    g = keys[i::n]
    lf = open(os.path.join(DEV, "spikes", "W2S", "_vlow_%d.log" % i), "wb")
    procs.append((subprocess.Popen([sys.executable, os.path.join(DEV, "buildings", "pipeline.py"), "--verify-only"] + g,
                                   stdout=lf, stderr=subprocess.STDOUT, cwd=DEV, creationflags=0x4000), lf))
rc = 0
for p, lf in procs:
    rc |= p.wait()
    lf.close()
print("exit", rc)
