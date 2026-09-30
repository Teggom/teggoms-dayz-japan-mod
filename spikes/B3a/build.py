#!/usr/bin/env python3
r"""build.py - B3a interior props, wave 1 (research/interior/BUILD_LIST.md) -> jp_furniture.pbo

  python build.py [prop ...] [--list] [--no-binarize] [--pack]

  prop = a build-list id (jp_f_kama) or a short name (kama); none = every registered prop.
  1. MLOD per model (props_*.py builders) -> spikes/B3a/out/<cat>/<p3d>.p3d          (the masters, regenerated)
  2. checks per model -> spikes/B3a/checks.json (merged: models not rebuilt keep their last result)
  3. sidecar per prop -> src/JP/furniture/<cat>/<prop>.prop.json (loot_surfaces, states, footprints, faces)
  4. config.cpp (CfgPatches JP_Furniture, StaticObj_JP_F_* : HouseNoDestruct, scope 1) + model.cfg, CfgConvert
  5. binarize.exe (cwd P:\): every master MLOD is copied into src/JP/furniture/<cat>/, binarized, and the ODOL
     replaces it there (the MLOD master stays in out/)
  6. --pack: src/JP/furniture (minus sidecars, model.cfg, md) -> ..\@Japan\addons\jp_furniture.pbo
Never starts or stops the server, the game or any GUI program.
"""
import importlib
import json
import math
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
import fkit  # noqa: E402
from fkit import core, mlod  # noqa: E402

PATCH = "JP_Furniture"
PREFIX = "JP\\furniture"
SRC = os.path.join(DEV, "src", "JP", "furniture")
OUT = os.path.join(HERE, "out")
TEMP = os.path.join(HERE, "_build")
PBO_OUT = os.path.join(ROOT, "@Japan", "addons", "jp_furniture.pbo")
TOOLS = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
BINARIZE = os.path.join(TOOLS, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS, "CfgConvert", "CfgConvert.exe")
CHECKS = os.path.join(HERE, "checks.json")
MODULES = ["props_kitchen", "props_heat", "props_storage", "props_bedding", "props_shop", "props_debris"]
BL = {e["id"]: e for e in json.load(open(os.path.join(DEV, "research", "interior", "build_list.json"),
                                         encoding="utf-8"))["entries"]}


def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text if isinstance(text, bytes) else text.replace("\r\n", "\n").encode("utf-8"))


def class_name(p3d):
    """jp_f_kama_nabe_rusted -> StaticObj_JP_F_Kama_Nabe_Rusted (vanilla: StaticObj_Furniture_<name>)."""
    parts = p3d.split("_")[2:]
    return "StaticObj_JP_F_" + "_".join(p[:1].upper() + p[1:] for p in parts)


def registry():
    """[(prop spec, [model spec])]. A props module exposes PROPS = [{id, cat, models: [{p3d, variant, state,
    abandoned, display, build}]}]."""
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
def _sat_overlap(a, b):
    """Penetration depth of two convex point sets along the face normals of both hulls (conservative)."""
    def axes(pts):
        ax = []
        n = len(pts)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    c = core.cross(core.sub(pts[j], pts[i]), core.sub(pts[k], pts[i]))
                    if core.length(c) > 1e-9:
                        c = core.norm(c)
                        d = [core.dot(core.sub(p, pts[i]), c) for p in pts]
                        if min(d) > -1e-6 or max(d) < 1e-6:
                            ax.append(c)
        return ax
    best = 1e9
    for ax in axes(a) + axes(b):
        pa = [core.dot(p, ax) for p in a]
        pb = [core.dot(p, ax) for p in b]
        ov = min(max(pa), max(pb)) - max(min(pa), min(pb))
        if ov <= 0:
            return 0.0
        best = min(best, ov)
    return best


