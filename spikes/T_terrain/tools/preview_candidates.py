"""One-off: compose the island with several Hakone patch windows and write a contact sheet of hillshades."""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsi_dem  # noqa: E402
import terrain  # noqa: E402

OUT = os.path.join(gsi_dem.DEV, "spikes", "T_terrain", "previews")
full = np.load(os.path.join(gsi_dem.CACHE, "hakone_filled_z15.npy"))
mpp = gsi_dem.metres_per_pixel(35.23, 15)
half = int(round(900 / mpp))


def hillshade(h, cell):
    gz, gx = np.gradient(h.astype(np.float64), cell)
    gz = -gz                                    # row 0 = south -> flip for image
    slope = np.arctan(np.hypot(gx, gz))
    aspect = np.arctan2(-gx, gz)
    az, alt = np.radians(315), np.radians(45)
    hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    return np.clip(hs, 0, 1)


def colour(h):
    hs = hillshade(h, terrain.CELL)[::-1]
    hh = h[::-1]
    rgb = np.zeros(hh.shape + (3,))
    land = hh > 0
    t = np.clip(hh / 250.0, 0, 1)[..., None]
    rgb[land] = ((1 - t) * np.array([0.45, 0.62, 0.35]) + t * np.array([0.75, 0.68, 0.55]))[land]
    rgb[~land] = np.array([0.15, 0.3, 0.55])
    rgb *= (0.35 + 0.65 * hs)[..., None]
    return Image.fromarray((rgb * 255).astype(np.uint8))


layout = {"patch_origin": (1024.0, 1300.0), "road": [(1024, 1124), (1024, 1300)], "road_half_width": 3.0,
          "canal": [(1850, 900), (1700, 900)], "canal_half_width": 8.0, "pond": (800, 1000, 16, 27.0)}
cands = {"A_futago": (1300, 1900), "B_koma": (1150, 1750), "C_south": (1100, 2350), "D_ne": (2100, 800),
         "E_east": (2100, 1500), "F_se": (2000, 2500)}
sheet = Image.new("RGB", (512 * 3, 512 * 2 + 40), (255, 255, 255))
dr = ImageDraw.Draw(sheet)
for k, (name, (cx, cy)) in enumerate(cands.items()):
    patch = full[cy - half:cy + half, cx - half:cx + half]
    r = terrain.compose(patch, mpp, layout)
    img = colour(r["h"])
    sheet.paste(img, ((k % 3) * 512, (k // 3) * 532))
    dr.text(((k % 3) * 512 + 5, (k // 3) * 532 + 514), "%s vscale %.2f max %.0f" % (name, r["vscale"], r["h"].max()), fill=(0, 0, 0))
    print(name, "vscale %.2f" % r["vscale"], "max %.1f" % r["h"].max(), "land %.2f km2" % ((r["h"] > 0).sum() * 16 / 1e6))
sheet.save(os.path.join(OUT, "island_candidates.png"))
