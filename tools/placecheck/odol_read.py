# COPY of spikes/A_arms/tools/odol.py (2026-09-27, placecheck). Do not edit the original; fixes go here.
"""Read what we need out of a vanilla DayZ ODOL (binarized p3d, version 54): the ModelInfo box,
the LOD table, and per LOD the vertex positions, faces and named selections (memory points).

Worked out 2026-09-26 (spike A) on medieval_sword.p3d by hand, then checked on the spear and bows.
Layout (v54, all little-endian):

  'ODOL' u32 version(54) u32 nLods  f32 resolution[nLods]
  ModelInfo: u32 special, f32 bSphere, f32 geoSphere, u32 remarks/andHints/orHints, xyz aimingCenter,
             u32 colour, u32 colourType, f32 viewDensity, xyz bboxMin, xyz bboxMax, xyz bboxMinVisual,
             xyz bboxMaxVisual, xyz boundingCenter, xyz geometryCenter, xyz centerOfMass, xyz invInertia[3],
             u8 autoCenter, ...
  ... u32 lodStart[nLods] u32 lodEnd[nLods] (found by pattern: end[i] of one is start of the next;
      the LODs are stored in reverse order)
  per LOD:
    u32 nProxies, [proxies], u32 nSubSkel, [..], u32 nSkelToSub, [..], u32 vertexCount, f32 faceArea,
    u32 orHints, u32 andHints, xyz bMin, xyz bMax, xyz bCenter, f32 bRadius,
    u32 nTextures + asciiz[], u32 nMaterials + materials (skipped: not parsed, see below),
    compressed pointToVertex, vertexToPoint, u32 nFaces u32 faceAlloc u16 0, faces (u8 n, u16 idx[n]),
    u32 nSections + sections, u32 nNamedSel + (asciiz, carr faces, u32 0, u8 sectional, carr sections,
    carr u16 vertices, carr u8 weights), u32 nProps + (asciiz, asciiz), u32 nFrames, u32 col, u32 col,
    u32 special, u8 vbrSimple, u32 sizeOfRestData (counted from its own offset to the LOD end),
    rest: condensed clipFlags, f32 uvScale[4], condensed uv(u16 pairs), u32 nUVSets, [...],
          carr xyz vertices ...
  Compressed arrays: u32 count, then data; data of >= 1024 bytes is LZO1X compressed (Enfusion-era
  DayZ) - both LZSS and LZO are tried, the one giving the exact size wins.

Faces and named selections are found by pattern (robust, avoids parsing embedded materials).
"""
import re
import struct
import sys


