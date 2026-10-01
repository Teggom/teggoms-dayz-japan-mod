"""M2: montage of the rendered bonji masks (research/materials/bonji_masks) for a visual check."""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "research", "materials", "bonji_masks")
ORDER = ["bonji_kha", "bonji_ha", "bonji_ra", "bonji_va", "bonji_a", "bonji_hum", "bonji_trah", "bonji_hrih",
         "bonji_ah"]


def main(out):
    T = 300
    im = Image.new("RGB", (T * 5, (T + 30) * 2), (40, 40, 40))
    d = ImageDraw.Draw(im)
    for i, n in enumerate(ORDER):
        p = os.path.join(SRC, n + ".png")
        if not os.path.exists(p):
            continue
        g = Image.open(p).convert("L")
        s = (T - 20) / max(g.size)
        g = g.resize((max(1, int(g.width * s)), max(1, int(g.height * s))), Image.LANCZOS)
        x, y = (i % 5) * T, (i // 5) * (T + 30)
        im.paste(Image.merge("RGB", [g, g, g]), (x + (T - g.width) // 2, y + (T - g.height) // 2))
        d.text((x + 8, y + T + 6), "%s %dx%d" % (n, *Image.open(p).size), fill=(230, 200, 120))
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
