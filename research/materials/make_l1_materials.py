#!/usr/bin/env python3
r"""make_l1_materials.py - the materials L1 (the interior life layer, research/interior/LIFE_LAYER.md) ADDS to jp_common
through B1's pipeline.

  python make_l1_materials.py [--no-pack] [--only ID[,ID...]]

Adds only; never changes an existing material or palette entry (the same route as make_b3b_materials.py: B1's
make_one = textures, PAAs, rvmats, sidecar, C1 matcheck on the PNG and the shipped PAA), then repacks jp_common.pbo.

- jp_m_decal_sumi_text_life  A second ink text atlas (B1's decal_sumi_text recipe and fonts: Yuji Syuku kanji, Yuji
                             Hentaigana Akebono kana, SIL OFL): paper charms (ofuda), the 1730 printed calendar, lantern
                             shop names and crests, the ledger cover, a sake-cask mark. B1's own atlas is untouched.
- jp_m_food_rice             Rice / grain spill and bowl rice (B3a's gap: spills used paper). Palette `rice_grain`.
- jp_m_food_hoshigaki        Dried persimmon: wrinkled dark orange-brown with a white sugar bloom. Palette `hoshigaki`.
- jp_m_textile_kaya          Mosquito-net hemp gauze, faded moegi green (Omi nets, BUILDING_LIST 1500). Palette
                             `kaya_moegi`.
The three palette entries are 'assumed' (no licensed period sample): judge in game.
C1 results: src/JP/common/materials/checks_l1.json. Never starts or stops the server or any GUI program.
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
    {"id": "rice_grain", "name": "Rice grains, polished (town) to part-polished", "material": "rice / millet grain",
     "group": "food", "tiers": [1, 2, 3], "use": "rice in bowls and measures, grain spills (jp_m_food_rice)",
     "note": "Added 2026-09-30 by L1. Assumed: an off-white with a warm cast (Edo townspeople ate polished rice; rural "
             "houses mixed grains, which reads a little darker). Judge in game.",
     "srgb": [206, 196, 170], "method": "assumed", "tolerance_dE76": 12},
    {"id": "hoshigaki", "name": "Dried persimmon (hoshigaki), with a white sugar bloom", "material": "dried fruit",
     "group": "food", "tiers": [1, 2], "use": "persimmon strings under beams and eaves (jp_m_food_hoshigaki)",
     "note": "Added 2026-09-30 by L1. Assumed: dark orange-brown flesh, the white bloom (ko) of a few weeks' drying. "
             "Judge in game.",
     "srgb": [128, 70, 42], "method": "assumed", "tolerance_dE76": 12},
    {"id": "kaya_moegi", "name": "Mosquito-net hemp, faded moegi green", "material": "hemp gauze (Omi kaya)",
     "group": "textile", "tiers": [2, 3], "use": "the folded mosquito net (jp_m_textile_kaya); the red edge uses "
                                                 "jp_m_textile_bib_red",
     "note": "Added 2026-09-30 by L1. Omi nets were green with a red edge (BUILDING_LIST 1500). Assumed: a dulled "
             "yellow-green after years of summer use. Judge in game.",
     "srgb": [98, 112, 74], "method": "assumed", "tolerance_dE76": 12},
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


# ================================================================================================ the text atlas
# (name, (x0, y0, x1, y1) px on the 1024 atlas, what it is for); columns right to left as (text, size px, indent)
LIFE_CELLS = [
    ("ofuda_jingu", (0, 0, 100, 450), "jp_f_ofuda: Ise Jingu taima (the most widely held house charm)"),
    ("ofuda_akiba", (100, 0, 200, 450), "jp_f_ofuda: Akiba fire charm (kitchens, Edo)"),
    ("ofuda_somin", (200, 0, 300, 480), "jp_f_ofuda: Somin Shorai door charm"),
    ("ofuda_goo", (300, 0, 400, 330), "jp_f_ofuda: Kumano Goo hoin"),
    ("koyomi_kyoho15", (420, 0, 1024, 500), "jp_f_koyomi: the printed calendar for Kyoho 15 (1730), month heads and "
                                            "the 24 seasonal nodes"),
    ("chochin_iseya", (0, 520, 140, 880), "jp_f_chochin: shop name Iseya (the commonest Edo shop name)"),
    ("chochin_yamatoya", (140, 520, 280, 880), "jp_f_chochin: shop name Yamatoya"),
    ("crest_igeta", (280, 520, 420, 660), "jp_f_chochin / jp_f_yoroibitsu: family crest, well-frame in a ring"),
    ("crest_mitsubiki", (420, 520, 560, 660), "jp_f_chochin: family crest, three bars in a ring"),
    ("daifukucho", (560, 520, 700, 880), "jp_f_choba_set: ledger cover 'daifukucho' with the year"),
    ("taru_morohaku", (700, 520, 820, 800), "jp_f_taru: 'morohaku' (fine polished sake) on the cask wrap"),
]
LIFE_TEXT = {
    "ofuda_jingu": [("天照皇大神宮", 62, 0)], "ofuda_akiba": [("秋葉山大権現", 62, 0)],
    "ofuda_somin": [("蘇民将来子孫之門", 50, 0)], "ofuda_goo": [("牛王宝印", 66, 0)],
    "chochin_iseya": [("伊勢屋", 100, 0)], "chochin_yamatoya": [("大和屋", 100, 0)],
    "daifukucho": [("大福帳", 78, 0), ("享保十五年", 26, 2)], "taru_morohaku": [("諸白", 96, 0)],
}
MONTHS = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
NODES = [("立春", "雨水"), ("啓蟄", "春分"), ("清明", "穀雨"), ("立夏", "小満"), ("芒種", "夏至"), ("小暑", "大暑"),
         ("立秋", "処暑"), ("白露", "秋分"), ("寒露", "霜降"), ("立冬", "小雪"), ("大雪", "冬至"), ("小寒", "大寒")]


def life_layout(S, sc=2):
    """Coverage mask (0-1) and the cells' UV rectangles, drawn with B1's column writer (_col: the two OFL fonts)."""
    im = Image.new("L", (S * sc, S * sc), 0)
    d = ImageDraw.Draw(im)
    uv = {}
    for name, (x0, y0, x1, y1), use in LIFE_CELLS:
        uv[name] = {"uv": [round(x0 / S, 4), round(y0 / S, 4), round(x1 / S, 4), round(y1 / S, 4)], "for": use}
        if name == "koyomi_kyoho15":
            title = "享保十五年庚戌暦"
            uv[name]["text"] = title + " / " + " ".join(m + ":" + a + b for m, (a, b) in zip(MONTHS, NODES))
            lw = 4 * sc
            d.rectangle([(x0 + 8) * sc, (y0 + 8) * sc, (x1 - 8) * sc, (y1 - 8) * sc], outline=255, width=lw)
            B._col(d, (x1 - 50) * sc, (y0 + 30) * sc, title, 44, sc)                  # the title column, right
            gx0, gx1, gy0, gy1 = x0 + 22, x1 - 96, y0 + 22, y1 - 22
            d.line([((gx1 + 6) * sc, (y0 + 8) * sc), ((gx1 + 6) * sc, (y1 - 8) * sc)], fill=255, width=lw)
            cw, ch = (gx1 - gx0) / 6.0, (gy1 - gy0) / 2.0
            d.line([(gx0 * sc, (gy0 + ch) * sc), (gx1 * sc, (gy0 + ch) * sc)], fill=255, width=2 * sc)
            for k in range(12):
                row, colk = divmod(k, 6)
                cx1 = gx1 - colk * cw                                          # months run right to left
                cy0 = gy0 + row * ch
                if colk:
                    d.line([(cx1 * sc, cy0 * sc), (cx1 * sc, (cy0 + ch) * sc)], fill=255, width=2 * sc)
                B._col(d, (cx1 - cw * 0.28) * sc, (cy0 + 10) * sc, MONTHS[k], 28, sc)
                a, b = NODES[k]
                B._col(d, (cx1 - cw * 0.66) * sc, (cy0 + 40) * sc, a, 20, sc)
                B._col(d, (cx1 - cw * 0.86) * sc, (cy0 + 96) * sc, b, 20, sc)
            continue
        if name.startswith("crest_"):
            cx, cy, r = (x0 + x1) / 2 * sc, (y0 + y1) / 2 * sc, 60 * sc
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=255, width=11 * sc)
            if name == "crest_igeta":                   # a well frame: two verticals over two horizontals, tilted 45
                k = 26 * sc
                for s in (-1, 1):
                    d.polygon([(cx + s * k - 6 * sc, cy - 46 * sc), (cx + s * k + 6 * sc, cy - 46 * sc),
                               (cx + s * k + 6 * sc, cy + 46 * sc), (cx + s * k - 6 * sc, cy + 46 * sc)], fill=255)
                    d.polygon([(cx - 46 * sc, cy + s * k - 6 * sc), (cx + 46 * sc, cy + s * k - 6 * sc),
                               (cx + 46 * sc, cy + s * k + 6 * sc), (cx - 46 * sc, cy + s * k + 6 * sc)], fill=255)
                uv[name]["text"] = "(crest: igeta in a ring)"
            else:                                        # three horizontal bars in a ring (maru ni mitsubiki)
                for k in (-1, 0, 1):
                    yy = cy + k * 26 * sc
                    d.rectangle([cx - 44 * sc, yy - 8 * sc, cx + 44 * sc, yy + 8 * sc], fill=255)
                uv[name]["text"] = "(crest: three bars in a ring)"
            continue
        cols = LIFE_TEXT[name]
        uv[name]["text"] = " / ".join(c[0] for c in cols)
        pitch = [1.3 * s for _, s, _ in cols]
        x = x1 - (x1 - x0 - sum(pitch)) / 2
        for (t, s, ind), p in zip(cols, pitch):
            xc = x - p / 2
            n = sum(0.5 if c == " " else 1.06 for c in t) + ind
            top = y0 + max(10, ((y1 - y0) - n * s) / 2)
            B._col(d, xc * sc, (top + ind * s) * sc, t, s, sc)
            x -= p
    a = B._arr(im.resize((S, S), Image.LANCZOS).convert("RGB"))[..., 0]
    return a, uv


def decal_sumi_text_life(lv, S):
    """B1's decal_sumi_text recipe on the life atlas (same ink colours, kasure streaks, fading and flaking)."""
    m, _ = B.atlas("life", S)
    T, MT = B.T, B.MT
    t = [T("sumi_black", -2), T("sumi_black", 7, 2, 5), T("sumi_black", 8, 2, 5)][lv]
    co = B.base(t, 1 + 0.05 * MT.fbm(S, 2.4, 1, 1, 4201))
    kasure = np.clip(MT.fbm(S, 1.4, 1, 6, 4202) - 0.8, 0, 1)
    a = m * (1 - 0.35 * kasure)
    if lv == 1:
        a = a * np.clip(0.72 + 0.12 * MT.fbm(S, 2.4, 1, 1, 4203), 0.45, 0.9)
    if lv == 2:
        flake = MT.fbm(S, 2.0, 1, 1, 4204) > 0.5
        a = a * 0.42 * np.where(flake, 0.3, 1.0)
    return B.R(co, MT.flat_n(S), 0.9, B.Z(S), t, 0.05, 0.1, alpha=np.clip(a, 0, 1))


