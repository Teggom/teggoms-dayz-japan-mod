"""FX5 gradesweep: find visible up-facing faces lying AT grade (z-fight with the terrain) in built ODOLs.

For every ODOL p3d under the given folders (default: the compound / corridor site folders), every Resolution LOD
(< 1e4) face whose normal points up (ny > 0.9) and whose vertices all lie within [-0.015, +0.025] m of the model's
design grade (MLOD y 0 = ODOL y -bc) is summed per model. Faces between +0.025 and +0.045 are listed as 'near'.

  python spikes/FX5/gradesweep.py [folder ...] [--min 0.05]
"""
import os
import sys

import numpy as np

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "tools", "placecheck"))
import odol_read  # noqa: E402

DEFAULT = ["src/JP/buildings/dw_site", "src/JP/buildings/tr_site"]


def sweep(path):
    info = odol_read.read_odol(path)
    g = -float(info["boundingCenter"][1])
    out = {}
    for lod in info["lods"]:
        r = lod.resolution
        if r >= 1e4 or not lod.vertices:
            continue
        V = np.array(lod.vertices, np.float64)
        at = near = 0.0
        for f in lod.faces:
            P = V[list(f)]
            if len(P) < 3:
                continue
            n = np.cross(P[1] - P[0], P[2] - P[0])
            a = np.linalg.norm(n)
            if a < 1e-9:
                continue
            n = n / a
            area = 0.5 * a if len(P) == 3 else 0.5 * np.linalg.norm(np.cross(P[2] - P[0], P[3] - P[1]))
            if abs(n[1]) < 0.9:
                continue
            dy = P[:, 1] - g
            if dy.min() >= -0.015 and dy.max() <= 0.025:
                at += area
            elif dy.min() >= -0.015 and dy.max() <= 0.045:
                near += area
        out[r] = (at, near)
    return out


def main(argv):
    mn = float(argv[argv.index("--min") + 1]) if "--min" in argv else 0.05
    dirs = [a for a in argv if not a.startswith("--") and not a.replace(".", "").isdigit()] or DEFAULT
    bad = 0
    for d in dirs:
        full = os.path.join(DEV, d)
        for dp, _, fs in os.walk(full):
            for f in sorted(fs):
                if not f.endswith(".p3d"):
                    continue
                p = os.path.join(dp, f)
                try:
                    res = sweep(p)
                except Exception as ex:  # noqa: BLE001
                    print("%-60s unreadable: %s" % (os.path.relpath(p, DEV), ex))
                    continue
                r1 = res.get(min(res)) if res else (0, 0)
                if r1 and (r1[0] >= mn or r1[1] >= mn):
                    bad += 1
                    print("%-60s R1 at-grade %.2f m2, near-grade %.2f m2" % (os.path.relpath(p, DEV), r1[0], r1[1]))
    print("models with >= %.2f m2 at / near grade: %d" % (mn, bad))
    return bad


if __name__ == "__main__":
    main(sys.argv[1:])
