"""W3B: the labelled island map (research/production/contact_sheets/w3b_map.jpg) and the W3B section of
spikes/SH1/SHOWCASE_MAP.md, from spikes/W3B/w3b_items.json (written by layout_w3b.py).
  python spikes/W3B/map_w3b.py"""
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
import layout_w3b as LD  # noqa: E402

MD = os.path.join(DEV, "spikes", "SH1", "SHOWCASE_MAP.md")
A, B = "<!-- W3B BEGIN -->", "<!-- W3B END -->"
AREAS = [("A", "The artisans' street, east of the spawn (panel A)"),
         ("B", "Bathhouse + stable yard by the post-town street (panel B)"),
         ("T", "Timber yard at the south edge (panel T/F)"),
         ("F", "Foundry yard at the south edge (panel T/F)")]
PANELS = [("A", (1030.0, 1096.0, 985.0, 1022.0)), ("B", (1036.0, 1082.0, 1044.0, 1068.0)),
          ("T/F", (996.0, 1056.0, 898.0, 926.0))]
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
        if os.path.basename(p) == "W3B.csv":
            continue
        for row in csv.DictReader(open(p, newline="")):
            k = row["p3d"].lower()
            if k in recs:
                out.append((row["p3d"], LW.corners(recs[k], (float(row["x"]), 25.0, float(row["z"])),
                                                   float(row["yaw_deg"]))))
    return out


def panel(name, box, items, S=9.0):
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
        if os.path.basename(p) in ("W3B.csv", "C.csv"):
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


def main():
    with open(os.path.join(HERE, "w3b_items.json"), "rb") as f:
        items = json.loads(f.read().decode("utf-8"))
    ims = [panel(n, b, items) for n, b in PANELS]
    W = max(ims[0].width, ims[1].width + ims[2].width + 10) + 30
    H = ims[0].height + max(ims[1].height, ims[2].height) + 120
    sheet = Image.new("RGB", (W, H), (245, 244, 240))
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), "W3B wave 3b on the test island: workshops, stalls, bathhouse, stable yard, timber yard, foundry "
           "(IDs = SHOWCASE_MAP.md W3B)", font=F["h"], fill=(0, 0, 0))
    d.text((10, 38), "red = furnished building, brown = yard fence, green dot = free prop (stall, logs, bell mould), "
           "grey = earlier agents' objects; spawn (1024, 985) is west of panel A", font=F["s"], fill=(40, 40, 40))
    sheet.paste(ims[0], (10, 60))
    sheet.paste(ims[1], (10, 70 + ims[0].height))
    sheet.paste(ims[2], (20 + ims[1].width, 70 + ims[0].height))
    out = os.path.join(DEV, "research", "production", "contact_sheets", "w3b_map.jpg")
    sheet.save(out, quality=88)
    print(out, sheet.size)
    md = [A, "", "## W3B wave 3b: workshops, services, stalls, timber yard, foundry (agent W3B, 2026-10-02)", "",
          "Regenerate: `python spikes/W3B/layout_w3b.py` then `python spikes/W3B/map_w3b.py`. Map: "
          "research/production/contact_sheets/w3b_map.jpg. Buildings are furnished variants (`buildings/w3b_sets.py`); "
          "yard fences (`Land_JP_Compound_*Yard`) are K3-kit objects; `.sN` = a site object of that building; IDs "
          "without a class are free props. y_off is over the ground at the object.", ""]
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
    print("SHOWCASE_MAP.md W3B section:", len(items), "items")


if __name__ == "__main__":
    main()
