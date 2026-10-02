"""FX3: binarize byte-noise -> HEAD, decided by the MLOD masters instead of a keep-list.

  python spikes/FX3/noise_fx3.py snap            hash every master (buildings/*/out, spikes/*/out) BEFORE the rebuild
  python spikes/FX3/noise_fx3.py restore [--dry] after the rebuild: every modified tracked ODOL under src/JP whose
                                                 master (same stem) is byte-identical to its snapshot is restored to
                                                 HEAD (the model did not change: its new ODOL is only float noise)
A master that changed (its wood UVs / moss / rvmat-carrying faces) keeps its new ODOL. ODOLs without a master are
listed and kept. Never deletes anything; `git checkout -- <file>` only.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
SNAP = os.path.join(HERE, "_build", "master_hashes.json")
GLOBS = ["buildings/*/out/**/*.p3d", "spikes/B3a/out/**/*.p3d", "spikes/B3b/out/**/*.p3d", "spikes/L1/out/**/*.p3d",
         "spikes/L2/out/**/*.p3d", "spikes/S1/out/**/*.p3d", "spikes/W2F/out/**/*.p3d"]


def masters():
    out = {}
    for g in GLOBS:
        for p in glob.glob(os.path.join(DEV, g), recursive=True):
            out.setdefault(os.path.splitext(os.path.basename(p))[0].lower(), []).append(p)
    return out


def h(p):
    return hashlib.sha1(open(p, "rb").read()).hexdigest()


def snap():
    m = masters()
    d = {k: sorted(h(p) for p in v) for k, v in m.items()}
    os.makedirs(os.path.dirname(SNAP), exist_ok=True)
    with open(SNAP, "wb") as f:
        f.write(json.dumps(d).encode("utf-8"))
    print("snapshot: %d master stems" % len(d))


def restore(dry):
    old = json.load(open(SNAP, encoding="utf-8"))
    m = masters()
    r = subprocess.run(["git", "status", "--porcelain", "--", "src/JP"], cwd=DEV, capture_output=True, text=True)
    mod = [l[3:].strip() for l in r.stdout.splitlines() if l.startswith(" M") and l.strip().endswith(".p3d")]
    keep, back, orphan = [], [], []
    for f in mod:
        stem = os.path.splitext(os.path.basename(f))[0].lower()
        if f.startswith("src/JP/parts/"):
            keep.append(f)                    # MLOD part sources: a diff is a real uv change
            continue
        if stem not in m or stem not in old:
            orphan.append(f)
            continue
        now = sorted(h(p) for p in m[stem])
        (back if now == old[stem] else keep).append(f)
    print("modified ODOLs %d: restore %d (master unchanged), keep %d, no master %d" % (len(mod), len(back), len(keep),
                                                                                     len(orphan)))
    for f in orphan[:40]:
        print("  no master:", f)
    if not dry:
        for i in range(0, len(back), 50):
            subprocess.run(["git", "checkout", "--"] + back[i:i + 50], cwd=DEV, check=True)
    return keep


if __name__ == "__main__":
    if sys.argv[1] == "snap":
        snap()
    else:
        restore("--dry" in sys.argv)
