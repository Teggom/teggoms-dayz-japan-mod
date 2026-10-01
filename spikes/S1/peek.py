"""Quick look: tile the given renders/<name>_row.png into one image (scratch preview, not a deliverable)."""
import os
import sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
names = [a for a in sys.argv[2:]]
out = sys.argv[1]
ims = [Image.open(os.path.join(HERE, "renders", n + ".png")).convert("RGB") for n in names
       if os.path.isfile(os.path.join(HERE, "renders", n + ".png"))]
w, h = 640, 360
cols = 3
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
for i, im in enumerate(ims):
    sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
sheet.save(out, quality=85)
print(out, sheet.size)
