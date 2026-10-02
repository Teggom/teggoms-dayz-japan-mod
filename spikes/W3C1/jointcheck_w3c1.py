"""W3C1 copy of spikes/FX5/jointcheck.py (the wave-3c-1 yards only: brewery, dyersyard, paperyard; out: spikes/W3C1/jointcheck.json).
FX5 jointcheck: measure wall-line joints in the BUILT (binarized) objects as placed on the island.

For each joint (a point on a compound's wall line where two materials / objects meet) every placed object within
15 m is read from its ODOL (src/JP/...), placed with its test/placements row (world = origin + R(yaw) * mlod), and
its Geometry, View Geometry and Resolution 1 LODs are sliced at 0.3 / 1.0 / 1.6 m above the compound's grade.
The slices are rasterised (2 cm) in a 4 x 4 m window round the joint; a flood fill from a point 1.5 m INSIDE the
compound must not reach a point 1.5 m OUTSIDE. If it does, the joint leaks: the narrowest opening is found by
dilating the blocked cells until the two points separate (gap ~ 2 x radius).

  python spikes/FX5/jointcheck.py            # all joints, table + spikes/FX5/jointcheck.json
"""
import json
import math
import os
import sys

import numpy as np

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "tools", "placecheck"))
import odol_read  # noqa: E402
from sources import read_placement_rows, read_8wvr, WRP  # noqa: E402
from grounding import Terrain, yaw_matrix  # noqa: E402
from model import p3d_file  # noqa: E402

KEN = 1.82
LODS = {"geo": 1e13, "view": 6e15, "res1": 1.0}
CELL = 0.02
HALF_WIN = 2.0
PNG = "--png" in sys.argv

# joints: (label, compound p3d (basename), kit node (x, z), unit vector pointing INTO the compound (kit frame),
#          what meets there, centre_kit (W/2, D/2))
def _c(W, D):
    return (W / 2.0, D / 2.0)


JOINTS = [
    # honjin: plastered dobei street wall (north line z = 26 ken) meets the board fence (east / west lines)
    ("honjin NE dobei/itabei", "jp_compound_honjin", (17 * KEN, 26 * KEN), (-0.7, -0.7), _c(17 * KEN, 26 * KEN)),
    ("honjin NW dobei/itabei", "jp_compound_honjin", (0.0, 26 * KEN), (0.7, -0.7), _c(17 * KEN, 26 * KEN)),
    # honjin front gate (roofed kabuki) posts in the dobei, back gate posts in the board fence
    ("honjin front gate W post", "jp_compound_honjin", (4.5 * KEN, 26 * KEN), (0.0, -1.0), _c(17 * KEN, 26 * KEN)),
    ("honjin front gate E post", "jp_compound_honjin", (6.0 * KEN, 26 * KEN), (0.0, -1.0), _c(17 * KEN, 26 * KEN)),
    # samurai M: black board fence meets the samurai nagaya-mon (separate object) at both ends of the south gap
    ("samurai fence/nagaya-mon W", "jp_compound_samurai_m", (4.5 * KEN, 0.0), (0.0, 1.0), _c(13 * KEN, 17.5 * KEN)),
    ("samurai fence/nagaya-mon E", "jp_compound_samurai_m", (11.5 * KEN, 0.0), (0.0, 1.0), _c(13 * KEN, 17.5 * KEN)),
    # Kanto headman: tall hedge meets the board nagaya-mon
    ("headman hedge/nagaya-mon W", "jp_compound_headman_east", (6.5 * KEN, 0.0), (0.0, 1.0), _c(20 * KEN, 17 * KEN)),
    ("headman hedge/nagaya-mon E", "jp_compound_headman_east", (13.5 * KEN, 0.0), (0.0, 1.0), _c(20 * KEN, 17 * KEN)),
    # hedge corner + hedge at the back gate
    ("headman hedge NW corner", "jp_compound_headman_east", (0.0, 17 * KEN), (0.7, -0.7), _c(20 * KEN, 17 * KEN)),
    ("headman hedge/back gate post", "jp_compound_headman_east", (9.5 * KEN, 17 * KEN), (0.0, -1.0),
     _c(20 * KEN, 17 * KEN)),
]


P3D = {"kumi": "jp_compound_kumiyashiki"}
BY_DESIGN = ("kumi ", "paperyard ")
BY_DESIGN_WHY = "yotsume-gaki: an open bamboo grid 1.05 m high, see-through by K3 design"