# ================================================================================================ food and the net
def food_rice(lv, S):
    """Loose rice grains (~5 x 2.5 mm; 512 px per 0.5 m tile = ~1 mm a pixel), packed, with shadowed gaps."""
    T, MT = B.T, B.MT
    t = [T("rice_grain", 2), T("rice_grain", -3, 0, 2), T("rice_grain", -8, 1, 5)][lv]
    rg = np.random.default_rng(4301)
    w = MT.Wrap(S)
    h = MT.Wrap(S)
    for _ in range(int(S * S / 14)):
        x, y = rg.uniform(0, S, 2)
        a = rg.uniform(0, math.pi)
        L, Wd = rg.uniform(2.0, 2.8), rg.uniform(1.0, 1.4)
        pts = [(x + L * math.cos(a + k * math.pi / 3) * (1 if k % 3 == 0 else 0.55) - Wd * 0.0,
                y + L * math.sin(a + k * math.pi / 3) * (1 if k % 3 == 0 else 0.55)) for k in range(6)]
        v = int(rg.uniform(150, 255))
        w.polygon(pts, v)
        h.polygon(pts, 255)
    val = w.arr()
    cov = MT.blur(h.arr(), 0.6)
    shade = 0.55 + 0.45 * cov
    co = B.base(t, (0.82 + 0.18 * val) * shade)
    mask = B.Z(S)
    if lv >= 1:                                                   # dust / husk flecks
        fl = MT.spots(S, [0, 30, 60][lv], 6, 0.8, 1.6, 8, 4302)
        co = MT.mix(co, (120, 100, 70), fl * 0.7)
        mask |= fl > 0.3
    if lv == 2:                                                   # grey mould and droppings
        mo = B.blobs(S, 4303, 1.5, 3.0, 2)
        co = MT.patch(co, mo, (128, 130, 118), 0.5, 4304)
        mask |= mo
    return B.R(np.clip(co, 0, 1), MT.h2n(cov * 1.5, 1.0), 0.85, mask, t, 0.05, 0.12)


