"""M2 contact sheets -> research/materials/contact_sheets/m2_1_bonji_cells.jpg, m2_2_bonji_stones.jpg

1 cells: the 9 rendered masks (Chromium-shaped Noto Sans Siddham) and the atlas corner on stone at _w0 / _w1 / _w2,
  with the syllable, its ring / face and its composition.
2 stones: BEFORE (left) / AFTER (right) close-ups of the gorinto (small, large + its rings, re-stacked, fallen) and
  the hokyointo (front = HUM, left = TRAH, back = HRIH; broken), from the MLOD masters (spikes/M2/render_m2.py).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import look_atlas  # noqa: E402

TEX = os.path.join(DEV, "data", "materials", "textures")
MASKS = os.path.join(DEV, "research", "materials", "bonji_masks")
REN = os.path.join(HERE, "renders")
OUT = os.path.join(DEV, "research", "materials", "contact_sheets")
try:
    F = ImageFont.truetype("arial.ttf", 16)
    FB = ImageFont.truetype("arialbd.ttf", 21)
except OSError:
    F = FB = ImageFont.load_default()
BG = (34, 34, 34)
CELLS = [("bonji_kha", "KHA (kya)", "gorinto sky / jewel (kurin)", "U+1158F"),
         ("bonji_ha", "HA", "gorinto wind / crescent (furin)", "U+115AE"),
         ("bonji_ra", "RA", "gorinto fire / roof (karin)", "U+115A8"),
         ("bonji_va", "VA (ba)", "gorinto water / sphere (suirin)", "U+115AA"),
         ("bonji_a", "A", "gorinto earth / cube (chirin)", "U+11580"),
         ("bonji_hum", "HUM (un)", "hokyointo east = front: Akshobhya", "HA+UU+anusvara"),
         ("bonji_trah", "TRAH (taraku)", "hokyointo south = +x: Ratnasambhava", "TA+virama+RA+AA+visarga"),
         ("bonji_hrih", "HRIH (kiriku)", "hokyointo west = back: Amitabha", "HA+virama+RA+II+visarga"),
         ("bonji_ah", "AH (aku)", "hokyointo north = -x: Amoghasiddhi", "A+visarga")]


def fit(im, w, h):
    im = im.convert("RGB")
    sc = min(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    out = Image.new("RGB", (w, h), BG)
    out.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return out


def sheet_cells():
    T = 210
    tiles = [look_atlas.corner(TEX, lv) for lv in range(3)]
    W = 5 * (T + 120) + 20
    H = 60 + 2 * (T + 80) + 3 * (tiles[0].height + 30) + 20
    sh = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sh)
    d.text((10, 12), "M2 bonji cells (jp_m_decal_carved_text_grave, x 340-1020 / y 680-952): Noto Sans Siddham (SIL OFL "
           "1.1) shaped by Chromium; masks, then the atlas corner on stone _w0 / _w1 / _w2", font=FB,
           fill=(255, 255, 255))
    for i, (n, syl, use, comp) in enumerate(CELLS):
        x, y = 10 + (i % 5) * (T + 120), 50 + (i // 5) * (T + 80)
        sh.paste(fit(Image.open(os.path.join(MASKS, n + ".png")), T, T), (x, y))
        d.text((x, y + T + 4), "%s  %s" % (n, syl), font=F, fill=(255, 220, 140))
        d.text((x, y + T + 24), use, font=F, fill=(210, 210, 210))
        d.text((x, y + T + 44), comp, font=F, fill=(160, 160, 160))
    y = 50 + 2 * (T + 80)
    for lv, t in enumerate(tiles):
        d.text((10, y), "_w%d" % lv, font=F, fill=(140, 255, 140))
        sh.paste(t, (60, y))
        y += t.height + 30
    sh.save(os.path.join(OUT, "m2_1_bonji_cells.jpg"), quality=88)


def sheet_stones():
    rows = [("gorinto_s_front", "gorinto 0.6 m: kha / ha / ra / va / a, top to bottom"),
            ("gorinto_l_front", "gorinto 2.0 m on its platform"),
            ("gorinto_l_rings", "gorinto 2.0 m, the rings close"),
            ("gorinto_stack_front", "re-stacked: roof + jewel from a bigger stupa (ra, kha), crescent missing"),
            ("ab_gorinto_fallen_front", "fallen (quake): cube + sphere stand (a, va); the toppled rings keep theirs"),
            ("hokyointo_front", "hokyointo front (east): HUM"),
            ("hokyointo_left", "hokyointo from its left (+x, south): TRAH"),
            ("hokyointo_back", "hokyointo back (west): HRIH"),
            ("ab_hokyointo_broken_front", "hokyointo, finial fallen: body still carries its four")]
    w, h = 720, 405
    sh = Image.new("RGB", (2 * w + 30, 50 + len(rows) * (h + 30)), BG)
    d = ImageDraw.Draw(sh)
    d.text((10, 12), "M2 seed syllables on the graves: BEFORE (left, M1 state) / AFTER (right), MLOD masters, "
           "Resolution 1", font=FB, fill=(255, 255, 255))
    y = 50
    for key, title in rows:
        d.text((10, y), title, font=F, fill=(255, 220, 140))
        for k, mode in enumerate(("before", "after")):
            im = Image.open(os.path.join(REN, "%s_%s.png" % (mode, key)))
            # crop the middle of the 16:9 frame (the stone), then fit
            cw = im.width * 0.55
            im = im.crop((int((im.width - cw) / 2), 0, int((im.width + cw) / 2), im.height))
            sh.paste(fit(im, w, h), (10 + k * (w + 10), y + 22))
        y += h + 30
    sh.save(os.path.join(OUT, "m2_2_bonji_stones.jpg"), quality=86)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sheet_cells()
    sheet_stones()
    print("sheets written to", OUT)
