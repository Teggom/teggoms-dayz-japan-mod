#!/usr/bin/env python3
r"""make_s1_materials.py - the materials S1 (the KEEP_TRADES shop sets, research/interior/SHOP_SETS.md) ADDS to
jp_common through B1's pipeline.

  python make_s1_materials.py [--no-pack] [--only ID[,ID...]]

Adds only; never changes an existing material or palette entry (the route of make_l1_materials.py / make_l2_materials.py:
B1's make_one = textures, PAAs, rvmats, sidecar, C1 matcheck on the PNG and the shipped PAA), then repacks jp_common.pbo.

- jp_m_decal_sumi_text_shop  A third ink atlas (B1's decal_sumi_text recipe and fonts: Yuji Syuku kanji, Yuji Hentaigana
                             Akebono kana, SIL OFL): the shop kanban of the 28 trades, menu strips, pawn tags, medicine
                             labels and packets, book title slips, and three ink pictures (an Otsu-e, a fan landscape, a
                             printed page). B1's and L1's atlases are untouched.
- jp_m_lacquer_shu           Red (shu) lacquer of bowls, trays, kneading bowls, doll stands. New palette `lacquer_shu`
                             (assumed: a dull brick vermilion, darker than the shrine paint `shu_vermilion`). Glazed
                             finish, as jp_m_lacquer_black.
- jp_m_ceramic_porcelain     Blue-and-white porcelain (sometsuke): white glaze, cobalt brush bands and scrolls (the blue
                             is masked out of the palette mean). New palette `porcelain_sometsuke` (assumed). Glazed.
- jp_m_leather_tan           Tanned leather (pouches, setta soles, rolled hides). Palette `cha_koge` (existing).
- jp_m_food_tofu             Tofu and rice cakes: smooth off-white with faint pores. Palette `gofun_white` (existing).
C1 results: src/JP/common/materials/checks_s1.json. Never starts or stops the server or any GUI program.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

PAL = os.path.join(DEV, "playbook", "palette.json")
f32 = np.float32
ENTRIES = [
    {"id": "lacquer_shu", "name": "Red (shu) lacquer on wares, aged", "material": "lacquer with cinnabar / bengara red",
     "group": "paint", "tiers": [2, 3], "use": "bowls, trays, kneading bowls, doll stands (jp_m_lacquer_shu)",
     "note": "Added 2026-09-30 by S1. Assumed: the dull brick vermilion of used shu lacquer (negoro wares wear through "
             "to black), darker and browner than the shrine paint shu_vermilion. Judge in game.",
     "srgb": [126, 42, 28], "method": "assumed", "tolerance_dE76": 12},
    {"id": "porcelain_sometsuke", "name": "Porcelain glaze, white with a grey-blue cast (sometsuke ground)",
     "material": "Hizen (Arita / Hasami) porcelain", "group": "ceramic", "tiers": [2, 3],
     "use": "the white ground of blue-and-white wares (jp_m_ceramic_porcelain); the cobalt pattern is masked",
     "note": "Added 2026-09-30 by S1. Assumed: the faintly blue-grey white of period Hizen glaze. Judge in game.",
     "srgb": [200, 203, 200], "method": "assumed", "tolerance_dE76": 12},
]


def add_palette():
    pal = json.load(open(PAL, encoding="utf-8"))
    have = {e.get("id") for e in pal["entries"]}
    added = []
    for ent in ENTRIES:
        if ent["id"] in have:
            continue
        e = dict(ent)
        e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
        pal["entries"].append(e)
        added.append(ent["id"])
    if added:
        with open(PAL, "wb") as f:
            f.write(json.dumps(pal, indent=1).encode("utf-8"))
    return added


# ================================================================================================ the shop atlas
# 1024 px = 1 m. Grid A: kanban cells 96 x 200 px (8 a row, 4 rows: y 0-800, x 0-768). Grid B (y 800-1024): small
# text (tags, packets, labels, title slips). Grid C (x 768-1024): the ink pictures.
KANBAN = [
    ("aramono", "荒物"), ("futomono", "太物"), ("furugi", "古着"), ("kanamono", "金物"), ("setomono", "瀬戸物"),
    ("nurimono", "塗物"), ("hitsuboku", "筆墨"), ("abura", "油"),
    ("rousoku", "蝋燭"), ("sumimaki", "炭薪"), ("tabidogu", "旅道具"), ("otsue", "大津絵"), ("kome", "米"),
    ("sakana", "魚"), ("aomono", "青物"), ("tofu", "豆腐"),
    ("mochi", "名物餅"), ("niuri", "煮売"), ("shichi", "質"), ("ryogae", "両替"), ("shorin", "書林"),
    ("fukuromono", "袋物"), ("momen", "木綿"), ("shitate", "仕立物"),
    ("edokoro", "絵所"), ("nushi", "塗師"), ("kushi", "櫛"), ("ningyo", "人形"), ("butsugu", "仏具"),
    ("menu_nishime", "煮しめ"), ("menu_nimame", "煮豆"), ("menu_dengaku", "田楽"),
]
SMALL = [   # (name, rect px, columns [(text, size, indent)], for)
    ("tag_ichi", (0, 810, 48, 1010), [("質札壱番", 30, 0)], "jp_f_pawn_board: pawn ticket no. 1"),
    ("tag_ni", (48, 810, 96, 1010), [("質札弐番", 30, 0)], "jp_f_pawn_board: pawn ticket no. 2"),
    ("tag_san", (96, 810, 144, 1010), [("質札参番", 30, 0)], "jp_f_pawn_board: pawn ticket no. 3"),
    ("pkt_hangontan", (144, 810, 216, 1010), [("反魂丹", 50, 0)], "jp_f_sg medicine: Toyama Hangontan packet"),
    ("pkt_mankintan", (216, 810, 288, 1010), [("万金丹", 50, 0)], "jp_f_sg medicine: Ise Mankintan packet"),
    ("title_tsurezure", (288, 810, 328, 1010), [("徒然草", 34, 0)], "jp_f_sg books: title slip (Tsurezuregusa)"),
    ("title_hyakunin", (328, 810, 368, 1010), [("百人一首", 30, 0)], "jp_f_sg books: title slip (Hyakunin isshu)"),
    ("pkt_kizami", (368, 810, 432, 1010), [("きざみ", 44, 0)], "jp_f_sg tobacco: cut-tobacco packet"),
]
LABELS = ["甘草", "桂枝", "芍薬", "大黄", "人参", "当帰", "山薬", "黄連", "附子", "麻黄", "杏仁", "半夏", "陳皮", "生姜",
          "茯苓", "白朮"]                                         # 4 x 4 drawer labels, 64 x 48 px each
LABEL_RECT = (448, 816, 704, 1008)
PICTURES = [
    ("pic_otsue", (768, 0, 1024, 340), "jp_f_print_line _otsue: an Otsu-e (the demon as a mendicant monk), ink only"),
    ("pic_fan", (768, 350, 1024, 520), "jp_f_print_line _fans: a fan leaf with an ink landscape"),
    ("pic_page", (768, 530, 1024, 870), "jp_f_print_line _books: a printed page (sumizuri-e), text columns and a picture"),
    ("pic_scroll", (768, 880, 1024, 1024), "jp_f_print_line _fans: a small ink landscape (scroll / album leaf)"),
]


def _mount(d, sc, cx, base, r=1.0):
    """Three ink mountains with brush texture lines, the base line at y = base (atlas px)."""
    for k, (dx, h, w) in enumerate(((-40, 80, 70), (10, 110, 85), (55, 60, 55))):
        x = cx + dx * r
        pts = [((x - w * r) * sc, base * sc), (x * sc, (base - h * r) * sc), ((x + w * r) * sc, base * sc)]
        d.line(pts, fill=255, width=int(6 * sc))
        for q in range(3):
            yy = base - h * r * (0.3 + 0.2 * q)
            d.line([((x - w * r * (0.55 - 0.15 * q)) * sc, yy * sc), ((x - w * r * (0.25 - 0.1 * q)) * sc,
                                                                      (yy + 10 * r) * sc)], fill=255, width=int(3 * sc))


def shop_layout(S, sc=2):
    im = Image.new("L", (S * sc, S * sc), 0)
    d = ImageDraw.Draw(im)
    uv = {}

    def cell(name, x0, y0, x1, y1, use, text=None):
        uv[name] = {"uv": [round(x0 / S, 4), round(y0 / S, 4), round(x1 / S, 4), round(y1 / S, 4)], "for": use}
        if text:
            uv[name]["text"] = text

    def column(x0, y0, x1, y1, cols):
        pitch = [1.3 * s for _, s, _ in cols]
        x = x1 - (x1 - x0 - sum(pitch)) / 2
        for (t, s, ind), p in zip(cols, pitch):
            xc = x - p / 2
            n = sum(0.5 if c == " " else 1.06 for c in t) + ind
            top = y0 + max(6, ((y1 - y0) - n * s) / 2)
            B._col(d, xc * sc, (top + ind * s) * sc, t, s, sc)
            x -= p

    for i, (name, text) in enumerate(KANBAN):
        r, c = divmod(i, 8)
        x0, y0 = c * 96, r * 200
        n = len(text)
        size = {1: 86, 2: 76, 3: 56, 4: 44}[n]
        cols = [(text, size, 0)]
        column(x0, y0, x0 + 96, y0 + 200, cols)
        cell("kanban_" + name if not name.startswith("menu") else name, x0, y0, x0 + 96, y0 + 200,
             "shop kanban / menu strip (S1)", text)
    for name, (x0, y0, x1, y1), cols, use in SMALL:
        column(x0, y0, x1, y1, cols)
        cell(name, x0, y0, x1, y1, use, " / ".join(c[0] for c in cols))
    lx0, ly0, lx1, ly1 = LABEL_RECT
    for k, t in enumerate(LABELS):
        r, c = divmod(k, 4)
        x0, y0 = lx0 + c * 64, ly0 + r * 48
        d.rectangle([(x0 + 3) * sc, (y0 + 3) * sc, (x0 + 61) * sc, (y0 + 45) * sc], outline=255, width=2 * sc)
        B._col(d, (x0 + 32) * sc, (y0 + 5) * sc, t, 18, sc)
    cell("drawer_labels", lx0, ly0, lx1, ly1, "jp_f_yakudansu: 4 x 4 drawer labels (crop one 1/4 x 1/4 per drawer)",
         " ".join(LABELS))
    for name, (x0, y0, x1, y1), use in PICTURES:
        cell(name, x0, y0, x1, y1, use)
        if name == "pic_otsue":                 # the demon as a mendicant monk: head, horns, robe, gong, stick
            cx = (x0 + x1) / 2
            d.rectangle([(x0 + 6) * sc, (y0 + 6) * sc, (x1 - 6) * sc, (y1 - 6) * sc], outline=255, width=3 * sc)
            hy = y0 + 95                         # head centre
            d.ellipse([(cx - 32) * sc, (hy - 32) * sc, (cx + 32) * sc, (hy + 30) * sc], outline=255, width=7 * sc)
            for s_ in (-1, 1):
                d.polygon([((cx + s_ * 14) * sc, (hy - 28) * sc), ((cx + s_ * 26) * sc, (hy - 62) * sc),
                           ((cx + s_ * 28) * sc, (hy - 24) * sc)], fill=255)                     # horns
                d.line([((cx + s_ * 6) * sc, (hy - 14) * sc), ((cx + s_ * 24) * sc, (hy - 6) * sc)], fill=255,
                       width=5 * sc)                                                             # scowling brows
                d.ellipse([(cx + s_ * 14 - 6) * sc, (hy - 6) * sc, (cx + s_ * 14 + 6) * sc, (hy + 4) * sc],
                          outline=255, width=3 * sc)                                             # glaring eyes
                d.polygon([((cx + s_ * 8) * sc, (hy + 12) * sc), ((cx + s_ * 11) * sc, (hy + 22) * sc),
                           ((cx + s_ * 14) * sc, (hy + 12) * sc)], fill=255)                     # fangs
            d.line([((cx - 16) * sc, (hy + 12) * sc), ((cx + 16) * sc, (hy + 12) * sc)], fill=255, width=4 * sc)
            # the monk's robe: a wide body with hanging sleeves, a collar V, the hem
            d.polygon([((cx - 36) * sc, (hy + 34) * sc), ((cx + 36) * sc, (hy + 34) * sc), ((cx + 62) * sc, (y1 - 28) * sc),
                       ((cx - 62) * sc, (y1 - 28) * sc)], outline=255, width=6 * sc)
            d.line([((cx - 20) * sc, (hy + 34) * sc), (cx * sc, (hy + 80) * sc), ((cx + 20) * sc, (hy + 34) * sc)],
                   fill=255, width=4 * sc)
            for s_ in (-1, 1):
                d.polygon([((cx + s_ * 36) * sc, (hy + 38) * sc), ((cx + s_ * 92) * sc, (hy + 70) * sc),
                           ((cx + s_ * 84) * sc, (hy + 130) * sc), ((cx + s_ * 44) * sc, (hy + 110) * sc)],
                          outline=255, width=5 * sc)
            d.ellipse([(cx - 24) * sc, (hy + 92) * sc, (cx + 24) * sc, (hy + 140) * sc], outline=255, width=6 * sc)
            d.line([((cx - 20) * sc, (hy + 40) * sc), ((cx - 14) * sc, (hy + 92) * sc)], fill=255, width=2 * sc)
            d.line([((cx + 20) * sc, (hy + 40) * sc), ((cx + 14) * sc, (hy + 92) * sc)], fill=255, width=2 * sc)
            d.line([((cx + 60) * sc, (hy + 96) * sc), ((cx + 100) * sc, (hy + 60) * sc)], fill=255, width=6 * sc)
            B._col(d, (x0 + 30) * sc, (y0 + 20) * sc, "鬼の念仏", 28, sc)
            uv[name]["text"] = "鬼の念仏 (Oni no nenbutsu) + the figure"
        elif name == "pic_fan":                 # fan leaf outline (two arcs and the side ribs) + a landscape
            cx, cy = (x0 + x1) / 2, y1 + 60
            d.arc([(cx - 125) * sc, (cy - 225) * sc, (cx + 125) * sc, (cy + 225) * sc], 222, 318, fill=255,
                  width=5 * sc)
            d.arc([(cx - 70) * sc, (cy - 120) * sc, (cx + 70) * sc, (cy + 120) * sc], 222, 318, fill=255,
                  width=4 * sc)
            _mount(d, sc, cx, y0 + 140, 0.7)
            d.ellipse([(cx + 40) * sc, (y0 + 40) * sc, (cx + 64) * sc, (y0 + 64) * sc], outline=255, width=4 * sc)
        elif name == "pic_page":                # a printed page: a frame, a picture box, text columns
            d.rectangle([(x0 + 8) * sc, (y0 + 8) * sc, (x1 - 8) * sc, (y1 - 8) * sc], outline=255, width=4 * sc)
            d.rectangle([(x0 + 20) * sc, (y0 + 20) * sc, (x1 - 20) * sc, (y0 + 170) * sc], outline=255, width=3 * sc)
            _mount(d, sc, (x0 + x1) / 2, y0 + 160, 0.8)
            d.polygon([((x0 + 70) * sc, (y0 + 160) * sc), ((x0 + 90) * sc, (y0 + 135) * sc),
                       ((x0 + 110) * sc, (y0 + 160) * sc)], outline=255, width=3 * sc)
            txt = ["春の夜の夢のうき橋", "とだえして峰に別るる", "横雲の空"]
            for k, t in enumerate(txt):
                B._col(d, (x1 - 40 - 50 * k) * sc, (y0 + 182) * sc, t[:7], 20, sc)
            uv[name]["text"] = "/".join(txt)
        else:                                   # pic_scroll: a small landscape, boat
            _mount(d, sc, (x0 + x1) / 2, y0 + 110, 0.6)
            d.line([((x0 + 40) * sc, (y0 + 125) * sc), ((x0 + 90) * sc, (y0 + 125) * sc)], fill=255, width=4 * sc)
            d.line([((x0 + 150) * sc, (y0 + 130) * sc), ((x0 + 220) * sc, (y0 + 130) * sc)], fill=255, width=3 * sc)
    a = B._arr(im.resize((S, S), Image.LANCZOS).convert("RGB"))[..., 0]
    return a, uv


def decal_sumi_text_shop(lv, S):
    """B1's decal_sumi_text recipe on the shop atlas (same ink colours, kasure streaks, fading and flaking)."""
    m, _ = B.atlas("shop", S)
    T, MT = B.T, B.MT
    t = [T("sumi_black", -2), T("sumi_black", 7, 2, 5), T("sumi_black", 8, 2, 5)][lv]
    co = B.base(t, 1 + 0.05 * MT.fbm(S, 2.4, 1, 1, 7101))
    kasure = np.clip(MT.fbm(S, 1.4, 1, 6, 7102) - 0.8, 0, 1)
    a = m * (1 - 0.35 * kasure)
    if lv == 1:
        a = a * np.clip(0.72 + 0.12 * MT.fbm(S, 2.4, 1, 1, 7103), 0.45, 0.9)
    if lv == 2:
        flake = MT.fbm(S, 2.0, 1, 1, 7104) > 0.5
        a = a * 0.42 * np.where(flake, 0.3, 1.0)
    return B.R(co, MT.flat_n(S), 0.9, B.Z(S), t, 0.05, 0.1, alpha=np.clip(a, 0, 1))


