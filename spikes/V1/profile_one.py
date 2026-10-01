"""V1 profiler: one building, timed per phase (model generation steps, each check) without touching src.

  python spikes/V1/profile_one.py <key> [--cprofile]   -> spikes/V1/prof/<key>.json (+ <key>.pstats.txt)

Runs pipeline.build_model(b, stage=False) + pipeline.run_verify (exactly what --verify-only does). Check timings: the
time between consecutive OK/FAIL lines is charged to the check printed (the work precedes its rec()).
"""
import builtins
import json
import os
import sys
import time

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
OUT = os.environ.get("V1_PROF_OUT") or os.path.join(DEV, "spikes", "V1", "prof")

T = {"phases": [], "checks": []}
_mark = [time.perf_counter()]


def phase(name, fn):
    def w(*a, **k):
        t0 = time.perf_counter()
        r = fn(*a, **k)
        T["phases"].append((name, round(time.perf_counter() - t0, 3)))
        return r
    return w


_real_print = builtins.print


def tprint(*a, **k):
    s = " ".join(str(x) for x in a)
    if s[:4] in ("OK  ", "FAIL"):
        now = time.perf_counter()
        T["checks"].append((s[5:57].strip(), round(now - _mark[0], 3), s[:4].strip()))
        _mark[0] = now
    _real_print(*a, **k)


def main():
    key = sys.argv[1]
    prof = "--cprofile" in sys.argv
    import pipeline as P
    import registry
    from jpparts import zfight as ZF, core, mlod
    b = registry.get(key)
    ZF.resolve = phase("zfight.resolve", ZF.resolve)
    core.Part.lods = phase("Part.lods", core.Part.lods)
    mlod.write_mlod = phase("write_mlod", mlod.write_mlod)
    real_load = P.load_module

    def load(bb):
        m = real_load(bb)
        if not getattr(m, "_v1_wrapped", False) and hasattr(m, "model"):
            m.model = phase("recipe model()", m.model)
            try:
                m._v1_wrapped = True
            except Exception:
                pass
        return m
    P.load_module = load
    builtins.print = tprint
    pr = None
    if prof:
        import cProfile
        pr = cProfile.Profile()
        pr.enable()
    t0 = time.perf_counter()
    bd = P.build_model(b, stage=False)
    t1 = time.perf_counter()
    _mark[0] = t1
    ok = P.run_verify(bd)
    t2 = time.perf_counter()
    if pr:
        pr.disable()
    builtins.print = _real_print
    os.makedirs(OUT, exist_ok=True)
    res = {"key": key, "ok": ok, "build_s": round(t1 - t0, 3), "verify_s": round(t2 - t1, 3),
           "phases": T["phases"], "checks": sorted(T["checks"], key=lambda x: -x[1]), "n_checks": len(T["checks"])}
    with open(os.path.join(OUT, key + (".cprof" if prof else "") + ".json"), "wb") as f:
        f.write(json.dumps(res, indent=1).encode("utf-8"))
    if pr:
        import io
        import pstats
        s = io.StringIO()
        pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(60)
        s2 = io.StringIO()
        pstats.Stats(pr, stream=s2).sort_stats("tottime").print_stats(40)
        with open(os.path.join(OUT, key + ".pstats.txt"), "wb") as f:
            f.write((s.getvalue() + "\n\n" + s2.getvalue()).encode("utf-8"))
    _real_print("PROFILE %s: build %.1f s, verify %.1f s, %d checks, %s" % (key, t1 - t0, t2 - t1, len(T["checks"]),
                                                                         "PASS" if ok else "FAIL"))


if __name__ == "__main__":
    main()
