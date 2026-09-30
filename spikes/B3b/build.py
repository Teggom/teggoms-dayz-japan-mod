#!/usr/bin/env python3
r"""build.py - B3b outdoor props, wave 1 (research/outdoor_kit/BUILD_LIST.md, the 20 W1 items) -> jp_site.pbo

  python build.py [item ...] [--list] [--no-binarize] [--pack]

  item = a build-list id (jp_s_oke) or a short name (oke); none = every registered item.
  1. MLOD per model (props_*.py builders) -> spikes/B3b/out/<group>/<p3d>.p3d          (the masters, regenerated)
  2. checks per model -> spikes/B3b/checks.json (merged: models not rebuilt keep their last result)
  3. sidecar per item -> src/JP/site/<group>/<item>.prop.json (states, anchors, footprints, loot, faces, text used)
  4. config.cpp (CfgPatches JP_Site; StaticObj_JP_S_* : HouseNoDestruct, scope 1, like vanilla StaticObj_Misc_*;
     the wells Land_JP_S_Well_* : HouseNoDestruct + a one-line script class 'extends Well', exactly as vanilla
     Land_Misc_Well_Pump_Yellow) + model.cfg + scripts/4_World/JP_Site/jp_site_wells.c; CfgConvert
  5. binarize.exe (cwd P:\): master MLOD copied into src/JP/site/<group>/, binarized, ODOL replaces it there
  6. --pack: src/JP/site (minus sidecars, model.cfg, md) -> ..\@Japan\addons\jp_site.pbo
Built on B3a's pipeline (spikes/B3a: fkit, bits, the check set); B3a's files are imported, never modified.
Never starts or stops the server, the game or any GUI program.
"""
import importlib
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
sys.path.insert(0, os.path.join(DEV, "tools", "common"))
import skit  # noqa: E402
from skit import core, mlod  # noqa: E402
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("b3a_build", os.path.join(DEV, "spikes", "B3a", "build.py"))
B3A = importlib.util.module_from_spec(_spec)   # B3a's check helpers: palette_check, _ray_down, _sat_overlap, bbox_pts
_spec.loader.exec_module(B3A)
B3A.TEMP = os.path.join(HERE, "_build")         # its cfgconvert() writes into TEMP: keep that inside spikes/B3b

PATCH = "JP_Site"
PREFIX = "JP\\site"
SRC = os.path.join(DEV, "src", "JP", "site")
OUT = os.path.join(HERE, "out")
TEMP = os.path.join(HERE, "_build")
PBO_OUT = os.path.join(ROOT, "@Japan", "addons", "jp_site.pbo")
BINARIZE = B3A.BINARIZE
CFGCONVERT = B3A.CFGCONVERT
CHECKS = os.path.join(HERE, "checks.json")
MODULES = ["props_wood", "props_wells", "props_stone", "props_street", "props_straw"]
BL = {e["id"]: e for e in json.load(open(os.path.join(DEV, "research", "outdoor_kit", "build_list.json"),
                                         encoding="utf-8"))["entries"]}
SCRIPT_DIR = "scripts\\4_World\\JP_Site"


def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text if isinstance(text, bytes) else text.replace("\r\n", "\n").encode("utf-8"))


def class_name(m):
    """jp_s_well_tsurube_curb_tub -> Land_JP_S_Well_Tsurube_Curb_Tub (a Well, Land_ + p3d name so a .wrp-baked well
    finds its class, as vanilla Land_Misc_Well_Pump_*); every other model StaticObj_JP_S_<Name> (vanilla
    StaticObj_Misc_*: non-interactive map objects)."""
    parts = m["p3d"].split("_")[2:]
    body = "_".join(p[:1].upper() + p[1:] for p in parts)
    return ("Land_JP_S_" if m.get("well") else "StaticObj_JP_S_") + body


def registry():
    out = []
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
        out += mod.PROPS
    return out


# ================================================================================================ checks
_C1 = {}


