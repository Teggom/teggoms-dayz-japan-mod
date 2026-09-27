"""GSI (国土地理院) elevation tiles: fetch + decode + mosaic.

Tiles: https://cyberjapandata.gsi.go.jp/xyz/<layer>/<z>/<x>/<y>.png  (標高タイル, PNG encoding)
  dem5a_png  z15  5 m lidar (not everywhere)      dem_png  z14  10 m (DEM10B, nationwide)
PNG decoding (GSI spec): v = R*65536 + G*256 + B; v < 2^23 -> v*0.01 m; v == 2^23 -> no data;
v > 2^23 -> (v - 2^24)*0.01 m.
Tiles are cached under japan_dev/data/T_terrain/gsi/ and only downloaded once.
Credit (PDL1.0 / GSI terms): 「出典：国土地理院」 + a note that the data was edited (see CREDITS.md).
"""
import io
import math
import os
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CACHE = os.path.join(DEV, "data", "T_terrain", "gsi")
URL = "https://cyberjapandata.gsi.go.jp/xyz/{layer}/{z}/{x}/{y}.png"


def lonlat_to_tile(lon, lat, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    lr = math.radians(lat)
    y = (1.0 - math.log(math.tan(lr) + 1.0 / math.cos(lr)) / math.pi) / 2.0 * n
    return x, y


def tile_to_lonlat(x, y, z):
    n = 2 ** z
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lon, lat


def fetch_tile(layer, z, x, y):
    """Decoded tile (256x256 float32 metres, NaN = no data) or None when the tile does not exist."""
    path = os.path.join(CACHE, layer, str(z), str(x), "%d.png" % y)
    missing = path + ".404"
    if os.path.isfile(missing):
        return None
    if not os.path.isfile(path):
        import requests
        url = URL.format(layer=layer, z=z, x=x, y=y)
        r = requests.get(url, timeout=60, headers={"User-Agent": "japan_dev terrain spike (personal, non-commercial)"})
        time.sleep(0.2)   # be polite to the GSI server
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if r.status_code == 404:
            open(missing, "wb").close()
            return None
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.int64)
    v = im[:, :, 0] * 65536 + im[:, :, 1] * 256 + im[:, :, 2]
    h = np.where(v < 2 ** 23, v, v - 2 ** 24).astype(np.float64) * 0.01
    h[v == 2 ** 23] = np.nan
    return h.astype(np.float32)


def mosaic(layer, z, x0, y0, nx, ny):
    """Stitched array (ny*256, nx*256), north up, plus the (lon, lat) of the NW corner and SE corner."""
    out = np.full((ny * 256, nx * 256), np.nan, np.float32)
    got = 0
    for j in range(ny):
        for i in range(nx):
            t = fetch_tile(layer, z, x0 + i, y0 + j)
            if t is not None:
                out[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = t
                got += 1
    nw = tile_to_lonlat(x0, y0, z)
    se = tile_to_lonlat(x0 + nx, y0 + ny, z)
    return out, nw, se, got


def metres_per_pixel(lat, z):
    return 40075016.686 * math.cos(math.radians(lat)) / (2 ** z * 256)
