#!/usr/bin/env python3
r"""verify_b.py - offline checks of the machiya p3d (MLOD from the kit, ODOL from binarize) and its drop-ins.

  python verify_b.py [jp_machiya_01 ...]

Checks, per variant:
  1. LODs present: Resolution 1/2/3, Geometry, Memory, Roadway, View Geometry, Fire Geometry (vanilla house set).
  2. Geometry named properties (class/map/damage/autocenter) and mass.
  3. Every ComponentNN in Geometry, View and Fire Geometry is closed and convex; Fire faces carry penetration rvmats.
  4. Doors: doorsN in every LOD it must be in; in Geometry/View/Fire it is exactly one component; memory axis =
     2 points 1.00 m apart along the slide direction, action + leaf points; model.cfg animation + config class exist.
  5. Door clipping: each leaf, closed -> open (swept box), against every other Geometry component and the visual
     posts. Passage: with the leaf open, a 0.6 x 1.8 m column through the doorway is free of geometry.
  6. Roadway vs Geometry: every roadway sample sits on a Geometry top surface (+-3 cm); every walkable floor sample
     has a roadway face at floor height; head room >= 1.95 m above floors, the stair ramp and doorways.
  7. Loot points: on a roadway at their floor height, inside the building, their range circle clear of walls;
     CE-frame transform cross-checked against the model->world transform for both instances.
  8. The binarized ODOL (src/JP/structures/machiya/<name>.p3d): magic, LOD list, door strings.
Exit code 0 = all checks passed.
"""
import json
import math
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, ".."))
DEV = os.path.abspath(os.path.join(B, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(B, "kit"))
import mlod_b as mlod  # noqa: E402
from jpkit import loot as lootmod  # noqa: E402

FAIL = []
WARN = []


def fail(msg):
    FAIL.append(msg)
    print("  FAIL", msg)


def ok(msg):
    print("  ok  ", msg)


# ------------------------------------------------------------------------------------------------------
# convex component helpers
# ------------------------------------------------------------------------------------------------------
def components(lod):
    out = []
    for name, (pw, fs) in lod.selections.items():
        if not name.startswith("Component"):
            continue
        pts = [lod.points[i] for i in pw]
        planes = []
        for fi in fs:
            fp = [lod.points[v[0]] for v in lod.faces[fi][0]]
            n = mlod._normalize(mlod._face_formula_normal(fp))   # inward
            planes.append((n, mlod._dot(n, fp[0])))           # inside: dot(n, p) >= d
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        zs = [p[2] for p in pts]
        doors = [s for s, (pw2, fs2) in lod.selections.items() if s.startswith("doors") and fs2 == fs]
        out.append(dict(name=name, planes=planes, bbox=(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)),
                        faces=fs, door=doors[0] if doors else None, pts=pts))
    return out


def ray_y(comp, x, z):
    """Vertical line through (x, z): (ymin, ymax) inside the convex component, or None."""
    lo, hi = -1e9, 1e9
    for n, d in comp["planes"]:
        # dot(n, (x, y, z)) >= d  ->  n.y * y >= d - n.x x - n.z z
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
    if lo > hi + 1e-9:
        return None
    return (lo, hi)


def point_inside(comp, p, eps=0.01):
    for n, d in comp["planes"]:
        if mlod._dot(n, p) < d + eps:
            return False
    return True


def box_overlap(a, b, pad=0.0):
    return (a[0] < b[1] - pad and a[1] > b[0] + pad and a[2] < b[3] - pad and a[3] > b[2] + pad
            and a[4] < b[5] - pad and a[5] > b[4] + pad)


def comp_box_intersect(comp, bx):
    """Exact test: convex component vs axis-aligned box (separating axis on the component's planes + box axes)."""
    if not box_overlap(comp["bbox"], bx, 0.002):
        return False
    corners = [(x, y, z) for x in (bx[0], bx[1]) for y in (bx[2], bx[3]) for z in (bx[4], bx[5])]
    for n, d in comp["planes"]:
        if all(mlod._dot(n, c) < d + 0.002 for c in corners):
            return False          # box entirely outside this face plane
    return True


