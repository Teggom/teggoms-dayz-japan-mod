"""FP2: read a packed PBO and compare its files with the source tree (the PBO is what the game loads)."""
import os
import struct
import sys


def read_pbo(path):
    d = open(path, "rb").read()
    i, ents = 0, []
    while True:
        j = d.index(b"\0", i)
        name = d[i:j].decode("utf-8", "replace")
        mime, orig, res, ts, size = struct.unpack_from("<5I", d, j + 1)
        i = j + 21
        if not name:
            if mime == 0x56657273:                       # 'Vers' header: properties until an empty key
                while True:
                    k = d.index(b"\0", i)
                    key = d[i:k]
                    i = k + 1
                    if not key:
                        break
                    i = d.index(b"\0", i) + 1
                continue
            break
        ents.append((name, size))
    out, off = {}, i
    for name, size in ents:
        out[name.replace("\\", "/").lower()] = d[off:off + size]
        off += size
    return out


if __name__ == "__main__":
    pbo, src = sys.argv[1], sys.argv[2]
    files = read_pbo(pbo)
    p3d = [k for k in files if k.endswith(".p3d")]
    bad = 0
    for k in p3d:
        sp = os.path.join(src, k)
        if not os.path.isfile(sp) or open(sp, "rb").read() != files[k]:
            bad += 1
            if bad < 5:
                print("differs:", k)
    cfg = [k for k in files if k.startswith("config")]
    print(os.path.basename(pbo), "p3d", len(p3d), "differ from src", bad, "config:", cfg,
          "ODOL:", sum(1 for k in p3d if files[k][:4] == b"ODOL"))
