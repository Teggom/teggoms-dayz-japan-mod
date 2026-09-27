"""Kasa previews: bind pose + posed, male and female."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import kasa
import scene
from wlib import SRC, RENDERS

TEX = os.path.join(SRC, "kasa", "data", "jp_kasa_co.png")
g = kasa.build()
outs = []
for sex in "mf":
    def shots(pose, J):
        h = J("Head")
        fac = -1 if pose == "bind" else 1
        dirs = {"front": [0, 0.15, fac], "side": [-1, 0.15, 0], "q34b": [0.7, 0.35, -0.7 * fac]}
        return [{"name": n, "target": (h + [0, 0.08, 0]).tolist(), "dir": d, "dist": 1.6, "ortho": 0.75} for n, d in dirs.items()]
    outs += scene.render("kasa", sex, [(g, {"straw": TEX})], ["bind", "sprint", "prone"], shots, res=(560, 560), samples=16)
print(scene.sheet(outs, os.path.join(RENDERS, "kasa", "kasa_sheet.png"), cols=6, scale=0.4))
