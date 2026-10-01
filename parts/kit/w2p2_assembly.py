#!/usr/bin/env python3
r"""W2P2 offline proof assemblies (not island buildings; W2S builds the shells): the curved roof (jpparts/sori.py)
and the bracket sets (jpparts/kumimono.py) assembled the way a town-grade shrine / temple shell uses them, written as
MLOD, put through the building checks (the FB2 z-fight resolver first, as buildings/pipeline.py does) and binarized.

  python w2p2_assembly.py [name ...] [--no-binarize]

  hall          town-grade worship hall: 3 x 2 bays (2.275 m), degumi sets + kaerumata, curved irimoya HONGAWARA,
                on W2P1's stone platform (stilts.kidan), board walls on three sides, open front
  hall_kokera   the same hall as a shrine haiden: hira-mitsudo sets, curved irimoya thick KOKERA
  hondo         a town temple main hall: 3 x 3 bays (2.275 m), MITESAKI sets with odaruki tail rafters into the
                curved eave, curved irimoya hongawara
  shoro         bell tower: hakama skirt (storey.hakama) on a stone platform, upper deck + W2P1 koran railing, four
                columns with degumi corner sets, bell beam (memory 'bell_hook'), curved irimoya hongawara
Outputs: src/JP/parts/_test_w2p2/<name>.p3d (MLOD; binarized copies in data/parts_test/w2p2/) and
parts/w2p2_assembly_checks.json (all results, committed).
"""
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, checks, mlod, raycheck, sori as S, kumimono as KM, storey as ST  # noqa: E402
from jpparts import stilts as STL, koran as KR, buildcheck as BC, zfight as ZF  # noqa: E402
from jpparts.core import Part, KEN, HALF, box, cyl, rng_for  # noqa: E402
from jpparts import found as FD  # noqa: E402
from jpparts.shapes import board_run  # noqa: E402

DEV = core.DEV
SRC = os.path.join(DEV, "src", "JP", "parts", "_test_w2p2")
OUT = os.path.join(DEV, "data", "parts_test", "w2p2")
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
GEO_PROPS = {"class": "house", "map": "house", "damage": "no", "autocenter": "0"}
BUDGETS = {"large": (12000, 4600, 1600), "standard": (6000, 2300, 800)}       # PLAYBOOK §12


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.replace("\r\n", "\n").encode("utf-8"))


# ------------------------------------------------------------------------------------------------ pieces
def board_walls(W, D, nx, nz, y0, y1, c, sides=("back", "left", "right")):
    """Board walls (itakabe) between the columns: random-width vertical boards in Resolution 1, one panel in
    Resolution 2 / 3 + Geometry, on the column centreline."""
    w = Part("walls", "", "")
    rng = rng_for("w2p2_walls")
    t = 0.05
    for side in sides:
        if side in ("front", "back"):
            z = 0.0 if side == "front" else -D
            for k in range(nx):
                a, b = k * W / nx + c / 2, (k + 1) * W / nx - c / 2
                for s in board_run(a, b, y0, y1, z - t / 2, z + t / 2, rng, 0.24, 0.34, "wood_weathered", vis=(1,)):
                    w.add(s)
                w.add(box(a, b, y0, y1, z - t / 2, z + t / 2, "wood_weathered", vis=(2, 3), geo=True, view=True,
                          fire=True, tag="itakabe_lod"))
        else:
            x = 0.0 if side == "left" else W
            for k in range(nz):
                a, b = -(k + 1) * D / nz + c / 2, -k * D / nz - c / 2
                for s in _zboards(x, t, y0, y1, a, b, rng):
                    w.add(s)
                w.add(box(x - t / 2, x + t / 2, y0, y1, a, b, "wood_weathered", vis=(2, 3), geo=True, view=True,
                          fire=True, tag="itakabe_lod"))
    return w


