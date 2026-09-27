"""placecheck: find floating and sunken objects offline, before Stephen loads the game.

USAGE (from japan_dev\\):
  python tools\\placecheck\\check.py island [--fix] [--all] [--no-cache] [--out DIR] [--rules FILE]
                                            [--wrp FILE] [--placements GLOB] [--spawns GLOB]
      Checks the test island: every object baked into the source world
      src\\JP\\worlds\\testisland\\world\\japantestisland.wrp (T's trees, rocks, road, house, pond), the rows of
      test\\placements\\*.csv (recomputed from the CSV + heightmap, so edits show before T rebuilds) and every
      object of test\\spawns\\*.json (the runtime object spawner). Writes to data\\placecheck\\island\\:
        failures.csv  one row per failure: source, row, class, p3d, category, x y z, yaw, problem, float_m,
                      sink_m, embed_m, side (model side + compass), host, fix_dy, fix_pitch, fix_roll, fixable, note
        summary.txt   counts per category, every failure, and every drop-in object (placements + spawns) with its
                      numbers even when it passes
      --all          also list passing objects in failures.csv (as problem "ok")
      --fix          trivial cases only (category plant/prop, a pure y shift fixes it, source is a CSV or spawns
                     JSON): writes corrected COPIES to data\\placecheck\\island\\fix\\<same relative path> plus
                     fix\\fix.diff, and prints every change. Nothing is written in place; review the diff, then copy.
  python tools\\placecheck\\check.py profile <p3d> [<p3d> ...]
      Prints a model's grounding profile (bbox, bc, MLOD origin, LODs, contact points, memory points, category).
  python tools\\placecheck\\check.py bench [--n 3000000] [--size 12800] [--grid 4096]
      Synthetic map-scale benchmark: full pass, no-change rerun, then an incremental rerun after moving 1% of the
      objects and raising 16 terrain tiles.

WHAT IS CHECKED (rules and tolerances live in tools\\placecheck\\rules.json; categories come from overrides, then
class/p3d naming, then the ODOL "class" property, then size):
  plant     base rim (lowest point in 12 directions round the stem) >= min_sink under the soil everywhere;
            terrain at the stem <= max_embed above the model's ground line (MLOD origin)
  rock      its lowest band embedded all round (>= min_sink)
  building  footprint gap <= gap_tol at every sampled edge/corner point; terrain above the model's ground line
            (its MLOD origin) <= embed_max. Reports which side floats and by how much
  prop      bottom within +-tol of its support: terrain, or a host building's Roadway (else Geometry) LOD
  hanging   attach points (memory points named attach/hang/hook..., else the model top) within tol of a host's
            Geometry LOD (vertical-free point-to-mesh distance); no host near = floating in mid-air
  road      Roadway LOD vs terrain; mode "drape" (the engine drapes class=road pieces) or "rigid"
Sign convention: gap = object bottom - support; + floats, - sunk. fix_dy is the y change to apply (to y_offset in a
placements CSV, to pos[1] in a spawns JSON). fix_pitch/roll: +pitch = front up, +roll = right side up (the
convention of spikes/T_terrain/tools/wrp8.py; the in-game SetOrientation sign for pitch/roll is unverified).

HOW OBJECT POSITIONS ARE READ: the .wrp and the object spawner both hold the ENGINE position = the binarized (ODOL)
origin, i.e. the model's boundingCenter; a model point (x, y, z) from the ODOL file lands at
pos + x*aside + y*up + z*dir. T proved the .wrp side on Bohemia's utes (30/30 models). For the spawner this assumes
CreateObjectEx(pos) + SetOrientation places the same frame (the only reading consistent with GetPosition()
round-tripping through the DayZ Editor); if it were the MLOD origin instead, objects with a non-zero bc.y would be
off by bc.y (the summary prints bc.y for every spawner object so this can be checked with one look in game).

SPEED: terrain checks are numpy-vectorised (bilinear sampling on the 8WVR grid, row 0 = south); results are cached
per object key (model SHA-1 + rules + matrix + terrain tiles under it + hosts in its cells) in
data\\placecheck\\cache_<scope>.npz, so reruns re-check only what changed. Model profiles are cached by file SHA-1 in
data\\placecheck\\profiles\\.
"""
import csv
import io
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from model import CACHE, ClassIndex, Profiles, load_rules  # noqa: E402
import grounding as G  # noqa: E402
import sources  # noqa: E402

FAILBITS = G.F_FLOAT | G.F_SINK | G.F_EMBED | G.F_NOHOST | G.F_ROAD