def food_hoshigaki(lv, S):
    """Dried persimmon skin: fine wrinkles along v (the fruit hangs), darker creases, white sugar bloom patches."""
    T, MT = B.T, B.MT
    t = [T("hoshigaki", 3, 2, 3), T("hoshigaki"), T("hoshigaki", -4, -2, -3)][lv]
    wr = MT.fbm(S, 1.6, 6, 1, 4401)                               # wrinkles along v
    cr = np.clip(-MT.fbm(S, 1.3, 8, 1, 4402) - 0.9, 0, 1)         # deep creases
    co = B.base(t, 1 + 0.10 * wr - 0.35 * cr)
    bloom = np.clip(MT.fbm(S, 2.6, 1, 1, 4403) - [0.6, 0.3, 0.8][lv], 0, 1) * [0.35, 0.5, 0.25][lv]
    co = MT.mix(co, (214, 206, 190), bloom)
    mask = bloom > 0.15
    if lv == 2:                                                   # mould spots, black rot
        mo = MT.spots(S, 16, 6, 2, 5, 16, 4404)
        co = MT.mix(co, (40, 34, 28), mo * 0.8)
        mask |= mo > 0.3
    return B.R(np.clip(co, 0, 1), MT.h2n(wr * 1.2 - cr * 2.0, 1.0), 0.75, mask, t, 0.12, 0.25)


