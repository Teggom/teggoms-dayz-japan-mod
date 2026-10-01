"""M1: sample reference photos for the new palette entries, the playbook way (playbook/tools/sample_palette.py):
per box, drop the darkest / brightest 15 % by luminance (or keep a band: 'dark' 10-45, 'light' 55-90, 'top' 75-95),
take the median; the entry value is the mean of the per-box medians (each box weighs the same); spread = 75th pct
CIE76 dE of the kept pixels from that value.

  python sample.py            prints every entry, writes look/boxes_<id>.jpg (boxes drawn) and crops/<id>_<n>.png
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
REF = {
    "c": "data/playbook/refs", "k": "data/research_okit/refs", "i": "data/research_int/refs",
    "x": "data/research_ext/refs",
}


def ref_path(rid):
    if rid.startswith("ph:"):
        a = rid[3:]
        return os.path.join(DEV, "data", "materials", "polyhaven", a, a + "_diff_1k.jpg")
    return os.path.join(DEV, REF[rid[0]], rid + ".jpg")


def srgb_to_lab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def keep(px, select):
    lum = px @ np.array([0.2126, 0.7152, 0.0722])
    band = {"dark": (10, 45), "light": (55, 90), "top": (75, 95)}.get(select, (15, 85))
    lo, hi = np.percentile(lum, band)
    return px[(lum >= lo) & (lum <= hi)]


def crop(rid, box):
    im = Image.open(ref_path(rid)).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = box  # noqa
    return im.crop((int(x0 * w), int(y0 * h), max(int(x1 * w), int(x0 * w) + 2), max(int(y1 * h), int(y0 * h) + 2)))


def wb_gain(wb):
    """Grey-card white balance: (ref id, box, target sRGB). Per-channel gains that give the reference patch the
    target's chromaticity (r:g:b ratios) at its own luminance (so exposure is untouched)."""
    rid, box, tgt = wb
    m = np.median(keep(np.asarray(crop(rid, box), dtype=np.float64).reshape(-1, 3), None), axis=0)
    t = np.asarray(tgt, dtype=np.float64)
    g = (t / t.sum()) / (m / m.sum())
    lw = np.array([0.2126, 0.7152, 0.0722])
    return g * (m @ lw) / ((m * g) @ lw), [int(round(v)) for v in m]


def sample(boxes):
    """boxes: [(ref id, [x0, y0, x1, y1] fractions, select or None[, wb])] -> (srgb, spread, per-box values, crops,
    wb notes). wb = (ref id, box, target sRGB): a grey card in the same light (see wb_gain)."""
    pooled, meds, crops, notes = [], [], [], []
    for b in boxes:
        rid, box, sel = b[:3]
        c = crop(rid, box)
        crops.append(c)
        px = keep(np.asarray(c, dtype=np.float64).reshape(-1, 3), sel)
        if len(b) > 3 and b[3]:
            g, m = wb_gain(b[3])
            notes.append({"box": box, "ref_patch_raw": m, "target": list(b[3][2]),
                          "raw_median": [int(round(v)) for v in np.median(px, axis=0)],
                          "gains": [round(float(v), 3) for v in g]})
            px = np.clip(px * g, 0, 255)
        pooled.append(px)
        meds.append(np.median(px, axis=0))
    med = np.mean(meds, axis=0)
    de = np.linalg.norm(srgb_to_lab(np.concatenate(pooled)) - srgb_to_lab(med), axis=1)
    return ([int(round(v)) for v in med], float(np.percentile(de, 75)),
            [[int(round(v)) for v in m] for m in meds], crops, notes)


