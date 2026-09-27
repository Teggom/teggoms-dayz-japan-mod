"""Make 2x2 contact sheets of the reference images with a labelled 10x10 grid, for choosing sample boxes.

Output: data/playbook/work/grid_XX.png (not shipped, not in git).
"""
import os, glob
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
REFS = os.path.join(ROOT, "data", "playbook", "refs")
WORK = os.path.join(ROOT, "data", "playbook", "work")
W = 760


def tile(path):
    im = Image.open(path).convert("RGB")
    h = int(im.height * W / im.width)
    if h > 760:
        h = 760
        w = int(im.width * h / im.height)
    else:
        w = W
    im = im.resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    for i in range(1, 10):
        x = int(w * i / 10)
        y = int(h * i / 10)
        d.line([(x, 0), (x, h)], fill=(255, 0, 255), width=1)
        d.line([(0, y), (w, y)], fill=(255, 0, 255), width=1)
    for i in range(10):
        d.text((int(w * i / 10) + 2, 2), str(i), fill=(255, 255, 0))
        d.text((2, int(h * i / 10) + 2), str(i), fill=(0, 255, 255))
    d.text((4, h - 14), os.path.basename(path), fill=(255, 255, 255))
    return im


def main():
    os.makedirs(WORK, exist_ok=True)
    files = sorted(glob.glob(os.path.join(REFS, "*.jpg")))
    for s in range(0, len(files), 4):
        tiles = [tile(p) for p in files[s:s + 4]]
        sheet = Image.new("RGB", (2 * W + 10, 2 * 770), (20, 20, 20))
        for k, t in enumerate(tiles):
            sheet.paste(t, ((k % 2) * (W + 10), (k // 2) * 770))
        sheet.save(os.path.join(WORK, "grid_%02d.png" % (s // 4)))


if __name__ == "__main__":
    main()
