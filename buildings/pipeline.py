#!/usr/bin/env python3
r"""pipeline.py - the multi-building build (B0 step 0b; replaces the machiya's one-building build.py).

  python buildings/pipeline.py [key ...] [--all] [--no-binarize] [--no-pack] [--no-verify] [--combine-only]

  key ...         the buildings to (re)build (buildings/registry.py keys); default = every shipped building
  --all           every registered building, shipped or not
  --combine-only  rebuild nothing; regenerate the shared outputs from the stored records

Per building (buildings/<key>/):
  1. model() -> MLOD (every LOD, Geometry properties + mass) -> out/<name>.p3d; shipped ones are staged to
     src/JP/buildings/<model_dir>/
  2. record.json: its config class (HouseNoDestruct, class Doors DoorsTwin1-N with the vanilla door sounds,
     DamageZones per door), its model.cfg skeleton + model (one bone per leaf, both leaves of a twin door driven by
     source DoorsTwinN), its loot group (points from the Roadway floors); rooms.json (room tags for the decorator)
Then, from the records of EVERY shipped building (so building N never erases building N-1):
  3. src/JP/buildings/config.cpp and src/JP/buildings/<model_dir>/model.cfg -> CfgConvert syntax check
  4. binarize.exe (cwd P:\) the rebuilt shipped p3ds -> ODOL replaces the MLOD copy in src (the MLOD stays in out/)
  5. pack src/JP/buildings (minus model.cfg) -> ..\@Japan\addons\jp_buildings.pbo, prefix JP\buildings
  6. drop-ins: test/placements/C.csv, test/ce/C_mapgroupproto.xml, test/ce/C_mapgrouppos.xml
  7. checks: the building's own verify.run(M, floors, pts) (checks.json), or the generic checks below
Never touches the server, the game or any GUI program. A running server locks the PBO: the pack step then reports it
and fails; nothing is worked around.
"""
import importlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(DEV, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "tools", "common"))              # pbo.py (read-only, imported)
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))  # B's loot.py (read-only, imported)
import registry  # noqa: E402
from jpparts import mlod  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

SRC = os.path.join(DEV, "src", "JP", "buildings")
TEMP = os.path.join(DEV, "data", "C", "_build")
PBO_OUT = os.path.join(ROOT, "@Japan", "addons", "jp_buildings.pbo")
PREFIX = "JP\\buildings"
TOOLS = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
BINARIZE = os.path.join(TOOLS, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS, "CfgConvert", "CfgConvert.exe")
CONFIG = os.path.join(SRC, "config.cpp")
PLACEMENTS = os.path.join(DEV, "test", "placements", "C.csv")
CE_PROTO = os.path.join(DEV, "test", "ce", "C_mapgroupproto.xml")
CE_POS = os.path.join(DEV, "test", "ce", "C_mapgrouppos.xml")
GEO_PROPS = {"class": "house", "map": "house", "damage": "no", "autocenter": "0"}


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


def bdir(b):
    return os.path.join(HERE, b["key"])


def load_module(b):
    d = bdir(b)
    if d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module(b["module"])


def model_path(b, name):
    return "\\JP\\buildings\\%s\\%s.p3d" % (b["model_dir"], name)


def record_path(b):
    return os.path.join(bdir(b), "record.json")


# ------------------------------------------------------------------------------------------------ config fragments
def skeleton_fragment(name, doors):
    bones = ",\n".join('\t\t\t"%s",""' % a["bone"] for d in doors for a in d.anims)
    return ("\tclass %s_skeleton: Default\n\t{\n\t\tskeletonInherit=\"Default\";\n"
            "\t\tskeletonBones[]=\n\t\t{\n%s\n\t\t};\n\t};\n" % (name, bones))


