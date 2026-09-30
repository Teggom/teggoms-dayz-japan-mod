"""peek.py - tile renders into one small image to look at: python peek.py out.png a.png b.png ..."""
import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
W, H = 800, 450
cols = 2
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, H * rows), (20, 20, 20))
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((W, H))
    sheet.paste(im, ((i % cols) * W, (i // cols) * H))
sheet.save(out)
