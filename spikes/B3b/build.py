#!/usr/bin/env python3
r"""build.py - B3b outdoor props, wave 1 (research/outdoor_kit/BUILD_LIST.md, the 20 W1 items) -> jp_site.pbo

  python build.py [item ...] [--list] [--no-binarize] [--pack]

  item = a build-list id (jp_s_oke) or a short name (oke); none = every registered item.
  1. MLOD per model (props_*.py builders) -> spikes/B3b/out/<group>/<p3d>.p3d          (the masters, regenerated)
  2. checks per model -> spikes/B3b/checks.json (merged: models not rebuilt keep their last result)
  3. sidecar per item -> src/JP/site/<group>/<item>.prop.json (states, anchors, footprints, loot, faces, text used)
  4. config (CA1, 2026-10-01): B3b's OWN classes (StaticObj_JP_S_* : HouseNoDestruct, scope 1, like vanilla
     StaticObj_Misc_*; the wells Land_JP_S_Well_* : HouseNoDestruct + a one-line script class 'extends Well', exactly
     as vanilla Land_Misc_Well_Pump_Yellow), model.cfg entries and well script lines -> src/JP/site/_frags/B3b.json;
     tools/assemble_config.py merges every builder's fragment (B3b, L2, ...) into config.cpp + model.cfg +
     scripts/4_World/JP_Site/jp_site_wells.c; CfgConvert. A B3b rebuild no longer drops L2's classes.
  5. binarize.exe (cwd P:\): master MLOD copied into src/JP/site/<group>/, binarized, ODOL replaces it there
  6. --pack: assemble, then src/JP/site (minus sidecars, model.cfg, md, _frags) -> ..\@Japan\addons\jp_site.pbo
  --config-only: no model build, no binarize: rewrite this builder's fragment from the masters in out/ + assemble
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
W2_CATS = {"shrine", "grave"}                          # W2 (2026-09-30): the wave-2 folders
MODULES = ["props_wood", "props_wells", "props_stone", "props_street", "props_straw",
           "props_torii", "props_shrine", "props_grave",       # W2 (2026-09-30): the 7 wave-2 items
           "props_torii_fallen",                               # FP1 (2026-10-01): collapsed torii
           "props_guardian"]                                   # FX2 (2026-10-01): komainu + kitsune pairs
OWN_MODULES = tuple(MODULES)   # CA1: B3b's fragment = these modules only (L2 appends its own to MODULES)
PBO = "jp_site"
ASM = B3A.ASM                  # tools/assemble_config.py (CA1)
BL = {e["id"]: e for e in json.load(open(os.path.join(DEV, "research", "outdoor_kit", "build_list.json"),
                                         encoding="utf-8"))["entries"]}
SCRIPT_DIR = "scripts\\4_World\\JP_Site"
# F1 (G4 walk: the well gave no drink / wash / fill action). A .wrp-baked object only becomes an entity of its
# Land_<p3d> config class (and so gets the script class 'extends Well' with its actions) when its Geometry LOD carries the
# named property class=house, as every JP building has and vanilla misc_well_pump_yellow.p3d has (class=house,
# map=waterpump; read from the ODOL). Our wells had only autocenter=0: the engine made them plain static objects.
WELL_GEO = {"class": "house", "map": "waterpump"}
# TEMPORARY DIAGNOSTIC (F1, 2026-09-30) - REMOVE after the next well test: every well script class prints one line
# '[JPWell] <type> at <pos> IsWell=<0|1>' to the script log (server and client) from DeferredInit (EntityAI calls it
# 34 ms after creation), so the log shows whether the map wells are created as our Well classes. Set False and rebuild
# (python spikes/B3b/build.py wells --pack; CA1: the assembler keeps L2's classes) to remove it.
WELL_DIAG = False  # C1 2026-09-30: the well passed in game (G4 re-walk), diagnostic removed


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
    # FP1 (2026-10-01): a model flagged land=True (the climbable fire-watch ladder) is a Land_ class too, so the
    # .wrp-baked object binds to it as a Building (its Geometry carries class=house, set by the builder)
    return ("Land_JP_S_" if (m.get("well") or m.get("land")) else "StaticObj_JP_S_") + body


def registry():
    out = []
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
        for p in mod.PROPS:
            p["_module"] = m          # CA1: which builder's fragment a prop belongs to
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
    if getattr(P, "keep_memory", False):                 # FP1: a climbable ladder carries its Memory points
        need.append("Memory")
    extra = [n for n in L if n not in need and n != "Roadway"]
    b0, b1, b2 = skit.BUDGET[P.budget]
    f1, f2, f3 = faces.get("Resolution 1", 0), faces.get("Resolution 2", 0), faces.get("Resolution 3", 0)
    steps = f2 < f1
    if P.res3:
        steps = steps and f3 < f2
    # CA1: budgets via fkit.budget_fit: a deliberate overage (P.over_budget_ok, <= +50 %) passes and is reported
    fits, over = skit.budget_fit(P, (f1, f2, f3) if P.res3 else (f1, f2), (b0, b1, b2) if P.res3 else (b0, b1))
    ok = all(n in L for n in need) and not extra and 0 < f1 and fits and steps and (("Memory" not in L) or getattr(P, "keep_memory", False)) \
        and (("Roadway" in L) == bool(P.roadway))
    det = {"faces": faces, "extra": extra}
    if over:
        det["over_budget"] = over
    add("C5", "LOD set (%s) + budget %s R1<=%d R2<=%d%s, LODs step down" % ("+".join(
        n.replace("Resolution ", "R").replace(" Geometry", "G") for n in need), P.budget, b0, b1,
        " R3<=%d" % b2 if P.res3 else ""), ok, det)
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
        mount = m.get("mount") or prop.get("mount")      # W2: where the decorator may put it (decor.OUTDOOR_MOUNTS)
        if mount and prop["cat"] in W2_CATS:             # (L2's wrapper writes its own mount / master)
            sc["models"][-1]["mount"] = mount
            sc["models"][-1]["master"] = os.path.relpath(os.path.join(OUT, prop["cat"], m["p3d"] + ".p3d"),
                                                         DEV).replace("\\", "/")
    return sc


def txt_check(mp):
    """L2's TXT check (spikes/L2/textface.py, imported read-only): every text decal faces out of its host and reads
    left to right in game. Models without text pass with 0 faces."""
    sys.path.insert(0, os.path.join(DEV, "spikes", "L2"))
    import textface
    r = textface.check_file(mp)
    bad = [x for x in r if not (x["reads"] and x["host_behind"])]
    return {"id": "TXT", "name": "text decals face out of their host and read left to right in game (%d faces)" % len(r),
            "pass": not bad, "detail": bad[:4]}


def write_all(sel):
    reg = registry()
    results = json.load(open(CHECKS, encoding="utf-8")) if os.path.isfile(CHECKS) else {"models": {}}
    for prop in sel:
        built = []
        for m in prop["models"]:
            P = m["build"]()
            if m.get("well"):
                P.geo_props = dict(WELL_GEO)             # F1: class=house so the .wrp object binds to its Land_ class
            skit.face_text(P.solids, mirror_u=True)      # L2 text fix: face out + read right in game (skit.py)
            P.pid = m["p3d"]
            lods = P.lods()
            mp = os.path.join(OUT, prop["cat"], m["p3d"] + ".p3d")
            os.makedirs(os.path.dirname(mp), exist_ok=True)
            mlod.write_mlod(mp, lods)
            res, faces, L = check_model(P, mp, m)
            res.append(txt_check(mp))                    # W2: L2's TXT check (spikes/L2/textface.py) on every model
            for fn in getattr(P, "checks_extra", []):    # W2: item-specific checks (C7 on the stone steps)
                res.append(fn(P, L))
            fails = [c for c in res if not c["pass"]]
            results["models"][m["p3d"]] = {"prop": prop["id"], "cat": prop["cat"], "state": m["state"],
                                           "variant": m["variant"], "pass": not fails, "faces": faces, "checks": res}
            print("%-40s %-6s R1 %4d R2 %4d R3 %4s  %s" % (
                m["p3d"], P.budget, faces.get("Resolution 1", 0), faces.get("Resolution 2", 0),
                faces.get("Resolution 3", "-"), ("PASS" + B3A.over_note(res)) if not fails else "FAIL " + ", ".join(
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


def frag_classes(models):
    """CA1: config entries for tools/assemble_config.py (the old config_cpp() class text, one dict per model)."""
    return [{"group": "%s (%s)" % (prop["id"], prop["cat"]), "class": class_name(m), "base": "HouseNoDestruct",
             "body": ["scope=1;", "displayName=\"%s\";" % m["display"].replace('"', "'"),
                      "model=\"\\%s\\%s\\%s.p3d\";" % (PREFIX, prop["cat"], m["p3d"])]} for prop, m in models]


def write_fragment(models, builder="B3b", writer="spikes/B3b/build.py", order=10):
    """CA1: write THIS builder's fragment (its own classes, model.cfg entries and well script lines), then assemble
    jp_site's config.cpp + model.cfg + jp_site_wells.c from every builder's fragment."""
    ASM.write_fragment(PBO, builder, writer, order, frag_classes(models), [m["p3d"] for _, m in models],
                       required=("DZ_Data", "DZ_Scripts", "JP_Common"),
                       scripts={SCRIPT_DIR + "\\jp_site_wells.c": well_blocks(models)})
    return ASM.assemble(PBO)


def own_models(models):
    """B3b's (+ W2 / FP1 / FX2 modules registered in MODULES) models: the props of OWN_MODULES."""
    return [(p, m) for p, m in models if p.get("_module") in OWN_MODULES]