# ================================================================================================ the four surfaces
def lacquer_shu(lv, S):
    """B1's lacquer_black recipe in shu: brush marks along u; rubbed through to the black undercoat at the edges (the
    negoro look) at _w1; flaking to the wood and dust at _w2."""
    T, MT = B.T, B.MT
    t = [T("lacquer_shu", 2, 2, 2), T("lacquer_shu", 0), T("lacquer_shu", -2, -2, -2)][lv]
    brush = MT.fbm(S, 2.0, 10, 1, 7201)
    co = B.base(t, 1 + 0.05 * brush + 0.04 * MT.fbm(S, 2.6, 1, 1, 7202))
    h = brush * 0.3
    mask = B.Z(S)
    if lv >= 1:
        e = MT.blur(MT.spots(S, [0, 10, 16][lv], 5, 2, 7, 10, 7203), 2.0)
        co = MT.mix(co, (40, 34, 32), np.clip(e * 1.2, 0, 1) * 0.6)
        mask |= e > 0.3
    if lv == 2:
        fl = B.blobs(S, 7204, 1.4, 3.0, 1.5)
        wood = B.base((92, 70, 52), 1 + 0.1 * MT.fbm(S, 1.5, 1, 20, 7205))
        co[fl] = wood[fl]
        co = MT.mix(co, (100, 96, 90), np.full((S, S), 0.15, f32))
        h = h - fl * 1.0
        mask |= fl
    return B.R(np.clip(co, 0, 1), MT.h2n(h, 1.0), [0.08, 0.25, 0.5][lv], mask, t, [0.8, 0.6, 0.35][lv],
               [0.85, 0.6, 0.35][lv])


