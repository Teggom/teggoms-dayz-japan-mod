"""FX4: binarize byte-noise -> HEAD (README rule 3). Binarize rewrites whole folders with float noise, so a diff can't
tell noise from a change. A modified tracked ODOL under the given src folders is KEPT when its MLOD master
  (a) uses an atlased stone texture (jp_m_stone_carved / _carved_aged / _cut: FX4's uv pass remapped it), or
  (b) differs from the pre-FX4 master snapshot (OLD = the scratchpad copy of spikes/<X>/out taken before the rebuild:
      the bells, the gong, the fire-watch tower, the lids / hat / tassel collars FX4 turned outward),
and restored to HEAD otherwise.

  python spikes/FX4/noise.py [--dry] OLD_DIR <src folder> ...
"""
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402

STONE = re.compile(r"\\jp_m_stone_(carved|carved_aged|cut)_w\d_co\.paa$", re.I)
PROP_OUT = ["B3a", "L1", "S1", "W2F", "B3b", "L2"]


def masters_by_stem():
    idx = {}
    for x in PROP_OUT:
        for p in glob.glob(os.path.join(DEV, "spikes", x, "out", "**", "*.p3d"), recursive=True):
            idx.setdefault(os.path.basename(p).lower(), []).append(("prop", x, p))
    for p in glob.glob(os.path.join(DEV, "buildings", "**", "out", "*.p3d"), recursive=True):
        idx.setdefault(os.path.basename(p).lower(), []).append(("bldg", None, p))
    for p in glob.glob(os.path.join(DEV, "parts", "**", "out", "**", "*.p3d"), recursive=True):
        idx.setdefault(os.path.basename(p).lower(), []).append(("part", None, p))
    return idx


def uses_stone(p):
    try:
        for l in mlod.read_mlod(p):
            for f in l.faces:
                if STONE.search(f[2] or ""):
                    return True
    except Exception as e:  # noqa: BLE001
        print("  unreadable master %s: %s (kept)" % (p, e))
        return True
    return False


def main(argv):
    dry = "--dry" in argv
    args = [a for a in argv if not a.startswith("--")]
    old, dirs = args[0], args[1:]
    out = subprocess.run(["git", "status", "--porcelain", "--"] + dirs, capture_output=True, text=True,
                         cwd=DEV).stdout
    idx = masters_by_stem()
    keep, noise, why = [], [], {}
    for ln in out.splitlines():
        if not ln.startswith(" M") or not ln.endswith(".p3d"):
            continue
        rel = ln[3:].strip()
        stem = os.path.basename(rel).lower()
        cands = idx.get(stem, [])
        k = None
        for kind, x, mp in cands:
            if uses_stone(mp):
                k = "stone"
                break
            if kind == "prop":
                op = os.path.join(old, x, os.path.relpath(mp, os.path.join(DEV, "spikes", x, "out")))
                if not os.path.isfile(op) or open(op, "rb").read() != open(mp, "rb").read():
                    k = "master changed"
                    break
        if not cands:
            k = "no master found (kept)"
        (keep if k else noise).append(rel)
        if k:
            why[rel] = k
    print("modified ODOLs: %d keep, %d noise -> HEAD%s" % (len(keep), len(noise), " (dry)" if dry else ""))
    for r in keep:
        if why[r] != "stone":
            print("  keep %s (%s)" % (r, why[r]))
    nst = sum(1 for r in keep if why[r] == "stone")
    print("  keep %d stone-atlas models" % nst)
    if noise and not dry:
        for i in range(0, len(noise), 100):
            subprocess.run(["git", "checkout", "--"] + noise[i:i + 100], cwd=DEV, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
