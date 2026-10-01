"""SH1 labelled overhead maps: the top-down orthographic renders (render_sh1.py 'maps') with every showcase ID drawn
on with PIL, a legend (ID -> short name), a north arrow and the direction / distance to the spawn.

  python spikes/SH1/map_labels.py        (after render_sh1.py maps; normally called by it)

Writes research/production/contact_sheets/sh1_map_<shrine|graveyard|gallery|street>.jpg. The IDs are the ones in
spikes/SH1/showcase_items.json, SHOWCASE_MAP.md and TEST_CHECKLIST.md.
"""
import json
import math
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "renders")
SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
SPAWN = (1024.0, 985.0)
FONT = r"C:\Windows\Fonts\arial.ttf"
FONTB = r"C:\Windows\Fonts\arialbd.ttf"

STREET = [  # (id, label, x, z) - the street units, north row then south row (registry placements)
    ("D1", "ironmonger (S1 demo, replaced the bare Edo board-roof unit)", 1046.146, 1087.64),
    ("D2", "tobacco (S1 demo, inserted)", 989.236, 1087.64),
    ("D3", "sweets / rice cakes (S1 demo, replaced the bare Kamigata corner unit)", 1003.238, 1087.64),
    ("D4", "apothecary (S1 demo, replaced the bare Edo 2-ken end unit)", 1040.590, 1087.64),
    ("D5", "tailor (S1 demo, inserted)", 1050.824, 1087.64),
    ("D6", "dolls (S1 demo, inserted)", 984.558, 1087.64),
    ("C-a", "rice dealer (C3)", 997.682, 1087.64), ("C-b", "paper shop (C3)", 993.004, 1087.64),
    ("C-c", "cloth dealer (C3)", 1054.592, 1087.64), ("C-d", "sake shop, corner (C3)", 1059.238, 1087.64),
    ("C-e", "bare Kamigata 3-ken end unit (moved to the new row end)", 979.002, 1087.64),
    ("C-f", "post-town house (C3, furnished home)", 988.730, 1072.36),
    ("C-g", "post-town row houses (bare)", 1000.0, 1072.36),
    ("C-h", "ordinary inn (C3)", 1013.122, 1071.45), ("C-i", "grand inn, two storeys (C3)", 1026.222, 1071.45),
    ("C-j", "town kura (C3)", 1000.0, 1097.5), ("S01", "shrine: first stone torii", 1024.0, 1099.5)]


def short(it):
    lab = it["label"].strip()
    if it["area"] == "gallery" and ": " in lab:
        lab = lab.split(": ", 1)[1]
    lab = re.sub(r"\s*\(.*$", "", lab)
    if it["area"] == "graveyard":
        lab = lab.split(",")[0]
    lab = lab.replace("sub-shrine row ", "row ").replace("hill stair ", "").replace("path to the hill stair: ", "path: ")
    return lab[:52]


def wanted(it):
    i = it["id"]
    if it["area"] == "graveyard":
        return not re.match(r"G\d-\d\d[sti]$", i)
    if it["area"] == "shrine":
        m = re.match(r"([KI])(\d\d)([EW]?)$", i)
        if m:
            return False                              # stair modules: labelled as ranges below
        return not i.endswith("h")
    return True


