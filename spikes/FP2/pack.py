"""FP2: repack a PBO from the (noise-restored) source tree without rebuilding anything.
  python spikes/FP2/pack.py furniture|site      -> @Japan/addons/jp_furniture.pbo | jp_site.pbo
Uses the pipelines' own pack() (B3a build.py / B3b build.py); never starts or stops anything. A locked PBO (a running
server) is reported, not forced."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))


def load(pipe):
    d = os.path.join(DEV, "spikes", pipe)
    sys.path.insert(0, d)
    sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
    sp = importlib.util.spec_from_file_location("build_" + pipe, os.path.join(d, "build.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


if __name__ == "__main__":
    which = sys.argv[1]
    B = load({"furniture": "B3a", "site": "B3b"}[which])
    ok, det = B.pack()
    print("packed:", ok, det)
    sys.exit(0 if ok else 1)
