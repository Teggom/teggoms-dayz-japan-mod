"""Q5 step 3: how do vanilla furniture proxies relate to the loot points?

For each vanilla house class: read its Res 1 proxies (name + transform, q5_lods.proxies_at), each furniture p3d's
bounding box (odol_read header), and the class's loot points from the vanilla Chernarus mapgroupproto.xml. Loot
points are converted to model axes with (mx, my, mz) = (-lz, ly, lx) (pokemon_dev WORLD_BUILDINGS.md §0, proven on
360 classes). Then every point is classified:
  floor  - within 0.10 m of the lowest floor level of the house... (we use: no furniture footprint under it, or
           it sits at the height of a floor point)
  on     - inside a furniture footprint and 0.05-0.30 m above that piece's bottom or on/below its top
Prints one line per point and a summary per container. Writes JSON with --json OUT.

Run: python research/interior/tools/q5_loot.py Land_House_1W01=P:\\DZ\\structures\\residential\\houses\\house_1w01.p3d ...
Read-only on P:\\DZ and the vanilla mission. Research agent PA2, 2026-09-29.
"""
import json, math, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "tools", "placecheck"))
import q5_lods  # noqa: E402
import odol_read  # noqa: E402

PROTO = os.path.join(DEV, "..", "mpmissions", "dayzOffline.chernarusplus", "mapgroupproto.xml")
_bbox_cache = {}


def furn_bbox(name):
    p = "P:" + name + ".p3d"
    if p in _bbox_cache:
        return _bbox_cache[p]
    try:
        d = open(p, "rb").read(4096)
        ver, n = struct.unpack_from("<II", d, 4)
        mi = 12 + 4 * n
        f = struct.unpack_from("<42f", d, mi)
        bb = (f[12:15], f[15:18])
    except Exception:  # noqa: BLE001
        bb = None
    _bbox_cache[p] = bb
    return bb


def res1_proxies(path):
    d, ver, res, s, e = q5_lods.table_only(path)
    i = res.index(min(res))
    n = struct.unpack_from("<I", d, s[i])[0]
    p = s[i] + 4
    out = []
    for _ in range(n):
        z = d.index(b"\x00", p)
        name = d[p:z].decode("latin-1")
        p = z + 1
        tr = struct.unpack_from("<12f", d, p)
        p += 64
        out.append((name, tr))
    return out


def proto_points(cls):
    txt = open(PROTO, "rb").read().decode("utf-8", "replace")
    m = re.search(r'<group name="%s">(.*?)</group>' % re.escape(cls), txt, re.S)
    pts = []
    if not m:
        return pts
    for c in re.finditer(r'<container name="([^"]+)"[^>]*>(.*?)</container>', m.group(1), re.S):
        for q in re.finditer(r'<point pos="([-\d.]+) ([-\d.]+) ([-\d.]+)" range="([\d.]+)" height="([\d.]+)"', c.group(2)):
            lx, ly, lz, rg, h = map(float, q.groups())
            pts.append({"container": c.group(1), "model": (-lz, ly, lx), "range": rg, "height": h})
    return pts


def footprint(tr, bb, transpose):
    (x0, y0, z0), (x1, y1, z1) = bb
    R = tr[:9]
    pos = tr[9:12]
    corners = []
    for x in (x0, x1):
        for y in (y0, y1):
            for z in (z0, z1):
                if transpose:
                    w = (R[0] * x + R[1] * y + R[2] * z, R[3] * x + R[4] * y + R[5] * z, R[6] * x + R[7] * y + R[8] * z)
                else:
                    w = (R[0] * x + R[3] * y + R[6] * z, R[1] * x + R[4] * y + R[7] * z, R[2] * x + R[5] * y + R[8] * z)
                corners.append((w[0] + pos[0], w[1] + pos[1], w[2] + pos[2]))
    xs, ys, zs = zip(*corners)
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


def classify(path, cls, transpose):
    prox = [(n, tr, furn_bbox(n)) for (n, tr) in res1_proxies(path) if "furniture" in n.lower()]
    pts = proto_points(cls)
    floor_y = min((p["model"][1] for p in pts), default=0.0)
    rows = []
    for p in pts:
        x, y, z = p["model"]
        hit = None
        for (n, tr, bb) in prox:
            if not bb:
                continue
            fx0, fx1, fy0, fy1, fz0, fz1 = footprint(tr, bb, transpose)
            if fx0 - 0.02 <= x <= fx1 + 0.02 and fz0 - 0.02 <= z <= fz1 + 0.02 and fy0 - 0.05 <= y <= fy1 + 0.10:
                hit = (n.replace("\\", "/").split("/")[-1], round(y - fy0, 2), round(fy1 - fy0, 2))
                if y - floor_y > 0.05:
                    break
        rows.append({"container": p["container"], "above_floor_m": round(y - floor_y, 2), "range": p["range"],
                     "height": p["height"], "furniture": hit})
    return {"class": cls, "file": path, "n_furniture_proxies": len(prox), "points": rows}


if __name__ == "__main__":
    args = sys.argv[1:]
    out = None
    if "--json" in args:
        k = args.index("--json")
        out = args[k + 1]
        del args[k:k + 2]
    res = []
    for a in args:
        cls, path = a.split("=", 1)
        best = None
        for tp in (False, True):
            r = classify(path, cls, tp)
            score = sum(1 for p in r["points"] if p["furniture"] and p["above_floor_m"] > 0.05)
            if best is None or score > best[0]:
                best = (score, tp, r)
        score, tp, r = best
        r["rotation_convention"] = "transposed" if tp else "row-vector"
        res.append(r)
        print("==", cls, "furniture proxies", r["n_furniture_proxies"], "| points", len(r["points"]), "| convention", r["rotation_convention"])
        by = {}
        for p in r["points"]:
            c = by.setdefault(p["container"], {"n": 0, "raised": 0, "raised_on_furniture": 0, "floor": 0, "floor_in_furn_footprint": 0})
            c["n"] += 1
            if p["above_floor_m"] > 0.05:
                c["raised"] += 1
                if p["furniture"]:
                    c["raised_on_furniture"] += 1
            else:
                c["floor"] += 1
                if p["furniture"]:
                    c["floor_in_furn_footprint"] += 1
        for k, v in by.items():
            print("   %-14s %s" % (k, v))
        for p in r["points"]:
            if p["above_floor_m"] > 0.05:
                print("     raised %-12s y+%.2f r%.2f -> %s" % (p["container"], p["above_floor_m"], p["range"], p["furniture"]))
    if out:
        with open(out, "wb") as f:
            f.write((json.dumps(res, indent=1) + "\n").encode("utf-8"))