def _zboards(x, t, y0, y1, z0, z1, rng):
    out = []
    p = z0
    while p < z1 - 1e-4:
        q = min(z1, p + rng.uniform(0.24, 0.34))
        if z1 - q < 0.12:
            q = z1
        out.append(box(x - t / 2, x + t / 2, y0, y1, p + 0.002, q - 0.002, "wood_weathered", vis=(1,), tag="board",
                       uvoff=(rng.random(), rng.random())))
        p = q
    return out


def column_bases(nodes, c, y_top):
    b = Part("bases", "", "")
    for (x, z) in nodes:
        b.add(cyl("y", x, z, 0.78 * c, y_top - 0.10, y_top, "stone_cut", n=8, vis=(1, 2), tag="soseki_dressed"))
    return b


def platform(x0, x1, z0, z1, h, step_w=1.82):
    """A light cut-stone platform for the proofs (W2P1's stilts.kidan is the shell part; it costs ~2,000 faces in
    Resolution 1 AND 2 on a hall-size platform): a core slab (every LOD, Geometry, Roadway top), kerb stones and
    facing blocks standing 2 cm proud in Resolution 1, a cut step with a hidden ramp at the front (found.step)."""
    p = Part("platform", "", "")
    p.add(box(x0, x1, -h - 0.10, 0.0, z0, z1, {"top": "ground_doma_earth", "default": "stone_cut"}, vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="platform_core"))
    p.road([(x0, 0.0, z0), (x1, 0.0, z0), (x1, 0.0, z1), (x0, 0.0, z1)], "stone_ext")
    rng = rng_for("w2p2_platform")
    for (a0, a1, fixed, axis, sg) in ((x0, x1, z1, "x", 1), (x0, x1, z0, "x", -1), (z0, z1, x0, "z", -1),
                                      (z0, z1, x1, "z", 1)):
        a = a0 + (0.02 if axis == "z" else 0.0)
        while a < a1 - 0.05:
            b = min(a1 - (0.02 if axis == "z" else 0.0), a + rng.uniform(0.9, 1.3))
            if a1 - b < 0.4:
                b = a1 - (0.02 if axis == "z" else 0.0)
            for (yy0, yy1, dep, tag) in ((-0.16, 0.02, 0.32, "kerb"), (-h + 0.02, -0.165, 0.10, "facing")):
                o0, o1 = (fixed - dep + 0.02, fixed + 0.02) if sg > 0 else (fixed - 0.02, fixed + dep - 0.02)
                if axis == "x":
                    p.add(box(a + 0.006, b - 0.006, yy0, yy1, o0, o1, "stone_cut", vis=(1,), tag=tag,
                              uvoff=(rng.random(), rng.random())))
                else:
                    p.add(box(o0, o1, yy0, yy1, a + 0.006, b - 0.006, "stone_cut", vis=(1,), tag=tag,
                              uvoff=(rng.random(), rng.random())))
            a = b
    st = Part("step", "", "")
    FD.step(st, (x0 + x1) / 2, "cut", drop=h, width=step_w)
    p.merge(st.transformed(0.0, (0.0, 0.0, z1 + 0.02)))
    return p


def floor_deck(W, D, c, y):
    """The hall's board floor inside the columns (a stand-in for W2S's floor)."""
    f = Part("floor", "", "")
    f.add(box(c / 2, W - c / 2, y - 0.08, y, -D + c / 2, -c / 2, {"top": "floor_boards_rough", "default": "wood_weathered"},
              vis=(1, 2, 3), geo=True, view=True, fire=True, tag="floor"))
    f.road([(c / 2 + 0.01, y, -c / 2 - 0.01), (W - c / 2 - 0.01, y, -c / 2 - 0.01), (W - c / 2 - 0.01, y, -D + c / 2 + 0.01),
            (c / 2 + 0.01, y, -D + c / 2 + 0.01)], "boards")
    return f


