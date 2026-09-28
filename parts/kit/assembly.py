#!/usr/bin/env python3
r"""Test assembly: proves the connectors, the MLOD part sources and the binarize path. Not a building for the island.

  python assembly.py [--no-binarize]

Main frame (2 x 2 ken, x 0..3.64, z 0 (front) .. -3.64), all on the ken grid:
  - dodai on dressed stones under all four walls; posts at every ken node (+ one half-ken post for the window)
  - front: itado door in bay 1 parking over bay 2 (plain shinkabe, grime decal); stone step with the hidden ramp
  - left: koshi lattice over a 0.45 wainscot in bay 1, battened board wall in bay 2
  - back: renji window in a half-ken bay + shinkabe; right: arakabe shinkabe with a 0.90 koshi-ita
  - keta on the eave walls, tile gables on the gable walls, sangawara kirizuma roof from the generator; doma floor
Beside it, one roof corner per remaining family on its own post frame (2 x 1 ken each): ishioki, kokera, thatch.

Two paths are built and compared: (A) everything from the kit in memory; (B) recipes in memory + the FIXED parts
(door, window, lattice, posts, step) merged from their MLOD files in src/JP/parts (the way buildings get them).
(B) is written to src/JP/parts/_test/jp_p_test_assembly.p3d with model.cfg, binarized (cwd P:\) to data/parts_test,
and checked (C7 on the assembled model: sweep, clear width with the real posts, roadway, components; ODOL LODs).
"""
import copy
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, checks, registry, walls, frame, found, openings, roofs as R, trim, mlod  # noqa: E402
from jpparts.core import Part, KEN, HALF, POST, EAVE_Y, WALL_H, box  # noqa: E402

DEV = core.DEV
TEST_SRC = os.path.join(DEV, "src", "JP", "parts", "_test")
TEST_OUT = os.path.join(DEV, "data", "parts_test")
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
REG = {p + v: (p, v, fn) for p, v, fn in registry.ALL}
L = 2 * KEN

# wall frames: (yaw, origin): part +x runs along the wall, part +z faces out (see core.rot_y)
FRONT = (0.0, (0.0, 0.0, 0.0))
LEFT = (90.0, (0.0, 0.0, -L))
BACK = (180.0, (L, 0.0, -L))
RIGHT = (-90.0, (L, 0.0, 0.0))

# fixed parts: (registry name, frame, local offset along the wall)
FIXED = [
    ("jp_p_open_itado_battened", FRONT, 0.0),
    ("jp_p_open_koshi_kyo", LEFT, 0.0),
    ("jp_p_open_renji_wood", BACK, 0.0),
]


def build_part(name):
    p, v, fn = REG[name]
    return fn(v)


def place(fr, dx=0.0):
    yaw, o = fr
    off = core.rot_y((dx, 0.0, 0.0), yaw)
    return yaw, (o[0] + off[0], o[1], o[2] + off[2])