def ceramic_porcelain(lv, S):
    """White glaze (faint pooling), cobalt-blue brushwork: two bands along u (rim and foot of a bowl mapped u round
    the pot) and a scroll pattern between them; the blue is masked out of the palette mean."""
    T, MT = B.T, B.MT
    t = [T("porcelain_sometsuke", 2), T("porcelain_sometsuke", -2, 0, 1), T("porcelain_sometsuke", -6, 0, 3)][lv]
    yy, xx = B.grid(S)
    co = B.base(t, 1 + 0.02 * MT.fbm(S, 2.4, 1, 1, 7301))
    v = yy / S
    band = ((np.abs(v - 0.08) < 0.018) | (np.abs(v - 0.12) < 0.006) | (np.abs(v - 0.90) < 0.02)).astype(f32)
    scroll = np.abs(0.5 + 0.18 * np.sin(2 * math.pi * xx / S * 6) - v) < 0.012
    leaves = MT.spots(S, 24, 4, 3, 7, 6, 7302) * ((v > 0.25) & (v < 0.75))
    blue = np.clip(band + scroll.astype(f32) + leaves, 0, 1) * np.clip(0.75 + 0.25 * MT.fbm(S, 2.0, 1, 1, 7303), 0, 1)
    co = MT.mix(co, (52, 70, 120), blue * 0.85)
    mask = blue > 0.2
    h = 0.05 * MT.fbm(S, 2.2, 1, 1, 7304)
    if lv >= 1:                                                   # dust in the foot ring, a few chips
        ch = MT.spots(S, [0, 6, 14][lv], 3, 1.5, 4, 8, 7305)
        co = MT.mix(co, (150, 132, 108), ch * 0.8)
        mask |= ch > 0.3
    if lv == 2:
        cr = MT.blur(B.scratches(S, 60, 7306, 20, 120, width=1), 0.5)
        co = MT.mix(co, (120, 110, 96), cr * 0.6)
        mask |= cr > 0.3
    return B.R(np.clip(co, 0, 1), MT.h2n(h, 1.0), [0.06, 0.12, 0.3][lv], mask, t, [0.85, 0.7, 0.5][lv],
               [0.9, 0.75, 0.5][lv])