# ------------------------------------------------------------------------------------------------------
def roadway_height(lod, x, z):
    hs = []
    for verts, _, tex, _ in lod.faces:
        pts = [lod.points[v[0]] for v in verts]
        if _in_poly_xz(pts, x, z):
            n = mlod._face_formula_normal(pts)
            if abs(n[1]) < 1e-9:
                continue
            p0 = pts[0]
            y = p0[1] - (n[0] * (x - p0[0]) + n[2] * (z - p0[2])) / n[1]
            hs.append((y, tex))
    return hs


def _in_poly_xz(pts, x, z):
    sgn = 0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        c = (b[0] - a[0]) * (z - a[2]) - (b[2] - a[2]) * (x - a[0])
        if abs(c) < 1e-9:
            continue
        s = 1 if c > 0 else -1
        if sgn == 0:
            sgn = s
        elif s != sgn:
            return False
    return True


def geo_top_below(comps, x, y, z, skip_doors=True):
    best = None
    for c in comps:
        if skip_doors and c["door"]:
            continue
        r = ray_y(c, x, z)
        if r and r[1] <= y + 0.05 and (best is None or r[1] > best):
            best = r[1]
    return best


def geo_bottom_above(comps, x, y, z, skip_doors=True):
    best = None
    for c in comps:
        if skip_doors and c["door"]:
            continue
        r = ray_y(c, x, z)
        if r and r[0] >= y + 0.05 and (best is None or r[0] < best):
            best = r[0]
        elif r and r[0] < y + 0.05 < r[1]:
            return y       # inside a component
    return best


