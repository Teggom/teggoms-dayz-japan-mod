"""Render the extracted vanilla bodies (male + female) in bind pose, textured with the vanilla skin, with backface
culling ON - proves the ODOL extraction (positions, faces, winding, UVs) before anything is fitted to it."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wlib import *  # noqa

TEX = {"m": os.path.join(DATA, "tex", "m_adam_body_co.png"), "f": os.path.join(DATA, "tex", "f_eva_body_co.png")}

for sex in ("m", "f"):
    objs = []
    for part, m in body(sex).items():
        objs.append(mesh_obj(part, m, texture=TEX[sex], backface_cull=True))
    head = load_ref(HEAD[sex])
    objs.append(mesh_obj("head", head, color=[0.75, 0.6, 0.5, 1], backface_cull=True))
    scene = {"out_dir": os.path.join(RENDERS, "ref"), "res": [700, 1000], "engine": "CYCLES", "samples": 16,
             "objects": objs, "shots": views([0, 0.95, 0], dist=4, ortho=2.1, names=("front", "side", "back"),
                                             prefix="ref_%s_" % sex)}
    run_blender(scene, "ref_" + sex)
