"""FP2 shots: SHOTS[group] = [(shot, [master p3d (DEV-relative)], view (x, front, up) in model terms, tight, lod
[, offsets])]. Rendered by render_fp2.py (back faces culled, as the game draws them)."""
B3A = "spikes/B3a/out/"
B3B = "spikes/B3b/out/"
L1 = "spikes/L1/out/"
L2 = "spikes/L2/out/"
S1 = "spikes/S1/out/"

SHOTS = {
    "f1": [
        ("f1_wall_h120", [B3B + "yard/jp_s_firewood_stack_wall_1ken_h120.p3d"], (0.45, 1.0, 0.35), 0.9, 1.0),
        ("f1_wall_h120_close", [B3B + "yard/jp_s_firewood_stack_wall_1ken_h120.p3d"], (0.25, 1.0, 0.15), 0.55, 1.0),
        ("f1_wall_h180", [B3B + "yard/jp_s_firewood_stack_wall_1ken_h180.p3d"], (-0.5, 1.0, 0.3), 0.9, 1.0),
        ("f1_half", [B3B + "yard/jp_s_firewood_stack_half.p3d"], (0.6, 1.0, 0.35), 0.9, 1.0),
        ("f1_free_posts", [B3B + "yard/jp_s_firewood_stack_free_posts.p3d"], (0.6, 1.0, 0.45), 0.9, 1.0),
        ("f1_collapsed", [B3B + "yard/jp_s_firewood_stack_ab_collapsed.p3d"], (0.5, 1.0, 0.45), 0.9, 1.0),
        ("f1_f_stack", [B3A + "kitchen/jp_f_firewood_stack.p3d"], (0.5, 1.0, 0.5), 0.9, 1.0),
        ("f1_f_low", [B3A + "kitchen/jp_f_firewood_low.p3d"], (0.5, 1.0, 0.5), 0.9, 1.0),
        ("f1_wall_h120_r2", [B3B + "yard/jp_s_firewood_stack_wall_1ken_h120.p3d"], (0.45, 1.0, 0.35), 0.9, 2.0),
    ],
    "f2": [
        ("f2_usu_mallet", [L1 + "work/jp_f_usu_mallet.p3d"], (0.8, 1.0, 0.35), 0.9, 1.0),
        ("f2_usu_mallet_side", [L1 + "work/jp_f_usu_mallet.p3d"], (1.0, 0.05, 0.12), 0.9, 1.0),
        ("f2_usu", [L1 + "work/jp_f_usu.p3d"], (0.4, 1.0, 0.3), 0.9, 1.0),
        ("f2_usu_side", [L1 + "work/jp_f_usu.p3d"], (0.05, 1.0, 0.08), 0.9, 1.0),
        ("f2_usu_fallen", [L1 + "work/jp_f_usu_fallen.p3d"], (0.4, 1.0, 0.5), 0.9, 1.0),
    ],
    "f3": [
        ("f3_rope_pegs_3", [L1 + "wall/jp_f_rope_pegs_3.p3d"], (0.15, 1.0, 0.05), 0.7, 1.0),
        ("f3_rope_pegs_fallen", [L1 + "wall/jp_f_rope_pegs_fallen.p3d"], (0.4, 1.0, 0.5), 0.9, 1.0),
        ("f3_shimenawa_2ken", [B3B + "roadside/jp_s_shimenawa_len_2ken.p3d"], (0.1, 1.0, 0.05), 0.5, 1.0),
        ("f3_shimenawa_wrap", [B3B + "roadside/jp_s_shimenawa_wrap_d10.p3d"], (0.3, 1.0, 0.15), 0.8, 1.0),
        ("f3_torii_rope", [B3B + "shrine/jp_s_torii_wood_myojin_rope_shide.p3d"], (0.15, 1.0, 0.1), 0.45, 1.0),
        ("f3_well_tsurube", [B3B + "water/jp_s_well_tsurube_roofed.p3d"], (0.4, 1.0, 0.25), 0.55, 1.0),
        ("f3_tawara", [B3A + "storage/jp_f_tawara.p3d"], (1.0, 0.4, 0.2), 0.9, 1.0),
    ],
}
SHOTS["f1x"] = [
    ("f1_h120_endtop", [B3B + "yard/jp_s_firewood_stack_wall_1ken_h120.p3d"], (-1.0, 0.7, 0.8), 0.45, 1.0),
    ("f1_h120_eye", [B3B + "yard/jp_s_firewood_stack_wall_1ken_h120.p3d"], (0.3, 1.0, 0.25), 0.7, 1.0),
]
