#!/usr/bin/env python3
r"""Two jp_common materials for the G3 fix pass (Stephen's first in-game house walk, 2026-09-27). Both palette-bound,
both matchecked, same layout as make_part_materials.py (library Super-shader rvmats, _co/_nohq/_smdi, 3 wear levels).

1. jp_m_wall_nakanuri_int (family wall, palette earth_wall_aged): the INTERIOR face of earth walls. In DayZ's cool
   interior ambient the weathered exterior nakanuri reads dark and greenish. This is the same clay, UNWEATHERED (no
   rain streaks, no splash - those are exterior effects, PLAYBOOK §15 T6), shifted warmer (+a*, +b*) at about the
   same lightness (Stephen: "it's supposed to be a dark game"; he judges in game). _w0 clean, _w1 = a trace of
   handling marks, _w2 light soot near the top (W5 is an interior effect, allowed).
2. jp_m_roof_kawara_far (family roof, palette kawara_ibushi): the far-LOD kawara field (Resolution 2 and 3). The flat
   far plane with the close material's specular (0.6 / 90) looked "too shiny and flat" and then darkened when the
   close geometry took over. This bakes the LOD0 corrugation (pan shadow, roll highlight, the course shadows of
   jp_m_roof_kawara_field) into colour and normal map, darkens the mean the way the modelled tiles shade (about -4 L*,
   inside tolerance), and uses a matte specular.

Writes data/materials/textures/*.png, src/JP/common/materials/<family>/*.paa|.rvmat|.json,
src/JP/common/materials/checks_fix.json, then repacks @Japan\addons\jp_common.pbo (unless --no-pack).
Usage: python make_fix_materials.py [--no-pack] [--rvmats-only]
(--rvmats-only, G3 fix 2: rewrite the 6 rvmats only, with the finish from build_materials.finish_for.)
"""
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_part_materials as MPM  # noqa: E402   (paths, save, to_paa, rvmat, lp; imports make_textures / matcheck)

MT, BM, matcheck = MPM.MT, MPM.BM, MPM.matcheck
TEX, LIB = MPM.TEX, MPM.LIB
KAWARA_FAR_SPEC = (0.22, 35)        # matte (close tiles: 0.6 / 90)
INT_TARGET = dict(dL=1.5, da=4.0, db=5.0)   # warmer (ochre, not pink) than earth_wall_aged at about the same lightness


# ------------------------------------------------------------------------------------------------ interior wall
def wall_int(lv, S=1024):
    r = MT.wall_nakanuri(0, S)                                    # the CLEAN exterior clay: no streaks, no patches
    t = MT.tgt("earth_wall_aged", **INT_TARGET)
    co = MT.recolor(r["co"], t, 1.6, 0.25)
    mask = np.zeros((S, S), bool)
    if lv == 1:                                                   # faint handling marks at hand height (low contrast)
        co = co * (1 - 0.03 * np.clip(MT.fbm(S, 2.2, 1, 1, 811), 0, 1))[..., None]
    if lv == 2:                                                   # W5: light soot toward the top of the texture tile
        yy = (np.arange(S, dtype=np.float32) / S)[:, None]
        soot = np.clip(0.6 - yy, 0, 1) * np.clip(0.8 + 0.4 * MT.fbm(S, 1.8, 1, 1, 812), 0, 1.4)
        co = co * (1 - 0.10 * soot)[..., None]
    co = MT.fix_mean(np.clip(co, 0, 1).astype(np.float32), t, ~mask)
    return co, r["n"], r["rough"], mask, t, r["spec"], r["gloss"]


