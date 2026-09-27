"""Grip-frame proof renders: each new model (LOD 0, from the generator) drawn in ONE frame with
  - the vanilla parent's binarized LOD 0 (read from the ODOL, grey, translucent)
  - the hands the parent's in-hands IK pose puts there (red = right, blue = left)
  - the vanilla and new memory points
Writes renders/grip_<name>.png and prints how far each hand's grip centre is from our grip axis.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hands  # noqa: E402
import models  # noqa: E402
from odol import read_odol  # noqa: E402
from overlay import render  # noqa: E402
from vanilla_frames import to_p3d, mem_points  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "renders")
IK = r"P:\DZ\anims\anm\player\ik"
CLIP = r"P:\DZ\anims\anm\player\moves\bow\p_bow_erc_idle_ras.anm"


def circumcentre(a, b, c):
    a, b, c = map(np.array, (a, b, c))
    ab, ac = b - a, c - a
    n = np.cross(ab, ac)
    d = 2 * np.dot(n, n)
    return a + (np.cross(n, ab) * np.dot(ac, ac) + np.cross(ac, n) * np.dot(ab, ab)) / d


def grip_centre(fw, side):
    return np.mean([circumcentre(*[to_p3d(fw[side + "Hand" + f + k][0]) for k in "123"]) for f in ("Index", "Middle", "Ring")], 0)


def mesh_layer_from(m, color, label, alpha=0.9):
    return {"verts": m.pts, "faces": [f["v"] for f in m.faces], "color": color, "alpha": alpha, "label": label}


def hands_layers(h):
    return [
        {"segments": [(to_p3d(a), to_p3d(b)) for a, b in h["segs_r"]], "color": (210, 30, 30), "width": 3, "label": "right hand (vanilla IK)"},
        {"segments": [(to_p3d(a), to_p3d(b)) for a, b in h["segs_l"]], "color": (30, 70, 220), "width": 3, "label": "left hand"},
    ]


def job(name, mesh, vanilla, ik, clip, zoom=None, extra_pts=None, axis_fn=None):
    info = read_odol(vanilla)
    V = info["lods"][0]
    van = {"verts": V.vertices, "faces": V.faces, "color": (150, 150, 150), "alpha": 0.35, "label": "vanilla " + os.path.basename(vanilla)}
    ours = mesh_layer_from(mesh, (205, 150, 60), name + " (ours)")
    vm = {"points": mem_points(info), "color": (20, 140, 60), "radius": 3, "label": "vanilla memory pts"}
    if ik:
        h = hands.hands_in_item(ik, clip)
        gr, gl = grip_centre(h["fr"], "Right"), grip_centre(h["fl"], "Left")
        pts = {"points": [(tuple(gr), "R grip"), (tuple(gl), "L grip")], "color": (20, 20, 20), "radius": 4}
        layers = [van, ours] + hands_layers(h) + [pts, vm]
    else:
        gr = gl = None
        layers = [van, ours, vm]
    if extra_pts:
        layers.append({"points": extra_pts, "color": (160, 0, 160), "radius": 4, "label": "our memory pts"})
    render(layers, os.path.join(OUT, "grip_%s.png" % name), title="%s in the vanilla frame (%s)" % (name, os.path.basename(ik) if ik else os.path.basename(vanilla)))
    if zoom:
        render(layers, os.path.join(OUT, "grip_%s_zoom.png" % name), title="%s grip close-up" % name, bounds=zoom)
    if axis_fn:
        for side, g in (("right", gr), ("left", gl)):
            print("  %-10s %s grip centre %s -> distance to our grip axis %.1f mm" % (name, side, np.round(g, 3), 1000 * axis_fn(g)))
    return gr, gl


def main():
    os.makedirs(OUT, exist_ok=True)
    kat = models.build_katana(1.0)
    job("jp_katana", kat, r"P:\DZ\weapons\melee\blade\medieval_sword.p3d", IK + r"\two_handed\medieval_sword.anm", None,
        zoom=((-0.1, -0.15, -0.1), (0.1, 0.2, 0.1)), axis_fn=lambda g: float(np.hypot(g[0], g[2])))
    yari = models.build_yari(1.0)
    job("jp_yari", yari, r"P:\DZ\gear\crafting\advanced_spear.p3d", IK + r"\two_handed\advanced_spear.anm", None,
        zoom=((-0.1, -0.15, -0.1), (0.1, 0.35, 0.1)), axis_fn=lambda g: float(np.hypot(g[0] - models.Y["ax"], g[2])))
    m, info, extra = models.yumi_bow_variant(1.0)
    mem = [(v[0], k) for k, v in models.yumi_memory(m, info, extra).items() if k in ("eye", "hlavne")]
    G = (-0.037, 0.0, -0.049)
    job("jp_yumi", m, r"P:\DZ\weapons\archery\bow_recurve\bow_recurve.p3d", IK + r"\weapons\bow_erc_recurve_IK.anm", CLIP,
        zoom=((-0.3, -0.25, -0.2), (0.3, 0.25, 0.1)), extra_pts=mem,
        axis_fn=lambda g: float(np.hypot(g[0] - G[0], g[2] - G[2])))
    m2, info2, extra2 = models.yumi_xb_variant(1.0)
    mem2 = [(v[0], k) for k, v in models.yumi_memory(m2, info2, extra2).items() if k in ("eye", "hlavne")]
    G2 = (-0.210, 0.035, 0.010)
    job("jp_yumi_xb", m2, r"P:\DZ\weapons\archery\crossbow\crossbow.p3d", IK + r"\weapons\crossbow.anm", None,
        zoom=((-0.45, -0.2, -0.3), (0.35, 0.3, 0.3)), extra_pts=mem2,
        axis_fn=lambda g: float(np.hypot(g[0] - G2[0], g[2] - G2[2])))
    ya = models.build_ya(1.0)
    job("jp_ya", ya, r"P:\DZ\weapons\projectiles\bolt_biggame.p3d", None, None)
    job("jp_ya_vs_arrow", ya, r"P:\DZ\weapons\projectiles\arrow_composite.p3d", None, None)


if __name__ == "__main__":
    main()
