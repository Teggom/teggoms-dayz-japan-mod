"""Side-by-side of the candidate library textures (wood + iron families) for picking the tansu stand-ins."""
import os
from PIL import Image, ImageDraw, ImageFont

DEV = r"D:\DayZ-Server_AI-20260907-MultiMap\japan_dev"
TEX = os.path.join(DEV, "data", "materials", "textures")
OUT = os.path.join(DEV, "spikes", "effort_test", "max", "renders", "tex_compare.png")
MATS = ["jp_m_wood_street_dark", "jp_m_wood_weathered", "jp_m_wood_sooted", "jp_m_wood_bengara", "jp_m_wood_kuro",
        "jp_m_metal_iron"]
S = 300
F = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 14)
im = Image.new("RGB", (3 * (S + 8) + 8, len(MATS) * (S + 26) + 8), (230, 228, 224))
d = ImageDraw.Draw(im)
for r, m in enumerate(MATS):
    for c, w in enumerate(("_w0", "_w1", "_w2")):
        p = os.path.join(TEX, m + w + "_co.png")
        x, y = 8 + c * (S + 8), 8 + r * (S + 26)
        if os.path.isfile(p):
            t = Image.open(p).convert("RGB")
            mean = [round(v) for v in t.resize((1, 1), Image.BOX).getpixel((0, 0))]
            im.paste(t.resize((S, S), Image.LANCZOS), (x, y + 18))
            d.text((x, y), "%s%s  %dpx mean %s" % (m[5:], w, t.size[0], mean), font=F, fill=(20, 20, 20))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print(OUT, im.size)