# ------------------------------------------------------------------------------------------------ assemblies
def _hall(name, nx, nz, bay, form, covering, used, col_h=3.0, c=None, ov_extra=1.35, budget="large"):
    W, D = nx * bay, nz * bay
    a = Part(name, "", "_test_w2p2", tiers=[3], used_for=used)
    a.wear = "_w1"
    m = 1.30                                    # platform margin beyond the column lines
    a.merge(platform(-m, W + m, -D - m, m, 0.45))
    y_floor = 0.10                              # dressed column bases 0..0.10 on the platform top
    km = Part("kumimono", "", "")
    K = KM.frame(km, W, D, nx, nz, col_h, form, c=c, y0=y_floor, covering=covering,
                 nakazonae="kaerumata" if form != "mitsudo" else "kentozuka")
    c = K["c"]
    a.merge(km)
    a.merge(column_bases(K["nodes"], c, y_floor))
    a.merge(floor_deck(W, D, c, y_floor + 0.06))
    a.merge(board_walls(W, D, nx, nz, y_floor + 0.06, y_floor + col_h - 0.62 * c, c))
    rp = Part("roof", "", "")
    sls, info = S.roof(rp, W, D, "irimoya", covering, bear_y=K["bear_y"], g_out=K["g_out"], ov=K["g_out"] + ov_extra)
    a.merge(rp)
    floors = [{"name": "hall", "rect": (c / 2 + 0.05, W - c / 2 - 0.05, -D + c / 2 + 0.05, -c / 2 - 0.05),
               "y": y_floor + 0.06, "obstacles": [], "enclosed": False}]
    return a, dict(W=W, D=D, K=K, info=info, sls=sls, floors=floors, budget=budget, form=form, covering=covering)


def hall():
    return _hall("w2p2_hall", 3, 2, 2.275, "degumi", "hongawara",
                 "W2P2 proof: town-grade worship hall, degumi + kaerumata, curved irimoya hongawara")


def hall_kokera():
    return _hall("w2p2_hall_kokera", 3, 2, 2.275, "mitsudo", "kokera",
                 "W2P2 proof: shrine haiden, hira-mitsudo + kentozuka, curved irimoya thick kokera", ov_extra=1.45)


def hondo():
    return _hall("w2p2_hondo", 3, 3, 2.275, "mitesaki", "hongawara",
                 "W2P2 proof: town temple main hall, mitesaki + odaruki, curved irimoya hongawara", col_h=3.2,
                 c=0.27, ov_extra=1.30)


