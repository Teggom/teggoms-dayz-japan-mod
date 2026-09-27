"""One-off experiment: how does binarize choose the ODOL boundingCenter of an MLOD?
Writes three test MLODs whose visual / geometry / memory LODs have different extents, binarizes them and prints
the resulting boundingCenter next to the candidate rules. Output under data/T_terrain/bc_experiment/.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DEV, "tools", "common"))
sys.path.insert(0, HERE)
import mlod  # noqa: E402
from odol import odol_info, mlod_center  # noqa: E402

BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
SRC = os.path.join(DEV, "src", "JP", "worlds", "testisland", "_smoke", "bc")
OUT = os.path.join(DEV, "data", "T_terrain", "bc_experiment")


def box(lod, x0, y0, z0, x1, y1, z1, tex=""):
    p = [lod.add_point((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    n = lod.add_normal((0, 1, 0))
    # 6 quads (winding not important for this test)
    for a, b, c, d in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
        lod.add_face([(p[a], n, 0, 0), (p[b], n, 0, 1), (p[c], n, 1, 1), (p[d], n, 1, 0)], tex, "")


def make(name, vis, geo, mem, props=None):
    lods = []
    v = mlod.Lod(1.0)
    box(v, *vis)
    lods.append(v)
    g = mlod.Lod(mlod.LOD_GEOMETRY)
    box(g, *geo)
    g.mass = [10.0] * len(g.points)
    for k, val in (props or {}).items():
        g.properties[k] = val
    lods.append(g)
    if mem:
        m = mlod.Lod(mlod.LOD_MEMORY)
        m.add_point(mem)
        lods.append(m)
    mlod.write_mlod(os.path.join(SRC, name + ".p3d"), lods)


os.makedirs(SRC, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
make("bc_a", (-1, 0, -1, 1, 2, 1), (-1, 0, -1, 1, 6, 1), None)                  # geometry taller than visual
make("bc_b", (-1, 0, -1, 1, 6, 1), (-1, 0, -1, 1, 2, 1), None)                  # visual taller than geometry
make("bc_c", (-1, 0, -1, 1, 2, 1), (-1, 0, -1, 1, 2, 1), (0, 10, 0))            # far memory point
make("bc_d", (-1, 0, -1, 3, 2, 1), (-1, 0, -1, 3, 2, 1), None, {"autocenter": "0"})
cmd = [BINARIZE, "-always", "-silent", "-binpath=P:\\", "P:\\JP\\worlds\\testisland\\_smoke\\bc", OUT, "*.p3d"]
res = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
open(os.path.join(OUT, "binarize.log"), "wb").write((res.stdout + res.stderr).encode("utf-8"))
for n in ("bc_a", "bc_b", "bc_c", "bc_d"):
    p = os.path.join(OUT, n + ".p3d")
    info = odol_info(p) if os.path.isfile(p) else None
    src = os.path.join(SRC, n + ".p3d")
    print(n, "ODOL bc", info and tuple(round(x, 3) for x in info["bc"]),
          "| all", tuple(round(x, 3) for x in mlod_center(src, "all")[0]),
          "| visual", tuple(round(x, 3) for x in mlod_center(src, "visual")[0]),
          "| geometry", tuple(round(x, 3) for x in mlod_center(src, "geometry")[0]))