def _ray_down(lod, x, z, y_from):
    """First Resolution face hit going down from (x, y_from, z): (y, face normal y) or None."""
    best = None
    for fv, fl, tex, mat in lod.faces:
        pts = [lod.points[v[0]] for v in fv]
        # point-in-polygon on xz (convex faces)
        sgn = 0
        inside = True
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            c = (b[0] - a[0]) * (z - a[2]) - (b[2] - a[2]) * (x - a[0])
            if abs(c) < 1e-12:
                continue
            s = 1 if c > 0 else -1
            if sgn == 0:
                sgn = s
            elif s != sgn:
                inside = False
                break
        if not inside:
            continue
        n = core.newell(pts)
        if abs(n[1]) < 1e-9:
            continue
        # plane y at (x, z)
        y = pts[0][1] - (n[0] * (x - pts[0][0]) + n[2] * (z - pts[0][2])) / n[1]
        if y <= y_from and (best is None or y > best[0]):
            best = (y, core.norm(n)[1])
    return best


PAL = None
C1_CACHE = {}


def palette_check(mat, wear):
    global PAL
    key = (mat, wear)
    if key in C1_CACHE:
        return C1_CACHE[key]
    from PIL import Image
    import numpy as np
    if PAL is None:
        pal = json.load(open(os.path.join(DEV, "playbook", "palette.json"), encoding="utf-8"))
        ent = pal.get("entries", pal)
        items = ent.items() if isinstance(ent, dict) else [(e.get("id"), e) for e in ent]
        PAL = {k: v for k, v in items if isinstance(v, dict) and "srgb" in v}
    mi = core.mat_info(mat)
    im = Image.open(core.png_path(mat, wear)).convert("RGBA")
    a = np.asarray(im, dtype=float).reshape(-1, 4)
    if mi["alpha"]:
        a = a[a[:, 3] > 127]
    mean = a[:, :3].mean(axis=0)
    pid = mi["palette_id"]
    p = PAL.get(pid)
    if not p:
        r = {"material": mi["id"] + wear, "palette": pid, "pass": None, "note": "no palette entry"}
    else:
        d = de76(mean, p["srgb"])
        r = {"material": mi["id"] + wear, "mean_srgb": [round(float(c), 1) for c in mean], "palette": pid,
             "dE76": round(d, 1), "tolerance": p["tolerance_dE76"], "pass": d <= p["tolerance_dE76"]}
    C1_CACHE[key] = r
    return r


def _srgb_to_lab(rgb):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(float(c)) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116   # noqa: E731
    return (116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z)))


def de76(a, b):
    la, lb = _srgb_to_lab(a), _srgb_to_lab(b)
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5


def bbox_pts(pts):
    return [min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts),
            min(p[2] for p in pts), max(p[2] for p in pts)]