def textile_kaya(lv, S):
    """Coarse hemp gauze (~1.2 mm threads, open weave): the net's threads lighter, the gaps darker (it lies folded,
    so the gaps show the layer under it). Opaque (no alpha): folded, bundled or draped."""
    T, MT = B.T, B.MT
    t = [T("kaya_moegi", 2), T("kaya_moegi", -2, 0, 2), T("kaya_moegi", -5, -2, 4)][lv]
    yy, xx = B.grid(S)
    p = 8.0 * S / 512
    tx = np.abs(np.sin(math.pi * xx / p))
    ty = np.abs(np.sin(math.pi * yy / p))
    thread = np.maximum(tx > 0.55, ty > 0.55).astype(f32) * (0.85 + 0.15 * MT.fbm(S, 1.5, 1, 1, 4501))
    co = B.base(t, 0.72 + 0.4 * thread)
    mask = B.Z(S)
    if lv >= 1:                                                   # faded folds
        fold = np.clip(MT.fbm(S, 2.6, 1, 4, 4502), 0, None)
        co = co * (1 + [0, 0.10, 0.16][lv] * fold)[..., None]
    if lv == 2:                                                   # holes, mildew
        mil = MT.spots(S, 14, 8, 1, 3, 12, 4503)
        co = MT.mix(co, (64, 66, 56), mil * 0.7)
        mask |= mil > 0.3
    return B.R(np.clip(co, 0, 1), MT.h2n(thread * 1.2, 1.0), 0.85, mask, t, 0.05, 0.12)


