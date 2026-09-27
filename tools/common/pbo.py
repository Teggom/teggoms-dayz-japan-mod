#!/usr/bin/env python3
"""Minimal PBO packer / unpacker for DayZ mods.

Usage:
  pbo.py list    <file.pbo> [--grep REGEX]
  pbo.py extract <file.pbo> <out_dir> [--grep REGEX]
  pbo.py pack    <src_dir> <out.pbo> --prefix <PboPrefix>

Files are stored uncompressed. The pack command writes the standard
product header entry (prefix=...), the file table, the data, and the
trailing SHA-1 checksum that the game expects.
"""
import hashlib
import os
import re
import struct
import sys
import time

PRODUCT_ENTRY = 0x56657273  # 'sreV'


def _read_cstr(f):
    out = bytearray()
    while True:
        c = f.read(1)
        if not c or c == b"\x00":
            return out.decode("latin-1")
        out += c


def read_header(f):
    """Return (properties, entries, data_start). entries = [(name, method, orig, ts, size)]."""
    props = {}
    entries = []
    while True:
        name = _read_cstr(f)
        method, orig, reserved, ts, size = struct.unpack("<5I", f.read(20))
        if name == "" and method == PRODUCT_ENTRY:
            while True:
                k = _read_cstr(f)
                if k == "":
                    break
                props[k] = _read_cstr(f)
            continue
        if name == "":
            break
        entries.append((name, method, orig, ts, size))
    return props, entries, f.tell()


def cmd_list(path, pattern=None):
    rx = re.compile(pattern, re.I) if pattern else None
    with open(path, "rb") as f:
        props, entries, _ = read_header(f)
    print("properties:", props)
    n = 0
    for name, method, orig, ts, size in entries:
        if rx and not rx.search(name.replace("\\", "/")):
            continue
        flag = "" if method == 0 else f" method={method:#x}"
        print(f"{size:>10}  {name}{flag}")
        n += 1
    print(f"{n} of {len(entries)} entries")


def cmd_extract(path, out_dir, pattern=None):
    rx = re.compile(pattern, re.I) if pattern else None
    with open(path, "rb") as f:
        props, entries, off = read_header(f)
        count = 0
        for name, method, orig, ts, size in entries:
            if not rx or rx.search(name.replace("\\", "/")):
                if method not in (0, PRODUCT_ENTRY) and method != 0x00000000:
                    print(f"skip compressed entry {name} (method {method:#x})")
                else:
                    f.seek(off)
                    data = f.read(size)
                    dest = os.path.join(out_dir, name.replace("\\", "/"))
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    with open(dest, "wb") as o:
                        o.write(data)
                    count += 1
            off += size
    print(f"extracted {count} files to {out_dir} (prefix={props.get('prefix', '')})")


def cmd_pack(src_dir, out_path, prefix):
    src_dir = os.path.abspath(src_dir)
    files = []
    for root, dirs, names in os.walk(src_dir):
        dirs.sort()
        for n in sorted(names):
            full = os.path.join(root, n)
            rel = os.path.relpath(full, src_dir).replace("/", "\\")
            if rel.lower() in ("$pboprefix$", "$pboprefix$.txt"):
                continue
            # Workbench-side sources and scratch files never need to ship (see ANIMATION_PIPELINE.md)
            if os.path.splitext(n)[1].lower() in (".fbx", ".meta", ".txo", ".txa", ".blend", ".blend1", ".log", ".png"):
                continue
            files.append((rel, full))
    body = bytearray()
    # product entry
    body += b"\x00" + struct.pack("<5I", PRODUCT_ENTRY, 0, 0, 0, 0)
    body += b"prefix\x00" + prefix.encode("latin-1") + b"\x00"
    body += b"\x00"
    # file table
    datas = []
    for rel, full in files:
        with open(full, "rb") as fh:
            data = fh.read()
        ts = int(os.path.getmtime(full)) or int(time.time())
        body += rel.encode("latin-1") + b"\x00" + struct.pack("<5I", 0, 0, 0, ts, len(data))
        datas.append(data)
    body += b"\x00" + struct.pack("<5I", 0, 0, 0, 0, 0)
    for d in datas:
        body += d
    digest = hashlib.sha1(bytes(body)).digest()
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "wb") as o:
        o.write(body)
        o.write(b"\x00")
        o.write(digest)
    print(f"packed {len(files)} files -> {out_path} (prefix={prefix}, {len(body)} bytes)")


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    cmd = argv[1]
    pattern = None
    prefix = None
    args = []
    i = 2
    while i < len(argv):
        if argv[i] == "--grep":
            pattern = argv[i + 1]
            i += 2
        elif argv[i] == "--prefix":
            prefix = argv[i + 1]
            i += 2
        else:
            args.append(argv[i])
            i += 1
    if cmd == "list":
        cmd_list(args[0], pattern)
    elif cmd == "extract":
        cmd_extract(args[0], args[1], pattern)
    elif cmd == "pack":
        if not prefix:
            print("pack needs --prefix")
            return 2
        cmd_pack(args[0], args[1], prefix)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
