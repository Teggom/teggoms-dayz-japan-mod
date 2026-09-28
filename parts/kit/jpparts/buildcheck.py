"""Building-level checks added after Stephen's first in-game house walk (G3, 2026-09-27; PLAYBOOK §15).

Every building's verify.py calls run_g3(M, L, floors, rec) after its own checks:
  C10 doors + windows reachable (camera ray hits the leaf first) from both sides, open and closed
  C11 envelope leak (rooms see outside only through doors / windows)
  C12 roof / wall intersection (nothing from another sub-part inside a roof body)
  C13 kawara seated on the clay bed, fascia at every eave
  C14 interior faces use the interior clay (no exterior-weathered earth looking into a room)
  C15 stable silhouette (Resolution 2 / 3 top heights within 0.10 m of Resolution 1)
  C16 far-LOD kawara material (matte far field in Resolution 2 / 3 only)
M: the building Part in the model frame (M.doors, M.memory, M.solids); L: {lod name: mlod.Lod} read back from the
MLOD; floors: [{name, rect (model x0,x1,z0,z1), y, obstacles}]; rec(check, ok, detail).
"""
import os
import re

from . import mlod, checks as C, core, raycheck as RC

DEV = core.DEV


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


def run_g3(M, L, floors, rec):
    """The checks added after Stephen's first in-game walk (G3, 2026-09-27; PLAYBOOK §15)."""
    rooms = [{"name": f["name"], "rect": f["rect"], "y": f["y"], "obstacles": f.get("obstacles", [])} for f in floors]
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
            portals.append(("DoorsTwin%d" % k, (bx[0] - nx, bx[1] + nx, bx[2] - 0.06, bx[3] + 0.06, bx[4] - nz,
                                                  bx[5] + nz)))
    res = RC.envelope_leak(L["Resolution 1"], rooms, portals)
    wb = M.bbox()
    detail, nleak = [], 0
    for name, (n, via, leaks) in res.items():
        nleak += len(leaks)
        ex = sorted({RC.leak_exit(o, dv, wb) for o, dv in leaks[:40]})[:3]
        detail.append("%s %d rays, %d out through doors/windows, %d LEAKS%s" % (name, n, via, len(leaks),
                                                                               (" e.g. exit %s" % ex) if ex else ""))
    rec("C11 envelope leak: rooms see outside only through doors / windows", nleak == 0, "; ".join(detail))
    # C12 roof pokes: nothing from another sub-part enters a roof body, in any LOD
    pk = RC.roof_pokes(M.solids)
    rec("C12 roof / wall intersection (no part pokes into a roof body > 3 cm)", not pk,
        "%d roof bodies clear" % sum(1 for s_ in M.solids if s_.tag.startswith("roof_geo_")) if not pk
        else "; ".join("%s/%s (LOD %s) into %s %s by %.2f m" % x for x in pk[:4]))
    # C13 tile seating
    ts = C.tile_seating(M)
    rec("C13 kawara seated on the clay bed, fascia at every eave", ts is not None and ts[0], ts[1] if ts else "no kawara")
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
    tops = {}
    for lname in ("Resolution 1", "Resolution 2", "Resolution 3"):
        t = RC.cast(RC.lod_triangles(L[lname]), O, Dn, 40.0, chunk=64)
        tops[lname] = 30.0 - t
    worst = []
    for lname in ("Resolution 2", "Resolution 3"):
        a, b = tops["Resolution 1"], tops[lname]
        both = np.isfinite(a) & (a > 2.5)
        dd = np.where(np.isfinite(b), np.abs(a - b), 9.9)
        m = both & (dd > 0.10)
        if m.any():
            i = int(np.argmax(np.where(m, dd, 0)))
            worst.append("%s: %d columns differ > 0.10 m, worst %.2f m at (%.2f, %.2f)" % (
                lname, int(m.sum()), float(dd[i]), O[i][0], O[i][2]))
    rec("C15 stable silhouette: Resolution 2 / 3 top heights within 0.10 m of Resolution 1", not worst,
        "; ".join(worst) if worst else "%d columns over 2.5 m compared in each LOD" % int(
            (np.isfinite(tops["Resolution 1"]) & (tops["Resolution 1"] > 2.5)).sum()))
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
    rec("C16 far-LOD kawara: matte far material in Resolution 2 / 3", fars["Resolution 1"] == 0 and
        fars["Resolution 2"] > 0 and fars["Resolution 3"] > 0 and not any(nears.values()) and sf < sn,
        "far-field faces R1/R2/R3 %d/%d/%d; close field in R2/R3 %d/%d; specular far %.2f < close %.2f" % (
            fars["Resolution 1"], fars["Resolution 2"], fars["Resolution 3"], nears["Resolution 2"],
            nears["Resolution 3"], sf, sn))
