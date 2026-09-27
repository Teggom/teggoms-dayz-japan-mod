#!/usr/bin/env python3
"""Download the CC0 Poly Haven source textures for the machiya kit into japan_dev/data/B/polyhaven/<id>/.

Every asset is CC0 (Poly Haven's only licence). Writes data/B/polyhaven/manifest.json with author, real-world
dimensions and URLs, which CREDITS.md is built from.   Usage:  python fetch_textures.py
"""
import json
import os
import sys

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(DEV, "data", "B", "polyhaven")

ASSETS = [
    "tatami_mat",            # tatami
    "white_plaster_02",      # white plaster walls
    "clay_plaster",          # earth plaster walls (material mix option)
    "grey_roof_tiles",       # kawara roof
    "japanese_cedar_planks", # timber (darkened for posts and beams)
    "hinoki_planks",         # floor boards
    "dark_planks",           # weathered exterior boards / plank doors
    "clay_floor_001",        # earthen floor of the toriniwa
    "japanese_stone_wall",   # foundation and stepping stones
]
MAPS = {"Diffuse": "diff", "nor_dx": "nor_dx", "Rough": "rough"}
RES = "1k"


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for a in ASSETS:
        info = requests.get("https://api.polyhaven.com/info/" + a, timeout=30).json()
        files = requests.get("https://api.polyhaven.com/files/" + a, timeout=30).json()
        d = os.path.join(OUT, a)
        os.makedirs(d, exist_ok=True)
        entry = {"name": info.get("name"), "authors": list(info.get("authors", {}).keys()),
                 "dimensions_mm": info.get("dimensions"), "licence": "CC0 1.0",
                 "page": "https://polyhaven.com/a/" + a, "files": {}}
        for key, short in MAPS.items():
            url = files[key][RES]["jpg"]["url"]
            dst = os.path.join(d, "%s_%s_%s.jpg" % (a, short, RES))
            if not os.path.isfile(dst):
                r = requests.get(url, timeout=120)
                r.raise_for_status()
                with open(dst, "wb") as f:
                    f.write(r.content)
            entry["files"][short] = url
            print(a, short, os.path.getsize(dst))
        manifest[a] = entry
    with open(os.path.join(OUT, "manifest.json"), "wb") as f:
        f.write(json.dumps(manifest, indent=1).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
