"""Evidence renders made FROM THE SHIPPED FILES: the MLOD LOD 0 that binarize consumed (verify_odol.py proves the
ODOL carries the same points, faces and weights), skinned by its own weights on real vanilla clips.

usage: python final_renders.py [set ...]    sets: kasa tabi short long seams ground outfit lods
Writes spikes/W_wearables/renders/final/<set>/... and a contact sheet per set.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene  # noqa: E402
from garment import Garment  # noqa: E402
from mlod_w import read_mlod  # noqa: E402
from modelcfg import skeleton_pairs  # noqa: E402
from wlib import WORK, SRC, RENDERS  # noqa: E402

OUT = os.path.join(RENDERS, "final")
BONES = None
TEX = {
    "kasa": os.path.join(SRC, "kasa", "data", "jp_kasa_co.png"),
    "kimono_short": os.path.join(SRC, "kimono", "data", "jp_kimono_short_co.png"),
    "kimono_long": os.path.join(SRC, "kimono", "data", "jp_kimono_long_co.png"),
    "tabi_waraji": os.path.join(SRC, "tabi", "data", "jp_tabi_waraji_co.png"),
}


def load(sub, name, lod=0):
    """-> (Garment, looks) from the MLOD copy of a shipped p3d"""
    global BONES
    if BONES is None:
        BONES = {b for b, _ in skeleton_pairs()}
    L = read_mlod(os.path.join(WORK, "mlod", sub, name + ".p3d"))[lod]
    g = Garment(name)
    g.P = [np.array(p) for p in L.points]
    g.W = [dict() for _ in L.points]
    for sel, (pw, fs) in L.selections.items():
        if sel.lower() in BONES:
            for i, w in pw.items():
                g.W[i][sel.lower()] = w
    for w in g.W:
        s = sum(w.values()) or 1.0
        for k in w:
            w[k] /= s
    key = next(k for k in TEX if name.startswith("jp_" + k))
    for verts, flags, tex, mat in L.faces:
        g.F.append([v[0] for v in verts])
        g.FUV.append([(v[2], v[3]) for v in verts])
        g.FM.append("skin" if "hhl_dummy_skin" in mat else "cloth")
    return g, key


def looks_for(key, sex):
    return {"cloth": TEX[key], "skin": scene.ATLAS[sex]}


def views_fn(target_joint, offs, ortho, dist=3.0, names=("front", "side", "back", "q34")):
    def f(pose, J):
        t = (J(target_joint) + np.array(offs)).tolist()
        fac = -1 if pose == "bind" else 1
        dirs = {"front": [0, 0.08, fac], "side": [-1, 0.08, 0], "back": [0, 0.08, -fac], "q34": [0.75, 0.3, 0.75 * fac],
                "q34b": [-0.7, 0.3, -0.7 * fac], "low": [0.5, -0.25, 1.0 * fac], "top": [0.3, 1.0, 0.4 * fac]}
        return [{"name": n, "target": t, "dir": dirs[n], "dist": dist, "ortho": ortho} for n in names]
    return f


def run(set_name, sexes, items, poses, shots, hide, res=(520, 640), cols=4, scale=0.5, samples=16):
    scene.SHOW_BACKFACES = False
    outs = []
    for sex in sexes:
        gs = []
        for sub, stem in items:
            g, key = load(sub, stem + "_" + sex)
            gs.append((g, looks_for(key, sex)))
        outs += scene.render(set_name, sex, gs, poses, shots, hide=hide, res=res, samples=samples,
                             out_dir=os.path.join(OUT, set_name))
    sheet = scene.sheet(outs, os.path.join(OUT, set_name, "%s_sheet.png" % set_name), cols=cols, scale=scale)
    print("SHEET", sheet)
    return sheet


def main(argv):
    sets = argv or ["kasa", "tabi", "short", "long", "seams", "ground", "outfit"]
    if "kasa" in sets:
        run("kasa", "mf", [("kasa", "jp_kasa")], ["bind", "idle", "sprint", "prone", "rifle"],
            views_fn("Head", [0, 0.06, 0], 0.75, names=("front", "side", "q34b")), (), res=(460, 460), cols=6, scale=0.45)
    if "tabi" in sets:
        def feet(pose, J):
            t = ((J("LeftFoot") + J("RightFoot")) / 2 + np.array([0, -0.02, 0])).tolist()
            fac = -1 if pose == "bind" else 1
            dirs = {"front": [0.3, 0.35, fac], "side": [-1, 0.25, 0.15 * fac], "back": [0.3, 0.3, -fac]}
            o = 0.55 if pose in ("bind", "idle", "crouch") else 0.9
            return [{"name": n, "target": t, "dir": d, "dist": 2.5, "ortho": o} for n, d in dirs.items()]
        run("tabi", "mf", [("tabi", "jp_tabi_waraji")], ["bind", "walk", "sprint", "crouch"], feet, ("feet3",),
            res=(480, 400), cols=6, scale=0.5)
    for length in ("short", "long"):
        if length in sets:
            o = 1.6 if length == "short" else 2.0
            y = 0.15 if length == "short" else -0.05
            run(length, "mf", [("kimono", "jp_kimono_" + length)],
                ["bind", "idle", "walk", "sprint", "crouch", "crouchwalk", "sit", "prone", "armsup", "rifle"],
                views_fn("Pelvis", [0, y, 0], o), ("torso3",), res=(420, 520), cols=8, scale=0.5, samples=14)
    if "seams" in sets:
        def seams(pose, J):
            fac = -1 if pose == "bind" else 1
            return [
                {"name": "neck_front", "target": J("Neck").tolist(), "dir": [0.1, 0.2, fac], "dist": 2, "ortho": 0.32},
                {"name": "neck_back", "target": J("Neck").tolist(), "dir": [0.1, 0.35, -fac], "dist": 2, "ortho": 0.32},
                {"name": "wrist", "target": J("LeftHand").tolist(), "dir": [0.7, -0.1, 0.7 * fac], "dist": 2, "ortho": 0.3},
                {"name": "cuff_in", "target": J("LeftHand").tolist(), "dir": [1.0, -0.3, 0.0], "dist": 2, "ortho": 0.3},
                {"name": "ankle", "target": J("LeftFoot").tolist(), "dir": [0.8, 0.3, 0.5 * fac], "dist": 2, "ortho": 0.3},
                {"name": "hem_under", "target": (J("Pelvis") + [0, -0.25, 0]).tolist(), "dir": [0.2, -0.7, 0.7 * fac], "dist": 2, "ortho": 0.8},
            ]
        run("seams", "mf", [("kimono", "jp_kimono_short"), ("tabi", "jp_tabi_waraji"), ("kasa", "jp_kasa")],
            ["bind", "idle", "rifle"], seams, ("torso3", "feet3"), res=(420, 420), cols=6, scale=0.5)
    if "outfit" in sets:
        for length in ("short", "long"):
            run("outfit_" + length, "mf", [("kasa", "jp_kasa"), ("kimono", "jp_kimono_" + length), ("tabi", "jp_tabi_waraji")],
                ["idle", "walk", "crouch", "rifle"], views_fn("Pelvis", [0, 0.2, 0], 2.1, names=("q34", "side")),
                ("torso3", "feet3"), res=(480, 640), cols=4, scale=0.5)
    if "ground" in sets:
        ground()
    if "lods" in sets:
        lods()


def ground():
    objs = []
    x = -0.55
    for sub, name, key in (("kasa", "jp_kasa_g", "kasa"), ("kimono", "jp_kimono_short_g", "kimono_short"),
                           ("kimono", "jp_kimono_long_g", "kimono_long"), ("tabi", "jp_tabi_waraji_g", "tabi_waraji")):
        L = read_mlod(os.path.join(WORK, "mlod", sub, name + ".p3d"))[0]
        P = np.array(L.points)
        P[:, 0] += x
        x += 0.40
        faces = [[v[0] for v in f[0]] for f in L.faces]
        fuv = [[(v[2], v[3]) for v in f[0]] for f in L.faces]
        objs.append({"name": name, "points": P.tolist(), "faces": faces, "face_uvs": fuv, "texture": TEX[key],
                     "roughness": 0.8, "cull": True})
    shots = [{"name": "ground_q34", "target": [0.0, 0.05, 0], "dir": [0.5, 0.7, -0.7], "dist": 3, "ortho": 1.9},
             {"name": "ground_top", "target": [0.0, 0.0, 0], "dir": [0.001, 1, -0.05], "dist": 3, "ortho": 1.9}]
    sc = {"out_dir": os.path.join(OUT, "ground"), "res": [900, 520], "engine": "CYCLES", "samples": 20,
          "objects": objs, "shots": shots}
    outs = scene.run_blender(sc, "final_ground")
    print("SHEET", scene.sheet(outs, os.path.join(OUT, "ground", "ground_sheet.png"), cols=1, scale=0.8))


def lods():
    """LOD 0 / 1 / 2 side by side (male kimono short, tabi, kasa) - the lower LODs must keep the silhouette"""
    objs = []
    x = -0.9
    for sub, name, key in (("kimono", "jp_kimono_short_m", "kimono_short"),):
        for lod in (0, 1, 2):
            L = read_mlod(os.path.join(WORK, "mlod", sub, name + ".p3d"))[lod]
            P = np.array(L.points)
            P[:, 0] += x
            x += 0.9
            faces = [[v[0] for v in f[0]] for f in L.faces]
            fuv = [[(v[2], v[3]) for v in f[0]] for f in L.faces]
            objs.append({"name": "%s_%d" % (name, lod), "points": P.tolist(), "faces": faces, "face_uvs": fuv,
                         "texture": TEX[key], "roughness": 0.8, "cull": True})
    shots = [{"name": "lods_front", "target": [0.0, 1.1, 0], "dir": [0.2, 0.1, -1], "dist": 4, "ortho": 2.8}]
    sc = {"out_dir": os.path.join(OUT, "lods"), "res": [1100, 560], "engine": "CYCLES", "samples": 16, "objects": objs, "shots": shots}
    scene.run_blender(sc, "final_lods")


if __name__ == "__main__":
    main(sys.argv[1:])