def cfgmodel_fragment(name, doors):
    anims = ""
    for k, d in enumerate(doors, 1):
        for a in d.anims:
            # translation: axis 1.00 m, offset1 = metres. rotation (windows): angle1 in radians; the engine turns by
            # the RIGHT-hand rule about axis point 1 -> 2 (vanilla vehicle doors; PLAYBOOK §15 T4)
            last = ("offset0=0;\n\t\t\t\toffset1=%.4f;" % a["amount"]) if a["type"] == "translation" else \
                ("angle0=0;\n\t\t\t\tangle1=%.6f;" % a["amount"])
            anims += ("\t\t\tclass %s\n\t\t\t{\n\t\t\t\ttype=\"%s\";\n\t\t\t\tsource=\"DoorsTwin%d\";\n"
                      "\t\t\t\tselection=\"%s\";\n\t\t\t\taxis=\"%s_axis\";\n\t\t\t\tmemory=1;\n\t\t\t\tminValue=0;\n"
                      "\t\t\t\tmaxValue=1;\n\t\t\t\t%s\n\t\t\t};\n"
                      % (a["bone"][0].upper() + a["bone"][1:], a["type"], k, a["bone"], a["bone"], last))
    return ("\tclass %s: Default\n\t{\n\t\tskeletonName=\"%s_skeleton\";\n\t\tclass Animations\n\t\t{\n%s\t\t};\n"
            "\t};\n" % (name, name, anims))


def model_cfg(records):
    """One model.cfg for a model folder: every shipped building in it."""
    return ("class CfgSkeletons\n{\n\tclass Default\n\t{\n\t\tisDiscrete=1;\n\t\tskeletonInherit=\"\";\n"
            "\t\tskeletonBones[]={};\n\t};\n%s};\nclass CfgModels\n{\n\tclass Default\n\t{\n"
            "\t\tsectionsInherit=\"\";\n\t\tsections[]={};\n\t\tskeletonName=\"\";\n\t};\n%s};\n"
            % ("".join(r["skeleton"] for r in records), "".join(r["cfgmodel"] for r in records)))


def _armor(t, proj, melee, frag):
    out = ""
    for name, dmg in (("Projectile", proj), ("Melee", melee), ("FragGrenade", frag)):
        out += ("%sclass %s\n%s{\n%s\tclass Health\n%s\t{\n%s\t\tdamage=%s;\n%s\t};\n%s\tclass Blood\n%s\t{\n"
                "%s\t\tdamage=0;\n%s\t};\n%s\tclass Shock\n%s\t{\n%s\t\tdamage=0;\n%s\t};\n%s};\n"
                % (t, name, t, t, t, t, dmg, t, t, t, t, t, t, t, t, t, t))
    return out


def config_class(b, cls, name, doors):
    dcls = ""
    zones = ""
    snd = b["sound"]
    for k, d in enumerate(doors, 1):
        dcls += ("\t\t\tclass DoorsTwin%d\n\t\t\t{\n\t\t\t\tdisplayName=\"%s\";\n\t\t\t\tcomponent=\"DoorsTwin%d\";\n"
                 "\t\t\t\tsoundPos=\"doorsTwin%d_action\";\n\t\t\t\tanimPeriod=%g;\n\t\t\t\tinitPhase=0;\n"
                 "\t\t\t\tinitOpened=%g;\n\t\t\t\tsoundOpen=\"%sOpen\";\n\t\t\t\tsoundClose=\"%sClose\";\n"
                 "\t\t\t\tsoundLocked=\"%sRattle\";\n\t\t\t\tsoundOpenABit=\"%sOpenABit\";\n\t\t\t};\n"
                 % (k, getattr(d, "label", "door"), k, k, d.anim_period, d.init_opened, snd, snd, snd, snd))
        zones += ("\t\t\t\tclass DoorsTwin%d\n\t\t\t\t{\n\t\t\t\t\tclass Health\n\t\t\t\t\t{\n\t\t\t\t\t\thitpoints=1000;\n"
                  "\t\t\t\t\t\ttransferToGlobalCoef=0;\n\t\t\t\t\t};\n\t\t\t\t\tcomponentNames[]=\n\t\t\t\t\t{\n"
                  "\t\t\t\t\t\t\"doorstwin%d\"\n\t\t\t\t\t};\n\t\t\t\t\tfatalInjuryCoef=-1;\n\t\t\t\t\tclass ArmorType\n"
                  "\t\t\t\t\t{\n%s\t\t\t\t\t};\n\t\t\t\t};\n" % (k, k, _armor("\t" * 6, 3, 5, 10)))
    return ("\tclass %s: HouseNoDestruct\n\t{\n\t\tscope=1;\n\t\tdisplayName=\"%s\";\n\t\tmodel=\"%s\";\n"
            "\t\tclass Doors\n\t\t{\n%s\t\t};\n"
            "\t\tclass DamageSystem\n\t\t{\n\t\t\tclass GlobalHealth\n\t\t\t{\n\t\t\t\tclass Health\n\t\t\t\t{\n"
            "\t\t\t\t\thitpoints=1000;\n\t\t\t\t};\n\t\t\t};\n\t\t\tclass GlobalArmor\n\t\t\t{\n%s\t\t\t};\n"
            "\t\t\tclass DamageZones\n\t\t\t{\n%s\t\t\t};\n\t\t};\n\t};\n"
            % (cls, b["display"], model_path(b, name), dcls, _armor("\t" * 4, 0, 0, 0), zones))


