"""placecheck inputs and outputs: the baked world (.wrp 8WVR), test/placements/*.csv, test/spawns/*.json, and the
--fix writers (corrected copies, never in place). Shared with tools/editor_bridge.

Conventions (README "Drop-in files", spikes/T_terrain/tools/objects.py):
  * placements CSV: p3d,x,z,yaw_deg,y_offset. The MLOD origin goes to (x, ground + y_offset, z); the engine position
    is that plus the rotated ODOL boundingCenter (bc), because binarize re-centres the model on bc.
  * spawns JSON: {"Objects":[{"name","pos","ypr","scale"}]}. pos is the engine position (ODOL origin), exactly what
    CreateObjectEx + SetOrientation get (scripts/3_game/objectspawner.c).
"""
import csv
import difflib
import glob
import json
import os
import re
import struct

import numpy as np

from grounding import ObjSet, yaw_matrix
from model import DEV, norm_p3d

TEST = os.path.join(DEV, "test")
WRP = os.path.join(DEV, "src", "JP", "worlds", "testisland", "world", "japantestisland.wrp")


def read_8wvr(path):
    d = open(path, "rb").read()
    if d[:4] != b"8WVR":
        raise ValueError("%s is not an 8WVR (source) world" % path)
    lx, ly, tx, ty = struct.unpack_from("<4i", d, 4)
    cs = struct.unpack_from("<f", d, 20)[0]
    off = 24
    elev = np.frombuffer(d, "<f4", tx * ty, off).reshape(ty, tx).copy()
    off += tx * ty * 4 + lx * ly * 2
    nm = struct.unpack_from("<i", d, off)[0]
    off += 4
    for _ in range(nm):
        while True:
            n = struct.unpack_from("<i", d, off)[0]
            off += 4
            if n == 0:
                break
            off += n
    objs = []
    while off < len(d):
        m = struct.unpack_from("<12f", d, off)
        off += 48
        oid, n = struct.unpack_from("<ii", d, off)
        off += 8
        name = d[off:off + n].decode("latin-1")
        off += n
        if name:
            objs.append((m, oid, name))
    world = lx * cs
    return {"elev": elev, "cell": world / tx, "world": world, "objects": objs}


def read_placement_rows(pattern=None):
    rows = []
    for path in sorted(glob.glob(pattern or os.path.join(TEST, "placements", "*.csv"))):
        with open(path, newline="", encoding="utf-8") as f:
            for n, rec in enumerate(csv.reader(f)):
                if not rec or rec[0].strip().startswith("#") or rec[0].strip().lower() == "p3d":
                    continue
                try:
                    yoff = float(rec[4]) if len(rec) > 4 and rec[4].strip() else 0.0
                    rows.append({"file": path, "line": n, "p3d": norm_p3d(rec[0]), "x": float(rec[1]), "z": float(rec[2]),
                                 "yaw": float(rec[3]), "yoff": yoff})
                except (ValueError, IndexError):
                    print("WARNING %s line %d unreadable: %r" % (path, n + 1, rec))
    return rows


def read_spawns(pattern=None):
    out = []
    for path in sorted(glob.glob(pattern or os.path.join(TEST, "spawns", "*.json"))):
        data = json.load(open(path, "rb"))
        for n, o in enumerate(data.get("Objects", [])):
            out.append({"file": path, "index": n, "name": o["name"], "pos": [float(v) for v in o["pos"]],
                        "ypr": [float(v) for v in (o.get("ypr") or [0, 0, 0])],
                        "scale": float(o.get("scale") or 1.0)})
    return out


def placement_matrix(profiles, terrain, r):
    """Engine matrix for a placements row, T's rule: pos = origin + R * bc."""
    prof = profiles.get(r["p3d"])
    bc = np.array(prof["bc"]) if prof and "bc" in prof else np.zeros(3)
    M = yaw_matrix([r["yaw"]])[0]
    gy = float(terrain.sample(np.array([r["x"]]), np.array([r["z"]]))[0])
    origin = np.array([r["x"], gy + r["yoff"], r["z"]])
    pos = origin + bc[0] * M[0:3] + bc[1] * M[3:6] + bc[2] * M[6:9]
    return np.concatenate([M, pos])


def spawn_matrix(s):
    M = yaw_matrix([s["ypr"][0]], [s["ypr"][1]], [s["ypr"][2]], [s["scale"]])[0]
    return np.concatenate([M, s["pos"]])


def rel(path):
    try:
        return os.path.relpath(path, DEV)
    except ValueError:
        return path


