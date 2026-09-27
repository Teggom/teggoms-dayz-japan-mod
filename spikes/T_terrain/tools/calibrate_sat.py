"""One-off calibration: per-surface satellite colour as vanilla Chernarus paints it.

For a spread of vanilla layer tiles: convert s_/m_ paa -> png (ImageToPAA), decode the mask with the 6-slot rule
(black / R / G / B@255 / B@128 / B@0, see layers.py) against the tile's full rvmat (the one with the most slots),
and take the median satellite colour per surface. Writes tools/sat_colours.json (used by layers.satellite).
"""
import json
import os
import re
import subprocess

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CACHE = os.path.join(DEV, "data", "T_terrain", "vanilla_tiles")
LAY = r"P:\DZ\worlds\chernarusplus\data\layers"
I2P = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\ImageToPAA\ImageToPAA.exe"
os.makedirs(CACHE, exist_ok=True)

names = os.listdir(LAY)
samples = {}
tiles = [(c, r) for c in range(2, 31, 4) for r in range(2, 31, 4)] + [(c, 31) for c in range(4, 30, 5)] + [(31, r) for r in range(3, 30, 5)]
for c, r in tiles:
    tag = "%03d_%03d" % (c, r)
    cands = [n for n in names if n.startswith("p_%03d-%03d_" % (c, r)) and n.endswith(".rvmat")]
    if not cands:
        continue
    full = max(cands, key=lambda n: sum(1 for p in n[:-6].split("_")[2:] if p != "n"))
    txt = open(os.path.join(LAY, full)).read()
    stages = dict(re.findall(r'class Stage(\d+)\s*\{\s*texture="([^"]*)"', txt))
    slots = []
    for k in range(6):
        ca = stages.get(str(4 + 2 * k), "")
        m = re.search(r"\\([a-z0-9_]+)_ca\.paa$", ca)
        slots.append(m.group(1) if m else None)
    pngs = []
    for pre, suf in (("s", "lco"), ("m", "lca")):
        png = os.path.join(CACHE, "%s_%s.png" % (pre, tag))
        if not os.path.isfile(png):
            subprocess.run([I2P, os.path.join(LAY, "%s_%s_%s.paa" % (pre, tag, suf)), png], check=True, capture_output=True)
        pngs.append(png)
    s = np.asarray(Image.open(pngs[0]).convert("RGB")).reshape(-1, 3)
    m = np.asarray(Image.open(pngs[1]).convert("RGBA")).reshape(-1, 4).astype(int)
    R, G, B, A = m[:, 0], m[:, 1], m[:, 2], m[:, 3]
    slot = np.full(len(m), -1)
    slot[(R < 64) & (G < 64) & (B < 64)] = 0
    slot[(R >= 128) & (G < 64) & (B < 64)] = 1
    slot[(G >= 128) & (R < 64) & (B < 64)] = 2
    blue = (B >= 128) & (R < 64) & (G < 64)
    slot[blue & (A >= 192)] = 3
    slot[blue & (A >= 64) & (A < 192)] = 4
    slot[blue & (A < 64)] = 5
    for k in range(6):
        if slots[k]:
            px = s[slot == k]
            if len(px) > 200:
                samples.setdefault(slots[k], []).append(px[::7])
out = {}
for name, lst in sorted(samples.items()):
    a = np.concatenate(lst)
    out[name] = [float(v) for v in np.median(a, axis=0)]
    print("%-24s n=%7d median RGB %s  p25 %s  p75 %s" % (name, len(a), np.median(a, axis=0), np.percentile(a, 25, axis=0), np.percentile(a, 75, axis=0)))
with open(os.path.join(HERE, "sat_colours.json"), "wb") as f:
    f.write(json.dumps(out, indent=1).encode("utf-8"))
