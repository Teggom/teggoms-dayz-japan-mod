"""List an ODOL LOD's sections (face ranges + material index) for the mesh odol_mesh.py extracted.

Section record (v54, 42 bytes, found by probing 2026-09-26):
  u32 faceLo, u32 faceHi   byte offsets into the in-memory face list (tri = 8 bytes, quad = 10 bytes)
  u32 minBone, u32 boneCount, u32 0, u32 flags?, u32 0, u16 0, i32 materialIndex, f32 ?, f32 ?
usage: python odol_sections.py file.p3d mesh.json
"""
import json
import struct
import sys

import numpy as np


def sections(path, face_block_off):
    d = open(path, "rb").read()
    nf, size, _ = struct.unpack_from("<IIH", d, face_block_off)
    p = face_block_off + 10
    mem = []   # in-memory offset of each face
    acc = 0
    for _ in range(nf):
        k = d[p]
        mem.append(acc)
        acc += 8 if k == 3 else 10
        p += 1 + 2 * k
    n = struct.unpack_from("<I", d, p)[0]
    p += 4
    out = []
    for _ in range(n):
        lo, hi, minb, nb, z0, flags, z1 = struct.unpack_from("<7I", d, p)
        mat = struct.unpack_from("<i", d, p + 30)[0]
        f0 = mem.index(lo) if lo in mem else None
        f1 = mem.index(hi) if hi in mem else nf
        out.append({"faces": (f0, f1), "material": mat, "flags": hex(flags), "bones": (minb, nb)})
        p += 42
    return out


if __name__ == "__main__":
    path, mj = sys.argv[1], sys.argv[2]
    m = json.load(open(mj))
    from odol_mesh import find_faces
    d = open(path, "rb").read()
    import odol_probe
    _, found = odol_probe.probe(path)
    n = len(m["points"])
    o = [f for f in found if f[1] == n and f[2] == "lzo"][0][0]
    fo = find_faces(d, n, o)
    P = np.array(m["points"])
    UV = np.array(m["uvs"]) if m.get("uvs") else None
    for s in sections(path, fo[0]):
        a, b = s["faces"]
        idx = sorted({i for f in m["faces"][a:b] for i in f})
        c = P[idx].mean(0)
        uvb = "" if UV is None else "uv[%.2f..%.2f, %.2f..%.2f]" % (UV[idx, 0].min(), UV[idx, 0].max(), UV[idx, 1].min(), UV[idx, 1].max())
        print("faces %4d-%4d mat %2d flags %s  centroid (%+.2f %+.2f %+.2f)  y[%.2f..%.2f] %s" % (
            a, b, s["material"], s["flags"], c[0], c[1], c[2], P[idx, 1].min(), P[idx, 1].max(), uvb))
