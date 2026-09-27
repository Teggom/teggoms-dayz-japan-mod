"""Step 4: our katana against the references -> compare_sheet.png, katana_spec_overlay.png, compare_metrics.json

    python spikes/A_arms/katana_v2/compare.py          (after build.py and render_blender.py)

Row 1  whole sword / blade, side, same px per cm, point up, edge left, aligned at the machi:
       ours (Blender side render) | Met 27600 blade | Met 27601 blade | TNM F-19992 koshirae (sheathed)
Row 2  kissaki, scaled so the width at the yokote matches, aligned at the yokote: ours | Met 27600 | Met 27601
Row 3  tsuka, same px per cm, kashira down: ours | TNM F-19992 | modern tsuka (how windows and menuki read)
Row 4  the shipped mesh (binarized ODOL LOD 0) silhouette in red over the spec drawing (side view + kissaki)
Numbers: measure_refs.py's photo measurements are re-run on our renders (masked to a black background).
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(os.path.dirname(HERE), "tools")
sys.path.insert(0, TOOLS)
sys.path.insert(0, HERE)
import katana_geom  # noqa: E402
import measure_refs as MR  # noqa: E402
from odol import read_odol  # noqa: E402

JAPAN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
REFS = os.path.join(JAPAN, "data", "A", "refs")
REN = os.path.join(HERE, "renders_alpha")      # transparent-film renders (render_blender.py --alpha)
MEAS = os.path.join(HERE, "measure")
P3D = os.path.join(JAPAN, "src", "JP", "weapons", "katana", "jp_katana.p3d")
G = katana_geom.KatanaGeom()


def font(size):
    for f in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


F_T, F_L, F_S = font(34), font(22), font(17)


def _alpha(img):
    """(rgb, mask) of a render: from the alpha channel of the transparent-film renders (renders_alpha/)"""
    a = np.asarray(img.convert("RGBA"), np.float32)
    return a[..., :3], a[..., 3] > 127


def mask_render(fn, out):
    """our render on black with every object pixel >= 46 (so measure_refs treats it like the museum photos)"""
    rgb, m = _alpha(Image.open(os.path.join(REN, fn)))
    b = np.where(m[..., None], np.maximum(rgb, 46), 0).astype(np.uint8)
    Image.fromarray(b).save(os.path.join(MEAS, out))
    return m


def side_px_per_m(mask):
    """side render: the sword's vertical extent in pixels / its model Y extent (from the shipped ODOL)"""
    v = np.array(read_odol(P3D)["lods"][0].vertices)
    top, bot = rows_extent(mask)
    return (bot - top) / float(v[:, 1].max() - v[:, 1].min())


def tsuka_px_per_m(mask):
    """tsuka close-up: the widest row is the round tsuba seen edge-on = its diameter"""
    widths = [(np.where(r)[0].max() - np.where(r)[0].min()) if r.any() else 0 for r in mask]
    return max(widths) / (2 * G.tsuba_r)


def black_bg(img):
    """a transparent-film render composited over black, like the museum photos"""
    a = np.asarray(img.convert("RGBA"), np.float32)
    return Image.fromarray((a[..., :3] * (a[..., 3:] / 255.0)).astype(np.uint8))


