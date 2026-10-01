"""V1: ray engines brute vs fast on one building, ray by ray: C11 envelope_leak (whole result), C17 jamb_slits per door,
C15 column heights (max abs diff, bitwise-equal count). Times both.  python spikes/V1/eq_rays.py <key> [...]"""
import os
import sys
import time

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import numpy as np  # noqa: E402
import builtins  # noqa: E402

_print = builtins.print


def run(key):
    import pipeline as P
    import registry
    from jpparts import mlod, raycheck as RC, checks as C
    builtins.print = lambda *a, **k: None
    bd = P.build_model(registry.get(key), stage=False)
    builtins.print = _print
    lods = mlod.read_mlod(bd["mlod"])
    if hasattr(bd["mod"], "proxies") and getattr(bd["mod"], "D", None) is not None:
        from jpparts import proxies as PX
        lods = [PX.strip(l) for l in lods]
    L = {mlod.lod_name(l.resolution): l for l in lods}
    M, floors = bd["M"], bd["floors"]
    rooms = [{"name": f["name"], "rect": f["rect"], "y": f["y"], "obstacles": f.get("obstacles", [])} for f in floors
             if f.get("enclosed", True)]
    vcomps = C.components(L["View Geometry"])
    portals = [("all_doors", (-99, 99, -99, 99, -99, 99))][:0]
    T1 = RC.lod_triangles(L["Resolution 1"])
    out = {}
    tm = {}
    rays17 = {}
    for eng in ("brute", "fast"):
        RC.ENGINE = eng
        t0 = time.perf_counter()
        r11 = RC.envelope_leak(L["Resolution 1"], rooms, portals)
        t1 = time.perf_counter()
        cap = []
        oc, oe = RC.cast, RC.escapes

        def cc(T_, O_, D_, tmax=60.0, chunk=24):
            cap.append((O_.copy(), D_.copy()))
            return oc(T_, O_, D_, tmax, chunk)

        def ce(T_, O_, D_, tmax=60.0):
            cap.append((O_.copy(), D_.copy()))
            return oe(T_, O_, D_, tmax)
        RC.cast, RC.escapes = cc, ce
        r17 = [RC.jamb_slits(d, vcomps, T1) for d in M.doors if d.kind != "lattice"]
        RC.cast, RC.escapes = oc, oe
        rays17[eng] = cap
        t2 = time.perf_counter()
        x0, x1, _, _, z0, z1 = M.bbox()
        xs = np.arange(x0 + 0.05, x1, 0.12)
        zs = np.arange(z0 + 0.05, z1, 0.12)
        O = np.array([(x, 30.0, z) for x in xs for z in zs])
        r15 = []
        for ln in ("Resolution 1", "Resolution 2", "Resolution 3"):
            tri = RC.lod_triangles(L[ln])
            for dx, dz in ((0.0, 0.0), (0.01, 0.0), (-0.01, 0.0), (0.0, 0.01), (0.0, -0.01)):
                r15.append(RC.cast_down(tri, O + np.array([dx, 0.0, dz]), 40.0))
        t3 = time.perf_counter()
        out[eng] = (r11, r17, r15)
        tm[eng] = (t1 - t0, t2 - t1, t3 - t2)
    a, b = out["brute"], out["fast"]
    rb, rf = rays17["brute"], rays17["fast"]
    rays_same = len(rb) == len(rf) and all(x[0].shape == y[0].shape and np.array_equal(x[0], y[0]) and
                                           np.array_equal(x[1], y[1]) for x, y in zip(rb, rf))
    same11 = a[0] == b[0]
    same17 = a[1] == b[1]
    d15 = max(float(np.max(np.where(np.isfinite(x) | np.isfinite(y), np.abs(np.nan_to_num(x, posinf=1e9) -
                                                                         np.nan_to_num(y, posinf=1e9)), 0.0)))
              for x, y in zip(a[2], b[2]))
    bit15 = sum(int(np.sum(x.view(np.int64) != y.view(np.int64))) for x, y in zip(a[2], b[2]))
    n11 = sum(v[0] for v in a[0].values())
    n17 = sum(v[0] for v in a[1])
    print("%-40s C11 %s (%d rays, leaks %d) %.1f->%.1f s | C17 %s rays-bitwise %s (%d rays, slits %d) %.1f->%.1f s | C15 maxdiff %.3g, "
          "%d non-bitwise of %d %.1f->%.1f s" % (
              key, "SAME" if same11 else "DIFF", n11, sum(len(v[2]) for v in a[0].values()), tm["brute"][0],
              tm["fast"][0], "SAME" if same17 else "DIFF", rays_same, n17, sum(len(v[1]) for v in a[1]), tm["brute"][1],
              tm["fast"][1], d15, bit15, sum(len(x) for x in a[2]), tm["brute"][2], tm["fast"][2]), flush=True)
    return same11 and same17 and rays_same and d15 == 0.0


if __name__ == "__main__":
    ok = True
    for k in sys.argv[1:]:
        ok = run(k) and ok
    sys.exit(0 if ok else 1)
