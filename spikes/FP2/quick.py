"""FP2 quick build: write the MLOD masters + checks of selected props only (no config.cpp, no binarize, no pack).
  python spikes/FP2/quick.py b3b jp_s_firewood_stack [...]
  python spikes/FP2/quick.py b3a jp_f_firewood [...]
  python spikes/FP2/quick.py l1 jp_f_usu [...]      (L1 via build_l1's module redirection)
The full builds (config, binarize, pack) are run at the end with each pipeline's own build script."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))


def load(path, name):
    d = os.path.dirname(path)
    for p in (d,):
        if p not in sys.path:
            sys.path.insert(0, p)
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    sp.loader.exec_module(m)
    return m


if __name__ == "__main__":
    which, names = sys.argv[1], sys.argv[2:]
    path = {"b3b": "spikes/B3b/build.py", "b3a": "spikes/B3a/build.py", "l1": "spikes/L1/build_l1.py",
            "l2": "spikes/L2/build_l2.py", "s1": "spikes/S1/build_s1.py"}[which]
    B = load(os.path.join(DEV, path), "fp2_build_" + which)
    if hasattr(B, "setup"):
        B.setup()
    core = B.B if hasattr(B, "B") and not hasattr(B, "registry") else B     # L1/L2/S1 wrap a base build module
    reg = core.registry()
    if which == "l1":
        reg = B.l1_props(reg)
    sel = core.select(reg, names)
    B.write_all(sel)