# ---------------------------------------------------------------------------------------------- the M1 sample boxes
# Kept boxes only; rejected candidates are listed in M1_PROGRESS.md with the reason.
ASH_I04 = ("i04_tsunashima_irori", [0.20, 0.24, 0.36, 0.40], (150, 146, 140))   # ash bed -> palette ash_grey
SHIKKUI_X01 = ("x01_ioka_a", [0.45, 0.17, 0.70, 0.27], (192, 194, 196))          # gable plaster -> shikkui_white
SAMPLES = {
    # 1. bare earth: Kanto loam topsoil at a roadside Koshin site (k41, Matsudo; sunlit) and brown forest soil under a
    #    shrine's sacred tree (k37, Shikaumi shrine; diffuse forest light). Deep-shade boxes rejected (B1's doma rule).
    "earth_bare": [
        ("k41_koshin_sendabori", [0.03, 0.83, 0.33, 0.97], None),     # sunlit bare soil, front left
        ("k37_shimenawa_tree", [0.40, 0.66, 0.62, 0.78], None),       # forest soil between the post and the stones
        ("k37_shimenawa_tree", [0.20, 0.56, 0.38, 0.64], None),       # forest soil left of the post, some litter
        ("k27_hida_torii", [0.44, 0.84, 0.63, 0.96], None),           # worn earth path under a Hida village torii
    ],
    # 2. pale new wood: freshly split conifer kindling by the Tsunashima irori (i04), the lit faces; white-balanced on
    #    the ash bed in the same light (B1 found i04 under a cool daylight cast)
    "wood_new": [
        ("i04_tsunashima_irori", [0.683, 0.283, 0.717, 0.367], None, ASH_I04),
        ("i04_tsunashima_irori", [0.764, 0.317, 0.791, 0.400], None, ASH_I04),
        ("i04_tsunashima_irori", [0.480, 0.342, 0.502, 0.392], None, ASH_I04),
    ],
    # 3. silver-grey weathered wood: an old storehouse gable of unpainted boards (x01, Ioka house, evening shade,
    #    white-balanced on the shikkui plaster above them) and an old unpainted handcart in sun (k31, Uzumasa)
    "wood_silver": [
        ("k31_daihachi_uzumasa", [0.18, 0.60, 0.42, 0.68], None),
        ("c03_tsumago_street", [0.900, 0.36, 0.917, 0.53], None),     # sunlit gate post, Tsumago
        ("c03_tsumago_street", [0.926, 0.43, 0.967, 0.53], None),     # sunlit board gate leaf
    ],
    # 8b. split firewood (i22): split faces + grey bark + end grain, the whole stacked mix
    "firewood_split": [
        ("i22_kamado_firewood", [0.70, 0.10, 0.92, 0.32], None),
        ("i22_kamado_firewood", [0.62, 0.35, 0.80, 0.52], None),
        ("i22_kamado_firewood", [0.60, 0.12, 0.67, 0.33], None),     # the big round log on the left: bark
    ],
    # 8c. firewood end grain (i22): six cut log ends, small boxes inside each end face
    "firewood_end": [("i22_kamado_firewood", b, None) for b in (
        [0.6813, 0.1393, 0.6937, 0.1581], [0.7984, 0.2488, 0.8109, 0.2676], [0.8792, 0.2817, 0.8917, 0.3005],
        [0.8375, 0.4014, 0.85, 0.4202], [0.9198, 0.2175, 0.9323, 0.2363], [0.676, 0.3388, 0.6885, 0.3576])],
    # 8a. wicker (no kori photo on this machine): the CC0 Poly Haven scan bamboo_wall (aged, dried bamboo), whole map
    "wicker_aged": [("ph:bamboo_wall", [0.0, 0.0, 1.0, 1.0], None)],
}


def boxes_img(eid, boxes):
    by = {}
    for b in boxes:
        by.setdefault(b[0], []).append(b[1])
        if len(b) > 3 and b[3]:
            by.setdefault(b[3][0], []).append(b[3][1])
    for rid, bl in by.items():
        im = Image.open(ref_path(rid)).convert("RGB")
        w, h = im.size
        d = ImageDraw.Draw(im)
        for b in bl:
            d.rectangle([b[0] * w, b[1] * h, b[2] * w, b[3] * h], outline=(255, 0, 255), width=max(2, w // 300))
        sc = 900 / max(w, h)
        im.resize((int(w * sc), int(h * sc))).save(os.path.join(HERE, "look", "boxes_%s_%s.jpg" % (eid, rid.replace(":", "_"))))


def main(argv):
    only = argv[0] if argv else None
    out = {}
    os.makedirs(os.path.join(HERE, "crops"), exist_ok=True)
    for eid, boxes in SAMPLES.items():
        if only and eid != only:
            continue
        rgb, spread, meds, crops, notes = sample(boxes)
        boxes_img(eid, boxes)
        for n, c in enumerate(crops):
            c.save(os.path.join(HERE, "crops", "%s_%d.png" % (eid, n)))
        lab = srgb_to_lab(rgb)
        out[eid] = {"srgb": rgb, "spread": round(spread, 1), "per_box": meds,
                    "lab": [round(float(v), 1) for v in lab]}
        if notes:
            out[eid]["white_balance"] = notes
        print("%-16s %s  spread %.1f  Lab %s  boxes %s" % (eid, rgb, spread, out[eid]["lab"], meds))
    with open(os.path.join(HERE, "samples.json"), "wb") as f:
        f.write(json.dumps({"samples": out, "boxes": SAMPLES}, indent=1).encode("utf-8"))


if __name__ == "__main__":
    main(sys.argv[1:])
