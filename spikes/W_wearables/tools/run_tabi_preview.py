"""Tabi + waraji previews (QA colours: backfaces magenta), bind + posed, male and female."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import tabi, scene
from wlib import SRC, RENDERS

poses = sys.argv[1].split(",") if len(sys.argv) > 1 else ["bind", "walk", "crouch"]
tex = sys.argv[2] if len(sys.argv) > 2 else None
outs = []
for sex in "mf":
    g = tabi.build_item(sex)
    looks = {"tabi": tex or [0.92, 0.91, 0.87, 1]}
    def shots(pose, J):
        a = (J("LeftFoot") + J("RightFoot")) / 2
        fac = -1 if pose == "bind" else 1
        dirs = {"front": [0.25, 0.35, fac], "side": [-1, 0.25, 0.1 * fac], "back": [0.3, 0.3, -fac]}
        return [{"name": n, "target": (a + [0, -0.03, 0]).tolist(), "dir": d, "dist": 2.0, "ortho": 0.55} for n, d in dirs.items()]
    outs += scene.render("tabi", sex, [(g, looks)], poses, shots, hide=("feet3",), res=(560, 460), samples=14)
print(scene.sheet(outs, os.path.join(RENDERS, "tabi", "tabi_sheet_%s.png" % "_".join(poses)), cols=6, scale=0.45))
