"""Shared paths and helpers for spike W (wearables)."""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)                       # japan_dev/spikes/W_wearables
DEV = os.path.dirname(os.path.dirname(SPIKE))       # japan_dev
DATA = os.path.join(DEV, "data", "W")               # vanilla-derived reference data (git-ignored)
REF = os.path.join(DATA, "ref")
WORK = os.path.join(DATA, "work")
RENDERS = os.path.join(SPIKE, "renders")
SRC = os.path.join(DEV, "src", "JP", "characters")  # = P:\JP\characters
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
TOOLS_BIN = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
IMAGE_TO_PAA = os.path.join(TOOLS_BIN, "ImageToPAA", "ImageToPAA.exe")
BINARIZE = os.path.join(TOOLS_BIN, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS_BIN, "CfgConvert", "CfgConvert.exe")

BODY_PARTS = ("torso3", "legs3", "feet3", "hands3")
HEAD = {"m": "m_adam", "f": "f_eva_2"}


class Mesh:
    def __init__(self, P, F, UV=None, W=None, name=""):
        self.P = np.asarray(P, dtype=float)
        self.F = [list(f) for f in F]
        self.UV = None if UV is None else np.asarray(UV, dtype=float)
        self.W = W
        self.name = name


def load_ref(name):
    """Binarized (ODOL) faces are stored in the reverse order of MLOD faces (binarize flips them; checked on
    a test cube, see REPORT.md). Reversed here so every mesh in W's pipeline uses the MLOD winding."""
    d = json.load(open(os.path.join(REF, name + ".json")))
    return Mesh(d["points"], [f[::-1] for f in d["faces"]], d.get("uvs"), d.get("weights"), name)


def body(sex):
    """dict part -> Mesh for the vanilla naked body of one sex (reference only, never shipped)"""
    return {p: load_ref("%s_%s" % (p, sex)) for p in BODY_PARTS}


def tri_list(F):
    out = []
    for f in F:
        if len(f) == 3:
            out.append(f)
        else:
            out.append([f[0], f[1], f[2]])
            out.append([f[0], f[2], f[3]])
    return out


def run_blender(scene, tag):
    os.makedirs(WORK, exist_ok=True)
    path = os.path.join(WORK, "scene_%s.json" % tag)
    with open(path, "wb") as f:
        f.write(json.dumps(scene).encode())
    cmd = [BLENDER, "--background", "--factory-startup", "--python", os.path.join(HERE, "render_scene.py"), "--", path]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    outs = [l for l in r.stdout.splitlines() if l.startswith("RENDERED")]
    if not outs:
        print(r.stdout[-4000:])
        print(r.stderr[-3000:])
        raise SystemExit("blender render failed for " + tag)
    for l in outs:
        print(" ", l)
    return outs


def mesh_obj(name, m, P=None, **kw):
    o = {"name": name, "points": (m.P if P is None else P).tolist(), "faces": m.F}
    if m.UV is not None and kw.get("texture"):
        o["uvs"] = m.UV.tolist()
    o.update(kw)
    return o


def views(target, dist=3.2, ortho=None, names=("front", "side", "back", "q34"), prefix="", facing=-1):
    """camera shots around a target. facing=-1: character faces -Z (bind pose); +1: faces +Z (clips)."""
    dirs = {"front": [0, 0.05, facing], "back": [0, 0.05, -facing], "side": [-1, 0.05, 0],
            "side_r": [1, 0.05, 0], "q34": [-0.7, 0.25, facing * 0.7], "q34b": [0.7, 0.25, -facing * 0.7],
            "top": [0.0001, 1, facing * 0.2], "low": [-0.4, -0.35, facing * 0.8]}
    return [{"name": prefix + n, "target": list(target), "dir": dirs[n], "dist": dist, "ortho": ortho} for n in names]
