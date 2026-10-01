r"""shellcheck.py - the machiya's check set (buildings/machiya_t3_01/verify.py, 78 checks on that house) for ANY template
shell (C1, 2026-09-30: townhouse units, post-town houses, inns). Registry entries use it with "verify": "shellcheck";
the pipeline calls run(bd) after combine / binarize / pack, so config.cpp, model.cfg, the CE group and the ODOL exist.

Checks (as the machiya, generalised):
  C5 LOD set, C5 face budget (the entry's class), Geometry properties + mass, C7 closed + convex (3 LODs),
  C7 Fire Geometry penetration rvmats, C2 library materials, C8 era lint (no glass; kawara corrugation modelled when
  the shell has kawara; separate plinth stones), C3 grid (kit-frame posts), per door: selections / memory /
  model.cfg / config + sweep, open clear >= 1.00 (D1) and head >= 2.00 (windows: sweep), the open toriniwa ->
  kitchen passage (clear + head), Roadway on Geometry, Roadway at every floor, head room >= 2.10 over every floor,
  loot points on the Roadway floors with ranges clear of walls, CE loot frame == model frame, placement (every
  registry placement inside the island's test area and clear of the reserved spots), the G3 checks C10-C19
  (jpparts/buildcheck.run_g3), ODOL (LODs, bones, axes, twin selections, skeleton).
Writes buildings/<dir>/checks/<key>.json.
"""
import importlib.util
import json
import math
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))
from jpparts import mlod, checks as C, buildcheck as BC  # noqa: E402
from jpkit import loot as bloot  # noqa: E402
import registry  # noqa: E402

_spec = importlib.util.spec_from_file_location("machiya_verify_helpers",
                                               os.path.join(HERE, "machiya_t3_01", "verify.py"))
MV = importlib.util.module_from_spec(_spec)
sys.path.insert(0, os.path.join(HERE, "machiya_t3_01"))
_spec.loader.exec_module(MV)          # door_world, geo_top_below, geo_bottom_above, road_heights (the machiya's own)

NOMINAL = ((1024.0, 25.0, 1045.0), 180.0)       # CE frame check when a shell has no placement
# test-island spots other agents own (README "The test island"), world x0, x1, z0, z1
RESERVED = {"player spawn": (1019.0, 1029.0, 980.0, 990.0), "item grid": (998.0, 1052.0, 966.0, 978.0),
            "machiya shop + yard": (1014.0, 1034.0, 1036.0, 1062.0), "sakura W": (980.0, 990.0, 1005.0, 1015.0),
            "sakura E": (1058.0, 1068.0, 1005.0, 1015.0), "bamboo grove": (1080.0, 1110.0, 955.0, 995.0),
            "weapon range": (995.0, 1055.0, 925.0, 950.0), "swatch wall (M)": (952.0, 963.0, 1095.0, 1105.0)}
# C2: the C1 test street (z 1080) is another agent's; the hamlet (C2) must stay clear of it
RESERVED_BY_KEY = {"c1 test street": (978.0, 1068.0, 1062.0, 1098.0)}


def placement_boxes(b, M):
    """World boxes (x0, x1, z0, z1) of every placement of building b (its model bbox incl. eaves)."""
    bb = M.bbox()
    out = []
    for pl in b["placements"]:
        cs = [bloot.model_to_world((x, 0.0, z), pl["pos"], pl["yaw"]) for x in (bb[0], bb[1]) for z in (bb[4], bb[5])]
        out.append((min(c[0] for c in cs), max(c[0] for c in cs), min(c[2] for c in cs), max(c[2] for c in cs)))
    return out


