"""probe: python spikes/FB2/probe.py <key> <tagA> [tagB] [tol]: nearest parallel-plane distances between tagA faces and other faces"""
import sys, os, math
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import registry, pipeline as P
from jpparts import zfight as Z
key, ta = sys.argv[1], sys.argv[2]
tb = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
tol = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
b = registry.get(key)
mod = P.load_module(b)
M = mod.model(name=b.get("recipe_name", b.get("name")), **b["params"])[0] if "params" in b else mod.model()[0]
for s in M.solids:
    s.finalize()
A = [s for s in M.solids if s.tag == ta and 1 in s.vis]
print(len(A), "solids tagged", ta)
out = {}
for a in A:
    for fi, f in enumerate(a.faces):
        n = a.fn[fi]
        d = Z._dot(n, a.verts[f[0]])
        bb = a.bbox()
        for s in M.solids:
            if s is a or 1 not in s.vis or (tb and s.tag != tb):
                continue
            sb = s.bbox()
            if sb[0] > bb[1] + tol or sb[1] < bb[0] - tol or sb[2] > bb[3] + tol or sb[3] < bb[2] - tol or sb[4] > bb[5] + tol or sb[5] < bb[4] - tol:
                continue
            for fj, g in enumerate(s.faces):
                m = s.fn[fj]
                c = Z._dot(n, m)
                if abs(c) < 0.999:
                    continue
                dist = max(abs(Z._dot(n, s.verts[i]) - d) for i in g)
                if dist < tol:
                    k = (s.tag, round(dist, 4), "same" if c > 0 else "opp", s.fm[fj], a.fm[fi])
                    out[k] = out.get(k, 0) + 1
for k, v in sorted(out.items(), key=lambda kv: kv[0][1]):
    print(v, k)
