"""DayZ Editor bridge: our placement files <-> the community DayZ Editor (InclementDab, Workshop 2250764298).

USAGE (from japan_dev\\):
  python tools\\editor_bridge\\bridge.py export [--out DIR] [--no-baked]
      Writes, into the Editor's own folder (Documents\\DayZ\\Editor unless --out):
        japan_island.dze           JSON save the Editor opens with Ctrl+O. EditorObjects = every object of
                                   test\\spawns\\*.json, plus a movable COPY of every test\\placements\\*.csv object
                                   that has a spawnable class (machiya, sakura, bamboo); EditorHiddenObjects hides the
                                   baked originals so the copies can be nudged. --no-baked leaves the placements out.
        japan_island_spawner.json  the same objects in object-spawner format (File > Import > Object Spawner)
      and data\\editor_bridge\\export_map.json (which exported object came from which file/row).
  python tools\\editor_bridge\\bridge.py import <file> [--radius 2.0] [--apply]
      Reads an Editor export and updates our files. Formats: Expansion .map (File > Export > Expansion: the only
      export that also lists hidden map objects, recommended), object-spawner .json, JSON .dze, init.c (SpawnObject
      lines). The Editor's own Ctrl+S save is binary ("EditorBinned") and is NOT readable here: export instead.
      Matching: each of our objects (spawns + placements) takes the nearest Editor object with the same class
      within --radius metres (greedy, nearest pairs first). Moved objects get new pos/ypr (spawns) or new
      x, z, yaw, y_offset (placements: MLOD origin = Editor position minus the rotated boundingCenter, y_offset =
      that minus the terrain height of the source .wrp). Writes corrected COPIES to data\\editor_bridge\\import\\
      <same relative path>, import.diff and import_report.txt; Editor objects that match nothing go to
      new_objects.json (object-spawner format) for review. --apply also writes the changed files in place
      (after printing the diff). Objects of ours that are missing from the export are reported, never deleted.

THE LOOP: start-japan-editor.bat (runs `export` first) -> Open Editor -> JapanTestIsland -> Ctrl+O japan_island ->
fly to the lantern, nudge it -> File > Export > Expansion (.map) -> `bridge.py import <Documents\\DayZ\\Editor\\x.map>`
-> review import.diff -> --apply -> placecheck -> T rebuilds the world if a placements CSV changed.

Conventions: Editor Position = GetPosition() = the engine position (ODOL origin), Orientation = [yaw, pitch, roll]
degrees = exactly the object-spawner pos/ypr (Editor source: EditorObjectData.Create, EditorObjectSpawnerFile).
Placements CSVs have no pitch/roll: a tilted Editor copy is reported and its tilt dropped.
Known gaps: baked objects without a config class (vanilla trees) cannot be exported as movable copies; Editor types
that are raw .p3d paths are matched by p3d but their Position is taken as-is (the Editor stores those minus the
bounding centre in its binary save; unverified for exports).
"""
import csv
import difflib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "tools", "placecheck"))
import numpy as np  # noqa: E402
import grounding as G  # noqa: E402
import sources  # noqa: E402
from model import ClassIndex, Profiles, norm_p3d  # noqa: E402

OUT = os.path.join(DEV, "data", "editor_bridge")


def documents_dir():
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
        return os.path.expandvars(winreg.QueryValueEx(k, "Personal")[0])
    except OSError:
        return os.path.join(os.path.expanduser("~"), "Documents")


def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def reverse_classes(ci, p3ds):
    """p3d (lower) -> the best spawnable class using that model."""
    ci.load()
    want = {norm_p3d(p).lower() for p in p3ds}
    found = {}
    for low, (parent, model, name) in ci.classes.items():
        if model and norm_p3d(model).lower() in want:
            found.setdefault(norm_p3d(model).lower(), []).append(name)
    best = {}
    for p, names in found.items():
        names.sort(key=lambda n: (not (n.lower().startswith("land_") or n.lower().startswith("staticobj_")
                                       or n.lower().endswith("_static")), n))
        best[p] = names[0]
    return best


