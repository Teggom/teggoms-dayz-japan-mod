"""W3 time logger. Usage: python tlog.py "<event>" "<name>" "<tag>" <5h%> <wk%>
Appends one LF line to japan_dev/TIMELOG_W3.md with the system clock time."""
import sys, datetime, os

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'TIMELOG_W3.md')


def main():
    ev, name, tag, h5, wk = (sys.argv[1:] + ['', '', '', 'n/a', 'n/a'])[:5]
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fmt = lambda v: v if v == 'n/a' or v.endswith('%') else v + '%'
    line = '%s | %s | %s | %s | 5h %s wk %s\n' % (ts, ev, name, tag, fmt(h5), fmt(wk))
    new = not os.path.exists(LOG)
    with open(LOG, 'ab') as f:
        if new:
            f.write(b'# TIMELOG W3 (more wooden grave posts)\n\n')
        f.write(line.encode('utf-8'))
    sys.stdout.write(line)


if __name__ == '__main__':
    main()