# --------------------------------------------------------------------------- decompressors
def lzo1x_decompress(src, out_len):
    """LZO1X decompressor (pure python port of the reference lzo1x_decompress state machine).
    Returns (bytes, consumed)."""
    op = bytearray()
    ip = 0

    def copy_match(dist, n):
        pos = len(op) - dist
        if pos < 0:
            raise ValueError("lzo: distance out of range")
        for _ in range(n):
            op.append(op[pos])
            pos += 1

    def run_len(base):
        nonlocal ip
        t = 0
        while src[ip] == 0:
            t += 255
            ip += 1
        t += base + src[ip]
        ip += 1
        return t

    state = "loop"
    t = src[ip]
    if t > 17:
        ip += 1
        t -= 17
        op += src[ip:ip + t]
        ip += t
        state = "first_literal_run" if t >= 4 else "match_next"
        if state == "match_next":
            trailing = t
    while True:
        if state == "loop":
            t = src[ip]
            ip += 1
            if t >= 16:
                state = "match"
                continue
            if t == 0:
                t = run_len(15)
            op += src[ip:ip + t + 3]
            ip += t + 3
            state = "first_literal_run"
            continue
        if state == "first_literal_run":
            t = src[ip]
            ip += 1
            if t >= 16:
                state = "match"
                continue
            dist = 1 + 0x0800 + (t >> 2) + (src[ip] << 2)
            ip += 1
            copy_match(dist, 3)
            state = "match_done"
            continue
        if state == "match":
            if t >= 64:
                dist = 1 + ((t >> 2) & 7) + (src[ip] << 3)
                ip += 1
                n = (t >> 5) - 1
                copy_match(dist, n + 2)
            elif t >= 32:
                n = t & 31
                if n == 0:
                    n = run_len(31)
                v = src[ip] | (src[ip + 1] << 8)
                ip += 2
                copy_match(1 + (v >> 2), n + 2)
            elif t >= 16:
                dist = (t & 8) << 11
                n = t & 7
                if n == 0:
                    n = run_len(7)
                v = src[ip] | (src[ip + 1] << 8)
                ip += 2
                dist += v >> 2
                if dist == 0:
                    return bytes(op), ip
                dist += 0x4000
                copy_match(dist, n + 2)
            else:
                dist = 1 + (t >> 2) + (src[ip] << 2)
                ip += 1
                copy_match(dist, 2)
            state = "match_done"
            continue
        if state == "match_done":
            trailing = src[ip - 2] & 3
            if trailing == 0:
                state = "loop"
                continue
            state = "match_next"
            continue
        if state == "match_next":
            op += src[ip:ip + trailing]
            ip += trailing
            t = src[ip]
            ip += 1
            state = "match"
            continue


def lzss_decompress(src, out_len):
    dst = bytearray()
    ip = 0
    while len(dst) < out_len and ip < len(src):
        flags = src[ip]
        ip += 1
        for bit in range(8):
            if len(dst) >= out_len:
                break
            if flags & (1 << bit):
                dst.append(src[ip])
                ip += 1
            else:
                a, b = src[ip], src[ip + 1]
                ip += 2
                rpos = len(dst) - ((a | ((b & 0xF0) << 4)))
                rlen = (b & 0x0F) + 3
                for _ in range(rlen):
                    if rpos < 0:
                        dst.append(0x20)
                    else:
                        dst.append(dst[rpos])
                    rpos += 1
    ip += 4  # checksum
    return bytes(dst[:out_len]), ip


def read_compressed(d, o, elem):
    """u32 count + data; returns (bytes, new_offset)"""
    cnt = struct.unpack_from("<I", d, o)[0]
    o += 4
    size = cnt * elem
    if size < 1024:
        return d[o:o + size], o + size, cnt
    last_err = None
    for fn in (lzo1x_decompress, lzss_decompress):
        try:
            raw, used = fn(d[o:o + size + 64], size)
            if len(raw) == size:
                return raw, o + used, cnt
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise ValueError("cannot decompress array of %d x %d at %d (%s)" % (cnt, elem, o, last_err))


# --------------------------------------------------------------------------- model
class OdolLod:
    pass


def _cstr(d, o):
    e = d.index(b"\x00", o)
    return d[o:e].decode("latin-1"), e + 1


