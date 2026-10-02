"""W3C1: the labelled district map (research/production/contact_sheets/w3c1_map.jpg: the trade quarter + where it lies
on the island) and the W3C1 section of spikes/SH1/SHOWCASE_MAP.md, from spikes/W3C1/w3c1_items.json (layout_w3c1.py).
  python spikes/W3C1/map_w3c1.py"""
import glob
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [os.path.join(DEV, "spikes", "SH1"), os.path.join(DEV, "spikes", "W2F"), os.path.join(DEV, "buildings"),
                os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")]
import terrain_sh1 as T  # noqa: E402
import layout_w2f as LW  # noqa: E402
sys.path.insert(0, HERE)
import layout_w3c1 as LD  # noqa: E402

MD = os.path.join(DEV, "spikes", "SH1", "SHOWCASE_MAP.md")
A, B = "<!-- W3C1 BEGIN -->", "<!-- W3C1 END -->"
AREAS = [("BR", "The sake brewery (north of the lane, west): the kasane-gura, the polishing shed, the cask kura, the brewer's shop"),
         ("DY", "The indigo dyer (north of the lane, east) and its drying yard"),
         ("PM", "The paper mill (north of the lane, far east) and its drying yard"),
         ("WM", "The water mill (south of the lane)"),
         ("LN", "On the lane")]
PANELS = [("W3C1 trade quarter", (880.0, 950.0, 849.0, 896.0))]
NEXT = [("3c-2: west", (835.0, 882.0, 850.0, 900.0)), ("3c-2: south", (884.0, 946.0, 825.0, 851.0))]
F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h": (r"C:\Windows\Fonts\arialbd.ttf", 22),
                                                  "b": (r"C:\Windows\Fonts\arialbd.ttf", 13),
                                                  "s": (r"C:\Windows\Fonts\arial.ttf", 12)}.items()}


def other_polys():
    """Every building another agent's CSV places (C / C3 / W2F / ...), as its record footprint."""
    import csv
    recs = {}
    for p in glob.glob(os.path.join(DEV, "buildings", "*", "records", "*.json")) +             glob.glob(os.path.join(DEV, "buildings", "*", "record.json")):
        try:
            r = json.loads(open(p, "rb").read().decode("utf-8"))
        except Exception:
            continue
        if r.get("model") and r.get("bbox"):
            recs[r["model"].lstrip("\\").lower()] = r["bbox"]
    out = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) == "W3C1.csv":
            continue
        for row in csv.DictReader(open(p, newline="")):
            k = row["p3d"].lower()
            if k in recs:
                out.append((row["p3d"], LW.corners(recs[k], (float(row["x"]), 25.0, float(row["z"])),
                                                   float(row["yaw_deg"]))))
    return out


