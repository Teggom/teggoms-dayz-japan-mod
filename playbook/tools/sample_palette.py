"""Build playbook/palette.json and playbook/palette_swatches.png from sampled reference photos.

Method (same idea as the katana dossier colours, with its lessons applied):
- Each sampled entry lists one or more boxes (fractions of image width/height) on photos in data/playbook/refs/.
- Per box, pixels in the darkest and brightest 15 % (by luminance) are dropped (shadow, specular, stray
  neighbours), unless the entry asks for 'dark' (keep the 10-45th luminance percentile), 'light' (55-90th) or 'top' (75-95th),
  used for two-colour surfaces such as namako walls, white-stitched indigo or plaster between dark windows.
- The entry value is the mean of the per-box medians (each box weighs the same), sRGB 0-255.
- Spread = 75th percentile CIE76 delta-E of the kept pixels from that median. tolerance_dE = clamp(spread, 6, 14).
- Entries without a usable photo carry a 'reference' value with its source, marked method 'reference' or 'assumed'.
- The swatch sheet shows every swatch next to the exact crops it came from, so neighbours can be checked by eye.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PB = os.path.normpath(os.path.join(HERE, ".."))                    # japan_dev/playbook
ROOT = os.path.normpath(os.path.join(PB, ".."))                    # japan_dev
REFS = os.path.join(ROOT, "data", "playbook", "refs")

# id, name, material/pigment, group, tiers, sample boxes [(img, [x0,y0,x1,y1], select)], reference, note
E = []


def S(id, name, material, group, tiers, boxes=None, ref=None, method=None, note="", weathering=None, use=""):
    E.append(dict(id=id, name=name, material=material, group=group, tiers=tiers, boxes=boxes or [], ref=ref,
                  method=method, note=note, weathering=weathering, use=use))


ALL = [1, 2, 3]
# ---- timber
S("timber_weathered", "Weathered exterior timber (sugi/hinoki, silver-brown)", "unpainted sugi / hinoki boards and posts, sun and rain aged",
  "timber", ALL, [("c02_narai_facade", [0.25, 0.55, 0.32, 0.72], None), ("c02_narai_facade", [0.33, 0.40, 0.40, 0.50], None), ("c12_higashi_chaya", [0.345, 0.15, 0.415, 0.30], None)],
  use="exterior boards, posts, board roofs, fences, rural everything",
  weathering={"clean": "timber_street_dark", "worst": "stone_lantern", "max_mix": 0.35})
S("timber_street_dark", "Dark street-front timber (oiled / soot-darkened)", "sugi/hinoki darkened by age, oil, soot or kakishibu (sampled wet, in rain)",
  "timber", [2, 3], [("c01_narai_street", [0.915, 0.42, 0.985, 0.62], None), ("c01_narai_street", [0.915, 0.06, 0.955, 0.19], None)],
  use="post-town and town facades, lattice frames, shop fronts")
S("timber_interior", "Interior timber, smoke-aged brown", "posts and frames inside a surviving farmhouse",
  "timber", ALL, [("c23_fukiya_katayama", [0.19, 0.30, 0.22, 0.70], None), ("c15_farmhouse_interior", [0.28, 0.45, 0.32, 0.65], "dark")],
  note="Warm artificial light. Machiya interiors are lighter (use timber_weathered darkened 10 %), farmhouses this or darker.")
S("timber_sooted", "Smoke-blackened beams (irori soot)", "structural timber and ceiling boards darkened by hearth smoke",
  "timber", ALL, ref=[36, 28, 22], method="assumed",
  note="The c15 roof space samples at about (9,5,3) because it is underexposed; a texture that dark reads as a hole in game. Keep albedo >= 30.",
  use="farmhouse and machiya kitchen roof space, beams above irori/kamado")
# ---- walls
S("shikkui_white", "Shikkui lime plaster, white", "slaked lime + seaweed glue + fibre (shikkui)",
  "wall", [2, 3], [("c09_himeji", [0.40, 0.62, 0.85, 0.72], "top"), ("c11_kurashiki", [0.55, 0.40, 0.68, 0.47], "top"), ("c03_tsumago_street", [0.79, 0.33, 0.86, 0.45], "top")],
  use="kura, castle, upper storeys of tier-3 townhouses, wall caps", weathering={"worst": "earth_wall_ochre", "max_mix": 0.25, "streaks": "rain streaks under eaves and sills, grime band 0-40 cm above ground"})
S("earth_wall_ochre", "Earthen wall, ochre (arakabe / nakanuri / tsuijibei)", "clay + straw over bamboo lath, or rammed earth",
  "wall", ALL, [("c29_earthen_wall", [0.18, 0.46, 0.72, 0.68], None), ("c12_higashi_chaya", [0.02, 0.30, 0.12, 0.50], None)],
  use="rural walls, interior walls, garden and temple earth walls", note="c12 is a repainted modern finish; c29 is the primary sample.")
S("earth_wall_interior", "Interior earthen wall (lit)", "interior clay finish seen in a surviving farmhouse",
  "wall", ALL, [("c15_farmhouse_interior", [0.74, 0.10, 0.95, 0.50], None)],
  note="Warm artificial light; use as the lit-interior check value, not as albedo.")
S("bengara_wall", "Bengara-red plaster", "earthen/lime plaster pigmented with bengara (iron oxide)",
  "wall", [3], [("c07_gion_machiya", [0.85, 0.30, 0.92, 0.42], None), ("c07_gion_machiya", [0.72, 0.46, 0.78, 0.51], None)],
  use="rare: a few prestige tea houses / pleasure-quarter fronts only", note="The Gion example (Ichiriki-tei) is famous precisely because it is unusual.")
S("neribei_clay", "Tile-course clay wall (neribei), mortar", "clay mortar between laid roof-tile courses",
  "wall", [2, 3], [("c25_tsuijibei", [0.52, 0.38, 0.60, 0.52], None)], use="temple / wealthy compound walls")
S("namako_tile", "Namako wall tile (dark)", "square flat tiles on kura lower walls",
  "wall", [2, 3], [("c11_kurashiki", [0.44, 0.62, 0.53, 0.74], "dark")])
S("namako_joint", "Namako joint plaster (white, raised)", "shikkui joints of namako walls",
  "wall", [2, 3], [("c11_kurashiki", [0.44, 0.62, 0.53, 0.74], "top")],
  note="Same material as shikkui_white, sampled in shade; use shikkui_white's texture with this as the shaded check value.")
S("kuro_board", "Black-stained boards (sumi / kakishibu)", "board cladding stained black",
  "wall", [2, 3], [("c16_hakone_sekisho", [0.86, 0.36, 0.96, 0.55], None)],
  use="official buildings (checkpoint, jinya, bansho), kura lower walls, castle-town board fences")
# ---- roofs
S("kawara_ibushi", "Kawara tile, ibushi silver-grey", "carbon-smoked fired clay tile (ibushi-gawara)",
  "roof", [2, 3], [("c08_kyomachiya", [0.18, 0.44, 0.60, 0.485], None), ("c14_minkaen_b", [0.40, 0.40, 0.62, 0.52], None), ("c04_tsumago_wakihonjin", [0.24, 0.48, 0.40, 0.52], None)],
  use="all tile roofs; never flat-textured: tiles are geometry (see PLAYBOOK roofs)", weathering={"worst": "kawara_weathered", "max_mix": 1.0})
S("kawara_weathered", "Kawara tile, weathered dark", "old ibushi tile with lichen and grime",
  "roof", [2, 3], [("c25_tsuijibei", [0.25, 0.21, 0.40, 0.27], None)])
S("thatch_weathered", "Thatch, weathered (kaya)", "susuki / reed thatch after years of weather",
  "roof", [1, 2], [("c05_ouchi_thatch", [0.85, 0.15, 0.98, 0.28], None), ("c06_shirakawa_gassho", [0.60, 0.55, 0.63, 0.62], None)],
  use="farmhouses, rural post towns, roadside tea houses", weathering={"clean": "thatch_new", "worst": "stone_lantern", "max_mix": 0.2, "moss": "moss_on_stone on north slopes"})
S("thatch_new", "Thatch, new", "freshly laid susuki / reed", "roof", [1, 2], ref=[176, 150, 98], method="assumed",
  note="No licensed photo of fresh thatch in the set. Straw-gold, pick up to 1 in 10 roofs as recently re-thatched.")
# ---- stone and ground
S("stone_granite", "Granite, weathered (ishigaki, gate posts)", "granite / hard stone, grey with warm specks",
  "stone", ALL, [("c09_himeji", [0.45, 0.84, 0.80, 0.97], None)],
  use="ishigaki, plinth stones (soseki), steps, lantern bodies, gravestones")
S("stone_lantern", "Stone lantern, lichen-grey", "weathered granite/andesite of shrine lanterns",
  "stone", ALL, [("c22_kasuga_lanterns", [0.625, 0.40, 0.675, 0.56], None)])
S("moss_on_stone", "Moss on stone / thatch", "moss and algae", "stone", ALL, [("c22_kasuga_lanterns", [0.30, 0.52, 0.42, 0.62], None)],
  use="weathering overlay only; never a base colour")
S("earth_road", "Packed earth (road, yard, exterior doma)", "compacted local soil", "ground", ALL,
  [("c05_ouchi_thatch", [0.30, 0.70, 0.55, 0.88], None), ("c16_hakone_sekisho", [0.45, 0.82, 0.62, 0.95], None)],
  use="roads, yards; interior doma = this darkened 20-30 % (compacted, smoke, damp)")
S("gravel_white", "White gravel / sand (shrine, court)", "decomposed granite sand (shirakawa-suna type)", "ground", [3],
  [("c22_kasuga_lanterns", [0.08, 0.80, 0.28, 0.95], None)], use="shrine approaches, bugyosho court (shirasu), temple courts")
# ---- pigments and paints
S("shu_vermilion", "Shu vermilion (shrine red)", "vermilion / red-lead paint on shrine timber",
  "paint", [3], [("c10_inari_torii", [0.33, 0.48, 0.365, 0.80], None), ("c10_inari_torii", [0.755, 0.47, 0.775, 0.58], None)],
  use="shrines, some temple gates/halls ONLY. Never on houses, shops or castles", note="Modern repaint; period shu is the same family (sampled in shade and sun).")
S("sumi_black", "Sumi black (lacquer / ink black)", "carbon black paint or lacquer", "paint", [3], ref=[52, 52, 52], method="reference",
  note="ja.wikipedia 'Nihon no iro no ichiran' sumi-iro #343434. The sampled black-stained boards (kuro_board) agree within tolerance.",
  use="torii kasagi, lacquered fittings, black plaster (kuro-shikkui) on castles")
S("bengara_lattice", "Bengara red-brown (lattice paint)", "iron-oxide red mixed with soot/oil on timber",
  "paint", [2, 3], [("c07_gion_machiya", [0.72, 0.36, 0.78, 0.45], None), ("c08_kyomachiya", [0.63, 0.60, 0.68, 0.70], None)],
  use="Kyoto/Osaka-side machiya lattices and fronts, sparingly")
S("gofun_white", "Gofun shell white", "calcined oyster-shell white", "paint", [3], ref=[205, 201, 192], method="assumed",
  note="Warm off-white on the same exposure scale as the sampled shikkui_white (vanilla whites ~150). Shrine carving, dolls. Not for walls.")
# ---- floors and fittings
S("tatami_aged", "Tatami, aged (igusa faded to straw)", "igusa rush mat face", "floor", [2, 3],
  [("c23_fukiya_katayama", [0.45, 0.74, 0.75, 0.86], None), ("c23_fukiya_katayama", [0.35, 0.66, 0.60, 0.72], None), ("c21_tatami", [0.55, 0.45, 0.95, 0.95], None)],
  use="all tatami; new green tatami only as rare accents", note="c23 is shaded daylight (golden), c21 is flat light (grey-beige).")
S("tatami_heri", "Tatami edge cloth (heri), plain", "black or indigo cotton/hemp binding", "floor", [2, 3], ref=[38, 36, 40], method="assumed",
  note="Commoner heri are plain dark; patterned (monberi) heri are temple/elite only.")
S("washi_shoji", "Shoji paper (washi)", "kozo paper", "fitting", [2, 3], ref=[200, 195, 182], method="assumed",
  note="Warm white on the shikkui_white exposure scale, never pure white; lets light through (alpha/translucency per B).")
S("bamboo_weathered", "Bamboo, weathered (inuyarai, fences)", "madake bamboo, sun-bleached", "fitting", ALL,
  [("c08_kyomachiya", [0.30, 0.76, 0.50, 0.88], None), ("c07_gion_machiya", [0.68, 0.84, 0.80, 0.95], None)])
S("sudare_reed", "Reed / bamboo blind (sudare)", "split bamboo or reed blind", "fitting", [2, 3],
  [("c08_kyomachiya", [0.36, 0.12, 0.56, 0.30], None)])
S("iron_black", "Wrought iron, dark", "iron fittings, pots, tools (katana dossier value)", "metal", ALL, ref=[76, 72, 69],
  method="reference", note="Measured in the katana dossier from Met 30091/30092 and TNM F-19992 (spikes/A_arms/katana_v2/DOSSIER.md s5).")
# ---- textiles
S("aizome_kachi", "Aizome, darkest indigo (kachi-iro)", "indigo-dyed cotton, many dips", "textile", ALL,
  [("m01_sashiko_jacket", [0.33, 0.62, 0.60, 0.78], "dark"), ("m02_indigo_piece", [0.03, 0.44, 0.30, 0.52], "dark")],
  use="work clothes, firemen, noren, futon covers; the commoner default")
S("aizome_kon", "Aizome, dark blue-grey (kon / nezumi-ai)", "indigo-dyed silk/cotton, faded", "textile", ALL,
  [("m03_kosode_stencil", [0.35, 0.40, 0.65, 0.80], None)])
S("aizome_maku", "Indigo curtain (maku / noren) as seen outdoors", "indigo cotton hanging in daylight", "textile", ALL,
  [("c16_hakone_sekisho", [0.03, 0.57, 0.10, 0.66], None)])
S("aizome_asagi", "Aizome, light (asagi / kamenozoki)", "indigo, few dips", "textile", ALL, ref=[128, 164, 178], method="assumed",
  note="Dictionary asagi (#00A4AC, ja.wikipedia) is a modern saturated rendering; this is a faded-cotton value. Verify with a museum sample.")
S("cha_danjuro", "Danjuro-cha (red-brown)", "tea-brown dye", "textile", ALL, ref=[159, 86, 58], method="reference",
  note="ja.wikipedia 'Nihon no iro no ichiran' #9F563A. One of the 'shijuhacha hyakunezumi' browns that sumptuary edicts pushed commoners toward.")
S("cha_koge", "Koge-cha (dark brown)", "tea-brown dye", "textile", ALL, ref=[106, 77, 50], method="reference", note="ja.wikipedia #6A4D32")
S("nezumi_rikyu", "Rikyu-nezumi (green-grey)", "grey dye", "textile", ALL, ref=[136, 142, 126], method="reference", note="ja.wikipedia #888E7E")
S("kinari_cloth", "Undyed cotton / hemp (kinari)", "unbleached cloth", "textile", ALL, ref=[190, 181, 160], method="assumed",
  note="Between dictionary kinari #C2B280 (khaki) and the shikkui_white scale. Loincloths, underlayers, sacks, bandages.")


def srgb_to_lab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], axis=-1)


def crop(img_id, box):
    im = Image.open(os.path.join(REFS, img_id + ".jpg")).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = box
    return im.crop((int(x0 * w), int(y0 * h), max(int(x1 * w), int(x0 * w) + 2), max(int(y1 * h), int(y0 * h) + 2)))


def keep(px, select):
    lum = px @ np.array([0.2126, 0.7152, 0.0722])
    if select == "dark":
        lo, hi = np.percentile(lum, [10, 45])
        return px[(lum >= lo) & (lum <= hi)]
    if select == "light":
        lo, hi = np.percentile(lum, [55, 90])
        return px[(lum >= lo) & (lum <= hi)]
    if select == "top":
        lo, hi = np.percentile(lum, [75, 95])
        return px[(lum >= lo) & (lum <= hi)]
    lo, hi = np.percentile(lum, [15, 85])
    return px[(lum >= lo) & (lum <= hi)]


def main():
    out, crops = [], {}
    for e in E:
        rec = {k: e[k] for k in ("id", "name", "material", "group", "tiers", "use", "note") if e[k] not in (None, "")}
        if e["boxes"]:
            pooled, cl = [], []
            for img_id, box, sel in e["boxes"]:
                c = crop(img_id, box)
                cl.append(c)
                px = np.asarray(c, dtype=np.float64).reshape(-1, 3)
                pooled.append(keep(px, sel))
            px = np.concatenate(pooled)
            med = np.mean([np.median(p, axis=0) for p in pooled], axis=0)   # each box weighs the same
            de = np.linalg.norm(srgb_to_lab(px) - srgb_to_lab(med), axis=1)
            spread = float(np.percentile(de, 75))
            rgb = [int(round(v)) for v in med]
            rec.update(srgb=rgb, hex="#%02X%02X%02X" % tuple(rgb), method="sampled",
                       tolerance_dE76=int(round(min(14, max(6, spread)))), observed_spread_dE76=round(spread, 1),
                       samples=[{"ref": i, "box": b, "select": s or "mid 70 % luminance"} for i, b, s in e["boxes"]])
            crops[e["id"]] = cl
        else:
            rgb = e["ref"]
            rec.update(srgb=rgb, hex="#%02X%02X%02X" % tuple(rgb), method=e["method"],
                       tolerance_dE76=10 if e["method"] == "reference" else 12)
        if e["weathering"]:
            rec["weathering"] = e["weathering"]
        out.append(rec)
    doc = {
        "version": 1,
        "colour_space": "sRGB, 8-bit, gamma-encoded (as in a _co texture)",
        "tolerance_metric": "CIE76 delta-E in CIELAB (D65). A texture passes when the mean colour of the material area, "
                            "excluding painted-on dirt/detail masks, is within tolerance_dE76 of srgb.",
        "method": "See playbook/tools/sample_palette.py docstring. Photos: data/playbook/refs (local only), listed in playbook/refs_index.json.",
        "method_values": {"sampled": "median of photo pixels", "reference": "value from a cited text source",
                          "assumed": "no licensed sample; reasoned value, verify when a sample is found"},
        "lighting_caveat": "Photo samples include daylight and camera processing. They are targets for texture mean albedo "
                           "within tolerance, not physically exact albedo.",
        "vanilla_calibration": {
            "note": "Mean sRGB of vanilla DayZ _co textures (converted with ImageToPAA, 2026-09-27). Vanilla 'white' walls sit near 150, "
                    "so photo-sampled whites of 130-195 are in the engine's range and pure 230+ whites would glow. At gate G3 compare in engine "
                    "and, if needed, apply ONE global exposure factor to all JP textures (expected 0.8-1.0).",
            "dz/structures/data/stucco_white_clean_01_co": [144, 144, 144],
            "dz/structures/data/plaster/coalplant_plaster_white_co": [155, 154, 151],
            "dz/structures/data/plaster/housebt_plaster1_co": [154, 156, 141],
            "dz/structures/data/wood_planks_gray_co": [112, 110, 107],
            "dz/structures/data/wood/planksold_01_co": [85, 84, 78],
            "dz/structures/data/wood/bridge_wood_planks_co": [108, 99, 92],
            "dz/structures/data/roof/roof_ceramic_01_co": [101, 73, 48],
            "dz/structures/data/roof/roof_ceramic_old_co": [104, 79, 64],
            "dz/structures/data/roof/cowshed_roof_co": [80, 80, 79]
        },
        "entries": out,
    }
    with open(os.path.join(PB, "palette.json"), "wb") as f:
        f.write(json.dumps(doc, indent=1, ensure_ascii=False).encode("utf-8"))
    sheet(out, crops)


def sheet(out, crops):
    cols, cw, ch = 2, 800, 118
    rows = math.ceil(len(out) / cols)
    im = Image.new("RGB", (cols * cw, rows * ch + 40), (32, 32, 32))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
        small = ImageFont.truetype("arial.ttf", 12)
    except OSError:
        font = small = ImageFont.load_default()
    d.text((10, 10), "JP playbook palette v1 - swatch | sample crops (as cut from the refs) | id, hex, tolerance, method",
           fill=(230, 230, 230), font=font)
    for k, e in enumerate(out):
        x = (k % cols) * cw + 10
        y = 40 + (k // cols) * ch
        d.rectangle([x, y, x + 100, y + 100], fill=tuple(e["srgb"]), outline=(90, 90, 90))
        cx = x + 110
        for c in crops.get(e["id"], [])[:3]:
            t = c.copy()
            t.thumbnail((110, 100))
            im.paste(t, (cx, y))
            cx += t.width + 6
        tx = x + 470 if crops.get(e["id"]) else x + 110
        d.text((tx, y + 2), e["id"], fill=(255, 255, 255), font=font)
        d.text((tx, y + 22), "%s  dE %d  %s" % (e["hex"], e["tolerance_dE76"], e["method"]), fill=(200, 200, 200), font=small)
        name = e["name"]
        d.text((tx, y + 40), name[:40], fill=(170, 170, 170), font=small)
        if len(name) > 40:
            d.text((tx, y + 55), name[40:80], fill=(170, 170, 170), font=small)
        d.text((tx, y + 75), "tiers " + ",".join(str(t) for t in e["tiers"]), fill=(150, 150, 150), font=small)
    im.save(os.path.join(PB, "palette_swatches.png"))


if __name__ == "__main__":
    main()
