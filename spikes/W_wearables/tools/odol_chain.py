"""Walk the compressed arrays that follow an ODOL LOD's vertex array, guessing element sizes.

usage: python odol_chain.py file.p3d vertex_array_offset(hex) [steps]
At each step: u32 count, then try element sizes; an LZO stream that ends exactly on its EOF marker with the
expected size is accepted (arrays under 1024 bytes are raw, so they are ambiguous - printed with all sizes).
"""
import struct
import sys

from lzo import decompress, LzoError

SIZES = [1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40]


def step(d, o):
    n = struct.unpack_from("<I", d, o)[0]
    res = []
    for s in SIZES:
        size = n * s
        if size == 0:
            res.append((s, "empty", 0, b""))
            continue
        if size < 1024:
            res.append((s, "raw", size, d[o + 4:o + 4 + size]))
            continue
        try:
            out, used = decompress(d, o + 4, size)
            res.append((s, "lzo", used, out))
        except (LzoError, IndexError):
            pass
    return n, res


if __name__ == "__main__":
    d = open(sys.argv[1], "rb").read()
    o = int(sys.argv[2], 16)
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    for k in range(steps):
        n, res = step(d, o)
        lzo = [r for r in res if r[1] == "lzo"]
        print("step %d at %#x: count=%d  lzo sizes=%s  raw candidates=%s" % (
            k, o, n, [(r[0], r[2]) for r in lzo], [r[0] for r in res if r[1] == "raw"][:4]))
        if lzo:
            s, _, used, out = lzo[0]
            print("   first bytes:", out[:48].hex(" "))
            o = o + 4 + used
        else:
            print("   next 48 bytes:", d[o:o + 48].hex(" "))
            break
