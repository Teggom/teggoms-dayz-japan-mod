"""Quick top-down footprint plot of showcase_items.json + buildings + other CSV rows (layout sanity check only).

  python spikes/SH1/quickplot.py x0 x1 z0 z1 out.png [px_per_m]
"""
import csv
import glob
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE, os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"),
          os.path.join(DEV, "spikes", "B_building", "kit"), os.path.join(DEV, "spikes", "C3")):
    sys.path.insert(0, p)
import layout_sh1 as L  # noqa: E402
import terrain_sh1 as T  # noqa: E402
from jpparts import decor as DC  # noqa: E402


def main(a):
    x0, x1, z0, z1 = map(float, a[:4])
    out = a[4]
    s = float(a[5]) if len(a) > 5 else 10.0
    W, Hh = int((x1 - x0) * s), int((z1 - z0) * s)
    im = Image.new("RGB", (W, Hh), (236, 232, 220))
    d = ImageDraw.Draw(im)
    F = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", max(9, int(s * 0.9)))

    def P(x, z):
        return ((x - x0) * s, (z1 - z) * s)
    # contours every 1 m
    import numpy as np
    for gx in np.arange(x0, x1, 2.0):
        for gz in np.arange(z0, z1, 2.0):
            g = T.ground(gx, gz)
            c = int(200 - (g - 25) * 6) % 256
            d.rectangle([P(gx, gz + 2), P(gx + 2, gz)], fill=(c, c, int(c * 0.9)))
    import dress_island as DI
    for key, wb, aprons, sboxes in DI.building_boxes():
        if wb[1] < x0 or wb[0] > x1 or wb[3] < z0 or wb[2] > z1:
            continue
        d.rectangle([P(wb[0], wb[3]), P(wb[1], wb[2])], outline=(120, 40, 40), width=2)
        d.text(P(wb[0] + 0.3, wb[3] - 0.3), key, font=F, fill=(120, 40, 40))
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) in ("SH1.csv", "C.csv"):
            continue
        for r in csv.DictReader(open(p)):
            x, z = float(r["x"]), float(r["z"])
            if x0 < x < x1 and z0 < z < z1:
                d.ellipse([P(x - 0.3, z + 0.3), P(x + 0.3, z - 0.3)], fill=(90, 90, 200))
    tr = T.trees()
    for tx, tz, ty, ts in tr:
        if x0 < tx < x1 and z0 < tz < z1:
            d.ellipse([P(tx - 0.5, tz + 0.5), P(tx + 0.5, tz - 0.5)], fill=(30, 110, 30))
    items = json.load(open(os.path.join(HERE, "showcase_items.json"), encoding="utf-8"))
    for it in items:
        if not (x0 < it["x"] < x1 and z0 < it["z"] < z1) or it.get("registry"):
            continue
        p3d, e = L.resolve(it["name"])
        b = L.fp_box(e, it["x"], it["z"], it["yaw"])
        col = (200, 60, 0) if (e is None or e["geo"]) else (0, 120, 200)
        d.rectangle([P(b[0], b[3]), P(b[1], b[2])], outline=col, width=1)
        if not it["id"][0] in "KI" or "E" not in it["id"]:
            d.text(P(it["x"], it["z"]), it["id"], font=F, fill=(0, 0, 0))
    im.save(out)
    print(out, im.size)


if __name__ == "__main__":
    main(sys.argv[1:])
