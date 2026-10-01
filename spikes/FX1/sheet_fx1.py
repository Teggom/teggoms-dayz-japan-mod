"""FX1 before / after sheet: research/production/contact_sheets/fx1_fixes.jpg from spikes/FX1/renders/before_<shot>.png
(rendered from a git-archive HEAD copy, pre-FX1) and after_<shot>.png (working tree), captions from fx1_jobs.py.
  python spikes/FX1/sheet_fx1.py"""
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fx1_jobs  # noqa: E402

REN = os.path.join(HERE, "renders")
DST = os.path.join(DEV, "research", "production", "contact_sheets", "fx1_fixes.jpg")


def main():
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 30),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 16),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 18)}.items()}
    cw, ch, cap = 560, 350, 44
    pairs = 2                                           # two before/after pairs per row
    jobs = fx1_jobs.JOBS
    rows = (len(jobs) + pairs - 1) // pairs
    W = pairs * (2 * cw + 8) + (pairs + 1) * 16
    H = 96 + rows * (ch + cap + 30)
    im = Image.new("RGB", (W, H), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((16, 10), "FX1: wave-2 fixes from Stephen's walk (2026-10-01) - BEFORE (left, HEAD) / AFTER (right)",
           font=F["h1"], fill=(20, 20, 20))
    d.text((16, 52), "1 door pulls on their own leaf  2 offering box beside the stair, no litter  3 hung things on real "
           "members  4 en ends  5 rope torii head room (1.80 m figure)  6 woodpile end stakes", font=F["s"],
           fill=(60, 60, 60))
    for i, (out, caption, _) in enumerate(jobs):
        x = 16 + (i % pairs) * (2 * cw + 8 + 16)
        y = 96 + (i // pairs) * (ch + cap + 30)
        d.text((x, y), out, font=F["b"], fill=(30, 30, 30))
        y += 24
        for k, tag in enumerate(("before", "after")):
            p = os.path.join(REN, "%s_%s.png" % (tag, out))
            xx = x + k * (cw + 8)
            if os.path.isfile(p):
                im.paste(Image.open(p).convert("RGB").resize((cw, ch)), (xx, y))
            d.rectangle([xx, y, xx + 70, y + 22], fill=(160, 30, 30) if k == 0 else (30, 120, 40))
            d.text((xx + 6, y + 2), tag.upper(), font=F["s"], fill=(255, 255, 255))
        d.rectangle([x, y + ch, x + 2 * cw + 8, y + ch + cap], fill=(250, 249, 246))
        yy = y + ch + 3
        for ln in textwrap.wrap(caption, 125)[:2]:
            d.text((x + 5, yy), ln, font=F["s"], fill=(40, 40, 40))
            yy += 19
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    im.save(DST, quality=85)
    print("sheet", DST, im.size)


if __name__ == "__main__":
    main()
