"""Bounding-centre lookup for p3d models, needed to place objects in an 8WVR.

Terrain Builder writes an object's position as the position of the model's BINARIZED origin, which binarize
moves to the ODOL boundingCenter (autocenter). So an object whose MLOD origin should sit at ground height g
gets y = g + scale * boundingCenter.y (and x/z shifted by the rotated boundingCenter.x/z). Checked on
Bohemia's Test_Terrain utes.wrp: 30 of 30 non-rock vanilla models match to < 0.05 m.

ODOL (DayZ, version 54 on every vanilla p3d checked): "ODOL", int version, int nLods, float res[nLods],
then ModelInfo: bboxMin at +0x30, bboxMax at +0x3C, boundingCenter at +0x60.

MLOD (source) models: binarize computes the centre itself. autocenter=0 in the geometry LOD's named
properties keeps it at the origin; otherwise it is the centre of the bounding box of the points of EVERY LOD,
memory LOD included (tools/bc_experiment.py, 2026-09-26: 4 of 4 test MLODs matched rule 'all' exactly,
'visual' and 'geometry' only rules each failed).
"""
import os
import struct


def odol_info(path):
    with open(path, "rb") as f:
        d = f.read(4096)
    if d[:4] != b"ODOL":
        return None
    ver, nl = struct.unpack_from("<2i", d, 4)
    mi = 12 + 4 * nl
    return {
        "ver": ver,
        "nlods": nl,
        "res": struct.unpack_from("<%df" % nl, d, 12),
        "bmin": struct.unpack_from("<3f", d, mi + 0x30),
        "bmax": struct.unpack_from("<3f", d, mi + 0x3C),
        "bc": struct.unpack_from("<3f", d, mi + 0x60),
    }


def mlod_center(path, which="all"):
    """Bounding-box centre of an MLOD p3d (x, y, z) and whether autocenter=0 is set.

    which: 'all' = every LOD (what binarize does), 'visual' = resolution LODs (< 1e4) only,
           'geometry' = LOD 1e13 only (the last two only exist for the experiment)."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools", "common"))
    import mlod  # noqa: E402  (japan_dev/tools/common/mlod.py, read-only)
    lods = mlod.read_mlod(path)
    autocenter = True
    pts = []
    for lod in lods:
        for k, v in lod.properties.items():
            if k.lower() == "autocenter" and str(v).strip() == "0":
                autocenter = False
        r = lod.resolution
        if which == "visual" and r >= 1e4:
            continue
        if which == "geometry" and abs(r - 1e13) > 1e9:
            continue
        pts.extend(lod.points)
    if not pts:
        return (0.0, 0.0, 0.0), autocenter
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    zs = [p[2] for p in pts]
    c = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2)
    return c, autocenter


def model_center(path, mlod_rule="all"):
    """(bc, kind) for any p3d on disk: kind = 'odol', 'mlod', 'mlod-noautocenter' or None if missing."""
    if not os.path.isfile(path):
        return None, None
    info = odol_info(path)
    if info:
        return info["bc"], "odol"
    with open(path, "rb") as f:
        head = f.read(4)
    if head == b"MLOD":
        c, auto = mlod_center(path, mlod_rule)
        if not auto:
            return (0.0, 0.0, 0.0), "mlod-noautocenter"
        return c, "mlod"
    return None, None
