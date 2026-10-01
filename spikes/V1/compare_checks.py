"""V1: compare checks files of two snapshots (data/V1/eq/<a> vs <b>): per building pass/fail, number of checks and
every check's (name, ok, detail) text.  python spikes/V1/compare_checks.py <a> <b>"""
import json
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def load(tag, k):
    p = os.path.join(DEV, "data", "V1", "eq", tag, k)
    with open(p, "rb") as f:
        d = f.read()
    return json.loads(d.decode("utf-8")) if d else None


def main(a, b):
    keys = sorted(os.listdir(os.path.join(DEV, "data", "V1", "eq", a)))
    same = bytes_same = 0
    diffs = []
    nchecks = 0
    for k in keys:
        A, B = load(a, k), load(b, k)
        if A is None or B is None:
            diffs.append((k, "missing in %s" % (a if A is None else b)))
            continue
        ca, cb = A.get("checks", []), B.get("checks", [])
        nchecks += len(ca)
        ta = [(r["check"], r["ok"], r["detail"]) for r in ca]
        tb = [(r["check"], r["ok"], r["detail"]) for r in cb]
        with open(os.path.join(DEV, "data", "V1", "eq", a, k), "rb") as f1, \
                open(os.path.join(DEV, "data", "V1", "eq", b, k), "rb") as f2:
            bytes_same += f1.read() == f2.read()
        if ta == tb:
            same += 1
            continue
        d = [(x, y) for x, y in zip(ta, tb) if x != y]
        diffs.append((k, "%d vs %d checks; %d differ; first: %s" % (len(ta), len(tb), len(d), d[:2])))
    print("%s vs %s: %d buildings, %d checks; identical results %d, byte-identical files %d, different %d" % (
        a, b, len(keys), nchecks, same, bytes_same, len(diffs)))
    for k, why in diffs:
        print("  DIFF %s: %s" % (k, why[:600]))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
