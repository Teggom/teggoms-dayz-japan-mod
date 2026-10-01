"""V1 bench: the ray checks (C11 envelope leak, C15 silhouette, C17 jamb slits) of one building, old vs candidate
engines, timed and compared ray by ray.  python spikes/V1/bench_rays.py <key>"""
import os
import pickle
import sys
import time

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in ("buildings", "parts/kit", "tools/common", "spikes/B_building/kit"):
    sys.path.insert(0, os.path.join(DEV, p))
import numpy as np  # noqa: E402

CACHE = os.path.join(DEV, "spikes", "V1", "prof")


def inputs(key):
    """(T1 triangles, rooms, portals, door list data) for C11 of one building, pickled after the first build."""
    p = os.path.join(CACHE, key + ".c11.pkl")
    if os.path.isfile(p):
        with open(p, "rb") as f:
            return pickle.load(f)
    import pipeline as P
    import registry
    from jpparts import mlod, raycheck as RC, checks as C
    b = registry.get(key)
    bd = P.build_model(b, stage=False)
    lods = mlod.read_mlod(bd["mlod"])
    if hasattr(bd["mod"], "proxies") and getattr(bd["mod"], "D", None) is not None:
        from jpparts import proxies as PX
        lods = [PX.strip(l) for l in lods]
    L = {mlod.lod_name(l.resolution): l for l in lods}
    M, floors = bd["M"], bd["floors"]
    rooms = [{"name": f["name"], "rect": f["rect"], "y": f["y"], "obstacles": f.get("obstacles", [])} for f in floors
             if f.get("enclosed", True)]
    vcomps = C.components(L["View Geometry"])
    portals = []
    for k, d in enumerate(M.doors, 1):
        bones = {a["bone"] for a in d.anims}
        lb = [c["bbox"] for c in vcomps if c["door"] in bones]
        if lb:
            bx = [min(b[0] for b in lb), max(b[1] for b in lb), min(b[2] for b in lb), max(b[3] for b in lb),
                  min(b[4] for b in lb), max(b[5] for b in lb)]
            a0 = d.anims[0]
            u = [abs(a0["axis"][1][q] - a0["axis"][0][q]) for q in range(3)]
            nx = 0.20 if u[2] > u[0] else 0.06
            nz = 0.20 if u[0] >= u[2] else 0.06
            if getattr(d, "half", False) and d.action:
                bx[3] = max(bx[3], d.action[1] + getattr(d, "half_top", 1.0))
                bx[2] = min(bx[2], d.action[1] - getattr(d, "act_h", 1.0))
            portals.append(("DoorsTwin%d" % k, (bx[0] - nx, bx[1] + nx, bx[2] - 0.06, bx[3] + 0.06, bx[4] - nz,
                                                  bx[5] + nz)))
    portals += [(n_, tuple(b_)) for n_, b_ in getattr(bd["mod"], "PORTALS", ())]
    T = {ln: RC.lod_triangles(L[ln]) for ln in ("Resolution 1", "Resolution 2", "Resolution 3")}
    bbox = M.bbox()
    jamb = []
    for d in M.doors:
        if d.kind != "lattice":
            jamb.append((d, ))
    out = {"T": T, "rooms": rooms, "portals": portals, "bbox": bbox}
    with open(p, "wb") as f:
        pickle.dump(out, f)
    return out


def c11_rays(rooms, ndirs=320, heights=(0.5, 1.1, 1.65), grid=(4, 3)):
    from jpparts import raycheck as RC
    D = RC.fib_dirs(ndirs)
    allO, allD = [], []
    for r in rooms:
        x0, x1, z0, z1 = r["rect"]
        O = []
        for i in range(grid[0]):
            for j in range(grid[1]):
                x = x0 + 0.25 + (x1 - x0 - 0.5) * (i + 0.5) / grid[0]
                z = z0 + 0.25 + (z1 - z0 - 0.5) * (j + 0.5) / grid[1]
                if any(a0 <= x <= a1 and b0 <= z <= b1 for (a0, a1, b0, b1) in r.get("obstacles", ())):
                    continue
                for h in heights:
                    O.append((x, r["y"] + h, z))
        O = np.asarray(O, float)
        allO.append(np.repeat(O, len(D), 0))
        allD.append(np.tile(D, (len(O), 1)))
    return np.concatenate(allO), np.concatenate(allD)


def main():
    key = sys.argv[1]
    which = sys.argv[2:] or ["old", "new"]
    from jpparts import raycheck as RC
    I = inputs(key)
    T = I["T"]["Resolution 1"]
    OO, DD = c11_rays(I["rooms"])
    print("%s: %d R1 triangles, %d C11 rays" % (key, len(T), len(OO)))
    res = {}
    if "old" in which:
        t0 = time.perf_counter()
        t_old = RC.cast(T, OO, DD)
        res["old"] = np.isinf(t_old)
        print("old cast       %.2f s, escaped %d" % (time.perf_counter() - t0, int(res["old"].sum())))
    if "new" in which:
        import importlib
        import raycast_v1 as RV
        importlib.reload(RV)
        t0 = time.perf_counter()
        esc = RV.escapes(T, OO, DD, 60.0)
        res["new"] = esc
        print("new escapes    %.2f s, escaped %d" % (time.perf_counter() - t0, int(esc.sum())))
    if "old" in res and "new" in res:
        diff = np.where(res["old"] != res["new"])[0]
        print("rays differing: %d" % len(diff), diff[:10])


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