def recipes(skip_fixed=True):
    """Everything that is a recipe (generated for this footprint)."""
    a = Part("jp_p_test_assembly", "", "_test", tiers=[2], used_for="connector proof")
    a.wear = "_w1"
    # ---- foundations: dodai on dressed stones, all 4 walls
    for fr in (FRONT, LEFT, BACK, RIGHT):
        w = Part("w", "", "")
        found.dodai_stones(w, 0.0, L, dressed=True, seed=int(fr[0]))
        a.merge(w.transformed(*place(fr)))
    # ---- walls
    wf = Part("front_wall", "", "")
    walls.wall_run(wf, "shinkabe", 0.0, L, finish="nakanuri", openings=[(POST / 2, KEN - POST / 2, 0.0, 2.0)],
                   internal_posts=False)
    trim.grime_band(wf, KEN + POST / 2, L - POST / 2, 0.0375)
    a.merge(wf.transformed(*place(FRONT)))
    wl = Part("left_wall", "", "")
    walls.wall_run(wl, "shinkabe", 0.0, KEN, finish="nakanuri", openings=[(POST / 2, KEN - POST / 2, 0.45, 2.0)])
    walls.koshiita(wl, POST / 2, KEN - POST / 2, 0.45 - 0.06, 0.0375)
    walls.wall_run(wl, "board_vertical", KEN, L, internal_posts=False)
    a.merge(wl.transformed(*place(LEFT)))
    wb_ = Part("back_wall", "", "")
    walls.wall_run(wb_, "shinkabe", 0.0, HALF, finish="nakanuri", openings=[(POST / 2, HALF - POST / 2, 0.85, 1.70)])
    walls.wall_run(wb_, "shinkabe", HALF, KEN, finish="nakanuri")
    walls.wall_run(wb_, "shinkabe", KEN, L, finish="nakanuri")
    a.merge(wb_.transformed(*place(BACK)))
    wr = Part("right_wall", "", "")
    walls.wall_run(wr, "shinkabe", 0.0, L, finish="arakabe", internal_posts=False)
    walls.koshiita(wr, POST / 2, KEN - POST / 2, 0.90, 0.0375)
    walls.koshiita(wr, KEN + POST / 2, L - POST / 2, 0.90, 0.0375)
    a.merge(wr.transformed(*place(RIGHT)))
    # ---- keta on the eave walls, tile gables on the gable walls
    for fr in (FRONT, BACK):
        k = Part("keta", "", "")
        frame.keta(k, -0.30, L + 0.30)
        a.merge(k.transformed(*place(fr)))
    for fr in (LEFT, RIGHT):
        g = Part("gable", "", "")
        walls.gable(g, L, R.PITCH["sangawara"], EAVE_Y, "_tile")
        a.merge(g.transformed(*place(fr)))
    # ---- roof from the generator
    r = Part("roof", "", "")
    R.roof(r, L, L, "kirizuma", "sangawara")
    a.merge(r)
    # ---- doma floor (walkable), step outside the door
    fl = Part("floor", "", "")
    fl.add(box(POST / 2, L - POST / 2, -0.40, 0.0, -L + POST / 2, -POST / 2, {"top": "wall_arakabe", "default": "stone_cut"},
               vis=(1, 2), geo=True, view=True, fire="dirt", tag="doma"))
    fl.road([(POST / 2, 0.0, -L + POST / 2), (L - POST / 2, 0.0, -L + POST / 2), (L - POST / 2, 0.0, -POST / 2),
             (POST / 2, 0.0, -POST / 2)], "doma")
    a.merge(fl)
    st = Part("step", "", "")
    found.step(st, HALF, "cut", drop=0.27, width=1.30)
    a.merge(st.transformed(0.0, (0.0, 0.0, POST / 2)))
    # ---- the other roof families, one corner each on a 2 x 1 ken post frame
    for i, fam in enumerate(("ishioki", "itabuki", "thatch")):
        x0 = L + 3.0 + i * 6.0
        pv = Part("pav", "", "")
        for (x, z) in ((0, 0), (KEN, 0), (L, 0), (0, -KEN), (KEN, -KEN), (L, -KEN)):
            frame.post(pv, x, z=z, size=0.15 if fam == "thatch" else POST, adzed=(fam == "thatch"))
            found.soseki(pv, x, z, int(x / KEN * 3 + (-z) / KEN) % 8)
        for z in (0.0, -KEN):
            frame.keta(pv, -0.3, L + 0.3, z=z)
        form = "yosemune" if fam == "thatch" else "kirizuma"
        R.roof(pv, L, KEN, form, fam, walkable=(fam != "thatch"))
        a.merge(pv.transformed(0.0, (x0, 0.0, 0.0)))
    # ---- posts (path A: from the kit; path B merges the post MLOD instead)
    posts = [(x, z) for x in (0.0, KEN, L) for z in (0.0, -KEN, -L) if not (x == KEN and z == -KEN)]
    posts.append((L - HALF, -L))                             # half-ken post beside the back window
    return a, posts


def build():
    """Path A: the whole assembly from the kit in memory (used for renders)."""
    a, posts = recipes()
    for (x, z) in posts:
        pp = build_part("jp_p_frame_post_planed")
        a.merge(pp.transformed(0.0, (x, 0.0, z)))
    for name, fr, dx in FIXED:
        a.merge(build_part(name).transformed(*place(fr, dx)))
    a.merge(build_part("jp_p_trim_grime_post").transformed(0.0, (KEN, 0.0, 0.0)))
    return a


