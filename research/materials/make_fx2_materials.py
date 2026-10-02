#!/usr/bin/env python3
r"""make_fx2_materials.py - FX2 (statues, 2026-10-01): the one material the statue pass needed. ADDS ONLY: never
changes an existing material or palette entry (the route of make_w2s_materials.py: the palette entry, then B1's
make_one: textures, PAAs, rvmats, sidecar, C1 matcheck on the PNG and the shipped PAA; then jp_common.pbo is repacked).

  python make_fx2_materials.py [--no-pack] [--draft]

- jp_m_gilt_worn   gold leaf over black lacquer (urushi-haku) on carved wood, as old temple images are: dull gold
                   with the leaf rubbed through to the black ground on the high points and edges, dust in the
                   hollows. New palette `gilt_worn`, SAMPLED from the open-access photos of gilded images fetched by
                   FX2 (research/statues/REFS.md: Met 44890 Amida, CMA 147588 seated Buddha) as a hand-picked mean of
                   the lit gold (general method: PLAYBOOK §8 box method, by eye on the downloaded web images).
C1 results: src/JP/common/materials/checks_fx2.json. Never starts or stops the server or any GUI program.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

PAL = os.path.join(DEV, "playbook", "palette.json")
DRAFT = os.path.join(DEV, "spikes", "FX2", "draft")
REFS = os.path.join(DEV, "data", "refs", "fx2")
f32 = np.float32
T, MT = B.T, B.MT

ADDED_BY = "Added 2026-10-01 by FX2 (research/materials/make_fx2_materials.py; research/statues/NOTES.md)."
# boxes on the lit gilt of two fetched images (x0, y0, x1, y1 as fractions): the chest / lap gold, no shadow, no halo
SAMPLES = [("met_44890_0.jpg", (0.40, 0.42, 0.60, 0.50)),
           ("cma_147588_0.jpg", (0.42, 0.42, 0.56, 0.50))]


def sample():
    vals = []
    for fn, (x0, y0, x1, y1) in SAMPLES:
        fp = os.path.join(REFS, fn)
        if not os.path.isfile(fp):
            continue
        im = np.asarray(Image.open(fp).convert("RGB"), f32)
        h, w = im.shape[:2]
        box = im[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)].reshape(-1, 3)
        vals.append({"ref": fn, "box": [x0, y0, x1, y1], "value": [int(round(v)) for v in box.mean(0)]})
    return vals


def entry():
    sm = sample()
    if sm:
        mean = np.mean([s["value"] for s in sm], 0)
        srgb = [int(round(v)) for v in mean]
        meth = "sampled"
    else:
        srgb, meth = [150, 118, 62], "assumed"
    return {"id": "gilt_worn", "name": "Worn gold leaf over black lacquer (old temple image)",
            "material": "gold leaf laid on black urushi over carved cypress, dulled by incense smoke and dust, rubbed "
                        "through to the black ground on the high points",
            "group": "fitting", "tiers": [1, 2, 3], "use": "Buddhist images on the altars (jp_m_gilt_worn; FX2)",
            "note": ADDED_BY + " The mean of the lit gilt in the fetched open-access photos (boxes in 'samples'); "
                    "museum lighting is warm and bright, so the in-hall value reads darker in game (dust _w1/_w2).",
            "srgb": srgb, "method": meth, "tolerance_dE76": 18, "observed_spread_dE76": 0.0, "samples": sm}


def add_palette():
    pal = json.load(open(PAL, encoding="utf-8"))
    have = {e.get("id") for e in pal["entries"]}
    e = entry()
    if e["id"] in have:
        return []
    e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
    pal["entries"].append(e)
    with open(PAL, "wb") as f:
        f.write(json.dumps(pal, indent=1).encode("utf-8"))
    return [e["id"]]


def gilt_worn(lv, S):
    """0.5 m tile at 512 px: gold leaf squares (~9 cm, the leaf size) with faint overlap seams, a soft mottle, the
    black ground showing through in rubbed patches (more with wear), dust in the hollows (low noise troughs).
    _w0 bright worn gilt (well kept), _w1 dulled + rubbed patches, _w2 heavily rubbed, dusty."""
    t = [T("gilt_worn", 8, 6, 2), T("gilt_worn"), T("gilt_worn", -6, -6, -4)][lv]
    yy, xx = B.grid(S)
    cell = S / 5.5
    sx = np.minimum((xx % cell) / cell, 1 - (xx % cell) / cell)
    sy = np.minimum(((yy + 0.37 * cell * np.floor(xx / cell)) % cell) / cell, 1 - ((yy + 0.37 * cell * np.floor(xx / cell)) % cell) / cell)
    seam = np.clip(1 - np.minimum(sx, sy) / 0.03, 0, 1)
    hgt = MT.fbm(S, 2.4, 1, 1, 9501)
    val = 1.0 + 0.10 * hgt + 0.05 * MT.fbm(S, 1.3, 1, 1, 9502) - 0.06 * seam
    co = B.base(t, val)
    rub = np.clip((MT.fbm(S, 2.0, 1, 1, 9503) - [1.3, 0.85, 0.45][lv]) / 0.6, 0, 1)
    rub = rub * np.clip(0.6 + 0.6 * MT.fbm(S, 1.2, 1, 1, 9504), 0, 1)
    co = MT.mix(co, (34, 28, 24), rub * 0.85)                   # the black lacquer ground through the leaf
    dust = np.clip((-hgt - [1.4, 1.0, 0.6][lv]) / 1.0, 0, 1)
    co = MT.mix(co, (120, 110, 96), dust * [0.3, 0.45, 0.6][lv])
    mask = (rub > 0.3) | (dust > 0.4)
    h = 0.3 * hgt - 0.3 * seam
    n = MT.h2n(h.astype(f32), 0.6)
    return B.R(np.clip(co, 0, 1).astype(f32), n, 0.55, mask, t, 0.30, 0.40)


def table():
    return [(B.M("jp_m_gilt_worn", "paint", "gilt_worn", 0.5, 512, gilt_worn, (0.30, 50), "wood", None,
                 "none; leaf squares ~9 cm", uv=B.WORLD, where="interior",
                 note="Worn gold leaf over black lacquer: the gilded Buddhist images on temple altars (FX2 statues). "
                      "0.5 m tile, world uvs on the sculpted meshes."),
             {"_w0": "bright worn gilt (a kept hall)", "_w1": "dulled by smoke and dust, rubbed patches",
              "_w2": "heavily rubbed to the black ground, dusty"},
             ["jp_f_dais_* (FX2 altar images)"], "Gilded altar images")]


def draft():
    os.makedirs(DRAFT, exist_ok=True)
    e = entry()
    MT.PAL[e["id"]] = dict(e)
    for m, _, _, _ in table():
        for lv in range(3):
            r = m["maker"](lv, m["S"])
            mask = np.asarray(r["mask"], bool)
            co = MT.fix_mean(np.clip(r["co"], 0, 1).astype(f32), r["target"], ~mask)
            Image.fromarray((co * 255 + 0.5).astype(np.uint8)).save(os.path.join(DRAFT, "%s_w%d.png" % (m["id"], lv)))
            print("draft", m["id"], lv, (co[~mask].mean(0) * 255).round(1))


def main(argv):
    if "--draft" in argv:
        draft()
        return 0
    added = add_palette()
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
        sc["sources"] = [{"procedural": "make_fx2_materials.py (on make_b1_materials.make_one)"},
                         {"palette_samples": "data/refs/fx2 (Met / Cleveland open access, research/statues/REFS.md)"}]
        sc["made_by"] = "research/materials/make_fx2_materials.py (agent FX2, 2026-10-01), through B1's make_one"
        sc["requested_by"] = "FX2 brief (statues: gilt as appropriate)"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-40s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_fx2.json"), json.dumps({"check": "C1 palette (tools/matcheck), FX2 materials",
                                                          "palette_entries_added": added, "results": allres}, indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("FX2 materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