def shoro():
    B = 2.73                                    # the upper bay (one temple ken), 4 columns
    a = Part("w2p2_shoro", "", "_test_w2p2", tiers=[2, 3],
             used_for="W2P2 proof: bell tower (shoro) with hakama skirt, degumi, curved irimoya hongawara")
    a.wear = "_w1"
    cx, cz = B / 2, -B / 2
    m = 5.4
    a.merge(platform(cx - m / 2, cx + m / 2, cz - m / 2, cz + m / 2, 0.60, step_w=1.30))
    y_f = 2.80                                  # upper floor
    hk = Part("hakama", "", "")
    ST.hakama(hk, cx, cz, hb=2.05, ht=1.62, y0=0.0, y1=y_f - 0.30)
    dk = ST.deck(hk, cx, cz, 2.05, y_f)
    a.merge(hk)
    # railing round the deck (W2P1 koran), in the deck frame (y 0 = deck top)
    rl = Part("koran", "", "")
    e = 2.05 - 0.10
    KR.rail(rl, (cx - e, cz + e), (cx + e, cz + e), "plain", ends=("cross", "cross"))
    KR.rail(rl, (cx - e, cz - e), (cx + e, cz - e), "plain", ends=("cross", "cross"))
    KR.rail(rl, (cx - e, cz + e), (cx - e, cz - e), "plain", ends=("cross", "cross"), lift=0.015)
    KR.rail(rl, (cx + e, cz + e), (cx + e, cz - e), "plain", ends=("cross", "cross"), lift=0.015)
    a.merge(rl.transformed(0.0, (0.0, y_f, 0.0)))
    km = Part("kumimono", "", "")
    K = KM.frame(km, B, B, 1, 1, 2.55, "degumi", c=0.26, y0=y_f, covering="hongawara", nageshi=False)
    a.merge(km)
    c = K["c"]
    # bell beam across the bay (front-back) at the head-tie level, the bell hangs from its middle (W2F prop)
    bb = Part("bellbeam", "", "")
    yb = y_f + 2.55 - 0.62 * c - 0.30
    KM.beam(bb, (cx, yb, 0.0), (cx, yb, -B), 0.20, 0.24, vis=(1, 2, 3), tag="bell_beam")
    bb.memory["bell_hook"] = [(cx, yb, cz)]
    a.merge(bb)
    rp = Part("roof", "", "")
    sls, info = S.roof(rp, B, B, "irimoya", "hongawara", bear_y=K["bear_y"], g_out=K["g_out"], ov=K["g_out"] + 1.30,
                       ridge_courses=5)
    a.merge(rp)
    floors = [{"name": "upper", "rect": (cx - 1.9, cx + 1.9, cz - 1.9, cz + 1.9), "y": y_f, "obstacles": [
        (-0.2, 0.2, -0.2, 0.2), (B - 0.2, B + 0.2, -0.2, 0.2), (-0.2, 0.2, -B - 0.2, -B + 0.2),
        (B - 0.2, B + 0.2, -B - 0.2, -B + 0.2)], "enclosed": False}]
    # budget class: the PLAYBOOK §12 table has no tower class; a temple's one bell tower is counted as a large /
    # landmark structure (decision W2P2: its curved roof alone is ~700 faces in Resolution 3, over the standard 800
    # with the tower; Resolution 1 / 2 do fit the standard 6,000 / 2,300)
    return a, dict(W=B, D=B, K=K, info=info, sls=sls, floors=floors, budget="large", form="degumi",
                   covering="hongawara")


ASSEMBLIES = {"hall": hall, "hall_kokera": hall_kokera, "hondo": hondo, "shoro": shoro}


# ------------------------------------------------------------------------------------------------ checks
def sori_checks(a, ctx):
    """S1-S5: the curved roof's own proofs."""
    res = []
    info, sls, K = ctx["info"], ctx["sls"], ctx["K"]
    # S1 hips shared: front/back and side surfaces meet on every hip (same covering height)
    worst = 0.0
    n = 0
    for ss in sls:
        if ss.name not in ("front", "back"):
            continue
        for end in (0, 1):
            u_c, sg = (ss.u_lo, 1.0) if end == 0 else (ss.u_hi, -1.0)
            for k in range(1, 12):
                t = (ss.ov + ctx["D"] / 4) * k / 12
                x, z = ss.xz(u_c + sg * t, t)
                y0 = ss.cs(u_c + sg * t, t)
                for o in sls:
                    if o.name in ("left", "right"):
                        u, d = o.ud(x, z)
                        if R_inside(o, x, z):
                            worst = max(worst, abs(o.cs(u, d) - y0))
                            n += 1
    res.append(("S1 hips shared: the front / back and side surfaces meet on every hip (<= 5 mm)", worst <= 0.005,
                "%d hip samples, worst %.4f m" % (n, worst)))
    # S2 the covering stays over the rafters (the hidden roof never inverts) everywhere on every slope
    worst = 9.9
    for ss in sls:
        for i in range(1, 20):
            u = ss.u_lo + (ss.u_hi - ss.u_lo) * i / 20
            top = ss.top(u)
            for j in range(0, 12):
                d = top * j / 12
                worst = min(worst, ss.cs(u, d) - ss.raft_top(u, d))
    res.append(("S2 covering base >= 5 cm over the rafter tops everywhere (eave stack, hidden roof)", worst >= 0.05,
                "smallest gap %.3f m" % worst))
    # S3 brackets / walls / columns under the roof: nothing of another sub-part reaches over the rafter undersides
    bad, nv = [], 0
    for s in a.solids:
        if getattr(s, "src", None) in ("roof",) or not s.vis:
            continue
        for v in s.verts:
            y = S.under(info, v[0], v[2])
            if y is None:
                continue
            nv += 1
            if v[1] > y + 0.03:
                bad.append((s.src, s.tag, tuple(round(q, 2) for q in v), round(v[1] - y, 3)))
    res.append(("S3 brackets, columns, walls stay under the rafters (<= 3 cm)", not bad,
                "%d vertices under the roof%s" % (nv, ("; e.g. %s" % bad[:3]) if bad else "")))
    # S4 the rafters bear on the gangyo / keta: base-rafter underside at the bearing line and the wall line
    ds = []
    for ss in sls:
        um = (ss.u_lo + ss.u_hi) / 2
        ds.append(abs(ss.base_bot(um, ss.d_b) - K["bear_y"]))
        ds.append(abs(ss.base_bot(um, ss.ov) - K["keta_y"]))
    res.append(("S4 base rafters bear on the gangyo and the wall keta (<= 1 cm)", max(ds) <= 0.01,
                "worst %.4f m (gangyo top %.3f, keta top %.3f, g_out %.3f)" % (max(ds), K["bear_y"], K["keta_y"],
                                                                          K["g_out"])))
    return res


