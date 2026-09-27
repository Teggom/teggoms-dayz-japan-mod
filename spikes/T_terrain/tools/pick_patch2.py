"""One-off: whole-block hillshade with a numbered 1.7 km grid, to pick a natural (non-built-up) hill patch by eye."""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsi_dem  # noqa: E402

OUT = os.path.join(gsi_dem.DEV, "spikes", "T_terrain", "previews")
a = np.load(os.path.join(gsi_dem.CACHE, "explore_dem5a_png_z15.npy"))
b = np.load(os.path.join(gsi_dem.CACHE, "explore_dem_png_z14.npy"))
mpp = gsi_dem.metres_per_pixel(35.23, 15)
# fill dem5a holes from dem10b (z14 is 2x coarser; the z14 block starts one z15 tile-column earlier? align by lon/lat)
x5, y5 = gsi_dem.lonlat_to_tile(138.99, 35.28, 15)
x4, y4 = gsi_dem.lonlat_to_tile(138.99, 35.28, 14)
ox = int(x5) * 256 - int(x4) * 2 * 256
oy = int(y5) * 256 - int(y4) * 2 * 256
b2 = np.kron(b, np.ones((2, 2), np.float32))[oy:oy + a.shape[0], ox:ox + a.shape[1]]
filled = np.where(np.isfinite(a), a, b2)
np.save(os.path.join(gsi_dem.CACHE, "hakone_filled_z15.npy"), filled)
print("offset", ox, oy, "diff where both valid: median %.2f m" % np.nanmedian(np.abs(a - b2)))
gy, gx = np.gradient(filled, mpp)
slope = np.arctan(np.hypot(gx, gy))
aspect = np.arctan2(-gx, gy)
az, alt = np.radians(315), np.radians(45)
hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
img = Image.fromarray((np.clip(hs, 0, 1) * 255).astype(np.uint8)).convert("RGB")
d = ImageDraw.Draw(img)
win = int(round(1700 / mpp))
k = 0
for y in range(0, a.shape[0] - win + 1, win // 2):
    for x in range(0, a.shape[1] - win + 1, win // 2):
        w = filled[y:y + win, x:x + win]
        rel = np.percentile(w, 98) - np.percentile(w, 2)
        d.text((x + win // 2 - 20, y + win // 2 - 8), "%d:%d" % (k, rel), fill=(255, 0, 0))
        k += 1
for y in range(0, a.shape[0], win // 2):
    d.line([(0, y), (a.shape[1], y)], fill=(0, 0, 255))
for x in range(0, a.shape[1], win // 2):
    d.line([(x, 0), (x, a.shape[0])], fill=(0, 0, 255))
img.resize((a.shape[1] // 2, a.shape[0] // 2)).save(os.path.join(OUT, "patch_grid.png"))
print("win", win, "grid step", win // 2)
