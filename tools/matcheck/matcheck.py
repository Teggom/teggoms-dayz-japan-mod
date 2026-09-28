#!/usr/bin/env python3
r"""matcheck - playbook check C1 (palette): is each _co texture's mean colour inside its palette entry's tolerance?

  python matcheck.py PATH [PATH ...] [--id PALETTE_ID] [--masks DIR] [--palette palette.json] [--json OUT]

PATH is a _co texture (.png .jpg .tga .paa) or a folder (every *_co.* inside, recursively). .paa files are converted
with ImageToPAA to a temp PNG first, so the shipped file itself is measured.

Which palette entry (PLAYBOOK §8, §9):
  --id wins. Otherwise the material sidecar next to the texture: jp_m_<name>_w1_co.paa -> jp_m_<name>.json with
  "palette_id" and optionally "palette_by_wear": {"_w0": "thatch_new"} for a wear level that is a different colour.

What is measured:
  mean     arithmetic mean sRGB over the material area. Painted-on dirt/detail is excluded when a mask exists:
           <stem>_mask.png (white = excluded) next to the texture or in --masks DIR (§8: "painted-on dirt and
           detail masks are excluded from that mean").
  dE       CIE76 in CIELAB (D65), same maths as playbook/tools/sample_palette.py. Weathering allowance (§8): when the
           entry has weathering.worst + max_mix, the target is the nearest point on the line from the entry to
           mix(entry, worst, max_mix); otherwise the entry itself.
  spread   the palette's own definition: 75th percentile dE of the mid-70 % luminance pixels from their median.
Verdicts: FAIL = dE > tolerance_dE76 (exit code 1). WARN (exit 0) = mask excludes > 40 %, the mean is brighter than
205 (vanilla white walls average ~150, §8), or the spread is < 1.5 (flat) or > 2.5 x the entry's observed spread.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
PALETTE = os.path.join(DEV, "playbook", "palette.json")
IMAGE_TO_PAA = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\ImageToPAA\ImageToPAA.exe"
EXTS = (".png", ".jpg", ".jpeg", ".tga", ".paa")


def srgb_to_lab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def load_palette(path=PALETTE):
    return {e["id"]: e for e in json.load(open(path, encoding="utf-8"))["entries"]}


def targets(pal, pid):
    """sRGB points along the allowed line: the entry, then toward weathering.worst up to max_mix."""
    e = pal[pid]
    a = np.array(e["srgb"], float)
    w = e.get("weathering") or {}
    if w.get("worst") in pal and w.get("max_mix"):
        b = np.array(pal[w["worst"]]["srgb"], float)
        return [a + (b - a) * w["max_mix"] * t for t in np.linspace(0, 1, 41)]
    return [a]


def read_rgb(path):
    if path.lower().endswith(".paa"):
        tmp = os.path.join(tempfile.gettempdir(), "matcheck_%d.png" % os.getpid())
        r = subprocess.run([IMAGE_TO_PAA, path, tmp], capture_output=True, text=True, errors="replace")
        if r.returncode != 0 or not os.path.isfile(tmp):
            raise RuntimeError("ImageToPAA could not read %s: %s" % (path, (r.stdout + r.stderr).strip()))
        im = Image.open(tmp).convert("RGB")
        im.load()
        os.remove(tmp)
        return np.asarray(im)
    return np.asarray(Image.open(path).convert("RGB"))


def stem_of(path):
    b = os.path.basename(path)
    return re.sub(r"_co\.[a-z]+$", "", b, flags=re.I)


def find_sidecar(path):
    s = stem_of(path)
    m = re.match(r"(.+?)(_w\d)$", s)
    base, wear = (m.group(1), m.group(2)) if m else (s, "")
    sc = os.path.join(os.path.dirname(path), base + ".json")
    return (json.load(open(sc, encoding="utf-8")) if os.path.isfile(sc) else None), wear


def find_mask(path, mask_dir):
    s = stem_of(path) + "_mask.png"
    for d in ([mask_dir] if mask_dir else []) + [os.path.dirname(path)]:
        p = os.path.join(d, s)
        if os.path.isfile(p):
            return p
    return None


def check(path, pal, pid=None, mask_dir=None):
    wear = ""
    if pid is None:
        sc, wear = find_sidecar(path)
        if sc is None:
            return {"file": path, "verdict": "FAIL", "why": "no --id and no sidecar json"}
        pid = (sc.get("palette_by_wear") or {}).get(wear) or sc["palette_id"]
    if pid not in pal:
        return {"file": path, "palette_id": pid, "verdict": "FAIL", "why": "palette id not in palette.json"}
    e = pal[pid]
    img = read_rgb(path)
    h, w = img.shape[:2]
    px = img.reshape(-1, 3).astype(np.float64)
    mpath = find_mask(path, mask_dir)
    keep = np.ones(len(px), bool)
    if mpath:
        mk = Image.open(mpath).convert("L").resize((w, h), Image.NEAREST)
        keep = np.asarray(mk).reshape(-1) < 128
    base = px[keep] if keep.any() else px
    mean = base.mean(0)
    lab_mean = srgb_to_lab(mean)
    des = [float(np.linalg.norm(lab_mean - srgb_to_lab(t))) for t in targets(pal, pid)]
    de = min(des)
    de_entry = des[0]
    # spread, palette definition (sample_palette.py): p75 dE of mid-70 % luminance pixels from their median
    sub = base[:: max(1, len(base) // 200000)]
    lum = sub @ np.array([0.2126, 0.7152, 0.0722])
    lo, hi = np.percentile(lum, [15, 85])
    mid = sub[(lum >= lo) & (lum <= hi)]
    med = np.median(mid, axis=0)
    spread = float(np.percentile(np.linalg.norm(srgb_to_lab(mid) - srgb_to_lab(med), axis=1), 75))
    tol = float(e["tolerance_dE76"])
    obs = e.get("observed_spread_dE76")
    warns = []
    frac = 1.0 - float(keep.mean())
    if frac > 0.40:
        warns.append("mask excludes %.0f %%" % (frac * 100))
    if mean.max() > 205:
        warns.append("mean %.0f brighter than 205 (vanilla white ~150)" % mean.max())
    if spread < 1.5:
        warns.append("flat (spread %.1f)" % spread)
    elif spread > 2.5 * max(obs or tol, tol):
        warns.append("busy (spread %.1f vs %s)" % (spread, obs or tol))
    verdict = "FAIL" if de > tol else ("WARN" if warns else "PASS")
    return {"file": path, "palette_id": pid, "wear": wear, "mean_srgb": [round(float(v), 1) for v in mean],
            "target_srgb": e["srgb"], "dE": round(de, 2), "dE_to_entry": round(de_entry, 2), "tol": tol,
            "spread_p75": round(spread, 1), "observed_spread": obs, "masked_frac": round(frac, 3),
            "mask": mpath, "verdict": verdict, "warnings": warns}


def collect(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True)):
                if f.lower().endswith(EXTS) and re.search(r"_co\.[a-z]+$", f, re.I):
                    out.append(f)
        else:
            out.append(p)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--id", help="palette id for every file (else the sidecar decides)")
    ap.add_argument("--masks", help="folder holding <stem>_mask.png detail masks")
    ap.add_argument("--palette", default=PALETTE)
    ap.add_argument("--json", help="write all results to this file")
    a = ap.parse_args(argv)
    pal = load_palette(a.palette)
    res = [check(f, pal, a.id, a.masks) for f in collect(a.paths)]
    for r in res:
        if "mean_srgb" in r:
            print("%-4s %-34s %-18s mean %-17s dE %5.1f/%-4g spread %4.1f (obs %s) mask %3.0f%% %s" % (
                r["verdict"], os.path.basename(r["file"]), r["palette_id"], "(%d,%d,%d)" % tuple(r["mean_srgb"]),
                r["dE"], r["tol"], r["spread_p75"], r["observed_spread"], r["masked_frac"] * 100,
                "; ".join(r["warnings"])))
        else:
            print("%-4s %s: %s" % (r["verdict"], r["file"], r["why"]))
    nf = sum(r["verdict"] == "FAIL" for r in res)
    nw = sum(r["verdict"] == "WARN" for r in res)
    print("matcheck: %d checked, %d FAIL, %d WARN" % (len(res), nf, nw))
    if a.json:
        with open(a.json, "wb") as f:
            f.write(json.dumps({"check": "C1 palette", "results": res}, indent=1).encode("utf-8"))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
