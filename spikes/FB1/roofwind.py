"""FB1 (E): what the sky sees of a building MLOD. For a grid of vertical rays from above, the HIGHEST face hit in each
visual LOD and whether it faces up (p3d formula normals point INWARD, jpparts/mlod.py: a face seen from above has
formula normal y < 0). A 'down' top face is culled by the engine: the roof looks missing from above / outside.
  python spikes/FB1/roofwind.py <mlod.p3d> [step_m]
"""
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402


def inside(px, pz, poly):
    c = False
    n = len(poly)
    for i in range(n):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % n]
        if (z1 > pz) != (z2 > pz):
            if px < x1 + (pz - z1) * (x2 - x1) / (z2 - z1):
                c = not c
    return c


def census(path, step=0.5):
    out = {}
    for l in mlod.read_mlod(path):
        name = mlod.lod_name(l.resolution)
        if not name.startswith("Resolution"):
            continue
        fs = []
        xs, zs = [], []
        for verts, _, tex, mat in l.faces:
            pts = [l.points[v[0]] for v in verts]
            n = mlod._normalize(mlod._face_formula_normal(pts))
            if abs(n[1]) < 1e-3:
                continue
            d = mlod._dot(n, pts[0])
            fs.append((pts, n, d, os.path.basename(mat or tex),
                       (min(p[0] for p in pts), max(p[0] for p in pts), min(p[2] for p in pts), max(p[2] for p in pts))))
            xs += [p[0] for p in pts]
            zs += [p[2] for p in pts]
        x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
        stats = {}
        bad = []
        x = x0 + step / 2
        while x < x1:
            z = z0 + step / 2
            while z < z1:
                best = None
                for pts, n, d, m, bb in fs:
                    if not (bb[0] <= x <= bb[1] and bb[2] <= z <= bb[3]):
                        continue
                    if not inside(x, z, [(p[0], p[2]) for p in pts]):
                        continue
                    y = (d - n[0] * x - n[2] * z) / n[1]
                    if best is None or y > best[0]:
                        best = (y, n, m)
                if best:
                    s = stats.setdefault(best[2], [0, 0])
                    up = best[1][1] < 0
                    s[0 if up else 1] += 1
                    if not up:
                        bad.append((round(x, 2), round(best[0], 2), round(z, 2), best[2]))
                z += step
            x += step
        out[name] = (stats, bad)
    return out


def main(path, step=0.5):
    for name, (stats, bad) in census(path, step).items():
        print(name)
        for k, (up, down) in sorted(stats.items()):
            print("   %-40s top faces up %5d  DOWN %5d" % (k, up, down))
        if bad:
            print("   first DOWN samples (x, y, z, material):", bad[:6])


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.5)
