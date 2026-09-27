"""One-off: rank 1.6 km windows of the Hakone DEM5A block by relief and write hillshade previews of the best."""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsi_dem  # noqa: E402

OUT = os.path.join(gsi_dem.DEV, "spikes", "T_terrain", "previews")
a = np.load(os.path.join(gsi_dem.CACHE, "explore_dem5a_png_z15.npy"))
mpp = gsi_dem.metres_per_pixel(35.23, 15)
win = int(round(1700 / mpp))
step = win // 6
cands = []
for y in range(0, a.shape[0] - win, step):
    for x in range(0, a.shape[1] - win, step):
        w = a[y:y + win, x:x + win]
        if not np.isfinite(w).all():
            continue
        p2, p98 = np.percentile(w, [2, 98])
        gy, gx = np.gradient(w, mpp)
        slope = np.degrees(np.arctan(np.hypot(gx, gy)))
        cands.append((p98 - p2, float(np.median(slope)), float((slope > 35).mean()), x, y))
print("windows", len(cands), "win px", win, "m/px %.2f" % mpp)
good = [c for c in cands if 180 <= c[0] <= 320 and c[2] < 0.08]
good.sort(key=lambda c: -c[1])
for c in good[:12]:
    lon, lat = gsi_dem.tile_to_lonlat(0, 0, 15)
    print("relief %.0f m  median slope %.1f  steep %.3f  at px (%d,%d)" % c)


def hillshade(w):
    gy, gx = np.gradient(w, mpp)
    az, alt = np.radians(315), np.radians(45)
    slope = np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    return (np.clip(hs, 0, 1) * 255).astype(np.uint8)


tiles = []
for c in good[:6]:
    x, y = c[3], c[4]
    tiles.append(Image.fromarray(hillshade(a[y:y + win, x:x + win])).resize((300, 300)))
if tiles:
    sheet = Image.new("L", (300 * len(tiles), 300))
    for i, t in enumerate(tiles):
        sheet.paste(t, (300 * i, 0))
    sheet.save(os.path.join(OUT, "patch_candidates.png"))
np.save(os.path.join(gsi_dem.CACHE, "patch_candidates.npy"), np.array([c[3:5] for c in good[:6]]))