def palette_check(mat, wear):
    """B3a's C1 (mean _co/_ca colour vs the palette entry, dE76), plus B1's detail mask: pixels painted as detail
    (<id>_w<n>_mask.png: noren crests, stains, mildew) are left out, exactly as B1's matcheck measured them."""
    key = (mat, wear)
    if key in _C1:
        return _C1[key]
    from PIL import Image
    import numpy as np
    r = dict(B3A.palette_check(mat, wear))
    mp = core.png_path(mat, wear)
    mask = mp[:-7] + "_mask.png"
    if os.path.isfile(mask) and r.get("pass") is not None:
        im = np.asarray(Image.open(mp).convert("RGBA"), dtype=float)
        mk = np.asarray(Image.open(mask).convert("L").resize(im.shape[1::-1], Image.NEAREST)) < 128
        keep = mk & ((im[..., 3] > 127) if core.mat_info(mat)["alpha"] else True)
        mean = im[..., :3][keep].mean(axis=0)
        pal = B3A.PAL[r["palette"]]
        d = B3A.de76(mean, pal["srgb"])
        r.update({"mean_srgb": [round(float(c), 1) for c in mean], "dE76": round(d, 1), "masked": True,
                  "pass": d <= pal["tolerance_dE76"]})
    _C1[key] = r
    return r


