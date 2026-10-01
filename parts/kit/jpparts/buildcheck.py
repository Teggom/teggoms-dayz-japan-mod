"""Building-level checks added after Stephen's first in-game house walk (G3, 2026-09-27; PLAYBOOK §15).

Every building's verify.py calls run_g3(M, L, floors, rec) after its own checks:
  C10 doors + windows reachable (camera ray hits the leaf first) from both sides, open and closed
  C11 envelope leak (rooms see outside only through doors / windows)
  C12 roof / wall intersection (nothing from another sub-part inside a roof body)
  C13 kawara seated on the clay bed, fascia at every eave
  C14 interior faces use the interior clay (no exterior-weathered earth looking into a room)
  C15 stable silhouette (Resolution 2 / 3 top heights within 0.10 m of Resolution 1)
  C16 far-LOD kawara material (matte far field in Resolution 2 / 3 only)
  C17 closed-leaf jamb seal (nothing seen through a closed door / window at a jamb or meeting stile)   G3 fix 2
  C18 pulls on the stub edge (every pull still in the doorway when its leaf is open)                  G3 fix 2
  C19 matte finish (no environment reflection on matte library materials)                              G3 fix 2
  C20 no z-fighting: no two visibly different faces of different solids share a plane (same-facing, within 1 mm,
      overlapping, not covered by a third solid) in Resolution 1-3 (zfight.py; the pipeline's zfight.resolve fixes
      them at build time)                                                                               FB2 2026-10-01
  C21 partitions end at a beam or a ceiling: every interior wall panel's top meets a ceiling / floor / roof / beam
      within 2.5 cm, or its stack ends in a beam running >= 0.6 m along it (parttop.py)                 FB2 2026-10-01
  C22 no free wall ends: every interior wall panel's vertical end meets a post / wall / panel (parttop.free_ends)
                                                                                                        FB2 2026-10-01
M: the building Part in the model frame (M.doors, M.memory, M.solids); L: {lod name: mlod.Lod} read back from the
MLOD; floors: [{name, rect (model x0,x1,z0,z1), y, obstacles}]; rec(check, ok, detail).
"""
import os
import re

from . import mlod, checks as C, core, raycheck as RC

DEV = core.DEV
GLOSSY = ("jp_m_roof_kawara", "jp_m_wall_namako_tile", "jp_m_metal_iron")   # build_materials.FINISH_BY_ID (glossy)
REFLECTIVE = ("glossy", "glazed")      # finishes that keep an environment reflection (build_materials.FINISH)


def reflective(mid):
    """True when a library material is glossy / glazed by design (C19 exempts it): the sidecar's 'finish' field
    (B1 sidecars carry it, e.g. the glazed stoneware and lacquer), else the pre-B1 glossy list (kawara, namako, iron),
    whose sidecars have no finish field."""
    fin = core.LIBRARY.get(mid[5:], {}).get("finish") if mid.startswith("jp_m_") else None
    if fin:
        return fin in REFLECTIVE
    return mid.startswith(GLOSSY)


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


def floor_fn(road):
    def f(x, z, y_hint):
        hs = [h for h, _ in road_heights(road, x, z) if h <= y_hint + 0.6]
        return max(hs) if hs else 0.0            # no Roadway under the eye = outside, on the ground (grade 0)
    return f