def load_island(terrain_holder, profiles, class_index, wrp=WRP, placements=None, spawns=None, log=print):
    """ObjSet for the test island: every baked .wrp object, with rows from test/placements recomputed from the CSV
    (so an edit shows before T rebuilds), plus every runtime spawner object. Also returns per-source detail used by
    --fix and the report (O.meta[i] = dict)."""
    W = read_8wvr(wrp)
    from grounding import Terrain
    T = Terrain(W["elev"], W["cell"])
    terrain_holder.append(T)
    O = ObjSet()
    O.meta = []
    rows = read_placement_rows(placements)
    csv_pos = []
    for r in rows:
        M = placement_matrix(profiles, T, r)
        csv_pos.append(M[9:12])
    used = set()
    wrp_objs = W["objects"]
    wp = np.array([o[0][9:12] for o in wrp_objs]) if wrp_objs else np.zeros((0, 3))
    wnames = [norm_p3d(o[2]).lower() for o in wrp_objs]
    for r, pos in zip(rows, csv_pos):
        cand = [i for i, nm in enumerate(wnames) if nm == r["p3d"].lower() and i not in used
                and np.hypot(*(wp[i][[0, 2]] - pos[[0, 2]])) < 0.5]
        r["in_wrp"] = None
        if cand:
            i = min(cand, key=lambda i: np.hypot(*(wp[i][[0, 2]] - pos[[0, 2]])))
            used.add(i)
            r["in_wrp"] = float(wp[i][1] - pos[1])
    for i, (m, oid, name) in enumerate(wrp_objs):
        if i in used:
            continue
        O.add(norm_p3d(name), "", np.array(m, np.float64), rel(wrp), oid)
        O.meta.append({"kind": "wrp", "id": oid})
    for r in rows:
        M = placement_matrix(profiles, T, r)
        O.add(r["p3d"], "", M, rel(r["file"]), r["line"] + 1)
        note = "not in the built .wrp yet (rerun build_world.py)" if r["in_wrp"] is None else (
            "built .wrp is stale by %+.3f m (rerun build_world.py)" % r["in_wrp"] if abs(r["in_wrp"]) > 0.005 else "")
        O.meta.append({"kind": "csv", "row": r, "note": note})
    for s in read_spawns(spawns):
        p3d = class_index.model(s["name"]) or ""
        O.add(p3d, s["name"], spawn_matrix(s), rel(s["file"]), s["index"])
        O.meta.append({"kind": "spawn", "spawn": s, "note": "" if p3d else "class not found in any config.cpp"})
    O.freeze()
    return O


# ------------------------------------------------------------------------------------------ fix writers
def _num(v, nd):
    s = ("%." + str(nd) + "f") % v
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s if s not in ("-0", "") else "0"


def write_fixes(changes, out_dir, log=print):
    """changes: list of dicts {kind: 'csv'|'spawn', file, line|index, dy}. Writes corrected COPIES under out_dir,
    mirroring the japan_dev-relative path, plus fix.diff. Returns the diff text."""
    by_file = {}
    for c in changes:
        by_file.setdefault(c["file"], []).append(c)
    diffs = []
    for path, cs in sorted(by_file.items()):
        old = open(path, "rb").read().decode("utf-8")
        new = old
        if path.lower().endswith(".csv"):
            lines = old.split("\n")
            for c in cs:
                rec = next(csv.reader([lines[c["line"]]]))
                while len(rec) < 5:
                    rec.append("0")
                rec[4] = _num(float(rec[4] or 0) + c["dy"], 3)
                lines[c["line"]] = ",".join(rec) + ("\r" if lines[c["line"]].endswith("\r") else "")
            new = "\n".join(lines)
        else:
            # replace the y of the N-th "pos" array in place, so formatting and every other byte survive
            rx = re.compile(r'("pos"\s*:\s*\[\s*[-+0-9.eE]+\s*,\s*)([-+0-9.eE]+)')
            ms = list(rx.finditer(old))
            edits = {c["index"]: c["dy"] for c in cs}
            parts, last = [], 0
            for n, m in enumerate(ms):
                if n in edits:
                    parts.append(old[last:m.start(2)])
                    parts.append(_num(float(m.group(2)) + edits[n], 3))
                    last = m.end(2)
            parts.append(old[last:])
            new = "".join(parts)
        r = rel(path)
        out = os.path.join(out_dir, r if not r.startswith("..") and not os.path.isabs(r) else
                           os.path.join("external", os.path.basename(path)))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "wb") as f:
            f.write(new.encode("utf-8"))
        diffs.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + rel(path).replace("\\", "/"),
                                          "b/" + rel(path).replace("\\", "/")))
        log("  fix: %d change(s) -> %s" % (len(cs), out))
    text = "".join(diffs)
    with open(os.path.join(out_dir, "fix.diff"), "wb") as f:
        f.write(text.encode("utf-8"))
    return text