def check_model(P, mp, spec):
    res = []

    def add(cid, name, ok, detail):
        res.append({"id": cid, "name": name, "pass": bool(ok), "detail": detail})

    back = mlod.read_mlod(mp)
    L = {mlod.lod_name(l.resolution): l for l in back}
    add("RT", "MLOD reads back", len(back) > 0, sorted(L))
    r1 = L.get("Resolution 1")
    bad, mats = set(), set()
    for n, l in L.items():
        for fv, fl, tex, mat in l.faces:
            if n.startswith("Resolution"):
                mats.add(mat)
                if not (tex.startswith("JP\\common\\materials\\") and mat.startswith("JP\\common\\materials\\")):
                    bad.add((tex, mat))
            elif n == "Fire Geometry" and not mat.startswith("dz\\data\\data\\penetration\\"):
                bad.add(mat)
            elif n == "Roadway" and not tex.startswith("dz\\surfaces\\data\\roadway\\"):
                bad.add(tex)
    add("C2", "library materials only", not bad, {"materials": sorted(mats), "bad": sorted(map(str, bad))})
    # C8 era lint (BUILD_LIST 'Checks'): no glass / metal names except the iron fittings; nothing emissive
    banned = [m for m in mats if re.search(r"glass|steel|chrome|plastic|brass|concrete|alu|emissive|light", m, re.I)]
    emis = []
    for m in mats:
        txt = open(os.path.join(DEV, "src", m.replace("\\", os.sep)), encoding="utf-8").read()
        mm = re.search(r"emmisive\[\]\s*=\s*\{([^}]*)\}", txt)
        if mm and any(float(x) > 0.001 for x in mm.group(1).split(",")[:3]):
            emis.append(m)
    add("C8", "era lint: no glass / steel / plastic material, no emissive rvmat, no metal on ordinary tubs",
        not banned and not emis and not (P.extra.get("no_iron") and any("metal_iron" in m for m in mats)),
        {"banned": banned, "emissive": emis})
    # C5 LOD set + budget
    faces = {n: len(l.faces) for n, l in L.items()}
    need = ["Resolution 1", "Resolution 2"] + (["Resolution 3"] if P.res3 else [])
    for k, nm in (("geo", "Geometry"), ("view", "View Geometry"), ("fire", "Fire Geometry")):
        if k in P.need:
            need.append(nm)
    extra = [n for n in L if n not in need and n != "Roadway"]
    b0, b1, b2 = skit.BUDGET[P.budget]
    f1, f2, f3 = faces.get("Resolution 1", 0), faces.get("Resolution 2", 0), faces.get("Resolution 3", 0)
    steps = f2 < f1 and f2 <= b1
    if P.res3:
        steps = steps and f3 < f2 and f3 <= b2
    ok = all(n in L for n in need) and not extra and 0 < f1 <= b0 and steps and ("Memory" not in L) \
        and (("Roadway" in L) == bool(P.roadway))
    add("C5", "LOD set (%s) + budget %s R1<=%d R2<=%d%s, LODs step down" % ("+".join(
        n.replace("Resolution ", "R").replace(" Geometry", "G") for n in need), P.budget, b0, b1,
        " R3<=%d" % b2 if P.res3 else ""), ok, {"faces": faces, "extra": extra})
    dd = [dict(d, ok=abs(d["measured"] - d["expected"]) <= d["tol"] + 1e-9) for d in P.dims]
    add("C4", "dimensions against the build list (tol per dim)", all(d["ok"] for d in dd) and len(dd) > 0, dd)
    # C6 placement: seated 0-2 cm (or `bury`) into the terrain; wall-backed items `wall_gap` off the wall line
    vb = B3A.bbox_pts(r1.points)
    gb = B3A.bbox_pts(L["Geometry"].points) if "Geometry" in L else None
    hung = getattr(P, "hung", False)
    ok = hung or (-(P.bury + 0.002) <= vb[2] <= 0.002 + 0.02 and (gb is None or -(P.bury + 0.002) <= gb[2] <= 0.03))
    det = {"res1_min_y": round(vb[2], 4), "geo_min_y": round(gb[2], 4) if gb else None, "bury": P.bury, "hung": hung}
    if P.anchor == "wall":
        if hung:      # hung pieces touch the wall at their hooks / bracket (a brace may dip 1.5 cm behind)
            ok = ok and -0.015 <= vb[4] <= 0.15
        else:
            ok = ok and P.wall_gap - 0.002 <= vb[4] <= P.wall_gap + 0.02
        det.update({"res1_min_z (wall plane z=0)": round(vb[4], 4), "wall_gap": P.wall_gap})
    add("C6a", "anchor '%s': base on the terrain (0-2 cm / bury), wall gap" % P.anchor, ok, det)
    if "Geometry" in L:
        g = L["Geometry"]
        comps = [n for n in g.selections if n.lower().startswith("component")]
        probs = {n: mlod.component_report(g, n) for n in comps}
        add("GEO", "Geometry: closed convex components, mass, autocenter=0",
            all(not p for p in probs.values()) and abs(sum(g.mass) - P.mass) < 0.01
            and g.properties.get("autocenter") == "0",
            {"components": len(comps), "problems": {k: v for k, v in probs.items() if v}, "mass": round(sum(g.mass), 2)})
        pts = []
        for n in comps:
            pw, fs = g.selections[n]
            pts.append((n, [g.points[i] for i in pw]))
        worst, pair = 0.0, None
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                a, b = B3A.bbox_pts(pts[i][1]), B3A.bbox_pts(pts[j][1])
                if min(a[1], b[1]) - max(a[0], b[0]) <= 0 or min(a[3], b[3]) - max(a[2], b[2]) <= 0 or \
                        min(a[5], b[5]) - max(a[4], b[4]) <= 0:
                    continue
                d = B3A._sat_overlap(pts[i][1], pts[j][1])
                if d > worst:
                    worst, pair = d, (pts[i][0], pts[j][0])
        add("C6b", "no Geometry interpenetration > 1 cm", worst <= 0.01, {"worst_m": round(worst, 4), "pair": pair})
    for nm in ("View Geometry", "Fire Geometry"):
        if nm in L:
            l = L[nm]
            cs = [n for n in l.selections if n.lower().startswith("component")]
            pr = {n: mlod.component_report(l, n) for n in cs}
            add("GEO", "%s components closed + convex" % nm, all(not p for p in pr.values()) and cs,
                {"components": len(cs)})
    lp = []
    ok = True
    for s in P.loot:
        for p in s["points"]:
            hit = B3A._ray_down(r1, p[0], p[2], p[1] + 0.03)
            good = hit is not None and abs(hit[0] - p[1]) <= 0.015 and abs(hit[1]) > 0.7 and p[1] <= 1.40
            ok = ok and good
            lp.append({"surface": s["name"], "point": p, "hit_y": round(hit[0], 4) if hit else None, "ok": good})
    add("LOOT", "loot points on a Res 1 up-face at their height, <= 1.40 m (%d surfaces)" % len(P.loot), ok, lp)
    if "Roadway" in L:
        rw = L["Roadway"]
        up = all(abs(core.norm(core.newell([rw.points[v[0]] for v in fv]))[1]) > 0.7 for fv, *_ in rw.faces)
        add("ROAD", "Roadway faces horizontal, vanilla surface", up, {"faces": len(rw.faces)})
    c19, c1 = {}, []
    for m in sorted(mats):
        rel = m.replace("\\", os.sep)
        mid = os.path.basename(m)[:-len(".rvmat")]
        key = re.sub(r"_w\d$", "", mid)[5:]
        wear = mid[len("jp_m_" + key):]
        info = core.mat_info(key)
        txt = open(os.path.join(DEV, "src", rel), encoding="utf-8").read()
        if info.get("finish") in ("matte", "wall"):
            c19[mid] = "color(0,0,0,1,CO)" in txt
        c1.append(palette_check(key, wear))
    add("C19", "matte library rvmats have the black env map (iron exempt)", all(c19.values()), c19)
    main = [r for r in c1 if r["material"].endswith("_w1") and r["pass"] is not None]
    add("C1", "palette: the _w1 of every material used within tolerance (_w0/_w2 listed)",
        all(r["pass"] for r in main), c1)
    return res, faces, L


