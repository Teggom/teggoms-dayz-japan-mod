#!/usr/bin/env python3
r"""textcheck.py - L2 step 0: is B3b's text mirrored in game?

  python textcheck.py <tag>        renders front close-ups of B3b's text-bearing masters (spikes/B3b/out) through
                                   render_l2.py (DayZ (x,y,z) -> Blender (x,z,y), the in-game handedness) and composes
                                   research/outdoor_kit/contact_sheets/l2_textcheck_<tag>.jpg: each render beside the
                                   atlas cell as drawn (how the text must read)
Never starts or stops the server, the game or any GUI program.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
B3B_OUT = os.path.join(DEV, "spikes", "B3b", "out")
TEX = os.path.join(DEV, "data", "materials", "textures")
SHEETS = os.path.join(DEV, "research", "outdoor_kit", "contact_sheets")
MAT = os.path.join(DEV, "src", "JP", "common", "materials")

# (label, p3d under spikes/B3b/out, view (x, front, up) in model terms, atlas family/material, cell)
CASES = [
    ("kanban_stand", "street/jp_s_shopfront_kanban_stand.p3d", (0.0, 1.0, 0.12), "paint/jp_m_decal_sumi_text",
     "kanban_osobakiri"),
    ("kanban_hang", "street/jp_s_shopfront_kanban_hang.p3d", (0.0, 1.0, 0.05), "paint/jp_m_decal_sumi_text",
     "kanban_okashidokoro"),
    ("chochin_shop", "street/jp_s_lantern_sign_chochin_shop.p3d", (0.0, 1.0, 0.05), "paint/jp_m_decal_sumi_text",
     None),
    ("fire_tub", "water/jp_s_fire_tub_rural.p3d", (0.0, 1.0, 0.2), "paint/jp_m_decal_sumi_text", "oke_yosui"),
    ("fire_tub_full", "water/jp_s_fire_tub_full.p3d", (0.0, 1.0, 0.15), "paint/jp_m_decal_sumi_text", "oke_yosui"),
    ("kosatsu", "roadside/jp_s_kosatsu_std.p3d", (0.0, 1.0, 0.1), "paint/jp_m_decal_sumi_text", "kosatsu_chuko_1711"),
    ("stele_pillar", "roadside/jp_s_stele_pillar.p3d", (0.0, 1.0, 0.1), "stone/jp_m_decal_carved_text", None),
    ("stele_michi", "roadside/jp_s_stele_natural_slab.p3d", (0.0, 1.0, 0.1), "stone/jp_m_decal_carved_text", None),
]


def cell_img(fam_mat, cellname):
    from PIL import Image
    sc = json.load(open(os.path.join(MAT, fam_mat + ".json"), encoding="utf-8"))
    u0, v0, u1, v1 = sc["cells"][cellname]["uv"]
    im = Image.open(os.path.join(TEX, os.path.basename(fam_mat) + "_w0_ca.png")).convert("RGBA")
    W, H = im.size
    c = im.crop((int(u0 * W), int(v0 * H), int(u1 * W), int(v1 * H)))
    bg = Image.new("RGBA", c.size, (200, 190, 170, 255))
    bg.alpha_composite(c)
    return bg.convert("RGB")


def main(tag, only=None):
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
    from jpparts import mlod
    cases = [c for c in CASES if not only or c[0] in only]
    jobs = []
    for label, rel, view, _, cell in cases:
        p = os.path.join(B3B_OUT, rel.replace("/", os.sep))
        jobs.append({"out": "textcheck_%s_%s" % (label, tag), "items": [{"p3d": p, "off": [0.0, 0.0], "lod": 1.0}],
                     "view": list(view), "lens": 50, "cull": True})
    jp = os.path.join(HERE, "_build", "textcheck_jobs.json")
    os.makedirs(os.path.dirname(jp), exist_ok=True)
    with open(jp, "wb") as f:
        f.write(json.dumps(jobs, indent=1).encode("utf-8"))
    r = subprocess.run([sys.executable, os.path.join(HERE, "render_l2.py"), "--run"], env=dict(os.environ, L2_JOBS=jp),
                       capture_output=True, text=True, errors="replace")
    print(r.stdout.strip()[-600:])
    try:
        f = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        f = ImageFont.load_default()
    rows = []
    for label, rel, view, fam, cell in cases:
        ren = os.path.join(HERE, "renders", "textcheck_%s_%s.png" % (label, tag))
        im = Image.open(ren).convert("RGB")
        im.thumbnail((800, 450))
        row = Image.new("RGB", (1100, 480), (24, 24, 26))
        row.paste(im, (10, 20))
        d = ImageDraw.Draw(row)
        d.text((10, 0), "%s  (%s), seen from the front as the game shows it (left-handed axes, back faces culled)" % (label, rel), fill=(230, 230, 230), font=f)
        if cell:
            c = cell_img(fam, cell)
            c.thumbnail((270, 440))
            row.paste(c, (820, 30))
            d.text((820, 8), "atlas cell as drawn: " + cell, fill=(230, 230, 230), font=f)
        rows.append(row)
    sheet = Image.new("RGB", (1100, 480 * len(rows)), (24, 24, 26))
    for i, row in enumerate(rows):
        sheet.paste(row, (0, 480 * i))
    os.makedirs(SHEETS, exist_ok=True)
    out = os.path.join(SHEETS, "l2_textcheck_%s.jpg" % tag)
    sheet.save(out, quality=88)
    print("sheet", out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else "before", set(args[1:]) or None)