def our_records(profiles, ci, T):
    """Every object we own: spawns (by class) and placements rows (with their class, if any)."""
    recs = []
    for s in sources.read_spawns():
        recs.append({"src": "spawn", "file": s["file"], "index": s["index"], "cls": s["name"], "pos": s["pos"],
                     "ypr": s["ypr"], "scale": s["scale"], "p3d": ci.model(s["name"]) or ""})
    rows = sources.read_placement_rows()
    rev = reverse_classes(ci, [r["p3d"] for r in rows])
    for r in rows:
        M = sources.placement_matrix(profiles, T, r)
        recs.append({"src": "csv", "file": r["file"], "line": r["line"], "row": r, "cls": rev.get(r["p3d"].lower(), ""),
                     "p3d": r["p3d"], "pos": [float(v) for v in M[9:12]], "ypr": [r["yaw"], 0.0, 0.0], "scale": 1.0})
    return recs


def load_terrain():
    W = sources.read_8wvr(sources.WRP)
    return G.Terrain(W["elev"], W["cell"])


# ------------------------------------------------------------------------------------------ export
def cmd_export(args):
    out = opt(args, "--out", os.path.join(documents_dir(), "DayZ", "Editor"))
    profiles, ci, T = Profiles(), ClassIndex(), load_terrain()
    recs = our_records(profiles, ci, T)
    objs, hidden, mapping, skipped = [], [], [], []
    for r in recs:
        if r["src"] == "csv":
            if "--no-baked" in args:
                continue
            if not r["cls"]:
                skipped.append("%s (no spawnable class uses this model)" % r["p3d"])
                continue
            hidden.append({"Type": r["cls"], "ModelName": os.path.splitext(os.path.basename(r["p3d"]))[0],
                           "Position": r["pos"], "Flags": 0})
        objs.append({"Type": r["cls"], "DisplayName": r["cls"], "Position": [round(v, 4) for v in r["pos"]],
                     "Orientation": [round(v, 4) for v in r["ypr"]], "Scale": r["scale"], "Flags": 30})
        mapping.append({"src": r["src"], "file": os.path.relpath(r["file"], DEV), "row": r.get("index", r.get("line")),
                        "cls": r["cls"], "pos": r["pos"]})
    dze = {"MapName": "JapanTestIsland", "CameraPosition": [1024.0, 45.0, 960.0],
           "EditorObjects": objs, "EditorHiddenObjects": hidden}
    wb(os.path.join(out, "japan_island.dze"), json.dumps(dze, indent=1))
    spawner = {"Objects": [{"name": o["Type"], "pos": o["Position"], "ypr": o["Orientation"], "scale": o["Scale"],
                            "enableCEPersistency": 0} for o in objs]}
    wb(os.path.join(out, "japan_island_spawner.json"), json.dumps(spawner, indent=1))
    wb(os.path.join(OUT, "export_map.json"), json.dumps(mapping, indent=1))
    profiles.save()
    print("exported %d objects (%d baked placements as movable copies, their originals hidden) to %s"
          % (len(objs), len(hidden), os.path.join(out, "japan_island.dze")))
    for s in skipped:
        print("  not exported: " + s)
    return 0


# ------------------------------------------------------------------------------------------ import
def read_editor_file(path):
    """-> (objects [{type, pos, ypr, scale}], hidden [{type, pos}])"""
    txt = open(path, "rb").read()
    if txt[:64].find(b"EditorBinned") >= 0:
        raise SystemExit("%s is a binary Editor save: use File > Export (Expansion .map recommended)" % path)
    txt = txt.decode("utf-8", "replace")
    objs, hidden = [], []
    ext = os.path.splitext(path)[1].lower()
    vec = lambda s: [float(v) for v in re.split(r"[\s,]+", s.strip().strip("<>[]")) if v]  # noqa: E731
    if ext in (".json", ".dze"):
        d = json.loads(txt)
        for o in d.get("Objects", []):
            objs.append({"type": o["name"], "pos": [float(v) for v in o["pos"]],
                         "ypr": [float(v) for v in o.get("ypr", [0, 0, 0])], "scale": float(o.get("scale") or 1)})
        for o in d.get("EditorObjects", []):
            objs.append({"type": o["Type"], "pos": [float(v) for v in o["Position"]],
                         "ypr": [float(v) for v in o.get("Orientation", [0, 0, 0])], "scale": float(o.get("Scale") or 1)})
        for o in d.get("EditorHiddenObjects", []) or d.get("EditorDeletedObjects", []):
            hidden.append({"type": o.get("Type") or o.get("ModelName", ""), "pos": [float(v) for v in o["Position"]]})
    elif ext == ".map":
        for line in txt.splitlines():
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            f = line.split("|")
            if len(f) < 3:
                continue
            t = f[0]
            dead = t.startswith("-")
            t = t.lstrip("-")
            if not t.lower().endswith(".p3d") and "." in t:
                t = t.split(".")[0]
            rec = {"type": t, "pos": vec(f[1]), "ypr": vec(f[2]), "scale": 1.0}
            (hidden if dead else objs).append(rec)
    else:   # init.c: SpawnObject("Type", "x y z", "y p r", scale)
        for m in re.finditer(r'SpawnObject\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*(?:,\s*([-0-9.eE]+))?', txt):
            objs.append({"type": m.group(1), "pos": vec(m.group(2)), "ypr": vec(m.group(3)),
                         "scale": float(m.group(4) or 1)})
    return objs, hidden


