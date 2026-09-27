"""Draw candidate sample boxes on reference images so they can be checked by eye before sampling.

Usage: python box_check.py out.png "img_id:x0,y0,x1,y1;x0,y0,x1,y1" "img_id:..." ...
"""
import os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
REFS = os.path.join(ROOT, "data", "playbook", "refs")
WORK = os.path.join(ROOT, "data", "playbook", "work")
W = 700

tiles = []
for arg in sys.argv[2:]:
    img_id, boxes = arg.split(":")
    im = Image.open(os.path.join(REFS, img_id + ".jpg")).convert("RGB")
    h = int(im.height * W / im.width)
    im = im.resize((W, h))
    d = ImageDraw.Draw(im)
    for k, b in enumerate(boxes.split(";")):
        x0, y0, x1, y1 = [float(v) for v in b.split(",")]
        d.rectangle([x0 * W, y0 * h, x1 * W, y1 * h], outline=(0, 255, 0), width=2)
        d.text((x0 * W + 3, y0 * h + 2), str(k), fill=(0, 255, 0))
    d.text((4, 4), img_id, fill=(255, 255, 0))
    tiles.append(im)
cols = 2
rows = (len(tiles) + 1) // 2
hmax = max(t.height for t in tiles)
sheet = Image.new("RGB", (cols * (W + 8), rows * (hmax + 8)), (20, 20, 20))
for k, t in enumerate(tiles):
    sheet.paste(t, ((k % cols) * (W + 8), (k // cols) * (hmax + 8)))
sheet.save(os.path.join(WORK, sys.argv[1]))
