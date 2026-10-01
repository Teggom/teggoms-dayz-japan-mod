#!/usr/bin/env python3
"""bindet.py - is binarize.exe deterministic? Binarizes the roadside group twice (temp output under spikes/W2/_bin)
and compares each ODOL pair; also compares run 1 with the ODOLs now in src/JP/site/roadside. Writes nothing in src."""
import os
import shutil
import subprocess

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
B = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
OUT = os.path.join(DEV, "spikes", "W2", "_bin")
SRC_MLOD = os.path.join(DEV, "spikes", "B3b", "out", "roadside")
STAGE = "P:\\JP\\site\\_w2tmp"          # = src/JP/site/_w2tmp through the P:\JP junction (removed afterwards)


def run(k):
    o = os.path.join(OUT, "r%d" % k)
    shutil.rmtree(o, ignore_errors=True)
    os.makedirs(o)
    subprocess.run([B, "-always", "-addon=P:\\JP\\site", "-binpath=P:\\bin", STAGE, o, "*.p3d"], cwd="P:\\",
                   capture_output=True, text=True)
    return o


def main():
    stage = os.path.join(DEV, "src", "JP", "site", "_w2tmp")
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage)
    names = sorted(f for f in os.listdir(SRC_MLOD) if f.endswith(".p3d"))[:12]
    for f in names:
        shutil.copyfile(os.path.join(SRC_MLOD, f), os.path.join(stage, f))
    try:
        a, b = run(1), run(2)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    same12 = same_src = 0
    for f in names:
        pa = [os.path.join(r, x) for r, _, fs in os.walk(a) for x in fs if x == f]
        pb = [os.path.join(r, x) for r, _, fs in os.walk(b) for x in fs if x == f]
        if not pa or not pb:
            print("missing", f)
            continue
        x, y = open(pa[0], "rb").read(), open(pb[0], "rb").read()
        s = open(os.path.join(DEV, "src", "JP", "site", "roadside", f), "rb").read()
        same12 += x == y
        same_src += x == s
        print("%-40s run1==run2 %s  run1==src %s" % (f, x == y, x == s))
    print("deterministic %d/%d, equal to src %d/%d" % (same12, len(names), same_src, len(names)))


if __name__ == "__main__":
    main()
