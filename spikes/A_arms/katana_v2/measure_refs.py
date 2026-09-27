"""Measure the katana reference photos (data/A/refs) -> ref_measurements.json + annotated PNGs.

    python spikes/A_arms/katana_v2/measure_refs.py

Everything here is a measurement of a published photo; katana_spec.json cites these numbers by ref id.
  kissaki  : Met 27600 / 27601 kissaki close-ups (CC0). Edge and mune silhouette per row, the yokote row
             (strongest brightness step in the hira-ji band), the shinogi line (dark shinogi-ji band), normalised
             fukura profile, kissaki length / width at the yokote.
  blade    : Met 27600 whole-blade photo (CC0), scaled by the museum's nagasa (71.5 cm): sori and where it peaks,
             width taper.
  koshirae : TNM F-19992 (ColBase, CC BY 4.0), scaled by the museum's overall mounting length (93.0 cm):
             tsuka length, tsuba diameter, count of wrap diamonds.
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
JAPAN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
REFS = os.path.join(JAPAN, "data", "A", "refs")
OUT = os.path.join(HERE, "measure")


def gray(fn):
    return np.asarray(Image.open(os.path.join(REFS, fn)).convert("L"), np.float32)


def extents(im, thr):
    rows = []
    for y in range(im.shape[0]):
        idx = np.where(im[y] > thr)[0]
        rows.append((idx.min(), idx.max()) if len(idx) > 2 else None)
    return rows


def measure_kissaki(ref_id, fn, edge_left=True, thr=40, below=900):
    im = gray(fn)
    ex = extents(im, thr)
    tip = next(y for y, e in enumerate(ex) if e is not None)
    ys = np.arange(tip, min(im.shape[0], tip + below))
    edge = np.array([ex[y][0] if edge_left else ex[y][1] for y in ys], np.float64)
    mune = np.array([ex[y][1] if edge_left else ex[y][0] for y in ys], np.float64)
    width = np.abs(mune - edge)
    # smooth the silhouette (1 px jitter)
    k = np.ones(9) / 9
    width_s = np.convolve(width, k, mode="same")
    # yokote: strongest mean vertical brightness step in the hira-ji band (20-45 % of the width from the edge),
    # searched where the width has almost reached its straight-blade value
    grad = np.zeros(len(ys))
    for i in range(3, len(ys) - 3):
        y = ys[i]
        a = int(edge[i] + (0.20 if edge_left else -0.45) * width[i])
        b = int(edge[i] + (0.45 if edge_left else -0.20) * width[i])
        a, b = min(a, b), max(a, b)
        up = im[y - 3:y, a:b].mean()
        dn = im[y + 1:y + 4, a:b].mean()
        grad[i] = abs(dn - up)
    # search window: the last 250 rows of the fukura, i.e. up to where the width stops growing fast
    slope = np.gradient(np.convolve(width_s, np.ones(25) / 25, mode="same"))
    i_peak = int(np.argmax(slope[20:len(ys) // 2])) + 20
    i_end = i_peak + int(np.argmax(slope[i_peak:] < 0.10)) + 30
    lo = max(5, i_end - 250)
    search = slice(lo, i_end)
    i_yok = lo + int(np.argmax(grad[search]))
    w_yok = float(np.median(width[i_yok:i_yok + 15]))
    L_k = float(i_yok)
    # shinogi line: inner edge of the dark shinogi-ji band (between the hira-ji and the bright mune facet)
    shin = []
    for i in range(0, len(ys), 4):
        y = ys[i]
        seg = im[y, int(min(edge[i], mune[i])):int(max(edge[i], mune[i])) + 1]
        if len(seg) < 12:
            shin.append((i, None))
            continue
        segs = seg if edge_left else seg[::-1]            # from the edge towards the mune
        sm = np.convolve(segs, np.ones(5) / 5, mode="same")
        n = len(sm)
        dark = np.where(sm[: int(0.97 * n)] < 45)[0]
        dark = dark[dark > 0.35 * n]
        shin.append((i, float(dark.min()) / width[i] if len(dark) else None))
    straight = [f for i, f in shin if f is not None and i > i_yok + 40]
    f_shin = float(np.median(straight)) if straight else None
    # normalised fukura: s = distance from the tip / kissaki length, w = width / width at the yokote
    prof = []
    for s in np.linspace(0, 1, 21):
        i = int(round(s * L_k))
        prof.append([round(float(s), 3), round(float(width_s[i] if i > 4 else width[i]) / w_yok, 4)])
    # ko-shinogi inside the kissaki (fraction of local width, from the edge)
    ko = [[round(i / L_k, 3), round(f, 3)] for i, f in shin if f is not None and 0.1 * L_k < i < L_k]
    # colours below the yokote: the hamon (frosted band near the edge) and the ji (between hamon and shinogi)
    rgbim = np.asarray(Image.open(os.path.join(REFS, fn)).convert("RGB"), np.float32)
    ham, ji, shj = [], [], []
    for i in range(i_yok + 60, min(len(ys), i_yok + 400), 3):
        y = ys[i]
        def at(f):
            x = int(edge[i] + f * width[i]) if edge_left else int(edge[i] - f * width[i])
            return rgbim[y, x]
        ham += [at(f) for f in (0.08, 0.12, 0.16)]
        ji += [at(f) for f in (0.36, 0.42, 0.48)]
        shj += [at(f) for f in (0.70, 0.75)]
    colours = {k: [int(c) for c in np.median(np.array(v), 0)] for k, v in (("hamon_rgb", ham), ("ji_rgb", ji), ("shinogi_ji_rgb", shj))}
    # annotated image
    os.makedirs(OUT, exist_ok=True)
    crop_h = int(min(len(ys), L_k * 2.2))
    img = Image.open(os.path.join(REFS, fn)).convert("RGB").crop((0, tip - 40, im.shape[1], tip + crop_h))
    d = ImageDraw.Draw(img)
    for i in range(0, crop_h - 1, 3):
        d.point((edge[i], i + 40), fill=(255, 60, 60))
        d.point((mune[i], i + 40), fill=(60, 160, 255))
    d.line([(0, i_yok + 40), (im.shape[1], i_yok + 40)], fill=(255, 220, 0), width=3)
    for i, f in shin:
        if f is not None and i < crop_h:
            x = edge[i] + f * width[i] if edge_left else edge[i] - f * width[i]
            d.ellipse([x - 3, i + 37, x + 3, i + 43], outline=(0, 255, 0))
    img.thumbnail((900, 1200))
    img.save(os.path.join(OUT, "kissaki_%s.png" % ref_id))
    return {
        "ref": ref_id, "photo": fn, "tip_row": int(tip), "yokote_row": int(ys[i_yok]),
        "kissaki_len_px": L_k, "width_at_yokote_px": w_yok,
        "kissaki_len_over_sakihaba": round(L_k / w_yok, 3),
        "shinogi_from_edge_frac": round(f_shin, 3) if f_shin else None,
        "fukura_profile_s_w": prof, "ko_shinogi_s_frac": ko, "colours_below_yokote": colours,
        "note": "s = distance from the point along the blade axis / kissaki length; w = blade width / width at the yokote",
    }


def measure_blade(ref_id, fn, nagasa_cm, thr=45, bright=95, machi_row=None):
    im = gray(fn)
    ex = extents(im, thr)
    rows = [y for y, e in enumerate(ex) if e is not None]
    tip = rows[0]
    # polished blade ends at the machi: mean brightness inside the silhouette drops (nakago is dark)
    means = []
    for y in rows:
        l, r = ex[y]
        means.append(im[y, l:r + 1].mean())
    means = np.array(means)
    sm = np.convolve(means, np.ones(31) / 31, mode="same")
    idx = [k for k, y in enumerate(rows) if y > tip + 0.6 * (rows[-1] - tip) and sm[k] < bright]
    machi = rows[idx[0]] if machi_row is None else int(machi_row)
    ys = np.arange(tip, machi)
    L = np.array([ex[y][0] for y in ys], np.float64)
    R = np.array([ex[y][1] for y in ys], np.float64)
    mid = (L + R) / 2
    # which side is convex (the edge): the side whose line bows outward from the tip-machi chord
    def bow(line):
        t = (ys - ys[0]) / (ys[-1] - ys[0])
        chord = line[0] + (line[-1] - line[0]) * t
        return line - chord
    bl, br = bow(L), bow(R)
    edge_is_right = br.max() > -bl.min()
    mune = L if edge_is_right else R
    # sori: max distance of the mune line from the chord tip -> mune-machi (perpendicular ~ horizontal here)
    t = (ys - ys[0]) / (ys[-1] - ys[0])
    chord = mune[0] + (mune[-1] - mune[0]) * t
    dev = (mune - chord) * (1 if edge_is_right else -1)
    k = int(np.argmax(dev))
    length_px = float(np.hypot(ys[-1] - ys[0], mune[-1] - mune[0]))
    cm = nagasa_cm / length_px
    width = R - L
    wm = float(np.median(width[-40:-10]))
    # mekugi-ana: background showing through the nakago centre line below the machi
    holes, inside = [], None
    for y in range(machi + 10, rows[-1] - 5):
        if ex[y] is None:
            break
        l, r = ex[y]
        hole = im[y, (l + r) // 2] < 25 and r - l > 8
        if hole and inside is None:
            inside = y
        elif not hole and inside is not None:
            if y - inside > 5:
                holes.append(round(((inside + y) / 2 - machi) * cm, 2))
            inside = None
    ws = [(round(float(f), 2), round(float(np.median(width[int(f * (len(ys) - 1)) - 5:int(f * (len(ys) - 1)) + 5])) * cm, 2))
          for f in (0.1, 0.25, 0.5, 0.75, 0.9)]
    os.makedirs(OUT, exist_ok=True)
    img = Image.open(os.path.join(REFS, fn)).convert("RGB")
    d = ImageDraw.Draw(img)
    d.line([(mune[0], ys[0]), (mune[-1], ys[-1])], fill=(255, 220, 0), width=4)
    d.line([(mune[k], ys[k]), (chord[k], ys[k])], fill=(255, 60, 60), width=8)
    d.line([(0, machi), (im.shape[1], machi)], fill=(60, 160, 255), width=4)
    img.thumbnail((500, 1100))
    img.save(os.path.join(OUT, "blade_%s.png" % ref_id))
    return {
        "ref": ref_id, "photo": fn, "scale_from": "museum nagasa %.1f cm = tip-to-machi chord" % nagasa_cm,
        "cm_per_px": round(cm, 5), "edge_side_in_photo": "right" if edge_is_right else "left",
        "sori_cm": round(float(dev[k]) * cm, 2),
        "sori_peak_from_machi_frac": round(1 - k / (len(ys) - 1), 3),
        "width_near_machi_cm": round(wm * cm, 2), "width_samples_from_tip_frac_cm": ws,
        "mekugi_ana_below_machi_cm": holes, "machi_row": int(machi), "tip_row": int(tip),
        "note": "photo widths include perspective and lighting, so they are a cross-check, not the spec value",
    }


def measure_koshirae(ref_id, fn, total_cm):
    rgb = np.asarray(Image.open(os.path.join(REFS, fn)).convert("RGB"), np.float32)
    H, W, _ = rgb.shape
    # background varies (light blue, vignetting): compare each pixel with its column's median of the top/bottom rows
    bgcol = np.median(np.concatenate([rgb[:60], rgb[-60:]], 0), 0)       # (W, 3)
    diff = np.abs(rgb - bgcol[None]).sum(-1)
    mask = diff > 70
    # track the vertical run through the mounting's axis from the middle of the tsuka, both ways
    def run_at(x, yc):
        col = mask[:, x]
        if not col[max(0, min(H - 1, yc))]:
            near = np.where(col[max(0, yc - 15):yc + 15])[0]
            if not len(near):
                return None
            yc = max(0, yc - 15) + int(near[len(near) // 2])
        a = yc
        while a > 0 and col[a - 1]:
            a -= 1
        b = yc
        while b < H - 1 and col[b + 1]:
            b += 1
        return a, b
    xs_mid = int(0.2 * W)
    col = np.where(mask[:, xs_mid])[0]
    runs = {}
    for direction in (-1, 1):
        yc = int(np.median(col))
        x = xs_mid
        while 0 <= x < W:
            r = run_at(x, yc)
            if r is None or r[1] - r[0] < 8:
                break
            runs[x] = r
            h = r[1] - r[0]
            if h < 120:                     # only re-centre on the slim parts (tsuka, saya), not on the tsuba/cord
                yc = (r[0] + r[1]) // 2
            x += direction
    xs = sorted(runs)
    x0, x1 = xs[0], xs[-1]
    heights = np.array([runs[x][1] - runs[x][0] if x in runs else 0 for x in range(W)])
    # tsuba: the tallest column group in the first quarter (tsuka side, before the kurikata and its cord)
    left = slice(x0, x0 + int(0.25 * (x1 - x0)))
    xt = x0 + int(np.argmax(heights[left]))
    cols_t = [x for x in range(xt - 60, xt + 60) if heights[x] > 0.6 * heights[xt]]
    t0, t1 = min(cols_t), max(cols_t)
    total_px = x1 - x0
    tsuka_h = float(np.median(heights[x0 + 40:t0 - 40]))
    cm = total_cm / total_px
    # wrap diamonds: darkness along the tsuka centre line (black same windows vs. buff wrap)
    sig, cols_rgb_wrap, cols_rgb_same = [], [], []
    for x in range(x0 + 20, t0 - 10):
        a, b = runs[x]
        c = (a + b) // 2
        band = rgb[c - 4:c + 5, x]
        lum = band.mean(-1)
        sig.append(float(lum.mean()))
        cols_rgb_wrap += [tuple(p) for p, l in zip(band, lum) if l > 150]
        cols_rgb_same += [tuple(p) for p, l in zip(band, lum) if l < 70]
    sig = np.convolve(np.array(sig), np.ones(9) / 9, mode="same")
    thr = (sig.max() + sig.min()) / 2
    dark = sig < thr
    n_dia = int(np.sum(dark[1:] & ~dark[:-1]))
    runs_dark = np.where(dark[1:] & ~dark[:-1])[0]
    pitch_cm = float(np.median(np.diff(runs_dark))) * cm if len(runs_dark) > 2 else None
    wrap_rgb = [int(v) for v in np.median(np.array(cols_rgb_wrap), 0)] if cols_rgb_wrap else None
    same_rgb = [int(v) for v in np.median(np.array(cols_rgb_same), 0)] if cols_rgb_same else None
    ts = rgb[runs[xt][0]:runs[xt][1], t0:t1].reshape(-1, 3)
    ts = ts[ts.mean(-1) < 110]
    tsuba_rgb = [int(v) for v in np.median(ts, 0)] if len(ts) else None
    return {
        "wrap_diamonds_one_face": n_dia, "wrap_diamond_pitch_cm": round(pitch_cm, 2) if pitch_cm else None,
        "wrap_rgb": wrap_rgb, "same_rgb": same_rgb, "tsuba_dark_rgb": tsuba_rgb,
        "ref": ref_id, "photo": fn, "scale_from": "museum overall mounting length %.1f cm = photo extent" % total_cm,
        "cm_per_px": round(cm, 4), "kashira_end_x": x0, "kojiri_end_x": x1, "tsuba_x": [t0, t1],
        "tsuka_len_cm_incl_fuchi_kashira": round((t0 - x0) * cm, 1),
        "tsuba_height_cm": round(float(heights[xt]) * cm, 1),
        "tsuba_thickness_cm_side_view": round((t1 - t0) * cm, 2),
        "tsuka_height_cm": round(tsuka_h * cm, 2),
        "note": "photo is near side-on; the mounting is curved and slightly tilted, so +-5 %",
    }


def main():
    res = {
        "kissaki": [measure_kissaki("met27600", "met27600_LC-2007_478_2a_b-032.jpg"),
                    measure_kissaki("met27601", "met27601_LC-2007_478_3a_c-020.jpg")],
        "blade": [measure_blade("met27600", "met27600_LC-2007_478_2a_b.jpg", 71.5)],
        "koshirae": [measure_koshirae("tnm_F19992", "wc_motoshige_koshirae.jpg", 93.0)],
    }
    with open(os.path.join(HERE, "ref_measurements.json"), "wb") as f:
        f.write(json.dumps(res, indent=1).encode("utf-8"))
    for k, v in res.items():
        for r in v:
            print(k, {a: b for a, b in r.items() if a not in ("fukura_profile_s_w", "ko_shinogi_s_frac")})
    for r in res["kissaki"]:
        print(r["ref"], "fukura", r["fukura_profile_s_w"])
        print(r["ref"], "ko-shinogi", r["ko_shinogi_s_frac"][::3])


if __name__ == "__main__":
    main()
