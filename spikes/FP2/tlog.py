"""FP2 time logger. Usage: python tlog.py "<event>" "<name>" "<tag>" "<5h%>" "<wk%>"
Appends one LF line to japan_dev/TIMELOG_FP2.md using the system clock."""
import sys, os, datetime
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_FP2.md')
a = sys.argv[1:] + [''] * 5
ev, name, tag, h5, wk = a[:5]
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
h5 = h5 or 'n/a'
wk = wk or 'n/a'
line = f"{ts} | {ev} | {name} | {tag} | 5h {h5}% wk {wk}%\n"
with open(LOG, 'ab') as f:
    f.write(line.encode('utf-8'))
print(line, end='')
