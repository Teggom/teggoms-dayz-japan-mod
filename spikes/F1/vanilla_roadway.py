"""Which vanilla furniture / misc p3ds (ODOL, D:\\DayZToolsExtract = P:) carry a Roadway LOD (3e15)? Reads the LOD
resolution table at the start of each ODOL: after 'ODOL', version (uint32), [v>=58: prefix string], lod count (uint32),
then that many float32 resolutions. Robust fallback: look for the float32 3e15 within the first 400 bytes.
  python spikes/F1/vanilla_roadway.py [folder ...]"""
import glob
import os
import struct
import sys

ROAD = struct.pack("<f", 3.0e15)
GEO = struct.pack("<f", 1.0e13)
folders = sys.argv[1:] or [r"P:\DZ\structures\furniture", r"P:\DZ\structures\residential\misc",
                           r"P:\DZ\structures_bliss\furniture"]
for fo in folders:
    fs = sorted(glob.glob(os.path.join(fo, "**", "*.p3d"), recursive=True))
    withr, without = [], []
    for f in fs:
        with open(f, "rb") as fh:
            head = fh.read(600)
        if head[:4] != b"ODOL":
            continue
        name = os.path.relpath(f, fo)
        (withr if ROAD in head else without).append((name, GEO in head))
    print("==", fo, "roadway:", len(withr), "no roadway:", len(without))
    for n, g in withr:
        print("  R ", n)
    for n, g in without:
        if g:
            print("  -G", n)
