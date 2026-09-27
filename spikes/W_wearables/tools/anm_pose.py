"""Player skeleton bind pose (.xob) + vanilla .anm clips -> world bone transforms, for posing test renders.

Copied (read-only source, 2026-09-26) from pokemon_dev/tools/player_anim/{xob_player.py, anm_decode.py,
player_fk.py}, trimmed to what W needs, so nothing ever writes into pokemon_dev (no __pycache__ there).
Formats are documented in those files. Conventions: quaternion (x, y, z, w), child world = parent world *
local, DayZ model space X = the character's left in the bind pose, Y up, bind pose faces -Z; clips turn the
Pelvis so the character faces +Z.
"""
import struct

import numpy as np

XOB_M = r"P:\DZ\characters\bodies\player_testing.xob"
XOB_F = r"P:\DZ\characters\bodies\player_f_testing.xob"


# ---------------------------------------------------------------- xob
def parse_xob(path):
    data = open(path, "rb").read()
    if not (data[:4] == b"FORM" and data[8:12] == b"XOB6" and data[12:16] == b"HEAD"):
        raise ValueError("not an XOB6 skeleton: %s" % path)
    front, bone_count, back = struct.unpack_from("<HHH", data, 0x40)
    names_size = struct.unpack_from("<I", data, 0x4C)[0]
    raw = data[0x50:0x50 + names_size].split(b"\x00")
    names = [n.decode("ascii") for n in raw[:front + bone_count + back]]
    off = 0x50 + names_size + 2 * front
    bones = []
    for i in range(bone_count):
        idx, flags = struct.unpack_from("<hh", data, off)
        pos = struct.unpack_from("<3f", data, off + 4)
        quat = struct.unpack_from("<4f", data, off + 16)
        sib, child = struct.unpack_from("<hh", data, off + 32)
        off += 36
        bones.append({"name": names[idx], "index": i, "pos": list(pos), "quat": list(quat),
                      "sibling": sib, "child": child, "parent": -1, "children": []})
    for b in bones:
        c = b["child"]
        while c != -1:
            bones[c]["parent"] = b["index"]
            b["children"].append(c)
            c = bones[c]["sibling"]
    return bones