def well_blocks(models):
    """CA1: the script blocks (one per well; WELL_DIAG adds a comment block) for the wells among <models>; the
    assembler adds the file header and joins them with newlines, as the old wells_script() did."""
    lines = []
    if WELL_DIAG and any(m.get("well") for _, m in models):
        lines += ["//", "// F1 TEMPORARY DIAGNOSTIC (2026-09-30) - REMOVE after the next well test (spikes/B3b/build.py WELL_DIAG).",
                  "// Prints '[JPWell] <type> at <pos> IsWell=<0|1>' once per well from DeferredInit."]
    if lines:
        lines = ["\n".join(lines)]                       # one block (the assembler keeps identical blocks once)
    for prop, m in models:
        if not m.get("well"):
            continue
        cn = class_name(m)
        if not WELL_DIAG:
            lines.append("class %s extends Well {};" % cn)
            continue
        lines.append("\n".join(["class %s extends Well" % cn, "{",
                  "\tprotected bool m_JPWellDiagDone; // F1 TEMP DIAGNOSTIC - remove",
                  "\toverride void DeferredInit() // F1 TEMP DIAGNOSTIC - remove",
                  "\t{",
                  "\t\tsuper.DeferredInit();",
                  "\t\tif (m_JPWellDiagDone)",
                  "\t\t\treturn;",
                  "\t\tm_JPWellDiagDone = true;",
                  "\t\tstring w = \"0\";",
                  "\t\tif (IsWell())",
                  "\t\t\tw = \"1\";",
                  "\t\tPrint(\"[JPWell] \" + GetType() + \" at \" + GetPosition().ToString() + \" IsWell=\" + w);",
                  "\t}",
                  "};"]))
    return lines


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
    """CA1: assemble every builder's fragment first, then pack (tools/assemble_config.pack). Every jp_site packer
    (L2, FP1 / FP2 pack.py) comes through here."""
    return ASM.pack(PBO, stage=os.path.join(TEMP, "pbo_stage"))


def main(argv):
    reg = registry()
    if "--list" in argv:
        for p in reg:
            print(p["id"], p["cat"], [m["p3d"] for m in p["models"]])
        return 0
    if "--config-only" in argv:     # CA1: re-emit the fragment from the masters in out/ + assemble (+ --pack)
        asm = write_fragment(own_models(built_models(reg)))
        ok = all(B3A.cfgconvert(os.path.join(SRC, f))[0] for f in ("config.cpp", "model.cfg"))
        print("CFG", "PASS" if ok else "FAIL", "; classes in config.cpp: %d" % asm["classes"])
        if "--pack" in argv:
            print("packed:", *pack())
        return 0 if ok else 1
    sel = select(reg, argv)
    reg, results = write_all(sel)
    models = built_models(reg)
    asm = write_fragment(own_models(models))
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
    print("models: %d, all checks pass: %d; classes in config.cpp (all builders): %d" % (
        results["summary"]["models"], results["summary"]["pass"], asm["classes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