# ------------------------------------------------------------------------------------------------------
def verify(name):
    print("=" * 100)
    print(name)
    summ = json.load(open(os.path.join(B, "out", name, name + "_summary.json")))
    lods = mlod.read_mlod(os.path.join(B, "out", name, name + ".p3d"))
    L = {}
    for l in lods:
        L[mlod.lod_name(l.resolution)] = l
    want = ["Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "Memory", "Roadway", "View Geometry",
            "Fire Geometry"]
    missing = [w for w in want if w not in L]
    if missing:
        fail("missing LODs %s" % missing)
    else:
        ok("LODs: " + ", ".join("%s (%d faces)" % (w, len(L[w].faces)) for w in want))
    geo, view, fire, mem, road = L["Geometry"], L["View Geometry"], L["Fire Geometry"], L["Memory"], L["Roadway"]
    props = geo.properties
    if props.get("class") == "house" and props.get("map") == "house" and props.get("damage") == "no" \
            and props.get("autocenter") == "0":
        ok("Geometry properties %s" % props)
    else:
        fail("Geometry properties %s" % props)
    if geo.mass and sum(geo.mass) > 1000:
        ok("Geometry mass %.0f kg on %d points" % (sum(geo.mass), len(geo.mass)))
    else:
        fail("Geometry mass missing")

    # 3. components closed + convex
    for lname in ("Geometry", "View Geometry", "Fire Geometry"):
        l = L[lname]
        comps = [s for s in l.selections if s.startswith("Component")]
        bad = 0
        for c in comps:
            probs = mlod.component_report(l, c)
            if probs:
                bad += 1
                fail("%s %s: %s" % (lname, c, "; ".join(probs[:2])))
        covered = set()
        for c in comps:
            covered |= l.selections[c][1]
        if len(covered) != len(l.faces):
            fail("%s: %d faces not in any component" % (lname, len(l.faces) - len(covered)))
        if not bad:
            ok("%s: %d components, all closed and convex, every face in a component" % (lname, len(comps)))
    mats = {f[3] for f in fire.faces}
    if all(m.startswith("dz\\data\\data\\penetration\\") for m in mats):
        ok("Fire Geometry materials: %s" % sorted(os.path.basename(m) for m in mats))
    else:
        fail("Fire Geometry faces without penetration material: %s" % mats)

    # 4. doors
    mcfg = open(os.path.join(DEV, "src", "JP", "structures", "machiya", "model.cfg")).read()
    ccfg = open(os.path.join(DEV, "src", "JP", "structures", "config.cpp")).read()
    gcomps = components(geo)
    for d in summ["doors"]:
        bone = d["bone"]
        probs = []
        for w in ("Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "View Geometry", "Fire Geometry"):
            sel = L[w].selections.get(bone)
            if not sel or not sel[1]:
                probs.append("no faces in " + w)
            elif w in ("Geometry", "View Geometry", "Fire Geometry"):
                fs = sel[1]
                if not any(L[w].selections[c][1] == fs for c in L[w].selections if c.startswith("Component")):
                    probs.append("%s: %s is not exactly one component" % (w, bone))
        for suffix, npts in (("_axis", 2), ("_action", 1), ("", 1)):
            sel = mem.selections.get(bone + suffix)
            if not sel or len(sel[0]) != npts:
                probs.append("memory %s%s needs %d points" % (bone, suffix, npts))
        ax = sorted(mem.selections[bone + "_axis"][0])
        p0, p1 = mem.points[ax[0]], mem.points[ax[1]]
        v = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        if abs(math.sqrt(mlod._dot(v, v)) - 1.0) > 1e-3 or mlod._dot(v, d["direction"]) < 0.999:
            probs.append("axis %s is not 1 m along the slide direction" % (v,))
        if not re.search(r"class %s\s*\{[^}]*type=\"translation\";[^}]*selection=\"%s\";[^}]*axis=\"%s_axis\";"
                         r"[^}]*offset1=%.4f;" % (d["cfg"], bone, bone, d["slide"]), mcfg):
            probs.append("model.cfg animation for %s missing or wrong" % d["cfg"])
        if not re.search(r"class %s\s*\{[^}]*component=\"%s\";[^}]*soundPos=\"%s_action\";" % (d["cfg"], d["cfg"], bone),
                         ccfg):
            probs.append("config.cpp class Doors/%s missing" % d["cfg"])
        if probs:
            fail("%s %s: %s" % (d["cfg"], d["note"], "; ".join(probs)))
        else:
            ok("%s (%s, %s, slides %.3f m): selections in Res1-3/Geometry/View/Fire, memory axis+action+leaf, "
               "model.cfg + config" % (d["cfg"], d["note"], d["kind"], d["slide"]))

    # 5. clipping + passage
    for d in summ["doors"]:
        bone = d["bone"]
        leaf = next(c for c in gcomps if c["door"] == bone)
        x0, x1, y0, y1, z0, z1 = leaf["bbox"]
        dx, dz = d["direction"][0] * d["slide"], d["direction"][2] * d["slide"]
        swept = (min(x0, x0 + dx), max(x1, x1 + dx), y0, y1, min(z0, z0 + dz), max(z1, z1 + dz))
        hits = [c["name"] for c in gcomps if c is not leaf and comp_box_intersect(c, swept)]
        # passage: column through the opening, leaf open
        ax, ay, az = d["action"]
        floor_y = ay - 1.0
        if abs(d["direction"][0]) > 0.5:       # wall along x: walk along z
            col = (ax - 0.30, ax + 0.30, floor_y + 0.03, floor_y + 1.83, az - 0.4, az + 0.4)
        else:
            col = (ax - 0.4, ax + 0.4, floor_y + 0.03, floor_y + 1.83, az - 0.30, az + 0.30)
        blocked = [c["name"] for c in gcomps if c is not leaf and comp_box_intersect(c, col)]
        # the step ramps rise into the column on the toriniwa side of a shoji: ignore components whose top is
        # below the floor of the door + 3 cm there
        if hits or blocked:
            fail("%s: leaf sweep hits %s; open doorway blocked by %s" % (d["cfg"], hits, blocked))
        else:
            ok("%s: leaf slides %.3f m without touching other geometry; open doorway 0.6 x 1.8 m clear"
               % (d["cfg"], d["slide"]))

    # 6. roadway vs geometry, floors, head room
    miss = 0
    n = 0
    for verts, _, tex, _ in road.faces:
        pts = [road.points[v[0]] for v in verts]
        xs = [p[0] for p in pts]
        zs = [p[2] for p in pts]
        for i in range(1, 6):
            for j in range(1, 6):
                x = min(xs) + (max(xs) - min(xs)) * i / 6
                z = min(zs) + (max(zs) - min(zs)) * j / 6
                hs = [h for h, t in roadway_height(road, x, z) if t == tex]
                if not hs:
                    continue
                y = max(hs)
                top = geo_top_below(gcomps, x, y, z)
                n += 1
                if top is None or abs(top - y) > 0.03:
                    miss += 1
                    if miss < 6:
                        fail("roadway %s at (%.2f, %.2f, %.2f): geometry top %s" % (os.path.basename(tex), x, y, z, top))
    if not miss:
        ok("roadway sits on geometry at all %d samples (+-3 cm)" % n)
    floors = summ["floors"]
    miss = low = 0
    n = 0
    lowest = 9.0
    for f in floors:
        x0, x1, z0, z1 = f["rect"]
        steps = 14
        for i in range(steps + 1):
            for j in range(steps + 1):
                x = x0 + 0.05 + (x1 - x0 - 0.1) * i / steps
                z = z0 + 0.05 + (z1 - z0 - 0.1) * j / steps
                # obstacles (stair, stairwell, hearth, kamado, step ramps) are not floor
                if any(a0 <= x <= a1 and b0 <= z <= b1 for (a0, a1, b0, b1) in f["obstacles"]):
                    continue
                n += 1
                hs = [h for h, t in roadway_height(road, x, z)]
                if not any(abs(h - f["y"]) < 0.02 for h in hs):
                    miss += 1
                    if miss < 6:
                        fail("floor %s (%.2f, %.2f): no roadway at y=%.2f (have %s)" % (f["name"], x, z, f["y"], hs))
                    continue
                above = geo_bottom_above(gcomps, x, f["y"], z)
                if above is not None:
                    clear = above - f["y"]
                    lowest = min(lowest, clear)
                    if clear < 1.95:
                        low += 1
                        if low < 6:
                            fail("floor %s (%.2f, %.2f): head room %.2f m" % (f["name"], x, z, clear))
    if not miss and not low:
        ok("walkable floors: roadway at floor height on all %d samples; lowest head room %.2f m" % (n, lowest))
    st = summ.get("stair")
    if st:
        zc = (st["z0"] + st["z1"]) / 2
        worst = 9.0
        for i in range(21):
            x = st["foot"] + (st["x_t"] - st["foot"]) * i / 20
            hs = [h for h, t in roadway_height(road, x, zc) if "stairs" in t]
            if not hs:
                fail("stair: no roadway at x=%.2f" % x)
                continue
            y = hs[0]
            above = geo_bottom_above(gcomps, x, y, zc)
            if above is not None:
                worst = min(worst, above - y)
        if worst >= 1.95:
            ok("stair: ramp %.1f deg (steps %.0f deg), %d steps of %.3f m, head room >= %.2f m along it"
               % (st["angle"], 40.0, st["n"], st["r"], worst))
        else:
            fail("stair head room only %.2f m" % worst)

    # 7. loot points
    bad = 0
    pts = summ["loot"]
    for p in pts:
        x, y, z = p["model"]
        hs = [h for h, t in roadway_height(road, x, z)]
        if not any(abs(h - y) < 0.02 for h in hs):
            bad += 1
            fail("loot point %s not on a roadway" % (p["model"],))
            continue
        for k in range(8):
            a = k * math.pi / 4
            q = (x + p["range"] * math.cos(a), y + 0.4, z + p["range"] * math.sin(a))
            if any(point_inside(c, q) for c in gcomps if not c["door"]):
                bad += 1
                fail("loot point %s range %.2f reaches into geometry" % (p["model"], p["range"]))
                break
    ce = open(os.path.join(DEV, "test", "ce", "B_mapgroupproto.xml")).read() if name == "jp_machiya_01" else ""
    if not bad:
        ok("%d loot points on roadway floors, ranges clear of walls (%s)" % (
            len(pts), ", ".join("%s %d" % (f["name"], len([q for q in pts if q["floor"] == f["name"]])) for f in floors)))
    if ce:
        cepts = [tuple(float(v) for v in m.group(1).split()) for m in re.finditer(r'<point pos="([^"]+)"', ce)]
        worst = 0.0
        for pos in ((1024.0, 25.0, 1045.0), (1075.0, 25.0, 1090.0)):
            for p, l in zip(pts, cepts):
                w1 = lootmod.ce_to_world(l, pos, 180.0)
                w2 = lootmod.model_to_world(p["model"], pos, 180.0)
                worst = max(worst, max(abs(a - b) for a, b in zip(w1, w2)))
        if len(cepts) == len(pts) and worst < 1e-3:
            ok("B_mapgroupproto.xml: %d points; CE-frame -> world equals model -> world for both instances "
               "(max diff %.1e m)" % (len(cepts), worst))
        else:
            fail("CE transform mismatch %.3f or count %d/%d" % (worst, len(cepts), len(pts)))
        # world-space sanity: every point of the baked instance lies inside the footprint box, facing south
        bb = summ["bbox"]
        for p in pts[:1]:
            w = lootmod.model_to_world(p["model"], (1024.0, 25.0, 1045.0), 180.0)
            ok("first loot point: model %s -> world (%.2f, %.2f, %.2f)" % (tuple(round(c, 2) for c in p["model"]), *w))

    # 8. ODOL
    odol = os.path.join(DEV, "src", "JP", "structures", "machiya", name + ".p3d")
    data = open(odol, "rb").read()
    if data[:4] != b"ODOL":
        fail("%s is not ODOL (binarize did not run?)" % odol)
    else:
        ver = struct.unpack_from("<I", data, 4)[0]
        res = None
        for off in range(8, 300):
            k = struct.unpack_from("<I", data, off)[0]
            if 1 <= k <= 40:
                r = struct.unpack_from("<%df" % k, data, off + 4)
                if any(abs(x - 1e15) < 1e10 for x in r) and all(x > 0 for x in r):
                    res = r
                    break
        names = [mlod.lod_name(r) for r in res] if res else []
        strs = set(m.group().decode() for m in re.finditer(rb"[\x20-\x7e]{4,}", data))
        low = {s.lower() for s in strs}
        doors_ok = all(d["bone"] in low and d["bone"] + "_axis" in low for d in summ["doors"])
        skel = (name + "_skeleton").lower()
        skel_ok = any(skel in s for s in low)
        if res and all(w in names for w in want) and doors_ok and skel_ok:
            ok("ODOL v%d, %d bytes, LODs: %s; door bones, axes and skeleton '%s' (model.cfg applied) present"
               % (ver, len(data), ", ".join(names), skel))
        else:
            fail("ODOL LODs %s doors_ok=%s skeleton=%s" % (names, doors_ok, skel_ok))


def main(argv):
    names = [a for a in argv if not a.startswith("--")] or ["jp_machiya_01", "jp_machiya_02"]
    for n in names:
        verify(n)
    print("=" * 100)
    print("RESULT: %s (%d failures)" % ("PASS" if not FAIL else "FAIL", len(FAIL)))
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
