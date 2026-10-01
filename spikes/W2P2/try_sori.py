"""Quick offline test of jpparts.sori: build roofs, write MLOD to the scratch dir, run the part checks + counts."""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "parts", "kit"))
sys.path.insert(0, KIT)
from jpparts import sori, checks, mlod, core  # noqa: E402
from jpparts.core import Part, KEN  # noqa: E402

OUT = os.path.join(HERE, "_try")


def run(name, **kw):
    t = time.time()
    p = Part("try_" + name, "", "roof")
    sls, info = sori.roof(p, **kw)
    path = os.path.join(OUT, name + ".p3d")
    p.write(path)
    lods = mlod.read_mlod(path)
    res, counts = checks.check_part(p, path, lods)
    bad = [r for r in res if not r[1]]
    print("%-18s %5.1fs %s" % (name, time.time() - t, {k[:12]: v for k, v in counts.items()}))
    print("   eave %.2f ridge %.2f sag %.3f Ls %.2f" % (info["eave_y"], info["y_ridge"], info["curve_depth_m"], info["Ls"]))
    for r in bad:
        print("   FAIL", r[0], r[2][:200])
    return p, info


if __name__ == "__main__":
    which = sys.argv[1:] or ["iri_hon"]
    cases = {
        "iri_hon": dict(W=3 * 2.275, D=2 * 2.275, form="irimoya", covering="hongawara", bear_y=4.0, g_out=0.55),
        "iri_kok": dict(W=3 * 2.275, D=2 * 2.275, form="irimoya", covering="kokera", bear_y=4.0, g_out=0.55),
        "kiri_hiw": dict(W=3 * KEN, D=2 * KEN, form="kirizuma", covering="hiwada", bear_y=3.2),
        "kiri_hon": dict(W=3 * KEN, D=2 * KEN, form="kirizuma", covering="hongawara", bear_y=3.2),
        "yose_cu": dict(W=2 * KEN, D=2 * KEN, form="yosemune", covering="copper", bear_y=3.2),
        "nagare": dict(W=2 * KEN, D=2 * KEN, form="nagare", covering="hiwada", bear_y=3.0, front_ext=KEN),
    }
    for w in which:
        run(w, **cases[w])