# ---------------------------------------------------------------- anm
def read_anm(path):
    d = open(path, "rb").read()
    if d[:4] != b"FORM" or d[8:12] != b"ANIM":
        raise ValueError("not an .anm: %s" % path)
    ver = d[12:16].decode("latin1")
    o = 20
    ch = {}
    while o + 8 <= len(d):
        tag = d[o:o + 4]
        sz = struct.unpack(">I", d[o + 4:o + 8])[0]
        ch[tag] = (o + 8, sz)
        o += 8 + sz
    fps = struct.unpack_from("<I", d, ch[b"FPS\x00"][0])[0]
    ho, hs = ch[b"HEAD"]
    tracks = []
    o, end = ho, ho + hs
    while o < end:
        if ver == "SET6":
            tmin, trng, qmin, qrng, smin, srng = struct.unpack_from("<6f", d, o)
            nf, nt, nq, ns = struct.unpack_from("<4H", d, o + 24)
            ln = d[o + 33]
            name = d[o + 34:o + 34 + ln].decode("latin1")
            o += 34 + ln
        elif ver == "SET5":
            name = d[o:o + 32].split(b"\x00")[0].decode("latin1")
            tmin, trng, qmin, qrng = struct.unpack_from("<4f", d, o + 32)
            nf, nt, nq, _ = struct.unpack_from("<4H", d, o + 48)
            smin, srng, ns = 100.0, 0.0, 0
            o += 56
        else:
            raise ValueError("unknown anm version %s" % ver)
        tracks.append({"name": name, "nf": nf, "n": (nt, nq, ns), "t_rng": (tmin, trng), "q_rng": (qmin, qrng),
                       "s_rng": (smin, srng)})
    do, ds = ch[b"DATA"]
    u = struct.unpack_from("<%dH" % (ds // 2), d, do)
    i = 0

    def chan(n, k, mn, rg):
        nonlocal i
        frames = list(u[i:i + n])
        i += n
        vals = []
        for _ in range(n):
            vals.append([mn + x / 65535.0 * rg for x in u[i:i + k]])
            i += k
        return dict(zip(frames, vals))

    for t in tracks:
        nt, nq, ns = t["n"]
        t["t"] = chan(nt, 3, *t["t_rng"])
        t["s"] = chan(ns, 3, *t["s_rng"]) if ns else {}
        t["q"] = chan(nq, 4, *t["q_rng"])
    return {"version": ver, "fps": fps, "numFrames": max(t["nf"] for t in tracks) if tracks else 0,
            "tracks": tracks}


def sample(chan_keys, f):
    ks = sorted(chan_keys)
    if not ks:
        return None
    if f <= ks[0]:
        return chan_keys[ks[0]]
    if f >= ks[-1]:
        return chan_keys[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= f <= b:
            w = (f - a) / float(b - a)
            va, vb = chan_keys[a], chan_keys[b]
            if len(va) == 4 and sum(x * y for x, y in zip(va, vb)) < 0:
                vb = [-x for x in vb]
            v = [x + (y - x) * w for x, y in zip(va, vb)]
            if len(v) == 4:
                n = sum(x * x for x in v) ** 0.5 or 1.0
                v = [x / n for x in v]
            return v


# ---------------------------------------------------------------- FK
def quat_mat(q):
    x, y, z, w = q
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def local_mats(bones, anm=None, frame=0, overrides=None):
    """{name: 4x4 local}: clip value where the clip has one, bind otherwise; overrides {name: (t|None, q|None)}"""
    tr = {t["name"]: t for t in anm["tracks"]} if anm else {}
    out = {}
    for b in bones:
        t, q = tuple(b["pos"]), tuple(b["quat"])
        a = tr.get(b["name"])
        if a:
            v = sample(a["t"], frame)
            if v:
                t = tuple(v)
            v = sample(a["q"], frame)
            if v:
                q = tuple(v)
        if overrides and b["name"] in overrides:
            ot, oq = overrides[b["name"]]
            if ot is not None:
                t = ot
            if oq is not None:
                q = oq
        m = np.eye(4)
        m[:3, :3] = quat_mat(np.array(q) / np.linalg.norm(q))
        m[:3, 3] = t
        out[b["name"]] = m
    return out


def world_mats(bones, local):
    by_i = {b["index"]: b for b in bones}
    w = {}

    def get(b):
        if b["name"] in w:
            return w[b["name"]]
        if b["parent"] == -1:
            w[b["name"]] = local[b["name"]]
        else:
            w[b["name"]] = get(by_i[b["parent"]]) @ local[b["name"]]
        return w[b["name"]]
    for b in bones:
        get(b)
    return w


class Rig:
    """bind + pose -> per-bone skinning matrices (keys lower-case, the p3d/ODOL spelling)"""

    def __init__(self, xob=XOB_M):
        self.bones = parse_xob(xob)
        self.bind = world_mats(self.bones, local_mats(self.bones))
        self.bind_inv = {k: np.linalg.inv(v) for k, v in self.bind.items()}

    def joint(self, name):
        return self.bind[name][:3, 3].copy()

    def skin_mats(self, anm=None, frame=0, overrides=None, face_forward=None):
        w = world_mats(self.bones, local_mats(self.bones, anm, frame, overrides))
        out = {k.lower(): w[k] @ self.bind_inv[k] for k in w}
        if face_forward is not None:
            out = {k: face_forward @ v for k, v in out.items()}
        return out


def skin(points, weights, mats):
    """linear blend skinning. points (N,3); weights: list per vertex of [bone(lower), w]"""
    P = np.asarray(points, dtype=float)
    out = np.zeros_like(P)
    Ph = np.hstack([P, np.ones((len(P), 1))])
    for i, ws in enumerate(weights):
        acc = np.zeros(3)
        tot = 0.0
        for b, w in ws:
            m = mats.get(b.lower())
            if m is None:
                continue
            acc += w * (m @ Ph[i])[:3]
            tot += w
        out[i] = acc / tot if tot > 0 else P[i]
    return out
