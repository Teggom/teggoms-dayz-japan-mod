"""FX3 time logger: python tlog.py EVENT "5h x% wk y%"  (appends one LF line)."""
import sys, datetime, os
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_FX3.md')
ev = sys.argv[1]
usage = sys.argv[2] if len(sys.argv) > 2 else 'n/a'
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
line = f'{ts} | {ev} | FX3 | wood-texture-variety | {usage}\n'
with open(os.path.normpath(LOG), 'ab') as f:
    f.write(line.encode('utf-8'))
print(line, end='')