def panel(name, box, items, S=12.0):
    x0, x1, z0, z1 = box
    W, H = int((x1 - x0) * S), int((z1 - z0) * S)
    im = Image.new("RGB", (W, H + 30), (225, 228, 215))
    d = ImageDraw.Draw(im)

    def P(x, z):
        return ((x - x0) * S, 30 + (z1 - z) * S)
    for j in range(0, H, 6):
        for i in range(0, W, 6):
            h = T.ground(x0 + i / S, z1 - j / S)
            c = int(max(0, min(255, 215 + (h - 25.0) * 12)))
            d.rectangle([i, 30 + j, i + 6, 36 + j], fill=(c, c + 4 if c < 251 else c, c - 10 if c > 10 else c))
    # other agents' buildings (grey) and points
    for nm, poly in other_polys():
        if any(x0 - 5 < q[0] < x1 + 5 and z0 - 5 < q[1] < z1 + 5 for q in poly):
            d.polygon([P(*q) for q in poly], outline=(150, 150, 150), fill=(205, 205, 200))
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) in ("W3C1.csv",):
            continue
        import csv
        for row in csv.DictReader(open(p, newline="")):
            x, z = float(row["x"]), float(row["z"])
            k = row["p3d"].lower()
            if x0 < x < x1 and z0 < z < z1:
                q = P(x, z)
                d.ellipse([q[0] - 2, q[1] - 2, q[0] + 2, q[1] + 2], fill=(160, 160, 170))
    for g in range(int(x0 // 10 * 10), int(x1) + 1, 10):
        d.line([P(g, z0), P(g, z1)], fill=(190, 190, 185))
        if g % 20 == 0:
            d.text((P(g, z1)[0] + 2, 31), str(g), font=F["s"], fill=(80, 80, 80))
    for g in range(int(z0 // 10 * 10), int(z1) + 1, 10):
        d.line([P(x0, g), P(x1, g)], fill=(190, 190, 185))
        if g % 20 == 0:
            d.text((2, P(x0, g)[1] - 14), str(g), font=F["s"], fill=(80, 80, 80))
    for it in items:
        if it["id"].count(".") or not it.get("key"):
            continue
        r = LD.rec(it["key"])
        pos = (it["x"], 25.0, it["z"])
        if it["key"].startswith(LD.LINE_KINDS):
            for sp in LD.strips(it["key"], pos, it["yaw"]):
                d.polygon([P(*q) for q in sp], fill=(120, 80, 40))
            continue
        poly = LW.corners(r["bbox"], pos, it["yaw"])
        col = (200, 70, 50) if it["key"].startswith("f_") else ((60, 110, 190) if "roka" in it["key"] else (220, 150, 60))
        d.polygon([P(*q) for q in poly], outline=(40, 20, 10), fill=col)
        # the model front (+z) arrow
        fx, fz = LW.to_world(0.0, (r["bbox"][5]) * 0.6, pos, it["yaw"])
        d.line([P(it["x"], it["z"]), P(fx, fz)], fill=(255, 255, 255), width=2)
    for it in items:
        if it["id"].count(".") or it.get("key") or not (x0 < it["x"] < x1 and z0 < it["z"] < z1):
            continue
        q = P(it["x"], it["z"])
        d.ellipse([q[0] - 5, q[1] - 5, q[0] + 5, q[1] + 5], fill=(40, 140, 60), outline=(0, 0, 0))
        d.text((q[0] + 6, q[1] - 6), it["id"], font=F["b"], fill=(0, 60, 0))
    for it in items:
        if it["id"].count(".") or not it.get("key"):
            continue
        q = P(it["x"], it["z"])
        tx = it["id"]
        w = d.textlength(tx, font=F["b"])
        d.rectangle([q[0] - w / 2 - 3, q[1] - 9, q[0] + w / 2 + 3, q[1] + 8], fill=(255, 255, 240), outline=(0, 0, 0))
        d.text((q[0] - w / 2, q[1] - 8), tx, font=F["b"], fill=(0, 0, 0))
    d.text((6, 4), "panel %s: x %d-%d, z %d-%d (north up; 10 m grid; white tick = model front)" % (name, x0, x1, z0, z1),
           font=F["b"], fill=(0, 0, 0))
    return im


def locator(S=1.6):
    """Where the district lies: the yard pad, the spawn, every placed building (grey), the W3C1 district (red box) and
    the free ground next to it for the next districts (dashed blue)."""
    x0, x1, z0, z1 = 820.0, 1150.0, 820.0, 1140.0
    W, H = int((x1 - x0) * S), int((z1 - z0) * S)
    im = Image.new("RGB", (W, H + 30), (225, 228, 215))
    d = ImageDraw.Draw(im)

    def P(x, z):
        return ((x - x0) * S, 30 + (z1 - z) * S)
    for j in range(0, H, 4):
        for i in range(0, W, 4):
            h = T.ground(x0 + i / S, z1 - j / S)
            c = int(max(0, min(255, 200 + (h - 25.0) * 10)))
            flat = abs(h - 25.0) < 0.05
            d.rectangle([i, 30 + j, i + 4, 34 + j], fill=(c - 25, c, c - 35) if flat else (c, c, c - 12))
    for nm, poly in other_polys():
        d.polygon([P(*q) for q in poly], outline=(120, 120, 120), fill=(185, 185, 180))
    bx = LD.DISTRICT
    d.rectangle([P(bx[0], bx[3]), P(bx[1], bx[2])], outline=(200, 30, 30), width=3)
    d.text((P(bx[0], bx[3])[0], P(bx[0], bx[3])[1] - 16), "W3C1 trade quarter", font=F["b"], fill=(200, 30, 30))
    for nm, b in NEXT:
        d.rectangle([P(b[0], b[3]), P(b[1], b[2])], outline=(40, 80, 200), width=2)
        d.text((P(b[0], b[3])[0] + 3, P(b[0], b[3])[1] + 3), nm, font=F["s"], fill=(40, 80, 200))
    q = P(1024.0, 985.0)
    d.ellipse([q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6], fill=(255, 220, 0), outline=(0, 0, 0))
    d.text((q[0] + 8, q[1] - 7), "spawn", font=F["b"], fill=(0, 0, 0))
    d.line([q, P((bx[0] + bx[1]) / 2, (bx[2] + bx[3]) / 2)], fill=(200, 30, 30), width=2)
    for g in range(840, 1141, 50):
        d.text((P(g, z1)[0] + 2, 31), str(g), font=F["s"], fill=(60, 60, 60))
        d.text((2, P(x0, g)[1] - 14), str(g), font=F["s"], fill=(60, 60, 60))
    d.text((6, 4), "where it is: green = the flat yard pad (25.0 m), grey = every earlier building, red = W3C1, "
           "blue = free ground for the next districts", font=F["b"], fill=(0, 0, 0))
    return im


def main():
    with open(os.path.join(HERE, "w3c1_items.json"), "rb") as f:
        items = json.loads(f.read().decode("utf-8"))
    pa = panel(PANELS[0][0], PANELS[0][1], items)
    lo = locator()
    W = pa.width + lo.width + 30
    H = max(pa.height, lo.height) + 100
    sheet = Image.new("RGB", (W, H), (245, 244, 240))
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), "W3C1 wave 3c-1 on the test island: the trade quarter (sake brewery, dyer, paper mill, water mill); "
           "IDs = SHOWCASE_MAP.md W3C1", font=F["h"], fill=(0, 0, 0))
    d.text((10, 38), "left: red = furnished building, brown = yard fence, green dot = free prop, grey = nothing else here; "
           "white tick = model front. The lane runs east-west at z 861.5-866 (district x %d-%d, z %d-%d)." % LD.DISTRICT,
           font=F["s"], fill=(40, 40, 40))
    sheet.paste(pa, (10, 60))
    sheet.paste(lo, (20 + pa.width, 60))
    out = os.path.join(DEV, "research", "production", "contact_sheets", "w3c1_map.jpg")
    sheet.save(out, quality=88)
    print(out, sheet.size)
    md = [A, "", "## W3C1 wave 3c-1: the trade quarter (sake brewery, dyer, paper mill, water mill) (agent W3C1, "
          "2026-10-02)", "",
          "**District (Stephen, 2026-10-02: one new district per wave, off the showcase):** x %d-%d, z %d-%d, south-west "
          "of the yard pad, ~160 m from the spawn (1024, 985); an east-west lane at z 861.5-866. **Free ground for the "
          "next districts (3c-2 etc.):** west of it x 835-882, z 850-900 (25.6-26.4 m, gentle) and south of it x 884-946, "
          "z 825-851 (a 2 %% slope down to the south). Ground survey: spikes/W3C1/W3C1_NOTES.md \"District\"." % LD.DISTRICT,
          "",
          "Regenerate: `python spikes/W3C1/layout_w3c1.py` then `python spikes/W3C1/map_w3c1.py`. Map: "
          "research/production/contact_sheets/w3c1_map.jpg. Buildings are furnished variants (`buildings/w3c1_sets.py`); "
          "yard fences (`Land_JP_Compound_*`) are K3-kit objects; `.sN` = a site object of that building; IDs without a "
          "class are free props. y_off is over the ground at the object (a building on uneven ground sits so no floor "
          "has terrain poking through it).", ""]
    for code, title in AREAS:
        md += ["### %s" % title, "", "| ID | Class / p3d | x | z | yaw | y_off | What |", "|---|---|---|---|---|---|---|"]
        for it in items:
            if it["area"] != code:
                continue
            name = it["class"] or os.path.basename(it["p3d"])
            md.append("| %s | `%s` | %.2f | %.2f | %.0f | %.2f | %s |" % (it["id"], name, it["x"], it["z"], it["yaw"],
                                                                        it["y_off"], it["label"]))
        md.append("")
    md.append(B)
    with open(MD, "rb") as f:
        s = f.read().decode("utf-8")
    block = "\n".join(md)
    if A in s:
        s = s[:s.index(A)] + block + s[s.index(B) + len(B):]
    else:
        s = s.rstrip("\n") + "\n\n" + block + "\n"
    with open(MD, "wb") as f:
        f.write(s.encode("utf-8"))
    print("SHOWCASE_MAP.md W3C1 section:", len(items), "items")


if __name__ == "__main__":
    main()
