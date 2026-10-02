"""FX4 sheet: research/production/contact_sheets/fx4_fixes.jpg (before | after, back faces culled as the game draws).

  python spikes/FX4/render_fx4.py before ; python spikes/FX4/render_fx4.py after ; python spikes/FX4/sheet_fx4.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "research", "production", "contact_sheets", "fx4_fixes.jpg")
ROWS = [
    ("bell_below", "1 Temple bell (bonsho, town) from below: was inside out (every face turned inward, a flat disc for "
                   "a mouth) -> hollow casting: inner wall faces the cavity, lip with a flat underside"),
    ("gong", "1 Waniguchi gong (same fault: profile traversed the wrong way) -> outward; also fixed: the hansho alarm "
             "bell, a tassel collar, two bowl lids, the sedge hat (lathecheck: 0 inside out)"),
    ("tower_deck", "2 Fire-watch ladder deck (4.90 m) with a 1.80 m stand-in: roof was 1.10 m over the deck -> 2.20 m "
                   "on four posts; the bell moved outside the back rail"),
    ("torii_posts", "3 Stone torii 3.6 posts: one 2 m tile mapped world-planar -> 2x2 stone atlas, every face its own "
                    "turn + offset (uvwood stone mode)"),
]
W, H = 760, 570


def font(sz):
    for f in ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"):
        if os.path.isfile(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def main():
    f1, f2 = font(22), font(28)
    cap = 64
    sheet = Image.new("RGB", (2 * W + 30, 60 + len(ROWS) * (H + cap + 10)), (245, 244, 240))
    d = ImageDraw.Draw(sheet)
    d.text((10, 14), "FX4 fixes (2026-10-01): before | after", fill=(20, 20, 20), font=f2)
    y = 60
    for name, text in ROWS:
        d.text((10, y + 4), text[:118], fill=(30, 30, 30), font=f1)
        if len(text) > 118:
            d.text((10, y + 30), text[118:], fill=(30, 30, 30), font=f1)
        for k, mode in enumerate(("before", "after")):
            p = os.path.join(HERE, "renders", "%s_%s.png" % (mode, name))
            im = Image.open(p).convert("RGB").resize((W, H))
            sheet.paste(im, (10 + k * (W + 10), y + cap))
            d.text((20 + k * (W + 10), y + cap + 8), mode, fill=(200, 30, 30), font=f2)
        y += H + cap + 10
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT, quality=82)
    print("sheet", OUT, sheet.size)


if __name__ == "__main__":
    main()
