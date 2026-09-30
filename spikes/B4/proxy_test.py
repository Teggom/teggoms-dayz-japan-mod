"""Which MLOD proxy triangle does binarize.exe read how? Writes a tiny test model with four differently built proxy
triangles (all meant as yaw 90), binarizes it and prints the ODOL proxy transforms. Temporary files only:
src/JP/buildings/_b4test (removed at the end) and data/B4/proxy_test."""
import os, shutil, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "research", "interior", "tools"))
from jpparts import mlod, core  # noqa
import q5_lods  # noqa

TMP = os.path.join(DEV, "src", "JP", "buildings", "_b4test")
OUT = os.path.join(DEV, "data", "B4", "proxy_test")
BIN = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
TANSU = "\\JP\\furniture\\storage\\jp_f_tansu"


def box_lod(res, geo=False):
    L = mlod.Lod(res)
    v = [(x, y, z) for x in (-3, 3) for y in (0, 0.2) for z in (-3, 3)]
    f = [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]]
    pis, fis = L.add_closed_solid(v, f, "", "dz\\data\\data\\penetration\\wood.rvmat" if geo else "")
    if geo:
        L.select("Component01", {p: 1.0 for p in pis}, fis)
        L.properties.update({"class": "house", "map": "house", "autocenter": "0"})
        L.mass = [100.0] * len(L.points)
    return L


def main():
    os.makedirs(TMP, exist_ok=True)
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    r1, geo = box_lod(1.0), box_lod(mlod.LOD_GEOMETRY, True)
    up, fw = (0.0, 1.0, 0.0), (1.0, 0.0, 0.0)          # yaw 90: forward = +x
    tris = {1: lambda o: [o, add(o, up, 2), add(o, fw, 1)],
            2: lambda o: [o, add(o, fw, 1), add(o, up, 2)],
            3: lambda o: [o, add(o, fw, 2), add(o, up, 1)],
            4: lambda o: [o, add(o, up, 1), add(o, fw, 2)]}
    for L in (r1, geo):
        for k, fn in tris.items():
            o = (float(k), 0.2, 0.0)
            pts = fn(o)
            pis = [L.add_point(p) for p in pts]
            ni = L.add_normal(mlod._normalize(mlod._face_formula_normal(pts)))
            fi = L.add_face([(pi, ni, 0.0, 0.0) for pi in pis])
            L.select("proxy:%s.%03d" % (TANSU, k), {p: 1.0 for p in pis}, [fi])
            if L.mass is not None:
                L.mass += [0.0] * 3
    mlod.write_mlod(os.path.join(TMP, "b4_proxytest.p3d"), [r1, geo])
    cmd = [BIN, "-always", "-addon=P:\\JP\\buildings", "-binpath=P:\\bin", "P:\\JP\\buildings\\_b4test", OUT, "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if l.strip())[-1500:])
    found = None
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".p3d"):
                found = os.path.join(root, f)
    print("ODOL:", found)
    d, ver, res, s, e = q5_lods.table_only(found)
    for i, rr in enumerate(res):
        n = struct.unpack_from("<I", d, s[i])[0]
        p = s[i] + 4
        print("LOD", q5_lods.lod_name(rr), "proxies", n)
        for _ in range(n):
            z = d.index(b"\x00", p)
            name = d[p:z].decode("latin-1")
            p = z + 1
            tr = struct.unpack_from("<12f", d, p)
            p += 48 + 16
            print("  %-45s rows %s | %s | %s pos %s" % (name, [round(v, 3) for v in tr[0:3]], [round(v, 3) for v in tr[3:6]],
                                                   [round(v, 3) for v in tr[6:9]], [round(v, 3) for v in tr[9:12]]))
    shutil.rmtree(TMP, ignore_errors=True)


def add(o, v, s):
    return (o[0] + v[0] * s, o[1] + v[1] * s, o[2] + v[2] * s)


if __name__ == "__main__":
    main()
