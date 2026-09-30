"""Contact sheet of renders/*.png -> contact_sheet.png (2 rows: intact, ransacked)."""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REN = os.path.join(HERE, "renders")
VIEWS = ["front", "3q", "back", "closeup", "side_handle", "lod2_3q", "lod3_3q"]
S = 360
img = Image.new("RGB", (S * len(VIEWS), (S + 24) * 2), (30, 30, 30))
d = ImageDraw.Draw(img)
for r, state in enumerate(("intact", "ransacked")):
    for c, v in enumerate(VIEWS):
        p = os.path.join(REN, "%s_%s.png" % (state, v))
        if os.path.isfile(p):
            img.paste(Image.open(p).convert("RGB").resize((S, S)), (c * S, r * (S + 24) + 24))
        d.text((c * S + 6, r * (S + 24) + 6), "%s / %s" % (state, v), fill=(240, 240, 240))
img.save(os.path.join(HERE, "contact_sheet.png"))
print("wrote contact_sheet.png", img.size)