# ------------------------------------------------------------------------------------------------ far kawara
def kawara_far(lv, S=1024):
    co, nn, rough, mask, t, spec, gloss = MPM.kawara_field(lv, S)
    cell = S // 4
    f = (np.arange(S) % cell).astype(np.float32) / cell           # fraction across a 0.26 column (texture u)
    prof = np.array(__import__("jpparts.kawara", fromlist=["PROFILE"]).PROFILE[0], np.float32)
    h = np.interp(f, prof[:, 0], prof[:, 1])                      # the LOD0 corrugation height (m)
    # baked shading of the modelled corrugation: pans shadowed, rolls lit (ambient-occlusion-like, sky light)
    occl = 0.80 + 0.30 * (h / h.max())                            # 0.80 in the pan .. 1.10 on the roll
    co = co * occl[None, :, None]
    dark = MT.tgt("kawara_ibushi", -4.0 + [1, -8, -9][lv], 0, -1)  # same wear offsets as roof_kawara, then -4 L*
    if lv == 2:
        dark = MT.tgt("kawara_ibushi", -13.0, toward="kawara_weathered", t=0.7)
    co = MT.fix_mean(np.clip(co, 0, 1).astype(np.float32), dark, ~mask)
    hmap = np.broadcast_to((h / 0.26 * cell)[None, :] * 0.5, (S, S)).astype(np.float32)
    ncor = MT.h2n(hmap, 1.0)
    n2 = MT.combine(nn, ncor)
    rough = np.clip(np.broadcast_to(np.asarray(rough, np.float32), (S, S)) + 0.25, 0, 1)
    return co, n2, rough, mask, dark, spec, gloss


def write_rvmat(fam, mid, lv, spec):
    w, (s, p), f = "_w%d" % lv, spec, [1.1, 1.0, 0.8][lv]
    MPM.wb(os.path.join(LIB, fam, mid + w + ".rvmat"), MPM.rvmat(fam, mid, w, round(s * f, 3), int(p * f)))


def write_set(fam, mid, pid, maker, spec_fn, looks, sidecar_extra, results):
    pal = matcheck.load_palette()
    wears = {}
    for lv in range(3):
        w = "_w%d" % lv
        co, nn, rough, mask, t, spec, gloss = maker(lv)
        stem = os.path.join(TEX, mid + w)
        MPM.save(stem + "_co.png", co)
        MPM.save(stem + "_nohq.png", nn * 0.5 + 0.5)
        rough = np.broadcast_to(np.asarray(rough, np.float32), co.shape[:2])
        s_, g_ = spec_fn(spec, gloss)
        MPM.save(stem + "_smdi.png", np.stack([np.ones_like(rough), s_ * (1 - rough), g_ * (1 - rough)], -1))
        mp = stem + "_mask.png"
        if mask.any():
            Image.fromarray((mask * 255).astype(np.uint8)).save(mp)
        elif os.path.isfile(mp):
            os.remove(mp)
        for suf in ("_co", "_nohq", "_smdi"):
            MPM.to_paa(stem + suf + ".png", os.path.join(LIB, fam, mid + w + suf + ".paa"))
        write_rvmat(fam, mid, lv, sidecar_extra["rvmat_spec"])
        a = matcheck.check(stem + "_co.png", pal, pid, TEX)
        b = matcheck.check(os.path.join(LIB, fam, mid + w + "_co.paa"), pal, pid, TEX)
        a["shipped_paa"] = {k: b.get(k) for k in ("mean_srgb", "dE", "verdict", "warnings")}
        results.append(a)
        wears[w] = {"name": ["clean", "normal", "heavy"][lv], "look": looks[lv], "co": MPM.lp(fam, mid, w, "_co.paa"),
                    "rvmat": MPM.lp(fam, mid, w, ".rvmat"), "target_srgb": [round(float(x), 1) for x in t],
                    "masked_frac": round(float(mask.mean()), 3)}
    sc = {"id": mid, "family": fam, "palette_id": pid, "palette_by_wear": {}, "wear": wears,
          "normal_convention": "DirectX (green = down), like the library",
          "made_by": "parts/kit/make_fix_materials.py (fix agent C-FIX, G3 2026-09-27)"}
    sc.update({k: v for k, v in sidecar_extra.items() if k != "rvmat_spec"})
    MPM.wb(os.path.join(LIB, fam, mid + ".json"), json.dumps(sc, indent=1, ensure_ascii=False))


