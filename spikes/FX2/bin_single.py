"""FX2: binarize prop masters one at a time (the W2F folder binarize crashes with an access violation on an existing
ODOL in sacred / civicfit: PRODUCTION_PLAN FX1 pitfall). For each master: copy it alone into a temporary folder
under the area (so the area's model.cfg applies), binarize that folder, copy the ODOL into src/JP/<area>/<cat>/,
remove the temporary folders.

  python spikes/FX2/bin_single.py <area> <cat>/<p3d stem> ...      e.g. furniture sacred/jp_f_waniguchi
Masters are read from spikes/W2F/out/<cat>/ (furniture) or spikes/B3b/out/<cat>/ (site).
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
OUTS = {"furniture": os.path.join(DEV, "spikes", "W2F", "out"), "site": os.path.join(DEV, "spikes", "B3b", "out")}


def main(argv):
    area = argv[0]
    src = os.path.join(DEV, "src", "JP", area)
    ok = True
    for spec in argv[1:]:
        cat, stem = spec.split("/")
        tmp = os.path.join(src, "_fx2bin")
        out = os.path.join(DEV, "spikes", "FX2", "_build", "bin_out")
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(tmp)
        os.makedirs(out)
        shutil.copyfile(os.path.join(OUTS[area], cat, stem + ".p3d"), os.path.join(tmp, stem + ".p3d"))
        cmd = [BINARIZE, "-always", "-addon=P:\\JP\\" + area, "-binpath=P:\\bin", "P:\\JP\\%s\\_fx2bin" % area, out,
               "*.p3d"]
        r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
        f = os.path.join(out, stem + ".p3d")
        if os.path.isfile(f) and open(f, "rb").read(4) == b"ODOL":
            shutil.copyfile(f, os.path.join(src, cat, stem + ".p3d"))
            print("ODOL", cat, stem, os.path.getsize(f))
        else:
            ok = False
            print("FAILED", cat, stem, r.returncode, (r.stdout + r.stderr)[-600:])
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(out, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