def config_cpp(records):
    # furnished buildings carry proxies of the prop PBOs (B4): require them so they load first
    extra = sorted({a for r in records for a in r.get("proxy_addons", [])})
    req = ["DZ_Data", "DZ_Structures_Residential", "JP_Common"] + extra
    return ("// JP_Buildings - buildings assembled from the JP parts library (japan_dev/buildings/*).\n"
            "// GENERATED by japan_dev/buildings/pipeline.py from buildings/registry.py - edit the generators, not this "
            "file.\n"
            "class CfgPatches\n{\n\tclass JP_Buildings\n\t{\n\t\tunits[]={};\n\t\tweapons[]={};\n"
            "\t\trequiredVersion=0.1;\n\t\trequiredAddons[]=\n\t\t{\n%s\n\t\t};\n\t};\n};\n"
            "class CfgVehicles\n{\n\tclass HouseNoDestruct;\n%s};\n"
            % (",\n".join("\t\t\t\"%s\"" % a for a in req), "".join(r["config_class"] for r in records)))


CONTAINERS = (("lootFloor", None), ("lootshelves", "shelves"))    # vanilla container names; shelves -> tag shelves


def ce_order(pts):
    """Loot points in the order they are written to the CE group: every lootFloor point, then every lootshelves one."""
    return [p for name, _ in CONTAINERS for p in pts if p.get("container", "lootFloor") == name]


def loot_group(b, cls, pts):
    """One CE group: a lootFloor container (the registry's tags) and, when the building has raised points on its
    furniture (B4 decorator), a lootshelves container tagged 'shelves', as vanilla houses have."""
    lo = b["loot"]
    lines = ['\t\t<group name="%s">' % cls]
    lines += ['\t\t\t\t<usage name="%s" />' % u for u in lo["usage"]]
    for cname, ctag in CONTAINERS:
        cp = [p for p in pts if p.get("container", "lootFloor") == cname]
        if not cp and cname != "lootFloor":
            continue
        lines.append('\t\t\t\t<container name="%s">' % cname)
        for c in lo["categories"]:
            lines.append('\t\t\t\t\t\t<category name="%s" />' % c)
        for tg in ([ctag] if ctag else lo["tags"]):
            lines.append('\t\t\t\t\t\t<tag name="%s" />' % tg)
        for p in cp:
            lx, ly, lz = bloot.model_to_ce(p["model"])
            lines.append('\t\t\t\t\t\t<point pos="%.6f %.6f %.6f" range="%.6f" height="%.6f" />'
                         % (lx, ly, lz, p["range"], p["height"]))
        lines.append("\t\t\t\t</container>")
    lines.append("\t\t</group>")
    return lines


def cfgconvert(path):
    os.makedirs(TEMP, exist_ok=True)
    dst = os.path.join(TEMP, os.path.basename(path) + ".bin")
    r = subprocess.run([CFGCONVERT, "-bin", "-dst", dst, path], capture_output=True, text=True, errors="replace")
    ok = r.returncode == 0 and os.path.isfile(dst)
    print("  CfgConvert %s: %s %s" % (os.path.basename(path), "OK" if ok else "FAILED", (r.stdout + r.stderr).strip()))
    return ok


