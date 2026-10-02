"""W3D: the labelled district map (research/production/contact_sheets/w3d_map.jpg: the government buildings + where
they lie on the island, west of 3c-2) and the W3D section of spikes/SH1/SHOWCASE_MAP.md, from spikes/W3D/w3d_items.json
(layout_w3d.py). Copied from spikes/W3C2/map_w3c2.py.
  python spikes/W3D/map_w3d.py"""
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
sys.path.insert(0, os.path.join(DEV, "spikes", "W3C1"))
import layout_w3c1 as L1  # noqa: E402
import layout_w3d as LD  # noqa: E402
sys.path.insert(0, os.path.join(DEV, "spikes", "W3C2"))
import layout_w3c2 as L2  # noqa: E402
LD.rec, LD.strips = L1.rec, L1.strips

MD = os.path.join(DEV, "spikes", "SH1", "SHOWCASE_MAP.md")
A, B = "<!-- W3D BEGIN -->", "<!-- W3D END -->"
AREAS = [("SK", "The checkpoint (west end; the lane runs through its two kora-mon gates)"),
         ("JY", "The intendant's jinya (north of the lane): the black nagaya-mon, the office, the court room + its gravel "
                "court, the tax-rice kura"),
         ("TY", "The post-station office and its yard (south of the lane, east)"),
         ("FB", "The fire brigade (south of the lane): the tall watchtower, the tool shed"),
         ("RY", "The jail (south of the lane, west): the cell block, the guard office")]
PANELS = [("W3D government district", (740.0, 830.0, 840.0, 896.0))]
NEXT = []
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
        if os.path.basename(p) == "W3D.csv":
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
        if os.path.basename(p) in ("W3D.csv",):
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
        col = (200, 70, 50) if it["key"].startswith("f_") else (220, 150, 60)
        d.polygon([P(*q) for q in poly], outline=(40, 20, 10), fill=col)
        # the model front (+z) arrow
        fx, fz = LW.to_world(0.0, (r["bbox"][5]) * 0.6, pos, it["yaw"])
        d.line([P(it["x"], it["z"]), P(fx, fz)], fill=(255, 255, 255), width=2)
    for nm, (a0, a1, c0, c1) in LD.LANES.items():
        d.rectangle([P(a0, c1), P(a1, c0)], outline=(150, 110, 60), fill=(235, 215, 170))
        d.text((P(a0, c1)[0] + 2, P(a0, c1)[1] + 1), nm, font=F["s"], fill=(120, 80, 30))
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
    x0, x1, z0, z1 = 735.0, 1150.0, 810.0, 1140.0
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
    d.text((P(bx[0], bx[3])[0], P(bx[0], bx[3])[1] - 16), "W3D government", font=F["b"], fill=(200, 30, 30))
    b1 = L1.DISTRICT
    d.rectangle([P(b1[0], b1[3]), P(b1[1], b1[2])], outline=(40, 80, 200), width=2)
    d.text((P(b1[0], b1[3])[0] + 3, P(b1[0], b1[3])[1] + 3), "3c-1", font=F["s"], fill=(40, 80, 200))
    b2 = L2.DISTRICT
    d.rectangle([P(b2[0], b2[3]), P(b2[1], b2[2])], outline=(40, 80, 200), width=2)
    d.text((P(b2[0], b2[3])[0] + 3, P(b2[0], b2[3])[1] + 3), "3c-2", font=F["s"], fill=(40, 80, 200))
    for nm, b in NEXT:
        d.rectangle([P(b[0], b[3]), P(b[1], b[2])], outline=(40, 80, 200), width=2)
        d.text((P(b[0], b[3])[0] + 3, P(b[0], b[3])[1] + 3), nm, font=F["s"], fill=(40, 80, 200))
    q = P(1024.0, 985.0)
    d.ellipse([q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6], fill=(255, 220, 0), outline=(0, 0, 0))
    d.text((q[0] + 8, q[1] - 7), "spawn", font=F["b"], fill=(0, 0, 0))
    d.line([q, P((bx[0] + bx[1]) / 2, (bx[2] + bx[3]) / 2)], fill=(200, 30, 30), width=2)
    for g in range(750, 1141, 50):
        d.text((P(g, z1)[0] + 2, 31), str(g), font=F["s"], fill=(60, 60, 60))
        d.text((2, P(x0, g)[1] - 14), str(g), font=F["s"], fill=(60, 60, 60))
    d.text((6, 4), "where it is: green = the flat yard pad (25.0 m), grey = every earlier building, red = W3D, "
           "blue = 3c-1 + 3c-2", font=F["b"], fill=(0, 0, 0))
    return im


def main():
    with open(os.path.join(HERE, "w3d_items.json"), "rb") as f:
        items = json.loads(f.read().decode("utf-8"))
    pa = panel(PANELS[0][0], PANELS[0][1], items)
    lo = locator()
    W = pa.width + lo.width + 30
    H = max(pa.height, lo.height) + 100
    sheet = Image.new("RGB", (W, H), (245, 244, 240))
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), "W3D wave 3d on the test island: the government buildings (checkpoint, post-station office, jinya, "
           "jail, fire brigade); IDs = SHOWCASE_MAP.md W3D", font=F["h"], fill=(0, 0, 0))
    d.text((10, 38), "left: red = furnished building, orange = gravel court, brown = fence / palisade, green dot = free "
           "prop (the tall watchtower = FB3), sand = the lane LG (from 3c-2's corner west through the checkpoint); white "
           "tick = model front (district x %d-%d, z %d-%d)." % LD.DISTRICT, font=F["s"], fill=(40, 40, 40))
    sheet.paste(pa, (10, 60))
    sheet.paste(lo, (20 + pa.width, 60))
    out = os.path.join(DEV, "research", "production", "contact_sheets", "w3d_map.jpg")
    sheet.save(out, quality=88)
    print(out, sheet.size)
    md = [A, "", "## W3D wave 3d: the government buildings (checkpoint, post-station office, jinya, jail, fire brigade) "
          "(agent W3D, 2026-10-02)", "",
          "**District (Stephen's one-district rule):** x %d-%d, z %d-%d, west of 3c-2's west lane (24.0-25.7 m: a ~1.3 %% "
          "fall west along the lane, 3-4 %% to the south). ONE lane LG (z 862-866) from 3c-2's west-lane corner (826, 864) "
          "west through the district and through the checkpoint's two kora-mon gates (Edo side x 771.7, Kyoto side x "
          "748.0) to x 744. North of the lane the jinya; south of it, from the east, the post-station office, the fire "
          "brigade and the jail; the checkpoint at the west end. Every building is seated so no floor has terrain "
          "through it (spikes/W3D/floorcheck.py); the low side of a hall shows its cut-stone foundation band, the board "
          "fences their 0.60 skirt, the palisade's logs run 1 m down." % LD.DISTRICT, "",
          "Regenerate: `python spikes/W3D/layout_w3d.py` then `python spikes/W3D/map_w3d.py`. Map: "
          "research/production/contact_sheets/w3d_map.jpg. Halls are furnished variants (`buildings/w3d_sets.py`); the "
          "fences / palisade (`Land_JP_Compound_*`) and the gravel courts (`Land_JP_Oshirasu_*`) are kit objects "
          "(`templates/govsite.py`); `.sN` = a site object of that building; IDs without a class are free props.", ""]
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
    print("SHOWCASE_MAP.md W3D section:", len(items), "items")


if __name__ == "__main__":
    main()
