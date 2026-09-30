"""C1: raycheck.cast (staged, culled) must give the same nearest hits as the original all-pairs cast."""
import os
import sys
import time

import numpy as np

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod, raycheck as RC  # noqa: E402

p = os.path.join(DEV, "buildings", "machiya_t3_01", "out", "jp_machiya_t3_01.p3d")
L = {mlod.lod_name(l.resolution): l for l in mlod.read_mlod(p)}
T = RC.lod_triangles(L["Resolution 1"])
rng = np.random.default_rng(1)
O = np.concatenate([rng.uniform((-6, 0.3, -7), (6, 5, 7), (1500, 3)), np.repeat([[0.0, 1.5, -2.0]], 320, 0)])
D = np.concatenate([rng.normal(size=(1500, 3)), RC.fib_dirs(320)])
D /= np.linalg.norm(D, axis=1)[:, None]
for tm in (60.0, 3.0):
    t0 = time.time()
    a = RC._cast_brute(T, O, D, tm)
    t1 = time.time()
    b = RC.cast(T, O, D, tm)
    t2 = time.time()
    same = np.array_equal(np.isinf(a), np.isinf(b)) and np.allclose(a[np.isfinite(a)], b[np.isfinite(b)], atol=1e-9)
    print("tmax %g: brute %.1f s, staged %.1f s, identical %s, max diff %.2e, escaped %d" % (
        tm, t1 - t0, t2 - t1, same, float(np.nanmax(np.abs(np.where(np.isfinite(a), a - b, 0)))), int(np.isinf(a).sum())))
# vertical columns (C15)
xs, zs = np.arange(-6, 6, 0.12), np.arange(-7, 7, 0.12)
O = np.array([(x, 30.0, z) for x in xs for z in zs])
Dn = np.tile([[0.0, -1.0, 0.0]], (len(O), 1))
t0 = time.time()
a = RC._cast_brute(T, O, Dn, 40.0, chunk=64)
t1 = time.time()
b = RC.cast(T, O, Dn, 40.0, chunk=64)
t2 = time.time()
print("columns: brute %.1f s, staged %.1f s, identical %s" % (t1 - t0, t2 - t1, np.array_equal(a, b)))