def auto_joints():
    """Every compound of dwelling.COMPOUNDS (D3 + W3B yards): run ends, corners and gate posts, probes towards / away
    from the plot centre. Free run ends (kumi lane fence) are expected open and marked so."""
    sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
    from jpparts.templates import dwelling as DW, trade, tradesite  # noqa: F401  (register the W3B / W3C1 yards)
    out = []
    for plot, spec in DW.COMPOUNDS.items():
        if plot not in ("brewery", "dyersyard", "paperyard"):
            continue
        Wd, Dd = spec["W"], spec["D"]
        ck = (Wd / 2.0, Dd / 2.0)
        name = P3D.get(plot, "jp_compound_" + plot)
        pts = []
        for ri, (nodes, kind, opt, ends) in enumerate(spec["runs"]):
            for k, nd in enumerate(nodes):
                tag = "corner" if (spec.get("closed") or 0 < k < len(nodes) - 1) else "run end"
                pts.append(("%s %s %s %d.%d" % (plot, kind, tag, ri, k), nd))
        for gi, (ri, si, off, kind, span) in enumerate(spec["gates"]):
            nodes = spec["runs"][ri][0]
            a, b = nodes[si], nodes[(si + 1) % len(nodes)]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
            for t, side in ((off, "A"), (off + span, "B")):
                pts.append(("%s gate%d post %s" % (plot, gi, side), (a[0] + u[0] * t, a[1] + u[1] * t)))
        seen = set()
        for lab, nd in pts:
            key = (round(nd[0], 3), round(nd[1], 3))
            if key in seen:
                continue
            seen.add(key)
            dx, dz = ck[0] - nd[0], ck[1] - nd[1]
            L = math.hypot(dx, dz)
            out.append((lab, name, nd, (dx / L, dz / L), ck))
    return out


def load_lods(full):
    info = odol_read.read_odol(full)
    out = {}
    for key, res in LODS.items():
        for lod in info["lods"]:
            if abs(lod.resolution - res) <= max(res * 1e-3, 1e-3) and lod.vertices:
                V = np.array(lod.vertices, np.float64)
                F = []
                for f in lod.faces:
                    if len(f) == 3:
                        F.append(f)
                    elif len(f) == 4:
                        F.append((f[0], f[1], f[2]))
                        F.append((f[0], f[2], f[3]))
                out[key] = (V, np.array(F, np.int64).reshape(-1, 3))
                break
    bc = np.array(info["boundingCenter"], np.float64)
    return out, bc


def slice_tris(V, F, y):
    """Segments (x0, z0, x1, z1) where the triangles cross the plane y."""
    A, B, C = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    segs = []
    ys = np.stack([A[:, 1], B[:, 1], C[:, 1]], 1)
    m = (ys.min(1) < y) & (ys.max(1) > y)
    for a, b, c in zip(A[m], B[m], C[m]):
        pts = []
        for p, q in ((a, b), (b, c), (c, a)):
            if (p[1] - y) * (q[1] - y) < 0:
                t = (y - p[1]) / (q[1] - p[1])
                pts.append((p[0] + t * (q[0] - p[0]), p[2] + t * (q[2] - p[2])))
        if len(pts) == 2:
            segs.append((pts[0][0], pts[0][1], pts[1][0], pts[1][1]))
    return segs


def raster(segs, x0, z0, n):
    G = np.zeros((n, n), bool)
    for (ax, az, bx, bz) in segs:
        L = math.hypot(bx - ax, bz - az)
        k = max(2, int(L / (CELL * 0.4)) + 1)
        t = np.linspace(0.0, 1.0, k)
        xs = ((ax + (bx - ax) * t) - x0) / CELL
        zs = ((az + (bz - az) * t) - z0) / CELL
        i = np.floor(xs).astype(int)
        j = np.floor(zs).astype(int)
        ok = (i >= 0) & (i < n) & (j >= 0) & (j < n)
        G[j[ok], i[ok]] = True
    return G


def fill_solids(G):
    """Outlines -> filled: cells not reachable from the window border are inside a closed outline (solid)."""
    reach = flood(~G, [(0, k) for k in range(G.shape[0])] + [(G.shape[0] - 1, k) for k in range(G.shape[0])]
                  + [(k, 0) for k in range(G.shape[0])] + [(k, G.shape[0] - 1) for k in range(G.shape[0])])
    return G | (~reach)


def flood(free, seeds):
    n0, n1 = free.shape
    R = np.zeros_like(free)
    stack = [(a, b) for a, b in seeds if 0 <= a < n0 and 0 <= b < n1 and free[a, b]]
    for a, b in stack:
        R[a, b] = True
    while stack:
        a, b = stack.pop()
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, q = a + da, b + db
            if 0 <= p < n0 and 0 <= q < n1 and free[p, q] and not R[p, q]:
                R[p, q] = True
                stack.append((p, q))
    return R


def dilate(G, r):
    out = G.copy()
    for _ in range(r):
        o = out.copy()
        o[1:, :] |= out[:-1, :]
        o[:-1, :] |= out[1:, :]
        o[:, 1:] |= out[:, :-1]
        o[:, :-1] |= out[:, 1:]
        out = o
    return out