def main(argv):
    if "--rvmats-only" in argv:                  # G3 fix 2: rvmats only (finish from BM.finish_for), no textures
        for lv in range(3):
            write_rvmat("wall", "jp_m_wall_nakanuri_int", lv, BM.SPEC["jp_m_wall_nakanuri"])
            write_rvmat("roof", "jp_m_roof_kawara_far", lv, KAWARA_FAR_SPEC)
        print("make_fix_materials: 6 rvmats rewritten")
        return 0 if ("--no-pack" in argv or BM.pack()) else 1
    results = []
    write_set("wall", "jp_m_wall_nakanuri_int", "earth_wall_aged", wall_int,
              lambda s, g: (s, g),
              ["clean clay, warm", "clean clay, faint handling marks", "clean clay, light soot at the top (W5)"],
              {"rvmat_spec": BM.SPEC["jp_m_wall_nakanuri"], "tile_size_m": 2.0, "texture_px": 1024, "px_per_m": 512.0,
               "uv": "world-scale: u, v = metres / tile_size_m (as jp_m_wall_nakanuri)", "grain": "none; fine trowel marks",
               "penetration_rvmat": "dz\\data\\data\\penetration\\dirt.rvmat", "roadway_surface": None,
               "interior": True, "exterior_twin": "jp_m_wall_nakanuri",
               "used_by": ["walls.wall_run(interior=...)", "buildings: interior faces of earth walls"],
               "used_on": "Every INTERIOR face of an earth (nakanuri / arakabe) wall, and interior clay fixtures "
                          "(kamado). Never the exterior face. PLAYBOOK §15 T6: interior faces never use exterior "
                          "weathering.",
               "sources": [{"derived_from": "jp_m_wall_nakanuri _w0 (Poly Haven clay_plaster, CC0)"},
                           {"target": "earth_wall_aged + (dL +1.5, da +4, db +5): warmer at about the same lightness, "
                                      "Stephen's G3 note (interior walls dark and greenish)"}]}, results)
    write_set("roof", "jp_m_roof_kawara_far", "kawara_ibushi", kawara_far,
              lambda s, g: (s * 0.35, g * 0.5),
              ["as roof_kawara_field _w0, corrugation baked, matte", "as _w0 at the _w1 wear", "as _w0 at the _w2 wear"],
              {"rvmat_spec": KAWARA_FAR_SPEC, "tile_size_m": 1.04, "tile_size_v_m": 0.94, "texture_px": 1024,
               "px_per_m": 985.0,
               "uv": "as jp_m_roof_kawara_field: u = metres along the eave / 1.04 from a ken line; v = metres down "
                     "the slope / 0.94",
               "grain": "4 columns (0.26) x 4 courses (0.235) per tile; LOD0 corrugation baked into colour + normal",
               "penetration_rvmat": "dz\\data\\data\\penetration\\pottery.rvmat",
               "roadway_surface": "dz\\surfaces\\data\\roadway\\ceramic_tiles_roof_ext.paa",
               "used_by": ["kawara.field (Resolution 2 and 3)"],
               "used_on": "The far LODs of every kawara field (the flat / 2-segment planes), so the roof keeps the "
                          "close LOD's darkness and matte look from a distance. PLAYBOOK §15 T7.",
               "sources": [{"derived_from": "jp_m_roof_kawara_field (make_part_materials.kawara_field)"},
                           {"baked": "kawara.PROFILE[0] corrugation: occlusion 0.80 pan .. 1.10 roll, height normal"}]},
              results)
    MPM.wb(os.path.join(LIB, "checks_fix.json"), json.dumps({"check": "C1 palette (tools/matcheck), G3 fix materials",
                                                            "results": results}, indent=1))
    bad = 0
    for r in results:
        print("  %-4s %-30s %-16s mean %-15s dE %4.1f/%-2g paa dE %4.1f %s" % (
            r["verdict"], os.path.basename(r["file"])[:-7], r["palette_id"], "(%d,%d,%d)" % tuple(r["mean_srgb"]),
            r["dE"], r["tol"], r["shipped_paa"]["dE"], "; ".join(r["warnings"])))
        bad += r["verdict"] == "FAIL" or r["shipped_paa"]["verdict"] == "FAIL"
    print("matcheck: %d sets, %d FAIL" % (len(results), bad))
    if "--no-pack" not in argv:
        BM.pack()
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
