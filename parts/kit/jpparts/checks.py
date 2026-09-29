"""Per-part and per-assembly checks (PLAYBOOK §12, grown from B's verify_b.py), run on the MLOD read back from disk.

C1  matcheck (materials, separate script)       C2  library-only paths             C3  grid snap of connectors
C4  dimensions vs the build list (+-1 cm)        C5  LODs + face counts              C7  closed convex components,
door selections + memory, leaf sweep clear, >= 1.00 m clear opening, >= 2.00 m head, Roadway on Geometry.
"""
import math
import os
import re

from . import mlod, raycheck
from .core import HALF, QK, MIN_CLEAR, MIN_HEAD, LIB, DEV, POST, WALL_H

ALLOWED_VANILLA = ("dz\\data\\data\\penetration\\", "dz\\surfaces\\data\\roadway\\")


def components(lod):
    out = []
    for name, (pw, fs) in lod.selections.items():
        if not name.startswith("Component"):
            continue
        pts = [lod.points[i] for i in pw]
        planes = []
        for fi in fs:
            fp = [lod.points[v[0]] for v in lod.faces[fi][0]]
            n = mlod._normalize(mlod._face_formula_normal(fp))          # inward
            planes.append((n, mlod._dot(n, fp[0])))
        xs, ys, zs = [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts]
        doors = [s for s, (pw2, fs2) in lod.selections.items() if s.startswith("doors") and fs2 and fs <= fs2]
        out.append(dict(name=name, planes=planes, bbox=(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)),
                        door=doors[0] if doors else None, pts=pts))
    return out


def box_comp(x0, x1, y0, y1, z0, z1, name="virtual_post"):
    planes = [((1.0, 0.0, 0.0), x0), ((-1.0, 0.0, 0.0), -x1), ((0.0, 1.0, 0.0), y0), ((0.0, -1.0, 0.0), -y1),
              ((0.0, 0.0, 1.0), z0), ((0.0, 0.0, -1.0), -z1)]
    return dict(name=name, planes=planes, bbox=(x0, x1, y0, y1, z0, z1), door=None, pts=[])


def comp_box_intersect(comp, bx, pad=0.002):
    b = comp["bbox"]
    if not (b[0] < bx[1] - pad and b[1] > bx[0] + pad and b[2] < bx[3] - pad and b[3] > bx[2] + pad
            and b[4] < bx[5] - pad and b[5] > bx[4] + pad):
        return False
    corners = [(x, y, z) for x in (bx[0], bx[1]) for y in (bx[2], bx[3]) for z in (bx[4], bx[5])]
    for n, d in comp["planes"]:
        if all(mlod._dot(n, c) < d + pad for c in corners):
            return False
    return True


def shifted(comp, dx, dy, dz):
    c = dict(comp)
    c["planes"] = [(n, d + n[0] * dx + n[1] * dy + n[2] * dz) for n, d in comp["planes"]]
    b = comp["bbox"]
    c["bbox"] = (b[0] + dx, b[1] + dx, b[2] + dy, b[3] + dy, b[4] + dz, b[5] + dz)
    return c


def ray_y(comp, x, z):
    lo, hi = -1e9, 1e9
    for n, d in comp["planes"]:
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


def roadway_samples(road):
    out = []
    for verts, _, tex, _ in road.faces:
        pts = [road.points[v[0]] for v in verts]
        n = mlod._face_formula_normal(pts)
        if abs(n[1]) < 1e-9:
            continue
        xs, zs = [p[0] for p in pts], [p[2] for p in pts]
        for i in range(1, 5):
            for j in range(1, 5):
                x = min(xs) + (max(xs) - min(xs)) * i / 5
                z = min(zs) + (max(zs) - min(zs)) * j / 5
                if not _in_poly_xz(pts, x, z):
                    continue
                p0 = pts[0]
                y = p0[1] - (n[0] * (x - p0[0]) + n[2] * (z - p0[2])) / n[1]
                out.append((x, y, z, tex))
    return out


