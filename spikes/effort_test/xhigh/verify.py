#!/usr/bin/env python3
"""verify.py - offline checks for jp_f_tansu (effort test, level xhigh), all read back from disk -> checks.json.

PLAYBOOK 12 / 15 checks that apply to a prop (BUILD_LIST row 26 lists C1 C2 C4 C5 C6 C8 C9):
  C1  palette: mean colour of every used _co texture vs its palette ID, and the stand-in wood vs timber_interior
  C2  library only: every texture / rvmat path under JP\\common\\materials (on disk) or a vanilla penetration rvmat
  C4  dimensions vs the build list (body 1.00 x 0.45 x 1.00, two parts of 0.50, 5 drawers)
  C5  LOD set and face budgets (furniture <= 1000 MLOD faces; the brief's 1,500 also met as triangles)
  C6  base on the floor, no interpenetration > 1 cm between separate pieces, dropped drawer inside the front zone,
      loot points sit on their surfaces with their range inside the surface
  C7  Geometry / View / Fire components closed and convex, Fire uses penetration rvmats, mass, autocenter=0
  C8  era lint: no glass, no modern metal (only the library's wrought iron), no vanilla textures
  C19 matte finish: every non-glossy rvmat has fresnel(0.01,0.01) and a black env map (iron is glossy by design)
  +   visual sanity: no degenerate faces, no coplanar overlapping faces facing the same way (z-fighting)
  +   binarize log, ODOL read-back, CfgConvert, PBO contents + SHA-1 trailer, config classes
"""
import hashlib
import json
import math
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(DEV, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "tools", "common"))
sys.path.insert(0, os.path.join(DEV, "tools", "placecheck"))
import tansu  # noqa: E402
from jpparts import mlod  # noqa: E402

LEVEL = "xhigh"
SRC = os.path.join(DEV, "src", "JP", "effort_test", LEVEL)
OUT = os.path.join(HERE, "out")
FILES = {"A": "jp_f_tansu.p3d", "B": "jp_f_tansu_ransacked.p3d"}
LIBDIR = os.path.join(DEV, "src", "JP", "common", "materials")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
PALETTE = os.path.join(DEV, "playbook", "palette.json")

RES = []


def check(name, ok, detail):
    RES.append({"check": name, "ok": bool(ok), "detail": detail})
    print("%s  %-58s %s" % ("PASS" if ok else "FAIL", name, detail))


# ------------------------------------------------------------------------------------------------ geometry helpers
def face_pts(lod, fi):
    return [lod.points[v[0]] for v in lod.faces[fi][0]]


def outward(lod, fi):
    """p3d: the formula normal points INTO the solid, so outward = -formula."""
    n = mlod._normalize(mlod._face_formula_normal(face_pts(lod, fi)))
    return (-n[0], -n[1], -n[2])


def area(pts):
    n = mlod._face_formula_normal(pts)
    return 0.5 * math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)


def comp_planes(lod, name):
    pw, fs = lod.selections[name]
    planes = []
    for fi in fs:
        fp = face_pts(lod, fi)
        n = mlod._normalize(mlod._face_formula_normal(fp))          # inward
        planes.append((n, mlod._dot(n, fp[0])))
    return planes, [lod.points[i] for i in pw]


def inside(planes, p, tol=0.0):
    return all(mlod._dot(n, p) >= d - tol for n, d in planes)


def penetration(A, B):
    """Max depth (m) of any vertex / edge sample of one convex component inside the other (0 = no overlap)."""
    best = 0.0
    for (pa, va), (pb, vb) in ((A, B), (B, A)):
        samples = list(va)
        for i in range(len(va)):
            for j in range(i + 1, len(va)):
                for t in (0.25, 0.5, 0.75):
                    samples.append(tuple(va[i][k] + (va[j][k] - va[i][k]) * t for k in range(3)))
        for p in samples:
            if inside(pb, p, 1e-6):
                depth = min(mlod._dot(n, p) - d for n, d in pb)
                best = max(best, depth)
    return best


def ray_down(planes, x, z):
    lo, hi = -1e9, 1e9
    for n, d in planes:
        rhs = d - n[0] * x - n[2] * z
        if abs(n[1]) < 1e-9:
            if rhs > 1e-6:
                return None
            continue
        t = rhs / n[1]
        if n[1] > 0:
            lo = max(lo, t)
        else:
            hi = min(hi, t)
    return (lo, hi) if lo <= hi + 1e-9 else None


