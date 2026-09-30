"""L1 time logger. Usage: python tlog.py "<event>" "<name>" "<tag>" <5h%> <wk%>
Timestamp taken from the system clock at call time. Appends one LF line."""
import sys, datetime, os
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_L1.md')
ev, name, tag, h5, wk = (sys.argv[1:] + [''] * 5)[:5]
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
h5 = (h5 + '%') if h5 and h5 != 'n/a' else 'n/a'
wk = (wk + '%') if wk and wk != 'n/a' else 'n/a'
line = f"{ts} | {ev} | {name} | {tag} | 5h {h5} wk {wk}\n"
with open(os.path.normpath(LOG), 'ab') as f:
    f.write(line.encode('utf-8'))
print(line, end='')