def on_grid(v, step=QK, tol=0.005):
    return abs(v / step - round(v / step)) * step <= tol


def check_part(part, path, lods=None):
    """Returns (results list [(check, ok, detail)], lod face counts)."""
    res = []
    lods = mlod.read_mlod(path) if lods is None else lods
    L = {mlod.lod_name(l.resolution): l for l in lods}
    counts = {k: len(v.faces) for k, v in L.items()}
    res.append(("C5 LODs", "Resolution 1" in L, ", ".join("%s %d" % kv for kv in counts.items())))
    # C2 library only
    bad = set()
    for l in lods:
        for _, _, tex, mat in l.faces:
            for pth in (tex, mat):
                if not pth:
                    continue
                pl = pth.lower()
                if pl.startswith(ALLOWED_VANILLA):
                    continue
                if pl.startswith("jp\\common\\materials\\"):
                    if not os.path.isfile(os.path.join(DEV, "src", pth)):
                        bad.add(pth + " (missing)")
                    continue
                bad.add(pth)
    res.append(("C2 library only", not bad, "%d paths bad: %s" % (len(bad), sorted(bad)[:3]) if bad else "all paths "
                "under JP\\common\\materials\\ (on disk) or vanilla penetration/roadway"))
    # C7 components
    for lname in ("Geometry", "View Geometry", "Fire Geometry"):
        if lname not in L:
            continue
        l = L[lname]
        comps = [s for s in l.selections if s.startswith("Component")]
        probs = []
        for c in comps:
            pr = mlod.component_report(l, c)
            if pr:
                probs.append("%s: %s" % (c, pr[0]))
        covered = set()
        for c in comps:
            covered |= l.selections[c][1]
        if len(covered) != len(l.faces):
            probs.append("%d faces outside components" % (len(l.faces) - len(covered)))
        res.append(("C7 %s closed+convex" % lname, not probs, "%d components%s" % (len(comps), "; " + "; ".join(probs[:3])
                                                                                    if probs else ", all closed and convex")))
    if "Fire Geometry" in L:
        mats = {f[3] for f in L["Fire Geometry"].faces}
        okf = all(m.startswith("dz\\data\\data\\penetration\\") for m in mats)
        res.append(("C7 Fire penetration mats", okf, ", ".join(sorted(os.path.basename(m)[:-6] for m in mats))))
    # doors
    geo = L.get("Geometry")
    gcomps = components(geo) if geo else []
    mem = L.get("Memory")
    # the part's own post nodes stand in for the jp_p_frame_post parts the building adds (sweep / clear width)
    vposts = [box_comp(c["pos"][0] - 0.06, c["pos"][0] + 0.06, c["pos"][1], c["pos"][1] + 2.70, c["pos"][2] - 0.06,
                       c["pos"][2] + 0.06) for c in part.connectors if c["type"] == "post" and not c.get("hidden")]
    for d in part.doors:
        probs = []
        for a in d.anims:
            b = a["bone"]
            for w in ("Resolution 1", "Geometry", "View Geometry", "Fire Geometry"):
                if w in L and w != "Resolution 1" and not getattr(d, "has_%s" % w.split()[0].lower(), True):
                    continue
                sel = L[w].selections.get(b) if w in L else None
                if w in ("Resolution 1", "Geometry") and (not sel or not sel[1]):
                    probs.append("%s: no faces in %s" % (b, w))
            sel = mem.selections.get(b + "_axis") if mem else None
            if not sel or len(sel[0]) != 2:
                probs.append("%s_axis needs 2 memory points" % b)
            else:
                ps = [mem.points[i] for i in sorted(sel[0])]
                ln = math.dist(ps[0], ps[1])
                if a["type"] == "translation" and abs(ln - 1.0) > 1e-3:
                    probs.append("%s axis %.3f m (must be 1.00)" % (b, ln))
        ds = d.anims[0]["bone"]
        act = getattr(d, "twin", None) or ds          # twin doors (vanilla DoorsTwinN): one action point for both leaves
        for nm in (act + "_action", ds):
            if not mem or not mem.selections.get(nm):
                probs.append("memory %s missing" % nm)
        if getattr(d, "twin", None):
            for w in ("Resolution 1", "Geometry"):
                if w in L and not (L[w].selections.get(d.twin) or ({}, set()))[1]:
                    probs.append("%s: twin selection %s has no faces" % (w, d.twin))
        res.append(("C7 door %s selections+memory" % ds, not probs, "; ".join(probs) if probs else
                    "%s, %d bone(s), axis/action/leaf points" % (d.anims[0]["type"], len(d.anims))))
        if getattr(d, "passable", True) and d.anims[0]["type"] == "translation" and geo:
            r = door_sweep(d, gcomps + vposts)
            res.append(("C7 door %s sweep + clear" % ds, r[0], r[1]))
        elif geo:
            hits = sweep_hits(d, gcomps + vposts)
            res.append(("C7 door %s sweep (window / hinged)" % ds, not hits, "moves closed -> open without touching "
                        "other geometry" if not hits else "HITS %s" % hits[:3]))
        if d.anims[0]["type"] == "translation" and geo:
            st = stub_left(d, gcomps)
            res.append(("C10 door %s open leaf keeps >= 0.15 m in the opening (vanilla)" % ds, st >= 0.15 - 1e-6,
                        "%.3f m of the leaf stays in the opening when open" % st))
            pp = raycheck.pull_positions(d, gcomps, part.solids)
            if pp:
                res.append(("C18 door %s pulls on the stub edge (still in the doorway when open)" % ds,
                            all(x[4] for x in pp), "; ".join("%s pull u %.2f closed -> %.2f open, doorway %.2f..%.2f"
                                                             % (x[0], x[1], x[2], x[3][0], x[3][1]) for x in pp)))
        if "View Geometry" in L:
            vcomps = components(L["View Geometry"]) + virtual_walls(part, d) + vposts
            for frac, state in ((1.0, "open"), (0.0, "closed")):
                rr = raycheck.door_reach(d, vcomps, part.memory, frac=frac, others=part.doors)
                bad = [k for k, (ok, _) in rr.items() if not ok]
                res.append(("C10 door %s reachable from both sides (%s)" % (ds, state), not bad,
                            "; ".join("%s: %s" % (k, v[1]) for k, v in rr.items())))
    # tile seating (kawara on a clay bed, fascia at the eave)
    ts = tile_seating(part)
    if ts is not None:
        res.append(("C13 kawara seated on the clay bed (gap <= 1 cm), fascia at every eave", ts[0], ts[1]))
    # roadway on geometry
    if part.walkable:
        if "Roadway" not in L:
            res.append(("C7 Roadway", False, "walkable part without Roadway"))
        else:
            smp = roadway_samples(L["Roadway"])
            miss = 0
            for x, y, z, tex in smp:
                tops = [r[1] for c in gcomps if not c["door"] for r in [ray_y(c, x, z)] if r and r[1] <= y + 0.05]
                if not tops or abs(max(tops) - y) > 0.03:
                    miss += 1
            res.append(("C7 Roadway on Geometry", miss == 0, "%d/%d samples on a Geometry top (+-3 cm)"
                        % (len(smp) - miss, len(smp))))
    # C4 dims
    for dm in part.dims:
        ok = dim_ok(dm)
        res.append(("C4 %s" % dm["name"], ok, "expected %s, measured %s" % (dm["expected"], dm["measured"])))
    # C3 grid
    offg = [c for c in part.connectors if c["type"] in ("post", "sill", "stair_foot", "stair_head")
            and not (on_grid(c["pos"][0]) and on_grid(c["pos"][2]))]
    res.append(("C3 grid snap", not offg, "%d connectors, %s" % (len(part.connectors), "all post/sill nodes on the 0.455 grid"
                                                                  if not offg else "off-grid: %s" % offg[:2])))
    return res, counts


