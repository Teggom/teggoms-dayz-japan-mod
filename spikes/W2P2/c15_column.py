import sys
sys.path.insert(0, "parts/kit")
import w2p2_assembly as A
fn = getattr(A, sys.argv[1])
a, ctx = fn()
x, z = float(sys.argv[2]), float(sys.argv[3])
def tri_hit(p0, p1, p2):
    # vertical ray at (x,z): barycentric in xz
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = p0, p1, p2
    den = (z1 - z2) * (x0 - x2) + (x2 - x1) * (z0 - z2)
    if abs(den) < 1e-12: return None
    l0 = ((z1 - z2) * (x - x2) + (x2 - x1) * (z - z2)) / den
    l1 = ((z2 - z0) * (x - x2) + (x0 - x2) * (z - z2)) / den
    l2 = 1 - l0 - l1
    if min(l0, l1, l2) < -1e-6: return None
    return l0 * y0 + l1 * y1 + l2 * y2
for k in (1, 2, 3):
    hits = []
    for s in a.solids:
        if k not in s.vis: continue
        best = None
        for f in s.faces:
            pts = [s.verts[i] for i in f]
            for i in range(1, len(pts) - 1):
                h = tri_hit(pts[0], pts[i], pts[i + 1])
                if h is not None and (best is None or h > best): best = h
        if best is not None: hits.append((round(best, 3), s.tag))
    hits.sort(reverse=True)
    print(k, hits[:5])
