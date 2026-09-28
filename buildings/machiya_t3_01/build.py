#!/usr/bin/env python3
r"""build.py - Land_JP_Machiya_T3_01 from the recipe (machiya_t3_01.py) to the game.

  python build.py [--no-binarize] [--no-pack]

  1. MLOD (every LOD, Geometry properties + mass) -> out/jp_machiya_t3_01.p3d, staged to src/JP/buildings/machiya/
  2. model.cfg (one bone per leaf; both leaves of a twin door driven by source DoorsTwinN, as vanilla double doors)
     and config.cpp (CfgPatches JP_Buildings, Land_JP_Machiya_T3_01: HouseNoDestruct, class Doors DoorsTwin1-6 with
     the vanilla doorWoodSlide sounds, DamageZones per door) -> CfgConvert syntax check
  3. binarize.exe (cwd P:\) -> ODOL replaces the MLOD copy in src (the MLOD stays in out/)
  4. pack src/JP/buildings (minus model.cfg) -> ..\@Japan\addons\jp_buildings.pbo, prefix JP\buildings
  5. drop-ins: test/placements/C.csv, test/ce/C_mapgroupproto.xml (loot from the Roadway floors, usage Town),
     test/ce/C_mapgrouppos.xml; rooms.json (room tags for the decorator)
  6. verify.py (checks.json)
Never touches the server, the game or any GUI program.
"""
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(DEV, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "tools", "common"))              # pbo.py (read-only, imported)
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))  # B's loot.py (read-only, imported)
import machiya_t3_01 as MT  # noqa: E402
from jpparts import mlod  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

NAME, CLASS = MT.NAME, MT.CLASS
SRC = os.path.join(DEV, "src", "JP", "buildings")
MDIR = os.path.join(SRC, "machiya")
OUT = os.path.join(HERE, "out")
TEMP = os.path.join(DEV, "data", "C", "_build")
PBO_OUT = os.path.join(ROOT, "@Japan", "addons", "jp_buildings.pbo")
PREFIX = "JP\\buildings"
MODEL_PATH = "\\JP\\buildings\\machiya\\%s.p3d" % NAME
TOOLS = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
BINARIZE = os.path.join(TOOLS, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS, "CfgConvert", "CfgConvert.exe")

POS = (1024.0, 25.0, 1045.0)      # README: the building spot, yard ground 25.0
YAW = 180.0                       # front (model +z) faces south, towards the spawn
MASS = 60000.0
SOUND = "doorWoodSlide"


def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text if isinstance(text, bytes) else text.replace("\r\n", "\n").encode("utf-8"))


def copy_retry(src, dst, tries=5):
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


# ------------------------------------------------------------------------------------------------ configs
def model_cfg(doors):
    bones = ",\n".join('\t\t\t"%s",""' % a["bone"] for d in doors for a in d.anims)
    anims = ""
    for k, d in enumerate(doors, 1):
        for a in d.anims:
            anims += ("\t\t\tclass %s\n\t\t\t{\n\t\t\t\ttype=\"translation\";\n\t\t\t\tsource=\"DoorsTwin%d\";\n"
                      "\t\t\t\tselection=\"%s\";\n\t\t\t\taxis=\"%s_axis\";\n\t\t\t\tmemory=1;\n\t\t\t\tminValue=0;\n"
                      "\t\t\t\tmaxValue=1;\n\t\t\t\toffset0=0;\n\t\t\t\toffset1=%.4f;\n\t\t\t};\n"
                      % (a["bone"][0].upper() + a["bone"][1:], k, a["bone"], a["bone"], a["amount"]))
    return ("class CfgSkeletons\n{\n\tclass Default\n\t{\n\t\tisDiscrete=1;\n\t\tskeletonInherit=\"\";\n"
            "\t\tskeletonBones[]={};\n\t};\n\tclass %s_skeleton: Default\n\t{\n\t\tskeletonInherit=\"Default\";\n"
            "\t\tskeletonBones[]=\n\t\t{\n%s\n\t\t};\n\t};\n};\nclass CfgModels\n{\n\tclass Default\n\t{\n"
            "\t\tsectionsInherit=\"\";\n\t\tsections[]={};\n\t\tskeletonName=\"\";\n\t};\n\tclass %s: Default\n\t{\n"
            "\t\tskeletonName=\"%s_skeleton\";\n\t\tclass Animations\n\t\t{\n%s\t\t};\n\t};\n};\n"
            % (NAME, bones, NAME, NAME, anims))


