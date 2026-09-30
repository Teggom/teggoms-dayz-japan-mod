"""B4: binarize ONLY the fittings props (kamidana, nagashi) that B4 added to B3a's pipeline (spikes/B3a/props_fittings.py)
and optionally pack jp_furniture.pbo, without re-binarizing B3a's other 110 models (binarize output is not byte-stable,
so a full run would churn every ODOL in git).
  python spikes/B4/build_fittings.py [--pack]
Run `python spikes/B3a/build.py kamidana nagashi --no-binarize` first (MLOD masters, sidecars, config.cpp)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
import build as B3  # noqa: E402

reg = B3.registry()
mine = [(p, m) for p, m in B3.built_models(reg) if p["cat"] == "fittings"]
ok, det = B3.binarize(mine)
print("fittings binarize:", ok, det)
if "--pack" in sys.argv:
    print("pack:", B3.pack())
sys.exit(0 if ok else 1)
