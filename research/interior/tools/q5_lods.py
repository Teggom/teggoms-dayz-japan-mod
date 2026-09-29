"""Q5 step 2: per LOD, which proxies does a vanilla house carry?

For each ODOL given: read the LOD table (tools/placecheck/odol_read.py, read-only import), then at each LOD start read
u32 nProxies and walk the proxy records (asciiz model name, 12 floats transform, 4 x u32). As a cross-check, also count
the raw "dz\\structures\\furniture" strings inside each LOD's byte span.

Run: python research/interior/tools/q5_lods.py P:\\DZ\\structures\\residential\\houses\\house_1w01.p3d ...
Writes nothing unless --json OUT is given. Research agent A-INT, 2026-09-29.
"""
import json, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DEV, "tools", "placecheck"))
import odol_read  # noqa: E402

FURN = re.compile(rb"dz\\structures\\furniture\\[a-z0-9_\\]+", re.I)


def lod_name(r):
    if r < 1000:
        return "Res %g" % r
    if 1e4 <= r < 2e4:
        return "ShadowVolume %g" % (r - 1e4)
    table = [(1e13, "Geometry"), (2e13, "GeometryBuoyancy"), (4e13, "GeometryPhysX"), (1e15, "Memory"),
             (2e15, "LandContact"), (3e15, "Roadway"), (4e15, "Paths"), (5e15, "HitPoints"), (6e15, "ViewGeometry"),
             (7e15, "FireGeometry"), (8e15, "ViewCargoGeometry"), (9e15, "ViewCargoFireGeometry"),
             (1e16, "ViewCommander"), (1.1e16, "ViewCommanderGeometry"), (1.2e16, "ViewCommanderFireGeometry"),
             (1.3e16, "ViewPilotGeometry"), (1.4e16, "ViewPilotFireGeometry"), (1.5e16, "ViewGunnerGeometry"),
             (1.6e16, "ViewGunnerFireGeometry"), (1.7e16, "SubParts"), (1.8e16, "ShadowVolumeViewCargo"),
             (1.9e16, "ShadowVolumeViewPilot"), (2e16, "ShadowVolumeViewGunner"), (2.1e16, "Wreck")]
    for v, n in table:
        if abs(r - v) / v < 1e-3:
            return n
    return "?%g" % r


def table_only(path):
    d = open(path, "rb").read()
    ver, n = struct.unpack_from("<II", d, 4)
    res = list(struct.unpack_from("<%df" % n, d, 12))
    mi = 12 + 4 * n
    L = len(d)
    for o in range(mi, L - 8 * n):
        st = struct.unpack_from("<%dI" % (2 * n), d, o)
        s, e = st[:n], st[n:]
        if not (all(o < x <= L for x in st) and all(s[i] < e[i] for i in range(n)) and max(e) == L):
            continue
        spans = sorted(zip(s, e))
        if all(spans[k][1] == spans[k + 1][0] for k in range(n - 1)) and spans[-1][1] == L:
            return d, ver, res, list(s), list(e)
    raise ValueError("LOD table not found")


def proxies_at(d, o, end):
    n = struct.unpack_from("<I", d, o)[0]
    out = []
    p = o + 4
    if n > 5000:
        return None, "implausible nProxies %d" % n
    for _ in range(n):
        z = d.index(b"\x00", p)
        name = d[p:z].decode("latin-1")
        p = z + 1
        tr = struct.unpack_from("<12f", d, p)
        p += 48
        ints = struct.unpack_from("<4I", d, p)
        p += 16
        if p > end:
            return None, "overran LOD"
        out.append({"name": name, "pos": [round(tr[9], 3), round(tr[10], 3), round(tr[11], 3)], "ints": ints})
    return out, None


def probe(path):
    d, ver, res, s, e = table_only(path)
    rows = []
    for i, r in enumerate(res):
        prox, err = proxies_at(d, s[i], e[i])
        raw = FURN.findall(d[s[i]:e[i]])
        rows.append({"lod": lod_name(r), "resolution": r, "n_proxies": None if prox is None else len(prox),
                     "error": err, "furniture_proxies": sorted({x["name"] for x in (prox or []) if "furniture" in x["name"].lower()}),
                     "other_proxies": sorted({x["name"] for x in (prox or []) if "furniture" not in x["name"].lower()}),
                     "n_furniture_records": sum(1 for x in (prox or []) if "furniture" in x["name"].lower()),
                     "raw_furniture_strings": len(raw), "bytes": e[i] - s[i]})
    return {"file": path, "odol_version": ver, "lods": rows}


if __name__ == "__main__":
    args = sys.argv[1:]
    out = None
    if "--json" in args:
        k = args.index("--json")
        out = args[k + 1]
        del args[k:k + 2]
    allres = []
    for p in args:
        r = probe(p)
        allres.append(r)
        print("==", os.path.basename(p), "ODOL v%d" % r["odol_version"])
        for L in r["lods"]:
            print("  %-22s nProx %-5s furn %-4s raw %-4s other %s%s" % (
                L["lod"], L["n_proxies"], L["n_furniture_records"], L["raw_furniture_strings"],
                len(L["other_proxies"]), ("  ERR " + L["error"]) if L["error"] else ""))
    if out:
        with open(out, "wb") as f:
            f.write((json.dumps(allres, indent=1) + "\n").encode("utf-8"))
