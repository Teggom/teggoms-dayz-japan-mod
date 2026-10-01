"""M1: quick look at the draft textures beside the existing material they complement (not the final sheet)."""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(DEV, "data", "materials", "textures")
ROWS = [("jp_m_ground_earth_bare", "jp_m_ground_leaf_litter"), ("jp_m_wood_new", "jp_m_wood_weathered"),
        ("jp_m_wood_silver", "jp_m_wood_weathered"), ("jp_m_floor_tatami_heri_cha", "jp_m_floor_tatami_heri"),
        ("jp_m_wicker_aged", "jp_m_bamboo_weave"), ("jp_m_wood_firewood", "jp_m_wood_weathered"),
        ("jp_m_wood_endgrain_firewood", "jp_m_wood_endgrain")]
C = 200


def tile(p):
    im = Image.open(p).convert("RGB")
    s = min(im.size)
    return im.crop((0, 0, s, s)).resize((C, C), Image.LANCZOS)


def main():
    sheet = Image.new("RGB", (C * 4 + 10, (C + 16) * len(ROWS)), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    for r, (new, old) in enumerate(ROWS):
        y = r * (C + 16)
        sheet.paste(tile(os.path.join(TEX, old + "_w1_co.png")), (0, y + 16))
        d.text((2, y + 2), "before: " + old + " _w1", fill=(255, 200, 120))
        for lv in range(3):
            sheet.paste(tile(os.path.join(HERE, "draft", "%s_w%d_co.png" % (new, lv))), (10 + C * (lv + 1), y + 16))
            d.text((12 + C * (lv + 1), y + 2), "%s _w%d" % (new[5:], lv), fill=(200, 255, 200))
    sheet.save(os.path.join(HERE, "look", "draft_sheet.jpg"), quality=88)


if __name__ == "__main__":
    main()
