#!/usr/bin/env python3
r"""W2P1 offline assemblies (proofs, NOT shipped buildings: W2S makes the shells): the village shrine and temple parts
assembled the way a shell will use them, written as MLOD, put through zfight.resolve (as buildings/pipeline.py does),
checked (C2 / C5 / C7 + buildcheck.run_g3 C10-C22 incl. C20, plus koran / stair / head-room checks) and binarized.

  python w2p1_assembly.py [name ...] [--no-binarize]

Assemblies (kit frame: x along the front, z 0 = the front wall line, +z out, y 0 = GRADE):
  honden        issha honden (1 x 1 ken) on stilts (+1.00): giboshi koran round three sides with wakishoji, kizahashi,
                board tobira opening out, board walls + gables, nagare roof (kokera) with kohai posts, okichigi (soto)
                + 3 katsuogi
  haiden        village haiden (3 x 2 ken) on a boarded floor (+0.60): front en with plain koran + kizahashi, latticed
                tobira in the middle bay, fixed lattice fronts in the side bays, board walls, kokera kirizuma roof with
                oni-ita, a kohai over the stair bay
  temple_hall   small temple hall (3 x 3 ken, +0.60): front en with plain koran + kizahashi, sankarado in the middle bay,
                hinged grid shitomido in the side bays, shinkabe walls, hogyo sangawara roof with a tile hoju, a tiled
                kohai
Outputs: src/JP/parts/_test_w2p1/<name>.p3d (MLOD, not committed; binarized copies in data/parts_test/w2p1/),
parts/w2p1_assembly_checks.json (all results, committed).
"""
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, checks, mlod, raycheck, walls, frame, roofs as R, zfight as ZF  # noqa: E402
from jpparts import koran as KR, tobira as TB, nagare as NG, ornament as ORN, stilts as STL, shitomi as SH  # noqa
from jpparts import buildcheck as BC  # noqa: E402
from jpparts.assemble import Builder  # noqa: E402
from jpparts.core import Part, KEN, HALF, POST, EAVE_Y, WALL_H, box  # noqa: E402

DEV = core.DEV
SRC = os.path.join(DEV, "src", "JP", "parts", "_test_w2p1")
OUT = os.path.join(DEV, "data", "parts_test", "w2p1")
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
GEO = {"class": "house", "map": "house", "damage": "no", "autocenter": "0"}


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.replace("\r\n", "\n").encode("utf-8"))


def frames(W, D):
    return {"front": (0.0, (0.0, 0.0, 0.0)), "back": (180.0, (W, 0.0, -D)), "left": (90.0, (0.0, 0.0, -D)),
            "right": (-90.0, (W, 0.0, 0.0))}


def hall_box(H, B, W, D, kind="board_vertical", front_doors=(), front_fixed=(), finish="nakanuri", gables=True,
             t=0.45, fam="itabuki", hip=False):
    """Posts on every ken node, walls on four sides (front bays with doors / fixed fronts left open for their parts),
    keta, gable walls. Floor frame (y 0 = floor)."""
    F = frames(W, D)
    for side, L in (("front", W), ("back", W), ("left", D), ("right", D)):
        xs = [k * KEN for k in range(int(round(L / KEN)) + 1)]
        B.posts_on(F[side], xs, 0.0, WALL_H)
    holes = [(k * KEN + POST / 2, (k + 1) * KEN - POST / 2, 0.0, 2.0) for k in list(front_doors) + list(front_fixed)]
    kw = {"finish": finish} if kind == "shinkabe" else {"mat": "wood_weathered"}
    B.wall(F["front"], "front", kind, 0.0, W, 0.0, WALL_H, openings_=holes, **kw)
    for side, L in (("back", W), ("left", D), ("right", D)):
        B.wall(F[side], side, kind, 0.0, L, 0.0, WALL_H, **kw)
    for side, L in (("front", W), ("back", W)) + ((("left", D), ("right", D)) if hip else ()):
        k = Part("keta", "", "")
        ext = 0.06 if hip else 0.30
        frame.keta(k, -ext, L + ext)
        B.put(k, F[side])
    if gables:
        for side in ("left", "right"):
            g = Part("gable", "", "")
            walls.gable(g, D, t, EAVE_Y, "_board")
            B.put(g, F[side])


