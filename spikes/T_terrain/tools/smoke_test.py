"""Route A smoke tests (run once, kept for the record):
  1. round-trip Bohemia's utes.wrp (8WVR) through wrp8.read_8wvr + Wrp8.write and compare bytes
  2. write a tiny 8WVR with vanilla materials + objects, binarize it, read the OPRW back
Usage: python smoke_test.py <path to utes.wrp or ->
"""
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wrp8  # noqa: E402
from odol import odol_info  # noqa: E402

BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SMOKE_SRC = os.path.join(DEV, "src", "JP", "worlds", "testisland", "_smoke")
SMOKE_OUT = os.path.join(DEV, "data", "T_terrain", "smoke_out")


def roundtrip(path):
    w = wrp8.read_8wvr(path)
    lx = w["land"][0]
    tx = w["terrain"][0]
    o = wrp8.Wrp8(lx, tx, w["cell"])
    o.elevation = w["elev"].copy()
    o.material_index = w["mat"].copy()
    o.materials = w["names"]
    for m, oid, name in w["objects"][:-1]:
        o.objects.append((m[0:3], m[3:6], m[6:9], m[9:12], oid, name))
    tmp = os.path.join(SMOKE_OUT, "utes_roundtrip.wrp")
    os.makedirs(SMOKE_OUT, exist_ok=True)
    o.write(tmp)
    a = open(path, "rb").read()
    b = open(tmp, "rb").read()
    # the dummy terminator differs only in its id (TB writes a running number, we write INT_MAX)
    tail = 48 + 8
    same = a[:-tail] == b[:-tail]
    print("round-trip utes.wrp: %d vs %d bytes, identical except dummy: %s" % (len(a), len(b), same))
    return same


def smoke_binarize():
    os.makedirs(SMOKE_SRC, exist_ok=True)
    os.makedirs(SMOKE_OUT, exist_ok=True)
    land, terr, cell = 32, 128, 16.0   # 512 m
    w = wrp8.Wrp8(land, terr, cell)
    yy, xx = np.mgrid[0:terr, 0:terr] * 4.0
    w.elevation[:] = 10.0 + 5.0 * np.sin(xx / 60.0) * np.cos(yy / 80.0)
    mi = w.add_material(r"dz\worlds\chernarusplus\data\layers\p_000-000_l01_l03_l04_n_l10.rvmat")
    w.material_index[:] = mi
    for p3d, x, z in [(r"dz\plants\tree\t_pinussylvestris_2s.p3d", 200.0, 200.0),
                      (r"dz\structures\industrial\power\power_pole_wood1.p3d", 260.0, 250.0),
                      (r"dz\structures\roads\parts\grav_12.p3d", 300.0, 300.0)]:
        bc = odol_info(os.path.join("P:\\", p3d))["bc"]
        g = 10.0 + 5.0 * np.sin(x / 60.0) * np.cos(z / 80.0)
        aside, up, dirv = wrp8.yaw_matrix(30.0)
        pos = np.array([x, g, z]) + bc[0] * aside + bc[1] * up + bc[2] * dirv
        w.add_object(p3d, pos, aside, up, dirv)
    src = os.path.join(SMOKE_SRC, "smoke.wrp")
    n = w.write(src)
    print("wrote", src, n, "bytes")
    for f in os.listdir(SMOKE_OUT):
        if f.endswith(".wrp") and f != "utes_roundtrip.wrp":
            os.remove(os.path.join(SMOKE_OUT, f))
    cmd = [BINARIZE, "-always", "-silent", "-binpath=P:\\bin", "P:\\JP\\worlds\\testisland\\_smoke", SMOKE_OUT, "*.wrp"]
    res = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = os.path.join(SMOKE_OUT, "binarize_smoke.log")
    with open(log, "wb") as f:
        f.write((" ".join(cmd) + "\n\n" + res.stdout + "\n" + res.stderr).encode("utf-8"))
    print("binarize exit", res.returncode, "log", log)
    out = os.path.join(SMOKE_OUT, "smoke.wrp")
    if os.path.isfile(out):
        info = wrp8.read_oprw_summary(out)
        print({k: v for k, v in info.items() if k not in ("rvmats",)})
        print("rvmats:", info["rvmats"])
        d = open(out, "rb").read()
        a = wrp8.oprw_objects(d, len(info["models"]), info.get("models_end", 0))
        if a is not None:
            for r in a:
                print("  obj id=%d model=%s pos=%s up_y=%.3f" % (r["id"], info["models"][r["mi"]], r["m"][9:12], r["m"][4]))
    else:
        print("NO OUTPUT")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        roundtrip(sys.argv[1])
    smoke_binarize()