def mesh_dims():
    """dimensions measured straight off the shipped, binarized ODOL LOD 0 (the 'blade' selection + all vertices)"""
    lod = read_odol(P3D)["lods"][0]
    V_ = np.array(lod.vertices, np.float64)
    B = V_[sorted(set(lod.selections["blade"]))]
    s, d = G.model_to_sd(B[:, 1], B[:, 2])
    x = B[:, 0]
    sr = np.round(s, 6)
    us, cnt = np.unique(sr, return_counts=True)
    s_tip = us.max()
    mune = [(ss, B[(sr == ss) & (np.abs(d) < 2e-4)]) for ss in us if ((sr == ss) & (np.abs(d) < 2e-4)).any()]
    P0 = mune[0][1][:, 1:].mean(0)
    P1 = B[sr == s_tip][:, 1:].mean(0)
    chord = np.linalg.norm(P1 - P0)
    t = (P1 - P0) / chord
    devs = []
    for ss, pts in mune:
        q = pts[:, 1:].mean(0) - P0
        devs.append((abs(q[0] * t[1] - q[1] * t[0]), float(np.dot(q, t)) / chord))
    k = int(np.argmax([dv for dv, _ in devs]))
    s_yok = us[np.argmax(cnt)]                         # the yokote ring is duplicated (body end + kissaki start)
    ring0 = (sr == us.min())
    ring_y = (sr == s_yok)
    d0 = np.sort(np.unique(np.round(d[ring0], 6)))
    kas = 2 * np.abs(x[ring0 & (np.abs(d - d0[1]) < 2e-5)]).max()      # thickness at the mune bevel = kasane
    shin = 2 * np.abs(x[ring0]).max()
    ally = V_[:, 1]
    tsuba = V_[(ally > G.y_tsuba[0] - 1e-4) & (ally < G.y_tsuba[1] + 1e-4)]
    return {
        "nagasa_cm": round(chord * 100, 2), "sori_cm": round(devs[k][0] * 100, 2), "sori_peak_from_machi_frac": round(devs[k][1], 3),
        "motohaba_cm": round(d[ring0].max() * 100, 2), "sakihaba_cm": round(d[ring_y].max() * 100, 2),
        "kissaki_cm": round((s_tip - s_yok) * 100, 2), "motokasane_cm": round(kas * 100, 3), "shinogi_thickness_machi_cm": round(shin * 100, 3),
        "tsuba_diameter_cm": round(2 * np.hypot(tsuba[:, 0], tsuba[:, 2]).max() * 100, 2),
        "tsuka_len_cm": round((G.y_tsuka_top - ally.min()) * 100, 2),
        "tip_on_mune_line_mm": round(float(np.abs(G.model_to_sd(P1[0], P1[1])[1])) * 1000, 3),
    }


def rows_extent(mask):
    r = np.where(mask.any(1))[0]
    return int(r.min()), int(r.max())


def orient(img, edge_side, want="left"):
    return ImageOps.mirror(img) if edge_side != want else img


def label(img, text, f=None):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 30], fill=(250, 248, 240))
    d.text((6, 4), text, font=f or F_S, fill=(20, 20, 30))
    return img