def check_model(P, mp, spec):
    res = []

    def add(cid, name, ok, detail):
        res.append({"id": cid, "name": name, "pass": bool(ok), "detail": detail})

    back = mlod.read_mlod(mp)
    L = {mlod.lod_name(l.resolution): l for l in back}
    add("RT", "MLOD reads back", len(back) > 0, sorted(L))
    r1 = L.get("Resolution 1")
    # C2 library only + C8 era lint on names
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
    banned = [m for m in mats if re.search(r"glass|steel|chrome|plastic|brass|concrete|alu", m, re.I)]
    add("C8", "era lint: no glass / steel / plastic material", not banned, banned)
    # C5 LOD set + budget
    faces = {n: len(l.faces) for n, l in L.items()}
    need = ["Resolution 1", "Resolution 2"] + (["Resolution 3"] if P.res3 else [])
    if not P.flat:
        need += ["Geometry", "View Geometry", "Fire Geometry"]
    extra = [n for n in L if n not in need and n != "Roadway" and not (P.flat and False)]
    budget = fkit.BUDGET[P.budget] if isinstance(P.budget, str) else P.budget
    f1 = faces.get("Resolution 1", 0)
    f2 = faces.get("Resolution 2", 0)
    f3 = faces.get("Resolution 3", 0)
    steps = f2 < f1                 # binarize warns when LODs are not ordered by face count
    if P.res3:
        steps = steps and f3 < f2
    ok = all(n in L for n in need) and not extra and 0 < f1 <= budget and steps and ("Memory" not in L) \
        and (("Roadway" in L) == bool(P.roadway))
    add("C5", "LOD set (%s) + budget Res 1 <= %d, LODs step down" % ("+".join(
        n.replace("Resolution ", "R").replace(" Geometry", "G") for n in need), budget), ok,
        {"faces": faces, "extra": extra, "budget": budget})
    # C4 dimensions
    dd = [dict(d, ok=abs(d["measured"] - d["expected"]) <= d["tol"] + 1e-9) for d in P.dims]
    add("C4", "dimensions against the build list (tol per dim)", all(d["ok"] for d in dd), dd)
    # C6a anchor / base
    vb = bbox_pts(r1.points)
    gb = bbox_pts(L["Geometry"].points) if "Geometry" in L else None
    if P.anchor == "floor":
        ok = -0.002 <= vb[2] <= 0.02 and (gb is None or -0.002 <= gb[2] <= 0.02)
        det = {"res1_min_y": round(vb[2], 4), "geo_min_y": round(gb[2], 4) if gb else None}
    elif P.anchor == "wall":
        ok = -0.002 <= vb[4] <= 0.02 and (gb is None or -0.002 <= gb[4] <= 0.02)
        det = {"res1_min_z (wall plane)": round(vb[4], 4), "geo_min_z": round(gb[4], 4) if gb else None}
    else:
        ok = -0.02 <= vb[3] <= 0.002
        det = {"res1_max_y (hook beam)": round(vb[3], 4)}
    add("C6a", "anchor '%s': base / wall / hook plane within 0-2 cm" % P.anchor, ok, det)
    # Geometry: closed convex components, mass, autocenter
    if "Geometry" in L:
        g = L["Geometry"]
        comps = [n for n in g.selections if n.lower().startswith("component")]
        probs = {n: mlod.component_report(g, n) for n in comps}
        add("GEO", "Geometry: closed convex components, mass, autocenter=0",
            all(not p for p in probs.values()) and abs(sum(g.mass) - P.mass) < 0.01
            and g.properties.get("autocenter") == "0",
            {"components": len(comps), "problems": {k: v for k, v in probs.items() if v}, "mass": round(sum(g.mass), 2)})
        for nm in ("View Geometry", "Fire Geometry"):
            l = L[nm]
            cs = [n for n in l.selections if n.lower().startswith("component")]
            pr = {n: mlod.component_report(l, n) for n in cs}
            add("GEO", "%s components closed + convex" % nm, all(not p for p in pr.values()) and cs,
                {"components": len(cs)})
        # C6b interpenetration between components
        pts = []
        for n in comps:
            pw, fs = g.selections[n]
            pts.append((n, [g.points[i] for i in pw]))
        worst, pair = 0.0, None
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                a, b = bbox_pts(pts[i][1]), bbox_pts(pts[j][1])
                if min(a[1], b[1]) - max(a[0], b[0]) <= 0 or min(a[3], b[3]) - max(a[2], b[2]) <= 0 or \
                        min(a[5], b[5]) - max(a[4], b[4]) <= 0:
                    continue
                d = _sat_overlap(pts[i][1], pts[j][1])
                if d > worst:
                    worst, pair = d, (pts[i][0], pts[j][0])
        add("C6b", "no Geometry interpenetration > 1 cm", worst <= 0.01, {"worst_m": round(worst, 4), "pair": pair})
    # loot surfaces: each point sits on an up-facing Res 1 face at its height; <= 1.40 m (vanilla max)
    lp = []
    ok = True
    for s in P.loot:
        for p in s["points"]:
            hit = _ray_down(r1, p[0], p[2], p[1] + 0.03)
            good = hit is not None and abs(hit[0] - p[1]) <= 0.015 and abs(hit[1]) > 0.7 and p[1] <= 1.40
            ok = ok and good
            lp.append({"surface": s["name"], "point": p, "hit_y": round(hit[0], 4) if hit else None, "ok": good})
    want = spec.get("loot_expected", None)
    if want is not None:
        ok = ok and len(P.loot) >= want
    add("LOOT", "loot points on a Res 1 up-face at their height, <= 1.40 m (%d surfaces)" % len(P.loot), ok, lp)
    # roadway: up-facing
    if "Roadway" in L:
        rw = L["Roadway"]
        up = all(core.norm(core.newell([rw.points[v[0]] for v in fv]))[1] > 0.7 or
                 core.norm(core.newell([rw.points[v[0]] for v in fv]))[1] < -0.7 for fv, *_ in rw.faces)
        add("ROAD", "Roadway faces horizontal, vanilla surface", up, {"faces": len(rw.faces)})
    # C19 matte finish / C1 palette
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
    add("C19", "matte library rvmats have the black env map (glossy ceramics / lacquer / iron exempt)",
        all(c19.values()), c19)
    main = [r for r in c1 if r["material"].endswith("_w1") and r["pass"] is not None]
    add("C1", "palette: the _w1 of every material used within tolerance (_w0/_w2 listed)",
        all(r["pass"] for r in main), c1)
    return res, faces, L


