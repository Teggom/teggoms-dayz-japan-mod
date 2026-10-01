"""M1 contact sheets -> research/materials/contact_sheets/m1_1_materials.jpg, m1_2_props.jpg, m1_3_text.jpg

1 materials: per new material the reference crops it was sampled from, the sampled swatch, BEFORE (what the props used),
  AFTER _w0 / _w1 / _w2.   2 props: before / after renders (B3a / B3b renderers) + a tatami heri mock-up.
3 text: the two grave atlases (carved on stone, ink on new wood) with their cell names.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(DEV, "data", "materials", "textures")
OUT = os.path.join(DEV, "research", "materials", "contact_sheets")
SAMP = json.load(open(os.path.join(HERE, "samples.json"), encoding="utf-8"))["samples"]
try:
    F = ImageFont.truetype("arial.ttf", 15)
    FB = ImageFont.truetype("arialbd.ttf", 20)
except OSError:
    F = FB = ImageFont.load_default()
try:
    FJ = ImageFont.truetype("C:/Windows/Fonts/YuGothM.ttc", 15)    # the cell list has kanji (labels only)
except OSError:
    FJ = F
BG = (34, 34, 34)
C = 220

ROWS = [  # new material, sample id (spikes/M1/samples.json), before material, title
    ("jp_m_ground_earth_bare", "earth_bare", "jp_m_ground_leaf_litter", "1 bare earth (grave mounds, paths): 148,130,108"),
    ("jp_m_wood_new", "wood_new", "jp_m_wood_weathered", "2 pale NEW wood: 172,146,129 (i04, WB on the ash)"),
    ("jp_m_wood_silver", "wood_silver", "jp_m_wood_weathered", "3 silver-grey weathered wood: 126,125,120"),
    ("jp_m_floor_tatami_heri_cha", None, "jp_m_floor_tatami_heri", "4 brown (cha) heri: cha_koge 106,77,50 (reference)"),
    ("jp_m_wicker_aged", "wicker_aged", "jp_m_bamboo_weave", "8a kori wicker: 137,110,86 (CC0 scan proxy)"),
    ("jp_m_wood_firewood", "firewood_split", "jp_m_wood_weathered", "8b firewood sides: 108,92,60 (i22)"),
    ("jp_m_wood_endgrain_firewood", "firewood_end", "jp_m_wood_endgrain", "8c firewood ends: 160,130,67 (i22)"),
]


def tile(name):
    p = os.path.join(TEX, name + "_co.png")
    im = Image.open(p).convert("RGB")
    s = min(im.size)
    return im.crop((0, 0, s, s)).resize((C, C), Image.LANCZOS)


def fit(im, w, h):
    im = im.convert("RGB")
    sc = min(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    out = Image.new("RGB", (w, h), BG)
    out.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return out


def sheet_materials():
    W = 4 * 150 + 120 + 4 * (C + 8) + 20
    H = len(ROWS) * (C + 40) + 50
    sh = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sh)
    d.text((10, 10), "M1 materials: reference crops -> sampled swatch | BEFORE (what the props used) | AFTER _w0 _w1 _w2",
           font=FB, fill=(255, 255, 255))
    y = 50
    for mid, sid, before, title in ROWS:
        d.text((10, y), title + "   [" + mid + "]", font=F, fill=(255, 220, 140))
        yy = y + 20
        x = 10
        if sid:
            k = 0
            while os.path.isfile(os.path.join(HERE, "crops", "%s_%d.png" % (sid, k))) and k < 4:
                sh.paste(fit(Image.open(os.path.join(HERE, "crops", "%s_%d.png" % (sid, k))), 145, C), (x, yy))
                k += 1
                x += 150
            rgb = tuple(SAMP[sid]["srgb"])
        else:
            d.text((x, yy + 90), "no local photo of a brown heri:\nvalue from the palette reference\n(ja.wikipedia koge-cha "
                   "#6A4D32)", font=F, fill=(200, 200, 200))
            rgb = (106, 77, 50)
        x = 10 + 4 * 150
        d.rectangle([x, yy, x + 110, yy + C], fill=rgb)
        d.text((x + 4, yy + C - 20), "%d,%d,%d" % rgb, font=F, fill=(255, 255, 255) if sum(rgb) < 380 else (0, 0, 0))
        x += 120
        sh.paste(tile(before + "_w1"), (x, yy))
        d.text((x + 4, yy + 4), "BEFORE " + before[5:] + " _w1", font=F, fill=(255, 120, 120))
        x += C + 8
        for lv in range(3):
            sh.paste(tile("%s_w%d" % (mid, lv)), (x, yy))
            d.text((x + 4, yy + 4), "AFTER _w%d" % lv, font=F, fill=(140, 255, 140))
            x += C + 8
        y += C + 40
    sh.save(os.path.join(OUT, "m1_1_materials.jpg"), quality=88)


def heri_mock():
    """Two tatami mats side by side with black heri (before) and cha heri (after), flat 2D (texture tiles)."""
    out = Image.new("RGB", (900, 300), BG)
    d = ImageDraw.Draw(out)
    mat = Image.open(os.path.join(TEX, "jp_m_floor_tatami_w1_co.png")).convert("RGB").resize((400, 200))
    for i, (heri, lab) in enumerate((("jp_m_floor_tatami_heri_w1", "BEFORE black heri (kept: machiya, T3)"),
                                     ("jp_m_floor_tatami_heri_cha_w1", "AFTER cha heri (farmhouse dei / zashiki, T2)"))):
        x0 = 30 + i * 440
        band = Image.open(os.path.join(TEX, heri + "_co.png")).convert("RGB").resize((400, 14))
        out.paste(mat, (x0, 60))
        out.paste(band, (x0, 60))
        out.paste(band, (x0, 246))
        d.text((x0, 30), lab, font=F, fill=(255, 220, 140))
    return out


def sheet_props():
    B3A, B3B, BEF = (os.path.join(DEV, "spikes", "B3a", "renders"), os.path.join(DEV, "spikes", "B3b", "renders"),
                     os.path.join(HERE, "before"))
    pairs = [("grave stones (kaimyo cells, bare-earth mound)", os.path.join(BEF, "jp_s_grave_stones_row.png"),
              os.path.join(B3B, "jp_s_grave_stones_row.png")),
             ("grave wood (bohyo: new wood / silver-grey, ink names, earth mounds)",
              os.path.join(BEF, "jp_s_grave_wood_row.png"), os.path.join(B3B, "jp_s_grave_wood_row.png")),
             ("site firewood stacks (i22 firewood)", os.path.join(BEF, "jp_s_firewood_stack_row.png"),
              os.path.join(B3B, "jp_s_firewood_stack_row.png")),
             ("kori (wicker_aged)", os.path.join(BEF, "jp_f_kori_row.png"), os.path.join(B3A, "jp_f_kori_row.png")),
             ("furniture firewood (i22 firewood)", os.path.join(BEF, "jp_f_firewood_row.png"),
              os.path.join(B3A, "jp_f_firewood_row.png"))]
    w, h = 880, 495
    extra = [("close-ups after", os.path.join(B3B, "m1_bohyo.png"), os.path.join(B3B, "m1_stones.png"))]
    rows = pairs + extra
    sh = Image.new("RGB", (2 * w + 30, len(rows) * (h + 30) + 60 + 320), BG)
    d = ImageDraw.Draw(sh)
    d.text((10, 10), "M1 props: BEFORE (left) / AFTER (right), rendered from the MLOD masters", font=FB,
           fill=(255, 255, 255))
    y = 50
    for title, a, b in rows:
        d.text((10, y), title, font=F, fill=(255, 220, 140))
        sh.paste(fit(Image.open(a), w, h), (10, y + 22))
        sh.paste(fit(Image.open(b), w, h), (20 + w, y + 22))
        y += h + 30
    sh.paste(heri_mock(), (10, y + 10))
    sh.save(os.path.join(OUT, "m1_2_props.jpg"), quality=86)


def atlas_on(mid, bg_tex, crop_h):
    a = Image.open(os.path.join(TEX, mid + "_w0_ca.png")).convert("RGBA")
    bg = Image.open(os.path.join(TEX, bg_tex)).convert("RGB").resize(a.size)
    bg.paste(a, (0, 0), a)
    return bg.crop((0, 0, 1024, crop_h))


def sheet_text():
    side = {}
    for fam, mid in (("stone", "jp_m_decal_carved_text_grave"), ("paint", "jp_m_decal_sumi_text_grave")):
        side[mid] = json.load(open(os.path.join(DEV, "src", "JP", "common", "materials", fam, mid + ".json"),
                                   encoding="utf-8"))["cells"]
    sh = Image.new("RGB", (1024 + 560, 1024 + 340 + 120), BG)
    d = ImageDraw.Draw(sh)
    d.text((10, 10), "M1 text: carved kaimyo for gravestones (13 cells) and ink kaimyo for grave posts (6 cells), Yuji "
           "Syuku, columns right to left: year | name | month-day", font=F, fill=(255, 255, 255))
    sh.paste(atlas_on("jp_m_decal_carved_text_grave", "jp_m_stone_carved_w1_co.png", 1024), (10, 40))
    sh.paste(atlas_on("jp_m_decal_sumi_text_grave", "jp_m_wood_new_w0_co.png", 340), (10, 40 + 1024 + 30))
    y = 40
    for mid in side:
        for name, c in side[mid].items():
            d.text((1050, y), "%s  %s" % (name.replace("kaimyo_", "").replace("bohyo_", "post: "), c["text"]), font=FJ,
                   fill=(220, 220, 220))
            y += 22
        y += 16
    d.text((1050, y + 10), "Bonji (Siddham seed syllables): NOT made -\nno Siddham font on this machine;\nneeds Noto Sans "
           "Siddham (SIL OFL 1.1)", font=F, fill=(255, 150, 150))
    sh.save(os.path.join(OUT, "m1_3_text.jpg"), quality=88)


if __name__ == "__main__":
    sheet_materials()
    sheet_props()
    sheet_text()
    print("sheets written to", OUT)