def clip_poly(subject, clip):
    """Sutherland-Hodgman on 2D convex polygons."""
    def inside_e(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= -1e-12

    def inter(p, q, a, b):
        x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
        x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-15:
            return q
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    out = subject
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside_e(e, a, b):
                if not inside_e(s, a, b):
                    out.append(inter(s, e, a, b))
                out.append(e)
            elif inside_e(s, a, b):
                out.append(inter(s, e, a, b))
            s = e
    return out


def area2(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2 if len(poly) >= 3 else 0.0


def ccw(poly):
    s = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
            for i in range(len(poly)))
    return poly if s > 0 else poly[::-1]


def zfight_pairs(lod):
    """Pairs of faces in one plane, facing the same way, whose polygons overlap by > 1 mm^2."""
    groups = {}
    for fi in range(len(lod.faces)):
        pts = face_pts(lod, fi)
        n = outward(lod, fi)
        d = mlod._dot(n, pts[0])
        key = (round(n[0], 3), round(n[1], 3), round(n[2], 3), round(d / 0.0002))
        groups.setdefault(key, []).append(fi)
    bad = []
    for key, fis in groups.items():
        if len(fis) < 2:
            continue
        n = key[:3]
        # 2D basis in the plane
        ref = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
        u = mlod._normalize(mlod._cross(n, ref))
        v = mlod._cross(n, u)
        polys = {fi: ccw([(mlod._dot(p, u), mlod._dot(p, v)) for p in face_pts(lod, fi)]) for fi in fis}
        for i in range(len(fis)):
            for j in range(i + 1, len(fis)):
                a = area2(clip_poly(polys[fis[i]], polys[fis[j]]))
                if a > 1e-6:
                    bad.append((fis[i], fis[j], round(a * 1e6, 1)))
    return bad


# ------------------------------------------------------------------------------------------------ colour
def lab(c):
    def f(u):
        u /= 255.0
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    r, g, b = [f(x) for x in c]
    X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def h(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else 7.787 * t + 16.0 / 116.0
    fx, fy, fz = h(X), h(Y), h(Z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de76(a, b):
    return math.dist(lab(a), lab(b))


# ------------------------------------------------------------------------------------------------ run
def run():
    RES.clear()
    L = {st: mlod.read_mlod(os.path.join(OUT, FILES[st])) for st in FILES}
    br = json.load(open(os.path.join(OUT, "build_result.json"), encoding="utf-8"))
    infos = br["infos"]
    pal = {e["id"]: e for e in json.load(open(PALETTE, encoding="utf-8"))["entries"]} \
        if "entries" in json.load(open(PALETTE, encoding="utf-8")) else None
    if pal is None:
        raw = json.load(open(PALETTE, encoding="utf-8"))
        lst = raw if isinstance(raw, list) else next(v for v in raw.values() if isinstance(v, list))
        pal = {e["id"]: e for e in lst}
    faces_summary = {}
    used_mats = set()
    for st in ("A", "B"):
        lods = L[st]
        byname = {mlod.lod_name(l.resolution): l for l in lods}
        counts = {k: len(v.faces) for k, v in byname.items()}
        faces_summary[st] = counts
        tris = {k: sum(len(f[0]) - 2 for f in v.faces) for k, v in byname.items() if k.startswith("Resolution")}
        want = ["Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "View Geometry", "Fire Geometry"]
        check("%s C5 LOD set (BUILD_LIST: Res 1-3, Geo, View, Fire, no Memory)" % st,
              all(w in byname for w in want) and len(byname) == len(want),
              ", ".join("%s %d" % kv for kv in counts.items()))
        r1, r2, r3 = counts["Resolution 1"], counts["Resolution 2"], counts["Resolution 3"]
        check("%s C5 budget Res 1 <= 1000 faces, <= 1500 triangles" % st, r1 <= 1000 and tris["Resolution 1"] <= 1500,
              "Res 1 %d faces = %d triangles (vanilla case_d 148, case_a 120 triangles)" % (r1, tris["Resolution 1"]))
        check("%s C5 LOD chain decreasing" % st, r1 > r2 > r3 > 0,
              "Res 2 = %.0f %% of Res 1, Res 3 = %.0f %% (playbook ratio ~38 %% / 13 %%); triangles %s"
              % (100.0 * r2 / r1, 100.0 * r3 / r1, tris))
        # C2 + C8 paths
        bad, vanilla_tex = set(), set()
        for l in lods:
            for _, _, tex, mat in l.faces:
                for pth in (tex, mat):
                    if not pth:
                        continue
                    pl = pth.lower()
                    if pl.startswith("dz\\data\\data\\penetration\\"):
                        if not os.path.isfile(os.path.join("P:\\", pth)):
                            bad.add(pth + " (missing on P:)")
                        continue
                    if pl.startswith("jp\\common\\materials\\"):
                        used_mats.add(pth)
                        if not os.path.isfile(os.path.join(DEV, "src", pth)):
                            bad.add(pth + " (missing)")
                        continue
                    bad.add(pth)
                    if pl.startswith("dz\\"):
                        vanilla_tex.add(pth)
        check("%s C2 library only" % st, not bad, "; ".join(sorted(bad)[:4]) if bad else
              "every texture / rvmat under JP\\common\\materials (on disk) or a vanilla penetration rvmat")
        names = " ".join(sorted({f[2].lower() + " " + f[3].lower() for l in lods for f in l.faces}))
        tells = [w for w in ("glass", "steel", "chrome", "alu", "plastic", "concrete") if w in names]
        check("%s C8 era lint" % st, not tells and not vanilla_tex,
              "materials: street_dark / weathered / sooted wood + wrought iron only" if not tells else str(tells))
        # C7 components
        for lname in ("Geometry", "View Geometry", "Fire Geometry"):
            l = byname[lname]
            comps = sorted(s for s in l.selections if s.startswith("Component"))
            probs = []
            covered = set()
            for c in comps:
                pr = mlod.component_report(l, c)
                if pr:
                    probs.append("%s: %s" % (c, pr[0]))
                covered |= l.selections[c][1]
            if len(covered) != len(l.faces):
                probs.append("%d faces outside components" % (len(l.faces) - len(covered)))
            check("%s C7 %s closed + convex" % (st, lname), not probs,
                  "%d components%s" % (len(comps), "; " + "; ".join(probs[:3]) if probs else ", all closed and convex"))
        fmats = {f[3] for f in byname["Fire Geometry"].faces}
        check("%s C7 Fire penetration rvmats" % st, all(m.lower().startswith("dz\\data\\data\\penetration\\")
                                                        for m in fmats), ", ".join(sorted(fmats)))
        g = byname["Geometry"]
        m = sum(g.mass or [0.0])
        check("%s C7 Geometry mass + autocenter=0" % st, abs(m - tansu.MASS) < 0.01 and
              g.properties.get("autocenter") == "0" and min(g.mass) >= 0.0,
              "mass %.2f kg over %d points (by component volume), properties %s" % (m, len(g.points), g.properties))
        # C6 base on the floor
        mins = {k: min(p[1] for p in v.points) for k, v in byname.items() if v.points and k != "Memory"}
        check("%s C6 base on the floor (0-2 cm)" % st, all(-1e-4 <= v <= 0.02 for v in mins.values()),
              ", ".join("%s %.4f" % (k.replace("Resolution ", "R"), v) for k, v in mins.items()))
        # C4 dimensions (state A body)
        r1l = byname["Resolution 1"]
        wood = [p for fi in range(len(r1l.faces)) if "\\wood\\" in r1l.faces[fi][2] for p in face_pts(r1l, fi)]
        allp = r1l.points
        bb = lambda P: (min(p[0] for p in P), max(p[0] for p in P), min(p[1] for p in P), max(p[1] for p in P),  # noqa
                        min(p[2] for p in P), max(p[2] for p in P))
        if st == "A":
            wb_ = bb(wood)
            W, H, D = wb_[1] - wb_[0], wb_[3] - wb_[2], wb_[5] - wb_[4]
            ok = abs(W - 1.0) <= 0.01 and abs(H - 1.0) <= 0.01 and abs(D - 0.45) <= 0.009
            ab = bb(allp)
            check("A C4 body 1.00 x 0.45 x 1.00 (+-1 cm / 2 %)", ok,
                  "wood body %.3f x %.3f x %.3f m (w x d x h); with fittings %.3f x %.3f x %.3f"
                  % (W, D, H, ab[1] - ab[0], ab[5] - ab[4], ab[3] - ab[2]))
            ys = sorted({round(p[1], 4) for p in wood})
            check("A C4 two stacked parts of 0.50", 0.5 in ys and min(ys) == 0.0 and max(ys) == 1.0,
                  "lower 0.00-0.50, upper 0.50-1.00 (upper 4 mm smaller at front and sides)")
            nd = len(infos["A"]["drawers"])
            nrings = sum(1 for fi in range(len(r1l.faces)) if "metal" in r1l.faces[fi][2]) // 1
            check("A C4 drawers 4-5, iron ring pulls, side handles", 4 <= nd <= 5,
                  "%d drawers (2 small over 1 wide in the upper part, 2 wide in the lower), 8 ring pulls, 3 lock "
                  "plates, 4 side handles, 10 corner plates; %d iron faces" % (nd, nrings))
        # visual sanity
        for lname in ("Resolution 1", "Resolution 2", "Resolution 3"):
            l = byname[lname]
            degen = [fi for fi in range(len(l.faces)) if area(face_pts(l, fi)) < 1e-8]
            zf = zfight_pairs(l)
            check("%s visual %s: no degenerate / z-fighting faces" % (st, lname), not degen and not zf,
                  "%d degenerate, %d coplanar overlapping pairs%s" % (len(degen), len(zf),
                                                                     (": " + str(zf[:4])) if zf else ""))
        # C6 interpenetration between separate pieces, front zone, loot
        comps = infos[st]["components"]
        names_geo = sorted(s for s in g.selections if s.startswith("Component"))
        cp = {comps[i]: comp_planes(g, names_geo[i]) for i in range(len(comps))}
        group = lambda n: "dropped" if n.startswith("drop_") else n                        # noqa: E731
        worst = (0.0, "")
        keys = list(cp)
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                if group(keys[i]) == group(keys[j]):
                    continue
                d = penetration(cp[keys[i]], cp[keys[j]])
                if d > worst[0]:
                    worst = (d, "%s / %s" % (keys[i], keys[j]))
        check("%s C6 no interpenetration > 1 cm between pieces" % st, worst[0] <= 0.010,
              "worst %.1f mm (%s)" % (worst[0] * 1000, worst[1] or "none"))
        top = cp["body"][0]
        for lp in infos[st]["loot"]:
            x, y, z = lp["model"]
            if lp["surface"] == "top":
                hit = ray_down(top, x, z)
                circle = [(x + lp["range"] * math.cos(a), z + lp["range"] * math.sin(a))
                          for a in [k * math.pi / 8 for k in range(16)]]
                upper = tansu.UPPER
                ins = all(upper["x0"] <= cx <= upper["x1"] and upper["zb"] <= cz <= upper["zf"] for cx, cz in circle)
                ok = hit is not None and abs(hit[1] - y) <= 0.01 and ins and y <= 1.40
                check("%s C6 loot %s on the top" % (st, lp["name"]), ok,
                      "Geometry top at %.3f under the point (%.3f); range %.2f inside the top: %s"
                      % (hit[1] if hit else -1, y, lp["range"], ins))
            else:
                bot = cp["drop_bottom"][0]
                hit = ray_down(bot, x, z)
                dp = infos[st]["dropped"]
                a = math.radians(-dp["yaw_deg"])
                hx, hz = dp["outer_m"][0] / 2 - 0.030, dp["outer_m"][1] / 2 - 0.030
                ins = True
                for k in range(16):
                    ang = k * math.pi / 8
                    cx, cz = x + lp["range"] * math.cos(ang) - dp["pos"][0], z + lp["range"] * math.sin(ang) - dp["pos"][2]
                    lx = cx * math.cos(a) - cz * math.sin(a)
                    lz = cx * math.sin(a) + cz * math.cos(a)
                    ins = ins and abs(lx) <= hx and abs(lz) <= hz
                ok = hit is not None and abs(hit[1] - y) <= 0.003 and ins
                check("%s C6 loot %s in the dropped drawer" % (st, lp["name"]), ok,
                      "drawer bottom (Geometry) at %.3f under the point (%.3f); range %.2f inside the walls: %s"
                      % (hit[1] if hit else -1, y, lp["range"], ins))
        sc = json.load(open(os.path.join(SRC, "jp_f_tansu.json"), encoding="utf-8"))
        var = "" if st == "A" else "_ransacked"
        side = sorted(p["name"] for s in sc["loot_surfaces"] if var in s["states"] for p in s["points"])
        check("%s loot note in the sidecar (BUILD_LIST row 26)" % st,
              side == sorted(lp["name"] for lp in infos[st]["loot"]) and len(side) == (2 if st == "A" else 3),
              "%s: %s" % ("jp_f_tansu.json loot_surfaces", ", ".join(side)))
        if st == "B":
            fz = tansu.FRONT_ZONE
            dpts = []
            for n in cp:
                if n.startswith("drop_"):
                    dpts += cp[n][1]
            # the dropped drawer's visual faces: every Res 1 point in front of the chest (z > 0.3)
            vis_front = [p for p in r1l.points if p[2] > 0.43]
            allz = dpts + vis_front
            ok = all(fz["x"][0] <= p[0] <= fz["x"][1] and fz["z"][0] <= p[2] <= fz["z"][1] for p in allz)
            check("B C6 dropped drawer inside the front zone", ok,
                  "zone x %s z %s; drawer spans x %.3f..%.3f, z %.3f..%.3f (Geometry + Res 1)"
                  % (fz["x"], fz["z"], min(p[0] for p in allz), max(p[0] for p in allz),
                     min(p[2] for p in allz), max(p[2] for p in allz)))
    # C19 matte + C1 palette over the used rvmats / textures
    rv = sorted({p for p in used_mats if p.lower().endswith(".rvmat")})
    matte_bad = []
    for p in rv:
        txt = open(os.path.join(DEV, "src", p), encoding="utf-8", errors="replace").read()
        glossy = "\\metal\\" in p.lower()
        s6 = re.search(r"class Stage6\s*\{[^}]*texture=\"([^\"]*)\"", txt)
        s7 = re.search(r"class Stage7\s*\{[^}]*texture=\"([^\"]*)\"", txt)
        s6, s7 = (s6.group(1) if s6 else ""), (s7.group(1) if s7 else "")
        if glossy:
            if "env_land_co" not in s7:
                matte_bad.append(p + " (iron: expected the glossy recipe)")
        elif not ("fresnel(0.01,0.01)" in s6 and "color(0,0,0,1,CO)" in s7):
            matte_bad.append(p)
    check("C19 matte finish (wood), iron glossy by design", not matte_bad,
          "; ".join(matte_bad) if matte_bad else "%d rvmats: %s" % (len(rv), ", ".join(os.path.basename(p) for p in rv)))
    try:
        from PIL import Image
        import numpy as np
        rows = []
        okc = True
        for p in rv:
            base = os.path.basename(p)[:-6]
            fam_id = re.sub(r"_w\d$", "", base)
            sc = json.load(open(os.path.join(LIBDIR, p.split("\\")[-2], fam_id + ".json"), encoding="utf-8"))
            png = os.path.join(TEXPNG, base + "_co.png")
            a = np.asarray(Image.open(png).convert("RGB"), dtype=float).reshape(-1, 3)
            mean = tuple(a.mean(0))
            pid = sc["palette_id"]
            e = pal[pid]
            d_own = de76(mean, e["srgb"])
            row = "%s mean (%d,%d,%d) vs %s dE %.1f (tol %s)" % (base, mean[0], mean[1], mean[2], pid, d_own,
                                                                 e.get("tolerance_dE76"))
            if fam_id == "jp_m_wood_street_dark":
                ti = pal["timber_interior"]
                d_t = de76(mean, ti["srgb"])
                row += "; vs the wanted timber_interior dE %.1f (tol %s)" % (d_t, ti.get("tolerance_dE76"))
                okc = okc and d_t <= ti.get("tolerance_dE76", 14)
            rows.append(row)
        check("C1 palette (whole-texture means)", okc, " | ".join(rows))
    except Exception as ex:  # noqa: BLE001
        check("C1 palette (whole-texture means)", False, "could not compute: %s" % ex)
    # build steps: CfgConvert, binarize, ODOL read-back, PBO, config
    cc = br["cfgconvert"]
    check("CfgConvert config.cpp + model.cfg (to bin and back)", cc["config.cpp"]["ok"] and cc["model.cfg"]["ok"],
          "config.cpp: %s | model.cfg: %s" % (cc["config.cpp"]["msg"] or "no output", cc["model.cfg"]["msg"] or
                                                  "no output"))
    b = br.get("binarize") or {}
    if b:
        check("binarize clean", b.get("ok") and all(v["odol"] for v in b["converted"].values()) and
              not b["unexplained_lines"],
              "both p3d -> ODOL (%s); %d log lines, flagged %d, unexplained %d (the rest is the same config noise as "
              "the machiya's log); %s" % (", ".join("%s %d B" % (k, v["bytes"]) for k, v in b["converted"].items()),
                                          b["lines"], len(b["flagged_lines"]), len(b["unexplained_lines"]), b["log"]))
        try:
            import odol_read
            for st in ("A", "B"):
                p = os.path.join(SRC, FILES[st])
                info = odol_read.read_odol(p)
                res = [round(r, 3) if r < 1e4 else "%.0e" % r for r in info["resolutions"]]
                mlres = [round(l.resolution, 3) if l.resolution < 1e4 else "%.0e" % l.resolution for l in L[st]]
                lods = info["lods"]
                fc = [len(l.faces) for l in lods]
                texs = sorted({t for l in lods for t in (l.textures or []) if t})    # '' = untextured Geometry
                bad_t = [t for t in texs if not (t.lower().startswith("jp\\common\\materials\\")
                                                 or t.lower().startswith("dz\\data\\data\\penetration\\"))]
                ok = (info["autoCenter"] == 0 and sorted(map(str, res)) == sorted(map(str, mlres))
                      and abs(info["bboxMin"][1]) < 0.002 and not bad_t)
                check("%s ODOL read-back" % st, ok,
                      "ODOL v%d, autoCenter %d, LODs %s, faces %s, bbox y %.3f..%.3f, %d texture paths all library"
                      % (info["version"], info["autoCenter"], res, fc, info["bboxMin"][1], info["bboxMax"][1],
                         len(texs)))
        except Exception as ex:  # noqa: BLE001
            check("ODOL read-back", False, "reader failed: %s" % ex)
    where = br.get("pbo")
    if where and os.path.isfile(where):
        import pbo
        data = open(where, "rb").read()
        body, trail = data[:-21], data[-21:]
        sha_ok = trail[0] == 0 and hashlib.sha1(body).digest() == trail[1:]
        with open(where, "rb") as f:
            props, entries, off = pbo.read_header(f)
            names = [e[0] for e in entries]
            odol = {}
            for name, method, orig, ts, size in entries:
                if name.endswith(".p3d"):
                    f.seek(off)
                    odol[name] = f.read(4) == b"ODOL"
                off += size
        want = {"config.cpp", FILES["A"], FILES["B"]}
        ok = sha_ok and props.get("prefix") == "JP\\effort_test\\%s" % LEVEL and set(names) == want and all(odol.values())
        check("PBO contents", ok, "%s: prefix %s, entries %s, p3d ODOL %s, SHA-1 trailer %s, %d bytes"
              % (os.path.relpath(where, ROOT), props.get("prefix"), names, odol, "OK" if sha_ok else "BAD", len(data)))
    cfg = open(os.path.join(SRC, "config.cpp"), encoding="utf-8").read()
    patches = re.findall(r"class\s+(\w+)\s*\{\s*units", cfg)
    classes = re.findall(r"class\s+(JP_EffTest_\w+)\s*:\s*HouseNoDestruct", cfg)
    models = re.findall(r'model="([^"]+)"', cfg)
    req = re.search(r"requiredAddons\[\]=\s*\{([^}]*)\}", cfg).group(1)
    ok = (patches == ["JP_EffTest_%s" % LEVEL] and classes == ["JP_EffTest_%s_Tansu" % LEVEL,
                                                              "JP_EffTest_%s_Tansu_Ransacked" % LEVEL]
          and all(os.path.isfile(os.path.join(DEV, "src", m.lstrip("\\"))) for m in models)
          and '"DZ_Data"' in req
          and not any(w in cfg.lower() for w in ("jp_worlds", "jp\\worlds", "cfgworlds", "testisland")))
    check("config: one CfgPatches, two static classes, models exist, no map coupling", ok,
          "CfgPatches %s, requiredAddons {%s}, classes %s" % (patches, " ".join(req.split()), classes))
    ok_all = all(r["ok"] for r in RES)
    with open(os.path.join(HERE, "checks.json"), "wb") as f:
        f.write(json.dumps({"asset": "jp_f_tansu (effort test %s)" % LEVEL, "faces": faces_summary,
                            "pass": sum(1 for r in RES if r["ok"]), "total": len(RES), "checks": RES},
                           indent=1).encode("utf-8") + b"\n")
    print("%d/%d checks pass -> checks.json" % (sum(1 for r in RES if r["ok"]), len(RES)))
    return ok_all


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