# ================================================================================================ build
def select(reg, argv):
    names = [a for a in argv if not a.startswith("--")]
    if not names:
        return reg
    want = {n if n.startswith("jp_f_") else "jp_f_" + n for n in names}
    sel = [p for p in reg if p["id"] in want]
    missing = want - {p["id"] for p in sel}
    if missing:
        raise SystemExit("unknown prop(s): %s" % sorted(missing))
    return sel


def sidecar(prop, built):
    e = BL.get(prop["id"], {})
    sc = {"id": prop["id"], "build_list": {k: e.get(k) for k in ("name", "importance", "tiers", "room_tags",
                                                              "loot_surface", "abandoned_state", "blocks_path",
                                                              "lod_budget", "dimensions", "refs")},
          "category": prop["cat"], "frame": "origin = base centre on the supporting floor, +y up, +z = front, "
          "autocenter=0 (anchor 'wall': floor below the shelf, wall plane z=0; 'hang': hook-beam underside)",
          "proxy_lods": "Resolution 1, Geometry, View Geometry, Fire Geometry (flat or hanging props: Resolution 1 "
          "only), BUILD_LIST Q5 rule 1", "notes": prop.get("notes", []), "models": []}
    for m, P, faces in built:
        gl = [s for s in P.solids if s.geo]
        fp = None
        if gl:
            xs = [v[0] for s in gl for v in s.verts]
            zs = [v[2] for s in gl for v in s.verts]
            fp = [round(min(xs), 3), round(min(zs), 3), round(max(xs), 3), round(max(zs), 3)]
        vb = P.bbox()
        sc["models"].append({
            "p3d": "\\%s\\%s\\%s.p3d" % (PREFIX, prop["cat"], m["p3d"]), "class": class_name(m["p3d"]),
            "variant": m["variant"], "state": m["state"], "abandoned": m["state"] != "intact",
            "display": m["display"], "anchor": P.anchor, "budget": P.budget, "faces": faces,
            "bbox": [round(v, 3) for v in vb], "collision": not P.flat, "footprint_xz": fp,
            "loot_floor_clearance_m": 0.4 if fp else 0.0, "roadway": bool(P.roadway), "mass_kg": P.mass if not P.flat
            else None, "loot_surfaces": P.loot, "dims": P.dims, "notes": P.notes, **P.extra})
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
            print("%-34s %-10s R1 %4d R2 %4d R3 %4s  %s" % (
                m["p3d"], P.budget, faces.get("Resolution 1", 0), faces.get("Resolution 2", 0),
                faces.get("Resolution 3", "-"), "PASS" if not fails else "FAIL " + ", ".join(
                    "%s(%s)" % (c["id"], json.dumps(c["detail"])[:260]) for c in fails)))
            built.append((m, P, faces))
        wb(os.path.join(SRC, prop["cat"], prop["id"] + ".prop.json"), json.dumps(sidecar(prop, built), indent=1))
    wb(CHECKS, json.dumps(results, indent=1))
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
                "\t};\n" % (class_name(m["p3d"]), m["display"], PREFIX, prop["cat"], m["p3d"]))
    return ("// JP_Furniture - interior props (jp_f_*), placed as proxies inside JP buildings like vanilla\n"
            "// \\dz\\structures\\furniture, plus a StaticObj_JP_F_<name> class each (HouseNoDestruct, scope 1) as vanilla\n"
            "// StaticObj_Furniture_<name>. No script, no vanilla change, no map dependency.\n"
            "// GENERATED by japan_dev/spikes/B3a/build.py - edit the generator, not this file.\n"
            "class CfgPatches\n{\n\tclass %s\n\t{\n\t\tunits[]={};\n\t\tweapons[]={};\n\t\trequiredVersion=0.1;\n"
            "\t\trequiredAddons[]=\n\t\t{\n\t\t\t\"DZ_Data\",\n\t\t\t\"JP_Common\"\n\t\t};\n\t};\n};\n"
            "class CfgVehicles\n{\n\tclass HouseNoDestruct;\n%s};\n" % (PATCH, cls))