def leather_tan(lv, S):
    """Vegetable-tanned leather: fine pebbled grain, darker creases, rubbed lighter at the edges with wear."""
    T, MT = B.T, B.MT
    t = [T("cha_koge", 2, 1, 2), T("cha_koge", 0), T("cha_koge", -3, -1, -3)][lv]
    grain = MT.fbm(S, 1.2, 1, 1, 7401)
    crease = np.clip(-MT.fbm(S, 1.6, 3, 1, 7402) - 0.9, 0, 1)
    co = B.base(t, 1 + 0.06 * grain - 0.25 * crease)
    mask = B.Z(S)
    if lv >= 1:
        rub = np.clip(MT.fbm(S, 2.6, 1, 1, 7403) - 0.7, 0, 1)
        co = MT.mix(co, (150, 118, 84), rub * 0.5)
        mask |= rub > 0.2
    if lv == 2:                                                   # mould bloom
        mo = MT.spots(S, 18, 6, 2, 6, 14, 7404)
        co = MT.mix(co, (140, 140, 120), mo * 0.6)
        mask |= mo > 0.3
    return B.R(np.clip(co, 0, 1), MT.h2n(grain * 0.8 - crease * 1.5, 1.0), 0.7, mask, t, 0.12, 0.25)


def food_tofu(lv, S):
    """Tofu / rice-cake surface: smooth off-white with faint pores and the cloth-press marks; _w1 dried and yellowed,
    _w2 mouldy (an abandoned shop's leftovers)."""
    T, MT = B.T, B.MT
    t = [T("gofun_white", 2), T("gofun_white", -3, 0, 4), T("gofun_white", -8, 1, 6)][lv]
    pores = MT.spots(S, 400, 1, 0.5, 1.2, 4, 7501)
    weave = 0.02 * (MT.fbm(S, 1.2, 40, 1, 7502) + MT.fbm(S, 1.2, 1, 40, 7503))
    co = B.base(t, 1 + weave - 0.12 * pores)
    mask = B.Z(S)
    if lv == 2:
        mo = MT.spots(S, 30, 8, 2, 6, 14, 7504)
        co = MT.mix(co, (110, 120, 96), mo * 0.7)
        mask |= mo > 0.3
    return B.R(np.clip(co, 0, 1), MT.h2n(weave * 10 - pores, 1.0), 0.8, mask, t, 0.1, 0.2)


