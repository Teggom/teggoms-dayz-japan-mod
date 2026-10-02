"""FX4's lathecheck on the W3B props (spikes/W3B/props_w3b.py): every closed lathe profile outward (no inside-out
surface).   python spikes/W3B/lathecheck_w3b.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [os.path.join(DEV, "spikes", "FX4"), HERE]
import lathecheck as LC  # noqa: E402  (patches fkit.lathe on import)
import build_w3b  # noqa: E402,F401
import props_w3b  # noqa: E402

n = 0
for p in props_w3b.PROPS:
    for md in p["models"]:
        md["build"]()
        n += 1
print("W3B models built: %d; closed lathes ok %d, open (not judged) %d" % (n, LC.OK[0], LC.OPEN[0]))
for k, v in sorted(LC.BAD.items()):
    print("  INSIDE-OUT %s x%d" % (k, v))
print("no inside-out lathe" if not LC.BAD else "FAIL")
sys.exit(1 if LC.BAD else 0)