def problem_text(k, fl, R, i):
    parts = []
    gmax, gmin = float(R.gmax[i]), float(R.gmin[i])
    if k.cat == "road":
        if fl & G.F_ROAD:
            parts.append("road surface off terrain: %+.2f / %+.2f m (%s)" % (gmax, gmin, k.rule["mode"]))
    elif k.cat == "hanging":
        if fl & G.F_NOHOST:
            parts.append("hangs in mid-air: no host within %.1f m" % k.rule["search"])
        elif fl & G.F_FLOAT:
            parts.append("attach point %.3f m from the host surface" % gmax)
    else:
        if fl & G.F_FLOAT:
            if k.cat in ("plant", "rock"):
                parts.append("base not sunk: highest contact point %+.3f m vs soil (needs <= -%.2f)" % (gmax, k.rule["min_sink"]))
            else:
                parts.append("floats %.3f m" % gmax)
        if fl & G.F_SINK:
            parts.append(("buried: terrain %.3f m above its ground line" % float(R.embed[i])) if k.cat == "plant"
                         else "sunk %.3f m" % -gmin)
        if fl & G.F_EMBED:
            parts.append("terrain %.3f m above its ground line" % float(R.embed[i]))
    return "; ".join(parts) if parts else "ok"


def suggest(T, k, M, fl, R, i):
    """(dy, pitch, roll, fixable, text)."""
    rule, gmax, gmin, emb = k.rule, float(R.gmax[i]), float(R.gmin[i]), float(R.embed[i])
    dy, pitch, roll, fixable, txt = 0.0, 0.0, 0.0, False, ""
    if k.cat == "plant":
        # preferred: the model's ground line (MLOD origin) back on the soil at the stem, as its author intended
        if gmax + emb <= -rule["min_sink"]:
            dy = emb
        elif fl & G.F_FLOAT:
            dy = -(gmax + rule["min_sink"])
        elif fl & G.F_SINK:
            dy = emb - rule["max_embed"]
        fixable = (gmax + dy <= -rule["min_sink"] + 1e-4) and (emb - dy <= rule["max_embed"] + 1e-4)
        if not fixable:
            pitch, roll = G.tilt_fit(T, k, M)
            txt = "a y shift alone cannot satisfy both sides (slope wider than the base allows)"
    elif k.cat == "rock":
        dy = -(gmax + rule["min_sink"])
    elif k.cat == "building":
        if fl & G.F_FLOAT:
            dy = -gmax
            if emb - dy > rule["embed_max"]:
                pitch, roll = G.tilt_fit(T, k, M)
                txt = "a y shift alone buries the %s side; level the terrain pad or tilt" % "other"
        elif fl & G.F_EMBED:
            dy = emb - rule["embed_max"]
            if gmax + dy > rule["gap_tol"]:
                pitch, roll = G.tilt_fit(T, k, M)
                txt = "a y shift alone opens a gap; level the terrain pad or tilt"
    elif k.cat == "prop":
        dy = -(gmax + gmin) / 2
        fixable = (gmax - gmin) <= 2 * rule["tol"]
        if not fixable:
            pitch, roll = G.tilt_fit(T, k, M)
            txt = "uneven support: tilt to the surface"
    elif k.cat == "road":
        txt = "rigid (as placed) worst %+.2f m; grade the terrain under the piece" % float(R.aux[i])
    elif k.cat == "hanging":
        txt = "move it onto the host (or add a hook memory point)"
    fixable = fixable and bool(rule.get("fixable"))
    return dy, pitch, roll, fixable, txt


