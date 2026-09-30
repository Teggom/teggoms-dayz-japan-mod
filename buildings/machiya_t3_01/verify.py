#!/usr/bin/env python3
r"""verify.py - offline checks of Land_JP_Machiya_T3_01 (verify_b.py's checks, the parts kit's C2/C3/C5/C7, PLAYBOOK
§12), run on the MLOD read back from out/ and the ODOL in src. Writes checks.json. Usually called by build.py.

  python verify.py
"""
import json
import math
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))
import machiya_t3_01 as MT  # noqa: E402
from jpparts import mlod, checks as C, core, raycheck as RC, buildcheck as BC  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

BUDGET = {"Resolution 1": 12000, "Resolution 2": 4600, "Resolution 3": 1600}   # PLAYBOOK §12 large / landmark
POS, YAW = (1024.0, 25.0, 1045.0), 180.0
RES = []


def rec(check, ok, detail):
    RES.append({"check": check, "ok": bool(ok), "detail": detail})
    print("%-4s %-52s %s" % ("OK" if ok else "FAIL", check, detail))


def geo_top_below(comps, x, y, z):
    best = None
    for c in comps:
        if c["door"]:
            continue
        r = C.ray_y(c, x, z)
        if r and r[1] <= y + 0.05 and (best is None or r[1] > best):
            best = r[1]
    return best


def geo_bottom_above(comps, x, y, z):
    best = None
    for c in comps:
        if c["door"]:
            continue
        r = C.ray_y(c, x, z)
        if r and r[0] >= y + 0.05 and (best is None or r[0] < best):
            best = r[0]
        elif r and r[0] < y + 0.05 < r[1]:
            return y
    return best


def road_heights(road, x, z):
    hs = []
    for verts, _, tex, _ in road.faces:
        pts = [road.points[v[0]] for v in verts]
        if C._in_poly_xz(pts, x, z):
            n = mlod._face_formula_normal(pts)
            if abs(n[1]) < 1e-9:
                continue
            p0 = pts[0]
            hs.append((p0[1] - (n[0] * (x - p0[0]) + n[2] * (z - p0[2])) / n[1], tex))
    return hs