def table():
    ATL = ("TEXT ATLAS, not world-scale (as jp_m_decal_sumi_text): map a face onto one cell's rectangle (\"cells\": "
           "u0, v0, u1, v1 with v down), keeping the cell's aspect; 1024 px = 1 m. Lay the decal 2-3 mm off the "
           "surface; never in Geometry/View/Fire. Text runs top to bottom, columns right to left.")
    return [
        (B.M("jp_m_decal_sumi_text_shop", "paint", "sumi_black", 1.0, 1024, decal_sumi_text_shop, (0.05, 10), None,
             None, "brush strokes (Yuji Syuku kanji, Yuji Hentaigana Akebono kana)", alpha="decal", uv=ATL,
             atlas_kind="shop", note="The shop sets' ink: kanban of the 28 trades, menu strips, pawn tags, medicine "
                                     "labels and packets, book title slips, an Otsu-e, a fan and a page (ink only: "
                                     "colour prints are later than 1744). Fonts: SIL OFL 1.1, Yuji Project Authors."),
         {"_w0": "crisp black ink", "_w1": "faded to grey-brown", "_w2": "ghost of text, flaking"},
         ["jp_f_kanban", "jp_f_pawn_board", "jp_f_menu_board", "jp_f_yakudansu", "jp_f_print_line", "jp_f_sg"],
         "Ink text and pictures for the shop sets"),
        (B.M("jp_m_lacquer_shu", "paint", "lacquer_shu", 0.5, 256, lacquer_shu, (0.45, 70), "wood", None,
             "brush marks along u", uv=B.WORLD, note="Red lacquer wares; wears through to black (negoro)."),
         {"_w0": "even shu", "_w1": "rubbed to black at the edges", "_w2": "flaking to the wood, dusty"},
         ["jp_f_sg lacquer", "jp_f_soba_board", "jp_f_doll_tiers"], "Red lacquer wares"),
        (B.M("jp_m_ceramic_porcelain", "ceramic", "porcelain_sometsuke", 0.25, 256, ceramic_porcelain, (0.45, 70),
             "pottery", None, "cobalt bands along u (round the pot), scroll between", uv=B.WORLD + "; u round the pot",
             note="Blue-and-white porcelain (Hizen). No glass, no enamel colours."),
         {"_w0": "clean glaze", "_w1": "dust, a few chips", "_w2": "crazed and grimy"},
         ["jp_f_sg porcelain", "jp_f_ware_crate"], "Blue-and-white porcelain wares"),
        (B.M("jp_m_leather_tan", "textile", "cha_koge", 0.5, 256, leather_tan, (0.12, 25), "cloth", None,
             "pebbled grain, creases along u", uv=B.WORLD),
         {"_w0": "new tanned leather", "_w1": "rubbed lighter at the edges", "_w2": "mould bloom"},
         ["jp_f_sg pouches", "jp_f_hides"], "Leather goods"),
        (B.M("jp_m_food_tofu", "food", "gofun_white", 0.25, 256, food_tofu, (0.1, 20), "cloth", None,
             "faint pores, the press-cloth weave", uv=B.WORLD),
         {"_w0": "fresh white", "_w1": "dried, yellowed", "_w2": "mouldy"},
         ["jp_f_tofu_tank", "jp_f_sg sweets"], "Tofu and rice cakes"),
    ]


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    added = add_palette()
    B._ATLAS["shop"] = shop_layout(1024)
    for mid in ("jp_m_lacquer_shu", "jp_m_ceramic_porcelain"):   # glazed like the other lacquer / ceramics (C19 exempt)
        B.BM.FINISH_BY_ID.setdefault(mid, "glazed")
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        if only and mid not in only:
            continue
        B.MATS.append(m)
        B.BYID[mid] = m
        B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by, "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"][-1] = {"procedural": "make_s1_materials.py (on make_b1_materials.make_one)"}
        sc["made_by"] = "research/materials/make_s1_materials.py (agent S1, 2026-09-30), through B1's make_one"
        sc["requested_by"] = "research/interior/SHOP_SETS.md (S1, the shop sets)"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-36s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_s1.json"), json.dumps({"check": "C1 palette (tools/matcheck), S1 materials",
                                                           "palette_entries_added": added, "results": allres},
                                                          indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("S1 materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
