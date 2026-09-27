"""Offline checks of the binarized world against its 8WVR source.

    python verify_oprw.py [<8wvr> <oprw>]      (defaults: the build_world.py outputs)

Checks: OPRW header (signature, version, land/terrain grid, cell size), the model table vs the 8WVR's models,
the rvmat list vs the 8WVR's materials, and that every non-road 8WVR object is present in the OPRW object
records with an identical transform. Road parts are stored by binarize in the road network, not the object
array, so they are only looked for by exact position anywhere in the file.
"""
import os
import struct
import sys
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wrp8  # noqa: E402

DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def main(argv):
    src = argv[0] if argv else os.path.join(DEV, "src", "JP", "worlds", "testisland", "world", "japantestisland.wrp")
    out = argv[1] if len(argv) > 1 else os.path.join(DEV, "data", "T_terrain", "bin", "world", "japantestisland.wrp")
    w = wrp8.read_8wvr(src)
    info = wrp8.read_oprw_summary(out)
    d = open(out, "rb").read()
    ok = True
    print("8WVR : land %s terrain %s cell %.1f, %d materials, %d objects" % (w["land"], w["terrain"], w["cell"], len(w["names"]), len(w["objects"]) - 1))
    print("OPRW : %s v%s tag %r appId %s land %s terrain %s cell %.1f, %d bytes" % (
        info["sig"], info.get("version"), info.get("tag"), info.get("appid"), info.get("land"), info.get("terrain"), info.get("cell", 0), info["size"]))
    if info.get("land") != w["land"] or info.get("terrain") != w["terrain"] or abs(info.get("cell", 0) - w["cell"]) > 1e-4:
        print("FAIL header mismatch")
        ok = False
    src_models = Counter(o[2].lower() for o in w["objects"][:-1])
    oprw_models = [m.lower() for m in info["models"]]
    missing = [m for m in src_models if m not in oprw_models]
    print("models: %d distinct in 8WVR, %d in OPRW table%s" % (len(src_models), len(oprw_models), (", MISSING " + str(missing)) if missing else ""))
    ok &= not missing
    mats = set(n.lower() for n in w["names"] if n)
    got = set(r.lower() for r in info["rvmats"])
    print("rvmats: %d in 8WVR, %d found in OPRW, missing %d" % (len(mats), len(mats & got), len(mats - got)))
    ok &= not (mats - got)
    # objects: exact transform match
    arr = wrp8.oprw_objects(d, len(info["models"]), info.get("models_end", 0), min_run=10)
    keyed = {}
    if arr is not None:
        for r in arr:
            keyed[tuple(np.round(r["m"][9:12], 3))] = (int(r["mi"]), r["m"])
    n_obj = n_match = n_road = n_road_found = 0
    worst = 0.0
    for m, oid, name in w["objects"][:-1]:
        if "\\roads\\parts\\" in name.lower():
            n_road += 1
            if d.find(struct.pack("<3f", *m[9:12])) >= 0:
                n_road_found += 1
            continue
        n_obj += 1
        k = tuple(np.round(np.array(m[9:12], np.float32), 3))
        if k in keyed:
            mi, mm = keyed[k]
            if oprw_models[mi] == name.lower():
                n_match += 1
                worst = max(worst, float(np.max(np.abs(np.array(m, np.float32) - mm))))
    print("objects: %d/%d non-road objects found with the same model and transform (max abs diff %.2g); "
          "%d/%d road parts found by position" % (n_match, n_obj, worst, n_road_found, n_road))
    ok &= n_match == n_obj and n_road_found == n_road
    print("VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
