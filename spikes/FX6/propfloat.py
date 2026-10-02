"""FX6 prop self-support check (Stephen's 3c-1 walk, 2026-10-02: "the cloths on the ground are floating in mid air", "a
washbasin floating in mid-air at an angle rather than resting on something").

Every piece of a prop must REST on something: the prop's own floor plane (y 0), or another piece that itself rests.
Pieces = connected components of the master's Resolution 1 (faces sharing a point). Two pieces touch when a vertex of
one lies within TOL of a triangle of the other, or an edge of one crosses a triangle of the other.

Per piece:
  FLOAT   not connected to the floor through a chain of touching pieces (a cloth end in mid-air, a tub in the air)
  TIPS    connected, but its centre of mass (surface-area centroid) lies outside the convex hull (in plan, + MARGIN) of
          its contact points (floor contacts + contacts with the pieces it touches): a tilted piece with nothing
          holding its high side (a cloth ramp standing at 55 deg on one edge, a tub on edge propped by nothing)
A hung prop (anchor 'hang' / mount 'beam' / 'wall') is checked the same way from its attachment instead of the
floor: pieces touching the prop's top plane (the hang line) or, for wall props, the wall plane z 0 count as held.

  python spikes/FX6/propfloat.py [stem ...]       default: every prop of the decor catalogue
  python spikes/FX6/propfloat.py --cat brewfit    one catalogue folder
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "buildings")):
    if p not in sys.path:
        sys.path.insert(0, p)
from jpparts import mlod, decor as DC  # noqa: E402

TOL = 0.02          # touching
MARGIN = 0.06       # centre of mass may lie this far outside the contact hull (cloth thickness, rounding)
MIN_AREA = 0.002    # pieces with less surface (m2) are ignored (tiny ties, nails)
FLOAT_GAP = 0.03    # a body floats when it hangs more than this off anything that rests (visible in game)
FLOAT_AREA = 0.02   # ... and has at least this much surface (m2)
CLOTH = set()       # indices (into the last pieces() result) of cloth pieces (textile materials)


def res1(path):
    lods = mlod.read_mlod(path)
    return next(l for l in lods if mlod.lod_name(l.resolution) == "Resolution 1")


def pieces(lod):
    """[(verts (n,3), tris (m,3,3))] per connected component (proxy faces dropped)."""
    drop = set()
    for name, (pw, fs) in lod.selections.items():
        if name.lower().startswith("proxy:"):
            drop |= fs
    par = list(range(len(lod.points)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    faces = [f for i, f in enumerate(lod.faces) if i not in drop]
    # the writer may split points per face (normals / UVs): points at the same place (1 mm) are one point
    first = {}
    for k, p in enumerate(lod.points):
        key = (round(p[0] * 1000), round(p[1] * 1000), round(p[2] * 1000))
        if key in first:
            ra, rb = find(first[key]), find(k)
            if ra != rb:
                par[rb] = ra
        else:
            first[key] = k
    for f in faces:
        ids = [v[0] for v in f[0]]
        r0 = find(ids[0])
        for q in ids[1:]:
            rq = find(q)
            if rq != r0:
                par[rq] = r0
    groups = {}
    cloth = {}
    for f in faces:
        ids = [v[0] for v in f[0]]
        r = find(ids[0])
        groups.setdefault(r, []).append(ids)
        c = cloth.setdefault(r, [0, 0])
        c[0] += 1
        c[1] += 1 if "/textile/" in (f[3] or "").lower().replace(chr(92), "/") else 0
    out = []
    P = np.array(lod.points, dtype=float)
    CLOTH.clear()
    for r, g in groups.items():
        tris = []
        vid = set()
        for ids in g:
            vid |= set(ids)
            tris.append((ids[0], ids[1], ids[2]))
            if len(ids) == 4:
                tris.append((ids[0], ids[2], ids[3]))
        T = P[np.array(tris)]
        if cloth[r][1] * 2 > cloth[r][0]:
            CLOTH.add(len(out))
        out.append((P[sorted(vid)], T))
    return out


def tri_area_centroid(T):
    a = 0.5 * np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1)
    c = T.mean(axis=1)
    A = a.sum()
    return A, (c * a[:, None]).sum(axis=0) / max(A, 1e-12)


def pt_tri_dist(Pp, T):
    """Distances (n, m) from points Pp (n,3) to triangles T (m,3,3) (Ericson's closest point, vectorised)."""
    a, b, c = T[None, :, 0], T[None, :, 1], T[None, :, 2]
    p = Pp[:, None, :]
    ab, ac, ap = b - a, c - a, p - a
    d1 = (ab * ap).sum(-1)
    d2 = (ac * ap).sum(-1)
    bp = p - b
    d3 = (ab * bp).sum(-1)
    d4 = (ac * bp).sum(-1)
    cp = p - c
    d5 = (ab * cp).sum(-1)
    d6 = (ac * cp).sum(-1)
    va = d3 * d6 - d5 * d4
    vb = d5 * d2 - d1 * d6
    vc = d1 * d4 - d3 * d2
    den = va + vb + vc
    den = np.where(np.abs(den) < 1e-18, 1e-18, den)
    v = vb / den
    w = vc / den
    q = a + ab * v[..., None] + ac * w[..., None]            # interior projection
    # region tests
    res = q
    m = (d1 <= 0) & (d2 <= 0)
    res = np.where(m[..., None], a, res)
    m2 = (d3 >= 0) & (d4 <= d3) & ~m
    res = np.where(m2[..., None], b, res)
    m3 = (d6 >= 0) & (d5 <= d6) & ~m & ~m2
    res = np.where(m3[..., None], c, res)
    vcab = (vc <= 0) & (d1 >= 0) & (d3 <= 0) & ~m & ~m2 & ~m3
    t = np.where(np.abs(d1 - d3) < 1e-18, 0.0, d1 / np.where(np.abs(d1 - d3) < 1e-18, 1.0, d1 - d3))
    res = np.where(vcab[..., None], a + ab * t[..., None], res)
    vbac = (vb <= 0) & (d2 >= 0) & (d6 <= 0) & ~m & ~m2 & ~m3 & ~vcab
    t2 = np.where(np.abs(d2 - d6) < 1e-18, 0.0, d2 / np.where(np.abs(d2 - d6) < 1e-18, 1.0, d2 - d6))
    res = np.where(vbac[..., None], a + ac * t2[..., None], res)
    vabc = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0) & ~m & ~m2 & ~m3 & ~vcab & ~vbac
    den3 = (d4 - d3) + (d5 - d6)
    t3 = np.where(np.abs(den3) < 1e-18, 0.0, (d4 - d3) / np.where(np.abs(den3) < 1e-18, 1.0, den3))
    res = np.where(vabc[..., None], b + (c - b) * t3[..., None], res)
    return np.linalg.norm(p - res, axis=-1)


