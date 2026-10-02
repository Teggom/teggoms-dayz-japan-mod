"""Append one line to TIMELOG_FX7.md.
usage: python tlog.py "<event>" "<name>" "<tag>" "<5h%>" "<wk%>"
"""
import sys, datetime, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_FX7.md')
ev, name, tag, h5, wk = (sys.argv[1:] + ['n/a'] * 5)[:5]
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
line = f"{ts} | {ev} | {name} | {tag} | 5h {h5}% wk {wk}%\n"
new = not os.path.exists(P)
with open(P, 'ab') as f:
    if new:
        f.write(b"# FX7 time log\n\n")
    f.write(line.encode('utf-8'))
print(line, end='')