def R_inside(o, x, z):
    from jpparts import roofs as R
    return any(R._inside(pc, x, z, eps=1e-4) for pc in o.pieces)


def mlod_checks(path, lods, budget):
    res = []
    L = {mlod.lod_name(l.resolution): l for l in lods}
    res.append(("C5 LODs (vanilla house set)", all(k in L for k in ("Resolution 1", "Resolution 2", "Resolution 3",
                                                                   "Geometry", "View Geometry", "Fire Geometry",
                                                                   "Roadway", "Memory")),
                ", ".join("%s %d" % (k, len(v.faces)) for k, v in L.items())))
    got = tuple(len(L["Resolution %d" % k].faces) for k in (1, 2, 3))
    bud = BUDGETS[budget]
    res.append(("C5 face budget (%s: %d / %d / %d)" % ((budget,) + bud), all(g <= m for g, m in zip(got, bud)),
                "%d / %d / %d" % got))
    for lname in ("Geometry", "View Geometry", "Fire Geometry"):
        l = L[lname]
        comps = [s for s in l.selections if s.startswith("Component")]
        badc = [c for c in comps if mlod.component_report(l, c)]
        covered = set()
        for c in comps:
            covered |= l.selections[c][1]
        res.append(("C7 %s closed + convex" % lname, not badc and len(covered) == len(l.faces),
                    "%d components, %d bad, %d faces outside" % (len(comps), len(badc), len(l.faces) - len(covered))))
    badm = set()
    for l in lods:
        for _, _, tex, mat in l.faces:
            for p in (tex, mat):
                if p and not p.lower().startswith(checks.ALLOWED_VANILLA) and not (
                        p.lower().startswith("jp\\common\\materials\\") and os.path.isfile(os.path.join(DEV, "src", p))):
                    badm.add(p)
    res.append(("C2 library materials only", not badm, "all library / vanilla" if not badm else str(sorted(badm)[:3])))
    return res, L


def floor_checks(L, floors):
    road = L["Roadway"]
    miss = n = 0
    for f in floors:
        x0, x1, z0, z1 = f["rect"]
        for i in range(9):
            for j in range(9):
                x, z = x0 + 0.05 + (x1 - x0 - 0.1) * i / 8, z0 + 0.05 + (z1 - z0 - 0.1) * j / 8
                if any(a0 <= x <= a1 and b0 <= z <= b1 for (a0, a1, b0, b1) in f["obstacles"]):
                    continue
                n += 1
                if not any(abs(h - f["y"]) < 0.02 for h, _ in BC.road_heights(road, x, z)):
                    miss += 1
    gcomps = checks.components(L["Geometry"])
    smp = checks.roadway_samples(road)
    off = 0
    for x, y, z, tex in smp:
        tops = [r[1] for c in gcomps if not c["door"] for r in [checks.ray_y(c, x, z)] if r and r[1] <= y + 0.05]
        if not tops or abs(max(tops) - y) > 0.03:
            off += 1
    return [("C7 walkable floors have Roadway at floor height", not miss, "%d/%d samples" % (n - miss, n)),
            ("C7 Roadway on Geometry (+-3 cm)", off == 0, "%d/%d samples on a Geometry top" % (len(smp) - off,
                                                                                               len(smp)))]


