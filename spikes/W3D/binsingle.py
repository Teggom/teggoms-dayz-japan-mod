"""Binarize a few W3D prop masters alone (FX1's workaround: binarize.exe crashes on an EXISTING ODOL in a folder run).

  python spikes/W3D/binsingle.py jp_f_kamaba ...

Copies the masters (spikes/W3D/out/govfit/<p3d>.p3d) into a temp folder under src/JP/furniture/_w3d_tmp, binarizes
that folder (cwd P:\\), copies each ODOL into src/JP/furniture/govfit/, removes the temp folder.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
SRC = os.path.join(DEV, "src", "JP", "furniture")
TMP = os.path.join(SRC, "_w3d_tmp")


def main(names):
    shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP)
    out = os.path.join(HERE, "_build", "binsingle")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    for n in names:
        shutil.copyfile(os.path.join(HERE, "out", "govfit", n + ".p3d"), os.path.join(TMP, n + ".p3d"))
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\furniture", "-binpath=P:\\bin", "P:\\JP\\furniture\\_w3d_tmp", out,
           "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    ok = 0
    for n in names:
        f = os.path.join(out, n + ".p3d")
        if os.path.isfile(f) and open(f, "rb").read(4) == b"ODOL":
            shutil.copyfile(f, os.path.join(SRC, "govfit", n + ".p3d"))
            ok += 1
        else:
            print("MISSING", n)
    shutil.rmtree(TMP, ignore_errors=True)
    print("binsingle: %d/%d ODOL (exit %d)" % (ok, len(names), r.returncode))
    return 0 if ok == len(names) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
