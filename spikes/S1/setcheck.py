#!/usr/bin/env python3
r"""setcheck.py - every S1 shop set on the two townhouse kinds it is defined for, at every abandoned level, through the
building pipeline's verify-only path (buildings/pipeline.py build_model(stage=False) + shellcheck: the shell checks +
decor D1-D16). Nothing is staged or shipped: temporary registry entries 's1v_<trade>_<kind>_ab<n>' live in this process
only, their MLODs and check files go to spikes/S1/_setcheck/.

  python spikes/S1/setcheck.py [trade ...] [--jobs N] [--ab 0,1,2] [--kinds 3k,2k]
  -> spikes/S1/setcheck.json {key: {pass, checks, fails: [...]}} and a one-line summary per key
Bases: 3k = th_kamigata_3k_middle_toril (toriniwa left), 2k = th_kamigata_2k_middle_torir (toriniwa right).
"""
import contextlib
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
TMP = os.path.join(HERE, "_setcheck")
BASES = {"3k": "th_kamigata_3k_middle_toril", "2k": "th_kamigata_2k_middle_torir"}


def worker(keys):
    for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"),
              os.path.join(DEV, "spikes", "B_building", "kit")):
        sys.path.insert(0, p)
    import registry
    import pipeline
    import furnishkit  # noqa: F401  (furnished_shells is furnishkit)
    sys.path.insert(0, os.path.join(DEV, "buildings", "furnished"))
    import furnished_shells  # noqa: F401
    real_bdir = pipeline.bdir

    def bdir(b):
        return TMP if b["key"].startswith("s1v_") else real_bdir(b)
    pipeline.bdir = bdir
    out = {}
    for key in keys:
        _, trade, kind, ab = key.split("|")
        k = "s1v_%s_%s_ab%s" % (trade, kind, ab)
        b = registry._furn(k, BASES[kind], "shop_%s_%s_ab%s" % (trade, kind, ab), "S1v", "set check")
        b["ship"] = False
        b["module"] = "furnished_shells"
        registry.BUILDINGS.append(b)
        buf = io.StringIO()
        err = None
        try:
            with contextlib.redirect_stdout(buf):
                pipeline.run_verify(pipeline.build_model(b, stage=False))
        except FileNotFoundError:
            pass            # shellcheck's last step reads the binarized ODOL in src: nothing is staged here
        except Exception as e:                                   # noqa: BLE001
            import traceback
            err = ["EXCEPTION %r" % e, traceback.format_exc().splitlines()[-3][:300]]
        lines = buf.getvalue().splitlines()
        # not set failures: the binarize check (nothing staged) and the config-class checks (the temporary class is in
        # no config.cpp)
        fails = [l for l in lines if l.startswith("FAIL") and "Binarize" not in l and "config Doors/" not in l
                 and "CE loot frame" not in l]
        n = sum(1 for l in lines if l.startswith(("OK", "FAIL")))
        if err:
            fails = err + fails
        out[k] = {"pass": not fails and n > 0, "checks": n, "fails": fails[:6]}
        print("%-36s %s %s" % (k, "PASS" if out[k]["pass"] else "FAIL", "; ".join(out[k]["fails"])[:400]),
              flush=True)
    return out


def main(argv):
    if "--worker" in argv:
        keys = json.load(open(argv[argv.index("--worker") + 1], encoding="utf-8"))
        res = worker(keys)
        dst = argv[argv.index("--worker") + 1] + ".out"
        with open(dst, "wb") as f:
            f.write(json.dumps(res, indent=1).encode("utf-8"))
        return 0
    jobs = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 6
    abs_ = argv[argv.index("--ab") + 1].split(",") if "--ab" in argv else ["0", "1", "2"]
    kinds = argv[argv.index("--kinds") + 1].split(",") if "--kinds" in argv else ["3k", "2k"]
    sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
    sys.path.insert(0, os.path.join(DEV, "buildings"))
    import shop_sets
    trades = [a for a in argv if not a.startswith("--") and a in shop_sets.TRADES] or list(shop_sets.TRADES)
    keys = ["k|%s|%s|%s" % (t, k, a) for t in trades for k in kinds for a in abs_]
    os.makedirs(TMP, exist_ok=True)
    procs = []
    for i in range(jobs):
        part = keys[i::jobs]
        if not part:
            continue
        jf = os.path.join(TMP, "_keys_%d.json" % i)
        with open(jf, "wb") as f:
            f.write(json.dumps(part).encode("utf-8"))
        procs.append((subprocess.Popen([sys.executable, os.path.abspath(__file__), "--worker", jf], cwd=DEV), jf))
    res = {}
    for p, jf in procs:
        p.wait()
        if os.path.isfile(jf + ".out"):
            res.update(json.load(open(jf + ".out", encoding="utf-8")))
    allp = os.path.join(HERE, "setcheck.json")
    old = json.load(open(allp, encoding="utf-8")) if os.path.isfile(allp) else {}
    old.update(res)
    with open(allp, "wb") as f:
        f.write(json.dumps(dict(sorted(old.items())), indent=1).encode("utf-8"))
    npass = sum(1 for v in res.values() if v["pass"])
    print("set checks: %d / %d pass (%d checks)" % (npass, len(res), sum(v["checks"] for v in res.values())))
    return 0 if npass == len(res) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