def read_odol(path):
    d = open(path, "rb").read()
    assert d[:4] == b"ODOL", "not ODOL"
    ver, n = struct.unpack_from("<II", d, 4)
    res = list(struct.unpack_from("<%df" % n, d, 12))
    mi = 12 + 4 * n
    f = struct.unpack_from("<42f", d, mi)
    info = {
        "version": ver,
        "resolutions": res,
        "bSphere": f[1],
        "bboxMin": f[12:15], "bboxMax": f[15:18],
        "bboxMinVisual": f[18:21], "bboxMaxVisual": f[21:24],
        "boundingCenter": f[24:27], "geometryCenter": f[27:30], "centerOfMass": f[30:33],
        "autoCenter": d[mi + 168],
    }
    L = len(d)
    table = None
    for o in range(mi, L - 8 * n):
        st = struct.unpack_from("<%dI" % (2 * n), d, o)
        s, e = st[:n], st[n:]
        if not (all(o < x <= L for x in st) and all(s[i] < e[i] for i in range(n)) and max(e) == L):
            continue
        # the LOD blocks must tile [min(start), L) exactly
        spans = sorted(zip(s, e))
        if all(spans[k][1] == spans[k + 1][0] for k in range(n - 1)) and spans[-1][1] == L:
            table = (o, list(s), list(e))
            break
    if not table:
        raise ValueError("LOD table not found")
    info["lod_table_at"] = table[0]
    lods = []
    for i in range(n):
        lod = OdolLod()
        lod.resolution = res[i]
        lod.start, lod.end = table[1][i], table[2][i]
        try:
            _parse_lod(d, lod)
        except Exception as ex:  # noqa: BLE001
            lod.error = str(ex)
            lod.vertexCount, lod.faces, lod.vertices, lod.selections, lod.textures = 0, [], None, {}, []
            lod.bMin = lod.bMax = (0.0, 0.0, 0.0)
        lods.append(lod)
    info["lods"] = lods
    return info


def _parse_lod(d, lod):
    s, e = lod.start, lod.end
    o = s
    nprox = struct.unpack_from("<I", d, o)[0]
    lod.nProxies = nprox
    # header after proxies: find vertexCount by the bbox pattern instead of parsing proxies
    # (proxy records are variable). Search: u32 vc, f32 area, u32, u32, 10 floats bbox.
    lod.vertexCount = None
    for p in range(o, min(e - 60, o + 200000)):
        vc = struct.unpack_from("<I", d, p)[0]
        if not (0 < vc < 200000):
            continue
        bmin = struct.unpack_from("<3f", d, p + 16)
        bmax = struct.unpack_from("<3f", d, p + 28)
        bc = struct.unpack_from("<3f", d, p + 40)
        br = struct.unpack_from("<f", d, p + 52)[0]
        ok = all(-50 < x < 50 for x in bmin + bmax + bc) and all(bmin[k] <= bmax[k] for k in range(3))
        ok = ok and 0 < br < 100 and all(abs(bc[k] - (bmin[k] + bmax[k]) / 2) < 1e-3 for k in range(3))
        ok = ok and max(bmax[k] - bmin[k] for k in range(3)) > 0.005 and vc < 100000
        if not ok:
            continue
        q = p + 56
        nt = struct.unpack_from("<I", d, q)[0]
        if nt > 64:
            continue
        q += 4
        texs = []
        good = True
        for _ in range(nt):
            try:
                t, q = _cstr(d, q)
            except ValueError:
                good = False
                break
            if len(t) > 200 or any(ord(c) < 32 or ord(c) > 126 for c in t):
                good = False
                break
            texs.append(t)
        if not good:
            continue
        lod.vertexCount = vc
        lod.bMin, lod.bMax, lod.bCenter, lod.bRadius = bmin, bmax, bc, br
        lod.hdr_end = p + 56
        lod.textures = texs
        o = q
        break
    if lod.vertexCount is None:
        raise ValueError("LOD header not found at %d" % s)
    # faces: find by pattern
    lod.faces = []
    vc = lod.vertexCount
    found = False
    for p in range(o, e - 10):
        nf, alloc, z = struct.unpack_from("<IIH", d, p)
        if not (0 < nf <= 200000) or z != 0 or alloc < nf * 8 or alloc > nf * 10:
            continue
        q = p + 10
        faces = []
        acc = 0
        good = True
        for _ in range(nf):
            if q >= e:
                good = False
                break
            k = d[q]
            if k not in (3, 4):
                good = False
                break
            idx = struct.unpack_from("<%dH" % k, d, q + 1)
            if max(idx) >= vc:
                good = False
                break
            faces.append(idx)
            q += 1 + 2 * k
            acc += 2 + 2 * k
        if good and acc == alloc:
            lod.faces = faces
            lod.faces_end = q
            found = True
            break
    if not found:
        lod.faces_end = o
    # named selections: pattern "asciiz name" followed by the selection record; collect vertex lists
    lod.selections = {}
    region = d[lod.faces_end:e]
    for m in re.finditer(rb"([a-z0-9_\-\.:\\]{2,80})\x00", region, re.I):
        name = m.group(1).decode("latin-1")
        q = lod.faces_end + m.end()
        try:
            cf = struct.unpack_from("<I", d, q)[0]
            if cf > 200000:
                continue
            _, q, _ = read_compressed(d, q, 2)
            z0 = struct.unpack_from("<I", d, q)[0]
            if z0 != 0:
                continue
            q += 4
            sect = d[q]
            if sect not in (0, 1):
                continue
            q += 1
            _, q, _ = read_compressed(d, q, 4)
            raw, q, cnt = read_compressed(d, q, 2)
            if cnt > vc:
                continue
            verts = list(struct.unpack_from("<%dH" % cnt, raw, 0)) if cnt else []
            if any(v >= vc for v in verts):
                continue
            lod.selections[name] = verts
        except Exception:  # noqa: BLE001
            continue
    # rest data: find u32 X at p with p + X == end, followed by condensed clip flags with count == vc
    lod.vertices = None
    for p in range(lod.faces_end, e - 8):
        x = struct.unpack_from("<I", d, p)[0]
        if p + x != e:
            continue
        q = p + 4
        cnt = struct.unpack_from("<I", d, q)[0]
        if cnt != vc:
            continue
        try:
            q = _skip_condensed(d, q, 4)
            q += 16  # uv scale
            q = _skip_condensed(d, q, 4)
            nuv = struct.unpack_from("<I", d, q)[0]
            q += 4
            for _ in range(max(0, nuv - 1)):
                q += 16
                q = _skip_condensed(d, q, 4)
            raw, q, c = read_compressed(d, q, 12)
            if c != vc:
                continue
            lod.vertices = [struct.unpack_from("<3f", raw, 12 * i) for i in range(c)]
            break
        except Exception:  # noqa: BLE001
            continue


