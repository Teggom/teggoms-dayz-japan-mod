"""K3 time logger: python tlog.py <event> <name> <tag> <usage>  (appends one LF line)."""
import sys, datetime, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_K3.md')
ev, name, tag, use = (sys.argv[1:] + ['', '', '', 'n/a'])[:4]
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
line = '%s | %s | %s | %s | %s\n' % (ts, ev, name, tag, use)
with open(os.path.normpath(P), 'ab') as f:
    f.write(line.encode('utf-8'))
print(line, end='')
