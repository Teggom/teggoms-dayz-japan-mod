#!/usr/bin/env python3
r"""shots.py - F1 before / after renders and the sheet spikes/F1/f1_fixes.jpg.

  python shots.py before        renders the pre-F1 masters (spikes/F1/_before/<B3a|B3b|L1|L2>/...)
  python shots.py after         renders the current masters (spikes/<X>/out/...)
  python shots.py sheet         composes spikes/F1/f1_fixes.jpg (before | after per fix)
  python shots.py <tag> <fix>   one fix only (fix = the key in SHOTS)
Every render culls back faces (the game draws single-sided faces from their outward side only). The shop is at the
kitchen-scale stand-ins described per shot; nothing starts the server, the game or a GUI program.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import render_f1  # noqa: E402

WALL = (0.42, 0.38, 0.32)
KAMADO = (0.46, 0.40, 0.34)

# (fix key, title, [(label, [items], job extras)])  items: (area, rel p3d, extra item keys)
SHOTS = [
    ("1", "1 Noren: plain cloth at real scale (was a 0.03 v strip over 1.1 m)", [
        ("noren_long (front, eye height)", [("B3b", "street/jp_s_shopfront_noren_long.p3d", {})],
         {"cam": [0.35, 1.55, 1.9], "look": [0.0, 1.25, 0.1], "lens": 40,
          "boxes": [[-1.0, 1.0, 0.0, 2.6, -0.06, 0.0, WALL]]}),
        ("ab_noren_torn (_w2)", [("B3b", "street/jp_s_shopfront_ab_noren_torn.p3d", {})],
         {"cam": [-0.3, 1.5, 1.8], "look": [0.0, 1.35, 0.1], "lens": 40,
          "boxes": [[-1.0, 1.0, 0.0, 2.6, -0.06, 0.0, WALL]]}),
    ]),
    ("2", "2 Fire tub: see-through sliver where the fill meets the far stave wall", [
        ("fire_tub_open, from above at a player's angle", [("B3b", "water/jp_s_fire_tub_open.p3d", {})],
         {"cam": [0.15, 1.78, 0.95], "look": [0.0, 0.77, -0.45], "lens": 30}),
    ]),
    ("3", "3 Laundry pole: the kimono (was the noren strip stretched over 1.25 m, a funnel)", [
        ("load_cloth (front)", [("B3b", "yard/jp_s_laundry_pole_load_cloth.p3d", {})],
         {"cam": [0.2, 1.6, 4.0], "look": [-0.2, 1.3, 0.0], "lens": 35}),
        ("load_cloth: the pole through the sleeves (from above, end-on)",
         [("B3b", "yard/jp_s_laundry_pole_load_cloth.p3d", {})],
         {"cam": [0.55, 2.75, 1.25], "look": [-0.62, 1.85, 0.0], "lens": 40}),
    ]),
    ("4", "4 Laundry forks: the V opens across the pole, the pole sits in it", [
        ("forked, end-on along the pole", [("B3b", "yard/jp_s_laundry_pole_forked.p3d", {})],
         {"cam": [-2.6, 2.2, 0.35], "look": [-1.57, 2.05, 0.0], "lens": 60}),
        ("crossed, end-on", [("B3b", "yard/jp_s_laundry_pole_crossed.p3d", {})],
         {"cam": [-3.2, 1.9, 0.6], "look": [-1.57, 1.8, 0.0], "lens": 45}),
        ("ab_down (the pole's seat in the standing fork)", [("B3b", "yard/jp_s_laundry_pole_ab_down.p3d", {})],
         {"cam": [-2.4, 2.3, 1.2], "look": [-1.4, 1.9, 0.0], "lens": 45}),
    ]),
    ("5", "5 Kama lid: the seated pot's lid lay 0.63 m up in the air (stand-in kamado, pot as placed)", [
        ("kama_nolid on the kamado (+ lid prop on the doma after)",
         [("B3a", "kitchen/jp_f_kama_nolid.p3d", {"off": [0.0, 0.632, 0.0], "yaw": 90.0}),
          ("B3a", "kitchen/jp_f_kama_lid.p3d", {"off": [0.62, 0.05, 0.28], "yaw": 70.0, "optional": True})],
         {"cam": [1.55, 1.55, 0.7], "look": [0.2, 0.45, 0.0], "lens": 32, "ground_y": 0.05,
          "boxes": [[-0.35, 0.35, 0.05, 0.77, -1.35, 0.45, KAMADO], [-0.42, -0.35, 0.05, 2.2, -1.5, 1.0, WALL]]}),
    ]),
    ("6", "6 Kamidana: the miya's ridge parallel to the front (shinmei), not a gable to the viewer", [
        ("kamidana_plain + L1 shimenawa", [("B3a", "fittings/jp_f_kamidana_plain.p3d", {}),
                                          ("L1", "religious/jp_f_kamidana_set_shimenawa.p3d", {})],
         {"cam": [0.75, 1.65, 1.5], "look": [0.0, 2.2, 0.12], "lens": 40,
          "boxes": [[-1.0, 1.0, 0.0, 2.8, -0.06, 0.0, WALL]]}),
    ]),
    ("7", "7 Cloth over a rim: into the chest onto the cloth inside, tight to the front face", [
        ("nagamochi_open", [("B3a", "storage/jp_f_nagamochi_open.p3d", {})],
         {"cam": [0.05, 1.75, 0.42], "look": [0.28, 0.14, 0.22], "lens": 32}),
        ("tansu_ransacked", [("B3a", "storage/jp_f_tansu_ransacked.p3d", {})],
         {"cam": [0.05, 1.5, 1.05], "look": [-0.26, 0.62, 0.38], "lens": 40}),
        ("kori_open", [("B3a", "storage/jp_f_kori_open.p3d", {})],
         {"cam": [0.35, 0.95, 0.95], "look": [0.0, 0.18, 0.1], "lens": 40}),
    ]),
    ("8", "8 Goods stand: Roadway on the steps (green) over the Geometry (red)", [
        ("misedana_1ken", [("B3a", "shop/jp_f_misedana_1ken.p3d", {}),
                           ("B3a", "shop/jp_f_misedana_1ken.p3d", {"lod": "geo", "tint": "red"}),
                           ("B3a", "shop/jp_f_misedana_1ken.p3d", {"lod": "road", "tint": "green"})],
         {"cam": [1.4, 1.5, 1.7], "look": [0.0, 0.25, 0.0], "lens": 35}),
    ]),
]


def path(tag, area, rel):
    if tag == "before":
        return os.path.join(HERE, "_before", area, rel.replace("/", os.sep))
    return os.path.join(DEV, "spikes", area, "out", rel.replace("/", os.sep))


def jobs_for(tag, only=None):
    jobs = []
    for key, _, shots in SHOTS:
        if only and key not in only:
            continue
        for k, (label, items, extra) in enumerate(shots):
            its = []
            for area, rel, kw in items:
                p = path(tag, area, rel)
                if not os.path.isfile(p):
                    if kw.get("optional"):
                        continue
                    print("missing", p)
                    continue
                it = {"p3d": p}
                it.update({a: b for a, b in kw.items() if a != "optional"})
                its.append(it)
            j = {"out": "f1_%s_%d_%s" % (key, k, tag), "items": its, "cull": True}
            j.update(extra)
            jobs.append(j)
    return jobs


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    try:
        ft = ImageFont.truetype("arialbd.ttf", 22)
        f = ImageFont.truetype("arial.ttf", 17)
    except OSError:
        ft = f = ImageFont.load_default()
    TW, TH = 560, 420
    rows = []
    for key, title, shots in SHOTS:
        for k, (label, _, _) in enumerate(shots):
            rows.append((key, k, title if k == 0 else None, label))
    W = 2 * TW + 30
    RH = TH + 34
    extra = sum(30 for r in rows if r[2])
    im = Image.new("RGB", (W, 60 + len(rows) * RH + extra), (24, 24, 26))
    d = ImageDraw.Draw(im)
    d.text((10, 10), "F1 (G4 walk fixes): BEFORE (left) | AFTER (right). Written MLOD masters, back faces culled as "
           "the game draws them.", fill=(235, 235, 235), font=ft)
    y = 50
    for key, k, title, label in rows:
        if title:
            d.text((10, y + 4), title, fill=(250, 210, 120), font=ft)
            y += 30
        d.text((10, y + 4), label, fill=(200, 200, 200), font=f)
        for c, tag in enumerate(("before", "after")):
            p = os.path.join(HERE, "renders", "f1_%s_%d_%s.png" % (key, k, tag))
            if os.path.isfile(p):
                t = Image.open(p).convert("RGB")
                t.thumbnail((TW, TH))
                im.paste(t, (10 + c * (TW + 10), y + 28))
            else:
                d.text((10 + c * (TW + 10), y + 60), "(no %s render)" % tag, fill=(150, 150, 150), font=f)
        y += RH
    out = os.path.join(HERE, "f1_fixes.jpg")
    im.save(out, quality=86)
    print("sheet", out, im.size)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "sheet":
        sheet()
    else:
        tag = a[0] if a else "after"
        render_f1.run(jobs_for(tag, set(a[1:]) or None), os.path.join(HERE, "_build", "jobs_%s.json" % tag))