def model_cfg(models):
    ms = "".join("\tclass %s: Default\n\t{\n\t};\n" % m["p3d"] for _, m in models)
    return ("class CfgSkeletons\n{\n\tclass Default\n\t{\n\t\tisDiscrete=1;\n\t\tskeletonInherit=\"\";\n"
            "\t\tskeletonBones[]={};\n\t};\n};\nclass CfgModels\n{\n\tclass Default\n\t{\n\t\tsectionsInherit=\"\";\n"
            "\t\tsections[]={};\n\t\tskeletonName=\"\";\n\t};\n%s};\n" % ms)


def cfgconvert(path):
    os.makedirs(TEMP, exist_ok=True)
    dst = os.path.join(TEMP, os.path.basename(path) + ".bin")
    if os.path.exists(dst):
        os.remove(dst)
    r = subprocess.run([CFGCONVERT, "-bin", "-dst", dst, path], capture_output=True, text=True, errors="replace")
    ok = r.returncode == 0 and os.path.isfile(dst)
    if ok:
        r2 = subprocess.run([CFGCONVERT, "-txt", "-dst", dst + ".cpp", dst], capture_output=True, text=True,
                            errors="replace")
        ok = r2.returncode == 0
    return ok, "CfgConvert %s: %s %s" % (os.path.basename(path), "OK" if ok else "FAILED", (r.stdout + r.stderr).strip())


def binarize(models):
    cats = sorted({p["cat"] for p, _ in models})
    for prop, m in models:
        shutil.copyfile(os.path.join(OUT, prop["cat"], m["p3d"] + ".p3d"), os.path.join(SRC, prop["cat"], m["p3d"] + ".p3d"))
    out = os.path.join(TEMP, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    log, lines, rc = "", [], 0
    for cat in cats:        # binarize does not recurse: one run per category folder
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
    print("binarize: %d/%d ODOL, %d warning/error lines (cats %s)" % (len(models) - len(missing), len(models),
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
    glob = {}
    conv = [cfgconvert(os.path.join(SRC, "config.cpp")), cfgconvert(os.path.join(SRC, "model.cfg"))]
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
    wb(CHECKS, json.dumps(results, indent=1))
    for k, v in glob.items():
        print(k, "PASS" if v["pass"] else "FAIL", json.dumps(v["detail"])[:300])
    print("models: %d, all checks pass: %d" % (results["summary"]["models"], results["summary"]["pass"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