# ------------------------------------------------------------------------------------------------ honden
def honden():
    W = D = KEN
    drop = 1.0
    H = Part("honden", "", "_test_w2p1", tiers=[1, 2, 3], used_for="W2P1 proof: village honden on stilts")
    H.wear = "_w1"
    B = Builder(H)
    F = frames(W, D)
    STL.platform(H, W, D, drop, "honden")
    hall_box(H, B, W, D, front_doors=(0,))
    B.place_door(TB.part_tobira("_board_out"), F["front"], 0.0, 0.0, label="Honden doors (board, open out)")
    en = KR.en_wrap(H, W, D, drop=drop, style="giboshi", stair=W / 2, waki=True)
    rp = Part("roof", "", "")
    sls, info = NG.nagare(rp, W, D, drop=drop, gov=0.60)
    yr = info["ridge"][0][1]
    top = info.get("ridge_top", yr + 0.08)
    for x in (-0.50, W + 0.50):
        ORN.chigi(rp, x, top - 0.02, -D / 2, cut="soto")
    ORN.katsuogi(rp, -0.6, W + 0.6, top - 0.01, -D / 2, n=3, r=0.07, length=0.70, inset=0.45)
    H.merge(rp)
    M = H.transformed(0.0, (0.0, drop, 0.0))
    rooms = [{"name": "honden", "rect": (POST / 2, W - POST / 2, -D + POST / 2, -POST / 2), "y": drop},
             {"name": "en", "rect": (-1.2, W + 1.2, 0.1, 1.2), "y": drop, "enclosed": False}]
    return M, dict(W=W, D=D, drop=drop, rooms=rooms, stair=en["stair"], roof=info, en=True)


# ------------------------------------------------------------------------------------------------ haiden
def haiden():
    W, D = 3 * KEN, 2 * KEN
    drop = 0.60
    H = Part("haiden", "", "_test_w2p1", tiers=[1, 2], used_for="W2P1 proof: village haiden")
    H.wear = "_w1"
    B = Builder(H)
    F = frames(W, D)
    STL.platform(H, W, D, drop, "hall")
    hall_box(H, B, W, D, front_doors=(1,), front_fixed=(0, 2))
    B.place_door(TB.part_tobira("_lattice_in"), F["front"], KEN, 0.0, label="Haiden doors (lattice, open in)")
    portals = []
    for k in (0, 2):
        s = Part("lattice", "", "")
        SH.shitomi(s, 0.0, KEN, "_fixed")
        B.put(s, F["front"], k * KEN)
        portals.append(("lattice%d" % k, (k * KEN + 0.06, (k + 1) * KEN - 0.06, drop + 0.62, drop + 2.0, -0.10, 0.10)))
    en = KR.en_wrap(H, W, D, drop=drop, style="plain", sides=("front",), stair=W / 2, waki=False)
    rp = Part("roof", "", "")
    sls, info = R.roof(rp, W, D, "kirizuma", "itabuki", eave_y=EAVE_Y)
    (x0, yr, zr), (x1, _, _) = info["ridge"]
    for x, sg in ((x0, -1), (x1, 1)):
        ORN.oniita(rp, x + (0.0 if sg > 0 else 0.0), yr + 0.04, zr, sg)
    H.merge(rp)
    kp = Part("kohai", "", "")
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    NG.kohai(kp, KEN, 2 * KEN, zp, R.PITCH["itabuki"], R.EAVE_OV["itabuki"], EAVE_Y, "itabuki", drop)
    H.merge(kp)
    M = H.transformed(0.0, (0.0, drop, 0.0))
    rooms = [{"name": "haiden", "rect": (POST / 2, W - POST / 2, -D + POST / 2, -POST / 2), "y": drop},
             {"name": "en", "rect": (0.1, W - 0.1, 0.1, 1.2), "y": drop, "enclosed": False}]
    return M, dict(W=W, D=D, drop=drop, rooms=rooms, stair=en["stair"], roof=info, portals=portals, en=True)