def run_g3(M, L, floors, rec, extra_portals=()):
    """The checks added after Stephen's first in-game walk (G3, 2026-09-27; PLAYBOOK §15).
    C2 (2026-09-30): extra_portals [(name, (x0, x1, y0, y1, z0, z1))] = declared openings without a leaf (a mushiro
    doorway, a smoke gable's lattice) that C11 counts like a door; a floor with enclosed=False (an open-sided shed or
    lean-to) is left out of C11. Both default to nothing: every older building checks exactly as before."""
    rooms = [{"name": f["name"], "rect": f["rect"], "y": f["y"], "obstacles": f.get("obstacles", [])} for f in floors
             if f.get("enclosed", True)]
    road = L["Roadway"]
    vcomps = C.components(L["View Geometry"])
    fa = floor_fn(road)
    # C10 every door and window: the camera ray hits its leaf first from both sides, open and closed
    for k, d in enumerate(M.doors, 1):
        for frac, state in ((1.0, "open"), (0.0, "closed")):
            rr = RC.door_reach(d, vcomps, M.memory, floor_at=fa, frac=frac, others=M.doors)
            bad = [s_ for s_, (ok, _) in rr.items() if not ok]
            rec("C10 DoorsTwin%d reachable from %s (%s)" % (k, "both sides" if len(rr) > 1 else "its leaf side",
                                                            state), not bad,
                "%s: %s" % (getattr(d, "label", ""), "; ".join("%s: %s" % (s_, v[1]) for s_, v in rr.items())))
    # C17 closed-leaf jamb seal (G3 fix 2): nothing seen through a closed opening at a jamb or meeting stile
    T1 = RC.lod_triangles(L["Resolution 1"])
    for k, d in enumerate(M.doors, 1):
        if d.kind == "lattice":                       # open-barred koshido leaves are see-through by design
            continue
        n_, sl = RC.jamb_slits(d, vcomps, T1)
        rec("C17 DoorsTwin%d closed: no see-through slit at a jamb or meeting stile" % k, n_ > 0 and not sl,
            "%s: %d rays through the closed doorway (steep ones at every jamb / meeting stile + straight through the "
            "leaves), %d see through%s" % (
                getattr(d, "label", ""), n_, len(sl), (", e.g. eye %s -> %s" % sl[0]) if sl else ""))
    # C18 pulls on the stub edge (G3 fix 2): every pull is still in the doorway when its leaf is open
    for k, d in enumerate(M.doors, 1):
        pp = RC.pull_positions(d, vcomps, M.solids)
        if pp:
            rec("C18 DoorsTwin%d pulls on the stub edge (in the doorway when open)" % k, all(x[4] for x in pp),
                "%s: %s" % (getattr(d, "label", ""), "; ".join("%s u %.2f closed -> %.2f open, doorway %.2f..%.2f" % (
                    x[0], x[1], x[2], x[3][0], x[3][1]) for x in pp)))
    # C10b vanilla stub: every sliding leaf keeps >= 0.15 m in its opening when open (checked on the parts too)
    # C11 envelope leak: nothing inside a room sees outside except through a door / window
    portals = []
    for k, d in enumerate(M.doors, 1):
        bones = {a["bone"] for a in d.anims}
        lb = [c["bbox"] for c in vcomps if c["door"] in bones]
        if lb:
            bx = [min(b[0] for b in lb), max(b[1] for b in lb), min(b[2] for b in lb), max(b[3] for b in lb),
                  min(b[4] for b in lb), max(b[5] for b in lb)]
            a0 = d.anims[0]
            u = [abs(a0["axis"][1][q] - a0["axis"][0][q]) for q in range(3)]
            nx = 0.20 if u[2] > u[0] else 0.06            # the wall normal is x when the leaf runs along z
            nz = 0.20 if u[0] >= u[2] else 0.06
            if getattr(d, "half", False) and d.action:      # B2 half door: its whole doorway (the open top, the gap
                bx[3] = max(bx[3], d.action[1] + getattr(d, "half_top", 1.0))      # under the leaf) is the portal
                bx[2] = min(bx[2], d.action[1] - getattr(d, "act_h", 1.0))
            portals.append(("DoorsTwin%d" % k, (bx[0] - nx, bx[1] + nx, bx[2] - 0.06, bx[3] + 0.06, bx[4] - nz,
                                                  bx[5] + nz)))
    portals += [(n_, tuple(b_)) for n_, b_ in extra_portals]
    res = RC.envelope_leak(L["Resolution 1"], rooms, portals)
    wb = M.bbox()
    detail, nleak = [], 0
    for name, (n, via, leaks) in res.items():
        nleak += len(leaks)
        ex = sorted({RC.leak_exit(o, dv, wb) for o, dv in leaks[:40]})[:3]
        detail.append("%s %d rays, %d out through doors/windows, %d LEAKS%s" % (name, n, via, len(leaks),
                                                                               (" e.g. exit %s" % ex) if ex else ""))
    opn = [f["name"] for f in floors if not f.get("enclosed", True)]
    if opn:
        detail.append("open-sided by design (not checked): %s" % ", ".join(opn))
    rec("C11 envelope leak: rooms see outside only through doors / windows", nleak == 0, "; ".join(detail))
    # C12 roof pokes: nothing from another sub-part enters a roof body, in any LOD
    pk = RC.roof_pokes(M.solids)
    rec("C12 roof / wall intersection (no part pokes into a roof body > 3 cm)", not pk,
        "%d roof bodies clear" % sum(1 for s_ in M.solids if s_.tag.startswith("roof_geo_")) if not pk
        else "; ".join("%s/%s (LOD %s) into %s %s by %.2f m" % x for x in pk[:4]))
    # C13 tile seating
    ts = C.tile_seating(M)
    # B2: a building with no kawara at all (board or thatch roofs only) has nothing to seat: pass, and say so
    rec("C13 kawara seated on the clay bed, fascia at every eave", ts is None or ts[0],
        ts[1] if ts else "no kawara on this building (board / thatch roofs): nothing to seat")
    # C14 interior faces never use the exterior-weathered earth
    bad = []
    for f_ in L["Resolution 1"].faces:
        tex = f_[2].lower()
        if not re.search(r"jp_m_wall_(nakanuri|arakabe)_w\d", tex):
            continue
        pts_ = [L["Resolution 1"].points[v[0]] for v in f_[0]]
        n_ = mlod._normalize(mlod._face_formula_normal(pts_))
        if abs(n_[1]) > 0.7:
            continue
        cx = [sum(p_[q] for p_ in pts_) / len(pts_) for q in range(3)]
        for sgn in (-1.0,):              # mlod face formula normal = inward (checks.components): outward = -n
            q_ = [cx[q] + sgn * n_[q] * 0.25 for q in range(3)]
            for r in rooms:
                x0, x1, z0, z1 = r["rect"]
                if x0 <= q_[0] <= x1 and z0 <= q_[2] <= z1 and r["y"] <= q_[1] <= r["y"] + 2.5:
                    bad.append((r["name"], tuple(round(v, 2) for v in cx)))
    rec("C14 interior faces use the interior clay, not the exterior-weathered earth", not bad,
        "no exterior earth face looks into a room" if not bad else "%d faces, e.g. %s" % (len(bad), bad[:3]))
    # C15 stable silhouette: the top-down height map of every LOD matches Resolution 1 (onigawara, ridge, verges)
    import numpy as np
    x0, x1, _, _, z0, z1 = M.bbox()
    xs = np.arange(x0 + 0.05, x1, 0.12)
    zs = np.arange(z0 + 0.05, z1, 0.12)
    O = np.array([(x, 30.0, z) for x in xs for z in zs])
    Dn = np.tile(np.array([[0.0, -1.0, 0.0]]), (len(O), 1))
    # FB2 (2026-10-01): each column is also cast 1 cm off in x and z; a column differs only when it differs in all
    # five (a sliver under 1 cm at an edge, e.g. a piece zfight.resolve set 5 mm proud, cannot pop at LOD distance)
    jit = ((0.0, 0.0), (0.01, 0.0), (-0.01, 0.0), (0.0, 0.01), (0.0, -0.01))
    tops = {}
    for lname in ("Resolution 1", "Resolution 2", "Resolution 3"):
        tri = RC.lod_triangles(L[lname])
        # V1: cast_down = cast(tri, O', Dn, 40.0, chunk=64) (same nearest hits; JP_RAY_ENGINE=brute runs that)
        tops[lname] = [30.0 - RC.cast_down(tri, O + np.array([dx, 0.0, dz]), 40.0) for dx, dz in jit]
    worst = []
    for lname in ("Resolution 2", "Resolution 3"):
        dds = []
        for j in range(len(jit)):
            a_, b_ = tops["Resolution 1"][j], tops[lname][j]
            dds.append(np.where(np.isfinite(a_) & np.isfinite(b_), np.abs(a_ - b_),
                                np.where(np.isfinite(a_) & (a_ > 2.5), 9.9, 0.0)))
        a = tops["Resolution 1"][0]
        both = np.isfinite(a) & (a > 2.5)
        dd = np.min(np.array(dds), axis=0)
        m = both & (dd > 0.10)
        if m.any():
            i = int(np.argmax(np.where(m, dd, 0)))
            worst.append("%s: %d columns differ > 0.10 m, worst %.2f m at (%.2f, %.2f)" % (
                lname, int(m.sum()), float(dd[i]), O[i][0], O[i][2]))
    rec("C15 stable silhouette: Resolution 2 / 3 top heights within 0.10 m of Resolution 1", not worst,
        "; ".join(worst) if worst else "%d columns over 2.5 m compared in each LOD" % int(
            (np.isfinite(tops["Resolution 1"][0]) & (tops["Resolution 1"][0] > 2.5)).sum()))
    # C16 far-LOD roof material: matte far field in Resolution 2 / 3, the close one only in Resolution 1
    fars = {ln: sum(1 for f_ in L[ln].faces if "jp_m_roof_kawara_far" in f_[2].lower()) for ln in
            ("Resolution 1", "Resolution 2", "Resolution 3")}
    nears = {ln: sum(1 for f_ in L[ln].faces if "jp_m_roof_kawara_field" in f_[2].lower()) for ln in
             ("Resolution 2", "Resolution 3")}

    def spec(rv):
        t_ = open(os.path.join(DEV, "src", rv), encoding="utf-8").read()
        return float(re.search(r"specular\[\]=\{([0-9.]+)", t_).group(1))
    sf = spec(core.rvmat_path("roof_kawara_far", "_w1"))
    sn = spec(core.rvmat_path("roof_kawara_field", "_w1"))
    # C19 matte finish (G3 fix 2): every non-glossy library material in the visual LODs has no environment reflection
    # (vanilla matte Super rvmats: Stage7 #(argb,8,8,3)color(0,0,0,1,CO)); only kawara, namako tile and iron keep one
    used = {f_[3] for ln in ("Resolution 1", "Resolution 2", "Resolution 3") for f_ in L[ln].faces
            if f_[3].lower().startswith("jp\\common\\materials\\")}
    shiny = []
    for rv in sorted(used):
        mid = re.sub(r"_w\d\.rvmat$", "", os.path.basename(rv).lower())
        if reflective(mid):
            continue
        t_ = open(os.path.join(DEV, "src", rv), encoding="utf-8").read()
        if "color(0,0,0,1,CO)" not in t_.replace(" ", ""):
            shiny.append(os.path.basename(rv))
    rec("C19 matte finish: no environment reflection on matte materials (clay, plaster, wood, straw, paper, stone)",
        not shiny, "%d library rvmats in the visual LODs, %d glossy / glazed by design (sidecar finish, else kawara, "
        "namako, iron)%s" % (len(used), sum(1 for rv in used if reflective(re.sub(r"_w\d\.rvmat$", "",
                                                                                   os.path.basename(rv).lower()))),
                             ("; SHINY: %s" % shiny[:4]) if shiny else ""))
    # B2: a building without a kawara field (board / thatch roofs only) passes when no far field appears either
    has_field = any("jp_m_roof_kawara_field" in f_[2].lower() for f_ in L["Resolution 1"].faces)
    rec("C16 far-LOD kawara: matte far material in Resolution 2 / 3", (fars["Resolution 1"] == 0 and
        fars["Resolution 2"] > 0 and fars["Resolution 3"] > 0 and not any(nears.values()) and sf < sn) if has_field
        else not any(fars.values()),
        "far-field faces R1/R2/R3 %d/%d/%d; close field in R2/R3 %d/%d; specular far %.2f < close %.2f" % (
            fars["Resolution 1"], fars["Resolution 2"], fars["Resolution 3"], nears["Resolution 2"],
            nears["Resolution 3"], sf, sn))
    # FB2 (2026-10-01, Stephen: "items perfectly aligned and flicker"): coplanar overlapping faces (zfight.py)
    from . import zfight as ZF
    zr = ZF.coplanar(M)
    rec("C20 no z-fighting: no visibly different faces share a plane (same-facing, <= 1 mm, overlapping), R1-R3",
        not zr["same"], "%d visible same-facing pairs%s; %d touching (opposite-facing: backface-culled) and %d "
        "covered / drawn-identically pairs not judged" % (len(zr["same"]), ("; " + "; ".join(ZF.summary(zr, "same", 3)))
                                                          if zr["same"] else "", len(zr["opposite"]), len(zr["hidden"])))
    # FB2 (2026-10-01, Stephen: partitions "just end below the open roof structure"; the inn's upstairs divider short
    # of the sloping ceiling): every interior wall ends at a beam or a ceiling (parttop.py)
    from . import parttop as PTOP
    pb = PTOP.top_ends(M)
    rec("C21 interior partitions end at a beam or a ceiling (no wall top open below the roof)", not pb,
        "every interior wall top closed" if not pb else "%d open wall-top samples: %s" % (
            len(pb), "; ".join(PTOP.summary(pb, 3))))
    fe = PTOP.free_ends(M)
    rec("C22 interior wall ends meet a post or a wall (no vertical see-through slot)", not fe,
        "every interior wall panel end closed" if not fe else "%d free ends: %s" % (len(fe), fe[:4]))
