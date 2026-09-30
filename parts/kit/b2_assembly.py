#!/usr/bin/env python3
r"""B2 test assemblies (offline proofs, not island buildings): each new B2 part assembled with kit parts the way a
building uses it, written as MLOD, checked, and binarized.

  python b2_assembly.py [name ...] [--no-binarize]

Assemblies (ASSEMBLIES below; the renders are parts/kit/render_b2.py):
  koya_farmhouse   7 x 5 ken yosemune THATCH on adzed posts and soseki: koyagumi sasu, log members, joya 3 ken with
                   geya aisles (1 ken) front and back under the one sweeping thatch slope (G1 A1-4)
  koya_farm_soot   the same, sooted wear level (koyagumi soot=True + soot_roof on the roof)
  koya_hut         3 x 2 ken kirizuma THATCH poor hut: sasu on log tie beams, thatch gables, sooted
  koya_workshop    4 x 3 ken kirizuma SANGAWARA on planed posts: koyagumi wagoya, sawn, tile gables
  koya_hip         4 x 3 ken yosemune SANGAWARA: wagoya hip framing (hip rafters, end purlins, end beams)
Outputs: src/JP/parts/_test_b2/<name>.p3d (MLOD; binarized copies in data/parts_test/b2/), and
data/parts_test/b2/<name>_checks.json + parts/b2_assembly_checks.json (all results, committed).
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, checks, mlod, raycheck, walls, frame, found, roofs as R, floors as FL, koyagumi as KY  # noqa
from jpparts.core import Part, KEN, HALF, POST, POST_FARM, EAVE_Y, WALL_H, box  # noqa: E402

DEV = core.DEV
SRC = os.path.join(DEV, "src", "JP", "parts", "_test_b2")
OUT = os.path.join(DEV, "data", "parts_test", "b2")
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
KOYA_TAGS = ("hari", "ushibari", "geya_bari", "tsuka", "munazuka", "moya", "munagi", "koyanuki", "sumigi", "tsunagi",
             "rafter_in", "sasu", "sumi_sasu", "tsuma_sasu", "lashing", "joya_plate", "joya_post")
REACH = {"rafter_in": 0.09, "sasu": 0.55, "sumi_sasu": 0.55, "tsuma_sasu": 0.55, "lashing": 0.40}


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.replace("\r\n", "\n").encode("utf-8"))


# ------------------------------------------------------------------------------------------------ builders
def post_frame(a, W, D, adzed, soseki=True, every=KEN, hip=False, y1=WALL_H):
    """Posts at every node of the perimeter (on soseki or on a dodai), keta on the eave walls (all four if hip)."""
    nodes = set()
    k = 0
    while k * every <= W + 1e-6:
        nodes.add((round(k * every, 4), 0.0))
        nodes.add((round(k * every, 4), round(-D, 4)))
        k += 1
    k = 0
    while k * every <= D + 1e-6:
        nodes.add((0.0, round(-k * every, 4)))
        nodes.add((round(W, 4), round(-k * every, 4)))
        k += 1
    size = POST_FARM if adzed else POST
    for i, (x, z) in enumerate(sorted(nodes)):
        frame.post(a, x, z=z, y1=y1, size=size, adzed=adzed)
        if soseki:
            found.soseki(a, x, z, i % 8)
    ext = 0.06 if hip else 0.30                  # hipped: the keta stop at the corners (no poke into the hip slopes)
    frame.keta(a, -ext, W + ext, z=0.0)
    frame.keta(a, -ext, W + ext, z=-D)
    if hip:
        a.add(box(-0.06, 0.06, EAVE_Y - core.KETA_H, EAVE_Y, -D - 0.06, 0.06, "wood_weathered", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="keta"))
        a.add(box(W - 0.06, W + 0.06, EAVE_Y - core.KETA_H, EAVE_Y, -D - 0.06, 0.06, "wood_weathered", vis=(1, 2, 3),
                  geo=True, view=True, fire=True, tag="keta"))
    return sorted(nodes)


def gable_ends(a, W, D, t, variant):
    for fr in ((90.0, (0.0, 0.0, -D)), (-90.0, (W, 0.0, 0.0))):
        g = Part("gable", "", "")
        walls.gable(g, D, t, EAVE_Y, variant)
        a.merge(g.transformed(fr[0], fr[1]))


def roof_frame(W, D, form, fam, **kw):
    """The roof + its koyagumi in ONE sub-part (the rafters continue inside the roof body, see koyagumi docstring)."""
    rp = Part("roof", "", "")
    sls, info = R.roof(rp, W, D, form, fam, eave_y=EAVE_Y, walkable=(fam != "thatch"))
    soot = kw.pop("soot", False)
    K = KY.koyagumi(rp, W, D, info, eave_y=EAVE_Y, soot=soot, **kw)
    if soot:
        K["sooted_roof_solids"] = KY.soot_roof(rp)
    return rp, sls, info, K


def doma(a, W, D):
    a.merge(FL.doma("doma", 0.0, W, -D, 0.0, road=(POST / 2, W - POST / 2, -D + POST / 2, -POST / 2), y=0.05))


def koya_farmhouse(soot=False, name="koya_farmhouse"):
    W, D = 7 * KEN, 5 * KEN
    a = Part(name, "", "_test_b2", tiers=[1, 2], used_for="B2 proof: thatch over koyagumi on posts")
    a.wear = "_w1"
    nodes = post_frame(a, W, D, adzed=True, hip=True)
    rp, sls, info, K = roof_frame(W, D, "yosemune", "thatch", members="log", geya=(KEN, KEN), floor_y=0.05,
                                  soot=soot)
    a.merge(rp)
    doma(a, W, D)
    for (x, z, y0, y1) in K["posts"]:
        found.soseki(a, x, z, int(x * 10) % 8)
    return a, dict(W=W, D=D, sls=sls, info=info, K=K, nodes=nodes, floor=0.05)


def koya_farm_soot():
    return koya_farmhouse(soot=True, name="koya_farm_soot")


def koya_hut():
    W, D = 3 * KEN, 2 * KEN
    a = Part("koya_hut", "", "_test_b2", tiers=[1], used_for="B2 proof: poor hut open to the sooted thatch")
    a.wear = "_w2"
    nodes = post_frame(a, W, D, adzed=True)
    gable_ends(a, W, D, R.PITCH["thatch"], "_thatch")
    rp, sls, info, K = roof_frame(W, D, "kirizuma", "thatch", members="log", floor_y=0.05, soot=True)
    a.merge(rp)
    doma(a, W, D)
    return a, dict(W=W, D=D, sls=sls, info=info, K=K, nodes=nodes, floor=0.05)


def koya_workshop():
    W, D = 4 * KEN, 3 * KEN
    a = Part("koya_workshop", "", "_test_b2", tiers=[2, 3], used_for="B2 proof: tile roof over wagoya koyagumi")
    a.wear = "_w1"
    nodes = post_frame(a, W, D, adzed=False, soseki=True)
    gable_ends(a, W, D, R.PITCH["sangawara"], "_tile")
    rp, sls, info, K = roof_frame(W, D, "kirizuma", "sangawara", members="sawn", floor_y=0.05)
    a.merge(rp)
    doma(a, W, D)
    return a, dict(W=W, D=D, sls=sls, info=info, K=K, nodes=nodes, floor=0.05)


def koya_hip():
    W, D = 4 * KEN, 3 * KEN
    a = Part("koya_hip", "", "_test_b2", tiers=[2, 3], used_for="B2 proof: hipped tile roof over wagoya koyagumi")
    a.wear = "_w1"
    nodes = post_frame(a, W, D, adzed=False, hip=True)
    rp, sls, info, K = roof_frame(W, D, "yosemune", "sangawara", members="sawn", floor_y=0.05)
    a.merge(rp)
    doma(a, W, D)
    return a, dict(W=W, D=D, sls=sls, info=info, K=K, nodes=nodes, floor=0.05)


ASSEMBLIES = {"koya_farmhouse": koya_farmhouse, "koya_farm_soot": koya_farm_soot, "koya_hut": koya_hut,
              "koya_workshop": koya_workshop, "koya_hip": koya_hip}


# ------------------------------------------------------------------------------------------------ checks
def koya_checks(a, ctx):
    """Framing under the roof, head room, beams on posts."""
    res = []
    sls, W, D = ctx["sls"], ctx["W"], ctx["D"]
    worst, n, bad = 0.0, 0, []
    for s in a.solids:
        if s.tag not in KOYA_TAGS or s.tag == "joya_post":
            continue
        allow = REACH.get(s.tag, 0.02)
        for v in s.verts:
            yr = KY.roof_under(sls, v[0], v[2])
            if yr is None:
                continue
            n += 1
            over = v[1] - yr
            if over > allow:
                bad.append((s.tag, tuple(round(c, 2) for c in v), round(over, 3)))
            worst = max(worst, over - allow)
    res.append(("KY1 framing stays under the roof (members <= 2 cm over the rafter plane; rafters in the roof body; "
                "sasu tips inside the thatch)", not bad, "%d vertices, %d over%s" % (n, len(bad), (
                    ", e.g. %s" % bad[:3]) if bad else "")))
    fl = ctx["floor"]
    lows = [(s.bbox()[2] - fl, s.tag) for s in a.solids if s.tag in KOYA_TAGS and s.tag != "joya_post"]
    low = min(lows)
    res.append(("KY2 head room under the framing >= 2.10 m (D4 + margin)", low[0] >= 2.10 - 1e-6,
                "lowest member %s at %.2f m over the floor" % (low[1], low[0])))
    posts = [(round(x, 3), round(z, 3)) for x, z in ctx["nodes"]] + [(round(x, 3), round(z, 3)) for x, z, _, _ in
                                                                    ctx["K"]["posts"]]
    unsup = []
    for x in ctx["K"]["frame_lines"]:
        for z in (0.0, round(-D, 3)):
            if not any(abs(px - x) < 0.01 and abs(pz - z) < 0.01 for px, pz in posts):
                unsup.append((x, z))
    res.append(("KY3 every frame line's beam ends on a post", not unsup, "%d frame lines%s" % (
        len(ctx["K"]["frame_lines"]), ("; no post at %s" % unsup) if unsup else ", all on wall posts")))
    pk = raycheck.roof_pokes(a.solids)
    res.append(("C12 roof / wall intersection (no other sub-part inside a roof body > 3 cm)", not pk,
                "%d tile / board roof bodies clear" % sum(1 for s in a.solids if s.tag.startswith("roof_geo_"))
                if not pk else "; ".join("%s/%s (LOD %s) into %s %s by %.2f m" % x for x in pk[:4])))
    return res


def mlod_checks(path, lods):
    res = []
    L = {mlod.lod_name(l.resolution): l for l in lods}
    res.append(("C5 LODs", all(k in L for k in ("Resolution 1", "Resolution 2", "Resolution 3", "Geometry",
                                               "View Geometry", "Fire Geometry")),
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
    return res


def binarize(names):
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\parts\_test_b2"):
        return {n: (False, r"P:\DZ or P:\JP\parts\_test_b2 missing") for n in names}
    out = os.path.join(OUT, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\parts", "-binpath=P:\\bin", "P:\\JP\\parts\\_test_b2", out, "*.p3d"]
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
            res[n] = (False, "no ODOL (see data/parts_test/b2/binarize.log)")
    return res


def main(argv):
    want = [a for a in argv if not a.startswith("--")] or list(ASSEMBLIES)
    allres = {}
    for nm in want:
        a, ctx = ASSEMBLIES[nm]()
        p = os.path.join(SRC, nm + ".p3d")
        a.write(p, geo_props={"class": "house", "map": "house", "damage": "no", "autocenter": "0"}, mass=20000.0)
        lods = mlod.read_mlod(p)
        res = mlod_checks(p, lods) + koya_checks(a, ctx)
        allres[nm] = {"faces": {mlod.lod_name(l.resolution): len(l.faces) for l in lods}, "checks": res,
                      "koyagumi": {k: v for k, v in ctx["K"].items() if k != "posts"}}
    if "--no-binarize" not in argv:
        bz = binarize(want)
        for nm in want:
            allres[nm]["checks"].append(("Binarize (cwd P:\\) -> ODOL", bz[nm][0], bz[nm][1]))
    nfail = 0
    for nm, r in allres.items():
        print("== %s  %s" % (nm, r["faces"]))
        for c, o, dt in r["checks"]:
            nfail += 0 if o else 1
            print("  %-4s %-60s %s" % ("OK" if o else "FAIL", c[:60], dt))
    prev = {}
    jp = os.path.join(DEV, "parts", "b2_assembly_checks.json")
    if os.path.isfile(jp):
        prev = json.load(open(jp, encoding="utf-8"))
    for nm, r in allres.items():
        prev[nm] = {"faces": r["faces"], "koyagumi": r["koyagumi"],
                    "checks": [{"check": c, "ok": bool(o), "detail": dt} for c, o, dt in r["checks"]]}
    wb(jp, json.dumps(prev, indent=1))
    print("%d assemblies, %d failures" % (len(allres), nfail))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