# ------------------------------------------------------------------------------------------------ temple hall
def temple_hall():
    W = D = 3 * KEN
    drop = 0.60
    H = Part("temple_hall", "", "_test_w2p1", tiers=[1, 2], used_for="W2P1 proof: small temple hall (hogyo)")
    H.wear = "_w1"
    B = Builder(H)
    F = frames(W, D)
    STL.platform(H, W, D, drop, "hall")
    hall_box(H, B, W, D, kind="shinkabe", front_doors=(1,), front_fixed=(0, 2), gables=False, hip=True)
    B.place_door(TB.part_tobira("_sankara_in"), F["front"], KEN, 0.0, label="Hall doors (sankarado, open in)")
    for k in (0, 2):
        B.place_door(SH.part_shitomi("_hinged"), F["front"], k * KEN, 0.0, label="Shitomido %d (upper leaf)" % k)
    en = KR.en_wrap(H, W, D, drop=drop, style="plain", sides=("front",), stair=W / 2, waki=False)
    rp = Part("roof", "", "")
    sls, info = NG.hogyo(rp, W, "sangawara", apex="hoju_kawara")
    H.merge(rp)
    kp = Part("kohai", "", "")
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    NG.kohai(kp, KEN, 2 * KEN, zp, R.PITCH["sangawara"], R.EAVE_OV["sangawara"], EAVE_Y, "sangawara", drop)
    H.merge(kp)
    M = H.transformed(0.0, (0.0, drop, 0.0))
    rooms = [{"name": "hall", "rect": (POST / 2, W - POST / 2, -D + POST / 2, -POST / 2), "y": drop},
             {"name": "en", "rect": (0.1, W - 0.1, 0.1, 1.2), "y": drop, "enclosed": False}]
    return M, dict(W=W, D=D, drop=drop, rooms=rooms, stair=en["stair"], roof=info, en=True, budget="large")


ASSEMBLIES = {"honden": honden, "haiden": haiden, "temple_hall": temple_hall}


# ------------------------------------------------------------------------------------------------ checks
def koran_checks(M, ctx, lods):
    """KR1 kizahashi ramp <= 38 deg, KR2 >= 1.10 clear between its rails, KR3 Roadway continuous floor -> en -> stair
    -> grade along the stair centreline, KR4 head room >= 2.05 over the stair, KR5 head room >= 2.00 over the en,
    KR6 the koran collision runs the en's open edges except the stair gap."""
    L = {mlod.lod_name(l.resolution): l for l in lods}
    road = L["Roadway"]
    res = []
    K = ctx["stair"]
    drop = ctx["drop"]
    res.append(("KR1 kizahashi walk ramp <= 38 deg (D4)", K["angle"] <= 38.0 + 1e-6, "%.2f deg, %d risers of %.3f, run "
                "%.3f" % (K["angle"], K["n"], K["riser"], K["run"])))
    clear = (K["xb"] - 0.05) - (K["xa"] + 0.05)
    res.append(("KR2 kizahashi clear between its rails >= 1.10 m (D4)", clear >= 1.10 - 1e-6, "%.3f m" % clear))
    xc = (K["xa"] + K["xb"]) / 2
    zs = [-0.5, 0.0, 0.5, 1.0, KR.DEPTH - 0.02] + [KR.DEPTH + K["run"] * f for f in (0.1, 0.3, 0.5, 0.7, 0.9)]
    bad = []
    prev = None
    for z in zs:
        hs = [h for h, _ in BC.road_heights(road, xc, z)]
        expect = drop if z <= KR.DEPTH else drop - drop * (z - KR.DEPTH) / K["run"]
        if not any(abs(h - expect) < 0.03 for h in hs):
            bad.append((round(z, 2), round(expect, 2), [round(h, 2) for h in hs]))
    res.append(("KR3 Roadway continuous: floor -> en -> kizahashi -> grade on the stair centreline", not bad,
                "%d samples on the expected walk line%s" % (len(zs), (", MISSING %s" % bad[:3]) if bad else "")))
    gcomps = checks.components(L["Geometry"])
    worst = (99.0, None)
    for i in range(1, 30):
        z = KR.DEPTH + K["run"] * i / 30
        yr = drop - drop * (z - KR.DEPTH) / K["run"]
        for x in (K["xa"] + 0.2, xc, K["xb"] - 0.2):
            for c in gcomps:
                r = checks.ray_y(c, x, z)
                if r and r[0] > yr + 0.05 and r[0] - yr < worst[0]:
                    worst = (r[0] - yr, (round(x, 2), round(z, 2), c["name"]))
    res.append(("KR4 head room over the kizahashi >= 2.05 m (D4)", worst[0] >= 2.05 - 1e-6,
                ("lowest %.2f m at %s" % worst) if worst[1] else "open above"))
    worst = (99.0, None)
    x0, x1 = -1.0 if ctx["W"] < 3 else 0.2, ctx["W"] + (1.0 if ctx["W"] < 3 else -0.2)
    for i in range(0, 25):
        x = x0 + (x1 - x0) * i / 24
        for z in (0.15, 0.6, 1.15):
            for c in gcomps:
                r = checks.ray_y(c, x, z)
                if r and r[0] > drop + 0.05 and r[0] - drop < worst[0]:
                    worst = (r[0] - drop, (round(x, 2), round(z, 2), c["name"]))
    res.append(("KR5 head room over the front en >= 2.00 m (D2 door head)", worst[0] >= 2.0 - 1e-6,
                "lowest %.2f m at %s" % worst))
    rails = [c for c in M.solids if c.tag == "koran_geo"]
    res.append(("KR6 koran collision on the en edges (+ the stair sides)", len(rails) >= 4,
                "%d koran Geometry slabs" % len(rails)))
    return res


