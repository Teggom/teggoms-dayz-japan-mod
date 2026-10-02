"""CA1 time logger: python tlog.py EVENT NAME TAG FIVEH WEEK
Appends one LF line to japan_dev/TIMELOG_CA1.md with the system clock."""
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.normpath(os.path.join(HERE, '..', '..', 'TIMELOG_CA1.md'))


def main(argv):
    ev, name, tag = argv[1], argv[2], argv[3]
    five = argv[4] if len(argv) > 4 else 'n/a'
    wk = argv[5] if len(argv) > 5 else 'n/a'
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = '%s | %s | %s | %s | 5h %s wk %s\n' % (ts, ev, name, tag, five, wk)
    with open(LOG, 'ab') as f:
        f.write(line.encode('utf-8'))
    sys.stdout.write(line)


if __name__ == '__main__':
    main(sys.argv)
