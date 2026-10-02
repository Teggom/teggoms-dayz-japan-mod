#!/usr/bin/env python3
r"""K3 offline proofs (not island buildings): the wall kit and the covered-corridor / kairo kit assembled the way D3's
compounds use them, written as MLOD, put through the building checks (FB2's z-fight resolver first, as
buildings/pipeline.py does), walkability checks and binarized.

  python k3_assembly.py [name ...] [--no-binarize] [-v]

Outputs: src/JP/parts/_test_k3/<name>.p3d (MLOD; binarized copies in data/parts_test/k3/) and
parts/k3_assembly_checks.json (all results, committed).
"""
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, checks, mlod, buildcheck as BC, zfight as ZF  # noqa: E402
from jpparts import striproof as SR  # noqa: E402
from jpparts.core import Part, KEN, HALF  # noqa: E402

DEV = core.DEV
SRC = os.path.join(DEV, "src", "JP", "parts", "_test_k3")
OUT = os.path.join(DEV, "data", "parts_test", "k3")
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
GEO_PROPS = {"class": "house", "map": "house", "damage": "no", "autocenter": "0"}
BUDGETS = {"large": (12000, 4600, 1600), "standard": (6000, 2300, 800), "small": (3000, 1150, 400)}


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.replace("\r\n", "\n").encode("utf-8"))


def place(dst, sub, deg=0.0, t=(0.0, 0.0, 0.0)):
    dst.merge(sub.transformed(deg, t))
    return dst


# ------------------------------------------------------------------------------------------------ cases (roof tests)
def _roof_L(family, profile="straight", body="open"):
    p = Part("case_roofL_" + family + profile, "", "test")
    D, ov = KEN, 0.60
    S = SR.Spec(D, ov, 2.85, family, profile=profile, body=body)
    a = Part("ra", "", "t")
    SR.straight(a, S, 2 * KEN, ("gable", "seam"), branches=((1, "+z"),))
    place(p, a, 0.0, (-D / 2 - 2 * KEN, 0.0, 0.0))
    c = Part("rc", "", "t")
    SR.junction(c, S, ("-x", "+z"))
    place(p, c)
    b = Part("rb", "", "t")
    SR.straight(b, S, 2 * KEN, ("seam", "gable"), branches=((0, "+z"),))
    place(p, b, 90.0, (0.0, 0.0, D / 2))
    return p


def _row(builds, gap=0.9, name="row"):
    """Lay part builders out along x (each part's own length + gap), for the look-sheets."""
    p = Part("case_" + name, "", "test")
    x = 0.0
    for fn in builds:
        q = fn()
        b = q.bbox()
        place(p, q, 0.0, (x - b[0], 0.0, 0.0))
        x += (b[1] - b[0]) + gap
    return p


def _walls_a():
    from jpparts import sitewall as W
    return _row([lambda: W.wall("tsuiji", KEN, ("end", "seam")),
                 lambda: W.wall("tsuiji", KEN, ("seam", "end"), finish="earth", cap="hongawara"),
                 lambda: W.wall("tsuiji", KEN, ("end", "end"), finish="suji5", cap="hongawara"),
                 lambda: W.wall("tsuiji", KEN, ("end", "end"), finish="neri"),
                 lambda: W.wall("dobei", KEN, ("end", "end"), finish="namako", hikae=True),
                 lambda: W.wall("dobei", KEN, ("end", "end"), finish="kuro")], name="walls_a")


def _walls_b():
    from jpparts import sitewall as W
    return _row([lambda: W.wall("itabei", KEN, ("end", "end")),
                 lambda: W.wall("itabei", KEN, ("end", "end"), cap="tile", kuro=True),
                 lambda: W.wall("yotsume", KEN, ("end", "end")),
                 lambda: W.wall("kenninji", KEN, ("end", "end")),
                 lambda: W.wall("shiba", KEN, ("end", "end")),
                 lambda: W.wall("takeho", KEN, ("end", "end")),
                 lambda: W.wall("ikegaki", KEN, ("end", "end"))], name="walls_b")