# ------------------------------------------------------------------------------------------------ per building
def build_model(b):
    """Recipe -> MLOD in out/ (and staged into src when shipped), rooms.json, record.json. Returns a build dict."""
    mod = load_module(b)
    name, cls = mod.NAME, mod.CLASS
    M, floors, rooms = mod.model()
    lods = M.lods(geo_props=GEO_PROPS, mass=b["mass"])
    # B4 decorator: a furnished building exposes proxies() (furniture / dressing as proxies in the vanilla LODs),
    # loot_points(floors) (floor + raised points) and site() (yard objects as separate map objects, model frame)
    prox = mod.proxies() if hasattr(mod, "proxies") else []
    from jpparts import proxies as PX
    faces = {mlod.lod_name(l.resolution): len(l.faces) for l in lods}      # without the proxy triangles
    nprox = PX.add(lods, prox) if prox else {}
    out = os.path.join(bdir(b), "out")
    os.makedirs(out, exist_ok=True)
    mp = os.path.join(out, name + ".p3d")
    mlod.write_mlod(mp, lods)
    print("[%s] MLOD %s: %s%s" % (b["key"], mp, faces, ("; proxies %s" % nprox) if nprox else ""))
    if hasattr(mod, "loot_points"):
        pts = ce_order(mod.loot_points(floors))
    else:
        pts = []
        for f in floors:
            for p in bloot.floor_points(f):
                p["tag"] = f["tag"]
                pts.append(p)
    site = mod.site() if hasattr(mod, "site") else []
    wb(os.path.join(bdir(b), "rooms.json"), json.dumps({
        "building": cls, "p3d": model_path(b, name), "frame": getattr(mod, "FRAME_NOTE", "model: origin = footprint "
                                                                       "centre at grade, +z = street front"),
        "rooms": rooms, "loot_points": len(pts),
        "loot_by_room": {r["name"]: sum(1 for p in pts if p["floor"] == r["name"]) for r in rooms}}, indent=1))
    rec = {"key": b["key"], "class": cls, "name": name, "model": model_path(b, name), "model_dir": b["model_dir"],
           "doors": [getattr(d, "label", "door") for d in M.doors], "faces": faces, "loot_points": len(pts),
           "config_class": config_class(b, cls, name, M.doors), "skeleton": skeleton_fragment(name, M.doors),
           "cfgmodel": cfgmodel_fragment(name, M.doors), "loot_group": loot_group(b, cls, pts)}
    if prox:
        rec["proxies"] = nprox
        rec["proxy_addons"] = sorted({"JP_Furniture" if p["p3d"].lower().startswith("\\jp\\furniture") else "JP_Site"
                                      for p in prox})
        rec["loot_containers"] = {c: sum(1 for p in pts if p.get("container", "lootFloor") == c) for c, _ in CONTAINERS}
    if site:
        # yard / street objects in the building's model frame: {p3d, x, z, yaw, y}; combine() turns them into C.csv
        # rows for every placement of the building (baked into the terrain like the building)
        rec["site"] = site
    if b["ship"]:
        mdir = os.path.join(SRC, b["model_dir"])
        os.makedirs(mdir, exist_ok=True)
        copy_retry(mp, os.path.join(mdir, name + ".p3d"))
        wb(record_path(b), json.dumps(rec, indent=1))
    return {"b": b, "mod": mod, "M": M, "floors": floors, "rooms": rooms, "pts": pts, "lods": lods, "rec": rec,
            "mlod": mp}


