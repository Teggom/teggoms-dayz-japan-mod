"""Spike A (arms) build: textures -> MLOD p3ds -> binarize -> config check -> PBO.

    python tools/build.py [--no-textures] [--no-binarize] [--no-pack] [--only jp_katana[,jp_yari...]]

--only builds just those parts (and, for jp_katana alone, just the katana textures), so a rebuild of one model
leaves every other p3d and texture byte-identical.

Writes (all inside our own paths):
  src/JP/weapons/data/*            textures (.png kept for renders, skipped by pbo.py) + rvmats
  src/JP/weapons/<part>/*.p3d      binarized ODOL (the MLOD source stays in spikes/A_arms/work/mlod/)
  spikes/A_arms/work/obj/*.obj     OBJ exports for the Blender renders
  ..\\@Japan\\addons\\jp_weapons.pbo  prefix JP\\weapons
Never starts or stops the DayZ server or any GUI tool.
"""
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import meshkit as mk  # noqa: E402
import mlod  # noqa: E402
import models  # noqa: E402

SPIKE = os.path.dirname(HERE)
JAPAN = os.path.dirname(os.path.dirname(SPIKE))
SRC = os.path.join(JAPAN, "src", "JP", "weapons")
WORK = os.path.join(SPIKE, "work")
ADDONS = os.path.join(os.path.dirname(JAPAN), "@Japan", "addons")
BIN = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
BINARIZE = os.path.join(BIN, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(BIN, "CfgConvert", "CfgConvert.exe")


def yumi_bow(detail):
    return models.yumi_bow_variant(detail)


def yumi_xb(detail):
    return models.yumi_xb_variant(detail)


PARTS = {
    # name: (folder, builder(detail) -> mesh | (mesh, info, extra), memory fn, mass kg)
    "jp_katana": ("katana", lambda d: models.build_katana(d), lambda m, i, e: models.katana_memory(m), 1.2),
    "jp_yari": ("yari", lambda d: models.build_yari(d), lambda m, i, e: models.yari_memory(m), 1.6),
    "jp_ya": ("ya", lambda d: models.build_ya(d), lambda m, i, e: models.ya_memory(m), 0.03),
    "jp_yumi": ("yumi", yumi_bow, models.yumi_memory, 0.8),
    "jp_yumi_xb": ("yumi", yumi_xb, models.yumi_memory, 0.8),
}
DETAILS = [(1.0, 1.0), (2.0, 0.5), (4.0, 0.28)]


def build_p3d(name):
    folder, fn, memfn, mass = PARTS[name]
    details = DETAILS
    if name == "jp_katana":                      # katana v2: mass and LOD scheme come from katana_spec.json
        import katana_geom
        bs = katana_geom.load_spec()["build"]
        mass = katana_geom.V(bs["mass_kg"])
        details = [tuple(x) for x in katana_geom.V(bs["lod_details"])]
    lods = []
    first = None
    for res, det in details:
        r = fn(det)
        mesh, info, extra = (r if isinstance(r, tuple) else (r, None, None))
        if first is None:
            first = (mesh, info, extra)
        lods.append(mk.mesh_lod(mesh, res))
    mesh, info, extra = first
    lo, hi = mesh.bounds()
    pad = 0.002
    lo, hi = lo - pad, hi + pad
    if name.startswith("jp_yumi"):
        # physics box around the bow body only (the nocked ya would make it 1 m deep)
        body = np.array([mesh.pts[i] for i in mesh.sel["body"]])
        blo, bhi = body.min(0) - pad, body.max(0) + pad
        boxes = [(tuple(blo), tuple(bhi))]
    else:
        boxes = [(tuple(lo), tuple(hi))]
    lods.append(mk.box_lod(mlod.LOD_GEOMETRY, None, None, mass=mass, props={"autocenter": "0"}, boxes=boxes))
    lods.append(mk.memory_lod(memfn(mesh, info, extra), props={"lodnoshadow": "1"}))
    lods.append(mk.box_lod(mlod.LOD_VIEW_GEOMETRY, None, None, boxes=boxes))
    lods.append(mk.box_lod(mlod.LOD_FIRE_GEOMETRY, None, None, boxes=boxes))
    os.makedirs(os.path.join(WORK, "mlod"), exist_ok=True)
    mlod_path = os.path.join(WORK, "mlod", name + ".p3d")
    mlod.write_mlod(mlod_path, lods)
    # round trip check
    back = mlod.read_mlod(mlod_path)
    assert len(back) == len(lods)
    dst_dir = os.path.join(SRC, folder)
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copyfile(mlod_path, os.path.join(dst_dir, name + ".p3d"))
    export_obj(mesh, os.path.join(WORK, "obj", name + ".obj"))
    print("  %-11s LOD0 %5d pts %5d faces  size %.3f x %.3f x %.3f m  -> %s" % (
        name, len(mesh.pts), len(mesh.faces), *(hi - lo), os.path.relpath(os.path.join(dst_dir, name + ".p3d"), JAPAN)))
    return mesh, info, extra


def export_obj(mesh, path):
    """OBJ for Blender. Mirrors X so the render shows the model as the (left-handed) game does."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mats = {}
    lines = ["mtllib %s" % os.path.basename(path)[:-4] + ".mtl"]
    for p in mesh.pts:
        lines.append("v %.6f %.6f %.6f" % (-p[0], p[1], p[2]))
    vt = []
    vn = []
    face_lines = []
    cur = None
    for f in mesh.faces:
        key = (f["tex"], f["mat"])
        mname = os.path.basename(f["mat"])[:-6] + "__" + os.path.basename(f["tex"])[:-4]
        mats[mname] = f["tex"]
        if mname != cur:
            face_lines.append("usemtl " + mname)
            cur = mname
        ids = []
        for k in range(len(f["v"]))[::-1]:          # mirrored -> reverse to stay CCW-outside
            vt.append(f["uv"][k])
            n = f["n"][k]
            vn.append((-n[0], n[1], n[2]))
            ids.append("%d/%d/%d" % (f["v"][k] + 1, len(vt), len(vn)))
        face_lines.append("f " + " ".join(ids))
    for u, v in vt:
        lines.append("vt %.6f %.6f" % (u, 1.0 - v))
    for n in vn:
        lines.append("vn %.6f %.6f %.6f" % n)
    lines += face_lines
    with open(path, "wb") as fh:
        fh.write(("\n".join(lines) + "\n").encode("ascii"))
    mtl = []
    for mname, tex in mats.items():
        png = os.path.join(JAPAN, "src", tex[:-4].replace("\\", os.sep) + ".png")
        mtl += ["newmtl " + mname, "Kd 1 1 1", "map_Kd " + png.replace("\\", "/"), ""]
    with open(path[:-4] + ".mtl", "wb") as fh:
        fh.write("\n".join(mtl).encode("ascii"))


MODEL_CFG = """class CfgSkeletons
{
	class Default
	{
		isDiscrete = 1;
		skeletonInherit = "";
		skeletonBones[] = {};
	};
};
class CfgModels
{
	class Default
	{
		sectionsInherit = "";
		sections[] = {};
		skeletonName = "";
	};
	class jp_yumi: Default
	{
		sections[] = {"bullet"};
	};
	class jp_yumi_xb: jp_yumi {};
};
"""


def binarize(folder):
    src = os.path.join(SRC, folder)
    temp = os.path.join(WORK, "bin", folder)
    shutil.rmtree(temp, ignore_errors=True)
    os.makedirs(temp)
    rel = os.path.relpath(src, os.path.join(JAPAN, "src")).replace("/", "\\")
    cmd = [BINARIZE, "-always", "-silent", "-addon=P:\\JP\\weapons", "-binpath=P:\\bin", "P:\\" + rel, temp, "*.p3d"]
    res = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = os.path.join(WORK, "binarize_%s.log" % folder)
    with open(log, "wb") as fh:
        fh.write((" ".join(cmd) + "\n\n" + res.stdout + "\n" + res.stderr).encode("utf-8", "replace"))
    ok = True
    for f in os.listdir(src):
        if not f.endswith(".p3d"):
            continue
        out = os.path.join(temp, f)
        if os.path.isfile(out) and open(out, "rb").read(4) == b"ODOL":
            shutil.copyfile(out, os.path.join(src, f))
            print("  binarized %-16s -> ODOL %d bytes" % (f, os.path.getsize(out)))
        else:
            ok = False
            print("  binarize FAILED for %s (see %s)" % (f, log))
    for l in (res.stdout + res.stderr).splitlines():
        if ("rror" in l or "arning" in l) and "No entry" not in l:
            print("   binarize:", l.strip()[:200])
    return ok


def cfgconvert():
    temp = os.path.join(WORK, "cfgcheck")
    os.makedirs(temp, exist_ok=True)
    out = os.path.join(temp, "config.bin")
    if os.path.exists(out):
        os.remove(out)
    res = subprocess.run([CFGCONVERT, "-bin", "-dst", out, os.path.join(SRC, "config.cpp")], capture_output=True, text=True)
    ok = res.returncode == 0 and os.path.isfile(out)
    print("  CfgConvert config.cpp -> bin: %s %s" % ("OK" if ok else "FAILED", (res.stdout + res.stderr).strip()[:400]))
    if ok:
        back = os.path.join(temp, "config_roundtrip.cpp")
        subprocess.run([CFGCONVERT, "-txt", "-dst", back, out], capture_output=True, text=True)
    return ok


def pack():
    sys.path.insert(0, HERE)
    import pbo
    os.makedirs(ADDONS, exist_ok=True)
    out = os.path.join(ADDONS, "jp_weapons.pbo")
    try:
        pbo.cmd_pack(SRC, out, "JP\\weapons")
    except PermissionError as e:
        print("  PBO write failed (server running? it locks PBOs):", e)
        return False
    pbo.cmd_list(out)
    return True


def main(argv):
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\weapons"):
        print("P: drive or P:\\JP\\weapons junction missing")
        return 1
    only = list(PARTS)
    if "--only" in argv:
        only = argv[argv.index("--only") + 1].split(",")
        assert all(n in PARTS for n in only), only
    if "--no-textures" not in argv:
        import katana_textures
        if only != ["jp_katana"]:
            import textures
            textures.main()
        if "jp_katana" in only:
            katana_textures.main()
    print("models:")
    built = {}
    for name in only:
        built[name] = build_p3d(name)
    if any(PARTS[n][0] == "yumi" for n in only):
        with open(os.path.join(SRC, "yumi", "model.cfg"), "wb") as fh:
            fh.write(MODEL_CFG.encode("ascii"))
    ok = True
    if "--no-binarize" not in argv:
        print("binarize:")
        for folder in sorted({PARTS[n][0] for n in only}):
            ok = binarize(folder) and ok
    print("config:")
    ok = cfgconvert() and ok
    if "--no-pack" not in argv:
        print("pack:")
        ok = pack() and ok
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
