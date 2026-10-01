"""Quick look grid: python spikes/FP1/montage.py <out.jpg> <cols> <png> ... (each tile 400 px wide, labelled)."""
import os
import sys

from PIL import Image, ImageDraw


def main(argv):
    out, cols, files = argv[0], int(argv[1]), argv[2:]
    T = 400
    ims = []
    for f in files:
        im = Image.open(f).convert("RGB")
        w, h = im.size
        ims.append((os.path.basename(f), im.resize((T, int(T * h / w)))))
    th = max(i.size[1] for _, i in ims)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * T, rows * (th + 16)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for k, (n, im) in enumerate(ims):
        x, y = (k % cols) * T, (k // cols) * (th + 16)
        sheet.paste(im, (x, y + 16))
        d.text((x + 4, y + 2), n[:60], fill=(0, 0, 0))
    sheet.save(out, quality=85)


if __name__ == "__main__":
    main(sys.argv[1:])