def door_world_rot(d, gcomps):
    """W2C (2026-10-01): MV.door_world for a PASSABLE door whose leaves rotate (the kido's hinged gate pair; the
    machiya's door_world shifts leaves along their axis, right only for sliding ones). The sweep is sampled along the
    real rotation (checks.sweep_hits); the clear width and head are measured on the closed leaves' line with the leaves
    turned fully open (raycheck.open_state), from the floor under the action point (action y - act_h)."""
    from jpparts import raycheck as RC
    bones = [a["bone"] for a in d.anims]
    hits = C.sweep_hits(d, gcomps)
    leaves = [c for c in gcomps if c["door"] in bones]
    if not leaves:
        return False, "no Geometry leaf", None
    lb = [c["bbox"] for c in leaves]
    bb = [min(b[0] for b in lb), max(b[1] for b in lb), min(b[4] for b in lb), max(b[5] for b in lb)]
    along_x = bb[1] - bb[0] >= bb[3] - bb[2]
    wall = (bb[2] + bb[3]) / 2 if along_x else (bb[0] + bb[1]) / 2
    obst = RC.open_state(gcomps, [d], 1.0)
    ax = d.action
    y0 = ax[1] - getattr(d, "act_h", 1.0)

    def col(s):
        if along_x:
            return (s - 0.004, s + 0.004, y0 + 0.05, y0 + 1.95, wall - 0.35, wall + 0.35)
        return (wall - 0.35, wall + 0.35, y0 + 0.05, y0 + 1.95, s - 0.004, s + 0.004)

    def free(s):
        return not any(C.comp_box_intersect(c, col(s), 0.0) for c in obst)
    c0 = ax[0] if along_x else ax[2]
    if not free(c0):
        return False, "doorway centre blocked with the leaves open (sweep hits %s)" % hits[:3], None
    lo = hi = c0
    while free(lo - 0.01) and lo > c0 - 4:
        lo -= 0.01
    while free(hi + 0.01) and hi < c0 + 4:
        hi += 0.01
    # W2S (2026-10-01): the head is the lowest Geometry underside over the doorway, found by vertical rays on the
    # doorway (5 stations across the clear width x every 5 cm from 0.30 m before to 0.30 m behind the leaves' line);
    # W2C's bounding-box test counted a sloped step canopy (kohai) in front of a shrine door at its outer eave height
    head = 99.0
    for i in range(1, 6):
        s = lo + (hi - lo) * i / 6
        for dz in [k * 0.05 for k in range(-6, 7)]:
            xq, zq = (s, wall + dz) if along_x else (wall + dz, s)
            ab = MV.geo_bottom_above(obst, xq, y0 + 0.5, zq)
            if ab is not None:
                head = min(head, ab - y0)
    clear = hi - lo
    ok = not hits and clear >= 1.0 - 1e-6 and head >= 2.0 - 0.005
    return ok, "leaves turn %s deg %s; open clear %.2f m, head %.2f m" % (
        "/".join("%.0f" % math.degrees(a["amount"]) for a in d.anims),
        "without touching other geometry" if not hits else "HITS %s" % hits[:3], clear, head), clear