def door_world(d, gcomps):
    """Leaf sweeps + open clear width + head in world space; works for walls along x or z."""
    bones = [a["bone"] for a in d.anims]
    others = [c for c in gcomps if c["door"] not in bones]
    hits, opened = [], []
    for a in d.anims:
        leaf = [c for c in gcomps if c["door"] == a["bone"]]
        if not leaf:
            return False, "no Geometry leaf for %s" % a["bone"], None
        dv = [a["axis"][1][k] - a["axis"][0][k] for k in range(3)]
        amt = a["amount"]
        lb = [c["bbox"] for c in leaf]
        bb = [min(b[0] for b in lb), max(b[1] for b in lb), min(b[2] for b in lb), max(b[3] for b in lb),
              min(b[4] for b in lb), max(b[5] for b in lb)]
        sw = (min(bb[0], bb[0] + dv[0] * amt) + 0.004, max(bb[1], bb[1] + dv[0] * amt) - 0.004, bb[2] + 0.004,
              bb[3] - 0.004, min(bb[4], bb[4] + dv[2] * amt) + 0.004, max(bb[5], bb[5] + dv[2] * amt) - 0.004)
        hits += [c["name"] for c in others if C.comp_box_intersect(c, sw)]
        opened += [C.shifted(c, dv[0] * amt, dv[1] * amt, dv[2] * amt) for c in leaf]
    obst = others + opened
    ax = d.action
    dv = [d.anims[0]["axis"][1][k] - d.anims[0]["axis"][0][k] for k in range(3)]
    along_x = abs(dv[0]) > 0.5
    y0 = ax[1] - 1.0
    # the action point is on the leaves' face (post face); the doorway centre line is the wall line 0.06 behind it
    zc = ax[2]
    xc = ax[0]
    lz = [c["bbox"] for c in gcomps if c["door"] in bones]
    if along_x:
        wall = zc - math.copysign(0.06, ((lz[0][4] + lz[0][5]) / 2) - zc) if lz else zc
    else:
        wall = xc - math.copysign(0.06, ((lz[0][0] + lz[0][1]) / 2) - xc) if lz else xc

    def col(s):
        if along_x:
            return (s - 0.004, s + 0.004, y0 + 0.05, y0 + 1.95, wall - 0.35, wall + 0.35)
        return (wall - 0.35, wall + 0.35, y0 + 0.05, y0 + 1.95, s - 0.004, s + 0.004)

    def free(s):
        return not any(C.comp_box_intersect(c, col(s), 0.0) for c in obst)
    c0 = xc if along_x else zc
    if not free(c0):
        return False, "doorway centre blocked (sweep hits %s)" % hits[:3], None
    lo = hi = c0
    while free(lo - 0.01) and lo > c0 - 3:
        lo -= 0.01
    while free(hi + 0.01) and hi < c0 + 3:
        hi += 0.01
    clear = hi - lo
    head = 99.0
    for c in obst:
        b = c["bbox"]
        inside = (b[0] < hi and b[1] > lo and b[4] < wall + 0.3 and b[5] > wall - 0.3) if along_x else \
            (b[4] < hi and b[5] > lo and b[0] < wall + 0.3 and b[1] > wall - 0.3)
        if inside and b[2] > y0 + 0.5:
            head = min(head, b[2] - y0)
    ok = not hits and clear >= 1.0 - 1e-6 and head >= 2.0 - 0.005
    return ok, "leaves slide %s m %s; open clear %.2f m, head %.2f m" % (
        "/".join("%.2f" % a["amount"] for a in d.anims), "without touching other geometry" if not hits else
        "HITS %s" % hits[:3], clear, head), clear


