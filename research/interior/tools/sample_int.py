"""Sample palette candidates from the interior reference photos, with the playbook method (PLAYBOOK §8): the median
of the pixels in a box, after dropping the darkest 15 % and brightest 15 % by luminance ("mid 70 % luminance").
Boxes are fractions [x0, y0, x1, y1] of the image. Prints sRGB per box and the mean of the boxes per candidate.

Run: python research/interior/tools/sample_int.py      Research agent PA2, 2026-09-29.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
REFS = os.path.join(ROOT, "data", "research_int", "refs")

SAMPLES = {
    "doma_earth": [("i02_kasuya_kamado", [0.62, 0.72, 0.95, 0.95]), ("i06_tsunashima_doma", [0.05, 0.72, 0.40, 0.95])],
    "floor_board_polished": [("i01_kasuya_irori", [0.05, 0.80, 0.25, 0.98])],
    "tatami_check": [("i03_tenmyo_irori", [0.05, 0.28, 0.35, 0.40])],
    "kamado_clay": [("i02_kasuya_kamado", [0.40, 0.30, 0.70, 0.50])],
    "stoneware_brown": [("i50_met_tokkuri_stoneware", [0.35, 0.40, 0.65, 0.70])],
}


def sample(ref, box):
    im = np.asarray(Image.open(os.path.join(REFS, ref + ".jpg")).convert("RGB")).astype(float)
    h, w, _ = im.shape
    x0, y0, x1, y1 = box
    px = im[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)].reshape(-1, 3)
    lum = px @ np.array([0.2126, 0.7152, 0.0722])
    lo, hi = np.percentile(lum, [15, 85])
    sel = px[(lum >= lo) & (lum <= hi)]
    return [int(round(v)) for v in np.median(sel, axis=0)]


def run():
    out = {}
    for k, boxes in SAMPLES.items():
        vals = []
        for ref, box in boxes:
            v = sample(ref, box)
            vals.append({"ref": ref, "box": box, "select": "mid 70 % luminance", "value": v})
        mean = [int(round(sum(s["value"][i] for s in vals) / len(vals))) for i in range(3)]
        out[k] = {"samples": vals, "srgb": mean}
    return out


if __name__ == "__main__":
    for k, v in run().items():
        print(k, v["srgb"], [(s["ref"], s["value"]) for s in v["samples"]])
