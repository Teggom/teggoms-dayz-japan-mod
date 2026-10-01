"""M1: quick labelled montage of reference images (for looking, not shipped).

usage: python montage.py out.jpg W img1 img2 ...   (W = thumb width; images as paths)
"""
import os
import sys

from PIL import Image, ImageDraw


def main():
    out, W = sys.argv[1], int(sys.argv[2])
    paths = sys.argv[3:]
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        h = int(im.height * W / im.width)
        im = im.resize((W, h), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 14], fill=(0, 0, 0))
        d.text((3, 1), os.path.basename(p)[:40] + " %dx%d" % Image.open(p).size, fill=(255, 255, 0))
        thumbs.append(im)
    cols = 3 if len(thumbs) > 4 else len(thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    rh = [max(t.height for t in thumbs[r * cols:(r + 1) * cols]) for r in range(rows)]
    sheet = Image.new("RGB", (cols * W, sum(rh)), (40, 40, 40))
    y = 0
    for r in range(rows):
        for c, t in enumerate(thumbs[r * cols:(r + 1) * cols]):
            sheet.paste(t, (c * W, y))
        y += rh[r]
    sheet.save(out, quality=88)


if __name__ == "__main__":
    main()
