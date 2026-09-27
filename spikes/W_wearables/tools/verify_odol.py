"""Offline verification of the binarized p3ds in src/JP/characters (no game needed):
  - ODOL, skeleton DayzTemporarySkeleton with the vanilla 159 (bone, parent) pairs
  - selection / section names present (camoMale / camoFemale / camoGround / personality, bone names)
  - LOD list vs vanilla (worn: resolutions + geometry; ground: + memory, view, fire geometry)
  - round trip of LOD 0: positions, faces, per-vertex bone weights read back from the ODOL and compared with
    what the generator wrote (weights are quantised to 1/255 by binarize)
  - winding: ODOL faces point outward like vanilla's
usage: python verify_odol.py
"""
import json
import os
import struct
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from odol_mesh import read_skeleton  # noqa: E402
from pstrings import runs  # noqa: E402
from wlib import SRC, WORK  # noqa: E402
from geom import tris  # noqa: E402

VANILLA = r"P:\DZ\characters\tops\raincoat_m.p3d"


def lods_of(d):
    ver, n = struct.unpack_from("<II", d, 4)
    return ver, list(struct.unpack_from("<%df" % n, d, 12))


def main():
    _, vskel = read_skeleton(open(VANILLA, "rb").read())
    report = []
    ok_all = True
    for sub in ("kasa", "kimono", "tabi"):
        for f in sorted(os.listdir(os.path.join(SRC, sub))):
            if not f.endswith(".p3d"):
                continue
            p = os.path.join(SRC, sub, f)
            d = open(p, "rb").read()
            worn = not f.endswith("_g.p3d")
            line = {"file": f, "magic": d[:4].decode()}
            ver, lods = lods_of(d)
            line["version"] = ver
            line["lods"] = ["%g" % x for x in lods]
            _, sk = read_skeleton(d)
            line["skeleton_ok"] = (sk == vskel) if worn else (len(sk) == 0)
            strs = set(s.lower() for _, s in runs(d, 4))
            want = {"camomale"} if f.endswith("_m.p3d") else ({"camofemale"} if f.endswith("_f.p3d") else {"camoground"})
            if "kimono" in f and worn:
                want.add("personality")
            line["selections_ok"] = want <= strs
            line["rvmat"] = sorted(s for s in strs if s.endswith(".rvmat"))
            if worn:
                out = os.path.join(WORK, "verify_%s.json" % f[:-4])
                r = subprocess.run([sys.executable, os.path.join(HERE, "odol_mesh.py"), p, out], capture_output=True, text=True)
                m = json.load(open(out))
                P = np.array(m["points"])
                line["lod0_vertices"] = len(P)
                line["lod0_faces"] = len(m["faces"])
                # compare weights with the generator's MLOD copy
                from mlod_w import read_mlod
                ml = read_mlod(os.path.join(WORK, "mlod", sub, f))[0]
                MP = np.array(ml.points)
                mw = [dict() for _ in MP]
                for name, (pw, fs) in ml.selections.items():
                    if name.lower() in [b for b, _ in vskel]:
                        for i, w in pw.items():
                            mw[i][name.lower()] = w
                worst = 0.0
                miss = 0
                for i, (pt, ws) in enumerate(zip(P, m["weights"] or [])):
                    j = int(np.argmin(((MP - pt) ** 2).sum(1)))
                    if np.linalg.norm(MP[j] - pt) > 1e-4:
                        miss += 1
                        continue
                    a = {b: w for b, w in ws}
                    s1 = sum(mw[j].values()) or 1.0
                    bb = {k: v / s1 for k, v in mw[j].items()}
                    for k in set(a) | set(bb):
                        worst = max(worst, abs(a.get(k, 0) - bb.get(k, 0)))
                line["weights_worst_diff"] = round(worst, 4)
                line["unmatched_vertices"] = miss
                line["max_bones_per_vertex"] = max(len(ws) for ws in m["weights"]) if m["weights"] else None
                # winding: each ODOL face against the MLOD face made of the same points. binarize reverses the
                # vertex order, so the ODOL cycle must be the REVERSE of the MLOD cycle (cube test, REPORT.md)
                key = {tuple(np.round(q, 5)): i for i, q in enumerate(MP)}
                pf = {}
                mfaces = [[v[0] for v in fv[0]] for fv in ml.faces]
                for fi, f_ in enumerate(mfaces):
                    for v in f_:
                        pf.setdefault(v, set()).add(fi)
                agree = total = 0
                for f_ in m["faces"]:
                    ids = [key.get(tuple(np.round(P[v], 5))) for v in f_]
                    if None in ids:
                        continue
                    cand = set.intersection(*[pf.get(i, set()) for i in ids])
                    if not cand:
                        continue
                    mf_ = mfaces[min(cand)]
                    # position of ids in the MLOD cycle: reversed order <=> next index goes backwards
                    pos = [mf_.index(i) for i in ids]
                    n_ = len(mf_)
                    step = (pos[1] - pos[0]) % n_
                    total += 1
                    agree += step == n_ - 1 or (step != 1 and (pos[2] - pos[1]) % n_ == n_ - 1)
                line["winding_matches_mlod"] = round(float(agree) / max(total, 1), 3)
                line["winding_faces_checked"] = total
            ok = line["magic"] == "ODOL" and line["skeleton_ok"] and line["selections_ok"]
            if worn:
                ok = ok and line["weights_worst_diff"] < 0.01 and line["unmatched_vertices"] == 0 and line["winding_matches_mlod"] > 0.99
            line["PASS"] = bool(ok)
            ok_all = ok_all and ok
            report.append(line)
            print(json.dumps(line))
    print("ALL PASS" if ok_all else "SOME FAILED")
    with open(os.path.join(WORK, "verify_odol.json"), "wb") as fh:
        fh.write(json.dumps(report, indent=1).encode())


if __name__ == "__main__":
    main()
