"""Offline check of the two MLOD facts W relies on, with a 12-triangle weighted cube:
  1. binarize accepts an MLOD bound to DayzTemporarySkeleton (model.cfg from modelcfg.py) and the ODOL carries
     the skeleton, the bone selections and the camo sections;
  2. binarize REVERSES each face's vertex order (so vanilla ODOL faces are the reverse of their MLOD source).
Writes into P:\\JP\\characters\\_cubetest (= src/JP/characters/_cubetest) and removes it afterwards.
"""
import os
import shutil
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mlod_w as mlod  # noqa: E402
from modelcfg import model_cfg  # noqa: E402
from wlib import SRC, WORK, BINARIZE  # noqa: E402

name = "jp_cubetest_m"
src = os.path.join(SRC, "_cubetest")
os.makedirs(src, exist_ok=True)
lod = mlod.Lod(mlod.LOD_VISUAL_1)
c = [(x, y, z) for x in (-0.1, 0.1) for y in (1.6, 1.8) for z in (-0.1, 0.1)]
pis = [lod.add_point(p) for p in c]
# deliberately recognisable first face: points 0, 1, 3
tri = [(0, 1, 3), (0, 3, 2), (4, 6, 7), (4, 7, 5), (0, 4, 5), (0, 5, 1), (2, 3, 7), (2, 7, 6), (0, 2, 6), (0, 6, 4), (1, 5, 7), (1, 7, 3)]
ni = lod.add_normal((0, 0, -1))
fis = [lod.add_face([(pis[i], ni, 0.0, 0.0) for i in t], texture="#(argb,8,8,3)color(1,0,0,1,co)") for t in tri]
lod.select("head", {p: 1.0 for p in pis}, fis)
lod.select("camoMale", {p: 1.0 for p in pis}, fis)
lod.properties["lodnoshadow"] = "1"
geo = mlod.Lod(mlod.LOD_GEOMETRY)
gp = [geo.add_point(p) for p in c]
gn = geo.add_normal((0, 0, -1))
gf = [geo.add_face([(gp[i], gn, 0.0, 0.0) for i in t]) for t in tri]
geo.select("Component01", {p: 1.0 for p in gp}, gf)
geo.properties["autocenter"] = "0"
geo.mass = [0.1] * len(gp)
mlod.write_mlod(os.path.join(src, name + ".p3d"), [lod, geo])
with open(os.path.join(src, "model.cfg"), "wb") as f:
    f.write(model_cfg([name], []).encode())
out = os.path.join(WORK, "cubetest_bin")
shutil.rmtree(out, ignore_errors=True)
os.makedirs(out)
cmd = [BINARIZE, "-always", "-silent", "-addon=P:\\JP", "-binpath=P:\\bin", "P:\\JP\\characters\\_cubetest", out, "*.p3d"]
r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
log = r.stdout + r.stderr
open(os.path.join(WORK, "cubetest_binarize.log"), "wb").write(log.encode())
print("\n".join(l for l in log.splitlines() if l.strip())[-3000:])
op = os.path.join(out, name + ".p3d")
if not os.path.isfile(op):
    raise SystemExit("no output")
d = open(op, "rb").read()
print("magic", d[:4], "size", len(d))
from pstrings import runs  # noqa: E402
print([s for _, s in runs(d, 4)][:40])
# find the 12-face polygon block: u32 12, u32 size, u16 0, then 12 x (u8 3, 3 x u16)
for o in range(len(d) - 20):
    if struct.unpack_from("<IIH", d, o)[:1] == (12,) and d[o + 10] == 3:
        faces = []
        p = o + 10
        ok = True
        for _ in range(12):
            if d[p] != 3:
                ok = False
                break
            faces.append(struct.unpack_from("<3H", d, p + 1))
            p += 7
        if ok:
            print("ODOL faces:", faces)
            break
shutil.rmtree(src, ignore_errors=True)
