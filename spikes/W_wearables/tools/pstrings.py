"""Tiny `strings` replacement: print printable ASCII runs (>= n chars) from binary files, optionally filtered.

usage: python pstrings.py [-n 5] [-g REGEX] [-c] file...
  -c   count unique strings instead of listing them in order
"""
import re
import sys


def runs(data, n):
    for m in re.finditer(rb"[\x20-\x7e]{%d,}" % n, data):
        yield m.start(), m.group().decode("ascii")


def main(argv):
    n = 5
    rx = None
    count = False
    files = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-n":
            n = int(argv[i + 1]); i += 2; continue
        if a == "-g":
            rx = re.compile(argv[i + 1], re.I); i += 2; continue
        if a == "-c":
            count = True; i += 1; continue
        files.append(a); i += 1
    for f in files:
        data = open(f, "rb").read()
        seen = {}
        print("== %s (%d bytes, magic %r)" % (f, len(data), data[:4]))
        for off, s in runs(data, n):
            if rx and not rx.search(s):
                continue
            if count:
                seen[s] = seen.get(s, 0) + 1
            else:
                print("%8x  %s" % (off, s))
        if count:
            for s, c in sorted(seen.items()):
                print("%5d  %s" % (c, s))


if __name__ == "__main__":
    main(sys.argv[1:])