def main():
    W = read_8wvr(WRP)
    T = Terrain(W["elev"], W["cell"])
    rows = read_placement_rows()
    cache = {}
    results = []
    joints = auto_joints() if "--all" in sys.argv else JOINTS
    for (label, cmp_, node, inward, ck) in joints:
        row = [r for r in rows if os.path.basename(r["p3d"]).lower() == cmp_ + ".p3d"][0]
        gy = float(T.sample(np.array([row["x"]]), np.array([row["z"]]))[0])
        M = yaw_matrix([row["yaw"]])[0]
        aside, dirv = M[0:3], M[6:9]

        def kit_to_world(x, z):
            mx, mz = x - ck[0], z - ck[1]
            return (row["x"] + mx * aside[0] + mz * dirv[0], row["z"] + mx * aside[2] + mz * dirv[2])
        jx, jz = kit_to_world(*node)
        ix, iz = kit_to_world(node[0] + inward[0] * 1.5, node[1] + inward[1] * 1.5)
        ox, oz = kit_to_world(node[0] - inward[0] * 1.5, node[1] - inward[1] * 1.5)
        y_grade = gy + row["yoff"]
        near = [r for r in rows if r is row or math.hypot(r["x"] - jx, r["z"] - jz) < 25.0]
        x0, z0 = jx - HALF_WIN, jz - HALF_WIN
        n = int(2 * HALF_WIN / CELL)
        res = {"joint": label, "world": [round(jx, 2), round(jz, 2)], "objects": sorted({os.path.basename(r["p3d"])
                                                                                          for r in near})}
        for lodk in LODS:
            for h in (0.35, 1.0, 1.6):
                segs = []
                for r in near:
                    full = p3d_file(r["p3d"])
                    if full not in cache:
                        cache[full] = load_lods(full)
                    lods, bc = cache[full]
                    if lodk not in lods:
                        continue
                    V, F = lods[lodk]
                    Mr = yaw_matrix([r["yaw"]])[0]
                    g = float(T.sample(np.array([r["x"]]), np.array([r["z"]]))[0]) + r["yoff"]
                    pos = np.array([r["x"], g, r["z"]]) + bc[0] * Mr[0:3] + bc[1] * Mr[3:6] + bc[2] * Mr[6:9]
                    Wv = pos + np.outer(V[:, 0], Mr[0:3]) + np.outer(V[:, 1], Mr[3:6]) + np.outer(V[:, 2], Mr[6:9])
                    near_v = (np.abs(Wv[:, 0] - jx) < 6) & (np.abs(Wv[:, 2] - jz) < 6)
                    if not near_v.any():
                        continue
                    segs += slice_tris(Wv, F, y_grade + h)
                G = fill_solids(raster(segs, x0, z0, n))
                if PNG and lodk == "geo" and h == 1.0:
                    from PIL import Image
                    im = np.stack([~G[::-1] * 255] * 3, -1).astype(np.uint8)
                    for (pz, px), col in (((int((iz - z0) / CELL), int((ix - x0) / CELL)), (0, 160, 0)),
                                          ((int((oz - z0) / CELL), int((ox - x0) / CELL)), (200, 0, 0))):
                        im[n - 1 - pz - 2:n - 1 - pz + 3, px - 2:px + 3] = col
                    Image.fromarray(im).resize((400, 400), Image.NEAREST).save(
                        os.path.join(DEV, "spikes", "W3C1", "renders", "joint_%s.png" % label.replace(" ", "_").replace("/", "-")))
                a = (int((iz - z0) / CELL), int((ix - x0) / CELL))
                b = (int((oz - z0) / CELL), int((ox - x0) / CELL))
                if G[a] or G[b]:
                    res["%s@%.2f" % (lodk, h)] = "probe point inside a solid"
                    continue
                R = flood(~G, [a])
                if not R[b]:
                    res["%s@%.2f" % (lodk, h)] = "sealed"
                    continue
                gap = None
                for r_ in range(1, 40):
                    D_ = dilate(G, r_)
                    if D_[a] or D_[b]:
                        break
                    if not flood(~D_, [a])[b]:
                        gap = 2 * r_ * CELL
                        break
                res["%s@%.2f" % (lodk, h)] = "LEAK gap ~%.2f m" % gap if gap else "LEAK (wide open)"
        results.append(res)
        bad = [k for k, v in res.items() if isinstance(v, str) and v.startswith("LEAK")]
        if bad and label.startswith(BY_DESIGN):
            res["by_design"] = BY_DESIGN_WHY
            print("%-32s %s" % (label, "open by design (%s)" % BY_DESIGN_WHY))
            continue
        print("%-32s %s  %s" % (label, "OK " if not bad else "BAD",
                                "; ".join("%s %s" % (k, res[k]) for k in bad) if bad else ""))
    with open(os.path.join(DEV, "spikes", "W3C1", "jointcheck.json"), "wb") as f:
        f.write(json.dumps(results, indent=1).encode("utf-8"))
    return results


if __name__ == "__main__":
    main()