def _walls_c():
    from jpparts import sitewall as W
    return _row([lambda: W.wall("ishigaki", KEN, ("end", "end")),
                 lambda: W.wall("ishigaki", KEN, ("end", "end"), stone="uchikomi", H=1.2, retaining=True),
                 lambda: W.wall("bank", KEN, ("end", "end")),
                 lambda: W.wall("tsuiji", 2 * KEN, ("end", "end"), state="collapsed"),
                 lambda: W.wall("tsuiji", KEN, ("end", "end"), state="tiles"),
                 lambda: W.step("tsuiji", 2 * KEN, 0.6, ("end", "end"))], name="walls_c")


def _gates():
    from jpparts import sitewall as W
    return _row([lambda: W.gate_kabuki(1.5 * KEN), lambda: W.gate_kabuki(1.5 * KEN, roofed=True),
                 lambda: W.gate_munemon(1.5 * KEN), lambda: W.wicket("itabei"), lambda: W.wicket("dobei"),
                 lambda: W.wicket("kenninji")], gap=1.5, name="gates")


def _corner_test():
    from jpparts import sitewall as W
    return W.run_wall([(0.0, 0.0), (0.0, 4 * KEN), (5 * KEN, 4 * KEN)], "tsuiji",
                      gates=[(1, KEN, "kabuki_roofed", 1.5 * KEN)], name="cornertest")


def _roka_row():
    from jpparts import roka as R
    return _row([lambda: R.straight(KEN, ("open", "open"), ends=("gable", "seam")),
                 lambda: R.straight(2 * KEN, ("enclosed", "open"), "sangawara"),
                 lambda: R.straight(2 * KEN, ("half", "half"), "kokera", "sori"),
                 lambda: R.junction(("-x", "+z"), roof="sangawara"),
                 lambda: R.junction(("-x", "+x", "+z", "-z"), roof="hongawara"),
                 lambda: R.stair(2 * KEN, 0.91, roof="sangawara")], gap=1.6, name="roka_row")


def _roka_L():
    from jpparts import roka as R
    return R.run_roka([(0.0, 0.0), (5 * KEN, 0.0), (5 * KEN, 5 * KEN)], ("open", "enclosed"), "sangawara",
                      stairs=[(1, 2 * KEN, 2 * KEN, 0.455)], name="rokaL")


CASES = {
    "roka_row": _roka_row,
    "roka_L": _roka_L,
    "gates": _gates,
    "corner_test": _corner_test,
    "walls_a": _walls_a,
    "walls_b": _walls_b,
    "walls_c": _walls_c,
    "roofL_tile": lambda: _roof_L("sangawara"),
    "roofL_board_sori": lambda: _roof_L("kokera", "sori"),
}