def table():
    ATL = ("TEXT ATLAS, not world-scale (as jp_m_decal_sumi_text): map a face onto one cell's rectangle (\"cells\": "
           "u0, v0, u1, v1 with v down), keeping the cell's aspect; 1024 px = 1 m. Lay the decal 2-3 mm off the "
           "surface; never in Geometry/View/Fire. Text runs top to bottom, columns right to left.")
    return [
        (B.M("jp_m_decal_sumi_text_life", "paint", "sumi_black", 1.0, 1024, decal_sumi_text_life, (0.05, 10), None,
             None, "brush strokes (Yuji Syuku kanji, Yuji Hentaigana Akebono kana)", alpha="decal", uv=ATL,
             atlas_kind="life", note="The life layer's ink: paper charms, the Kyoho 15 (1730) calendar, lantern shop "
                                     "names and crests, the ledger cover, a sake-cask mark. Fonts: SIL OFL 1.1, Yuji "
                                     "Project Authors. Nothing emissive."),
         {"_w0": "crisp black ink", "_w1": "faded to grey-brown", "_w2": "ghost of text, flaking"},
         ["jp_f_ofuda", "jp_f_koyomi", "jp_f_chochin", "jp_f_choba_set", "jp_f_taru"],
         "Ink text for the life layer (charms, calendar, lanterns, ledgers, casks)"),
        (B.M("jp_m_food_rice", "food", "rice_grain", 0.5, 512, food_rice, (0.05, 12), "dirt", None,
             "none; loose grains", uv=B.WORLD),
         {"_w0": "clean polished grains", "_w1": "dusty, husk flecks", "_w2": "grey mould, droppings"},
         ["jp_f_meal_left", "jp_f_masu", "jp_f_mi", "jp_f_kamidana_set"], "Rice in bowls and measures, grain spills"),
        (B.M("jp_m_food_hoshigaki", "food", "hoshigaki", 0.25, 256, food_hoshigaki, (0.12, 25), "cloth", None,
             "wrinkles along v (the fruit hangs stalk up)", uv=B.WORLD),
         {"_w0": "fresh-dried, orange-brown", "_w1": "dark, white sugar bloom", "_w2": "black rot, mould"},
         ["jp_f_hoshigaki"], "Dried persimmons on strings (autumn)"),
        (B.M("jp_m_textile_kaya", "textile", "kaya_moegi", 0.5, 512, textile_kaya, (0.05, 12), "cloth", None,
             "open hemp gauze, threads along u and v", uv=B.WORLD,
             note="Folded / draped net: opaque. The red edge band is jp_m_textile_bib_red geometry."),
         {"_w0": "moegi green gauze", "_w1": "faded along the folds", "_w2": "mildew, holes"},
         ["jp_f_kaya"], "The mosquito net, folded and hung up for autumn"),
    ]


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    added = add_palette()
    B._ATLAS["life"] = life_layout(1024)
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
        sc["sources"][-1] = {"procedural": "make_l1_materials.py (on make_b1_materials.make_one)"}
        sc["made_by"] = "research/materials/make_l1_materials.py (agent L1, 2026-09-30), through B1's make_one"
        sc["requested_by"] = "research/interior/LIFE_LAYER.md (L1, the interior life layer)"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-36s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_l1.json"), json.dumps({"check": "C1 palette (tools/matcheck), L1 materials",
                                                           "palette_entries_added": added, "results": allres},
                                                          indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("L1 materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
