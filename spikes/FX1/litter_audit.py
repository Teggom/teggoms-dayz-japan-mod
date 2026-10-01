"""FX1 litter audit: which wave-2 placed models carry leaf litter (decal_litter / ground_leaf_litter faces) of their own?

Sources: the site rows of test/placements/W2F.csv and the Resolution-1 proxies of the wave-2 furnished MLODs
(buildings/furnished/out). For each model with litter faces: where it stands (room / site) and the litter's height
over the model base (on top of the model = draped on it; at 0-5 mm = ground litter around it).

  python spikes/FX1/litter_audit.py
"""
import csv
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "buildings")):
    sys.path.insert(0, p)
from jpparts import mlod, proxies as PX, decor as DC  # noqa: E402

W2 = ("shrine", "temple", "teahouse", "smithy", "swordsmith", "guardhut", "kido")
KEYS = ("litter", "leaf")


def litter_faces(master):
    out = []
    for l in mlod.read_mlod(master):
        if mlod.lod_name(l.resolution) != "Resolution 1":
            continue
        for verts, _, tex, mat in l.faces:
            m = (mat or "").lower() + " " + (tex or "").lower()
            if any(k in m for k in KEYS):
                out.append(max(l.points[v[0]][1] for v in verts))
    return out


def main():
    cat = DC.catalog()
    by_p3d = {v["p3d"].lstrip("\\").lower(): k for k, v in cat.items()}
    uses = {}
    csvs = sorted(glob.glob(os.path.join(DEV, "test", "placements", "*.csv"))) if "--all" in sys.argv else         [os.path.join(DEV, "test", "placements", "W2F.csv")]
    for cp in csvs:
        with open(cp, newline="") as f:
            for row in csv.DictReader(f):
                k = by_p3d.get(row["p3d"].lower())
                if k:
                    uses.setdefault(k, []).append("%s site %.1f,%.1f" % (os.path.basename(cp)[:-4], float(row["x"]),
                                                                      float(row["z"])))
    for p in ([] if "--sites" in sys.argv else sorted(glob.glob(os.path.join(DEV, "buildings", "furnished", "out",
                                                                              "*.p3d")))):
        b = os.path.basename(p)
        if b[3:].split("_")[0] not in W2:
            continue
        l = next(q for q in mlod.read_mlod(p) if mlod.lod_name(q.resolution) == "Resolution 1")
        for name, o, up, fw in PX.listed(l):
            stem = name.split(":", 1)[1].rsplit(".", 1)[0].replace("\\", "/").split("/")[-1].lower()
            if stem in cat:
                uses.setdefault(stem, []).append("%s (%.1f, %.2f, %.1f)" % (b[:-4], o[0], o[1], o[2]))
    n = 0
    for k in sorted(uses):
        ys = litter_faces(cat[k]["master"])
        if not ys:
            continue
        n += 1
        top = cat[k]["bbox"][3]
        print("%-32s litter faces %3d, at y %.3f..%.3f (model top %.2f)" % (k, len(ys), min(ys), max(ys), top))
        for u in sorted(set(uses[k])):
            print("      " + u)
    print("LITTER AUDIT: %d wave-2 placed models carry litter faces" % n)


if __name__ == "__main__" and "--near" not in sys.argv:
    main()


def near_report(radius_tree=10.0, radius_litter=8.0):
    """--near: every SITE placement (all CSVs) of a model with litter ON it (a litter face >= 3 cm over its base):
    trees within radius_tree (T's trees + placed tree / bamboo / pine / sakura models) and ground-litter props within
    radius_litter. 'ALONE' = neither: litter there has no source around it (the offering-box mistake)."""
    import math
    sys.path.insert(0, os.path.join(DEV, "spikes", "SH1"))
    import terrain_sh1 as T
    cat = DC.catalog()
    by_p3d = {v["p3d"].lstrip("\\").lower(): k for k, v in cat.items()}
    rows = []
    for cp in sorted(glob.glob(os.path.join(DEV, "test", "placements", "*.csv"))):
        with open(cp, newline="") as f:
            for row in csv.DictReader(f):
                rows.append((os.path.basename(cp)[:-4], row["p3d"].lower(), float(row["x"]), float(row["z"])))
    trees = [(float(t[0]), float(t[1])) for t in T.trees()]
    trees += [(x, z) for _, p, x, z in rows if any(k in p for k in ("tree", "bamboo", "pine", "sakura", "matsu",
                                                                     "sugi", "hinoki", "momiji", "keyaki"))]
    cache = {}

    def raised(k):
        if k not in cache:
            ys = litter_faces(cat[k]["master"])
            cache[k] = (max(ys) if ys else None, bool(ys) and min(ys) < 0.01)
        return cache[k]
    ground = [(x, z) for _, p, x, z in rows if by_p3d.get(p) and
              (raised(by_p3d[p])[1] or "leaf_pile" in p or "debris_leaves" in p)]
    alone = 0
    for src, p, x, z in rows:
        k = by_p3d.get(p)
        if not k:
            continue
        top, _ = raised(k)
        if top is None or top < 0.03:
            continue
        nt = sum(1 for tx, tz in trees if math.hypot(tx - x, tz - z) <= radius_tree)
        ng = sum(1 for gx, gz in ground if 0.05 < math.hypot(gx - x, gz - z) <= radius_litter)
        tag = "ALONE" if nt == 0 and ng == 0 else "ok"
        alone += tag == "ALONE"
        print("%-5s %-36s %-5s (%.1f, %.1f) litter top %.2f  trees<=%.0fm %d  ground litter<=%.0fm %d" % (
            tag, k, src, x, z, top, radius_tree, nt, radius_litter, ng))
    print("NEAR: %d placements with litter on them and no source around" % alone)


if __name__ == "__main__" and "--near" in sys.argv:
    near_report()
