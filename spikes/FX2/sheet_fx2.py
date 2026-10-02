"""FX2 contact sheets -> research/production/contact_sheets/fx2_statues.jpg, fx2_komainu.jpg, fx2_detail.jpg,
fx2_rope.jpg. Renders (render_fx2.py, Blender, <= 3 processes) of the MLOD masters: AFTER from this tree, BEFORE from
a pre-FX2 copy (git archive c01351c built --no-binarize into the scratchpad; pass its root as BEFORE=<dir>), beside
the CC0 reference photos (data/refs/fx2, research/statues/REFS.md). Renders show what a player sees (left-handed
model space; render_parts' axis map mirrors).

  python spikes/FX2/sheet_fx2.py [--no-render]      (env BEFORE=<pre-FX2 tree root>)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import render_fx2 as R  # noqa: E402

REFS = os.path.join(DEV, "data", "refs", "fx2")
SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
BEFORE = os.environ.get("BEFORE", "")
W2F = "spikes/W2F/out/sacred/"
B3B = "spikes/B3b/out/"


def m(path, before=False):
    root = BEFORE if before else DEV
    return os.path.join(root, path).replace("\\", "/")


def dais_job(out, name, standing, before=False):
    if standing:
        cam, look = [0.0, 1.38, 1.45], [0.0, 1.25, -0.12]
    else:
        cam, look = [0.0, 1.48, 1.30], [0.0, 1.32, -0.13]
    return {"out": out, "items": [[m(W2F + name + ".p3d", before), 0, 0, 0, 0]], "cam": cam, "look": look, "lens": 50,
            "res": [700, 760]}


def jobs():
    J = []
    for k, (name, st) in {"amida": ("jp_f_dais_amida", False), "shaka": ("jp_f_dais_shaka", False),
                          "kannon": ("jp_f_dais_kannon", True), "jizo": ("jp_f_dais_jizo", True)}.items():
        J.append(dais_job("s_%s_after" % k, name, st))
        if BEFORE:
            J.append(dais_job("s_%s_before" % k, name, st, True))
    for k, p, cam, look in (("stone", B3B + "roadside/jp_s_stone_jizo_m.p3d", [0.45, 1.05, 1.9], [0.0, 0.78, 0.0]),
                            ("bib", B3B + "roadside/jp_s_stone_jizo_bib.p3d", [0.45, 1.05, 1.9], [0.0, 0.78, 0.0]),
                            ("child", B3B + "grave/jp_s_grave_stones_jizo_child.p3d", [0.25, 0.55, 1.05], [0.0, 0.36, 0.0]),
                            ("halo", B3B + "grave/jp_s_grave_stones_boat_halo.p3d", [0.3, 0.75, 1.5], [0.0, 0.55, 0.0])):
        J.append({"out": "s_%s_after" % k, "items": [[m(p), 0, 0, 0, 0]], "cam": cam, "look": look, "lens": 50,
                  "res": [700, 760]})
        if BEFORE:
            J.append({"out": "s_%s_before" % k, "items": [[m(p, True), 0, 0, 0, 0]], "cam": cam, "look": look,
                      "lens": 50, "res": [700, 760]})
    staff = {"items": [[m(W2F + "jp_f_dais_jizo.p3d"), 0, 0, 0, 0]], "cam": [0.12, 1.66, 0.42],
             "look": [0.10, 1.60, -0.04], "lens": 70, "res": [700, 760]}
    J.append(dict(staff, out="s_staff_after"))
    if BEFORE:
        J.append(dict(staff, out="s_staff_before", items=[[m(W2F + "jp_f_dais_jizo.p3d", True), 0, 0, 0, 0]],
                      cam=[0.18, 1.62, 0.42], look=[0.15, 1.55, -0.04]))
    # komainu + kitsune
    S = B3B + "shrine/"
    J.append({"out": "k_pair_a", "items": [[m(S + "jp_s_komainu_a_un.p3d"), -1.3, 0, 0, -15],
                                           [m(S + "jp_s_komainu_a_a.p3d"), 1.3, 0, 0, 15]],
              "cam": [0, 1.75, 4.6], "look": [0, 1.15, 0], "lens": 35, "res": [1000, 760], "humans": [[3.0, 0.4]]})
    J.append({"out": "k_pair_b", "items": [[m(S + "jp_s_komainu_b_un.p3d"), -1.2, 0, 0, -15],
                                           [m(S + "jp_s_komainu_b_a.p3d"), 1.2, 0, 0, 15]],
              "cam": [0, 1.6, 4.2], "look": [0, 1.0, 0], "lens": 35, "res": [1000, 760]})
    J.append({"out": "k_pair_moss", "items": [[m(S + "jp_s_komainu_a_un_moss.p3d"), -1.3, 0, 0, -15],
                                              [m(S + "jp_s_komainu_a_a_moss.p3d"), 1.3, 0, 0, 15]],
              "cam": [0.6, 1.8, 4.4], "look": [0, 1.15, 0], "lens": 35, "res": [1000, 760]})
    J.append({"out": "k_fox", "items": [[m(S + "jp_s_kitsune_key.p3d"), -0.85, 0, 0, -15],
                                        [m(S + "jp_s_kitsune_jewel.p3d"), 0.85, 0, 0, 15]],
              "cam": [0, 1.45, 3.2], "look": [0, 1.0, 0], "lens": 35, "res": [1000, 760]})
    for k, nm in (("a", "jp_s_komainu_a_a"), ("un", "jp_s_komainu_a_un")):
        J.append({"out": "k_head_" + k, "items": [[m(S + nm + ".p3d"), 0, 0, 0, 0]], "cam": [0.35, 1.85, 1.45],
                  "look": [0.0, 1.62, 0.15], "lens": 55, "res": [700, 760]})
    J.append({"out": "k_fox_head", "items": [[m(S + "jp_s_kitsune_key.p3d"), 0, 0, 0, 0]], "cam": [0.45, 1.65, 0.95],
              "look": [0.0, 1.38, 0.08], "lens": 55, "res": [700, 760]})
    # detail props
    for tag, before in (("after", False), ("before", True)):
        if before and not BEFORE:
            continue
        J.append({"out": "d_masks_" + tag, "items": [[m(W2F + "jp_f_kagura_masks.p3d", before), 0, 0, 0, 0]],
                  "cam": [0.0, 1.45, 1.25], "look": [0, 1.40, 0], "lens": 38, "res": [1200, 700]})
        J.append({"out": "d_bells_" + tag, "items": [[m(W2F + "jp_f_waniguchi.p3d", before), -0.6, 2.6, 0, 0],
                                                     [m(W2F + "jp_f_suzu_rope.p3d", before), 0.4, 2.6, 0, 0],
                                                     [m(W2F + "jp_f_bonsho_s.p3d", before), 2.0, 2.6, 0, 0]],
                  "cam": [0.7, 1.9, 3.2], "look": [0.7, 1.8, 0], "lens": 32, "res": [1200, 900]})
        J.append({"out": "d_ema_" + tag, "items": [[m(W2F + "jp_f_ema_rail.p3d", before), 0, 0, 0, 0],
                                                   [m(W2F + "jp_f_saisen_bako_l.p3d", before), 0, 0, 1.2, 0]],
                  "cam": [0.4, 1.5, 2.8], "look": [0, 1.0, 0.3], "lens": 35, "res": [1200, 900]})
    # rope
    for tag, before in (("after", False), ("before", True)):
        if before and not BEFORE:
            continue
        for nm in ("jp_s_torii_wood_myojin_rope_shide", "jp_s_torii_stone_s_rope_shide"):
            J.append({"out": "r_%s_%s" % (nm[11:], tag), "items": [[m(S + nm + ".p3d", before), 0, 0, 0, 0]],
                      "cam": [0.0, 1.7, 6.2], "look": [0.0, 2.0, 0.0], "lens": 40, "res": [900, 900],
                      "humans": [[0.0, -0.3]]})
    return J


def compose(name, rows, title, sub, h=330):
    from PIL import Image, ImageDraw
    pad = 10
    ims_rows = []
    W = 0
    for label, cells in rows:
        ims = []
        for cap, fp in cells:
            if not fp or not os.path.isfile(fp):
                continue
            im = Image.open(fp).convert("RGB")
            im.thumbnail((int(h * 1.6), h))
            ims.append((cap, im))
        ims_rows.append((label, ims))
        W = max(W, 230 + sum(i.width + pad for _, i in ims))
    H = 90 + len(rows) * (h + 34)
    S = Image.new("RGB", (W + pad, H), (244, 242, 236))
    d = ImageDraw.Draw(S)
    d.text((pad, 10), title, fill=(0, 0, 0))
    d.text((pad, 34), sub, fill=(60, 60, 60))
    y = 70
    for label, ims in ims_rows:
        d.text((pad, y + h // 2), label, fill=(0, 0, 0))
        x = 230
        for cap, im in ims:
            S.paste(im, (x, y + 18))
            d.text((x, y + 2), cap, fill=(90, 40, 20))
            x += im.width + pad
        y += h + 34
    os.makedirs(SHEETS, exist_ok=True)
    fp = os.path.join(SHEETS, name)
    S.save(fp, quality=86)
    print(fp, S.size)


def ren(k):
    return os.path.join(R.OUT, k + ".png")


def ref(fn):
    return os.path.join(REFS, fn)


def main(argv):
    if "--no-render" not in argv:
        R.run(jobs(), nproc=3)
    B = "before (pre-FX2)"
    compose("fx2_statues.jpg", [
        ("Amida (village hondo)", [("ref: Met 44890 (Amida, ca. 1250)", ref("met_44890_0.jpg")),
                                   ("after", ren("s_amida_after")), (B, ren("s_amida_before"))]),
        ("Shaka (town hondo, Zen)", [("ref: CMA 153384 (Shakyamuni)", ref("cma_153384_0.jpg")),
                                     ("ref: CMA 147590 (mandorla)", ref("cma_147590_0.jpg")),
                                     ("after", ren("s_shaka_after")), (B, ren("s_shaka_before"))]),
        ("Kannon (Kannon hall)", [("ref: CMA 152018 (Sho Kannon)", ref("cma_152018_0.jpg")),
                                  ("ref: Met 49257", ref("met_49257_0.jpg")),
                                  ("after", ren("s_kannon_after")), (B, ren("s_kannon_before"))]),
        ("Jizo (Jizo hall)", [("ref: Met 53175 (Jizo, ca. 1202)", ref("met_53175_0.jpg")),
                              ("ref: Met 76084 (Jizo, 1291)", ref("met_76084_0.jpg")),
                              ("after", ren("s_jizo_after")), (B, ren("s_jizo_before"))]),
        ("Shakujo staff head", [("ref: Met 53175 detail", ref("met_53175_1.jpg")), ("after: closed loop + rings",
                                                                                     ren("s_staff_after")),
                                (B + ": open top", ren("s_staff_before"))]),
        ("Stone roadside Jizo", [("ref: Met 53175 (face)", ref("met_53175_1.jpg")), ("after", ren("s_stone_after")),
                                 ("after, bib", ren("s_bib_after")), (B, ren("s_stone_before"))]),
        ("Child Jizo / boat halo", [("child after", ren("s_child_after")), ("child " + B, ren("s_child_before")),
                                    ("boat halo after", ren("s_halo_after")), ("boat halo " + B, ren("s_halo_before"))]),
    ], "FX2 statues: each beside its CC0 reference (research/statues/REFS.md)",
        "Sculpted from the photos (spikes/FX2/figures.py; proportions research/statues/NOTES.md). Renders = the "
        "player's view (the figure's right hand on the viewer's left).")
    compose("fx2_komainu.jpg", [
        ("Komainu, upright form", [("ref: CMA 106262 (un)", ref("cma_106262_0.jpg")),
                                   ("ref: CMA 106263 (a)", ref("cma_106263_0.jpg")),
                                   ("pair: un (left) / a (right), 1.8 m figure", ren("k_pair_a"))]),
        ("Heads", [("ref: Met 53190", ref("met_53190_0.jpg")), ("a (open)", ren("k_head_a")),
                   ("un (closed, horn)", ren("k_head_un"))]),
        ("Compact Edo form / mossy", [("style b pair", ren("k_pair_b")), ("style a mossy pair", ren("k_pair_moss"))]),
        ("Inari foxes", [("ref: Met 60375 (fox netsuke)", ref("met_60375_0.jpg")),
                         ("key (left) / jewel (right)", ren("k_fox")), ("head + key", ren("k_fox_head"))]),
    ], "FX2 komainu + kitsune pairs (new)", "Placed: FX2.csv (SHOWCASE_MAP 'FX2', map fx2_map_guardians.jpg). No stone "
                                            "Inari fox photo in the open-access sets: the fox is general knowledge.")
    compose("fx2_detail.jpg", [
        ("Kagura masks", [("ref: CMA 149100 okina", ref("cma_149100_0.jpg")), ("ref: CMA 147048", ref("cma_147048_0.jpg")),
                          ("after", ren("d_masks_after")), (B, ren("d_masks_before"))]),
        ("Masks refs", [("CMA 147046 (onna)", ref("cma_147046_0.jpg")), ("CMA 148010 (usobuki)", ref("cma_148010_0.jpg"))]),
        ("Gong / bell / temple bell", [("after", ren("d_bells_after")), (B, ren("d_bells_before"))]),
        ("Ema + offering box", [("ref: Met 36108 (ema, 1631)", ref("met_36108_0.jpg")), ("after", ren("d_ema_after")),
                                (B, ren("d_ema_before"))]),
    ], "FX2 detail props (PLAYBOOK §12 detail budget)", "waniguchi, suzu, bonsho, ema rail + gaku-ema, offering box, "
                                                       "kagura masks + bell tree (spikes/FX2/detail_fx2.py)")
    compose("fx2_rope.jpg", [
        ("Wooden myojin, rope + shide", [("after (1.8 m figure)", ren("r_wood_myojin_rope_shide_after")),
                                         (B + " (FX1)", ren("r_wood_myojin_rope_shide_before"))]),
        ("Stone torii s, rope + shide", [("after", ren("r_stone_s_rope_shide_after")),
                                         (B + " (FX1)", ren("r_stone_s_rope_shide_before"))]),
    ], "FX2 torii rope: 3/4 of the original sag (FX1 halved it), 0.20 of the nuki height up, shide into the lay",
        "spikes/FX1/ropeclear.py: lowest placed rope / shide / tassel tip 2.31 m (>= 2.30), 0 LOW")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