def binarize(names):
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\parts\_test_w2p2"):
        return {n: (False, r"P:\DZ or P:\JP\parts\_test_w2p2 missing") for n in names}
    out = os.path.join(OUT, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\parts", "-binpath=P:\\bin", "P:\\JP\\parts\\_test_w2p2", out, "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    wb(os.path.join(OUT, "binarize.log"), " ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr)
    res = {}
    for n in names:
        fp = None
        for root, _, files in os.walk(out):
            if n + ".p3d" in files:
                fp = os.path.join(root, n + ".p3d")
        if fp and open(fp, "rb").read(4) == b"ODOL":
            res[n] = (True, "ODOL, %d bytes" % os.path.getsize(fp))
        else:
            res[n] = (False, "no ODOL (see data/parts_test/w2p2/binarize.log)")
    return res


def main(argv):
    want = [x for x in argv if not x.startswith("--")] or list(ASSEMBLIES)
    allres = {}
    for nm in want:
        a, ctx = ASSEMBLIES[nm]()
        zlog = []
        ZF.resolve(a, log=zlog)
        path = os.path.join(SRC, "w2p2_" + nm + ".p3d")
        a.write(path, geo_props=GEO_PROPS, mass=40000.0)
        lods = mlod.read_mlod(path)
        res, L = mlod_checks(path, lods, ctx["budget"])
        res += floor_checks(L, ctx["floors"])
        g3 = []
        BC.run_g3(a, L, ctx["floors"], lambda c, o, d: g3.append((c, bool(o), d)))
        res += g3
        res += sori_checks(a, ctx)
        allres["w2p2_" + nm] = {"faces": {mlod.lod_name(l.resolution): len(l.faces) for l in lods}, "checks": res,
                                "zfight_resolved": zlog, "kumimono": {k: v for k, v in ctx["K"].items() if k != "nodes"},
                                "roof": {k: v for k, v in ctx["info"].items() if k not in ("sori",)}}
    if "--no-binarize" not in argv:
        bz = binarize(list(allres))
        for nm in allres:
            allres[nm]["checks"].append(("Binarize (cwd P:\\) -> ODOL", bz[nm][0], bz[nm][1]))
    nfail = 0
    for nm, r in allres.items():
        print("== %s  %s" % (nm, r["faces"]))
        for c, o, dt in r["checks"]:
            nfail += 0 if o else 1
            if not o or "-v" in argv:
                print("  %-4s %-70s %s" % ("OK" if o else "FAIL", c[:70], str(dt)[:300]))
        print("  %d/%d pass" % (sum(1 for c in r["checks"] if c[1]), len(r["checks"])))
    jp = os.path.join(DEV, "parts", "w2p2_assembly_checks.json")
    prev = json.load(open(jp, encoding="utf-8")) if os.path.isfile(jp) else {}
    for nm, r in allres.items():
        prev[nm] = {"faces": r["faces"], "kumimono": r["kumimono"], "zfight_resolved": r["zfight_resolved"],
                    "roof": json.loads(json.dumps(r["roof"], default=str)),
                    "checks": [{"check": c, "ok": bool(o), "detail": str(dt)} for c, o, dt in r["checks"]]}
    wb(jp, json.dumps(prev, indent=1))
    print("%d assemblies, %d failures" % (len(allres), nfail))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