def run(M=None, floors=None, pts=None, name=None, cls=None, here=None, extra=None):
    """The 78 machiya checks. B4: the furnished variant (buildings/machiya_t3_01_shop) runs them too, on its own MLOD /
    ODOL / config class (name, cls, here), with its proxy triangles stripped from the LODs before any geometry check;
    extra(M, L, floors, pts, rec, raw_lods) then adds the decorator checks. Loot: the Roadway / range check applies
    to the floor points (no 'prop'); the CE check compares every point, in CE order."""
    from jpparts import proxies as PX
    del RES[:]
    name, cls, here = name or MT.NAME, cls or MT.CLASS, here or HERE
    if M is None:
        M, floors, _ = MT.model()
    if pts is None:
        pts = []
        for f in floors:
            pts += bloot.floor_points(f)
    raw = mlod.read_mlod(os.path.join(here, "out", name + ".p3d"))
    lods = [PX.strip(l) for l in raw]
    L = {mlod.lod_name(l.resolution): l for l in lods}
    want = ["Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "Memory", "Roadway", "View Geometry",
            "Fire Geometry"]
    faces = {w: len(L[w].faces) for w in want if w in L}
    rec("C5 LOD set (vanilla house set)", all(w in L for w in want), ", ".join("%s %d" % kv for kv in faces.items()))
    over = {k: (faces.get(k, 0), v) for k, v in BUDGET.items() if faces.get(k, 0) > v}
    rec("C5 face budget (large / landmark: 12000 / 4600 / 1600)", not over,
        "R1 %d, R2 %d, R3 %d" % (faces["Resolution 1"], faces["Resolution 2"], faces["Resolution 3"]) +
        ("; OVER %s" % over if over else ""))
    geo, mem, road = L["Geometry"], L["Memory"], L["Roadway"]
    pr = geo.properties
    rec("Geometry properties + mass", pr.get("class") == "house" and pr.get("map") == "house" and
        pr.get("damage") == "no" and pr.get("autocenter") == "0" and sum(geo.mass or [0]) > 1000,
        "%s, mass %.0f kg" % (pr, sum(geo.mass or [0])))
    # C7 components
    for lname in ("Geometry", "View Geometry", "Fire Geometry"):
        l = L[lname]
        comps = [s for s in l.selections if s.startswith("Component")]
        bad = [c for c in comps if mlod.component_report(l, c)]
        covered = set()
        for c in comps:
            covered |= l.selections[c][1]
        rec("C7 %s closed + convex" % lname, not bad and len(covered) == len(l.faces),
            "%d components, %d bad, %d faces outside components" % (len(comps), len(bad), len(l.faces) - len(covered)))
    mats = {f[3] for f in L["Fire Geometry"].faces}
    rec("C7 Fire Geometry penetration rvmats", all(m.startswith("dz\\data\\data\\penetration\\") for m in mats),
        ", ".join(sorted(os.path.basename(m)[:-6] for m in mats)))
    # C2 library only
    bad = set()
    for l in lods:
        for _, _, tex, mat in l.faces:
            for pth in (tex, mat):
                if not pth:
                    continue
                pl = pth.lower()
                if pl.startswith(C.ALLOWED_VANILLA):
                    continue
                if pl.startswith("jp\\common\\materials\\") and os.path.isfile(os.path.join(DEV, "src", pth)):
                    continue
                bad.add(pth)
    rec("C2 library materials only", not bad, "every path under JP\\common\\materials\\ (on disk) or vanilla "
        "penetration / roadway" if not bad else "bad: %s" % sorted(bad)[:4])
    # C8 era / tells lint
    allp = {p.lower() for l in lods for f in l.faces for p in (f[2], f[3]) if p}
    glass = [p for p in allp if "glass" in p or "window_" in p]
    corrug = sum(len(s.faces) for s in M.solids if s.tag == "kawara_field" and 1 in s.vis)
    stones = sum(1 for s in M.solids if s.tag == "dodai_stone")
    rec("C8 era lint (no glass, kawara geometry, separate plinth stones)", not glass and corrug > 100 and stones > 40,
        "glass paths %d; %d corrugated kawara field faces in LOD0; %d individual dodai stones" % (len(glass), corrug,
                                                                                                   stones))
    # C3 grid
    off = [(round(x, 3), round(z, 3)) for (x, z, _, _) in MT.POSTS
           if not (C.on_grid(x, 0.455) and C.on_grid(z, 0.455))]
    rec("C3 grid snap (post nodes on the 0.455 grid)", not off, "%d posts%s" % (len(MT.POSTS), "" if not off else
                                                                                "; off-grid %s" % off[:4]))
    # doors: selections, memory, model.cfg, config
    mcfg = open(os.path.join(DEV, "src", "JP", "buildings", "machiya", "model.cfg")).read()
    ccfg = open(os.path.join(DEV, "src", "JP", "buildings", "config.cpp")).read()
    # config.cpp holds every shipped building (buildings/pipeline.py, B0): check this building's class only
    m_ = re.search(r"\tclass %s: HouseNoDestruct\n\t\{.*?\n\t\};\n" % cls, ccfg, re.S)
    ccfg = m_.group(0) if m_ else ""
    gcomps = C.components(geo)
    clears = []
    for k, d in enumerate(M.doors, 1):
        probs = []
        tw = "doorstwin%d" % k
        if d.twin != tw:
            probs.append("twin name %s" % d.twin)
        for w in ("Resolution 1", "Resolution 2", "Geometry", "View Geometry", "Fire Geometry"):
            sel = L[w].selections.get(tw)
            if not sel or not sel[1]:
                probs.append("%s: no %s faces" % (w, tw))
        for a in d.anims:
            b = a["bone"]
            for w in ("Resolution 1", "Geometry"):
                sel = L[w].selections.get(b)
                if not sel or not sel[1]:
                    probs.append("%s: no %s faces" % (w, b))
            if w == "Geometry" and sel:
                if not any(L[w].selections[c][1] == sel[1] for c in L[w].selections if c.startswith("Component")):
                    probs.append("%s is not exactly one Geometry component" % b)
            ax = mem.selections.get(b + "_axis")
            if not ax or len(ax[0]) != 2:
                probs.append("%s_axis needs 2 points" % b)
            elif a["type"] == "translation":
                ps = [mem.points[i] for i in sorted(ax[0])]
                v = [ps[1][i] - ps[0][i] for i in range(3)]
                want_d = [a["axis"][1][i] - a["axis"][0][i] for i in range(3)]
                if abs(math.sqrt(sum(c * c for c in v)) - 1.0) > 1e-3 or abs(sum(v[i] * want_d[i] for i in range(3))) < 0.999:
                    probs.append("%s axis not 1.00 m along the slide" % b)
            else:
                # rotation: memory vertex order = axis point order (the engine turns by the right-hand rule 1 -> 2)
                ps = [mem.points[i] for i in sorted(ax[0])]
                if max(abs(ps[0][i] - a["axis"][0][i]) for i in range(3)) > 1e-3:
                    probs.append("%s_axis point order differs from the recipe (rotation sense!)" % b)
            if not mem.selections.get(b):
                probs.append("memory leaf point %s missing" % b)
            acls = b[0].upper() + b[1:]
            last = ("offset1=%.4f;" % a["amount"]) if a["type"] == "translation" else ("angle1=%.6f;" % a["amount"])
            if not re.search(r'class %s\s*\{[^}]*type="%s";[^}]*source="DoorsTwin%d";[^}]*selection="%s";'
                             r'[^}]*axis="%s_axis";[^}]*%s' % (acls, a["type"], k, b, b, re.escape(last)), mcfg):
                probs.append("model.cfg %s wrong" % acls)
        if not mem.selections.get(tw + "_action"):
            probs.append("memory %s_action missing" % tw)
        if not re.search(r'class DoorsTwin%d\s*\{[^}]*component="DoorsTwin%d";[^}]*soundPos="doorsTwin%d_action";'
                         % (k, k, k), ccfg):
            probs.append("config Doors/DoorsTwin%d missing" % k)
        if not re.search(r'componentNames\[\]=\s*\{\s*"doorstwin%d"' % k, ccfg):
            probs.append("DamageZone DoorsTwin%d missing" % k)
        rec("C7 DoorsTwin%d selections, memory, model.cfg, config" % k, not probs,
            "%s (%s): bones %s" % (getattr(d, "label", ""), getattr(d, "style", ""),
                                   "+".join(a["bone"] for a in d.anims)) if not probs else "; ".join(probs[:4]))
        if getattr(d, "passable", True):
            ok, msg, clear = door_world(d, gcomps)
            clears.append(clear or 0.0)
            rec("C7 DoorsTwin%d sweep + clear (>= 1.00, D1) + head (D2)" % k, ok, msg)
        else:
            hits = C.sweep_hits(d, gcomps)
            rec("C7 DoorsTwin%d window sweep" % k, not hits, "%s moves closed -> open without touching other "
                "geometry" % d.style if not hits else "HITS %s" % hits[:3])
    # the open toriniwa passage into the kitchen (no door): clear width and head
    class _P:
        pass
    pv = _P()
    pv.anims = []
    passage = [c for c in gcomps if not c["door"]]
    x0m, z0m = MT.to_model_xz(MT.KEN / 2, MT.ZB)
    y0 = MT.DOMA
    lo = hi = x0m

    def free(xx):
        b = (xx - 0.004, xx + 0.004, y0 + 0.05, y0 + 1.95, z0m - 0.35, z0m + 0.35)
        return not any(C.comp_box_intersect(c, b, 0.0) for c in passage)
    while free(lo - 0.01) and lo > x0m - 3:
        lo -= 0.01
    while free(hi + 0.01) and hi < x0m + 3:
        hi += 0.01
    head = min([c["bbox"][2] for c in passage if c["bbox"][0] < hi and c["bbox"][1] > lo and
                c["bbox"][4] < z0m + 0.3 and c["bbox"][5] > z0m - 0.3 and c["bbox"][2] > y0 + 0.5] or [99]) - y0
    rec("C7 toriniwa -> kitchen passage (open) clear + head", hi - lo >= 1.0 and head >= 1.995,
        "clear %.2f m, head %.2f m" % (hi - lo, head))
    # Roadway on Geometry
    smp = C.roadway_samples(road)
    miss = [(round(x, 2), round(y, 2), round(z, 2)) for x, y, z, _ in smp
            if (lambda t: t is None or abs(t - y) > 0.03)(geo_top_below(gcomps, x, y, z))]
    rec("C7 Roadway sits on Geometry (+-3 cm)", not miss, "%d/%d samples%s" % (len(smp) - len(miss), len(smp),
                                                                              "; misses %s" % miss[:3] if miss else ""))
    # floors: roadway at floor height, head room >= 2.10
    n = miss_f = 0
    low = []
    lowest = 99.0
    for f in floors:
        x0, x1, z0, z1 = f["rect"]
        for i in range(15):
            for j in range(15):
                x = x0 + 0.05 + (x1 - x0 - 0.1) * i / 14
                z = z0 + 0.05 + (z1 - z0 - 0.1) * j / 14
                if any(a0 <= x <= a1 and b0 <= z <= b1 for (a0, a1, b0, b1) in f["obstacles"]):
                    continue
                n += 1
                if not any(abs(h - f["y"]) < 0.02 for h, _ in road_heights(road, x, z)):
                    miss_f += 1
                    continue
                ab = geo_bottom_above(gcomps, x, f["y"], z)
                if ab is not None:
                    lowest = min(lowest, ab - f["y"])
                    if ab - f["y"] < 2.10:
                        low.append((f["name"], round(x, 2), round(z, 2), round(ab - f["y"], 2)))
    rec("C7 walkable floors have Roadway at floor height", not miss_f, "%d/%d samples over %s" % (
        n - miss_f, n, ", ".join(f["name"] for f in floors)))
    rec("C7 head room >= 2.10 over every floor", not low, "lowest %.2f m%s" % (lowest, "; low %s" % low[:3] if low
                                                                                 else ""))
    # loot points (the floor ones: raised points on furniture are the decorator's D11)
    badl = []
    for p in pts:
        if p.get("prop"):
            continue
        x, y, z = p["model"]
        if not any(abs(h - y) < 0.02 for h, _ in road_heights(road, x, z)):
            badl.append(("off roadway", p["model"]))
            continue
        for k in range(8):
            a = k * math.pi / 4
            q = (x + p["range"] * math.cos(a), y + 0.4, z + p["range"] * math.sin(a))
            inside = [c for c in gcomps if not c["door"] and
                      all(mlod._dot(nrm, q) >= dd + 0.01 for nrm, dd in c["planes"])]
            if inside:
                badl.append(("range into geometry", p["model"]))
                break
    by = {}
    for p in pts:
        by[p["floor"]] = by.get(p["floor"], 0) + 1
    rec("Loot points on Roadway floors, ranges clear of walls", not badl and len(pts) >= 10,
        "%d points (%s)%s" % (len(pts), ", ".join("%s %d" % kv for kv in by.items()), "; bad %s" % badl[:2] if badl
                              else ""))
    ce = open(os.path.join(DEV, "test", "ce", "C_mapgroupproto.xml")).read()
    m_ = re.search(r'<group name="%s">.*?</group>' % cls, ce, re.S)       # this building's loot group only
    ce = m_.group(0) if m_ else ""
    cepts = [tuple(float(v) for v in m.group(1).split()) for m in re.finditer(r'<point pos="([^"]+)"', ce)]
    worst = max([max(abs(a - b) for a, b in zip(bloot.ce_to_world(l, POS, YAW), bloot.model_to_world(p["model"], POS,
                                                                                                     YAW)))
                 for p, l in zip(pts, cepts)] or [9])
    rec("CE loot frame -> world == model -> world (WORLD_BUILDINGS §0)", len(cepts) == len(pts) and worst < 1e-3,
        "%d points, max diff %.1e m" % (len(cepts), worst))
    # placement: footprint (incl. eaves) inside 14 x 14, clear of the sakura
    b = M.bbox()
    fw, fd = b[1] - b[0], b[5] - b[4]
    corners = [bloot.model_to_world((x, 0.0, z), POS, YAW) for x in (b[0], b[1]) for z in (b[4], b[5])]
    xs, zs = [c[0] for c in corners], [c[2] for c in corners]
    dist = min(math.hypot(max(min(xs) - sx, 0, sx - max(xs)), max(min(zs) - sz, 0, sz - max(zs)))
               for sx, sz in ((985.0, 1010.0), (1063.0, 1010.0)))
    rec("Placement footprint <= 14 x 14 m, inside the yard, clear of the sakura", fw <= 14 and fd <= 14 and
        min(xs) > 924 and max(xs) < 1124 and min(zs) > 924 and max(zs) < 1124 and dist > 8,
        "%.2f x %.2f m incl. eaves; world x %.1f-%.1f, z %.1f-%.1f; nearest sakura trunk %.1f m away; ridge %.2f m"
        % (fw, fd, min(xs), max(xs), min(zs), max(zs), dist, b[3]))
    BC.run_g3(M, L, floors, rec)          # C10-C19, the G3 checks every building runs (jpparts/buildcheck.py)
    # ODOL
    odol = os.path.join(DEV, "src", "JP", "buildings", "machiya", name + ".p3d")
    data = open(odol, "rb").read()
    if data[:4] != b"ODOL":
        rec("Binarize -> ODOL", False, "src p3d is not ODOL (binarize did not run?)")
    else:
        res = None
        for off in range(8, 400):
            kk = struct.unpack_from("<I", data, off)[0]
            if 1 <= kk <= 40:
                r = struct.unpack_from("<%df" % kk, data, off + 4)
                if any(abs(x - 1e15) < 1e10 for x in r) and all(x > 0 for x in r):
                    res = r
                    break
        names = [mlod.lod_name(r) for r in res] if res else []
        low_s = {m.group().decode().lower() for m in re.finditer(rb"[\x20-\x7e]{4,}", data)}
        bones = [a["bone"] for d in M.doors for a in d.anims]
        ok_b = all(b_ in low_s and b_ + "_axis" in low_s for b_ in bones)
        ok_t = all("doorstwin%d" % k in low_s and "doorstwin%d_action" % k in low_s for k in range(1, len(M.doors) + 1))
        skel = any((name + "_skeleton") in s for s in low_s)
        rec("Binarize -> ODOL (LODs, bones, axes, twin selections, skeleton)", res is not None and
            all(w in names for w in want) and ok_b and ok_t and skel,
            "ODOL v%d, %d bytes; LODs %d; bones+axes %s; twin selections+actions %s; skeleton %s" % (
                struct.unpack_from("<I", data, 4)[0], len(data), len(names), ok_b, ok_t, skel))
    n78 = len(RES)
    if extra:
        extra(M, L, floors, pts, rec, raw)
    out = {"building": cls, "date": "2026-09-30", "faces": "%d/%d/%d" % (faces["Resolution 1"],
                                                                         faces["Resolution 2"],
                                                                         faces["Resolution 3"]),
           "door_clear_m": [round(c, 2) for c in clears], "machiya_checks": n78,
           "machiya_failures": sum(1 for r in RES[:n78] if not r["ok"]), "checks": RES}
    with open(os.path.join(here, "checks.json"), "wb") as f:
        f.write(json.dumps(out, indent=1).encode("utf-8"))
    nf = sum(1 for r in RES if not r["ok"])
    print("RESULT: %s (%d checks, %d failures)" % ("PASS" if not nf else "FAIL", len(RES), nf))
    return nf == 0


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
