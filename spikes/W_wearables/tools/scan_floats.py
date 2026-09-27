"""Heuristic scan of a binary file for runs of plausible float3 vertex positions (character-sized).

usage: python scan_floats.py file [minrun]
Prints runs of consecutive 12-byte (x, y, z) float triples with |x|<1.2, -0.1<y<2.2, |z|<1.0 and not all ~0,
tried at every 4-byte alignment.
"""
import struct
import sys


def plausible(x, y, z):
    if x != x or y != y or z != z:
        return False
    if not (abs(x) < 1.2 and -0.1 < y < 2.2 and abs(z) < 1.0):
        return False
    if abs(x) < 1e-6 and abs(y) < 1e-6 and abs(z) < 1e-6:
        return False
    # reject denormal-ish garbage
    for v in (x, y, z):
        if v != 0.0 and abs(v) < 1e-5:
            return False
    return True


def scan(data, minrun):
    out = []
    n = len(data)
    for align in range(0, 12, 4):
        off = align
        run_start = None
        cnt = 0
        while off + 12 <= n:
            x, y, z = struct.unpack_from("<3f", data, off)
            if plausible(x, y, z):
                if run_start is None:
                    run_start = off
                    cnt = 0
                cnt += 1
            else:
                if run_start is not None and cnt >= minrun:
                    out.append((run_start, cnt))
                run_start = None
            off += 12
        if run_start is not None and cnt >= minrun:
            out.append((run_start, cnt))
    out.sort()
    return out


if __name__ == "__main__":
    data = open(sys.argv[1], "rb").read()
    minrun = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    for s, c in scan(data, minrun):
        xs = [struct.unpack_from("<3f", data, s + 12 * i) for i in range(c)]
        lo = [min(p[k] for p in xs) for k in range(3)]
        hi = [max(p[k] for p in xs) for k in range(3)]
        print("run at %#x: %d triples  x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]" % (s, c, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