def binarize(b, name):
    mdir = b["model_dir"]
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir("P:\\JP\\buildings\\" + mdir):
        print(r"binarize: P:\DZ or P:\JP\buildings\%s missing (subst P: D:\DayZToolsExtract; P:\JP junction)" % mdir)
        return False
    out = os.path.join(TEMP, "binarized" if mdir == "machiya" else "binarized_" + mdir)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    others = [f for f in os.listdir(os.path.join(SRC, mdir)) if f.lower().endswith(".p3d") and f != name + ".p3d"]
    mask = (name + ".p3d") if others else "*.p3d"        # a folder shared with other buildings: only this one
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\buildings", "-binpath=P:\\bin", "P:\\JP\\buildings\\" + mdir, out, mask]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = os.path.join(bdir(b), "out", "binarize.log")
    wb(log, " ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr)
    found = None
    for root_, _, files in os.walk(out):
        if name + ".p3d" in files:
            found = os.path.join(root_, name + ".p3d")
    bad = [l for l in (r.stdout + r.stderr).splitlines() if re.search(r"error|warning|cannot|not loaded", l, re.I)]
    if found and open(found, "rb").read(4) == b"ODOL":
        copy_retry(found, os.path.join(SRC, mdir, name + ".p3d"))
        print("binarize OK: %s (%d bytes), %d warning/error lines in %s" % (name, os.path.getsize(found), len(bad), log))
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


# ------------------------------------------------------------------------------------------------ shared outputs
def shipped_records():
    recs = []
    for b in registry.BUILDINGS:
        if not b["ship"]:
            continue
        p = record_path(b)
        if not os.path.isfile(p):
            print("  WARNING: %s is registered but has no record.json yet (build it once); left out" % b["key"])
            continue
        with open(p, "rb") as f:
            recs.append((b, json.loads(f.read().decode("utf-8"))))
    return recs


def combine():
    """config.cpp, every model folder's model.cfg, C.csv and the CE drop-ins from ALL shipped records."""
    recs = shipped_records()
    wb(CONFIG, config_cpp([r for _, r in recs]))
    ok = cfgconvert(CONFIG)
    for mdir in sorted({b["model_dir"] for b, _ in recs}):
        p = os.path.join(SRC, mdir, "model.cfg")
        wb(p, model_cfg([r for b, r in recs if b["model_dir"] == mdir]))
        ok = cfgconvert(p) and ok
    rows, pos, proto = ["p3d,x,z,yaw_deg,y_offset"], [], []
    for b, r in recs:
        proto += r["loot_group"]
        for pl in b["placements"]:
            x, y, z = pl["pos"]
            rows.append("%s,%.3f,%.3f,%.1f,0.0" % (r["model"].lstrip("\\"), x, z, pl["yaw"]))
            pos.append('    <group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />'
                       % (r["class"], x, y, z, pl["yaw"], 90.0 - pl["yaw"]))
            for s in r.get("site", []):
                wx, _, wz = bloot.model_to_world((s["x"], 0.0, s["z"]), pl["pos"], pl["yaw"])
                rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (s["p3d"].lstrip("\\"), wx, wz, (pl["yaw"] + s["yaw"]) % 360.0,
                                                        s.get("y", 0.0)))
    wb(PLACEMENTS, "\n".join(rows) + "\n")
    wb(CE_PROTO, "\n".join(proto) + "\n")
    wb(CE_POS, "\n".join(pos) + "\n")
    print("combined %d shipped building(s): config.cpp, model.cfg, C.csv (%d placements), C_mapgroupproto.xml, "
          "C_mapgrouppos.xml" % (len(recs), len(rows) - 1))
    return ok