def draw_map(name, center, scale, res):
    raw = os.path.join(OUT, "sh1_map_%s_raw.png" % name)
    if not os.path.isfile(raw):
        print("missing", raw)
        return
    im = Image.open(raw).convert("RGB")
    W, H = im.size
    ppm = max(W, H) / scale
    cx, cz = center

    def P(x, z):
        return (W / 2 + (x - cx) * ppm, H / 2 - (z - cz) * ppm)
    items = json.load(open(os.path.join(HERE, "showcase_items.json"), encoding="utf-8"))
    labels = []
    if name == "street":
        labels = [(i, lab, x, z) for i, lab, x, z in STREET]
    else:
        for it in items:
            if it["area"] != name or not wanted(it):
                continue
            labels.append((it["id"], short(it), it["x"], it["z"]))
        if name == "shrine":
            for tag, what in (("K", "hill stair"), ("I", "Inari stair")):
                mods = [it for it in items if re.match(r"%s\d\d$" % tag, it["id"])]
                if mods:
                    for it in mods[::6] + ([mods[-1]] if (len(mods) - 1) % 6 else []):
                        labels.append((it["id"], "%s module" % what, it["x"] - 1.6, it["z"]))
            # sub-shrine huts
            for it in items:
                if re.match(r"S\d\dh$", it["id"]):
                    labels.append((it["id"], short(it).strip(), it["x"], it["z"]))
    fs = max(11, min(22, int(ppm * 0.42)))
    if name == "graveyard":
        fs = 15
    F = ImageFont.truetype(FONTB, fs)
    FS = ImageFont.truetype(FONT, max(12, int(fs * 0.9)))
    # dim the render a little so labels read
    ov = Image.new("RGB", im.size, (255, 255, 255))
    im = Image.blend(im, ov, 0.18)
    d = ImageDraw.Draw(im)
    boxes = []

    def free(b):
        return all(b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3] for o in boxes)
    pts = [P(x, z) for _, _, x, z in labels]
    for (i, lab, x, z), (px, py) in zip(labels, pts):
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(200, 30, 20))
        boxes.append((px - 3, py - 3, px + 3, py + 3))
    for (i, lab, x, z), (px, py) in zip(labels, pts):
        tw, th = d.textbbox((0, 0), i, font=F)[2:]
        placed = None
        for r in (6, 14, 26, 40, 56):
            for ang in (0, 180, 90, 270, 45, 135, 225, 315):
                a = math.radians(ang)
                lx = px + r * math.cos(a) + (0 if math.cos(a) >= -0.1 else -tw)
                ly = py - r * math.sin(a) - th / 2
                b = (lx - 1, ly - 1, lx + tw + 1, ly + th + 1)
                if 0 <= b[0] and b[2] < W and 0 <= b[1] and b[3] < H and free(b):
                    placed = (lx, ly, b, r)
                    break
            if placed:
                break
        if not placed:
            lx, ly = px + 6, py - th / 2
            placed = (lx, ly, (lx, ly, lx + tw, ly + th), 6)
        lx, ly, b, r = placed
        if r > 6:
            d.line([px, py, lx + (0 if lx > px else tw), ly + th / 2], fill=(200, 30, 20), width=1)
        d.rectangle(b, fill=(255, 255, 240))
        d.text((lx, ly), i, font=F, fill=(10, 10, 10))
        boxes.append(b)
    # north arrow + spawn direction
    ax, ay = W - 60, 70
    d.polygon([(ax, ay - 40), (ax - 14, ay), (ax + 14, ay)], fill=(20, 20, 20))
    d.text((ax - 8, ay + 4), "N", font=ImageFont.truetype(FONTB, 24), fill=(20, 20, 20))
    dx, dz = SPAWN[0] - cx, SPAWN[1] - cz
    dist = math.hypot(dx, dz)
    ux, uy = dx / dist, -dz / dist
    tt = min((W / 2 - 70) / abs(ux) if abs(ux) > 1e-6 else 1e9, (H / 2 - 70) / abs(uy) if abs(uy) > 1e-6 else 1e9)
    bx, by = W / 2 + ux * tt, H / 2 + uy * tt
    if 0 < W / 2 + dx * ppm < W and 0 < H / 2 - dz * ppm < H:
        sx, sy = P(*SPAWN)
        d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], outline=(0, 90, 200), width=3)
        d.text((sx + 10, sy - 10), "SPAWN", font=F, fill=(0, 90, 200))
    else:
        d.line([bx - ux * 50, by - uy * 50, bx, by], fill=(0, 90, 200), width=5)
        d.polygon([(bx + ux * 14, by + uy * 14), (bx - uy * 10, by + ux * 10), (bx + uy * 10, by - ux * 10)],
                  fill=(0, 90, 200))
        t = "to the spawn (1024, 985): %d m" % round(dist)
        tw = d.textbbox((0, 0), t, font=F)[2]
        tx = min(max(8, bx - tw / 2), W - tw - 8)
        ty = by - 46 if uy > 0 else by + 18
        d.rectangle([tx - 2, ty - 2, tx + tw + 2, ty + fs + 4], fill=(255, 255, 255))
        d.text((tx, ty), t, font=F, fill=(0, 90, 200))
    # scale bar (10 m)
    sb = 10 * ppm
    d.rectangle([20, H - 40, 20 + sb, H - 32], fill=(20, 20, 20))
    d.text((20, H - 30), "10 m", font=FS, fill=(20, 20, 20))
    # legend panel
    seen = []
    for i, lab, x, z in labels:
        if i not in [s[0] for s in seen]:
            seen.append((i, lab))
    lh = int(fs * 1.25)
    rows_per_col = max(1, (H - 90) // lh)
    ncol = (len(seen) + rows_per_col - 1) // rows_per_col
    colw = 380 if name != "street" else 560
    canvas = Image.new("RGB", (W + ncol * colw + 20, max(H, 90 + min(len(seen), rows_per_col) * lh)), (246, 244, 238))
    canvas.paste(im, (0, 0))
    dc = ImageDraw.Draw(canvas)
    dc.text((W + 12, 12), "SH1 %s map" % name, font=ImageFont.truetype(FONTB, 26), fill=(20, 20, 20))
    dc.text((W + 12, 46), "ID  short name (full table: spikes/SH1/SHOWCASE_MAP.md)", font=FS, fill=(70, 70, 70))
    for k, (i, lab) in enumerate(seen):
        c, r = divmod(k, rows_per_col)
        x0, y0 = W + 12 + c * colw, 80 + r * lh
        dc.text((x0, y0), i, font=F, fill=(150, 20, 10))
        dc.text((x0 + 70, y0), lab[:52] if name != "street" else lab[:72], font=FS, fill=(20, 20, 20))
    os.makedirs(SHEETS, exist_ok=True)
    dst = os.path.join(SHEETS, "sh1_map_%s.jpg" % name)
    canvas.save(dst, quality=88)
    print("map", dst, canvas.size, "labels", len(labels))


def main(MAPS):
    for name, (center, scale, res, dk, bcut) in MAPS.items():
        draw_map(name, center, scale, res)


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    import render_sh1
    _, MAPS = render_sh1.jobs()
    main(MAPS)
