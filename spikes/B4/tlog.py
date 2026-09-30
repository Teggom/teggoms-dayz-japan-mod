"""B4 time logger: python spikes/B4/tlog.py "<event>" "<name>" "<tag>" <5h%> <wk%>
Takes the timestamp from the system clock; appends one LF line to TIMELOG_B4.md."""
import sys, datetime, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_B4.md')
ev, name, tag, h5, wk = sys.argv[1:6]
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
fmt = lambda v: 'n/a' if v == 'n/a' else v + '%'
line = f'{ts} | {ev} | {name} | {tag} | 5h {fmt(h5)} wk {fmt(wk)}\n'
with open(os.path.normpath(p), 'ab') as f:
    f.write(line.encode('utf-8'))
print(line, end='')
