"""W2C time logger: python spikes/W2C/log.py EVENT NAME TAG FIVEH WK
Appends one LF line to TIMELOG_W2C.md with the system clock time."""
import sys, datetime, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_W2C.md')
ev, name, tag, h5, wk = sys.argv[1:6]
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
h5 = h5 if h5 == 'n/a' else h5 + '%'
wk = wk if wk == 'n/a' else wk + '%'
line = f'{ts} | {ev} | {name} | {tag} | 5h {h5} wk {wk}\n'
with open(p, 'ab') as f:
    f.write(line.encode('utf-8'))
print(line, end='')