# ------------------------------------------------------------------------------------------------ MLOD merge (path B)
def merge_mlod(dst, src_path, yaw, t, bone_base):
    """Merge every LOD of an MLOD part file into the dst LOD list (same resolutions), placed by yaw + t.
    ComponentNN selections are renumbered, doorsN -> doors(N + bone_base). Returns the number of bones merged."""
    src = mlod.read_mlod(src_path)
    bones = set()
    for sl in src:
        dl = mlod.find_lod(dst, sl.resolution)
        if dl is None:
            dl = mlod.Lod(sl.resolution)
            dst.append(dl)
        p0, n0, f0 = len(dl.points), len(dl.normals), len(dl.faces)
        for p, fl in zip(sl.points, sl.point_flags):
            q = core.rot_y(p, yaw)
            dl.add_point((q[0] + t[0], q[1] + t[1], q[2] + t[2]), fl)
        for n in sl.normals:
            dl.add_normal(core.rot_y(n, yaw))
        for verts, flags, tex, mat in sl.faces:
            dl.add_face([(pi + p0, ni + n0, u, v) for pi, ni, u, v in verts], tex, mat, flags)
        ncomp = sum(1 for s in dl.selections if s.startswith("Component"))
        for name, (pw, fs) in sl.selections.items():
            m = re.match(r"^doors(\d+)(.*)$", name)
            if name.startswith("Component"):
                ncomp += 1
                nn = "Component%02d" % ncomp
            elif m:
                nn = "doors%d%s" % (int(m.group(1)) + bone_base, m.group(2))
                bones.add(int(m.group(1)))
            else:
                continue
            dl.select(nn, {pi + p0: w for pi, w in pw.items()}, {fi + f0 for fi in fs})
    return len(bones)


def order_lods(lods):
    key = {1.0: 0, 2.0: 1, 3.0: 2, mlod.LOD_GEOMETRY: 3, mlod.LOD_MEMORY: 4, mlod.LOD_ROADWAY: 5,
           mlod.LOD_VIEW_GEOMETRY: 6, mlod.LOD_FIRE_GEOMETRY: 7}
    return sorted(lods, key=lambda l: next((v for k, v in key.items() if mlod.same_res(l.resolution, k)), 99))


def door_records(name, yaw, t, base):
    """Door records of a placed part from its sidecar (bones renumbered, axes from the placed Memory LOD)."""
    p, v, fn = REG[name]
    part = fn(v)
    out = []
    for d in part.doors:
        nd = copy.copy(d)
        nd.anims = []
        for a in d.anims:
            k = int(a["bone"][5:]) + base
            ax = [core.add(core.rot_y(q, yaw), t) for q in a["axis"]]
            nd.anims.append(dict(a, bone="doors%d" % k, axis=ax))
        nd.opening = d.opening
        out.append(nd)
    return out


def modelcfg(name, doors):
    bones = ",\n".join('\t\t\t"%s",""' % a["bone"] for d in doors for a in d.anims)
    anims = ""
    for i, d in enumerate(doors):
        src = "Doors%d" % (i + 1)
        for j, a in enumerate(d.anims):
            cls = src if j == 0 else "%s_%d" % (src, j + 1)
            if a["type"] == "translation":
                anims += ("\t\t\tclass %s\n\t\t\t{\n\t\t\t\ttype=\"translation\";\n\t\t\t\tsource=\"%s\";\n"
                          "\t\t\t\tselection=\"%s\";\n\t\t\t\taxis=\"%s_axis\";\n\t\t\t\tmemory=1;\n\t\t\t\tminValue=0;\n"
                          "\t\t\t\tmaxValue=1;\n\t\t\t\toffset0=0;\n\t\t\t\toffset1=%.4f;\n\t\t\t};\n"
                          % (cls, src, a["bone"], a["bone"], a["amount"]))
            else:
                anims += ("\t\t\tclass %s\n\t\t\t{\n\t\t\t\ttype=\"rotation\";\n\t\t\t\tsource=\"%s\";\n"
                          "\t\t\t\tselection=\"%s\";\n\t\t\t\taxis=\"%s_axis\";\n\t\t\t\tmemory=1;\n\t\t\t\tminValue=0;\n"
                          "\t\t\t\tmaxValue=1;\n\t\t\t\tangle0=0;\n\t\t\t\tangle1=%.5f;\n\t\t\t};\n"
                          % (cls, src, a["bone"], a["bone"], a["amount"]))
    return ("class CfgSkeletons\n{\n\tclass Default\n\t{\n\t\tisDiscrete=1;\n\t\tskeletonInherit=\"\";\n"
            "\t\tskeletonBones[]={};\n\t};\n\tclass %s_skeleton: Default\n\t{\n\t\tskeletonInherit=\"Default\";\n"
            "\t\tskeletonBones[]=\n\t\t{\n%s\n\t\t};\n\t};\n};\nclass CfgModels\n{\n\tclass Default\n\t{\n"
            "\t\tsectionsInherit=\"\";\n\t\tsections[]={};\n\t\tskeletonName=\"\";\n\t};\n\tclass %s: Default\n\t{\n"
            "\t\tskeletonName=\"%s_skeleton\";\n\t\tclass Animations\n\t\t{\n%s\t\t};\n\t};\n};\n"
            % (name, bones, name, name, anims))


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def path_b():
    a, posts = recipes()
    lods = a.lods()
    base = 0
    doors = []
    merged = []
    for (x, z) in posts:
        merge_mlod(lods, os.path.join(DEV, "src", "JP", "parts", "frame", "jp_p_frame_post_planed.p3d"), 0.0, (x, 0.0, z), 0)
        merged.append("jp_p_frame_post_planed")
    for name, fr, dx in FIXED:
        yaw, t = place(fr, dx)
        grp = REG[name][2](REG[name][1]).group
        n = merge_mlod(lods, os.path.join(DEV, "src", "JP", "parts", grp, name + ".p3d"), yaw, t, base)
        doors += door_records(name, yaw, t, base)
        base += n
        merged.append(name)
    merge_mlod(lods, os.path.join(DEV, "src", "JP", "parts", "trim", "jp_p_trim_grime_post.p3d"), 0.0, (KEN, 0.0, 0.0), 0)
    merged.append("jp_p_trim_grime_post")
    lods = order_lods(lods)
    g = mlod.find_lod(lods, mlod.LOD_GEOMETRY)
    g.properties.update({"class": "house", "map": "house", "damage": "no", "autocenter": "0"})
    g.mass = [40000.0 / len(g.points)] * len(g.points)
    return lods, doors, merged