def edges_cross(TA, TB):
    """Does any edge of a triangle in TA cross a triangle of TB (Moller-Trumbore on segments)?"""
    E0 = np.concatenate([TA[:, 0], TA[:, 1], TA[:, 2]])
    E1 = np.concatenate([TA[:, 1], TA[:, 2], TA[:, 0]])
    d = E1 - E0
    a, b, c = TB[:, 0], TB[:, 1], TB[:, 2]
    e1, e2 = b - a, c - a
    h = np.cross(d[:, None, :], e2[None, :, :])
    det = (e1[None] * h).sum(-1)
    ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
    s = E0[:, None, :] - a[None]
    u = (s * h).sum(-1) * inv
    q = np.cross(s, e1[None])
    v = (d[:, None, :] * q).sum(-1) * inv
    t = (e2[None] * q).sum(-1) * inv
    hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t >= 0) & (t <= 1)
    return bool(hit.any())


def bbox(V):
    return V.min(axis=0), V.max(axis=0)


def contact(A, B, tol=TOL):
    """Contact points of piece A on piece B (A's vertices within tol of B's triangles + B's vertices within tol of
    A's), or None when apart. Crossing edges count as touching (the vertices nearest the crossing as contacts)."""
    (VA, TA), (VB, TB) = A, B
    a0, a1 = bbox(VA)
    b0, b1 = bbox(VB)
    if np.any(a0 > b1 + tol) or np.any(b0 > a1 + tol):
        return None
    pts = []
    da = pt_tri_dist(VA, TB).min(axis=1)
    pts += list(VA[da <= tol])
    db = pt_tri_dist(VB, TA).min(axis=1)
    pts += list(VB[db <= tol])
    if not pts and (edges_cross(TA, TB) or edges_cross(TB, TA)):
        # crossing: take the overlap box's centre as the contact
        lo, hi = np.maximum(a0, b0), np.minimum(a1, b1)
        pts = [(lo + hi) / 2]
    return np.array(pts) if pts else None


