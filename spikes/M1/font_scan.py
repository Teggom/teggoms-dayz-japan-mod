"""M1: scan font files for Siddham coverage (U+11580..U+115FF) with a minimal cmap reader (no fontTools here).

usage: python font_scan.py <dir> [<dir> ...]   prints every font that maps any Siddham code point.
"""
import os
import struct
import sys

LO, HI = 0x11580, 0x115FF


def cmap_cps(data, off):
    """Code points in [LO, HI] mapped by the font at table-directory offset `off`."""
    num = struct.unpack(">H", data[off + 4:off + 6])[0]
    cmap = None
    for i in range(num):
        tag, _, toff, _ = struct.unpack(">4sIII", data[off + 12 + 16 * i:off + 28 + 16 * i])
        if tag == b"cmap":
            cmap = toff
    if cmap is None:
        return set()
    n = struct.unpack(">H", data[cmap + 2:cmap + 4])[0]
    found = set()
    for i in range(n):
        pid, eid, so = struct.unpack(">HHI", data[cmap + 4 + 8 * i:cmap + 12 + 8 * i])
        st = cmap + so
        fmt = struct.unpack(">H", data[st:st + 2])[0]
        if fmt == 12:
            ng = struct.unpack(">I", data[st + 12:st + 16])[0]
            for g in range(ng):
                a, b, gid = struct.unpack(">III", data[st + 16 + 12 * g:st + 28 + 12 * g])
                if b >= LO and a <= HI:
                    found |= set(range(max(a, LO), min(b, HI) + 1))
    return found


def scan(path):
    data = open(path, "rb").read()
    offs = [0]
    if data[:4] == b"ttcf":
        k = struct.unpack(">I", data[8:12])[0]
        offs = list(struct.unpack(">%dI" % k, data[12:12 + 4 * k]))
    out = set()
    for o in offs:
        try:
            out |= cmap_cps(data, o)
        except Exception:
            pass
    return out


def main():
    n = 0
    for d in sys.argv[1:]:
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith((".ttf", ".otf", ".ttc")):
                    p = os.path.join(root, f)
                    n += 1
                    try:
                        cps = scan(p)
                    except Exception as e:
                        continue
                    if cps:
                        print("SIDDHAM %d code points: %s" % (len(cps), p))
    print("fonts scanned: %d" % n)


if __name__ == "__main__":
    main()
