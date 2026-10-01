"""FP1 shots: SHOTS[group] = [(shot, [master p3d (DEV-relative)], view (x, front, up) in model terms, tight, lod
[, offsets])]. Rendered by render_fp1.py (back faces culled, as the game draws them)."""
B3A = "spikes/B3a/out/"
B3B = "spikes/B3b/out/"
L1 = "spikes/L1/out/"
L2 = "spikes/L2/out/"
S1 = "spikes/S1/out/"

SHOTS = {
    "f6": [
        ("f6_charcoal_stack", [L2 + "yard_life/jp_s_charcoal_bales_stack.p3d"], (-1.0, 0.6, 0.25), 0.9, 1.0),
        ("f6_charcoal_burst", [L2 + "yard_life/jp_s_charcoal_bales_ab_burst.p3d"], (0.4, 1.0, 0.35), 0.9, 1.0),
        ("f6_charcoal_bales3", [L1 + "meal/jp_f_charcoal_bales3.p3d"], (0.3, 1.0, -0.05), 0.9, 1.0),
        ("f6_tawara", [B3A + "storage/jp_f_tawara.p3d"], (1.0, 0.4, 0.2), 0.9, 1.0),
        ("f6_tawara_stack", [B3B + "yard/jp_s_straw_stack_tawara_stack.p3d"], (0.5, 1.0, 0.3), 0.9, 1.0),
        ("f6_charcoal_stack_b", [L2 + "yard_life/jp_s_charcoal_bales_stack.p3d"], (1.0, 0.6, 0.25), 0.9, 1.0),
        ("f6_charcoal_burst_b", [L2 + "yard_life/jp_s_charcoal_bales_ab_burst.p3d"], (-0.6, -1.0, 0.35), 0.9, 1.0),
        ("f6_charcoal_bales3_b", [L1 + "meal/jp_f_charcoal_bales3.p3d"], (0.3, -1.0, 0.1), 0.9, 1.0),
        ("f6_taru_komo", [L1 + "meal/jp_f_taru_komo.p3d"], (0.5, 1.0, 0.5), 0.9, 1.0),
    ],
    "f11": [
        ("f11_slumped", [B3B + "yard/jp_s_straw_stack_ab_slumped.p3d"], (0.6, 1.0, 0.45), 0.9, 1.0),
        ("f11_slumped_top", [B3B + "yard/jp_s_straw_stack_ab_slumped.p3d"], (0.2, 0.4, 1.0), 0.9, 1.0),
    ],
    "f7": [
        ("f7_chochin_a", [L2 + "street_life/jp_s_lantern_fallen_chochin.p3d"], (0.5, 1.0, 0.5), 0.9, 1.0),
        ("f7_chochin_b", [L2 + "street_life/jp_s_lantern_fallen_chochin.p3d"], (-0.5, -1.0, 0.5), 0.9, 1.0),
        ("f7_chochin_c", [L2 + "street_life/jp_s_lantern_fallen_chochin.p3d"], (-1.0, 0.3, 0.3), 0.9, 1.0),
        ("f7_chochin_d", [L2 + "street_life/jp_s_lantern_fallen_chochin.p3d"], (1.0, -0.3, 0.3), 0.9, 1.0),
        ("f7_crushed", [L2 + "street_life/jp_s_lantern_fallen_crushed.p3d"], (0.5, 1.0, 0.5), 0.9, 1.0),
        ("f7_andon", [L2 + "street_life/jp_s_lantern_fallen_andon.p3d"], (0.5, 1.0, 0.5), 0.9, 1.0),
    ],
    "f8": [
        ("f8_loom", [L1 + "work/jp_f_izaribata.p3d"], (1.0, 0.25, 0.05), 0.9, 1.0),
        ("f8_wheel", [L1 + "work/jp_f_itoguruma.p3d"], (1.0, 0.25, 0.05), 0.9, 1.0),
        ("f8_loom_front", [L1 + "work/jp_f_izaribata.p3d"], (0.2, 1.0, 0.12), 0.9, 1.0),
        ("f8_wheel_front", [L1 + "work/jp_f_itoguruma.p3d"], (0.2, 1.0, 0.12), 0.9, 1.0),
        ("f8_loom_top", [L1 + "work/jp_f_izaribata.p3d"], (0.6, 0.8, 0.8), 0.9, 1.0),
        ("f8_wheel_top", [L1 + "work/jp_f_itoguruma.p3d"], (0.6, 0.8, 0.8), 0.9, 1.0),
    ],
    "f5": [
        ("f5_shu_snapped", [B3B + "shrine/jp_s_torii_wood_ab_leaning_shu.p3d"], (0.45, 1.0, 0.25), 0.55, 1.0),
        ("f5_rope_myojin", [B3B + "shrine/jp_s_torii_wood_myojin_rope_shide.p3d"], (0.25, 1.0, 0.05), 0.42, 1.0),
        ("f5_shimenawa_len", [B3B + "roadside/jp_s_shimenawa_len_1ken.p3d"], (0.3, 1.0, 0.2), 0.8, 1.0),
        ("f5_shimenawa_wrap", [B3B + "roadside/jp_s_shimenawa_wrap_d06.p3d"], (0.3, 1.0, 0.3), 0.8, 1.0),
        ("f5_shimenawa_tattered", [B3B + "roadside/jp_s_shimenawa_ab_tattered.p3d"], (0.3, 1.0, 0.3), 0.8, 1.0),
    ],
    "f10": [
        ("f10_torii_stone_l", [B3B + "shrine/jp_s_torii_stone_l.p3d"], (0.35, 1.0, 0.15), 0.85, 1.0),
        ("f10_torii_stone_s_moss", [B3B + "shrine/jp_s_torii_stone_s_moss.p3d"], (0.35, 1.0, 0.15), 0.85, 1.0),
        ("f10_lantern", [B3B + "shrine/jp_s_stone_lantern_kasuga_24.p3d"], (0.35, 1.0, 0.2), 0.85, 1.0),
    ],
    "f1": [
        ("f1_broom_pile", [L2 + "yard_life/jp_s_leaf_pile_broom.p3d"], (0.5, 1.0, 0.6), 0.75, 1.0),
        ("f1_broom_close", [L2 + "yard_life/jp_s_leaf_pile_broom.p3d"], (0.05, 0.5, 1.0), 0.55, 1.0),
        ("f1_aramono", [S1 + "shopgoods/jp_f_sg_aramono.p3d"], (0.3, 1.0, 0.7), 0.7, 1.0),
        ("f1_broom_scattered", [L2 + "yard_life/jp_s_leaf_pile_ab_scattered.p3d"], (0.5, 1.0, 0.6), 0.75, 1.0),
    ],
    "f2": [
        ("f2_hasa_low", [L2 + "yard_life/jp_s_hasa_low.p3d"], (0.45, 1.0, 0.25), 0.8, 1.0),
        ("f2_hasa_low_close", [L2 + "yard_life/jp_s_hasa_low.p3d"], (0.6, 1.0, 0.15), 0.42, 1.0),
        ("f2_hasa_tiers", [L2 + "yard_life/jp_s_hasa_tiers.p3d"], (0.45, 1.0, 0.25), 0.8, 1.0),
        ("f2_hasa_sagged", [L2 + "yard_life/jp_s_hasa_ab_sagged.p3d"], (0.45, 1.0, 0.25), 0.8, 1.0),
        ("f2_stook", [B3B + "yard/jp_s_straw_stack_stook.p3d"], (0.5, 1.0, 0.4), 0.8, 1.0),
    ],
    "f3": [
        ("f3_potted_stand", [L2 + "yard_life/jp_s_potted_stand.p3d"], (0.4, 1.0, 0.45), 0.8, 1.0),
        ("f3_potted_pair", [L2 + "yard_life/jp_s_potted_pair.p3d"], (0.4, 1.0, 0.45), 0.8, 1.0),
        ("f3_potted_dead", [L2 + "yard_life/jp_s_potted_ab_dead.p3d"], (0.4, 1.0, 0.45), 0.8, 1.0),
        ("f3_pine_close", [L2 + "yard_life/jp_s_potted_pair.p3d"], (0.2, 1.0, 0.25), 0.55, 1.0),
        ("f3_potted_fallen", [L2 + "yard_life/jp_s_potted_ab_fallen.p3d"], (0.4, 1.0, 0.45), 0.8, 1.0),
    ],
    "f4": [
        ("f4_katana_stand", [L1 + "tier/jp_f_katanakake_stand.p3d"], (0.35, 1.0, 0.25), 0.75, 1.0),
        ("f4_katana_stand_close", [L1 + "tier/jp_f_katanakake_stand.p3d"], (0.6, 1.0, 0.35), 0.45, 1.0),
        ("f4_katana_wall", [L1 + "tier/jp_f_katanakake_wall.p3d"], (0.35, 1.0, 0.25), 0.75, 1.0),
    ],
    "f12": [
        ("f12_lever_well", [B3B + "water/jp_s_well_hanetsurube_well.p3d"], (1.0, 0.45, 0.25), 0.85, 1.0),
        ("f12_lever_field", [B3B + "water/jp_s_well_hanetsurube_field.p3d"], (1.0, 0.45, 0.25), 0.85, 1.0),
    ],
    "f13": [
        ("f13_kosatsu_std", [B3B + "roadside/jp_s_kosatsu_std.p3d"], (0.45, 1.0, 0.3), 0.8, 1.0),
        ("f13_kosatsu_side", [B3B + "roadside/jp_s_kosatsu_std.p3d"], (1.0, 0.25, 0.2), 0.8, 1.0),
        ("f13_kosatsu_large", [B3B + "roadside/jp_s_kosatsu_large.p3d"], (0.45, 1.0, 0.3), 0.8, 1.0),
        ("f13_kosatsu_forest", [B3B + "roadside/jp_s_kosatsu_forest.p3d"], (0.45, 1.0, 0.3), 0.8, 1.0),
    ],
    "f14": [
        ("f14_ladder_tower", [L2 + "street_life/jp_s_fire_watch_ladder_tower.p3d"], (0.5, 1.0, 0.3), 0.85, 1.0),
    ],
    "f15": [
        ("f15_shinmei_rot", [B3B + "shrine/jp_s_torii_fallen_shinmei_rot.p3d"], (0.5, 1.0, 0.6), 0.85, 1.0),
        ("f15_myojin_typhoon", [B3B + "shrine/jp_s_torii_fallen_myojin_typhoon.p3d"], (0.5, 1.0, 0.6), 0.85, 1.0),
        ("f15_shu_snapped", [B3B + "shrine/jp_s_torii_fallen_shu_snapped.p3d"], (0.5, 1.0, 0.6), 0.85, 1.0),
        ("f15_stone_quake", [B3B + "shrine/jp_s_torii_fallen_stone_quake.p3d"], (0.5, 1.0, 0.6), 0.85, 1.0),
        ("f15_stone_quake_old", [B3B + "shrine/jp_s_torii_fallen_stone_quake_old.p3d"], (0.5, 1.0, 0.6), 0.85, 1.0),
    ],
}
