"""F1 time logger. Usage: python spikes/F1/log.py "<event>" <p5h> <pwk>
Appends '<timestamp> | <event> | F1 | G4-fixes | 5h <x>% wk <y>%' to TIMELOG_F1.md (LF, 'ab').
The timestamp comes from the system clock."""
import sys, os, datetime
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(root, 'TIMELOG_F1.md')
ev, p5, pw = sys.argv[1], sys.argv[2], sys.argv[3]
fmt = lambda p: p if p == 'n/a' else p + '%'
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
line = '%s | %s | F1 | G4-fixes | 5h %s wk %s\n' % (ts, ev, fmt(p5), fmt(pw))
new = not os.path.exists(path)
with open(path, 'ab') as f:
    if new:
        f.write(b'# TIMELOG F1 (G4 walk fixes)\n\n')
    f.write(line.encode('utf-8'))
print(line, end='')
