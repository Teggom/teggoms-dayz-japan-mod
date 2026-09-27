"""Kimono previews (QA colours: backfaces magenta). usage: run_kimono_preview.py poses [length] [tag]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import kimono, kimono_parts, scene
from wlib import SRC, RENDERS

FLAGS = [a for a in sys.argv[1:] if a.startswith("--")]
sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if not a.startswith("--")]
poses = sys.argv[1].split(",") if len(sys.argv) > 1 else ["bind"]
length = sys.argv[2] if len(sys.argv) > 2 else "short"
tag = sys.argv[3] if len(sys.argv) > 3 else "kimono_" + length
sexes = sys.argv[4] if len(sys.argv) > 4 else "mf"
tex = os.path.join(SRC, "kimono", "data", "jp_kimono_%s_co.png" % length)
use_tex = os.path.isfile(tex) and "--flat" not in FLAGS
INDIGO = [0.12, 0.16, 0.32, 1]
looks = {"trunk": INDIGO, "sleeve_left": [0.14, 0.2, 0.4, 1], "sleeve_right": [0.14, 0.2, 0.4, 1],
         "collar": [0.05, 0.05, 0.08, 1], "obi": [0.45, 0.25, 0.1, 1], "cuff_left": [0.3, 0.3, 0.5, 1],
         "cuff_right": [0.3, 0.3, 0.5, 1], "lining": [0.3, 0.35, 0.55, 1], "skin": scene.SKIN}
if use_tex:
    looks = {k: (tex if k != "skin" else scene.ATLAS["m"]) for k in looks}
outs = []
for sex in sexes:
    mode = "B" if "--modeB" in FLAGS else "A"
    g = kimono_parts.build_full(sex, length, 0, mode)
    if use_tex:
        looks["skin"] = scene.ATLAS[sex]
    if False:
        looks["skin"] = scene.ATLAS["f"]
    def shots(pose, J):
        p = J("Pelvis")
        fac = -1 if pose == "bind" else 1
        tgt = (p + [0, 0.18 if length == "short" else -0.05, 0]).tolist()
        o = 1.5 if length == "short" else 2.0
        dirs = {"front": [0, 0.1, fac], "side": [-1, 0.1, 0], "back": [0, 0.1, -fac], "q34": [0.7, 0.3, 0.7 * fac]}
        return [{"name": n, "target": tgt, "dir": d, "dist": 3.0, "ortho": o} for n, d in dirs.items()]
    outs += scene.render(tag, sex, [(g, looks)], poses, shots, hide=("torso3",), res=(520, 640), samples=14)
print(scene.sheet(outs, os.path.join(RENDERS, tag, "%s_%s.png" % (tag, "_".join(poses))), cols=4, scale=0.5))
