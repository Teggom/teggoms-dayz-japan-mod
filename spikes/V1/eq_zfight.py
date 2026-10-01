"""V1: zfight.coplanar old (per-face 81-cell loop) vs fast (cached candidate lists + numpy pre-filter) on built models:
the result dicts must be identical (same records, same order). Also times zfight.resolve old vs fast on a fresh model
and checks the resolved solids are identical.  python spikes/V1/eq_zfight.py <key> [...]"""
import builtins
import os
import sys
import time

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
_print = builtins.print


def raw_model(b):
    import pipeline as P
    mod = P.load_module(b)
    if "params" in b:
        return mod.model(name=b.get("recipe_name", b["name"]), **b["params"])[0]
    return mod.model()[0]


def solids_sig(M):
    return [(tuple(map(tuple, s.verts)), s.vis and tuple(sorted(s.vis)), s.geo, s.view, s.fire) for s in M.solids]


def run(key):
    import registry
    from jpparts import zfight as ZF
    b = registry.get(key)
    builtins.print = lambda *a, **k: None
    out, tm, sig = {}, {}, {}
    for eng in (False, True):
        ZF.FAST = eng
        M = raw_model(b)
        t0 = time.perf_counter()
        ZF.resolve(M)
        t1 = time.perf_counter()
        r = ZF.coplanar(M)
        t2 = time.perf_counter()
        out[eng], tm[eng], sig[eng] = r, (t1 - t0, t2 - t1), solids_sig(M)
    builtins.print = _print
    same = out[False] == out[True]
    same_m = sig[False] == sig[True]
    print("%-40s coplanar %s (same %d, opposite %d, hidden %d) %.2f->%.2f s | resolve %s %.2f->%.2f s" % (
        key, "SAME" if same else "DIFF", len(out[True]["same"]), len(out[True]["opposite"]),
        len(out[True]["hidden"]), tm[False][1], tm[True][1], "SAME" if same_m else "DIFF", tm[False][0],
        tm[True][0]), flush=True)
    return same and same_m


if __name__ == "__main__":
    keys = sys.argv[1:]
    ok = True
    for k in keys:
        ok = run(k) and ok
    sys.exit(0 if ok else 1)