def _armor(t, proj, melee, frag):
    out = ""
    for name, dmg in (("Projectile", proj), ("Melee", melee), ("FragGrenade", frag)):
        out += ("%sclass %s\n%s{\n%s\tclass Health\n%s\t{\n%s\t\tdamage=%s;\n%s\t};\n%s\tclass Blood\n%s\t{\n"
                "%s\t\tdamage=0;\n%s\t};\n%s\tclass Shock\n%s\t{\n%s\t\tdamage=0;\n%s\t};\n%s};\n"
                % (t, name, t, t, t, t, dmg, t, t, t, t, t, t, t, t, t, t))
    return out


def config_cpp(doors):
    dcls = ""
    zones = ""
    for k, d in enumerate(doors, 1):
        dcls += ("\t\t\tclass DoorsTwin%d\n\t\t\t{\n\t\t\t\tdisplayName=\"%s\";\n\t\t\t\tcomponent=\"DoorsTwin%d\";\n"
                 "\t\t\t\tsoundPos=\"doorsTwin%d_action\";\n\t\t\t\tanimPeriod=%g;\n\t\t\t\tinitPhase=0;\n"
                 "\t\t\t\tinitOpened=%g;\n\t\t\t\tsoundOpen=\"%sOpen\";\n\t\t\t\tsoundClose=\"%sClose\";\n"
                 "\t\t\t\tsoundLocked=\"%sRattle\";\n\t\t\t\tsoundOpenABit=\"%sOpenABit\";\n\t\t\t};\n"
                 % (k, getattr(d, "label", "door"), k, k, d.anim_period, d.init_opened, SOUND, SOUND, SOUND, SOUND))
        zones += ("\t\t\t\tclass DoorsTwin%d\n\t\t\t\t{\n\t\t\t\t\tclass Health\n\t\t\t\t\t{\n\t\t\t\t\t\thitpoints=1000;\n"
                  "\t\t\t\t\t\ttransferToGlobalCoef=0;\n\t\t\t\t\t};\n\t\t\t\t\tcomponentNames[]=\n\t\t\t\t\t{\n"
                  "\t\t\t\t\t\t\"doorstwin%d\"\n\t\t\t\t\t};\n\t\t\t\t\tfatalInjuryCoef=-1;\n\t\t\t\t\tclass ArmorType\n"
                  "\t\t\t\t\t{\n%s\t\t\t\t\t};\n\t\t\t\t};\n" % (k, k, _armor("\t" * 6, 3, 5, 10)))
    cls = ("\tclass %s: HouseNoDestruct\n\t{\n\t\tscope=1;\n\t\tdisplayName=\"Machiya (tier 3)\";\n\t\tmodel=\"%s\";\n"
           "\t\tclass Doors\n\t\t{\n%s\t\t};\n"
           "\t\tclass DamageSystem\n\t\t{\n\t\t\tclass GlobalHealth\n\t\t\t{\n\t\t\t\tclass Health\n\t\t\t\t{\n"
           "\t\t\t\t\thitpoints=1000;\n\t\t\t\t};\n\t\t\t};\n\t\t\tclass GlobalArmor\n\t\t\t{\n%s\t\t\t};\n"
           "\t\t\tclass DamageZones\n\t\t\t{\n%s\t\t\t};\n\t\t};\n\t};\n"
           % (CLASS, MODEL_PATH, dcls, _armor("\t" * 4, 0, 0, 0), zones))
    return ("// JP_Buildings - buildings assembled from the JP parts library (japan_dev/buildings/*).\n"
            "// GENERATED by japan_dev/buildings/machiya_t3_01/build.py - edit the generator, not this file.\n"
            "class CfgPatches\n{\n\tclass JP_Buildings\n\t{\n\t\tunits[]={};\n\t\tweapons[]={};\n"
            "\t\trequiredVersion=0.1;\n\t\trequiredAddons[]=\n\t\t{\n\t\t\t\"DZ_Data\",\n"
            "\t\t\t\"DZ_Structures_Residential\",\n\t\t\t\"JP_Common\"\n\t\t};\n\t};\n};\n"
            "class CfgVehicles\n{\n\tclass HouseNoDestruct;\n%s};\n" % cls)


def cfgconvert(path):
    os.makedirs(TEMP, exist_ok=True)
    dst = os.path.join(TEMP, os.path.basename(path) + ".bin")
    r = subprocess.run([CFGCONVERT, "-bin", "-dst", dst, path], capture_output=True, text=True, errors="replace")
    ok = r.returncode == 0 and os.path.isfile(dst)
    print("  CfgConvert %s: %s %s" % (os.path.basename(path), "OK" if ok else "FAILED", (r.stdout + r.stderr).strip()))
    return ok


