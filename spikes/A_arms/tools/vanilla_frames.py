"""Render vanilla weapon meshes (ODOL LOD 0) with the hands their IK pose implies, in the p3d model frame.

Axis finding (spike A, 2026-09-26): an IK pose's RightHand_Dummy frame is NOT the p3d frame. For the
sword, spear and bat the knuckle lines of both hands run along the dummy's Z while the weapons run along
the p3d Y; the crossbow (asymmetric) fixes the sign. p3d = (dx, dz, -dy), i.e. dummy = Rx(+90) * p3d.

usage: python vanilla_frames.py            writes renders/vanilla_*.png and prints the grip numbers
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hands  # noqa: E402
from odol import read_odol  # noqa: E402
from overlay import render  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "renders")
IK = r"P:\DZ\anims\anm\player\ik"
MV = r"P:\DZ\anims\anm\player\moves"


def to_p3d(p):
    return (p[0], p[2], -p[1])


def hand_layers(h):
    segs_r = [(to_p3d(a), to_p3d(b)) for a, b in h["segs_r"]]
    segs_l = [(to_p3d(a), to_p3d(b)) for a, b in h["segs_l"]]
    pr = to_p3d(hands.palm_centre(h["fr"], "Right"))
    pl = to_p3d(hands.palm_centre(h["fl"], "Left"))
    wr = to_p3d(h["right"][0])
    wl = to_p3d(h["left"][0])
    return [
        {"segments": segs_r, "color": (200, 40, 40), "width": 3, "label": "right hand (IK pose)"},
        {"segments": segs_l, "color": (40, 80, 210), "width": 3, "label": "left hand"},
        {"points": [(pr, "R palm"), (wr, "R wrist")], "color": (200, 40, 40)},
        {"points": [(pl, "L palm"), (wl, "L wrist")], "color": (40, 80, 210)},
    ], pr, pl


def mesh_layer(path, color, label, lod=0, alpha=0.55):
    info = read_odol(path)
    L = info["lods"][lod]
    return {"verts": L.vertices, "faces": L.faces, "color": color, "alpha": alpha, "label": label}, info


def mem_points(info):
    pts = []
    for L in info["lods"]:
        if 9e14 < L.resolution < 2e15 and L.vertices:
            for n, vs in L.selections.items():
                if n.startswith("proxy") or n.startswith("boundingbox") or n.startswith("ce_") or n == "invview":
                    continue
                for v in vs:
                    pts.append((L.vertices[v], n))
    return pts


JOBS = [
    ("sword", r"P:\DZ\weapons\melee\blade\medieval_sword.p3d", IK + r"\two_handed\medieval_sword.anm", None),
    ("spear", r"P:\DZ\gear\crafting\advanced_spear.p3d", IK + r"\two_handed\advanced_spear.anm", None),
    ("crossbow", r"P:\DZ\weapons\archery\crossbow\crossbow.p3d", IK + r"\weapons\crossbow.anm", None),
    ("recurve", r"P:\DZ\weapons\archery\bow_recurve\bow_recurve.p3d", IK + r"\weapons\bow_erc_recurve_IK.anm",
     MV + r"\bow\p_bow_erc_idle_ras.anm"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for name, model, ik, clip in JOBS:
        h = hands.hands_in_item(ik, clip)
        ml, info = mesh_layer(model, (150, 150, 140), "vanilla %s LOD0" % name)
        hl, pr, pl = hand_layers(h)
        mp = {"points": mem_points(info), "color": (20, 140, 60), "radius": 3, "label": "memory points"}
        render([ml] + hl + [mp], os.path.join(OUT, "vanilla_%s_hands.png" % name),
               title="vanilla %s + hands from %s (left: %s)" % (name, os.path.basename(ik), h["left_source"]))
        res[name] = (pr, pl)
        print("%-9s R palm %s  L palm %s  (left from %s)" % (
            name, np.round(pr, 3), np.round(pl, 3), h["left_source"]))
    return res


if __name__ == "__main__":
    main()