# ================================================================================================ build
def select(reg, argv):
    names = [a for a in argv if not a.startswith("--")]
    if not names:
        return reg
    want = {n if n.startswith("jp_s_") else "jp_s_" + n for n in names}
    sel = [p for p in reg if p["id"] in want]
    missing = want - {p["id"] for p in sel}
    if missing:
        raise SystemExit("unknown item(s): %s" % sorted(missing))
    return sel


def sidecar(prop, built):
    e = BL.get(prop["id"], {})
    sc = {"id": prop["id"], "build_list": {k: e.get(k) for k in ("name", "importance", "tiers", "abandoned_state",
                                                              "placement_rule", "lod_budget", "dimensions", "refs")},
          "group": prop["cat"], "frame": "origin = base centre on the terrain, +y up, +z = front (road side), "
          "autocenter=0; anchor 'wall': the wall plane is z = 0, the object stands wall_gap in front (+z), y = 0 at "
          "the wall foot", "notes": prop.get("notes", []), "models": []}
    for m, P, faces in built:
        gl = [s for s in P.solids if s.geo]
        fp = None
        if gl:
            xs = [v[0] for s in gl for v in s.verts]
            zs = [v[2] for s in gl for v in s.verts]
            fp = [round(min(xs), 3), round(min(zs), 3), round(max(xs), 3), round(max(zs), 3)]
        vb = P.bbox()
        sc["models"].append({
            "p3d": "\\%s\\%s\\%s.p3d" % (PREFIX, prop["cat"], m["p3d"]), "class": class_name(m),
            "variant": m["variant"], "state": m["state"], "abandoned": m["state"] != "intact",
            "display": m["display"], "anchor": P.anchor, "wall_gap": P.wall_gap if P.anchor == "wall" else None,
            "budget": P.budget, "faces": faces, "bbox": [round(v, 3) for v in vb], "collision": list(P.need),
            "footprint_xz": fp, "roadway": bool(P.roadway), "mass_kg": P.mass if "geo" in P.need else None,
            "well": bool(m.get("well")),
            "text_cells": sorted({s.cell for s in P.solids if getattr(s, "cell", None)}), "loot_surfaces": P.loot, "dims": P.dims, "notes": P.notes, **P.extra})
    return sc


