"""V1: profile_one.py over several keys, at most 4 processes (README 2b).
  python spikes/V1/run_profiles.py <tag> <old|new> key ...   -> spikes/V1/prof/<tag>/<key>.json"""
import os
import subprocess
import sys
import time

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
tag, eng, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
env = dict(os.environ)
if eng == "old":
    env["JP_RAY_ENGINE"] = "brute"
    env["JP_ZFIGHT_ENGINE"] = "old"
out = os.path.join(DEV, "spikes", "V1", "prof", tag)
os.makedirs(out, exist_ok=True)
env["V1_PROF_OUT"] = out
todo = list(keys)
running = []
t0 = time.time()
while todo or running:
    while todo and len(running) < 4:
        k = todo.pop(0)
        lf = open(os.path.join(out, k + ".log"), "wb")
        running.append((subprocess.Popen([sys.executable, os.path.join(DEV, "spikes", "V1", "profile_one.py"), k],
                                         stdout=lf, stderr=subprocess.STDOUT, cwd=DEV, env=env), lf, k))
    time.sleep(0.5)
    for r in list(running):
        if r[0].poll() is not None:
            r[1].close()
            running.remove(r)
print("done %d keys in %.0f s" % (len(keys), time.time() - t0))