# ------------------------------------------------------------------------------------------------ steps
def write_model():
    M, floors, rooms = MT.model()
    lods = M.lods(geo_props={"class": "house", "map": "house", "damage": "no", "autocenter": "0"}, mass=MASS)
    os.makedirs(OUT, exist_ok=True)
    mp = os.path.join(OUT, NAME + ".p3d")
    mlod.write_mlod(mp, lods)
    os.makedirs(MDIR, exist_ok=True)
    copy_retry(mp, os.path.join(MDIR, NAME + ".p3d"))
    wb(os.path.join(MDIR, "model.cfg"), model_cfg(M.doors))
    wb(os.path.join(SRC, "config.cpp"), config_cpp(M.doors))
    ok = cfgconvert(os.path.join(SRC, "config.cpp")) and cfgconvert(os.path.join(MDIR, "model.cfg"))
    faces = {mlod.lod_name(l.resolution): len(l.faces) for l in lods}
    print("MLOD %s: %s" % (mp, faces))
    return M, floors, rooms, ok


def binarize():
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\buildings"):
        print(r"binarize: P:\DZ or P:\JP\buildings missing (subst P: D:\DayZToolsExtract; P:\JP junction)")
        return False
    out = os.path.join(TEMP, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\buildings", "-binpath=P:\\bin", "P:\\JP\\buildings\\machiya", out,
           "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = os.path.join(OUT, "binarize.log")
    wb(log, " ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr)
    found = None
    for root_, _, files in os.walk(out):
        if NAME + ".p3d" in files:
            found = os.path.join(root_, NAME + ".p3d")
    bad = [l for l in (r.stdout + r.stderr).splitlines() if re.search(r"error|warning|cannot|not loaded", l, re.I)]
    if found and open(found, "rb").read(4) == b"ODOL":
        copy_retry(found, os.path.join(MDIR, NAME + ".p3d"))
        print("binarize OK: %s (%d bytes), %d warning/error lines in %s" % (NAME, os.path.getsize(found), len(bad), log))
        return True
    print("binarize FAILED - see", log)
    return False


def pack():
    stage = os.path.join(TEMP, "pbo_stage")
    shutil.rmtree(stage, ignore_errors=True)
    shutil.copytree(SRC, stage, ignore=shutil.ignore_patterns("model.cfg", "*.blend", "*.png", "*.log"))
    import pbo
    try:
        pbo.cmd_pack(stage, PBO_OUT, PREFIX)
    except PermissionError as e:
        print("PBO write FAILED (is the Japan test server or the game running? it locks the PBO):", e)
        return False
    print("packed", PBO_OUT, os.path.getsize(PBO_OUT), "bytes")
    return True


def dropins(M, floors, rooms):
    wb(os.path.join(DEV, "test", "placements", "C.csv"), "p3d,x,z,yaw_deg,y_offset\n"
       "JP\\buildings\\machiya\\%s.p3d,%.3f,%.3f,%.1f,0.0\n" % (NAME, POS[0], POS[2], YAW))
    pts = []
    for f in floors:
        for p in bloot.floor_points(f):
            p["tag"] = f["tag"]
            pts.append(p)
    lines = ['\t\t<group name="%s">' % CLASS, '\t\t\t\t<usage name="Town" />', '\t\t\t\t<container name="lootFloor">']
    for c in ("tools", "containers", "clothes", "food"):
        lines.append('\t\t\t\t\t\t<category name="%s" />' % c)
    lines.append('\t\t\t\t\t\t<tag name="floor" />')
    for p in pts:
        lx, ly, lz = bloot.model_to_ce(p["model"])
        lines.append('\t\t\t\t\t\t<point pos="%.6f %.6f %.6f" range="%.6f" height="%.6f" />'
                     % (lx, ly, lz, p["range"], p["height"]))
    lines += ["\t\t\t\t</container>", "\t\t</group>"]
    wb(os.path.join(DEV, "test", "ce", "C_mapgroupproto.xml"), "\n".join(lines) + "\n")
    wb(os.path.join(DEV, "test", "ce", "C_mapgrouppos.xml"),
       '    <group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />\n'
       % (CLASS, POS[0], POS[1], POS[2], YAW, 90.0 - YAW))
    wb(os.path.join(HERE, "rooms.json"), json.dumps({
        "building": CLASS, "p3d": MODEL_PATH, "frame": "model: origin = footprint centre at grade, +z = street front, "
        "+x = the rooms side (the toriniwa is -x); placed at yaw 180 (front south)",
        "rooms": rooms, "loot_points": len(pts),
        "loot_by_room": {r["name"]: sum(1 for p in pts if p["floor"] == r["name"]) for r in rooms}}, indent=1))
    print("drop-ins: C.csv, C_mapgroupproto.xml (%d loot points), C_mapgrouppos.xml, rooms.json" % len(pts))
    return pts


def main(argv):
    M, floors, rooms, ok = write_model()
    if "--no-binarize" not in argv:
        ok = binarize() and ok
    if "--no-pack" not in argv:
        ok = pack() and ok
    pts = dropins(M, floors, rooms)
    import verify
    ok = verify.run(M, floors, pts) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
