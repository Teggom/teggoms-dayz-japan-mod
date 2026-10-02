"""FX6 gate-family check: FX1's handle check (fittings on their own leaf, hinge straps at the hinge edge, pulls in the
free half) on every new gate leaf, plus each gate's door count, clear width (D1) and head (D2).

  python spikes/FX6/gatecheck.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "spikes", "FX1"))
import handlecheck as HC  # noqa: E402
from jpparts import sitewall as W  # noqa: E402

KEN = 1.82
GATES = [("kido_kata itabei", lambda: W.gate_kido_kata(KEN, "itabei", leaf_y0=0.13)),
         ("kido_kata itabei kuro", lambda: W.gate_kido_kata(KEN, "itabei", kuro=True, leaf_y0=0.13)),
         ("kido_kata ikegaki", lambda: W.gate_kido_kata(KEN, "ikegaki", leaf_y0=0.13)),
         ("kido_ryo 1 ken", lambda: W.gate_kido_ryo(KEN, leaf_y0=0.13)),
         ("kido_ryo 1.5 ken kuro", lambda: W.gate_kido_ryo(1.5 * KEN, kuro=True, leaf_y0=0.13)),
         ("shiorido yotsume", lambda: W.gate_shiorido(KEN, "yotsume", leaf_y0=0.13)),
         ("opening yotsume", lambda: W.gate_opening(KEN, "yotsume")),
         ("opening itabei", lambda: W.gate_opening(KEN, "itabei")),
         # W3D (2026-10-02): the checkpoint's kora-mon (the picker's saku / high / front row)
         ("koraimon 1.5 ken", lambda: W.gate_koraimon(1.5 * KEN, leaf_y0=0.13))]


def main():
    nf = 0
    for label, fn in GATES:
        p = fn()
        n, f = HC.check(p, label)
        dims = {d["name"]: d.get("measured", d.get("value")) for d in getattr(p, "dims", []) if isinstance(d, dict)}
        bad = list(f)
        cw = dims.get("clear_open_m", dims.get("clear_m"))
        if cw is not None and float(cw) < 1.0 - 1e-6:
            bad.append("%s clear %.2f < 1.00 (D1)" % (label, float(cw)))
        if label.startswith("opening") and p.doors:
            bad.append("%s has a door" % label)
        if not label.startswith("opening") and not p.doors:
            bad.append("%s has no door" % label)
        print("%-24s doors %d  fittings %2d  clear %s  %s" % (label, len(p.doors), n, cw, "PASS" if not bad else "FAIL"))
        for b in bad:
            print("   " + b)
        nf += len(bad)
    print("GATECHECK: %d gates, %d failures" % (len(GATES), nf))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