def dim_ok(dm):
    if "ok" in dm:
        return bool(dm["ok"])
    e, m, tol = dm["expected"], dm["measured"], dm.get("tol", 0.01)
    if isinstance(e, (int, float)):
        return abs(float(e) - float(m)) <= tol + 1e-9
    mm = re.match(r"^\s*([0-9.]+)\s*-\s*([0-9.]+)", str(e))
    if mm and isinstance(m, (int, float)):
        return float(mm.group(1)) - tol <= m <= float(mm.group(2)) + tol
    return True


def door_sweep(d, gcomps):
    """Every leaf swept closed -> open against every other Geometry component; then the clear opening with all the
    door's leaves open."""
    bones = [a["bone"] for a in d.anims]
    others = [c for c in gcomps if c["door"] not in bones]
    hits, opened = [], []
    for a in d.anims:
        leaf = [c for c in gcomps if c["door"] == a["bone"]]
        if not leaf:
            return False, "no leaf component for %s" % a["bone"]
        amt = a["amount"]
        dv = [(a["axis"][1][k] - a["axis"][0][k]) for k in range(3)]
        lb = [c["bbox"] for c in leaf]
        x0, x1 = min(b[0] for b in lb), max(b[1] for b in lb)
        y0, y1 = min(b[2] for b in lb), max(b[3] for b in lb)
        z0, z1 = min(b[4] for b in lb), max(b[5] for b in lb)
        sw = (min(x0, x0 + dv[0] * amt), max(x1, x1 + dv[0] * amt), min(y0, y0 + dv[1] * amt),
              max(y1, y1 + dv[1] * amt), min(z0, z0 + dv[2] * amt), max(z1, z1 + dv[2] * amt))
        sw_in = (sw[0] + 0.004, sw[1] - 0.004, sw[2] + 0.004, sw[3] - 0.004, sw[4] + 0.002, sw[5] - 0.002)
        hits += [c["name"] for c in others if comp_box_intersect(c, sw_in)]
        opened += [shifted(c, dv[0] * amt, dv[1] * amt, dv[2] * amt) for c in leaf]
    amt = d.anims[0]["amount"]
    obst = others + opened
    o0, o1, b0, b1 = d.opening
    ax_ = (o0 + o1) / 2
    zf = d.z_face
    # scan the free interval along the wall around the doorway centre, body column 0.05..(head-0.05)
    top = min(b1, b0 + MIN_HEAD) - 0.05

    def free(x):
        col = (x - 0.004, x + 0.004, b0 + 0.05, top, zf - 0.35, zf + 0.35)
        return not any(comp_box_intersect(c, col, 0.0) for c in obst)
    if not free(ax_):
        return False, "doorway centre blocked (sweep hits %s)" % hits
    lo = ax_
    while lo > ax_ - 3 and free(lo - 0.01):
        lo -= 0.01
    hi = ax_
    while hi < ax_ + 3 and free(hi + 0.01):
        hi += 0.01
    clear = hi - lo
    # head room through the doorway (lowest obstacle bottom above the sill across the clear width)
    head = 99.0
    for c in obst:
        b = c["bbox"]
        if b[0] < hi and b[1] > lo and b[4] < zf + 0.3 and b[5] > zf - 0.3 and b[2] > b0 + 0.5:
            head = min(head, b[2] - b0)
    d.clear = clear
    d.head = head
    ok = not hits and clear >= MIN_CLEAR - 1e-6 and head >= MIN_HEAD - 0.005
    return ok, "leaf slides %.3f m %s; open clear width %.2f m (>= %.2f), head %.2f m%s" % (
        amt, "without touching other geometry" if not hits else "HITS %s" % hits[:3], clear, MIN_CLEAR,
        head if head < 99 else float("nan"), "" if ok else " FAIL")


