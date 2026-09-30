#!/usr/bin/env python3
r"""make_b3b_materials.py - the materials B3b (outdoor props, wave 1) ADDS to jp_common through B1's pipeline.

  python make_b3b_materials.py [--no-pack]

Adds only; never changes an existing material or palette entry. Uses make_b1_materials.make_one (same textures, PAAs,
rvmats, sidecar, C1 matcheck on PNG and shipped PAA) with its own maker and table entry, then repacks jp_common.pbo.
- jp_m_textile_bib_red: the faded red rag bib on about 1 Jizo in 3 (G1 A3 answer 4; PRODUCTION_PLAN B1 open item
  'a faded-red jizo-bib cloth ... the bib is B3b's'). Palette entry `bib_red_faded` (assumed): a safflower / madder red
  cotton after a year or two outdoors, never bright. Alpha 'cut': rags and holes, shredded hem on _w2.
C1 results: src/JP/common/materials/checks_b3b.json. Never starts or stops the server or any GUI program.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

PAL = os.path.join(DEV, "playbook", "palette.json")
ENTRY = {
    "id": "bib_red_faded",
    "name": "Jizo bib red, faded (a year or two outdoors)",
    "material": "red-dyed cotton (safflower / madder), sun- and rain-faded",
    "group": "textile",
    "tiers": [1, 2, 3],
    "use": "the rag bibs on about 1 Jizo in 3 (jp_m_textile_bib_red; G1 A3 answer 4: faded, never bright)",
    "note": "Added 2026-09-30 by B3b. No licensed sample of a period-faded bib: a dull brick red between a fresh bib "
            "(modern, bright) and the grey the cloth fades to; judge in game. The Jizo-bib date is disputed "
            "(OUTDOOR_LIST 3.3): used sparingly.",
    "srgb": [142, 80, 68],
    "method": "assumed",
    "tolerance_dE76": 12,
}


def add_palette():
    pal = json.load(open(PAL, encoding="utf-8"))
    if any(e.get("id") == ENTRY["id"] for e in pal["entries"]):
        return False
    e = dict(ENTRY)
    e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
    pal["entries"].append(e)
    with open(PAL, "wb") as f:
        f.write(json.dumps(pal, indent=1).encode("utf-8"))
    return True


def textile_bib_red(lv, S):
    """Like B1's textile_kinari (cotton weave, mildew, shredded hem on _w2), in the faded bib red."""
    T = B.T
    MT = B.MT
    t = [T("bib_red_faded", 3, 4, 2), T("bib_red_faded", 0, 0, 0), T("bib_red_faded", -4, -6, 1)][lv]
    co, nn, r = B.cotton_common(S, t, tiles=4, contrast=0.85)
    mask = B.Z(S)
    alpha = np.ones((S, S), np.float32)
    fold = np.clip(MT.fbm(S, 2.4, 1, 1, 5601), 0, None)            # sun-faded folds toward grey-pink
    co = co * (1 + [0.08, 0.14, 0.2][lv] * fold)[..., None]
    if lv >= 1:
        mil = MT.spots(S, [0, 12, 20][lv], 8, 0.8, 2.5, 14, 5602)
        co = MT.mix(co, (70, 66, 60), mil * 0.7)
        mask |= mil > 0.3
    if lv == 2:
        rg = np.random.default_rng(5603)
        w = MT.Wrap(S)
        for _ in range(16):
            x = rg.uniform(0, S)
            L = rg.uniform(0.1, 0.45) * S
            w.polygon([(x - rg.uniform(1, 4), S), (x + rg.uniform(1, 4), S), (x + rg.normal(0, 3), S - L)], 255)
        alpha[w.arr() > 0.3] = 0
        alpha[B.blobs(S, 5604, 1.9, 3.0, 2)] = 0
        st = B.blobs(S, 5605, 1.3, 3.0, 3)
        co = MT.patch(co, st, (96, 76, 60), 0.5, 5606)
        mask |= st
    return B.R(co, nn, r, mask, t, 0.05, 0.12, alpha=alpha)


def main(argv):
    added = add_palette()
    mid = "jp_m_textile_bib_red"
    m = B.M(mid, "textile", "bib_red_faded", 1.0, 512, textile_bib_red, (0.06, 15), "cloth", None,
            "plain cotton weave", alpha="cut", srcs=["rough_linen"], uv=B.WORLD + "; _w2 shreds hang from v = 1",
            where="outdoor", note="Faded red rag bib and cap for the stone Jizo (about 1 in 3). Two-sided geometry.")
    B.MATS.append(m)
    B.BYID[mid] = m
    B.NEED[mid] = {"id": mid, "wear": {"_w0": "dull red cotton, lightly faded", "_w1": "faded brick red, mildew spots",
                                       "_w2": "grey-pink rag, shredded hem, holes"},
                   "used_by": ["jp_s_stone_jizo"], "note": "Jizo bib and cap (G1 A3 answer 4)"}
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    res = B.make_one(m, pal, man)
    # the sidecar says who made it and why (make_one writes B1's defaults)
    sp = os.path.join(B.LIB, "textile", mid + ".json")
    sc = json.load(open(sp, encoding="utf-8"))
    sc["sources"][-1] = {"procedural": "make_b3b_materials.py (on make_b1_materials.make_one)"}
    sc["made_by"] = "research/materials/make_b3b_materials.py (agent B3b, 2026-09-30), through B1's make_one"
    sc["requested_by"] = "G1 A3 answer 4 (Jizo bibs, faded, about 1 in 3); PRODUCTION_PLAN B1 open item"
    B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
    for r in res:
        print("  %-4s %-30s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
            r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
    B.wb(os.path.join(B.LIB, "checks_b3b.json"), json.dumps({"check": "C1 palette (tools/matcheck), B3b materials",
                                                            "palette_entry_added": added, "results": res}, indent=1))
    ok = all(r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL" for r in res)
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("B3b materials:", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
