r"""verify_all.py - the checks of every shipped building (or the given ones), through the check cache (V1, 2026-10-01).

  python buildings/verify_all.py [--jobs N] [--full] [--family NAME] [key ...]

  --jobs N        worker processes, default 4, at most 4 (README rule 2b)
  --full          ignore the check cache: run every building's checks (fresh passes are stored)
  --family NAME   every registered building whose dir is NAME
  key ...         these buildings only (default: every shipped building)

Builds nothing into src and combines nothing: each building that runs is built in memory + out/ and checked (as
pipeline.py --verify-only), so its config.cpp class, model.cfg, CE group and ODOL must come from an earlier full build.
Buildings whose cached pass is still valid (buildings/checkcache.py: registry entry, source of every module they
import, data files they read) are not run: "RESULT <key>: PASS (...) [cached]". Prints a per-family summary.
Exit 0 when every building passes.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import pipeline as P  # noqa: E402
import registry  # noqa: E402


def main(argv):
    if any(a in ("-h", "--help", "/?") for a in argv):
        print(__doc__)
        return 0
    jobs, full, fam, keys = P.MAX_JOBS, False, None, []
    it = iter(argv)
    for a in it:
        if a == "--jobs":
            jobs = int(next(it))
        elif a == "--full":
            full = True
        elif a == "--family":
            fam = next(it)
        elif a.startswith("-"):
            print("verify_all.py: unknown option %s (see --help)" % a)
            return 2
        else:
            keys.append(a)
    if fam:
        keys += [b["key"] for b in registry.BUILDINGS if b.get("dir", b["key"]) == fam]
    keys = keys or [b["key"] for b in registry.BUILDINGS if b["ship"]]
    jobs = max(1, min(jobs, P.MAX_JOBS))
    ok, res = P.verify_parallel(keys, jobs, full)
    fams = {}
    for k in keys:
        b = registry.get(k)
        a = fams.setdefault(b.get("dir", b["key"]), [0, 0, 0, 0, 0])
        v = res.get(k)
        a[0] += 1
        if v:
            a[1] += v[0] == "PASS"
            a[2] += v[1]
            a[3] += v[2]
            a[4] += v[3]
    for d, a in sorted(fams.items()):
        print("%-28s %3d buildings, %3d pass (%3d cached), %5d checks, %d failures" % (d, a[0], a[1], a[4], a[2], a[3]))
    print("buildings with results: %d / %d" % (sum(1 for k in keys if k in res), len(keys)))
    for k in keys:
        v = res.get(k)
        if not v or v[0] != "PASS":
            print("FAIL", k, v)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
