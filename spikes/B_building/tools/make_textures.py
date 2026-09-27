#!/usr/bin/env python3
"""Make the kit's texture PNGs (co / nohq / smdi) in data/B/textures/ (git-ignored, regenerable).

Sources: CC0 Poly Haven maps in data/B/polyhaven (fetch_textures.py), recoloured for a Japanese palette, plus
procedural textures (shoji, fusuma, plank door, koshi lattice, mushiko window, tansu drawers, ash).
build_b.py converts these PNGs to PAA.   Usage:  python make_textures.py
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, ".."))
DEV = os.path.abspath(os.path.join(B, "..", ".."))
PH = os.path.join(DEV, "data", "B", "polyhaven")
OUT = os.path.join(DEV, "data", "B", "textures")      # generated, git-ignored
SIZE = 1024
RNG = np.random.default_rng(7)


def ph(asset, kind):
    return Image.open(os.path.join(PH, asset, "%s_%s_1k.jpg" % (asset, kind))).convert("RGB").resize((SIZE, SIZE),
                                                                                                    Image.LANCZOS)


def arr(im):
    return np.asarray(im).astype(np.float32) / 255.0


def img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def lum(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def save(name, co, nohq=None, smdi=None, spec=0.2, gloss=0.3, rough=None):
    co.save(os.path.join(OUT, name + "_co.png"))
    w, h = co.size
    if nohq is None:
        nohq = Image.new("RGB", (w, h), (128, 128, 255))
    nohq.save(os.path.join(OUT, name + "_nohq.png"))
    if smdi is None:
        if rough is not None:
            r = arr(rough)[..., 0]
            s = np.stack([np.ones_like(r), (1 - r) * spec, (1 - r) * gloss], -1)
            smdi = img(s)
        else:
            smdi = Image.new("RGB", (w, h), (255, int(spec * 255), int(gloss * 255)))
    smdi.save(os.path.join(OUT, name + "_smdi.png"))
    print("  ", name, co.size)


def noise(w, h, scale, amp):
    small = RNG.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
    n = np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32)
    return (n / 255.0 - 0.5) * amp


def from_polyhaven():
    # white plaster: lift white_plaster_02 to a warm white, keep 60 % of its variation
    a = arr(ph("white_plaster_02", "diff"))
    m = a.mean(axis=(0, 1))
    a = (0.86 + (a - m) * 0.6) * np.array([1.0, 0.985, 0.95])
    save("jp_plaster_white", img(a), ph("white_plaster_02", "nor_dx"), rough=ph("white_plaster_02", "rough"),
         spec=0.12, gloss=0.25)
    # earth plaster: clay_plaster, a touch lighter
    a = arr(ph("clay_plaster", "diff")) * 1.08
    save("jp_plaster_earth", img(a), ph("clay_plaster", "nor_dx"), rough=ph("clay_plaster", "rough"),
         spec=0.10, gloss=0.2)
    # dark timber: japanese cedar planks turned into dark stained (bengara/soot) timber
    a = arr(ph("japanese_cedar_planks", "diff"))
    l = lum(a)[..., None]
    a = (0.07 + l * 0.34) * np.array([1.0, 0.70, 0.50])
    save("jp_timber_dark", img(a), ph("japanese_cedar_planks", "nor_dx"), rough=ph("japanese_cedar_planks", "rough"),
         spec=0.35, gloss=0.45)
    # floor boards: hinoki, slightly aged
    a = arr(ph("hinoki_planks", "diff")) * np.array([0.86, 0.80, 0.72])
    save("jp_boards_floor", img(a), ph("hinoki_planks", "nor_dx"), rough=ph("hinoki_planks", "rough"),
         spec=0.35, gloss=0.5)
    # weathered exterior boards
    a = arr(ph("dark_planks", "diff")) * 0.9
    save("jp_boards_ext", img(a), ph("dark_planks", "nor_dx"), rough=ph("dark_planks", "rough"), spec=0.2, gloss=0.3)
    # kawara: grey roof tiles, moss desaturated
    a = arr(ph("grey_roof_tiles", "diff"))
    l = lum(a)[..., None]
    a = (l * 0.75 + a * 0.25) * np.array([0.92, 0.95, 1.0]) * 0.95
    save("jp_kawara", img(a), ph("grey_roof_tiles", "nor_dx"), rough=ph("grey_roof_tiles", "rough"),
         spec=0.45, gloss=0.55)
    # tatami as is
    save("jp_tatami", ph("tatami_mat", "diff"), ph("tatami_mat", "nor_dx"), rough=ph("tatami_mat", "rough"),
         spec=0.2, gloss=0.35)
    # doma: clay floor, a little darker
    a = arr(ph("clay_floor_001", "diff")) * 0.85
    save("jp_doma", img(a), ph("clay_floor_001", "nor_dx"), rough=ph("clay_floor_001", "rough"), spec=0.1, gloss=0.2)
    save("jp_stone", ph("japanese_stone_wall", "diff"), ph("japanese_stone_wall", "nor_dx"),
         rough=ph("japanese_stone_wall", "rough"), spec=0.25, gloss=0.35)


def procedural():
    W, H = 512, 1024
    timber = Image.open(os.path.join(OUT, "jp_timber_dark_co.png")).convert("RGB")
    hinoki = Image.open(os.path.join(OUT, "jp_boards_floor_co.png")).convert("RGB")
    boards = Image.open(os.path.join(OUT, "jp_boards_ext_co.png")).convert("RGB")

    # ---- shoji: paper, light wood frame, kumiko grid, wooden kick panel
    paper = np.ones((H, W, 3), np.float32) * np.array([0.93, 0.91, 0.85]) + noise(W, H, 8, 0.04)[..., None]
    im = img(paper)
    d = ImageDraw.Draw(im)
    wood = (150, 112, 72)
    kick = hinoki.resize((W, int(H * 0.2))).crop((0, 0, W, int(H * 0.18)))
    im.paste(kick, (0, H - kick.size[1]))
    fw = int(W * 0.06)
    d.rectangle([0, 0, fw, H], fill=wood)
    d.rectangle([W - fw, 0, W, H], fill=wood)
    d.rectangle([0, 0, W, int(H * 0.035)], fill=wood)
    d.rectangle([0, H - kick.size[1] - int(H * 0.03), W, H - kick.size[1]], fill=wood)
    y0, y1 = int(H * 0.035), H - kick.size[1] - int(H * 0.03)
    for k in range(1, 4):
        x = fw + k * (W - 2 * fw) // 4
        d.rectangle([x - 3, y0, x + 3, y1], fill=wood)
    for k in range(1, 8):
        y = y0 + k * (y1 - y0) // 8
        d.rectangle([fw, y - 3, W - fw, y + 3], fill=wood)
    save("jp_shoji", im, spec=0.05, gloss=0.2)

    # ---- fusuma: patterned paper, black lacquer frame, round pull
    base = np.ones((H, W, 3), np.float32) * np.array([0.84, 0.79, 0.64])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    waves = (np.sin(xx / 22.0 + np.sin(yy / 40.0) * 2.0) * np.sin(yy / 30.0)) * 0.035
    base += waves[..., None] * np.array([0.6, 0.55, 0.2]) + noise(W, H, 16, 0.05)[..., None]
    im = img(base)
    d = ImageDraw.Draw(im)
    blk = (22, 18, 16)
    fw = int(W * 0.035)
    d.rectangle([0, 0, fw, H], fill=blk)
    d.rectangle([W - fw, 0, W, H], fill=blk)
    d.rectangle([0, 0, W, fw], fill=blk)
    d.rectangle([0, H - fw, W, H], fill=blk)
    for cx in (int(W * 0.13), int(W * 0.87)):
        cy = int(H * 0.47)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(60, 45, 30))
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(15, 12, 10))
    save("jp_fusuma", im, spec=0.1, gloss=0.25)

    # ---- plank door (itado): vertical boards, three battens
    pl = boards.rotate(90, expand=True).resize((W, H))
    im = pl.copy()
    d = ImageDraw.Draw(im)
    t = timber.resize((W, 64))
    for fy in (0.06, 0.5, 0.92):
        y = int(H * fy)
        im.paste(t.crop((0, 0, W, 44)), (0, y - 22))
    fw = int(W * 0.05)
    im.paste(timber.rotate(90, expand=True).resize((fw, H)), (0, 0))
    im.paste(timber.rotate(90, expand=True).resize((fw, H)), (W - fw, 0))
    save("jp_plankdoor", im, spec=0.2, gloss=0.3)

    # ---- koshi lattice (resolution 2 panel): 16 slats per 0.9 m tile over paper
    S = 512
    tile = np.ones((S, S, 3), np.float32) * np.array([0.80, 0.78, 0.72])
    tim = arr(timber.resize((S, S)).rotate(90))
    pitch = S // 16
    for k in range(16):
        x0 = k * pitch
        x1 = x0 + int(pitch * 0.62)
        tile[:, x0:x1] = tim[:, x0:x1]
        tile[:, x1:min(S, x1 + 3)] *= 0.55          # shadow beside each slat
    save("jp_koshi", img(tile), spec=0.2, gloss=0.3)

    # ---- mushiko-mado: white plaster panel with vertical slots
    pl = Image.open(os.path.join(OUT, "jp_plaster_white_co.png")).convert("RGB").resize((S, S))
    d = ImageDraw.Draw(pl)
    n = 11
    for k in range(n):
        cx = int(S * (0.07 + 0.86 * (k + 0.5) / n))
        d.rounded_rectangle([cx - 9, int(S * 0.1), cx + 9, int(S * 0.9)], radius=9, fill=(24, 20, 18))
    save("jp_mushiko", pl, spec=0.1, gloss=0.2)

    # ---- tansu (stair cabinet) drawers: 4 x 4 per 1 m tile
    im = timber.resize((S, S))
    d = ImageDraw.Draw(im)
    for k in range(5):
        v = k * S // 4
        d.line([(0, v), (S, v)], fill=(12, 8, 6), width=5)
        d.line([(v, 0), (v, S)], fill=(12, 8, 6), width=5)
    for i in range(4):
        for j in range(4):
            cx, cy = i * S // 4 + S // 8, j * S // 4 + S // 8
            d.rectangle([cx - 20, cy - 6, cx + 20, cy + 6], fill=(30, 30, 32))
            d.rectangle([cx - 14, cy - 2, cx + 14, cy + 2], fill=(80, 80, 85))
    save("jp_tansu", im, spec=0.3, gloss=0.45)

    # ---- ash
    a = np.ones((256, 256, 3), np.float32) * 0.36 + noise(256, 256, 4, 0.2)[..., None] + noise(256, 256, 32, 0.1)[..., None]
    save("jp_ash", img(a), spec=0.02, gloss=0.1)


def main():
    os.makedirs(OUT, exist_ok=True)
    from_polyhaven()
    procedural()
    return 0


if __name__ == "__main__":
    sys.exit(main())
