"""FP1 before / after sheet: one row per numbered finding (1-15) + the new material, renders from spikes/FP1/renders
(back faces culled, as the game draws) and texture swatches from spikes/FP1/look.
  python spikes/FP1/sheet_fp1.py  ->  research/production/contact_sheets/fp1_fixes.jpg
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "research", "production", "contact_sheets", "fp1_fixes.jpg")
R = os.path.join(HERE, "renders")
LK = os.path.join(HERE, "look")
TEX = os.path.join(DEV, "data", "materials", "textures")
W, H, LW = 400, 300, 330


def r(name):
    return os.path.join(R, name + ".png")


# (finding, text, [(before or None, after), ...])
ROWS = [
    ("1 Broom", "L2 #55 + S1 shop brooms: flat plank fan -> take-boki (bamboo handle, bound twig bundle, twigs + "
     "branchlets); shop zashiki-boki (sewn sorghum fan)",
     [(r("before_f1_broom_pile"), r("after_f1_broom_pile")), (r("before_f1_aramono"), r("after_f1_aramono"))]),
    ("2 Rice sheaves", "hasa sheaves were wedge slabs swallowing the rail -> split sheaves astride the rail, roped "
     "neck on top, ears down; stooks re-made",
     [(r("before_f2_hasa_low_close"), r("after_f2_hasa_low_close")), (r("before_f2_stook"), r("after_f2_stook"))]),
    ("3 Bonsai + pots", "unglazed earthenware pots, potted pine (S trunk, roots, branches, needle pads), satsuki, kiku "
     "on a stake with flowers (era #58)",
     [(r("before_f3_potted_stand"), r("after_f3_potted_stand")), (r("before_f3_pine_close"), r("after_f3_pine_close"))]),
    ("4 Sword rack", "curved koshirae: lacquer saya, sageo, tsuba + seppa, ito diamonds over samegawa; shaped stand "
     "with curled arms",
     [(r("before_f4_katana_stand_close"), r("after_f4_katana_stand_close")), (r("before_f4_katana_wall"),
                                                                            r("after_f4_katana_wall"))]),
    ("5 Torii rope", "plain prisms -> two twisted straw strands, frayed ends, 3-bundle tassels (all rope torii + "
     "shimenawa); the vermilion torii's snapped rope",
     [(r("before_f5_shu_snapped"), r("after_f5_shu_snapped")), (r("before_f5_rope_myojin"), r("after_f5_rope_myojin"))]),
    ("6 Bale ends", "charcoal bales (sumi-dawara) had an open bottom: lying ones see-through -> both ends closed, "
     "all LODs",
     [(r("look_f6_charcoal_stack_b"), r("after_f6_charcoal_stack_b")), (r("look_f6_charcoal_burst_b"),
                                                                       r("after_f6_charcoal_burst_b"))]),
    ("7 Fallen lantern", "the open paper end showed nothing inside -> inside drawn; the litter decal under it is cut "
     "alpha now (was a soft haze = clear sheet)",
     [(r("before_f7_chochin_c"), r("after_f7_chochin_c")), (r("before_f7_chochin_a"), r("after_f7_chochin_a"))]),
    ("8 Loom float", "breast beam, heddle, reed and seat hung in mid-air -> beam uprights, lever arms + cords, seat "
     "leg (bases were already at y 0)",
     [(r("before_f8_loom_front"), r("after_f8_loom_front")), (r("before_f8_loom"), r("after_f8_loom"))]),
    ("9 Leaf litter", "jp_m_decal_litter: round dots over a soft haze -> maple / ginkgo / oak / cherry leaves, straw, "
     "paper, shards, cut alpha (before: magenta = transparent)",
     [(os.path.join(LK, "litter_w1.jpg"), os.path.join(LK, "t1.png"))]),
    ("10 Stone texture", "1 m tile of round lichen dots repeating -> jp_m_stone_carved_aged (2 m, lichen rosettes) + "
     "per-piece uv turn/shift; lanterns too",
     [(r("before_f10_torii_stone_l"), r("after_f10_torii_stone_l")), (os.path.join(LK, "t4.png"),
                                                                    os.path.join(LK, "t3.png"))]),
    ("11 Two-tone pot", "= the slumped straw stack by the kura: texture top band repeated at the foot -> one pass top "
     "to foot, planar top; all nio",
     [(r("before_f11_slumped"), r("after_f11_slumped")), (r("before_f11_slumped_top"), r("after_f11_slumped_top"))]),
    ("12 Lever well", "stone lashed high under the pole, bucket in the shaft -> stone hangs low in a sling, bucket "
     "clear above the curb",
     [(r("before_f12_lever_well"), r("after_f12_lever_well"))]),
    ("13 Notice board", "boards floated in front of the posts, roof touched nothing -> rails on the post fronts, "
     "ridge beam on struts, rafters, braces",
     [(r("before_f13_kosatsu_side"), r("after_f13_kosatsu_side")), (r("before_f13_kosatsu_std"),
                                                                   r("after_f13_kosatsu_std"))]),
    ("14 Fire-watch ladder", "Land_JP_S_Fire_Watch_Ladder_Tower: ladder1 memory points + View component, class=house, "
     "laddertype=wood; railed lookout deck to step off",
     [(r("before_f14_ladder_tower"), r("after_f14_ladder_tower"))]),
    ("15 Collapsed torii", "new: shinmei rot, myojin typhoon, vermilion snapped, stone quake, stone quake (old)",
     [(None, r("after_f15_shinmei_rot")), (None, r("after_f15_myojin_typhoon")), (None, r("after_f15_shu_snapped")),
      (None, r("after_f15_stone_quake"))]),
    ("M Aged shikkui", "jp_m_wall_shikkui_aged for FB1's kura: shikkui_white (left) vs aged _w1 (sampled c25 + c03, "
     "162,163,159)",
     [(os.path.join(TEX, "jp_m_wall_shikkui_w1_co.png"), os.path.join(TEX, "jp_m_wall_shikkui_aged_w1_co.png"))]),
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
    d.text((12, 14), "FP1 (2026-10-01): Stephen's showcase-walk props, BEFORE | AFTER pairs (renders cull back faces "
           "as the game draws them; 15: new models)", fill=(20, 20, 20), font=font(26))
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