def sweep_hits(d, gcomps, steps=8):
    """Any leaf of the door (translation or rotation) touching another Geometry component on its way open."""
    bones = [a["bone"] for a in d.anims]
    others = [c for c in gcomps if c["door"] not in bones]
    hits = []
    for a in d.anims:
        leaf = [c for c in gcomps if c["door"] == a["bone"]]
        for k in range(1, steps + 1):
            f = raycheck.anim_point_fn(a, k / steps)
            for c in leaf:
                mc = raycheck.moved(c, f)
                for o in others:
                    if raycheck.convex_overlap(mc, o, 0.004) > 0:
                        hits.append(o["name"])
    return sorted(set(hits))


def stub_left(d, gcomps):
    """Smallest length of any open leaf still inside the opening along its slide axis (part frame)."""
    o = d.opening
    best = 99.0
    for a in d.anims:
        leaf = [c for c in gcomps if c["door"] == a["bone"]]
        if not leaf:
            return 0.0
        dv = [a["axis"][1][k] - a["axis"][0][k] for k in range(3)]
        k = 0 if abs(dv[0]) > 0.5 else (1 if abs(dv[1]) > 0.5 else 2)
        lo = min(c["bbox"][2 * k] for c in leaf) + dv[k] * a["amount"]
        hi = max(c["bbox"][2 * k + 1] for c in leaf) + dv[k] * a["amount"]
        olo, ohi = (o[0], o[1]) if k == 0 else (o[2], o[3])
        best = min(best, max(0.0, min(hi, ohi) - max(lo, olo)))
    return best


