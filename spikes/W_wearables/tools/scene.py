"""Posed preview renders: vanilla body (reference only) + W garments, skinned by linear blend skinning with the
real vanilla animation clips (xob bind pose + .anm, anm_pose.py), rendered headless in Blender.
"""
import os

import numpy as np

import anm_pose
from wlib import load_ref, body, run_blender, DATA, RENDERS, Mesh

ANM = r"P:\DZ\anims\anm\player"
CLIPS = {
    "bind": None,
    "idle": ("moves/unarmed/p_erc_idle.anm", 0),
    "walk": ("moves/unarmed/p_erc_walkf.anm", "stride"),
    "sprint": ("moves/unarmed/p_erc_sprintf.anm", "stride"),
    "crouch": ("moves/unarmed/p_cro_idle.anm", 0),
    "crouchwalk": ("moves/unarmed/p_cro_walkf.anm", "stride"),
    "prone": ("moves/unarmed/p_pne_idle.anm", 0),
    "sit": ("gestures/sit/p_cro_sit_loop.anm", 0),
    "armsup": ("moves/surrender_restrained/surrender/p_sur_erc_idle.anm", 0),
    "rifle": ("moves/rifles/p_rfl_erc_idle_ras.anm", 0),
}
SKIN = [0.78, 0.60, 0.48, 1]
SHOW_BACKFACES = True
ATLAS = {"m": os.path.join(DATA, "tex", "m_guo_body_co.png"), "f": os.path.join(DATA, "tex", "f_eva_body_co.png")}
UNDER = [0.55, 0.50, 0.42, 1]
_rigs = {}
_clips = {}


def rig(sex):
    if sex not in _rigs:
        _rigs[sex] = anm_pose.Rig(anm_pose.XOB_M if sex == "m" else anm_pose.XOB_F)
    return _rigs[sex]


def clip_mats(sex, pose):
    r = rig(sex)
    if pose == "bind" or CLIPS.get(pose) is None:
        return r.skin_mats(), 0
    path, frame = CLIPS[pose]
    if path not in _clips:
        _clips[path] = anm_pose.read_anm(os.path.join(ANM, path))
    a = _clips[path]
    if frame == "stride":
        best, bf = -1, 0
        for f in range(a["numFrames"]):
            w = anm_pose.world_mats(r.bones, anm_pose.local_mats(r.bones, a, f))
            d = np.linalg.norm(w["LeftFoot"][:3, 3] - w["RightFoot"][:3, 3])
            if d > best:
                best, bf = d, f
        frame = bf
    return r.skin_mats(a, frame), frame


def head_mesh(sex):
    """body-space head for previews: female f_keiko (weights from the ODOL), male m_guo (stored 0.907 m low,
    shifted; weights synthesised: head above the jaw, neck/neck1 below)"""
    if sex == "f":
        m = load_ref("f_keiko")
        return m
    m = load_ref("m_guo")
    m.P = m.P.copy()
    m.P[:, 1] += 1.449 - m.P[:, 1].min()
    W = []
    for p in m.P:
        y = p[1]
        if y > 1.60:
            W.append([["head", 1.0]])
        elif y > 1.53:
            t = (y - 1.53) / 0.07
            W.append([["head", t], ["neck1", 1 - t]])
        else:
            t = max(0.0, (y - 1.45) / 0.08)
            W.append([["neck1", t * 0.5], ["neck", 0.5 * t + (1 - t) * 0.5], ["spine3", (1 - t) * 0.5]])
        W[-1] = [x for x in W[-1] if x[1] > 0]
    m.W = W
    return m


def joint_world(sex, mats, name):
    return (mats[name.lower()] @ np.append(rig(sex).joint(name), 1.0))[:3]


def lbs(points, weights_list, mats):
    return anm_pose.skin(points, weights_list, mats)


def render(tag, sex, garments, poses, shots_fn, hide=(), res=(640, 900), samples=16, out_dir=None,
           textures=None, extra=None):
    """garments: list of (Garment, {material: texture png or rgba}) ; hide: body parts to leave out
    shots_fn(pose, joint) -> list of shots, joint(name) = posed world position of a bone. One Blender run
    per pose."""
    out_dir = out_dir or os.path.join(RENDERS, tag)
    B = body(sex)
    parts = {k: v for k, v in B.items() if k not in hide}
    head = head_mesh(sex) if "head" not in hide else None
    outs = []
    for pose in poses:
        mats, frame = clip_mats(sex, pose)
        objs = []
        atlas = ATLAS[sex]
        for name, m in parts.items():
            P = lbs(m.P, m.W, mats)
            o = {"name": name, "points": P.tolist(), "faces": m.F, "color": SKIN, "roughness": 0.6,
                 "show_backfaces": False}
            if name != "torso3" and m.UV is not None:
                o["uvs"] = m.UV.tolist()
                o["texture"] = atlas
            objs.append(o)
        if head is not None:
            P = lbs(head.P, head.W, mats)
            o = {"name": "head", "points": P.tolist(), "faces": head.F, "color": SKIN, "roughness": 0.6,
                 "show_backfaces": False}
            if head.UV is not None:
                o["uvs"] = head.UV.tolist()
                o["texture"] = atlas
            objs.append(o)
        for gi, (g, looks) in enumerate(garments):
            P = lbs(g.arrays(), g.weight_list(), mats)
            by_mat = {}
            for fi, m in enumerate(g.FM):
                by_mat.setdefault(m, []).append(fi)
            for m, fis in by_mat.items():
                look = looks.get(m, [0.6, 0.6, 0.6, 1])
                o = {"name": "%s_%d_%s" % (g.name, gi, m), "points": P.tolist(),
                     "faces": [g.F[i] for i in fis], "face_uvs": [g.FUV[i] for i in fis], "roughness": 0.8,
                     "show_backfaces": SHOW_BACKFACES and m != "lining", "cull": True}
                if isinstance(look, str):
                    o["texture"] = look
                else:
                    o["color"] = look
                objs.append(o)
        if extra:
            objs += extra(pose, mats)
        shots = shots_fn(pose, lambda j: joint_world(sex, mats, j))
        for s in shots:
            s["name"] = "%s_%s_%s" % (sex, pose, s["name"])
        scene = {"out_dir": out_dir, "res": list(res), "engine": "CYCLES", "samples": samples,
                 "objects": objs, "shots": shots}
        outs += run_blender(scene, "%s_%s_%s" % (tag, sex, pose))
    return outs


def sheet(paths, out, cols=4, scale=0.5):
    from PIL import Image
    ims = [Image.open(p.split("RENDERED ", 1)[-1].strip()) for p in paths]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    s = Image.new("RGB", (w * cols, h * rows), (255, 255, 255))
    for i, im in enumerate(ims):
        s.paste(im.convert("RGB"), ((i % cols) * w, (i // cols) * h))
    s = s.resize((int(w * cols * scale), int(h * rows * scale)))
    s.save(out)
    return out