def row_whole(metrics):
    """row 1: 12 px / cm, point up, edge left, machi aligned"""
    K = 12.0
    tiles = []
    # ours: side render, machi at model y = G.y_machi
    m = mask_render("jp_katana_side.png", "ours_side_masked.png")
    ppm = side_px_per_m(m)
    ours = Image.open(os.path.join(REN, "jp_katana_side.png")).convert("RGB")
    top, bot = rows_extent(m)                       # point .. kashira end (model y: tip .. y_end)
    y_tip = G.tip()[1]
    machi_row = top + (y_tip - G.y_machi) * ppm
    cols = np.where(m[int(machi_row) - 3])[0]
    ang = np.degrees(G.alpha)                        # chord vs tsuka axis: turn the chord upright like the photos
    ours = black_bg(ours).rotate(ang, resample=Image.BICUBIC, center=(float(cols.mean()), float(machi_row)))
    s = K * 100 / ppm
    ours = ours.resize((int(ours.width * s), int(ours.height * s)))
    tiles.append(("ours (render, chord upright)", ours, machi_row * s))
    metrics["ours_side_machi_row"] = float(machi_row)
    # Met 27600 / 27601 whole blades: scale from each museum nagasa (measure_blade), machi row measured
    for ref, fn, nag in (("met27600", "met27600_LC-2007_478_2a_b.jpg", 71.5), ("met27601", "met27601_LC-2007_478_3a_c-005.jpg", 80.8)):
        r = MR.measure_blade(ref + "_cmp", fn, nag)
        metrics["photo_" + ref + "_blade"] = {k: r[k] for k in ("sori_cm", "sori_peak_from_machi_frac", "edge_side_in_photo", "cm_per_px")}
        im = Image.open(os.path.join(REFS, fn)).convert("RGB")
        s = K * r["cm_per_px"]
        im = orient(im, r["edge_side_in_photo"])
        machi = r.get("machi_row")
        im = im.resize((int(im.width * s), int(im.height * s)))
        tiles.append(("%s blade (Met, CC0), nagasa %.1f" % (ref, nag), im, machi * s))
    # TNM F-19992: horizontal, kashira left -> rotate point up; tsuba ~ machi
    k = MR.measure_koshirae("tnm_F19992", "wc_motoshige_koshirae.jpg", 93.0)
    im = Image.open(os.path.join(REFS, "wc_motoshige_koshirae.jpg")).convert("RGB")
    im = im.crop((k["kashira_end_x"] - 20, 300, k["kojiri_end_x"] + 20, 1000))
    tsuba_x = k["tsuba_x"][1] - (k["kashira_end_x"] - 20)
    s = K * k["cm_per_px"]
    cw = im.width
    im = im.rotate(90, expand=True)                  # CCW: kashira (left) -> bottom, point up; the photo is edge-up
                                                     # (saya bows up), so the edge ends on the left, like ours
    im = im.resize((int(im.width * s), int(im.height * s)))
    machi_row = (cw - tsuba_x) * s
    tiles.append(("TNM F-19992 koshirae (ColBase CC BY 4.0), 93.0 cm", im, machi_row))
    # compose aligned at the machi
    above = max(t[2] for t in tiles)
    below = max(t[1].height - t[2] for t in tiles)
    W = sum(min(t[1].width, 360) for t in tiles) + 20 * len(tiles)
    H = int(above + below) + 40
    out = Image.new("RGB", (W, H), (30, 30, 34))
    x = 0
    for name, im, mr in tiles:
        cw = min(im.width, 360)
        c = im.crop(((im.width - cw) // 2, 0, (im.width - cw) // 2 + cw, im.height))
        out.paste(c, (x, int(above - mr) + 36))
        ImageDraw.Draw(out).text((x + 4, 4), name, font=F_S, fill=(240, 240, 240))
        x += cw + 20
    d = ImageDraw.Draw(out)
    d.line([(0, above + 36), (W, above + 36)], fill=(255, 200, 0), width=1)
    d.text((4, above + 40), "machi / tsuba line; scale 12 px per cm for every tile", font=F_S, fill=(255, 200, 0))
    return out


def row_tip(metrics):
    """row 2: kissaki, yokote width = 240 px, yokote rows aligned"""
    WY = 240.0
    tiles = []
    s_c = G.L_arc - 0.55 * G.L_k                      # the close-up is centred here (render_blender FOCUS)
    tip_up = black_bg(Image.open(os.path.join(REN, "jp_katana_tip.png"))).rotate(np.degrees(G.theta(s_c)), resample=Image.BICUBIC)
    tip_up.save(os.path.join(REN, "jp_katana_tip_upright.png"))
    a = np.asarray(tip_up, np.float32)
    Image.fromarray(np.where((a.sum(-1) > 0)[..., None], np.maximum(a, 46), 0).astype(np.uint8)).save(os.path.join(MEAS, "ours_tip_masked.png"))
    MR.REFS = MEAS
    ours = MR.measure_kissaki("ours", "ours_tip_masked.png")
    MR.REFS = REFS
    metrics["ours_kissaki_from_render"] = {k: ours[k] for k in ("kissaki_len_over_sakihaba", "shinogi_from_edge_frac")}
    metrics["ours_kissaki_from_render"]["fukura_w_at_t"] = {str(p[0]): p[1] for p in ours["fukura_profile_s_w"][::4]}
    refs = [MR.measure_kissaki(r, f) for r, f in (("met27600", "met27600_LC-2007_478_2a_b-032.jpg"), ("met27601", "met27601_LC-2007_478_3a_c-020.jpg"))]
    for r in refs:
        metrics["photo_" + r["ref"] + "_kissaki"] = {"kissaki_len_over_sakihaba": r["kissaki_len_over_sakihaba"],
                                                     "fukura_w_at_t": {str(p[0]): p[1] for p in r["fukura_profile_s_w"][::4]}}
    for name, r, path in (("ours (render, kissaki upright)", ours, os.path.join(REN, "jp_katana_tip_upright.png")),
                          ("Met 27600 (1622, CC0)", refs[0], os.path.join(REFS, refs[0]["photo"])),
                          ("Met 27601 (17th c., CC0)", refs[1], os.path.join(REFS, refs[1]["photo"]))):
        im = Image.open(path).convert("RGB")
        s = WY / r["width_at_yokote_px"]
        top = r["tip_row"] - 0.25 * r["kissaki_len_px"]
        bot = r["yokote_row"] + 1.2 * r["kissaki_len_px"]
        im = im.crop((0, int(top), im.width, int(bot)))
        im = im.resize((int(im.width * s), int(im.height * s)))
        # centre horizontally on the blade at the yokote
        a = np.asarray(im.convert("L"), np.float32)
        yk = int((r["yokote_row"] - top) * s)
        row = a[min(yk + 5, a.shape[0] - 1)]
        cols = np.where(np.abs(row - np.median(a[:, :10])) > 25)[0]
        cx = int(cols.mean()) if len(cols) else im.width // 2
        c = im.crop((cx - 260, 0, cx + 260, im.height))
        tiles.append((name + ": kissaki %.2f x sakihaba" % r["kissaki_len_over_sakihaba"], c, yk))
    above = max(t[2] for t in tiles)
    below = max(t[1].height - t[2] for t in tiles)
    W = sum(t[1].width + 20 for t in tiles)
    out = Image.new("RGB", (W, int(above + below) + 40), (30, 30, 34))
    x = 0
    for name, im, yk in tiles:
        out.paste(im, (x, int(above - yk) + 36))
        ImageDraw.Draw(out).text((x + 4, 4), name, font=F_S, fill=(240, 240, 240))
        x += im.width + 20
    d = ImageDraw.Draw(out)
    d.line([(0, above + 36), (W, above + 36)], fill=(255, 200, 0), width=1)
    d.text((4, above + 40), "yokote; every tile scaled to the same width at the yokote", font=F_S, fill=(255, 200, 0))
    return out


def row_tsuka(metrics):
    """row 3: 30 px / cm, kashira at the bottom"""
    K = 30.0
    tiles = []
    ppm = tsuka_px_per_m(mask_render("jp_katana_tsuka.png", "ours_tsuka_masked.png"))
    ours = Image.open(os.path.join(REN, "jp_katana_tsuka.png")).convert("RGB")
    s = K * 100 / ppm
    metrics["ours_tsuka_render_px_per_cm"] = round(ppm / 100, 2)
    ours = ours.resize((int(ours.width * s), int(ours.height * s)))
    tiles.append(("ours (render, omote face)", ours))
    k = MR.measure_koshirae("tnm_F19992", "wc_motoshige_koshirae.jpg", 93.0)
    im = Image.open(os.path.join(REFS, "wc_motoshige_koshirae.jpg")).convert("RGB")
    im = im.crop((k["kashira_end_x"] - 10, 520, k["tsuba_x"][1] + 60, 760))
    im = im.rotate(90, expand=True)                  # kashira (left) -> bottom; edge (up in the photo) -> left
    s = K * k["cm_per_px"]
    im = im.resize((int(im.width * s), int(im.height * s)))
    tiles.append(("TNM F-19992, %.1f cm" % k["tsuka_len_cm_incl_fuchi_kashira"], im))
    mod = Image.open(os.path.join(REFS, "wc_two_mekugi_hilt.jpg")).convert("RGB")
    mod.thumbnail((520, 760))
    tiles.append(("modern (CC0), not to scale", mod))
    metrics["tsuka"] = {"ours_len_cm": round(G.tsuka_len * 100, 1), "ours_windows": G.n_windows, "ours_pitch_cm": round(G.pitch_eff * 100, 2),
                        "tnm_len_cm": k["tsuka_len_cm_incl_fuchi_kashira"], "tnm_windows": k["wrap_diamonds_one_face"], "tnm_pitch_cm": k["wrap_diamond_pitch_cm"]}
    H = max(t[1].height for t in tiles) + 40
    W = sum(min(t[1].width, 520) + 20 for t in tiles)
    out = Image.new("RGB", (W, H), (30, 30, 34))
    x = 0
    for name, im in tiles:
        cw = min(im.width, 520)
        c = im.crop(((im.width - cw) // 2, 0, (im.width - cw) // 2 + cw, im.height))
        out.paste(c, (x, H - c.height))
        ImageDraw.Draw(out).text((x + 4, 4), name, font=F_S, fill=(240, 240, 240))
        x += cw + 20
    return out


def overlay(metrics):
    """shipped ODOL LOD 0 in red over the spec drawing (panel A side view and panel C kissaki)"""
    import draw_spec
    V_ = np.array(read_odol(P3D)["lods"][0].vertices, np.float64)
    F_ = read_odol(P3D)["lods"][0].faces
    res = {}

    def hook(img, PA, PC):
        # side view: fill every projected face into a mask at panel resolution, draw the mask boundary
        for P, fn, key in ((PA, lambda p: (p[1], p[2]), "side"), (PC, None, "kissaki")):
            mask = Image.new("L", img.size, 0)
            dm = ImageDraw.Draw(mask)
            for f in F_:
                pts = V_[list(f)]
                if key == "kissaki":
                    if pts[:, 1].min() < G.mune_point(G.s_yokote - 0.03)[1] - 0.01:
                        continue
                    s, d = G.model_to_sd(pts[:, 1], pts[:, 2])
                    if s.max() < G.s_yokote - 0.03:
                        continue
                    q = [P.P(a, b) for a, b in zip(s, d)]
                else:
                    q = [P.P(p[1], p[2]) for p in pts]
                dm.polygon(q, fill=255)
            m = np.asarray(mask) > 0
            er = np.zeros_like(m)
            er[1:-1, 1:-1] = m[1:-1, 1:-1] & m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]
            edge = m & ~er
            a = np.array(img)
            a[edge] = (230, 0, 0)
            img.paste(Image.fromarray(a))
            res[key] = m
        # kissaki agreement: mesh mask vs spec blade raster, inside panel C's blade window
        ss, dd = np.meshgrid(np.linspace(G.s_yokote - 0.03, G.L_arc, 700), np.linspace(-0.002, G.sakihaba + 0.002, 140))
        spec_in = katana_geom.KatanaGeom.zone_v(G, ss.ravel(), dd.ravel()).reshape(ss.shape) > 0
        px = np.array([PC.P(a, b) for a, b in zip(ss.ravel(), dd.ravel())]).round().astype(int)
        mesh_in = res["kissaki"][np.clip(px[:, 1], 0, img.size[1] - 1), np.clip(px[:, 0], 0, img.size[0] - 1)].reshape(ss.shape)
        inter = (spec_in & mesh_in).sum()
        union = (spec_in | mesh_in).sum()
        metrics["overlay_kissaki_iou_mesh_vs_spec"] = round(float(inter) / float(union), 4)
    draw_spec.main(overlay_hook=hook, out_name="katana_spec_overlay.png")
    return Image.open(os.path.join(HERE, "katana_spec_overlay.png")).convert("RGB")


def main():
    os.makedirs(MEAS, exist_ok=True)
    metrics = {"spec": {"kissaki_len_over_sakihaba": katana_geom.V(G.spec["kissaki"]["length_over_sakihaba"]),
                        "sori_cm": G.sori * 100, "sori_peak_from_machi_frac": 0.5, "nagasa_cm": G.nagasa * 100,
                        "motohaba_cm": G.motohaba * 100, "sakihaba_cm": G.sakihaba * 100, "kissaki_cm": G.L_k * 100,
                        "motokasane_cm": G.motokasane * 100, "shinogi_thickness_machi_cm": G.shin_ratio * G.motokasane * 100,
                        "tsuba_diameter_cm": G.tsuba_r * 200, "tsuka_len_cm": G.tsuka_len * 100}}
    metrics["mesh_from_odol"] = mesh_dims()
    r1, r2, r3 = row_whole(metrics), row_tip(metrics), row_tsuka(metrics)
    ov = overlay(metrics)
    # our whole-blade render measured like the photos
    m = mask_render("jp_katana_side.png", "ours_side_masked.png")
    MR.REFS = MEAS
    rb = MR.measure_blade("ours_side", "ours_side_masked.png", G.nagasa * 100, bright=60, machi_row=metrics["ours_side_machi_row"])
    MR.REFS = REFS
    metrics["ours_blade_from_render"] = {k: rb[k] for k in ("sori_cm", "sori_peak_from_machi_frac", "edge_side_in_photo")}
    ov_c = ov.crop((0, 0, ov.width, 1560))
    ov_c.thumbnail((2600, 1300))
    W = max(r1.width, r2.width, r3.width, ov_c.width) + 40
    H = 90 + r1.height + r2.height + r3.height + ov_c.height + 4 * 60
    sheet = Image.new("RGB", (W, H), (250, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((20, 20), "JP_Katana v2 vs references (c.1600)  -  compare sheet", font=F_T, fill=(20, 20, 30))
    y = 90
    for title, im in (("1  Whole sword / blades: same scale, point up, edge left, aligned at the machi", r1),
                      ("2  Kissaki: same width at the yokote, aligned at the yokote", r2),
                      ("3  Tsuka: same scale (30 px/cm), kashira down", r3),
                      ("4  Shipped mesh (binarized ODOL LOD 0) outline in red over the spec drawing; kissaki IoU %.3f" % metrics["overlay_kissaki_iou_mesh_vs_spec"], ov_c)):
        d.text((20, y), title, font=F_L, fill=(20, 20, 30))
        sheet.paste(im, (20, y + 34))
        y += im.height + 60
    sheet.save(os.path.join(HERE, "compare_sheet.png"))
    with open(os.path.join(HERE, "compare_metrics.json"), "wb") as f:
        f.write(json.dumps(metrics, indent=1).encode("utf-8"))
    print(json.dumps(metrics, indent=1))
    print("wrote compare_sheet.png", sheet.size)


if __name__ == "__main__":
    main()
