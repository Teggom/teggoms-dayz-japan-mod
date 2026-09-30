#!/usr/bin/env python3
r"""make_l2_materials.py - the materials L2 (the outdoor life layer, research/interior/LIFE_LAYER.md items 51-74) ADDS
to jp_common through B1's pipeline.

  python make_l2_materials.py [--no-pack] [--only ID[,ID...]]

Adds only; never changes an existing material or palette entry (the route of make_b3b_materials.py and
make_l1_materials.py: B1's make_one = textures, PAAs, rvmats, sidecar, C1 matcheck on the PNG and the shipped PAA),
then repacks jp_common.pbo.

- jp_m_textile_net      Knotted fishing net, persimmon-tannin dyed hemp (BUILDING_LIST 343-346, 1766-1767): an
                        alpha-cut diamond mesh (3.5 cm meshes) so a draped net is one sheet, not hundreds of strands.
                        Palette `cha_koge` (existing: the burnt-tea brown of tannin-dyed cloth).
- jp_m_plant_foliage    Small-leaved foliage and needles for potted plants (#58: pine, azalea, chrysanthemum) and
                        weeds: alpha-cut leaf clusters. _w0 green, _w1 green with browned tips (unwatered a season),
                        _w2 dead and brown (two years unwatered). New palette entry `foliage_green` (assumed).
C1 results: src/JP/common/materials/checks_l2.json. Never starts or stops the server or any GUI program.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

PAL = os.path.join(DEV, "playbook", "palette.json")
f32 = np.float32
ENTRIES = [
    {"id": "foliage_green", "name": "Foliage of potted plants and weeds, autumn green (dull)", "material":
     "pine needles, azalea and chrysanthemum leaves, weeds", "group": "plant", "tiers": [1, 2, 3],
     "use": "potted plants and weeds (jp_m_plant_foliage); dead foliage is its _w2",
     "note": "Added 2026-09-30 by L2. Assumed: a dull, dark autumn green between moss_on_stone and kaya_moegi, "
             "darker than either (evergreen needles, leathery azalea leaves). Judge in game.",
     "srgb": [72, 86, 56], "method": "assumed", "tolerance_dE76": 12},
]


def add_palette():
    pal = json.load(open(PAL, encoding="utf-8"))
    have = {e.get("id") for e in pal["entries"]}
    added = []
    for ent in ENTRIES:
        if ent["id"] in have:
            continue
        e = dict(ent)
        e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
        pal["entries"].append(e)
        added.append(ent["id"])
    if added:
        with open(PAL, "wb") as f:
            f.write(json.dumps(pal, indent=1).encode("utf-8"))
    return added


def textile_net(lv, S):
    """A knotted diamond net: cords ~2 mm (2 px at 512 px/m... drawn 3 px so the mip holds), meshes 3.5 cm, a knot at
    each crossing; tannin brown, greying with wear; _w2 has broken meshes (bigger holes)."""
    T, MT = B.T, B.MT
    t = [T("cha_koge", 2, 1, 2), T("cha_koge", 0, 0, 0), T("cha_koge", 4, -2, -4)][lv]
    yy, xx = B.grid(S)
    p = S / 1.0 * 0.035 / math.sqrt(2)                            # diamond: two diagonal families of lines
    wob = 2.0 * MT.fbm(S, 2.0, 1, 1, 6101)
    a = ((xx + yy + wob) % (2 * p)) / (2 * p)
    b = ((xx - yy + wob) % (2 * p)) / (2 * p)
    da = np.minimum(a, 1 - a) * 2 * p                             # px to the nearest line
    db = np.minimum(b, 1 - b) * 2 * p
    cord = np.clip(1.9 - np.minimum(da, db), 0, 1)
    knot = np.clip(3.2 - np.hypot(da, db), 0, 1)
    cov = np.maximum(cord, knot)
    tw = 0.85 + 0.15 * np.sin((xx + yy) * 1.3) * np.sin((xx - yy) * 1.3)   # the twist of the cord
    co = B.base(t, tw * (0.85 + 0.15 * MT.fbm(S, 2.2, 1, 1, 6102)))
    mask = B.Z(S)
    if lv >= 1:                                                   # salt / sun greying in patches
        g = np.clip(MT.fbm(S, 2.6, 1, 1, 6103), 0, None)
        co = MT.mix(co, (120, 112, 100), g * [0, 0.25, 0.4][lv])
    if lv == 2:                                                   # broken meshes
        br = B.blobs(S, 6104, 2.2, 3.0, 2)
        cov = cov * np.where(br, 0.0, 1.0)
    alpha = (cov > 0.45).astype(f32)
    return B.R(np.clip(co, 0, 1), MT.h2n(cov * 1.5, 1.0), 0.9, mask, t, 0.05, 0.1, alpha=alpha)


def plant_foliage(lv, S):
    """Leaf clusters on a 0.5 m tile (1 mm a pixel): overlapping small ellipse leaves (azalea / chrysanthemum) and
    needle strokes (pine) in two halves of the tile (u < 0.5 needles, u >= 0.5 leaves), gaps transparent."""
    T, MT = B.T, B.MT
    t = [T("foliage_green", 3, -3, 2), T("foliage_green", 0, 0, 0), T("foliage_green", 3, 5, 8)][lv]
    rg = np.random.default_rng(6201)
    cov = MT.Wrap(S)
    val = MT.Wrap(S)
    for _ in range(int(S * S / 90)):                              # needles in pairs, left half
        x, y = rg.uniform(0, S / 2), rg.uniform(0, S)
        ang = rg.uniform(0, math.pi)
        L = rg.uniform(10, 22)
        for d in (-0.25, 0.25):
            x1, y1 = x + L * math.cos(ang + d), y + L * math.sin(ang + d)
            v = int(rg.uniform(120, 255))
            cov.line([(x, y), (x1, y1)], 255, width=2)
            val.line([(x, y), (x1, y1)], v, width=2)
    for _ in range(int(S * S / 260)):                             # leaves, right half
        x, y = rg.uniform(S / 2, S), rg.uniform(0, S)
        ang = rg.uniform(0, math.pi)
        L, Wd = rg.uniform(7, 14), rg.uniform(3, 6)
        pts = [(x + L * math.cos(ang) * math.cos(k * math.pi / 4) - Wd * math.sin(ang) * math.sin(k * math.pi / 4),
                y + L * math.sin(ang) * math.cos(k * math.pi / 4) + Wd * math.cos(ang) * math.sin(k * math.pi / 4))
               for k in range(8)]
        v = int(rg.uniform(110, 255))
        cov.polygon(pts, 255)
        val.polygon(pts, v)
    c = cov.arr()
    v = val.arr()
    co = B.base(t, 0.6 + 0.5 * v)
    mask = B.Z(S)
    if lv >= 1:                                                   # browned tips and dead leaves (detail: masked)
        br = MT.fbm(S, 1.8, 1, 1, 6202) > [0, 0.9, 0.1][lv]
        co = MT.mix(co, (118, 92, 60), br.astype(f32) * 0.85)
        mask |= br
    alpha = (c > 0.5).astype(f32)
    if lv == 2:                                                   # dead: fewer leaves left
        alpha = alpha * (MT.fbm(S, 1.6, 1, 1, 6203) > -0.4)
    return B.R(np.clip(co, 0, 1), MT.h2n(c * 1.0 + v * 0.5, 1.0), 0.85, mask, t, 0.05, 0.12, alpha=alpha)


def table():
    return [
        (B.M("jp_m_textile_net", "textile", "cha_koge", 1.0, 512, textile_net, (0.05, 12), "cloth", None,
             "knotted diamond mesh, 3.5 cm meshes, lines diagonal to u and v", alpha="cut", uv=B.WORLD, where="outdoor",
             note="Fishing net (tannin-dyed hemp). Two-sided geometry; one sheet per net panel. Floats are geometry "
                  "(wood / gourd, never glass)."),
         {"_w0": "tannin-brown hemp net", "_w1": "sun and salt greyed in patches", "_w2": "grey, broken meshes"},
         ["jp_s_fishnet"], "Fishing nets drying on poles"),
        (B.M("jp_m_plant_foliage", "plant", "foliage_green", 0.5, 512, plant_foliage, (0.08, 16), "cloth", None,
             "needle pairs (u < 0.5) and small leaves (u >= 0.5), random directions", alpha="cut", uv=B.WORLD,
             where="outdoor",
             note="Potted plants and weeds. Map needle cards onto u 0-0.5, leaf cards onto u 0.5-1. Two-sided cards."),
         {"_w0": "green", "_w1": "green, browned tips (a season unwatered)", "_w2": "dead, brown, half the leaves gone"},
         ["jp_s_potted"], "Potted plants: pine, azalea, chrysanthemum; weeds"),
    ]


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    added = add_palette()
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        if only and mid not in only:
            continue
        B.MATS.append(m)
        B.BYID[mid] = m
        B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by, "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"][-1] = {"procedural": "make_l2_materials.py (on make_b1_materials.make_one)"}
        sc["made_by"] = "research/materials/make_l2_materials.py (agent L2, 2026-09-30), through B1's make_one"
        sc["requested_by"] = "research/interior/LIFE_LAYER.md (L2, the outdoor life layer)"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-36s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_l2.json"), json.dumps({"check": "C1 palette (tools/matcheck), L2 materials",
                                                           "palette_entries_added": added, "results": allres},
                                                          indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("L2 materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
