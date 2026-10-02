#!/usr/bin/env python3
"""FX5 (2026-10-02): the clipped-hedge surface material, through B1's make_one (same pipeline as make_l2_materials).

- jp_m_plant_hedge   Opaque clipped evergreen hedge face (kashi oak / podocarp / camellia / holly, sheared): a dense
                     mat of small leathery leaves in three depth layers (dark hollows behind, lit leaves on top),
                     sprig-sized clumps (~8 cm) and a soft large-scale light / dark drift. 0.5 m tile, 1 mm a pixel.
                     Replaces jp_m_plant_foliage (alpha-cut leaf cards for potted plants) on the hedge BODY, where the
                     card material's holes showed through and read as speckled paint. The hedge's leafy fringe stays
                     on jp_m_plant_foliage's leaf half (two-sided alpha cards). _w0 fresh, _w1 a season unclipped
                     (browned patches), _w2 years untended (dull, more brown and dead twigs).
  Palette `foliage_green` (L2's; dull dark autumn evergreen).

  python research/materials/make_fx5_materials.py [--no-pack]
C1 results: src/JP/common/materials/checks_fx5.json. Never starts or stops the server or any GUI program.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

f32 = np.float32


def plant_hedge(lv, S):
    T, MT = B.T, B.MT
    t = [T("foliage_green", 3, -3, 2), T("foliage_green", 0, 0, 0), T("foliage_green", 2, 4, 7)][lv]
    rg = np.random.default_rng(6501)
    val = MT.Wrap(S, fill=0)
    hgt = MT.Wrap(S, fill=0)
    brn = MT.Wrap(S, fill=0)
    # sprig clumps: a low-frequency field lifts whole clumps (lit crowns) and sinks the hollows between them
    clump = MT.fbm(S, 2.0, 2, 2, 6502)
    clump = (clump - clump.min()) / (np.ptp(clump) + 1e-6)
    sc = S / 512.0
    layers = [(int(1500 * sc * sc), 0.30, 0.48, 60), (int(1300 * sc * sc), 0.52, 0.74, 140),
              (int(900 * sc * sc), 0.74, 1.00, 230)]
    for li, (n, v0, v1, hh) in enumerate(layers):
        for _ in range(n):
            x, y = rg.uniform(0, S), rg.uniform(0, S)
            cl = clump[int(y) % S, int(x) % S]
            if li == 2 and rg.random() > 0.55 + 0.45 * cl:     # top leaves sit on the clump crowns
                continue
            ang = rg.uniform(0, math.pi)
            L = rg.uniform(14, 26) * sc                          # half length: 3-5 cm leaves
            Wd = L * rg.uniform(0.38, 0.52)
            pts = []
            for k in range(10):
                a = k * 2 * math.pi / 10
                ex, ey = L * math.cos(a), Wd * math.sin(a) * (1.0 - 0.25 * math.cos(a))   # pointed tip
                pts.append((x + ex * math.cos(ang) - ey * math.sin(ang), y + ex * math.sin(ang) + ey * math.cos(ang)))
            v = rg.uniform(v0, v1) * (0.88 + 0.12 * cl)
            val.polygon(pts, int(255 * v))
            hgt.polygon(pts, hh)
            # the lit half of the leaf (light from above-left) and the midrib
            half = [pts[0], pts[1], pts[2], pts[3], pts[4], pts[5]]
            val.polygon(half, int(255 * min(1.0, v * 1.12)))
            val.line([pts[0], pts[5]], int(255 * v * 0.80), width=max(1, int(sc)))
            # every leaf overwrites the brown mask, so a lit leaf drawn later covers a browned one beneath it
            brn.polygon(pts, 255 if (lv >= 1 and rg.random() < [0.0, 0.05, 0.16][lv]) else 0)
    v = val.arr()
    h = hgt.arr()
    hollow = v < 0.05
    v = np.where(hollow, 0.10, v)                                # the dark interior seen between leaves
    drift = MT.fbm(S, 2.8, 1, 1, 6503)
    drift = (drift - drift.mean()) / (drift.std() + 1e-6)
    v = v * (1.0 + 0.03 * drift)
    co = B.base(t, 0.45 + 0.85 * v)
    mask = B.Z(S)
    if lv >= 1:
        b = brn.arr() > 0.5
        co = MT.mix(co, (104, 92, 62), b.astype(f32) * 0.65)
        mask |= b
    if lv == 2:                                                  # dead twigs showing through thin patches
        tw = MT.Wrap(S, fill=0)
        for _ in range(int(60 * sc * sc)):
            x, y = rg.uniform(0, S), rg.uniform(0, S)
            a = rg.uniform(0, math.pi)
            L = rg.uniform(30, 80) * sc
            tw.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], 255, width=max(2, int(2 * sc)))
        twm = tw.arr() > 0.5
        co = MT.mix(co, (92, 80, 66), twm.astype(f32) * 0.9)
        mask |= twm
    n = MT.h2n(h + 0.35 * v, 1.6)
    return B.R(np.clip(co, 0, 1), n, 0.80, mask, t, 0.06, 0.14)


def plant_hedge_fringe(lv, S):
    """Leaf-sprig cards for the hedge's fringe: 2 x 2 cells (0.25 m each), one sprig cluster per cell (a few twigs
    with leaves fanning up from the cell's lower middle), dense at the base, thinning to a ragged leafy outline,
    fully transparent round it. Same leaves and colours as jp_m_plant_hedge."""
    T, MT = B.T, B.MT
    t = [T("foliage_green", 3, -3, 2), T("foliage_green", 0, 0, 0), T("foliage_green", 2, 4, 7)][lv]
    rg = np.random.default_rng(6601 + 0)
    cov = MT.Wrap(S, fill=0)
    val = MT.Wrap(S, fill=0)
    brn = MT.Wrap(S, fill=0)
    C = S // 2
    sc = S / 512.0
    for cy in range(2):
        for cx in range(2):
            ox, oy = cx * C, cy * C
            base = (ox + C * 0.5, oy + C * 0.95)
            for tw in range(rg.integers(4, 7)):
                a = math.radians(rg.uniform(-60, 60)) - math.pi / 2       # twigs fan upwards
                Ln = C * rg.uniform(0.45, 0.78)
                tip = (min(max(base[0] + Ln * math.cos(a), ox + 8), ox + C - 8),
                       min(max(base[1] + Ln * math.sin(a), oy + 8), oy + C - 8))
                val.line([base, tip], 70, width=max(1, int(2 * sc)))
                cov.line([base, tip], 255, width=max(1, int(2 * sc)))
                nleaf = int(rg.integers(9, 15))
                for k in range(nleaf):
                    f = (k + 0.5) / nleaf
                    px, py = base[0] + (tip[0] - base[0]) * f, base[1] + (tip[1] - base[1]) * f
                    for side in (-1.0, 1.0):
                        if rg.random() < 0.15:
                            continue
                        la = a + side * math.radians(rg.uniform(35, 65))
                        L = rg.uniform(12, 20) * sc * (1.1 - 0.4 * f)
                        Wd = L * rg.uniform(0.38, 0.5)
                        cxl, cyl = px + 0.9 * L * math.cos(la), py + 0.9 * L * math.sin(la)
                        pts = []
                        for j in range(10):
                            q = j * 2 * math.pi / 10
                            ex, ey = L * math.cos(q), Wd * math.sin(q) * (1.0 - 0.25 * math.cos(q))
                            pts.append((cxl + ex * math.cos(la) - ey * math.sin(la),
                                        cyl + ex * math.sin(la) + ey * math.cos(la)))
                        # keep every leaf inside its own cell (cards must not bleed into the neighbour cell)
                        pts = [(min(max(x, ox + 2), ox + C - 3), min(max(y, oy + 2), oy + C - 3)) for x, y in pts]
                        v = rg.uniform(0.55, 1.0)
                        cov.polygon(pts, 255)
                        val.polygon(pts, int(255 * v))
                        brn.polygon(pts, 255 if (lv >= 1 and rg.random() < [0.0, 0.05, 0.16][lv]) else 0)
    c = cov.arr()
    v = val.arr()
    co = B.base(t, 0.45 + 0.85 * np.maximum(v, 0.2))
    mask = B.Z(S)
    if lv >= 1:
        b = brn.arr() > 0.5
        co = MT.mix(co, (104, 92, 62), b.astype(f32) * 0.65)
        mask |= b
    alpha = (c > 0.5).astype(f32)
    return B.R(np.clip(co, 0, 1), MT.h2n(c * 0.8 + v * 0.4, 1.0), 0.85, mask, t, 0.05, 0.12, alpha=alpha)


def table():
    return [
        (B.M("jp_m_plant_hedge", "plant", "foliage_green", 1.0, 1024, plant_hedge, (0.08, 16), "cloth", None,
             "dense small leaves, random directions (no grain)", uv=B.WORLD, where="outdoor",
             note="Clipped evergreen hedge face (ikegaki body). Opaque; world-scale u along the run, v round the "
                  "section. The leafy fringe uses jp_m_plant_foliage's leaf half (two-sided alpha cards)."),
         {"_w0": "fresh clipped green", "_w1": "a season unclipped, browned patches",
          "_w2": "years untended: dull, browner, dead twigs"},
         ["jp_p_hedge_ikegaki"], "Clipped hedges (ikegaki): the hedge body"),
        (B.M("jp_m_plant_hedge_fringe", "plant", "foliage_green", 0.5, 512, plant_hedge_fringe, (0.08, 16), "cloth",
             None, "leaf sprigs fanning up from each cell's lower middle", alpha="cut", uv=B.WORLD, where="outdoor",
             note="Hedge fringe cards: 2 x 2 cells of 0.25 m, one sprig per cell; map a card onto one whole cell "
                  "(u, v in [0, 0.5] or [0.5, 1]), its bottom edge = the cell's bottom (v down). Two-sided cards."),
         {"_w0": "fresh green sprigs", "_w1": "a few browned leaves", "_w2": "dull, browner"},
         ["jp_p_hedge_ikegaki"], "Clipped hedges (ikegaki): the leafy fringe"),
    ]


def main(argv):
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        B.MATS.append(m)
        B.BYID[mid] = m
        B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by, "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"][-1] = {"procedural": "make_fx5_materials.py (on make_b1_materials.make_one)"}
        sc["made_by"] = "research/materials/make_fx5_materials.py (agent FX5, 2026-10-02), through B1's make_one"
        sc["requested_by"] = "FX5 (Stephen's 3a walk: the hedge read as flat paint with visible segments)"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-36s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_fx5.json"), json.dumps({"check": "C1 palette (tools/matcheck), FX5 materials",
                                                            "results": allres}, indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("FX5 materials:", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
