#!/usr/bin/env python3
"""odoldiff.py - compare working-tree ODOLs / MLOD masters in src/JP/site with git HEAD: how many changed, and by how
many bytes (separates real geometry changes from binarize noise). python odoldiff.py [folder ...]"""
import glob
import os
import subprocess
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def head_blob(rel):
    r = subprocess.run(["git", "show", "HEAD:" + rel.replace("\\", "/")], cwd=DEV, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main(folders):
    folders = folders or ["src/JP/site"]
    same = changed = new = 0
    rows = []
    for fo in folders:
        for p in sorted(glob.glob(os.path.join(DEV, fo, "**", "*.p3d"), recursive=True)):
            rel = os.path.relpath(p, DEV)
            a = head_blob(rel)
            b = open(p, "rb").read()
            if a is None:
                new += 1
                continue
            if a == b:
                same += 1
                continue
            changed += 1
            nd = sum(1 for i in range(min(len(a), len(b))) if a[i] != b[i]) + abs(len(a) - len(b))
            rows.append((rel, len(a), len(b), nd))
    for r in rows[:12]:
        print("%-70s %8d %8d  bytes differing %d" % r)
    print("same %d, changed %d, new %d" % (same, changed, new))


if __name__ == "__main__":
    main(sys.argv[1:])
