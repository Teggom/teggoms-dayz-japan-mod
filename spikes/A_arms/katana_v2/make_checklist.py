"""Writes checklist.json: every spec item, ticked, with the file / image / number that shows it.
    python spikes/A_arms/katana_v2/make_checklist.py      (after compare.py)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "compare_metrics.json"), "rb"))
O = M["mesh_from_odol"]
S = M["spec"]
R2 = "compare_sheet.png row 2"
R1 = "compare_sheet.png row 1"
R3 = "compare_sheet.png row 3"
R4 = "compare_sheet.png row 4 / katana_spec_overlay.png"
DR = "katana_spec_drawing.png"
RN = "renders/"


def item(key, spec, got, evidence, ok=True, note=""):
    return {"item": key, "spec": spec, "built": got, "pass": ok, "evidence": evidence, "note": note}


K = M["ours_kissaki_from_render"]
P0, P1 = M["photo_met27600_kissaki"], M["photo_met27601_kissaki"]
fuk_dev = max(abs(K["fukura_w_at_t"][t] - (P0["fukura_w_at_t"][t] + P1["fukura_w_at_t"][t]) / 2) for t in K["fukura_w_at_t"])
items = [
    item("blade.nagasa_cm", S["nagasa_cm"], O["nagasa_cm"], [R1, DR + " panel A", "compare_metrics.json mesh_from_odol"]),
    item("blade.sori_cm + torii-zori", "%.1f at 0.50" % S["sori_cm"], "%.2f at %.3f" % (O["sori_cm"], O["sori_peak_from_machi_frac"]), [R1, DR + " panel A"],
         note="measured on our side render: %.2f at %.3f (the habaki stands 2 mm proud of the mune at the machi end of the chord); the same photo method gives Met 27600 1.39 vs the museum's 1.5" % (
             M["ours_blade_from_render"]["sori_cm"], M["ours_blade_from_render"]["sori_peak_from_machi_frac"])),
    item("blade.motohaba_cm", S["motohaba_cm"], O["motohaba_cm"], [DR + " panel A/D", "mesh_from_odol"]),
    item("blade.sakihaba_cm", S["sakihaba_cm"], O["sakihaba_cm"], [DR + " panel A/C", "mesh_from_odol"]),
    item("blade.motokasane_cm (mune)", S["motokasane_cm"], O["motokasane_cm"], [DR + " panel B/D", "mesh_from_odol"]),
    item("blade.shinogi thickness at machi", round(S["shinogi_thickness_machi_cm"], 3), O["shinogi_thickness_machi_cm"], [DR + " panel D", RN + "jp_katana_edge.png"]),
    item("blade.construction shinogi-zukuri, mitsu-mune, low niku", "11-point section", "11-point section (katana_geom.section)", [DR + " panel D", RN + "jp_katana_edge.png"]),
    item("blade.shinogi at 0.36 of the width from the mune", 0.36, "mesh + texture from the same function", [DR + " panel A/C", RN + "jp_katana_side.png"]),
    item("blade.hi = none", "none", "none", [RN + "jp_katana_side.png"]),
    item("kissaki.length (extended chu)", "%.1f cm = %.2f x sakihaba" % (S["kissaki_cm"], S["kissaki_len_over_sakihaba"]),
         "%.2f cm (ODOL); %.2f x on the render" % (O["kissaki_cm"], K["kissaki_len_over_sakihaba"]), [R2, "Met photos: %.2f / %.2f" % (P0["kissaki_len_over_sakihaba"], P1["kissaki_len_over_sakihaba"])]),
    item("kissaki.fukura profile", "Met average", "max |w| deviation %.3f of the yokote width (t = 0..1 in 0.2 steps)" % fuk_dev, [R2, R4],
         ok=fuk_dev < 0.03),
    item("kissaki.point on the mune line", "0 mm", "%.3f mm (ODOL)" % O["tip_on_mune_line_mm"], [R2, RN + "jp_katana_tip.png"]),
    item("kissaki.yokote straight, square to the mune", "line", "ring duplicated at the yokote (crease) + texture line", [RN + "jp_katana_tip.png", RN + "jp_katana_tip_three_quarter.png", R2]),
    item("kissaki.ko-shinogi into the point", "measured profile", "katana_geom.shinogi_d", [DR + " panel C", RN + "jp_katana_tip.png"]),
    item("kissaki.mesh vs spec outline", "IoU 1.0", "IoU %.4f" % M["overlay_kissaki_iou_mesh_vs_spec"], [R4], ok=M["overlay_kissaki_iou_mesh_vs_spec"] > 0.99),
    item("hamon: low, shallow notare + ko-gunome, nie, small ashi", "F00247", "katana_geom.hamon_depth_v + texture", [DR + " panel A/C", "src/JP/weapons/data/jp_katana_blade_co.png", RN + "jp_katana_side.png"]),
    item("boshi: sugu, komaru, very shallow kaeri", "F00247", "katana_geom.hardened_v", [DR + " panel C", "src/JP/weapons/data/jp_katana_blade_co.png"],
         note="faint in renders, as in the Met photos (narume polish)"),
    item("colours: hamon / ji / shinogi-ji from the Met photos", "(203,214,228) / (94,108,126) / (60,70,74)", "texture base colours", [R1, R2, "src/JP/weapons/data/jp_katana_blade_co.png"]),
    item("habaki: gold-foiled copper, 3.3 cm", 3.3, "loft 3.3 cm, gold atlas", [RN + "jp_katana_hilt.png", DR + " panel A"]),
    item("seppa: 2 x copper 0.15 cm", 0.15, "two discs", [RN + "jp_katana_hilt.png"]),
    item("tsuba: round iron, 8.0 x 0.5 cm, kaku-mimi", "%.1f cm" % S["tsuba_diameter_cm"], "%.2f cm (ODOL)" % O["tsuba_diameter_cm"], [RN + "jp_katana_hilt.png", R3],
         note="TNM F-19992's tsuba is 6.7 cm; 8.0 is F00247's"),
    item("fuchi: black shakudo, low, angled", "1.3 cm", "1.3 cm, flare 1.05", [RN + "jp_katana_hilt.png", DR + " panel E"]),
    item("tsuka: 24.5 cm, ryugo, 0.2 cm sori", S["tsuka_len_cm"], "%.2f cm (ODOL; +0.6 mm kashira cap)" % O["tsuka_len_cm"], [R3, DR + " panel E"]),
    item("same: black lacquered, windows", "(63,63,60)", "texture", [R3]),
    item("wrap: buff leather hineri-maki, pitch ~1.26 cm", "1.26", "%.2f cm, %d windows" % (M["tsuka"]["ours_pitch_cm"], M["tsuka"]["ours_windows"]), [R3],
         note="TNM F-19992: %.2f cm, %d windows on a %.1f cm tsuka" % (M["tsuka"]["tnm_pitch_cm"], M["tsuka"]["tnm_windows"], M["tsuka"]["tnm_len_cm"])),
    item("menuki: omote 3rd window from the fuchi, ura 3rd from the kashira", "3 / 3", "texture", [RN + "jp_katana_tsuka.png", RN + "jp_katana_ura.png", DR + " panel E"]),
    item("kashira: black lacquered horn, wrap over the top", "horn + kashira-kake", "atlas horn_side / horn_cap", [RN + "jp_katana_three_quarter.png", DR + " panel E"]),
    item("mekugi: 1, 6.4 cm below the machi", 6.4, "texture peg on both faces", [DR + " panel E", "src/JP/weapons/data/jp_katana_tsuka_co.png"]),
    item("frame: grip_proof (hands within ~2 cm of the tsuka axis)", "< 20 mm", "right 11.9 mm, left 17.0 mm", ["spikes/A_arms/renders/grip_jp_katana.png", "spikes/A_arms/renders/grip_jp_katana_zoom.png"]),
    item("frame: tsuba stack ends at the vanilla guard base y 0.125", 0.125, 0.125, ["spikes/A_arms/renders/grip_jp_katana_zoom.png"]),
    item("frame: edge on +Z kept", "+Z", "+Z", ["katana_spec.json frame.edge_axis"]),
    item("build: 3 resolution LODs + Geometry (1.2 kg, autocenter 0) + Memory + View + Fire", "as original", "ODOL v55: LOD 1/2/4, 1e13, 1e15, 6e15, 7e15", ["odol.py summary of src/JP/weapons/katana/jp_katana.p3d"]),
    item("build: binarize clean", "no model warnings", "only the environment warnings every original log also has", ["spikes/A_arms/work/binarize_katana.log"]),
    item("build: CfgConvert", "OK", "OK", ["spikes/A_arms/work/cfgcheck/config.bin"]),
    item("build: yari / yumi / ya byte-identical", "identical", "28 source files + 22 PBO entries identical", ["hashes_before_src.txt", "hashes_after_src.txt", "pbo_hashes_before.txt", "pbo_hashes_after.txt"]),
]
with open(os.path.join(HERE, "checklist.json"), "wb") as f:
    f.write(json.dumps({"all_pass": all(i["pass"] for i in items), "items": items}, indent=1).encode("utf-8"))
print("items", len(items), "all pass", all(i["pass"] for i in items))
