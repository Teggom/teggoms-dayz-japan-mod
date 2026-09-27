#!/usr/bin/env python3
r"""build_b.py - turn the kit output into the game-ready jp_structures.pbo and the test drop-in files.

  python build_b.py [--no-binarize] [--no-pack]

Needs the kit to have run first (Blender):  blender --background --python kit/build_building.py -- jp_machiya_01 jp_machiya_02
Steps:
  1. data/B/textures/*.png (make_textures.py) -> src/JP/structures/data/*.paa (ImageToPAA) + one .rvmat per texture set (vanilla Super shader layout)
  2. stage: out/<name>/<name>.p3d (MLOD) -> src/JP/structures/machiya/, model.cfg for all variants next to them
  3. config.cpp (CfgPatches JP_Structures, CfgVehicles Land_JP_*) -> src/JP/structures/config.cpp, checked with CfgConvert
  4. binarize.exe, cwd P:\  -> ODOL p3ds replace the MLOD copies in src (the MLOD stays in out/<name>/)
  5. pack src/JP/structures (minus model.cfg / sources) -> ..\@Japan\addons\jp_structures.pbo, prefix JP\structures
  6. test drop-ins: test/placements/B.csv, test/spawns/B.json, test/ce/B_mapgroupproto.xml, test/ce/B_mapgrouppos.xml
Never touches the server or any GUI program.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, ".."))
DEV = os.path.abspath(os.path.join(B, "..", ".."))
ROOT = os.path.abspath(os.path.join(DEV, ".."))
SRC = os.path.join(DEV, "src", "JP", "structures")
TEX = os.path.join(DEV, "data", "B", "textures")
OUT = os.path.join(B, "out")
TOOLS = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
IMAGE_TO_PAA = os.path.join(TOOLS, "ImageToPAA", "ImageToPAA.exe")
BINARIZE = os.path.join(TOOLS, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS, "CfgConvert", "CfgConvert.exe")
PBO_OUT = os.path.join(ROOT, "@Japan", "addons", "jp_structures.pbo")
TEMP = os.path.join(DEV, "data", "B", "_build")

sys.path.insert(0, os.path.join(B, "kit"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "tools", "common"))      # pbo.py (read-only, imported, not modified)
from jpkit import machiya, cfg, loot  # noqa: E402
from variants import VARIANTS  # noqa: E402

VARIANT_ORDER = ["jp_machiya_01", "jp_machiya_02"]

# placement of the two test instances (README: yard ground = 25.0 m, front facing south = model +z to the south)
GROUND = 25.0
YAW_SOUTH = 180.0
INSTANCES = {
    "baked": (1024.0, 1045.0),
    "spawned": (1075.0, 1090.0),
}

# rvmat specular per texture set: (specular rgb, specularPower)
SPEC = {"jp_plaster_white": (0.15, 30), "jp_plaster_earth": (0.12, 25), "jp_timber_dark": (0.35, 60),
        "jp_boards_floor": (0.35, 60), "jp_boards_ext": (0.2, 40), "jp_kawara": (0.45, 80), "jp_tatami": (0.2, 30),
        "jp_doma": (0.1, 20), "jp_stone": (0.25, 40), "jp_shoji": (0.08, 20), "jp_fusuma": (0.12, 25),
        "jp_plankdoor": (0.2, 40), "jp_koshi": (0.25, 40), "jp_mushiko": (0.12, 25), "jp_tansu": (0.35, 60),
        "jp_ash": (0.05, 10)}

RVMAT = """ambient[]={1,1,1,1};
diffuse[]={1,1,1,1};
forcedDiffuse[]={0,0,0,0};
emmisive[]={0,0,0,1};
specular[]={%(s)g,%(s)g,%(s)g,1};
specularPower=%(p)d;
PixelShaderID="Super";
VertexShaderID="Super";
class Stage1
{
	texture="JP\\structures\\data\\%(t)s_nohq.paa";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage2
{
	texture="#(argb,8,8,3)color(0.5,0.5,0.5,1,DT)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage3
{
	texture="#(argb,8,8,3)color(0,0,0,0,MC)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage4
{
	texture="#(argb,8,8,3)color(1,1,1,1,AS)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage5
{
	texture="JP\\structures\\data\\%(t)s_smdi.paa";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage6
{
	texture="#(ai,64,64,1)fresnel(1.3,0.7)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage7
{
	texture="dz\\data\\data\\env_land_co.paa";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
"""


def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("ascii"))


def textures():
    data = os.path.join(SRC, "data")
    os.makedirs(data, exist_ok=True)
    sets = sorted({f[:-7] for f in os.listdir(TEX) if f.endswith("_co.png")})
    for t in sets:
        for suf in ("_co", "_nohq", "_smdi"):
            png = os.path.join(TEX, t + suf + ".png")
            paa = os.path.join(data, t + suf + ".paa")
            if os.path.isfile(paa) and os.path.getmtime(paa) >= os.path.getmtime(png):
                continue
            res = subprocess.run([IMAGE_TO_PAA, png, paa], capture_output=True, text=True, errors="replace")
            if res.returncode != 0 or not os.path.isfile(paa):
                raise RuntimeError("ImageToPAA failed for %s: %s %s" % (png, res.stdout, res.stderr))
            print("  paa", os.path.basename(paa), os.path.getsize(paa))
        s, p = SPEC.get(t, (0.2, 40))
        wb(os.path.join(data, t + ".rvmat"), RVMAT % {"t": t, "s": s, "p": p})
    print("textures: %d sets" % len(sets))
    return sets


def stage_models():
    mdir = os.path.join(SRC, "machiya")
    os.makedirs(mdir, exist_ok=True)
    models = []
    for name in VARIANT_ORDER:
        src = os.path.join(OUT, name, name + ".p3d")
        if not os.path.isfile(src):
            raise RuntimeError("missing %s - run the Blender kit first" % src)
        _copy_retry(src, os.path.join(mdir, name + ".p3d"))
        models.append(machiya.generate(VARIANTS[name]))
    wb(os.path.join(mdir, "model.cfg"), cfg.modelcfg(models))
    paths = ["\\JP\\structures\\machiya\\%s.p3d" % n for n in VARIANT_ORDER]
    wb(os.path.join(SRC, "config.cpp"), cfg.config_cpp(models, paths))
    # CfgConvert syntax check (writes a throwaway .bin)
    os.makedirs(TEMP, exist_ok=True)
    for f in (os.path.join(SRC, "config.cpp"), os.path.join(mdir, "model.cfg")):
        dst = os.path.join(TEMP, os.path.basename(f) + ".bin")
        res = subprocess.run([CFGCONVERT, "-bin", "-dst", dst, f], capture_output=True, text=True, errors="replace")
        ok = res.returncode == 0 and os.path.isfile(dst)
        print("  CfgConvert %s: %s %s" % (os.path.basename(f), "OK" if ok else "FAILED", (res.stdout + res.stderr).strip()))
        if not ok:
            raise RuntimeError("CfgConvert failed on " + f)
    return models


def _copy_retry(src, dst, tries=5):
    """A freshly written p3d is sometimes briefly locked (virus scanner, another tool reading P:) - retry."""
    import time
    for k in range(tries):
        try:
            shutil.copyfile(src, dst)
            return
        except OSError as e:
            if k == tries - 1:
                raise
            print("  copy retry (%s)" % e)
            time.sleep(2.0)


def binarize():
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\structures"):
        raise RuntimeError(r"P:\DZ or P:\JP\structures missing (subst P: D:\DayZToolsExtract; P:\JP junction)")
    out = os.path.join(TEMP, "binarized")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\structures", "-binpath=P:\\bin", "P:\\JP\\structures\\machiya",
           out, "*.p3d"]
    res = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = os.path.join(B, "out", "binarize.log")
    with open(log, "wb") as f:
        f.write((" ".join(cmd) + "\n\n" + res.stdout + "\n" + res.stderr).replace("\r\n", "\n").encode("utf-8"))
    bad = [l for l in (res.stdout + res.stderr).splitlines()
           if any(k in l for k in ("Error", "error", "Warning", "warning", "not loaded", "Cannot", "cannot"))]
    for l in bad:
        print("  binarize:", l.strip())
    ok = True
    for name in VARIANT_ORDER:
        p = os.path.join(out, name + ".p3d")
        if not os.path.isfile(p):
            # binarize mirrors the input tree under the output folder on some versions
            for root, _, files in os.walk(out):
                if name + ".p3d" in files:
                    p = os.path.join(root, name + ".p3d")
        if os.path.isfile(p) and open(p, "rb").read(4) == b"ODOL":
            _copy_retry(p, os.path.join(SRC, "machiya", name + ".p3d"))
            print("  binarized OK", name, os.path.getsize(p), "bytes")
        else:
            print("  binarize FAILED for", name, "- MLOD left in src (see %s)" % log)
            ok = False
    print("binarize log:", log, "(%d warning/error lines)" % len(bad))
    return ok


def pack():
    stage = os.path.join(TEMP, "pbo_stage")
    if os.path.isdir(stage):
        shutil.rmtree(stage)
    shutil.copytree(SRC, stage, ignore=shutil.ignore_patterns("model.cfg", "*.blend", "*.png", "*.log"))
    import pbo
    try:
        pbo.cmd_pack(stage, PBO_OUT, "JP\\structures")
    except PermissionError as e:
        print("PBO write failed (is the test server running and holding the file?):", e)
        return False
    return True


def dropins(models):
    m01 = models[0]
    name = VARIANT_ORDER[0]
    cls = m01.params["class"]
    # terrain-baked instance (T bakes it into the .wrp); y = ground + y_offset, origin is at ground level
    bx, bz = INSTANCES["baked"]
    # bare data line only (format p3d,x,z,yaw_deg,y_offset); the model origin is at ground level (autocenter=0)
    wb(os.path.join(DEV, "test", "placements", "B.csv"),
       "JP\\structures\\machiya\\%s.p3d,%.3f,%.3f,%.1f,0.0\n" % (name, bx, bz, YAW_SOUTH))
    sx, sz = INSTANCES["spawned"]
    spawn = {"Objects": [{"name": cls, "pos": [sx, GROUND, sz], "ypr": [YAW_SOUTH, 0.0, 0.0], "scale": 1}]}
    wb(os.path.join(DEV, "test", "spawns", "B.json"), json.dumps(spawn, indent=1) + "\n")
    grp, pts = loot.proto_group(m01)
    # bare <group> elements only, as the README asks (explanations live in REPORT.md)
    wb(os.path.join(DEV, "test", "ce", "B_mapgroupproto.xml"), grp)
    a = 90.0 - YAW_SOUTH
    lines = []
    for key in ("baked", "spawned"):
        x, z = INSTANCES[key]
        lines.append('    <group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />'
                     % (cls, x, GROUND, z, YAW_SOUTH, a))
    wb(os.path.join(DEV, "test", "ce", "B_mapgrouppos.xml"), "\n".join(lines) + "\n")
    print("drop-ins written: %d loot points, instances %s" % (len(pts), INSTANCES))


def main(argv):
    textures()
    models = stage_models()
    ok = True
    if "--no-binarize" not in argv:
        ok = binarize() and ok
    if "--no-pack" not in argv:
        ok = pack() and ok
    dropins(models)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