# ================================================================================================ the proofs
def _hall(name, W, D, F, keta, door_z=None, grade=0.0):
    """A plain stand-in hall (NOT a shipped building): floor deck, corner + mid posts, plastered walls, a hipped
    sangawara roof (roofs.roof) with its keta top at F + keta; an opening (no leaf) on its x = W wall for the
    corridor, centred on z = door_z (hall frame: x 0..W, z 0..-D as roofs.py)."""
    from jpparts import roofs as RF
    from jpparts.core import box
    from jpparts.found import soseki
    rng = core.rng_for(name)
    h = Part(name, "", "test")
    h.add(box(0.0, W, F - 0.12, F, -D, 0.0, "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="hall_floor"))
    h.add(box(0.05, W - 0.05, -0.3, F - 0.12, -D + 0.05, -0.05, "stone_field", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="hall_base"))
    h.road([(0.0, F, 0.0), (W, F, 0.0), (W, F, -D), (0.0, F, -D)], "boards")
    nx, nz = int(round(W / KEN)), int(round(D / KEN))
    for i in range(nx + 1):
        for j in range(nz + 1):
            if 0 < i < nx and 0 < j < nz:
                continue
            if door_z is not None and i == nx and abs(-j * KEN - door_z) < 0.8:
                continue                    # no post in the doorway
            x, z = i * KEN, -j * KEN
            soseki(h, x, z, int(rng.random() * 8))
            h.add(box(x - 0.075, x + 0.075, 0.0, F + keta - 0.18, z - 0.075, z + 0.075, "wood_weathered",
                      vis=(1, 2, 3), geo=True, view=True, fire=True, tag="hall_post"))
    top = F + keta - 0.18
    t = 0.04
    walls = [((0.0, W), (0.0, 0.0), "x"), ((0.0, W), (-D, -D), "x"), ((0.0, 0.0), (0.0, -D), "z"),
             ((W, W), (0.0, -D), "z")]
    for (x0, x1), (z0, z1), ax in walls:
        if ax == "x":
            h.add(box(x0 + 0.075, x1 - 0.075, F, top, z0 - t, z0 + t, "wall_shikkui", vis=(1, 2, 3), geo=True,
                      view=True, fire=True, tag="hall_wall"))
        else:
            if abs(x0 - W) < 1e-6 and door_z is not None:
                for (a, b) in ((z1 + 0.075, door_z - 0.70), (door_z + 0.70, z0 - 0.075)):
                    h.add(box(x0 - t, x0 + t, F, top, a, b, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True,
                              fire=True, tag="hall_wall"))
                h.add(box(x0 - t, x0 + t, F + 2.15, top, door_z - 0.70, door_z + 0.70, "wall_shikkui", vis=(1, 2, 3),
                          geo=True, view=True, fire=True, tag="hall_wall"))
                h.add(box(x0 - 0.05, x0 + 0.05, F + 2.05, F + 2.15, door_z - 0.75, door_z + 0.75, "wood_weathered",
                          vis=(1, 2, 3), geo=True, view=True, fire=True, tag="hall_kamoi"))
                # the threshold carries the hall's Roadway out to the wall face (the corridor connector starts there)
                h.add(box(x0 - 0.04, x0 + 0.08, F - 0.10, F, door_z - 0.70, door_z + 0.70, "wood_weathered",
                          vis=(1, 2, 3), geo=True, view=True, fire=True, tag="hall_sill"))
                h.road([(x0 - 0.04, F, door_z - 0.70), (x0 + 0.08, F, door_z - 0.70), (x0 + 0.08, F, door_z + 0.70),
                        (x0 - 0.04, F, door_z + 0.70)], "boards")
            else:
                h.add(box(x0 - t, x0 + t, F, top, z1 + 0.075, z0 - 0.075, "wall_shikkui", vis=(1, 2, 3), geo=True,
                          view=True, fire=True, tag="hall_wall"))
    for (x0, x1), (z0, z1), ax in walls:
        if ax == "x":
            h.add(box(x0 - 0.06, x1 + 0.06, top, F + keta, z0 - 0.06, z0 + 0.06, "wood_weathered", vis=(1, 2, 3),
                      geo=True, view=True, fire=True, tag="hall_keta"))
        else:
            h.add(box(x0 - 0.06, x0 + 0.06, top + 0.003, F + keta - 0.003, z1 + 0.06, z0 - 0.06, "wood_weathered",
                      vis=(1, 2, 3), geo=True, view=True, fire=True, tag="hall_keta"))
    r = Part(name + "_roof", "", "")
    RF.roof(r, W, D, form="yosemune", fam="sangawara", eave_y=F + keta)
    h.merge(r)
    return h.transformed(0.0, (0.0, grade, 0.0))


def compound_corner():
    """A walled compound corner with a gate: plastered tsuiji (tile cap) along two sides, one corner, a roofed
    kabuki-mon in the second run, a dobei with a wicket and a namako lower wall continuing past the corner."""
    from jpparts import sitewall as W
    p = Part("k3_compound_corner", "", "test")
    p.merge(W.run_wall([(0.0, 0.0), (0.0, 5 * KEN), (6 * KEN, 5 * KEN)], "tsuiji",
                       gates=[(1, 2 * KEN, "kabuki_roofed", 1.5 * KEN)], finish="plaster", cap="tile", name="tsuiji"))
    # an inner board fence (itabei) with a wicket door, dividing the yard
    p.merge(W.run_wall([(6 * KEN, 3 * KEN), (2 * KEN, 3 * KEN)], "itabei", gates=[(0, KEN, "wicket", KEN)],
                       name="itabei"))
    lines = [((0.0, 0.0), (0.0, 5 * KEN)), ((0.0, 5 * KEN), (6 * KEN, 5 * KEN)), ((6 * KEN, 3 * KEN), (2 * KEN, 3 * KEN))]
    gaps = [((2 * KEN + 0.10, 5 * KEN), (3.5 * KEN - 0.10, 5 * KEN)), ((4 * KEN + 0.32, 3 * KEN), (5 * KEN - 0.32, 3 * KEN))]
    return p, {"budget": "large", "floors": [], "lines": lines, "gaps": gaps, "walk": [], "kind": "wall"}


def slope_fences():
    """A clipped hedge and a yotsume bamboo fence climbing a slope in 0.30 m terrain steps (step pieces between
    level modules), side by side."""
    from jpparts import sitewall as W
    p = Part("k3_slope_fences", "", "test")
    lines, steps = [], []
    for z, kind, kw in ((0.0, "ikegaki", {"size": "low"}), (-2.0, "yotsume", {}), (-4.0, "kenninji", {})):
        y = 0.0
        x = 0.0
        seq = [("m", KEN, ("end", "seam")), ("s", KEN), ("m", KEN, ("seam", "seam")), ("s", KEN),
               ("m", KEN, ("seam", "end"))]
        for it in seq:
            if it[0] == "m":
                q = W.wall(kind, it[1], it[2], pid="%s_%d" % (kind, int(x * 100)), **kw)
                p.merge(q.transformed(0.0, (x, y, z)))
                lines.append(((x, z), (x + it[1], z), y))
            else:
                q = W.step(kind, it[1], 0.30, pid="%s_st%d" % (kind, int(x * 100)), **kw)
                p.merge(q.transformed(0.0, (x, y, z)))
                lines.append(((x, z), (x + it[1] / 2, z), y))
                lines.append(((x + it[1] / 2, z), (x + it[1], z), y + 0.30))
                steps.append((x + it[1] / 2, z, y, y + 0.30))
                y += 0.30
            x += it[1]
    return p, {"budget": "standard", "floors": [], "lines": [(a, b) for a, b, _ in lines], "line_y": lines,
               "steps": steps, "gaps": [], "walk": [], "kind": "fence"}


def corridor_court():
    """Two small stand-in halls (hall B on ground 0.455 higher) linked by a covered corridor that runs round a
    courtyard: out of hall A's east wall, east, north (with a covered stair: the level change), west into hall B's
    east wall; tile corridor roof, open rail on the court side, enclosed (plaster + renji) on the outer side."""
    from jpparts import roka as R
    p = Part("k3_corridor_court", "", "test")
    F = 0.45
    p.merge(_hall("hallA", 3 * KEN, 2 * KEN, F, 3.70, door_z=-KEN).transformed(0.0, (-3 * KEN, 0.0, KEN)))
    p.merge(_hall("hallB", 3 * KEN, 2 * KEN, F, 3.70, door_z=-KEN, grade=0.455).transformed(0.0, (-3 * KEN, 0.0,
                                                                                                  6 * KEN)))
    path = [(0.0, 0.0), (4 * KEN, 0.0), (4 * KEN, 5 * KEN), (0.0, 5 * KEN)]
    run = R.run_roka(path, ("enclosed", "open"), "sangawara", stairs=[(1, 2 * KEN, 2 * KEN, 0.455)],
                     connect=(True, True), name="court")
    p.merge(run)
    fit = R.connector_fit(F + 3.70 - 0.45 * 0.90, F, "sangawara")
    walk = [(-1.0, 0.0)] + path + [(-1.0, 5 * KEN)]
    # one p3d per real object: the two halls and the corridor are separate map objects (one MLOD of all three is
    # over the engine's vertex limit: binarize "Too many vertices")
    split = [("roka", lambda src: not src.startswith("hall")), ("halls", lambda src: src.startswith("hall"))]
    return p, {"budget": "large", "floors": [], "lines": [], "gaps": [], "walk": walk, "y0": F, "kind": "corridor",
               "connector_fit": fit, "per_ken": (4 + 5 + 4) * 1.0, "split": split}


def kairo_segment():
    """A kairo segment: a cloister turning a corner round a court (inner side open, outer side plastered with
    renji windows), curved (sori) hongawara roof, gable ends."""
    from jpparts import roka as R
    path = [(0.0, 0.0), (4 * KEN, 0.0), (4 * KEN, 3 * KEN)]
    p = R.run_roka(path, ("enclosed", "open"), "hongawara", profile="sori", name="k3_kairo_segment")
    return p, {"budget": "large", "floors": [], "lines": [], "gaps": [], "walk": path, "y0": 0.45, "kind": "corridor"}


ASSEMBLIES = {"compound_corner": compound_corner, "slope_fences": slope_fences, "corridor_court": corridor_court,
              "kairo_segment": kairo_segment}


# ------------------------------------------------------------------------------------------------ checks
def mlod_checks(lods, budget, own=None, per_ken=None):
    res = []
    L = {mlod.lod_name(l.resolution): l for l in lods}
    need = ("Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "View Geometry", "Fire Geometry", "Memory")
    res.append(("C5 LODs (vanilla house set)", all(k in L for k in need),
                ", ".join("%s %d" % (k, len(v.faces)) for k, v in L.items())))
    got = tuple(len(L["Resolution %d" % k].faces) for k in (1, 2, 3))
    bud = BUDGETS[budget]
    if per_ken:
        # stand-in halls are not shipped: judge the corridor alone by its run (K3_NOTES §5: <= 1,500 R1 per ken)
        rate = own / per_ken
        res.append(("C5 corridor faces per ken of run <= 1,500 (K3_NOTES §5; stand-in halls excluded)",
                    rate <= 1500, "corridor %d R1 faces over %.1f ken = %.0f per ken; whole proof %d / %d / %d" % (
                        own, per_ken, rate, got[0], got[1], got[2])))
    else:
        over = max(g / m for g, m in zip(got, bud))
        res.append(("C5 face budget (%s: %d / %d / %d; +50 %% guidance)" % ((budget,) + bud), over <= 1.5,
                    "%d / %d / %d (%.0f %% of the class)" % (got + (over * 100,))))
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
            for q in (tex, mat):
                if q and not q.lower().startswith(checks.ALLOWED_VANILLA) and not (
                        q.lower().startswith("jp\\common\\materials\\") and os.path.isfile(os.path.join(DEV, "src", q))):
                    badm.add(q)
    res.append(("C2 library materials only", not badm, "all library / vanilla" if not badm else str(sorted(badm)[:3])))
    return res, L


def _inside(c, x, y, z, pad=0.0):
    return all(n[0] * x + n[1] * y + n[2] * z >= d - pad for n, d in c["planes"])


def wall_checks(L, ctx):
    """KW1 the wall line is closed (Geometry at 0.3 / 1.0 / 1.6 m over grade every 0.1 m, except at gates); KW2 at
    every terrain step Geometry fills the step from the lower grade up (no slot under the raised half)."""
    g = checks.components(L["Geometry"])
    res = []
    miss, n = [], 0
    for item in ctx.get("line_y") or [(a, b, 0.0) for a, b in ctx["lines"]]:
        a, b, y0 = item
        Ln = math.dist(a, b)
        k = int(Ln / 0.1)
        for i in range(1, k):
            x = a[0] + (b[0] - a[0]) * i / k
            z = a[1] + (b[1] - a[1]) * i / k
            if any(min(p[0], q[0]) - 1e-6 <= x <= max(p[0], q[0]) + 1e-6 and min(p[1], q[1]) - 1e-6 <= z <=
                   max(p[1], q[1]) + 1e-6 for p, q in ctx["gaps"]):
                continue
            for hy in ((0.3, 0.7) if ctx["kind"] == "fence" else (0.3, 1.0, 1.6)):
                n += 1
                if not any(_inside(c, x, y0 + hy, z, 0.002) for c in g):
                    miss.append((round(x, 2), round(y0 + hy, 2), round(z, 2)))
    res.append(("KW1 wall / fence line closed in Geometry (gates excepted)", not miss,
                "%d/%d samples inside a Geometry component%s" % (n - len(miss), n, "; gaps at %s" % miss[:4] if miss
                                                                  else "")))
    if ctx.get("steps"):
        bad = []
        for (x, z, ylo, yhi) in ctx["steps"]:
            for dx in (-0.15, 0.15):
                for hy in (ylo + 0.10, (ylo + yhi) / 2, yhi + 0.10):
                    if not any(_inside(c, x + dx, hy, z, 0.002) for c in g):
                        bad.append((round(x + dx, 2), round(hy, 2)))
        res.append(("KW2 terrain steps closed (Geometry from the lower grade up on both sides of each step)", not bad,
                    "%d steps, %s" % (len(ctx["steps"]), "no slot" if not bad else "open at %s" % bad[:4])))
    return res


def walk_checks(L, ctx):
    """KW3 Roadway continuous along the corridor centreline (from hall to hall), KW4 ramp <= 38 deg, KW5 head room
    >= 2.05 over the walk, KW6 clear width >= 1.00 at 1.0 m over the floor."""
    road = L["Roadway"]
    g = checks.components(L["Geometry"])
    pts = []
    path = ctx["walk"]
    for a, b in zip(path[:-1], path[1:]):
        Ln = math.dist(a, b)
        k = max(1, int(Ln / 0.05))
        for i in range(k):
            pts.append((a[0] + (b[0] - a[0]) * i / k, a[1] + (b[1] - a[1]) * i / k, (b[0] - a[0]) / Ln,
                        (b[1] - a[1]) / Ln))
    pts.append((path[-1][0], path[-1][1], 0.0, 0.0))
    y = ctx["y0"]
    gaps, jumps, steep, heads, widths = [], 0, 0.0, [], []
    prev = None
    for i, (x, z, ux, uz) in enumerate(pts):
        hs = [h_ for h_, _ in BC.road_heights(road, x, z) if h_ <= y + 0.45]
        if not hs:
            gaps.append((round(x, 2), round(z, 2)))
            continue
        h_ = max(hs)
        if prev is not None:
            d = math.dist(prev[:2], (x, z))
            if abs(h_ - prev[2]) > 0.06:
                jumps += 1
            if d > 1e-6:
                steep = max(steep, math.degrees(math.atan(abs(h_ - prev[2]) / d)))
        prev = (x, z, h_)
        y = h_
        if i % 4 == 0:
            low = 99.0
            for c in g:
                r = checks.ray_y(c, x, z)
                if r and r[0] > h_ + 0.10:
                    low = min(low, r[0] - h_)
            heads.append(low)
        if i % 10 == 0 and (ux or uz):
            px, pz = -uz, ux
            wsum = 0.0
            for sg in (1.0, -1.0):
                t = 0.0
                while t < 3.0 and not any(_inside(c, x + px * sg * t, h_ + 1.0, z + pz * sg * t, 0.0) for c in g):
                    t += 0.01
                wsum += t
            widths.append(wsum)
    res = [("KW3 Roadway continuous along the walk (hall -> corridor -> hall)", not gaps and not jumps,
            "%d samples, %d without Roadway%s, %d height jumps > 6 cm" % (len(pts), len(gaps),
                                                                            (" e.g. %s" % gaps[:3]) if gaps else "",
                                                                            jumps)),
           ("KW4 walk slope <= 38 deg (stairs as ramps)", steep <= 38.0 + 1e-6, "steepest %.1f deg" % steep),
           ("KW5 head room >= 2.05 over the walk", min(heads) >= 2.05 - 1e-3,
            "lowest %.2f m over %d samples" % (min(heads), len(heads))),
           ("KW6 clear width >= 1.00 at 1.0 m over the floor", min(widths) >= 1.00 - 1e-3,
            "narrowest %.2f m over %d samples" % (min(widths), len(widths)))]
    if ctx.get("connector_fit"):
        fits, ridge, margin = ctx["connector_fit"]
        res.append(("KW7 corridor ridge clears the host eave (connector_fit)", fits,
                    "ridge top %.2f m, host soffit margin %.2f m" % (ridge, margin)))
    return res


def roadway_on_geo(L):
    gcomps = checks.components(L["Geometry"])
    smp = checks.roadway_samples(L["Roadway"]) if "Roadway" in L else []
    off = 0
    for x, y, z, tex in smp:
        tops = [r[1] for c in gcomps if not c["door"] for r in [checks.ray_y(c, x, z)] if r and r[1] <= y + 0.05]
        if not tops or abs(max(tops) - y) > 0.03:
            off += 1
    return [("C7 Roadway on Geometry (+-3 cm)", off == 0, "%d/%d samples on a Geometry top" % (len(smp) - off,
                                                                                             len(smp)))]


def binarize(names):
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\parts\_test_k3"):
        return {n: (False, r"P:\DZ or P:\JP\parts\_test_k3 missing") for n in names}
    out = os.path.join(OUT, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\parts", "-binpath=P:\\bin", "P:\\JP\\parts\\_test_k3", out, "*.p3d"]
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
            res[n] = (False, "no ODOL (see data/parts_test/k3/binarize.log)")
    return res


def main(argv):
    want = [x for x in argv if not x.startswith("--") and x in ASSEMBLIES] or list(ASSEMBLIES)
    allres = {}
    # only the proofs in the binarize folder (the look-cases are written elsewhere)
    os.makedirs(SRC, exist_ok=True)
    for f in os.listdir(SRC):
        if f.endswith(".p3d") and not f.startswith("k3_"):
            os.remove(os.path.join(SRC, f))
    for nm in want:
        a, ctx = ASSEMBLIES[nm]()
        a.memory.setdefault("k3_origin", [(0.0, 0.0, 0.0)])
        own = sum(len(s.faces) for s in a.solids if 1 in s.vis and not str(getattr(s, "src", "")).startswith("hall"))
        zlog = []
        ZF.resolve(a, log=zlog)
        path = os.path.join(SRC, "k3_" + nm + ".p3d")
        bins = ["k3_" + nm]
        if ctx.get("split"):
            # the whole assembly is checked from a copy outside the binarize folder; its objects are binarized
            path = os.path.join(OUT, "mlod", "k3_" + nm + ".p3d")
            bins = []
            for suf, keep in ctx["split"]:
                q = Part("k3_%s_%s" % (nm, suf), "", "test")
                q.solids = [s_ for s_ in a.solids if keep(str(getattr(s_, "src", "")))]
                # Roadway by object: the halls' floors lie west of x 0.09 (their wall faces), the corridor's east of it
                q.roadway = [r_ for r_ in a.roadway if (min(p_[0] for p_ in r_[0]) > 0.0) == (suf == "roka")]
                q.memory = {"k3_origin": [(0.0, 0.0, 0.0)]}
                q.write(os.path.join(SRC, "k3_%s_%s.p3d" % (nm, suf)), geo_props=GEO_PROPS, mass=40000.0)
                bins.append("k3_%s_%s" % (nm, suf))
        a.write(path, geo_props=GEO_PROPS, mass=40000.0)
        lods = mlod.read_mlod(path)
        res, L = mlod_checks(lods, ctx["budget"], own if ctx.get("per_ken") else None, ctx.get("per_ken"))
        if "Roadway" in L:
            res += roadway_on_geo(L)
        if ctx["lines"]:
            res += wall_checks(L, ctx)
        if ctx["walk"]:
            res += walk_checks(L, ctx)
        g3 = []
        if "Roadway" not in L:
            # run_g3 reads the Roadway for C10's floor heights: a wall-only assembly stands on grade (an empty LOD)
            L["Roadway"] = mlod.Lod(mlod.LOD_ROADWAY)
        BC.run_g3(a, L, ctx["floors"], lambda c, o, d: g3.append((c, bool(o), d)))
        res += g3
        allres["k3_" + nm] = {"faces": {mlod.lod_name(l.resolution): len(l.faces) for l in lods}, "checks": res,
                              "zfight_resolved": zlog, "bins": bins}
    if "--no-binarize" not in argv:
        bz = binarize([b for nm in allres for b in allres[nm]["bins"]])
        for nm in allres:
            for b in allres[nm]["bins"]:
                allres[nm]["checks"].append(("Binarize (cwd P:\\) -> ODOL: %s" % b, bz[b][0], bz[b][1]))
    nfail = 0
    for nm, r in allres.items():
        print("== %s  %s" % (nm, r["faces"]))
        for c, o, dt in r["checks"]:
            nfail += 0 if o else 1
            if not o or "-v" in argv:
                print("  %-4s %-72s %s" % ("OK" if o else "FAIL", c[:72], str(dt)[:300]))
        print("  %d/%d pass" % (sum(1 for c in r["checks"] if c[1]), len(r["checks"])))
    jp = os.path.join(DEV, "parts", "k3_assembly_checks.json")
    prev = json.load(open(jp, encoding="utf-8")) if os.path.isfile(jp) else {}
    for nm, r in allres.items():
        prev[nm] = {"faces": r["faces"], "zfight_resolved": r["zfight_resolved"],
                    "checks": [{"check": c, "ok": bool(o), "detail": str(dt)} for c, o, dt in r["checks"]]}
    wb(jp, json.dumps(prev, indent=1))
    print("%d assemblies, %d failures" % (len(allres), nfail))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