def mlod_checks(lods, budget="standard"):
    res = []
    L = {mlod.lod_name(l.resolution): l for l in lods}
    res.append(("C5 LODs", all(k in L for k in ("Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "Memory",
                                               "Roadway", "View Geometry", "Fire Geometry")),
                ", ".join("%s %d" % (k, len(v.faces)) for k, v in L.items())))
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
    n = [len(L["Resolution %d" % k].faces) for k in (1, 2, 3)]
    lim = {"standard": (6000, 2300, 800), "large": (12000, 4600, 1600)}[budget]
    res.append(("C5 budget: %s building (<= %d / %d / %d; PLAYBOOK §12)" % ((budget,) + lim),
                all(a <= b for a, b in zip(n, lim)), "%d / %d / %d" % tuple(n)))
    return res


def binarize(names):
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\parts\_test_w2p1"):
        return {n: (False, r"P:\DZ or P:\JP\parts\_test_w2p1 missing") for n in names}
    out = os.path.join(OUT, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\parts", "-binpath=P:\\bin", "P:\\JP\\parts\\_test_w2p1", out, "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    wb(os.path.join(OUT, "binarize.log"), " ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr)
    res = {}
    for n in names:
        fp = None
        for root, _, files in os.walk(out):
            if n + ".p3d" in files:
                fp = os.path.join(root, n + ".p3d")
        res[n] = (True, "ODOL, %d bytes" % os.path.getsize(fp)) if fp and open(fp, "rb").read(4) == b"ODOL" else \
            (False, "no ODOL (see data/parts_test/w2p1/binarize.log)")
    return res


def main(argv):
    want = [a for a in argv if not a.startswith("--")] or list(ASSEMBLIES)
    allres = {}
    for nm in want:
        M, ctx = ASSEMBLIES[nm]()
        zlog = []
        ZF.resolve(M, log=zlog)
        p = os.path.join(SRC, nm + ".p3d")
        M.write(p, geo_props=GEO, mass=30000.0)
        lods = mlod.read_mlod(p)
        res = mlod_checks(lods, ctx.get("budget", "standard"))
        L = {mlod.lod_name(l.resolution): l for l in lods}
        BC.run_g3(M, L, ctx["rooms"], lambda c, o, d: res.append((c, o, d)), extra_portals=ctx.get("portals", ()))
        res += koran_checks(M, ctx, lods)
        allres[nm] = {"faces": {mlod.lod_name(l.resolution): len(l.faces) for l in lods}, "checks": res,
                      "zfight_resolve": zlog}
    if "--no-binarize" not in argv:
        bz = binarize(want)
        for nm in want:
            allres[nm]["checks"].append(("Binarize (cwd P:\\) -> ODOL", bz[nm][0], bz[nm][1]))
    nfail = 0
    for nm, r in allres.items():
        print("== %s  %s  %s" % (nm, r["faces"], "; ".join(r["zfight_resolve"])))
        for c, o, dt in r["checks"]:
            nfail += 0 if o else 1
            print("  %-4s %-62s %s" % ("OK" if o else "FAIL", c[:62], dt[:200]))
    jp = os.path.join(DEV, "parts", "w2p1_assembly_checks.json")
    prev = json.load(open(jp, encoding="utf-8")) if os.path.isfile(jp) else {}
    for nm, r in allres.items():
        prev[nm] = {"faces": r["faces"], "zfight_resolve": r["zfight_resolve"],
                    "checks": [{"check": c, "ok": bool(o), "detail": dt} for c, o, dt in r["checks"]]}
    wb(jp, json.dumps(prev, indent=1))
    print("%d assemblies, %d failures" % (len(allres), nfail))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
