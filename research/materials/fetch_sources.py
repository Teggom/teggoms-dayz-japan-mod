#!/usr/bin/env python3
"""Download the CC0 Poly Haven source maps for the jp_common material library into data/materials/polyhaven/<id>/.

Poly Haven publishes everything as CC0 1.0. A manifest (author, real size, URLs) is written next to the files and
CREDITS.md is built from it. Requests carry only a generic User-Agent (README rule 4: no personal data).
Usage:  python fetch_sources.py        (skips files already on disk)
"""
import json
import os
import sys

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "data", "materials", "polyhaven")
UA = {"User-Agent": "JapanDevResearch/1.0 (DayZ mod research)"}

# asset id -> what it becomes (the recipes live in make_textures.py)
ASSETS = {
    "weathered_planks": "jp_m_wood_weathered",
    "japanese_cedar_planks": "jp_m_wood_street_dark, jp_m_wood_bengara, jp_m_wood_sooted",
    "black_painted_planks": "jp_m_wood_kuro",
    "clay_plaster": "jp_m_wall_arakabe, jp_m_wall_nakanuri (smoothed)",
    "white_plaster_02": "jp_m_wall_shikkui",
    "reed_roof_04": "jp_m_roof_thatch",
    "wood_planks_grey": "jp_m_roof_kureita, jp_m_roof_kokera, jp_m_roof_kakigara (board grain)",
    "worn_rock_natural_01": "jp_m_stone_field",
    "rock_surface": "jp_m_stone_cut",
    "seaside_rock": "jp_m_stone_river",
    "rust_coarse_01": "jp_m_metal_iron (rust layer)",
}
MAPS = {"Diffuse": "diff", "nor_dx": "nor_dx", "Rough": "rough"}
RES = "1k"


def get(url, **kw):
    r = requests.get(url, headers=UA, timeout=kw.pop("timeout", 60))
    r.raise_for_status()
    return r


def main():
    os.makedirs(OUT, exist_ok=True)
    man_path = os.path.join(OUT, "manifest.json")
    manifest = json.load(open(man_path, encoding="utf-8")) if os.path.isfile(man_path) else {}
    manifest = {k: v for k, v in manifest.items() if k in ASSETS}         # drop assets no longer used
    for a, use in ASSETS.items():
        d = os.path.join(OUT, a)
        os.makedirs(d, exist_ok=True)
        need = [s for s in MAPS.values() if not os.path.isfile(os.path.join(d, "%s_%s_%s.jpg" % (a, s, RES)))]
        if not need and a in manifest:
            manifest[a]["used_for"] = use
            continue
        info = get("https://api.polyhaven.com/info/" + a).json()
        files = get("https://api.polyhaven.com/files/" + a).json()
        entry = {"name": info.get("name"), "authors": list(info.get("authors", {}).keys()),
                 "dimensions_mm": info.get("dimensions"), "licence": "CC0 1.0",
                 "page": "https://polyhaven.com/a/" + a, "used_for": use, "files": {}}
        for key, short in MAPS.items():
            src = files.get(key)
            if src is None and key == "Rough" and "arm" in files:      # roughness packed in ARM.g
                src = files["arm"]
            url = src[RES]["jpg"]["url"]
            dst = os.path.join(d, "%s_%s_%s.jpg" % (a, short, RES))
            if not os.path.isfile(dst):
                with open(dst, "wb") as f:
                    f.write(get(url, timeout=180).content)
            entry["files"][short] = url
            print(a, short, os.path.getsize(dst))
        manifest[a] = entry
    with open(man_path, "wb") as f:
        f.write(json.dumps(manifest, indent=1).encode("utf-8"))
    print("manifest:", man_path, len(manifest), "assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
