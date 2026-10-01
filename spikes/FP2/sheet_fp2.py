"""FP2 before / after sheet: Stephen's re-check props (firewood, usu / kine, rope), renders from spikes/FP2/renders
(back faces culled, as the game draws) and texture swatches from spikes/FP2/look.
  python spikes/FP2/sheet_fp2.py  ->  research/production/contact_sheets/fp2_fixes.jpg
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "research", "production", "contact_sheets", "fp2_fixes.jpg")
R = os.path.join(HERE, "renders")
LK = os.path.join(HERE, "look")
TEX = os.path.join(DEV, "data", "materials", "textures")
W, H, LW = 400, 300, 330


def r(name):
    return os.path.join(R, name + ".png")


# (finding, text, [(before or None, after), ...])
ROWS = [
    ("1 Firewood", "B3b wall stacks were a sooted box with flat yellow 4-sided end decals -> woodpile.py: split "
     "billets (halves, quarters, thirds, rounds), bark sides, end grain from each round's pith, ends staggered",
     [(r("before_f1_wall_h120"), r("after_f1_wall_h120")), (r("before_f1_wall_h120_close"), r("after_f1_wall_h120_close"))]),
    ("1 Firewood", "free-standing stack under its board cap; B3a's kitchen stack (both ends showing, a loose billet "
     "split face up = the loot point). Same origins, wall gap, collision",
     [(r("before_f1_free_posts"), r("after_f1_free_posts")), (r("before_f1_f_stack"), r("after_f1_f_stack"))]),
    ("1 Textures", "end grain: 25 rings 4.5 px apart at 256 px (mip -> flat yellow) -> 512 px, ~11 clear rings, "
     "heartwood, sapwood, bark ring, drying checks; sides: plank photo (nail holes) -> bark band + split band",
     [(os.path.join(LK, "old_textures.png"), os.path.join(LK, "new_textures.png"))]),
    ("2 Usu + mallet", "the yokogine hung over the bowl -> its head lies in the hollow (both end circles on the "
     "bowl), the handle rests on the rim edge; mortar 16-sided, base flat on y 0",
     [(r("before_f2_usu_mallet"), r("after_f2_usu_mallet")), (r("before_f2_usu_mallet_side"),
                                                           r("after_f2_usu_mallet_side"))]),
    ("2 Usu + pounder", "the tategine leaned on nothing -> stands on the floor, leaning 16 deg on the rim's outer "
     "edge (contact solved); the fallen one no longer passes through the mortar",
     [(r("before_f2_usu"), r("after_f2_usu")), (r("before_f2_usu_fallen"), r("after_f2_usu_fallen"))]),
    ("3 Rope coils", "coils 10 x 4 (octagonal, flat) -> 25 x 10 round the coil and the rope, smooth normals "
     "(inner coil 8 x 3 -> 20 x 8); wall-facing faces culled",
     [(r("before_f3_rope_pegs_3"), r("after_f3_rope_pegs_3")), (r("before_f3_rope_pegs_close"),
                                                             r("after_f3_rope_pegs_close"))]),
    ("3 Shimenawa", "twisted straw strands 3 / 4 sides -> 8 / 10, a segment every pitch/4 -> pitch/10 (strand faces "
     "inside the lay culled); all rope torii + shimenawa",
     [(r("before_f3_shimenawa_2ken"), r("after_f3_shimenawa_2ken")), (r("before_f3_torii_rope"),
                                                                   r("after_f3_torii_rope"))]),
    ("3 Ropes, ties", "rope_path / cords: one prism per segment, 3-5 sides -> one smooth tube, 8-13 sides, 2.5x the "
     "segments on bends (wells, laundry, nets, nio, carts); tawara ties: round 8-segment section",
     [(r("before_f3_well_close"), r("after_f3_well_close")), (r("before_f3_tawara"), r("after_f3_tawara"))]),
]


def font(sz):
    for f in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def tile(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w / h > W / H:                                     # centre-crop to 4:3
        nw = int(h * W / H)
        im = im.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    else:
        nh = int(w * H / W)
        im = im.crop((0, (h - nh) // 2, w, (h + nh) // 2))
    return im.resize((W, H), Image.LANCZOS)


def wrap(text, n):
    out, line = [], ""
    for wd in text.split():
        if len(line) + len(wd) + 1 > n:
            out.append(line)
            line = wd
        else:
            line = (line + " " + wd).strip()
    out.append(line)
    return out


def main():
    rows = len(ROWS)
    sheet = Image.new("RGB", (LW + 4 * W + 20, 60 + rows * (H + 12)), (244, 243, 239))
    d = ImageDraw.Draw(sheet)
    d.text((12, 14), "FP2 (2026-10-01): Stephen's re-check props, BEFORE | AFTER pairs (renders from the MLOD masters, "
           "back faces culled as the game draws them)", fill=(20, 20, 20), font=font(26))
    for i, (head, text, pairs) in enumerate(ROWS):
        y0 = 60 + i * (H + 12)
        d.text((10, y0 + 8), head, fill=(10, 10, 10), font=font(24))
        for k, ln in enumerate(wrap(text, 34)):
            d.text((10, y0 + 46 + 22 * k), ln, fill=(40, 40, 40), font=font(17))
        x = LW
        for before, after in pairs:
            for lab, p in (("BEFORE", before), ("AFTER", after)):
                if p is None:
                    continue
                if x + W > sheet.size[0]:
                    break
                sheet.paste(tile(p), (x, y0))
                d.rectangle([x, y0, x + 92, y0 + 24], fill=(255, 255, 255))
                d.text((x + 4, y0 + 2), lab, fill=(180, 20, 20) if lab == "BEFORE" else (20, 120, 20), font=font(18))
                x += W
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT, quality=86)
    print(OUT, sheet.size)


if __name__ == "__main__":
    main()
