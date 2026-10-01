"""M2: the bonji corner of a grave-atlas _ca.png composited over carved stone, all three wear levels side by side.

  python spikes/M2/look_atlas.py <dir with jp_m_decal_carved_text_grave_w{0,1,2}_ca.png> <out.png>
"""
import os
import sys

from PIL import Image, ImageDraw

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
BG = os.path.join(DEV, "data", "materials", "textures", "jp_m_stone_carved_w1_co.png")


def corner(src, lv, box=(340, 680, 1020, 952)):
    a = Image.open(os.path.join(src, "jp_m_decal_carved_text_grave_w%d_ca.png" % lv)).convert("RGBA")
    bg = Image.open(BG).convert("RGB").resize(a.size)
    bg.paste(a, (0, 0), a)
    return bg.crop(box)


def main(src, out):
    tiles = [corner(src, lv) for lv in range(3)]
    w, h = tiles[0].size
    im = Image.new("RGB", (w, (h + 24) * 3), (30, 30, 30))
    d = ImageDraw.Draw(im)
    for i, t in enumerate(tiles):
        im.paste(t, (0, i * (h + 24) + 24))
        d.text((6, i * (h + 24) + 6), "_w%d" % i, fill=(240, 210, 120))
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