def hull_dist(P2, q):
    """Distance in plan from q to the convex hull of points P2 (0 inside)."""
    pts = sorted(set((round(float(x), 4), round(float(z), 4)) for x, z in P2))
    if len(pts) == 1:
        return math.hypot(q[0] - pts[0][0], q[1] - pts[0][1])

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    H = lo[:-1] + up[:-1]
    if len(H) >= 3 and all(cr(H[i], H[(i + 1) % len(H)], q) >= -1e-9 for i in range(len(H))):
        return 0.0
    best = 1e9
    segs = list(zip(H, H[1:] + H[:1])) if len(H) >= 2 else [(H[0], H[0])]
    for a, b in segs:
        dx, dz = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dz * dz
        t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dz) / L2))
        best = min(best, math.hypot(q[0] - a[0] - t * dx, q[1] - a[1] - t * dz))
    return best


def analyse(path, anchor="floor"):
    """[(piece index, problem, detail)] for one prop master; problems FLOAT / TIPS."""
    lod = res1(path)
    PS0 = pieces(lod)
    keep = [k for k, p in enumerate(PS0) if tri_area_centroid(p[1])[0] >= MIN_AREA]
    cloth = {i for i, k in enumerate(keep) if k in CLOTH}
    PS = [PS0[k] for k in keep]
    if not PS:
        return [], 0
    allV = np.concatenate([p[0] for p in PS])
    ytop = allV[:, 1].max()
    held = []
    for V, T in PS:
        if anchor == "hang":
            held.append(V[V[:, 1] >= ytop - TOL])
        elif anchor == "wall":
            g = V[(V[:, 1] <= TOL) | (V[:, 2] <= TOL)]
            held.append(g)
        else:
            held.append(V[V[:, 1] <= TOL])
    n = len(PS)
    C = {}
    for i in range(n):
        for j in range(i + 1, n):
            c = contact(PS[i], PS[j])
            if c is not None:
                C[(i, j)] = c
    nb = {i: [] for i in range(n)}
    for (i, j), c in C.items():
        nb[i].append((j, c))
        nb[j].append((i, c))
    # bodies: pieces joined by contact (a tub's staves + hoops; a frame + the cloths hung on it; two tubs leaning on
    # each other). A body rests when it touches the floor (or its hang line / wall) and its centre of mass lies over
    # the hull of those contacts; a body that does not reach them floats.
    body = [-1] * n
    nbody = 0
    for s in range(n):
        if body[s] >= 0:
            continue
        stack = [s]
        body[s] = nbody
        while stack:
            i = stack.pop()
            for j, _ in nb[i]:
                if body[j] < 0:
                    body[j] = nbody
                    stack.append(j)
        nbody += 1
    out = []
    for b in range(nbody):
        mem = [i for i in range(n) if body[i] == b]
        Asum, cs = 0.0, np.zeros(3)
        for i in mem:
            A, c = tri_area_centroid(PS[i][1])
            Asum += A
            cs += A * c
        com = cs / max(Asum, 1e-12)
        V = np.concatenate([PS[i][0] for i in mem])
        cps = [held[i] for i in mem if len(held[i])]
        if not cps:
            # how far it hangs in the air: the nearest other body (or the floor / hang line)
            gap = float(V[:, 1].min()) if anchor == "floor" else (float(ytop - V[:, 1].max()) if anchor == "hang"
                                                                   else float(min(V[:, 1].min(), V[:, 2].min())))
            for j in range(n):
                if body[j] == b:
                    continue
                VB, TB = PS[j]
                b0, b1 = bbox(VB)
                a0, a1 = bbox(V)
                if np.any(a0 > b1 + gap) or np.any(b0 > a1 + gap):
                    continue
                gap = min(gap, float(pt_tri_dist(V, TB).min()))
            if gap <= FLOAT_GAP or Asum < FLOAT_AREA:
                continue                 # a hairline (a lid in its pot, a cushion's top skin): invisible in game
            out.append((mem[0], "FLOAT", "body of %d pieces, %.2f m2 at (%.2f, %.2f, %.2f), y %.2f..%.2f, %.2f m "
                        "from anything that rests" % (len(mem), Asum, com[0], com[1], com[2], V[:, 1].min(),
                                                     V[:, 1].max(), gap)))
            continue
        if anchor in ("hang", "wall"):
            continue
        cp = np.concatenate(cps)
        d = hull_dist(cp[:, [0, 2]], (com[0], com[2]))
        if d > MARGIN and (V[:, 1].max() - V[:, 1].min()) > 0.05:
            out.append((mem[0], "TIPS", "body of %d pieces, %.2f m2, centre (%.2f, %.2f, %.2f), y %.2f..%.2f: %.2f m "
                        "outside the hull of its floor contacts (tilted with nothing holding it)" %
                        (len(mem), Asum, com[0], com[1], com[2], V[:, 1].min(), V[:, 1].max(), d)))
    # CLOTH: a cloth either lies flat on something (<= 0.10 m tall, in a resting body) or hangs: its top edge must
    # touch a support that is not cloth (a bar, a peg, a beam, a table edge) or the prop's hang line. A cloth standing
    # up with a free top (a stiff ramp of cloth in the air) fails.
    for i in sorted(cloth):
        V, T = PS[i]
        y0, y1 = V[:, 1].min(), V[:, 1].max()
        if y1 - y0 <= 0.10:
            continue
        # only SHEETS (a hung length, a cloth over a bar): a lump of cloth (a heap, a bag) rests like any body
        C0 = V - V.mean(axis=0)
        ax = np.linalg.svd(C0, full_matrices=False)[2][-1]
        if np.ptp(C0 @ ax) > 0.03:
            continue
        top = V[V[:, 1] >= y1 - 0.03]
        if anchor == "hang" and y1 >= ytop - TOL:
            continue
        ok = False
        for j in range(n):
            if j == i or j in cloth:
                continue
            VB, TB = PS[j]
            b0, b1 = bbox(VB)
            if np.any(top.min(axis=0) > b1 + TOL) or np.any(b0 > top.max(axis=0) + TOL):
                continue
            if float(pt_tri_dist(top, TB).min()) <= TOL:
                ok = True
                break
        if not ok:
            A, c = tri_area_centroid(T)
            out.append((i, "CLOTH", "cloth %.2f m2, y %.2f..%.2f at (%.2f, %.2f): its top edge hangs from nothing "
                        "(no bar / peg / beam / edge within %.0f cm)" % (A, y0, y1, c[0], c[2], TOL * 100)))
    return out, n


