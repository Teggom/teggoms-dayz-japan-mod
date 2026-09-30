#!/usr/bin/env python3
"""Renders (Blender, background) of the built MLODs in out/ + the contact sheet renders/tansu_contact_sheet.png.

  python render.py [--no-render] [--only NAME,NAME]

Row 1 intact: front (ortho), 3/4 with a 1.8 m figure, back 3/4, close-up of the fittings.
Row 2 ransacked: front (ortho), 3/4, 3/4 from the other side, close-up into the drawers.
Row 3 LODs: Resolution 2 and 3 of both states (same view as the 3/4 cells).
Row 4 ransacked collision (Geometry red, View Geometry blue over a ghost of Resolution 1), top view with the loot
points (green) and the front zone (yellow), and the two reference photos (crops) the model follows.
"""
import json
import os
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tansu  # noqa: E402

BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(HERE, "out")
RDIR = os.path.join(HERE, "renders")
SHEET = os.path.join(RDIR, "tansu_contact_sheet.png")
CELL = (600, 480)
FONT, FONTB = r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf"
A = os.path.join(OUT, "jp_f_tansu.p3d")
B = os.path.join(OUT, "jp_f_tansu_ransacked.p3d")


def jobs():
    _, meta = tansu.build("ransacked")
    pts = [p for s in tansu.loot_surfaces("ransacked", meta) for p in s["points"]]
    fz = tansu.front_zone("ransacked", meta)
    v34 = {"az": 38, "el": 22, "dist": 3.0, "lens": 45}
    b34 = {"az": 36, "el": 27, "dist": 3.3, "lens": 45}
    return [
        # row 1: intact
        {"out": "A_front", "p3d": A, "lod": 1, "view": {"az": 0, "el": 5, "dist": 8, "ortho": 1.32}, "target": [0, 0.5, 0],
         "cap": "Intact, front (ortho): two boxes, 4 drawers, 2 ring pulls + an oval lock plate each, joint clasp"},
        {"out": "A_34", "p3d": A, "lod": 1, "view": {"az": 36, "el": 18, "dist": 4.1, "lens": 45},
         "target": [-0.28, 0.85, 0.0], "human": [-1.15, -0.05],
         "cap": "Intact 3/4 beside a 1.8 m figure: 1.00 x 0.45 x 1.00 m; dusty street_dark wood (_w2), iron _w1"},
        {"out": "A_back", "p3d": A, "lod": 1, "view": {"az": 212, "el": 22, "dist": 3.0, "lens": 45},
         "target": [0, 0.5, 0], "cap": "Intact, back 3/4: back boards, corner caps on all 16 corners, side handles"},
        {"out": "A_close", "p3d": A, "lod": 1, "view": {"az": 34, "el": 12, "dist": 0.95, "lens": 50, "sun_off": 55},
         "target": [0.30, 0.84, 0.13],
         "cap": "Close-up: ring pull (kan) on its plate, lock plate + keyhole, corner cap, bail handle on the side"},
        # row 2: ransacked
        {"out": "B_front", "p3d": B, "lod": 1, "view": {"az": 0, "el": 5, "dist": 8, "ortho": 1.40},
         "target": [0.03, 0.5, 0.2], "cap": "Ransacked, front (ortho): 3 drawers pulled out, the 4th on the floor"},
        {"out": "B_34", "p3d": B, "lod": 1, "view": b34, "target": [0.0, 0.42, 0.28],
         "cap": "Ransacked 3/4: the empty slot is dark (sooted faces stand in for shadow), drawer boxes raw wood"},
        {"out": "B_34r", "p3d": B, "lod": 1, "view": {"az": -40, "el": 27, "dist": 3.3, "lens": 45},
         "target": [0.0, 0.42, 0.28], "cap": "Ransacked, other side: the dropped drawer lies askew in the front zone"},
        {"out": "B_close", "p3d": B, "lod": 1, "view": {"az": 18, "el": 40, "dist": 1.45, "lens": 45, "sun_off": 25},
         "target": [0.0, 0.5, 0.33], "cap": "Close-up into the pulled drawers and the empty slot; loot lies in the "
                                            "dropped drawer"},
        # row 3: LODs
        {"out": "A_res2", "p3d": A, "lod": 2, "view": v34, "target": [0, 0.5, 0],
         "cap": "Intact, Resolution 2: fittings as blocks, front corner caps only"},
        {"out": "A_res3", "p3d": A, "lod": 3, "view": v34, "target": [0, 0.5, 0],
         "cap": "Intact, Resolution 3: two blocks + four drawer fronts"},
        {"out": "B_res2", "p3d": B, "lod": 2, "view": b34, "target": [0.0, 0.42, 0.28],
         "cap": "Ransacked, Resolution 2"},
        {"out": "B_res3", "p3d": B, "lod": 3, "view": b34, "target": [0.0, 0.42, 0.28],
         "cap": "Ransacked, Resolution 3: blocks, the dark slot and the hollow floor drawer kept"},
        # row 4
        {"out": "B_coll", "p3d": B, "lod": 1, "ghost": True, "overlay": ["geo", "view"], "view": b34,
         "target": [0.0, 0.42, 0.28], "cap": "Ransacked collision: Geometry (red, 10 convex parts, the floor drawer "
                                             "hollow) and View/Fire (blue, 6)"},
        {"out": "B_top", "p3d": B, "lod": 1, "view": {"az": 0, "el": 89.5, "dist": 6, "ortho": 1.75, "sun_off": 30},
         "target": [0.05, 0.5, 0.33], "markers": pts, "zone": [fz["x"][0], fz["x"][1], fz["z"][0], fz["z"][1]],
         "cap": "Top view: loot points (green: 2 on the top, 1 in the dropped drawer) and the front zone (yellow)"},
    ]


