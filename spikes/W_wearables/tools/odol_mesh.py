"""Extract one LOD's triangle mesh (+ skin weights where present) from a binarized DayZ ODOL v54 p3d.

This is a heuristic reader, written for this spike (2026-09-26) to get REFERENCE geometry of the vanilla
naked body parts (torso3_m/f, legs3_m/f, feet3_m/f, hands3_m/f) for fitting garments. It is not a general
ODOL parser. What it relies on (found by probing, see REPORT.md "ODOL notes"):
  * arrays >= 1024 bytes are LZO1X compressed: u32 count, then the LZO stream (no compressed length)
  * the per-LOD vertex block is:  positions (count, 12 B, LZO)  ->  normals (count, u8 fill flag, 4 B)
    -> ST (count, 8 B) -> vertexBoneRef (count, 12 B = u32 n + 4 x (u8 subBone, u8 weight/255))
    -> neighbour refs (count, usually 0) ...
  * faces: u32 nFaces, u32 byteSize, u16 0, then per face u8 n (3|4) + n x u16 vertex index
  * the LOD's sub-skeleton: a u32 count + u32 skeleton-bone indices, found before the LOD's proxies

usage: python odol_mesh.py file.p3d out.json [--lod-vertex-count N]
The LOD with the most vertices is taken unless N is given.
"""
import json
import struct
import sys

from lzo import decompress, LzoError
from odol_probe import probe


def read_skeleton(d):
    i = d.find(b"DayzTemporarySkeleton\x00")
    if i < 0:
        return None, []
    o = i + len("DayzTemporarySkeleton") + 1
    o += 1  # isDiscrete / inherit byte (0)
    n = struct.unpack_from("<I", d, o)[0]
    o += 4
    bones = []
    for _ in range(n):
        e = d.index(b"\x00", o); name = d[o:e].decode("ascii"); o = e + 1
        e = d.index(b"\x00", o); par = d[o:e].decode("ascii"); o = e + 1
        bones.append((name, par))
    return o, bones


def find_faces(d, nverts, before):
    """Scan backwards from `before` for the largest valid polygon block referencing < nverts."""
    best = None
    for o in range(before - 16, 0, -1):
        nf, size, zero = struct.unpack_from("<IIH", d, o)
        # size is the in-memory size (8 bytes per triangle), not the stored one
        if not (10 <= nf <= 100000) or zero != 0 or size < nf * 8 or size > nf * 10 + 16:
            continue
        p = o + 10
        faces = []
        ok = True
        for _ in range(nf):
            if p >= len(d):
                ok = False; break
            k = d[p]
            if k not in (3, 4):
                ok = False; break
            idx = struct.unpack_from("<%dH" % k, d, p + 1)
            if max(idx) >= nverts:
                ok = False; break
            faces.append(list(idx))
            p += 1 + 2 * k
        if ok and faces and max(max(f) for f in faces) == nverts - 1:
            return o, faces
    return best


def find_subskeleton(d, nbones, lod_lo, lod_hi):
    """u32 count + count x u32 (< nbones, distinct), then u32 count2 == nbones -> LAST match before the faces
    (every LOD has its own table; the one belonging to this LOD is the nearest one before its polygons)."""
    for o in range(lod_hi - 8, lod_lo, -1):
        n = struct.unpack_from("<I", d, o)[0]
        if not (1 <= n <= nbones):
            continue
        vals = struct.unpack_from("<%dI" % n, d, o + 4) if o + 4 + 4 * n <= len(d) else None
        if not vals or max(vals) >= nbones or len(set(vals)) != n:
            continue
        n2 = struct.unpack_from("<I", d, o + 4 + 4 * n)[0]
        if n2 == nbones:
            return o, list(vals)
    return None, None


def main(argv):
    path, out = argv[0], argv[1]
    want = None
    if "--lod-vertex-count" in argv:
        want = int(argv[argv.index("--lod-vertex-count") + 1])
    d, found = probe(path)
    cands = [f for f in found if f[2] == "lzo"]
    if want:
        cands = [f for f in cands if f[1] == want]
    o, n, _, data, used = max(cands, key=lambda f: f[1])
    pts = [list(struct.unpack_from("<3f", data, 12 * i)) for i in range(n)]
    # walk: normals (flag byte), ST, bone refs
    p = o + 4 + used
    weights = None
    try:
        c = struct.unpack_from("<I", d, p)[0]; assert c == n
        flag = d[p + 4]
        if flag:
            p = p + 5 + 4
        else:
            _, u = decompress(d, p + 5, n * 4); p = p + 5 + u
        c = struct.unpack_from("<I", d, p)[0]; assert c == n
        _, u = decompress(d, p + 4, n * 8); p = p + 4 + u
        c = struct.unpack_from("<I", d, p)[0]
        if c == n:
            raw, u = decompress(d, p + 4, n * 12)
            weights = []
            for i in range(n):
                k = struct.unpack_from("<I", raw, 12 * i)[0]
                ws = []
                for j in range(min(k, 4)):
                    b, w = raw[12 * i + 4 + 2 * j], raw[12 * i + 5 + 2 * j]
                    ws.append([b, w / 255.0])
                weights.append(ws)
    except (AssertionError, LzoError, IndexError) as e:
        print("weights not read:", e)
    fo = find_faces(d, n, o)
    faces = fo[1] if fo else []
    skel_end, bones = read_skeleton(d)
    sub = None
    if bones and fo:
        so, sub = find_subskeleton(d, len(bones), skel_end, fo[0])
    uvs = read_uvs(d, n, o)
    named = None
    if weights is not None and sub and max(b for ws in weights for b, _ in ws) < len(sub):
        named = [[[bones[sub[b]][0], w] for b, w in ws] for ws in weights]
    res = {"source": path, "points": pts, "faces": faces, "uvs": uvs, "weights": named,
           "skeleton": bones, "subskeleton": sub}
    open(out, "wb").write(json.dumps(res).encode())
    print("%s: %d verts, %d faces (at %s), uvs=%s, weights=%s, skeleton=%d bones, subskeleton=%s" % (
        path, n, len(faces), hex(fo[0]) if fo else None, None if uvs is None else len(uvs),
        None if named is None else len(named), len(bones), None if sub is None else len(sub)))


def read_uvs(d, n, pos_off):
    """UV set 0 sits right before the positions: f32 minU, minV, maxU, maxV, u32 n, u8 fill, LZO(n x 2 x i16),
    then a u32 (1) and the positions' count. Dequantised as min + (s + 32767) / 65534 * (max - min)."""
    for o in range(pos_off - 8, max(0, pos_off - 60000), -1):
        if struct.unpack_from("<I", d, o)[0] != n:
            continue
        try:
            if d[o + 4]:
                continue
            raw, used = decompress(d, o + 5, n * 4)
        except (LzoError, IndexError):
            continue
        if o + 5 + used != pos_off - 4:
            continue
        mnu, mnv, mxu, mxv = struct.unpack_from("<4f", d, o - 16)
        out = []
        for i in range(n):
            su, sv = struct.unpack_from("<hh", raw, 4 * i)
            out.append([mnu + (su + 32767) / 65534.0 * (mxu - mnu), mnv + (sv + 32767) / 65534.0 * (mxv - mnv)])
        return out
    return None


if __name__ == "__main__":
    main(sys.argv[1:])
