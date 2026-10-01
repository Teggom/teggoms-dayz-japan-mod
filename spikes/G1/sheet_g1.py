"""G1 before / after sheet: each view of spikes/G1/renders as a before | after pair (centre crop), labelled.
  python spikes/G1/sheet_g1.py  ->  research/outdoor_kit/contact_sheets/g1_gorinto_fix.jpg
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "research", "outdoor_kit", "contact_sheets", "g1_gorinto_fix.jpg")
VIEWS = ["gorinto_s_side", "gorinto_s_front", "gorinto_stack_side", "gorinto_stack_front", "gorinto_l_side",
         "ab_gorinto_fallen_low", "gorinto_heap_low"]
T, LAB, PER_ROW = 420, 34, 4


def font(sz):
    for f in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    rows = (len(VIEWS) + PER_ROW - 1) // PER_ROW
    sheet = Image.new("RGB", (PER_ROW * (2 * T + 16), rows * (T + LAB) + 50), (245, 245, 242))
    d = ImageDraw.Draw(sheet)
    d.text((12, 10), "G1: gorinto rings seated flat (truncated water sphere, 12 sides; re-stacked roof flat, 5 deg yaw)."
           "  Each pair: BEFORE | AFTER", fill=(20, 20, 20), font=font(24))
    for i, v in enumerate(VIEWS):
        x0 = (i % PER_ROW) * (2 * T + 16)
        y0 = 50 + (i // PER_ROW) * (T + LAB)
        for j, mode in enumerate(("before", "after")):
            im = Image.open(os.path.join(HERE, "renders", "%s_%s.png" % (mode, v))).convert("RGB")
            w, h = im.size
            im = im.crop(((w - h) // 2, 0, (w + h) // 2, h)).resize((T, T), Image.LANCZOS)
            sheet.paste(im, (x0 + j * T, y0 + LAB))
            d.text((x0 + j * T + 6, y0 + 6), "%s  %s" % (mode.upper(), v), fill=(20, 20, 20), font=font(18))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT, quality=88)
    print(OUT, sheet.size)


if __name__ == "__main__":
    main()