def run(bd):
    b, M, floors, pts, mod = bd["b"], bd["M"], bd["floors"], bd["pts"], bd["mod"]
    name, cls = bd["rec"]["name"], bd["rec"]["class"]
    RES = []

    def rec(check, ok, detail):
        RES.append({"check": check, "ok": bool(ok), "detail": detail})
        print("%-4s %-52s %s" % ("OK" if ok else "FAIL", check, detail))
    raw = mlod.read_mlod(bd["mlod"])
    furnished = getattr(mod, "D", None) is not None and hasattr(mod, "proxies")
    if furnished:
        # C3: a furnished variant (the B4 pattern): the shell checks run on the LODs with the proxy triangles stripped;
        # the decorator checks (decor.check_all, D1-D16) read the raw LODs for the proxy records
        from jpparts import proxies as PX
        lods = [PX.strip(l) for l in raw]
    else:
        lods = raw
    L = {mlod.lod_name(l.resolution): l for l in lods}
    want = ["Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "Memory", "Roadway", "View Geometry",
            "Fire Geometry"]
    faces = {w: len(L[w].faces) for w in want if w in L}
    rec("C5 LOD set (vanilla house set)", all(w in L for w in want), ", ".join("%s %d" % kv for kv in faces.items()))
    bud = registry.BUDGETS[b["budget"]]
    got = (faces.get("Resolution 1", 0), faces.get("Resolution 2", 0), faces.get("Resolution 3", 0))
    rec("C5 face budget (%s: %d / %d / %d)" % ((b["budget"],) + bud), all(g <= m for g, m in zip(got, bud)),
        "R1 %d, R2 %d, R3 %d" % got)
    geo, mem, road = L["Geometry"], L["Memory"], L["Roadway"]
    pr = geo.properties
    rec("Geometry properties + mass", pr.get("class") == "house" and pr.get("map") == "house" and
        pr.get("damage") == "no" and pr.get("autocenter") == "0" and sum(geo.mass or [0]) > 1000,
        "%s, mass %.0f kg" % (pr, sum(geo.mass or [0])))
    import bindcheck              # FB1: the engine binds a WRP object only via Land_<p3d stem> + Geometry class=house
    bprobs = bindcheck.check(cls, bd["rec"]["model"], b["model_dir"], name)
    rec("B1/B2 binds in game (class == Land_<p3d stem>, shipped p3d has class=house)", not bprobs,
        "%s -> %s.p3d" % (cls, name) if not bprobs else "; ".join(bprobs))
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
    allp = {p.lower() for l in lods for f in l.faces for p in (f[2], f[3]) if p}
    glass = [p for p in allp if "glass" in p or "window_" in p]
    has_kawara = any(s.tag == "kawara_field" for s in M.solids)
    corrug = sum(len(s.faces) for s in M.solids if s.tag == "kawara_field" and 1 in s.vis)
    stones = sum(1 for s in M.solids if s.tag == "dodai_stone")
    soseki = sum(1 for s in M.solids if s.tag == "soseki")         # C2: rural posts stand on field stones
    soseki += sum(1 for s in M.solids if s.tag == "footing")       # C3: a kura stands on individual cut blocks
    rec("C8 era lint (no glass, kawara geometry, separate plinth stones)",
        not glass and (corrug > 100 or not has_kawara) and stones + soseki >= 4,
        "glass paths %d; %s; %d individual dodai stones%s" % (
            len(glass), "%d corrugated kawara field faces in LOD0" % corrug if has_kawara else "no kawara (board roof)",
            stones, (", %d soseki under the posts" % soseki) if soseki else ""))
    posts = getattr(mod, "POSTS", [])
    off = [(round(x, 3), round(z, 3)) for (x, z, _, _) in posts if not (C.on_grid(x, 0.455) and C.on_grid(z, 0.455))]
    rec("C3 grid snap (post nodes on the 0.455 grid)", bool(posts) and not off,
        "%d posts%s" % (len(posts), "" if not off else "; off-grid %s" % off[:4]))
    mcfg = open(os.path.join(DEV, "src", "JP", "buildings", b["model_dir"], "model.cfg")).read()
    ccfg = open(os.path.join(DEV, "src", "JP", "buildings", "config.cpp")).read()
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
            bn = a["bone"]
            for w in ("Resolution 1", "Geometry"):
                sel = L[w].selections.get(bn)
                if not sel or not sel[1]:
                    probs.append("%s: no %s faces" % (w, bn))
            sel = L["Geometry"].selections.get(bn)
            if sel and not any(L["Geometry"].selections[c][1] == sel[1] for c in L["Geometry"].selections
                               if c.startswith("Component")):
                probs.append("%s is not exactly one Geometry component" % bn)
            ax = mem.selections.get(bn + "_axis")
            if not ax or len(ax[0]) != 2:
                probs.append("%s_axis needs 2 points" % bn)
            elif a["type"] == "translation":
                ps = [mem.points[i] for i in sorted(ax[0])]
                v = [ps[1][i] - ps[0][i] for i in range(3)]
                want_d = [a["axis"][1][i] - a["axis"][0][i] for i in range(3)]
                if abs(math.sqrt(sum(c * c for c in v)) - 1.0) > 1e-3 or abs(sum(v[i] * want_d[i] for i in range(3))) < 0.999:
                    probs.append("%s axis not 1.00 m along the slide" % bn)
            else:
                ps = [mem.points[i] for i in sorted(ax[0])]
                if max(abs(ps[0][i] - a["axis"][0][i]) for i in range(3)) > 1e-3:
                    probs.append("%s_axis point order differs from the recipe (rotation sense!)" % bn)
            if not mem.selections.get(bn):
                probs.append("memory leaf point %s missing" % bn)
            acls = bn[0].upper() + bn[1:]
            last = ("offset1=%.4f;" % a["amount"]) if a["type"] == "translation" else ("angle1=%.6f;" % a["amount"])
            if not re.search(r'class %s\s*\{[^}]*type="%s";[^}]*source="DoorsTwin%d";[^}]*selection="%s";'
                             r'[^}]*axis="%s_axis";[^}]*%s' % (acls, a["type"], k, bn, bn, re.escape(last)), mcfg):
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
            gc = gcomps
            if getattr(mod, "DOOR_CHECK_OTHERS_OPEN", False):
                # C3 (kura '_hinged'): the outer plaster leaves are shutters over the same doorway (initOpened 1):
                # the inner door's clear width is measured with them open, as C10 measures reach
                from jpparts import raycheck as RC
                sh = [od for od in M.doors if od is not d and not getattr(od, "passable", True)]
                gc = RC.open_state(gcomps, sh, 1.0) if sh else gcomps
            if any(a["type"] == "rotation" for a in d.anims):
                ok, msg, clear = door_world_rot(d, gc)        # W2C: hinged gate leaves (MV.door_world slides them)
            else:
                ok, msg, clear = MV.door_world(d, gc)
            clears.append(clear or 0.0)
            rec("C7 DoorsTwin%d sweep + clear (>= 1.00, D1) + head (D2)" % k, ok, msg)
        else:
            hits = C.sweep_hits(d, gcomps)
            rec("C7 DoorsTwin%d window sweep" % k, not hits, "%s moves closed -> open without touching other "
                "geometry" % d.style if not hits else "HITS %s" % hits[:3])
    passage = [c for c in gcomps if not c["door"]]
    for (x0m, z0m, y0) in getattr(mod, "PASSAGES", []):
        lo = hi = x0m

        def free(xx):
            bx = (xx - 0.004, xx + 0.004, y0 + 0.05, y0 + 1.95, z0m - 0.35, z0m + 0.35)
            return not any(C.comp_box_intersect(c, bx, 0.0) for c in passage)
        while free(lo - 0.01) and lo > x0m - 3:
            lo -= 0.01
        while free(hi + 0.01) and hi < x0m + 3:
            hi += 0.01
        head = min([c["bbox"][2] for c in passage if c["bbox"][0] < hi and c["bbox"][1] > lo and
                    c["bbox"][4] < z0m + 0.3 and c["bbox"][5] > z0m - 0.3 and c["bbox"][2] > y0 + 0.5] or [99]) - y0
        rec(getattr(mod, "PASSAGE_LABEL", "C7 toriniwa -> kitchen passage (open) clear + head"),
            hi - lo >= 1.0 and head >= 1.995, "clear %.2f m, head %.2f m" % (hi - lo, head))
    smp = C.roadway_samples(road)
    miss = [(round(x, 2), round(y, 2), round(z, 2)) for x, y, z, _ in smp
            if (lambda t: t is None or abs(t - y) > 0.03)(MV.geo_top_below(gcomps, x, y, z))]
    rec("C7 Roadway sits on Geometry (+-3 cm)", not miss, "%d/%d samples%s" % (len(smp) - len(miss), len(smp),
                                                                              "; misses %s" % miss[:3] if miss else ""))
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
                if not any(abs(h - f["y"]) < 0.02 for h, _ in MV.road_heights(road, x, z)):
                    miss_f += 1
                    continue
                ab = MV.geo_bottom_above(gcomps, x, f["y"], z)
                if ab is not None:
                    lowest = min(lowest, ab - f["y"])
                    if ab - f["y"] < 2.10:
                        low.append((f["name"], round(x, 2), round(z, 2), round(ab - f["y"], 2)))
    rec("C7 walkable floors have Roadway at floor height", not miss_f, "%d/%d samples over %s" % (
        n - miss_f, n, ", ".join(f["name"] for f in floors)))
    rec("C7 head room >= 2.10 over every floor", not low, "lowest %.2f m%s" % (lowest, "; low %s" % low[:3] if low
                                                                                 else ""))
    # stairs (the grand inn): b2_assembly.stair_checks ST1-ST5 on the placed flight, any direction along x
    for st in getattr(mod, "STAIRS", []):
        angs = []
        for verts, _, tex, _ in road.faces:
            if "stairs" in tex:
                pp = [road.points[v[0]] for v in verts]
                nn = mlod._normalize(mlod._face_formula_normal(pp))
                angs.append(math.degrees(math.acos(min(1.0, abs(nn[1])))))
        rec("ST1 walk ramp <= 38 deg (D4, 37.8 walked in game)", bool(angs) and max(angs) <= 38.0 + 1e-6,
            "ramp faces %s deg" % sorted({round(x, 2) for x in angs}))
        rec("ST2 flight width >= 1.10 m (D4)", st["width"] >= 1.10 - 1e-6, "%.2f m" % st["width"])
        (xf, zf), sx, run = st["foot"], st["dir"], st["run"]
        y0, rise = st["y_low"], st["y_up"] - st["y_low"]
        zl = (zf + 0.15, zf + st["width"] / 2, zf + st["width"] - 0.15)
        worst = (99.0, None)
        for i in range(1, 60):
            x = xf + sx * run * i / 60
            yr = y0 + rise * i / 60
            for z in zl:
                for c in gcomps:
                    r = C.ray_y(c, x, z)
                    if r and r[0] > yr + 0.05 and r[0] - yr < worst[0]:
                        worst = (r[0] - yr, (round(x, 2), round(z, 2), c["name"]))
        rec("ST3 head room >= 2.05 m over the flight (D4)", worst[0] >= 2.05 - 1e-6,
            "lowest %.2f m over the ramp at %s" % worst if worst[1] else "nothing over the flight")
        hs_foot = [h for h, _ in MV.road_heights(road, xf + sx * 0.02, zl[1])]
        hs_head = [h for h, _ in MV.road_heights(road, xf + sx * (run + 0.05), zl[1])]
        rec("ST4 the ramp meets the lower floor at its foot and the upper floor at its head",
            any(abs(h - y0) < 0.03 for h in hs_foot) and any(abs(h - st["y_up"]) < 0.02 for h in hs_head),
            "foot %s / head side %s (floors %.2f / %.2f)" % ([round(h, 3) for h in hs_foot],
                                                             [round(h, 3) for h in hs_head], y0, st["y_up"]))
        over = 0
        w0, w1 = st["well"][0], st["well"][1]
        for i in range(1, 20):
            x = w0 + 0.05 + (w1 - w0 - 0.15) * i / 20
            yr = y0 + rise * abs(x - xf) / run
            for z in (zl[0], zl[2]):
                if any(yr + 0.3 < h < st["y_up"] + 0.5 for h, _ in MV.road_heights(road, x, z)):   # the roof above is not a floor
                    over += 1
        rec("ST5 stairwell cut: no upper-floor Roadway over the flight", over == 0, "%d samples covered" % over)
    badl = []
    for p in pts:
        if p.get("prop"):
            continue
        x, y, z = p["model"]
        if not any(abs(h - y) < 0.02 for h, _ in MV.road_heights(road, x, z)):
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
    empty = [f["name"] for f in floors if not by.get(f["name"])]
    rec("Loot points on Roadway floors, ranges clear of walls, every room", not badl and not empty,
        "%d points (%s)%s%s" % (len(pts), ", ".join("%s %d" % kv for kv in by.items()),
                                "; bad %s" % badl[:2] if badl else "", "; no points in %s" % empty if empty else ""))
    ce = open(os.path.join(DEV, "test", "ce", "C_mapgroupproto.xml")).read()
    m_ = re.search(r'<group name="%s">.*?</group>' % cls, ce, re.S)
    ce = m_.group(0) if m_ else ""
    cepts = [tuple(float(v) for v in m.group(1).split()) for m in re.finditer(r'<point pos="([^"]+)"', ce)]
    pos, yaw = (b["placements"][0]["pos"], b["placements"][0]["yaw"]) if b["placements"] else NOMINAL
    worst = max([max(abs(a - c) for a, c in zip(bloot.ce_to_world(l, pos, yaw), bloot.model_to_world(p["model"], pos,
                                                                                                    yaw)))
                 for p, l in zip(pts, cepts)] or [9])
    rec("CE loot frame -> world == model -> world (WORLD_BUILDINGS §0)", len(cepts) == len(pts) and worst < 1e-3,
        "%d points, max diff %.1e m" % (len(cepts), worst))
    boxes = placement_boxes(b, M)
    clash = []
    for (x0, x1, z0, z1) in boxes:
        if not (924 < x0 and x1 < 1124 and 924 < z0 and z1 < 1124):
            clash.append("outside the test yard")
        extra = RESERVED_BY_KEY if b.get("dir") in ("farmhouse", "hut", "shed") else {}
        for nm, (a0, a1, c0, c1) in list(RESERVED.items()) + list(extra.items()):
            if x0 < a1 and x1 > a0 and z0 < c1 and z1 > c0:
                clash.append(nm)
    rec("Placement inside the test yard, clear of the reserved spots", not clash,
        ("%d placement(s): %s" % (len(boxes), "; ".join("x %.1f-%.1f z %.1f-%.1f" % bx for bx in boxes)) if boxes
         else "not placed on the island (shipped in the PBO only)") + ("; CLASH %s" % sorted(set(clash)) if clash
                                                                        else ""))
    BC.run_g3(M, L, floors, rec, extra_portals=getattr(mod, "PORTALS", ()))
    if furnished:
        from jpparts import decor as DC, raycheck as RC

        def door_fn(d, gc):
            if getattr(mod, "DOOR_CHECK_OTHERS_OPEN", False):
                sh = [od for od in M.doors if od is not d and not getattr(od, "passable", True)]
                gc = RC.open_state(gc, sh, 1.0) if sh else gc
            if any(a["type"] == "rotation" for a in d.anims):
                return door_world_rot(d, gc)      # W2F: hinged leaves (shrine / temple doors, kido) as C7 measures them
            return MV.door_world(d, gc)
        DC.check_all(mod.D, M, L, pts, rec, door_fn=door_fn,
                     extra_openings=getattr(mod, "EXTRA_OPENINGS", None), fixed_band=getattr(mod, "FIXED_BAND", None),
                     site_bounds=getattr(mod, "SITE_BOUNDS", None), mlod_lods=raw)
    odol =os.path.join(DEV, "src", "JP", "buildings", b["model_dir"], name + ".p3d")
    data = open(odol, "rb").read()
    if data[:4] != b"ODOL":
        rec("Binarize -> ODOL", False, "src p3d is not ODOL (binarize did not run?)")
    else:
        res = None
        for off_ in range(8, 400):
            kk = struct.unpack_from("<I", data, off_)[0]
            if 1 <= kk <= 40:
                r = struct.unpack_from("<%df" % kk, data, off_ + 4)
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
    nf = sum(1 for r in RES if not r["ok"])
    out = {"building": cls, "key": b["key"], "date": "2026-09-30", "budget": b["budget"],
           "faces": "%d/%d/%d" % got, "door_clear_m": [round(c, 2) for c in clears], "checks_n": len(RES),
           "failures": nf, "checks": RES}
    p = os.path.join(HERE, b.get("dir", b["key"]), "checks", b["key"] + ".json") if "dir" in b else \
        os.path.join(HERE, b["key"], "checks.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(json.dumps(out, indent=1).encode("utf-8"))
    print("RESULT %s: %s (%d checks, %d failures)" % (b["key"], "PASS" if not nf else "FAIL", len(RES), nf))
    return nf == 0