def write_all(sel):
    reg = registry()
    results = json.load(open(CHECKS, encoding="utf-8")) if os.path.isfile(CHECKS) else {"models": {}}
    for prop in sel:
        built = []
        for m in prop["models"]:
            P = m["build"]()
            P.pid = m["p3d"]
            lods = P.lods()
            mp = os.path.join(OUT, prop["cat"], m["p3d"] + ".p3d")
            os.makedirs(os.path.dirname(mp), exist_ok=True)
            mlod.write_mlod(mp, lods)
            res, faces, L = check_model(P, mp, m)
            fails = [c for c in res if not c["pass"]]
            results["models"][m["p3d"]] = {"prop": prop["id"], "cat": prop["cat"], "state": m["state"],
                                           "variant": m["variant"], "pass": not fails, "faces": faces, "checks": res}
            print("%-40s %-6s R1 %4d R2 %4d R3 %4s  %s" % (
                m["p3d"], P.budget, faces.get("Resolution 1", 0), faces.get("Resolution 2", 0),
                faces.get("Resolution 3", "-"), "PASS" if not fails else "FAIL " + ", ".join(
                    "%s(%s)" % (c["id"], json.dumps(c["detail"])[:300]) for c in fails)))
            built.append((m, P, faces))
        wb(os.path.join(SRC, prop["cat"], prop["id"] + ".prop.json"), json.dumps(sidecar(prop, built), indent=1,
                                                                                 ensure_ascii=False))
    wb(CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    return reg, results


def built_models(reg):
    out = []
    for prop in reg:
        for m in prop["models"]:
            if os.path.isfile(os.path.join(OUT, prop["cat"], m["p3d"] + ".p3d")):
                out.append((prop, m))
    return out


def config_cpp(models):
    cls = ""
    last = None
    for prop, m in models:
        if prop["id"] != last:
            cls += "\t// %s (%s)\n" % (prop["id"], prop["cat"])
            last = prop["id"]
        cls += ("\tclass %s: HouseNoDestruct\n\t{\n\t\tscope=1;\n\t\tdisplayName=\"%s\";\n\t\tmodel=\"\\%s\\%s\\%s.p3d\";\n"
                "\t};\n" % (class_name(m), m["display"].replace('"', "'"), PREFIX, prop["cat"], m["p3d"]))
    return ("// JP_Site - outdoor site objects (jp_s_*), stage S, B3b wave 1. Map objects: StaticObj_JP_S_<name>\n"
            "// (HouseNoDestruct, scope 1, like vanilla StaticObj_Misc_*); the wells Land_JP_S_Well_* with a one-line\n"
            "// script class 'extends Well' each (drink + wash hands + fill, exactly as vanilla Land_Misc_Well_Pump_*).\n"
            "// Shop-front dressing is meant as proxies on shop buildings; it also has classes for loose placement.\n"
            "// No vanilla change, no map dependency. GENERATED by japan_dev/spikes/B3b/build.py - edit the generator.\n"
            "class CfgPatches\n{\n\tclass %s\n\t{\n\t\tunits[]={};\n\t\tweapons[]={};\n\t\trequiredVersion=0.1;\n"
            "\t\trequiredAddons[]=\n\t\t{\n\t\t\t\"DZ_Data\",\n\t\t\t\"DZ_Scripts\",\n\t\t\t\"JP_Common\"\n\t\t};\n\t};\n};\n"
            "class CfgMods\n{\n\tclass %s\n\t{\n\t\tdir=\"Japan\";\n\t\tpicture=\"\";\n\t\taction=\"\";\n\t\thideName=1;\n"
            "\t\thidePicture=1;\n\t\tname=\"JP Site\";\n\t\tcredits=\"\";\n\t\tauthor=\"japan_dev\";\n\t\tauthorID=\"0\";\n"
            "\t\tversion=\"0.1\";\n\t\textra=0;\n\t\ttype=\"mod\";\n\t\tdependencies[]={\"World\"};\n\t\tclass defs\n\t\t{\n"
            "\t\t\tclass worldScriptModule\n\t\t\t{\n\t\t\t\tvalue=\"\";\n\t\t\t\tfiles[]={\"JP/site/scripts/4_World\"};\n"
            "\t\t\t};\n\t\t};\n\t};\n};\n"
            "class CfgVehicles\n{\n\tclass HouseNoDestruct;\n%s};\n" % (PATCH, PATCH, cls))


def wells_script(models):
    lines = ["// JP_Site wells: vanilla declares one script class per well config (P:\\scripts\\4_world\\entities\\",
             "// building\\residential\\misc\\land_misc_well_pump_yellow.c: 'class Land_Misc_Well_Pump_Yellow extends Well'),",
             "// and Well (4_world\\entities\\building\\well.c) adds ActionDrinkWellContinuous + ActionWashHandsWell and makes",
             "// the object a WELL water source (bottles fill from it). These mirror that for our wells; nothing else.",
             "// GENERATED by japan_dev/spikes/B3b/build.py - edit the generator."]
    for prop, m in models:
        if m.get("well"):
            lines.append("class %s extends Well {};" % class_name(m))
    return "\n".join(lines) + "\n"


def model_cfg(models):
    ms = "".join("\tclass %s: Default\n\t{\n\t};\n" % m["p3d"] for _, m in models)
    return ("class CfgSkeletons\n{\n\tclass Default\n\t{\n\t\tisDiscrete=1;\n\t\tskeletonInherit=\"\";\n"
            "\t\tskeletonBones[]={};\n\t};\n};\nclass CfgModels\n{\n\tclass Default\n\t{\n\t\tsectionsInherit=\"\";\n"
            "\t\tsections[]={};\n\t\tskeletonName=\"\";\n\t};\n%s};\n" % ms)


def binarize(models):
    cats = sorted({p["cat"] for p, _ in models})
    for prop, m in models:
        os.makedirs(os.path.join(SRC, prop["cat"]), exist_ok=True)
        shutil.copyfile(os.path.join(OUT, prop["cat"], m["p3d"] + ".p3d"), os.path.join(SRC, prop["cat"], m["p3d"] + ".p3d"))
    out = os.path.join(TEMP, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    log, lines, rc = "", [], 0
    for cat in cats:
        cmd = [BINARIZE, "-always", "-addon=P:\\" + PREFIX, "-binpath=P:\\bin", "P:\\%s\\%s" % (PREFIX, cat),
               os.path.join(out, cat), "*.p3d"]
        r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
        log += " ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr + "\n"
        lines += (r.stdout + r.stderr).splitlines()
        rc = rc or r.returncode
    wb(os.path.join(HERE, "binarize.log"), log)
    noise = (r"^Warning: Terrain grid", r"^Warning: CfgVehicles missing in PreloadConfig", r"^Trying to access error value")
    bad = [l for l in lines if re.search(r"error|warning|cannot|not loaded|missing", l, re.I)
           and not any(re.search(n, l) for n in noise)]
    found = {}
    for root_, _, files in os.walk(out):
        for f in files:
            if f.endswith(".p3d"):
                found[f[:-4]] = os.path.join(root_, f)
    missing = []
    for prop, m in models:
        f = found.get(m["p3d"])
        if f and open(f, "rb").read(4) == b"ODOL":
            shutil.copyfile(f, os.path.join(SRC, prop["cat"], m["p3d"] + ".p3d"))
        else:
            missing.append(m["p3d"])
    print("binarize: %d/%d ODOL, %d warning/error lines (groups %s)" % (len(models) - len(missing), len(models),
                                                                         len(bad), cats))
    for l in bad[:15]:
        print("   ", l)
    return not missing and not bad, {"missing": missing, "warning_lines": bad, "exit": rc}


def pack():
    stage = os.path.join(TEMP, "pbo_stage")
    shutil.rmtree(stage, ignore_errors=True)
    shutil.copytree(SRC, stage, ignore=shutil.ignore_patterns("model.cfg", "*.json", "*.md", "*.png", "*.log"))
    import pbo
    try:
        pbo.cmd_pack(stage, PBO_OUT, PREFIX)
        return True, PBO_OUT
    except PermissionError as e:
        print("PBO write to @Japan FAILED (locked by a running server/game?):", e)
        return False, str(e)


def main(argv):
    reg = registry()
    if "--list" in argv:
        for p in reg:
            print(p["id"], p["cat"], [m["p3d"] for m in p["models"]])
        return 0
    sel = select(reg, argv)
    reg, results = write_all(sel)
    models = built_models(reg)
    wb(os.path.join(SRC, "config.cpp"), config_cpp(models))
    wb(os.path.join(SRC, "model.cfg"), model_cfg(models))
    wb(os.path.join(SRC, SCRIPT_DIR, "jp_site_wells.c"), wells_script(models))
    glob = {}
    conv = [B3A.cfgconvert(os.path.join(SRC, "config.cpp")), B3A.cfgconvert(os.path.join(SRC, "model.cfg"))]
    glob["CFG"] = {"pass": all(c[0] for c in conv), "detail": [c[1] for c in conv]}
    if "--no-binarize" not in argv:
        ok, det = binarize(models)
        glob["BIN"] = {"pass": ok, "detail": det}
    if "--pack" in argv:
        ok, det = pack()
        glob["PBO"] = {"pass": ok, "detail": det}
        print("packed:", ok, det)
    results["global"] = glob
    results["summary"] = {"models": len(results["models"]),
                          "pass": sum(1 for r in results["models"].values() if r["pass"])}
    wb(CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    for k, v in glob.items():
        print(k, "PASS" if v["pass"] else "FAIL", json.dumps(v["detail"])[:300])
    print("models: %d, all checks pass: %d" % (results["summary"]["models"], results["summary"]["pass"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