def binarize(name):
    if not os.path.isdir(r"P:\DZ") or not os.path.isdir(r"P:\JP\parts\_test"):
        return False, "P:\\DZ or P:\\JP\\parts\\_test missing"
    out = os.path.join(TEST_OUT, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\parts", "-binpath=P:\\bin", "P:\\JP\\parts\\_test", out, "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = os.path.join(TEST_OUT, "binarize.log")
    wb(log, (" ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr).replace("\r\n", "\n"))
    found_p = None
    for root, _, files in os.walk(out):
        if name + ".p3d" in files:
            found_p = os.path.join(root, name + ".p3d")
    bad = [l for l in (r.stdout + r.stderr).splitlines() if re.search(r"error|warning|cannot|not loaded", l, re.I)]
    return found_p, bad


def odol_check(path, doors):
    data = open(path, "rb").read()
    if data[:4] != b"ODOL":
        return False, "not ODOL"
    res = None
    for off in range(8, 400):
        k = struct.unpack_from("<I", data, off)[0]
        if 1 <= k <= 40:
            r = struct.unpack_from("<%df" % k, data, off + 4)
            if any(abs(x - 1e15) < 1e10 for x in r) and all(x > 0 for x in r):
                res = r
                break
    names = [mlod.lod_name(r) for r in res] if res else []
    low = {m.group().decode().lower() for m in re.finditer(rb"[\x20-\x7e]{4,}", data)}
    bones = [a["bone"] for d in doors for a in d.anims]
    ok_b = all(b in low and b + "_axis" in low for b in bones)
    skel = any("jp_p_test_assembly_skeleton" in s for s in low)
    want = ["Resolution 1", "Resolution 2", "Resolution 3", "Geometry", "Memory", "Roadway", "View Geometry",
            "Fire Geometry"]
    ok = res is not None and all(w in names for w in want) and ok_b and skel
    return ok, "ODOL v%d, %d bytes; LODs %s; door bones+axes %s; skeleton %s" % (
        struct.unpack_from("<I", data, 4)[0], len(data), ", ".join(names), ok_b, skel)


def assembly_checks(lods, doors):
    res = []
    L_ = {mlod.lod_name(l.resolution): l for l in lods}
    for lname in ("Geometry", "View Geometry", "Fire Geometry"):
        l = L_[lname]
        comps = [s for s in l.selections if s.startswith("Component")]
        bad = [c for c in comps if mlod.component_report(l, c)]
        res.append(("C7 %s closed+convex" % lname, not bad, "%d components, %d bad %s" % (len(comps), len(bad), bad[:3])))
    gcomps = checks.components(L_["Geometry"])
    for d in doors:
        if d.anims[0]["type"] != "translation":
            continue
        dd = copy.copy(d)
        # opening / face in world coordinates for the scan: use the placed axis to find the wall frame
        ok, msg = _door_world(dd, gcomps)
        res.append(("C7 door %s sweep + clear (real posts and walls)" % d.anims[0]["bone"], ok, msg))
    smp = checks.roadway_samples(L_["Roadway"])
    miss = 0
    for x, y, z, tex in smp:
        tops = [r[1] for c in gcomps if not c["door"] for r in [checks.ray_y(c, x, z)] if r and r[1] <= y + 0.05]
        if not tops or abs(max(tops) - y) > 0.03:
            miss += 1
    res.append(("C7 Roadway on Geometry", miss == 0, "%d/%d samples" % (len(smp) - miss, len(smp))))
    return res


def _door_world(d, gcomps):
    """Door check in world space: wall direction from the axis; scan the free width through the doorway."""
    a0 = d.anims[0]
    ax = a0["axis"]
    dv = [ax[1][k] - ax[0][k] for k in range(3)]
    bone = a0["bone"]
    leaf = [c for c in gcomps if c["door"] == bone]
    others = [c for c in gcomps if c["door"] != bone]
    amt = a0["amount"]
    lb = [c["bbox"] for c in leaf]
    bb = (min(b[0] for b in lb), max(b[1] for b in lb), min(b[2] for b in lb), max(b[3] for b in lb),
          min(b[4] for b in lb), max(b[5] for b in lb))
    sw = (min(bb[0], bb[0] + dv[0] * amt) + 0.004, max(bb[1], bb[1] + dv[0] * amt) - 0.004, bb[2] + 0.004, bb[3] - 0.004,
          min(bb[4], bb[4] + dv[2] * amt) + 0.002, max(bb[5], bb[5] + dv[2] * amt) - 0.002)
    hits = [c["name"] for c in others if checks.comp_box_intersect(c, sw)]
    opened = [checks.shifted(c, dv[0] * amt, dv[1] * amt, dv[2] * amt) for c in leaf]
    obst = others + opened
    along_x = abs(dv[0]) > 0.5
    # doorway centre: the leaf's closed centre along the wall, the wall line through the axis minus the leaf offset
    cx = (bb[0] + bb[1]) / 2 if along_x else (bb[4] + bb[5]) / 2
    wall = 0.0 if along_x else None
    zc = ax[0][2] - (0.08 if along_x else 0.0)
    y0 = bb[2] + 0.05

    def free(s):
        if along_x:
            col = (s - 0.004, s + 0.004, y0, y0 + 1.90, zc - 0.35, zc + 0.35)
        else:
            col = (ax[0][0] - 0.35, ax[0][0] + 0.35, y0, y0 + 1.90, s - 0.004, s + 0.004)
        return not any(checks.comp_box_intersect(c, col, 0.0) for c in obst)
    if not free(cx):
        return False, "doorway centre blocked; sweep hits %s" % hits[:3]
    lo = hi = cx
    while free(lo - 0.01) and lo > cx - 3:
        lo -= 0.01
    while free(hi + 0.01) and hi < cx + 3:
        hi += 0.01
    clear = hi - lo
    ok = not hits and clear >= 1.0
    return ok, "leaf slides %.2f m %s; open clear width %.2f m between the real posts" % (
        amt, "clear of every other component" if not hits else "HITS %s" % hits[:3], clear)


def main(argv):
    name = "jp_p_test_assembly"
    A = build()
    lods_a = A.lods()
    lods_b, doors, merged = path_b()
    ca = {mlod.lod_name(l.resolution): len(l.faces) for l in lods_a}
    cb = {mlod.lod_name(l.resolution): len(l.faces) for l in lods_b}
    same = all(ca.get(k) == cb.get(k) for k in set(ca) | set(cb))
    p3d = os.path.join(TEST_SRC, name + ".p3d")
    os.makedirs(TEST_SRC, exist_ok=True)
    mlod.write_mlod(p3d, lods_b)
    wb(os.path.join(TEST_SRC, "model.cfg"), modelcfg(name, doors))
    res = assembly_checks(mlod.read_mlod(p3d), doors)
    res.insert(0, ("path A (kit) == path B (MLOD merge) face counts per LOD", same, "A %s | B %s" % (ca, cb)))
    if "--no-binarize" not in argv:
        bp, bad = binarize(name)
        if bp:
            ok, msg = odol_check(bp, doors)
            res.append(("Binarize (cwd P:\\) -> ODOL", ok, msg + ("; %d warning lines (see log)" % len(bad) if bad else
                                                                  "; no warnings")))
        else:
            res.append(("Binarize (cwd P:\\) -> ODOL", False, "no ODOL written: %s" % bad))
    for c, o, dt in res:
        print("%-4s %-55s %s" % ("OK" if o else "FAIL", c, dt))
    wb(os.path.join(TEST_OUT, "assembly_checks.json"), json.dumps(
        {"assembly": name, "merged_from_mlod": merged, "doors": [[a["bone"] for a in d.anims] for d in doors],
         "lod_faces": cb, "checks": [{"check": c, "ok": bool(o), "detail": dt} for c, o, dt in res]}, indent=1))
    return 0 if all(o for _, o, _ in res) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
