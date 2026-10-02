"""CR counts of files vs HEAD (README rule 5).  python spikes/FX6/crlf.py <path ...>"""
import subprocess
import sys

for p in sys.argv[1:]:
    now = open(p, "rb").read().count(b"\r")
    r = subprocess.run(["git", "show", "HEAD:" + p.replace("\\", "/")], capture_output=True)
    head = r.stdout.count(b"\r") if r.returncode == 0 else "new"
    print("%-60s now %s  HEAD %s" % (p, now, head))
