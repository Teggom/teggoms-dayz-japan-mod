"""FP2: which MLOD masters differ from the pre-FP2 masters (rebuilt from af3193e in the scratch copy)? Writes
spikes/FP2/_build/changed.json {pipeline: [p3d stem, ...]}: only their binarized ODOLs are kept after a rebuild; the
rest are restored to HEAD (binarize byte-noise)."""
import filecmp
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
HEAD = sys.argv[1]
out = {}
for x in ("B3a", "B3b", "L1", "L2", "S1"):
    a = os.path.join(DEV, "spikes", x, "out")
    b = os.path.join(HEAD, "spikes", x, "out")
    ch, same, new = [], 0, []
    for root, _, files in os.walk(a):
        for f in files:
            if not f.endswith(".p3d"):
                continue
            pa = os.path.join(root, f)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.isfile(pb):
                new.append(f[:-4])
            elif not filecmp.cmp(pa, pb, shallow=False):
                ch.append(f[:-4])
            else:
                same += 1
    out[x] = sorted(ch + new)
    print(x, "changed", len(ch), "new/unmatched", len(new), "same", same)
with open(os.path.join(HERE, "_build", "changed.json"), "wb") as fh:
    fh.write(json.dumps(out, indent=1).encode("utf-8"))