def virtual_walls(part, d):
    """Stand-ins for the wall the building puts around the part (the wall plane over the part's post span, minus the
    opening), so C10 sees the part the way a player in the building does. Parts with hidden posts (okabe) get none."""
    xs = [c["pos"][0] for c in part.connectors if c["type"] == "post" and not c.get("hidden")]
    if len(xs) < 2 or not getattr(d, "opening", None):
        return []
    x0, x1 = min(xs) + POST / 2, max(xs) - POST / 2
    o0, o1, b0, b1 = d.opening
    t = 0.0375
    out = []
    for (a, b, c, e) in ((x0, o0 - POST, 0.0, WALL_H), (o1 + 0.001, x1, 0.0, WALL_H), (o0 - POST, o1 + 0.001, b1, WALL_H),
                         (o0 - POST, o1 + 0.001, 0.0, b0)):
        if b - a > 0.01 and e - c > 0.01:
            out.append(box_comp(a, b, c, e, -t, t, name="virtual_wall"))
    return out


def tile_seating(part):
    """None if the part has no kawara. Else (ok, detail): every LOD0 kawara field vertex that lies over the part's
    sheathing has a closed visual solid (the fuki-tsuchi clay bed) within 1 cm below its tile underside, and every
    slope with eave tiles has a fascia (kayaoi) board under them."""
    field = [s for s in part.solids if s.tag in ("kawara_field", "hongawara") and 1 in s.vis]
    if not field:
        return None
    beds = [raycheck.solid_comp(s) for s in part.solids if s.tag == "tile_bed" and s.closed]
    sheath = [raycheck.solid_comp(s) for s in part.solids if s.tag == "sheathing" and s.closed]
    if not beds:
        return (False, "no clay bed (tile_bed) under the kawara")
    n = bad = 0
    worst = 0.0
    for s in field:
        for v in s.verts[::3]:
            over = [c for c in sheath if ray_y(c, v[0], v[2])]
            if not over:
                continue
            n += 1
            tops = [r[1] for c in beds for r in [ray_y(c, v[0], v[2])] if r and r[1] <= v[1] + 0.005]
            gap = (v[1] - max(tops)) if tops else 9.9
            # the corrugation: pans sit on the bed, rolls stand up to 0.055 + the row step above it
            if gap > 0.055 + 0.022 + 0.012:
                bad += 1
                worst = max(worst, gap)
    eaves = [s for s in part.solids if s.tag == "eave_tile"]
    fasc = [s for s in part.solids if s.tag == "kawara_fascia"]
    ok = bad == 0 and (not eaves or fasc)
    return (ok, "%d/%d field points within reach of the bed%s; %d eave tile sets, %d fascia boards" % (
        n - bad, n, "" if not bad else " (worst gap %.3f m)" % worst, len(eaves), len(fasc)))
