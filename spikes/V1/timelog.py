"""V1 time logger: append one line to TIMELOG_V1.md (binary append, LF).

usage: python timelog.py "<event>" "<name>" "<tag>" "<5h%>" "<wk%>"
"""
import datetime
import os
import sys

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "TIMELOG_V1.md")


def main():
    ev, name, tag, h5, wk = (sys.argv[1:] + ["n/a"] * 5)[:5]
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {ev} | {name} | {tag} | 5h {h5}% wk {wk}%\n"
    with open(os.path.normpath(LOG), "ab") as f:
        f.write(line.encode("utf-8"))
    sys.stdout.write(line)


if __name__ == "__main__":
    main()