def _one(job):
    s, path, anchor = job
    try:
        return analyse(path, anchor)
    except Exception as e:                           # noqa: BLE001
        return "%s" % e


def main(argv):
    cat = DC.catalog()
    stems = [a for a in argv if not a.startswith("--")]
    if "--cat" in argv:
        f = argv[argv.index("--cat") + 1]
        stems = [k for k, v in cat.items() if v.get("folder") == f]
        argv = [a for a in argv if a != f]
    if not stems:
        stems = sorted(cat)
    nbad = 0
    nchk = 0
    jobs = []
    for s in stems:
        inf = cat.get(s)
        if not inf or not inf.get("master") or not os.path.exists(inf["master"]):
            continue
        anchor = "hang" if (inf.get("anchor") == "hang" or inf.get("mount") == "beam") else (
            "wall" if inf.get("anchor") == "wall" or inf.get("mount") == "wall" else "floor")
        jobs.append((s, inf["master"], anchor))
    if len(jobs) > 8:
        from multiprocessing import Pool
        with Pool(4) as pool:                         # README rule 2b: at most 4 processes
            results = pool.map(_one, jobs)
    else:
        results = [_one(j) for j in jobs]
    for (s, _m, anchor), r in zip(jobs, results):
        if isinstance(r, str):
            print("  ERR  %-36s %s" % (s, r))
            continue
        res, n = r
        nchk += 1
        if res:
            nbad += 1
            print("  FAIL %-36s (%s, %d pieces)" % (s, anchor, n))
            for i, k, d in res[:6]:
                print("         %s %s" % (k, d))
        elif "-v" in argv:
            print("  PASS %-36s (%s, %d pieces)" % (s, anchor, n))
    print("PROPFLOAT: %d props checked, %d failing" % (nchk, nbad))
    return 1 if nbad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
