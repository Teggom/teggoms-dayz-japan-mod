#!/usr/bin/env python3
r"""verify.py - Land_JP_Machiya_T3_01_Shop (the B4 furnished pilot): the machiya's own 78 checks on this p3d (proxy
triangles stripped first; its config class, loot group and ODOL), then the decorator checks D1-D14
(parts/kit/jpparts/decor.check_all) with the furniture and the yard objects in. Writes checks.json here.

  python verify.py            (after `python buildings/pipeline.py machiya_t3_01_shop`)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "buildings", "machiya_t3_01"))
import machiya_t3_01_shop as MS  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("machiya_verify", os.path.join(DEV, "buildings", "machiya_t3_01",
                                                                               "verify.py"))
MV = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MV)
from jpparts import decor as DC  # noqa: E402


def run(M=None, floors=None, pts=None):
    if M is None:
        M, floors, _ = MS.model()
    if pts is None:
        pts = MS.loot_points(floors)

    def extra(M_, L, floors_, pts_, rec, raw):
        DC.check_all(MS.D, M_, L, pts_, rec, door_fn=lambda d, gc: MV.door_world(d, gc), extra_openings=MS.EXTRA_OPENINGS,
                     fixed_band=MS.FIXED_BAND, site_bounds=MS.SITE_BOUNDS, mlod_lods=raw)
    return MV.run(M, floors, pts, name=MS.NAME, cls=MS.CLASS, here=HERE, extra=extra)


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