def _skip_condensed(d, o, elem):
    cnt = struct.unpack_from("<I", d, o)[0]
    o += 4
    default = d[o]
    o += 1
    if default:
        return o + elem
    _, o2, _ = read_compressed(d, o - 4 - 1 + 0, elem) if False else (None, None, None)
    # non-default: plain compressed array body (no second count)
    size = cnt * elem
    if size < 1024:
        return o + size
    for fn in (lzo1x_decompress, lzss_decompress):
        try:
            raw, used = fn(d[o:o + size + 64], size)
            if len(raw) == size:
                return o + used
        except Exception:  # noqa: BLE001
            pass
    raise ValueError("condensed array decompress failed")


def summary(path):
    info = read_odol(path)
    print("%s  ODOL v%d  autoCenter=%d" % (path, info["version"], info["autoCenter"]))
    print("  bbox min %s max %s  boundingCenter %s" % (fmt(info["bboxMin"]), fmt(info["bboxMax"]), fmt(info["boundingCenter"])))
    for lod in info["lods"]:
        nv = len(lod.vertices) if lod.vertices else 0
        print("  LOD %-8g vc=%-5d faces=%-5d verts=%-5d box %s..%s tex=%s" % (
            lod.resolution, lod.vertexCount, len(lod.faces), nv, fmt(lod.bMin), fmt(lod.bMax), lod.textures[:2]))
        if lod.resolution >= 9e14 and lod.resolution < 2e15 and lod.vertices:
            for name, vs in lod.selections.items():
                pts = [lod.vertices[v] for v in vs]
                print("     %-26s %s" % (name, " ".join(fmt(p) for p in pts)))
    return info


def fmt(v):
    return "(%+.3f %+.3f %+.3f)" % tuple(v)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        summary(p)