REFS = [("refs_crop/i07_tansu.png", "Ref i07: Fukagawa Edo Museum tenement tansu (Tenpo-era reconstruction). "
         "Photo DryPot, CC BY 2.5, Wikimedia Commons"),
        ("refs_crop/i01_chest_right.png", "Ref i01: surviving tansu, former Kasuya house (Edo farmhouse). "
         "Photo Asanagi, CC0, Wikimedia Commons")]


def run_blender(js):
    jf = os.path.join(RDIR, "jobs.json")
    os.makedirs(RDIR, exist_ok=True)
    spec = {"out_dir": RDIR, "res": list(CELL), "jobs": js,
            "save_blend": {"path": os.path.join(HERE, "tansu_preview.blend"), "models": [[A, 0.0], [B, 1.6]]}}
    with open(jf, "wb") as f:
        f.write(json.dumps(spec, indent=1).encode("utf-8"))
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.join(HERE, "render_blend.py"),
                        "--", jf], capture_output=True, text=True, errors="replace")
    with open(os.path.join(RDIR, "blender.log"), "wb") as f:
        f.write((r.stdout + "\n" + r.stderr).encode("utf-8", "replace"))
    done = sum(os.path.isfile(os.path.join(RDIR, j["out"] + ".png")) for j in js)
    print("blender: %d/%d rendered (rc %d, log renders/blender.log)" % (done, len(js), r.returncode))
    if done < len(js):
        print((r.stdout + r.stderr)[-2500:])


def fit(im, size):
    w, h = im.size
    s = min(size[0] / w, size[1] / h)
    im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    bg = Image.new("RGB", size, (30, 30, 32))
    bg.paste(im, ((size[0] - im.size[0]) // 2, (size[1] - im.size[1]) // 2))
    return bg


def compose(js, faces=None):
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (FONTB, 30), "s": (FONT, 16), "b": (FONTB, 16),
                                                        "t": (FONT, 15)}.items()}
    cells = [(os.path.join(RDIR, j["out"] + ".png"), j["out"], j["cap"]) for j in js]
    cells += [(os.path.join(HERE, p), os.path.basename(p)[:-4], cap) for p, cap in REFS]
    cols, cap_h = 4, 58
    rows = (len(cells) + cols - 1) // cols
    W = cols * CELL[0] + (cols + 1) * 10
    H = 110 + rows * (CELL[1] + cap_h + 10) + 10
    im = Image.new("RGB", (W, H), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((14, 12), "jp_f_tansu (BUILD_LIST row 26) - effort test, level max - intact and ransacked", font=F["h1"],
           fill=(20, 20, 20))
    fl = ""
    if faces:
        fl = "Faces: " + "; ".join("%s R1 %d / R2 %d / R3 %d, Geo %d" % (s, f["Resolution 1"], f["Resolution 2"],
                                                                        f["Resolution 3"], f["Geometry"])
                                   for s, f in faces.items()) + ".  "
    d.text((14, 52), fl + "Blender renders of the MLOD read back from disk, library textures (PNG twins of the .paa) "
                          "with their normal maps; Standard view transform.", font=F["s"], fill=(60, 60, 60))
    d.text((14, 76), "Materials: body jp_m_wood_street_dark_w2 (stand-in for jp_m_wood_interior), drawer boxes "
                     "jp_m_wood_weathered_w2, cavity faces jp_m_wood_sooted_w0, fittings jp_m_metal_iron_w1.",
           font=F["s"], fill=(60, 60, 60))
    for i, (p, name, cap) in enumerate(cells):
        x = 10 + (i % cols) * (CELL[0] + 10)
        y = 110 + (i // cols) * (CELL[1] + cap_h + 10)
        if os.path.isfile(p):
            im.paste(fit(Image.open(p).convert("RGB"), CELL), (x, y))
        d.rectangle([x, y + CELL[1], x + CELL[0], y + CELL[1] + cap_h], fill=(250, 249, 246))
        d.text((x + 6, y + CELL[1] + 3), name, font=F["b"], fill=(20, 20, 20))
        yy = y + CELL[1] + 21
        for line in textwrap.wrap(cap, 78)[:2]:
            d.text((x + 6, yy), line, font=F["t"], fill=(50, 50, 50))
            yy += 17
    im.save(SHEET)
    print("sheet", SHEET, im.size)


def main(argv):
    js = jobs()
    if "--only" in argv:
        want = set(argv[argv.index("--only") + 1].split(","))
        js_r = [j for j in js if j["out"] in want]
    else:
        js_r = js
    if "--no-render" not in argv:
        run_blender(js_r)
    faces = None
    cj = os.path.join(HERE, "checks.json")
    if os.path.isfile(cj):
        faces = {s: v["faces"] for s, v in json.load(open(cj, encoding="utf-8"))["states"].items()}
    compose(js, faces)


if __name__ == "__main__":
    main(sys.argv[1:])