def same_type(rec, t):
    t = t.lower()
    if t.endswith(".p3d") or "\\" in t or "/" in t:
        return norm_p3d(t).lower() == rec["p3d"].lower()
    return rec["cls"].lower() == t


def cmd_import(args):
    files = [a for a in args if not a.startswith("--") and a != opt(args, "--radius", None)]
    if not files:
        print(__doc__)
        return 2
    radius = float(opt(args, "--radius", "2.0"))
    objs, hidden = read_editor_file(files[0])
    profiles, ci, T = Profiles(), ClassIndex(), load_terrain()
    recs = our_records(profiles, ci, T)
    pairs = []
    for ri, r in enumerate(recs):
        for oi, o in enumerate(objs):
            if same_type(r, o["type"]):
                d = math.dist(r["pos"], o["pos"])
                if d <= radius:
                    pairs.append((d, ri, oi))
    pairs.sort()
    r_take, o_take = {}, set()
    for d, ri, oi in pairs:
        if ri in r_take or oi in o_take:
            continue
        r_take[ri] = oi
        o_take.add(oi)
    report, csv_changes, spawn_changes = [], {}, {}
    for ri, r in enumerate(recs):
        tag = "%s:%s" % (os.path.relpath(r["file"], DEV), r.get("index", (r.get("line") or 0) + 1))
        if ri not in r_take:
            if r["src"] == "csv" and not r["cls"]:
                continue                                   # never exported (no class): nothing to compare
            report.append("MISSING  %-28s %-26s not in the export within %.1f m (deleted in the Editor?)"
                          % (r["cls"] or r["p3d"], tag, radius))
            continue
        o = objs[r_take[ri]]
        dp = [o["pos"][k] - r["pos"][k] for k in range(3)]
        dyaw = (o["ypr"][0] - r["ypr"][0] + 180) % 360 - 180
        if max(abs(v) for v in dp) < 0.001 and abs(dyaw) < 0.01 and max(abs(v) for v in o["ypr"][1:]) < 0.01 \
                and abs(o["scale"] - r["scale"]) < 1e-4:
            continue
        report.append("MOVED    %-28s %-26s d(x,y,z) = (%+.3f, %+.3f, %+.3f) m, dyaw %+.2f deg%s" % (
            r["cls"] or r["p3d"], tag, dp[0], dp[1], dp[2], dyaw,
            (", pitch/roll %.2f/%.2f" % tuple(o["ypr"][1:3])) if max(abs(v) for v in o["ypr"][1:]) >= 0.01 else ""))
        if r["src"] == "spawn":
            spawn_changes.setdefault(r["file"], {})[r["index"]] = o
        else:
            if max(abs(v) for v in o["ypr"][1:]) >= 0.01:
                report.append("         placements CSVs have no pitch/roll: the tilt was dropped")
            prof = profiles.get(r["p3d"])
            bc = np.array(prof["bc"]) if prof else np.zeros(3)
            M = G.yaw_matrix([o["ypr"][0]])[0]
            origin = np.array(o["pos"]) - (bc[0] * M[0:3] + bc[1] * M[3:6] + bc[2] * M[6:9])
            g = float(T.sample(np.array([origin[0]]), np.array([origin[2]]))[0])
            csv_changes.setdefault(r["file"], {})[r["line"]] = (origin[0], origin[2], o["ypr"][0] % 360, origin[1] - g)
    new = [objs[i] for i in range(len(objs)) if i not in o_take]
    out = os.path.join(OUT, "import")
    diffs = []
    for path, ch in csv_changes.items():
        old = open(path, "rb").read().decode("utf-8")
        lines = old.split("\n")
        for ln, (x, z, yaw, yoff) in ch.items():
            rec = next(csv.reader([lines[ln]]))
            while len(rec) < 5:
                rec.append("0")
            rec[1:5] = ["%.3f" % x, "%.3f" % z, "%.2f" % yaw, "%.3f" % yoff]
            lines[ln] = ",".join(rec) + ("\r" if lines[ln].endswith("\r") else "")
        diffs += write_copy(path, old, "\n".join(lines), out, "--apply" in args)
    for path, ch in spawn_changes.items():
        old = open(path, "rb").read().decode("utf-8")
        new_txt = patch_spawn_json(old, ch)
        diffs += write_copy(path, old, new_txt, out, "--apply" in args)
    if new:
        wb(os.path.join(out, "new_objects.json"), json.dumps({"Objects": [
            {"name": o["type"], "pos": o["pos"], "ypr": o["ypr"], "scale": o["scale"]} for o in new]}, indent=1))
        report.append("NEW      %d Editor object(s) matched nothing of ours -> %s (review, then merge by hand)"
                      % (len(new), os.path.join(out, "new_objects.json")))
    if hidden:
        report.append("HIDDEN   %d baked map object(s) hidden in the Editor (listed only)" % len(hidden))
    diff = "".join(diffs)
    wb(os.path.join(out, "import.diff"), diff)
    text = "editor import from %s: %d Editor objects, %d hidden, %d of ours\n" % (files[0], len(objs), len(hidden),
                                                                                len(recs))
    text += "\n".join(report) + "\n"
    wb(os.path.join(out, "import_report.txt"), text)
    print(text)
    print(diff if diff else "(no file changes)")
    print("copies + import.diff + import_report.txt in %s%s" % (out, "; APPLIED in place" if "--apply" in args and diff
                                                               else ""))
    profiles.save()
    return 0


