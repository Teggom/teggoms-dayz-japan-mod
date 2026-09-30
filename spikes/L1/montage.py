"""Quick look: tile row renders (spikes/L1/renders/<prop>_row.png) into one image for review.
python montage.py out.png prop [prop ...]"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
out, props = sys.argv[1], sys.argv[2:]
W, H = 800, 450
cols = 2
rows = (len(props) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, H * rows), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for i, p in enumerate(props):
    pid = p if p.startswith("jp_f_") else "jp_f_" + p
    f = os.path.join(HERE, "renders", pid + "_row.png")
    if os.path.isfile(f):
        sheet.paste(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS), ((i % cols) * W, (i // cols) * H))
    d.text(((i % cols) * W + 8, (i // cols) * H + 6), pid, fill=(255, 255, 0))
sheet.save(out)