def run_island(args):
    out_dir = opt(args, "--out", os.path.join(CACHE, "island"))
    rules = load_rules(opt(args, "--rules", None))
    profiles = Profiles()
    ci = ClassIndex()
    holder = []
    t0 = time.time()
    O = sources.load_island(holder, profiles, ci, wrp=opt(args, "--wrp", sources.WRP),
                            placements=opt(args, "--placements", None), spawns=opt(args, "--spawns", None))
    T = holder[0]
    t1 = time.time()
    ch = G.Checker(T, rules, profiles, ci, scope="island", use_cache="--no-cache" not in args)
    R = ch.run(O)
    profiles.save()
    kinds = ch.kinds
    fails = (R.flags & FAILBITS) != 0
    os.makedirs(out_dir, exist_ok=True)
    rows, changes, dropin = [], [], []
    yaw, pitch, roll, sc = G.matrix_angles(O.M)
    for i in range(len(O)):
        meta = O.meta[i]
        show = fails[i] or "--all" in args
        if not show and meta["kind"] == "wrp":
            continue
        k = kinds[O.kidx[i]]
        fl = int(R.flags[i])
        dy, pt, rl, fixable, txt = suggest(T, k, O.M[i], fl, R, i) if fails[i] else (0.0, 0.0, 0.0, False, "")
        if fails[i] and fixable and meta["kind"] in ("csv", "spawn"):
            if meta["kind"] == "csv":
                changes.append({"file": meta["row"]["file"], "line": meta["row"]["line"], "dy": round(dy, 3)})
            else:
                changes.append({"file": meta["spawn"]["file"], "index": meta["spawn"]["index"], "dy": round(dy, 3)})
        hname = ""
        if R.host[i] >= 0:
            hk = kinds[O.kidx[R.host[i]]]
            hname = hk.cls or os.path.basename(hk.p3d)
        rec = {"source": O.sources[O.src[i]], "row": int(O.row[i]), "class": k.cls, "p3d": k.p3d, "category": k.cat,
               "x": "%.2f" % O.M[i, 9], "y": "%.3f" % O.M[i, 10], "z": "%.2f" % O.M[i, 11], "yaw": "%.1f" % yaw[i],
               "problem": problem_text(k, fl, R, i) if fails[i] else ("ok" if not fl & (G.F_SKIP | G.F_NOPROFILE)
                                                                       else G.FLAG_TEXT[fl & (G.F_SKIP | G.F_NOPROFILE)]),
               "float_m": "%.3f" % max(float(R.gmax[i]), 0) if np.isfinite(R.gmax[i]) else "",
               "sink_m": "%.3f" % max(-float(R.gmin[i]), 0) if np.isfinite(R.gmin[i]) else "",
               "embed_m": "%.3f" % float(R.embed[i]) if k.cat in ("building", "plant") else "",
               "side": G.side_of(k, O.M[i], int(R.worst[i])) if k.cat in ("plant", "rock", "building", "prop") else "",
               "host": hname, "fix_dy": "%+.3f" % dy if fails[i] and k.cat not in ("road", "hanging") else "", "fix_pitch": "%+.1f" % pt if pt else "",
               "fix_roll": "%+.1f" % rl if rl else "", "fixable": "yes" if (fails[i] and fixable) else "",
               "note": "; ".join(x for x in (txt, meta.get("note", "")) if x)}
        if show:
            rows.append(rec)
        if meta["kind"] != "wrp":
            rec = dict(rec)
            rec["bc_y"] = "%.3f" % k.prof["bc"][1] if k.prof and "bc" in k.prof else "?"
            rec["gmax"], rec["gmin"] = float(R.gmax[i]), float(R.gmin[i])
            dropin.append(rec)
    cols = ["source", "row", "class", "p3d", "category", "x", "y", "z", "yaw", "problem", "float_m", "sink_m", "embed_m",
            "side", "host", "fix_dy", "fix_pitch", "fix_roll", "fixable", "note"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, cols, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    with open(os.path.join(out_dir, "failures.csv"), "wb") as f:
        f.write(buf.getvalue().encode("utf-8"))
    # summary
    L = []
    st = ch.stats
    L.append("placecheck island  (%s)" % time.strftime("%Y-%m-%d %H:%M"))
    L.append("objects %d (checked %d, from cache %d); load %.2f s, check %.2f s" % (
        st["objects"], st["checked"], st["cached"], t1 - t0, st["t_total"]))
    L.append("")
    L.append("%-10s %7s %7s %7s %7s" % ("category", "objects", "ok", "FAIL", "skipped"))
    cats = np.array([kinds[k].cat for k in O.kidx])
    for c in sorted(set(cats)):
        m = cats == c
        nf = int((fails & m).sum())
        ns = int((((R.flags & (G.F_SKIP | G.F_NOPROFILE)) != 0) & m).sum())
        L.append("%-10s %7d %7d %7d %7d" % (c, m.sum(), m.sum() - nf - ns, nf, ns))
    L.append("")
    L.append("FAILURES (%d) - every one with its fix in failures.csv" % int(fails.sum()))
    frows = [r for r in rows if r["problem"] != "ok" and not r["problem"].startswith(("not checked", "no model"))]

    def sev(r):
        """the failing amount: float, or terrain above the ground line (buried), or plain sink"""
        pr = r["problem"]
        if "not sunk" in pr or "floats" in pr or "attach" in pr or r["category"] == "road":
            return float(r["float_m"] or 0)
        if "ground line" in pr:
            return float(r["embed_m"] or 0)
        return float(r["sink_m"] or 0)
    groups = {}
    for r in frows:
        kind = "floats" if ("not sunk" in r["problem"] or "floats" in r["problem"] or "mid-air" in r["problem"]
                            or "attach" in r["problem"]) else ("road" if r["category"] == "road" else "sunk/buried")
        groups.setdefault((os.path.basename(r["p3d"]) or r["class"], r["category"], kind), []).append(sev(r))
    L.append("  by model:  %-32s %-9s %-12s %5s %8s %8s" % ("model", "category", "problem", "n", "median", "max"))
    for key in sorted(groups, key=lambda k: -len(groups[k])):
        v = sorted(groups[key])
        L.append("             %-32s %-9s %-12s %5d %8.3f %8.3f" % (key[0][:32], key[1], key[2], len(v), v[len(v) // 2], v[-1]))
    L.append("  worst 40:")
    for r in sorted(frows, key=sev, reverse=True)[:40]:
        L.append("  %-26s %-9s (%s, %s, %s) %s%s%s%s" % (
            (r["class"] or os.path.basename(r["p3d"]))[:26], r["category"], r["x"], r["y"], r["z"], r["problem"],
            ", side " + r["side"] if r["side"] else "", ", fix dy " + r["fix_dy"] if r["fix_dy"] else "",
            (" pitch %s roll %s" % (r["fix_pitch"] or "0", r["fix_roll"] or "0")) if (r["fix_pitch"] or r["fix_roll"]) else ""))
    L.append("")
    L.append("DROP-IN OBJECTS (test/placements + test/spawns), pass or fail. gap = bottom - support at the worst contact")
    L.append("point (+ floats, - sunk); bc_y = the model's boundingCenter.y (the spawner-origin caveat in the docstring).")
    for r in dropin:
        L.append("  %-30s %-9s %-26s (%s, %s, %s) highest %+.3f lowest %+.3f%s bc_y %s -> %s%s" % (
            (r["class"] or os.path.basename(r["p3d"]))[:30], r["category"], r["source"][-26:] + ":" + str(r["row"]),
            r["x"], r["y"], r["z"], r["gmax"] if np.isfinite(r["gmax"]) else float("nan"),
            r["gmin"] if np.isfinite(r["gmin"]) else float("nan"),
            (" embed %s" % r["embed_m"]) if r["embed_m"] else "", r["bc_y"], r["problem"],
            ("  [" + r["note"] + "]") if r["note"] else ""))
    text = "\n".join(L) + "\n"
    with open(os.path.join(out_dir, "summary.txt"), "wb") as f:
        f.write(text.encode("utf-8"))
    print(text)
    print("wrote %s" % os.path.join(out_dir, "failures.csv"))
    if "--fix" in args:
        if not changes:
            print("--fix: nothing trivially fixable")
        else:
            print("--fix: %d change(s), corrected copies only (nothing written in place):" % len(changes))
            diff = sources.write_fixes(changes, os.path.join(out_dir, "fix"))
            print(diff)
    return 0


def run_profile(args):
    rules = load_rules(opt(args, "--rules", None))
    profiles = Profiles()
    from model import categorize
    for p in [a for a in args if not a.startswith("--")]:
        prof = profiles.get(p)
        if not prof:
            print("%s: not found" % p)
            continue
        cat, why = categorize(rules, "", p, prof)
        print("%s  sha1 %s  category %s (%s)" % (p, prof["sha1"][:12], cat, why))
        if "error" in prof:
            print("  ERROR", prof["error"])
            continue
        print("  bbox %s .. %s  bc %s  mlod origin y %.3f  odol class '%s'" % (
            fmt(prof["bmin"]), fmt(prof["bmax"]), fmt(prof["bc"]), prof["mlod_origin"][1], prof["odol_class"]))
        print("  LODs: " + ", ".join("%g(%dv)" % (r, n) for r, n, _ in prof["lods"]))
        for kind in prof.get("contact_kinds", []):
            P = prof["low_" + kind]
            print("  contact %-11s %4d pts, lowest y %.3f" % (kind, len(P), P[:, 1].min()))
        if prof["memory"]:
            print("  memory: " + ", ".join("%s%s" % (n, fmt(v)) for n, v in list(prof["memory"].items())[:12]))
    profiles.save()
    return 0


def fmt(v):
    return "(%.2f %.2f %.2f)" % tuple(v)


def opt(args, name, default):
    if name in args:
        return args[args.index(name) + 1]
    return default


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]
    if cmd == "island":
        return run_island(args)
    if cmd == "profile":
        return run_profile(args)
    if cmd == "bench":
        import bench
        return bench.main(args)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