def patch_spawn_json(old, changes):
    """Replace pos/ypr/scale of the N-th object in place, keeping every other byte of the file."""
    data = json.loads(old)
    spans = [m.start() for m in re.finditer(r'"name"\s*:', old)] + [len(old)]
    parts, last = [], 0
    for n, o in sorted(changes.items()):
        a, b = spans[n], spans[n + 1]
        seg = old[a:b]
        seg = sub_numbers(seg, "pos", o["pos"])
        seg = sub_numbers(seg, "ypr", o["ypr"])
        if abs(o["scale"] - float(data["Objects"][n].get("scale") or 1)) > 1e-6:
            seg = re.sub(r'("scale"\s*:\s*)[-0-9.eE]+', lambda m: m.group(1) + num(o["scale"]), seg, count=1)
        parts.append(old[last:a])
        parts.append(seg)
        last = b
    parts.append(old[last:])
    return "".join(parts)


def sub_numbers(seg, key, values):
    """Inside the first "key": [ ... ] of seg, replace only the numbers whose value changed (keeps layout)."""
    m = re.search(r'"%s"\s*:\s*\[([^\]]*)\]' % key, seg)
    if not m:
        return seg
    body = m.group(1)
    toks = list(re.finditer(r"[-+0-9.eE]+", body))
    out, last = [], 0
    for i, t in enumerate(toks):
        out.append(body[last:t.start()])
        v = values[i] if i < len(values) else float(t.group())
        out.append(t.group() if abs(float(t.group()) - v) < 1e-6 else num(v))
        last = t.end()
    out.append(body[last:])
    return seg[:m.start(1)] + "".join(out) + seg[m.end(1):]


def num(v):
    s = "%.4f" % v
    s = s.rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def write_copy(path, old, new, out, apply):
    rel = os.path.relpath(path, DEV)
    wb(os.path.join(out, rel), new)
    if apply:
        wb(path, new)
    return list(difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + rel.replace("\\", "/"),
                                     "b/" + rel.replace("\\", "/")))


def opt(args, name, default):
    return args[args.index(name) + 1] if name in args else default


def main(argv):
    if not argv or argv[0] not in ("export", "import"):
        print(__doc__)
        return 2
    return cmd_export(argv[1:]) if argv[0] == "export" else cmd_import(argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
