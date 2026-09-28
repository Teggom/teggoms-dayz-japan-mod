#!/usr/bin/env python3
r"""Two small jp_common materials the parts need (parts agent, 2026-09-27). Both palette-bound, both matchecked.

1. jp_m_wall_grime (family wall, palette grime_splash): the W1 splash band (PLAYBOOK §6.5) as an ALPHA DECAL.
   A tiling texture cannot carry a band bound to the wall base, so jp_p_trim_grime_* lays a 0.45 m high strip of this
   over wall bases, posts and sills. Texture u tiles every 2.0 m along the wall, v spans the band (top = transparent,
   bottom = most grime). _ca (DXT5 with alpha); rvmat = the library Super-shader layout + renderFlags NoZWrite, like
   vanilla dz\structures\residential\police\data\big_police_station_decals.rvmat. The RGB is the grime colour
   everywhere (alpha only sets coverage), so the palette mean is meaningful: matcheck measures the RGB.
2. jp_m_roof_kawara_field (family roof, palette kawara_ibushi): PLAYBOOK §6.1 LOD0 asks for "row steps from the
   normal map and baked AO" between the geometry-stepped rows near eave and ridge; the library kawara is a plain
   ceramic surface with no courses. This is the same ceramic (make_textures.roof_kawara, same wear targets) with the
   0.235 m courses (AO under each tile butt, lip highlight, a step in the normal map) and a per-tile tint (W8), laid
   out as 4 columns x 4 rows = 1.04 x 0.94 m per texture tile (columns 0.26 = ken/7, aligned to ken lines).

Writes data/materials/textures/*.png, src/JP/common/materials/<family>/*.paa|.rvmat|.json and
src/JP/common/materials/checks_parts.json. Usage: python make_part_materials.py
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
MATRES = os.path.join(DEV, "research", "materials")
sys.path[:0] = [MATRES, os.path.join(DEV, "tools", "matcheck"), os.path.join(DEV, "tools", "common")]
import make_textures as MT  # noqa: E402
import build_materials as BM  # noqa: E402
import matcheck  # noqa: E402

TEX = MT.OUT
LIB = os.path.join(DEV, "src", "JP", "common", "materials")
IMAGE_TO_PAA = BM.IMAGE_TO_PAA


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def lp(fam, mid, wear, suf):
    return "JP\\common\\materials\\%s\\%s%s%s" % (fam, mid, wear, suf)


# ------------------------------------------------------------------------------------------------ grime
def grime(lv, W=1024, H=256):
    """RGBA, u tiles (W px = 2.0 m), v = band from top (0, clear) to bottom (1, max)."""
    t = [MT.tgt("grime_splash", 4), MT.tgt("grime_splash"), MT.tgt("grime_splash", -5)][lv]
    base = np.asarray(t, np.float32) / 255
    n1 = MT.fbm(W, 2.4, 1, 1, 301 + lv)[:H, :]                  # tone, periodic along u
    n2 = MT.fbm(W, 3.0, 1, 5, 305 + lv)[:H, :]                  # soft vertical drip streaks (fy > 1 = along v)
    co = base[None, None, :] * (1 + 0.10 * n1 + 0.05 * n2)[..., None]
    v = (np.arange(H, dtype=np.float32) / (H - 1))[:, None]
    edge = 0.72 + 0.10 * MT.fbm(W, 3.2, 1, 1, 311)[0:1, :] + 0.04 * n2  # ragged upper limit (~0.32 m of 0.45)
    cov = np.clip((v - (1 - edge * [0.75, 1.0, 1.15][lv])) / 0.55, 0, 1) ** 1.2
    specks = (MT.spots(W, 90, 10, 1, 3, 30, 321 + lv)[:H, :] * (v > 0.55)).astype(np.float32)
    amax = [0.45, 0.72, 0.9][lv]
    alpha = np.clip(cov * amax + specks * 0.35 * cov, 0, 1)
    mask = np.zeros((H, W), bool)
    if lv == 2:                                                   # W6 moss at the very foot, masked from the mean
        mo = MT.spots(W, 50, 8, 2, 6, 18, 331)[:H, :] * (v > 0.8)
        co = MT.mix(co, (84, 96, 52), mo * 0.8)
        mask = mo > 0.3
    co = MT.fix_mean(np.clip(co, 0, 1).astype(np.float32), t, ~mask)
    h = 0.5 * n1 + specks
    nrm = MT.h2n(np.pad(h, ((0, W - H), (0, 0)), mode="wrap"), 0.6)[:H]
    rough = np.full((H, W), 0.9, np.float32)
    return co, alpha, nrm, rough, mask, t


# ------------------------------------------------------------------------------------------------ kawara field
def kawara_field(lv, S=1024):
    r = MT.roof_kawara(lv, S)                                     # same ceramic, same wear target
    co, n, mask, t = r["co"].astype(np.float32), r["n"], r["mask"], r["target"]
    cell = S // 4
    rng = np.random.default_rng(401 + lv)
    tint = np.ones((S, S), np.float32)
    for i in range(4):
        for j in range(4):
            tint[i * cell:(i + 1) * cell, j * cell:(j + 1) * cell] = 1 + rng.normal(0, [0.035, 0.05, 0.07][lv])
    yy = (np.arange(S) % cell).astype(np.float32)[:, None]
    shade = 1 - 0.42 * np.exp(-yy / 9.0)                          # AO in the shadow under the butt of the row above
    lip = 1 + 0.10 * np.exp(-(cell - 1 - yy) / 2.5)              # lit lip of the butt
    xx = (np.arange(S) % cell).astype(np.float32)[None, :] / cell
    trough = 1 - 0.07 * np.exp(-((xx - 0.40) / 0.16) ** 2)       # slight darkening in the pan (geometry does the rest)
    co = co * (tint * shade * lip * trough)[..., None]
    co = MT.fix_mean(np.clip(co, 0, 1), t, ~mask)
    ramp = -(yy / cell) * 1.0                                     # each row rises toward its butt... sawtooth step
    h = np.broadcast_to(ramp, (S, S)).astype(np.float32)
    n2 = MT.h2n(h, 18.0)
    nn = MT.combine(n, n2)
    return co, nn, r["rough"], mask, t, r["spec"], r["gloss"]


def save(path, a):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)


def to_paa(png, paa):
    os.makedirs(os.path.dirname(paa), exist_ok=True)
    r = subprocess.run([IMAGE_TO_PAA, png, paa], capture_output=True, text=True, errors="replace")
    if r.returncode != 0 or not os.path.isfile(paa):
        raise RuntimeError("ImageToPAA failed %s: %s" % (png, r.stdout + r.stderr))


def rvmat(fam, mid, wear, s, p, decal=False):
    t = BM.rvmat_text(lp(fam, mid, wear, "_nohq.paa"), lp(fam, mid, wear, "_smdi.paa"), s, p)
    if decal:
        t = t.replace('VertexShaderID="Super";\n', 'VertexShaderID="Super";\nrenderFlags[]=\n{\n\t"NoZWrite"\n};\n', 1)
    return t


def main():
    pal = matcheck.load_palette()
    results = []
    # ---- grime
    fam, mid = "wall", "jp_m_wall_grime"
    wears = {}
    for lv in range(3):
        w = "_w%d" % lv
        co, alpha, nrm, rough, mask, t = grime(lv)
        stem = os.path.join(TEX, mid + w)
        rgba = np.concatenate([co, alpha[..., None]], -1)
        save(stem + "_ca.png", rgba)
        save(stem + "_co.png", co)                                # RGB twin for matcheck (not shipped)
        save(stem + "_nohq.png", nrm * 0.5 + 0.5)
        smdi = np.stack([np.ones_like(rough), 0.05 * (1 - rough), 0.1 * (1 - rough)], -1)
        save(stem + "_smdi.png", smdi)
        if mask.any():
            Image.fromarray((mask * 255).astype(np.uint8)).save(stem + "_mask.png")
        for suf in ("_ca", "_nohq", "_smdi"):
            to_paa(stem + suf + ".png", os.path.join(LIB, fam, mid + w + suf + ".paa"))
        wb(os.path.join(LIB, fam, mid + w + ".rvmat"), rvmat(fam, mid, w, round(0.05 * [1.1, 1, 0.8][lv], 3), 10, True))
        a = matcheck.check(stem + "_co.png", pal, "grime_splash", TEX)
        b = matcheck.check(os.path.join(LIB, fam, mid + w + "_ca.paa"), pal, "grime_splash", TEX)
        a["shipped_paa"] = {k: b.get(k) for k in ("mean_srgb", "dE", "verdict", "warnings")}
        results.append(a)
        wears[w] = {"name": ["clean", "normal", "heavy"][lv],
                    "look": ["light dust at the foot", "splash band, ragged top, drips", "dark mud band, moss at the foot"][lv],
                    "co": lp(fam, mid, w, "_ca.paa"), "rvmat": lp(fam, mid, w, ".rvmat"),
                    "target_srgb": [round(float(x), 1) for x in t], "alpha_max": [0.45, 0.72, 0.9][lv],
                    "masked_frac": round(float(mask.mean()), 3)}
    wb(os.path.join(LIB, fam, mid + ".json"), json.dumps({
        "id": mid, "family": fam, "palette_id": "grime_splash", "palette_by_wear": {}, "alpha": True,
        "tile_size_m": 2.0, "tile_size_v_m": 0.45, "texture_px": [1024, 256], "px_per_m": 512.0,
        "uv": "u = metres along the wall / 2.0 (tiles); v = 0 at the band top (y 0.45) .. 1 at its foot (y 0): "
              "explicit UVs from jp_p_trim_grime, not world-scale",
        "grain": "none; vertical drips", "penetration_rvmat": "dz\\data\\data\\penetration\\dirt.rvmat",
        "roadway_surface": None, "decal": True,
        "render": "Super shader, renderFlags NoZWrite (vanilla decal rvmat pattern); _ca alpha = coverage",
        "wear": wears, "used_by": ["jp_p_trim_grime"],
        "used_on": "W1 splash band over the bottom 0.4 m of exterior walls, posts, sills and plinth stones.",
        "sources": [{"procedural": "parts/kit/make_part_materials.py"},
                    {"palette_sample": "x08_hirose_earthwall (grime_splash)"}],
        "normal_convention": "DirectX (green = down), like the library",
        "made_by": "parts/kit/make_part_materials.py (parts agent, 2026-09-27)",
        "note": "Never in Geometry/View/Fire. Keep 3 mm off the surface it covers."}, indent=1, ensure_ascii=False))
    # ---- kawara field
    fam, mid = "roof", "jp_m_roof_kawara_field"
    wears = {}
    for lv in range(3):
        w = "_w%d" % lv
        co, nn, rough, mask, t, spec, gloss = kawara_field(lv)
        stem = os.path.join(TEX, mid + w)
        save(stem + "_co.png", co)
        save(stem + "_nohq.png", nn * 0.5 + 0.5)
        rough = np.broadcast_to(np.asarray(rough, np.float32), co.shape[:2])
        save(stem + "_smdi.png", np.stack([np.ones_like(rough), spec * (1 - rough), gloss * (1 - rough)], -1))
        mp = stem + "_mask.png"
        if mask.any():
            Image.fromarray((mask * 255).astype(np.uint8)).save(mp)
        elif os.path.isfile(mp):
            os.remove(mp)
        for suf in ("_co", "_nohq", "_smdi"):
            to_paa(stem + suf + ".png", os.path.join(LIB, fam, mid + w + suf + ".paa"))
        s, p = BM.SPEC["jp_m_roof_kawara"]
        f = [1.1, 1.0, 0.8][lv]
        wb(os.path.join(LIB, fam, mid + w + ".rvmat"), rvmat(fam, mid, w, round(s * f, 3), int(p * f)))
        a = matcheck.check(stem + "_co.png", pal, "kawara_ibushi", TEX)
        b = matcheck.check(os.path.join(LIB, fam, mid + w + "_co.paa"), pal, "kawara_ibushi", TEX)
        a["shipped_paa"] = {k: b.get(k) for k in ("mean_srgb", "dE", "verdict", "warnings")}
        results.append(a)
        wears[w] = {"name": ["clean", "normal", "heavy"][lv], "look": "as jp_m_roof_kawara %s, plus courses" % w,
                    "co": lp(fam, mid, w, "_co.paa"), "rvmat": lp(fam, mid, w, ".rvmat"),
                    "target_srgb": [round(float(x), 1) for x in t], "masked_frac": round(float(mask.mean()), 3)}
    wb(os.path.join(LIB, fam, mid + ".json"), json.dumps({
        "id": mid, "family": fam, "palette_id": "kawara_ibushi", "palette_by_wear": {},
        "tile_size_m": 1.04, "tile_size_v_m": 0.94, "texture_px": 1024, "px_per_m": 985.0,
        "uv": "u = metres along the eave / 1.04 from a ken line; v = metres down the slope from a course line / 0.94",
        "grain": "4 columns (0.26) x 4 courses (0.235) per tile; butts at v = k/4",
        "penetration_rvmat": "dz\\data\\data\\penetration\\pottery.rvmat",
        "roadway_surface": "dz\\surfaces\\data\\roadway\\ceramic_tiles_roof_ext.paa",
        "wear": wears, "used_by": ["jp_p_roof_sangawara_field", "jp_p_roof_hongawara", "jp_p_roof_forms",
                                   "jp_p_roof_hisashi"],
        "used_on": "The continuous corrugated middle of kawara slopes, where PLAYBOOK §6.1 takes the course steps "
                   "from the normal map and AO; the modelled rows near eave and ridge use it too, so the roof "
                   "reads as one surface.",
        "sources": [{"derived_from": "jp_m_roof_kawara (make_textures.roof_kawara)"}],
        "normal_convention": "DirectX (green = down), like the library",
        "made_by": "parts/kit/make_part_materials.py (parts agent, 2026-09-27)"}, indent=1, ensure_ascii=False))
    wb(os.path.join(LIB, "checks_parts.json"), json.dumps({"check": "C1 palette (tools/matcheck), parts-agent materials",
                                                           "results": results}, indent=1))
    bad = 0
    for r in results:
        print("  %-4s %-30s %-14s mean %-15s dE %4.1f/%-2g paa dE %4.1f %s" % (
            r["verdict"], os.path.basename(r["file"])[:-7], r["palette_id"], "(%d,%d,%d)" % tuple(r["mean_srgb"]),
            r["dE"], r["tol"], r["shipped_paa"]["dE"], "; ".join(r["warnings"])))
        bad += r["verdict"] == "FAIL" or r["shipped_paa"]["verdict"] == "FAIL"
    print("matcheck: %d sets, %d FAIL" % (len(results), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
