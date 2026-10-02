"""D3: an overview of the test island around the yard: terrain heights (shaded, 1 m contours), every placed object
(all test/placements/*.csv points; buildings drawn as their record footprints), trees, reserved spots.
  python spikes/D3/overview.py [x0 x1 z0 z1] -> spikes/D3/renders/_overview.png"""
import csv, glob, json, os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [os.path.join(DEV, "spikes", "SH1"), os.path.join(DEV, "spikes", "W2F"), os.path.join(DEV, "buildings"),
                os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")]
import terrain_sh1 as T
x0, x1, z0, z1 = [float(v) for v in sys.argv[1:5]] if len(sys.argv) > 4 else (880.0, 1180.0, 900.0, 1280.0)
S = 3.0
W, Hh = int((x1 - x0) * S), int((z1 - z0) * S)
img = Image.new("RGB", (W, Hh))
px = img.load()
g = np.zeros((Hh, W))
for j in range(0, Hh, 3):
    for i in range(0, W, 3):
        g[j, i] = T.ground(x0 + i / S, z1 - j / S)
for j in range(0, Hh, 3):
    for i in range(0, W, 3):
        h = g[j, i]
        c = int(max(0, min(255, 120 + (h - 25.0) * 9)))
        col = (c, c, int(c * 0.9)) if abs(h - 25.0) > 0.05 else (150, 170, 140)
        if int(h) != int(g[j, max(0, i - 3)]) or int(h) != int(g[max(0, j - 3), i]):
            col = (60, 60, 60)
        for dj in range(3):
            for di in range(3):
                if j + dj < Hh and i + di < W:
                    px[i + di, j + dj] = col
d = ImageDraw.Draw(img)
def P(x, z):
    return ((x - x0) * S, (z1 - z) * S)
recs = {}
for p in glob.glob(os.path.join(DEV, "buildings", "*", "records", "*.json")) + glob.glob(os.path.join(DEV, "buildings", "*", "record.json")):
    try:
        r = json.loads(open(p, "rb").read().decode("utf-8"))
    except Exception:
        continue
    if r.get("model") and r.get("bbox"):
        recs[r["model"].lstrip("\\").lower()] = r["bbox"]
import layout_w2f as LW
for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
    for row in csv.DictReader(open(p, newline="")):
        x, z = float(row["x"]), float(row["z"])
        k = row["p3d"].lower()
        if k in recs:
            poly = LW.corners(recs[k], (x, 25.0, z), float(row["yaw_deg"]))
            d.polygon([P(*q) for q in poly], outline=(200, 30, 30))
        else:
            q = P(x, z)
            d.ellipse([q[0] - 2, q[1] - 2, q[0] + 2, q[1] + 2], fill=(30, 30, 200))
for t in T.trees():
    q = P(float(t[0]), float(t[1]))
    d.ellipse([q[0] - 3, q[1] - 3, q[0] + 3, q[1] + 3], outline=(20, 120, 20))
for nm, (a0, a1, c0, c1) in LW.RESERVED.items():
    d.rectangle([P(a0, c1), P(a1, c0)], outline=(240, 160, 0))
for v in range(int(x0 // 20 * 20), int(x1) + 1, 20):
    d.line([P(v, z0), P(v, z1)], fill=(255, 255, 255) if v % 100 else (255, 255, 0))
    d.text((P(v, z1)[0] + 2, 2), str(v), fill=(255, 255, 0))
for v in range(int(z0 // 20 * 20), int(z1) + 1, 20):
    d.line([P(x0, v), P(x1, v)], fill=(255, 255, 255) if v % 100 else (255, 255, 0))
    d.text((2, P(x0, v)[1] + 2), str(v), fill=(255, 255, 0))
out = os.path.join(HERE, "renders", "_overview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print(out, img.size)
