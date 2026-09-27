"""One-off: download a Hakone block of GSI tiles and look for a good 1.6 km hill patch. Writes previews."""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsi_dem  # noqa: E402

OUT = os.path.join(gsi_dem.DEV, "spikes", "T_terrain", "previews")
os.makedirs(OUT, exist_ok=True)

# Hakone caldera and its rim: roughly 139.00-139.08 E, 35.19-35.27 N
lon0, lat0, lon1, lat1 = 138.99, 35.28, 139.09, 35.18
for layer, z in (("dem5a_png", 15), ("dem_png", 14)):
    x0, y0 = gsi_dem.lonlat_to_tile(lon0, lat0, z)
    x1, y1 = gsi_dem.lonlat_to_tile(lon1, lat1, z)
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    arr, nw, se, got = gsi_dem.mosaic(layer, z, x0, y0, x1 - x0 + 1, y1 - y0 + 1)
    mpp = gsi_dem.metres_per_pixel(35.23, z)
    valid = np.isfinite(arr)
    print(layer, z, "tiles", (x1 - x0 + 1) * (y1 - y0 + 1), "got", got, "shape", arr.shape, "m/px %.2f" % mpp,
          "valid %.1f%%" % (100 * valid.mean()), "range", np.nanmin(arr) if valid.any() else None,
          np.nanmax(arr) if valid.any() else None, "NW", nw, "SE", se)
    if valid.any():
        a = np.where(valid, arr, np.nanmin(arr))
        g = ((a - a.min()) / (a.max() - a.min()) * 255).astype(np.uint8)
        g[~valid] = 0
        Image.fromarray(g).save(os.path.join(OUT, "explore_%s_z%d.png" % (layer, z)))
        np.save(os.path.join(gsi_dem.CACHE, "explore_%s_z%d.npy" % (layer, z)), arr)