# ------------------------------------------------------------------------------------------------ generic checks
def generic_verify(bd):
    """Checks for a building without its own verify.py: LOD set, face budget, closed convex components, library
    materials, the post grid, door sweeps, Roadway at every floor, and the G3 checks (C10-C19)."""
    from jpparts import checks as C, buildcheck as BC
    b, M, floors, mod = bd["b"], bd["M"], bd["floors"], bd["mod"]
    res = []

    def rec(check, ok, detail):
        res.append({"check": check, "ok": bool(ok), "detail": detail})
        print("%-4s %-52s %s" % ("OK" if ok else "FAIL", check, detail))
    lods = mlod.read_mlod(bd["mlod"])
    L = {mlod.lod_name(l.resolution): l for l in lods}
    want = ["Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "Memory", "Roadway", "View Geometry",
            "Fire Geometry"]
    faces = {w: len(L[w].faces) for w in want if w in L}
    rec("C5 LOD set (vanilla house set)", all(w in L for w in want), ", ".join("%s %d" % kv for kv in faces.items()))
    bud = registry.BUDGETS[b["budget"]]
    got = (faces.get("Resolution 1", 0), faces.get("Resolution 2", 0), faces.get("Resolution 3", 0))
    rec("C5 face budget (%s: %d / %d / %d)" % ((b["budget"],) + bud), all(g <= m for g, m in zip(got, bud)),
        "R1 %d, R2 %d, R3 %d" % got)
    for lname in ("Geometry", "View Geometry", "Fire Geometry"):
        l = L[lname]
        comps = [s for s in l.selections if s.startswith("Component")]
        bad = [c for c in comps if mlod.component_report(l, c)]
        covered = set()
        for c in comps:
            covered |= l.selections[c][1]
        rec("C7 %s closed + convex" % lname, not bad and len(covered) == len(l.faces),
            "%d components, %d bad, %d faces outside components" % (len(comps), len(bad), len(l.faces) - len(covered)))
    badm = set()
    for l in lods:
        for _, _, tex, mat in l.faces:
            for pth in (tex, mat):
                if pth and not pth.lower().startswith(C.ALLOWED_VANILLA) and not (
                        pth.lower().startswith("jp\\common\\materials\\") and
                        os.path.isfile(os.path.join(DEV, "src", pth))):
                    badm.add(pth)
    rec("C2 library materials only", not badm, "all library / vanilla" if not badm else "bad: %s" % sorted(badm)[:4])
    posts = getattr(mod, "POSTS", [])
    grid_off = getattr(mod, "GRID_EXEMPT", lambda x, z: False)
    off = [(round(x, 3), round(z, 3)) for (x, z, _, _) in posts
           if not (C.on_grid(x, 0.455) and C.on_grid(z, 0.455)) and not grid_off(x, z)]
    rec("C3 grid snap (post nodes on the 0.455 grid)", not off, "%d posts%s" % (len(posts), "; off-grid %s" % off[:4]
                                                                                if off else ""))
    gcomps = C.components(L["Geometry"])
    for k, d in enumerate(M.doors, 1):
        hits = C.sweep_hits(d, gcomps)
        rec("C7 DoorsTwin%d sweep" % k, not hits, "%s: moves closed -> open without touching other geometry"
            % getattr(d, "label", "") if not hits else "HITS %s" % hits[:3])
    road = L["Roadway"]
    miss = n = 0
    for f in floors:
        x0, x1, z0, z1 = f["rect"]
        for i in range(9):
            for j in range(9):
                x, z = x0 + 0.05 + (x1 - x0 - 0.1) * i / 8, z0 + 0.05 + (z1 - z0 - 0.1) * j / 8
                if any(a0 <= x <= a1 and b0 <= z <= b1 for (a0, a1, b0, b1) in f["obstacles"]):
                    continue
                n += 1
                if not any(abs(h - f["y"]) < 0.02 for h, _ in BC.road_heights(road, x, z)):
                    miss += 1
    rec("C7 walkable floors have Roadway at floor height", not miss, "%d/%d samples" % (n - miss, n))
    BC.run_g3(M, L, floors, rec)
    nf = sum(1 for r in res if not r["ok"])
    wb(os.path.join(bdir(b), "checks.json"), json.dumps({"building": bd["rec"]["class"], "faces": "%d/%d/%d" % got,
                                                          "checks": res}, indent=1))
    print("RESULT %s: %s (%d checks, %d failures)" % (b["key"], "PASS" if not nf else "FAIL", len(res), nf))
    return nf == 0


def run_verify(bd):
    b = bd["b"]
    if b.get("verify"):
        d = bdir(b)
        if d not in sys.path:
            sys.path.insert(0, d)
        # load by path under a per-building name: several buildings each have a verify.py (B4), and
        # importlib.import_module("verify") would hand the second one the first one's cached module
        import importlib.util
        spec = importlib.util.spec_from_file_location("verify_" + b["key"], os.path.join(d, b["verify"] + ".py"))
        v = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(v)
        return v.run(bd["M"], bd["floors"], bd["pts"])
    return generic_verify(bd)


# ------------------------------------------------------------------------------------------------ main
def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    keys = [a for a in argv if not a.startswith("--")]
    if "--combine-only" in flags:
        return 0 if combine() else 1
    if keys:
        todo = [registry.get(k) for k in keys]
    else:
        todo = [b for b in registry.BUILDINGS if b["ship"] or "--all" in flags]
    built = [build_model(b) for b in todo]
    ok = combine() if any(bd["b"]["ship"] for bd in built) else True
    shipped = [bd for bd in built if bd["b"]["ship"]]
    if shipped and "--no-binarize" not in flags:
        for bd in shipped:
            ok = binarize(bd["b"], bd["rec"]["name"]) and ok
    if shipped and "--no-pack" not in flags:
        ok = pack() and ok
    if "--no-verify" not in flags:
        for bd in built:
            ok = run_verify(bd) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
