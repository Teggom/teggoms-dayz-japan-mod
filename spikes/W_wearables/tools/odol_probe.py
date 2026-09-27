"""Probe a binarized (ODOL) p3d for LZO-compressed float3 arrays (vertex positions) without a full parser.

usage: python odol_probe.py file.p3d [--dump out_prefix]

Method: every u32 N (30..60000) that occurs >= 3 times in the file is a candidate array length (vertices,
normals, UVs, clip flags and bone refs of one LOD all share N). At each occurrence, try to LZO-decompress
N*12 bytes right after it; keep the ones whose floats all look like model-space positions.
"""
import struct
import sys
from collections import Counter

from lzo import decompress, LzoError


def plausible_xyz(data):
    n = len(data) // 12
    bad = 0
    for i in range(n):
        x, y, z = struct.unpack_from("<3f", data, 12 * i)
        if not (abs(x) < 3 and abs(y) < 3 and abs(z) < 3) or x != x:
            bad += 1
    return bad == 0


def probe(path):
    d = open(path, "rb").read()
    cnt = Counter()
    offs = {}
    for o in range(0, len(d) - 4):
        v = struct.unpack_from("<I", d, o)[0]
        if 30 <= v <= 60000:
            cnt[v] += 1
            offs.setdefault(v, []).append(o)
    found = []
    for v, c in cnt.items():
        if c < 3:
            continue
        for o in offs[v]:
            size = v * 12
            if size < 1024:
                raw = d[o + 4:o + 4 + size]
                if len(raw) == size and plausible_xyz(raw):
                    found.append((o, v, "raw", raw, size))
                continue
            try:
                out, used = decompress(d, o + 4, size)
            except (LzoError, IndexError):
                continue
            if plausible_xyz(out):
                found.append((o, v, "lzo", out, used))
    return d, sorted(found, key=lambda f: f[0])


if __name__ == "__main__":
    d, found = probe(sys.argv[1])
    dump = sys.argv[sys.argv.index("--dump") + 1] if "--dump" in sys.argv else None
    for k, (o, v, kind, data, used) in enumerate(found):
        pts = [struct.unpack_from("<3f", data, 12 * i) for i in range(v)]
        lo = [min(p[a] for p in pts) for a in range(3)]
        hi = [max(p[a] for p in pts) for a in range(3)]
        print("#%d at %#x: N=%d %s (%d bytes in)  x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]" % (
            k, o, v, kind, used, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
        if dump:
            with open("%s_%d.xyz" % (dump, k), "wb") as f:
                f.write(data)
